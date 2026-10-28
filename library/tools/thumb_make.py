# Thumbnail / cover / poster maker: a small JSON spec -> HTML/CSS -> PNG (+ JPG under 2 MB) rendered in Chromium.
#
#   python3 library/tools/thumb_make.py spec.json out.png [--variants]
#
# Spec (all paths relative to the spec file; see library/templates/thumbnail/*.example.json):
#   {"size": "yt" | "short" | "square" | [w, h],
#    "bg": {"image": "frame.png", "blur": 0, "darken": 0.25, "saturate": 1.2, "zoom": 1.0, "pos": "50% 40%"}
#          or {"gradient": ["#0b1020", "#3b0d5c"], "angle": 135},
#    "vignette": 0.45,
#    "subject": {"image": "cutout.png", "side": "right", "height": 0.95, "x": null, "stroke": 10,
#                "stroke_color": "#ffffff", "glow": "#ffcc00", "flip": false},
#    "texts": [{"text": "100 PLAYERS", "x": 0.05, "y": 0.08, "w": 0.55, "size": 150, "font": "Anton",
#               "color": "#ffffff", "stroke": 14, "stroke_color": "#000000", "rotate": -3,
#               "box": "#e11d48", "accent": {"word": "100", "color": "#ffd400"}, "align": "left"}],
#    "stickers": [{"image": "../../emoji/noto/emoji_u1f525.png", "x": 0.7, "y": 0.1, "w": 0.12, "rotate": 10}],
#    "arrows": [{"from": [0.45, 0.75], "to": [0.62, 0.55], "color": "#ff2d2d", "width": 18}],
#    "circles": [{"x": 0.7, "y": 0.5, "r": 0.12, "color": "#ff2d2d", "width": 12}],
#    "badge": {"text": "NEW", "x": 0.04, "y": 0.8, "color": "#000", "bg": "#ffd400"}}
# x / y / w / r are fractions of the canvas width (y of the height). Fonts = files in library/fonts (family name =
# file stem before "-", e.g. Anton, BebasNeue, LuckiestGuy, Bangers, Montserrat, Poppins, NotoNastaliqUrdu).
# Writes out.png, out.jpg (YouTube phone upload limit 2 MB) and out.boxes.json (text boxes, used by thumb_check.py).
# --variants also writes out_bgonly.png (texts hidden) so thumb_check.py can measure text contrast.
# Renders with Node Playwright (require('playwright') works in this container; chromium needs no options).
import argparse, html, json, os, subprocess, sys, tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
FONTS = os.path.join(ROOT, "library", "fonts")
SIZES = {"yt": (1280, 720), "short": (1080, 1920), "square": (1080, 1080), "post45": (1080, 1350)}

ap = argparse.ArgumentParser()
ap.add_argument("spec")
ap.add_argument("out")
ap.add_argument("--variants", action="store_true", help="also render texts hidden (for thumb_check.py contrast)")
a = ap.parse_args()

spec = json.load(open(a.spec))
base = os.path.dirname(os.path.abspath(a.spec))
W, H = SIZES[spec.get("size", "yt")] if isinstance(spec.get("size", "yt"), str) else spec["size"]


def url(p):
    p = p if os.path.isabs(p) else os.path.join(base, p)
    if not os.path.exists(p):
        sys.exit(f"missing file: {p}")
    return "file://" + p


def font_faces():
    css, seen = [], set()
    for f in sorted(os.listdir(FONTS)):
        if not f.lower().endswith((".ttf", ".otf")):
            continue
        fam = f.split("-")[0].split(".")[0]
        weight = "100 900" if "Variable" in f else ("700" if "Bold" in f else "400")
        if "ExtraBold" in f:
            weight = "800"
        if "SemiBold" in f:
            weight = "600"
        style = "italic" if "Italic" in f else "normal"
        css.append(f'@font-face{{font-family:"{fam}";src:url("file://{FONTS}/{f}");font-weight:{weight};font-style:{style}}}')
        seen.add(fam)
    return "\n".join(css)


