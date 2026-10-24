#!/usr/bin/env python3
"""Logo image -> brand palette + readable text colours (WCAG 2.1 contrast).

  python3 brand_from_logo.py logo.png                 # print palette and suggestions
  python3 brand_from_logo.py logo.png --write brand.json   # also fill brand.json "colors" (other keys kept)

k-means (numpy, seeded, k=5) on the logo's opaque, non-near-white/near-black pixels finds the main colours,
sorted by pixel share. For each colour it picks the text colour (white, black, or the darkest/lightest
palette colour) with the highest contrast ratio and reports whether it passes 4.5:1 (normal text) and
3:1 (large text). Contrast formula: WCAG 2.1 relative luminance + (L1 + 0.05) / (L2 + 0.05)
(https://www.w3.org/TR/WCAG21/#dfn-contrast-ratio).
"""
import json
import sys

import numpy as np
from PIL import Image


def lin(c):
    c = c / 255.0
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def luminance(rgb):
    r, g, b = lin(np.asarray(rgb, dtype=float))
    return float(0.2126 * r + 0.7152 * g + 0.0722 * b)


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def hexc(rgb):
    return "#%02x%02x%02x" % tuple(int(round(v)) for v in rgb)


def kmeans(px, k=5, iters=25, seed=7):
    rng = np.random.default_rng(seed)
    k = min(k, len(px))
    cent = px[rng.choice(len(px), k, replace=False)].astype(float)
    for _ in range(iters):
        lab = np.argmin(((px[:, None, :] - cent[None]) ** 2).sum(-1), 1)
        new = np.array([px[lab == i].mean(0) if (lab == i).any() else cent[i] for i in range(k)])
        if np.allclose(new, cent, atol=0.5):
            break
        cent = new
    share = np.bincount(lab, minlength=k) / len(lab)
    return cent, share


def palette(path, k=5):
    im = Image.open(path).convert("RGBA")
    im.thumbnail((256, 256))
    a = np.asarray(im).reshape(-1, 4).astype(float)
    a = a[a[:, 3] > 200][:, :3]
    mx, mn = a.max(1), a.min(1)
    keep = ~((mn > 240) | (mx < 15))          # drop paper-white and pure-black backgrounds
    px = a[keep] if keep.sum() > 50 else a
    cent, share = kmeans(px, k)
    order = np.argsort(-share)
    out = []
    for i in order:
        if share[i] < 0.02:
            continue
        c = cent[i]
        if any(np.abs(c - np.array(o["rgb"])).sum() < 30 for o in out):
            continue                           # merge near-duplicates
        out.append({"hex": hexc(c), "rgb": [float(v) for v in c], "share": round(float(share[i]), 3)})
    return out


def best_text(bg, pal):
    cands = {"#ffffff": (255, 255, 255), "#000000": (0, 0, 0)}
    for p in pal:
        cands[p["hex"]] = p["rgb"]
    best = max(cands.items(), key=lambda kv: contrast(bg, kv[1]))
    return best[0], round(contrast(bg, best[1]), 2)


def main():
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    pal = palette(a[0])
    for p in pal:
        t, r = best_text(p["rgb"], pal)
        p["text"], p["ratio"] = t, r
        print("%s  share %5.1f%%  text %s  contrast %.2f  normal %s  large %s"
              % (p["hex"], p["share"] * 100, t, r, "PASS" if r >= 4.5 else "fail", "PASS" if r >= 3 else "fail"))
    if "--write" in a:
        f = a[a.index("--write") + 1]
        try:
            brand = json.load(open(f, encoding="utf-8"))
        except FileNotFoundError:
            brand = {"name": ""}
        lum = sorted(pal, key=lambda p: luminance(p["rgb"]))
        prim = pal[0]
        sec = pal[1] if len(pal) > 1 else pal[0]
        dark = lum[0]["hex"] if luminance(lum[0]["rgb"]) < 0.05 else "#0b0d10"
        brand["colors"] = {"primary": prim["hex"], "on_primary": prim["text"], "secondary": sec["hex"],
                           "on_secondary": sec["text"], "accent": sec["hex"], "dark": dark}
        json.dump(brand, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print("wrote colors to", f)


if __name__ == "__main__":
    main()
