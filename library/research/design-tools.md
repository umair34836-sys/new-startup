# Design tools for thumbnails, covers and art (2026-10-28)

The owner asked on 2026-10-28: "Now install tools skills for designing skills for designer for tumbnails for art".
What is now in the repo:
- skill `.claude/skills/thumbnail-design`
- template `library/templates/thumbnail`
- tools `thumb_frames.py`, `thumb_cutout.py`, `thumb_make.py`, `thumb_check.py`
- 4 fonts
- the MediaPipe face landmarker model

## What was installed / made (measured here 2026-10-28)

**MediaPipe FaceLandmarker model `face_landmarker.task`**
- Source: storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/. Licence: Apache-2.0 (MediaPipe).
- Download: HTTP 200, 3,758,596 bytes.
- Saved to /home/user/tools/perc-models/ and added to setup-specialist-a.sh.
- The perc-venv already had mediapipe 1.1.1 (`import mediapipe`, 2026-10-28). FaceLandmarker and FaceDetector are present in `mediapipe.tasks.python.vision`.

**Fonts from github.com/google/fonts (raw.githubusercontent, HTTP 200)**

| Font | File | Bytes | Licence |
|---|---|---|---|
| Bebas Neue | ofl/bebasneue | 61,400 | OFL, "Copyright © 2010 by Dharma Type" |
| Luckiest Guy | apache/luckiestguy | 73,320 | Apache-2.0 |
| Bangers | ofl/bangers | 93,148 | OFL |
| Montserrat variable | ofl/montserrat | 744,936 | OFL |

Each licence file is saved beside its font in library/fonts.

**Tools (our own code)**
- thumb_frames.py: a 20 s 720p clip took 3 s for 39 frames.
- thumb_cutout.py: rembg u2net_human_seg, 22 s for one frame including the model load.
- thumb_make.py: 2 s per render.
- thumb_check.py: under 1 s.
- Tests passed for a 16:9 face thumbnail, a 9:16 cover with Urdu Nastaliq text, and a 1:1 poster. The thumbnails were looked at.

## Checked and NOT installed

| Tool | Why not |
|---|---|
| aabrole/claude-video-thumbnail-skill (MIT; cloned 2026-10-28) | Generation needs `GEMINI_API_KEY`, which its .env.example says is pay-as-you-go billing (Gemini 3 Pro Image). It is not free, and the owner wants free tools. |
| Image generators (Stable Diffusion family, FLUX, ...) | Not tried: this box has no GPU, 4 cores, and 3.8 GB free disk (df 2026-10-28). |
| Real-ESRGAN upscaler (BSD-3-Clause per secondary sources) | Its FAQ says CPU needs `--fp32` and is "extremely slow"; a Hugging Face demo reports ~30-60 s for 512 px x4 (WebSearch 2026-10-28). Not needed for 1280x720 thumbnails made from 720p or 1080p frames. |
| Other GitHub thumbnail makers (preangelleo/youtube-thumbnail-generator, remvisual/podcast-thumbnail-extractor, ekkolon/youtube-thumbnail-generator, miguelgargallo/youtube-thumbnail-maker) | None does frame pick + cutout + outlined text + checks in one place (WebSearch summary 2026-10-28, repos not opened). Our tools cover that with libraries already installed here. |

## Not reachable on 2026-10-28
- Openverse API: the request failed (no JSON returned).
- Wikimedia Commons API: no JSON returned.
- The Mr Aloo session saw Openverse 504 and Wikimedia rate limits on the same day.
- Test media came from Mixkit instead: clip 41165 from library/stock/mixkit-links.json, used in the scratchpad only.

## Paid / account options that already exist as connectors
Not used without the owner asking:
- Canva MCP: create, edit, export designs; uses the owner's Canva account.
- Aiwings `generate_image`: AI image generation; check credits with `get_credits`.
- gallery `design_image`: the owner's Future Gallery Pro editor.

Sources:
- [MediaPipe face landmarker model (Google storage)](https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task)
- [google/fonts](https://github.com/google/fonts)
- [aabrole/claude-video-thumbnail-skill](https://github.com/aabrole/claude-video-thumbnail-skill)
- [Real-ESRGAN FAQ (mintlify mirror)](https://mintlify.com/xinntao/Real-ESRGAN/resources/faq)
- [pypi youtube-thumbnail-generator](https://pypi.org/project/youtube-thumbnail-generator/2.2.4/)
