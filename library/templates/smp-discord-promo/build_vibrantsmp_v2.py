# Vibrant SMP promo v2 (9:16, 27.7 s, 2026-11-07): owner asked to add the store (https://store.vibrantsmp.fun, read
# 2026-11-07: free-to-play, Java + Bedrock, Ranks / Crate Keys / Player Tags / Coins, buy via Discord ticket, 4 vote sites,
# its 3D V logo) and to use ElevenLabs for the voice AND the transcription (Scribe word stamps time the text).
# v1 header: Owner: "Ye recording lelo and isse sari information le ker in k lie ek
# promotional video banado ... voices elavenlabbs ... under 40 minutes ... gameplay video ... serf as a background".
#   python3 build_vibrantsmp.py        (run inside the project folder)
# If assets/gameplay.mp4 exists it becomes the full-frame background (muted, darkened); otherwise an animated purple
# backdrop stands in, so the same build re-runs as soon as the owner's gameplay clip arrives.
# Facts = frames of the owner's phone recording of the Vibrant SMP Discord (Drive 1Wk6iASytIJvjeOpAewmc4duG-LR7cEO4, read
# 2026-11-07): Survival Multiplayer, "premium vibes", economy (MOTD "Survival | Economy"), Java IP play.vibrantsmp.fun:62222,
# Bedrock amd.titannode.fun:19133 (#announcements), Leaf 1.21.11, 246 slots, channels giveaways/events/builds/trading,
# roles Media / Streamers / Clippers, #create-ticket. VO: ElevenLabs (owner asked), timed by Whisper word stamps.
import json, os, subprocess

TOTAL = 27.7
VO = 0.3
WORDS = [(w, s + VO, e + VO) for w, s, e in json.load(open("assets/words.json"))]
EV = json.load(open("assets/music/events.json"))
KICKS = []
for t, s in EV["kicks"]:
    if s >= 0.4 and t < TOTAL - 1 and (not KICKS or t - KICKS[-1] >= 0.35):
        KICKS.append(t)
PUR, PINK, GOLD, WHITE = "#a64dff", "#ff4fd8", "#ffd45a", "#ffffff"
BGV = os.path.exists("assets/gameplay.mp4")


def w(word, n=1):
    """absolute start of the n-th spoken occurrence of `word`"""
    k = 0
    for x, s, e in WORDS:
        if word.lower() in x.lower():
            k += 1
            if k == n:
                return round(s, 2)
    raise KeyError(word)


def dur(p):
    return round(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                      capture_output=True, text=True).stdout), 3)


CUTS = [0.0, w("Welcome") - 0.1, w("free-to-play") - 0.2, w("Join") - 0.1, w("Want") - 0.1, w("Vote") - 0.1, w("Join", 2) - 0.1, TOTAL]
SC = [(f"s{i + 1}", CUTS[i], CUTS[i + 1]) for i in range(len(CUTS) - 1)]
W = {k: (s, e) for k, s, e in SC}

CSS = f"""
    @font-face {{ font-family: "AN"; src: url("assets/fonts/Anton-Regular.ttf"); }}
    @font-face {{ font-family: "PX"; src: url("assets/fonts/Poppins-ExtraBold.ttf"); font-weight: 800; }}
    @font-face {{ font-family: "PB"; src: url("assets/fonts/Poppins-Bold.ttf"); font-weight: 700; }}
    #root {{ position: absolute; inset: 0; overflow: hidden; }}
    .c {{ position: absolute; left: 0; right: 0; text-align: center; }}
    .big {{ font-family: AN; text-transform: uppercase; line-height: 0.95; color: {WHITE};
            text-shadow: -4px 0 0 rgba(255,79,216,0.75), 4px 0 0 rgba(90,200,255,0.75), 0 10px 40px rgba(0,0,0,0.9); }}
    .sub {{ font-family: PB; font-weight: 700; color: {GOLD}; text-shadow: 0 4px 20px rgba(0,0,0,0.95); }}
    .chip {{ display: inline-block; font-family: PX; font-weight: 800; font-size: 54px; color: #fff; background: rgba(30,10,50,0.85);
             border: 4px solid {PUR}; border-radius: 999px; padding: 12px 38px; margin: 10px; box-shadow: 0 0 40px rgba(166,77,255,0.55); }}
    .card {{ position: absolute; border-radius: 30px; overflow: hidden; background: #fff; box-shadow: 0 30px 80px rgba(0,0,0,0.7), 0 0 0 4px rgba(166,77,255,0.7); }}
    .card img {{ display: block; width: 100%; }}
    .ip {{ display: inline-block; font-family: PX; font-weight: 800; color: #fff; background: rgba(20,6,36,0.9); border: 4px solid {GOLD};
           border-radius: 26px; padding: 16px 34px; font-size: 56px; }}
"""


