# kinetic-laptop-type (16:9, 20 s, text + music, no VO)

Kinetic typography inside a static CSS laptop on a dark desk; the camera never moves, no cuts. Made for SkilloraClouds
on 2026-10-24 (owner's style reference: a TikTok where a light UI inside a laptop screen opens a search bar, types a
question word by word with blur-to-sharp reveals and inline icons, fans out image cards, then ends on a dark screen).

Phases: search bar opens + question words blur in (pluck SFX per word) -> 4 spec chips with icons (glass-tap per chip)
-> 3 cards fan out (swish) -> "Budget & Standard plans" + LIMITED! stamp + coupon -> dark end screen, logo, URL typed
with GSAP TextPlugin (#2560), Discord line.

Skills used: #404 kinetic type basics, #2560/#2561 TextPlugin, #3107 device stage (hand-built CSS laptop instead of a
registry block). Assets: `assets/vendor/gsap-3.14.2.min.js` + `TextPlugin.min.js` (from `npm pack gsap@3.14.2`,
dist/TextPlugin.min.js, GSAP standard no-charge licence), fonts from library/fonts, SFX from library/sfx (ui/pluck,
ui-open, mouse-click, glass-tap, confirm-1, maximize, typing/typing-synth, transition/whoosh-up/down-0.6s, swish-4),
music library/music/cc0 "Traveling in your mind" (Loyalty Freak Music, CC0).

Measured here 2026-10-24: `npx hyperframes check` passed (2 warnings: duplicate logo img, one 27 px word);
`render -q high -w 3` took 49 s; the render came out at -20.6 LUFS, so the audio was loudnormed to -16 afterwards
(`ffmpeg -c:v copy -af loudnorm=I=-16:TP=-1.5`). Green text on the light UI needs the darker #16a34a (check: #22c55e on
white failed 3:1 contrast). The search bar opens with width + marginLeft together so it grows from the centre.

To reuse: change the words/cards/end screen to the new client's verified facts, keep every word hit paired with one SFX.
