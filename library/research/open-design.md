# OpenDesign (nexu-io/open-design): AI design agent workspace

Installed here on 2026-10-27 because the owner asked: "Nex-io/open-design github repo install kro high star wala".

## What it is
- The repo is **nexu-io/open-design**. "Nex-io/open-design" does not exist: git ls-remote asked for a login, and raw README returned 404 (2026-10-27).
- Agent-Reach web search (Exa snapshot, 2026-10-27) reports 104,150 stars, Apache-2.0, homepage https://open-design.ai, created 2026-04-28.
- README (raw.githubusercontent.com/nexu-io/open-design/HEAD/README.md, read 2026-10-27) describes a local-first "collaborative AI design agent workspace". It makes motion, prototypes, websites, apps, dashboards, presentations, images and videos, and has 100+ skills, a rendering-template catalog and 151 design systems.
- It drives an agent CLI that is on PATH (Claude Code, Codex, ...). Otherwise it uses a BYOK model key set in Settings.
- It has an `od` CLI and a stdio MCP server, with `od mcp install <agent>` for claude, codex, cursor and others.
- Linux has no prebuilt app, so it is run from source.

## Install (measured here 2026-10-27)
- **Requirements:** Node `~24` and pnpm `>=10.33.2 <11` (package.json engines). The box had Node 22.22.0, so Node v24.22.1 went to /home/user/tools/node24 from nodejs.org.
- **Commands:**
  1. `git clone --depth 1` (HEAD 26d6029, 2026-10-26; 472 MB)
  2. `corepack enable`
  3. `pnpm install`: took 1m34s with pnpm 10.33.2; node_modules is 2.7 GB, plus ~0.4 GB in the pnpm store.
- **First try failed:** ERR_PNPM_ENOSPC. The owner chose to delete the ACE-Step checkpoints (6.0 GB, /home/user/tools/ACE-Step-1.5/checkpoints) to make room.
- **Build scripts:** pnpm reported ignored build scripts (ffmpeg/ffprobe installers, @google/genai, node-pty): "Run pnpm approve-builds".
- **Smoke test:** `PATH=/home/user/tools/node24/bin:$PATH pnpm tools-dev run web` printed Web http://127.0.0.1:33975/ and Daemon http://127.0.0.1:38107/ (dynamic ports).
  - Web answered 200.
  - Daemon `GET /api/plugins` returned the bundled plugin list (for example video-template-3d-animated-boy-building-lego).
  - `node apps/daemon/bin/od.mjs --help` works.

## Use
- Run it with `cd /home/user/tools/open-design && PATH=/home/user/tools/node24/bin:$PATH pnpm tools-dev run web`.
- The cloud box has no browser for the owner, so they can't open the 127.0.0.1 URL. Use it through the `od` CLI / MCP, or run it on the owner's PC.
