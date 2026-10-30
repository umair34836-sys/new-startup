# "Who is Herobrine" 9:16 cinematic lore Short (portal order 2, 2026-10-30). One scene per VO line; a CSS-3D blocky
# shadow figure with white eyes (own skin) in every scene, slow push-ins, fog, lightning, soft blur cross-fades,
# English word-group captions from Whisper word times. Facts: library/research/herobrine.md (minecraft.wiki, 2026-10-30).
# Base: library/templates/phonk-3d-promo/build_heavendeveloper_phonk.py (character(), comp(), audio lanes).
# Needs in the project: assets/characters/shadow-skin.png, assets/fonts (Anton, Poppins-Bold), assets/vendor gsap,
# assets/sfx, assets/video (smoke-fog-vertical, lightning-storm-night), assets/audio/mix.wav, assets/vo/lines.json,
# assets/vo/words.json ([[start, end, word], ...] relative to the VO file).
import html, importlib.util, json, os, subprocess

spec = importlib.util.spec_from_file_location("bc", "/home/user/new-startup/library/tools/blocky_character.py")
bc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bc)

VO_START = float(os.environ.get("VO_START", 0.6))
BG, WHITE, ICE, RED, GOLD = "#04050a", "#f2f4ff", "#bcd2ff", "#e62117", "#f7dc94"
L = json.load(open("assets/vo/lines.json"))
WORDS = json.load(open("assets/vo/words.json"))
TOTAL = float(os.environ.get("TOTAL", 20.0))
st = [round(VO_START + a - 0.15, 2) for a, _ in L]
st[0] = 0.0
SCENES = [(f"s{i + 1}", st[i], st[i + 1] if i + 1 < len(st) else TOTAL) for i in range(len(st))]
W = {k: (s, e) for k, s, e in SCENES}
SKIN = "assets/characters/shadow-skin.png"
XF = 0.35  # cross-fade length


def dur(p):
    return round(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                      capture_output=True, text=True).stdout), 3)


def rel(i, frac):
    a, b = L[i]
    return round(max(0.05, VO_START + a + frac * (b - a) - st[i]), 2)


def d_of(i):
    s, e = W[f"s{i + 1}"]
    return round(e - s, 2)


CSS = f"""
    @font-face {{ font-family: "AN"; src: url("assets/fonts/Anton-Regular.ttf"); }}
    @font-face {{ font-family: "PO"; src: url("assets/fonts/Poppins-Bold.ttf"); font-weight: 700; }}
    #root {{ position: absolute; inset: 0; overflow: hidden; }}
    .c {{ position: absolute; left: 60px; right: 60px; text-align: center; }}
    .big {{ font-family: AN; line-height: 0.95; color: {WHITE}; text-transform: uppercase; letter-spacing: 2px;
            text-shadow: 0 0 30px rgba(170,200,255,0.45), 0 12px 40px rgba(0,0,0,0.9); }}
    .sub {{ font-family: PO; font-weight: 700; color: {ICE}; letter-spacing: 6px; text-transform: uppercase;
            text-shadow: 0 6px 24px rgba(0,0,0,0.9); }}
    .card {{ background: rgba(10,12,22,0.82); border: 2px solid rgba(188,210,255,0.35); border-radius: 26px;
             box-shadow: 0 30px 90px rgba(0,0,0,0.7); font-family: PO; color: {WHITE}; padding: 46px 52px; text-align: left; }}
"""


def character(P, d, moves, x=540, y=1650, scale=20, turn=-20, tilt=-6):
    html_ = (f'<div class="{P}-stage" style="position:absolute;left:{x}px;top:{y}px;width:0;height:0;perspective:{80 * scale}px;'
             f'perspective-origin:0 {-16 * scale}px;"><div id="{P}-move" style="position:absolute;left:0;top:0;width:0;height:0;">'
             f'<div style="position:absolute;left:0;top:0;width:0;height:0;transform-style:preserve-3d;transform:rotateX({tilt}deg)">\n'
             f'{bc.rig_html(P, scale, "      ")}\n      </div></div></div>'
             f'<div id="{P}-shadow" style="position:absolute;left:{x - 6 * scale}px;top:{y - scale}px;width:{12 * scale}px;height:{2 * scale}px;'
             f'border-radius:50%;background:radial-gradient(closest-side, rgba(0,0,0,0.7), rgba(0,0,0,0));"></div>')
    js = "\n".join(bc.pose_js(P, scale, moves, d, turn)) + "\n"
    return html_, js, bc.css(P, SKIN)


