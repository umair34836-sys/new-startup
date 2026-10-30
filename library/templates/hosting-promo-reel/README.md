# hosting-promo-reel (9:16, ~44 s in v3, VO-synced kinetic scenes)

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
v3 (2026-10-24): spec chip/VO "AMD EPYC 9" (client's wording via the owner; skilloraclouds.com/minecraft itself shows
"AMD EPYC" for Budget/Standard India and Premium India/Singapore, "AMD Ryzen" for Premium Dubai, checked 2026-10-24) and
a new scene `s6b` after the price: "Budget & Standard plans LIMITED" + Discord / website cards. Scene starts live in
`SCENES`; whoosh/pop/sparkle times are derived from them, so re-timing a scene moves its SFX too.

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

## build_pakwebhoster.py (PakWebHoster, 2026-10-25)
Light theme (site --color-four #f0f7fd, green #2a862e, logo navy #1a2f3b; the logo PNG has a white background, so it
sits on white "logo cards"), 7 scenes = 7 VO lines: hook -> logo + "Web Hosting in Pakistan" -> Starter Lite chips
(10 GB NVMe, Unlimited bandwidth) -> SSL / LiteSpeed / Malware Scanner chips -> 24/7 Live Support -> PKR 200 / mahina +
"PKR 2000 / Year, 2 Month FREE" -> end card (URL pill, Call / WhatsApp). TOTAL = VO end + 3.7 s = 30.0 s (owner asked 30 s).
VO: vs_tts.py default voice; weak lines regenerated (seed 21 / reworded) and the chosen takes joined with
library/tools/vo_join.py (pitch-matched to 172 Hz, gap 0.55 s). Music: CC0 "Sunglasses" (Loyalty Freak Music) from
19.6 s at volume 0.16. Render -w 3: 69 s; -16.6 LUFS after loudnorm; watch.py 30.0 real fps.

## build_hostlixo.py (HostLixo, 2026-10-27)
Dark monochrome site (#050505, white type, Space Grotesk / Plus Jakarta Sans / JetBrains Mono, all from the site CSS),
7 scenes = 7 VO lines, TOTAL 30 s: hook over the site's own Minecraft image -> logo + "₹90/mo" -> real plans-grid
screenshot in a browser frame (full width, vertical pan only: a wider zoom cut the ₹90 column) + "9 PLANS" -> site DDoS
card + 2 rows with the site's own inline SVG icons -> software chips over the site's castle image -> "24h REFUND POLICY"
+ terms-page badge -> end card (mark, "Order on Discord" white button with the site's Discord icon, URL, footer payment
badges) over the cave image blurred 8 px (hides the in-game crosshair behind the CTA). Screens from
library/clients/hostlixo/site/tools/shots.js (scratchpad only). VO: saved voice `promo-male`, lines 3/4 re-taken with
seeds 21/33. Music CC0 "It feels good to be alive too" from its first drop (12.89 s). Measured here 2026-10-27: check
passed; render -w 3 1m14s; listen.py -15.3 LUFS, 0 clipped; watch.py 30.0 real fps. watch.py first flagged 1.1 s of
black at the start of the "24h" scene (the number entered 1 s late): bring a scene's main element in by ~0.1 s.
