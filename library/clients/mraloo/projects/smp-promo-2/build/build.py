# ALOO SMP Promo 2, 60 s YouTube Short 1080x1920. Client VO "aloosmp promo 2.mp3" (retake + dead air cut, vo_edit.py),
# client editing guide (library/clients/mraloo/projects/smp-promo-2/editing-guide.txt) second by second.
# Footage = the client's two ALOO SMP recordings, mostly parts the first Short did not use (client: "alag-alag footage").
# HOOK=B builds the alternate first-5-s hook (guide deliverable); the rest of the edit is identical.
import json, os, subprocess, sys

HOOK = os.environ.get("HOOK", "A")
SRC = "/tmp/claude-0/-home-user-new-startup/d818cf68-9ee4-503e-aa36-a24c445c7006/scratchpad/promo2/src"
W = json.load(open("words.json"))
from captions import CAP
VO_END = W[-1][1]
TOTAL = 62.5
HITS = json.load(open("sfx_hits.json"))
GOLD, ORANGE, ICE, ICE2, NAVY, RED, GREEN = "#fcb43c", "#fc9c24", "#84ccfc", "#cce4fc", "#0c0c24", "#ef4444", "#22c55e"   # emblem colours (brief.md)


def ws(i):
    return W[i][0]


def we(i):
    return W[i][1]


def o(d):
    return "{ " + ", ".join(f"{k}: {json.dumps(v)}" for k, v in d.items()) + " }"


def ft(sel, a, b, t):
    return f'    tl.fromTo("{sel}", {o(a)}, {o(b)}, {t:.3f});'


def slam(sel, t, s=2.0, r=0):
    return ft(sel, dict(opacity=0, scale=s, rotation=r), dict(opacity=1, scale=1, rotation=r * 0, duration=0.24, ease="back.out(2)"), t - 0.05)


def pop(sel, t, d=0.28):
    return ft(sel, dict(opacity=0, scale=0.3), dict(opacity=1, scale=1, duration=d, ease="back.out(2.2)"), t - 0.05)


def out_(sel, t, d=0.18):
    return f'    tl.to("{sel}", {o(dict(opacity=0, scale=0.8, duration=d, ease="power2.in"))}, {t - d:.3f});'


