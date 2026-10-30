# Brand-identity reveal film (16:9 or 9:16), driven by one reveal.json: logo construction on a grid -> lockup with
# spacing markers -> (music drop) browser mockup -> phone mockup -> 3D-stacked page cards -> typography card -> colour
# swatches -> stat widgets -> price/plan chart -> photo inserts -> social-post phone -> held end logo.
# Shot order and pacing follow library/research/ref-brand-identity-reveal.md (Solune / Design On Acid, measured 2026-10-27:
# quiet intro, drop at 7.4 s, beat cuts). Every scene length is a whole number of beats counted from the drop.
# usage (inside a project folder that holds the assets named in reveal.json):
#   python3 build.py reveal.json            -> index.html + compositions/*.html
# reveal.json keys: see reveal.example.json beside this file. mark_json comes from mark_to_svg.py.
import json, os, statistics, subprocess, sys

R = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "reveal.json"))
W, H = R.get("size", [1920, 1080])
PORT = H > W
C = R["colors"]
BG, CARD, SURF, TXT, MUT, ACC = C["bg"], C["card"], C["surface"], C["text"], C["muted"], C.get("accent", C["text"])
F = {f["role"]: f for f in R["fonts"]}  # display / body / mono
M = R["music"]
BEAT = 60.0 / M["bpm"]
DROP = M["drop_at"]                       # video time of the music drop
TOTAL = R.get("total", 30.0)
MARK = json.load(open(R["mark_json"]))

# scene list: (key, beats). Intro scenes are fixed seconds before the drop.
POST = [("browser", 4), ("phone", 4), ("stack", 8), ("type", 4), ("swatch", 4), ("stats", 4), ("chart", 4),
        ("photos", 2 * len(R["photos"])), ("social", 4)]
SC = [("construct", 0.0, round(DROP * 0.53, 3)), ("lockup", round(DROP * 0.53, 3), DROP)]
t = DROP
for k, b in POST:
    SC.append((k, round(t, 3), round(t + b * BEAT, 3))); t += b * BEAT
SC.append(("end", round(t, 3), TOTAL))
Wn = {k: (s, e) for k, s, e in SC}


def d_of(k):
    return round(Wn[k][1] - Wn[k][0], 3)


def dur(p):
    return round(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                      capture_output=True, text=True).stdout), 3)


CSS = f"""
    @font-face {{ font-family: "FD"; src: url("assets/fonts/{F['display']['file']}"); font-weight: 100 900; }}
    @font-face {{ font-family: "FB"; src: url("assets/fonts/{F['body']['file']}"); font-weight: 100 900; }}
    @font-face {{ font-family: "FM"; src: url("assets/fonts/{F['mono']['file']}"); font-weight: 100 900; }}
    #root {{ position: absolute; inset: 0; overflow: hidden; background: {BG}; }}
    .fd {{ font-family: FD; font-weight: {F['display'].get('weight', 700)}; color: {TXT}; letter-spacing: -1px; }}
    .fb {{ font-family: FB; color: {TXT}; }}
    .fm {{ font-family: FM; font-weight: 700; color: {MUT}; letter-spacing: 3px; text-transform: uppercase; }}
    .card {{ background: {CARD}; border: 2px solid rgba(255,255,255,0.14); border-radius: 22px; }}
    .lab {{ display: inline-block; font-family: FM; font-weight: 700; font-size: 30px; letter-spacing: 3px; color: {TXT};
            padding: 10px 20px; border: 2px solid rgba(255,255,255,0.3); border-radius: 8px; }}
    .grid {{ position: absolute; inset: -200px; background-image: linear-gradient(rgba(255,255,255,0.06) 2px, transparent 2px),
             linear-gradient(90deg, rgba(255,255,255,0.06) 2px, transparent 2px); background-size: 60px 60px; }}
    .cc {{ position: absolute; left: 0; right: 0; text-align: center; }}
"""


def comp(cid, html, js):
    return f"""<template>
  <style>{CSS}</style>
  <div id="root" data-composition-id="{cid}" data-width="{W}" data-height="{H}">
{html}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{js}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
"""


