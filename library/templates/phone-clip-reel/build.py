# Builds index.html + compositions for the client "boss call" reel (105 BPM, one bar per shot).
import json, os

B = 60 / 105 * 4          # one bar = 2.2857 s
FIN = 3.6                 # end card length
TOTAL = round(6 * B + FIN, 4)
GRADE = {"preset": "skin-soft", "intensity": 0.6,
         "adjust": {"exposure": -0.04, "contrast": 0.18, "highlights": -0.35, "shadows": 0.05, "blacks": -0.06,
                    "temperature": 0.1, "saturation": -0.22},
         "details": {"vignette": 0.28, "grain": 0.06, "grainSize": 0.2}}
G = json.dumps(GRADE).replace('"', "&quot;")
FACE = "531px 745px"      # face centre in the 1080x1920 frame

CSS = """
    @font-face { font-family: "Anton"; src: url("assets/fonts/Anton-Regular.ttf"); }
    @font-face { font-family: "Jakarta"; src: url("assets/fonts/PlusJakartaSans-Variable.ttf"); font-weight: 200 800; }
    #root { position: absolute; inset: 0; overflow: hidden; background: #0b0d10; }
    .frame { position: absolute; inset: 0; }
    .frame video, .frame img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
    .veil { position: absolute; left: 0; right: 0; bottom: 0; height: 820px;
      background: linear-gradient(to top, rgba(6, 8, 12, 0.86), rgba(6, 8, 12, 0.55) 45%, rgba(6, 8, 12, 0)); }
    .topveil { position: absolute; left: 0; right: 0; top: 0; height: 760px;
      background: linear-gradient(to bottom, rgba(6, 8, 12, 0.8), rgba(6, 8, 12, 0)); }
    .cap { position: absolute; left: 70px; right: 70px; top: 1500px; text-align: center;
      font-family: "Jakarta", sans-serif; font-weight: 800; font-size: 78px; line-height: 1.15; color: #ffffff;
      letter-spacing: -0.5px; text-shadow: 0 4px 24px rgba(0, 0, 0, 0.85), 0 1px 3px rgba(0, 0, 0, 0.7); }
    .cap .w { display: inline-block; }
    .cap .gold { color: #ffc94a; }
    .bar { position: absolute; left: 50%; top: 1460px; width: 120px; height: 8px; margin-left: -60px;
      border-radius: 4px; background: #ffc94a; box-shadow: 0 0 18px rgba(255, 201, 74, 0.7); }
"""


def words(sid, text):
    out = []
    for w in text.split():
        cls = "w %s-w" % sid
        if w.startswith("*"):
            w, cls = w[1:], cls + " gold"
        out.append('<span class="%s">%s</span>' % (cls, w))
    return " ".join(out)


def scene(sid, src, cap, motion, extra_html="", extra_js="", img=False, dur=None):
    media = ('<img id="{s}-v" class="clip" src="{src}" data-start="0" data-duration="{d}" data-color-grading="{g}" alt="client">'
             if img else
             '<video id="{s}-v" class="clip" src="{src}" data-start="0" data-duration="{d}" data-color-grading="{g}" muted playsinline></video>'
             ).format(s=sid, src=src, d=round(dur or B, 4), g=G)
    lines = "".join("<div>%s</div>" % words(sid, l) for l in cap) if cap else ""
    capjs = ""
    if cap:
        capjs = (
            'tl.fromTo("#%(s)s-bar", { scaleX: 0 }, { scaleX: 1, duration: 0.35, ease: "power3.out" }, 0.22);\n'
            '    tl.fromTo(".%(s)s-w", { opacity: 0, y: 26, filter: "blur(10px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.34, ease: "power3.out", stagger: 0.1 }, 0.3);\n'
            '    tl.to(["#%(s)s-cap", "#%(s)s-bar"], { opacity: 0, filter: "blur(6px)", duration: 0.2, ease: "power2.in" }, %(out)s);'
        ) % {"s": sid, "out": round(B - 0.24, 3)}
    return f"""<template>
  <style>{CSS}</style>
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920">
    <div id="{sid}-frame" class="frame" data-layout-allow-overflow>{media}</div>
    <div class="veil"></div>
    {'<div id="%s-bar" class="bar"></div><div id="%s-cap" class="cap">%s</div>' % (sid, sid, lines) if cap else ''}
    {extra_html}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {motion}
    {capjs}
    {extra_js}
    window.__timelines["{sid}"] = tl;
  </script>
</template>
"""


