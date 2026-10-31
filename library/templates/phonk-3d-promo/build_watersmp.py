# WaterSMP 9:16 promo (portal order #5, 2026-10-31): phonk-3d-promo "formula v2" (build_heavendeveloper_phonk_v2.py)
# re-skinned for a Minecraft SMP with a water brand. Same rules as v2 (library/research/phonk-edit-formula.md): a cut on
# every beat (new camera preset of the 3D blocky character), kick punches, white flash on strong kicks and scene
# changes, giant ghost words behind the character, snare RGB split + grade + grain in post.sh.
# What is new here:
#  - brand colours = the server's own MOTD gradient (#17C8F5 -> #08A2FB) + MOTD gold #FFAA00 (brief.md);
#  - the real server icon (64 px, nearest-neighbour x8 = crisp pixel art) spins in like a coin; splash SFX on the name;
#  - ocean background: deep-blue glows, cyan grid floor, rising bubbles (CSS), beat pulses;
#  - an English caption line for every VO line (client asked for English captions; VO is Hindi), dark pill at y~1400;
#  - hard names (WATERSMP, play.watersmp.in, 25590, 3RD NOVEMBER) always on screen because the voice can garble them.
# Character = the owner's default host skin (CLAUDE.md DEFAULT HOST). Facts: library/clients/watersmp/brief.md.
# Run inside the HyperFrames project (assets/ as in README.md): python3 build_watersmp.py
import html as H
import importlib.util, json, os, subprocess

spec = importlib.util.spec_from_file_location("bc", "/home/user/new-startup/library/tools/blocky_character.py")
bc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bc)

VO_START = float(os.environ.get("VO_START", 0.3))
BG, CYAN, BLUE, GOLD, WHITE, RED = "#020c1c", "#17c8f5", "#08a2fb", "#ffaa00", "#ffffff", "#ff3b5c"
L = json.load(open("assets/vo/lines.json"))
EV = json.load(open("assets/music/events.json"))
TOTAL = float(os.environ.get("TOTAL", 30.0))
IP, PORT = H.escape("play.watersmp.in"), H.escape("25590")
BEATS = [b for b in EV["beats"] if b < TOTAL]
KICKS, last = [], -9
for t, s in EV["kicks"]:
    if s >= 0.38 and t - last >= 0.35:
        KICKS.append(t); last = t
