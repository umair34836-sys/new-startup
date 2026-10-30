#!/usr/bin/env bash
# Makes portal-upload.zip for cPanel: README-FIRST.md (install steps for a person or an AI browser agent),
# app/, public/, storage/ (empty, plus the Android app if it was built), docs. No tests, no secrets.
set -euo pipefail
cd "$(dirname "$0")/.."
OUT="$(realpath -m "${1:-portal-upload.zip}")"
TMP="$(mktemp -d)"
rm -f "$OUT"
mkdir -p "$TMP/portal"
cp portal/README-FIRST.md "$TMP/README-FIRST.md"
cp -r portal/.htaccess portal/app portal/public portal/storage portal/README.md portal/ARCHITECTURE.md portal/config.example.php "$TMP/portal/"
rm -rf "$TMP/portal/storage/files/"* "$TMP/portal/storage/chunks/"* "$TMP/portal/storage/sessions" "$TMP/portal/storage/app" \
  "$TMP/portal/storage/install-key.txt" "$TMP/portal/config.php"
touch "$TMP/portal/storage/files/.keep" "$TMP/portal/storage/chunks/.keep"
# The native app (latest build), so /app/download works right after install.
APK="$(ls -t portal/mobile/build/MrCopper804-v*.apk 2>/dev/null | grep -v emulatortest | head -1 || true)"
if [ -n "$APK" ]; then
  mkdir -p "$TMP/portal/storage/app"
  cp "$APK" "$TMP/portal/storage/app/app.apk"
  echo "included $(basename "$APK") as storage/app/app.apk"
fi
(cd "$TMP" && zip -qr "$OUT" README-FIRST.md portal)
rm -rf "$TMP"
echo "$OUT: $(du -h "$OUT" | cut -f1)"
