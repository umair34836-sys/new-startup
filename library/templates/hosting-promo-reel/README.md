# hosting-promo-reel (9:16, ~32 s, VO-synced kinetic scenes)

Made for SkilloraClouds (skilloraclouds.com, a game/VPS hosting company) on 2026-10-24; the owner approved the preview
and the render. `build.py` writes `index.html` + `compositions/{bg,s1..s8}.html` and the audio lanes.

Scenes, each timed to one VO line (times from the VO's word alignment + VO_START): hook over the site's own game art
("MINECRAFT SERVER?" + "BINA LAG KE!" pill) -> logo + wordmark + site tagline -> real control-panel screenshot + 4 spec
chips popping on the spoken words -> "<60 SECONDS" ring -> location cards with flags + "LOWEST PING" -> price card ->
coupon card (code + % off) -> end card (logo, URL pill, Discord). Global layer: dark navy, green glow, moving grid.

To reuse: replace every claim with what the NEW client's site says (capture it with library/tools/web_capture.py and
quote the page), take brand colours from the site's CSS (most frequent hex), download logo/screens/flags from the site,
re-time SCENES and the pop/whoosh lists to the new VO's word timings, then check -> snapshot -> owner preview -> render
(`--workers 3`: 32.5 s rendered in 1 m 38 s here, 2026-10-24).

## build_moradosolution.py (MoradoSolution, 2026-10-24)
Second variant: scene starts come from `assets/vo/lines.json` (per-line [start, end] of the VO, written by
`vs_tts.py --parts`) so re-timing after a new VO needs no hand edits; `SONG=1 python3 build.py` builds the sung version
from `assets/vo/song.wav` + `assets/vo/song_lines.json` (from `align_lyrics.py`) with no extra music bed.
Free VoxCPM2 Hindi VO (one cloned voice) for the 32 s spoken cut, ACE-Step turbo seed 21 (64 s, 110 BPM) for the song cut.

## build_moradosolution_welcome30.py (MoradoSolution WELCOME30 offer reel, 2026-10-24)
30.2 s offer reel, 8 scenes on 8 VO lines: hook "MINECRAFT SERVER? 30% OFF" (on screen at 0 s, confetti burst) ->
coupon card typing WELCOME30 -> Starter ₹199 struck -> ₹139 -> Gold ₹699 struck -> ₹489 -> Hytale art + brand-kit
`brand-offer` starburst -> AMD EPYC 7C13 / NVMe / DDoS chips over the site's rack image -> "SERVER MINUTES MEIN READY"
-> brand-kit `brand-end` (code row added, QR = https://moradosolution.in). Also mounts brand-kit `brand-bug` (moved to
top 290 px for the Reels safe zone). Registry patterns used: `strikethrough-replace` (price strike) and `confetti`
(deterministic burst). Needs in the project: compositions/brand-{offer,end,bug}.html + assets/brand from
`build_brand.py` (brand.json in the scratchpad), assets/img (site images as jpg), sfx (swish-4, punch-heavy,
cash-register, keypress, pop-high, digital-powerup-1, sparkle), music = cc0 desi-eastern--bollywood-groove from 23.85 s.
Checked here: `check` passed; render 1m17s (--workers 3); listen.py -14.4 LUFS, no clipping; watch.py 30.0 real fps;
QR decoded from a rendered frame with OpenCV QRCodeDetector (perc-venv cv2 5.0.0).
v2 (same day): checked against find_skill.py #3598 (Meta Reels margins: top 14 %, bottom 35 %, sides 6 %): "HYTALE BHI!"
moved to top 1060 px; brand-end column changed to flex-start + padding-top 280 px, logo 230 px, QR 250 px so all of it
ends above y=1248. Re-rendered 1m15s, -14.4 LUFS, QR decoded again. brand-end.html edits: code row, these sizes.
