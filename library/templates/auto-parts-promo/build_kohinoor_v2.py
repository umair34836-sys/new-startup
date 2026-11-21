# Kohinoor promo v2 (owner 2026-11-21: two TikTok references "as an inspiration ... is inspiration k style me bana do").
# 9:16, 30 s, music only (both references have no voice: listen.py found 0 voice activity in either).
# Reference 1 (motion-design "creative concept"): white set, kinetic words with blur-in, red circle reveal, an app-like
#   search bar being typed, a card with icons, a "Pinned"-style button press, red end card.
# Reference 2 (hype "exploded" product edit): object parts flying apart, whip-pans with motion blur, beat cuts, letterbox
#   bars, red light accents, glowing name low in frame, glitch end.
# Nothing is copied from the references (no frames, no audio): only the editing grammar.
# Music: HoliznaCC0 "Phonk Remix" (CC0) 92 BPM, intro 0-10.4 s, drop on the strong kick at 10.48 s (listen.py +
#   beat_events.py, 2026-11-21) -> act 1 = clean white motion design on the quiet intro, act 2 = hype footage on the drop,
#   act 3 = clean white card on the 18.9 s break, red end card under the fade.
# Facts: library/clients/kohinoor/site-data.md. Hallmark floor: no eyebrow labels, no tracked caps, no single coloured
#   word in a headline; the red accent is the reference's grammar, used on shapes/buttons, not words.
#   cd <project>; python3 build_kohinoor_v2.py
import json, os, subprocess

WD, HT, TOTAL = 1080, 1920, 30.0
RED, INK, PAPER, MUTED = "#d7141f", "#141414", "#f4f3f1", "#6b6b6b"
DROP, BREAK, END = 10.48, 18.92, 26.5
EV = json.load(open("assets/audio/events2.json"))
STRONG = [round(t, 2) for t, s in EV["strong_kicks"]]


def run(*a):
    subprocess.run(a, check=True, capture_output=True)


# ---------- act 2 footage: one shot per kick/snare group (beat_events.py), 9:16 crops of the 4K Mixkit clips ----------
# (t0, t1, clip, source start, x-focus, extra filter)
A2 = [(10.48, 11.48, "65", 3.0, 0.60, ""),
      (11.48, 12.46, "4716", 1.5, 0.30, ""),
      (12.46, 14.07, "2675", 0.8, 0.47, ""),
      (14.07, 15.71, "65", 5.5, 0.50, ",boxblur=18:2,eq=brightness=-0.18"),   # dark bed under the exploded piston
      (15.71, 17.02, "41937", 0.5, 0.52, ""),
      (17.02, BREAK, "44284", 5.0, 0.42, "")]
os.makedirs("assets/clips", exist_ok=True)
parts = []
for j, (t0, t1, cid, a, fx, extra) in enumerate(A2):
    d = round(t1 - t0, 3)
    cw = 1214
    vf = (f"fps=30,crop={cw}:2160:{int((3840 - cw) * fx)}:0,scale={WD}:{HT}:flags=lanczos,"
          f"eq=contrast=1.25:saturation=0.82,colorbalance=bs=0.06:rs=0.03{extra},"
          f"tpad=stop_mode=clone:stop_duration={d},trim=0:{d},setpts=PTS-STARTPTS,format=yuv420p")
    out = f"assets/clips/a2_{j}.mp4"
    run("ffmpeg", "-y", "-ss", str(a), "-t", str(d + 0.5), "-i", f"assets/stock/mk_{cid}.mp4", "-an", "-vf", vf,
        "-t", str(d), "-c:v", "libx264", "-crf", "16", "-r", "30", out)
    parts.append(out)
