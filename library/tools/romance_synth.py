# Copyright-free romantic instrumental: 72 BPM, 6 bars (20 s) + reverb tail.
import sys, wave
import numpy as np

SR = 48000
BPM = 72
BEAT = 60 / BPM
BAR = 4 * BEAT
TOTAL = 6 * BAR + 1.6
N = int(TOTAL * SR)
rng = np.random.default_rng(72)
L = np.zeros(N)
R = np.zeros(N)

def hz(note):
    names = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}
    n, o = note[:-1], int(note[-1])
    return 440.0 * 2 ** ((names[n] + 12 * (o + 1) - 69) / 12)

def put(sig, t0, pan=0.0, gain=1.0):
    i = int(t0 * SR)
    j = min(N, i + len(sig))
    s = sig[: j - i] * gain
    L[i:j] += s * np.sqrt(0.5 * (1 - pan))
    R[i:j] += s * np.sqrt(0.5 * (1 + pan))

def piano(f, dur, vel=1.0):
    t = np.arange(int((dur + 2.5) * SR)) / SR
    out = np.zeros_like(t)
    for n in range(1, 10):
        fn = f * n * np.sqrt(1 + 0.0004 * n * n)
        if fn > SR / 2.2:
            break
        out += (1 / n ** 1.35) * np.sin(2 * np.pi * fn * t) * np.exp(-t * (0.9 + f / 900 + 0.55 * n))
    att = np.minimum(1, t / 0.004)
    rel = np.where(t > dur, np.exp(-(t - dur) * 7), 1.0)
    return out * att * rel * vel * 0.28

def strings(freqs, dur):
    t = np.arange(int((dur + 1.2) * SR)) / SR
    out = np.zeros_like(t)
    vib = 1 + 0.0025 * np.sin(2 * np.pi * 5.2 * t)
    for f in freqs:
        for cents in (-9, -3, 4, 10):
            fd = f * 2 ** (cents / 1200)
            phase = 2 * np.pi * np.cumsum(fd * vib) / SR + rng.uniform(0, 6.28)
            for n in range(1, 14):
                if fd * n > 9000:
                    break
                out += (1 / n ** 1.7) * np.sin(n * phase)
    env = np.minimum(1, t / 0.9) * np.where(t > dur, np.exp(-(t - dur) * 3.2), 1.0)
    return out * env * 0.018

def bell(f, vel=1.0):
    t = np.arange(int(3.0 * SR)) / SR
    out = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 3)
    return out * np.exp(-t * 1.6) * np.minimum(1, t / 0.002) * vel * 0.09

def thump(vel=1.0):
    t = np.arange(int(0.5 * SR)) / SR
    f = 55 + 70 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9) * vel * 0.26

def shaker(vel=1.0):
    t = np.arange(int(0.12 * SR)) / SR
    noise = rng.standard_normal(len(t))
    noise = np.diff(np.concatenate([[0], noise]))  # tilt toward highs
    return noise * np.exp(-t * 45) * np.minimum(1, t / 0.01) * vel * 0.03

# Chords per half bar: (root bass, chord tones)
C = (["C3"], ["C4", "E4", "G4", "B4"])
Am = (["A2"], ["A3", "C4", "E4", "G4"])
F = (["F2"], ["F3", "A3", "C4", "E4"])
G = (["G2"], ["G3", "B3", "D4", "F#4"])
Gs = (["G2"], ["G3", "B3", "D4", "A4"])
halves = [C, C, Am, Am, F, F, Gs, G, Am, F, C]  # bar 5 splits Am|F; bar 6 holds C to the end

# Opening shimmer: a bell glissando into bar 1.
for k, n in enumerate(["G5", "C6", "E6", "G6", "C7"]):
    put(bell(hz(n), 0.8), 0.02 + k * 0.09, pan=-0.4 + k * 0.2)

for h, (bass, tones) in enumerate(halves):
    t0 = h * BAR / 2
    last = h == len(halves) - 1
    span = BAR / 2 if not last else BAR + 1.0
    if h % 2 == 0 or halves[h] != halves[h - 1]:
        dur = span if last else (BAR if h + 1 < len(halves) and halves[h + 1] == halves[h] else BAR / 2)
        put(strings([hz(n) for n in tones[:3]], dur), t0, pan=0.0, gain=1.0)
        put(piano(hz(bass[0]), dur, 0.8), t0, pan=-0.15)
    # Broken-chord eighths, softer on off-beats.
    pattern = [tones[0], tones[2], tones[3], tones[1]]
    steps = 4 if not last else 1
    for s in range(steps):
        n = pattern[s % 4]
        up = n[:-1] + str(int(n[-1]) + 1)
        put(piano(hz(up), BEAT * 0.9, 0.55 if s % 2 else 0.7), t0 + s * BEAT / 2, pan=0.25)
        if not last:
            put(piano(hz(pattern[(s + 2) % 4]), BEAT * 0.9, 0.35), t0 + s * BEAT / 2 + BEAT / 4, pan=-0.3)

# Melody (start beat within the film, beats long).
mel = [
    (4, "A4", 1), (5, "C5", 1), (6, "E5", 2),
    (8, "F5", 1.5), (9.5, "E5", 0.5), (10, "C5", 2),
    (12, "D5", 1), (13, "E5", 1), (14, "G5", 1), (15, "D5", 1),
    (16, "C5", 1), (17, "E5", 1), (18, "A5", 1), (19, "G5", 1),
    (20, "E5", 2), (22, "C5", 4),
]
for b, n, d in mel:
    put(piano(hz(n), d * BEAT * 0.95, 1.0), b * BEAT, pan=0.05, gain=1.15)
    put(bell(hz(n) * 2, 0.25), b * BEAT, pan=0.3)

# Gentle pulse from bar 2: thump on 1 and 3, shaker on the eighths.
for beat in range(4, 24):
    if beat % 2 == 0:
        put(thump(0.8 if beat % 4 == 0 else 0.55), beat * BEAT)
    for e in range(2):
        put(shaker(0.9 if e else 0.5), beat * BEAT + e * BEAT / 2, pan=0.35)
# Final chime on the freeze-frame bar.
for k, n in enumerate(["C6", "E6", "G6"]):
    put(bell(hz(n), 0.9), 20 * BEAT + k * 0.05, pan=-0.2 + k * 0.2)

# Stereo convolution reverb.
def reverb(x, seed):
    g = np.random.default_rng(seed)
    t = np.arange(int(2.4 * SR)) / SR
    ir = g.standard_normal(len(t)) * np.exp(-t * 2.6)
    ir[: int(0.012 * SR)] = 0
    ir /= np.sqrt(np.sum(ir ** 2))
    n = 1 << int(np.ceil(np.log2(len(x) + len(ir))))
    y = np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(ir, n), n)[: len(x)]
    return y

wetL, wetR = reverb(L, 1), reverb(R, 2)
L = L + 0.45 * wetL
R = R + 0.45 * wetR
# Fade the tail and normalise to -1 dBFS peak.
fade = np.ones(N)
tail = int(1.2 * SR)
fade[-tail:] = np.linspace(1, 0, tail) ** 2
L, R = L * fade, R * fade
peak = max(np.abs(L).max(), np.abs(R).max())
L, R = L / peak * 0.89, R / peak * 0.89
pcm = (np.stack([L, R], 1) * 32767).astype("<i2")
with wave.open(sys.argv[1], "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print(f"wrote {TOTAL:.2f}s")
