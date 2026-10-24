# CPU speed on this box (no GPU): benchmarks and what to use

All numbers measured here on 2026-10-24 (cloud container, `nproc` = 4, 15 GB RAM, no GPU), one job at a time
unless the row says parallel. Software: ffmpeg 6.1.1-3ubuntu5, onnxruntime 1.31.0, torch 2.10.0+cpu (main venv),
MediaPipe 1.1.1, HyperFrames 0.8.191. Scripts used are described in each section so the runs can be repeated.

## Winners (short)

| Job | Use | Instead of | Measured gain |
|---|---|---|---|
| Person matte for video | `library/tools/fast_matte.py` (RVM MobileNetV3 ONNX, recurrent) | rembg u2net_human_seg | 0.10 vs 0.33 s/frame at 1080x1920; P3M alpha error 6.8 vs 17.1; 2.7x less jitter |
| Fill the subject hole before background blur | `cv2.inpaint` Telea on a quarter-size frame, radius 5, upscaled into the hole | Telea on a half-size frame, radius 9 | 0.12 vs 1.25 s/frame; final blurred background differs by 1.8/255 on average |
| bg_blur.py as a whole (both changes above, scratch copy) | see "bg_blur.py switch" below | current bg_blur.py | 0.66 vs 2.08 s/frame (3.2x) on 60 frames 1080x1920 |
| HyperFrames render (1920x1080, 10 s project `video/`) | `--workers 3` (or 2) | default `--workers auto` | 24.6-25 s vs 39.5-50 s |
| x264 delivery encode | `-preset veryfast` for drafts, `fast`/`medium` for finals; leave `-threads` unset | `-preset slow` | slow is 1.4x medium time for +0.00007 SSIM |
| Whisper small transcription | 4 torch threads; dynamic INT8 Linear layers | 2 threads / fp32 | 4 vs 2 threads: 6.6 vs 10.3 s; INT8: 5.5 s, same 99 words |
| Many clips through an ONNX model | several processes with fewer threads each | one process with 4 threads, clips in a row | 4 procs x 1 thread: 14.8 frames/s total vs 10.2 |

## 1. Person matting on CPU (GAP: bg_blur.py is slow)

Ground truth: P3M-500-NP (portrait matting test set with real alpha, HF dataset `nobg/P3M-10K`, card licence MIT,
https://huggingface.co/datasets/nobg/P3M-10K, read 2026-10-24), 30 images (every 17th), resized to long side 1024.
Metrics: MAD = mean |alpha - truth| x1000, IoU at 0.5, edge = MAD inside a 15 px band around the truth edge.
ONNX models: 4 intra-op threads. Script: `library/tools/bench/bench_matte.py`.

| Model (input long side 1024) | s/frame | MAD x1000 | IoU | edge MAD x1000 | Source / licence (repo page) |
|---|---|---|---|---|---|
| rembg `u2net_human_seg` (current bg_blur) | 0.275 | 17.17 | 0.964 | 125.9 | rembg 2.0.86 |
| MediaPipe selfie_segmenter (256 px) | 0.007 | 18.96 | 0.949 | 148.7 | storage.googleapis.com/mediapipe-models, licence not checked |
| MediaPipe selfie_multiclass 256 (1 - background) | 0.080 | 68.55 | 0.973 | 126.5 | same |
| MODNet fp32, short side 512 (Xenova ONNX) | 0.187 | 15.55 | 0.961 | 80.3 | github.com/ZHKKKe/MODNet, Apache-2.0, 4382 stars |
| MODNet uint8 (Xenova ONNX) | 0.427 | 41.57 | 0.896 | 130.5 | same: slower AND worse |
| RVM mobilenetv3, ratio 0.25, 1 pass | 0.030 | 11.87 | 0.972 | 84.3 | github.com/PeterL1n/RobustVideoMatting, GPL-3.0, 9565 stars |
| RVM ratio 0.375, 1 pass | 0.054 | 7.24 | 0.981 | 70.5 | same |
| RVM ratio 0.5, 1 pass | 0.082 | 6.00 | 0.986 | 62.5 | same |
| RVM ratio 0.375, 3 passes (state fed back) | 0.143 | 6.63 | 0.983 | 68.2 | same |
| RVM ratio 0.5, 3 passes | 0.241 | 5.52 | 0.987 | 61.2 | same |
| BiRefNet-lite 1024 (onnx-community ONNX) | 6.54 | 3.41 | 0.992 | 39.8 | github.com/ZhengPeng7/BiRefNet, MIT, 3914 stars |

Same images upscaled to long side 1920 (phone-video size; pre/post-processing included):

| Model | s/frame | MAD x1000 | IoU | edge |
|---|---|---|---|---|
| rembg u2net_human_seg | 0.324 | 17.10 | 0.964 | 125.5 |
| MediaPipe selfie_segmenter | 0.010 | 19.24 | 0.946 | 150.7 |
| MODNet fp32 512 | 0.233 | 15.55 | 0.960 | 85.0 |
| RVM ratio 0.25 (480 px inside), 1 pass | 0.115 | 6.78 | 0.983 | 65.1 |
| RVM ratio 0.375, 1 pass | 0.203 | 10.54 | 0.976 | 65.0 |

RVM's own docs: "Set `downsample_ratio` so that the downsampled resolution is between 256 and 512. For example,
for 1920x1080 input with downsample_ratio=0.25 ..." and "You must process frames sequentially and recycle its
recurrent states" (https://github.com/PeterL1n/RobustVideoMatting/blob/master/documentation/inference.md, read
2026-10-24). fast_matte.py does both (auto ratio = 480 / long side).

