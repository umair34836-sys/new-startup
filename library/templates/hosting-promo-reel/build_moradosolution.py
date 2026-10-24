# MoradoSolution 9:16 promo reel (free VoxCPM2 Hindi VO). Every on-screen claim is quoted from moradosolution.in
# (pages read 2026-10-24; moradosolution.com itself only shows the DirectAdmin placeholder, owner chose .in).
# Scene starts follow the VO line starts (vo/lines.json: start of each line inside vo.wav) shifted by VO_START.
import json, os, subprocess

SONG = os.environ.get("SONG") == "1"   # song version: sung lines (assets/vo/song.wav has its own music)
VO_START = 0.0 if SONG else 0.4
RED, BLUE, DARK = "#e11d48", "#3b82f6", "#050505"   # site CSS: --bg #050505; accents #e11d48 / #3b82f6 (logo red/blue)
L = json.load(open("assets/vo/song_lines.json" if SONG else "assets/vo/lines.json"))          # [[start, end], ...] per script line, seconds inside vo.wav
VO_END = VO_START + L[-1][1]
VO_FILE = "assets/vo/song.wav" if SONG else "assets/vo/vo.wav"
TOTAL = round(VO_END + 2.6, 2)
if SONG:  # end with the song's own outro (up to 3.5 s after the last sung word), faded out
    _sd = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", VO_FILE],
                               capture_output=True, text=True).stdout)
    TOTAL = round(min(_sd, VO_END + 3.5), 2)
st = [round(VO_START + a - 0.15, 2) for a, _ in L]
st[0] = 0.0
# s1 hook, s2 brand, s3 hardware, s4 DDoS, s5 locations, s6 price, s7 deploy/support, s8 end card (last line)
SCENES = [(f"s{i + 1}", st[i], st[i + 1] if i + 1 < len(st) else TOTAL) for i in range(len(st))]
W = {k: (s, e) for k, s, e in SCENES}


def dur(p):
    return round(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                      capture_output=True, text=True).stdout), 3)


def rel(i, frac):
    """time inside scene i (0-based line) at a fraction of that line's speech"""
    a, b = L[i]
    return round(VO_START + a + frac * (b - a) - st[i], 2)


