#!/usr/bin/env python3
"""Kohinoor Traders: own-designed red diamond logo with "KNT" + 18 s VFX logo-reveal ad (9:16), 2026-11-25.
Owner (personal session): "kohinoor ka khod se design kia howa diamond logo banao us logo me knt hona chaye diamond color
red hoga and tum ek special ad bana do using vfx". VFX layer = library/tools/vfx_kit.py (procedural, no AI); logo = SVG
polygons (brilliant-cut side view) drawn with stroke-dash, filled on the impact, light sweep through a clipPath.
Facts on screen only from library/clients/kohinoor/brief.md (owner's words): auto parts dealer, authorized NPR dealer.
python3 build_kohinoor_vfx_reveal.py PROJECT VFX.mp4
"""
import os, shutil, subprocess, sys
P, VFX = sys.argv[1:3]
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
for d in ("vendor", "fonts", "audio"): os.makedirs(f"{P}/assets/{d}", exist_ok=True)
shutil.copy(VFX, f"{P}/assets/vfx.mp4"); shutil.copy(f"{REPO}/library/vendor/gsap-3.14.2.min.js", f"{P}/assets/vendor/")
for f in ("NotoSerif-Variable.ttf", "Montserrat-Variable.ttf"): shutil.copy(f"{REPO}/library/fonts/{f}", f"{P}/assets/fonts/")
for f in ("hyperframes.json", "meta.json", "package.json"): shutil.copy(f"{REPO}/video/{f}", P)
T = 18.0; IMP = 5.4
# ---- logo geometry (600 x 520 box): table T0..T3, girdle G0..G6, culet B
Tp = [(150, 0), (250, 0), (350, 0), (450, 0)]; Gp = [(x, 140) for x in range(0, 601, 100)]; B = (300, 520)
crown = [(Gp[0], Tp[0], Gp[1]), (Tp[0], Gp[2], Gp[1]), (Tp[0], Tp[1], Gp[2]), (Tp[1], Gp[3], Gp[2]), (Tp[1], Tp[2], Gp[3]),
         (Tp[2], Gp[4], Gp[3]), (Tp[2], Tp[3], Gp[4]), (Tp[3], Gp[5], Gp[4]), (Tp[3], Gp[6], Gp[5])]
pav = [(Gp[k], Gp[k + 1], B) for k in range(6)]
shades = ["#ff5a6a", "#e01c35", "#ff7584", "#c8102a", "#ff4257", "#b30d24", "#ff6676", "#d4152e", "#ff3b52",
          "#9e0a1f", "#d0142c", "#7d0617", "#e3203a", "#a10b21", "#6e0414"]