S = {}
# 1: slow-mo pickup + title (visible at t=0 for the thumbnail), exits with a zoom-through
S["s1"] = scene("s1", "assets/clips/c1.mp4", None,
    f'tl.fromTo("#s1-frame", {{ scale: 1.12, transformOrigin: "{FACE}" }}, {{ scale: 1.24, duration: {B - 0.3:.3f}, ease: "sine.inOut" }}, 0);\n'
    f'    tl.to("#s1-frame", {{ scale: 2.2, filter: "blur(14px)", duration: 0.3, ease: "power3.in" }}, {B - 0.3:.3f});',
    extra_html="""<div class="topveil"></div>
    <div id="s1-title" style="position:absolute;left:0;right:0;top:250px;text-align:center;">
      <div id="s1-boss" style="font-family:Anton;font-size:300px;line-height:0.95;color:#ffc94a;letter-spacing:6px;text-shadow:0 0 50px rgba(255,180,40,0.55),0 8px 30px rgba(0,0,0,0.8);">BOSS</div>
      <div id="s1-mode" style="font-family:Anton;font-size:104px;letter-spacing:26px;color:#fff;margin-top:6px;text-shadow:0 6px 24px rgba(0,0,0,0.85);">MODE&nbsp;<span id="s1-on" style="color:#3dff8f;text-shadow:0 0 30px rgba(61,255,143,0.8),0 6px 24px rgba(0,0,0,0.85);">ON</span></div>
    </div>""",
    extra_js=f"""tl.fromTo("#s1-boss", {{ scale: 1.08 }}, {{ scale: 1, duration: 1.4, ease: "power2.out" }}, 0);
    tl.fromTo("#s1-mode", {{ scaleX: 1.14 }}, {{ scaleX: 1, duration: 1.2, ease: "power2.out" }}, 0);
    tl.fromTo("#s1-on", {{ opacity: 1 }}, {{ opacity: 0.2, duration: 0.07, ease: "none", repeat: 5, yoyo: true }}, 1.25);
    tl.to("#s1-title", {{ scale: 1.6, opacity: 0, filter: "blur(12px)", duration: 0.3, ease: "power3.in" }}, {B - 0.3:.3f});""")

# 2: lands from the zoom-through with a small impact shake, then whips out to the left
S["s2"] = scene("s2", "assets/clips/c2.mp4", ["Har *call ke peeche..."],
    f'tl.fromTo("#s2-frame", {{ scale: 1.7, filter: "blur(12px)", transformOrigin: "{FACE}" }}, {{ scale: 1.22, filter: "blur(0px)", duration: 0.45, ease: "power3.out" }}, 0);\n'
    f'    tl.fromTo("#s2-frame", {{ x: -16, y: 10 }}, {{ x: 12, y: -8, duration: 0.06, repeat: 3, yoyo: true, ease: "none" }}, 0);\n'
    f'    tl.to("#s2-frame", {{ x: 0, y: 0, duration: 0.1, ease: "power2.out" }}, 0.24);\n'
    f'    tl.to("#s2-frame", {{ scale: 1.3, duration: {B - 0.65:.3f}, ease: "sine.inOut" }}, 0.45);\n'
    f'    tl.to("#s2-frame", {{ x: -260, filter: "blur(16px)", duration: 0.2, ease: "power3.in" }}, {B - 0.2:.3f});')
# 3: whip in from the right, medium on the face
S["s3"] = scene("s3", "assets/clips/c3.mp4", ["...ek nayi *deal"],
    f'tl.fromTo("#s3-frame", {{ x: 260, scale: 1.55, filter: "blur(16px)", transformOrigin: "{FACE}" }}, {{ x: 0, filter: "blur(0px)", duration: 0.28, ease: "power3.out" }}, 0);\n'
    f'    tl.to("#s3-frame", {{ scale: 1.66, duration: {B - 0.28:.3f}, ease: "sine.inOut" }}, 0.28);')
# 4: wide, slow lateral drift (light leak covers the cut in)
S["s4"] = scene("s4", "assets/clips/c4.mp4", ["Baat kam,", "*kaam zyada"],
    f'tl.fromTo("#s4-frame", {{ scale: 1.14, x: 30, transformOrigin: "{FACE}" }}, {{ scale: 1.2, x: -30, duration: {B - 0.25:.3f}, ease: "sine.inOut" }}, 0);\n'
    f'    tl.to("#s4-frame", {{ scale: 1.9, filter: "blur(12px)", duration: 0.25, ease: "power3.in" }}, {B - 0.25:.3f});')
