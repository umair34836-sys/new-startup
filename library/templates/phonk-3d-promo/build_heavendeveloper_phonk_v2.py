# Heaven Developer PHONK 3D promo v2: "formula v2" after the owner said v1 "bhot boring sa lag raha hai ... upgrade it and
# upgrade your formula" (2026-10-29). Research + sources: library/research/phonk-edit-formula.md. What changed vs v1:
#  - a hard CUT ON EVERY BEAT: each beat is a new camera shot of the 3D character (wide / face close-up / low hero /
#    dutch / side / back / top), not one static framing per VO line;
#  - 808 KICKS -> 6% impact zoom with fast snap-back (kicks from library/tools/beat_events.py);
#  - STRONG KICKS -> 1-frame white flash (~120 ms decay); SNARES -> RGB split + cold high-contrast grade + grain are done
#    after the render in ffmpeg (post.sh written next to index.html);
#  - depth: giant outlined words BEHIND the character, real Heaven material IN the frame (logo, orders banner), a crowd
#    of character clones for the member count, speed-ramped moves (expo in/out), a jump on the drop;
#  - "hit hard and breathe": the music-only bar keeps cutting on beats but holds the text.
# Facts: library/clients/heavendeveloper/brief.md. Skin: the client's own 64x64 skin (scratchpad, never committed).
import importlib.util, json, os, subprocess

spec = importlib.util.spec_from_file_location("bc", "/home/user/new-startup/library/tools/blocky_character.py")
bc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bc)

VO_START = 0.3
BG, BLURPLE, GREEN, GOLD, WHITE, RED = "#04030a", "#5865f2", "#58b234", "#f7dc94", "#ffffff", "#ff2a55"
L = json.load(open("assets/vo/lines.json"))
EV = json.load(open("assets/music/events.json"))
TOTAL = float(os.environ.get("TOTAL", 30.0))
BEATS = [b for b in EV["beats"] if b < TOTAL]
# kicks for punches: strong enough and >= 0.3 s apart (raw low-band onsets include ghost notes)
KICKS, last = [], -9
for t, s in EV["kicks"]:
    if s >= 0.38 and t - last >= 0.35:
        KICKS.append(t); last = t
STRONG = [t for t, s in EV["strong_kicks"] if t < TOTAL - 0.3]
st = [round(VO_START + a - 0.1, 2) for a, _ in L]
st[0] = 0.0
SCENES = [(f"s{i + 1}", st[i], st[i + 1] if i + 1 < len(st) else TOTAL) for i in range(len(st))]
W = {k: (s, e) for k, s, e in SCENES}
SKIN = "assets/characters/bhupendra-skin.png"
SC = 20  # px per skin pixel: character 640 px tall


def dur(p):
    return round(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                      capture_output=True, text=True).stdout), 3)


def rel(i, frac):
    a, b = L[i]
    return round(max(0.05, VO_START + a + frac * (b - a) - st[i]), 2)


def d_of(i):
    s, e = W[f"s{i + 1}"]
    return round(e - s, 2)


def inside(i, times, pad=0.05):
    s, e = W[f"s{i + 1}"]
    return [round(t - s, 3) for t in times if s + pad < t < e - 0.25]


CSS = f"""
    @font-face {{ font-family: "AN"; src: url("assets/fonts/Anton-Regular.ttf"); }}
    @font-face {{ font-family: "OU"; src: url("assets/fonts/Outfit-Bold.ttf"); font-weight: 700; }}
    #root {{ position: absolute; inset: 0; overflow: hidden; }}
    .c {{ position: absolute; left: 0; right: 0; text-align: center; }}
    .slam {{ font-family: AN; line-height: 0.92; color: {WHITE}; text-transform: uppercase;
             text-shadow: -5px 0 0 rgba(255,42,85,0.8), 5px 0 0 rgba(40,220,255,0.8), 0 12px 44px rgba(0,0,0,0.85); }}
    .ghost {{ font-family: AN; line-height: 0.85; color: rgba(150,160,255,0.16); -webkit-text-stroke: 4px rgba(255,255,255,0.22); text-transform: uppercase; white-space: nowrap; }}
    .sub {{ font-family: OU; font-weight: 700; color: {GOLD}; letter-spacing: 3px; text-shadow: 0 6px 24px rgba(0,0,0,0.9); }}
    .btn {{ display: inline-flex; align-items: center; gap: 24px; background: {BLURPLE}; color: #fff; font-family: AN;
            border-radius: 22px; padding: 26px 56px; font-size: 76px; box-shadow: 0 18px 60px rgba(88,101,242,0.6); }}
    .bars {{ position: absolute; left: 0; right: 0; height: 170px; background: #000; }}
"""
DISCORD = '<path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0 12.64 12.64 0 0 0-.617-1.25.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 0 0 .031.057 19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028c.462-.63.874-1.295 1.226-1.994a.076.076 0 0 0-.041-.106 13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.128 10.2 10.2 0 0 0 .372-.292.074.074 0 0 1 .077-.01c3.929 1.793 8.18 1.793 12.061 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127 12.299 12.299 0 0 1-1.873.894.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.028zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.955-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.946 2.418-2.157 2.418z"></path>'

