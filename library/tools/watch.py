#!/home/user/tools/perc-venv/bin/python
# Usage: /home/user/tools/perc-venv/bin/python library/tools/watch.py VIDEO [--json] [--out report.json] [--sheet sheet.png]
#        /home/user/tools/perc-venv/bin/python library/tools/watch.py compare A B [--at 1.0,3.5] [--out cmp.png] [--labels before,after]
# Turns a video into facts Claude can reason about, because Claude can't watch at full speed:
#   real fps from frame timestamps (VFR / dropped / duplicated frames), shot cuts (PySceneDetect content + adaptive),
#   motion energy per second, camera shake (phase-correlation path minus its smooth path), sharpness (Laplacian
#   variance), exposure (mean luma, clipped highlights, crushed shadows) and colour cast (Lab a*/b*) per scene,
#   faces and people per scene (MediaPipe BlazeFace short-range + EfficientDet-Lite0 "person"), flicker
#   (frame-to-frame luma oscillation), black and frozen stretches, and a labelled contact sheet of key frames.
# compare: before/after frames side by side (videos or images) with luma/sharpness/colour numbers, for approvals.
# Setup: bash library/tools/setup-specialist-a.sh   (venv /home/user/tools/perc-venv, models /home/user/tools/perc-models)
# Accuracy notes and limits: library/research/perception-tools.md
import argparse, json, os, subprocess, sys
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

MODELS = "/home/user/tools/perc-models"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def r(x, n=2):
    return None if x is None else float(round(float(x), n))


def font(sz):
    try:
        return ImageFont.truetype(FONT, sz)
    except Exception:
        return ImageFont.load_default()


def probe(path):
    j = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                   "stream=width,height,r_frame_rate,avg_frame_rate,nb_frames,codec_name:stream_side_data=rotation:format=duration",
                                   "-of", "json", path], capture_output=True, text=True, check=True).stdout)
    st = j["streams"][0]
    rot = 0
    for sd in st.get("side_data_list", []) or []:
        if "rotation" in sd:
            rot = int(sd["rotation"])
    return st, float(j["format"].get("duration", 0)), rot


def frame_times(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "frame=pts_time",
                          "-of", "csv=p=0", path], capture_output=True, text=True, check=True).stdout
    return np.array([float(x.split(",")[0]) for x in out.split() if x.strip() and x.split(",")[0] not in ("", "N/A")])


def frames(path, w):
    """Yield every decoded frame as RGB uint8 at width w (height keeps aspect, even)."""
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", path, "-an", "-vf", f"scale={w}:-2", "-vsync", "passthrough",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    hh = probe_scaled_height(path, w)  # after autorotation, so a rotated phone clip gets the right height
    n = w * hh * 3
    while True:
        b = p.stdout.read(n)
        if len(b) < n:
            break
        yield np.frombuffer(b, np.uint8).reshape(hh, w, 3)
    p.wait()


def probe_scaled_height(path, w):
    out = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-frames:v", "1", "-vf", f"scale={w}:-2", "-f", "rawvideo",
                          "-pix_fmt", "gray", "-"], capture_output=True).stdout
    return len(out) // w


def grab(path, t, w=None):
    """One frame at time t (s) as RGB array; images are loaded directly."""
    if path.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".bmp")):
        im = Image.open(path).convert("RGB")
    else:
        out = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", path, "-frames:v", "1", "-f", "image2pipe",
                              "-vcodec", "png", "-"], capture_output=True).stdout
        if not out:
            raise SystemExit(f"no frame at {t}s in {path}")
        import io
        im = Image.open(io.BytesIO(out)).convert("RGB")
    if w:
        im = im.resize((w, int(round(im.height * w / im.width))), Image.LANCZOS)
    return np.asarray(im)