Video test (10 s of the CC0 interview upscaled to 1080x1920, 302 frames, state carried in RVM; jitter = mean
|alpha_t - alpha_t-1| x1000 on pixels whose grey value changed < 2 levels):

| Model | s/frame | jitter |
|---|---|---|
| RVM (fast_matte.RVM, auto ratio 0.25) | 0.103 | 0.93 |
| MediaPipe selfie_segmenter | 0.012 | 4.67 |
| rembg u2net_human_seg | 0.327 | 2.50 |

`fast_matte.py IN.mp4 alpha.mp4 --composite comp.mp4 --bg blur` on the same clip: model 0.134 s/frame, whole
tool (decode + 2 encodes + blur) 0.278 s/frame. Looked at frame 5.0 s: clean hair/shoulder edge.

Decision: RVM is the CPU winner (3x faster than u2net, ~2.5x lower alpha error, ~2.7x steadier). BiRefNet-lite
is the most accurate but 6.5 s/frame (CLAUDE.md already says BiRefNet-portrait was too slow). MediaPipe is only
good for instant previews. Licence: RVM is GPL-3.0 (repo page); MODNet Apache-2.0 is the permissive runner-up.

### bg_blur.py switch (NOT applied; bg_blur.py is unchanged - show the owner before/after first)

cProfile of the current bg_blur.py on 15 frames 1080x1920: `cv2.inpaint` 1.113 s/frame (16.7 of 29.6 s),
u2net ONNX run 0.313 s/frame. So the inpaint is the main cost, not the mask.

A scratch copy with two edits ran 60 frames in 39.4 s (0.66 s/frame) vs 124.8 s (2.08 s/frame) for the original.
`watch.py compare` at 0.5 s and 1.5 s: mean abs difference 1.0 and 1.7 /255, luma 134 vs 134, same look on the
main subject. One visible difference: RVM matted only the main person, so a second person's shoulder at the left
frame edge got blurred, while u2net kept it sharp at 0.5 s. Edits:

```python
# 1) mask: replace rembg (import + new_session + remove(...) + resize) with
sys.path.insert(0, "/home/user/new-startup/library/tools"); from fast_matte import RVM
RV = RVM()                 # once
pm = RV(rgb)               # in process(): full-res float alpha 0..1, call frames in order
# (the existing temporal smoothing, dark-shirt fill and desk logic stay as they are)

# 2) background(): replace  filled = cv2.inpaint(small, hole, 9, cv2.INPAINT_TELEA)  with
s2 = cv2.resize(small, (sw // 2, sh // 2), interpolation=cv2.INTER_AREA)
h2 = (cv2.resize(hole, (sw // 2, sh // 2)) > 0).astype(np.uint8) * 255
up = cv2.resize(cv2.inpaint(s2, h2, 5, cv2.INPAINT_TELEA), (sw, sh), interpolation=cv2.INTER_LINEAR)
filled = small.copy(); filled[hole > 0] = up[hole > 0]
```

