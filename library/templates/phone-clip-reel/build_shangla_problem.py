#!/usr/bin/env python3
"""Shangla UPVC problem -> solution ad (2026-11-24), bright premium look (client feedback "not good" on the dark glitch
style; references were bright daylight UPVC shorts). Only REAL footage: problem = real weather/traffic stock
(library/stock weather + city-traffic, Mixkit videoFree 3304); solution = Shangla's own product clips. Real logo.
python3 build_shangla_problem.py PROJECT CLIPDIR VO MUSIC LOGO "t1,t2,...,t7,end"   (line start times in the VO, s)
"""
import os, shutil, subprocess, sys
P, CL, VO, MUS, LOGO, TS = sys.argv[1:7]
L = [float(x) for x in TS.split(",")]; L1, L2, L3, L4, L5, L6, L7, VEND = L
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
for d in ("clips", "vendor", "fonts", "audio", "img"): os.makedirs(f"{P}/assets/{d}", exist_ok=True)
for f in os.listdir(CL): shutil.copy(f"{CL}/{f}", f"{P}/assets/clips/{f}")
shutil.copy(f"{REPO}/library/vendor/gsap-3.14.2.min.js", f"{P}/assets/vendor/"); shutil.copy(LOGO, f"{P}/assets/img/logo.png")
for f in ("Poppins-SemiBold.ttf", "Anton-Regular.ttf"): shutil.copy(f"{REPO}/library/fonts/{f}", f"{P}/assets/fonts/")
for f in ("hyperframes.json", "meta.json", "package.json"): shutil.copy(f"{REPO}/video/{f}", P)
O = 0.4; t = lambda x: round(x + O, 2); T = round(VEND + O + 3.2, 2)
G, INK = "#3f8f1d", "#14181c"
b, j = [], []
def show(s, a, z):
    j.append(f'gsap.set("{s}",{{visibility:"hidden"}});tl.set("{s}",{{visibility:"visible"}},{a});')
    if z < T: j.append(f'tl.set("{s}",{{visibility:"hidden"}},{z});')
n = [0]
def shot(clip, a, z, z0=1.0, z1=1.08, cold=False, src0=0.0):
    n[0] += 1; i = f"v{n[0]}"; d = round(z - a, 2)
    flt = "filter:saturate(0.55) brightness(0.9) contrast(1.05) hue-rotate(-8deg);" if cold else "filter:brightness(1.05) saturate(1.05);"
    b.append(f'<div id="{i}" style="position:absolute;inset:0;overflow:hidden;"><div id="{i}z" style="position:absolute;inset:0;{flt}"><video id="{i}v" src="assets/clips/{clip}.mp4" data-start="{a}" data-duration="{d}" data-media-start="{src0}" muted playsinline style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;"></video></div></div>')
    show(f"#{i}", a, z); j.append(f'tl.fromTo("#{i}z",{{scale:{z0}}},{{scale:{z1},duration:{d},ease:"none"}},{a});')
    j.append(f'tl.fromTo("#{i}",{{opacity:0}},{{opacity:1,duration:0.25}},{a});')
def cap(i, txt, a, z, top=1380, dark=True, size=64):
    bg, fg = ("rgba(20,24,28,0.88)", "#ffffff") if dark else ("#ffffff", INK)
    b.append(f'<div id="{i}" style="position:absolute;left:70px;right:70px;top:{top}px;text-align:center;"><span style="display:inline-block;padding:18px 34px;border-radius:18px;background:{bg};color:{fg};font-family:PS;font-size:{size}px;line-height:1.2;box-shadow:0 12px 40px rgba(0,0,0,0.25);">{txt}</span></div>')
    show(f"#{i}", a, z); j.append(f'tl.fromTo("#{i}",{{y:40,opacity:0}},{{y:0,opacity:1,duration:0.35,ease:"power3.out"}},{a});')
