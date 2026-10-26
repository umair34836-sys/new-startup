# ALOO SMP YouTube Short v1: edit log (2026-10-25)

Brief from the owner (2026-10-25): YouTube Short, ALOO SMP promotion, Hinglish (Roman Urdu) captions, use the files the
client sent, strong hook, no guesswork. Client gave IP play.aloosmp.fun, port 19132 (Bedrock), Discord discord.gg/e89HSbjd5Y.
Build script: kept in the session scratchpad with the media; its reusable pattern is described below.
Every decision -> where it came from.

## Checks before editing
| Decision | Source |
| --- | --- |
| listen.py on both MP3s + both videos, watch.py on both videos, contact sheets looked at | CLAUDE.md "Specialists" A, skill listen-and-watch, owner rule |
| Whisper medium (not small) with condition_on_previous_text=False for the VO | CLAUDE.md "Whisper on a long song misses whole sung stretches"; small dropped the last 28 s here |
| Discord invite valid (discord.com/api/v10/invites/e89HSbjd5Y: guild "ALOO SMP ☀", no expiry, 641 members, checked 2026-10-25); play.aloosmp.fun resolves (46.232.234.65) | VERIFIED ONLY rule |
| Server list frame (spawn video 1 s) shows "ALOO SMP / VANILLA SURVIVAL"; tab list (50 s) shows play.aloosmp.fun | looked at here |

## Voice
| Decision | Source |
| --- | --- |
| Use the client's own VO "smp promo.mp3", no new voice | CLAUDE.md "if a video the owner gives already has a voice, USE THAT VOICE" |
| No clean_voice.py: listen.py found no hum, no hiss, noise floor -89 dBFS | skill listen-and-watch ("hum/hiss -> clean") |
| Retakes: kept the 2nd take of "24x7 online" (Whisper mean word prob 0.84 vs 0.83, min 0.69 vs 0.52, "koi bhi" heard) and of "doston ke saath aao" (complete line); dropped the aborted 1st opening and "banao apna base" false start | skill #4 jump cut (cut mistakes instead of reshooting); measured here |
| Cuts placed inside silencedetect -45 dB gaps, 15/30 ms fades, 0.15 s between lines | CLAUDE.md "Patching one VO line" (splice at silences), skill #117 (few frames of audio crossfade prevent pops) |
| Cut the leading "to" so the Short opens on "Bhai agar tum Minecraft..." (cut at the -42 dB dip at 0.245 s; Whisper medium re-check: first word "बाई") | skill #99 hook in the first 3 s / start mid-action |
| VO loudnorm I=-16, TP=-1.5 (60.875 s) | CLAUDE.md "QA after render: VO loudnormed to -16" |

## Music and sound
| Decision | Source |
| --- | --- |
| Music "Monarch of the street" (Loyalty Freak Music, CC0, library/music/cc0): of 4 measured candidates the only steady grid (essentia conf 3.42 > 1.5), 99 BPM, -13 LUFS, full energy from 0 s | owner rule CC0 only; skill listen-and-watch "trust the grid when confidence > 1.5"; decision-guide section 12 Music |
| Music at volume 0.16 under the VO, rises to 0.45 after the last word with a 1.4 s fade | CLAUDE.md "Music under VO at volume 0.16 (-13 LUFS track) and VO -16 gave -16.0 LUFS"; "data-fade-out must start after the last spoken word" |
| SFX from library/sfx (CC0, index.json): whoosh on section cuts (peak placed on the cut using hit_s), pop on each feature chip, impact-boom on the logo and on "khatarnak player", impact-punch on "khatarnak PvP" and the NO WHITELIST stamp, game-coin on "economy"/"paise", level-up on "SMP journey shuru karo", chime on "join karo", sparkle on the Discord card, sub-drop on the hook | skill stock-sfx-luts; faceless section 17 ("whoosh on transitions, click on text pops"); memes.md rule 4-6 (SFX on the visual hit, 6-12 dB under the voice, not on serious lines) |
| SFX volumes 0.22-0.55 | CLAUDE.md "Mix levels that worked" (impact 0.35-0.4, whoosh 0.6-0.8, the 0.8-0.9 impacts were too loud) |
| Each SFX on its own audio lane | CLAUDE.md HyperFrames "overlapping clips need different data-track-index lanes" |