def push_in(sel, d, frm="x", drift=True):
    """beat cut: fast push in from the side (reference: push transitions), slow camera drift, no exit (hard cut out)"""
    off = {"x": f"x: {W * 0.35:.0f}", "y": f"y: {H * 0.35:.0f}", "s": "scale: 1.25"}[frm]
    js = f'    tl.fromTo("{sel}", {{ {off}, opacity: 0.0, filter: "blur(18px)" }}, {{ x: 0, y: 0, scale: 1, opacity: 1, filter: "blur(0px)", duration: 0.32, ease: "expo.out" }}, 0);\n'
    if drift:
        js += f'    tl.to("{sel}-cam", {{ scale: 1.06, duration: {d:.2f}, ease: "none" }}, 0);\n'
    return js


C_ = {}
cx, cy = W / 2, H / 2

# ---------- 1. logo construction on a grid (stroke draw-on per polygon, vertex dots, measured angle, fill wipe)
d = d_of("construct")
scale = min(W, H) * 0.62 / max(MARK["w"], MARK["h"])
ox, oy = cx - MARK["w"] * scale / 2, cy - MARK["h"] * scale / 2
paths, dots = [], []
for i, p in enumerate(MARK["polys"]):
    pts = " ".join(f"{ox + x * scale:.1f},{oy + y * scale:.1f}" for x, y in p)
    paths.append(f'<polygon id="c-p{i}" points="{pts}" fill="none" stroke="{TXT}" stroke-width="3" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>')
    paths.insert(0, f'<polygon class="c-ghost" points="{pts}" fill="{TXT}" opacity="0.18"/>')  # thumbnail at 0 s: the mark is already readable
    paths.append(f'<polygon id="c-f{i}" points="{pts}" fill="{TXT}" opacity="0"/>')
    for j, (x, y) in enumerate(p):
        dots.append(f'<circle class="c-dot" cx="{ox + x * scale:.1f}" cy="{oy + y * scale:.1f}" r="7" fill="{BG}" stroke="{TXT}" stroke-width="3"/>')
steep = [a for a in MARK["angles"] if a < 45]
ang = round(statistics.median(steep)) if steep else None  # measured slant of the long edges, degrees from vertical
# construction guide lines through the mark's bounding box
xs = [ox + x * scale for p in MARK["polys"] for x, _ in p]; ys = [oy + y * scale for p in MARK["polys"] for _, y in p]
x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
guides = "".join(f'<line class="c-g" x1="{a}" y1="{b}" x2="{c}" y2="{e}" stroke="rgba(255,255,255,0.35)" stroke-width="2" stroke-dasharray="10 10" pathLength="1"/>'
                 for a, b, c, e in [(0, y0, W, y0), (0, y1, W, y1), (x0, 0, x0, H), (x1, 0, x1, H)])
angle_svg = ""
if ang is not None:  # small arc + label at the first long edge's lower vertex
    angle_svg = (f'<g id="c-ang"><line x1="{x0 - 60}" y1="{y1 - 260}" x2="{x0 - 60}" y2="{y1 - 20}" stroke="{TXT}" stroke-width="2" stroke-dasharray="6 6"/>'
                 f'<text x="{x0 - 80}" y="{y1 - 130}" text-anchor="end" font-family="FM" font-weight="700" font-size="40" fill="{TXT}">{ang}°</text></g>')
C_["construct"] = comp("construct", f"""    <div class="grid" id="c-grid"></div>
    <svg id="c-svg" viewBox="0 0 {W} {H}" style="position:absolute;inset:0;width:{W}px;height:{H}px;">
      {guides}{''.join(paths)}{''.join(dots)}{angle_svg}
    </svg>
    <div class="fm" style="position:absolute;left:60px;top:{60 if not PORT else 200}px;font-size:30px;">{R['name']} — logo construction</div>""",
    '    tl.fromTo("#c-grid", { scale: 1.08 }, { scale: 1, duration: 3.0, ease: "power2.out" }, 0);\n'
    + "".join(f'    tl.to("#c-p{i}", {{ strokeDashoffset: 0, duration: 1.1, ease: "power2.inOut" }}, {0.35 + i * 0.09:.2f});\n' for i in range(len(MARK["polys"])))  # #427 draw-on 0.6-1.2 s, stagger 0.06-0.10
    + '    tl.fromTo(".c-dot", { scale: 0, transformOrigin: "50% 50%" }, { scale: 1, duration: 0.25, stagger: 0.03, ease: "back.out(3)" }, 0.9);\n'
    + ('    tl.fromTo("#c-ang", { opacity: 0 }, { opacity: 1, duration: 0.3 }, 1.6);\n' if angle_svg else "")
    + "".join(f'    tl.to("#c-f{i}", {{ opacity: 1, duration: 0.5, ease: "power2.out" }}, {d - 1.3 + i * 0.08:.2f});\n' for i in range(len(MARK["polys"])))
    + f'    tl.to(".c-dot, .c-g, #c-ang", {{ opacity: 0, duration: 0.4 }}, {d - 1.2:.2f});\n'
    + f'    tl.fromTo("#c-svg", {{ scale: 1.04 }}, {{ scale: 1.0, duration: 0.18, ease: "power2.out" }}, {d - 0.75:.2f});\n')  # settle 1.04 -> 1.00