# camera presets: scale about the feet point, offsets in px, yaw (turn of the character), pitch (camera tilt), roll
SHOT = {
    "wide":  dict(s=1.0, x=0, y=0, yaw=-22, pitch=-6, roll=0),
    "face":  dict(s=2.25, x=0, y=900, yaw=-12, pitch=-2, roll=0),
    "low":   dict(s=1.45, x=0, y=180, yaw=28, pitch=16, roll=0),
    "dutch": dict(s=1.25, x=40, y=120, yaw=-45, pitch=-4, roll=-11),
    "side":  dict(s=1.3, x=-60, y=120, yaw=85, pitch=-4, roll=0),
    "back":  dict(s=1.15, x=0, y=60, yaw=165, pitch=-8, roll=0),
    "top":   dict(s=1.1, x=0, y=-60, yaw=-30, pitch=-30, roll=5),
    "hero":  dict(s=1.7, x=0, y=420, yaw=10, pitch=10, roll=0),
}


def character(P, d, moves, shots, x=540, y=1650):
    """3D character with a camera wrapper: on every time in `shots` [(t, preset)] the camera hard-cuts to that preset."""
    s0 = SHOT[shots[0][1]]
    html = (f'<div style="position:absolute;left:{x}px;top:{y}px;width:0;height:0;perspective:{80 * SC}px;perspective-origin:0 {-16 * SC}px;">'
            f'<div id="{P}-cam" style="position:absolute;left:0;top:0;width:0;height:0;transform-style:preserve-3d;">'
            f'<div id="{P}-move" style="position:absolute;left:0;top:0;width:0;height:0;transform-style:preserve-3d;">'
            f'<div id="{P}-yaw" style="position:absolute;left:0;top:0;width:0;height:0;transform-style:preserve-3d;">\n'
            f'{bc.rig_html(P, SC, "      ")}\n      </div></div></div></div>')
    js = "\n".join(bc.pose_js(P, SC, moves, d, 0)) + "\n"
    js += (f'    gsap.set("#{P}-cam", {{ scale: {s0["s"]}, x: {s0["x"]}, y: {s0["y"]}, rotationX: {s0["pitch"]}, rotationZ: {s0["roll"]} }});\n'
           f'    gsap.set("#{P}-yaw", {{ rotationY: {s0["yaw"]} }});\n')
    for t, name in shots:
        p = SHOT[name]
        js += (f'    tl.set("#{P}-cam", {{ scale: {p["s"]}, x: {p["x"]}, y: {p["y"]}, rotationX: {p["pitch"]}, rotationZ: {p["roll"]} }}, {t:.3f});\n'
               f'    tl.set("#{P}-yaw", {{ rotationY: {p["yaw"]} }}, {t:.3f});\n')
        # a small push inside the shot keeps it alive between cuts (velocity feel)
        js += f'    tl.fromTo("#{P}-move", {{ scale: 1.0 }}, {{ scale: 1.05, duration: 0.7, ease: "expo.out", immediateRender: false }}, {t:.3f});\n'
    return html, js, bc.css(P, SKIN)


def shot_plan(i, cycle):
    """a new shot on every beat of scene i (cut on the beat, skill #372 lands it 1 frame early)"""
    times = [0.0] + [max(0.0, b - 0.033) for b in inside(i, BEATS)]
    return [(t, cycle[n % len(cycle)]) for n, t in enumerate(times)]


