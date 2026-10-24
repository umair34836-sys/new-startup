# Editing skills catalogue, part 2 (#561 onward)

4,832 new editing skills in 21 categories, written 2026-10-24 by 21 research agents and reviewed for duplicates
against #1-560 (`../skills/`) and against each other. The target was 5,000. Where a category ran out of verified
material it stopped short instead of padding (owner rule), so the real total is 4,832.

Owner rule applied to every line: verified only. Each skill carries its reference, either a page that was actually
fetched and read (URL + "checked 2026-10-24"), a local doc or `--help` output, or "(tested here 2026-10-24)" with the
exact command that ran. "Tested" means the command ran without error on synthetic clips (ffmpeg 6.1.1 etc.). It says
nothing about how the result looks or sounds unless the line gives a measured number.

Line format: `N. **Name** — what / when. **How:** steps or command (tested here …) [refs]`.

## Find a skill fast

```
python3 library/tools/find_skill.py "speed ramp"        # all words must match; prints what / how / refs
python3 library/tools/find_skill.py "denoise" --tested  # only skills whose command ran here
python3 library/tools/find_skill.py "#2836"             # one skill by number
python3 library/tools/find_skill.py --build             # rebuild index.json after editing a .md file
```

`index.json` holds every skill: id, name, category, section, tags, file, what, how, tested (true/false), refs.

Numbers are not contiguous. Each category had its own range, so there are gaps between files and where duplicates were
removed. Skills point to each other by number (for example #5121 points to #2836), so never renumber.

## Files

| File | Numbers | Skills | Tested here |
| --- | --- | --- | --- |
| [01-nle-translation.md](01-nle-translation.md) | #561-720 | 160 | 119 |
| [02-color-science.md](02-color-science.md) | #801-1040 | 240 | 115 |
| [03-color-looks.md](03-color-looks.md) | #1041-1279 | 239 | 92 |
| [04-restoration.md](04-restoration.md) | #1281-1520 | 239 | 205 |
| [05-audio-dialogue.md](05-audio-dialogue.md) | #1521-1760 | 240 | 106 |
| [06-audio-mix-master.md](06-audio-mix-master.md) | #1761-2000 | 239 | 180 |
| [07-sound-design.md](07-sound-design.md) | #2001-2236 | 236 | 121 |
| [08-music-editing.md](08-music-editing.md) | #2241-2480 | 240 | 154 |
| [09-kinetic-type-motion.md](09-kinetic-type-motion.md) | #2481-2720 | 240 | 184 |
| [10-captions-subtitles.md](10-captions-subtitles.md) | #2721-2960 | 240 | 130 |
| [11-vfx-compositing.md](11-vfx-compositing.md) | #2961-3195 | 235 | 135 |
| [12-ae-mobile-effects.md](12-ae-mobile-effects.md) | #3201-3410 | 210 | 129 |
| [13-camera-reframe-speed.md](13-camera-reframe-speed.md) | #3441-3644 | 201 | 169 |
| [14-story-genre.md](14-story-genre.md) | #3681-3920 | 240 | 20 |
| [15-retention-platform.md](15-retention-platform.md) | #3921-4158 | 238 | 15 |
| [16-thumbnails.md](16-thumbnails.md) | #4161-4399 | 239 | 114 |
| [17-delivery-export.md](17-delivery-export.md) | #4401-4640 | 240 | 210 |
| [18-workflow-automation.md](18-workflow-automation.md) | #4641-4880 | 240 | 182 |
| [19-client-business.md](19-client-business.md) | #4881-5120 | 240 | 25 |
| [20-south-asian-styles.md](20-south-asian-styles.md) | #5121-5360 | 240 | 107 |
| [21-ffmpeg-filter-reference.md](21-ffmpeg-filter-reference.md) | #5361-5556 | 196 | 193 |
| **Total** | | **4,832** | **2,705** |

## Findings that change how we work (tested here 2026-10-24)

- Urdu Nastaliq and Hindi conjuncts break in ffmpeg 6.1.1's `subtitles=` filter and in `drawtext` (empty boxes;
  सिर्फ comes out as सरि्फ). The same ASS file renders correctly through `ass=` (#2836, #5121, #5122). Convert SRT to ASS, then
  burn it with `ass=`. HyperFrames' headless Chrome renders Nastaliq correctly. Fonts are now in `library/fonts` (Noto Nastaliq
  Urdu, Noto Sans Devanagari, Noto Naskh Arabic, OFL).
