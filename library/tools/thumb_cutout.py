#!/home/user/tools/venv/bin/python
# Cut a person (or any subject) out of a frame for a thumbnail: transparent PNG trimmed to the subject.
#
#   /home/user/tools/venv/bin/python library/tools/thumb_cutout.py frame.png cutout.png [--model u2net_human_seg|isnet-general-use|u2net]
#
# rembg 2.x (MIT) in /home/user/tools/venv. u2net_human_seg is the person model that worked on this box (the default
# BRIA model OOM-killed at 14 GB, CLAUDE.md "Realistic 3D model" note); use isnet-general-use for objects/logos.
# Alpha is cleaned (small specks removed, edge softened 1 px) and the image is cropped to the subject + margin.
import argparse
import numpy as np
from PIL import Image, ImageFilter
from rembg import new_session, remove

ap = argparse.ArgumentParser()
ap.add_argument("src")
ap.add_argument("out")
ap.add_argument("--model", default="u2net_human_seg")
ap.add_argument("--margin", type=int, default=12, help="px kept around the subject")
a = ap.parse_args()

im = Image.open(a.src).convert("RGB")
cut = remove(im, session=new_session(a.model))
alpha = np.array(cut.split()[-1])
alpha[alpha < 24] = 0  # drop faint specks the model leaves in the background
import cv2  # keep only blobs >= 3% of the biggest one (a stray shoe/hand fragment showed up as a white island in a test)
n, lab, stats, _ = cv2.connectedComponentsWithStats((alpha > 127).astype(np.uint8), 8)
if n > 2:
    big = stats[1:, cv2.CC_STAT_AREA].max()
    keep = np.isin(lab, [i for i in range(1, n) if stats[i, cv2.CC_STAT_AREA] >= 0.03 * big])
    alpha[~keep & (alpha > 0)] = 0
cut.putalpha(Image.fromarray(alpha).filter(ImageFilter.GaussianBlur(0.8)))
ys, xs = np.nonzero(alpha)
if len(xs) == 0:
    raise SystemExit("no subject found")
m = a.margin
box = (max(0, xs.min() - m), max(0, ys.min() - m), min(im.width, xs.max() + m), min(im.height, ys.max() + m))
cut.crop(box).save(a.out)
print(f"wrote {a.out} {box[2] - box[0]}x{box[3] - box[1]} (subject {100 * (alpha > 127).mean():.1f}% of the frame, model {a.model})")
