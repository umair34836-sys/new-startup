#!/usr/bin/env python3
"""Kohinoor Traders REAL-logo motion-graphics reveal (16:9, ~10 s), 2026-11-25.
Logo = the client's own KNT red diamond, vectorised from the owner's brochure photo (cv2 red mask -> 9 pieces -> convex
hull + approxPolyDP; logo_clean.json). Style after the reference the owner sent (TikTok @kxjouanim "eye-catching
animation": dark frame, viewfinder corner brackets, outline draw-on, fill, glow, clean text reveal) + vfx_kit.py layer.
Urdu line copied exactly from the client's brochure in that photo.
python3 build_kohinoor_logo_motion.py PROJECT LOGO.json VFX.mp4
"""
import json, os, shutil, subprocess, sys, glob
P, LJ, VFX = sys.argv[1:4]
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
for d in ("vendor", "fonts", "audio"): os.makedirs(f"{P}/assets/{d}", exist_ok=True)
shutil.copy(VFX, f"{P}/assets/vfx.mp4"); shutil.copy(f"{REPO}/library/vendor/gsap-3.14.2.min.js", f"{P}/assets/vendor/")
for f in ("Montserrat-Variable.ttf", "NotoNastaliqUrdu-Variable.ttf"): shutil.copy(f"{REPO}/library/fonts/{f}", f"{P}/assets/fonts/")
for f in ("hyperframes.json", "meta.json", "package.json"): shutil.copy(f"{REPO}/video/{f}", P)
L = json.load(open(LJ)); polys = L["polys"]; T = 10.0; ASM = 2.3
RED = "#e8383d"; BG = "#0c0e15"
cx = lambda p: sum(x for x, _ in p) / len(p); cy = lambda p: sum(y for _, y in p) / len(p)
pts = lambda p: " ".join(f"{x},{y}" for x, y in p)
fill = "".join(f'<polygon id="pc{i}" points="{pts(p)}" fill="{RED}" style="transform-box:fill-box;transform-origin:50% 50%;"/>' for i, p in enumerate(polys))
line = "".join(f'<polygon class="ol" id="ol{i}" points="{pts(p)}" pathLength="100"/>' for i, p in enumerate(polys))
clip = "".join(f'<polygon points="{pts(p)}"/>' for p in polys)
svg = f'''<svg id="logo" viewBox="-10 -10 620 {L["h"] + 20}" width="440" height="{(L["h"] + 20) * 440 / 620:.0f}" style="position:absolute;left:740px;top:170px;overflow:visible;">
<defs><clipPath id="cl">{clip}</clipPath><linearGradient id="sw" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.5" stop-color="#fff" stop-opacity="0.75"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>
<g id="fills">{fill}</g><g clip-path="url(#cl)"><rect id="sweep" x="-300" y="-20" width="170" height="{L["h"] + 40}" fill="url(#sw)" transform="skewX(-22)"/></g>
<g id="lines">{line}</g></svg>'''
br = lambda i, css: f'<div id="{i}" style="position:absolute;width:70px;height:70px;{css}"></div>'
b = ['<div id="cam" style="position:absolute;inset:0;">',
     f'<video id="vfx" src="assets/vfx.mp4" data-start="0" data-duration="{T}" muted playsinline style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;mix-blend-mode:screen;"></video>',
     '<div id="frame" style="position:absolute;left:640px;top:120px;width:640px;height:520px;">',
     br("b1", "left:0;top:0;border-left:4px solid #fff;border-top:4px solid #fff;"), br("b2", "right:0;top:0;border-right:4px solid #fff;border-top:4px solid #fff;"),
     br("b3", "left:0;bottom:0;border-left:4px solid #fff;border-bottom:4px solid #fff;"), br("b4", "right:0;bottom:0;border-right:4px solid #fff;border-bottom:4px solid #fff;"),
     '<div id="xh" style="position:absolute;left:310px;top:250px;width:20px;height:20px;"><div style="position:absolute;left:9px;top:0;width:2px;height:20px;background:#fff;"></div><div style="position:absolute;top:9px;left:0;height:2px;width:20px;background:#fff;"></div></div>',
     '</div>', svg,
     '<div id="w1" style="position:absolute;left:0;right:0;top:650px;text-align:center;font-family:MS;font-weight:800;font-size:112px;color:#fff;line-height:1;">' +
     "".join(f'<span style="display:inline-block;overflow:hidden;vertical-align:top;"><span class="lt" style="display:inline-block;">{c}</span></span>' for c in "KOHINOOR") + '</div>',
     '<div id="w2" style="position:absolute;left:0;right:0;top:785px;text-align:center;font-family:MS;font-weight:700;font-size:56px;color:#fff;letter-spacing:4px;">TRADERS</div>',
     '<div id="ul" style="position:absolute;left:800px;width:320px;top:875px;height:3px;background:#e8383d;transform-origin:50% 50%;"></div>',
     '<div id="ur" lang="ur" style="position:absolute;left:0;right:0;top:895px;text-align:center;direction:rtl;font-family:NN;font-size:44px;line-height:1.9;color:#f1f1f4;">ہم آپ کے وقت کی قدر کرتے ہیں</div>',
     '<div id="cr" style="position:absolute;right:40px;bottom:26px;font-family:MS;font-weight:500;font-size:22px;color:rgba(255,255,255,0.45);">Edited by MrCopper804</div>',
     '</div>']
