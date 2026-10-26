# Build a 3D Minecraft-style character (CSS 3D cubes, no WebGL) from a 64x64 skin as a HyperFrames scene.
#
#   python3 blocky_character.py OUT.html --skin assets/characters/host-skin.png \
#       --id host --duration 6 --scale 16 --moves '[[0,"idle"],[1,"wave"],[3,"talk"],[5,"idle"]]'
#
# Poses: idle (breathing sway), wave (right hand), talk (nods + gestures), walk / run (in place),
# point (arm toward the viewer), hold (forearm up, holding a cup), spin (one full turn).
# As a module: css(), rig_html(), pose_js() embed one or more characters in your own 3D scene. --turn sets the resting angle (degrees, 0 = facing
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
ap.add_argument("--beats", default=None, help='JSON [[t, strength 0-1], ...] speech onsets (e.g. word starts): "talk" nods on these '
                "instead of every 0.5 s, so the head moves with the voice")
ap.add_argument("--path", default=None, help='JSON [[t, x, y, scale, flip, dur], ...]: move/resize the character over time '
                "(x/y = feet px, scale = multiplier, flip = 1 faces the other way, dur = tween seconds; first entry is the start)")
# (name, uv origin of the base layer, uv origin of the overlay, size w,h,d, box centre, pivot, overlay grow), skin px, y up.
PARTS = [
    ("head", (0, 0), (32, 0), (8, 8, 8), (0, 28, 0), (0, 24, 0), 0.5),
    ("body", (16, 16), (16, 32), (8, 12, 4), (0, 18, 0), (0, 18, 0), 0.25),
    ("rarm", (40, 16), (40, 32), (4, 12, 4), (-6, 18, 0), (-6, 22, 0), 0.25),
    ("larm", (32, 48), (48, 48), (4, 12, 4), (6, 18, 0), (6, 22, 0), 0.25),
    ("rleg", (0, 16), (0, 32), (4, 12, 4), (-2, 6, 0), (-2, 12, 0), 0.25),
    ("lleg", (16, 48), (0, 48), (4, 12, 4), (2, 6, 0), (2, 12, 0), 0.25),
]
SHADE = {"front": 1.0, "back": 0.78, "right": 0.86, "left": 0.86, "top": 1.08, "bottom": 0.6}


def css(P, skin):
    """Classes the rig needs; append to the scene's <style>."""
    return (f".{P}-rig, .{P}-at, .{P}-pivot, .{P}-box {{ position: absolute; left: 0; top: 0; width: 0; height: 0; transform-style: preserve-3d; }}\n"
            f'.{P}-f {{ position: absolute; display: block; background-image: url("{skin}"); background-repeat: no-repeat; image-rendering: pixelated; backface-visibility: hidden; }}')


def _faces(P, S, uv, size, grow):
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


def rig_html(P, S, indent="      "):
    """The character: <div id="P-rig"> with six posable parts; feet at its origin, facing +z (the viewer)."""
    parts = []
    for name, uv, ov, size, centre, pivot, grow in PARTS:
        px, py, pz = (c * S for c in pivot)
        cx, cy, cz = ((centre[i] - pivot[i]) * S for i in range(3))
        parts.append(
            f'{indent}  <div class="{P}-at" style="transform:translate3d({px:g}px,{-py:g}px,{pz:g}px)">'
            f'<div id="{P}-{name}" class="{P}-pivot">'
            f'<div class="{P}-box" style="transform:translate3d({cx:g}px,{-cy:g}px,{cz:g}px)">{_faces(P, S, uv, size, 0)}</div>'
            f'<div class="{P}-box" style="transform:translate3d({cx:g}px,{-cy:g}px,{cz:g}px)">{_faces(P, S, ov, size, grow)}</div>'
            f"</div></div>"
        )
    return f'{indent}<div id="{P}-rig" class="{P}-rig">\n' + "\n".join(parts) + f"\n{indent}</div>"


