#!/bin/bash
# mux_tut.sh v1|v2 : render video + mix.wav -> final mp4 (yuv420p, high profile, faststart) + QA
set -e
D=$(dirname "$(readlink -f "$0")"); V=$1; P=$D/proj_$V
REN=$(ls -t $P/renders/*.mp4 2>/dev/null | head -1); [ -n "$REN" ] || REN=$P/render.mp4
OUT=$D/out/${2:-tutorial_$V}.mp4; mkdir -p $D/out
# phone + PC safe: H.264 High@4.1, 4:2:0, AAC-LC stereo 48 kHz, faststart (CLAUDE.md "Your device cant play this file format")
ffmpeg -v error -y -i "$REN" -i $P/mix.wav -map 0:v -map 1:a -c:v libx264 -crf 19 -preset medium -pix_fmt yuv420p -profile:v high -level 4.1 \
  -x264-params keyint=60:min-keyint=30 -tag:v avc1 -c:a aac -b:a 192k -ac 2 -ar 48000 -shortest -movflags +faststart "$OUT"
ffprobe -v error -select_streams v -show_entries stream=codec_name,profile,level,pix_fmt,width,height,r_frame_rate -of csv=p=0 "$OUT"; ffprobe -v error -select_streams a -show_entries stream=codec_name,profile,channels,sample_rate -of csv=p=0 "$OUT"
ffmpeg -i "$OUT" -af ebur128 -f null - 2>&1 | grep -A3 "Integrated" | head -4
echo "$OUT"
