# Video-editor portfolio / showreel (16:9 and 9:16 from one config). Made for MrCopper804 on 2026-10-27.
# Style copied from the owner's reference TikTok (abuhuraira__008, video 7679106664250789142, frames read here
# 2026-10-27): light grey paper with dust specks and blurred tape crosses in two corners, red (#f0193f) accents,
# avatar + "Hi, I'M <NAME>" + red "Available For Freelance Work" tag + "View My Work" button, kinetic
# "Want a video EDITOR", a clip montage and a "CONTACT ME" end card. Here the montage plays real clips of delivered
# videos (not thumbnails), one section per brand: the brand name lands once, then its videos follow (vertical ones
# side by side), so no brand repeats (owner feedback on v1, 2026-10-27: "ek brand ka baar baar repeat hona").
# Skills: #82 metric cutting (one group per bar), #96 reel shot budget, #104 hook < 3 s, #126 faked whip pan,
# #149 transitions on the music; CLAUDE.md "HyperFrames learnings" (first frame = title, audio lanes +
# data-duration, visibility windows).
# SFX timing (owner feedback on v1: "sound effect apne right place per nahi lage"): every SFX is placed so its
# measured PEAK (numpy envelope, README table) lands on the music beat where the visual lands; one-shot files are
# trimmed to the action (v1 let the 8 s typing loop run under the next scene).
#
#   python3 build.py CONFIG.json --format 16x9|9x16 --out PROJECT_DIR
#
# CONFIG (see example-config.json): name, role, tag, cta_sub, contacts [[label, value, colour]], bpm + drop (from
# listen.py on the cut music: drop = the downbeat where the montage starts), brands [{client, clips: [{src, start,
# type}]}] in screen order, grid = indices into the flattened clip list (vertical clips) for the wall.
# PROJECT_DIR must already hold assets/vendor/gsap-3.14.2.min.js, assets/fonts (Poppins, Anton), assets/sfx,
# assets/img/avatar.png and assets/music/music.mp3 (the template README lists them).
import argparse, json, math, os, random, subprocess

ap = argparse.ArgumentParser()
ap.add_argument("config")
ap.add_argument("--format", choices=["16x9", "9x16"], default="16x9")
ap.add_argument("--out", required=True)
ap.add_argument("--no-clips", action="store_true", help="skip re-cutting clips that already exist")
a = ap.parse_args()
C = json.load(open(a.config))
os.chdir(a.out)
REPO = os.environ.get("REPO", "/home/user/new-startup")
WIDE = a.format == "16x9"
W, H = (1920, 1080) if WIDE else (1080, 1920)
RED, INK, GREY = "#f0193f", "#151515", "#6b6b6b"
BAR = 240.0 / C["bpm"]
BEAT = BAR / 4
DROP = C["drop"]
random.seed(7)

# measured here 2026-10-27 (numpy RMS envelope, 10 ms window): seconds from file start to the loudest point
PEAK = {"riser-2s": 1.68, "impact-boom": 0.03, "whoosh-fast-0.3s": 0.17, "whoosh-up-0.6s": 0.30, "swish-1": 0.04, "impact-punch": 0.01, "sub-drop": 0.02,
        "pop-high": 0.01, "pluck": 0.0, "click-1": 0.0, "sparkle": 0.45, "typing-keyboard-fast": 0.04}


def r3(x):
    return round(x, 3)


def bt(n):
    """time of beat n counted from the drop (n < 0 = before it): every hit sits on the music grid"""
    return r3(DROP + n * BEAT)


def next_beat(t):
    return bt(math.ceil((t - DROP) / BEAT - 1e-6))


def probe(p, what):
    return subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", what, "-of", "csv=p=0", p],
                          capture_output=True, text=True).stdout.strip()


def dur(p):
    return round(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                      capture_output=True, text=True).stdout), 3)


# ---------------------------------------------------------------- optional voice-over (v4, owner 2026-10-30)
# "vo": {"parts": [8 wavs from vs_tts.py --parts], "hello": 0, "want": 1, "policy": [2..6], "contact": 7,
#        "music_src": track, "src_drop": s}: the hello / "want" scenes stretch to their lines, policy scenes (text +
#        rates) follow the wall one per line, the end card waits for its line; the music is fitted with music_fit.py
#        so its drop sits on the montage drop, then mixed under the voice with mix_vo_music.py (ducking).
VO = C.get("vo")
if VO:
    VLEN = [dur(p) for p in VO["parts"]]
    # at least 3.4 s so the role line and the "View My Work" button (beat-timed) are seen before the scene leaves
    t_want = r3(max(0.3 + VLEN[VO["hello"]] + 0.35, 3.4))
    # line "want" starts 0.1 s into the 6-beat "want" scene and must end 0.3 s before the drop
    DROP = r3(t_want + max(6 * BEAT, VLEN[VO["want"]] + 0.4))


# ---------------------------------------------------------------- clips + groups (one group = one bar)
MAXV = 3 if WIDE else 2
if WIDE:
    BOX_V, BOX_H = (388, 690), (1220, 686)
