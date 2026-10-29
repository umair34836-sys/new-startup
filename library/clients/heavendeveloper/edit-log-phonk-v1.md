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

## v3 = formula v2 (owner 2026-10-29: "bhot boring ... upgrade it and upgrade your formula")
Builder build_heavendeveloper_phonk_v2.py + post.sh; research library/research/phonk-edit-formula.md (sources + dates).
Same VO/music/mix as v2 (verified), new picture: beat-cut camera shots, kick punches, flashes, snare RGB split, cold
grade, grain, depth text, clones/crowd ("2,500+ MEMBERS", "17 BOOSTS • LEVEL 3": brief.md), jump on $4, letterbox.
Snapshot fixes: face close-up lowered (head covered "BUILDS IT ALL"), crowd 2 rows x 4 (3 rows overlapped).
QA: -15.3 LUFS, -1.91 dBTP, 0 clipped, 30.0 fps, blackdetect 0. Preview watermarked; clean kept in the scratchpad.

## v4 = client feedback round (2026-10-29, Discord #edits screenshots from the owner)
Client: "with phonk, with beats, with vibes - this one is not good"; remove the watermark; "mostly talk about Minecraft";
English only; "tell the plans are free, don't explain invites and paid". Owner then also asked for a NO-VOICE, NOT
Minecraft-focused cut. Both delivered as clean finals (no watermark).
- Music: HoliznaCC0 "Re-Adjustment" (CC0, catalogued) from its drop (music_fit --src-drop 13.978 -> 14.65 on the bar
  grid): listen.py RMS -8 dB in 14-60 s vs -13 dB for "Phonk-ish"; voice activity only 0-12 s (not used).
  Rejected: archive.org "Fox72z" phonk items (subject "Suno Ai", PD Mark set by uploader: licence doubt);
  "Alec Penn Radio" phonk (CC0 on archive.org, own site says "free to use, AI co-created with Suno", but listen.py voice
  activity 37-86 % = vocals that would fight the VO); other PD-marked items are re-uploads of other artists' songs.
  fetch_free_music.py "drift phonk"/"phonk cowbell"/"brazilian phonk" found 0 tracks; "phonk" returned HTTP 404.
- "Free": VO "And you can start for free." + "START FOR FREE" on screen = brief.md #pricing "PLANS Free"; paid/invites not
  mentioned (client's ask). No claim that everything is free.
- Minecraft cut (build_heavendeveloper_phonk_v3.py): VO gaming-hype --lang en, 7 lines, Whisper small heard all 7
  word-for-word; lines on downbeats 0.3/2.694/5.364/9.368/13.351/17.357/24.021, crowd bar 18.6-23.9 music-only.
  Minecraft night world (square moon, grass floor), textured CSS cubes (new voxel_textures: diamond/emerald ore, gold,
  TNT, obsidian), block tower per beat, inventory GUI, TNT blast, texture swap per beat; Minecraft SFX rotated.
  Snapshot fixes: moon behind titles -> top corner; GUI hidden by character -> left, character right; chips overlapped -> 128 px.
  QA: -15.5 LUFS, -1.9 dB peak, 30 fps, blackdetect 0. Render -w 3: 1m37s capture.
- No-voice cut (build_heavendeveloper_phonk_novo.py): neon studio bg, text-only: NEED A DISCORD BOT/WEBSITE/MINECRAFT
  PLUGIN, logo + "PREMIUM DEVELOPMENT, DELIVERED" (bot footer line), WE BUILD x5 services, DISCORD BOTS + WEBSITES chips
  (#services), START FOR FREE, members/boosts, CTA. Scene grid on downbeats. Render -13.5 LUFS -> post GAIN=0.2 -> -15.3
  LUFS, -1.9 dB peak, 30 fps, blackdetect 0.
