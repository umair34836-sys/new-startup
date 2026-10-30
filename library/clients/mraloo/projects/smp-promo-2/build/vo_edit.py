# ALOO SMP Promo 2 VO: client's own "aloosmp promo 2.mp3" (70.2 s). Guide: dead air + repeated words cut, natural pauses
# kept (no speed-up). Retake: "yahan tum survival kar sakte ho" (32.96-35.4, Whisper medium hi/en) said again at 37.24
# with the rest of the list -> keep the second take. Pauses > 0.40 s shortened to 0.28 s, beats kept before "aur wahin se
# shuru hua ALOO SMP" (0.45 s) and "to bhai" CTA (0.35 s).
import json, subprocess
import numpy as np
SR = 48000
a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", "in/promo2.mp3", "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"],
                                 capture_output=True).stdout, np.int16).astype(np.float32) / 32768
W = json.load(open("words_raw.json"))
F = 480
db = 20 * np.log10(np.array([np.sqrt((a[i:i + F] ** 2).mean()) for i in range(0, len(a) - F, F)]) + 1e-9)
def quiet(t, r=0.15):
    i0, i1 = int((t - r) * 100), int((t + r) * 100)
    return (i0 + int(np.argmin(db[i0:i1]))) / 100
REMOVE = [(quiet(32.85), quiet(37.12))]
thr = np.percentile(db[db > -60], 95) - 35
sil = db < thr
KEEP = {81: 0.45, 152: 0.35}
i = 0
while i < len(sil):
    if sil[i]:
        j = i
        while j < len(sil) and sil[j]: j += 1
        s, e = i / 100, j / 100
        if e - s > 0.40 and not any(rs - 0.05 <= s and e <= re + 0.05 for rs, re in REMOVE):
            nxt = [k for k, w in enumerate(W) if w[0] >= e - 0.1]
            keep = KEEP.get(nxt[0], 0.28) if nxt else 0.28
            if e - s > keep + 0.02:
                m = (s + e) / 2; REMOVE.append((round(m - (e - s - keep) / 2, 2), round(m + (e - s - keep) / 2, 2)))
        i = j
    else:
        i += 1
REMOVE.sort(); M = []
for s, e in REMOVE:
    if M and s <= M[-1][1]: M[-1] = (M[-1][0], max(M[-1][1], e))
    else: M.append((s, e))
REMOVE = M
Fd = int(0.010 * SR); out, prev = [], 0
for s, e in REMOVE + [(len(a) / SR, None)]:
    seg = a[prev:int(s * SR)].copy(); seg[:Fd] *= np.linspace(0, 1, Fd); seg[-Fd:] *= np.linspace(1, 0, Fd); out.append(seg)
    if e is None: break
    prev = int(e * SR)
o = np.concatenate(out)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af",
                "highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=9", "-ar", str(SR), "-c:a", "pcm_s16le", "vo.wav"], input=o.tobytes(), check=True)
def mp(t):
    d = 0.0
    for s, e in REMOVE:
        if t >= e: d += e - s
        elif t > s: d += t - s
    return round(t - d, 3)
W2 = [[mp(s), mp(e), w] for s, e, w in W]
json.dump(W2, open("words.json", "w"), ensure_ascii=False)
json.dump(dict(remove=REMOVE), open("vo_cuts.json", "w"))
print("cuts", len(REMOVE), "removed", round(sum(e - s for s, e in REMOVE), 2), "->", round(len(o) / SR, 2), "s")
