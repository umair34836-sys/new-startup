# "GTA 5 FOR ANDROID UNDER 10 MB?!" (Mr Aloo), 16:9 1920x1080. Client VO (retakes cut, 1.15x, owner's choice), client
# editing guide scenes 1-6 (library/clients/mraloo/projects/gta5-under-10mb/editing-guide.txt). Every shot starts on the
# VO word it illustrates (words.json = Whisper medium on the final VO clock). GTA gameplay is not here yet (asked the
# client): gp() draws a labelled placeholder slot that becomes the client's clip later.
import json, os, subprocess, sys

UNTIL = float(sys.argv[1]) if len(sys.argv) > 1 else 1e9
W = json.load(open("words.json"))
from captions import CAP
VO_END = W[-1][1]
TOTAL = round(min(VO_END + 1.6, UNTIL + 0.5), 2)
MUSIC_VOL = 0.32
HITS = json.load(open("sfx_hits.json"))

BG, INK, PINK, ORANGE, GREEN, RED, CYAN, WHITE = "#140c24", "#0b0614", "#ff2e88", "#ffb020", "#2bd96b", "#ff3b3b", "#35d6ff", "#ffffff"


def ws(i):
    return W[i][0]


def we(i):
    return W[i][1]


def T(i):              # a shot cuts in just before its word
    return round(ws(i) - 0.08, 3)


def o(d):              # python dict -> JS object literal
    return "{ " + ", ".join(f"{k}: {json.dumps(v)}" for k, v in d.items()) + " }"


def ft(sel, a, b, t):
    return f'    tl.fromTo("{sel}", {o(a)}, {o(b)}, {t:.3f});'


def slam(sel, t, s=2.2, r=0):
    return ft(sel, dict(opacity=0, scale=s, rotation=r), dict(opacity=1, scale=1, rotation=0, duration=0.26, ease="back.out(2)"), t - 0.05)


def pop(sel, t, d=0.3):
    return ft(sel, dict(opacity=0, scale=0.2), dict(opacity=1, scale=1, duration=d, ease="back.out(2.4)"), t - 0.05)


def slide(sel, t, x=0, y=0, d=0.35):
    return ft(sel, dict(opacity=0, x=x, y=y), dict(opacity=1, x=0, y=0, duration=d, ease="power3.out"), t - 0.08)


def shake(sel, t, amp=16):   # even repeat: ends at rest (CLAUDE.md yoyo learning)
    return ft(sel, dict(x=-amp, y=amp // 2), dict(x=0, y=0, duration=0.05, repeat=4, yoyo=True, immediateRender=False), t)


def em(name, size, extra=""):
    return f'<img src="assets/el/{name}.png" style="width:{size}px;height:{size}px;{extra}" alt="">'


def txt(tid, s, size, color=WHITE, extra="", font="Anton"):
    return (f'<div id="{tid}" class="stroke" style="font-family:{font};font-size:{size}px;line-height:1.02;color:{color};'
            f'font-weight:800;opacity:0;{extra}">{s}</div>')


def center(inner, top=0, bottom=0, gap=30, col=True):
    return (f'<div style="position:absolute;left:80px;right:80px;top:{top}px;bottom:{bottom}px;display:flex;'
            f'flex-direction:{"column" if col else "row"};align-items:center;justify-content:center;gap:{gap}px;text-align:center;">{inner}</div>')


GP = []                # gameplay slots for the client's clips: (shot id, start, end, what the guide asks for)


GPF = "../gp_in/gta_gameplay.mp4"     # client's GTA 5 recording (Drive 1nZX4fI3_pHjqgs6-Ci4jE8YZxzBV5fSI), 1280x720 60 fps
# slot -> source in-point (s), picked from contact sheets (look/gp_sheet_*.jpg, every 4 s). Only Franklin is in the recording:
# the Michael / Trevor lines get a city / dramatic shot, never another character passed off as them; no blood shots.
GP_SRC = {"fast action / driving": 37.0, "phone / action": 140.0, "city / driving": 64.0, "in phone": 220.0,
          "cool character shot": 0.5, "same shot, freeze": None, "Los Santos city wide": 16.0, "Los Santos skyline": 20.0,
          "Franklin shot": 118.5, "Michael shot": 384.0, "Trevor shot": 196.0, "massive open world, wide / aerial": 164.0,
          "PC gameplay": 356.0, "gameplay, dramatic": 260.0, "gameplay: police chase": 296.0}
FREEZE_AT = 6.0
# montage on "city, cars, buildings, missions, characters": one source shot per spoken word
MONTAGE = [(437, 76.0), (439, 40.0), (440, 80.5), (441, 148.0), (442, 88.5), (443, 228.0), (444, 136.0), (448, 208.0)]
CUR = [0.0, 0.0]
DRY = [False]     # pre-pass: no clip cutting


def gp_clip(src, dur, tag):
    out = f"assets/gp/{tag}_{src:.2f}_{dur:.2f}.mp4"
    if not os.path.exists(out):
        os.makedirs("assets/gp", exist_ok=True)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{src:.3f}", "-t", f"{dur + 0.1:.3f}", "-i", GPF, "-an",
                        "-vf", "scale=1920:1080:flags=lanczos,cas=strength=0.5,fps=30", "-c:v", "libx264", "-crf", "17",
                        "-preset", "veryfast", "-pix_fmt", "yuv420p", out], check=True)
    return out


def montage_clip(a, b):
    out = f"assets/gp/montage_{a:.2f}_{b:.2f}.mp4"
    if not os.path.exists(out):
        cuts = [a] + [ws(wi) - 0.05 for wi, _ in MONTAGE[1:]] + [b]
        parts = []
        for n, (_, src) in enumerate(MONTAGE):
            parts.append(gp_clip(src, max(0.2, cuts[n + 1] - cuts[n]), f"m{n}"))
        lst = "assets/gp/montage.txt"
        open(lst, "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in parts))
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c:v", "libx264", "-crf", "17",
                        "-preset", "veryfast", "-pix_fmt", "yuv420p", "-t", f"{b - a:.3f}", out], check=True)
    return out


def gp(k, desc, dim=0.0, blur=0):
    """client gameplay for a slot (GP_SRC), cut to the shot length; dim = darken under text"""
    GP.append((k, desc))
    a, b = CUR
    if DRY[0]:
        return f'<div id="g{k}"></div>'
    f = f"filter:brightness({1 - dim});" if dim else ""
    d = round(max(0.3, b - a), 3)
    if desc.startswith("city / cars"):
        src = montage_clip(a, b)
    elif desc == "same shot, freeze":
        src = None
        img = f"assets/gp/freeze_{FREEZE_AT}.jpg"
        if not os.path.exists(img):
            os.makedirs("assets/gp", exist_ok=True)
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(FREEZE_AT), "-i", GPF, "-frames:v", "1", "-vf",
                            "scale=1920:1080:flags=lanczos,hue=s=0", "-q:v", "2", img], check=True)
        return f'<div id="g{k}" style="position:absolute;inset:-60px;{f}"><img src="{img}" style="position:absolute;inset:60px;width:1920px;height:1080px;" alt=""></div>'
    else:
        src = gp_clip(GP_SRC[desc], d, "c")
    return (f'<div id="g{k}" style="position:absolute;inset:-60px;{f}"><video id="gv{k}" src="{src}" data-start="{a}" data-duration="{d}" muted playsinline '
            f'style="position:absolute;left:60px;top:60px;width:1920px;height:1080px;object-fit:cover;"></video></div>')


# client 2026-10-28: "thora sa AI jaisa lag raha hai" -> design shots sit on real footage instead of a flat purple card:
# dimmed client GTA gameplay (rotating driving shots), or real phone b-roll (Mixkit Free License, no credit) on phone lines
BG_GP = [44.0, 60.0, 72.0, 168.0, 208.0, 216.0, 232.0, 244.0, 284.0, 308.0, 348.0, 364.0, 376.0, 388.0]
BROLL = {"s_apk": ("mixkit_4915", 1.0), "s_install": ("mixkit_4915", 5.0), "s_sure": ("mixkit_144", 2.0), "s_perms": ("mixkit_4915", 8.0),
         "s_rules": ("mixkit_144", 7.0), "s_tips": ("mixkit_4915", 2.0), "s_legit": ("mixkit_4915", 10.0), "s_dimaag": ("mixkit_144", 0.0),
         "s_atrisk": ("mixkit_4915", 4.0), "s_sub": ("mixkit_144", 9.0), "s_final": ("mixkit_4915", 0.0)}
CURFN = [""]
_bgn = [0]


def bg_clip(src_file, src, dur, tag):
    out = f"assets/bgclips/{tag}_{src:.2f}_{dur:.2f}.mp4"
    if not os.path.exists(out):
        os.makedirs("assets/bgclips", exist_ok=True)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-stream_loop", "-1", "-ss", f"{src:.3f}", "-i", src_file, "-an", "-t", f"{dur + 0.1:.3f}",
                        "-vf", "scale=1920:1080:flags=lanczos,fps=30", "-c:v", "libx264", "-crf", "20", "-preset", "veryfast",
                        "-pix_fmt", "yuv420p", out], check=True)
    return out


def dark(extra=""):
    a, b = CUR
    d = round(max(0.3, b - a), 3)
    _bgn[0] += 1
    vid = ""
    if not DRY[0]:
        if CURFN[0] in BROLL:
            f, src = BROLL[CURFN[0]]
            p = bg_clip(f"assets/broll/{f}.mp4", src, d, f); bri = 0.62
        else:
            src = BG_GP[_bgn[0] % len(BG_GP)]
            p = bg_clip(GPF, src, d, "gpbg"); bri = 0.55
        vid = (f'<div style="position:absolute;inset:0;filter:brightness({bri}) saturate(0.85);"><video id="bgv{_bgn[0]}" src="{p}" data-start="{a}" data-duration="{d}" '
               f'muted playsinline style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;"></video></div>')
    return (vid + f'<div style="position:absolute;inset:0;background:linear-gradient(160deg, rgba(43,20,64,0.30) 0%, rgba(20,12,36,0.55) 80%);"></div>'
            f'<div style="position:absolute;inset:0;background:repeating-linear-gradient(0deg, rgba(255,255,255,0.03) 0 2px, transparent 2px 5px);"></div>{extra}')


def veil():
    return '<div style="position:absolute;inset:0;background:linear-gradient(180deg, rgba(10,5,20,0.25) 0%, rgba(10,5,20,0.55) 100%);"></div>'


def phone(pid, inner, left=700, top=70, w=520, h=930):
    return (f'<div id="{pid}" style="position:absolute;left:{left}px;top:{top}px;width:{w}px;height:{h}px;border-radius:64px;background:#05030a;'
            f'border:6px solid #3a3150;box-shadow:0 30px 90px rgba(0,0,0,0.6), 0 0 0 3px #0d0a16;opacity:0;">'
            f'<div style="position:absolute;left:18px;right:18px;top:18px;bottom:18px;border-radius:48px;overflow:hidden;background:#101018;">{inner}</div>'
            f'<div style="position:absolute;left:50%;top:30px;width:110px;height:28px;margin-left:-55px;border-radius:14px;background:#05030a;"></div></div>')


