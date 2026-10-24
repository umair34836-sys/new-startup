#!/usr/bin/env python3
"""Write our own 3D colour LUTs (.cube, 33^3) with numpy: no download, no credit needed (made by us).

    python3 library/tools/make_luts.py library/luts            # all looks
    python3 library/tools/make_luts.py out/ --only teal-orange-cinematic,bw-classic
    python3 library/tools/make_luts.py --list

Every look is a short recipe of the operations below, applied to an identity grid in display (sRGB) space.
Apply a .cube with ffmpeg: -vf "lut3d=file=library/luts/<id>.cube" (blend with the original for strength).
Never cat a .cube into an AI context: it is ~36k lines of numbers.
"""
import argparse
import os
import sys

import numpy as np

SIZE = 33
LUMA = np.array([0.2126, 0.7152, 0.0722])


def luma(x):
    return (x * LUMA).sum(-1, keepdims=True)


def smoothstep(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


# ---- operations (x: N x 3 floats in 0..1) -------------------------------------------------------
def contrast(x, k):
    """k>0: S-curve (k=0.5 = full smoothstep, keeps 0 and 1); k<0: linear flatten around 0.5."""
    if k < 0:
        return np.clip(0.5 + (x - 0.5) * (1 + k), 0, 1)
    return np.clip(mix(x, x * x * (3 - 2 * x), min(k * 2, 1.0)), 0, 1)


def saturation(x, s):
    l = luma(x)
    return np.clip(l + (x - l) * s, 0, 1)


def vibrance(x, v):
    """Boost low-saturation colours more than saturated ones."""
    mx, mn = x.max(-1, keepdims=True), x.min(-1, keepdims=True)
    sat = mx - mn
    return saturation_per(x, 1 + v * (1 - sat))


def saturation_per(x, s):
    l = luma(x)
    return np.clip(l + (x - l) * s, 0, 1)


def white_balance(x, temp=0.0, tint=0.0):
    """temp>0 warmer (more red, less blue); tint>0 more magenta."""
    g = np.array([1 + 0.12 * temp + 0.04 * tint, 1 - 0.08 * tint, 1 - 0.14 * temp + 0.04 * tint])
    return np.clip(x * g, 0, 1)


def lift_gamma_gain(x, lift=(0, 0, 0), gamma=(1, 1, 1), gain=(1, 1, 1)):
    lift, gamma, gain = map(np.array, (lift, gamma, gain))
    y = x * gain + lift * (1 - x)
    return np.clip(np.clip(y, 0, 1) ** (1 / gamma), 0, 1)


def split_tone(x, shadows, highlights, amount=1.0, balance=0.5):
    l = luma(x)
    wh = smoothstep(balance - 0.35, balance + 0.35, l)
    tint = (1 - wh) * np.array(shadows) + wh * np.array(highlights)
    return np.clip(x + tint * amount, 0, 1)


def fade(x, black=0.06, white=0.97):
    return black + x * (white - black)


def exposure(x, stops):
    return np.clip(x * 2 ** stops, 0, 1)


def soft_highlights(x, k=0.3):
    """Roll off highlights (filmic shoulder)."""
    return np.where(x > 0.7, 0.7 + (x - 0.7) * (1 - k), x)


def hue_shift_skin_teal(x, amount=0.5):
    """Teal-orange: warm tones (skin) pushed to orange, everything else nudged to teal."""
    r, g, b = x[..., 0:1], x[..., 1:2], x[..., 2:3]
    warmness = np.clip((r - b) * 2.0, 0, 1)  # skin/oranges have r>b
    orange = np.array([0.05, 0.0, -0.06])
    teal = np.array([-0.05, 0.015, 0.06])
    return np.clip(x + amount * (warmness * orange + (1 - warmness) * teal * (1 - luma(x) * 0.5)), 0, 1)


def bw(x, mix=(0.30, 0.59, 0.11)):
    l = (x * np.array(mix)).sum(-1, keepdims=True)
    return np.repeat(np.clip(l, 0, 1), 3, -1)


def tone_tint(x, color, amount):
    """Multiply-tint toward a colour, weighted to midtones (sepia, cyanotype)."""
    l = luma(x)
    mid = 4 * l * (1 - l)
    return np.clip(x * (1 - amount * mid) + np.array(color) * l * amount * mid * 1.6, 0, 1)


def channel_curve(x, ch, pts):
    xs, ys = zip(*pts)
    y = x.copy()
    y[..., ch] = np.interp(x[..., ch], xs, ys)
    return y


def green_shift(x, amt):
    return np.clip(x + np.array([-0.3, 0.6, -0.3]) * amt * (1 - luma(x)), 0, 1)


def mix(a, b, t):
    return a * (1 - t) + b * t


# ---- looks -----------------------------------------------------------------------------------------
def L(*ops):
    def f(x):
        for op in ops:
            x = op(x)
        return x
    return f


LOOKS = {
    "teal-orange-cinematic": ("Blockbuster teal shadows + orange skin, strong contrast", L(
        lambda x: hue_shift_skin_teal(x, 0.9), lambda x: split_tone(x, [-0.03, 0.02, 0.06], [0.06, 0.02, -0.04], 0.9),
        lambda x: contrast(x, 0.22), lambda x: saturation(x, 1.08))),
    "teal-orange-soft": ("Gentle teal-orange for vlogs/people, skin stays natural", L(
        lambda x: hue_shift_skin_teal(x, 0.45), lambda x: contrast(x, 0.1), lambda x: soft_highlights(x, 0.25))),
    "warm-skin-glow": ("Warm flattering skin, soft highlights, lifted shadows (portraits, interviews)", L(
        lambda x: white_balance(x, 0.35, 0.05), lambda x: lift_gamma_gain(x, (0.02, 0.015, 0.01), (1.06, 1.04, 1.0)),
        lambda x: soft_highlights(x, 0.35), lambda x: vibrance(x, 0.12))),
    "golden-hour": ("Strong sunset gold, orange highlights, warm shadows", L(
        lambda x: white_balance(x, 0.7, 0.08), lambda x: split_tone(x, [0.03, 0.01, -0.02], [0.08, 0.04, -0.06]),
        lambda x: contrast(x, 0.12), lambda x: saturation(x, 1.12))),
    "moody-desaturated": ("Muted colours, deep blacks, cool shadows (drama, serious ads)", L(
        lambda x: saturation(x, 0.6), lambda x: split_tone(x, [-0.02, 0.0, 0.03], [0.02, 0.01, 0.0]),
        lambda x: contrast(x, 0.25), lambda x: lift_gamma_gain(x, (0, 0, 0), (0.95, 0.95, 0.97)))),
    "moody-green": ("Desaturated with green-cyan shadows (thriller)", L(
        lambda x: saturation(x, 0.7), lambda x: split_tone(x, [-0.03, 0.03, 0.01], [0.02, 0.02, -0.02]),
        lambda x: contrast(x, 0.2))),
    "cold-blue-night": ("Blue night look, cool highlights, dark", L(
        lambda x: white_balance(x, -0.6, 0.0), lambda x: exposure(x, -0.35), lambda x: saturation(x, 0.8),
        lambda x: contrast(x, 0.15))),
    "neon-night-city": ("Night city: magenta highlights, cyan shadows, punchy", L(
        lambda x: split_tone(x, [-0.04, 0.03, 0.07], [0.06, -0.02, 0.05]), lambda x: contrast(x, 0.25),
        lambda x: saturation(x, 1.3))),
    "day-for-night": ("Turns daylight footage into fake night (blue, dark, low saturation)", L(
        lambda x: exposure(x, -1.1), lambda x: white_balance(x, -0.9, 0.05), lambda x: saturation(x, 0.55),
        lambda x: contrast(x, 0.1))),
    "bw-classic": ("Neutral black and white", L(lambda x: bw(x), lambda x: contrast(x, 0.12))),
    "bw-high-contrast": ("Hard black and white, red filter look (dark skies)", L(
        lambda x: bw(x, (0.55, 0.40, 0.05)), lambda x: contrast(x, 0.45))),
    "bw-soft-matte": ("Soft faded black and white (memories, tributes)", L(
        lambda x: bw(x), lambda x: fade(x, 0.08, 0.93), lambda x: contrast(x, -0.05))),
    "sepia": ("Old-photo sepia", L(lambda x: bw(x), lambda x: tone_tint(x, [1.0, 0.78, 0.55], 0.55),
                                   lambda x: fade(x, 0.04, 0.96))),
    "vintage-70s": ("Warm faded 70s film, yellow-green mids, lifted blacks", L(
        lambda x: white_balance(x, 0.4, -0.15), lambda x: fade(x, 0.07, 0.94),
        lambda x: split_tone(x, [0.02, 0.03, -0.01], [0.04, 0.03, -0.05]), lambda x: saturation(x, 0.85))),
    "vintage-matte": ("Instagram matte: faded blacks, soft contrast", L(
        lambda x: fade(x, 0.1, 0.95), lambda x: saturation(x, 0.9), lambda x: split_tone(x, [0.0, 0.01, 0.03], [0.03, 0.01, -0.01]))),
    "film-warm-print": ("Warm print-film style: rich reds, soft shoulder (our own approximation, no brand emulation)", L(
        lambda x: channel_curve(x, 0, [(0, 0.02), (0.5, 0.53), (1, 0.98)]), lambda x: channel_curve(x, 2, [(0, 0.04), (0.5, 0.47), (1, 0.93)]),
        lambda x: soft_highlights(x, 0.4), lambda x: contrast(x, 0.12), lambda x: saturation(x, 1.05))),
    "film-cool-print": ("Cool print-film style: green-cyan shadows, clean highlights (our own approximation)", L(
        lambda x: channel_curve(x, 1, [(0, 0.03), (0.5, 0.51), (1, 0.98)]), lambda x: channel_curve(x, 2, [(0, 0.05), (0.5, 0.5), (1, 0.96)]),
        lambda x: soft_highlights(x, 0.3), lambda x: contrast(x, 0.1), lambda x: saturation(x, 0.92))),
    "bleach-bypass": ("Silvery high contrast, low saturation (war, action, grit)", L(
        lambda x: mix(x, bw(x), 0.55), lambda x: contrast(x, 0.4))),
    "cross-process": ("Cross-processed: yellow highlights, blue shadows, strong", L(
        lambda x: channel_curve(x, 0, [(0, 0), (0.25, 0.2), (0.75, 0.82), (1, 1)]),
        lambda x: channel_curve(x, 1, [(0, 0), (0.25, 0.22), (0.75, 0.82), (1, 1)]),
        lambda x: channel_curve(x, 2, [(0, 0.12), (1, 0.82)]), lambda x: saturation(x, 1.1))),
    "wedding-pastel": ("Soft pastel wedding: lifted blacks, pink-peach highlights, low contrast", L(
        lambda x: fade(x, 0.06, 0.98), lambda x: split_tone(x, [0.01, 0.0, 0.02], [0.04, 0.01, 0.02]),
        lambda x: saturation(x, 0.85), lambda x: exposure(x, 0.12), lambda x: soft_highlights(x, 0.3))),
    "wedding-bright-airy": ("Bright airy wedding/event: +exposure, clean whites, gentle warmth", L(
        lambda x: exposure(x, 0.25), lambda x: white_balance(x, 0.12, 0.03), lambda x: soft_highlights(x, 0.45),
        lambda x: contrast(x, -0.05), lambda x: vibrance(x, 0.1))),
    "wedding-royal-gold": ("Rich desi wedding: deep reds and golds, warm contrast", L(
        lambda x: white_balance(x, 0.3, 0.06), lambda x: split_tone(x, [0.02, 0.0, -0.01], [0.06, 0.035, -0.04]),
        lambda x: contrast(x, 0.18), lambda x: saturation(x, 1.2))),
    "pak-reel-punchy": ("Punchy social reel: strong contrast and colour, slight warmth (shops, food, bikes)", L(
        lambda x: contrast(x, 0.3), lambda x: saturation(x, 1.3), lambda x: white_balance(x, 0.1, 0.0), lambda x: vibrance(x, 0.15))),
    "pak-reel-clean": ("Clean bright reel for products/offices: lifted mids, neutral, crisp", L(
        lambda x: lift_gamma_gain(x, (0, 0, 0), (1.12, 1.12, 1.12)), lambda x: contrast(x, 0.15), lambda x: vibrance(x, 0.2))),
    "food-vivid": ("Food: warm, saturated reds/oranges, appetising", L(
        lambda x: white_balance(x, 0.25, 0.04), lambda x: saturation(x, 1.35), lambda x: contrast(x, 0.15))),
    "summer-vibrant": ("Bright summer: blue skies, green grass, high saturation", L(
        lambda x: exposure(x, 0.1), lambda x: vibrance(x, 0.4), lambda x: saturation(x, 1.15), lambda x: contrast(x, 0.12))),
    "autumn-orange": ("Greens turn olive/orange, warm overall", L(
        lambda x: channel_curve(x, 1, [(0, 0), (0.5, 0.46), (1, 0.95)]), lambda x: white_balance(x, 0.45, -0.02),
        lambda x: saturation(x, 1.1))),
    "cyberpunk": ("Magenta-teal gamer look, crushed blacks", L(
        lambda x: split_tone(x, [0.0, 0.05, 0.09], [0.1, -0.03, 0.08]), lambda x: contrast(x, 0.3),
        lambda x: saturation(x, 1.35))),
    "gaming-saturated": ("Minecraft / gaming promo: very saturated, bright, crisp", L(
        lambda x: saturation(x, 1.5), lambda x: contrast(x, 0.22), lambda x: exposure(x, 0.08))),
    "horror-green": ("Sickly green desaturated horror", L(
        lambda x: saturation(x, 0.45), lambda x: green_shift(x, 0.12), lambda x: contrast(x, 0.3), lambda x: exposure(x, -0.2))),
    "dreamy-soft": ("Dreamy: lifted, low contrast, warm-pink, slight haze", L(
        lambda x: fade(x, 0.09, 1.0), lambda x: white_balance(x, 0.15, 0.12), lambda x: saturation(x, 0.9),
        lambda x: soft_highlights(x, 0.5))),
    "documentary-natural": ("Subtle: a touch of contrast and vibrance, keeps colours true", L(
        lambda x: contrast(x, 0.08), lambda x: vibrance(x, 0.12))),
}


def identity(n=SIZE):
    r = np.linspace(0, 1, n)
    # .cube order: red changes fastest, then green, then blue
    b, g, rr = np.meshgrid(r, r, r, indexing="ij")
    return np.stack([rr, g, b], -1).reshape(-1, 3)


def write_cube(path, title, fn, n=SIZE):
    x = identity(n)
    y = np.clip(fn(x.copy()), 0, 1)
    with open(path, "w") as f:
        f.write(f'TITLE "{title}"\n# Made with library/tools/make_luts.py (own work, no credit needed)\n')
        f.write(f"LUT_3D_SIZE {n}\nDOMAIN_MIN 0.0 0.0 0.0\nDOMAIN_MAX 1.0 1.0 1.0\n")
        np.savetxt(f, y, fmt="%.6f")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out", nargs="?")
    ap.add_argument("--only", default="")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    if a.list or not a.out:
        for k, (d, _) in LOOKS.items():
            print(f"{k:24s} {d}")
        return
    os.makedirs(a.out, exist_ok=True)
    only = set(filter(None, a.only.split(",")))
    for k, (d, fn) in LOOKS.items():
        if only and k not in only:
            continue
        write_cube(os.path.join(a.out, k + ".cube"), k, fn)
        print("wrote", k)


if __name__ == "__main__":
    sys.exit(main())
