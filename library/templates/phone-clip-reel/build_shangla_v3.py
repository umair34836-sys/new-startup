#!/usr/bin/env python3
"""Shangla UPVC winter ad v3 (2026-11-20): the CLIENT's own 91.7 s Urdu VO is the clock. 9:16, kinetic type synced to
the VO's word times (Whisper small word_timestamps, +0.3 s placement), a transition at every scene change, snow overlay
for the winter lines, grain + light leak. Phone 0313-512-0718 = what the VO says (Whisper medium, 4 settings agree).
python3 build_shangla_v3.py PROJECT
"""
import os, subprocess, sys
os.chdir(sys.argv[1])
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
PV, TL = "/home/user/tools/perc-venv/bin/python", f"{REPO}/library/tools"
TOTAL = 93.6
G, G2, P, W_, K = "#5bbf2a", "#2e7d1a", "#3d2b8f", "#ffffff", "#0d0b14"
S = [0, 5.4, 12.6, 19.9, 25.0, 35.6, 46.4, 56.3, 63.3, 68.9, 76.4, 83.4, TOTAL]
r2 = lambda x: round(x, 2)
body, js, aud = [], [], []
def tw(sel, fr, to, at): js.append(f'tl.fromTo("{sel}", {fr}, {to}, {r2(at)});')
def to(sel, v, at): js.append(f'tl.to("{sel}", {v}, {r2(at)});')
def show(sel, t0, t1):
    js.append(f'gsap.set("{sel}", {{visibility:"hidden"}});'); js.append(f'tl.set("{sel}", {{visibility:"visible"}}, {r2(t0)});')
    if t1 < TOTAL: js.append(f'tl.set("{sel}", {{visibility:"hidden"}}, {r2(t1)});')
def sfx(n, at, d, v=0.22): aud.append(f'<audio id="fx{len(aud)}" src="assets/sfx/{n}.mp3" data-start="{r2(at)}" data-duration="{d}" data-volume="{v}" data-track-index="{11 + len(aud) % 3}"></audio>')
def clip(i, name, t0, t1, z0=1.0, z1=1.08, origin="50% 50%", enter=None):
    d = r2(t1 - t0)
    body.append(f'<div id="{i}" style="position:absolute;inset:0;overflow:hidden;"><div id="{i}z" style="position:absolute;inset:0;transform-origin:{origin};">'
                f'<video id="{i}v" src="assets/clips/{name}.mp4" data-start="{r2(t0)}" data-duration="{d}" muted playsinline style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;"></video></div></div>')
    show(f"#{i}", t0, t1); tw(f"#{i}z", f"{{scale:{z0}}}", f'{{scale:{z1}, duration:{d}, ease:"none"}}', t0)
    if enter == "right": tw(f"#{i}", "{x:1080}", '{x:0, duration:0.45, ease:"power4.inOut"}', t0)
    if enter == "up": tw(f"#{i}", "{y:1920}", '{y:0, duration:0.45, ease:"power4.inOut"}', t0)
    if enter == "iris":
        js.append(f'gsap.set("#{i}", {{clipPath:"circle(0% at 50% 50%)"}});'); tw(f"#{i}", '{clipPath:"circle(0% at 50% 50%)"}', '{clipPath:"circle(80% at 50% 50%)", duration:0.5, ease:"power3.out"}', t0)
    if enter == "wipe":
        js.append(f'gsap.set("#{i}", {{clipPath:"inset(0% 0% 100% 0%)"}});'); tw(f"#{i}", '{clipPath:"inset(0% 0% 100% 0%)"}', '{clipPath:"inset(0% 0% 0% 0%)", duration:0.45, ease:"power3.inOut"}', t0)
