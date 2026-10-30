---
name: music-for-video
description: Pick, cut and mix background music like a professional editor for any video (promo, hosting/tech, food, tutorial, explainer, gaming/Minecraft, emotional, wedding/desi, kids/funny, luxury, news/announcement, brand reveal, showreel). Use whenever a video needs music or the owner says "music lagao", "gaana lagao", "background music", "music theek nahi", "music change karo", or asks about BPM, beat cuts, the drop, ducking, music too loud/quiet under the voice, or music length/ending.
---

# Music for video (professional workflow)

OWNER (2026-10-27): sessions picked music that did not fit the situation or the video type. Never pick a track by its
folder name or by habit. Follow these 8 steps every time and write the reasons in the edit log.
Research behind every rule: `library/research/music-for-video.md` (sources + dates). Worked examples with measurements:
`library/research/music-for-video-tests.md`. Catalogue of every usable track: `library/music/catalogue.md`.

Tools (perc-venv python = `/home/user/tools/perc-venv/bin/python`; needs setup-all light, flag
`/home/user/tools/.specialist-a-ready`):
- `python3 library/tools/find_music.py "<type / mood words>" [--length 30] [--client] [--vo|--no-vo] [--drop] [--platform youtube]`
- `$PY library/tools/listen.py track.mp3 --no-words` (skill listen-and-watch)
- `$PY library/tools/music_fit.py track.mp3 bed.wav --length 30 [--drop-at 7.4] [--end resolve|fade|cut] --check`
- `$PY library/tools/mix_vo_music.py vo.wav bed.wav mix.wav [--gap 15 --duck-db -10 --lufs -16]`

## 1. Know the video first

Write down: video type (one of the table in music-for-video.md section 2), the ONE emotion word, length in seconds,
platform (YouTube / Reels / TikTok / WhatsApp), client or owner's own video, and the structure with times:
hook (0-3 s), sections, the reveal/key moment (logo, price, offer, result), CTA/end card, where the voice-over talks.
Client work = `--client` (CC0/PD only). A VO = no vocals in the music (sources: BBC, PremiumBeat, Musicbed).
Ask: does this video need music at all, or only in the bookends? (BBC, PremiumBeat: section 7.)

## 2. Shortlist with find_music.py

`python3 library/tools/find_music.py "hosting promo" --length 30 --client --vo`
It filters by licence (client, YouTube-only, own tracks), drops vocal tracks under a VO, and ranks by type tag, energy,
tempo band, steady beat grid, real ending, drop, fast intro and (under VO) a steady level. Read every "+" and "!" line.
Owner's own YouTube video: add `--platform youtube` to include his Drive tracks (YouTube Audio Library), fetched with
gdown (library/music/owner-drive/README.md). Own ACE-Step tracks only with `--own` when the owner asked.

## 3. Listen (measure) the top 2-3

Run listen.py on each. Check: tempo (and its half/double alternative), downbeats, sections, where the energy rises,
the ending, LUFS, any voice activity. Look at the short-term loudness curve around the moment you want to use.

## 4. Choose by documented reasons

Pick the one whose emotion, energy and tempo match the type row, whose arc fits the video (music "in" by ~1-2 s;
a drop or build for the reveal; a real ending or a usable hit), and that fits the brand (tech brand != Bollywood
groove; food: light/breezy or matching the cuisine). If nothing fits, fetch more no-credit tracks first: `python3 library/tools/fetch_free_music.py "<mood words>" --category <cat> --n 5` (FMA CC0/PD, licence re-checked per page), measure them with `music_catalogue.py --only`, run find_music.py again; if still nothing fits, say so to the owner instead of forcing one.

## 5. Fit it to the exact length (music_fit.py)

- Reveal / logo / price moment at T s: `--drop-at T` (the track's measured drop lands on it; pass `--src-drop` to use
  another moment, e.g. a section start from listen.py).
- Ending: `--end resolve` (default) keeps the composer's real ending; a loop or fade-out track ends on a downbeat hit
  with a ring-out. Never a fade in the middle of a phrase. `--end fade` only for a soft outro under an end card.
- If the edit allows, put the reveal ON the track's own drop time (or whole bars later): on tracks whose tempo
  changes at the drop, a repeated build bar is harder to check (tests file, test 3).
- Always `--check`: every join's `beat_phase_error_after_join_ms` must be close to `phase_error_no_edit_median_ms`
  (the tracker's own noise). If a join is far worse, move the drop/length by one bar or pick another track.
- Cut picture on bars only where the edit should be felt (music reels, section changes, the reveal); in VO videos cut
  on the voice and the action (The Power Edit: on-beat cuts call attention to themselves).

## 6. Level and duck under the voice

VO + music: `mix_vo_music.py vo.wav bed.wav mix.wav` (defaults: duck -10 dB, attack 60 ms, release 400 ms, 1.5-4 kHz dip
-4 dB under speech, voice 15 LU over the ducked bed, -16 LUFS integrated, -1 dBTP). Use the mix as the video's single
audio track (HyperFrames: one `<audio>` with the real `data-duration`). Lines cut from one take and placed by time:
`voice_over_music.py` instead. Music-only video (reveal, reel): normalise the fitted bed with `music_fit.py --lufs -16`.
SFX: keep impacts under the music (repo: impact-bass 0.35-0.4, whoosh 0.6-0.8 against music 1.0).

## 7. QA (measure, Claude can't listen)

`$PY library/tools/listen.py final.mp4 --no-words`: integrated LUFS -16..-14, true peak <= -1 dBTP, 0 clipped samples,
no loud/quiet jumps in the short-term curve (R 128 s1: short-term max about +5 LU over integrated). With a VO:
mix_vo_music's report `music_vs_vo_gap_lu` >= 12 (target 15), and Whisper words of the final match the script.
Music ends on its ending or hit, not cut off: the last second of the music is a decay, not full level.

## 8. Log it

In the client/job edit log: track id + licence, why it fits (type, emotion word, energy, BPM, brand), which part was
used (music_fit plan: segments, joins, drop time, ending), the mix numbers (gap, LUFS, peak), and what was rejected and
why. In the delivery message name this skill, the track and the tools used (CLAUDE.md SKILL-BASED ONLY).
New track added to library/music? Re-run `music_catalogue.py` so it is measured and searchable.
