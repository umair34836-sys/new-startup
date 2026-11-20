#!/usr/bin/env python3
"""Shangla UPVC reel v2 (2026-11-20): kinetic typography synced to the VO's word times + a different transition at
every scene change + overlays (grain, light leak, brand bars). Same assets as build_shangla.py.
python3 build_shangla_v2.py PROJECT
Word times W come from Whisper small word_timestamps on the VO (+0.3 s placement).
"""
import os, subprocess, sys
os.chdir(sys.argv[1])
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
PV, TL = "/home/user/tools/perc-venv/bin/python", f"{REPO}/library/tools"
TOTAL = 36.6
G, P, W_, K = "#5bbf2a", "#3d2b8f", "#ffffff", "#0d0b14"
S = [0, 2.74, 7.58, 15.44, 19.6, 23.3, 29.4, TOTAL]  # scene starts
r2 = lambda x: round(x, 2)
body, js, aud = [], [], []
def tw(sel, fr, to, at): js.append(f'tl.fromTo("{sel}", {fr}, {to}, {r2(at)});')
def to(sel, v, at): js.append(f'tl.to("{sel}", {v}, {r2(at)});')
def show(sel, t0, t1):
    js.append(f'gsap.set("{sel}", {{visibility:"hidden"}});'); js.append(f'tl.set("{sel}", {{visibility:"visible"}}, {r2(t0)});')
    if t1 < TOTAL: js.append(f'tl.set("{sel}", {{visibility:"hidden"}}, {r2(t1)});')
def sfx(n, at, d, v=0.3): aud.append(f'<audio id="fx{len(aud)}" src="assets/sfx/{n}.mp3" data-start="{r2(at)}" data-duration="{d}" data-volume="{v}" data-track-index="{11 + len(aud) % 3}"></audio>')
def clip(i, name, t0, t1, box="inset:0;", z0=1.0, z1=1.08, origin="50% 50%"):
    d = r2(t1 - t0)
    body.append(f'<div id="{i}" style="position:absolute;{box}overflow:hidden;"><div id="{i}z" style="position:absolute;inset:0;transform-origin:{origin};">'
                f'<video id="{i}v" src="assets/clips/{name}.mp4" data-start="{r2(t0)}" data-duration="{d}" muted playsinline style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;"></video></div></div>')
    show(f"#{i}", t0, t1); tw(f"#{i}z", f"{{scale:{z0}}}", f'{{scale:{z1}, duration:{d}, ease:"none"}}', t0)
FX = {"slam": ('{scale:2.6, opacity:0}', '{scale:1, opacity:1, duration:0.32, ease:"power4.out"}'),
      "up": ('{y:120, opacity:0}', '{y:0, opacity:1, duration:0.4, ease:"power3.out"}'),
      "drop": ('{y:-160, opacity:0, rotation:-8}', '{y:0, opacity:1, rotation:0, duration:0.45, ease:"bounce.out"}'),
      "left": ('{x:-260, opacity:0}', '{x:0, opacity:1, duration:0.4, ease:"power4.out"}'),
      "right": ('{x:260, opacity:0}', '{x:0, opacity:1, duration:0.4, ease:"power4.out"}'),
      "blur": ('{scale:1.25, opacity:0, filter:"blur(18px)"}', '{scale:1, opacity:1, filter:"blur(0px)", duration:0.4, ease:"power2.out"}'),
      "stamp": ('{scale:0.3, rotation:-14, opacity:0}', '{scale:1, rotation:-6, opacity:1, duration:0.35, ease:"back.out(3)"}')}
def word(i, text, at, t1, css, fx="slam", sound=None):
    body.append(f'<div id="{i}" class="kw" style="position:absolute;{css}">{text}</div>'); show(f"#{i}", at, t1)
    a, b = FX[fx]; tw(f"#{i}", a, b, at)
    if sound: sfx(sound, at, 0.3, 0.22)
