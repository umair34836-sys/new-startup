# SkilloraClouds 9:16 promo reel (Viraj Hindi VO). Every on-screen claim comes from skilloraclouds.com (2026-10-24).
# Scene times follow the VO alignment (take 2) shifted by VO_START.
import os, subprocess

VO_START = 0.4
TOTAL = 32.5
GREEN, GREEN2, DARK = "#22c55e", "#16a34a", "#070b12"   # site CSS: #22c55e x17, #16a34a x5
SCENES = [("s1", 0.0, 4.5), ("s2", 4.5, 6.8), ("s3", 6.8, 12.6), ("s4", 12.6, 15.7),
          ("s5", 15.7, 19.6), ("s6", 19.6, 22.6), ("s7", 22.6, 26.9), ("s8", 26.9, TOTAL)]


def dur(p):
    return round(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                      capture_output=True, text=True).stdout), 3)


CSS = f"""
    @font-face {{ font-family: "Anton"; src: url("assets/fonts/Anton-Regular.ttf"); }}
    @font-face {{ font-family: "Jakarta"; src: url("assets/fonts/PlusJakartaSans-Variable.ttf"); font-weight: 200 800; }}
    #root {{ position: absolute; inset: 0; overflow: hidden; }}
    .c {{ position: absolute; left: 0; right: 0; text-align: center; }}
    .anton {{ font-family: Anton; letter-spacing: 2px; line-height: 0.95; }}
    .jk {{ font-family: Jakarta; }}
    .g {{ color: {GREEN}; }}
    .shadow {{ text-shadow: 0 6px 30px rgba(0,0,0,0.85); }}
    .pill {{ display: inline-block; padding: 18px 44px; border-radius: 999px; background: {GREEN}; color: #04140a;
             font-family: Jakarta; font-weight: 800; font-size: 64px; box-shadow: 0 0 60px rgba(34,197,94,0.55); }}
    .card {{ border-radius: 34px; background: rgba(17,24,39,0.82); border: 2px solid rgba(34,197,94,0.45);
             box-shadow: 0 20px 60px rgba(0,0,0,0.5), 0 0 40px rgba(34,197,94,0.18); }}
"""


def comp(cid, html, js, extra_css=""):
    return f"""<template>
  <style>{CSS}{extra_css}</style>
  <div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920">
{html}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{js}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
"""


def enter_exit(cid, d, sel):
    """Scene in (blur/scale settle) and out (zoom-through)."""
    return (f'    tl.fromTo("{sel}", {{ scale: 1.12, filter: "blur(14px)", opacity: 0 }}, {{ scale: 1, filter: "blur(0px)", opacity: 1, duration: 0.3, ease: "power3.out" }}, 0);\n'
            f'    tl.to("{sel}", {{ scale: 1.35, filter: "blur(16px)", opacity: 0, duration: 0.22, ease: "power3.in" }}, {d - 0.22:.2f});\n')


C = {}
# global background: dark navy, green glow, moving grid
C["bg"] = comp("bg", f"""    <div id="bg-base" style="position:absolute;inset:0;background:radial-gradient(ellipse 80% 60% at 50% 35%, #0f2a1a 0%, {DARK} 60%);"></div>
    <div id="bg-grid" style="position:absolute;inset:-200px;background-image:linear-gradient(rgba(34,197,94,0.10) 2px, transparent 2px),linear-gradient(90deg, rgba(34,197,94,0.10) 2px, transparent 2px);background-size:90px 90px;" data-layout-allow-overflow></div>
    <div id="bg-glow" style="position:absolute;left:140px;top:500px;width:800px;height:800px;border-radius:50%;background:radial-gradient(circle, rgba(34,197,94,0.22), rgba(34,197,94,0) 70%);"></div>""",
               f'    tl.fromTo("#bg-grid", {{ y: 0 }}, {{ y: 180, duration: {TOTAL}, ease: "none" }}, 0);\n'
               f'    tl.fromTo("#bg-glow", {{ scale: 0.9, opacity: 0.7 }}, {{ scale: 1.15, opacity: 1, duration: {TOTAL / 2:.2f}, ease: "sine.inOut", yoyo: true, repeat: 1 }}, 0);\n')

