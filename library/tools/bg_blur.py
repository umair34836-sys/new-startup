# Usage: /home/user/tools/venv/bin/python library/tools/bg_blur.py IN.mp4|IN.jpg OUT [--radius 34]  (1080x1920 video, ~4 s/frame on CPU; 2 runs in parallel OK)
# Professional portrait-mode background for phone footage:
#  - person mask (rembg u2net_human_seg), temporally smoothed (no flicker), soft but tight edges
#  - desk (subject plane) kept sharp; found from the cyan desk mats with a RANSAC line
#  - background: person area filled from surroundings first (no halo), lens (disc/bokeh) blur, blue/cyan objects
#    desaturated and warmed into the wall colour, slightly darker so the subject pops
#   python bgblur2.py IN.(mp4|jpg|png) OUT [--radius 34]
import argparse, os, subprocess, sys
import cv2
import numpy as np
from PIL import Image
from rembg import new_session, remove

ap = argparse.ArgumentParser()
ap.add_argument("inp"); ap.add_argument("out")
ap.add_argument("--radius", type=int, default=34)
a = ap.parse_args()
sess = new_session("u2net_human_seg")


def desk_line(rgb):
    h, w, _ = rgb.shape
    f = rgb.astype(np.float32)
    r, g, b = f[..., 0], f[..., 1], f[..., 2]
    cyan = (b > 120) & (b > r + 50) & (g > r + 20)
    y0 = int(h * 0.45)
    top = np.full(w, h, np.int32); gap = np.zeros(w, np.int32); alive = np.ones(w, bool)
    for y in range(h - 1, y0, -1):  # cyan stretch connected to the bottom of the frame
        c = cyan[y] & alive
        top[c] = y
        gap = np.where(cyan[y], 0, gap + 1)
        alive &= gap <= 90  # mats have white seams and print between them
    ok = top < h
    if ok.sum() < w * 0.3:
        return None
    xs, ys = np.nonzero(ok)[0].astype(np.float32), top[ok].astype(np.float32)
    rng = np.random.default_rng(0); best = None
    for _ in range(300):
        i, j = rng.choice(len(xs), 2, replace=False)
        if abs(xs[i] - xs[j]) < w * 0.2:
            continue
        k = (ys[j] - ys[i]) / (xs[j] - xs[i]); c = ys[i] - k * xs[i]
        n = int((np.abs(ys - (k * xs + c)) < 12).sum())
        if best is None or n > best[0]:
            best = (n, k, c)
    _, k, c = best
    keep = np.abs(ys - (k * xs + c)) < 12
    return np.polyfit(xs[keep], ys[keep], 1)


def sharp_mask(rgb, person, line):
    h, w, _ = rgb.shape
    yy = np.arange(h, dtype=np.float32)[:, None]
    m = person.copy()
    if line is not None:
        L = (line[0] * np.arange(w) + line[1])[None, :]
        desk = np.clip((yy - L - 10) / 28.0, 0, 1)  # soft hand-over at the desk edge
        lum = rgb.mean(axis=2)
        band = ((yy > L - 120) & (yy < L + 30) & (lum < 60)).astype(np.uint8) * 255  # phone, keyboard
        band = cv2.dilate(cv2.erode(band, np.ones((5, 5), np.uint8)), np.ones((15, 15), np.uint8))
        band = cv2.GaussianBlur(band, (0, 0), 4).astype(np.float32) / 255
        m = np.maximum(m, np.maximum(desk, band))
    return m


def disc(r):
    k = np.zeros((2 * r + 1, 2 * r + 1), np.float32)
    cv2.circle(k, (r, r), r, 1, -1, cv2.LINE_AA)
    return k / k.sum()


