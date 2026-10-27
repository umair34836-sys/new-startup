# editor-portfolio (video-editor showreel, 16:9 + 9:16 from one config)

Made for the owner (MrCopper804) on 2026-10-27: "is video ki trah mere lie bhi ek portfolio video bana do ... kis kis
client k lie videos banayi hai sub ki highlights do". Built from his reference TikTok and his own delivered videos.

## Reference (looked at here 2026-10-27)
TikTok @abuhuraira__008 video 7679106664250789142 (15.3 s, 1024x576). yt-dlp could not download it ("Unexpected
response"), so frames were read in Playwright by seeking the page's `<video>` every 0.5 s with overlays hidden
(`scratchpad/scripts/tt3.js` pattern: element screenshot after `seeked`). What it shows:
- 0-1.5 s: round avatar, "Hi , IM <NAME>" typed, then red tag "Available For Freelance Work", "Video editor |
  Motion graphics", red button "Views My Work >".
- 2-4.5 s: "Want a videos EDITOR" word by word, EDITOR in a red rounded box.
- 4.5-9 s: dot grows into a circle mask, intro again with all details.
- 10-15 s: rows of 3 thumbnails flip/slide in, red "CONTACT ME" pill, "For all Type Editing" typed.
- Look: light grey paper with dust specks/scratches and a vignette, blurred dark tape crosses in the top-left and
  bottom-right corners, red ~#f0193f accents, black geometric sans.

## What this template does differently
The montage plays real clips of delivered videos (not thumbnails), ONE SECTION PER BRAND: the brand name lands once
with "CLIENT 03 / 07" and "6 videos", then its videos follow, vertical ones side by side (3 per bar in 16:9, 2 in
9:16), each horizontal video on its own bar, a type caption under every card. Then a 2-bar wall of 6 vertical clips
with "N VIDEOS • M BRANDS" (counted from the config), then the contact end card.
v1 (one clip per bar, brands interleaved) got owner feedback 2026-10-27: "ek brand ka baar baar repeat hona" (brands
kept coming back), "sound effect right place per nahi lage", "background music judge nahi raha". v2 fixed all three.

Timeline (BAR = 240 / bpm, bt(n) = drop + n beats): hello 0 → bt(-6), "Want a video EDITOR?" → drop, one group per
bar from the drop, wall 2 bars, end card 3 bars + 1 s. 17 clips / 7 brands at 110 BPM: 13 bars 16:9 (47.1 s),
14 bars 9:16 (49.3 s).

## SFX placement (v2)
Every SFX is placed by its measured PEAK (numpy RMS envelope, 10 ms window, measured here 2026-10-27) so the peak
sits on the beat where the visual lands: whoosh-fast-0.3s 0.17 s, whoosh-up-0.6s 0.30 s, swish-1 0.04 s, sparkle
0.45 s, impact-punch / sub-drop / pop-high / pluck / click-1 ~0 s. typing-keyboard-fast is an 8 s loop: trimmed with
data-duration to the 0.9 s of typing (v1 let it run under the next scene). Cards move across the downbeat (0.15 s
either side) with the whoosh peak on it; a new brand adds impact-punch on that downbeat, its "N videos" pill a pop on
the next beat; contact rows pluck on consecutive beats; tweens start ~0.06-0.12 s early so the pop/slam reads on the
beat.

## Use
```
mkdir -p PROJECT/assets/{vendor,fonts,sfx,music,characters,img}
cp library/vendor/gsap-3.14.2.min.js PROJECT/assets/vendor/
cp library/fonts/{Poppins-SemiBold,Poppins-Bold,Poppins-ExtraBold,Anton-Regular}.ttf PROJECT/assets/fonts/
# sfx used: transition/whoosh-fast-0.3s, transition/swish-1, transition/whoosh-up-0.6s, impact/impact-punch,
# impact/sub-drop, pop/pop-high, ui/pluck, ui/click-1, typing/typing-keyboard-fast, magic/sparkle (flat in assets/sfx)
# music: cut so a downbeat (the drop) lands ~6.9 s in, then listen.py for bpm + drop
cp video/hyperframes.json PROJECT/   # plus a meta.json / package.json like video/
python3 library/templates/editor-portfolio/build.py CONFIG.json --format 16x9 --out PROJECT
npx hyperframes check; npx hyperframes snapshot --at 0,2.6,5.7,7.6,17.9,37.3,44.5; npx hyperframes render -q high -w 3
```
CONFIG: see `example-config.json` (name, role, tag, cta_sub, bpm, drop, contacts, clips [{src, start, client, type}],
grid = 6 indices of VERTICAL clips). `--no-clips` reuses cut clips when only the layout changed.

Avatar (`assets/img/avatar.png`): the owner's skin waving, made with blocky_character.py in a 600x600 mini project:
`--scale 17 --width 600 --height 600 --x 300 --y 650 --turn -18 --moves '[[0,"wave"]]'` on a
`radial-gradient(circle at 50% 35%, #3a3a3a, #0d0d0d 70%)` root, `hyperframes snapshot --at 0.6`.

## Measured / learned here (2026-10-27)
- A live blocky_character sub-composition inside a `border-radius:50%; overflow:hidden` avatar escaped the clip and
  stayed on screen after its scene's `visibility:hidden` window (snapshot at 5.7 s and 7.6 s still showed it): use a
  still image of the character for round avatars.
- Music v1: "High Technologic Beat Explosion" (cut from 46.75 s, 140 BPM): owner said it did not suit
  ("judge nahi raha"); listen.py called it tense/driving, dark, -17.2 LUFS with a quiet intro section.
- Music v2: library/music/cc0 "People are spinning" (Loyalty Freak Music, CC0): listen.py 110.0 BPM, CV 0.013,
  bright/upbeat; sections intro 0-8.71, build 8.71-17.44, drop 17.44 (exactly 4 bars after 8.71). Cut from 10.59 s so
  the drop lands at 6.85 s; in the cut, detected beats sit 15-25 ms before drop + n x 0.5455 s up to 46 s.
- `hyperframes check` warned `gsap_repeated_fromto_without_baseline` for a card that had an entry fromTo plus a
  fromTo scale drift; the drift is a plain `tl.to` now.
- Choosing clips: per-second ffmpeg tile sheets (`fps=1,scale=160:-2,drawtext t,tile=12xN`) were much faster than
  watch.py (2-4 min per video here) for finding each video's strongest second (a price slam, a list building up).
  Watermarked previews (tiled "Made by MrCopper804") and duplicate drafts were left out.

## v3 music + hook (owner feedback 2026-10-27: "music taste bad", "music me jan dallo ... hook bana rahay")
- Two picks from library/music/cc0 were rejected. v3 uses Mixkit "Uplifting Bass" (Lily J) from the owner's Drive
  (library/music/owner-drive: Mixkit licence = any platform, no credit; the file is not in this repo).
  listen.py: 133.8 BPM, CV 0.023, bright/upbeat; energy step at 29.605 s; bar hits at 29.605 + n x 1.7935 s
  (38.59, 40.38, 43.96, 52.92, 54.71, 65.46 s all matched). Cut from 22.755 s so that step is the montage drop (6.85 s);
  in the cut, detected beats stay within ~30 ms of drop + n x 0.4484 s up to 38 s.
- Hook gaps (config "hook_gaps", default on): the music is muted for the beat before the drop and the half beat
  before the wall (20 ms ramps, music_hook.mp3); riser-2s (peak 1.68 s) peaks on the drop / wall, impact-boom +
  sub-drop on the drop. Measured in the cut: -180 dB inside the gaps, -4.4 dB right after the drop.
- When unsure what music the owner likes, send 4-6 loudness-matched 20 s samples (loudnorm -14) and let them pick.
