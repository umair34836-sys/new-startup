#!/bin/bash
# Sets up one HyperFrames project per (language, format) in the scratchpad for build_goods.py (GOOD's, 2026-11-02).
#   bash make_projects.sh <work dir>   (needs <work>/shared/{img,sfx,fonts,vendor}, <work>/rec916, <work>/rec169,
#                                       <work>/mix/<lang>.wav and <work>/vo/<lang>_parts/lines.json)
set -e
W=$1; T=$(cd "$(dirname "$0")" && pwd)
for lang in en hi; do for fmt in portrait landscape; do
  d=$W/proj-$lang-$fmt; mkdir -p $d/assets/{vo,audio}
  for x in img sfx fonts vendor; do ln -sfn $W/shared/$x $d/assets/$x; done
  ln -sfn $W/$([ $fmt = portrait ] && echo rec916 || echo rec169) $d/rec
  cp $W/vo/${lang}_parts/lines.json $d/assets/vo/lines.json
  cp $W/mix/$lang.wav $d/assets/audio/mix.wav
  cp $T/build_goods.py $d/
  (cd $d && LANG_=$lang FMT=$fmt TOTAL=${TOTAL:-46} python3 build_goods.py | head -1)
done; done
