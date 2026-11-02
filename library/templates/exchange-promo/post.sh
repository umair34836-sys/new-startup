#!/bin/bash
# post one render: clean final (metadata stripped, yuv420p high, faststart) + watermarked preview, then QA
# (scratchpad paths; strip pass: see README step 5)
G=/tmp/claude-0/-home-user-new-startup/3d4f3bcc-f0b8-52d3-9235-43bef2acf917/scratchpad/goods/out; v=$1; name=$2
ffmpeg -v error -y -i $G/raw-$v.mp4 -map_metadata -1 -map 0:v -map 0:a -c:v libx264 -crf 17 -preset slow -profile:v high -vf format=yuv420p -c:a aac -b:a 192k -movflags +faststart $G/final/$name.mp4
nice python3 /home/user/new-startup/library/tools/watermark.py $G/final/$name.mp4 $G/preview/tmp-$name.mp4 --text "Edited by MrCopper804" --tag "PREVIEW" >/dev/null 2>&1
ffmpeg -v error -y -i $G/preview/tmp-$name.mp4 -c:v libx264 -crf 18 -preset slow -profile:v high -vf format=yuv420p -c:a copy -movflags +faststart $G/preview/$name-PREVIEW.mp4 && rm $G/preview/tmp-$name.mp4
for f in $G/final/$name.mp4 $G/preview/$name-PREVIEW.mp4; do
 echo "$(basename $f): $(ffprobe -v error -select_streams v -show_entries stream=pix_fmt,profile,width,height -of csv=p=0 $f) $(ffprobe -v error -show_entries format=duration -of csv=p=0 $f)s $(du -h $f | cut -f1)"
done
ffmpeg -i $G/final/$name.mp4 -af ebur128=peak=true -vn -f null - 2>&1 | grep -A20 Summary | grep -E "I:|Peak:" | tr -s ' ' | tr '\n' ' '; echo
ffmpeg -i $G/final/$name.mp4 -vf blackdetect=d=0.05:pix_th=0.05 -an -f null - 2>&1 | grep -c black_start | sed 's/^/black spans: /'
ffprobe -v error -show_entries format_tags -of compact $G/final/$name.mp4
