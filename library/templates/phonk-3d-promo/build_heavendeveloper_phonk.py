# Heaven Developer 30 s PHONK promo with a 3D blocky look-alike of Bhupendra (client asked 2026-10-29: "30 seconds edit
# with a phonk, promotional, about Heaven Developer, with 3d animations, like 3d characters, preview first").
# 9:16. One scene per VO line (English, field voice gaming-hype); in every scene the CSS-3D character
# (library/tools/blocky_character.py rig, skin library/tools/make_bhupendra_skin.py) poses while hard phonk-style text
# slams in with flashes, RGB-split glow and hit shakes on the music's beats (skills #123 flash, #161/#162 shake on the hit,
# #372 picture 1-2 frames before the beat, #138 glitch). Facts: library/clients/heavendeveloper/brief.md.
# Needs in the project (scratchpad): assets/characters/bhupendra-skin.png, assets/img/logo_circle.png, assets/fonts
# (Anton, Outfit), assets/vendor/gsap, assets/sfx, assets/audio/mix.wav, assets/vo/lines.json, assets/music/beats.json
# (beat times of the fitted bed, from listen.py).
import importlib.util, json, os, subprocess

spec = importlib.util.spec_from_file_location("bc", "/home/user/new-startup/library/tools/blocky_character.py")
bc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bc)

VO_START = 0.3
BG, BLURPLE, GREEN, GOLD, WHITE = "#05040a", "#5865f2", "#58b234", "#f7dc94", "#ffffff"
L = json.load(open("assets/vo/lines.json"))
BEATS = json.load(open("assets/music/beats.json")) if os.path.exists("assets/music/beats.json") else []
TOTAL = float(os.environ.get("TOTAL", 30.0))
st = [round(VO_START + a - 0.1, 2) for a, _ in L]
st[0] = 0.0
SCENES = [(f"s{i + 1}", st[i], st[i + 1] if i + 1 < len(st) else TOTAL) for i in range(len(st))]
W = {k: (s, e) for k, s, e in SCENES}
SKIN = "assets/characters/bhupendra-skin.png"


def dur(p):
    return round(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                      capture_output=True, text=True).stdout), 3)


def rel(i, frac):
    a, b = L[i]
    return round(max(0.05, VO_START + a + frac * (b - a) - st[i]), 2)


def d_of(i):
    s, e = W[f"s{i + 1}"]
    return round(e - s, 2)


def beats_in(i):
    """beat times inside scene i, relative to the scene start"""
    s, e = W[f"s{i + 1}"]
    return [round(b - s, 3) for b in BEATS if s + 0.05 < b < e - 0.05]


CSS = f"""
    @font-face {{ font-family: "AN"; src: url("assets/fonts/Anton-Regular.ttf"); }}
    @font-face {{ font-family: "OU"; src: url("assets/fonts/Outfit-Bold.ttf"); font-weight: 700; }}
    #root {{ position: absolute; inset: 0; overflow: hidden; }}
    .c {{ position: absolute; left: 0; right: 0; text-align: center; }}
    .slam {{ font-family: AN; line-height: 0.95; color: {WHITE}; text-transform: uppercase;
             text-shadow: -6px 0 0 rgba(255,40,90,0.75), 6px 0 0 rgba(40,220,255,0.75), 0 10px 40px rgba(0,0,0,0.8); }}
    .sub {{ font-family: OU; font-weight: 700; color: {GOLD}; letter-spacing: 2px; text-shadow: 0 6px 24px rgba(0,0,0,0.8); }}
    .btn {{ display: inline-flex; align-items: center; gap: 24px; background: {BLURPLE}; color: #fff; font-family: AN;
            border-radius: 22px; padding: 26px 56px; font-size: 76px; box-shadow: 0 18px 60px rgba(88,101,242,0.6); }}
"""
DISCORD = bc_discord = '<path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0 12.64 12.64 0 0 0-.617-1.25.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 0 0 .031.057 19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028c.462-.63.874-1.295 1.226-1.994a.076.076 0 0 0-.041-.106 13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.128 10.2 10.2 0 0 0 .372-.292.074.074 0 0 1 .077-.01c3.929 1.793 8.18 1.793 12.061 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127 12.299 12.299 0 0 1-1.873.894.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.028zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.955-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.946 2.418-2.157 2.418z"></path>'


