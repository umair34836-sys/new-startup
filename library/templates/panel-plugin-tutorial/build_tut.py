#!/usr/bin/env python3
"""Build a 16:9 panel tutorial (HyperFrames) from VO lines + recordings + screenshots, synced to the words.
usage: build_tut.py v1|v2 [--stub]   -> proj_vX/index.html, proj_vX/assets/vid/*.mp4, proj_vX/timing.json
"""
import json, os, re, subprocess, sys, shutil, html, difflib
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shots import V1, V2, CHEV, path

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
WORDS = json.load(open(f"{D}/vo/words_{V}.json")) if os.path.exists(f"{D}/vo/words_{V}.json") else {}

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

# ---------- timeline: lines first ----------
t = 0.0
LT = {}
for s in PLAN["shots"]:
    kind = s["kind"]; t0 = t; tt = t0 + LEAD[kind]
    for i in s["lines"]:
        d = vo_len(i); LT[i] = (round(tt, 3), round(tt + d, 3)); tt += d + GAP
    end = max(tt - GAP + TAIL, t0 + MIN.get(kind, 0))
    s["_t0"], s["_t1"] = round(t0, 3), round(end, 3)
    t = end
TOTAL = round(t, 3)

norm = lambda w: re.sub(r"[^\w]", "", w).replace("़", "").replace("ॉ", "ो")
def word_time(line, word):
    """absolute time when `word` is spoken in `line`: Whisper word match, else proportional to its text position"""
    a, b = LT[line]; text = lines[line - 1]
    ws = WORDS.get(str(line), [])
    target = norm(word)
    pos = text.find(word)
    frac = (pos / len(text)) if pos >= 0 else 0.0
    est = frac * (b - a) * 0.95                       # proportional estimate (relative)
    best, score = None, 0.0
    for w, st, en in ws:                                # best Whisper word: similar text AND near the estimate
        r = difflib.SequenceMatcher(None, norm(w), target).ratio() - 0.25 * abs(st - est) / max(b - a, 1)
        if r > score: best, score = st, r
    if best is not None and score >= 0.55:
        return round(a + best, 3)
    return round(a + est, 3)

def ref(r):
    if isinstance(r, str):
        n, w = r.split(":", 1); return word_time(int(n), w)
    n = int(r); f = r - n; a, b = LT[n]
    return round(a + f * (b - a), 3)

R = lambda v: f"{v:.3f}"

