# PakWebHoster kinetic-typography reel (9:16, 20 s, text + CC0 music, no VO). 2026-10-25.
# Every claim is from pakwebhoster.com read in Playwright on 2026-10-25 (library/clients/pakwebhoster/site-data.md):
# Starter Lite "PKR 200 /mo", "10 GB NVMe Storage", "Unlimited Bandwidth", "Free SSL Certificate", "Litespeed Webserver",
# "24/7 Live Support" [/shared-hosting]; logo tagline "FAST • SECURE • RELIABLE" [logo.png]; phone [footer].
# Skills: #404 kinetic type basics (hierarchy, words readable >= 0.5 s after they settle), word hits on the music's
# beat grid (listen.py: 139.9 BPM, first beat 0.46 s in the cut music), one SFX per hit.
import subprocess

W, H, TOTAL = 1080, 1920, 20.0
GREEN, GREEN_D, NAVY, LIME, WHITE = "#2a862e", "#257629", "#1a2f3b", "#01c062", "#ffffff"   # site CSS + logo
B0, BEAT = 0.46, 60 / 139.9


def b(n):
    return round(B0 + n * BEAT, 3)


def dur(p):
    return round(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                      capture_output=True, text=True).stdout), 3)


T, A, HTML = [], [], []


def slam(id_, text, top, size, color, t, cls="anton", rot=0, extra="", anim=True):
    HTML.append(f'<div class="mask" data-layout-allow-overflow data-layout-allow-occlusion style="top:{top}px;height:{int(size * 1.08)}px;"><div id="{id_}" class="{cls}" style="font-size:{size}px;color:{color};{extra}">{text}</div></div>')
    if anim:
        T.append(f'tl.fromTo("#{id_}", {{yPercent:105, rotation:{rot}}}, {{yPercent:0, rotation:0, duration:0.32, ease:"power4.out"}}, {t});')


def punch(sel, t, s=1.12):
    T.append(f'tl.fromTo("{sel}", {{scale:{s}}}, {{scale:1, duration:0.35, ease:"power3.out"}}, {t});')


def hide(sel, t, d=0.25):
    T.append(f'tl.to("{sel}", {{yPercent:-110, duration:{d}, ease:"power3.in"}}, {t});')


def bg(color, t):
    T.append(f'tl.set("#bgc", {{backgroundColor:"{color}"}}, {t});')


def sfx(id_, f, t, v):
    A.append((id_, f, t, v))


# ---- S1 (0 - b(7)): "APNI WEBSITE ONLINE LAANI HAI?"  visible at 0 s for the thumbnail -------------------------------
HTML.append('<div id="s1" style="position:absolute;inset:0;">')
slam("w1", "APNI", 560, 150, NAVY, 0, anim=False)
slam("w2", "WEBSITE", 720, 230, GREEN, 0, anim=False)
slam("w3", "ONLINE", 980, 190, NAVY, b(1))
slam("w4", "LAANI HAI?", 1200, 150, GREEN, b(3), cls="anton")
HTML.append('</div>')
punch("#w2", b(0), 1.08)   # w1/w2 are on screen from frame 0 (thumbnail)
sfx("i1", "impact/impact-punch", b(1), 0.45)
sfx("i2", "impact/impact-punch", b(3), 0.45)
for i, s in enumerate(["#w1", "#w2", "#w3", "#w4"]):
    hide(s, b(6.5) + i * 0.04)
sfx("wh1", "transition/whoosh-fast-0.3s", b(6.6), 0.6)

