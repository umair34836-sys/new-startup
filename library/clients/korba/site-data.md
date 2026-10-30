# Korba Restaurant: facts from its website

Source site: https://korba-restaurant.localoria.com/ (+ /full-menu). Crawled in Chromium with `crawl.js` on
2026-10-26 (04:00 UTC). Only these two pages belong to Korba; every other link goes to Localoria or other listings.

IMPORTANT: the site is a **Localoria directory listing** (og:site_name "Localoria", footer "© Localoria 2026",
"Claim Your Listing"), not a site Korba built itself. Its text paragraphs are Localoria's write-up, not the
restaurant's own words. No JSON menu API: the only JSON the pages load is Google Maps/Places.
The site has **no videos** (no `<video>`, only a Google Maps iframe).

## Text facts (page: home `/`, 2026-10-26)
- Name: Korba Restaurant
- Address: "2X49V6Q, GT Rd, Khat Kalay, Nowshera, Pakistan" (Google Places JSON loaded by the page:
  "2X49+H53, Grand Trunk Rd, Khat Kalay, Nowshera")
- Phone: "+92 333 3443313"
- Category: "$$$ Restaurant", "(4431 Reviews)" (Places JSON the page loads: rating 3.9, 4685 ratings; not shown as text)
- Hours: Monday-Sunday "Open 24 hours" (the same block also shows a "Closed" status label: contradiction, see brief)
- Write-up (Localoria): along G.T. Road in Khat Kalay, Nowshera; "scenic views of the Kabul River"; separate
  areas for men and women; "elevated seating areas that overlook the river"; dishes named: BBQ platter, Fish Angara,
  Fried Fish, Mutton Karahi, "Korba Special Full Roasted Lamb", soups, salads.
- Highlights list: Has fireplace; Serves great coffee; Serves great dessert; Has great tea selection; Popular for
  lunch / dinner; Good for solo dining; Has all you can eat; Serves coffee; Serves halal food; Serves late-night food;
  Quick bite; Serves small plates; Serves vegan dishes; Serves vegetarian dishes; Serves breakfast / brunch / lunch /
  dinner; Has catering; Serves dessert; Has seating; wheelchair-accessible car park / entrance / seating / toilet;
  Free of charge street parking; Free parking lot; Plenty of parking.
- Reviews shown (6, names = public reviewers, not used in video): mention fried fish, angara fish, BBQ platter
  "huge quantity", river view, family area, "kids play area" (Saba Manzur, 13 Sep 2025).

## Text facts (page: `/full-menu`, 2026-10-26)
- Only a Localoria paragraph: BBQ platters, mutton karahi, chicken roast, fried fish, fish with lamb fat, soups
  (soup of the day), Russian salad, salad platters, green tea. No item list or prices as text.