def eyes(k, x, y, size, at=0.0):
    """two soft white glows over the figure's eyes (2D layer above the 3D rig)"""
    g = lambda n, dx: (f'<div id="{k}-e{n}" style="position:absolute;left:{x + dx - size}px;top:{y - size}px;width:{2 * size}px;height:{2 * size}px;'
                       f'border-radius:50%;background:radial-gradient(circle, rgba(255,255,255,0.95), rgba(200,220,255,0.35) 35%, rgba(255,255,255,0) 70%);opacity:0;"></div>')
    sep = size * 0.75
    h = g(1, -sep) + g(2, sep)
    js = (f'    tl.fromTo(["#{k}-e1", "#{k}-e2"], {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5, ease: "power2.out" }}, {at:.2f});\n'
          f'    tl.to(["#{k}-e1", "#{k}-e2"], {{ opacity: 0.55, duration: 0.6, ease: "sine.inOut", yoyo: true, repeat: 4 }}, {at + 0.5:.2f});\n')
    return h, js


def comp(cid, html_, js, extra_css="", d=None):
    return f"""<template>
  <style>{CSS}{extra_css}</style>
  <div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920" data-layout-allow-overflow data-layout-allow-occlusion>
{html_}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{js}
    tl.to({{}}, {{ duration: {d if d else TOTAL} }}, 0);
    window.__timelines["{cid}"] = tl;
  </script>
</template>
"""


def wrap(k, d, inner, inner_js, ccss, first=False, last=False):
    # cinematic: slow push-in over the whole scene, blur cross-fade in and out (no hard slams)
    js = inner_js + f'    tl.fromTo("#{k}-w", {{ scale: 1.0 }}, {{ scale: 1.08, duration: {d}, ease: "none" }}, 0);\n'
    if not first:
        js += f'    tl.fromTo("#{k}-w", {{ opacity: 0, filter: "blur(14px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: {XF}, ease: "power2.out" }}, 0);\n'
    if not last:
        js += f'    tl.to("#{k}-w", {{ opacity: 0, filter: "blur(14px)", duration: {XF}, ease: "power2.in" }}, {d - XF:.2f});\n'
    return comp(k, f'    <div id="{k}-w" style="position:absolute;inset:0;transform-origin:50% 45%;">\n{inner}\n    </div>', js, ccss, d)


def rise(sel, at, dy=50, d=0.6):
    return f'    tl.fromTo("{sel}", {{ y: {dy}, opacity: 0, filter: "blur(8px)" }}, {{ y: 0, opacity: 1, filter: "blur(0px)", duration: {d}, ease: "power3.out" }}, {at:.2f});\n'


C, SFX = {}, []
# background: deep night gradient, faint lightning video, moving fog video on top of the scenes (separate comps)
C["bg"] = comp("bg", f"""    <div style="position:absolute;inset:0;background:radial-gradient(120% 70% at 50% 35%, #141a2e 0%, #070912 55%, {BG} 100%);"></div>
    <video id="bg-l" src="assets/video/lightning-storm-night.mp4" muted playsinline data-start="0" data-duration="12" data-track-index="0"
      style="position:absolute;left:-1166px;top:0;width:3413px;height:1920px;object-fit:cover;opacity:0.28;"></video>
    <div style="position:absolute;left:0;right:0;top:1480px;bottom:0;background:linear-gradient(#0b0f1a, #020306);"></div>""", "")
C["fog"] = comp("fog", """    <video id="fog-v" src="assets/video/smoke-fog-vertical.mp4" muted playsinline data-start="0" data-duration="10" data-track-index="0"
      style="position:absolute;inset:0;width:1080px;height:1920px;object-fit:cover;opacity:0.22;"></video>
    <div style="position:absolute;inset:0;background:radial-gradient(90% 70% at 50% 45%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.75) 100%);"></div>""", "")

# 1 hook (title on screen at 0 s for the thumbnail): far figure in the fog, eyes light up, lightning
i, k = 0, "s1"; d = d_of(i)
h, j, cc = character("c1", d, [[0, "idle"]], y=1560, scale=14, turn=0)
eh, ej = eyes("s1", 540, 1560 - 14 * 28 + 4, 16, 0.5)
txt = ('<div class="c sub" id="s1-a" style="top:430px;font-size:64px;">Who is</div>'
       '<div class="c big" id="s1-b" style="top:520px;font-size:190px;">HEROBRINE?</div>')
js = j + ej  # title static from 0 s (thumbnail)
SFX.append(("thunder", "rain-thunder", 0.0, 0.5))
C[k] = wrap(k, d, txt + h + eh, js, cc, first=True)