# S1 hook: Minecraft art + question (visible at t=0 for the thumbnail)
d = 4.5
C["s1"] = comp("s1", f"""    <div id="s1-w" style="position:absolute;inset:0;">
      <div id="s1-img" style="position:absolute;inset:0;background:url(assets/img/hero-minecraft.jpg) center/cover;" data-layout-allow-overflow></div>
      <div style="position:absolute;inset:0;background:linear-gradient(to bottom, rgba(7,11,18,0.55), rgba(7,11,18,0.15) 35%, rgba(7,11,18,0.85) 70%, {DARK});"></div>
      <div class="c jk shadow" id="s1-a" style="top:1040px;font-weight:800;font-size:60px;color:#e5e7eb;letter-spacing:6px;">APNA KHUD KA</div>
      <div class="c anton shadow" id="s1-b" style="top:1120px;font-size:200px;color:#fff;">MINECRAFT</div>
      <div class="c anton shadow g" id="s1-c" style="top:1310px;font-size:200px;">SERVER?</div>
      <div class="c" id="s1-d" style="top:1560px;"><span class="pill">BINA LAG KE!</span></div>
    </div>""",
               f'    tl.fromTo("#s1-img", {{ scale: 1.25 }}, {{ scale: 1.4, duration: {d}, ease: "none" }}, 0);\n'
               f'    tl.fromTo("#s1-b", {{ scale: 1.08 }}, {{ scale: 1, duration: 1.2, ease: "power2.out" }}, 0);\n'
               f'    tl.fromTo("#s1-d", {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2.2)" }}, 3.0);\n'
               f'    tl.fromTo("#s1-d", {{ x: -10 }}, {{ x: 10, duration: 0.05, repeat: 5, yoyo: true, ease: "none" }}, 3.35);\n'
               f'    tl.to("#s1-d", {{ x: 0, duration: 0.05 }}, 3.65);\n'
               f'    tl.to("#s1-w", {{ scale: 1.35, filter: "blur(16px)", opacity: 0, duration: 0.22, ease: "power3.in" }}, {d - 0.22:.2f});\n')

# S2 logo reveal
d = 2.3
C["s2"] = comp("s2", f"""    <div id="s2-w" style="position:absolute;inset:0;">
      <div id="s2-ring" style="position:absolute;left:290px;top:430px;width:500px;height:500px;border-radius:50%;border:6px solid {GREEN};box-shadow:0 0 80px {GREEN};"></div>
      <img id="s2-logo" src="assets/img/logo.png" style="position:absolute;left:340px;top:480px;width:400px;height:400px;" alt="SkilloraClouds logo">
      <div class="c jk" id="s2-name" style="top:1010px;font-weight:800;font-size:110px;color:#fff;">Skillora<span class="g">Clouds</span></div>
      <div class="c jk" id="s2-tag" style="top:1160px;font-weight:600;font-size:46px;color:#9ca3af;">High Performance Gaming Without Lag</div>
    </div>""",
               enter_exit("s2", d, "#s2-w") +
               '    tl.fromTo("#s2-logo", { scale: 0.3, rotation: -25, opacity: 0 }, { scale: 1, rotation: 0, opacity: 1, duration: 0.6, ease: "back.out(1.8)" }, 0.15);\n'
               '    tl.fromTo("#s2-ring", { scale: 0.5, opacity: 0 }, { scale: 1.12, opacity: 0, duration: 1.4, ease: "power2.out" }, 0.2);\n'
               '    tl.fromTo("#s2-name", { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: "power3.out" }, 0.45);\n'
               '    tl.fromTo("#s2-tag", { opacity: 0 }, { opacity: 1, duration: 0.3 }, 0.55);\n')

# S3 specs over the real control-panel screenshot
d = 5.8
chips = [("AMD Ryzen", 0.08), ("NVMe SSD", 1.2), ("DDoS Protection", 2.64), ("24/7 Support", 4.16)]
chip_html = "".join(
    f'<div class="card jk s3-chip" id="s3-c{i}" style="position:absolute;left:{80 if i % 2 == 0 else 560}px;top:{1180 + (i // 2) * 210}px;width:440px;height:170px;display:flex;align-items:center;justify-content:center;gap:18px;font-weight:800;font-size:{48 if len(t) < 12 else 42}px;color:#fff;">'
    f'<svg viewBox="0 0 40 40" style="width:46px;height:46px;flex:none;"><circle cx="20" cy="20" r="19" fill="{GREEN}"/><path d="M11 21 L18 27 L29 14" stroke="#04140a" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>{t}</div>'
    for i, (t, _) in enumerate(chips))
