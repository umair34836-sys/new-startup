# desi-vocal: Urdu / Hindustani songs WITH vocals, no credit needed (public domain)

29 songs (14 Urdu, 15 Hindi, **0 Pashto**), 96 MB, 160 kbps mono MP3, 2-5.6 min each. All are 78 rpm gramophone
records **published 1905-1919** in British India, transferred and uploaded to the Internet Archive by a record
collector (uploads list: `uploader:` search on archive.org; item pages linked in `index.json`). Collected Oct 24 2026.

Sound: these are 100+ year-old shellac records: mono, surface hiss/crackle, narrow band, singer with harmonium/sarangi/
tabla. Good for vintage, heritage, nostalgia, Iqbal Day, old-Lahore/Delhi moods, shayari reels. Not a modern
studio sound. A light clean-up that worked for listening tests here: `ffmpeg -af "highpass=f=150,lowpass=f=4500,afftdn=nf=-25,loudnorm"`.

## Why each file is safe to use without credit (checked Oct 24 2026)

Each record's release year comes from its archive.org item description (copied from the Discogs entry, label and
matrix numbers included). For a record published in year Y <= 1919:

| Where | Rule (source) | Result |
| --- | --- | --- |
| India | Sound recording: 60 years from the year after publication (Copyright Act 1957 s.27, https://indiankanoon.org/doc/202531/). Literary/musical work: author's life + 60 (s.22); anonymous work: 60 years from publication (s.23) (https://copyright.gov.in/Copyright_Act_1957/chapter_v.html) | recording expired by 1980 at the latest; texts with no named author expired the same way |
| Pakistan | Record: 50 years from publication; literary work: life + 50 (Copyright Ordinance 1962 s.18, s.20; https://www.wipo.int/wipolex/en/text/191444 ; https://en.wikipedia.org/wiki/Copyright_law_of_Pakistan) | expired |
| USA (YouTube/Meta servers) | Recordings first published before 1923: protection ended Dec 31 2021 (Music Modernization Act; https://ask.loc.gov/recorded-sound/faq/313179 ; LoC guide https://www.loc.gov/static/programs/national-recording-preservation-plan/publications-and-reports/documents/Hatch-Goodlatte-Music-Modernization-Act_Guide-for-Sound-Recording-Collectors.pdf) | expired |

Named authors we checked: Muhammad Iqbal (Saare Jahan Se Achha) died 21 Apr 1938
(https://en.wikipedia.org/wiki/Muhammad_Iqbal) -> PD in India since 1999, Pakistan since 1989. Janki Bai (singer and
poet) died 18 May 1934 (https://en.wikipedia.org/wiki/Janki_Bai). Gauhar Jaan died 17 Jan 1930
(https://commons.wikimedia.org/wiki/Category:Gauhar_Jaan). Other lyricists are not named on the records.

Records published 1923-1925 were skipped on purpose (US protection for 1923-1946 recordings is 100 years, so a 1925
record only became PD in the US on Jan 1 2026: too close to call). Records from 1926 on were not considered.

The archive.org items carry NO licence tag and NO usage terms; their public-domain status comes from age alone (above),
not from an uploader's label. The transfer itself is a plain digitisation (no new creative work); this is our reading,
**not checked with a lawyer**.

## Rejected (and why)
- Wikimedia Commons files of Gauhar Jaan from Gallica (BnF, 1904): the recordings are PD, but BnF's Gallica terms
  require the source credit "Source gallica.bnf.fr / BnF" and a paid licence for commercial reuse
  (https://gallica.bnf.fr/edit/conditions-dutilisation-des-contenus-de-gallica ;
  https://www.bnf.fr/fr/faire-une-utilisation-commerciale-dune-reproduction). Needs credit -> rejected.
- "Thumari By Gauhar Jaan Recorded in 1905.ogg" (Commons, PD, "personal collection"): fine in principle, but
  upload.wikimedia.org returned HTTP 429 to this server on Oct 24 2026; archive.org has other 1905-1912 Gauhar Jaan sides.
- FMA "Excavated Shellac" (e.g. Peara Saheb, Gazal, 1910): FMA page shows a CC BY licence -> needs credit -> rejected.
- archive.org modern Urdu/Pashto nasheeds tagged CC0/PD by uploaders who are not shown to be the rights holders, and
  militant "tarana/nasheed" uploads: rejected (doubtful rights; unsuitable content).
- Berlin Lautarchiv 1916 recordings of Pashtun prisoners of war (Pashto songs/tales,
  https://www.lautarchiv.hu-berlin.de/objekte/lautarchiv/7444/): no licence shown, POW context -> not used.
- Pashto: no public-domain or CC0 Pashto SONG with vocals was found (archive.org, Commons, FMA, SoundSafari mirror,
  Openverse in library/research/free-music-sources.md). Gauhar Jaan recorded in "Pushto" per Wikipedia
  (https://en.wikipedia.org/wiki/Gauhar_Jaan) but no such side was found online.

## How "has vocals" was measured (here, Oct 24 2026)
1. Record notes (Discogs text in each item): "Hindustani song - Female Solo", "male solo", "vocal solo", etc.
2. Vocal separation (UVR-MDX-NET Voc FT via audio-separator, 45 s excerpt from 40 s): share of 0.5 s frames whose
   vocal stem is above -40 dBFS and within 6 dB of the instrumental stem. Songs: 0.49-1.00 (median 0.967).
   Controls from the same archive: Imdad Khan sitar solo (1909) **0.00**, Talim Hussain shehnai (1909) **0.10**.
   Lowest songs: Janki Bai "Fana Kaisi Baqa Kaisi" 0.49 and Miss Kasi "Aaya Karo" 0.58 (singing with long
   instrumental passages in that excerpt).
3. Whisper small on denoised 40 s windows at 20/70/110 s (`language='ur'`): it recognised Urdu words on some records
   (e.g. Janki Bai "...ایمان ... تم ہی ہو"), nothing on others. Whisper is unreliable on 1900s shellac noise, so it is
   only supporting evidence. Numbers per file are in `index.json` -> `vocal_check`.

## Files
See `index.json` (file, language, genre, title, singer, release date, label, lyricist note, duration, vocal_check,
archive.org page and source file). Highlights:
- `urdu--peara-saheb--dr-iqbal-s-national-song-saare-jahan-se--1919.mp3`: Iqbal's "Saare Jahan Se Achha", male, 5.6 min.
- `urdu--janki-bai--tumhi-kufr-ho-aur-iman-tumhin-ho--1916.mp3`, `urdu--janki-bai--tumhin-ko-dil-mein-basa-chuke-hain--1916.mp3`: ghazals.
- `urdu--miss-kasi--chahe-bolo-ya-na-bolo--1912.mp3`, `urdu--ratan--kawali-side-a-...--1916.mp3`: qawwali.
- `urdu--keeti-jan-meerut--teri-zaat-paak-hai-ai-khuda--1909.mp3`: hamd-style ghazal.
- `hindi--gauhar-jaan--barse-badarva--1912.mp3` (rain song), `hindi--gauhar-jaan--nahak-laye-gavanva-mora--1906.mp3` (thumri).
- `hindi--miss-jhandi-jhelum--saiyan-ek-jogi-aaya--1909.mp3`: singer from Jhelum (now Pakistan).

Language split: the records say "Hindustani". Files are filed under `urdu--` when the label calls the piece a ghazal,
gazal, kawali or the national song, or the title is in Urdu wording ("Fana Kaisi Baqa Kaisi", "Darde Jigar",
"Deewana Kiya Jaan"), and under `hindi--` for thumri, khayal, bhajan, hori, mand and raag pieces with Braj/Purbi
titles. This is our grouping, not the record's.
