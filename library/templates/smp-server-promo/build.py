# Minecraft SMP server promo (16:9 and 9:16 from one config), voice-led: one scene per VO line. Made for the owner's
# FireCraft SMP on 2026-10-29 from three sources only: in-game camera shots taken with the WorldLens plugin
# (mcp worldlens_shot, spawn chunks force-loaded for the shots and released after), the server's Discord
# (announcements / rules / ip-port channels read with discord_read_messages) and firecraft.fun (web_capture.py).
# Every on-screen claim must come from those sources (CLAUDE.md VERIFIED ONLY); the config keeps a "source" per scene.
# Skills: #96 reel shot budget (a new picture every line, nothing static > ~3 s: Ken Burns on stills), #104 hook < 3 s
# (title on screen at 0 s), CLAUDE.md "HyperFrames learnings" (first frame = title, unique ids, visibility windows,
# audio data-duration), music-for-video skill (one mixed VO + music track from mix_vo_music.py).
#
#   python3 build.py CONFIG.json --format 16x9|9x16 --out PROJECT_DIR
#
# CONFIG: brand {name, sub, colours}, vo_lines (path to vs_tts --parts lines.json), audio (mixed track), scenes:
#   [{line, kind: shot|art|powers|cta, img|imgs, title, sub, source}] in VO order; end_hold seconds after the last line.
# PROJECT_DIR holds assets/vendor/gsap-3.14.2.min.js, assets/fonts (Anton, Poppins), assets/img/*, assets/sfx/*,
# assets/audio/mix.wav.
import argparse, json, os, subprocess

ap = argparse.ArgumentParser()
ap.add_argument("config")
ap.add_argument("--format", choices=["16x9", "9x16"], default="16x9")
ap.add_argument("--out", required=True)
a = ap.parse_args()
C = json.load(open(a.config))
os.chdir(a.out)
WIDE = a.format == "16x9"
W, H = (1920, 1080) if WIDE else (1080, 1920)
COL = C["brand"]["colours"]          # {"fire": "#ff4d1a", "gold": "#ffc21a", "red": "#e0141e", "dark": "#0b0b0f"}
LINES = json.load(open(C["vo_lines"]))
VO0 = C.get("vo_start", 0.6)          # VO starts after the hook title has landed


def r3(x):
    return round(x, 3)


def dur(p):
    return round(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                      capture_output=True, text=True).stdout), 3)


SC = C["scenes"]
for i, s in enumerate(SC):
    s0 = 0 if i == 0 else r3(VO0 + LINES[s["line"]][0] - 0.15)
    s["t0"] = s0
for i, s in enumerate(SC):
    s["t1"] = SC[i + 1]["t0"] if i + 1 < len(SC) else r3(VO0 + LINES[-1][1] + C.get("end_hold", 3.5))
TOTAL = SC[-1]["t1"]
T, A, HTML, PRE = [], [], [], []


def sfx(f, t, v, d=None):
    A.append((f, r3(max(0, t)), v, d))


def win(sel, s0, s1):
    if s0 > 0:
        PRE.append(f'gsap.set("{sel}", {{visibility:"hidden"}});')
        T.append(f'tl.set("{sel}", {{visibility:"visible"}}, {r3(s0)});')
    if s1 < TOTAL:
        T.append(f'tl.set("{sel}", {{visibility:"hidden"}}, {r3(s1)});')


TS = 1.0 if WIDE else 1.25            # text scale for portrait


def title_block(i, s, top):
    t = s.get("title", "")
    sub = s.get("sub", "")
    return (f'<div id="sc{i}tb" style="position:absolute;left:60px;right:60px;top:{top}px;text-align:center;">'
            f'<div class="mask" data-layout-allow-overflow><div id="sc{i}tt" class="anton fire-text" style="font-size:{int(118 * TS)}px;line-height:1.02;">{t}</div></div>'
            + (f'<div id="sc{i}ts" class="pop" style="display:inline-block;margin-top:{int(14 * TS)}px;font-size:{int(40 * TS)}px;color:#fff;'
               f'background:rgba(0,0,0,0.55);border:2px solid {COL["gold"]};padding:6px 22px;border-radius:12px;">{sub}</div>' if sub else "")
            + '</div>')


