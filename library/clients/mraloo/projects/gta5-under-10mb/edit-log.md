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
