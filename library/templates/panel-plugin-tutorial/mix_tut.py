#!/usr/bin/env python3
"""Audio for a tutorial render: VO lines at their times + CC0 music bed (music_fit, envelope-ducked) + click/chime SFX.
usage: mix_tut.py v1|v2  -> proj_vX/mix.wav (loudnorm -16 LUFS) ; then mux_tut.sh"""
import json, os, subprocess, sys
import numpy as np, soundfile as sf
D = os.path.dirname(os.path.abspath(__file__)); V = sys.argv[1]; P = f"{D}/proj_{V}"
T = json.load(open(f"{P}/timing.json")); SR = 48000
assert not T["stub"], "timing.json was built with stub VO durations: rebuild without --stub"
TOTAL = T["total"]; N = int(TOTAL * SR)
PY = "/home/user/tools/perc-venv/bin/python"
LIB = "/home/user/new-startup/library"

def load(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).copy()

def put(buf, x, at, gain=1.0):
    i = int(at * SR); n = min(len(x), len(buf) - i)
    if n > 0: buf[i:i + n] += x[:n] * gain

# 1. VO
vo = np.zeros(N, np.float32)
for i, (a, b) in T["lines"].items():
    put(vo, load(f"{D}/vo/parts_{V}/{int(i) - 1:03d}.wav"), a)   # parts are 0-indexed: 000.wav = line 1
# loudnorm the VO bed to -16 once (two-pass by ffmpeg)
sf.write(f"{P}/vo_raw.wav", vo, SR)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{P}/vo_raw.wav", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", str(SR), f"{P}/vo.wav"], check=True)
vo = load(f"{P}/vo.wav")[:N]; vo = np.pad(vo, (0, N - len(vo)))

# 2. music bed: music_fit (skill music-for-video) to the exact length, start after the slow intro, soft fade under the end card
bed = f"{P}/bed.wav"; src = f"{LIB}/music/cc0/{T['music']}"
if T.get("music_cut"):   # drop the track's fade-out tail so music_fit never loops through it (chills: fade from 167.5 s)
    src = f"{P}/music_src.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{LIB}/music/cc0/{T['music']}", "-t", str(T["music_cut"]), "-ar", str(SR), src], check=True)
subprocess.run([PY, f"{LIB}/tools/music_fit.py", src, bed, "--length", f"{TOTAL:.2f}", "--start", str(T["music_start"]),
                "--end", "fade", "--fade", "4", "--lufs", "-20"], check=True)
mus = load(bed)[:N]; mus = np.pad(mus, (0, N - len(mus)))
# envelope ducking (#1890 partial ducking): -11 dB under speech, full between, 0.35 s smoothing
act = np.zeros(N, np.float32)
for a, b in T["lines"].values():
    act[max(0, int((a - 0.2) * SR)):int((b + 0.3) * SR)] = 1
k = int(0.35 * SR); act = np.convolve(act, np.ones(k) / k, mode="same")
under, free = 10 ** (-11 / 20), 10 ** (-3 / 20)        # music -20 LUFS bed -> about -23 free / -31 under voice
mus *= free * (1 - act) + under * act
fade_in = int(1.0 * SR); mus[:fade_in] *= np.linspace(0, 1, fade_in)

# 3. SFX: mouse clicks on the recordings' clicks, a soft chime when the console "ready" line is ringed
sfx = np.zeros(N, np.float32)
click = load(f"{LIB}/sfx/ui/mouse-click.mp3"); chime = load(f"{LIB}/sfx/notification/success-chime.mp3")
def norm(x, peak): return x / (np.abs(x).max() + 1e-9) * peak
click = norm(click, 0.35); chime = norm(chime, 0.22)
clicks = [c for s in T["shots"] for c in s["clicks"]]
for c in clicks: put(sfx, click, c)
for c in T["chimes"]: put(sfx, chime, c)

mix = vo + mus + sfx
sf.write(f"{P}/mix_raw.wav", mix, SR)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{P}/mix_raw.wav", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11:linear=true", "-ar", str(SR), f"{P}/mix.wav"], check=True)
print(f"{V}: mix {TOTAL:.1f}s, {len(T['lines'])} lines, {len(clicks)} clicks, {len(T['chimes'])} chimes -> {P}/mix.wav")
