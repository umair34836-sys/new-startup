# Emoji / icon sets: licences and findings (checked 2026-10-26)

All read on raw.githubusercontent.com on 2026-10-26 (default branch; commits in library/elements/licence_proof.json).

- microsoft/fluentui-emoji: LICENSE = "MIT License / Copyright (c) Microsoft Corporation."
  (https://github.com/microsoft/fluentui-emoji/blob/main/LICENSE). Assets: `assets/<Name>/{3D,Color,Flat,High Contrast}/`,
  skin-tone emoji under `Default/Light/Dark/...`; 3D PNGs are 256x256 (measured here, PIL). Each folder has metadata.json
  with the `unicode` codepoint. No country flags and no "Police car light" folder (git ls-tree at commit 1ffb34c).
- googlefonts/noto-emoji: README "License": "Emoji fonts (under the fonts subdirectory) are under the SIL Open Font
  License, version 1.1. Tools and most image resources are under the Apache license, version 2.0 (./LICENSE). Flag
  images under third_party/region-flags are in the public domain or otherwise exempt from copyright". But the root
  LICENSE file text is "This Font Software is licensed under the SIL Open Font License, Version 1.1"; `2D/svg/LICENSE`
  is Apache-2.0. Layout now `2D/png/{32,72,128,512}/emoji_u<cp>.png` (fe0f dropped) and `3D/png/...`; country flags
  only in `3D/png` and `third_party/region-flags/{png,svg,waved-svg}`.
- lucide-icons/lucide: LICENSE = ISC, "Copyright (c) 2026 Lucide Icons and Contributors"; icons derived from Feather
  (list in the LICENSE) are MIT, "Copyright (c) 2013-present Cole Bemis". Icons at `icons/<name>.svg`.
- tabler/tabler-icons: LICENSE = MIT, "Copyright (c) 2020-2026 Paweł Kuna". Icons at `icons/outline/<name>.svg`.
- Listing a GitHub repo without downloading it: `git clone --filter=blob:none --no-checkout --depth 1 <url>` then
  `git ls-tree -r --name-only HEAD` (worked here 2026-10-26 for all four repos).
- SVG rasterising here: ImageMagick `convert` has no SVG delegate (output 0 files, 2026-10-26); the HyperFrames
  chrome-headless-shell `--screenshot` of an HTML page with <img src=svg> worked.
