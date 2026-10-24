# Matting benchmark used for library/research/cpu-speed.md (2026-10-24). Images: P3M-500-NP (HF nobg/P3M-10K), extract to IMGDIR/NN.jpg + GTDIR/NN.png.
# Needs the --bench models: bash library/tools/setup-specialist-a.sh --bench
# Benchmark CPU person-matting models on P3M-500-NP images with ground-truth alpha.
# usage: perc-venv/bin/python bench_matte.py IMGDIR GTDIR OUT.json [--threads 4] [--only a,b]
import argparse, glob, json, os, time
import numpy as np, cv2
from PIL import Image
import onnxruntime as ort

M = "/home/user/tools/perc-models"
ap = argparse.ArgumentParser()
ap.add_argument("img"); ap.add_argument("gt"); ap.add_argument("out")
ap.add_argument("--threads", type=int, default=4); ap.add_argument("--only", default="")
ap.add_argument("--upscale", type=int, default=0, help="resize inputs to this long side first (timing at video size)")
a = ap.parse_args()


def so():
    o = ort.SessionOptions(); o.intra_op_num_threads = a.threads; o.inter_op_num_threads = 1
    o.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
    return o


def sess(f):
    return ort.InferenceSession(os.path.join(M, f), so(), providers=["CPUExecutionProvider"])


# ---- models: each takes RGB uint8 HxWx3 -> alpha float32 HxW in [0,1]
def mk_rembg(name):
    from rembg import new_session
    s = new_session(name, sess_opts=so())
    def f(rgb):
        m = s.predict(Image.fromarray(rgb))[0]
        return np.asarray(m.resize((rgb.shape[1], rgb.shape[0])), np.float32) / 255
    return f


def mk_modnet(file, ref=512):
    s = sess(file)
    def f(rgb):
        h, w = rgb.shape[:2]
        sc = ref / min(h, w)
        nh, nw = int(round(h * sc / 32) * 32), int(round(w * sc / 32) * 32)
        x = cv2.resize(rgb, (nw, nh), interpolation=cv2.INTER_AREA).astype(np.float32) / 255
        x = ((x - 0.5) / 0.5).transpose(2, 0, 1)[None]
        p = s.run(None, {"input": x})[0][0, 0]
        return cv2.resize(p, (w, h), interpolation=cv2.INTER_LINEAR)
    return f


def mk_rvm(ratio):
    s = sess("rvm_mobilenetv3_fp32.onnx")
    def f(rgb, state=None):
        x = (rgb.astype(np.float32) / 255).transpose(2, 0, 1)[None]
        rec = [np.zeros((1, 1, 1, 1), np.float32)] * 4
        # single image: run 3 times feeding the state back (RVM is recurrent; one pass from zero state is weak)
        for _ in range(3):
            fgr, pha, *rec = s.run(None, {"src": x, "r1i": rec[0], "r2i": rec[1], "r3i": rec[2], "r4i": rec[3],
                                          "downsample_ratio": np.array([ratio], np.float32)})
        return pha[0, 0]
    return f


def mk_rvm1(ratio):
    s = sess("rvm_mobilenetv3_fp32.onnx")
    def f(rgb):
        x = (rgb.astype(np.float32) / 255).transpose(2, 0, 1)[None]
        rec = [np.zeros((1, 1, 1, 1), np.float32)] * 4
        fgr, pha, *rec = s.run(None, {"src": x, "r1i": rec[0], "r2i": rec[1], "r3i": rec[2], "r4i": rec[3],
                                      "downsample_ratio": np.array([ratio], np.float32)})
        return pha[0, 0]
    return f


def mk_birefnet():
    s = sess("birefnet_lite.onnx")
    mean = np.array([0.485, 0.456, 0.406], np.float32); std = np.array([0.229, 0.224, 0.225], np.float32)
    def f(rgb):
        h, w = rgb.shape[:2]
        x = cv2.resize(rgb, (1024, 1024), interpolation=cv2.INTER_LINEAR).astype(np.float32) / 255
        x = ((x - mean) / std).transpose(2, 0, 1)[None]
        p = s.run(None, {"input_image": x})[0][0, 0]
        p = 1 / (1 + np.exp(-p)) if p.min() < 0 or p.max() > 1 else p
        return cv2.resize(p, (w, h))
    return f


