#!/usr/bin/env python3
"""Aqua Green bottled water: 17.1 s "Cooler Edit" structure (TikTok @ubaid.4d 7699154533766712594, same cut times as
build_shangla_ads2.py cool mode / build_kohinoor_v3.py), 2026-11-26. Owner gave 6 phone photos of the bottle.
Real elements only: Ken-Burns shots cut from those photos; the bottle cut out with rembg (isnet-general-use) and sliced
into cap / shoulder / label / body for the exploded view; facts on screen read from the label in the photos
(500ml, pH 6.5-8.5, TDS 180-300, Bottled Drinking Water, UAN 033-111-110-52, www.aquagreenwaters.org).
VFX layer = library/tools/vfx_kit.py (water-blue bursts on the hits). Audio = the reference's own sound (owner's choice;
scratchpad only, never in git).
python3 build_aquagreen_cooler.py PROJECT SHOTS_DIR PARTS_DIR VFX.mp4 AUDIO.wav
"""
import os, shutil, sys
P, SH, PT, VFX, AUD = sys.argv[1:6]
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
for d in ("img", "vendor", "fonts", "audio"): os.makedirs(f"{P}/assets/{d}", exist_ok=True)
for f in os.listdir(SH): shutil.copy(f"{SH}/{f}", f"{P}/assets/img/{f}")
for n in ("cap", "shoulder", "label", "body"): shutil.copy(f"{PT}/p_{n}.png", f"{P}/assets/img/p_{n}.png")
shutil.copy(VFX, f"{P}/assets/vfx.mp4"); shutil.copy(AUD, f"{P}/assets/audio/mix.wav")
shutil.copy(f"{REPO}/library/vendor/gsap-3.14.2.min.js", f"{P}/assets/vendor/")
for f in ("Anton-Regular.ttf", "Montserrat-Variable.ttf"): shutil.copy(f"{REPO}/library/fonts/{f}", f"{P}/assets/fonts/")
for f in ("hyperframes.json", "meta.json", "package.json"): shutil.copy(f"{REPO}/video/{f}", P)
T = 17.1; CUTS = [5.2, 5.93, 6.57, 7.27, 7.83, 8.43, 9.73, 10.33, 11.07, 11.7, 12.4, 12.97, 13.67, 14.2, 14.87, 15.47]
BLUE, GREEN, K, W = "#1f6fd1", "#5cc23a", "#05080d", "#ffffff"
b, j = [], []; r2 = lambda x: round(x, 2)
def show(s, a, z):
    j.append(f'gsap.set("{s}",{{visibility:"hidden"}});tl.set("{s}",{{visibility:"visible"}},{r2(a)});')
    if z < T: j.append(f'tl.set("{s}",{{visibility:"hidden"}},{r2(z)});')
n = [0]
def shot(img, a, z, z0=1.0, z1=1.1, x=0, rot=0, look="", pos="50% 50%", filt=""):
    n[0] += 1; i = f"s{n[0]}"; d = r2(z - a)
    b.append(f'<div id="{i}" style="position:absolute;inset:0;overflow:hidden;"><div id="{i}z" style="position:absolute;inset:-3%;{filt}">'
             f'<img src="assets/img/{img}.jpg" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:{pos};"></div>')
    if look == "bands": b.append(f'<div style="position:absolute;left:0;right:0;top:0;height:400px;background:{W};"></div><div style="position:absolute;left:0;right:0;bottom:0;height:400px;background:{W};"></div>')
    if look == "box": b.append('<div style="position:absolute;left:0;right:0;top:0;height:290px;background:#000;"></div><div style="position:absolute;left:0;right:0;bottom:0;height:290px;background:#000;"></div>')
    b.append('</div>'); show(f"#{i}", a, z)
    j.append(f'tl.fromTo("#{i}z",{{scale:{z0},x:{x},rotation:{rot}}},{{scale:{z1},x:{-x},rotation:0,duration:{d},ease:"none"}},{r2(a)});')
