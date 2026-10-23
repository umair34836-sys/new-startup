---
name: clean-video-voice
description: When the owner gives a video (or audio) that already has someone talking, use THAT voice as the voiceover - remove noise, music, TV, crowd, fan/AC hum, hiss, wind and all other background sound so only the person's voice remains, and put the clean voice back into the video. Use for "is video ki awaaz saaf karo", "noise hatao", "background sound hatao", "sirf awaaz chahiye", or whenever an uploaded clip with speech is used in an edit.
---

# Clean the voice that is already in a video

Owner rule: if a video already has a voice, use that voice (don't generate a new one), and clean it so ONLY the
person's voice is heard.

1. Wait for `/home/user/tools/.heavy-ready` (SessionStart installs audio-separator and its models).
2. Work in the scratchpad only (personal media never goes to git). Run in the background with a per-minute monitor:
   ```bash
   cd /home/user/tools && venv/bin/python -u /home/user/new-startup/library/tools/clean_voice.py \
     <scratchpad>/input.mp4 --out <scratchpad>/clean --lang hi
   ```
   - `--dereverb` when the room sounds echoey (bathroom, hall, empty room).
   - `--fast` for long clips when time matters (quicker, slightly less clean).
   - `--no-denoise` if the voice sounds thin/robotic after cleaning.
3. Outputs: `clean.mp4` (same video, clean sound), `voice.wav` (voice only, to use under music or in an edit),
   `report.json` (Whisper transcript: check the words survived), and `work/` with each step's audio.
4. Verify before handing over: transcript matches what is said; measure gaps with pyworld/volumedetect (music and
   noise should be far below the voice). Claude can't listen, so tell the owner what was measured and ask them to
   listen.
5. In an edit, use `voice.wav` as the voice track; add music under it with `voice_over_music.py` only if asked.

Speed on this CPU box (26 s test): full = ~8 min vocals + ~3 min denoise (~25x the clip length); `--fast` = 43 s
vocals + ~3 min denoise. Full is clearly cleaner (pauses -106 dB vs -69 dB before denoise). For clips over ~1 minute
say how long it will take and offer `--fast`. A background song with a singer stays (it is a voice too).
