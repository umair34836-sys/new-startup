# FireCraft SMP 15 s 9:16 cut-down (owner request via main session, 2026-10-30)
Source: portal order 4 project (60 s 16:9 promo). Nothing new: same client gameplay, same site facts (firecraft.fun,
re-checked 2026-10-30), same CC0 music, same Whisper-checked VO takes, same end card. Not posted to the portal.

- Format: 9:16 1080x1920 (main session's pick; owner named none). 15.0 s, 30 fps, yuv420p, faststart, metadata stripped.
- Music: cinematic--komiku--la-citadelle.mp3 (CC0), music_fit --length 15 --start 78.2 (loudest section, -13.7 dB)
  --end resolve -> one segment 78.2-93.16 s, hit at 13.00 s + 2 s ring-out. listen.py on the bed: 129.2 BPM,
  downbeats 1.86, 3.69, 5.55, 7.41, 9.24, 11.10, 12.96.
- Cuts (plate9.py, shots.json): every 2 beats in the hook (0, 0.93, 1.86, 2.79), then on downbeats 3.69, 5.55, 7.41,
  9.24 (CTA). 60 fps source at 0.5x, 9:16 crop, lanczos + cas=strength=0.5, smp-server-promo grade.
- Structure: hook 0-3.69 music only, title "FIRECRAFT SMP / SEASON 2 IS LIVE" on screen from frame 0; VO line 4
  ("किसी प्लेयर को हराओ, और उसका दिल छीन लो।", Whisper 78%) at 3.84 s, title "KILL A PLAYER / +1 MAX HEART";
  VO line 12 ("अभी अप्लाई करो, और सर्वर जॉइन करो।", 86%) at 9.38 s over the end card (play.firecraft.fun:20011,
  firecraft.fun). English captions for both lines. Takes from the order 4 vo_join (pitch 138 Hz, loudnorm).
- Check: first try failed content_overlap (portrait title at y 1250 over the caption) -> config title_top_portrait 700
  (build.py option added). Check passed; snapshots looked at (8 frames).
- QA: watch.py 450 frames real 30 fps, no gaps; blackdetect 0; -15.7 LUFS, true peak -2.57 dBTP, 0 clipped;
  strings check 0 tool tags. Render 1m18s (-w 3).
