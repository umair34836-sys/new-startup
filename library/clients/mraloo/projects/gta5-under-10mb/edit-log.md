# GTA 5 FOR ANDROID UNDER 10 MB?! - edit log (started 2026-10-28)

Build files live in the session scratchpad (`gta/proj/build.py`, `captions.py`, `mood_bed.py`); no media in git.
Every decision and its source:

## Voice
| Decision | Source |
| --- | --- |
| Client VO 453.5 s: retakes removed (best take of each line, see README "Retakes heard"), cuts at the quietest 10 ms within +-0.15 s, 15 ms fades, 0.25 s between lines, inner pauses > 0.35 s trimmed -> 355.6 s | decision-guide (explainer), skills #4 jump cut, #289 dialogue compression; measured here |
| Tempo 1.15x with rubberband (pitch kept) + loudnorm -16 -> 309.2 s (159 wpm) | owner chose "1.15x - 5:09" (2026-10-28); skills #188/#2348, #3864 |
| Word times moved to the new clock through the cut map (orig -> new every 10 ms) / 1.15 | measured here |
| Whisper medium on the final VO (2026-10-28) found two retakes still in: "haan ek baat samajhna zaroori" twice (191.7 / 193.9 s) and "bhai YouTube thumbnail" twice plus a lone "bhai" (252.4-256.6 s). Kept the later take of each, cut at the quietest 10 ms (cut2.py) -> 302.65 s; re-checked with Whisper (en + small hi passes) that both lines are whole | VERIFIED ONLY rule; measured here |
| Caption "kisi ke paas GTA V Ultra Lite hai": Whisper heard "के बाद" / "kisi ka bha" (hi / en); the client script line is "kisi ke paas GTA 5 Ultra Lite". One word before "cloud gaming" (~264.7 s) stayed unclear in three passes ("legendary", "लेजरी", "लैजीरी") and is left out of the caption | VERIFIED ONLY (never invent words) |
| Music section times shifted with the cuts (mood_bed.py), stops kept before "lekin bhai" and the punchline | as above |

## Music and SFX
| Decision | Source |
| --- | --- |
| Bed by scene mood (guide: hook energetic, fake tutorial playful, permissions suspenseful, reality check light comedy, tips calm, roast dramatic build-up): Euphoria 0-27.5, silence for "lekin bhai...", Apocalyptic Echoes 33.3-43.4, Silly Snickerdoodle 43.4-101.8, Pouncin Bouncin 101.8-160.4, Demented 90s 160.4-215.4, On The Flip 215.4-276.5, Challenge Accepted 276.5-293.8, silence after the punchline, Euphoria 296.6-end. Owner's Drive YouTube Audio Library tracks (YouTube use only), loudnorm -14, 0.8 s crossfades, sidechain-ducked under the VO | editing guide "Background music"; owner allows YT Audio Library tracks; skills #316/#317 |
| SFX (library/sfx + library/memes/sfx, all CC0): record scratch on the scam reveal, Trevor and the fake thumbnail; tape stop on "lekin bhai"; impact boom on "SCAM" and "PROBLEM LEVEL BADHEGA"; magic shimmer on "digital jaadu"; thruster on the rocket; ba-dum-tss after the rishta joke; error on "bhai, ruk ja" (guide: funny Windows-style error); pops / whooshes only where something enters. Each placed by its measured peak (sfx_hits.json) | editing guide scenes 1-6 + "Har dialogue ke baad SFX mat lagana" |