def bar(bid, label, w=1100, color=GREEN):
    return (f'<div style="width:{w}px;"><div id="{bid}l" style="font-family:Jakarta;font-weight:800;font-size:44px;color:#fff;text-align:left;margin-bottom:14px;opacity:0;">{label}</div>'
            f'<div style="height:54px;border-radius:27px;background:rgba(255,255,255,0.12);border:3px solid rgba(255,255,255,0.4);overflow:hidden;">'
            f'<div id="{bid}" style="height:100%;width:100%;background:linear-gradient(90deg,{color},#b6ff6a);transform-origin:0 50%;transform:scaleX(0);"></div></div></div>')


# ----------------------------------------------------------------------------------------------- recording clips
def rec_clip(name, src0, src1, dur):
    """cut the client's Google search recording (cropped to the page) and time-fit it to the shot"""
    out = f"assets/rec/{name}_{src0}_{src1}_{dur:.2f}.mp4"
    if not os.path.exists(out):
        sp = (src1 - src0) / dur
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(src0), "-t", str(src1 - src0), "-i", "assets/rec/search.mp4", "-an",
                        "-vf", f"setpts=PTS/{sp:.4f},fps=30", "-t", f"{dur:.3f}", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", out], check=True)
    return out


def rec_still(name, t):
    out = f"assets/rec/{name}.jpg"
    if not os.path.exists(out):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", "assets/rec/search.mp4", "-frames:v", "1", "-q:v", "2", out], check=True)
    return out


# ----------------------------------------------------------------------------------------------- shots
# (start word, builder). Each shot runs until the next one starts; bumpers are the VO's own spoken headings.
SH, SFX = [], []


def shot(i, fn, t=None):
    SH.append((T(i) if t is None else t, fn))


HEADS = [(261, 264, "NOW THE INSTALLATION TRAP", "SCENE 3"), (417, 421, "10 MB GTA 5 DOESN'T MAKE SENSE", "SCENE 4"),
         (565, 568, "HOW TO STAY SAFE", "SCENE 5")]


# Scene 1 - hook (guide: start straight on gameplay, big "GTA 5 IN JUST 10 MB?!", fake 10 MB download bar,
# scam reveal = music stops + record scratch + quick zoom + red text)
def s_hook(k, a, b):
    h = gp(k, "fast action / driving", dim=0.15) + veil() + (
        f'<div id="s{k}t" style="position:absolute;left:90px;top:300px;">'
        f'<div class="stroke" style="font-family:Anton;font-size:150px;line-height:0.95;color:#fff;">GTA 5 FOR ANDROID</div>'
        f'<div class="stroke" style="font-family:Anton;font-size:190px;line-height:0.95;color:{ORANGE};">UNDER 10 MB?!</div></div>')
    j = [ft(f"#s{k}t", dict(scale=1), dict(scale=1.06, duration=b - a, ease="none"), 0)]
    return h, j, [("sub-drop", 0.02, 0.5), ("whoosh-fast-0.3s", 0.05, 0.4)]


def s_10mb(k, a, b):
    h = gp(k, "phone / action", dim=0.45, blur=6) + center(
        txt(f"s{k}a", "GTA 5 IN JUST", 120) + txt(f"s{k}b", "10 MB?!", 260, ORANGE) + bar(f"s{k}p", "Downloading... 10 MB"), bottom=150, gap=20)
    j = [slam(f"#s{k}a", ws(17)), slam(f"#s{k}b", ws(18), 3, -6), shake(f"#s{k}b", ws(18) + 0.22),
         ft(f"#s{k}pl", dict(opacity=0), dict(opacity=1, duration=0.2), ws(20)),
         ft(f"#s{k}p", dict(scaleX=0), dict(scaleX=1, duration=we(24) - ws(20), ease="power1.inOut"), ws(20))]
    return h, j, [("impact-punch", ws(18), 0.4), ("game-coin", we(24), 0.35)]


def s_na(k, a, b):
    rows = [(32, "100 GB STORAGE TENSION"), (38, "GAMING PC"), (43, "EXPENSIVE LAPTOP")]
    inner = "".join(f'<div id="s{k}r{r}" style="display:flex;align-items:center;gap:36px;opacity:0;">{em("cross_mark", 120)}'
                    f'<div class="stroke" style="font-family:Anton;font-size:120px;color:{WHITE if r % 2 == 0 else ORANGE};white-space:nowrap;">NA {t}</div></div>'
                    for r, (_, t) in enumerate(rows))
    h = gp(k, "city / driving", dim=0.5, blur=8) + center(inner, bottom=120, gap=40)
    j, s = [], []
    for r, (wi, _) in enumerate(rows):
        j += [slam(f"#s{k}r{r}", ws(wi), 1.8, -4 if r % 2 else 4)]
        s.append(("impact-punch", ws(wi), 0.3))
    return h, j, s


def s_pocket(k, a, b):
    scr = (f'<div id="s{k}dl" style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:24px;background:#141420;">'
           f'{em("package", 150)}<div style="font-family:Jakarta;font-weight:800;font-size:40px;color:#fff;">10 MB</div>'
           f'<div style="width:330px;height:22px;border-radius:11px;background:#2a2a3a;overflow:hidden;"><div id="s{k}pb" style="height:100%;background:{GREEN};transform-origin:0 50%;transform:scaleX(0);"></div></div>'
           f'<div id="s{k}in" style="padding:16px 56px;border-radius:40px;background:{GREEN};font-family:Jakarta;font-weight:800;font-size:40px;color:#0b2a14;opacity:0;">INSTALL</div></div>'
           f'<div id="s{k}gs" style="position:absolute;inset:0;opacity:0;">{gp(f"{k}p", "in phone")}</div>')
    h = dark() + phone(f"s{k}ph", scr, left=1180, top=75, w=520, h=930) + (
        f'<div style="position:absolute;left:110px;top:300px;width:1000px;">{txt(f"s{k}a", "LOS SANTOS", 190, ORANGE)}{txt(f"s{k}b", "TUMHARI JEB MEIN!", 110)}</div>')
    j = [slide(f"#s{k}ph", a + 0.05, y=500, d=0.45),
         ft(f"#s{k}pb", dict(scaleX=0), dict(scaleX=1, duration=we(52) - ws(49), ease="power1.inOut"), ws(49)),
         pop(f"#s{k}in", ws(53)), ft(f"#s{k}in", dict(scale=1), dict(scale=0.88, duration=0.08, yoyo=True, repeat=1, immediateRender=False), ws(54)),
         ft(f"#s{k}gs", dict(opacity=0, scale=1.4), dict(opacity=1, scale=1, duration=0.35, ease="power3.out"), ws(56) - 0.1),
         slam(f"#s{k}a", ws(56)), slam(f"#s{k}b", ws(58), 1.6)]
    return h, j, [("pop-high", ws(53), 0.4), ("mouse-click", ws(54), 0.8), ("sparkle", ws(56), 0.35)]


def s_secret(k, a, b):
    h = gp(k, "cool character shot", dim=0.3) + veil() + center(em("face_with_monocle", 200) + txt(f"s{k}a", "AAJ KA SECRET...", 140, ORANGE), top=0, bottom=200)
    return h, [slam(f"#s{k}a", ws(66)), ft(f"#g{k}", dict(scale=1), dict(scale=1.12, duration=b - a, ease="none"), a)], [("whoosh-fast-0.3s", ws(66), 0.35)]


def s_lekin(k, a, b):   # guide: dramatic music stops; the bed has silence here (mood_bed.py)
    h = gp(k, "same shot, freeze", dim=0.55) + '' + center(
        txt(f"s{k}a", "LEKIN BHAI...", 150) + txt(f"s{k}b", "EK CHHOTI SI PROBLEM HAI", 110, ORANGE), bottom=150, gap=20)
    return h, [slide(f"#s{k}a", ws(70), y=40), slide(f"#s{k}b", ws(72), y=40)], [("tape-stop", ws(70), 0.5), ("riser-2s", ws(77), 0.3)]


def s_scam(k, a, b):
    h = (f'<div style="position:absolute;inset:0;background:linear-gradient(160deg, #7a0b0b 0%, #1a0306 75%);"></div>'
         + center(em("police_light", 180) + txt(f"s{k}a", "TUMHARE SAATH", 140) + txt(f"s{k}b", "SCAM HO RAHA HAI!", 200, RED, "-webkit-text-stroke-color:#fff;"), bottom=150, gap=10)
         + f'<div id="s{k}f" style="position:absolute;inset:0;background:#fff;opacity:0;"></div>')
    j = [ft(f"#s{k}f", dict(opacity=0.8), dict(opacity=0, duration=0.25), a), ft(f"#s{k}c", dict(scale=1.25), dict(scale=1, duration=0.3, ease="power4.out"), a),
         slam(f"#s{k}a", ws(77)), slam(f"#s{k}b", ws(79), 3.2, 5), shake(f"#s{k}c", ws(79) + 0.2, 22)]
    return h, j, [("record-scratch", a + 0.05, 0.6), ("impact-boom", ws(79), 0.45)]


def s_apk(k, a, b):
    h = dark() + center(f'<div style="display:flex;align-items:center;gap:60px;">'
                        f'<div id="s{k}a" style="opacity:0;display:flex;flex-direction:column;align-items:center;">{em("package", 260)}'
                        f'<div class="stroke" style="font-family:Anton;font-size:90px;color:#fff;">RANDOM .APK</div></div>'
                        f'<div id="s{k}q" class="stroke" style="font-family:Anton;font-size:240px;color:{ORANGE};opacity:0;">?</div>'
                        f'<div id="s{k}b" style="opacity:0;display:flex;flex-direction:column;align-items:center;">{em("anxious", 260)}'
                        f'<div class="stroke" style="font-family:Anton;font-size:90px;color:{RED};">TENSION ZAROOR!</div></div></div>'
                        + txt(f"s{k}g", "GTA 5 MILE YA NA MILE...", 90, WHITE), bottom=150)
    j = [pop(f"#s{k}a", ws(90)), pop(f"#s{k}q", ws(96)), slide(f"#s{k}g", ws(96), y=40), slam(f"#s{k}b", ws(104))]
    return h, j, [("pop-high", ws(90), 0.4), ("negative", ws(104), 0.3)]


# Scene 2 - fake tutorial: the client's own Google search recording, cropped to the page
def s_google(k, a, b):
    d = round(b - a, 3)
    src = rec_clip(f"r{k}", 0.0, 10.8, d)
    h = (f'<div id="s{k}v" style="position:absolute;inset:0;"><video id="v{k}" src="{src}" data-start="{a}" data-duration="{d}" muted playsinline '
         f'style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;"></video></div>'
         f'<div id="s{k}q" style="position:absolute;left:260px;right:260px;top:690px;padding:26px 44px;border-radius:60px;background:#fff;display:flex;align-items:center;gap:26px;'
         f'box-shadow:0 20px 60px rgba(0,0,0,0.6);opacity:0;">{em("magnifying_glass", 70)}'
         + "".join(f'<span id="s{k}w{n}" style="font-family:Jakarta;font-weight:800;font-size:58px;color:#202124;opacity:0;">{w}</span>'
                   for n, w in enumerate(["GTA 5", "for", "Android", "under", "10 MB"])) + '</div>')
    wi = [119, 121, 122, 123, 124]
    j = [ft(f"#s{k}v", dict(scale=1.0), dict(scale=1.08, duration=d, ease="none"), a), slide(f"#s{k}q", ws(119) - 0.1, y=60)]
    j += [ft(f"#s{k}w{n}", dict(opacity=0), dict(opacity=1, duration=0.05), ws(i)) for n, i in enumerate(wi)]
    return h, j, [("typing-keyboard-fast", ws(119), 0.35)]


