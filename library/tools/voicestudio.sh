#!/bin/bash
# VoiceStudio backend (debpalash/VoiceStudio, AGPL-3.0): local voice cloning / voice design / TTS / transcription.
#   bash library/tools/voicestudio.sh start   # starts the API on http://127.0.0.1:3900 (OpenAPI at /openapi.json, MCP at /mcp)
#   bash library/tools/voicestudio.sh stop | status
# Installed by setup-all.sh heavy into /home/user/tools/VoiceStudio. CPU only here. Model licences matter:
# see library/research/voicestudio.md before using a voice in a client or paid video.
VS=/home/user/tools/VoiceStudio
LOG=/home/user/tools/voicestudio-backend.log
case "${1:-status}" in
  start)
    curl -sf http://127.0.0.1:3900/health && exit 0
    cd "$VS" && OMNIVOICE_DEVICE=cpu nohup setsid "$HOME/.local/bin/uv" run --no-sync uvicorn main:app \
      --app-dir backend --host 127.0.0.1 --port 3900 >> "$LOG" 2>&1 &
    for _ in $(seq 1 60); do curl -sf http://127.0.0.1:3900/health && exit 0; sleep 3; done
    echo "backend did not start, see $LOG" >&2; exit 1 ;;
  stop) pkill -f "uvicorn main:app --app-dir backend" && echo stopped ;;
  status) curl -sf http://127.0.0.1:3900/health || echo "not running" ;;
esac
