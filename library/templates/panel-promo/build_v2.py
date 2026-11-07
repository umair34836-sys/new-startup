# panel-promo v2: the same recordings + VO as build.py, edited "with jan" (owner, 2026-11-07: "editing me jan dallo,
# 3d editing kro, special transitions, animations, kuch naya try kro"). Run build.py first (it makes the speed-fitted
# assets/clips/<scene>.mp4 and timing.json); this script rewrites index.html.
#   python3 build_v2.py CONFIG.json --format 16x9|9x16 --out PROJECT
# What it adds: a CSS-3D stage (perspective) with a moving copper grid floor and floating particles; every recording
# plays on a tilted floating screen that flies in and leaves with a different camera move (depth fly, flip, swing,
# zoom-through); a copper light sweep + whoosh on every cut; kinetic headlines whose words rise in 3D on the words the
# voice says (config "words": Whisper word times on the video timeline); per-scene specials from config "fx":
#   hook (3D logo cube + stacked lines), flow (server -> panel diagram, packets only go out), push (camera pushes into
#   a region of the screen), tiles (metric tiles pop out of the screen), toasts, shutter (camera brackets + flash),
#   orbit (ring of names around a rolling counter), glitch (RGB-split shake + Confirm button), stack (chips fly in on
#   their words), steps (three 3D cards fan out), connected (green shockwave), end (logo cube + CTA + typed URL).
# Rules kept: no blend modes / filters on preserve-3d containers (they flatten 3D, CLAUDE.md); filters only on leaves;
# Hallmark floor (no eyebrow labels, no tracked caps, no single coloured word); unique ids; even yoyo repeats.
import argparse, html, json, math, os, random, subprocess

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
random.seed(11)
ACC, OK, TXT, MUT = L["accent"], L["ok"], L["text"], L["muted"]
T, PRE, HT, SFX = [], [], [], []


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


# ---------------------------------------------------------------- background: glow, 3D grid floor, particles
HT.append(f'''<div id="bg" style="position:absolute;inset:0;background:radial-gradient(70% 60% at 50% 40%, #2a2216 0%, #121110 55%, #0a0a0a 100%);"></div>
<div id="floorwrap" style="position:absolute;left:0;top:0;width:{W}px;height:{H}px;perspective:900px;perspective-origin:50% 30%;overflow:hidden;">
  <div id="floor" style="position:absolute;left:{W / 2 - 2000}px;top:{H * 0.55:.0f}px;width:4000px;height:3000px;transform:rotateX(76deg);transform-origin:50% 0;
    background-image:linear-gradient(rgba(201,163,90,0.32) 2px, transparent 2px), linear-gradient(90deg, rgba(201,163,90,0.32) 2px, transparent 2px);
    background-size:110px 110px;-webkit-mask-image:linear-gradient(180deg, rgba(0,0,0,0) 0%, #000 18%, #000 45%, rgba(0,0,0,0) 85%);
    mask-image:linear-gradient(180deg, rgba(0,0,0,0) 0%, #000 18%, #000 45%, rgba(0,0,0,0) 85%);"></div>
</div>''')
T.append(f'tl.fromTo("#floor", {{backgroundPosition:"0px 0px"}}, {{backgroundPosition:"0px {int(110 * TOTAL / 1.6)}px", duration:{TOTAL}, ease:"none"}}, 0);')
parts = []
for k in range(46):
    x, y, sz = random.uniform(0, W), random.uniform(0, H), random.choice([4, 6, 8, 10])
    parts.append(f'<div class="pt" id="pt{k}" style="left:{x:.0f}px;top:{y:.0f}px;width:{sz}px;height:{sz}px;opacity:{random.uniform(0.15, 0.55):.2f};"></div>')
    T.append(f'tl.fromTo("#pt{k}", {{y:0, rotation:0}}, {{y:{-random.uniform(120, 420):.0f}, rotation:{random.choice([-180, 180])}, duration:{TOTAL}, ease:"none"}}, 0);')
HT.append('<div id="parts" style="position:absolute;inset:0;">' + "".join(parts) + "</div>")

# ---------------------------------------------------------------- 3D stage
if WIDE:
    PW, PH, PX, PY = 1180, 664, 1180, 540         # screen plane size and centre
    HX, HY, HWD, HS = 110, 300, 560, 92           # headline box
else:
    PW, PH, PX, PY = 700, 1244, 540, 760
    HX, HY, HWD, HS = 70, 1430, 940, 96
ENTER = [  # (from, to) for the screen plane
    ("{z:-1800, rotationY:-35, rotationX:8, opacity:0}", "{z:0, rotationY:-14, rotationX:4, opacity:1"),
    ("{rotationY:95, x:300, opacity:0}", "{rotationY:-12, x:0, opacity:1"),
    ("{x:-1400, rotationZ:-12, rotationY:30, opacity:0}", "{x:0, rotationZ:0, rotationY:-10, opacity:1"),
    ("{y:900, rotationX:-60, opacity:0}", "{y:0, rotationX:5, rotationY:-12, opacity:1"),
]
EXIT = [
    "{z:900, opacity:0, duration:0.35, ease:'power2.in'}",
    "{rotationY:-100, x:-200, opacity:0, duration:0.35, ease:'power2.in'}",
    "{x:1600, rotationZ:10, opacity:0, duration:0.35, ease:'power2.in'}",
    "{y:-900, rotationX:50, opacity:0, duration:0.35, ease:'power2.in'}",
]
if not WIDE:
    ENTER = [(f, t.replace("rotationY:-14", "rotationY:-8").replace("rotationY:-12", "rotationY:-7").replace("rotationY:-10", "rotationY:-6"))
             for f, t in ENTER]
