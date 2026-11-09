# Problem -> solution app promo (16:9 or 9:16), edited after three owner references (2026-11-09):
#   ref 1 (pastel kinetic type): sentences built word by word, two weights / two colours, a cut-out object per idea;
#   ref 2 (portfolio): huge outline word behind the subject, rows of cards sliding in;
#   ref 3 (SaaS promo): white rounded stage on a soft gradient, chapter tabs at the bottom (Problem / Solution / ...)
#   with the active pill moving, phone mockups floating in 3D with UI chips around them, cloud-soft ending.
# Visuals = the owner's own app screenshots (phone screens) in CSS-3D phone frames. Text on screen = the VO's points.
#   python3 build.py CONFIG.json --format 16x9|9x16 --out PROJECT
# CONFIG: total, look {bg1, bg2, primary, primary2, text, muted, card}, chapters [names], scenes [{start, chapter, kind,
#   lines [[text, word-time or null, style]], phones [[img, word-time]], chips [[text, word-time]], outline, ...}].
# PROJECT: assets/vendor/gsap-3.14.2.min.js, assets/fonts/{PlusJakartaSans-Variable.ttf,JetBrainsMono-Variable.ttf},
#   assets/img/*.jpg (screens), assets/img/logo.svg, assets/sfx/*.mp3, assets/audio/mix.wav.
import argparse, html, json, os, random, subprocess

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
r3 = lambda x: round(x, 3)
random.seed(5)
T, PRE, HT, SFX = [], [], [], []
P1, P2, TX, MU = L["primary"], L["primary2"], L["text"], L["muted"]


def dur(p):
    return round(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                      capture_output=True, text=True).stdout), 3)


def win(sel, s0, s1):
    if s0 > 0:
        PRE.append(f'gsap.set("{sel}", {{visibility:"hidden"}});')
        T.append(f'tl.set("{sel}", {{visibility:"visible"}}, {r3(s0)});')
    if s1 < TOTAL:
        T.append(f'tl.set("{sel}", {{visibility:"hidden"}}, {r3(s1)});')


def tw(sel, frm, to, at):
    T.append(f'tl.fromTo("{sel}", {frm}, {to}, {r3(at)});')


def sfx(name, at, vol):
    SFX.append((name, r3(max(0, at)), vol))


# ---------------------------------------------------------------- frame: gradient, blobs, white stage, chapter tabs
M = 40 if WIDE else 34                      # stage margin
TAB_H = 86 if WIDE else 96
SX, SY, SW, SH = M, M, W - 2 * M, H - 2 * M - TAB_H - 20
HT.append(f'''<div id="bg" style="position:absolute;inset:0;background:linear-gradient(135deg, {L['bg1']} 0%, {L['bg2']} 100%);"></div>
<div class="blob" id="b1" style="left:{-W * 0.1:.0f}px;top:{H * 0.55:.0f}px;width:{W * 0.6:.0f}px;height:{W * 0.6:.0f}px;background:radial-gradient(circle, rgba(124,58,237,0.55), rgba(124,58,237,0) 70%);"></div>
<div class="blob" id="b2" style="left:{W * 0.55:.0f}px;top:{-H * 0.2:.0f}px;width:{W * 0.6:.0f}px;height:{W * 0.6:.0f}px;background:radial-gradient(circle, rgba(79,70,229,0.5), rgba(79,70,229,0) 70%);"></div>
<div id="stagecard" style="position:absolute;left:{SX}px;top:{SY}px;width:{SW}px;height:{SH}px;border-radius:{34 if WIDE else 40}px;background:{L['card']};
  box-shadow:0 30px 80px rgba(49,31,120,0.35);overflow:hidden;">
  <div id="wash" style="position:absolute;left:0;right:0;bottom:0;height:45%;background:linear-gradient(180deg, rgba(255,255,255,0), rgba(196,181,253,0.55) 70%, rgba(167,139,250,0.65));"></div>
  <div id="stage" style="position:absolute;inset:0;perspective:1600px;"></div>
</div>''')
T.append(f'tl.fromTo("#b1", {{x:0, y:0}}, {{x:{W * 0.25:.0f}, y:-{H * 0.25:.0f}, duration:{TOTAL}, ease:"sine.inOut"}}, 0);')
T.append(f'tl.fromTo("#b2", {{x:0, y:0}}, {{x:-{W * 0.2:.0f}, y:{H * 0.2:.0f}, duration:{TOTAL}, ease:"sine.inOut"}}, 0);')
CH = C["chapters"]
tabw = (SW - 20 * (len(CH) - 1)) / len(CH)
tabs = "".join(f'<div class="tab" id="tab{j}" style="left:{SX + j * (tabw + 20):.0f}px;width:{tabw:.0f}px;">{E(c)}</div>' for j, c in enumerate(CH))
HT.append(f'<div id="tabs" style="position:absolute;left:0;top:{H - M - TAB_H}px;height:{TAB_H}px;width:{W}px;">'
          f'<div id="pill" style="position:absolute;left:{SX}px;top:0;width:{tabw:.0f}px;height:{TAB_H}px;border-radius:999px;background:#0f0b1f;"></div>{tabs}</div>')
