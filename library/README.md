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
| `romance-bollywood-72bpm-vocal-bed.wav` | 21.6 s | Same track with the flute melody pulled back | Bed for a voice-over or spoken lyrics (use with `tools/voice_over_music.py`). |
| `baarish-ki-pehli-shaam-ai-song.mp3` | 60 s | AI Hindi song WITH vocals (ACE-Step 1.5 turbo), romantic pop ballad, piano/guitar/strings/tabla, beats pulled back under the sung words | Lyrics in `lyrics/baarish-ki-pehli-shaam.txt`. Owner loved it. Made with `ai_song.py` defaults (seed 7, 8 steps, INT8, 80 BPM) and the caption below. |
| `romance-piano-72bpm.wav` | 21.6 s | Soft synthesized piano + strings + light pulse | Made by `tools/romance_synth.py` (numpy). Plainer than the Bollywood track. |

## Sound effects (`sfx/`)

| File | Notes |
| --- | --- |
| `wheel-clicks-13-steps.wav` | 13 soft clicks slowing down over 1 s (a prize wheel landing). Click k is at `1 - sqrt(1 - k/13)` s. |
| `phone-ring.wav` | 1.2 s desk-phone double ring (400+450 Hz, 20 Hz trill, 0.4 on / 0.2 off / 0.4 on). Made by us with numpy, no credit. Volume ~0.5. |

19 more effects (whoosh, pop, impact-bass, riser, sparkle, ping, glitch, ...) ship inside
`.claude/skills/media-use/audio/assets/sfx/` with `manifest.json`. Get them into a project with
`npx hyperframes media-use resolve --type sfx --intent "<name>" --project . --local-only`. See the
gotchas in the root `CLAUDE.md` (the riser crests at 3.47 s, the error tone is late and quiet).

## Characters (`characters/`)

- `host-skin.png`: the owner's own Minecraft skin (64x64 classic: white hoodie with hood, black hair, blue
  eyes, ripped black jeans, white shoes, red "M" on the back). **Default host for every video that needs a
  host or presenter.** Build it with `tools/blocky_character.py` (CSS 3D, no WebGL, renders anywhere).

- `girl-skin.png`: a girl partner character (long black hair, bindi, maroon kurta with gold trim, gold
  dupatta, bangles, cream salwar, gold juttis), painted by `tools/make_girl_skin.py`.

## Textures (`textures/`)

16x16 Minecraft-style block textures from `tools/voxel_textures.py` (grass, dirt, cobble, stone brick, oak and
dark-oak planks, log, leaves, lit window, door, red/white awning, red wool, lantern, iron) plus seamless rain
streak tiles `rain_blue_0/1.png` and `rain_gold_0/1.png` (512 px, slant -0.18).

## Templates (`templates/`)

