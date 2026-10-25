# Client: Pizza Base PK (pizza delivery / pick-up; Attock, Haripur, Wah Cantt, Hazro, Swabi, Nowshera)

New client (Oct 25 2026). Home session: this branch `client-pizzabasepk`. Everything below is from the live site read in
Chromium on 2026-10-25 (details, sources and the contradictions list: `site-data.md`). Re-crawl before every new
video (`node crawl.js <dir>` then `node crawl_items.js <dir>`; prices/deals change).

## Site
- https://pizzabasepk.com/ : one-page Indolj storefront (order type + city selector, then the menu). Item popups at
  /product/<slug>. Other pages: /pages/faqs (generic platform text), /pages/privacy-policy.
- curl gets Cloudflare "error code: 520": use a real browser (Playwright). The menu is lazy-loaded: full-page
  screenshots show empty sections; scroll in steps (crawl_items.js does).
- The page's own JSON (console.indolj.io WebApiV2 StructuredMenu / BranchDetails) holds the full menu, branches,
  timings; every price was cross-checked against the rendered popup (0 mismatches, 2026-10-25).

## Facts safe for videos (site, 2026-10-25)
- 6 cities: Attock, Haripur, Wah Cantt, Hazro, Swabi, Nowshera. Delivery + Pick-Up. One menu/price list for all.
- Phone 051 111 121 222 (every page); WhatsApp wa.me/923114000029 (menu page); info@pizzabasepk.com;
  socials @pizzabasepk (Facebook, Instagram, Threads), TikTok @pizzabase.pk.
- Deals: Daily Base Deal 1 = 1 Pan Pizza + 345ml drink Rs. 650 ... Deal 4 = 1 Jumbo + 1.5 L Rs. 2,099;
  Super Base (2 pizzas) Rs. 1,050 / 1,999 / 2,899 / 3,399; Teen Ka Scene (3 pizzas) Rs. 1,299 / 2,499 / 3,699 / 4,799;
  Time Offer Deal 1 Rs. 1,399 (Regular pizza, 4 pcs kabab, 2 drinks), Deal 2 Rs. 1,999 (Large pizza, 6 pcs wings, 1.5 L).
- Pizzas: 19 flavours Small Rs. 899 / Regular 1,799 / Large 2,399 / Jumbo 2,799 (Seekh Kabab: no Small);
  Grilled Black Pepper Tikka 1,199 / 1,799 / 2,399; Crown Crust and Kabab Crust 1,299 / 1,899 / 2,399.
- New (hero slide): "NEW PIZZA & BIHARI ROLL! Taste the Best New Arrivals in Town." Bihari Roll 2 pcs Rs. 380, 4 pcs Rs. 699.
- Other slides: "BAZUKA PLATTER One Platter. Endless Cravings." (Rs. 2,099), "THE CROWN OF Cheesy Perfection",
  "KABAB INSIDE Party Outside". Nowshera branch "OPEN NOW" banner (new branch).
- Logo tagline: "Best Taste In Your Town".
- No promo code / offer API data on 2026-10-25.

## Do NOT claim without asking the client (see site-data.md contradictions)
Opening hours (11 AM-2 AM vs FAQ 11 AM-11 PM, and "closed right now" at 5 PM Sunday), card/online payment, delivery
minutes, dine-in, thin/stuffed crust, delivery areas inside the cities, branch phone numbers other than the main line.

## Images (main-session rule, 2026-10-25)
Photos are NOT kept in git on main (CLAUDE.md: never commit photos). Re-download the site's food/banner/logo images
for each job into the scratchpad from the URLs in `site/images.json` (or re-run crawl.js); paths below are the file
names those URLs give.

## Brand
- Red #D80101 (site buttons), banner deep red ~#980000-#A00000 + yellow ~#F8C000, white. Font Poppins (site CSS).
- Logo `assets/brand/1768998138-logo--60-.png` (600x600, red/yellow wordmark on white circle).
- Food photos: `assets/food/` (60 item photos; NOT transparent: food on a solid #A50000 red background, measured 2026-10-25, good for
  push-ins over brand-red backgrounds; deal photos are the client's own price posters). Category banners and hero
  slides: `assets/banners/`. `site/images.json` maps every file to its item/category and source URL.
- Not committed (people in the photo): Nowshera "OPEN NOW" banners (URLs listed in site/images.json).

## Voice
Default free voice (CLAUDE.md "DEFAULT VOICE"): `library/tools/vs_tts.py` (VoxCPM2). No ElevenLabs.

## Delivery rule for this client
New, unpaid client: ask the owner per job whether to send a watermarked preview (library/tools/watermark.py) or the final.
