# Reusable media library

Assets and tools made or downloaded once, kept here so new edits don't download or rebuild them.
Copy what a project needs into its own `assets/` (HyperFrames paths are project-root-relative).
Nothing personal lives here: no footage, photos, names or captions from anyone's private videos.

Full inventory of installed tools, models, scripts and skills (sizes, licences, where they live): `TOOLS-INVENTORY.md`.

## Music (`music/`)

The table below is self-made, copyright-free. The three 72 BPM tracks are 4/4, so one bar = 3.333 s: cut scenes on
multiples of 3.333 s. CC0 tracks by others: `music/cc0/` (131 files); our ACE-Step tracks: `music/own/` (9).
Audit 2026-10-24: lengths (ffprobe) and loudness (ffmpeg ebur128) below re-measured: romance-bollywood -15.0 LUFS,
vocal bed -16.0, piano -15.6, baarish -13.0, talkember promo song -13.5 (362.5 s).

| File | Length | Sound | Notes |
| --- | --- | --- | --- |
| `romance-bollywood-72bpm.wav` | 21.6 s | 90s Bollywood romantic: sitar intro, bansuri (flute) melody, piano arpeggios, strings, bass, dholak-style keherwa | Melody written by Magenta Improv RNN over C, Am, F, G, Am+F, C. Percussion and flute start at 3.333 s. Fade-out from 20.2 s. -15 LUFS. |
| `romance-bollywood-72bpm.mid` | 6 bars | MIDI of the above | Re-voice it (change GM programs in `tools/magenta/arrange.py`) and re-render with FluidSynth. |
| `romance-bollywood-72bpm-vocal-bed.wav` | 21.6 s | Same track with the flute melody pulled back | Bed for a voice-over or spoken lyrics (use with `tools/voice_over_music.py`). |
| `baarish-ki-pehli-shaam-ai-song.mp3` | 60 s | AI Hindi song WITH vocals (ACE-Step 1.5 turbo), romantic pop ballad, piano/guitar/strings/tabla, beats pulled back under the sung words | Lyrics in `lyrics/baarish-ki-pehli-shaam.txt`. Owner loved it. Made with `ai_song.py` defaults (seed 7, 8 steps, INT8, 80 BPM) and the caption below. |
| `romance-piano-72bpm.wav` | 21.6 s | Soft synthesized piano + strings + light pulse | Made by `tools/romance_synth.py` (numpy). Plainer than the Bollywood track. |

## Desi songs with vocals (`music/desi-vocal/`)