else:
    BOX_V, BOX_H = (640, 1138), (1000, 562)
CLIP_LEN = r3(2 * BAR + 0.4)          # the montage uses the first bar, the wall replays the second
os.makedirs("assets/clips", exist_ok=True)
FLAT, GROUPS = [], []
for bi, b in enumerate(C["brands"]):
    run = []
    for c in b["clips"]:
        w, h = map(int, probe(c["src"], "stream=width,height").split(","))
        c["vert"] = h > w
        c["client"] = b["client"]
        c["id"] = len(FLAT)
        c["file"] = f"assets/clips/c{c['id']:02d}.mp4"
        FLAT.append(c)
        if not (a.no_clips and os.path.exists(c["file"])):
            bw, bh = BOX_V if c["vert"] else BOX_H
            # cover-scale into the card; cas sharpens upscaled 720p sources (skill #489)
            vf = (f"scale={bw}:{bh}:force_original_aspect_ratio=increase:flags=lanczos,crop={bw}:{bh},"
                  f"cas=strength=0.4,fps=30,format=yuv420p")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(c["start"]), "-t", str(CLIP_LEN), "-i", c["src"],
                            "-an", "-vf", vf, "-c:v", "libx264", "-crf", "17", "-preset", "medium", c["file"]], check=True)
    # consecutive vertical clips share a bar (side by side), a horizontal clip gets its own bar
    verts = [c for c in b["clips"] if c["vert"]]
    hors = [c for c in b["clips"] if not c["vert"]]
    for k in range(0, len(verts), MAXV):
        GROUPS.append({"brand": bi, "clips": verts[k:k + MAXV]})
    for c in hors:
        GROUPS.append({"brand": bi, "clips": [c]})
NB = len(C["brands"])
NG = len(GROUPS)
N = len(FLAT)
T_WANT = bt(-6)
T_GRID = r3(DROP + NG * BAR)
T_END = r3(T_GRID + 2 * BAR)
T_C = T_END                          # end card start
TOTAL = r3(T_END + 3 * BAR + 1.0)
VOAT = []                            # (part index, start) placements of the voice lines
POL = []                             # policy scenes: [start, end, line index, scene config]
if VO:
    VOAT.append((VO["hello"], 0.3))
    VOAT.append((VO["want"], r3(T_WANT + 0.1)))
    cur = T_END
    for li, pc in zip(VO["policy"], C["policy"]):
        s0 = next_beat(cur)          # every policy scene starts on a beat of the (ducked) music
        VOAT.append((li, r3(s0 + 0.2)))
        cur = r3(s0 + 0.2 + VLEN[li] + 0.5)
        POL.append([s0, cur, li, pc])
    T_C = next_beat(cur)
    for k in range(len(POL)):        # each scene stays up until the next one starts (no empty paper between them)
        POL[k][1] = POL[k + 1][0] if k + 1 < len(POL) else T_C
    VOAT.append((VO["contact"], r3(T_C + 0.3)))
    TOTAL = r3(T_C + max(3 * BAR + 1.0, 0.3 + VLEN[VO["contact"]] + 3.2))
for gi, g in enumerate(GROUPS):
    g["s0"] = r3(DROP + gi * BAR)
    g["first"] = gi == 0 or GROUPS[gi - 1]["brand"] != g["brand"]
brand_t = {}
for g in GROUPS:
    brand_t.setdefault(g["brand"], [g["s0"], 0])
    brand_t[g["brand"]][1] = r3(g["s0"] + BAR)

T, A, HTML, PRE = [], [], [], []


def sfx(f, hit, v, d=None):
    """place SFX f so its measured peak lands on `hit`; d trims the file (seconds of audio kept)"""
    A.append((f, r3(max(0, hit - PEAK[f])), v, d))


def win(sel, s0, s1):
    """visible only inside [s0, s1) (keeps hidden things out of layout checks)"""
    if s0 > 0:
        PRE.append(f'gsap.set("{sel}", {{visibility:"hidden"}});')
        T.append(f'tl.set("{sel}", {{visibility:"visible"}}, {r3(s0)});')
    if s1 < TOTAL:
        T.append(f'tl.set("{sel}", {{visibility:"hidden"}}, {r3(s1)});')


# ---------------------------------------------------------------- avatar (owner's skin)
# A still of the waving host made with blocky_character.py in a 600x600 mini project (recipe in README.md). A live
# CSS-3D character inside the round mask escaped the clip and its scene's visibility window (snapshot 2026-10-27).
AV = 300 if WIDE else 340