def character(P, d, moves, x=540, y=1560, scale=26, turn=-20, tilt=-6, enter="drop"):
    """html + js for one posed 3D character whose feet stand at (x, y)"""
    html = (f'<div class="{P}-stage" style="position:absolute;left:{x}px;top:{y}px;width:0;height:0;perspective:{80 * scale}px;'
            f'perspective-origin:0 {-16 * scale}px;"><div id="{P}-move" style="position:absolute;left:0;top:0;width:0;height:0;">'
            f'<div style="position:absolute;left:0;top:0;width:0;height:0;transform-style:preserve-3d;transform:rotateX({tilt}deg)">\n'
            f'{bc.rig_html(P, scale, "      ")}\n      </div></div></div>'
            f'<div id="{P}-shadow" style="position:absolute;left:{x - 6 * scale}px;top:{y - scale}px;width:{12 * scale}px;height:{2 * scale}px;'
            f'border-radius:50%;background:radial-gradient(closest-side, rgba(0,0,0,0.6), rgba(0,0,0,0));"></div>')
    js = "\n".join(bc.pose_js(P, scale, moves, d, turn)) + "\n"
    if enter == "drop":
        js += f'    tl.fromTo("#{P}-move", {{ y: -900 }}, {{ y: 0, duration: 0.45, ease: "bounce.out" }}, 0);\n'
    elif enter == "zoom":
        js += f'    tl.fromTo("#{P}-move", {{ scale: 2.2, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.4, ease: "power4.out" }}, 0);\n'
    elif enter == "side":
        js += f'    tl.fromTo("#{P}-move", {{ x: -900 }}, {{ x: 0, duration: 0.45, ease: "power4.out" }}, 0);\n'
    return html, js, bc.css(P, SKIN)


def slam(sel, at, frm="scale: 2.6, opacity: 0", ease="power4.out", d=0.22):
    return f'    tl.fromTo("{sel}", {{ {frm} }}, {{ scale: 1, x: 0, y: 0, opacity: 1, duration: {d}, ease: "{ease}" }}, {at:.2f});\n'


def shake(sel, at):
    # skill #161/#162: a short hit shake that starts on the hit; even repeat ends at rest (CLAUDE.md yoyo note)
    return f'    tl.fromTo("{sel}", {{ x: -14, y: 8 }}, {{ x: 12, y: -6, duration: 0.05, ease: "none", repeat: 4, yoyo: true }}, {at:.2f});\n'


def comp(cid, html, js, extra_css=""):
    return f"""<template>
  <style>{CSS}{extra_css}</style>
  <div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920" data-layout-allow-overflow>
{html}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{js}
    tl.to({{}}, {{ duration: {round(W[cid][1] - W[cid][0], 2) if cid in W else TOTAL} }}, 0);
    window.__timelines["{cid}"] = tl;
  </script>
</template>
"""


def wrap(k, d, inner, inner_js, ccss, exit_=True):
    js = inner_js + shake(f"#{k}-w", 0.0)
    if exit_:
        js += f'    tl.to("#{k}-w", {{ scale: 1.25, opacity: 0, filter: "blur(12px)", duration: 0.16, ease: "power3.in" }}, {d - 0.16:.2f});\n'
    return comp(k, f'    <div id="{k}-w" style="position:absolute;inset:0;">\n{inner}\n    </div>', js, ccss)


