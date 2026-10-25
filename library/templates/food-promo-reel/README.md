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
