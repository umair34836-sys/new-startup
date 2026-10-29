# Edit log: Heaven Developer PHONK 3D promo v1/v2 (9:16, 30 s, 2026-10-29)

Client (Bhupendra, Discord #edits, screenshot from the owner 2026-10-29): "Can you make a 30 seconds edit? With a phonk,
Promotional, About Heaven Developer ... With 3d animations, Like 3d characters ... Preview first!". Owner choices
(AskUserQuestion): 3D character = Bhupendra look-alike; English VO too. Thumbnail feedback ("just a thumbnail ... all in
one") was set aside by the owner ("tumbnail wali bat choro").
- Builder: library/templates/phonk-3d-promo/build_heavendeveloper_phonk.py. 8 scenes: 7 VO lines + one music-only bar.
  Every scene: the CSS-3D blocky rig (blocky_character.py: rig_html/pose_js, poses idle/shock/think/point/talk/wave/walk/
  spin/run) on a neon grid floor; Anton slams with RGB-split glow, hit shakes (#161/#162, even repeat ends at rest),
  scene flashes (#123), beat pulses on every music beat; impact SFX rotate impact-boom / sub-drop / punch-heavy and
  whoosh / swish-4 (Mr Aloo feedback: one repeated pop sounds cheap).
- Character: v1 used a painted look-alike (library/tools/make_bhupendra_skin.py, from the site avatar). v2 uses the
  client's REAL 64x64 skin that the owner sent in chat (2026-10-29): kept in the scratchpad only, not committed.
- VO: vs_tts.py --voice gaming-hype --lang en, 7 lines; Whisper small heard all 7 word-for-word. Each line placed on a
  music downbeat (listen.py on the fitted bed: 75 BPM, bar 3.199 s, downbeats 3.17, 6.37, 9.57, 12.77, 15.98, 19.17,
  22.37): lines at 0.3, 3.17, 6.37, 9.57, 12.77, 15.98, (19.17 = music-only "PREMIUM DEVELOPMENT DELIVERED." bar), 22.37.
- Music (music-for-video): no phonk in the catalogue, so fetch_free_music.py "phonk" fetched 5 CC0 tracks by HoliznaCC0
  (album "Phonk Aura Farming", licence re-read per page) and music_catalogue.py measured them. Picked "Phonk-ish":
  listen.py tense/driving, A minor, no vocals, drop/chorus from 15.7 s. Rejected "Phonk Remix" (calm/warm, voice
  activity 3-10 s) and "Pantheon" (40 clipped samples, voice activity at the start). music_fit --start 15.7 --length 30
  (bar grid moved the start to 16.05; fade-out track -> hit + ring-out; last 1 s -36 dBFS). mix_vo_music --gap 12
  (phonk kept louder than the 15 LU default; still >= 12 LU under the voice).
- QA: check passed after fixes (flash/beat-pulse fromTo got immediateRender:false: frame 0 was washed white; character
  scale 26 -> 20 so the head no longer covers the text; hook text + character on screen at 0 s; SFX lanes widened for
  overlapping sub-drops). Render -w 3: 1m21s; -17.2 LUFS -> +2.2 dB + alimiter 0.79 = -15.2 LUFS, -1.92 dBTP, 0 clipped;
  watch.py 30.0 fps; blackdetect 0. Preview = watermark.py; clean file kept in the scratchpad.
