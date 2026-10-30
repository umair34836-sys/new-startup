# HostLixo brand identity reveal v1: edit log (2026-10-27)

The owner's request came through the main session: "Haan, Hostlixo ke liye is style ka template bana do". The owner answered here on 2026-10-27: 16:9 only, only the site's own images (no stock), music only (no voice), watermark (a) as before.

| Decision | Source |
|---|---|
| Shot order, quiet intro + drop at 7.4 s, beat cuts | library/research/ref-brand-identity-reveal.md (measured reference) |
| Logo construction draws the REAL mark edges (OpenCV trace of hero-logo.png: 2 polygons, 10 vertices each), with the measured 11° slant | mark_to_svg.py; skill #427 (draw-on 0.6-1.2 s, stagger 0.06-0.10 s, settle 1.04 -> 1.00) |
| Lockup = site logo.png with a clear-space box, plus the site's title words "Minecraft Server Hosting in India" | brief.md; skill #426 |
| Mockups use real site screenshots: home hero in a browser frame (URL hostlixo.in); RECOMMENDED AMD EPYC 8 GB card in a phone | site/tools/shots.js; skill #3107 (device blocks, hand-built) |
| Stacked cards = 4 real page screenshots | reference shot 6 |
| Typography = the 3 fonts the site loads; colours = 6 site CSS variables with their names | site/brand.json |
| Widget cards = the home-page stat row verbatim; chart = the 9 real plan prices (₹90-₹1,440), 8 GB highlighted (site: RECOMMENDED) | site-data.md |
| Photos = the site's 3 Minecraft images, labelled with the site's own captions | brief.md (images looked at) |
| Music: CC0 "It feels good to be alive too" (Loyalty Freak Music), from 5.48 s so its 12.887 s drop hit lands at 7.4 s; 140 BPM grid | listen.py; owner CC0 rule |
| SFX: riser into the drop, impact on the drop, whoosh on every post-drop cut | stock-sfx-luts; CLAUDE.md mix levels |
| Mastering with gain + limiter (keeps the intro contrast) | template README "Mastering" |
| Copyright: watermark.py, now sized by the short side (it was 1.8x too big on 16:9) | owner's choice (a) |
