#!/usr/bin/env python3
"""vfx_kit.py - procedural VFX layers rendered on black (composite with screen/add blend), CPU only, no AI.
Built 2026-11-25 (owner: "full vfx ka use ker k ... apni skill dekao"). numpy + OpenCV (perc-venv).
Layers (all driven by one timeline in a JSON spec):
  smoke   : animated fractal (fBm) noise smoke, tinted, low alpha
  converge: ember particles flying from the frame edges into a point on swirling paths (gathering energy)
  burst   : spark explosion at a point: drag + gravity, streaks along velocity, cooling colour (white->yellow->red)
  shock   : expanding shockwave ring(s) with a soft glow
  rays    : volumetric god rays from a point (angular noise, slow rotation, radial falloff)
  embers  : slow rising embers with flicker
  flash   : full-frame flash at given times
Bloom = multi-scale Gaussian glow of the whole layer. Rendered at half size, upscaled (glows hide it).
Usage: perc-venv/bin/python vfx_kit.py spec.json out.mp4
spec: {"w":1080,"h":1920,"fps":30,"dur":18,"seed":7,"center":[540,880],"color":[255,40,60], "layers":[{"type":..., ...}]}
"""
import json, subprocess, sys
import numpy as np, cv2

def fbm_bank(rng, h, w, octaves=5, frames=4):
    """a few random low-res grids per octave; animated by drifting + crossfading them"""
    return [[rng.random((max(2, h // (2 ** (6 - o))), max(2, w // (2 ** (6 - o))))).astype(np.float32) for _ in range(frames)] for o in range(octaves)]

def fbm(bank, h, w, t, drift=(0.0, -40.0)):
    acc = np.zeros((h, w), np.float32); amp = 1.0; tot = 0
    for o, grids in enumerate(bank):
        k = (t * 0.25 * (1 + o * 0.5)) % len(grids); i = int(k); f = k - i
        g = grids[i] * (1 - f) + grids[(i + 1) % len(grids)] * f
        big = cv2.resize(g, (w + 64, h + 64), interpolation=cv2.INTER_CUBIC)
        dx = int(drift[0] * t * (1 + o * 0.3)) % 64; dy = int(-drift[1] * t * (1 + o * 0.3)) % 64
        acc += big[dy:dy + h, dx:dx + w] * amp; tot += amp; amp *= 0.55
    return acc / tot

def splat(img, xs, ys, cols, sizes):
    """draw soft dots (additive)"""
    H, W = img.shape[:2]
    for x, y, c, s in zip(xs, ys, cols, sizes):
        if -10 < x < W + 10 and -10 < y < H + 10:
            cv2.circle(img, (int(x), int(y)), max(1, int(s)), tuple(float(v) for v in c), -1, lineType=cv2.LINE_AA)

def streaks(img, x0, y0, x1, y1, cols, th):
    H, W = img.shape[:2]
    for a, b, c, d, col, t in zip(x0, y0, x1, y1, cols, th):
        if -50 < c < W + 50 and -50 < d < H + 50:
            cv2.line(img, (int(a), int(b)), (int(c), int(d)), tuple(float(v) for v in col), max(1, int(t)), lineType=cv2.LINE_AA)

def heat(temp):
    """temp 1 -> white-yellow, 0 -> deep red (BGR float 0..1)"""
    t = np.clip(temp, 0, 1)[:, None]
    hot = np.array([0.85, 0.95, 1.0]); mid = np.array([0.15, 0.55, 1.0]); cold = np.array([0.1, 0.08, 0.75])
    return np.where(t > 0.5, mid + (hot - mid) * (t - 0.5) * 2, cold + (mid - cold) * t * 2)

def main():
    S = json.load(open(sys.argv[1])); out = sys.argv[2]
    W, H, FPS, DUR = S["w"], S["h"], S["fps"], S["dur"]; w, h = W // 2, H // 2
    rng = np.random.default_rng(S.get("seed", 7)); cx, cy = S["center"][0] / 2, S["center"][1] / 2
    col = np.array(S.get("color", [255, 40, 60])[::-1], np.float32) / 255  # BGR
    L = S["layers"]; prep = {}
    for i, ly in enumerate(L):
        ty = ly["type"]
        if ty == "smoke": prep[i] = fbm_bank(rng, h, w)
        if ty == "converge":
            n = ly.get("n", 700); side = rng.integers(0, 4, n); u = rng.random(n)
            sx = np.where(side == 0, u * w, np.where(side == 1, w + 20, np.where(side == 2, u * w, -20)))
            sy = np.where(side == 0, -20, np.where(side == 1, u * h, np.where(side == 2, h + 20, -20 + 0 * u)))
            sy = np.where(side == 3, u * h, sy)
            prep[i] = (sx, sy, rng.random(n) * 0.35, rng.uniform(-2.2, 2.2, n), rng.uniform(0.6, 1.8, n))
        if ty == "burst":
            n = ly.get("n", 1400); ang = rng.random(n) * 2 * np.pi; sp = rng.gamma(2.0, 1.0, n) * ly.get("speed", 260)
            prep[i] = (np.cos(ang) * sp, np.sin(ang) * sp, rng.uniform(0.6, 1.0, n) * ly.get("life", 2.4), rng.uniform(0.6, 1.6, n))
        if ty == "embers":
            n = ly.get("n", 160)
            prep[i] = (rng.random(n) * w, rng.random(n) * h, rng.uniform(15, 45, n), rng.random(n) * 6.28, rng.uniform(0.6, 1.6, n))
        if ty == "rays": prep[i] = rng.random(180).astype(np.float32)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32); dx, dy = xx - cx, yy - cy
    rad = np.sqrt(dx * dx + dy * dy); ang = (np.arctan2(dy, dx) + np.pi) / (2 * np.pi)
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for fi in range(int(DUR * FPS)):
        t = fi / FPS; img = np.zeros((h, w, 3), np.float32)
        for i, ly in enumerate(L):
            a, z = ly.get("start", 0), ly.get("end", DUR)
            if not (a <= t < z): continue
            lt = t - a; ty = ly["type"]; k = ly.get("gain", 1.0)
            if ty == "smoke":
                n = fbm(prep[i], h, w, t); m = np.clip((n - 0.45) * 2.2, 0, 1) ** 1.6
                fade = min(1, lt / 1.0, (z - t) / 1.0); img += m[..., None] * col * 0.35 * k * fade
            elif ty == "converge":
                sx, sy, delay, curl, sz = prep[i]; D = z - a
                p = np.clip((lt / D - delay) / (1 - delay), 0, 1); e = p * p * (3 - 2 * p)
                th = curl * (1 - e); ox, oy = sx - cx, sy - cy
                x = cx + (ox * np.cos(th) - oy * np.sin(th)) * (1 - e); y = cy + (ox * np.sin(th) + oy * np.cos(th)) * (1 - e)
                vis = (p > 0) & (p < 1); c = heat(0.3 + 0.7 * e)[vis] * k
                splat(img, x[vis], y[vis], c, sz[vis] * (0.6 + e[vis]))
                glow = np.exp(-rad / (30 + 60 * (lt / D))) * (lt / D) ** 2 * 1.4 * k; img += glow[..., None] * np.array([0.7, 0.8, 1.0])
            elif ty == "burst":
                vx, vy, life, sz = prep[i]; drag = 2.2; g = 60.0
                d = (1 - np.exp(-drag * lt)) / drag; x = cx + vx * d; y = cy + vy * d + 0.5 * g * lt * lt
                vxt, vyt = vx * np.exp(-drag * lt), vy * np.exp(-drag * lt) + g * lt
                alive = lt < life; temp = 1 - lt / life
                c = heat(temp)[alive] * np.clip(temp[alive] * 1.5, 0, 1)[:, None] * k
                streaks(img, x[alive], y[alive], (x - vxt * 0.035)[alive], (y - vyt * 0.035)[alive], c, sz[alive])
            elif ty == "shock":
                for j, dl in enumerate(ly.get("delays", [0, 0.12])):
                    st = lt - dl
                    if 0 <= st < 0.9:
                        r = st * ly.get("speed", 900) / 2 + 10; wdt = 6 + st * 30; fade = (1 - st / 0.9) ** 1.5
                        ring = np.exp(-((rad - r) / wdt) ** 2) * fade * (1.0 if j == 0 else 0.5) * k
                        img += ring[..., None] * np.array([0.9, 0.9, 1.0])
            elif ty == "rays":
                seeds = prep[i]; n = len(seeds); pos = (ang * n + lt * ly.get("spin", 1.5)) % n; i0 = pos.astype(int); f = pos - i0
                pat = seeds[i0] * (1 - f) + seeds[(i0 + 1) % n] * f; pat = np.clip((pat - 0.45) * 2.5, 0, 1) ** 2
                fall = np.exp(-rad / ly.get("reach", 420)) * np.clip(rad / 40, 0, 1)
                fade = min(1, lt / 0.6, (z - t) / 0.8); img += (pat * fall)[..., None] * col * 1.1 * k * fade
            elif ty == "embers":
                x0, y0, sp, ph, sz = prep[i]
                y = (y0 - sp * lt) % h; x = x0 + np.sin(ph + lt * 1.3) * 12
                fl = 0.55 + 0.45 * np.sin(ph * 3 + lt * 7); fade = min(1, lt / 1.0)
                splat(img, x, y, heat(0.35 + 0.3 * fl) * (fl * fade * k)[:, None], sz)
            elif ty == "flash":
                for ft in ly["times"]:
                    d = t - ft
                    if 0 <= d < 0.5: img += (1 - d / 0.5) ** 2 * 1.2 * k
        bloom = cv2.GaussianBlur(img, (0, 0), 6) * 0.9 + cv2.GaussianBlur(img, (0, 0), 22) * 0.7
        o = img + bloom; o = 1 - np.exp(-o * 1.4)  # soft tonemap, never clips hard
        o = cv2.resize(o, (W, H), interpolation=cv2.INTER_LINEAR)
        ff.stdin.write((np.clip(o, 0, 1) * 255).astype(np.uint8).tobytes())
    ff.stdin.close(); ff.wait(); print("wrote", out)

if __name__ == "__main__":
    main()
