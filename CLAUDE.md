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
- The owner runs FireCraft SMP (www.firecraft.fun), a Minecraft lifesteal server. The `video/` folder
  is its Season 2 launch video and a template for similar promos.

## Environment facts (cloud container)

- Everything runs in an ephemeral cloud container, not the owner's PC.
- Network is allowlisted. Blocked: huggingface.co (no MusicGen/HF models), cdn.jsdelivr.net,
  download.pytorch.org, firecraft.fun, youtube, openverse, github.com web pages. Allowed: npm, pypi,
  archive.ubuntu.com (apt works), raw.githubusercontent.com, `git clone` of public repos,
  storage.googleapis.com (Magenta checkpoints, Firecrawl screenshots), fonts.googleapis.com.
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
  settings, both fail with 403. No GPU here, so ACE-Step runs on CPU (slow; use the 2B turbo, LM off).

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