CSS = f"""
    @font-face {{ font-family: "Anton"; src: url("assets/fonts/Anton-Regular.ttf"); }}
    @font-face {{ font-family: "Grotesk"; src: url("assets/fonts/SpaceGrotesk-Variable.ttf"); font-weight: 300 700; }}
    #root {{ position: absolute; inset: 0; overflow: hidden; }}
    .c {{ position: absolute; left: 0; right: 0; text-align: center; }}
    .anton {{ font-family: Anton; letter-spacing: 2px; line-height: 0.95; }}
    .gr {{ font-family: Grotesk; }}
    .r {{ color: {RED}; }}
    .shadow {{ text-shadow: 0 6px 30px rgba(0,0,0,0.85); }}
    .pill {{ display: inline-block; padding: 18px 46px; border-radius: 999px; background: #fff; color: {DARK};
             font-family: Grotesk; font-weight: 700; font-size: 62px; box-shadow: 0 0 60px rgba(255,255,255,0.25); }}
    .pill.red {{ background: {RED}; color: #fff; box-shadow: 0 0 60px rgba(225,29,72,0.55); }}
    .card {{ border-radius: 30px; background: rgba(18,18,21,0.92); border: 2px solid rgba(255,255,255,0.14);
             box-shadow: 0 20px 60px rgba(0,0,0,0.6); }}
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


def d_of(k):
    s, e = W[k]
    return round(e - s, 2)


C = {}
# global background: near-black, red + blue glows (logo colours), slow star drift
stars = "".join(f'<div style="position:absolute;left:{(i * 397) % 1080}px;top:{(i * 613) % 1920}px;width:{2 + i % 3}px;height:{2 + i % 3}px;border-radius:50%;background:rgba(255,255,255,{0.25 + (i % 4) * 0.12});"></div>' for i in range(70))
C["bg"] = comp("bg", f"""    <div style="position:absolute;inset:0;background:{DARK};"></div>
    <div id="bg-red" style="position:absolute;left:420px;top:-200px;width:1000px;height:1000px;border-radius:50%;background:radial-gradient(circle, rgba(225,29,72,0.30), rgba(225,29,72,0) 70%);" data-layout-allow-overflow></div>
    <div id="bg-blue" style="position:absolute;left:-400px;top:1100px;width:1000px;height:1000px;border-radius:50%;background:radial-gradient(circle, rgba(59,130,246,0.22), rgba(59,130,246,0) 70%);" data-layout-allow-overflow></div>
    <div id="bg-stars" style="position:absolute;inset:0;" data-layout-allow-overflow>{stars}</div>""",
               f'    tl.fromTo("#bg-stars", {{ y: 0 }}, {{ y: -160, duration: {TOTAL}, ease: "none" }}, 0);\n'
               f'    tl.fromTo("#bg-red", {{ scale: 0.9 }}, {{ scale: 1.2, duration: {TOTAL / 2:.2f}, ease: "sine.inOut", yoyo: true, repeat: 1 }}, 0);\n'
               f'    tl.fromTo("#bg-blue", {{ scale: 1.15 }}, {{ scale: 0.9, duration: {TOTAL / 2:.2f}, ease: "sine.inOut", yoyo: true, repeat: 1 }}, 0);\n')

# S1 hook (site H1: "Minecraft Server Hosting in India"); visible at t=0 for the thumbnail
d = d_of("s1")
C["s1"] = comp("s1", f"""    <div id="s1-w" style="position:absolute;inset:0;">
      <div id="s1-img" style="position:absolute;inset:0;background:url(assets/img/mc.jpg) center/cover;" data-layout-allow-overflow></div>
      <div style="position:absolute;inset:0;background:linear-gradient(to bottom, rgba(5,5,5,0.55), rgba(5,5,5,0.1) 30%, rgba(5,5,5,0.85) 62%, {DARK});"></div>
      <div class="c gr shadow" id="s1-a" style="top:1010px;font-weight:700;font-size:62px;color:#e4e4e7;letter-spacing:8px;">INDIA MEIN</div>
      <div class="c anton shadow" id="s1-b" style="top:1100px;font-size:190px;color:#fff;">MINECRAFT</div>
      <div class="c anton shadow r" id="s1-c" style="top:1290px;font-size:150px;">SERVER HOSTING?</div>
    </div>""",
               f'    tl.fromTo("#s1-img", {{ scale: 1.2 }}, {{ scale: 1.38, duration: {d}, ease: "none" }}, 0);\n'
               f'    tl.fromTo("#s1-b", {{ scale: 1.08 }}, {{ scale: 1, duration: 1.0, ease: "power2.out" }}, 0);\n'
               f'    tl.fromTo("#s1-c", {{ y: 60, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "back.out(2)" }}, {rel(0, 0.55)});\n'
               + enter_exit("#s1-w", d, enter=False))

# S2 brand (site title/tagline)
d = d_of("s2")
C["s2"] = comp("s2", f"""    <div id="s2-w" style="position:absolute;inset:0;">
      <div id="s2-ring" style="position:absolute;left:265px;top:420px;width:550px;height:550px;border-radius:50%;border:5px solid rgba(255,255,255,0.8);box-shadow:0 0 80px {RED};"></div>
      <img id="s2-logo" src="assets/img/logo.png" style="position:absolute;left:300px;top:520px;width:480px;height:384px;" alt="MoradoSolution logo">
      <div class="c gr" id="s2-name" style="top:1060px;font-weight:700;font-size:112px;color:#fff;">MoradoSolution</div>
      <div class="c gr" id="s2-tag" style="top:1210px;font-weight:500;font-size:46px;color:#a1a1aa;">Minecraft Server Hosting in India</div>
    </div>""",
               enter_exit("#s2-w", d) +
               '    tl.fromTo("#s2-logo", { scale: 0.3, rotation: -25, opacity: 0 }, { scale: 1, rotation: 0, opacity: 1, duration: 0.6, ease: "back.out(1.8)" }, 0.12);\n'
               '    tl.fromTo("#s2-ring", { scale: 0.5, opacity: 0 }, { scale: 1.15, opacity: 0, duration: 1.4, ease: "power2.out" }, 0.2);\n'
               f'    tl.fromTo("#s2-name", {{ y: 40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.45, ease: "power3.out" }}, {rel(1, 0.45)});\n'
               '    tl.fromTo("#s2-tag", { opacity: 0 }, { opacity: 1, duration: 0.3 }, 0.9);\n')

# S3 hardware (infrastructure page: AMD EPYC 7C13, NVMe Gen 4; home: "Zero swap", "0 swap on NVMe")
d = d_of("s3")
chips = [("AMD EPYC 7C13", "PROCESSOR", 0.02), ("NVMe Gen 4", "STORAGE", 0.42), ("Zero Swap", "MAXIMUM PERFORMANCE", 0.78)]
chip_html = "".join(
    f'<div class="card gr" id="s3-c{i}" style="position:absolute;left:110px;top:{560 + i * 290}px;width:860px;height:240px;display:flex;flex-direction:column;justify-content:center;padding-left:70px;border-left:10px solid {RED if i != 1 else BLUE};">'
    f'<div style="font-weight:600;font-size:36px;color:#a1a1aa;letter-spacing:6px;">{sub}</div>'
    f'<div style="font-weight:700;font-size:92px;color:#fff;line-height:1.05;">{t}</div></div>'
    for i, (t, sub, _) in enumerate(chips))
chip_js = "".join(f'    tl.fromTo("#s3-c{i}", {{ x: -900, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.4, ease: "power3.out" }}, {max(0.05, rel(2, f))});\n'
                  for i, (_, _, f) in enumerate(chips))
C["s3"] = comp("s3", f"""    <div id="s3-w" style="position:absolute;inset:0;">
      <div class="c gr" style="top:380px;font-weight:700;font-size:56px;letter-spacing:10px;color:#fff;">HARDWARE</div>
      {chip_html}
    </div>""", enter_exit("#s3-w", d) + chip_js)

# S4 DDoS (home: "Every plan includes DDoS filtering"; DDoS page: "always on, included on every plan")
d = d_of("s4")
C["s4"] = comp("s4", f"""    <div id="s4-w" style="position:absolute;inset:0;">
      <svg id="s4-shield" viewBox="0 0 200 230" style="position:absolute;left:340px;top:380px;width:400px;height:460px;">
        <path d="M100 8 L188 40 V110 C188 165 150 205 100 222 C50 205 12 165 12 110 V40 Z" fill="rgba(225,29,72,0.16)" stroke="{RED}" stroke-width="8"/>
        <path id="s4-tick" d="M60 115 L90 145 L145 85" fill="none" stroke="#fff" stroke-width="14" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="150" stroke-dashoffset="150"/>
      </svg>
      <div class="c anton" id="s4-t" style="top:940px;font-size:150px;color:#fff;">DDoS PROTECTION</div>
      <div class="c" id="s4-p" style="top:1150px;"><span class="pill red">EVERY PLAN · INCLUDED</span></div>
      <div class="c gr" id="s4-s" style="top:1310px;font-weight:500;font-size:44px;color:#a1a1aa;">Always-on filtering, inline at the edge</div>
    </div>""",
               enter_exit("#s4-w", d) +
               '    tl.fromTo("#s4-shield", { scale: 0.4, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.5, ease: "back.out(2)" }, 0.1);\n'
               '    tl.to("#s4-tick", { strokeDashoffset: 0, duration: 0.5, ease: "power2.out" }, 0.55);\n'
               f'    tl.fromTo("#s4-t", {{ y: 50, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "power3.out" }}, 0.25);\n'
               f'    tl.fromTo("#s4-p", {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2.2)" }}, {rel(3, 0.4)});\n'
               f'    tl.fromTo("#s4-s", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, 0.45);\n')

# S5 locations (infrastructure page "Network": Frankfurt Europe, Delhi North India, Mumbai West India; nav "DEL · BOM · FRA")
d = d_of("s5")
locs = [("Delhi", "North India", "india-flag.png", 0.25), ("Mumbai", "West India", "india-flag-2.png", 0.45),
        ("Frankfurt", "Europe", "germany-flag.png", 0.7)]
loc_html = "".join(
    f'<div class="card gr" data-layout-allow-overflow id="s5-l{i}" style="position:absolute;left:120px;top:{520 + i * 250}px;width:840px;height:210px;display:flex;align-items:center;gap:44px;padding-left:56px;">'
    f'<img src="assets/img/{f}" style="width:150px;height:100px;object-fit:cover;border-radius:14px;" alt="{n} flag">'
    f'<div><div style="font-weight:700;font-size:78px;color:#fff;line-height:1;">{n}</div><div style="font-weight:500;font-size:38px;color:#a1a1aa;margin-top:8px;">{r}</div></div></div>'
    for i, (n, r, f, _) in enumerate(locs))
loc_js = "".join(f'    tl.fromTo("#s5-l{i}", {{ x: 900, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.4, ease: "power3.out" }}, {max(0.05, rel(4, f))});\n'
                 for i, (_, _, _, f) in enumerate(locs))
C["s5"] = comp("s5", f"""    <div id="s5-w" style="position:absolute;inset:0;">
      <div class="c gr" style="top:360px;font-weight:700;font-size:60px;color:#fff;letter-spacing:8px;">SERVERS IN</div>
      {loc_html}
      <div class="c" id="s5-up" style="top:1320px;"><span class="pill">99.9% UPTIME TARGET</span></div>
    </div>""",
               enter_exit("#s5-w", d) + loc_js +
               f'    tl.fromTo("#s5-up", {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2.2)" }}, {rel(4, 0.55)});\n')

# S6 price (home: Minecraft "From ₹199/mo", Hytale "From ₹199/mo")
d = d_of("s6")
C["s6"] = comp("s6", f"""    <div id="s6-w" style="position:absolute;inset:0;">
      <div id="s6-mc" style="position:absolute;left:-220px;top:0;width:1520px;height:960px;background:url(assets/img/mc.jpg) center/cover;filter:brightness(0.45);" data-layout-allow-overflow></div>
      <div id="s6-hy" style="position:absolute;left:-220px;top:960px;width:1520px;height:960px;background:url(assets/img/hytale.jpg) center/cover;filter:brightness(0.45);" data-layout-allow-overflow></div>
      <div style="position:absolute;inset:0;background:radial-gradient(ellipse 70% 45% at 50% 50%, rgba(5,5,5,0.92), rgba(5,5,5,0.35));"></div>
      <div class="c gr" id="s6-a" style="top:520px;font-weight:700;font-size:70px;color:#fff;letter-spacing:4px;">MINECRAFT &amp; HYTALE</div>
      <div class="c gr" style="top:660px;font-weight:600;font-size:56px;color:#e4e4e7;">sirf</div>
      <div class="c anton r" id="s6-p" style="top:740px;font-size:360px;text-shadow:0 0 70px rgba(225,29,72,0.55);">₹199</div>
      <div class="c gr" id="s6-m" style="top:1120px;font-weight:700;font-size:72px;color:#fff;">/ month se shuru</div>
    </div>""",
               enter_exit("#s6-w", d) +
               f'    tl.fromTo("#s6-mc", {{ x: -100 }}, {{ x: 100, duration: {d}, ease: "none" }}, 0);\n'
               f'    tl.fromTo("#s6-hy", {{ x: 100 }}, {{ x: -100, duration: {d}, ease: "none" }}, 0);\n'
               f'    tl.fromTo("#s6-p", {{ scale: 0.2, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.45, ease: "back.out(2.4)" }}, {rel(5, 0.55)});\n'
               f'    tl.fromTo("#s6-m", {{ y: 40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "power3.out" }}, {rel(5, 0.75)});\n')

# S7 deploy + support (game hosting page: "Deploy in minutes."; footer: "support answered by humans")
d = d_of("s7")
C["s7"] = comp("s7", f"""    <div id="s7-w" style="position:absolute;inset:0;">
      <div class="c anton" id="s7-a" style="top:520px;font-size:180px;color:#fff;">DEPLOY</div>
      <div class="c anton r" id="s7-b" style="top:700px;font-size:180px;">IN MINUTES</div>
      <div id="s7-line" style="position:absolute;left:240px;top:960px;width:600px;height:6px;background:rgba(255,255,255,0.3);"></div>
      <div class="c gr" id="s7-c" style="top:1040px;font-weight:700;font-size:74px;color:#fff;">Support answered</div>
      <div class="c gr" id="s7-d" style="top:1135px;font-weight:700;font-size:74px;color:#fff;">by <span style="color:{BLUE};">humans</span></div>
    </div>""",
               enter_exit("#s7-w", d) +
               '    tl.fromTo("#s7-a", { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.35, ease: "power3.out" }, 0.05);\n'
               '    tl.fromTo("#s7-b", { y: 60, opacity: 0 }, { y: 0, opacity: 1, duration: 0.35, ease: "power3.out" }, 0.3);\n'
               '    tl.fromTo("#s7-line", { scaleX: 0 }, { scaleX: 1, duration: 0.4, ease: "power2.out" }, 0.5);\n'
               f'    tl.fromTo("#s7-c", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.35 }}, {rel(6, 0.5)});\n'
               f'    tl.fromTo("#s7-d", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.35 }}, {rel(6, 0.62)});\n')

# S8 end card (site URL chosen by the owner: moradosolution.in; Discord link from the site footer)
d = d_of("s8")
C["s8"] = comp("s8", f"""    <div id="s8-w" style="position:absolute;inset:0;">
      <img id="s8-logo" src="assets/img/logo.png" style="position:absolute;left:340px;top:360px;width:400px;height:320px;" alt="MoradoSolution logo">
      <div class="c gr" id="s8-name" style="top:740px;font-weight:700;font-size:104px;color:#fff;">MoradoSolution</div>
      <div class="c gr" id="s8-cta" style="top:930px;font-weight:600;font-size:56px;color:#e4e4e7;">Aaj hi visit karein</div>
      <div class="c" id="s8-url" style="top:1040px;"><span class="pill" style="font-size:70px;">moradosolution.in</span></div>
      <div class="c gr" id="s8-dc" style="top:1250px;font-weight:500;font-size:44px;color:#a1a1aa;">discord.gg/moradosolution</div>
    </div>""",
               '    tl.fromTo("#s8-w", { scale: 1.12, filter: "blur(14px)", opacity: 0 }, { scale: 1, filter: "blur(0px)", opacity: 1, duration: 0.3, ease: "power3.out" }, 0);\n'
               '    tl.fromTo("#s8-logo", { scale: 0.3, rotation: -25, opacity: 0 }, { scale: 1, rotation: 0, opacity: 1, duration: 0.6, ease: "back.out(1.8)" }, 0.1);\n'
               '    tl.fromTo("#s8-name", { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: "power3.out" }, 0.4);\n'
               '    tl.fromTo("#s8-cta", { opacity: 0 }, { opacity: 1, duration: 0.4 }, 0.6);\n'
               f'    tl.fromTo("#s8-url", {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2.2)" }}, {rel(7, 0.5)});\n'
               f'    tl.to("#s8-url", {{ scale: 1.06, duration: 0.45, ease: "sine.inOut", yoyo: true, repeat: 5 }}, {rel(7, 0.5) + 0.45:.2f});\n'
               f'    tl.fromTo("#s8-dc", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {rel(7, 0.5) + 0.6:.2f});\n')

os.makedirs("compositions", exist_ok=True)
for k, v in C.items():
    open(f"compositions/{k}.html", "w").write(v)

divs = [f'      <div id="bg" data-composition-id="bg" data-composition-src="compositions/bg.html" data-start="0" data-duration="{TOTAL}" data-track-index="0" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: 0"></div>']
for k, s, e in SCENES:
    divs.append(f'      <div id="{k}" data-composition-id="{k}" data-composition-src="compositions/{k}.html" data-start="{s}" data-duration="{round(e - s, 3)}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: 1"></div>')

sfx = lambda n: f"assets/sfx/{n}.mp3"
loud_at = round(TOTAL - 2.5, 2)
A = [("vo", VO_FILE, VO_START, min(dur(VO_FILE), TOTAL), 1.0, 10, 0)]
if not SONG:
    A += [("m1", "assets/music/music.mp3", 0, loud_at, 0.22, 11, 0),
          ("m2", "assets/music/music.mp3", loud_at, 2.5, 0.6, 12, loud_at)]
A += [
     ("hit", sfx("impact-bass-1"), round(st[0] + rel(0, 0.55), 2), dur(sfx("impact-bass-1")), 0.3, 13, 0)]
for i, (k, s, e) in enumerate(SCENES[1:]):
    A.append((f"wh{i}", sfx("whoosh-short"), round(max(0, s - 0.12), 2), dur(sfx("whoosh-short")), 0.45, 14 + i % 2, 0))
pops = [W["s3"][0] + max(0.05, rel(2, f)) for *_, f in chips] + [W["s5"][0] + max(0.05, rel(4, f)) for *_, f in locs]
for i, t in enumerate(pops):
    A.append((f"pop{i}", sfx("pop"), round(t, 2), dur(sfx("pop")), 0.5, 16 + i % 2, 0))
A += [("spk", sfx("sparkle"), round(W["s6"][0] + rel(5, 0.55), 2), dur(sfx("sparkle")), 0.35, 18, 0),
      ("spk2", sfx("sparkle"), round(W["s8"][0] + rel(7, 0.5), 2), dur(sfx("sparkle")), 0.35, 19, 0)]
aud = "\n".join(f'      <audio id="{i}" src="{s}" data-start="{a}" data-duration="{dd}" data-volume="{v}" data-track-index="{ln}"'
                + (f' data-media-start="{ms}"' if ms else "") + (' data-fade-out="1.5"' if i == "m2" or (SONG and i == "vo") else "") + "></audio>"
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
