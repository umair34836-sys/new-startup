#!/usr/bin/env python3
"""Shangla UPVC ad pair (2026-11-23), one look (dark, brand green, Anton, same end card):
  cool  - 17.1 s "Cooler Edit" structure (TikTok @ubaid.4d 7699154533766712594): dark intro + white caption bar,
          push-in, EXPLODED UPVC WINDOW (frame, sash, 2 glass panes, gasket, handle) that snaps back on the beat,
          one shot per beat with white bands / letterbox / red flicker, glitch end card. Audio = the reference's own sound
          (owner's choice, scratchpad only, never in git).
  vo    - ~20.5 s hook ad on an ElevenLabs Viraj VO, kinetic words on the VO's word times, same exploded window as hook.
python3 build_shangla_ads2.py MODE PROJECT CLIPDIR AUDIO
Footage: only human-free shots of Shangla's own videos + Mixkit videoFree 3977/3978 (licence read per page 2026-11-23).
"""
import os, shutil, subprocess, sys
MODE, P, CL, AUD = sys.argv[1:5]
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
os.makedirs(f"{P}/assets/clips", exist_ok=True); os.makedirs(f"{P}/assets/vendor", exist_ok=True); os.makedirs(f"{P}/assets/fonts", exist_ok=True); os.makedirs(f"{P}/assets/audio", exist_ok=True)
for f in os.listdir(CL): shutil.copy(f"{CL}/{f}", f"{P}/assets/clips/{f}")
shutil.copy(f"{REPO}/library/vendor/gsap-3.14.2.min.js", f"{P}/assets/vendor/")
for f in ("Anton-Regular.ttf", "Poppins-SemiBold.ttf"): shutil.copy(f"{REPO}/library/fonts/{f}", f"{P}/assets/fonts/")
for f in ("hyperframes.json", "meta.json", "package.json"): shutil.copy(f"{REPO}/video/{f}", P)
G, K, W, RED = "#5bbf2a", "#07080a", "#ffffff", "#e0161f"
b, j = [], []
r2 = lambda x: round(x, 2)
DUR = {"slide": 2.87, "xsec": 5.6, "close": 4.5, "prof1": 4.07, "prof2": 4.5, "prof3": 4.2, "room": 2.6, "win1": 2.6, "mx3977": 11.0, "mx3978": 11.0}
def show(s, t0, t1, total):
    j.append(f'gsap.set("{s}",{{visibility:"hidden"}});tl.set("{s}",{{visibility:"visible"}},{r2(t0)});')
    if t1 < total: j.append(f'tl.set("{s}",{{visibility:"hidden"}},{r2(t1)});')
n = [0]
def shot(clip, t0, t1, total, z0=1.0, z1=1.08, x=0, rot=0, look="", src0=0.0):
    n[0] += 1; i = f"sh{n[0]}"; d = r2(t1 - t0)
    filt = "filter:blur(14px) brightness(0.45);" if look == "bed" else ("filter:brightness(0.55) saturate(0.7);" if look == "dark" else "")
    b.append(f'<div id="{i}" style="position:absolute;inset:0;overflow:hidden;"><div id="{i}z" style="position:absolute;inset:-4%;{filt}">'
             f'<video id="{i}v" src="assets/clips/{clip}.mp4" data-start="{r2(t0)}" data-duration="{d}" data-media-start="{src0}" muted playsinline style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;"></video></div>')
    if look == "bands": b.append(f'<div style="position:absolute;left:0;right:0;top:0;height:420px;background:{W};"></div><div style="position:absolute;left:0;right:0;bottom:0;height:420px;background:{W};"></div>')
    if look == "box": b.append(f'<div style="position:absolute;left:0;right:0;top:0;height:300px;background:#000;"></div><div style="position:absolute;left:0;right:0;bottom:0;height:300px;background:#000;"></div>')
    b.append('</div>')
    show(f"#{i}", t0, t1, total); j.append(f'tl.fromTo("#{i}z",{{scale:{z0},x:{x},rotation:{rot}}},{{scale:{z1},x:{-x},rotation:0,duration:{d},ease:"none"}},{r2(t0)});')
    return i
