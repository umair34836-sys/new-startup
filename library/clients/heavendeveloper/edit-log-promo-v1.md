# Edit log: Heaven Developer promo v1 (9:16, 30 s, 2026-10-28)

Every decision with its source. Facts on screen/VO: library/clients/heavendeveloper/brief.md (recording frames).

## Triage (video-edit-playbook step 1)
- Input: phone screen recording, 948x2160, 120.06 s (ffprobe). Contact sheets every 2 s and 0.5 s (ffmpeg tile) to
  find the channels and the scrolling moments; full frames read at 10/18/26/30/46/50/62/64/70/74/84/94/114/118 s.
- No usable speech to keep (screen recording of a Discord app); voice = new field VO (owner chose English promo-male).

## Recipe
- decision-guide.md "Screen recording" row (cut dead time; zooms/callouts) + section 26 App/website promo (real
  screens in a device frame, only the client's own facts). Closest repo template:
  library/templates/hosting-promo-reel/build_hostlixo.py (30 s, 7 VO-line scenes, promo-male) -> new template
  library/templates/discord-server-promo/build_heavendeveloper.py.
- Skills: #99 hook in the first 3 s with text on screen at 0 s; #393/#3598 Reels safe zones (main content between
  y 230 and 1340 of 1920); #425 number count-up (start at 0, ~1.3 s, ease-out) for 2,521 members; #3107 device frame
  idea (phone frame built in CSS, real recording playing inside).
- Owner choices (AskUserQuestion 2026-10-28): Limited Edition prices, 9:16 ~30 s, English promo-male, watermark preview.
- HyperFrames lint: no letterSpacing tweens; no two fromTo on one element without immediateRender (fixed).

## Scenes = VO lines
1 hook "NEED A DISCORD BOT? WEBSITE? MINECRAFT PLUGIN?" over the client's banner (blurred) | 2 logo reveal (gold ring,
shine) + "Premium development, delivered." | 3 real #services scroll (recording 45-50 s, status bar cropped) in a phone
frame + 5 service cards | 4 "LIMITED EDITION PERKS / STARTING FROM $4" + 5 starting prices | 5 invite rewards (3 invites =
1 free project, 7 = medium) + real post | 6 count-up 2,521 MEMBERS + real 5/5 review | 7 end card: logo, welcome-post 3
steps, "JOIN ON DISCORD" (no invite link given), "FREE • PAID • PREMIUM PLANS".
Privacy: crops avoid the status bar, server sidebar, the owner's account bar and other members' chats.

## Music (skill music-for-video)
- Type hosting-tech/promo, emotion "confident/premium", 30 s, Reels, client -> --client --vo.
- find_music.py "tech promo confident modern" --length 30 --client --vo: #1 cc0 Loyalty Freak Music "Monarch of the
  Street" (CC0 1.0): 99 BPM, steady grid CV 0.012, full sound by 1.24 s, real ending 222.13 s, LRA ~1.7 LU (steady under
  VO). Also compared: "People Are Spinning" (slow intro till 19 s, fade ending) and the gaming/cinematic list
  ("gaming promo hype": battle/orchestral = wrong for a tech-service brand). listen.py: D minor, dark timbre - fits the
  black/gold "premium" brand.
- music_fit.py --length 30 --end resolve --check: segments [0-27.9] + own ending [222.13-224.14]; join phase error
  22 ms vs 20 ms tracker noise; last 1 s -62.7 dBFS (real decay).

## Voice (skill voice-or-song; library/voices/README.md)
- `vs_tts.py script.txt vo.wav --voice promo-male --lang en --parts parts` (VoxCPM2 clone of the promo-male reference;
  --lang en is new, 2026-10-28). Measured here 2026-10-28: first run downloaded VoxCPM2 (~5 GB) and generated 7 lines
  07:32-07:44; Whisper small (language en) heard all 7 lines word-perfect ("$4", "2500" as digits).
- Raw VO 30.2 s of speech (+0.45 s gaps = 30.6 s): too long for 30 s. Lines 1-6 atempo 1.06, CTA line at 1x, gaps
  0.3 s -> 28.06 s; Whisper re-check of the 1.06x lines: all still word-perfect. VO placed at 0.35 s.

## Mix + QA (measured here 2026-10-28)
- mix_vo_music.py (duck -10 dB, gap 15 LU, -16 LUFS): music_vs_vo_gap_lu 15.0, 0 clipped. SFX lanes: sub-drop at 0,
  whoosh per scene change 0.5, pops 0.35, sparkle on the logo shine/gift, cash-register on $4, impact on the review,
  clicks on the 3 steps, confirm on the JOIN button.
- check passed (0 errors); snapshots at 15 times looked at; fixes: hook word size (edge overflow), review enters at 15%
  of its line (was 45%: on screen only ~1 s), end title 86 px, $4 pop on "four dollars" (68% of the line).
- render -w 3: 1m28s. listen.py: -15.7 LUFS, TP -1.45 dBTP, 0 clipped, voice 0.45-28.42 s, music decays to silence at
  28.77 s (its own ending). watch.py: 30.0 real fps, 900 frames, no black frames; "frozen" = static text holds.
- Preview: watermark.py (tiled "Made by MrCopper804" + PREVIEW tag); clean render kept in the scratchpad for after payment.
- 2026-10-28: owner asked "Give me a final video" -> clean FINAL (no watermark, same render as the preview, 1080x1920, 30.0 s) delivered.
