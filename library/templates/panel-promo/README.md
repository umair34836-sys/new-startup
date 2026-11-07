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
Renders (-w 3, measured 2026-11-07): 71.3 s 16:9 ~3 min, 9:16 ~2 min; render -16.1 LUFS -> +1 dB + alimiter 0.85 ->
-15.2 LUFS; yuv420p, 0 black spans; metadata stripped (`-bsf:v filter_units=remove_types=6`, bitexact AAC: 0 tool
strings). Delivered to the owner and, at his request, as versions 7 + 8 of the portal demo account's order 4
("firecraft smp promotional video": the demo account had no copper_work order; the bridge cannot create orders).

## v2 "jan dallo" edit (owner 2026-11-07: "editing bilkul bhi nhi dekh rahi ... 3d editing, special transitions")
`build_v2.py CONFIG --format ... --out PROJECT` after build.py (it reuses assets/clips + timing.json, rewrites
index.html). CSS-3D stage: moving copper grid floor, particles, each recording on a tilted floating screen with a
rotating enter/exit preset (depth fly, flip, swing, rise) + glare pass, copper light sweep + whoosh on every cut,
headline words rising in 3D, and per-scene `fx` kinds (hook cube, flow diagram, push, tiles, toasts, shutter, orbit
counter, glitch + Confirm, stack, steps, connected shockwave, end card with typed URL). Config `words` = Whisper word
times on the video timeline (Hindi words aliased to English keys for lookups).
Lessons (hyperframes check here): a relative `rotationY:"+=6"` drift while the entry tween still wrote rotationY was a
`gsap_relative_value_second_writer` ERROR: drift with absolute y/z only. Two fromTo on one element -> second as tl.to.
9:16: one-line hook text needs ~84 px (112 px wrapped and overlapped the next line); keep pop-out tiles over the screen,
not over the headline; 4 chips in one row at 250 px spacing.