# ---- S2 (b(7) - b(13)): green flash, logo + PAK WEB HOSTER + tagline ------------------------------------------------
bg(GREEN, b(7))
HTML.append(f'''<div id="s2" style="position:absolute;inset:0;">
  <div id="logo-card" style="position:absolute;left:90px;top:520px;width:900px;height:250px;background:#fff;border-radius:40px;
       box-shadow:0 30px 80px rgba(0,0,0,0.25);display:flex;align-items:center;justify-content:center;">
    <img src="assets/img/logo.png" style="width:820px;height:189px;" alt="PakWebHoster logo"></div>
  <div class="mask" data-layout-allow-overflow data-layout-allow-occlusion style="top:880px;height:170px;"><div id="pw1" class="anton" style="font-size:160px;color:#fff;">PAK WEB</div></div>
  <div class="mask" data-layout-allow-overflow data-layout-allow-occlusion style="top:1050px;height:170px;"><div id="pw2" class="anton" style="font-size:160px;color:{NAVY};">HOSTER</div></div>
  <div id="tag" class="c man" style="top:1290px;font-weight:800;font-size:46px;letter-spacing:10px;color:#fff;">FAST &#8226; SECURE &#8226; RELIABLE</div>
</div>''')
T.append(f'tl.fromTo("#logo-card", {{scale:0.4, rotation:-8, opacity:0}}, {{scale:1, rotation:0, opacity:1, duration:0.45, ease:"back.out(1.8)"}}, {b(7)});')
T.append(f'tl.fromTo("#pw1", {{yPercent:105}}, {{yPercent:0, duration:0.3, ease:"power4.out"}}, {b(8)});')
T.append(f'tl.fromTo("#pw2", {{yPercent:105}}, {{yPercent:0, duration:0.3, ease:"power4.out"}}, {b(9)});')
T.append(f'tl.fromTo("#tag", {{opacity:0, scaleX:1.5}}, {{opacity:1, scaleX:1, duration:0.6, ease:"power3.out"}}, {b(10)});')
sfx("pop1", "pop/pop-high", b(7), 0.5)
sfx("i3", "impact/impact-punch", b(8), 0.4)
sfx("i4", "impact/impact-punch", b(9), 0.4)
T.append(f'tl.to("#s2", {{scale:1.4, opacity:0, filter:"blur(16px)", duration:0.25, ease:"power3.in"}}, {b(12.6)});')
sfx("wh2", "transition/whoosh-fast-0.3s", b(12.7), 0.6)

# ---- S3 (b(13) - b(29)): specs, one per two beats; background flips on each downbeat ------------------------------
SPECS = [("10 GB", "NVMe STORAGE", WHITE, GREEN, NAVY),
         ("UNLIMITED", "BANDWIDTH", NAVY, LIME, WHITE),
         ("FREE", "SSL CERTIFICATE", GREEN, WHITE, NAVY),
         ("LITESPEED", "WEBSERVER", WHITE, NAVY, GREEN),
         ("24/7", "LIVE SUPPORT", NAVY, LIME, WHITE)]
HTML.append('<div id="s3" style="position:absolute;inset:0;">')
for i, (big, small, bgc, c1, c2) in enumerate(SPECS):
    t = b(13 + i * 3)
    bg(bgc, t)
    size = 260 if len(big) <= 6 else 175
    HTML.append(f'<div class="mask" data-layout-allow-overflow data-layout-allow-occlusion style="top:{760 if size > 200 else 800}px;height:{int(size * 1.08)}px;"><div id="sb{i}" class="anton" style="font-size:{size}px;color:{c1};">{big}</div></div>'
                f'<div class="mask" data-layout-allow-overflow data-layout-allow-occlusion style="top:1080px;height:110px;"><div id="ss{i}" class="man" style="font-weight:800;font-size:84px;color:{c2};letter-spacing:3px;">{small}</div></div>')
    T.append(f'tl.fromTo("#sb{i}", {{yPercent:105, scale:1.25}}, {{yPercent:0, scale:1, duration:0.3, ease:"power4.out"}}, {t});')
    T.append(f'tl.fromTo("#ss{i}", {{yPercent:105}}, {{yPercent:0, duration:0.28, ease:"power4.out"}}, {b(13 + i * 3 + 1)});')
    T.append(f'tl.to(["#sb{i}","#ss{i}"], {{yPercent:-110, duration:0.2, ease:"power3.in"}}, {round(b(13 + i * 3 + 3) - 0.2, 3)});')
    sfx(f"sk{i}", "impact/impact-punch", t, 0.35)
    sfx(f"sp{i}", "ui/pluck", b(13 + i * 3 + 1), 0.6)
HTML.append('</div>')
# counter row of dots shows progress through the 5 specs
dots = "".join(f'<div id="dot{i}" style="width:22px;height:22px;border-radius:50%;background:rgba(0,0,0,0.18);"></div>' for i in range(5))
HTML.append(f'<div id="dots" style="position:absolute;left:0;right:0;top:1330px;display:flex;justify-content:center;gap:22px;opacity:0;">{dots}</div>')
T.append(f'tl.to("#dots", {{opacity:1, duration:0.2}}, {b(13)});')
for i in range(5):
    T.append(f'tl.to("#dot{i}", {{backgroundColor:"{LIME}", scale:1.3, duration:0.2}}, {b(13 + i * 3)});')
