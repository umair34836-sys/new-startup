# smp-server-promo (voice-led Minecraft server promo, 16:9 + 9:16)

Made 2026-10-29 for the owner's FireCraft SMP ("worldlens wale plugin ka use ker k hamare server k lie promotional
video bana lo ... in game and in dc server images and info ... firecraft.fun"). One scene per VO line, 8 scenes, 24 s.

## Sources (only these; every scene carries a "source" in the config)
- In-game pictures: WorldLens MCP (`worldlens_status`, `worldlens_top`, `worldlens_shot` 1920x1080, 10 s cooldown,
  ~2-3 s render). Measured 2026-10-29: with no player online most spawn chunks were NOT loaded (top map 78 used / 91
  unloaded; shots half sky). With the owner's OK: `forceload add 580 -40 770 150` (169 chunks) -> shots -> `forceload
  remove 580 -40 770 150` (checked `forceload query` first: none). View distance is capped at 96 blocks (fog).
  Good angles found at FireCraft spawn (logo wall z~100): front (675, 84, 58, yaw 0, pitch -4); low hero
  (660, 72, 84, yaw -20, pitch -28, fov 80); spawn aerial (640, 100, 15, yaw -40, pitch 32). An obsidian grid hangs
  above spawn around y 120: keep the camera below it. The logo's back side reads mirrored.
- Discord (read only): `discord_channels`, `discord_read_messages` on #announcements, #smp-announcements, #smp-rules,
  #ip-port. Never write/ping.
- Website: `web_capture.py https://www.firecraft.fun https://www.firecraft.fun/rules/`; images from /images/powers,
  /images/features, /images/gallery/scene-*-1280.webp, /images/logo.webp (1254 px). The gallery scenes look like
  artwork, not in-game captures: real spawn = WorldLens shots, artwork only for powers / PvP / mobs / events.

## Voice (gaming-hype, VoxCPM2 clone, vs_tts.py --parts) - measured 2026-10-29
- First request after starting the backend: ~8 min; then ~1 min per line. 8 lines = 19.8 s.
- Whisper small per line (wcheck_lines.py): brand names and some words failed in 3 seeds: "फायरक्राफ्ट एसएमपी" (line
  start), "स्पॉन" at a line start, "हर हफ्ते"/"हर वीकेंड" short lines. Two seeds produced ~25-30 s of babble for one
  line (last_word_end 24-30 s): always check part lengths. What worked: drop the acronym ("फायरक्राफ्ट का सीज़न टू
  लाइव है", seed 33), drop the hard word and show it on screen ("बाहर रेड करो, अपना बेस खुद बचाओ", seed 33), and leave
  the events scene without VO (text + music). Takes joined with vo_join.py --target-f0 148 (gaming-hype median).

## Music (music-for-video skill)
- find_music.py "gaming minecraft server promo hype" --vo --drop: top CC0 were Traveling in Your Mind, You Know Why,
  La Citadelle. Owner had rejected CC0 picks before, so 4 loudness-matched samples were sent; no answer came, so his
  earlier choices were used: 16:9 Lion - Dyalla (YouTube only), 9:16 Mixkit Uplifting Bass (any platform).
- Lion with `--end resolve` jumped to the composer's ending (179.56 s), which is near silent: the end card had 4.2 s
  of silence (listen.py). Fixed with one continuous segment from the loud section (23.452 s) and `--end fade --fade 2.5`.
- mix_vo_music.py: music_vs_vo_gap_lu 15.0. Final: +1.4-1.6 dB gain + alimiter -> -15.0 LUFS, LRA 6.6, peak -1.35 dBTP.

## Layout lessons
- 9:16 from 16:9 stills: cover-crop cut the logo to "RECRA"; portrait now shows the whole picture as a card over a
  blurred copy (build.py). 16:9 titles sit at y 850 so they don't cover the subject.
- Monitor filters: "0 error(s)" contains "rror": grep for "rendered in", not "rror".
