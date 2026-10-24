# Editing skills catalog (index)

560 numbered editing skills, one line each: what / when / how, the ffmpeg or HyperFrames way to do it here, and
the source in brackets. Owner rule: every item carries a reference; nothing is written from guesswork. ffmpeg
commands marked "(ran OK locally)" were run once on a test clip with this container's ffmpeg 6.1.1 on 2026-10-24.
Researched 2026-10-24 via agent-reach (Exa) web search, ffmpeg filter docs and this repo's own tested notes.

Numbers are unique across files, so "skill #212" always means one thing.

| # | File | Groups |
| --- | --- | --- |
| 1-110 | [skills/01-cutting-pacing-story.md](skills/01-cutting-pacing-story.md) | Cutting (cut types, J/L cuts, match cuts, cut on action, eyeline, 180/30 degree rules, trims, filler removal, assembly -> lock), Pacing & rhythm, Story & structure (hooks, open loops, three-act, AIDA/PAS, radio edit, Kuleshov, Murch's rule of six) |
| 111-200 | [skills/02-transitions-camera-speed.md](skills/02-transitions-camera-speed.md) | Transitions (dissolve, fades, flash, whip, zoom-through, light leak, mask wipe, glitch, sound bridge, xfade types), Camera moves & reframing (punch-in, Ken Burns, shake, 16:9 -> 9:16, blurred fill), Speed (slow-mo, optical flow, ramps, time-lapse, freeze, reverse) |
| 201-275 | [skills/03-color-look.md](skills/03-color-look.md) | Correction (order of operations, white balance, scopes, skin-tone line, shot matching, HDR -> SDR), Grading & looks (mood, teal-orange, bleach bypass, film fade, split toning, day-for-night, B&W), Finishing (vignette, grain, halation, sharpening, deband) |
| 276-380 | [skills/04-audio-sfx-music.md](skills/04-audio-sfx-music.md) | Dialogue & cleanup, Mixing & loudness (LUFS per platform, ducking), Sound design & SFX, Music editing (BPM, cut on bar, edit to length, hit points, CC0 sources) |
| 381-455 | [skills/05-captions-motion-compositing.md](skills/05-captions-motion-compositing.md) | Captions & typography (reading speed, word highlight, safe zones, lower thirds), Motion graphics (easing, 12 principles, logo reveal, end screens), Compositing & masking (chroma key, masks, PiP, split screen, blend modes, background removal) |
| 456-560 | [skills/06-cleanup-platform-delivery.md](skills/06-cleanup-platform-delivery.md) | Cleanup & repair (stabilize, low/variable fps, denoise, deflicker, upscale, sync), Platform & retention, Thumbnails, Delivery & export |

## How to search

`grep -n -i "speed ramp" library/research/editing/skills/*.md` finds the item and its source. Where sources
disagree (for example Reels/TikTok loudness -14 vs -16 LUFS, or how often to pattern-interrupt) both views are
listed as separate items with their sources; pick by testing on the real video.

Two colour chains in 03 (bleach-bypass and halation ffmpeg chains) are marked UNVERIFIED: our own combination of documented
filters: they ran, but no guide gives that exact chain, so compare frames before using them.
