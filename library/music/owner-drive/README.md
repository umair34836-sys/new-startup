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

The folder also contains other files:
- `sfx/`: 19 Pixabay files, byte-identical (md5) to HyperFrames' bundled media-use SFX, so already available. Also 2 Mixkit vinyl scratches.
- `emoji/noto/`: copied into library/emoji/noto.
- `fonts/tiktoksans/`: copied to library/fonts/TikTokSans-*.
- `brand/logo.jpg` + `banner.jpg`: the owner's channel images. Not committed (no photos rule).