def comp(cid, html, js, d):
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


def slam(sel, t, frm="scale: 2.4, opacity: 0", d=0.22):
    return f'    tl.fromTo("{sel}", {{ {frm} }}, {{ scale: 1, x: 0, y: 0, rotation: 0, opacity: 1, duration: {d}, ease: "power4.out" }}, {t:.2f});\n'


def shake(sel, t):
    return f'    tl.fromTo("{sel}", {{ x: -10, y: 6 }}, {{ x: 8, y: -4, duration: 0.045, ease: "none", repeat: 4, yoyo: true, immediateRender: false }}, {t:.2f});\n'


C, HITS, POPS = {}, [], []


def scene(k, html, js):
    s, e = W[k]
    d = round(e - s, 3)
    js += "".join(f'    tl.fromTo("#{k}-w", {{ scale: 1.06 }}, {{ scale: 1, duration: 0.22, ease: "expo.out", immediateRender: false }}, {t - s:.3f});\n'
                  for t in KICKS if s + 0.1 < t < e - 0.2)
    if k != "s7":
        js += f'    tl.to("#{k}-w", {{ scale: 1.25, opacity: 0, filter: "blur(12px)", duration: 0.14, ease: "power3.in" }}, {d - 0.14:.2f});\n'
    C[k] = comp(k, f'    <div id="{k}-w" style="position:absolute;inset:0;transform-origin:50% 45%;">\n{html}\n    </div>', js, d)


r = lambda k, t: round(t - W[k][0], 2)
# background: the owner's gameplay (when uploaded) or an animated purple backdrop
if BGV:
    bg_html = (f'    <video id="bgv" src="assets/gameplay.mp4" muted playsinline data-start="0" data-duration="{TOTAL}" data-track-index="0" '
               'style="position:absolute;inset:0;width:1080px;height:1920px;object-fit:cover;"></video>\n'
               '    <div style="position:absolute;inset:0;background:linear-gradient(180deg, rgba(10,0,25,0.45), rgba(10,0,25,0.22) 40%, rgba(10,0,25,0.6));"></div>')
    bg_js = ""
else:
    bg_html = ('    <div style="position:absolute;inset:0;background:#0b0418;"></div>\n'
               '    <div id="g1" style="position:absolute;left:-300px;top:150px;width:1200px;height:1200px;border-radius:50%;background:radial-gradient(circle, rgba(166,77,255,0.45), rgba(0,0,0,0) 70%);"></div>\n'
               '    <div id="g2" style="position:absolute;left:350px;top:950px;width:1100px;height:1100px;border-radius:50%;background:radial-gradient(circle, rgba(255,79,216,0.25), rgba(0,0,0,0) 70%);"></div>\n'
               '    <div style="position:absolute;inset:0;background-image:linear-gradient(rgba(166,77,255,0.12) 2px, transparent 2px),linear-gradient(90deg, rgba(166,77,255,0.12) 2px, transparent 2px);background-size:110px 110px;"></div>')
    bg_js = (f'    tl.fromTo("#g1", {{ x: 0 }}, {{ x: 480, duration: {TOTAL}, ease: "sine.inOut" }}, 0);\n'
             f'    tl.fromTo("#g2", {{ x: 0 }}, {{ x: -520, duration: {TOTAL}, ease: "sine.inOut" }}, 0);\n')
