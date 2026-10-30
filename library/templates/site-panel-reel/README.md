# site-panel-reel (9:16, ~60 s, real site recordings under kinetic badges)

First used: AethelGrid (aethelgrid.cloud + panel gp.aethelgrid.cloud), 2026-10-28.
1. `flow_aethelgrid.js`: records each real page with library/tools/screen_recorder.js at 1080x1920, CSS zoom 1.4
   (desktop layout ~770 px wide, no overflow; zoom 2.5 broke the layout: media queries still see 1080 px). Cursor +
   ripple on every click; only in-page toggles and "Copy" are clicked. The recorder's `scrollTo` takes CSS only, so the
   flow has its own `scroll()` for Playwright selectors (`:text(...)`, `:has-text(...)`).
   `NODE_PATH="$(npm root -g)" node flow_aethelgrid.js $PWD/rec [shot ...]`
2. VO: `vs_tts.py --voice <field voice> --parts`, Whisper-check (`wcheck_lines.py`), redo weak lines with `--seed 21`,
   join the chosen parts with 0.9 s gaps (60 s target) -> assets/vo/{vo.wav,lines.json}.
3. Music: music_fit.py --length 60 --start <downbeat of the full section>; VO placed at 0.6 s (adelay + apad) ->
   mix_vo_music.py -> assets/audio/mix.wav (one audio track; whoosh/pop/click SFX lanes on top).
4. `seg.json` (copy: seg_aethelgrid.json) = scene -> [recording, from s, to s]; `build_aethelgrid.py` speed-fits each
   span to its VO line, concatenates screen.mp4, writes the overlay compositions; click sounds land on the real clicks.
5. check -> snapshot -> render --workers 3 -> loudness fix -> watch.py / listen.py / blackdetect -> watermark.py.

AethelGrid numbers (measured here 2026-10-28): 7 recordings 7.5-23.5 s; VO 55.5 s (explainer-pro, 13 lines);
span speeds 0.95-2.2x; render -w 3 2m55s; render audio -17.7 LUFS -> volume +2.4 dB + alimiter 0.79 -> -15.3 LUFS,
true peak -1.6 dBTP (limit 0.85 left -0.9 dBTP); watch.py 30.0 real fps, 0 gaps; "frozen" spans = still screen
moments (expected); a 0.1 s dark blip at the hook->site cut came from a fade-out on the hook card (removed).
