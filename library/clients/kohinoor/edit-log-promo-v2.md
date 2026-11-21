# Kohinoor promo v2: edit log (2026-11-21)

Owner: two TikTok links "as an inspiration lelo and once again is inspiration k style me bana do".
Builder: library/templates/auto-parts-promo/build_kohinoor_v2.py. Facts: site-data.md (same as v1).

## References (downloaded with yt-dlp into the scratchpad only; nothing from them is in the video)
- Ref 1 (TikTok id 7685534272882576642, 16:9, 10.0 s, "Pinterest Creative Concept" motion design): white set, kinetic
  words with blur-in ("Need some ideas?" / "We have solution"), red circle reveal, search bar typed, swatch/card grid,
  card with round icon buttons, "Pinned" button press, red gradient end card. listen.py: music only, 0 voice.
- Ref 2 (TikTok id 7699154533766712594, 720x960, 17.1 s, "Cooler Edit", After Effects): exploded view of an object
  (parts fly apart), whip-pans with motion blur, beat cuts, letterbox bars, red light streaks, glowing name low in
  frame, glitch logo end. listen.py: 92.6 BPM, music only, 0 voice.
- Decision: music only (both refs have no voice); v1's VO not reused. Can be added back if the owner wants.

## Music (skill music-for-video)
- find_music.py "phonk hype edit beat" --client --no-vo --drop: HoliznaCC0 "Phonk Remix" (CC0, library/music/cc0):
  92.0 BPM = ref 2's tempo (92.6), steady grid (CV 0.013), quiet intro 0-10.4 s then drop/chorus 10.4-18.9, break
  18.9-31.3 (listen.py). Loyalty Freak tracks ranked higher but are happy/bright (wrong mood, as in v1).
- music_fit --length 30 --end fade --fade 2.5 --lufs -15: source 0-30 s, no joins, fade from the downbeat at 26.73 s.
- beat_events.py: strong kick 10.48 s = the drop; snares >= 0.6 at 12.43, 14.07, 14.40, 14.72, 15.70, 17.65.

## Structure (acts follow the track's sections)
- 0-10.48 (quiet intro, ref 1 grammar): whole question on frame 0 (thumbnail; first try showed a lone "Need"),
  "We have the solution." blur-in per word, red circle on the 5.84 s strong kick -> piston badge + name, search bar
  typed "genuine piston rings", click on the search icon at 10.18.
- 10.48-18.92 (drop, ref 2 grammar): Mixkit shots cut on strong kicks/snares (10.48, 11.48, 12.46, 14.07, 15.71,
  17.02), 6% kick punches, white flash on 3 strong kicks only, whip-pans into 11.48 and 17.02, letterbox bars on 2
  shots, red edge light, glowing "Kohinoor" low in frame, RGB split on the 6 snares (ffmpeg post), grain.
  Exploded piston (generic illustration: top ring, second ring, oil ring) with one ring flying out per snare
  14.07/14.40/14.72 and seating on the 15.71 kick.
- 18.92-26.5 (break, ref 1): pin-style card (engine frame), round icons, NPR / Nippon Piston Ring / Japan, since 1934,
  "Authorized NPR dealer" button press on the 23.21 kick.
- 26.5-30 (fade): name letters glitch in over red-tinted highway footage, credit "Edited by MrCopper804".
- SFX each file once: pop-low, typing-keyboard-fast, mouse-click, car-engine-start (drop), swish-1/4/7 (one per ring),
  metal-hit (rings seat), whoosh-up-0.6s, confirm-1 (button), glitch-short (end name).

## Fixes from snapshots / lint
- First frame showed only "Need" -> all words visible at 0 s.
- Highway shot from 2.0 s showed the trailer lettering close up and the headline sat on the bright sky -> source start
  5.0 s + dark band behind the text. "Every ring." (a claim) -> "Genuine NPR piston rings."
- Lint: CSS transform + GSAP scale/y conflict (#dot, letterbox bars) -> gsap.set; repeated fromTo on one element needs
  immediateRender:false after the first; a repeated white-flash fromTo rendered its 0.9 "from" before the first flash
  (text_occluded at 1.667 s) -> tl.set + tl.to.

## QA (measured here 2026-11-21)
- Render -q high -w 3: 47 s. Final 1080x1920 H.264 High yuv420p 30 fps faststart, 30.0 s, x264/Lavf strings 0.
- ebur128 -14.9 LUFS, LRA 2.1 LU, peak -1.6 dBFS; blackdetect d=0.05: 0; watch.py real 30.0 fps, 0 black, 0 frozen.
- Delivered with SendUserFile 2026-11-21.
