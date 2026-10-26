# food-promo-reel (9:16, VO-synced food/deal promo from a restaurant's own site photos)

Made for Pizza Base PK (pizzabasepk.com) on 2026-10-25. `build_pizzabase.py` follows hosting-promo-reel/
build_moradosolution.py: scene starts come from `assets/vo/lines.json` (vs_tts.py --parts) + VO_START 0.4 s.

Scenes: hook (spinning pizza photo, "PIZZA KA / MANN HAI?", logo pop) -> 3 deal scenes (the client's own deal poster
in a white-border card + yellow price stamp popping on the spoken price, bass hit) -> "NAYA AAYA HAI!" 3 items popping
on their spoken names -> platter push-in + site slide text + price stamp -> 6 city chips + "DELIVERY & PICK-UP" ->
end card (logo, site pill, phone, WhatsApp). Background = the photos' own solid red (#A50000, measured on every corner
pixel), photo edges faded into it with a radial CSS mask, so no cut-out is needed.

Measured here 2026-10-25: `check` passed (after moving the platter below its title: text_occluded info); render
35.9 s 1080x1920 `--quality high --workers 3` in 2 m 05 s (25 MB); listen.py -14.6 LUFS, true peak -1.2 dBTP,
0 clipped; watch.py 30.0 real fps, 0 black frames. Music: CC0 desi-eastern--bollywood-groove.mp3 at volume 0.18.

To reuse: new client's crawl (library/clients/<name>/crawl.js pattern), replace image files/texts/prices with what the
site shows, keep one line per scene, re-run with the new VO.

## build_korba.py (Korba Restaurant, 2026-10-26)
For a site whose photos are mixed phone shots (no shared solid background): each scene = the photo in a white-border card
over a blurred, darkened copy of the same photo. Make that copy as a separate file (`<name>_bg.jpg`, ffmpeg scale/crop
1200x2040 -> 300x510 -> gblur sigma 10 -> back up, eq brightness -0.18): using the same `src` twice in one scene gave lint
`duplicate_media_discovery_risk` (measured here 2026-10-26). Menu-card photos cropped to one section (deal list + price)
work as their own scene visual. Key-word timings come from `assets/vo/fracs.json` (Whisper word starts / line length).
The first frame must show the title: don't fade the hook title in from opacity 0 (the first snapshot at 0 s was empty).
Measured: `check` 0 errors/0 warnings; render 33.1 s 1080x1920 in 1 m 57 s (--workers 3); -14.5 LUFS, 0 clipped, 30 fps.