chip_js = "".join(f'    tl.fromTo("#s3-c{i}", {{ scale: 0.4, opacity: 0, y: 40 }}, {{ scale: 1, opacity: 1, y: 0, duration: 0.35, ease: "back.out(2)" }}, {t});\n'
                  for i, (_, t) in enumerate(chips))
C["s3"] = comp("s3", f"""    <div id="s3-w" style="position:absolute;inset:0;">
      <div class="c jk" style="top:190px;font-weight:800;font-size:52px;letter-spacing:8px;color:{GREEN};">POWERED BY</div>
      <div id="s3-panel" class="card" style="position:absolute;left:70px;top:300px;width:940px;height:555px;overflow:hidden;padding:0;">
        <img src="assets/img/panel-console.jpg" style="width:100%;height:100%;object-fit:cover;" alt="SkilloraClouds game panel console">
      </div>
      <div class="c jk" style="top:885px;font-weight:600;font-size:38px;color:#9ca3af;">panel.skilloraclouds.com</div>
      {chip_html}
    </div>""",
               enter_exit("s3", d, "#s3-w") +
               '    tl.fromTo("#s3-panel", { rotationX: 18, y: 60 }, { rotationX: 0, y: 0, duration: 0.8, ease: "power3.out" }, 0);\n' + chip_js)

# S4 under 60 seconds (site: "Launch your game server in under 60 seconds")
d = 3.1
C["s4"] = comp("s4", f"""    <div id="s4-w" style="position:absolute;inset:0;">
      <div class="c jk" style="top:330px;font-weight:800;font-size:64px;color:#fff;letter-spacing:4px;">GAME SERVER READY</div>
      <svg id="s4-svg" viewBox="0 0 600 600" style="position:absolute;left:240px;top:520px;width:600px;height:600px;">
        <circle cx="300" cy="300" r="260" stroke="rgba(255,255,255,0.12)" stroke-width="34" fill="none"/>
        <circle id="s4-arc" cx="300" cy="300" r="260" stroke="{GREEN}" stroke-width="34" fill="none" stroke-linecap="round"
          stroke-dasharray="1634" stroke-dashoffset="1634" transform="rotate(-90 300 300)"/>
      </svg>
      <div class="c anton g" id="s4-num" style="top:640px;font-size:300px;">&lt;60</div>
      <div class="c jk" style="top:1150px;font-weight:800;font-size:56px;color:#fff;letter-spacing:10px;">SECONDS</div>
      <div class="c" id="s4-ok" style="top:1290px;"><span class="pill">INSTANT SETUP</span></div>
    </div>""",
               enter_exit("s4", d, "#s4-w") +
               '    tl.to("#s4-arc", { strokeDashoffset: 0, duration: 2.2, ease: "power2.inOut" }, 0.1);\n'
               '    tl.fromTo("#s4-num", { scale: 0.7 }, { scale: 1, duration: 0.5, ease: "back.out(2)" }, 1.15);\n'
               '    tl.fromTo("#s4-ok", { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2.2)" }, 2.55);\n')

# S5 locations (site: "Pick India, Singapore or Dubai for the lowest ping")
d = 3.9
locs = [("India", "india-flag.png", 0.1), ("Singapore", "singapore-flag.png", 0.7), ("Dubai", "dubai-flag.png", 1.26)]
loc_html = "".join(
    f'<div class="card jk" id="s5-l{i}" style="position:absolute;left:140px;top:{470 + i * 250}px;width:800px;height:200px;display:flex;align-items:center;gap:40px;padding-left:50px;font-weight:800;font-size:72px;color:#fff;">'
    f'<img src="assets/img/{f}" style="width:150px;height:100px;object-fit:cover;border-radius:14px;" alt="{n} flag">{n}</div>'
    for i, (n, f, _) in enumerate(locs))
