# client (2026-10-28): "2:05 mein word repeat hua hai" -> the spoken heading was said twice: "why 10MB GTA5 doesn't...
# doesn't" (123.02-125.02) then the clean "why 10 MB GTA5 doesn't make sense" (Whisper medium en, measured here). Keep the second.
import json, numpy as np, subprocess
SR = 48000
CUTS = [(123.02, 125.02)]
a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", "vo_hype2.wav", "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"],
                                 capture_output=True).stdout, np.int16).astype(np.float32) / 32768
F = int(0.010 * SR); out, prev = [], 0
for s, e in CUTS + [(len(a) / SR, None)]:
    seg = a[prev:int(s * SR)].copy(); seg[:F] *= np.linspace(0, 1, F); seg[-F:] *= np.linspace(1, 0, F); out.append(seg)
    if e is None: break
    prev = int(e * SR)
o = np.concatenate(out)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-c:a", "pcm_s16le", "vo_hype3.wav"], input=o.tobytes(), check=True)
def mp(t):
    d = 0.0
    for s, e in CUTS:
        if t >= e: d += e - s
        elif t > s: d += t - s
    return round(t - d, 3)
W = json.load(open("words_hype2.json"))
for i, (s, e) in zip(range(417, 420), [(125.36, 125.78), (125.78, 126.5), (126.5, 126.9)]):
    W[i][0], W[i][1] = s, e
json.dump([[mp(s), mp(e), w] for s, e, w in W], open("words_hype3.json", "w"), ensure_ascii=False)
print(len(o) / SR)
