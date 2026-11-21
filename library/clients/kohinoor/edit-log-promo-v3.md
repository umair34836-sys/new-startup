# Kohinoor promo v3, "cooler video" style: edit log (2026-11-21)

Owner: "Ek cooler wali video ki trah bhi bana do ussi ka music use ker k".
Builder: library/templates/auto-parts-promo/build_kohinoor_v3.py. Facts: site-data.md.

## MUSIC EXCEPTION (owner's explicit choice)
- The music is the reference TikTok's "original sound" (yt-dlp info: track "original sound - Ubaid Edtiz Ubaid.4d"),
  NOT CC0/PD. Asked the owner with AskUserQuestion (CC0 beat recommended, copyright risk explained); owner answered
  "Same wahi link wali video ka music use kerlo". Used for this video only; the audio stays in the scratchpad, never in
  git; NOT added to library/music. Risk told to the owner: claim/mute on the client's account is possible.
- Reference audio measured -5.5 LUFS integrated; loudnorm I=-14 -> final -14.1 LUFS, peak -1.7 dBFS.

## Reference structure copied (timings only, from the reference itself)
- watch.py content cuts on the reference: 1.37, 2.97, 5.2, 5.93, 6.57, 7.27, 7.83, 8.43, 9.73, 10.33, 11.07, 11.7,
  12.4, 12.97, 13.67, 14.2, 14.87, 15.47 (63/min). beat_events.py beats ~0.645 s apart, strong kicks 0.1, 7.93, 9.53, 13.07.
- 0-1.37 dark intro + white caption bar on top; 1.37-2.97 move toward the object; 2.97-5.2 exploded view held (parts
  drift) and slammed together ~4.9; whip at 5.2; 5.2-15.47 one shot per beat, white bands / black letterbox on some
  shots, red light flicker, glowing name low in frame; 15.47-17.1 black end, glitch-glow name + "edited by".

## Ours
- Exploded hero (owner chose "Piston + rings, bara version"): generic piston illustration with top ring, second ring,
  oil ring, wrist pin, 2 pin clips; each part flies out on the 2.97 cut, drifts, snaps back at 4.75-4.95.
- Beat section: 6 piston shots, each framed differently (scale/rotation/offset), 9 Mixkit shots (same 5 videoFree clips
  as v1, different crops/zooms); white bands on 3 shots, letterbox on 2; facts on the strong-kick shots:
  "Authorized NPR dealer" (9.73), "Nippon Piston Ring / Japan, since 1934" (12.97). Last piston shot: rings pop once.
- End: "Kohinoor" letters glitch in (steps ease + skew), "Authorized NPR dealer", "Edited by MrCopper804".
- No extra SFX (the reference audio already carries its hits).

## Fixes
- Snapshots: glow name and fact text overlapped the piston -> name moved to y 1580, facts to y 300, piston frames lowered.
- blackdetect found 2-4 near-black frames at 9.67 s and 12.87 s: per-clip `-t` lost 1 frame on 4 blurred clips
  (15.33 s instead of 15.47 s), so the footage reached the dark piston bed before the HTML piston appeared. Fix:
  tpad then `-frames:v <exact count> -fps_mode cfr` per clip -> 464 frames = 15.47 s. Remaining black spans are the
  designed black end card (15.5-15.73 letters glitching in) and the final fade (16.87-17.07).

## QA (measured here 2026-11-21)
- Render 35 s. 1080x1920 H.264 High yuv420p 30 fps faststart, 17.1 s; x264/Lavf strings 0; watch.py 30.0 fps,
  0 frozen; -14.1 LUFS. Delivered with SendUserFile.
