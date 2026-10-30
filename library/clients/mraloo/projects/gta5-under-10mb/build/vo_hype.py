# VO v3 (owner 2026-10-28: "voice bhot slow hai, customize karo, hype aur hook"): from the retake-free cut (vo_cut.wav,
# 355.6 s, before tempo) drop the two retakes found later (cut2.py), shorten every pause > 0.28 s to 0.20 s (dramatic
# beats kept: before "lekin bhai", after each spoken heading, after the punchline), then rubberband tempo, then a voice
# chain for punch (high-pass 80 Hz, +2.5 dB presence at 3 kHz, compressor, loudnorm -16).
import json, subprocess, sys
import numpy as np
TEMPO = float(sys.argv[1]) if len(sys.argv) > 1 else 1.22
SR = 48000
a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", "vo_cut.wav", "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"],
                                 capture_output=True).stdout, np.int16).astype(np.float32) / 32768
W = json.load(open("words_final_pre2.json"))           # 1.15x clock, before cut2
W = [[s * 1.15, e * 1.15, w] for s, e, w in W]         # -> vo_cut clock
# later takes of the two repeated lines (tr_parts.py, 1.15x clock) -> vo_cut clock
for i, (s, e) in zip(range(495, 501), [(193.92, 194.16), (194.18, 194.42), (194.44, 194.49), (194.50, 194.88), (194.90, 195.28), (195.30, 195.6)]):
    W[i][0], W[i][1] = s * 1.15, e * 1.15
for i, (s, e) in zip(range(651, 656), [(256.82, 257.28), (257.30, 257.76), (257.78, 258.12), (258.14, 258.32), (258.34, 258.46)]):
    W[i][0], W[i][1] = s * 1.15, e * 1.15
F = 480                                                 # 10 ms frames
env = np.array([np.sqrt((a[i:i + F] ** 2).mean()) for i in range(0, len(a) - F, F)])
db = 20 * np.log10(env + 1e-9)


def quiet(t, r=0.12):
    i0, i1 = int((t - r) * 100), int((t + r) * 100)
    return (i0 + int(np.argmin(db[i0:i1]))) / 100


REMOVE = [(quiet(191.435 * 1.15), quiet(193.865 * 1.15)), (quiet(252.565 * 1.15, 0.08), quiet(256.675 * 1.15))]
# pauses: runs of frames 35 dB under the speech level (p95), longer than 0.28 s
thr = np.percentile(db[db > -60], 95) - 35
sil = db < thr
KEEP_GAP = {70: 0.45, 77: 0.30, 265: 0.40, 422: 0.40, 569: 0.40, 775: 0.70}   # gap BEFORE these word indices (s)
runs, i = [], 0
while i < len(sil):
    if sil[i]:
        j = i
        while j < len(sil) and sil[j]:
            j += 1
        if (j - i) / 100 > 0.28:
            runs.append((i / 100, j / 100))
        i = j
    else:
        i += 1
for s, e in runs:
    if any(rs - 0.05 <= s and e <= re_ + 0.05 for rs, re_ in REMOVE):
        continue
    nxt = [k for k, w in enumerate(W) if w[0] >= e - 0.08]
    keep = KEEP_GAP.get(nxt[0], 0.20) if nxt else 0.20
    if e - s > keep + 0.02:
        mid = (s + e) / 2
        REMOVE.append((round(mid - (e - s - keep) / 2, 2), round(mid + (e - s - keep) / 2, 2)))
REMOVE = sorted(REMOVE)
M = []
for s_, e_ in REMOVE:
    if M and s_ <= M[-1][1]:
        M[-1] = (M[-1][0], max(M[-1][1], e_))
    else:
        M.append((s_, e_))
REMOVE = M
Fd = int(0.010 * SR)
out, prev = [], 0
for s, e in REMOVE:
    seg = a[prev:int(s * SR)].copy()
    if len(seg) > 2 * Fd:
        seg[:Fd] *= np.linspace(0, 1, Fd); seg[-Fd:] *= np.linspace(1, 0, Fd)
    out.append(seg); prev = int(e * SR)
seg = a[prev:].copy(); seg[:Fd] *= np.linspace(0, 1, Fd); out.append(seg)
o = np.concatenate(out)


def mp(t):
    d = 0.0
    for s, e in REMOVE:
        if t >= e:
            d += e - s
        elif t > s:
            d += t - s
    return (t - d) / TEMPO


subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-",
                "-af", f"rubberband=tempo={TEMPO}:pitchq=quality,highpass=f=80,equalizer=f=3000:t=q:w=1.2:g=2.5,"
                       "acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=2,loudnorm=I=-16:TP=-1.5:LRA=9",
                "-ar", str(SR), "-c:a", "pcm_s16le", "vo_hype.wav"], input=o.tobytes(), check=True)
W3 = [[round(mp(s), 3), round(mp(e), 3), w] for s, e, w in W]
json.dump(W3, open("words_hype.json", "w"), ensure_ascii=False)
d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", "vo_hype.wav"], capture_output=True, text=True).stdout)
print(f"tempo {TEMPO}: removed {sum(e - s for s, e in REMOVE):.1f} s in {len(REMOVE)} cuts -> {d:.1f} s, {len(W3) / d * 60:.0f} wpm, last word {W3[-1]}")
