# PakWebHoster 9:16 Rs 200 shared-hosting promo reel (free VoxCPM2 Hindi VO, default voice). 2026-10-25.
# Based on library/templates/hosting-promo-reel/build_moradosolution.py (scene starts = VO line starts).
# Every on-screen claim is quoted from pakwebhoster.com read in Playwright on 2026-10-25 (site-data.md):
# title "Web Hosting in Pakistan from Rs. 200/mo" [/]; Starter Lite "PKR 200 /mo", "PKR 2000 / Year (2 Month Free)",
# "10 GB NVMe Storage", "Unlimited Bandwidth", "Free SSL Certificate", "Litespeed Webserver", "Realtime Malware
# Scanner", "24/7 Live Support" [/shared-hosting]; phone +923243458649 + info@pakwebhoster.com [footer].
import json, os, subprocess

VO_START = 0.4
GREEN, GREEN_D, NAVY, LIME, BG = "#2a862e", "#257629", "#1a2f3b", "#01c062", "#f0f7fd"
L = json.load(open("assets/vo/lines.json"))           # [[start, end], ...] per script line inside vo.wav
VO_END = VO_START + L[-1][1]
TOTAL = round(VO_END + 3.7, 2)   # owner asked for a 30 s reel
st = [round(VO_START + a - 0.15, 2) for a, _ in L]
st[0] = 0.0
SCENES = [(f"s{i + 1}", st[i], st[i + 1] if i + 1 < len(st) else TOTAL) for i in range(len(st))]
W = {k: (s, e) for k, s, e in SCENES}


def dur(p):
    return round(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                      capture_output=True, text=True).stdout), 3)


def rel(i, frac):
    a, b = L[i]
    return round(max(0.05, VO_START + a + frac * (b - a) - st[i]), 2)


def d_of(k):
    s, e = W[k]
    return round(e - s, 2)


CSS = f"""
    @font-face {{ font-family: "Anton"; src: url("assets/fonts/Anton-Regular.ttf"); }}
    @font-face {{ font-family: "Manrope"; src: url("assets/fonts/Manrope-Variable.ttf"); font-weight: 200 800; }}
    #root {{ position: absolute; inset: 0; overflow: hidden; }}
    .c {{ position: absolute; left: 0; right: 0; text-align: center; }}
    .anton {{ font-family: Anton; letter-spacing: 2px; line-height: 0.95; }}
    .man {{ font-family: Manrope; }}
    .g {{ color: {GREEN}; }}
    .pill {{ display: inline-block; padding: 18px 46px; border-radius: 999px; background: {GREEN}; color: #fff;
             font-family: Manrope; font-weight: 800; font-size: 58px; box-shadow: 0 14px 40px rgba(42,134,46,0.35); }}
    .card {{ border-radius: 30px; background: #fff; box-shadow: 0 20px 60px rgba(26,47,59,0.12); }}
    .logo-card {{ position:absolute; background:#fff; border-radius:40px; box-shadow:0 24px 70px rgba(26,47,59,0.15);
                  display:flex; align-items:center; justify-content:center; }}
"""


