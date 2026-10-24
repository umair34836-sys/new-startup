---
name: video-edit-playbook
description: Decide fast how to edit any video the owner sends (phone clip, WhatsApp clip, talking head, event, product, screen recording, silent clip, photos, or no footage at all). Use whenever the owner asks to edit, "professional bana do", make a reel/short/promo, or build a video from scratch. Gives the triage checklist and tells you which knowledge-base file to read (library/research/editing/).
---

# Video edit playbook

Every rule below points to where it was learned or researched. The knowledge base lives in
`library/research/editing/` (index: `README.md` there). Personal media stays in the scratchpad; never commit it
[repo: CLAUDE.md "Rules from the owner"].

## 1. Look at the video first (triage, ~1 min)

1. Duration, resolution, rotation, codec: `ffprobe -v error -show_entries format=duration:stream=codec_type,width,height,r_frame_rate:stream_side_data=rotation -of json in.mp4`
   [repo: CLAUDE.md "Editing a phone video" step 1].
2. REAL fps: WhatsApp clips can report 28.4 fps while really being ~12 fps; count frame timestamps:
   `ffprobe -v error -select_streams v:0 -show_entries frame=pts_time -of csv=p=0 in.mp4 | wc -l` and divide by
   the duration. Low real fps -> motion-interpolate every clip to 30 fps (`minterpolate ...:scd=none`)
   [repo: CLAUDE.md "Client phone-video edits"].
3. Audio and speech: is there an audio stream, is it speech, music or noise? Run Whisper; if it finds no usable
   speech the clip becomes a music reel [repo: CLAUDE.md "Client phone-video edits"]. If there IS a voice, keep
   that voice and clean it with `library/tools/clean_voice.py` (skill clean-video-voice) instead of a new voice
   [repo: CLAUDE.md "Voice and songs with words"].
4. Contact sheet every ~0.4 s to find the best moments (smiles, actions) [repo: CLAUDE.md "Editing a phone video" step 1].
5. Where will it be posted (Reels/Shorts/TikTok 9:16, YouTube 16:9, WhatsApp)? Specs and export:
   `library/research/editing/skills/06-cleanup-platform-delivery.md`.

## 2. Pick the recipe

- Find the video type in `library/research/editing/decision-guide.md` (input-triage table at the top, then one
  section per type: goal, length, beat map, cuts, transitions, grade, captions, music, mistakes, steps here).
- No footage at all -> `library/research/editing/from-scratch.md`.
- Need a specific technique (a transition, a grade, a mix level, a caption style, a fix)? Search the numbered
  catalog (5,392 skills, #1-5556): `python3 library/tools/find_skill.py "<words>"` (add `--tested` for commands that ran here;
  `"#2836"` for one skill). Indexes: `skills-catalog.md` (#1-560) and `skills2/README.md` (#561+, what each file covers, missing tools).
- Proven repo recipes to build on: CLAUDE.md "Editing a phone video into a professional edit" and
  "Client phone-video edits"; template `library/templates/phone-clip-reel/build.py` [repo: library/README.md "Templates"].

## 3. Owner rules that always apply

- Urdu/Hindi text on video: build ASS and burn with ffmpeg `ass=` (ffmpeg 6.1.1 `subtitles=`/`drawtext` break Nastaliq and Hindi
  conjuncts; tested here 2026-10-24, skills2 #2836, #5121); fonts in `library/fonts` (Noto Nastaliq Urdu, Noto Sans Devanagari).
- Music: CC0 / public domain made by others (`library/music/cc0`), no-credit only; not our own ACE-Step tracks unless
  asked [repo: CLAUDE.md "Environment facts" OWNER RULE Oct 24 2026].
- No ElevenLabs unless the owner names it; voice-over = `ai_voice.py` or `vs_tts.py` [repo: CLAUDE.md "Rules from the owner", "Voice and songs with words"].
- A host/presenter = the owner's skin `library/characters/host-skin.png` via `blocky_character.py` [repo: CLAUDE.md "DEFAULT HOST"].
- First frame is the thumbnail: title or key image at 0 s [repo: CLAUDE.md "HyperFrames learnings"].
- Check before render, snapshot and look at frames, measure audio with `npx hyperframes audio` [repo: CLAUDE.md "HyperFrames learnings"].
- Deliver full quality + a WhatsApp copy (`-crf 23 -preset slow ... -movflags +faststart`) [repo: CLAUDE.md "Editing a phone video" step 8].
- Reply in Roman Urdu [repo: CLAUDE.md "Rules from the owner"].

## 4. After the edit

Anything new that worked or failed goes into `library/research/editing/` (or CLAUDE.md) with source and date
[repo: CLAUDE.md "SAVE ALL USEFUL DATA"].
