#!/usr/bin/env python3
"""Build a 16:9 panel tutorial (HyperFrames) from VO lines + recordings + screenshots.
usage: build_tut.py v1|v2 [--stub]   -> proj_vX/index.html, proj_vX/assets/..., proj_vX/timing.json
"""
import json, os, subprocess, sys, shutil, html
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shots import V1, V2

D = os.path.dirname(os.path.abspath(__file__))
V = sys.argv[1]
STUB = "--stub" in sys.argv
PLAN = V1 if V == "v1" else V2
P = f"{D}/proj_{V}"
os.makedirs(f"{P}/assets/vid", exist_ok=True)
for sub in ("fonts", "vendor", "img"):
    shutil.copytree(f"{D}/assets/{sub}", f"{P}/assets/{sub}", dirs_exist_ok=True)

W, H = 1920, 1080
FX, FY, FW = 140, 80, 1640           # monitor frame
LEAD = {"title": 0.8, "outro": 0.6, "card": 0.5, "rec": 0.6, "shot": 0.6}
GAP, TAIL = 0.45, 0.7
MIN = {"title": 5.5, "outro": 7.0}

lines = [l.strip() for l in open(f"{D}/vo/{V}_lines.txt", encoding="utf-8") if l.strip()]

def probe(p, key="duration", stream=None):
    args = ["ffprobe", "-v", "error"]
    if stream: args += ["-select_streams", stream, "-show_entries", f"stream={key}"]
    else: args += ["-show_entries", f"format={key}"]
    return subprocess.run(args + ["-of", "csv=p=0", p], capture_output=True, text=True).stdout.strip()

def vo_len(i):
    p = f"{D}/vo/parts_{V}/{i:03d}.wav"
    if STUB or not os.path.exists(p):
        return round(0.07 * len(lines[i - 1]) + 0.3, 2)
    return float(probe(p))

# ---------- timeline ----------
t = 0.0
LT = {}                 # line -> (start, end)
shots = []
for k, s in enumerate(PLAN["shots"]):
    kind = s["kind"]; t0 = t
    tt = t0 + LEAD[kind]
    for i in s["lines"]:
        d = vo_len(i); LT[i] = (round(tt, 3), round(tt + d, 3)); tt += d + GAP
    end = tt - GAP + TAIL
    if kind == "rec":
        src = f"{D}/in/{s['src']}"
        L = float(probe(src)); w, h = map(int, probe(src, "width,height", "v").split(","))
        need = end - t0
        speed = min(max(L / need, 0.85), 1.6)
        clip = L / speed
        if clip > need: end = t0 + clip
        s["_speed"], s["_L"], s["_wh"] = speed, L, (w, h)
    end = max(end, t0 + MIN.get(kind, 0))
    s["_t0"], s["_t1"] = round(t0, 3), round(end, 3)
    t = end
TOTAL = round(t, 3)

def ref(r):
    """line ref: 19 -> line start; 19.6 -> start + 0.6 * its length"""
    n = int(r); f = r - n
    a, b = LT[n]
    return round(a + f * (b - a), 3)

R = lambda v: f"{v:.3f}"

# ---------- recordings: speed-fit clips of exactly the shot length ----------
for k, s in enumerate(PLAN["shots"]):
    if s["kind"] != "rec": continue
    out = f"{P}/assets/vid/s{k}.mp4"
    dur = s["_t1"] - s["_t0"]
    w, h = s["_wh"]
    cut = h
    for ss in ("1", "4", "7", "10"):   # a GIF-derived page can get a white band at the bottom once the page gets shorter
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", ss, "-i", f"{D}/in/{s['src']}", "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True).stdout
        if len(raw) < h * w: continue
        rows = np.frombuffer(raw, np.uint8)[: h * w].reshape(h, w).mean(axis=1)
        white = np.where(rows > 240)[0]
        if len(white) > 10 and white.max() == h - 1: cut = min(cut, int(white.min() // 2 * 2))
    if cut < h: s["_crop"] = cut; h = cut
    fh = int(round(FW * h / w / 2)) * 2
    s["_fh"] = fh
    if not os.path.exists(out) or abs(float(probe(out)) - dur) > 0.1:
        crop = f"crop={w}:{s['_crop']}:0:0," if s.get("_crop") else ""
        vf = (f"{crop}setpts=PTS/{s['_speed']:.4f},scale={FW}:{fh}:flags=lanczos,tpad=stop_mode=clone:stop_duration={dur + 1:.3f},"
              f"trim=duration={dur:.3f},fps=30,format=yuv420p")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{D}/in/{s['src']}", "-vf", vf, "-an", "-c:v", "libx264", "-crf", "16",
                        "-preset", "medium", out], check=True)
    s["_clicks"] = [round(s["_t0"] + c / s["_speed"], 3) for c in s.get("clicks", []) if c < s["_L"]]