def shake(sel, t, amp=14):
    return ft(sel, dict(x=-amp, y=amp // 2), dict(x=0, y=0, duration=0.05, repeat=4, yoyo=True, immediateRender=False), t)


# ---------------------------------------------------------------- shots: (start, source, in-point, crop-x-centre 0..1, why)
# rec182 = "2026-10-25 20-34-02.mkv" (Drive 1SmJKT0fOUn--o94gnSx_Pg3D4gq5wpwA), spawn51 = "2026-10-25 20-24-48.mkv"
# (Drive 16nhkyo2QlKAAevAWaIz2osWhvI8kQOri); in-points from 2 s contact sheets (look/*.jpg). Avoided: connecting screens,
# YOU ARE AFK (rec 26-50), creative-mode chat (96-100), the white frame (162), chat lines in the crop.
R, S = "rec182.mkv", "spawn51.mkv"
SH = [
    (0.0, R, 21.8, 0.50, "hook: character alone in the desert (guide 0-3 s; 21.8-22.6 is the only stretch without tab list or plugin chat in the crop, frames checked every 0.2 s)"),
    (0.75, R, 120.4, 0.50, "alone on the grass, looking around"),
    (ws(5) - 0.05, R, 0.4, 0.45, "'itne saare servers': the real multiplayer server list"),
    (ws(14), S, 20.0, 0.50, "'achha server nahi mil raha': alone at spawn"),
    (ws(20), S, 36.0, 0.50, "'bade server pe jao, hazaaron players': busy spawn crowd (guide 3-8 s)"),
    (ws(28), R, 124.2, 0.50, "'par bhai, kisi ko jaante hi nahi': hard cut to the lonely character"),
    (ws(36), S, 24.0, 0.50, "'sab apna apna khel rahe hain': players walking past"),
    (ws(42), R, 128.2, 0.50, "'aur main join kar ke sochta tha': walking alone"),
    (ws(49), R, 132.4, 0.50, "'karun to karun kya idhar': standing in front of a house"),
    (ws(55), R, 84.4, 0.50, "'phir maine socha': beat shift to the server's builds (guide 15-23 s)"),
    (ws(63), R, 88.6, 0.50, "'khud ka hi ek SMP banate hain'"),
    (ws(69), S, 28.0, 0.50, "'friends ke saath khelenge': players together"),
    (ws(74), S, 6.0, 0.40, "'baaki players bhi join kar sakenge': the real ALOO SMP >> Welcome join message"),
    (ws(81), R, 104.0, 0.50, "'aur wahin se shuru hua': clean flyover into the reveal"),
    (ws(86) - 0.08, R, 116.2, 0.50, "ALOO SMP reveal (logo over the best clean server shot, guide 23-32 s)"),
    (ws(94), R, 108.4, 0.50, "survive"),
    (ws(100), R, 56.4, 0.50, "economy: shop with a player's balance"),
    (ws(106), S, 32.0, 0.50, "PvP: another player close up"),
    (ws(111), R, 92.2, 0.50, "custom enchants"),
    (ws(118), S, 40.0, 0.50, "'friends ke saath full maze': crowd of players (guide 42-51 s)"),
    (ws(128), S, 12.4, 0.50, "'tum ek normal player banke join karoge': walking into spawn"),
    (ws(137), R, 118.2, 0.50, "'kal tumhara khud ka base hoga'"),
    (ws(142), S, 44.4, 0.50, "'apni team hogi'"),
    (ws(145), R, 62.0, 0.55, "'server pe tumhari alag pehchaan': a player's nametag with stats"),
    (ws(152), R, 134.4, 0.50, "'to bhai, kya kar rahe ho, akele Minecraft khelna band karo'"),
    (ws(162), R, 168.6, 0.50, "'aur join karo ALOO SMP': active market (guide 51-60 s: end on an active shot)"),
    (ws(167) - 0.1, S, 20.0, 0.50, "end card plate (IP / port / Discord), blurred"),
]
if HOOK == "B":   # alternate hook: open on the busy crowd + the 1000 vs 0 joke, then the server list (same VO)
    SH[0] = (0.0, S, 38.0, 0.50, "hook B: busy spawn crowd")
    SH[1] = (0.75, S, 40.5, 0.50, "busy spawn crowd")
    SH[2] = (ws(5) - 0.05, R, 0.4, 0.45, "server list")
    SH[3] = (ws(14), R, 120.4, 0.50, "alone on the grass")
os.makedirs("assets/clips", exist_ok=True)
SHOTS = []
for k, (st, src, inp, cx, why) in enumerate(SH):
    end = SH[k + 1][0] if k + 1 < len(SH) else TOTAL
    d = round(end - st, 3)
    blur = k == len(SH) - 1
    fill = "Welcome join message" in why          # whole frame over a blurred copy so the chat line stays readable (template mode "fill")
    out = f"assets/clips/{HOOK}{k:02d}_{inp}_{d:.2f}.mp4"
    if not os.path.exists(out):
        x = int(max(0, min(1920 - 608, 1920 * cx - 304)))               # sources are 1920x1080
        vf = f"crop=608:1080:{x}:0,scale=1080:1920:flags=lanczos,cas=strength=0.5,fps=60"
        if blur:
            vf += ",boxblur=18:8,eq=brightness=-0.10"
        args = ["-vf", vf]
        if fill:
            args = ["-filter_complex", "[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=20:10,eq=brightness=-0.12[bg];"
                    "[b]scale=1080:-2:flags=lanczos,cas=strength=0.5[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2-120,fps=60[o]", "-map", "[o]"]
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(inp), "-t", f"{d + 0.1:.3f}", "-i", f"{SRC}/{src}", "-an", *args,
                        "-c:v", "libx264", "-crf", "17", "-preset", "veryfast", "-g", "60", "-pix_fmt", "yuv420p", out], check=True)
    SHOTS.append(dict(k=k, start=round(st, 3), dur=d, file=out, why=why, src=src, inp=inp))