def mk_mp(file, cat_mask_person=None):
    import mediapipe as mp
    from mediapipe.tasks.python import vision, BaseOptions
    seg = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(
        base_options=BaseOptions(model_asset_path=os.path.join(M, file)), output_confidence_masks=True,
        output_category_mask=False))
    def f(rgb):
        r = seg.segment(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(rgb)))
        cm = r.confidence_masks
        if len(cm) == 1:
            return cm[0].numpy_view().astype(np.float32).copy()
        return 1 - cm[0].numpy_view().astype(np.float32)  # multiclass: channel 0 = background
    f.close = seg.close
    return f


MODELS = {
    "rembg_u2net_human_seg": lambda: mk_rembg("u2net_human_seg"),
    "mediapipe_selfie_segmenter": lambda: mk_mp("selfie_segmenter.tflite"),
    "mediapipe_selfie_multiclass": lambda: mk_mp("selfie_multiclass_256x256.tflite"),
    "modnet_fp32_512": lambda: mk_modnet("modnet.onnx"),
    "modnet_uint8_512": lambda: mk_modnet("modnet_uint8.onnx"),
    "rvm_mnv3_r0.25_x1": lambda: mk_rvm1(0.25),
    "rvm_mnv3_r0.375_x3": lambda: mk_rvm(0.375),
    "birefnet_lite_1024": lambda: mk_birefnet(),
    "rvm_mnv3_r0.375_x1": lambda: mk_rvm1(0.375),
    "rvm_mnv3_r0.5_x1": lambda: mk_rvm1(0.5),
    "rvm_mnv3_r0.25_x3": lambda: mk_rvm(0.25),
    "rvm_mnv3_r0.5_x3": lambda: mk_rvm(0.5),
}
only = [x for x in a.only.split(",") if x]
files = sorted(glob.glob(os.path.join(a.img, "*.jpg")))
res = {}
for name, ctor in MODELS.items():
    if only and name not in only:
        continue
    f = ctor()
    times, mad, mse, iou, bnd = [], [], [], [], []
    for k, p in enumerate(files):
        rgb = np.asarray(Image.open(p).convert("RGB"))
        gt = np.asarray(Image.open(os.path.join(a.gt, os.path.basename(p)[:-4] + ".png")), np.float32) / 255
        inp = rgb
        if a.upscale:
            sc = a.upscale / max(rgb.shape[:2])
            inp = cv2.resize(rgb, (round(rgb.shape[1] * sc), round(rgb.shape[0] * sc)), interpolation=cv2.INTER_LINEAR)
        t0 = time.perf_counter()
        al = f(inp)
        dt = time.perf_counter() - t0
        if k > 0:
            times.append(dt)  # first call = warm-up
        al = cv2.resize(np.clip(al, 0, 1).astype(np.float32), (gt.shape[1], gt.shape[0]))
        e = np.abs(al - gt)
        mad.append(e.mean()); mse.append((e ** 2).mean())
        A, G = al > 0.5, gt > 0.5
        iou.append((A & G).sum() / max((A | G).sum(), 1))
        band = cv2.dilate(((gt > 0.02) & (gt < 0.98)).astype(np.uint8) | cv2.morphologyEx(G.astype(np.uint8), cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8)), np.ones((15, 15), np.uint8)) > 0
        bnd.append(e[band].mean() if band.any() else 0)
        if k < 3:
            os.makedirs("vis", exist_ok=True)
            Image.fromarray((al * 255).astype(np.uint8)).save(f"vis/{name}_{k:02d}.png")
    if hasattr(f, "close"):
        f.close()
    res[name] = {"s_per_frame_mean": round(float(np.mean(times)), 4), "s_per_frame_p90": round(float(np.percentile(times, 90)), 4),
                 "MAD_x1000": round(float(np.mean(mad)) * 1000, 2), "MSE_x1000": round(float(np.mean(mse)) * 1000, 2),
                 "IoU@0.5": round(float(np.mean(iou)), 4), "edge_band_MAD_x1000": round(float(np.mean(bnd)) * 1000, 1),
                 "n": len(files), "threads": a.threads, "input_long_side": a.upscale or 1024}
    print(name, res[name], flush=True)
json.dump(res, open(a.out, "w"), indent=1)
