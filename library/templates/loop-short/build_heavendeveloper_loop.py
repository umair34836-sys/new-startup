# Heaven Developer LOOP SHORT (YouTube Short, 9:16, from scratch, 2026-10-30). Owner: "entertaining and promotional video
# youtube short k lie ... natural female voice ... hook ... video ko ek loop me rakho (user ko pata na lage k end hogya hai)
# ... repo + discord screen recording ki saari info ... dark look and white look dono ... heaven developer ki skin".
#   THEME=dark|light python3 build_heavendeveloper_loop.py      (run inside the project folder)
# How the loop works (decision-guide 14: "end on a frame that leads into the first, trim music to whole bars"):
#  - the last VO line ends "...because if you still" and the first line is "Need a Discord bot, a website, or a Minecraft
#    plugin?", so the sentence runs across the seam;
#  - the music bed is a whole number of bars cut from one steady section (no fade), so bar N+1 = bar 1 of the replay;
#  - the end card clears in its last beat and puts back exactly the frame-0 layout ("NEED A" + the character in the wide
#    shot, idle), the background drift is a full sine period, and no flash/whoosh sits on the seam.
# Facts: library/clients/heavendeveloper/brief.md (recordings 1 + 2). Real screens = crops of the client's Discord
# recordings (scratchpad only). Skin: the client's own skin (scratchpad only). Captions: word-timed, above the bottom 420 px.
import importlib.util, json, os, subprocess

spec = importlib.util.spec_from_file_location("bc", "/home/user/new-startup/library/tools/blocky_character.py")
bc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bc)

THEME = os.environ.get("THEME", "dark")
T = {
    "dark": dict(bg="#090a12", ink="#ffffff", sub="#c9cdf5", acc="#7c87ff", gold="#f7d27a", glow1="rgba(88,101,242,0.42)",
                 glow2="rgba(247,210,122,0.16)", card="#111320", cardsh="0 30px 90px rgba(0,0,0,0.65), 0 0 0 2px rgba(124,135,255,0.35)",
                 chip="rgba(20,22,40,0.9)", chipb="rgba(124,135,255,0.6)", grid="rgba(124,135,255,0.18)", cap="rgba(0,0,0,0.62)", capink="#ffffff", hl="#f7d27a", shadow="rgba(0,0,0,0.55)"),
    "light": dict(bg="#f5f6fb", ink="#14151c", sub="#4b4f6b", acc="#4752e0", gold="#a8740a", glow1="rgba(88,101,242,0.20)",
                  glow2="rgba(247,180,60,0.18)", card="#ffffff", cardsh="0 30px 80px rgba(40,44,90,0.22), 0 0 0 2px rgba(71,82,224,0.18)",
                  chip="#ffffff", chipb="rgba(71,82,224,0.45)", grid="rgba(71,82,224,0.10)", cap="rgba(255,255,255,0.92)", capink="#14151c", hl="#4752e0", shadow="rgba(30,34,90,0.28)"),
}[THEME]
L = json.load(open("assets/vo/lines.json"))          # [[start, end], ...] of each VO line in the final timeline
WORDS = json.load(open("assets/vo/words.json"))     # [[word, start, end], ...] (Whisper word timestamps, final timeline)
EV = json.load(open("assets/music/events.json"))
TOTAL = float(open("assets/music/total.txt").read())
BEATS = [b for b in EV["beats"] if b < TOTAL - 0.2]
st = [0.0] + [round(a - 0.12, 3) for a, _ in L[1:]]
SCENES = [(f"s{i + 1}", st[i], st[i + 1] if i + 1 < len(st) else TOTAL) for i in range(len(st))]
W = {k: (s, e) for k, s, e in SCENES}
SKIN = "assets/characters/bhupendra-skin.png"
SC = 17
TX = "assets/textures"


def dur(p):
    return round(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                      capture_output=True, text=True).stdout), 3)


def d_of(i):
    s, e = W[f"s{i + 1}"]
    return round(e - s, 3)


