---
name: listen-and-watch
description: Before editing or judging any audio or video (music track, voiceover, song, phone clip, render), run listen.py / watch.py to turn it into facts Claude can reason about - BPM and beat grid, downbeats, hits, loudness (LUFS), sections, silences, where voice/singing is, key, hum/hiss/clipping, Whisper words; real fps, shot cuts, shake, blur, exposure, colour cast, faces, flicker, black/frozen frames and a contact sheet - plus compare mode for before/after approvals and fast_matte.py for fast CPU person mattes. Use for "cut on the beat", "check the render", "is the sound ok", "kya video theek hai", "music ke beat pe cut", "background blur", or any time Claude would otherwise guess what media sounds or looks like.
---

# Listen and watch before you edit

Claude can't hear and can't watch video in real time. Never guess timings, tempo, loudness or what a clip shows:
measure first, then reason from the report. Details, accuracy and limits: `library/research/perception-tools.md`.
Speed tips and benchmarks: `library/research/cpu-speed.md`.

## 0. Setup (once per session, ~30 s when cached)

```bash
[ -f /home/user/tools/.specialist-a-ready ] || bash library/tools/setup-specialist-a.sh
P=/home/user/tools/perc-venv/bin/python
```
Whisper words and `--vocals` also need the main venv (`/home/user/tools/.heavy-ready`, from setup-all.sh).

## 1. Audio: `listen.py`

```bash
$P library/tools/listen.py track.mp3 --out /tmp/.../track.json          # music: add --no-words to skip Whisper
$P library/tools/listen.py song.mp3 --vocals --out song.json           # songs: real singing timeline (~+40 s/min)
$P library/tools/listen.py clip.mp4 --out clip.json                    # a video's audio works too
```
Read it like this:
- First line `type:` - if it says speech, ignore tempo/key/mood/sections.
- `tempo ... LOW CONFIDENCE: could be X BPM` = half/double ambiguity: rerun with `--bpm-hint` (the BPM the song
  was made at, or what the cuts should follow). Trust the grid when essentia confidence > 1.5.
- Cut on `rhythm.beats_s` / `downbeats_s_estimated` (4/4 guess; low `downbeat_phase_clarity` = check with
  `strongest_hits`). `bar_s_4_4` = length of one bar.
- `loudness.integrated_lufs` (CLAUDE.md target for reels: about -16 LUFS); `clipped_samples` > 0 or
  `true_peak_dbtp_est` above 0 means it clips. `short_term_lufs_3s` shows where it gets loud/quiet.
- `voice_activity` = speech (Silero). For SINGING use `--vocals` (`vocal_stem.segments_s`): Silero found only 40%
  of the sung parts in a test song.
- Place a `data-fade-out` or a music swell only after the last speech segment ends.
- `quality.hum_suspected` / `hiss_suspected` true -> clean the voice (`clean-video-voice` skill) before using it.

## 2. Video: `watch.py`

```bash
$P library/tools/watch.py clip.mp4 --out clip_watch.json --sheet /tmp/.../sheet.png
```
Then LOOK at the sheet with Read (numbers don't say if a shot is pretty). Read it like this:
- `fps: header X / real Y` - if real < 20 or VFR/gaps: motion-interpolate to 30 fps (CLAUDE.md recipe).
- `cuts (content)` = hard cuts in the source; scenes list exposure, cast, sharpness, motion, shake, faces.
- FLAGS: shake > 1.5 px (at 320 px width) -> stabilise (this ffmpeg has `deshake` and `vidstabdetect`/`vidstabtransform`) or crop in; `soft/blurred`
  scenes -> avoid or use short; exposure `dark`/`highlights clipped` -> grade; "more warm/cool than the other
  shots" -> match the grade; flicker -> ffmpeg `deflicker`; black/frozen spans -> cut them or use the freeze on purpose.
- `faces`/`people` per scene: pick shots with the person, frame `transformOrigin` on the face.
- Most-motion seconds = candidates for speed ramps and beat hits.

Check every render the same way: `watch.py render.mp4` + `listen.py render.mp4` (cuts on beats, LUFS, no
black frames, words present).

## 3. Before/after for owner approval

```bash
$P library/tools/watch.py compare before.mp4 after.mp4 --at 1.0,3.5 --labels before,after --out cmp.png
```
Works with images too. Send `cmp.png` with SendUserFile and wait for approval before rendering (owner rule for
looks like background blur).

## 4. Fast person matte (CPU)

```bash
$P library/tools/fast_matte.py clip.mp4 alpha.mp4 --composite comp.mp4 --bg blur   # or --bg green / '#101820'
```
RVM ONNX: ~0.10 s/frame at 1080x1920 (u2net_human_seg: 0.33), steadier edges. Matte only the main person: a
second person at the frame edge may be treated as background. In Python: `from fast_matte import RVM;
m = RVM(); a = m(rgb)` - call frames in order, `m.reset()` at each new shot. How bg_blur.py could switch (3.2x
faster, not yet applied): `library/research/cpu-speed.md` -> "bg_blur.py switch".

## 5. Speed rules on this 4-core box (measured, see cpu-speed.md)

- HyperFrames: `render --workers 3` (25 s vs 40-50 s with auto for a 10 s 1080p project); `--quality draft` for looks.
- x264: don't set `-threads`; `-preset veryfast` for drafts, `medium` for finals (`slow` = 1.4x time, same SSIM).
- Several clips through an ONNX model: run them in parallel with fewer threads each (4 x 1 thread = 1.45x
  throughput). Big torch models: still one at a time (CLAUDE.md).
- Dynamic INT8 made the conv nets (RVM, MODNet) slower here; it made Whisper small 17% faster with the same words.