ttop = 850 if WIDE else 1250
for i, s in enumerate(SC):
    k = s["kind"]
    d = r3(s["t1"] - s["t0"])
    parts = []
    if k in ("shot", "art"):
        # still picture with a slow push-in (Ken Burns) so nothing sits frozen (#96)
        if WIDE:
            parts.append(f'<div id="sc{i}ph" class="photo" style="background-image:url({s["img"]});"></div>')
        else:
            # portrait: a 16:9 picture cropped to 9:16 loses the subject (logo cut to "RECRA" in the first test), so show
            # the whole picture as a card over a blurred, darkened copy of itself
            parts.append(f'<div class="photo" style="background-image:url({s["img"]});filter:blur(28px) brightness(0.55);transform:scale(1.15);"></div>'
                         f'<div id="sc{i}ph" class="photo" style="background-image:url({s["img"]});background-size:contain;background-repeat:no-repeat;'
                         f'background-position:center 300px;"></div>')
        z0, z1 = (1.04, 1.16) if i % 2 == 0 else (1.16, 1.04)
        T.append(f'tl.fromTo("#sc{i}ph", {{scale:{z0}}}, {{scale:{z1}, duration:{d}, ease:"none"}}, {s["t0"]});')
        parts.append('<div class="veil"></div>')
        parts.append(title_block(i, s, ttop))
    elif k == "powers":
        imgs = s["imgs"]
        cols = 6 if WIDE else 4
        size = 230 if WIDE else 220
        gap = 26
        rows = (len(imgs) + cols - 1) // cols
        y0 = 120 if WIDE else 360
        cells = []
        for j, im in enumerate(imgs):
            r, q = divmod(j, cols)
            n_in_row = min(cols, len(imgs) - r * cols)
            x = (W - (n_in_row * size + (n_in_row - 1) * gap)) // 2 + q * (size + gap)
            y = y0 + r * (size + gap + 30)
            nm = os.path.splitext(os.path.basename(im))[0].replace("power-", "").upper()
            cells.append(f'<div id="sc{i}p{j}" class="pw" style="left:{x}px;top:{y}px;width:{size}px;">'
                         f'<img src="{im}" alt="{nm} power" style="width:{size}px;height:{size}px;border-radius:50%;">'
                         f'<div class="pop" style="text-align:center;color:#fff;font-size:{int(28 * TS)}px;margin-top:4px;">{nm}</div></div>')
            T.append(f'tl.fromTo("#sc{i}p{j}", {{scale:0, rotation:-25, opacity:0}}, {{scale:1, rotation:0, opacity:1, duration:0.3, '
                     f'ease:"back.out(2)"}}, {r3(s["t0"] + 0.1 + j * 0.09)});')
        parts.append(f'<div class="bgfire"></div>{"".join(cells)}')
        parts.append(title_block(i, s, (y0 + rows * (size + gap + 30) + 10) if WIDE else 1440))
    elif k == "cta":
        lg = 420 if WIDE else 560
        parts.append(f'<div class="bgfire"></div><img id="sc{i}lg" src="{s["img"]}" alt="{C["brand"]["name"]} logo" '
                     f'style="position:absolute;left:{(W - lg) // 2}px;top:{40 if WIDE else 220}px;width:{lg}px;height:{lg}px;border-radius:50%;box-shadow:0 0 60px {COL["fire"]};">')
        rows = "".join(f'<div id="sc{i}r{j}" class="ctarow"><span class="pop" style="color:{COL["gold"]};">{lab}</span>'
                       f'<span class="pop" style="color:#fff;">{val}</span></div>' for j, (lab, val) in enumerate(s["rows"]))
        ty = (40 + lg + 20) if WIDE else (220 + lg + 60)
        parts.append(f'<div style="position:absolute;left:0;right:0;top:{ty}px;text-align:center;">'
                     f'<div id="sc{i}btn" style="display:inline-block;" class="pop cta-btn">{s["title"]}</div>'
                     f'<div style="margin-top:{int(22 * TS)}px;">{rows}</div></div>')
        T.append(f'tl.fromTo("#sc{i}lg", {{scale:0.3, rotation:-15, opacity:0}}, {{scale:1, rotation:0, opacity:1, duration:0.5, ease:"back.out(1.8)"}}, {s["t0"]});')
        T.append(f'tl.to("#sc{i}lg", {{scale:1.04, duration:0.6, yoyo:true, repeat:5, ease:"sine.inOut"}}, {r3(s["t0"] + 0.6)});')
        T.append(f'tl.fromTo("#sc{i}btn", {{scale:0, opacity:0}}, {{scale:1, opacity:1, duration:0.35, ease:"back.out(2.4)"}}, {r3(s["t0"] + 0.35)});')
        T.append(f'tl.to("#sc{i}btn", {{scale:1.07, duration:0.4, yoyo:true, repeat:7, ease:"sine.inOut"}}, {r3(s["t0"] + 0.9)});')
        for j in range(len(s["rows"])):
            T.append(f'tl.fromTo("#sc{i}r{j}", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.25}}, {r3(s["t0"] + 0.6 + 0.15 * j)});')
        sfx("impact-boom", s["t0"], 0.4)
        sfx("pop-high", s["t0"] + 0.35, 0.45)
    HTML.append(f'<div id="sc{i}" class="scene">' + "".join(parts) + "</div>")
    # title slams in; scene enters with a whip + whoosh (first scene is already on screen at 0 s for the thumbnail)
    if k != "cta":
        if i == 0:
            T.append(f'tl.fromTo("#sc{i}tt", {{scale:1.0}}, {{scale:1.06, duration:0.5, yoyo:true, repeat:1, ease:"sine.inOut"}}, 0.2);')
        else:
            T.append(f'tl.fromTo("#sc{i}tt", {{yPercent:110}}, {{yPercent:0, duration:0.25, ease:"power4.out"}}, {r3(s["t0"] + 0.12)});')
        if s.get("sub"):
            T.append(f'tl.fromTo("#sc{i}ts", {{scale:0, opacity:0}}, {{scale:1, opacity:1, duration:0.3, ease:"back.out(2.2)"}}, {r3(s["t0"] + 0.45)});')
            sfx("pop-high", s["t0"] + 0.5, 0.35)
    if i > 0:
        T.append(f'tl.fromTo("#sc{i}", {{x:{W * 0.25:.0f}, filter:"blur(14px)", opacity:0}}, {{x:0, filter:"blur(0px)", opacity:1, duration:0.28, ease:"power3.out"}}, {s["t0"]});')
        sfx("whoosh-fast-0.3s", s["t0"] - 0.03, 0.5)
        if k != "cta":
            sfx("impact-punch", s["t0"] + 0.15, 0.3)
    win(f"#sc{i}", s["t0"], s["t1"])

