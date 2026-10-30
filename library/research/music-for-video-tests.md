# Music workflow tests (skill music-for-video), measured here on 2026-10-27

Three past video types run through the whole workflow (find_music.py -> listen.py -> choose -> music_fit.py ->
mix_vo_music.py -> listen.py QA). No video was made and no client media was used. The test voice-overs were
assembled from the repo's own AI field-voice reference lines (`library/voices/*-ref.wav`, 8 lines each, 0.7-0.9 s gaps,
speech 1.0-28.9 s / 1.0-27.1 s). All audio outputs stayed in the session scratchpad (not in git).
`$P` = `/home/user/tools/perc-venv/bin/python`.

## Test 1: hosting promo reel, 30 s, with VO, client job

1. Shortlist: `python3 library/tools/find_music.py "hosting promo" --length 30 --client --vo --top 5`
   -> types hosting-tech + promo, energy mid/high, 100-130 BPM, VO = no vocals; 130 tracks passed the filters.
   Top 2: Monarch of the street (score 19.0), People are spinning (18.0).
2. listen.py on both:
   - Monarch of the street (Loyalty Freak Music, CC0): 99.0 BPM (essentia conf 3.42, librosa agrees), beat CV 0.012,
     -13.0 LUFS, LRA 1.7 LU, full sound by 1.24 s, real ending from 222.13 s, no voice activity.
   - People are spinning: 110 BPM, G major, but intro until 17.4 s (-19.0 dB intro, -16.2 dB build) and a fade-out end.
3. Choice and reasons: Monarch. Upbeat-electronic fits a tech brand (music-for-video.md section 2: unboxing/tech
   "upbeat electronica", explainer music that "doesn't steal the spotlight"); in from the first second (hook);
   LRA 1.7 LU = a steady bed under a voice (BBC: "not too dynamic"); a real ending to land the CTA on.
   Rejected People are spinning: 17 s intro would waste the first seconds of a 30 s reel.
   Note: listen.py's mood heuristic calls it "sad/reflective" (D minor); the brighter G-major track lost on its intro.
4. Fit: `$P library/tools/music_fit.py <monarch> h-bed.wav --length 30 --end resolve --check`
   -> segments [0.0-27.9] + [222.13-224.14] (the track's own 2.0 s ending), one join at 27.9 s, 0.09 s silence at the
   end. Check: join 1.0 ms from the nearest detected beat; beat-phase error after the join 22.0 ms vs 20.0 ms median at
   unedited points (= tracker noise); BPM 98.9, beat CV 0.009; last second -62.7 dBFS (it really ends).
5. Mix: `$P library/tools/mix_vo_music.py hosting-vo.wav h-bed.wav h-mix.wav` (defaults)
   -> VO -15.7 LUFS and music -30.7 LUFS during speech (gap 15.0 LU), music -23.3 LUFS in the pauses, final -16.1 LUFS,
   sample peak -2.0 dBFS, 0 clipped. listen.py on the mix: -16.1 LUFS, LRA 3.0 LU, true peak -1.91 dBTP, 0 clipped.
6. Old method for comparison (fixed music volume 0.16, VO loudnormed to -16, no ducking, as in the MoradoSolution and
   Pizza Base reels): VO over music during speech = 12.6 LU with Bollywood Groove, 14.1 LU with Monarch, and the music
   never rises in the pauses.

## Test 2: food promo reel, 30 s, with VO, client job

1. `python3 library/tools/find_music.py "food restaurant promo" --length 30 --client --vo --top 4`
   -> food + promo, energy mid/high, 95-125 BPM. Top: Everyone is so alive (18.0), Tupac Lives (18.0), Yippee (17.5).
2. listen.py:
   - Everyone is so alive: tempo NOT reliable (librosa 107.7 vs essentia 161.7, conf 1.08, beat CV 0.055), 12 s intro.
   - Tupac Lives (John Bartmann): 95.9 BPM, F minor, -9.8 LUFS, true peak +0.2 dBTP, 2 clipped samples in the source.
   - Yippee (Loyalty Freak Music, CC0): essentia 178.2 BPM (conf 1.9; librosa 117.5), C major on all 3 key profiles,
     -13.3 LUFS, LRA 3.1 LU, full by 1.41 s, real ending from 126.62 s.
3. Choice: Yippee: happy, bright major key = "light, breezy" food music (PremiumBeat, section 2); hook in the first
   second; real ending; no clipping. Rejected: Everyone is so alive (no reliable beat grid to cut on, slow intro),
   Tupac Lives (minor key, clipped source).
   Tool fix from this test: find_music.py now penalises beat CV >= 0.05 or essentia confidence < 1.0 (it had ranked
   Everyone is so alive first); after the fix the order is Tupac Lives, Yippee, Monarch.
4. Fit: `--length 30 --end resolve --check` -> [0.0-26.7] + [126.62-129.92] (own 3.5 s ending, last 0.22 s of silent
   tail trimmed). Join 3.0 ms from a detected beat; the phase check had too few beats after the join (the ending
   decays) so it reports null; this track's tracker noise is high (74.0 ms median at unedited points; the output
   tracker read 123.0 BPM, i.e. the tempo itself is ambiguous). Last second -71.8 dBFS.
