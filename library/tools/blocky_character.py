# Build a 3D Minecraft-style character (CSS 3D cubes, no WebGL) from a 64x64 skin as a HyperFrames scene.
#
#   python3 blocky_character.py OUT.html --skin assets/characters/host-skin.png \
#       --id host --duration 6 --scale 16 --moves '[[0,"idle"],[1,"wave"],[3,"talk"],[5,"idle"]]'
#
# Poses: idle (breathing sway), wave (right hand), talk (nods + gestures), walk (in place),
# point (arm toward the viewer), spin (one full turn). --turn sets the resting angle (degrees, 0 = facing
# the viewer); --x/--y place the feet in the frame. The skin path is written into the scene as is, so keep
# it project-root-relative (assets/...). Classic (4 px) arms; overlays (hat, jacket, sleeves, pants) included.
import argparse, json

ap = argparse.ArgumentParser()
ap.add_argument("out")
ap.add_argument("--skin", default="assets/characters/host-skin.png")
ap.add_argument("--id", default="host")
ap.add_argument("--duration", type=float, default=6)
ap.add_argument("--scale", type=float, default=16, help="screen px per skin pixel (character is 32 skin px tall)")
ap.add_argument("--width", type=int, default=1080)
ap.add_argument("--height", type=int, default=1920)
ap.add_argument("--x", type=float, default=None, help="feet x in px (default: centre)")
ap.add_argument("--y", type=float, default=None, help="feet y in px (default: 80%% of height)")
ap.add_argument("--turn", type=float, default=-22)
ap.add_argument("--tilt", type=float, default=-6, help="camera tilt in degrees (negative looks slightly down)")
ap.add_argument("--moves", default='[[0,"idle"]]')
a = ap.parse_args()
P, S = a.id, a.scale
X = a.width / 2 if a.x is None else a.x
Y = a.height * 0.8 if a.y is None else a.y
moves = json.loads(a.moves)

# (name, uv origin of the base layer, uv origin of the overlay, size w,h,d, box centre, pivot), skin px, y up.
PARTS = [
    ("head", (0, 0), (32, 0), (8, 8, 8), (0, 28, 0), (0, 24, 0), 0.5),
    ("body", (16, 16), (16, 32), (8, 12, 4), (0, 18, 0), (0, 18, 0), 0.25),
    ("rarm", (40, 16), (40, 32), (4, 12, 4), (-6, 18, 0), (-6, 22, 0), 0.25),
    ("larm", (32, 48), (48, 48), (4, 12, 4), (6, 18, 0), (6, 22, 0), 0.25),
    ("rleg", (0, 16), (0, 32), (4, 12, 4), (-2, 6, 0), (-2, 12, 0), 0.25),
    ("lleg", (16, 48), (0, 48), (4, 12, 4), (2, 6, 0), (2, 12, 0), 0.25),
]
SHADE = {"front": 1.0, "back": 0.78, "right": 0.86, "left": 0.86, "top": 1.08, "bottom": 0.6}

def faces(uv, size, grow):
    u, v = uv
    w, h, d = size
    W, H, D = (w + 2 * grow) * S, (h + 2 * grow) * S, (d + 2 * grow) * S
    regions = {  # face: (region x, y, w, h), face px size, transform
        "front": ((u + d, v + d, w, h), (W, H), f"translateZ({D / 2}px)"),
        "back": ((u + 2 * d + w, v + d, w, h), (W, H), f"rotateY(180deg) translateZ({D / 2}px)"),
        "right": ((u, v + d, d, h), (D, H), f"rotateY(-90deg) translateZ({W / 2}px)"),
        "left": ((u + d + w, v + d, d, h), (D, H), f"rotateY(90deg) translateZ({W / 2}px)"),
        "top": ((u + d, v, w, d), (W, D), f"rotateX(90deg) translateZ({H / 2}px)"),
        "bottom": ((u + d + w, v, w, d), (W, D), f"rotateX(-90deg) translateZ({H / 2}px)"),
    }
    out = []
    for name, ((rx, ry, rw, rh), (fw, fh), tf) in regions.items():
        kx, ky = fw / rw, fh / rh  # screen px per skin px on this face
        out.append(
            f'<i class="{P}-f" style="width:{fw:g}px;height:{fh:g}px;left:{-fw / 2:g}px;top:{-fh / 2:g}px;'
            f"transform:{tf};background-size:{64 * kx:g}px {64 * ky:g}px;"
            f'background-position:{-rx * kx:g}px {-ry * ky:g}px;filter:brightness({SHADE[name]})"></i>'
        )
    return "".join(out)

