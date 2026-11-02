# GOOD's promo v1 (English + Hinglish, 9:16 + 16:9, 48.7 s): edit log (2026-11-02)

Template: library/templates/exchange-promo (new, built from site-panel-reel). Every decision below names its source.

| Decision | Source |
|---|---|
| Facts only from goodss.store (Playwright render) + Discord invite API, dated; risky claims left out (100% track record, 2000+ clients, $60,000+, 99.97% uptime, reviews, "financial advice", "best rates", "zero hidden fees") | site-data.md; brief rules; CLAUDE.md VERIFIED ONLY; Hallmark gate 46a |
| Type: app/website promo, real site walk-through, title on screen at 0 s | decision-guide #26; CLAUDE.md HyperFrames learnings |
| Real recordings with cursor + ripple on every click (rate tabs PKR / CRYPTO / BINANCE GIFT, calculator PKR -> crypto, 32,500 typed -> $100.00 shown by the site) ; form never filled | OWNER RULE tutorials; screen_recorder.js |
| Discord scene = client's banner GIF + member count (3,532 on 2026-11-02, shown as "3,500+") instead of a recording: Discord's web invite page shows a register form | invite API; seen in recording 2026-11-02 |
| Client's animated logo GIF opens (started at 1.8 s of the GIF, where the G is formed, so frame 0 works as thumbnail) and closes the video | CLAUDE.md "first frame is the thumbnail"; snapshot 2026-11-02 |
| Voice explainer-pro (owner's choice), English `--lang en`, Hinglish Devanagari `--lang hi`, 0.7 s gaps | brief owner answers; voices README |
| Whisper small per line, read the heard text: EN line 1/12 "GOOD's" heard "Go dozi" -> retake written "Goods" (seed 21, heard "goods where trust is built"); HI lines 1/12, 9, 11 retaken seed 21 (better); HI line 4 retake lost "swap" -> original kept | CLAUDE.md "read the HYP text"; wcheck |
| Brand/URLs/numbers on screen (goodss.store, discord.gg/goods, 7 currency codes with the site's own flags, $100 example) | CLAUDE.md PakWebHoster/AethelGrid TTS notes |
| Music: CC0 "Monarch of the Street" (Loyalty Freak Music): find_music rank 1 for hosting-tech/promo + VO; 99 BPM, steady grid (CV 0.012), full sound by 1.24 s, LRA 1.7 LU (steady under VO), real ending; D minor = serious tone for a money brand. Rejected: People Are Spinning (slow intro 19 s, already used for AethelGrid), Pantheon (fade-out ending) | skill music-for-video; find_music.py; listen.py |
| music_fit --length 48.7 --end resolve: [0-47.3 s] + ending [222.13-223.53], join phase error 11.5 ms (tracker noise 20 ms); 47.5 s tried first: 57 ms, rejected | music_fit --check |
| mix_vo_music: VO at 0.5 s, duck -10 dB, music_vs_vo_gap 15.0 LU | skill music-for-video step 6 |
| OWNER RULE 2026-11-02 "ai jaise flow nhi, repeated sfx mat": whoosh only on 3 real picture changes (logo->site, site->Discord card, ->end card), each a different file; every click its own click file; no pops on chips; one coin sound on the calculator result; one soft thud on the first logo frame; builder asserts no SFX file repeats | skills #147, #2032; Mr Aloo feedback 2026-10-28 |
| Scene entries vary (top drop / gold bar rise / slide from left / clip wipe), no exit fade on every scene: plain cuts | #147; owner rule |
| Hallmark floor: Outfit (site's own font) display, headlines one colour, no eyebrow/tracked-caps labels, no purple/cyan gradient, gold bar the only accent, cards over real recordings; 16:9 s2 has no overlay so two headlines never share a frame | .claude/skills/hallmark references/gates.md section 4 |
| hyperframes check fixes: note text 26 -> 30 px (type floor 28), notes shortened to be readable in their time, contact chips cut to 3, Hinglish s10 overlap fixed | hyperframes check 2026-11-02 |
| Veil strengthened after snapshots showed site text ghosting behind headlines; 16:9 veil 500 px so the recording stays visible | snapshots 2026-11-02 |
| Preview: watermark.py (owner chose watermarked preview), credit "Edited by MrCopper804" on the end card | brief; CLAUDE.md secrecy rule |
| Recording spans start after the smooth scroll settles (~4 s): starting at 2.0-2.4 s showed the page top + a near-black mid-scroll frame | blackdetect 25.63 s (first render) |
| Slow eased push-in (3.5-6%, smoothstep) on scenes whose screen holds still | watch.py frozen spans 2-3 s; skill #154 |
| Discord card banner visible from frame 1 (a fade from opacity 0 made a 2-frame near-black cut); 16:9 s7 from 4.4 s | blackdetect 37.67 s / 25.2 s |
| Delivery: final = -map_metadata -1, yuv420p High, faststart; then remux with `-bsf:v filter_units=remove_types=6 -fflags +bitexact` so no encoder/software string stays in the file (strings: x264/Lavf 0) | CLAUDE.md client secrecy; measured here |

## QA (measured here 2026-11-02, delivered files)
| File | Size | LUFS | True peak | Black spans | Tags |
|---|---|---|---|---|---|
| English 9:16 | 1080x1920 48.7 s | -16.0 | -1.5 | 0 | 0 |
| Hinglish 9:16 | 1080x1920 48.7 s | -16.0 | -2.2 | 0 | 0 |
| English 16:9 | 1920x1080 48.7 s | -16.0 | -1.5 | 0 | 0 |
| Hinglish 16:9 | 1920x1080 48.7 s | -16.0 | -1.1 (listen.py: 0 clipped, LRA 3.9) | 0 | 0 |
watch.py (EN 9:16 earlier pass): real 30.0 fps, 0 gaps; "dark" = the site's navy design (expected).
Renders: ~2-3 min each with --workers 3.

## Thumbnails (skill thumbnail-design + Hallmark floor; thumb_make.py / thumb_check.py; scratchpad only)
- A "brand mark": navy single-hue gradient, client's G mark (Goood-store.png), "GOOD's" + "Currency & crypto exchange" /
  "Currency aur crypto exchange" in Outfit 800, slogan in gold. One colour per line (no accent word: Hallmark 38iii).
- B "product proof": real calculator frame zoomed 1.9-2.2x, darken 0.72 + blur 3 (first try showed the site's "100% track
  record" card behind the text: hidden), "See it before you send" / "Bhejne se pehle dekhein", gold box "32,500 PKR = $100",
  "Rates as of 2 Nov 2026" (thumb_check first flagged it 8-10 px at 320 wide: raised to 58-62 px).
- 16:9 1280x720 + 9:16 1080x1920 for each language = 8; all thumb_check "ok": true.
