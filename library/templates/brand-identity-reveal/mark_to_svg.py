#!/home/user/tools/perc-venv/bin/python
# Trace a flat logo mark (PNG with alpha, or light mark on dark) into straight-edge polygons for the "logo construction"
# shot: writes mark.json = {w, h, polys: [[[x,y],...],...], angles: [deg of each long edge from vertical]} in the PNG's
# pixel space. Uses OpenCV contours + approxPolyDP, so it only fits marks made of straight edges (check the overlay PNG).
# usage: mark_to_svg.py mark.png out.json [--eps 0.004] [--overlay check.png]
import argparse, json, math
import cv2, numpy as np
ap = argparse.ArgumentParser(); ap.add_argument("png"); ap.add_argument("out")
ap.add_argument("--eps", type=float, default=0.004, help="approxPolyDP epsilon as a fraction of the contour length")
ap.add_argument("--overlay"); a = ap.parse_args()
im = cv2.imread(a.png, cv2.IMREAD_UNCHANGED)
if im.shape[2] == 4 and im[:, :, 3].min() < 250:
    m = im[:, :, 3]
else:
    m = cv2.cvtColor(im[:, :, :3], cv2.COLOR_BGR2GRAY)
_, m = cv2.threshold(m, 127, 255, cv2.THRESH_BINARY)
cs, hier = cv2.findContours(m, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
polys, angles = [], []
for c in cs:
    if cv2.contourArea(c) < 0.002 * m.size:
        continue
    p = cv2.approxPolyDP(c, a.eps * cv2.arcLength(c, True), True)[:, 0, :]
    polys.append(p.tolist())
    for i in range(len(p)):
        x0, y0 = p[i]; x1, y1 = p[(i + 1) % len(p)]
        L = math.hypot(x1 - x0, y1 - y0)
        if L > 0.15 * m.shape[0]:  # long edges only
            angles.append(round(math.degrees(math.atan2(abs(x1 - x0), abs(y1 - y0))), 1))
json.dump({"w": m.shape[1], "h": m.shape[0], "polys": polys, "angles": sorted(set(angles))}, open(a.out, "w"))
print(f"{len(polys)} polygons, vertices {[len(p) for p in polys]}, long-edge angles from vertical {sorted(set(angles))}")
if a.overlay:
    o = cv2.cvtColor(m, cv2.COLOR_GRAY2BGR) // 3
    for p in polys:
        cv2.polylines(o, [np.array(p, np.int32)], True, (0, 0, 255), 2)
        for x, y in p:
            cv2.circle(o, (int(x), int(y)), 5, (0, 255, 0), -1)
    cv2.imwrite(a.overlay, o)
