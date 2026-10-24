# Urdu / Hindi / Pashto songs WITH vocals that need no credit: research Oct 24 2026

Result: 29 public-domain songs saved in `library/music/desi-vocal/` (14 Urdu, 15 Hindi, 0 Pashto). Details, licence
reasoning and per-file measurements: `library/music/desi-vocal/README.md` and its `index.json`.
Earlier research (CC0 instrumentals, FMA, Freesound, Openverse, Pixabay): `free-music-sources.md`.

## The source that works: pre-1923 78 rpm records on archive.org
- One archive.org uploader has put 5,526 Indian 78 rpm items online (count from the advancedsearch API, Oct 24 2026),
  each with the Discogs entry pasted into the description (label, matrix, "Released:" date, notes such as
  "Hindustani song - Female Solo"). Parsing "Released:" gave: 1900s 138, 1910s 266, 1920s 201, later decades the rest,
  1,983 without a date.
- 446 items released 1902-1922 are listed in `data/archive-org-78rpm-hindustani-1902-1922.tsv` (year, id, title) for
  future picks. Everything published before 1923 is PD in the US (MMA) and long expired in India/Pakistan
  (see desi-vocal README for the law links). For a new pick: check the item's "Released:" year, the notes say it is a
  song (not "Instrumental"), and no named lyricist died after 1965 (India life+60).
- Query used: `https://archive.org/advancedsearch.php?q=uploader:<the uploader's address>&fl[]=identifier&fl[]=title&fl[]=description&rows=10000&output=json`
  (the uploader field is on any of the item pages, e.g. https://archive.org/details/d_20230808). Files download
  directly from `https://archive.org/download/<id>/<file>` (no login, fast).
- Other singers in the list worth a look: Peara Saheb (many ghazals 1905-1916), Janki Bai (more 1916 ghazals), Malka
  Jan, Amir Jan Panipat, Mumtaz Jan Delhi ("Gazal Kawali", 1916), Gauhar Jaan "Mere Hazrat Ne Madine Mein Manai Holi"
  (1912; item had no mp3 file).

## Measuring vocals on 100-year-old shellac (what worked / failed)
- Whisper small on the raw 78 found NO speech in many sung records (e.g. Iqbal song: 0 words). After
  `highpass=150, lowpass=4500, afftdn=nf=-25, loudnorm`, it transcribed some Urdu lines (Janki Bai 1916: "ایمان ...").
  Still unreliable; long transcriptions of shellac also loop/hallucinate ("بھائی بھائی ..."), and a full-length pass
  took ~2.5 min per record on this 4-core box.
- Reliable: UVR-MDX-NET Voc FT separation on a 45 s excerpt, then share of 0.5 s frames where the vocal stem is
  > -40 dBFS and within 6 dB of the instrumental stem. Songs 0.49-1.00; sitar control 0.00; shehnai control 0.10.
  Speed: ~1.5 min per 45 s excerpt with mdx_params hop 1024, segment 256, overlap 0.1 (a full 3 min record took
  ~4.5 min). Script logic: scratchpad `sepcheck.py` (re-create from this description).

## Dead ends (Oct 24 2026)
- Wikimedia Commons: 5 Gauhar Jaan files (PD), 4 of them from Gallica/BnF, whose terms require a source credit and a
  paid licence for commercial use -> rejected. Commons API and upload.wikimedia.org returned HTTP 429 to this server.
- FMA "Excavated Shellac" old Indian records: labelled CC BY on FMA -> rejected.
- archive.org `licenseurl:*publicdomain*` Urdu/Pashto audio: mostly lectures, Quran translation, nasheeds; some
  militant nasheed uploads. Not songs we can use.
- Pashto: Berlin Lautarchiv has 1916 Pashto recordings of Pashtun POWs (11 Pashto records per
  https://doi.org/10.25673/92647); no licence shown, POW context, not downloadable as files -> not used.
  1904-05 Pashto Gramophone sides (Sarjool, "Landay", "Charbeta") exist as collector items sold on eBay
  (gripsweat.com archive pages), no online transfer found.
- YouTube: `yt-dlp` subtitle/metadata fetches got HTTP 429 and "Sign in to confirm you're not a bot" (Oct 24 2026).
- Agent-Reach `read` (Jina) paused with UPSTREAM_BROKEN for a while; retry later or use web search snippets.
