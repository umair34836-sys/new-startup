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

## Delivery (2026-11-07)
- Owner: Vibrant SMP belongs to the same client as this session (Heaven Developer / BHUPENDRA) -> deliver via the portal.
- Portal (editor.firecraft.fun, bridge ping ok): this session's portal client = client #3, order #3 (was "draft", no
  versions). `portal_bridge.py deliver 3 VibrantSMP_promo_v2_FINAL.mp4` (36.2 MB, chunked upload) -> version 6,
  order status now "delivered". Gmail could not take it (25 MB attachment limit); Drive folder had canAddChildren=false.
- Only ids/status/session fields of portal orders were read to find the client's order; no client-written text opened.

## Cinematic trailer + cinematic horror (2026-11-09; owner: in-game video + store info, ElevenLabs voice, 2 videos)
- Input: Drive 1__MoXI44-tjFb6660mAKm6otrn6A2d1S "2026-11-09 08-21-29.mp4" (1280x720 60 fps, 128.2 s): a spawn flythrough.
  Replay-editor UI shows before ~8 s and after ~112 s (not used). Seen signs/places: CRATES (Vote, Party, Rare, Epic,
  Spawner crates), AUCTION, RTP (+ "RTPZONE ... Teleports all players in the box to the same location"), SHOP, RANKS
  (rank NPC podiums), LEADER(boards: boards with player names not used), Overworld/Nether NPCs.
- Builder build_vibrantsmp_cinematic.py, MODE=trailer|horror, 16:9 1920x1080 (the footage is 16:9: no 2.67x 9:16 crop).
- VO (ElevenLabs eleven_v4, 1 take each): trailer "Don - Movie Trailers" (JJCR1UICgHnHljtvu5uF) 29.84 s, 344 credits;
  horror "True - Crime & Horror Narrator" (tZssYepgGaQmegsMEXjK) 22.96 s, 294 credits. Scribe: trailer 58 words 164 credits,
  horror 47 words 126 credits; both heard every word; word stamps time the shot cuts and titles.
- Music: trailer Komiku "Ultimate Power" (CC0) from 2.1 s so its drop (19.81 s, listen.py section) lands on "Climb the
  ranks"; horror Loyalty-free CC0 "Zombies March" pitched/slowed to x0.82, lowpass 2.6 kHz, echo = eerie bed.
- Trailer: cuts on VO words, push-ins, letterbox 140 px, flashes, booms on brand/drop, riser into the drop, teal-orange grade.
  Horror: 0.5x slow-mo (60 fps source -> clean 30 fps), drifting push-ins, random black flickers, heartbeat, static +
  glitch at RTP, riser + sub-drop on the logo; grade brightness -0.05, contrast 1.28, saturation 0.42, gamma 0.82, grain 16.
- Bugs caught: w("Your") matched "carve your name" (negative shot length) -> 2nd occurrence; red "SMP" vanished under the
  horror desaturation -> #ff2a3c + saturation 0.42.
- QA: both H.264 High yuv420p 1920x1080 30 fps; trailer 34.0 s -15.1 LUFS; horror 28.0 s -15.5 LUFS, -0.6 dB peak.
- Delivery size: horror with grain 16 at crf 17 came out 486 MB (464 MiB > the 400 MiB chat limit). Re-encoded with
  crf 19 + maxrate 16M / bufsize 32M -> 58 MB (16.7 Mbps), same grade/loudness. Strong grain needs a bitrate cap.
