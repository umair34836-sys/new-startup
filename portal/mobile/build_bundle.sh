#!/usr/bin/env bash
# Live update: zips www/ for the app's updater. Upload the zip in Admin -> Settings -> "Live update bundle",
# then set the same version there. Every app downloads it by itself (no reinstall).
#   VERSION=1.0.1 bash build_bundle.sh
set -euo pipefail
cd "$(dirname "$0")"
: "${VERSION:?set VERSION=x.y.z (higher than the last one)}"
VERSION="$VERSION" bash build_www.sh
rm -f "bundle-$VERSION.zip"
(cd www && zip -qr "../bundle-$VERSION.zip" .)
echo "bundle-$VERSION.zip $(du -h "bundle-$VERSION.zip" | cut -f1) sha256 $(sha256sum "bundle-$VERSION.zip" | cut -c1-64)"