def frame_stats(rgb):
    g = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB).astype(np.float32)
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    A, B, L = lab[..., 1] - 128, lab[..., 2] - 128, lab[..., 0]
    # colour cast is read from near-neutral pixels (low chroma, mid lightness): what should be grey/white
    neutral = (np.hypot(A, B) < 14) & (L > 50) & (L < 235)
    if neutral.mean() >= 0.02:
        ca, cb, src = float(A[neutral].mean()), float(B[neutral].mean()), 1.0
    else:
        ca, cb, src = float(A.mean()), float(B.mean()), 0.0
    return {"cast_a": ca, "cast_b": cb, "cast_from_neutrals": src,
        "luma": float(g.mean()), "luma_std": float(g.std()),
        "clip_hi": float((g >= 250).mean()), "crush_lo": float((g <= 5).mean()),
        "a": float(lab[..., 1].mean() - 128), "b": float(lab[..., 2].mean() - 128),
        "sat": float(hsv[..., 1].mean()),
        "sharp": float(cv2.Laplacian(g, cv2.CV_64F).var()),
    }


def cast_name(a_, b_):
    if abs(a_) < 3 and abs(b_) < 3:
        return "neutral"
    parts = []
    if b_ >= 3:
        parts.append("warm/yellow")
    if b_ <= -3:
        parts.append("cool/blue")
    if a_ >= 3:
        parts.append("magenta")
    if a_ <= -3:
        parts.append("green")
    return "+".join(parts)


def exposure_name(luma, hi, lo):
    s = "dark" if luma < 70 else ("bright" if luma > 180 else "normal")
    if hi > 0.05:
        s += ", highlights clipped"
    if lo > 0.10:
        s += ", shadows crushed"
    return s


# ---------------- detectors (MediaPipe Tasks) ----------------
class Detectors:
    def __init__(self):
        self.face = self.obj = None
        try:
            import mediapipe as mp
            from mediapipe.tasks.python import vision, BaseOptions
            self.mp = mp
            self.face = vision.FaceDetector.create_from_options(vision.FaceDetectorOptions(
                base_options=BaseOptions(model_asset_path=os.path.join(MODELS, "blaze_face_short_range.tflite")),
                min_detection_confidence=0.5))
            self.obj = vision.ObjectDetector.create_from_options(vision.ObjectDetectorOptions(
                base_options=BaseOptions(model_asset_path=os.path.join(MODELS, "efficientdet_lite0.tflite")),
                score_threshold=0.4, category_allowlist=["person"], max_results=20))
        except Exception as e:
            self.err = str(e)[:200]

    def count(self, rgb):
        if not self.face:
            return None, None
        im = self.mp.Image(image_format=self.mp.ImageFormat.SRGB, data=np.ascontiguousarray(rgb))
        f = len(self.face.detect(im).detections)
        p = len(self.obj.detect(im).detections)
        return f, p


