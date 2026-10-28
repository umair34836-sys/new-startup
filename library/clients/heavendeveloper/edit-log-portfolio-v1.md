# Edit log: Bhupendra portfolio video v1 (16:9 1920x1080, 78.2 s, 2026-10-28)

- Recipe: decision-guide section 26 (App / website promo: walk through the REAL site, browser frame + side panel with the
  site's own headings) + templates/screen-tutorial (record with screen_recorder.js, speed-fit each recorded span to its
  VO line 0.85-3x, map clicks to output time; OWNER RULE: every click shown with cursor + ripple + click sound).
  16:9 because the walkthrough template renders 1920x1080 and the site is a desktop layout.
- Facts: bhupendra-portfolio.md (web_capture.py + DOM probe). The site's Heaven invite link is expired -> not shown.
- Recording: templates/portfolio-site-promo/record_bhupendra.js, zoom 1.25, real in-page nav clicks, FAQ answers opened by
  real clicks, external links (Work with me, Join Heaven Developer, guns.lol, YouTube) fakeClick only. 83.7 s.
  The full-page screenshot was blank (scroll-reveal sections), so only the live scroll recording is used.
- Look: the site's own CSS variables (--bg #07090d, --panel #0d1218, --ice #6fd3ff, --gold #d4af6a); serif = Noto Serif
  (in the site's --serif stack; added to library/fonts, OFL) because lint failed on fonts without @font-face.
- VO: vs_tts.py --voice explainer-pro --lang en, 12 lines, Whisper small: all lines heard ("Bupendra" spelling only).
- Music (music-for-video): find_music "portfolio showreel tech calm modern" --client --vo; picked CC0 "People Are
  Spinning" (Loyalty Freak Music, 110 BPM, G major, bright: a personal developer brand, different from the Heaven
  promos' darker Monarch track); its slow intro skipped with --start 19.09 (full sound); fade-out track -> music_fit
  ends on a downbeat + 2 s ring-out; mix_vo_music gap 15.0 LU.
- QA: check passed (first_frame_empty fixed: browser, title and first panel visible at 0 s; 22 px text raised to 28 px);
  render -w 3: 2m55s; listen.py -16.1 LUFS, TP -3.21, 0 clipped; watch.py 30.0 fps; blackdetect 0.