def pose_js(P, S, moves, duration, turn=0.0, beats=None):
    """GSAP lines (for a timeline named tl) that play keyed poses: [[t, "idle"|"wave"|"talk"|"walk"|"run"|"point"|"hold"|"spin"|
    "shrug"|"think"|"shock"|"no"|"nod"], ...]. beats = [[t, strength], ...] speech onsets that "talk" nods on."""
    js = [f'    tl.set("#{P}-rig", {{ rotationY: {turn}, y: 0 }}, 0);',
          f'    tl.set(["#{P}-head", "#{P}-body", "#{P}-rleg", "#{P}-lleg"], {{ rotationX: 0, rotationY: 0, rotationZ: 0 }}, 0);',
          f'    tl.set("#{P}-rarm", {{ rotationX: 0, rotationZ: 3 }}, 0);',
          f'    tl.set("#{P}-larm", {{ rotationX: 0, rotationZ: -3 }}, 0);']
    segs = [(float(t), p) for t, p in moves] + [(duration, None)]

    def tw(target, props, dur, at, ease="sine.inOut"):
        pr = ", ".join(f"{k}: {v}" for k, v in props.items())
        js.append(f'    tl.to("#{P}-{target}", {{ {pr}, duration: {dur:.3f}, ease: "{ease}" }}, {at:.3f});')

    REST = {"rarm": {"rotationX": 0, "rotationZ": 3}, "larm": {"rotationX": 0, "rotationZ": -3},
            "rleg": {"rotationX": 0}, "lleg": {"rotationX": 0}, "head": {"rotationX": 0, "rotationY": 0}}
    OWN = {"idle": {"rarm", "larm"}, "wave": {"rarm", "head"}, "talk": {"head", "larm"}, "hold": {"rarm"},
           "walk": {"rarm", "larm", "rleg", "lleg"}, "run": {"rarm", "larm", "rleg", "lleg"}, "point": {"rarm"}, "spin": set(),
           "shrug": {"rarm", "larm", "head"}, "think": {"rarm", "head"}, "shock": {"rarm", "larm", "head"},
           "no": {"head", "rarm"}, "nod": {"head", "larm"}}
    for (t0, pose), (t1, _) in zip(segs, segs[1:]):
        span = t1 - t0
        if span <= 0:
            continue
        settle = min(0.3, span / 3)
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
            bt = [(float(b), float(v)) for b, v in (beats or []) if t0 <= float(b) < t1 - 0.08]
            if bt:   # one nod per spoken onset: dip on the word, recover before the next
                for k, (b, v) in enumerate(bt):
                    nxt = bt[k + 1][0] if k + 1 < len(bt) else t1
                    d = max(0.06, min(0.14, (nxt - b) / 2))
                    tw("head", {"rotationX": -4 - 8 * v, "rotationY": (6 if k % 2 == 0 else -6) * (0.5 + v)}, d, b, "power2.out")
                    tw("head", {"rotationX": 2, "rotationY": 0}, max(0.06, min(0.3, nxt - b - d)), b + d)
            else:
                n = max(1, int(span / 0.5))
                for k in range(n):
                    s = t0 + k * span / n
                    tw("head", {"rotationX": -7 if k % 2 == 0 else 3, "rotationY": 8 if k % 3 == 0 else -6}, span / n, s)
            e = min(0.4, span / 4)
            tw("larm", {"rotationX": -40, "rotationZ": -12}, e, t0, "back.out(1.4)")
            tw("larm", {"rotationX": -25}, max(0.05, span - 2 * e), t0 + e)
            tw("larm", {"rotationX": 0, "rotationZ": -3}, e, t1 - e)
        elif pose in ("walk", "run"):
            step, swing, bob = (0.5, 30, 0.6) if pose == "walk" else (0.3, 50, 1.0)
            body = span - 0.2
            n = max(1, int(body / step))
            for k in range(n):
                s, sgn = t0 + k * body / n, (1 if k % 2 == 0 else -1)
                d = body / n
                tw("rleg", {"rotationX": swing * sgn}, d, s)
                tw("lleg", {"rotationX": -swing * sgn}, d, s)
                tw("rarm", {"rotationX": -swing * sgn}, d, s)
                tw("larm", {"rotationX": swing * sgn}, d, s)
                tw("rig", {"y": -bob * S}, d / 2, s)
                tw("rig", {"y": 0}, d / 2, s + d / 2)
            for part in ("rleg", "lleg", "rarm", "larm"):
                tw(part, {"rotationX": 0}, 0.2, t1 - 0.2)
        elif pose == "point":
            tw("rarm", {"rotationX": -85, "rotationZ": 8}, min(0.35, span / 3), t0, "back.out(1.6)")
            tw("rarm", {"rotationX": 0, "rotationZ": 3}, min(0.35, span / 3), t1 - min(0.35, span / 3))
        elif pose == "hold":
            e = min(0.35, span / 3)
            tw("rarm", {"rotationX": -55, "rotationZ": -10}, e, t0, "power2.out")
            tw("rarm", {"rotationX": -50}, max(0.05, span - 2 * e), t0 + e)
            tw("rarm", {"rotationX": 0, "rotationZ": 3}, e, t1 - e)
        elif pose == "shrug":   # both arms out, head tilt: a question ("kya sochte hain?")
            e = min(0.3, span / 3)
            tw("rarm", {"rotationZ": 55, "rotationX": -20}, e, t0, "back.out(1.6)")
            tw("larm", {"rotationZ": -55, "rotationX": -20}, e, t0, "back.out(1.6)")
            tw("head", {"rotationZ": 10}, e, t0)
            for part, props in (("rarm", REST["rarm"]), ("larm", REST["larm"]), ("head", {"rotationZ": 0})):
                tw(part, props, e, t1 - e)
        elif pose == "think":   # hand to chin, head tilted up
            e = min(0.35, span / 3)
            tw("rarm", {"rotationX": -120, "rotationZ": -35}, e, t0, "power2.out")
            tw("head", {"rotationX": 8, "rotationZ": 6}, e, t0)
            tw("rarm", REST["rarm"], e, t1 - e)
            tw("head", {"rotationX": 0, "rotationZ": 0}, e, t1 - e)
        elif pose == "shock":   # both hands up to the head, small jump back
            e = min(0.2, span / 3)
            tw("rarm", {"rotationZ": 150, "rotationX": -30}, e, t0, "back.out(2)")
            tw("larm", {"rotationZ": -150, "rotationX": -30}, e, t0, "back.out(2)")
            tw("head", {"rotationX": 10}, e, t0)
            tw("rig", {"y": -0.8 * S}, e, t0, "power2.out")
            tw("rig", {"y": 0}, e, t0 + e, "power2.in")
            for part, props in (("rarm", REST["rarm"]), ("larm", REST["larm"]), ("head", {"rotationX": 0})):
                tw(part, props, e, t1 - e)
        elif pose == "no":   # head shake + flat hand: "bilkul nahi"
            e = min(0.3, span / 3)
            tw("rarm", {"rotationX": -70, "rotationZ": 30}, e, t0, "power2.out")
            n = max(2, int((span - 2 * e) / 0.22))
            for k in range(n):
                tw("head", {"rotationY": 14 if k % 2 == 0 else -14}, 0.11, t0 + e + k * 0.22)
                tw("head", {"rotationY": 0}, 0.11, t0 + e + k * 0.22 + 0.11)
            tw("rarm", REST["rarm"], e, t1 - e)
        elif pose == "nod":   # slow yes nods: agreement / "safe hai bro"
            n = max(1, int(span / 0.45))
            for k in range(n):
                tw("head", {"rotationX": -12}, 0.2, t0 + k * span / n)
                tw("head", {"rotationX": 2}, 0.2, t0 + k * span / n + 0.2)
        elif pose == "spin":
            js.append(f'    tl.fromTo("#{P}-rig", {{ rotationY: {turn} }}, {{ rotationY: {turn + 360}, duration: {span:.3f}, ease: "power1.inOut" }}, {t0:.3f});')
            js.append(f'    tl.set("#{P}-rig", {{ rotationY: {turn} }}, {t1:.3f});')
    return js


