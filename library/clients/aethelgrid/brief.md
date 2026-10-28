# AethelGrid (client) - brief

- Relayed by the owner 2026-10-28 (verbatim): "so we want a 60 sec video showing the core features of our host
  including site and panel"
- Site: https://aethelgrid.cloud/ - Panel: https://gp.aethelgrid.cloud/
- Job: ~60 s video, core features of the host, from BOTH the website and the panel.
- Site crawled 2026-10-28 (facts: site-data.md). Panel = public login page only (Pterodactyl + Blueprint,
  "Powered by Nebula" theme); inside of the panel NOT seen.
- OWNER CHOICES 2026-10-28: panel = show only the public login page + the site's own panel image (experience.png);
  9:16; Hindi VO + CC0 music; watermarked PREVIEW until payment. Script (13 lines) approved 2026-10-28
  (template library/templates/site-panel-reel/: flow_aethelgrid.js records, build_aethelgrid.py builds).
- Voice: first run used `promo-male`; stopped after 4 lines when the main session relayed the owner's ban on it
  (2026-10-28, commit 633bf73). Owner (2026-10-28): "simple mat bejho khod as a pro editor chose kroo" -> chosen `explainer-pro`: README use
  "explainers, corporate, product walk-throughs" (= this site+panel features video, decision-guide #10/#26); 2-line sample
  vs news-anchor, Whisper small 50% both (spelling-level misses, same words), explainer-pro 6.00 s vs 7.24 s (fits 60 s).
- Music: CC0 "People Are Spinning" (Loyalty Freak Music): listen.py 110 BPM, G major, bright/upbeat, drop/full sound
  from 17.4 s. Rejected "Monarch of the Street" (top find_music score, but listen.py: D minor, sad/reflective).
- New client: ask before sending a clean file (watermark rule for unpaid clients).
- Never create an account, log in with guessed data, submit a form or press "Order Now" on this site.

## Re-capture (screenshots are never committed)
- `node site/tools/crawl.js urls.txt <scratch>/crawl` (urls.txt = https://aethelgrid.cloud/ + https://gp.aethelgrid.cloud/)
- `node site/tools/explore.js <scratch>/explore`: clicks menus, FAQ, location/processor/currency toggles, panel tabs
  (never Order Now / Get Started / Copy). /vps can miss `networkidle` (30 s timeout, 2026-10-28): use `load` + 6 s wait.
