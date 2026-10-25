# PakWebHoster: full website data (pakwebhoster.com + user.pakwebhoster.com)

Full crawl done 2026-10-25 (04:58-05:05 UTC) in headless Chromium (Playwright), tool `site/tools/crawl.js`:
start = all 15 sitemap.xml URLs + the client-area entry pages, then every internal link found on each page
(64 URLs fetched, 2 hosts). On every page the crawler clicked every tab/toggle and then opened every accordion, dropdown
and tab pane, so hidden text is in the saved text (sections "--- after clicking [...]" / "--- hidden text ---").
Nothing was logged into, registered, added to a cart, ordered or submitted. Every fact below was read on that crawl;
the page is in brackets ([/x] = https://pakwebhoster.com/x, [user:/x] = https://user.pakwebhoster.com/x).
Nothing here is guessed. Prices/offers change: re-run the crawl before every video and diff.

Files beside this one:
- `site/pages/<slug>.txt`: rendered text of every fetched URL (`home.txt` = /, `user__*` = client area);
  `site/pages/_index.json`: every URL + HTTP status + final URL + every external / not-crawled link.
  `site/pages/user__domain_pricing_all.txt`: the full TLD price table (tool `site/tools/domain_pricing.js`).
- `site/screens/*.webp`: full-page screenshots (1440 px wide) of the 30 pages with real content (tool
  `site/tools/shots.js`). Every big image is HIDDEN in them on purpose: the hero/feature images are stock photos
  of people (some embedded inside .svg files), and the repo never stores people's photos.
- `site/images.json`: every image URL used on each page. `site/sitemap.xml`, `site/robots.txt`: as fetched.
- `assets/`: logo, client-area favicon and non-people images from the site (see brief.md "Brand").
  NOT downloaded/kept on purpose: og-home.jpg, fast.svg, sharedhosting.svg, wordpresspage.png (stock photos of people).

## Sites and what is on them
- Main site https://pakwebhoster.com (LiteSpeed, Cloudflare). sitemap.xml (lastmod 2026-10-08) lists 15 URLs.
  Real pages (HTTP 200 with content): /, /domain-register, /shared-hosting, /wordpress, /business-hosting, /reseller,
  /Privacy-Policy, /Refund-Policy, /Term-Condition (the .html versions of the last three show the same text).
- Client area https://user.pakwebhoster.com (WHMCS with the theme "zhostv2"; the "Login" button on the main site goes
  there). Public pages read: home, store categories (shared, wordpress, business, reseller, vps), domain pricing,
  domain-search.php, transfer-domain.php, domain-promos.php, shared-hosting.php, wordpress-hosting.php,
  reseller-hosting.php, vps-server.php, dedicated-server.php, knowledgebase, announcements, downloads, contact.php,
  legal-agreement.php, privacy-policy.php.
- robots.txt (Cloudflare-managed): `User-agent: *` Allow /, "Content-Signal: search=yes,ai-train=no,use=reference";
  training crawlers (GPTBot, ClaudeBot, anthropic-ai, CCBot, ...) Disallow /. [/robots.txt]

## Broken / empty pages (could not be read: nothing there)
- Sitemap URLs that return **404**: /extension, /contact, /privacy-policy, /refund-policy, /term-condition, /career,
  /cookies-policy (the policies exist only with capital letters: /Privacy-Policy, /Refund-Policy, /Term-Condition).
- **/sitelock and /codeguard: HTTP 200 but empty page (0 characters).**
- Footer/menu links that 404: "Contact Us" / "Contact Support" (/contact), "Career" (/career, /career.html),
  "Useful Extension" (/Extension), /transfer.html, /contact.php. [footer + nav of every main-site page]
- Client area: /serverstatus.php ("Network Status"), cart.php?gid=addons, supporttickets.php redirect to the login
  page; /announcements and /knowledgebase (without .php) 404. Knowledgebase: "No categories exist", "No Articles Found";
  Downloads: "No Downloads to Display". [user:/index.php/knowledgebase, user:/index.php?rp=/download]
- Not opened on purpose (order/login steps): product pages /store/<group>/<product> and cart.php?a=add (the first step
  of an order), login, register, password reset, client area, affiliates.php, submitticket.php.

## Headline claims (main site)
- Title: "Web Hosting in Pakistan from Rs. 200/mo | PAK WEB HOSTER"; meta description: "Cheap web hosting in Pakistan
  from Rs. 200/mo. NVMe storage, LiteSpeed, free SSL, cPanel and 24/7 support. Register your domain and go live today." [/]
