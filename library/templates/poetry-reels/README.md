# poetry-reels: silent poetry/quote reels + 4:5 posts (2026-11-21)

`python3 build_poetry_reels.py OUTDIR` (env HANDLE) builds 5 HyperFrames projects (9:16, 10 s): CC0 stock from
library/stock (vertical crop, tint, vignette, slow zoom) + lines revealed word by word (Playfair Italic) + handle.
Render each, then cut a 1080x1350 post from the last frame (`crop=1080:1350:0:285`).
- NO music in the file: the trending song is added in the Instagram app (copyrighted songs are never downloaded).
- Songs paired (trending lists checked 2026-11-21: virlo.ai 7 days to Nov 20 2026; later.com; socialpilot.co):
  Dilruba Dilnasheen (Rito Riba, Siddhant Kaushal; virlo #3, 46 reels/7 days), Inkaar (Azan Ahmad, new release on IG),
  Vintage November (Peaceful Reveries; virlo #13), November Rain (Guns N' Roses; socialpilot Nov), Coming Up Roses
  (Harry Styles; later.com "I feel like I haven't done much this year", Nov 20).
- Measured: 5 renders 10.0 s, 5.6-7.9 MB, yuv420p. A 4-word line at 84 px wraps: keep lines <= ~22 characters.
