# Stock video, sound effects and LUTs without credit: sources checked Oct 24 2026

Goal: b-roll, SFX and colour LUTs that need NO credit and are allowed in client videos. Results live in
`library/stock/`, `library/sfx/`, `library/luts/` (each has README + index.json). Everything below was tested or read
from this cloud server on 2026-10-24 unless marked otherwise.

## Reachability from this server (curl with a browser User-Agent, 2026-10-24)
- 200: mixkit.co, assets.mixkit.co, coverr.co, commons.wikimedia.org (API), images-api.nasa.gov, images-assets.nasa.gov,
  archive.org, kenney.nl, opengameart.org, vidsplay.com.
- 403: pexels.com, pixabay.com, cdn.pixabay.com, freesound.org, cdn.freesound.org. api.pexels.com: 401 (needs a key).
- upload.wikimedia.org: works but answers bursts with HTTP 429 ("robot policy" / "too many requests"); downloads
  needed 20-60 s gaps and retries. The Commons API also returns 429 in bursts (with back-off, about one search query per 2 minutes).

## Licences read (2026-10-24)
- **Kenney** (kenney.nl/support): "all game assets on the asset pages are public domain licensed (CC0)",
  "Attribution is not required". Each audio pack's License.txt says CC0 1.0. 7 audio packs (~520 sounds) downloaded.
- **OpenGameArt**: per page licence field. Kept only pages listing CC0 alone; pages listing CC0 plus CC BY/BY-SA were
  skipped (e.g. wierd-whooshes, fireworks-with-applause-happy-people, rain-on-window-loop, video-game-cheerful-ending).
  The "well-done" page is listed CC0 but its file is named "Well Done CCBY3": skipped.
  Search URL: `https://opengameart.org/art-search-advanced?keys=<q>&field_art_type_tid[]=13&field_art_licenses_tid[]=4`
  (13 = sound effect, 4 = CC0).
- **Mixkit** video free licence (https://mixkit.co/license/modal/videoFree/): commercial, YouTube, social, ads allowed,
  "Attribution is not required". Restricted licence (`/license/modal/videoRestricted/`): personal only, no YouTube,
  no ads, no company posts. Each item page carries `data-license="videoFree"` or `"videoRestricted"`.
  SFX free licence (`/license/modal/sfxFree/`): "You can't redistribute the Item on its own, as stock".
  User Terms (https://mixkit.co/terms/, revised Oct 2 2025) clause 9: no making Items available "on a stock or inventory
  basis", no "scripts or bots to mass download"; clause 13: brands/trademarks inside items are not cleared.
  File URLs: `https://assets.mixkit.co/videos/<id>/<id>-720.mp4` (and `-1080.mp4`, tested 200 for id 918, 34 MB).
  -> kept as a link list only (`library/stock/mixkit-links.json`, 42 videoFree items), since this repo is public.
- **Coverr** (https://coverr.co/license): free commercial use, attribution not required; no redistribution/resale,
  no AI training or datasets. Not stored.
- **NASA** (https://www.nasa.gov/nasa-brand-center/images-and-media/, read via agent-reach): content "generally [is] not
  subject to copyright in the United States"; "NASA should be acknowledged as the source"; commercial use "must not
  explicitly or implicitly convey NASA's endorsement"; NASA logos/employees in promotional content may need clearance.
  -> NASA clips are marked `licence_doubt` in the stock index.
- **Wikimedia Commons**: licence per file from the API (`prop=videoinfo&viprop=extmetadata`, `LicenseShortName`).
  Categories "Videos from Mazwai" and "Videos from Videvo" are CC BY 3.0 (credit) -> rejected.
  "Category:Videos from Pixabay" had 15 CC0 files.
- **Sonniss GDC bundles**: not checked in detail (site redirected); not used.

## What Commons has and lacks (searches 2026-10-24)
- Good CC0/PD material: cloud and sunset time-lapses, rain, lightning, city traffic time-lapse, night city, wildfire
  (US Forest Service), NASA/NOAA space and satellite clips, waterfalls, ocean waves, snow, birds, 1906 India street film.
- Not found as usable CC0 b-roll: Pakistani/Lahore/Karachi street scenes (only news/CCTV), office, handshake,
  payments, delivery, tea pouring. Many "public domain" hits are US government news, police or CCTV videos: not b-roll.
- Search tip: `generator=search&gsrsearch=filetype:video <words>&gsrnamespace=6` plus `viprop=derivatives` gives
  ready 1080p/720p VP9 transcodes (much smaller than originals).

## HyperFrames LUT ingest (tested)
`npx hyperframes media-use resolve --type lut --from <file.cube> --project . --json` returned `"ok":true` for all 32
own LUTs (hyperframes 0.8.188) and copied each to `.media/luts/lut_NNN.cube`.
