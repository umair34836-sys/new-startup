# Owner's Drive music folder (files NOT in this repo)

Folder: https://drive.google.com/drive/folders/1w3h8SHEG8Ixiqwk0I_7jI-1HVU5ZBXsn. The owner shared it on 2026-10-26.
It has 72 files: music, SFX, emoji, a font, and the owner's own logo and banner.

The audio stays on Drive because this repo is public:
- YouTube Audio Library terms: "solely for use by you in videos"; no standalone distribution.
- Mixkit User Terms: no redistribution "on its own, as stock".
- See library/research/free-music-sources.md and library/sfx/README.md.

Fetch per job into the scratchpad. gdown 6.4.2 is in setup-all heavy.

    /home/user/tools/venv/bin/gdown --folder "https://drive.google.com/drive/folders/1w3h8SHEG8Ixiqwk0I_7jI-1HVU5ZBXsn" -O <scratchpad>/owner-drive

The licence column is taken from the folder's own `music/CREDITS.md` (written by an earlier session on 2026-10-19/21).
Per that file:
- **YT-ALib** = YouTube Audio Library "Attribution not required". Use in YOUTUBE videos only. Per the secondary sources in free-music-sources.md, other platforms are not covered.
- **Mixkit** = Mixkit Free License (https://mixkit.co/license/modal/musicFree/). Any web/social platform, commercial use, no credit. OK for client reels.
- **Eleven** = generated with the owner's ElevenLabs plan ("Music commercial use"). This is the owner's channel intro sting.

The numbers were measured here on 2026-10-26 with `listen.py <file> --no-words`:
- BPM = essentia/librosa. "alt" = the half/double-time alternative, where listen.py gave one.
- LUFS = EBU R128 integrated.
- Key = Krumhansl profile.

| Folder | Track | Licence | Length s | BPM (alt) | LUFS | Key |
|---|---|---|---|---|---|---|
| lofi | No Rush - Dyalla | YT-ALib | 162 | 172.3 (86.1) | -10.9 | G major |
| lofi | On The Flip - The Grey Room _ Density & Time | YT-ALib | 183 | 84.0 | -10.1 | D major |
| lofi | Twinkle - The Grey Room _ Density & Time | YT-ALib | 194 | 172.3 (86.1) | -10.0 | A minor |
| mixkit | Better Times are Coming - Alejandro Magana | Mixkit | 100 | 119.9 | -12.3 | B major |
| mixkit | Comical - Ahjay Stelino | Mixkit | 114 | 140.0 | -11.4 | G major |
| mixkit | Deep Urban - Eugenio Mininni | Mixkit | 289 | 123.9 | -9.4 | A minor |
| mixkit | Digital Clouds - Alejandro Magana | Mixkit | 101 | 129.0 | -13.2 | C minor |
| mixkit | Focus on Yourself - Eugenio Mininni | Mixkit | 286 | 113.9 | -11.8 | E minor |
| mixkit | Gummies - Michael Ramir C | Mixkit | 100 | 120.0 | -14.2 | A major |
| mixkit | Hip Hop 02 - Lily J | Mixkit | 115 | 96.9 | -12.0 | Eb minor |
| mixkit | Natures Fabric - Ahjay Stelino | Mixkit | 101 | 139.9 | -12.4 | A minor |
| mixkit | Slow Trail - Ahjay Stelino | Mixkit | 103 | 136.0 (68.0) | -8.8 | A minor |
| mixkit | Uplifting Bass - Lily J | Mixkit | 96 | 133.8 | -11.8 | Eb major |
| suspense | Apocalyptic Echoes - Jimena Contreras | YT-ALib | 164 | 123.0 (61.5) | -11.7 | C minor |
| suspense | Cinematic Symphony of Steel - Jimena Contreras | YT-ALib | 186 | 117.5 (234.9) | -11.9 | C minor |
| suspense | Deep Space Sector 9 - Ezra Lipp | YT-ALib | 104 | 107.7 (215.3) | -12.9 | F# minor |
| upbeat | After Sunset - Alex Jones _ Xander Jones | YT-ALib | 160 | 90.0 | -14.4 | C major |
| upbeat | Club Love - Everet Almond | YT-ALib | 183 | 105.0 | -9.1 | Eb major |
| upbeat | Lion - Dyalla | YT-ALib | 183 | 123.0 (61.5) | -10.5 | D major |
| upbeat | mrcopper_intro_5s_eleven | Eleven | 5 | 129.2 (64.6) | -13.1 | Eb minor |
| upbeat | mrcopper_intro_eleven_full | Eleven | 11 | 128.5 | -11.6 | Ab major |
| assets/music/promo | 360 No Scope - The Soundlings | YT-ALib | 187 | 120.0 | -9.7 | C major |
| assets/music/promo | Fusion of Dhol - Aakash Gandhi | YT-ALib | 181 | 89.1 (178.2) | -18.1 | C# minor |
| music/desi | Crash & Burn - Aakash Gandhi | YT-ALib | 127 | 98.1 | -14.0 | F minor |
| music/desi | Shake It - Aakash Gandhi | YT-ALib | 112 | 119.9 | -14.0 | G minor |
| music/desi | The Mumbai Beat - Hanu Dixit | YT-ALib | 116 | 86.7 | -8.7 | C minor |
| music/emotional | Days Are Long - Silent Partner | YT-ALib | 187 | 143.6 (71.8) | -7.9 | E major |
| music/emotional | Renunciation - Asher Fulero | YT-ALib | 222 | 136.0 (68.0) | -17.4 | F major |
| music/emotional | Restless Heart - Jimena Contreras | YT-ALib | 96 | 152.0 (76.0) | -14.3 | D minor |
| music/funny | Demented 90s Cartoon Theme - Rod Kim | YT-ALib | 91 | 111.9 | -10.3 | F# major |
| music/funny | Pouncin and Bouncin - The Soundlings | YT-ALib | 116 | 118.2 | -11.5 | F minor |
| music/funny | Silly Snickerdoodle - Joel Cummins | YT-ALib | 124 | 99.0 | -13.1 | C major |
| music/happy | Dove Love - Quincas Moreira | YT-ALib | 175 | 101.0 | -12.0 | C major |
| music/happy | Hopping Trains - Nathan Moore | YT-ALib | 118 | 137.0 | -11.8 | E major |
| music/happy | Island Summer Breeze - Coyote Hearing | YT-ALib | 129 | 112.0 | -22.4 | C major |
| music/sting | Detour (Sting) - Gunnar Olsen | YT-ALib | 8 | 100.9 | -9.4 | Bb minor |
| music/sting | Dizzy (Sting) - Max Surla_Media Right Productions | YT-ALib | 6 | 125.2 | -9.6 | A major |
| music/sting | Dub Hub (Sting) - Jimmy Fontanez_Media Right Productions | YT-ALib | 6 | 152.5 | -8.1 | F major |
| music/suspense | Battle Of The Beast - The Soundings | YT-ALib | 128 | 120.0 | -8.4 | E minor |
| music/suspense | Challenge Accepted - The Soundings | YT-ALib | 155 | 140.0 | -10.3 | D minor |
| music/suspense | Risen - Density & Time | YT-ALib | 186 | 116.0 | -12.4 | C minor |
| music/tutorial | All For You - Anno Domini Beats | YT-ALib | 134 | 115.8 | -10.1 | F major |
| music/tutorial | Kicking It - Dyalla | YT-ALib | 157 | 88.0 | -12.9 | G minor |
| music/tutorial | Misdirection - The Grey Room _ Density & Time | YT-ALib | 184 | 120.0 | -11.7 | C major |
| music/upbeat | All The Smoke - The Soundlings | YT-ALib | 144 | 128.4 | -10.4 | B minor |
| music/upbeat | Euphoria - Dyalla | YT-ALib | 134 | 124.9 | -13.6 | D minor |
| music/upbeat | No Combat - Telecasted | YT-ALib | 156 | 95.0 | -11.6 | G minor |

Notes on the two `assets/music/promo/` tracks (added by the owner 2026-10-26):
- The folder's `assets/music/CREDITS.md` gives 120 BPM for both, "measured on the kick/dhol band". For Fusion of Dhol, listen.py's full-mix tempo (89.1, alt 178.2) disagrees.
  Check the beat grid before cutting to it.
- Fusion of Dhol is quiet (-18.1 LUFS): raise its volume against VO more than the other tracks.

Since 2026-10-26 the folder also has an `assets/` subfolder. Apart from `assets/music/promo/` and its CREDITS.md, every file in it is byte-identical (md5) to the root copies.
`assets/music/` has no `upbeat/` YT tracks (After Sunset, Club Love, Lion): those are only in the root `music/upbeat/`.

The 24 `music/{tutorial,funny,desi,upbeat,suspense,emotional,happy,sting}/` rows were added by the owner on 2026-10-26.
They came from the download list given in chat. Per the folder's `music/CREDITS.md` ("Library expansion"), each one was
"checked 'Attribution not required' / 'YouTube Audio Library License'", so they are for YouTube use only.
Where CREDITS.md (kick-band estimate) and listen.py (full mix) disagree on BPM, check the beat grid before cutting:
All For You (~96 vs 115.8), The Mumbai Beat (~112/136 vs 86.7), No Combat (~126 vs 95.0), Misdirection (~117 vs 120.0).
Island Summer Breeze is very quiet (-22.4 LUFS) and Renunciation is quiet (-17.4 LUFS): normalise them before mixing.
The root `music/promo/` and `assets/music/upbeat/` are byte-identical copies of tracks listed above (md5, 2026-10-26).

The folder also contains other files:
- `sfx/`: 19 Pixabay files, byte-identical (md5) to HyperFrames' bundled media-use SFX, so already available. Also 2 Mixkit vinyl scratches.
- `emoji/noto/`: copied into library/emoji/noto.
- `fonts/tiktoksans/`: copied to library/fonts/TikTokSans-*.
- `brand/logo.jpg` + `banner.jpg`: the owner's channel images. Not committed (no photos rule).
