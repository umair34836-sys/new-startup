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
Every montage bar plays a real ~1.7 s clip of a delivered video (not a thumbnail), with the client name, a red type
pill and an "07 / 17" counter, so the reel shows the work itself. Then a 2-bar wall of 6 vertical clips with
"N VIDEOS • M BRANDS" (counted from the config, so it is always true), then the contact end card.

Timeline (BAR = 240 / bpm): hello 0 → drop-2 bars, "Want a video EDITOR?" → drop, one clip per bar from the drop,
wall 2 bars, end card 4 bars + 1 s. 17 clips at 140 BPM = 47.3 s.

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
- Music: library/music/cc0 "High Technologic Beat Explosion" (Loyalty Freak Music, CC0) cut from 46.75 s: listen.py
  140.0 BPM, downbeats 1.71 + n x 1.714 s, so the drop/montage starts at 6.85 s.
- `hyperframes check` warned `gsap_repeated_fromto_without_baseline` for a card that had an entry fromTo plus a
  fromTo scale drift; the drift is a plain `tl.to` now.
- Choosing clips: per-second ffmpeg tile sheets (`fps=1,scale=160:-2,drawtext t,tile=12xN`) were much faster than
  watch.py (2-4 min per video here) for finding each video's strongest second (a price slam, a list building up).
  Watermarked previews (tiled "Made by MrCopper804") and duplicate drafts were left out.
