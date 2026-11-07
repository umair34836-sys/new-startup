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
2. `shots.py`: one plan per video. Shot kinds: `title`, `card` (rows with number badges, `reveal` per line),
   `rec` (recording, speed-fit 0.85-1.6x to its VO lines, frozen on the last frame if the VO is longer, a white band at the
   bottom of a GIF page is cropped off automatically), `shot` (screenshot in a monitor frame, Ken Burns `kb=(fx,fy,scale)`
   toward the ringed region, `rings` in screenshot px at a VO line ref, `code` card rows, `chips` path rows), `outro`.
   Line refs: `19` = start of VO line 19, `19.6` = 60% into it.
3. `build_tut.py vX [--stub]` -> proj_vX/index.html (+ clips). `--stub` estimates 0.07 s per Devanagari character so the
   layout can be checked while the VO is still generating. Then `npx -y hyperframes@0.8.210 check` and
   `snapshot --at a,b,c --no-end -o snaps`; look at every frame.
4. VO: `vs_tts.py vX_lines.txt vX.wav --lang hi --model voxcpm2 --ref ref.wav --ref-text "<ref line>" --seed 7 --gap 0.35
   --parts parts_vX`; Whisper-check each part (library/tools/wcheck_lines.py) AFTER TTS finished (never two torch jobs at once),
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
