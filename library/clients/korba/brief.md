# Korba Restaurant: client brief

- Owner's client (MrCopper804), session started 2026-10-26, branch client-korba.
- Website: https://korba-restaurant.localoria.com/ (a Localoria directory listing, not Korba's own site).
  All facts + image list: site-data.md (crawled 2026-10-26 with crawl.js).
- Owner's rule for this client (2026-10-26): promotional video; visuals ONLY from the website's own pictures/videos,
  nothing from elsewhere, no guesswork.

## Brand (from the site's images, 2026-10-26)
- The website's CSS/font (Jost, Localoria colours) is Localoria's, not Korba's: do not use as brand.
- Korba's printed menu card: deep red ~#912828 / #8a2f21 with yellow labels ~#cfc040, white text
  (pixel samples of llimg-menu-6, measured here 2026-10-26). Night signage: red/pink neon "I ❤ KORBA".
- Logo: only the white calligraphy emblem on the Ramadan 2025 flyer (llimg-menu-4), small.

## Contact
- +92 333 3443313 (site text; WhatsApp icon beside it on the Ramadan flyer); menu cards also list 0315-9403090 and
  0923-560131. Facebook: www.facebook.com/korba.nsr (flyer). Address: GT Rd, Khat Kalay, Nowshera.

## Contradictions / cautions found
- Hours block says "Open 24 hours" every day but also shows a "Closed" status label: don't claim 24 hours without
  the owner/client confirming.
- Menu prices come from photos of a printed card (date unknown, "excluded tax", some hand-corrected): quote only if the
  owner OKs, with "+ tax".
- llimg-menu-10 is another business's flyer (Istanbul, Mardan) and llimg-menu-4 is an old Ramadan 2025 offer: never use.
- llphoto-2 is a YouTuber's frame with a person + "Subscribe" overlay: don't use. llphoto-4 has a photographer
  watermark ("By Khalid Ur Rahman").
- No videos on the site; only 9 usable photos (most portrait phone photos, some low-res) + menu card photos.

## Promo reel v1 (FINAL delivered 2026-10-26; owner: client paid, final directly, no timing claim)
- 9:16, 33.1 s, built with library/templates/food-promo-reel/build_korba.py. Script (owner-approved 2026-10-26):
  vo-script-2026-10-26.txt (8 lines; prices Fish Angara 1400/kg, Korba Special BBQ Platter (Full) 8000, Mix Tawa 8 Person
  8000, "Prices + tax (menu card)" on screen).
- VO: vs_tts.py default voice (VoxCPM2), --parts; lines 3-4 re-made with seed 21 (Whisper small heard "आथ हजार" /
  "मिक्स्तवा" instead of "आट्ध हादार" / "निक्स्तवा"); pitch to 172 Hz median (voices.json target_f0).
- Music: CC0 desi-eastern--breaking-bollywood.mp3 (FreePD) from 26.8 s (first drop per listen.py), volume 0.18.
- SFX (own): whoosh-fast-0.3s, impact-punch on prices, pop-high on item pops, sparkle on logo.
- QA (measured here 2026-10-26): listen.py -14.5 LUFS, true peak -1.45 dBTP, 0 clipped; watch.py 30.0 real fps,
  993 frames, no gaps; render 1 m 57 s (--quality high --workers 3), 31.7 MB; WhatsApp copy 8.2 MB.
