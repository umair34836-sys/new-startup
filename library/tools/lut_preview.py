#!/usr/bin/env python3
"""Contact sheet of .cube LUTs applied to one frame (ffmpeg lut3d), so looks can be compared by eye.

    python3 library/tools/lut_preview.py frame.jpg library/luts sheet.jpg [--width 480] [--cols 5]
    python3 library/tools/lut_preview.py frame.jpg library/luts out_dir --each   # one before/after JPG per LUT

The first tile is the untouched frame ("original").
"""
import argparse
import glob
import os
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFont

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def apply(frame, cube, width, out):
    vf = f"scale={width}:-2" + (f",lut3d=file='{cube}'" if cube else "")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", frame, "-vf", vf, "-q:v", "3", out], check=True)
    return Image.open(out).convert("RGB")


def label(im, text):
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(FONT, max(14, im.width // 26)) if os.path.exists(FONT) else ImageFont.load_default()
    d.rectangle([0, im.height - f.size - 10, im.width, im.height], fill=(0, 0, 0))
    d.text((6, im.height - f.size - 6), text, fill=(255, 255, 255), font=f)
    return im


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("frame")
    ap.add_argument("lut_dir")
    ap.add_argument("out")
    ap.add_argument("--width", type=int, default=480)
    ap.add_argument("--cols", type=int, default=5)
    ap.add_argument("--each", action="store_true")
    a = ap.parse_args()
    cubes = sorted(glob.glob(os.path.join(a.lut_dir, "*.cube")))
    with tempfile.TemporaryDirectory() as tmp:
        orig = label(apply(a.frame, None, a.width, os.path.join(tmp, "o.jpg")), "original")
        tiles = [orig]
        for c in cubes:
            name = os.path.basename(c)[:-5]
            im = label(apply(a.frame, c, a.width, os.path.join(tmp, name + ".jpg")), name)
            if a.each:
                os.makedirs(a.out, exist_ok=True)
                pair = Image.new("RGB", (orig.width * 2, orig.height))
                pair.paste(orig, (0, 0))
                pair.paste(im, (orig.width, 0))
                pair.save(os.path.join(a.out, name + ".jpg"), quality=85)
            tiles.append(im)
        if a.each:
            return
        w, h = tiles[0].size
        rows = (len(tiles) + a.cols - 1) // a.cols
        sheet = Image.new("RGB", (w * a.cols, h * rows))
        for i, t in enumerate(tiles):
            sheet.paste(t, ((i % a.cols) * w, (i // a.cols) * h))
        sheet.save(a.out, quality=85)


if __name__ == "__main__":
    main()
