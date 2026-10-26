# "Indian Gamers Ignore This Warning… Until It's Too Late": 16:9 explainer, edit log (2026-10-26)

Client VO: "Indian Gamers Ignore This Warning… Until It's Too Late.mp3" (PC security for Indian gamers).
The owner asked for both formats: this 16:9 video first, then a 9:16 Short under 3 min. Host: the owner's blocky character.
Build script, VO, music and photos stay in the session scratchpad (no media in git). Every decision and its source:

## Voice
| Decision | Source |
| --- | --- |
| VO measured at 137 wpm overall but 173 wpm while speaking, so it felt slow because of the pauses. Removed 2 retakes; VAD gaps > 0.6 s cut to ~0.3 s (236.9 s left) | skill #3864 (125-150 wpm), #289 dialogue compression, #4 jump cut; measured here |
| Owner: "voice phika, hype banao". rubberband tempo 1.1 + acompressor (thr -18 dB, ratio 2.5) + loudnorm -16 gave 215.3 s | skills #188/#2348 (rubberband keeps pitch), #316/#317; CLAUDE.md (VO -16 LUFS) |
| Whisper medium (hi, condition_on_previous_text=False) on the edited VO: 592 words. The full pass merged 107.5-120.5 s into one word although the audio is speech there (RMS -16..-21 dB every 0.5 s), so that stretch was re-transcribed alone (+38 words) | CLAUDE.md "Whisper on a long song misses whole sung stretches"; measured here |
| Unclear words re-checked with Whisper medium in Hindi and English: "extra tool", "first week / second week", "random mod site", "keep it on". The "नहीं" in "अगले नहीं वीडियो में" was left out (English pass: "See you in the next video") | VERIFIED ONLY rule |

## Music and SFX
| Decision | Source |
| --- | --- |
| The owner's YouTube Audio Library tracks (Drive; YouTube use only): Apocalyptic Echoes 0-17 s (suspense hook), 360 No Scope from 15.5 s (steadiest grid, conf 2.45), Lion from 201.5 s (outro). Each track loudnorm -14 and sidechain-ducked under the VO (thr 0.05, ratio 4, attack 20, release 500), bed volume 0.32 | owner allowed YT library tracks; skills #316/#317 ducking; listen.py |
| Each section title gets a sting (crest timed to the title) + punch; whoosh on every image card; error on "This file may harm" and "New login attempt detected", glitch on "har virus", negative on "scam", alarm on "band karo", chime on "share kar dena" | memes.md rules 4-6; faceless section 17; library/memes/sfx (CC0) |

## Picture
| Decision | Source |
| --- | --- |
| Section titles = the VO's own English headings (7 sections: Warning, Why vulnerable, My Real Story, How this file actually work, The Biggest Lie, Signs, Final message) | decision-guide 16 explainer; VERIFIED ONLY (no invented headings) |
| One image card per VO line (57 cards), each labelled with the VO's words. Images are online CC0/PDM only: 8 Minecraft images from Openverse (mc_licence_proof.json) where the line is about gaming/mods, otherwise a real photo of what the line says (padlock = password, bitcoin = crypto mining, envelopes = email alerts, PC fan = fan loud...) | owner 2026-10-26: "emojis ko priority mat do, real images", "minecraft relevent", "game play wale mat use kro, online images", "voice ka topic se relevent" |
| Not used: the client's gameplay recordings (owner said no); virus-microscope photo (a biological virus, not a PC virus) | owner; relevance |
| Emoji badge on each card + reaction emoji above the host (Fluent 3D, MIT) and Lucide/Tabler line icons in the labels | owner: "photos + emojis dono"; library/elements licence_proof.json |
| Host poses change on every card and section (spin, point, talk, wave) so he never just stands there | owner: "player khada hai awkward" |
| Word-timed Hinglish captions, one gold word per group, 210 groups | CLAUDE.md captions recipe; captions.md |
| Section titles of up to 32 characters are sized to fit one line (Anton is ~0.42 em per capital, measured on the renders) because a 2-line title covered the image card | snapshot check |
| Frame 0 shows the title and the first image, set as inline opacity (a tl.set at 0 left frame 0 empty: check first_frame_empty) | CLAUDE.md "tl.set(..., 0) does not render on frame 0" |

## QA
| Round | Found | Fix |
| --- | --- | --- |
| preview 4 | gameplay cards (owner rejected them) | online images |
| preview 5 | label overlap at 23.6 s (two cards at once) | each card ends where the next one starts |
| full build | 2-line titles over the cards; empty frame 0 | one-line title size; inline opacity |
