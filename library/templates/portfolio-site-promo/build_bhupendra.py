# Bhupendra portfolio walkthrough: 16:9 1920x1080, the REAL site (bhupendra.pages.dev) recorded with cursor + click ripples
# (record_bhupendra.js) inside a browser frame, a side panel with the site's own headings/words per VO line, intro title
# and end card. Recipe = decision-guide section 26 (App / website promo) + templates/website-promo (browser frame + side
# panel) + templates/screen-tutorial (speed-fit each recorded span to its VO line, clicks mapped to output time).
# Facts: library/clients/heavendeveloper/bhupendra-portfolio.md. Colours/fonts = the site's own CSS variables
# (--bg #07090d, --panel #0d1218, --ink #eef4f8, --muted #8e9bab, --ice #6fd3ff, --gold #d4af6a, --serif stack).
# Run inside the HyperFrames project:  python3 build_bhupendra.py REC_DIR VO_PARTS_DIR
#   REC_DIR/recording.mp4 + events.json (record_bhupendra.js), VO_PARTS_DIR/000.wav.. (vs_tts.py --parts)
# Writes assets/screen.mp4, assets/vo/vo.wav, assets/vo/times.json, index.html, compositions/*.html.
import json, os, subprocess, sys
import numpy as np

REC, PARTS = sys.argv[1], sys.argv[2]
BG, PANEL, INK, MUTED, ICE, GOLD = "#07090d", "#0d1218", "#eef4f8", "#8e9bab", "#6fd3ff", "#d4af6a"
SERIF = '"Iowan Old Style","Palatino Linotype",Palatino,"Noto Serif",Georgia,serif'


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                capture_output=True, text=True).stdout)


EV = json.load(open(f"{REC}/events.json"))["events"]
M = {e["name"]: e["t"] for e in EV if e["type"] == "mark"}
END_REC = json.load(open(f"{REC}/events.json"))["duration"]
VO = [f"{PARTS}/{i:03d}.wav" for i in range(12)]
vl = [dur(p) for p in VO]
# (recording start, end) per VO line, from the recorder's marks
SEG = [(0.3, M["hero"] + 2.4), (M["hero"] + 2.4, M["about"]), (M["about"], M["whatido"]), (M["whatido"], M["skills"]),
       (M["skills"], M["skills"] + 3.6), (M["skills"] + 3.6, M["skills"] + 6.9), (M["skills"] + 6.9, M["projects"]),
       (M["projects"], M["experience"]), (M["experience"], M["contact"]), (M["faq"], M["footer"]),
       (M["contact"], M["faq"]), (M["footer"], END_REC - 0.1)]
LEAD, GAP, START, END = 0.2, 0.35, 0.6, 4.2

chains, outs, plan, vo_at, t = [], [], [], [], START
for k, (a, b) in enumerate(SEG):
    need = LEAD + vl[k] + GAP
    L = b - a
    speed = min(max(L / need, 0.85), 3.0)
    d = max(L / speed, need)
    chains.append(f"[0:v]trim={a:.3f}:{b:.3f},setpts=(PTS-STARTPTS)/{speed:.4f},tpad=stop_mode=clone:stop_duration={d:.3f},trim=duration={d:.3f}[s{k}]")
    plan.append(dict(rec=(a, b), out=t, speed=speed, d=d))
    vo_at.append(t + LEAD)
    outs.append(f"[s{k}]")
    t += d
SCREEN_END = t
TOTAL = round(SCREEN_END + END, 2)
# the intro hold (first frame) and the end hold (last frame) are part of screen.mp4 so the browser never goes empty
graph = (f"[0:v]trim=start=0.3:duration=0.04,setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration={START},trim=duration={START}[pre];"
         + ";".join(chains) + f";[0:v]trim=start={END_REC - 0.2:.3f}:duration=0.04,setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration={END},trim=duration={END}[post];"
         + "[pre]" + "".join(outs) + f"[post]concat=n={len(outs) + 2}:v=1:a=0,fps=30,format=yuv420p[v]")
os.makedirs("assets/vo", exist_ok=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{REC}/recording.mp4", "-filter_complex", graph, "-map", "[v]", "-an",
                "-c:v", "libx264", "-crf", "16", "-preset", "medium", "assets/screen.mp4"], check=True)

# VO placed by time in numpy (CLAUDE.md: adelay after concat does nothing), loudnorm -16
SR = 44100
buf = np.zeros(int((TOTAL + 1) * SR), np.float32)
for p, at in zip(VO, vo_at):
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                                     capture_output=True).stdout, np.float32)
    i = int(at * SR)
    buf[i:i + len(x)] += x[: len(buf) - i]
