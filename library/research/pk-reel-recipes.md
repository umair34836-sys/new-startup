# Pakistani-style reel recipes mapped to this repo's tools (Oct 24 2026)

Every style choice below points to its source in `library/research/pk-reels-trends.md` (section number in brackets,
e.g. [T2] = section 2 there) or to a learning already measured in this repo (`CLAUDE.md`, "measured here").
Tool behaviour is taken from each tool's own header comment. Nothing here is a guess about what clients like; where we
have no source, the recipe says so.

Common base for every recipe
- Canvas 1080x1920, 30 fps, export H.264 + AAC, then the WhatsApp copy command from CLAUDE.md (measured here).
  Length: Reels/Shorts allow up to 3 min [T1]; aisle.studio suggests 60-90 s for a highlight, 15-30 s for a teaser [T3].
- Keep text out of ~270 px top / ~672 px bottom / ~64 px sides and the bottom-right button rail [T1].
- Title or key image on screen at 0 s (thumbnail = first frame, CLAUDE.md HyperFrames learnings).
- Hook within the first 1-3 s; first text by 2 s [T1 Instagram tips; T3 gameofbranding].
- Captions on screen because many watch muted [T1, T3]. Default script: Roman Urdu [T3 captionlagao]; Nastaliq only
  for short titles/poetry, with Noto Nastaliq Urdu (OFL, Google Fonts) [T3].
- Music: only no-credit music (owner rule): `library/music/cc0/` (incl. `desi-eastern--*`), `library/music/desi-vocal/`
  (public-domain 1905-1922 records, see its README), or a track the client owns. Trending in-app songs are copyrighted [T3].
- Mix levels and loudness that worked: music 1.0, impacts 0.35-0.4, whoosh 0.6-0.8, about -16 LUFS (CLAUDE.md, measured).
- Phone clips: check real fps and motion-interpolate every clip to 30 fps (CLAUDE.md, measured).

## 1. Slow-mo song-line reel ("Meri zindagi he tu" style)
Why: 11 of 20 trending CapCut template cards on Oct 24 2026 were slow-motion, titled with a Roman Urdu/Hindi song line [T2].
How: 3-5 clips, each slowed with the `minterpolate` slow-mo command from CLAUDE.md; one Roman Urdu line per clip
(word blur-in, 0.12 s stagger, one gold word: CLAUDE.md recipe step 6); soft light leak between clips
(`library/blocks/light-leak-portrait.html`); warm grade via `npx hyperframes grade-compare`. Music: a slow track from
`library/music/cc0` or a sung line from `library/music/desi-vocal`.

## 2. Shayari / "Arz kiya hai" black-screen reel
Why: CapCut tags "Instagram Trend Reels Shayari" and "Trending Instagram Reel Black Screen"; "Arz Kiya" template 1.4M uses [T2].
How: HyperFrames scene, black background, 2-4 lines of the client's own (or public-domain) poetry in Noto Nastaliq Urdu
centred inside the safe zone, Roman Urdu line under it; each line fades in on a beat. Voice: if the client recorded it,
`clean_voice.py`; else `vs_tts.py` (Urdu) or `ai_voice.py` (spoken, no music). A public-domain ghazal record from
`library/music/desi-vocal` can sit underneath for a vintage feel (scratchy 78 rpm sound: say so to the client).

## 3. Beat-sync photo dump / slideshow
Why: "Trending Reels With Photos" tag [T2]; beat-sync & fast-cut and multi-clip (10-20 clips) are CapCut's top template
types [T2]; rajantemplate suggests 6-15 photos/clips, polaroid stack, film strip [T2].
How: pick BPM, cut on bars (CLAUDE.md recipe step 2); find the music's hits with `npx hyperframes audio <file>` and
place a photo change on each; ken-burns push-in per photo (scale tween on a wrapper div, CLAUDE.md step 5); flash on
the drop (`library/blocks/flash-warm.html`). Template to copy from: `library/templates/phone-clip-reel/build.py`
(one bar per shot, words(), scene()).

## 4. Wedding highlight (90 s vertical)
Why: couples want a ~90 s vertical film next to the long one [T3 barakaevents]; 60-90 s, hook = vow/first-look audio,
30-45 cuts/min, music ducked -9 dB under speech, names/date/venue at the END [T3 aisle.studio].
How: phone-clip-reel structure with more shots; drone or widest shot first (drone pull-back opener [T3]); slow-mo for
emotion (CLAUDE.md minterpolate); film-look warm grade or moody dark grade for evening functions [T3 hamzasproduction],
compared on a real frame with `grade-compare`; spoken lines cleaned with `clean_voice.py`; mix with
`voice_over_music.py` (duck_db -9). `floating_hearts.py` for the end card. End card: couple names + date + venue.

## 5. Mehndi / dholki teaser (15-30 s)
Why: teaser length 15-30 s [T3 aisle.studio]. No Pakistan-specific mehndi editing source found (unverified beyond that).
How: 10-15 cuts on a dhol pattern: `desi-eastern--damal-drumming-lahore.mp3` or `desi-eastern--wedding-ceremony-music.mp3`
(both CC0, verified, library/music/cc0); flash transitions on accents; one title at 0 s.