SHADOW = "text-shadow:0 6px 24px rgba(0,0,0,0.55);"
VEIL = '<div style="position:absolute;left:0;right:0;bottom:0;height:1000px;background:linear-gradient(180deg, rgba(13,11,20,0) 0%, rgba(13,11,20,0.82) 100%);"></div>'

# ---------- S1 hook 0-2.74: real install, words slam on the beat of the VO
clip("c1", "install1", 0, 3.0, z0=1.0, z1=1.15, origin="60% 40%")
body.append(f'<div id="v1" style="position:absolute;inset:0;">{VEIL}</div>'); show("#v1", 0, 3.0)
word("w1a", "GHAR KI", 0.30, 3.0, f"left:70px;top:1180px;font-family:AN;font-size:150px;color:{W_};{SHADOW}", "left")
word("w1b", "KHIDKI", 0.98, 3.0, f"left:70px;top:1340px;font-family:AN;font-size:230px;color:{G};{SHADOW}", "slam", "whoosh-fast-0.3s")
word("w1c", "sirf sheesha", 1.42, 3.0, f"left:76px;top:1600px;font-family:PS;font-size:70px;color:{W_};{SHADOW}", "up")
word("w1d", "NAHI HOTI", 2.24, 3.0, f"left:560px;top:1580px;padding:6px 26px;background:{G};font-family:AN;font-size:96px;color:{K};", "stamp", "pop-high")
# transition 1: three brand bars sweep across (covers the cut at 2.74)
for k, c in enumerate([G, P, W_]):
    body.append(f'<div id="b1{k}" style="position:absolute;left:-200px;top:{-300 + k * 0}px;width:1500px;height:2600px;background:{c};transform:rotate(18deg);"></div>')
    show(f"#b1{k}", 2.45, 3.25); tw(f"#b1{k}", "{x:-1700}", f'{{x:1900, duration:0.75, ease:"power3.inOut"}}', 2.45 + k * 0.07)
sfx("swish-4", 2.45, 0.4, 0.3)

# ---------- S2 brand 2.74-7.58: faint product animation behind, giant outline type, logo pop, words
clip("c2", "prod1", 2.74, 4.94, z0=1.2, z1=1.0)
body.append(f'<div id="s2" style="position:absolute;inset:0;background:rgba(244,245,242,0.86);">'
            f'<div id="s2o" style="position:absolute;left:0;top:300px;white-space:nowrap;font-family:AN;font-size:420px;color:rgba(61,43,143,0.07);">SHANGLA SHANGLA</div>'
            f'<div id="s2p" style="position:absolute;left:0;top:1280px;white-space:nowrap;font-family:AN;font-size:420px;color:rgba(91,191,42,0.12);">UPVC UPVC UPVC</div>'
            f'<img id="s2l" src="assets/img/logo.png" alt="Shangla UPVC logo" data-start="{S[1]}" data-duration="{r2(S[2] - S[1])}" style="position:absolute;left:90px;top:640px;width:900px;height:460px;object-fit:contain;border-radius:36px;box-shadow:0 30px 80px rgba(61,43,143,0.25);"></div>')
show("#s2", S[1], S[2]); tw("#s2o", "{x:0}", f'{{x:-900, duration:{r2(S[2] - S[1])}, ease:"none"}}', S[1]); tw("#s2p", "{x:-900}", f'{{x:0, duration:{r2(S[2] - S[1])}, ease:"none"}}', S[1])
tw("#s2l", "{scale:0.4, rotation:-10, opacity:0}", '{scale:1, rotation:0, opacity:1, duration:0.6, ease:"back.out(1.8)"}', 2.85); sfx("impact-punch", 2.85, 0.6, 0.3)
word("w2a", "WINDOWS", 4.70, S[2], f"left:90px;top:1170px;font-family:AN;font-size:170px;color:{P};", "left", "whoosh-fast-0.3s")
word("w2b", "&amp; DOORS", 6.80, S[2], f"left:90px;top:1360px;font-family:AN;font-size:170px;color:{G};", "right", "swish-1")
# transition 2: zoom-through (scene scales up and blurs out, light leak)
tw("#s2", "{scale:1, filter:\"blur(0px)\"}", '{scale:2.2, filter:"blur(14px)", duration:0.4, ease:"power2.in"}', S[2] - 0.35)

