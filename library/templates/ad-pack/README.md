# ad-pack: many short ads for one product, each in a different edit style

Made 2026-11-10 (Personal session) for the owner's app (app.talkember.site / video.talkember.site):
20 ads, 9:16, 15-22 s each, 15 Hinglish + 5 English, one topic and one style per ad.

## Files
- `build_ad.py SPEC.json --out PROJECT [--format 9x16|16x9]`: builds one HyperFrames project from a spec.
  20 styles `s01`..`s20`; each sets background, palette, fonts, headline animation, scene move, cut overlay,
  screenshot frame and layout, so no two ads look alike.
- `specs_talkember.py`: the 20 specs used (topic, language, style, voice, CC0 track, lines with spoken text,
  on-screen headline, accent words, visual). Running it writes `NN/spec.json` + `NN/say.txt`.
- `run_ad.sh NN check|render|all`: copy assets, Whisper-check the VO, build, `hyperframes check`, snapshot
  sheet; then render, finalize (yuv420p, faststart, metadata stripped) and deliver to the portal order.
  Paths inside are from that session's scratchpad: change them for a new job.

## How timing works
Line times come from the VO itself: `silencedetect=n=-36dB:d=0.14`, the silence nearest each line's share of
the characters. VO starts at 0.25 s; total = VO + 1.95 s. Music: `music_fit.py` + `mix_vo_music.py`.

## Measured here 2026-11-10
- 20 renders (`-q high -w 3`): 15.1-21.7 s long, -13.9 to -16.2 LUFS, 0 black spans, 3-27 MB, all yuv420p.
- VO: ElevenLabs `eleven_v4`, 1 take per ad (owner asked for ElevenLabs), 172-256 credits each, 4,156 total.
  Whisper small heard every line; it often spells the URL wrong ("talkamber"), so the URL is always on screen.
- Line 3 of ad 12 landed about 1.2 s late (two short pauses inside one line): look at the Whisper times
  beside the "lines at" list after each check.

## Fixes found in the snapshot sheets
- Dark brand icon on a dark chip was invisible: chip icons now sit on a white rounded tile.
- `split` background with a light lower panel hid the light headline: panel is dark with an accent edge.
- `halftone` palette (#00b4d8) failed contrast in `hyperframes check` (2.3-2.9:1): now #0068a8 / #023e8a.
- `mono` progress bar crossed the end-card icon row: moved to 95.5% of the height.

## Rules kept
Only facts from the site and the owner's screenshots; e-mail fields blurred; no eyebrow labels or tracked
caps; client-visible portal notes and file names carry no tool words (`talkember-ad-NN.mp4`).
