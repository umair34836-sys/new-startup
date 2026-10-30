# Reference video: 3D/CGI "one-take" product ad (owner asked 2026-10-30)

The owner asked: "Check this video and tell me kia is level ki editing k qabil hai hum or in me kia kia or konsi skills use
howi hai or is editing ko kia name se kehte hai".

## Source
- Video: https://vm.tiktok.com/ZSgWqnorX/
  - It resolves to https://www.tiktok.com/@lenny_motion/video/7700981857067732257
  - Downloaded with yt-dlp on 2026-10-30, into the scratchpad only, never committed.
- Title: "Wasn't ready for that.. #CapCutPC #capcutmarketing #capcutsale".
- Uploader: lenny_motion. Spec: 16.7 s, 1080x1920, 30 fps.

## What the frames show (contact sheet at 5 fps, looked at 2026-10-30)
- One continuous camera move with no hard cuts. `select='gt(scene,0.3)'` found 0 scene cuts.
1. Real phone footage in a studio: a person drives an RC car that drifts on a table.
2. The camera follows the car low. Camera lenses and black discs fall and bounce on the table. They look 3D-rendered
   (they cast light and shadow on the real table).
3. Large white mouse cursors fly through the shot.
4. An editing-app timeline (ruler, clips) appears as a physical 3D strip on the table. It rolls up like a carpet and
   flips with the camera. The camera passes inside the clip thumbnails.
5. The move ends on real POV footage of hands on a laptop running the editor. A glowing hologram logo
   "CapCut PC 60% off" rises above the screen.
- Heavy motion blur on every fast move; the camera rotates 90-180 degrees.

## Audio (listen.py, measured 2026-10-30)
- Music bed: 89.9 BPM, bar 2.669 s.
- Strongest hits: 0.07, 7.50, 9.61-12.91 s. This is a dense run of impacts in the CGI part.
- Two short voice bits; Whisper heard "Let's go."
- Loudness -15.2 LUFS, true peak -2.97 dBTP.

## Names for this kind of edit (descriptive terms, not checked against a source)
- CGI / VFX ad
- 3D integration
- camera tracking (match-move) + compositing
- seamless one-take transition
- 3D motion design / product ad

## Can the repo pipeline make this? (judged against CLAUDE.md facts)
- No, not at this level. The core needs:
  - 3D camera tracking of handheld footage;
  - photoreal 3D models lit to match the room;
  - a GPU render.
- The box is CPU-only (4 cores, no GPU), and the repo has no camera-tracking tool.
- Within reach with existing tools:
  - motion graphics and UI animation (HyperFrames, GSAP);
  - animated cursor + click (screen_recorder.js);
  - glowing title/logo reveals (brand-identity-reveal template);
  - speed ramps, motion blur, 2D seamless transitions;
  - SFX hits on the beat (beat_events.py, library/sfx);
  - loudness to -15 LUFS.