C, HITS = {}, []
# global background: near-black, two neon glows, scanlines, beat pulses; a white flash layer on every beat
pulses = "".join(f'    tl.fromTo("#bg-p", {{ opacity: 0.55 }}, {{ opacity: 0, duration: 0.3, ease: "power2.out" }}, {b:.3f});\n' for b in BEATS if b < TOTAL)
C["bg"] = comp("bg", f"""    <div style="position:absolute;inset:0;background:{BG};"></div>
    <div id="bg-g1" style="position:absolute;left:-300px;top:200px;width:1200px;height:1200px;border-radius:50%;background:radial-gradient(circle, rgba(88,101,242,0.35), rgba(88,101,242,0) 70%);"></div>
    <div id="bg-g2" style="position:absolute;left:300px;top:900px;width:1100px;height:1100px;border-radius:50%;background:radial-gradient(circle, rgba(88,178,52,0.25), rgba(88,178,52,0) 70%);"></div>
    <div id="bg-p" style="position:absolute;inset:0;background:radial-gradient(70% 50% at 50% 60%, rgba(140,150,255,0.45), rgba(0,0,0,0) 70%);opacity:0;"></div>
    <div style="position:absolute;inset:0;background:repeating-linear-gradient(0deg, rgba(255,255,255,0.035) 0 2px, rgba(0,0,0,0) 2px 6px);"></div>
    <div id="bg-floor" style="position:absolute;left:-200px;right:-200px;top:1500px;height:600px;background-image:linear-gradient(rgba(88,101,242,0.5) 2px, transparent 2px),linear-gradient(90deg, rgba(88,101,242,0.5) 2px, transparent 2px);background-size:90px 90px;transform:perspective(600px) rotateX(70deg);transform-origin:50% 0;"></div>""",
               f'    tl.fromTo("#bg-g1", {{ x: 0 }}, {{ x: 500, duration: {TOTAL}, ease: "sine.inOut" }}, 0);\n'
               f'    tl.fromTo("#bg-g2", {{ x: 0 }}, {{ x: -600, duration: {TOTAL}, ease: "sine.inOut" }}, 0);\n'
               f'    tl.fromTo("#bg-floor", {{ backgroundPositionY: "0px" }}, {{ backgroundPositionY: "900px", duration: {TOTAL}, ease: "none" }}, 0);\n' + pulses)
C["flash"] = comp("flash", '    <div id="fl" style="position:absolute;inset:0;background:radial-gradient(circle at 50% 45%, rgba(255,255,255,0.95), rgba(255,255,255,0.5) 60%, rgba(255,255,255,0.2));opacity:0;"></div>',
                  "".join(f'    tl.fromTo("#fl", {{ opacity: 0.85 }}, {{ opacity: 0, duration: 0.35, ease: "power2.out" }}, {max(0, s - 0.04):.2f});\n' for _, s, _ in SCENES[1:]))

# 1 hook: character drops in, the three asks slam one after the other
i, k = 0, "s1"; d = d_of(i)
h, j, cc = character("c1", d, [[0, "idle"], [0.6, "shock"], [2.0, "think"]], enter="drop")
asks = [("DISCORD BOT?", "#9aa3ff", 0.0), ("WEBSITE?", WHITE, 0.42), ("MINECRAFT PLUGIN?", GOLD, 0.66)]
txt = '<div class="c slam" style="top:250px;font-size:120px;">NEED A</div>' + "".join(
    f'<div class="c slam" id="s1-a{n}" style="top:{390 + n * 150}px;font-size:{140 if n < 2 else 112}px;color:{c};">{t}</div>' for n, (t, c, _) in enumerate(asks))
js = j + "".join(slam(f"#s1-a{n}", rel(i, f) if f else 0.15) + shake("#s1-w", rel(i, f) if f else 0.15) for n, (_, _, f) in enumerate(asks))
HITS += [W[k][0] + (rel(i, f) if f else 0.15) for _, _, f in asks]
C[k] = wrap(k, d, txt + h, js, cc)

# 2 logo + name
i, k = 1, "s2"; d = d_of(i)
h, j, cc = character("c2", d, [[0, "idle"], [0.3, "point"]], enter="zoom", y=1640, scale=24)
txt = ('<div id="s2-logo" style="position:absolute;left:290px;top:250px;width:500px;height:500px;border-radius:50%;overflow:hidden;box-shadow:0 0 90px rgba(247,220,148,0.6);">'
       '<img src="assets/img/logo_circle.png" style="width:500px;height:500px;" alt="Heaven Developer logo"></div>'
       '<div class="c slam" id="s2-n" style="top:790px;font-size:150px;color:#f7dc94;">HEAVEN DEVELOPER</div>'
       '<div class="c sub" id="s2-s" style="top:960px;font-size:56px;">BUILDS IT ALL</div>')
