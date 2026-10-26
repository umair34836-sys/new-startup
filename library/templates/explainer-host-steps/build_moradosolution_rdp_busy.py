# MoradoSolution "Indian RDP + BUSY" setup explainer, 1920x1080. Script = the owner's own words (2026-10-26),
# price + specs from the owner: 16 GB RAM, 8 vCore, 150 GB NVMe, ₹3,000/month. No fake Windows/BUSY screens (owner chose "bina screen ke"):
# step cards with generic drawn icons, the owner's blocky host (library/characters/host-skin.png), Roman captions.
# Scene/caption times follow the VO line starts in assets/vo/lines.json (vs_tts.py --parts), shifted by VO_START.
import json, os, subprocess, html as H

VO_START = 0.6
RED, BLUE, DARK, CARD = "#e11d48", "#3b82f6", "#050505", "rgba(18,18,21,0.94)"
L = json.load(open("assets/vo/lines.json"))
CAP = [l.strip() for l in open("captions.txt", encoding="utf-8") if l.strip()]
assert len(CAP) == len(L), (len(CAP), len(L))
VO_FILE = "assets/vo/vo.wav"
T0 = [round(VO_START + a, 2) for a, _ in L]       # line start in the film
T1 = [round(VO_START + b, 2) for _, b in L]       # line end
TOTAL = round(T1[-1] + 2.5, 2)

# sections: (id, first line index)
SEC = [("title", 0), ("aud", 1), ("easy", 4), ("offer", 5), ("price", 7), ("rdp", 8), ("busy", 12), ("imp", 16),
       ("outro", 19), ("end", 21)]
S0 = {k: (0.0 if i == 0 else round(T0[i] - 0.2, 2)) for k, i in SEC}
order = [k for k, _ in SEC]
S1 = {k: (S0[order[j + 1]] if j + 1 < len(order) else TOTAL) for j, k in enumerate(order)}


def at(line, frac=0.0, sec=None):
    """time inside a section at a fraction of a VO line"""
    t = T0[line] + frac * (T1[line] - T0[line])
    return round(max(0.05, t - S0[sec]), 2)


def dur(p):
    return round(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                      capture_output=True, text=True).stdout), 3)


CSS = f"""
    @font-face {{ font-family: "Anton"; src: url("assets/fonts/Anton-Regular.ttf"); }}
    @font-face {{ font-family: "Grotesk"; src: url("assets/fonts/SpaceGrotesk-Variable.ttf"); font-weight: 300 700; }}
    #root {{ position: absolute; inset: 0; overflow: hidden; }}
    .gr {{ font-family: Grotesk; }}
    .anton {{ font-family: Anton; letter-spacing: 2px; line-height: 1.0; }}
    .panel {{ position: absolute; left: 760px; top: 120px; width: 1060px; height: 720px; }}
    .card {{ border-radius: 24px; background: {CARD}; border: 2px solid rgba(255,255,255,0.14); box-shadow: 0 16px 50px rgba(0,0,0,0.55); }}
    .row {{ position: absolute; left: 0; width: 1060px; height: 130px; display: flex; align-items: center; gap: 30px; padding: 0 34px; }}
    .num {{ width: 74px; height: 74px; border-radius: 50%; background: {RED}; color: #fff; font-family: Anton; font-size: 42px;
            display: flex; align-items: center; justify-content: center; flex: none; }}
    .ic {{ width: 74px; height: 74px; flex: none; }}
    .t1 {{ font-family: Grotesk; font-weight: 700; font-size: 44px; color: #fff; line-height: 1.15; }}
    .t2 {{ font-family: Grotesk; font-weight: 500; font-size: 32px; color: #d4d4d8; margin-top: 4px; }}
    .k {{ color: {RED}; }}
    .b {{ color: #93c5fd; }}
"""