json.dump(SHOTS, open(f"shots_{HOOK}.json", "w"), indent=1)

CSS = f"""
    @font-face {{ font-family: "Anton"; src: url("assets/fonts/Anton-Regular.ttf"); }}
    @font-face {{ font-family: "Jakarta"; src: url("assets/fonts/PlusJakartaSans-Variable.ttf"); font-weight: 200 800; }}
    #root {{ position: absolute; inset: 0; overflow: hidden; }}
    .c {{ position: absolute; left: 0; right: 0; text-align: center; }}
    .anton {{ font-family: Anton; letter-spacing: 2px; line-height: 0.95; }}
    .jk {{ font-family: Jakarta; font-weight: 800; }}
    .stroke {{ -webkit-text-stroke: 10px {NAVY}; paint-order: stroke fill; }}
    .chip {{ display: inline-flex; align-items: center; gap: 18px; padding: 16px 34px; border-radius: 22px; background: rgba(12,12,36,0.88);
             border: 4px solid {ICE}; color: #fff; font-family: Jakarta; font-weight: 800; font-size: 54px; box-shadow: 0 14px 40px rgba(0,0,0,0.5); }}
"""


def comp(cid, html, js):
    return f"""<template>
  <style>{CSS}</style>
  <div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920">
{html}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{js}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
"""


C, SFX = {}, []
# ---------------------------------------------------------------- footage: hard cuts (guide: "mostly hard cuts"), punch-ins on the jokes
html, js = [], []
PUNCH = {0: ws(0), 8: ws(53), 5: ws(34)}                # "Bhai" (guide: quick punch-in), "kya?" (tiny zoom for the punchline), "nahi ho"
for s in SHOTS:
    k, st, d = s["k"], s["start"], s["dur"]
    html.append(f'    <div id="w{k}" style="position:absolute;inset:0;" data-layout-allow-overflow><video id="v{k}" src="{s["file"]}" data-start="{st}" '
                f'data-duration="{d}" muted playsinline style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;"></video></div>')
    if k in PUNCH:
        t = PUNCH[k]
        js.append(ft(f"#w{k}", dict(scale=1.0), dict(scale=1.18, duration=0.12, ease="power4.out"), max(st, t - 0.04)))
        js.append(f'    tl.to("#w{k}", {o(dict(scale=1.0, duration=0.4, ease="power2.out"))}, {min(st + d - 0.4, t + 0.5):.3f});')
C["footage"] = comp("footage", "\n".join(html), "\n".join(js))

# ---------------------------------------------------------------- text moments (guide timeline "SOUND / TEXT" column)
html, js = [], []
def moment(mid, inner, a, b, jj):
    vis = 1 if a <= 0.02 else 0                                       # frame 0 = thumbnail: hook text visible inline
    html.append(f'    <div id="{mid}" style="position:absolute;inset:0;opacity:{vis};" data-layout-allow-overflow data-layout-allow-occlusion>{inner}</div>')
    if a > 0.02:
        js.append(ft(f"#{mid}", dict(opacity=0), dict(opacity=1, duration=0.06), a - 0.02))
    js.extend(jj)
    js.append(f'    tl.to("#{mid}", {o(dict(opacity=0, duration=0.15))}, {b - 0.15:.3f});')


TOP = '<div style="position:absolute;left:0;right:0;top:0;height:820px;background:linear-gradient(to bottom, rgba(12,12,36,0.78), rgba(12,12,36,0));"></div>'
if HOOK == "A":   # guide 0-3 s: Text "SERVER MILA HI NAHI?" on frame 0 (thumbnail), caption within 0.2 s
    moment("m0", TOP + '<div id="m0t" class="c" style="top:280px;"><div class="anton stroke" style="font-size:150px;color:#fff;">SERVER</div>'
           f'<div class="anton stroke" style="font-size:170px;color:{GOLD};">MILA HI NAHI?</div></div>', 0.0, ws(5) - 0.05,
           [ft("#m0t", dict(scale=1.15), dict(scale=1, duration=0.6, ease="power2.out"), 0.0)])
    SFX.append(("pop-high", 0.02))