# 5: punch-in close on the face
S["s5"] = scene("s5", "assets/clips/c5.mp4", ["Mehnat. Imaandari.", "*Bharosa."],
    f'tl.fromTo("#s5-frame", {{ scale: 2.1, filter: "blur(10px)", transformOrigin: "{FACE}" }}, {{ scale: 1.7, filter: "blur(0px)", duration: 0.4, ease: "power3.out" }}, 0);\n'
    f'    tl.to("#s5-frame", {{ scale: 1.78, duration: {B - 0.4:.3f}, ease: "sine.inOut" }}, 0.4);')
# 6: slow-mo hang-up; check mark pops when the handset lands (0.87 s into the clip)
S["s6"] = scene("s6", "assets/clips/c6.mp4", ["Deal *pakki."],
    f'tl.fromTo("#s6-frame", {{ scale: 1.18, transformOrigin: "490px 1240px" }}, {{ scale: 1.36, duration: {B:.3f}, ease: "sine.inOut" }}, 0);',
    extra_html="""<svg id="s6-check" viewBox="0 0 120 120" style="position:absolute;left:480px;top:1300px;width:120px;height:120px;">
      <circle cx="60" cy="60" r="54" fill="#3dff8f" opacity="0.95"/>
      <path id="s6-tick" d="M34 62 L52 80 L88 42" fill="none" stroke="#0b0d10" stroke-width="12" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="90" stroke-dashoffset="90"/></svg>""",
    extra_js="""tl.fromTo("#s6-check", { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2.4)" }, 0.9);
    tl.to("#s6-tick", { strokeDashoffset: 0, duration: 0.3, ease: "power2.out" }, 1.05);
    tl.to("#s6-check", { opacity: 0, duration: 0.2 }, %s);""" % round(B - 0.24, 3))
# end card: hero frame (on the call, smiling), slow push, title
S["fin"] = scene("fin", "assets/clips/hero.jpg", None,
    f'tl.fromTo("#fin-frame", {{ scale: 1.25, transformOrigin: "{FACE}" }}, {{ scale: 1.38, duration: {FIN}, ease: "sine.out" }}, 0);',
    img=True, dur=FIN,
    extra_html="""<div id="fin-dim" style="position:absolute;inset:0;background:rgba(6,8,12,0.35);"></div>
    <div id="fin-flash" style="position:absolute;inset:0;background:radial-gradient(circle at 50% 40%, #fffaf2, #ffe2cc 70%);"></div>
    <div id="fin-msg" style="position:absolute;left:0;right:0;top:1290px;text-align:center;">
      <div id="fin-a" style="font-family:Jakarta;font-weight:700;font-size:70px;color:#fff;text-shadow:0 4px 22px rgba(0,0,0,0.85);">Kaam hi</div>
      <div id="fin-b" style="font-family:Anton;font-size:190px;line-height:1.02;color:#ffc94a;letter-spacing:4px;text-shadow:0 0 44px rgba(255,180,40,0.5),0 8px 28px rgba(0,0,0,0.85);">PEHCHAAN</div>
      <div id="fin-c" style="font-family:Jakarta;font-weight:700;font-size:70px;color:#fff;text-shadow:0 4px 22px rgba(0,0,0,0.85);">hai.</div>
      <div id="fin-d" style="margin-top:44px;font-family:Jakarta;font-weight:600;font-size:46px;letter-spacing:6px;color:#e8e2d6;text-shadow:0 3px 14px rgba(0,0,0,0.85);">MANANA &nbsp;•&nbsp; SHUKRIYA</div>
    </div>""",
    extra_js="""tl.fromTo("#fin-flash", { opacity: 0.9 }, { opacity: 0, duration: 0.55, ease: "power2.out" }, 0);
    tl.fromTo("#fin-a", { opacity: 0, y: 24, filter: "blur(8px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.4, ease: "power3.out" }, 0.35);
    tl.fromTo("#fin-b", { opacity: 0, scale: 1.25, filter: "blur(16px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.6, ease: "power3.out" }, 0.55);
    tl.fromTo("#fin-c", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }, 0.9);
    tl.fromTo("#fin-d", { opacity: 0 }, { opacity: 1, duration: 0.6, ease: "power2.out" }, 1.4);""")