STRONG = [t for t, s in EV["strong_kicks"] if t < TOTAL - 0.3]
st = [round(VO_START + a - 0.1, 2) for a, _ in L]
st[0] = 0.0
SCENES = [(f"s{i + 1}", st[i], st[i + 1] if i + 1 < len(st) else TOTAL) for i in range(len(st))]
W = {k: (s, e) for k, s, e in SCENES}
SKIN = "assets/characters/host-skin.png"
SC = 18  # px per skin pixel: character 576 px tall
CY = 1600  # feet y


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
    @font-face {{ font-family: "OU"; src: url("assets/fonts/Poppins-ExtraBold.ttf"); font-weight: 800; }}
    #root {{ position: absolute; inset: 0; overflow: hidden; }}
    .c {{ position: absolute; left: 0; right: 0; text-align: center; }}
    .slam {{ font-family: AN; line-height: 0.92; color: {WHITE}; text-transform: uppercase;
             text-shadow: -5px 0 0 rgba(255,59,92,0.75), 5px 0 0 rgba(23,200,245,0.85), 0 12px 44px rgba(0,0,0,0.85); }}
    .water {{ background: linear-gradient(180deg, #8ff0ff 0%, {CYAN} 45%, {BLUE} 100%); -webkit-background-clip: text; background-clip: text;
              color: transparent; text-shadow: none; filter: drop-shadow(0 0 26px rgba(23,200,245,0.75)) drop-shadow(0 10px 0 #033d6b); }}
    .ghost {{ font-family: AN; line-height: 0.85; color: rgba(23,200,245,0.12); -webkit-text-stroke: 4px rgba(143,240,255,0.22); text-transform: uppercase; white-space: nowrap; }}
    .sub {{ font-family: OU; font-weight: 800; color: {GOLD}; letter-spacing: 3px; text-shadow: 0 6px 24px rgba(0,0,0,0.9); }}
    .card {{ display: inline-block; font-family: OU; font-weight: 800; background: rgba(2,18,40,0.82); border: 4px solid {CYAN};
             border-radius: 26px; padding: 18px 40px; box-shadow: 0 0 40px rgba(23,200,245,0.45); }}
    .btn {{ display: inline-block; background: linear-gradient(90deg, {CYAN}, {BLUE}); color: #fff; font-family: AN;
            border-radius: 22px; padding: 22px 64px; font-size: 92px; box-shadow: 0 18px 60px rgba(8,162,251,0.6); letter-spacing: 3px; }}
    .bars {{ position: absolute; left: 0; right: 0; height: 150px; background: #000; }}
    .cap {{ display: inline-block; font-family: OU; font-weight: 800; font-size: 50px; line-height: 1.18; color: #fff;
            background: rgba(0,0,0,0.62); border-radius: 18px; padding: 12px 28px; max-width: 960px; }}
    .cap b {{ color: {CYAN}; }}
"""

SHOT = {
    "wide":  dict(s=1.0, x=0, y=0, yaw=-22, pitch=-6, roll=0),
    "face":  dict(s=2.1, x=0, y=760, yaw=-12, pitch=-2, roll=0),
    "low":   dict(s=1.4, x=0, y=150, yaw=28, pitch=16, roll=0),
    "dutch": dict(s=1.2, x=40, y=100, yaw=-45, pitch=-4, roll=-11),
    "side":  dict(s=1.25, x=-60, y=100, yaw=85, pitch=-4, roll=0),
    "back":  dict(s=1.1, x=0, y=50, yaw=165, pitch=-8, roll=0),
    "top":   dict(s=1.05, x=0, y=-60, yaw=-30, pitch=-30, roll=5),
    "hero":  dict(s=1.6, x=0, y=360, yaw=10, pitch=10, roll=0),
}


def character(P, d, moves, shots, x=540, y=CY):
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
               f'    tl.set("#{P}-yaw", {{ rotationY: {p["yaw"]} }}, {t:.3f});\n'
               f'    tl.fromTo("#{P}-move", {{ scale: 1.0 }}, {{ scale: 1.05, duration: 0.7, ease: "expo.out", immediateRender: false }}, {t:.3f});\n')
    return html, js, bc.css(P, SKIN)


def shot_plan(i, cycle):
    times = [0.0] + [max(0.0, b - 0.033) for b in inside(i, BEATS)]
    return [(t, cycle[n % len(cycle)]) for n, t in enumerate(times)]


def slam(sel, at, frm="scale: 2.6, opacity: 0", d=0.2):
    return f'    tl.fromTo("{sel}", {{ {frm} }}, {{ scale: 1, x: 0, y: 0, rotationX: 0, rotation: 0, opacity: 1, duration: {d}, ease: "power4.out" }}, {at:.2f});\n'


def shake(sel, at):
    # even repeat count: a yoyo shake ends at rest (CLAUDE.md HyperFrames learnings)
    return f'    tl.fromTo("{sel}", {{ x: -12, y: 7 }}, {{ x: 0, y: 0, duration: 0.045, ease: "none", repeat: 4, yoyo: true, immediateRender: false }}, {at:.2f});\n'


def punches(i, k):
    return "".join(f'    tl.fromTo("#{k}-w", {{ scale: 1.06 }}, {{ scale: 1, duration: 0.24, ease: "expo.out", immediateRender: false }}, {t:.3f});\n'
                   for t in inside(i, KICKS))


def ghost(k, i, word, top=760, size=420):
    return (f'<div class="c ghost" id="{k}-gh" style="top:{top}px;font-size:{size}px;">{word}</div>',
            f'    tl.fromTo("#{k}-gh", {{ x: 160 }}, {{ x: -160, duration: {d_of(i)}, ease: "none" }}, 0);\n')


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


C, HITS = {}, []
SPLASH, SWORD, COIN, JOIN = [], [], [], []

# background: deep ocean, moving glows, cyan grid floor, rising bubbles, beat pulses
pulses = "".join(f'    tl.fromTo("#bg-p", {{ opacity: 0.45 }}, {{ opacity: 0, duration: 0.3, ease: "power2.out", immediateRender: false }}, {b:.3f});\n' for b in BEATS)
bub_html, bub_js = "", ""
for n in range(22):
    x = (n * 467) % 1040 + 20
    sz = 10 + (n * 7) % 34
    t0 = (n * 1.37) % 6.0
    rise = 9 + (n % 5) * 1.6
    bub_html += (f'<div id="bub{n}" style="position:absolute;left:{x}px;top:1960px;width:{sz}px;height:{sz}px;border-radius:50%;'
                 f'border:3px solid rgba(143,240,255,0.55);background:radial-gradient(circle at 30% 30%, rgba(255,255,255,0.5), rgba(23,200,245,0.08) 60%);"></div>')
    k_ = 0
    t = t0
    while t < TOTAL:
        bub_js += f'    tl.fromTo("#bub{n}", {{ y: 0, x: 0 }}, {{ y: -2100, x: {(-1) ** n * 60}, duration: {rise:.2f}, ease: "none", immediateRender: false }}, {t:.2f});\n'
        t += rise
        k_ += 1
C["bg"] = comp("bg", f"""    <div style="position:absolute;inset:0;background:linear-gradient(180deg, #03203f 0%, {BG} 60%, #010712 100%);"></div>
    <div id="bg-g1" style="position:absolute;left:-300px;top:150px;width:1200px;height:1200px;border-radius:50%;background:radial-gradient(circle, rgba(23,200,245,0.32), rgba(23,200,245,0) 70%);"></div>
    <div id="bg-g2" style="position:absolute;left:300px;top:900px;width:1100px;height:1100px;border-radius:50%;background:radial-gradient(circle, rgba(8,162,251,0.30), rgba(8,162,251,0) 70%);"></div>
    <div id="bg-p" style="position:absolute;inset:0;background:radial-gradient(70% 50% at 50% 60%, rgba(143,240,255,0.42), rgba(0,0,0,0) 70%);opacity:0;"></div>
    <div id="bg-floor" style="position:absolute;left:-300px;right:-300px;top:1480px;height:700px;background-image:linear-gradient(rgba(23,200,245,0.55) 3px, transparent 3px),linear-gradient(90deg, rgba(23,200,245,0.55) 3px, transparent 3px);background-size:90px 90px;transform:perspective(600px) rotateX(72deg);transform-origin:50% 0;"></div>
    {bub_html}
    <div style="position:absolute;inset:0;background:repeating-linear-gradient(0deg, rgba(255,255,255,0.03) 0 2px, rgba(0,0,0,0) 2px 6px);"></div>""",
               f'    tl.fromTo("#bg-g1", {{ x: 0 }}, {{ x: 500, duration: {TOTAL}, ease: "sine.inOut" }}, 0);\n'
               f'    tl.fromTo("#bg-g2", {{ x: 0 }}, {{ x: -600, duration: {TOTAL}, ease: "sine.inOut" }}, 0);\n'
               f'    tl.fromTo("#bg-floor", {{ backgroundPositionY: "0px" }}, {{ backgroundPositionY: "1800px", duration: {TOTAL}, ease: "none" }}, 0);\n'
               + bub_js + pulses)
FLASH_T = sorted(set([round(t, 2) for t in STRONG] + [round(max(0, s - 0.03), 2) for _, s, _ in SCENES[1:]]))
C["flash"] = comp("flash", '    <div id="fl" style="position:absolute;inset:0;background:#e9fbff;opacity:0;"></div>',
                  "".join(f'    tl.fromTo("#fl", {{ opacity: 0.85 }}, {{ opacity: 0, duration: 0.12, ease: "power2.out", immediateRender: false }}, {t:.2f});\n' for t in FLASH_T))
C["bars"] = comp("bars", '    <div class="bars" id="bt" style="top:-150px;"></div><div class="bars" id="bb" style="bottom:-150px;"></div>',
                 "".join(f'    tl.set("#bt", {{ y: {150 if n % 2 == 0 else 0} }}, {t:.3f});\n    tl.set("#bb", {{ y: {-150 if n % 2 == 0 else 0} }}, {t:.3f});\n'
                         for n, t in enumerate([b for b in BEATS[8::4] if b < W["s7"][0]]))
                 + f'    tl.set("#bt", {{ y: 0 }}, {W["s7"][0]:.3f});\n    tl.set("#bb", {{ y: 0 }}, {W["s7"][0]:.3f});\n')

# 1 hook (on screen at 0 s = thumbnail): best Java + Bedrock cracked SMP?
i, k = 0, "s1"; d = d_of(i)
h, j, cc = character("c1", d, [[0, "think"], [rel(i, 0.55), "shrug"]], shot_plan(i, ["wide", "face", "low", "dutch"]))
gh, gj = ghost(k, i, "SMP?")
txt = ('<div class="c sub" id="s1-t" style="top:230px;font-size:62px;color:#fff;">LOOKING FOR THE BEST</div>'
       '<div class="c slam" id="s1-a0" style="top:330px;font-size:170px;">JAVA <span style="color:#ffaa00;">+</span></div>'
       '<div class="c slam water" id="s1-a1" style="top:490px;font-size:170px;">BEDROCK</div>'
       '<div class="c slam" id="s1-a2" style="top:660px;font-size:130px;">CRACKED SMP?</div>')
js = j + gj + slam("#s1-t", 0.0, "scale: 1, opacity: 1", 0.01)
for n, f in enumerate([0.22, 0.38, 0.6]):
    js += slam(f"#s1-a{n}", rel(i, f)) + shake("#s1-w", rel(i, f))
    HITS.append(W[k][0] + rel(i, f))
js = js.replace(slam("#s1-a0", rel(i, 0.22)), '    gsap.set("#s1-a0", { opacity: 1 });\n')  # first word already on screen at 0 s
C[k] = scene(k, i, gh, h, txt, js, cc)

# 2 brand reveal: the real server icon spins in like a coin, WATERSMP in the MOTD gradient, splash on the name
i, k = 1, "s2"; d = d_of(i)
h, j, cc = character("c2", d, [[0, "idle"], [rel(i, 0.55), "point"]], shot_plan(i, ["hero", "low", "face", "wide"]))
gh, gj = ghost(k, i, "WATER")
txt = ('<div class="c sub" id="s2-q" style="top:210px;font-size:60px;color:#fff;">NO TENSION!</div>'
       '<div id="s2-logo" style="position:absolute;left:350px;top:300px;width:380px;height:380px;filter:drop-shadow(0 0 50px rgba(23,200,245,0.8));">'
       '<img src="assets/img/icon.png" style="width:380px;height:380px;image-rendering:pixelated;" alt="WaterSMP server icon"></div>'
       '<div class="c slam water" id="s2-n" style="top:700px;font-size:190px;">WATERSMP</div>')
at = rel(i, 0.72)
js = (j + gj + slam("#s2-q", 0.05, "y: -60, opacity: 0")
      + f'    tl.fromTo("#s2-logo", {{ rotationY: -540, scale: 0.3, opacity: 0 }}, {{ rotationY: 0, scale: 1, opacity: 1, duration: 0.7, ease: "expo.out" }}, {max(0.1, at - 0.7):.2f});\n'
      + slam("#s2-n", at, "scale: 3.2, opacity: 0") + shake("#s2-w", at))
HITS.append(W[k][0] + at); SPLASH.append(W[k][0] + at)
C[k] = scene(k, i, gh, h, txt, js, cc)

# 3 features: one per beat-ish, flipping in
i, k = 2, "s3"; d = d_of(i)
h, j, cc = character("c3", d, [[0, "talk"]], shot_plan(i, ["side", "face", "dutch", "low", "back"]))
FE = [("AMAZING PING", WHITE, 0.12), ("ACTIVE PLAYERS", CYAN, 0.38), ("EXCITING SURVIVAL", GOLD, 0.66)]
gh, gj = ghost(k, i, "SURVIVAL", size=360)
txt = "".join(f'<div class="c slam" id="s3-v{n}" style="top:{290 + n * 175}px;font-size:{150 if n < 2 else 124}px;color:{c};opacity:0;">{t}</div>'
              for n, (t, c, _) in enumerate(FE))
js = j + gj
for n, (_, _, f) in enumerate(FE):
    js += slam(f"#s3-v{n}", rel(i, f), "rotationX: -90, scale: 1.6, opacity: 0", 0.16) + shake("#s3-w", rel(i, f))
    HITS.append(W[k][0] + rel(i, f))
C[k] = scene(k, i, gh, h, txt, js, cc)

# 4 tournament: date card + EPIC PVP TOURNAMENT, the character jumps on "epic", sword slashes in
i, k = 3, "s4"; d = d_of(i)
a_date, a_epic = rel(i, 0.3), rel(i, 0.7)
h, j, cc = character("c4", d, [[0, "idle"], [a_epic - 0.1, "shock"]], shot_plan(i, ["low", "wide", "hero", "dutch"]))
j += (f'    tl.to("#c4-move", {{ y: -330, duration: 0.28, ease: "expo.out" }}, {a_epic:.2f});\n'
      f'    tl.to("#c4-move", {{ y: 0, duration: 0.42, ease: "bounce.out" }}, {a_epic + 0.28:.2f});\n')
gh, gj = ghost(k, i, "PVP", size=520, top=700)
txt = ('<div class="c" id="s4-d" style="top:200px;"><span class="card" style="font-size:72px;color:#fff;">'
       f'<span style="color:{GOLD};">3RD</span> NOVEMBER</span></div>'
       '<div class="c slam" id="s4-e" style="top:370px;font-size:210px;color:#ffaa00;">EPIC PVP</div>'
       '<div class="c slam water" id="s4-t" style="top:580px;font-size:150px;">TOURNAMENT</div>'
       '<img id="s4-sw" src="assets/img/sword.png" alt="sword" style="position:absolute;left:760px;top:840px;width:240px;height:240px;image-rendering:pixelated;opacity:0;">')
js = (j + gj + slam("#s4-d", a_date, "y: -80, opacity: 0") + shake("#s4-w", a_date)
      + slam("#s4-e", a_epic, "scale: 4.0, opacity: 0") + shake("#s4-w", a_epic)
      + slam("#s4-t", a_epic + 0.25, "y: 80, opacity: 0")
      + f'    tl.fromTo("#s4-sw", {{ x: 400, rotation: 200, opacity: 0 }}, {{ x: 0, rotation: 0, opacity: 1, duration: 0.3, ease: "back.out(1.6)" }}, {a_epic + 0.35:.2f});\n')
HITS += [W[k][0] + a_date, W[k][0] + a_epic]; SWORD.append(W[k][0] + a_epic + 0.35)
C[k] = scene(k, i, gh, h, txt, js, cc)

# 5 skills + rewards: two rivals step in with swords, "win amazing rewards" on the coin sound
i, k = 4, "s5"; d = d_of(i)
a_sk, a_rw = rel(i, 0.12), rel(i, 0.62)
hm, jm, cm = character("c5", d, [[0, "idle"], [0.3, "point"]], shot_plan(i, ["wide", "low", "wide", "dutch"]))
rivals, rj, cc = "", "", cm
for n, (cx, cy) in enumerate([(200, 1560), (880, 1560)]):
    hh, jj, c2 = character(f"c5r{n}", d, [[0, "idle"], [0.6, "point"]], [(0.0, "wide")], x=cx, y=cy)
    rivals += (f'<div id="s5-r{n}" style="position:absolute;inset:0;opacity:0;transform:scale(0.72);transform-origin:{cx}px {cy}px;">{hh}'
               f'<img src="assets/img/sword.png" alt="" style="position:absolute;left:{cx + (-150 if n == 0 else 30)}px;top:{cy - 470}px;width:120px;height:120px;'
               f'image-rendering:pixelated;transform:scaleX({-1 if n == 0 else 1});"></div>')
    rj += jj + f'    tl.fromTo("#s5-r{n}", {{ opacity: 0, y: -500 }}, {{ opacity: 0.92, y: 0, duration: 0.3, ease: "bounce.out" }}, {a_sk + 0.1 + n * 0.16:.2f});\n'
    cc += c2
txt = ('<div class="c slam" id="s5-a" style="top:250px;font-size:140px;">SHOW YOUR</div>'
       '<div class="c slam water" id="s5-b" style="top:390px;font-size:170px;">PVP SKILLS</div>'
       '<div class="c slam" id="s5-c" style="top:600px;font-size:104px;color:#ffaa00;">WIN AMAZING REWARDS</div>')
js = (jm + rj + slam("#s5-a", a_sk) + slam("#s5-b", a_sk + 0.2) + shake("#s5-w", a_sk + 0.2)
      + slam("#s5-c", a_rw, "scale: 3, opacity: 0") + shake("#s5-w", a_rw))
HITS += [W[k][0] + a_sk + 0.2, W[k][0] + a_rw]; COIN.append(W[k][0] + a_rw); SWORD.append(W[k][0] + a_sk + 0.1)
C[k] = scene(k, i, "", rivals + hm, txt, js, cc)

# 6 join today + community: a crowd of players pops in
i, k = 5, "s6"; d = d_of(i)
crowd, cj, cc = "", "", ""
grid = [(x, y) for y in (1250, 1700) for x in (150, 410, 670, 930)]
for n, (cx, cy) in enumerate(grid):
    hh, jj, c2 = character(f"c6m{n}", d, [[0, ["idle", "wave", "nod"][n % 3]]], [(0.0, ["wide", "dutch", "low"][n % 3])], x=cx, y=cy)
    crowd += f'<div id="s6-m{n}" style="position:absolute;inset:0;transform:scale(0.5);transform-origin:{cx}px {cy}px;opacity:0;">{hh}</div>'
    cj += jj + f'    tl.fromTo("#s6-m{n}", {{ opacity: 0, y: 120 }}, {{ opacity: 1, y: 0, duration: 0.2, ease: "power3.out" }}, {rel(i, 0.55) + n * 0.07:.2f});\n'
    cc += c2
a_j, a_c = rel(i, 0.3), rel(i, 0.62)
txt = ('<div class="c slam" id="s6-a" style="top:240px;font-size:200px;">JOIN</div>'
       '<div class="c slam water" id="s6-b" style="top:440px;font-size:170px;">TODAY</div>'
       '<div class="c slam" id="s6-c" style="top:640px;font-size:84px;color:#ffaa00;">BE PART OF THE COMMUNITY</div>')
js = cj + slam("#s6-a", a_j) + shake("#s6-w", a_j) + slam("#s6-b", a_j + 0.18) + slam("#s6-c", a_c) + shake("#s6-w", a_c)
HITS += [W[k][0] + a_j, W[k][0] + a_c]
C[k] = scene(k, i, "", crowd, txt, js, cc)

# 7 end card: icon, name, IP + port cards, JOIN NOW button, "see you on WaterSMP"
i, k = 6, "s7"; d = d_of(i)
h, j, cc = character("c7", d, [[0, "wave"], [2.6, "spin"], [3.8, "wave"]],
                     shot_plan(i, ["wide", "low", "wide", "hero", "wide", "dutch", "wide", "low", "wide", "wide"]), y=1720)
txt = ('<div id="s7-logo" style="position:absolute;left:400px;top:150px;width:280px;height:280px;filter:drop-shadow(0 0 40px rgba(23,200,245,0.8));">'
       '<img src="assets/img/icon.png" style="width:280px;height:280px;image-rendering:pixelated;" alt="WaterSMP server icon"></div>'
       '<div class="c slam water" id="s7-n" style="top:450px;font-size:150px;">WATERSMP</div>'
       f'<div class="c" id="s7-ip" style="top:640px;"><span class="card" style="font-size:66px;color:#fff;"><span style="color:{GOLD};">IP</span> {IP}</span></div>'
       f'<div class="c" id="s7-pt" style="top:775px;"><span class="card" style="font-size:66px;color:#fff;"><span style="color:{GOLD};">PORT</span> {PORT}</span></div>'
       '<div class="c sub" id="s7-jb" style="top:905px;font-size:44px;color:#8ff0ff;">JAVA + BEDROCK</div>'
       '<div class="c" id="s7-b" style="top:975px;"><span class="btn">JOIN NOW</span></div>')
a_b = rel(i, 0.4)
js = (j + '    tl.fromTo("#s7-logo", { rotationY: -540, scale: 0.2, opacity: 0 }, { rotationY: 0, scale: 1, opacity: 1, duration: 0.7, ease: "expo.out" }, 0.05);\n'
      + slam("#s7-n", 0.15) + slam("#s7-ip", 0.4, "x: -700, opacity: 0") + slam("#s7-pt", 0.55, "x: 700, opacity: 0")
      + slam("#s7-jb", 0.7, "y: 40, opacity: 0") + slam("#s7-b", a_b) + shake("#s7-w", a_b)
      + f'    tl.to("#s7-b", {{ scale: 1.07, duration: 0.4, ease: "sine.inOut", yoyo: true, repeat: 8 }}, {a_b + 0.3:.2f});\n')
HITS.append(W[k][0] + a_b); JOIN.append(W[k][0] + a_b)
C[k] = scene(k, i, "", h, txt, js, cc, exit_=False)

# English captions (one composition on top; each VO line split into its chunks at fractions of the line)
CAPS = [
    [(0.0, "Looking for the best <b>Java + Bedrock</b>"), (0.5, "<b>cracked SMP</b> server?")],
    [(0.0, "No tension!"), (0.4, "I've brought you <b>WaterSMP!</b>")],
    [(0.0, "Here you get <b>amazing ping</b>,"), (0.45, "<b>active players</b> and an exciting <b>survival</b> experience!")],
    [(0.0, "And the best part:"), (0.3, "on <b>3rd November</b>, an <b>EPIC PvP Tournament!</b>")],
    [(0.0, "Show your <b>PvP skills</b>"), (0.55, "and win <b>amazing rewards!</b>")],
    [(0.0, "So why wait? <b>Join WaterSMP</b> today"), (0.55, "and be part of our <b>community!</b>")],
    [(0.0, "See you on <b>WaterSMP!</b>")],
]
cap_html, cap_js = "", ""
for li, chunks in enumerate(CAPS):
    a, b = L[li]
    for n, (f, text) in enumerate(chunks):
        t0 = round(VO_START + a + f * (b - a), 2)
        t1 = round(VO_START + a + chunks[n + 1][0] * (b - a), 2) if n + 1 < len(chunks) else round(VO_START + b + 0.25, 2)
        if li + 1 < len(L) and n + 1 == len(chunks):
            t1 = min(t1, round(VO_START + L[li + 1][0] - 0.02, 2))
        cid = f"cp{li}_{n}"
        cap_html += f'<div class="c" id="{cid}" style="top:1360px;visibility:hidden;"><span class="cap">{text}</span></div>'
        cap_js += (f'    tl.set("#{cid}", {{ visibility: "visible" }}, {t0:.2f});\n'
                   f'    tl.fromTo("#{cid}", {{ y: 24, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.14, ease: "power2.out", immediateRender: false }}, {t0:.2f});\n'
                   f'    tl.set("#{cid}", {{ visibility: "hidden" }}, {t1:.2f});\n')
C["caps"] = comp("caps", cap_html, cap_js)

os.makedirs("compositions", exist_ok=True)
for f in os.listdir("compositions"):
    os.remove(os.path.join("compositions", f))
for kk, v in C.items():
    open(f"compositions/{kk}.html", "w").write(v)
div = lambda kk, s, d_, lane, z: (f'      <div id="{kk}" data-composition-id="{kk}" data-composition-src="compositions/{kk}.html" data-start="{s}" data-duration="{d_}" '
                                  f'data-track-index="{lane}" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: {z}"></div>')
divs = ([div("bg", 0, TOTAL, 0, 0)] + [div(kk, s, round(e - s, 3), 1, 1) for kk, s, e in SCENES]
        + [div("bars", 0, TOTAL, 2, 2), div("caps", 0, TOTAL, 3, 3), div("flash", 0, TOTAL, 4, 4)])
sfx = lambda n: f"assets/sfx/{n}.mp3"
A = [("mix", "assets/audio/mix.wav", 0, min(dur("assets/audio/mix.wav"), TOTAL), 1.0, 10)]
HIT_SFX = ["impact-boom", "punch-heavy", "sub-drop"]
for n, t in enumerate(sorted(HITS)):
    f = HIT_SFX[n % len(HIT_SFX)]
    A.append((f"hit{n}", sfx(f), round(t, 2), dur(sfx(f)), 0.3, 20 + n % 6))
for n, (kk, s, e) in enumerate(SCENES[1:]):
    f = ["whoosh-fast-0.3s", "swish-4"][n % 2]
    A.append((f"wh{n}", sfx(f), round(max(0, s - 0.12), 2), dur(sfx(f)), 0.5, 14 + n % 2))
for n, t in enumerate(SPLASH):
    A.append((f"spl{n}", sfx("splash"), round(t, 2), dur(sfx("splash")), 0.45, 16))
for n, t in enumerate(SWORD):
    A.append((f"swd{n}", sfx("sword-draw"), round(t, 2), dur(sfx("sword-draw")), 0.45, 17 + n % 2))
for n, t in enumerate(COIN):
    A.append((f"coin{n}", sfx("game-coin"), round(t, 2), dur(sfx("game-coin")), 0.35, 19))
for n, t in enumerate(JOIN):
    A.append((f"ok{n}", sfx("game-levelup"), round(t, 2), dur(sfx("game-levelup")), 0.35, 26))
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
SN = [round(t, 2) for t, s in EV["snares"] if s >= 0.6 and t < TOTAL]
en = "+".join(f"between(t,{t:.2f},{t + 0.09:.2f})" for t in SN) or "0"
open("post.sh", "w").write(
    "#!/bin/bash\n# post-process the HyperFrames render: snare RGB split, cool grade (keeps the brand cyan), grain; then loudness\n"
    f'ffmpeg -v error -y -i "$1" -vf "rgbashift=rh=-6:bh=6:enable=\'{en}\',eq=contrast=1.15:saturation=1.0:gamma=0.98,'
    'colorbalance=bs=0.06:bm=0.02,noise=alls=7:allf=t+u,vignette=PI/5,format=yuv420p" -c:v libx264 -crf 16 -preset medium '
    '-af "volume=${GAIN:-2.0}dB,alimiter=limit=0.79:level=false" -c:a aac -b:a 192k "$2"\n')
print("built", TOTAL, len(SCENES), "scenes,", len(BEATS), "beat cuts,", len(KICKS), "kick punches,", len(FLASH_T), "flashes,", len(SN), "snare splits")