# generic line icons (drawn here, no brand marks)
IC = {
    "monitor": '<rect x="6" y="10" width="62" height="40" rx="5" fill="none" stroke="#fff" stroke-width="5"/><path d="M28 64h18M37 50v14" stroke="#fff" stroke-width="5" stroke-linecap="round"/>',
    "plug": '<path d="M14 37h46M44 22l16 15-16 15" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>',
    "key": '<circle cx="24" cy="37" r="13" fill="none" stroke="#fff" stroke-width="5"/><path d="M37 37h30M56 37v12M66 37v9" stroke="#fff" stroke-width="5" stroke-linecap="round"/>',
    "check": '<circle cx="37" cy="37" r="31" fill="#16a34a"/><path d="M22 38l10 10 20-22" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>',
    "app": '<rect x="10" y="10" width="54" height="54" rx="12" fill="none" stroke="#fff" stroke-width="5"/><path d="M24 30h26M24 44h18" stroke="#fff" stroke-width="5" stroke-linecap="round"/>',
    "lock": '<rect x="14" y="32" width="46" height="34" rx="6" fill="none" stroke="#fff" stroke-width="5"/><path d="M24 32v-8a13 13 0 0 1 26 0v8" fill="none" stroke="#fff" stroke-width="5"/>',
    "backup": '<path d="M20 52a14 14 0 0 1 2-28 18 18 0 0 1 34 4 12 12 0 0 1 0 24" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round"/><path d="M37 40v26M28 57l9 9 9-9" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>',
    "help": '<path d="M14 42v-6a23 23 0 0 1 46 0v6" fill="none" stroke="#fff" stroke-width="5"/><rect x="8" y="40" width="14" height="22" rx="5" fill="#fff"/><rect x="52" y="40" width="14" height="22" rx="5" fill="#fff"/>',
    "nobox": '<rect x="12" y="20" width="50" height="40" rx="5" fill="none" stroke="#fff" stroke-width="5"/><path d="M10 10l54 54" stroke="#e11d48" stroke-width="7" stroke-linecap="round"/>',
}


def icon(name):
    return f'<svg class="ic" viewBox="0 0 74 74">{IC[name]}</svg>'


def row(rid, y, lead, t1, t2="", border=RED):
    t2h = f'<div class="t2">{t2}</div>' if t2 else ""
    return (f'<div class="row card" id="{rid}" style="top:{y}px;border-left:10px solid {border};opacity:0;">{lead}'
            f'<div><div class="t1">{t1}</div>{t2h}</div></div>')


def pop(sel, t):
    return f'    tl.fromTo("{sel}", {{ x: 120, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.4, ease: "power3.out" }}, {t});\n'


def comp(cid, body, js):
    d = round(S1[cid] - S0[cid], 2)
    return f"""<template>
  <style>{CSS}</style>
  <div id="root" data-composition-id="{cid}" data-width="1920" data-height="1080">
    <div id="{cid}-w" style="position:absolute;inset:0;">
{body}
    </div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    tl.fromTo("#{cid}-w", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }}, 0);
{js}    tl.to("#{cid}-w", {{ opacity: 0, y: -30, duration: 0.25, ease: "power2.in" }}, {d - 0.25:.2f});
    window.__timelines["{cid}"] = tl;
  </script>
</template>
"""


C, POPS = {}, []   # POPS: absolute times of row pops (for SFX)


def mark(sec, t, kind="pop"):
    POPS.append((round(S0[sec] + t, 2), kind))


# title (on screen at 0 s = thumbnail)
C["title"] = f"""<template>
  <style>{CSS}</style>
  <div id="root" data-composition-id="title" data-width="1920" data-height="1080">
    <div id="title-w" style="position:absolute;inset:0;">
      <div class="panel">
        <div class="gr" style="position:absolute;top:70px;font-weight:700;font-size:40px;letter-spacing:10px;color:#d4d4d8;">SETUP GUIDE</div>
        <div class="anton" style="position:absolute;top:140px;font-size:150px;color:#fff;">INDIAN RDP</div>
        <div class="anton" style="position:absolute;top:300px;font-size:150px;" ><span class="k">+</span> <span style="color:#fff;">BUSY</span></div>
        <div class="gr" style="position:absolute;top:500px;font-weight:600;font-size:44px;color:#d4d4d8;">Pre-installed &amp; pre-configured</div>
      </div>
    </div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    tl.to("#title-w", {{ opacity: 0, y: -30, duration: 0.25, ease: "power2.in" }}, {S1["title"] - S0["title"] - 0.25:.2f});
    window.__timelines["title"] = tl;
  </script>
</template>
"""

# audience (lines 1-3)
b = (row("aud-r0", 40, icon("app"), "Battery business?") + row("aud-r1", 200, icon("monitor"), "Billing · Accounting · Stock", "BUSY software use karte ho?", BLUE)
     + '<div class="anton" id="aud-r2" style="position:absolute;top:420px;left:0;font-size:96px;color:#fff;opacity:0;">YE VIDEO <span class="k">AAPKE LIYE</span></div>')