FX = {"slam": ('{scale:2.6, opacity:0}', '{scale:1, opacity:1, duration:0.32, ease:"power4.out"}'),
      "up": ('{y:120, opacity:0}', '{y:0, opacity:1, duration:0.4, ease:"power3.out"}'),
      "drop": ('{y:-160, opacity:0, rotation:-8}', '{y:0, opacity:1, rotation:0, duration:0.45, ease:"bounce.out"}'),
      "left": ('{x:-260, opacity:0}', '{x:0, opacity:1, duration:0.4, ease:"power4.out"}'),
      "right": ('{x:260, opacity:0}', '{x:0, opacity:1, duration:0.4, ease:"power4.out"}'),
      "blur": ('{scale:1.25, opacity:0, filter:"blur(18px)"}', '{scale:1, opacity:1, filter:"blur(0px)", duration:0.4, ease:"power2.out"}'),
      "stamp": ('{scale:0.3, rotation:-14, opacity:0}', '{scale:1, rotation:-6, opacity:1, duration:0.35, ease:"back.out(3)"}')}
SH = "text-shadow:0 6px 24px rgba(0,0,0,0.6);"
def word(i, text, at, t1, css, fx="slam", sound=None):
    body.append(f'<div id="{i}" class="kw" style="position:absolute;{css}">{text}</div>'); show(f"#{i}", at, t1)
    a, b = FX[fx]; tw(f"#{i}", a, b, at)
    if sound: sfx(sound, at, 0.3)
def big(i, text, at, t1, top, size=170, color=W_, fx="slam", sound=None, left=70, extra=""):
    word(i, text, at, t1, f"left:{left}px;top:{top}px;font-family:AN;font-size:{size}px;color:{color};{SH}{extra}", fx, sound)
def small(i, text, at, t1, top, size=64, color=W_, fx="up", left=76):
    word(i, text, at, t1, f"left:{left}px;top:{top}px;font-family:PS;font-size:{size}px;color:{color};{SH}", fx)
VEIL = '<div style="position:absolute;left:0;right:0;bottom:0;height:1100px;background:linear-gradient(180deg, rgba(13,11,20,0) 0%, rgba(13,11,20,0.85) 100%);"></div>'
def veil(i, t0, t1, top=False):
    v = VEIL if not top else '<div style="position:absolute;left:0;right:0;top:0;height:1000px;background:linear-gradient(0deg, rgba(13,11,20,0) 0%, rgba(13,11,20,0.8) 100%);"></div>'
    body.append(f'<div id="{i}" style="position:absolute;inset:0;">{v}</div>'); show(f"#{i}", t0, t1)
def bars(i, at, cols=(G, P, W_)):
    for k, c in enumerate(cols):
        body.append(f'<div id="{i}{k}" style="position:absolute;left:-200px;top:-300px;width:1500px;height:2600px;background:{c};transform:rotate(18deg);"></div>')
        show(f"#{i}{k}", at, at + 0.85); tw(f"#{i}{k}", "{x:-1700}", '{x:1900, duration:0.75, ease:"power3.inOut"}', at + k * 0.07)
    sfx("swish-4", at, 0.4, 0.26)
def shutters(i, at, col=P):
    for k in range(6):
        body.append(f'<div id="{i}{k}" style="position:absolute;left:{k * 180}px;top:0;width:181px;height:1920px;background:{col};transform-origin:50% 0;"></div>')
        show(f"#{i}{k}", at - 0.3, at + 0.35)
        tw(f"#{i}{k}", "{scaleY:0}", '{scaleY:1, duration:0.25, ease:"power2.in"}', at - 0.3 + k * 0.02)
        to(f"#{i}{k}", '{scaleY:0, transformOrigin:"50% 100%", duration:0.25, ease:"power2.out"}', at + 0.05 + k * 0.02)
    sfx("swish-1", at - 0.3, 0.35, 0.26)
def flash(i, at):
    body.append(f'<div id="{i}" style="position:absolute;inset:0;background:#fff;"></div>'); show(f"#{i}", at - 0.05, at + 0.3)
    tw(f"#{i}", "{opacity:1}", '{opacity:0, duration:0.3, ease:"power2.out"}', at - 0.05); sfx("impact-punch", at, 0.6, 0.24)