PARTS = [("cap", 0, 268, -300, -30), ("shoulder", 268, 596, -150, 18), ("label", 596, 1102, 30, -10), ("body", 1102, 1987, 240, 8)]
def exploded(i, a, z, snap, sc=0.6):
    left = 540 - 637 * sc / 2; top = 960 - 1987 * sc / 2
    b.append(f'<div id="{i}" style="position:absolute;left:{left:.0f}px;top:{top:.0f}px;width:{637 * sc:.0f}px;height:{1987 * sc:.0f}px;">' +
             "".join(f'<img id="{i}{nm}" src="assets/img/p_{nm}.png" style="position:absolute;left:0;top:{y0 * sc:.0f}px;width:{637 * sc:.0f}px;height:{(y1 - y0) * sc:.0f}px;filter:drop-shadow(0 18px 30px rgba(0,0,0,0.6));">' for nm, y0, y1, _, _ in PARTS) + '</div>')
    show(f"#{i}", a, z)
    for k, (nm, _, _, dy, rt) in enumerate(PARTS):
        dx = (-1) ** k * 90
        j.append(f'tl.fromTo("#{i}{nm}",{{x:0,y:0,rotation:0}},{{x:{dx},y:{dy * sc:.0f},rotation:{rt},duration:0.32,ease:"power3.out"}},{r2(a + 0.02)});')
        j.append(f'tl.to("#{i}{nm}",{{x:{dx * 1.1:.0f},y:{dy * sc * 1.1:.0f},rotation:{rt * 1.25:.1f},duration:{r2(snap - a - 0.4)},ease:"none"}},{r2(a + 0.34)});')
        j.append(f'tl.to("#{i}{nm}",{{x:0,y:0,rotation:0,duration:0.2,ease:"power4.in"}},{r2(snap)});')
    j.append(f'tl.fromTo("#{i}",{{scale:1.07}},{{scale:1,duration:0.25,ease:"power2.out"}},{r2(snap + 0.2)});')
def word(i, html, a, z, css, fx="slam"):
    b.append(f'<div id="{i}" style="position:absolute;white-space:nowrap;line-height:1;{css}">{html}</div>'); show(f"#{i}", a, z)
    fr, to = {"slam": ('{scale:2.3,opacity:0}', '{scale:1,opacity:1,duration:0.25,ease:"power4.out"}'),
              "up": ('{y:80,opacity:0}', '{y:0,opacity:1,duration:0.3,ease:"power3.out"}')}[fx]
    j.append(f'tl.fromTo("#{i}",{fr},{to},{r2(a)});')
SHD = "text-shadow:0 6px 26px rgba(0,0,0,0.75);"
# 0-1.37 dark intro + caption bar; 1.37-2.97 push in; 2.97-5.2 exploded bottle
shot("full2", 0, 1.37, 1.15, 1.0, filt="filter:brightness(0.45) saturate(0.7);")
b.append(f'<div id="cap" style="position:absolute;z-index:5;left:0;right:0;top:0;height:250px;background:{W};"><div style="position:absolute;left:30px;right:30px;top:60px;text-align:center;font-family:AN;font-size:68px;line-height:1.05;color:{K};">EDITING RANDOM THINGS:<br>WATER BOTTLE</div></div>')
show("#cap", 0, 2.97)
shot("full1", 1.37, 2.97, 1.0, 1.75, pos="50% 45%")
j.append('tl.fromTo("#s2z",{filter:"blur(0px)"},{filter:"blur(12px)",duration:0.25},2.72);')
b.append(f'<div id="exbg" style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 45%, #0e3a6b 0%, {K} 75%);"></div>'); show("#exbg", 2.97, 5.2)
exploded("ex", 2.97, 5.2, 4.75)
# beat montage (one shot per cut)
SEQ = [("label", 1.25, "", "50% 50%"), ("full2", 1.4, "bands", "50% 45%"), ("back", 1.2, "", "50% 50%"), ("EX", 0, "", ""), ("minerals", 1.5, "box", "50% 50%"),
       ("angle", 1.3, "", "50% 40%"), ("label", 1.2, "bands", "50% 55%"), ("full1", 1.6, "", "50% 45%"), ("minerals", 1.35, "", "50% 40%"),
       ("angle", 1.25, "box", "50% 35%"), ("EX", 0, "", ""), ("back", 1.3, "bands", "50% 45%"), ("full2", 1.5, "", "50% 45%"), ("label", 1.2, "box", "50% 50%"), ("angle", 1.3, "", "50% 45%")]
