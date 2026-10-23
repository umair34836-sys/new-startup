# Build the "Baarish ki pehli shaam" music video (Blocky Monsoon) scenes from SPEC.md.
#   python3 -I build.py
import sys
sys.path.insert(0, "/home/user/new-startup/library/tools")
from voxel_world import World
import blocky_character as bc

DUR = 60.0
W = World("vw", B=64, tex="assets/textures", perspective=1300)
js = []

def tw(sel, props, dur, at, ease="power2.inOut"):
    pr = ", ".join(f"{k}: {v}" for k, v in props.items())
    js.append(f'    tl.to("{sel}", {{ {pr}, duration: {dur:.3f}, ease: "{ease}" }}, {at:.3f});')

def st(sel, props, at):
    pr = ", ".join(f"{k}: {v}" for k, v in props.items())
    js.append(f'    tl.set("{sel}", {{ {pr} }}, {at:.3f});')

# ---------------------------------------------------------------- ground
# Ground in 4x4-block tiles: Chrome drops a whole face once any part of it passes behind the camera,
# so one huge ground quad vanishes in close shots.
def tiled(x0, z0, x1, z1, tex, y=0.0, step=4):
    z = z0
    while z < z1:
        x = x0
        while x < x1:
            W.plane(x, y, z, min(step, x1 - x), min(step, z1 - z), tex)
            x += step
        z += step
tiled(-20, -34, -2.5, 20, "grass_top")
tiled(2.5, -34, 20, 20, "grass_top")
tiled(-2.5, -34, 2.5, -16.5, "grass_top")
tiled(-2.5, -11.99, 2.5, 20, "cobble", 0.01, 2.5)
tiled(-4, -16.5, 4, -11.99, "cobble", 0.01, 4)
for (x, z, w, d) in ((-1.6, 4.0, 1.8, 1.2), (0.6, -2.5, 1.5, 1.0), (-1.2, -7.6, 1.4, 0.9), (0.3, 10.0, 1.6, 1.1)):
    W.raw(f'<i class="vw-f" style="width:{w*64:.0f}px;height:{d*64:.0f}px;left:{-w*32:.0f}px;top:{-d*32:.0f}px;'
          f'transform:translate3d({(x+w/2)*64:.0f}px,-1.3px,{(z+d/2)*64:.0f}px) rotateX(90deg);'
          f'background:radial-gradient(ellipse at 50% 50%, rgba(40,70,110,0.85), rgba(20,40,70,0.55) 60%, rgba(20,40,70,0) 72%);border-radius:40%"></i>')

# ---------------------------------------------------------------- houses
def house(x0, z0, w, d, h, wall, facade_x):
    W.box(x0, 0, z0, w, h, d, wall)
    W.box(x0 - 0.5, h, z0 - 0.5, w + 1, 0.6, d + 1, "dark_planks")
    W.box(x0 + 0.5, h + 0.6, z0 + 0.5, w - 1, 0.6, d - 1, "dark_planks")
    W.box(x0 + 1.5, h + 1.2, z0 + 1, w - 3, 0.6, d - 2, "dark_planks")
    zc = z0 + d / 2
    fx = facade_x - 0.06 if facade_x > x0 else facade_x - 0.04
    for wz in (zc - 2.2, zc + 1.2):
        W.box(fx, 1.4, wz, 0.1, 1.1, 1.0, "window_lit", light=1.35)
    W.box(fx, 0, zc - 0.5, 0.1, 2.0, 1.0, "door")
for i, (z0, wall) in enumerate(((-10, "planks"), (-2, "cobble"), (6, "stone_brick"))):
    house(-11, z0, 6, 6, 4, wall, -5)
for i, (z0, wall) in enumerate(((-8, "stone_brick"), (0, "planks"), (8, "cobble"))):
    house(5, z0, 6, 6, 4, wall, 5)
for x0 in (-15, -6, 3, 11):
    house(x0, -30, 6, 5, 5, "planks" if x0 % 2 else "stone_brick", x0)
# trees
for (x, z) in ((-14, -15), (13, -14), (-15, 3), (14, 6), (-8, -20), (9, -21)):
    W.box(x, 0, z, 1, 4, 1, "log")
    W.box(x - 1.5, 3.2, z - 1.5, 4, 2.4, 4, "leaves")
    W.box(x - 0.5, 5.6, z - 0.5, 2, 1, 2, "leaves")