def at(i, frac):
    """time inside scene i at a fraction of its VO line"""
    a, b = L[i]
    return round(max(0.05, a + frac * (b - a) - st[i]), 2)


def word_at(i, word, default=0.3):
    """scene-relative start of the first spoken `word` inside line i (so text lands on the word)"""
    a, b = L[i]
    for w, s, e in WORDS:
        if a - 0.05 <= s <= b + 0.05 and word.lower() in w.lower():
            return round(max(0.03, s - st[i] - 0.04), 2)
    return default


def inside(i, times):
    s, e = W[f"s{i + 1}"]
    return [round(t - s, 3) for t in times if s + 0.05 < t < e - 0.2]


CSS = f"""
    @font-face {{ font-family: "PX"; src: url("assets/fonts/Poppins-ExtraBold.ttf"); font-weight: 800; }}
    @font-face {{ font-family: "PB"; src: url("assets/fonts/Poppins-Bold.ttf"); font-weight: 700; }}
    @font-face {{ font-family: "PS"; src: url("assets/fonts/Poppins-SemiBold.ttf"); font-weight: 600; }}
    #root {{ position: absolute; inset: 0; overflow: hidden; }}
    .c {{ position: absolute; left: 0; right: 0; text-align: center; }}
    .h {{ font-family: PX; font-weight: 800; color: {T['ink']}; line-height: 1.02; letter-spacing: -2px; }}
    .s {{ font-family: PS; font-weight: 600; color: {T['sub']}; }}
    .acc {{ color: {T['acc']}; }} .gold {{ color: {T['gold']}; }}
    .chip {{ display: inline-block; font-family: PB; font-weight: 700; font-size: 52px; color: {T['ink']}; background: {T['chip']};
             border: 3px solid {T['chipb']}; border-radius: 999px; padding: 14px 40px; box-shadow: {T['cardsh']}; }}
    .card {{ position: absolute; border-radius: 34px; overflow: hidden; background: {T['card']}; box-shadow: {T['cardsh']}; }}
    .card img {{ display: block; width: 100%; }}
    .cap {{ position: absolute; left: 70px; right: 70px; top: 1230px; text-align: center; }}
    .cap span {{ display: inline-block; font-family: PX; font-weight: 800; font-size: 58px; color: {T['capink']}; background: {T['cap']};
                 padding: 8px 18px; margin: 4px 6px; border-radius: 16px; }}
    .btn {{ display: inline-flex; align-items: center; gap: 22px; background: #5865f2; color: #fff; font-family: PX; font-weight: 800;
            border-radius: 28px; padding: 26px 54px; font-size: 64px; box-shadow: 0 20px 60px rgba(88,101,242,0.5); }}
    .cube {{ position: absolute; width: 0; height: 0; transform-style: preserve-3d; }}
    .cube i {{ position: absolute; display: block; background-size: 100% 100%; image-rendering: pixelated; backface-visibility: hidden; }}
"""
DISCORD = '<path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0 12.64 12.64 0 0 0-.617-1.25.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 0 0 .031.057 19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028c.462-.63.874-1.295 1.226-1.994a.076.076 0 0 0-.041-.106 13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.128 10.2 10.2 0 0 0 .372-.292.074.074 0 0 1 .077-.01c3.929 1.793 8.18 1.793 12.061 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127 12.299 12.299 0 0 1-1.873.894.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.028zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.955-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.946 2.418-2.157 2.418z"></path>'

SHOT = {"wide": dict(s=1.0, x=0, y=0, yaw=-20, pitch=-6), "close": dict(s=1.5, x=0, y=320, yaw=-12, pitch=-2),
        "left": dict(s=1.1, x=-40, y=60, yaw=40, pitch=-4), "right": dict(s=1.1, x=40, y=60, yaw=-50, pitch=-4),
        "low": dict(s=1.25, x=0, y=140, yaw=20, pitch=12)}
X0, Y0 = 540, 1880   # character feet: the frame-0 / loop-seam position


