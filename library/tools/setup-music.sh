#!/bin/bash
# One-time setup for the music tools in a fresh cloud container:
# FluidSynth + the FluidR3 GM SoundFont (apt), mido (pip), Magenta.js (npm).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"

if ! command -v fluidsynth >/dev/null || [ ! -f /usr/share/sounds/sf2/FluidR3_GM.sf2 ]; then
  apt-get update -qq
  DEBIAN_FRONTEND=noninteractive apt-get install -y -qq fluidsynth fluid-soundfont-gm
fi
python3 -c "import mido" 2>/dev/null || pip install -q mido
python3 -c "import numpy" 2>/dev/null || pip install -q numpy
(cd "$HERE/magenta" && [ -d node_modules/@magenta/music ] || npm install --silent)
echo "music tools ready"
