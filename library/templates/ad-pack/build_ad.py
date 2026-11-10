# Ad pack builder: many short ads for one product, every ad with a different editing style. First used for
# AI Video Automator (app.talkember.site), 2026-11-10: owner asked for 20 ads on different topics, "her ek video me alag
# alag editing skill", 15 Hinglish + 5 English.
#   python3 build_ad.py SPEC.json --out PROJECT [--format 9x16|16x9]
# SPEC: id, style (key of STYLES), music (path under library/music), vo (finished voice file), lines [{say, h, hi
#   [accent words], sub, vis {type: phone|chips|big|icons|steps, ...}, end {cta, url2, icons}}].
# Timing comes from the voice: line boundaries = silences in the VO nearest to each line's share of the characters
# (ffmpeg silencedetect), so no hand timing. Music: music_fit.py + mix_vo_music.py (music-for-video skill).
# A style = background + palette + fonts + headline animation + scene move + cut overlay + picture frame + layout,
# so two ads never share a look. Text on screen is the spec's own (site facts); client strings are HTML-escaped.
# PROJECT needs assets/vendor/gsap, assets/fonts/*, assets/img/* (screens, logo.svg, icons/*.svg), assets/sfx/*.
import argparse, html, json, os, random, re, subprocess

ap = argparse.ArgumentParser()
ap.add_argument("spec")
ap.add_argument("--out", required=True)
ap.add_argument("--format", choices=["9x16", "16x9"], default="9x16")
a = ap.parse_args()
SP = json.load(open(a.spec))
REPO = os.environ.get("REPO", "/home/user/new-startup")
os.chdir(a.out)
WIDE = a.format == "16x9"
W, H = (1920, 1080) if WIDE else (1080, 1920)
E = lambda t: html.escape(str(t))
r3 = lambda x: round(x, 3)

# name: bg, pal (bg1, bg2, text, accent, accent2, card, cardtext), fonts (head, body), anim, move, over, frame, layout, caps, size
STYLES = {
    "s01": dict(bg="mesh", pal=["#eef2ff", "#c7d2fe", "#0f172a", "#4f46e5", "#7c3aed", "#ffffff", "#0f172a"], fonts=["PlusJakartaSans-Variable.ttf", "PlusJakartaSans-Variable.ttf"], anim="rise", move="push", over="none", frame="phone", layout="top", caps=False, size=104),
    "s02": dict(bg="grid", pal=["#07070c", "#141428", "#f5f5ff", "#22d3ee", "#a78bfa", "#12122a", "#f5f5ff"], fonts=["SpaceGrotesk-Variable.ttf", "JetBrainsMono-Variable.ttf"], anim="glitch", move="cut", over="glitch", frame="neon", layout="bottom", caps=True, size=100),
    "s03": dict(bg="paper", pal=["#f4efe4", "#e6dcc8", "#1c1a17", "#d9480f", "#1c1a17", "#fffdf7", "#1c1a17"], fonts=["Anton-Regular.ttf", "Poppins-SemiBold.ttf"], anim="slam", move="drop", over="none", frame="polaroid", layout="top", caps=True, size=128),
    "s04": dict(bg="sunburst", pal=["#ffd60a", "#ffc300", "#14110f", "#e5383b", "#14110f", "#ffffff", "#14110f"], fonts=["Bangers-Regular.ttf", "Poppins-Bold.ttf"], anim="pop", move="spin", over="flash", frame="sticker", layout="top", caps=True, size=132),
    "s05": dict(bg="blueprint", pal=["#0b3d91", "#0a2f70", "#eaf2ff", "#ffd166", "#8ecae6", "#0f4bb0", "#eaf2ff"], fonts=["JetBrainsMono-Variable.ttf", "JetBrainsMono-Variable.ttf"], anim="type", move="fade", over="bar", frame="browser", layout="bottom", caps=False, size=84),
    "s06": dict(bg="stripes", pal=["#ff5d8f", "#ff87ab", "#1b1b1e", "#ffffff", "#ffe066", "#ffffff", "#1b1b1e"], fonts=["LuckiestGuy-Regular.ttf", "Poppins-Bold.ttf"], anim="drop", move="slide", over="none", frame="card", layout="top", caps=True, size=110),
    "s07": dict(bg="dots", pal=["#fffbf0", "#fff1cc", "#1d3557", "#e63946", "#457b9d", "#ffffff", "#1d3557"], fonts=["Montserrat-Variable.ttf", "Montserrat-Variable.ttf"], anim="marker", move="push", over="none", frame="card", layout="center", caps=False, size=96),
    "s08": dict(bg="neon", pal=["#0a0014", "#1a0033", "#ffffff", "#ff2e97", "#00f5d4", "#1b0b2e", "#ffffff"], fonts=["BebasNeue-Regular.ttf", "Poppins-SemiBold.ttf"], anim="flip", move="zoom", over="circle", frame="neon", layout="top", caps=True, size=150),
    "s09": dict(bg="terminal", pal=["#06120a", "#0a1f10", "#b7f5c5", "#39ff14", "#f5f749", "#0c2413", "#b7f5c5"], fonts=["JetBrainsMono-Variable.ttf", "JetBrainsMono-Variable.ttf"], anim="type", move="cut", over="stripes", frame="flat", layout="top", caps=False, size=78),
    "s10": dict(bg="split", pal=["#111111", "#2b2b2b", "#f2f2f2", "#ff4d00", "#111111", "#ffffff", "#111111"], fonts=["Anton-Regular.ttf", "Manrope-Variable.ttf"], anim="wipe", move="slide", over="diag", frame="flat", layout="bottom", caps=True, size=124),
    "s11": dict(bg="waves", pal=["#e0fbfc", "#98c1d9", "#293241", "#ee6c4d", "#3d5a80", "#ffffff", "#293241"], fonts=["Manrope-Variable.ttf", "Manrope-Variable.ttf"], anim="zoom", move="blur", over="none", frame="round", layout="top", caps=False, size=100),
    "s12": dict(bg="notebook", pal=["#fdfcf5", "#f1eed9", "#22223b", "#2a6f97", "#c9184a", "#fffef2", "#22223b"], fonts=["Kalam-Bold.ttf", "Kalam-Bold.ttf"], anim="marker", move="turn", over="none", frame="polaroid", layout="top", caps=False, size=104),
    "s13": dict(bg="shapes", pal=["#fff8e7", "#ffe8b3", "#1a1423", "#7b2cbf", "#ff9e00", "#ffffff", "#1a1423"], fonts=["Poppins-ExtraBold.ttf", "Poppins-SemiBold.ttf"], anim="spin", move="push", over="circle", frame="sticker", layout="bottom", caps=False, size=100),
    "s14": dict(bg="gradient", pal=["#0f2027", "#2c5364", "#f8f9fa", "#f4d35e", "#ee964b", "#12303c", "#f8f9fa"], fonts=["PlayfairDisplay-Italic.ttf", "Manrope-Variable.ttf"], anim="rise", move="fade", over="none", frame="tilt", layout="top", caps=False, size=104),
    "s15": dict(bg="halftone", pal=["#0068a8", "#023e8a", "#ffffff", "#ffea00", "#03045e", "#ffffff", "#03045e"], fonts=["Bangers-Regular.ttf", "Poppins-Bold.ttf"], anim="slam", move="spin", over="flash", frame="sticker", layout="top", caps=True, size=128),
    "s16": dict(bg="mono", pal=["#ffffff", "#f1f1f1", "#0a0a0a", "#0a0a0a", "#8d8d8d", "#0a0a0a", "#ffffff"], fonts=["TikTokSans-Variable.ttf", "TikTokSans-Variable.ttf"], anim="wipe", move="cut", over="bar", frame="flat", layout="center", caps=False, size=120),
    "s17": dict(bg="aurora", pal=["#020617", "#0f172a", "#e2e8f0", "#34d399", "#60a5fa", "#0b1220", "#e2e8f0"], fonts=["SpaceGrotesk-Variable.ttf", "SpaceGrotesk-Variable.ttf"], anim="zoom", move="zoom", over="none", frame="phone", layout="bottom", caps=False, size=100),
    "s18": dict(bg="steps", pal=["#f7f7ff", "#e4e4ff", "#14142b", "#5f2eea", "#00ba88", "#ffffff", "#14142b"], fonts=["Ubuntu-Bold.ttf", "Ubuntu-Regular.ttf"], anim="slide", move="slide", over="none", frame="browser", layout="top", caps=False, size=100),
    "s19": dict(bg="news", pal=["#f3f0e8", "#e7e2d3", "#111111", "#b00020", "#111111", "#fffdf8", "#111111"], fonts=["NotoSerif-Variable.ttf", "NotoSerif-Variable.ttf"], anim="rise", move="turn", over="none", frame="polaroid", layout="center", caps=False, size=96),
    "s20": dict(bg="pricetag", pal=["#0b6e4f", "#08a045", "#ffffff", "#ffe45e", "#073b3a", "#ffffff", "#073b3a"], fonts=["Montserrat-Variable.ttf", "Montserrat-Variable.ttf"], anim="pop", move="drop", over="flash", frame="card", layout="top", caps=True, size=110),
}
ST = STYLES[SP["style"]]
BG1, BG2, TX, AC, AC2, CARD, CTX = ST["pal"]
random.seed(int(re.sub(r"\D", "", SP["id"]) or 1))


