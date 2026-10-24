# Client brand kit (HyperFrames)

Fill `brand.json` once per client, then every branded block is generated from it, so branding is never asked twice.
Keep the client's real `brand.json` + logo in the session scratchpad (client data is personal/business data: do not
commit it); only the FAKE example lives here.

| File | What |
| --- | --- |
| `brand.schema.json` | Fields: name, name_ur, tagline(_ur), logo, colors (primary/on_primary/secondary/on_secondary/accent/dark), fonts, phone, whatsapp, address, website, socials, language, tone, cta, offer |
| `brand.example.json` + `demo-logo.png` | FAKE "Demo Chai House" (placeholder phone 0300-0000000); `make_demo_logo.py` redraws the logo |
| `brand_from_logo.py logo.png [--write brand.json]` | k-means palette from the logo + text colour per colour with WCAG 2.1 contrast (PASS >= 4.5 normal, >= 3 large) |
| `build_brand.py brand.json <project> [--size 1920x1080]` | writes the blocks below + `assets/brand/qr.png` + a 16.5 s demo `index.html` |

Blocks (`compositions/`): `brand-sting` 3 s logo intro, `brand-lower` 4 s lower third, `brand-offer` 3 s price badge,
`brand-cta` 2.5 s "Abhi call karein" sticker + phone, `brand-end` 4 s contact end card with QR, `brand-bug` corner
watermark (host sets duration), `brand-bg` stand-in background for the demo.

Tested 2026-10-24 (HyperFrames 0.8.188), with the example + a test `name_ur` (`امن`, a word copied from the UDHR Urdu text):
- `check --json` ok for 1080x1920 and 1920x1080 (first version failed landscape: Urdu name overlapped the contact rows;
  fixed by flex-column layout for sting text and end card).
- Draft render 16.500 s; snapshots looked at for every block in both sizes.
- QR decoded with jsQR 1.4.0 both from `qr.png` and from a decoded video frame of the end card at 16.4 s:
  `https://wa.me/923000000000`. Link format from WhatsApp's FAQ (https://faq.whatsapp.com/425247423114725, read
  2026-10-24): full international number, no plus, dashes, brackets or leading zeros.
- `brand_from_logo.py demo-logo.png`: #8a3b12 (72.5%) text #ffffff 7.70; #fdf4e4 text #000000 19.24; #f1c04f text
  #000000 12.39. Formula check: white/black = 21.00, #777777/white = 4.48.
- Snapshot of the last frame (16.005 s) showed the end card column lower than at 15.5 s; the rendered video frames at
  14.0 / 15.5 / 16.4 s are identical in layout, so it is a snapshot-only difference.
Limits: the sting splits the name per word (safe for any script); long names (> ~18 Anton characters at 1080 wide) wrap to
two lines, check the snapshot. No audio in the blocks: add a whoosh/pop from the media-use SFX when using them.
