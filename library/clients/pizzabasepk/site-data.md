# Pizza Base PK: site data (https://pizzabasepk.com/)

Read in a real browser (Playwright Chromium, this container) on **2026-10-25, 11:59-12:21 UTC** (16:59-17:21 PKT,
a Sunday) with `crawl.js` + `crawl_items.js` (this folder). Nothing was ordered, no login, no form sent: only the
"Delivery / Pick-Up" + city selector was used to open the menu, and item popups were closed again.
Raw evidence: `site/text/*.txt` (rendered page text per order type x city), `site/items/<id>.txt` (rendered popup of
every item), `site/pages/` (FAQ, privacy policy), `site/net/*.json` (the JSON the page itself loaded from
console.indolj.io), `site/shots/*.jpg` (screenshots), `site/images.json` (every image URL -> repo file).

Platform: the storefront is "Powered by indolj" (footer link https://www.indolj.pk/). Merchant id 221465.

## Brand
- Name: **Pizza Base**. Logo tagline (in the logo image `assets/brand/1768998138-logo--60-.png`, 600x600): "Best Taste In Your Town".
- Colours (computed CSS on the home page): brand red **#D80101** (rgb 216,1,1: "Delivery" + "Select" buttons, white text);
  text #2E2E2E / #111827. Banner art (most common colours in the site's hero banners, measured here): deep red
  ~#980000-#A00000, yellow ~#F8C000, white.
- Font (computed `font-family`, `document.fonts` loaded): **Poppins** 400/500/600/700.
- Favicon: `assets/brand/_faviconMgOSNlLv17fKDG1q.png`.

## Contact (footer, every page; BranchDetails JSON)
- Phone (header + footer + every branch's `phone_number`): **051 111 121 222**
- Email (footer): info@pizzabasepk.com
- WhatsApp: link `https://wa.me/923114000029` on the menu page; BranchDetails `whatsapp_on_menu` = "923114000029" (all 6 branches).
- Socials (footer icons): Facebook https://www.facebook.com/pizzabasepk/ , Instagram https://www.instagram.com/pizzabasepk/ ,
  TikTok https://www.tiktok.com/@pizzabase.pk , Threads https://www.threads.com/@pizzabasepk (link present, no visible icon in the footer screenshot).
- Footer address (shown on every page, also before a city is chosen): "Takbeer Plaza In Front Of The City School, Takbeer Chowk, Kamra Rd, Attock".

## Cities and branches (city dropdown + Pick-Up branch dropdown + BranchDetails JSON)
Order types offered: **Delivery** and **Pick-Up** (selector modal). Cities in the dropdown, in site order:
Attock, Haripur, Wah Cantt, Hazro, Swabi, Nowshera.

| City | Pick-Up branch name (dropdown) | Address (BranchDetails `address`) | branch_id |
|---|---|---|---|
| Attock | Pizza Base Kamra Road Attock | Takbeer Plaza In Front Of The City School, Takbeer Chowk, Kamra Rd, | 44697 |
| Haripur | Pizza Base - Haripur | KKR, Awan Colony, Harīpur, Pakistan | 44724 |
| Wah Cantt | Pizza Base - Wah Cantt | Plot 18, Goraya's Arcade Civic Center, Wah Modal Town, Wah Cantt, Peshawar Rd | 44723 |
| Hazro | Pizza Base - Hazro | Toll Tax Chowk Tarbela Road Nartopa, Hazro | 44725 |
| Swabi | Pizza Base - Swabi | Jahangira Rd, Darra, Wadood Plaza, Swabi | 44726 |
| Nowshera | Pizza Base - Nowshera | Khsra No. 449, Al-Yaya Shopping Mall, Al-Yahya Shopping Mall, Khat Kalay, Nowshera, 24100, Pakistan | 46607 |

- Delivery areas: `GetAreasCityWise` returned no area list for any city (`"areas":{"<city_id>":false}`), so the site
  names no delivery areas beyond the six cities.
- Timings (BranchDetails `timings`, all 6 branches identical): every day Mon-Sun **11:00 AM - 02:00 AM**; pre-order 11:45 AM - 02:00 AM.
- Delivery / pick-up estimate (BranchDetails `delivery_est` / `pickup_est`): **45** (minutes) for every branch.
- Payment (BranchDetails): `has_active_offline_payment` true, `has_active_online_payment` false (all 6 branches).
- Offers / promo codes: `GetMerchantOffers` returned `details: null` for every branch and both order types;
  `GetActiveBanners` and `active-campaign-animations` empty; no promo code anywhere on the site (2026-10-25).
- Menu: the `StructuredMenu` JSON was identical (same items, prices, descriptions) in all 15 loads across all cities and
  both order types: one menu and one price list for every branch.

## Hero slider (home/menu page, 5 slides, `site/shots`, files in `assets/banners/`)
1. "OPEN NOW / NOWSHERA BRANCH / GREAT TASTE OPEN NOW" (storefront photo with people: NOT committed, see images.json)
2. "NEW PIZZA & BIHARI ROLL! Taste the Best New Arrivals in Town." (`1771417649-1771065304-Benners.jpg`)
3. "BAZUKA PLATTER One Platter. Endless Cravings." (`1771417644-...-Bazuka-banner.jpg`)
4. "THE CROWN OF Cheesy Perfection" (`1771417636-...-Crown--Curst-benner.jpg`)
5. "KABAB INSIDE Party Outside" (`1771417628-...-kabab-crust-benner.jpg`)
Nowshera branch also has a popup banner (BranchDetails `dynamic_popup_banner_branch_wise`) with the same "OPEN NOW
NOWSHERA BRANCH" art (people in photo: not committed).

## Site text (home, under the menu; also <title>)
- Title: "Order Delicious Pizza in Attock, Haripur, Wah Cantt, Hazro, Swabi, Nowshera | Hot & Fresh from Pizza Base"
- H2: "Perfectly Baked Pizza for Every Craving – Order from Pizza Base". Body: "...freshly made with premium ingredients and
  baked to perfection... Dine in, take out, or get it delivered hot and fresh to your doorstep... Order now and satisfy your cravings!"
- Search box placeholder: "Search for Bihari Roll..."

## Menu (rendered popups `site/items/<id>.txt`; every price below was found in the rendered popup: 0 mismatches)
Prices in PKR ("Rs." on site). Tax class "Default" 0.0000% (GetMerchantTaxClasses).

### Starters
Category banner: `assets/banners/1768919181-Starters.jpg`

| Item (id) | Description on site | Price(s) | Photo in repo |
|---|---|---|---|
| Bihari Roll (815513) | With a Secret Homemade Sauce. | 2 Pcs Rs. 380, 4 Pcs Rs. 699 | `assets/food/1771065830-Bihari-Roll.jpg` |
| Chicken Mughali Roll (811177) | (none) | 4 Pcs Rs. 599 | `assets/food/1769064308-mughlai-roll.png` |
| Chicken Tikka Roll (811180) | (none) | 4 Pcs Rs. 599 | `assets/food/1769064400-Tikka-roll.png` |
| Chicken Drum Stick (811185) | (none) | 6 Pcs Rs. 450, 12 Pcs Rs. 799 | `assets/food/1769064065-Chicken-drums-itcik.png` |
| French Fries (811186) | (none) | Rs. 280 | `assets/food/1769064188-French-Fries.png` |
| Finger Kabab (811187) | (none) | 4 Pcs Rs. 399 | `assets/food/1769064169-Fingetr-kabab.png` |
| Chicken Nuggets (811188) | (none) | 5 Pcs Rs. 399 | `assets/food/1769064093-Chicken-Nugge5ts.png` |
| Cheese Sticks (811189) | (none) | 4 Pcs Rs. 340 | `assets/food/1771065263-chese-stick.jpg` |
| Supreme Bread (811190) | (none) | 4 Pcs Rs. 330 | `assets/food/1769264726-Supreme_bread.jpg` |
| Garlic Bread (811191) | (none) | 4 Pcs Rs. 270 | `assets/food/1769064210-Garlic_bread.png` |
| Chicken Potato Skin (811192) | (none) | 4 Pcs Rs. 350 | `assets/food/1779456242-ChickenPotatoSkin.jpeg` |

### Daily Base Deals
Category banner: `assets/banners/1769264467-Daily-Base.webp`

| Item (id) | Description on site | Price(s) | Photo in repo |
|---|---|---|---|
| Deal 1 (811052) | 1 Pan Pizza 1 345ml Drink | Rs. 650 | `assets/food/1786801448-WhatsAppImage2026-08-15at6.22.06PM1.webp` |
| Deal 2 (811053) | 1 Regular Pizza 2 345ml Drinks | Rs. 1,199 | `assets/food/1786801463-WhatsAppImage2026-08-15at6.22.07PM.webp` |
| Deal 3 (811054) | 1 Large Pizza 1 1.5 Liter Drink | Rs. 1,750 | `assets/food/1786801476-WhatsAppImage2026-08-15at6.22.07PM1.webp` |
| Deal 4 (811055) | 1 Jumbo Pizza 1 1.5 Liter Drink | Rs. 2,099 | `assets/food/1786802194-WhatsAppImage2026-08-15at6.22.08PM.webp` |

### Super Base Deals
Category banner: `assets/banners/1769241098-Super.jpg`

| Item (id) | Description on site | Price(s) | Photo in repo |
|---|---|---|---|
| Deal 1 (811062) | 2 Pan Pizza | Rs. 1,050 | `assets/food/1773298546-Superbase1.webp` |
| Deal 2 (811082) | 2 Regular Pizza | Rs. 1,999 | `assets/food/1773298561-Superbase2.webp` |
| Deal 3 (811083) | 2 Large Pizza | Rs. 2,899 | `assets/food/1773298576-Superbase3.webp` |
| Deal 4 (811084) | 2 Jumbo Pizza | Rs. 3,399 | `assets/food/1773298709-Superbase4.webp` |

### Teen Ka Scene Deals
Category banner: `assets/banners/1769241128-Teen-ka-scene.jpg`

| Item (id) | Description on site | Price(s) | Photo in repo |
|---|---|---|---|
| Deal 1 (811056) | 3 Pan Pizza | Rs. 1,299 | `assets/food/1783432542-WhatsApp-Image-2026-07-07-at-6-30-17-PM--1-.jpeg` |
| Deal 2 (811057) | 3 Regular Pizza | Rs. 2,499 | `assets/food/1783432571-WhatsApp-Image-2026-07-07-at-6-30-16-PM.jpeg` |
| Deal 3 (811058) | 3 Large Pizza | Rs. 3,699 | `assets/food/1783432596-WhatsApp-Image-2026-07-07-at-6-30-16-PM--1-.jpeg` |
| Deal 4 (811059) | 3 Jumbo Pizza | Rs. 4,799 | `assets/food/1783432610-WhatsApp-Image-2026-07-07-at-6-30-17-PM.jpeg` |

### Time Offer Deals
Category banner: `assets/banners/1769241179-Time-offer.jpg`

| Item (id) | Description on site | Price(s) | Photo in repo |
|---|---|---|---|
| Deal 1 (811060) | 1 Regular Pizza  4 Pcs Kabob, 2 345ml Drinks | Rs. 1,399 | `assets/food/1786801330-WhatsAppImage2026-08-15at6.22.06PM.webp` |
| Deal 2 (811061) | 1 Large Pizza  6 Pcs Wings, 1 1.5 Liter Drink | Rs. 1,999 | `assets/food/1786801339-WhatsAppImage2026-08-15at6.22.05PM.webp` |

### Pizza
Category banner: `assets/banners/1768919151-pizza.jpg`

| Item (id) | Description on site | Price(s) | Photo in repo |
|---|---|---|---|
| Grilled Black Pepper Tikka (815516) | with Tarragon Sauce | Regular Rs. 1,199, Large Rs. 1,799, Jumbo Rs. 2,399 | `assets/food/1771066087-GRILL-BLACK-PEPER-TIKKA.jpg` |
| Crown Crust (811428) | (none) | Regular Rs. 1,299, Large Rs. 1,899, Jumbo Rs. 2,399 | `assets/food/1774535203-crownpizza.jpeg` |
| Kabab Crust (811429) | (none) | Regular Rs. 1,299, Large Rs. 1,899, Jumbo Rs. 2,399 | `assets/food/1769064234-kabab-Crust.png` |
| Chicken Mughlai Base (811085) | Onion, Capsicum, Mughlai Chicken Top With Garlic Creamy Sauce And Cheese. | Small Rs. 899, Regular Rs. 1,799, Large Rs. 2,399, Jumbo Rs. 2,799 | `assets/food/1768923008-Mughlai.png` |
| Chicken Supreme Base (811086) | Red Sauce, Onion, Capsicum, Black Olive And Mushroom, Tikka Kabab And Spicy Chicken And Cheese. | Small Rs. 899, Regular Rs. 1,799, Large Rs. 2,399, Jumbo Rs. 2,799 | `assets/food/1768923073-Supreme-base.png` |
| Chicken Arabian Base (811087) | Red Sauce, Onion, Capsicum, Olives, Mughlai Chicken Top With Garlic Ring And Cheese | Small Rs. 899, Regular Rs. 1,799, Large Rs. 2,399, Jumbo Rs. 2,799 | `assets/food/1768815514-chicken-supereme_1_.webp` |
| Chicken Creamy Base (811088) | Creamy Sauce, Jalapeno, Mushroom, Spicy Chicken And Cheese. | Small Rs. 899, Regular Rs. 1,799, Large Rs. 2,399, Jumbo Rs. 2,799 | `assets/food/1783432408-WhatsAppImage2026-07-07at6.49.41PM.jpeg` |
| Tandoori Hot (811089) | Onion, Green Pepper, Jalapeno, Tandoori Tikka Creamy Sauce And Cheese. | Small Rs. 899, Regular Rs. 1,799, Large Rs. 2,399, Jumbo Rs. 2,799 | `assets/food/1768923117-Tandoori.png` |
| Fajita Sicilian (811115) | Onion, Capsicum, Jalapeno, Spicy Chicken And Cheese. | Small Rs. 899, Regular Rs. 1,799, Large Rs. 2,399, Jumbo Rs. 2,799 | `assets/food/1768816450-fajita-pizza-32.webp` |
| Fajita Chicken (811116) | Red Sauce, Onion, Capsicum, Spicy Chicken And Cheese. | Small Rs. 899, Regular Rs. 1,799, Large Rs. 2,399, Jumbo Rs. 2,799 | `assets/food/1768816556-fajita-pizza.webp` |
| Chicken Tikka (811117) | Red Sauce, Onion, Tikka Meat And Cheese. | Small Rs. 899, Regular Rs. 1,799, Large Rs. 2,399, Jumbo Rs. 2,799 | `assets/food/1768922780-Chicken-Tikka.png` |
| Chicken Turkish Base (811118) | Red Sauce, Fajita Chicken, Onion, Green Pepper, Mushrooms Top With Turkish Sauce And Cheese. | Small Rs. 899, Regular Rs. 1,799, Large Rs. 2,399, Jumbo Rs. 2,799 | `assets/food/1768923151-Turkish-base.png` |
| Chicken Rich Creamy (811121) | Onion, Chicken Tikka, Creamy Sauce And Cheese. | Small Rs. 899, Regular Rs. 1,799, Large Rs. 2,399, Jumbo Rs. 2,799 | `assets/food/1768923037-Rich-Creamy.png` |
| Chicken Achari (811124) | Creamy Sauce, Onion, Green Pepper, Spring Onion, Tandoori Chicken, Creamy Sauce And Cheese. | Small Rs. 899, Regular Rs. 1,799, Large Rs. 2,399, Jumbo Rs. 2,799 | `assets/food/1769000572-Chicken-Achari.png` |
| Hot & Spicy (811130) | Red Sauce, Onion, Jalapeno, Tomato, Chicken Kabab And Cheese. | Small Rs. 899, Regular Rs. 1,799, Large Rs. 2,399, Jumbo Rs. 2,799 | `assets/food/1769000591-Hot-and-Spicy.png` |
| Spicy Italian (811131) | Red Sauce, Onion, Capsicum, Jalapeno, Spicy Chicken, Olives And Cheese. | Small Rs. 899, Regular Rs. 1,799, Large Rs. 2,399, Jumbo Rs. 2,799 | `assets/food/1771065257-SPICY-ITALIAN.jpg` |
| Chicken Kabab (811132) | Red Sauce, Kabab Meat, Mushroom, Jalapeno And Cheese. | Small Rs. 899, Regular Rs. 1,799, Large Rs. 2,399, Jumbo Rs. 2,799 | `assets/food/1768922738-Chicken-Kabab.png` |
| Seekh Kabab (811137) | Red Sauce, Onion, Spring Onion, Tomato, Seekh Kabab Chunks And Cheese. | Regular Rs. 1,799, Large Rs. 2,399, Jumbo Rs. 2,799 | `assets/food/1768922970-kabab.png` |
| Euro Base (811143) | Red Sauce, Capsicum, Mushroom, Tomato, Olives, Afghani Kabab Meat And Cheese | Small Rs. 899, Regular Rs. 1,799, Large Rs. 2,399, Jumbo Rs. 2,799 | `assets/food/1768922910-Euro-Base.png` |
| American Hot (811146) | Red Sauce, Pepperoni, Jalapeno, Cheese. | Small Rs. 899, Regular Rs. 1,799, Large Rs. 2,399, Jumbo Rs. 2,799 | `assets/food/1769000608-Hot-amrecain.png` |
| Cheese Lover (811153) | 100% Topping Cheese And Red Sauce. | Small Rs. 899, Regular Rs. 1,799, Large Rs. 2,399, Jumbo Rs. 2,799 | `assets/food/1768922813-Chese-lover.png` |
| Veggie Lover (811154) | Spring Onion, Capsicum, Olives, Jalapeno, Mushroom, Tomato Red Sauce And Cheese. | Small Rs. 899, Regular Rs. 1,799, Large Rs. 2,399, Jumbo Rs. 2,799 | `assets/food/1768923176-Vegy.png` |

### Platters
| Item (id) | Description on site | Price(s) | Photo in repo |
|---|---|---|---|
| Bazuka Platter (811423) | 4 Pcs Mughlai Rolls  4 Chicken Cheese Bread  4 Pcs Cheese Potato Skin  4 Pcs Chicken Drumstick  4 Pcs Nuggets, 4 Pcs Finger Kabab  French Fries With Dip Sauce | Rs. 2,099 | `assets/food/1769000560-Bazuka.png` |
| Base Platter (811182) | (none) | Rs. 680 | `assets/food/1769264325-Base-platter.webp` |

### Sandwiches
Category banner: `assets/banners/1768919190-Sandwiches.jpg`

| Item (id) | Description on site | Price(s) | Photo in repo |
|---|---|---|---|
| Chicken Sandwich (811194) | (none) | Rs. 630 | `assets/food/1769064124-Chicken-Sandhwich.png` |
| Base Made Sandwich (811195) | (none) | Rs. 599 | `assets/food/1769264407-Base-amde-sandwich.webp` |

### Pasta
Category banner: `assets/banners/1768919201-Pasta.jpg`

| Item (id) | Description on site | Price(s) | Photo in repo |
|---|---|---|---|
| Alfredo Pasta (820767) | (none) | Rs. 850 | `assets/food/1779260810-ChickenAlfredoPasta.jpeg` |
| Supreme Primavera (811196) | (none) | Rs. 730 | `assets/food/1769264363-Supreme-Primavera.webp` |
| Chicken Pasta (811197) | (none) | Rs. 730 | `assets/food/1769064037-Chicekn-pasta.png` |
| Creamy Lasagne (811198) | (none) | Rs. 730 | `assets/food/1769064283-Lagsania.png` |
| Chicken  Lasagne (811199) | (none) | Rs. 730 | `assets/food/1769264343-chicken-lasagne.webp` |
| Chicken Cheese Fries (811200) | (none) | Rs. 580 | `assets/food/1769064633-Chese-fries.png` |

### Beverages
Category banner: `assets/banners/1769241074-Beverages.jpg`

| Item (id) | Description on site | Price(s) | Photo in repo |
|---|---|---|---|
| Soft Drinks (811211) | (none) | 345ml Rs. 80, 1.5 Liter Rs. 199 | `assets/food/1769264090-Soft-Drink.webp` |
| Glass (811214) | (none) | Rs. 80 | `assets/food/1769264883-Glass.webp` |
| Mineral Water (811217) | (none) | 345ml Rs. 50, 1.5 Liter Rs. 100 | `assets/food/1769264528-Watar.webp` |

### Options shown in popups (StructuredMenu `addon_item`, also in the popup text)
- Deals: "Choose Your Pizza Flavor" (Required) from 19 flavours (Chicken Mughlai Base ... Veggie Lover, Seekh Kabab), +Rs. 0;
  "Choose Your Soft Drink": Pepsi, 7up, Mirinda, Dew (+Rs. 0). Deal popups show a "Most Popular Combo" (e.g. Chicken Mughlai + Pepsi).
- Extra toppings (Chicken, Cheese, Olives, Jalapeno, Mushroom, Onion, Green Pepper, Pepperoni), price by size:
  Small 100/100/60/60/70/20/30/120; Regular 180/180/100/100/100/40/50/150; Large 250/250/170/170/160/80/100/180;
  Jumbo 320/300/220/220/230/100/120/220 (Chicken/Cheese/Olives/Jalapeno/Mushroom/Onion/Green Pepper/Pepperoni).

### Deal posters (the item photos themselves are price posters, text matches the JSON)
Daily Base Deal 1-4 (650 / 1199 / 1750 / 2099), Super Base Deal 1-4 (1050 / 1999 / 2899 / 3399), Teen Ka Scene 1-4
(1,299 / 2,499 / 3,699 / 4,799), Time Offer 1-2 (1399 / 1999). Files in `assets/food/` (see table).

## Contradictions / things to confirm with the client
1. **Hours**: BranchDetails says every day 11:00 AM - 02:00 AM, but the FAQ says "Generally, we deliver from 11:00 AM to
   11:00 PM daily". And at 17:00 PKT on Sunday 2026-10-25 (inside both ranges) the checkout status for every branch was
   "Sorry, we are closed right now. We will open on Mon 11:00 am". Don't put hours in a video without asking.
2. **Payment**: FAQ says "Cash on Delivery (COD), Credit/Debit Cards, and various digital payment methods including mobile
   wallets"; BranchDetails: online payment inactive, offline active (all branches).
3. **Delivery time**: FAQ "30-45 minutes"; branch estimate 45 for all. Use "45" only if needed, or nothing.
4. **Dine-in**: the home text says "Dine in, take out, or get it delivered" but the selector offers only Delivery and Pick-Up.
5. **Thin / stuffed crust**: the home text mentions "a crispy thin crust, a cheesy stuffed crust"; the menu has no thin-crust
   item or crust option; crust items are Crown Crust and Kabab Crust.
6. **FAQ is generic platform text** ("Sign Up", "live chat", "SMS and email tracking", "vegetarian label", "allergen
   information"): none of these were visible on the site. Don't quote the FAQ.
7. **Footer address** is always the Attock branch, even after choosing another city; Attock branch latitude/longitude are 0.
8. Spellings on site: "Chicken Mughali Roll" (starter) vs "Chicken Mughlai Base" (pizza); "Kabob" in Time Offer Deal 1
   text vs "Kabab" elsewhere; Nowshera address "Al-Yaya" and "Al-Yahya" in one line.
9. Item JSON field `not_available` = "1" on every item although all items show prices and open normally: meaning unknown (unverified).
10. Nowshera "OPEN NOW" banner image shows "051-111-12-12-22" (same digits as 051 111 121 222); the storefront sign in that
    photo reads like "051-111-421-222" (low-res, unverified).
11. Privacy policy mentions "Make a reservation" and "newsletter": not offered anywhere on the site.

## Pages that exist (all links found on the site)
https://pizzabasepk.com/ (menu), /product/<item-slug> (item popup URL), /pages/privacy-policy, /pages/faqs.
No about, contact, branches or blog page is linked. The FAQ page has a "Contact Us" button; no contact-page URL appeared among the page links (`site/links.txt`).
