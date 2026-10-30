# Kinetic typography inside a static laptop screen (16:9, 20 s, text + music, no VO).
# Made for SkilloraClouds on 2026-10-24. Every claim is from skilloraclouds.com read in Playwright on 2026-10-24,
# except "AMD EPYC 9" and "Budget & Standard plans LIMITED", which are the client's own approved wording.
# Skills: #404 kinetic type basics (blur-to-sharp word reveals, hierarchy), #2561 word-by-word / #2560 TextPlugin
# typewriter (URL on the end screen), #3107 device stage (here a hand-built CSS laptop, camera never moves).
# Run from the project folder: assets/{img,fonts,vendor,sfx,music} must exist (see README).
import subprocess

W, H, TOTAL = 1920, 1080, 20.0
GREEN, GREEN2, DARK, INK = "#22c55e", "#16a34a", "#070b12", "#0b1220"   # site CSS: #22c55e x17, #16a34a x5 (darker: text on light UI)
SX, SY, SW, SH = 348, 108, 1224, 734                 # screen rect inside the laptop (px, root coords)


def dur(p):
    return round(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                      capture_output=True, text=True).stdout), 3)


def svg(path, size=56, stroke="#04140a", bg=GREEN):
    return (f'<svg viewBox="0 0 24 24" style="width:{size}px;height:{size}px;flex:none;"><rect width="24" height="24" rx="7" fill="{bg}"/>'
            f'<path d="{path}" stroke="{stroke}" stroke-width="1.9" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>')


ICON = {"cpu": "M8 8h8v8H8zM10 4v3M14 4v3M10 17v3M14 17v3M4 10h3M4 14h3M17 10h3M17 14h3",
        "ssd": "M5 7h14v10H5zM8 11h5M16 12h.01",
        "shield": "M12 4l7 3v5c0 4-3 7-7 8-4-1-7-4-7-8V7z",
        "chat": "M5 6h14v9h-8l-4 3v-3H5z",
        "clock": "M12 5a7 7 0 1 0 0 14a7 7 0 1 0 0-14M12 8v4l3 2",
        "search": "M10 4a6 6 0 1 0 0 12a6 6 0 1 0 0-12M15 15l5 5"}

T = []          # timeline lines
A = []          # audio: (id, file, start, volume)


def word_in(sel, t, d=0.45, y=18):
    T.append(f'tl.fromTo("{sel}", {{opacity:0, filter:"blur(14px)", y:{y}}}, {{opacity:1, filter:"blur(0px)", y:0, duration:{d}, ease:"power3.out"}}, {t:.2f});')


def out(sel, t, d=0.35, **to):
    props = ", ".join(f"{k}:{v}" for k, v in to.items())
    T.append(f'tl.to("{sel}", {{opacity:0, filter:"blur(10px)", {props + ", " if props else ""}duration:{d}, ease:"power2.in"}}, {t:.2f});')


# ---- phase 0 (0-4.2): search bar opens, the question types in word by word -------------------------------
Q = [("Lag-free", 1.35), ("Minecraft", 1.75), ("@img", 2.1), ("server", 2.4), ("chahiye?", 2.8)]
q_html = "".join(f'<img id="q{i}" class="w" src="assets/img/hero-minecraft.jpg" style="width:46px;height:46px;border-radius:12px;object-fit:cover;" alt="">'
                 if w == "@img" else f'<span id="q{i}" class="w">{w}</span>' for i, (w, _) in enumerate(Q))
T.append('tl.fromTo("#bar", {width:96, marginLeft:-48}, {width:860, marginLeft:-430, duration:0.7, ease:"power3.inOut"}, 0.45);')
T.append('tl.fromTo("#q-ph", {opacity:0}, {opacity:1, duration:0.25}, 0.6);')
T.append('tl.to("#q-ph", {opacity:0, duration:0.15}, 1.3);')
A.append(("open", "ui-open", 0.45, 0.6))
for i, (w, t) in enumerate(Q):
    word_in(f"#q{i}", t, y=10)
    A.append((f"qk{i}", "pluck", t, 0.55))
T.append('tl.to("#bar", {scale:0.97, duration:0.08, yoyo:true, repeat:1, ease:"power1.inOut"}, 3.55);')
A.append(("click", "mouse-click", 3.55, 0.9))
T.append('tl.to("#hello", {opacity:0, y:-20, duration:0.3, ease:"power2.in"}, 3.9);')
T.append('tl.to("#bar", {y:-170, scale:0.72, duration:0.55, ease:"power3.inOut"}, 3.95);')
T.append('tl.to("#bar", {opacity:0, filter:"blur(8px)", duration:0.3}, 8.0);')
A.append(("wh1", "whoosh-up-0.6s", 3.95 - 0.333 + 0.3, 0.45))

