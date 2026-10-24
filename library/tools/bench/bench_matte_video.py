# temporal stability + speed of mattes on a video: perc-venv/bin/python bench_video.py VIDEO model [threads]
import sys, time, subprocess, numpy as np, cv2, json
sys.path.insert(0, "/home/user/new-startup/library/tools")
from fast_matte import RVM, MediaPipeSelfie, probe
v, model = sys.argv[1], sys.argv[2]; th = int(sys.argv[3]) if len(sys.argv) > 3 else 4
fps, w, h = probe(v)
if model == "rvm": M = RVM(threads=th)
elif model == "mediapipe": M = MediaPipeSelfie()
else:
    import onnxruntime as ort
    from rembg import new_session
    from PIL import Image
    so = ort.SessionOptions(); so.intra_op_num_threads = th; so.inter_op_num_threads = 1
    s = new_session("u2net_human_seg", sess_opts=so)
    M = lambda rgb: np.asarray(s.predict(Image.fromarray(rgb))[0].resize((rgb.shape[1], rgb.shape[0])), np.float32) / 255
dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", v, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
prev = prevg = None; jit = []; ts = []; n = 0
while True:
    b = dec.stdout.read(w * h * 3)
    if len(b) < w * h * 3: break
    rgb = np.frombuffer(b, np.uint8).reshape(h, w, 3)
    t0 = time.perf_counter(); a = M(rgb); dt = time.perf_counter() - t0
    if n > 0: ts.append(dt)
    g = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY).astype(np.float32)
    if prev is not None:
        still = np.abs(g - prevg) < 2
        jit.append(float(np.abs(a - prev)[still].mean()))
    prev, prevg = a, g; n += 1
print(json.dumps({"model": model, "threads": th, "frames": n, "size": f"{w}x{h}", "s_per_frame": round(float(np.mean(ts)), 4),
                  "alpha_jitter_on_still_pixels_x1000": round(float(np.mean(jit)) * 1000, 3)}))