C["bg"] = comp("bg", bg_html, bg_js, TOTAL)
C["fl"] = comp("fl", '    <div id="fl" style="position:absolute;inset:0;background:#fff;opacity:0;"></div>',
               "".join(f'    tl.fromTo("#fl", {{ opacity: 0.85 }}, {{ opacity: 0, duration: 0.12, ease: "power2.out", immediateRender: false }}, {max(0.01, s - 0.03):.2f});\n'
                       for _, s, _ in SC[1:]), TOTAL)

LOGO = '<img src="assets/img/vlogo.png" style="width:100%;height:100%;filter:drop-shadow(0 0 40px rgba(166,77,255,0.9));" alt="Vibrant SMP logo">'
k = "s1"   # hook (on screen at 0 s)
scene(k, f'    <div class="c sub" id="s1-f" style="top:430px;font-size:80px;color:{GOLD};">A FREE</div>\n'
         '    <div class="c big" id="s1-a" style="top:520px;font-size:150px;">MINECRAFT<br>SERVER</div>\n'
         '    <div class="c sub" id="s1-b" style="top:860px;font-size:70px;opacity:0;">with REAL</div>\n'
         f'    <div class="c big" id="s1-c" style="top:950px;font-size:180px;color:{PINK};opacity:0;">PREMIUM VIBES?</div>',
      slam("#s1-f", 0.0, "scale: 1, opacity: 1") + slam("#s1-a", 0.0, "scale: 1, opacity: 1") + slam("#s1-b", r(k, w("real")), "y: 40, opacity: 0")
      + slam("#s1-c", r(k, w("premium"))) + shake("#s1-w", r(k, w("premium"))))
HITS.append(w("premium"))

k = "s2"   # brand: the store's 3D V logo
scene(k, f'    <div id="s2-l" style="position:absolute;left:240px;top:240px;width:600px;height:600px;opacity:0;">{LOGO}</div>\n'
         '    <div class="c sub" id="s2-a" style="top:860px;font-size:70px;opacity:0;">WELCOME TO</div>\n'
         f'    <div class="c big" id="s2-b" style="top:950px;font-size:200px;opacity:0;">VIBRANT <span style="color:{PUR};">SMP</span></div>',
      '    tl.fromTo("#s2-l", { scale: 0.2, rotation: -20, opacity: 0 }, { scale: 1, rotation: 0, opacity: 1, duration: 0.6, ease: "back.out(1.6)" }, 0.03);\n'
      + '    tl.to("#s2-l", { y: -20, duration: 0.8, ease: "sine.inOut", yoyo: true, repeat: 3 }, 0.7);\n'
      + slam("#s2-a", r(k, w("to")), "y: -40, opacity: 0") + slam("#s2-b", r(k, w("Vibrant"))) + shake("#s2-w", r(k, w("Vibrant"))))
HITS.append(w("Vibrant"))

k = "s3"   # free-to-play, survival, economy, Java + Bedrock: the store's "How to join" + the Discord #server-info card
items = [("FREE TO PLAY", "free-to-play"), ("SURVIVAL", "survival"), ("ECONOMY", "economy"), ("JAVA", "Java"), ("BEDROCK", "Bedrock")]
scene(k, '    <div class="card" id="s3-c" style="left:90px;top:200px;width:900px;opacity:0;"><img src="assets/img/serverinfo.jpg" alt=""></div>\n'
         '    <div class="card" id="s3-j" style="left:70px;top:1330px;width:940px;opacity:0;"><img src="assets/img/howjoin.jpg" alt=""></div>\n'
         '    <div class="c" style="top:850px;">' + "".join(f'<span class="chip" id="s3-k{n}" style="opacity:0;">{t}</span>' for n, (t, _) in enumerate(items)) + '</div>',
      slam("#s3-c", 0.05, "y: 200, rotation: -3, opacity: 0", 0.45) + slam("#s3-j", r(k, w("Java")) - 0.1, "y: 200, opacity: 0", 0.4)
      + "".join(slam(f"#s3-k{n}", r(k, w(x)), "scale: 0.3, opacity: 0", 0.3) for n, (_, x) in enumerate(items)))
