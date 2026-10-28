# Thumbnail / cover / poster template (added 2026-10-28)

The owner asked on 2026-10-28: "Now install tools skills for designing skills for designer for tumbnails for art".
Workflow and rules: skill `.claude/skills/thumbnail-design`. All four tools ran on this box on 2026-10-28 (timings below).

| Step | Tool | What it does | Measured here 2026-10-28 |
|---|---|---|---|
| 1. Pick frames | `thumb_frames.py` (perc-venv) | scores frames: sharpness, exposure, face size, expression (smile / jaw open / brows up; eyes closed = penalty) via MediaPipe FaceLandmarker | 20 s 720p clip, 39 frames in 3 s |
| 2. Cut out | `thumb_cutout.py` (venv, rembg u2net_human_seg) | transparent PNG trimmed to the person; drops stray islands under 3% of the biggest blob | 1280x720 frame in 22 s (incl. model load) |
| 3. Build | `thumb_make.py` (Node Playwright) | JSON spec -> PNG + JPG (< 2 MB) + text boxes | 2 s per render |
| 4. Check | `thumb_check.py` | size/ratio/file size, previews at the served sizes, WCAG contrast per text box | < 1 s |

```
P=/home/user/tools/perc-venv/bin/python; V=/home/user/tools/venv/bin/python
$P library/tools/thumb_frames.py video.mp4 work/frames --top 6        # look at work/frames/sheet.jpg
$V library/tools/thumb_cutout.py work/frames/pick01_*.png work/cutout.png
cp library/templates/thumbnail/yt-face.example.json work/spec.json      # edit texts, colours, paths
python3 library/tools/thumb_make.py work/spec.json work/thumb.png --variants
python3 library/tools/thumb_check.py work/thumb.png                    # look at work/thumb_check.png; fix every issue
```

## Example specs
- `yt-face.example.json`: 16:9 YouTube. Blurred and darkened frame behind, cutout on the right with a white outline and glow, two text lines (Anton with a yellow accent word; Montserrat on a yellow box), emoji, red arrow.
- `short-cover.example.json`: 9:16 Shorts/Reels cover. Gradient background, centred cutout, Luckiest Guy title, badge.
- `poster-art.example.json`: 1:1 post/poster without a person. Bebas Neue title, boxed line, emoji in a circle.

Paths inside a spec are relative to the spec file, or absolute.

## Learnings from the build (2026-10-28)
- An outline on the cutout made of 16 stacked CSS `drop-shadow()`s timed out Chromium's screenshot (> 30 s, then failed).
  thumb_make.py now draws the outline and glow with PIL (MaxFilter grow + blur), and the render takes 2 s.
- rembg left a separate fragment (part of a shoe) that the white outline turned into a visible island. thumb_cutout.py keeps only blobs >= 3% of the biggest one.
- Urdu in Noto Nastaliq Urdu rendered shaped in Chromium (test frame, 2026-10-28). Never write Urdu text that is not verified (CLAUDE.md).
- `thumb_check.py` compares boxed text with its box colour, not with the photo behind it. Without that, it flagged a boxed line wrongly (2.31 vs the real 14.67).

Test media: a Mixkit clip (41165, "Man answering a whatsapp", videoFree licence, links in library/stock/mixkit-links.json), used in the scratchpad only. No images are committed here.
