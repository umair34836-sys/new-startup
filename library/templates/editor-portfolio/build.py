# Video-editor portfolio / showreel (16:9 and 9:16 from one config). Made for MrCopper804 on 2026-10-27.
# Style copied from the owner's reference TikTok (abuhuraira__008, video 7679106664250789142, frames read here
# 2026-10-27): light grey paper with dust specks and blurred tape crosses in two corners, red (#f0193f) accents,
# avatar + "Hi, I'M <NAME>" + red "Available For Freelance Work" tag + "View My Work" button, kinetic
# "Want a video EDITOR", a clip montage and a "CONTACT ME" end card. Here every montage bar is a real clip of a
# delivered video (not a thumbnail) with the client's name, so the reel shows the work itself.
# Skills: #82 metric cutting (one clip per bar), #96 reel shot budget (nothing static > ~4 s), #104 hook < 3 s,
# #126 faked whip pan, #149 transitions on the music; CLAUDE.md "HyperFrames learnings" (first frame = title,
# audio lanes + data-duration, visibility windows).
#
#   python3 build.py CONFIG.json --format 16x9|9x16 --out PROJECT_DIR
#
# CONFIG (see example-config.json): name, role, tag, contacts [[label, value, colour]], music + drop + bpm (from
# listen.py on the cut music: drop = a downbeat where the montage starts), clips [{src, start, client, type}],
# grid [clip indices for the wall]. Clips are cut + scaled with ffmpeg into PROJECT_DIR/assets/clips (muted).
# PROJECT_DIR must already hold assets/vendor/gsap-3.14.2.min.js, assets/fonts (Poppins, Anton), assets/sfx,
# assets/characters/host-skin.png and assets/music/music.mp3 (the template README lists them).
import argparse, json, os, random, subprocess

ap = argparse.ArgumentParser()
ap.add_argument("config")
ap.add_argument("--format", choices=["16x9", "9x16"], default="16x9")
ap.add_argument("--out", required=True)
ap.add_argument("--no-clips", action="store_true", help="skip re-cutting clips that already exist")
a = ap.parse_args()
C = json.load(open(a.config))
os.chdir(a.out)
os.makedirs("compositions", exist_ok=True)
REPO = os.environ.get("REPO", "/home/user/new-startup")
WIDE = a.format == "16x9"
W, H = (1920, 1080) if WIDE else (1080, 1920)
RED, INK, GREY = "#f0193f", "#151515", "#6b6b6b"
BAR = 240.0 / C["bpm"]
BEAT = BAR / 4
DROP = C["drop"]
CL = C["clips"]
N = len(CL)
T_WANT = round(DROP - 2 * BAR, 3)
T_MONT = DROP
T_GRID = round(DROP + N * BAR, 3)
T_END = round(T_GRID + 2 * BAR, 3)
TOTAL = round(T_END + 4 * BAR + 1.0, 3)
random.seed(7)


def r3(x):
    return round(x, 3)


def probe(p, what="format=duration"):
    return subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", what, "-of", "csv=p=0", p],
                          capture_output=True, text=True).stdout.strip()


def dur(p):
    return round(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                      capture_output=True, text=True).stdout), 3)


# ---------------------------------------------------------------- clips: one card per bar
# card box per orientation of the SOURCE: vertical sources go in a phone-shaped card, horizontal in a 16:9 card
if WIDE:
    BOX_V, BOX_H = (486, 864), (1216, 684)
else:
    BOX_V, BOX_H = (792, 1408), (1000, 562)
CLIP_LEN = r3(2 * BAR + 0.4)          # montage uses the first bar, the wall replays the same file
os.makedirs("assets/clips", exist_ok=True)
for i, c in enumerate(CL):
    w, h = map(int, probe(c["src"], "stream=width,height").split(","))
    c["vert"] = h > w
    bw, bh = BOX_V if c["vert"] else BOX_H
    c["box"] = (bw, bh)
    c["file"] = f"assets/clips/c{i:02d}.mp4"
    if a.no_clips and os.path.exists(c["file"]):
        continue
    # cover-scale into the card (sources are 9:16 or 16:9, so this is a scale with at most a sliver of crop);
    # cas sharpens upscaled 720p sources (skill #489)
    vf = (f"scale={bw}:{bh}:force_original_aspect_ratio=increase:flags=lanczos,crop={bw}:{bh},"
          f"cas=strength=0.4,fps=30,format=yuv420p")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(c["start"]), "-t", str(CLIP_LEN), "-i", c["src"], "-an",
                    "-vf", vf, "-c:v", "libx264", "-crf", "17", "-preset", "medium", c["file"]], check=True)

