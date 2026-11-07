# panel-promo (web panel / SaaS promo, 16:9 + 9:16, real screen recordings + one finished VO)

First used: copper_work (https://plugin.firecraft.fun, the owner's own Minecraft server panel), 2026-11-07.
1. `flow_copperwork.js` records the public site and the logged-in panel with library/tools/screen_recorder.js
   (cursor + ripple on clicks, CSS zoom 1.4, 1920x1080 or 1080x1920). Logged-in shots use a Playwright `storageState`
   file made once from the owner's demo login (scratchpad only, chmod 600, never committed). Public pages look
   different when logged in (home redirected to the dashboard), so those shots run without the state.
   A privacy mask (initScripts) rewrites text before it is drawn: IPv4, e-mail, `cwk_` server keys, UUIDs, player
   names in join/leave/auth lines and whole chat lines (`[chat] •••`). A first version replaced any word after
   "Disconnecting" and turned "Disconnecting signs the app out" into "Disconnecting Player the app": keep name rules tied
   to log shapes ("of player X", "X (/ip", "client X") and look at a frame of every page.
   Delete a shot's folder before re-recording it: the recorder does not clear old frames.
   Only harmless things are clicked: console `list`, an existing AI chat, Copy, view toggles. Never Add/Save/Remove.
2. VO: one ElevenLabs take (owner asked for it) checked with Whisper medium (hi). Scenes are cut at the silences
   (`silencedetect=n=-40dB:d=0.3`) between script lines.
3. Music: music_fit.py --length TOTAL --end resolve; VO placed at 0.3 s (adelay + apad); mix_vo_music.py -> mix.wav.
4. `build.py CONFIG --format 16x9|9x16 --out PROJECT`: speed-fits each recording span to its scene, writes one small
   caption card per scene (title + sub or chips, text from the site), a "big" word option and an end card; whoosh /
   click / pop SFX rotate 3 variants each. Look comes from the product's own CSS tokens (bg #181818, panel #1f1f1f,
   copper #c9a35a, ok #4fd1a1, Geist + Geist Mono from the site). Hallmark floor: no eyebrow labels or tracked caps.

copper_work numbers (measured here 2026-11-07): ElevenLabs eleven_v4, voice "Viraj – Viral Ad & Content Voice"
(pHG3exaXQt8bmTWbaVOs): 12-line Hindi script = 69.6 s / 69.2 s per take, 1007 credits per take (estimate 2014 for 2).
Both takes read "copper_work" as "copper underscore work" (Whisper hi and en): the brand line was re-voiced as
"कॉपर वर्क" (83 credits per take, 5.76 s) and spliced at the 6.0 s silence. Whisper medium on 2 x 69 s took ~10 min.
Spans ran at 0.64-2.28x. Music: CC0 "Monarch of the Street" (Loyalty Freak Music, find_music rank 1 for a tech promo
with VO), real ending used; mix: VO -16 LUFS, music -31 LUFS under speech, final -16.0 LUFS.
