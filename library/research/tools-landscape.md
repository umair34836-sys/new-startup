# Open-source tools researched

Stars and licences re-checked 2026-10-24 with `agent-reach web search "<owner/repo> github"` (Exa index; star counts
are Exa's latest snapshot, not live GitHub: github.com and its API are blocked for repos outside this session).
Versions re-checked the same day with `npm view` / pypi.org JSON / `git clone --depth 1`.

## Songs with vocals (lyrics -> song)
- ace-step/ACE-Step-1.5: 13,969 stars, MIT. Runs on CPU with `--quantization int8_weight_only` (option present in the
  repo; CPU runs measured here Oct 2026, see CLAUDE.md). INSTALLED, our choice (ai_song.py). Vocal languages
  (acestep/constants.py VALID_LANGUAGES, clone 2026-10-24): 50 codes incl. 'ur', 'hi', 'pa', 'fa', no Pashto ('ps').
- multimodal-art-projection/YuE: 12,618 stars, Apache-2.0. "Heavy, GPU-oriented": our impression, unverified.
- ace-step/ACE-Step (v1): 4,966 stars, Apache-2.0. ASLP-lab/DiffRhythm: 2,353 stars, Apache-2.0, diffusion model for
  full-length songs (its README).
- List of related projects: github.com/ace-step/awesome-ace-step (162 stars, CC0).

## Transcription
- openai/whisper: 111,152 stars, MIT. INSTALLED (small model, word timestamps). small.pt = 483,617,219 bytes
  (461 MiB; `curl -I` of the URL in whisper/__init__.py, 2026-10-24).

## Agent tools
- Panniantong/Agent-Reach: 101,393 stars, MIT. INSTALLED (version 1.6.0 per `agent-reach doctor`, 2026-10-24).
  Read-only web/YouTube/Reddit/GitHub/X access. The PyPI package "agent-reach" (0.1.0, "Give an agent the channels it
  needs") is a DIFFERENT project (pypi.org JSON 2026-10-24): install only from the GitHub release zip.
- NanoNets/Graft (npm @nanonets/graft 0.25.0, MIT; npm repository field now points to trailhq/Trail-Code): 10,546 stars
  (Trail-Code 10,691). INSTALLED. Vendor claims (npm README, self-reported): "up to 4x tokens saved"; "across 162 runs:
  32% lower cost, 60% less time".
- headroomlabs-ai/headroom: 77,670 stars, Apache-2.0: "Compress tool outputs, logs, files, and RAG chunks before they
  reach the LLM" (repo description). Not installed.
- "graftv": no such GitHub project found in an Oct 2026 search (past search, not repeated).
- heygen-com/hyperframes: 70,877 stars, Apache-2.0. Repo uses `npx hyperframes@0.8.188` (exists on npm; latest 0.8.191
  on 2026-10-24).

## Added Oct 23 2026
- affaan-m/everything-claude-code (ECC), MIT: Exa shows 130,679 stars for that URL and 287,456 for github.com/affaan-m/ecc
  (probably the same repo renamed; unverified). INSTALLED into this repo's .claude/ (owner said yes): agents-core,
  commands-core, workflow-quality only. Commit 93862a1 added 53 skills, 71 agents, 97 commands (`git show --name-only
  93862a1`, counted 2026-10-24); no hook runtime and no language rule packs. Reinstall/update: `bash
  /home/user/tools/ECC/install.sh --target claude-project --modules agents-core,commands-core,workflow-quality`
  (clone github.com/affaan-m/everything-claude-code first).
- morluto/rea "Reverse Engineer Anything": 374,315 stars (Oct 2026 note: it jumped from 41 to 300k+ that month: treat
  the hype with care), MIT, npm rea-agents 6.7.0 (MIT). INSTALLED: CLI `rea`, MCP server in .mcp.json
  (`npx -y rea-agents@6.7.0 mcp`), skill in .claude/skills/reverse-engineer-anything. Native binaries need
  Hopper/Ghidra/IDA (not installed); JS/Electron, Go, PyInstaller, WASM, Android need none or caller-supplied tools (per
  its docs, Oct 2026; not re-read). Only analyse software we are allowed to. aliyenidede/rea (rea-dev on PyPI) is a
  different, deprecated project (Oct 2026 note, not re-checked).
- nomadkaraoke/python-audio-separator (1,438 stars, MIT; PyPI audio-separator latest 0.47.1) + BS-RoFormer
  `model_bs_roformer_ep_368_sdr_12.9628.ckpt`: median vocals SDR 12.10 in the package's models-scores.json (0.47.1
  wheel, 2026-10-24). INSTALLED in the tools venv. Measured here Oct 2026: removes music completely (silent gaps at
  -180 dB after denoise) but slow on CPU (~6 min per 20 s clip).

## Firecrawl replacements (Oct 24 2026, via Agent-Reach web search)
- D4Vinci/Scrapling: 89,308 stars, BSD-3-Clause; adaptive scraping framework (stealth fetchers). Not installed.
- unclecode/crawl4ai: 86,051 stars, Apache-2.0, v0.9.5 (PyPI latest on 2026-10-24). INSTALLED in
  /home/user/tools/crawl-venv with playwright==1.56.0. Wrapper: library/tools/web_capture.py.
  Oct 24 2026 (earlier session): /opt/pw-browsers had chromium-1194, which matched playwright 1.56.0; tested
  huggingface.co/ace-step -> 10.6k chars + 1440x1524 PNG.
  AUDIT 2026-10-24 (this session): /opt/pw-browsers holds chromium-1243 (system playwright 1.63.0), so web_capture.py
  FAILED with "playwright install" (measured: `crawl-venv/bin/python web_capture.py https://www.firecraft.fun --out ...`).
  The browser build depends on the container image: check `ls /opt/pw-browsers` and match the playwright version.
  Workaround that worked the same day: `agent-reach read <url>` (Jina) or plain curl of the HTML.
  FIX 2026-10-24 (main session): web_capture.py now falls back to launching the image's own Chromium
  (/opt/pw-browsers/chromium-*/chrome-linux*/chrome) with --remote-debugging-port and attaching Crawl4AI over CDP
  (BrowserConfig browser_mode="cdp", cdp_url, cdp_cleanup_on_close=True). Tested here 2026-10-24 on https://example.com
  with chromium-1194 hidden: 953 chars + PNG, no errors.
  Fails on Cloudflare JS challenges (pixabay.com returned 403 to curl too, 2026-10-24).
  Firecrawl itself is open source too but heavy to self-host (Docker stack; not checked in detail).
- Small Firecrawl-compatible clones (us/crw in Rust, servo-fetch, beecrawl): too few stars to rely on (Oct 2026 search,
  counts not recorded).
