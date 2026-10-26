# explainer-host-steps (16:9 explainer: blocky host + step cards + Roman captions)

First used 2026-10-26 for MoradoSolution "Indian RDP + BUSY setup" (owner's own Roman Hindi script, owner's price
16GB RDP ₹3,000/month; the owner chose "bina screen ke" = no fake Windows/BUSY screens, since we can't run either here).
Layout: owner's blocky host (library/characters/host-skin.png via library/tools/blocky_character.py) left
(talk on every VO line, wave on hello/thank-you, point on new steps), step cards with generic drawn SVG icons right,
captions = the owner's own Roman lines split into <= 42-char, max-2-line chunks timed by character share of each VO line
(decision-guide / from-scratch.md "Captions: Netflix 42 chars, 2 lines"). Brand-kit blocks (build_brand.py --size 1920x1080):
brand-bug (moved top-left), brand-end (+ price row, QR = website).
Needs in the project: assets/vo/{vo.wav,lines.json} (vs_tts.py --parts), captions.txt (one line per VO line), brand
blocks + assets/brand, fonts Anton + SpaceGrotesk, sfx swish-4, pop-high, confirm-1, cash-register, success-chime,
music cc0 background--chill-lofi-inspired (volume 0.2). Run with REPO=<repo> python3 build.py.
Measured here 2026-10-26: check passed (only zero-length host tween overlap warnings); 112 s rendered in 4m04s
(--quality delivery --workers 3); listen.py -14.4 LUFS, true peak -1.53 dBTP, no clipping; watch.py 30.0 real fps;
QR decoded from the rendered end card (OpenCV) = https://moradosolution.in.