parts_html = []
for name, uv, ov, size, centre, pivot, grow in PARTS:
    px, py, pz = (c * S for c in pivot)
    cx, cy, cz = ((centre[i] - pivot[i]) * S for i in range(3))
    parts_html.append(
        f'      <div class="{P}-at" style="transform:translate3d({px:g}px,{-py:g}px,{pz:g}px)">\n'
        f'        <div id="{P}-{name}" class="{P}-pivot">\n'
        f'          <div class="{P}-box" style="transform:translate3d({cx:g}px,{-cy:g}px,{cz:g}px)">{faces(uv, size, 0)}</div>\n'
        f'          <div class="{P}-box" style="transform:translate3d({cx:g}px,{-cy:g}px,{cz:g}px)">{faces(ov, size, grow)}</div>\n'
        f"        </div>\n      </div>"
    )

# Keyed poses -> GSAP tweens (finite, deterministic).
js = []
segs = [(float(t), p) for t, p in moves] + [(a.duration, None)]
def tw(target, props, dur, at, ease="sine.inOut"):
    pr = ", ".join(f"{k}: {v}" for k, v in props.items())
    js.append(f'    tl.to("#{P}-{target}", {{ {pr}, duration: {dur:.3f}, ease: "{ease}" }}, {at:.3f});')
REST = {"rarm": {"rotationX": 0, "rotationZ": 3}, "larm": {"rotationX": 0, "rotationZ": -3},
        "rleg": {"rotationX": 0}, "lleg": {"rotationX": 0}, "head": {"rotationX": 0, "rotationY": 0}}
