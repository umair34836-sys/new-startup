---
name: desi-reels
description: Make a Pakistani/Indian-style Reel, TikTok or YouTube Short (wedding, mehndi, Eid, shop/boutique, restaurant, real estate, shayari, slow-mo song-line, photo slideshow, Pashto audience) or pick desi music with vocals that needs no credit. Use when the owner says "Pakistani style reel", "desi reel", "trending reel banao", "shaadi ki reel", "dukaan ka promo", "Eid reel", "Urdu gaana chahiye (free)", or asks what is trending on Reels/TikTok in Pakistan.
---

# Desi reels + no-credit desi music

Read first:
1. `library/research/pk-reels-trends.md`: sourced 2026 trends (CapCut trending list, platform limits, safe zone,
   Pakistani wedding/shop/food/real-estate findings). Every claim there has a URL and date. Do NOT add claims of your
   own; if you need a new fact, research it (Agent-Reach, not Firecrawl) and save it there with source + date.
2. `library/research/pk-reel-recipes.md`: 16 recipes mapped to this repo's tools. Pick the closest one.
3. `CLAUDE.md` sections "Editing a phone video" and "Client phone-video edits" (measured mix levels, fps fix,
   WhatsApp export) and the `hyperframes` skill for building/rendering.

## Steps
1. Ask (only if unclear): occasion/business, length (teaser 15-30 s or 60-90 s), language of captions (default Roman
   Urdu), whether the client has their own music.
2. Look at the footage first (ffprobe, contact sheet). Personal/client media stays in the scratchpad, never in git.
3. Build from `library/templates/phone-clip-reel/build.py` (one shot per bar, word captions, light leak/flash blocks).
   Title at 0 s, hook in 1-3 s, text inside the safe zone (keep ~270 px top, ~672 px bottom, ~64 px sides clear).
4. Music (owner rule: NO-credit only, made by others):
   - instrumentals: `library/music/cc0/` (`desi-eastern--*` for dhol, tabla, sitar, wedding music);
   - songs WITH vocals in Urdu/Hindustani: `library/music/desi-vocal/` (public-domain 78 rpm records from 1905-1922,
     mono and scratchy: tell the owner it is a 100-year-old recording). Check its README for which files have
     clearly audible singing.
   - Pashto song with vocals: none found that is free of credit. Use a Pashto voice line from `vs_tts.py` (Pashto tested at 81%
     Whisper match, library/research/voicestudio.md; check which `--lang` value it expects before running) over a CC0
     instrumental, or the client's own licensed track.
   - Never trending film songs or YouTube rips (copyrighted). Never our own ACE-Step songs unless the owner asks.
5. Voice: client's own voice -> `clean_voice.py`; new narration -> skill `voice-or-song`.
6. Check with `npx hyperframes audio` + snapshots, mix about -16 LUFS, render, make the WhatsApp copy, send with
   SendUserFile. Reply to the owner in Roman Urdu.
