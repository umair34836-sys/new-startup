# exchange-promo (currency / crypto exchange promo, EN + Hinglish, 9:16 + 16:9, ~46 s)

First used: GOOD's (goodss.store), 2026-11-02. Facts: library/clients/goods/site-data.md. Edit log: clients/goods/edit-log-promo-v1.md.

1. `flow_goods.js <out> portrait|landscape`: records the real site (hero, rate tabs PKR/CRYPTO/BINANCE GIFT, calculator
   PKR -> crypto with an amount typed, How It Works, contact channels) with screen_recorder.js. Portrait 1080x1920 zoom 1.4,
   landscape 1920x1080 zoom 1.35. The exchange form is never filled or submitted.
   The Discord web invite page asks visitors to register (seen 2026-11-02), so the Discord scene is a card made of the
   client's banner GIF + the member count from the invite API instead of a recording.
2. VO: `vs_tts.py script.txt vo.wav --voice <field voice> --lang en|hi --parts <dir>`; Whisper-check each line.
3. Music: skill music-for-video (find_music.py -> listen.py -> music_fit.py -> mix_vo_music.py), VO placed at 0.5 s.
4. `make_projects.sh <work>` builds 4 projects; in each: `npx -y hyperframes@0.8.210 check`, snapshot, render -w 3.
5. Post: loudness to -15/-16 LUFS, `format=yuv420p`, faststart, watermark.py for previews, watch.py/listen.py/blackdetect.

Builder notes: per-scene SEG table (recording, from, to, optional zoom/focus crop for 16:9 where cards are small);
copy per language in the T table (Roman Hinglish on screen, Devanagari only for TTS); Hallmark floor: no eyebrow or
tracked-caps labels, headlines one colour, expo.out easing, gold bar as the only accent, real material behind cards.
6. `post.sh <variant> <name>`: final (metadata off, yuv420p High, faststart) + watermark.py preview + QA; then remux every
   delivery file with `-map_metadata -1 -bsf:v filter_units=remove_types=6 -fflags +bitexact` (no x264/Lavf strings).
Measured 2026-11-02: render 2-3 min per 48.7 s video (-w 3); post ~2 min per variant; all 4 at -16.0 LUFS, 0 black spans.
