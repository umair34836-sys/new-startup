#!/bin/bash
# run_ad.sh NN [stage]  : stage = check (whisper + build + snapshot) | render (render + finalize + deliver) | all
set -e
ID=$1; STAGE=${2:-all}
S=/tmp/claude-0/-home-user-new-startup/9d153c96-dfa4-5839-b190-6129735fe20f/scratchpad; R=/home/user/new-startup
D=$S/ads/$ID; P=$D/proj
if [ "$STAGE" != "render" ]; then
  mkdir -p $P/assets/{vendor,fonts,img/icons,sfx}
  cp $R/library/vendor/gsap-3.14.2.min.js $P/assets/vendor/
  cp $R/library/fonts/*.ttf $P/assets/fonts/
  cp $S/tk/shots/*.jpg $P/assets/img/; cp $S/tk/p9/assets/img/logo.svg $P/assets/img/; cp $S/tk/p9/assets/img/icons/*.svg $P/assets/img/icons/
  [ -f $P/assets/img/icons/gmail.svg ] || sed 's#<svg #<svg fill="\#EA4335" #' $S/tk/icons/gmail.svg > $P/assets/img/icons/gmail.svg
  for f in transition/whoosh-fast-0.3s transition/swish-1 transition/swish-4 transition/whoosh-up-0.6s pop/pop-high pop/pop-low pop/plop impact/impact-punch ui/confirm-1 glitch/glitch-short typing/typing-keyboard-fast; do cp $R/library/sfx/$f.mp3 $P/assets/sfx/; done
  cp $R/video/hyperframes.json $R/video/meta.json $R/video/package.json $P/
  LANG=$(python3 -c "import json;print(json.load(open('$D/spec.json'))['lang'])")
  echo "--- whisper ($LANG)"
  /home/user/tools/venv/bin/python -I -c "
import whisper,warnings; warnings.filterwarnings('ignore')
m=whisper.load_model('small'); r=m.transcribe('$D/vo.mp3',language='$LANG',condition_on_previous_text=False)
for s in r['segments']: print(f\"{s['start']:5.1f} {s['text']}\")" 2>/dev/null
  python3 $R/library/templates/ad-pack/build_ad.py $D/spec.json --out $P
  cd $P && npx -y hyperframes@0.8.210 check 2>&1 | grep -E "error\(s\)|Check passed|Check failed" | tail -2
  T=$(python3 -c "
import json;t=json.load(open('$P/timing.json'));print(','.join(str(round((a+b)/2+0.4,1)) for a,b,_ in t['lines']))")
  npx -y hyperframes@0.8.210 snapshot --at $T 2>&1 | grep -oE "/tmp\S+contact-sheet[^ ]*\.jpg" | head -1 > $D/sheet.txt; cat $D/sheet.txt
fi
if [ "$STAGE" != "check" ]; then
  cd $P && npx -y hyperframes@0.8.210 render -q high -w 3 -o $P/render.mp4 > $P/render.log 2>&1
  O=$S/ads/out/talkember-ad-$ID.mp4; mkdir -p $S/ads/out
  ffmpeg -v error -y -i $P/render.mp4 -map 0 -c:v copy -bsf:v filter_units=remove_types=6 -af "volume=2dB,alimiter=limit=0.85:level=false" -c:a aac -b:a 192k -flags:a +bitexact -map_metadata -1 -metadata title="talkember ad $ID" -metadata artist="MrCopper804" -fflags +bitexact -flags:v +bitexact -movflags +faststart $O
  echo "final: $(ffprobe -v error -show_entries stream=pix_fmt -show_entries format=duration -of csv=p=0 $O | tr '\n' ' ') $(ffmpeg -i $O -af ebur128 -f null - 2>&1 | grep -A6 Summary | grep 'I:') black=$(ffmpeg -i $O -vf blackdetect=d=0.3:pix_th=0.05 -an -f null - 2>&1 | grep -c black_start) $(du -m $O | cut -f1)MB"
  NOTE=$(python3 -c "
import json;s=json.load(open('$D/spec.json'));print(f\"Ad $ID: {s['title']} ({'English' if s['lang']=='en' else 'Hinglish'}), 9:16\")")
  cd $R && python3 portal/bridge/portal_bridge.py deliver 1 $O --note "$NOTE" 2>&1 | tail -4 | tr -d '\n'; echo
fi
