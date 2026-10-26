# blocky-walk (16:9, 21.5 s, two blocky characters walk down a sunny voxel village lane)

This template was made on 2026-10-26: the owner asked for a 3D world with the host plus the girl skin and a walking video.
It reuses blocky-monsoon's village, character rig, 4x4 ground tiles, camera rig and frame-0 init. The look is daylight:
a sky gradient with pixel clouds, a warm sun wash, a vignette and a 0.8 s fade at the end.

## Setup and build
Copy these into the project:
- `assets/textures`: from `python3 library/tools/voxel_textures.py assets/textures`
- `assets/characters/{host,girl}-skin.png`
- `assets/vendor/gsap-3.14.2.min.js`: from video/assets/vendor
- `assets/music/background--town-theme-rpg.mp3`: CC0, from library/music/cc0

Then run `python3 -I build.py`. It writes index.html and compositions/{sky,world,grade}.html.

## Shots
Cuts fall on the music's downbeats (listen.py: 91.6 BPM, bar 2.621 s; downbeats 2.73, 5.36, ... 18.51):
- S1, 0 to 5.36 s: a high wide shot from down the lane, craning down toward the pair as they walk at the camera.
- S2, 5.36 to 13.27 s: a 3/4-front tracking shot in the west gap.
- S3, 13.27 to 18.51 s: a front shot that dollies back with them.
- S4, 18.51 s to the end: they stop, turn to each other and wave, then the camera cranes up and back.

## Fixes found in snapshots (2026-10-26)
- Camera paths:
  - The S1 end at yaw 160 put the camera into an east house, so it was changed to 174.
  - S2 at yaw -66 (blocky-monsoon's side shot) showed their backs here, because they walk toward -z. It was changed to -140/-132.
  - The west lamp posts at z=-2..16 filled the frame edge in S2 (camera x ≈ -3.0 to -3.6), so only z=-14/-8 are kept on that side.
- The host skin's white hood overlay shows as a flat slab behind the head in 3/4 views. It is part of the skin, not a rig bug.

## Measured here
- `hyperframes check` passed, with one warning: first_frame_empty, because there is no title at 0 s.