def strike(i, at, t1, top, w):
    body.append(f'<div id="{i}" style="position:absolute;left:60px;top:{top}px;width:{w}px;height:16px;background:#e23b3b;transform-origin:0 50%;transform:rotate(-4deg);"></div>')
    show(f"#{i}", at, t1); tw(f"#{i}", "{scaleX:0}", '{scaleX:1, duration:0.25, ease:"power3.out"}', at)

# 1 0-5.4 question hook on the real install
clip("c1", "a1", 0, S[1] + 0.1, 1.0, 1.15, "60% 40%"); veil("v1", 0, S[1] + 0.1)
small("w1a", "Kya aap apne ghar ko dena chahte hain", 0.4, S[1], 1180, 44)
big("w1b", "KHOOBSURAT", 2.62, S[1], 1270, 170, W_, "left", "whoosh-fast-0.3s")
big("w1c", "JADEED", 3.50, S[1], 1450, 170, G, "right")
big("w1d", "SHANDAAR", 4.20, S[1], 1630, 170, W_, "slam", "pop-low")
bars("t1", S[1] - 0.3)
# 2 5.4-12.6 winter problems, struck through, snow
clip("c2a", "b1", S[1], 9.1, 1.1, 1.0); clip("c2b", "c1", 9.0, S[2], 1.0, 1.1, enter="right"); veil("v2", S[1], S[2])
small("w2a", "Sardiyon ki", 6.74, S[2], 900, 60)
big("w2b", "THANDI HAWA", 7.36, S[2], 980, 150, W_, "left", "whoosh-fast-0.3s")
big("w2c", "BAHAR KA SHOR", 8.38, S[2], 1150, 150, W_, "right", "whoosh-fast-0.3s")
big("w2d", "GARD-O-GHUBAR", 9.52, S[2], 1320, 150, W_, "left", "whoosh-fast-0.3s")
for k, (at, top, w) in enumerate([(10.4, 1055, 760), (10.7, 1225, 900), (11.0, 1395, 960)]): strike(f"x2{k}", at, S[2], top, w)
small("w2e", "ghar ka sukoon nahi bigadna chahiye", 11.18, S[2], 1540, 50, G)
flash("f2", S[2])
# 3 12.6-19.9 the standard: three values
clip("c3a", "a2", S[2], 18.4, 1.0, 1.1); clip("c3b", "a3", 18.4, S[3], 1.1, 1.0, enter="wipe"); veil("v3", S[2], S[3])
small("w3a", "Ek aisa", 15.28, S[3], 1100, 60)
big("w3b", "MEYAR", 15.62, S[3], 1170, 230, G, "slam", "impact-punch")
for k, (txt, at) in enumerate([("Khoobsurti", 16.52), ("Aaraam", 17.66), ("Aitmaad", 18.48)]):
    word(f"w3c{k}", txt, at, S[3], f"left:{[76, 400, 680][k]}px;top:1450px;padding:10px 22px;border-radius:14px;background:{P};font-family:PS;font-size:52px;color:{W_};", "drop", "pop-high")
bars("t3", S[3] - 0.3, (P, G, W_))
# 4 19.9-25.0 "Ji haan!" brand reveal (outline-free background type)
clip("c4", "b4", S[3], S[4], 1.2, 1.0)
body.append(f'<div id="s4" style="position:absolute;inset:0;background:rgba(244,245,242,0.88);">'
            f'<div id="s4o" style="position:absolute;left:0;top:260px;white-space:nowrap;font-family:AN;font-size:420px;color:rgba(61,43,143,0.07);">SHANGLA SHANGLA</div>'
            f'<div id="s4p" style="position:absolute;left:0;top:1320px;white-space:nowrap;font-family:AN;font-size:420px;color:rgba(91,191,42,0.12);">UPVC UPVC UPVC</div>'
            f'<img id="s4l" src="assets/img/logo.png" alt="Shangla UPVC logo" data-start="{S[3]}" data-duration="{r2(S[4] - S[3])}" style="position:absolute;left:90px;top:700px;width:900px;height:460px;object-fit:contain;border-radius:36px;box-shadow:0 30px 80px rgba(61,43,143,0.25);"></div>')
