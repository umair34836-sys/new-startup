# discord-server-promo (9:16, 30 s, VO-synced, from a screen recording of the client's Discord server)

Made for Heaven Developer (a Discord server selling bots, websites, Minecraft plugins/mods, texture packs) on 2026-10-28.
Input was only the owner's phone screen recording of the server; every claim comes from its frames
(library/clients/heavendeveloper/brief.md). Edit log with every decision: library/clients/heavendeveloper/edit-log-promo-v1.md.

`build_heavendeveloper.py` (run inside the HyperFrames project) writes index.html + compositions/{bg,s1..s7}.html;
scene starts = VO line starts from assets/vo/lines.json (vs_tts.py --parts). Audio = one mix.wav from mix_vo_music.py
plus SFX lanes.

Prepare the project (scratchpad only, never git):
1. Frames: `ffmpeg -ss T -i rec.mp4 -frames:v 1 f_T.jpg`; crop the embeds (pricing, services, invite, review), the
   banner and the logo with PIL. Crop away the phone status bar, the server sidebar and other members' chats.
2. Real motion: `ffmpeg -ss 45 -t 5 -i rec.mp4 -an -vf "crop=948:2040:0:100,fps=30" assets/clips/services.mp4`
   (a scroll through the channel, played inside the phone frame).
3. VO: `vs_tts.py script.txt vo.wav --voice <field voice> --lang en; promo-male used in v1 is BANNED since 2026-10-28 --parts parts` (--lang en added 2026-10-28: a saved
   voice otherwise forces its own language, hi).
4. Music: skill music-for-video (find_music.py -> listen.py -> music_fit.py -> mix_vo_music.py).
5. `python3 build_heavendeveloper.py && npx hyperframes check && npx hyperframes snapshot --at ...`, render -w 3.
