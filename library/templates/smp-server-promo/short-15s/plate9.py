# 9:16 footage plate cut on the music's beats (owner's 15 s FireCraft cut-down of portal order 4, 2026-10-30).
# Each shot: 60 fps gameplay at 0.5x (real frames), 9:16 crop of the 16:9 source at a chosen centre, lanczos to
# 1080x1920 + cas=strength=0.5 (CLAUDE.md: 9:16 crops of 1080p gameplay are an upscale, skill #489), same grade as
# smp-server-promo/plate.py, hard cuts on the beat/downbeat times measured with listen.py on the fitted bed.
#   python3 plate9.py SHOTS.json OUT.mp4     SHOTS = {"total": s, "shots": [[cut_s, file, in_s, x_centre_0..1], ...]}
import json, subprocess, sys

J = json.load(open(sys.argv[1]))
SH, TOTAL = J["shots"], J["total"]
SPEED = 0.5
GRADE = ("eq=contrast=1.08:saturation=1.12:gamma=0.97,"
         "colorbalance=rs=-0.04:bs=0.05:rh=0.05:bh=-0.03,vignette=angle=PI/5")
args, ch = [], []
for i, (cut, f, a, xc) in enumerate(SH):
    d = (SH[i + 1][0] if i + 1 < len(SH) else TOTAL) - cut
    args += ["-ss", str(a), "-t", f"{d * SPEED + 0.2:.3f}", "-i", f]
    crop = f"crop=ih*9/16:ih:(iw-ih*9/16)*{xc}:0"
    ch.append(f"[{i}:v]setpts=PTS/{SPEED},fps=30,{crop},scale=1080:1920:flags=lanczos,cas=strength=0.5,{GRADE},"
              f"trim=0:{d:.3f},setpts=PTS-STARTPTS,format=yuv420p[v{i}]")
ch.append("".join(f"[v{i}]" for i in range(len(SH))) + f"concat=n={len(SH)}:v=1:a=0[out]")
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"] + args +
               ["-filter_complex", ";".join(ch), "-map", "[out]", "-an", "-c:v", "libx264", "-crf", "16", "-preset", "medium",
                "-r", "30", sys.argv[2]], check=True)
print("plate9", sys.argv[2], TOTAL, len(SH), "shots")