# ---------------------------------------------------------------- chai stall
W.box(-3.2, 0, -15.8, 6.4, 3.6, 0.4, "planks")
W.box(-3.2, 0, -15.4, 0.4, 3.4, 3.0, "planks")
W.box(2.8, 0, -15.4, 0.4, 3.4, 3.0, "planks")
W.box(-2.6, 0, -13.3, 5.2, 1.1, 1.0, "planks", top="dark_planks")
W.box(-3.1, 0, -12.5, 0.3, 3.5, 0.3, "log")
W.box(2.8, 0, -12.5, 0.3, 3.5, 0.3, "log")
for k, (y, z) in enumerate(((3.45, -12.9), (3.7, -14.1), (3.95, -15.3))):
    W.box(-3.4, y, z, 6.8, 0.25, 1.25, "awning")
W.box(-1.3, 4.25, -12.95, 2.6, 0.95, 0.15, "dark_planks")
W.raw('<i class="vw-f vw-sign" style="width:166px;height:61px;left:-83px;top:-30px;'
      'transform:translate3d(0px,-302px,-823px);display:flex;align-items:center;justify-content:center;'
      'font-family:\'Rozha One\';font-size:46px;color:#ffd36b;text-shadow:0 0 10px rgba(255,180,80,0.6)">चाय</i>')
W.box(-0.25, 2.55, -12.65, 0.5, 0.6, 0.5, "lantern", light=1.5)
W.box(-0.3, 3.15, -12.7, 0.6, 0.15, 0.6, "iron")
W.raw('<i class="vw-f" style="width:520px;height:420px;left:-260px;top:-210px;transform:translate3d(0px,-2px,-760px) rotateX(90deg);'
      'background:radial-gradient(ellipse at 50% 50%, rgba(255,180,90,0.55), rgba(255,160,70,0.18) 50%, rgba(255,160,70,0) 72%)"></i>')
# kettle + glasses on the counter (props)
W.box(1.2, 1.1, -13.1, 0.5, 0.45, 0.5, "iron")
W.box(1.32, 1.55, -12.98, 0.26, 0.15, 0.26, "iron")

# cups: on the counter, later in the two hands
CUPS = {"cupA": (-0.62, -12.95), "cupB": (0.32, -12.95)}
for cid, (x, z) in CUPS.items():
    W.group(cid, x, 1.1, z)
    W.box(-0.15, 0, -0.15, 0.3, 0.34, 0.3, "#f2efe8", top="#8a5a2b", group=cid)
    W.box(0.15, 0.08, -0.04, 0.08, 0.16, 0.08, "#f2efe8", group=cid)

# ---------------------------------------------------------------- street lamps (light up in the chorus)
LAMPS = [(-3.4, -9.0), (3.0, -9.0), (-3.4, -3.0), (3.0, -3.0), (-3.4, 3.0), (3.0, 3.0), (-3.4, 9.0), (3.0, 9.0)]
for i, (x, z) in enumerate(LAMPS):
    W.box(x, 0, z, 0.22, 3.0, 0.22, "iron")
    W.box(x - 0.14, 3.0, z - 0.14, 0.5, 0.6, 0.5, "iron")
    W.box(x - 0.15, 3.0, z - 0.15, 0.52, 0.6, 0.52, "lantern", cls=f"lamp{i}", light=1.6)
    W.box(x - 0.2, 3.6, z - 0.2, 0.62, 0.12, 0.62, "iron")
    W.raw(f'<i class="vw-f lamp{i}" style="width:420px;height:420px;left:-210px;top:-210px;transform:translate3d({(x+0.11)*64:.0f}px,-2px,{(z+0.11)*64:.0f}px) rotateX(90deg);'
          'background:radial-gradient(circle, rgba(255,200,110,0.6), rgba(255,170,80,0.2) 45%, rgba(255,170,80,0) 70%)"></i>')
    st(f".lamp{i}", {"opacity": 0}, 0)
    on = 38.0 + i * 0.85
    tw(f".lamp{i}", {"opacity": 1}, 0.15, on, "power1.out")