def avatar(cid, left, top, size=AV):
    return (f'<div class="avatar" style="left:{left}px;top:{top}px;width:{size}px;height:{size}px;">'
            f'<img id="{cid}" src="{C.get("avatar", "assets/img/avatar.png")}" alt="{C["name"]} avatar" '
            f'style="position:absolute;left:0;top:0;width:100%;height:100%;transform-origin:50% 85%;"></div>')


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
  {avatar("hosta", ax, ay)}
  <div id="h-tag" class="pill" style="position:absolute;{pos}top:{ty - 70}px;text-align:{align};"><span style="background:{RED};color:#fff;font-size:{30 if WIDE else 34}px;padding:6px 18px;border-radius:8px;">{C["tag"]}</span></div>
  <div id="h-name" class="pop" style="position:absolute;{pos}top:{ty}px;font-size:{nsize}px;color:{INK};text-align:{align};white-space:nowrap;"><span class="sb">Hi,&nbsp;I'M&nbsp;</span>{letters}</div>
  <div id="h-role" class="sb" style="position:absolute;{pos}top:{ty + nsize + 22}px;font-size:{40 if WIDE else 46}px;color:{INK};text-align:{align};">{C["role"]}</div>
  <div id="h-btn" style="position:absolute;{pos}top:{ty + nsize + 100}px;text-align:{align};"><span class="pop" style="display:inline-block;background:{RED};color:#fff;font-size:{40 if WIDE else 46}px;padding:10px 34px;border-radius:16px;box-shadow:0 10px 30px rgba(240,25,63,0.35);">View My Work &#8250;</span></div>
</div>''')
# the name types in from 0.15 s; the first 4 letters are already there at 0 s (thumbnail shows a name)
nch = len(name)
TYPE0, TYPED = 0.15, 0.9
PRE.append(f'gsap.set("#h-name .ch", {{opacity:0}}); gsap.set("#h-name .ch:nth-child(-n+5)", {{opacity:1}});')
T.append(f'tl.to("#h-name .ch:nth-child(n+6)", {{opacity:1, duration:0.01, stagger:{r3(TYPED / max(1, nch - 4))}}}, {TYPE0});')
sfx("typing-keyboard-fast", TYPE0 + PEAK["typing-keyboard-fast"], 0.4, d=TYPED + 0.05)
T.append(f'tl.fromTo("#hosta", {{rotation:-3, y:0}}, {{rotation:3, y:-6, duration:{r3(BEAT * 2)}, yoyo:true, repeat:3, ease:"sine.inOut"}}, 0);')
t_tag = next_beat(TYPE0 + TYPED)
t_role, t_btn = r3(t_tag + BEAT), r3(t_tag + 2 * BEAT)
# pops land ON the beat: the back-out scale reaches full size ~0.12 s after it starts
T.append(f'tl.fromTo("#h-tag", {{scale:0, opacity:0}}, {{scale:1, opacity:1, duration:0.35, ease:"back.out(2.2)"}}, {r3(t_tag - 0.06)});')
T.append(f'tl.fromTo("#h-role", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.3}}, {r3(t_role - 0.06)});')
T.append(f'tl.fromTo("#h-btn", {{scale:0, opacity:0}}, {{scale:1, opacity:1, duration:0.35, ease:"back.out(2.4)"}}, {r3(t_btn - 0.06)});')
sfx("pop-high", t_tag, 0.5)
sfx("pluck", t_role, 0.5)
sfx("pop-high", t_btn, 0.5)
t_press = r3(t_btn + 2 * BEAT)
if t_press < T_WANT - 0.3:            # the button "press": scale dip exactly on the click
    T.append(f'tl.to("#h-btn", {{scale:0.92, duration:0.06, yoyo:true, repeat:1, ease:"power2.out"}}, {t_press});')
    sfx("click-1", t_press, 0.6)
T.append(f'tl.to("#s1", {{scale:1.25, opacity:0, filter:"blur(14px)", duration:0.25, ease:"power3.in"}}, {r3(T_WANT - 0.2)});')
sfx("whoosh-fast-0.3s", T_WANT, 0.5)
win("#s1", 0, T_WANT)

# ---------------------------------------------------------------- S2 "Want a video EDITOR?" (T_WANT - DROP)
ws = 120 if WIDE else 116
WW = C.get("want_words", ["Want", "a", "video", "EDITOR?"])
HTML.append(f'''<div id="s2" style="position:absolute;inset:0;">
  <div style="position:absolute;left:0;right:0;top:{H / 2 - (ws if WIDE else ws * 1.6):.0f}px;text-align:center;">
    <span id="w1" class="pop wd" style="font-size:{ws}px;color:{INK};">{WW[0]}</span>
    <span id="w2" class="pop wd" style="font-size:{ws}px;color:{INK};">{WW[1]}</span>
    <span id="w3" class="pop wd" style="font-size:{ws}px;color:{INK};">{WW[2]}</span>{"" if WIDE else "<br>"}
    <span id="w4" class="pop wd" style="font-size:{int(ws * 1.05)}px;color:#fff;background:{RED};padding:0 26px;border-radius:18px;">{WW[3]}</span>
  </div>