for k, (im, z, look, pos) in enumerate(SEQ):
    a, e = CUTS[k], CUTS[k + 1]
    if im == "EX":
        b.append(f'<div id="eb{k}" style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 45%, #0e3a6b 0%, {K} 75%);"></div>'); show(f"#eb{k}", a, e)
        exploded(f"ex{k}", a, e, e - 0.25, sc=0.62)
    else:
        shot(im, a, e, z, 1.0 if k % 2 else z + 0.12, x=(40 if k % 3 == 0 else 0), rot=(4 if k % 4 == 1 else 0), look=look, pos=pos)
    tint = "rgba(31,111,209,0.6)" if k % 2 else "rgba(92,194,58,0.55)"
    b.append(f'<div id="fl{k}" style="position:absolute;inset:0;background:radial-gradient(circle at 50% 80%, {tint}, rgba(0,0,0,0) 60%);mix-blend-mode:screen;"></div>')
    show(f"#fl{k}", a, a + 0.18); j.append(f'tl.fromTo("#fl{k}",{{opacity:1}},{{opacity:0,duration:0.18}},{a});')
b.append(f'<video id="vfx" src="assets/vfx.mp4" data-start="0" data-duration="{T}" muted playsinline style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;mix-blend-mode:screen;"></video>')
b.append(f'<div id="gl" style="position:absolute;left:0;right:0;top:1560px;text-align:center;font-family:AN;font-size:66px;color:{W};text-shadow:0 0 18px {BLUE},0 0 40px {GREEN};">AQUA GREEN</div>'); show("#gl", 5.2, 15.47)
# detail on every beat as animated ELEMENTS (owner 2026-11-26: "text ke through nahi, elements ke through detailing"):
# drawn SVG infographics on a dark glass badge, 1-3 word label only. Facts: library/clients/aquagreen/brief.md.
LB, LG, WH = "#4aa8ff", "#6fdc48", "#ffffff"
def elem(k, label, inner, anim):
    a, e = CUTS[k], CUTS[k + 1]; i = f"el{k}"
    b.append(f'<div id="{i}" style="position:absolute;left:290px;top:230px;width:500px;height:560px;">'
             f'<div style="position:absolute;left:0;top:0;width:500px;height:500px;border-radius:50%;background:radial-gradient(circle, rgba(6,22,45,0.88) 0%, rgba(6,22,45,0.78) 62%, rgba(6,22,45,0) 72%);"></div>'
             f'<svg viewBox="0 0 200 200" width="500" height="500" style="position:absolute;left:0;top:0;overflow:visible;filter:drop-shadow(0 0 8px rgba(74,168,255,0.8));">'
             f'<circle id="{i}r" cx="100" cy="100" r="92" fill="none" stroke="{LB}" stroke-width="2" pathLength="100" stroke-dasharray="100" stroke-dashoffset="100"/>{inner}</svg>'
             f'<div style="position:absolute;left:-150px;right:-150px;top:515px;text-align:center;"><span style="display:inline-block;padding:8px 26px;border-radius:30px;background:rgba(6,22,45,0.88);border:2px solid {LB};font-family:MS;font-weight:800;font-size:44px;color:#fff;">{label}</span></div></div>')
    show(f"#{i}", a, e)
    j.append(f'tl.fromTo("#{i}",{{scale:0.6,opacity:0}},{{scale:1,opacity:1,duration:0.22,ease:"back.out(2)"}},{r2(a)});')
    j.append(f'tl.to("#{i}r",{{attr:{{"stroke-dashoffset":0}},duration:{r2(min(0.5, e - a - 0.05))},ease:"power2.out"}},{r2(a)});')
    d = e - a
    for line in anim(i, a, d): j.append(line)
