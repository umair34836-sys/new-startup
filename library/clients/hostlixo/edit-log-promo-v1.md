# HostLixo 30 s promo v1: edit log (2026-10-27)

Owner's ask (2026-10-27): 30 s promotional video, facts only from hostlixo.in, real site elements over emojis,
professional promotional voice (not "default", no ElevenLabs), owner's copyright on it, skill-based editing.
Owner approved the script, picked voice sample A and watermark option (a) on 2026-10-27.

| Decision | Source (skill # / file) |
|---|---|
| Every fact from a full Playwright crawl of all 7 pages; lists grepped item by item | CLAUDE.md "MISSED OFFER", "MISSED FACT"; site-data.md |
| Intel/Ryzen/VPS, Mumbai, 99.99% SLA, latency ms left out (coming soon / contradictory / sample estimates) | site-data.md "Contradictions" |
| Type: product ad, 9:16, 15-30 s, hook 0-2 s -> benefits -> proof -> CTA last seconds | decision-guide.md #9 "Product ad / UGC ad" |
| Title on screen at 0 s (thumbnail), strongest question first, no logo intro | CLAUDE.md "HyperFrames learnings"; skill #100 "Cold open: strongest line first" |
| Template: hosting-promo-reel, new builder build_hostlixo.py (scene starts = VO line starts from lines.json) | library/templates/hosting-promo-reel/README.md (build_pakwebhoster.py, build_moradosolution.py) |
| Visual language copied from the site CSS: #050505 black, white type, #999 secondary, thin borders, Space Grotesk / Plus Jakarta Sans / JetBrains Mono, white primary button | brief.md "Brand"; skill client-brand-kit (colours/fonts from the client) |
| Real elements: site logo + mark, site images mc_world/mc_1/mc_2, real plans-grid screenshot, site DDoS card, terms-page refund badge, site's own inline SVG icons, footer payment badges | owner's ask; site/tools/shots.js; every image looked at before use (Korba learning) |
| Plans screenshot in a browser frame with a slow diagonal pan (two eased positions) | skill #155 "Ken Burns = two eased crop rectangles" |
| Must-read text kept between y 300 and ~1250 of 1920 | skill #393 "Safe zones for Reels/TikTok UI"; #3598 (Meta Reels margins) |
| Numbers / software names shown big on screen (TTS mispronounces numbers and names) | research/voicestudio.md (चौबीस heard wrong); CLAUDE.md PakWebHoster note |
| Voice: VoxCPM2 voice design -> ONE reference line -> every line cloned from it; 3 samples, owner picked A | research/voicestudio.md "Voice design per line ... different voice per line"; skill voice-or-song |
| Music: CC0 "It feels good to be alive too" (Loyalty Freak Music), from its first drop at 12.89 s (listen.py), bed 0.17 under VO, up to 0.45 for the end card | library/music/cc0/README.md; CLAUDE.md owner music rule; listen.py |
| SFX: whoosh on every scene change, pop on chips, cash-register on the price, impact on "24h", click + confirm on the CTA; levels 0.35-0.5 | skill stock-sfx-luts; CLAUDE.md "Mix levels that worked"; #2018 "Level SFX by loudness" |
| QA: hyperframes check, snapshots looked at, watch.py, listen.py (-14..-16 LUFS, 0 clipped) | CLAUDE.md QA rules; skill listen-and-watch |
| Copyright: watermark.py ("Made by MrCopper804" tiles + PREVIEW · © tag + metadata) | owner's choice (a); library/tools/watermark.py |
