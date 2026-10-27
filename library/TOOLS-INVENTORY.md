# Everything we have: tools, models, skills, scripts (inventory)

This list was made on 2026-10-27 because the owner asked: "Hamare pass jitne bhi tools repo skills models hai subko hamare repo k
under clone kerne ki try kro ... or sare tools sub kuch ki list file bana ker repo me save bhi kerdo".
Sizes were measured here on 2026-10-27 with `du -sh` in this container. Licences come from the research notes named
beside each one. "not checked" means nobody verified it yet.

## Why the big tools are NOT copied into this repo

Everything below `/home/user/tools` plus its caches adds up to about 23 GB in this container. Measured on 2026-10-27:
- tools: 14 GB
- Hugging Face cache: 4.7 GB
- pnpm store: 2.7 GB
- Whisper: 0.46 GB
- npm: 0.5 GB

The ACE-Step checkpoints (6.0 GB) had been deleted earlier that day.

Four things block putting this into the repo:
1. **GitHub file size limit.** GitHub rejects any file over 100 MB. `find -size +100M` found 20 such files here. The largest is the VoxCPM2 weight blob (4,368 MB). Others include libtorch_cpu.so (423 MB), whisper small.pt (461 MB) and the separator models (610 / 871 MB).
2. **Repo size.** The repo's .git is already 903 MB. Adding ~23 GB would make every clone at session start slower than installing.
3. **Python venvs can't be copied.** They break when moved to another path or Python build.
4. **The repo is public.** Copying third-party weights and code into it is redistribution, and some licences forbid it. For example, VoiceStudio's OmniVoice weights are NON-COMMERCIAL (research/voicestudio.md), and the YouTube Audio Library and Mixkit files have no-redistribution terms (music/owner-drive/README.md).

So the repo keeps the INSTALL RECIPE instead: `library/tools/setup-all.sh`, which the SessionStart hook runs. Small reusable assets do live in `library/`:
- music, sfx, fonts, emoji/icons, LUTs, blocks, templates
- arnndn models in `library/models/` (7.1 MB)

## Installed tools (`/home/user/tools`, by setup-all.sh)

| Tool | What it does | Where | Size | Installed by | Licence |
|---|---|---|---|---|---|
| ffmpeg, PIL, numpy, mido, pyworld, fonttools, pysubs2 | media + analysis basics for library/tools scripts | system | - | setup-all light | not checked |
| uv | Python env manager | ~/.local/bin | - | setup-all light | not checked |
| Agent-Reach | web search/read, YouTube search (free, instead of Firecrawl) | /home/user/tools/Agent-Reach | 2.3 MB | setup-all light | not checked |
| graft 0.25 | code context graph | npm global | - | setup-all light | not checked |
| REA (rea-agents 6.7.0) | reverse engineering CLI + MCP | npm global | - | setup-all light | not checked |
| specialist D tools | Urdu/Pashto/Hindi captions, brand kit (qrcode etc.) | system python | - | setup-specialist-d.sh | not checked |
| perc-venv + perc-models | listen.py / watch.py / fast_matte.py (BPM, LUFS, VAD, faces, mattes) | /home/user/tools/perc-venv, perc-models | 1.3 GB + 22 MB | setup-specialist-a.sh | research/perception-tools.md |
| crawl-venv (Crawl4AI + playwright 1.56.0) | web_capture.py page capture | /home/user/tools/crawl-venv | 697 MB | setup-all light | not checked |
| main venv (torch CPU, Whisper, ACE-Step, audio-separator, rembg, yt-dlp, curl_cffi, gdown, pyworld) | songs, transcription, vocal separation, bg blur, downloads | /home/user/tools/venv | 2.0 GB | setup-music.sh, setup-ai-song.sh, setup-all heavy | Whisper MIT, ACE-Step MIT (CLAUDE.md) |
| ACE-Step 1.5 code (+ checkpoints) | AI songs with vocals | /home/user/tools/ACE-Step-1.5 | 32 MB (checkpoints 6.0 GB, deleted here 2026-10-27) | setup-ai-song.sh + heavy | MIT (CLAUDE.md) |
| sep-models | BS-RoFormer, denoise, de-reverb, MDX-Net vocal models | /home/user/tools/sep-models | 1.6 GB | setup-all heavy | not checked |
| VoiceStudio (+ VoxCPM2) | free voiceover: design + cloning (vs_tts.py) | /home/user/tools/VoiceStudio | 3.1 GB (+ VoxCPM2 4.7 GB in ~/.cache/huggingface) | setup-all heavy | OmniVoice non-commercial; VoxCPM2 Apache-2.0 (research/voicestudio.md) |
| saved voices | voice references rebuilt from voices.json | /home/user/tools/voices | 58 MB | vs_tts.py on first use | client/AI voices, never committed |
| Artemis | AI agent that uses an Android phone | /home/user/tools/artemis | 1.2 GB | setup-all heavy | Apache-2.0 (research/artemis.md) |
| Node 24 | runtime for OpenDesign | /home/user/tools/node24 | 208 MB | setup-all heavy | not checked |
| OpenDesign | AI design agent workspace (od CLI / MCP) | /home/user/tools/open-design | 3.8 GB (+ pnpm store 2.7 GB) | setup-all heavy | Apache-2.0 (research/open-design.md) |
| HyperFrames + its Chrome | HTML -> video renders (npx hyperframes) | ~/.npm/_npx, ~/.cache/hyperframes | 0.5 + 0.4 GB | npx on first use / SessionStart hook | not checked |