stage = []
WORDS = C.get("words", [])


def word_t(word, s0, s1, default):
    """time the voice says `word` inside [s0, s1) (first match, case-insensitive), else default"""
    for w, t in WORDS:
        if s0 <= t < s1 and word.lower() in w.lower():
            return t
    return default


def headline(k, lines, s0, s1, keys=None, top=None, size=None, align=None):
    """kinetic headline: words rise in 3D; a word listed in keys lands on its spoken time"""
    size = size or HS
    al = align or ("left" if WIDE else "center")
    pos = f"left:{HX}px;width:{HWD}px;" if WIDE else "left:40px;right:40px;"
    out, n = [], 0
    for li, line in enumerate(lines):
        ws = []
        for wd in line.split(" "):
            ws.append(f'<span class="w" id="{k}w{n}">{E(wd)}</span>')
            t = s0 + 0.25 + n * 0.09
            if keys and wd.lower().strip(".,") in keys:
                t = keys[wd.lower().strip(".,")]
            tw(f"#{k}w{n}", "{rotationX:-95, y:50, opacity:0}", "{rotationX:0, y:0, opacity:1, duration:0.45, ease:'back.out(1.8)'}", t - 0.15)
            n += 1
        out.append(f'<div class="hl" style="font-size:{size}px;">{" ".join(ws)}</div>')
    HT.append(f'<div class="hbox" id="{k}h" style="{pos}top:{top if top is not None else HY}px;text-align:{al};">{"".join(out)}</div>')
    tw(f"#{k}h", "{opacity:1}", "{opacity:0, y:-30, duration:0.3}", s1 - 0.3)
    win(f"#{k}h", s0, s1)


def sub(k, text, at, s1, top_off=None):
    y = (HY + (top_off or 260)) if WIDE else (HY + (top_off or 250))
    pos = f"left:{HX}px;width:{HWD}px;text-align:left;" if WIDE else "left:40px;right:40px;text-align:center;"
    HT.append(f'<div class="sub" id="{k}s" style="{pos}top:{y}px;">{E(text)}</div>')
    tw(f"#{k}s", "{opacity:0, y:20}", "{opacity:1, y:0, duration:0.4}", at)
    win(f"#{k}s", at - 0.05, s1)


def screen(k, i, s, extra="", origin="50% 50%"):
    """floating 3D screen with the scene's clip; preset enter/exit rotate through the list"""
    s0, s1 = s["start"], s["end"]
    d = r3(s1 - s0)
    stage.append(f'''<div class="grp" id="{k}g"><div class="plane" id="{k}p" style="left:{PX - PW / 2:.0f}px;top:{PY - PH / 2:.0f}px;width:{PW}px;height:{PH}px;transform-origin:{origin};">
    <video id="{k}v" src="assets/clips/{k}.mp4" data-start="{s0}" data-duration="{d}" muted playsinline style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;"></video>
    <div class="glare" id="{k}gl"></div></div>{extra}</div>''')
    f, t = ENTER[i % len(ENTER)]
    tw(f"#{k}p", f, t + ", duration:0.6, ease:'power3.out'}", s0)
    T.append(f'tl.to("#{k}p", {{y:-16, z:60, duration:{max(0.5, d - 1.0):.2f}, ease:"sine.inOut"}}, {r3(s0 + 0.6)});')   # slow push-in drift
    T.append(f'tl.fromTo("#{k}gl", {{x:-{PW}}}, {{x:{PW * 2}, duration:1.1, ease:"power2.inOut"}}, {r3(s0 + 0.35)});')
    if i + 1 < len(SC):
        T.append(f'tl.to("#{k}p", {EXIT[i % len(EXIT)]}, {r3(s1 - 0.35)});')
    win(f"#{k}g", s0, s1)


def sweep(at):
    """copper light sweep across the frame on a cut"""
    n = len(SWEEPS)
    SWEEPS.append(f'<div class="sweep" id="sw{n}"></div>')
    tw(f"#sw{n}", f"{{x:{-W * 0.8:.0f}, opacity:1}}", f"{{x:{W * 1.2:.0f}, opacity:0.0, duration:0.55, ease:'power2.inOut'}}", at - 0.25)
    win(f"#sw{n}", at - 0.3, at + 0.35)


SWEEPS = []
WH = ["whoosh-fast-0.3s", "swish-1", "swish-4", "whoosh-up-0.6s"]


