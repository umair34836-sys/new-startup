# Memory for this repo

This repo is Claude's long-term memory and reusable media library for the owner's video work.
Read this first in every session.

## Rules from the owner

- Store on GitHub ONLY: skills, learnings and things worth remembering (this file), and reusable
  assets/tools in `library/` (music, sound effects, fonts, overlay blocks, models, scripts).
- NEVER commit videos, photos, voice recordings, or personal data (family names, captions written about
  family members, faces). Work on personal media only in the session scratchpad and hand the result
  over with SendUserFile. `.gitignore` blocks common video/photo formats as a safety net.
- Whenever something is downloaded or made that a future edit could reuse (a track, an effect, a font,
  a block, a model), add it to `library/` and list it in `library/README.md` so it is never fetched or
  rebuilt twice.
- Do NOT use ElevenLabs (voice, music, transcription, anything) unless the owner explicitly asks for it
  in that request. Default to free/local tools (library/tools, Magenta, FluidSynth, numpy) instead.
- Reply in Roman Urdu (the owner writes Roman Urdu/Hindi). Keep answers short when they ask for short.
- DEFAULT HOST: when a video needs a host/presenter/character (or the owner says "character use karo"),
  use the owner's own skin `library/characters/host-skin.png` built with `library/tools/blocky_character.py`
  unless they name another character.
- The owner runs FireCraft SMP (www.firecraft.fun), a Minecraft lifesteal server. The `video/` folder
  is its Season 2 launch video and a template for similar promos.

## Environment facts (cloud container)

- Everything runs in an ephemeral cloud container, not the owner's PC.
- Network is allowlisted. The owner has allowed (Oct 2026): npm, pypi, archive.ubuntu.com (apt),
  raw.githubusercontent.com, `git clone` of public repos, storage.googleapis.com, fonts.googleapis.com,
  huggingface.co + its CDNs (us.aws.cdn.hf.co, *.xethub.hf.co), openaipublic.azureedge.net (Whisper),
  YouTube (youtube.com, *.googlevideo.com, i.ytimg.com), pixabay, freesound, api.openverse.org,
  wikimedia commons/upload, archive.org, freemusicarchive.org, incompetech.com.
  Still blocked: modelscope.cn, cdn.jsdelivr.net, download.pytorch.org, firecraft.fun, github.com web pages.
  YouTube downloads: `yt-dlp` (in /home/user/tools/venv). Only download CC/public-domain/royalty-free
  media, check the licence, and credit it; never copyrighted songs.
- A blocked website can still be read and seen through the Firecrawl MCP: `firecrawl_scrape` with
  `formats: ["screenshot"]` (fullPage for the whole page) returns a storage.googleapis.com PNG you can
  curl and crop. Image URLs themselves can't be screenshotted.
- Never download copyrighted songs (YouTube rips etc.). Make music with `library/tools` or ask the
  owner to upload an MP3 they have.
- HyperFrames renders need headless Chrome: the SessionStart hook runs `browser ensure`.
- Music tools need `library/tools/setup-music.sh` once per container.
- Song-with-vocals (ACE-Step 1.5, 13.9k stars) and transcription (OpenAI Whisper, 111k stars) install
  with `library/tools/setup-ai-song.sh` into /home/user/tools/venv (Py 3.12, CPU, ~7.6 GB, ~10 min).
  Their WEIGHTS download from huggingface.co, whose big files are served from us.aws.cdn.hf.co
  (non-Xet path, forced in ai_song.py with HF_HUB_DISABLE_XET=1) or cas-server/transfer.xethub.hf.co (Xet),
  and Whisper's from openaipublic.azureedge.net (works now: small model, 461 MB in ~20 s): until the owner allows those hosts in the environment's network
  settings, both fail with 403. No GPU here, so ACE-Step runs on CPU: load the DiT with quantization=int8_weight_only (fp32 OOMs
  at VAE decode), raise ACESTEP_GENERATION_TIMEOUT (default 600 s). Turbo 60 s song ~5 min; base 32
  steps ~16 min. The base model's `lego` task (add vocals over an instrumental) did NOT add vocals on
  CPU (output = 0.97 copy of the input): make vocal songs with turbo text2music + lyrics instead.

## HyperFrames learnings

- Load GSAP from `assets/vendor/gsap-3.14.2.min.js`, never the CDN (render fails with
  `sub_timeline_script_failure`). Registry blocks (`npx hyperframes add ...`) also point at the CDN: fix them.
- `media-treatment --apply` rewrites the scene markup (adds `data-hf-id`, reorders attributes): later
  string edits must match the new markup, so edit by regex or re-read the file.
- Every `<audio>` needs `data-duration` set to the clip's real length, and overlapping clips need
  different `data-track-index` lanes, or lint warns `duplicate_audio_track`.
- Bundled SFX quirks: `riser` (10 s file) actually crests at 3.47 s and is silent after 4.5 s; use
  `data-media-start` so 3.47 s lands on the hit. `error` starts 0.6 s into the file and is very quiet
  (needs `data-volume` ~2.5). `whoosh` == `whoosh-short`, `click` == `click-soft` (same files).
- `npx hyperframes audio <file>` measures hits/loudness/silence: use it to verify sound lands, since
  Claude can't listen.
