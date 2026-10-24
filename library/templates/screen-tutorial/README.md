# Screen tutorial template (first used: FireCraft SMP whitelist tutorial, 2026-10-24)

Real-site tutorial with a visible cursor + click ripple + click sound on every click, a voice-over that is the clock,
step chips, highlight rings and title/end cards. 1920x1080, 30 fps, HyperFrames.

1. `flow.js` (Node): records the real site with `library/tools/screen_recorder.js` -> run*/recording.mp4 + events.json.
   Live forms are never submitted: use `fakeClick` (cursor + ripple, no click) on Create/Submit buttons.
   `NODE_PATH="$(npm root -g)" node flow.js $PWD/run3`
2. VO: one line per on-screen step (`vo-script-hi.txt`, Devanagari only). Design ONE good line with VoxCPM2
   (`vs_tts.py --model voxcpm2 --instruct ...`), trim any run-on tail, then clone it for all other lines
   (`--ref ref.wav --ref-text "<line 1>" --parts c7`). Check every line with `library/tools/wcheck_lines.py`
   (Whisper small, similarity + last word end) and regenerate bad ones; `vo/override.json` swaps in redone takes.
3. `build.py`: SEG = recording span per VO line (a number = freeze frame). Each span is sped 0.85-3x to fit its line,
   frozen at the end if the line is longer; VO placed with numpy and loudnormed; click events mapped to output time;
   writes tut/index.html from `index.tpl.html` (+ step chips, highlight boxes in video px, info chip).
4. `npx hyperframes check`, `snapshot --at ...`, `render --workers 3`, then watch.py + listen.py.

FireCraft numbers (2026-10-24): recording 66.3 s / 1,458 frames; video 62.2 s; render 2m01s with 3 workers;
19 click sounds; listen.py -12.7 LUFS, true peak -1.14 dBTP, 0 clipped samples; watch.py 30.0 fps, 1,867 frames, no gaps.

VO used in the FireCraft video: lines 1-11 of `vo-script-hi.txt`; line 12 ("स्टाफ़ चौबीस से...") came out unclear in 3 takes
(Whisper heard "चाछ चाबिष"), so it was replaced by two lines: "एप्लीकेशन का रिव्यू, चौबीस से अड़तालीस घंटे में होता है।" +
"फिर लॉगिन करके, माई स्टेटस में अपना स्टेटस देखें।", with an on-screen "24–48 ghante mein review" chip to back the numbers.