- `blocky-monsoon/`: the full 60 s voxel music video for "Baarish ki pehli shaam" (owner's character meets the
  girl at a chai stall in the rain; lamps light, rain turns gold, umbrella pops on the song's peak). `build.py`
  writes `compositions/world.html` (village, characters, camera); `sky/rain/grade/titles.html` are the layers;
  `SPEC.md` has every shot. Copy the folder, copy assets (textures, skins, fonts, gsap, song) and edit `build.py`.
- `phone-clip-reel/build.py`: turns one short phone clip into a 9:16 "Boss mode" reel (Oct 2026 client edit): one shot per
  bar at 105 BPM, title card at 0 s, zoom-through / whip / light leak / punch-in / flash transitions, slow-mo end with
  letterbox bars and a check-mark pop, end card on a hero frame, Roman Urdu captions (Plus Jakarta 800 + Anton titles,
  gold accent words), SFX lanes and the cinematic-muted grade. Needs `assets/clips/c1..c6.mp4` (2.3 s each, 1080x1920)
  and `hero.jpg`; run `python3 build.py`, then check / snapshot / render.

## Lyrics (`lyrics/`)

- `baarish-ki-pehli-shaam.txt`: 1-minute Hindi love story (rain, a tea stall, first meeting), ACE-Step section tags.

## Fonts (`fonts/`)

SIL OFL fonts (licences beside them). Load with `@font-face { src: url("assets/fonts/<file>") }`.

- `GreatVibes-Regular.ttf`: elegant script for names and romantic titles.
- `PlayfairDisplay-Italic.ttf`: serif italic for captions.
- `Anton-Regular.ttf` (+ `Anton-OFL.txt`): tall condensed display font for punchy titles ("BOSS", "PEHCHAAN").

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
| `setup-all.sh` | Installs everything (`light`: Agent-Reach, graft; `heavy`: music + ACE-Step/Whisper + weights). Run automatically by the SessionStart hook. |
| `setup-agent-tools.sh` | Agent-Reach + graft only (also part of setup-all.sh light). |
| `setup-music.sh` | One-time setup per container: apt FluidSynth + FluidR3 GM SoundFont (148 MB, too big for git), pip mido/numpy, npm Magenta.js. |
| `magenta/melody.mjs` | `node melody.mjs <checkpoint-url> out.json`: 12 Improv RNN takes over the chords, scored; best first. Serve the checkpoint with `python3 -m http.server 8766 --directory library/models/magenta/chord_pitches_improv`. Edit `seed` / `chords` inside for a new song. |
| `magenta/arrange.py` | `python3 arrange.py melody.json out.mid [temp]`: arranges a take for sitar, flute, piano, strings, bass, celesta and dholak-style percussion. |
| render | `fluidsynth -ni -q -g 0.7 -r 48000 -F out.wav /usr/share/sounds/sf2/FluidR3_GM.sf2 out.mid`, then `ffmpeg -af "atrim=0:21.6,afade=t=out:st=20.2:d=1.4,loudnorm=I=-16:TP=-1.5"`. |
| `romance_synth.py` | `python3 romance_synth.py out.wav`: the numpy piano/strings track, no installs needed. |
| `voice_over_music.py` | `python3 voice_over_music.py spec.json out.wav`: places voice lines (cut from one take by transcript word timings) at chosen film times, speeds a line up only if it overruns, polishes the voice, ducks the bed 8 dB under it and sets the voice 5.5 dB over the bed. Spec format is in the file header. |
| `ai_voice.py` | Script -> spoken Hindi/Hinglish voiceover, music ZERO: ACE-Step speaks each line, Whisper picks the best take per line, BS-RoFormer removes the music, lines joined with pauses. See skill voice-or-song. |
| `vs_tts.py` | Script -> spoken voiceover through VoiceStudio (OmniVoice/VoxCPM2): Urdu/Hindi/Pashto, voice design text, cloning. Start the backend with `voicestudio.sh start`. OmniVoice is non-commercial. |
| `voicestudio.sh` | start / stop / status of the VoiceStudio backend (:3900, OpenAPI + MCP). |
| `clean_voice.py` | Video/audio with speech -> only the person's voice (BS-RoFormer vocals + Mel-RoFormer denoise, optional de-reverb), put back into the video as clean.mp4. Skill clean-video-voice. |
| `web_capture.py` | Free Firecrawl replacement (Crawl4AI): URL -> markdown + full-page screenshot via local Chromium; domain must be network-allowed. |
| `music_pack.py` | Many own songs/instrumentals (ACE-Step) in ONE model load from a JSON spec -> mp3 at -14 LUFS. Ours: no credit needed. |
| `setup-ai-song.sh` | Installs ACE-Step 1.5 (lyrics -> song with vocals) and OpenAI Whisper into /home/user/tools/venv. Weights need huggingface.co + openaipublic.azureedge.net allowed. |
| `ai_song.py` | Full pipeline: song with vocals from lyrics (turbo text2music) -> Whisper finds where words are sung -> bass and cymbal bands lowered there, voice band lifted -> Whisper transcript compared to the lyrics (`report.json`). Resumable; run it in the background (CPU). |
| `blocky_character.py` | `python3 blocky_character.py compositions/host.html --skin assets/characters/host-skin.png --duration 6 --scale 16 --moves '[[0,"idle"],[1,"wave"],[3,"talk"]]'`: a 3D Minecraft-style character scene from a 64x64 skin. Poses: idle, wave, talk, walk, point, spin; `--turn`, `--tilt`, `--x/--y` place it. Copy the skin into the project's assets first. |
| `voxel_world.py` | CSS 3D voxel worlds for HyperFrames: `World.box/plane/group/raw`, a camera rig (dolly, pitch, yaw, target) and `camera_js` keyframes. Faces take a texture name or a CSS colour. |
| `voxel_textures.py` | Paints the 16x16 block textures into a folder. |
| `make_girl_skin.py` | Paints `characters/girl-skin.png`. |
| `floating_hearts.py` | Writes a deterministic floating hearts + bokeh overlay scene (`--duration`, `--count`, `--burst-at` for an end-card burst, `--width/--height`). |
| `ember_background.py` | Writes the dark ember background scene used in the FireCraft video (36 rising embers + glow). |

## Colour grades that worked

Apply with `npx hyperframes media-treatment --project . --file <scene.html> --selector '#<video-id>' --grading '<json>' --apply`.

- Cinematic muted (office/shop phone footage with loud cyan/blue surfaces; tames the cyan, keeps skin warm; client reel):
  `{"preset":"skin-soft","intensity":0.6,"adjust":{"exposure":-0.04,"contrast":0.18,"highlights":-0.35,"shadows":0.05,"blacks":-0.06,"temperature":0.1,"saturation":-0.22},"details":{"vignette":0.28,"grain":0.06,"grainSize":0.2}}`
- Romantic glow (indoor phone footage, harsh window light, people):
  `{"preset":"warm-daylight","intensity":0.7,"adjust":{"exposure":0.04,"contrast":0.04,"highlights":-0.25,"shadows":0.2,"whites":-0.1,"temperature":0.12,"tint":0.04,"vibrance":0.08},"details":{"vignette":0.14}}`

## fonts (added)

`fonts/PlusJakartaSans-Variable.ttf` (OFL, weights 200-800): TalkEmber Studio's brand font.

## research/

Facts gathered by tools and web research, one topic per file (source + date), so nothing is looked up twice:
`firecraft-smp.md` (server facts for promos), `tools-landscape.md` (open-source tools and star counts),
`video-editing.md` (editing techniques), `talkember-studio.md` (the owner's website, for promos).

## templates/website-promo

Song + HyperFrames walkthrough video of a real website (TalkEmber Studio promo, Oct 2026): build.py, alignment (dp_align.py), multi-part song generation. See its README.

## music (added)

`music/talkember-studio-promo-song.mp3`: 6 min upbeat Hindi pop promo song about TalkEmber Studio (ACE-Step, 3 parts joined at 96.0 s and 212.5 s); line timings in `templates/website-promo/talkember-timing.json`.

## music/cc0

29 CC0 tracks (no credit needed) from OpenGameArt, verified per page: background (lofi, bossa nova, happy, town), cinematic (epic, choir, battle, tragic), piano, desi/eastern (tabla, sitar style, Arabic, desert, oriental). List and moods: `music/cc0/README.md`.