def slam(sel, at, frm="scale: 2.6, opacity: 0", d=0.2):
    return f'    tl.fromTo("{sel}", {{ {frm} }}, {{ scale: 1, x: 0, y: 0, rotationX: 0, opacity: 1, duration: {d}, ease: "power4.out" }}, {at:.2f});\n'


def shake(sel, at):
    return f'    tl.fromTo("{sel}", {{ x: -12, y: 7 }}, {{ x: 10, y: -5, duration: 0.045, ease: "none", repeat: 4, yoyo: true, immediateRender: false }}, {at:.2f});\n'


def punches(i, k):
    """808 kick -> 6% impact zoom with a fast snap-back (Onset Engine formula)"""
    return "".join(f'    tl.fromTo("#{k}-w", {{ scale: 1.06 }}, {{ scale: 1, duration: 0.24, ease: "expo.out", immediateRender: false }}, {t:.3f});\n'
                   for t in inside(i, KICKS))


def ghost(k, word, top=760, size=420):
    """giant outlined word behind the character (depth), drifting"""
    return (f'<div class="c ghost" id="{k}-gh" style="top:{top}px;font-size:{size}px;">{word}</div>',
            f'    tl.fromTo("#{k}-gh", {{ x: 160 }}, {{ x: -160, duration: {d_of(int(k[1:]) - 1)}, ease: "none" }}, 0);\n')


def comp(cid, html, js, extra_css=""):
    d = round(W[cid][1] - W[cid][0], 2) if cid in W else TOTAL
    return f"""<template>
  <style>{CSS}{extra_css}</style>
  <div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920" data-layout-allow-overflow>
{html}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{js}
    tl.to({{}}, {{ duration: {d} }}, 0);
    window.__timelines["{cid}"] = tl;
  </script>
</template>
"""


def scene(k, i, back, chars, front, js, ccss, exit_=True):
    d = d_of(i)
    js = js + punches(i, k) + shake(f"#{k}-w", 0.0)
    if exit_:
        js += f'    tl.to("#{k}-w", {{ scale: 1.3, opacity: 0, filter: "blur(14px)", duration: 0.14, ease: "power3.in" }}, {d - 0.14:.2f});\n'
    html = f'    <div id="{k}-w" style="position:absolute;inset:0;transform-origin:50% 55%;">\n{back}\n{chars}\n{front}\n    </div>'
    return comp(k, html, js, ccss)


C, HITS, BIG = {}, [], []
# background: near-black, neon glows, moving grid floor, scanlines, beat pulses
pulses = "".join(f'    tl.fromTo("#bg-p", {{ opacity: 0.5 }}, {{ opacity: 0, duration: 0.3, ease: "power2.out", immediateRender: false }}, {b:.3f});\n' for b in BEATS)
C["bg"] = comp("bg", f"""    <div style="position:absolute;inset:0;background:{BG};"></div>
    <div id="bg-g1" style="position:absolute;left:-300px;top:200px;width:1200px;height:1200px;border-radius:50%;background:radial-gradient(circle, rgba(88,101,242,0.38), rgba(88,101,242,0) 70%);"></div>
    <div id="bg-g2" style="position:absolute;left:300px;top:900px;width:1100px;height:1100px;border-radius:50%;background:radial-gradient(circle, rgba(255,42,85,0.18), rgba(255,42,85,0) 70%);"></div>
    <div id="bg-p" style="position:absolute;inset:0;background:radial-gradient(70% 50% at 50% 60%, rgba(150,160,255,0.45), rgba(0,0,0,0) 70%);opacity:0;"></div>
    <div id="bg-floor" style="position:absolute;left:-300px;right:-300px;top:1480px;height:700px;background-image:linear-gradient(rgba(88,101,242,0.55) 3px, transparent 3px),linear-gradient(90deg, rgba(88,101,242,0.55) 3px, transparent 3px);background-size:90px 90px;transform:perspective(600px) rotateX(72deg);transform-origin:50% 0;"></div>
    <div style="position:absolute;inset:0;background:repeating-linear-gradient(0deg, rgba(255,255,255,0.03) 0 2px, rgba(0,0,0,0) 2px 6px);"></div>""",
               f'    tl.fromTo("#bg-g1", {{ x: 0 }}, {{ x: 500, duration: {TOTAL}, ease: "sine.inOut" }}, 0);\n'
               f'    tl.fromTo("#bg-g2", {{ x: 0 }}, {{ x: -600, duration: {TOTAL}, ease: "sine.inOut" }}, 0);\n'
               f'    tl.fromTo("#bg-floor", {{ backgroundPositionY: "0px" }}, {{ backgroundPositionY: "1800px", duration: {TOTAL}, ease: "none" }}, 0);\n' + pulses)