buf[: int(TOTAL * SR)].tofile("assets/vo/raw.f32")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "assets/vo/raw.f32", "-af",
                "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", str(SR), "assets/vo/vo.wav"], check=True)
os.remove("assets/vo/raw.f32")


def out_t(rec_t):
    for p in plan:
        a, b = p["rec"]
        if a <= rec_t < b:
            return p["out"] + (rec_t - a) / p["speed"]
    return None


clicks = [round(x, 2) for x in (out_t(e["t"]) for e in EV if e["type"] in ("click", "fakeclick")) if x is not None]
json.dump(dict(vo_at=[round(v, 3) for v in vo_at], vo_len=[round(v, 3) for v in vl], clicks=clicks, total=TOTAL,
               plan=[(p["rec"], round(p["out"], 2), round(p["speed"], 2), round(p["d"], 2)) for p in plan]),
          open("assets/vo/times.json", "w"), indent=0)

# side panel per VO line: the site's own section label, a heading and its words (chips)
PANELS = [
    ("HI, I'M", "Bhupendra", ["Independent Developer", "Nepal"]),
    ("INDEPENDENT DEVELOPER", "Discord bots, websites &amp; custom software", ["Useful features", "Clean design", "Reliable functionality"]),
    ("ABOUT ME", "Self-taught, since around 2024", ["Smaller projects first", "Then more complex ideas", "Performance &amp; presentation"]),
    ("WHAT I DO", "Seven kinds of work", ["Discord bots", "Websites", "Minecraft plugins", "Minecraft mods", "Resource packs", "Python &amp; Node.js", "Custom development"]),
    ("SKILLS • DISCORD BOTS", "Discord bots", ["Commands &amp; interactions", "Server automation", "Custom bot features", "Python", "Node.js"]),
    ("SKILLS • WEBSITES", "Websites", ["Responsive layouts", "Frontend implementation", "UI styling"]),
    ("SKILLS • MINECRAFT", "Minecraft development", ["Plugins", "Mods", "Resource packs", "Custom features"]),
    ("PROJECTS", "Heaven Developer", ["Discord development community", "Service project", "Status: In progress"]),
    ("HOW I WORK", "Four steps", ["01 Brief", "02 Build", "03 Test", "04 Deliver"]),
    ("FAQ • QUOTES", "Simple projects may be free", ["At his discretion", "Advanced projects quoted individually"]),
    ("LET'S WORK TOGETHER", "Message me on Discord", ["Bhupendra 67", "guns.lol/bhupendra67", "YouTube @chrxsz_editss"]),
    ("DESIGNED AND CODED BY", "Bhupendra", ["bhupendra.pages.dev"]),
]
CSS = f"""
    #root {{ position: absolute; inset: 0; overflow: hidden; }}
    .se {{ font-family: {SERIF}; color: {INK}; }}
    .lab {{ display: inline-block; font-family: system-ui, sans-serif; font-weight: 700; font-size: 22px; letter-spacing: 4px; color: {ICE};
            padding: 10px 20px; border: 1.5px solid rgba(111,211,255,.35); border-radius: 999px; background: rgba(13,18,24,.9); }}
    .chip {{ display: inline-block; font-family: system-ui, sans-serif; font-weight: 600; font-size: 27px; color: {INK}; margin: 0 10px 14px 0;
             padding: 12px 20px; border-radius: 14px; background: {PANEL}; border: 1.5px solid rgba(111,211,255,.16); }}
"""


def comp(cid, html, js, w=1920, h=1080):
    return f"""<template>
  <style>{CSS}</style>
  <div id="root" data-composition-id="{cid}" data-width="{w}" data-height="{h}">
{html}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{js}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
"""


C = {}
# background + browser frame with the recording (one long video, never empty)
C["bg"] = comp("bg", f"""    <div style="position:absolute;inset:0;background:radial-gradient(90% 70% at 30% 40%, #0f1a24 0%, {BG} 70%);"></div>
    <div id="bg-g" style="position:absolute;left:-300px;top:-200px;width:1200px;height:1200px;border-radius:50%;background:radial-gradient(circle, rgba(111,211,255,.10), rgba(111,211,255,0) 70%);" data-layout-allow-overflow></div>
    <div id="bg-g2" style="position:absolute;left:1300px;top:500px;width:900px;height:900px;border-radius:50%;background:radial-gradient(circle, rgba(212,175,106,.08), rgba(212,175,106,0) 70%);" data-layout-allow-overflow></div>""",
               f'    tl.fromTo("#bg-g", {{ x: 0, scale: 0.9 }}, {{ x: 500, scale: 1.2, duration: {TOTAL}, ease: "sine.inOut" }}, 0);\n'
               f'    tl.fromTo("#bg-g2", {{ y: 0 }}, {{ y: -400, duration: {TOTAL}, ease: "sine.inOut" }}, 0);\n')