def character(P, d, moves, shots, x=X0, y=Y0):
    s0 = SHOT[shots[0][1]]
    html = (f'<div style="position:absolute;left:{x}px;top:{y}px;width:0;height:0;perspective:{80 * SC}px;perspective-origin:0 {-16 * SC}px;">'
            f'<div id="{P}-cam" style="position:absolute;left:0;top:0;width:0;height:0;transform-style:preserve-3d;">'
            f'<div id="{P}-move" style="position:absolute;left:0;top:0;width:0;height:0;transform-style:preserve-3d;">'
            f'<div id="{P}-yaw" style="position:absolute;left:0;top:0;width:0;height:0;transform-style:preserve-3d;">\n'
            f'{bc.rig_html(P, SC, "      ")}\n      </div></div></div></div>')
    js = "\n".join(bc.pose_js(P, SC, moves, d, 0)) + "\n"
    js += (f'    gsap.set("#{P}-cam", {{ scale: {s0["s"]}, x: {s0["x"]}, y: {s0["y"]}, rotationX: {s0["pitch"]} }});\n'
           f'    gsap.set("#{P}-yaw", {{ rotationY: {s0["yaw"]} }});\n')
    for n, (t, name) in enumerate(shots):
        p = SHOT[name]
        if n == 0:
            continue
        js += (f'    tl.to("#{P}-cam", {{ scale: {p["s"]}, x: {p["x"]}, y: {p["y"]}, rotationX: {p["pitch"]}, duration: 0.45, ease: "power3.inOut" }}, {t:.3f});\n'
               f'    tl.to("#{P}-yaw", {{ rotationY: {p["yaw"]}, duration: 0.45, ease: "power3.inOut" }}, {t:.3f});\n')
    return html, js, bc.css(P, SKIN)


def pop(sel, t, frm="y: 80, scale: 0.6, opacity: 0", d=0.42, ease="back.out(1.8)"):
    return f'    tl.fromTo("{sel}", {{ {frm} }}, {{ x: 0, y: 0, scale: 1, rotation: 0, opacity: 1, duration: {d}, ease: "{ease}" }}, {t:.2f});\n'


def out(sel, t, d=0.25):
    return f'    tl.to("{sel}", {{ y: -40, opacity: 0, duration: {d}, ease: "power2.in" }}, {t:.2f});\n'


def card(cid, src, x, y, w, h, img_w=None, img_y=0):
    iw = img_w or w
    return (f'<div class="card" id="{cid}" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;">'
            f'<img id="{cid}-i" src="{src}" style="width:{iw}px;" alt=""></div>')


def cube(cid, size, side, top=None, x=0, y=0):
    top = top or side
    h = size / 2
    f = [("translateZ", side, 0.9), ("rotateY(180deg) translateZ", side, 0.62), ("rotateY(90deg) translateZ", side, 0.75),
         ("rotateY(-90deg) translateZ", side, 0.75), ("rotateX(90deg) translateZ", top, 1.0), ("rotateX(-90deg) translateZ", top, 0.5)]
    faces = "".join(f'<i style="width:{size}px;height:{size}px;left:{-h}px;top:{-h}px;transform:{tf}({h}px);'
                    f'background-image:url(\'{TX}/{tx}.png\');filter:brightness({sh});"></i>' for tf, tx, sh in f)
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:0;height:0;perspective:1400px;" id="{cid}-o">'
            f'<div class="cube" id="{cid}">{faces}</div></div>')


