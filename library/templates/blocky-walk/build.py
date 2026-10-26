# Blocky Walk: the owner's host + the girl character walk together down a sunny voxel village lane.
# World, character rig, ground tiling, camera rig and frame-0 init are from library/templates/blocky-monsoon/build.py.
#   python3 -I build.py
import re, sys
sys.path.insert(0, "/home/user/new-startup/library/tools")
from voxel_world import World
import blocky_character as bc

DUR = 21.5
# shot cuts on the music's downbeats (listen.py on background--town-theme-rpg.mp3: 91.6 BPM, bar 2.621 s)
CUT1, CUT2, CUT3 = 5.36, 13.27, 18.51
W = World("vw", B=64, tex="assets/textures", perspective=1300)
B = 64
js = []

def tw(sel, props, dur, at, ease="power2.inOut"):
    pr = ", ".join(f"{k}: {v}" for k, v in props.items())
    js.append(f'    tl.to("{sel}", {{ {pr}, duration: {dur:.3f}, ease: "{ease}" }}, {at:.3f});')

def st(sel, props, at):
    pr = ", ".join(f"{k}: {v}" for k, v in props.items())
    js.append(f'    tl.set("{sel}", {{ {pr} }}, {at:.3f});')

# ---------------------------------------------------------------- ground (4x4 tiles: Chrome drops big faces near the camera)
def tiled(x0, z0, x1, z1, tex, y=0.0, step=4):
    z = z0
    while z < z1:
        x = x0
        while x < x1:
            W.plane(x, y, z, min(step, x1 - x), min(step, z1 - z), tex)
            x += step
        z += step
tiled(-20, -34, -2.5, 24, "grass_top")
tiled(2.5, -34, 20, 24, "grass_top")
tiled(-2.5, -34, 2.5, 24, "cobble", 0.01, 2.5)

# ---------------------------------------------------------------- houses (gap of 2.5 blocks between lane edge and facades)
def house(x0, z0, w, d, h, wall, facade_x):
    W.box(x0, 0, z0, w, h, d, wall)
    W.box(x0 - 0.5, h, z0 - 0.5, w + 1, 0.6, d + 1, "dark_planks")
    W.box(x0 + 0.5, h + 0.6, z0 + 0.5, w - 1, 0.6, d - 1, "dark_planks")
    W.box(x0 + 1.5, h + 1.2, z0 + 1, w - 3, 0.6, d - 2, "dark_planks")
    zc = z0 + d / 2
    fx = facade_x - 0.06 if facade_x > x0 else facade_x - 0.04
    for wz in (zc - 2.2, zc + 1.2):
        W.box(fx, 1.4, wz, 0.1, 1.1, 1.0, "window_lit")
    W.box(fx, 0, zc - 0.5, 0.1, 2.0, 1.0, "door")
for z0, wall in ((-12, "planks"), (-4, "cobble"), (4, "stone_brick"), (12, "planks")):
    house(-11, z0, 6, 6, 4, wall, -5)
for z0, wall in ((-10, "stone_brick"), (-2, "planks"), (6, "cobble"), (14, "stone_brick")):
    house(5, z0, 6, 6, 4, wall, 5)
for x0 in (-15, -6, 3, 11):
    house(x0, -30, 6, 5, 5, "planks" if x0 % 2 else "stone_brick", x0)
for (x, z) in ((-14, -17), (13, -16), (-15, 1), (14, 4), (-8, -21), (9, -22), (-14, 19), (13, 21)):
    W.box(x, 0, z, 1, 4, 1, "log")
    W.box(x - 1.5, 3.2, z - 1.5, 4, 2.4, 4, "leaves")
    W.box(x - 0.5, 5.6, z - 0.5, 2, 1, 2, "leaves")
# fence posts + lamps along the lane edges (unlit by day)
# west side only beyond z=-8: the S2 tracking camera passes x=-3..-3.6 for z=-5..5 and a post filled the frame edge
for (x, z) in [(3.0, z) for z in (-14, -8, -2, 4, 10, 16)] + [(-3.4, -14), (-3.4, -8)]:
    if True:
        W.box(x, 0, z, 0.22, 3.0, 0.22, "iron")
        W.box(x - 0.15, 3.0, z - 0.15, 0.52, 0.6, 0.52, "lantern")
        W.box(x - 0.2, 3.6, z - 0.2, 0.62, 0.12, 0.62, "iron")