def S(sel, fr, to, at, du, ease="power2.out"): return f'tl.fromTo("{sel}",{fr},{{...{to},duration:{du:.2f},ease:"{ease}"}},{at:.2f});'
DROP = "M100 40 C100 40 70 80 70 102 A30 30 0 0 0 130 102 C130 80 100 40 100 40Z"
# k0: logo ring pulse + rising bubbles (purity)
elem(0, "Since 2019", f'<path d="{DROP}" fill="{LB}" opacity="0.9"/><path d="M84 108 Q100 92 116 108 Q100 130 84 108Z" fill="{LG}"/>' + "".join(f'<circle id="el0b{n}" cx="{60 + n * 20}" cy="160" r="{3 + n % 3}" fill="none" stroke="{WH}" stroke-width="1.5"/>' for n in range(5)),
     lambda i, a, d: [S(f"#{i}b{n}", "{y:0,opacity:1}", "{y:-110,opacity:0}", a + n * 0.06, d - 0.1, "none") for n in range(5)])
# k1: reverse osmosis membrane - water passes, dirt blocked
elem(1, "Reverse Osmosis", f'<line x1="30" y1="100" x2="170" y2="100" stroke="{WH}" stroke-width="3" stroke-dasharray="4 3"/>' +
     "".join(f'<circle id="el1w{n}" cx="{45 + n * 22}" cy="40" r="5" fill="{LB}"/>' for n in range(6)) +
     "".join(f'<rect id="el1d{n}" x="{52 + n * 34}" y="40" width="9" height="9" fill="#a0784a"/>' for n in range(4)),
     lambda i, a, d: [S(f"#{i}w{n}", "{y:0}", "{y:120}", a + 0.03 * n, d - 0.1, "power1.in") for n in range(6)] + [S(f"#{i}d{n}", "{y:0}", "{y:48}", a + 0.03 * n, (d - 0.1) * 0.5, "power1.in") for n in range(4)])
# k2: 6 filter stages light up, drop falls through
elem(2, "6 Stages", "".join(f'<rect id="el2s{n}" x="55" y="{38 + n * 22}" width="90" height="14" rx="7" fill="none" stroke="{LB}" stroke-width="2.5"/>' for n in range(6)) + f'<circle id="el2d" cx="100" cy="28" r="6" fill="{WH}"/>',
     lambda i, a, d: [S(f"#{i}s{n}", f'{{fill:"rgba(74,168,255,0)"}}', f'{{fill:"{LB}"}}', a + n * d / 7, 0.1) for n in range(6)] + [S(f"#{i}d", "{y:0}", "{y:140}", a, d - 0.05, "none")])
# k3 = exploded bottle beat (no element)
# k4: lab flask fills + check
elem(4, "Lab Tested", f'<path d="M85 40 L85 85 L55 150 Q52 160 62 160 L138 160 Q148 160 145 150 L115 85 L115 40" fill="none" stroke="{WH}" stroke-width="4"/>'
     f'<clipPath id="el4c"><path d="M85 40 L85 85 L55 150 Q52 160 62 160 L138 160 Q148 160 145 150 L115 85 L115 40Z"/></clipPath>'
     f'<rect id="el4f" x="40" y="160" width="120" height="0" fill="{LB}" clip-path="url(#el4c)"/>'
     f'<path id="el4k" d="M120 60 L135 75 L165 42" fill="none" stroke="{LG}" stroke-width="8" stroke-linecap="round" pathLength="100" stroke-dasharray="100" stroke-dashoffset="100"/>',
     lambda i, a, d: [S(f"#{i}f", "{attr:{y:160,height:0}}", "{attr:{y:100,height:60}}", a, d * 0.6), S(f"#{i}k", '{attr:{"stroke-dashoffset":100}}', '{attr:{"stroke-dashoffset":0}}', a + d * 0.5, d * 0.35)])
