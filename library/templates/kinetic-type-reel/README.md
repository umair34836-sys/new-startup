# kinetic-type-reel (9:16, 20 s, text + CC0 music, no VO)

Made for PakWebHoster on 2026-10-25 (owner asked for a "kinetic typography" reel). `build_pakwebhoster.py` writes one
`index.html`: big Anton words rise out of masks (yPercent 105 -> 0) on the music's beats, the full-screen background
colour flips on each spec (white / green / navy), 5 progress dots, price slam with a shake, end card (logo card, URL
pill, phone). Scenes are visible only inside their own time window (`WIN`), which also keeps `hyperframes check` clean.

Beat grid from `listen.py` on the cut music (139.9 BPM, first beat 0.46 s): `b(n)` = time of beat n. Music:
library/music/cc0 "High Technologic Beat Explosion" (Loyalty Freak Music, CC0) from 42.4 s (its drop). SFX from
library/sfx (impact-punch, pop-high, pluck, cash-register, sparkle, whoosh-fast/up/down).

Measured here 2026-10-25: check 0 errors; render `-q high -w 2` took 42 s; -18.1 LUFS -> loudnorm to -16
(`ffmpeg -c:v copy -af loudnorm=I=-16:TP=-1.5`); watch.py 30.0 real fps, no black frames.
Lessons: words that start on screen at 0 s must NOT get a fromTo (it renders them hidden on frame 0: blank thumbnail);
don't tween letterSpacing (lint), use scaleX.

To reuse: change the words/specs/price/end card to the new client's verified facts, re-run listen.py on the new music
cut and set B0/BEAT, copy assets (gsap from library/vendor, fonts, logo, sfx, music) into assets/.