T.append(f'tl.to("#dots", {{opacity:0, duration:0.2}}, {round(b(28) - 0.2, 3)});')
sfx("wh3", "transition/whoosh-up-0.6s", round(b(28) - 0.35, 3), 0.5)

# ---- S4 (b(28) - b(37)): SIRF / PKR 200 / MAHINA + Starter Lite ------------------------------------------------------
bg(WHITE, b(28))
HTML.append(f'''<div id="s4" style="position:absolute;inset:0;">
  <div class="mask" data-layout-allow-overflow data-layout-allow-occlusion style="top:470px;height:150px;"><div id="p1" class="anton" style="font-size:140px;color:{NAVY};">SIRF</div></div>
  <div class="mask" data-layout-allow-overflow data-layout-allow-occlusion style="top:640px;height:120px;"><div id="p2" class="anton" style="font-size:110px;color:{NAVY};">PKR</div></div>
  <div class="mask" data-layout-allow-overflow data-layout-allow-occlusion style="top:740px;height:420px;"><div id="p3" class="anton" style="font-size:400px;color:{GREEN};line-height:1;">200</div></div>
  <div class="mask" data-layout-allow-overflow data-layout-allow-occlusion style="top:1170px;height:130px;"><div id="p4" class="anton" style="font-size:120px;color:{NAVY};">/ MAHINA</div></div>
  <div id="p5" class="c" style="top:1360px;"><span style="display:inline-block;padding:18px 46px;border-radius:999px;background:{GREEN};
       color:#fff;font-family:Manrope;font-weight:800;font-size:54px;">Starter Lite plan</span></div>
</div>''')
for k, n in (("p1", 28), ("p2", 29), ("p3", 30), ("p4", 31)):
    T.append(f'tl.fromTo("#{k}", {{yPercent:105}}, {{yPercent:0, duration:0.3, ease:"power4.out"}}, {b(n)});')
punch("#p3", b(30), 1.35)
T.append(f'tl.fromTo("#p3", {{rotation:-3}}, {{rotation:3, duration:0.12, yoyo:true, repeat:3, ease:"none"}}, {b(30) + 0.3:.3f});')
T.append(f'tl.to("#p3", {{rotation:0, duration:0.1}}, {b(30) + 0.8:.3f});')
T.append(f'tl.fromTo("#p5", {{scale:0, opacity:0}}, {{scale:1, opacity:1, duration:0.35, ease:"back.out(2.2)"}}, {b(32)});')
sfx("i5", "impact/impact-punch", b(28), 0.35)
sfx("i6", "impact/impact-punch", b(30), 0.55)
sfx("cash", "money/cash-register", b(32), 0.5)
T.append(f'tl.to("#s4", {{scale:0.6, opacity:0, duration:0.3, ease:"power3.in"}}, {round(b(37) - 0.3, 3)});')
sfx("wh4", "transition/whoosh-down-0.6s", round(b(37) - 0.4, 3), 0.5)

# ---- S5 (b(37) - 20): end card on green ------------------------------------------------------------------------------
bg(GREEN, b(37))
HTML.append(f'''<div id="s5" style="position:absolute;inset:0;">
  <div id="e-card" style="position:absolute;left:90px;top:470px;width:900px;height:250px;background:#fff;border-radius:40px;
       display:flex;align-items:center;justify-content:center;box-shadow:0 30px 80px rgba(0,0,0,0.25);">
    <img src="assets/img/logo.png" style="width:820px;height:189px;" alt="PakWebHoster logo"></div>
  <div id="e-cta" class="c man" style="top:820px;font-weight:800;font-size:66px;color:#fff;">Aaj hi website live karein</div>
  <div id="e-url" class="c" style="top:950px;"><span style="display:inline-block;padding:22px 56px;border-radius:999px;background:#fff;
       color:{NAVY};font-family:Manrope;font-weight:800;font-size:76px;">pakwebhoster.com</span></div>
  <div id="e-ph" class="c man" style="top:1150px;font-weight:700;font-size:50px;color:#fff;">Call / WhatsApp: +92 324 3458649</div>
</div>''')
T.append(f'tl.fromTo("#e-card", {{y:-300, opacity:0}}, {{y:0, opacity:1, duration:0.45, ease:"back.out(1.6)"}}, {b(37)});')
T.append(f'tl.fromTo("#e-cta", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.35}}, {b(38)});')
T.append(f'tl.fromTo("#e-url", {{scale:0, opacity:0}}, {{scale:1, opacity:1, duration:0.35, ease:"back.out(2.2)"}}, {b(39)});')
T.append(f'tl.to("#e-url", {{scale:1.06, duration:0.43, yoyo:true, repeat:5, ease:"sine.inOut"}}, {b(40)});')
T.append(f'tl.fromTo("#e-ph", {{opacity:0}}, {{opacity:1, duration:0.4}}, {b(40)});')
sfx("pop2", "pop/pop-high", b(39), 0.5)
sfx("spk", "magic/sparkle", b(39), 0.3)

