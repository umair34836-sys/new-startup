# Reusable media library

Assets and tools made or downloaded once, kept here so new edits don't download or rebuild them.
Copy what a project needs into its own `assets/` (HyperFrames paths are project-root-relative).
Nothing personal lives here: no footage, photos, names or captions from anyone's private videos.

## Music (`music/`)

All self-made, copyright-free. 72 BPM, 4/4, so one bar = 3.333 s: cut scenes on multiples of 3.333 s.

| File | Length | Sound | Notes |
| --- | --- | --- | --- |
| `romance-bollywood-72bpm.wav` | 21.6 s | 90s Bollywood romantic: sitar intro, bansuri (flute) melody, piano arpeggios, strings, bass, dholak-style keherwa | Melody written by Magenta Improv RNN over C, Am, F, G, Am+F, C. Percussion and flute start at 3.333 s. Fade-out from 20.2 s. -15 LUFS. |
| `romance-bollywood-72bpm.mid` | 6 bars | MIDI of the above | Re-voice it (change GM programs in `tools/magenta/arrange.py`) and re-render with FluidSynth. |
| `romance-piano-72bpm.wav` | 21.6 s | Soft synthesized piano + strings + light pulse | Made by `tools/romance_synth.py` (numpy). Plainer than the Bollywood track. |

## Sound effects (`sfx/`)

| File | Notes |
| --- | --- |
| `wheel-clicks-13-steps.wav` | 13 soft clicks slowing down over 1 s (a prize wheel landing). Click k is at `1 - sqrt(1 - k/13)` s. |

19 more effects (whoosh, pop, impact-bass, riser, sparkle, ping, glitch, ...) ship inside
`.claude/skills/media-use/audio/assets/sfx/` with `manifest.json`. Get them into a project with
`npx hyperframes media-use resolve --type sfx --intent "<name>" --project . --local-only`. See the
gotchas in the root `CLAUDE.md` (the riser crests at 3.47 s, the error tone is late and quiet).

## Fonts (`fonts/`)

SIL OFL fonts (licences beside them). Load with `@font-face { src: url("assets/fonts/<file>") }`.

- `GreatVibes-Regular.ttf`: elegant script for names and romantic titles.
- `PlayfairDisplay-Italic.ttf`: serif italic for captions.

Bundled HyperFrames fonts (Inter, Archivo Black, Space Mono, Playfair Display, ...) need no file.

## Blocks (`blocks/`)

HyperFrames scenes. They load GSAP from `assets/vendor/gsap-3.14.2.min.js` (copy it from `video/assets/vendor/`).

- `light-leak-portrait.html`: the registry's organic light leak, resized to 1080x1920. Its timeline scales
  to the host's `data-duration` (1.8 s works for a cut). For a second leak in one video, copy it and rename
  `leak` / `leak-root` / `leak-` classes so ids stay unique.
- `flash-warm.html`: a 0.65 s soft warm-white flash for a cut (host `data-duration="0.7"`, start 0.2 s before the cut).

## Models (`models/`)

- `magenta/chord_pitches_improv/`: Magenta.js Improv RNN checkpoint (Apache-2.0, from
  storage.googleapis.com/magentadata). Generates a melody over a chord progression.

## Tools (`tools/`)

| Tool | What it does |
| --- | --- |
| `setup-music.sh` | One-time setup per container: apt FluidSynth + FluidR3 GM SoundFont (148 MB, too big for git), pip mido/numpy, npm Magenta.js. |
| `magenta/melody.mjs` | `node melody.mjs <checkpoint-url> out.json`: 12 Improv RNN takes over the chords, scored; best first. Serve the checkpoint with `python3 -m http.server 8766 --directory library/models/magenta/chord_pitches_improv`. Edit `seed` / `chords` inside for a new song. |
| `magenta/arrange.py` | `python3 arrange.py melody.json out.mid [temp]`: arranges a take for sitar, flute, piano, strings, bass, celesta and dholak-style percussion. |
| render | `fluidsynth -ni -q -g 0.7 -r 48000 -F out.wav /usr/share/sounds/sf2/FluidR3_GM.sf2 out.mid`, then `ffmpeg -af "atrim=0:21.6,afade=t=out:st=20.2:d=1.4,loudnorm=I=-16:TP=-1.5"`. |
| `romance_synth.py` | `python3 romance_synth.py out.wav`: the numpy piano/strings track, no installs needed. |
| `floating_hearts.py` | Writes a deterministic floating hearts + bokeh overlay scene (`--duration`, `--count`, `--burst-at` for an end-card burst, `--width/--height`). |
| `ember_background.py` | Writes the dark ember background scene used in the FireCraft video (36 rising embers + glow). |

## Colour grades that worked

Apply with `npx hyperframes media-treatment --project . --file <scene.html> --selector '#<video-id>' --grading '<json>' --apply`.

- Romantic glow (indoor phone footage, harsh window light, people):
  `{"preset":"warm-daylight","intensity":0.7,"adjust":{"exposure":0.04,"contrast":0.04,"highlights":-0.25,"shadows":0.2,"whites":-0.1,"temperature":0.12,"tint":0.04,"vibrance":0.08},"details":{"vignette":0.14}}`