- Check before render, then `snapshot --at ...` and look at the frames. Layout warnings for decorative
  overflow are fixed with `data-layout-allow-overflow`; stacked text effects with `data-layout-allow-occlusion`.
- The first frame is the thumbnail: put a title or key image on screen at 0 s.
- Light text on a bright wall fails contrast: use a deep colour (#6e0c20) with a light glow, or put
  captions over the darker lower part of the frame with a bottom gradient veil.

## Voice and songs with words

- AI songs with vocals that the owner LOVED ("perfect song"): `library/tools/ai_song.py` with seed 7,
  80 BPM, 60 s, caption "romantic hindi pop ballad, soft piano, acoustic guitar, strings, gentle tabla,
  rainy evening mood, warm male vocals, clear hindi lyrics". Reuse this recipe/style for new songs; the
  result is in `library/music/baarish-ki-pehli-shaam-ai-song.mp3`. Run it in the background with a
  per-minute status monitor (the owner likes minute-by-minute updates on long jobs).

- ElevenLabs connector (ONLY when the owner asks for it; TTS only, costs the owner's credits; ~230 credits for 2 takes of a 16 s script,
  ~90 per transcription). Good warm Urdu/Hindi romantic male voice: "Ashar – Romantic, Warm Boyfriend"
  (`nq3gz2RQGRBB1SbrgTqF`), model `eleven_v4`. Write the script in Devanagari (English words stay
  English); it pronounces Hindustani well.
- The `[singing]` tag does NOT really sing for this voice: pitch analysis (pyworld) showed only 4% held
  notes, i.e. soft expressive speech. Treat it as spoken izhar/shayari over music, and say so.
- Verify every take with ElevenLabs transcription (`creative_attach_reference_file` with the take's URL
  on the same flow, then `creative_transcribe_audio`): it checks the words and gives per-word timings
  to cut lines from. Result/asset URLs are on storage.googleapis.com, so curl can download them.
- Mix with `library/tools/voice_over_music.py`. ffmpeg 6.1 quirk: `adelay` after `concat`+`atempo`
  silently does nothing, so place lines in numpy (the tool does).
- A video `<audio data-fade-out>` must start after the last spoken word, or it swallows the final line.

## CSS 3D voxel films (learned on the Blocky Monsoon video)

- `mix-blend-mode` (and opacity < 1 / filter on a preserve-3d container) flattens the whole 3D world: camera pitch
  stops working and the ground vanishes. Use plain rgba/gradients on faces; put blends only in separate 2D overlay
  compositions above the world.
- Chrome drops a whole face once any part of it passes behind the camera: tile ground into 4x4-block quads.
- `tl.set(..., 0)` does not render on frame 0: also apply initial states with `gsap.set` before the timeline
  (build.py does this automatically). Hide things with `visibility`, not container opacity.
- Keep the camera out of buildings: a side tracking shot needs a gap between the lane and the houses.
- ~1,200 faces + 2 characters render fine; snapshot at the QA times before every render.
- Never `cd` somewhere and `rm -rf *`: make a fresh folder instead (the safety check blocks it anyway).

## Editing a phone video into a "professional" edit (recipe that worked)

1. Look first: ffprobe (rotation, fps), a contact sheet every ~0.4 s, find the best moments (smiles, actions).
2. Pick a BPM and cut on bars (72 BPM: every 3.333 s). Cut the source into clips with ffmpeg at the
   speed each beat needs: 1.5x for setup, slow-mo for emotion. Smooth slow-mo:
   `ffmpeg -ss S -t T -i in.mp4 -an -vf "minterpolate=fps=<30/rate>:mi_mode=mci:mc_mode=aobmc:vsbmc=1,setpts=PTS/<rate>,fps=30,trim=0:3.333" -r 30 -crf 15 clip.mp4`.
   Fast hand motion smears a little.
3. End on a freeze frame: make the last slow-mo clip end exactly on the chosen frame, export it as a
   PNG, and place it with the same framing so the freeze is seamless.
4. Grade: compare 2-3 candidates with `npx hyperframes grade-compare --for frame.png --grades grades.json`
   on a real frame, then apply the winner to every clip (see `library/README.md` for payloads).
5. Framing: wrap each video in a div and tween `scale`/`x`/`y` on the wrapper (transformOrigin on the face).
   Vary transitions: light leak, zoom-through (scale up + blur out, next shot settles from 2.0 to 1.7),
   soft flash, seamless freeze.
6. Captions: per-word blur-in, 0.12 s stagger, over a bottom gradient; one gold accent word per line.
7. Overlays: `floating_hearts.py`, light leak block, bokeh. Music from `library/music`.
8. Deliver full quality plus a WhatsApp copy: `ffmpeg -i in.mp4 -c:v libx264 -crf 23 -preset slow -c:a aac -b:a 160k -movflags +faststart out.mp4`.

## Agent tools (library/tools/setup-agent-tools.sh)
- Agent-Reach 1.6 (`agent-reach`, skill auto-installed): `agent-reach read <url>`, `agent-reach youtube ...`, JSON output.
  Its GitHub channel fails here (session gh API is repo-scoped); use WebSearch/Firecrawl for GitHub discovery.
- graft 0.25 (`graft build`, `graft ask "<q>"`): code context graph; telemetry disabled. Don't commit its graft/ folder unless asked.