def comp(cid, html, js):
    d = round(W[cid][1] - W[cid][0], 3) if cid in W else TOTAL
    return f"""<template>
  <style>{CSS}</style>
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


C, POP, WH = {}, [], []          # POP: soft pop SFX times, WH: whoosh times (absolute)
# background: soft drifting glows (one full sine period over TOTAL -> same at 0 and TOTAL), faint grid, beat breathing
C["bg"] = comp("bg", f"""    <div style="position:absolute;inset:0;background:{T['bg']};"></div>
    <div id="bg-g1" style="position:absolute;left:-360px;top:120px;width:1200px;height:1200px;border-radius:50%;background:radial-gradient(circle, {T['glow1']}, rgba(0,0,0,0) 70%);"></div>
    <div id="bg-g2" style="position:absolute;left:320px;top:980px;width:1100px;height:1100px;border-radius:50%;background:radial-gradient(circle, {T['glow2']}, rgba(0,0,0,0) 70%);"></div>
    <div style="position:absolute;inset:0;background-image:linear-gradient({T['grid']} 2px, transparent 2px),linear-gradient(90deg, {T['grid']} 2px, transparent 2px);background-size:120px 120px;"></div>
    <div style="position:absolute;left:300px;top:1830px;width:480px;height:90px;border-radius:50%;background:radial-gradient(closest-side, {T['shadow']}, rgba(0,0,0,0));"></div>
    <div id="bg-p" style="position:absolute;inset:0;background:radial-gradient(60% 40% at 50% 45%, {T['glow1']}, rgba(0,0,0,0) 70%);opacity:0;"></div>""",
               f'    tl.fromTo("#bg-g1", {{ x: 0, y: 0 }}, {{ x: 420, y: 160, duration: {TOTAL / 2:.3f}, ease: "sine.inOut", yoyo: true, repeat: 1 }}, 0);\n'
               f'    tl.fromTo("#bg-g2", {{ x: 0, y: 0 }}, {{ x: -460, y: -200, duration: {TOTAL / 2:.3f}, ease: "sine.inOut", yoyo: true, repeat: 1 }}, 0);\n'
               + "".join(f'    tl.fromTo("#bg-p", {{ opacity: 0.6 }}, {{ opacity: 0, duration: 0.4, ease: "power2.out", immediateRender: false }}, {b:.3f});\n'
                         for b in BEATS[::2]))

# 1 HOOK (frame 0 = loop seam): "NEED A" + character; the three asks pop on their words
i, k = 0, "s1"; d = d_of(i)
h, j, cc = character("c1", d, [[0, "idle"], [word_at(i, "bot"), "think"], [word_at(i, "plugin"), "point"]],
                     [(0, "wide"), (word_at(i, "website"), "close")])
asks = [("DISCORD BOT?", "acc", "bot"), ("WEBSITE?", "", "website"), ("MINECRAFT PLUGIN?", "gold", "plugin")]
html = ('    <div class="c h" id="s1-n" style="top:250px;font-size:96px;">Need a</div>\n'
        + "".join(f'    <div class="c h {c}" id="s1-a{n}" style="top:{380 + n * 150}px;font-size:{124 if n < 2 else 100}px;opacity:0;">{t}</div>\n'
                  for n, (t, c, _) in enumerate(asks)) + h)
js = j
for n, (_, _, w) in enumerate(asks):
    t = word_at(i, w, 0.3 + n * 0.6)
    js += pop(f"#s1-a{n}", t, "scale: 0.4, opacity: 0, rotation: -6")
    POP.append(W[k][0] + t)
js += out("#s1-n", d - 0.25) + "".join(out(f"#s1-a{n}", d - 0.25) for n in range(3))
C[k] = comp(k, f"<style>{cc}</style>\n" + html, js)

# 2 MEET: logo coin + name + footer line + the real banner from the recording
i, k = 1, "s2"; d = d_of(i)
h, j, cc = character("c2", d, [[0, "wave"], [1.4, "idle"]], [(0, "wide"), (1.2, "right")])
t_name = word_at(i, "heaven", 0.3)
html = (f'    <div id="s2-logo" style="position:absolute;left:390px;top:170px;width:300px;height:300px;border-radius:50%;overflow:hidden;box-shadow:0 0 90px rgba(247,210,122,0.55);opacity:0;">'
        f'<img src="assets/img/logo_circle.png" style="width:300px;height:300px;" alt="Heaven Developer logo"></div>\n'
        f'    <div class="c h gold" id="s2-n" style="top:500px;font-size:100px;opacity:0;">Heaven Developer</div>\n'
        f'    <div class="c s" id="s2-s" style="top:630px;font-size:46px;opacity:0;">Premium development, delivered</div>\n'
        + "    " + card("s2-b", "assets/img/banner.jpg", 110, 760, 860, 405, 860) + "\n" + h)
js = (j + f'    tl.fromTo("#s2-logo", {{ rotationY: -540, scale: 0.3, opacity: 0 }}, {{ rotationY: 0, scale: 1, opacity: 1, duration: 0.8, ease: "expo.out" }}, {max(0.05, t_name - 0.3):.2f});\n'
      + pop("#s2-n", t_name) + pop("#s2-s", word_at(i, "premium", 1.2), "y: 40, opacity: 0") + pop("#s2-b", word_at(i, "delivered", 1.8), "y: 200, rotation: 4, opacity: 0", 0.6, "expo.out")
      + f'    tl.fromTo("#s2-b-i", {{ scale: 1.0 }}, {{ scale: 1.08, duration: {d:.2f}, ease: "none" }}, 0);\n')
POP.append(W[k][0] + t_name)
C[k] = comp(k, f"<style>{cc}</style>\n" + html, js + "".join(out(s, d - 0.25) for s in ("#s2-logo", "#s2-n", "#s2-s", "#s2-b")))


def service_scene(i, k, title, cls, items, words, crop_y, pose_moves, shots, extra_html="", extra_js=""):
    """title + the real #services post panned to the right section + chips on their spoken words"""
    d = d_of(i)
    h, j, cc = character(f"c{i + 1}", d, pose_moves, shots)
    html = (f'    <div class="c h {cls}" id="{k}-t" style="top:170px;font-size:{108 if len(title) < 14 else 92}px;opacity:0;">{title}</div>\n'
            + "    " + card(f"{k}-sv", "assets/img/services.jpg", 120, 330, 840, 560, 840, crop_y) + "\n"
            + f'    <div class="c" style="top:930px;">' + "".join(f'<span class="chip" id="{k}-k{n}" style="margin:10px 8px;opacity:0;">{t}</span>' for n, t in enumerate(items)) + '</div>\n'
            + extra_html + h)
    js = j + pop(f"#{k}-t", 0.05, "x: -200, opacity: 0", 0.4, "expo.out") + pop(f"#{k}-sv", 0.15, "y: 160, opacity: 0", 0.5, "expo.out")
    js += f'    tl.fromTo("#{k}-sv-i", {{ y: {-crop_y} }}, {{ y: {-crop_y - 60}, duration: {d:.2f}, ease: "none" }}, 0);\n'
    for n, w in enumerate(words):
        t = word_at(i, w, 0.4 + n * 0.45)
        js += pop(f"#{k}-k{n}", t)
        POP.append(W[k][0] + t)
    js += extra_js + "".join(out(s, d - 0.25) for s in (f"#{k}-t", f"#{k}-sv") + tuple(f"#{k}-k{n}" for n in range(len(items))))
    WH.append(W[k][0])
    C[k] = comp(k, f"<style>{cc}</style>\n" + html, js)