# ---------------------------------------------------------------- falling raindrop + splash (S1)
W.group("drop", -0.62, 7.0, -12.95)
W.box(-0.06, 0, -0.06, 0.12, 0.28, 0.12, "rgba(170,205,240,0.95)", group="drop")
tw("#drop", {"y": (7.0 - 1.5) * 64}, 0.5, 0.54, "power2.in")
st("#drop", {"visibility": '"hidden"'}, 1.04)
for k in range(8):
    import math
    ang = k * math.pi / 4
    sid = f"spl{k}"
    W.group(sid, -0.62, 1.46, -12.95)
    W.box(-0.04, 0, -0.04, 0.08, 0.08, 0.08, "rgba(190,220,250,0.95)", group=sid)
    st(f"#{sid}", {"visibility": '"hidden"'}, 0)
    st(f"#{sid}", {"visibility": '"visible"'}, 1.04)
    tw(f"#{sid}", {"x": math.cos(ang) * 22, "z": math.sin(ang) * 22, "y": -26}, 0.25, 1.04, "power2.out")
    tw(f"#{sid}", {"y": 4}, 0.25, 1.29, "power2.in")
    st(f"#{sid}", {"visibility": '"hidden"'}, 1.56)

# ---------------------------------------------------------------- the two characters
S = 64 * 1.85 / 32
W.group("him", 0, 0, 9)
W.raw(bc.rig_html("him", S, ""), group="him")
W.group("her", 8, 0, -10.6)
W.raw(bc.rig_html("her", S, ""), group="her")

him_moves = [[0, "idle"], [13.05, "run"], [17.6, "idle"], [18.1, "talk"], [19.4, "idle"], [24.0, "wave"], [26.0, "idle"],
             [29.4, "hold"], [36.6, "idle"]]
her_moves = [[0, "idle"], [19.5, "walk"], [23.5, "idle"], [26.2, "talk"], [28.6, "idle"], [29.6, "hold"], [36.6, "idle"]]
js += bc.pose_js("him", S, him_moves, DUR, 0)
js += bc.pose_js("her", S, her_moves, DUR, 0)
B = 64
# him: run up the lane, duck under the awning, face the camera, then turn to her
st("#him", {"rotationY": 180, "x": 0, "z": 0}, 0)
tw("#him", {"z": (-10.6 - 9) * B}, 4.55, 13.05, "none")
tw("#him", {"x": -0.9 * B}, 1.2, 16.4, "power2.out")
tw("#him", {"rotationY": 0}, 0.4, 17.6, "power2.out")
tw("#him", {"rotationY": 90}, 0.5, 21.0, "power2.inOut")
tw("#him", {"rotationY": 0}, 0.5, 36.8, "power2.inOut")
# her: appears at 19.5 to the east, walks in, faces him
st("#her", {"visibility": '"hidden"', "rotationY": -90}, 0)
st("#her", {"visibility": '"visible"'}, 19.5)
tw("#her", {"x": (0.9 - 8) * B}, 4.0, 19.5, "power1.out")
tw("#her", {"rotationY": 0}, 0.5, 36.9, "power2.inOut")

# cups: slide to the edge, then fly into the hands (S5)
tw("#cupA", {"z": 0.55 * B}, 0.6, 29.0, "power2.out")
tw("#cupB", {"z": 0.55 * B}, 0.6, 29.1, "power2.out")
handA = (-0.9 + 0.69, 1.12, -10.6 + 0.35)
handB = (0.9 - 0.69, 1.12, -10.6 - 0.35)
for cid, (hx, hy, hz) in (("cupA", handA), ("cupB", handB)):
    x0, z0 = CUPS[cid]
    tw(f"#{cid}", {"x": (hx - x0) * B, "y": -(hy - 1.1) * B, "z": (hz - z0) * B}, 0.6, 30.2, "power2.inOut")
    tw(f"#{cid}", {"x": 0, "y": 0, "z": 0.55 * B}, 0.5, 36.5, "power2.inOut")