def main():
    a = ap.parse_args()
    P, S = a.id, a.scale
    X = a.width / 2 if a.x is None else a.x
    Y = a.height * 0.8 if a.y is None else a.y
    js = pose_js(P, S, json.loads(a.moves), a.duration, a.turn, json.loads(a.beats) if a.beats else None)
    path = json.loads(a.path) if a.path else []
    MOVE0 = ""
    if path:   # the stage itself moves: x/y in px from the initial feet point, scale and facing flip on #P-move
        t, x0, y0, sc, fl, _ = path[0]
        X, Y = x0, y0
        # fromTo renders its from-values immediately (frame 0 too) and owns the whole transform (no CSS transform)
        js.append(f'    tl.fromTo("#{P}-move", {{ x: 0, y: 0, scaleX: {-sc if fl else sc}, scaleY: {sc} }}, '
                  f'{{ x: 0, y: 0, scaleX: {-sc if fl else sc}, scaleY: {sc}, duration: 0.001 }}, 0);')
        for t, x, y, sc, fl, d in path[1:]:
            js.append(f'    tl.to("#{P}-move", {{ x: {x - x0:g}, y: {y - y0:g}, scaleX: {-sc if fl else sc}, scaleY: {sc}, duration: {d}, '
                      f'ease: "power3.inOut" }}, {t:.3f});')
    nl = "\n"
    open(a.out, "w").write(f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; pointer-events: none; }}
    .{P}-stage {{ position: absolute; left: {X:g}px; top: {Y:g}px; width: 0; height: 0; perspective: {80 * S:g}px; perspective-origin: 0 {-16 * S:g}px; }}
    .{P}-cam {{ position: absolute; left: 0; top: 0; width: 0; height: 0; transform-style: preserve-3d; }}
    {css(P, a.skin)}
  </style>
  <div id="root" data-composition-id="{P}" data-layout-allow-overflow data-width="{a.width}" data-height="{a.height}">
    <div class="{P}-stage"><div id="{P}-move" style="position:absolute;left:0;top:0;width:0;height:0;transform-origin:0 0;{MOVE0}">
      <div class="{P}-cam" style="transform: rotateX({a.tilt}deg)">
{rig_html(P, S, "      ")}
      </div>
    </div></div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{nl.join(js)}
    tl.to({{}}, {{ duration: {a.duration} }}, 0);
    window.__timelines["{P}"] = tl;
  </script>
</template>
""")
    print(f"wrote {a.out}: {len(json.loads(a.moves))} poses, {a.duration:g}s, {32 * S:g}px tall")


if __name__ == "__main__":
    main()
