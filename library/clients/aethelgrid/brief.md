# AethelGrid (client) - brief

- Relayed by the owner 2026-10-28 (verbatim): "so we want a 60 sec video showing the core features of our host
  including site and panel"
- Site: https://aethelgrid.cloud/ - Panel: https://gp.aethelgrid.cloud/
- Job: ~60 s video, core features of the host, from BOTH the website and the panel.
- Status 2026-10-28: site crawled (facts: site-data.md). Panel = public login page only (Pterodactyl + Blueprint,
  "Powered by Nebula" theme); inside of the panel NOT seen. Waiting for the owner: format (9:16/16:9), VO or
  music+text (language), watermarked previews?, and panel access (demo login / client recording / login page only).
- New client: ask before sending a clean file (watermark rule for unpaid clients).
- Never create an account, log in with guessed data, submit a form or press "Order Now" on this site.

## Re-capture (screenshots are never committed)
- `node site/tools/crawl.js urls.txt <scratch>/crawl` (urls.txt = https://aethelgrid.cloud/ + https://gp.aethelgrid.cloud/)
- `node site/tools/explore.js <scratch>/explore`: clicks menus, FAQ, location/processor/currency toggles, panel tabs
  (never Order Now / Get Started / Copy). /vps can miss `networkidle` (30 s timeout, 2026-10-28): use `load` + 6 s wait.