# ---------------- analyse ----------------
def analyse(a):
    st, dur, rot = probe(a.inp)
    rep = {"file": os.path.abspath(a.inp), "codec": st.get("codec_name"), "width": int(st["width"]),
           "height": int(st["height"]), "rotation": rot, "duration_s": r(dur, 3),
           "r_frame_rate_header": st.get("r_frame_rate"), "avg_frame_rate_header": st.get("avg_frame_rate")}
    # real fps from presentation timestamps
    ts = np.sort(frame_times(a.inp))
    dts = np.diff(ts) if len(ts) > 1 else np.array([0.04])
    med = float(np.median(dts)) if len(dts) else 0.04
    rep["timing"] = {
        "frames": int(len(ts)), "real_fps_median": r(1 / med, 3) if med > 0 else None,
        "real_fps_mean": r((len(ts) - 1) / (ts[-1] - ts[0]), 3) if len(ts) > 2 and ts[-1] > ts[0] else None,
        "frame_interval_ms_p5_p50_p95": [r(np.percentile(dts, q) * 1000, 2) for q in (5, 50, 95)],
        "gaps_over_1_5x": int((dts > 1.5 * med).sum()),
        "vfr": bool(np.percentile(dts, 95) > 1.2 * np.percentile(dts, 5)),
        "note": "trust real_fps over the header rate (CLAUDE.md: a WhatsApp clip said 28.4 fps but carried ~12)",
    }
    # shot cuts with PySceneDetect
    cuts = {}
    try:
        from scenedetect import detect, ContentDetector, AdaptiveDetector
        for name, det in (("content", ContentDetector(threshold=27.0)), ("adaptive", AdaptiveDetector())):
            sl = detect(a.inp, det)
            cuts[name] = [r(s[0].seconds, 3) for s in sl[1:]]
    except Exception as e:
        cuts["error"] = str(e)[:200]
    # per-frame pass at analysis width
    W = a.width
    det = Detectors()
    prev_g = None
    per = []  # t, luma, diff, dx, dy, sharp, stats subset
    win = None
    k = 0
    for fr in frames(a.inp, W):
        t = float(ts[k]) if k < len(ts) else (k / (1 / med))
        k += 1
        g = cv2.cvtColor(fr, cv2.COLOR_RGB2GRAY).astype(np.float32)
        if win is None:
            win = cv2.createHanningWindow((g.shape[1], g.shape[0]), cv2.CV_32F)
        s = frame_stats(fr)
        if prev_g is None:
            diff, dx, dy = 0.0, 0.0, 0.0
        else:
            diff = float(np.abs(g - prev_g).mean())
            (dx, dy), _ = cv2.phaseCorrelate(prev_g, g, win)
            if g.std() < 8 or prev_g.std() < 8:  # black/flat frames: the shift estimate is noise
                dx, dy = 0.0, 0.0
        per.append([t, s["luma"], diff, dx, dy, s["sharp"], s["clip_hi"], s["crush_lo"], s["cast_a"], s["cast_b"], s["sat"], s["luma_std"],
                    s["cast_from_neutrals"], s["a"], s["b"]])
        prev_g = g
    P = np.array(per)
    if len(P) < 2:
        sys.exit("could not decode frames")
    t, luma, diff, dx, dy, sharp = P[:, 0], P[:, 1], P[:, 2], P[:, 3], P[:, 4], P[:, 5]
    fps = 1 / med
    # scene list: union of content cuts (primary) ; adaptive kept for reference
    cut_list = cuts.get("content", [])
    bounds = [0.0] + [c for c in cut_list if 0 < c < dur] + [float(t[-1]) + med]
    # shake: high-pass of the cumulative camera path, reset at cuts
    path_x, path_y = np.cumsum(dx), np.cumsum(dy)
    shake = np.zeros_like(t)
    win_n = max(3, int(round(fps * 0.5)) | 1)
    ker = np.ones(win_n) / win_n
    for b0, b1 in zip(bounds[:-1], bounds[1:]):
        m = (t >= b0) & (t < b1)
        idx = np.nonzero(m)[0]
        if len(idx) < win_n + 2:
            continue
        idx = idx[1:]  # the first frame after a cut has a meaningless shift
        for pth in (path_x, path_y):
            seg = pth[idx] - pth[idx][0]
            sm = np.convolve(np.pad(seg, win_n // 2, mode="edge"), ker, mode="valid")
            shake[idx] += (seg - sm) ** 2
    shake = np.sqrt(shake)
    # black / frozen
    black = (luma < 16) & (P[:, 11] < 8)
    frozen = np.append(False, diff[1:] < 0.15)

    def spans(mask, min_s):
        out, s0 = [], None
        for i, v in enumerate(np.append(mask, False)):
            if v and s0 is None:
                s0 = i
            elif not v and s0 is not None:
                t0, t1 = t[s0], (t[i - 1] + med)
                if t1 - t0 >= min_s:
                    out.append([r(t0, 2), r(t1, 2)])
                s0 = None
        return out

    rep["cuts"] = {"content_s": cuts.get("content"), "adaptive_s": cuts.get("adaptive"), "error": cuts.get("error"),
                   "cuts_per_minute": r(len(cut_list) / max(dur, 1e-6) * 60, 1)}
    rep["black_spans_s"] = spans(black, 0.1)
    rep["frozen_spans_s"] = spans(frozen & ~black, 0.4)
    # per second
    secs = []
    for s0 in range(int(np.ceil(t[-1] + med))):
        m = (t >= s0) & (t < s0 + 1)
        if not m.any():
            continue
        lm = luma[m]
        idx = np.nonzero(m)[0]
        idx = idx[idx > 0]
        dd = luma[idx] - luma[idx - 1]
        flick = 0.0
        if len(dd) > 3:
            # flicker = whole-frame brightness steps that flip direction, where the step explains most of the pixel change
            uni = np.abs(dd) / (diff[idx] + 1e-6) > 0.5
            sc = ((dd[1:] * dd[:-1]) < 0) & (np.abs(dd[1:]) > 1.5) & (np.abs(dd[:-1]) > 1.5) & uni[1:] & uni[:-1]
            flick = float(sc.mean())
        secs.append({"t": s0, "motion": r(diff[m].mean(), 2), "shake_px": r(shake[m].mean(), 2),
                     "luma": r(lm.mean(), 1), "luma_swing": r(lm.max() - lm.min(), 1), "flicker": r(flick, 2),
                     "sharp": r(np.median(sharp[m]), 1)})
    rep["per_second"] = secs
    rep["per_second_units"] = {"motion": "mean abs grey diff between frames (0-255)",
                               "shake_px": f"camera-path jitter in px at analysis width {W}",
                               "flicker": "share of frames whose whole-frame brightness step (>1.5 levels, >50% of the pixel change) flips direction",
                               "sharp": f"Laplacian variance at width {W} (compare within one video only)"}
    # per scene
    scenes = []
    for i, (b0, b1) in enumerate(zip(bounds[:-1], bounds[1:])):
        m = (t >= b0) & (t < b1)
        if not m.any():
            continue
        sub = P[m]
        mid = float((b0 + min(b1, dur)) / 2)
        sample_t = [b0 + (b1 - b0) * q for q in (0.2, 0.5, 0.8)]
        fc, pc = [], []
        for tt in sample_t:
            try:
                f_, p_ = det.count(grab(a.inp, min(tt, max(dur - 0.05, 0)), 640))
            except SystemExit:
                f_, p_ = None, None
            if f_ is not None:
                fc.append(f_); pc.append(p_)
        la, lb = float(sub[:, 8].mean()), float(sub[:, 9].mean())
        lmean, hi, lo = float(sub[:, 1].mean()), float(sub[:, 6].mean()), float(sub[:, 7].mean())
        sc = {"i": i + 1, "start": r(b0, 2), "end": r(min(b1, dur), 2), "len": r(min(b1, dur) - b0, 2),
              "luma": r(lmean, 1), "exposure": exposure_name(lmean, hi, lo), "clipped_hi": r(hi, 3), "crushed_lo": r(lo, 3),
              "lab_a": r(la, 1), "lab_b": r(lb, 1), "cast": cast_name(la, lb) if lmean > 25 else "n/a (dark)",
              "cast_from_neutral_pixels": bool(sub[:, 12].mean() > 0.5),
              "frame_a": r(sub[:, 13].mean(), 1), "frame_b": r(sub[:, 14].mean(), 1), "saturation": r(sub[:, 10].mean(), 1),
              "sharp_median": r(np.median(sub[:, 5]), 1), "motion": r(sub[1:, 2].mean() if len(sub) > 1 else 0, 2),
              "shake_px": r(shake[m].mean(), 2),
              "faces": max(fc) if fc else None, "people": max(pc) if pc else None, "mid_t": r(mid, 2)}
        scenes.append(sc)
    # sharpness relative to the video's own best scene
    best = max((s["sharp_median"] for s in scenes), default=1) or 1
    lit = [s for s in scenes if s["luma"] > 25]
    if len(lit) >= 2:  # shot-to-shot colour match: whole-frame a*/b* against the median of all lit shots
        ma, mb = np.median([s["frame_a"] for s in lit]), np.median([s["frame_b"] for s in lit])
        for s in lit:
            da, db_ = s["frame_a"] - ma, s["frame_b"] - mb
            s["vs_other_shots"] = {"d_a": r(da, 1), "d_b": r(db_, 1),
                                   "note": cast_name(da, db_).replace("neutral", "matches")}
    for s in scenes:
        s["sharp_rel"] = r(s["sharp_median"] / best, 2)
        s["soft"] = bool(s["sharp_rel"] < 0.35 and s["luma"] > 25)  # black/dark scenes have no detail to judge
    rep["scenes"] = scenes
    for d_ in (det.face, det.obj):
        if d_:
            d_.close()
    if getattr(det, "err", None):
        rep["detector_error"] = det.err
    # flags
    flags = []
    if rep["timing"]["real_fps_median"] and rep["timing"]["real_fps_median"] < 20:
        flags.append(f"low real fps {rep['timing']['real_fps_median']}: motion-interpolate to 30")
    if rep["timing"]["gaps_over_1_5x"]:
        flags.append(f"{rep['timing']['gaps_over_1_5x']} frame gaps (dropped frames)")
    for s in secs:
        if s["flicker"] and s["flicker"] > 0.3 and s["luma_swing"] > 6:
            flags.append(f"flicker around {s['t']} s"); break
    shaky = [s["t"] for s in secs if s["shake_px"] and s["shake_px"] > 1.5]
    if shaky:
        flags.append(f"shake > 1.5 px (at width {W}) in seconds {shaky[:10]}")
    for s in scenes:
        if s["soft"]:
            flags.append(f"scene {s['i']} soft/blurred ({s['start']}-{s['end']} s)")
        if "clipped" in s["exposure"] or "crushed" in s["exposure"] or s["exposure"].startswith(("dark", "bright")):
            flags.append(f"scene {s['i']} exposure: {s['exposure']}")
        if s["cast"] not in ("neutral", "n/a (dark)"):
            flags.append(f"scene {s['i']} near-neutral pixels lean {s['cast']} (a*={s['lab_a']}, b*={s['lab_b']})")
        vs = s.get("vs_other_shots")
        if vs and vs["note"] != "matches":
            flags.append(f"scene {s['i']} is more {vs['note']} than the other shots (d_a*={vs['d_a']}, d_b*={vs['d_b']})")
    if rep["black_spans_s"]:
        flags.append(f"black: {rep['black_spans_s']}")
    if rep["frozen_spans_s"]:
        flags.append(f"frozen: {rep['frozen_spans_s']}")
    rep["flags"] = flags
    # contact sheet
    if a.sheet:
        keys = [(s["mid_t"], f"#{s['i']} {s['mid_t']:.1f}s") for s in scenes]
        if len(keys) < 6:  # few scenes: add evenly spaced frames
            keys += [(float(x), f"{x:.1f}s") for x in np.linspace(0.3, max(dur - 0.3, 0.3), 12 - len(keys))]
            keys.sort()
        keys = keys[:a.max_tiles]
        contact_sheet(a.inp, keys, a.sheet)
        rep["contact_sheet"] = os.path.abspath(a.sheet)
    return rep


def contact_sheet(path, keys, out, tw=320):
    tiles = []
    for tt, lab in keys:
        try:
            im = Image.fromarray(grab(path, tt, tw))
        except SystemExit:
            continue
        d = ImageDraw.Draw(im)
        f = font(18)
        d.rectangle([0, 0, tw, 26], fill=(0, 0, 0))
        d.text((6, 3), lab, fill=(255, 255, 0), font=f)
        tiles.append(im)
    if not tiles:
        return
    cols = min(6, len(tiles))
    rows = (len(tiles) + cols - 1) // cols
    th = max(t_.height for t_ in tiles)
    sheet = Image.new("RGB", (cols * tw, rows * th), (20, 20, 20))
    for i, im in enumerate(tiles):
        sheet.paste(im, ((i % cols) * tw, (i // cols) * th))
    sheet.save(out)


def compare(a):
    A, B = a.inp, a.b
    labels = (a.labels or "A,B").split(",")
    times = [float(x) for x in a.at.split(",")] if a.at else None
    if times is None:
        d = []
        for p in (A, B):
            if not p.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".bmp")):
                d.append(probe(p)[1])
        D = min(d) if d else 0
        times = [D * q for q in (0.2, 0.5, 0.8)] if D else [0.0]
    rows, nums = [], []
    tw = a.width if a.width else 480
    for tt in times:
        fa, fb = grab(A, tt, tw), grab(B, tt, tw)
        if fb.shape != fa.shape:
            fb = np.asarray(Image.fromarray(fb).resize((fa.shape[1], fa.shape[0]), Image.LANCZOS))
        sa, sb = frame_stats(fa), frame_stats(fb)
        nums.append({"t": r(tt, 2), labels[0]: {k: r(v, 2) for k, v in sa.items()}, labels[1]: {k: r(v, 2) for k, v in sb.items()},
                     "mean_abs_diff": r(np.abs(fa.astype(np.float32) - fb.astype(np.float32)).mean(), 2)})
        row = Image.new("RGB", (fa.shape[1] * 2 + 8, fa.shape[0] + 30), (20, 20, 20))
        row.paste(Image.fromarray(fa), (0, 30)); row.paste(Image.fromarray(fb), (fa.shape[1] + 8, 30))
        dr = ImageDraw.Draw(row); f = font(18)
        dr.text((6, 5), f"{labels[0]}  {tt:.2f}s  luma {sa['luma']:.0f} sharp {sa['sharp']:.0f}", fill=(255, 255, 0), font=f)
        dr.text((fa.shape[1] + 14, 5), f"{labels[1]}  luma {sb['luma']:.0f} sharp {sb['sharp']:.0f}", fill=(0, 255, 255), font=f)
        rows.append(row)
    H = sum(x.height for x in rows)
    out = Image.new("RGB", (rows[0].width, H), (20, 20, 20))
    y = 0
    for x in rows:
        out.paste(x, (0, y)); y += x.height
    o = a.out or "compare.png"
    out.save(o)
    rep = {"compare_image": os.path.abspath(o), "frames": nums}
    print(f"COMPARE {os.path.basename(A)} vs {os.path.basename(B)} -> {o}")
    for n in nums:
        x, y_ = n[labels[0]], n[labels[1]]
        print(f"  {n['t']}s  luma {x['luma']}->{y_['luma']}  sharp {x['sharp']}->{y_['sharp']}  b* {x['b']}->{y_['b']}  sat {x['sat']}->{y_['sat']}  diff {n['mean_abs_diff']}")
    if a.json:
        print(json.dumps(rep))


def summary(rep):
    tm = rep["timing"]
    L = [f"WATCH {os.path.basename(rep['file'])}  {rep['width']}x{rep['height']} rot {rep['rotation']}  {rep['duration_s']} s",
         f"fps: header {rep['r_frame_rate_header']} / real {tm['real_fps_median']} (mean {tm['real_fps_mean']}), {tm['frames']} frames, VFR {tm['vfr']}, gaps {tm['gaps_over_1_5x']}",
         f"cuts (content): {rep['cuts']['content_s']}   adaptive: {rep['cuts']['adaptive_s']}   ({rep['cuts']['cuts_per_minute']}/min)"]
    for s in rep["scenes"]:
        L.append(f"  scene {s['i']} {s['start']}-{s['end']}s: {s['exposure']} (luma {s['luma']}), cast {s['cast']}, sharp {s['sharp_rel']}, "
                 f"motion {s['motion']}, shake {s['shake_px']} px, faces {s['faces']}, people {s['people']}")
    top = sorted(rep["per_second"], key=lambda s: -(s["motion"] or 0))[:5]
    L.append("most motion at seconds: " + ", ".join(f"{s['t']} ({s['motion']})" for s in top))
    L.append("FLAGS: " + ("; ".join(rep["flags"]) if rep["flags"] else "none"))
    if rep.get("contact_sheet"):
        L.append(f"contact sheet -> {rep['contact_sheet']}  (look at it with Read)")
    print("\n".join(L))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "compare":
        ap = argparse.ArgumentParser(prog="watch.py compare")
        ap.add_argument("cmd"); ap.add_argument("inp"); ap.add_argument("b")
        ap.add_argument("--at"); ap.add_argument("--out"); ap.add_argument("--labels", default="before,after")
        ap.add_argument("--width", type=int, default=480); ap.add_argument("--json", action="store_true")
        compare(ap.parse_args())
        sys.exit()
    ap = argparse.ArgumentParser()
    ap.add_argument("inp")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--out")
    ap.add_argument("--sheet", help="contact sheet PNG path")
    ap.add_argument("--max-tiles", type=int, default=24)
    ap.add_argument("--width", type=int, default=320, help="analysis width (shake px and sharpness are in this scale)")
    a = ap.parse_args()
    rep = analyse(a)
    summary(rep)
    if a.out:
        with open(a.out, "w") as fh:
            json.dump(rep, fh, indent=1)
        print(f"report -> {a.out}")
    if a.json:
        print(json.dumps(rep))