# ---------- HTML ----------
CSS = """
@font-face { font-family: "Anton"; src: url("assets/fonts/Anton-Regular.ttf"); }
@font-face { font-family: "Jakarta"; src: url("assets/fonts/PlusJakartaSans-Variable.ttf"); font-weight: 200 800; }
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { width: 1920px; height: 1080px; overflow: hidden; background: #070b12; }
#root { position: absolute; inset: 0; overflow: hidden; font-family: Jakarta, sans-serif; color: #e5e7eb; }
.bg { position: absolute; inset: 0; background: #070b12; }
.bg .grid { position: absolute; inset: 0; background-image: linear-gradient(rgba(34,197,94,0.05) 1px, transparent 1px),
  linear-gradient(90deg, rgba(34,197,94,0.05) 1px, transparent 1px); background-size: 80px 80px; }
.shot { position: absolute; inset: 0; }
.brand { position: absolute; left: 40px; top: 26px; display: flex; align-items: center; gap: 14px; font-weight: 700; font-size: 28px; color: #cbd5e1; }
.brand img { width: 44px; height: 44px; border-radius: 10px; }
.brand b { color: #22c55e; font-weight: 800; }
.step { position: absolute; right: 40px; top: 22px; display: flex; align-items: center; gap: 14px; padding: 8px 22px 8px 8px; border-radius: 999px;
  background: #0f172a; border: 1px solid rgba(255,255,255,0.1); font-weight: 700; font-size: 28px; color: #e5e7eb; }
.step i { display: inline-flex; width: 46px; height: 46px; border-radius: 50%; background: #22c55e; color: #04140a; font-style: normal; font-weight: 800;
  font-size: 28px; align-items: center; justify-content: center; }
.frame { position: absolute; left: 140px; top: 80px; width: 1640px; border-radius: 14px; overflow: hidden; background: #0b1220;
  border: 2px solid rgba(255,255,255,0.09); box-shadow: 0 24px 70px rgba(0,0,0,0.55); }
.frame video, .frame .kb img { display: block; width: 100%; height: 100%; }
.kb { position: absolute; inset: 0; }
.ring { position: absolute; border: 4px solid #22c55e; border-radius: 8px; box-shadow: 0 0 0 9999px rgba(0,0,0,0.38), 0 0 22px rgba(34,197,94,0.6); }
.cap { position: absolute; left: 50%; transform: translateX(-50%); top: 962px; max-width: 1360px; padding: 16px 34px 18px 30px; border-radius: 12px;
  background: rgba(7,11,18,0.93); border-left: 6px solid #22c55e; font-weight: 600; font-size: 36px; line-height: 1.25; color: #f1f5f9; white-space: nowrap; }
.chips { position: absolute; left: 140px; top: 884px; display: flex; align-items: center; gap: 10px; }
.chips span { padding: 10px 20px; border-radius: 10px; background: #111827; border: 1px solid rgba(255,255,255,0.12); font-weight: 700; font-size: 28px; color: #e5e7eb; white-space: nowrap; }
.chips .chev { width: 26px; height: 26px; color: #22c55e; }
.chips span.hi { background: #14532d; border-color: #22c55e; color: #fff; }
.warn { position: absolute; right: 180px; top: 120px; padding: 16px 28px; border-radius: 12px; background: #7f1d1d; border: 2px solid #ef4444;
  font-weight: 800; font-size: 34px; color: #fff; box-shadow: 0 12px 40px rgba(0,0,0,0.5); }
.code { position: absolute; right: 180px; top: 150px; min-width: 560px; padding: 22px 30px; border-radius: 14px; background: rgba(8,12,20,0.96);
  border: 1px solid rgba(255,255,255,0.12); font-family: "DejaVu Sans Mono", "Liberation Mono", monospace; font-size: 34px; line-height: 1.6; color: #cbd5e1;
  box-shadow: 0 20px 60px rgba(0,0,0,0.6); }
.code .k { color: #93c5fd; } .code .v { color: #22c55e; font-weight: 700; } .code .row { white-space: pre; }
.code.big { right: auto; left: 160px; top: 300px; font-size: 46px; min-width: 760px; padding: 28px 40px; }
.savebtn.big { right: auto; left: 160px; top: 640px; }
.code .hd { font-family: Jakarta; font-weight: 700; font-size: 30px; color: #9ca3af; margin-bottom: 8px; }
.cardwrap { position: absolute; left: 160px; top: 150px; width: 1600px; }
.cardwrap h2 { font-family: Anton; font-size: 92px; letter-spacing: 1px; color: #fff; line-height: 1; margin-bottom: 44px; }
.rows { display: flex; flex-direction: column; gap: 22px; }
.row2 { display: flex; align-items: center; gap: 28px; padding: 22px 30px; border-radius: 16px; background: #0f172a; border: 1px solid rgba(255,255,255,0.1); width: 1240px; }
.row2 i { flex: none; display: inline-flex; width: 64px; height: 64px; border-radius: 50%; background: #22c55e; color: #04140a; font-style: normal; font-weight: 800; font-size: 34px; align-items: center; justify-content: center; }
.row2 i.d { background: #ef4444; color: #fff; } .row2 i.e { background: #1f2937; color: #22c55e; }
.row2 .l { font-weight: 700; font-size: 44px; color: #f8fafc; } .row2 .s { font-weight: 500; font-size: 30px; color: #9ca3af; margin-top: 4px; }
.row2.danger { border-color: #ef4444; background: #1f0a0a; }
.row2.pulse { border-color: #22c55e; background: #0b2a18; }
.note { position: absolute; left: 160px; top: 760px; font-weight: 600; font-size: 36px; color: #22c55e; }
.bgimg { position: absolute; inset: 0; } .bgimg img { width: 100%; height: 100%; object-fit: cover; filter: brightness(0.2) blur(3px); transform: scale(1.03); }
.bgimg.sharp img { filter: brightness(0.22) blur(3px); }
.titlebg img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; filter: brightness(0.16) saturate(0.6) blur(2px); transform: scale(1.02); }
.h1 { position: absolute; left: 140px; top: 330px; font-family: Anton; font-size: 170px; line-height: 0.95; color: #fff; letter-spacing: 2px; }
.h2 { position: absolute; left: 146px; top: 540px; font-weight: 600; font-size: 64px; color: #22c55e; }
.tags { position: absolute; left: 146px; top: 660px; display: flex; gap: 16px; }
.tags span { padding: 12px 26px; border-radius: 999px; border: 2px solid rgba(255,255,255,0.28); font-weight: 600; font-size: 32px; color: #e5e7eb; }
.biglogo { position: absolute; left: 140px; top: 120px; width: 150px; height: 150px; border-radius: 30px; }
.outro .biglogo { left: 860px; top: 150px; width: 200px; height: 200px; border-radius: 40px; }
.outro .h1 { left: 0; right: 0; top: 400px; text-align: center; font-size: 150px; }
.outro .h2 { left: 0; right: 0; top: 570px; text-align: center; }
.outro .url { position: absolute; left: 0; right: 0; top: 680px; text-align: center; font-weight: 800; font-size: 70px; color: #fff; }
.outro .next { position: absolute; left: 50%; transform: translateX(-50%); top: 790px; padding: 18px 40px; border-radius: 999px; background: #22c55e; color: #04140a; font-weight: 800; font-size: 40px; white-space: nowrap; }
.outro .credit { position: absolute; right: 60px; bottom: 36px; text-align: right; font-weight: 600; font-size: 30px; color: #9ca3af; }
.savebtn { position: absolute; right: 180px; top: 560px; padding: 18px 34px; border-radius: 10px; background: #1f2937; border: 3px solid #22c55e; font-weight: 800; font-size: 32px; color: #fff; }
"""
from shots import CHEV, path