def s_results(k, a, b):
    d = round(b - a, 3)
    src = rec_clip(f"r{k}", 10.8, 13.6, d)
    h = (f'<div id="s{k}v" style="position:absolute;inset:0;"><video id="v{k}" src="{src}" data-start="{a}" data-duration="{d}" muted playsinline '
         f'style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;"></video></div>'
         + txt(f"s{k}a", "KITNE SAARE RESULTS!", 120, ORANGE, "position:absolute;right:90px;top:120px;transform:rotate(-4deg);background:rgba(14,8,26,0.82);padding:14px 30px;border-radius:20px;"))
    return h, [slam(f"#s{k}a", ws(128), 1.8, 6)], [("pop-high", ws(128), 0.35)]


def s_compressed(k, a, b):   # recording frame at 12.6 s: real result title "Gta 5 Download For Pc Highly Compressed"
    img = rec_still(f"st{k}", 12.6)
    h = (f'<div id="s{k}v" style="position:absolute;inset:0;transform-origin:22% 74%;"><img src="{img}" style="position:absolute;inset:0;width:100%;height:100%;" alt="">'
         f'<div id="s{k}u" style="position:absolute;left:186px;top:812px;width:500px;height:8px;background:{ORANGE};transform-origin:0 50%;transform:scaleX(0);"></div></div>'
         + txt(f"s{k}a", "HIGHLY COMPRESSED", 100, ORANGE, "position:absolute;right:90px;top:120px;background:rgba(14,8,26,0.82);padding:14px 30px;border-radius:20px;")
         + f'<div id="s{k}e" style="position:absolute;right:110px;top:270px;opacity:0;">{em("clown_face", 170)}</div>'
         + txt(f"s{k}b", "GTA GAME OF 10 MB", 100, WHITE, "position:absolute;right:90px;top:480px;background:rgba(14,8,26,0.82);padding:14px 30px;border-radius:20px;"))
    j = [ft(f"#s{k}v", dict(scale=1), dict(scale=1.7, duration=0.6, ease="power3.inOut"), ws(136) - 0.2),
         ft(f"#s{k}u", dict(scaleX=0), dict(scaleX=1, duration=0.4, ease="power2.out"), ws(140)),
         slam(f"#s{k}a", ws(140)), pop(f"#s{k}e", ws(141)), slam(f"#s{k}b", ws(142), 1.8)]
    return h, j, [("whoosh-fast-0.3s", ws(136) - 0.1, 0.35), ("pop-high", ws(141), 0.35)]


def s_ultra(k, a, b):   # safe recreated result (guide): fictional title from the VO, reserved .example domain
    card = (f'<div id="s{k}card" style="position:absolute;left:260px;top:260px;width:1400px;padding:46px 56px;border-radius:26px;background:#202124;'
            f'border:2px solid #3c4043;box-shadow:0 30px 80px rgba(0,0,0,0.55);opacity:0;">'
            f'<div style="font-family:Jakarta;font-size:30px;color:#bdc1c6;">random-website.example › gta-5-android</div>'
            f'<div style="font-family:Jakarta;font-size:66px;color:#8ab4f8;margin:12px 0 18px;white-space:nowrap;">GTA V Ultra Lite (10 MB) - Free Download</div>'
            f'<div style="font-family:Jakarta;font-size:34px;color:#bdc1c6;">100% working!! no root!! full game!! ...</div>'
            f'<div id="s{k}o" style="position:absolute;left:30px;top:78px;width:700px;height:120px;border:9px solid {RED};border-radius:50%;transform:rotate(-3deg) scale(0);"></div></div>')
    h = dark() + card + txt(f"s{k}t", "SAFE RECREATION", 30, "#ffffffaa", "position:absolute;left:260px;top:200px;", "Jakarta")
    j = [slide(f"#s{k}card", a + 0.05, y=80), ft(f"#s{k}t", dict(opacity=0), dict(opacity=1, duration=0.2), a + 0.1),
         ft(f"#s{k}o", dict(scale=0, rotation=-30), dict(scale=1, rotation=-3, duration=0.35, ease="back.out(2)"), ws(150)),
         ft(f"#s{k}card", dict(scale=1), dict(scale=1.12, duration=0.5, ease="power3.out", immediateRender=False), ws(150))]
    return h, j, [("pop-high", ws(150), 0.4)]


def s_hawa(k, a, b):
    h = dark() + center(f'<div id="s{k}f" style="display:flex;align-items:center;gap:40px;opacity:0;">{em("fan_wind", 220)}{em("package", 200)}</div>'
                        + txt(f"s{k}a", "HAWA SE DOWNLOAD!", 170, CYAN), bottom=150)
    j = [pop(f"#s{k}f", ws(162)), ft(f"#s{k}f", dict(x=0, y=0), dict(x=40, y=-25, duration=1.0, repeat=3, yoyo=True, ease="sine.inOut", immediateRender=False), ws(162) + 0.3),
         slam(f"#s{k}a", ws(167))]
    return h, j, [("whoosh-fast-0.3s", ws(167), 0.45)]


def s_rockstar(k, a, b):
    h = gp(k, "Los Santos city wide", dim=0.2) + veil() + (
        f'<div style="position:absolute;left:90px;bottom:200px;">{txt(f"s{k}a", "ROCKSTAR GAMES", 80, ORANGE)}{txt(f"s{k}b", "ITNE SAALON KI MEHNAT", 130)}</div>')
    return h, [slide(f"#s{k}a", ws(174), x=-200), slide(f"#s{k}b", ws(177), x=-200)], [("whoosh-fast-0.3s", a + 0.05, 0.35)]


def s_uncle(k, a, b):
    h = dark() + (f'<div id="s{k}u" style="position:absolute;left:180px;top:220px;opacity:0;text-align:center;">{em("old_man", 330)}'
                  f'<div class="stroke" style="font-family:Anton;font-size:72px;color:#fff;margin-top:10px;">RANDOM WEBSITE<br>WALE UNCLE</div></div>'
                  f'<div id="s{k}g" style="position:absolute;left:820px;top:180px;width:900px;height:520px;border-radius:30px;border:6px dashed rgba(255,255,255,0.5);'
                  f'display:flex;align-items:center;justify-content:center;opacity:0;"><div class="stroke" style="font-family:Anton;font-size:170px;color:{ORANGE};">POORA GTA 5</div></div>'
                  f'<div id="s{k}x" style="position:absolute;left:1120px;top:330px;width:300px;height:220px;border-radius:24px;background:{GREEN};display:flex;align-items:center;justify-content:center;opacity:0;">'
                  f'<div style="font-family:Anton;font-size:96px;color:#0b2a14;">10 MB</div></div>'
                  f'<div id="s{k}r" style="position:absolute;left:1180px;top:720px;opacity:0;">{em("rocket", 220)}</div>')
    j = [pop(f"#s{k}u", ws(190)), pop(f"#s{k}g", ws(192)),
         ft(f"#s{k}g", dict(scale=1, opacity=1), dict(scale=0.25, opacity=0, duration=0.35, ease="power3.in", immediateRender=False), ws(199) - 0.1),
         pop(f"#s{k}x", ws(199) + 0.2),
         ft(f"#s{k}r", dict(opacity=1, y=0, rotation=0), dict(opacity=1, y=-1100, rotation=0, duration=1.3, ease="power2.in"), we(202) - 0.1),
         ft(f"#s{k}x", dict(y=0), dict(y=-1100, duration=1.3, ease="power2.in", immediateRender=False), we(202) - 0.1)]
    return h, j, [("boing", ws(199), 0.35), ("thruster", we(202) - 0.1, 0.35)]


def s_nasa(k, a, b):
    stars = "".join(f'<div style="position:absolute;left:{(i * 397) % 1920}px;top:{(i * 263) % 1080}px;width:{3 + i % 3}px;height:{3 + i % 3}px;border-radius:50%;background:#fff;opacity:{0.4 + (i % 5) / 10};"></div>' for i in range(70))
    h = (f'<div style="position:absolute;inset:0;background:linear-gradient(160deg, #1d1b4a 0%, #04030c 70%);">{stars}</div>'
         f'<div id="s{k}e" style="position:absolute;left:250px;top:200px;opacity:0;">{em("astronaut", 380)}</div>'
         f'<div style="position:absolute;left:760px;top:260px;width:1050px;">{txt(f"s{k}a", "INKO TOH", 120)}{txt(f"s{k}b", "NASA MEIN HONA CHAHIYE!", 120, CYAN)}</div>')
    j = [ft(f"#s{k}e", dict(opacity=0, x=-300, rotation=-30), dict(opacity=1, x=0, rotation=10, duration=b - a, ease="sine.out"), a),
         slam(f"#s{k}a", ws(204)), slam(f"#s{k}b", ws(206), 1.8)]
    return h, j, [("whoosh-fast-0.3s", a + 0.05, 0.4)]


def s_loading(k, a, b):   # script note: fake loading bar "GTA 5 - 10 MB downloaded. Los Santos loading..."; stops on "ruk jao"
    h = gp(k, "Los Santos skyline", dim=0.55, blur=6) + center(
        txt(f"s{k}a", "GTA 5 · 10 MB DOWNLOADED ✓", 70, GREEN, font="Jakarta") + bar(f"s{k}p", "Los Santos loading...", 1200, ORANGE)
        + txt(f"s{k}b", "RUK JAO!", 170, RED), bottom=150, gap=34)
    j = [ft(f"#s{k}a", dict(opacity=0), dict(opacity=1, duration=0.2), a), ft(f"#s{k}pl", dict(opacity=0), dict(opacity=1, duration=0.2), a),
         ft(f"#s{k}p", dict(scaleX=0), dict(scaleX=0.93, duration=ws(211) - a, ease="power1.out"), a),
         slam(f"#s{k}b", ws(211), 2.6), shake(f"#s{k}b", ws(211) + 0.22)]
    return h, j, [("record-scratch", ws(211), 0.55)]


def eq_shot(k, a, b, A, B, ia, ib, neq=True, fs=150):
    opd = (f'<div id="s{k}o" style="position:relative;opacity:0;"><div class="stroke" style="font-family:Anton;font-size:{int(fs * 1.15)}px;color:{RED};">=</div>'
           + (f'<div style="position:absolute;left:50%;top:12%;width:{int(fs * 0.13)}px;height:76%;background:{RED};border:5px solid {INK};'
              f'transform:translateX(-50%) rotate(28deg);border-radius:6px;"></div>' if neq else "") + '</div>')
    h = dark() + center(f'<div id="s{k}A" class="stroke" style="font-family:Anton;font-size:{fs}px;color:#fff;opacity:0;white-space:nowrap;">{A}</div>{opd}'
                        f'<div id="s{k}B" class="stroke" style="font-family:Anton;font-size:{fs}px;color:{ORANGE};opacity:0;white-space:nowrap;">{B}</div>', bottom=150, gap=10)
    j = [slide(f"#s{k}A", ws(ia), x=-300), pop(f"#s{k}o", (ws(ia) + ws(ib)) / 2), slam(f"#s{k}B", ws(ib)), shake(f"#s{k}B", ws(ib) + 0.22)]
    return h, j, [("whoosh-fast-0.3s", ws(ia), 0.3), ("impact-punch", ws(ib), 0.35)]