def comp(cid, html, js):
    return f"""<template>
  <style>{CSS}</style>
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


def enter_exit(sel, d, enter=True):
    js = ""
    if enter:
        js += f'    tl.fromTo("{sel}", {{ scale: 1.12, filter: "blur(14px)", opacity: 0 }}, {{ scale: 1, filter: "blur(0px)", opacity: 1, duration: 0.3, ease: "power3.out" }}, 0);\n'
    js += f'    tl.to("{sel}", {{ scale: 1.35, filter: "blur(16px)", opacity: 0, duration: 0.22, ease: "power3.in" }}, {d - 0.22:.2f});\n'
    return js


ICON = {"ssd": "M5 7h14v10H5zM8 11h5M16 12h.01", "wave": "M3 12h4l3-7 4 14 3-7h4",
        "lock": "M7 11V8a5 5 0 0 1 10 0v3M6 11h12v9H6z", "bolt": "M13 3L5 14h6l-1 7 8-11h-6z",
        "shield": "M12 4l7 3v5c0 4-3 7-7 8-4-1-7-4-7-8V7z", "chat": "M5 6h14v9h-8l-4 3v-3H5z"}


def icon(k, size=96):
    return (f'<svg viewBox="0 0 24 24" style="width:{size}px;height:{size}px;flex:none;"><rect width="24" height="24" rx="7" fill="{GREEN}"/>'
            f'<path d="{ICON[k]}" stroke="#fff" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>')


C = {}
# global background: light site colour (--color-four), soft green glows, drifting grid
C["bg"] = comp("bg", f"""    <div style="position:absolute;inset:0;background:{BG};"></div>
    <div id="bg-g1" style="position:absolute;left:420px;top:-260px;width:1000px;height:1000px;border-radius:50%;background:radial-gradient(circle, rgba(1,192,98,0.22), rgba(1,192,98,0) 70%);" data-layout-allow-overflow></div>
    <div id="bg-g2" style="position:absolute;left:-420px;top:1150px;width:1000px;height:1000px;border-radius:50%;background:radial-gradient(circle, rgba(42,134,46,0.18), rgba(42,134,46,0) 70%);" data-layout-allow-overflow></div>
    <div id="bg-grid" style="position:absolute;left:0;top:0;width:1080px;height:2200px;background-image:linear-gradient(rgba(26,47,59,0.05) 2px, transparent 2px),linear-gradient(90deg, rgba(26,47,59,0.05) 2px, transparent 2px);background-size:60px 60px;" data-layout-allow-overflow></div>""",
               f'    tl.fromTo("#bg-grid", {{ y: 0 }}, {{ y: -240, duration: {TOTAL}, ease: "none" }}, 0);\n'
               f'    tl.fromTo("#bg-g1", {{ scale: 0.9 }}, {{ scale: 1.2, duration: {TOTAL / 2:.2f}, ease: "sine.inOut", yoyo: true, repeat: 1 }}, 0);\n'
               f'    tl.fromTo("#bg-g2", {{ scale: 1.15 }}, {{ scale: 0.9, duration: {TOTAL / 2:.2f}, ease: "sine.inOut", yoyo: true, repeat: 1 }}, 0);\n')

# S1 hook (visible at 0 s for the thumbnail)
d = d_of("s1")
C["s1"] = comp("s1", f"""    <div id="s1-w" style="position:absolute;inset:0;">
      <div class="c anton" id="s1-a" style="top:560px;font-size:150px;color:{NAVY};">APNI</div>
      <div class="c anton g" id="s1-b" style="top:720px;font-size:230px;">WEBSITE</div>
      <div class="c anton" id="s1-c" style="top:970px;font-size:170px;color:{NAVY};">ONLINE</div>
      <div class="c" id="s1-d" style="top:1190px;"><span class="pill" style="font-size:72px;">laani hai?</span></div>
    </div>""",
               f'    tl.fromTo("#s1-b", {{ scale: 1.08 }}, {{ scale: 1, duration: 1.0, ease: "power2.out" }}, 0);\n'
               f'    tl.fromTo("#s1-c", {{ y: 60, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "back.out(2)" }}, {rel(0, 0.35)});\n'
               f'    tl.fromTo("#s1-d", {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2.2)" }}, {rel(0, 0.6)});\n'
               + enter_exit("#s1-w", d, enter=False))

# S2 brand: logo + site title words
d = d_of("s2")
C["s2"] = comp("s2", f"""    <div id="s2-w" style="position:absolute;inset:0;">
      <div class="logo-card" id="s2-logo" style="left:90px;top:560px;width:900px;height:250px;"><img src="assets/img/logo.png" style="width:820px;height:189px;" alt="PakWebHoster logo"></div>
      <div class="c man" id="s2-t1" style="top:900px;font-weight:800;font-size:96px;color:{NAVY};">Web Hosting</div>
      <div class="c man" id="s2-t2" style="top:1020px;font-weight:800;font-size:96px;color:{GREEN};">in Pakistan</div>
    </div>""",
               enter_exit("#s2-w", d) +
               '    tl.fromTo("#s2-logo", { scale: 0.4, rotation: -8, opacity: 0 }, { scale: 1, rotation: 0, opacity: 1, duration: 0.55, ease: "back.out(1.8)" }, 0.1);\n'
               f'    tl.fromTo("#s2-t1", {{ y: 40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "power3.out" }}, {rel(1, 0.45)});\n'
               f'    tl.fromTo("#s2-t2", {{ y: 40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "power3.out" }}, {rel(1, 0.65)});\n')


def chips_scene(key, idx, title, items, top0=560, gap=290):
    d = d_of(key)
    html = "".join(
        f'<div class="card man" id="{key}-c{i}" style="position:absolute;left:110px;top:{top0 + i * gap}px;width:860px;height:240px;display:flex;align-items:center;gap:44px;padding-left:60px;border-left:12px solid {GREEN};">'
        f'{icon(ic)}<div><div style="font-weight:700;font-size:34px;color:#4a5568;letter-spacing:5px;">{sub}</div>'
        f'<div style="font-weight:800;font-size:{fs}px;color:{NAVY};line-height:1.05;">{t}</div></div></div>'
        for i, (t, sub, ic, fs, _) in enumerate(items))
    js = "".join(f'    tl.fromTo("#{key}-c{i}", {{ x: -900, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.4, ease: "power3.out" }}, {rel(idx, f)});\n'
                 for i, (*_, f) in enumerate(items))
    C[key] = comp(key, f"""    <div id="{key}-w" style="position:absolute;inset:0;">
      <div class="c man" style="top:{top0 - 170}px;font-weight:800;font-size:56px;letter-spacing:8px;color:{GREEN};">{title}</div>
      {html}
    </div>""", enter_exit(f"#{key}-w", d) + js)
    return [W[key][0] + rel(idx, f) for *_, f in items]


pops = []
# S3 Starter Lite storage + bandwidth
pops += chips_scene("s3", 2, "STARTER LITE PLAN", [("10 GB NVMe", "STORAGE", "ssd", 84, 0.25), ("Unlimited", "BANDWIDTH", "wave", 84, 0.7)], top0=700)
# S4 SSL, LiteSpeed, malware scanner
pops += chips_scene("s4", 3, "AUR SAATH MEIN", [("Free SSL", "CERTIFICATE", "lock", 80, 0.05), ("LiteSpeed", "WEBSERVER", "bolt", 80, 0.35),
                                               ("Malware Scanner", "REALTIME", "shield", 68, 0.7)])

# S5 24/7 live support
d = d_of("s5")
C["s5"] = comp("s5", f"""    <div id="s5-w" style="position:absolute;inset:0;">
      <div id="s5-ic" style="position:absolute;left:390px;top:440px;">{icon("chat", 300)}</div>
      <div class="c anton g" id="s5-a" style="top:820px;font-size:300px;">24/7</div>
      <div class="c" id="s5-b" style="top:1160px;"><span class="pill" style="font-size:70px;background:{NAVY};">Live Support</span></div>
    </div>""",
               enter_exit("#s5-w", d) +
               '    tl.fromTo("#s5-ic", { scale: 0.3, opacity: 0, rotation: -15 }, { scale: 1, opacity: 1, rotation: 0, duration: 0.5, ease: "back.out(2)" }, 0.05);\n'
               f'    tl.fromTo("#s5-a", {{ scale: 0.3, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2.2)" }}, {rel(4, 0.2)});\n'
               f'    tl.fromTo("#s5-b", {{ y: 50, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "power3.out" }}, {rel(4, 0.55)});\n')

# S6 price (Starter Lite PKR 200 /mo; PKR 2000 / Year (2 Month Free))
d = d_of("s6")
C["s6"] = comp("s6", f"""    <div id="s6-w" style="position:absolute;inset:0;">
      <div class="c man" style="top:430px;font-weight:800;font-size:66px;color:{NAVY};">sirf</div>
      <div class="c anton g" id="s6-p" style="top:540px;font-size:270px;line-height:1;">PKR 200</div>
      <div class="c man" id="s6-m" style="top:880px;font-weight:800;font-size:84px;color:{NAVY};">/ mahina</div>
      <div class="c" id="s6-y" style="top:1080px;"><div class="card man" style="display:inline-block;padding:34px 54px;border:4px dashed {GREEN};">
        <div style="font-weight:800;font-size:64px;color:{NAVY};">PKR 2000 / Year</div>
        <div style="font-weight:800;font-size:56px;color:{GREEN};margin-top:8px;">2 Month FREE</div></div></div>
    </div>""",
               enter_exit("#s6-w", d) +
               f'    tl.fromTo("#s6-p", {{ scale: 0.2, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.45, ease: "back.out(2.4)" }}, {rel(5, 0.12)});\n'
               f'    tl.fromTo("#s6-m", {{ y: 40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "power3.out" }}, {rel(5, 0.3)});\n'
               f'    tl.fromTo("#s6-y", {{ scale: 0, opacity: 0, rotation: -6 }}, {{ scale: 1, opacity: 1, rotation: 0, duration: 0.4, ease: "back.out(2)" }}, {rel(5, 0.6)});\n')

# S7 end card
d = d_of("s7")
C["s7"] = comp("s7", f"""    <div id="s7-w" style="position:absolute;inset:0;">
      <div class="logo-card" id="s7-logo" style="left:90px;top:460px;width:900px;height:250px;"><img src="assets/img/logo.png" style="width:820px;height:189px;" alt="PakWebHoster logo"></div>
      <div class="c man" id="s7-cta" style="top:800px;font-weight:800;font-size:64px;color:{NAVY};">Aaj hi visit karein</div>
      <div class="c" id="s7-url" style="top:920px;"><span class="pill" style="font-size:78px;">pakwebhoster.com</span></div>
      <div class="c man" id="s7-ph" style="top:1120px;font-weight:700;font-size:52px;color:{NAVY};">Call / WhatsApp: +92 324 3458649</div>
    </div>""",
               '    tl.fromTo("#s7-w", { scale: 1.12, filter: "blur(14px)", opacity: 0 }, { scale: 1, filter: "blur(0px)", opacity: 1, duration: 0.3, ease: "power3.out" }, 0);\n'
               '    tl.fromTo("#s7-logo", { scale: 0.4, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.55, ease: "back.out(1.8)" }, 0.1);\n'
               '    tl.fromTo("#s7-cta", { opacity: 0 }, { opacity: 1, duration: 0.4 }, 0.4);\n'
               f'    tl.fromTo("#s7-url", {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2.2)" }}, {rel(6, 0.55)});\n'
               f'    tl.to("#s7-url", {{ scale: 1.06, duration: 0.45, ease: "sine.inOut", yoyo: true, repeat: 3 }}, {rel(6, 0.55) + 0.45:.2f});\n'
               f'    tl.fromTo("#s7-ph", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {rel(6, 0.55) + 0.5:.2f});\n')

os.makedirs("compositions", exist_ok=True)
for k, v in C.items():
    open(f"compositions/{k}.html", "w").write(v)

divs = [f'      <div id="bg" data-composition-id="bg" data-composition-src="compositions/bg.html" data-start="0" data-duration="{TOTAL}" data-track-index="0" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: 0"></div>']
for k, s, e in SCENES:
    divs.append(f'      <div id="{k}" data-composition-id="{k}" data-composition-src="compositions/{k}.html" data-start="{s}" data-duration="{round(e - s, 3)}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: 1"></div>')

sfx = lambda n: f"assets/sfx/{n}.mp3"
loud_at = round(TOTAL - 2.5, 2)
A = [("vo", "assets/vo/vo.wav", VO_START, min(dur("assets/vo/vo.wav"), TOTAL), 1.0, 10, 0),
     ("m1", "assets/music/music.mp3", 0, loud_at, 0.16, 11, 0),
     ("m2", "assets/music/music.mp3", loud_at, 2.5, 0.5, 12, loud_at),
     ("hit", sfx("impact-punch"), round(rel(0, 0.6), 2), dur(sfx("impact-punch")), 0.3, 13, 0)]
for i, (k, s, e) in enumerate(SCENES[1:]):
    A.append((f"wh{i}", sfx("whoosh-fast-0.3s"), round(max(0, s - 0.1), 2), dur(sfx("whoosh-fast-0.3s")), 0.4, 14 + i % 2, 0))
for i, t in enumerate(pops):
    A.append((f"pop{i}", sfx("pop-high"), round(t, 2), dur(sfx("pop-high")), 0.45, 16 + i % 2, 0))
A += [("cash", sfx("cash-register"), round(W["s6"][0] + rel(5, 0.12), 2), dur(sfx("cash-register")), 0.35, 18, 0),
      ("spk", sfx("sparkle"), round(W["s7"][0] + rel(6, 0.55), 2), dur(sfx("sparkle")), 0.3, 19, 0)]
aud = "\n".join(f'      <audio id="{i}" src="{s}" data-start="{a}" data-duration="{dd}" data-volume="{v}" data-track-index="{ln}"'
                + (f' data-media-start="{ms}"' if ms else "") + (' data-fade-out="1.5"' if i == "m2" else "") + "></audio>"
                for i, s, a, dd, v, ln, ms in A)
open("index.html", "w").write(f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap-3.14.2.min.js"></script>
    <style>* {{ margin: 0; padding: 0; box-sizing: border-box; }} html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: {BG}; }}</style>
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
print("built", TOTAL, SCENES)