# problem (real weather / traffic, cooled grade)
m1 = (L1 + L2) / 2
shot("snow", t(0) - O, t(m1), 1.0, 1.1, cold=True); shot("drip", t(m1), t(L2), 1.1, 1.0, cold=True)
cap("c1", "Sardiyon mein thandi hawa andar?", t(0) - O + 0.1, t(L2))
m2 = (L2 + L3) / 2
shot("rain", t(L2), t(m2), 1.0, 1.1, cold=True); shot("jam", t(m2), t(L3), 1.1, 1.0, cold=True, src0=1.0)
cap("c2", "Baarish, shor aur gard?", t(L2), t(m2)); cap("c3", "Ghar ka sukoon gaya?", t(m2), t(L3))
# turn
shot("room", t(L3), t(L4), 1.25, 1.0)
cap("c4", "Ab fikr chhodiye.", t(L3), t(L4), top=860, dark=False, size=80)
b.append('<div id="fl" style="position:absolute;inset:0;background:#fff;"></div>'); show("#fl", t(L3) - 0.05, t(L3) + 0.4)
j.append(f'tl.fromTo("#fl",{{opacity:0.9}},{{opacity:0,duration:0.4}},{t(L3) - 0.05});')
# solution (Shangla's own product footage)
shot("slide", t(L4), t(L5), 1.0, 1.1)
b.append(f'<div id="lg" style="position:absolute;left:340px;top:250px;width:400px;height:400px;border-radius:40px;background:#fff;box-shadow:0 20px 60px rgba(0,0,0,0.25);overflow:hidden;"><img src="assets/img/logo.png" style="width:100%;height:100%;object-fit:contain;"></div>')
show("#lg", t(L4), t(L5)); j.append(f'tl.fromTo("#lg",{{scale:0.7,opacity:0}},{{scale:1,opacity:1,duration:0.45,ease:"back.out(1.8)"}},{t(L4)});')
cap("c5", "Shangla UPVC<br>Windows &amp; Doors", t(L4) + 0.2, t(L5), top=1420, dark=False, size=70)
s = (L6 - L5) / 3
for k, (clip, txt) in enumerate([("xsec", "Single &amp; Double Glazed"), ("prof2", "Mazboot Profile"), ("close", "Behtareen Finishing")]):
    a, z = t(L5 + k * s), t(L5 + (k + 1) * s); shot(clip, a, z, 1.0 if k % 2 else 1.12, 1.12 if k % 2 else 1.0, src0=0.5 if k == 2 else 0.0)
    cap(f"f{k}", f'<span style="color:{G};">&#10003;</span> {txt}', a, z, dark=False)
shot("prof3", t(L6), t(L7), 1.0, 1.1)
cap("c6", "Thandi hawa, shor, gard: bahar.<br>Sukoon: andar.", t(L6), t(L7), dark=False, size=60)
# end card (white, real logo, number)
E = t(L7)
b.append(f'<div id="end" style="position:absolute;inset:0;background:#f7f7f4;"><img src="assets/img/logo.png" style="position:absolute;left:290px;top:380px;width:500px;height:500px;object-fit:contain;">'
         f'<div style="position:absolute;left:0;right:0;top:960px;text-align:center;font-family:PS;font-size:58px;color:{INK};">UPVC Windows &amp; Doors</div>'
         f'<div id="ph" style="position:absolute;left:150px;right:150px;top:1100px;padding:24px 0;border-radius:24px;background:{G};text-align:center;font-family:AN;font-size:96px;color:#fff;">0313-512-0718</div>'
         f'<div style="position:absolute;left:0;right:0;top:1290px;text-align:center;font-family:PS;font-size:46px;color:{INK};">Aaj hi call karein</div>'
         f'<div style="position:absolute;left:0;right:0;top:1780px;text-align:center;font-family:PS;font-size:30px;color:rgba(20,24,28,0.55);">Edited by MrCopper804</div></div>')
show("#end", E, T + 1); j.append(f'tl.fromTo("#end",{{opacity:0}},{{opacity:1,duration:0.4}},{E});tl.fromTo("#ph",{{scale:0.8,opacity:0}},{{scale:1,opacity:1,duration:0.4,ease:"back.out(2)"}},{E + 0.3});')
# audio
A = f"{P}/assets/audio"; PV = "/home/user/tools/perc-venv/bin/python"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", VO, "-af", f"aresample=48000,aformat=channel_layouts=stereo,adelay={int(O*1000)}|{int(O*1000)},apad", "-t", str(T), f"{A}/vo.wav"], check=True)
subprocess.run([PV, f"{REPO}/library/tools/music_fit.py", MUS, f"{A}/music.wav", "--length", str(T), "--end", "fade", "--fade", "2"], check=True, capture_output=True)
subprocess.run([PV, f"{REPO}/library/tools/mix_vo_music.py", f"{A}/vo.wav", f"{A}/music.wav", f"{A}/mix.wav", "--lufs", "-16"], check=True, capture_output=True)
open(f"{P}/index.html", "w").write(f'''<!doctype html><html lang="en" data-resolution="portrait"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080, height=1920">
<script src="assets/vendor/gsap-3.14.2.min.js"></script><style>@font-face{{font-family:"PS";src:url("assets/fonts/Poppins-SemiBold.ttf");}}@font-face{{font-family:"AN";src:url("assets/fonts/Anton-Regular.ttf");}}
*{{margin:0;padding:0;box-sizing:border-box;}}html,body{{width:1080px;height:1920px;overflow:hidden;background:#fff;}}</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{T}" data-width="1080" data-height="1920" style="position:absolute;inset:0;overflow:hidden;background:#fff;">
{chr(10).join(b)}
<audio id="mix" src="assets/audio/mix.wav" data-start="0" data-duration="{T}" data-volume="1.0" data-track-index="10"></audio>
</div><script>const tl=gsap.timeline({{paused:true}});
{chr(10).join(j)}
tl.to({{}},{{duration:{T}}},0);window.__timelines=window.__timelines||{{}};window.__timelines["main"]=tl;</script></body></html>''')
print("built", T)