def s_not_inside(k, a, b):
    return eq_shot(k, a, b, "10 MB DOWNLOAD", "POORA GTA 5", 213, 226)


def q_list(k, rows, title=None, icon="thinking_face"):
    inner = (txt(f"s{k}t", title, 90, WHITE) if title else "") + "".join(
        f'<div id="s{k}r{r}" style="display:flex;align-items:center;gap:30px;opacity:0;">{em(e, 110)}'
        f'<div class="stroke" style="font-family:Anton;font-size:110px;color:{c};white-space:nowrap;">{t}</div></div>' for r, (_, t, e, c) in enumerate(rows))
    return dark() + center(inner, bottom=150, gap=30)


def s_maybe(k, a, b):
    rows = [(238, "SIRF EK LAUNCHER?", "package", WHITE), (241, "KOI FAKE APP?", "clown_face", ORANGE), (246, "YA KUCH AUR HI?", "eyes", RED)]
    j = [slide(f"#s{k}r{r}", ws(wi), x=250) for r, (wi, *_) in enumerate(rows)]
    return q_list(k, rows), j, [("pop-high", ws(wi), 0.35) for wi, *_ in rows]


def s_milega(k, a, b):   # guide: freeze frame + bold text
    img = rec_still(f"st{k}", 12.6)
    h = (f'<img src="{img}" style="position:absolute;inset:0;width:100%;height:100%;filter:grayscale(1) brightness(0.35);" alt="">'
         + center(txt(f"s{k}a", "DOWNLOAD KARNE KE BAAD", 120) + txt(f"s{k}b", "MILEGA KYA?", 230, ORANGE), bottom=150, gap=10))
    j = [ft(f"#s{k}c", dict(scale=1.15), dict(scale=1, duration=0.3, ease="power4.out"), a), slam(f"#s{k}a", ws(255)), slam(f"#s{k}b", ws(259), 3), shake(f"#s{k}b", ws(259) + 0.22)]
    return h, j, [("camera-freeze", a, 0), ("impact-punch", ws(259), 0.4)]


# Scene 3 - installation trap (safe recreations, nothing downloaded or installed)
def s_install(k, a, b):
    scr = (f'<div style="position:absolute;inset:0;background:#141420;display:flex;flex-direction:column;align-items:center;padding-top:120px;gap:26px;">'
           f'<div style="font-family:Jakarta;font-weight:800;font-size:34px;color:#9aa0b4;">Downloads</div>'
           f'<div id="s{k}f" style="width:420px;padding:26px;border-radius:24px;background:#22223a;display:flex;align-items:center;gap:20px;opacity:0;">{em("package", 90)}'
           f'<div style="font-family:Jakarta;font-weight:800;font-size:30px;color:#fff;text-align:left;">gta5_ultra_lite.apk<br><span style="color:#9aa0b4;font-size:26px;">10 MB · complete</span></div></div>'
           f'<div id="s{k}i" style="margin-top:40px;padding:18px 70px;border-radius:40px;background:{GREEN};font-family:Jakarta;font-weight:800;font-size:40px;color:#0b2a14;opacity:0;">INSTALL</div></div>')
    h = dark() + phone(f"s{k}ph", scr, left=1180, top=75) + (
        f'<div style="position:absolute;left:110px;top:280px;width:1000px;">{txt(f"s{k}a", "APK MIL BHI GAYA...", 120)}{txt(f"s{k}b", "DOWNLOAD ✓", 120, GREEN)}{txt(f"s{k}ab", "AB INSTALL...", 120, ORANGE)}</div>'
        f'<div style="position:absolute;left:110px;top:200px;">{txt(f"s{k}n", "ILLUSTRATIVE RECREATION", 30, "#ffffffaa", "", "Jakarta")}</div>')
    j = [slide(f"#s{k}ph", a + 0.05, y=500, d=0.45), ft(f"#s{k}n", dict(opacity=0), dict(opacity=1, duration=0.2), a + 0.2),
         slam(f"#s{k}a", ws(271)), pop(f"#s{k}f", ws(278)), slam(f"#s{k}b", ws(278)), pop(f"#s{k}i", ws(283)), slam(f"#s{k}ab", ws(283)),
         ft(f"#s{k}i", dict(scale=1), dict(scale=0.88, duration=0.08, yoyo=True, repeat=1, immediateRender=False), ws(285))]
    return h, j, [("pop-high", ws(278), 0.35), ("mouse-click", ws(285), 0.8)]


def s_sure(k, a, b):
    words = ["Are", "you", "sure", "want", "to", "install", "this", "app?"]
    h = dark() + (f'<div id="s{k}d" style="position:absolute;left:460px;top:200px;width:1000px;padding:60px;border-radius:40px;background:#2a2838;'
                  f'box-shadow:0 40px 100px rgba(0,0,0,0.6);opacity:0;">'
                  f'<div style="display:flex;align-items:center;gap:26px;margin-bottom:34px;">{em("package", 90)}<div style="font-family:Jakarta;font-weight:800;font-size:44px;color:#fff;">GTA 5 Ultra Lite</div></div>'
                  f'<div style="font-family:Jakarta;font-weight:700;font-size:62px;line-height:1.2;color:#fff;">'
                  + "".join(f'<span id="s{k}w{n}" style="opacity:0;">{w} </span>' for n, w in enumerate(words)) + '</div>'
                  f'<div style="display:flex;justify-content:flex-end;gap:70px;margin-top:50px;font-family:Jakarta;font-weight:800;font-size:44px;color:#a8c7fa;">'
                  f'<span>CANCEL</span><span id="s{k}i">INSTALL</span></div></div>')
    j = [pop(f"#s{k}d", a + 0.1)] + [ft(f"#s{k}w{n}", dict(opacity=0), dict(opacity=1, duration=0.06), ws(290 + n)) for n in range(len(words))]
    return h, j, [("notification-pop", a + 0.1, 0)]


def s_brain(k, a, b):
    def side(sid, e, who, say, col):
        return (f'<div id="{sid}" style="flex:1;display:flex;flex-direction:column;align-items:center;gap:20px;opacity:0;">{em(e, 260)}'
                f'<div style="font-family:Jakarta;font-weight:800;font-size:46px;color:#cfc6e8;">{who}</div>'
                f'<div class="stroke" style="font-family:Anton;font-size:120px;color:{col};white-space:nowrap;">{say}</div></div>')
    h = dark() + (f'<div style="position:absolute;left:60px;right:60px;top:110px;bottom:200px;display:flex;align-items:center;">'
                  + side(f"s{k}L", "brain", "TUMHARA DIMAAG", "BHAI, GTA 5 HAI!", ORANGE)
                  + f'<div style="width:6px;height:520px;background:rgba(255,255,255,0.25);"></div>'
                  + side(f"s{k}R", "light_bulb", "COMMON SENSE", "BHAI, RUK JA!", GREEN) + '</div>')
    j = [slide(f"#s{k}L", ws(298), x=-200), slide(f"#s{k}R", ws(307), x=200), shake(f"#s{k}R", ws(313))]
    return h, j, [("whoosh-fast-0.3s", ws(298), 0.3), ("whoosh-fast-0.3s", ws(307), 0.3), ("ui-error-1", we(314) + 0.05, 0.9)]


def s_side(k, a, b):
    h = dark() + (f'<div id="s{k}L" style="position:absolute;left:300px;top:200px;text-align:center;opacity:0;">{em("fire", 280)}'
                  f'<div class="stroke" style="font-family:Anton;font-size:130px;color:{ORANGE};">EXCITEMENT</div></div>'
                  f'<div id="s{k}R" style="position:absolute;left:1180px;top:240px;text-align:center;opacity:0;">{em("light_bulb", 220)}'
                  f'<div style="font-family:Jakarta;font-weight:800;font-size:56px;color:{GREEN};">COMMON SENSE</div></div>'
                  + txt(f"s{k}t", "SIDE MEIN!", 120, WHITE, "position:absolute;left:1180px;top:700px;"))
    j = [pop(f"#s{k}L", ws(316)), pop(f"#s{k}R", a + 0.1),
         ft(f"#s{k}R", dict(x=0, rotation=0), dict(x=650, rotation=40, duration=0.45, ease="power3.in", immediateRender=False), ws(322)),
         slam(f"#s{k}t", ws(322) + 0.1)]
    return h, j, [("swish-4", ws(322), 0.5), ("fall", ws(322) + 0.1, 0.35)]


def s_perms(k, a, b):
    rows = [(331, "Contacts", "busts"), (334, "SMS", "speech_balloon"), (337, "Files", "file_folder")]
    h = dark() + (f'<div id="s{k}d" style="position:absolute;left:480px;top:110px;width:960px;padding:50px 60px;border-radius:40px;background:#2a2838;'
                  f'box-shadow:0 40px 100px rgba(0,0,0,0.6);opacity:0;">'
                  f'<div style="font-family:Jakarta;font-weight:800;font-size:46px;color:#fff;margin-bottom:30px;">Allow GTA 5 Ultra Lite to access:</div>'
                  + "".join(f'<div id="s{k}r{r}" style="display:flex;align-items:center;gap:30px;padding:22px 26px;margin:14px 0;border-radius:24px;border:5px solid transparent;">'
                            f'{em(e, 90)}<div style="font-family:Jakarta;font-weight:800;font-size:60px;color:#fff;">{t}</div>'
                            f'<div id="s{k}m{r}" style="margin-left:auto;font-family:Anton;font-size:60px;color:{RED};opacity:0;">?!</div></div>' for r, (_, t, e) in enumerate(rows))
                  + '</div>')
    j = [pop(f"#s{k}d", a + 0.1)]
    for r, (wi, *_) in enumerate(rows):
        j += [ft(f"#s{k}r{r}", dict(borderColor="rgba(255,59,59,0)", backgroundColor="rgba(255,59,59,0)"),
                 dict(borderColor=RED, backgroundColor="rgba(255,59,59,0.18)", duration=0.15), ws(wi) - 0.05), pop(f"#s{k}m{r}", ws(wi) + 0.1)]
    return h, j, [("alarm", ws(wi), 0.25) for wi, *_ in rows]


def s_rishta(k, a, b):
    h = dark() + center(txt(f"s{k}a", "BHAI, GTA 5 KHELNA HAI", 120) + f'<div id="s{k}e" style="opacity:0;">{em("ring", 220)}</div>'
                        + txt(f"s{k}b", "YA SHAADI KA RISHTA DHOONDHNA HAI?", 105, PINK), bottom=150, gap=16)
    j = [slam(f"#s{k}a", ws(340)), pop(f"#s{k}e", ws(347)), slam(f"#s{k}b", ws(347), 1.8),
         ft(f"#s{k}c", dict(scale=1), dict(scale=1.12, duration=0.18, ease="power4.out", immediateRender=False), ws(347))]
    return h, j, [("pop-high", ws(347), 0.4), ("badumtss", we(351) + 0.15, 0.4)]