# ---------------------------------------------------------------- host avatar (owner's skin)
# A still of the waving host made with blocky_character.py in a 600x600 mini project (scale 17, feet y 650, turn -18,
# snapshot at 0.6 s; recipe in README.md). A live CSS-3D character inside the round mask escaped the clip and the
# scene's visibility window in the first test render (snapshot 2026-10-27), so the avatar is an <img> that bobs.
AV = 300 if WIDE else 340             # avatar circle size


def avatar(cid, d, left, top, size=AV):
    return (f'<div class="avatar" style="left:{left}px;top:{top}px;width:{size}px;height:{size}px;">'
            f'<img id="{cid}" src="{C.get("avatar", "assets/img/avatar.png")}" alt="{C["name"]} avatar" '
            f'style="position:absolute;left:0;top:0;width:100%;height:100%;transform-origin:50% 85%;"></div>')


T, A, HTML, PRE = [], [], [], []
lane = [2]


def sfx(f, t, v):
    A.append((f, r3(max(0, t)), v))


def win(sel, s0, s1):
    """visible only inside [s0, s1) (keeps hidden things out of layout checks)"""
    if s0 > 0:
        PRE.append(f'gsap.set("{sel}", {{visibility:"hidden"}});')
        T.append(f'tl.set("{sel}", {{visibility:"visible"}}, {r3(s0)});')
    if s1 < TOTAL:
        T.append(f'tl.set("{sel}", {{visibility:"hidden"}}, {r3(s1)});')


# ---------------------------------------------------------------- background: paper, dust, tape crosses, grain
dust = []
for k in range(140):
    x, y = random.uniform(0, W), random.uniform(0, H)
    ln, ang, op = random.uniform(2, 16), random.uniform(0, 180), random.uniform(0.25, 0.7)
    th = random.choice([1.2, 1.6, 2.2])
    dust.append(f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x + ln:.0f}" y2="{y + random.uniform(-6, 6):.0f}" '
                f'stroke="#222" stroke-width="{th}" stroke-linecap="round" opacity="{op:.2f}" '
                f'transform="rotate({ang:.0f} {x:.0f} {y:.0f})"/>')
for k in range(40):
    dust.append(f'<circle cx="{random.uniform(0, W):.0f}" cy="{random.uniform(0, H):.0f}" r="{random.uniform(1, 2.6):.1f}" '
                f'fill="#222" opacity="{random.uniform(0.3, 0.7):.2f}"/>')
TS = 1.0 if WIDE else 1.15


def tape(x, y, rot):
    bar = lambda r: (f'<div style="position:absolute;left:-{int(170 * TS)}px;top:-{int(34 * TS)}px;width:{int(340 * TS)}px;'
                     f'height:{int(68 * TS)}px;border-radius:12px;background:linear-gradient(90deg,#2b2b2b,#555 50%,#2b2b2b);'
                     f'transform:rotate({r}deg);box-shadow:0 0 0 10px rgba(80,80,80,0.35);"></div>')
    return (f'<div class="tape" data-layout-allow-overflow style="left:{x}px;top:{y}px;transform:rotate({rot}deg);filter:blur(7px);opacity:0.85;">'
            f'{bar(45)}{bar(-45)}</div>')


HTML.append(f'''<div id="bg" style="position:absolute;inset:0;background:radial-gradient(ellipse 75% 70% at 50% 46%, #fbfbfb 0%, #e3e3e3 52%, #9d9d9d 100%);"></div>
  <svg id="dust" data-layout-allow-overflow width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="position:absolute;left:0;top:0;">{"".join(dust)}</svg>
  {tape(20, 0, 8)}{tape(W - 30, H - 20, -6)}''')