# ---------- S3 product 7.58-15.44: split screen of the real workshop, kinetic spec words
clip("c3a", "prof1", S[2], 10.98, box="left:0;top:0;width:1080px;height:960px;", z0=1.1, z1=1.0)
clip("c3b", "prof2", 7.9, 12.4, box="left:0;top:960px;width:1080px;height:960px;", z0=1.0, z1=1.1)
tw("#c3a", "{x:-1080}", '{x:0, duration:0.5, ease:"power4.out"}', S[2]); tw("#c3b", "{x:1080}", '{x:0, duration:0.5, ease:"power4.out"}', 7.9)
body.append(f'<div id="s3bar" style="position:absolute;left:0;top:930px;width:1080px;height:60px;background:{G};transform-origin:0 50%;"></div>'); show("#s3bar", 7.9, 11.0)
tw("#s3bar", "{scaleX:0}", '{scaleX:1, duration:0.5, ease:"power3.out"}', 8.0)
word("w3a", "IMPORTED", 7.58, 11.0, f"left:60px;top:740px;font-family:AN;font-size:170px;color:{W_};{SHADOW}", "slam", "whoosh-fast-0.3s")
word("w3b", "uPVC PROFILE", 8.88, 11.0, f"left:60px;top:1010px;padding:4px 22px;background:{P};font-family:AN;font-size:120px;color:{W_};", "left")
clip("c3c", "prod3", 11.0, 14.5, z0=1.0, z1=1.12)
body.append(f'<div id="v3" style="position:absolute;inset:0;">{VEIL}</div>'); show("#v3", 11.0, 15.44)
# iris reveal into the product shot
js.append('gsap.set("#c3c", {clipPath:"circle(0% at 50% 50%)"});'); tw("#c3c", '{clipPath:"circle(0% at 50% 50%)"}', '{clipPath:"circle(75% at 50% 50%)", duration:0.5, ease:"power3.out"}', 11.0)
word("w3c", "SINGLE", 11.20, 14.45, f"left:70px;top:1000px;font-family:AN;font-size:190px;color:{W_};{SHADOW}", "drop", "pop-low")
word("w3d", "DOUBLE", 12.92, 14.45, f"left:70px;top:1200px;font-family:AN;font-size:190px;color:{G};{SHADOW}", "drop", "pop-high")
word("w3e", "glazed", 13.22, 14.45, f"left:620px;top:1280px;font-family:PS;font-size:90px;color:{W_};{SHADOW}", "up")
clip("c3d", "install3", 14.4, 15.44, z0=1.08, z1=1.0)
tw("#c3d", '{clipPath:"inset(0% 0% 100% 0%)"}', '{clipPath:"inset(0% 0% 0% 0%)", duration:0.4, ease:"power3.inOut"}', 14.4)
js.append('gsap.set("#c3d", {clipPath:"inset(0% 0% 100% 0%)"});')
word("w3f", "KHIDKIYAN", 14.45, 15.44, f"left:70px;top:380px;font-family:AN;font-size:160px;color:{W_};{SHADOW}", "blur")
word("w3g", "&amp; DARWAZE", 14.84, 15.44, f"left:70px;top:560px;font-family:AN;font-size:160px;color:{G};{SHADOW}", "blur")
# move w3c..w3e above install3 by z-order: re-show them is enough since they come later in DOM? keep words after clips
# ---------- S4 15.44-19.6: fabrication -> installation, line draws between
clip("c4a", "prof3", S[3], 17.4, z0=1.0, z1=1.1)
clip("c4b", "install2", 17.2, S[4] + 0.2, z0=1.1, z1=1.0, origin="60% 40%")
tw("#c4b", "{x:1080}", '{x:0, duration:0.45, ease:"power4.inOut"}', 17.2); tw("#c4a", "{x:0}", '{x:-540, duration:0.45, ease:"power4.inOut"}', 17.2)
body.append(f'<div id="v4" style="position:absolute;inset:0;">{VEIL}</div>'); show("#v4", S[3], S[4])
word("w4a", "FABRICATION", 15.44, 17.3, f"left:60px;top:1300px;font-family:AN;font-size:160px;color:{W_};{SHADOW}", "left", "whoosh-fast-0.3s")
body.append(f'<div id="w4l" style="position:absolute;left:70px;top:1500px;width:940px;height:10px;background:{G};transform-origin:0 50%;"></div>'); show("#w4l", 16.4, S[4])
tw("#w4l", "{scaleX:0}", '{scaleX:1, duration:0.9, ease:"power2.inOut"}', 16.4)
word("w4b", "INSTALLATION", 16.84, S[4], f"left:60px;top:1540px;font-family:AN;font-size:160px;color:{G};{SHADOW}", "right", "swish-1")
word("w4c", "sab hum karte hain", 17.96, S[4], f"left:66px;top:1740px;font-family:PS;font-size:64px;color:{W_};{SHADOW}", "up")
# transition 4: white flash + shake
body.append('<div id="fl4" style="position:absolute;inset:0;background:#fff;"></div>'); show("#fl4", S[4] - 0.05, S[4] + 0.3)
tw("#fl4", "{opacity:1}", '{opacity:0, duration:0.3, ease:"power2.out"}', S[4] - 0.05); sfx("impact-punch", S[4], 0.6, 0.28)

