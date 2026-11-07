# Panel plugin tutorial template (16:9 YouTube, HyperFrames)

First used: SkilloraClouds "GeyserMC + Floodgate (Java + Bedrock, NetherNet 2026)" ~3:50 and "Simple Voice Chat" ~2:05,
built 2026-11-07 (skillora-reel-v3 session). For tutorials made from a client's panel recordings + screenshots + a VO script,
without the owner's own in-game/phone shots (those become step cards; add recordings in a v2).

Folder layout (scratchpad, never committed: recordings/screenshots are client media):
```
tut/
  in/      panel recordings (mp4; GIF-derived 30 fps is fine)
  img/     panel screenshots (1280x551 typical) - *_BLUR-IP* ones get their IP boxes blurred into assets/img/
  vo/      vX_lines.txt (Devanagari, one line each), parts_vX/NNN.wav (vs_tts.py --parts), ref.wav
  assets/  fonts (Anton, Plus Jakarta), vendor/gsap-3.14.2.min.js, img/ (processed), logo.png, panel-console.jpg
  shots.py build_tut.py mix_tut.py mux_tut.sh  (this template)
```

Steps:
1. Look at every input (contact sheets for recordings, every screenshot full size). Find click moments in the recordings by
   frame difference (fraction of pixels changed > 20 levels; GIF-derived recordings are static between UI changes) and
   confirm on the contact sheet. Locate IPs / account data and blur them with PIL (GaussianBlur 10 on the exact boxes),
   then view the crop again. Screenshots under ~400 px wide are unreadable even at x3: use them only as a frosted,
   dimmed backdrop (`bg`) behind a crisp card that repeats the text.
2. `shots.py`: one plan per video. Shot kinds: `title`, `card` (rows with number badges, `reveal` per word ref, optional
   `diagram` block: ports / floodgate / voice / proximity), `rec` (one or more `clips`: a recording range, `until=ref` where
   the next clip takes over, `play_at=(ref, action_s)` holds the first frame until the word is spoken so the recorded click
   lands ON the word, then plays at 1x and freezes; otherwise speed-fit 0.85-1.6x; a white band at the bottom and the
   scrollbar column are cropped), `shot` (screenshot in a monitor frame, mild Ken Burns `kb`), `code` card rows, `outro`.
   `calls` = word-synced arrows: `(ref, label, (x, y) in source px, clip index, 'g'|'r')`; each shows at its word and leaves
   when the next one comes. `caps` = one English caption per VO line (switches at the line).
   Refs: `19` = start of VO line 19, `19.6` = 60% into it, `"19:शब्द"` = when that word is spoken (Whisper word timestamps
   from `words.py`, matched by text similarity AND position; fallback = proportional position of the word in the line).
   Coordinates: make 100 px grid overlays of recording frames and screenshots (PIL) and read them off, never guess.
   LEADV = 0.5 s: every visual reaction (arrow, reveal, code row, click) lands 0.4-0.5 s BEFORE its word; at 0 s lead the
   owner saw "voice pehle, video baad mein" (2026-11-07). Recordings never play below 1x (freeze instead of slow-mo).
3. `build_tut.py vX [--stub]` -> proj_vX/index.html (+ clips). `--stub` estimates 0.07 s per Devanagari character so the
   layout can be checked while the VO is still generating. Then `npx -y hyperframes@0.8.210 check` and
   `snapshot --at a,b,c --no-end -o snaps`; look at every frame.
4. VO: `vs_tts.py vX_lines.txt vX.wav --lang hi --model voxcpm2 --ref ref.wav --ref-text "<ref line>" --seed 7 --gap 0.35
   --parts parts_vX`; Whisper-check each part (library/tools/wcheck_lines.py) AFTER TTS finished (never two torch jobs at once),
   then `words.py vX` (Whisper small, word_timestamps) -> vo/words_vX.json for the word-synced arrows,
   redo weak lines with seeds 21/33 (a word that stutters in every seed: reword it). Rebuild without --stub.
   Running `check` while VoxCPM2 generates crashed this container (exit 137, 2026-11-07): nothing heavy during TTS.
5. Render video only: `npx -y hyperframes@0.8.210 render -q high -w 3` (no audio tags in the HTML; audio is mixed in numpy).
6. `mix_tut.py vX`: VO loudnormed to -16, CC0 bed via music_fit.py (--start after the slow intro, music_cut before the track's fade-out so the loop never runs through it, --end fade, --lufs -20),
   envelope ducking -11 dB under speech (skill #1890), mouse clicks at the recordings' clicks, a soft chime on the console
   "ready" ring. `mux_tut.sh vX name` -> out/name.mp4 (yuv420p, high, faststart) + ebur128.
7. QA: watch.py + listen.py, ffprobe pix_fmt, then deliver (SkilloraClouds: FINAL directly, no preview, no WhatsApp copy).

Design floor (Hallmark gates §4): solid dark surfaces (#070b12 / #0f172a), one accent (#22c55e), Anton headlines +
Plus Jakarta body, real panel screens (dimmed) instead of gradients, no eyebrow labels, no tracked caps, captions in a
bottom box <= 1360 px wide (skill #402). Credit "Edited by MrCopper804" on the end card.

Sync upgrade (owner 2026-11-07, "voice ke saath perfect sync, arrows, captions, extra things"): v2 of both videos added
word-synced arrow callouts (27 + 13), per-line captions, held-until-the-word recording clips and 4 concept diagrams.
Measured: Whisper small word timestamps for 52 Hindi lines ~12 min; both renders 6 + 3 min; HyperFrames lint error
`content_overlap` when a hidden callout was faded with opacity only -> hide with autoAlpha (visibility) and mark the
callout `data-layout-allow-overlap`.