# k5: govt test shield + check (PCRWR, Oct-Dec 2025: Safe)
elem(5, "PCRWR: Safe", f'<path id="el5s" d="M100 30 L155 50 L155 100 Q155 145 100 170 Q45 145 45 100 L45 50Z" fill="rgba(111,220,72,0.15)" stroke="{LG}" stroke-width="5" pathLength="100" stroke-dasharray="100" stroke-dashoffset="100"/>'
     f'<path id="el5k" d="M75 100 L93 118 L128 80" fill="none" stroke="{WH}" stroke-width="10" stroke-linecap="round" pathLength="100" stroke-dasharray="100" stroke-dashoffset="100"/>',
     lambda i, a, d: [S(f"#{i}s", '{attr:{"stroke-dashoffset":100}}', '{attr:{"stroke-dashoffset":0}}', a, d * 0.45), S(f"#{i}k", '{attr:{"stroke-dashoffset":100}}', '{attr:{"stroke-dashoffset":0}}', a + d * 0.45, d * 0.3)])
# k6/k7: bottle sizes 500 ml -> 1.5 L -> 19 L silhouettes
BOT = lambda x, w, h, n: f'<g id="el7b{n}" style="transform-box:fill-box;transform-origin:50% 100%;"><rect x="{x + w * 0.35}" y="{165 - h - 10}" width="{w * 0.3}" height="10" fill="{LB}"/><rect x="{x}" y="{165 - h}" width="{w}" height="{h}" rx="{w * 0.25}" fill="none" stroke="{WH}" stroke-width="3"/><rect x="{x + 3}" y="{165 - h * 0.6}" width="{w - 6}" height="{h * 0.6 - 3}" rx="{w * 0.2}" fill="{LB}" opacity="0.7"/></g>'
elem(6, "500 ml", BOT(80, 40, 95, 9).replace("el7b9", "el6b"), lambda i, a, d: [S(f"#{i}b", "{scaleY:0}", "{scaleY:1}", a, 0.3, "back.out(2)")])
elem(7, "1.5 L &middot; 19 L", BOT(40, 26, 60, 0) + BOT(78, 34, 85, 1) + BOT(122, 46, 115, 2),
     lambda i, a, d: [S(f"#{i}b{n}", "{scaleY:0}", "{scaleY:1}", a + n * 0.1, 0.25, "back.out(2)") for n in range(3)])
# k8: TDS - mineral bubbles rising (Ca Mg Na K from the label)
elem(8, "Minerals", "".join(f'<g id="el8m{n}"><circle cx="{50 + n * 33}" cy="150" r="15" fill="rgba(74,168,255,0.3)" stroke="{WH}" stroke-width="2"/><text x="{50 + n * 33}" y="155" text-anchor="middle" style="font-family:MS;font-weight:800;font-size:13px;fill:#fff;">{m}</text></g>' for n, m in enumerate(["Ca", "Mg", "Na", "K"])),
     lambda i, a, d: [S(f"#{i}m{n}", "{y:20,opacity:0}", f"{{y:{-70 - n * 8},opacity:1}}", a + n * 0.07, d - 0.1, "power1.out") for n in range(4)])
# k9: pH gauge, needle into the 6.5-8.5 band
elem(9, "pH 6.5&ndash;8.5", f'<path d="M40 130 A60 60 0 0 1 160 130" fill="none" stroke="rgba(255,255,255,0.35)" stroke-width="12"/><path d="M95 70 A60 60 0 0 1 133 82" fill="none" stroke="{LG}" stroke-width="12"/>'
     f'<line id="el9n" x1="100" y1="130" x2="100" y2="80" stroke="{WH}" stroke-width="5" stroke-linecap="round" style="transform-origin:100px 130px;"/><circle cx="100" cy="130" r="7" fill="{WH}"/>',
     lambda i, a, d: [S(f"#{i}n", "{rotation:-80}", "{rotation:25}", a, d * 0.7, "back.out(1.5)")])