T.append(f'tl.fromTo("#dust", {{x:0, y:0}}, {{x:-40, y:24, duration:{TOTAL}, ease:"none"}}, 0);')
T.append(f'tl.fromTo(".tape", {{rotation:"-=4"}}, {{rotation:"+=8", duration:{TOTAL}, ease:"sine.inOut"}}, 0);')

# ---------------------------------------------------------------- S1 hello (0 - T_WANT): on screen at frame 0
if WIDE:
    ax, ay, tx, ty, nsize = 360, 390, 720, 405, 72
else:
    ax, ay, tx, ty, nsize = (W - AV) // 2, 520, 0, 930, 78
name = C["name"]
letters = "".join(f'<span class="ch">{ch if ch != " " else "&nbsp;"}</span>' for ch in name)
align = "left" if WIDE else "center"
pos = f"left:{tx}px;" if WIDE else "left:0;right:0;"
HTML.append(f'''<div id="s1" style="position:absolute;inset:0;">
  {avatar("hosta", T_WANT, ax, ay)}
  <div id="h-tag" class="pill" style="position:absolute;{pos}top:{ty - 70}px;text-align:{align};"><span style="background:{RED};color:#fff;font-size:{30 if WIDE else 34}px;padding:6px 18px;border-radius:8px;">{C["tag"]}</span></div>
  <div id="h-name" class="pop" style="position:absolute;{pos}top:{ty}px;font-size:{nsize}px;color:{INK};text-align:{align};white-space:nowrap;"><span class="sb">Hi,&nbsp;I'M&nbsp;</span>{letters}</div>
  <div id="h-role" class="sb" style="position:absolute;{pos}top:{ty + nsize + 22}px;font-size:{40 if WIDE else 46}px;color:{INK};text-align:{align};">{C["role"]}</div>
  <div id="h-btn" style="position:absolute;{pos}top:{ty + nsize + 100}px;text-align:{align};"><span class="pop" style="display:inline-block;background:{RED};color:#fff;font-size:{40 if WIDE else 46}px;padding:10px 34px;border-radius:16px;box-shadow:0 10px 30px rgba(240,25,63,0.35);">View My Work &#8250;</span></div>
</div>''')
# name types in letter by letter from 0.25 s; the first 4 letters are already there at 0 s (thumbnail shows a name)
nch = len(name)
PRE.append(f'gsap.set("#h-name .ch", {{opacity:0}}); gsap.set("#h-name .ch:nth-child(-n+5)", {{opacity:1}});')
T.append(f'tl.to("#h-name .ch:nth-child(n+6)", {{opacity:1, duration:0.01, stagger:{r3(0.9 / max(1, nch - 4))}}}, 0.2);')
sfx("typing-keyboard-fast", 0.2, 0.35)
T.append(f'tl.fromTo("#hosta", {{rotation:-3, y:0}}, {{rotation:3, y:-6, duration:{r3(BEAT * 2)}, yoyo:true, repeat:3, ease:"sine.inOut"}}, 0);')
T.append(f'tl.fromTo("#h-tag", {{scale:0, opacity:0}}, {{scale:1, opacity:1, duration:0.35, ease:"back.out(2.2)"}}, {r3(BEAT * 3)});')
T.append(f'tl.fromTo("#h-role", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.3}}, {r3(BEAT * 4)});')
T.append(f'tl.fromTo("#h-btn", {{scale:0, opacity:0}}, {{scale:1, opacity:1, duration:0.35, ease:"back.out(2.4)"}}, {r3(BEAT * 5)});')
T.append(f'tl.to("#h-btn", {{scale:1.06, duration:{r3(BEAT)}, yoyo:true, repeat:1, ease:"sine.inOut"}}, {r3(BEAT * 6)});')
sfx("pop-high", BEAT * 3, 0.5)
sfx("pluck", BEAT * 4, 0.5)
sfx("pop-high", BEAT * 5, 0.5)
sfx("click-1", BEAT * 7, 0.6)
T.append(f'tl.to("#s1", {{scale:1.25, opacity:0, filter:"blur(14px)", duration:0.25, ease:"power3.in"}}, {r3(T_WANT - 0.25)});')
sfx("whoosh-fast-0.3s", T_WANT - 0.3, 0.6)
win("#s1", 0, T_WANT)

