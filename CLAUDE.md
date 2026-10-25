# Memory for this repo

This repo is Claude's long-term memory and reusable media library for the owner's video work.
Read this first in every session.

## Rules from the owner

- SKILL-BASED ONLY (owner, Oct 24 2026): whenever the owner asks to MAKE or EDIT a video, never build or edit from
  guesswork. Use the repo first, in this order, before writing anything new:
  1. Client brief if one exists (library/clients/<name>/), then the matching template (library/templates/*).
  2. `.claude/skills/video-edit-playbook` + library/research/editing/decision-guide.md (find the video type, follow
     "Steps here"); look up every technique with `python3 library/tools/find_skill.py "<words>"` (prefer --tested).
  3. Repo tools and assets: listen.py / watch.py on every input before deciding cuts; library/music (CC0), sfx, stock,
     luts, fonts, blocks; vs_tts.py (free voice), watermark.py, screen_recorder.js, etc. (library/README.md lists them).
  4. Repo skills for the job (desi-reels, urdu-captions, client-brand-kit, stock-sfx-luts, voice-or-song,
     clean-video-voice, listen-and-watch, hyperframes).
  If the repo has nothing for a step, say so to the owner, use a verified source (with reference), and save what worked
  back to the repo. In the delivery message, name the template/skills/tools used.
- Store on GitHub ONLY: skills, learnings and things worth remembering (this file), and reusable
  assets/tools in `library/` (music, sound effects, fonts, overlay blocks, models, scripts).
- NEVER commit videos, photos, voice recordings, or personal data (family names, captions written about
  family members, faces). Work on personal media only in the session scratchpad and hand the result
  over with SendUserFile. `.gitignore` blocks common video/photo formats as a safety net.
- Whenever something is downloaded or made that a future edit could reuse (a track, an effect, a font,
  a block, a model), add it to `library/` and list it in `library/README.md` so it is never fetched or
  rebuilt twice.
- AUDIT (Oct 24 2026): claims in this file, library/README.md, library/music/*, library/research/*.md (not editing/,
  urdu-captions, client-intake) and the voice skills were re-checked; every change and its evidence is listed in
  library/research/audit-2026-10-24-part1.md. Timings marked "(Oct 2026)" are past measurements on this box, not re-run.
- VERIFIED ONLY (owner, Oct 24 2026): never add anything from guesswork, not a single letter. Research notes,
  knowledge files and sub-session output may contain ONLY verified facts or results measured here, each with its
  reference (source URL + date checked, or "measured here on <date>" + command). Unverifiable -> leave out or mark
  "unverified". Never invent Urdu/Pashto/Hindi words or translations. Applies to EVERY session and sub-session:
  first LOOK at the real source (or measure it), UNDERSTAND it, then WRITE only that, reference beside every item.
- SAVE ALL USEFUL DATA (owner, Oct 2026): every fact, finding or result gathered through tools or research
  (web reads, searches, star counts, specs, measurements, what worked/failed) goes into `library/research/`
  (one topic per .md, with source and date) or this file, and is pushed, so nothing is fetched twice.
  Downloaded reusable media goes to `library/` as before. Still NEVER personal data, family media or videos.
- Every tool installed for the owner must be added to `library/tools/setup-all.sh` so it is present in
  every session (the SessionStart hook runs it).
- Do NOT use ElevenLabs (voice, music, transcription, anything) unless the owner explicitly asks for it
  in that request. OWNER (Oct 24 2026, Skillora v3 session): "ab agay se elaven labs use nhi kroge": from now on the
  default voice is the free VoxCPM2 recipe (library/clients/moradosolution/brief.md "Voice"). Default to free/local tools (library/tools, Magenta, FluidSynth, numpy) instead.
- Reply in Roman Urdu (the owner writes Roman Urdu/Hindi). Keep answers short when they ask for short.
- DEFAULT HOST: when a video needs a host/presenter/character (or the owner says "character use karo"),
  use the owner's own skin `library/characters/host-skin.png` built with `library/tools/blocky_character.py`
  unless they name another character.
- The owner runs FireCraft SMP (www.firecraft.fun), a Minecraft lifesteal server. The `video/` folder
  is its Season 2 launch video and a template for similar promos.

## Environment facts (cloud container)

- Everything runs in an ephemeral cloud container, not the owner's PC.
- NETWORK: since Oct 24 2026 the owner set Network access to FULL (any site works, e.g. visit.talkember.site,
  www.firecraft.fun -> use web_capture.py for them, not Firecrawl; both answered 200 to curl on 2026-10-24; a
  browser-version mismatch that broke web_capture.py in one container is fixed, see Agent tools below). The old allowlist is saved in
  library/research/network-allowlist.md: give it to the owner when asked. Previously the network was allowlisted (Oct 2026): npm, pypi, archive.ubuntu.com (apt),
  raw.githubusercontent.com, `git clone` of public repos, storage.googleapis.com, fonts.googleapis.com,
  huggingface.co + its CDNs (us.aws.cdn.hf.co, *.xethub.hf.co), openaipublic.azureedge.net (Whisper),
  YouTube (youtube.com, *.googlevideo.com, i.ytimg.com), pixabay, freesound, api.openverse.org,
  wikimedia commons/upload, archive.org, freemusicarchive.org, incompetech.com.
  Blocked under that old allowlist: modelscope.cn, cdn.jsdelivr.net, download.pytorch.org, firecraft.fun, github.com web
  pages. With FULL access (re-checked 2026-10-24): cdn.jsdelivr.net, download.pytorch.org, huggingface.co, us.aws.cdn.hf.co
  answer 200; github.com pages + API stay 403 for repos outside the session (proxy), but `git clone` and
  raw.githubusercontent.com of public repos work; freesound.org, cdn.freesound.org and pixabay.com answer 403.
  YouTube downloads: `yt-dlp` (in /home/user/tools/venv). Only download CC/public-domain/royalty-free
  media, check the licence, and credit it; never copyrighted songs.
- A blocked website can still be read and seen through the Firecrawl MCP: `firecrawl_scrape` with
  `formats: ["screenshot"]` (fullPage for the whole page) returns a storage.googleapis.com PNG you can
  curl and crop. Image URLs themselves can't be screenshotted.
- OWNER RULE (Oct 24 2026): use FREE OPEN-SOURCE music MADE BY OTHERS (CC0 / public domain) for videos. Our own
  ACE-Step tracks (library/music/own) are good but the owner does NOT want them used; make music ourselves only if asked.
- OWNER RULE (Oct 2026): background music / songs must need NO credit: CC0, public domain or made by us. CC BY (YouTube
  CC filter, incompetech, most FMA/Jamendo) is not acceptable. Sources + findings: library/research/free-music-sources.md;
  own tracks: library/tools/music_pack.py (ACE-Step, one model load) -> library/music/own/.
- Never download copyrighted songs (YouTube rips etc.). Make music with `library/tools` or ask the
  owner to upload an MP3 they have.
- AUTO-INSTALL (owner asked that tools be there every session): the SessionStart hook fetches HyperFrames'
  Chrome, then runs `library/tools/setup-all.sh all` in the background: light part (ffmpeg,
  PIL/numpy/mido/pyworld, Agent-Reach, graft, REA, specialist-D tools, Crawl4AI; flag /home/user/tools/.light-ready;
  "~1 min" was an Oct 2026 estimate, not re-timed), then heavy part (music, ACE-Step/Whisper + weights,
  audio-separator, VoiceStudio, yt-dlp link; ~15 min fresh, Oct 2026; flag .heavy-ready). Log /home/user/tools/setup.log.
  Before using a tool early in a session, check its flag. Installed programs and the ~10 GB weights
  can't live in the repo (GitHub 100 MB file limit). Any new tool: add it to setup-all.sh, not only to chat.
- Song-with-vocals (ACE-Step 1.5, 13,969 stars, MIT) and transcription (OpenAI Whisper, 111,152 stars, MIT; Exa
  snapshot 2026-10-24) install with `library/tools/setup-ai-song.sh` into /home/user/tools/venv (Py 3.12, CPU;
  ~7.6 GB, ~10 min in Oct 2026).
  Their WEIGHTS download from huggingface.co, whose big files are served from us.aws.cdn.hf.co
  (non-Xet path, forced in ai_song.py with HF_HUB_DISABLE_XET=1) or cas-server/transfer.xethub.hf.co (Xet),
  and Whisper's from openaipublic.azureedge.net (small.pt = 483,617,219 bytes = 461 MiB, curl -I 2026-10-24; it took
  ~20 s in Oct 2026). Under the old allowlist these hosts failed with 403 until the owner allowed them; with FULL access
  they answer 200 (2026-10-24). No GPU here, so ACE-Step runs on CPU: load the DiT with quantization=int8_weight_only (fp32 OOMs
  at VAE decode), raise ACESTEP_GENERATION_TIMEOUT (default 600 s: acestep source, checked 2026-10-24). Turbo 60 s song ~5 min;
  base 32 steps ~16 min (Oct 2026). The base model's `lego` task (add vocals over an instrumental) did NOT add vocals on
  CPU (output = 0.97 copy of the input): make vocal songs with turbo text2music + lyrics instead.

- Long AI songs (Oct 2026, TalkEmber promo): a 47-line, 200 s ACE-Step song SKIPPED half the lyrics (sang ~25 lines).
  Keep each generation to ~16-19 lines (~130-150 s) and join parts at an instrumental gap with a crossfade. Several
  parts in one Python process share one model load (first load + INT8 ~11 min, later ~1 min).
- Promo jingle test (MoradoSolution, 8 dense Hindi ad lines, turbo, measured here 2026-10-24): 36 s @120 BPM sang only
  ~4 lines (whole-mix Whisper similarity 38%); 64 s @110 BPM sang lines 3-8 but dropped the two hook lines 1-2 (61%).
  ai_song.py's initialize_service re-downloads the unused 3.5 GB LM (acestep-5Hz-lm-1.7B) every run: delete it after.
  Whisper on the UVR-separated vocals returned nothing for the first 30 s window (a lone hallucinated word at 30 s)
  while the full-mix transcript had those lines: check both. library/tools/align_lyrics.py maps lines to times.
- Whisper on a long song misses whole sung stretches: separate the vocals first (UVR-MDX-NET Voc FT, ~2 min for
  200 s), transcribe with condition_on_previous_text=False, then align lyric lines with a global in-order DP
  (video/dp_align.py pattern), never greedy first-match (one weak match pushes every later line out of place).
- NEVER run two heavy torch jobs at once on this 4-core box (nproc = 4, RAM 15 GB: checked 2026-10-24; the slowdown below is from Oct 2026) (ACE-Step + Whisper together: load 8, both 3-4x slower;
  a part that takes 9 min alone took 35+). Queue them.
- Background Bash jobs die at their timeout (default 30 min = 1800000 ms, max 7200000 ms per the Bash tool's own
  description, 2026-10-24): give long jobs a timeout up to 7200000 ms.

- Realistic 3D model of a person (Oct 2026): the owner REJECTED the CPU results ("very bad"): TripoSR (full body from a
  video frame / bust from a selfie; face blurry) and 3DDFA_V2 (face mask with photo texture, nothing behind). Don't offer
  CPU image-to-3D of people again. For a realistic, identity-exact model: a GPU phone scan app (KIRI Engine, Polycam,
  Luma) whose file the owner sends, or a Minecraft-style look-alike skin for the blocky host. (TripoSR needed: rembg
  u2net_human_seg instead of the default BRIA model, which OOM-killed at 14 GB; PyMCubes instead of torchmcubes.)
- Disk allowance is small (Oct 2026): `uv cache clean` freed 8.7 GB; the unused ACE-Step base model (4.5 GB) was deleted.

## HyperFrames learnings

(Observed in renders here, Oct 2026. Re-measured 2026-10-24: the riser/error timings and that whoosh = whoosh-short and
click = click-soft are byte-identical (md5); GSAP core 3.14.2 has no "rough" ease. The rest is not re-tested.)

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

- RULE (owner, Oct 2026): "voice over / narration / awaaz" = spoken voice with ZERO music and every line present ->
  `library/tools/ai_voice.py`. "song / gaana / music" = with music -> `ai_song.py`. Skill: `.claude/skills/voice-or-song`.
  The owner prefers this ACE-Step voice over Kokoro (Kokoro sounded less natural and smooth to them).
- RULE (owner, Oct 2026): if a video the owner gives already has a voice, USE THAT VOICE: remove noise, music and
  every background sound so only the person's voice remains -> `library/tools/clean_voice.py` (skill
  `.claude/skills/clean-video-voice`). Don't generate a new voice for it.
- clean_voice.py test (Oct 2026, 26 s voice + instrumental music + pink noise + 120 Hz hum): BS-RoFormer took the
  pauses from -28 dB to -106 dB and SNR 5.7 -> 21.9 dB in ~8 min; --fast (MDX-Net Voc FT) gave -69 dB / 18 dB in
  43 s. The denoise pass (~3 min) then took the pauses to digital silence (-180 dB). Whisper words unchanged.
  A song WITH a singer as background is kept as "voice" by any vocal model: only instrumental sound is removable.
  Measuring: a causal 70 Hz high-pass shifts phase, so waveform SNR vs a reference collapses (2 dB) though nothing
  audible changed; compare against a reference passed through the same filter, or use pause levels.
- ai_voice.py lessons (Oct 2026 test, 6 lines): a lone short line per take came out garbled (40-53% Whisper match);
  the whole passage per take works (round 1: 65-100% per line, round 2: all >= 84%, overall 88%), so lines are
  generated in groups of 6 and each line keeps its clearest stretch from any take. Cut each line between its
  neighbouring words (a +0.3 s tail leaked the next line's first word). Music after separation: gaps at -86 dB.
  Time: ~6.5 min per round of 3 x 25 s takes + ~1 min music removal per line.

- DEFAULT VOICE (owner, Oct 24 2026; pitch set to a 172 Hz median like the Viraj VO via --target-f0): `vs_tts.py` with no --voice/--ref/--instruct uses voices.json "default": the free
  AI-designed young energetic Hindi ad narrator from the MoradoSolution reel (VoxCPM2, not a real person; the owner
  first asked for a Viraj clone, declined: real voice actor). Real Viraj only via ElevenLabs when the owner asks.
- SAVED VOICES (owner, Oct 24 2026): "senpaispider" = the owner's client Senpai Spider. When the owner says "senpai ki
  voice me banao" (or names a saved voice), use `vs_tts.py --voice senpaispider` (VoxCPM2 clone, recipe in
  library/voices/voices.json; reference rebuilt from the Drive link, never committed). Script in Devanagari,
  Whisper-check every line (first test: lines 2-4 clear, line 1 partly, "सब्सक्राइब" garbled -> regenerate bad lines).
- AI songs with vocals that the owner LOVED ("perfect song"): `library/tools/ai_song.py` with seed 7,
  80 BPM, 60 s, caption "romantic hindi pop ballad, soft piano, acoustic guitar, strings, gentle tabla,
  rainy evening mood, warm male vocals, clear hindi lyrics". Reuse this recipe/style for new songs; the
  result is in `library/music/baarish-ki-pehli-shaam-ai-song.mp3`. Run it in the background with a
  per-minute status monitor (the owner likes minute-by-minute updates on long jobs).

- VOICESTUDIO (owner, Oct 24 2026: "replacing ElevenLabs"): debpalash/VoiceStudio runs locally (setup-all heavy, backend
  `library/tools/voicestudio.sh start`, script tool `vs_tts.py`, skill voice-or-song). OmniVoice engine: Urdu 100%/97%,
  Hindi 92%, Pashto 81% Whisper match, voice design + cloning; Oct 24 test: 4.4-9.5 s clips took 22-36 s incl. model load
  (~4-5x the audio length; the old "~3-4x" did not match those numbers). Its weights are NON-COMMERCIAL:
  client/paid work -> `--model voxcpm2` (Apache-2.0, Hindi, 4.96 GB: HF API 2026-10-24; download when needed) or ai_voice.py. Details:
  library/research/voicestudio.md.
- CPU-ONLY TORCH: the main venv now uses torch 2.10.0+cpu (wheel exists on download.pytorch.org/whl/cpu, checked
  2026-10-24; the pypi CUDA build wasted ~5 GB of nvidia libs on disk, Oct 2026).
- ElevenLabs notes below are from Oct 2026 and NOT re-checked in the audit (ElevenLabs is owner-gated).
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

- Spoken voiceover from ACE-Step (test Oct 2026): caption "spoken word, male narrator speaking hindi, warm
  friendly youtube voiceover, a cappella, dry clean vocal, no music, no instruments, no singing, clear hindi
  speech", lyrics under [Spoken Word], 20 s, 90 BPM, ducking off (--duck-*-db 0 --presence-db 0), ~2.5 min/take.
  Seed 21: Whisper similarity 46% (most lines, one skipped), seed 7: 24% (skipped lines). The loved song scored
  23%, so Whisper scores are low for any AI vocal. ~25% of voiced frames are held notes (half-sung delivery),
  quiet bed at -30 dB. Usable as a sing-song narrator, not a flat newsreader; it can drop lines: check report.json.

## CSS 3D voxel films (learned on the Blocky Monsoon video)

(Observed in Chrome renders here, Oct 2026; not re-tested.)

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

## Client phone-video edits (Oct 2026, "Boss mode" reel; template library/templates/phone-clip-reel)
- WhatsApp clips can report r_frame_rate 28.4 while really being ~12 fps (134 frames in 11 s). Check frame pts
  (`ffprobe -show_entries frame=pts_time`) and motion-interpolate EVERY clip to 30 fps (minterpolate ...:scd=none),
  not only the slow-mo ones, or 1x shots look choppy.
- A clip with no usable speech (Whisper finds nothing) becomes a music reel: title at 0 s, one shot per bar, varied
  transitions, Roman Urdu attitude lines that claim nothing specific about the client's business.
- Mix levels that worked: music 1.0, impact-bass 0.35-0.4, whoosh 0.6-0.8, ring 0.5. At 0.8-0.9 the impacts were
  8 dB over the music for 2 s. Measure the render per 0.5 s (numpy RMS) and `ebur128` (target about -16 LUFS).
- HyperFrames lint: don't tween letterSpacing (use scaleX); GSAP "rough" ease is not in core GSAP (use a yoyo shake).
  An <img> over 2 MB isn't inlined: use JPG. A scene's <img>/<video> data-duration must equal the scene length.
- Pausing a harness background job with kill -STOP makes the harness mark it failed and kill it. Don't pause; queue
  heavy jobs. music_pack.py skips finished tracks, so a restart only redoes the unfinished ones.
- BACKGROUND BLUR the owner approved (Oct 2026): `library/tools/bg_blur.py`. First tries looked "awkward": plain
  Gaussian, a halo around the person (the blur smeared his own dark pixels outward), hard edges, blue boxes still
  visible as blue blobs. What fixed it: inpaint the subject out of the background BEFORE blurring, disc (bokeh) blur in
  linear light, desaturate blue/cyan background objects into the wall hue, background -14% exposure, soft temporally
  smoothed mask. u2net_human_seg misses dark shirt between arm and body: add dark pixels inside the silhouette's
  convex hull (open 23 px to drop thin shelf lines). Keep the desk sharp via a RANSAC line on the cyan mats found
  bottom-up (a top-down search grabbed blue boxes). BiRefNet-portrait is cleaner but 39 s/frame and OOM-killed: not
  usable. Always show the owner a before/after frame and get approval before rendering.
- Pashto touch for Pashto-speaking clients: "Manana" (مننه) = thank you (omniglot.com/language/phrases/pashto.php via
  WebSearch, 2026-10-24). Captions stay Roman Urdu.

## Tutorials / screen videos
- OWNER RULE (Oct 24 2026): in every tutorial or screen video, EVERY click is shown with a visible mouse cursor that moves
  to the target and plays a click animation (ripple/press) at the moment of the click (plus a soft click sound).
  Show only what really happens on the real site/app (recorded or screenshotted here), nothing invented.
- FireCraft whitelist tutorial (Oct 24 2026, template library/templates/screen-tutorial, notes
  library/research/firecraft-whitelist-flow.md): record real sites with `library/tools/screen_recorder.js` (cursor + ripple
  drawn in the page, `fakeClick` for buttons that must NOT be sent: never create accounts or submit live forms). CDP screencast
  frames are DIP-sized, so deviceScaleFactor does not sharpen them: use CSS zoom (`zoom: 1.25`) for big, sharp UI text; the
  cursor overlay divides by the zoom. Block ad hosts while recording (firecraft.fun loads AdSense + vignette ads). On firecraft.fun
  at window heights < ~900 CSS px the login modal's x sits under the fixed header (a click opened Leaderboard): reload instead.
  Voice is the clock: build.py speed-fits each recorded span (0.85-3x) to its VO line. Render 62 s in 2m01s (--workers 3).
- Client screen-recording + free VO (SkilloraClouds reseller tutorial, measured here 2026-10-24): Google Drive file
  downloads with `curl -L "https://drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t"` (169 MB,
  200). VoxCPM2 cloned lines took ~3-4 min each on this box (23 lines 13:47-15:14); seed 7 designed ref ran on
  ("...चाहते हैं? आई गेई"): trimmed at the silence (2.85 s). Seed 21 fixed 3 of 3 weak lines (doubled word, garbled
  start/restart/stop, "MOTD Maker"). Whisper scores 11-86% were mostly spelling; read the HYP text, not the %.
- ffmpeg OOM (exit 137) on 9 `trim` branches of one 1440x810 60 fps input in one filter graph: render each segment
  to its own file (-ss/-t, setpts for 2x), concat -c copy, then one pass for `ass=` captions + audio (worked, 147 s).
- `pkill -f "<words>"` also kills the Bash shell whose own command line contains those words (exit 144): use the PID.
- Owner chose for this tutorial: no blur of the client's demo emails; dheema CC0 music under the VO; Roman captions.

## Website/hosting promo reels (SkilloraClouds, Oct 24 2026; template library/templates/hosting-promo-reel)
- Owner flow that worked: capture the site (web_capture.py: homepage + pricing pages), quote ONLY what the pages say
  (price "from ₹20/mo" was on /games, coupon from the top banner), brand colours from the site CSS (most frequent hex),
  logo/screens/flags downloaded from the site, owner-chosen VO, PREVIEW (contact sheet + VO/music mix) before render.
- ElevenLabs (owner asked by name: "Viraj" Hindi): creative_list_voices showed 24 distinct voice names starting "Viraj"; "Viraj – Viral Ad & Content Voice"
  (pHG3exaXQt8bmTWbaVOs) fits reels. 2 takes of a 29 s script = 2 x 427 credits (2026-10-24).
- IMPORTANT: creative_transcribe_audio on a flow's own TTS take returned the PROMPT text verbatim (incl. the "[excited]"
  tag) with 0 credits = the TTS alignment, NOT a real transcription. Use it for word timings only; verify words
  independently (Whisper small per line on cuts from those timings worked: all 8 lines heard; whole-file Whisper failed).
- OWNER RULE (Oct 24 2026, said in the MoradoSolution session): "Final video ab se diya kro preview nhi": send the final
  clean video + WhatsApp copy directly, no watermarked preview. Applies to MoradoSolution (deal done); for a NEW unpaid
  client, ask the owner whether the watermark rule below still applies.
- (Earlier rule, now only for new unpaid clients if the owner says so) client videos shown BEFORE payment get `library/tools/watermark.py` ("Made by MrCopper804"
  tiled + PREVIEW corner tag + copyright metadata); the clean, open-licence file goes out only after payment.
- MISSED FACT (2026-10-24): the first reel listed India/Singapore/Dubai but the homepage also lists "Frankfurt(Germany)" /
  "Europe (Germany)"; the owner caught it. Before writing a script, grep the captures for EVERY item of a list
  (locations, games, plans), not just the first sentence that names some.
- MISSED OFFER (2026-10-24, MoradoSolution): curl text of moradosolution.in/sales showed only "Live promo codes are
  listed here as soon as they are published" (codes load by JavaScript); a browser crawl later the same day found
  WELCOME30 = 30% OFF live. Read offer/price pages in a real browser (web_capture.py / Playwright), never curl text only.
- Patching one VO line later: regenerate only that line with the same ElevenLabs voice (5.4 s line = 78 credits per take,
  2 takes, 2026-10-24), Whisper-check it, splice at the silences around the old line (silencedetect -40 dB), loudnorm the
  whole VO again, shift later scenes/SFX by the length difference. Its loudness matched the old line (-19.0 vs -19.3 LUFS).
  Never clone a real voice actor's voice with a free tool to avoid this (owner chose the ElevenLabs line instead).
- QA after render: watch.py (fps, black/frozen) + listen.py (LUFS, clipping, voice span). Music under VO at volume 0.16
  (-13 LUFS track) and VO loudnormed to -16 gave a -16.0 LUFS mix, no clipping.

## Sub-sessions (Oct 24 2026)
- ARCHIVED Oct 24 2026 (owner asked; all work merged): Self-study, Specialists A-D, Audit 1 + Audit 2 sessions.
  Their branches stay on GitHub. Active: FireCraft tutorial, SkilloraClouds v3, MoradoSolution client session.
- Self-study DONE + merged (Oct 24 2026): library/research/editing/ (decision-guide.md: 29 video types -> how to edit;
  skills/01-06: 560 cited skills; from-scratch.md) + skill .claude/skills/video-edit-playbook. READ decision-guide.md
  before editing any new video.
- Self-study round 2 DONE + merged (Oct 24 2026): skills2/ = 4,832 new cited skills (#561-5556, 21 categories; 2,705
  marked "(tested here 2026-10-24)"; target 5,000 not reached: no padding). Search ALL skills with
  `python3 library/tools/find_skill.py "<words>" [--tested]`. Key: Urdu/Hindi burn-in needs ffmpeg `ass=` (subtitles=/drawtext
  break Nastaliq + conjuncts); arnndn models in library/models/arnndn. Spot-checked on merge (2026-10-24): arnndn std.rnnn on
  white noise -30.8 -> -43.1 dB mean; `ass=` + fontsdir=library/fonts rendered shaped Nastaliq. Missing-tools list: skills2/README.md.
- Specialists: A perception tools + CPU speed (session_01BdHJpuB2BTCGDxFdR7KV44, specialist-a-perception-cpu);
  A DONE + merged Oct 24 2026: listen.py / watch.py / fast_matte.py (perc-venv), skill listen-and-watch: run them before
  editing instead of guessing (verified here: 105.0 BPM on a 105 BPM track; 12.4 real fps on the 12 fps WhatsApp clip).
  Specialist A measured (cpu-speed.md, 2026-10-24): HyperFrames `render --workers 3` took 25 s vs 40-50 s with auto on a
  10 s 1080p project; MediaPipe needs apt libgles2 + libegl1; bg_blur.py with RVM + cheaper fill: 2.08 -> 0.66 s/frame
  (patch in cpu-speed.md; RVM drops a second person at the frame edge; show the owner before/after before switching).
  B DONE + merged Oct 24 2026: library/music/desi-vocal (29 PD Urdu/Hindi vocal songs, 1905-1919 78 rpm; no Pashto PD song
  found), research/pk-reels-trends.md + pk-reel-recipes.md, skill desi-reels. Rejected: Gallica/BnF (credit + fee),
  FMA Excavated Shellac (CC BY).
  C stock b-roll + SFX + LUTs (session_015uWvzd8vXhZJRw2ch8F5Ym): DONE + squash-merged Oct 24 2026: library/stock (67 clips),
  library/sfx (164), library/luts (32 own), find_stock.py, skill stock-sfx-luts. Mixkit = links only, fetch one per need;
  2 NASA clips licence_doubt (not for client ads). Every entry has licence_proof.
  D Urdu/Pashto captions + client brand kit (session_01NZND2H5jzoXgcGVrFFtHH2): DONE + merged Oct 24 2026 (fonts,
  urdu_captions.py, blocks/urdu-captions.html, templates/brand-kit, skills urdu-captions + client-brand-kit).
  They add new files only; merge each branch into the main work branch when done, then update library/README.md,
  setup-all.sh (their setup-specialist-*.sh) and this file.

- FireCraft whitelist tutorial (session_01TPMNGNY1pArQWPm5nmzAfF): DONE + merged Oct 24 2026 (screen_recorder.js,
  wcheck_lines.py, templates/screen-tutorial, research/firecraft-whitelist-flow.md). 62.2 s 1080p, 19 clicks with cursor,
  nothing submitted; preview sent to the owner by that session, final waits for approval there.
- SkilloraClouds reel v3 (session_01Se2FPfh8Ga51Fqqm2KT6cL, branch skillora-reel-v3): v3 draft 44.09 s sent (Viraj lines,
  438 credits, generated before the switch; EPYC 9 at the client's request, not on the site). Site 2026-10-24: game
  servers India/Singapore/Dubai; Germany = VPS/RDP/Dedicated only; Malaysia/Qatar/US list no services. Next videos: free voice.

- Client MoradoSolution home session: session_01CQ1ajF7SNBueqvBiNGWsLX (branch client-moradosolution, Oct 24 2026).
  Brief: library/clients/moradosolution/brief.md. Deal done; clean FINAL reel delivered Oct 24 2026.
- Client PakWebHoster (pakwebhoster.com) home session: session_01Kmr9yVm1eY9vB1qqC9R3R8 (branch client-pakwebhoster,
  Oct 25 2026). Full crawl + brief: library/clients/pakwebhoster/ (site-data.md lists contradictions to ask about).
- Client-site crawl lessons (PakWebHoster, measured here 2026-10-25): a WHMCS client area's relative links nest forever
  (index.php/store/index.php/...): skip URLs with "index.php" twice. Hero images can be stock photos of people, even
  inside .svg files: screenshots for the repo must hide every big image (pakwebhoster/site/tools/shots.js) and be
  checked visually; the Read tool can show a cached old image for a re-written path, so view a new filename.
- PakWebHoster reels (2026-10-25, measured here): `bash voicestudio.sh start 2>&1 | tail -3; python3 vs_tts.py ...` in one
  Bash call HANGS: the backend keeps the pipe open, tail never exits, vs_tts never starts (lost 9 min). Start the backend
  without a pipe. vs_tts default voice: 7 lines took ~10 min; "स्टार्टर लाइट प्लान" at a line start was garbled in 3 takes
  (seeds 7/21, Devanagari and Latin): keep hard brand/plan names on screen, not in the VO. Takes from different runs differ
  in pitch (153-207 Hz median): join them with library/tools/vo_join.py (pitch-matched to 172 Hz). Owner chose for this
  NEW client: watermarked previews first. New templates: kinetic-type-reel, typewriter-reel; GSAP plugins in library/vendor.

## Agent tools (library/tools/setup-agent-tools.sh)
- OWNER RULE (Oct 2026): use Agent-Reach INSTEAD of Firecrawl for searching/reading the web (Firecrawl costs
  the owner credits). Fallback when an Agent-Reach channel fails: WebSearch. Use Firecrawl only if the owner asks.
- Screenshots / page capture: `library/tools/web_capture.py` (Crawl4AI, free, local Chromium) -> markdown + full-page
  PNG. 2026-10-24: one container had chromium-1243 while crawl-venv's playwright 1.56.0 wants chromium-1194, and it
  failed ("playwright install"). FIXED the same day: if chromium-1194 is missing, web_capture.py starts the image's own
  Chromium with remote debugging and attaches over CDP (tested here 2026-10-24 on https://example.com both ways:
  953 chars + PNG). Fallback if it still fails: `agent-reach read` or curl of the HTML. It only reaches domains allowed in the environment's network settings: for a blocked site ask the owner to
  add the domain (e.g. visit.talkember.site, www.firecraft.fun) instead of spending Firecrawl credits.
- Agent-Reach 1.6 (1.6.0 per `agent-reach doctor`, 2026-10-24; `agent-reach`, skill auto-installed): `agent-reach read <url>`, `agent-reach web search "<q>"`,
  `agent-reach youtube search "<q>"` (works, via yt-dlp), JSON output.
  Owner allowed r.jina.ai, s.jina.ai, mcp.exa.ai, api.exa.ai, www/old.reddit.com (Oct 2026): web read (jina) and
  web search (exa) WORK (both worked 2026-10-24; after many searches that day Exa answered RATE_LIMITED "wait 3512 s"). For GitHub tool discovery use `agent-reach web search "<name> github"` (results show stars);
  the github channel itself fails (session gh API is repo-scoped). Reddit search can hit Exa 429 (rate limit) and
  its opencli fallback needs a GitHub release download (blocked): wait and retry once, else WebSearch.
- ECC (everything-claude-code) lives in .claude/ (agents, commands, quality skills; no hooks). REA (reverse engineering,
  MCP `rea` in .mcp.json + skill). See library/research/tools-landscape.md.
- graft 0.25 (`graft build`, `graft ask "<q>"`): code context graph; telemetry disabled. Don't commit its graft/ folder unless asked.
