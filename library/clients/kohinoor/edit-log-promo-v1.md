# Kohinoor promo v1 — edit log (2026-11-21)

Job: 9:16, ~30 s, English VO, direct FINAL (owner's answers, brief.md). Builder:
`library/templates/auto-parts-promo/build_kohinoor.py`. Facts: site-data.md.

## Type and structure
- decision-guide.md section 9 "Product ad / UGC ad": 15-30 s, 9:16, hook 0-2 s, benefit captions, CTA last ~4 s,
  "a slow brand intro before the product moment" is a common mistake -> hook line first, brand on screen from 0 s
  (first frame = thumbnail, CLAUDE.md HyperFrames learnings).
- Scenes = the 5 VO lines (exchange-promo pattern: scene starts 0.12 s before each line).

## Picture (no client material: owner "Kuch nahi, stock se banao")
- library/stock had no car/engine clip (find_stock.py "car engine mechanic garage": 0 results).
- Mixkit pages checked one by one (curl, 2026-11-21) for `data-license="videoFree"`:
  free = 4716 (mechanic repairing a car engine), 65 (sports car engine close-up), 2675 (speedometer of an accelerating
  car), 44284 (cars and trucks on a highway), 29995 (engineer's workshop), 41937 (mechanic pouring oil into an engine),
  100334 (no 4K file found). Restricted (not used): 33329, 13179, 15056, 17133, 24193, 13270, 33324 and others.
  Licence: https://mixkit.co/license/modal/videoFree/ (no attribution, commercial OK; stock README).
- Fetched the 2160p files one at a time into the scratchpad (never git). 9:16 = 1214x2160 crop scaled DOWN to 1080x1920.
- Looked at contact sheets (every 1.5 s): dropped 29995 (Scotch/brand labels on a desk). Skipped mk_65 0-1.5 s
  (radiator cap with a maker's badge) and mk_44284 0-1.5 s (trailer lettering): Mixkit clause 13, brands not cleared.
- Slow eased push-ins on s1/s3/s5 with different amounts (skill #154; no identical animation on every scene).

## Graphics (Hallmark floor, gates.md s.4)
- Display face Manrope (library/fonts, OFL): no client font exists. One accent colour (amber bar/chip), no gradient
  cards: every card sits on real footage under a dark veil; no tracked caps, no eyebrow labels, no coloured word inside
  a headline. Each scene enters differently: s1 lift, s2 bar + rise, s3 slide from left at the top of frame (rev counter
  visible below), s4 clip-path wipe, s5 end card rise.
- NPR shown as type only (no NPR logo file from the client; brief.md).
- Credit "Edited by MrCopper804" on the end card (CLAUDE.md client-facing rule).

## Voice
- vs_tts.py --voice luxury-deep --lang en (voices/README: "luxury, real estate, premium brand"; promo-male banned).
  Script lines: see the project's vo/script.txt (copy below). "N P R" spelled with spaces so it is read as letters;
  "nineteen thirty-four" written out (numbers kept on screen too, HANDBOOK s.12).

## Music (skill music-for-video)
- find_music.py "product ad promo confident industrial" and "rock driving powerful energetic" (--client --vo, 30 s).
  Top hits were happy/bright (Loyalty Freak "It feels good to be alive too", "Yippee"): wrong emotion for an engine-parts
  dealer. listen.py on two tense/driving picks:
  - high-technologic-beat-explosion: 140 BPM but loose grid (CV 0.116), full sound only at 27.88 s -> rejected.
  - cinematic--eye-of-the-storm (OpenGameArt, CC0; library/music/cc0/README.md): 125 BPM, steady grid (CV 0.013,
    downbeat clarity 0.824), full sound by 1.97 s, tense/driving, A minor, LRA 1.1 LU (steady under a VO) -> CHOSEN.

## Script (English)
1. Your engine deserves genuine parts.
2. Kohinoor is an authorized dealer of NPR piston rings.
3. N P R. Nippon Piston Ring, from Japan, since nineteen thirty-four.
4. Genuine NPR piston rings, and more auto parts, all in one place.
5. Kohinoor. Ask us for genuine NPR today.