# ---------------------------------------------------------------- S2 "Want a video EDITOR?" (T_WANT - DROP)
ws = 120 if WIDE else 116
HTML.append(f'''<div id="s2" style="position:absolute;inset:0;">
  <div style="position:absolute;left:0;right:0;top:{H / 2 - (ws if WIDE else ws * 1.6):.0f}px;text-align:center;">
    <span id="w1" class="pop wd" style="font-size:{ws}px;color:{INK};">Want</span>
    <span id="w2" class="pop wd" style="font-size:{ws}px;color:{INK};">a</span>
    <span id="w3" class="pop wd" style="font-size:{ws}px;color:{INK};">video</span>{"" if WIDE else "<br>"}
    <span id="w4" class="pop wd" style="font-size:{int(ws * 1.05)}px;color:#fff;background:{RED};padding:0 26px;border-radius:18px;">EDITOR?</span>
  </div>
</div>''')
for k, b in ((1, 0), (2, 1), (3, 2), (4, 4)):
    t = r3(T_WANT + b * BEAT)
    T.append(f'tl.fromTo("#w{k}", {{opacity:0, y:60, scale:1.6}}, {{opacity:1, y:0, scale:1, duration:0.28, ease:"power4.out"}}, {t});')
    sfx("impact-punch" if k == 4 else "pluck", t, 0.5 if k == 4 else 0.45)
T.append(f'tl.fromTo("#w4", {{rotation:-4}}, {{rotation:4, duration:0.1, yoyo:true, repeat:4, ease:"none"}}, {r3(T_WANT + 4 * BEAT + 0.3)});')
T.append(f'tl.to("#s2", {{scale:3, opacity:0, duration:0.3, ease:"power3.in"}}, {r3(DROP - 0.3)});')
sfx("whoosh-up-0.6s", DROP - 0.55, 0.55)
win("#s2", T_WANT, DROP)

# ---------------------------------------------------------------- S3 montage: one clip per bar
VARIANTS = ["whipL", "zoom", "whipR", "drop", "flip", "rise"]
mont = []
lab_top = 0
for i, c in enumerate(CL):
    s0 = r3(T_MONT + i * BAR)
    s1 = r3(s0 + BAR)
    bw, bh = c["box"]
    if WIDE:
        if c["vert"]:
            cx, cy = 1180, (H - bh) // 2        # phone card right of centre, label on the left
            lx, ly, lw, la = 150, 380, 820, "left"
        else:
            cx, cy = (W - bw) // 2 + 150, 230
            lx, ly, lw, la = 150, 60, 1700, "left"
    else:
        cx = (W - bw) // 2
        cy = 380 if c["vert"] else 760
        lx, ly, lw, la = 60, (150 if c["vert"] else 470), W - 120, "center"
    rot = (-2, 1.5, -1, 2, -1.5, 1)[i % 6]
    mont.append(f'''<div id="m{i}" style="position:absolute;inset:0;">
    <div id="m{i}c" class="card" style="left:{cx}px;top:{cy}px;width:{bw}px;height:{bh}px;transform:rotate({rot}deg);border-radius:{26 if c["vert"] else 18}px;">
      <video id="m{i}v" src="{c["file"]}" data-start="{s0}" data-duration="{r3(BAR)}" muted playsinline style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;"></video>
    </div>
    <div id="m{i}t" class="tapebit" style="left:{cx + bw / 2 - 90:.0f}px;top:{cy - 26}px;transform:rotate({-rot * 2}deg);"></div>
    <div id="m{i}l" style="position:absolute;left:{lx}px;top:{ly}px;width:{lw}px;text-align:{la};">
      <div class="sb" style="font-size:{30 if WIDE else 34}px;color:{GREY};letter-spacing:3px;">{i + 1:02d} / {N:02d}</div>
      <div class="anton" style="font-size:{(96 if c["vert"] else 84) if WIDE else 92}px;color:{INK};line-height:1.05;">{c["client"]}</div>
      <div style="margin-top:12px;"><span class="pill" style="background:{RED};color:#fff;font-size:{34 if WIDE else 38}px;padding:6px 20px;border-radius:10px;">{c["type"]}</span></div>
    </div>
  </div>''')
    v = VARIANTS[i % len(VARIANTS)]
    frm = {"whipL": "{x:-900, filter:'blur(18px)'}", "whipR": "{x:900, filter:'blur(18px)'}",
           "zoom": "{scale:0.3, opacity:0}", "drop": "{y:-900}", "flip": "{rotationY:90, opacity:0}",
           "rise": "{y:700, rotation:12}"}[v]
    to = {"whipL": "{x:0, filter:'blur(0px)'", "whipR": "{x:0, filter:'blur(0px)'", "zoom": "{scale:1, opacity:1",
          "drop": "{y:0", "flip": "{rotationY:0, opacity:1", "rise": f"{{y:0, rotation:{rot}"}[v]
    T.append(f'tl.fromTo("#m{i}c", {frm}, {to}, duration:0.3, ease:"power3.out"}}, {s0});')
    T.append(f'tl.to("#m{i}c", {{scale:1.04, duration:{r3(BAR - 0.3)}, ease:"none"}}, {r3(s0 + 0.3)});')
    T.append(f'tl.fromTo("#m{i}t", {{scaleX:0}}, {{scaleX:1, duration:0.2, ease:"power2.out"}}, {r3(s0 + 0.2)});')
    same = i > 0 and CL[i - 1]["client"] == c["client"]
    T.append(f'tl.fromTo("#m{i}l", {{opacity:0, x:{0 if not WIDE else -60}, y:{30 if not WIDE else 0}}}, '
             f'{{opacity:1, x:0, y:0, duration:{0.15 if same else 0.3}, ease:"power3.out"}}, {r3(s0 + (0 if same else BEAT * 0.5))});')
    sfx("whoosh-fast-0.3s" if v.startswith("whip") else ("swish-1" if i % 2 else "pop-high"), s0 - 0.05, 0.5)
    win(f"#m{i}", s0, s1)
