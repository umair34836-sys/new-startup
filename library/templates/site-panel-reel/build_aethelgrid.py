# AethelGrid 9:16 ~60 s "site + panel" reel (free VoxCPM2 Hindi VO, field voice promo-male). 2026-10-28.
# Picture = real screen recordings of aethelgrid.cloud + the public panel login page (flow_aethelgrid.js, cursor +
# ripple on every click), joined into one 1080x1920 screen.mp4; each recording span is speed-fitted to its VO line
# (screen-tutorial idea). On top: one overlay composition per VO line with pills/badges quoting the site.
# Every on-screen claim is from library/clients/aethelgrid/site-data.md (Playwright read 2026-10-28).
# Look = the site's own: dark #0c0a18 / navy-purple gradient, Tailwind blue-600 #2563eb buttons, green #22c55e accent
# (/minecraft heading), system-like sans (Plus Jakarta Sans here), mono labels.
# Run inside the project folder (scratchpad, never git) that holds: rec/<shot>/{recording.mp4,events.json},
# assets/img/{logo.png,panel.png}, assets/fonts, assets/sfx, assets/audio/mix.wav (VO + music from mix_vo_music.py),
# assets/vo/lines.json (vs_tts.py --parts), assets/vendor/gsap-3.14.2.min.js.
import json, os, subprocess

VO_START = 0.6
TOTAL = float(os.environ.get("TOTAL", 60.0))
BG, BLUE, GREEN, GREY = "#0c0a18", "#2563eb", "#22c55e", "#9ca3af"
L = json.load(open("assets/vo/lines.json"))           # [[start, end], ...] per script line inside vo.wav
st = [round(VO_START + a - 0.15, 2) for a, _ in L]
st[0] = 0.0
SCENES = [(f"s{i + 1}", st[i], st[i + 1] if i + 1 < len(st) else TOTAL) for i in range(len(st))]
W = {k: (s, e) for k, s, e in SCENES}

# scene -> (recording, from s, to s) inside that recording; None = no recording behind (designed card)
SEG = json.load(open("seg.json"))


def run(*a):
    subprocess.run(a, check=True, capture_output=True)


def rel(i, frac):
    a, b = L[i]
    return round(max(0.05, VO_START + a + frac * (b - a) - st[i]), 2)


# ---------- picture track: one speed-fitted span per scene ----------
os.makedirs("assets/clips", exist_ok=True)
CLICKS = []          # output times of real clicks / presses -> click sound
parts = []
for k, s, e in SCENES:
    d = round(e - s, 3)
    out = f"assets/clips/{k}.mp4"
    seg = SEG.get(k)
    if seg is None:   # designed card: dark frame (the overlay covers it)
        run("ffmpeg", "-y", "-f", "lavfi", "-i", f"color=c={BG}:s=1080x1920:r=30:d={d}", "-c:v", "libx264", "-crf", "16",
            "-pix_fmt", "yuv420p", out)
    else:
        shot, a, b = seg
        span = b - a
        speed = span / d   # >1 = faster; spans are chosen so this stays about 0.85-2.5
        vf = f"setpts=(PTS-STARTPTS)/{speed:.5f},fps=30,trim=0:{d},setpts=PTS-STARTPTS"
        blur = len(seg) > 3 and seg[3] == "blur"
        if blur:
            vf += ",gblur=sigma=18,eq=brightness=-0.12"
        run("ffmpeg", "-y", "-ss", str(a), "-t", str(span + 0.5), "-i", f"rec/{shot}/recording.mp4", "-an", "-vf",
            vf + f",tpad=stop_mode=clone:stop_duration={d}", "-t", str(d), "-c:v", "libx264", "-crf", "16",
            "-pix_fmt", "yuv420p", "-r", "30", out)
        ev = json.load(open(f"rec/{shot}/events.json"))["events"]
        for x in ev:
            if x["type"] in ("click", "fakeclick") and a <= x["t"] <= b and not blur:
                CLICKS.append(round(s + (x["t"] - a) / speed, 2))
    parts.append(out)