- GSAP ScrambleText, the `rough` ease and `repeatRefresh` are not seek-safe (they use Math.random or re-evaluate on seek).
  HyperFrames renders by seeking, so preview and render frames can differ (files 09 and 12).
- `arnndn` speech de-noise works with the models now in `library/models/arnndn/`. It lowered pauses from -42.9 to -65.6 dB, and its
  output is 10 ms late. afftdn adds 25 ms and dialoguenhance 35 ms of delay (file 05).
- ffmpeg 6.1.1 differs from the online docs in many options (acrossfade `n`, bm3d block size, vidstab `fileformat`,
  rgbashift `wrap`, drawtext `text_align`, mpdecimate `mode`...). Each file notes what it found. Trust the tested lines over the docs.
- Copy-splitting a WhatsApp Status video with `-c copy` gave 100 s pieces instead of 90 s, because cuts land on keyframes.
  Force keyframes first (file 20).
- `-n` exits 0 when the output exists, and `exiftool -gps:all=` did not strip location from an ffmpeg-tagged MP4 (file 18).
- `web_capture.py`'s Playwright expects chromium-1194, but this container has 1243. A direct Playwright call works (file 15).

## Missing tools (from each file's "Missing tools" section; licence and source are in that file)

Not installed. Each was left for the owner to decide, never worked around with something invented.

- Restoration/AI: rife-ncnn-vulkan (MIT), realesrgan-ncnn-vulkan (MIT, needs Mesa lavapipe on CPU), Real-ESRGAN Python
  (BSD-3), untrunc (GPL-2), nnedi3 weights, QTGMC/VapourSynth, Gyroflow (GPL-3), DVRescue, lensfun, DNN-enabled ffmpeg (04, 13).
- Newer ffmpeg (7.x/8.x: drawvg, OCIO, libplacebo, xpsnr, newer vidstab), libvmaf, Tesseract for `ocr`, pyzmq (02, 06, 09, 21).
- Audio: Rubber Band CLI, SoX, aubio, Demucs CLI, Audacity, DeepFilterNet, WhisperX, faster-whisper, stable-ts, Silero VAD,
  VoiceFixer, real impulse responses, SOFA/HRTF files, a vocoder, a transient shaper, a dialog-gated loudness meter (05-08).
- Tracking/faces: MediaPipe, opencv-contrib (CSRT/KCF trackers, saliency), YuNet and OpenCV Zoo models (01, 11, 13, 16).
- Subtitles: Aegisub, ffsubsync (MIT), alass (GPL-3), a CEA-608/SCC encoder (pycaption) (10).
- Workflow: ExifTool, rsync, PySceneDetect, OpenTimelineIO, MoviePy 2, auto-editor, GNU parallel (01, 18).
- Graphics: GSAP CustomEase/EasePack files in assets/vendor, frei0r plugins (GPL), datamosh/pixelsort tools, a fire/smoke
  block, a `wdth`/`slnt` variable font, a Gurmukhi font (03, 09, 12, 13, 20).
- Other: SVT-AV1 >= 3.0, libfdk_aac, GPU encoders, a YouTube Data/Analytics API sign-in (OAuth) from the owner (15, 16, 17).

Added on 2026-10-24 because the catalogue uses them: `fonttools` and `pysubs2` in `setup-all.sh`, the arnndn models, and the Noto
fonts.