POPS += [w(x) for _, x in items]

k = "s4"   # community
items = [("GIVEAWAYS", "giveaways"), ("EVENTS", "events"), ("BUILDS", "builds"), ("TRADING", "trade")]
scene(k, '    <div class="c big" id="s4-a" style="top:300px;font-size:130px;">JOIN THE</div>\n'
         f'    <div class="c big" id="s4-b" style="top:430px;font-size:170px;color:{GOLD};">COMMUNITY</div>\n'
         + "".join(f'    <div class="c" id="s4-k{n}" style="top:{760 + n * 150}px;opacity:0;"><span class="chip" style="font-size:72px;">{t}</span></div>\n' for n, (t, _) in enumerate(items)),
      slam("#s4-a", 0.03) + slam("#s4-b", 0.15) + "".join(slam(f"#s4-k{n}", r(k, w(x)), f"x: {-700 if n % 2 == 0 else 700}, opacity: 0", 0.25) + shake("#s4-w", r(k, w(x))) for n, (_, x) in enumerate(items)))
HITS += [w(x) for _, x in items]

k = "s5"   # the official store: its real "Featured Packages" + categories on their words
items = [("RANKS", "ranks"), ("CRATE KEYS", "keys"), ("PLAYER TAGS", "tags"), ("COINS", "coins")]
scene(k, '    <div class="c big" id="s5-a" style="top:150px;font-size:120px;">WANT MORE?</div>\n'
         + '    <div class="c" style="top:300px;">' + "".join(f'<span class="chip" id="s5-k{n}" style="opacity:0;font-size:50px;">{t}</span>' for n, (t, _) in enumerate(items)) + '</div>\n'
         '    <div class="card" id="s5-c" style="left:110px;top:560px;width:860px;opacity:0;background:#0b0713;"><img src="assets/img/packages.jpg" alt=""></div>\n'
         f'    <div class="c sub" id="s5-s" style="top:1180px;font-size:64px;opacity:0;">store.vibrantsmp.fun</div>',
      slam("#s5-a", 0.03) + shake("#s5-w", 0.03) + "".join(slam(f"#s5-k{n}", r(k, w(x)), "scale: 0.3, opacity: 0", 0.28) for n, (_, x) in enumerate(items))
      + slam("#s5-c", r(k, w("Grab")), "y: 260, opacity: 0", 0.45) + slam("#s5-s", r(k, w("official")), "y: 40, opacity: 0"))
POPS += [w(x) for _, x in items]
HITS.append(w("Want"))

k = "s6"   # vote: the four sites listed on the store's Vote page
sites = ["MinecraftServers.org", "Minecraft-MP", "Minecraft.Buzz", "Planet Minecraft"]
scene(k, f'    <div class="c big" id="s6-a" style="top:330px;font-size:200px;color:{GOLD};">VOTE</div>\n'
         '    <div class="c sub" id="s6-b" style="top:560px;font-size:62px;color:#fff;opacity:0;">AND HELP US GROW</div>\n'
         + "".join(f'    <div class="c" id="s6-k{n}" style="top:{700 + n * 135}px;opacity:0;"><span class="chip" style="font-size:52px;">{n + 1}. {s}</span></div>\n' for n, s in enumerate(sites)),
      slam("#s6-a", 0.03) + shake("#s6-w", 0.03) + slam("#s6-b", r(k, w("help")), "y: 40, opacity: 0")
      + "".join(slam(f"#s6-k{n}", 0.25 + 0.22 * n, f"x: {-700 if n % 2 == 0 else 700}, opacity: 0", 0.25) for n in range(4)))
HITS.append(w("Vote"))