# steam rising into a pixel heart between them (S5)
HEART = [".XX.XX.", "XXXXXXX", "XXXXXXX", ".XXXXX.", "..XXX..", "...X..."]
k = 0
for r, row in enumerate(HEART):
    for c, ch in enumerate(row):
        if ch != "X":
            continue
        sid = f"st{k}"
        tx, ty = (c - 3) * 0.14, 2.75 - r * 0.14
        sx, sz = (handA[0], handA[2]) if k % 2 == 0 else (handB[0], handB[2])
        W.group(sid, sx, 1.45, sz)
        W.box(-0.06, 0, -0.06, 0.12, 0.12, 0.12, "rgba(245,245,245,0.85)", faces=("front", "top", "left", "right"), group=sid)
        st(f"#{sid}", {"visibility": '"hidden"'}, 0)
        st(f"#{sid}", {"visibility": '"visible"'}, 31.6 + k * 0.035)
        tw(f"#{sid}", {"x": (tx - sx) * B, "y": -(ty - 1.45) * B, "z": (-10.6 - sz) * B}, 1.6, 31.6 + k * 0.035, "power2.out")
        tw(f"#{sid}", {"y": -(ty - 1.45 + 0.6) * B}, 0.7, 36.4, "power1.in")
        st(f"#{sid}", {"visibility": '"hidden"'}, 37.1)
        k += 1

# umbrella pops open on the 45.30 hit (S7)
W.group("umb", 0, 0, -10.6)
W.box(-0.05, 1.3, -0.05, 0.1, 1.25, 0.1, "iron", group="umb")
for (s, y) in ((3.2, 2.45), (2.2, 2.65), (1.0, 2.85)):
    W.box(-s / 2, y, -s / 2, s, 0.2, s, "wool_red", group="umb")
st("#umb", {"scale": 0.01, "visibility": '"hidden"'}, 0)
st("#umb", {"visibility": '"visible"'}, 45.15)
tw("#umb", {"scale": 1}, 0.45, 45.15, "back.out(1.6)")

# ---------------------------------------------------------------- camera (target in blocks, yaw, pitch, distance px)
cup = (-0.62, 1.4, -12.95)
cam = [
    (0.0, 0, "", cup, 10, 24, 270),
    (0.0, 3.5, "sine.inOut", cup, 4, 20, 205),
    (3.6, 0.7, "power3.in", (0, 5.5, 2), 0, 38, 1500),
    (4.3, 8.3, "power2.inOut", (0, 1.6, -9), 0, 12, 860),
    (13.05, 0, "", (0, 1.0, 8), -66, 8, 290),                     # hard cut: side tracking shot (west gap)
    (13.05, 4.55, "none", (0, 1.0, -9.6), -58, 8, 290),
    (17.6, 1.6, "power2.inOut", (-0.9, 1.15, -10.6), -12, 7, 520),
    (19.5, 3.4, "power2.inOut", (3.2, 1.05, -10.6), -8, 6, 640),
    (23.2, 5.0, "sine.inOut", (0, 1.1, -10.6), 10, 6, 470),
    (28.6, 0, "", (0, 1.45, -10.7), -6, 4, 360),                   # cut: chai close two-shot
    (28.6, 8.3, "sine.inOut", (0, 1.7, -10.7), 4, 6, 320),
    (37.19, 7.8, "power2.inOut", (0, 1.8, -8.5), 0, 20, 1250),
    (45.3, 7.7, "sine.inOut", (0, 1.2, -5), 28, 36, 2050),
    (53.0, 3.1, "power2.inOut", (0, 1.7, -10.6), 4, 8, 560),
    (56.14, 3.86, "sine.out", (0, 1.8, -10.6), 0, 7, 520),
]
import os
if os.environ.get("CAMTEST"):
    cam = [(0, 0, "", (0, 1, -5), 0, 30, 1500), (1, 0, "", (0, 1.2, -10.6), 0, 12, 600), (2, 0, "", (-0.62, 1.4, -12.95), 0, 16, 230)]
js += W.camera_js(cam)

# Zero-time sets at t=0 don't render on frame 0, so apply every initial state once before the timeline too.
import re
init_js = []
for line in js:
    m = re.match(r'\s*tl\.set\((.*), 0(?:\.0+)?\);$', line)
    if m:
        init_js.append(f"    gsap.set({m.group(1)});")
world_html = W.wrap(W.html("        "))
open("compositions/world.html", "w").write(f"""<template>
  <style>
    @font-face {{ font-family: "Rozha One"; src: url("assets/fonts/RozhaOne-Regular.ttf"); }}
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
print("world.html written:", len(world_html) // 1024, "KB")
