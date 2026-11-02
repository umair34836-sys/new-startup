# Footage plate for build.py kind "clip": one graded 1920x1080 30 fps video, one shot per scene, cut at the same scene
# times build.py uses (first scene 0, then VO0 + line start - 0.15; last ends end_hold after the last line).
# Each shot = 60 fps gameplay played at 0.5x (cinematic slow motion with real frames, no interpolation), lanczos to
# 1080p + cas sharpen (skill #489, CLAUDE.md 9:16 note), cool-warm cinematic grade + vignette, 0.4 s xfade between shots.
#   python3 plate.py CONFIG.json OUT.mp4      (CONFIG scenes[i]["src"] = [file, in_seconds])
import json, subprocess, sys

C = json.load(open(sys.argv[1]))
OUT = sys.argv[2]
L = json.load(open(C["vo_lines"]))
VO0 = C.get("vo_start", 0.6)
SC = C["scenes"]
t0 = [0 if i == 0 else round(VO0 + L[s["line"]][0] - 0.15, 3) for i, s in enumerate(SC)]
t1 = t0[1:] + [round(VO0 + L[-1][1] + C.get("end_hold", 3.5), 3)]
XF = 0.4
SPEED = C.get("plate_speed", 0.5)
GRADE = ("scale=1920:1080:flags=lanczos,cas=strength=0.5,"
         "eq=contrast=1.08:saturation=1.12:gamma=0.97,"
         "colorbalance=rs=-0.04:bs=0.05:rh=0.05:bh=-0.03,vignette=angle=PI/5")
args, chains = [], []
for i, s in enumerate(SC):
    f, a = s["src"]
    d = (t1[i] - t0[i]) + (XF if i + 1 < len(SC) else 0)
    args += ["-ss", str(a), "-t", f"{d * SPEED + 0.2:.3f}", "-i", f]
    chains.append(f"[{i}:v]setpts=PTS/{SPEED},fps=30,{GRADE},trim=0:{d:.3f},setpts=PTS-STARTPTS,format=yuv420p[v{i}]")
prev, off = "v0", 0.0
for i in range(1, len(SC)):
    off = t0[i]  # each shot (but the last) is XF longer than its scene, so the fade starts on the cut time
    chains.append(f"[{prev}][v{i}]xfade=transition=fade:duration={XF}:offset={off:.3f}[x{i}]")
    prev = f"x{i}"
fc = ";".join(chains)
cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"] + args + ["-filter_complex", fc, "-map", f"[{prev}]", "-an",
                                                                       "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-r", "30", OUT]
subprocess.run(cmd, check=True)
print("plate", OUT, list(zip(t0, t1)))
