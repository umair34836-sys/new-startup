# Video editing knowledge base

Built 2026-10-24 by an editing self-study session (owner asked: learn how to turn a simple video into a
professional one, how to edit from scratch, and 500+ skills, so future sessions can judge quickly how to handle
any video). Owner rule: every claim has a reference (web source with URL/date, ffmpeg docs + a local test run,
or a section of this repo's own tested notes). Skill that points here: `.claude/skills/video-edit-playbook`.

## Files

| File | Read it when |
| --- | --- |
| [decision-guide.md](decision-guide.md) | A video arrived: input-triage table, then 29 video types (talking head, podcast, wedding, event, product/UGC ad, real estate, gaming/Minecraft, music video, tutorial, faceless, Pakistani/Indian reel style, client phone-clip reel, ...) each with goal, length/aspect, beat map, cut rhythm, transitions, grade, captions, music/SFX, mistakes and steps with this repo's tools. |
| [from-scratch.md](from-scratch.md) | There is no footage: format, script (words per minute), storyboard, no-credit visuals (licence checks for Pexels, Pixabay, Wikimedia, NASA, Openverse, archive.org), generated visuals, voice, CC0 music, HyperFrames assembly, loudness, export, QA. |
| [skills-catalog.md](skills-catalog.md) | Index of the 560 numbered skills in `skills/01..06`. |
| `skills/*.md` | You need one technique: grep it. |
| [skills2/README.md](skills2/README.md) | 4,832 more skills (#561-5556, 21 categories: NLE translation, colour science, looks, restoration, dialogue, mix/master, sound design, music, kinetic type, captions incl. Urdu/Hindi, VFX, AE/CapCut effects, reframe/speed, story by genre, retention, thumbnails, delivery, workflow, client business, Pakistani/Indian styles, ffmpeg filters). Each has a **How:** step; 2,705 commands were tested here. Search: `python3 library/tools/find_skill.py "<words>"`. |

## Fast path

1. Triage the video (`.claude/skills/video-edit-playbook/SKILL.md` section 1).
2. Find its type in `decision-guide.md`, follow "Steps here".
3. Look up any technique: `python3 library/tools/find_skill.py "<words>"` (searches skills/ and skills2/, add `--tested`
   for commands that ran here).
4. Save anything new that worked or failed back here with source and date.

## Research notes

- Tested here on 2026-10-24: with 11+ research agents in parallel, Exa search and the jina reader were rate-limited for most of the run;
  agents found URLs with WebSearch and read the pages with curl / headless Chromium instead (skills2 headers say which).
- Tested here on 2026-10-24: `agent-reach web search` (Exa) worked for ~250 queries in parallel (xargs -P 6) on 2026-10-24.
- Tested here on 2026-10-24: YouTube subtitles via `agent-reach youtube subtitle` hit HTTP 429 after the first video and the channel paused
  for 3,599 s (2026-10-24), so this study used web pages, not YouTube transcripts. Next time: fetch at most a few
  subtitles, spaced out.
