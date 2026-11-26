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
# detail on every beat: label facts + aquagreenwater.org + PCRWR report (sources in library/clients/aquagreen/brief.md)
FACTS = [(0, "SINCE 2019"), (1, "REVERSE OSMOSIS"), (2, "6-STAGE<br>PURIFICATION"), (4, "100% BATCHES<br>LAB TESTED"),
         (5, "PCRWR REPORT:<br>SAFE &#10003;<small>Govt. quality test, Oct–Dec 2025</small>"), (6, "500 ML"), (7, "1.5 L &bull; 19 L"),
         (8, "TDS 180–300"), (9, "pH 6.5–8.5"), (11, "HOME DELIVERY<br>6 DAYS A WEEK"), (12, "ISLAMABAD &amp;<br>RAWALPINDI"),
         (13, "WATER COOLERS"), (14, "10,000+ SAPLINGS<br>PLANTED")]
for k, txt in FACTS:
    word(f"f{k}", f'<span style="display:inline-block;padding:16px 30px 20px;border-radius:22px;background:rgba(5,10,20,0.78);">{txt}</span>', CUTS[k], CUTS[k + 1], f"left:50px;right:50px;top:290px;white-space:normal;text-align:center;font-family:AN;font-size:104px;line-height:1.02;color:{W};{SHD}")
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
