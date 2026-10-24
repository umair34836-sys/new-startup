# Video editing knowledge base

Built 2026-10-24 by an editing self-study session (owner asked: learn how to turn a simple video into a
professional one, how to edit from scratch, and 500+ skills, so future sessions can judge quickly how to handle
any video). Owner rule: every claim has a reference (web source with URL/date, ffmpeg docs + a local test run,
or a section of this repo's own tested notes). Skill that points here: `.claude/skills/video-edit-playbook`.

## Files

| File | Read it when |
| --- | --- |
| [decision-guide.md](decision-guide.md) | A video arrived: input-triage table, then 29 video types (talking head, podcast, wedding, event, product/UGC ad, real estate, gaming/Minecraft, music video, tutorial, faceless, Pakistani/Indian reel style, client phone-clip reel, ...) each with goal, structure (beat map), cut rhythm, transitions, mistakes and steps with this repo's tools, plus length/aspect, grade, captions and music/SFX where the sources covered them (counted 2026-10-24: "Grade:" in 9 of 29 sections, "Captions:" in 17, "Music/SFX:" in 14). |
| [from-scratch.md](from-scratch.md) | There is no footage: format, script (words per minute), storyboard, no-credit visuals (licence checks for Pexels, Pixabay, Wikimedia, NASA, Openverse, archive.org), generated visuals, voice, CC0 music, HyperFrames assembly, loudness, export, QA. |
| [skills-catalog.md](skills-catalog.md) | Index of the 560 numbered skills in `skills/01..06`. |
| `skills/*.md` | You need one technique: grep it. |

## Fast path

1. Triage the video (`.claude/skills/video-edit-playbook/SKILL.md` section 1).
2. Find its type in `decision-guide.md`, follow "Steps here".
3. Look up any technique in `skills/` by grep.
4. Save anything new that worked or failed back here with source and date.

## Research notes

- Tested here on 2026-10-24 (self-study session, past observation, not re-counted): `agent-reach web search` (Exa) worked for ~250 queries in parallel (xargs -P 6).
- Observed here on 2026-10-24 (audit session): after that day's heavy use, `agent-reach web search` and `agent-reach read`
  both returned `RATE_LIMITED` ("Wait 2872 seconds before retrying this channel"); WebSearch/WebFetch and direct curl
  were used instead.
- Tested here on 2026-10-24 (self-study session, past observation, not re-tested in the audit): YouTube subtitles via `agent-reach youtube subtitle` hit HTTP 429 after the first video and the channel paused
  for 3,599 s (2026-10-24), so this study used web pages, not YouTube transcripts. Next time: fetch at most a few
  subtitles, spaced out.
