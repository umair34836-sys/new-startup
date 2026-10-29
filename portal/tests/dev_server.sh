#!/usr/bin/env bash
# Starts a throw-away portal on http://127.0.0.1:${PORT:-8088} with SQLite in $DIR (default: a temp folder).
# PHP limits mirror the owner's host (2 MB per file, 8 MB per request).
set -euo pipefail
HERE="$(cd "$(dirname "$0")/.." && pwd)"
DIR="${DIR:-$(mktemp -d)}"
PORT="${PORT:-8088}"
mkdir -p "$DIR/storage/files" "$DIR/storage/chunks"
cat > "$DIR/config.php" <<PHP
<?php return ['db_driver' => 'sqlite', 'db_path' => '$DIR/portal.sqlite', 'storage_dir' => '$DIR/storage', 'base_path' => '', 'timezone' => 'Asia/Karachi', 'mail_log' => '$DIR/mail.log'];
PHP
PORTAL_CONFIG="$DIR/config.php" php "$HERE/tests/seed.php" "${ADMIN_EMAIL:-owner@example.com}" "${ADMIN_PASSWORD:-ownerpass123}" "${BRIDGE_TOKEN:-pb_testtoken}"
echo "DIR=$DIR"
exec env PORTAL_CONFIG="$DIR/config.php" php -d upload_max_filesize=2M -d post_max_size=8M -d memory_limit=128M \
  -S 127.0.0.1:$PORT -t "$HERE/public" "$HERE/public/index.php"