def exploded(i, t0, t1, total, snap, top=560):
    # a UPVC window drawn in HTML: outer frame, sash, gasket, two glass panes (double glazing), handle
    parts = [("fr", f"left:0;top:0;width:560px;height:760px;border:34px solid #f2f2ef;border-radius:6px;box-shadow:0 30px 80px rgba(0,0,0,0.6);", -330, -260, -14),
             ("sa", "left:46px;top:46px;width:468px;height:668px;border:26px solid #e4e4df;border-radius:4px;", 300, -220, 10),
             ("gk", "left:72px;top:72px;width:416px;height:616px;border:6px solid #1b1d20;", -300, 280, -8),
             ("g1", "left:78px;top:78px;width:404px;height:604px;background:linear-gradient(135deg,rgba(170,215,240,0.55),rgba(120,170,205,0.25));", 340, 120, 12),
             ("g2", "left:92px;top:92px;width:376px;height:576px;background:linear-gradient(135deg,rgba(190,230,250,0.35),rgba(140,190,220,0.15));border:2px solid rgba(255,255,255,0.35);", -260, 40, 6),
             ("hd", "left:478px;top:330px;width:26px;height:110px;border-radius:13px;background:#dcdcd8;box-shadow:0 4px 10px rgba(0,0,0,0.5);", 260, 330, 40)]
    h = "".join(f'<div id="{i}{k}" style="position:absolute;{css}"></div>' for k, css, *_ in parts)
    b.append(f'<div id="{i}" style="position:absolute;left:260px;top:{top}px;width:560px;height:760px;">{h}</div>'); show(f"#{i}", t0, t1, total)
    for k, _, dx, dy, rt in parts:
        j.append(f'tl.fromTo("#{i}{k}",{{x:0,y:0,rotation:0}},{{x:{dx},y:{dy},rotation:{rt},duration:0.32,ease:"power3.out"}},{r2(t0 + 0.02)});')
        j.append(f'tl.to("#{i}{k}",{{x:{dx * 1.08:.0f},y:{dy * 1.08:.0f},rotation:{rt * 1.2:.1f},duration:{r2(snap - t0 - 0.4)},ease:"none"}},{r2(t0 + 0.34)});')
        j.append(f'tl.to("#{i}{k}",{{x:0,y:0,rotation:0,duration:0.2,ease:"power4.in"}},{r2(snap)});')
    j.append(f'tl.fromTo("#{i}",{{scale:1.06}},{{scale:1,duration:0.25,ease:"power2.out"}},{r2(snap + 0.2)});')
def word(i, html, t0, t1, total, css, fx="slam"):
    b.append(f'<div id="{i}" style="position:absolute;white-space:nowrap;line-height:1;{css}">{html}</div>'); show(f"#{i}", t0, t1, total)
    a = {"slam": ('{scale:2.4,opacity:0}', '{scale:1,opacity:1,duration:0.28,ease:"power4.out"}'),
         "up": ('{y:90,opacity:0}', '{y:0,opacity:1,duration:0.32,ease:"power3.out"}'),
         "stamp": ('{scale:0.3,rotation:-12,opacity:0}', '{scale:1,rotation:-5,opacity:1,duration:0.3,ease:"back.out(3)"}')}[fx]
    j.append(f'tl.fromTo("#{i}",{a[0]},{a[1]},{r2(t0)});')