# 2 close-up: the face fills the frame, eyes glow
i, k = 1, "s2"; d = d_of(i)
h, j, cc = character("c2", d, [[0, "idle"]], y=2350, scale=44, turn=0, tilt=-2)
eh, ej = eyes("s2", 540, 2350 - 44 * 28 + 12, 34, 0.2)
txt = ('<div class="c sub" id="s2-a" style="top:260px;font-size:58px;">A Minecraft legend</div>'
       '<div class="c big" id="s2-b" style="top:340px;font-size:120px;">GLOWING<br>WHITE EYES</div>')
js = j + ej + rise("#s2-a", 0.1) + rise("#s2-b", rel(i, 0.45))
SFX.append(("heart", "heartbeat", W[k][0] + 0.2, 0.55))
C[k] = wrap(k, d, txt + h + eh, js, cc)

# 3 origin: 2010, fan forums
i, k = 2, "s3"; d = d_of(i)
h, j, cc = character("c3", d, [[0, "walk"]], x=760, y=1640, scale=16, turn=-60)
txt = ('<div class="c big" id="s3-y" style="top:300px;font-size:330px;color:#dfe6ff;">2010</div>'
       '<div class="c sub" id="s3-s" style="top:660px;font-size:52px;">Minecraft Forum · July 31</div>')
js = j + rise("#s3-y", 0.05) + rise("#s3-s", 0.3)
SFX.append(("boom1", "sub-drop", W[k][0] + 0.05, 0.4))
C[k] = wrap(k, d, txt + h, js, cc)

# 4 never in the game, not even in the code: the figure glitches away
i, k = 3, "s4"; d = d_of(i)
h, j, cc = character("c4", d, [[0, "idle"]], y=1600, scale=20, turn=-15)
txt = '<div class="c big" id="s4-a" style="top:330px;font-size:170px;">NEVER IN<br>THE GAME</div>'
ga = rel(i, 0.6)
js = (j + rise("#s4-a", 0.05)
      + f'    tl.fromTo("#c4-move", {{ x: -18, skewX: 12 }}, {{ x: 14, skewX: -8, duration: 0.05, ease: "none", repeat: 6, yoyo: true }}, {ga:.2f});\n'
      + f'    tl.to("#c4-move", {{ opacity: 0, duration: 0.25, ease: "power2.in" }}, {ga + 0.35:.2f});\n'
      + f'    tl.to("#c4-shadow", {{ opacity: 0, duration: 0.25 }}, {ga + 0.35:.2f});\n')
SFX.append(("glitch", "glitch-short", W[k][0] + ga, 0.45))
C[k] = wrap(k, d, txt + h, js, cc)

# 5 Notch's own words (his automatic email reply, quoted on minecraft.wiki)
i, k = 4, "s5"; d = d_of(i)
txt = ('<div class="card" id="s5-k" style="position:absolute;left:90px;right:90px;top:520px;font-size:62px;line-height:1.3;">'
       '<div style="font-family:AN;font-size:160px;color:#9fb4e6;line-height:0.6;">&ldquo;</div>'
       '&hellip;never has been part of Minecraft.'
       '<div style="margin-top:34px;font-size:40px;color:#8fa6d8;letter-spacing:2px;">NOTCH, CREATOR OF MINECRAFT</div></div>')
js = rise("#s5-k", 0.0, 40, 0.35)
C[k] = wrap(k, d, txt, js, "")

# 6 the running joke: "Removed Herobrine" in the update notes
i, k = 5, "s6"; d = d_of(i)
h, j, cc = character("c6", d, [[0, "idle"], [0.8, "think"]], x=800, y=1680, scale=16, turn=-35)
txt = ('<div class="c sub" id="s6-a" style="top:300px;font-size:56px;">Update notes still say</div>'
       '<div class="card" id="s6-k" style="position:absolute;left:90px;right:90px;top:430px;font-size:46px;">'
       '<div style="color:#8fa6d8;font-size:32px;letter-spacing:3px;">JAVA EDITION BETA 1.6.6 · CHANGELOG</div>'
       '<div id="s6-r" style="margin-top:26px;font-family:AN;font-size:84px;color:#fff;white-space:nowrap;">• REMOVED HEROBRINE</div></div>')
js = (j + rise("#s6-a", 0.05) + rise("#s6-k", 0.25, 70)
      + f'    tl.fromTo("#s6-r", {{ color: "#ffffff" }}, {{ color: "{GOLD}", duration: 0.4 }}, {rel(i, 0.7):.2f});\n')
C[k] = wrap(k, d, txt + h, js, cc)

