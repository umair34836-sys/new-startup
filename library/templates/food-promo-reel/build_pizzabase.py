# Pizza Base PK 9:16 promo reel (free VoxCPM2 Hindi VO). Every claim/price on screen is from pizzabasepk.com, read in
# Chromium on 2026-10-25 (library/clients/pizzabasepk/site-data.md). Structure follows hosting-promo-reel/
# build_moradosolution.py: scene starts = VO line starts (assets/vo/lines.json from vs_tts.py --parts) + VO_START.
# Food photos sit on a solid #A50000 background (measured: every corner pixel), so the reel uses that red and fades
# each photo's edge into it with a radial mask.
import json, subprocess

VO_START = 0.4
BG, RED, YEL, DARK = "#A50000", "#D80101", "#F8C000", "#1a0000"   # photo bg / site button red / banner yellow
L = json.load(open("assets/vo/lines.json"))       # [[start, end], ...] per script line inside vo.wav
VO_END = VO_START + L[-1][1]
TOTAL = round(VO_END + 2.4, 2)
st = [round(VO_START + a - 0.15, 2) for a, _ in L]
st[0] = 0.0
# s1 hook, s2 daily deal, s3 super base, s4 teen ka scene, s5 new items, s6 bazuka, s7 cities, s8 end card
SCENES = [(f"s{i + 1}", st[i], st[i + 1] if i + 1 < len(st) else TOTAL) for i in range(len(st))]
W = {k: (s, e) for k, s, e in SCENES}


def dur(p):
    return round(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                      capture_output=True, text=True).stdout), 3)


def rel(i, frac):
    """time inside scene i (0-based line) at a fraction of that line's speech"""
    a, b = L[i]
    return round(max(0.05, VO_START + a + frac * (b - a) - st[i]), 2)


def d_of(k):
    s, e = W[k]
    return round(e - s, 2)