# scene windows: each scene is visible only inside its own time (keeps hidden words out of layout checks)
WIN = {"s1": (0, b(7)), "s2": (b(7), b(13)), "s3": (b(13), b(28)), "s4": (b(28), b(37)), "s5": (b(37), TOTAL)}
PRE = []
for k, (s0, s1) in WIN.items():
    if s0 > 0:
        PRE.append(f'gsap.set("#{k}", {{visibility:"hidden"}});')
        T.append(f'tl.set("#{k}", {{visibility:"visible"}}, {s0});')
    T.append(f'tl.set("#{k}", {{visibility:"hidden"}}, {round(s1, 3)});')
for i in range(5):
    PRE.append(f'gsap.set(["#sb{i}","#ss{i}"], {{visibility:"hidden"}});')
    T.append(f'tl.set(["#sb{i}","#ss{i}"], {{visibility:"visible"}}, {b(13 + i * 3)});')
    T.append(f'tl.set(["#sb{i}","#ss{i}"], {{visibility:"hidden"}}, {b(13 + i * 3 + 3)});')
PRE.append('gsap.set("#w3", {yPercent:105}); gsap.set("#w4", {yPercent:105});')

CSS = f"""
@font-face {{ font-family: "Anton"; src: url("assets/fonts/Anton-Regular.ttf"); }}
@font-face {{ font-family: "Manrope"; src: url("assets/fonts/Manrope-Variable.ttf"); font-weight: 200 800; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:#fff; }}
#root {{ position:absolute; inset:0; overflow:hidden; }}
.mask {{ position:absolute; z-index:2; left:0; right:0; overflow:hidden; text-align:center; }}
.anton {{ font-family:Anton; letter-spacing:2px; line-height:1.0; display:inline-block; }}
.man {{ font-family:Manrope; }}
.c {{ position:absolute; left:0; right:0; text-align:center; }}
"""

html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width={W}, height={H}">
<script src="assets/vendor/gsap-3.14.2.min.js"></script>
<style>{CSS}</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="{W}" data-height="{H}">
  <div id="bgc" style="position:absolute;inset:0;background:#fff;"></div>
  <div style="position:absolute;inset:0;background:radial-gradient(ellipse 80% 55% at 50% 45%, rgba(255,255,255,0.18), rgba(0,0,0,0.10));"></div>
  {chr(10).join(HTML)}
{chr(10).join(f'  <audio id="{i}" src="assets/sfx/{f.split("/")[-1]}.mp3" data-start="{max(0, round(s, 2))}" data-duration="{dur(f"assets/sfx/{f.split('/')[-1]}.mp3")}" data-volume="{v}" data-track-index="{2 + n % 6}"></audio>' for n, (i, f, s, v) in enumerate(A))}
  <audio id="music" src="assets/music/music.mp3" data-start="0" data-duration="{TOTAL}" data-volume="0.8" data-track-index="1" data-fade-out="1.2"></audio>
</div>
<script>
  {chr(10).join("  " + l for l in PRE)}
  const tl = gsap.timeline({{ paused: true }});
  {chr(10).join("  " + l for l in T)}
  window.__timelines = window.__timelines || {{}};
  window.__timelines["main"] = tl;
</script>
</body>
</html>
"""
open("index.html", "w").write(html)
print("built", TOTAL, "s,", len(T), "tweens,", len(A), "sfx; end beat", b(41))
