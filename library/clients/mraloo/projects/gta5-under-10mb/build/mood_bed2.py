# GTA 5 under 10 MB, bed v3: same tracks and moods as mood_bed.py (client guide "Background music"), now anchored to VO
# words so it follows any VO edit. Music STOPS on the topic-change bumpers (the bumper's glitch + hit carries the cut,
# client voice note) and restarts right after the spoken heading; stops before "lekin bhai" and before the punchline.
# Raw bed only: ducking under the voice is done in mix.py (gain automation from the VO envelope).
import json, subprocess
D = "../../odrive"
W = json.load(open("words.json"))
ws = lambda i: W[i][0]
we = lambda i: W[i][1]
TOTAL = round(W[-1][1] + 1.6, 2)
BUMP = [(261, 264), (417, 421), (565, 568)]
b0 = [round(ws(h0) - 0.15, 3) for h0, _ in BUMP]          # bumper starts (build.py BUMP)
b1 = [round(we(h1) + 0.35, 3) for _, h1 in BUMP]          # bumper ends
SEG = [  # (track, source in-point, start, end, why)
    ("euphoria", 0.0, 0.0, ws(70) - 0.14, "hook: energetic; stops before 'lekin bhai...'"),
    ("apocalyptic-echoes", 0.0, ws(83) - 0.15, ws(110), "after the scam reveal: low suspense"),
    ("silly-snickerdoodle", 0.0, ws(110), b0[0], "scene 2 fake tutorial: playful"),
    ("pouncin-bouncin", 0.0, b1[0], b0[1], "scene 3 permissions: comic suspense"),
    ("demented-90s", 7.5, b1[1], b0[2], "scene 4 reality check: light comedy"),
    ("on-the-flip", 21.4, b1[2], ws(719), "scene 5 safety tips: calm"),
    ("challenge-accepted", 0.0, ws(719), ws(770) - 0.1, "scene 6 roast: dramatic build-up, stops before the punchline"),
    ("euphoria", 60.0, ws(775) - 0.15, TOTAL, "outro: back to the opening energy"),
]
X = 0.8
parts = []
for i, (n, src, t0, t1, _) in enumerate(SEG):
    joined_in = i > 0 and abs(SEG[i - 1][3] - t0) < 0.01
    joined_out = i + 1 < len(SEG) and abs(SEG[i + 1][2] - t1) < 0.01
    a = max(0.0, t0 - (X / 2 if joined_in else 0)); b = min(TOTAL, t1 + (X / 2 if joined_out else 0))
    fi = X if joined_in else 0.02           # hard restart after a bumper / stop = a drop
    fo = X if joined_out else (2.0 if t1 >= TOTAL else 0.05)
    out = f"assets/music/seg{i}.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{src:.3f}", "-t", f"{b - a:.3f}", "-i", f"{D}/{n}.mp3",
                    "-af", f"loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000,afade=t=in:d={fi},afade=t=out:st={b - a - fo:.3f}:d={fo}",
                    "-ac", "2", out], check=True)
    parts.append((out, a))
inp, fl = [], []
for k, (p, a) in enumerate(parts):
    inp += ["-i", p]; fl.append(f"[{k}]adelay={int(a * 1000)}|{int(a * 1000)}[a{k}]")
fc = ";".join(fl) + ";" + "".join(f"[a{k}]" for k in range(len(parts))) + f"amix=inputs={len(parts)}:normalize=0,apad,atrim=0:{TOTAL}[m]"
subprocess.run(["ffmpeg", "-v", "error", "-y", *inp, "-filter_complex", fc, "-map", "[m]", "-t", str(TOTAL), "assets/music/bed_raw.wav"], check=True)
json.dump([[n, src, round(a, 3), round(b, 3), why] for n, src, a, b, why in SEG], open("assets/music/bed_plan.json", "w"), indent=1)
print("bed_raw", TOTAL)