# progress ticks under the tabs
first = {}
for s in SC:
    first.setdefault(s["chapter"], s["start"])
for j, c in enumerate(CH):
    if c in first:
        t = first[c]
        T.append(f'tl.to("#pill", {{left:{SX + j * (tabw + 20):.0f}, duration:0.45, ease:"power3.inOut"}}, {r3(max(0, t - 0.2))});')
        T.append(f'tl.to(".tab", {{color:"#3b3355", duration:0.2}}, {r3(max(0, t - 0.2))});')
        T.append(f'tl.to("#tab{j}", {{color:"#ffffff", duration:0.2}}, {r3(max(0, t - 0.05))});')
        if t > 0:
            sfx("click-1", t - 0.05, 0.25)
PRE.append('gsap.set(".tab", {color:"#3b3355"}); gsap.set("#tab0", {color:"#ffffff"});')

# ---------------------------------------------------------------- scene pieces (positions inside the stage card)
if WIDE:
    TXT_X, TXT_Y, TXT_W, FS = 90, 170, 980, 92
    PH_W = 330
else:
    TXT_X, TXT_Y, TXT_W, FS = 60, 120, SW - 120, 92
    PH_W = 380
PH_H = round(PH_W * 1965 / 1080) + 36        # screenshot ratio + bezel


def lines_html(k, lines, s0, s1, x=None, y=None, w=None, fs=None, align=None):
    """sentence built word by word; style 'b' = bold dark, 'a' = accent gradient, 'l' = light italic, 'o' = outline"""
    x = TXT_X if x is None else x
    y = TXT_Y if y is None else y
    w = TXT_W if w is None else w
    fs = fs or FS
    al = align or ("left" if WIDE else "center")
    out, n = [], 0
    for li, (text, t0, style) in enumerate(lines):
        ws = []
        words = text.split(" ")
        for wi, wd in enumerate(words):
            wid = f"{k}w{n}"
            ws.append(f'<span class="w {style}" id="{wid}">{E(wd)}</span>')
            t = (t0 if t0 is not None else s0 + 0.2 + li * 0.5) + wi * 0.11
            tw(f"#{wid}", "{y:'0.6em', opacity:0, filter:'blur(10px)'}", "{y:0, opacity:1, filter:'blur(0px)', duration:0.4, ease:'power3.out'}", t)
            n += 1
        fsz = fs * (0.62 if style == "l" else 1.0)
        out.append(f'<div class="ln" style="font-size:{fsz:.0f}px;">{" ".join(ws)}</div>')
    STAGE.append(f'<div class="tx" id="{k}tx" style="left:{x}px;top:{y}px;width:{w}px;text-align:{al};">{"".join(out)}</div>')
    tw(f"#{k}tx", "{opacity:1}", "{opacity:0, y:-40, filter:'blur(8px)', duration:0.35}", s1 - 0.35)
    win(f"#{k}tx", s0, s1)


