#!/bin/bash
# Fetch the headless Chrome HyperFrames renders with; fresh cloud containers don't have it.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "$CLAUDE_PROJECT_DIR/video"
npx -y hyperframes@0.8.188 browser ensure >/dev/null
