---
name: stock-sfx-luts
description: Pick no-credit b-roll (stock video), sound effects and colour LUTs from the repo's library for an edit. Use when a video needs filler/establishing shots, overlays (light leak, grain, bokeh, embers, confetti), transitions, whooshes/impacts/UI/cash/phone/game sounds, or a colour look (teal-orange, wedding, B&W, vintage, night, punchy reel), or when the owner asks for "b-roll", "stock", "SFX", "sound effect", "LUT", "grade", "look", "filter".
---

# Stock b-roll, SFX and LUTs (no credit needed)

Everything here was checked on 2026-10-24 (sources and proof in each folder's README and `index.json`).
Search first, then copy what the project needs into its `assets/`:

```bash
python3 library/tools/find_stock.py "sunset clouds"          # b-roll + Mixkit links
python3 library/tools/find_stock.py "embers" --vertical      # 9:16 only
python3 library/tools/find_stock.py --sfx "whoosh"           # sound effects
python3 library/tools/find_stock.py --lut "wedding"          # LUTs
python3 library/tools/find_stock.py --all "fire"             # everything
```

## B-roll (`library/stock/`, see its README)

- What exists: own overlays/backgrounds (light leaks, film grain, dust, film-burn transition, glitch bars, bokeh,
  embers, sparks, snow, rain, smoke, confetti on green, gradients, neon grid, dot network, stars; most also in 9:16),
  Commons CC0/public-domain sky, sunset/sunrise, rain, lightning, city night, traffic time-lapse, fire, nature,
  and NASA space shots.
- NASA clips have `licence_doubt: true` (NASA asks to be acknowledged and forbids implied endorsement): use them in
  space/gaming intros, not in client ads.
- No CC0 Pakistani street footage exists in the library (none found). For office/handshake/payment/delivery/shop
  shots use the Mixkit links (licence: no credit, commercial OK) and fetch ONE clip per need:
  `python3 library/tools/find_stock.py --fetch-mixkit <id> assets/broll/<name>.mp4`. Never bulk-download Mixkit and
  never commit Mixkit/Coverr files to this public repo (their terms forbid re-sharing as stock).
- Overlays on black: CSS `mix-blend-mode: screen` on the overlay `<video>` (inside its own 2D layer, never on a
  preserve-3d container). `film-grain`: `overlay`/`soft-light` at 0.2-0.4 opacity. Green-screen confetti: key in
  ffmpeg first or composite with ffmpeg. Tested 2026-10-24 (frame checked):
  `ffmpeg -i bg.mp4 -i confetti-greenscreen.mp4 -filter_complex "[1:v]colorkey=0x00FF00:0.3:0.1[k];[0:v][k]overlay=shortest=1" out.mp4`
  and screen blend `-filter_complex "[0:v]format=gbrp[a];[1:v]format=gbrp[b];[a][b]blend=all_mode=screen,format=yuv420p"`.
  (The CSS `mix-blend-mode: screen` route in HyperFrames was not render-tested here.)
- `film-burn-transition.mp4` (3 s) fills the frame at about 1.4 s: start it 1.4 s before the cut.
- Every `<video>` needs `data-duration` equal to its scene length (HyperFrames lint).
- Look at the clip before using it: `ffmpeg -ss 3 -i clip.mp4 -frames:v 1 f.jpg` and Read the frame.
- New clip from a long source: `python3 library/tools/stock_prep.py in.webm out.mp4 --start S --dur D [--crop WxH+X+Y]`.
  Library mp4s are blocked by `.gitignore` (personal-video safety net): add licensed stock with `git add -f`.

## Sound effects (`library/sfx/`, 164 files)

- Categories: transition (whooshes, swipes, tape stop, scratch), riser (2/4/8 s, downlifter), impact (boom, punch,
  sub-drop, explosions, heartbeat), glitch, pop, ui, notification (dings, chimes, error), phone (vibrate, ringtone),
  money (cash register, coins), camera, typing, door, vehicle, crowd (applause, shouting), weather (rain, thunder),
  fire, ambience (birds, river, wind, traffic), game (chiptune coin/jump/power-up/level-up, block place/break,
  retro, digital), scifi, magic, foley.
- `index.json` gives `hit_s` (loudest 10 ms) and `length_s`: start the audio at `cut_time - hit_s` so the hit lands on
  the cut. Separate `data-track-index` lanes for overlapping sounds; `data-duration` = `length_s`.
- Levels that worked on earlier edits (root CLAUDE.md): music 1.0, impacts 0.35-0.4, whooshes 0.6-0.8. Quiet
  ambiences (low `rms_dbfs`) need more volume than clicks. Verify with `npx hyperframes audio` or ffmpeg ebur128
  on the render, since Claude cannot listen.
- Own synth effects can be remade or varied: `python3 library/tools/synth_sfx.py <dir> --only <name>`.

## LUTs (`library/luts/`, 32 own-made `.cube`)

- Never read a `.cube` into context. Choose from `previews/<id>.jpg` (before/after) or `previews/_all-luts-*.jpg`.
- Quick choice by job: people/interviews `warm-skin-glow` or `teal-orange-soft`; shop/food reels `pak-reel-punchy`
  or `food-vivid`; offices/products `pak-reel-clean`; weddings `wedding-royal-gold`, `wedding-pastel`,
  `wedding-bright-airy`; drama `moody-desaturated`; gaming/Minecraft `gaming-saturated` or `cyberpunk`;
  memories `bw-soft-matte`, `sepia`, `vintage-70s`; fake night `day-for-night`.
- Test 2-3 on a real frame of the clip first: `python3 library/tools/lut_preview.py frame.jpg library/luts sheet.jpg`.
- ffmpeg: `-vf "lut3d=file=library/luts/<id>.cube"` (blend with the original for less strength, see luts/README).
- HyperFrames: `npx hyperframes media-use resolve --type lut --from library/luts/<id>.cube --project . --json`
  (validated OK for all 32 on hyperframes 0.8.188), then use the returned `.media/luts/lut_NNN.cube` in the
  grading block `{"lut": {"src": "...", "intensity": 0.6-0.9}}` via `media-treatment --grading ... --apply`.
- New or tweaked look: edit `LOOKS` in `library/tools/make_luts.py` and rerun it.