# 3 bots / 4 websites / 5 Minecraft (the real #services post, panned to each section)
service_scene(2, "s3", "Discord Bots", "acc", ["Moderation", "Tickets", "Economy", "Dashboards"],
              ["moderation", "tickets", "economy", "dashboards"], 40, [[0, "talk"], [1.0, "point"]], [(0, "left"), (1.4, "wide")])
service_scene(3, "s4", "Websites", "", ["Portfolios", "Full web apps"], ["portfolios", "apps"], 180,
              [[0, "idle"], [0.4, "point"]], [(0, "right"), (1.2, "close")])
mc_cubes = "".join(cube(f"s5-q{n}", 150, sd, tp, x, 1120) for n, (sd, tp, x) in enumerate([("grass_side", "grass_top", 160), ("diamond_ore", None, 540), ("tnt_side", "tnt_top", 920)]))
mc_js = "".join(f'    gsap.set("#s5-q{n}", {{ rotationX: -24 }});\n    tl.fromTo("#s5-q{n}", {{ rotationY: {30 * n} }}, {{ rotationY: {30 * n + 300}, duration: {d_of(4):.2f}, ease: "none" }}, 0);\n'
                + pop(f"#s5-q{n}-o", 0.5 + 0.25 * n, "scale: 0, y: -300", 0.45, "back.out(2)") + f'    gsap.set("#s5-q{n}-o", {{ opacity: 0 }});\n'
                for n in range(3))