# 7 call to action: subscribe to the channel
i, k = 6, "s7"; d = d_of(i)
h, j, cc = character("c7", d, [[0, "wave"], [2.0, "idle"]], y=1650, scale=18, turn=-10)
bell = '<svg viewBox="0 0 24 24" style="width:70px;height:70px;" fill="#fff"><path d="M12 22a2.5 2.5 0 0 0 2.45-2h-4.9A2.5 2.5 0 0 0 12 22zm7-6V11a7 7 0 0 0-5.5-6.84V3.5a1.5 1.5 0 0 0-3 0v.66A7 7 0 0 0 5 11v5l-2 2v1h18v-1z"/></svg>'
txt = ('<div class="c big" id="s7-n" style="top:300px;font-size:130px;color:#fff;">MRCOPPER804</div>'
       f'<div class="c" id="s7-b" style="top:480px;"><span style="display:inline-flex;align-items:center;gap:24px;background:{RED};color:#fff;font-family:AN;'
       'border-radius:20px;padding:24px 60px;font-size:96px;box-shadow:0 20px 70px rgba(230,33,23,0.55);">SUBSCRIBE ' + bell + '</span></div>'
       )
js = (j + rise("#s7-n", 0.05) + rise("#s7-b", rel(i, 0.15), 60)
      + f'    tl.to("#s7-b", {{ scale: 1.06, duration: 0.35, ease: "sine.inOut", yoyo: true, repeat: 5 }}, {rel(i, 0.15) + 0.6:.2f});\n'
      )
SFX.append(("boom2", "impact-boom", W[k][0] + rel(i, 0.15), 0.3))
C[k] = wrap(k, d, txt + h, js, cc, last=True)

# captions: Whisper word groups (3-4 words, skill #383), one gold word per group, over a dark pill above the bottom 20%
groups, cur = [], []
for w in WORDS:
    cur.append(w)
    if len(cur) >= 4 or w[2].rstrip().endswith((".", "?", ",", "!", ":")):
        groups.append(cur); cur = []
if cur:
    groups.append(cur)
cap_html, cap_js = "", ""
for n, g in enumerate(groups):
    a = VO_START + g[0][0]
    b = VO_START + (groups[n + 1][0][0] if n + 1 < len(groups) else g[-1][1] + 0.4)
    b = min(b, VO_START + g[-1][1] + 0.6)
    words = [html.escape(w[2].strip()) for w in g]
    longest = max(range(len(words)), key=lambda q: len(words[q]))
    words[longest] = f'<span style="color:{GOLD};">{words[longest]}</span>'
    cap_html += (f'<div id="cp{n}" class="c" style="top:1340px;opacity:0;"><span style="display:inline-block;background:rgba(0,0,0,0.62);'
                 f'border-radius:16px;padding:12px 30px;font-family:PO;font-weight:700;font-size:62px;color:#fff;">{" ".join(words)}</span></div>')
    cap_js += (f'    tl.fromTo("#cp{n}", {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: 0.12, ease: "power2.out" }}, {a:.2f});\n'
               f'    tl.to("#cp{n}", {{ opacity: 0, duration: 0.1 }}, {max(a + 0.2, b - 0.1):.2f});\n')
C["caps"] = comp("caps", cap_html, cap_js)

os.makedirs("compositions", exist_ok=True)
for kk, v in C.items():
    open(f"compositions/{kk}.html", "w").write(v)
div = lambda kk, s, d_, lane, z: (f'      <div id="{kk}" data-composition-id="{kk}" data-composition-src="compositions/{kk}.html" data-start="{s}" data-duration="{d_}" '
                                  f'data-track-index="{lane}" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: {z}"></div>')
divs = ([div("bg", 0, TOTAL, 0, 0)] + [div(kk, s, round(e - s + (XF if e < TOTAL else 0), 3), 1 + n % 2, 1) for n, (kk, s, e) in enumerate(SCENES)]
        + [div("fog", 0, TOTAL, 3, 2), div("caps", 0, TOTAL, 4, 3)])
A = [("mix", "assets/audio/mix.wav", 0, min(dur("assets/audio/mix.wav"), TOTAL), 1.0, 10)]
for n, (a, f, t, v) in enumerate(SFX):
    p = f"assets/sfx/{f}.mp3"
    A.append((a, p, round(t, 2), min(dur(p), TOTAL - t), v, 20 + n))
A.append(("wind", "assets/sfx/wind-loop.mp3", 0, min(dur("assets/sfx/wind-loop.mp3"), TOTAL), 0.18, 30))
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
print("built", TOTAL, SCENES, len(groups), "caption groups")
