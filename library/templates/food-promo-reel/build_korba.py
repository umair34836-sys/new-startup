# Korba Restaurant 9:16 promo reel (free VoxCPM2 Hindi VO). Every claim/price on screen is from
# korba-restaurant.localoria.com, crawled in Chromium on 2026-10-26 (library/clients/korba/site-data.md); prices are read
# from the menu-card photos on that site ("Rs/- EXCLUDED TAX"). Same structure as build_pizzabase.py: scene starts =
# VO line starts (assets/vo/lines.json from vs_tts.py --parts) + VO_START. Visuals are ONLY the site's own photos.
# The site's photos are phone shots on varied backgrounds (not one solid colour like Pizza Base), so each scene puts its
# photo in a white-border card over a blurred, darkened copy of the same photo (<name>_bg.jpg, made with ffmpeg: a
# separate file, because the same src twice in one scene triggers lint duplicate_media_discovery_risk).
import json, os, subprocess

VO_START = 0.4
# menu card red / yellow label: medians of the menu-7 photo pixels, measured 2026-10-26
RED, YEL, DARK = "#751c1a", "#d3cd23", "#1a0505"
L = json.load(open("assets/vo/lines.json"))
VO_END = VO_START + L[-1][1]
TOTAL = round(VO_END + 2.4, 2)
st = [round(VO_START + a - 0.15, 2) for a, _ in L]
st[0] = 0.0
# s1 hook, s2 fish angara, s3 bbq platter, s4 mix tawa, s5 soup/salad/tea, s6 family+parking, s7 address, s8 end card
SCENES = [(f"s{i + 1}", st[i], st[i + 1] if i + 1 < len(st) else TOTAL) for i in range(len(st))]
W = {k: (s, e) for k, s, e in SCENES}
# fraction of each line's speech where its key word (price / item) is said; refined from Whisper word times if present
FR = json.load(open("assets/vo/fracs.json")) if os.path.exists("assets/vo/fracs.json") else {}


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
    @font-face {{ font-family: "Pop"; src: url("assets/fonts/Poppins-ExtraBold.ttf"); font-weight: 800; }}
    @font-face {{ font-family: "Pop"; src: url("assets/fonts/Poppins-Bold.ttf"); font-weight: 700; }}
    @font-face {{ font-family: "Pop"; src: url("assets/fonts/Poppins-SemiBold.ttf"); font-weight: 600; }}
    #root {{ position: absolute; inset: 0; overflow: hidden; }}
    .c {{ position: absolute; left: 0; right: 0; text-align: center; }}
    .anton {{ font-family: Anton; letter-spacing: 2px; line-height: 0.95; }}
    .pop {{ font-family: Pop; }}
    .y {{ color: {YEL}; }}
    .sh {{ text-shadow: 0 6px 24px rgba(20,0,0,0.85); }}
    .bgimg {{ position: absolute; left: -60px; top: -60px; width: 1200px; height: 2040px; object-fit: cover; }}
    .veil {{ position: absolute; inset: 0; background: linear-gradient(to bottom, rgba(117,28,26,0.55), rgba(117,28,26,0.25) 40%, rgba(40,5,5,0.75)); }}
    .card {{ position: absolute; object-fit: cover; border-radius: 34px; border: 6px solid #fff;
             box-shadow: 0 30px 80px rgba(20,0,0,0.7); }}
    .stamp {{ position: absolute; display: flex; flex-direction: column; align-items: center; justify-content: center;
              border-radius: 50%; background: {YEL}; color: {DARK}; box-shadow: 0 16px 50px rgba(20,0,0,0.6);
              border: 8px solid #fff; font-family: Pop; font-weight: 800; }}
    .pill {{ display: inline-block; padding: 16px 44px; border-radius: 999px; background: #fff; color: {RED};
             font-family: Pop; font-weight: 800; font-size: 60px; box-shadow: 0 10px 40px rgba(20,0,0,0.45); }}
    .tax {{ position: absolute; left: 0; right: 0; bottom: 120px; text-align: center; font-family: Pop; font-weight: 600;
            font-size: 34px; color: rgba(255,255,255,0.85); }}
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


def bg(k, img):
    return (f'    <img class="bgimg" id="{k}-bg" src="assets/img/{img.rsplit('.', 1)[0]}_bg.jpg" alt="" data-layout-allow-overflow>\n'
            f'    <div class="veil"></div>\n')


def bg_js(k, d):
    return f'    tl.fromTo("#{k}-bg", {{ scale: 1.0 }}, {{ scale: 1.12, duration: {d}, ease: "none" }}, 0);\n'


def enter_exit(sel, d, enter=True):
    js = ""
    if enter:
        js += f'    tl.fromTo("{sel}", {{ scale: 1.12, filter: "blur(14px)", opacity: 0 }}, {{ scale: 1, filter: "blur(0px)", opacity: 1, duration: 0.3, ease: "power3.out" }}, 0);\n'
    js += f'    tl.to("{sel}", {{ scale: 1.3, filter: "blur(16px)", opacity: 0, duration: 0.22, ease: "power3.in" }}, {d - 0.22:.2f});\n'
    return js


def stamp_js(sel, t):
    return (f'    tl.fromTo("{sel}", {{ scale: 0, rotation: -30 }}, {{ scale: 1, rotation: -8, duration: 0.45, ease: "back.out(2.6)" }}, {t});\n'
            f'    tl.to("{sel}", {{ scale: 1.06, duration: 0.4, ease: "sine.inOut", yoyo: true, repeat: 3 }}, {t + 0.5:.2f});\n')


def stamp(k, price, sub, left=640, top=1180, size=330):
    return (f'      <div class="stamp" id="{k}-s" style="left:{left}px;top:{top}px;width:{size}px;height:{size}px;">\n'
            f'        <div style="font-size:44px;line-height:1;">Rs.</div><div style="font-size:{86 if len(price) > 4 else 100}px;line-height:1.05;">{price}</div>\n'
            f'        <div style="font-size:34px;line-height:1;">{sub}</div></div>\n')


f = lambda i, dflt: FR.get(str(i), dflt)
C = {}

# S1 hook (on screen at t=0 = thumbnail): night exterior photo (llphoto-1), name + river-view line, logo pop
d = d_of("s1")
C["s1"] = comp("s1", bg("s1", "p1.jpg") + f"""    <div id="s1-w" style="position:absolute;inset:0;">
      <div class="c anton y sh" style="top:250px;font-size:120px;">NOWSHERA KA</div>
      <div class="c anton sh" style="top:380px;font-size:150px;color:#fff;">KORBA</div>
      <div class="c anton sh" style="top:530px;font-size:96px;color:#fff;">RESTAURANT</div>
      <img id="s1-p" class="card" src="assets/img/p1.jpg" style="left:60px;top:700px;width:960px;height:540px;" alt="Korba Restaurant at night">
      <div class="c" id="s1-r" style="top:1310px;"><span class="pill" style="font-size:52px;">Kabul Dariya ka nazara</span></div>
      <img id="s1-logo" src="assets/img/logo.png" style="position:absolute;left:400px;top:1460px;width:280px;height:auto;" alt="Korba emblem">
    </div>""",
               bg_js("s1", d) +
               f'    tl.fromTo("#s1-p", {{ scale: 1.0 }}, {{ scale: 1.06, duration: {d}, ease: "none" }}, 0);\n'
               # title stays visible at t=0 (first frame = thumbnail): only a scale settle, no fade-in
               '    tl.fromTo("#s1-w .anton", { scale: 1.15 }, { scale: 1, duration: 0.5, stagger: 0.1, ease: "power3.out" }, 0);\n'
               f'    tl.fromTo("#s1-r", {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2.2)" }}, {rel(0, f(0, 0.25))});\n'
               f'    tl.fromTo("#s1-logo", {{ scale: 0, rotation: -40 }}, {{ scale: 1, rotation: 0, duration: 0.55, ease: "back.out(2)" }}, {rel(0, f("0b", 0.75))});\n'
               + enter_exit("#s1-w", d, enter=False))

# S2 Fish Angara (menu-6: "Fish Angara Grilled, Local Fish ... 1400/-", Urdu (فی کلو) = per kilo); photos llphoto-5 + 7
d = d_of("s2")
C["s2"] = comp("s2", bg("s2", "p5.jpg") + f"""    <div id="s2-w" style="position:absolute;inset:0;">
      <div class="c anton y sh" style="top:230px;font-size:130px;">FISH ANGARA</div>
      <div class="c pop sh" style="top:380px;font-weight:700;font-size:54px;color:#fff;">Korba Special</div>
      <img id="s2-p" class="card" src="assets/img/p5.jpg" style="left:110px;top:500px;width:640px;height:853px;" alt="Fish angara on foil">
      <img id="s2-q" class="card" src="assets/img/p7.jpg" style="left:520px;top:1090px;width:500px;height:375px;" alt="Fried fish with lemon">
      {stamp("s2", "1400", "per kg", left=650, top=470, size=320)}
      <div class="tax">Prices + tax (menu card)</div>
    </div>""",
               bg_js("s2", d) + enter_exit("#s2-w", d) +
               f'    tl.fromTo("#s2-p", {{ scale: 0.94, rotation: -3 }}, {{ scale: 1.02, rotation: 1, duration: {d}, ease: "none" }}, 0);\n'
               f'    tl.fromTo("#s2-q", {{ x: 600, rotation: 12 }}, {{ x: 0, rotation: 4, duration: 0.5, ease: "power3.out" }}, {rel(1, 0.3)});\n'
               + stamp_js("#s2-s", rel(1, f(1, 0.72))))

# S3 Korba Special BBQ Platter (Full) (4-5 Person) 8000/- (menu-6); menu-card crop + llphoto-6
d = d_of("s3")
C["s3"] = comp("s3", bg("s3", "p6.jpg") + f"""    <div id="s3-w" style="position:absolute;inset:0;">
      <div class="c anton y sh" style="top:220px;font-size:116px;">KORBA SPECIAL</div>
      <div class="c anton sh" style="top:340px;font-size:116px;color:#fff;">BBQ PLATTER</div>
      <img id="s3-p" class="card" src="assets/img/p6.jpg" style="left:90px;top:500px;width:520px;height:924px;" alt="Fish and tikka plate">
      <img id="s3-m" class="card" src="assets/img/platter.jpg" style="left:150px;top:1460px;width:780px;height:205px;object-fit:cover;" alt="Menu card: Korba Special Platter">
      <div class="c" id="s3-n" style="top:560px;left:560px;"><span class="pill" style="font-size:52px;">4-5 Person</span></div>
      {stamp("s3", "8000", "Full", left=650, top=860, size=330)}
      <div class="tax" style="bottom:60px;">Prices + tax (menu card)</div>
    </div>""",
               bg_js("s3", d) + enter_exit("#s3-w", d) +
               f'    tl.fromTo("#s3-p", {{ scale: 0.95, rotation: 2 }}, {{ scale: 1.03, rotation: -1, duration: {d}, ease: "none" }}, 0);\n'
               f'    tl.fromTo("#s3-m", {{ y: 300, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.45, ease: "power3.out" }}, 0.25);\n'
               f'    tl.fromTo("#s3-n", {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2.4)" }}, {rel(2, f("2b", 0.5))});\n'
               + stamp_js("#s3-s", rel(2, f(2, 0.82))))

# S4 Mix Tawa 8 Person 8000/- (menu-7): the menu card section itself is the visual
d = d_of("s4")
C["s4"] = comp("s4", bg("s4", "tawa.jpg") + f"""    <div id="s4-w" style="position:absolute;inset:0;">
      <div class="c anton y sh" style="top:250px;font-size:150px;">BARA GROUP?</div>
      <div class="c anton sh" style="top:410px;font-size:120px;color:#fff;">MIX TAWA</div>
      <img id="s4-m" class="card" src="assets/img/tawa.jpg" style="left:60px;top:620px;width:960px;height:462px;" alt="Menu card: Mix Tawa 8 Person">
      <div class="c" id="s4-n" style="top:1180px;"><span class="pill" style="font-size:64px;">8 Person</span></div>
      {stamp("s4", "8000", "", left=375, top=1330, size=330)}
      <div class="tax" style="bottom:70px;">Prices + tax (menu card)</div>
    </div>""",
               bg_js("s4", d) + enter_exit("#s4-w", d) +
               f'    tl.fromTo("#s4-m", {{ scale: 0.92 }}, {{ scale: 1.04, duration: {d}, ease: "none" }}, 0);\n'
               f'    tl.fromTo("#s4-n", {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2.4)" }}, {rel(3, f("3b", 0.5))});\n'
               + stamp_js("#s4-s", rel(3, f(3, 0.82))))

# S5 soup, salad, green tea (full-menu text: soups, salad platters, green tea): llphoto-3, -8, -9 pop on their words
d = d_of("s5")
items = [("p3.jpg", "SOUP", f("4a", 0.2), 60, 470, -8), ("p8.jpg", "SALAD", f("4b", 0.5), 560, 760, 7), ("p9.jpg", "GREEN TEA", f("4c", 0.8), 140, 1150, -4)]
it_html = "".join(
    f'<div id="s5-i{n}" style="position:absolute;left:{x}px;top:{y}px;width:460px;height:560px;">'
    f'<img class="card" src="assets/img/{img}" style="left:0;top:0;width:460px;height:460px;" alt="{t.title()}">'
    f'<div class="c pop sh" style="top:470px;font-weight:800;font-size:54px;color:#fff;">{t}</div></div>'
    for n, (img, t, _, x, y, r) in enumerate(items))
it_js = "".join(f'    tl.fromTo("#s5-i{n}", {{ scale: 0, rotation: {r * 3} }}, {{ scale: 1, rotation: {r}, duration: 0.45, ease: "back.out(2)" }}, {rel(4, fr)});\n'
                for n, (_, _, fr, _, _, r) in enumerate(items))
C["s5"] = comp("s5", bg("s5", "p8.jpg") + f"""    <div id="s5-w" style="position:absolute;inset:0;" data-layout-allow-overflow>
      <div class="c anton y sh" id="s5-t" style="top:250px;font-size:130px;">GARMA GARAM!</div>
      {it_html}
    </div>""", bg_js("s5", d) + enter_exit("#s5-w", d) +
               '    tl.fromTo("#s5-t", { scale: 0.3, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2.4)" }, 0.08);\n' + it_js)

# S6 family area + free parking (home: separate areas for men and women; "Free parking lot"): llphoto-4 (credit kept)
d = d_of("s6")
C["s6"] = comp("s6", bg("s6", "p4.jpg") + f"""    <div id="s6-w" style="position:absolute;inset:0;">
      <img id="s6-p" class="card" src="assets/img/p4.jpg" style="left:150px;top:260px;width:780px;height:1040px;" alt="Korba entrance at night">
      <div class="c" id="s6-a" style="top:1360px;"><span class="pill" style="font-size:66px;">FAMILY AREA</span></div>
      <div class="c" id="s6-b" style="top:1510px;"><span class="pill" style="font-size:66px;background:{YEL};color:{DARK};">FREE PARKING</span></div>
    </div>""", bg_js("s6", d) + enter_exit("#s6-w", d) +
               f'    tl.fromTo("#s6-p", {{ scale: 1.0 }}, {{ scale: 1.07, duration: {d}, ease: "none" }}, 0);\n'
               f'    tl.fromTo("#s6-a", {{ x: -900 }}, {{ x: 0, duration: 0.45, ease: "power3.out" }}, {rel(5, f("5a", 0.1))});\n'
               f'    tl.fromTo("#s6-b", {{ x: 900 }}, {{ x: 0, duration: 0.45, ease: "power3.out" }}, {rel(5, f("5b", 0.7))});\n')

# S7 address (home: "2X49V6Q, GT Rd, Khat Kalay, Nowshera, Pakistan")
d = d_of("s7")
C["s7"] = comp("s7", bg("s7", "p1.jpg") + f"""    <div id="s7-w" style="position:absolute;inset:0;">
      <div class="c" id="s7-pin" style="top:520px;font-size:200px;line-height:1;">&#128205;</div>
      <div class="c anton y sh" id="s7-a" style="top:800px;font-size:130px;">GT ROAD</div>
      <div class="c anton sh" id="s7-b" style="top:950px;font-size:120px;color:#fff;">KHAT KALAY</div>
      <div class="c" id="s7-c" style="top:1110px;"><span class="pill" style="font-size:72px;">NOWSHERA</span></div>
    </div>""", bg_js("s7", d) + enter_exit("#s7-w", d) +
               '    tl.fromTo("#s7-pin", { y: -500 }, { y: 0, duration: 0.5, ease: "bounce.out" }, 0.05);\n'
               f'    tl.fromTo("#s7-a", {{ x: -900 }}, {{ x: 0, duration: 0.4, ease: "power3.out" }}, {rel(6, 0.05)});\n'
               f'    tl.fromTo("#s7-b", {{ x: 900 }}, {{ x: 0, duration: 0.4, ease: "power3.out" }}, {rel(6, 0.35)});\n'
               f'    tl.fromTo("#s7-c", {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2.2)" }}, {rel(6, 0.7)});\n')

# S8 end card: emblem (Ramadan flyer), phones (site text + menu cards; WhatsApp icon beside 0333 on the flyer), facebook
d = d_of("s8")
C["s8"] = comp("s8", f"""    <div style="position:absolute;inset:0;background:radial-gradient(circle at 50% 40%, #9a2a25, {RED} 55%, #3a0b0a);"></div>
    <div id="s8-w" style="position:absolute;inset:0;">
      <img id="s8-logo" src="assets/img/logo.png" style="position:absolute;left:340px;top:250px;width:400px;height:auto;" alt="Korba emblem">
      <div class="c anton sh" style="top:700px;font-size:110px;color:#fff;">KORBA RESTAURANT</div>
      <div class="c anton y sh" id="s8-cta" style="top:850px;font-size:120px;">ABHI CALL KAREIN</div>
      <div class="c" id="s8-ph" style="top:1030px;"><span class="pill" style="font-size:76px;">0333 3443313</span></div>
      <div class="c pop sh" id="s8-wa" style="top:1190px;font-weight:700;font-size:48px;color:#fff;">WhatsApp 0333 3443313</div>
      <div class="c pop sh" id="s8-p2" style="top:1270px;font-weight:700;font-size:48px;color:#fff;">0315 9403090 &#183; 0923 560131</div>
      <div class="c pop sh" id="s8-fb" style="top:1360px;font-weight:600;font-size:44px;color:{YEL};">facebook.com/korba.nsr</div>
      <div class="c pop sh" style="top:1440px;font-weight:600;font-size:40px;color:rgba(255,255,255,0.85);">GT Road, Khat Kalay, Nowshera</div>
    </div>""",
               '    tl.fromTo("#s8-w", { scale: 1.12, filter: "blur(14px)", opacity: 0 }, { scale: 1, filter: "blur(0px)", opacity: 1, duration: 0.3, ease: "power3.out" }, 0);\n'
               '    tl.fromTo("#s8-logo", { scale: 0.3, rotation: -25, opacity: 0 }, { scale: 1, rotation: 0, opacity: 1, duration: 0.6, ease: "back.out(1.8)" }, 0.1);\n'
               '    tl.fromTo("#s8-cta", { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: "power3.out" }, 0.3);\n'
               f'    tl.fromTo("#s8-ph", {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2.2)" }}, {rel(7, 0.3)});\n'
               f'    tl.to("#s8-ph", {{ scale: 1.06, duration: 0.45, ease: "sine.inOut", yoyo: true, repeat: 5 }}, {rel(7, 0.3) + 0.45:.2f});\n'
               '    tl.fromTo("#s8-wa, #s8-p2, #s8-fb", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.35, stagger: 0.15 }, 0.7);\n')

os.makedirs("compositions", exist_ok=True)
for k, v in C.items():
    open(f"compositions/{k}.html", "w").write(v)

divs = [f'      <div id="bgc" style="position:absolute;inset:0;background:{RED};z-index:0"></div>']
for k, s, e in SCENES:
    divs.append(f'      <div id="{k}" data-composition-id="{k}" data-composition-src="compositions/{k}.html" data-start="{s}" data-duration="{round(e - s, 3)}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: 1"></div>')

sfx = lambda n: f"assets/sfx/{n}.mp3"
MUSIC_VOL = float(os.environ.get("MUSIC_VOL", "0.18"))
MUSIC_IN = 26.8   # listen.py 2026-10-26: Breaking Bollywood first drop/chorus section starts at 26.8 s
loud_at = round(TOTAL - 2.3, 2)
A = [("vo", "assets/vo/vo.wav", VO_START, min(dur("assets/vo/vo.wav"), TOTAL - VO_START), 1.0, 10, 0),
     ("m1", "assets/music/music.mp3", 0, loud_at, MUSIC_VOL, 11, MUSIC_IN),
     ("m2", "assets/music/music.mp3", loud_at, 2.3, min(1.0, MUSIC_VOL * 3), 12, round(MUSIC_IN + loud_at, 2))]
for i, (k, s, e) in enumerate(SCENES[1:]):
    A.append((f"wh{i}", sfx("whoosh"), round(max(0, s - 0.1), 2), dur(sfx("whoosh")), 0.6, 14 + i % 2, 0))
hits = [W["s2"][0] + rel(1, f(1, 0.72)), W["s3"][0] + rel(2, f(2, 0.82)), W["s4"][0] + rel(3, f(3, 0.82))]
for i, t in enumerate(hits):
    A.append((f"hit{i}", sfx("hit"), round(t, 2), dur(sfx("hit")), 0.35, 16 + i % 2, 0))
pops = [W["s5"][0] + rel(4, fr) for _, _, fr, *_ in items] + [W["s3"][0] + rel(2, f("2b", 0.5)), W["s4"][0] + rel(3, f("3b", 0.5))]
for i, t in enumerate(pops):
    A.append((f"pop{i}", sfx("pop"), round(t, 2), dur(sfx("pop")), 0.5, 18 + i % 2, 0))
A += [("spk", sfx("sparkle"), round(rel(0, f("0b", 0.75)), 2), dur(sfx("sparkle")), 0.35, 20, 0),
      ("spk2", sfx("sparkle"), round(W["s8"][0] + rel(7, 0.3), 2), dur(sfx("sparkle")), 0.35, 21, 0)]
aud = "\n".join(f'      <audio id="{i}" src="{s}" data-start="{a}" data-duration="{dd}" data-volume="{v}" data-track-index="{ln}"'
                + (f' data-media-start="{ms}"' if ms else "") + (' data-fade-out="1.5"' if i == "m2" else "") + "></audio>"
                for i, s, a, dd, v, ln, ms in A)
open("index.html", "w").write(f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap-3.14.2.min.js"></script>
    <style>* {{ margin: 0; padding: 0; box-sizing: border-box; }} html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: {RED}; }}</style>
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
