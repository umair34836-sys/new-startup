# brand-identity-reveal (16:9 or 9:16, ~30 s, music only)

Brand identity / brand-guidelines showcase film in the style of the reference the owner sent on 2026-10-27
(Solune / Design On Acid; analysis in library/research/ref-brand-identity-reveal.md: quiet intro, drop at 7.4 s,
beat cuts, shot order logo construction -> lockup -> mockups -> stacked guideline cards -> typography -> colour ->
UI widget cards -> photos -> held end logo). First made for HostLixo (hostlixo.in), 2026-10-27.

Files:
- `build.py reveal.json`: run it inside a project folder. It writes index.html + compositions/*.html.
  - The scenes are construct, lockup, browser, phone, stack, type, swatch, stats, chart, photos, social, end.
  - Every scene after the drop is a whole number of beats: `music.bpm` / `music.drop_at`.
  - The music starts at `music.from`, so its drop hit lands on `drop_at`.
  - Size comes from `size` ([1920,1080] or [1080,1920]). Only 16:9 has been rendered so far: the 9:16 layout branches are untested.
- `mark_to_svg.py mark.png mark.json [--overlay check.png]` (perc-venv OpenCV) traces a flat, straight-edged logo mark into polygons.
  - It also measures the slant of the long edges. The construction shot draws those real edges and vertices and shows the measured angle.
  - Check the overlay PNG: marks with curves need a real SVG instead (not supported yet).
- `reveal.example.json`: HostLixo's config. All values come from hostlixo.in (2026-10-27): colours = site CSS vars, fonts = loaded site fonts, stats = home-page stat row, chart = the 9 plan prices.

Project assets: assets/vendor/gsap-3.14.2.min.js, assets/fonts/<the 3 font files>, assets/sfx/{whoosh-fast-0.3s,riser-2s,riser-4s,impact-boom}.mp3 (library/sfx),
assets/<music + every image named in reveal.json>. Site screenshots and images live only in the scratchpad (library/clients/hostlixo/site/tools/shots.js).

Mastering: the render came out at -19.8 LUFS. The fix was gain + limiter, not loudnorm:
`ffmpeg -i raw.mp4 -c:v copy -af "volume=4.9dB,alimiter=limit=0.84:level=false" -c:a aac -b:a 192k out.mp4`
gave -15.0 LUFS, LRA 6.7 LU, true peak -1.29 dBTP, 0 clipped. Two-pass loudnorm hit -14.9 LUFS but flattened the LRA from 6.7 to 2.8 LU (it lost the quiet-intro contrast).

QA, HostLixo v1 (measured here 2026-10-27):
- `hyperframes check` passed. Its warnings are line_unread on fast beat cuts (inherent to the style) and nothing else.
- I looked at snapshots of every scene.
- Render `--workers 3` took 44.6 s.
- watch.py: 30.0 real fps. Black only in 0.1-0.27 s push-in transitions after a fix: the first version had 0.93 s of near-black at 0 s; a ghost of the mark (opacity 0.18) is now on screen at 0 s for the thumbnail.
- listen.py after mastering: see above. Its sections show the intro at -21.8 dB, then the drop.

Skills used: #426/#427 (logo reveal ingredients and timing: draw-on 1.1 s, stagger 0.09 s, settle 1.04 -> 1.00 in 0.18 s), #155 (eased push-ins / camera drift), client-brand-kit (brand-config idea), #3107 (device blocks: hand-built CSS browser/phone frames here, no registry block), listen-and-watch.
Not used: #184 speed ramp (no video footage in this version).
