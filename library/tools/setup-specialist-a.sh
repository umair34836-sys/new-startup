#!/usr/bin/env bash
# Perception + fast-CPU tools (listen.py, watch.py, fast_matte.py). Idempotent: safe to run every session.
#   bash library/tools/setup-specialist-a.sh          # venv /home/user/tools/perc-venv (~1.4 GB), models /home/user/tools/perc-models (~40 MB)
#   bash library/tools/setup-specialist-a.sh --bench  # also BiRefNet-lite (214 MB) + MODNet, only needed to rerun the matting benchmark
# listen.py's Whisper words and --vocals use the MAIN venv (/home/user/tools/venv, setup-all.sh heavy).
set -u
T=/home/user/tools
V=${PERC_VENV:-$T/perc-venv}
M=${PERC_MODELS:-$T/perc-models}
export PATH="$HOME/.local/bin:$PATH"
command -v uv >/dev/null || curl -LsSf https://astral.sh/uv/install.sh | sh
mkdir -p "$M"

# MediaPipe Tasks needs libGLESv2/libEGL even on CPU (import fails with "libGLESv2.so.2: cannot open shared object file")
if ! ldconfig -p | grep -q libGLESv2.so.2; then
  apt-get install -y -q libgles2 libegl1 >/dev/null 2>&1 || { apt-get update -q >/dev/null 2>&1; apt-get install -y -q libgles2 libegl1 >/dev/null 2>&1; }
fi

[ -x "$V/bin/python" ] || uv venv -q -p /usr/bin/python3.12 "$V"
# no torch here on purpose (silero-vad's pip package pulls CUDA torch, ~5 GB): Silero runs from its ONNX file
"$V/bin/python" -c "import librosa, pyloudnorm, scenedetect, onnxruntime, mediapipe, essentia, cv2, rembg, pyarrow" 2>/dev/null ||
  VIRTUAL_ENV="$V" uv pip install -q librosa pyloudnorm "scenedetect[opencv-headless]" onnxruntime onnx mediapipe essentia \
    soundfile rembg pyarrow

get() {  # get FILE URL
  if [ ! -s "$M/$1" ]; then
    curl -sSfL --retry 3 -o "$M/$1.part" "$2" && mv "$M/$1.part" "$M/$1" || echo "setup-specialist-a: FAILED to download $1" >&2
  fi
}
get silero_vad.onnx https://raw.githubusercontent.com/snakers4/silero-vad/master/src/silero_vad/data/silero_vad.onnx
get rvm_mobilenetv3_fp32.onnx https://github.com/PeterL1n/RobustVideoMatting/releases/download/v1.0.0/rvm_mobilenetv3_fp32.onnx
get selfie_segmenter.tflite https://storage.googleapis.com/mediapipe-models/image_segmenter/selfie_segmenter/float16/latest/selfie_segmenter.tflite
get blaze_face_short_range.tflite https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/latest/blaze_face_short_range.tflite
get efficientdet_lite0.tflite https://storage.googleapis.com/mediapipe-models/object_detector/efficientdet_lite0/int8/latest/efficientdet_lite0.tflite
if [ "${1:-}" = "--bench" ]; then
  get selfie_multiclass_256x256.tflite https://storage.googleapis.com/mediapipe-models/image_segmenter/selfie_multiclass_256x256/float32/latest/selfie_multiclass_256x256.tflite
  get modnet.onnx https://huggingface.co/Xenova/modnet/resolve/main/onnx/model.onnx
  get modnet_uint8.onnx https://huggingface.co/Xenova/modnet/resolve/main/onnx/model_uint8.onnx
  get birefnet_lite.onnx https://huggingface.co/onnx-community/BiRefNet_lite-ONNX/resolve/main/onnx/model.onnx
fi
uv cache clean >/dev/null 2>&1 || true
"$V/bin/python" -c "import librosa, essentia, scenedetect, mediapipe, onnxruntime; print('specialist-a ready')" 2>/dev/null | grep -v INFO
[ -z "${PERC_VENV:-}" ] && touch "$T/.specialist-a-ready"