def esc(x): return html.escape(str(x), quote=False)

body, js, videos = [], [], []
for k, s in enumerate(PLAN["shots"]):
    kind, t0, t1 = s["kind"], s["_t0"], s["_t1"]; dur = t1 - t0
    sid = f"s{k}"
    inner = []
    if kind in ("title", "outro"):
        inner.append('<div class="titlebg"><img src="assets/img/panel-console.jpg" alt=""></div>')
        inner.append(f'<img class="biglogo" id="{sid}-logo" src="assets/img/logo.png" alt="SkilloraClouds">')
        inner.append(f'<div class="h1" id="{sid}-h1">{esc(s["h1"])}</div><div class="h2" id="{sid}-h2">{esc(s["h2"])}</div>')
        if kind == "title":
            inner.append(f'<div class="tags" id="{sid}-tags">' + "".join(f"<span>{esc(x)}</span>" for x in s["tags"]) + "</div>")
            js.append(f'tl.from("#{sid}-h1", {{ y: 60, opacity: 0, duration: 0.7, ease: "power3.out" }}, {R(t0 + 0.1)});')
            js.append(f'tl.from("#{sid}-h2", {{ y: 40, opacity: 0, duration: 0.6, ease: "power3.out" }}, {R(t0 + 0.45)});')
            js.append(f'tl.from("#{sid}-tags span", {{ y: 30, opacity: 0, duration: 0.5, stagger: 0.12, ease: "power3.out" }}, {R(t0 + 0.8)});')
        else:
            inner.append(f'<div class="url" id="{sid}-url">skilloraclouds.com</div><div class="next" id="{sid}-next">{esc(s["next"])}</div>')
            inner.append('<div class="credit">Edited by MrCopper804</div>')
            js.append(f'tl.from("#{sid}-logo", {{ scale: 0.6, opacity: 0, duration: 0.6, ease: "back.out(1.6)" }}, {R(t0 + 0.05)});')
            js.append(f'tl.from("#{sid}-h1, #{sid}-h2, #{sid}-url, #{sid}-next", {{ y: 40, opacity: 0, duration: 0.55, stagger: 0.14, ease: "power3.out" }}, {R(t0 + 0.3)});')
            js.append(f'tl.fromTo("#{sid}-next", {{ scale: 1 }}, {{ scale: 1.05, duration: 0.6, ease: "sine.inOut", yoyo: true, repeat: 4 }}, {R(t0 + 1.6)});')
    else:
        if s.get("bg"):
            inner.append(f'<div class="bgimg"><img src="assets/img/{s["bg"]}" alt=""></div>')
        inner.append('<div class="brand"><img src="assets/img/logo.png" alt="">Skillora<b>Clouds</b></div>')
        if s.get("step"):
            n, lbl = s["step"]
            inner.append(f'<div class="step" id="{sid}-step"><i>{n}</i>{esc(lbl)}</div>')
            js.append(f'tl.from("#{sid}-step", {{ x: 40, opacity: 0, duration: 0.45, ease: "power3.out" }}, {R(t0 + 0.1)});')
        if kind == "rec":
            fh = s["_fh"]
            videos.append(f'<video id="{sid}-v" class="clip frame" src="assets/vid/{sid}.mp4" muted playsinline data-start="{R(t0)}" data-duration="{R(dur)}" '
                          f'data-track-index="0" style="height:{fh}px"></video>')
            if s.get("warn"):
                ln, rc, txt = s["warn"]; at = t0 + rc / s["_speed"]
                inner.append(f'<div class="warn" id="{sid}-warn">{esc(txt)}</div>')
                js.append(f'tl.fromTo("#{sid}-warn", {{ scale: 0.7, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2)" }}, {R(at)});')
                js.append(f'tl.fromTo("#{sid}-warn", {{ x: -14 }}, {{ x: 0, duration: 0.08, repeat: 4, yoyo: true }}, {R(at + 0.35)});')
        if kind == "shot":
            iw, ih = map(int, probe(f"{P}/assets/img/{s['src']}", "width,height", "v").split(","))
            sx = FW / iw; fh = int(round(ih * sx))
            fx, fy, sc = s["kb"]
            rings = []
            for j, (r, x, y, w, h) in enumerate(s.get("rings", [])):
                rid = f"{sid}-r{j}"
                rings.append(f'<div class="ring" id="{rid}" style="left:{x*sx-6:.0f}px;top:{y*sx-5:.0f}px;width:{w*sx+12:.0f}px;height:{h*sx+10:.0f}px"></div>')
                js.append(f'tl.fromTo("#{rid}", {{ scale: 1.3, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2)" }}, {R(ref(r) + 0.15)});')
            inner.append(f'<div class="frame" style="height:{fh}px"><div class="kb" id="{sid}-kb" style="transform-origin:{fx*100:.0f}% {fy*100:.0f}%">'
                         f'<img src="assets/img/{s["src"]}" alt="">{"".join(rings)}</div></div>')
            js.append(f'tl.fromTo("#{sid}-kb", {{ scale: 1 }}, {{ scale: {sc}, duration: {R(max(dur - 0.6, 1))}, ease: "power1.inOut" }}, {R(t0 + 0.3)});')
        if kind == "card":
            inner.append(f'<div class="cardwrap"><h2 id="{sid}-h">{esc(s.get("title", ""))}</h2><div class="rows">')
            if s.get("pathline"):
                r, *parts = s["pathline"]
                inner.append(f'<div class="chips" id="{sid}-path" style="position:static;margin-bottom:30px">{path(*map(esc, parts))}</div>')
                js.append(f'tl.from("#{sid}-path > *", {{ y: 20, opacity: 0, duration: 0.4, stagger: 0.12, ease: "power3.out" }}, {R(ref(r))});')
            rev = s.get("reveal")
            for j, (badge, lbl, sub) in enumerate(s.get("items", [])):
                cls = "d" if badge == "!" else ("e" if badge == "" else "")
                b = badge if badge else "&#10003;"
                rid = f"{sid}-i{j}"
                inner.append(f'<div class="row2" id="{rid}"><i class="{cls}">{b}</i><div><div class="l">{esc(lbl)}</div>' + (f'<div class="s">{esc(sub)}</div>' if sub else "") + "</div></div>")
                at = ref(rev[j]) if rev else t0 + 0.35 + 0.18 * j
                js.append(f'tl.from("#{rid}", {{ x: -50, opacity: 0, duration: 0.5, ease: "power3.out" }}, {R(at)});')
            inner.append("</div></div>")
            if s.get("pulse"):
                r, j = s["pulse"]
                js.append(f'tl.to("#{sid}-i{j}", {{ className: "row2 pulse", duration: 0.3 }}, {R(ref(r))});')
                js.append(f'tl.fromTo("#{sid}-i{j}", {{ scale: 1 }}, {{ scale: 1.03, duration: 0.4, ease: "sine.inOut", yoyo: true, repeat: 3 }}, {R(ref(r))});')
            if s.get("danger") is not None:
                j = len(s["items"]) - 1
                js.append(f'tl.to("#{sid}-i{j}", {{ className: "row2 danger", duration: 0.3 }}, {R(ref(s["danger"]))});')
                js.append(f'tl.fromTo("#{sid}-i{j}", {{ x: -12 }}, {{ x: 0, duration: 0.08, repeat: 4, yoyo: true }}, {R(ref(s["danger"]) + 0.3)});')
            if s.get("note"):
                r, txt = s["note"]
                inner.append(f'<div class="note" id="{sid}-note">{esc(txt)}</div>')
                js.append(f'tl.from("#{sid}-note", {{ y: 20, opacity: 0, duration: 0.5, ease: "power3.out" }}, {R(ref(r))});')
            if s.get("save"):
                r, txt = s["save"]
                inner.append(f'<div class="savebtn big" id="{sid}-save">{esc(txt)}</div>')
                js.append(f'tl.fromTo("#{sid}-save", {{ scale: 0.8, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2)" }}, {R(ref(r))});')
        # chips (path rows under the frame), one row at a time
        for j, c in enumerate(s.get("chips", [])):
            r, *parts = c
            cid = f"{sid}-c{j}"
            inner.append(f'<div class="chips" id="{cid}">{path(*map(esc, parts))}</div>')
            at = ref(r) + 0.1
            js.append(f'tl.from("#{cid} > *", {{ y: 24, opacity: 0, duration: 0.4, stagger: 0.08, ease: "power3.out" }}, {R(at)});')
            if j + 1 < len(s["chips"]):
                nxt = ref(s["chips"][j + 1][0])
                js.append(f'tl.to("#{cid}", {{ opacity: 0, y: -16, duration: 0.3 }}, {R(nxt - 0.25)});')
        # code card rows
        if s.get("code"):
            rows = []
            for j, (r, key, val) in enumerate(s["code"]):
                rows.append(f'<div class="row" id="{sid}-k{j}"><span class="k">{esc(key)}</span> <span class="v">{esc(val)}</span></div>')
                js.append(f'tl.from("#{sid}-k{j}", {{ x: 30, opacity: 0, duration: 0.4, ease: "power3.out" }}, {R(ref(r) + 0.2 + 0.12 * j)});')
            hd = "config.yml" if V == "v1" else "voicechat-server.properties"
            inner.append(f'<div class="code{" big" if kind == "card" else ""}" id="{sid}-code"><div class="hd">{hd}</div>{"".join(rows)}</div>')
            js.append(f'tl.from("#{sid}-code", {{ y: 30, opacity: 0, duration: 0.45, ease: "power3.out" }}, {R(ref(s["code"][0][0]) + 0.05)});')
    inner.append(f'<div class="cap" id="{sid}-cap">{esc(s["cap"])}</div>')
    js.append(f'tl.from("#{sid}-cap", {{ y: 24, opacity: 0, duration: 0.4, ease: "power3.out" }}, {R(t0 + 0.25)});')
    cls = "shot " + kind + (" outro" if kind == "outro" else "")
    body.append(f'<div id="{sid}" class="clip {cls}" data-hold data-start="{R(t0)}" data-duration="{R(dur)}" data-track-index="1" data-track-kind="graphics">{"".join(inner)}</div>')
    if k > 0:   # the first frame is the thumbnail: no fade at 0 s
        js.append(f'tl.from("#{sid}", {{ opacity: 0, duration: 0.35, ease: "power1.out" }}, {R(t0)});')

