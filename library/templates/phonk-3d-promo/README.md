# phonk-3d-promo (9:16, 30 s, phonk beat + English VO + a 3D blocky character in every scene)
Made for Heaven Developer, 2026-10-29 (edit log library/clients/heavendeveloper/edit-log-phonk-v1.md).
Setup in the HyperFrames project: assets/characters/<skin>.png (the client's real 64x64 skin, or a painted look-alike
such as library/tools/make_bhupendra_skin.py), assets/img/logo_circle.png, assets/fonts/{Anton-Regular,Outfit-Bold}.ttf,
assets/sfx (impact-boom, sub-drop, punch-heavy, whoosh-fast-0.3s, swish-4, cash-register, confirm-1), assets/vendor gsap,
assets/music/beats.json (listen.py rhythm.beats_s of the fitted bed), assets/vo/lines.json (one entry per scene; a fake
2 s entry = a music-only scene), assets/audio/mix.wav (VO placed on downbeats + bed, mix_vo_music.py).
Then `python3 build_heavendeveloper_phonk.py`, `npx -y hyperframes@0.8.210 check`, snapshot, render -w 3, gain + alimiter.
