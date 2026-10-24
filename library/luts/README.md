# Colour LUTs (`luts/`)

32 own-made 3D LUTs (`.cube`, 33x33x33, ~1 MB each, ~31 MB total), written by `library/tools/make_luts.py` with numpy.
No download, so **no licence or credit needed** (our own work). Metadata per LUT: `index.json`.
Never `cat` a `.cube` into an AI context: it is ~36,000 lines of numbers. Look at the previews instead.

Why own LUTs: free LUT packs found online usually carry their own licence terms; making them here avoids any doubt, and
`make_luts.py` rebuilds or tweaks them in about a second (`--list` shows the looks, `--only a,b` remakes some).

## Previews (made here 2026-10-24 with `library/tools/lut_preview.py`)

- `previews/<id>.jpg`: before (left) / after (right) on one frame from the public-domain Wikimedia Commons clip
  "Altocumulus in sunset Galley Common 2 Jan 2022" (https://commons.wikimedia.org/wiki/File:Altocumulus_in_sunset_Galley_Common_2_Jan_2022.webm); its Licensing section, read 2026-10-24, says
  "This work has been released into the public domain by its author, User:Rubbish computer"
  above our own test chart (skin swatches, colours, grey ramp, hue ramp).
- `previews/_all-luts-sunset.jpg`, `previews/_all-luts-chart.jpg`: all looks side by side.
- Other frame: `python3 library/tools/lut_preview.py frame.jpg library/luts out.jpg` (first tile = original).

Observed on the previews (2026-10-24): every look changes the image as its name says; `day-for-night` and
`cold-blue-night` are much darker; `horror-green` turns shadows strongly green; `bw-*`/`sepia` remove colour;
`cyberpunk`, `neon-night-city` and `wedding-pastel` tint whites pink/magenta; `golden-hour`, `vintage-70s` and
`wedding-royal-gold` make whites cream. They were checked on a sky frame and a synthetic chart only, not on real
skin footage: compare 2-3 candidates on a frame of the actual clip before grading a client video.

| Group | LUTs |
| --- | --- |
| Cinematic | teal-orange-cinematic, teal-orange-soft, moody-desaturated, moody-green, bleach-bypass, film-warm-print, film-cool-print, cross-process |
| Skin / people | warm-skin-glow, documentary-natural, dreamy-soft |
| Wedding / events | wedding-pastel, wedding-bright-airy, wedding-royal-gold |
| Pakistani reels / business | pak-reel-punchy, pak-reel-clean, food-vivid, summer-vibrant, golden-hour, autumn-orange |
| Night | cold-blue-night, neon-night-city, day-for-night |
| Black & white / old | bw-classic, bw-high-contrast, bw-soft-matte, sepia, vintage-70s, vintage-matte |
| Gaming / stylised | gaming-saturated, cyberpunk, horror-green |

`film-*-print` are our own approximations, not emulations of any real film stock.

## Apply

ffmpeg (full strength):
```bash
ffmpeg -i in.mp4 -vf "lut3d=file=library/luts/teal-orange-cinematic.cube" -c:a copy out.mp4
```
ffmpeg at partial strength (e.g. 60%), blending graded with original:
```bash
ffmpeg -i in.mp4 -filter_complex "[0:v]split[a][b];[b]lut3d=file=library/luts/warm-skin-glow.cube[g];[a][g]blend=all_expr='A*0.4+B*0.6'" -c:a copy out.mp4
```
HyperFrames: ingest the file into the project (validates it and copies it to `.media/luts/lut_NNN.cube`; tested 2026-10-24
on all 32 with hyperframes 0.8.188, each returned `"ok":true`):
```bash
npx hyperframes media-use resolve --type lut --from library/luts/teal-orange-cinematic.cube --project . --json
```
then reference the returned path in the grading block, in the form shown in `.claude/skills/media-use/references/grading.md`:
`{"intensity": 1, "lut": {"src": ".media/luts/lut_001.cube", "intensity": 0.85}}` via
`npx hyperframes media-treatment --project . --file <scene.html> --selector '#<video-id>' --grading '<json>' --apply`.
(The media-treatment step was not run here; the resolve/ingest step was.)
