#!/home/user/tools/perc-venv/bin/python
# Usage: python library/tools/fast_matte.py IN.(mp4|jpg|png) OUT_ALPHA.(mp4|png) [--composite COMP.mp4|png --bg blur|green|#rrggbb]
#        [--ratio auto] [--threads 4] [--model rvm|mediapipe]
# Fast CPU person matte. Default model: Robust Video Matting (MobileNetV3, ONNX, GPL-3.0), recurrent, so the
# matte stays stable from frame to frame. Benchmarked here (library/research/cpu-speed.md): at 1080x1920 input
# ~0.11 s/frame vs rembg u2net_human_seg ~0.32 s/frame, with less than half the alpha error on P3M-500-NP.
# Works in either venv (perc-venv or the main venv): needs numpy + onnxruntime (+ opencv for --bg blur) and ffmpeg.
# Python use (e.g. from bg_blur.py):
#   sys.path.insert(0, "library/tools"); from fast_matte import RVM
#   m = RVM(); alpha = m(rgb_uint8)   # call frames IN ORDER; m.reset() at a cut or a new clip
import argparse, json, os, subprocess, sys, time
import numpy as np

MODELS = "/home/user/tools/perc-models"


def auto_ratio(h, w):
    # RVM docs: pick downsample_ratio so the downsampled frame is between 256 and 512 px (1920x1080 -> 0.25)
    return float(min(1.0, max(0.1, 480.0 / max(h, w))))


class RVM:
    def __init__(self, ratio=None, threads=4, model=os.path.join(MODELS, "rvm_mobilenetv3_fp32.onnx")):
        import onnxruntime as ort
        so = ort.SessionOptions()
        so.intra_op_num_threads = threads; so.inter_op_num_threads = 1
        self.s = ort.InferenceSession(model, so, providers=["CPUExecutionProvider"])
        self.ratio = ratio
        self.reset()

    def reset(self):
        self.rec = [np.zeros((1, 1, 1, 1), np.float32)] * 4

    def __call__(self, rgb, fgr=False):
        h, w = rgb.shape[:2]
        r = self.ratio or auto_ratio(h, w)
        x = (rgb.astype(np.float32) / 255).transpose(2, 0, 1)[None]
        f, pha, *self.rec = self.s.run(None, {"src": x, "r1i": self.rec[0], "r2i": self.rec[1], "r3i": self.rec[2],
                                              "r4i": self.rec[3], "downsample_ratio": np.array([r], np.float32)})
        a = np.clip(pha[0, 0], 0, 1)
        return (a, np.clip(f[0].transpose(1, 2, 0), 0, 1)) if fgr else a


class MediaPipeSelfie:
    """~0.01 s/frame but coarse edges (P3M MAD 19 vs RVM 7): previews and rough masks only."""
    def __init__(self, **_):
        import mediapipe as mp
        from mediapipe.tasks.python import vision, BaseOptions
        self.mp = mp
        self.seg = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(
            base_options=BaseOptions(model_asset_path=os.path.join(MODELS, "selfie_segmenter.tflite")),
            output_confidence_masks=True, output_category_mask=False,
            running_mode=vision.RunningMode.IMAGE))

    def reset(self):
        pass

    def __call__(self, rgb):
        r = self.seg.segment(self.mp.Image(image_format=self.mp.ImageFormat.SRGB, data=np.ascontiguousarray(rgb)))
        m = r.confidence_masks[0].numpy_view().astype(np.float32)
        return m if m.shape == rgb.shape[:2] else __import__("cv2").resize(m, (rgb.shape[1], rgb.shape[0]))


def probe(path):
    j = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                   "stream=avg_frame_rate", "-of", "json", path], capture_output=True, text=True).stdout)
    num, den = j["streams"][0]["avg_frame_rate"].split("/")
    fps = float(num) / float(den) if float(den) else 30.0
    one = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-vf", "null", "-"], capture_output=True).stdout
    hw = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                         "-of", "csv=p=0", path], capture_output=True, text=True).stdout.strip().split(",")
    w, h = int(hw[0]), int(hw[1])
    if len(one) != w * h * 3:  # autorotated phone clip: width/height swapped
        w, h = h, w
    return fps, w, h