# ---------- 2. lockup with spacing markers
d = d_of("lockup")
wm_w = W * (0.5 if not PORT else 0.8)
C_["lockup"] = comp("lockup", f"""    <div class="grid" style="opacity:0.5"></div>
    <div id="l-cam" style="position:absolute;inset:0;">
      <div id="l-box" style="position:absolute;left:{(W - wm_w) / 2:.0f}px;top:{cy - wm_w * 0.165:.0f}px;width:{wm_w:.0f}px;">
        <img src="assets/{R['wordmark']}" style="width:100%;display:block;" alt="{R['name']} logo">
        <div class="l-mk" style="position:absolute;inset:-60px;border:2px dashed rgba(255,255,255,0.4);"></div>
        <div class="l-mk fm" style="position:absolute;left:-60px;top:-110px;font-size:30px;">clear space</div>
      </div>
      <div class="cc fb" id="l-tag" style="top:{cy + wm_w * 0.25:.0f}px;font-size:{40 if not PORT else 44}px;font-weight:600;color:{MUT};">{R['tagline']}</div>
    </div>""",
    '    tl.fromTo("#l-box", { scale: 0.85, opacity: 0, filter: "blur(16px)" }, { scale: 1, opacity: 1, filter: "blur(0px)", duration: 0.6, ease: "expo.out" }, 0);\n'
    '    tl.fromTo(".l-mk", { opacity: 0, scale: 1.1 }, { opacity: 1, scale: 1, duration: 0.4, stagger: 0.1 }, 0.5);\n'
    '    tl.fromTo("#l-tag", { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: "power3.out" }, 1.0);\n'
    f'    tl.to("#l-cam", {{ scale: 1.05, duration: {d:.2f}, ease: "none" }}, 0);\n')


# ---------- 3. browser mockup
def browser(img, url, w, h):
    return (f'<div class="card" style="width:{w}px;height:{h}px;overflow:hidden;box-shadow:0 40px 120px rgba(0,0,0,0.8);">'
            f'<div style="height:56px;display:flex;align-items:center;gap:12px;padding-left:22px;border-bottom:2px solid rgba(255,255,255,0.12);background:{SURF};">'
            '<span style="width:14px;height:14px;border-radius:50%;background:#5e5e5e"></span><span style="width:14px;height:14px;border-radius:50%;background:#5e5e5e"></span>'
            '<span style="width:14px;height:14px;border-radius:50%;background:#5e5e5e"></span>'
            f'<span style="margin-left:22px;padding:6px 26px;border-radius:8px;background:{BG};font-family:FM;font-size:30px;color:{TXT};">{url}</span></div>'
            f'<img src="assets/{img}" style="width:100%;display:block;" alt="{url} page"></div>')


d = d_of("browser")
bw = W * 0.72 if not PORT else W * 0.9
C_["browser"] = comp("browser", f"""    <div class="grid" style="opacity:0.4"></div>
    <div id="b-w" style="position:absolute;left:{(W - bw) / 2:.0f}px;top:{(H - bw * 0.62) / 2:.0f}px;"><div id="b-w-cam">{browser(R['browser']['image'], R['browser']['url'], int(bw), int(bw * 0.62))}</div></div>""",
    push_in("#b-w", d, "y"))


