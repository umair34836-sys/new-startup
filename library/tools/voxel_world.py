# Helpers for Minecraft-style worlds in CSS 3D (no WebGL) inside a HyperFrames scene.
# World units are blocks: x right, y up, z toward the viewer. B = px per block.
#
#   from voxel_world import World
#   w = World("vw", B=64, tex="assets/textures")
#   w.box(-2, 0, -13, 4, 1.2, 1, side="planks", top="planks")      # min corner + size
#   w.plane(-20, 0, -30, 40, 40, "grass_top")                      # ground (y = 0)
#   html = w.html()  # faces as absolutely positioned <i> elements inside #vw-world
#   css = w.css()    # classes + perspective camera
#   js  = w.camera_js([...])  # keyed camera moves for the scene's timeline
SHADE = {"top": 1.0, "front": 0.9, "back": 0.62, "right": 0.75, "left": 0.75, "bottom": 0.5}


class World:
    def __init__(self, P, B=64, tex="assets/textures", perspective=1300):
        self.P, self.B, self.tex, self.persp = P, B, tex, perspective
        self.items = []

    def _face(self, cx, cy, cz, w, h, tf, texname, shade, cls, extra, tile):
        B = self.B
        bs = B * tile
        # texname is a texture file name, or a CSS colour ("#rrggbb", "rgba(...)") for a flat face.
        paint = (f"background-color:{texname};" if texname.startswith(("#", "rgb")) else
                 f"background-image:url('{self.tex}/{texname}.png');background-size:{bs:.1f}px {bs:.1f}px;")
        return (f'<i class="{self.P}-f{(" " + cls) if cls else ""}" style="width:{w:.1f}px;height:{h:.1f}px;'
                f"left:{-w / 2:.1f}px;top:{-h / 2:.1f}px;transform:translate3d({cx:.1f}px,{-cy:.1f}px,{cz:.1f}px) {tf};"
                f'{paint}filter:brightness({shade});{extra}"></i>')

    def box(self, x, y, z, w, h, d, side, top=None, bottom=None, front=None, cls="", extra="", tile=1.0,
            faces=("top", "bottom", "front", "back", "left", "right"), group=None, light=1.0):
        """A cuboid from min corner (x, y, z) with size (w, h, d) in blocks."""
        B = self.B
        top, bottom, front = top or side, bottom or side, front or side
        cx, cy, cz = (x + w / 2) * B, (y + h / 2) * B, (z + d / 2) * B
        W, H, D = w * B, h * B, d * B
        spec = {
            "front": (W, H, f"translateZ({D / 2:.1f}px)", front),
            "back": (W, H, f"rotateY(180deg) translateZ({D / 2:.1f}px)", side),
            "right": (D, H, f"rotateY(90deg) translateZ({W / 2:.1f}px)", side),
            "left": (D, H, f"rotateY(-90deg) translateZ({W / 2:.1f}px)", side),
            "top": (W, D, f"rotateX(90deg) translateZ({H / 2:.1f}px)", top),
            "bottom": (W, D, f"rotateX(-90deg) translateZ({H / 2:.1f}px)", bottom),
        }
        out = [self._face(cx, cy, cz, fw, fh, tf, tn, round(SHADE[f] * light, 3), cls, extra, tile)
               for f, (fw, fh, tf, tn) in spec.items() if f in faces]
        self._add("".join(out), group)

    def plane(self, x, y, z, w, d, texname, cls="", extra="", tile=1.0, group=None, light=1.0):
        """A horizontal quad at height y covering x..x+w, z..z+d (faces up)."""
        B = self.B
        cx, cy, cz = (x + w / 2) * B, y * B, (z + d / 2) * B
        self._add(self._face(cx, cy, cz, w * B, d * B, "rotateX(90deg)", texname, light, cls, extra, tile), group)

    def raw(self, html, group=None):
        self._add(html, group)

    def group(self, gid, x=0, y=0, z=0):
        """Open a movable group (GSAP-able wrapper) at a block position; items added with group=gid go inside."""
        B = self.B
        self.items.append(("open", gid, (x * B, -y * B, z * B)))
        return gid

    def _add(self, html, group):
        self.items.append(("item", group, html))

    def html(self, indent="      "):
        groups, order, loose = {}, [], []
        for kind, gid, payload in self.items:
            if kind == "open":
                groups[gid] = (payload, [])
                order.append(gid)
            elif gid is None:
                loose.append(payload)
            else:
                groups[gid][1].append(payload)
        out = [indent + h for h in loose]
        for gid in order:
            (gx, gy, gz), items = groups[gid]
            out.append(f'{indent}<div class="{self.P}-g" style="transform:translate3d({gx:.1f}px,{gy:.1f}px,{gz:.1f}px)">'
                       f'<div id="{gid}" class="{self.P}-g">' + "".join(items) + "</div></div>")
        return "\n".join(out)

    def css(self):
        P = self.P
        return (f".{P}-view {{ position: absolute; inset: 0; perspective: {self.persp}px; perspective-origin: 50% 50%; overflow: hidden; }}\n"
                f".{P}-cam, .{P}-dolly, .{P}-pitch, .{P}-yaw, .{P}-pos, .{P}-g {{ position: absolute; left: 0; top: 0; width: 0; height: 0; transform-style: preserve-3d; }}\n"
                f".{P}-cam {{ left: 50%; top: 50%; }}\n"
                f".{P}-f {{ position: absolute; display: block; background-repeat: repeat; image-rendering: pixelated; backface-visibility: hidden; }}")

    def wrap(self, inner):
        """The camera rig around the world: dolly (distance), pitch, yaw, then the world moved to the target."""
        P = self.P
        return (f'<div class="{P}-view"><div class="{P}-cam"><div id="{P}-dolly" class="{P}-dolly"><div id="{P}-pitch" class="{P}-pitch">'
                f'<div id="{P}-yaw" class="{P}-yaw"><div id="{P}-pos" class="{P}-pos">\n{inner}\n'
                f"</div></div></div></div></div></div>")

    def camera_js(self, keys):
        """keys: [(t, dur, ease, (tx, ty, tz) target in blocks, yaw deg, pitch deg, distance px), ...].
        The first key is set instantly; each later key tweens from the previous state."""
        P, B, js = self.P, self.B, []
        for i, (t, dur, ease, (tx, ty, tz), yaw, pitch, dist) in enumerate(keys):
            props = [("dolly", {"z": self.persp - dist}), ("pitch", {"rotationX": -pitch}),
                     ("yaw", {"rotationY": -yaw}), ("pos", {"x": -tx * B, "y": ty * B, "z": -tz * B})]
            for part, p in props:
                pr = ", ".join(f"{k}: {v:.2f}" for k, v in p.items())
                if i == 0 or dur <= 0:
                    js.append(f'    tl.set("#{P}-{part}", {{ {pr} }}, {t:.3f});')
                else:
                    js.append(f'    tl.to("#{P}-{part}", {{ {pr}, duration: {dur:.3f}, ease: "{ease}" }}, {t:.3f});')
        return js
