# Web panel / SaaS promo (16:9 or 9:16) from real screen recordings + one finished voice-over. First used for
# copper_work (plugin.firecraft.fun, owner's own product) on 2026-11-07.
# Picture = recordings from flow_*.js (screen_recorder.js: cursor + ripple on every click, privacy mask), one span per
# scene, speed-fitted to the scene's slice of the VO (site-panel-reel idea). On top: one small caption card per scene
# quoting the site (title + sub or chips), an end card, and click / whoosh SFX (2-3 rotating variants per type: Mr Aloo
# feedback "same pop repeated sounds cheap"). Look = the product's own tokens (config "look"), no eyebrow labels, no
# tracked caps, no single coloured word (Hallmark floor, references/gates.md section 4).
#   python3 build.py CONFIG.json --format 16x9|9x16 --out PROJECT
# CONFIG: total, vo_at, look {bg, panel, text, muted, accent, ok, font, mono}, brand {name, url, icon},
#   scenes [{id, start, rec, a, b, title, sub, chips, big}] (start = video time; the last scene runs to total; rec spans
#   from the recordings of this format: <PROJECT>/rec/<rec>/{recording.mp4,events.json}).
# PROJECT holds assets/vendor/gsap-3.14.2.min.js, assets/fonts/{sans,mono}.woff2, assets/img/icon.svg, assets/sfx/*.mp3,
# assets/audio/mix.wav (VO + music, mix_vo_music.py).
import argparse, html, json, os, subprocess

ap = argparse.ArgumentParser()
ap.add_argument("config")
ap.add_argument("--format", choices=["16x9", "9x16"], default="16x9")
ap.add_argument("--out", required=True)
a = ap.parse_args()
C = json.load(open(a.config))
os.chdir(a.out)
WIDE = a.format == "16x9"
W, H = (1920, 1080) if WIDE else (1080, 1920)
L = C["look"]
TOTAL = C["total"]
SC = C["scenes"]
for i, s in enumerate(SC):
    s["end"] = SC[i + 1]["start"] if i + 1 < len(SC) else TOTAL
E = lambda t: html.escape(str(t))


def run(*x):
    subprocess.run(x, check=True, capture_output=True)


def dur(p):
    return round(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                      capture_output=True, text=True).stdout), 3)


# ---------- picture: one speed-fitted span per scene ----------
os.makedirs("assets/clips", exist_ok=True)
CLICKS, parts = [], []
for s in SC:
    d = round(s["end"] - s["start"], 3)
    out = f"assets/clips/{s['id']}.mp4"
    span = s["b"] - s["a"]
    speed = span / d
    vf = (f"setpts=(PTS-STARTPTS)/{speed:.5f},fps=30,scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},"
          f"tpad=stop_mode=clone:stop_duration={d},trim=0:{d},setpts=PTS-STARTPTS,format=yuv420p")
    run("ffmpeg", "-y", "-ss", str(s["a"]), "-t", str(span + 0.3), "-i", f"rec/{s['rec']}/recording.mp4", "-an", "-vf", vf,
        "-t", str(d), "-c:v", "libx264", "-crf", "16", "-r", "30", out)
    for x in json.load(open(f"rec/{s['rec']}/events.json"))["events"]:
        if x["type"] in ("click", "fakeclick") and s["a"] <= x["t"] <= s["b"]:
            CLICKS.append(round(s["start"] + (x["t"] - s["a"]) / speed, 2))
    s["speed"] = round(speed, 2)
    parts.append(out)