# white flash: 1 frame full, ~120 ms decay, on strong kicks and on every scene change
FLASH_T = sorted(set([round(t, 2) for t in STRONG] + [round(max(0, s - 0.03), 2) for _, s, _ in SCENES[1:]]))
C["flash"] = comp("flash", '    <div id="fl" style="position:absolute;inset:0;background:#fff;opacity:0;"></div>',
                  "".join(f'    tl.fromTo("#fl", {{ opacity: 0.9 }}, {{ opacity: 0, duration: 0.12, ease: "power2.out", immediateRender: false }}, {t:.2f});\n' for t in FLASH_T))
# letterbox bars that snap in on some beats (cinematic punctuation), grain is added in post
C["bars"] = comp("bars", '    <div class="bars" id="bt" style="top:-170px;"></div><div class="bars" id="bb" style="bottom:-170px;"></div>',
                 "".join(f'    tl.set("#bt", {{ y: {170 if n % 2 == 0 else 0} }}, {t:.3f});\n    tl.set("#bb", {{ y: {-170 if n % 2 == 0 else 0} }}, {t:.3f});\n'
                         for n, t in enumerate([b for b in BEATS[8::4]])))

# 1 hook: on screen at 0 s; three asks, shots cycle wide/face/low/dutch
i, k = 0, "s1"; d = d_of(i)
h, j, cc = character("c1", d, [[0, "idle"], [0.8, "shock"], [2.0, "think"]], shot_plan(i, ["wide", "face", "low", "dutch"]))
gh, gj = ghost(k, "DISCORD")
asks = [("DISCORD BOT?", "#9aa3ff", None), ("WEBSITE?", WHITE, 0.42), ("MINECRAFT PLUGIN?", GOLD, 0.66)]
txt = '<div class="c slam" style="top:220px;font-size:110px;">NEED A</div>' + "".join(
    f'<div class="c slam" id="s1-a{n}" style="top:{350 + n * 140}px;font-size:{130 if n < 2 else 104}px;color:{c};">{t}</div>' for n, (t, c, _) in enumerate(asks))
js = j + gj + "".join(slam(f"#s1-a{n}", rel(i, f)) + shake("#s1-w", rel(i, f)) for n, (_, _, f) in enumerate(asks) if f)
HITS += [W[k][0] + rel(i, f) for _, _, f in asks if f]
C[k] = scene(k, i, gh, h, txt, js, cc)

# 2 logo + name: hero low angle, the real logo spins in like a coin
i, k = 1, "s2"; d = d_of(i)
h, j, cc = character("c2", d, [[0, "idle"], [0.3, "point"]], shot_plan(i, ["hero", "low", "face", "wide"]))
txt = ('<div id="s2-logo" style="position:absolute;left:340px;top:200px;width:400px;height:400px;border-radius:50%;overflow:hidden;box-shadow:0 0 110px rgba(247,220,148,0.7);">'
       '<img src="assets/img/logo_circle.png" style="width:400px;height:400px;" alt="Heaven Developer logo"></div>'
       '<div class="c slam" id="s2-n" style="top:640px;font-size:136px;color:#f7dc94;">HEAVEN DEVELOPER</div>'
       '<div class="c sub" id="s2-s" style="top:790px;font-size:62px;">BUILDS IT ALL</div>')
js = (j + '    tl.fromTo("#s2-logo", { rotationY: -540, scale: 0.3, opacity: 0 }, { rotationY: 0, scale: 1, opacity: 1, duration: 0.7, ease: "expo.out" }, 0.02);\n'
      + slam("#s2-n", rel(i, 0.05)) + shake("#s2-w", rel(i, 0.05)) + slam("#s2-s", rel(i, 0.6), "y: 60, opacity: 0"))
HITS.append(W[k][0] + rel(i, 0.05))
C[k] = scene(k, i, "", h, txt, js, cc)