for (t0, pose), (t1, _) in zip(segs, segs[1:]):
    span = t1 - t0
    if span <= 0:
        continue
    settle = min(0.3, span / 3)
    OWN = {"idle": {"rarm", "larm"}, "wave": {"rarm", "head"}, "talk": {"head", "larm"},
           "walk": {"rarm", "larm", "rleg", "lleg"}, "point": {"rarm"}, "spin": set()}
    for part, props in REST.items():
        if part not in OWN.get(pose, set()):
            tw(part, props, settle, t0, "power2.out")
    if pose == "idle":
        n = max(1, int(span / 1.6))
        for k in range(n):
            s = t0 + k * span / n
            tw("rig", {"y": -0.35 * S}, span / n / 2, s)
            tw("rig", {"y": 0}, span / n / 2, s + span / n / 2)
            tw("rarm", {"rotationZ": 6}, span / n / 2, s)
            tw("rarm", {"rotationZ": 2}, span / n / 2, s + span / n / 2)
            tw("larm", {"rotationZ": -6}, span / n / 2, s)
            tw("larm", {"rotationZ": -2}, span / n / 2, s + span / n / 2)
    elif pose == "wave":
        up = min(0.35, span / 4)
        tw("rarm", {"rotationZ": 160, "rotationX": 0}, up, t0, "back.out(1.4)")
        n = max(1, int((span - 2 * up) / 0.32))
        for k in range(n):
            tw("rarm", {"rotationZ": 135 if k % 2 == 0 else 165}, 0.16, t0 + up + k * 0.32)
            tw("rarm", {"rotationZ": 160}, 0.16, t0 + up + k * 0.32 + 0.16)
        tw("rarm", {"rotationZ": 3}, up, t1 - up, "power2.inOut")
        tw("head", {"rotationZ": -6}, up, t0)
        tw("head", {"rotationZ": 0}, up, t1 - up)
    elif pose == "talk":
        n = max(1, int(span / 0.5))
        for k in range(n):
            s = t0 + k * span / n
            tw("head", {"rotationX": -7 if k % 2 == 0 else 3, "rotationY": 8 if k % 3 == 0 else -6}, span / n, s)
        e = min(0.4, span / 4)
        tw("larm", {"rotationX": -40, "rotationZ": -12}, e, t0, "back.out(1.4)")
        tw("larm", {"rotationX": -25}, max(0.05, span - 2 * e), t0 + e)
        tw("larm", {"rotationX": 0, "rotationZ": -3}, e, t1 - e)
    elif pose == "walk":
        body = span - 0.2
        n = max(1, int(body / 0.5))
        for k in range(n):
            s, sgn = t0 + k * body / n, (1 if k % 2 == 0 else -1)
            d = body / n
            tw("rleg", {"rotationX": 30 * sgn}, d, s)
            tw("lleg", {"rotationX": -30 * sgn}, d, s)
            tw("rarm", {"rotationX": -30 * sgn}, d, s)
            tw("larm", {"rotationX": 30 * sgn}, d, s)
            tw("rig", {"y": -0.6 * S}, d / 2, s)
            tw("rig", {"y": 0}, d / 2, s + d / 2)
        for part in ("rleg", "lleg", "rarm", "larm"):
            tw(part, {"rotationX": 0}, 0.2, t1 - 0.2)
    elif pose == "point":
        tw("rarm", {"rotationX": -85, "rotationZ": 8}, min(0.35, span / 3), t0, "back.out(1.6)")
        tw("rarm", {"rotationX": 0, "rotationZ": 3}, min(0.35, span / 3), t1 - min(0.35, span / 3))
    elif pose == "spin":
        js.append(f'    tl.fromTo("#{P}-rig", {{ rotationY: {a.turn} }}, {{ rotationY: {a.turn + 360}, duration: {span:.3f}, ease: "power1.inOut" }}, {t0:.3f});')
        js.append(f'    tl.set("#{P}-rig", {{ rotationY: {a.turn} }}, {t1:.3f});')

nl = "\n"
open(a.out, "w").write(f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; pointer-events: none; }}
    .{P}-stage {{ position: absolute; left: {X:g}px; top: {Y:g}px; width: 0; height: 0; perspective: {80 * S:g}px; perspective-origin: 0 {-16 * S:g}px; }}
    .{P}-cam, .{P}-rig, .{P}-at, .{P}-pivot, .{P}-box {{ position: absolute; left: 0; top: 0; width: 0; height: 0; transform-style: preserve-3d; }}
    .{P}-f {{ position: absolute; display: block; background-image: url("{a.skin}"); background-repeat: no-repeat; image-rendering: pixelated; backface-visibility: hidden; }}
  </style>
  <div id="root" data-composition-id="{P}" data-layout-allow-overflow data-width="{a.width}" data-height="{a.height}">
    <div class="{P}-stage">
      <div class="{P}-cam" style="transform: rotateX({a.tilt}deg)">
      <div id="{P}-rig" class="{P}-rig">
{nl.join(parts_html)}
      </div>
      </div>
    </div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    tl.set("#{P}-rig", {{ rotationY: {a.turn}, y: 0 }}, 0);
    tl.set(["#{P}-head", "#{P}-body", "#{P}-rleg", "#{P}-lleg"], {{ rotationX: 0, rotationY: 0, rotationZ: 0 }}, 0);
    tl.set("#{P}-rarm", {{ rotationX: 0, rotationZ: 3 }}, 0);
    tl.set("#{P}-larm", {{ rotationX: 0, rotationZ: -3 }}, 0);
{nl.join(js)}
    tl.to({{}}, {{ duration: {a.duration} }}, 0);
    window.__timelines["{P}"] = tl;
  </script>
</template>
""")
print(f"wrote {a.out}: {len(moves)} poses, {a.duration:g}s, {32 * S:g}px tall")