else:            # hook B: the 1000 vs 0 contrast up front
    moment("m0", TOP + f'<div id="m0t" class="c" style="top:260px;"><div class="anton stroke" style="font-size:120px;color:#fff;">1000 PLAYERS</div>'
           f'<div class="anton stroke" style="font-size:150px;color:{RED};">0 FRIENDS?</div></div>', 0.0, ws(5) - 0.05,
           [ft("#m0t", dict(scale=1.15), dict(scale=1, duration=0.6, ease="power2.out"), 0.0)])
    SFX.append(("record-scratch", 0.05))

# guide 3-8 s: "Players: 1000 / Friends: 0" (big servers, a joke about other servers, not a claim about ALOO SMP)
moment("m1", TOP + f'<div class="c" style="top:300px;"><span id="m1a" class="chip" style="font-size:80px;border-color:{GREEN};opacity:0;">PLAYERS: 1000</span></div>'
       f'<div class="c" style="top:470px;"><span id="m1b" class="chip" style="font-size:80px;border-color:{RED};opacity:0;">FRIENDS: 0</span></div>',
       ws(25) - 0.05, ws(36),
       [pop("#m1a", ws(25)), slam("#m1b", ws(30), 2.2), shake("#m1b", ws(30) + 0.22)])
SFX += [("pop-high", ws(25)), ("impact-punch", ws(30))]
SFX += [("trombone", we(35) + 0.1)]                                  # guide: one joke sound, after the joke, 0.5-1 s
# guide 8-15 s: tiny impact on "kya?"
SFX += [("punch-medium", ws(53))]
# guide 15-23 s: "TOH KHUD KA SMP BANAYA..."
moment("m2", TOP + f'<div id="m2t" class="c" style="top:300px;"><div class="anton stroke" style="font-size:110px;color:#fff;">TOH KHUD KA</div>'
       f'<div class="anton stroke" style="font-size:150px;color:{GOLD};">SMP BANAYA...</div></div>', ws(63) - 0.05, ws(74),
       [slam("#m2t", ws(63), 1.4)])
SFX += [("whoosh-fast-0.3s", ws(55) - 0.05), ("swish-1", ws(63))]
# guide 23-32 s: reveal, beat hit on "ALOO SMP", logo ~1.5 s
R0 = ws(86) - 0.08
moment("m3", f'<div id="m3f" style="position:absolute;inset:0;background:#fffdf5;"></div>'
       f'<div id="m3c" style="position:absolute;left:190px;top:420px;width:700px;height:700px;border-radius:60px;overflow:hidden;border:6px solid {GOLD};'
       f'box-shadow:0 30px 80px rgba(0,0,0,0.6), 0 0 80px rgba(252,180,60,0.5);"><img src="assets/img/emblem.jpg" style="width:100%;height:100%;object-fit:cover;" alt="ALOO SMP emblem"></div>',
       R0, R0 + 1.6,
       [ft("#m3f", dict(opacity=0.95), dict(opacity=0, duration=0.45, ease="power2.out"), R0),
        ft("#m3c", dict(scale=1.6, rotation=-6, opacity=0), dict(scale=1, rotation=0, opacity=1, duration=0.32, ease="power4.out"), R0),
        shake("#m3c", R0 + 0.32, 12)])
SFX += [("riser-2s", R0), ("impact-boom", R0)]
# guide 32-42 s: one label per feature word, 1-1.5 s each
FEAT = [(96, "SURVIVAL"), (101, "ECONOMY"), (106, "PvP"), (111, "CUSTOM ENCHANTS"), (122, "FRIENDS KE SAATH")]
for n, (wi, lab) in enumerate(FEAT):
    end = ws(FEAT[n + 1][0]) - 0.1 if n + 1 < len(FEAT) else ws(128)
    moment(f"f{n}", f'<div class="c" style="top:330px;"><span id="f{n}t" class="chip" style="font-size:72px;border-color:{GOLD};">{lab}</span></div>', ws(wi) - 0.08, end,
           [pop(f"#f{n}t", ws(wi))])
    SFX.append((["pop-high", "bubble-pop", "plop"][n % 3], ws(wi)))
