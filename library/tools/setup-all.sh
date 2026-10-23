#!/bin/bash
# Install every tool this repo uses into a fresh cloud container, skipping what is already there.
#   bash library/tools/setup-all.sh light   # quick CLIs (~1 min): Agent-Reach, graft
#   bash library/tools/setup-all.sh heavy   # music + AI song stack and its model weights (~15 min, ~17 GB)
# The SessionStart hook runs "light" in the foreground and "heavy" in the background, logging to
# /home/user/tools/setup.log and touching /home/user/tools/.heavy-ready when it finishes.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
T=/home/user/tools
export PATH="$HOME/.local/bin:$PATH"
mkdir -p "$T"

light() {
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
  touch "$T/.heavy-ready"
}

case "${1:-all}" in
  light) light ;;
  heavy) heavy ;;
  all) light && heavy ;;
esac