def phone(pid, img, x, y, rot, t_in, s1, scale=1.0, z=0):
    w, h = PH_W * scale, PH_H * scale
    STAGE.append(f'<div class="phone" id="{pid}" style="left:{x - w / 2:.0f}px;top:{y - h / 2:.0f}px;width:{w:.0f}px;height:{h:.0f}px;">'
                 f'<img src="assets/img/{img}" alt="AI Video Automator screen" style="position:absolute;left:{14 * scale:.0f}px;top:{14 * scale:.0f}px;'
                 f'width:{w - 28 * scale:.0f}px;height:{h - 28 * scale:.0f}px;border-radius:{30 * scale:.0f}px;object-fit:cover;object-position:top;"></div>')
    tw(f"#{pid}", f"{{y:{H * 0.7:.0f}, rotationX:45, rotationY:{rot * 2}, z:-400, opacity:0}}",
       f"{{y:0, rotationX:8, rotationY:{rot}, z:{z}, opacity:1, duration:0.75, ease:'power3.out'}}", t_in)
    T.append(f'tl.to("#{pid}", {{rotationY:{-rot * 0.6:.1f}, y:-24, duration:{max(0.6, s1 - t_in - 1.1):.2f}, ease:"sine.inOut"}}, {r3(t_in + 0.75)});')
    T.append(f'tl.to("#{pid}", {{y:-{H * 0.8:.0f}, rotationX:-30, opacity:0, duration:0.4, ease:"power2.in"}}, {r3(s1 - 0.4)});')
    sfx("whoosh-up-0.6s", t_in + 0.25, 0.3)
    win(f"#{pid}", t_in, s1)


def chip(cid, text, x, y, t, s1, icon=""):
    STAGE.append(f'<div class="chip" id="{cid}" style="left:{x:.0f}px;top:{y:.0f}px;">{icon}{E(text)}</div>')
    tw(f"#{cid}", "{scale:0.4, opacity:0, y:30}", "{scale:1, opacity:1, y:0, duration:0.4, ease:'back.out(2)'}", t)
    T.append(f'tl.to("#{cid}", {{y:"-=14", duration:1.6, yoyo:true, repeat:{max(0, int((s1 - t) / 1.6) // 2 * 2)}, ease:"sine.inOut"}}, {r3(t + 0.4)});')
    sfx(["pop-high", "pop-low", "plop"][len(SFX) % 3], t + 0.05, 0.28)
    win(f"#{cid}", t, s1)


def outline(oid, word, s0, s1, y=None):
    fs = 300 if WIDE else 220
    STAGE.append(f'<div class="outl" id="{oid}" style="top:{(y if y is not None else SH * 0.32):.0f}px;font-size:{fs}px;">{E(word)}</div>')
    tw(f"#{oid}", "{x:300, opacity:0}", f"{{x:-120, opacity:1, duration:{max(1, s1 - s0):.2f}, ease:'none'}}", s0)
    win(f"#{oid}", s0, s1)


