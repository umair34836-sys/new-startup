---
name: thumbnail-design
description: Design YouTube thumbnails, Shorts/Reels/TikTok covers, Instagram/Facebook posts, posters and simple social art for the owner or a client - pick the best frame, cut the person out, build the layout (big outlined text, accent word, cutout with outline/glow, emoji, arrows, badge) and check how it reads at real phone sizes. Use for "thumbnail banao", "thumbnail design", "cover banao", "poster", "post design", "art banao", "Shorts cover", or after any video delivery that needs a thumbnail.
---

# Thumbnail and cover design

Owner (2026-10-28): "install tools skills for designing ... for thumbnails for art". All tools are local and free.
The knowledge base is `library/research/editing/skills2/16-thumbnails.md`: 239 cited rules covering specs, A/B tests, faces, composition, colour, text, small-size checks and Pakistani/Indian styles.
Search it with `python3 library/tools/find_skill.py "thumbnail <words>"`. The template and timings are in `library/templates/thumbnail/README.md`.

## 1. Brief (write it down first)
- Format:
  - 16:9 1280x720 for a long YouTube video;
  - 9:16 1080x1920 for a Shorts/Reels cover (a 16:9 thumbnail on a vertical video gets swapped, #4165);
  - 1:1 or 4:5 for posts.
- The ONE idea the thumbnail sells. Its text complements the title, never repeats it (see the research file, section "Text on thumbnails").
- At most 3 attention elements: face/emotion, big text or number, a graphic, an arrow or circle, colour contrast.
- Only show what is really in the video. Misleading thumbnails break YouTube policy (#4170).
- No gore or violence as the focal point (#4171). Never another creator's face or brand (#4173).
- Client work: use only the client's own material and the repo's licensed assets (emoji/icons in library/emoji and library/elements, CC0 stock). For the owner's own channel, his host skin and his footage.

## 2. Frame
`/home/user/tools/perc-venv/bin/python library/tools/thumb_frames.py video.mp4 work/frames --top 6`
Look at `work/frames/sheet.jpg` and pick by eye. Use the printed scores (sharp, expose, face, expr) as the reason in the edit log.
No usable frame: make a design-only layout (gradient, logo, product shot) instead of inventing a scene.

## 3. Cutout
`/home/user/tools/venv/bin/python library/tools/thumb_cutout.py frame.png work/cutout.png` (use `--model isnet-general-use` for objects or logos).
Open the cutout and check its edges. Hair and hands are where models fail; if it looks bad, use the frame without a cutout.

## 4. Build
Copy an example spec from `library/templates/thumbnail/` and edit it.
- Text: 2-4 words, at least ~110 px at 1280 wide, an outline of 8-14 px (doubled in CSS) and one accent word in a contrasting colour.
- Fonts in library/fonts: Anton, BebasNeue, LuckiestGuy, Bangers, Montserrat (900), Poppins, NotoNastaliqUrdu (Urdu; verified text only).
- Background: the frame blurred 10-16 px and darkened 0.3-0.4 when a cutout sits on top, or a brand gradient.
- Brand colours for clients: client-brand-kit skill or the client brief.

Run: `python3 library/tools/thumb_make.py work/spec.json work/thumb.png --variants`.

## 5. Check (always, and fix every issue)
`python3 library/tools/thumb_check.py work/thumb.png`. Then LOOK at `work/thumb_check.png`, which shows:
- 320x180, 168x94 and 120x90 versions: the text must still read at 168x94;
- a luminance-only version: the subject must separate from the background without colour;
- a 4:3 letterbox.

The JSON report lists contrast per text box, text running off the canvas, text too small on phones, size/ratio, and whether the JPG is under 2 MB.

## 6. Deliver
- Send the PNG (and the JPG for phone upload) with SendUserFile.
- For an A/B test: 3 variants that differ in ONE thing (text, face or colour), all >= 1280x720 (#4179-#4181).
- Name the tools and the frame time in the delivery message.
- Never commit the frames, cutouts or thumbnails (no photos in git); keep them in the scratchpad.

## When this is not enough
- Generated art (illustrations, AI images) cannot run locally on this CPU box.
- Connectors exist but use the owner's accounts or credits, so ask first: Canva (`mcp__Canva__*`), Aiwings image generation, and the gallery `design_image`.
- Never use another creator's thumbnail as a base.