loc_js = "".join(f'    tl.fromTo("#s5-l{i}", {{ x: 900, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.4, ease: "power3.out" }}, {t});\n'
                 for i, (_, _, t) in enumerate(locs))
C["s5"] = comp("s5", f"""    <div id="s5-w" style="position:absolute;inset:0;">
      <div class="c jk" style="top:300px;font-weight:800;font-size:64px;color:#fff;letter-spacing:4px;">SERVERS IN</div>
      {loc_html}
      <div class="c" id="s5-ping" style="top:1300px;"><span class="pill">LOWEST PING</span></div>
    </div>""",
               enter_exit("s5", d, "#s5-w") + loc_js +
               '    tl.fromTo("#s5-ping", { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2.2)" }, 2.9);\n')

# S6 price (games page: "Java & Bedrock servers from ₹20/mo")
d = 3.0
C["s6"] = comp("s6", f"""    <div id="s6-w" style="position:absolute;inset:0;">
      <div style="position:absolute;inset:0;background:url(assets/img/hero-minecraft.jpg) center/cover;filter:blur(18px) brightness(0.35);" data-layout-allow-overflow></div>
      <div class="c jk" id="s6-a" style="top:430px;font-weight:800;font-size:72px;color:#fff;letter-spacing:4px;">MINECRAFT HOSTING</div>
      <div class="c jk" style="top:530px;font-weight:600;font-size:44px;color:#9ca3af;">Java &amp; Bedrock</div>
      <div class="c jk" style="top:700px;font-weight:700;font-size:56px;color:#e5e7eb;">sirf</div>
      <div class="c anton g" id="s6-p" style="top:780px;font-size:380px;text-shadow:0 0 70px rgba(34,197,94,0.55);">₹20</div>
      <div class="c jk" id="s6-m" style="top:1190px;font-weight:800;font-size:72px;color:#fff;">/ month se shuru</div>
    </div>""",
               enter_exit("s6", d, "#s6-w") +
               '    tl.fromTo("#s6-p", { scale: 0.2, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.45, ease: "back.out(2.4)" }, 1.1);\n'
               '    tl.fromTo("#s6-m", { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.35, ease: "power3.out" }, 1.45);\n')

# S7 coupon (site banner: "Get 10% OFF on Premium Plans with code SKILL26")
d = 4.3
C["s7"] = comp("s7", f"""    <div id="s7-w" style="position:absolute;inset:0;">
      <div class="c jk" style="top:380px;font-weight:800;font-size:60px;color:#fff;letter-spacing:4px;">PREMIUM PLANS PAR</div>
      <div id="s7-card" style="position:absolute;left:140px;top:560px;width:800px;height:420px;border-radius:40px;border:8px dashed {GREEN};background:rgba(17,24,39,0.85);box-shadow:0 0 70px rgba(34,197,94,0.3);">
        <div class="c jk" style="top:60px;font-weight:700;font-size:50px;color:#9ca3af;letter-spacing:12px;">CODE</div>
        <div class="c anton" id="s7-code" style="top:140px;font-size:200px;color:#fff;">SKILL26</div>
      </div>
      <div class="c anton g" id="s7-off" style="top:1060px;font-size:260px;text-shadow:0 0 70px rgba(34,197,94,0.55);">10% OFF</div>
    </div>""",
               enter_exit("s7", d, "#s7-w") +
               '    tl.fromTo("#s7-card", { rotation: -6, scale: 0.6, opacity: 0 }, { rotation: 0, scale: 1, opacity: 1, duration: 0.5, ease: "back.out(1.8)" }, 0.2);\n'
               '    tl.fromTo("#s7-off", { scale: 0.2, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.45, ease: "back.out(2.4)" }, 3.05);\n')