# cinematic letterbox bars over the slow-mo hang-up, sliding out as the end card arrives
BARS = """<template>
  <style>#root{position:absolute;inset:0;pointer-events:none;} .lb{position:absolute;left:0;right:0;height:150px;background:#000;}</style>
  <div id="root" data-composition-id="bars" data-width="1080" data-height="1920">
    <div id="lb-top" class="lb" style="top:0"></div><div id="lb-bot" class="lb" style="bottom:0"></div>
  </div>
  <script>
    const tl = gsap.timeline({ paused: true });
    tl.fromTo("#lb-top", { yPercent: -100 }, { yPercent: 0, duration: 0.5, ease: "power3.out" }, 0);
    tl.fromTo("#lb-bot", { yPercent: 100 }, { yPercent: 0, duration: 0.5, ease: "power3.out" }, 0);
    tl.to("#lb-top", { yPercent: -100, duration: 0.35, ease: "power3.in" }, %s);
    tl.to("#lb-bot", { yPercent: 100, duration: 0.35, ease: "power3.in" }, %s);
    window.__timelines["bars"] = tl;
  </script>
</template>
""" % (round(B - 0.1, 3), round(B - 0.1, 3))

os.makedirs("compositions", exist_ok=True)
for k, v in S.items():
    open(f"compositions/{k}.html", "w").write(v)
open("compositions/bars.html", "w").write(BARS)
leak = open("/home/user/new-startup/library/blocks/light-leak-portrait.html").read()
open("compositions/leak.html", "w").write(leak)
fl = open("/home/user/new-startup/library/blocks/flash-warm.html").read()
open("compositions/flash.html", "w").write(fl)

order = ["s1", "s2", "s3", "s4", "s5", "s6"]
divs = []
for i, k in enumerate(order):
    divs.append((k, i * B, B, 0, "graphics", 1))
divs.append(("fin", 6 * B, FIN, 0, "graphics", 1))
divs += [("leak", 3 * B - 0.6, 1.8, 1, "graphics", 4), ("flash", 5 * B - 0.2, 0.7, 2, "graphics", 4),
         ("bars", 5 * B, B + 0.25, 3, "graphics", 3)]
comp = "\n".join(
    f'      <div id="{k}" data-composition-id="{k}" data-composition-src="compositions/{k}.html" data-start="{s:.4f}" '
    f'data-duration="{d:.4f}" data-track-index="{t}" data-track-kind="{kind}" data-width="1080" data-height="1920" style="z-index: {z}"></div>'
    for k, s, d, t, kind, z in divs)

# audio: (id, src, start, duration, volume, lane, media_start, fade_out)
A = [("ring", "assets/sfx/phone-ring.wav", 0.05, 1.2, 0.5, 10, 0, 0),
     ("lift", "assets/sfx/click-soft.mp3", 1.35, 0.36, 1.2, 11, 0, 0),
     ("rise", "assets/sfx/riser.mp3", 1.3, 1.2, 0.6, 12, round(3.47 - (B - 1.3), 3), 0),
     ("hit1", "assets/sfx/impact-bass-1.mp3", B, 2.1, 0.4, 13, 0, 0),
     ("music", "assets/music/pashto-rabab-folk-bg.mp3", B, round(TOTAL - B, 3), 1.0, 14, 0, 1.6),
     ("wh1", "assets/sfx/whoosh-short.mp3", 2 * B - 0.22, 0.57, 0.8, 15, 0, 0),
     ("wh2", "assets/sfx/whoosh-short.mp3", 3 * B - 0.22, 0.57, 0.6, 15, 0, 0),
     ("wh3", "assets/sfx/whoosh-short.mp3", 4 * B - 0.22, 0.57, 0.8, 15, 0, 0),
     ("whc", "assets/sfx/whoosh-cinematic.mp3", 5 * B - 0.45, 2.0, 0.55, 16, 0, 0.4),
     ("put", "assets/sfx/click-soft.mp3", 5 * B + 0.87, 0.36, 1.4, 11, 0, 0),
     ("ping", "assets/sfx/ping.mp3", 5 * B + 0.92, 1.3, 0.55, 17, 0, 0),
     ("hit2", "assets/sfx/impact-bass-2.mp3", 6 * B, 2.59, 0.35, 12, 0, 0),
     ("spark", "assets/sfx/sparkle.mp3", 6 * B + 0.55, 1.8, 0.35, 17, 0, 0)]
aud = "\n".join(
    f'      <audio id="{i}" src="{s}" data-start="{st:.4f}" data-duration="{d}" data-volume="{v}" data-track-index="{ln}"'
    + (f' data-media-start="{ms}"' if ms else "") + (f' data-fade-out="{fo}"' if fo else "") + "></audio>"
    for i, s, st, d, v, ln, ms, fo in A)

open("index.html", "w").write(f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap-3.14.2.min.js"></script>
    <style>* {{ margin: 0; padding: 0; box-sizing: border-box; }} html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #0b0d10; }}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
{comp}
{aud}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
""")
print("total", TOTAL, "bar", round(B, 4))
