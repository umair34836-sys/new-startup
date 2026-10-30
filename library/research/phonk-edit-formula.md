# Phonk / velocity edit formula (researched 2026-10-29, Heaven Developer phonk promo)

Owner 2026-10-29 on v1: "bhot boring sa lag raha hai soo upgrade it and upgrade your formula". Sources read that day
(agent-reach web search + read):

- Onset Engine, "How to Make Phonk Drift Edits on PC" (https://onsetengine.com/guides/make-phonk-drift-edits/, 2026-03-15):
  808 kicks -> 4-6% impact zoom with fast snap-back (100% -> 106% -> 100%, exponential ease-out); snares -> 2-3 px red/blue
  channel split; bass drops -> 1-frame white flash (opacity 100 -> 0 over ~3 frames / ~120 ms); a hard cut on every beat
  (469 ms at 128 BPM); grade: desaturate 15-20%, contrast +30-40%, shadows pushed blue; biggest hits get stutters and
  motion streaks.
- Vikas Editing, "Phonk CapCut Template 2026" (https://editingbyvikas.com/phonk-capcut-template/, 2026-06-13): phonk =
  dark, aggressive, beat driven; add shake and glitch after the base cut; "keep effects sharp but not constant, because
  the best phonk edits hit hard on the drop and breathe in between".
- Vikas Editing, "Alight Motion Shake Preset XML" (https://editingbyvikas.com/alight-motion-shake-preset-xml/, 2026-06-16):
  moderate amplitude (extreme shake looks amateur), strongest shake on the heaviest beat, shake on the beat and rest in
  between, not on the whole clip; don't stack too many effects.
- Alight Motion velocity tutorial (https://alightmotionsapp.org/alight-motion-velocity-edit-tutorial/, 2026-10-10):
  velocity/phonk tracks with strong regular beats, classic range 140-180 BPM; mark the beats first, every speed change
  anchors on a beat (V-shaped speed graph).
- r/VideoEditing "How do people make phonk edits" (2023-04-05): sped-up zooms/slides + shakes; overlays behind the cut-out
  character.

## Formula v2 as built here (library/templates/phonk-3d-promo/build_heavendeveloper_phonk_v2.py)
1. Beat map first: `perc-venv/bin/python library/tools/beat_events.py bed.wav events.json` -> beats, kicks (30-150 Hz
   onsets), snares (1.5-6 kHz onsets), strong kicks. On "Phonk-ish" (HoliznaCC0) 30 s: 36 beats; kicks >= 0.38 strength
   and >= 0.35 s apart = 23 punches; snares >= 0.6 = 12 splits; 17 strong kicks (measured here 2026-10-29).
2. A new camera shot on every beat (wide / face close-up / low hero / dutch / side / back / top) of the 3D character, cut
   1 frame before the beat (skill #372); a slow 5% push inside each shot.
3. Kick -> 6% scale punch, 0.24 s expo.out; strong kick + every scene change -> white flash 0.9 -> 0 in 0.12 s.
4. Snare -> rgbashift 6 px for 0.09 s, grade eq contrast 1.22 / saturation 0.85, colorbalance blue shadows, grain, soft
   vignette: all in ffmpeg after the render (post.sh), so the HTML stays light.
5. Depth and variety: giant outlined word behind the character, real client material in frame (logo coin-flip, orders
   banner), clones for "3 friends" and a crowd for "2,500+ members", a speed-ramped jump on the price reveal, letterbox
   bars snapping on some bars, rotating impact SFX (impact-boom / punch-heavy / sub-drop) and whooshes.
6. Breathe: one music-only bar; text holds while the camera keeps cutting.
Measured (2026-10-29): render -w 3 1m37s; post -> -15.3 LUFS, -1.91 dBTP, 0 clipped; 30.0 fps; blackdetect 0.
HyperFrames lint: a text with a fully transparent fill + stroke fails (text_not_painted): give the outline text a faint fill.
