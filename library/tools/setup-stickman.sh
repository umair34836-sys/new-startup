#!/bin/bash
# Stickman Video Director skill (kaomei/stickman-video-director, MIT). Pinned commit below, cloned 2026-11-02; the owner
# asked for the install on 2026-11-02. Skill text, references, scripts and PNG assets are in the repo at
# .claude/skills/directing-stickman-videos. This script adds what git does not carry:
# - 3 reference media files that .gitignore blocks (b1 approved mp4 + 2 contact-sheet/style-board JPGs), from the pinned commit;
# - the Autopilot runtime dependency (@napi-rs/canvas via `npm ci` in the skill folder; node_modules is git-ignored).
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SK="$ROOT/.claude/skills/directing-stickman-videos"
REV=d19705dea434626d4fc6e651e24cdf23c7eba156
MEDIA="assets/b1/approved-2026-10-23.mp4 assets/b1/approved-2026-10-24-longform-contact-sheet.jpg assets/b2/approved-style-board.jpg"
[ -d "$SK" ] || { echo "stickman skill folder missing: $SK"; exit 1; }
missing=0; for f in $MEDIA; do [ -f "$SK/$f" ] || missing=1; done
if [ "$missing" = 1 ]; then
  tmp=$(mktemp -d)
  if git clone -q --filter=blob:none --no-checkout https://github.com/kaomei/stickman-video-director.git "$tmp/s" &&
     git -C "$tmp/s" checkout -q "$REV" -- $(for f in $MEDIA; do echo "skills/directing-stickman-videos/$f"; done); then
    for f in $MEDIA; do cp "$tmp/s/skills/directing-stickman-videos/$f" "$SK/$f"; done
  fi
  rm -rf "$tmp"
fi
[ -d "$SK/node_modules/@napi-rs/canvas" ] || (cd "$SK" && npm ci -s --no-audit --no-fund)
exit 0