- Hero: "RELIABLE HOSTING TO MAKE ANY WEBSITE", "Unmetered Sub Domains, Accounts", "99% Uptime Guarantee",
  "14-Day Money-Back Guarantee", "Get all the essentials features Starting at PKR 200/mo". [/]
- Footer strip on every main-site page: "24 x 7 Customer Support", "99% Uptime Guarantee", "10+ Running Promos",
  "14-day Money-back guarantee". "Hotline 24/7: +923243458649". [/ and all main pages]
- "Your Website 20x Faster" (home); "UP TO 20X FASTER" and "5x faster loading times than competing services"
  (/shared-hosting, /wordpress). "Shared Hosting powers 27% of websites on the Internet" [/shared-hosting];
  "WordPress powers 27% of websites on the Internet" [/wordpress]. "over 25,000+ themes"; "50+ Plugins - Powered by
  Softaculous" [/shared-hosting].
- Logo tagline (in the logo image): "FAST • SECURE • RELIABLE". [assets/logo.png]

## Shared Hosting [/shared-hosting] (PKR; card shows monthly + yearly)
| Plan | Monthly | Yearly (as printed) | Websites | NVMe | Subdomains | Emails | Databases |
|---|---|---|---|---|---|---|---|
| Starter Lite | PKR 200 /mo | PKR 2000 / Year (2 Month Free) | 1 | 10 GB | 10 | 10 | 10 |
| Performance Basic | PKR 350 /mo | PKR 3500 / Year (2 Month Free) | 3 | 35 GB | 30 | 30 | 30 |
| Standard | PKR 500 /mo | PKR 5000 / Year (2 Month Free) | 7 | 50 GB | Unlimited | Unlimited | Unlimited |
| Enterprise | PKR 900 /mo | PKR 9000 / Year (2 Month Free) | Unlimited | Unlimited | Unlimited | Unlimited | Unlimited |
Every card: Unlimited Bandwidth, Free SSL Certificate, Litespeed Webserver, Python & Node JS Supported, Realtime Malware
Scanner, 24/7 Live Support. Page also: Auto-Setup, Auto-Updates, Optimized Performance, Auto-Backups, Auto-Secured.
Client-area store [user:/index.php?rp=/store/shared-hosting]: Starter Rs200, Basic Rs350, Standard Rs500, Enterprise Rs900,
all "Monthly"; Starter/Basic/Standard cards add "One Click Apps Installer" and "14 Days Money Back Guarantee";
Enterprise card adds ".com Domain Free". (Basic = 30 GB there vs 35 GB on /shared-hosting: see contradictions.)

## WordPress Hosting [/wordpress] (= [user:/index.php?rp=/store/wordpress-hosting], "Monthly")
| Plan | Price | Websites | NVMe | Subdomains/Emails/DBs | Extra |
|---|---|---|---|---|---|
| WordPress Lite | Rs 200.00 /mo | 1 | 15 GB | 5 / 5 / 5 | |
| WordPress Basic | Rs 350.00 /mo | 3 | 40 GB | 10 / 10 / 10 | |
| WordPress Medium | Rs 500.00 /mo | 7 | 60 GB | Unlimited | ".SITE \| .XYZ Domain Free" |
Every card: Unlimited Bandwidth, Free SSL, Free 1-click WordPress Installation, Realtime Malware Scanner, 24/7 Live
Support (Lite/Basic also "LiteSpeed Webserver"). Page also says: auto WordPress updates, "CodeGuard automatically set up"
backups, "SiteLock's advanced security tools", cache + CDN, "Ceph-based storage ... across 3 distinct devices",
"Automatic Failover", "Instant Scaling ... add RAM and CPU without a reboot". [/wordpress]

## Business Hosting [/business-hosting]
"Simplicity of Shared Hosting with the Power of Cloud"; "The first prepaid managed cloud infrastructure starting at
Rs500.00/mo*"; "99% uptime for rock-solid performance".
| Plan | Price | Websites | NVMe | Extra |
|---|---|---|---|---|
| Business Lite | Rs 500.00 /mo | 1 | 100 GB | |
| Business Basic | Rs 800.00 /mo | 3 | 300 GB | |
| Business Medium (client area only) | Rs1,400 Monthly | 7 | 500 GB | ".Site \| .XYZ Domain Free (YEARLY plan)" |
| Business Enterprise | Rs 1800.00 /mo | Unlimited | Unlimited | ".COM Domain Free (YEARLY Plan)" |
All: Unlimited Bandwidth/Subdomains/Emails/Databases, Free SSL, Python & Node JS, Realtime Malware Scanner, 24/7 Live
Support (Lite/Basic also LiteSpeed). Business Medium appears only at [user:/index.php?rp=/store/business-hosting].