</div>''')
for k, n in ((1, -6), (2, -5), (3, -4), (4, -2)):
    t = bt(n)
    # words slam in 0.2 s and land on their beat
    T.append(f'tl.fromTo("#w{k}", {{opacity:0, y:60, scale:1.6}}, {{opacity:1, y:0, scale:1, duration:0.2, ease:"power4.out"}}, {r3(t - 0.12)});')
    if k == 4:
        sfx("impact-punch", t, 0.5)
    else:
        sfx("pluck", t, 0.45)
T.append(f'tl.fromTo("#w4", {{rotation:-4}}, {{rotation:4, duration:0.1, yoyo:true, repeat:4, ease:"none"}}, {r3(bt(-2) + 0.1)});')
T.append(f'tl.to("#s2", {{scale:3, opacity:0, duration:0.3, ease:"power3.in"}}, {r3(DROP - 0.3)});')
sfx("riser-2s", DROP, 0.45)          # rises through the words and the silent beat, peaks on the drop
win("#s2", T_WANT, DROP)

# ---------------------------------------------------------------- S3 montage: one section per brand
if WIDE:
    LAB = dict(left=120, top=44, align="left", cnt=28, nm=88, pill=32)
    AREA_TOP, AREA_BOT, GAP = 236, 936, 50
else:
    LAB = dict(left=0, top=150, align="center", cnt=34, nm=104, pill=38)
    AREA_TOP, AREA_BOT, GAP = 440, 1640, 40
VARIANTS = ["whipL", "zoom", "whipR", "drop", "rise"]
mont = []
for bi, b in enumerate(C["brands"]):
    s0, s1 = brand_t[bi]
    nvid = len(b["clips"])
    lpos = f"left:{LAB['left']}px;" if WIDE else "left:0;right:0;"
    mont.append(f'''<div id="b{bi}" style="position:absolute;{lpos}top:{LAB["top"]}px;text-align:{LAB["align"]};">
    <div id="b{bi}c" class="sb" style="font-size:{LAB["cnt"]}px;color:{GREY};letter-spacing:3px;">CLIENT {bi + 1:02d} / {NB:02d}</div>
    <div class="mask1" data-layout-allow-overflow><div id="b{bi}n" class="anton" style="font-size:{LAB["nm"]}px;color:{INK};line-height:1.05;">{b["client"]}</div></div>
    <div id="b{bi}p" style="margin-top:8px;"><span class="pill" style="background:{RED};color:#fff;font-size:{LAB["pill"]}px;padding:6px 20px;border-radius:10px;">{nvid} video{"s" if nvid > 1 else ""}</span></div>
  </div>''')
    # name lands on the brand's first downbeat (impact there), counter + pill on the next beat
    T.append(f'tl.fromTo("#b{bi}n", {{yPercent:110}}, {{yPercent:0, duration:0.2, ease:"power4.out"}}, {r3(s0 - 0.15)});')
    T.append(f'tl.fromTo("#b{bi}c", {{opacity:0, y:-14}}, {{opacity:1, y:0, duration:0.2}}, {r3(s0 - 0.05)});')
    T.append(f'tl.fromTo("#b{bi}p", {{scale:0}}, {{scale:1, duration:0.3, ease:"back.out(2.4)"}}, {r3(s0 + BEAT - 0.06)});')
    sfx("impact-punch", s0, 0.42)
    sfx("pop-high", r3(s0 + BEAT), 0.4)
    win(f"#b{bi}", r3(s0 - 0.15), r3(s1 - 0.15))
for gi, g in enumerate(GROUPS):
    s0 = g["s0"]
    cl = g["clips"]
    n = len(cl)
    if cl[0]["vert"]:
        bh = AREA_BOT - AREA_TOP - (60 if WIDE else 80)
        if not WIDE and n == 1:
            bh = 1138
        bw = round(bh * 9 / 16)
        if not WIDE and n == 2:
            bw = (W - 3 * GAP) // 2
            bh = round(bw * 16 / 9)
        total_w = n * bw + (n - 1) * GAP
        boxes = [((W - total_w) // 2 + k * (bw + GAP), AREA_TOP, bw, bh) for k in range(n)]
    else:
        bw, bh = BOX_H
        boxes = [((W - bw) // 2, AREA_TOP + (0 if WIDE else 120), bw, bh)]
    cards = []
    v = VARIANTS[gi % len(VARIANTS)]
    for k, (c, (x0, y0, w0, h0)) in enumerate(zip(cl, boxes)):
        rot = (-2, 1.5, -1, 2, -1.5)[(gi + k) % 5]
        cid = f"g{gi}k{k}"
        cards.append(f'''<div id="{cid}" class="card" style="left:{x0}px;top:{y0}px;width:{w0}px;height:{h0}px;transform:rotate({rot}deg);border-radius:{22 if c["vert"] else 18}px;">
      <video id="{cid}v" src="{c["file"]}" data-start="{r3(s0 - 0.15)}" data-duration="{r3(BAR + 0.15)}" muted playsinline style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;"></video></div>
    <div id="{cid}t" class="tapebit" style="left:{x0 + w0 / 2 - 80:.0f}px;top:{y0 - 22}px;transform:rotate({-rot * 2}deg);"></div>
    <div id="{cid}l" class="pill" style="position:absolute;left:{x0 - 40}px;width:{w0 + 80}px;top:{y0 + h0 + 24}px;text-align:center;font-size:{28 if WIDE else 34}px;color:{INK};">{c["type"]}</div>''')
        frm = {"whipL": "{x:-900, filter:'blur(18px)'}", "whipR": "{x:900, filter:'blur(18px)'}",
               "zoom": "{scale:0.3, opacity:0}", "drop": "{y:-900}", "rise": "{y:800}"}[v]
        to = {"whipL": "{x:0, filter:'blur(0px)'", "whipR": "{x:0, filter:'blur(0px)'", "zoom": "{scale:1, opacity:1",
              "drop": "{y:0", "rise": "{y:0"}[v]
        # cards move across the downbeat (0.15 s either side) and settle on it; side-by-side cards follow 0.07 s apart
        st = r3(s0 - 0.15 + 0.07 * k)
        T.append(f'tl.fromTo("#{cid}", {frm}, {to}, duration:0.3, ease:"power3.out"}}, {st});')
        T.append(f'tl.to("#{cid}", {{scale:1.035, duration:{r3(BAR - 0.3)}, ease:"none"}}, {r3(st + 0.3)});')
        T.append(f'tl.fromTo("#{cid}t", {{scaleX:0}}, {{scaleX:1, duration:0.15, ease:"power2.out"}}, {r3(s0 + 0.1)});')
        T.append(f'tl.fromTo("#{cid}l", {{opacity:0, y:16}}, {{opacity:1, y:0, duration:0.25}}, {r3(s0 + BEAT * 0.5)});')
    mont.append(f'<div id="g{gi}" style="position:absolute;inset:0;">' + "\n    ".join(cards) + "</div>")
    sfx("whoosh-fast-0.3s", s0, 0.5 if g["first"] else 0.4)
    win(f"#g{gi}", r3(s0 - 0.15), r3(s0 + BAR))
HTML.append('<div id="s3" style="position:absolute;inset:0;">' + "\n  ".join(mont) + "</div>")
sfx("sub-drop", DROP, 0.4)
sfx("impact-boom", DROP, 0.45)

# ---------------------------------------------------------------- S4 wall: the grid clips at once (2 bars)
G = C["grid"]
cols = 6 if WIDE else 3
gw, ch, gap = (260, 462, 34) if WIDE else (300, 533, 30)
rows = (len(G) + cols - 1) // cols
cells = []
for k, i in enumerate(G):
    c = FLAT[i]
    r_, q = divmod(k, cols)
    x0 = (W - (cols * gw + (cols - 1) * gap)) // 2 + q * (gw + gap)
    y0 = (190 if WIDE else 380) + r_ * (ch + gap)
    cells.append(f'<div id="w{k}c" class="card" style="left:{x0}px;top:{y0}px;width:{gw}px;height:{ch}px;border-radius:14px;">'
                 f'<video id="w{k}v" src="{c["file"]}" data-start="{r3(T_GRID - 0.15)}" data-duration="{r3(2 * BAR + 0.15)}" '
                 f'data-media-start="{r3(BAR - 0.15)}" muted playsinline style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;"></video></div>')
    T.append(f'tl.fromTo("#w{k}c", {{scale:0, rotation:{random.choice([-8, 8])}}}, {{scale:1, rotation:0, duration:0.3, '
             f'ease:"back.out(1.7)"}}, {r3(T_GRID - 0.15 + k * 0.05)});')
gy = (190 if WIDE else 380) + rows * (ch + gap) + 20
HTML.append(f'''<div id="s4" style="position:absolute;inset:0;">{"".join(cells)}
  <div id="w-cap" style="position:absolute;left:0;right:0;top:{gy}px;text-align:center;">
    <span class="anton" style="font-size:{70 if WIDE else 84}px;color:{INK};">{N} VIDEOS</span>
    <span class="anton" style="font-size:{70 if WIDE else 84}px;color:{RED};">&nbsp;&#8226;&nbsp;{NB} BRANDS</span></div>
