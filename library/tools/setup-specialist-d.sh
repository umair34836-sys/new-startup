#!/usr/bin/env bash
# Python packages for the Urdu captions + client brand kit tools (idempotent).
#   urdu_captions.py --check : fonttools        brand_from_logo.py : numpy, pillow
#   build_brand.py QR code   : qrcode (BSD, 8.2 tested 2026-10-24)
# Fonts are in library/fonts (no download needed).
set -e
python3 - <<'PY' 2>/dev/null && { echo "specialist-d: already installed"; exit 0; }
import fontTools, numpy, PIL, qrcode
PY
pip install -q --break-system-packages fonttools numpy pillow qrcode 2>/dev/null || pip install -q fonttools numpy pillow qrcode
echo "specialist-d: installed fonttools numpy pillow qrcode"