polys = crown + pav; pts = lambda p: " ".join(f"{x},{y}" for x, y in p)
facets = "".join(f'<polygon id="fa{i}" points="{pts(p)}" fill="{shades[i]}"/>' for i, p in enumerate(polys))
lines = "".join(f'<polygon class="ln" id="ln{i}" points="{pts(p)}" pathLength="100"/>' for i, p in enumerate(polys))
outline = f'{pts([Gp[0], Tp[0], Tp[3], Gp[6], B])}'
svg = f'''<svg id="dia" viewBox="-20 -20 640 560" width="640" height="560" style="position:absolute;left:220px;top:600px;overflow:visible;">
<defs><clipPath id="clip"><polygon points="{outline}"/></clipPath>
<linearGradient id="sw" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.5" stop-color="#fff" stop-opacity="0.85"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>
<g id="fill" style="opacity:0">{facets}</g>
<g clip-path="url(#clip)"><rect id="sweep" x="-260" y="-40" width="160" height="620" fill="url(#sw)" transform="skewX(-20)"/></g>
<g id="lines">{lines}</g>
<text id="knt" x="300" y="300" text-anchor="middle" style="font-family:NS;font-weight:800;font-size:150px;fill:#ffffff;stroke:#5a0010;stroke-width:4;paint-order:stroke;letter-spacing:6px;">KNT</text>
</svg>'''
b = [f'<div id="cam" style="position:absolute;inset:0;">',
     f'<video id="vfx" src="assets/vfx.mp4" data-start="0" data-duration="{T}" muted playsinline style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;"></video>',
     svg,
     '<div id="w1" style="position:absolute;left:0;right:0;top:1250px;text-align:center;font-family:NS;font-weight:700;font-size:118px;color:#fff;letter-spacing:10px;text-shadow:0 0 30px rgba(255,40,60,0.7);">KOHINOOR</div>',
     '<div id="w2" style="position:absolute;left:0;right:0;top:1395px;text-align:center;font-family:MS;font-weight:500;font-size:52px;color:#ffd6db;letter-spacing:22px;">TRADERS</div>',
     '<div id="bar" style="position:absolute;left:390px;width:300px;top:1490px;height:3px;background:#ff2a40;transform-origin:50% 50%;"></div>',
     '<div id="t1" style="position:absolute;left:0;right:0;top:1550px;text-align:center;font-family:MS;font-weight:600;font-size:46px;color:#fff;">Auto Parts Dealer</div>',
     '<div id="t2" style="position:absolute;left:0;right:0;top:1620px;text-align:center;font-family:MS;font-weight:500;font-size:40px;color:#ffb3bc;">Authorized NPR Dealer</div>',
     '<div id="cr" style="position:absolute;left:0;right:0;top:1820px;text-align:center;font-family:MS;font-weight:500;font-size:28px;color:rgba(255,255,255,0.55);">Edited by MrCopper804</div>',
     '</div>']
j = [f'gsap.set("#dia",{{opacity:0,transformOrigin:"50% 50%"}});', 'gsap.set(".ln",{strokeDasharray:100,strokeDashoffset:100});',
     'gsap.set(["#knt","#w1","#w2","#t1","#t2","#cr"],{opacity:0});gsap.set("#bar",{scaleX:0});',
     'tl.set("#dia",{opacity:1},3.2);']
for i in range(len(polys)):
    j.append(f'tl.to("#ln{i}",{{strokeDashoffset:0,duration:1.1,ease:"power2.inOut"}},{3.3 + i * 0.07:.2f});')
j += [f'tl.to("#fill",{{opacity:1,duration:0.12}},{IMP});', f'tl.to("#lines",{{opacity:0.35,duration:0.4}},{IMP + 0.1});',
      f'tl.fromTo("#dia",{{scale:1.18}},{{scale:1,duration:0.6,ease:"power4.out"}},{IMP});',
      f'tl.to("#dia",{{scale:1.07,duration:{T - IMP - 0.6},ease:"none"}},{IMP + 0.6});',
      f'tl.fromTo("#cam",{{x:-14,y:10}},{{x:0,y:0,duration:0.07,repeat:6,yoyo:true,ease:"none"}},{IMP});',
      f'tl.fromTo("#sweep",{{attr:{{x:-260}}}},{{attr:{{x:820}},duration:1.1,ease:"power2.inOut"}},{IMP + 0.9});',
      f'tl.fromTo("#sweep",{{attr:{{x:-260}}}},{{attr:{{x:820}},duration:1.1,ease:"power2.inOut"}},{IMP + 6.0});',
      f'tl.fromTo("#knt",{{opacity:0,scale:2.2,transformOrigin:"50% 50%"}},{{opacity:1,scale:1,duration:0.35,ease:"power4.in"}},6.1);',
      'tl.fromTo("#w1",{opacity:0,y:30,filter:"blur(14px)"},{opacity:1,y:0,filter:"blur(0px)",duration:0.8,ease:"power3.out"},7.9);',
      'tl.fromTo("#w2",{opacity:0,y:20},{opacity:1,y:0,duration:0.6,ease:"power3.out"},8.6);',
      'tl.to("#bar",{scaleX:1,duration:0.6,ease:"power3.inOut"},9.2);',
      'tl.fromTo("#t1",{opacity:0,y:20},{opacity:1,y:0,duration:0.5},10.6);',
      'tl.fromTo("#t2",{opacity:0,y:20},{opacity:1,y:0,duration:0.5},11.6);',
      'tl.fromTo("#cr",{opacity:0},{opacity:1,duration:0.6},14.5);']