k = "s7"   # CTA: one IP for Java + Bedrock (store "How to join"), Java port 62222, the Discord invite from the store
scene(k, f'    <div id="s7-l" style="position:absolute;left:330px;top:120px;width:420px;height:420px;opacity:0;">{LOGO}</div>\n'
         f'    <div class="c big" id="s7-a" style="top:560px;font-size:170px;">JOIN <span style="color:{PUR};">NOW</span></div>\n'
         '    <div class="c sub" id="s7-j" style="top:770px;font-size:46px;color:#fff;opacity:0;">JAVA &amp; BEDROCK</div>\n'
         '    <div class="c" id="s7-ji" style="top:840px;opacity:0;"><span class="ip" style="font-size:70px;">play.vibrantsmp.fun</span></div>\n'
         '    <div class="c sub" id="s7-p" style="top:990px;font-size:50px;opacity:0;">PORT 62222</div>\n'
         '    <div class="c" id="s7-d" style="top:1100px;opacity:0;"><span class="ip" style="border-color:#5865f2;font-size:54px;">discord.gg/W7zqUp2kbM</span></div>',
      '    tl.fromTo("#s7-l", { scale: 0.3, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.5, ease: "back.out(1.7)" }, 0.03);\n'
      + slam("#s7-a", 0.05) + shake("#s7-w", 0.05) + slam("#s7-j", r(k, w("now")), "y: 30, opacity: 0")
      + slam("#s7-ji", r(k, w("play.vibrantsmp.fun")), "scale: 0.4, opacity: 0", 0.3) + slam("#s7-p", r(k, w("play.vibrantsmp.fun")) + 0.5, "y: 30, opacity: 0")
      + slam("#s7-d", r(k, w("play.vibrantsmp.fun")) + 0.9, "y: 60, opacity: 0", 0.3)
      + f'    tl.to("#s7-ji", {{ scale: 1.06, duration: 0.45, ease: "sine.inOut", yoyo: true, repeat: 4 }}, {r(k, w("play.vibrantsmp.fun")) + 0.6:.2f});\n')
HITS.append(w("Join", 2))

os.makedirs("compositions", exist_ok=True)
for f in os.listdir("compositions"):
    os.remove(os.path.join("compositions", f))
for kk, v in C.items():
    open(f"compositions/{kk}.html", "w").write(v)
div = lambda kk, s, d_, lane, z: (f'      <div id="{kk}" data-composition-id="{kk}" data-composition-src="compositions/{kk}.html" data-start="{s}" data-duration="{d_}" '
                                  f'data-track-index="{lane}" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: {z}"></div>')
divs = [div("bg", 0, TOTAL, 0, 0)] + [div(kk, s, round(e - s, 3), 1, 1) for kk, s, e in SC] + [div("fl", 0, TOTAL, 2, 2)]
sfx = lambda n: f"assets/sfx/{n}.mp3"
A = [("mix", "assets/audio/mix.wav", 0, TOTAL, 1.0, 10)]
for n, t in enumerate(sorted(HITS)):
    f = ["impact-boom", "punch-heavy", "sub-drop"][n % 3]
    A.append((f"h{n}", sfx(f), t, dur(sfx(f)), 0.28, 20 + n % 6))
for n, t in enumerate(sorted(POPS)):
    f = ["pop-high", "bubble-pop", "plop"][n % 3]
    A.append((f"p{n}", sfx(f), t, dur(sfx(f)), 0.35, 30 + n % 4))
for n, (_, s, _) in enumerate(SC[1:]):
    f = ["whoosh-fast-0.3s", "swish-4"][n % 2]
    A.append((f"wh{n}", sfx(f), round(max(0, s - 0.1), 2), dur(sfx(f)), 0.45, 40 + n % 2))
aud = "\n".join(f'      <audio id="{a}" src="{s}" data-start="{b}" data-duration="{min(dd, round(TOTAL - b, 3))}" data-volume="{v}" data-track-index="{ln}"></audio>'
                for a, s, b, dd, v, ln in A)
open("index.html", "w").write(f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap-3.14.2.min.js"></script>
    <style>* {{ margin: 0; padding: 0; box-sizing: border-box; }} html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #0b0418; }}</style>
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
print("built", TOTAL, "gameplay bg" if BGV else "purple bg", len(SC), "scenes,", len(KICKS), "kick punches")
