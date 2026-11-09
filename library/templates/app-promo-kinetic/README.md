# app-promo-kinetic (problem -> solution app promo, 16:9 + 9:16)

First used: AI Video Automator (app.talkember.site / video.talkember.site, the owner's own product), 2026-11-09.
Built after three owner reference TikToks (frames read with a Playwright seek script, scratchpad tt4.js pattern):
pastel kinetic type with two weights/colours + cut-out objects; a big outline word behind the subject; a SaaS promo with
a white rounded stage on a soft gradient, chapter tabs at the bottom (Intro / Problem / Use Case / Call to Action)
and phone mockups floating with UI chips.

`build.py CONFIG --format 16x9|9x16 --out PROJECT`. Scene kinds: hook (sentence + task chips), pc (old way: monitor
playing a clip, clock spinning, "PC ON" bar), reveal (logo burst + URL), default (kinetic lines + 3D phones with the
app's own screenshots + floating chips), end (logo, price, CTA URL, payment line). Chapter pill moves with `x`
(a `left` tween is a hyperframes check ERROR: gsap_non_transform_motion). Brand chip sits in the stage from frame 0.
Copy: brand tokens from the site CSS (primary #4f46e5, primary-2 #7c3aed, text #0f172a, muted #5b6475).

AI Video Automator facts used (read 2026-11-09): video.talkember.site home/pricing/download/refund (Windows 10/11,
8 GB RAM, 649 MB installer, plans Rs 100 / 500 / 1,000 / 10,000, JazzCash, Easypaisa, SadaPay, UPaisa) and the owner's
phone screenshots of app.talkember.site (Accounts, Autopilot ON 09:00-21:00, Channel Profile, Video banao 30 sec - 5 min,
Masla hal karein, daily report e-mail). E-mail fields blurred; a payment-methods screenshot was left out (card data).
ElevenLabs Viraj, eleven_v4, 12 lines: 64.96 s / 66.24 s per take, 915 credits each; Whisper medium heard every line
in take A, the closing URL only clearly in take B, so take A + take B's URL were spliced at a silence.
Music: CC0 Pantheon (HoliznaCC0), music_fit --end resolve, mix_vo_music -16 LUFS.

v2 (owner 2026-11-09: "video.talkember.site last me dekhao, YouTube ChatGPT Google Flow ka icon bhi use kro"):
config `icons` maps a chip name to a brand icon file; icons come from Simple Icons (CC0, cdn.jsdelivr.net/npm/
simple-icons@13.21.0/icons/<slug>.svg, checked 2026-11-09: youtube, openai, google, gmail exist; windows is NOT in
the set) recoloured with a `fill` attribute. The end card has `url2` (second site), `works` (icon row) and sits higher
in 16:9 (BASE = 4% of the stage) so all rows fit above the chapter tabs.
