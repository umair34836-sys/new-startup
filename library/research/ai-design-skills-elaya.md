# elayadesign/ai-design-skills (installed 2026-11-07)

Source: https://github.com/elayadesign/ai-design-skills (cloned here 2026-11-07, commit 456d9e0d3e2d84c748bb143c6ca3d90c45e16213,
dated 2026-11-02 "README: SlopScan banner"). Licence: MIT (LICENSE file, "Copyright (c) 2026 Elaya"). Parts adapted from
Leonxlnx/taste-skill (MIT, credited in the SKILL.md).
Installed as `.claude/skills/elaya-landing-page-design` and `.claude/skills/elaya-figma-designer` (SKILL.md + LICENSE copied,
only the `name:` front-matter changed to avoid clashes). The repo has only these two skills (README table, 2026-11-07).
Owner's ask (2026-11-07): "is skill ko download kar ke issi se knowledge lo" for the SkilloraClouds tutorial thumbnails.

## What the skills say (read 2026-11-07; landing-page-design 479 lines, figma-designer 405 lines)
landing-page-design, Part B visual system (the part that transfers to any graphic):
- Fonts: Geist, Manrope, Geist Mono, Poppins; never Inter/Roboto/Arial/Open Sans/Helvetica; never italics; ONE typeface
  per site (a second only when asked); never ultra-bold 900, cap at semibold/bold.
- Copy: no hyphens inside text, no orphaned last word, sentence case for headings and buttons, banned filler words
  ("revolutionize", "supercharge", "cutting edge", "effortless", "take it to the next level", "world class" ...).
- Type sizes only on the Tailwind scale (12 14 16 18 20 24 30 36 48 60 72 96 128), named styles Heading 1-6 / Title / Body /
  Button / Caption; spacing tokens 0 2 4 8 12 16 24 32 40 48 64 80 96; nested radius = outer radius - gap.
- Backgrounds flat, never gradients; dark surfaces only #000000 #181818 #1F1F1F #272727 #313131 #131209.
- The one allowed gradient: hero heading TEXT, left to right #FFFFFF -> #9B9B9B (dark theme) / #000000 -> #666666 (light).
- Icons: Phosphor, Solar, Iconamoon (never Material). Motion: cubic-bezier(0.22,1,0.36,1), 500 ms, transform/opacity only.
- Content realism: never invent facts/prices/testimonials; mark missing facts as {{placeholders}}.
figma-designer adds: one accent colour kept below 80% saturation; tokens named by role; same type scale and copy rules.

## How it was applied to the SkilloraClouds tutorial thumbnails (2026-11-07)
- Direction "clean" follows it: flat #181818 surface, one typeface (Manrope, weight 800 max), sentence case, one accent
  (#22c55e = the client's green), no gradient backgrounds, the real panel screenshot as the hero visual.
- Direction "bold" follows the repo's own thumbnail research instead (library/research/editing/skills2/16-thumbnails.md,
  #4253 3-4 words with heavy outline, #4248 one highlighted word, #4254 fewer bigger words): Anton caps with outline.
  The two skills disagree on this (web UI vs YouTube thumbnails); both directions were rendered and checked at 168x94.