C["aud"] = comp("aud", f'<div class="panel">{b}</div>', pop("#aud-r0", at(1, 0.1, "aud")) + pop("#aud-r1", at(2, 0.15, "aud"))
                + pop("#aud-r2", at(3, 0.1, "aud")))
mark("aud", at(1, 0.1, "aud")); mark("aud", at(2, 0.15, "aud")); mark("aud", at(3, 0.1, "aud"))

# easy (line 4)
b = (row("easy-r0", 60, icon("nobox"), "BUSY install? <span class='k'>Zarurat nahi</span>") + row("easy-r1", 220, icon("nobox"), "Baar-baar setup? <span class='k'>Tension nahi</span>"))
C["easy"] = comp("easy", f'<div class="panel">{b}</div>', pop("#easy-r0", at(4, 0.15, "easy")) + pop("#easy-r1", at(4, 0.55, "easy")))
mark("easy", at(4, 0.15, "easy")); mark("easy", at(4, 0.55, "easy"))

# offer (lines 5-6)
b = ('<div class="anton" id="off-a" style="position:absolute;top:30px;left:0;font-size:120px;color:#fff;opacity:0;">INDIAN RDP</div>'
     + row("off-r0", 210, icon("check"), "BUSY pre-installed", "", "#16a34a") + row("off-r1", 370, icon("check"), "BUSY pre-configured", "", "#16a34a")
     + row("off-r2", 530, icon("check"), "Pehle se setup karke", "aapko diya jayega", "#16a34a"))
C["offer"] = comp("offer", f'<div class="panel">{b}</div>', pop("#off-a", at(5, 0.05, "offer")) + pop("#off-r0", at(5, 0.5, "offer"))
                  + pop("#off-r1", at(5, 0.75, "offer")) + pop("#off-r2", at(6, 0.2, "offer")))
for t in (at(5, 0.5, "offer"), at(5, 0.75, "offer"), at(6, 0.2, "offer")):
    mark("offer", t, "ok")

# price (line 7): owner's price + specs (owner 2026-10-26: 16 GB RAM, 8 vCore, 150 GB NVMe, ₹3,000/month)
SPECS = [("ram", "16 GB", "RAM"), ("cpu", "8", "vCore"), ("disk", "150 GB", "NVMe")]
SIC = {"ram": '<rect x="6" y="20" width="62" height="34" rx="4" fill="none" stroke="#fff" stroke-width="5"/><path d="M18 54v8M30 54v8M44 54v8M56 54v8M18 30v14M30 30v14M44 30v14M56 30v14" stroke="#fff" stroke-width="4"/>',
       "cpu": '<rect x="18" y="18" width="38" height="38" rx="4" fill="none" stroke="#fff" stroke-width="5"/><rect x="29" y="29" width="16" height="16" fill="#fff"/><path d="M28 8v10M46 8v10M28 56v10M46 56v10M8 28h10M8 46h10M56 28h10M56 46h10" stroke="#fff" stroke-width="4"/>',
       "disk": '<rect x="8" y="22" width="58" height="30" rx="6" fill="none" stroke="#fff" stroke-width="5"/><circle cx="54" cy="37" r="4" fill="#fff"/><path d="M18 37h22" stroke="#fff" stroke-width="5" stroke-linecap="round"/>'}
chips = "".join(
    f'<div class="sp" id="pr-s{i}" style="position:absolute;left:{40 + i * 280}px;top:150px;width:260px;height:150px;border-radius:20px;'
    f'background:rgba(255,255,255,0.07);border:2px solid rgba(255,255,255,0.16);display:flex;flex-direction:column;align-items:center;justify-content:center;opacity:0;">'
    f'<svg viewBox="0 0 74 74" style="width:52px;height:52px;">{SIC[k]}</svg>'
    f'<div class="gr" style="font-weight:700;font-size:44px;color:#fff;line-height:1.1;">{v} <span style="font-size:32px;color:#d4d4d8;">{u}</span></div></div>'
    for i, (k, v, u) in enumerate(SPECS))
b = (f'<div class="card" id="pr-card" style="position:absolute;left:100px;top:20px;width:880px;height:640px;border:4px solid {RED};opacity:0;">'
     '<div class="anton" style="position:absolute;top:34px;width:100%;text-align:center;font-size:78px;color:#fff;">INDIAN RDP PLAN</div>'
     + chips +
     f'<div class="anton" id="pr-p" style="position:absolute;top:330px;width:100%;text-align:center;font-size:190px;color:{RED};text-shadow:0 0 60px rgba(225,29,72,0.5);">₹3,000</div>'
     '<div class="gr" style="position:absolute;top:548px;width:100%;text-align:center;font-weight:700;font-size:50px;color:#fff;">per month</div></div>')