## Picture
| Decision | Source |
| --- | --- |
| 1080x1920, 30 fps, under 3 min (62.6 s) so YouTube files it as a Short; CC0 music only (no claim risk over 60 s) | skills #547, #3968, #3966 |
| Gameplay recomposed by full-height 9:16 crop; the "ALOO SMP >> Welcome" shot as whole frame over a blurred copy so the chat stays readable; no black bars | skills #163, #167, #168, #169 |
| Every shot shows what its VO line says (spawn flyover for the hook, shop rooms with a player's "$ 3.7M" for "player economy", market chests for "crates", the tab list of online players for "doston ke saath") | decision-guide section 17 Faceless ("cut to the voiceover, change the picture with purpose"; mistake: clips that loosely match) |
| A new shot every 1-2.5 s, cuts snapped to the music's beat grid nearest the phrase end | skill #96 shot budget; types/vertical.md "shots of 1-2 s"; CLAUDE.md "cut on bars" |
| Avoided: connecting screens, "YOU ARE AFK", plugin-update chat spam, the near-white 162.8 s frame, the black last second, crops with chat lines (hook moved 101.0 -> 102.8 s, shop 55.6/60.5 -> 63.0/66.0 s) | watch.py report + contact sheets; decision-guide section 12 mistakes |
| Dark shop shots (watch.py luma 50-70) brightened (eq gamma 1.28) ; first 3 shots +20% saturation | decision-guide section 12 "brighten night footage"; skill #5250 "pop in the first 3 seconds" |
| Hook: frame 0 = gameplay + "DHAASU INDIAN SMP / DHOONDH RAHE HO?" (the VO's own words), shake on "Indian" | CLAUDE.md "first frame is the thumbnail"; types/vertical.md "one bold line already on screen"; skill #99 |
| Logo reveal on the spoken "ALOO SMP": white flash, emblem scale-in, shake, boom | skill #122 (dip to white = impact), #161 (shake for impact) |
| Zoom-through blur only at section changes; hard cuts on the beat inside sections | template hosting-promo-reel enter_exit; skill #97 (interrupts must carry meaning) |
| Punch-in + shake on "khatarnak PvP" and "sabse khatarnak player" (meme format: zoom punch + SFX on the hit) | skills #150, #161; memes.md rule 4 |
| Feature chips appear on the spoken word (Survival, OP PvP, Mini games, Custom terrain, Custom enchantments, Khatarnak PvP, Spawner, Crates, Player economy, Apna base, Paise, Crates, OP items) | template hosting-promo-reel s3 chips |
| 24x7 ONLINE + NO WHITELIST stamp; JAVA + BEDROCK cards; end card emblem + IP + port + "ABHI JOIN KARO!" + Discord + "Link description mein", IP shown again for the last 3.3 s | client data; HyperFrames check line_unread (closing line >= 2 s) |
| Colours sampled from the emblem: gold #fcb43c, orange #fc9c24, ice #84ccfc/#cce4fc, navy #0c0c24 | skill client-brand-kit (brand colours from the client's own art) |
| Emblem as JPG (the PNG is 2.5 MB and has no transparency: 99.6% opaque pixels) | CLAUDE.md "An <img> over 2 MB isn't inlined: use JPG" |
| All text inside 168-1330 px; captions at y 1130 | types/vertical.md platform UI band; skill #166 |

## Captions (Hinglish / Roman Urdu)
| Decision | Source |
| --- | --- |
| 59 groups of 1-4 words, each word pops in at its own Whisper-medium start time, one gold word per group, white with navy stroke | CLAUDE.md "Captions: per-word ... one gold accent word per line"; captions.md (2-3 words for high energy, one group at a time, hard kill) ; memes.md rule 4 bold outlined caption |
| Words not shown because Whisper could not make them out clearly: "चुकाया" (7.4 s) and "लेते" (56.5 s) | VERIFIED ONLY rule ("unverifiable -> leave out") |
| Roman spellings follow the heard words (e.g. "der kis baat ka", "khatarnak", "khareedo") | owner: Hinglish captions |

## Not used, and why
- "Indian Gamers Ignore This Warning… Until It's Too Late.mp3": a different topic (PC security), not part of this promo.
- No copyrighted meme clips or sounds; no Vine Boom (memes.md rules 1, 3).
- No claims the VO does not make (no player counts, no prices).

## QA (measured here 2026-10-25)
| Round | Found | Fix |
| --- | --- | --- |
| v1 render | caption groups "yahan hai" + "custom" overlapped at 17.6 s; level-up (49.3 s) and sub-drop (2.8 s) 6 dB over the VO; owner name tag too close at 23.7 s | group end clamped to next group start (asserted); SFX levels lowered; shop in-point 63.0 -> 63.6 |
| v1 render (frames 39-62 s) | shot at 49 s opened on a wall in front of the camera | rec 178.0 -> 172.4 |
| v2 render | tab-list clip 1.03 s for a 1.21 s shot (0.17 s hold); Whisper medium on the mix: 157/157 words, all lines present | previous shot ends at 48.1; clip-length check added |
| v3 render | watch.py: footage scenes "soft" (9:16 crop = 1.78x upscale) | cas=strength=0.5 after lanczos (skill #489; Laplacian var 39 -> 62 on a test frame) |
| v4 render (final) | 62.6 s, 1080x1920, 30.0 fps real, 0 frame gaps, 0 black, 0 frozen spans; -16.1 LUFS integrated, 0 clipped samples; only 1 of 250 windows (39.25 s, whoosh + pop in a VO pause) over VO+4 dB; full 1.6 s contact sheet looked at | delivered |

Deliverables: ALOO-SMP-Short-FINAL.mp4 (200 MB, delivery quality) + ALOO-SMP-Short-WhatsApp.mp4 (CRF 23, 63 MB).

## v2 (2026-10-26): owner asked for the spawn video as overlays, then laptop + phone for Java/Bedrock
| Decision | Source |
| --- | --- |
| Server-list card (real "aloo / ALOO SMP / VANILLA SURVIVAL • Play Now!" entry, still from 0.5 s) on "kyunki aaj" | skills #439, #578; overlays.md; owner approved the mockup |
| Join sequence (Encrypting/Joining world -> "ALOO SMP >> Welcome") as PiP on "abhi server ko join karo"; logo steps aside, returns on "Discord" | same; owner approved the mockup |
| Laptop = JAVA, phone = BEDROCK with gameplay on the screens | minecraft.net article (library/research/minecraft-editions.md); laptop from templates/kinetic-laptop-type; skill #3107; owner approved the mockup |
| Not placed: top 168 px, chip sections, moving holograms | types/vertical.md; < 28 px readability |
| QA v6: 62.6 s, 30.0 fps, 0 gaps/black/frozen, -16.2 LUFS, 0 clipped, only the known 39.25 s window over VO+4 dB; full 1.6 s contact sheet looked at | measured here 2026-10-26 |
