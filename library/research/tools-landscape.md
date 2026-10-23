# Open-source tools researched (stars as seen Oct 2026)

## Songs with vocals (lyrics -> song)
- ace-step/ACE-Step-1.5: 13.9k stars, MIT, runs on CPU (INT8). INSTALLED, our choice (see ai_song.py).
- multimodal-art-projection/YuE: 12.6k, Apache-2.0; heavy, GPU-oriented.
- ace-step/ACE-Step (v1): 5.0k. ASLP-lab/DiffRhythm: Apache-2.0, full-length songs via latent diffusion.
- List of related projects: github.com/ace-step/awesome-ace-step.

## Transcription
- openai/whisper: ~111k stars. INSTALLED (small model, word timestamps).

## Agent tools
- Panniantong/Agent-Reach: 101k stars, MIT. INSTALLED. Read-only web/YouTube/Reddit/GitHub/X access.
  The PyPI package "agent-reach" is a DIFFERENT project: install only from the GitHub release zip.
- NanoNets/Graft (now trailhq/Trail-Code): ~5-10k stars, MIT, npm @nanonets/graft. INSTALLED.
  Code context graph as markdown; vendor claims up to 4x cheaper / 3x faster agent runs.
- headroomlabs-ai/headroom: 77.6k, Apache-2.0: compresses tool output/logs before they reach the LLM
  (not installed; candidate if context size becomes a problem).
- "graftv": no such GitHub project found (Oct 2026); only a Hex package "mix_graft" version string.
- heygen-com/hyperframes: 69.7k stars. INSTALLED (npx hyperframes@0.8.188).

## Added Oct 23 2026
- affaan-m/everything-claude-code (ECC): ~147k-225k stars, MIT. INSTALLED into this repo's .claude/ (owner said yes):
  agents-core, commands-core, workflow-quality only (57 skills, 71 agents, 97 commands); no hook runtime and no
  language rule packs. Reinstall/update: `bash /home/user/tools/ECC/install.sh --target claude-project --modules
  agents-core,commands-core,workflow-quality` (clone github.com/affaan-m/everything-claude-code first).
- morluto/rea "Reverse Engineer Anything": ~348k stars (jumped from 41 to 300k+ in Oct 2026: treat the hype with care),
  MIT, npm rea-agents 6.7.0. INSTALLED: CLI `rea`, MCP server in .mcp.json (`npx -y rea-agents@6.7.0 mcp`), skill in
  .claude/skills/reverse-engineer-anything. Native binaries need Hopper/Ghidra/IDA (not installed); JS/Electron,
  Go, PyInstaller, WASM, Android need none or caller-supplied tools. Only analyse software we are allowed to.
  aliyenidede/rea (rea-dev on PyPI) is a different, deprecated project.
- nomadkaraoke python-audio-separator 0.47 + BS-RoFormer (vocals SDR 12.1): INSTALLED in the tools venv.
  Removes music completely (silent gaps at -180 dB) but is slow on CPU: ~6 min per 20 s clip.