SH = "text-shadow:0 6px 26px rgba(0,0,0,0.7);"
def endcard(t0, total, glitch=False):
    b.append(f'<div id="end" style="position:absolute;inset:0;background:{K};">'
             f'<div id="e1" style="position:absolute;left:0;right:0;top:700px;text-align:center;font-family:AN;font-size:170px;color:{W};text-shadow:0 0 30px rgba(91,191,42,0.75),0 0 60px rgba(91,191,42,0.4);">SHANGLA</div>'
             f'<div id="e2" style="position:absolute;left:0;right:0;top:890px;text-align:center;font-family:PS;font-size:52px;color:{G};">UPVC Windows &amp; Doors</div>'
             f'<div id="e3" style="position:absolute;left:120px;right:120px;top:1030px;padding:22px 0;border-radius:24px;background:{G};text-align:center;font-family:AN;font-size:96px;color:{K};">0313-512-0718</div>'
             f'<div id="e4" style="position:absolute;left:0;right:0;top:1250px;text-align:center;font-family:PS;font-size:34px;color:rgba(255,255,255,0.6);">Edited by MrCopper804</div></div>')
    show("#end", t0, total + 1, total)
    if glitch:
        j.append(f'tl.fromTo("#e1",{{opacity:0,skewX:40,x:-80}},{{opacity:1,skewX:0,x:0,duration:0.35,ease:"steps(6)"}},{r2(t0 + 0.05)});')
        j.append(f'tl.to("#e1",{{x:8,skewX:-8,duration:0.06,yoyo:true,repeat:4,ease:"steps(1)"}},{r2(t0 + 0.6)});')
    else:
        j.append(f'tl.fromTo("#e1",{{opacity:0,scale:1.6}},{{opacity:1,scale:1,duration:0.4,ease:"power4.out"}},{r2(t0 + 0.05)});')
    j.append(f'tl.fromTo("#e2",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.3}},{r2(t0 + 0.3)});')
    j.append(f'tl.fromTo("#e3",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2)"}},{r2(t0 + 0.5)});')
    j.append(f'tl.fromTo("#e4",{{opacity:0}},{{opacity:1,duration:0.3}},{r2(t0 + 0.8)});')

if MODE == "cool":
    T = 17.1
    CUTS = [5.2, 5.93, 6.57, 7.27, 7.83, 8.43, 9.73, 10.33, 11.07, 11.7, 12.4, 12.97, 13.67, 14.2, 14.87, 15.47]
    shot("mx3978", 0, 1.37, T, 1.15, 1.0, look="dark")
    b.append(f'<div id="cap" style="position:absolute;left:0;right:0;top:0;height:250px;background:{W};"><div style="position:absolute;left:30px;right:30px;top:62px;text-align:center;font-family:AN;font-size:68px;line-height:1.05;color:{K};">EDITING RANDOM THINGS:<br>UPVC WINDOW</div></div>')
    show("#cap", 0, 2.97, T)
    shot("room", 1.37, 2.97, T, 1.0, 1.7)
    j.append('tl.fromTo("#sh2z",{filter:"blur(0px)"},{filter:"blur(10px)",duration:0.25},2.72);')
    shot("xsec", 2.97, 5.2, T, 1.1, 1.0, look="bed")
    exploded("ex", 2.97, 5.2, T, snap=4.75)
    SEQ = [("xsec", 2.4, "", 1.25), ("prof1", 0.3, "bands", 1.4), ("slide", 0.6, "", 1.2), ("EX", 0, "", 1), ("close", 1.0, "box", 1.5),
           ("prof2", 1.2, "", 1.3), ("room", 1.0, "bands", 1.25), ("xsec", 0.3, "", 1.6), ("room", 0.6, "box", 1.35), ("prof3", 0.5, "", 1.25),
           ("EX", 0, "", 1), ("close", 2.5, "bands", 1.3), ("slide", 1.4, "", 1.5), ("prof1", 2.0, "box", 1.2), ("xsec", 4.0, "", 1.3)]
    for k, (c, s0, look, z) in enumerate(SEQ):
        t0, t1 = CUTS[k], CUTS[k + 1]
        if c == "EX":
            shot("xsec", t0, t1, T, 1.0, 1.0, look="bed", src0=1.0); exploded(f"ex{k}", t0, t1, T, snap=t1 - 0.25, top=600)
        else:
            shot(c, t0, t1, T, z, 1.0 if k % 2 else z + 0.12, x=(40 if k % 3 == 0 else 0), rot=(4 if k % 4 == 1 else 0), look=look, src0=s0)
        b.append(f'<div id="rf{k}" style="position:absolute;inset:0;background:radial-gradient(circle at 50% 80%, rgba(224,22,31,0.55), rgba(224,22,31,0) 60%);mix-blend-mode:screen;"></div>')
        show(f"#rf{k}", t0, t0 + 0.18, T); j.append(f'tl.fromTo("#rf{k}",{{opacity:1}},{{opacity:0,duration:0.18}},{t0});')
    b.append(f'<div id="gl" style="position:absolute;left:0;right:0;top:1560px;text-align:center;font-family:AN;font-size:64px;color:{W};text-shadow:0 0 18px {G},0 0 40px {G};">SHANGLA</div>'); show("#gl", 5.2, 15.47, T)
    word("f1", "SINGLE &amp; DOUBLE GLAZED", 9.73, 10.33, T, f"left:60px;right:60px;top:300px;text-align:center;font-family:AN;font-size:96px;color:{W};{SH}")
    word("f2", "UPVC WINDOWS &amp; DOORS", 12.97, 13.67, T, f"left:60px;right:60px;top:300px;text-align:center;font-family:AN;font-size:96px;color:{G};{SH}")
    endcard(15.47, T, glitch=True)
    shutil.copy(AUD, f"{P}/assets/audio/mix.wav")
