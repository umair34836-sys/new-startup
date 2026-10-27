#!/home/user/tools/perc-venv/bin/python
# Usage: /home/user/tools/perc-venv/bin/python library/tools/mix_vo_music.py VO.wav MUSIC.wav OUT.wav
#            [--vo-at 0.0] [--duck-db -10] [--gap 12] [--dip-db -4] [--lufs -14] [--tp -1] [--sfx sfx.wav]
# Mixes a FINISHED voice-over (one file, already timed, e.g. vs_tts.py output) over a fitted music bed
# (music_fit.py output) the way a mixer does it, and measures the result:
#   * the bed ducks --duck-db under speech (attack 60 ms, release 400 ms, gaps < 0.5 s held so it does not pump);
#     defaults from skills #314/#315 (6-12 dB, attack 30-80 ms, release 250-700 ms) and #313/#318;
#   * while the voice talks, the bed's speech band (1.5-4 kHz) is dipped --dip-db more (iZotope, skills #1848),
#     so the music keeps its body but leaves the consonants clear;
#   * the voice is set --gap dB over the ducked bed (speech-weighted loudness, BS.1770 via pyloudnorm), then the
#     whole mix is normalised to --lufs integrated with a --tp dBTP ceiling (ffmpeg alimiter);
#   * report: voice LUFS vs music LUFS during speech (the "music-vs-VO gap"), music LUFS in pauses, final LUFS / true
#     peak / clipped samples. Use voice_over_music.py instead when lines must be cut from one take and placed.
# Settings, sources and a measured test: library/research/music-for-video.md + music-for-video-tests.md.
import argparse, json, os, subprocess, wave
import numpy as np
import pyloudnorm as pyln
from scipy.signal import butter, sosfiltfilt

SR = 48000
ap = argparse.ArgumentParser()
ap.add_argument("vo")
ap.add_argument("music")
ap.add_argument("out")
ap.add_argument("--vo-at", type=float, default=0.0, help="where the VO file starts in the music (s)")
ap.add_argument("--duck-db", type=float, default=-10.0)
ap.add_argument("--gap", type=float, default=12.0, help="voice loudness over the ducked music during speech (LU)")
ap.add_argument("--dip-db", type=float, default=-4.0, help="extra cut of the music's 1.5-4 kHz band under speech")
ap.add_argument("--lufs", type=float, default=-14.0)
ap.add_argument("--tp", type=float, default=-1.0)
ap.add_argument("--sfx", help="optional SFX stem (already timed, same start as the music) mixed at its own level")
a = ap.parse_args()


def read(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)


music = read(a.music)
vo0 = read(a.vo)
n = len(music)
vo = np.zeros_like(music)
i0 = int(a.vo_at * SR)
m = min(len(vo0), n - i0)
vo[i0:i0 + m] = vo0[:m]

# speech activity from the VO's own level (50 ms RMS above -45 dBFS and within 30 dB of its loud parts)
w = int(0.05 * SR)
k = n // w
r = np.sqrt(np.mean(vo[: k * w].mean(1).reshape(k, w) ** 2, axis=1))
rdb = 20 * np.log10(np.maximum(r, 1e-9))
act = (rdb > -45) & (rdb > np.percentile(rdb[rdb > -80], 95) - 30 if (rdb > -80).any() else False)
hold = int(0.5 / 0.05)
on = act.copy()
last = -10 ** 9
for i in range(k):
    if act[i]:
        last = i
    elif i - last <= hold:
        on[i] = True
# gain envelope with attack/release (one-pole per 50 ms block, then interpolated per sample)
g_duck = 10 ** (a.duck_db / 20)
att, rel = 0.06, 0.40
g, env = 1.0, np.empty(k)
for i in range(k):
    tgt = g_duck if on[i] else 1.0
    c = 1 - np.exp(-0.05 / (att if tgt < g else rel))
    g += (tgt - g) * c
    env[i] = g
