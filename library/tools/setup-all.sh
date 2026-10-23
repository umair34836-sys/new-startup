#!/bin/bash
# Install every tool this repo uses into a fresh cloud container, skipping what is already there.
#   bash library/tools/setup-all.sh light   # quick (~1 min): ffmpeg, PIL/numpy/mido/pyworld, Agent-Reach, graft
#   bash library/tools/setup-all.sh heavy   # music + AI song stack and its model weights (~15 min, ~17 GB)
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
}

heavy() {
  bash "$HERE/setup-music.sh"
  bash "$HERE/setup-ai-song.sh"
  # Weights: ACE-Step turbo + VAE + text encoder + LM (huggingface, non-Xet path) and Whisper small.
  cd "$T/ACE-Step-1.5" && HF_HUB_DISABLE_XET=1 "$T/venv/bin/python" -c \
    "from acestep.model_downloader import ensure_main_model as e; print(e(prefer_source='huggingface'))"
  "$T/venv/bin/python" -c "import whisper; whisper.load_model('small'); print('whisper small ready')"
  ln -sf "$T/venv/bin/yt-dlp" "$HOME/.local/bin/yt-dlp"   # YouTube downloads (CC/royalty-free only)
  touch "$T/.heavy-ready"
}

case "${1:-all}" in
  light) light && touch "$T/.light-ready" ;;
  heavy) heavy ;;
  all) light && touch "$T/.light-ready"; heavy ;;
esac
