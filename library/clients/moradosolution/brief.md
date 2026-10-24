# Client: MoradoSolution (game hosting, VPS, VDS, bare metal; India)

Deal done 2026-10-24 (owner). Everything below was read on the live sites on 2026-10-24 unless marked otherwise.
Re-read the site before every new video: prices and plans change.

**FULL SITE DATA (all 37 pages, plans, offer, contradictions): `site-data.md` beside this file** (crawl 2026-10-24,
raw page text in site/pages, screenshots in site/screens, brand images in assets/). Check it first; re-crawl only to diff.

## Sites
- Real site: https://moradosolution.in (owner chose this URL for videos). https://moradosolution.com showed only the
  DirectAdmin placeholder ("Something amazing will be constructed here...") on 2026-10-24.
- Panel: https://panel.moradosolution.com (linked from the .in site), VM panel https://vm.moradosolution.com,
  status https://status.moradosolution.com, Discord https://discord.gg/moradosolution (all linked from moradosolution.in).
- Fetching: plain curl got "Connection reset by peer" at times; a browser User-Agent + 3 retries worked.
  web_capture.py worked on moradosolution.in (homepage + /minecraft-budget).

## Facts used in the first reel (with the page they came from)
- "Minecraft Server Hosting in India" (home H1). "Zero swap, maximum performance." (home)
- AMD EPYC 7C13, DDR4 ECC, NVMe Gen 4, 10 Gbps uplink, "Always-on filtering", "Inline at the edge" (/infrastructure)
- Network: Frankfurt (Europe), Delhi (North India), Mumbai (West India), all "Operational" (/infrastructure);
  nav shows "DEL · BOM · FRA". Note: the /infrastructure FAQ says every node is in their own Delhi data centre: the
  page contradicts itself, so say only "servers in Delhi, Mumbai, Frankfurt" as the Network list does.
- "99.9% uptime target" (footer, every page); the nav card says "99.95% uptime": use 99.9% (footer) or ask the client.
- Every plan includes DDoS filtering (home); DDoS page: always on, included on every plan, no premium tier.
- Prices (home, 2026-10-24): Minecraft Starter ₹199, Stone ₹449, Gold ₹699 (Popular), Titan ₹1,599 /month;
  Hytale Starter ₹199, Standard ₹449, Pro ₹799 (Popular), Ultra ₹1,299; VPS 1 ₹676, VPS 2 ₹1,352, VPS 3 ₹1,690,
  VPS 4 ₹2,028. /minecraft-budget lists ₹199 up to ₹4,399. Rust, ARK, Valheim, Palworld: "Coming Soon".
- "Deploy in minutes" (/game-hosting), "support answered by humans" (footer). Sales page: no live promo code earlier on 2026-10-24; the later full crawl (same day) shows WELCOME30 = 30% OFF, see site-data.md.

## Brand
- Colours (site CSS): --bg #050505, text #f4f4f5 / #a2a2a8, cards #121215; accents from the logo: red #e11d48, blue #3b82f6.
- Font: Space Grotesk (site display font; library/fonts/SpaceGrotesk-Variable.ttf, OFL). Body: Inter.
- Logo: https://moradosolution.in/assets/moradosolution-logo-t.png (320x256, transparent),
  round dark icon https://moradosolution.in/assets/icon-512.png, OG cover https://moradosolution.in/assets/og-cover.png.
- Game art on the site: https://moradosolution.in/assets/games/minecraft-card.webp, hytale-card.webp.

## Voice (free, commercial-OK)
- VoiceStudio + VoxCPM2 (Apache-2.0) via library/tools/vs_tts.py. Recipe that gave one consistent voice
  (median f0 151-238 Hz, close to the Viraj voice's 172 Hz): reference line = voice design with
  --instruct "a young Indian man with a deep, confident, energetic voice, speaking Hindi like a TV advertisement"
  --seed 7 on the text "Deploy minutes में, और support इंसानों से."; then every line cloned from it with
  --ref ref.wav --ref-text "Deploy minutes में, और support इंसानों से." and the script fully in Devanagari.
  Whisper-check each line (vo check script pattern: library/tools/wcheck_lines.py); one line needed a second seed (21).
- Never commit the reference wav (voice recording rule): regenerate it from the recipe above.

## Delivered
- 2026-10-24: 9:16 promo reel, 32.1 s, Hindi VO (FINAL clean + WhatsApp copy, -14.9 LUFS, 30 fps), built with
  library/templates/hosting-promo-reel/build_moradosolution.py (8 scenes: hook, brand, hardware, DDoS, locations,
  ₹199 price, deploy/support, end card moradosolution.in + discord). A 64 s song version (ACE-Step seed 21) was
  previewed only.
- Before payment: preview with library/tools/watermark.py; after payment: clean file (owner rule).