def s_char(k, a, b, who, wi, e, label, zoom=False):
    h = gp(k, f"{who} shot", dim=0.15) + veil() + (
        f'<div id="s{k}b" style="position:absolute;right:120px;top:180px;display:flex;align-items:center;gap:26px;padding:30px 46px;border-radius:40px;'
        f'background:rgba(20,12,36,0.88);border:5px solid {ORANGE};opacity:0;">{em(e, 130)}'
        f'<div class="stroke" style="font-family:Anton;font-size:100px;color:#fff;white-space:nowrap;">{label}</div></div>')
    j = [pop(f"#s{k}b", ws(wi))]
    s = [("pop-high", ws(wi), 0.35)]
    if zoom:   # guide: Trevor - dramatic zoom, record scratch, short pause
        j += [ft(f"#g{k}", dict(scale=1), dict(scale=1.35, duration=0.25, ease="power4.out"), ws(368) - 0.05), shake(f"#g{k}", ws(368) + 0.25, 12)]
        s = [("record-scratch", ws(368), 0.55), ("pop-high", ws(wi), 0.35)]
    return h, j, s


def s_risk(k, a, b):
    rows = [(386, "PERMISSIONS KA MISUSE", "unlocked"), (396, "DATA CHURA SAKTE", "money_bag"), (401, "DEVICE KO HARM", "skull")]
    h = dark() + (f'<div id="s{k}w" style="position:absolute;left:150px;right:150px;top:110px;padding:28px 0;border-radius:26px;background:{RED};text-align:center;opacity:0;">'
                  f'<div class="stroke" style="font-family:Anton;font-size:116px;color:#fff;-webkit-text-stroke-color:#5a0000;">UNKNOWN APK = POTENTIAL RISK</div></div>'
                  f'<div style="position:absolute;left:330px;top:400px;display:flex;flex-direction:column;gap:34px;">'
                  + "".join(f'<div id="s{k}r{r}" style="display:flex;align-items:center;gap:34px;opacity:0;">{em(e, 100)}'
                            f'<div class="stroke" style="font-family:Anton;font-size:90px;color:{WHITE if r % 2 == 0 else ORANGE};white-space:nowrap;">{t}</div></div>' for r, (_, t, e) in enumerate(rows))
                  + '</div>' + txt(f"s{k}j", "JOKES ASIDE...", 70, "#cfc6e8", "position:absolute;left:150px;top:30px;"))
    j = [slide(f"#s{k}j", a + 0.05, y=-30), slam(f"#s{k}w", ws(380), 1.5), shake(f"#s{k}w", ws(380) + 0.2)]
    j += [slide(f"#s{k}r{r}", ws(wi), x=200) for r, (wi, *_) in enumerate(rows)]
    return h, j, [("error-buzz", ws(380), 0.3)] + [("pop-high", ws(wi), 0.3) for wi, *_ in rows]


def s_verify(k, a, b):
    h = dark() + center(f'<div id="s{k}e" style="opacity:0;">{em("prohibited", 240)}</div>' + txt(f"s{k}a", "BINA VERIFY KIYE", 150, ORANGE)
                        + txt(f"s{k}b", "RANDOM WEBSITE SE APK INSTALL MAT KARNA!", 84), bottom=150, gap=14)
    return h, [pop(f"#s{k}e", ws(406)), slam(f"#s{k}a", ws(407)), slide(f"#s{k}b", ws(410), y=40)], [("impact-punch", ws(407), 0.35)]


# Scene 4 - 10 MB reality check
def s_logic(k, a, b):
    h = dark() + center(f'<div id="s{k}e" style="opacity:0;">{em("face_with_monocle", 260)}</div>' + txt(f"s{k}a", "AB THODA LOGIC...", 160, CYAN), bottom=150)
    return h, [pop(f"#s{k}e", ws(422)), slam(f"#s{k}a", ws(424))], [("pop-high", ws(424), 0.3)]


def s_world(k, a, b):
    h = gp(k, "massive open world, wide / aerial", dim=0.1) + veil() + txt(f"s{k}a", "MASSIVE OPEN WORLD", 130, WHITE, "position:absolute;left:90px;bottom:200px;")
    return h, [slide(f"#s{k}a", ws(431), x=-200), ft(f"#g{k}", dict(scale=1), dict(scale=1.15, duration=b - a, ease="none"), a)], [("whoosh-fast-0.3s", a + 0.05, 0.3)]


def s_stuff(k, a, b):
    tags = [(437, "CITY", "cityscape"), (439, "CARS", "automobile"), (440, "BUILDINGS", "office_building"), (441, "MISSIONS", "fire"),
            (442, "CHARACTERS", "bust"), (443, "AUDIO", "speaker"), (444, "TEXTURES", "artist_palette"), (448, "GAME DATA", "floppy")]
    h = gp(k, "city / cars / buildings / missions / characters (one cut per word)", dim=0.45, blur=4) + (
        '<div style="position:absolute;left:120px;right:120px;top:150px;display:flex;flex-wrap:wrap;gap:30px 40px;justify-content:center;">'
        + "".join(f'<div id="s{k}t{r}" style="display:flex;align-items:center;gap:20px;padding:18px 36px;border-radius:30px;background:rgba(20,12,36,0.9);'
                  f'border:4px solid {ORANGE if r < 5 else CYAN};opacity:0;">{em(e, 90)}<div style="font-family:Anton;font-size:84px;color:#fff;">{t}</div></div>'
                  for r, (_, t, e) in enumerate(tags)) + '</div>')
    j = [pop(f"#s{k}t{r}", ws(wi), 0.22) for r, (wi, *_) in enumerate(tags)]
    return h, j, [("pop-high", ws(wi), 0.28) for wi, *_ in tags]


def s_fit(k, a, b):
    blocks = "".join(f'<div style="position:absolute;left:{x}px;top:{y}px;width:230px;height:150px;border-radius:20px;background:{c};"></div>'
                     for x, y, c in [(0, 300, ORANGE), (240, 300, CYAN), (480, 300, PINK), (120, 140, GREEN), (360, 140, ORANGE), (240, -20, CYAN)])
    h = dark() + (f'<div id="s{k}p" style="position:absolute;left:180px;top:280px;width:720px;height:460px;opacity:0;">{blocks}'
                  f'<div class="stroke" style="position:absolute;left:0;right:0;top:470px;text-align:center;font-family:Anton;font-size:70px;color:#fff;">YE SAB</div></div>'
                  f'<div id="s{k}x" style="position:absolute;left:1260px;top:480px;width:240px;height:170px;border-radius:20px;background:{GREEN};display:flex;align-items:center;justify-content:center;opacity:0;">'
                  f'<div style="font-family:Anton;font-size:84px;color:#0b2a14;">10 MB</div></div>'
                  + txt(f"s{k}a", "ISME AA JAYEGA?", 120, ORANGE, "position:absolute;left:1020px;top:220px;"))
    j = [pop(f"#s{k}p", ws(456)), pop(f"#s{k}x", ws(458)), slam(f"#s{k}a", ws(461)),
         ft(f"#s{k}p", dict(x=0, scale=1), dict(x=700, scale=0.4, duration=0.35, ease="power2.in", immediateRender=False), ws(462)),
         ft(f"#s{k}p", dict(x=700, scale=0.4), dict(x=150, scale=1, duration=0.5, ease="back.out(1.6)", immediateRender=False), ws(462) + 0.4),
         shake(f"#s{k}x", ws(462) + 0.35)]
    return h, j, [("boing", ws(462) + 0.35, 0.4)]


def s_minecraft(k, a, b):   # guide: quick Minecraft gameplay cut = the client's own ALOO SMP spawn recording (Drive 1SmJKT0fOUn--o94gnSx_Pg3D4gq5wpwA, 20 s in)
    d = round(b - a, 3)
    out = f"assets/gp/mc_{d:.2f}.mp4"
    if not DRY[0] and not os.path.exists(out):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "20", "-t", f"{d + 0.1:.3f}", "-i", "../../in/spawn.mkv", "-an", "-vf", "fps=30",
                        "-c:v", "libx264", "-crf", "17", "-preset", "veryfast", "-pix_fmt", "yuv420p", out], check=True)
    h = (f'<div id="g{k}" style="position:absolute;inset:0;filter:brightness(0.8);"><video id="gv{k}" src="{out}" data-start="{a}" data-duration="{d}" muted playsinline '
         f'style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;"></video></div>' + veil()
         + txt(f"s{k}a", "MERA MINECRAFT RESOURCE PACK", 96, WHITE, "position:absolute;left:90px;top:330px;")
         + txt(f"s{k}b", "ISSE BADA HAI!", 130, ORANGE, "position:absolute;left:90px;top:450px;"))
    return h, [slam(f"#s{k}a", ws(465)), slam(f"#s{k}b", ws(470), 1.8)], [("whoosh-fast-0.3s", a + 0.05, 0.4), ("pop-high", ws(470), 0.35)]


def s_tiny(k, a, b):
    h = dark() + (f'<div id="s{k}g" style="position:absolute;left:260px;top:200px;width:820px;height:560px;border-radius:30px;background:linear-gradient(135deg,{ORANGE},{PINK});'
                  f'display:flex;align-items:center;justify-content:center;opacity:0;"><div class="stroke" style="font-family:Anton;font-size:120px;color:#fff;">POORA GAME</div></div>'
                  f'<div id="s{k}f" style="position:absolute;left:1350px;top:420px;text-align:center;opacity:0;">{em("floppy", 120)}'
                  f'<div style="font-family:Jakarta;font-weight:800;font-size:40px;color:#fff;">chhoti si file</div></div>'
                  + txt(f"s{k}a", "EK CHHOTI SI FILE MEIN?", 120, ORANGE, "position:absolute;left:0;right:0;top:780px;text-align:center;"))
    j = [pop(f"#s{k}g", ws(480)), pop(f"#s{k}f", ws(483)), slam(f"#s{k}a", ws(485)),
         ft(f"#s{k}g", dict(scaleX=1, scaleY=1, x=0), dict(scaleX=0.12, scaleY=0.2, x=900, duration=0.5, ease="power3.in", immediateRender=False), ws(485))]
    return h, j, [("swish-4", ws(485), 0.45)]


def s_jaadu(k, a, b):
    sp = "".join(f'<div class="s{k}sp" style="position:absolute;left:{300 + (i * 211) % 1300}px;top:{120 + (i * 137) % 640}px;opacity:0;">{em("sparkles", 90 + (i % 3) * 30)}</div>' for i in range(10))
    h = dark() + sp + center(f'<div id="s{k}e" style="opacity:0;">{em("magic_wand", 230)}</div>' + txt(f"s{k}a", "COMPRESSION NAHI...", 100)
                             + txt(f"s{k}b", "YE TOH DIGITAL JAADU HAI!", 150, PINK), bottom=150, gap=10)
    j = [slide(f"#s{k}a", ws(487), y=40), pop(f"#s{k}e", ws(490)), slam(f"#s{k}b", ws(492), 2.4),
         ft(f".s{k}sp", dict(opacity=0, scale=0), dict(opacity=1, scale=1, duration=0.3, stagger=0.06, ease="back.out(2)"), ws(492)),
         ft(f"#s{k}c", dict(scale=1), dict(scale=1.15, duration=0.25, ease="power4.out", immediateRender=False), ws(492))]
    return h, j, [("magic-shimmer", ws(492), 0.5), ("wink", ws(493), 0.4)]