fast_matte needs onnxruntime + numpy, both already in the main venv (rembg depends on onnxruntime), plus the
model file from `setup-specialist-a.sh`. Fill methods compared on 5 frames (`library/tools/bench/bench_fill.py`) (final blurred background vs Telea
half-size): Telea quarter-size 0.124 s, diff 1.76 (4.43 inside the hole); push-pull pyramid 0.059 s, diff 11.2
(28.5 inside the hole, a dark smear was visible) -> not used.

## 2. ONNX Runtime threads and INT8

RVM at 1080x1920 (4 s clip, 122 frames, `library/tools/bench/bench_matte_video.py`), one process: 1 thread 0.233 s/frame, 2 threads 0.136, 4 threads 0.098.
Parallel processes on the same clip: 2 procs x 2 threads 0.157 s/frame each (12.7 frames/s total, wall 22.6 s for
two jobs vs 32.3 s for the two jobs one after the other with 4 threads); 4 procs x 1 thread 0.271 s/frame each
(14.8 frames/s total, wall 37.5 s for four jobs). -> For several clips, run clips in parallel with
`intra_op_num_threads = 4 / jobs`; for one clip use 4 threads.

INT8: `onnxruntime.quantization.quantize_dynamic` (QUInt8 weights) of RVM at 1920 px: 0.187 s/frame vs 0.130 fp32
and MAD 7.35 vs 6.78 -> slower and worse. Xenova's MODNet uint8 was also slower (0.43 vs 0.19 s) and worse.
Dynamic INT8 does not help these conv nets on this CPU.

## 3. torch threads and INT8 (Whisper small, main venv, `library/tools/bench/bench_whisper.py`)

40 s English speech, `transcribe(fp16=False, condition_on_previous_text=False, language="en")`, model load excluded:
4 threads fp32 6.6 s, 2 threads fp32 10.3 s, 4 threads `torch.quantization.quantize_dynamic(model, {nn.Linear},
qint8)` 5.5 s with the same 99 words (difflib word ratio 1.0). Untested here: INT8 on Urdu/Hindi (unverified).
ACE-Step INT8 notes are in CLAUDE.md (already measured by another session).

## 4. ffmpeg / x264

Source: 10 s, 1080x1920, 30 fps, lossless FFV1 (made from the CC0 clip). `-c:v libx264 -crf 18 -pix_fmt yuv420p`,
SSIM vs the source with ffmpeg's `ssim` filter (time includes FFV1 decode):

| preset | time s | size MB | SSIM |
|---|---|---|---|
| ultrafast | 7.25 | 33.3 | 0.96661 |
| superfast | 7.69 | 12.2 | 0.96995 |
| veryfast | 8.99 | 9.3 | 0.97002 |
| faster | 11.60 | 10.7 | 0.97130 |
| fast | 13.74 | 11.3 | 0.97187 |
| medium | 15.69 | 11.0 | 0.97182 |
| slow | 21.98 | 10.9 | 0.97189 |

Threads (medium): `-threads 1` 37.8 s, `2` 20.7 s, `4` 16.5 s, unset/`0` (x264 auto) 14.5 s -> don't set it.
Two medium encodes: one after the other 29.1 s, both at once 26.9 s (auto threads) / 26.7 s (`-threads 2` each):
~8% gain from running two at once.

## 5. HyperFrames render

`npx --yes hyperframes@0.8.191 render . -o OUT.mp4 --quiet` in `video/` (10 s, 1920x1080, 30 fps, 300 frames),
wall clock:

| flags | run 1 | run 2 |
|---|---|---|
| (default, `--workers auto`) | 50 s (first run of the session) | 39.5 s |
| `--workers 1` | 35 s | 36.1 s |
| `--workers 2` | 26 s | 27.1 s |
| `--workers 3` | 25 s | 24.6 s |
| `--workers 4` | 32 s | - |
| `--quality draft` (auto workers) | 38 s | - |
| `--quality draft --workers 2` | 22.5 s | - |

The help text (`render --help`, v0.8.191) says each worker is a separate Chrome (~256 MB RAM), and
`--experimental-fast-capture` engages by default only on "macOS + hardware-GPU browser", so it does not apply here.
-> Use `--workers 3` on this box; `--quality draft` for quick looks.

## 6. Running two heavy jobs at once

Measured here: two ONNX jobs at 2 threads each beat one-after-the-other at 4 threads (22.6 vs 32.3 s); two x264
encodes gain ~8%. CLAUDE.md (earlier session) measured that ACE-Step + Whisper together made both 3-4x slower:
it was not re-measured here, and why it happens was not measured (unverified).