HTML.append('<div id="s3" style="position:absolute;inset:0;">' + "\n  ".join(mont) + "</div>")
sfx("impact-punch", T_MONT, 0.4)

# ---------------------------------------------------------------- S4 wall: the grid clips at once (2 bars)
G = C["grid"]                         # vertical clips: the wall cells are portrait
cols = 6 if WIDE else 3
gw, ch, gap = (260, 462, 34) if WIDE else (300, 533, 30)
rows = (len(G) + cols - 1) // cols
cells = []
for k, i in enumerate(G):
    c = CL[i]
    r_, q = divmod(k, cols)
    x0 = (W - (cols * gw + (cols - 1) * gap)) // 2 + q * (gw + gap)
    y0 = (190 if WIDE else 380) + r_ * (ch + gap)
    cells.append(f'<div id="g{k}" class="card" style="left:{x0}px;top:{y0}px;width:{gw}px;height:{ch}px;border-radius:14px;">'
                 f'<video id="g{k}v" src="{c["file"]}" data-start="{T_GRID}" data-duration="{r3(2 * BAR)}" data-media-start="{r3(BAR)}" '
                 f'muted playsinline style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;"></video></div>')
    T.append(f'tl.fromTo("#g{k}", {{scale:0, rotation:{random.choice([-8, 8])}}}, {{scale:1, rotation:0, duration:0.35, '
             f'ease:"back.out(1.7)"}}, {r3(T_GRID + k * 0.06)});')
nclients = len(dict.fromkeys(c["client"] for c in CL))
gy = (190 if WIDE else 380) + rows * (ch + gap) + 20
HTML.append(f'''<div id="s4" style="position:absolute;inset:0;">{"".join(cells)}
  <div id="g-cap" style="position:absolute;left:0;right:0;top:{gy}px;text-align:center;">
    <span class="anton" style="font-size:{70 if WIDE else 84}px;color:{INK};">{N} VIDEOS</span>
    <span class="anton" style="font-size:{70 if WIDE else 84}px;color:{RED};">&nbsp;&#8226;&nbsp;{nclients} BRANDS</span></div>
</div>''')
T.append(f'tl.fromTo("#g-cap", {{opacity:0, scale:1.5}}, {{opacity:1, scale:1, duration:0.3, ease:"power4.out"}}, {r3(T_GRID + BAR)});')
sfx("sub-drop", T_GRID, 0.45)
sfx("impact-punch", T_GRID + BAR, 0.45)
T.append(f'tl.to("#s4", {{scale:0.6, opacity:0, duration:0.3, ease:"power3.in"}}, {r3(T_END - 0.3)});')
sfx("whoosh-fast-0.3s", T_END - 0.3, 0.6)
win("#s4", T_GRID, T_END)