open("assets/clips/list2.txt", "w").write("".join(f"file '{os.path.basename(p)}'\n" for p in parts))
run("ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "assets/clips/list2.txt", "-c", "copy", "assets/act2.mp4")
# end-card bed: highway shot tinted red (real footage behind the end card, not a flat gradient)
run("ffmpeg", "-y", "-ss", "3", "-t", str(TOTAL - END + 0.3), "-i", "assets/stock/mk_44284.mp4", "-an", "-vf",
    f"fps=30,crop=1214:2160:{int((3840 - 1214) * 0.42)}:0,scale={WD}:{HT}:flags=lanczos,hue=s=0,"
    f"colorchannelmixer=rr=0.9:gg=0.12:bb=0.12,eq=brightness=-0.12:contrast=1.1,format=yuv420p",
    "-t", str(round(TOTAL - END, 3)), "-c:v", "libx264", "-crf", "18", "-r", "30", "assets/endbed.mp4")
# card photo for act 3: one frame of the engine close-up
run("ffmpeg", "-y", "-ss", "6.5", "-i", "assets/stock/mk_65.mp4", "-frames:v", "1", "-vf",
    "crop=1600:2000:1300:80,scale=640:800,eq=contrast=1.1", "-q:v", "3", "assets/card.jpg")

# ---------- piston illustration (generic piston + 3-ring set: top ring, second ring, oil ring) ----------
PISTON = """
<svg id="pst" viewBox="0 0 600 640" width="600" height="640" style="position:absolute;left:240px;top:760px;overflow:visible">
  <defs>
    <linearGradient id="metal" x1="0" x2="1"><stop offset="0" stop-color="#6d7178"/><stop offset="0.35" stop-color="#e6e8ea"/>
      <stop offset="0.6" stop-color="#b9bdc2"/><stop offset="1" stop-color="#5b5f66"/></linearGradient>
    <linearGradient id="ringm" x1="0" x2="1"><stop offset="0" stop-color="#3a3c40"/><stop offset="0.45" stop-color="#cfd2d6"/>
      <stop offset="1" stop-color="#2c2e31"/></linearGradient>
  </defs>
  <path d="M120 250 Q120 215 160 210 L440 210 Q480 215 480 250 L480 560 Q300 600 120 560 Z" fill="url(#metal)"/>
  <rect x="120" y="262" width="360" height="12" fill="#2a2c30"/>
  <rect x="120" y="296" width="360" height="12" fill="#2a2c30"/>
  <rect x="120" y="330" width="360" height="18" fill="#2a2c30"/>
  <circle cx="300" cy="455" r="46" fill="#4a4d52"/><circle cx="300" cy="455" r="30" fill="#25272a"/>
  <g id="rg0"><ellipse cx="300" cy="268" rx="186" ry="22" fill="none" stroke="url(#ringm)" stroke-width="12"/></g>
  <g id="rg1"><ellipse cx="300" cy="302" rx="186" ry="22" fill="none" stroke="url(#ringm)" stroke-width="12"/></g>
  <g id="rg2"><ellipse cx="300" cy="339" rx="186" ry="22" fill="none" stroke="url(#ringm)" stroke-width="18"/>
    <ellipse cx="300" cy="339" rx="186" ry="22" fill="none" stroke="#17181a" stroke-width="3" stroke-dasharray="10 8"/></g>
</svg>"""
LBL = ["Top ring", "Second ring", "Oil ring"]
RING_UP = [-300, -205, -110]     # where each ring flies (px, y) in the exploded view

# ---------- the page ----------
QUERY = "genuine piston rings"
TYPE0, TYPE1 = 8.55, 9.95          # typing span (act 1 search bar)
html, js = [], []
J = js.append
IN = 'ease: "expo.out"'

# act 1 white set
html.append(f'<div id="w1" style="position:absolute;inset:0;background:radial-gradient(circle at 50% 42%, #ffffff 0%, {PAPER} 70%);"></div>')
html.append(f'<div id="brand0" style="position:absolute;left:0;right:0;top:170px;text-align:center;font-weight:700;font-size:54px;color:{INK};letter-spacing:-0.01em;">Kohinoor</div>')
W1 = ["Need", "genuine", "parts?"]
W2 = ["We", "have", "the", "solution."]
html.append('<div id="q1" style="position:absolute;left:80px;right:80px;top:820px;text-align:center;font-weight:700;font-size:112px;line-height:1.05;color:%s;">%s</div>'
            % (INK, " ".join(f'<span id="q1w{i}" style="display:inline-block;">{w}</span>' for i, w in enumerate(W1))))
html.append('<div id="q2" style="position:absolute;left:80px;right:80px;top:820px;text-align:center;font-weight:700;font-size:112px;line-height:1.05;color:%s;visibility:hidden;">%s</div>'
            % (INK, " ".join(f'<span id="q2w{i}" style="display:inline-block;">{w}</span>' for i, w in enumerate(W2))))
# first word visible at 0 s (thumbnail), the rest blur in on the intro beats (listen.py grid 0.67 + n*0.652)
# whole question readable on frame 0 (thumbnail; first render showed a lone "Need"); words settle on the first beats
for i, t in [(0, 0.0), (1, 0.67), (2, 1.32)]:
    J(f'    tl.fromTo("#q1w{i}", {{ y: 0 }}, {{ y: -14, duration: 0.5, yoyo: true, repeat: 1, ease: "power2.out" }}, {t});')
J('    tl.to("#q1", { x: -260, opacity: 0, filter: "blur(16px)", duration: 0.28, ease: "power3.in" }, 3.05);')
J('    tl.set("#q2", { visibility: "visible" }, 3.32);')
for i, t in enumerate([3.32, 3.66, 3.97, 4.32]):
    J(f'    tl.fromTo("#q2w{i}", {{ y: 70, opacity: 0, filter: "blur(14px)" }}, {{ y: 0, opacity: 1, filter: "blur(0px)", duration: 0.5, {IN} }}, {t});')
J('    tl.to("#q2", { scale: 0.86, opacity: 0, filter: "blur(10px)", duration: 0.3, ease: "power3.in" }, 5.5);')
# red circle on the strong kick at 5.84 s, grows to fill, piston badge + name
html.append(f'<div id="dot" style="position:absolute;left:390px;top:810px;width:300px;height:300px;border-radius:50%;background:{RED};box-shadow:0 30px 80px rgba(215,20,31,0.35);"></div>')
html.append('<div id="badge" style="position:absolute;left:0;right:0;top:700px;text-align:center;color:#fff;opacity:0;">'
            '<svg width="220" height="230" viewBox="0 0 220 230"><path d="M30 60 Q30 40 50 38 L170 38 Q190 40 190 60 L190 190 Q110 210 30 190 Z" fill="#fff"/>'
            f'<rect x="30" y="66" width="160" height="9" fill="{RED}"/><rect x="30" y="88" width="160" height="9" fill="{RED}"/><rect x="30" y="110" width="160" height="13" fill="{RED}"/>'
            f'<circle cx="110" cy="152" r="20" fill="{RED}"/></svg>'
            '<div style="font-weight:800;font-size:120px;letter-spacing:-0.03em;margin-top:24px;">Kohinoor</div>'
            '<div style="font-weight:500;font-size:46px;opacity:0.9;">Auto parts dealer</div></div>')
J('    gsap.set("#dot", { scale: 0 }); gsap.set("#bt", { yPercent: -100 }); gsap.set("#bb", { yPercent: 100 });')
J(f'    tl.fromTo("#dot", {{ scale: 0 }}, {{ scale: 1, duration: 0.35, ease: "back.out(2)" }}, 5.84);')
J('    tl.to("#dot", { scale: 8.5, duration: 0.5, ease: "power3.in" }, 6.25);')
J(f'    tl.fromTo("#badge", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.5, {IN} }}, 6.6);')
J('    tl.to(["#dot", "#badge"], { opacity: 0, duration: 0.2 }, 8.1);')
J('    tl.set("#brand0", { opacity: 0 }, 5.9);')
# search bar typing (8.41 s downbeat) + click on the search icon right before the drop
html.append(f'<div id="sb" style="position:absolute;left:90px;right:90px;top:860px;height:150px;border-radius:75px;background:#fff;'
            f'box-shadow:0 24px 60px rgba(0,0,0,0.12);display:flex;align-items:center;padding:0 60px;opacity:0;">'
            f'<div id="sbt" style="flex:1;font-weight:600;font-size:56px;color:{INK};white-space:nowrap;">'
            + "".join(f'<span id="ch{i}" style="visibility:hidden;">{c if c != " " else "&nbsp;"}</span>' for i, c in enumerate(QUERY))
            + f'<span id="caret" style="display:inline-block;width:5px;height:60px;background:{RED};vertical-align:middle;margin-left:4px;"></span></div>'
            f'<div id="sbi" style="width:92px;height:92px;border-radius:50%;background:{RED};display:flex;align-items:center;justify-content:center;">'
            '<svg width="46" height="46" viewBox="0 0 24 24"><circle cx="10" cy="10" r="6.5" fill="none" stroke="#fff" stroke-width="2.6"/>'
            '<line x1="15" y1="15" x2="21" y2="21" stroke="#fff" stroke-width="2.6" stroke-linecap="round"/></svg></div></div>')
J(f'    tl.fromTo("#sb", {{ opacity: 0, y: 60, scale: 0.94 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.45, {IN} }}, 8.41);')
for i in range(len(QUERY)):
    J(f'    tl.set("#ch{i}", {{ visibility: "visible" }}, {TYPE0 + i * (TYPE1 - TYPE0) / len(QUERY):.3f});')
J('    tl.to("#sbi", { scale: 0.82, duration: 0.08 }, 10.18); tl.to("#sbi", { scale: 1, duration: 0.12 }, 10.26);')
J('    tl.to("#sb", { scale: 1.6, opacity: 0, filter: "blur(18px)", duration: 0.22, ease: "power3.in" }, 10.28);')
J('    tl.set("#w1", { visibility: "hidden" }, %s);' % DROP)

# act 2: hype footage (video is its own clip in the root; this layer = punches, whips, bars, glow name, flashes)
html.append(f'<div id="bars" style="position:absolute;inset:0;pointer-events:none;">'
            f'<div id="bt" style="position:absolute;left:0;right:0;top:0;height:210px;background:#000;"></div>'
            f'<div id="bb" style="position:absolute;left:0;right:0;bottom:0;height:210px;background:#000;"></div></div>')
html.append('<div id="glow" style="position:absolute;left:0;right:0;top:1340px;text-align:center;font-weight:800;font-size:92px;color:#fff;'
            f'letter-spacing:-0.01em;text-shadow:0 0 18px rgba(255,255,255,0.75),0 0 46px {RED};opacity:0;">Kohinoor</div>')
html.append(f'<div id="ledL" style="position:absolute;left:0;top:0;bottom:0;width:26px;background:linear-gradient(180deg,transparent,{RED},transparent);opacity:0;"></div>')
J(f'    tl.fromTo("#glow", {{ opacity: 0, scale: 1.25 }}, {{ opacity: 1, scale: 1, duration: 0.35, {IN} }}, {DROP + 0.05});')
J(f'    tl.to("#glow", {{ opacity: 0, duration: 0.15 }}, 14.0); tl.to("#glow", {{ opacity: 1, duration: 0.2 }}, 15.75);')
J(f'    tl.to("#glow", {{ opacity: 0, duration: 0.2 }}, 17.0);')
# letterbox bars snap in on the rev-counter shot and on the oil shot (not every shot)
for t0, t1 in [(12.46, 14.05), (15.71, 17.0)]:
    J(f'    tl.to("#bt", {{ yPercent: 0, duration: 0.14, ease: "power4.out" }}, {t0}); tl.to("#bb", {{ yPercent: 0, duration: 0.14, ease: "power4.out" }}, {t0});')
    J(f'    tl.to("#bt", {{ yPercent: -100, duration: 0.12 }}, {t1}); tl.to("#bb", {{ yPercent: 100, duration: 0.12 }}, {t1});')
J(f'    tl.fromTo("#ledL", {{ opacity: 0 }}, {{ opacity: 0.9, duration: 0.2, yoyo: true, repeat: 3 }}, 11.48);')

# exploded piston on the three snares 14.07 / 14.40 / 14.72, back together on the strong kick 15.71
html.append(f'<div id="ex" style="position:absolute;inset:0;opacity:0;">{PISTON}'
            + "".join(f'<div id="lb{i}" style="position:absolute;left:96px;top:{760 + 268 + [-300, -205, -110][i] + [0, 34, 71][i] - 30}px;'
                      f'font-weight:700;font-size:40px;color:#fff;opacity:0;"><span style="display:inline-block;width:46px;height:6px;background:{RED};vertical-align:middle;margin-right:14px;"></span>{LBL[i]}</div>'
                      for i in range(3))
            + f'<div id="exh" style="position:absolute;left:0;right:0;top:1500px;text-align:center;font-weight:800;font-size:84px;color:#fff;opacity:0;">NPR piston rings</div></div>')
J('    tl.fromTo("#ex", { opacity: 0 }, { opacity: 1, duration: 0.12 }, 14.07);')
J('    tl.fromTo("#pst", { scale: 0.9, transformOrigin: "50% 50%" }, { scale: 1, duration: 0.5, ease: "expo.out" }, 14.07);')
for i, t in enumerate([14.07, 14.40, 14.72]):
    J(f'    tl.to("#rg{i}", {{ y: {RING_UP[i]}, duration: 0.3, ease: "expo.out" }}, {t});')
    J(f'    tl.fromTo("#lb{i}", {{ opacity: 0, x: -30 }}, {{ opacity: 1, x: 0, duration: 0.25, {IN} }}, {t + 0.08:.2f});')
J(f'    tl.fromTo("#exh", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.35, {IN} }}, 14.2);')
J('    tl.to(["#lb0", "#lb1", "#lb2"], { opacity: 0, duration: 0.12 }, 15.45);')
J('    tl.to(["#rg0", "#rg1", "#rg2"], { y: 0, duration: 0.22, ease: "power4.in" }, 15.49);')
J('    tl.to("#ex", { opacity: 0, duration: 0.1 }, 15.71);')
# big type on the highway shot
html.append('<div id="gpv" style="position:absolute;left:0;right:0;top:420px;height:820px;opacity:0;background:linear-gradient(180deg,rgba(0,0,0,0) 0%,rgba(0,0,0,0.62) 35%,rgba(0,0,0,0.62) 65%,rgba(0,0,0,0) 100%);"></div>')
html.append('<div id="gp" style="position:absolute;left:80px;right:80px;top:640px;font-weight:800;font-size:122px;line-height:1.0;color:#fff;'
            'text-shadow:0 6px 30px rgba(0,0,0,0.6);opacity:0;">Genuine NPR<br>piston rings.</div>')
J(f'    tl.fromTo("#gp", {{ opacity: 0, x: -120, filter: "blur(16px)" }}, {{ opacity: 1, x: 0, filter: "blur(0px)", duration: 0.4, {IN} }}, 17.05);')
J('    tl.fromTo("#gpv", { opacity: 0 }, { opacity: 1, duration: 0.2 }, 17.02);')
J('    tl.to(["#gp", "#gpv"], { opacity: 0, duration: 0.15 }, 18.75);')
# white flash on the strong kicks of the drop (phonk formula step 3), not on every kick
html.append('<div id="fl" style="position:absolute;inset:0;background:#fff;opacity:0;"></div>')
for t in [DROP, 12.46, 15.71]:   # set + to: a fromTo would render its 0.9 "from" before the first flash
    J(f'    tl.set("#fl", {{ opacity: 0.9 }}, {t}); tl.to("#fl", {{ opacity: 0, duration: 0.12, ease: "none" }}, {t + 0.01:.2f});')

# act 3 white card (pin-style) on the break
html.append(f'<div id="w3" style="position:absolute;inset:0;background:radial-gradient(circle at 50% 40%, #ffffff 0%, {PAPER} 70%);visibility:hidden;">'
            f'<div id="pin" style="position:absolute;left:220px;top:300px;width:640px;height:800px;border-radius:44px;overflow:hidden;'
            f'box-shadow:0 40px 90px rgba(0,0,0,0.22);"><img src="assets/card.jpg" alt="" style="width:640px;height:800px;object-fit:cover;"></div>'
            + "".join(f'<div id="ic{i}" style="position:absolute;left:{[880, 900, 870][i]}px;top:{[520, 680, 840][i]}px;width:96px;height:96px;border-radius:50%;'
                      f'background:{"#fff" if i else RED};box-shadow:0 12px 30px rgba(0,0,0,0.18);display:flex;align-items:center;justify-content:center;">'
                      f'<svg width="46" height="46" viewBox="0 0 24 24">{s}</svg></div>'
                      for i, s in enumerate([
                          '<path d="M12 2 L15 9 L12 22 L9 9 Z" fill="#fff"/>',
                          f'<path d="M12 21 C5 15 3 11.5 3 8.5 C3 6 5 4 7.5 4 C9.5 4 11 5.2 12 6.8 C13 5.2 14.5 4 16.5 4 C19 4 21 6 21 8.5 C21 11.5 19 15 12 21 Z" fill="none" stroke="{INK}" stroke-width="2"/>',
                          f'<circle cx="6" cy="12" r="2.4" fill="{INK}"/><circle cx="18" cy="6" r="2.4" fill="{INK}"/><circle cx="18" cy="18" r="2.4" fill="{INK}"/>'
                          f'<line x1="8" y1="11" x2="16" y2="7" stroke="{INK}" stroke-width="2"/><line x1="8" y1="13" x2="16" y2="17" stroke="{INK}" stroke-width="2"/>']))
            + f'<div id="pt" style="position:absolute;left:120px;right:120px;top:1170px;text-align:center;color:{INK};">'
              f'<div style="font-weight:800;font-size:96px;letter-spacing:-0.02em;">NPR</div>'
              f'<div style="font-weight:600;font-size:52px;margin-top:4px;">Nippon Piston Ring</div>'
              f'<div style="font-weight:500;font-size:44px;color:{MUTED};margin-top:12px;">Japan, since 1934</div></div>'
            + f'<div id="btn" style="position:absolute;left:0;right:0;top:1520px;text-align:center;">'
              f'<span id="btnp" style="display:inline-block;padding:30px 58px;border-radius:60px;background:{RED};color:#fff;font-weight:700;font-size:52px;'
              f'box-shadow:0 18px 40px rgba(215,20,31,0.35);">Authorized NPR dealer</span></div></div>')
J(f'    tl.set("#w3", {{ visibility: "visible" }}, {BREAK});')
J(f'    tl.fromTo("#pin", {{ rotation: -14, scale: 0.6, y: 300, opacity: 0 }}, {{ rotation: 0, scale: 1, y: 0, opacity: 1, duration: 0.7, {IN} }}, {BREAK});')
for i, t in enumerate([19.62, 19.9, 20.18]):
    J(f'    tl.fromTo("#ic{i}", {{ scale: 0 }}, {{ scale: 1, duration: 0.35, ease: "back.out(2.2)" }}, {t});')
J(f'    tl.fromTo("#pt", {{ opacity: 0, y: 50, filter: "blur(10px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.5, {IN} }}, 20.93);')
J(f'    tl.fromTo("#btn", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.4, {IN} }}, 22.56);')
J('    tl.to("#btnp", { scale: 0.9, duration: 0.09 }, 23.12); tl.to("#btnp", { scale: 1.06, duration: 0.14, ease: "back.out(3)" }, 23.21);'
  ' tl.to("#btnp", { scale: 1, duration: 0.2 }, 23.4);')
J('    tl.to("#pin", { y: -30, duration: 3.2, ease: "none" }, 21.0);')
J(f'    tl.to("#w3", {{ opacity: 0, scale: 1.08, filter: "blur(14px)", duration: 0.3, ease: "power3.in" }}, {END - 0.3});')

# end card over the red-tinted highway; name letters glitch in (ref 2 end), credit line
NAME = "Kohinoor"
html.append('<div id="ec" style="position:absolute;inset:0;visibility:hidden;">'
            '<div style="position:absolute;left:0;right:0;top:760px;text-align:center;color:#fff;">'
            '<div style="font-weight:800;font-size:170px;letter-spacing:-0.03em;text-shadow:0 0 30px rgba(255,255,255,0.35);">'
            + "".join(f'<span id="ek{i}" style="display:inline-block;">{c}</span>' for i, c in enumerate(NAME))
            + '</div><div id="es" style="font-weight:600;font-size:56px;margin-top:10px;">Authorized NPR dealer</div>'
            '<div id="es2" style="font-weight:500;font-size:44px;opacity:0.85;margin-top:8px;">Auto parts, Pakistan</div></div>'
            '<div id="ecr" style="position:absolute;left:0;right:0;bottom:110px;text-align:center;font-weight:500;font-size:30px;color:rgba(255,255,255,0.75);">Edited by MrCopper804</div></div>')
J(f'    tl.set("#ec", {{ visibility: "visible" }}, {END});')
for i in range(len(NAME)):
    J(f'    tl.fromTo("#ek{i}", {{ opacity: 0, y: {[-26, 22][i % 2]}, filter: "blur(10px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.3, {IN} }}, {END + 0.05 + 0.05 * i:.2f});')
J(f'    tl.fromTo(["#es", "#es2"], {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {END + 0.6});')
J(f'    tl.fromTo("#ecr", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {END + 1.0});')

# camera layer for act 2: kick punches (6% snap-back, phonk formula) and whip-pans with blur into two cuts
KICKS = [t for t in STRONG if DROP <= t < BREAK]
cam = []
for n, t in enumerate(KICKS):
    cam.append(f'    tl.fromTo("#cam", {{ scale: 1.06 }}, {{ scale: 1, duration: 0.24, {IN}{", immediateRender: false" if n else ""} }}, {t});')
for t in [11.48, 17.02]:
    cam.append(f'    tl.to("#cam", {{ x: -240, filter: "blur(16px)", duration: 0.1, ease: "power2.in" }}, {t - 0.1:.2f});')
    cam.append(f'    tl.fromTo("#cam", {{ x: 240, filter: "blur(16px)" }}, {{ x: 0, filter: "blur(0px)", duration: 0.16, ease: "power2.out", immediateRender: false }}, {t});')

def dur(p):
    return round(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                      capture_output=True, text=True).stdout), 3)