5. Mix with food-vo.wav: VO -15.7 / music -30.7 LUFS during speech (gap 15.0 LU), music -24.4 in pauses, final -16.0
   LUFS, 0 clipped; listen.py: -16.0 LUFS, LRA 3.9 LU, true peak -2.48 dBTP.

## Test 3: 16:9 brand reveal, 30 s, music only, logo reveal at 7.4 s

1. `python3 library/tools/find_music.py "brand logo reveal" --length 30 --client --no-vo --top 4` -> drop needed;
   top: La Citadelle (20.0), Manic WarLord Mother (16.5, has vocals: vocal-scan), Action Epic (16.5),
   Dome of grey (16.5).
2. listen.py:
   - La Citadelle (Komiku, CC0): 129.9 BPM (conf 1.72, librosa agrees), beat CV 0.019, intro 0-6.2 s (-18.9 dB) then
     the drop (-15.8 dB, +5.0 dB rise), fade-out ending, -16.4 LUFS.
   - Dome of grey: no steady beat (essentia conf -0.16, CV 0.056), LRA 8.6 LU: rejected for a beat-counted reveal.
3. Choice: La Citadelle: epic/driving (section 2 gaming/action "builds up to climactic moments"), a measured drop to
   land the logo on, steady grid for counting scenes in beats (brand-identity-reveal template).
4. Fit: `--length 30 --drop-at 7.4 --end resolve --lufs -16 --check`. The drop (6.2 s) comes earlier than 7.4 s, so
   music_fit repeats the bar before the drop: [0.79-6.2] + [4.21-28.56]; the track fades out, so the end is a downbeat
   hit at 28.0 s + 2.0 s ring-out. Result -16.0 LUFS, true peak -2.65 dBTP, 0 clipped.
   Bug found and fixed in this test: the repeated bar first started at 6.2 - 1 bar (4.35 s) instead of the real
   downbeat 4.21 s (the intro's beats are 0.49-0.50 s apart, slower than the 0.464 s after the drop). It now snaps to
   the measured downbeat.
   Check numbers: join phase error 66.5 ms vs 28.0 ms median; but the UNEDITED source already shows 46.0 ms at its own
   drop (tempo change intro -> drop), and an unedited run (`--drop-at 6.2`, no join at all) puts the nearest detected
   beat 93 ms from the drop. On tracks whose tempo changes at the drop, listen.py's beat tracker is the limit, not the
   edit. Lesson: when the edit allows, put the reveal on the track's own drop time (here 6.2 s) or later by whole bars.

## What the tests established

- The workflow picks from documented reasons and rejects tracks for measured faults (slow intro, no beat grid,
  clipping, vocals), instead of folder names.
- Bar-accurate joins measured at the beat tracker's noise floor on steady tracks (Test 1: 22.0 vs 20.0 ms; earlier
  loop test: 33.0 / 39.5 / 1.0 ms vs 33.7 ms, loading-screen-loop stretched to 45 s).
- Real endings kept (last second -62.7 and -71.8 dBFS: the music ends, it is not cut).
- Mixes hit -16.0/-16.1 LUFS with a 15.0 LU voice-over-music gap and 0 clipped samples.
- Limits: 4/4 assumed; downbeat phase is an estimate (listen.py `downbeat_phase_clarity`); tracks with tempo changes
  or weak beats (essentia confidence < 1.5) give noisier checks; Claude can't listen, so the owner's ear is the final
  check of a new track.
