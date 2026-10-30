#!/usr/bin/env python3
# Join chosen VO line takes (e.g. from several vs_tts.py --parts runs / seeds) into one voiceover, like vs_tts.py does:
# each line pitch-matched to the same median f0 first (takes from different runs/seeds have different pitch: measured
# 171 / 185 / 196 Hz on 2026-10-25), then joined with --gap s of silence, loudnorm -16 LUFS, lines.json written.
#   python3 vo_join.py OUT.wav line1.wav line2.wav ... [--gap 0.45] [--target-f0 172] [--lines OUT_lines.json]
# Needs pyworld + numpy (system python3, as vs_tts.py; setup-all light) and ffmpeg with rubberband.
import argparse, json, os, subprocess, tempfile
import numpy as np, pyworld

ap = argparse.ArgumentParser()
ap.add_argument("out")
ap.add_argument("takes", nargs="+")
ap.add_argument("--gap", type=float, default=0.45)
ap.add_argument("--target-f0", type=float, default=172.0, help="voices.json 'default' uses 172")
ap.add_argument("--lines", help="where to write [start, end] per line (default: <out dir>/lines.json)")
a = ap.parse_args()


def median_f0(path):
    x = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", "16000", "-f", "f64le", "-"],
                       capture_output=True, check=True).stdout
    f0, _ = pyworld.harvest(np.frombuffer(x, np.float64), 16000)
    return float(np.median(f0[f0 > 0]))


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                capture_output=True, text=True).stdout)


tmp = tempfile.mkdtemp(prefix="vo_join_")
fixed = []
for i, p in enumerate(a.takes):
    q = os.path.join(tmp, f"{i:03d}.wav")
    before = median_f0(p)
    ratio = a.target_f0 / before
    for _ in range(4):  # the measured median after rubberband can miss (160 -> 192 Hz in one pass): correct and redo
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", p, "-af", f"aresample=44100,aformat=channel_layouts=mono,"
                        f"rubberband=pitch={ratio:.5f}:formant=preserved:pitchq=quality", q], check=True)
        after = median_f0(q)
        if abs(after - a.target_f0) <= 3:
            break
        ratio *= a.target_f0 / after
    print(f"{i + 1}: {os.path.basename(p)} median {before:.0f} Hz -> {after:.0f} Hz (x{ratio:.3f}), {dur(q):.2f} s")
    fixed.append(q)

inputs, chains = [], []
for i, q in enumerate(fixed):
    inputs += ["-i", q]
    chains.append(f"[{i}]apad=pad_dur={a.gap}[a{i}]")
graph = ";".join(chains) + ";" + "".join(f"[a{i}]" for i in range(len(fixed))) + \
    f"concat=n={len(fixed)}:v=0:a=1,loudnorm=I=-16:TP=-1.5[out]"
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", graph, "-map", "[out]", "-ar", "44100", a.out], check=True)
spans, t = [], 0.0
for q in fixed:
    d = dur(q)
    spans.append([round(t, 3), round(t + d, 3)]); t += d + a.gap
json.dump(spans, open(a.lines or os.path.join(os.path.dirname(os.path.abspath(a.out)), "lines.json"), "w"))
print("wrote", a.out, f"{dur(a.out):.2f} s", spans)