js = (j + '    tl.fromTo("#s2-logo", { scale: 0.2, rotation: -40, opacity: 0 }, { scale: 1, rotation: 0, opacity: 1, duration: 0.4, ease: "back.out(1.8)" }, 0.02);\n'
      + slam("#s2-n", rel(i, 0.05)) + shake("#s2-w", rel(i, 0.05)) + slam("#s2-s", rel(i, 0.6), "y: 60, opacity: 0"))
HITS.append(W[k][0] + rel(i, 0.05))
C[k] = wrap(k, d, txt + h, js, cc)

# 3 services: one word slams at a time over the talking character
i, k = 2, "s3"; d = d_of(i)
h, j, cc = character("c3", d, [[0, "talk"]], enter="side", turn=-30)
SV = ["BOTS", "WEBSITES", "PLUGINS", "MODS", "TEXTURE PACKS"]
txt = "".join(f'<div class="c slam" id="s3-v{n}" style="top:420px;font-size:{220 if n < 4 else 160}px;opacity:0;color:{[WHITE, "#9aa3ff", GOLD, "#7fe05a", WHITE][n]};">{t}</div>' for n, t in enumerate(SV))
js = j
for n in range(len(SV)):
    a = rel(i, 0.05 + n * 0.19)
    js += slam(f"#s3-v{n}", a) + shake("#s3-w", a)
    if n + 1 < len(SV):
        js += f'    tl.to("#s3-v{n}", {{ opacity: 0, scale: 0.6, duration: 0.1 }}, {rel(i, 0.05 + (n + 1) * 0.19) - 0.08:.2f});\n'
    HITS.append(W[k][0] + a)
C[k] = wrap(k, d, txt + h, js, cc)

# 4 price: giant $4 behind the character, who reacts
i, k = 3, "s4"; d = d_of(i)
h, j, cc = character("c4", d, [[0, "idle"], [rel(i, 0.6), "shock"]], enter="drop")
txt = ('<div class="c sub" id="s4-a" style="top:300px;font-size:70px;">STARTING FROM</div>'
       '<div class="c slam" id="s4-p" style="top:380px;font-size:620px;color:#ffd76a;">$4</div>')
js = j + slam("#s4-a", 0.1, "y: -60, opacity: 0") + slam("#s4-p", rel(i, 0.62), "scale: 4, opacity: 0") + shake("#s4-w", rel(i, 0.62))
HITS.append(W[k][0] + rel(i, 0.62))
CASH = W[k][0] + rel(i, 0.62)
C[k] = wrap(k, d, txt + h, js, cc)

# 5 invite rewards
i, k = 4, "s5"; d = d_of(i)
h, j, cc = character("c5", d, [[0, "wave"]], enter="zoom")
txt = ('<div class="c slam" id="s5-a" style="top:300px;font-size:150px;">INVITE <span style="color:#ffd76a;">3</span></div>'
       '<div class="c slam" id="s5-b" style="top:460px;font-size:150px;">FRIENDS</div>'
       '<div class="c slam" id="s5-c" style="top:640px;font-size:120px;color:#7fe05a;">= FREE PROJECT</div>')
js = j + slam("#s5-a", 0.1) + slam("#s5-b", rel(i, 0.25)) + slam("#s5-c", rel(i, 0.62)) + shake("#s5-w", rel(i, 0.62))
HITS += [W[k][0] + 0.1, W[k][0] + rel(i, 0.62)]
C[k] = wrap(k, d, txt + h, js, cc)

