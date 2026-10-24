#!/usr/bin/env python3
"""sfx_prep.py spec.json out_dir index.json : decode, trim silence, cap length, fade, peak-normalise to -1 dBFS,
encode mp3, measure (length, hit time = loudest 10 ms window, RMS)."""
import json, subprocess, sys, os, numpy as np
spec, outdir, idx = sys.argv[1:4]
os.makedirs(outdir, exist_ok=True)
SR = 48000
res = json.load(open(idx)) if os.path.exists(idx) else []
done = {r["file"] for r in res}
for it in json.load(open(spec)):
    rel = f'{it["category"]}/{it["name"]}.mp3'
    if rel in done: continue
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", it["src"], "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, "<f4").reshape(-1, 2).astype(np.float64)
    if it.get("start"): x = x[int(it["start"] * SR):]
    mono = np.abs(x).max(1)
    pk = mono.max() or 1
    thr = pk * 10 ** (-45 / 20)
    nz = np.where(mono > thr)[0]
    a = max(nz[0] - int(0.005 * SR), 0); b = min(nz[-1] + int(0.05 * SR), len(x))
    x = x[a:b]
    mx = it.get("max", 12.0)
    long_ = len(x) > mx * SR
    if long_:
        x = x[: int(mx * SR)]
    fo = min(int((0.4 if long_ else 0.01) * SR), len(x) // 4)
    x[-fo:] *= np.linspace(1, 0, fo)[:, None]
    if long_ or it.get("fadein"):
        fi = int(0.15 * SR); x[:fi] *= np.linspace(0, 1, fi)[:, None]
    x = x / (np.abs(x).max() or 1) * 10 ** (-1 / 20)
    stereo = np.abs(x[:, 0] - x[:, 1]).max() > 1e-3
    w = int(0.01 * SR)
    m = x.mean(1) if not stereo else np.sqrt((x ** 2).mean(1))
    e = np.sqrt(np.convolve(m ** 2, np.ones(w) / w, "same"))
    hit = float(np.argmax(e) / SR)
    rms = float(20 * np.log10(np.sqrt((x ** 2).mean()) + 1e-12))
    os.makedirs(os.path.join(outdir, it["category"]), exist_ok=True)
    data = (x if stereo else x[:, :1]).astype("<f4").tobytes()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2" if stereo else "1", "-i", "-",
                    "-c:a", "libmp3lame", "-b:a", "192k" if stereo else "128k", os.path.join(outdir, rel)], input=data, check=True)
    r = {"file": rel, "name": it["name"], "category": it["category"], "tags": it.get("tags", []),
         "length_s": round(len(x) / SR, 3), "hit_s": round(hit, 3), "rms_dbfs": round(rms, 1), "peak_dbfs": -1.0,
         "channels": 2 if stereo else 1, "trimmed_to_max": long_, "description": it.get("desc", ""),
         "licence": it["licence"], "licence_url": it["licence_url"], "source": it["source"], "author": it.get("author", ""),
         "original_file": it.get("orig", os.path.basename(it["src"]))}
    res.append(r); done.add(rel)
    print(rel, r["length_s"], r["hit_s"])
json.dump(res, open(idx, "w"), indent=1, ensure_ascii=False)
