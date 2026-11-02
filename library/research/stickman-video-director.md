# Stickman Video Director (installed 2026-11-02)

The owner asked on 2026-11-02: "Now Install skaomei stikman-video-director tool from github".

## Source
- Repo: https://github.com/kaomei/stickman-video-director ("kaomei" / CrazyKaomei). Licence: MIT.
- Shallow clone on 2026-11-02, HEAD d19705dea434626d4fc6e651e24cdf23c7eba156 (Nov 1 2026).
- Stars: the README roadmap, as quoted in an Exa search snippet on 2026-11-02, shows the "3,000 Stars" step done and the
  "5,000 Stars" step open. The GitHub API is not open to this session, so there is no exact count.
- Skill name: `directing-stickman-videos`. Installed at .claude/skills/directing-stickman-videos (7.1 MB).
  The repo's 135 MB `assets/readme` previews were NOT copied.

## What it does (from its README + SKILL.md, read 2026-11-02)
- Turns a topic, article or script into a stickman video. 8 styles: Classic B&W, Modern Pop, Prehistoric Cave,
  Cozy Storytelling, Historical Cartoon, Minimal Hand-Drawn (B1), Amber Noir, Colorful Hand-Drawn (B2).
- **A · Director mode**: treatment, storyboard and scene-by-scene prompts for an outside video generator
  (Google Flow/Veo, Runway, Luma, Kling...). It does not render.
- **B · Autopilot mode**: makes a finished narrated, captioned video with a local renderer
  (Node 20+, FFmpeg, @napi-rs/canvas). The scene illustrations and the voice come from "the user's configured tools".
  - Defaults: Google Gemini TTS (voices Bodi / Fola / Puck) and Gemini images through `scripts/gemini-media.mjs`.
    These need GEMINI_API_KEY plus explicit network approval and may be billed.
  - User choice overrides the defaults.
- Captions: `scripts/align_captions.py`, optional Whisper (we already have it).

## Measured here 2026-11-02
- `bash library/tools/setup-stickman.sh`:
  - re-fetched the 3 git-ignored media files (b1 mp4 + 2 JPGs) from the pinned commit;
  - `npm ci` installed @napi-rs/canvas 0.1.100.
- `node scripts/autopilot.mjs doctor`: node, ffmpeg, ffprobe, canvas and fonts all true; gemini_key_present false.

## How it fits our rules
- Voice: use our free field voices (`vs_tts.py --voice ...`; promo-male banned), not Gemini. User choice overrides
  the skill's default.
- Images:
  - It needs an image source per scene. This box has no GPU and no free local image generator in the repo.
  - Paid/credit options that already exist as connectors: Aiwings `generate_image` (owner's credits) or Canva
    `generate-image`. Use them only when the owner says so.
  - Gemini images only with the owner's key and go-ahead.
- Music: CC0/PD only (music-for-video skill).
- Output: yuv420p + faststart and the white-label rules, as for every video.

## Image sources checked 2026-11-02 (owner: "Kia hum gallery connector ka pro editor use ker sakte hai for this ?")
- **Gallery `design_image` ("Pro editor")**, per its tool description:
  - It lays out a NEW picture from layers: photos already in the owner's backup, text and shapes on a colour,
    gradient or photo background.
  - It does NOT draw from a text prompt, so it cannot make new stickman illustrations.
  - It fits title cards, thumbnails and end cards.
  - get_account 2026-11-02: plan premium (ends 2026-11-14), 100 edits/day, 0 used.
- **B1 style**: `references/b1-minimal-handdrawn.md` says each story needs newly generated character poses and props
  ("generate the expressions, poses and prop interactions needed by that story"). So a real image generator is needed.
- **Aiwings** get_credits 2026-11-02:
  - 7 credits left (free plan); default GPT Image 2.5 Sunburst @ medium = 6 credits/image, so about 1 image.
  - Top up: https://aiwings.io/dashboard