# ---------- S5 19.6-23.3: three full-frame word cards on the beat, product animation between
clip("c5", "prod2", S[4], S[5] + 0.3, z0=1.0, z1=1.1)
for k, (txt, at, t1, bg, fg) in enumerate([("MAZBOOT", 19.72, 20.65, P, W_), ("KHOOB<br>SURAT", 20.70, 21.55, G, K)]):
    body.append(f'<div id="c5{k}" style="position:absolute;inset:0;background:{bg};"><div style="position:absolute;left:60px;top:700px;font-family:AN;font-size:300px;line-height:0.95;color:{fg};">{txt}</div></div>')
    show(f"#c5{k}", at, t1); tw(f"#c5{k}", '{clipPath:"inset(0% 100% 0% 0%)"}', '{clipPath:"inset(0% 0% 0% 0%)", duration:0.22, ease:"power3.out"}', at); sfx("pop-high" if k else "pop-low", at, 0.2, 0.25)
word("w5a", "SHOR", 22.44, S[5], f"left:70px;top:620px;font-family:AN;font-size:260px;color:{P};", "slam", "whoosh-fast-0.3s")
word("w5b", "BAHAR.", 22.86, S[5], f"left:70px;top:870px;font-family:AN;font-size:260px;color:#2e7d1a;", "slam")
# transition 5: vertical shutters close and open
for k in range(6):
    body.append(f'<div id="sh{k}" style="position:absolute;left:{k * 180}px;top:0;width:181px;height:1920px;background:{P};transform-origin:50% 0;"></div>')
    show(f"#sh{k}", S[5] - 0.3, S[5] + 0.35)
    tw(f"#sh{k}", "{scaleY:0}", '{scaleY:1, duration:0.25, ease:"power2.in"}', S[5] - 0.3 + k * 0.02)
    to(f"#sh{k}", '{scaleY:0, transformOrigin:"50% 100%", duration:0.25, ease:"power2.out"}', S[5] + 0.05 + k * 0.02)
sfx("swish-4", S[5] - 0.3, 0.4, 0.28)

# ---------- S6 23.3-29.4: real projects as tilted cards, marquee strip, typed labels
body.append(f'<div id="s6" style="position:absolute;inset:0;background:{K};">'
            f'<div id="mq" style="position:absolute;left:0;top:60px;white-space:nowrap;font-family:AN;font-size:120px;color:{G};">PROJECT DELIVERED &nbsp;•&nbsp; PROJECT DELIVERED &nbsp;•&nbsp; PROJECT DELIVERED</div>'
            f'<div id="mq2" style="position:absolute;left:0;top:1740px;white-space:nowrap;font-family:AN;font-size:120px;color:rgba(91,191,42,0.75);">RAWALPINDI &nbsp;•&nbsp; ISLAMABAD &nbsp;•&nbsp; RAWALPINDI &nbsp;•&nbsp; ISLAMABAD</div></div>')
