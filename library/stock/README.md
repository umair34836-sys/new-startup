# Stock video / b-roll library (`stock/`)

58 short clips that need **no credit**, 157 MB in total, plus 42 Mixkit links (not downloaded, see below).
H.264 (yuv420p) mp4, no audio, short side at most 1080 px (sources are never upscaled), fps capped at 30, 12 s or less.
Every number in `index.json` (size, fps, duration, resolution) was measured with ffprobe after encoding (2026-10-24).
Search: `python3 library/tools/find_stock.py "rain night"` (add `--vertical` for 9:16, `--all` to include SFX and LUTs).

## Licences (checked 2026-10-24)

| Group | Clips | Proof |
| --- | --- | --- |
| Own overlays/backgrounds (`own-overlays/`) | 37 | Made here with `library/tools/make_overlays.py` (PIL + numpy, fixed seeds). No credit needed. |
| Wikimedia Commons CC0 | 12 | Licence read from each file page's metadata via the Commons API (`extmetadata.LicenseShortName` = CC0). Page URL per clip in `index.json`. |
| Wikimedia Commons public domain (US government: National Park Service, US Forest Service, BLM, etc.) | 4 | Same check (`LicenseShortName` = Public domain). |
| NASA (public domain, **licence doubt**) | 5 | NASA Media Usage Guidelines (https://www.nasa.gov/nasa-brand-center/images-and-media/, read 2026-10-24): NASA content "generally [is] not subject to copyright in the United States", but "NASA should be acknowledged as the source" and commercial use "must not explicitly or implicitly convey NASA's endorsement". Marked `licence_doubt: true`: OK for space/gaming intros, avoid in client ads. |

Not stored here, and why (tested from this server on 2026-10-24):
- **Pexels, Pixabay** (pexels.com, pixabay.com, cdn.pixabay.com): HTTP 403 to this server. Pexels API needs a key (401).
- **Mixkit**: licence fine for client videos (Stock Video Free License: "Attribution is not required", YouTube/social/ads/commercial
  allowed, https://mixkit.co/license/modal/videoFree/), but the Mixkit User Terms (https://mixkit.co/terms/, clause 9) forbid making
  Items available "on a stock or inventory basis" and mass downloading with scripts, and this repo is public. So only links:
  `mixkit-links.json` (42 items whose page says `data-license="videoFree"`; 21 "videoRestricted" items, which forbid
  commercial use, YouTube and ads, were left out). Fetch ONE clip into a project when a video needs it:
  `python3 library/tools/find_stock.py --fetch-mixkit <id> assets/clip.mp4`. Mixkit clause 13: brands/logos inside a clip are not cleared.
  The Mixkit clips were not viewed here; titles and durations are as listed on mixkit.co.
- **Coverr** (coverr.co/license, read 2026-10-24): free, commercial use, "You are not required to add an attribution credit", but
  "Am I allowed to sell or redistribute the videos ...? No" and no AI training/datasets. Download by hand from coverr.co when needed.
- **Mazwai and Videvo uploads on Commons**: CC BY 3.0 (credit required): rejected.
- **Pakistani / South-Asian street footage**: Commons searches for Pakistan, Lahore, Karachi, bazaar, tea and street food
  (2026-10-24) returned only news/CCTV clips or US-government event videos, nothing usable as CC0 b-roll. For desi street
  shots use the owner's own footage or a Mixkit/Coverr clip fetched per project.
- Wikimedia's upload server answers bursts with HTTP 429 ("robot policy"); `commons_dl` style downloads need ~20-60 s gaps.

## Own overlays: how to use them

Black-background clips (light leaks, bokeh, embers, sparks, snow, rain, smoke, dust, glitch, film burn) go on top with
`mix-blend-mode: screen` in HyperFrames, or ffmpeg `blend=all_mode=screen`. `film-grain` is mid-grey: use `overlay`/`soft-light`
at 20-40% opacity. `confetti-greenscreen*` are on pure #00FF00: key with ffmpeg `colorkey=0x00FF00:0.3:0.1`.
`film-burn-transition` (3 s) fills the frame at about 1.4 s (frame checked): put the cut there.
Re-make or change any of them: `python3 library/tools/make_overlays.py <dir> --only <name>` (`--list` for all).
New stock cuts: `python3 library/tools/stock_prep.py in.webm out.mp4 --start S --dur D [--crop WxH+X+Y]`.

## Clips


### city-night (2)

| File | Size | Dur | Licence | What |
| --- | --- | --- | --- | --- |
| `city-night/night-city-lights-rain.mp4` | 1280x720 30fps | 12.0s | CC0 | night city lights seen through a rainy window (720p source) |
| `city-night/bus-arriving-at-night.mp4` | 1920x1080 25fps | 12.0s | CC0 | city bus with headlights arriving at a stop at night, street lights |

### city-traffic (1)

| File | Size | Dur | Licence | What |
| --- | --- | --- | --- | --- |
| `city-traffic/city-traffic-timelapse-aerial.mp4` | 1920x1080 30fps | 12.0s | CC0 | high-angle time-lapse of busy city roads, buses and cars, tower blocks (Causeway Bay) |

### fire (1)

| File | Size | Dur | Licence | What |
| --- | --- | --- | --- | --- |
| `fire/forest-fire-flames.mp4` | 1920x1080 30fps | 11.0s | Public domain | forest fire: tall flames and thick smoke among pine trees |

### nature-sky (3)

| File | Size | Dur | Licence | What |
| --- | --- | --- | --- | --- |
| `nature-sky/clouds-timelapse-blue-sky.mp4` | 1920x1080 25fps | 12.0s | CC0 | white clouds moving fast over a blue sky (time-lapse, camera pointing up) |
| `nature-sky/mountain-cloud-timelapse.mp4` | 1920x1080 30fps | 12.0s | CC0 | lenticular cloud over snowy mountains, blue sky (time-lapse) |
| `nature-sky/desert-tree-clouds-timelapse.mp4` | 1920x1080 29.97fps | 12.01s | Public domain | desert with a Joshua tree, clouds and sun moving (time-lapse) |

### own-abstract (12)

| File | Size | Dur | Licence | What |
| --- | --- | --- | --- | --- |
| `own-overlays/gradient-purple-blue.mp4` | 1920x1080 30fps | 10.0s | own | slow purple/blue/pink gradient loop |
| `own-overlays/gradient-warm.mp4` | 1920x1080 30fps | 10.0s | own | slow orange/red/gold gradient |
| `own-overlays/gradient-teal-green.mp4` | 1920x1080 30fps | 10.0s | own | teal/green/navy gradient (corporate) |
| `own-overlays/gradient-purple-blue-vertical.mp4` | 1080x1920 30fps | 10.0s | own | purple/blue gradient 9:16 |
| `own-overlays/tech-grid.mp4` | 1920x1080 30fps | 10.0s | own | neon perspective grid moving forward (retro/tech/gaming) |
| `own-overlays/particle-network.mp4` | 1920x1080 30fps | 10.0s | own | connected dots network (tech, IT, business) |
| `own-overlays/starfield.mp4` | 1920x1080 30fps | 10.0s | own | twinkling stars drifting (space, night) |
| `own-overlays/gradient-warm-vertical.mp4` | 1080x1920 30fps | 10.0s | own | orange/red/gold gradient 9:16 |
| `own-overlays/gradient-teal-green-vertical.mp4` | 1080x1920 30fps | 10.0s | own | teal/green/navy gradient 9:16 |
| `own-overlays/tech-grid-vertical.mp4` | 1080x1920 30fps | 10.0s | own | neon perspective grid 9:16 |
| `own-overlays/particle-network-vertical.mp4` | 1080x1920 30fps | 10.0s | own | connected dots network 9:16 |
| `own-overlays/starfield-vertical.mp4` | 1080x1920 30fps | 10.0s | own | twinkling stars 9:16 |

### own-celebration (2)

| File | Size | Dur | Licence | What |
| --- | --- | --- | --- | --- |
| `own-overlays/confetti-greenscreen.mp4` | 1920x1080 30fps | 8.0s | own | confetti falling on green screen |
| `own-overlays/confetti-greenscreen-vertical.mp4` | 1080x1920 30fps | 8.0s | own | confetti on green screen 9:16 |

### own-fire (6)

| File | Size | Dur | Licence | What |
| --- | --- | --- | --- | --- |
| `own-overlays/embers-rising.mp4` | 1920x1080 30fps | 10.0s | own | orange embers/sparks rising (fire, gaming, Minecraft promos) |
| `own-overlays/sparks-fountain.mp4` | 1920x1080 30fps | 10.0s | own | spark fountain from bottom centre with gravity |
| `own-overlays/embers-rising-vertical.mp4` | 1080x1920 30fps | 10.0s | own | rising embers 9:16 |
| `own-overlays/smoke-fog.mp4` | 1920x1080 30fps | 10.0s | own | drifting grey fog/smoke on black |
| `own-overlays/sparks-fountain-vertical.mp4` | 1080x1920 30fps | 10.0s | own | spark fountain 9:16 |
| `own-overlays/smoke-fog-vertical.mp4` | 1080x1920 30fps | 10.0s | own | drifting fog/smoke 9:16 |

### own-overlay (12)

| File | Size | Dur | Licence | What |
| --- | --- | --- | --- | --- |
| `own-overlays/light-leak-warm.mp4` | 1920x1080 30fps | 10.0s | own | warm orange/gold light leak drifting |
| `own-overlays/light-leak-pink.mp4` | 1920x1080 30fps | 10.0s | own | pink/magenta light leak |
| `own-overlays/light-leak-blue.mp4` | 1920x1080 30fps | 10.0s | own | cool blue/cyan light leak |
| `own-overlays/light-leak-warm-vertical.mp4` | 1080x1920 30fps | 10.0s | own | warm light leak 9:16 |
| `own-overlays/film-grain.mp4` | 1920x1080 30fps | 6.0s | own | mid-grey animated grain (blend overlay/soft-light, 20-40%) |
| `own-overlays/dust-scratches.mp4` | 1920x1080 30fps | 8.0s | own | old-film dust, hairs and scratches on black |
| `own-overlays/glitch-overlay.mp4` | 1920x1080 30fps | 4.0s | own | RGB glitch bars on black, flickering 4 s |
| `own-overlays/bokeh-warm.mp4` | 1920x1080 30fps | 10.0s | own | warm golden bokeh circles drifting up |
| `own-overlays/bokeh-blue-pink.mp4` | 1920x1080 30fps | 10.0s | own | blue and pink bokeh (night, party) |
| `own-overlays/bokeh-warm-vertical.mp4` | 1080x1920 30fps | 10.0s | own | warm bokeh 9:16 |
| `own-overlays/light-leak-pink-vertical.mp4` | 1080x1920 30fps | 10.0s | own | pink light leak 9:16 |
| `own-overlays/bokeh-blue-pink-vertical.mp4` | 1080x1920 30fps | 10.0s | own | blue and pink bokeh 9:16 |

### own-transition (1)

| File | Size | Dur | Licence | What |
| --- | --- | --- | --- | --- |
| `own-overlays/film-burn-transition.mp4` | 1920x1080 30fps | 3.0s | own | 3 s orange film burn, fills frame at 1.5 s: cut under it |

### own-weather (4)

| File | Size | Dur | Licence | What |
| --- | --- | --- | --- | --- |
| `own-overlays/snow-falling.mp4` | 1920x1080 30fps | 10.0s | own | white snow falling on black |
| `own-overlays/rain-streaks.mp4` | 1920x1080 30fps | 10.0s | own | rain streaks on black |
| `own-overlays/snow-falling-vertical.mp4` | 1080x1920 30fps | 10.0s | own | snow 9:16 |
| `own-overlays/rain-streaks-vertical.mp4` | 1080x1920 30fps | 10.0s | own | rain streaks 9:16 |

### space (5)

| File | Size | Dur | Licence | What |
| --- | --- | --- | --- | --- |
| `space/earth-at-night-rotating.mp4` | 1920x1080 30fps | 12.0s | Public domain (doubt) | animated globe at night with city lights, rotating, black background |
| `space/earth-city-lights-from-space.mp4` | 1920x1080 29fps | 12.0s | Public domain (doubt) | view from orbit: clouds and city lights at night, ends with sunrise glow on the horizon |
| `space/nasa-earth-horizon-iss.mp4` | 1280x720 30fps | 12.03s | Public domain (NASA) (doubt) | Earth's horizon and clouds seen from the International Space Station, part of a docked spacecraft at the edge |
| `space/nasa-earth-clouds-iss.mp4` | 1280x720 30fps | 9.03s | Public domain (NASA) (doubt) | Earth's clouds and sea from the ISS (720p source) |
| `space/nasa-sunrise-from-space.mp4` | 1280x720 30fps | 10.03s | Public domain (NASA) (doubt) | sunrise over Earth's horizon from the ISS: bright sun with lens flare, then a thin blue horizon; ISS parts and a thin vertical line artefact visible in the first ~6 s |

### sunrise-sunset (6)

| File | Size | Dur | Licence | What |
| --- | --- | --- | --- | --- |
| `sunrise-sunset/sunset-golden-clouds.mp4` | 1920x1080 30fps | 12.0s | Public domain | golden sunset light on a sky full of altocumulus clouds, dark horizon |
| `sunrise-sunset/sunset-paris-eiffel-tower.mp4` | 1920x1014 24fps | 12.0s | CC0 | sun setting behind the Eiffel Tower, purple-orange sky over Paris rooftops |
| `sunrise-sunset/sunset-paris-eiffel-tower-vertical.mp4` | 570x1014 24fps | 12.0s | CC0 | 9:16 crop of the Eiffel Tower sunset |
| `sunrise-sunset/sunset-clouds-mountain-timelapse.mp4` | 1920x1080 29.97fps | 12.05s | Public domain | sunset time-lapse, golden clouds racing over dark mountain ridge, sun rays |
| `sunrise-sunset/sunrise-timelapse-orange-sky.mp4` | 1920x1080 25fps | 12.0s | CC0 | sunrise time-lapse: sun rises in an orange sky above a city horizon, plants in foreground |
| `sunrise-sunset/sunset-sun-going-down-timelapse.mp4` | 1920x1080 25fps | 12.0s | CC0 | red sun setting on a flat horizon behind lamp posts (time-lapse) |

### weather (3)

| File | Size | Dur | Licence | What |
| --- | --- | --- | --- | --- |
| `weather/rain-dripping-from-roof.mp4` | 1920x1080 29.693fps | 12.02s | CC0 | rain dripping from a roof edge, copper roofs behind |
| `weather/rain-city-trees.mp4` | 1906x1080 29.917fps | 10.03s | CC0 | rain falling over trees and apartment blocks, grey day |
| `weather/lightning-storm-night.mp4` | 1920x1080 25fps | 12.0s | CC0 | night thunderstorm on the horizon with repeated lightning flashes |

Descriptions of downloaded clips were written after looking at contact sheets of each source (frames every 1.5-3.5 s).