# k10 = exploded bottle beat
# k11: delivery van along a road, 6 day dots
elem(11, "6 Days a Week", f'<line x1="25" y1="130" x2="175" y2="130" stroke="{WH}" stroke-width="3"/>' + "".join(f'<circle id="el11d{n}" cx="{35 + n * 26}" cy="150" r="6" fill="rgba(255,255,255,0.25)"/>' for n in range(6)) +
     f'<g id="el11v"><rect x="20" y="95" width="45" height="30" rx="4" fill="{LB}"/><rect x="65" y="105" width="18" height="20" rx="3" fill="{LB}"/><circle cx="35" cy="128" r="6" fill="{WH}"/><circle cx="72" cy="128" r="6" fill="{WH}"/></g>',
     lambda i, a, d: [S(f"#{i}v", "{x:-20}", "{x:95}", a, d - 0.05, "none")] + [S(f"#{i}d{n}", '{fill:"rgba(255,255,255,0.25)"}', f'{{fill:"{LG}"}}', a + n * d / 7, 0.08) for n in range(6)])
# k12: two pins joined by a drawn route (Islamabad - Rawalpindi)
PIN = lambda x, y, n: f'<g id="el12p{n}" style="transform-box:fill-box;transform-origin:50% 100%;"><path d="M{x} {y} C{x - 14} {y - 18} {x - 14} {y - 34} {x} {y - 34} C{x + 14} {y - 34} {x + 14} {y - 18} {x} {y}Z" fill="{LG if n else LB}"/><circle cx="{x}" cy="{y - 24}" r="5" fill="#06162d"/></g>'
elem(12, "ISB &middot; RWP", f'<path id="el12r" d="M60 120 Q100 60 140 135" fill="none" stroke="{WH}" stroke-width="4" stroke-dasharray="6 5"/>'
     f'<path id="el12m" d="M60 120 Q100 60 140 135" fill="none" stroke="#06162d" stroke-width="6" pathLength="100" stroke-dasharray="100" stroke-dashoffset="0"/>' + PIN(60, 122, 0) + PIN(140, 137, 1),
     lambda i, a, d: [S(f"#{i}p0", "{scale:0}", "{scale:1}", a, 0.2, "back.out(2)"), S(f"#{i}m", '{attr:{"stroke-dashoffset":0}}', '{attr:{"stroke-dashoffset":-100}}', a + 0.1, d * 0.5), S(f"#{i}p1", "{scale:0}", "{scale:1}", a + d * 0.55, 0.2, "back.out(2)")])
# k13: water cooler, hot / normal / cold taps
elem(13, "Water Coolers", f'<rect x="70" y="30" width="60" height="45" rx="12" fill="rgba(74,168,255,0.5)" stroke="{WH}" stroke-width="3"/><rect x="65" y="75" width="70" height="95" rx="6" fill="none" stroke="{WH}" stroke-width="3"/>' +
     "".join(f'<rect id="el13t{n}" x="{78 + n * 16}" y="95" width="10" height="14" rx="2" fill="{c}"/>' for n, c in enumerate(["#ff5a4a", WH, LB])) +
     f'<rect id="el13w" x="81" y="109" width="4" height="0" fill="{LB}"/>',
     lambda i, a, d: [S(f"#{i}t{n}", "{scale:0}", "{scale:1}", a + n * 0.08, 0.15, "back.out(3)") for n in range(3)] + [S(f"#{i}w", "{attr:{height:0}}", "{attr:{height:40}}", a + 0.3, d - 0.35, "none")])
# k14: sapling grows (10,000+ saplings planted)
elem(14, "10,000+ Saplings", f'<line x1="40" y1="165" x2="160" y2="165" stroke="#8a6a3c" stroke-width="5"/>'
     f'<path id="el14s" d="M100 165 L100 80" stroke="{LG}" stroke-width="6" stroke-linecap="round" pathLength="100" stroke-dasharray="100" stroke-dashoffset="100"/>'
     f'<path id="el14l1" d="M100 115 Q70 105 68 82 Q95 85 100 115Z" fill="{LG}" style="transform-box:fill-box;transform-origin:100% 100%;"/>'
     f'<path id="el14l2" d="M100 95 Q130 88 134 62 Q105 66 100 95Z" fill="{LG}" style="transform-box:fill-box;transform-origin:0% 100%;"/>',
     lambda i, a, d: [S(f"#{i}s", '{attr:{"stroke-dashoffset":100}}', '{attr:{"stroke-dashoffset":0}}', a, d * 0.45), S(f"#{i}l1", "{scale:0}", "{scale:1}", a + d * 0.35, 0.2, "back.out(2)"), S(f"#{i}l2", "{scale:0}", "{scale:1}", a + d * 0.5, 0.2, "back.out(2)")])
