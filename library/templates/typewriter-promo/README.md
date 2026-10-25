# Typewriter promo template (first used: FireCraft SMP typewriter video, 2026-10-25)

Text-only promo: each card has a kicker (appears at once) and lines typed character by character on the GSAP timeline
with seeded human jitter (skill #408: uneven gaps, longer after spaces/punctuation), a caret per line that blinks after
the card finishes (finite stepped repeat, no repeat:-1), real images popping in when named (FireCraft: the 11 power icons
from www.firecraft.fun/images/powers/), keypress sounds (library/sfx/typing/keypress.mp3, CC0) pre-mixed into ONE wav
with numpy (+-10% pitch, random gain), and a small bell (sfx/notification/bell-small.mp3, CC0) when each card finishes.

Use: copy into a project made with `npx hyperframes init proj`, put gsap-3.14.2.min.js in proj/assets/vendor, logo,
images, sfx and a CC0 track in proj/assets, edit CARDS (`[[x]]` = accent colour, `{{x}}` = red), run
`/home/user/tools/venv/bin/python build.py`, check, snapshot, render --workers 3, then loudnorm the audio
(`ffmpeg -i in.mp4 -c:v copy -af loudnorm=I=-16:TP=-1.5:LRA=11 -c:a aac -b:a 192k out.mp4`).

Measured on the FireCraft video (2026-10-25): 9 cards, 342 key sounds, 54.3 s, render 1m19s (--workers 3), 1,630 frames
at 30.0 fps, no gaps. Raw mix was -22.2 LUFS (keypress track peak-normalised + music at volume 0.22); after loudnorm
-17.8 LUFS, true peak -0.83 dBTP, 0 clipped samples.
Checker note: `line_unread` counts every per-character <span> as a word, so its hold floors are inflated; judge
holds by real words (0.5 s + 0.3 s a word).