# 3 services: one word per beat, the word flips in (rotationX), giant ghost of the same word behind
i, k = 2, "s3"; d = d_of(i)
h, j, cc = character("c3", d, [[0, "talk"]], shot_plan(i, ["side", "face", "dutch", "low", "back"]))
SV = ["BOTS", "WEBSITES", "PLUGINS", "MODS", "TEXTURE PACKS"]
cols = [WHITE, "#9aa3ff", GOLD, "#7fe05a", WHITE]
txt = "".join(f'<div class="c slam" id="s3-v{n}" style="top:360px;font-size:{220 if n < 4 else 150}px;opacity:0;color:{cols[n]};">{t}</div>' for n, t in enumerate(SV))
js = j
times = [rel(i, 0.04 + n * 0.19) for n in range(len(SV))]
for n, a in enumerate(times):
    js += slam(f"#s3-v{n}", a, "rotationX: -90, scale: 1.6, opacity: 0", 0.16) + shake("#s3-w", a)
    if n + 1 < len(SV):
        js += f'    tl.to("#s3-v{n}", {{ opacity: 0, duration: 0.06 }}, {times[n + 1] - 0.06:.2f});\n'
    HITS.append(W[k][0] + a)
C[k] = scene(k, i, "", h, txt, js, cc)

# 4 price: speed-ramped jump on the reveal, giant $4 behind
i, k = 3, "s4"; d = d_of(i)
h, j, cc = character("c4", d, [[0, "idle"], [rel(i, 0.6), "shock"]], shot_plan(i, ["low", "wide", "hero", "dutch"]))
j += (f'    tl.to("#c4-move", {{ y: -360, duration: 0.28, ease: "expo.out" }}, {rel(i, 0.58):.2f});\n'
      f'    tl.to("#c4-move", {{ y: 0, duration: 0.42, ease: "bounce.out" }}, {rel(i, 0.58) + 0.28:.2f});\n')
txt = ('<div class="c sub" id="s4-a" style="top:260px;font-size:74px;">STARTING FROM</div>'
       '<div class="c slam" id="s4-p" style="top:350px;font-size:540px;color:#ffd76a;">$4</div>')
js = j + slam("#s4-a", 0.08, "y: -60, opacity: 0") + slam("#s4-p", rel(i, 0.62), "scale: 4.5, opacity: 0") + shake("#s4-w", rel(i, 0.62))
HITS.append(W[k][0] + rel(i, 0.62)); BIG.append(W[k][0] + rel(i, 0.62))
CASH = W[k][0] + rel(i, 0.62)
C[k] = scene(k, i, "", h, txt, js, cc)

# 5 invite: three clones step in for "3 friends"
i, k = 4, "s5"; d = d_of(i)
hm, jm, cm = character("c5", d, [[0, "wave"]], shot_plan(i, ["wide", "low", "wide", "top"]))
clones = ""
cj = ""
cc = cm
for n, (cx, cy) in enumerate([(220, 1560), (860, 1560), (540, 1450)]):
    hh, jj, c2 = character(f"c5f{n}", d, [[0, "idle"], [0.6, "wave"]], [(0.0, "wide")], x=cx, y=cy)
    clones += f'<div id="s5-f{n}" style="position:absolute;inset:0;opacity:0;transform:scale(0.78);transform-origin:{cx}px {cy}px;">{hh}</div>'
    cj += jj + f'    tl.fromTo("#s5-f{n}", {{ opacity: 0, y: -500 }}, {{ opacity: 0.9, y: 0, duration: 0.3, ease: "bounce.out" }}, {rel(i, 0.12 + n * 0.14):.2f});\n'
    cc += c2
txt = ('<div class="c slam" id="s5-a" style="top:250px;font-size:150px;">INVITE <span style="color:#ffd76a;">3</span> FRIENDS</div>'
       '<div class="c slam" id="s5-c" style="top:430px;font-size:126px;color:#7fe05a;">= FREE PROJECT</div>')
js = jm + cj + slam("#s5-a", 0.08) + slam("#s5-c", rel(i, 0.62)) + shake("#s5-w", rel(i, 0.62))
HITS += [W[k][0] + 0.08, W[k][0] + rel(i, 0.62)]
C[k] = scene(k, i, "", clones + hm, txt, js, cc)