# end card (glitch name, real contact from the back label)
E = 15.47
b.append(f'<div id="end" style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 40%, #0b2d55 0%, {K} 70%);">'
         f'<div id="e1" style="position:absolute;left:0;right:0;top:640px;text-align:center;font-family:AN;font-size:170px;line-height:1;"><span style="color:{BLUE};">AQUA</span> <span style="color:{GREEN};">GREEN</span></div>'
         f'<div id="e2" style="position:absolute;left:0;right:0;top:830px;text-align:center;font-family:MS;font-weight:700;font-size:50px;color:{W};">Bottled Drinking Water</div>'
         f'<div id="e3" style="position:absolute;left:110px;right:110px;top:960px;padding:22px 0;border-radius:22px;background:{W};text-align:center;font-family:AN;font-size:84px;color:{K};">UAN 033-111-110-52</div>'
         f'<div id="e4" style="position:absolute;left:0;right:0;top:1140px;text-align:center;font-family:MS;font-weight:600;font-size:44px;color:#bfe3ff;">www.aquagreenwaters.org</div>'
         f'<div id="e6" style="position:absolute;left:0;right:0;top:1220px;text-align:center;font-family:MS;font-weight:600;font-size:40px;color:#ffffff;">Home delivery: Islamabad &amp; Rawalpindi</div>'
         f'<div id="e5" style="position:absolute;left:0;right:0;top:1780px;text-align:center;font-family:MS;font-weight:500;font-size:30px;color:rgba(255,255,255,0.55);">Edited by MrCopper804</div></div>')
show("#end", E, T + 1)
j += [f'tl.fromTo("#e1",{{opacity:0,skewX:40,x:-80}},{{opacity:1,skewX:0,x:0,duration:0.35,ease:"steps(6)"}},{E + 0.05});',
      f'tl.fromTo("#e1",{{x:-8}},{{x:0,duration:0.06,yoyo:true,repeat:4,ease:"steps(1)"}},{E + 0.6});',
      f'tl.fromTo("#e2",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.3}},{E + 0.3});',
      f'tl.fromTo("#e3",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2)"}},{E + 0.5});',
      f'tl.fromTo("#e4",{{opacity:0}},{{opacity:1,duration:0.3}},{E + 0.75});tl.fromTo("#e5",{{opacity:0}},{{opacity:1,duration:0.3}},{E + 0.9});']
b.append('<div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 50%, rgba(0,0,0,0) 50%, rgba(0,0,0,0.5) 100%);pointer-events:none;"></div>')
open(f"{P}/index.html", "w").write(f'''<!doctype html><html lang="en" data-resolution="portrait"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080, height=1920">
<script src="assets/vendor/gsap-3.14.2.min.js"></script><style>@font-face{{font-family:"AN";src:url("assets/fonts/Anton-Regular.ttf");}}@font-face{{font-family:"MS";src:url("assets/fonts/Montserrat-Variable.ttf");font-weight:100 900;}}
small{{display:block;font-family:MS;font-weight:600;font-size:40px;margin-top:14px;color:#cfe9ff;}}*{{margin:0;padding:0;box-sizing:border-box;}}html,body{{width:1080px;height:1920px;overflow:hidden;background:{K};}}</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{T}" data-width="1080" data-height="1920" style="position:absolute;inset:0;overflow:hidden;background:{K};">
{chr(10).join(b)}
<audio id="mix" src="assets/audio/mix.wav" data-start="0" data-duration="{T}" data-volume="1.0" data-track-index="10"></audio>
</div><script>const tl=gsap.timeline({{paused:true}});
{chr(10).join(j)}
tl.to({{}},{{duration:{T}}},0);window.__timelines=window.__timelines||{{}};window.__timelines["main"]=tl;</script></body></html>''')
print("built", T)
