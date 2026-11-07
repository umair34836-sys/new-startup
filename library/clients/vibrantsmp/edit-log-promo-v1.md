# Edit log: Vibrant SMP promo v1 (9:16, 26.5 s, 2026-11-07)
- Builder library/templates/smp-discord-promo/build_vibrantsmp.py (gameplay bg when assets/gameplay.mp4 exists).
- VO: ElevenLabs (owner asked, for speed): voice "Liam - Viral Short-Form Storyteller" (VCgLBmBjldJmfphyB8sZ),
  eleven_v4, 1 take, 397 credits, 24.32 s. Whisper small heard the whole script word-for-word; word stamps time the text.
- Music: HoliznaCC0 "Re-Adjustment" (CC0) bed from the Heaven Developer phonk job (from its drop), first 26.5 s, 1.5 s fade;
  constant mix voice -16 LUFS, music ~13 LU under.
- Visuals: real crops (server-info card, roles post, server header, logo from #mc-status), chips on spoken words, kick
  punches, flashes on cuts, rotating impact/pop SFX. Background: owner's parkour gameplay 30-56.5 s, crop 405x720 center
  -> 1080x1920 lanczos + cas 0.5, purple overlay 0.45/0.22/0.6.
- Fix: first logo crop took text; found the logo by purple pixels (x 724-855, y 433-527 in the 40.5 s frame).
- QA: H.264 High yuv420p 30 fps, -15.4 LUFS, -0.9 dB peak, blackdetect 0.

## v2 (2026-11-07): store info + ElevenLabs voice AND transcription (owner)
- Builder build_vibrantsmp_v2.py. VO: same voice (Liam), eleven_v4, 1 take, 411 credits, 25.52 s.
- Transcription: ElevenLabs Scribe (eleven_scribe_v1, 140 credits) on the take attached as a flow asset by URL: heard the
  whole script (65 words; it wrote the IP as "play.vibrantsmp.fun"). This was a real transcription (punctuation and the
  URL differ from the prompt), unlike the flow-alignment echo noted in CLAUDE.md. Its word stamps time every text slam.
- New scenes: "A FREE" hook, store 3D V logo (inline base64 from the store HTML), free-to-play chip + store "How to join"
  crop, store "Featured Packages" crop + Ranks/Crate keys/Player tags/Coins chips, Vote + 4 sites, CTA play.vibrantsmp.fun
  (Java & Bedrock, port 62222) + discord.gg/W7zqUp2kbM. Gameplay 30-57.7 s.
- Bug caught before render: w("at") matched "crate" (first word containing "at") -> used "now".
- QA: H.264 High yuv420p 30 fps, 27.7 s, -15.0 LUFS, -0.8 dB peak, blackdetect 0.
