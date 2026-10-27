# Client: HostLixo (hostlixo.in; Minecraft server hosting, India)

Home session for this client: branch `client-hostlixo` (started 2026-10-27). Owner's ask (2026-10-27): a 30 s
promotional video, facts only from the website, real site elements (logo, screenshots, site images, brand colours/fonts)
over emojis, professional promotional voice (not the "default" voice, no ElevenLabs), owner's copyright on it.

**Full site data (every plan, price, policy, contradiction): `site-data.md` beside this file.** Raw text: site/pages.
Images and screenshots are NOT in git (owner rule): re-download per job into the scratchpad
(`node site/tools/crawl.js urls.txt out` -> out/screens/*.png; images below).

## Key facts (same on every page where they appear, read 2026-10-27)
- "Minecraft Server Hosting in India from ₹90/mo" (title + hero) [/]. ₹45 per GB RAM per month [/, /minecraft.html].
- 9 AMD EPYC plans, 2 GB -> 32 GB DDR5 ECC RAM, ₹90 -> ₹1,440 /mo; NVMe 8 -> 128 GB; CPU 100% -> 600%.
- Every plan: Enterprise L3/L4 DDoS Protection, 2 automated backups, 2 extra ports, 1 MySQL database.
- Software: Paper, Purpur, Fabric, Forge, NeoForge, Spigot (+ Vanilla in the FAQ).
- Ordering: "Order on Discord" (discord.gg/bcEghUwdyD). Email support@hostlixo.in. 24-Hour Refund Policy (footer + terms).
- Coming soon (never sell as live): Intel + Ryzen plans, Cloud VPS / Dedicated (Q4 2026).
- Ask before using: Mumbai datacenter, 99.99% SLA, "lowest latency" (Terms only); latency ms values (sample estimates).

## Brand (site CSS, read 2026-10-27, `site/brand.json`)
- Monochrome: backgrounds #050505 / #0a0a0a / #0c0c0c / #111111, text #ffffff / #ededed, secondary #999999, muted
  #5e5e5e, borders rgba(255,255,255,.08/.16/.32). White primary buttons with black text. No accent colour.
- Fonts: Space Grotesk 700 (display/headings), Plus Jakarta Sans 400-800 (body), JetBrains Mono 500/700 (labels/tags).
  All three are Google Fonts (OFL).
- Logo: https://www.hostlixo.in/logo.png (432x142, white "HL" mark + "HostLixo" wordmark, transparent),
  https://www.hostlixo.in/hero-logo.png (500x500 white mark, transparent), https://www.hostlixo.in/icon-mark.png
  (708x708 white mark on black).
- Site images (looked at 2026-10-27, all Minecraft gameplay scenes the site uses): /images/mc_world.jpg (shader river
  village), /images/mc_1.jpg (castle SMP), /images/mc_2.jpg (deep dark diamond cave), each 1376x768.
- UI look: thin-border dark cards, small mono uppercase pill labels ("AVAILABLE PLANS", "RECOMMENDED"), big ₹ prices.

## Videos made
- 2026-10-27: 30 s 9:16 promo, watermarked PREVIEW delivered (builder library/templates/hosting-promo-reel/build_hostlixo.py,
  edit log `edit-log-promo-v1.md`, voice `promo-male`, owner chose watermark option (a): tiled "Made by MrCopper804" +
  PREVIEW tag + metadata). Clean file only when the owner says so.
- 2026-10-27: 30 s 16:9 brand identity reveal (music only, site images only), watermarked PREVIEW delivered (template
  library/templates/brand-identity-reveal, config reveal.json, edit log edit-log-reveal-v1.md).