BW, BH = 1270, 714  # 1920x1080 recording at 0.6615
C["browser"] = comp("browser", f"""    <div id="br" style="position:absolute;left:56px;top:150px;width:{BW}px;height:{BH + 52}px;border-radius:18px;overflow:hidden;background:{PANEL};border:1.5px solid rgba(111,211,255,.25);box-shadow:0 40px 120px rgba(0,0,0,.7), 0 0 60px rgba(111,211,255,.10);">
      <div style="height:52px;display:flex;align-items:center;gap:10px;padding-left:20px;background:#0b1016;border-bottom:1.5px solid rgba(111,211,255,.16);">
        <span style="width:14px;height:14px;border-radius:50%;background:#ff5f57;"></span><span style="width:14px;height:14px;border-radius:50%;background:#febc2e;"></span><span style="width:14px;height:14px;border-radius:50%;background:#28c840;"></span>
        <span style="margin-left:24px;font-family:system-ui,sans-serif;font-size:22px;color:{MUTED};background:{BG};padding:6px 22px;border-radius:10px;">bhupendra.pages.dev</span></div>
      <video id="br-v" src="assets/screen.mp4" data-start="0" data-duration="{TOTAL}" muted playsinline style="display:block;width:{BW}px;height:{BH}px;"></video>
    </div>""",
                    '    tl.fromTo("#br", { y: 60, opacity: 0, scale: 0.96 }, { y: 0, opacity: 1, scale: 1, duration: 0.6, ease: "power3.out" }, 0);\n')
# top title strip (on screen from 0 s = thumbnail)
C["top"] = comp("top", f"""    <div id="tp" style="position:absolute;left:56px;top:46px;display:flex;align-items:baseline;gap:22px;">
      <span class="se" style="font-size:62px;">Bhupendra</span><span style="font-family:system-ui,sans-serif;font-size:28px;color:{ICE};letter-spacing:5px;">PORTFOLIO • INDEPENDENT DEVELOPER</span></div>""",
                '    tl.fromTo("#tp", { x: -40, opacity: 0 }, { x: 0, opacity: 1, duration: 0.5, ease: "power3.out" }, 0);\n')

times = json.load(open("assets/vo/times.json"))
scenes = []
for i, (lab, title, chips) in enumerate(PANELS):
    s = 0.0 if i == 0 else round(vo_at[i] - 0.25, 2)
    e = round(vo_at[i + 1] - 0.25, 2) if i + 1 < len(PANELS) else TOTAL
    d = round(e - s, 2)
    k = f"p{i + 1}"
    ch = "".join(f'<span class="chip" id="{k}-c{j}">{c}</span>' for j, c in enumerate(chips))
    js = (f'    tl.fromTo("#{k}-l", {{ y: 20, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.3, ease: "power2.out" }}, 0.05);\n'
          f'    tl.fromTo("#{k}-t", {{ y: 40, opacity: 0, filter: "blur(10px)" }}, {{ y: 0, opacity: 1, filter: "blur(0px)", duration: 0.45, ease: "power3.out" }}, 0.12);\n'
          f'    tl.fromTo("#{k}-bar", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.5, ease: "power3.out" }}, 0.2);\n')
    for j in range(len(chips)):
        js += f'    tl.fromTo("#{k}-c{j}", {{ y: 24, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.3, ease: "back.out(1.8)" }}, {0.35 + j * min(0.35, (vl[i] * 0.8) / max(1, len(chips))):.2f});\n'
    js += f'    tl.to("#{k}-w", {{ x: 40, opacity: 0, duration: 0.25, ease: "power2.in" }}, {max(0.5, d - 0.25):.2f});\n' if i + 1 < len(PANELS) else ""
    C[k] = comp(k, f"""    <div id="{k}-w" style="position:absolute;left:1380px;top:170px;width:500px;">
      <div id="{k}-l"><span class="lab">{lab}</span></div>
      <div class="se" id="{k}-t" style="margin-top:30px;font-size:{60 if len(title) < 24 else 50}px;line-height:1.1;">{title}</div>
      <div id="{k}-bar" style="margin:26px 0 30px;width:120px;height:4px;background:linear-gradient(90deg,{ICE},{GOLD});transform-origin:left;"></div>
      <div>{ch}</div>
    </div>""", js)
    scenes.append((k, s, d))

