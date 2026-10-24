#!/usr/bin/env python3
"""Make our own overlay / background clips (no download, no credit: made by us) with PIL + numpy -> H.264 mp4.

    python3 library/tools/make_overlays.py library/stock/own            # all clips
    python3 library/tools/make_overlays.py out/ --only embers-rising,film-grain
    python3 library/tools/make_overlays.py --list

Black-background clips are for `mix-blend-mode: screen` (or ffmpeg blend=all_mode=screen); `film-grain` is mid-grey for
`overlay` blend; `*-greenscreen` clips are on pure #00FF00 for chroma key (ffmpeg colorkey=0x00FF00:0.3:0.1).
Deterministic (fixed seeds). Soft looks are drawn at half size and upscaled by ffmpeg.
"""
import argparse
import math
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

FPS = 30


def writer(path, w, h, out_w=None, out_h=None, crf=21, maxrate="6M"):
    vf = f"scale={out_w}:{out_h}:flags=bicubic," if out_w else ""
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-r", str(FPS), "-i", "-",
           "-vf", vf + "format=yuv420p", "-c:v", "libx264", "-preset", "medium", "-crf", str(crf), "-maxrate", maxrate,
           "-bufsize", "12M", "-movflags", "+faststart", path]
    return subprocess.Popen(cmd, stdin=subprocess.PIPE)


def run(path, w, h, n, frame_fn, out=None, **kw):
    p = writer(path, w, h, *(out or (None, None)), **kw)
    for i in range(n):
        im = frame_fn(i)
        p.stdin.write(np.asarray(im.convert("RGB"), np.uint8).tobytes())
    p.stdin.close()
    p.wait()


