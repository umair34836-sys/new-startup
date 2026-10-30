# Music: "High Technologic Beat Explosion" (Loyalty Freak Music, CC0, library/music/cc0; listen.py: 140 BPM, conf 1.73,
# drop/chorus from 42.42 s). One continuous take placed so the drop lands on the spoken "ALOO SMP" (guide: beat hit on the
# reveal). Problem part (0 -> "phir maine socha") muffled (low-pass 900 Hz, -4 dB): guide "music lifts gently" on the
# beat shift, then opens fully into the drop. Comedic silence for 0.8 s after "kisi ko jaante hi nahi ho" (guide 3-8 s).
import json, subprocess, numpy as np
T = json.load(open("timing.json")); W = json.load(open("words.json"))
SR = 48000; TOTAL = T["total"]; R0 = T["reveal"]; LIFT = T["lift"]
SRC = "/home/user/new-startup/library/music/cc0/upbeat-electronic--loyalty-freak-music--high-technologic-beat-explosion.mp3"
s0 = 42.42 - R0
def load(af):
    x = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{s0:.3f}", "-t", f"{TOTAL:.3f}", "-i", SRC, "-af", af, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                       capture_output=True).stdout
    return np.frombuffer(x, np.float32).reshape(-1, 2).copy()
clear = load("loudnorm=I=-14:TP=-1.5:LRA=11"); muff = load("loudnorm=I=-14:TP=-1.5:LRA=11,lowpass=f=900,volume=-4dB")
n = min(len(clear), len(muff)); t = np.arange(n) / SR
mixw = np.clip((t - LIFT) / max(0.5, R0 - 0.4 - LIFT), 0, 1)[:, None]      # muffled -> clear across the beat shift
bed = muff[:n] * (1 - mixw) + clear[:n] * mixw
s_sil, e_sil = W[35][1] + 0.05, W[35][1] + 0.85                              # comedic silence (trombone plays here)
g = np.ones(n)
for a, b, d in [(s_sil, e_sil, 0.08)]:
    g[(t >= a) & (t < b)] = 0
    ramp = (t >= b) & (t < b + 0.3); g[ramp] = (t[ramp] - b) / 0.3
    ramp = (t >= a - d) & (t < a); g[ramp] = (a - t[ramp]) / d
fo = t > TOTAL - 2.0; g[fo] *= (TOTAL - t[fo]) / 2.0                           # guide: "music resolves"
bed *= g[:, None]
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", "pcm_s16le", "assets/bed_raw.wav"], input=bed.astype(np.float32).tobytes(), check=True)
print("bed", round(n / SR, 2), "source offset", round(s0, 2))