## 6. Shop / boutique new-stock reel with price
Why: English + Roman Urdu captions with a clear price [T3 sitey.pk]; fashion: outfit transitions, "one piece five ways",
Eid/festive moments [T3 gameofbranding].
How: one product per bar; price card ("Rs 4,500") as a big Anton number with the gold accent; last 3 s = address +
WhatsApp lower-third. `bg_blur.py` if the shop background is messy (owner-approved recipe, show before/after first).

## 7. Real-estate walkthrough
Why: first 3 s = size + sector/phase + PKR price as high-contrast text; lens/exposure fix; Urdu lapel VO over ambient
at 15-20%; permanent contact lower-third at the end [T3 mediaintiation].
How: HyperFrames title over the first clip; grade lifts shadows (`grade-compare` with an exposure/shadows-up candidate);
VO: client's own voice via `clean_voice.py`, else `vs_tts.py --model voxcpm2` for paid work (OmniVoice weights are
non-commercial: CLAUDE.md); bed at 0.15-0.2 under the voice with `voice_over_music.py`.

## 8. Restaurant "kitchen process" reel (30 s)
Why: 30-second kitchen clips of the signature dish beat photos [T3 loopverses]; process + first-bite + Urdu/Hinglish
captions [T3 gameofbranding].
How: 6-8 close shots, speed ramp (fast prep, slow pour/sizzle: minterpolate), hard cut to the first bite on the drop;
captions in Roman Urdu; end card with the dish name + price.

## 9. Eid transition reel (before/after outfit)
Why: "Eid is incomplete without the transition videos" (#pakistan #karachi reel) [T3]; "Eid Template 2026" 148.4K uses [T2].
How: two clips with matched framing; match cut or flash on the beat (`flash-warm.html`); zoom-through transition from
the phone-clip-reel template; gold accent text "Eid Mubarak".

## 10. Hook-first talking head (business tip)
Why: hook formulas: bold claim, curiosity gap, visual transformation; text by 2 s [T3 gameofbranding]; Instagram:
check skip rate for hook strength [T1].
How: clean the client's audio with `clean_voice.py`; transcribe with Whisper; per-word captions (CLAUDE.md step 6)
placed in the centre band [T1 safe zone]; punch-in zoom (scale 1.0 -> 1.12) on each key word.

## 11. Freeze-frame name card
Why: freeze frame is now built into Instagram's Edits app [T1] and in rajantemplate's list [T2].
How: CLAUDE.md recipe step 3 (end the slow-mo clip on the chosen frame, export PNG, place it seamlessly); name/label
slides in over the frozen frame.

## 12. Black & white to colour reveal
Why: listed in rajantemplate's 2026 trend edits [T2].
How: first 1-2 s of the hero clip with a desaturated grade, cut/flash to the full colour grade on the beat.

## 13. Lyrics reel with a public-domain classic
Why: "Minimal Lyrics" edit type [T2]; song-line titles dominate the CapCut list [T2].
How: a 15-30 s excerpt from `library/music/desi-vocal` (e.g. a Janki Bai ghazal, 1916); show the sung line in Nastaliq +
Roman Urdu when it is sung (find the time with Whisper on a denoised copy: measured in desi-vocal README). Tell the
client it is a 100-year-old recording (sound is scratchy, mono).

## 14. Pashto-audience version of any recipe
Why: Pashto trending results on YouTube were mostly new Pashto songs, some AI-made [T3]. No public-domain Pashto song
with vocals was found (see library/music/desi-vocal/README.md).
How: captions in Roman Urdu or Pashto script; a Pashto voice line via `vs_tts.py` (Pashto 81% Whisper match, CLAUDE.md);
"Manana" (thank you) end line (CLAUDE.md); music: `library/music/cc0` instrumental. A Pashto SONG with vocals: only
if the client provides one they own, or the owner explicitly asks us to make one.

## 15. Same-day wedding edit (2-4 min)
Why: same-day edits of 2-4 min shown at the reception/walima are a requested add-on [T3 hamzasproduction].
How: same as recipe 4 but 2-4 min, 16:9 copy for the venue screen plus the 9:16 reel; render both from one HyperFrames
project with two root sizes. (We have no measured render time for a 3 min film on this box: check before promising same-day.)

## 16. Weekly-trend format (Later's list)
Why: Later publishes current Reels trend formats weekly [T3].
How: read https://later.com/blog/instagram-reels-trends/ with `agent-reach read` at the start of the job; rebuild the
format with HyperFrames (text-first hook, rapid photo run) and our no-credit music.

## Posting tips to pass to the client (sourced)
- Evening is the shared peak in both Pakistani sources (after Maghrib/Isha to midnight; 8-11 pm) [T3]; one source also
  lists 9-11 am and 1-2 pm.
- Post the same 1080x1920 file to Reels, TikTok and Shorts [T3 aisle.studio].
- Tag the venue/vendors on wedding reels; client posts first, editor 24 h later [T3 aisle.studio].