t_blk = (np.arange(k) + 0.5) * w
env_s = np.interp(np.arange(n), t_blk, env)
# speech-band dip: split 1.5-4 kHz out of the bed and lower it in proportion to the duck
sos = butter(4, [1500, 4000], btype="band", fs=SR, output="sos")
band = sosfiltfilt(sos, music, axis=0)
depth = (1 - env_s) / max(1e-9, 1 - g_duck)  # 0 = no speech .. 1 = fully ducked
band_gain = 10 ** (a.dip_db * depth / 20)
bed = (music - band + band * band_gain[:, None]) * env_s[:, None]

meter = pyln.Meter(SR)
sp = np.repeat(on, w)[:n] if k * w >= n else np.concatenate([np.repeat(on, w), np.zeros(n - k * w, bool)])


def lufs(x, mask=None):
    y = x[mask] if mask is not None else x
    if len(y) < SR // 2:
        return None
    v = meter.integrated_loudness(y)
    return float(v) if np.isfinite(v) else None


vo_l = lufs(vo, sp)
bed_l = lufs(bed, sp)
gain_vo = 10 ** ((bed_l + a.gap - vo_l) / 20) if vo_l is not None and bed_l is not None else 1.0
vo_g = vo * gain_vo
mix = bed + vo_g
if a.sfx:
    s = read(a.sfx)
    mix[: min(n, len(s))] += s[:n]
tot = lufs(mix)
mix *= 10 ** ((a.lufs - tot) / 20)
scale = 10 ** ((a.lufs - tot) / 20)
tmp = a.out + ".tmp.f32"
mix.astype(np.float32).tofile(tmp)
lim = 10 ** ((a.tp - 1.0) / 20)  # alimiter works on sample peaks: 1 dB margin covers inter-sample overshoot
extra = 0.0
for _ in range(4):  # the limiter shaves loudness off peaks: add it back until the target is met (<= 0.2 LU)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", tmp, "-af",
                    f"volume={extra:.2f}dB,alimiter=limit={lim:.4f}:level=false:attack=1:release=50",
                    "-ar", str(SR), "-c:a", "pcm_s16le", a.out], check=True)
    got = lufs(read(a.out))
    if got is None or a.lufs - got <= 0.2:
        break
    extra += a.lufs - got
scale *= 10 ** (extra / 20)
os.remove(tmp)

# ---- measure the result ----
fin = read(a.out)[:n]
musf = bed * scale
vof = vo_g * scale
pause = ~sp & (np.abs(musf).mean(1) > 1e-5)
tp = float(np.abs(np.repeat(fin, 4, axis=0)).max())  # crude; listen.py gives the 4x-oversampled true peak
rep = {
    "vo_lufs_during_speech": round(lufs(vof, sp), 1) if lufs(vof, sp) is not None else None,
    "music_lufs_during_speech": round(lufs(musf, sp), 1) if lufs(musf, sp) is not None else None,
    "music_lufs_in_pauses": round(lufs(musf, pause), 1) if lufs(musf, pause) is not None else None,
    "final_lufs": round(lufs(fin), 1),
    "final_sample_peak_dbfs": round(20 * np.log10(max(1e-9, float(np.abs(fin).max()))), 2),
    "clipped_samples": int((np.abs(fin) >= 0.999).sum()),
    "speech_s": round(float(sp.sum()) / SR, 1),
    "limiter_extra_gain_db": round(extra, 2),
    "settings": {"duck_db": a.duck_db, "gap_lu": a.gap, "dip_db": a.dip_db, "lufs": a.lufs, "tp": a.tp,
                 "attack_s": att, "release_s": rel, "hold_s": 0.5},
}
if rep["vo_lufs_during_speech"] is not None and rep["music_lufs_during_speech"] is not None:
    rep["music_vs_vo_gap_lu"] = round(rep["vo_lufs_during_speech"] - rep["music_lufs_during_speech"], 1)
json.dump(rep, open(os.path.splitext(a.out)[0] + ".mix.json", "w"), indent=1)
print(f"mix_vo_music -> {a.out}")
print(json.dumps(rep, indent=1))
