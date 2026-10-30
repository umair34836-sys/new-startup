#!/home/user/tools/perc-venv/bin/python
# Pick the best thumbnail frames from a video: sharp, well exposed, a big face with a strong expression.
#
#   /home/user/tools/perc-venv/bin/python library/tools/thumb_frames.py video.mp4 outdir [--every 0.5] [--top 6]
#
# Samples a frame every --every s, scores it and writes the top N as PNG + outdir/frames.json + outdir/sheet.jpg.
# Score parts (each 0..1, printed so the choice can be explained in the edit log):
#   sharp   Laplacian variance relative to the sharpest sampled frame (blurry/motion frames lose)
#   expose  mean luma close to mid grey and few clipped pixels
#   face    largest face area (MediaPipe FaceLandmarker, Apache-2.0, /home/user/tools/perc-models/face_landmarker.task)
#   expr    strongest of smile / jaw open (surprise) / brows up from the model's blendshapes; eyes closed = penalty
# No face in the video -> ranks by sharp + expose only (use for gameplay / product shots).
# Thumbnail rules behind this (faces, emotion, sharpness): library/research/editing/skills2/16-thumbnails.md.
import argparse, json, os, subprocess
import numpy as np
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("video")
ap.add_argument("outdir")
ap.add_argument("--every", type=float, default=0.5)
ap.add_argument("--top", type=int, default=6)
ap.add_argument("--min-gap", type=float, default=2.0, help="seconds between picked frames (no near-duplicates)")
a = ap.parse_args()
os.makedirs(a.outdir, exist_ok=True)

probe = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                   "stream=width,height:format=duration", "-of", "json", a.video],
                                  capture_output=True, text=True, check=True).stdout)
W, H = probe["streams"][0]["width"], probe["streams"][0]["height"]
dur = float(probe["format"]["duration"])
sw = 640  # analyse small; save full-size frames for the picks
sh = int(round(H * sw / W / 2) * 2)
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", a.video, "-vf", f"fps=1/{a.every},scale={sw}:{sh}", "-f", "rawvideo",
                      "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
frames = np.frombuffer(raw, np.uint8).reshape(-1, sh, sw, 3)

import mediapipe as mp
from mediapipe.tasks.python import BaseOptions, vision
model = "/home/user/tools/perc-models/face_landmarker.task"
lm = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model), output_face_blendshapes=True, num_faces=3)) if os.path.exists(model) else None


def lap_var(g):
    k = g[1:-1, 1:-1] * -4 + g[:-2, 1:-1] + g[2:, 1:-1] + g[1:-1, :-2] + g[1:-1, 2:]
    return float(k.var())


rows = []
for i, f in enumerate(frames):
    g = f.mean(axis=2).astype(np.float32)
    clip = float(((g < 6) | (g > 250)).mean())
    row = {"t": round(i * a.every, 2), "sharp_raw": lap_var(g), "expose": max(0.0, 1 - abs(g.mean() - 120) / 120 - 2 * clip),
           "face": 0.0, "expr": 0.0, "faces": 0}
    if lm:
        res = lm.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(f)))
        row["faces"] = len(res.face_landmarks)
        best = 0
        for k, pts in enumerate(res.face_landmarks):
            xs, ys = [p.x for p in pts], [p.y for p in pts]
            area = float((max(xs) - min(xs)) * (max(ys) - min(ys)))
            if area > best:
                best = area
                bs = {c.category_name: c.score for c in res.face_blendshapes[k]}
                smile = float(bs.get("mouthSmileLeft", 0) + bs.get("mouthSmileRight", 0)) / 2
                surprise = float(max(bs.get("jawOpen", 0), bs.get("browInnerUp", 0)))
                blink = float(bs.get("eyeBlinkLeft", 0) + bs.get("eyeBlinkRight", 0)) / 2
                row["expr"] = round(max(smile, surprise) * (1 - max(0, blink - 0.4)), 3)
                row["smile"], row["surprise"], row["blink"] = round(smile, 3), round(surprise, 3), round(blink, 3)
        row["face"] = round(min(1.0, best / 0.12), 3)  # a face filling ~12% of the frame scores full
    rows.append(row)

top_sharp = max(r["sharp_raw"] for r in rows) or 1
has_face = any(r["faces"] for r in rows)
for r in rows:
    r["sharp"] = round(r["sharp_raw"] / top_sharp, 3)
    r["expose"] = round(r["expose"], 3)
    r["score"] = round((0.3 * r["sharp"] + 0.15 * r["expose"] + 0.25 * r["face"] + 0.3 * r["expr"]) if has_face
                       else (0.65 * r["sharp"] + 0.35 * r["expose"]), 3)

picks = []
for r in sorted(rows, key=lambda r: -r["score"]):
    if all(abs(r["t"] - p["t"]) >= a.min_gap for p in picks):
        picks.append(r)
    if len(picks) == a.top:
        break
for n, p in enumerate(picks, 1):
    p["file"] = os.path.join(a.outdir, f"pick{n:02d}_{p['t']:.2f}s.png")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(p["t"]), "-i", a.video, "-frames:v", "1", p["file"]], check=True)

thumbs = [Image.open(p["file"]).convert("RGB").resize((320, int(320 * H / W))) for p in picks]
if thumbs:
    sheet = Image.new("RGB", (330 * min(3, len(thumbs)), (thumbs[0].height + 10) * ((len(thumbs) + 2) // 3)), (30, 30, 30))
    for k, t in enumerate(thumbs):
        sheet.paste(t, (330 * (k % 3), (t.height + 10) * (k // 3)))
    sheet.save(os.path.join(a.outdir, "sheet.jpg"), quality=88)
json.dump({"video": a.video, "duration": dur, "every": a.every, "face_model": bool(lm), "picks": picks},
          open(os.path.join(a.outdir, "frames.json"), "w"), indent=1, default=float)
for p in picks:
    print(f"{p['t']:7.2f}s score {p['score']:.3f}  sharp {p['sharp']:.2f} expose {p['expose']:.2f} "
          f"face {p['face']:.2f} expr {p['expr']:.2f}  {p['file']}")
print(f"{len(rows)} frames scored ({'faces found' if has_face else 'no faces: sharp + exposure only'}); sheet: {a.outdir}/sheet.jpg")