def s_compare(k, a, b):   # guide + script: "10 MB - Website ka promise" vs "Full game - Actual game data"; no made-up size
    h = dark() + (f'<div style="position:absolute;left:150px;right:150px;top:110px;bottom:220px;display:flex;align-items:flex-end;justify-content:space-around;">'
                  f'<div id="s{k}L" style="text-align:center;opacity:0;"><div style="width:300px;height:60px;margin:0 auto 26px;border-radius:12px;background:{GREEN};"></div>'
                  f'<div class="stroke" style="font-family:Anton;font-size:96px;color:{GREEN};">10 MB</div>'
                  f'<div style="font-family:Jakarta;font-weight:800;font-size:44px;color:#fff;">website ka promise<br>(installer / launcher ho sakta hai)</div></div>'
                  f'<div id="s{k}R" style="text-align:center;opacity:0;"><div id="s{k}h" style="width:300px;height:520px;margin:0 auto 26px;border-radius:12px;'
                  f'background:linear-gradient(0deg,{ORANGE},{PINK});transform-origin:50% 100%;"></div>'
                  f'<div class="stroke" style="font-family:Anton;font-size:96px;color:{ORANGE};">FULL GTA 5</div>'
                  f'<div style="font-family:Jakarta;font-weight:800;font-size:44px;color:#fff;">actual game data<br>(kahin zyada)</div></div></div>')
    j = [slide(f"#s{k}L", ws(501), y=80), slide(f"#s{k}R", ws(519), y=80),
         ft(f"#s{k}h", dict(scaleY=0.1), dict(scaleY=1, duration=0.9, ease="power3.out"), ws(519))]
    return h, j, [("pop-high", ws(501), 0.3), ("riser-2s", ws(519) + 0.8, 0.25)]


def s_cloud(k, a, b):
    h = dark() + (f'<div id="s{k}cl" style="position:absolute;left:180px;top:200px;text-align:center;opacity:0;">{em("cloud", 300)}'
                  f'<div class="stroke" style="font-family:Anton;font-size:80px;color:{CYAN};">REMOTE SERVER</div>'
                  f'<div style="font-family:Jakarta;font-weight:800;font-size:44px;color:#fff;">game yahan run hota hai</div></div>'
                  f'<div id="s{k}l" style="position:absolute;left:720px;top:420px;width:540px;height:14px;border-radius:7px;'
                  f'background:repeating-linear-gradient(90deg,{CYAN} 0 40px, transparent 40px 70px);transform-origin:0 50%;transform:scaleX(0);"></div>'
                  f'<div id="s{k}p" style="position:absolute;left:1320px;top:200px;text-align:center;opacity:0;">{em("mobile_phone", 300)}'
                  f'<div class="stroke" style="font-family:Anton;font-size:80px;color:#fff;">INTERNET SE STREAM</div></div>'
                  + txt(f"s{k}t", "CLOUD GAMING = ALAG CHEEZ", 100, ORANGE, "position:absolute;left:0;right:0;top:40px;text-align:center;"))
    j = [slam(f"#s{k}t", ws(528)), pop(f"#s{k}cl", ws(538)), pop(f"#s{k}p", ws(544)),
         ft(f"#s{k}l", dict(scaleX=0), dict(scaleX=1, duration=0.5, ease="power2.out"), ws(544)),
         ft(f"#s{k}l", dict(backgroundPositionX="0px"), dict(backgroundPositionX="210px", duration=max(0.5, b - ws(544) - 0.5), ease="none", immediateRender=False), ws(544) + 0.5)]
    return h, j, [("pop-high", ws(538), 0.3), ("blip-up", ws(544), 0.3)]


def s_filesize(k, a, b):
    return eq_shot(k, a, b, "FILE SIZE", "FULL GAME", 550, 561)


# Scene 5 - how to stay safe (guide: clean, readable, calm; tips text from the guide)
def s_rules(k, a, b):
    h = dark() + center(f'<div id="s{k}e" style="display:flex;gap:30px;opacity:0;">{em("shield", 220)}</div>'
                        + txt(f"s{k}a", "KUCH SIMPLE RULES", 140, GREEN), bottom=150)
    return h, [pop(f"#s{k}e", ws(576)), slam(f"#s{k}a", ws(584))], [("success-chime", ws(585), 0.25)]


TIPS = [(589, "Official sources check karo."), (601, "Developer aur app ki authenticity verify karo."),
        (611, "Unbelievable offers ko blindly trust mat karo."), (628, "Unknown APKs bina verify kiye install mat karo.")]


def s_tips(k, a, b):
    h = dark() + ('<div style="position:absolute;left:170px;right:170px;top:110px;display:flex;flex-direction:column;gap:34px;">'
                  + "".join(f'<div id="s{k}r{r}" style="display:flex;align-items:center;gap:36px;padding:26px 40px;border-radius:30px;background:rgba(43,217,107,0.10);'
                            f'border:4px solid rgba(43,217,107,0.35);opacity:0;">'
                            f'<div style="font-family:Anton;font-size:70px;color:{GREEN};white-space:nowrap;">TIP {r + 1}</div>'
                            f'<div style="font-family:Jakarta;font-weight:800;font-size:54px;color:#fff;">{t}</div>'
                            f'<img src="assets/el/check_mark.png" id="s{k}m{r}" style="width:80px;height:80px;margin-left:auto;opacity:0;" alt=""></div>' for r, (_, t) in enumerate(TIPS))
                  + '</div>')
    j = []
    for r, (wi, _) in enumerate(TIPS):
        j += [slide(f"#s{k}r{r}", ws(wi), x=200), pop(f"#s{k}m{r}", ws(wi) + 0.6),
              ft(f"#s{k}r{r}", dict(borderColor="rgba(43,217,107,0.35)"), dict(borderColor=GREEN, duration=0.2), ws(wi))]
        if r:
            j.append(ft(f"#s{k}r{r - 1}", dict(borderColor=GREEN), dict(borderColor="rgba(43,217,107,0.35)", duration=0.2, immediateRender=False), ws(wi)))
    return h, j, [("pop-high", ws(wi), 0.3) for wi, _ in TIPS]


def s_thumb(k, a, b):   # "YouTube thumbnail par log GTA 6 bhi mobile mein chala dete hain": the client's own picture (sent 2026-10-28) shown as a clickbait thumbnail
    th = (f'<div id="s{k}th" style="position:absolute;left:360px;top:70px;width:1200px;opacity:0;">'
          f'<div style="position:relative;width:1200px;height:675px;border-radius:24px;overflow:hidden;box-shadow:0 40px 100px rgba(0,0,0,0.6);">'
          f'<img src="assets/img/client_gta6_thumb.jpg" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;" alt="">'
          f'<div style="position:absolute;right:20px;bottom:20px;padding:4px 14px;border-radius:8px;background:rgba(0,0,0,0.85);font-family:Jakarta;font-weight:800;font-size:34px;color:#fff;">10:00</div></div>'
          f'<div style="font-family:Jakarta;font-weight:800;font-size:44px;color:#fff;margin-top:20px;">GTA 6 ON ANDROID?! 100% WORKING!! 😱🔥</div></div>'
          + txt(f"s{k}n", "CLICKBAIT THUMBNAIL", 30, "#ffffffaa", "position:absolute;left:360px;top:24px;", "Jakarta")
          + f'<div id="s{k}s" data-layout-allow-overlap data-layout-allow-occlusion style="position:absolute;left:760px;top:330px;padding:10px 50px;border:12px solid {RED};border-radius:20px;transform:rotate(-12deg);opacity:0;'
          f'font-family:Anton;font-size:150px;color:{RED};background:rgba(255,255,255,0.92);">FAKE?</div>')
    h = dark() + th
    j = [ft(f"#s{k}n", dict(opacity=0), dict(opacity=1, duration=0.2), ws(652)), pop(f"#s{k}th", ws(652)),
         ft(f"#s{k}th", dict(scale=1), dict(scale=1.12, duration=0.2, ease="power4.out", immediateRender=False), ws(657)),
         slam(f"#s{k}s", ws(661), 3)]
    return h, j, [("pop-high", ws(652), 0.3), ("record-scratch", ws(657), 0.5), ("impact-punch", ws(661), 0.35)]


def s_pcphone(k, a, b):
    h = dark() + (f'<div id="s{k}L" style="position:absolute;left:150px;top:150px;width:780px;text-align:center;opacity:0;">'
                  f'<div style="position:relative;height:440px;border-radius:20px;overflow:hidden;border:8px solid #3a3150;">{gp(f"{k}pc", "PC gameplay")}</div>'
                  f'<div class="stroke" style="font-family:Anton;font-size:90px;color:#fff;margin-top:20px;">GAMEPLAY: PC KA</div></div>'
                  f'<div id="s{k}R" style="position:absolute;left:1180px;top:110px;text-align:center;opacity:0;">'
                  f'<div style="width:300px;height:540px;margin:0 auto;border-radius:40px;background:#101018;border:8px solid #3a3150;display:flex;align-items:center;justify-content:center;">'
                  f'{em("clown_face", 160)}</div><div class="stroke" style="font-family:Anton;font-size:90px;color:{RED};margin-top:20px;">PHONE: FAKE APP</div></div>')
    return h, [slide(f"#s{k}L", ws(674), x=-200), slide(f"#s{k}R", ws(686), x=200)], [("whoosh-fast-0.3s", ws(674), 0.3), ("negative", ws(687), 0.3)]


def s_legit(k, a, b):
    h = dark() + center(txt(f"s{k}a", "GTA MOBILE PAR KHELNA HAI?", 110)
                        + f'<div id="s{k}b" style="display:flex;align-items:center;gap:30px;padding:26px 50px;border-radius:40px;background:rgba(43,217,107,0.15);border:5px solid {GREEN};opacity:0;">'
                        f'{em("cloud", 140)}<div class="stroke" style="font-family:Anton;font-size:110px;color:{GREEN};">LEGIT CLOUD GAMING</div></div>'
                        + f'<div id="s{k}rg" style="display:flex;align-items:center;gap:24px;opacity:0;">{em("globe", 100)}'
                        f'<div style="font-family:Jakarta;font-weight:800;font-size:58px;color:#fff;">agar tumhare region mein available ho</div></div>', bottom=150, gap=34)
    return h, [slide(f"#s{k}a", ws(692), y=40), pop(f"#s{k}b", ws(704)), slide(f"#s{k}rg", ws(711), y=40)], [("success-chime", ws(704), 0.3)]


# Scene 6 - final roast (guide: suspense before the punchline, dramatic zoom + shake, short silence, final text)
def s_bole(k, a, b):
    h = gp(k, "gameplay, dramatic", dim=0.3) + veil() + (
        f'<div id="s{k}b" style="position:absolute;left:320px;top:250px;display:flex;align-items:center;gap:30px;padding:40px 60px;border-radius:50px;background:#fff;opacity:0;">'
        f'{em("speaking_head", 150)}<div style="font-family:Anton;font-size:96px;color:#140c24;white-space:nowrap;">"GTA 5 SIRF 10 MB MEIN!"</div></div>')
    return h, [pop(f"#s{k}b", ws(725))], [("pop-high", ws(725), 0.35)]


