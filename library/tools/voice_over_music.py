# Place voice lines on a music bed at chosen times, duck the bed under them, and normalise.
# Usage: python3 voice_over_music.py spec.json out.wav
# spec.json:
# {
#   "bed": "music.wav", "voice": "take.wav", "total": 21.6,
#   "duck_db": -8, "voice_over_bed_db": 5.5, "lufs": -15,
#   "lines": [ {"at": 3.43, "parts": [[0.06, 1.92], [2.60, 4.08]], "gap": 0.3, "max_len": 3.18}, ... ]
# }
# "parts" are [start, end] seconds in the voice file (take them from a transcript's word timings),
# joined with "gap" seconds between them; a line longer than "max_len" is sped up (atempo) to fit.
# Note: ffmpeg 6.1 drops adelay after concat+atempo, so lines are placed here with numpy instead.
import json, os, subprocess, sys, tempfile, wave
import numpy as np

spec = json.load(open(sys.argv[1]))
out = sys.argv[2]
SR = 48000
TOTAL = spec.get("total", 21.6)

def read(p, ch=None):
    tmp = tempfile.mktemp(suffix=".wav")
    args = ["-ac", str(ch)] if ch else []
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", p, *args, "-ar", str(SR), tmp], check=True)
    w = wave.open(tmp)
    x = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float64) / 32768
    x = x.reshape(-1, w.getnchannels())
    os.remove(tmp)
    return x

n = int(TOTAL * SR)
voc = np.zeros(n)
for line in spec["lines"]:
    parts, gap = line["parts"], line.get("gap", 0.3)
    speech = sum(b - a for a, b in parts) + gap * (len(parts) - 1)
    tempo = max(1.0, speech / line.get("max_len", 1e9))
    chains, labels = [], []
    for k, (a, b) in enumerate(parts):
        pad = f",apad=pad_dur={gap}" if k < len(parts) - 1 else ""
        chains.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.03,afade=t=out:st={b - a - 0.06:.3f}:d=0.06{pad}[p{k}]")
        labels.append(f"[p{k}]")
    fc = ";".join(chains) + f";{''.join(labels)}concat=n={len(parts)}:v=0:a=1,atempo={tempo:.4f}[o]"
    tmp = tempfile.mktemp(suffix=".wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", spec["voice"], "-filter_complex", fc, "-map", "[o]", "-ac", "1", "-ar", str(SR), tmp], check=True)
    x = read(tmp, 1)[:, 0]
    os.remove(tmp)
    i = int(line["at"] * SR)
    j = min(n, i + len(x))
    voc[i:j] += x[: j - i]
    print(f"line at {line['at']:.2f}s: {len(x) / SR:.2f}s (tempo {tempo:.3f})")

# Voice polish: rumble cut, less mud, presence, gentle compression, small room.
tmp_in, tmp_out = tempfile.mktemp(suffix=".wav"), tempfile.mktemp(suffix=".wav")
with wave.open(tmp_in, "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(voc, -1, 1) * 32767).astype("<i2").tobytes())
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp_in, "-af",
                "highpass=f=90,equalizer=f=250:t=q:w=1:g=-2,equalizer=f=3500:t=q:w=1.2:g=2,"
                "acompressor=threshold=-20dB:ratio=3:attack=8:release=120,aecho=0.8:0.6:70|140:0.18|0.10",
                "-ac", "2", "-ar", str(SR), tmp_out], check=True)
voc2 = read(tmp_out, 2)[:n]
bed = read(spec["bed"], 2)[:n]
m = min(len(bed), len(voc2)); bed, voc2 = bed[:m], voc2[:m]
os.remove(tmp_in); os.remove(tmp_out)

# Duck envelope from voice activity (holds through gaps < 0.5 s so the bed doesn't pump).
act = np.convolve(np.abs(voc2).mean(1), np.ones(int(0.05 * SR)) / int(0.05 * SR), mode="same")
on = act > 0.004
hold, last = int(0.5 * SR), -10**9
for i in range(m):
    if on[i]: last = i
    elif i - last < hold: on[i] = True
duck = 10 ** (spec.get("duck_db", -8) / 20)
env, g = np.empty(m), 1.0
for i in range(m):
    t = duck if on[i] else 1.0
    g += (t - g) * (6 / (0.25 * SR) if t < g else 6 / (0.6 * SR))
    env[i] = g
bed_d = bed * env[:, None]
rms = lambda x: np.sqrt(np.mean(x ** 2))
gain = 10 ** (spec.get("voice_over_bed_db", 5.5) / 20) * rms(bed_d[on]) / rms(voc2[on])
mix = bed_d + voc2 * gain
mix /= max(1.0, np.abs(mix).max() / 0.95)
tmp_mix = tempfile.mktemp(suffix=".wav")
with wave.open(tmp_mix, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype("<i2").tobytes())
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp_mix, "-af", f"loudnorm=I={spec.get('lufs', -15)}:TP=-1.5:LRA=11", "-ar", str(SR), out], check=True)
os.remove(tmp_mix)
print(f"wrote {out}: voice gain {20 * np.log10(gain):+.1f} dB, voice {spec.get('voice_over_bed_db', 5.5)} dB over the ducked bed")
