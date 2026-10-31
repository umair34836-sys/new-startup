# WaterSMP promo v1 (portal order #5) - edit log, 2026-10-31

Brief: library/clients/watersmp/brief.md. Order had no files; visuals made from the repo + the server's public status.

## Choices and their sources (CLAUDE.md SKILL-BASED ONLY)
- Template: library/templates/phonk-3d-promo, formula v2 (owner: start from v2/v3, v1 was "boring"); new builder
  build_watersmp.py. Why: Minecraft SMP promo, 9:16, 30 s, gaming hype, no client footage -> 3D blocky character in
  every scene (CLAUDE.md DEFAULT HOST = library/characters/host-skin.png) + kinetic type; cut on every beat.
- Shape 9:16 (client "not sure", posts to Instagram/Facebook reels).
- Brand: server MOTD gradient #17C8F5 -> #08A2FB + MOTD gold #FFAA00 (api.mcsrvstat.us, 2026-10-31); real 64 px server
  icon upscaled x8 nearest-neighbour (pixel art stays crisp). Own 16x16 pixel sword drawn here for the PvP scenes.
- Hard names kept on screen (voice can garble them: smp-server-promo README): WATERSMP, 3RD NOVEMBER, EPIC PVP
  TOURNAMENT, IP play.watersmp.in, PORT 25590, JAVA + BEDROCK, JOIN NOW.
- Captions: English line per VO chunk (client asked English captions; VO Hindi), dark pill at y 1360.
- Voice: field voice gaming-hype (voices README: Minecraft/gaming server promos; promo-male banned), vs_tts.py, script in
  Devanagari (client's Roman Hindi script, emoji dropped). Whisper small per line (wcheck_lines.py):
  seed 7 lines 1,3,4,6 kept; lines 2 and 5 from seed 33 (seed 7 line 5 doubled "aap"); line 3 "exciting survival
  experience" weak in seeds 7/21/33 (24-33%) -> seed 7 kept, words shown on screen. Line 7 "See you on WaterSMP" was
  garbled in 4 takes (seeds 7/21/33, also --lang en with Latin text); a take of "तो मिलते हैं, सी यू ऑन वॉटर एसएमपी"
  (seed 7) was clear and was cut at the pause before "सी" (0.78 s) -> Whisper "see you on Water S&P".
  Joined with vo_join.py --gap 0.4 --target-f0 148: VO 26.0 s.
- Music (music-for-video skill): find_music.py "gaming minecraft server promo hype" --length 32 --client --vo --drop ->
  #1 cc0 HoliznaCC0 "Phonk Remix" (CC0 1.0; gaming/promo tags, 92 BPM steady grid CV 0.013, steady level under VO).
  listen.py: drop/chorus 31.3-95.8 s, so music_fit --start 31.3 --length 30 --end fade --fade 2 (fade from the downbeat
  at 26.73 s, under the end card; beat CV 0.009, no joins). Rejected: #2 Traveling in Your Mind (172 BPM, outside band),
  #3 You Know Why (slow intro, full sound only at 21 s).
- Mix: mix_vo_music.py --vo-at 0.3 -> music_vs_vo_gap_lu 15.0. SFX: impacts rotated (impact-boom / punch-heavy /
  sub-drop, 0.3), whoosh/swish per scene, splash on the WATERSMP reveal, sword-draw on PvP, game-coin on rewards,
  game-levelup on JOIN NOW.
- HyperFrames check: bubbles first used radial-gradient (25 heavy-overlay elements, warning); changed to flat rgba.