# ---- phase 1 (4.3-8.3): specs, one chip per word hit ---------------------------------------------------------
SPECS = [("AMD EPYC 9", "cpu", 4.55), ("NVMe SSD", "ssd", 5.25), ("DDoS Protection", "shield", 5.95), ("24/7 Support", "chat", 6.65)]
spec_html = "".join(
    f'<div id="sp{i}" class="chip" style="left:{90 + (i % 2) * 540}px;top:{300 + (i // 2) * 170}px;">{svg(ICON[ic], 60)}<span>{w}</span></div>'
    for i, (w, ic, _) in enumerate(SPECS))
word_in("#sp-h", 4.3, y=10)
for i, (w, ic, t) in enumerate(SPECS):
    T.append(f'tl.fromTo("#sp{i}", {{opacity:0, filter:"blur(16px)", scale:0.85, y:30}}, {{opacity:1, filter:"blur(0px)", scale:1, y:0, duration:0.5, ease:"back.out(1.8)"}}, {t:.2f});')
    A.append((f"sk{i}", "glass-tap", t, 0.5))
for i in range(4):
    out(f"#sp{i}", 8.05 + i * 0.05, y=-30)
out("#sp-h", 8.0)

# ---- phase 2 (8.4-12.4): three cards fan out from the centre --------------------------------------------------
flags = "".join(f'<img src="assets/img/{f}" style="width:62px;height:42px;border-radius:7px;object-fit:cover;" alt="">'
                for f in ("india-flag.png", "singapore-flag.png", "dubai-flag.png", "germany-flag.png"))
CARDS = [
    (f'<div class="cimg" style="background:url(assets/img/hero-minecraft.jpg) center/cover;"></div>'
     f'<div class="ct">Minecraft hosting</div><div class="cs">Java &amp; Bedrock</div><div class="cbig">from ₹20<small>/mo</small></div>', -360, -7),
    (f'<div class="cimg" style="display:flex;align-items:center;justify-content:center;gap:12px;background:#eef2f7;">{flags}</div>'
     f'<div class="ct">Servers in</div><div class="cs">India · Singapore<br>Dubai · Germany</div><div class="cbig" style="font-size:40px;">lowest ping</div>', 0, 0),
    (f'<div class="cimg" style="display:flex;align-items:center;justify-content:center;background:{INK};">{svg(ICON["clock"], 110)}</div>'
     f'<div class="ct">Instant setup</div><div class="cs">game server ready in</div><div class="cbig">&lt;60 sec</div>', 360, 7),
]
card_html = "".join(f'<div id="cd{i}" class="card">{h}</div>' for i, (h, _, _) in enumerate(CARDS))
for i, (_, x, r) in enumerate(CARDS):
    T.append(f'tl.fromTo("#cd{i}", {{opacity:0, x:0, y:80, rotation:0, scale:0.8, filter:"blur(12px)"}}, '
             f'{{opacity:1, x:{x}, y:0, rotation:{r}, scale:1, filter:"blur(0px)", duration:0.75, ease:"power3.out"}}, {8.45 + i * 0.12:.2f});')
A.append(("fan", "swish-4", 8.45 - 0.046, 0.7))
A.append(("fan2", "maximize", 8.6, 0.35))
for i in range(3):
    T.append(f'tl.to("#cd{i}", {{y:520, rotation:{(i - 1) * 14}, opacity:0, duration:0.5, ease:"power3.in"}}, {12.05 + i * 0.06:.2f});')

# ---- phase 3 (12.6-16.1): limited plans + coupon ---------------------------------------------------------------
LIM = [("Budget", 12.65), ("&amp;", 12.95), ("Standard", 13.15), ("plans", 13.5)]
lim_html = "".join(f'<span id="lm{i}" class="w">{w}</span>' for i, (w, _) in enumerate(LIM))
for i, (w, t) in enumerate(LIM):
    word_in(f"#lm{i}", t)
    A.append((f"lk{i}", "pluck", t, 0.55))
T.append('tl.fromTo("#stamp", {opacity:0, scale:2.4, rotation:-14}, {opacity:1, scale:1, rotation:-5, duration:0.32, ease:"power4.in"}, 13.9);')
T.append('tl.fromTo("#stamp", {x:-8}, {x:8, duration:0.05, repeat:5, yoyo:true, ease:"none"}, 14.22);')
T.append('tl.to("#stamp", {x:0, duration:0.05}, 14.52);')
A.append(("stamp", "confirm-1", 14.2, 0.7))
word_in("#cpn", 14.35, y=14)
A.append(("cp", "glass-tap", 14.35, 0.45))
for sel in ("#lim-row", "#stamp", "#cpn"):
    out(sel, 16.1)

