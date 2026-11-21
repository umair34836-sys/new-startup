# auto-parts-promo (dealer / shop promo from free stock b-roll, 9:16, ~30 s, VO-synced)

First used: Kohinoor (Pakistani auto parts dealer, NPR piston rings), 2026-11-21. Brief, facts and edit log: library/clients/kohinoor/.
Use when the client gives NO footage, logo or site: picture = Mixkit 4K clips (page must say `data-license="videoFree"`,
check each page; look at a contact sheet and skip frames with brand badges/lettering), 9:16 crop scaled down.

1. Fetch clips one by one into `<project>/assets/stock/mk_<id>.mp4` (`https://assets.mixkit.co/videos/<id>/<id>-2160.mp4`).
2. VO: `vs_tts.py script.txt vo.wav --voice <field voice> --lang en --parts parts` -> copy parts/lines.json to assets/vo/.
   Whisper-check each line with language="en" (wcheck_lines.py is hard-coded to "hi").
3. Music (skill music-for-video): find_music -> listen.py -> `music_fit.py --length 30 --check` -> `mix_vo_music.py --vo-at 0.5`.
4. Copy font, GSAP vendor, the 3 SFX; edit SHOTS (scene -> clip, start, x-focus, speed) and copy in the builder;
   `python3 build_kohinoor.py`, then `npx -y hyperframes@0.8.210 check`, `snapshot --at ...`, `render -q high -w 3`.
5. Post: re-encode `format=yuv420p -profile:v high -movflags +faststart`, then remux with
   `-map_metadata -1 -bsf:v filter_units=remove_types=6 -fflags +bitexact`; QA ebur128, blackdetect, watch.py.
Measured 2026-11-21: render 74 s for 30 s; final -16.0 LUFS, 0 black/frozen spans.

## v2 / v3 builders (2026-11-21)
- `build_kohinoor_v2.py`: reference-style 30 s music-only edit (white motion-design act + hype drop act + pin card),
  CC0 "Phonk Remix", beat map from beat_events.py. Needs assets/audio/{bed2.wav,events2.json}.
- `build_kohinoor_v3.py`: copy of a reference edit's timing (cut list from watch.py on the reference) with an exploded
  piston hero. Needs assets/audio/refB_audio.wav (the reference audio was used only because the owner insisted;
  default to a CC0 track).
- Lesson: per-clip `-t <seconds>` can drop a frame per clip; for beat-exact montages use tpad + `-frames:v N -fps_mode cfr`
  and check the concat's frame count before rendering.
