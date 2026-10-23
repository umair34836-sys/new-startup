# Website promo music video (made for TalkEmber Studio, Oct 2026)

A song about a website + a HyperFrames video that walks through the REAL site: full-page screenshots scrolling in a
browser frame, a side panel with the site's own headings, the owner's blocky host, Roman Urdu captions synced to the
sung lines, big chorus text, section title cards, intro + end card (URL, WhatsApp, email).

Pipeline (what worked):
1. Research: list pages from the sitemap (`agent-reach read <site>/sitemap.xml`), read every page with Agent-Reach,
   save facts to library/research/<site>.md. Screenshots: if the host is blocked from the container, Firecrawl
   full-page screenshots (1 credit each; owner rule: only when needed and say so). Check crops with a contact sheet.
2. Lyrics `lines.tsv`: Devanagari line <TAB> Roman Urdu caption, with [Verse]/[Chorus] tags; only facts from the site.
3. Song: <= ~19 lines per ACE-Step generation (a 47-line 200 s song skipped half). `gen_parts.py` makes several parts
   with one model load; `ai_song.py` (existing raw.flac is reused) adds the beat ducking.
4. Timing: separate vocals (UVR-MDX-NET Voc FT), Whisper words (`check_part.sh`), then `dp_align.py` (global in-order
   DP; greedy `align.py` is kept only for reference). Mark lines you could not confirm as sung=false: no caption.
5. Join parts at instrumental gaps with 1.5 s acrossfades; build timing.json with slots {id, start, end, sung, roman}
   and "titles" for section cards at each join.
6. `build.py`: edit the S table (line id -> page, scroll y0->y1, panel label/title/chips), CHORUS pages, URL map,
   contact details; `python3 build.py`, `npx hyperframes check`, snapshot ~20 times, then render
   (6 min video, 1920x1080). Background Bash jobs need a long timeout.
