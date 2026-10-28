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