CSS = f"""
    @font-face {{ font-family: "Anton"; src: url("assets/fonts/Anton-Regular.ttf"); }}
    @font-face {{ font-family: "Pop"; src: url("assets/fonts/Poppins-ExtraBold.ttf"); font-weight: 800; }}
    @font-face {{ font-family: "Pop"; src: url("assets/fonts/Poppins-Bold.ttf"); font-weight: 700; }}
    @font-face {{ font-family: "Pop"; src: url("assets/fonts/Poppins-SemiBold.ttf"); font-weight: 600; }}
    #root {{ position: absolute; inset: 0; overflow: hidden; }}
    .c {{ position: absolute; left: 0; right: 0; text-align: center; }}
    .anton {{ font-family: Anton; letter-spacing: 2px; line-height: 0.95; }}
    .pop {{ font-family: Pop; }}
    .y {{ color: {YEL}; }}
    .sh {{ text-shadow: 0 6px 24px rgba(40,0,0,0.75); }}
    .food {{ position: absolute; -webkit-mask-image: radial-gradient(circle at 50% 50%, #000 56%, transparent 71%);
             mask-image: radial-gradient(circle at 50% 50%, #000 56%, transparent 71%); }}
    .poster {{ position: absolute; border-radius: 34px; box-shadow: 0 30px 80px rgba(30,0,0,0.65); border: 6px solid #fff; }}
    .stamp {{ position: absolute; display: flex; flex-direction: column; align-items: center; justify-content: center;
              border-radius: 50%; background: {YEL}; color: {DARK}; box-shadow: 0 16px 50px rgba(30,0,0,0.6);
              border: 8px solid #fff; font-family: Pop; font-weight: 800; }}
    .pill {{ display: inline-block; padding: 16px 44px; border-radius: 999px; background: #fff; color: {RED};
             font-family: Pop; font-weight: 800; font-size: 60px; box-shadow: 0 10px 40px rgba(30,0,0,0.45); }}
    .chip {{ position: absolute; width: 420px; height: 120px; border-radius: 26px; background: #fff; color: {RED};
             display: flex; align-items: center; justify-content: center; font-family: Pop; font-weight: 800; font-size: 56px;
             box-shadow: 0 12px 36px rgba(30,0,0,0.5); }}
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
    js += f'    tl.to("{sel}", {{ scale: 1.3, filter: "blur(16px)", opacity: 0, duration: 0.22, ease: "power3.in" }}, {d - 0.22:.2f});\n'
    return js


def stamp_js(sel, t):
    return (f'    tl.fromTo("{sel}", {{ scale: 0, rotation: -30 }}, {{ scale: 1, rotation: -8, duration: 0.45, ease: "back.out(2.6)" }}, {t});\n'
            f'    tl.to("{sel}", {{ scale: 1.06, duration: 0.4, ease: "sine.inOut", yoyo: true, repeat: 3 }}, {t + 0.5:.2f});\n')


C = {}
# global background: the photos' own red, a lighter centre glow, slow drifting yellow dots
dots = "".join(f'<div style="position:absolute;left:{(i * 397) % 1080}px;top:{(i * 613) % 1920}px;width:{8 + i % 4 * 4}px;height:{8 + i % 4 * 4}px;border-radius:50%;background:rgba(248,192,0,{0.10 + (i % 3) * 0.06});"></div>' for i in range(40))
C["bg"] = comp("bg", f"""    <div style="position:absolute;inset:0;background:{BG};"></div>
    <div id="bg-glow" style="position:absolute;left:-300px;top:260px;width:1680px;height:1400px;border-radius:50%;background:radial-gradient(circle, rgba(232,40,20,0.55), rgba(165,0,0,0) 65%);" data-layout-allow-overflow></div>
    <div id="bg-dots" style="position:absolute;inset:0;" data-layout-allow-overflow>{dots}</div>
    <div style="position:absolute;left:0;right:0;bottom:0;height:520px;background:linear-gradient(to bottom, rgba(60,0,0,0), rgba(60,0,0,0.55));"></div>""",
               f'    tl.fromTo("#bg-dots", {{ y: 0 }}, {{ y: -220, duration: {TOTAL}, ease: "none" }}, 0);\n'
               f'    tl.fromTo("#bg-glow", {{ scale: 0.9 }}, {{ scale: 1.15, duration: {TOTAL / 2:.2f}, ease: "sine.inOut", yoyo: true, repeat: 1 }}, 0);\n')

# S1 hook: on screen at t=0 (thumbnail). Pizza = Chicken Mughlai Base photo (site item 811085)
d = d_of("s1")
C["s1"] = comp("s1", f"""    <div id="s1-w" style="position:absolute;inset:0;">
      <img id="s1-pz" class="food" src="assets/img/mughlai.png" style="left:40px;top:640px;width:1000px;height:1000px;" alt="Chicken Mughlai Base pizza" data-layout-allow-overflow>
      <div class="c anton y sh" id="s1-a" style="top:300px;font-size:150px;">PIZZA KA</div>
      <div class="c anton sh" id="s1-b" style="top:450px;font-size:170px;color:#fff;">MANN HAI?</div>
      <img id="s1-logo" src="assets/img/logo.png" style="position:absolute;left:390px;top:1000px;width:300px;height:300px;border-radius:50%;box-shadow:0 14px 50px rgba(30,0,0,0.7);" alt="Pizza Base logo">
    </div>""",
               f'    tl.fromTo("#s1-pz", {{ scale: 0.92, rotation: 0 }}, {{ scale: 1.08, rotation: 40, duration: {d}, ease: "none" }}, 0);\n'
               '    tl.fromTo("#s1-b", { scale: 1.1 }, { scale: 1, duration: 0.9, ease: "power2.out" }, 0);\n'
               f'    tl.fromTo("#s1-logo", {{ scale: 0, rotation: -40 }}, {{ scale: 1, rotation: 0, duration: 0.55, ease: "back.out(2)" }}, {rel(0, 0.62)});\n'
               + enter_exit("#s1-w", d, enter=False))


def poster_scene(k, i, img, alt, top_a, top_b, price, sub, price_frac):
    d = d_of(k)
    return comp(k, f"""    <div id="{k}-w" style="position:absolute;inset:0;">
      <div class="c anton y sh" style="top:290px;font-size:110px;">{top_a}</div>
      <div class="c anton sh" style="top:400px;font-size:84px;color:#fff;">{top_b}</div>
      <img id="{k}-p" class="poster" src="assets/img/{img}" style="left:150px;top:540px;width:780px;height:780px;" alt="{alt}">
      <div class="stamp" id="{k}-s" style="left:640px;top:1080px;width:330px;height:330px;">
        <div style="font-size:44px;line-height:1;">Rs.</div><div style="font-size:{86 if len(price) > 4 else 100}px;line-height:1.05;">{price}</div>
        <div style="font-size:34px;line-height:1;">{sub}</div></div>
    </div>""",
                enter_exit(f"#{k}-w", d) +
                f'    tl.fromTo("#{k}-p", {{ scale: 0.9, rotation: -3 }}, {{ scale: 1.0, rotation: 2, duration: {d}, ease: "none" }}, 0);\n'
                + stamp_js(f"#{k}-s", rel(i, price_frac)))


# S2-S4: the client's own deal posters (item photos on the site), price as said in the VO
C["s2"] = poster_scene("s2", 1, "daily1.webp", "Daily Base Deal 1 poster", "DAILY BASE DEAL", "1 PAN PIZZA + DRINK", "650", "", 0.72)
C["s3"] = poster_scene("s3", 2, "super1.webp", "Super Base Deal 1 poster", "SUPER BASE DEAL", "2 PIZZA", "1,050", "se shuru", 0.6)
C["s4"] = poster_scene("s4", 3, "teen1.jpeg", "Teen Ka Scene Deal 1 poster", "TEEN KA SCENE", "3 PAN PIZZA", "1,299", "", 0.7)

# S5 new arrivals (hero slide "NEW PIZZA & BIHARI ROLL!"; items Bihari Roll, Crown Crust, Kabab Crust)
d = d_of("s5")
items = [("bihari.jpg", "BIHARI ROLL", 0.32), ("crown.jpeg", "CROWN CRUST", 0.58), ("kabab.png", "KABAB CRUST", 0.82)]
it_html = "".join(
    f'<div id="s5-i{n}" style="position:absolute;left:{[60, 560, 310][n]}px;top:{[560, 560, 990][n]}px;width:460px;height:470px;">'
    f'<img class="food" src="assets/img/{f}" style="left:0;top:0;width:460px;height:460px;" alt="{t.title()}">'
    f'<div class="c pop sh" style="top:380px;font-weight:800;font-size:50px;color:#fff;">{t}</div></div>'
    for n, (f, t, _) in enumerate(items))
it_js = "".join(f'    tl.fromTo("#s5-i{n}", {{ scale: 0, rotation: {[-20, 20, -10][n]} }}, {{ scale: 1, rotation: 0, duration: 0.45, ease: "back.out(2)" }}, {rel(4, f)});\n'
                for n, (*_, f) in enumerate(items))
C["s5"] = comp("s5", f"""    <div id="s5-w" style="position:absolute;inset:0;" data-layout-allow-overflow>
      <div class="c" id="s5-t" style="top:330px;"><span class="pill" style="background:{YEL};color:{DARK};font-size:84px;">NAYA AAYA HAI!</span></div>
      {it_html}
    </div>""", enter_exit("#s5-w", d) +
               '    tl.fromTo("#s5-t", { scale: 0.3, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2.4)" }, 0.08);\n' + it_js)

# S6 Bazuka Platter (hero slide "BAZUKA PLATTER One Platter. Endless Cravings."; item 811423 Rs. 2099)
d = d_of("s6")
C["s6"] = comp("s6", f"""    <div id="s6-w" style="position:absolute;inset:0;">
      <div class="c anton y sh" style="top:290px;font-size:140px;z-index:2;">BAZUKA PLATTER</div>
      <div class="c pop sh" style="top:450px;font-weight:600;font-size:52px;color:#fff;font-style:italic;z-index:2;">One Platter. Endless Cravings.</div>
      <img id="s6-p" class="food" src="assets/img/bazuka.png" style="left:40px;top:540px;width:1000px;height:1000px;" alt="Bazuka Platter" data-layout-allow-overflow>
      <div class="stamp" id="s6-s" style="left:650px;top:1020px;width:330px;height:330px;">
        <div style="font-size:44px;line-height:1;">Rs.</div><div style="font-size:86px;line-height:1.05;">2,099</div></div>
    </div>""", enter_exit("#s6-w", d) +
               f'    tl.fromTo("#s6-p", {{ scale: 0.95 }}, {{ scale: 1.12, duration: {d}, ease: "none" }}, 0);\n'
               + stamp_js("#s6-s", rel(5, 0.62)))

# S7 cities (city dropdown order on the site) + order types
d = d_of("s7")
cities = ["Attock", "Haripur", "Wah Cantt", "Hazro", "Swabi", "Nowshera"]
ch_html = "".join(f'<div class="chip" id="s7-c{n}" style="left:{90 + (n % 2) * 480}px;top:{520 + (n // 2) * 160}px;">{c}</div>' for n, c in enumerate(cities))
ch_js = "".join(f'    tl.fromTo("#s7-c{n}", {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.3, ease: "back.out(2.4)" }}, {rel(6, 0.04 + n * 0.1)});\n' for n in range(6))
C["s7"] = comp("s7", f"""    <div id="s7-w" style="position:absolute;inset:0;">
      <img id="s7-pz" class="food" src="assets/img/supreme.png" style="left:140px;top:960px;width:800px;height:800px;opacity:0.55;" alt="Chicken Supreme Base pizza" data-layout-allow-overflow>
      <div class="c anton y sh" style="top:320px;font-size:120px;">6 SHEHRON MEIN</div>
      {ch_html}
      <div class="c" id="s7-d" style="top:1040px;"><span class="pill" style="font-size:66px;">DELIVERY &amp; PICK-UP</span></div>
    </div>""", enter_exit("#s7-w", d) +
               f'    tl.fromTo("#s7-pz", {{ rotation: 0 }}, {{ rotation: -50, duration: {d}, ease: "none" }}, 0);\n' + ch_js +
               f'    tl.fromTo("#s7-d", {{ y: 60, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "power3.out" }}, {rel(6, 0.72)});\n')

# S8 end card: logo, site, phone (header/footer), WhatsApp (wa.me/923114000029 on the menu page), logo tagline
d = d_of("s8")
C["s8"] = comp("s8", f"""    <div id="s8-w" style="position:absolute;inset:0;">
      <img id="s8-logo" src="assets/img/logo.png" style="position:absolute;left:330px;top:290px;width:420px;height:420px;border-radius:50%;box-shadow:0 18px 60px rgba(30,0,0,0.7);" alt="Pizza Base logo">
      <div class="c anton y sh" id="s8-cta" style="top:760px;font-size:120px;">ABHI ORDER KAREIN</div>
      <div class="c" id="s8-url" style="top:920px;"><span class="pill" style="font-size:72px;">pizzabasepk.com</span></div>
      <div class="c pop sh" id="s8-ph" style="top:1070px;font-weight:800;font-size:62px;color:#fff;">&#9742; 051 111 121 222</div>
      <div class="c pop sh" id="s8-wa" style="top:1160px;font-weight:700;font-size:48px;color:#fff;">WhatsApp 0311 4000029</div>
    </div>""",
               '    tl.fromTo("#s8-w", { scale: 1.12, filter: "blur(14px)", opacity: 0 }, { scale: 1, filter: "blur(0px)", opacity: 1, duration: 0.3, ease: "power3.out" }, 0);\n'
               '    tl.fromTo("#s8-logo", { scale: 0.3, rotation: -25, opacity: 0 }, { scale: 1, rotation: 0, opacity: 1, duration: 0.6, ease: "back.out(1.8)" }, 0.1);\n'
               '    tl.fromTo("#s8-cta", { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: "power3.out" }, 0.3);\n'
               f'    tl.fromTo("#s8-url", {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2.2)" }}, {rel(7, 0.45)});\n'
               f'    tl.to("#s8-url", {{ scale: 1.06, duration: 0.45, ease: "sine.inOut", yoyo: true, repeat: 5 }}, {rel(7, 0.45) + 0.45:.2f});\n'
               '    tl.fromTo("#s8-ph", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.35 }, 0.7);\n'
               '    tl.fromTo("#s8-wa", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.35 }, 0.9);\n')

import os
os.makedirs("compositions", exist_ok=True)
for k, v in C.items():
    open(f"compositions/{k}.html", "w").write(v)

divs = [f'      <div id="bg" data-composition-id="bg" data-composition-src="compositions/bg.html" data-start="0" data-duration="{TOTAL}" data-track-index="0" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: 0"></div>']
for k, s, e in SCENES:
    divs.append(f'      <div id="{k}" data-composition-id="{k}" data-composition-src="compositions/{k}.html" data-start="{s}" data-duration="{round(e - s, 3)}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: 1"></div>')

sfx = lambda n: f"assets/sfx/{n}.mp3"
MUSIC_VOL = float(os.environ.get("MUSIC_VOL", "0.18"))
loud_at = round(TOTAL - 2.3, 2)
A = [("vo", "assets/vo/vo.wav", VO_START, min(dur("assets/vo/vo.wav"), TOTAL - VO_START), 1.0, 10, 0),
     ("m1", "assets/music/music.mp3", 0, loud_at, MUSIC_VOL, 11, 0),
     ("m2", "assets/music/music.mp3", loud_at, 2.3, min(1.0, MUSIC_VOL * 3), 12, loud_at)]
for i, (k, s, e) in enumerate(SCENES[1:]):
    A.append((f"wh{i}", sfx("whoosh-short"), round(max(0, s - 0.12), 2), dur(sfx("whoosh-short")), 0.45, 14 + i % 2, 0))
hits = [W["s2"][0] + rel(1, 0.72), W["s3"][0] + rel(2, 0.6), W["s4"][0] + rel(3, 0.7), W["s6"][0] + rel(5, 0.62)]
for i, t in enumerate(hits):
    A.append((f"hit{i}", sfx("impact-bass-1"), round(t, 2), dur(sfx("impact-bass-1")), 0.3, 16 + i % 2, 0))
pops = [W["s5"][0] + rel(4, f) for *_, f in items] + [W["s7"][0] + rel(6, 0.04 + n * 0.1) for n in range(6)]
for i, t in enumerate(pops):
    A.append((f"pop{i}", sfx("pop"), round(t, 2), dur(sfx("pop")), 0.45, 18 + i % 2, 0))
A += [("spk", sfx("sparkle"), round(W["s1"][0] + rel(0, 0.62), 2), dur(sfx("sparkle")), 0.35, 20, 0),
      ("spk2", sfx("sparkle"), round(W["s8"][0] + rel(7, 0.45), 2), dur(sfx("sparkle")), 0.35, 21, 0)]
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
