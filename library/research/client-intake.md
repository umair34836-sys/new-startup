# Client intake (one message, collect everything once)

Written 2026-10-24 for the brand kit (`library/templates/brand-kit`). The questions are our own wording;
every field maps to `brand.schema.json`. Client answers are client data: keep them in the session scratchpad,
never commit them.

## Message to send the client (Roman Urdu)

Assalam o alaikum! Aap ki video professional aur aap ke brand ke mutabiq banane ke liye yeh cheezein ek hi baar bhej dein:

1. Business ka naam (English spelling jaisa aap likhte hain) aur agar video mein Urdu/Pashto mein bhi chahiye to
   naam Urdu/Pashto likhai mein (khud type kar ke ya logo/board ki photo).
2. Logo: asal file (PNG, transparent background ho to behtar). WhatsApp photo ki jagah "document" bana kar bhejein
   taake quality kam na ho.
3. Brand ke rang: agar pata hain to color codes, warna "logo wale rang" likh dein.
4. Tagline / slogan (agar hai) aur kis zuban mein: Roman Urdu, Urdu, Pashto, Hindi ya English.
5. Phone number jo video mein dikhana hai, aur WhatsApp number (agar alag hai).
6. Address / location (jitna video mein dikhana hai).
7. Website, Instagram, Facebook, TikTok, YouTube handles.
8. Koi offer ya price dikhani hai? (offer ka naam, price, aakhri tareekh / sharait)
9. Call-to-action kya ho? (masalan "Abhi call karein", "WhatsApp karein", "Visit karein")
10. Video ka mood: premium, friendly, bold, family, funny?
11. Video kahan lagegi: Instagram Reel / TikTok (9:16), YouTube (16:9), WhatsApp status? Lambai kitni?
12. Koi cheez jo video mein bilkul NAHI honi chahiye (rang, lafz, kisi ka chehra, gaana)?
13. Video mein jo log ya jagah dikh rahi hai, kya unhon ne video public karne ki ijazat di hai?

Shukriya! Sab ek saath mil jaye to hum jaldi video bana dete hain.

## Checklist before a branded render (our process)

- [ ] `brand.json` filled; Urdu/Pashto text exactly as the client sent it (never transliterated by us; see
      `library/research/urdu-captions.md`); show the client a still of any Urdu/Pashto line to confirm.
- [ ] `python3 brand_from_logo.py logo.png` run; every text colour PASS (>= 4.5:1, or >= 3:1 for large titles).
- [ ] Phone/WhatsApp re-typed from the client's message, then read back on the end-card snapshot digit by digit.
- [ ] QR decoded from a rendered frame (jsQR) and it opens the right number/website.
- [ ] `npx hyperframes check --json` ok in the delivery size(s); snapshot at the middle of every block.
- [ ] Offer price, dates and conditions match the client's words exactly.
- [ ] Title or logo on screen at 0 s (first frame is the thumbnail: root CLAUDE.md HyperFrames learnings).
- [ ] Music/SFX need no credit (owner rule in CLAUDE.md).
- [ ] Deliver full quality + WhatsApp copy (recipe in CLAUDE.md).