service_scene(4, "s5", "Minecraft", "gold", ["Plugins", "Mods", "Texture packs"], ["plugins", "mods", "texture"], 330,
              [[0, "idle"], [0.5, "wave"], [2.0, "nod"]], [(0, "low"), (1.6, "wide")], mc_cubes, mc_js + "".join(out(f"#s5-q{n}-o", d_of(4) - 0.25) for n in range(3)))

# 6 ORDER FLOW: the real "Choose a service" menu + the 3 steps from #create-ticket
i, k = 5, "s6"; d = d_of(i)
h, j, cc = character("c6", d, [[0, "idle"], [0.3, "point"]], [(0, "right"), (1.5, "wide")])
steps = [("1", "Choose", "pick"), ("2", "Fill the form", "form"), ("3", "Private ticket", "ticket")]
html = ("    " + card("s6-m", "assets/img/dropdown.jpg", 60, 170, 520, 820, 520) + "\n"
        + "".join(f'    <div id="s6-p{n}" style="position:absolute;left:620px;top:{240 + n * 240}px;width:420px;opacity:0;">'
                  f'<div class="h acc" style="font-size:96px;line-height:1;">{a}</div><div class="h" style="font-size:50px;line-height:1.05;">{b}</div></div>\n'
                  for n, (a, b, _) in enumerate(steps)) + h)
js = j + pop("#s6-m", 0.05, "x: -400, rotation: -4, opacity: 0", 0.5, "expo.out") + f'    tl.fromTo("#s6-m-i", {{ y: 0 }}, {{ y: -260, duration: {d:.2f}, ease: "sine.inOut" }}, 0);\n'
for n, (_, _, w) in enumerate(steps):
    t = word_at(i, w, 0.5 + n * 0.8)
    js += pop(f"#s6-p{n}", t, "x: 200, opacity: 0", 0.4, "expo.out")
    POP.append(W[k][0] + t)
js += "".join(out(s, d - 0.25) for s in ("#s6-m", "#s6-p0", "#s6-p1", "#s6-p2"))
WH.append(W[k][0])
C[k] = comp(k, f"<style>{cc}</style>\n" + html, js)

# 7 PROOF: the real server profile card (2,521 members) + counters
i, k = 6, "s7"; d = d_of(i)
h, j, cc = character("c7", d, [[0, "nod"], [1.2, "wave"]], [(0, "close"), (1.0, "wide")])
html = ("    " + card("s7-pr", "assets/img/profile.jpg", 90, 700, 900, 318, 900) + "\n"
        f'    <div class="c h gold" id="s7-a" style="top:170px;font-size:170px;opacity:0;">2,500+</div>\n'
        f'    <div class="c h" id="s7-b" style="top:370px;font-size:70px;opacity:0;">members</div>\n'
        f'    <div class="c h acc" id="s7-c" style="top:470px;font-size:70px;opacity:0;">17 server boosts</div>\n' + h)
tm, tb = word_at(i, "members", 1.0), word_at(i, "boosts", 2.2)
js = (j + pop("#s7-a", 0.05, "scale: 0.3, opacity: 0") + pop("#s7-b", tm, "y: 40, opacity: 0") + pop("#s7-c", tb, "y: 40, opacity: 0")
      + pop("#s7-pr", 0.25, "y: 200, opacity: 0", 0.5, "expo.out")
      + "".join(out(s, d - 0.25) for s in ("#s7-a", "#s7-b", "#s7-c", "#s7-pr")))
POP += [W[k][0] + 0.05, W[k][0] + tb]
WH.append(W[k][0])
C[k] = comp(k, f"<style>{cc}</style>\n" + html, js)

