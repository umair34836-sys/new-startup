# HostLixo (hostlixo.in): site data

Read on the live site on 2026-10-27 with a real-browser crawl (Playwright Chromium, `site/tools/crawl.js`, every tab /
toggle / accordion opened). Raw page text: `site/pages/*.txt`; colours/fonts/images: `site/brand.json`
(`site/tools/brand.js`). The crawl found 7 pages (= sitemap.xml): `/`, `/minecraft.html`, `/network.html`, `/vps.html`,
`/about.html`, `/support.html`, `/terms.html`. curl also answered 200 (https://hostlixo.in -> https://www.hostlixo.in/).
`https://control.hostlixo.in/` (header "Control Panel" link) answered 403 to curl on 2026-10-27: not captured.

## Product: Minecraft server hosting, AMD EPYC (the only live product)
Title of `/`: "HostLixo Minecraft Server Hosting in India from ₹90/mo". Hero: "Minecraft Server Hosting in India from
₹90/mo" [/]. "Compare nine AMD EPYC plans ... priced at ₹45 per GB of RAM" [/minecraft.html].

| Plan | RAM (DDR5 ECC Registered) | CPU allocation | NVMe disk | ₹/mo | ₹/year (annual toggle) | Tag |
|---|---|---|---|---|---|---|
| AMD EPYC 2 GB | 2 GB | 100% | 8 GB | 90 | 1,080 (= 90 x 12; the crawl drops "1,080" here because that string was already on the page) | |
| AMD EPYC 4 GB | 4 GB | 150% | 16 GB | 180 | 2,160 | |
| AMD EPYC 6 GB | 6 GB | 200% | 24 GB | 270 | 3,240 | |
| AMD EPYC 8 GB | 8 GB | 250% | 32 GB | 360 | 4,320 | RECOMMENDED, POPULAR, "Community Favorite" |
| AMD EPYC 12 GB | 12 GB | 300% | 48 GB | 540 | 6,480 | "Modpack Scale" |
| AMD EPYC 16 GB | 16 GB | 350% | 64 GB | 720 | 8,640 | NETWORK GRADE, "Heavy SMP & Bungee" |
| AMD EPYC 20 GB | 20 GB | 400% | 80 GB | 900 | 10,800 | "High Entity Performance" |
| AMD EPYC 24 GB | 24 GB | 500% | 96 GB | 1,080 | 12,960 | "Multi-Hub Cluster" |
| AMD EPYC 32 GB | 32 GB | 600% | 128 GB | 1,440 | 17,280 | TITAN CLUSTER, "Maximum Raw Scale" |

(The annual toggle shows "12x MONTHLY": the year price is exactly 12 x monthly, i.e. NO annual discount. Read the
annual screenshot before quoting a yearly price.)

Every plan [/minecraft.html, /support.html FAQ]: 2 automated backup allocations, 2 extra ports, 1 MySQL database,
"Enterprise L3/L4 DDoS Protection". Button on every plan: "Order on Discord" (no web checkout).
Home stats [/]: "₹90 Starting price per month", "9 Plans AMD EPYC tiers available", "2–32 GB DDR5 ECC RAM per plan
range", "2 Backups Allocation included per plan". Home card: "2 GB up to 32 GB DDR5 ECC RAM", "100% to 600% Dedicated
CPU Allocation", "8 GB to 128 GB High-Speed NVMe Disk".
Software [/support.html FAQ]: Vanilla, Paper, Purpur, Spigot, Fabric, Forge, NeoForge (home/about list 6, without
Vanilla; terms add Mohist).
Order steps [/]: 01 Compare the plans, 02 Choose your tier, 03 Contact HostLixo on Discord.

## Coming soon (never show as available)
- Intel and AMD Ryzen 9 Minecraft plans: "COMING SOON", "PRICING TBA" [/, /minecraft.html].
- Cloud VPS + Bare-Metal Dedicated + BGP Anycast: "COMING Q4 2026", "Planned; details to be announced" [/vps.html].

## Policies
- "24-Hour Refund Policy" (footer of every page). Terms [/terms.html]: "24-HOUR MONEY-BACK GUARANTEE", "100% No-Risk
  Trial on All HostLixo Minecraft Plans", refund within 24 h of first purchase; renewals not refundable.
- Terms: "99.99% Network SLA", "Tier-IV facilities in Mumbai, Maharashtra, India".

## Network page [/network.html]
"Preview Latency Estimates": Mumbai ~14 ms, Singapore ~48 ms, Dubai ~35 ms, each marked "SAMPLE ESTIMATE ... not live
routing data". Protection list (Minecraft Query Botnet, UDP Amplification, TCP SYN Flood, Layer 7 Handshake Spam) each
says only "See plan details". Do not quote these ms values as real ping.

## Contact / community
- Discord (every nav/CTA link): https://discord.gg/bcEghUwdyD. (https://discord.gg/9ysfdEUzgN is the web developer
  ThunderStudio's link, not HostLixo's.) Discord member counts show "Unavailable".
- Email: support@hostlixo.in [/support.html]. No phone / WhatsApp / social pages on the site.
- Payments (footer badges): VISA, MASTERCARD, UPI, PAYTM, CRYPTO.
- Company line: "© 2026 HostLixo Cloud Solutions Inc." Team [/about.html]: founders Rifat Ahmed, Shubham Mishra,
  "Sʜᴏᴜʀʏᴀ !=" (names: never put in a video without asking).

## Contradictions (ask the client before using)
1. Terms' refund section: "We stand 100% behind the quality of our AMD Ryzen™ 9 9950X and Intel hardware" and lists
   "Ryzen Starter/Champion/Titan, Intel Elite/Pro, AMD Performance" plans; the plan pages say Ryzen/Intel are coming
   soon and the live plans are named "AMD EPYC 2 GB ... 32 GB". Footer lists "AMD EPYC Genoa"; plan pages say only
   "AMD EPYC".
2. Mumbai datacenter + 99.99% SLA + "lowest latency in India" appear only in the Terms, not on the plan pages; home
   says "DDoS-filtered" while plan cards say "Enterprise L3/L4 DDoS Protection".
3. Software list differs per page (6 / 7 / 8 names, see above).
4. Home card "Dedicated CPU Allocation" vs plan cards "CPU Allocation".