</div>''')
T.append(f'tl.fromTo("#w-cap", {{opacity:0, scale:1.5}}, {{opacity:1, scale:1, duration:0.2, ease:"power4.out"}}, {r3(T_GRID + BAR - 0.12)});')
sfx("whoosh-fast-0.3s", T_GRID, 0.5)
sfx("riser-2s", T_GRID, 0.35)         # second lift into the wall (half-beat music gap before it)
sfx("impact-punch", r3(T_GRID + BAR), 0.45)
T.append(f'tl.to("#s4", {{scale:0.6, opacity:0, duration:0.25, ease:"power3.in"}}, {r3(T_END - 0.25)});')
sfx("whoosh-fast-0.3s", T_END - 0.05, 0.5)
win("#s4", r3(T_GRID - 0.15), T_END)

# ---------------------------------------------------------------- S4b policy scenes (one per voice line)
# scene config: {"kicker": small grey line, "big": [lines], "stamp": red stamp text, "mark": "check"|"cross"|"play"|"",
#                "chips": [..] (pop one per beat), "price": "1", "unit": "/ second", "note": small line}
K = 1.0 if WIDE else 1.08


def mark(kind, size):
    if kind == "check":
        inner = (f'<span style="position:absolute;left:{size * .30:.0f}px;top:{size * .18:.0f}px;width:{size * .26:.0f}px;height:{size * .48:.0f}px;'
                 f'border-right:{size * .11:.0f}px solid #fff;border-bottom:{size * .11:.0f}px solid #fff;transform:rotate(45deg);"></span>')
        bg = "#1fa45a"
    elif kind == "cross":
        bar = lambda r: (f'<span style="position:absolute;left:{size * .18:.0f}px;top:{size * .445:.0f}px;width:{size * .64:.0f}px;height:{size * .11:.0f}px;'
                         f'background:#fff;border-radius:4px;transform:rotate({r}deg);"></span>')
        inner, bg = bar(45) + bar(-45), RED
    else:                            # a plain play button (the owner's channel), not a logo
        inner = (f'<span style="position:absolute;left:{size * .40:.0f}px;top:{size * .27:.0f}px;width:0;height:0;border-top:{size * .23:.0f}px solid transparent;'
                 f'border-bottom:{size * .23:.0f}px solid transparent;border-left:{size * .36:.0f}px solid #fff;"></span>')
        bg = RED
    rad = "22%" if kind == "play" else "50%"
    return (f'<span class="mk" style="display:inline-block;position:relative;vertical-align:middle;width:{size}px;height:{size}px;'
            f'border-radius:{rad};background:{bg};box-shadow:0 10px 26px rgba(0,0,0,0.25);">{inner}</span>')


for pi, (s0, s1, li, pc) in enumerate(POL):
    pid = f"p{pi}"
    parts = []
    if pc.get("kicker"):
        parts.append(f'<div id="{pid}k" class="sb" style="font-size:{int(38 * K)}px;color:{GREY};letter-spacing:4px;">{pc["kicker"]}</div>')
    if pc.get("mark"):
        parts.append(f'<div id="{pid}m" style="margin:14px 0;">{mark(pc["mark"], int(150 * K))}</div>')
    for bi_, line in enumerate(pc.get("big", [])):
        parts.append(f'<div class="mask1" data-layout-allow-overflow><div id="{pid}b{bi_}" class="anton" style="font-size:{int(pc.get("big_size", 120) * K)}px;'
                     f'color:{INK};line-height:1.08;white-space:nowrap;">{line}</div></div>')
    if pc.get("price"):
        parts.append(f'<div id="{pid}pr" style="white-space:nowrap;"><span class="anton" style="font-size:{int(300 * K)}px;color:{RED};line-height:1;">{pc["price"]}</span>'
                     f'<span class="pop" style="font-size:{int(70 * K)}px;color:{INK};margin-left:18px;">{pc.get("unit", "")}</span></div>')
    if pc.get("chips"):
        chips = "".join(f'<span id="{pid}c{k}" class="pill chip">{c}</span>' for k, c in enumerate(pc["chips"]))
        parts.append(f'<div style="margin-top:22px;">{chips}</div>')
    if pc.get("stamp"):
        parts.append(f'<div style="margin-top:28px;"><span id="{pid}s" class="pop stamp" style="font-size:{int(76 * K)}px;">{pc["stamp"]}</span></div>')
    if pc.get("note"):
        parts.append(f'<div id="{pid}n" class="sb" style="font-size:{int(40 * K)}px;color:{INK};margin-top:26px;">{pc["note"]}</div>')
    HTML.append(f'<div id="{pid}" style="position:absolute;left:0;right:0;top:0;height:{H}px;display:flex;flex-direction:column;'
                f'align-items:center;justify-content:center;text-align:center;">{"".join(parts)}</div>')
    # build-up: kicker on the scene's first beat, then each element on the next beat (pop SFX on its beat)
    t = s0
    sfx("whoosh-up-0.6s", s0, 0.4)
    if pc.get("kicker"):
        T.append(f'tl.fromTo("#{pid}k", {{opacity:0, y:-20}}, {{opacity:1, y:0, duration:0.25}}, {r3(t - 0.08)});')
    if pc.get("mark"):
        T.append(f'tl.fromTo("#{pid}m", {{scale:0, rotation:-25}}, {{scale:1, rotation:0, duration:0.35, ease:"back.out(2.4)"}}, {r3(t - 0.06)});')
        sfx("pop-high", t, 0.45)
    for bi_ in range(len(pc.get("big", []))):
        t = r3(t + BEAT)
        T.append(f'tl.fromTo("#{pid}b{bi_}", {{yPercent:110}}, {{yPercent:0, duration:0.22, ease:"power4.out"}}, {r3(t - 0.15)});')
        sfx("swish-1", t, 0.35)
    if pc.get("price"):
        t = r3(t + BEAT)
        T.append(f'tl.fromTo("#{pid}pr", {{scale:2.2, opacity:0}}, {{scale:1, opacity:1, duration:0.25, ease:"power4.out"}}, {r3(t - 0.15)});')
        sfx("impact-punch", t, 0.45)
    for k in range(len(pc.get("chips", []))):
        t = r3(t + BEAT)
        T.append(f'tl.fromTo("#{pid}c{k}", {{scale:0, opacity:0}}, {{scale:1, opacity:1, duration:0.3, ease:"back.out(2.4)"}}, {r3(t - 0.06)});')
        sfx("pluck", t, 0.4)
    if pc.get("stamp"):
        # the stamp slams in about where the voice says it (scene start + 55 % of the line), on a beat
        t = max(r3(t + BEAT), next_beat(s0 + 0.2 + 0.55 * VLEN[li]))
        T.append(f'tl.fromTo("#{pid}s", {{scale:2.6, opacity:0, rotation:-14}}, {{scale:1, opacity:1, rotation:-5, duration:0.2, ease:"power4.in"}}, {r3(t - 0.2)});')
        T.append(f'tl.fromTo("#{pid}", {{x:0}}, {{x:-10, duration:0.05, yoyo:true, repeat:4, ease:"none"}}, {t});')
        sfx("impact-boom", t, 0.4)
    if pc.get("note"):
        t = r3(t + BEAT)
        T.append(f'tl.fromTo("#{pid}n", {{opacity:0, y:20}}, {{opacity:1, y:0, duration:0.3}}, {r3(t - 0.1)});')
    T.append(f'tl.to("#{pid}", {{scale:1.15, opacity:0, filter:"blur(10px)", duration:0.22, ease:"power3.in"}}, {r3(s1 - 0.22)});')
    win(f"#{pid}", r3(s0 - 0.1), s1)

# ---------------------------------------------------------------- S5 contact end card
rows_html = []
for k, (lab, val, col) in enumerate(C["contacts"]):
    rows_html.append(f'<div id="c{k}" class="crow"><span class="cdot" style="background:{col};"></span>'
                     f'<span class="sb" style="color:{GREY};">{lab}</span><span class="pop" style="color:{INK};">{val}</span></div>')
if WIDE:
    ex, ey, cl_ = 250, 300, 720
    end_head = f'''{avatar("hostb", ex, ey - 20)}
  <div id="e-name" class="anton" style="position:absolute;left:{ex - 60}px;top:{ey + AV + 10}px;width:{AV + 120}px;text-align:center;font-size:62px;color:{INK};">{name}</div>
  <div id="e-role" class="sb" style="position:absolute;left:{ex - 60}px;top:{ey + AV + 95}px;width:{AV + 120}px;text-align:center;font-size:34px;color:{GREY};">{C["role"]}</div>'''
    cpos = f"left:{cl_}px;top:190px;"
else:
    end_head = f'''{avatar("hostb", (W - AV) // 2, 230)}
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
T.append(f'tl.fromTo("#hostb", {{scale:0.6, rotation:-10}}, {{scale:1, rotation:0, duration:0.4, ease:"back.out(2)"}}, {r3(T_C - 0.1)});')
T.append(f'tl.to("#hostb", {{rotation:3, y:-6, duration:{r3(BEAT * 2)}, yoyo:true, repeat:7, ease:"sine.inOut"}}, {r3(T_C + 0.4)});')
T.append(f'tl.fromTo("#e-cta", {{scale:0, opacity:0}}, {{scale:1, opacity:1, duration:0.35, ease:"back.out(2.2)"}}, {r3(T_C - 0.06)});')
T.append(f'tl.fromTo("#e-name", {{opacity:0, y:30}}, {{opacity:1, y:0, duration:0.25}}, {r3(T_C + BEAT - 0.1)});')
T.append(f'tl.fromTo("#e-sub", {{opacity:0, x:-30}}, {{opacity:1, x:0, duration:0.25}}, {r3(T_C + BEAT - 0.1)});')
T.append(f'tl.fromTo("#e-role", {{opacity:0}}, {{opacity:1, duration:0.25}}, {r3(T_C + 2 * BEAT - 0.1)});')
sfx("impact-punch", T_C, 0.42)
sfx("pop-high", r3(T_C + BEAT), 0.4)
nc = len(C["contacts"])
for k in range(nc):
    t = r3(T_C + (2 + k) * BEAT)
    T.append(f'tl.fromTo("#c{k}", {{opacity:0, x:{-60 if WIDE else 0}, y:{0 if WIDE else 30}}}, {{opacity:1, x:0, y:0, duration:0.2, ease:"power3.out"}}, {r3(t - 0.08)});')
    sfx("pluck", t, 0.4)
t_last = r3(T_C + (2 + nc) * BEAT)
sfx("sparkle", t_last, 0.3)
T.append(f'tl.to("#e-cta", {{scale:1.06, duration:{r3(BEAT)}, yoyo:true, repeat:5, ease:"sine.inOut"}}, {t_last});')
win("#s5", r3(T_C - 0.1), TOTAL + 1)

# grain over everything (soft-light, own overlay from library/stock, looped by repeated clips)
grain = []
k, t = 0, 0.0
while t < TOTAL:
    grain.append(f'<video id="gr{k}" src="assets/clips/grain.mp4" data-start="{r3(t)}" data-duration="{r3(min(6.0, TOTAL - t))}" muted playsinline '
                 f'style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;mix-blend-mode:soft-light;opacity:0.35;"></video>')
    t += 6.0
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
.mask1 {{ overflow:hidden; }}
.wd {{ display:inline-block; margin:0 10px; }}
.avatar {{ position:absolute; border-radius:50%; overflow:hidden; background:radial-gradient(circle at 50% 35%, #3a3a3a, #0d0d0d 70%);
          box-shadow:0 0 0 8px rgba(255,255,255,0.9), 0 18px 40px rgba(0,0,0,0.35); }}
.card {{ position:absolute; overflow:hidden; background:#111; box-shadow:0 0 0 8px #fff, 0 26px 60px rgba(0,0,0,0.38); }}
.tapebit {{ position:absolute; width:160px; height:42px; background:rgba(240,25,63,0.85); transform-origin:50% 50%; }}
.tape {{ position:absolute; width:0; height:0; }}
.crow {{ display:flex; align-items:center; gap:18px; font-size:{40 if WIDE else 44}px; margin:12px 0; white-space:nowrap; }}
.cdot {{ width:22px; height:22px; border-radius:50%; flex:none; }}
.chip {{ display:inline-block; margin:8px 10px; padding:10px 28px; border-radius:14px; background:#fff; color:{INK}; font-size:{int(46 * K)}px;
        box-shadow:0 8px 22px rgba(0,0,0,0.18); border:3px solid {INK}; }}
.stamp {{ display:inline-block; color:{RED}; border:8px solid {RED}; border-radius:16px; padding:4px 30px; letter-spacing:2px;
         background:rgba(255,255,255,0.6); transform:rotate(-5deg); }}
"""
# hook gaps (owner, 2026-10-27: "music me jan dallo ... hook bana rahay"): the music drops out for the beat before the
# montage drop and the half beat before the wall, so the riser + impact land in silence (20 ms ramps, no clicks)
GAPS = [(r3(DROP - BEAT), DROP), (r3(T_GRID - BEAT / 2), T_GRID)] if C.get("hook_gaps", True) else []
vol = "*".join(f"(1-between(t,{g0},{g1})*min(1,min(t-{g0},{g1}-t)/0.02))" for g0, g1 in GAPS) or "1"
if VO:
    # fit the track so its drop lands on DROP and it ends (fade) at TOTAL, then place the lines and mix with ducking
    T_ = f"{REPO}/library/tools"
    PV = "/home/user/tools/perc-venv/bin/python"
    subprocess.run([PV, f"{T_}/music_fit.py", VO["music_src"], "assets/music/music.wav", "--length", str(TOTAL), "--drop-at", str(DROP),
                    "--src-drop", str(VO["src_drop"]), "--end", "fade", "--fade", "2.5"], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "assets/music/music.wav", "-af", f"volume='{vol}':eval=frame", "assets/music/music_gap.wav"], check=True)
    import numpy as np
    SR = 48000
    vo = np.zeros((int((TOTAL + 1) * SR), 2), np.float32)
    for li, t0 in VOAT:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", VO["parts"][li], "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                             capture_output=True, check=True).stdout
        x = np.frombuffer(raw, np.float32).reshape(-1, 2)
        i0 = int(t0 * SR)
        vo[i0:i0 + len(x)] += x[:len(vo) - i0]
    os.makedirs("assets/vo", exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "assets/vo/vo_placed.wav"],
                   input=vo.tobytes(), check=True)
    subprocess.run([PV, f"{T_}/mix_vo_music.py", "assets/vo/vo_placed.wav", "assets/music/music_gap.wav", "assets/music/mix.wav",
                    "--lufs", "-16"], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "assets/music/mix.wav", "-t", str(TOTAL), "-c:a", "libmp3lame", "-q:a", "2",
                    "assets/music/music_hook.mp3"], check=True)
else:
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "assets/music/music.mp3", "-af", f"volume='{vol}':eval=frame",
                    "-c:a", "libmp3lame", "-q:a", "2", "assets/music/music_hook.mp3"], check=True)
music_d = dur("assets/music/music_hook.mp3")
audio = [f'<audio id="music" src="assets/music/music_hook.mp3" data-start="0" data-duration="{min(TOTAL, music_d)}" '
         f'data-volume="{1.0 if VO else C.get("music_volume", 0.8)}" data-track-index="1" data-fade-out="{0.5 if VO else 1.5}"></audio>']
lanes = []                            # greedy lane per sfx so overlapping clips never share a track (lint)
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
json.dump({"total": TOTAL, "drop": DROP, "bar": BAR, "want": T_WANT, "groups": [[g["s0"], C["brands"][g["brand"]]["client"],
          [c["type"] for c in g["clips"]]] for g in GROUPS], "wall": [T_GRID, T_END], "end": T_C, "policy": [p[:3] for p in POL], "vo_at": VOAT,
           "sfx": sorted([(round(s + PEAK[f], 3), f) for f, s, v, d in A])}, open("timing.json", "w"), indent=1)
print(f"built {a.format}: {TOTAL} s, {N} clips in {NG} bars, {NB} brands, {len(T)} tweens, {len(A)} sfx")