# SFX: every file once; only on story moments (pop on the circle, typing, click, engine on the drop, one swish per ring,
# metal hit when the rings seat, whoosh to the card, confirm on the button, glitch on the end name)
SFX = [("s_pop", "pop/pop-low", 5.84, 0.5), ("s_typ", "typing/typing-keyboard-fast", TYPE0, 0.35),
       ("s_clk", "ui/mouse-click", 10.18, 0.6), ("s_eng", "vehicle/car-engine-start", DROP - 0.05, 0.35),
       ("s_r0", "transition/swish-1", 14.05, 0.5), ("s_r1", "transition/swish-4", 14.38, 0.5), ("s_r2", "transition/swish-7", 14.70, 0.5),
       ("s_hit", "impact/metal-hit", 15.69, 0.4), ("s_wh", "transition/whoosh-up-0.6s", BREAK - 0.35, 0.35),
       ("s_ok", "ui/confirm-1", 23.21, 0.45), ("s_gl", "glitch/glitch-short", END, 0.3)]
assert len({n for _, n, _, _ in SFX}) == len(SFX)
aud = [f'      <audio id="bed" src="assets/audio/bed2.wav" data-start="0" data-duration="{TOTAL}" data-volume="1" data-track-index="10"></audio>']
for ln, (i, n, t, v) in enumerate(SFX):
    d = dur(f"assets/sfx/{n.split('/')[1]}.mp3")
    if i == "s_typ":
        d = min(d, round(TYPE1 - TYPE0 + 0.1, 2))
    aud.append(f'      <audio id="{i}" src="assets/sfx/{n.split("/")[1]}.mp3" data-start="{t}" data-duration="{d}" data-volume="{v}" data-track-index="{11 + ln}"></audio>')

open("index.html", "w").write(f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={WD}, height={HT}" />
    <script src="assets/vendor/gsap-3.14.2.min.js"></script>
    <style>
      @font-face {{ font-family: "Manrope"; src: url("assets/fonts/Manrope-Variable.ttf"); font-weight: 200 800; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: {WD}px; height: {HT}px; overflow: hidden; background: #000; font-family: Manrope; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="{WD}" data-height="{HT}">
      <div id="cam" style="position:absolute;inset:0;">
        <video id="a2v" src="assets/act2.mp4" muted playsinline data-start="{DROP}" data-duration="{round(BREAK - DROP, 3)}" data-track-index="0"
          style="position:absolute;inset:0;width:{WD}px;height:{HT}px;object-fit:cover;"></video>
      </div>
      <video id="endv" src="assets/endbed.mp4" muted playsinline data-start="{END}" data-duration="{round(TOTAL - END, 3)}" data-track-index="1"
        style="position:absolute;inset:0;width:{WD}px;height:{HT}px;object-fit:cover;"></video>
      <div id="ov" style="position:absolute;inset:0;">
{chr(10).join(html)}
      </div>
{chr(10).join(aud)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
{chr(10).join(cam)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
""")
print("built v2", TOTAL, "kick punches", KICKS)