C["price"] = comp("price", f'<div class="panel">{b}</div>',
                  '    tl.fromTo("#pr-card", { scale: 0.7, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.45, ease: "back.out(1.8)" }, 0.1);\n'
                  + "".join(f'    tl.fromTo("#pr-s{i}", {{ y: 30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.3, ease: "back.out(2)" }}, {0.35 + i * 0.15:.2f});\n' for i in range(3))
                  + f'    tl.fromTo("#pr-p", {{ scale: 0.4 }}, {{ scale: 1, duration: 0.4, ease: "back.out(2.4)" }}, {at(7, 0.6, "price")});\n')
for i in range(3):
    mark("price", 0.35 + i * 0.15)
mark("price", at(7, 0.6, "price"), "cash")

# RDP login steps (lines 8-11)
b = (row("rdp-r0", 0, '<div class="num">1</div>' + icon("monitor"), "Remote Desktop Connection", "computer / laptop par open karein")
     + row("rdp-r1", 160, '<div class="num">2</div>' + icon("plug"), "RDP IP address → Connect", "IP hamari taraf se milega")
     + row("rdp-r2", 320, '<div class="num">3</div>' + icon("key"), "Login ID + Password", "hamari taraf se provide kiya jayega")
     + row("rdp-r3", 480, icon("check"), "Remote desktop open!", "", "#16a34a"))
js = "".join(pop(f"#rdp-r{i}", at(8 + i, 0.08, "rdp")) for i in range(4))
C["rdp"] = comp("rdp", f'<div class="panel"><div class="gr" style="position:absolute;top:-80px;font-weight:700;font-size:40px;letter-spacing:8px;color:#d4d4d8;">RDP LOGIN</div>{b}</div>', js)
for i in range(4):
    mark("rdp", at(8 + i, 0.08, "rdp"), "ok" if i == 3 else "pop")

# BUSY steps (lines 12-15)
b = (row("busy-r0", 0, '<div class="num">4</div>' + icon("app"), "Desktop par BUSY icon")
     + row("busy-r1", 160, '<div class="num">5</div>' + icon("app"), "BUSY open → Company select", "aur kaam start")
     + row("busy-r2", 320, icon("check"), "Daily billing · accounting · stock", "", "#16a34a")
     + row("busy-r3", 480, icon("nobox"), "Local PC par install? <span class='k'>Nahi</span>", "software RDP par pehle se installed", BLUE))
js = "".join(pop(f"#busy-r{i}", at(12 + i, 0.08, "busy")) for i in range(4))
C["busy"] = comp("busy", f'<div class="panel"><div class="gr" style="position:absolute;top:-80px;font-weight:700;font-size:40px;letter-spacing:8px;color:#d4d4d8;">BUSY SOFTWARE</div>{b}</div>', js)
for i in range(4):
    mark("busy", at(12 + i, 0.08, "busy"))

# important (lines 16-18)
b = (row("imp-r0", 0, icon("lock"), "Login ID / password", "kisi ke saath share mat karein")
     + row("imp-r1", 160, icon("backup"), "Company data ka backup", "regular zaroor lein", BLUE)
     + row("imp-r2", 320, icon("help"), "Koi problem?", "hamari support team se contact karein", "#16a34a"))
js = "".join(pop(f"#imp-r{i}", at(16 + i, 0.08, "imp")) for i in range(3))
C["imp"] = comp("imp", f'<div class="panel"><div class="gr" style="position:absolute;top:-80px;font-weight:700;font-size:40px;letter-spacing:8px;color:{RED};">IMPORTANT</div>{b}</div>', js)
for i in range(3):
    mark("imp", at(16 + i, 0.08, "imp"))

# outro (lines 19-20)
b = ('<div class="anton" id="out-a" style="position:absolute;top:60px;left:0;font-size:110px;color:#fff;opacity:0;">INDIAN RDP <span class="k">+</span> BUSY</div>'
     '<div class="anton" id="out-b" style="position:absolute;top:210px;left:0;font-size:110px;color:#16a34a;opacity:0;">EASY!</div>'
     + row("out-r0", 420, icon("check"), "Time save", "", "#16a34a") + row("out-r1", 580, icon("check"), "Business manage karna aur bhi easy", "", "#16a34a"))