# ---- phase 4 (16.35-20): dark end screen, URL types in (TextPlugin) ----------------------------------------------
T.append('tl.fromTo("#end", {opacity:0}, {opacity:1, duration:0.45, ease:"power2.out"}, 16.35);')
A.append(("wh2", "whoosh-down-0.6s", 16.35 - 0.321 + 0.2, 0.45))
T.append('tl.fromTo("#e-logo", {scale:0.3, rotation:-20, opacity:0}, {scale:1, rotation:0, opacity:1, duration:0.6, ease:"back.out(1.8)"}, 16.55);')
word_in("#e-name", 16.85)
word_in("#e-cta", 17.15)
T.append('tl.fromTo("#e-pill", {opacity:0, scale:0.7}, {opacity:1, scale:1, duration:0.35, ease:"back.out(2)"}, 17.4);')
T.append('tl.to("#e-url", {text:"skilloraclouds.com", duration:0.9, ease:"none"}, 17.6);')
A.append(("type", "typing-synth", 17.6 - 0.05, 0.4))
word_in("#e-dc", 17.9, y=10)
T.append('tl.to("#e-pill", {scale:1.05, duration:0.4, yoyo:true, repeat:1, ease:"sine.inOut"}, 18.8);')

CSS = f"""
@font-face {{ font-family: "Anton"; src: url("assets/fonts/Anton-Regular.ttf"); }}
@font-face {{ font-family: "Jakarta"; src: url("assets/fonts/PlusJakartaSans-Variable.ttf"); font-weight: 200 800; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:{DARK}; }}
#root {{ position:absolute; inset:0; overflow:hidden; font-family:Jakarta; }}
.w {{ display:inline-block; }}
#screen {{ position:absolute; left:{SX}px; top:{SY}px; width:{SW}px; height:{SH}px; overflow:hidden; background:#f5f7fb; border-radius:6px; }}
.c {{ position:absolute; left:0; right:0; text-align:center; }}
.chip {{ position:absolute; width:500px; height:136px; display:flex; align-items:center; gap:24px; padding-left:34px; background:#fff;
        border-radius:28px; box-shadow:0 14px 40px rgba(11,18,32,0.10); font-weight:800; font-size:44px; color:{INK}; }}
.card {{ position:absolute; left:{SW // 2 - 160}px; top:150px; width:320px; height:440px; background:#fff; border-radius:28px; overflow:hidden;
        box-shadow:0 24px 60px rgba(11,18,32,0.18); }}
.cimg {{ height:180px; }}
.ct {{ margin:20px 24px 0; font-weight:800; font-size:32px; color:{INK}; }}
.cs {{ margin:6px 24px 0; font-weight:600; font-size:28px; color:#6b7280; line-height:1.3; }}
.cbig {{ position:absolute; left:24px; bottom:24px; font-family:Anton; font-size:56px; color:{GREEN2}; letter-spacing:1px; }}
.cbig small {{ font-size:28px; color:#6b7280; }}
"""

