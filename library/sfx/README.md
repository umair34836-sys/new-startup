# Sound effects library (`sfx/`)

164 effects that need **no credit**, sorted into category folders, plus the two older files in this folder root
(`phone-ring.wav`, `wheel-clicks-13-steps.wav`, see `library/README.md`). Total about 7 MB (mp3; mono 128k / stereo 192k, 48 kHz).
Full metadata per file: `index.json` (category, tags, length, hit time, RMS, licence, source page, author, original file name).

## Licence (checked 2026-10-24)

| Source | Files | Licence proof |
| --- | --- | --- |
| Kenney audio packs (Interface Sounds, UI Audio, Impact Sounds, Casino Audio, RPG Audio, Digital Audio, Sci-Fi Sounds) | 58 | Each pack's `License.txt`: "License: (Creative Commons Zero, CC0) http://creativecommons.org/publicdomain/zero/1.0/ ... free to use in personal, educational and commercial projects" and https://kenney.nl/support: "all game assets on the asset pages are public domain licensed (CC0) ... Attribution is not required". Pages: https://kenney.nl/assets/<pack> |
| OpenGameArt.org pages | 60 | Only pages whose licence field lists CC0 and nothing else (parsed from each page on 2026-10-24; pages listing CC0 together with CC BY were skipped). Source page per file in `index.json`. |
| Own work | 46 | Made here with `library/tools/synth_sfx.py` (numpy, deterministic). No credit needed. |