# S8 end card
d = round(TOTAL - 26.9, 2)
C["s8"] = comp("s8", f"""    <div id="s8-w" style="position:absolute;inset:0;">
      <img id="s8-logo" src="assets/img/logo.png" style="position:absolute;left:390px;top:380px;width:300px;height:300px;" alt="SkilloraClouds logo">
      <div class="c jk" id="s8-name" style="top:720px;font-weight:800;font-size:100px;color:#fff;">Skillora<span class="g">Clouds</span></div>
      <div class="c jk" id="s8-cta" style="top:930px;font-weight:700;font-size:56px;color:#e5e7eb;">Aaj hi visit karein</div>
      <div class="c" id="s8-url" style="top:1040px;"><span class="pill" style="font-size:70px;">skilloraclouds.com</span></div>
      <div class="c jk" id="s8-dc" style="top:1250px;font-weight:600;font-size:44px;color:#9ca3af;">discord.gg/skilloraclouds</div>
    </div>""",
               '    tl.fromTo("#s8-w", { scale: 1.12, filter: "blur(14px)", opacity: 0 }, { scale: 1, filter: "blur(0px)", opacity: 1, duration: 0.3, ease: "power3.out" }, 0);\n'
               '    tl.fromTo("#s8-logo", { scale: 0.3, rotation: -25, opacity: 0 }, { scale: 1, rotation: 0, opacity: 1, duration: 0.6, ease: "back.out(1.8)" }, 0.1);\n'
               '    tl.fromTo("#s8-name", { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: "power3.out" }, 0.4);\n'
               '    tl.fromTo("#s8-cta", { opacity: 0 }, { opacity: 1, duration: 0.4 }, 0.7);\n'
               '    tl.fromTo("#s8-url", { scale: 0, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2.2)" }, 1.95);\n'
               '    tl.to("#s8-url", { scale: 1.06, duration: 0.45, ease: "sine.inOut", yoyo: true, repeat: 5 }, 2.4);\n'
               '    tl.fromTo("#s8-dc", { opacity: 0 }, { opacity: 1, duration: 0.4 }, 2.6);\n')

os.makedirs("compositions", exist_ok=True)
for k, v in C.items():
    open(f"compositions/{k}.html", "w").write(v)

divs = [f'      <div id="bg" data-composition-id="bg" data-composition-src="compositions/bg.html" data-start="0" data-duration="{TOTAL}" data-track-index="0" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: 0"></div>']
for k, s, e in SCENES:
    divs.append(f'      <div id="{k}" data-composition-id="{k}" data-composition-src="compositions/{k}.html" data-start="{s}" data-duration="{round(e - s, 3)}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: 1"></div>')

sfx = lambda n: f"assets/sfx/{n}.mp3"
A = [("vo", "assets/vo/vo.wav", VO_START, dur("assets/vo/vo.wav"), 1.0, 10, 0),
     ("m1", "assets/music/music.mp3", 0, 30.0, 0.16, 11, 0),
     ("m2", "assets/music/music.mp3", 30.0, 2.5, 0.5, 12, 30.0),
     ("hit", sfx("impact-bass-1"), 3.0, dur(sfx("impact-bass-1")), 0.3, 13, 0)]
for i, t in enumerate([4.38, 6.68, 12.48, 15.58, 19.48, 22.48, 26.78]):
    A.append((f"wh{i}", sfx("whoosh-short"), t, dur(sfx("whoosh-short")), 0.45, 14 + i % 2, 0))
for i, t in enumerate([6.88, 8.0, 9.44, 10.96, 15.8, 16.4, 16.96]):
    A.append((f"pop{i}", sfx("pop"), t, dur(sfx("pop")), 0.5, 16 + i % 2, 0))
A += [("spk", sfx("sparkle"), 25.65, dur(sfx("sparkle")), 0.35, 18, 0),
      ("spk2", sfx("sparkle"), 28.85, dur(sfx("sparkle")), 0.35, 19, 0)]
aud = "\n".join(f'      <audio id="{i}" src="{s}" data-start="{st}" data-duration="{d}" data-volume="{v}" data-track-index="{ln}"'
                + (f' data-media-start="{ms}"' if ms else "") + (' data-fade-out="1.5"' if i == "m2" else "") + "></audio>"
                for i, s, st, d, v, ln, ms in A)
open("index.html", "w").write(f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap-3.14.2.min.js"></script>
    <style>* {{ margin: 0; padding: 0; box-sizing: border-box; }} html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: {DARK}; }}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
{chr(10).join(divs)}
{aud}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
""")
print("built", TOTAL)