# ---------- 4. phone mockup
def phone(inner, h):
    w = h * 0.49
    return (f'<div style="width:{w:.0f}px;height:{h:.0f}px;border-radius:{h * 0.07:.0f}px;border:14px solid #1b1b1b;background:{BG};overflow:hidden;'
            f'box-shadow:0 40px 120px rgba(0,0,0,0.8), 0 0 0 2px rgba(255,255,255,0.18);position:relative;">{inner}'
            f'<div style="position:absolute;top:14px;left:50%;width:{w * 0.3:.0f}px;height:30px;margin-left:-{w * 0.15:.0f}px;border-radius:20px;background:#000;"></div></div>')


d = d_of("phone")
ph = H * 0.86 if not PORT else H * 0.62
C_["phone"] = comp("phone", f"""    <div class="grid" style="opacity:0.4"></div>
    <div id="p-w" style="position:absolute;left:{cx - ph * 0.245:.0f}px;top:{cy - ph / 2:.0f}px;"><div id="p-w-cam">{phone(f'<img src="assets/{R["phone"]["image"]}" style="position:absolute;left:0;top:70px;width:100%;" alt="plan card">', ph)}</div></div>
    <div class="fm" id="p-l" style="position:absolute;left:{80 if not PORT else 60}px;top:{cy - 20 if not PORT else 160}px;font-size:28px;color:{TXT};">{R['phone'].get('label', '')}</div>""",
    push_in("#p-w", d, "x") + '    tl.fromTo("#p-l", { opacity: 0, x: -40 }, { opacity: 1, x: 0, duration: 0.3 }, 0.2);\n')

# ---------- 5. 3D-stacked page cards
d = d_of("stack")
n = len(R["stack"])
sw = W * 0.6 if not PORT else W * 0.78
cards = "".join(f'<div class="card s-c" style="position:absolute;left:0;top:0;width:{sw:.0f}px;height:{sw * 0.62:.0f}px;overflow:hidden;'
                f'transform: translate3d({i * 70}px, {-i * 60}px, {-i * 140}px);box-shadow:0 30px 90px rgba(0,0,0,0.8);">'
                f'<img src="assets/{img}" style="width:100%;display:block;" alt="page {i + 1}"></div>' for i, img in enumerate(R["stack"]))
C_["stack"] = comp("stack", f"""    <div class="grid" style="opacity:0.35"></div>
    <div style="position:absolute;inset:0;perspective:1800px;">
      <div id="s-rig" style="position:absolute;left:{cx - sw / 2 - 80:.0f}px;top:{cy - sw * 0.27:.0f}px;width:{sw:.0f}px;height:{sw * 0.62:.0f}px;transform-style:preserve-3d;">{cards}</div>
    </div>
    <div class="fm" style="position:absolute;left:60px;top:{60 if not PORT else 200}px;font-size:30px;">{R.get('stack_label', 'brand guidelines')}</div>""",
    f'    tl.fromTo("#s-rig", {{ rotationY: -38, rotationX: 22, z: -400 }}, {{ rotationY: -18, rotationX: 12, z: 0, duration: {d:.2f}, ease: "power2.out" }}, 0);\n'
    f'    tl.fromTo(".s-c", {{ y: 500, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.45, stagger: {BEAT:.3f}, ease: "expo.out" }}, 0);\n')

# ---------- 6. typography card
d = d_of("type")
rows = "".join(f'<div class="t-r" style="display:flex;align-items:baseline;gap:40px;border-top:2px solid rgba(255,255,255,0.12);padding:{22 if not PORT else 30}px 0;">'
               f'<div style="font-family:{ {"display": "FD", "body": "FB", "mono": "FM"}[f["role"]]};font-weight:{f.get("weight", 700)};font-size:{110 if not PORT else 96}px;color:{TXT};width:{220 if not PORT else 190}px;line-height:1;">Aa</div>'
               f'<div><div style="font-family:{ {"display": "FD", "body": "FB", "mono": "FM"}[f["role"]]};font-weight:{f.get("weight", 700)};font-size:{54 if not PORT else 46}px;color:{TXT};">{f["family"]}</div>'
               f'<div class="fm" style="font-size:28px;margin-top:8px;">{f["role"]} · {f.get("note", "")}</div></div></div>'
               for f in R["fonts"])
