#!/bin/bash
# Hallmark design skill (Nutlope/hallmark, MIT, Together AI). Pinned commit below, cloned 2026-11-02; owner approved
# the install on 2026-11-02. Skill text, references and scripts are in the repo at .claude/skills/hallmark.
# This script adds what git does not carry:
# - the 50 theme preview JPGs (references/themes/*.jpg): .gitignore blocks images, so they come from the pinned commit;
# - puppeteer-core + /usr/bin/chromium for `sloplint --render` (sloplint-render.mjs ignores CHROME_PATH).
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SK="$ROOT/.claude/skills/hallmark"
REV=4f6a46c6dc325d40ab268c93e25c7b96676ebccd
[ -d "$SK" ] || { echo "hallmark skill folder missing: $SK"; exit 1; }
if ! ls "$SK"/references/themes/*.jpg >/dev/null 2>&1; then
  tmp=$(mktemp -d)
  if git clone -q https://github.com/Nutlope/hallmark.git "$tmp/h" && git -C "$tmp/h" checkout -q "$REV"; then
    cp "$tmp"/h/skills/hallmark/references/themes/*.jpg "$SK/references/themes/"
  fi
  rm -rf "$tmp"
fi
npm ls -g puppeteer-core >/dev/null 2>&1 || npm i -g -s puppeteer-core
[ -e /usr/bin/chromium ] || { [ -x /opt/pw-browsers/chromium ] && ln -s /opt/pw-browsers/chromium /usr/bin/chromium; }
exit 0