def outlined(path, px, color, glow, glow_px, tmpdir):
    # bake the outline + glow into the cutout with PIL: 16 stacked CSS drop-shadows on a big image made
    # Chromium's screenshot time out after 30 s (measured here 2026-10-28), this takes well under a second
    from PIL import Image, ImageColor, ImageFilter
    im = Image.open(path).convert("RGBA")
    pad = px + (glow_px if glow else 0) + 4
    big = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad))
    big.paste(im, (pad, pad), im)
    a = big.split()[-1].point(lambda v: 255 if v > 110 else 0)
    ring = a
    for _ in range(max(0, px) // 2):  # grow the silhouette 2 px per pass
        ring = ring.filter(ImageFilter.MaxFilter(5))
    out = Image.new("RGBA", big.size)
    if glow:
        g = ring.filter(ImageFilter.GaussianBlur(glow_px / 2)).point(lambda v: int(v * 0.9))
        out.paste(Image.new("RGBA", big.size, ImageColor.getrgb(glow) + (255,)), (0, 0), g)
    if px:
        out.paste(Image.new("RGBA", big.size, ImageColor.getrgb(color) + (255,)), (0, 0), ring.filter(ImageFilter.GaussianBlur(0.7)))
    out.alpha_composite(big)
    dst = os.path.join(tmpdir, "subject.png")
    out.save(dst)
    return dst, pad / im.height


tmp = tempfile.mkdtemp(prefix="thumb_")
parts = []
bg = spec.get("bg", {"gradient": ["#0b1020", "#2a0a4a"]})
if "image" in bg:
    f = f"blur({bg.get('blur', 0)}px) saturate({bg.get('saturate', 1.0)}) brightness({1 - bg.get('darken', 0.0)})"
    z = bg.get("zoom", 1.0)
    parts.append(f'<div class="bg" style="background-image:url(\'{url(bg["image"])}\');background-position:{bg.get("pos", "50% 50%")};'
                 f'filter:{f};transform:scale({z * (1.06 if bg.get("blur") else 1)})"></div>')
else:
    g = bg.get("gradient", ["#0b1020", "#2a0a4a"])
    parts.append(f'<div class="bg" style="background:linear-gradient({bg.get("angle", 135)}deg,{",".join(g)})"></div>')
if spec.get("vignette"):
    v = spec["vignette"]
    parts.append(f'<div class="full" style="background:radial-gradient(ellipse at center,rgba(0,0,0,0) 45%,rgba(0,0,0,{v}) 100%)"></div>')

s = spec.get("subject")
if s:
    src, padf = outlined(url(s["image"])[7:], s.get("stroke", 10), s.get("stroke_color", "#ffffff"), s.get("glow"),
                         s.get("glow_size", 30), tmp)
    h = s.get("height", 0.95) * H * (1 + 2 * padf)  # the baked outline/glow pad would otherwise shrink the person
    side = s.get("side", "right")
    pos = f"left:{s['x'] * W}px" if s.get("x") is not None else (f"{side}:{W * 0.02 - h * padf}px" if side in ("left", "right")
                                                                 else "left:50%;transform:translateX(-50%)")
    flip = "transform:scaleX(-1)" if s.get("flip") and "translateX" not in pos else ""
    parts.append(f'<img class="subj" src="file://{src}" style="height:{h}px;bottom:{-h * padf}px;{pos};{flip}">')

for c in spec.get("circles", []):
    r = c["r"] * W
    parts.append(f'<div class="full" style="pointer-events:none"><svg width="{W}" height="{H}"><ellipse cx="{c["x"] * W}" '
                 f'cy="{c["y"] * H}" rx="{r}" ry="{r * c.get("squash", 0.85)}" fill="none" stroke="{c.get("color", "#ff2d2d")}" '
                 f'stroke-width="{c.get("width", 12)}" transform="rotate({c.get("rotate", -8)} {c["x"] * W} {c["y"] * H})"/></svg></div>')
for ar in spec.get("arrows", []):
    (x1, y1), (x2, y2) = ar["from"], ar["to"]
    col, wd = ar.get("color", "#ff2d2d"), ar.get("width", 18)
    parts.append(f'<div class="full"><svg width="{W}" height="{H}"><defs><marker id="m{len(parts)}" markerWidth="4" markerHeight="4" '
                 f'refX="2.2" refY="2" orient="auto"><path d="M0,0 L4,2 L0,4 z" fill="{col}"/></marker></defs>'
                 f'<path d="M{x1 * W},{y1 * H} Q{(x1 + x2) / 2 * W + ar.get("bend", 0.05) * W},{(y1 + y2) / 2 * H} {x2 * W},{y2 * H}" '
                 f'stroke="{col}" stroke-width="{wd}" fill="none" stroke-linecap="round" marker-end="url(#m{len(parts)})" '
                 f'style="filter:drop-shadow(0 4px 6px rgba(0,0,0,.6))"/></svg></div>')
for st in spec.get("stickers", []):
    parts.append(f'<img class="stk" src="{url(st["image"])}" style="left:{st["x"] * W}px;top:{st["y"] * H}px;width:{st["w"] * W}px;'
                 f'transform:rotate({st.get("rotate", 0)}deg);filter:drop-shadow(0 6px 10px rgba(0,0,0,.55))">')

for i, t in enumerate(spec.get("texts", [])):
    words = html.escape(t["text"]).replace("\n", "<br>")
    acc = t.get("accent")
    if acc:
        for wd in (acc["word"] if isinstance(acc["word"], list) else [acc["word"]]):
            words = words.replace(html.escape(wd), f'<span style="color:{acc["color"]}">{html.escape(wd)}</span>')
    st = t.get("stroke", 12)
    box = (f"background:{t['box']};padding:{t.get('pad', 0.12)}em {t.get('pad', 0.12) * 2.5}em;"
           f"box-decoration-break:clone;-webkit-box-decoration-break:clone;") if t.get("box") else ""
    parts.append(f'<div class="txt" id="t{i}" style="left:{t.get("x", 0.05) * W}px;top:{t.get("y", 0.08) * H}px;'
                 f'width:{t.get("w", 0.6) * W}px;text-align:{t.get("align", "left")};transform:rotate({t.get("rotate", 0)}deg)">'
                 f'<span style="font-family:\'{t.get("font", "Anton")}\';font-size:{t.get("size", 120)}px;'
                 f'font-weight:{t.get("weight", 400)};line-height:{t.get("line", 1.0)};color:{t.get("color", "#fff")};'
                 f'-webkit-text-stroke:{st * 2}px {t.get("stroke_color", "#000")};paint-order:stroke fill;'
                 f'letter-spacing:{t.get("tracking", 0)}em;text-transform:{t.get("case", "none")};'
                 f'text-shadow:0 {max(4, st // 2)}px {st}px rgba(0,0,0,{t.get("shadow", 0.55)});{box}">{words}</span></div>')

b = spec.get("badge")
if b:
    parts.append(f'<div class="txt" id="badge" style="left:{b["x"] * W}px;top:{b["y"] * H}px"><span style="font-family:\'{b.get("font", "Anton")}\';'
                 f'font-size:{b.get("size", 60)}px;color:{b.get("color", "#000")};background:{b.get("bg", "#ffd400")};padding:.08em .35em;'
                 f'border-radius:.18em;box-shadow:0 6px 14px rgba(0,0,0,.5)">{html.escape(b["text"])}</span></div>')

page = f"""<!doctype html><html><head><meta charset="utf-8"><style>{font_faces()}
html,body{{margin:0;width:{W}px;height:{H}px;overflow:hidden;background:#000}}
.bg{{position:absolute;inset:0;background-size:cover}} .full{{position:absolute;inset:0}}
.subj,.stk{{position:absolute}} .txt{{position:absolute;transform-origin:left top}}
body.notext .txt{{visibility:hidden}}
</style></head><body>{''.join(parts)}</body></html>"""

out = os.path.abspath(a.out)
stem = os.path.splitext(out)[0]
open(os.path.join(tmp, "page.html"), "w").write(page)
js = f"""
const {{chromium}} = require('playwright');
(async () => {{
  const b = await chromium.launch({{args: ['--allow-file-access-from-files']}});
  const p = await b.newPage({{viewport: {{width: {W}, height: {H}}}}});
  await p.goto('file://{tmp}/page.html');
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(300);
  await p.screenshot({{path: {json.dumps(out)}}});
  const boxes = await p.evaluate(() => [...document.querySelectorAll('.txt')].map(e => {{
    const r = e.firstElementChild.getBoundingClientRect(); const cs = getComputedStyle(e.firstElementChild);
    return {{id: e.id, x: r.x, y: r.y, w: r.width, h: r.height, color: cs.color, box: cs.backgroundColor, size: parseFloat(cs.fontSize),
             stroke: cs.webkitTextStrokeWidth, text: e.innerText}}; }}));
  require('fs').writeFileSync({json.dumps(stem + '.boxes.json')}, JSON.stringify({{size: [{W}, {H}], boxes}}, null, 1));
  if ({'true' if a.variants else 'false'}) {{
    await p.evaluate(() => document.body.classList.add('notext'));
    await p.screenshot({{path: {json.dumps(stem + '_bgonly.png')}}});
  }}
  await b.close();
}})().catch(e => {{ console.error(e); process.exit(1); }});
"""
open(os.path.join(tmp, "render.js"), "w").write(js)
subprocess.run(["node", os.path.join(tmp, "render.js")], check=True)

# JPG copy under 2 MB (YouTube's phone-upload limit for video thumbnails: library/research/editing/skills2/16-thumbnails.md #4163)
from PIL import Image
im = Image.open(out).convert("RGB")
for q in (95, 92, 88, 84, 80, 75):
    im.save(stem + ".jpg", quality=q, optimize=True, progressive=True)
    if os.path.getsize(stem + ".jpg") < 2_000_000:
        break
print(f"wrote {out} ({W}x{H}), {stem}.jpg ({os.path.getsize(stem + '.jpg') / 1e6:.2f} MB, q{q}), {stem}.boxes.json"
      + (f", {stem}_bgonly.png" if a.variants else ""))