def s_dimaag(k, a, b):
    h = dark() + center(f'<div id="s{k}d" style="display:flex;align-items:center;gap:20px;padding:30px 80px;border-radius:30px;background:{GREEN};opacity:0;">'
                        f'{em("download", 110)}<div style="font-family:Anton;font-size:100px;color:#0b2a14;">DOWNLOAD</div></div>'
                        f'<div style="display:flex;align-items:center;gap:40px;">{em("brain", 200)}'
                        f'<div id="s{k}sw" style="position:relative;width:260px;height:130px;border-radius:65px;background:#444;opacity:0;">'
                        f'<div id="s{k}k" style="position:absolute;left:10px;top:10px;width:110px;height:110px;border-radius:50%;background:#fff;"></div></div>'
                        + txt(f"s{k}a", "DIMAAG ON!", 140, GREEN) + '</div>', bottom=150, gap=50)
    j = [pop(f"#s{k}d", ws(735)), pop(f"#s{k}sw", ws(740)),
         ft(f"#s{k}k", dict(x=0), dict(x=130, duration=0.15, ease="power2.out"), ws(742)),
         ft(f"#s{k}sw", dict(backgroundColor="#444444"), dict(backgroundColor=GREEN, duration=0.15, immediateRender=False), ws(742)),
         slam(f"#s{k}a", ws(742))]
    return h, j, [("switch", ws(742), 0.7)]


def s_atrisk(k, a, b):
    items = [(754, "ACCOUNT", "key"), (755, "DATA", "file_folder"), (757, "PHONE", "mobile_phone")]
    h = dark() + center('<div style="display:flex;gap:90px;">' + "".join(
        f'<div id="s{k}i{r}" style="text-align:center;opacity:0;padding:30px;border-radius:30px;border:6px solid {RED};background:rgba(255,59,59,0.12);">{em(e, 190)}'
        f'<div class="stroke" style="font-family:Anton;font-size:84px;color:#fff;">{t}</div></div>' for r, (_, t, e) in enumerate(items)) + '</div>'
        + txt(f"s{k}a", "RISK MEIN!", 150, RED), bottom=150, gap=40)
    j = [pop(f"#s{k}i{r}", ws(wi)) for r, (wi, *_) in enumerate(items)] + [slam(f"#s{k}a", ws(758)), shake(f"#s{k}a", ws(758) + 0.2)]
    return h, j, [("pop-high", ws(wi), 0.3) for wi, *_ in items] + [("alarm", ws(758), 0.25)]


STAR = '<svg viewBox="0 0 24 24" width="{s}" height="{s}"><path d="M12 2l2.9 6.6 7.1.6-5.4 4.7 1.6 7-6.2-3.7-6.2 3.7 1.6-7L2 9.2l7.1-.6z" fill="none" stroke="#fff" stroke-width="1.6"/></svg>'


def s_wanted(k, a, b):   # wanted-level-INSPIRED (plain outline stars, own design, not the game's HUD)
    stars = "".join(f'<div class="s{k}st" style="opacity:0;">{STAR.format(s=150)}</div>' for _ in range(5))
    h = gp(k, "gameplay: police chase", dim=0.25) + veil() + (
        f'<div style="position:absolute;right:100px;top:100px;display:flex;gap:16px;">{stars}</div>'
        + txt(f"s{k}a", "LOS SANTOS MEIN WANTED LEVEL...", 90, WHITE, "position:absolute;left:90px;bottom:330px;")
        + txt(f"s{k}b", "NAHI BADHEGA", 130, ORANGE, "position:absolute;left:90px;bottom:180px;"))
    j = [ft(f".s{k}st", dict(opacity=0, scale=0), dict(opacity=1, scale=1, duration=0.2, stagger=0.12, ease="back.out(2)"), ws(766)),
         slide(f"#s{k}a", ws(763), x=-200), slam(f"#s{k}b", ws(768)), ft(f"#g{k}", dict(scale=1), dict(scale=1.12, duration=b - a, ease="none"), a)]
    return h, j, [("riser-4s", ws(770), 0.3)]


def s_problem(k, a, b):
    stars = "".join(f'<div class="s{k}st">{em("warning", 140)}</div>' for _ in range(5))
    h = (f'<div style="position:absolute;inset:0;background:linear-gradient(160deg, #7a0b0b 0%, #1a0306 75%);"></div>'
         f'<div style="position:absolute;left:0;right:0;top:120px;display:flex;justify-content:center;gap:24px;">{stars}</div>'
         + center(txt(f"s{k}a", "TUMHARI REAL LIFE MEIN", 110) + txt(f"s{k}b", "PROBLEM LEVEL BADHEGA!", 160, RED, "-webkit-text-stroke-color:#fff;"), top=200, bottom=150, gap=10))
    j = [ft(f".s{k}st", dict(opacity=0, scale=2.5), dict(opacity=1, scale=1, duration=0.18, stagger=0.08, ease="back.out(2)"), ws(773) - 0.1),
         slam(f"#s{k}a", ws(770)), slam(f"#s{k}b", ws(773), 3.4, -5),
         ft(f"#s{k}c", dict(scale=1), dict(scale=1.2, duration=0.2, ease="power4.out", immediateRender=False), ws(773)), shake(f"#s{k}c", ws(773) + 0.2, 24)]
    return h, j, [("impact-boom", ws(773), 0.5), ("sub-drop", ws(773), 0.35)]


def s_sub(k, a, b):   # guide: short subscribe animation
    h = dark() + center('<div style="display:flex;gap:60px;align-items:center;">'
                        f'<div id="s{k}l" style="display:flex;align-items:center;gap:24px;padding:30px 60px;border-radius:999px;background:#fff;opacity:0;">{em("thumbs_up", 130)}'
                        f'<div style="font-family:Anton;font-size:110px;color:#140c24;">LIKE</div></div>'
                        f'<div id="s{k}s" style="display:flex;align-items:center;gap:24px;padding:30px 60px;border-radius:999px;background:{RED};opacity:0;">{em("bell", 130)}'
                        f'<div style="font-family:Anton;font-size:110px;color:#fff;">SUBSCRIBE</div></div></div>'
                        + txt(f"s{k}a", "SARCASTIC GAMING + SCAM AWARENESS", 76, ORANGE), bottom=150, gap=50)
    j = [slide(f"#s{k}a", ws(781), y=40), pop(f"#s{k}l", ws(792)), pop(f"#s{k}s", ws(796)),
         ft(f"#s{k}s", dict(rotation=0), dict(rotation=4, duration=0.08, repeat=5, yoyo=True, immediateRender=False), ws(796) + 0.35)]
    return h, j, [("pop-high", ws(792), 0.4), ("mouse-click", ws(796), 0.8), ("pop-high", ws(796), 0.4)]


def s_final(k, a, b):   # guide: final screen text "APK SE BACHO, COMMON SENSE KO INSTALL KARO!"
    h = dark() + center(txt(f"s{k}a", "APK SE BACHO,", 170, RED)
                        + txt(f"s{k}b", "COMMON SENSE KO INSTALL KARO!", 120, GREEN) + bar(f"s{k}p", "Installing common sense...", 1100), bottom=150, gap=30)
    j = [slam(f"#s{k}a", ws(809)), slam(f"#s{k}b", ws(813), 1.8), ft(f"#s{k}pl", dict(opacity=0), dict(opacity=1, duration=0.2), ws(813)),
         ft(f"#s{k}p", dict(scaleX=0), dict(scaleX=1, duration=we(817) - ws(813) + 0.3, ease="power1.inOut"), ws(813))]
    return h, j, [("impact-punch", ws(809), 0.35), ("success-chime", we(817) + 0.3, 0.35)]


shot(0, s_hook, 0.0)
shot(17, s_10mb); shot(25, s_na); shot(48, s_pocket); shot(61, s_secret); shot(70, s_lekin); shot(77, s_scam); shot(83, s_apk)
shot(109, s_google); shot(126, s_results); shot(136, s_compressed); shot(148, s_ultra); shot(162, s_hawa); shot(173, s_rockstar)
shot(184, s_uncle); shot(203, s_nasa); shot(210, s_loading); shot(213, s_not_inside); shot(232, s_maybe); shot(250, s_milega)
shot(265, s_install); shot(287, s_sure); shot(298, s_brain); shot(315, s_side); shot(327, s_perms); shot(340, s_rishta)
shot(352, lambda k, a, b: s_char(k, a, b, "Franklin", 355, "busts", "CONTACT LIST?"))
shot(359, lambda k, a, b: s_char(k, a, b, "Michael", 361, "speech_balloon", "MESSAGES?"))
shot(366, lambda k, a, b: s_char(k, a, b, "Trevor", 371, "framed_picture", "GALLERY?!", zoom=True))
shot(377, s_risk); shot(406, s_verify)
shot(422, s_logic); shot(428, s_world); shot(435, s_stuff); shot(451, s_fit); shot(463, s_minecraft); shot(473, s_tiny); shot(487, s_jaadu)
shot(495, s_compare); shot(528, s_cloud); shot(549, s_filesize)
shot(569, s_rules); shot(589, s_tips); shot(651, s_thumb); shot(665, s_pcphone); shot(692, s_legit)
shot(717, s_bole); shot(734, s_dimaag); shot(744, s_atrisk); shot(762, s_wanted); shot(770, s_problem); shot(775, s_sub); shot(800, s_final)

# bumpers (client 2026-10-26 on the last video: pause + glitch + sound on topic change; here the heading is spoken in English)
BUMP = [(round(ws(h0) - 0.15, 3), round(we(h1) + 0.35, 3), name, sub, h0, h1) for h0, h1, name, sub in HEADS]
SH.sort(key=lambda x: x[0])

CSS = """
    @font-face { font-family: "Anton"; src: url("assets/fonts/Anton-Regular.ttf"); }
    @font-face { font-family: "Jakarta"; src: url("assets/fonts/PlusJakartaSans-Variable.ttf"); font-weight: 200 800; }
    #root { position: absolute; inset: 0; overflow: hidden; }
    .stroke { -webkit-text-stroke: 8px #0b0614; paint-order: stroke fill; }
    .gpgrad { background: linear-gradient(120deg, #3b1d5e, #c2416b 45%, #f59e42 80%, #ffd27a); background-size: 300% 300%; }
"""


def comp(cid, html, js):
    return f"""<template>
  <style>{CSS}</style>
  <div id="root" data-composition-id="{cid}" data-width="1920" data-height="1080">
{html}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{js}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
"""


C = {}
# no empty screens (guide: no black/blank frames): a design shot whose first element enters > 0.6 s after its cut
# starts later instead, so the previous shot holds over the lead-in words
import re
MEDIA_BG = {"s_google", "s_results", "s_compressed", "s_milega"}
starts = [x[0] for x in SH]
DRY[0] = True
for k, (a, fn) in enumerate(SH):
    CUR[:] = [a, a + 5]; CURFN[0] = getattr(fn, "__name__", "")
    if k == 0 or getattr(fn, "__name__", "") in MEDIA_BG or f'id="g{k}"' in fn(k, a, a + 5)[0]:
        continue
    j = fn(k, a, a + 5)[1]
    ts = [float(t) for sel, t in re.findall(r'tl\.fromTo\("([^"]+)", \{[^}]*opacity: 0[^}]*\}, \{[^}]*\}, ([\d.]+)\);', "\n".join(j))
          if re.match(rf'[#.]s{k}[a-zA-Z]', sel)]
    if ts and min(ts) - a > 0.6:
        starts[k] = round(min(ts) - 0.1, 3)
