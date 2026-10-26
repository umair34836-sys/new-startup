# Stock photos via Openverse (CC0 / Public Domain only)

Measured here on 2026-10-26 (PC-security explainer for Indian gamers, 16:9). Photos themselves are NOT in the repo
(repo rule); the per-file proof list lives with the project in the session scratchpad (`projw/assets/img/licence_proof.json`).

## How the API behaves here (measured 2026-10-26)

- `curl -s -G https://api.openverse.org/v1/images/ --data-urlencode q=... --data-urlencode license=cc0,pdm
  --data-urlencode source=wikimedia --data-urlencode page_size=20` -> 200. Python `urllib` with its default
  User-Agent got **403** from the same API: use curl.
- `category=photograph` together with `source=wikimedia` returned 0 results for every query: leave it out.
- Results with `source=flickr` only carried `_b.jpg` URLs (<= 1024 px), so none passed a >= 1280 px filter.
- **Wikimedia downloads**: `upload.wikimedia.org` answered **429** often (both original and thumb URLs). Retrying
  with 10-60 s backoff worked for most files; the standard thumb `.../thumb/<a>/<ab>/<File>/1920px-<File>` gives a
  1920 px JPG. One file (`A_laptop_on_the_wooden_table_(1,_Pixabay).jpg`) gave 404 on the thumb and 429 x6 on the original.
- **Licence check for Wikimedia**: one Commons API call for all files:
  `https://commons.wikimedia.org/w/api.php?action=query&pageids=<id|id|...>&prop=imageinfo&iiprop=extmetadata&iiextmetadatafilter=LicenseShortName|Artist|Credit&format=json`
  (page id = the `curid=` in Openverse's `foreign_landing_url`). All 14 Commons files used showed `CC0`.
- **rawpixel** (Openverse `source=rawpixel`, licence cc0): `images.rawpixel.com/editor_1024/...` (Openverse `url`) =
  1024 px **without** watermark; swapping to `image_1300/...` gives 1300 px but **with a rawpixel watermark** (seen
  2026-10-26): do not use image_1300. rawpixel landing pages answer 403 to curl; `agent-reach read <page>` (exa backend)
  returned the page text "Free public domain CC0 image" for the 5 pages checked.
- `cdn.stocksnap.io` (StockSnap CC0 results) answered 403 to curl; not used.

## Queries that worked (Wikimedia unless noted) -> file picked

| Concept | Query | Picked (creator, licence) | Landing URL |
|---|---|---|---|
| gaming PC setup | `rgb computer` | RGB desktop computer setup with keyboard and monitor (SankalpSasnur, CC0) | https://commons.wikimedia.org/w/index.php?curid=189333268 |
| old computer | `old computer` | Old packard bell pc (Spacekid, CC0) | https://commons.wikimedia.org/w/index.php?curid=30825592 |
| laptop on desk | `computer code` | ComputerProgrammer (Free-Photos from Pixabay, CC0) | https://commons.wikimedia.org/w/index.php?curid=99618818 |
| keyboard | `computer keyboard` | Computer keyboard rainbow (Kurt Kaiser, CC0) | https://commons.wikimedia.org/w/index.php?curid=87687725 |
| hooded hacker | `hacker` | Hacker-3342696 (B_A, CC0) | https://commons.wikimedia.org/w/index.php?curid=85622328 |
| code on screen | `source code` | Html php java source code (Markus Spiske, CC0) | https://commons.wikimedia.org/w/index.php?curid=97404553 |
| server room | `server rack` | Front of server racks at NERSC (Derrick Coetzee, CC0) | https://commons.wikimedia.org/w/index.php?curid=17445617 |
| padlock | `padlock` | Closeup photography of white gate with brass padlock (Bich Tran, CC0) | https://commons.wikimedia.org/w/index.php?curid=89481647 |
| PC fan | `cpu cooler` | CPU air cooler (TheSaturnLover, CC0; portrait, cropped to 16:9) | https://commons.wikimedia.org/w/index.php?curid=178414186 |
| CPU / motherboard | `motherboard` | Pentium II 400 and Slot 1 Motherboard (full shot) (Oligopolism, CC0) | https://commons.wikimedia.org/w/index.php?curid=94433236 |
| network cable | `ethernet cable` | EthernetCableGreen (Raysonho, CC0) | https://commons.wikimedia.org/w/index.php?curid=39564634 |
| warning sign | `danger sign` | High voltage danger sign in English, Hindi, Urdu ... (Syced, CC0) | https://commons.wikimedia.org/w/index.php?curid=178931662 |
| rupee notes | `rupee banknotes` | Indian 50-rupees banknote closeup (Sohel Patel, CC0) | https://commons.wikimedia.org/w/index.php?curid=115874024 |
| virus | `virus microscope` | Microscopic image of bluetongue virus (Dr. Fred Murphy, CDC; CC0 on Commons) | https://commons.wikimedia.org/w/index.php?curid=93452570 |
| envelope (rawpixel, 1024 px) | `envelope` | Pastel envelopes background (CC0) | https://www.rawpixel.com/image/5926999/photo-image-background-paper-public-domain |
| smartphone (rawpixel, 1024 px) | `people phones` | Free woman's hands holding a smart phone (CC0) | https://www.rawpixel.com/image/5918498/image-background-phone-public-domain |
| person on phone (rawpixel, 1024 px) | `people phones` | Free person using phone image (CC0) | https://www.rawpixel.com/image/5915502/image-public-domain-person-free |
| bitcoin (rawpixel, 1024 px) | `bitcoin` | Bitcoin. Free public domain CC0 (physical coins) | https://www.rawpixel.com/image/5974114/bitcoin-free-public-domain-cc0-image |

## Rejected (and why), 2026-10-26
- Backlit keyboard (freestocks) and "Black Computer keyboard": Windows key logo prominent / dull.
- "Hacker typing on a Linux laptop" (Kowalski7cc): identifiable face of a private person.
- "Satchel and laptop": Apple logo on the laptop. "Gaming pc" (Prolete): MSI branding in background.
- "Young people texting on smartphones": identifiable faces. Pegatron motherboard: Cooler Master + Intel logos.
- Rawpixel "Letter envelope" / "Letters envelopes": a private person's handwritten name and address.
- "Green envelope" (Commons): actually Eid greeting cards. "Dark Bitcoin Coins" (rawpixel): 3D render, not a photo.
- No CC0/PD photo found of an email inbox on a screen or of a phone showing a notification. The only email match,
  "Scam-phishing-fraud-email-attack..." (Mohamed Hassan, CC0 per Openverse, https://commons.wikimedia.org/w/index.php?curid=149797851),
  is a flat illustration, not a photo.