show("#s4", S[3], S[4]); tw("#s4o", "{x:0}", f'{{x:-900, duration:{r2(S[4] - S[3])}, ease:"none"}}', S[3]); tw("#s4p", "{x:-900}", f'{{x:0, duration:{r2(S[4] - S[3])}, ease:"none"}}', S[3])
word("w4a", "JI HAAN!", 20.14, 22.1, f"left:90px;top:420px;font-family:AN;font-size:200px;color:{P};", "stamp", "pop-high")
tw("#s4l", "{scale:0.4, rotation:-10, opacity:0}", '{scale:1, rotation:0, opacity:1, duration:0.6, ease:"back.out(1.8)"}', 22.1); sfx("impact-punch", 22.1, 0.6, 0.26)
word("w4b", "WINDOWS", 23.32, S[4], f"left:90px;top:1220px;font-family:AN;font-size:170px;color:{P};", "left", "whoosh-fast-0.3s")
word("w4c", "&amp; DOORS", 24.14, S[4], f"left:90px;top:1400px;font-family:AN;font-size:170px;color:{G2};", "right")
tw("#s4", '{scale:1, filter:"blur(0px)"}', '{scale:2.2, filter:"blur(14px)", duration:0.4, ease:"power2.in"}', S[4] - 0.35)
# 5 25.0-35.6 design, finishing, quality
clip("c5a", "b2", S[4], 31.2, 1.0, 1.08); clip("c5b", "c2", 31.2, S[5], 1.0, 1.1, enter="iris"); veil("v5", 31.2, S[5])
for k, (txt, at, col) in enumerate([("JADEED DESIGN", 27.10, P), ("BEHTAREEN FINISHING", 28.32, G2), ("AALA MEYAR", 30.0, K)]):
    word(f"w5{k}", txt, at, 31.2, f"left:70px;top:{380 + k * 170}px;font-family:AN;font-size:130px;color:{col};", ["left", "right", "slam"][k], "whoosh-fast-0.3s")
small("w5d", "Ghar ki khoobsurti ko", 31.9, S[5], 1300, 60)
big("w5e", "NAYI PEHCHAN", 32.9, S[5], 1380, 170, G, "blur", "swish-1")
shutters("t5", S[5])
# 6 35.6-46.4 new house or old: real projects, then installs
body.append(f'<div id="s6" style="position:absolute;inset:0;background:{K};">'
            f'<div id="mq" style="position:absolute;left:0;top:60px;white-space:nowrap;font-family:AN;font-size:110px;color:{G};">NAYA GHAR &nbsp;•&nbsp; PURANA GHAR &nbsp;•&nbsp; NAYA GHAR &nbsp;•&nbsp; PURANA GHAR</div></div>')
show("#s6", S[5], 41.6); tw("#mq", "{x:0}", '{x:-1500, duration:6, ease:"none"}', S[5])
for k, (img, lab, top, rot, at) in enumerate([("dha.jpg", "DHA Overseas Tower", 260, -4, 35.8), ("farm.jpg", "Farmhouse, Islamabad", 940, 3, 37.6)]):
    body.append(f'<div id="pc{k}" style="position:absolute;left:100px;top:{top}px;width:880px;padding:22px 22px 30px;background:#fff;border-radius:18px;box-shadow:0 30px 80px rgba(0,0,0,0.6);">'
                f'<img id="pci{k}" src="assets/img/{img}" alt="{lab} project" data-start="{at}" data-duration="{r2(41.6 - at)}" style="display:block;width:836px;height:470px;object-fit:cover;border-radius:10px;">'
                f'<div style="margin-top:18px;font-family:AN;font-size:78px;color:{P};">{lab}</div></div>')
    show(f"#pc{k}", at, 41.6); tw(f"#pc{k}", f"{{y:900, rotation:{rot * 4}, opacity:0}}", f'{{y:0, rotation:{rot}, opacity:1, duration:0.6, ease:"power3.out"}}', at); sfx("swish-1", at, 0.35)
