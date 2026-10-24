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
