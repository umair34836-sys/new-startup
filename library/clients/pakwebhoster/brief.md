# Client: PakWebHoster ("PAK WEB HOSTER"; web hosting + domains, Pakistan)

Home session for this client: this branch `client-pakwebhoster` (started 2026-10-25). Everything below was read on the
live sites on 2026-10-25 (full browser crawl) unless marked otherwise. Re-read the relevant live pages in a browser
before every new video: prices and offers change.

**FULL SITE DATA (every plan, price, domain table, offer, policy, contradiction): `site-data.md` beside this file**
(raw page text in site/pages, people-free screenshots in site/screens, crawl tools in site/tools, brand images in assets/).

## Sites
- Main site: https://pakwebhoster.com (use this URL in videos). 9 real pages; 7 sitemap URLs 404 and /sitelock,
  /codeguard are empty (list in site-data.md "Broken / empty pages").
- Client area / store / domain pricing: https://user.pakwebhoster.com (WHMCS, "Login" on the main site). Much of its
  text is theme demo text (Jaipur address, example@gmail.com, +91 number, "Zhostv2", Lorem ipsum): never quote it.
- Fetching: curl and Playwright both worked (HTTP 200, Cloudflare + LiteSpeed). robots.txt allows `*` with
  "Content-Signal: search=yes,ai-train=no,use=reference" (we read it only to make the client's own videos).

## Key facts (safe: same on every page where they appear)
- "Web Hosting in Pakistan from Rs. 200/mo" (title + meta) [/]; hero "Reliable hosting to make any Website",
  "Get all the essentials features Starting at PKR 200/mo" [/].
- Shared: Starter Lite PKR 200/mo (PKR 2000/yr, "2 Month Free"), Performance Basic 350, Standard 500, Enterprise 900
  [/shared-hosting]. WordPress: Lite Rs 200, Basic 350, Medium 500 (.SITE | .XYZ domain free) [/wordpress].
  Business: Lite Rs 500, Basic 800, Enterprise 1800 [/business-hosting]. Reseller: Lite Rs 800 (25 cPanel), Basic 2000,
  Medium 3500, Enterprise 5000; Free WHMCS + free .com on yearly plan [/reseller].
- Every plan card: NVMe storage, Free SSL Certificate, LiteSpeed web server, Unlimited/Unmetered Bandwidth, Realtime
  Malware Scanner, 24/7 Live Support; most add "Python & Node JS Supported" [all plan pages].
- Domains (first year): .com PKR 3800, .site 400, .online/.xyz/.shop 750, .info 1700 [/domain-register]; renewals are
  much higher (table in site-data.md). Free with every domain: 2 email accounts, forwarding, DNS, theft protection [/].
- Client-area banner: "Hosting Flash Sale: Starting at Rs 200/mo for a limited time" (no end date, no code) [user:/].
  No promo code exists on the site (2026-10-25).
- NOT on the site (ask the client if a video needs it): payment methods, data-centre locations, social media pages,
  real testimonials, VPS/dedicated plans (store "VPS Hosting" holds only a "Test" product, Rs1,000).

## Ask the client before using (pages disagree; details in site-data.md "Contradictions")
- Money-back: 14 vs 30 vs 45 days; Terms say monthly plans are non-refundable. Uptime: 99% vs 99.9%/99.99%/99.999%.
- "20x faster" vs "5x faster"; "10+" vs "100+ Running Promos"; Shared Basic 35 GB vs 30 GB; Business Medium Rs1,400
  only in the store; company name PAK WEB HOSTER vs "Jet Host Hub" vs "Muhammad Fahad LTD" (UK address in Terms).

## Brand
- Name as written on the site: "PAK WEB HOSTER" (titles, footer); logo wordmark "PAKWEBHOSTER" (PAKWEB navy + HOSTER
  green) with tagline "FAST • SECURE • RELIABLE" and a green cloud + server-stack icon.
- Logo: https://pakwebhoster.com/images/logo.png (1957x452, white background, no transparency) = `assets/logo.png`
  (byte-identical to the client-area logo). Favicon: main-site /images/favicon.png and /images/favicon.ico are 404;
  client-area favicon https://user.pakwebhoster.com/templates/zhostv2/custom/images/favicon.png = `assets/favicon-client-area.png` (64x64).
- Colours:
  - Logo (measured on assets/logo.png with PIL 2026-10-25): green #01c062 ("HOSTER"), navy #1a2f3b ("PAKWEB").
    `brand_from_logo.py` palette: #07ac5e (36%, black text 7.08:1), #1d323e (16%, white text 13.34:1), #43d04d, #cee4da, #7eb9a4.
  - Site CSS (https://pakwebhoster.com/css/style.css): --color-one #2a862e (buttons/badges), --color-one-dark #257629,
    --color-two #ffd900 (yellow underline accents in the client area), --color-three #1372de, --color-four #f0f7fd;
    meta theme-color #198754. Computed in Chromium (home): text #212529 / #4a5568 / #00284e, backgrounds #f8f8f8,
    #eff2f7, #f6f9ff, WhatsApp button #25d366.
- Fonts (loaded in Chromium on /, 2026-10-25): Manrope (headings + body, 114 text nodes) and Ubuntu (34). Both in
  `library/fonts/` (Manrope-Variable.ttf OFL; Ubuntu-Regular/Bold.ttf, Ubuntu Font Licence).
- Other site images kept in `assets/` (no people): finddomain.png, client-area herobannerimg/migrate/2.png illustrations,
  icon1-4.png (white line icons), app logos (WordPress, Joomla, Drupal), money/guarantee/discount/customer/
  performance/transferdomain .svg icons, Norton + "trust" badges (third-party marks: do not use as our claims).
  Stock photos of people on the site (hero images, og-home.jpg, fast.svg, sharedhosting.svg, wordpresspage.png) are NOT
  stored and must not be used.

## Contact (for end cards; read back digit by digit on the render)
- Call / WhatsApp: +92 324 3458649 (site: "+923243458649", wa.me/923243458649). Email: info@pakwebhoster.com.
  Web: pakwebhoster.com. Address exactly as printed in the main-site footer: "Pakistan,punajab,city bahawalnagar,area
  farooqbad st 18" (has typos): get the correct spelling from the client before showing it.

## Voice
- Repo default (owner rule, no ElevenLabs): `library/tools/vs_tts.py` with no --voice/--ref/--instruct = voices.json
  "default" (free AI-designed young energetic Hindi ad narrator, VoxCPM2, Apache-2.0, commercial OK). Script in
  Devanagari, Whisper-check every line (library/tools/wcheck_lines.py). Captions in Roman Urdu (owner rule).
- This is a Pakistani client: ask the owner whether the VO should be Urdu-leaning wording (the voice itself is the
  default one either way).

## Templates to start from
- `library/templates/hosting-promo-reel` (MoradoSolution/SkilloraClouds hosting reels), `library/templates/brand-kit`
  (logo sting, offer badge, contact end card with WhatsApp QR), `library/templates/screen-tutorial` (order/how-to videos
  with a visible cursor on every click), `library/templates/website-promo`.

## Delivered
- (nothing yet)