## Reseller Hosting [/reseller] (= [user:/index.php?rp=/store/reseller-hosting], "Monthly")
| Plan | Price | cPanel accounts | NVMe |
|---|---|---|---|
| Reseller Lite | Rs 800.00 /mo | 25 | 70 GB |
| Reseller Basic | Rs 2000.00 /mo | 60 | 150 GB |
| Reseller Medium | Rs 3500.00 /mo | 100 | 500 GB |
| Reseller Enterprise | Rs 5000.00 /mo | Unlimited | Unlimited |
All: Free WHMCS, Free .com Domain (Yearly Plan), Unmetered Bandwidth, Unlimited Subdomains/Emails/Databases, Private
Nameservers, 1 GB RAM/cp, Free SSL, Litespeed, Python & Node JS, Realtime Malware Scanner, 24/7 Live Support.
Page also: "99.9% Uptime Guarantee", "30-Day Money-Back Guarantee", "24x7x365 Support", WHM + cPanel + Softaculous,
"Dual Quad-Core Xeon powered Servers". Server Specifications tab: "Dual E5530 2.40GHz Xeon quad core hyperthreaded
processors, 24 GB RAM, 250 GB RAID 1 (mirrored) OS drive, 1 TB RAID 1 (mirrored) customer data drive cached, Battery
backed RAID controller, Redundant Power, HVAC & Fire-Detection Systems". Programming tab: "PHP 7.3/7.4, Perl, Python,
RoR, GD, cURL, CGI, mcrypt3; Apache 2.4x; MySQL 5; Zend Optimizer, Zend Engine, ionCube Loader". Email tab: webmail,
spam/virus protection, forwards, aliases, autoresponders, mailing lists, parked domains, free DNS management. [/reseller]

## VPS / Dedicated (client area only; NO real plan)
- Store "VPS Hosting" has one product named **"Test", Rs1,000 Monthly**, no specs. [user:/index.php?rp=/store/vps-hosting]
- vps-server.php: "Linux KVM VPS Hosting", "Instant Provisioning", "Full Root Access", "DDOS Protection", semi-managed
  support list; "Additional Storage ... At $ 21.78/GB/month"; contact block shows "example@gmail.com", "+91 123 456 7890"
  and "Lorem Ipsum" = theme demo text. No VPS prices. [user:/vps-server.php]
- dedicated-server.php: "30 Days Money Return Available", "99.999% uptime" and "99.99% uptime", "Lorem ipsum"; no plans
  or prices. [user:/dedicated-server.php]
- Store shared-hosting also lists a product "ffdfdd" at Rs0 (test product). [user:/index.php?rp=/store/shared-hosting]

## Domains
Main-site cards [/domain-register]: .Com PKR 3800, .Online PKR 750, .UK PKR 2126, .Site PKR 400, .Info PKR 1700,
.XYZ PKR 750, .Blog PKR 1440, .Shop PKR 750. Home cards [/]: .Com 3800, .XYZ 750, .Site 400, .Online 750 "/Yearly".
Full client-area table [user:/index.php?rp=/domain/pricing, Show entries = All; 23 TLDs], Rs, 1 year:
| TLD | Register | Transfer | Renewal | | TLD | Register | Transfer | Renewal |
|---|---|---|---|---|---|---|---|---|
| .com (HOT) | 3,800 | 3,831 | 4,156 | | .xyz | 750 | 5,413 | 5,413 |
| .online (NEW) | 750 | 12,410 | 12,410 | | .agency | 2,600 | 10,829 | 10,829 |
| .site (SALE) | 400 | 12,410 | 12,410 | | .app | 9,000 | 8,662 | 8,662 |
| .shop (NEW) | 750 | 14,447 | 14,447 | | .blog | 1,900 | 9,395 | 9,395 |
| .store (HOT) | 750 | 18,953 | 18,953 | | .click | 750 | 4,232 | 4,232 |
| .net | 5,000 | 5,059 | 5,059 | | .digital | 1,700 | 14,440 | 14,440 |
| .info | 1,700 | 10,107 | 10,107 | | .tech | 1,500 | 22,113 | 22,113 |
| .icu | 1,500 | 6,857 | 6,857 | | .life | 1,300 | 12,634 | 12,634 |
| .me | 900 | 8,301 | 8,301 | | .rest | 750 | 14,407 | 14,407 |
| .top | 800 | 2,531 | 2,531 | | .sale | 2,500 | 13,537 | 13,537 |
| .org | 3,200 | 4,652 | 4,652 | | .bio | 2,500 | 25,915 | 25,915 |
| .fun | 400 | 12,465 | 12,465 | | | | | |
NOTE for any video: the cheap prices are FIRST-YEAR register prices; renewals are far higher (.site 400 -> 12,410).
"FREE Add-ons with every Domain Name!": Free Email Account (2 addresses), Domain Forwarding, DNS Management, Domain Theft
Protection, Free Mail Forwards, Easy to use Control Panel, Bulk Tools. [/, /domain-register]