# end card over the last hold: name, Discord / guns.lol / YouTube, URL (all from the site's contact section)
es = round(SCREEN_END - 0.2, 2)
ed = round(TOTAL - es, 2)
C["end"] = comp("end", f"""    <div id="en" style="position:absolute;inset:0;background:rgba(7,9,13,.82);">
      <div class="se" id="en-n" style="position:absolute;left:0;right:0;top:300px;text-align:center;font-size:130px;">Bhupendra</div>
      <div id="en-s" style="position:absolute;left:0;right:0;top:470px;text-align:center;font-family:system-ui,sans-serif;font-size:34px;letter-spacing:8px;color:{ICE};">INDEPENDENT DEVELOPER • NEPAL</div>
      <div id="en-l" style="position:absolute;left:0;right:0;top:580px;display:flex;justify-content:center;gap:24px;">
        <span class="chip" style="font-size:32px;border-color:rgba(111,211,255,.5);">Discord: Bhupendra 67</span><span class="chip" style="font-size:32px;">guns.lol/bhupendra67</span><span class="chip" style="font-size:32px;">YouTube @chrxsz_editss</span></div>
      <div id="en-u" style="position:absolute;left:0;right:0;top:720px;text-align:center;"><span style="font-family:system-ui,sans-serif;font-weight:700;font-size:54px;color:{BG};background:{ICE};padding:20px 50px;border-radius:999px;">bhupendra.pages.dev</span></div>
    </div>""",
               '    tl.fromTo("#en", { opacity: 0 }, { opacity: 1, duration: 0.4 }, 0);\n'
               '    tl.fromTo("#en-n", { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: "power3.out" }, 0.15);\n'
               '    tl.fromTo("#en-s", { opacity: 0 }, { opacity: 1, duration: 0.4 }, 0.4);\n'
               '    tl.fromTo("#en-l", { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: "power3.out" }, 0.6);\n'
               '    tl.fromTo("#en-u", { scale: 0.5, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.45, ease: "back.out(2)" }, 0.9);\n')

os.makedirs("compositions", exist_ok=True)
for k, v in C.items():
    open(f"compositions/{k}.html", "w").write(v)
div = lambda k, s, d, lane, z: (f'      <div id="{k}" data-composition-id="{k}" data-composition-src="compositions/{k}.html" data-start="{s}" data-duration="{d}" '
                                f'data-track-index="{lane}" data-track-kind="graphics" data-width="1920" data-height="1080" style="z-index: {z}"></div>')
divs = [div("bg", 0, TOTAL, 0, 0), div("browser", 0, TOTAL, 1, 1), div("top", 0, TOTAL, 2, 2)]
divs += [div(k, s, d, 3, 3) for k, s, d in scenes]
divs.append(div("end", es, ed, 4, 4))
sfx = lambda n: f"assets/sfx/{n}.mp3"
A = [("mix", "assets/audio/mix.wav" if os.path.exists("assets/audio/mix.wav") else "assets/vo/vo.wav", 0, TOTAL, 1.0, 10)]
for j, c in enumerate(clicks):
    A.append((f"ck{j}", sfx("click-1"), c, round(dur(sfx("click-1")), 3), 0.5, 11 + j % 2))
for j, (k, s, d) in enumerate(scenes[1:]):
    A.append((f"wh{j}", sfx("whoosh-fast-0.3s"), round(s, 2), round(dur(sfx("whoosh-fast-0.3s")), 3), 0.25, 13 + j % 2))
A.append(("endfx", sfx("sparkle"), round(es + 0.9, 2), round(dur(sfx("sparkle")), 3), 0.35, 15))
aud = "\n".join(f'      <audio id="{a}" src="{s}" data-start="{b}" data-duration="{dd}" data-volume="{v}" data-track-index="{ln}"></audio>' for a, s, b, dd, v, ln in A)
open("index.html", "w").write(f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="assets/vendor/gsap-3.14.2.min.js"></script>
    <style>* {{ margin: 0; padding: 0; box-sizing: border-box; }} html, body {{ margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: {BG}; }}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1920" data-height="1080">
{chr(10).join(divs)}
{aud}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
""")
print("built", TOTAL, "s;", len(scenes), "panels;", len(clicks), "clicks")