# 6 three steps over the real orders banner
i, k = 5, "s6"; d = d_of(i)
h, j, cc = character("c6", d, [[0, "walk"]], shot_plan(i, ["side", "wide", "low", "face"]))
ST = ["OPEN A TICKET", "SHARE YOUR IDEA", "WE DELIVER"]
txt = ('<div id="s6-ban" style="position:absolute;left:90px;top:900px;width:900px;height:342px;border-radius:24px;overflow:hidden;opacity:0.55;box-shadow:0 0 60px rgba(255,120,40,0.5);">'
       '<img src="assets/img/orders.jpg" style="width:900px;height:342px;" alt="Heaven orders banner"></div>'
       + "".join(f'<div class="c slam" id="s6-k{n}" style="top:{250 + n * 180}px;font-size:{124 if n < 2 else 150}px;color:{[WHITE, "#9aa3ff", "#ffd76a"][n]};">{t}</div>' for n, t in enumerate(ST)))
js = j + '    tl.fromTo("#s6-ban", { scale: 1.2 }, { scale: 1, duration: 3, ease: "none" }, 0);\n'
for n in range(3):
    a = rel(i, 0.02 + n * 0.33)
    js += slam(f"#s6-k{n}", a, "x: -800, opacity: 0") + shake("#s6-w", a)
    HITS.append(W[k][0] + a)
C[k] = scene(k, i, txt.split("</div>", 1)[0] + "</div>", h, "".join(txt.split("</div>", 1)[1:]), js, cc)

# 7 music-only bar: the crowd (members), cut on every beat
i, k = 6, "s7"; d = d_of(i)
crowd, cj, cc = "", "", ""
grid = [(x, y) for y in (1180, 1720) for x in (150, 410, 670, 930)]
for n, (cx, cy) in enumerate(grid):
    hh, jj, c2 = character(f"c7m{n}", d, [[0, ["idle", "wave", "nod"][n % 3]]], [(0.0, ["wide", "dutch", "low"][n % 3])], x=cx, y=cy)
    crowd += f'<div id="s7-m{n}" style="position:absolute;inset:0;transform:scale(0.5);transform-origin:{cx}px {cy}px;opacity:0;">{hh}</div>'
    cj += jj + f'    tl.fromTo("#s7-m{n}", {{ opacity: 0, y: 120 }}, {{ opacity: 1, y: 0, duration: 0.2, ease: "power3.out" }}, {0.05 + n * 0.08:.2f});\n'
    cc += c2
bt = inside(i, BEATS)[:3] or [0.1, 0.9, 1.7]
txt = ('<div class="c slam" id="s7-a" style="top:250px;font-size:200px;color:#f7dc94;">2,500+</div>'
       '<div class="c slam" id="s7-b" style="top:460px;font-size:120px;">MEMBERS</div>'
       '<div class="c slam" id="s7-c" style="top:590px;font-size:96px;color:#9aa3ff;">17 BOOSTS • LEVEL 3</div>')
js = cj + "".join(slam(f"#s7-{c}", t) + shake("#s7-w", t) for c, t in zip("abc", bt))
HITS += [W[k][0] + t for t in bt]
C[k] = scene(k, i, "", crowd, txt, js, cc)

# 8 end card
i, k = 7, "s8"; d = d_of(i)
h, j, cc = character("c8", d, [[0, "wave"], [2.4, "spin"], [3.6, "wave"]], shot_plan(i, ["wide", "low", "wide", "hero", "wide", "dutch", "wide", "low", "wide", "wide"]), y=1720)
txt = ('<div id="s8-logo" style="position:absolute;left:390px;top:180px;width:300px;height:300px;border-radius:50%;overflow:hidden;box-shadow:0 0 90px rgba(247,220,148,0.6);">'
       '<img src="assets/img/logo_circle.png" style="width:300px;height:300px;" alt="Heaven Developer logo"></div>'
       '<div class="c slam" id="s8-n" style="top:520px;font-size:120px;color:#f7dc94;">HEAVEN DEVELOPER</div>'
       f'<div class="c" id="s8-b" style="top:700px;"><span class="btn"><svg viewBox="0 0 24 24" style="width:80px;height:80px;" fill="#fff">{DISCORD}</svg>JOIN ON DISCORD</span></div>'
       '<div class="c sub" id="s8-u" style="top:880px;font-size:58px;color:#fff;">discord.gg/<span style="color:#f7dc94;">heavendeveloper</span></div>')