# 6 three steps
i, k = 5, "s6"; d = d_of(i)
h, j, cc = character("c6", d, [[0, "walk"]], enter="side", turn=-35)
ST = ["OPEN A TICKET", "SHARE YOUR IDEA", "WE DELIVER"]
txt = "".join(f'<div class="c slam" id="s6-k{n}" style="top:{300 + n * 190}px;font-size:{130 if n < 2 else 150}px;color:{[WHITE, "#9aa3ff", "#ffd76a"][n]};">{t}</div>' for n, t in enumerate(ST))
js = j
for n in range(3):
    a = rel(i, 0.02 + n * 0.33)
    js += slam(f"#s6-k{n}", a, "x: -700, opacity: 0") + shake("#s6-w", a)
    HITS.append(W[k][0] + a)
C[k] = wrap(k, d, txt + h, js, cc)

# 7 end card
i, k = 6, "s7"; d = d_of(i)
h, j, cc = character("c7", d, [[0, "wave"], [2.2, "spin"], [3.4, "wave"]], enter="drop", y=1700, scale=22)
txt = ('<div id="s7-logo" style="position:absolute;left:390px;top:200px;width:300px;height:300px;border-radius:50%;overflow:hidden;box-shadow:0 0 80px rgba(247,220,148,0.55);">'
       '<img src="assets/img/logo_circle.png" style="width:300px;height:300px;" alt="Heaven Developer logo"></div>'
       '<div class="c slam" id="s7-n" style="top:540px;font-size:120px;color:#f7dc94;">HEAVEN DEVELOPER</div>'
       f'<div class="c" id="s7-b" style="top:720px;"><span class="btn"><svg viewBox="0 0 24 24" style="width:80px;height:80px;" fill="#fff">{DISCORD}</svg>JOIN ON DISCORD</span></div>'
       '<div class="c sub" id="s7-u" style="top:900px;font-size:58px;color:#fff;">discord.gg/<span style="color:#f7dc94;">heavendeveloper</span></div>')
js = (j + '    tl.fromTo("#s7-logo", { scale: 0.2, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.4, ease: "back.out(1.8)" }, 0.05);\n'
      + slam("#s7-n", 0.15) + slam("#s7-b", rel(i, 0.55)) + shake("#s7-w", rel(i, 0.55))
      + f'    tl.to("#s7-b", {{ scale: 1.07, duration: 0.3, ease: "sine.inOut", yoyo: true, repeat: 6 }}, {rel(i, 0.55) + 0.3:.2f});\n'
      + slam("#s7-u", rel(i, 0.75), "y: 60, opacity: 0"))
HITS.append(W[k][0] + rel(i, 0.55))
JOIN = W[k][0] + rel(i, 0.55)
C[k] = wrap(k, d, txt + h, js, cc, exit_=False)

os.makedirs("compositions", exist_ok=True)
for kk, v in C.items():
    open(f"compositions/{kk}.html", "w").write(v)
div = lambda kk, s, d_, lane, z: (f'      <div id="{kk}" data-composition-id="{kk}" data-composition-src="compositions/{kk}.html" data-start="{s}" data-duration="{d_}" '
                                  f'data-track-index="{lane}" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: {z}"></div>')
divs = [div("bg", 0, TOTAL, 0, 0)] + [div(kk, s, round(e - s, 3), 1, 1) for kk, s, e in SCENES] + [div("flash", 0, TOTAL, 2, 2)]
sfx = lambda n: f"assets/sfx/{n}.mp3"
A = [("mix", "assets/audio/mix.wav", 0, min(dur("assets/audio/mix.wav"), TOTAL), 1.0, 10)]
# rotate impact variants so the hits do not repeat one sound (Mr Aloo feedback 2026-10-28, CLAUDE.md)
HIT_SFX = ["impact-boom", "sub-drop", "punch-heavy"]
for n, t in enumerate(sorted(HITS)):
    f = HIT_SFX[n % len(HIT_SFX)]
    if os.path.exists(sfx(f)):
        A.append((f"hit{n}", sfx(f), round(t, 2), dur(sfx(f)), 0.32, 11 + n % 3))
for n, (kk, s, e) in enumerate(SCENES[1:]):
    f = ["whoosh-fast-0.3s", "swish-4"][n % 2] if os.path.exists(sfx("swish-4")) else "whoosh-fast-0.3s"
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
print("built", TOTAL, SCENES, len(HITS), "hits")