open("assets/clips/list.txt", "w").write("".join(f"file '{os.path.basename(p)}'\n" for p in parts))
run("ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "assets/clips/list.txt", "-c", "copy", "assets/screen.mp4")

# ---------- overlays ----------
CSS = f"""
    @font-face {{ font-family: "PJ"; src: url("assets/fonts/PlusJakartaSans-Variable.ttf"); font-weight: 200 800; }}
    @font-face {{ font-family: "JB"; src: url("assets/fonts/JetBrainsMono-Variable.ttf"); font-weight: 100 800; }}
    #root {{ position: absolute; inset: 0; overflow: hidden; }}
    .c {{ position: absolute; left: 0; right: 0; text-align: center; }}
    .h {{ font-family: PJ; font-weight: 800; letter-spacing: -2px; line-height: 1.0; color: #fff; text-shadow: 0 6px 30px rgba(0,0,0,0.7); }}
    .pill {{ display: inline-block; font-family: JB; font-weight: 700; font-size: 32px; letter-spacing: 3px; color: #fff;
             padding: 14px 28px; border-radius: 999px; background: rgba(12,10,24,0.88); border: 2px solid rgba(96,165,250,0.6); }}
    .badge {{ display: inline-flex; align-items: center; gap: 18px; font-family: PJ; font-weight: 800; font-size: 60px; color: #fff;
              padding: 22px 40px; border-radius: 22px; background: rgba(12,10,24,0.92); border: 2px solid rgba(255,255,255,0.18);
              box-shadow: 0 20px 60px rgba(0,0,0,0.6); }}
    .badge.b {{ background: {BLUE}; border-color: {BLUE}; }}
    .badge.g {{ background: {GREEN}; border-color: {GREEN}; color: #06140b; }}
    .veil {{ position: absolute; left: 0; right: 0; top: 1020px; height: 900px;
             background: linear-gradient(180deg, rgba(12,10,24,0) 0%, rgba(12,10,24,0.92) 25%, rgba(12,10,24,0.97) 100%); }}
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


POPS = []


def scene(k, i, top_pill, badges, veil=True, extra_html="", extra_js=""):
    """top pill + badges popping on the spoken words; badges = [(html, cls, frac of the VO line, top px)]"""
    s, e = W[k]
    d = round(e - s, 2)
    html = (('<div class="veil"></div>' if veil else "") +
            (f'<div class="c" id="{k}-p" style="top:170px;"><span class="pill">{top_pill}</span></div>' if top_pill else "") +
            extra_html +
            "".join(f'<div class="c" id="{k}-b{j}" style="top:{top}px;"><span class="badge {cls}">{h}</span></div>'
                    for j, (h, cls, fr, top) in enumerate(badges)))
    js = (f'    tl.fromTo("#{k}-p", {{ y: -40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "power3.out" }}, 0.05);\n' if top_pill else "")
    for j, (h, cls, fr, top) in enumerate(badges):
        t = rel(i, fr)
        js += f'    tl.fromTo("#{k}-b{j}", {{ scale: 0.3, opacity: 0, y: 40 }}, {{ scale: 1, opacity: 1, y: 0, duration: 0.4, ease: "back.out(2.2)" }}, {t});\n'
        POPS.append(round(s + t, 2))
    js += f'    tl.to("#root", {{ opacity: 0, duration: 0.18, ease: "power2.in" }}, {d - 0.18:.2f});\n'
    return comp(k, html, js + extra_js)


C = {}
# S1 hook (thumbnail at 0 s): logo + the three services from the site's menu/pricing + headline
d1 = round(W["s1"][1], 2)
C["s1"] = comp("s1", f"""    <div style="position:absolute;inset:0;background:radial-gradient(120% 80% at 50% 30%, #3b0f8a 0%, #1a0b4a 45%, {BG} 100%);"></div>
    <div class="c" id="s1-logo" style="top:420px;"><img src="assets/img/logo.png" style="width:820px;height:188px;" alt="AethelGrid logo"></div>
    <div class="c h" id="s1-a" style="top:700px;font-size:120px;">HOSTING</div>
    <div class="c h" id="s1-b" style="top:830px;font-size:120px;color:#60a5fa;">SAB EK JAGAH</div>
    <div class="c" id="s1-k0" style="top:1040px;"><span class="badge g">Minecraft Servers</span></div>
    <div class="c" id="s1-k1" style="top:1190px;"><span class="badge b">VPS Hosting</span></div>
    <div class="c" id="s1-k2" style="top:1340px;"><span class="badge">Discord Bot Hosting</span></div>""",
               '    tl.fromTo("#s1-logo", { scale: 0.85 }, { scale: 1, duration: 1.2, ease: "power2.out" }, 0);\n'
               '    tl.fromTo("#s1-b", { y: 50, opacity: 0 }, { y: 0, opacity: 1, duration: 0.35, ease: "back.out(2)" }, 0.25);\n'
               + "".join(f'    tl.fromTo("#s1-k{j}", {{ x: {(-1) ** j * 700}, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.35, ease: "power3.out" }}, {rel(0, f)});\n'
                         for j, f in enumerate((0.05, 0.25, 0.45)))
               )
POPS += [round(rel(0, f), 2) for f in (0.05, 0.25, 0.45)]

C["s2"] = scene("s2", 1, "AETHELGRID.CLOUD", [('<img src="assets/img/logo.png" style="width:520px;height:119px;" alt="AethelGrid">', "", 0.1, 1250)])
C["s3"] = scene("s3", 2, None, [("&lt; 60 sec Instant Setup", "b", 0.05, 1120), ("DDoS Protection", "", 0.4, 1270),
                                ("99.9% Uptime", "", 0.6, 1420), ("24/7 Support", "g", 0.8, 1570)])
C["s4"] = scene("s4", 3, "ADVANCED FEATURES", [("High Performance", "", 0.05, 1200), ("Low Latency", "", 0.35, 1350),
                                               ("Auto Recovery + Backup", "b", 0.65, 1500)])
C["s5"] = scene("s5", 4, "GLOBAL LOCATIONS", [("INDIA", "g", 0.2, 1250), ("GERMANY", "b", 0.6, 1400)])
C["s6"] = scene("s6", 5, "MINECRAFT HOSTING", [("11 Plans", "", 0.15, 1200),
                                               ('<span style="font-size:96px;">₹80</span>/mo se', "g", 0.6, 1360)])
C["s7"] = scene("s7", 6, "HAR PLAN MEIN", [("NVMe SSD Storage", "", 0.2, 1200), ("DDR4 ECC Memory", "", 0.45, 1350),
                                          ("Premium Game Panel", "g", 0.7, 1500)])
C["s8"] = scene("s8", 7, "VPS HOSTING", [("Intel Xeon • AMD EPYC", "b", 0.15, 1200), ("Full Root Access", "", 0.65, 1350),
                                        ('<span style="font-size:80px;">₹285</span>/mo se', "g", 0.85, 1500)])
C["s9"] = scene("s9", 8, "DISCORD BOT HOSTING", [('<span style="font-size:80px;">₹35.07</span>/mo se', "g", 0.2, 1250),
                                                ("LavaLink V4", "b", 0.65, 1400)])
# the site's own panel picture (aethelgrid.cloud/experience.png, 1024x1024 with black bands; panel UI = y 224-800)
PANEL = ('<div id="s10-pan" style="position:absolute;left:40px;top:420px;width:1000px;height:563px;overflow:hidden;border-radius:22px;'
         'border:3px solid rgba(96,165,250,0.7);box-shadow:0 30px 90px rgba(0,0,0,0.8);">'
         '<img src="assets/img/panel.png" style="position:absolute;left:0;top:-219px;width:1000px;height:1000px;" alt="AethelGrid panel (site image)"></div>')
C["s10"] = scene("s10", 9, "OUR PANEL", [("Live Console", "", 0.25, 1250), ("1-Click Plugin Installer", "b", 0.5, 1400),
                                         ("Version Changer", "g", 0.8, 1550)], extra_html=PANEL,
                 extra_js='    tl.fromTo("#s10-pan", { scale: 0.6, opacity: 0, y: 120 }, { scale: 1, opacity: 1, y: 0, duration: 0.5, ease: "power3.out" }, 2.6);\n'
                          '    tl.to("#s10-pan", { scale: 1.05, duration: 2.4, ease: "none" }, 3.1);\n')
C["s11"] = scene("s11", 10, "GP.AETHELGRID.CLOUD", [("Full Control Panel", "b", 0.4, 1350)])
C["s12"] = scene("s12", 11, "LIMITED-TIME OFFER", [('<span style="font-size:110px;">25% OFF</span>', "g", 0.55, 1180),
                                                   ('CODE: <span style="font-family:JB;">AETHEL25</span>', "b", 0.25, 1420)])
# S13 end card
dE = round(W["s13"][1] - W["s13"][0], 2)
C["s13"] = comp("s13", f"""    <div style="position:absolute;inset:0;background:radial-gradient(120% 80% at 50% 35%, #3b0f8a 0%, #1a0b4a 45%, {BG} 100%);"></div>
    <div class="c" id="e-logo" style="top:480px;"><img src="assets/img/logo.png" style="width:860px;height:197px;" alt="AethelGrid logo"></div>
    <div class="c h" id="e-t" style="top:760px;font-size:72px;font-weight:700;">Minecraft • VPS • Bot Hosting</div>
    <div class="c" id="e-url" style="top:930px;"><span class="badge b" style="font-size:72px;">aethelgrid.cloud</span></div>
    <div class="c" id="e-dc" style="top:1110px;"><span class="badge" style="font-size:46px;">Discord: discord.gg/GbPcdsnsNg</span></div>
    <div class="c" id="e-code" style="top:1260px;"><span class="pill">25% OFF • CODE AETHEL25</span></div>""",
                f'    tl.fromTo("#e-logo", {{ scale: 0.5, opacity: 0, filter: "blur(16px)" }}, {{ scale: 1, opacity: 1, filter: "blur(0px)", duration: 0.55, ease: "back.out(1.6)" }}, 0.05);\n'
                f'    tl.fromTo("#e-t", {{ y: 40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4 }}, 0.4);\n'
                f'    tl.fromTo("#e-url", {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2.2)" }}, {rel(12, 0.5)});\n'
                f'    tl.to("#e-url", {{ scale: 1.06, duration: 0.45, ease: "sine.inOut", yoyo: true, repeat: 4 }}, {rel(12, 0.5) + 0.45:.2f});\n'
                f'    tl.fromTo("#e-dc", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.4 }}, {rel(12, 0.5) + 0.5:.2f});\n'
                f'    tl.fromTo("#e-code", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.4 }}, {rel(12, 0.5) + 0.8:.2f});\n'
                f'    tl.to("#e-logo", {{ y: -20, duration: {max(1, dE - 1):.2f}, ease: "sine.inOut" }}, 0.7);\n')
POPS.append(round(W["s13"][0] + rel(12, 0.5), 2))

os.makedirs("compositions", exist_ok=True)
for k, v in C.items():
    open(f"compositions/{k}.html", "w").write(v)

divs = [f'      <video id="screen" src="assets/screen.mp4" muted playsinline data-start="0" data-duration="{TOTAL}" data-track-index="0" '
        f'style="position:absolute;inset:0;width:1080px;height:1920px;object-fit:cover;"></video>']
for k, s, e in SCENES:
    divs.append(f'      <div id="{k}" data-composition-id="{k}" data-composition-src="compositions/{k}.html" data-start="{s}" data-duration="{round(e - s, 3)}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: 1"></div>')


def dur(p):
    return round(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                      capture_output=True, text=True).stdout), 3)


sfx = lambda n: f"assets/sfx/{n}.mp3"
A = [("mix", "assets/audio/mix.wav", 0, min(dur("assets/audio/mix.wav"), TOTAL), 1.0, 10)]
for i, (k, s, e) in enumerate(SCENES[1:]):
    A.append((f"wh{i}", sfx("whoosh-fast-0.3s"), round(max(0, s - 0.1), 2), dur(sfx("whoosh-fast-0.3s")), 0.45, 11 + i % 2))
for i, t in enumerate(sorted(set(POPS))):
    A.append((f"pop{i}", sfx("pop-high"), t, dur(sfx("pop-high")), 0.3, 13 + i % 2))
for i, t in enumerate(CLICKS):   # owner rule: soft click sound on every click
    A.append((f"clk{i}", sfx("mouse-click"), t, dur(sfx("mouse-click")), 0.55, 15 + i % 2))
aud = "\n".join(f'      <audio id="{i}" src="{s}" data-start="{a}" data-duration="{dd}" data-volume="{v}" data-track-index="{ln}"></audio>'
                for i, s, a, dd, v, ln in A)
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
print("built", TOTAL, "clicks", CLICKS, "\n", SCENES)
