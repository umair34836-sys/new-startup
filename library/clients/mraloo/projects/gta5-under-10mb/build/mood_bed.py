# GTA 5 under 10 MB: music by scene mood (client guide "Background music": hook energetic, fake tutorial playful,
# permissions suspenseful, reality check light comedy, safety tips calm, final roast dramatic build-up; never one track).
# Tracks = owner's Drive YouTube Audio Library folders (YouTube use only), measured with listen.py (../../odrive/*.json).
# Each piece loudnorm -14, 0.8 s crossfades; the bed STOPS before "lekin bhai ek chhoti si problem" (guide: music band,
# skill #2035) and before the roast punchline; whole bed sidechain-ducked under the VO (skills #316/#317).
import json, subprocess
D = "../../odrive"
TOTAL = 304.3   # VO 302.65 s after the second retake pass (cut2.py) + outro tail
SEG = [  # (track, source in-point, timeline start, timeline end, why)
    ("euphoria", 0.0, 0.0, 27.5, "hook: energetic (upbeat folder)"),
    ("apocalyptic-echoes", 0.0, 33.3, 43.4, "after the scam reveal: low suspense under 'tension zaroor mil sakti hai'"),
    ("silly-snickerdoodle", 0.0, 43.4, 101.8, "scene 2 fake tutorial: playful (funny folder, 99 BPM)"),
    ("pouncin-bouncin", 0.0, 101.8, 160.4, "scene 3 permissions: comic suspense (funny folder, tense/driving)"),
    ("demented-90s", 7.5, 160.4, 212.97, "scene 4 reality check: light comedy (funny folder, bright/upbeat)"),
    ("on-the-flip", 21.4, 212.97, 269.96, "scene 5 safety tips: calm (lofi folder, calm/warm)"),
    ("challenge-accepted", 0.0, 269.96, 287.26, "scene 6 roast: dramatic build-up (suspense folder), stops before the punchline"),
    ("euphoria", 60.0, 290.06, TOTAL, "outro: back to the opening energy"),
]
X = 0.8
parts = []
for i, (n, src, t0, t1, _) in enumerate(SEG):
    joined_in = i > 0 and abs(SEG[i - 1][3] - t0) < 0.01
    joined_out = i + 1 < len(SEG) and abs(SEG[i + 1][2] - t1) < 0.01
    a = max(0.0, t0 - (X / 2 if joined_in else 0)); b = min(TOTAL, t1 + (X / 2 if joined_out else 0))
    fi = X if joined_in else 0.3
    fo = X if joined_out else (2.0 if t1 >= TOTAL else 0.05)
    out = f"assets/music/seg{i}.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{src:.3f}", "-t", f"{b - a:.3f}", "-i", f"{D}/{n}.mp3",
                    "-af", f"loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000,afade=t=in:d={fi},afade=t=out:st={b - a - fo:.3f}:d={fo}",
                    "-ac", "2", out], check=True)
    parts.append((out, a))
inp, fl = [], []
for k, (p, a) in enumerate(parts):
    inp += ["-i", p]; fl.append(f"[{k}]adelay={int(a * 1000)}|{int(a * 1000)}[a{k}]")
inp += ["-i", "assets/vo/vo.wav"]; v = len(parts)
fc = (";".join(fl) + ";" + "".join(f"[a{k}]" for k in range(v)) + f"amix=inputs={v}:normalize=0,apad,atrim=0:{TOTAL}[m];"
      f"[{v}]aformat=channel_layouts=stereo,aresample=48000,apad[k];[m][k]sidechaincompress=threshold=0.05:ratio=4:attack=20:release=500[o]")
subprocess.run(["ffmpeg", "-v", "error", "-y", *inp, "-filter_complex", fc, "-map", "[o]", "-t", str(TOTAL), "assets/music/bed.wav"], check=True)
json.dump(SEG, open("assets/music/bed_plan.json", "w"), indent=1)
print("bed", TOTAL)