clip("c6a", "a4", 41.6, 44.9, 1.1, 1.0, enter="up"); clip("c6b", "a5", 44.9, S[6], 1.0, 1.08); veil("v6", 41.6, S[6])
small("w6a", "Aap ke liye", 43.0, S[6], 1300, 60)
big("w6b", "BEHTAREEN", 43.6, S[6], 1380, 190, W_, "left", "whoosh-fast-0.3s")
big("w6c", "INTIKHAB", 44.5, S[6], 1570, 190, G, "slam", "pop-low")
flash("f6", S[6])
# 7 46.4-56.3 beautiful outside, comfortable inside
clip("c7a", "b3", S[6], 51.4, 1.0, 1.1); clip("c7b", "c3", 51.4, S[7], 1.1, 1.0, enter="right"); veil("v7", S[6], S[7])
small("w7a", "Bahar se", 49.4, 51.4, 1250, 64)
big("w7b", "KHOOBSURAT", 50.12, 51.4, 1330, 190, W_, "slam", "whoosh-fast-0.3s")
small("w7c", "Andar se", 52.46, S[7], 1250, 64)
big("w7d", "AARAAMDEH", 54.24, S[7], 1330, 190, G, "slam", "whoosh-fast-0.3s")
shutters("t7", S[7], G2)
# 8 56.3-63.3 four features ticked
body.append(f'<div id="s8" style="position:absolute;inset:0;background:{P};"></div>'); show("#s8", S[7], S[8])
for k, (txt, at) in enumerate([("Mazboot saakht", 56.44), ("Dilkash design", 57.76), ("Aasan safai", 59.0), ("Behtareen finishing", 60.10)]):
    word(f"w8{k}", f'<span style="display:inline-block;width:110px;color:{G};">✓</span>{txt}', at, S[8], f"left:90px;top:{430 + k * 230}px;font-family:AN;font-size:108px;color:{W_};", "left", "pop-high")
