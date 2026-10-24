#!/usr/bin/env python3
"""Make our own sound effects with numpy (no download, no credit: made by us).

    python3 library/tools/synth_sfx.py out_dir            # all effects as 48 kHz 16-bit WAV
    python3 library/tools/synth_sfx.py out_dir --only whoosh-up-0.6s,riser-4s
    python3 library/tools/synth_sfx.py --list

Deterministic (fixed seeds), so the same command always writes the same files.
"""
import argparse
import os
import sys
import wave

import numpy as np

SR = 48000


def t_(d):
    return np.arange(int(d * SR)) / SR


def rng(seed):
    return np.random.default_rng(seed)


def env_adsr(n, a=0.005, d=0.1, s=0.0, r=0.05, hold=0.0):
    a_, d_, h_, r_ = (int(x * SR) for x in (a, d, hold, r))
    e = np.concatenate([np.linspace(0, 1, max(a_, 1)), np.linspace(1, s, max(d_, 1)), np.full(max(h_, 0), s),
                        np.linspace(s, 0, max(r_, 1))])
    return np.pad(e, (0, max(0, n - len(e))))[:n]


def exp_decay(n, tau):
    return np.exp(-np.arange(n) / (tau * SR))


def onepole_lp(x, fc):
    """Time-varying one-pole low-pass; fc may be an array (Hz)."""
    fc = np.broadcast_to(np.asarray(fc, float), x.shape)
    a = 1 - np.exp(-2 * np.pi * fc / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc += a[i] * (x[i] - acc)
        y[i] = acc
    return y


def bandpass(x, fc, q=2.0):
    """Time-varying state-variable band-pass (Chamberlin)."""
    fc = np.broadcast_to(np.asarray(fc, float), x.shape)
    f = 2 * np.sin(np.pi * np.minimum(fc, SR / 6) / SR)
    damp = 1 / q
    lo = bp = 0.0
    y = np.empty_like(x)
    for i in range(len(x)):
        hi = x[i] - lo - damp * bp
        bp += f[i] * hi
        lo += f[i] * bp
        y[i] = bp
    return y


def sine_sweep(f0, f1, d, curve="exp"):
    t = t_(d)
    f = f0 * (f1 / f0) ** (t / d) if curve == "exp" else f0 + (f1 - f0) * t / d
    return np.sin(2 * np.pi * np.cumsum(f) / SR)


def bell(freq, d, partials=((1, 1), (2.76, 0.5), (5.4, 0.25), (8.93, 0.12)), tau=0.4):
    t = t_(d)
    y = sum(a * np.sin(2 * np.pi * freq * m * t) * np.exp(-t / (tau / (1 + 0.6 * k)))
            for k, (m, a) in enumerate(partials))
    return y * env_adsr(len(t), a=0.002, d=0.01, s=1, r=0.01, hold=d)


def place(total, *items):
    """items: (start_s, signal)"""
    out = np.zeros(int(total * SR))
    for s, sig in items:
        i = int(s * SR)
        n = min(len(sig), len(out) - i)
        out[i:i + n] += sig[:n]
    return out


def norm(x, peak=0.89):
    m = np.max(np.abs(x)) or 1
    return x / m * peak


def stereo_pan_sweep(x, l0=-0.8, l1=0.8):
    p = np.linspace(l0, l1, len(x))
    return np.stack([x * np.sqrt((1 - p) / 2), x * np.sqrt((1 + p) / 2)], -1)


# ---- effects ------------------------------------------------------------------------------------------
def whoosh(d, up=True, seed=1, center=0.55, pan=True):
    n = int(d * SR)
    noise = rng(seed).standard_normal(n)
    t = np.linspace(0, 1, n)
    shape = np.exp(-((t - center) ** 2) / (2 * (0.18 if d > 0.5 else 0.22) ** 2))
    fc = (300 + 3500 * t) if up else (3800 - 3300 * t)
    y = bandpass(noise, fc * (0.6 + 0.8 * shape), q=1.2) * shape
    y = norm(y)
    return stereo_pan_sweep(y) if pan else y


def swipe(d=0.25, seed=2):
    n = int(d * SR)
    t = np.linspace(0, 1, n)
    y = bandpass(rng(seed).standard_normal(n), 1500 + 5000 * t, q=1.5) * np.sin(np.pi * t) ** 1.5
    return norm(y)


def riser(d=4.0, seed=3):
    t = t_(d)
    n = len(t)
    noise = bandpass(rng(seed).standard_normal(n), 400 + 7000 * (t / d) ** 2, q=1.0)
    tone = sum(np.sin(2 * np.pi * np.cumsum(f0 * 2 ** (2 * t / d)) / SR) for f0 in (110, 165, 220.5))
    amp = (t / d) ** 2.2
    y = (0.7 * noise / np.max(np.abs(noise)) + 0.35 * tone / 3) * amp
    y[-int(0.01 * SR):] *= np.linspace(1, 0, int(0.01 * SR))
    return norm(y)


def downlifter(d=2.0, seed=4):
    t = t_(d)
    n = len(t)
    noise = bandpass(rng(seed).standard_normal(n), 6000 * (1 - t / d) ** 2 + 200, q=1.0)
    tone = np.sin(2 * np.pi * np.cumsum(440 * 2 ** (-3 * t / d)) / SR)
    y = (noise / np.max(np.abs(noise)) * 0.7 + 0.3 * tone) * np.exp(-3 * t / d)
    return norm(y)


def impact(d=2.5, seed=5, low=48):
    t = t_(d)
    n = len(t)
    sub = np.sin(2 * np.pi * np.cumsum(low * 2 ** (-1.2 * t)) / SR) * exp_decay(n, 0.6)
    click = rng(seed).standard_normal(n) * exp_decay(n, 0.012)
    body = onepole_lp(rng(seed + 1).standard_normal(n), 900) * exp_decay(n, 0.25) * 3
    return norm(sub + 0.5 * click + 0.6 * body)


def sub_drop(d=2.0):
    t = t_(d)
    return norm(np.sin(2 * np.pi * np.cumsum(90 * 2 ** (-2.2 * t)) / SR) * env_adsr(len(t), 0.003, d - 0.2, 0.0, 0.1))


def glitch(d=0.6, seed=6):
    r = rng(seed)
    out = np.zeros(int(d * SR))
    i = 0
    while i < len(out):
        seg = int(r.uniform(0.01, 0.06) * SR)
        kind = r.integers(4)
        tt = np.arange(seg) / SR
        if kind == 0:
            s = np.sign(np.sin(2 * np.pi * r.uniform(200, 2000) * tt))
        elif kind == 1:
            s = r.standard_normal(seg)
        elif kind == 2:
            s = np.round(np.sin(2 * np.pi * r.uniform(60, 400) * tt) * 3) / 3
        else:
            s = np.zeros(seg)
        out[i:i + seg] = s[:len(out) - i] * r.uniform(0.3, 1)
        i += seg
    return norm(out)


def pop(f0=900, d=0.12):
    t = t_(d)
    return norm(sine_sweep(f0, f0 * 0.35, d) * env_adsr(len(t), 0.001, d - 0.01, 0, 0.005))


def bubble(d=0.15):
    t = t_(d)
    return norm(sine_sweep(300, 1400, d) * np.sin(np.pi * t / d) ** 2)


def ding(f=1318.5, d=1.6):
    return norm(bell(f, d, tau=0.7))


def notify_two_tone(f1=880, f2=1318.5):
    return norm(place(0.9, (0, bell(f1, 0.6, tau=0.25)), (0.13, bell(f2, 0.75, tau=0.35))))


def success_chime():
    notes = [523.25, 659.25, 783.99, 1046.5]
    return norm(place(1.4, *[(0.09 * k, bell(f, 1.0, tau=0.35)) for k, f in enumerate(notes)]))


def error_buzz():
    t = t_(0.5)
    sq = np.sign(np.sin(2 * np.pi * 150 * t)) + 0.5 * np.sign(np.sin(2 * np.pi * 157 * t))
    gate = ((t % 0.25) < 0.18).astype(float)
    return norm(onepole_lp(sq * gate, 2500) * env_adsr(len(t), 0.005, 0.0, 1, 0.03, hold=0.45))


def phone_vibrate(pulses=2):
    on, off = 0.4, 0.25
    total = pulses * (on + off)
    t = t_(total)
    motor = np.sin(2 * np.pi * 165 * t) * (1 + 0.5 * np.sin(2 * np.pi * 23 * t))
    rattle = onepole_lp(rng(7).standard_normal(len(t)), 3000) * 0.25
    gate = ((t % (on + off)) < on).astype(float)
    gate = onepole_lp(gate, 60)
    return norm((motor + rattle) * gate)


def cash_register():
    """Synthetic 'ka-ching': drawer thunk + two bell strikes + coin jingle."""
    r = rng(8)
    thunk = onepole_lp(r.standard_normal(int(0.15 * SR)), 600) * exp_decay(int(0.15 * SR), 0.03) * 3
    b = bell(2093, 1.4, tau=0.6) + 0.6 * bell(2637, 1.4, tau=0.5)
    jingle = np.zeros(int(0.6 * SR))
    for k in range(9):
        s = int(r.uniform(0, 0.45) * SR)
        g = bell(r.uniform(3500, 6500), 0.12, tau=0.03)
        jingle[s:s + len(g)] += g[:len(jingle) - s] * 0.25
    return norm(place(1.7, (0, thunk), (0.06, b * 0.5), (0.1, jingle)))


def camera_shutter():
    r = rng(9)

    def clk(tau, fc):
        n = int(0.05 * SR)
        return bandpass(r.standard_normal(n), fc, q=3) * exp_decay(n, tau)
    return norm(place(0.25, (0, clk(0.004, 3500)), (0.012, clk(0.006, 1800) * 0.5), (0.11, clk(0.005, 2800) * 0.8)))


def tick_tock(n=4):
    r = rng(10)
    items = []
    for k in range(n):
        tt = int(0.03 * SR)
        s = bandpass(r.standard_normal(tt), 3200 if k % 2 == 0 else 2400, q=6) * exp_decay(tt, 0.005)
        items.append((k * 0.5, s))
    return norm(place(n * 0.5, *items))


def countdown_beeps():
    items = [(k, np.sin(2 * np.pi * 880 * t_(0.15)) * env_adsr(int(0.15 * SR), 0.003, 0.0, 1, 0.02, 0.13)) for k in range(3)]
    items.append((3, np.sin(2 * np.pi * 1760 * t_(0.6)) * env_adsr(int(0.6 * SR), 0.003, 0.0, 1, 0.1, 0.5)))
    return norm(place(3.7, *items))


def heartbeat(beats=2):
    def thump(f):
        n = int(0.18 * SR)
        return np.sin(2 * np.pi * np.cumsum(f * 2 ** (-2 * np.arange(n) / n)) / SR) * exp_decay(n, 0.05)
    items = []
    for k in range(beats):
        items += [(k * 0.85, thump(70)), (k * 0.85 + 0.22, thump(60) * 0.7)]
    return norm(place(beats * 0.85 + 0.2, *items))


def typing_burst(n=12, seed=11):
    r = rng(seed)
    items = []
    t0 = 0
    for _ in range(n):
        m = int(0.04 * SR)
        s = bandpass(r.standard_normal(m), r.uniform(2000, 4500), q=4) * exp_decay(m, 0.006)
        items.append((t0, s * r.uniform(0.5, 1)))
        t0 += r.uniform(0.06, 0.16)
    return norm(place(t0 + 0.1, *items))


# Game blips (generic chiptune; not copies of any game's sounds)
def square(f, d, duty=0.5):
    t = t_(d)
    return np.where((t * f) % 1 < duty, 1.0, -1.0)


def blip_coin():
    return norm(place(0.35, (0, square(988, 0.07) * 0.6), (0.07, square(1319, 0.25) * np.linspace(0.6, 0, int(0.25 * SR)))))


def blip_jump():
    t = t_(0.25)
    f = 300 * 2 ** (1.5 * t / 0.25)
    return norm(np.where((np.cumsum(f) / SR) % 1 < 0.5, 1.0, -1.0) * np.linspace(0.7, 0, len(t)))


def blip_powerup():
    notes = [523.25, 659.25, 783.99, 1046.5, 1318.5, 1568]
    return norm(place(0.65, *[(0.07 * k, square(f, 0.09, 0.25) * 0.5) for k, f in enumerate(notes)]))


def blip_levelup():
    notes = [392, 523.25, 659.25, 783.99, 1046.5]
    items = [(0.1 * k, square(f, 0.1, 0.5) * 0.45) for k, f in enumerate(notes)]
    items.append((0.5, square(1046.5, 0.5, 0.5) * np.linspace(0.45, 0, int(0.5 * SR))))
    return norm(place(1.05, *items))


def blip_hit():
    n = int(0.18 * SR)
    noise = np.sign(rng(12).standard_normal(n // 40).repeat(40))[:n]
    return norm(noise * np.linspace(1, 0, n) ** 2)


def blip_lose():
    notes = [523.25, 466.16, 415.3, 349.23]
    return norm(place(1.0, *[(0.18 * k, square(f, 0.2, 0.5) * 0.5) for k, f in enumerate(notes)]))


def blip_select():
    return norm(place(0.12, (0, square(1760, 0.04, 0.25) * 0.5), (0.05, square(2349, 0.06, 0.25) * 0.5)))


def block_place(seed=13):
    """Soft woody thunk for building/placing blocks (generic)."""
    n = int(0.22 * SR)
    r = rng(seed)
    body = bandpass(r.standard_normal(n), 420, q=2.5) * exp_decay(n, 0.04)
    knock = bandpass(r.standard_normal(n), 1800, q=4) * exp_decay(n, 0.008) * 0.5
    return norm(body + knock)


def block_break(seed=14):
    r = rng(seed)
    out = np.zeros(int(0.45 * SR))
    for k in range(6):
        m = int(0.08 * SR)
        g = bandpass(r.standard_normal(m), r.uniform(600, 2500), q=3) * exp_decay(m, 0.02)
        s = int(r.uniform(0, 0.3) * SR)
        out[s:s + m] += g * r.uniform(0.4, 1)
    return norm(out)


def explosion_8bit(seed=15):
    n = int(1.2 * SR)
    hold = np.linspace(20, 120, n).astype(int)
    r = rng(seed).standard_normal(n)
    y = np.empty(n)
    i = 0
    while i < n:
        h = hold[i]
        y[i:i + h] = np.sign(r[i])
        i += h
    return norm(y * exp_decay(n, 0.3))


def sparkle(seed=16):
    r = rng(seed)
    items = [(r.uniform(0, 0.6), bell(r.uniform(2500, 6000), 0.4, tau=0.08) * r.uniform(0.3, 1)) for _ in range(14)]
    return norm(place(1.0, *items))


def magic_shimmer(seed=17):
    r = rng(seed)
    items = [(0.05 * k, bell(f, 0.8, tau=0.25) * 0.6) for k, f in enumerate([1046.5, 1318.5, 1568, 2093, 2637, 3136])]
    return norm(place(1.3, *items) + 0.0 * r.standard_normal(1))


def static_noise(d=1.0):
    return norm(onepole_lp(rng(18).standard_normal(int(d * SR)), 6000) * env_adsr(int(d * SR), 0.01, 0, 1, 0.05, d - 0.06))


def tape_stop(d=1.0):
    t = t_(d)
    f = 220 * (1 - t / d) ** 2 + 5
    s = sum(np.sin(2 * np.pi * k * np.cumsum(f) / SR) / k for k in range(1, 6))
    return norm(onepole_lp(s, 4000 * (1 - t / d) + 200))


def record_scratch(seed=19):
    t = t_(0.35)
    f = 1200 * np.abs(np.sin(2 * np.pi * 2.5 * t)) + 150
    s = bandpass(rng(seed).standard_normal(len(t)), f, q=2) + 0.3 * np.sin(2 * np.pi * np.cumsum(f) / SR)
    return norm(s * np.sin(np.pi * t / 0.35))


EFFECTS = {
    "whoosh-up-0.6s": ("transition", "rising air whoosh, pans L->R", lambda: whoosh(0.6, True, 1)),
    "whoosh-down-0.6s": ("transition", "falling air whoosh, pans L->R", lambda: whoosh(0.6, False, 2)),
    "whoosh-fast-0.3s": ("transition", "quick whoosh for whip pans", lambda: whoosh(0.3, True, 3, 0.5)),
    "whoosh-long-1.2s": ("transition", "slow big whoosh", lambda: whoosh(1.2, True, 4, 0.6)),
    "whoosh-heavy-0.8s": ("transition", "darker whoosh (mono)", lambda: onepole_lp(whoosh(0.8, False, 5, 0.5, pan=False), 1500)),
    "swipe-short": ("transition", "phone-screen swipe", lambda: swipe(0.22, 6)),
    "swipe-long": ("transition", "longer swipe", lambda: swipe(0.4, 7)),
    "riser-2s": ("riser", "noise + tone riser, ends at peak", lambda: riser(2.0, 8)),
    "riser-4s": ("riser", "noise + tone riser, ends at peak", lambda: riser(4.0, 9)),
    "riser-8s": ("riser", "long build-up riser", lambda: riser(8.0, 10)),
    "downlifter-2s": ("riser", "falling sweep after a drop", lambda: downlifter(2.0, 11)),
    "impact-boom": ("impact", "cinematic boom: sub + body + click", lambda: impact(2.5, 12, 48)),
    "impact-punch": ("impact", "shorter tighter hit", lambda: impact(1.0, 13, 70)),
    "sub-drop": ("impact", "low sine drop (bass drop)", sub_drop),
    "glitch-short": ("glitch", "digital glitch 0.3 s", lambda: glitch(0.3, 14)),
    "glitch-medium": ("glitch", "digital glitch 0.6 s", lambda: glitch(0.6, 15)),
    "glitch-long": ("glitch", "digital glitch 1.2 s", lambda: glitch(1.2, 16)),
    "static-noise": ("glitch", "TV static 1 s", static_noise),
    "tape-stop": ("transition", "tape/record slowing to a stop", tape_stop),
    "record-scratch": ("transition", "synthetic record scratch", record_scratch),
    "pop-high": ("pop", "UI pop (pitch drop)", lambda: pop(1200, 0.1)),
    "pop-low": ("pop", "softer lower pop", lambda: pop(600, 0.14)),
    "bubble-pop": ("pop", "rising bubble blip", bubble),
    "ding": ("notification", "single bell ding", ding),
    "notification-two-tone": ("notification", "two-note message chime", notify_two_tone),
    "success-chime": ("notification", "4-note rising success", success_chime),
    "error-buzz": ("notification", "wrong-answer buzzer", error_buzz),
    "phone-vibrate": ("phone", "phone vibrating on a desk, 2 pulses", phone_vibrate),
    "cash-register": ("money", "synthetic ka-ching (drawer + bell + coins)", cash_register),
    "camera-shutter-synth": ("camera", "synthetic camera shutter click", camera_shutter),
    "clock-tick-tock": ("ui", "4 clock ticks, 0.5 s apart", tick_tock),
    "countdown-beeps": ("ui", "3 beeps (1 s apart) + long beep at 3 s", countdown_beeps),
    "heartbeat": ("impact", "2 heartbeats", heartbeat),
    "typing-synth": ("typing", "12 synthetic key clicks", typing_burst),
    "game-coin": ("game", "chiptune coin pickup", blip_coin),
    "game-jump": ("game", "chiptune jump", blip_jump),
    "game-powerup": ("game", "chiptune power-up arpeggio", blip_powerup),
    "game-levelup": ("game", "chiptune level-up fanfare", blip_levelup),
    "game-hit": ("game", "chiptune hit/damage noise", blip_hit),
    "game-lose": ("game", "chiptune lose jingle", blip_lose),
    "game-select": ("game", "chiptune menu select", blip_select),
    "game-explosion-8bit": ("game", "8-bit explosion", explosion_8bit),
    "block-place": ("game", "soft woody thunk (placing a block)", block_place),
    "block-break": ("game", "crumbly break (mining a block)", block_break),
    "sparkle": ("magic", "random high sparkles 1 s", sparkle),
    "magic-shimmer": ("magic", "rising bell shimmer", magic_shimmer),
}


def write_wav(path, x):
    x = np.asarray(x, float)
    if x.ndim == 1:
        x = x[:, None]
    pcm = (np.clip(x, -1, 1) * 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(pcm.shape[1])
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out", nargs="?")
    ap.add_argument("--only", default="")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    if a.list or not a.out:
        for k, (c, d, _) in EFFECTS.items():
            print(f"{k:24s} {c:12s} {d}")
        return
    os.makedirs(a.out, exist_ok=True)
    only = set(filter(None, a.only.split(",")))
    for k, (_, _, fn) in EFFECTS.items():
        if only and k not in only:
            continue
        write_wav(os.path.join(a.out, k + ".wav"), fn())
        print("wrote", k)


if __name__ == "__main__":
    sys.exit(main())
