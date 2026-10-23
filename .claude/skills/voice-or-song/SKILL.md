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
| Voice over AND background music | Make the voice with ai_voice.py, music separately (library/music or ai_song.py instrumental), mix with `voice_over_music.py` | both |

If it is genuinely unclear, ask one short question. Never use ElevenLabs unless the owner names it.

## Voice over (ai_voice.py)

1. Tools: wait for `/home/user/tools/.heavy-ready` (the SessionStart hook installs ACE-Step, Whisper, audio-separator).
2. Write the script one spoken line per row, ALL in Devanagari, English words included (वीडियो, माइनक्राफ्ट, लाइक).
   Short lines (3-8 words) work best; each line is generated on its own.
3. Run in the background with a per-minute status monitor (the owner wants minute-by-minute updates):
   ```bash
   cd /home/user/tools && venv/bin/python -u /home/user/new-startup/library/tools/ai_voice.py \
     --script lines.txt --out <scratchpad>/voice --voice "warm friendly male"
   ```
   `--voice "soft female"` etc. for another voice. Rerunning resumes; editing one line redoes only that line.
4. Check `report.json`: every line's `score` (Whisper match of that line) and `heard`. Below ~0.6, look at the
   line: rewrite it shorter/simpler in Devanagari and rerun (only that line regenerates), or raise `--rounds`.
5. Hand over `voice.mp3` with SendUserFile. Personal scripts and outputs stay in the scratchpad, never in git.

Timing on this CPU box: ~1.5 min per round of 3 takes per line + ~1 min music removal per line.

## Song (ai_song.py)

Use the loved recipe from CLAUDE.md (seed 7, 80 BPM, the romantic Hindi ballad caption) unless the owner asks for
another style. It keeps the music and pulls the beat back under the sung words.
