# Free music without credit: sources checked Oct 24 2026

Audit 2026-10-24 (later session): re-tested items carry "(re-checked 2026-10-24)"; counts from the earlier crawls
the same day are past results (scripts not kept) unless marked.

Owner rule: only music that needs NO credit/attribution (CC0, public domain, Pixabay-style licence, or made by us).
CC BY (YouTube "Creative Commons" filter, Kevin MacLeod/incompetech, most Jamendo/FMA) is NOT acceptable: it needs credit.

- YouTube Audio Library: only inside YouTube Studio with a login; not reachable from here.
- YouTube CC filter (search URL + &sp=EgIwAQ%253D%253D, yt-dlp --flat-playlist): CC BY = credit required -> rejected.
  Also many "CC" uploads are re-uploads/AI covers of famous songs: never trust the label alone.
- Openverse API (api.openverse.org, license=cc0,pdm): anonymous page_size max 20, needs a curl-like User-Agent, rate
  limits quickly (sleep ~4 s between calls; re-checked 2026-10-24: page_size=50 -> 401 "page_size may not exceed
  20 for anonymous requests"; a curl/8 User-Agent worked). Found (earlier session) 128 CC0 music tracks 45-400 s, almost all from Freesound, plus a few
  on Wikimedia Commons (e.g. Komiku, CC0). Freesound files live on cdn.freesound.org, which answers 403 to this server
  even with the network open (re-checked 2026-10-24). Shortlist (CC0): Good Vibe Background Music, Cute Happy Background Music, Lofi Fusion
  Background Music, Free Uplifting Music, Big Band Jazz, Epic Music loop, Emotional Original Soundtrack - FORGIVENESS,
  Sad Piano Background Music, Atmospheric Piano & Violin Music 01, Hip Hop beat Chill, Corporate company introduction
  video, Indian Wedding Dhols, Pashto Rhythm12/13, Tanpura 10, Sitar.wav, Arabian style soundtrack (+ others in
  the session's candidates list; re-query Openverse to get URLs).
- Urdu/Pashto SONGS under CC0/PD: none found anywhere (only word-pronunciation clips on Commons).
- archive.org "CC0" filter: the licence is set by uploaders and is often false (Mohammed Abdel Wahab's songs and a
  "Hindi Bhajans collection" are tagged CC0). Do not use archive.org licence tags as proof.
- Wikimedia Commons API: needs a descriptive User-Agent; rate-limits bursts ("too many requests").
- Our own music (ACE-Step, library/tools/music_pack.py): fully ours, no credit. ACE-Step 1.5 vocal languages include
  Urdu ('ur'); Pashto is not supported (acestep/constants.py, re-checked 2026-10-24) (try lyrics in Pashto script with lang 'unknown').

## Update Oct 24 2026 (network now full)
- cdn.freesound.org and freesound.org pages return 403 to this cloud IP, even with browser headers (re-checked 2026-10-24).
- upload.wikimedia.org returns 429 in bursts to this IP (one request got 200 on 2026-10-24; the commons API answered
  429 to a single request that day); a slow downloader (1 file/min, 3 min back-off) is the only way.
- OpenGameArt.org WORKS: advanced search with field_art_type_tid[]=12 (music) & field_art_licenses_tid[]=4 (CC0).
  Verify each page links only to publicdomain/zero (some list CC0 + CC BY: skip). Real files are
  /sites/default/files/<name>.mp3|ogg (NOT the /styles/.../audio_preview/ links, which are truncated previews).
  29 tracks saved in library/music/cc0 (see its README).

## Hindi / Urdu / Pashto music without credit: research Oct 24 2026 (GitHub + web)
Short answer: CC0 or public-domain SONGS WITH VOCALS in Hindi, Urdu or Pashto barely exist. What does exist: CC0
desi instrumentals, loops, field recordings and a few Pashto rhythm tracks. For songs with words, we make our own
(ACE-Step, `music_pack.py`; Urdu 'ur' works, Pashto only as an attempt).

- **GitHub: SoundSafari/CC0-1.0-Music** (75 stars, repo licence CC0, Exa 2026-10-24): 9,292 files (`git ls-tree`,
  re-checked 2026-10-24: freesound.org 2,998, freemusicarchive.org 5,181, chosic.com 798, freepd.com 302, pixbay.com 11,
  + README/LICENSE). Its README says "~7000 songs" and "~40gb" (size not measured).
  KEY: files download from raw.githubusercontent.com/SoundSafari/CC0-1.0-Music/main/<url-encoded path> (tested 200 OK),
  so it gets around Freesound's IP block on this server. List files without downloading 40 GB:
  `git clone --filter=blob:none --no-checkout --depth 1 https://github.com/SoundSafari/CC0-1.0-Music.git && git ls-tree -r --name-only HEAD`.
  Desi picks in it: freepd.com/Bollywood Groove.mp3, freepd.com/Breaking Bollywood.mp3 (FreePD = public domain),
  freesound 553179 Damal drumming in Pakistan (Lahore, 2:29), 395024 Hindu wedding ceremony music (2:56),
  331466 Indian drums atmosphere (1:01), 593850 India electric dreams (0:54), 423453 men singing a traditional Indian
  song (1:21), 685775 indian rap 72bpm loop, 380750/377315/216060 veena, 322327 Middle East tribal percussion.
  The repo's own CC0 claim is not proof: check each Freesound ID's page (below). The FMA part also holds old
  78 rpm recordings (e.g. "Veena Kinhal - Haratanaya Sree", "Anonymous - Persian Music"): verify before use.
- **GitHub: 0lhi/FreePD** (11 stars, CC0, Exa 2026-10-24): mirror of freepd.com. freepd.com itself now shows only a
  closure page: "FreePD.com - Site Closed ... we have officially taken the service offline ... 2008-2025" (re-checked
  2026-10-24; freepd.com/world.php = 404). That it was Kevin MacLeod's site is NOT stated there (unverified).
- **Verify a Freesound licence without Freesound access**: `agent-reach read https://freesound.org/s/<id>/` (Jina fetches
  it from its own servers). The page says "...for commercial purposes, all without the need of asking permission" for CC0.
  Verified CC0 Oct 24 2026 (553179, 395024, 331466, 593850, 423453 re-checked later that day via Jina/Exa page text): 553179, 395024, 331466, 593850, 685775, 423453, 380750, 322327, 725362 (Eastern Delight Beat),
  554480 (Bollywood flute), 639391 + 639390 (Nigar585 "Pashto Rhythm12" 0:39 and "Pashto Rhythm13" 3:22, the only
  CC0 Pashto music found; NOT in the SoundSafari mirror, and cdn.freesound.org is blocked here).
- **Openverse** (license=cc0,pdm) for pashto/urdu/hindi/qawwali/ghazal/bhajan: only word-pronunciation clips
  (Lingua Libre), Urdu poetry readings by maqsood5 (CC0, spoken), phone intercept messages, plus the Freesound items above.
  sitar 34 hits, tabla 115 (re-checked 2026-10-24, license=cc0,pdm) (mostly one-shots/loops).
- **Pixabay** ("13,816 Urdu songs", Pashto tracks such as "Echoes of Khyber Pashto": seen in an earlier search; not
  re-checkable, pixabay.com returns 403 here, re-checked 2026-10-24): Pixabay Content License = free,
  no credit needed, but not CC0 (no standalone redistribution, some uploads get YouTube Content ID claims). pixabay.com
  returns 403 to this server (Cloudflare); the owner would have to download on their phone/PC.
- **archive.org**: thousands of Hindustani 78 rpm discs (Great 78 Project: Lata, Rafi, Shamshad Begum, Naushad...),
  but 1940s-50s film songs are still under copyright. Terms (WebSearch 2026-10-24): India = author's life + 60 years
  (Copyright Act 1957 s.22, per law summaries); Pakistan = life + 50 years (Copyright Ordinance 1962 s.18, per
  en.wikipedia.org/wiki/Copyright_law_of_Pakistan; corrected: the old note said 60); US: recordings published in 1925
  entered the public domain on 1 Jan 2026 (adp.library.ucsb.edu Public Domain Day 2026). Only recordings published
  before 1926 whose composers/poets died 60+ years ago (e.g. Gauhar Jaan's early-1900s
  thumri/dadra, traditional texts) are safely public domain. "VintageSense Vintage Indian Music" items are CC BY-NC-ND
  (credit + non-commercial: rejected). IndiaCulture/NCAA items are CC BY-NC (rejected).
- **Kaggle / Hugging Face Urdu/Pashto audio datasets**: speech (ASR) data, not music. Common Voice Pashto/Urdu is CC0
  but it is people reading sentences. PMB (Persian music benchmark) and PCMIR are research data, not cleared for videos.
- aigei.com mirrors Nigar585's Pashto Rhythm files (labelled CC0) but needs a login.
- nullrights.com: every track CC0 ("no attribution required"), general genres; songly.gift lists CC0 Hindi pages.
- 7 of the verified desi files are saved in library/music/cc0 (desi-eastern--*), see its README.

## FMA directly (Oct 24 2026, network full): the best no-credit source found so far
- freemusicarchive.org pages load with curl (browser User-Agent). Public-domain search, 100 per page:
  `https://freemusicarchive.org/search/?adv=1&music-filter-public-domain=1&pageSize=100&page=N` -> 9,457 tracks (95 pages; re-checked 2026-10-24:
  94 full pages + 57 on page 95). files.freemusicarchive.org mp3 download: HTTP 206 (re-checked).
  Each result carries `data-track-info` JSON (id, title, artistName, url). The track PAGE's data-track-info has `fileUrl`
  (files.freemusicarchive.org/...mp3, direct download, no login), the licence link and "Plays"/"Downloads" counts.
  (Adding `&sort=interest` with pageSize returned nothing.)
- Licence check per track: keep only creativecommons.org/publicdomain/zero/1.0 or /licenses/publicdomain/ (old PD mark),
  reject any /licenses/by. Of 2,222 tracks by trusted artists, 2,188 passed (the rest had no licence link).
- Mislabels exist: the PD filter also lists commercial uploads (e.g. "Mzansi Hooligans - Woza ft Busiswa"), so only use
  artists who release everything CC0: Komiku 291, HoliznaCC0 690, Monplaisir 520, John Bartmann 340, TRG Banks 126,
  Loyalty Freak Music 96, Kimiko Ishizaka 32 (Bach), Daniel Veesey 30 (Beethoven), Alpha Hydrae 64, Soundtrack 4 Life 33.
  Kosta T (2,951) is experimental (counts from the Oct 24 crawl, not re-counted). Desi/Indian music on FMA PD: almost none (two Carnatic veena recordings).
- 95 most-downloaded tracks saved in library/music/cc0 (see its README). Scripts: scratchpad fma/crawl.py, verify.py, dl.py
  (logic described here; re-create if needed). Wikimedia slow downloader abandoned (FMA has the same Komiku tracks, fast).