# 8 FREE: setup, then the payoff with a jump and blocks raining
i, k = 7, "s8"; d = d_of(i)
tf = word_at(i, "free", 1.2)
h, j, cc = character("c8", d, [[0, "think"], [tf, "shock"]], [(0, "close"), (tf, "wide")])
j += (f'    tl.to("#c8-move", {{ y: -300, duration: 0.26, ease: "expo.out" }}, {tf:.2f});\n'
      f'    tl.to("#c8-move", {{ y: 0, duration: 0.45, ease: "bounce.out" }}, {tf + 0.26:.2f});\n')
rain = "".join(cube(f"s8-g{n}", 100, "gold_block", None, x, -120) for n, x in enumerate((140, 360, 560, 760, 950)))
html = (f'    <div class="c h" id="s8-a" style="top:260px;font-size:84px;opacity:0;">The best part?</div>\n'
        f'    <div class="c s" id="s8-b" style="top:420px;font-size:66px;opacity:0;">Start for</div>\n'
        f'    <div class="c h gold" id="s8-c" style="top:480px;font-size:330px;opacity:0;">FREE</div>\n' + rain + h)
js = j + pop("#s8-a", 0.05, "y: 40, opacity: 0") + pop("#s8-b", max(0.1, tf - 0.5), "y: 40, opacity: 0") + pop("#s8-c", tf, "scale: 3, opacity: 0", 0.35, "expo.out")
for n in range(5):
    js += (f'    gsap.set("#s8-g{n}", {{ rotationX: -30 }});\n'
           f'    tl.fromTo("#s8-g{n}", {{ rotationY: {20 * n} }}, {{ rotationY: {20 * n + 400}, duration: {d:.2f}, ease: "none" }}, 0);\n'
           f'    tl.fromTo("#s8-g{n}-o", {{ y: 0 }}, {{ y: {1400 + 140 * (n % 3)}, duration: {1.2 + 0.15 * (n % 2):.2f}, ease: "power2.in", immediateRender: false }}, {tf + 0.05 * n:.2f});\n')
js += out("#s8-a", tf - 0.1) + "".join(out(s, d - 0.25) for s in ("#s8-b", "#s8-c"))
POP.append(W[k][0] + tf)
C[k] = comp(k, f"<style>{cc}</style>\n" + html, js)

# 9 CTA, then back to the frame-0 layout for the seam ("...because if you still" -> "Need a ...")
i, k = 8, "s9"; d = d_of(i)
tb_ = word_at(i, "because", 1.6)
h, j, cc = character("c9", d, [[0, "wave"], [tb_, "idle"]], [(0, "close"), (tb_, "wide")])
html = (f'    <div id="s9-logo" style="position:absolute;left:415px;top:200px;width:250px;height:250px;border-radius:50%;overflow:hidden;box-shadow:0 0 80px rgba(247,210,122,0.5);opacity:0;">'
        f'<img src="assets/img/logo_circle.png" style="width:250px;height:250px;" alt="Heaven Developer logo"></div>\n'
        f'    <div class="c" id="s9-b" style="top:520px;opacity:0;"><span class="btn"><svg viewBox="0 0 24 24" style="width:72px;height:72px;" fill="#fff">{DISCORD}</svg>Join on Discord</span></div>\n'
        f'    <div class="c s" id="s9-u" style="top:700px;font-size:54px;opacity:0;">discord.gg/<span class="gold">heavendeveloper</span></div>\n'
        f'    <div class="c h" id="s9-n" style="top:250px;font-size:96px;opacity:0;">Need a</div>\n' + h)
js = (j + f'    tl.fromTo("#s9-logo", {{ rotationY: -360, scale: 0.4, opacity: 0 }}, {{ rotationY: 0, scale: 1, opacity: 1, duration: 0.6, ease: "expo.out" }}, 0.05);\n'
      + pop("#s9-b", word_at(i, "join", 0.3)) + pop("#s9-u", word_at(i, "discord", 0.8), "y: 40, opacity: 0")
      + "".join(out(s, d - 0.75) for s in ("#s9-logo", "#s9-b", "#s9-u"))
      + f'    tl.fromTo("#s9-n", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "power2.out" }}, {d - 0.5:.2f});\n')