show("#s6", S[5], S[6]); tw("#mq", "{x:0}", f'{{x:-1400, duration:{r2(S[6] - S[5])}, ease:"none"}}', S[5]); tw("#mq2", "{x:-1400}", f'{{x:0, duration:{r2(S[6] - S[5])}, ease:"none"}}', S[5])
for k, (img, lab, top, rot, at) in enumerate([("dha.jpg", "DHA Overseas Tower", 260, -4, 23.34), ("farm.jpg", "Farmhouse, Islamabad", 930, 3, 25.96)]):
    body.append(f'<div id="pc{k}" style="position:absolute;left:100px;top:{top}px;width:880px;padding:22px 22px 30px;background:#fff;border-radius:18px;box-shadow:0 30px 80px rgba(0,0,0,0.6);">'
                f'<img id="pci{k}" src="assets/img/{img}" alt="{lab} project" data-start="{at}" data-duration="{r2(S[6] - at)}" style="display:block;width:836px;height:470px;object-fit:cover;border-radius:10px;">'
                f'<div id="pct{k}" style="margin-top:18px;font-family:AN;font-size:78px;color:{P};">{lab}</div></div>')
    show(f"#pc{k}", at, S[6]); tw(f"#pc{k}", f"{{y:900, rotation:{rot * 4}, opacity:0}}", f'{{y:0, rotation:{rot}, opacity:1, duration:0.6, ease:"power3.out"}}', at)
    tw(f"#pct{k}", '{clipPath:"inset(0% 100% 0% 0%)"}', '{clipPath:"inset(0% 0% 0% 0%)", duration:0.7, ease:"steps(14)"}', at + 0.5)
    js.append(f'gsap.set("#pct{k}", {{clipPath:"inset(0% 100% 0% 0%)"}});'); sfx("swish-1", at, 0.35, 0.25)
word("w6", "DELIVERED ✓", 28.94, S[6], f"left:520px;top:1540px;padding:8px 26px;background:{G};font-family:AN;font-size:90px;color:{K};", "stamp", "confirm-1")

# ---------- S7 29.4-end: iris into the end card, digits drop one by one
body.append(f'<div id="e" style="position:absolute;inset:0;background:#f4f5f2;">'
            f'<img id="ei" src="assets/img/logo.png" alt="Shangla UPVC logo" data-start="{S[6]}" data-duration="{r2(TOTAL - S[6])}" style="position:absolute;left:90px;top:300px;width:900px;height:460px;object-fit:contain;border-radius:36px;"></div>')
show("#e", S[6], TOTAL); tw("#e", '{clipPath:"circle(0% at 50% 50%)"}', '{clipPath:"circle(80% at 50% 50%)", duration:0.6, ease:"power3.inOut"}', S[6])
tw("#ei", "{scale:0.7, opacity:0}", '{scale:1, opacity:1, duration:0.5, ease:"back.out(1.6)"}', S[6] + 0.3)
word("w7a", "RAWALPINDI", 29.48, TOTAL, f"left:90px;top:880px;font-family:AN;font-size:120px;color:{P};", "left")
word("w7b", "ISLAMABAD", 31.48, TOTAL, f"left:90px;top:1010px;font-family:AN;font-size:120px;color:#2e7d1a;", "right")
body.append(f'<div id="ph" style="position:absolute;left:70px;right:70px;top:1230px;height:200px;border-radius:30px;background:{P};"></div>'); show("#ph", 32.3, TOTAL)
tw("#ph", "{scaleX:0}", '{scaleX:1, duration:0.4, ease:"power3.out"}', 32.3)
num = "0311-0444465"
xs, x = [], 128
for ch in num: xs.append(x); x += 46 if ch == "-" else 76
for k, ch in enumerate(num):
    word(f"d{k}", ch, 32.5 + k * 0.06, TOTAL, f"left:{xs[k]}px;top:1250px;font-family:AN;font-size:150px;color:{W_};width:{46 if ch == "-" else 76}px;text-align:center;", "drop")