SFX += [("whoosh-up-0.6s", ws(106) - 0.1)]
# guide 42-51 s: "APNI STORY START KARO"
moment("m4", f'<div class="c" style="top:330px;"><span id="m4a" class="chip" style="font-size:66px;opacity:0;">APNA BASE</span></div>'
       f'<div class="c" style="top:470px;"><span id="m4b" class="chip" style="font-size:66px;opacity:0;">APNI TEAM</span></div>'
       f'<div class="c" style="top:610px;"><span id="m4c" class="chip" style="font-size:66px;border-color:{GOLD};opacity:0;">APNI PEHCHAAN</span></div>',
       ws(140) - 0.1, ws(152),
       [pop("#m4a", ws(140)), pop("#m4b", ws(143)), pop("#m4c", ws(149))])
SFX += [("pop-high", ws(140)), ("bubble-pop", ws(143)), ("game-levelup", ws(149))]
moment("m5", TOP + f'<div id="m5t" class="c" style="top:300px;"><div class="anton stroke" style="font-size:120px;color:#fff;">APNI STORY</div>'
       f'<div class="anton stroke" style="font-size:150px;color:{GOLD};">START KARO</div></div>', ws(157), ws(165) - 0.1,
       [slam("#m5t", ws(157), 1.5)])
SFX += [("impact-punch", ws(157))]
moment("m6", f'<div id="m6t" class="c" style="top:330px;"><div class="anton stroke" style="font-size:130px;color:{GOLD};">JOIN ALOO SMP</div></div>', ws(165) - 0.08, ws(167) - 0.1,
       [slam("#m6t", ws(165), 1.6)])
SFX += [("success-chime", ws(165))]
C["moments"] = comp("moments", "\n".join(html), "\n".join(js))

# ---------------------------------------------------------------- end card (guide 51-60 s: IP + port + Java/Bedrock + Discord, 5-7 s,
# no distracting effects; client data brief.md: play.aloosmp.fun, Bedrock port 19132, discord.gg/e89HSbjd5Y)
E0 = ws(167) - 0.1
end_html = f"""    <div id="e-w" style="position:absolute;inset:0;">
      <div id="e-logo" style="position:absolute;left:360px;top:230px;width:360px;height:360px;border-radius:40px;overflow:hidden;border:5px solid {GOLD};box-shadow:0 0 60px rgba(252,180,60,0.45);opacity:0;">
        <img src="assets/img/emblem.jpg" style="width:100%;height:100%;object-fit:cover;" alt="ALOO SMP emblem"></div>
      <div class="c" style="top:650px;"><span id="e-ip" class="chip" style="font-size:62px;border-color:{GOLD};opacity:0;"><span style="color:{GOLD};">IP</span>play.aloosmp.fun</span></div>
      <div class="c" style="top:790px;"><span id="e-port" class="chip" style="font-size:52px;opacity:0;"><span style="color:{ICE};">PORT</span>19132 <span style="font-size:38px;color:{ICE2};">(Bedrock)</span></span></div>
      <div class="c" style="top:920px;"><span id="e-ed" class="chip" style="font-size:52px;border-color:{GREEN};opacity:0;">JAVA + BEDROCK</span></div>
      <div class="c" style="top:1050px;"><span id="e-dc" class="chip" style="font-size:46px;border-color:#5865f2;opacity:0;"><span style="color:#8b93ff;">DISCORD</span>discord.gg/e89HSbjd5Y</span></div>
      <div id="e-desc" class="c jk stroke" style="top:1170px;font-size:46px;color:#fff;opacity:0;">Link description mein</div>
    </div>"""