POP.append(W[k][0] + word_at(i, "join", 0.3))
C[k] = comp(k, f"<style>{cc}</style>\n" + html, js)

# word-timed captions (3-4 words per group, the spoken word highlighted), above the bottom 420 px
groups, cur = [], []
for w, s, e in WORDS:
    cur.append((w.strip(), s, e))
    if len(cur) == 3 or w.strip().endswith((".", "?", ",")):
        groups.append(cur); cur = []
if cur:
    groups.append(cur)
cap_html, cap_js = "", ""
for g, ws in enumerate(groups):
    g0, g1 = ws[0][1], ws[-1][2]
    nxt = groups[g + 1][0][1] if g + 1 < len(groups) else TOTAL - 0.05
    cap_html += f'    <div class="cap" id="cp{g}" style="opacity:0;">' + "".join(f'<span id="cp{g}w{n}">{w}</span>' for n, (w, _, _) in enumerate(ws)) + "</div>\n"
    cap_js += f'    tl.fromTo("#cp{g}", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.12, immediateRender: false }}, {g0 - 0.05:.2f});\n'
    for n, (w, s, e) in enumerate(ws):
        cap_js += f'    tl.fromTo("#cp{g}w{n}", {{ color: "{T["capink"]}" }}, {{ color: "{T["hl"]}", duration: 0.05, immediateRender: false }}, {s:.2f});\n'
    cap_js += f'    tl.to("#cp{g}", {{ opacity: 0, duration: 0.08 }}, {min(nxt - 0.06, g1 + 0.35):.2f});\n'
C["cap"] = comp("cap", cap_html, cap_js)

os.makedirs("compositions", exist_ok=True)
for f in os.listdir("compositions"):
    os.remove(os.path.join("compositions", f))
for kk, v in C.items():
    open(f"compositions/{kk}.html", "w").write(v)
div = lambda kk, s, d_, lane, z: (f'      <div id="{kk}" data-composition-id="{kk}" data-composition-src="compositions/{kk}.html" data-start="{s}" data-duration="{d_}" '
                                  f'data-track-index="{lane}" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: {z}"></div>')
divs = [div("bg", 0, TOTAL, 0, 0)] + [div(kk, s, round(e - s, 3), 1, 1) for kk, s, e in SCENES] + [div("cap", 0, TOTAL, 2, 2)]
sfx = lambda n: f"assets/sfx/{n}.mp3"
A = [("mix", "assets/audio/mix.wav", 0, TOTAL, 1.0, 10)]
POPS = ["pop-high", "bubble-pop", "plop"]                     # rotate variants (Mr Aloo feedback: one repeated pop sounds cheap)
for n, t in enumerate(sorted(POP)):
    f = POPS[n % 3]
    A.append((f"p{n}", sfx(f), round(t, 2), dur(sfx(f)), 0.35, 20 + n % 6))
for n, t in enumerate(sorted(WH)):
    f = ["swish-4", "whoosh-fast-0.3s"][n % 2]
    A.append((f"w{n}", sfx(f), round(max(0, t - 0.1), 2), dur(sfx(f)), 0.4, 30 + n % 2))
aud = "\n".join(f'      <audio id="{a}" src="{s}" data-start="{b}" data-duration="{min(dd, round(TOTAL - b, 3))}" data-volume="{v}" data-track-index="{ln}"></audio>'
                for a, s, b, dd, v, ln in A)
open("index.html", "w").write(f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap-3.14.2.min.js"></script>
    <style>* {{ margin: 0; padding: 0; box-sizing: border-box; }} html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: {T['bg']}; }}</style>
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
print("built", THEME, TOTAL, len(SCENES), "scenes,", len(groups), "caption groups,", len(POP), "pops")