STAGE = []
for i, s in enumerate(SC):
    k, s0, s1, kind = f"s{i}", s["start"], s["end"], s.get("kind", "text")
    if i > 0:
        sfx(["swish-1", "whoosh-fast-0.3s", "swish-4"][i % 3], s0 - 0.12, 0.35)
    if s.get("outline"):
        outline(f"{k}o", s["outline"], s0, s1)
    if kind == "hook":       # problem montage: task words stack and pile up, a clock spins
        lines_html(k, s["lines"], s0, s1)
        for j, (wd, t) in enumerate(s["chips"]):
            x = (1100 + (j % 2) * 300) if WIDE else (100 + (j % 3) * 300)
            y = (150 + j * 110) if WIDE else (900 + (j // 3) * 150 + (j % 3) * 40)
            chip(f"{k}c{j}", wd, x, y, t, s1)
        continue
    if kind == "pc":         # the old way: a PC that must stay on, with a clock running round
        cx, cy = (SW * 0.72, SH * 0.48) if WIDE else (SW / 2, SH * 0.62)
        # the old desktop software playing on the monitor (the site's own tutorial clip, config "pc_video")
        pcv = (f'<video id="{k}pv" src="{s["pc_video"]}" data-start="{r3(s0)}" data-duration="{r3(s1 - s0)}" muted playsinline '
               f'style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0.85;"></video>') if s.get("pc_video") else ""
        STAGE.append(f'''<div class="pc" id="{k}pc" style="left:{cx - 260:.0f}px;top:{cy - 190:.0f}px;">
  <div class="mon"><div class="scr">{pcv}<div class="bar" id="{k}bar"></div><div class="lbl">PC ON</div></div></div><div class="neck"></div><div class="base"></div></div>
<div class="clock" id="{k}clk" style="left:{cx + (150 if WIDE else 140):.0f}px;top:{cy - (260 if WIDE else 300):.0f}px;"><div class="hand" id="{k}hd"></div><div class="hand2" id="{k}hm"></div></div>''')
        tw(f"#{k}pc", "{scale:0.6, opacity:0, rotationY:-40}", "{scale:1, opacity:1, rotationY:-12, duration:0.6, ease:'back.out(1.6)'}", s0 + 0.1)
        tw(f"#{k}clk", "{scale:0, opacity:0}", "{scale:1, opacity:1, duration:0.4, ease:'back.out(2)'}", s0 + 0.5)
        T.append(f'tl.fromTo("#{k}hd", {{rotation:0}}, {{rotation:1440, duration:{s1 - s0 - 0.6:.2f}, ease:"none"}}, {r3(s0 + 0.6)});')
        T.append(f'tl.fromTo("#{k}hm", {{rotation:0}}, {{rotation:120, duration:{s1 - s0 - 0.6:.2f}, ease:"none"}}, {r3(s0 + 0.6)});')
        T.append(f'tl.fromTo("#{k}bar", {{scaleX:0}}, {{scaleX:1, duration:{s1 - s0 - 0.8:.2f}, ease:"none"}}, {r3(s0 + 0.6)});')
        T.append(f'tl.to("#{k}pc", {{y:-{H:.0f}, opacity:0, duration:0.4, ease:"power2.in"}}, {r3(s1 - 0.4)});')
        T.append(f'tl.to("#{k}clk", {{scale:0, opacity:0, duration:0.3}}, {r3(s1 - 0.35)});')
        sfx("clock-tick-tock", s0 + 0.6, 0.25)
        win(f"#{k}pc", s0, s1)
        win(f"#{k}clk", s0, s1)
        lines_html(k, s["lines"], s0, s1, y=(TXT_Y if WIDE else 140))
        continue
    if kind == "reveal":     # "ab nahi!" -> logo + URL burst
        cx, cy = SW / 2, SH * (0.36 if WIDE else 0.34)
        STAGE.append(f'<div class="logo" id="{k}lg" style="left:{cx - 110:.0f}px;top:{cy - 110:.0f}px;"><img src="assets/img/logo.svg" alt="AI Video Automator logo" style="width:220px;height:220px;"></div>'
                     f'<div class="ring" id="{k}rg" style="left:{cx - 150:.0f}px;top:{cy - 150:.0f}px;"></div>'
                     f'<div class="url" id="{k}url" style="top:{cy + 300 if WIDE else cy + 520:.0f}px;">{E(s["url"])}</div>')
        tw(f"#{k}lg", "{scale:0, rotation:-180, opacity:0}", "{scale:1, rotation:0, opacity:1, duration:0.6, ease:'back.out(1.8)'}", s["t_logo"])
        tw(f"#{k}rg", "{scale:0.4, opacity:0.9}", "{scale:5, opacity:0, duration:1.0, ease:'power2.out'}", s["t_logo"] + 0.1)
        tw(f"#{k}url", "{y:40, opacity:0, scale:0.8}", "{y:0, opacity:1, scale:1, duration:0.45, ease:'back.out(2)'}", s["t_url"])
        sfx("impact-boom", s["t_logo"] + 0.1, 0.45)
        sfx("sparkle", s["t_url"], 0.3)
        win(f"#{k}lg", s["t_logo"] - 0.05, s1)
        win(f"#{k}rg", s["t_logo"], s["t_logo"] + 1.2)
        win(f"#{k}url", s["t_url"] - 0.05, s1)
        T.append(f'tl.to(["#{k}lg", "#{k}url"], {{opacity:0, scale:1.2, duration:0.35}}, {r3(s1 - 0.35)});')
        lines_html(k, s["lines"], s0, s1, y=(SH * 0.56 if WIDE else SH * 0.53), align="center", x=60, w=SW - 120)
        continue
    if kind == "end":
        cx = SW / 2
        STAGE.append(f'<div class="logo" id="{k}lg" style="left:{cx - 100:.0f}px;top:{SH * 0.12:.0f}px;"><img src="assets/img/logo.svg" alt="AI Video Automator logo" style="width:200px;height:200px;"></div>'
                     f'<div class="endt" id="{k}t" style="top:{SH * 0.12 + 230:.0f}px;">AI Video Automator</div>'
                     f'<div class="price" id="{k}p" style="top:{SH * 0.12 + 350:.0f}px;">{E(s["price"])}</div>'
                     f'<div class="cta" id="{k}c" style="top:{SH * 0.12 + (500 if WIDE else 520):.0f}px;"><span>{E(s["url"])}</span></div>'
                     f'<div class="small" id="{k}s" style="top:{SH * 0.12 + (640 if WIDE else 660):.0f}px;">{E(s["small"])}</div>')
        tw(f"#{k}lg", "{scale:0, rotation:-120}", "{scale:1, rotation:0, duration:0.6, ease:'back.out(1.8)'}", s0 + 0.05)
        tw(f"#{k}t", "{y:40, opacity:0}", "{y:0, opacity:1, duration:0.45}", s0 + 0.3)
        tw(f"#{k}p", "{scale:0.5, opacity:0}", "{scale:1, opacity:1, duration:0.4, ease:'back.out(2.2)'}", s["t_price"])
        tw(f"#{k}c", "{scale:0.5, opacity:0}", "{scale:1, opacity:1, duration:0.4, ease:'back.out(2.2)'}", s["t_url"])
        T.append(f'tl.to("#{k}c span", {{scale:1.06, duration:0.45, yoyo:true, repeat:5, ease:"sine.inOut"}}, {r3(s["t_url"] + 0.45)});')
        tw(f"#{k}s", "{opacity:0}", "{opacity:1, duration:0.5}", s["t_url"] + 0.6)
        sfx("impact-punch", s["t_price"], 0.4)
        sfx("confirm-1", s["t_url"], 0.35)
        for q in ("lg", "t", "p", "c", "s"):
            win(f"#{k}{q}", s0, TOTAL + 1)
        continue
    # default: kinetic text + phones + chips
    lines_html(k, s["lines"], s0, s1, **s.get("text_pos", {}).get(a.format, {}))
    for j, (img, t) in enumerate(s.get("phones", [])):
        n = len(s["phones"])
        if WIDE:
            x = SW - 300 - (n - 1 - j) * 330
            y = SH * 0.52
        else:
            x = SW / 2 + (j - (n - 1) / 2) * 400
            y = SH * 0.66
        phone(f"{k}ph{j}", img, x, y, (-14 if j % 2 == 0 else 14), t, s1, scale=(1.0 if n == 1 else 0.92), z=j * 40)
    for j, (text, t) in enumerate(s.get("chips", [])):
        if WIDE:
            x, y = 90 + (j % 2) * 380, SH * 0.62 + (j // 2) * 120
        else:
            x, y = 60 + (j % 2) * 480, SH * 0.36 + (j // 2) * 120
        chip(f"{k}c{j}", text, x, y, t, s1, icon='<span class="dot"></span>')

HT.insert(2, "")  # keep order
stage_html = "\n".join(STAGE)
HT = [h.replace('<div id="stage" style="position:absolute;inset:0;perspective:1600px;"></div>',
                f'<div id="stage" style="position:absolute;inset:0;perspective:1600px;">{stage_html}</div>') for h in HT]

CSS = f"""
@font-face {{ font-family: "PJ"; src: url("assets/fonts/PlusJakartaSans-Variable.ttf"); font-weight: 200 800; }}
@font-face {{ font-family: "JB"; src: url("assets/fonts/JetBrainsMono-Variable.ttf"); font-weight: 100 800; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:{L['bg1']}; }}
#root {{ position:absolute; inset:0; overflow:hidden; font-family:PJ; color:{TX}; }}
.blob {{ position:absolute; border-radius:50%; }}
.tab {{ position:absolute; top:0; height:{TAB_H}px; line-height:{TAB_H}px; text-align:center; font-weight:700; font-size:{28 if WIDE else 26}px;
        border-radius:999px; background:rgba(255,255,255,0.55); }}
#pill {{ z-index:0; }} .tab {{ z-index:1; background:transparent; }}
#tabs::before {{ content:""; position:absolute; left:{SX}px; right:{SX}px; top:0; bottom:0; border-radius:999px; background:rgba(255,255,255,0.45); }}
.tx {{ position:absolute; }}
.ln {{ line-height:1.08; letter-spacing:-2px; margin-bottom:6px; }}
.w {{ display:inline-block; }}
.w.b {{ font-weight:800; color:{TX}; }}
.w.a {{ font-weight:800; background:linear-gradient(90deg, {P1}, {P2}); -webkit-background-clip:text; background-clip:text; color:transparent; }}
.w.l {{ font-weight:500; font-style:italic; color:{MU}; letter-spacing:-0.5px; }}
.w.o {{ font-weight:800; color:transparent; -webkit-text-stroke:3px {P1}; }}
.outl {{ position:absolute; left:0; white-space:nowrap; font-weight:800; letter-spacing:-8px; color:transparent; -webkit-text-stroke:3px rgba(79,70,229,0.16); }}
.phone {{ position:absolute; border-radius:46px; background:#0f0b1f; box-shadow:0 40px 90px rgba(49,31,120,0.45), inset 0 0 0 3px #2d2550; }}
.chip {{ position:absolute; display:flex; align-items:center; gap:14px; font-weight:700; font-size:{34 if WIDE else 36}px; padding:16px 28px; border-radius:20px;
         background:#ffffff; color:{TX}; box-shadow:0 18px 40px rgba(49,31,120,0.22); border:2px solid rgba(79,70,229,0.18); white-space:nowrap; }}
.dot {{ width:16px; height:16px; border-radius:50%; background:linear-gradient(135deg, {P1}, {P2}); flex:none; }}
.pc {{ position:absolute; width:520px; height:400px; }}
.mon {{ position:absolute; left:0; top:0; width:520px; height:320px; border-radius:22px; background:#1d1834; padding:18px; box-shadow:0 30px 70px rgba(49,31,120,0.35); }}
.scr {{ position:relative; width:100%; height:100%; border-radius:12px; background:linear-gradient(135deg, #312e81, #4c1d95); overflow:hidden; }}
.bar {{ position:absolute; left:0; bottom:0; height:16px; width:100%; background:#f87171; transform-origin:0 50%; }}
.lbl {{ position:absolute; left:16px; top:14px; font-family:JB; font-weight:800; font-size:30px; color:#fff; background:#ef4444; padding:4px 14px; border-radius:8px; }}
.neck {{ position:absolute; left:230px; top:320px; width:60px; height:50px; background:#2d2550; }}
.base {{ position:absolute; left:150px; top:368px; width:220px; height:22px; border-radius:11px; background:#2d2550; }}
.clock {{ position:absolute; width:190px; height:190px; border-radius:50%; background:#fff; border:10px solid {TX}; box-shadow:0 20px 50px rgba(49,31,120,0.3); }}
.hand, .hand2 {{ position:absolute; left:50%; bottom:50%; width:8px; margin-left:-4px; border-radius:4px; background:{TX}; transform-origin:50% 100%; }}
.hand {{ height:72px; background:#ef4444; }} .hand2 {{ height:52px; }}
.logo {{ position:absolute; }}
.ring {{ position:absolute; width:300px; height:300px; border-radius:50%; border:8px solid {P2}; }}
.url {{ position:absolute; left:0; right:0; text-align:center; font-family:JB; font-weight:800; font-size:{64 if WIDE else 58}px; color:{P1}; }}
.endt {{ position:absolute; left:0; right:0; text-align:center; font-weight:800; font-size:{96 if WIDE else 84}px; letter-spacing:-3px; }}
.price {{ position:absolute; left:0; right:0; text-align:center; font-weight:700; font-size:{54 if WIDE else 52}px; color:{MU}; }}
.cta {{ position:absolute; left:0; right:0; text-align:center; }}
.cta span {{ display:inline-block; font-family:JB; font-weight:800; font-size:{60 if WIDE else 52}px; color:#fff; padding:22px 48px; border-radius:22px;
             background:linear-gradient(90deg, {P1}, {P2}); box-shadow:0 20px 50px rgba(79,70,229,0.4); }}
.small {{ position:absolute; left:0; right:0; text-align:center; font-size:{34 if WIDE else 34}px; color:{MU}; }}
"""

A = [("mix", "assets/audio/mix.wav", 0, min(dur("assets/audio/mix.wav"), TOTAL), 1.0)]
A += [(f"fx{n}", f"assets/sfx/{nm}.mp3", t, None, v) for n, (nm, t, v) in enumerate(SFX)]
lanes, aud = [], []
for i, p, st, dd, v in sorted(A, key=lambda x: x[2]):
    if not os.path.exists(p):
        print("missing sfx", p)
        continue
    dd = min(dd or dur(p), dur(p), r3(TOTAL - st))
    if dd <= 0.05:
        continue
    j = next((q for q, e in enumerate(lanes) if e <= st), None)
    if j is None:
        lanes.append(0)
        j = len(lanes) - 1
    lanes[j] = st + dd + 0.01
    aud.append(f'<audio id="{i}" src="{p}" data-start="{st}" data-duration="{dd}" data-volume="{v}" data-track-index="{10 + j}"></audio>')

open("index.html", "w").write(f"""<!doctype html>
<html lang="en" data-resolution="{'landscape' if WIDE else 'portrait'}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width={W}, height={H}">
<script src="assets/vendor/gsap-3.14.2.min.js"></script>
<style>{CSS}</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="{W}" data-height="{H}">
{chr(10).join(HT)}
{chr(10).join(aud)}
</div>
<script>
{chr(10).join(PRE)}
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(T)}
tl.to({{}}, {{ duration: {TOTAL} }}, 0);
window.__timelines = window.__timelines || {{}};
window.__timelines["main"] = tl;
</script>
</body>
</html>
""")
print(f"built {a.format}: {len(T)} tweens, {len(aud)} audio, {len(SC)} scenes")