js = (j + '    tl.fromTo("#s8-logo", { rotationY: -540, scale: 0.2, opacity: 0 }, { rotationY: 0, scale: 1, opacity: 1, duration: 0.7, ease: "expo.out" }, 0.05);\n'
      + slam("#s8-n", 0.15) + slam("#s8-b", rel(i, 0.55)) + shake("#s8-w", rel(i, 0.55))
      + f'    tl.to("#s8-b", {{ scale: 1.07, duration: 0.4, ease: "sine.inOut", yoyo: true, repeat: 8 }}, {rel(i, 0.55) + 0.3:.2f});\n'
      + slam("#s8-u", rel(i, 0.75), "y: 60, opacity: 0"))
HITS.append(W[k][0] + rel(i, 0.55))
JOIN = W[k][0] + rel(i, 0.55)
C[k] = scene(k, i, "", h, txt, js, cc, exit_=False)

os.makedirs("compositions", exist_ok=True)
for f in os.listdir("compositions"):
    os.remove(os.path.join("compositions", f))
for kk, v in C.items():
    open(f"compositions/{kk}.html", "w").write(v)
div = lambda kk, s, d_, lane, z: (f'      <div id="{kk}" data-composition-id="{kk}" data-composition-src="compositions/{kk}.html" data-start="{s}" data-duration="{d_}" '
                                  f'data-track-index="{lane}" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: {z}"></div>')
divs = [div("bg", 0, TOTAL, 0, 0)] + [div(kk, s, round(e - s, 3), 1, 1) for kk, s, e in SCENES] + [div("bars", 0, TOTAL, 2, 2), div("flash", 0, TOTAL, 3, 3)]
sfx = lambda n: f"assets/sfx/{n}.mp3"
A = [("mix", "assets/audio/mix.wav", 0, min(dur("assets/audio/mix.wav"), TOTAL), 1.0, 10)]
HIT_SFX = ["impact-boom", "punch-heavy", "sub-drop"]
for n, t in enumerate(sorted(HITS)):
    f = HIT_SFX[n % len(HIT_SFX)]
    A.append((f"hit{n}", sfx(f), round(t, 2), dur(sfx(f)), 0.3, 20 + n % 6))
for n, (kk, s, e) in enumerate(SCENES[1:]):
    f = ["whoosh-fast-0.3s", "swish-4"][n % 2]
    A.append((f"wh{n}", sfx(f), round(max(0, s - 0.12), 2), dur(sfx(f)), 0.5, 14 + n % 2))
A += [("cash", sfx("cash-register"), round(CASH, 2), dur(sfx("cash-register")), 0.35, 16),
      ("ok", sfx("confirm-1"), round(JOIN, 2), dur(sfx("confirm-1")), 0.4, 17)]
aud = "\n".join(f'      <audio id="{a}" src="{s}" data-start="{b}" data-duration="{dd}" data-volume="{v}" data-track-index="{ln}"></audio>'
                for a, s, b, dd, v, ln in A)
open("index.html", "w").write(f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap-3.14.2.min.js"></script>
    <style>* {{ margin: 0; padding: 0; box-sizing: border-box; }} html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: {BG}; }}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
{chr(10).join(divs)}
{aud}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
""")
# post: snares -> RGB split (~2.5 px at 1080p scale: 5 px), cold high-contrast desaturated grade, grain (Onset Engine formula)
SN = [round(t, 2) for t, s in EV["snares"] if s >= 0.6 and t < TOTAL]
en = "+".join(f"between(t,{t:.2f},{t + 0.09:.2f})" for t in SN) or "0"
open("post.sh", "w").write(
    "#!/bin/bash\n# post-process the HyperFrames render: snare RGB split, grade, grain; then loudness\n"
    f'ffmpeg -v error -y -i "$1" -vf "rgbashift=rh=-6:bh=6:enable=\'{en}\',eq=contrast=1.22:saturation=0.85:gamma=0.97,'
    'colorbalance=bs=0.10:bm=0.03:rh=-0.03,noise=alls=9:allf=t+u,vignette=PI/5" -c:v libx264 -crf 16 -preset medium '
    '-af "volume=2.2dB,alimiter=limit=0.79:level=false" -c:a aac -b:a 192k "$2"\n')
print("built", TOTAL, len(SCENES), "scenes,", len(BEATS), "beat cuts,", len(KICKS), "kick punches,", len(FLASH_T), "flashes,", len(SN), "snare splits")