# ---------- recordings: clips of exactly their window, held / speed-fit / frozen ----------
def rec_info(src):
    p = f"{D}/in/{src}"
    L = float(probe(p)); w, h = map(int, probe(p, "width,height", "v").split(","))
    cut = h
    for ss in ("1", "4", "7", "10"):   # a GIF-derived page can get a white band at the bottom once the page gets shorter
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", ss, "-i", p, "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True).stdout
        if len(raw) < h * w: continue
        rows = np.frombuffer(raw, np.uint8)[: h * w].reshape(h, w).mean(axis=1)
        white = np.where(rows > 240)[0]
        if len(white) > 10 and white.max() == h - 1: cut = min(cut, int(white.min() // 2 * 2))
    return dict(L=L, w=w, h=h, crop=cut if cut < h else None, cw=min(w, 1900))

for k, s in enumerate(PLAN["shots"]):
    if s["kind"] != "rec": continue
    t0, t1 = s["_t0"], s["_t1"]
    clips = s["clips"]
    starts = [t0] + [ref(c["until"]) for c in clips[:-1]]
    ends = starts[1:] + [t1]
    for j, c in enumerate(clips):
        info = rec_info(c["src"]); a, b = c.get("range", (0, info["L"])); b = min(b, info["L"]); L = b - a
        cs, ce = starts[j], ends[j]; win = ce - cs
        if c.get("play_at"):
            pa = c["play_at"]; word, off = (pa if isinstance(pa, tuple) else (pa, 0.6))   # (word, action time within the range)
            hold = max(0.0, ref(word) - off - cs)                 # the click/action lands when the word is said
            speed = max(1.0, min(1.6, L / max(win - hold, 0.1)))
            if hold + L / speed > win:                           # still too long: extend the shot (last clip only)
                if j == len(clips) - 1:
                    ce = cs + hold + L / speed; s["_t1"] = round(ce, 3); win = ce - cs
                else:
                    speed = 1.6
        else:
            hold = 0.0; speed = min(max(L / win, 0.85), 1.6)
            if L / speed > win and j == len(clips) - 1:
                ce = cs + L / speed; s["_t1"] = round(ce, 3); win = ce - cs
        c.update(_cs=round(cs, 3), _ce=round(ce, 3), _hold=round(hold, 3), _speed=round(speed, 4), _a=a, _info=info)
        h = info["crop"] or info["h"]; fh = int(round(FW * h / info["cw"] / 2)) * 2; c["_fh"] = fh; c["_sx"] = FW / info["cw"]
        out = f"{P}/assets/vid/s{k}c{j}.mp4"
        sig = f"{c['src']}|{a}|{b}|{hold:.3f}|{speed:.4f}|{win:.3f}|{info['crop']}|{info['cw']}"
        if not (os.path.exists(out) and os.path.exists(out + ".sig") and open(out + ".sig").read() == sig):
            crop = f"crop={info['cw']}:{info['crop'] or info['h']}:0:0,"
            vf = (f"trim={a}:{b},setpts=(PTS-STARTPTS)/{speed:.4f},{crop}scale={FW}:{fh}:flags=lanczos,"
                  f"tpad=start_mode=clone:start_duration={hold:.3f}:stop_mode=clone:stop_duration={win + 1:.3f},trim=duration={win:.3f},fps=30,format=yuv420p")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{D}/in/{c['src']}", "-vf", vf, "-an", "-c:v", "libx264", "-crf", "16", "-preset", "medium", out], check=True)
            open(out + ".sig", "w").write(sig)
        c["_clicks"] = [round(cs + hold + (rc - a) / speed, 3) for rc in c.get("clicks", []) if a <= rc < b and cs + hold + (rc - a) / speed < ce]
    # shots after this one shift if the shot grew
for k in range(1, len(PLAN["shots"])):
    prev, s = PLAN["shots"][k - 1], PLAN["shots"][k]
    if s["_t0"] < prev["_t1"]:
        shift = round(prev["_t1"] - s["_t0"], 3)
        s["_t0"] = round(s["_t0"] + shift, 3); s["_t1"] = round(s["_t1"] + shift, 3)
        for i in s["lines"]: LT[i] = (round(LT[i][0] + shift, 3), round(LT[i][1] + shift, 3))
        for c in s.get("clips", []):
            for key in ("_cs", "_ce"): c[key] = round(c[key] + shift, 3)
            c["_clicks"] = [round(x + shift, 3) for x in c["_clicks"]]
TOTAL = round(PLAN["shots"][-1]["_t1"], 3)

# ---------- HTML ----------
CSS = open(f"{D}/tut.css").read()

def esc(x): return html.escape(str(x), quote=False)

def callout(cid, label, x, y, colour):
    """label box + arrow pointing at (x, y) frame px"""
    col = "#ef4444" if colour == "r" else "#22c55e"
    above = y > 300
    lw = min(max(26 * len(label) * 0.62 + 44, 160), 980)
    lx = min(max(x - lw / 2, 150), W - 150 - lw)
    ly = (y - 150) if above else (y + 70)
    ax, ay = lx + lw / 2, (ly + 62) if above else ly
    svg = (f'<svg class="arr" viewBox="0 0 {W} {H}"><defs><marker id="{cid}-m" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">'
           f'<path d="M0,0 L8,4 L0,8 z" fill="{col}"/></marker></defs>'
           f'<line x1="{ax:.0f}" y1="{ay:.0f}" x2="{x:.0f}" y2="{y:.0f}" stroke="{col}" stroke-width="5" stroke-linecap="round" marker-end="url(#{cid}-m)"/></svg>')
    dot = f'<div class="dot" style="left:{x - 14:.0f}px;top:{y - 14:.0f}px;border-color:{col}"></div>'
    lab = f'<div class="lab" style="left:{lx:.0f}px;top:{ly:.0f}px;width:{lw:.0f}px;border-color:{col}">{esc(label)}</div>'
    return f'<div class="callout" id="{cid}" data-layout-allow-overlap>{svg}{dot}{lab}</div>'

DIAGRAMS = {
 "ports": '<div class="dg"><div class="box">Java players<small>PC</small></div><div class="port"><span>:20004</span></div><div class="srv">Your server</div><div class="port"><span>:20025</span></div><div class="box">Bedrock players<small>phone, console</small></div></div>',
 "floodgate": '<div class="dg"><div class="box">Bedrock player<small>no Java account</small></div><div class="port"><span>Geyser + Floodgate</span></div><div class="srv">Java server</div></div>',
 "voice": '<div class="dg"><div class="box">Server<small>Simple Voice Chat plugin</small></div><div class="port"><span>UDP port</span></div><div class="box">Every player&#39;s PC<small>Simple Voice Chat mod</small></div></div>',
 "proximity": '<div class="dg"><div class="box">You<small>talking</small></div><div class="port"><span>near = loud</span></div><div class="box">Friend<small>5 blocks</small></div><div class="port fade"><span>far = quiet</span></div><div class="box dim">Friend<small>40 blocks</small></div></div>',
}

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
            js.append(f'tl.from("#{sid}-h1", {{ y: 40, duration: 0.7, ease: "power3.out" }}, {R(t0)});')
            js.append(f'tl.from("#{sid}-h2", {{ y: 30, duration: 0.6, ease: "power3.out" }}, {R(t0 + 0.1)});')
            js.append(f'tl.from("#{sid}-tags span", {{ y: 20, duration: 0.5, stagger: 0.1, ease: "power3.out" }}, {R(t0 + 0.2)});')
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
        calls_px = []     # (ref time, label, fx, fy, colour)
        if kind == "rec":
            for j, c in enumerate(s["clips"]):
                videos.append(f'<video id="{sid}-v{j}" class="clip frame" src="assets/vid/{sid}c{j}.mp4" muted playsinline data-start="{R(c["_cs"])}" '
                              f'data-duration="{R(c["_ce"] - c["_cs"])}" data-track-index="0" style="height:{c["_fh"]}px"></video>')
            for cl in s.get("calls", []):
                r, label, (x, y) = cl[0], cl[1], cl[2]; j = cl[3] if len(cl) > 3 else 0; colour = cl[4] if len(cl) > 4 else "g"
                sx = s["clips"][j]["_sx"]
                calls_px.append((ref(r), label, FX + x * sx, FY + y * sx, colour, s["clips"][j]["_ce"]))
        if kind == "shot":
            iw, ih = map(int, probe(f"{P}/assets/img/{s['src']}", "width,height", "v").split(","))
            sx = FW / iw; fh = int(round(ih * sx)); fx, fy, sc = s["kb"]
            inner.append(f'<div class="frame" style="height:{fh}px"><div class="kb" id="{sid}-kb" style="transform-origin:{fx*100:.0f}% {fy*100:.0f}%">'
                         f'<img src="assets/img/{s["src"]}" alt=""></div></div>')
            js.append(f'tl.fromTo("#{sid}-kb", {{ scale: 1 }}, {{ scale: {sc}, duration: {R(max(dur - 0.6, 1))}, ease: "power1.inOut" }}, {R(t0 + 0.3)});')
            for cl in s.get("calls", []):
                r, label, (x, y) = cl[0], cl[1], cl[2]; colour = cl[4] if len(cl) > 4 else "g"
                # the Ken Burns zoom moves the target: follow it (origin fx,fy of the frame, scale sc at the end)
                tt = ref(r); prog = min(max((tt - (t0 + 0.3)) / max(dur - 0.6, 1), 0), 1); scl = 1 + (sc - 1) * prog
                ox, oy = FX + fx * FW, FY + fy * fh
                px = ox + (FX + x * sx - ox) * scl; py = oy + (FY + y * sx - oy) * scl
                calls_px.append((tt, label, px, py, colour, t1))
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
            if s.get("diagram"):
                name, r = s["diagram"]
                inner.append(f'<div class="dgwrap" id="{sid}-dg">{DIAGRAMS[name]}</div>')
                js.append(f'tl.from("#{sid}-dg .dg > *", {{ y: 24, opacity: 0, duration: 0.45, stagger: 0.12, ease: "power3.out" }}, {R(ref(r))});')
            if s.get("pulse"):
                r, j = s["pulse"]
                js.append(f'tl.to("#{sid}-i{j}", {{ className: "row2 pulse", duration: 0.3 }}, {R(ref(r))});')
                js.append(f'tl.fromTo("#{sid}-i{j}", {{ scale: 1 }}, {{ scale: 1.03, duration: 0.4, ease: "sine.inOut", yoyo: true, repeat: 3 }}, {R(ref(r))});')
            if s.get("danger") is not None:
                j = len(s["items"]) - 1
                js.append(f'tl.to("#{sid}-i{j}", {{ className: "row2 danger", duration: 0.3 }}, {R(ref(s["danger"]))});')
                js.append(f'tl.fromTo("#{sid}-i{j}", {{ x: -12 }}, {{ x: 0, duration: 0.08, repeat: 4, yoyo: true }}, {R(ref(s["danger"]) + 0.3)});')
            if s.get("save"):
                r, txt = s["save"]
                inner.append(f'<div class="savebtn big" id="{sid}-save">{esc(txt)}</div>')
                js.append(f'tl.fromTo("#{sid}-save", {{ scale: 0.8, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2)" }}, {R(ref(r))});')
        # callouts: each shows at its word and leaves when the next one comes (or its clip / the shot ends)
        calls_px.sort(key=lambda c: c[0])
        for j, (tt, label, px, py, colour, cend) in enumerate(calls_px):
            cid = f"{sid}-a{j}"
            inner.append(callout(cid, label, px, py, colour))
            nxt = calls_px[j + 1][0] if j + 1 < len(calls_px) else cend
            hide = min(nxt - 0.15, cend - 0.1)
            js.append(f'tl.set("#{cid}", {{ autoAlpha: 0 }}, {R(t0)});')
            js.append(f'tl.to("#{cid}", {{ autoAlpha: 1, duration: 0.05 }}, {R(tt)});')
            js.append(f'tl.from("#{cid} .lab", {{ scale: 0.8, opacity: 0, duration: 0.3, ease: "back.out(2)" }}, {R(tt)});')
            js.append(f'tl.from("#{cid} .arr line", {{ opacity: 0, duration: 0.2 }}, {R(tt + 0.1)});')
            js.append(f'tl.from("#{cid} .dot", {{ scale: 1.8, opacity: 0, duration: 0.35, ease: "power2.out" }}, {R(tt + 0.15)});')
            js.append(f'tl.to("#{cid} .dot", {{ scale: 1.25, duration: 0.45, ease: "sine.inOut", yoyo: true, repeat: 3 }}, {R(tt + 0.55)});')
            if hide > tt + 0.5:
                js.append(f'tl.to("#{cid}", {{ autoAlpha: 0, duration: 0.25 }}, {R(hide)});')
            s.setdefault("_calltimes", []).append((round(tt, 2), label))
        # code card rows
        if s.get("code"):
            rows = []
            for j, (r, key, val) in enumerate(s["code"]):
                rows.append(f'<div class="row" id="{sid}-k{j}"><span class="k">{esc(key)}</span> <span class="v">{esc(val)}</span></div>')
                js.append(f'tl.from("#{sid}-k{j}", {{ x: 30, opacity: 0, duration: 0.4, ease: "power3.out" }}, {R(ref(r) + 0.05 * j)});')
            hd = "config.yml" if V == "v1" else "voicechat-server.properties"
            inner.append(f'<div class="code{" big" if kind == "card" else ""}" id="{sid}-code"><div class="hd">{hd}</div>{"".join(rows)}</div>')
            js.append(f'tl.from("#{sid}-code", {{ y: 30, opacity: 0, duration: 0.45, ease: "power3.out" }}, {R(ref(s["code"][0][0]) - 0.1)});')
    # per-line captions
    for j, i in enumerate(s["lines"]):
        cap = PLAN["caps"].get(i) or s.get("cap", "")
        a = LT[i][0]; b = LT[s["lines"][j + 1]][0] if j + 1 < len(s["lines"]) else t1
        inner.append(f'<div class="cap" id="{sid}-cap{j}">{esc(cap)}</div>')
        show = max(t0, a - 0.35)
        js.append(f'tl.set("#{sid}-cap{j}", {{ autoAlpha: 0 }}, {R(t0)});')
        js.append(f'tl.fromTo("#{sid}-cap{j}", {{ autoAlpha: 0, y: 16 }}, {{ autoAlpha: 1, y: 0, duration: 0.3, ease: "power3.out" }}, {R(show)});')
        if j + 1 < len(s["lines"]):
            js.append(f'tl.to("#{sid}-cap{j}", {{ autoAlpha: 0, duration: 0.2 }}, {R(b - 0.4)});')
    cls = "clip shot " + kind + (" outro" if kind == "outro" else "")
    body.append(f'<div id="{sid}" class="{cls}" data-hold data-start="{R(t0)}" data-duration="{R(dur)}" data-track-index="1" data-track-kind="graphics">{"".join(inner)}</div>')
    if k > 0 and kind != "outro":
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

clicks = [c for s in PLAN["shots"] for cl in s.get("clips", []) for c in cl["_clicks"]]
chimes = [ref(s["calls"][-1][0]) + 0.1 for s in PLAN["shots"] if s["kind"] == "shot" and "Console" in (s.get("step") or ("", ""))[1]]
timing = dict(total=TOTAL, lines={str(i): LT[i] for i in sorted(LT)}, stub=STUB, music=PLAN["music"], music_start=PLAN["music_start"], music_cut=PLAN.get("music_cut"),
              shots=[dict(k=k, kind=s["kind"], t0=s["_t0"], t1=s["_t1"], lines=s["lines"],
                          clips=[dict(src=c["src"], cs=c["_cs"], ce=c["_ce"], hold=c["_hold"], speed=c["_speed"]) for c in s.get("clips", [])],
                          clicks=[c for cl in s.get("clips", []) for c in cl["_clicks"]], calls=s.get("_calltimes", [])) for k, s in enumerate(PLAN["shots"])],
              chimes=chimes, words_used=bool(WORDS))
json.dump(timing, open(f"{P}/timing.json", "w"), indent=1)
print(f"{V}: total {TOTAL:.1f}s, {len(PLAN['shots'])} shots, stub={STUB}, words={bool(WORDS)}, clicks={len(clicks)}")
for s in timing["shots"]:
    print(f"  s{s['k']:<2} {s['kind']:<5} {s['t0']:7.2f}-{s['t1']:7.2f} lines {s['lines']} " + " ".join(f"[{c['src'][:4]} hold {c['hold']} x{c['speed']}]" for c in s["clips"]))