29 public-domain Urdu/Hindustani songs WITH vocals (14 Urdu, 15 Hindi, 0 Pashto): 78 rpm gramophone records 1905-1919
from archive.org (Gauhar Jaan, Janki Bai, Iqbal's "Saare Jahan Se Achha" 1919...), 96 MB. Licence reasoning from the
Indian/Pakistani/US law texts and every source page in `music/desi-vocal/README.md` + `index.json` (specialist B,
2026-10-24; spot-checked by the main session: archive.org item a-4294903-1483330581-3381 says "Released: Jan 1916").
Old shellac sound: noisy, mono. 446 more candidate records: research/data/archive-org-78rpm-hindustani-1902-1922.tsv.

## Sound effects (`sfx/`)

| File | Notes |
| --- | --- |
| `wheel-clicks-13-steps.wav` | Clicks slowing down (a prize wheel landing); file 1.5 s, first sound at 0.083 s (measured 2026-10-24). "13 clicks, click k at `1 - sqrt(1 - k/13)` s" is the design note: an onset count on the file was ambiguous (each click rings), so the timing is unverified. |
| `phone-ring.wav` | 1.2 s desk-phone double ring (400+450 Hz, 20 Hz trill, 0.4 on / 0.2 off / 0.4 on; length, the two tones and the on/off pattern measured 2026-10-24, the trill not). Made by us with numpy, no credit. Volume ~0.5. |

19 more effects (19 mp3 files, counted 2026-10-24: whoosh, pop, impact-bass, riser, sparkle, ping, glitch, ...) ship inside
`.claude/skills/media-use/audio/assets/sfx/` with `manifest.json`. Get them into a project with
`npx hyperframes media-use resolve --type sfx --intent "<name>" --project . --local-only`. See the
gotchas in the root `CLAUDE.md` (the riser crests at 3.47 s, the error tone is late and quiet: both re-measured 2026-10-24).

## Meme SFX (`memes/sfx/`, added 2026-10-25)

10 CC0 comedy / meme-style sounds (sad trombone, ba-dum-tss + crickets, cricket chirp, wink sparkle, cartoon blink,
cartoon fall, cartoon squeak, boing, squeaky toy honk, spring boing), MP3 from StoryCut's free page, each original's
Freesound page checked as "Creative Commons 0" on 2026-10-25. No credit needed. Proof + lengths/levels:
`memes/sfx/licence_proof.json`. How/when to use meme SFX and the copyright rules: `research/memes.md`.

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

- `brand-identity-reveal/`: 16:9 ~30 s music-only brand identity / guidelines film driven by one reveal.json (logo construction
  from the real traced mark via mark_to_svg.py, lockup, browser/phone mockups, stacked page cards, typography, colour
  swatches, stat widgets, price chart, photo inserts, social post, end logo; scenes counted in beats from the music drop).
  HostLixo, 2026-10-27; README has QA numbers and the gain+limiter mastering step.

- `screen-tutorial/`: real-site tutorial (cursor + click ripple + click sound on every click, VO-timed speed-fit of the
  recording, step chips, highlight rings). Recorder: tools/screen_recorder.js; VO check: tools/wcheck_lines.py. FireCraft whitelist, 2026-10-24.

- `blocky-monsoon/`: the full 60 s voxel music video for "Baarish ki pehli shaam" (owner's character meets the
  girl at a chai stall in the rain; lamps light, rain turns gold, umbrella pops on the song's peak). `build.py`
  writes `compositions/world.html` (village, characters, camera); `sky/rain/grade/titles.html` are the layers;
  `SPEC.md` has every shot. Copy the folder, copy assets (textures, skins, fonts, gsap, song) and edit `build.py`.
- `kinetic-laptop-type/build.py`: 16:9 kinetic typography inside a CSS laptop (search bar, word-by-word blur reveal, end screen); skills #404, #2560/#2561, #3107. First used for SkilloraClouds, 2026-10-24. See its README.
- `food-promo-reel/build_pizzabase.py`: 9:16 ~36 s restaurant deal promo from the site's own food photos + deal posters, scenes timed from VO lines.json (Pizza Base PK, 2026-10-25; README in the folder).
- `minecraft-smp-short/build.py`: 9:16 ~62 s Minecraft server promo Short from a client's own VO + gameplay recordings
  (ALOO SMP, 2026-10-25): word-timed Hinglish captions (Whisper medium words, one gold word, never overlapping groups),
  shots cut on the music's beat grid and matched to each VO line, 9:16 crop + lanczos + CAS sharpen, blurred-fill for
  readable chat shots, hook title at 0 s, logo flash/shake reveal, feature checklist chips on the spoken words,
  24x7/NO WHITELIST stamp, JAVA+BEDROCK cards, end card (logo, IP, port, join, Discord), SFX lanes. See its README.
- `hosting-promo-reel/build.py`: 9:16 ~32 s website/hosting promo synced to a voiceover (hook, logo, specs over a real
  panel screenshot, '<60 SECONDS' ring, location flags, price card, coupon card, end card). See its README.
- `blocky-walk/build.py`: 16:9 21.5 s, host + girl skins walk down a sunny voxel village lane (4 shots cut on music downbeats, CC0 town-theme-rpg). Made 2026-10-26; see its README.
- `kinetic-type-reel/build_pakwebhoster.py`: 9:16 20 s kinetic typography reel, no VO (beat-synced word slams out of masks,
  full-screen colour flips per spec, price slam, end card); beat grid from listen.py. PakWebHoster, 2026-10-25. See its README.
- `typewriter-reel/build_pakwebhoster.py`: 9:16 20 s typewriter reel, no VO (editor window, characters typed with uneven
  gaps + caret + keyboard SFX, URL typed into an address bar). PakWebHoster, 2026-10-25. See its README.
- `editor-portfolio/build.py`: video-editor portfolio / showreel, 16:9 and 9:16 from one JSON config (avatar + "Hi, I'M
  NAME" + freelance tag, "Want a video EDITOR?", one section per brand with its real clips (verticals side by side),
  SFX placed by measured peak on the beat, 6-clip wall with
  counted "N VIDEOS • M BRANDS", contact end card). MrCopper804's own portfolio, 2026-10-27. See its README.
- `hosting-promo-reel/build_pakwebhoster.py`: light-theme 30 s Rs 200 shared-hosting reel with the free default voice. PakWebHoster, 2026-10-25.
- `brand-kit/`: client branding kit: `brand.json` schema + fake example, `brand_from_logo.py` (palette + WCAG text colours from a logo), `build_brand.py` (logo sting, lower third, contact card with local QR, watermark, CTA, offer badge; 9:16 and 16:9). Intake questionnaire: research/client-intake.md. Skill client-brand-kit.
- `phone-clip-reel/build.py`: turns one short phone clip into a 9:16 "Boss mode" reel (Oct 2026 client edit): one shot per
  bar at 105 BPM, title card at 0 s, zoom-through / whip / light leak / punch-in / flash transitions, slow-mo end with
  letterbox bars and a check-mark pop, end card on a hero frame, Roman Urdu captions (Plus Jakarta 800 + Anton titles,
  gold accent words), SFX lanes and the cinematic-muted grade. Needs `assets/clips/c1..c6.mp4` (2.3 s each, 1080x1920)
  and `hero.jpg`; run `python3 build.py`, then check / snapshot / render.

## Lyrics (`lyrics/`)

- `baarish-ki-pehli-shaam.txt`: 1-minute Hindi love story (rain, a tea stall, first meeting), ACE-Step section tags.

## Emoji (`emoji/noto/`)

21 Noto Emoji 512 px PNGs (Apache-2.0, no on-screen credit needed). Upstream match is md5-checked; see `emoji/noto/README.md`.

## Fonts (`fonts/`)

SIL OFL fonts (licences beside them; audit 2026-10-24: every .ttf's name table says "licensed under the SIL Open Font
License" and every font family has an OFL .txt here). Load with `@font-face { src: url("assets/fonts/<file>") }`.

- `GreatVibes-Regular.ttf`: elegant script for names and romantic titles.
- `PlayfairDisplay-Italic.ttf`: serif italic for captions.
- Urdu/Pashto/Hindi (specialist D, Oct 24 2026; see library/research/urdu-captions.md): `NotoNastaliqUrdu-Variable.ttf`,
  `Gulzar-Regular.ttf` (Urdu only: no Pashto letters), `NotoNaskhArabic-Variable.ttf`, `NotoSansArabic-Variable.ttf`,
  `Vazirmatn-Variable.ttf`, `NotoSansDevanagari-Variable.ttf`, `Mukta-Regular/Bold.ttf` (Hindi). OFL licences beside them.
- `Anton-Regular.ttf` (+ `Anton-OFL.txt`): tall condensed display font for punchy titles ("BOSS", "PEHCHAAN").
- `TikTokSans-Variable.ttf` (+ `TikTokSans-OFL.txt`, OFL 1.1, Copyright 2024 TikTok Inc., github.com/tiktok/TikTokSans): variable font with axes opsz 12-36, wdth 75-150, wght 300-900, slnt -6-0 (fontTools, 2026-10-26). From the owner's Drive folder, 2026-10-26.
- `Poppins-SemiBold/Bold/ExtraBold.ttf` (+ `Poppins-OFL.txt`, from github.com/google/fonts ofl/poppins, 2026-10-25): Pizza Base PK site font (computed CSS).
- `Kalam-Bold.ttf` (+ `OFL-Kalam.txt`) and `RozhaOne-Regular.ttf` (+ `OFL-RozhaOne.txt`): also present (found in the
  2026-10-24 audit; not described before).

- Same Noto files, details (self-study skills2): `NotoNastaliqUrdu-Variable.ttf` (wght 400-700). Burn with ffmpeg `ass=` (not `subtitles=`, which
  showed empty boxes in ffmpeg 6.1.1; skills2/10). `NotoSansDevanagari-Variable.ttf` (wght 100-900, wdth 62.5-100): Hindi.
  `NotoNaskhArabic-Variable.ttf` (wght 400-700): Arabic Naskh. All SIL OFL 1.1 (Noto*-OFL.txt), from github.com/google/fonts (2026-10-24).

Bundled HyperFrames fonts (Inter, Archivo Black, Space Mono, Playfair Display, ...) need no file.

## Blocks (`blocks/`)

HyperFrames scenes. They load GSAP from `assets/vendor/gsap-3.14.2.min.js` (copy it from `video/assets/vendor/`).

- `light-leak-portrait.html`: the registry's organic light leak, resized to 1080x1920. Its timeline scales
  to the host's `data-duration` (1.8 s works for a cut). For a second leak in one video, copy it and rename
  `leak` / `leak-root` / `leak-` classes so ids stay unique.
- `flash-warm.html`: a 0.65 s soft warm-white flash for a cut (host `data-duration="0.7"`, start 0.2 s before the cut).

## Emoji + line icons (`elements/`, added 2026-10-26)

Licence-clean pack for explainer/faceless videos (PC security for gamers): 41 Microsoft Fluent 3D emoji (MIT, 256 px PNG),
43 Google Noto emoji (Apache-2.0, 512 px PNG) + India flag (public domain, flat PNG + waved SVG), 36 Lucide (ISC) and
4 Tabler (MIT) line-icon SVGs. Concepts: warning, siren, skull, bug, virus, lock/unlock, key, shield, laptop, desktop,
fan/wind, mail, money, coin, chart down, controller, joystick, download, package/folder/zip, link, speech, robot,
thinking/scream/exploding faces, check/cross, no entry/prohibited, eyes, red flag, hourglass, detective/magnifier,
globe, fire, thumbs up, India flag. Concept table: `elements/README.md`; per-file proof (pinned source URL, licence
line, date, sha256): `elements/licence_proof.json`; licence texts: `elements/licences/`. No on-screen credit needed;
no Twemoji/OpenMoji, no brand logos. Notes: `research/emoji-icon-sets.md`.

## Stock b-roll, SFX and LUTs (specialist C, merged 2026-10-24)

No-credit only; every entry's `licence_proof` (URL, date, quoted licence text) is in each folder's `index.json`.
Search: `python3 tools/find_stock.py "<words>" [--sfx|--lut|--all] [--vertical]`. Skill: `stock-sfx-luts`.

- `stock/`: 67 clips, 203 MB (37 own-made overlays/backgrounds, 17 CC0, 11 public domain, 2 NASA via Commons marked
  `licence_doubt`: space/gaming intros only, not client ads). `stock/mixkit-links.json`: Mixkit links only (their terms
  forbid re-sharing as stock): fetch one clip per need with `--fetch-mixkit <id> <dst>`, never commit Mixkit files.
- `sfx/`: 164 files, 7.4 MB (Kenney + OpenGameArt CC0, plus own `tools/synth_sfx.py`), each with length, hit time, levels.
- `luts/`: 32 own-made `.cube` LUTs (`tools/make_luts.py`, previews by `tools/lut_preview.py`).
- Tools: `stock_prep.py`, `sfx_prep.py`, `make_overlays.py`, `synth_sfx.py`, `make_luts.py`, `lut_preview.py`, `find_stock.py`.
- Merge check (2026-10-24, main session): Commons pages re-read here for rain-dripping (API: CC0, attribution not required)
  and clouds time-lapse ("CC0 1.0 Universal Public Domain Dedication"); 5 clips the specialist dropped (CC BY-SA /
  unreviewed / NASA no-licence) are not in this branch's history (squash merge).

## Models (`models/`)

- `arnndn/`: 6 RNNoise `.rnnn` models for ffmpeg's `arnndn` speech de-noise (std = Xiph RNNoise, BSD-style; others by Gregor
  Richards, not copyrighted). See `models/arnndn/README.md`.

- `magenta/chord_pitches_improv/`: Magenta.js Improv RNN checkpoint (Apache-2.0 = @magenta/music licence on npm, checked 2026-10-24; from
  storage.googleapis.com/magentadata). Generates a melody over a chord progression.

## Tools (`tools/`)

| Tool | What it does |
| --- | --- |
| `setup-all.sh` | Installs everything (`light`: ffmpeg, PIL/numpy/mido/pyworld, Agent-Reach, graft, REA, Crawl4AI, specialist-D fonts tools; `heavy`: music + ACE-Step/Whisper + weights, audio-separator, VoiceStudio). Run automatically by the SessionStart hook. |
| `setup-agent-tools.sh` | Agent-Reach + graft only (also part of setup-all.sh light). |
| `setup-music.sh` | One-time setup per container: apt FluidSynth + FluidR3 GM SoundFont (fluid-soundfont-gm, Installed-Size 145,172 kB per apt-cache 2026-10-24; too big for git), pip mido/numpy, npm Magenta.js. |
| `magenta/melody.mjs` | `node melody.mjs <checkpoint-url> out.json`: 12 Improv RNN takes over the chords, scored; best first. Serve the checkpoint with `python3 -m http.server 8766 --directory library/models/magenta/chord_pitches_improv`. Edit `seed` / `chords` inside for a new song. |
| `magenta/arrange.py` | `python3 arrange.py melody.json out.mid [temp]`: arranges a take for sitar, flute, piano, strings, bass, celesta and dholak-style percussion. |
| render | `fluidsynth -ni -q -g 0.7 -r 48000 -F out.wav /usr/share/sounds/sf2/FluidR3_GM.sf2 out.mid`, then `ffmpeg -af "atrim=0:21.6,afade=t=out:st=20.2:d=1.4,loudnorm=I=-16:TP=-1.5"`. |
| `romance_synth.py` | `python3 romance_synth.py out.wav`: the numpy piano/strings track, no installs needed. |
| `voice_over_music.py` | `python3 voice_over_music.py spec.json out.wav`: places voice lines (cut from one take by transcript word timings) at chosen film times, speeds a line up only if it overruns, polishes the voice, ducks the bed 8 dB under it and sets the voice 5.5 dB over the bed. Spec format is in the file header. |
| `find_music.py` | `python3 find_music.py "<video type / mood>" [--length 30] [--client] [--vo] [--drop] [--platform youtube]`: ranks catalogue tracks for a video (type tag, energy, tempo band, steady grid, real ending, drop, fast intro, steady level under VO) and prints why each fits / what to watch. Licence filters: client = CC0/PD only, YT Audio Library only for YouTube, own tracks only with --own, vocals never under a VO. Skill music-for-video. |
| `fetch_free_music.py` | `python3 fetch_free_music.py "<words>" --category <catalogue category> [--n 5] [--genre Ambient] [--min-sec 60 --max-sec 240] [--any-artist] [--dry-run]`: fetches NO-CREDIT music from the Free Music Archive (public-domain filter) into `music/cc0`: re-reads every track page and keeps only CC0 1.0 / PD-mark licence links (no licenses/by), only artists who release everything CC0 unless --any-artist, re-encodes to 160 kbps, adds index.json + README rows; then `music_catalogue.py --only <file>` measures it for find_music.py. Research: research/music-fetch-tools.md. |
| `ia` (CLI) | Internet Archive's own command-line tool (`ia search`, `ia download`; pip internetarchive, setup-all light). archive.org licence tags are set by uploaders and are often wrong: never use them as proof. |
| `music_fit.py` | perc-venv: cuts/stitches a track to an EXACT length on downbeat->downbeat joins (40 ms equal-power, snapped to the onset), loops by 4-bar phrases, `--drop-at T` lands the measured drop on T, `--end resolve` keeps the real ending (loops/fade-outs end on a downbeat hit + ring-out), `--check` re-measures beat phase across each join. |
| `mix_vo_music.py` | perc-venv: finished VO + fitted bed -> mix: duck -10 dB (60/400 ms, 0.5 s hold), 1.5-4 kHz dip under speech, voice 15 LU over the ducked bed, -16 LUFS / -1 dBTP; reports the music-vs-VO gap. |
| `music_catalogue.py` / `music_analysis.py` | perc-venv: measures every repo track with listen.py (one at a time, resumable; raw reports in /home/user/tools/music-reports) -> `music/catalogue.json` + `catalogue.md` (BPM/alt, key, LUFS, energy, first full bar, drop, ending type + where it starts, vocals, licence/client OK, video types). `--owner-drive DIR` adds the owner's Drive tracks. |
| `ai_voice.py` | Script -> spoken Hindi/Hinglish voiceover, music ZERO: ACE-Step speaks each line, Whisper picks the best take per line, BS-RoFormer removes the music, lines joined with pauses. See skill voice-or-song. |
| `listen.py` | Audio/video -> facts (run with /home/user/tools/perc-venv/bin/python): BPM + beat grid, downbeats, hits, LUFS curve, sections, silence, voice activity, `--vocals` singing timeline, key, hum/hiss/clipping, Whisper words. Tested here 2026-10-24: pashto-rabab-folk-bg (made at 105 BPM) -> 105.0 BPM. Skill listen-and-watch. |
| `watch.py` | Video -> facts: real fps from timestamps, cuts, shake, flicker, sharpness, exposure/cast per scene, faces/people, black/frozen frames, contact sheet, `compare` mode. Tested here 2026-10-24: client WhatsApp clip -> real 12.4 fps, 134 frames, flagged 'motion-interpolate to 30'. |
| `fast_matte.py` | Fast CPU person matte (Robust Video Matting ONNX); benchmarks and the optional bg_blur.py switch in research/cpu-speed.md. |
| `urdu_captions.py` | Urdu/Pashto/Hindi captions for HyperFrames (Nastaliq shaping, RTL, per-word reveal; `--check` verifies a font has the needed letters). Block: `blocks/urdu-captions.html`. Skill urdu-captions. |
| `vs_tts.py` | Script -> spoken voiceover through VoiceStudio (OmniVoice/VoxCPM2): Urdu/Hindi/Pashto, voice design text, cloning. Start the backend with `voicestudio.sh start`. OmniVoice is non-commercial. |
| `vo_join.py` | Join chosen VO line takes (other seeds/rewordings from several vs_tts.py --parts runs) into one VO: each line pitch-matched to one median f0 (default 172 Hz), gap, loudnorm -16, lines.json. Made 2026-10-25 (PakWebHoster reel). |
| `voicestudio.sh` | start / stop / status of the VoiceStudio backend (:3900, OpenAPI + MCP). |
| `align_lyrics.py` | `python3 align_lyrics.py lyrics.txt words.json out.json`: start/end of every lyric line inside a song from Whisper word timings, by one global in-order character alignment (a weak line can't shift later ones). Smoke-tested 2026-10-24 on Whisper words of a VoxCPM2 take. |
| `watermark.py` | Unpaid-preview copyright mark for client videos: diagonal tiled "Made by MrCopper804" over the whole frame (16% alpha, hard to crop), a solid "PREVIEW · © 2026 MrCopper804" corner tag, and copyright/artist/comment metadata. Send the clean render after payment. First used on the SkilloraClouds reel, 2026-10-24 (32.5 s 1080x1920 re-encode, crf 18). |
| `bg_blur.py` | Portrait-mode background for phone footage: person (rembg u2net_human_seg + dark-shirt hull fill, temporally smoothed) and the desk stay sharp; background gets the subject inpainted out (no halo), lens/bokeh blur in linear light, blue/cyan objects desaturated into the wall, -14% exposure. Owner approved it on the client boss reel (Oct 2026). |
| `clean_voice.py` | Video/audio with speech -> only the person's voice (BS-RoFormer vocals + Mel-RoFormer denoise, optional de-reverb), put back into the video as clean.mp4. Skill clean-video-voice. |
| `find_skill.py` | `python3 find_skill.py "speed ramp"` searches the editing skills catalogue (skills + skills2) and prints the How lines; `--tested`, `#<id>`, `--build` (index.json). |
| `youtube_chapters.py` | Validates/prints a YouTube chapter list (00:00 first, >=3, ascending, >=10 s each). |
| `web_capture.py` | Free Firecrawl replacement (Crawl4AI): URL -> markdown + full-page screenshot via local Chromium; domain must be network-allowed. 2026-10-24: a container with only chromium-1243 made it fail (playwright 1.56.0 wants chromium-1194); fixed the same day: it then starts the image's own Chromium and attaches over CDP (tested on example.com). |
| `screen_recorder.js` | Tutorial/screen-video recorder (Node + Playwright): drives a real site, draws a visible mouse cursor that glides to each target and plays a press + ripple on every click, `fakeClick` = the same animation WITHOUT clicking (never submit live forms), records via the CDP screencast (sharp JPEG frames) and encodes recording.mp4 at 30 fps plus events.json (click times/positions for click sounds). `zoom: 1.25` makes UI text big and still sharp at 1080p (deviceScaleFactor does not help: screencast frames are DIP-sized). First used on the FireCraft whitelist tutorial, 2026-10-24 (66 s recording, 1,458 frames). Run with `NODE_PATH="$(npm root -g)"`. |
| `wcheck_lines.py` | Whisper-check TTS lines: `venv/bin/python wcheck_lines.py script.txt 000.wav 001.wav ...` prints similarity to each script line and the last word's end (a run-on tail shows as extra words / end near the clip end). `--same` checks several takes of line 1. |
| `music_pack.py` | Many own songs/instrumentals (ACE-Step) in ONE model load from a JSON spec -> mp3 normalised toward -14 LUFS (the 9 files in music/own measure -12.9 to -14.1 LUFS, ebur128 2026-10-24). Ours: no credit needed. |
| `setup-ai-song.sh` | Installs ACE-Step 1.5 (lyrics -> song with vocals) and OpenAI Whisper into /home/user/tools/venv. Weights need huggingface.co + openaipublic.azureedge.net allowed. |
| `ai_song.py` | Full pipeline: song with vocals from lyrics (turbo text2music) -> Whisper finds where words are sung -> bass and cymbal bands lowered there, voice band lifted -> Whisper transcript compared to the lyrics (`report.json`). Resumable; run it in the background (CPU). |
| `blocky_character.py` | `python3 blocky_character.py compositions/host.html --skin assets/characters/host-skin.png --duration 6 --scale 16 --moves '[[0,"idle"],[1,"wave"],[3,"talk"]]'`: a 3D Minecraft-style character scene from a 64x64 skin. Poses: idle, wave, talk, walk, run, point, hold, spin, shrug, think, shock, no, nod; `--turn`, `--tilt`, `--x/--y` place it; `--beats '[[t,strength],...]'` makes "talk" nod on each spoken word (pass the VO's word starts); `--path '[[t,x,y,scale,flip,dur],...]'` moves/resizes/mirrors the character between layouts (added 2026-10-26, Mr Aloo explainer). Copy the skin into the project's assets first. |
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
`fonts/Manrope-Variable.ttf` (+ `OFL-Manrope.txt`, weights 200-800) and `fonts/Ubuntu-Regular.ttf` / `Ubuntu-Bold.ttf`
(+ `Ubuntu-UFL.txt`, Ubuntu Font Licence 1.0, free to use and embed): PakWebHoster's site fonts (Manrope body/headings,
Ubuntu theme font; loaded fonts read in Chromium 2026-10-25). From github.com/google/fonts (ofl/manrope, ufl/ubuntu), 2026-10-25.
`fonts/JetBrainsMono-Variable.ttf` (+ `OFL-JetBrainsMono.txt`, OFL, weights 100-800): HostLixo's mono label font (site
loads Space Grotesk 700 + Plus Jakarta Sans + JetBrains Mono, read in Chromium 2026-10-27). From github.com/google/fonts
(ofl/jetbrainsmono), 2026-10-27.

## vendor/

`gsap-3.14.2.min.js`, `TextPlugin-3.14.2.min.js`, `SplitText-3.14.2.min.js`: from `npm pack gsap@3.14.2` (dist/),
GreenSock standard "no charge" licence (https://gsap.com/standard-license), fetched 2026-10-25. Copy into a project's
assets/vendor/ (never load GSAP from the CDN in HyperFrames).

## clients/

One folder per client: `brief.md` (facts + brand + voice + delivered), `site-data.md` (every fact from a full browser
crawl, with page + date), `site/` (page text, crawl/screenshot tools, images.json). Site photos/screenshots are never
committed (owner rule 2026-10-26): re-make them per job in the scratchpad.
`moradosolution/` (branch client-moradosolution), `pakwebhoster/` (pakwebhoster.com, crawl 2026-10-25).

## research/

Facts gathered by tools and web research, one topic per file (source + date), so nothing is looked up twice:
`firecraft-smp.md` (server facts for promos), `firecraft-whitelist-flow.md` (real whitelist steps + exact field labels, 2026-10-24), `tools-landscape.md` (open-source tools and star counts),
`video-editing.md` (editing techniques), `pk-reels-trends.md` + `pk-reel-recipes.md` (Pakistani reels styles, 16 recipes), `desi-vocal-sources.md`, `perception-tools.md` + `cpu-speed.md` (specialist A: what listen/watch measure; CPU benchmarks), `editing/` (decision guide for 29 video types + 560 cited editing skills), `talkember-studio.md` (the owner's website, for promos),
`free-music-sources.md` (no-credit music sources), `hinglish-tts.md` and `voicestudio.md` (voice models),
`network-allowlist.md` (domains), `urdu-captions.md`, `client-intake.md`, `audit-2026-10-24-part1.md` (claim audit), `tiktok-access.md`, `emoji-icon-sets.md` (Fluent/Noto/Lucide/Tabler licences + layout, 2026-10-26), `artemis.md` (google/artemis Android phone agent: installed in /home/user/tools/artemis, needs a phone + API key), `open-design.md` (nexu-io/open-design AI design workspace: /home/user/tools/open-design, Node 24 in /home/user/tools/node24).

## templates/website-promo

Song + HyperFrames walkthrough video of a real website (TalkEmber Studio promo, Oct 2026): build.py, alignment (dp_align.py), multi-part song generation. See its README.

## Owner Drive music index (`music/owner-drive/`)

47 tracks (35 YouTube Audio Library = YouTube only, 10 Mixkit = social/client OK, 2 own ElevenLabs intro stings) indexed with BPM/LUFS/key; files stay on the owner's Drive (fetch with gdown). See its README.

## music (added)

`music/talkember-studio-promo-song.mp3`: 6 min upbeat Hindi pop promo song about TalkEmber Studio (ACE-Step, 3 parts joined at 96.0 s and 212.5 s); line timings in `templates/website-promo/talkember-timing.json`.

## music catalogue

`music/catalogue.json` + `catalogue.md`: every usable track measured and tagged (music_catalogue.py, 2026-10-27). Pick with `tools/find_music.py`, fit with `tools/music_fit.py`; workflow = skill music-for-video; research library/research/music-for-video.md.

## music/cc0

131 no-credit tracks (counted 2026-10-24; index.json has 131 entries): 29 CC0 from OpenGameArt (background, cinematic,
piano, desi/eastern), 7 desi from the SoundSafari mirror (5 Freesound CC0 + 2 FreePD), 95 CC0/PD from FMA. List,
moods, sources and the licence audit: `music/cc0/README.md`.

## Clients
- `library/clients/moradosolution/`: brief.md (verified facts, voice recipe, deliveries) + **site-data.md** (full crawl of
  moradosolution.in on 2026-10-24: every plan/price, WELCOME30 offer, contacts, policies, contradictions) + site/pages
  (rendered text of 37 pages), site/screens (full-page screenshots, webp), assets/ (logo, icons, game/service images
  from the site), site/tools/crawl.js + shots.js (re-crawl).
