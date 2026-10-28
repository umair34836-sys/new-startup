# second pass (2026-10-28): the final-VO Whisper check found two retakes left in: "haan ek baat samajhna zaroor" twice
# (191.7 / 193.9) and "bhai YouTube thumbnail" twice (252.4 / 256.6, with a lone "bhai" at 254.8). Keep the later take.
import json, numpy as np, subprocess, shutil, os
SR = 48000
if not os.path.exists("vo_final_pre2.wav"):
    shutil.copy("vo_final.wav", "vo_final_pre2.wav"); shutil.copy("words_final.json", "words_final_pre2.json")
a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", "vo_final_pre2.wav", "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"],
                                 capture_output=True).stdout, np.int16).astype(np.float32) / 32768
def quiet(t, r=0.12):
    best, bt = 9, t
    for c in np.arange(t - r, t + r, 0.01):
        e = np.sqrt((a[int(c * SR):int((c + 0.01) * SR)] ** 2).mean())
        if e < best: best, bt = e, c
    return round(bt + 0.005, 3)
CUTS = [(quiet(191.55), quiet(193.85)), (quiet(252.6, 0.08), quiet(256.55))]
print("cuts", CUTS)
W = json.load(open("words_final_pre2.json"))
# later takes' word times from the part re-transcription (tr_parts.py, Whisper medium hi)
for i, t in zip(range(495, 501), [193.92, 194.18, 194.44, 194.50, 194.90, 195.30]):
    W[i][0] = t; W[i][1] = round(W[i + 1][0] if i < 500 else 195.6, 3) if i == 500 else t + 0.2
for i, (s, e) in zip(range(495, 500), [(193.92, 194.16), (194.18, 194.42), (194.44, 194.49), (194.50, 194.88), (194.90, 195.28)]):
    W[i][0], W[i][1] = s, e
W[500][0], W[500][1] = 195.30, 195.6
for i, (s, e) in zip(range(651, 656), [(256.82, 257.28), (257.30, 257.76), (257.78, 258.12), (258.14, 258.32), (258.34, 258.46)]):
    W[i][0], W[i][1] = s, e
F = int(0.015 * SR)
keep, prev = [], 0
for s, e in CUTS:
    keep.append((prev, int(s * SR))); prev = int(e * SR)
keep.append((prev, len(a)))
out = []
for x0, x1 in keep:
    seg = a[x0:x1].copy(); seg[:F] *= np.linspace(0, 1, F); seg[-F:] *= np.linspace(1, 0, F); out.append(seg)
o = np.concatenate(out)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-c:a", "pcm_s16le", "vo_final.wav"], input=o.tobytes(), check=True)
def sh(t):
    d = 0
    for s, e in CUTS:
        if t >= e - 0.001: d += e - s
    return round(t - d, 3)
W2 = [[sh(s), sh(e), w] for s, e, w in W]
json.dump(W2, open("words_final.json", "w"), ensure_ascii=False)
json.dump(dict(cuts=CUTS), open("cut2_map.json", "w"))
print("new length", len(o) / SR, "last word", W2[-1])
