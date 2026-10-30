#!/usr/bin/env bash
# Makes portal-update.zip: program files only (no config.php, no storage), plus README-UPDATE.md.
# Extract it over the live folder (/home/talkembe/editor.firecraft.fun/) to update without touching data.
set -euo pipefail
cd "$(dirname "$0")/.."
OUT="$(realpath -m "${1:-portal-update.zip}")"
rm -f "$OUT"
cp portal/README-UPDATE.md /tmp/README-UPDATE.md.$$
(cd /tmp && mv README-UPDATE.md.$$ README-UPDATE.md && zip -q "$OUT" README-UPDATE.md && rm README-UPDATE.md)
zip -qr "$OUT" portal/.htaccess portal/app portal/public -x '*/.DS_Store'
echo "$OUT: $(du -h "$OUT" | cut -f1)"