ej = [pop("#e-logo", 0.15), pop("#e-ip", ws(167) - E0), pop("#e-port", ws(168) - E0), pop("#e-ed", ws(169) - E0),
      pop("#e-dc", ws(176) - E0), ft("#e-desc", dict(opacity=0, y=30), dict(opacity=1, y=0, duration=0.3), ws(180) - E0)]
C["end"] = comp("end", end_html, "\n".join(ej))
SFX += [("whoosh-fast-0.3s", E0), ("pop-high", ws(167)), ("plop", ws(176))]

# ---------------------------------------------------------------- captions: Hinglish, 3-6 words, gold keywords, centre-lower safe area
html, js = [], []
for g, (i0, i1, text) in enumerate(CAP):
    st = ws(i0)
    words = text.split()
    nxt = ws(CAP[g + 1][0]) if g + 1 < len(CAP) else VO_END + 0.6
    end = round(min(nxt, we(i1) + 0.45), 3)
    n = i1 - i0 + 1
    sp = []
    for m, w in enumerate(words):
        gold = w.startswith("*")
        w = w.lstrip("*").replace("_", " ")
        t = max(ws(i0 + min(n - 1, int(m * n / len(words)))), st)
        sp.append(f'<span id="c{g}w{m}" style="display:inline-block;margin:0 0.12em;color:{GOLD if gold else "#fff"};">{w}</span>')
        js.append(f'    tl.fromTo("#c{g}w{m}", {{ opacity: 0, scale: 0.6, y: 16 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.12, ease: "back.out(2.5)" }}, {t:.3f});')
    top = 1330 if st < E0 else 1420
    html.append(f'    <div id="c{g}" class="c jk stroke" style="top:{top}px;padding:0 70px;font-size:80px;line-height:1.08;opacity:0;visibility:hidden;'
                f'text-shadow:0 6px 22px rgba(0,0,0,0.8);">{" ".join(sp)}</div>')
    js.append(f'    tl.set("#c{g}", {{ opacity: 1, visibility: "visible" }}, {st:.3f});')
    js.append(f'    tl.to("#c{g}", {{ opacity: 0, duration: 0.08 }}, {end - 0.08:.3f});')
    js.append(f'    tl.set("#c{g}", {{ opacity: 0, visibility: "hidden" }}, {end:.3f});')
C["captions"] = comp("captions", "\n".join(html), "\n".join(js))

os.makedirs("compositions", exist_ok=True)
for k, v in C.items():
    open(f"compositions/{k}.html", "w").write(v)

PLAN = []
for name, t in sorted(SFX, key=lambda x: x[1]):
    hit = HITS[name]["peak"]
    st = round(max(0, t - hit), 3)
    d = 1.0 if name == "trombone" else HITS[name]["dur"]
    PLAN.append(dict(name=name, hit=round(t, 3), start=st, dur=round(min(d, TOTAL - st), 3)))
json.dump(PLAN, open("sfx_plan.json", "w"), indent=0)
json.dump(dict(total=TOTAL, reveal=round(R0, 3), lift=round(ws(55), 3), end_card=round(E0, 3)), open("timing.json", "w"))
hosts = "\n".join(
    f'      <div id="{c}-h" data-composition-id="{c}" data-composition-src="compositions/{c}.html" data-start="{st}" data-duration="{round(TOTAL - st, 3)}" data-track-index="{i}" '
    f'data-track-kind="{"captions" if c == "captions" else "graphics"}" data-width="1080" data-height="1920" style="z-index: {i}"></div>'
    for i, (c, st) in enumerate([("footage", 0), ("moments", 0), ("end", round(E0, 3)), ("captions", 0)]))
open("index.html", "w").write(f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap-3.14.2.min.js"></script>
    <style>* {{ margin: 0; padding: 0; box-sizing: border-box; }} html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: {NAVY}; }}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-fps="60" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
{hosts}
      <audio id="mix" src="assets/mix.wav" data-start="0" data-duration="{TOTAL}" data-volume="1.0" data-track-index="10"></audio>
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
""")
print("built", HOOK, TOTAL, "shots", len(SHOTS), "captions", len(CAP), "sfx", len(PLAN))
