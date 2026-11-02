# minecraft-lore-short (9:16, ~20 s cinematic lore explainer: English VO + dark CC0 music + CSS-3D blocky figure)
Made for portal order 2 "Who is Herobrine" (2026-10-30). Facts: library/research/herobrine.md (minecraft.wiki).
Builder `build_herobrine.py` (base: templates/phonk-3d-promo): one scene per VO line, slow push-in + blur cross-fades,
fog + lightning stock layers, white eye glows, Whisper word-group captions (3-4 words, gold longest word).
Own skin: `python3 make_shadow_skin.py assets/characters/shadow-skin.png` (hooded figure, white eyes; not Mojang's Steve).
Project assets: fonts Anton + Poppins-Bold, library/vendor gsap, sfx (rain-thunder, heartbeat, sub-drop, glitch-short,
impact-boom, wind-loop), video library/stock own-overlays/smoke-fog-vertical.mp4 + weather/lightning-storm-night.mp4,
assets/audio/mix.wav (mix_vo_music.py --vo-at VO_START), assets/vo/lines.json, assets/vo/words.json ([start,end,word]).
Run: `VO_START=0.3 TOTAL=21.5 python3 build_herobrine.py`, `npx -y hyperframes@0.8.210 check`, snapshot, `render -w 3`.

Measured here 2026-10-30:
- vs_tts.py --voice luxury-deep --lang en: 7 lines / 56 words = 33.0 s (too long for 20 s). A 7-line, 37-word script
  = 24.4 s, with a 1.0 s and 0.8 s pause inside line 6. Cutting those pauses to ~0.3/0.45 s and atempo 1.15 gave 20.5 s;
  Whisper small still heard every word ("Herobrine" spelled "Harobrin": put the real spelling in captions).
- Budget for a 20 s English Short with this voice: about 35 words.
- hyperframes check: a gsap fromTo on the title at t=0 leaves frame 0 empty (thumbnail): keep the hook title static.
  "line_unread" flags text shown < 0.5 s + 0.3 s/word: keep on-screen text to 2-4 words per short scene.
- Music: cinematic--zombies-march.mp3 (OpenGameArt CC0, A minor, 93.3 BPM, LRA 2.4 = steady under a VO), music_fit
  --end fade 1.5; mix gap 15.0 LU; render -15.6 LUFS, peak -2.3 dBFS; 21.5 s rendered in 1m18s with -w 3.