# ---------------------------------------------------------------- S5 contact end card
rows_html = []
for k, (lab, val, col) in enumerate(C["contacts"]):
    rows_html.append(f'<div id="c{k}" class="crow"><span class="cdot" style="background:{col};"></span>'
                     f'<span class="sb" style="color:{GREY};">{lab}</span><span class="pop" style="color:{INK};">{val}</span></div>')
if WIDE:
    ex, ey, cl_ = 250, 300, 720
    end_head = f'''{avatar("hostb", r3(TOTAL - T_END), ex, ey - 20)}
  <div id="e-name" class="anton" style="position:absolute;left:{ex - 60}px;top:{ey + AV + 10}px;width:{AV + 120}px;text-align:center;font-size:62px;color:{INK};">{name}</div>
  <div id="e-role" class="sb" style="position:absolute;left:{ex - 60}px;top:{ey + AV + 95}px;width:{AV + 120}px;text-align:center;font-size:34px;color:{GREY};">{C["role"]}</div>'''
    cpos = f"left:{cl_}px;top:190px;"
else:
    end_head = f'''{avatar("hostb", r3(TOTAL - T_END), (W - AV) // 2, 230)}
  <div id="e-name" class="anton" style="position:absolute;left:0;right:0;top:{230 + AV + 20}px;text-align:center;font-size:84px;color:{INK};">{name}</div>
  <div id="e-role" class="sb" style="position:absolute;left:0;right:0;top:{230 + AV + 125}px;text-align:center;font-size:42px;color:{GREY};">{C["role"]}</div>'''
    cpos = f"left:70px;right:70px;top:{230 + AV + 230}px;"
HTML.append(f'''<div id="s5" style="position:absolute;inset:0;">
  {end_head}
  <div id="e-box" style="position:absolute;{cpos}">
    <div id="e-cta"><span class="pop" style="display:inline-block;background:{RED};color:#fff;font-size:{64 if WIDE else 72}px;padding:8px 36px;border-radius:16px;">CONTACT ME</span></div>
    <div id="e-sub" class="sb" style="font-size:{38 if WIDE else 44}px;color:{INK};margin:14px 0 26px;">{C["cta_sub"]}</div>
    {"".join(rows_html)}
  </div>
</div>''')
T.append(f'tl.fromTo("#e-name", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.3}}, {r3(T_END + BEAT)});')
T.append(f'tl.fromTo("#e-role", {{opacity:0}}, {{opacity:1, duration:0.3}}, {r3(T_END + 2 * BEAT)});')
T.append(f'tl.fromTo("#e-cta", {{scale:0, opacity:0}}, {{scale:1, opacity:1, duration:0.35, ease:"back.out(2.2)"}}, {r3(T_END)});')
T.append(f'tl.fromTo("#e-sub", {{opacity:0, x:-30}}, {{opacity:1, x:0, duration:0.3}}, {r3(T_END + BEAT)});')
for k in range(len(C["contacts"])):
    t = r3(T_END + (2 + k) * BEAT)
    T.append(f'tl.fromTo("#c{k}", {{opacity:0, x:{-60 if WIDE else 0}, y:{0 if WIDE else 30}}}, {{opacity:1, x:0, y:0, duration:0.28, ease:"power3.out"}}, {t});')
    sfx("pluck", t, 0.4)
T.append(f'tl.to("#e-cta", {{scale:1.06, duration:{r3(BEAT * 2)}, yoyo:true, repeat:5, ease:"sine.inOut"}}, {r3(T_END + 8 * BEAT)});')
sfx("impact-punch", T_END, 0.4)
T.append(f'tl.fromTo("#hostb", {{scale:0.6, rotation:-10}}, {{scale:1, rotation:0, duration:0.45, ease:"back.out(2)"}}, {r3(T_END)});')
T.append(f'tl.to("#hostb", {{rotation:3, y:-6, duration:{r3(BEAT * 2)}, yoyo:true, repeat:9, ease:"sine.inOut"}}, {r3(T_END + 0.5)});')
sfx("sparkle", T_END + BEAT, 0.3)
win("#s5", T_END, TOTAL + 1)