def run(*x, **k):
    return subprocess.run(x, check=True, capture_output=True, text=True, **k)


def dur(p):
    return round(float(run("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p).stdout), 3)


# ---------------------------------------------------------------- voice -> line times
VO_AT = 0.25
os.makedirs("assets/audio", exist_ok=True)
run("ffmpeg", "-y", "-i", SP["vo"], "-ar", "48000", "-ac", "2", "-af", "loudnorm=I=-18:TP=-2", "assets/audio/vo.wav")
VD = dur("assets/audio/vo.wav")
err = subprocess.run(["ffmpeg", "-i", "assets/audio/vo.wav", "-af", "silencedetect=n=-36dB:d=0.14", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
ss = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", err)]
se = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", err)]
gaps = [(s, e) for s, e in zip(ss, se) if 0.3 < s < VD - 0.3]
LN = SP["lines"]
chars = [len(re.sub(r"\[[^\]]*\]", "", l["say"])) for l in LN]
tot = sum(chars)
starts, used = [0.0], set()
for i in range(1, len(LN)):
    est = VD * sum(chars[:i]) / tot
    cand = sorted(((abs((s + e) / 2 - est) - 0.6 * (e - s), k) for k, (s, e) in enumerate(gaps) if k not in used and (s + e) / 2 > starts[-1] + 0.8))
    if cand and cand[0][0] < 1.6:
        k = cand[0][1]
        used.add(k)
        starts.append(r3(gaps[k][1] - 0.08))
    else:
        starts.append(r3(est))
TOTAL = r3(VO_AT + VD + 1.7)
for i, l in enumerate(LN):
    l["t0"] = 0.0 if i == 0 else r3(VO_AT + starts[i] - 0.12)
    l["t1"] = r3(VO_AT + starts[i + 1] - 0.12) if i + 1 < len(LN) else TOTAL

PV, TL = "/home/user/tools/perc-venv/bin/python", f"{REPO}/library/tools"
run(PV, f"{TL}/music_fit.py", f"{REPO}/library/music/{SP['music']}", "assets/audio/music.wav", "--length", str(TOTAL), "--end", SP.get("music_end", "fade"), "--fade", "1.5",
    *(["--start", str(SP["music_start"])] if SP.get("music_start") else []))
run("ffmpeg", "-y", "-i", "assets/audio/vo.wav", "-af", f"adelay={int(VO_AT * 1000)}|{int(VO_AT * 1000)},apad=whole_dur={TOTAL}", "assets/audio/vo_placed.wav")
run(PV, f"{TL}/mix_vo_music.py", "assets/audio/vo_placed.wav", "assets/audio/music.wav", "assets/audio/mix.wav", "--lufs", "-16")

T, PRE, HT, SFX = [], [], [], []


def win(sel, s0, s1):
    if s0 > 0:
        PRE.append(f'gsap.set("{sel}", {{visibility:"hidden"}});')
        T.append(f'tl.set("{sel}", {{visibility:"visible"}}, {r3(s0)});')
    if s1 < TOTAL:
        T.append(f'tl.set("{sel}", {{visibility:"hidden"}}, {r3(s1)});')


def tw(sel, frm, to, at):
    T.append(f'tl.fromTo("{sel}", {frm}, {to}, {r3(max(0, at))});')


def to(sel, v, at):
    T.append(f'tl.to("{sel}", {v}, {r3(max(0, at))});')


def sfx(name, at, vol):
    SFX.append((name, r3(max(0, at)), vol))


# ---------------------------------------------------------------- backgrounds
def background():
    b = ST["bg"]
    base = f'<div id="bg" style="position:absolute;inset:0;background:linear-gradient(160deg, {BG1}, {BG2});"></div>'
    ex = ""
    if b in ("mesh", "aurora"):
        cols = [AC, AC2, AC] if b == "mesh" else [AC, AC2, "#a78bfa"]
        for k, c in enumerate(cols):
            x, y = [(-0.2, 0.55), (0.5, -0.15), (0.3, 0.8)][k]
            ex += f'<div class="blob" id="bl{k}" style="left:{W * x:.0f}px;top:{H * y:.0f}px;width:{W * 0.9:.0f}px;height:{W * 0.9:.0f}px;background:radial-gradient(circle, {c}{"66" if b == "mesh" else "55"}, {c}00 68%);"></div>'
            to(f"#bl{k}", f'{{x:{random.choice([-1, 1]) * W * 0.3:.0f}, y:{random.choice([-1, 1]) * H * 0.18:.0f}, duration:{TOTAL}, ease:"sine.inOut"}}', 0)
    elif b in ("grid", "blueprint"):
        col = "rgba(255,255,255,0.14)" if b == "blueprint" else f"{AC}33"
        if b == "grid":
            ex += (f'<div style="position:absolute;inset:0;perspective:800px;overflow:hidden;"><div id="gr" style="position:absolute;left:{W / 2 - 2000}px;top:{H * 0.62:.0f}px;width:4000px;height:3000px;'
                   f'transform:rotateX(74deg);transform-origin:50% 0;background-image:linear-gradient({col} 2px, transparent 2px), linear-gradient(90deg, {col} 2px, transparent 2px);background-size:120px 120px;"></div></div>')
            tw("#gr", '{backgroundPosition:"0px 0px"}', f'{{backgroundPosition:"0px {int(TOTAL * 70)}px", duration:{TOTAL}, ease:"none"}}', 0)
        else:
            ex += (f'<div id="gr" style="position:absolute;inset:-200px;background-image:linear-gradient({col} 2px, transparent 2px), linear-gradient(90deg, {col} 2px, transparent 2px), '
                   f'linear-gradient(rgba(255,255,255,0.06) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.06) 1px, transparent 1px);background-size:160px 160px,160px 160px,40px 40px,40px 40px;"></div>')
            tw("#gr", "{x:0, y:0}", f'{{x:-120, y:-120, duration:{TOTAL}, ease:"none"}}', 0)
    elif b in ("paper", "news", "notebook"):
        if b == "notebook":
            ex += f'<div style="position:absolute;inset:0;background-image:linear-gradient(transparent 94%, {AC}55 94%);background-size:100% 84px;"></div><div style="position:absolute;left:120px;top:0;bottom:0;width:4px;background:{AC2}88;"></div>'
        if b == "news":
            ex += f'<div style="position:absolute;left:60px;right:60px;top:150px;height:6px;background:{TX};"></div><div style="position:absolute;left:60px;right:60px;top:164px;height:2px;background:{TX};"></div>'
        d = "".join(f'<line x1="{random.uniform(0, W):.0f}" y1="{random.uniform(0, H):.0f}" x2="{random.uniform(0, W):.0f}" y2="{random.uniform(0, H):.0f}" stroke="{TX}" stroke-width="1" opacity="0.05"/>' for _ in range(26))
        ex += f'<svg id="dust" width="{W}" height="{H}" style="position:absolute;inset:0;">{d}</svg>'
        tw("#dust", "{x:0}", f'{{x:-40, y:30, duration:{TOTAL}, ease:"none"}}', 0)
    elif b == "sunburst":
        ex += f'<div id="sun" style="position:absolute;left:{W / 2 - 1600}px;top:{H / 2 - 1600}px;width:3200px;height:3200px;background:repeating-conic-gradient({BG2} 0deg 10deg, {BG1} 10deg 20deg);"></div>'
        tw("#sun", "{rotation:0}", f'{{rotation:{TOTAL * 6:.0f}, duration:{TOTAL}, ease:"none"}}', 0)
    elif b == "stripes":
        ex += f'<div id="str" style="position:absolute;inset:-400px;background:repeating-linear-gradient(45deg, {BG1} 0 70px, {BG2} 70px 140px);"></div>'
        tw("#str", "{x:0}", f'{{x:198, duration:{TOTAL}, ease:"none"}}', 0)
    elif b in ("dots", "halftone"):
        c = f"{AC2}55" if b == "dots" else "rgba(255,255,255,0.28)"
        sz = 46 if b == "dots" else 30
        ex += f'<div id="dt" style="position:absolute;inset:-200px;background-image:radial-gradient({c} {6 if b == "dots" else 8}px, transparent {7 if b == "dots" else 9}px);background-size:{sz}px {sz}px;"></div>'
        tw("#dt", "{x:0, y:0}", f'{{x:{sz * 3}, y:-{sz * 3}, duration:{TOTAL}, ease:"none"}}', 0)
    elif b == "neon":
        for k in range(3):
            s_ = 500 + k * 380
            ex += f'<div id="ng{k}" style="position:absolute;left:{W / 2 - s_ / 2}px;top:{H * 0.48 - s_ / 2:.0f}px;width:{s_}px;height:{s_}px;border-radius:50%;border:6px solid {[AC, AC2, AC][k]};box-shadow:0 0 60px {[AC, AC2, AC][k]};opacity:0.35;"></div>'
            to(f"#ng{k}", f'{{scale:1.12, opacity:0.6, duration:{0.9 + k * 0.2}, yoyo:true, repeat:{int(TOTAL / (0.9 + k * 0.2)) // 2 * 2 + 1}, ease:"sine.inOut"}}', 0)
    elif b == "terminal":
        ex += (f'<div style="position:absolute;inset:0;background:repeating-linear-gradient(0deg, rgba(0,0,0,0.25) 0 2px, transparent 2px 6px);"></div>'
               f'<div id="scan" style="position:absolute;left:0;right:0;top:0;height:180px;background:linear-gradient(180deg, transparent, {AC}22, transparent);"></div>')
        tw("#scan", "{y:-200}", f'{{y:{H + 200}, duration:3.2, repeat:{int(TOTAL / 3.2)}, ease:"none"}}', 0)
    elif b == "split":
        ex += f'<div id="spl" style="position:absolute;left:-600px;top:{H * 0.5:.0f}px;width:{W + 1200}px;height:{H}px;background:{BG2};border-top:10px solid {AC};transform:rotate(-12deg);transform-origin:50% 0;"></div>'
        tw("#spl", "{rotation:-12}", f'{{rotation:-6, y:-80, duration:{TOTAL}, ease:"sine.inOut"}}', 0)
    elif b == "waves":
        for k in range(3):
            ex += (f'<svg id="wv{k}" width="{W * 2}" height="420" viewBox="0 0 2160 420" style="position:absolute;left:0;bottom:{k * 110 - 40}px;opacity:{0.5 - k * 0.12};">'
                   f'<path d="M0 120 Q 270 0 540 120 T 1080 120 T 1620 120 T 2160 120 V420 H0Z" fill="{[AC2, BG2, AC][k]}"/></svg>')
            tw(f"#wv{k}", "{x:0}", f'{{x:-{W}, duration:{TOTAL * (0.6 + k * 0.25):.1f}, repeat:1, ease:"none"}}', 0)
    elif b == "shapes":
        for k in range(12):
            sz = random.choice([60, 90, 130])
            kind = k % 3
            st_ = f"border-radius:50%;background:{AC}33;" if kind == 0 else (f"background:{AC2}44;" if kind == 1 else f"border:8px solid {AC}55;")
            ex += f'<div id="sh{k}" style="position:absolute;left:{random.uniform(0, W - sz):.0f}px;top:{random.uniform(0, H - sz):.0f}px;width:{sz}px;height:{sz}px;{st_}"></div>'
            to(f"#sh{k}", f'{{y:{random.choice([-1, 1]) * random.uniform(120, 300):.0f}, rotation:{random.choice([-180, 180])}, duration:{TOTAL}, ease:"sine.inOut"}}', 0)
    elif b == "gradient":
        ex += f'<div id="gg" style="position:absolute;left:0;top:-{H}px;width:{W}px;height:{H * 3}px;background:linear-gradient(180deg, {BG1}, {BG2}, {AC2}55, {BG1});"></div>'
        tw("#gg", "{y:0}", f'{{y:{H}, duration:{TOTAL}, ease:"none"}}', 0)
    elif b == "mono":
        ex += f'<div id="mb" style="position:absolute;left:0;top:{H * 0.955:.0f}px;width:{W}px;height:14px;background:{TX};transform-origin:0 50%;"></div>'
        tw("#mb", "{scaleX:0}", f'{{scaleX:1, duration:{TOTAL}, ease:"none"}}', 0)
    elif b == "steps":
        for k in range(6):
            ex += f'<div id="sp{k}" style="position:absolute;left:{k * 190 - 60}px;top:{H - 200 - k * 150}px;width:260px;height:{200 + k * 150}px;background:{AC}{"1f" if k % 2 else "14"};border-radius:28px 28px 0 0;"></div>'
            tw(f"#sp{k}", "{scaleY:0, transformOrigin:'50% 100%'}", "{scaleY:1, duration:0.8, ease:'power3.out'}", 0.1 + k * 0.12)
    elif b == "pricetag":
        ex += f'<div id="pt" style="position:absolute;inset:-300px;background-image:repeating-linear-gradient(-45deg, rgba(255,255,255,0.07) 0 40px, transparent 40px 120px);"></div>'
        tw("#pt", "{x:0}", f'{{x:170, duration:{TOTAL}, ease:"none"}}', 0)
    HT.append(base + ex)


background()

# ---------------------------------------------------------------- layout
SAFE_T, SAFE_B = (150, 300) if not WIDE else (70, 110)
if WIDE:
    HX, HW_ = 110, 860
    HEAD_Y = {"top": 190, "bottom": 190, "center": 230}[ST["layout"]]
    VIS = dict(cx=1400, cy=540, w=700, h=780)
else:
    HX, HW_ = 70, W - 140
    HEAD_Y = {"top": 250, "bottom": 1150, "center": 520}[ST["layout"]]
    VIS = {"top": dict(cx=W / 2, cy=1150, w=600, h=860), "bottom": dict(cx=W / 2, cy=640, w=560, h=820), "center": dict(cx=W / 2, cy=1290, w=640, h=620)}[ST["layout"]]
FS = ST["size"] if not WIDE else int(ST["size"] * 0.8)
ALIGN = "left" if (WIDE or ST["bg"] in ("terminal", "blueprint", "news", "mono")) else "center"
MOVES_SFX = ["whoosh-fast-0.3s", "swish-1", "swish-4", "whoosh-up-0.6s"]
POPS = ["pop-high", "pop-low", "plop"]
ICONS = {"ChatGPT": "openai.svg", "Google Flow": "google.svg", "YouTube": "youtube.svg", "Gmail": "gmail.svg"}


def words_html(i, text, accents):
    out, n = [], 0
    acc = [x.lower() for x in accents]
    for wd in text.split(" "):
        key = re.sub(r"[^\w]", "", wd.lower())
        cls = "w ac" if key in acc else "w"
        if ST["anim"] == "type":
            inner = "".join(f'<span class="c">{E(ch)}</span>' for ch in wd)
            out.append(f'<span class="{cls}" id="L{i}w{n}">{inner}</span>')
        else:
            out.append(f'<span class="{cls}" id="L{i}w{n}">{E(wd)}</span>')
        n += 1
    return " ".join(out), n


def animate_words(i, n, t0, span):
    an = ST["anim"]
    step = min(0.16, max(0.07, (span * 0.55) / max(1, n)))
    for k in range(n):
        s, t = f"#L{i}w{k}", t0 + 0.1 + k * step
        if an == "rise":
            tw(s, "{y:70, opacity:0, filter:'blur(10px)'}", "{y:0, opacity:1, filter:'blur(0px)', duration:0.45, ease:'power3.out'}", t)
        elif an == "slam":
            tw(s, "{scale:2.6, opacity:0}", "{scale:1, opacity:1, duration:0.22, ease:'power4.in'}", t)
        elif an == "flip":
            tw(s, "{rotationX:-95, y:40, opacity:0}", "{rotationX:0, y:0, opacity:1, duration:0.5, ease:'back.out(1.8)'}", t)
        elif an == "slide":
            tw(s, f"{{x:{-500 if k % 2 == 0 else 500}, opacity:0}}", "{x:0, opacity:1, duration:0.45, ease:'power3.out'}", t)
        elif an == "wipe":
            tw(s, "{clipPath:'inset(0% 100% 0% 0%)'}", "{clipPath:'inset(0% 0% 0% 0%)', duration:0.4, ease:'power2.out'}", t)
        elif an == "drop":
            tw(s, "{y:-420, opacity:0}", "{y:0, opacity:1, duration:0.7, ease:'bounce.out'}", t)
        elif an == "spin":
            tw(s, f"{{rotation:{-40 if k % 2 == 0 else 40}, scale:0, opacity:0}}", "{rotation:0, scale:1, opacity:1, duration:0.5, ease:'back.out(2)'}", t)
        elif an == "pop":
            tw(s, "{scale:0, opacity:0}", "{scale:1, opacity:1, duration:0.4, ease:'back.out(3)'}", t)
        elif an == "glitch":
            tw(s, "{x:-40, opacity:0, skewX:30}", "{x:0, opacity:1, skewX:0, duration:0.16, ease:'steps(4)'}", t)
        elif an == "zoom":
            tw(s, "{scale:0.5, opacity:0, filter:'blur(14px)'}", "{scale:1, opacity:1, filter:'blur(0px)', duration:0.5, ease:'power3.out'}", t)
        elif an == "marker":
            tw(s, "{opacity:0, y:20}", "{opacity:1, y:0, duration:0.3}", t)
        elif an == "type":
            PRE.append(f'gsap.set("{s} .c", {{opacity:0}});')
            to(f"{s} .c", "{opacity:1, duration:0.01, stagger:0.035}", t0 + 0.1 + k * max(step, 0.22))
    if an == "marker":
        tw(f"#L{i}h .ac", "{backgroundSize:'0% 100%'}", "{backgroundSize:'100% 100%', duration:0.5, ease:'power2.out'}", t0 + 0.2 + n * step)
    if an == "type":
        sfx("typing-keyboard-fast", t0 + 0.1, 0.3)


def frame_html(fid, img, w, h):
    f = ST["frame"]
    im = f'<img src="assets/img/{img}" alt="AI Video Automator screen" style="width:100%;height:100%;object-fit:cover;object-position:top;display:block;">'
    if f == "phone":
        return f'<div id="{fid}" class="vis" style="width:{w}px;height:{h}px;border-radius:54px;background:#0d0d14;padding:16px;box-shadow:0 40px 90px rgba(0,0,0,0.45);"><div style="width:100%;height:100%;border-radius:40px;overflow:hidden;">{im}</div></div>'
    if f == "neon":
        return f'<div id="{fid}" class="vis" style="width:{w}px;height:{h}px;border-radius:30px;padding:6px;background:linear-gradient(135deg, {AC}, {AC2});box-shadow:0 0 70px {AC}99;"><div style="width:100%;height:100%;border-radius:26px;overflow:hidden;">{im}</div></div>'
    if f == "polaroid":
        return f'<div id="{fid}" class="vis" style="width:{w}px;height:{h}px;background:#fff;padding:22px 22px 90px;box-shadow:0 26px 60px rgba(0,0,0,0.35);"><div style="width:100%;height:100%;overflow:hidden;">{im}</div></div>'
    if f == "sticker":
        return f'<div id="{fid}" class="vis" style="width:{w}px;height:{h}px;border-radius:40px;border:12px solid #fff;box-shadow:14px 14px 0 {TX};overflow:hidden;background:#fff;">{im}</div>'
    if f == "browser":
        return (f'<div id="{fid}" class="vis" style="width:{w}px;height:{h}px;border-radius:22px;background:{CARD};box-shadow:0 30px 70px rgba(0,0,0,0.4);overflow:hidden;">'
                f'<div style="height:54px;background:rgba(0,0,0,0.25);display:flex;align-items:center;gap:10px;padding-left:20px;"><i style="width:16px;height:16px;border-radius:50%;background:#ff5f57;"></i><i style="width:16px;height:16px;border-radius:50%;background:#febc2e;"></i><i style="width:16px;height:16px;border-radius:50%;background:#28c840;"></i></div>'
                f'<div style="height:{h - 54}px;overflow:hidden;">{im}</div></div>')
    if f == "round":
        return f'<div id="{fid}" class="vis" style="width:{w}px;height:{h}px;border-radius:{w // 2}px {w // 2}px 60px 60px;overflow:hidden;box-shadow:0 30px 70px rgba(0,0,0,0.3);border:10px solid {CARD};">{im}</div>'
    if f == "tilt":
        return f'<div id="{fid}" class="vis" style="width:{w}px;height:{h}px;border-radius:28px;overflow:hidden;box-shadow:-30px 40px 80px rgba(0,0,0,0.5);border:2px solid {AC}88;">{im}</div>'
    if f == "card":
        return f'<div id="{fid}" class="vis" style="width:{w}px;height:{h}px;border-radius:36px;background:{CARD};padding:18px;box-shadow:0 24px 0 rgba(0,0,0,0.18);"><div style="width:100%;height:100%;border-radius:22px;overflow:hidden;">{im}</div></div>'
    return f'<div id="{fid}" class="vis" style="width:{w}px;height:{h}px;overflow:hidden;box-shadow:0 20px 50px rgba(0,0,0,0.35);border:4px solid {TX};">{im}</div>'


def visual(i, v, t0, t1):
    """returns html placed in the visual area; registers tweens"""
    cx, cy, w, h = VIS["cx"], VIS["cy"], VIS["w"], VIS["h"]
    typ = v.get("type", "none")
    tv = t0 + 0.35
    if typ == "phone":
        fid = f"L{i}v"
        rot = {"polaroid": -5, "sticker": 4, "tilt": 0, "card": -3}.get(ST["frame"], 0)
        html_ = f'<div style="position:absolute;left:{cx - w / 2:.0f}px;top:{cy - h / 2:.0f}px;width:{w}px;height:{h}px;perspective:1400px;">{frame_html(fid, v["img"], w, h)}</div>'
        ent = {"phone": "{y:700, rotationX:40, opacity:0}", "neon": "{scale:0.3, opacity:0}", "polaroid": "{y:-900, rotation:-30, opacity:0}", "sticker": "{scale:0, rotation:-25}",
               "browser": "{x:900, opacity:0}", "round": "{y:500, opacity:0, scale:0.8}", "tilt": "{rotationY:70, x:400, opacity:0}", "card": "{y:800, rotation:12, opacity:0}", "flat": "{clipPath:'inset(100% 0% 0% 0%)'}"}[ST["frame"]]
        fin = {"tilt": f"{{rotationY:-16, rotationX:6, x:0, opacity:1", "flat": "{clipPath:'inset(0% 0% 0% 0%)'", "phone": "{y:0, rotationX:6, opacity:1"}.get(ST["frame"], f"{{x:0, y:0, scale:1, rotation:{rot}, opacity:1")
        tw(f"#{fid}", ent, fin + ", duration:0.6, ease:'back.out(1.3)'}", tv)
        to(f"#{fid}", f'{{y:"-=22", duration:{max(0.5, t1 - tv - 1.0):.2f}, ease:"sine.inOut"}}', tv + 0.62)
        sfx(POPS[i % 3], tv + 0.2, 0.3)
        return html_
    if typ == "chips":
        items = v["items"]
        gap = min(130, (h - 40) / max(1, len(items)))
        y0 = cy - gap * (len(items) - 1) / 2 - 50
        out = ""
        for k, it in enumerate(items):
            cid = f"L{i}c{k}"
            ic = f'<img src="assets/img/icons/{ICONS[it]}" alt="{E(it)} icon" style="width:52px;height:52px;background:#fff;border-radius:12px;padding:7px;box-sizing:border-box;">' if it in ICONS else f'<span class="dot"></span>'
            out += f'<div style="position:absolute;left:0;width:{W}px;top:{y0 + k * gap:.0f}px;text-align:center;"><span class="chip" id="{cid}">{ic}{E(it)}</span></div>'
            t = tv + k * min(0.5, (t1 - tv - 0.8) / max(1, len(items)))
            tw(f"#{cid}", f"{{scale:0, opacity:0, x:{-200 if k % 2 == 0 else 200}}}", "{scale:1, opacity:1, x:0, duration:0.4, ease:'back.out(2)'}", t)
            sfx(POPS[k % 3], t + 0.05, 0.28)
        return out
    if typ == "big":
        bid = f"L{i}b"
        out = (f'<div style="position:absolute;left:0;width:{W}px;top:{cy - 230:.0f}px;text-align:center;"><div class="bignum" id="{bid}">{E(v["text"])}</div>'
               + (f'<div class="bigsub" id="{bid}s">{E(v["sub"])}</div>' if v.get("sub") else "") + "</div>")
        tw(f"#{bid}", "{scale:0.2, opacity:0, rotation:-8}", "{scale:1, opacity:1, rotation:0, duration:0.5, ease:'back.out(2.4)'}", tv)
        to(f"#{bid}", f'{{scale:1.05, duration:0.5, yoyo:true, repeat:{max(1, int((t1 - tv - 0.6) / 0.5) // 2 * 2 - 1)}, ease:"sine.inOut"}}', tv + 0.55)
        if v.get("sub"):
            tw(f"#{bid}s", "{opacity:0, y:30}", "{opacity:1, y:0, duration:0.4}", tv + 0.4)
        sfx("impact-punch", tv + 0.1, 0.4)
        return out
    if typ == "steps":
        items = v["items"]
        gap = min(170, (h - 20) / max(1, len(items)))
        y0 = cy - gap * (len(items) - 1) / 2 - 70
        out = ""
        for k, it in enumerate(items):
            sid = f"L{i}s{k}"
            out += f'<div class="step" id="{sid}" style="left:{(W - min(900, W - 140)) / 2:.0f}px;width:{min(900, W - 140)}px;top:{y0 + k * gap:.0f}px;"><span class="sn">{k + 1}</span><span>{E(it)}</span></div>'
            t = tv + k * min(0.7, (t1 - tv - 0.6) / max(1, len(items)))
            tw(f"#{sid}", "{x:-900, opacity:0}", "{x:0, opacity:1, duration:0.45, ease:'power3.out'}", t)
            sfx(POPS[k % 3], t + 0.1, 0.28)
        return out
    return ""


def overlay(i, t):
    o = ST["over"]
    oid = f"ov{i}"
    if o == "flash":
        HT.append(f'<div id="{oid}" style="position:absolute;inset:0;background:#fff;z-index:30;"></div>')
        tw(f"#{oid}", "{opacity:0.9}", "{opacity:0, duration:0.35, ease:'power2.out'}", t)
        win(f"#{oid}", t - 0.02, t + 0.4)
    elif o == "bar":
        HT.append(f'<div id="{oid}" style="position:absolute;left:0;top:0;width:{W}px;height:{H}px;background:{AC};z-index:30;"></div>')
        tw(f"#{oid}", f"{{x:{-W}}}", f"{{x:{W}, duration:0.55, ease:'power3.inOut'}}", t - 0.28)
        win(f"#{oid}", t - 0.3, t + 0.3)
    elif o == "circle":
        HT.append(f'<div id="{oid}" style="position:absolute;left:{W / 2 - 100}px;top:{H / 2 - 100}px;width:200px;height:200px;border-radius:50%;background:{AC};z-index:30;"></div>')
        tw(f"#{oid}", "{scale:0, opacity:1}", "{scale:14, opacity:0, duration:0.6, ease:'power2.out'}", t - 0.1)
        win(f"#{oid}", t - 0.12, t + 0.55)
    elif o == "stripes":
        bars = "".join(f'<div class="vb" style="top:{k * H / 6:.0f}px;height:{H / 6 + 2:.0f}px;background:{AC if k % 2 else AC2};"></div>' for k in range(6))
        HT.append(f'<div id="{oid}" style="position:absolute;inset:0;z-index:30;">{bars}</div>')
        tw(f"#{oid} .vb", "{scaleX:1, transformOrigin:'100% 50%'}", "{scaleX:0, duration:0.35, stagger:0.04, ease:'power2.in'}", t)
        win(f"#{oid}", t - 0.02, t + 0.65)
    elif o == "glitch":
        bars = "".join(f'<div class="vb" id="{oid}b{k}" style="top:{random.uniform(0, H - 120):.0f}px;height:{random.choice([30, 60, 110])}px;background:{[AC, AC2, "#fff"][k % 3]};opacity:0.8;"></div>' for k in range(5))
        HT.append(f'<div id="{oid}" style="position:absolute;inset:0;z-index:30;">{bars}</div>')
        tw(f"#{oid} .vb", "{x:-200, opacity:0.9}", "{x:200, opacity:0, duration:0.08, stagger:0.03, repeat:1, ease:'steps(2)'}", t - 0.05)
        win(f"#{oid}", t - 0.06, t + 0.35)
        sfx("glitch-short", t - 0.05, 0.3)
    elif o == "diag":
        HT.append(f'<div id="{oid}" style="position:absolute;left:{-W}px;top:{-H * 0.3:.0f}px;width:{W * 0.9:.0f}px;height:{H * 1.6:.0f}px;background:{AC};transform:rotate(18deg);z-index:30;"></div>')
        tw(f"#{oid}", "{x:0}", f"{{x:{W * 2.6:.0f}, duration:0.55, ease:'power2.inOut'}}", t - 0.25)
        win(f"#{oid}", t - 0.27, t + 0.32)


# ---------------------------------------------------------------- scenes
for i, l in enumerate(LN):
    t0, t1 = l["t0"], l["t1"]
    hd = l["h"].upper() if ST["caps"] else l["h"]
    wh, n = words_html(i, hd, l.get("hi", []))
    body = f'<div class="head" id="L{i}h" style="left:{HX}px;width:{HW_}px;top:{HEAD_Y}px;font-size:{l.get("size", FS)}px;text-align:{ALIGN};">{wh}</div>'
    if l.get("sub"):
        body += f'<div class="sub" id="L{i}sub" style="left:{HX}px;width:{HW_}px;text-align:{ALIGN};">{E(l["sub"])}</div>'
    if l.get("end"):
        en = l["end"]
        ey = VIS["cy"] - 330
        icons = "".join(f'<span><img src="assets/img/icons/{ICONS[n_]}" alt="{E(n_)} icon">{E(n_)}</span>' for n_ in en.get("icons", []) if n_ in ICONS)
        body += (f'<div class="endc" id="L{i}e" style="top:{ey:.0f}px;"><img src="assets/img/logo.svg" alt="AI Video Automator logo" class="elogo" id="L{i}lg">'
                 f'<div class="ename">AI Video Automator</div><div><span class="ecta" id="L{i}cta">{E(en["cta"])}</span></div>'
                 + (f'<div class="eurl2">{E(en["url2"])}</div>' if en.get("url2") else "")
                 + (f'<div class="eicons">{icons}</div>' if icons else "") + "</div>")
        tw(f"#L{i}e", "{y:80, opacity:0}", "{y:0, opacity:1, duration:0.5, ease:'power3.out'}", t0 + 0.4)
        tw(f"#L{i}lg", "{scale:0, rotation:-120}", "{scale:1, rotation:0, duration:0.6, ease:'back.out(1.8)'}", t0 + 0.45)
        tw(f"#L{i}cta", "{scale:0.4, opacity:0}", "{scale:1, opacity:1, duration:0.4, ease:'back.out(2.4)'}", t0 + 0.9)
        to(f"#L{i}cta", '{scale:1.06, duration:0.45, yoyo:true, repeat:5, ease:"sine.inOut"}', t0 + 1.35)
        sfx("impact-punch", t0 + 0.95, 0.4)
        sfx("confirm-1", t0 + 1.0, 0.3)
    else:
        body += visual(i, l.get("vis", {}), t0, t1)
    HT.append(f'<div class="scene" id="L{i}">{body}</div>')
    animate_words(i, n, t0 + (0.3 if i else 0.0), t1 - t0)
    if l.get("sub"):
        tw(f"#L{i}sub", "{opacity:0, y:24}", "{opacity:1, y:0, duration:0.4}", t0 + 0.5 + n * 0.1)
    mv = ST["move"]
    if i > 0:
        ent = {"push": f"{{y:{H}}}", "slide": f"{{x:{W}}}", "turn": "{rotationY:90, transformOrigin:'0% 50%', opacity:0}", "zoom": "{scale:0.3, opacity:0}", "blur": "{opacity:0, filter:'blur(30px)'}",
               "cut": "{x:24}", "drop": f"{{y:{-H}}}", "spin": "{rotation:-90, scale:0.2, opacity:0}", "fade": "{opacity:0}"}[mv]
        fin = {"push": "{y:0", "slide": "{x:0", "turn": "{rotationY:0, opacity:1", "zoom": "{scale:1, opacity:1", "blur": "{opacity:1, filter:'blur(0px)'", "cut": "{x:0", "drop": "{y:0",
               "spin": "{rotation:0, scale:1, opacity:1", "fade": "{opacity:1"}[mv]
        ease = {"drop": "bounce.out", "cut": "steps(3)", "spin": "back.out(1.4)"}.get(mv, "power3.out")
        tw(f"#L{i}", ent, fin + f", duration:{0.12 if mv == 'cut' else 0.45}, ease:'{ease}'}}", t0)
        overlay(i, t0)
        sfx(MOVES_SFX[(i + int(SP["id"])) % 4], t0 - 0.1, 0.35)
    if i + 1 < len(LN):
        ex = {"push": f"{{y:{-H}", "slide": f"{{x:{-W}", "turn": "{rotationY:-90, transformOrigin:'100% 50%', opacity:0", "zoom": "{scale:3, opacity:0", "blur": "{opacity:0, filter:'blur(30px)'",
              "cut": "{opacity:0", "drop": f"{{y:{H}", "spin": "{rotation:90, scale:0.2, opacity:0", "fade": "{opacity:0"}[mv]
        to(f"#L{i}", ex + f", duration:{0.05 if mv == 'cut' else 0.35}, ease:'power2.in'}}", t1 - (0.05 if mv == "cut" else 0.35))
    win(f"#L{i}", t0, t1)

# brand lockup (always on; also the thumbnail)
HT.append(f'<div id="brand"><img src="assets/img/logo.svg" alt="AI Video Automator logo"><span>AI Video Automator</span></div>')

HEADF, BODYF = ST["fonts"]
ACC_CSS = {
    "marker": f"color:{TX};background:linear-gradient({AC}88, {AC}88) no-repeat 0 82%/100% 38%;",
    "glitch": f"color:{AC};text-shadow:4px 0 {AC2}, -4px 0 #ff0055;",
    "type": f"color:{AC};",
}.get(ST["anim"], f"color:{AC};")
SUB_Y = HEAD_Y + (FS * 1.1 * 3.2 if not WIDE else FS * 3.4)
CSS = f"""
@font-face {{ font-family:"HD"; src:url("assets/fonts/{HEADF}"); font-weight:100 900; }}
@font-face {{ font-family:"BD"; src:url("assets/fonts/{BODYF}"); font-weight:100 900; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:{BG1}; }}
#root {{ position:absolute; inset:0; overflow:hidden; font-family:BD; color:{TX}; perspective:1600px; }}
.blob {{ position:absolute; border-radius:50%; }}
.vb {{ position:absolute; left:0; width:100%; }}
.scene {{ position:absolute; inset:0; }}
.head {{ position:absolute; font-family:HD; font-weight:800; line-height:1.06; letter-spacing:{'1px' if ST['caps'] else '-2px'}; color:{TX}; perspective:900px; }}
.w {{ display:inline-block; transform-origin:50% 100%; }}
.w.ac {{ {ACC_CSS} }}
.sub {{ position:absolute; top:{SUB_Y:.0f}px; font-family:BD; font-weight:600; font-size:{44 if not WIDE else 36}px; line-height:1.3; color:{TX}; opacity:0.85; }}
.vis {{ position:absolute; left:0; top:0; }}
.chip {{ display:inline-flex; align-items:center; gap:18px; font-family:BD; font-weight:700; font-size:{52 if not WIDE else 40}px; padding:20px 40px; border-radius:26px; background:{CARD}; color:{CTX};
         box-shadow:0 16px 40px rgba(0,0,0,0.22); border:3px solid {AC}; white-space:nowrap; }}
.dot {{ width:22px; height:22px; border-radius:50%; background:{AC}; flex:none; }}
.bignum {{ display:inline-block; font-family:HD; font-weight:800; font-size:{250 if not WIDE else 200}px; line-height:1; color:{AC}; letter-spacing:-6px; white-space:nowrap;
           text-shadow:0 14px 0 rgba(0,0,0,0.15); }}
.bigsub {{ font-family:BD; font-weight:700; font-size:{56 if not WIDE else 44}px; margin-top:26px; color:{TX}; }}
.step {{ position:absolute; display:flex; align-items:center; gap:28px; font-family:BD; font-weight:700; font-size:{46 if not WIDE else 36}px; padding:24px 30px; border-radius:26px;
         background:{CARD}; color:{CTX}; box-shadow:0 16px 40px rgba(0,0,0,0.2); }}
.sn {{ width:84px; height:84px; border-radius:22px; background:{AC}; color:{BG1}; font-family:HD; font-weight:800; font-size:56px; display:flex; align-items:center; justify-content:center; flex:none; }}
.endc {{ position:absolute; left:0; width:{W}px; text-align:center; }}
.elogo {{ width:{200 if not WIDE else 150}px; height:{200 if not WIDE else 150}px; }}
.ename {{ font-family:HD; font-weight:800; font-size:{84 if not WIDE else 70}px; letter-spacing:-2px; margin:18px 0 34px; color:{TX}; }}
.ecta {{ display:inline-block; font-family:BD; font-weight:800; font-size:{62 if not WIDE else 52}px; padding:24px 52px; border-radius:26px; background:{AC}; color:{BG1 if ST['bg'] not in ('mono',) else '#fff'};
         box-shadow:0 18px 44px rgba(0,0,0,0.3); }}
.eurl2 {{ font-family:BD; font-weight:700; font-size:{46 if not WIDE else 38}px; margin-top:34px; color:{TX}; }}
.eicons {{ display:flex; justify-content:center; gap:22px; margin-top:40px; }}
.eicons span {{ display:flex; align-items:center; gap:12px; font-family:BD; font-weight:700; font-size:30px; padding:12px 22px; border-radius:18px; background:#fff; color:#111; }}
.eicons img {{ width:38px; height:38px; }}
#brand {{ position:absolute; left:{HX}px; top:{SAFE_T - 70 if not WIDE else 50}px; display:flex; align-items:center; gap:16px; font-family:BD; font-weight:800; font-size:{36 if not WIDE else 30}px; color:{TX}; z-index:40; }}
#brand img {{ width:{62 if not WIDE else 50}px; height:{62 if not WIDE else 50}px; }}
"""

A = [("mix", "assets/audio/mix.wav", 0, min(dur("assets/audio/mix.wav"), TOTAL), 1.0)]
A += [(f"fx{n}", f"assets/sfx/{nm}.mp3", t, None, v) for n, (nm, t, v) in enumerate(SFX)]
lanes, aud = [], []
for i, p, st, dd, v in sorted(A, key=lambda x: x[2]):
    if not os.path.exists(p):
        print("missing sfx", p)
        continue
    dd = min(dd or dur(p), dur(p), r3(TOTAL - st), 2.5 if i != "mix" else 999)
    if dd <= 0.05:
        continue
    j = next((q for q, e in enumerate(lanes) if e <= st), None)
    if j is None:
        lanes.append(0)
        j = len(lanes) - 1
    lanes[j] = st + dd + 0.01
    aud.append(f'<audio id="{i}" src="{p}" data-start="{st}" data-duration="{r3(dd)}" data-volume="{v}" data-track-index="{10 + j}"></audio>')

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
json.dump({"total": TOTAL, "lines": [[l["t0"], l["t1"], l["h"]] for l in LN]}, open("timing.json", "w"), indent=1)
print(f"built ad {SP['id']} style {SP['style']}: {TOTAL} s, lines at {[l['t0'] for l in LN]}")