else:
    VO = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", AUD], capture_output=True, text=True).stdout)
    O = 0.3; T = round(VO + O + 2.4, 2)
    t = lambda x: r2(x + O)
    shot("mx3978", 0, t(2.46), T, 1.15, 1.0, look="dark")
    word("h1", "SARDI ANDAR?", t(0.0), t(2.46), T, f"left:70px;top:720px;font-family:AN;font-size:150px;color:{W};{SH}")
    word("h2", "SUKOON BAHAR?", t(0.98), t(2.46), T, f"left:70px;top:890px;font-family:AN;font-size:150px;color:{W};{SH}", "up")
    shot("xsec", t(2.46), t(3.6), T, 1.0, 1.0, look="bed"); exploded("ex", t(2.46), t(3.6), T, snap=t(3.3), top=520)
    word("h3", "BILKUL NAHI.", t(2.46), t(3.6), T, f"left:90px;top:1380px;padding:8px 26px;background:{G};font-family:AN;font-size:120px;color:{K};", "stamp")
    shot("slide", t(3.6), t(5.8), T, 1.15, 1.0)
    word("w1", "SHANGLA UPVC", t(3.6), t(5.8), T, f"left:70px;top:1260px;font-family:AN;font-size:150px;color:{W};{SH}")
    word("w2", "Windows &amp; Doors", t(4.76), t(5.8), T, f"left:76px;top:1430px;font-family:PS;font-size:62px;padding:4px 18px;background:{K};color:{G};", "up")
    shot("xsec", t(5.8), t(7.6), T, 1.0, 1.1, src0=0.5)
    word("w3", "SINGLE", t(5.8), t(7.6), T, f"left:70px;top:330px;font-family:AN;font-size:170px;color:{K};")
    word("w4", "DOUBLE GLAZED", t(6.62), t(7.6), T, f"left:70px;top:510px;font-family:AN;font-size:130px;color:{G};")
    shot("prof2", t(7.6), t(8.9), T, 1.0, 1.1, look="box"); shot("close", t(8.9), t(10.2), T, 1.2, 1.0, look="bands", src0=1.0)
    word("w5", "MAZBOOT PROFILE", t(7.62), t(8.9), T, f"left:60px;right:60px;top:1280px;text-align:center;font-family:AN;font-size:120px;color:{W};{SH}")
    word("w6", "BEHTAREEN FINISHING", t(8.9), t(10.2), T, f"left:40px;right:40px;top:1530px;text-align:center;font-family:AN;font-size:100px;color:{K};")
    shot("close", t(10.2), t(11.9), T, 1.15, 1.25, src0=2.5); shot("room", t(11.9), t(13.5), T, 1.1, 1.0)
    for k, (txt, at) in enumerate([("THANDI HAWA", 10.22), ("SHOR", 11.62), ("GARD", 12.22)]):
        word(f"x{k}", txt, t(at), t(13.5), T, f"left:70px;top:{360 + k * 170}px;font-family:AN;font-size:140px;color:{W};{SH}", "up")
        b.append(f'<div id="xs{k}" style="position:absolute;left:60px;top:{430 + k * 170}px;width:{[760, 360, 380][k]}px;height:16px;background:{RED};transform-origin:0 50%;transform:rotate(-3deg);"></div>')
        show(f"#xs{k}", t(at + 0.5), t(13.5), T); j.append(f'tl.fromTo("#xs{k}",{{scaleX:0}},{{scaleX:1,duration:0.2}},{t(at + 0.5)});')
    word("x3", "SAB BAHAR.", t(12.74), t(13.5), T, f"left:70px;top:900px;padding:8px 26px;background:{G};font-family:AN;font-size:120px;color:{K};", "stamp")
    shot("prof3", t(13.5), t(15.3), T, 1.0, 1.1)
    word("w7", "NAYA GHAR?", t(14.16), t(15.3), T, f"left:70px;top:1240px;font-family:AN;font-size:140px;color:{W};{SH}")
    word("w8", "PURANA GHAR?", t(14.94), t(15.3), T, f"left:70px;top:1400px;font-family:AN;font-size:140px;color:{G};{SH}", "up")
    shot("slide", t(15.3), t(16.9), T, 1.0, 1.15, src0=1.2)
    word("w9", "SHANGLA UPVC", t(15.34), t(16.9), T, f"left:60px;right:60px;top:860px;text-align:center;font-family:AN;font-size:170px;color:{W};{SH}")
    endcard(t(16.9), T)
    word("w10", "ABHI CALL KAREIN", t(16.92), T, T, f"left:0;right:0;top:1380px;text-align:center;font-family:AN;font-size:96px;color:{W};", "up")
    PV = "/home/user/tools/perc-venv/bin/python"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", AUD, "-af", f"aresample=48000,aformat=channel_layouts=stereo,adelay={int(O * 1000)}|{int(O * 1000)},apad=pad_dur=2.6", "-t", str(T), f"{P}/assets/audio/vo_placed.wav"], check=True)
    subprocess.run([PV, f"{REPO}/library/tools/music_fit.py", f"{REPO}/library/music/cc0/upbeat-electronic--holiznacc0--pantheon.mp3", f"{P}/assets/audio/music.wav", "--length", str(T), "--end", "fade", "--fade", "1.5"], check=True, capture_output=True)
    subprocess.run([PV, f"{REPO}/library/tools/mix_vo_music.py", f"{P}/assets/audio/vo_placed.wav", f"{P}/assets/audio/music.wav", f"{P}/assets/audio/mix.wav", "--lufs", "-16"], check=True, capture_output=True)