C["outro"] = comp("outro", f'<div class="panel">{b}</div>', pop("#out-a", at(19, 0.05, "outro")) + pop("#out-b", at(19, 0.6, "outro"))
                  + pop("#out-r0", at(20, 0.2, "outro")) + pop("#out-r1", at(20, 0.55, "outro")))
mark("outro", at(20, 0.2, "outro"), "ok"); mark("outro", at(20, 0.55, "outro"), "ok")

os.makedirs("compositions", exist_ok=True)
for k, v in C.items():
    open(f"compositions/{k}.html", "w").write(v)

# background
stars = "".join(f'<div style="position:absolute;left:{(i * 397) % 1920}px;top:{(i * 613) % 1080}px;width:{2 + i % 3}px;height:{2 + i % 3}px;border-radius:50%;background:rgba(255,255,255,{0.2 + (i % 4) * 0.1});"></div>' for i in range(80))
open("compositions/bg.html", "w").write(f"""<template>
  <div id="root" data-composition-id="bg" data-width="1920" data-height="1080">
    <div style="position:absolute;inset:0;background:{DARK};"></div>
    <div id="bg-red" style="position:absolute;left:1100px;top:-300px;width:1100px;height:1100px;border-radius:50%;background:radial-gradient(circle, rgba(225,29,72,0.26), rgba(225,29,72,0) 70%);" data-layout-allow-overflow></div>
    <div id="bg-blue" style="position:absolute;left:-300px;top:300px;width:1000px;height:1000px;border-radius:50%;background:radial-gradient(circle, rgba(59,130,246,0.22), rgba(59,130,246,0) 70%);" data-layout-allow-overflow></div>
    <div id="bg-stars" style="position:absolute;inset:0;" data-layout-allow-overflow>{stars}</div>
    <div style="position:absolute;left:0;right:0;bottom:0;height:260px;background:linear-gradient(to bottom, rgba(5,5,5,0), rgba(5,5,5,0.92));"></div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    tl.fromTo("#bg-stars", {{ y: 0 }}, {{ y: -120, duration: {TOTAL}, ease: "none" }}, 0);
    tl.fromTo("#bg-red", {{ scale: 0.9 }}, {{ scale: 1.15, duration: {TOTAL / 2:.2f}, ease: "sine.inOut", yoyo: true, repeat: 1 }}, 0);
    window.__timelines["bg"] = tl;
  </script>
</template>
""")

# captions: owner's Roman lines, split into chunks of <= 42 chars, timed by character share of each VO line
chunks = []
for i, text in enumerate(CAP):
    words, cur, parts = text.split(), "", []
    for w in words:
        if cur and len(cur) + 1 + len(w) > 42:
            parts.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    parts.append(cur)
    groups = [parts[j:j + 2] for j in range(0, len(parts), 2)]   # max 2 lines per caption
    total = sum(len(" ".join(g)) for g in groups)
    t = T0[i]
    for g in groups:
        d = (T1[i] - T0[i]) * len(" ".join(g)) / total
        chunks.append((round(t, 2), round(t + d, 2), g)); t += d
cap_html, cap_js = [], []
for j, (a, e, g) in enumerate(chunks):
    lines = "<br>".join(H.escape(x) for x in g)
    cap_html.append(f'<div class="cap" id="cap{j}" style="opacity:0;">{lines}</div>')
    cap_js.append(f'    tl.fromTo("#cap{j}", {{ opacity: 0, y: 10 }}, {{ opacity: 1, y: 0, duration: 0.12 }}, {a});\n'
                  f'    tl.to("#cap{j}", {{ opacity: 0, duration: 0.08 }}, {max(a + 0.2, e - 0.02):.2f});\n')
open("compositions/caps.html", "w").write(f"""<template>
  <style>
    @font-face {{ font-family: "Grotesk"; src: url("assets/fonts/SpaceGrotesk-Variable.ttf"); font-weight: 300 700; }}
    #root {{ position: absolute; inset: 0; }}
    .cap {{ position: absolute; left: 200px; right: 200px; top: 868px; text-align: center; font-family: Grotesk; font-weight: 700;
            font-size: 40px; line-height: 1.25; color: #fff; text-shadow: 0 3px 12px rgba(0,0,0,0.9); }}
  </style>
  <div id="root" data-composition-id="caps" data-width="1920" data-height="1080">
{chr(10).join(cap_html)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{''.join(cap_js)}    window.__timelines["caps"] = tl;
  </script>
</template>
""")

