# MoradoSolution: full website data (moradosolution.in)

Full crawl done 2026-10-24 (~12:20 UTC): all 36 sitemap URLs plus every internal link found on them
(37 pages, all HTTP 200), each rendered in headless Chromium (Playwright) and saved as its visible text.
Every fact below was read on that crawl; the page it comes from is in brackets. Nothing here is guessed.
Prices and offers change: before a new video, re-run the crawl (see "Re-crawl" at the end) and diff.

Files beside this one:
- `site/pages/<page>.txt`: full rendered text of every page (home.txt = /). `site/pages/_index.json`: list + external links.
- `site/screens/*.webp`: full-page screenshots (1440 px wide) of home, game-hosting, minecraft-budget, hytale, vps,
  vds-bare-metal, bare-metal, infrastructure, ddos-protection, sales, services, status, support, contact.
  (/about screenshot NOT stored: it shows team photos = faces.)
- `assets/`: images downloaded from https://moradosolution.in/assets/ (logo, icons, OG cover, game cards, service and
  rack images). The two team photos (assets/team/*.webp) were deliberately not downloaded.
- `site/sitemap.xml`: sitemap as fetched.

## Pages (37)
/, /about, /abuse, /auctions, /aup, /backup-policy, /bare-metal-guide, /bare-metal, /best-minecraft-hosting-india,
/blog, /cancellation, /contact, /cookies, /ddos-protection-explained, /ddos-protection, /dmca, /fair-use,
/game-hosting, /guides, /hytale, /infrastructure, /minecraft-budget, /refund, /sales, /security, /services, /sla,
/ssl, /status, /support, /suspension-policy, /terms, /third-party, /vds-bare-metal, /vds-vs-bare-metal, /vps,
/privacy (not in sitemap; on 2026-10-24 it showed the Terms of Service page, title "Terms of Service").
robots.txt blocks /admin, /dashboard, /cart, /checkout, /billing, /login, /register, /verify-email, /google-callback,
/api/ (not crawled).

## Live offer (2026-10-24)
- Code **WELCOME30 = 30% OFF**, "No expiry" [/sales]. Valid on: Starter, Basic, Stone, Iron, Gold, Diamond, Emerald,
  Netherite, Titan, Pro, Ultra, Extreme, Ultimate, Spark, Blaze, Inferno, Apex, Eclipse, Nova, Eternal, Hytale Starter,
  Hytale Standard, Hytale Pro, Hytale Ultra [/sales]. (Spark...Eternal appear only on /sales, no plan page found.)
- /game-hosting top banner: "LIMITED OFFER WELCOME30 30% OFF on selected plans".
- /minecraft-budget + /hytale: "Codes apply automatically when you tap Buy Now — or paste them at checkout."
- /services: "Sales & Offers ... Up to 30% Off". /auctions: "No Auctions Running".
- NOTE: the brief said "no live promo code" on 2026-10-24 earlier; by this crawl WELCOME30 is live.

## Minecraft plans [/minecraft-budget] (INR/month; offer price with WELCOME30 as shown on the page)
| Plan | RAM | CPU | NVMe | Price | With WELCOME30 | Players (page FAQ) |
|---|---|---|---|---|---|---|
| Starter | 2 GB | 50% EPYC | 6 GB | ₹199 | ₹139 | 5-10 |
| Basic | 4 GB | 100% | 12 GB | ₹299 | ₹209 | 10-20 |
| Stone | 6 GB | 150% | 18 GB | ₹449 | ₹314 | 20-30 |
| Iron | 8 GB | 200% | 24 GB | ₹549 | ₹384 | 30-50 |
| Gold (POPULAR) | 10 GB | 250% | 30 GB | ₹699 | ₹489 | 50-70 |
| Diamond | 12 GB | 300% | 36 GB | ₹799 | ₹559 | 70-100 |
| Emerald | 16 GB | 350% | 48 GB | ₹999 | ₹699 | 100-150 |
| Netherite | 20 GB | 400% | 60 GB | ₹1,299 | ₹909 | 150-200 |
| Titan | 24 GB | 500% | 72 GB | ₹1,599 | ₹1,119 | 200-250 |
| Pro | 30 GB | 600% | 90 GB | ₹2,099 | ₹1,469 | 250-350 |
| Ultra | 32 GB | 700% | 100 GB | ₹2,399 | ₹1,679 | 350-400 |
| Extreme | 48 GB | 900% | 140 GB | ₹3,399 | ₹2,379 | 400-600 |
| Ultimate | 64 GB | 1200% | 180 GB | ₹4,399 | ₹3,079 | 600+ |
Every card: "DDoS Protection: Cloudflare + In-house", "Panel: Pterodactyl". Home shows 4 of them (Starter, Stone, Gold,
Titan) with "2 GB DDR4" etc.
Other lines on the page: "NVMe storage, Cloudflare Magic Transit DDoS protection, and our own in-house traffic filtering
layer. Deploy instantly, scale freely."; Java + Bedrock (cross-play); Forge, Fabric, CurseForge, Technic; one-click
modpacks; Paper, Purpur; "unlimited player slots"; "no swap memory"; "Scheduled backup support"; "Full console, SFTP
and file-manager access"; payment UPI, net banking, cards, wallets, "no forex charge"; upgrades prorated, immediate.
Ping: "Our primary datacenter is in Delhi, India. This provides 5-25ms ping to all major Indian cities."

## Hytale plans [/hytale]
| Plan | RAM | CPU | NVMe | Price | With WELCOME30 | Players |
|---|---|---|---|---|---|---|
| Starter | 2 GB | 50% | 6 GB | ₹199 | ₹139 | 5-10 |
| Standard | 6 GB | 150% | 18 GB | ₹449 | ₹314 | 20-30 |
| Pro (POPULAR) | 12 GB | 300% | 36 GB | ₹799 | ₹559 | 70-100 |
| Ultra | 20 GB | 400% | 60 GB | ₹1,299 | ₹909 | 150-200 |
Hytale page: "Hytale servers, ready on day one.", "Hytale supports crossplay, and our servers come ready for it".

## Other games [/, /game-hosting]
Available now: Minecraft (RAM 2-64 GB, CPU 50%-1200%, storage 6-180 GB, from ₹199/mo), Hytale (2-20 GB, 50%-400%,
6-60 GB, from ₹199/mo). Coming Soon: Rust, ARK, Valheim, Palworld.
/game-hosting: "Server provisioned in under 60 seconds"; "Automated Backups: Daily backups with one-click restore on all
plans"; "Local team available 24/7 via Discord and tickets"; payments "UPI, GPay, PhonePe, Paytm, net banking".

## VPS [/vps] (KVM, full root, unmetered bandwidth, 1 IPv4, DDoS included)
| Plan | vCPU (EPYC 7C13) | RAM | Gen 4 storage | Price |
|---|---|---|---|---|
| VPS 1 | 2 | 8 GB | 80 GB | ₹676 |
| VPS 2 | 6 | 16 GB | 120 GB | ₹1,352 |
| VPS 3 | 8 | 20 GB | 180 GB | ₹1,690 |
| VPS 4 (BEST VALUE) | 10 | 24 GB | 240 GB | ₹2,028 |
| VPS 5 | 16 | 32 GB | 300 GB | ₹2,704 |
| VPS 6 | 18 | 48 GB | 450 GB | ₹4,056 |
| VPS 7 | 24 | 64 GB | 550 GB | ₹5,408 |
| VPS 8 | 32 | 96 GB | 800 GB | ₹8,112 |
Headline "From zero to SSH in under a minute." OS: Ubuntu 24.04/22.04/20.04, Debian 12/11, AlmaLinux 9/8, Rocky 9/8,
Fedora 41/40, custom ISO. Features: KVM, NVMe, full root, API & Terraform, cloud-init, free private VLAN.
Locations on /vps: Delhi AVAILABLE; Mumbai OUT OF STOCK; Bangalore OUT OF STOCK.
Payments on /vps: UPI, Google Pay, PhonePe, Paytm, net banking, credit/debit cards.

## VDS [/vds-bare-metal] (guaranteed dedicated cores, KVM, unmetered, 1 IPv4)
| Plan | RAM DDR4 | Dedicated vCPU | NVMe | Price |
|---|---|---|---|---|
| Starter | 8 GB | 3 | 50 GB | ₹550 |
| Standard | 12 GB | 6 | 150 GB | ₹850 |
| Pro (POPULAR) | 32 GB | 10 | 400 GB | ₹2,100 |
| Enterprise | 64 GB | 16 | 600 GB | ₹4,100 |
"NVMe Gen4 ... Up to 7 GB/s read speeds." Unmanaged; managed "available on request".

## Bare metal [/bare-metal] (no virtualization, 3 IPv4 each; old price struck through, new price per month)
| Plan | RAM | Cores | NVMe | Was | Now |
|---|---|---|---|---|---|
| VDS-6 "Workstation grade" | 32 GB | 12 | 500 GB | ₹6,500 | ₹4,999 |
| 64 GB (POPULAR) | 64 GB | 18 | 1000 GB | ₹9,500 | ₹7,499 |
| 128 GB | 128 GB | 28 | 2000 GB | ₹12,500 | ₹9,999 |
| 256 GB | 256 GB | 64 | 3000 GB | ₹18,500 | ₹15,999 |
(/bare-metal-guide calls the first one "Entry" and the last "Top-end".)

## Hardware / network [/infrastructure, /game-hosting, /about]
- AMD EPYC 7C13 (64 cores, 128 threads, Zen 3), DDR4 ECC, NVMe Gen 4, 10 Gbps uplink per node.
- "~65% Typical CPU utilization ceiling per host node", "1:1 vCPU to physical thread ratio. No overcommit."
- Network list: Frankfurt (Europe), Delhi (North India), Mumbai (West India): all "OPERATIONAL" [/infrastructure].
- "We peer with 200+ networks at major IXPs", RAID 1 NVMe on every node, node health checked every 30 s,
  N+1 UPS + generator, daily off-site backups [/infrastructure].
- "We own and operate all servers, routers and switches. No resellers" [/game-hosting].
- Footer (every page): "Hosted in Delhi on AMD EPYC 7C13", "99.9% uptime target", "0 swap on NVMe", "7C13 AMD EPYC",
  "DDoS protection included, support answered by humans".

## DDoS [/ddos-protection]
"Attacks end at the edge, not in your server." L3-L7, always-on, "₹0 added", zero config, every plan every location.
"3+ Tbps" global scrubbing, "15+" scrubbing centers, "< 5 s" detection to mitigation. eBPF/XDP, DPDK, nftables,
anycast/BGP. Game ports shown: 25565, 30120, 28015. Honest note on the page: 5-10% of attack traffic may pass
Cloudflare; automatic null-routing above thresholds; no protection can guarantee 100%.

## Support / contact [/support, /contact, /about]
- Emails: support@, abuse@, founder@, regionalmanager@, security@, dmca@ (all @moradosolution.com).
- Discord: discord.gg/moradosolution. Panel: panel.moradosolution.com. VM panel: vm.moradosolution.com.
  Status: status.moradosolution.com (and on-site /status).
- "we respond within 24 hours on business days" [/contact]; "Most issues are resolved the same day" [/support].
- Free migration from another host [/support, /guides, /about].
- /status (2026-10-24): "All systems operational", "Last checked: 24 August 2026"; 90-day uptime: Website & Checkout
  100%, Game Panel & Login 100%, Minecraft Budget Servers 99.98%, VPS Hosting 100%, Network & DDoS Mitigation 100%.

## Company [/about, legal pages]
"Independent game hosting, VPS and infrastructure ... Owned and operated in Delhi, India."
Proprietor: Vandana Shankarmal Kumardey. Team listed: Shivnath Dey (Director & Founder), Amolik Mehta (CEO, Director &
Co-Founder), Heman Rathore (Regional Manager & Technical Head), Jayant Naulakha (Head Manager).
/about: "Delhi & Mumbai: Data centers in India"; "24/7 Support response"; "Free migrations".

## Policies (short; full text in site/pages)
- Refund [/refund, updated 28 Aug 2026]: generally non-refundable once provisioned; request within 24 hours; not automatic.
- Cancellation [/cancellation]: anytime, effective end of billing period.
- Backup [/backup-policy]: customer responsible; data may be deleted 30 days after cancellation.
- SLA [/sla, 28 Aug 2026]: Shared 99.9%, VPS/Dedicated 99.95%, Premium 99.99% monthly target; credits as account credit.
- Fair use [/fair-use]: CPU >80% sustained / RAM >90% may trigger review; 7 days to fix; not for dedicated plans.
- Security [/security]: vulnerability reports to security@, ack within 48 h.

## Blog [/blog] (titles + dates; the "Read more" links led to no separate pages in this crawl)
2026-10-04 VDS vs VPS vs bare metal; 2026-10-04 Bare metal hosting in India; 2026-10-04 DDoS protection explained;
2026-10-03 Best Minecraft hosting in India (zero swap guide); 2026-08-20 "Minecraft budget servers are live in Delhi
... starting at just ₹100/month"; 2026-08-12 "A 48-hour money-back guarantee on every new server"; 2026-08-05 Getting
started with your first Minecraft server; 2026-07-28 How we stop attacks before they reach your server.

## CONTRADICTIONS on the site (do NOT put these in a video without asking the owner/client)
- Locations: /infrastructure lists Delhi + Mumbai + Frankfurt "OPERATIONAL"; its own FAQ, the footer and the plan
  pages say Delhi data centre; /vps says Mumbai + Bangalore OUT OF STOCK / "coming soon"; /about says "Delhi & Mumbai";
  /support FAQ says "Across North America, Europe, and Asia-Pacific". Safe line: "Delhi data centre".
- Uptime: footer 99.9% target; SLA 99.9% / 99.95% / 99.99% by plan type.
- Backups: /game-hosting "Daily backups ... on all plans"; /minecraft-budget "automated backups" and "Scheduled backup
  support"; /support FAQ "Backups are not automatic ... using Google Drive"; /backup-policy "customer responsible".
- Refund: blog title "48-hour money-back guarantee" vs /refund "within 24 hours", "not an automatic right".
- Price floor: blog "starting at just ₹100/month" (Aug 2026) vs every plan page today: from ₹199 (₹139 with WELCOME30).
- Payments: /support FAQ mentions PayPal; plan pages list UPI/GPay/PhonePe/Paytm/net banking/cards.
- DDoS: /game-hosting "In-house filtering ... not third-party" vs plan cards "Cloudflare + In-house".
- /services lists VPS "1 Gbps" and Bare Metal "1Gbps" chips; other pages say 10 Gbps uplinks.
- Support hours: "24/7" [/about, /game-hosting, /vds-bare-metal] vs "within 24 hours on business days" [/contact].
- /privacy shows the Terms of Service page.

## Re-crawl (how this was made)
`node crawl.js urls.txt outdir` (Playwright: goto networkidle, open <details>, save document.body.innerText and follow
internal links, skipping robots-disallowed paths) and `node shots.js` for full-page screenshots; both scripts are kept
in `library/clients/moradosolution/site/tools/`. Run with `NODE_PATH=$(npm root -g)`. 37 pages took ~2 min here.