j = ['gsap.set(".ol",{strokeDasharray:100,strokeDashoffset:100});gsap.set("#fills polygon",{opacity:0});',
     'gsap.set(["#w2","#ur","#cr"],{opacity:0});gsap.set(".lt",{yPercent:110});gsap.set("#ul",{scaleX:0});gsap.set("#xh",{opacity:0});',
     # viewfinder brackets snap in, crosshair blinks, then brackets close onto the logo
     'tl.fromTo("#frame",{scale:1.6,opacity:0},{scale:1,opacity:1,duration:0.5,ease:"expo.out"},0.15);',
     'tl.to("#xh",{opacity:1,duration:0.05,repeat:5,yoyo:true},0.5);',
     f'tl.to("#frame",{{scale:0.86,duration:0.25,ease:"power3.in"}},{ASM - 0.25});tl.to("#frame",{{opacity:0,duration:0.15}},{ASM});']
for i, p in enumerate(polys):
    j.append(f'tl.to("#ol{i}",{{strokeDashoffset:0,duration:0.7,ease:"power2.inOut"}},{0.6 + i * 0.1:.2f});')
    dx, dy = (cx(p) - 300) * 0.5, (cy(p) - L["h"] / 2) * 0.5
    j.append(f'tl.fromTo("#pc{i}",{{opacity:0,x:{dx:.0f},y:{dy:.0f},scale:0.6,rotation:{(i % 3 - 1) * 14}}},{{opacity:1,x:0,y:0,scale:1,rotation:0,duration:0.45,ease:"expo.out"}},{ASM + i * 0.035:.3f});')
j += [f'tl.to("#lines",{{opacity:0,duration:0.3}},{ASM + 0.3});',
      f'tl.fromTo("#logo",{{scale:1.08,transformOrigin:"50% 50%"}},{{scale:1,duration:0.8,ease:"expo.out"}},{ASM});',
      f'tl.fromTo("#logo",{{filter:"drop-shadow(0 0 0px rgba(232,56,61,0))"}},{{filter:"drop-shadow(0 0 40px rgba(232,56,61,0.9))",duration:0.25,yoyo:true,repeat:1}},{ASM + 0.35});',
      f'tl.fromTo("#cam",{{x:-6,y:4}},{{x:0,y:0,duration:0.05,repeat:4,yoyo:true}},{ASM + 0.3});',
      f'tl.fromTo("#sweep",{{attr:{{x:-300}}}},{{attr:{{x:860}},duration:0.9,ease:"power2.inOut"}},{ASM + 0.8});',
      'tl.to(".lt",{yPercent:0,duration:0.6,ease:"expo.out",stagger:0.05},3.1);',
      'tl.fromTo("#w2",{opacity:0,scaleX:1.5},{opacity:1,scaleX:1,duration:0.8,ease:"expo.out"},3.6);',
      'tl.to("#ul",{scaleX:1,duration:0.6,ease:"expo.inOut"},4.1);',
      'tl.fromTo("#ur",{opacity:0,y:16,filter:"blur(8px)"},{opacity:1,y:0,filter:"blur(0px)",duration:0.7},4.6);',
      'tl.fromTo("#cr",{opacity:0},{opacity:1,duration:0.5},6.0);',
      f'tl.fromTo("#sweep",{{attr:{{x:-300}}}},{{attr:{{x:860}},duration:0.9,ease:"power2.inOut"}},7.2);',
      'tl.to("#logo",{y:-6,duration:2.5,ease:"sine.inOut",yoyo:true,repeat:1},5.0);']
