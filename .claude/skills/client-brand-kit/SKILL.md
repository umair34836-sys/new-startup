---
name: client-brand-kit
description: Branded client videos without asking for branding every time - brand.json (name, Urdu name, logo, colours, fonts, phone/WhatsApp, address, socials, CTA, offer), logo palette with WCAG contrast, and HyperFrames blocks (logo sting, lower third, offer badge, "Abhi call karein" CTA sticker, contact end card with WhatsApp QR, watermark). Use for any client/business promo, reel, ad, or when the owner says "client ka logo/brand lagao", "end card banao", "contact details dalo".
---

# Client brand kit

Files and test results: `library/templates/brand-kit/README.md`. Intake message: `library/research/client-intake.md`.

1. If the client has no `brand.json` yet, send the owner the Roman Urdu intake message (client-intake.md) ONCE.
   Keep the client's brand.json + logo in the session scratchpad (client data, never commit).
2. `bash library/tools/setup-specialist-d.sh` (fonttools, numpy, pillow, qrcode) if not installed.
3. Copy `brand.example.json` to the scratchpad, fill it from the client's answers. Urdu/Pashto fields only as the
   client supplied them. `whatsapp` = the full number in international format, digits only (no plus, dashes,
   brackets or leading zeros, e.g. `923000000000`), because the QR is `https://wa.me/<whatsapp>` (build_brand.py;
   WhatsApp FAQ https://faq.whatsapp.com/425247423114725, read 2026-10-24). Colours: `python3 library/templates/brand-kit/brand_from_logo.py logo.png --write brand.json`
   (keeps other keys); use the suggested text colours (contrast PASS).
4. `python3 library/templates/brand-kit/build_brand.py brand.json <project> [--size 1920x1080]`.
5. In the project: `npx hyperframes check --json`, `snapshot --at` mid-point of each block, LOOK; decode the QR from a
   rendered frame (jsQR) before delivering.
6. To use blocks inside a real edit: copy the composition files + `assets/brand` + fonts, add hosts like the demo
   `index.html` (sting at 0 s for the thumbnail, bug over the footage, end card last), add SFX on pops/wipes.