open("assets/clips/list.txt", "w").write("".join(f"file '{os.path.basename(p)}'\n" for p in parts))
run("ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "assets/clips/list.txt", "-c", "copy", "assets/screen.mp4")

# ---------- overlays ----------
F = 1.0 if WIDE else 1.15
CSS = f"""
@font-face {{ font-family: "S"; src: url("assets/fonts/sans.woff2"); font-weight: 100 900; }}
@font-face {{ font-family: "M"; src: url("assets/fonts/mono.woff2"); font-weight: 100 900; }}
#root {{ position: absolute; inset: 0; overflow: hidden; font-family: S; color: {L['text']}; }}
.card {{ position: absolute; {'left: 72px; bottom: 72px; width: 860px;' if WIDE else 'left: 56px; right: 56px; bottom: 150px;'}
        background: {L['panel']}; border: 1px solid rgba(255,255,255,0.10); border-radius: 18px; padding: {int(30 * F)}px {int(36 * F)}px;
        box-shadow: 0 24px 60px rgba(0,0,0,0.55); }}
.card::before {{ content: ""; position: absolute; left: 0; top: 22px; bottom: 22px; width: 5px; border-radius: 3px; background: {L['accent']}; }}
.t {{ font-weight: 700; font-size: {int(58 * F)}px; line-height: 1.08; letter-spacing: -1px; }}
.s {{ font-weight: 400; font-size: {int(32 * F)}px; color: {L['muted']}; margin-top: 12px; line-height: 1.3; }}
.chips {{ margin-top: 18px; display: flex; flex-wrap: wrap; gap: 12px; }}
.chip {{ font-family: M; font-size: {int(28 * F)}px; padding: 8px 18px; border-radius: 10px; background: rgba(255,255,255,0.05);
         border: 1px solid rgba(255,255,255,0.12); color: {L['text']}; }}
.big {{ position: absolute; left: 0; right: 0; top: {H // 2 - int(90 * F)}px; text-align: center; }}
.big span {{ display: inline-block; font-weight: 800; font-size: {int(150 * F)}px; letter-spacing: -4px; color: {L['ok']};
            background: rgba(10,10,10,0.82); padding: 10px 56px; border-radius: 28px; border: 2px solid {L['ok']}; }}
.brand {{ position: absolute; {'left: 72px; top: 60px;' if WIDE else 'left: 56px; top: 90px;'} display: flex; align-items: center; gap: 16px;
          background: rgba(24,24,24,0.9); border: 1px solid rgba(255,255,255,0.12); border-radius: 14px; padding: 12px 22px; }}
.brand img {{ width: 44px; height: 44px; }}
.brand b {{ font-size: 34px; font-weight: 700; }}
.brand i {{ font-style: normal; font-family: M; font-size: 26px; color: {L['muted']}; }}
"""


def comp(cid, body, js):
    return f"""<template>
  <style>{CSS}</style>
  <div id="root" data-composition-id="{cid}" data-width="{W}" data-height="{H}">
{body}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{js}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
"""


POPS = []
B = C["brand"]
os.makedirs("compositions", exist_ok=True)
for i, s in enumerate(SC):
    k, d = s["id"], round(s["end"] - s["start"], 2)
    body, js = "", ""
    if i == 0 and B.get("chip", True):   # brand chip from frame 0 (thumbnail); off when the first shot already shows the brand
        body += (f'<div class="brand" id="{k}-br"><img src="{B["icon"]}" alt="{E(B["name"])} icon"><b>{E(B["name"])}</b>'
                 f'<i>{E(B["url"])}</i></div>')
    if s.get("big"):
        body += f'<div class="big" id="{k}-big"><span>{E(s["big"])}</span></div>'
        js += f'    tl.fromTo("#{k}-big", {{ scale: 0.4, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2.2)" }}, 0.1);\n'
        POPS.append(round(s["start"] + 0.2, 2))
    if s.get("title"):
        chips = "".join(f'<span class="chip" id="{k}-c{j}">{E(c)}</span>' for j, c in enumerate(s.get("chips", [])))
        body += (f'<div class="card" id="{k}-card"><div class="t">{E(s["title"])}</div>'
                 + (f'<div class="s">{E(s["sub"])}</div>' if s.get("sub") else "")
                 + (f'<div class="chips">{chips}</div>' if chips else "") + "</div>")
        js += f'    tl.fromTo("#{k}-card", {{ y: 60, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "power3.out" }}, 0.15);\n'
        for j in range(len(s.get("chips", []))):
            t = round(0.5 + j * min(0.45, (d - 1.2) / max(1, len(s["chips"]))), 2)
            js += f'    tl.fromTo("#{k}-c{j}", {{ scale: 0.6, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.25, ease: "back.out(2)" }}, {t});\n'
    if s.get("end_card"):
        ec = s["end_card"]
        body += f"""<div style="position:absolute;inset:0;background:{L['bg']};" id="{k}-bg"></div>
    <div style="position:absolute;left:0;right:0;top:{H // 2 - int(260 * F)}px;text-align:center;" id="{k}-e">
      <img src="{B['icon']}" style="width:{int(150 * F)}px;height:{int(150 * F)}px;" alt="{E(B['name'])} icon">
      <div style="font-weight:800;font-size:{int(110 * F)}px;letter-spacing:-3px;margin-top:24px;">{E(B['name'])}</div>
      <div style="font-size:{int(44 * F)}px;color:{L['muted']};margin-top:10px;">{E(ec['line'])}</div>
      <div style="margin-top:44px;"><span id="{k}-cta" style="display:inline-block;font-weight:700;font-size:{int(52 * F)}px;color:#141414;background:{L['accent']};padding:20px 46px;border-radius:16px;">{E(ec['cta'])}</span></div>
      <div style="font-family:M;font-size:{int(46 * F)}px;margin-top:30px;">{E(B['url'])}</div>
    </div>"""
        t0 = ec.get("at", 1.5)
        js += (f'    tl.fromTo("#{k}-bg", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.35 }}, {t0});\n'
               f'    tl.fromTo("#{k}-e", {{ y: 50, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.45, ease: "power3.out" }}, {t0 + 0.15});\n'
               f'    tl.to("#{k}-cta", {{ scale: 1.05, duration: 0.5, yoyo: true, repeat: 5, ease: "sine.inOut" }}, {t0 + 0.8});\n')
        POPS.append(round(s["start"] + t0 + 0.2, 2))
    elif s.get("title") or s.get("big"):
        js += f'    tl.to("#root", {{ opacity: 0, duration: 0.15 }}, {max(0.3, d - 0.15):.2f});\n'
    s["comp"] = bool(body)
    if body:
        open(f"compositions/{k}.html", "w").write(comp(k, body, js))

divs = [f'      <video id="screen" src="assets/screen.mp4" muted playsinline data-start="0" data-duration="{TOTAL}" data-track-index="0" '
        f'style="position:absolute;inset:0;width:{W}px;height:{H}px;object-fit:cover;"></video>']
for s in SC:
    if s["comp"]:
        divs.append(f'      <div id="{s["id"]}" data-composition-id="{s["id"]}" data-composition-src="compositions/{s["id"]}.html" data-start="{s["start"]}" '
                    f'data-duration="{round(s["end"] - s["start"], 3)}" data-track-index="1" data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index: 1"></div>')

sfx = lambda n: f"assets/sfx/{n}.mp3"
WH = ["whoosh-fast-0.3s", "swish-1", "swish-4"]          # rotate variants
CK = ["mouse-click", "click-1", "click-2"]
PP = ["pop-high", "pop-low", "plop"]
A = [("mix", "assets/audio/mix.wav", 0, min(dur("assets/audio/mix.wav"), TOTAL), 1.0)]
A += [(f"wh{i}", sfx(WH[i % 3]), round(max(0, s["start"] - 0.12), 2), dur(sfx(WH[i % 3])), 0.35) for i, s in enumerate(SC[1:])]
A += [(f"ck{i}", sfx(CK[i % 3]), t, dur(sfx(CK[i % 3])), 0.5) for i, t in enumerate(CLICKS)]
A += [(f"pp{i}", sfx(PP[i % 3]), t, dur(sfx(PP[i % 3])), 0.3) for i, t in enumerate(sorted(set(POPS)))]
lanes, aud = [], []
for n, (i, p, st, dd, v) in enumerate(sorted(A, key=lambda x: x[2])):
    dd = min(dd, round(TOTAL - st, 3))
    j = next((q for q, e in enumerate(lanes) if e <= st), None)
    if j is None:
        lanes.append(0)
        j = len(lanes) - 1
    lanes[j] = st + dd + 0.01
    aud.append(f'      <audio id="{i}" src="{p}" data-start="{st}" data-duration="{dd}" data-volume="{v}" data-track-index="{10 + j}"></audio>')
open("index.html", "w").write(f"""<!doctype html>
<html lang="en" data-resolution="{'landscape' if WIDE else 'portrait'}">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="assets/vendor/gsap-3.14.2.min.js"></script>
    <style>* {{ margin: 0; padding: 0; box-sizing: border-box; }} html, body {{ margin: 0; width: {W}px; height: {H}px; overflow: hidden; background: {L['bg']}; }}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="{W}" data-height="{H}">
{chr(10).join(divs)}
{chr(10).join(aud)}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
""")
json.dump({"scenes": [{k: s[k] for k in ("id", "start", "end", "rec", "a", "b", "speed")} for s in SC], "clicks": CLICKS},
          open("timing.json", "w"), indent=1)
print(f"built {a.format}: {TOTAL} s, {len(SC)} scenes, speeds {[s['speed'] for s in SC]}, {len(CLICKS)} clicks")
