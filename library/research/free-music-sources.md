# Free music without credit: sources checked Oct 24 2026

Owner rule: only music that needs NO credit/attribution (CC0, public domain, Pixabay-style licence, or made by us).
CC BY (YouTube "Creative Commons" filter, Kevin MacLeod/incompetech, most Jamendo/FMA) is NOT acceptable: it needs credit.

- YouTube Audio Library: only inside YouTube Studio with a login; not reachable from here.
- YouTube CC filter (search URL + &sp=EgIwAQ%253D%253D, yt-dlp --flat-playlist): CC BY = credit required -> rejected.
  Also many "CC" uploads are re-uploads/AI covers of famous songs: never trust the label alone.
- Openverse API (api.openverse.org, license=cc0,pdm): anonymous page_size max 20, needs a curl-like User-Agent, rate
  limits quickly (sleep ~4 s between calls). Found 128 CC0 music tracks 45-400 s, almost all from Freesound, plus a few
  on Wikimedia Commons (e.g. Komiku, CC0). Freesound files live on cdn.freesound.org, which is NOT in the network
  allowlist (owner must add it). Shortlist (CC0): Good Vibe Background Music, Cute Happy Background Music, Lofi Fusion
  Background Music, Free Uplifting Music, Big Band Jazz, Epic Music loop, Emotional Original Soundtrack - FORGIVENESS,
  Sad Piano Background Music, Atmospheric Piano & Violin Music 01, Hip Hop beat Chill, Corporate company introduction
  video, Indian Wedding Dhols, Pashto Rhythm12/13, Tanpura 10, Sitar.wav, Arabian style soundtrack (+ others in
  the session's candidates list; re-query Openverse to get URLs).
- Urdu/Pashto SONGS under CC0/PD: none found anywhere (only word-pronunciation clips on Commons).
- archive.org "CC0" filter: the licence is set by uploaders and is often false (Mohammed Abdel Wahab's songs and a
  "Hindi Bhajans collection" are tagged CC0). Do not use archive.org licence tags as proof.
- Wikimedia Commons API: needs a descriptive User-Agent; rate-limits bursts ("too many requests").
- Our own music (ACE-Step, library/tools/music_pack.py): fully ours, no credit. ACE-Step 1.5 vocal languages include
  Urdu ('ur'); Pashto is not supported (try lyrics in Pashto script with lang 'unknown').

## Update Oct 24 2026 (network now full)
- cdn.freesound.org still returns 403 to this cloud IP (Freesound blocks it), even with browser headers.
- upload.wikimedia.org returns 429 in bursts to this IP; a slow downloader (1 file/min, 3 min back-off) is the only way.
- OpenGameArt.org WORKS: advanced search with field_art_type_tid[]=12 (music) & field_art_licenses_tid[]=4 (CC0).
  Verify each page links only to publicdomain/zero (some list CC0 + CC BY: skip). Real files are
  /sites/default/files/<name>.mp3|ogg (NOT the /styles/.../audio_preview/ links, which are truncated previews).
  29 tracks saved in library/music/cc0 (see its README).

## Hindi / Urdu / Pashto music without credit: research Oct 24 2026 (GitHub + web)
Short answer: CC0 or public-domain SONGS WITH VOCALS in Hindi, Urdu or Pashto barely exist. What does exist: CC0
desi instrumentals, loops, field recordings and a few Pashto rhythm tracks. For songs with words, we make our own
(ACE-Step, `music_pack.py`; Urdu 'ur' works, Pashto only as an attempt).

- **GitHub: SoundSafari/CC0-1.0-Music** (75 stars, repo licence CC0): ~9,300 CC0/PD files (~40 GB), mirrored from
  freesound.org (2,998), freemusicarchive.org (~5,180), chosic.com (~800), freepd.com (302), pixabay (11).
  KEY: files download from raw.githubusercontent.com/SoundSafari/CC0-1.0-Music/main/<url-encoded path> (tested 200 OK),
  so it gets around Freesound's IP block on this server. List files without downloading 40 GB:
  `git clone --filter=blob:none --no-checkout --depth 1 https://github.com/SoundSafari/CC0-1.0-Music.git && git ls-tree -r --name-only HEAD`.
  Desi picks in it: freepd.com/Bollywood Groove.mp3, freepd.com/Breaking Bollywood.mp3 (FreePD = public domain),
  freesound 553179 Damal drumming in Pakistan (Lahore, 2:29), 395024 Hindu wedding ceremony music (2:56),
  331466 Indian drums atmosphere (1:01), 593850 India electric dreams (0:54), 423453 men singing a traditional Indian
  song (1:21), 685775 indian rap 72bpm loop, 380750/377315/216060 veena, 322327 Middle East tribal percussion.
  The repo's own CC0 claim is not proof: check each Freesound ID's page (below). The FMA part also holds old
  78 rpm recordings (e.g. "Veena Kinhal - Haratanaya Sree", "Anonymous - Persian Music"): verify before use.
- **GitHub: 0lhi/FreePD** (11 stars, CC0): mirror of freepd.com (Kevin MacLeod's public-domain site; freepd.com itself went OFFLINE in 2026, so the GitHub mirrors are now the only source). freepd.com/world.php
  returned 404 on Oct 24 2026.
- **Verify a Freesound licence without Freesound access**: `agent-reach read https://freesound.org/s/<id>/` (Jina fetches
  it from its own servers). The page says "...for commercial purposes, all without the need of asking permission" for CC0.
  Verified CC0 Oct 24 2026: 553179, 395024, 331466, 593850, 685775, 423453, 380750, 322327, 725362 (Eastern Delight Beat),
  554480 (Bollywood flute), 639391 + 639390 (Nigar585 "Pashto Rhythm12" 0:39 and "Pashto Rhythm13" 3:22, the only
  CC0 Pashto music found; NOT in the SoundSafari mirror, and cdn.freesound.org is blocked here).
- **Openverse** (license=cc0,pdm) for pashto/urdu/hindi/qawwali/ghazal/bhajan: only word-pronunciation clips
  (Lingua Libre), Urdu poetry readings by maqsood5 (CC0, spoken), phone intercept messages, plus the Freesound items above.
  sitar 34 hits, tabla 115 (mostly one-shots/loops).
- **Pixabay** ("13,816 Urdu songs", Pashto tracks such as "Echoes of Khyber Pashto"): Pixabay Content License = free,
  no credit needed, but not CC0 (no standalone redistribution, some uploads get YouTube Content ID claims). pixabay.com
  returns 403 to this server (Cloudflare); the owner would have to download on their phone/PC.
- **archive.org**: thousands of Hindustani 78 rpm discs (Great 78 Project: Lata, Rafi, Shamshad Begum, Naushad...),
  but 1940s-50s film songs are still under copyright (lyricist/composer life + 60 years in India/Pakistan; US 95 years).
  Only recordings published before 1926 whose composers/poets died 60+ years ago (e.g. Gauhar Jaan's early-1900s
  thumri/dadra, traditional texts) are safely public domain. "VintageSense Vintage Indian Music" items are CC BY-NC-ND
  (credit + non-commercial: rejected). IndiaCulture/NCAA items are CC BY-NC (rejected).
- **Kaggle / Hugging Face Urdu/Pashto audio datasets**: speech (ASR) data, not music. Common Voice Pashto/Urdu is CC0
  but it is people reading sentences. PMB (Persian music benchmark) and PCMIR are research data, not cleared for videos.
- aigei.com mirrors Nigar585's Pashto Rhythm files (labelled CC0) but needs a login.
- nullrights.com: every track CC0 ("no attribution required"), general genres; songly.gift lists CC0 Hindi pages.
- 7 of the verified desi files are saved in library/music/cc0 (desi-eastern--*), see its README.
