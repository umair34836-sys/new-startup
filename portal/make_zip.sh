#!/usr/bin/env bash
# Makes portal-upload.zip for cPanel: app/, public/, storage/ (empty), docs. No tests, no APK build, no secrets.
set -euo pipefail
cd "$(dirname "$0")/.."
OUT="${1:-portal-upload.zip}"
rm -f "$OUT"
zip -qr "$OUT" portal/app portal/public portal/storage portal/README.md portal/ARCHITECTURE.md portal/config.example.php \
  -x 'portal/storage/files/*' -x 'portal/storage/chunks/*' -x 'portal/storage/install-key.txt' -x 'portal/config.php' -x '*/.DS_Store'
# Keep the empty storage folders (zip drops empty dirs otherwise).
zip -q "$OUT" portal/storage/files/.keep portal/storage/chunks/.keep
echo "$OUT: $(du -h "$OUT" | cut -f1)"
