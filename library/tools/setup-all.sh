#!/bin/bash
# Install every tool this repo uses into a fresh cloud container, skipping what is already there.
#   bash library/tools/setup-all.sh light   # quick (~1 min, Oct 2026 estimate): ffmpeg, PIL/numpy/mido/pyworld, Agent-Reach, graft, REA, Crawl4AI
#   bash library/tools/setup-all.sh heavy   # music + AI song stack, VoiceStudio, model weights (~20 min, ~15 GB)
# The SessionStart hook runs "all" in the background, logging to /home/user/tools/setup.log; it touches
# /home/user/tools/.light-ready and then /home/user/tools/.heavy-ready as each part finishes.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
T=/home/user/tools
export PATH="$HOME/.local/bin:$PATH"
mkdir -p "$T"

light() {
  command -v ffmpeg >/dev/null || { apt-get update -qq && DEBIAN_FRONTEND=noninteractive apt-get install -y -qq ffmpeg; }
  # System-python libraries the library/tools scripts import (PIL, numpy, mido, pyworld pitch analysis).
  python3 -c "import PIL, numpy, mido, pyworld" 2>/dev/null || pip install -q pillow numpy mido pyworld
  command -v uv >/dev/null || curl -LsSf https://astral.sh/uv/install.sh | sh
  command -v agent-reach >/dev/null || {
    uv tool install -q https://github.com/Panniantong/Agent-Reach/releases/latest/download/agent-reach.zip &&
      agent-reach setup >/dev/null
  }
  command -v graft >/dev/null || { npm i -g -s @nanonets/graft@0.25.0 && graft telemetry disable >/dev/null; }
  # REA (morluto/rea): reverse-engineering CLI; its MCP server is registered in the repo's .mcp.json.
  command -v rea >/dev/null || npm i -g -s rea-agents@6.7.0
  # Urdu/Pashto/Hindi captions + client brand kit (specialist D): fonttools, numpy, pillow, qrcode
  bash "$HERE/setup-specialist-d.sh" >/dev/null
  # Crawl4AI (free local Firecrawl replacement, web_capture.py): own venv; playwright 1.56.0 = /opt/pw-browsers chromium-1194
  # (container-dependent: the 2026-10-24 image had chromium-1243 / system playwright 1.63.0, and web_capture.py failed).
  [ -x "$T/crawl-venv/bin/python" ] || uv venv -q -p /usr/bin/python3.12 "$T/crawl-venv"
  "$T/crawl-venv/bin/python" -c "import crawl4ai" 2>/dev/null ||
    VIRTUAL_ENV="$T/crawl-venv" uv pip install -q crawl4ai "playwright==1.56.0"
}

heavy() {
  bash "$HERE/setup-music.sh"
  bash "$HERE/setup-ai-song.sh"
  # Weights: ACE-Step turbo + VAE + text encoder + LM (huggingface, non-Xet path) and Whisper small.
  cd "$T/ACE-Step-1.5" && HF_HUB_DISABLE_XET=1 "$T/venv/bin/python" -c \
    "from acestep.model_downloader import ensure_main_model as e; print(e(prefer_source='huggingface'))"
  "$T/venv/bin/python" -c "import whisper; whisper.load_model('small'); print('whisper small ready')"
  # Vocal separation (music -> zero under a voice): audio-separator + BS-RoFormer weights (GitHub release download).
  VIRTUAL_ENV="$T/venv" uv pip install -q "audio-separator[cpu]" audioread pydub onnxruntime librosa samplerate \
    julius diffq ml_collections beartype rotary-embedding-torch resampy
  "$T/venv/bin/audio-separator" --download_model_only -m model_bs_roformer_ep_368_sdr_12.9628.ckpt \
    --model_file_dir "$T/sep-models" >/dev/null && echo "separator ready"
  # clean_voice.py: denoise, de-reverb and the fast vocal model.
  for m in denoise_mel_band_roformer_aufr33_sdr_27.9959.ckpt UVR-DeEcho-DeReverb.pth UVR-MDX-NET-Voc_FT.onnx; do
    "$T/venv/bin/audio-separator" --download_model_only -m "$m" --model_file_dir "$T/sep-models" >/dev/null
  done
  # bg_blur.py: person segmentation (u2net_human_seg weights download on first use, 175,997,641 bytes = 168 MiB, 2026-10-24)
  "$T/venv/bin/python" -c "import rembg, cv2" 2>/dev/null || VIRTUAL_ENV="$T/venv" uv pip install -q "rembg[cpu]" opencv-python-headless
  ln -sf "$T/venv/bin/yt-dlp" "$HOME/.local/bin/yt-dlp"   # YouTube downloads (CC/royalty-free only)
  # VoiceStudio (debpalash/VoiceStudio, local ElevenLabs alternative): own uv venv with CPU torch; backend on :3900
  # via library/tools/voicestudio.sh start. Models download through its API (see library/research/voicestudio.md).
  [ -d "$T/VoiceStudio" ] || git clone -q --depth 1 https://github.com/debpalash/VoiceStudio.git "$T/VoiceStudio"
  [ -x "$T/VoiceStudio/.venv/bin/python" ] || (cd "$T/VoiceStudio" && uv sync -q --locked --no-group cuda --group cpu)
  # VoxCPM2 engine (Apache-2.0, commercial OK, Hindi): package only; its 4.96 GB checkpoint (HF API 2026-10-24) downloads on first use.
  "$T/VoiceStudio/.venv/bin/python" -c "import voxcpm" 2>/dev/null ||
    VIRTUAL_ENV="$T/VoiceStudio/.venv" uv pip install -q "voxcpm>=2.0.3"
  uv cache clean >/dev/null 2>&1 || true
  touch "$T/.heavy-ready"
}

case "${1:-all}" in
  light) light && touch "$T/.light-ready" ;;
  heavy) heavy ;;
  all) light && touch "$T/.light-ready"; heavy ;;
esac