word("w8e", "SAB AIK HI NAAM KE SAATH", 61.46, S[8], f"left:90px;top:1420px;padding:10px 26px;background:{G};font-family:AN;font-size:84px;color:{K};", "stamp", "confirm-1")
bars("t8", S[8] - 0.3, (W_, G, P))
# 9 63.3-68.9 winter: snow, comfort first
clip("c9", "a2", S[8], S[9], 1.15, 1.0); veil("v9", S[8], S[9])
small("w9a", "Is", 63.86, S[9], 1180, 64)
big("w9b", "MAUSAM-E-SARMA", 63.96, S[9], 1260, 120, W_, "blur", "whoosh-fast-0.3s")
small("w9c", "ghar ka aaraam aur khoobsurti", 65.6, S[9], 1440, 54)
big("w9d", "PEHLI TARJEEH", 67.94, S[9], 1520, 130, G, "stamp", "pop-low")
flash("f9", S[9])
# 10 68.9-76.4 call to action
clip("c10", "c2", S[9], 74.5, 1.0, 1.1); veil("v10", S[9], 74.5)
small("w10a", "To phir", 69.08, 74.5, 1150, 64)
big("w10b", "INTEZAR KIS BAAT KA?", 69.46, 74.5, 1230, 104, W_, "left", "whoosh-fast-0.3s")
big("w10c", "AAJ HI RABTA KAREIN", 70.86, 74.5, 1380, 104, G, "right", "pop-high")
body.append(f'<div id="s10" style="position:absolute;inset:0;background:#f4f5f2;"><img id="s10l" src="assets/img/logo.png" alt="Shangla UPVC logo" data-start="74.5" data-duration="{r2(S[10] - 74.5)}" style="position:absolute;left:90px;top:730px;width:900px;height:460px;object-fit:contain;border-radius:36px;"></div>')
show("#s10", 74.5, S[10]); tw("#s10", '{clipPath:"circle(0% at 50% 50%)"}', '{clipPath:"circle(80% at 50% 50%)", duration:0.5, ease:"power3.inOut"}', 74.5)
# 11 76.4-83.4 the number, digit by digit on the spoken digit
body.append(f'<div id="s11" style="position:absolute;inset:0;background:#f4f5f2;"><img id="s11l" src="assets/img/logo.png" alt="Shangla UPVC logo" data-start="{S[10]}" data-duration="{r2(S[11] - S[10])}" style="position:absolute;left:190px;top:260px;width:700px;height:360px;object-fit:contain;border-radius:28px;"></div>')
show("#s11", S[10], S[11])
word("w11a", "RABTA NUMBER", 76.5, S[11], f"left:90px;top:760px;font-family:AN;font-size:120px;color:{P};", "left")
body.append(f'<div id="ph" style="position:absolute;left:60px;right:60px;top:960px;height:220px;border-radius:30px;background:{P};"></div>'); show("#ph", 77.2, S[11])
tw("#ph", "{scaleX:0}", '{scaleX:1, duration:0.35, ease:"power3.out"}', 77.2)
num, times = "0313-512-0718", [77.78, 78.28, 78.56, 78.84, None, 79.30, 79.86, 80.10, None, 80.48, 81.02, 81.36, 81.68]
xs, x = [], 132
for ch in num: xs.append(x); x += 36 if ch == "-" else 68
for k, ch in enumerate(num):
    at = times[k] if times[k] else times[k - 1] + 0.12
    word(f"d{k}", ch, at, S[11], f"left:{xs[k]}px;top:985px;width:{36 if ch == '-' else 68}px;text-align:center;font-family:AN;font-size:136px;color:{W_};", "drop")
sfx("confirm-1", 77.8, 0.4, 0.26)
word("w11b", "ABHI CALL KAREIN", 81.9, S[11], f"left:90px;top:1260px;font-family:AN;font-size:110px;color:{K};", "slam", "pop-high")
js.append('tl.to("#ph", {scale:1.04, duration:0.35, yoyo:true, repeat:3, ease:"sine.inOut"}, 82.0);')
# 12 83.4-end tagline, then end card held
body.append(f'<div id="s12" style="position:absolute;inset:0;background:{K};"></div>'); show("#s12", S[11], 89.2)
tw("#s12", '{clipPath:"inset(0% 100% 0% 0%)"}', '{clipPath:"inset(0% 0% 0% 0%)", duration:0.4, ease:"power3.inOut"}', S[11])
for k, (txt, at, col) in enumerate([("KHOOBSURTI BHI.", 83.62, W_), ("MEYAR BHI.", 85.24, G), ("AITMAAD BHI.", 86.24, W_)]):
    word(f"w12{k}", txt, at, 89.2, f"left:80px;top:{560 + k * 230}px;font-family:AN;font-size:140px;color:{col};", ["left", "right", "slam"][k], "whoosh-fast-0.3s")
