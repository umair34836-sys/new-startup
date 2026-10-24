---
name: urdu-captions
description: Urdu (Nastaliq), Pashto and Hindi captions or titles in a HyperFrames video - RTL, correct letter joining, line height, per-word reveal, gold accent word, mixed Roman/Latin words and numbers. Use whenever a video needs Urdu/Pashto/Hindi script on screen ("Urdu mein caption", "Pashto text", "Hindi likho").
---

# Urdu / Pashto / Hindi captions

Findings and sources: `library/research/urdu-captions.md` (read it for the why).

1. Text: get the Urdu/Pashto/Hindi-script lines from the owner or client. Never write Urdu-script words yourself
   from Roman Urdu or invent a translation; if you must propose a spelling, mark it "unverified" and get it confirmed
   on a rendered frame.
2. Write a spec (format: `library/blocks/urdu-captions.json`): one entry per caption line with `in`/`out` seconds,
   `*` before the gold accent word, `script`: `nastaliq` (Urdu), `naskh` + `"lang": "ps"` (Pashto), `sans`
   (bold title), `deva` (Hindi). Optional `sub` = a Roman Urdu / English line under it.
3. `python3 library/tools/urdu_captions.py --check spec.json` (missing glyphs, presentation forms, Arabic ي/ك in Urdu).
   Fix the TEXT with the person who supplied it, not by guessing.
4. `python3 library/tools/urdu_captions.py spec.json <project>/compositions/ucap.html`; copy the fonts it names from
   `library/fonts/` into `<project>/assets/fonts/`; mount it on a `data-track-kind="captions"` host.
5. `npx hyperframes check --json`, then `snapshot --at` the middle of every line and LOOK: letters joined, words in
   RTL order, Latin/number runs readable left-to-right, nothing clipped.

Hard rules (all tested):
- Animate per WORD (inline-block spans). Never split a word into letter spans: the joins break.
- Nastaliq `line-height: 2.0` or more, no `overflow: hidden` on the text box; Naskh 1.7; Devanagari 1.5.
- Noto Nastaliq needs `word-spacing: 0.25em` or words after د/ر look glued.
- Consecutive Latin/number words go in ONE `<span dir="ltr">` (two separate spans flip to "1948 UDHR").
  Outside the block, wrap them in `<bdi dir="ltr" style="white-space:nowrap">`.
- Pashto: Noto Naskh / Noto Sans Arabic / Vazirmatn (Gulzar has no Pashto letters).
- Sanah sign ؁ goes before the year digits: `؁۲۰۰۴ء`.