## Picture
| Decision | Source |
| --- | --- |
| 53 shots, each cut in on the VO word it shows (words.json) | guide: "Har visual ko voice-over ke saath sync karna" |
| Frame 0 = title "GTA 5 FOR ANDROID UNDER 10 MB?!" over the first gameplay slot (thumbnail frame) | CLAUDE.md "first frame is the thumbnail"; guide "no long intro" |
| Google search = the client's own recording, cropped to the page (taskbar, tabs, URL bar and profile picture removed), time-fitted; "Gta 5 Download For Pc Highly Compressed" is a real result in that recording (zoom + underline on "highly compressed") | guide scene 2 |
| "GTA V Ultra Lite" result, APK download screen, install dialog and permission dialog are safe recreations labelled as such; fictional domain `random-website.example` (reserved domain); nothing downloaded or installed | guide: "Suspicious APK ko actually download ya install mat karna", "safe recreated results" |
| Risk wording says "ho sakta / kar sakte" (VO's own words), never "confirmed malware" | guide Important |
| 10 MB vs full game comparison uses the script's labels ("website ka promise" / "actual game data") and no number for the full game | guide: "Full game ka made-up exact file size mat likhna" |
| Wanted-level-inspired stars = plain outline stars of our own, not the game's HUD; fake thumbnail labelled "FICTIONAL THUMBNAIL" | guide scene 5/6 |
| NASA joke: Fluent 3D astronaut + rocket emoji (MIT) on a star field instead of a NASA photo | guide: "short astronaut/space meme" |
| Glitch bumpers on the three English headings the VO speaks (installation trap, doesn't make sense, how to stay safe) | client voice feedback on the last video (glitch + sound on topic change) |
| Hinglish captions (Roman) from the heard words, client script spelling where the VO says the same words; important words orange + 1.18x; dark band behind captions for the light Google page | guide "Captions"; captions.md |
| GTA 5 gameplay: 17 labelled slots (hook action, city wide, Franklin / Michael / Trevor, police chase, Minecraft resource pack...) until the client sends gameplay; never downloaded from YouTube | owner 2026-10-28 ("client se gameplay mangwa raha hoon"); CLAUDE.md copyright rule |

## QA
| Round | Found | Fix |
| --- | --- | --- |
| check 1 | 49 heavy-overlay elements (black-frame risk), video without id | linear gradients, no blur filters, hidden shots use display:none; ids |
| snapshots 1 | captions unreadable on the white-ish Google page, overlay text on the recording, circle off the Ultra Lite title, "FAKE?" stamp over "100% WORKING!!", empty frame after the file shrinks | caption band, dark panels, nowrap title + smaller circle, stamp moved, "EK CHHOTI SI FILE MEIN?" text |
| preview 1 render | blackdetect: 6 near-black spans; cause = duplicate element id `s{k}c` (shot wrapper and a text) hid whole shots for seconds; design shots showed only the background for 1-3 s before their first element | unique ids; a design shot now starts when its first element enters (previous shot holds); caption band hugs the spoken words |
| preview 2 (2026-10-28, measured here) | 304.1 s, 30.0 fps; -17.1 LUFS, peak -1.6 dBFS, 0 clipped; no mix window > 2 dB over the VO's p95; blackdetect (d 0.2, pix_th 0.10) finds nothing | sent to the owner; GTA gameplay slots wait for the client's footage |

## v3 audio (owner 2026-10-28: "voice bhot slow hai, customize karo; bolte waqt music kam; SFX/music pro editor ki tarah, hype + hook")
| Decision | Source |
| --- | --- |
| VO rebuilt from the retake-free cut (vo_hype.py): both later retakes removed, every pause > 0.28 s shortened to 0.20 s (124 cuts, 64.1 s), dramatic beats kept (before "lekin bhai", after each spoken heading, after the punchline), tempo 1.2x (rubberband), high-pass 80 Hz, +2.5 dB at 3 kHz, compressor 3:1, loudnorm -16 -> 242.9 s, 202 words/min (was 304 s) | owner request; skills #188/#2348, #289, #316; measured here |
| Music no longer sidechain-compressed: gain automation from the VO envelope (mix.py): -5 dB in pauses, -20 dB under speech, 60 ms down / 350 ms up, no pumping in gaps < ~0.4 s. Measured: music+SFX sit 15.4 dB under the voice while it speaks | owner request; skills #316/#317 |
| Music stops on each topic bumper and drops back in right after the spoken heading; stops before "lekin bhai" and the punchline (mood_bed2.py, anchored to VO words) | guide (scam reveal: music band; punchline: short silence), client voice note (glitch + sound on topic change) |
| SFX level-matched per type (impacts loudest, UI clicks quietest), -3 dB when they land on speech except reveal hits; added a sub-drop under the opening title and a riser into "SCAM HO RAHA HAI" | guide "Sound effects" (restraint), hook skills #99/#103 |
| Master: two-pass loudnorm -15 LUFS linear + limiter -1.5 dBTP. Measured: -15.0 LUFS, peak -1.5 dBFS; only the opening boom and the punchline hit go 3-4 dB over the voice's p95 (intended) | measured here |

## Final v1 (2026-10-28)
| Decision | Source |
| --- | --- |
| Four stumbles left in the v3 VO, found by Whisper medium (full pass + per-region hi/en passes) and cut, keeping the corrected take: "na da, na 100 GB," false start (7.60-9.45 s), first of "bina, bina verify" (121.30-121.78), first "to thoda suspicious" (187.45-188.60), "kyunki kisi..." restart (194.12-195.08). Re-checked: all four lines whole. VO 238.5 s | owner: "mistake hata ker theek wala rakho"; VERIFIED ONLY |
| Checked and kept: "sab sab pehle" (0.36 s, heard as "first of all" in the en pass), "install karo" (present), "ek APK" (single) | per-region Whisper, measured here |
| GTA gameplay = the client's recording (Drive 1nZX4fI3_pHjqgs6-Ci4jE8YZxzBV5fSI, "GTA 5 ... No Copyright Gameplay 4K 60fps _ 197 (720P_HD).mp4", 408 s, 1280x720 60 fps; client allowed its use, owner 2026-10-28). Upscaled lanczos + cas 0.5. Slots: hook driving 37 s, phone/action 140, city 64, in-phone 220, Franklin walk 0.5, freeze at 6 (grey), city wide 16, skyline 20, Franklin 118.5, Michael line -> car shot 384 (no Michael in the recording), Trevor line -> underpass 196 (no Trevor), open world 164, montage city/cars/buildings/missions/characters/audio/textures/data = 76/40/80.5/148/88.5/228/136/208, PC 356, dramatic 260, police chase 296. Blood shots (112, 156, 336 s) not used | contact sheets look/gp_sheet_*.jpg; guide "relevant GTA 5 gameplay" |
| Minecraft resource-pack joke: the client's own ALOO SMP spawn recording (Drive 1SmJKT0fOUn--o94gnSx_Pg3D4gq5wpwA) from 20 s | guide scene 4 |
| Owner: "final video bhej dena" -> delivery render directly, full quality only (no WhatsApp copy) | owner 2026-10-28; CLAUDE.md |
| Final QA (measured here): 239.9 s, 1920x1080 30 fps h264 + aac, 145 MB; -15.8 LUFS, peak -1.4 dBFS; blackdetect (d 0.2, pix_th 0.10) and freezedetect (2 s) find nothing; thumbnail = frame at 1.2 s (title over gameplay) | delivered with SendUserFile |
| Credit note for the client: the gameplay file name says it is a "No Copyright Gameplay" upload; such channels often ask for credit in the description, so the client should credit the source channel | told the owner |

## Final v2 (2026-10-28, client feedback on v1)
| Client said | Fix | Source |
| --- | --- | --- |
| "2:05 mein word repeat hua hai" | The spoken heading was said twice ("why 10MB GTA5 doesn't... doesn't", 123.02-125.02 s); kept the clean second take (cut5.py). Final checked with Whisper medium (en): "...Why 10mb gta 5 doesn't make sense? Now let's put some logic" | measured here |
| "popup sounds alag alag, same sound baar baar repeat, 2-3 type" | Pops rotate pop-high / bubble-pop / plop (13 each), whooshes whoosh-fast / swish-1 / whoosh-up, impacts impact-punch / punch-medium / punch-heavy (library/sfx, CC0) | client; library/sfx |
| "thora sa AI jaisa lag raha hai, photos use karo" | Every design shot now sits on real footage instead of a flat purple card: dimmed client GTA gameplay (14 rotating driving shots, brightness 0.55) or real phone b-roll on phone lines (Mixkit 4915 "Hands of a person typing on a cell phone", 144 "Hands shown texting on a smartphone"; Mixkit Stock Video Free License, no credit, fetched with find_stock.py); dropped the phone emoji on "simple rules". Openverse (504) and Wikimedia API (rate limit) were down, so no stock photos this round | client; skill stock-sfx-luts |
| client picture (GTA VI on Android) | Used as the clickbait YouTube thumbnail on "YouTube thumbnail par toh log GTA 6 bhi..." with "CLICKBAIT THUMBNAIL" label and FAKE? stamp (replaces the drawn one). File stays in the scratchpad (client media, not committed) | client |
| QA (measured here) | 237.9 s, 1920x1080 30 fps, 305 MB; -15.8 LUFS, peak -2.0 dBFS; blackdetect + freezedetect clean; render 41 min (stalled once at low disk; freed space) | |