small("w12d", "Kyunke aap ka ghar khaas hai", 87.58, 89.2, 1330, 60, G)
body.append(f'<div id="e" style="position:absolute;inset:0;background:#f4f5f2;">'
            f'<img id="ei" src="assets/img/logo.png" alt="Shangla UPVC logo" data-start="89.2" data-duration="{r2(TOTAL - 89.2)}" style="position:absolute;left:90px;top:300px;width:900px;height:460px;object-fit:contain;border-radius:36px;">'
            f'<div style="position:absolute;left:90px;top:860px;font-family:AN;font-size:96px;line-height:1.05;color:{P};">Darwaze aur khidkiyan<br>bhi khaas.</div>'
            f'<div style="position:absolute;left:60px;right:60px;top:1150px;padding:26px 0;border-radius:30px;background:{P};text-align:center;font-family:AN;font-size:136px;color:{W_};">0313-512-0718</div>'
            f'<div style="position:absolute;left:0;right:0;top:1420px;text-align:center;font-family:MR;font-weight:700;font-size:52px;color:#444;">facebook.com/shanglaupvc</div></div>')
show("#e", 89.2, TOTAL); tw("#e", '{clipPath:"circle(0% at 50% 50%)"}', '{clipPath:"circle(80% at 50% 50%)", duration:0.6, ease:"power3.inOut"}', 89.2); sfx("confirm-1", 89.2, 0.4, 0.24)

# snow for the winter lines (scenes 2 and 9)
import random
rnd = random.Random(7)
for k in range(46):
    x, s_, d = rnd.randint(0, 1060), rnd.choice([8, 10, 12, 16]), rnd.uniform(3.2, 5.5)
    body.append(f'<div id="sn{k}" style="position:absolute;left:{x}px;top:-40px;width:{s_}px;height:{s_}px;border-radius:50%;background:rgba(255,255,255,0.85);box-shadow:0 0 8px rgba(255,255,255,0.8);"></div>')
    for t0, t1 in ((S[1], S[2]), (S[8], S[9])):
        tw(f"#sn{k}", f"{{y:{rnd.randint(-200, 1200)}, x:0}}", f'{{y:2000, x:{rnd.randint(-120, 120)}, duration:{d:.2f}, ease:"none", repeat:3}}', t0)
    js.append(f'gsap.set("#sn{k}", {{visibility:"hidden"}});')
    for t0, t1 in ((S[1], S[2]), (S[8], S[9])):
        js.append(f'tl.set("#sn{k}", {{visibility:"visible"}}, {t0}); tl.set("#sn{k}", {{visibility:"hidden"}}, {t1});')
# grain, light leak, frame
body.append('<svg id="gr" width="1300" height="2200" style="position:absolute;left:-100px;top:-100px;opacity:0.10;pointer-events:none;mix-blend-mode:overlay;" data-layout-allow-overflow>'
            '<filter id="nz"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch"/></filter><rect width="1300" height="2200" filter="url(#nz)"/></svg>')
js.append(f'tl.to("#gr", {{x:60, y:-40, duration:0.08, repeat:{int(TOTAL / 0.16)}, yoyo:true, ease:"steps(1)"}}, 0);')
body.append('<div id="lk" style="position:absolute;left:-600px;top:-400px;width:1400px;height:1400px;border-radius:50%;background:radial-gradient(circle, rgba(255,190,120,0.45) 0%, rgba(255,140,60,0) 65%);mix-blend-mode:screen;pointer-events:none;"></div>')
for at in (S[4] - 0.35, S[6] - 0.2, S[9] - 0.2, 74.3):
    tw("#lk", "{x:-200, y:0, opacity:0}", '{x:900, y:900, opacity:1, duration:0.7, ease:"sine.inOut"}', at); to("#lk", "{opacity:0, duration:0.3}", at + 0.7)
body.append('<div id="fr" style="position:absolute;inset:28px;border:3px solid rgba(255,255,255,0.35);border-radius:20px;pointer-events:none;"></div>'); show("#fr", 0, 74.5)

run = lambda *a: subprocess.run(a, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
run(PV, f"{TL}/music_fit.py", f"{REPO}/library/music/" + os.environ.get("MUSIC", "cc0/upbeat-electronic--holiznacc0--pantheon.mp3"), "assets/audio/music.wav", "--length", str(TOTAL), "--end", "fade", "--fade", "2.5")
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
print("built shangla v3", TOTAL)