A = f"{P}/assets/audio"; PV = "/home/user/tools/perc-venv/bin/python"; SF = f"{REPO}/library/sfx"
subprocess.run([PV, f"{REPO}/library/tools/music_fit.py", f"{REPO}/library/music/cc0/cinematic--eye-of-the-storm.mp3", f"{A}/music.wav", "--length", str(T), "--end", "fade", "--fade", "2"], check=True, capture_output=True)
sfx = [("whoosh-fast-0.3s.mp3", 0.12, 0.6), ("riser-2s.mp3", 0.4, 0.6), ("impact-boom.mp3", ASM, 0.9), ("glass-hit.mp3", ASM + 0.02, 0.5),
       ("magic-shimmer.mp3", ASM + 0.8, 0.45), ("whoosh-down-0.6s.mp3", 3.05, 0.5), ("sparkle.mp3", 7.2, 0.35)]
inp, fl = ["-i", f"{A}/music.wav"], []
for f, at, v in sfx:
    path = (glob.glob(f"{SF}/**/{f}", recursive=True) or [None])[0]
    if not path: continue
    inp += ["-i", path]; n = len(inp) // 2 - 1; ms = int(at * 1000)
    fl.append(f"[{n}]aresample=48000,aformat=channel_layouts=stereo,volume={v},adelay={ms}|{ms}[s{n}]")
k = len(inp) // 2
subprocess.run(["ffmpeg", "-v", "error", "-y", *inp, "-filter_complex", "[0]volume=0.6[m];" + ";".join(fl) + ";[m]" + "".join(f"[s{i}]" for i in range(1, k)) +
                f"amix=inputs={k}:normalize=0,atrim=0:{T},volume=3dB,alimiter=limit=0.7:level=false[o]", "-map", "[o]", f"{A}/mix.wav"], check=True)
open(f"{P}/index.html", "w").write(f'''<!doctype html><html lang="en" data-resolution="landscape"><head><meta charset="UTF-8"><meta name="viewport" content="width=1920, height=1080">
<script src="assets/vendor/gsap-3.14.2.min.js"></script><style>
@font-face{{font-family:"MS";src:url("assets/fonts/Montserrat-Variable.ttf");font-weight:100 900;}}@font-face{{font-family:"NN";src:url("assets/fonts/NotoNastaliqUrdu-Variable.ttf");font-weight:400 700;}}
*{{margin:0;padding:0;box-sizing:border-box;}}html,body{{width:1920px;height:1080px;overflow:hidden;background:{BG};}}
.ol{{fill:none;stroke:#ffffff;stroke-width:2.5;stroke-linejoin:round;}}</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{T}" data-width="1920" data-height="1080" style="position:absolute;inset:0;overflow:hidden;background:radial-gradient(ellipse at 50% 40%, #1c2030 0%, {BG} 70%);">
{chr(10).join(b)}
<audio id="mix" src="assets/audio/mix.wav" data-start="0" data-duration="{T}" data-volume="1.0" data-track-index="10"></audio>
</div><script>const tl=gsap.timeline({{paused:true}});
{chr(10).join(j)}
tl.to({{}},{{duration:{T}}},0);window.__timelines=window.__timelines||{{}};window.__timelines["main"]=tl;</script></body></html>''')
print("built", T)