C_["type"] = comp("type", f"""    <div id="t-w" style="position:absolute;left:{W * 0.12:.0f}px;top:{H * 0.14:.0f}px;width:{W * 0.76:.0f}px;"><div id="t-w-cam">
      <div class="fm" style="font-size:30px;color:{TXT};margin-bottom:24px;">Typography</div>{rows}</div></div>""",
    push_in("#t-w", d, "x") + f'    tl.fromTo(".t-r", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.3, stagger: {BEAT / 2:.3f} }}, 0.1);\n')

# ---------- 7. colour swatches
d = d_of("swatch")
nsw = len(R["swatches"])
cols = 3 if PORT else nsw
cw = (W * 0.84) / cols
sws = "".join(f'<div class="sw" style="position:absolute;left:{(i % cols) * cw:.0f}px;top:{(i // cols) * (H * 0.3):.0f}px;width:{cw - 16:.0f}px;height:{H * (0.62 if not PORT else 0.27):.0f}px;'
              f'background:{s["hex"]};border:2px solid rgba(255,255,255,0.18);border-radius:18px;">'
              f'<div style="position:absolute;left:22px;bottom:22px;font-family:FM;font-weight:700;font-size:30px;color:{"#080808" if s.get("light") else "#ffffff"};">{s["hex"].upper()}</div>'
              f'<div style="position:absolute;left:22px;bottom:62px;font-family:FB;font-weight:700;font-size:28px;color:{"#333" if s.get("light") else "#999"};">{s["name"]}</div></div>'
              for i, s in enumerate(R["swatches"]))
C_["swatch"] = comp("swatch", f"""    <div style="position:absolute;left:{W * 0.08:.0f}px;top:{H * 0.08:.0f}px;" class="fm"><span style="font-size:30px;color:{TXT};">Colour</span></div>
    <div id="w-w" style="position:absolute;left:{W * 0.08:.0f}px;top:{H * 0.2:.0f}px;width:{W * 0.84:.0f}px;height:{H * 0.7:.0f}px;">{sws}</div>""",
    f'    tl.fromTo(".sw", {{ scaleY: 0, transformOrigin: "50% 100%" }}, {{ scaleY: 1, duration: 0.35, stagger: {BEAT / 3:.3f}, ease: "expo.out" }}, 0);\n')

# ---------- 8. stat widgets (UI cards)
d = d_of("stats")
st = R["stats"]
gc = 2 if (PORT or len(st) == 4) else len(st)
gw, gh = (W * 0.84) / gc, (H * (0.36 if not PORT else 0.22))
stc = "".join(f'<div class="card st" style="position:absolute;left:{(i % gc) * gw:.0f}px;top:{(i // gc) * (gh + 24):.0f}px;width:{gw - 24:.0f}px;height:{gh:.0f}px;padding:36px 44px;display:flex;flex-direction:column;justify-content:center;">'
              f'<div class="fd" style="font-size:{110 if not PORT else 90}px;line-height:1;">{s["value"]}</div>'
              f'<div class="fb" style="font-size:30px;color:{MUT};margin-top:18px;">{s["label"]}</div></div>' for i, s in enumerate(st))
C_["stats"] = comp("stats", f"""    <div class="grid" style="opacity:0.3"></div>
    <div id="g-w" style="position:absolute;left:{W * 0.08:.0f}px;top:{(H - (gh + 24) * ((len(st) + gc - 1) // gc)) / 2:.0f}px;width:{W * 0.84:.0f}px;"><div id="g-w-cam">{stc}</div></div>""",
    push_in("#g-w", d, "s") + f'    tl.fromTo(".st", {{ y: 80, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.3, stagger: 0.07, ease: "expo.out" }}, 0.05);\n')

# ---------- 9. chart card (bars from real values)
d = d_of("chart")
ch = R["chart"]
mx = max(ch["values"])
nb = len(ch["values"])
aw, ah = (W * 0.76, H * 0.5) if not PORT else (W * 0.84, H * 0.36)
bwid = aw / nb
bars = "".join(f'<div class="bar" style="position:absolute;left:{i * bwid + bwid * 0.15:.0f}px;bottom:60px;width:{bwid * 0.7:.0f}px;height:{(v / mx) * (ah - 120):.0f}px;'
               f'background:{TXT if i == ch.get("highlight", -1) else "rgba(255,255,255,0.35)"};border-radius:8px 8px 0 0;"></div>'
               f'<div class="fm" style="position:absolute;left:{i * bwid:.0f}px;width:{bwid:.0f}px;text-align:center;bottom:14px;font-size:28px;">{lab}</div>'
               f'<div class="fb bv" style="position:absolute;left:{i * bwid:.0f}px;width:{bwid:.0f}px;text-align:center;bottom:{(v / mx) * (ah - 120) + 70:.0f}px;font-size:30px;font-weight:700;">{ch.get("prefix", "")}{v:,}</div>'
               for i, (lab, v) in enumerate(zip(ch["labels"], ch["values"])))