# grain over everything (soft-light, own overlay from library/stock, looped by repeated clips)
grain = []
gd = 6.0
k = 0
t = 0.0
while t < TOTAL:
    d = r3(min(gd, TOTAL - t))
    grain.append(f'<video id="gr{k}" src="assets/clips/grain.mp4" data-start="{r3(t)}" data-duration="{d}" muted playsinline '
                 f'style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;mix-blend-mode:soft-light;opacity:0.35;"></video>')
    t += gd
    k += 1
if not os.path.exists("assets/clips/grain.mp4"):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{REPO}/library/stock/own-overlays/film-grain.mp4", "-an", "-vf",
                    f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},format=yuv420p", "-c:v", "libx264",
                    "-crf", "26", "assets/clips/grain.mp4"], check=True)

CSS = f"""
@font-face {{ font-family: "Poppins"; src: url("assets/fonts/Poppins-SemiBold.ttf"); font-weight: 600; }}
@font-face {{ font-family: "Poppins"; src: url("assets/fonts/Poppins-Bold.ttf"); font-weight: 700; }}
@font-face {{ font-family: "Poppins"; src: url("assets/fonts/Poppins-ExtraBold.ttf"); font-weight: 800; }}
@font-face {{ font-family: "Anton"; src: url("assets/fonts/Anton-Regular.ttf"); }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:#e3e3e3; }}
#root {{ position:absolute; inset:0; overflow:hidden; font-family:Poppins; }}
.pop {{ font-family:Poppins; font-weight:800; }}
.sb {{ font-family:Poppins; font-weight:600; }}
.pill {{ font-family:Poppins; font-weight:700; }}
.anton {{ font-family:Anton; letter-spacing:1px; }}
.wd {{ display:inline-block; margin:0 10px; }}
.avatar {{ position:absolute; border-radius:50%; overflow:hidden; background:radial-gradient(circle at 50% 35%, #3a3a3a, #0d0d0d 70%);
          box-shadow:0 0 0 8px rgba(255,255,255,0.9), 0 18px 40px rgba(0,0,0,0.35); }}
.card {{ position:absolute; overflow:hidden; background:#111; box-shadow:0 0 0 8px #fff, 0 26px 60px rgba(0,0,0,0.38); }}
.tapebit {{ position:absolute; width:180px; height:46px; background:rgba(240,25,63,0.85); transform-origin:50% 50%; }}
.tape {{ position:absolute; width:0; height:0; }}
.crow {{ display:flex; align-items:center; gap:18px; font-size:{40 if WIDE else 44}px; margin:12px 0; white-space:nowrap; }}
.cdot {{ width:22px; height:22px; border-radius:50%; flex:none; }}
"""
music_d = dur("assets/music/music.mp3")
audio = [f'<audio id="music" src="assets/music/music.mp3" data-start="0" data-duration="{min(TOTAL, music_d)}" data-volume="0.85" '
         f'data-track-index="1" data-fade-out="1.5"></audio>']
lanes = []                            # greedy lane per sfx so overlapping clips never share a track (lint)
for n, (f, s, v) in enumerate(sorted(A, key=lambda x: x[1])):
    p = f"assets/sfx/{f}.mp3"
    d = min(dur(p), r3(TOTAL - s))
    k = next((j for j, end in enumerate(lanes) if end <= s), None)
    if k is None:
        lanes.append(0)
        k = len(lanes) - 1
    lanes[k] = s + d + 0.01
    audio.append(f'<audio id="sx{n}" src="{p}" data-start="{s}" data-duration="{d}" data-volume="{v}" data-track-index="{2 + k}"></audio>')

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
  {chr(10).join(grain)}
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
json.dump({"total": TOTAL, "drop": DROP, "bar": BAR, "montage": [T_MONT, T_GRID], "wall": [T_GRID, T_END], "end": T_END},
          open("timing.json", "w"), indent=1)
print(f"built {a.format}: {TOTAL} s, {N} clips, {len(T)} tweens, {len(A)} sfx")