# film grain + vignette over everything
b.append('<div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 50%, rgba(0,0,0,0) 45%, rgba(0,0,0,0.55) 100%);pointer-events:none;"></div>')
open(f"{P}/index.html", "w").write(f'''<!doctype html><html lang="en" data-resolution="portrait"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080, height=1920">
<script src="assets/vendor/gsap-3.14.2.min.js"></script><style>
@font-face{{font-family:"AN";src:url("assets/fonts/Anton-Regular.ttf");}}@font-face{{font-family:"PS";src:url("assets/fonts/Poppins-SemiBold.ttf");}}
*{{margin:0;padding:0;box-sizing:border-box;}}html,body{{width:1080px;height:1920px;overflow:hidden;background:{K};}}
</style></head><body><div id="root" data-composition-id="main" data-start="0" data-duration="{T}" data-width="1080" data-height="1920" style="position:absolute;inset:0;overflow:hidden;background:{K};">
{chr(10).join(b)}
<audio id="mix" src="assets/audio/mix.wav" data-start="0" data-duration="{T}" data-volume="1.0" data-track-index="10"></audio>
</div><script>const tl=gsap.timeline({{paused:true}});
{chr(10).join(j)}
tl.to({{}},{{duration:{T}}},0);window.__timelines=window.__timelines||{{}};window.__timelines["main"]=tl;</script></body></html>''')
print("built", MODE, T)