sfx("confirm-1", 32.5, 0.4, 0.3)
word("w7c", "ABHI CALL KAREIN", 33.42, TOTAL, f"left:90px;top:1490px;font-family:AN;font-size:110px;color:{K};", "slam", "pop-high")
word("w7d", "facebook.com/shanglaupvc", 34.2, TOTAL, f"left:96px;top:1660px;font-family:MR;font-weight:700;font-size:52px;color:#444;", "up")
js.append('tl.to("#ph", {scale:1.04, duration:0.35, yoyo:true, repeat:5, ease:"sine.inOut"}, 34.0);')

# ---------- global overlays: grain, moving light leak, thin frame
body.append('<svg id="gr" width="1300" height="2200" style="position:absolute;left:-100px;top:-100px;opacity:0.10;pointer-events:none;mix-blend-mode:overlay;" data-layout-allow-overflow>'
            '<filter id="nz"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch"/></filter><rect width="1300" height="2200" filter="url(#nz)"/></svg>')
js.append(f'tl.to("#gr", {{x:60, y:-40, duration:0.08, repeat:{int(TOTAL / 0.16)}, yoyo:true, ease:"steps(1)"}}, 0);')
body.append('<div id="lk" style="position:absolute;left:-600px;top:-400px;width:1400px;height:1400px;border-radius:50%;background:radial-gradient(circle, rgba(255,190,120,0.45) 0%, rgba(255,140,60,0) 65%);mix-blend-mode:screen;pointer-events:none;"></div>')
for at in (S[2] - 0.35, S[3] - 0.2, S[6] - 0.2):
    tw("#lk", "{x:-200, y:0, opacity:0}", '{x:900, y:900, opacity:1, duration:0.7, ease:"sine.inOut"}', at); to("#lk", "{opacity:0, duration:0.3}", at + 0.7)
body.append(f'<div id="fr" style="position:absolute;inset:28px;border:3px solid rgba(255,255,255,0.35);border-radius:20px;pointer-events:none;"></div>'); show("#fr", 0, S[6])

run = lambda *a: subprocess.run(a, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
run(PV, f"{TL}/music_fit.py", f"{REPO}/library/music/" + os.environ.get("MUSIC", "cc0/upbeat-electronic--holiznacc0--pantheon.mp3"), "assets/audio/music.wav", "--length", str(TOTAL), "--end", "fade", "--fade", "1.8")
run(PV, f"{TL}/mix_vo_music.py", "assets/audio/vo_placed.wav", "assets/audio/music.wav", "assets/audio/mix.wav", "--lufs", "-16")
open("index.html", "w").write(f'''<!doctype html>
<html lang="en" data-resolution="portrait"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080, height=1920">
<script src="assets/vendor/gsap-3.14.2.min.js"></script><style>
@font-face {{ font-family:"AN"; src:url("assets/fonts/Anton-Regular.ttf"); }}
@font-face {{ font-family:"PS"; src:url("assets/fonts/Poppins-SemiBold.ttf"); }}
@font-face {{ font-family:"MR"; src:url("assets/fonts/Manrope-Variable.ttf"); font-weight:200 800; }}
* {{ margin:0; padding:0; box-sizing:border-box; }} html, body {{ width:1080px; height:1920px; overflow:hidden; background:{K}; }}
.kw {{ white-space:nowrap; line-height:1; }}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920" style="position:absolute;inset:0;overflow:hidden;background:{K};">
{chr(10).join(body)}
<audio id="mix" src="assets/audio/mix.wav" data-start="0" data-duration="{TOTAL}" data-volume="1.0" data-track-index="10"></audio>
{chr(10).join(aud)}
</div><script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
tl.to({{}}, {{ duration: {TOTAL} }}, 0);
window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;
</script></body></html>''')
print("built shangla reel v2", TOTAL)
