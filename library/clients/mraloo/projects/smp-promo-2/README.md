# ALOO SMP Promo 2 (client job, 2026-10-28)
Client voice note (owner forwarded 2026-10-28, Whisper medium hi/en): new script + "aloosmp promo 2" VO in the main Drive
folder; use the old clips, different footage where possible; the client will shoot and upload a new clip for the bigger
SMP parts. Owner (asleep): "as a pro editor and repo se khud hi choose kar lena".
Inputs (Drive main folder 1HlOwa50KDkqBf0KIaCJnQ6JxjPTzB6gx): Aloo_SMP_Viral_Editing_Guide_Hinglish.pdf
(1Cjnx_kkYNrsXtzWj3LcIB_mBowd7dopL, copied here + editing-guide.txt), aloosmp promo 2.mp3 (1IYPtJ0SPgbFv5lb63zNKafOoBtpk30uB,
70.2 s), rec182 = 2026-10-25 20-34-02.mkv (1SmJKT0fOUn--o94gnSx_Pg3D4gq5wpwA, 182.6 s), spawn51 = 2026-10-25 20-24-48.mkv
(16nhkyo2QlKAAevAWaIz2osWhvI8kQOri, 51.0 s), emblem 1Lrh9ySfQthZ68dVMwWZaojNyjQm-8kyg.
Guide deliverable: 1 final 60 s 9:16 video + 1 alternate first-5-s hook (rest identical). Build: build/ (HOOK=B for the alt).

## Edit log (decision -> source)
| Decision | Source |
| --- | --- |
| VO: retake "yahan tum survival kar sakte ho" (32.96-35.4 s) dropped, second take kept; pauses > 0.40 s cut to 0.28 s (beats kept before "aur wahin se shuru hua" 0.45 s and the CTA 0.35 s); no speed change; high-pass 80 + loudnorm -16 -> 60.89 s. Whisper medium (en) re-check: every line present | guide 1 "dead air cut, repeated words", 5 "breaths ko completely remove mat karo", "voice ko fast karne ke bajaye..."; measured here |
| Music "High Technologic Beat Explosion" (Loyalty Freak Music, CC0, library/music/cc0; not the track of Short v1). listen.py: 140 BPM (conf 1.73), drop/chorus from 42.42 s. Placed so its drop lands on the spoken "ALOO SMP" (28.0 s); muffled (low-pass 900 Hz, -4 dB) through the problem part, opening across the beat shift ("phir maine socha") into the drop; 0.8 s comedic silence after "kisi ko jaante hi nahi ho"; 2 s fade at the end | guide 2 (beat hit on the reveal, music lifts gently 15-23 s), 3 (lyrics-free, CC0/licensed); owner rule CC0 |
| Mix (mix.py, same engine as the GTA video): music -20 dB under speech / -5 dB in gaps, SFX level-matched per type, master -15 LUFS / -1.5 dBTP. Measured: -15.0 LUFS, peak -1.5 dBFS; only the reveal boom (+4.2 dB over the voice p95) and the "apni story" punch (+2.7) stand out | guide 1 "voice sabse clear, music low, SFX short" |
| SFX: pop on frame 0 (hook B: record scratch), pop + punch on PLAYERS 1000 / FRIENDS 0, sad trombone cut to 1.0 s right after the joke, punch on "kya?", whoosh on the beat shift, riser + boom on the reveal, rotating pops (pop-high / bubble-pop / plop) on feature labels, level-up on "pehchaan", chime on JOIN, quiet pops on the end card | guide 3 table; client feedback on the GTA video (vary pop sounds) |
| Footage: 27 hard-cut shots, a new picture every 1-3 s, each matching its line (lonely player for the problem, busy spawn crowd for "hazaaron players", the real server list for "itne saare servers", the real "ALOO SMP >> Welcome" join message for "baaki players bhi join", shop with a player balance for economy, nametag with stats for "pehchaan", market for the CTA). Mostly rec182 0-135 s, which Short v1 did not use | guide 1-2; client "alag footage" |
| Avoided: tab list (rec 18-21.7), plugin-update chat (rec 6-24 except 21.8-22.6, checked every 0.2 s), YOU ARE AFK (rec 26-50), creative-mode chat (96-100), white frame (162) | contact sheets look/*.jpg, frame checks |
| 9:16 crop 608x1080 of the 1080p60 source + lanczos + cas 0.5; join message shown as whole frame over a blurred copy so it stays readable | CLAUDE.md (cas on 1.78x upscale), template minecraft-smp-short "fill" mode |
| Text per guide: SERVER MILA HI NAHI? on frame 0 (thumbnail), PLAYERS: 1000 / FRIENDS: 0 (about big servers, not a claim about ALOO SMP), TOH KHUD KA SMP BANAYA..., emblem reveal ~1.5 s, feature labels SURVIVAL / ECONOMY / PvP / CUSTOM ENCHANTS / FRIENDS KE SAATH (only what the VO says), APNA BASE / APNI TEAM / APNI PEHCHAAN, APNI STORY START KARO, JOIN ALOO SMP, end card IP play.aloosmp.fun + PORT 19132 (Bedrock) + JAVA + BEDROCK + Discord discord.gg/e89HSbjd5Y + "Link description mein", 7.5 s on screen | guide 2 + 4; brief.md (client data) |
| Captions: Hinglish Roman, 3-6 words, Jakarta ExtraBold 80 px with dark outline, gold keywords, centre-lower (y 1330, end card y 1420) | guide 4 |
| Alternate hook (B): opens on the busy spawn crowd with "1000 PLAYERS / 0 FRIENDS?" + record scratch, then the server list; from 5 s identical to A | guide "EDITOR DELIVERABLE" |
| Pending: the client's new clip for the bigger SMP parts (not received yet) | client voice note |