# a few flower blocks on the grass verge
for (x, z, c) in ((-4.2, -11, "#e2475b"), (-4.4, 1, "#f2c94c"), (3.8, -5, "#e2475b"), (4.0, 9, "#f2c94c"), (-4.3, 13, "#d16bd6")):
    W.box(x, 0, z, 0.25, 0.25, 0.25, c, top=c)

# ---------------------------------------------------------------- the two characters (walk from z=14 to z=-9, side by side)
S = 64 * 1.85 / 32
Z0, Z1 = 14.0, -9.0
W.group("him", -0.75, 0, Z0)
W.raw(bc.rig_html("him", S, ""), group="him")
W.group("her", 0.75, 0, Z0)
W.raw(bc.rig_html("her", S, ""), group="her")
WALK0, WALK1 = 1.2, CUT3 + 0.4          # 1.2 s idle on the establishing shot, stop just after the last cut
him_moves = [[0, "idle"], [WALK0, "walk"], [WALK1, "idle"], [WALK1 + 0.5, "wave"], [WALK1 + 2.3, "idle"]]
her_moves = [[0, "idle"], [WALK0, "walk"], [WALK1, "idle"], [WALK1 + 0.7, "wave"], [WALK1 + 2.3, "idle"]]
js += bc.pose_js("him", S, him_moves, DUR, 0)
js += bc.pose_js("her", S, her_moves, DUR, 0)
for cid in ("him", "her"):
    st(f"#{cid}", {"rotationY": 180, "z": 0}, 0)                        # face down the lane (-z)
    tw(f"#{cid}", {"z": (Z1 - Z0) * B}, WALK1 - WALK0, WALK0, "none")
# at the stop they turn to each other, then to the camera
tw("#him", {"rotationY": 90}, 0.5, WALK1, "power2.out")
tw("#her", {"rotationY": -90}, 0.5, WALK1, "power2.out")
tw("#him", {"rotationY": 0}, 0.5, DUR - 1.4, "power2.inOut")
tw("#her", {"rotationY": 0}, 0.5, DUR - 1.4, "power2.inOut")

def pos(t):  # lane z of the pair at time t (linear walk)
    if t <= WALK0:
        return Z0
    if t >= WALK1:
        return Z1
    return Z0 + (Z1 - Z0) * (t - WALK0) / (WALK1 - WALK0)

# ---------------------------------------------------------------- camera (target blocks, yaw, pitch, distance px)
cam = [
    (0.0, 0, "", (0, 2.0, pos(0) - 2), 180, 30, 1450),                 # S1 wide from down the lane, high
    (0.0, CUT1, "power2.inOut", (0, 1.4, pos(CUT1)), 174, 12, 760),     # crane down toward the pair walking at us
    (CUT1, 0, "", (0, 1.0, pos(CUT1) - 0.4), -140, 7, 300),             # S2 hard cut: 3/4 front tracking shot (west gap)
    (CUT1, CUT2 - CUT1, "none", (0, 1.0, pos(CUT2) - 0.4), -132, 7, 300),
    (CUT2, 0, "", (0, 1.2, pos(CUT2) - 0.5), 180, 6, 520),              # S3 cut: in front, dolly back with them
    (CUT2, CUT3 - CUT2, "none", (0, 1.2, pos(CUT3) - 0.5), 190, 7, 470),
    (CUT3, 0, "", (0, 1.15, Z1), 180, 6, 430),                          # S4 cut: two-shot at the stop
    (CUT3 + 1.0, DUR - CUT3 - 1.0, "sine.inOut", (0, 1.6, Z1), 196, 24, 1150),  # crane up and back
]
js += W.camera_js(cam)

# tl.set at 0 does not render on frame 0: apply initial states with gsap.set first (blocky-monsoon learning)
init_js = []
for line in js:
    m = re.match(r'\s*tl\.set\((.*), 0(?:\.0+)?\);$', line)
    if m:
        init_js.append(f"    gsap.set({m.group(1)});")