CC0 means no credit and commercial/client use allowed. Mixkit and Sonniss sounds were NOT added: Mixkit's Sound Effects Free
License says "You can't redistribute the Item on its own, as stock" (https://mixkit.co/license/modal/sfxFree/, read 2026-10-24),
and this repo is public. Freesound (freesound.org, cdn.freesound.org) and Pixabay return 403 to this server (tested 2026-10-24).

## How the files were made (measured here 2026-10-24)

`library/tools/sfx_prep.py spec.json out_dir index.json`: decode with ffmpeg, cut silence before/after (threshold 45 dB below the
file's peak), cap long ambiences (max per file noted as `trimmed_to_max`, 0.4 s fade-out), peak-normalise to -1 dBFS, encode mp3,
then measure: `length_s`, `hit_s` (centre of the loudest 10 ms RMS window = where the sound hits; line an effect up so
`hit_s` lands on the cut) and `rms_dbfs` (average level; quiet ambiences need more volume than clicks).
Cross-check (2026-10-24): `npx hyperframes audio <file> --json` (hyperframes 0.8.188) was run on all 164 files; its
`moments.onset`, `moments.peak` and `moments.tailEnd` are stored as `hf_onset_s`, `hf_peak_s`, `hf_tail_end_s`.
For 142 files `hit_s` and `hf_peak_s` agree within 50 ms; the 22 that differ are sounds with several events
(ambiences, typing, door open+close, fireworks loop, engine hum), where "the hit" depends on the use.
Own effects whose name carries a length (`riser-4s`, `whoosh-long-1.2s`) are shorter after the silence trim
(the quiet start is cut): `riser-2s` 1.73 s, `riser-4s` 3.45 s, `riser-8s` 6.85 s; each still ends on its peak.

Claude cannot listen: descriptions come from the source's file/folder names. The `*-202-*` files come from folders of the
"202 More Sound Effects" pack (named Money, Phone, Drink, Camera); their exact content was not checked by ear.
`length_s` keeps up to 50 ms after the last sound above the threshold (see `sfx_prep.py`); Kenney's shortest clicks are 10-45 ms
originals (ffprobe, 2026-10-24).

## Use

- Find: `python3 library/tools/find_stock.py --sfx "whoosh"` (searches name, category, tags, description), or read `index.json`.
- HyperFrames: copy into the project's `assets/sfx/`, `<audio src="assets/sfx/whoosh-up-0.6s.mp3" data-start="<cut - hit_s>"
  data-duration="<length_s>" data-track-index="<free lane>" data-volume="0.6">`.
- Re-make own effects: `python3 library/tools/synth_sfx.py <dir>` (`--list` shows all; same seeds = same files).

## Files by category


### ambience (4)

| File | Length s | Hit s | Source | What |
| --- | --- | --- | --- | --- |
| `ambience/wind-loop.mp3` | 5.959 | 2.812 | OGA | wind whoosh loop |
| `ambience/traffic-highway.mp3` | 12.0 | 2.992 | OGA | highway traffic loop |
| `ambience/birds-park.mp3` | 20.0 | 0.982 | OGA | park birds ambience |
| `ambience/river.mp3` | 20.0 | 10.057 | OGA | river ambience |

### camera (4)

| File | Length s | Hit s | Source | What |
| --- | --- | --- | --- | --- |
| `camera/camera-shutter-1.mp3` | 0.88 | 0.138 | OGA | camera shutter |
| `camera/camera-shutter-2.mp3` | 0.534 | 0.052 | OGA | camera shutter |
| `camera/camera-202.mp3` | 0.436 | 0.248 | OGA | sound from the pack's 'Camera' folder (content not listened to) |
| `camera/camera-shutter-synth.mp3` | 0.184 | 0.115 | own | synthetic camera shutter click |

### celebration (3)

| File | Length s | Hit s | Source | What |
| --- | --- | --- | --- | --- |
| `celebration/firework-1.mp3` | 0.852 | 0.076 | OGA | firework burst |
| `celebration/firework-2.mp3` | 1.126 | 0.01 | OGA | firework burst |
| `celebration/fireworks-loop.mp3` | 12.0 | 7.757 | OGA | fireworks loop |

### crowd (2)

| File | Length s | Hit s | Source | What |
| --- | --- | --- | --- | --- |
| `crowd/applause-hall.mp3` | 12.0 | 6.793 | OGA | crowd applause in a hall |
| `crowd/crowd-shouting.mp3` | 12.0 | 2.188 | OGA | crowd shouting / talking ambience |

### door (6)

| File | Length s | Hit s | Source | What |
| --- | --- | --- | --- | --- |
| `door/door-open-wood.mp3` | 0.918 | 0.202 | Kenney | wooden door opening |
| `door/door-close-wood.mp3` | 0.675 | 0.205 | Kenney | wooden door closing |
| `door/creak.mp3` | 0.606 | 0.377 | Kenney | wood creak |
| `door/latch.mp3` | 0.241 | 0.041 | Kenney | metal latch |
| `door/door-open-close.mp3` | 6.233 | 0.163 | OGA | door open and close |
| `door/doorbell.mp3` | 3.262 | 0.675 | OGA | old doorbell ring |

### fire (2)

| File | Length s | Hit s | Source | What |
| --- | --- | --- | --- | --- |
| `fire/fire-crackle.mp3` | 2.871 | 0.799 | OGA | fire crackling |
| `fire/fireplace.mp3` | 15.0 | 12.811 | OGA | fireplace loop |

### foley (11)

| File | Length s | Hit s | Source | What |
| --- | --- | --- | --- | --- |
| `foley/footstep-concrete.mp3` | 0.103 | 0.005 | Kenney | single footstep |
| `foley/footstep-grass.mp3` | 0.175 | 0.005 | Kenney | single footstep |
| `foley/footstep-wood.mp3` | 0.271 | 0.005 | Kenney | single footstep |
| `foley/card-shuffle.mp3` | 3.063 | 0.258 | Kenney | card shuffle |
| `foley/page-flip.mp3` | 0.682 | 0.526 | Kenney | book page flip |
| `foley/book-open.mp3` | 0.151 | 0.06 | Kenney | book open |
| `foley/cloth.mp3` | 0.611 | 0.202 | Kenney | cloth rustle |
| `foley/knife-slice.mp3` | 0.411 | 0.173 | Kenney | knife slice (cooking/food) |
| `foley/paper.mp3` | 0.532 | 0.347 | OGA | paper handling |
| `foley/water-boiling.mp3` | 4.492 | 0.15 | OGA | water boiling (tea/kitchen) |
| `foley/drink-202.mp3` | 0.452 | 0.209 | OGA | sound from the pack's 'Drink' folder (content not listened to) |

### game (23)

| File | Length s | Hit s | Source | What |
| --- | --- | --- | --- | --- |
| `game/sword-draw.mp3` | 0.4 | 0.171 | Kenney | blade draw |
| `game/digital-powerup-1.mp3` | 1.012 | 0.018 | Kenney | power-up |
| `game/laser-1.mp3` | 0.814 | 0.201 | Kenney | laser |
| `game/phaser-up.mp3` | 0.429 | 0.301 | Kenney | rising phaser |
| `game/phaser-down.mp3` | 0.358 | 0.107 | Kenney | falling phaser |
| `game/zap.mp3` | 0.913 | 0.021 | Kenney | zap |
| `game/blip-up.mp3` | 0.405 | 0.054 | Kenney | rising blip |
| `game/blip-down.mp3` | 0.637 | 0.265 | Kenney | falling blip |
| `game/retro-coin.mp3` | 0.299 | 0.016 | OGA | retro coin |
| `game/retro-powerup.mp3` | 0.486 | 0.022 | OGA | retro power-up |
| `game/retro-explosion.mp3` | 0.929 | 0.12 | OGA | retro explosion |
| `game/synth-beep.mp3` | 0.201 | 0.017 | OGA | synth beep |
| `game/retro-die.mp3` | 0.526 | 0.016 | OGA | retro game over |
| `game/game-coin.mp3` | 0.35 | 0.005 | own | chiptune coin pickup |
| `game/game-jump.mp3` | 0.25 | 0.005 | own | chiptune jump |
| `game/game-powerup.mp3` | 0.49 | 0.078 | own | chiptune power-up arpeggio |
| `game/game-levelup.mp3` | 1.047 | 0.005 | own | chiptune level-up fanfare |
| `game/game-hit.mp3` | 0.18 | 0.005 | own | chiptune hit/damage noise |
| `game/game-lose.mp3` | 0.79 | 0.194 | own | chiptune lose jingle |
| `game/game-select.mp3` | 0.12 | 0.005 | own | chiptune menu select |
| `game/game-explosion-8bit.mp3` | 1.2 | 0.005 | own | 8-bit explosion |
| `game/block-place.mp3` | 0.216 | 0.005 | own | soft woody thunk (placing a block) |
| `game/block-break.mp3` | 0.346 | 0.022 | own | crumbly break (mining a block) |

### glitch (6)

| File | Length s | Hit s | Source | What |
| --- | --- | --- | --- | --- |
| `glitch/ui-glitch-1.mp3` | 0.017 | 0.005 | Kenney | short UI glitch |
| `glitch/ui-glitch-2.mp3` | 0.012 | 0.005 | Kenney | short UI glitch |
| `glitch/glitch-short.mp3` | 0.3 | 0.281 | own | digital glitch 0.3 s |
| `glitch/glitch-medium.mp3` | 0.6 | 0.38 | own | digital glitch 0.6 s |
| `glitch/glitch-long.mp3` | 1.167 | 0.127 | own | digital glitch 1.2 s |
| `glitch/static-noise.mp3` | 1.0 | 0.446 | own | TV static 1 s |

### impact (15)

| File | Length s | Hit s | Source | What |
| --- | --- | --- | --- | --- |
| `impact/punch-heavy.mp3` | 0.492 | 0.038 | Kenney | heavy punch |
| `impact/punch-medium.mp3` | 0.332 | 0.031 | Kenney | punch |
| `impact/metal-hit.mp3` | 0.165 | 0.005 | Kenney | metal hit |
| `impact/wood-hit.mp3` | 0.31 | 0.005 | Kenney | wood hit / knock |
| `impact/glass-hit.mp3` | 0.238 | 0.005 | Kenney | glass hit |
| `impact/bell-hit.mp3` | 1.236 | 0.005 | Kenney | bell strike |
| `impact/soft-thud.mp3` | 0.527 | 0.006 | Kenney | soft thud |
| `impact/pickaxe-hit.mp3` | 0.633 | 0.01 | Kenney | pickaxe on stone (mining) |
| `impact/bang.mp3` | 0.814 | 0.06 | OGA | bang |
| `impact/cannon.mp3` | 0.934 | 0.087 | OGA | cannon boom |
| `impact/explosion-1.mp3` | 0.984 | 0.034 | OGA | explosion |
| `impact/impact-boom.mp3` | 2.5 | 0.005 | own | cinematic boom: sub + body + click |
| `impact/impact-punch.mp3` | 1.0 | 0.008 | own | shorter tighter hit |
| `impact/sub-drop.mp3` | 1.842 | 0.017 | own | low sine drop (bass drop) |
| `impact/heartbeat.mp3` | 1.3 | 0.007 | own | 2 heartbeats |

### magic (2)

| File | Length s | Hit s | Source | What |
| --- | --- | --- | --- | --- |
| `magic/sparkle.mp3` | 0.926 | 0.451 | own | random high sparkles 1 s |
| `magic/magic-shimmer.mp3` | 1.1 | 0.257 | own | rising bell shimmer |

### money (7)

| File | Length s | Hit s | Source | What |
| --- | --- | --- | --- | --- |
| `money/coins-stack.mp3` | 0.153 | 0.014 | Kenney | coins/chips stacking |
| `money/coins-handle.mp3` | 0.551 | 0.012 | Kenney | coins handled in the hand |
| `money/coins-jingle-1.mp3` | 0.758 | 0.112 | Kenney | coin pouch jingle |
| `money/money-202-a.mp3` | 0.775 | 0.499 | OGA | sound from the pack's 'Money' folder (content not listened to) |
| `money/money-202-b.mp3` | 0.394 | 0.103 | OGA | sound from the pack's 'Money' folder (content not listened to) |
| `money/money-202-c.mp3` | 0.478 | 0.256 | OGA | sound from the pack's 'Money' folder (content not listened to) |
| `money/cash-register.mp3` | 1.51 | 0.005 | own | synthetic ka-ching (drawer + bell + coins) |

### notification (12)

| File | Length s | Hit s | Source | What |
| --- | --- | --- | --- | --- |
| `notification/alert.mp3` | 0.954 | 0.154 | OGA | alert / notification |
| `notification/ding-real.mp3` | 0.519 | 0.007 | OGA | ding |
| `notification/chimes.mp3` | 2.005 | 0.188 | OGA | chimes |
| `notification/ding-deep.mp3` | 1.54 | 0.018 | OGA | deep ding |
| `notification/negative.mp3` | 1.046 | 0.035 | OGA | negative / wrong |
| `notification/alarm.mp3` | 0.429 | 0.129 | OGA | alarm |
| `notification/bell-small.mp3` | 0.434 | 0.023 | OGA | small bell |
| `notification/kalimba.mp3` | 0.675 | 0.163 | OGA | two kalimba notes |
| `notification/ding.mp3` | 1.6 | 0.007 | own | single bell ding |
| `notification/notification-two-tone.mp3` | 0.9 | 0.138 | own | two-note message chime |
| `notification/success-chime.mp3` | 1.32 | 0.276 | own | 4-note rising success |
| `notification/error-buzz.mp3` | 0.48 | 0.286 | own | wrong-answer buzzer |

### phone (4)

| File | Length s | Hit s | Source | What |
| --- | --- | --- | --- | --- |
| `phone/ringtone-chirp.mp3` | 2.154 | 1.037 | OGA | modern phone ringtone |
| `phone/phone-202-a.mp3` | 1.15 | 0.304 | OGA | sound from the pack's 'Phone' folder (content not listened to) |
| `phone/phone-202-b.mp3` | 0.162 | 0.036 | OGA | sound from the pack's 'Phone' folder (content not listened to) |
| `phone/phone-vibrate.mp3` | 1.112 | 1.009 | own | phone vibrating on a desk, 2 pulses |

### pop (4)

| File | Length s | Hit s | Source | What |
| --- | --- | --- | --- | --- |
| `pop/plop.mp3` | 0.223 | 0.079 | OGA | plop |
| `pop/pop-high.mp3` | 0.1 | 0.006 | own | UI pop (pitch drop) |
| `pop/pop-low.mp3` | 0.14 | 0.006 | own | softer lower pop |
| `pop/bubble-pop.mp3` | 0.15 | 0.072 | own | rising bubble blip |

### riser (4)

| File | Length s | Hit s | Source | What |
| --- | --- | --- | --- | --- |
| `riser/riser-2s.mp3` | 1.727 | 1.698 | own | noise + tone riser, ends at peak |
| `riser/riser-4s.mp3` | 3.447 | 3.427 | own | noise + tone riser, ends at peak |
| `riser/riser-8s.mp3` | 6.853 | 6.83 | own | long build-up riser |
| `riser/downlifter-2s.mp3` | 2.0 | 0.017 | own | falling sweep after a drop |

### scifi (8)

| File | Length s | Hit s | Source | What |
| --- | --- | --- | --- | --- |
| `scifi/explosion-crunch.mp3` | 0.777 | 0.005 | Kenney | crunchy explosion |
| `scifi/explosion-low.mp3` | 1.685 | 0.278 | Kenney | deep explosion |
| `scifi/laser-big.mp3` | 0.592 | 0.007 | Kenney | big laser |
| `scifi/force-field.mp3` | 0.753 | 0.13 | Kenney | force field hum |
| `scifi/computer-noise.mp3` | 5.0 | 2.171 | Kenney | computer data noise |
| `scifi/scifi-door.mp3` | 0.532 | 0.005 | Kenney | sci-fi door |
| `scifi/thruster.mp3` | 5.0 | 1.137 | Kenney | rocket thruster |
| `scifi/engine-hum.mp3` | 5.0 | 3.726 | Kenney | engine hum |

### sting (1)

| File | Length s | Hit s | Source | What |
| --- | --- | --- | --- | --- |
| `sting/mystery-sting.mp3` | 5.235 | 1.053 | OGA | mystery sting |

### transition (13)

| File | Length s | Hit s | Source | What |
| --- | --- | --- | --- | --- |
| `transition/swish-1.mp3` | 0.109 | 0.042 | OGA | real swish / whoosh |
| `transition/swish-4.mp3` | 0.126 | 0.046 | OGA | real swish / whoosh |
| `transition/swish-7.mp3` | 0.175 | 0.044 | OGA | real swish / whoosh |
| `transition/air-whoosh.mp3` | 5.247 | 2.383 | OGA | air whoosh |
| `transition/whoosh-up-0.6s.mp3` | 0.573 | 0.333 | own | rising air whoosh, pans L->R |
| `transition/whoosh-down-0.6s.mp3` | 0.6 | 0.321 | own | falling air whoosh, pans L->R |
| `transition/whoosh-fast-0.3s.mp3` | 0.3 | 0.172 | own | quick whoosh for whip pans |
| `transition/whoosh-long-1.2s.mp3` | 1.072 | 0.663 | own | slow big whoosh |
| `transition/whoosh-heavy-0.8s.mp3` | 0.8 | 0.457 | own | darker whoosh (mono) |
| `transition/swipe-short.mp3` | 0.22 | 0.131 | own | phone-screen swipe |
| `transition/swipe-long.mp3` | 0.396 | 0.204 | own | longer swipe |
| `transition/tape-stop.mp3` | 1.0 | 0.952 | own | tape/record slowing to a stop |
| `transition/record-scratch.mp3` | 0.35 | 0.128 | own | synthetic record scratch |

### typing (5)

| File | Length s | Hit s | Source | What |
| --- | --- | --- | --- | --- |
| `typing/typing-keyboard-medium.mp3` | 5.875 | 2.153 | OGA | keyboard typing, medium speed |
| `typing/typing-keyboard-fast.mp3` | 8.0 | 2.193 | OGA | keyboard typing, fast |
| `typing/keypress.mp3` | 0.25 | 0.042 | OGA | single key press |
| `typing/typewriter-1.mp3` | 0.659 | 0.098 | OGA | typewriter |
| `typing/typing-synth.mp3` | 1.494 | 1.017 | own | 12 synthetic key clicks |

### ui (19)

| File | Length s | Hit s | Source | What |
| --- | --- | --- | --- | --- |
| `ui/click-1.mp3` | 0.076 | 0.005 | Kenney | UI click |
| `ui/click-2.mp3` | 0.007 | 0.004 | Kenney | UI click |
| `ui/select-1.mp3` | 0.04 | 0.005 | Kenney | menu select |
| `ui/confirm-1.mp3` | 0.29 | 0.005 | Kenney | confirm / success blip |
| `ui/ui-error-1.mp3` | 0.162 | 0.005 | Kenney | error blip |
| `ui/toggle.mp3` | 0.136 | 0.005 | Kenney | toggle switch |
| `ui/switch.mp3` | 0.185 | 0.005 | Kenney | switch |
| `ui/ui-open.mp3` | 0.148 | 0.113 | Kenney | window open |
| `ui/ui-close.mp3` | 0.148 | 0.005 | Kenney | window close |
| `ui/drop.mp3` | 0.13 | 0.005 | Kenney | item drop |
| `ui/pluck.mp3` | 0.1 | 0.005 | Kenney | plucky blip |
| `ui/tick.mp3` | 0.045 | 0.005 | Kenney | tick |
| `ui/maximize.mp3` | 0.258 | 0.245 | Kenney | pop-up appear |
| `ui/minimize.mp3` | 0.258 | 0.005 | Kenney | pop-up disappear |
| `ui/glass-tap.mp3` | 0.276 | 0.005 | Kenney | glass tap UI |
| `ui/rollover.mp3` | 0.224 | 0.064 | Kenney | hover / rollover |
| `ui/mouse-click.mp3` | 0.056 | 0.017 | Kenney | computer mouse click |
| `ui/clock-tick-tock.mp3` | 1.575 | 1.505 | own | 4 clock ticks, 0.5 s apart |
| `ui/countdown-beeps.mp3` | 3.65 | 0.011 | own | 3 beeps (1 s apart) + long beep at 3 s |

### vehicle (5)

| File | Length s | Hit s | Source | What |
| --- | --- | --- | --- | --- |
| `vehicle/car-engine-start.mp3` | 1.647 | 0.953 | OGA | car engine start |
| `vehicle/car-accelerate.mp3` | 4.247 | 0.34 | OGA | car accelerating |
| `vehicle/car-door-open.mp3` | 0.986 | 0.173 | OGA | car door opening |
| `vehicle/car-door-close.mp3` | 0.567 | 0.145 | OGA | car door closing |
| `vehicle/car-blinker.mp3` | 0.383 | 0.009 | OGA | car indicator ticking |

### water (1)

| File | Length s | Hit s | Source | What |
| --- | --- | --- | --- | --- |
| `water/splash.mp3` | 0.589 | 0.126 | OGA | water splash |

### weather (3)

| File | Length s | Hit s | Source | What |
| --- | --- | --- | --- | --- |
| `weather/rain-1.mp3` | 15.0 | 7.363 | OGA | rain ambience |
| `weather/rain-2.mp3` | 15.0 | 2.794 | OGA | rain loop |
| `weather/rain-thunder.mp3` | 20.0 | 6.733 | OGA | rain with long thunder |
