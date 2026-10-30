# Edit log: Heaven Developer LOOP SHORT (YouTube Short, 9:16, 33.95 s, dark + white, 2026-10-30)

Owner: from scratch, entertaining + promotional YouTube Short, natural female voice, a hook, a seamless loop ("user ko
pata na lage k end hogya hai"), all info from the repo + the Discord recordings, dark look AND white look, the client's
skin. Then: "Target audience foriners hai" -> English VO, captions and on-screen text only; no price/currency shown.
- Template: library/templates/loop-short/build_heavendeveloper_loop.py (THEME=dark|light). Decision guide 14 (loop: end
  on a frame that leads into the first, trim music to whole bars, EasyReels 2026-10-10) and 27 (captions: few words at a
  time, active word coloured, out of the bottom 420 px, Clyper 2026-10-10).
- Script (facts from brief.md): hook "Need a Discord bot, a website, or a Minecraft plugin?"; "Premium development,
  delivered" (bot footer line); bots: moderation, tickets, economy, dashboards; websites: portfolios ... web apps;
  Minecraft plugins, mods, texture packs; order flow 1 Choose > 2 Fill the form > 3 private ticket (#create-ticket);
  2,500+ members (2,521) + 17 boosts; "start for free" (#pricing Free plan); CTA discord.gg/heavendeveloper.
  Left out: the 5/5 review (its post names BHUPENDRA as the client, so it is not independent proof).
- Loop: last line "So join Heaven Developer on Discord, because if you still" runs into line 1 "Need a ..."; the end card
  clears and rebuilds the frame-0 layout ("Need a" + character wide/idle); background drift = one full sine period.
  Measured: mean abs grey difference first vs last frame 0.75 (dark) / 0.53 (light) of 255.
- Voice: explainer-pro (female, voices/README Whisper 0.90; used on this client's FULL promo) --lang en, 9 lines; Whisper
  small heard all 9 word-for-word. Lines laid end to end with equal 0.286 s gaps (incl. the seam) to fill 14 bars.
- Music (music-for-video): find_music.py "promo tech upbeat entertaining short" --client --vo --platform shorts -> #1
  Loyalty Freak Music "Monarch of the Street" (CC0, 99 BPM, beat CV 0.012, LRA ~1.7 LU). listen.py: steady section
  65.5-202.4 s, downbeat 66.688 s; cut exactly 14 bars (33.95 s) with 5 ms edge fades only, so the replay continues the groove.
- Mix: mix_vo_music.py ducking left the music full at 0 s (-15.9 dB RMS first 0.3 s) but ducked at the end (-30.9 dB): a
  jump at the seam. Replaced by a constant mix (voice -16 LUFS, music 14 LU under, numpy + pyloudnorm): music RMS first /
  last 0.3 s = -34.2 / -30.9 dB (groove only). Pops rotate pop-high / bubble-pop / plop.
- Real screens (scratchpad crops of recordings 1+2): banner, #services post (panned to each section), "Choose a service"
  menu, server profile card (2,521 Members). Minecraft cubes from voxel_textures. Skin: client's own (not committed).
- Snapshot fixes: services crop did not pan (GSAP y overwrote the CSS translate -> fromTo from -crop); order menu covered
  the steps (narrower card, steps at 620 px); CTA URL held to d-0.75; floor shadow so the white skin reads on the light theme.
- QA: both H.264 High yuv420p 30 fps, -15.5 LUFS, -1.0 dB peak, blackdetect 0.
