# GOOD's — verified site + Discord data

Every line below was read on 2026-11-02 (UTC 14:28-14:30) by this session.
- Website: https://www.goodss.store/ rendered in headless Chromium (Playwright, desktop 1440 px + mobile 430 px), page
  text from `document.body.innerText` after the JS rate cards loaded. Static HTML (curl) shows OLDER rate numbers than the
  rendered page (e.g. INR->CRYPTO 105 static vs 108 rendered): quote the rendered values only, with the date.
- Terms: https://www.goodss.store/terms.html (same method). /privacy.html and /aml.html answered 404 (curl, same day),
  although the footer links "Privacy Policy" and "AML Policy".
- Discord: https://discord.com/api/v9/invites/goods?with_counts=true (and invite SVhXk5nPbe: same guild id).

## Names used by the client (they differ by place)
- Discord server name: "GOOD's" (server tag "GOOD"), brand colour in the invite profile: `#e8c02f`.
- Website title / header: "GOOD's EXCHANGE".
- Logo GIF + banners: "GOOD's STORE".
- Slogan given by the owner (client's wording): "GOOD's | Where trust is build."

## Discord (invite API, 2026-11-02 14:28 UTC)
- Guild id 1236946348373442580, vanity `goods`, community + discoverable, boost tier 3 (19 boosts).
- approximate_member_count 3532, approximate_presence_count (online) 583.
- Description (verbatim): "⚡ Welcome to GOOD's. A Crypto Currency platform that focuses on exchanges, trading and
  financial advice from experts. We have 'top-tier' security measurements to ensure maximum encryption of funds in
  accordance to discord's policies."
- "Est. May 2024" was seen on the invite card in the owner's screen recording (main session, 2026-11-02). Guild id
  snowflake 1236946348373442580 -> timestamp (id >> 22) + 1420070400000 = 2024-05-06 07:43 UTC (computed here with python), which agrees.

## Website: what it is
- Meta description: "GOOD's EXCHANGE — Fast, Secure & Reliable Currency & Crypto Exchange. Get the best rates for BDT,
  PKR, INR, NPR, EGP, PHP and Crypto conversions."
- Hero: "Exchange Currency & Crypto At The Best Rates". "Instant BDT, PKR, INR, NPR, EGP & PHP exchange with crypto.
  Transparent fixed rates, fast processing, zero hidden fees." Buttons "Calculate Now", "View Rates", "Start Exchange".
- Hero stats: "2000+ Happy Clients", "7 Currencies", "24/7 Support".
- Sections (nav): Home, Rates, Calculator, How It Works, Terms, Contact. Also Client Reviews, Server Status.

## Every list on the site (grepped from the rendered text)
- Currency tabs: All Currencies, BDT, PKR, INR, NPR, EGP, PHP, SAR, CRYPTO, BINANCE GIFT.
- Fiat cards: Bangladesh Taka BDT (9 pairs), Pakistani Rupee PKR (8), Indian Rupee INR (8), Nepali Rupee NPR (8),
  Egyptian Pound EGP (8), Philippine Peso PHP (8), Saudi Riyal SAR (8). Plus "Crypto to Crypto" (8) and
  "Binance Gift Card" (8). NOTE: hero text names 6 currencies (no SAR), the stat says 7, the cards show 7 fiat.
- Crypto named in the calculator: "Crypto (LTC,USDT,USDC,ETH,SOL & Any Crypto)"; also "Binance USDT Gift Card".
  How Rates Work says fiat->crypto pays "USDT/BTC".
- Rendered rates 2026-11-02 (per $ of crypto; "BUY" = you pay fiat, "SELL" = you get fiat):
  BDT 135 / 120, PKR 325 / 265, INR 108 / 90, NPR 180 / 130, EGP 75 / 35, PHP 85 / 40, SAR 5 / 2.5.
  BDT->BDT 5% fee, CRYPTO->CRYPTO 5% fee. Binance Gift -> crypto 0.9 / $, -> PKR 238.50 / $, -> BDT 108.00 / $.
  Site footer: "Exchange rates are set by GOOD's EXCHANGE and are subject to change without notice." Rates are
  "fixed by GOOD's EXCHANGE and updated manually".
- How It Works: 01 Check Rates, 02 Contact Us (contact form: amount, pair, payment details), 03 Receive Funds
  ("within 5–30 minutes" after payment confirmation).
- Processing: "Most exchanges are processed within 5–30 minutes after payment confirmation. For payment confirmation
  need time up to 24h." Terms §4: "max 24h and in rare cases, up to 3 days ... We do not guarantee immediate execution".
- Fees: "All transaction and network fees are borne by the customer." (contradicts hero "zero hidden fees"; not hidden
  if stated, but do not repeat "zero fees").
- Contact channels: Discord discord.gg/goods, Telegram @goodss05 (t.me/goodss05), WhatsApp group (chat.whatsapp.com
  link), Email goodsstorebd@gmail.com. Availability "24 hours a day, 7 days a week"; "Typical response time is under 10
  minutes during active hours (9 AM – 11 PM UTC+6)".
- Footer chips: Secure, Fast, Reliable. Footer line: "Fast, Secure & Trusted Currency Exchange. Your funds, our priority."
- Design: dark navy background, gold/yellow accent, fonts Outfit + Inter (Google Fonts link in the HTML).

## Claims that need the OWNER's OK before any use (risky for a money/crypto promo)
- "100% track record with 2000+ satisfied clients. 5000+ deals, $60,000+ Exchanged." (self-reported, unverifiable)
- "2000+ Happy Clients" vs "trusted by hundreds of clients" (two different numbers on the same page).
- "At The Best Rates", "Instant", "zero hidden fees" (fees are borne by the customer; processing 5 min-3 days).
- "System Uptime 99.97%" and "Last checked" = the viewer's current clock time (it showed 2026-11-02 14:29:37 = our
  render time), i.e. the status panel is not a real measurement: never quote it.
- Client Reviews (AhmedK, Sarah_Trade, Rahul99): cannot be verified; do not show as testimonials.
- Discord: "financial advice from experts", "'top-tier' security ... maximum encryption of funds": never repeat
  (financial advice + security promises).