SH = [(starts[k], fn) for k, (_, fn) in enumerate(SH)]
DRY[0] = False
GP.clear()
html, js, shots_meta = [], [], []
bounds = [x[0] for x in SH] + [TOTAL]
for k, (a, fn) in enumerate(SH):
    b = bounds[k + 1]
    if a >= TOTAL:
        break
    CUR[:] = [a, b]; CURFN[0] = getattr(fn, "__name__", "")
    h, j, s = fn(k, a, b)
    vis = "block" if k == 0 else "none"
    html.append(f'    <div id="s{k}" style="position:absolute;inset:0;display:{vis};" data-layout-allow-overflow data-layout-allow-occlusion>'
                f'<div id="s{k}c" style="position:absolute;inset:0;">{h}</div></div>')
    if k:
        js.append(f'    tl.set("#s{k}", {{ display: "block" }}, {a:.3f});')
    if b < TOTAL:
        js.append(f'    tl.set("#s{k}", {{ display: "none" }}, {b:.3f});')
    js += j
    for g in GP:
        if False:
            js.append(ft(f"#g{k} .gpgrad", dict(backgroundPosition="0% 50%"), dict(backgroundPosition="100% 50%", duration=round(b - a, 3), ease="none"), a))
    SFX += [x for x in s if x[2] > 0]
    shots_meta.append(dict(k=k, a=round(a, 3), b=round(b, 3), fn=getattr(fn, "__name__", "char")))
# frame 0 (thumbnail): the title is on screen from 0 s (hook shot has no fade-in)
html[0] = html[0]
C["shots"] = comp("shots", "\n".join(html), "\n".join(js))
json.dump(dict(total=TOTAL, shots=shots_meta, gameplay_slots=[dict(k=k, desc=d) for k, d in GP]), open("shot_plan.json", "w"), indent=1)

# glitch bumpers on the spoken headings
html, js = [], []
for k, (a, b, name, sub, h0, h1) in enumerate(BUMP):
    if a >= TOTAL:
        break
    words = name.split()
    fs = min(150, int(1700 / (len(name) * 0.43)))
    sp = lambda col, lid: (f'<div id="{lid}" data-layout-allow-overlap style="position:absolute;left:0;right:0;top:440px;text-align:center;font-family:Anton;font-size:{fs}px;'
                           f'line-height:1;color:{col};white-space:nowrap;">' + "".join(f'<span class="gw{k}_{i}" style="display:inline-block;margin:0 0.13em;opacity:0;">{w}</span>' for i, w in enumerate(words)) + '</div>')
    html.append(f'    <div id="gb{k}" style="position:absolute;inset:0;opacity:0;" data-layout-allow-overflow data-layout-allow-occlusion>'
                f'<div style="position:absolute;inset:0;background:{INK};"></div>'
                f'<div id="gb{k}n" style="position:absolute;inset:-60px;background:repeating-linear-gradient(0deg, rgba(255,255,255,0.09) 0 2px, transparent 2px 4px),'
                f'repeating-linear-gradient(90deg, rgba(255,46,136,0.07) 0 3px, transparent 3px 9px);"></div>'
                f'<div data-layout-allow-overlap style="position:absolute;left:0;right:0;top:320px;text-align:center;"><span style="display:inline-block;padding:10px 30px;border-radius:12px;background:{PINK};'
                f'font-family:Jakarta;font-weight:800;font-size:44px;color:#fff;letter-spacing:6px;">{sub}</span></div>'
                f'<div id="gb{k}r" style="position:absolute;inset:0;opacity:0;mix-blend-mode:screen;">{sp("#ff1744", f"gb{k}rl")}</div>'
                f'<div id="gb{k}c" style="position:absolute;inset:0;opacity:0;mix-blend-mode:screen;">{sp("#00e5ff", f"gb{k}cl")}</div>'
                f'<div id="gb{k}w" style="position:absolute;inset:0;">{sp("#ffffff", f"gb{k}wl")}</div>'
                f'<div id="gb{k}f" style="position:absolute;inset:0;background:#fff;opacity:0;"></div></div>')
    js.append(f'    tl.fromTo("#gb{k}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.05 }}, {a:.3f});')
    js.append(f'    tl.fromTo("#gb{k}f", {{ opacity: 0.6 }}, {{ opacity: 0, duration: 0.15 }}, {a:.3f});')
    js.append(f'    tl.fromTo("#gb{k}n", {{ y: 0 }}, {{ y: 60, duration: {b - a:.3f}, ease: "steps({max(8, int((b - a) * 12))})" }}, {a:.3f});')
    bursts = []
    for bt in [a] + [ws(h0 + i) for i in range(len(words))] + [b - 0.22]:
        if not bursts or bt - bursts[-1] >= 0.26:
            bursts.append(bt)
    for n, bt in enumerate(bursts):
        d = 0.25 if n in (0, len(bursts) - 1) else 0.12
        for lid, x0 in ((f"gb{k}r", -22), (f"gb{k}c", 20)):
            js.append(f'    tl.fromTo("#{lid}", {{ opacity: 0.85, x: {x0} }}, {{ opacity: 0, x: {-x0 // 2}, duration: {d}, ease: "steps(4)", immediateRender: false }}, {bt:.3f});')
        js.append(f'    tl.fromTo("#gb{k}w", {{ x: {-12 if n % 2 else 12}, skewX: {10 if n % 2 else -10} }}, {{ x: 0, skewX: 0, duration: {d}, ease: "steps(4)", immediateRender: false }}, {bt:.3f});')
    for i in range(len(words)):
        js.append(f'    tl.fromTo(".gw{k}_{i}", {{ opacity: 0, scale: 1.6 }}, {{ opacity: 1, scale: 1, duration: 0.14, ease: "back.out(2)" }}, {ws(h0 + i) - 0.03:.3f});')
    js.append(f'    tl.to("#gb{k}", {{ opacity: 0, duration: 0.1 }}, {b - 0.1:.3f});')
    SFX += [("glitch-medium", a, 0.4), ("impact-punch", ws(h0), 0.25), ("glitch-short", b - 0.22, 0.3)]
C["bumpers"] = comp("bumpers", "\n".join(html), "\n".join(js))

# captions: word-timed Hinglish groups at the bottom; gold = important words (guide: bold + large)
html, js = [], []
for g, (i0, i1, text) in enumerate(CAP):
    st = ws(i0)
    if st >= TOTAL:
        break
    words = text.split()
    nxt = ws(CAP[g + 1][0]) if g + 1 < len(CAP) else VO_END + 0.6
    end = round(min(nxt, we(i1) + 0.5), 3)
    n = i1 - i0 + 1
    sp = []
    for m, w in enumerate(words):
        gold = w.startswith("*")
        w = w.lstrip("*").replace("_", " ")
        t = max(ws(i0 + min(n - 1, int(m * n / len(words)))), st)
        rad = ("border-radius:18px 0 0 18px;" if m == 0 else "") + ("border-radius:0 18px 18px 0;" if m == len(words) - 1 else "") if len(words) > 1 else "border-radius:18px;"
        sp.append(f'<span id="c{g}w{m}" style="display:inline-block;padding:4px 0.16em 8px;background:rgba(10,5,20,0.55);{rad}color:{ORANGE if gold else WHITE};{"font-size:1.18em;" if gold else ""}">{w}</span>')
        js.append(f'    tl.fromTo("#c{g}w{m}", {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: 0.1, ease: "power2.out" }}, {t:.3f});')
    html.append(f'    <div id="c{g}" style="position:absolute;left:160px;right:160px;top:920px;text-align:center;opacity:0;visibility:hidden;">'
                f'<div class="stroke" style="display:inline-block;font-family:Jakarta;font-weight:800;'
                f'font-size:56px;line-height:1.25;">{"".join(sp)}</div></div>')
    js.append(f'    tl.set("#c{g}", {{ opacity: 1, visibility: "visible" }}, {st:.3f});')
    js.append(f'    tl.to("#c{g}", {{ opacity: 0, duration: 0.08 }}, {end - 0.08:.3f});')
    js.append(f'    tl.set("#c{g}", {{ opacity: 0, visibility: "hidden" }}, {end:.3f});')
C["captions"] = comp("captions", "\n".join(html), "\n".join(js))

os.makedirs("compositions", exist_ok=True)
for k, v in C.items():
    open(f"compositions/{k}.html", "w").write(v)


def dur(p):
    return round(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                      capture_output=True, text=True).stdout), 3)


LONG = {"typing-keyboard-fast", "thruster", "riser-2s", "riser-4s", "badumtss"}
PLAN = []
# client 2026-10-28: "popup sounds alag alag use karo, same sound baar baar repeat lag raha hai, 2-3 type" -> rotate variants
VARIANTS = {"pop-high": ["pop-high", "bubble-pop", "plop"], "whoosh-fast-0.3s": ["whoosh-fast-0.3s", "swish-1", "whoosh-up-0.6s"],
            "impact-punch": ["impact-punch", "punch-medium", "punch-heavy"]}
_rot, _sfx = {}, []
for n, t, v in sorted(SFX, key=lambda x: x[1]):
    if n in VARIANTS:
        c = _rot.get(n, 0); _rot[n] = c + 1
        n = VARIANTS[n][c % len(VARIANTS[n])]
    _sfx.append((n, t, v))
SFX = _sfx
for name, t, v in SFX:
    if t >= TOTAL or name not in HITS:
        continue
    hit = HITS[name]["peak"] if name.startswith("riser") else (HITS[name]["onset"] if name in LONG else HITS[name]["peak"])
    st = round(max(0, t - hit), 3)
    d = 2.6 if name == "typing-keyboard-fast" else HITS[name]["dur"]
    PLAN.append(dict(name=name, hit=round(t, 3), start=st, dur=round(min(d, TOTAL - st), 3)))
json.dump(PLAN, open("sfx_plan.json", "w"), indent=0)
A = [("mix", "assets/mix.wav", 0, TOTAL, 1.0, 10)]   # mix.py: VO + ducked bed + level-matched SFX
aud = "\n".join(f'      <audio id="{i}" src="{s}" data-start="{st}" data-duration="{d}" data-volume="{v}" data-track-index="{ln}"></audio>' for i, s, st, d, v, ln in A)
hosts = "\n".join(
    f'      <div id="{c}-h" data-composition-id="{c}" data-composition-src="compositions/{c}.html" data-start="0" data-duration="{TOTAL}" data-track-index="{i}" '
    f'data-track-kind="{"captions" if c == "captions" else "graphics"}" data-width="1920" data-height="1080" style="z-index: {i}"></div>'
    for i, c in enumerate(["shots", "bumpers", "captions"]))
open("index.html", "w").write(f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="assets/vendor/gsap-3.14.2.min.js"></script>
    <style>* {{ margin: 0; padding: 0; box-sizing: border-box; }} html, body {{ margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: {BG}; }}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1920" data-height="1080">
{hosts}
{aud}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
""")
print("built", TOTAL, "shots", len(shots_meta), "sfx", len(PLAN), "gameplay slots", len(GP))