def cube(cid, size, cx, cy):
    """3D copper logo cube (the site icon: copper square with a dark core) built from 6 faces"""
    h = size / 2
    faces = [("rotateY(0deg)", 1.0), ("rotateY(180deg)", 0.6), ("rotateY(90deg)", 0.8), ("rotateY(-90deg)", 0.8), ("rotateX(90deg)", 0.95), ("rotateX(-90deg)", 0.5)]
    fs = "".join(f'<div class="face" style="width:{size}px;height:{size}px;transform:{tr} translateZ({h}px);filter:brightness({b});">'
                 f'<div class="core" style="left:{size * 0.28:.0f}px;top:{size * 0.28:.0f}px;width:{size * 0.44:.0f}px;height:{size * 0.44:.0f}px;"></div></div>'
                 for tr, b in faces)
    return f'<div class="cube" id="{cid}" style="left:{cx - h:.0f}px;top:{cy - h:.0f}px;width:{size}px;height:{size}px;">{fs}</div>'


# ---------------------------------------------------------------- scenes
FX = {s["id"]: s.get("fx", {}) for s in SC}
for i, s in enumerate(SC):
    k, s0, s1 = s["id"], s["start"], s["end"]
    fx = FX[k]
    kind = fx.get("kind", "screen")
    if i > 0:
        sweep(s0)
        sfx(WH[i % len(WH)], s0 - 0.15, 0.4)
    if kind == "hook":
        cy = H * (0.33 if WIDE else 0.3)
        stage.append(f'<div class="grp" id="{k}g">{cube(k + "cube", 220 if WIDE else 240, W / 2, cy)}</div>')
        tw(f"#{k}cube", "{rotationX:-30, rotationY:-200, z:-1600, opacity:0}", "{rotationX:-18, rotationY:35, z:0, opacity:1, duration:1.0, ease:'power3.out'}", 0.0)
        T.append(f'tl.to("#{k}cube", {{rotationY:"+=290", duration:{s1 - 1.2:.2f}, ease:"none"}}, 1.0);')
        T.append(f'tl.to("#{k}cube", {{z:700, opacity:0, duration:0.35, ease:"power2.in"}}, {r3(s1 - 0.35)});')
        win(f"#{k}g", 0, s1)
        top = int(H * (0.55 if WIDE else 0.5))
        lines = fx["lines"]
        for li, (line, t) in enumerate(lines):
            lid = f"{k}l{li}"
            HT.append(f'<div class="hookl" id="{lid}" style="top:{top + li * (110 if WIDE else 112)}px;font-size:{100 if WIDE else 84}px;white-space:nowrap;">{E(line)}</div>')
            tw(f"#{lid}", "{rotationX:-90, z:-300, opacity:0}", "{rotationX:0, z:0, opacity:1, duration:0.45, ease:'back.out(1.6)'}", t - 0.2)
            sfx("impact-punch" if li < 2 else "impact-boom", t, 0.35)
            T.append(f'tl.to("#{lid}", {{opacity:0, y:-40, duration:0.25}}, {r3(fx["brand_at"] - 0.3)});')
            win(f"#{lid}", 0, fx["brand_at"])
        bid = f"{k}brand"
        HT.append(f'<div class="hookl" id="{bid}" style="top:{top + (40 if WIDE else 60)}px;font-size:{150 if WIDE else 150}px;letter-spacing:-5px;">copper_work</div>')
        tw(f"#{bid}", "{scale:2.4, opacity:0, filter:'blur(18px)'}", "{scale:1, opacity:1, filter:'blur(0px)', duration:0.4, ease:'power4.out'}", fx["brand_at"] - 0.1)
        sfx("impact-boom", fx["brand_at"], 0.45)
        sfx("riser-2s", fx["brand_at"] - 0.05, 0.3)
        win(f"#{bid}", fx["brand_at"] - 0.15, s1)
        T.append(f'tl.to("#{bid}", {{opacity:0, scale:1.4, duration:0.3}}, {r3(s1 - 0.3)});')
        continue
    if kind == "flow":     # server card -> panel card; packets only travel outwards
        cw, ch = (420, 300) if WIDE else (400, 300)
        if WIDE:
            ax, ay, bx, by = 1000, 520, 1600, 520
        else:
            ax, ay, bx, by = 300, 560, 780, 960
        card = lambda cid, x, y, title, icon: (f'<div class="fcard" id="{cid}" style="left:{x - cw / 2:.0f}px;top:{y - ch / 2:.0f}px;width:{cw}px;height:{ch}px;">'
                                               f'<div class="ficon">{icon}</div><div class="ftitle">{E(title)}</div></div>')
        srv = '<div style="width:86px;height:86px;border-radius:14px;background:#5d8a3a;box-shadow:inset 0 -26px 0 #6b4a2b;"></div>'
        pan = '<div style="width:86px;height:86px;border-radius:14px;background:' + ACC + ';position:relative;"><div style="position:absolute;left:24px;top:24px;width:38px;height:38px;border-radius:6px;background:#111;"></div></div>'
        packets = "".join(f'<div class="pk" id="{k}pk{j}" style="left:{ax:.0f}px;top:{ay:.0f}px;"></div>' for j in range(7))
        stage.append(f'<div class="grp" id="{k}g">{card(k + "a", ax, ay, "Your server", srv)}{card(k + "b", bx, by, "copper_work panel", pan)}{packets}'
                     f'<div class="lock" id="{k}lk" style="left:{ax - 70:.0f}px;top:{ay + ch / 2 + 30:.0f}px;">Port closed</div></div>')
        tw(f"#{k}a", "{rotationY:-90, z:-600, opacity:0}", "{rotationY:18, z:0, opacity:1, duration:0.6, ease:'power3.out'}", s0)
        tw(f"#{k}b", "{rotationY:90, z:-600, opacity:0}", "{rotationY:-18, z:0, opacity:1, duration:0.6, ease:'power3.out'}", s0 + 0.15)
        for j in range(7):
            t = s0 + 0.9 + j * 0.62
            tw(f"#{k}pk{j}", f"{{x:0, y:0, opacity:0, scale:0.5}}", f"{{x:{bx - ax}, y:{by - ay}, opacity:1, scale:1, duration:0.9, ease:'power1.inOut'}}", t)
            T.append(f'tl.to("#{k}pk{j}", {{opacity:0, duration:0.15}}, {r3(t + 0.9)});')
        tp = word_t("port", s0, s1, s0 + 3.4)
        tw(f"#{k}lk", "{scale:0, rotation:-20}", "{scale:1, rotation:-6, duration:0.35, ease:'back.out(2.4)'}", tp)
        sfx("impact-punch", tp + 0.1, 0.4)
        T.append(f'tl.to("#{k}g", {{opacity:0, duration:0.3}}, {r3(s1 - 0.3)});')
        win(f"#{k}g", s0, s1)
        headline(k, fx["title"], s0, s1, top=(HY if WIDE else 1240))
        sub(k, fx["sub"], word_t("server", s0, s1, s0 + 4.0), s1, top_off=(220 if WIDE else 270))
        continue
    if kind == "connected":
        HT.append(f'<div id="{k}ring" class="ring" style="left:{W / 2 - 160}px;top:{H / 2 - 160}px;"></div>'
                  f'<div id="{k}big" class="bigok" style="top:{H / 2 - 80}px;">Connected</div>')
        tw(f"#{k}big", "{scale:0.2, opacity:0, rotationX:-70}", "{scale:1, opacity:1, rotationX:0, duration:0.35, ease:'back.out(2.2)'}", s0)
        tw(f"#{k}ring", "{scale:0.3, opacity:0.9}", "{scale:6, opacity:0, duration:0.9, ease:'power2.out'}", s0 + 0.05)
        sfx("impact-boom", s0 + 0.1, 0.5)
        sfx("confirm-1", s0 + 0.15, 0.4)
        win(f"#{k}ring", s0, s1)
        win(f"#{k}big", s0, s1)
        screen(k, i, s)
        continue
    if kind == "end":
        cy = H * (0.3 if WIDE else 0.32)
        stage.append(f'<div class="grp" id="{k}g">{cube(k + "cube", 200 if WIDE else 230, W / 2, cy)}</div>')
        tw(f"#{k}cube", "{rotationY:-180, z:-1400, opacity:0}", "{rotationY:30, rotationX:-18, z:0, opacity:1, duration:0.9, ease:'power3.out'}", s0)
        T.append(f'tl.to("#{k}cube", {{rotationY:"+=200", duration:{s1 - s0 - 0.9:.2f}, ease:"none"}}, {r3(s0 + 0.9)});')
        win(f"#{k}g", s0, TOTAL + 1)
        y0 = int(H * (0.5 if WIDE else 0.5))
        url = C["brand"]["url"]
        letters = "".join(f'<span class="ul" id="{k}u{j}">{E(ch)}</span>' for j, ch in enumerate(url))
        HT.append(f'''<div class="endbox" id="{k}e" style="top:{y0}px;">
  <div class="endname">copper_work</div>
  <div class="endline">{E(fx["line"])}</div>
  <div style="margin-top:38px;"><span class="cta" id="{k}cta">{E(fx["cta"])}</span></div>
  <div class="url">{letters}</div></div>''')
        tw(f"#{k}e", "{y:60, opacity:0}", "{y:0, opacity:1, duration:0.5, ease:'power3.out'}", s0 + 0.3)
        tw(f"#{k}cta", "{scale:0.3, opacity:0}", "{scale:1, opacity:1, duration:0.4, ease:'back.out(2.4)'}", s0 + 0.7)
        T.append(f'tl.to("#{k}cta", {{scale:1.06, duration:0.45, yoyo:true, repeat:5, ease:"sine.inOut"}}, {r3(s0 + 1.2)});')
        tu = word_t("plugin", s0, s1, s0 + 1.5)
        PRE.append(f'gsap.set("#{k}e .ul", {{opacity:0}});')
        T.append(f'tl.to("#{k}e .ul", {{opacity:1, duration:0.01, stagger:{1.3 / max(1, len(url)):.3f}}}, {r3(tu)});')
        sfx("typing-keyboard-fast", tu, 0.35)
        sfx("sparkle", s0 + 0.6, 0.3)
        win(f"#{k}e", s0, TOTAL + 1)
        continue
    # --- screen-based scenes
    extra = ""
    origin = fx.get("origin", "50% 50%")
    screen(k, i, s, origin=origin)
    if kind == "push":   # camera pushes into a region of the screen on a spoken word
        tpz = word_t(fx["word"], s0, s1, s0 + 2.0)
        T.append(f'tl.to("#{k}p", {{scale:{fx.get("scale", 1.7)}, x:{fx.get("push_x", 160 if WIDE else 0)}, rotationY:0, rotationX:0, duration:0.7, ease:"power3.inOut"}}, {r3(tpz - 0.2)});')
        sfx("whoosh-up-0.6s", tpz, 0.3)
    if kind == "tiles":
        n = len(fx["tiles"])
        for j, (lab, val) in enumerate(fx["tiles"]):
            tid = f"{k}t{j}"
            if WIDE:
                x, y = PX - 520 + j * 270, PY + PH / 2 - 40
            else:
                x, y = 70 + (j % 2) * 480, 170 + (j // 2) * 190
            HT.append(f'<div class="tile" id="{tid}" style="left:{x:.0f}px;top:{y:.0f}px;"><div class="tl">{E(lab)}</div><div class="tv">{E(val)}</div></div>')
            t = word_t(fx["words"][j], s0, s1, s0 + 0.6 + j * 0.45) if j < len(fx["words"]) else s0 + 0.6 + j * 0.45
            tw(f"#{tid}", "{z:-500, rotationX:70, opacity:0, y:-80}", "{z:0, rotationX:0, opacity:1, y:0, duration:0.45, ease:'back.out(1.8)'}", t - 0.1)
            sfx(["pop-high", "pop-low", "plop"][j % 3], t, 0.3)
            win(f"#{tid}", t - 0.15, s1)
    if kind == "toasts":
        for j, txt in enumerate(fx["toasts"]):
            tid = f"{k}n{j}"
            x = (PX - 120) if WIDE else 90
            y = (150 + j * 130) if WIDE else (130 + j * 140)
            HT.append(f'<div class="toast" id="{tid}" style="left:{x}px;top:{y}px;"><span class="bell"></span>{E(txt)}</div>')
            t = word_t(fx["words"][j], s0, s1, s0 + 0.8 + j * 0.8)
            tw(f"#{tid}", "{y:-200, rotationX:80, opacity:0}", "{y:0, rotationX:0, opacity:1, duration:0.45, ease:'back.out(1.6)'}", t - 0.1)
            sfx("alert" if j == 0 else "pop-high", t, 0.35)
            win(f"#{tid}", t - 0.15, s1)
    if kind == "shutter":
        HT.append(f'<div class="brk" id="{k}bk" style="left:{PX - PW / 2 + 60:.0f}px;top:{PY - PH / 2 + 60:.0f}px;width:{PW - 120}px;height:{PH - 120}px;">'
                  '<i class="c1"></i><i class="c2"></i><i class="c3"></i><i class="c4"></i></div><div class="flash" id="' + k + 'fl"></div>')
        tb = s0 + 0.7
        tw(f"#{k}bk", "{scale:1.3, opacity:0}", "{scale:1, opacity:1, duration:0.4, ease:'power3.out'}", tb)
        tf = word_t(fx["word"], s0, s1, s0 + 3.0)
        tw(f"#{k}fl", "{opacity:0.95}", "{opacity:0, duration:0.45, ease:'power2.out'}", tf)
        sfx("camera-shutter-1", tf, 0.5)
        win(f"#{k}bk", tb, s1)
        win(f"#{k}fl", tf - 0.02, tf + 0.5)
    if kind == "orbit":
        names = fx["names"]
        R = 380 if WIDE else 330
        cx, cy = (PX - 90, PY + 60) if WIDE else (W / 2, PY + 120)
        chips = "".join(f'<div class="och" style="transform:rotateY({j * 360 / len(names):.1f}deg) translateZ({R}px);">{E(nm)}</div>' for j, nm in enumerate(names))
        HT.append(f'<div class="orbwrap" id="{k}ow" style="left:{cx:.0f}px;top:{cy:.0f}px;"><div class="orb" id="{k}orb">{chips}</div></div>'
                  f'<div class="count" id="{k}cnt" style="left:{cx - 200:.0f}px;top:{cy - 130:.0f}px;">0</div>')
        tc = word_t("17", s0, s1, s0 + 1.6)
        tw(f"#{k}ow", "{opacity:0, scale:0.4}", "{opacity:1, scale:1, duration:0.5, ease:'back.out(1.6)'}", tc - 0.4)
        T.append(f'tl.fromTo("#{k}orb", {{rotationY:0}}, {{rotationY:-300, duration:{s1 - tc + 0.4:.2f}, ease:"none"}}, {r3(tc - 0.4)});')
        T.append(f'tl.fromTo("#{k}cnt", {{innerText:0}}, {{innerText:{fx["count"]}, snap:{{innerText:1}}, duration:0.8, ease:"power2.out"}}, {r3(tc - 0.6)});')
        tw(f"#{k}cnt", "{scale:0.3, opacity:0}", "{scale:1, opacity:1, duration:0.4, ease:'back.out(2)'}", tc - 0.6)
        T.append(f'tl.to("#{k}ow", {{opacity:0, duration:0.3}}, {r3(fx.get("orbit_end", s1) - 0.3)});')
        T.append(f'tl.to("#{k}cnt", {{opacity:0, duration:0.3}}, {r3(fx.get("orbit_end", s1) - 0.3)});')
        sfx("countdown-beeps", tc - 0.5, 0.18)
        sfx("impact-punch", tc + 0.2, 0.35)
        win(f"#{k}ow", tc - 0.45, fx.get("orbit_end", s1))
        win(f"#{k}cnt", tc - 0.65, fx.get("orbit_end", s1))
    if kind == "glitch":
        tg = word_t(fx["word"], s0, s1, s0 + 1.2)
        HT.append(f'<div class="glr" id="{k}r"></div><div class="glb" id="{k}b"></div>'
                  f'<div class="confirm" id="{k}cf" style="left:{(PX - 190) if WIDE else W / 2 - 190:.0f}px;top:{(PY + PH / 2 - 60) if WIDE else PY + PH / 2 - 90:.0f}px;">Confirm</div>')
        T.append(f'tl.to("#{k}p", {{x:-18, duration:0.05, yoyo:true, repeat:6, ease:"none"}}, {r3(tg - 0.6)});')
        tw(f"#{k}r", "{opacity:0.0, x:0}", "{opacity:0.55, x:24, duration:0.06, yoyo:true, repeat:6}", tg - 0.6)
        tw(f"#{k}b", "{opacity:0.0, x:0}", "{opacity:0.45, x:-24, duration:0.06, yoyo:true, repeat:6}", tg - 0.6)
        sfx("glitch-short", tg - 0.6, 0.35)
        tw(f"#{k}cf", "{scale:0, opacity:0}", "{scale:1, opacity:1, duration:0.35, ease:'back.out(2.4)'}", tg)
        T.append(f'tl.to("#{k}cf", {{scale:1.08, duration:0.35, yoyo:true, repeat:3, ease:"sine.inOut"}}, {r3(tg + 0.35)});')
        T.append(f'tl.to("#{k}cf", {{scale:0.9, backgroundColor:"{OK}", duration:0.12, yoyo:true, repeat:1}}, {r3(tg + 1.8)});')
        sfx("mouse-click", tg + 1.8, 0.5)
        sfx("confirm-1", tg + 1.9, 0.35)
        win(f"#{k}r", tg - 0.65, tg)
        win(f"#{k}b", tg - 0.65, tg)
        win(f"#{k}cf", tg - 0.05, s1)
    if kind == "stack":
        for j, (lab, wd) in enumerate(fx["chips"]):
            cid = f"{k}c{j}"
            if WIDE:
                x, y = PX + PW / 2 - 360, 170 + j * 120
            else:
                x, y = 90 + (j % 2) * 470, 120 + (j // 2) * 130
            HT.append(f'<div class="stk" id="{cid}" style="left:{x:.0f}px;top:{y:.0f}px;">{E(lab)}</div>')
            t = word_t(wd, s0, s1, s0 + 0.7 + j * 0.9)
            tw(f"#{cid}", "{x:600, rotationY:-80, opacity:0}", "{x:0, rotationY:0, opacity:1, duration:0.45, ease:'back.out(1.5)'}", t - 0.1)
            sfx(["pop-high", "pop-low", "plop"][j % 3], t, 0.3)
            win(f"#{cid}", t - 0.15, s1)
    if kind == "steps":
        for j, (num, lab, wd) in enumerate(fx["steps"]):
            cid = f"{k}st{j}"
            if WIDE:
                x, y, rz = 560 + j * 420, 300, (-8, 0, 8)[j]
            else:
                x, y, rz = 90, 260 + j * 330, (-4, 0, 4)[j]
            HT.append(f'<div class="step" id="{cid}" style="left:{x}px;top:{y}px;"><div class="sn">{num}</div><div class="sl">{E(lab)}</div></div>')
            t = word_t(wd, s0, s1, s0 + 1.5 + j * 1.6)
            tw(f"#{cid}", "{z:-900, rotationY:-120, opacity:0}", f"{{z:0, rotationY:0, rotationZ:{rz}, opacity:1, duration:0.55, ease:'back.out(1.4)'}}", t - 0.15)
            sfx("impact-punch", t, 0.3)
            win(f"#{cid}", t - 0.2, s1)
    if kind == "chips":
        for j, (lab, wd) in enumerate(fx["chips"]):
            cid = f"{k}ch{j}"
            if WIDE:
                x, y = 110 + j * 0, 560 + j * 92
            else:
                x, y = 40 + j * 250, 1690
            HT.append(f'<div class="chipx" id="{cid}" style="left:{x}px;top:{y}px;">{E(lab)}</div>')
            t = word_t(wd, s0, s1, s0 + 0.6 + j * 0.5)
            tw(f"#{cid}", "{scale:0.3, opacity:0, rotationX:-80}", "{scale:1, opacity:1, rotationX:0, duration:0.35, ease:'back.out(2)'}", t - 0.1)
            sfx(["pop-high", "pop-low", "plop"][j % 3], t, 0.3)
            win(f"#{cid}", t - 0.15, s1)
    if fx.get("title"):
        keys = {kk.lower(): word_t(v, s0, s1, s0 + 0.3) for kk, v in fx.get("keys", {}).items()}
        headline(k, fx["title"], s0, s1, keys=keys)
    if fx.get("sub"):
        sub(k, fx["sub"], word_t(fx.get("sub_word", "~"), s0, s1, s0 + 1.2), s1)

HT.insert(1, '<div id="stage">' + "\n".join(stage) + "</div>")
HT.extend(SWEEPS)

CSS = f"""
@font-face {{ font-family: "S"; src: url("assets/fonts/sans.woff2"); font-weight: 100 900; }}
@font-face {{ font-family: "M"; src: url("assets/fonts/mono.woff2"); font-weight: 100 900; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:#0a0a0a; }}
#root {{ position:absolute; inset:0; overflow:hidden; font-family:S; color:{TXT}; }}
.pt {{ position:absolute; background:{ACC}; border-radius:2px; }}
#stage {{ position:absolute; inset:0; perspective:1700px; perspective-origin:50% 45%; transform-style:preserve-3d; }}
.grp {{ position:absolute; inset:0; transform-style:preserve-3d; }}
.plane {{ position:absolute; border-radius:22px; overflow:hidden; background:#111; border:2px solid rgba(201,163,90,0.55);
          box-shadow:0 0 0 1px rgba(255,255,255,0.06), 0 40px 120px rgba(0,0,0,0.75), 0 0 80px rgba(201,163,90,0.18); }}
.glare {{ position:absolute; top:-20%; left:0; width:28%; height:140%; transform:rotate(18deg);
          background:linear-gradient(90deg, rgba(255,255,255,0), rgba(255,240,210,0.16), rgba(255,255,255,0)); }}
.hbox {{ position:absolute; perspective:900px; }}
.hl {{ font-weight:800; line-height:1.02; letter-spacing:-3px; color:{TXT}; text-shadow:0 10px 40px rgba(0,0,0,0.8); }}
.w {{ display:inline-block; transform-origin:50% 100%; }}
.sub {{ position:absolute; font-size:{36 if WIDE else 40}px; color:{MUT}; line-height:1.3; }}
.hookl {{ position:absolute; left:0; right:0; text-align:center; font-weight:800; letter-spacing:-4px; color:{TXT}; transform-origin:50% 100%;
          text-shadow:0 14px 50px rgba(0,0,0,0.85); }}
.cube {{ position:absolute; transform-style:preserve-3d; }}
.face {{ position:absolute; left:0; top:0; border-radius:18px; background:linear-gradient(145deg, #e4c37e, {ACC} 55%, #8e6d20);
         border:2px solid rgba(255,255,255,0.25); backface-visibility:hidden; }}
.core {{ position:absolute; border-radius:10px; background:#0d0d0f; box-shadow:inset 0 0 18px rgba(0,0,0,0.9); }}
.fcard {{ position:absolute; border-radius:24px; background:#1f1f1f; border:2px solid rgba(201,163,90,0.5); display:flex; flex-direction:column;
          align-items:center; justify-content:center; gap:26px; box-shadow:0 30px 90px rgba(0,0,0,0.7); }}
.ftitle {{ font-weight:700; font-size:40px; }}
.pk {{ position:absolute; width:22px; height:22px; margin:-11px 0 0 -11px; border-radius:6px; background:{OK}; box-shadow:0 0 22px {OK}; }}
.lock {{ position:absolute; font-family:M; font-weight:700; font-size:34px; color:#ff6b5b; border:4px solid #ff6b5b; border-radius:12px;
         padding:6px 22px; background:rgba(10,10,10,0.85); }}
.ring {{ position:absolute; width:320px; height:320px; border-radius:50%; border:10px solid {OK}; }}
.bigok {{ position:absolute; left:0; right:0; text-align:center; font-weight:800; font-size:{170 if WIDE else 150}px; letter-spacing:-6px; color:{OK};
          text-shadow:0 0 60px rgba(79,209,161,0.6), 0 10px 40px rgba(0,0,0,0.9); z-index:5; }}
.tile {{ position:absolute; width:240px; padding:20px 24px; border-radius:18px; background:rgba(31,31,31,0.96); border:2px solid rgba(201,163,90,0.6);
         box-shadow:0 30px 70px rgba(0,0,0,0.7); }}
.tl {{ font-family:M; font-size:26px; color:{MUT}; }}
.tv {{ font-weight:800; font-size:54px; letter-spacing:-2px; white-space:nowrap; }}
.toast {{ position:absolute; display:flex; align-items:center; gap:18px; font-weight:700; font-size:{38 if WIDE else 40}px; padding:20px 30px; border-radius:18px;
          background:#262321; border:2px solid {ACC}; box-shadow:0 26px 70px rgba(0,0,0,0.75); white-space:nowrap; }}
.bell {{ width:26px; height:26px; border-radius:50%; background:#ff6b5b; box-shadow:0 0 18px #ff6b5b; }}
.brk {{ position:absolute; }}
.brk i {{ position:absolute; width:90px; height:90px; border-color:#fff; border-style:solid; }}
.brk .c1 {{ left:0; top:0; border-width:8px 0 0 8px; }} .brk .c2 {{ right:0; top:0; border-width:8px 8px 0 0; }}
.brk .c3 {{ left:0; bottom:0; border-width:0 0 8px 8px; }} .brk .c4 {{ right:0; bottom:0; border-width:0 8px 8px 0; }}
.flash {{ position:absolute; inset:0; background:#fff; }}
.orbwrap {{ position:absolute; width:0; height:0; perspective:1400px; transform-style:preserve-3d; }}
.orb {{ position:absolute; left:0; top:0; transform-style:preserve-3d; transform:rotateX(-12deg); }}
.och {{ position:absolute; left:-110px; top:-30px; width:220px; text-align:center; font-family:M; font-weight:700; font-size:28px; padding:12px 0;
        border-radius:14px; background:rgba(31,31,31,0.95); border:2px solid rgba(201,163,90,0.7); backface-visibility:hidden; }}
.count {{ position:absolute; width:400px; text-align:center; font-weight:800; font-size:230px; letter-spacing:-10px; color:{ACC};
          text-shadow:0 0 60px rgba(201,163,90,0.45), 0 10px 40px rgba(0,0,0,0.9); }}
.glr, .glb {{ position:absolute; inset:0; mix-blend-mode:screen; }}
.glr {{ background:rgba(255,40,40,0.35); }} .glb {{ background:rgba(40,120,255,0.3); }}
.confirm {{ position:absolute; width:380px; text-align:center; font-weight:800; font-size:56px; color:#141414; background:{ACC}; border-radius:18px;
            padding:18px 0; box-shadow:0 0 50px rgba(201,163,90,0.5), 0 24px 60px rgba(0,0,0,0.7); }}
.stk {{ position:absolute; font-weight:700; font-size:{44 if WIDE else 42}px; padding:18px 34px; border-radius:18px; background:#262321;
        border:2px solid rgba(201,163,90,0.7); box-shadow:0 26px 60px rgba(0,0,0,0.7); white-space:nowrap; }}
.step {{ position:absolute; width:{380 if WIDE else 900}px; padding:30px 34px; border-radius:24px; background:#1f1f1f; border:2px solid {ACC};
         box-shadow:0 34px 90px rgba(0,0,0,0.8); display:flex; {'flex-direction:column;' if WIDE else 'align-items:center;'} gap:20px; }}
.sn {{ width:96px; height:96px; border-radius:20px; background:{ACC}; color:#141414; font-weight:800; font-size:64px; display:flex;
       align-items:center; justify-content:center; flex:none; }}
.sl {{ font-family:M; font-weight:700; font-size:{40 if WIDE else 44}px; line-height:1.25; }}
.chipx {{ position:absolute; font-weight:700; font-size:{40 if WIDE else 38}px; padding:14px 28px; border-radius:14px; background:#262321;
          border:2px solid rgba(201,163,90,0.7); white-space:nowrap; box-shadow:0 20px 50px rgba(0,0,0,0.6); }}
.sweep {{ position:absolute; top:-10%; left:0; width:{W * 0.35:.0f}px; height:120%; transform:skewX(-18deg);
          background:linear-gradient(90deg, rgba(201,163,90,0), rgba(242,217,155,0.55), rgba(201,163,90,0)); z-index:20; }}
.endbox {{ position:absolute; left:0; right:0; text-align:center; }}
.endname {{ font-weight:800; font-size:{130 if WIDE else 130}px; letter-spacing:-5px; }}
.endline {{ font-size:{44 if WIDE else 46}px; color:{MUT}; margin-top:6px; }}
.cta {{ display:inline-block; font-weight:800; font-size:{56 if WIDE else 58}px; color:#141414; background:{ACC}; padding:20px 50px; border-radius:18px;
        box-shadow:0 0 60px rgba(201,163,90,0.45); }}
.url {{ font-family:M; font-weight:600; font-size:{52 if WIDE else 50}px; margin-top:34px; }}
"""

# ---------------------------------------------------------------- audio
SFXDIR = "assets/sfx"
A = [("mix", "assets/audio/mix.wav", 0, min(dur("assets/audio/mix.wav"), TOTAL), 1.0)]
clicks = json.load(open("timing.json"))["clicks"]
CK = ["mouse-click", "click-1", "click-2"]
A += [(f"ck{n}", f"{SFXDIR}/{CK[n % 3]}.mp3", t, None, 0.45) for n, t in enumerate(clicks)]
A += [(f"fx{n}", f"{SFXDIR}/{nm}.mp3", t, None, v) for n, (nm, t, v) in enumerate(SFX)]
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
print(f"v2 built {a.format}: {len(T)} tweens, {len(aud)} audio clips, {len(SC)} scenes")
