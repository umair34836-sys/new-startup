# MoradoSolution WELCOME30 offer reel (9:16). Every claim is quoted from moradosolution.in, crawl 2026-10-24
# (library/clients/moradosolution/site-data.md): /sales "WELCOME30 30% OFF" on 13 Minecraft + 4 Hytale plans;
# /minecraft-budget Starter ₹199 -> ₹139 (2 GB, 6 GB NVMe), Gold POPULAR ₹699 -> ₹489 (10 GB, 30 GB NVMe),
# "Codes apply automatically when you tap Buy Now — or paste them at checkout.", "Deploy your Minecraft server in
# minutes.", "All plans include DDoS protection", AMD EPYC 7C13, NVMe. Scene starts follow the VO line starts
# (assets/vo/lines.json from vs_tts.py --parts), shifted by VO_START.
import json, os, subprocess

VO_START = 0.35
RED, BLUE, DARK = "#e11d48", "#3b82f6", "#050505"   # site CSS --bg #050505; logo red / blue accents
L = json.load(open("assets/vo/lines.json"))
VO_FILE = "assets/vo/vo.wav"
VO_END = VO_START + L[-1][1]
TOTAL = round(VO_END + 3.0, 2)
st = [round(VO_START + a - 0.15, 2) for a, _ in L]
st[0] = 0.0
SCENES = [(f"s{i + 1}", st[i], st[i + 1] if i + 1 < len(st) else TOTAL) for i in range(len(st))]
W = {k: (s, e) for k, s, e in SCENES}
MUSIC_IN = 23.85   # listen.py: Bollywood Groove 161.5 BPM, drop/chorus 23.6-48.8 s, downbeat ~23.85 s


def dur(p):
    return round(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                      capture_output=True, text=True).stdout), 3)


def rel(i, frac):
    """time inside scene i at a fraction of VO line i"""
    a, b = L[i]
    return round(max(0.05, VO_START + a + frac * (b - a) - st[i]), 2)


def d_of(k):
    s, e = W[k]
    return round(e - s, 2)