html = f"""<!doctype html>
<html lang="en" data-resolution="landscape">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width={W}, height={H}">
<script src="assets/vendor/gsap-3.14.2.min.js"></script>
<script src="assets/vendor/TextPlugin.min.js"></script>
<style>{CSS}</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="{W}" data-height="{H}">
  <!-- desk scene: wall, glow, desk top -->
  <div style="position:absolute;inset:0;background:radial-gradient(ellipse 70% 60% at 50% 38%, #16241c 0%, {DARK} 70%);"></div>
  <div style="position:absolute;left:0;right:0;top:880px;bottom:0;background:linear-gradient(#1a1410, #0d0a08);"></div>
  <div style="position:absolute;left:260px;right:260px;top:875px;height:40px;background:radial-gradient(ellipse at center, rgba(0,0,0,0.75), rgba(0,0,0,0) 70%);"></div>
  <!-- laptop: lid + bezel, base, notch -->
  <div style="position:absolute;left:{SX - 22}px;top:{SY - 22}px;width:{SW + 44}px;height:{SH + 44}px;background:#0e1014;border-radius:26px 26px 6px 6px;border:2px solid #2a2e36;box-shadow:0 30px 80px rgba(0,0,0,0.6);"></div>
  <div style="position:absolute;left:{SX + SW // 2 - 5}px;top:{SY - 14}px;width:10px;height:10px;border-radius:50%;background:#1d2128;"></div>
  <div style="position:absolute;left:{SX - 120}px;top:{SY + SH + 22}px;width:{SW + 240}px;height:26px;background:linear-gradient(#c9ced6,#8b919b);border-radius:2px 2px 18px 18px;"></div>
  <div style="position:absolute;left:{SX + SW // 2 - 110}px;top:{SY + SH + 22}px;width:220px;height:9px;background:#7d838d;border-radius:0 0 10px 10px;"></div>
  <div id="screen">
    <div data-layout-ignore data-layout-allow-occlusion style="position:absolute;left:0;right:0;top:0;height:64px;display:flex;align-items:center;gap:12px;padding-left:26px;background:#fff;border-bottom:1px solid #e6e9ef;">
      <img src="assets/img/logo.png" style="width:36px;height:36px;" alt="SkilloraClouds logo">
      <span style="font-weight:800;font-size:22px;color:{INK};">Skillora<span style="color:{GREEN2};">Clouds</span></span>
      <span style="margin-left:auto;margin-right:26px;padding:6px 16px;border-radius:999px;background:#eef2f7;font-weight:600;font-size:16px;color:#6b7280;">skilloraclouds.com</span>
    </div>
    <div id="hello" class="c" style="top:150px;font-weight:800;font-size:46px;color:{INK};">Find your <span style="color:{GREEN2};">game server</span></div>
    <div id="bar" style="position:absolute;left:50%;top:300px;width:860px;height:92px;margin-left:-430px;transform-origin:50% 50%;background:#fff;border-radius:46px;box-shadow:0 18px 50px rgba(11,18,32,0.14);overflow:hidden;display:flex;align-items:center;gap:16px;padding-left:24px;white-space:nowrap;">
      {svg(ICON["search"], 46, "#ffffff", INK)}
      <span id="q-ph" style="position:absolute;left:92px;font-weight:600;font-size:34px;color:#6b7280;">Search…</span>
      <div style="display:flex;align-items:center;gap:14px;font-weight:700;font-size:38px;color:{INK};">{q_html}</div>
    </div>
    <div id="sp-h" class="c" style="top:240px;font-weight:800;font-size:30px;letter-spacing:6px;color:{GREEN2};">POWERED BY</div>
    {spec_html}
    {card_html}
    <div id="lim-row" class="c" style="top:200px;display:flex;justify-content:center;gap:22px;font-weight:800;font-size:64px;color:{INK};">{lim_html}</div>
    <div id="stamp" class="c" style="top:300px;font-family:Anton;font-size:170px;color:{GREEN2};text-shadow:0 10px 30px rgba(34,197,94,0.35);">LIMITED!</div>
    <div id="cpn" class="c" style="top:560px;"><span style="display:inline-block;padding:14px 30px;border:3px dashed {GREEN};border-radius:18px;font-weight:700;font-size:32px;color:{INK};">Premium par 10% off · code <b style="color:{GREEN2};">SKILL26</b></span></div>
    <div id="end" style="position:absolute;inset:0;background:radial-gradient(ellipse 80% 70% at 50% 40%, #12301f, {DARK} 70%);">
      <img id="e-logo" src="assets/img/logo.png" style="position:absolute;left:{SW // 2 - 80}px;top:110px;width:160px;height:160px;" alt="SkilloraClouds logo">
      <div id="e-name" class="c" style="top:300px;font-weight:800;font-size:72px;color:#fff;">Skillora<span style="color:{GREEN};">Clouds</span></div>
      <div id="e-cta" class="c" style="top:405px;font-weight:700;font-size:36px;color:#e5e7eb;">Aaj hi visit karein</div>
      <div id="e-pill" class="c" style="top:480px;"><span style="display:inline-block;min-width:520px;padding:14px 40px;border-radius:999px;background:{GREEN};font-weight:800;font-size:48px;color:#04140a;box-shadow:0 0 50px rgba(34,197,94,0.5);"><span id="e-url"></span>&#8203;</span></div>
      <div id="e-dc" class="c" style="top:610px;font-weight:600;font-size:30px;color:#9ca3af;">discord.gg/skilloraclouds</div>
    </div>
  </div>
{chr(10).join(f'  <audio id="{i}" src="assets/sfx/{f}.mp3" data-start="{max(0, round(s, 2))}" data-duration="{dur(f"assets/sfx/{f}.mp3")}" data-volume="{v}" data-track-index="{2 + n % 6}"></audio>' for n, (i, f, s, v) in enumerate(A))}
  <audio id="music" src="assets/music/music.mp3" data-start="0" data-duration="{TOTAL}" data-volume="0.55" data-track-index="1" data-fade-out="1.5"></audio>
</div>
<script>
  gsap.registerPlugin(TextPlugin);
  const tl = gsap.timeline({{ paused: true }});
  {chr(10).join("  " + l for l in T)}
  window.__timelines = window.__timelines || {{}};
  window.__timelines["main"] = tl;
</script>
</body>
</html>
"""
open("index.html", "w").write(html)
print("built", TOTAL, "s,", len(T), "tweens,", len(A), "sfx")