# ---- audio: CC0 epic + SFX placed on the hits
A = f"{P}/assets/audio"; PV = "/home/user/tools/perc-venv/bin/python"; SF = f"{REPO}/library/sfx"
subprocess.run([PV, f"{REPO}/library/tools/music_fit.py", f"{REPO}/library/music/cc0/cinematic--komiku--action-epic.mp3", f"{A}/music.wav", "--length", str(T), "--end", "fade", "--fade", "2.5"], check=True, capture_output=True)
sfx = [("riser/riser-4s.mp3", 1.4, 0.9), ("whoosh/whoosh-long-1.2s.mp3", 3.2, 0.6), ("impact/impact-boom.mp3", IMP, 1.0),
       ("impact/glass-hit.mp3", IMP + 0.02, 0.7), ("impact/metal-hit.mp3", 6.45, 0.6), ("magic-shimmer.mp3", 6.5, 0.5),
       ("whoosh/whoosh-fast-0.3s.mp3", 7.85, 0.5), ("sparkle.mp3", IMP + 0.9, 0.4)]
import glob
inp, fl = ["-i", f"{A}/music.wav"], []
for k, (f, at, v) in enumerate(sfx):
    path = (glob.glob(f"{SF}/**/{os.path.basename(f)}", recursive=True) or [None])[0]
    if not path: continue
    inp += ["-i", path]; n = len(inp) // 2 - 1; ms = int(at * 1000)
    fl.append(f"[{n}]aresample=48000,aformat=channel_layouts=stereo,volume={v},adelay={ms}|{ms}[s{n}]")
mixin = "[0]volume=0.55[m];" + ";".join(fl) + ";[m]" + "".join(f"[s{i}]" for i in range(1, len(inp) // 2)) + f"amix=inputs={len(inp) // 2}:normalize=0,atrim=0:{T},alimiter=limit=0.89[o]"
subprocess.run(["ffmpeg", "-v", "error", "-y", *inp, "-filter_complex", mixin, "-map", "[o]", f"{A}/mix.wav"], check=True)
open(f"{P}/index.html", "w").write(f'''<!doctype html><html lang="en" data-resolution="portrait"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080, height=1920">
<script src="assets/vendor/gsap-3.14.2.min.js"></script><style>
@font-face{{font-family:"NS";src:url("assets/fonts/NotoSerif-Variable.ttf");font-weight:100 900;}}@font-face{{font-family:"MS";src:url("assets/fonts/Montserrat-Variable.ttf");font-weight:100 900;}}
*{{margin:0;padding:0;box-sizing:border-box;}}html,body{{width:1080px;height:1920px;overflow:hidden;background:#000;}}
.ln{{fill:none;stroke:#ffd0d6;stroke-width:3;stroke-linejoin:round;filter:drop-shadow(0 0 6px #ff2a40);}}
#dia{{filter:drop-shadow(0 0 40px rgba(255,30,55,0.55));}}</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{T}" data-width="1080" data-height="1920" style="position:absolute;inset:0;overflow:hidden;background:#000;">
{chr(10).join(b)}
<audio id="mix" src="assets/audio/mix.wav" data-start="0" data-duration="{T}" data-volume="1.0" data-track-index="10"></audio>
</div><script>const tl=gsap.timeline({{paused:true}});
{chr(10).join(j)}
tl.to({{}},{{duration:{T}}},0);window.__timelines=window.__timelines||{{}};window.__timelines["main"]=tl;</script></body></html>''')
print("built", T)
