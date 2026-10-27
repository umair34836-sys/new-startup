---
name: voice-or-song
description: Make the owner's Hindi/Hinglish audio with the local ACE-Step voice. Use whenever the owner asks for a voice over, voiceover, narration, awaaz, "bolne wali awaaz", host voice or dialogue (→ spoken voice with ZERO music), or for a song, gaana, music, beat or "music ke sath" (→ song with music). Not ElevenLabs unless the owner names it.
---

# Voice over or song?

Decide from the owner's words (Roman Urdu/Hindi):

| Owner says | Make | Tool |
|---|---|---|
| "voice over", "voiceover", "narration", "awaaz", "sirf voice", "bol ke", host/dialogue lines | Spoken voice, music must be ZERO, every line present | `library/tools/ai_voice.py` |
| "song", "gaana", "music", "beat", "music ke sath", "background music" | Song with vocals and music | `library/tools/ai_song.py` (loved recipe in CLAUDE.md) |
| "VoiceStudio", "ElevenLabs jaisi awaaz", voice clone ("meri/is ki awaaz mein"), Urdu/Pashto voiceover | Spoken voice from VoiceStudio (local ElevenLabs replacement) | `library/tools/vs_tts.py` (section below) |
| Voice over AND background music | Make the voice with ai_voice.py, music separately (library/music or ai_song.py instrumental), mix with `voice_over_music.py` | both |

If it is genuinely unclear, ask one short question. Never use ElevenLabs unless the owner names it.

## Voice over (ai_voice.py)

1. Tools: wait for `/home/user/tools/.heavy-ready` (the SessionStart hook installs ACE-Step, Whisper, audio-separator).
2. Write the script one spoken line per row, ALL in Devanagari, English words included (वीडियो, माइनक्राफ्ट, लाइक).
   Short lines (3-8 words) work best. Lines are spoken together in groups of 6 (`--group`, default 6 in ai_voice.py):
   in the Oct 2026 test a lone short line per take came out garbled, a whole passage per take worked.
3. Run in the background with a per-minute status monitor (the owner wants minute-by-minute updates):
   ```bash
   cd /home/user/tools && venv/bin/python -u /home/user/new-startup/library/tools/ai_voice.py \
     --script lines.txt --out <scratchpad>/voice --voice "warm friendly male"
   ```
   `--voice "soft female"` etc. for another voice. Rerunning resumes from the cached takes (out/groups/NN/<seed>.flac).
   Caution (read from the code 2026-10-24): the cache is keyed by group number and seed, NOT by the text, so after
   editing a line delete that line's `out/groups/NN/` folder (NN = first line index of its group, from 00) or the old
   takes are re-scored against the new text instead of being regenerated.
4. Check `report.json`: every line's `score` (Whisper match of that line) and `heard`. Below ~0.6, look at the
   line: rewrite it shorter/simpler in Devanagari, delete its group's cache folder and rerun (that group regenerates),
   or raise `--rounds`.
5. Hand over `voice.mp3` with SendUserFile. Personal scripts and outputs stay in the scratchpad, never in git.

Timing on this CPU box (Oct 2026 test, 6 lines): ~6.5 min per round of 3 x 25 s takes of a group + ~1 min music
removal per line.

## Song (ai_song.py)

First, if the ACE-Step weights are missing (`/home/user/tools/ACE-Step-1.5/checkpoints`), run `bash library/tools/setup-all.sh acestep` (~6 GB, on demand since 2026-10-27).


Use the loved recipe from CLAUDE.md (seed 7, 80 BPM, the romantic Hindi ballad caption) unless the owner asks for
another style. It keeps the music and pulls the beat back under the sung words.

## VoiceStudio voice (vs_tts.py), the local ElevenLabs replacement (Oct 2026)

**Pick a field voice first (owner, 2026-10-27; there is no default voice).** `--voice <name>` with one of:
- promo-male, promo-female (promos, offers)
- tutorial-calm (tutorials)
- explainer-pro (explainers)
- gaming-hype (gaming / Minecraft)
- food-warm (food)
- story-emotional (stories / shayari)
- kids-cheerful (kids / funny)
- luxury-deep (luxury / premium)
- news-anchor (announcements)

The table with what each one fits and its measurements is in library/voices/README.md. Hindi, VoxCPM2, Apache-2.0.

Clean spoken speech, no music at all, in 600+ languages incl. Urdu, Hindi and Pashto; voice design by text
(`--instruct "male, middle-aged, low pitch"`) and zero-shot cloning (`--ref clip.wav --ref-text "..."`, only voices
the owner may use). Oct 24 2026 test, Whisper word match: Urdu 100% / 97%, Hindi 92%, Pashto 81%; 4.4-9.5 s clips
took 22-36 s on CPU incl. model load (~4-5x the audio length).

1. `bash library/tools/voicestudio.sh start` (needs `/home/user/tools/.heavy-ready`; backend on :3900). If GET /models
   shows k2-fsa/OmniVoice not installed: POST /models/install {"repo_id":"k2-fsa/OmniVoice"} (3.27 GB per HF API
   2026-10-24; took ~30 s in Oct 2026).
   Licences must be accepted once per machine (owner chose to accept OmniVoice + VoxCPM2 on Oct 24 2026):
   GET /models/licenses/details/<repo> -> acceptance.fingerprint -> POST /models/licenses/accept.
2. Script: one sentence per line in the language's own script (Urdu/Pashto Nastaliq, Hindi Devanagari).
3. `python3 library/tools/vs_tts.py lines.txt <scratchpad>/voice.mp3 --lang ur --instruct "male, young adult"`.
4. Verify with Whisper (venv) before handing over.

LICENCE: OmniVoice weights are NON-COMMERCIAL (CC-BY-NC): personal/own videos only. For client or paid videos use
`--model voxcpm2` (Apache-2.0, Hindi among 30 languages, no Urdu, no Pashto, 4.96 GB download: HF API 2026-10-24;
slower) or ai_voice.py (ours).
