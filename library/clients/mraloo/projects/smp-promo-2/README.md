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
| Guide export checklist: source is 60 fps -> clips cut at 60 fps and rendered with `-f 60` (a 30 fps render was stopped) | guide 6 "Source 60 FPS hai toh 60 FPS export" |
| Final QA (measured here 2026-10-28): A and B both 62.5 s, 1080x1920, 60 fps; -15.0 LUFS, peaks -1.2 / -1.1 dBFS; blackdetect (d 0.2, pix_th 0.10) + freezedetect (2 s) clean; Whisper medium on A's mix hears every line; Discord invite valid (discord.com API: "ALOO SMP ☀", no expiry, 660 members) and play.aloosmp.fun resolves (46.232.234.65) | delivered with SendUserFile: ALOO-SMP-Promo2-FINAL-A.mp4, ...-FINAL-B-alt-hook.mp4, thumbnail PNG (frame 1 s of A) |
| Disk: /tmp/hyperframes-extract-cache-0 held 1.7 GB from earlier renders; deleted before the 60 fps renders (A 9m56s, B 13m27s) | template minecraft-smp-short README note |

## v2 (2026-10-29): client's big-SMP clip
Client (via owner): "Bro shorts wale bade smp ke liye ek alag video dala tha". New Drive file "2026-10-28 21-52-40.mp4"
(1wLIJBx3gdu-5bHqWf3IRysKLVsYB3gTD, 335.5 s, 1080p60, 1.12 GB): client's own recording on OTHER big servers.
Contents (contact sheets, measured here): server list 0-6 (Wynncraft 1454/2000, MCPVP 1389/50000, then aloosmp + a "test"
row "Can't connect to server"), loading screens, Wynncraft 33-69, mc-complex lobby 87-99 ("SURVIVAL SMP (168 Playing)"),
tab list 108-111 ("1,511 Global • 168 Here"), lone survival in a forest 141-210 / 270-291, woodcutting 219-231, animals
240-258, heavy chat 294-312, snow 324-330.

| Decision | Source |
| --- | --- |
| Whole problem part (0 s -> "phir maine socha") re-cut from the new clip: lone player 156.4 / 282 / 165.5 / 175 / 199, lobby 96.5 / 99, tab list 109, forest wandering 227 for "karun to karun kya". ALOO SMP footage only from the solution on (v1 wrongly showed ALOO's own spawn as the lonely big server) | client note; edit logic "problem = other servers" |
| "itne saare servers": only the top two rows of the server list (crop 1440x548 at 240,0 over a darkened blur), because the rows below show ALOO SMP and a "Can't connect to server" line | snapshot 2026-10-29 |
| 220 s (dark log close-up) replaced by 227 s (forest, nothing to do) | snapshot 2026-10-29 |
| Hook B: lobby crowd (96.5) + tab list "1,511 Global" (109) under "1000 PLAYERS / 0 FRIENDS?" | client clip |
| Audio, captions, text and end card unchanged from v1 | — |
