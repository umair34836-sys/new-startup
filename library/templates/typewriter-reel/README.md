# typewriter-reel (9:16, 20 s, text + CC0 music, no VO)

Made for PakWebHoster on 2026-10-25 (owner asked for a "typewriter" reel). `build_pakwebhoster.py`: a white editor
window ("pakwebhoster.txt") under the client logo; 10 lines type in one character at a time with uneven gaps
(skill #408: random.Random(7) gaps 0.55-1.6x the rate, longer after , ? .), a green block caret that follows the last
character (characters are `display:none` spans switched on with `tl.set`, so the caret sits right after them), a
keyboard loop clip per line (`typing-keyboard-medium`, different media offset each line) + a keypress "enter" after
each line, then the end screen types the URL into an address bar and the phone number.

Fonts: JetBrains Mono (bundled in HyperFrames, no file) + Manrope (library/fonts). Music: library/music/cc0 "Chills"
(HoliznaCC0, CC0) from 2.51 s (first downbeat), volume 0.45.
Measured here 2026-10-25: check 0 errors (give every audio its own data-track-index, overlapping SFX on one lane warn);
render 40 s; -17.9 LUFS -> loudnorm -16. A 46 px mono line holds ~31 characters in a 960 px card (860 px text width):
longer lines overflow, so check every line's length (the builder asserts that each line ends before the next starts).
