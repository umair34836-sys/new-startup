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