KER = disc(max(3, a.radius // 2))


def background(rgb, hard):
    h, w, _ = rgb.shape
    sw, sh = w // 2, h // 2
    small = cv2.resize(rgb, (sw, sh), interpolation=cv2.INTER_AREA)
    hole = cv2.resize(hard, (sw, sh)) > 0.3
    hole = cv2.dilate(hole.astype(np.uint8) * 255, np.ones((21, 21), np.uint8))
    filled = cv2.inpaint(small, hole, 9, cv2.INPAINT_TELEA)  # remove the subject before blurring: no halo
    hsv = cv2.cvtColor(filled, cv2.COLOR_RGB2HSV).astype(np.float32)
    hue, sat = hsv[..., 0], hsv[..., 1]
    blue = np.clip(1 - np.abs(hue - 100) / 25, 0, 1) * np.clip((sat - 40) / 60, 0, 1)  # cyan/blue objects
    hsv[..., 1] = sat * (1 - 0.9 * blue)
    hsv[..., 0] = hue * (1 - blue) + 15 * blue  # pushed toward the warm wall hue
    filled = cv2.cvtColor(hsv.clip(0, 255).astype(np.uint8), cv2.COLOR_HSV2RGB)
    lin = (filled.astype(np.float32) / 255) ** 2.2  # blur in linear light: brighter, rounder bokeh
    bl = cv2.filter2D(lin, -1, KER, borderType=cv2.BORDER_REFLECT)
    bl = cv2.filter2D(bl, -1, KER, borderType=cv2.BORDER_REFLECT)
    out = (bl ** (1 / 2.2)) * 255 * 0.86  # a touch darker so the subject pops
    out = cv2.resize(out.astype(np.float32), (w, h), interpolation=cv2.INTER_CUBIC)
    return out


prev = None


def process(rgb):
    global prev
    h, w, _ = rgb.shape
    pm = remove(Image.fromarray(rgb).resize((w // 2, h // 2), Image.BILINEAR), session=sess, only_mask=True,
                post_process_mask=True)
    pm = cv2.resize(np.asarray(pm, np.float32) / 255, (w, h), interpolation=cv2.INTER_LINEAR)
    # the model misses dark shirt between arm and body: add very dark pixels right next to the silhouette
    cnts, _ = cv2.findContours((pm > 0.5).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    hull = np.zeros((h, w), np.uint8)
    if cnts:
        cv2.fillPoly(hull, [cv2.convexHull(max(cnts, key=cv2.contourArea))], 1)
    near = (cv2.dilate(hull, np.ones((15, 15), np.uint8)) > 0)
    dark = cv2.GaussianBlur(rgb, (0, 0), 2).mean(axis=2) < 55
    add = cv2.morphologyEx((near & dark).astype(np.uint8) * 255, cv2.MORPH_OPEN, np.ones((23, 23), np.uint8))  # drops thin dark lines (shelf edges)
    pm = np.maximum(pm, add.astype(np.float32) / 255)
    prev = pm if prev is None else 0.55 * pm + 0.45 * prev  # temporal smoothing: no edge flicker
    # fill holes inside the silhouette (dark shirt patches the model misses), keep soft outer edges
    hard = (prev > 0.45).astype(np.uint8) * 255
    hard = cv2.morphologyEx(hard, cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8))
    cnts, _ = cv2.findContours(hard, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    solid = np.zeros_like(hard)
    cv2.drawContours(solid, [c for c in cnts if cv2.contourArea(c) > 5000], -1, 255, -1)
    solid = cv2.GaussianBlur(cv2.erode(solid, np.ones((5, 5), np.uint8)), (0, 0), 3).astype(np.float32) / 255
    person = np.maximum(solid, cv2.GaussianBlur(prev, (0, 0), 2.5) * (solid > 0.01))
    m = sharp_mask(rgb, np.clip(person * 1.15, 0, 1), desk_line(rgb))
    bg = background(rgb, m)
    out = rgb.astype(np.float32) * m[..., None] + bg * (1 - m[..., None])
    return out.clip(0, 255).astype(np.uint8)


if a.inp.lower().endswith((".jpg", ".jpeg", ".png")):
    Image.fromarray(process(np.asarray(Image.open(a.inp).convert("RGB")))).save(a.out, quality=95)
    sys.exit()
W, H = 1080, 1920
dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", a.inp, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                        "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-pix_fmt", "yuv420p", a.out], stdin=subprocess.PIPE)
n = 0
while True:
    buf = dec.stdout.read(W * H * 3)
    if len(buf) < W * H * 3:
        break
    enc.stdin.write(process(np.frombuffer(buf, np.uint8).reshape(H, W, 3)).tobytes()); n += 1
enc.stdin.close(); enc.wait()
print(os.path.basename(a.out), n, "frames", flush=True)
