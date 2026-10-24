# Used for library/research/cpu-speed.md (2026-10-24): fill methods for the bg_blur.py hole, timing + diff vs Telea.
# usage: perc-venv/bin/python bench_fill.py VIDEO_1080x1920
import sys, time, subprocess, numpy as np, cv2
sys.path.insert(0, "/home/user/new-startup/library/tools")
from fast_matte import RVM
def disc(r):
    k = np.zeros((2*r+1, 2*r+1), np.float32); cv2.circle(k, (r, r), r, 1, -1, cv2.LINE_AA); return k/k.sum()
KER = disc(17)
def finish(filled, w, h):
    lin = (filled.astype(np.float32)/255)**2.2
    bl = cv2.filter2D(cv2.filter2D(lin, -1, KER, borderType=cv2.BORDER_REFLECT), -1, KER, borderType=cv2.BORDER_REFLECT)
    return cv2.resize(((bl**(1/2.2))*255*0.86).astype(np.float32), (w, h), interpolation=cv2.INTER_CUBIC)
def telea(small, hole):
    return cv2.inpaint(small, hole, 9, cv2.INPAINT_TELEA)
def telea_quarter(small, hole):
    h, w = hole.shape
    s2 = cv2.resize(small, (w//2, h//2), interpolation=cv2.INTER_AREA); h2 = (cv2.resize(hole, (w//2, h//2)) > 0).astype(np.uint8)*255
    f2 = cv2.inpaint(s2, h2, 5, cv2.INPAINT_TELEA)
    up = cv2.resize(f2, (w, h), interpolation=cv2.INTER_LINEAR)
    out = small.copy(); m = hole > 0; out[m] = up[m]; return out
def pushpull(small, hole):
    # normalized-convolution pyramid: average known pixels down, fill holes from coarser levels on the way up
    known = (hole == 0).astype(np.float32); img = small.astype(np.float32) * known[..., None]
    pyr = [(img, known)]
    while min(pyr[-1][1].shape) > 8:
        i, k = pyr[-1]; pyr.append((cv2.pyrDown(i), cv2.pyrDown(k)))
    i, k = pyr[-1]; cur = i / np.maximum(k, 1e-6)[..., None]
    for i, k in reversed(pyr[:-1]):
        up = cv2.resize(cur, (k.shape[1], k.shape[0]), interpolation=cv2.INTER_LINEAR)
        val = i / np.maximum(k, 1e-6)[..., None]
        wk = np.clip(k, 0, 1)[..., None]
        cur = val * wk + up * (1 - wk)
    out = small.copy(); m = hole > 0; out[m] = np.clip(cur[m], 0, 255).astype(np.uint8); return out
v = sys.argv[1]; w, h = 1080, 1920
dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", v, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
M = RVM(); T = {"telea": [], "telea_quarter": [], "pushpull": []}; D = {"telea_quarter": [], "pushpull": []}; DH = {"telea_quarter": [], "pushpull": []}
n = 0
while n < 20:
    b = dec.stdout.read(w*h*3)
    if len(b) < w*h*3: break
    rgb = np.frombuffer(b, np.uint8).reshape(h, w, 3); hard = (M(rgb) > 0.5).astype(np.float32); n += 1
    if n % 4: continue
    sw, sh = w//2, h//2
    small = cv2.resize(rgb, (sw, sh), interpolation=cv2.INTER_AREA)
    hole = cv2.dilate(((cv2.resize(hard, (sw, sh)) > 0.3).astype(np.uint8))*255, np.ones((21, 21), np.uint8))
    res = {}
    for name, f in (("telea", telea), ("telea_quarter", telea_quarter), ("pushpull", pushpull)):
        t0 = time.perf_counter(); fl = f(small, hole); T[name].append(time.perf_counter()-t0); res[name] = finish(fl, w, h)
    bigh = cv2.resize(hole, (w, h)) > 0
    for name in D:
        d = np.abs(res[name] - res["telea"]); D[name].append(d.mean()); DH[name].append(d[bigh].mean())
    if n == 8:
        cv2.imwrite("fill_cmp.jpg", cv2.cvtColor(np.hstack([res[k] for k in ("telea", "telea_quarter", "pushpull")]).clip(0,255).astype(np.uint8)[::3, ::3], cv2.COLOR_RGB2BGR))
for k in T: print(k, "fill s/frame", round(np.mean(T[k]), 3), *( ["final-background diff vs telea (0-255): all", round(np.mean(D[k]), 2), "inside hole", round(np.mean(DH[k]), 2)] if k in D else []))
