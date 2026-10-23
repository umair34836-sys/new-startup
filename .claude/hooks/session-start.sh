#!/bin/bash
# Fresh cloud containers start empty: fetch HyperFrames' headless Chrome now, and install every other
# tool (library/tools/setup-all.sh) in the background so the session starts at once.
# Log: /home/user/tools/setup.log; done flags: /home/user/tools/.light-ready, .heavy-ready.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

# uv tools (agent-reach) and the yt-dlp link live in ~/.local/bin: put it on PATH for the session's shells.
[ -n "${CLAUDE_ENV_FILE:-}" ] && echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$CLAUDE_ENV_FILE"

(cd "$CLAUDE_PROJECT_DIR/video" && npx -y hyperframes@0.8.188 browser ensure >/dev/null)

if [ ! -f /home/user/tools/.heavy-ready ] || [ ! -f /home/user/tools/.light-ready ]; then
  mkdir -p /home/user/tools "$HOME/.local/bin"
  nohup setsid bash "$CLAUDE_PROJECT_DIR/library/tools/setup-all.sh" all >> /home/user/tools/setup.log 2>&1 < /dev/null &
fi
