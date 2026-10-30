# Beat events for music-driven edits (phonk / drift / velocity): beats + downbeats (listen.py's grid) plus KICKS (low
# band onsets) and SNARES (mid/high band onsets that land on beats 2 and 4 or between), and the strongest hits.
# The phonk formula (Onset Engine guide, https://onsetengine.com/guides/make-phonk-drift-edits/, read 2026-10-29):
#   808 kick -> 4-6% impact zoom with fast snap-back; snare -> ~2.5 px red/blue split; bass drop -> 1-frame white flash
#   (~120 ms decay); a hard cut on every beat; desaturated, high-contrast, cold grade.
#   /home/user/tools/perc-venv/bin/python beat_events.py bed.wav out.json [--start 0 --end 30]
import argparse, json
import numpy as np
import librosa

ap = argparse.ArgumentParser()
ap.add_argument("audio")
ap.add_argument("out")
ap.add_argument("--start", type=float, default=0.0)
ap.add_argument("--end", type=float, default=None)
a = ap.parse_args()

y, sr = librosa.load(a.audio, sr=22050, mono=True)
hop = 256
S = np.abs(librosa.stft(y, n_fft=2048, hop_length=hop))
f = librosa.fft_frequencies(sr=sr, n_fft=2048)


def band_onsets(lo, hi, delta):
    env = librosa.onset.onset_strength(S=librosa.amplitude_to_db(S[(f >= lo) & (f < hi)], ref=np.max), sr=sr, hop_length=hop)
    env = env / (env.max() + 1e-9)
    fr = librosa.onset.onset_detect(onset_envelope=env, sr=sr, hop_length=hop, delta=delta, wait=int(0.12 * sr / hop))
    return [(round(float(t), 3), round(float(env[i]), 3)) for t, i in zip(librosa.frames_to_time(fr, sr=sr, hop_length=hop), fr)]


tempo, bf = librosa.beat.beat_track(y=y, sr=sr, hop_length=hop)
beats = [round(float(t), 3) for t in librosa.frames_to_time(bf, sr=sr, hop_length=hop)]
kicks = band_onsets(30, 150, 0.12)
snares = band_onsets(1500, 6000, 0.14)
rms = librosa.feature.rms(y=y, hop_length=hop)[0]
t_rms = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=hop)
end = a.end if a.end is not None else len(y) / sr
keep = lambda L: [x for x in L if a.start <= (x[0] if isinstance(x, tuple) else x) <= end]
strong = sorted(keep(kicks), key=lambda x: -x[1])[: max(3, len(keep(kicks)) // 6)]
out = {"source": a.audio, "tempo_librosa": float(np.atleast_1d(tempo)[0]), "beats": keep(beats),
       "kicks": keep(kicks), "snares": keep(snares), "strong_kicks": sorted(strong),
       "note": "kicks/snares = [time s, onset strength 0-1]; strong_kicks = top sixth of kicks (flash/stutter candidates)"}
json.dump(out, open(a.out, "w"), indent=1)
print(f"{len(out['beats'])} beats, {len(out['kicks'])} kicks, {len(out['snares'])} snares, {len(strong)} strong -> {a.out}")
