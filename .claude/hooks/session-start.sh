#!/bin/bash
# Fresh cloud containers start empty: fetch HyperFrames' headless Chrome and the quick CLIs now, and
# install the music/AI-song stack in the background (log: /home/user/tools/setup.log).
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

# uv tools (agent-reach) live in ~/.local/bin: put it on PATH for the session's shells.
[ -n "${CLAUDE_ENV_FILE:-}" ] && echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$CLAUDE_ENV_FILE"

TOOLS="$CLAUDE_PROJECT_DIR/library/tools"
(cd "$CLAUDE_PROJECT_DIR/video" && npx -y hyperframes@0.8.188 browser ensure >/dev/null)
bash "$TOOLS/setup-all.sh" light >/dev/null 2>&1 || echo "light tool setup failed; rerun library/tools/setup-all.sh light"

if [ ! -f /home/user/tools/.heavy-ready ]; then
  mkdir -p /home/user/tools
  nohup setsid bash "$TOOLS/setup-all.sh" heavy >> /home/user/tools/setup.log 2>&1 < /dev/null &
fi
