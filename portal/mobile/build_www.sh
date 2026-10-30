#!/usr/bin/env bash
# Assembles mobile/www (the app's built-in screens) from src/ plus the website's CSS, GSAP and icons.
#   API=https://editor.firecraft.fun VERSION=1.0.0 bash build_www.sh
set -euo pipefail
cd "$(dirname "$0")"
API="${API:-https://editor.firecraft.fun}"
VERSION="${VERSION:-1.0.0}"
PUB=../public
rm -rf www && mkdir -p www/vendor www/icons
cat "$PUB/assets/app.css" src/app-extra.css > www/app.css
cp src/app.js www/app.js
sed "s#__API__#$API#g" src/index.html > www/index.html
cp "$PUB/assets/vendor/gsap-3.14.2.min.js" www/vendor/
cp "$PUB/assets/icons/logo.png" "$PUB/assets/icons/logo-480.png" "$PUB/assets/icons/icon-192.png" www/icons/
cat > www/config.js <<JS
window.PORTAL_API = '$API';
window.APP_BUNDLE_VERSION = '$VERSION';
JS
echo "www built: API=$API version=$VERSION"
