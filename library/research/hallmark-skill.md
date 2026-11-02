# Hallmark design skill (checked 2026-11-02)

The owner asked on 2026-11-02 to install "hallmark skill ... GitHub se 300k plus stars".

## What it is
- Repo: https://github.com/Nutlope/hallmark, made by Together AI. Site: https://www.usehallmark.com/
- Licence: MIT (LICENSE file, "Copyright (c) 2026 Hallmark contributors"). Version 2.0.0 (package.json).
- Shallow clone on 2026-11-02, HEAD 4f6a46c (Oct 29 2026).
- Purpose: an "anti-AI-slop" design skill for building websites and pages. It is not a video tool.
  - 50 themes; it asks for real material; `sloplint` lints the page in a real browser.
  - Verbs: `/hallmark <page>`, `/hallmark redesign <dir>`, `/hallmark audit <page>`.
- Install command from its README: `npx skills add nutlope/hallmark -g`.
  It lands in `~/.claude/skills/hallmark`. Needs Node 18+.
  `sloplint --render` and screenshots also need `npm i -g puppeteer-core` plus Chrome.

## Stars
- gitstars.io snapshot 2026-11-01 (via `agent-reach web search`): 44,766 stars and 2,374 forks.
- That is NOT 300k+. The GitHub API answered "not enabled for this session" (403), so the gitstars figure is the only one.

## Contents of skills/hallmark (7.1 MB)
- 101 .md, 11 .mjs scripts, 50 theme preview JPGs (references/themes/*.jpg, 5.2 MB; screenshots of designed pages).
- photos.json: links to Wikimedia Commons photos (CC0 / PD / CC BY / CC BY-SA). Each photo used must be credited.
- scripts/imagegen.mjs calls api.together.xyz only when TOGETHER_API_KEY is set (opt-in, paid).
  Without the key it falls back to CSS art or a placeholder.
- Chrome lookup: capture.mjs and picture.mjs honour CHROME_PATH. sloplint-render.mjs only checks fixed paths
  (/usr/bin/chromium, ...). This container has /opt/pw-browsers/chromium and no /usr/bin/chromium.

## Status
- NOT installed yet (2026-11-02).
- Copying it into .claude/skills (loaded by every session) was stopped by the session's permission check as untrusted
  third-party code. It needs the owner's explicit go-ahead.