# host: talk while each line is spoken, idle in the gaps, wave on hello / thank you, point at new step cards
moves = []
for i in range(len(L)):
    moves.append([T0[i], "wave" if i in (0, 21, 23) else ("point" if i in (8, 9, 10, 12, 13) else "talk")])
    moves.append([T1[i], "idle"])
json.dump(moves, open("host_moves.json", "w"))
subprocess.run(["python3", os.environ.get("REPO", "/home/user/new-startup") + "/library/tools/blocky_character.py", "compositions/host.html",
                "--skin", "assets/characters/host-skin.png", "--id", "host", "--duration", str(S0["end"]), "--scale", "19",
                "--width", "700", "--height", "1080", "--x", "350", "--y", "840", "--turn", "18", "--moves", json.dumps(moves)], check=True)

host = lambda cid, s, du, lane, z, w=1920, h=1080: (f'      <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" data-start="{s}" '
                                                  f'data-duration="{round(du, 3)}" data-track-index="{lane}" data-track-kind="graphics" data-width="{w}" data-height="{h}" style="z-index: {z}"></div>')
divs = [host("bg", 0, TOTAL, 0, 0)]
for k in order[:-1]:
    divs.append(host(k, S0[k], S1[k] - S0[k], 1, 2))
divs.append(host("host", 0, S0["end"], 2, 3, 700, 1080).replace('style="z-index: 3"', 'style="z-index: 3; position:absolute; left:0; top:0; width:700px; height:1080px;"'))
divs.append(host("brand-bug", 0, S0["end"], 3, 4))
divs.append(host("brand-end", S0["end"], TOTAL - S0["end"], 1, 2))
divs.append(f'      <div id="caps" data-composition-id="caps" data-composition-src="compositions/caps.html" data-start="0" data-duration="{TOTAL}" '
            f'data-track-index="5" data-track-kind="captions" data-width="1920" data-height="1080" style="z-index: 6"></div>')

# phone pill on the end card pulses when line 22 says "contact" (client asked for his number at the end)
T_PH = round(T0[22] + 0.75 * (T1[22] - T0[22]), 2)
be = open("compositions/brand-end.html").read()
import re as _re
be = _re.sub(r"\}, (PHONE_PULSE|[0-9.]+)\);\n    window.__timelines\[\"brand-end\"\]", "}, %.2f);\n    window.__timelines[\"brand-end\"]" % (T_PH - S0["end"]), be)
open("compositions/brand-end.html", "w").write(be)
sfx = lambda n: f"assets/sfx/{n}.mp3"
A = [("vo", VO_FILE, VO_START, dur(VO_FILE), 1.0, 10, 0),
     ("m1", "assets/music/music.mp3", 0, round(T1[-1] + 0.3, 2), 0.2, 11, 0),
     ("m2", "assets/music/music.mp3", round(T1[-1] + 0.3, 2), round(TOTAL - T1[-1] - 0.3, 2), 0.5, 12, round(T1[-1] + 0.3, 2))]
for j, k in enumerate(order[1:]):
    A.append((f"wh{j}", sfx("swish-4"), round(max(0, S0[k] - 0.046), 2), dur(sfx("swish-4")), 0.5, 13 + j % 2, 0))
hit = {"pop": ("pop-high", 0.006, 0.45), "ok": ("confirm-1", 0.005, 0.5), "cash": ("cash-register", 0.005, 0.45)}
for j, (t, kind) in enumerate(POPS):
    n, h, v = hit[kind]
    A.append((f"p{j}", sfx(n), round(t - h, 2), dur(sfx(n)), v, 15 + j % 2, 0))
A.append(("ding", sfx("ding-real"), round(T_PH - 0.007, 2), dur(sfx("ding-real")), 0.5, 18, 0))
A.append(("chime", sfx("success-chime"), round(S0["end"] + 0.1, 2), dur(sfx("success-chime")), 0.4, 17, 0))
aud = "\n".join(f'      <audio id="{i}" src="{s}" data-start="{a}" data-duration="{dd}" data-volume="{v}" data-track-index="{ln}"'
                + (f' data-media-start="{ms}"' if ms else "") + (' data-fade-out="2"' if i == "m2" else "") + "></audio>"
                for i, s, a, dd, v, ln, ms in A)
open("index.html", "w").write(f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="assets/vendor/gsap-3.14.2.min.js"></script>
    <style>* {{ margin: 0; padding: 0; box-sizing: border-box; }} html, body {{ margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: {DARK}; }}</style>
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
print("built", TOTAL, {k: (S0[k], S1[k]) for k in order}, len(chunks), "caption chunks")