## Images on the site (all `https://cdn.localoria.com/5335-*`, downloaded 2026-10-26, kept in scratchpad only)
| file | what it shows (looked at 2026-10-26) | use? |
|---|---|---|
| llphoto-1 (1200x675) | night exterior, "I ❤ KORBA" sign, "KORBA Cocktails & Juices", lit arch | yes, hero |
| llphoto-2 (675x1200) | a man in turban giving thumbs up, "Taim Alam / SUBSCRIBE" overlay (a YouTuber's frame) | NO (person + third-party overlay) |
| llphoto-3 (900x1200) | soup bowl with spoon | yes |
| llphoto-4 (900x1200) | night exterior, lights, "KORBA" sign, stairs; watermark "By Khalid Ur Rahman" (re-read 2026-10-26; first read "Ali" was wrong) | yes (watermark visible) |
| llphoto-5 (900x1200) | grilled fish on foil, chutney | yes |
| llphoto-6 (675x1200) | fried fish / tikka plate with chutney | yes |
| llphoto-7 (1080x810) | fried fish with lemon and salad | yes |
| llphoto-8 (1080x810) | decorated salad platter | yes |
| llphoto-9 (900x1200) | green tea cups on a table | yes |
| llphoto-10 (540x1200) | clay pot (matka) dish, low-res | yes (small) |
| llimg-menu-1,2,3,5,6,7,8,9 | photos of Korba's red/yellow printed menu card (prices "Excluded Tax") | yes (prices) |
| llimg-menu-4 | "Buffet & Iftar Ramadan Menu 2025" Korba flyer | old offer: do NOT advertise |
| llimg-menu-10 | flyer of a DIFFERENT business: "Istanbul", Al-Noor Plaza, Nowshera Road Mardan, 034-47826285 | NO (not Korba) |
| 5330..5334-llphoto-1, 28339..28343-llphoto-1 | other Localoria listings (related places) | NO |

## Menu card prices (read from the menu photos above, 2026-10-26; card date unknown, "Rs/- EXCLUDED TAX",
some prices hand-corrected; footer note in Urdu: KPRA tax and service charge apply on the bill)
From llimg-menu-6 ("Korba Specialities" / "Korba Special Platter"):
- Korba Special Full Lamb Steam (Per KG) - handwritten, unclear (2500 / 2400 crossed): do not quote
- Fish Sher Mahi Fried / Grilled (Per KG) - "????"
- Fish Angara Grilled, Local Fish (Special Recipe) (Silver, Grace, Rao, Masher) - 1400/-
- Fish Grilled, Local Fish (Per KG) - 900/-; Fish Fried, Local Fish (Per KG) - 850/-; Fish Tikka, Local Fish (Per KG) - 900/-
- Korba Special BBQ Platter (Full) (4-5 Person) - 8000/- (Rice, Chicken Tikka, Beef Kabab, Chicken Kabab, Chicken Boti,
  Malai Boti, Fish, Batair; 1 Kg Tikka, 1.5 Liter Drink)
- Special Platter (Half) - 4000/-
- BBQ Platter Regular (Full) (4-5 Person) - 5500/-; BBQ Platter Regular (Half) (2 Person) - 3000/-
- American Steak (Red Spicy Sauce) - Beef 1300/-, Chicken 1200/-
- "Matka Lamb Dum Pukht Per Kg Rs: 2500/-" (yellow box, bottom of the card)
From llimg-menu-7 (tawa deals):
- Chinese Tawa 8 Person - 7000/- (1 Egg Rice, 1 Chicken Manchurian, 1 Chicken Chilli Dry, 1 Chicken Chowmein,
  1 Chicken Lolly Pop, 1 Chicken Black Pepper, 1 Chicken Sechzwan, 1 Chicken Honey, 1.5 Liter Drink)
- Chinese + Pakistani Tawa 8 Person - 7000/- (1 Egg Fried Rice, 1 Chicken Vegetable, 1 Beef Chilli Dry, 1 Chicken Wings,
  1/2 Chicken Handi White, 1/2 Mutton Karahi, 1 Chicken Butter, 1.5 Liter Drink, 3 Naan, 1 Salad, 1 Raita)
- Mix Tawa 8 Person (Chinese Bar B Que + Pakistani) - 8000/- (1 Chicken Chilli Dry, 1 Chicken Manchurian, 1 Egg Rice,
  1 Chicken Honey Wings, 1/2 Chicken Handi, 1/2 Chicken Karahi, 1 Chicken Boti, 1 Chicken Malai Boti, 1 Beef Kabab,
  1.5 Liter Drink, 5 Naan, 1 Salad, 1 Raita)
- Contact on every card: 0315-9403090 | 0333-3443313 | 0923-560131
Other cards (menu-1,2,3,5,8,9: Pakistani foods, naan, beverages, desserts/ice cream, salad bar, BBQ chef's
specialities, Chinese cuisine) were looked at as thumbnails only; zoom in before quoting any line from them.

## From the Ramadan 2025 flyer (llimg-menu-4 footer, read 2026-10-26)
- 0923-560131; 0333-3443313 (WhatsApp icon beside it), 0315-9403090; www.facebook.com/korba.nsr
- Korba calligraphy emblem (white on navy) = the only logo-like mark on the site.