world_html = W.wrap(W.html("        "))
open("compositions/world.html", "w").write(f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; overflow: hidden; }}
    {W.css()}
    {bc.css("him", "assets/characters/host-skin.png")}
    {bc.css("her", "assets/characters/girl-skin.png")}
  </style>
  <div id="root" data-composition-id="world" data-layout-allow-overflow data-width="1920" data-height="1080">
{world_html}
  </div>
  <script>
{chr(10).join(init_js)}
    const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
    tl.to({{}}, {{ duration: {DUR} }}, 0);
    window.__timelines["world"] = tl;
  </script>
</template>
""")

open("compositions/sky.html", "w").write(f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; overflow: hidden; }}
    #sk-day {{ position: absolute; inset: 0; background: linear-gradient(to bottom, #4f9fe0 0%, #8cc6f0 55%, #d8eefa 100%); }}
    .sk-cloud {{ position: absolute; height: 64px; background: #ffffff; opacity: 0.92;
      box-shadow: 64px 32px 0 #ffffff, -64px 32px 0 #ffffff, 128px 32px 0 #f4f8fb; }}
  </style>
  <div id="root" data-composition-id="sky" data-width="1920" data-height="1080">
    <div id="sk-day"></div>
    <div id="sk-c1" class="sk-cloud" style="left: 140px; top: 80px; width: 384px"></div>
    <div id="sk-c2" class="sk-cloud" style="left: 940px; top: 40px; width: 512px"></div>
    <div id="sk-c3" class="sk-cloud" style="left: 1500px; top: 140px; width: 320px"></div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    tl.fromTo("#sk-c1", {{ x: 0 }}, {{ x: 70, duration: {DUR}, ease: "none" }}, 0);
    tl.fromTo("#sk-c2", {{ x: 0 }}, {{ x: 50, duration: {DUR}, ease: "none" }}, 0);
    tl.fromTo("#sk-c3", {{ x: 0 }}, {{ x: 40, duration: {DUR}, ease: "none" }}, 0);
    window.__timelines["sky"] = tl;
  </script>
</template>
""")

open("compositions/grade.html", "w").write(f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; pointer-events: none; }}
    .gr {{ position: absolute; inset: 0; }}
    #gr-sun {{ background: radial-gradient(ellipse 80% 70% at 30% 20%, rgba(255, 228, 160, 0.16), rgba(255, 228, 160, 0) 70%); }}
    #gr-vig {{ background: radial-gradient(ellipse 78% 72% at 50% 50%, rgba(0, 0, 0, 0) 58%, rgba(0, 0, 0, 0.30) 100%); }}
    #gr-fade {{ background: #000; opacity: 0; }}
  </style>
  <div id="root" data-composition-id="grade" data-width="1920" data-height="1080">
    <div id="gr-sun" class="gr"></div>
    <div id="gr-vig" class="gr"></div>
    <div id="gr-fade" class="gr"></div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    tl.to("#gr-fade", {{ opacity: 1, duration: 0.8, ease: "power1.in" }}, {DUR - 0.8});
    window.__timelines["grade"] = tl;
  </script>
</template>
""")

open("index.html", "w").write(f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="assets/vendor/gsap-3.14.2.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1920px; height: 1080px; overflow: hidden; background: #8cc6f0; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1920" data-height="1080">
      <div id="sky" data-composition-id="sky" data-composition-src="compositions/sky.html" data-start="0" data-duration="{DUR}" data-track-index="0" data-track-kind="graphics" data-width="1920" data-height="1080" style="z-index: 0"></div>
      <div id="world" data-composition-id="world" data-composition-src="compositions/world.html" data-start="0" data-duration="{DUR}" data-track-index="1" data-track-kind="graphics" data-width="1920" data-height="1080" style="z-index: 1"></div>
      <div id="grade" data-composition-id="grade" data-composition-src="compositions/grade.html" data-start="0" data-duration="{DUR}" data-track-index="2" data-track-kind="graphics" data-width="1920" data-height="1080" style="z-index: 2"></div>
      <audio id="music" src="assets/music/background--town-theme-rpg.mp3" data-start="0" data-duration="{DUR}" data-volume="0.9" data-fade-out="1.5" data-track-index="3"></audio>
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
""")
print("written:", len(world_html) // 1024, "KB world")