def smooth_noise(rng, steps, k):
    """k smooth random walks (values ~ -1..1) over `steps` frames."""
    x = rng.standard_normal((steps // 30 + 3, k))
    t = np.linspace(0, len(x) - 3, steps)
    i = t.astype(int)
    f = (t - i)[:, None]
    f = f * f * (3 - 2 * f)
    return x[i] * (1 - f) + x[i + 1] * f


# ---- generators: each returns (w, h, n_frames, frame_fn, out_size) ---------------------------------------
def light_leak(colors, seed, secs=10, w=960, h=540, out=(1920, 1080)):
    rng = np.random.default_rng(seed)
    n = secs * FPS
    k = len(colors)
    wx = smooth_noise(rng, n, k)
    wy = smooth_noise(rng, n, k)
    amp = smooth_noise(rng, n, k)

    def f(i):
        im = Image.new("RGB", (w, h))
        d = ImageDraw.Draw(im)
        for j, c in enumerate(colors):
            cx = w * (0.15 + 0.7 * (j / max(k - 1, 1))) + wx[i, j] * w * 0.25
            cy = h * 0.5 + wy[i, j] * h * 0.35
            r = h * max(0.12, 0.35 + 0.15 * amp[i, j])
            a = 0.55 + 0.35 * amp[i, j]
            d.ellipse([cx - r * 1.6, cy - r, cx + r * 1.6, cy + r], fill=tuple(int(v * max(a, 0.1)) for v in c))
        return im.filter(ImageFilter.GaussianBlur(h * 0.18))
    return w, h, n, f, out


def film_grain(secs=6, w=1920, h=1080, strength=26):
    rng = np.random.default_rng(1)

    def f(i):
        g = rng.normal(128, strength, (h // 2, w // 2)).clip(0, 255).astype(np.uint8)
        im = Image.fromarray(g).resize((w, h), Image.BILINEAR)
        return im.convert("RGB")
    return w, h, secs * FPS, f, None


def dust_scratches(secs=8, w=1920, h=1080):
    rng = np.random.default_rng(2)

    def f(i):
        im = Image.new("L", (w, h))
        d = ImageDraw.Draw(im)
        for _ in range(rng.integers(6, 22)):
            x, y = rng.uniform(0, w), rng.uniform(0, h)
            r = rng.uniform(1, 4)
            d.ellipse([x - r, y - r * rng.uniform(0.5, 1.5), x + r, y + r], fill=int(rng.uniform(120, 255)))
        for _ in range(rng.integers(0, 4)):  # hairs
            x, y = rng.uniform(0, w), rng.uniform(0, h)
            pts = [(x + 25 * math.sin(t / 3 + x), y + t * 6) for t in range(int(rng.uniform(5, 20)))]
            d.line(pts, fill=int(rng.uniform(100, 200)), width=2)
        if rng.random() < 0.35:  # vertical scratch
            x = rng.uniform(0, w)
            d.line([(x, 0), (x + rng.uniform(-8, 8), h)], fill=int(rng.uniform(90, 200)), width=int(rng.integers(1, 3)))
        return im.filter(ImageFilter.GaussianBlur(0.8)).convert("RGB")
    return w, h, secs * FPS, f, None


def bokeh(palette, seed, secs=10, w=960, h=540, out=(1920, 1080), count=34):
    rng = np.random.default_rng(seed)
    n = secs * FPS
    x0, y0 = rng.uniform(0, w, count), rng.uniform(0, h, count)
    vx, vy = rng.uniform(-8, 8, count), rng.uniform(-14, -2, count)
    r = rng.uniform(10, 45, count)
    col = [palette[j % len(palette)] for j in range(count)]
    ph = rng.uniform(0, 6.28, count)

    def f(i):
        t = i / FPS
        lay = Image.new("RGB", (w, h))
        d = ImageDraw.Draw(lay)
        for j in range(count):
            x = (x0[j] + vx[j] * t) % (w + 100) - 50
            y = (y0[j] + vy[j] * t) % (h + 100) - 50
            a = 0.35 + 0.25 * math.sin(ph[j] + t * 0.8)
            d.ellipse([x - r[j], y - r[j], x + r[j], y + r[j]], fill=tuple(int(v * a) for v in col[j]))
        im = lay
        return im.filter(ImageFilter.GaussianBlur(2.2))
    return w, h, n, f, out


def particles(kind, seed, secs=10, w=1920, h=1080):
    """embers (rising orange), sparks (fast burst + gravity), snow (falling white), rain (streaks)."""
    rng = np.random.default_rng(seed)
    n = secs * FPS
    N = {"embers": 220, "sparks": 260, "snow": 260, "rain": 420}[kind]
    x, y = rng.uniform(0, w, N), rng.uniform(0, h, N)
    size = rng.uniform(2, 6, N) if kind != "snow" else rng.uniform(1.5, 5, N)
    life = rng.uniform(0, 1, N)
    vx = rng.uniform(-30, 30, N)
    vy = {"embers": rng.uniform(-160, -60, N), "sparks": rng.uniform(-900, -300, N),
          "snow": rng.uniform(40, 120, N), "rain": rng.uniform(1600, 2200, N)}[kind]
    st = {"x": x, "y": y, "vx": vx, "vy": vy}

    def reset(m):
        c = m.sum()
        if kind == "sparks":
            st["x"][m] = w / 2 + rng.normal(0, 60, c)
            st["y"][m] = h + 10
            st["vx"][m] = rng.normal(0, 380, c)
            st["vy"][m] = rng.uniform(-1300, -500, c)
        elif kind == "embers":
            st["x"][m] = rng.uniform(0, w, c)
            st["y"][m] = h + rng.uniform(0, 80, c)
        else:
            st["x"][m] = rng.uniform(-200, w, c)
            st["y"][m] = rng.uniform(-200, -10, c)
        life[m] = 0

    def f(i):
        dt = 1 / FPS
        t = i * dt
        if kind == "sparks":
            st["vy"] += 900 * dt
        if kind in ("embers", "snow"):
            st["vx"] += np.sin(t * 1.3 + st["y"] / 90) * 6
        st["x"] += st["vx"] * dt
        st["y"] += st["vy"] * dt
        life[:] += dt / {"embers": 5, "sparks": 1.6, "snow": 12, "rain": 2}[kind]
        out = (st["y"] < -60) | (st["y"] > h + 120) | (life > 1)
        if out.any():
            reset(out)
        im = Image.new("RGB", (w, h))
        d = ImageDraw.Draw(im)
        for j in range(N):
            xx, yy, s = st["x"][j], st["y"][j], size[j]
            if kind == "rain":
                d.line([(xx, yy), (xx + st["vx"][j] * 0.02, yy + st["vy"][j] * 0.02)], fill=(150, 165, 185), width=1)
            elif kind == "snow":
                d.ellipse([xx - s, yy - s, xx + s, yy + s], fill=(235, 240, 255))
            else:
                fade = max(0.0, 1 - life[j]) if kind == "embers" else max(0.0, 1 - life[j] * 0.9)
                c = (255, int(120 + 100 * fade), int(30 * fade)) if kind == "embers" else (255, 210, 120)
                c = tuple(int(v * fade) for v in c)
                if kind == "sparks":
                    d.line([(xx, yy), (xx - st["vx"][j] * 0.025, yy - st["vy"][j] * 0.025)], fill=c, width=2)
                else:
                    d.ellipse([xx - s, yy - s, xx + s, yy + s], fill=c)
        glow = im.filter(ImageFilter.GaussianBlur(6 if kind in ("embers", "sparks") else 1.2))
        a = np.asarray(im, np.uint16) + (np.asarray(glow, np.uint16) * (2 if kind in ("embers", "sparks") else 1))
        return Image.fromarray(a.clip(0, 255).astype(np.uint8))
    return w, h, n, f, None


def confetti_green(seed=7, secs=8, w=1920, h=1080, N=220):
    rng = np.random.default_rng(seed)
    cols = [(255, 64, 96), (255, 200, 40), (60, 140, 255), (255, 255, 255), (180, 80, 255), (255, 130, 40)]
    x, y = rng.uniform(0, w, N), rng.uniform(-1.6 * h, 0.1 * h, N)
    vy, vx = rng.uniform(170, 330, N), rng.uniform(-40, 40, N)
    ang, spin = rng.uniform(0, 6.28, N), rng.uniform(-8, 8, N)
    c = [cols[j % len(cols)] for j in range(N)]
    sw, sh = rng.uniform(22, 40, N), rng.uniform(11, 20, N)

    def f(i):
        t = i / FPS
        im = Image.new("RGB", (w, h), (0, 255, 0))
        d = ImageDraw.Draw(im)
        for j in range(N):
            yy = y[j] + vy[j] * t
            if yy > h + 30:
                continue
            xx = x[j] + vx[j] * t + 25 * math.sin(t * 2 + j)
            a = ang[j] + spin[j] * t
            flip = abs(math.cos(a * 0.7))
            hw, hh = sw[j] / 2, sh[j] / 2 * max(flip, 0.15)
            pts = [(xx + px * math.cos(a) - py * math.sin(a), yy + px * math.sin(a) + py * math.cos(a))
                   for px, py in ((-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh))]
            d.polygon(pts, fill=c[j])
        return im
    return w, h, secs * FPS, f, None


def gradient_flow(colors, seed, secs=10, w=480, h=270, out=(1920, 1080)):
    rng = np.random.default_rng(seed)
    n = secs * FPS
    yy, xx = np.mgrid[0:h, 0:w] / max(w, h)
    cols = np.array(colors, float)
    ph = rng.uniform(0, 6.28, (len(colors), 3))

    def f(i):
        t = i / FPS * 0.35
        acc = np.zeros((h, w, 3))
        wsum = np.zeros((h, w, 1))
        for j, c in enumerate(cols):
            cx = 0.5 + 0.45 * math.sin(t * (0.6 + 0.2 * j) + ph[j, 0])
            cy = 0.28 + 0.25 * math.cos(t * (0.5 + 0.15 * j) + ph[j, 1])
            wgt = np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / 0.05)[..., None] + 1e-3
            acc += wgt * c
            wsum += wgt
        return Image.fromarray((acc / wsum).clip(0, 255).astype(np.uint8))
    return w, h, n, f, out


def tech_grid(secs=10, w=1920, h=1080, color=(0, 220, 255)):
    n = secs * FPS

    def f(i):
        im = Image.new("RGB", (w, h), (4, 6, 16))
        d = ImageDraw.Draw(im)
        hy = h * 0.42
        off = (i / FPS * 0.6) % 1
        for k in range(1, 26):  # horizontal lines receding
            z = k - off
            if z <= 0.05:
                continue
            y = hy + (h - hy) * (1.4 / z) ** 1.0 * 0.35
            if y > h:
                continue
            a = min(1, 2.5 / z)
            d.line([(0, y), (w, y)], fill=tuple(int(v * a) for v in color), width=2)
        for k in range(-24, 25):
            x_bottom = w / 2 + k * 160
            d.line([(w / 2 + k * 6, hy), (x_bottom, h)], fill=tuple(int(v * 0.7) for v in color), width=2)
        glow = im.filter(ImageFilter.GaussianBlur(5))
        a = np.asarray(im, np.uint16) + np.asarray(glow, np.uint16)
        sky = np.linspace(1, 0, int(hy))[:, None, None] * np.array([40, 10, 70]) * 0.9
        a[:int(hy)] += sky.astype(np.uint16)
        return Image.fromarray(a.clip(0, 255).astype(np.uint8))
    return w, h, n, f, None


def particle_network(seed=9, secs=10, w=1920, h=1080, N=70):
    rng = np.random.default_rng(seed)
    p = rng.uniform([0, 0], [w, h], (N, 2))
    v = rng.normal(0, 25, (N, 2))

    def f(i):
        q = p + v * (i / FPS)
        q[:, 0] = np.abs((q[:, 0] + w) % (2 * w) - w)
        q[:, 1] = np.abs((q[:, 1] + h) % (2 * h) - h)
        im = Image.new("RGB", (w, h), (6, 10, 28))
        d = ImageDraw.Draw(im)
        dist = np.linalg.norm(q[:, None] - q[None], axis=-1)
        for a in range(N):
            for b in range(a + 1, N):
                if dist[a, b] < 260:
                    s = 1 - dist[a, b] / 260
                    d.line([tuple(q[a]), tuple(q[b])], fill=(int(40 * s), int(140 * s), int(255 * s)), width=1)
        for a in range(N):
            d.ellipse([q[a, 0] - 3, q[a, 1] - 3, q[a, 0] + 3, q[a, 1] + 3], fill=(140, 210, 255))
        return im
    return w, h, secs * FPS, f, None


def starfield(seed=10, secs=10, w=1920, h=1080, N=500):
    rng = np.random.default_rng(seed)
    x, y = rng.uniform(0, w, N), rng.uniform(0, h, N)
    b, ph, s = rng.uniform(80, 255, N), rng.uniform(0, 6.28, N), rng.uniform(0.6, 2.2, N)

    def f(i):
        t = i / FPS
        im = Image.new("RGB", (w, h), (2, 3, 10))
        d = ImageDraw.Draw(im)
        for j in range(N):
            v = int(b[j] * (0.6 + 0.4 * math.sin(ph[j] + t * 2.2)))
            xx = (x[j] + t * 6 * s[j]) % w
            d.ellipse([xx - s[j], y[j] - s[j], xx + s[j], y[j] + s[j]], fill=(v, v, min(255, v + 20)))
        return im
    return w, h, secs * FPS, f, None


def smoke_fog(seed=11, secs=10, w=480, h=270, out=(1920, 1080), tint=(200, 205, 215)):
    rng = np.random.default_rng(seed)
    layers = [rng.standard_normal((h // s + 2, w // s + 2)) for s in (60, 30, 15)]
    n = secs * FPS

    def f(i):
        t = i / FPS
        acc = np.zeros((h, w))
        for k, (L, s) in enumerate(zip(layers, (60, 30, 15))):
            im = Image.fromarray(((L - L.min()) / (np.ptp(L)) * 255).astype(np.uint8))
            big = np.asarray(im.resize(((w // s + 2) * s, (h // s + 2) * s), Image.BICUBIC), float) / 255
            dx = int(t * (12 + 10 * k)) % s
            acc += big[: h, dx: dx + w] * (0.55 / (k + 1))
        acc = np.clip((acc - 0.4) * 1.5, 0, 1) ** 1.5 * np.linspace(0.4, 1, h)[:, None]
        rgb = (acc[..., None] * np.array(tint)).astype(np.uint8)
        return Image.fromarray(rgb).filter(ImageFilter.GaussianBlur(6))
    return w, h, n, f, out


def film_burn(secs=3, w=960, h=540, out=(1920, 1080)):
    """Transition: an orange-white burn sweeps in, peaks at 1.5 s (fills the frame), then clears."""
    n = secs * FPS
    rng = np.random.default_rng(12)
    noise = np.asarray(Image.fromarray((rng.random((h // 8, w // 8)) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), float) / 255
    xx = np.linspace(0, 1, w)[None, :]

    def f(i):
        p = i / (n - 1)
        front = 1.6 * math.sin(math.pi * p) - 0.3
        m = np.clip((front - xx * 0.8 + noise * 0.5 - 0.25) * 3, 0, 1)
        col = np.stack([m * 255, m ** 1.4 * 190, m ** 3 * 120], -1)
        return Image.fromarray(col.clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(12))
    return w, h, n, f, out


def glitch_overlay(seed=13, secs=4, w=1920, h=1080):
    rng = np.random.default_rng(seed)

    def f(i):
        im = Image.new("RGB", (w, h))
        if rng.random() < 0.55:
            d = ImageDraw.Draw(im)
            for _ in range(rng.integers(3, 14)):
                y = rng.uniform(0, h)
                hh = rng.uniform(4, 60)
                x = rng.uniform(-200, w)
                c = [(255, 0, 80), (0, 255, 220), (255, 255, 255), (80, 80, 255)][rng.integers(4)]
                d.rectangle([x, y, x + rng.uniform(100, 900), y + hh], fill=c)
        return im
    return w, h, secs * FPS, f, None


V = (1080, 1920)
CLIPS = {
    "light-leak-warm": ("overlay", "screen", "warm orange/gold light leak drifting", lambda: light_leak([(255, 140, 40), (255, 80, 30), (255, 210, 120)], 1)),
    "light-leak-pink": ("overlay", "screen", "pink/magenta light leak", lambda: light_leak([(255, 70, 140), (255, 140, 90), (200, 60, 255)], 2)),
    "light-leak-blue": ("overlay", "screen", "cool blue/cyan light leak", lambda: light_leak([(40, 140, 255), (80, 255, 230), (140, 90, 255)], 3)),
    "light-leak-warm-vertical": ("overlay", "screen", "warm light leak 9:16", lambda: light_leak([(255, 140, 40), (255, 80, 30), (255, 210, 120)], 4, w=540, h=960, out=V)),
    "film-grain": ("overlay", "overlay", "mid-grey animated grain (blend overlay/soft-light, 20-40%)", film_grain),
    "dust-scratches": ("overlay", "screen", "old-film dust, hairs and scratches on black", dust_scratches),
    "film-burn-transition": ("transition", "screen", "3 s orange film burn, fills frame at 1.5 s: cut under it", film_burn),
    "glitch-overlay": ("overlay", "screen", "RGB glitch bars on black, flickering 4 s", glitch_overlay),
    "bokeh-warm": ("overlay", "screen", "warm golden bokeh circles drifting up", lambda: bokeh([(255, 190, 90), (255, 140, 60), (255, 230, 170)], 5)),
    "bokeh-blue-pink": ("overlay", "screen", "blue and pink bokeh (night, party)", lambda: bokeh([(80, 140, 255), (255, 90, 170), (170, 120, 255)], 6)),
    "bokeh-warm-vertical": ("overlay", "screen", "warm bokeh 9:16", lambda: bokeh([(255, 190, 90), (255, 140, 60), (255, 230, 170)], 7, w=540, h=960, out=V)),
    "embers-rising": ("fire", "screen", "orange embers/sparks rising (fire, gaming, Minecraft promos)", lambda: particles("embers", 8)),
    "sparks-fountain": ("fire", "screen", "spark fountain from bottom centre with gravity", lambda: particles("sparks", 9)),
    "embers-rising-vertical": ("fire", "screen", "rising embers 9:16", lambda: particles("embers", 10, w=1080, h=1920)),
    "snow-falling": ("weather", "screen", "white snow falling on black", lambda: particles("snow", 11)),
    "rain-streaks": ("weather", "screen", "rain streaks on black", lambda: particles("rain", 12)),
    "smoke-fog": ("fire", "screen", "drifting grey fog/smoke on black", smoke_fog),
    "confetti-greenscreen": ("celebration", "chroma key #00FF00", "confetti falling on green screen", confetti_green),
    "gradient-purple-blue": ("abstract", "background", "slow purple/blue/pink gradient loop", lambda: gradient_flow([(90, 30, 160), (30, 80, 220), (220, 60, 150), (20, 20, 60)], 14)),
    "gradient-warm": ("abstract", "background", "slow orange/red/gold gradient", lambda: gradient_flow([(255, 120, 40), (200, 30, 60), (255, 200, 80), (60, 10, 20)], 15)),
    "gradient-teal-green": ("abstract", "background", "teal/green/navy gradient (corporate)", lambda: gradient_flow([(0, 150, 140), (20, 60, 120), (80, 200, 120), (5, 20, 40)], 16)),
    "gradient-purple-blue-vertical": ("abstract", "background", "purple/blue gradient 9:16", lambda: gradient_flow([(90, 30, 160), (30, 80, 220), (220, 60, 150), (20, 20, 60)], 17, w=270, h=480, out=V)),
    "tech-grid": ("abstract", "background", "neon perspective grid moving forward (retro/tech/gaming)", tech_grid),
    "particle-network": ("abstract", "background", "connected dots network (tech, IT, business)", particle_network),
    "starfield": ("abstract", "background", "twinkling stars drifting (space, night)", starfield),
    "sparks-fountain-vertical": ("fire", "screen", "spark fountain 9:16", lambda: particles("sparks", 18, w=1080, h=1920)),
    "snow-falling-vertical": ("weather", "screen", "snow 9:16", lambda: particles("snow", 19, w=1080, h=1920)),
    "rain-streaks-vertical": ("weather", "screen", "rain streaks 9:16", lambda: particles("rain", 20, w=1080, h=1920)),
    "light-leak-pink-vertical": ("overlay", "screen", "pink light leak 9:16", lambda: light_leak([(255, 70, 140), (255, 140, 90), (200, 60, 255)], 21, w=540, h=960, out=V)),
    "bokeh-blue-pink-vertical": ("overlay", "screen", "blue and pink bokeh 9:16", lambda: bokeh([(80, 140, 255), (255, 90, 170), (170, 120, 255)], 22, w=540, h=960, out=V)),
    "gradient-warm-vertical": ("abstract", "background", "orange/red/gold gradient 9:16", lambda: gradient_flow([(255, 120, 40), (200, 30, 60), (255, 200, 80), (60, 10, 20)], 23, w=270, h=480, out=V)),
    "gradient-teal-green-vertical": ("abstract", "background", "teal/green/navy gradient 9:16", lambda: gradient_flow([(0, 150, 140), (20, 60, 120), (80, 200, 120), (5, 20, 40)], 24, w=270, h=480, out=V)),
    "tech-grid-vertical": ("abstract", "background", "neon perspective grid 9:16", lambda: tech_grid(w=1080, h=1920)),
    "particle-network-vertical": ("abstract", "background", "connected dots network 9:16", lambda: particle_network(25, w=1080, h=1920, N=60)),
    "starfield-vertical": ("abstract", "background", "twinkling stars 9:16", lambda: starfield(26, w=1080, h=1920)),
    "confetti-greenscreen-vertical": ("celebration", "chroma key #00FF00", "confetti on green screen 9:16", lambda: confetti_green(27, w=1080, h=1920, N=160)),
    "smoke-fog-vertical": ("fire", "screen", "drifting fog/smoke 9:16", lambda: smoke_fog(28, w=270, h=480, out=V)),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out", nargs="?")
    ap.add_argument("--only", default="")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    if a.list or not a.out:
        for k, (c, b, d, _) in CLIPS.items():
            print(f"{k:32s} {c:12s} {b:20s} {d}")
        return
    os.makedirs(a.out, exist_ok=True)
    only = set(filter(None, a.only.split(",")))
    for k, (_, _, _, fn) in CLIPS.items():
        if only and k not in only:
            continue
        w, h, n, f, out = fn()
        run(os.path.join(a.out, k + ".mp4"), w, h, n, f, out=out)
        print("wrote", k, flush=True)


if __name__ == "__main__":
    sys.exit(main())