C_["chart"] = comp("chart", f"""    <div id="h-w" class="card" style="position:absolute;left:{(W - aw - 80) / 2:.0f}px;top:{(H - ah - 140) / 2:.0f}px;width:{aw + 80:.0f}px;height:{ah + 140:.0f}px;"><div id="h-w-cam">
      <div class="fm" style="position:absolute;left:40px;top:34px;font-size:30px;color:{TXT};">{ch['title']}</div>
      <div style="position:absolute;left:40px;top:90px;width:{aw:.0f}px;height:{ah:.0f}px;">{bars}</div></div></div>""",
    push_in("#h-w", d, "y") + f'    tl.fromTo(".bar", {{ scaleY: 0, transformOrigin: "50% 100%" }}, {{ scaleY: 1, duration: 0.4, stagger: 0.06, ease: "expo.out" }}, 0.15);\n'
    '    tl.fromTo(".bv", { opacity: 0 }, { opacity: 1, duration: 0.25, stagger: 0.06 }, 0.4);\n')

# ---------- 10. photo inserts, one per 2 beats
d = d_of("photos")
pp = "".join(f'<div class="ph" id="ph{i}" style="position:absolute;inset:0;visibility:hidden;"><div id="ph{i}-cam" style="position:absolute;inset:0;background:url(assets/{p["image"]}) center/cover;"></div>'
             f'<div style="position:absolute;inset:0;background:linear-gradient(180deg, rgba(0,0,0,0) 55%, rgba(0,0,0,0.75) 100%);"></div>'
             f'<div class="lab" style="position:absolute;left:60px;top:{60 if not PORT else 300}px;background:rgba(0,0,0,0.6);">{p.get("label", "")}</div></div>'
             for i, p in enumerate(R["photos"]))
js = ""
for i in range(len(R["photos"])):
    t0 = round(i * 2 * BEAT, 3)
    js += f'    tl.set("#ph{i}", {{ visibility: "visible" }}, {t0});\n'
    js += f'    tl.fromTo("#ph{i}-cam", {{ scale: 1.25 }}, {{ scale: 1.08, duration: {2 * BEAT:.3f}, ease: "power2.out" }}, {t0});\n'
    if i + 1 < len(R["photos"]):
        js += f'    tl.set("#ph{i}", {{ visibility: "hidden" }}, {round((i + 1) * 2 * BEAT, 3)});\n'
C_["photos"] = comp("photos", pp, js)

# ---------- 11. social post on a phone
d = d_of("social")
so = R["social"]
post = (f'<div style="position:absolute;left:0;right:0;top:70px;padding:22px;display:flex;align-items:center;gap:16px;">'
        f'<div style="width:64px;height:64px;border-radius:50%;background:{SURF};border:2px solid rgba(255,255,255,0.3);display:flex;align-items:center;justify-content:center;">'
        f'<img src="assets/{R["mark"]}" style="width:44px;height:44px;" alt=""></div><div class="fb" style="font-weight:800;font-size:28px;">{R["name"]}</div></div>'
        f'<img src="assets/{so["image"]}" style="position:absolute;left:0;top:170px;width:100%;" alt="">'
        f'<div class="fb" style="position:absolute;left:22px;right:22px;top:{170 + ph * 0.49 * 0.56 + 20:.0f}px;font-size:28px;line-height:1.3;font-weight:600;">{so["text"]}</div>'
        + (f'<div style="position:absolute;left:22px;right:22px;top:{170 + ph * 0.49 * 0.56 + 140:.0f}px;text-align:center;background:{TXT};color:{BG};border-radius:12px;'
           f'padding:18px 0;font-family:FB;font-weight:800;font-size:30px;">{so["button"]}</div>' if so.get("button") else "")
        + f'<div class="fm" style="position:absolute;left:0;right:0;text-align:center;top:{170 + ph * 0.49 * 0.56 + 240:.0f}px;font-size:28px;">{R["url"]}</div>')
