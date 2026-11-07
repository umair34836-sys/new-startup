#!/bin/bash
# mux_tut.sh v1|v2 : render video + mix.wav -> final mp4 (yuv420p, high profile, faststart) + QA
set -e
D=$(dirname "$(readlink -f "$0")"); V=$1; P=$D/proj_$V
REN=$(ls -t $P/.hyperframes/artifacts/renders/*.mp4 2>/dev/null | head -1); [ -n "$REN" ] || REN=$P/render.mp4
OUT=$D/out/${2:-tutorial_$V}.mp4; mkdir -p $D/out
ffmpeg -v error -y -i "$REN" -i $P/mix.wav -map 0:v -map 1:a -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -profile:v high \
  -c:a aac -b:a 192k -shortest -movflags +faststart "$OUT"
ffprobe -v error -select_streams v -show_entries stream=pix_fmt,width,height,r_frame_rate,duration -of csv=p=0 "$OUT"
ffmpeg -i "$OUT" -af ebur128 -f null - 2>&1 | grep -A3 "Integrated" | head -4
echo "$OUT"