CSS = f"""
    @font-face {{ font-family: "Anton"; src: url("assets/fonts/Anton-Regular.ttf"); }}
    @font-face {{ font-family: "Grotesk"; src: url("assets/fonts/SpaceGrotesk-Variable.ttf"); font-weight: 300 700; }}
    #root {{ position: absolute; inset: 0; overflow: hidden; }}
    .c {{ position: absolute; left: 64px; right: 64px; text-align: center; }}
    .anton {{ font-family: Anton; letter-spacing: 2px; line-height: 0.95; }}
    .gr {{ font-family: Grotesk; }}
    .r {{ color: {RED}; }}
    .shadow {{ text-shadow: 0 6px 30px rgba(0,0,0,0.85); }}
    .pill {{ display: inline-block; padding: 18px 46px; border-radius: 999px; background: #fff; color: {DARK};
             font-family: Grotesk; font-weight: 700; font-size: 56px; }}
    .pill.red {{ background: {RED}; color: #fff; box-shadow: 0 0 60px rgba(225,29,72,0.55); }}
    .card {{ border-radius: 30px; background: rgba(18,18,21,0.94); border: 2px solid rgba(255,255,255,0.14);
             box-shadow: 0 20px 60px rgba(0,0,0,0.6); }}
    .strike {{ position: relative; display: inline-block; color: #a1a1aa; }}
    .strike i {{ position: absolute; left: -8px; right: -8px; top: 52%; height: 12px; border-radius: 999px;
                 background: {RED}; transform-origin: left center; }}
    .p {{ position: absolute; left: 540px; top: 860px; width: 18px; height: 30px; border-radius: 4px; }}
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


def exit_(sel, d):
    return f'    tl.to("{sel}", {{ scale: 1.3, filter: "blur(16px)", opacity: 0, duration: 0.2, ease: "power3.in" }}, {d - 0.2:.2f});\n'


def enter(sel):
    return f'    tl.fromTo("{sel}", {{ scale: 1.12, filter: "blur(14px)", opacity: 0 }}, {{ scale: 1, filter: "blur(0px)", opacity: 1, duration: 0.28, ease: "power3.out" }}, 0);\n'


def confetti(prefix, n=26):
    """registry component 'confetti' pattern: deterministic burst (cos/sin of the index, no random)"""
    cols = [RED, BLUE, "#ffffff", "#f59e0b", "#22c55e"]
    html = "".join(f'<span class="p {prefix}-p" style="background:{cols[i % 5]};opacity:0;"></span>' for i in range(n))
    js = lambda t: (f'    tl.fromTo(".{prefix}-p", {{ x: 0, y: 0, rotation: 0, opacity: 0 }}, '
                    f'{{ opacity: 1, x: (i) => Math.cos(i * 0.83) * (300 + (i % 4) * 70), y: (i) => -260 - Math.sin(i * 0.61) * 260, '
                    f'rotation: (i) => 180 + i * 37, duration: 0.7, stagger: 0.012, ease: "power2.out" }}, {t});\n'
                    f'    tl.to(".{prefix}-p", {{ y: "+=700", opacity: 0, duration: 1.1, stagger: 0.012, ease: "power1.in" }}, {t + 0.7:.2f});\n')
    return html, js


C = {}
stars = "".join(f'<div style="position:absolute;left:{(i * 397) % 1080}px;top:{(i * 613) % 1920}px;width:{2 + i % 3}px;height:{2 + i % 3}px;border-radius:50%;background:rgba(255,255,255,{0.25 + (i % 4) * 0.12});"></div>' for i in range(70))
C["bg"] = comp("bg", f"""    <div style="position:absolute;inset:0;background:{DARK};"></div>
    <div id="bg-red" style="position:absolute;left:420px;top:-200px;width:1000px;height:1000px;border-radius:50%;background:radial-gradient(circle, rgba(225,29,72,0.30), rgba(225,29,72,0) 70%);" data-layout-allow-overflow></div>
    <div id="bg-blue" style="position:absolute;left:-400px;top:1100px;width:1000px;height:1000px;border-radius:50%;background:radial-gradient(circle, rgba(59,130,246,0.22), rgba(59,130,246,0) 70%);" data-layout-allow-overflow></div>
    <div id="bg-stars" style="position:absolute;inset:0;" data-layout-allow-overflow>{stars}</div>""",
               f'    tl.fromTo("#bg-stars", {{ y: 0 }}, {{ y: -160, duration: {TOTAL}, ease: "none" }}, 0);\n'
               f'    tl.fromTo("#bg-red", {{ scale: 0.9 }}, {{ scale: 1.2, duration: {TOTAL / 2:.2f}, ease: "sine.inOut", yoyo: true, repeat: 1 }}, 0);\n'
               f'    tl.fromTo("#bg-blue", {{ scale: 1.15 }}, {{ scale: 0.9, duration: {TOTAL / 2:.2f}, ease: "sine.inOut", yoyo: true, repeat: 1 }}, 0);\n')

# S1 hook + thumbnail: "MINECRAFT SERVER?" and "30% OFF" are on screen at t=0 (/sales: WELCOME30 30% OFF)
d = d_of("s1")
ch, cj = confetti("s1")
C["s1"] = comp("s1", f"""    <div id="s1-w" style="position:absolute;inset:0;">
      <div id="s1-img" style="position:absolute;inset:0;background:url(assets/img/games_minecraft-card.jpg) center/cover;filter:brightness(0.75);" data-layout-allow-overflow></div>
      <div style="position:absolute;inset:0;background:linear-gradient(to bottom, rgba(5,5,5,0.35), rgba(5,5,5,0.55) 30%, rgba(5,5,5,0.9) 62%, {DARK});"></div>
      <div class="c anton shadow" id="s1-a" style="top:430px;font-size:150px;color:#fff;">MINECRAFT<br>SERVER?</div>
      <div class="c anton r" id="s1-b" style="top:780px;font-size:230px;white-space:nowrap;text-shadow:0 0 80px rgba(225,29,72,0.6);">30% OFF</div>
      <div class="c gr shadow" id="s1-c" style="top:1060px;font-weight:700;font-size:54px;color:#e4e4e7;letter-spacing:6px;">MORADOSOLUTION</div>
      {ch}
    </div>""",
               f'    tl.fromTo("#s1-img", {{ scale: 1.15 }}, {{ scale: 1.35, duration: {d}, ease: "none" }}, 0);\n'
               f'    tl.fromTo("#s1-b", {{ scale: 1.0 }}, {{ scale: 1.12, duration: 0.18, ease: "power2.out", yoyo: true, repeat: 1 }}, {rel(0, 0.62)});\n'
               + cj(rel(0, 0.62)) + exit_("#s1-w", d))

# S2 coupon code (/minecraft-budget: "Codes apply automatically when you tap Buy Now — or paste them at checkout.")
d = d_of("s2")
code = "WELCOME30"
letters = "".join(f'<span class="s2-l" style="opacity:0;">{ch_}</span>' for ch_ in code)
C["s2"] = comp("s2", f"""    <div id="s2-w" style="position:absolute;inset:0;">
      <div class="c gr" style="top:470px;font-weight:700;font-size:58px;color:#fff;letter-spacing:10px;">BAS YE CODE</div>
      <div id="s2-card" class="card" style="position:absolute;left:110px;top:600px;width:860px;height:300px;border:6px dashed {RED};display:flex;align-items:center;justify-content:center;">
        <div class="anton" style="font-size:170px;color:#fff;letter-spacing:8px;">{letters}</div>
      </div>
      <div class="c gr" id="s2-n" style="top:960px;font-weight:600;font-size:44px;color:#d4d4d8;line-height:1.35;">Checkout par paste karein</div>
    </div>""",
               enter("#s2-w") +
               '    tl.fromTo("#s2-card", { scale: 0.6, rotation: -6, opacity: 0 }, { scale: 1, rotation: 0, opacity: 1, duration: 0.4, ease: "back.out(2)" }, 0.08);\n'
               f'    tl.to(".s2-l", {{ opacity: 1, duration: 0.01, stagger: 0.07 }}, {rel(1, 0.15)});\n'
               f'    tl.fromTo("#s2-n", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.35 }}, {rel(1, 0.15) + 0.6:.2f});\n'
               + exit_("#s2-w", d))


def price_scene(k, i, name, tag, specs, old, new, save):
    """registry component 'strikethrough-replace' pattern: strike line scales in, new price fades up"""
    d = d_of(k)
    chips = "".join(f'<span style="display:inline-block;margin:0 10px;padding:10px 26px;border-radius:999px;background:rgba(255,255,255,0.1);">{s}</span>' for s in specs)
    tagh = f'<span style="margin-left:22px;font-size:40px;padding:8px 22px;border-radius:999px;background:{RED};color:#fff;vertical-align:middle;">{tag}</span>' if tag else ""
    html = f"""    <div id="{k}-w" style="position:absolute;inset:0;">
      <div class="c gr" style="top:430px;font-weight:700;font-size:62px;color:#fff;">MINECRAFT {name.upper()}{tagh}</div>
      <div class="c gr" style="top:540px;font-weight:600;font-size:38px;color:#d4d4d8;">{chips}</div>
      <div class="c anton" id="{k}-old" style="top:680px;font-size:170px;"><span class="strike">{old}<i id="{k}-i"></i></span></div>
      <div class="c anton r" id="{k}-new" style="top:870px;font-size:280px;text-shadow:0 0 70px rgba(225,29,72,0.55);">{new}</div>
      <div class="c gr" id="{k}-mo" style="top:1150px;font-weight:700;font-size:60px;color:#fff;">/ month &nbsp;<span style="color:#22c55e;">{save}</span></div>
    </div>"""
    js = (enter(f"#{k}-w") +
          f'    tl.fromTo("#{k}-i", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.28, ease: "power2.out" }}, {rel(i, 0.3)});\n'
          f'    tl.fromTo("#{k}-new", {{ scale: 0.3, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2.4)" }}, {rel(i, 0.62)});\n'
          f'    tl.fromTo("#{k}-mo", {{ y: 30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.3 }}, {rel(i, 0.62) + 0.3:.2f});\n'
          + exit_(f"#{k}-w", d))
    return comp(k, html, js)


C["s3"] = price_scene("s3", 2, "Starter", "", ["2 GB RAM", "6 GB NVMe"], "₹199", "₹139", "SAVE ₹60")
C["s4"] = price_scene("s4", 3, "Gold", "POPULAR", ["10 GB RAM", "30 GB NVMe"], "₹699", "₹489", "SAVE ₹210")

# S5 Hytale: brand-kit block brand-offer (starburst "WELCOME30 / 30% OFF / Minecraft + Hytale plans") over Hytale art
d = d_of("s5")
C["s5"] = comp("s5", f"""    <div id="s5-w" style="position:absolute;inset:0;">
      <div id="s5-img" style="position:absolute;inset:0;background:url(assets/img/games_hytale-card.jpg) center/cover;filter:brightness(0.6);" data-layout-allow-overflow></div>
      <div style="position:absolute;inset:0;background:linear-gradient(to bottom, rgba(5,5,5,0.2), rgba(5,5,5,0.85) 75%);"></div>
      <div class="c anton shadow" id="s5-t" style="top:1060px;font-size:130px;color:#fff;">HYTALE BHI!</div>
    </div>""",
               f'    tl.fromTo("#s5-img", {{ scale: 1.15 }}, {{ scale: 1.35, duration: {d}, ease: "none" }}, 0);\n'
               '    tl.fromTo("#s5-t", { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.35, ease: "back.out(2)" }, 0.15);\n'
               + exit_("#s5-w", d))

# S6 hardware + DDoS (/minecraft-budget: AMD EPYC 7C13, NVMe; "All plans include DDoS protection")
d = d_of("s6")
chips = [("AMD EPYC 7C13", "PROCESSOR", 0.05, RED), ("NVMe", "STORAGE", 0.35, BLUE), ("DDoS Protection", "HAR PLAN MEIN", 0.68, RED)]
chip_html = "".join(
    f'<div class="card gr" id="s6-c{i}" style="position:absolute;left:110px;top:{470 + i * 270}px;width:860px;height:230px;display:flex;flex-direction:column;justify-content:center;padding-left:70px;border-left:10px solid {c};">'
    f'<div style="font-weight:600;font-size:34px;color:#a1a1aa;letter-spacing:6px;">{sub}</div>'
    f'<div style="font-weight:700;font-size:88px;color:#fff;line-height:1.05;">{t}</div></div>'
    for i, (t, sub, _, c) in enumerate(chips))
C["s6"] = comp("s6", f"""    <div id="s6-w" style="position:absolute;inset:0;">
      <div id="s6-img" style="position:absolute;inset:0;background:url(assets/img/guides_mc-hardware-racks.jpg) center/cover;filter:brightness(0.35);" data-layout-allow-overflow></div>
      {chip_html}
    </div>""",
               enter("#s6-w") + f'    tl.fromTo("#s6-img", {{ scale: 1.1 }}, {{ scale: 1.25, duration: {d}, ease: "none" }}, 0);\n'
               + "".join(f'    tl.fromTo("#s6-c{i}", {{ x: -900, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.35, ease: "power3.out" }}, {rel(5, f)});\n'
                         for i, (_, _, f, _) in enumerate(chips))
               + exit_("#s6-w", d))

# S7 deploy (/minecraft-budget: "Deploy your Minecraft server in minutes.")
d = d_of("s7")
C["s7"] = comp("s7", f"""    <div id="s7-w" style="position:absolute;inset:0;">
      <div class="c anton" id="s7-a" style="top:560px;font-size:190px;color:#fff;">SERVER</div>
      <div class="c anton r" id="s7-b" style="top:760px;font-size:170px;">MINUTES MEIN</div>
      <div class="c anton" id="s7-c" style="top:940px;font-size:170px;color:#fff;">READY</div>
    </div>""",
               enter("#s7-w") +
               '    tl.fromTo("#s7-a", { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.3, ease: "power3.out" }, 0.05);\n'
               '    tl.fromTo("#s7-b", { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.3, ease: "power3.out" }, 0.25);\n'
               f'    tl.fromTo("#s7-c", {{ scale: 0.3, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2.4)" }}, {rel(6, 0.6)});\n'
               + exit_("#s7-w", d))

os.makedirs("compositions", exist_ok=True)
for k, v in C.items():
    open(f"compositions/{k}.html", "w").write(v)

host = lambda cid, s, du, lane, z: (f'      <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" data-start="{s}" '
                                    f'data-duration="{round(du, 3)}" data-track-index="{lane}" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: {z}"></div>')
divs = [host("bg", 0, TOTAL, 0, 0)]
for k, s, e in SCENES[:-1]:
    divs.append(host(k, s, e - s, 1, 1))
s5s, s5e = W["s5"]
divs.append(host("brand-offer", round(s5s + 0.1, 2), round(s5e - s5s - 0.1, 2), 2, 2))
divs.append(host("brand-bug", W["s2"][0], round(W["s8"][0] - W["s2"][0], 2), 3, 3))
divs.append(host("brand-end", W["s8"][0], round(TOTAL - W["s8"][0], 2), 1, 1))

sfx = lambda n: f"assets/sfx/{n}.mp3"
loud_at = round(VO_END + 0.3, 2)
A = [("vo", VO_FILE, VO_START, dur(VO_FILE), 1.0, 10, 0),
     ("m1", "assets/music/music.mp3", 0, loud_at, 0.13, 11, MUSIC_IN),
     ("m2", "assets/music/music.mp3", loud_at, round(TOTAL - loud_at, 2), 0.45, 12, round(MUSIC_IN + loud_at, 2))]
t_slam = rel(0, 0.62)
A.append(("hit", sfx("punch-heavy"), round(t_slam - 0.038, 2), dur(sfx("punch-heavy")), 0.4, 13, 0))
for i, (k, s, e) in enumerate(SCENES[1:]):
    A.append((f"wh{i}", sfx("swish-4"), round(max(0, s - 0.046), 2), dur(sfx("swish-4")), 0.7, 14 + i % 2, 0))
for j in range(len(code)):
    A.append((f"key{j}", sfx("keypress"), round(W["s2"][0] + rel(1, 0.15) + j * 0.07 - 0.042, 2), dur(sfx("keypress")), 0.5, 30 + j, 0))
for k, i in (("s3", 2), ("s4", 3)):
    A.append((f"cash{k}", sfx("cash-register"), round(W[k][0] + rel(i, 0.62) - 0.005, 2), dur(sfx("cash-register")), 0.45, 18, 0))
A.append(("popoffer", sfx("pop-high"), round(W["s5"][0] + 0.15, 2), dur(sfx("pop-high")), 0.6, 19, 0))
for i, (_, _, f, _) in enumerate(chips):
    A.append((f"pop{i}", sfx("pop-high"), round(W["s6"][0] + rel(5, f) - 0.006, 2), dur(sfx("pop-high")), 0.5, 20 + i % 2, 0))
A.append(("pw", sfx("digital-powerup-1"), round(W["s7"][0] + rel(6, 0.6) - 0.018, 2), dur(sfx("digital-powerup-1")), 0.4, 22, 0))
A.append(("spk", sfx("sparkle"), round(W["s8"][0] + 0.1, 2), dur(sfx("sparkle")), 0.4, 23, 0))
aud = "\n".join(f'      <audio id="{i}" src="{s}" data-start="{a}" data-duration="{dd}" data-volume="{v}" data-track-index="{ln}"'
                + (f' data-media-start="{ms}"' if ms else "") + (' data-fade-out="1.5"' if i == "m2" else "") + "></audio>"
                for i, s, a, dd, v, ln, ms in A)
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
print("built", TOTAL, SCENES)