C_["social"] = comp("social", f"""    <div class="grid" style="opacity:0.4"></div>
    <div id="o-w" style="position:absolute;left:{cx - ph * 0.245:.0f}px;top:{cy - ph / 2:.0f}px;"><div id="o-w-cam">{phone(post, ph)}</div></div>""",
    push_in("#o-w", d, "x"))

# ---------- 12. held end logo
d = d_of("end")
C_["end"] = comp("end", f"""    <div id="e-w" style="position:absolute;inset:0;">
      <div class="cc" id="e-m" style="top:{cy - H * 0.3:.0f}px;"><img src="assets/{R['mark']}" style="width:{H * 0.32:.0f}px;height:{H * 0.32:.0f}px;" alt="{R['name']} mark"></div>
      <div class="cc fd" id="e-n" style="top:{cy + H * 0.06:.0f}px;font-size:{H * 0.12:.0f}px;">{R['name']}</div>
      <div class="cc" id="e-u" style="top:{cy + H * 0.24:.0f}px;"><span class="lab" style="font-size:34px;">{R['url']}</span></div>
    </div>""",
    '    tl.fromTo("#e-m", { scale: 0.6, opacity: 0, filter: "blur(16px)" }, { scale: 1, opacity: 1, filter: "blur(0px)", duration: 0.6, ease: "expo.out" }, 0);\n'
    '    tl.fromTo("#e-n", { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: "power3.out" }, 0.25);\n'
    '    tl.fromTo("#e-u", { opacity: 0 }, { opacity: 1, duration: 0.5 }, 0.6);\n'
    f'    tl.to("#e-w", {{ scale: 1.04, duration: {d:.2f}, ease: "none" }}, 0);\n')

os.makedirs("compositions", exist_ok=True)
for k, v in C_.items():
    open(f"compositions/{k}.html", "w").write(v)

divs = [f'      <div id="{k}" data-composition-id="{k}" data-composition-src="compositions/{k}.html" data-start="{s}" data-duration="{round(e - s, 3)}" '
        f'data-track-index="1" data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index: 1"></div>' for k, s, e in SC]

# audio: music from music.from so its drop lands on DROP; whoosh on every post-drop cut, impact on the drop
sfx = lambda n: f"assets/sfx/{n}.mp3"
A = [("music", f"assets/{M['file']}", 0, TOTAL, M.get("volume", 0.9), 10, M["from"]),
     ("riser", sfx("riser-2s"), round(DROP - 2.0, 2), dur(sfx("riser-2s")), 0.35, 11, 0),
     ("drop", sfx("impact-boom"), DROP, dur(sfx("impact-boom")), 0.4, 12, 0)]
for i, (k, s, e) in enumerate(SC[3:]):
    A.append((f"wh{i}", sfx("whoosh-fast-0.3s"), round(max(0, s - 0.08), 2), dur(sfx("whoosh-fast-0.3s")), 0.35, 13 + i % 2, 0))
A.append(("draw", sfx("riser-4s"), 0.3, min(dur(sfx("riser-4s")), Wn["construct"][1]), 0.15, 15, 0))
aud = "\n".join(f'      <audio id="{i}" src="{s}" data-start="{a}" data-duration="{dd}" data-volume="{v}" data-track-index="{ln}"'
                + (f' data-media-start="{ms}"' if ms else "") + (' data-fade-out="2.0"' if i == "music" else "") + "></audio>"
                for i, s, a, dd, v, ln, ms in A)
open("index.html", "w").write(f"""<!doctype html>
<html lang="en" data-resolution="{'portrait' if PORT else 'landscape'}">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="assets/vendor/gsap-3.14.2.min.js"></script>
    <style>* {{ margin: 0; padding: 0; box-sizing: border-box; }} html, body {{ margin: 0; width: {W}px; height: {H}px; overflow: hidden; background: {BG}; }}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="{W}" data-height="{H}">
{chr(10).join(divs)}
{aud}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
""")
print("built", W, "x", H, TOTAL, "s; measured mark slant", ang, "deg;", [(k, s, e) for k, s, e in SC])
