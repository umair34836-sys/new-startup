# Edit log: Heaven Developer FULL promo v1 (9:16, 119.4 s, 24 scenes, 2026-10-28)

Owner: "ek video or banao jis me everything cover kro her ek chote se choti jizz cover keroo for promotional", then a second
recording "Is video se jitni info cover ker sakte ho uthna cover kro". Owner choices: voice explainer-pro, clean final,
format/length "as a pro editor from the repo".
- Format: 9:16 like v1 (both inputs are vertical phone recordings; decision-guide 26 + pk-reels-trends.md: Shorts allow up
  to 3 min). Length = the VO: every promotional fact in both recordings (brief.md) = 24 lines = 116.5 s of speech.
- Facts: brief.md (recording 1 + recording 2 sections). Left out: other members' names (top inviters, boost thanks),
  staff-only channels, the owner's own ticket/edits chat, the outdated "1,600+ members" announcement.
- Builder: library/templates/discord-server-promo/build_heavendeveloper_full.py (one scene per VO line: feature scenes
  with label/icon/title/chips + a proof crop of the real post, price list, plans, order steps + real orders banner,
  invite cards, security cards, bot, review, member count-up (#425), end card).
- VO: vs_tts.py --voice explainer-pro --lang en. Lines 1-4 from the first run, line 5 from the second, lines 6-24 after a
  VoiceStudio backend crash (curl failed on line 6; health down; restarted with voicestudio.sh start, generation resumed
  from line 6). Whisper small heard "Discord boards" in line 3 -> retake seed 21 -> "Discord bots". All other lines
  word-for-word (2500 / $5 / $4 / 17 / 3 as digits). Measured here 2026-10-28: ~3-6 min per line while ffmpeg also ran.
- Music (skill music-for-video): same CC0 "Monarch of the Street" as v1 (brand continuity; find_music top pick again),
  music_fit --length 119.43 --end resolve: [0-117.6] + own ending [222.13-223.96], join phase error 33.5 ms vs 20 ms
  noise (accepted), mix_vo_music gap 15.0 LU.
- QA: check passed; 24 snapshots at line ends, fixes: proof-crop offsets (headers were cut), Support crop re-made from the
  full dropdown frame (168 s), lounge chips hidden behind the crop (smaller crop). Render -w 3: 4m46s. listen.py -15.8 LUFS,
  TP -1.25, 0 clipped; watch.py 30.0 fps, 3583 frames; blackdetect 0 spans.
- npx hyperframes (no version) tried to fetch 0.8.212 and failed "notarget" (2026-10-28): use npx -y hyperframes@0.8.210.