## Models (weights)
| Model | Used for | Where | Size |
|---|---|---|---|
| VoxCPM2 (openbmb) | default free voice, cloning | ~/.cache/huggingface | 4.7 GB |
| Whisper small (+ medium when used) | transcription, VO checks | ~/.cache/whisper | 0.46 GB |
| ACE-Step turbo + VAE + text encoder + LM | ai_song.py | /home/user/tools/ACE-Step-1.5/checkpoints | 6.0 GB (deleted here 2026-10-27; setup-all heavy re-downloads) |
| BS-RoFormer, denoise mel-band RoFormer, UVR-DeEcho-DeReverb, UVR-MDX-NET-Voc_FT | clean_voice.py, ai_song.py | /home/user/tools/sep-models | 1.6 GB |
| silero_vad, blaze_face, efficientdet_lite0, selfie_segmenter, rvm_mobilenetv3 | listen.py / watch.py / fast_matte.py | /home/user/tools/perc-models | 22 MB |
| u2net_human_seg | bg_blur.py (downloads on first use; not present in this container on 2026-10-27) | rembg default cache | 168 MiB (CLAUDE.md) |
| arnndn (rnnoise) | ffmpeg denoise | library/models/arnndn (in the repo) | 7.1 MB folder |

## Our scripts (in the repo: library/tools, 42 entries)
ai_song.py, ai_voice.py, align_lyrics.py, bg_blur.py, blocky_character.py, clean_voice.py, ember_background.py,
fast_matte.py, find_skill.py, find_stock.py, floating_hearts.py, listen.py, lut_preview.py, magenta/, make_girl_skin.py,
make_luts.py, make_overlays.py, music_pack.py, romance_synth.py, screen_recorder.js, setup-agent-tools.sh,
setup-ai-song.sh, setup-all.sh, setup-music.sh, setup-specialist-a.sh, setup-specialist-d.sh, sfx_prep.py,
stock_prep.py, synth_sfx.py, urdu_captions.py, vo_join.py, voice_over_music.py, voicestudio.sh, voxel_textures.py,
voxel_world.py, vs_tts.py, watch.py, watermark.py, wcheck_lines.py, web_capture.py, youtube_chapters.py, bench/.
What each one does and how to run it is in `library/README.md` ("Tools").

## Skills (in the repo: .claude/skills, 66)

**Video work, used by the owner's rules:**
- video-edit-playbook, desi-reels, listen-and-watch, stock-sfx-luts, voice-or-song, clean-video-voice, urdu-captions, client-brand-kit
- HyperFrames: hyperframes, hyperframes-cli, hyperframes-registry, media-use
- reverse-engineer-anything (REA)

**General coding/agent skills (ECC = everything-claude-code):**
- agent-introspection-debugging, agent-self-evaluation, agent-sort, ai-regression-testing, architecture-decision-records, brownfield-retrospective
- browser-qa, ck, click-path-audit, code-tour, codebase-onboarding, codehealth-mcp, config-gc, configure-ecc, context-budget
- continuous-learning, continuous-learning-v2, conventional-commit-review, council, council-multi-model, deepseek-harness-setup
- delivery-gate, dev-team, e2e-testing, ecc-guide, ecc-recipes, error-handling, eval-harness, git-workflow, growth-log, hookify-rules
- inherit-legacy-style, intent-driven-development, iterative-retrieval, living-docs-governance, loop-design-check, plan-canvas
- plankton-code-quality, product-lens, production-audit, repo-scan, rules-distill, santa-method, skill-comply, skill-host-compat
- skill-scout, skill-stocktake, story-lifecycle, strategic-compact, tdd-workflow, unified-memory, verification-loop, windows-desktop-e2e

## Templates and asset libraries (in the repo)
- **Templates:** `library/templates/` has 13 folders (blocky-monsoon, blocky-walk, brand-kit, explainer-host-steps, food-promo-reel, hosting-promo-reel, kinetic-laptop-type, kinetic-type-reel, minecraft-smp-short, phone-clip-reel, screen-tutorial, typewriter-reel, website-promo).
- **Assets:** music (CC0), sfx, memes, stock, luts, fonts, emoji, elements (icons), blocks, characters, textures, voices registry. All are listed in `library/README.md`.
- **Owner's Drive music:** indexed in `library/music/owner-drive/README.md`. The files stay on Drive.