## Offers / promo codes
- Client-area top bar on every page: **"Hosting Flash Sale: Starting at Rs 200/mo for a limited time"** (no end date,
  no code). [user:/ and every user: page]
- **No promo/coupon code appears anywhere** on either site. domain-promos.php shows only theme text ("Zhostv2 Theme is
  dedicated to provide you...") and domain price cards. [user:/domain-promos.php]
- Free domain with plans: Shared Enterprise ".com Domain Free" [store]; WordPress Medium ".SITE | .XYZ Domain Free";
  Business Medium ".Site | .XYZ" and Enterprise ".COM" free on YEARLY plan; all Reseller plans "Free .com Domain
  (Yearly Plan)". Shared yearly billing = "2 Month Free" [/shared-hosting].
- "Bulk discounts of up to 31% off when you register or transfer more than five .com domains" is on
  [user:/transfer-domain.php] but that page is theme demo text ("Transfer ... to ZhostV2"): do not use.

## Guarantees and policies
- Uptime: 99% [/, every footer]; 99.9% [/reseller]; 99.99% and 99.999% [user:/dedicated-server.php].
- Money-back: 14-day [/, main footer, store cards]; 30-day [/reseller, user: footer, user:/shared-hosting.php];
  45-day [user:/ hero]. Refund Policy [/Refund-Policy] (last updated January 22, 2025): cancel an Order within 14 days;
  refund within 14 days; plans with a free domain: domain fee deducted from the refund. Terms [/Term-Condition]
  (January 22, 2025): "we don't have any refund policy for purchased domains. Monthly plans are non-refundable.";
  a suspended domain costs "20 pounds" to release (paid to the registrar).
- Terms [/Term-Condition]: Company = "Muhammad Fahad LTD, Lytchett House, 13 Freeland Park, Wareham Road, Poole, Dorset,
  BH16 6FA"; no illegal/copyright content, torrents, warez, IRC scripts; no migration service ("we are not responsible for
  migrating, transferring, uploading, or editing any website content"); users must be over 18.
- Privacy Policy [/Privacy-Policy] (last updated "Augest 31, 2025"): "Company refers to Jet Host Hub", Country Pakistan;
  also a privacy policy for a "Quick CPanel Login Chrome Extension" (stores cPanel logins locally, AES-GCM).
- Support: "24/7 Live Support" on every plan card; "24 x 7 Customer Support" footer; "24x7x365 Support" [/reseller].

## Contact channels (as printed)
- Phone / hotline / WhatsApp: **+923243458649** ("Hotline 24/7", "Call") [all main pages]; floating WhatsApp button
  -> https://wa.me/923243458649 [/]; client-area footer "+92 324 345 8649" [user:].
- Email: **info@pakwebhoster.com** (footer, Terms) [/, /Term-Condition]; ameezfarmood477@gmail.com (contact block
  "Email Us", Privacy, Refund) [/, /Privacy-Policy, /Refund-Policy].
- Address: "Pakistan,punajab,city bahawalnagar,area farooqbad st 18" (sic) [main footer].
- "Our Location: Open Google Maps" links to https://www.google.com/maps (no place). [/]
- Client area contact form "Pre-Sales Contact Us" (not submitted) [user:/contact.php]; "Open Ticket" needs login.
- Social media: **none linked** anywhere (no Facebook/Instagram/YouTube/TikTok link found in _index.json external list).
- Payment methods: **not stated on any public page** (no JazzCash/Easypaisa/bank/card text found).
- Data centres / server locations: **not stated** anywhere ("State-of-the-art Datacenters", "top-tier data centres" only).

## Contradictions and template leftovers (do NOT use these in videos without asking the client)
1. Money-back: 14 days (main site, store) vs 30 days (/reseller, client area) vs 45 days (client-area home hero).
2. Uptime: 99% vs 99.9% vs 99.99% vs 99.999%.
3. Running promos: "10+" (main footer) vs "100+" (client-area footer).
4. Speed: "20x faster" vs "5x faster" vs "upto 2x faster" (/wordpress Cloud section).
5. Shared Basic: "Performance Basic" 35 GB (/shared-hosting) vs "Basic" 30 GB (store). Starter Lite vs Starter.
6. Business Medium Rs1,400 exists only in the client-area store, not on /business-hosting.
7. Domains: .Blog PKR 1440 [/domain-register] vs Rs1,900 [domain pricing]; .UK PKR 2126 is not in the pricing table;
   client-area cards print domain prices as "Rs 3800.00 /mo" (should be per year) [user:/, user:/domain-promos.php].
8. Company name: "PAK WEB HOSTER" vs "Jet Host Hub" (/Privacy-Policy, /domain-register "Transfer Your Domain to Jet Host
   Hub", Terms) vs "Muhammad Fahad LTD" (UK address, Terms) vs "Zhostv2"/"ZhostV2" (client-area theme text).
9. Address: Bahawalnagar, Punjab, Pakistan (main) vs "House 168/170, Jaipur, Rajasthan India" (client-area footer).
10. Contact on client-area pages: "example@gmail.com", "+91 123 456 7890", tel:1234567899 (theme placeholders).
11. Refund: Refund Policy allows 14-day cancellation; Terms say monthly plans are non-refundable.
12. Testimonials are theme placeholders ("Aaron Sweeney", "Sara Wilsson" with "Lorem ipsum...", "Simon Deubele");
    "Lorem ipsum" also on /wordpress-hosting.php, vps-server.php, dedicated-server.php. Do not quote any testimonial.
13. Hardware: Reseller "Dual E5530 2.40GHz Xeon ... 24 GB RAM" vs shared-hosting.php "Dual Intel Xeon E5-2630, 64 GB
    RAM, 256 GB SSD RAID 1, 2 TB SATA RAID 1" vs dedicated "Xenon D processors"; "Apache 2.4x" vs "LiteSpeed".
14. WordPress FAQ: "No, You cannot change upgrade or downgrade plans" vs "Instant Scaling ... add RAM and CPU".
15. Announcements: only the WHMCS sample "Thank you for choosing WHMCS!" (15 Sept 2026).
16. Home FAQ (7 questions) exists only inside an HTML comment on the main site: not visible to visitors.

## Safe facts for a promo (consistent everywhere they appear)
- Hosting from Rs/PKR 200 per month (Starter Lite / WordPress Lite) [/, /shared-hosting, /wordpress, store].
- NVMe storage, Free SSL, LiteSpeed web server, unlimited bandwidth, realtime malware scanner, 24/7 live support
  [every plan card]. cPanel [meta description, /reseller]. Free email accounts with domains [/, /domain-register].
- .com Rs 3,800/year, .site Rs 400 first year, .online/.xyz/.shop/.store Rs 750 first year [/domain-register, pricing].
- Contact: +92 324 3458649 (call/WhatsApp), info@pakwebhoster.com, pakwebhoster.com.
- Ask the client before using: money-back days, uptime %, "Flash Sale" end date, any speed multiplier, company name.

## Re-crawl
```
cd <scratch> && cp library/clients/pakwebhoster/site/tools/*.js . && \
grep -o '<loc>[^<]*' library/clients/pakwebhoster/site/sitemap.xml | sed 's/<loc>//' > urls.txt   # + client-area entry URLs
node crawl.js urls.txt out             # text + links (+ raw screenshots, NOT for commit: they show stock people photos)
node domain_pricing.js out/pages/user__domain_pricing_all.txt
node shots.js shots.txt screens images.json   # "<url> <name>" per line; hides people photos
```
Never run `pgrep/pkill -f "node crawl.js"` from a shell whose own command line contains those words (it matches itself).
