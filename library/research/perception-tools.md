# Perception tools: listen.py and watch.py (what they measure, accuracy, limits)

Claude can't hear audio or watch video at full speed. These two tools turn media into numbers and a contact
sheet. Every number below was measured in this cloud box (4 CPU, no GPU) on 2026-10-24, unless a source URL
is given. "Unverified" means it was not checked here.

Setup: `bash library/tools/setup-specialist-a.sh` (venv `/home/user/tools/perc-venv`, models
`/home/user/tools/perc-models`). Whisper words and `--vocals` need the main venv (`setup-all.sh heavy`).

## Libraries and models used (source checked 2026-10-24)

| Piece | Used for | Licence (from the repo page) | Source |
|---|---|---|---|
| librosa 1.0.0 | beats, onsets, chroma/MFCC, novelty sections | ISC | https://github.com/librosa/librosa (8673 stars) |
| essentia 2.1-beta6-dev (pypi `essentia`) | RhythmExtractor2013 tempo + confidence, KeyExtractor, Danceability | AGPL-3.0 | https://github.com/mtg/essentia (3780 stars) |
| pyloudnorm | EBU R128 integrated/short-term loudness | MIT | https://github.com/csteinmetz1/pyloudnorm (784 stars) |
| Silero VAD (`silero_vad.onnx`, run with onnxruntime) | speech activity | MIT | https://github.com/snakers4/silero-vad (10506 stars) |
| PySceneDetect 0.7.2 | shot cuts (ContentDetector, AdaptiveDetector) | BSD-3-Clause | https://github.com/Breakthrough/PySceneDetect (5284 stars) |
| MediaPipe Tasks 1.1.1: BlazeFace short-range, EfficientDet-Lite0 | faces and people per scene | licence not checked | https://ai.google.dev/edge/mediapipe/solutions/vision/face_detector |
| OpenAI Whisper small (main venv) | words with timestamps | not checked here | installed by setup-all.sh heavy |
| UVR-MDX-NET Voc FT via audio-separator (main venv) | `--vocals` stem | not checked here | installed by setup-all.sh heavy |

Notes from the sources: Google's page says BlazeFace short-range is "optimized for front-facing phone camera
images at short range" (so small/far faces can be missed). Essentia's own docstring
(`essentia.standard.BeatTrackerMultiFeature.__doc__`, read 2026-10-24) grades the multifeature confidence:
[0,1) very low, [1,1.5] low, (1.5,3.5] good ("accuracy around 80% in AMLt"), (3.5,5.32] excellent, and says the
input must be 44100 Hz. listen.py uses essentia's grid only when confidence >= 1.5 and feeds it 44.1 kHz.

Install facts measured here: `pip install silero-vad` pulls CUDA torch (venv grew to 6.2 GB); without it the
perc-venv is ~1.3 GB, so Silero runs from the ONNX file. MediaPipe 1.1.1 has no `mp.solutions` (only `mp.tasks`)
and needs `libgles2` + `libegl1` from apt, otherwise import fails with
`libGLESv2.so.2: cannot open shared object file`.

## listen.py

`/home/user/tools/perc-venv/bin/python library/tools/listen.py FILE [--out r.json] [--json] [--no-words] [--vocals] [--bpm-hint N]`

Reports: tempo (essentia multifeature when its confidence >= 1.5, else librosa) + beat list, `bar_s_4_4`,
estimated downbeats (4/4 assumed: the beat phase with the most <200 Hz onset energy), onsets + 20 strongest
hits, integrated LUFS + 3 s short-term curve (1 s hop) + LRA approximation + 4x-oversampled true-peak estimate +
clipped-sample count, silences (< -50 dBFS for >= 0.3 s), sections (beat-synchronous chroma+MFCC
self-similarity, checkerboard novelty), Silero speech segments, optional vocal-stem segments, key (3 essentia
profiles vote), a mood rule of thumb, noise floor, hum and hiss checks, Whisper words, and a content-type guess.

### Accuracy measured (2026-10-24)

| Test | Truth | Result |
|---|---|---|
| Synthetic 30 s click track (kick every 4th beat), `synth124.wav` | 124 BPM, first beat 0.50 s, downbeats every 1.935 s from 0.50 s | essentia 124.0 (conf 3.49), librosa 123.0; downbeats 0.49, 2.44, 4.37 ... (phase correct, ~10 ms early); bar 1.935 s |
| same file | tone section 10-20 s, digital silence 22-24 s | section bounds 10.2 s and 19.9 s; silence span found inside 22-24 s |
| same file + 50 Hz sine at -50 dBFS | hum present | 50 Hz bin 19.8 dB over neighbours -> `hum_suspected: true, hum_hz: 50` (60 Hz: 0.7 dB) |
| same file + white noise (ffmpeg anoisesrc amplitude 0.004) | hiss present | `hiss_suspected: true` (HF share 0.358); clean file: false (0.0) |
| `library/music/baarish-ki-pehli-shaam-ai-song.mp3` (made with ai_song.py at 80 BPM) | 80 BPM | both libraries said ~162 (double), essentia confidence 0.76 -> tool prints `LOW CONFIDENCE: could be 80.7 BPM`; with `--bpm-hint 80`: 80.7 BPM |
| same song, Silero VAD vs vocal stem (MDX Voc FT stem active = 100 ms RMS within 30 dB of its peak) | vocal stem active 50.7% of the time | Silero on the mix: 20.7%, precision 0.968, recall 0.395 -> Silero misses most SINGING; use `--vocals` for songs |
| `cc0/background--bossa-nova.mp3`, `cc0/desi-eastern--electronic-indian-tabla-tune.mp3` | unknown BPM | librosa and essentia agree (129.2/129.0, 83.4/83.0, essentia conf 3.77/2.85) - agreement only, not truth |
| 40 s CC0 English interview (Wikimedia Commons "IBAI student launch 1.webm") | speech | VAD 85.6% speech, type guess "speech"; Whisper small text readable (not checked word by word) |