def composite(rgb, a, bg):
    if bg == "blur":
        import cv2
        k = max(3, int(max(rgb.shape[:2]) / 40) | 1)
        back = cv2.GaussianBlur(rgb, (k, k), 0).astype(np.float32)
    elif bg == "green":
        back = np.zeros_like(rgb, np.float32); back[..., 1] = 255
    else:
        c = bg.lstrip("#"); back = np.zeros_like(rgb, np.float32) + np.array([int(c[i:i + 2], 16) for i in (0, 2, 4)], np.float32)
    a3 = a[..., None]
    return (rgb.astype(np.float32) * a3 + back * (1 - a3)).clip(0, 255).astype(np.uint8)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inp"); ap.add_argument("out", help="alpha: .mp4 (grey, crf 12) or .png (image input)")
    ap.add_argument("--composite"); ap.add_argument("--bg", default="green")
    ap.add_argument("--ratio", type=float, default=None, help="RVM downsample_ratio (default: auto, 480 px long side)")
    ap.add_argument("--threads", type=int, default=4)
    ap.add_argument("--model", default="rvm", choices=["rvm", "mediapipe"])
    a = ap.parse_args()
    from PIL import Image
    M = RVM(a.ratio, a.threads) if a.model == "rvm" else MediaPipeSelfie()
    if a.inp.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
        rgb = np.asarray(Image.open(a.inp).convert("RGB"))
        t0 = time.perf_counter()
        al = M(rgb)
        if a.model == "rvm":  # single image: feed the state back twice (measured on P3M at 1024 px, ratio 0.5: MAD 6.0 -> 5.5)
            al = M(rgb); al = M(rgb)
        Image.fromarray((al * 255).astype(np.uint8)).save(a.out)
        if a.composite:
            Image.fromarray(composite(rgb, al, a.bg)).save(a.composite)
        print(f"{a.out}  {time.perf_counter() - t0:.2f} s")
        return
    fps, w, h = probe(a.inp)
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", a.inp, "-an", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                           stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "gray", "-s", f"{w}x{h}", "-r", f"{fps}",
                            "-i", "-", "-c:v", "libx264", "-crf", "12", "-preset", "veryfast", "-pix_fmt", "yuv420p", a.out],
                           stdin=subprocess.PIPE)
    comp = None
    if a.composite:
        comp = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-r", f"{fps}",
                                 "-i", "-", "-i", a.inp, "-map", "0:v", "-map", "1:a?", "-c:v", "libx264", "-crf", "18",
                                 "-preset", "veryfast", "-pix_fmt", "yuv420p", "-c:a", "copy", "-shortest", a.composite],
                                stdin=subprocess.PIPE)
    n, t0, tm = 0, time.perf_counter(), 0.0
    while True:
        b = dec.stdout.read(w * h * 3)
        if len(b) < w * h * 3:
            break
        rgb = np.frombuffer(b, np.uint8).reshape(h, w, 3)
        t1 = time.perf_counter()
        al = M(rgb)
        tm += time.perf_counter() - t1
        enc.stdin.write((al * 255 + 0.5).astype(np.uint8).tobytes())
        if comp:
            comp.stdin.write(composite(rgb, al, a.bg).tobytes())
        n += 1
        if n % 100 == 0:
            print(f"  {n} frames, model {tm / n:.3f} s/frame", flush=True)
    for p in (enc, comp):
        if p:
            p.stdin.close(); p.wait()
    dec.wait()
    print(f"{a.out}: {n} frames {w}x{h}, model {tm / max(n, 1):.3f} s/frame, total {(time.perf_counter() - t0) / max(n, 1):.3f} s/frame")


if __name__ == "__main__":
    main()
