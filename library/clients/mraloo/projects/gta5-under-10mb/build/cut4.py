# stumbles found in the v3 VO (Whisper medium hi + en per region, 2026-10-28): keep the corrected take of each
# A "na da, na 100 GB," false start before "na 100 GB storage ki tension"; B first of "bina, bina verify";
# C first "to thoda suspicious"; D "kyunki kisi... " restart before "kyunki YouTuber ne bol diya"
import json, numpy as np, subprocess
SR = 48000
CUTS = [(7.60, 9.45), (121.30, 121.78), (187.45, 188.60), (194.12, 195.08)]
a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", "vo_hype.wav", "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"],
                                 capture_output=True).stdout, np.int16).astype(np.float32) / 32768
F = int(0.010 * SR); out, prev = [], 0
for s, e in CUTS + [(len(a) / SR, None)]:
    seg = a[prev:int(s * SR)].copy(); seg[:F] *= np.linspace(0, 1, F); seg[-F:] *= np.linspace(1, 0, F); out.append(seg)
    if e is None: break
    prev = int(e * SR)
o = np.concatenate(out)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-c:a", "pcm_s16le", "vo_hype2.wav"], input=o.tobytes(), check=True)
def mp(t):
    d = 0.0
    for s, e in CUTS:
        if t >= e: d += e - s
        elif t > s: d += t - s
    return round(t - d, 3)
W = json.load(open("words_hype.json"))
W[407][0] = 121.80; W[623][0] = 189.30; W[622][0] = 188.70; W[622][1] = 188.95; W[639][0] = 195.15; W[639][1] = 195.50; W[640][0] = 195.52
json.dump([[mp(s), mp(e), w] for s, e, w in W], open("words_hype2.json", "w"), ensure_ascii=False)
print(len(o) / SR)