Fixes made because of these tests: hum is only judged when the quietest 30% of 1 s windows is below -35 dBFS
(the loud tabla track gave a false "hum" before); sections with < 3 dB energy spread are labelled `part N`
instead of intro/drop guesses; a speech file is flagged so tempo/key/mood are not taken seriously.

### Limits

- Downbeats assume 4/4 and are a heuristic (`downbeat_phase_clarity`: 0.84 on the click track, 0.04-0.37 on real
  music, i.e. weak). No madmom-style downbeat model is used.
- Section labels (`intro`, `drop/chorus`, `break`) come from relative loudness only. Boundaries are the real output.
- `mood_heuristic` is a rule (major/minor x BPM >= 110 x spectral centroid > 2500 Hz), not a trained model.
- Key: 3 profiles agreed on every file tested; correctness against a known key was not tested (unverified).
- Silero is a speech detector: recall 0.40 on sung vocals (above). `--vocals` costs ~44 s per 60 s of audio.
- Hum rule can fire on sustained bass notes; hiss rule threshold 0.3 is close to a real outdoor recording (0.322).

Speed: 60 s song 10 s, 127 s track 20 s, 40 s speech with Whisper small 24 s; `--vocals` +~40 s per minute.

## watch.py

`/home/user/tools/perc-venv/bin/python library/tools/watch.py VIDEO [--out r.json] [--sheet sheet.png] [--width 320]`
`... watch.py compare A B [--at 1,3.5] [--labels before,after] [--out cmp.png]` (videos or images)

Reports: header vs real fps (median frame interval from ffprobe pts), VFR and frame gaps, cuts (ContentDetector
threshold 27 = primary; AdaptiveDetector listed too), per second: motion (mean abs grey diff), shake (phase
correlation camera path minus its 0.5 s moving average, px at analysis width), flicker, luma, sharpness;
per scene: exposure (mean luma, >= 250 clipped share, <= 5 crushed share), colour (near-neutral-pixel a*/b* and
whole-frame a*/b* vs the median of the other shots), sharpness relative to the best scene, faces and people
(max over 3 sample frames at 640 px), black and frozen spans, and a labelled contact sheet.

### Accuracy measured (2026-10-24) on a built test video with known truth

Built with ffmpeg from the CC0 interview (406x720, 30 fps, 16.5 s): 0-4 s normal, 4-5 s black, 5-8.5 s shaken
(crop offset 14 px/12 px sine), 8.5-10.5 s frozen frame, 10.5-13.5 s 10 Hz brightness flicker (eq brightness
+-0.12), 13.5-16.5 s Gaussian blur sigma 6 + warmer shadows/mids (colorbalance rs=.3 bs=-.3 rm=.2 bm=-.2).

| Truth | watch.py |
|---|---|
| cuts 4.0, 5.0, 8.5, 10.5, 13.5 | ContentDetector 4.0, 5.0, 8.5, 10.5, 13.5 (5/5); AdaptiveDetector only 4.0, 5.0 |
| black 4-5 s | black [4.0, 5.0] |
| frozen 8.5-10.5 s | frozen [8.53, 10.5] |
| shake 5-8.5 s | shake 8.9-9.2 px in seconds 5-7 (second 8: 4.7), 0.0-0.5 px elsewhere |
| flicker 10.5-13.5 s | flicker score 0.31-0.66 in seconds 10-13, 0.0 elsewhere (also 0.0 in the shaken part) |
| blur 13.5-16.5 s | scene 6 sharp_rel 0.0 -> "soft/blurred" |
| warmer shadows in scene 6 | whole-frame shift caught (d_a* +3.6, d_b* +4.9 vs other shots); the near-neutral-pixel cast did NOT change (the white banner/highlights were untouched by the filter) |
| 1 person, 1 face | faces 1, people 1 in every lit scene |

Real clip: the same interview (VP9, header 598/25 = 23.92 fps) -> real median 23.81 fps, 6 frame gaps, no cuts,
1 face. Speed: 135 s 406x720 video in 64 s; the 16.5 s test video in 13 s (analysis width 320).

Fixes made because of these tests: phase correlation on black frames gave 123 px "shake" (now zeroed when the
frame is flat); motion was read as flicker (now a flicker step must explain > 50% of the pixel change); MediaPipe
needed apt libs; whole-frame a*/b* of colourful scenes looked like a "magenta cast", so the cast is read from
near-neutral pixels and shot-to-shot matching uses whole-frame values against the median shot.

### Limits

- Near-neutral-pixel cast misses grades that only touch shadows/mids (see table). Read both numbers.
- Sharpness is Laplacian variance: compare scenes inside one video only (`sharp_rel`), not across videos.
- Faces: BlazeFace short-range, so far/small faces can be missed (Google: "short range"); people: EfficientDet-
  Lite0 "person" score >= 0.4. Not tested on crowds (unverified).
- Shake is in pixels at the analysis width (320 default); camera pans also add to it when they are not smooth.
- Dissolves/fades: not tested (unverified); ContentDetector is tuned for hard cuts.
- The contact sheet must still be LOOKED at (Read the PNG): the numbers don't say whether a shot is good.