# fire embers overlay + vignette (own CC0 overlay from library/stock)
emb = []
k_, t_ = 0, 0.0
ED = dur("assets/img/embers.mp4")
while t_ < TOTAL:
    emb.append(f'<video id="em{k_}" src="assets/img/embers.mp4" data-start="{r3(t_)}" data-duration="{r3(min(ED, TOTAL - t_))}" muted playsinline '
               f'style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;mix-blend-mode:screen;opacity:0.55;"></video>')
    t_ += ED
    k_ += 1

CSS = f"""
@font-face {{ font-family: "Anton"; src: url("assets/fonts/Anton-Regular.ttf"); }}
@font-face {{ font-family: "Poppins"; src: url("assets/fonts/Poppins-ExtraBold.ttf"); font-weight: 800; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:{COL["dark"]}; }}
#root {{ position:absolute; inset:0; overflow:hidden; background:{COL["dark"]}; }}
.scene {{ position:absolute; inset:0; overflow:hidden; }}
.photo {{ position:absolute; inset:0; background-size:cover; background-position:center; }}
.veil {{ position:absolute; inset:0; background:linear-gradient(180deg, rgba(0,0,0,0.0) 35%, rgba(0,0,0,0.75) 100%); }}
.bgfire {{ position:absolute; inset:0; background:radial-gradient(ellipse 70% 60% at 50% 45%, #3a0d05 0%, #140606 55%, {COL["dark"]} 100%); }}
.anton {{ font-family:Anton; letter-spacing:2px; }}
.pop {{ font-family:Poppins; font-weight:800; }}
.mask {{ overflow:hidden; }}
.fire-text {{ color:#fff; text-shadow:0 0 18px {COL["fire"]}, 0 6px 0 {COL["red"]}, 0 10px 24px rgba(0,0,0,0.8); }}
.pw {{ position:absolute; }}
.cta-btn {{ background:linear-gradient(90deg,{COL["red"]},{COL["fire"]},{COL["gold"]}); color:#fff; font-size:{58 if WIDE else 56}px; white-space:nowrap;
           padding:12px 44px; border-radius:18px; box-shadow:0 0 30px {COL["fire"]}; }}
.ctarow {{ display:flex; justify-content:center; gap:16px; font-size:{int(38 * TS)}px; margin:8px 0; }}
"""
mix_d = dur(C["audio"])
audio = [f'<audio id="mix" src="{C["audio"]}" data-start="0" data-duration="{min(TOTAL, mix_d)}" data-volume="1" data-track-index="1"></audio>']
lanes = []
for n, (f, s, v, d) in enumerate(sorted(A, key=lambda x: x[1])):
    p = f"assets/sfx/{f}.mp3"
    d = min(d or dur(p), dur(p), r3(TOTAL - s))
    k = next((j for j, end in enumerate(lanes) if end <= s), None)
    if k is None:
        lanes.append(0)
        k = len(lanes) - 1
    lanes[k] = s + d + 0.01
    audio.append(f'<audio id="sx{n}" src="{p}" data-start="{s}" data-duration="{r3(d)}" data-volume="{v}" data-track-index="{2 + k}"></audio>')

html = f"""<!doctype html>
<html lang="en" data-resolution="{"landscape" if WIDE else "portrait"}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width={W}, height={H}">
<script src="assets/vendor/gsap-3.14.2.min.js"></script>
<style>{CSS}</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="{W}" data-height="{H}">
  {chr(10).join(HTML)}
  {chr(10).join(emb)}
  {chr(10).join(audio)}
</div>
<script>
  {chr(10).join("  " + l for l in PRE)}
  const tl = gsap.timeline({{ paused: true }});
  {chr(10).join("  " + l for l in T)}
  tl.to({{}}, {{ duration: {TOTAL} }}, 0);
  window.__timelines = window.__timelines || {{}};
  window.__timelines["main"] = tl;
</script>
</body>
</html>
"""
open("index.html", "w").write(html)
json.dump({"total": TOTAL, "scenes": [[s["t0"], s["t1"], s.get("title", "")] for s in SC]}, open("timing.json", "w"), indent=1)
print(f"built {a.format}: {TOTAL} s, {len(SC)} scenes, {len(A)} sfx")