page = f"""<!doctype html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=1920, height=1080">
<script src="assets/vendor/gsap-3.14.2.min.js"></script>
<style>{CSS}</style></head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{R(TOTAL)}" data-width="1920" data-height="1080">
<div class="bg"><div class="grid"></div></div>
{chr(10).join(videos)}
{chr(10).join(body)}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
window.__timelines["main"] = tl;
</script>
</body></html>"""
open(f"{P}/index.html", "w", encoding="utf-8").write(page)

timing = dict(total=TOTAL, lines={str(i): LT[i] for i in sorted(LT)}, stub=STUB, music=PLAN["music"], music_start=PLAN["music_start"],
              shots=[dict(k=k, kind=s["kind"], t0=s["_t0"], t1=s["_t1"], lines=s["lines"], speed=s.get("_speed"), clicks=s.get("_clicks", [])) for k, s in enumerate(PLAN["shots"])],
              chimes=[ref(r) + 0.15 for s in PLAN["shots"] if s["kind"] == "shot" and "Console" in (s.get("step") or ("", ""))[1] for (r, *_) in s["rings"][:1]])
json.dump(timing, open(f"{P}/timing.json", "w"), indent=1)
print(f"{V}: total {TOTAL:.1f}s, {len(PLAN['shots'])} shots, stub={STUB}")
for s in timing["shots"]:
    print(f"  s{s['k']:<2} {s['kind']:<5} {s['t0']:7.2f}-{s['t1']:7.2f} lines {s['lines']} speed {s['speed'] and round(s['speed'],2)} clicks {s['clicks']}")
