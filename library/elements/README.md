# Emoji + icon pack (PC security / gamer explainer)

Small licence-clean pack for faceless/explainer videos (first use: "crack games, free mods, FPS boost tools can
carry malware"). Added 2026-10-26. Every file is listed in `licence_proof.json` (source URL pinned to a commit,
set, licence, licence URL, the licence line read on the source, date checked, sha256). Licence texts: `licences/`.
No Twemoji/OpenMoji (attribution needed) and no brand logos (trademarks).

| Folder | Set (commit) | Licence (read on source 2026-10-26) | Format |
|---|---|---|---|
| `emoji/fluent-3d/` | microsoft/fluentui-emoji (1ffb34c) | MIT, "Copyright (c) Microsoft Corporation." | 256x256 PNG (the repo's 3D PNGs are 256 px; no 512 exists) |
| `emoji/noto/` | googlefonts/noto-emoji (e20cbc2), `2D/png/512` | Apache-2.0 (README: "most image resources are under the Apache license, version 2.0"; `2D/svg/LICENSE`) | 512x512 PNG |
| `emoji/noto/india_flag_*` | noto-emoji `third_party/region-flags` | Public domain (region-flags/LICENSE) | flat PNG 1350x900 + waved SVG |
| `icons/lucide/` | lucide-icons/lucide (7faf876) | ISC | 24x24 line SVG, `stroke="currentColor"` |
| `icons/tabler/` | tabler/tabler-icons (a4ce140), `icons/outline` | MIT | 24x24 line SVG, `stroke="currentColor"` |

Note: noto-emoji's repo-root `LICENSE` file text is SIL OFL 1.1 while its README names `./LICENSE` as Apache-2.0
(seen 2026-10-26); both are permissive and need no on-screen credit. MIT/ISC/Apache ask that the licence notice
travels with copies of the files: keep `licences/` with the pack; a rendered video needs no on-screen credit.

File names: emoji `<concept>.png`; icons `<concept>__<original-icon-name>.svg`.

| Concept | Fluent 3D | Noto | Line icon |
|---|---|---|---|
| warning sign | warning | warning | lucide triangle-alert |
| police light / siren | - (not in Fluent) | police_light | lucide siren |
| skull | skull | skull | lucide skull |
| bug | bug | bug | lucide bug |
| virus / microbe | virus (Microbe) | virus | lucide virus |
| lock | lock | lock | lucide lock |
| unlocked lock | unlocked | unlocked | lucide lock-open |
| key | key | key | lucide key-round |
| shield | shield | shield | lucide shield |
| laptop | laptop | laptop | lucide laptop |
| desktop computer | desktop | desktop | lucide monitor |
| PC fan / wind | fan_wind (Wind face), dashing_away | fan_wind, dashing_away | lucide fan (a real fan) |
| envelope | envelope | envelope | lucide mail |
| incoming envelope | incoming_envelope | incoming_envelope | tabler mail-down |
| money bag | money_bag | money_bag | lucide badge-dollar-sign |
| coin | coin | coin | lucide coins |
| chart going down | chart_down | chart_down | lucide trending-down |
| game controller | game_controller | game_controller | lucide gamepad-2 |
| joystick | joystick | joystick | lucide joystick |
| download | download (Inbox tray), down_arrow | download, down_arrow | lucide download |
| package / zip / folder | package, file_folder | package, file_folder | lucide package, folder, file-archive (zip) |
| link | link | link | lucide link |
| speech bubble | speech_bubble | speech_bubble | lucide message-circle |
| robot (bots) | robot | robot | lucide bot |
| thinking face | thinking_face | thinking_face | tabler mood-puzzled |
| screaming face | screaming_face | screaming_face | tabler mood-surprised |
| exploding head | exploding_head | exploding_head | lucide brain (closest) |
| check mark | check_mark (Check mark button) | check_mark | lucide circle-check |
| cross mark | cross_mark | cross_mark | lucide circle-x |
| no entry | no_entry | no_entry | - |
| prohibited | prohibited | prohibited | lucide ban |
| eyes | eyes | eyes | lucide eye |
| red flag | red_flag (Triangular flag) | red_flag | lucide flag |
| hourglass | hourglass (not done) | hourglass | lucide hourglass |
| detective | detective | detective | tabler spy |
| magnifying glass | magnifying_glass | magnifying_glass | lucide search |
| globe / browser | globe (Globe with meridians) | globe | lucide globe |
| fire | fire | fire | lucide flame |
| thumbs up | thumbs_up | thumbs_up | lucide thumbs-up |
| India flag | - (Fluent has no country flags) | india_flag_flat.png, india_flag_waved.svg | - |

Not found: Fluent has no "Police car light" and no country flags (checked the repo's assets/ tree at 1ffb34c,
2026-10-26); there is no zip emoji in Unicode (zip only as a line icon). Line icons are monochrome: set the SVG
`stroke` (or CSS `color`) to recolour. All 84 emoji PNGs (41 Fluent, 43 Noto), the waved flag SVG and the 40 icon SVGs were looked at on a contact sheet
(headless Chrome) on 2026-10-26.
