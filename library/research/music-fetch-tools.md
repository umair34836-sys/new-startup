# Tools that fetch songs / music: GitHub search 2026-10-27

The owner asked on 2026-10-27: "GitHub per tools dondhoo for songs or musics jo tumhe songs and musics la ker dingay and
unko install kerdo". Rules that decide what may be installed (CLAUDE.md):
- Never copyrighted songs.
- Client work only CC0 / public domain.
- No CC BY music, because it needs credit.

How the search was done:
- `agent-reach web search` (Exa) on 2026-10-27. Exa answered UPSTREAM_BROKEN after 3 searches, so the rest used WebSearch.
- Star counts come from those search results. They were not checked on github.com, which returns 403 to this session.

## Installed

| Tool | What it does | Facts | Status |
|---|---|---|---|
| `ia` (jjjake/internetarchive) | Official archive.org command-line tool + Python library: search, download | GitHub page via Exa 2026-10-27: 1,928 stars, AGPL-3.0. `pip install internetarchive` gave version 5.12.1 (measured here 2026-10-27). `ia search 'collection:georgeblood AND subject:"Hindustani"' --itemlist` returned Great 78 Project item ids (measured here 2026-10-27). | Installed. Added to setup-all light. |
| `library/tools/fetch_free_music.py` (ours) | FMA search with the public-domain filter. It re-reads every track page, keeps only CC0 / PD-mark licence links, and saves the file into library/music/cc0 with index + README rows. | Test 2026-10-27: `"lofi" --n 2` fetched 2 HoliznaCC0 tracks (CC0 1.0 on the page). music_catalogue.py measured them (82.0 / 161.5 BPM). find_music.py ranked "first-snow" 5th for "tutorial calm background --vo --client". | Made here. |

Why we wrote our own fetcher: no maintained GitHub tool downloads FMA public-domain music with a per-page licence check.
- drzhn/FreeMusicArchive_downloader has 5 stars (Exa 2026-10-27).
- The fetcher's logic is the method in free-music-sources.md section "FMA directly".

## Rejected (and why)

| Tool | Why not |
|---|---|
| CharlesPikachu/musicdl (~1,155-1,206 stars per ecosyste.ms snapshots, WebSearch 2026-10-27) | Downloads from commercial platforms (QQ Music, Netease, Kugou, Kuwo, Migu, JOOX; ossinsight also lists Spotify, Apple Music, YouTube). Those are copyrighted songs, against the owner's rule. |
| spotDL and other YouTube/Spotify rippers | Copyrighted songs. Not searched further. |
| dohliam/ccmixter-download, jtara1/ccmixter_song_downloader | ccMixter licences were not checked here. Its own issue #1 is "Download and streaming produces 403 Forbidden" (Exa 2026-10-27). Re-check before use; CC BY tracks would be rejected anyway. |
| Openverse clients (openverse-api-client on PyPI, LGPL-3.0; a Go openverse-cli, Apache-2.0) | CC0 audio on Openverse is almost all Freesound. Measured here 2026-10-27: 20 of 20 "piano" CC0 results were Freesound. cdn.freesound.org answered 403 with an honest User-Agent (same as on 2026-10-24). The rest is Wikimedia Commons, which mostly holds word-pronunciation clips and answered 429 to a file request on 2026-10-27. |

## AI song makers found (not installed: the owner wants music made by others; make our own only when asked)

Licences below are from WebSearch 2026-10-27 (READMEs / HF model cards).

| Model | Licence | Notes |
|---|---|---|
| YuE (m-a-p) | Apache-2.0 since Jan 2025 | The maintainers ask for credit "YuE by HKUST/M-A-P". |
| DiffRhythm (ASLP-Lab) | Apache-2.0 since 2025-03-07 | Full-length songs. |
| DiffRhythm 2 | Apache-2.0 for code + weights (HF card) | |
| SongBloom | not checked | |

CPU speed and disk need for these were not measured here. ACE-Step 1.5 (MIT) is already set up on demand: `setup-all.sh acestep`.
