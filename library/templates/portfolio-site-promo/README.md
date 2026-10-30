# portfolio-site-promo (16:9, real website walkthrough synced to a VO)

Made for Bhupendra's portfolio (bhupendra.pages.dev), 2026-10-28; edit log library/clients/heavendeveloper/edit-log-portfolio-v1.md.
1. `NODE_PATH="$(npm root -g)" node record_bhupendra.js OUT` - real browser recording 1920x1080 (zoom 1.25) with cursor,
   click ripples, one mark per VO line; leave-site links are fakeClick only.
2. VO: `vs_tts.py script.txt vo.wav --voice <field voice> --lang en --parts parts` (one line per section).
3. `python3 build_bhupendra.py REC_DIR PARTS_DIR` inside the HyperFrames project (needs assets/vendor gsap, assets/sfx,
   assets/fonts/NotoSerif-Variable.ttf): speed-fits each mark span to its VO line, places the VO, writes screen.mp4,
   times.json, browser frame + side panels + end card. Then music_fit.py (--length = times.json total) and
   mix_vo_music.py into assets/audio/mix.wav, rebuild (or swap the audio src), check, snapshot, render -w 3.
For another site: edit SEG (mark spans), PANELS (the site's own words) and the colours from its CSS variables.
