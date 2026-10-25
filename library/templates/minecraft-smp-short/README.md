# minecraft-smp-short (9:16 YouTube Short, VO-driven Minecraft server promo)

Made for Mr Aloo / ALOO SMP on 2026-10-25 (edit log: library/clients/mraloo/edit-log-short-v1.md). The owner's rule
for this client: zero guesswork, every decision from repo skills; the log maps each choice to its source.

Inputs (scratchpad only, never committed): client VO (retakes removed, loudnorm -16), `words.json` = Whisper MEDIUM
word timings on the final VO (`[start, end, word]`), gameplay recordings (OBS .mkv 1080p60), the server emblem (JPG if
the PNG is over 2 MB), a CC0 music track and its listen.py JSON (beat grid).

`python3 build.py` cuts every shot with ffmpeg (crop/fill/blur modes, `RECUT=1` to redo all), writes
`compositions/{footage,hook,logo,f1..f5,online,jb,end,captions}.html` + `index.html` with all audio lanes.
Then: `npx hyperframes@0.8.188 check --json`, `snapshot --at ...` (look at every frame), `render -q delivery -w 3`
(62.6 s took 4m55s-5m52s here), then QA: watch.py + listen.py + ebur128 + per-0.25 s mix-vs-VO level check +
Whisper medium on the mix + a 1.6 s contact sheet of the whole render.

To reuse: replace `RAW` shots (in-points from 2 s contact sheets of the recordings, avoid chat/AFK/loading screens),
`GROUPS` (caption groups = word indices + Roman words, `*` = gold, `_` joins two Roman words for one Whisper token),
checklist items, the end-card data (IP, port, Discord) and the colours sampled from the client's logo.

Lessons from QA (2026-10-25):
- A group's hide time must never pass the next group's start (v1 showed "customn hai" for a frame); build asserts it.
- SFX more than 4 dB over the VO window = too loud (level-up at 0.22 and sub-drop at 0.3 were 6 dB over); final levels
  are in build.py.
- A clip must be at least as long as its shot, or the last frame holds (tab-list clip was 1.03 s for a 1.21 s shot).
- 9:16 crop of 1080p = 1.78x upscale: `cas=strength=0.5` after lanczos raised Laplacian variance 39 -> 62 on a test
  frame without halos (skill #489).
- watch.py "soft" is relative to the sharpest scene (sharp_rel < 0.35), so text-heavy cards make footage read "soft".
