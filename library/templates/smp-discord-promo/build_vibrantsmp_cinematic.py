# Vibrant SMP CINEMATIC videos (16:9 1920x1080, 2026-11-09). Owner: "drive k folder me new video daaldi hai in game walii
# ... ussi ko and store ki information ko use ker k ek cenematic video ... voice k lie ellavenlabs ... ek or video bhi
# banao cenematic horror type video soo final me tum 2 videos doge".
#   MODE=trailer|horror python3 build_vibrantsmp_cinematic.py      (inside the project folder; needs assets/ig.mp4)
# Footage: the owner's in-game spawn flythrough (Drive 1__MoXI44-tjFb6660mAKm6otrn6A2d1S, 1280x720 60 fps, 128 s; the
# replay-editor UI before 8 s and after 112 s is never used; leaderboard boards with player names are not used).
# What is on screen comes from that footage (signs CRATES / AUCTION / RTP / RANKS / LEADER, crate names) and the store
# (free to play, Java + Bedrock, ranks Deadly / Legend, play.vibrantsmp.fun, discord.gg/W7zqUp2kbM). VO: ElevenLabs;
# word stamps: ElevenLabs Scribe (assets/words_<mode>.json).
import json, os, subprocess

MODE = os.environ.get("MODE", "trailer")
WORDS = json.load(open(f"assets/words_{MODE}.json"))
O = 1.2 if MODE == "trailer" else 1.5           # where the VO starts


def w(word, n=1):
    k = 0
    for x, s, e in WORDS:
        if x.lower().strip(".,?!") == word.lower():
            k += 1
            if k == n:
                return round(s + O, 2)
    raise KeyError(word)


# shots: (out start, source second, speed); each runs to the next shot's start
if MODE == "trailer":
    TOTAL = 34.0
    SH = [(0.0, 8.0, 0.8), (w("one") - 0.1, 10.0, 0.9), (w("Vibrant") - 0.1, 16.0, 0.8), (w("Open") - 0.1, 20.0, 1.0),
          (w("Vote") - 0.05, 24.0, 1.0), (w("Rare") - 0.05, 28.0, 1.0), (w("Epic") - 0.05, 30.0, 1.0), (w("Spawner") - 0.05, 32.0, 1.0),
          (w("Trade") - 0.1, 40.0, 1.0), (w("Jump") - 0.1, 48.0, 1.0), (w("Climb") - 0.1, 83.0, 0.9), (w("deadly") - 0.1, 87.5, 1.0),
          (w("carve") - 0.1, 100.5, 0.9), (w("Free") - 0.1, 97.5, 0.9), (w("Vibrant", 2) - 0.1, 38.0, 0.8), (w("Your", 2) - 0.1, 9.0, 0.5)]
else:
    TOTAL = 28.0
    SH = [(0.0, 8.0, 0.5), (w("They", 2) - 0.1, 20.0, 0.5), (w("But") - 0.1, 26.0, 0.5), (w("another") - 0.1, 33.0, 0.5),
          (w("auction") - 0.2, 41.0, 0.5), (w("leaderboards") - 0.2, 101.0, 0.5), (w("once") - 0.2, 48.0, 0.5),
          (w("there") - 0.2, 50.5, 0.5), (w("Vibrant") - 0.3, 9.0, 0.4)]
SH = [(round(s, 2), src, sp) for s, src, sp in SH]
END = [s for s, _, _ in SH[1:]] + [TOTAL]


def make_bg():
    """cut the shots from the source (60 fps; 0.5x = a clean 30 fps slow-mo) and join them into assets/bg.mp4"""
    os.makedirs("assets/shots", exist_ok=True)
    lst = []
    for n, ((s, src, sp), e) in enumerate(zip(SH, END)):
        d = e - s
        p = f"assets/shots/{MODE}_{n:02d}.mp4"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(src), "-t", f"{d * sp + 0.1:.3f}", "-i", "assets/ig.mp4", "-an",
                        "-vf", f"setpts=PTS/{sp},scale=1920:1080:flags=lanczos,fps=30,trim=0:{d:.3f},setpts=PTS-STARTPTS",
                        "-c:v", "libx264", "-crf", "16", "-preset", "fast", "-pix_fmt", "yuv420p", p], check=True)
        lst.append(f"file '{os.path.abspath(p)}'")
    open("assets/shots/list.txt", "w").write("\n".join(lst) + "\n")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "assets/shots/list.txt", "-c", "copy", "assets/bg.mp4"], check=True)


def dur(p):
    return round(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                      capture_output=True, text=True).stdout), 3)


HOR = MODE == "horror"
ACC = "#c08bff" if not HOR else "#ff2a3c"
CSS = f"""
    @font-face {{ font-family: "BB"; src: url("assets/fonts/BebasNeue-Regular.ttf"); }}
    @font-face {{ font-family: "GL"; src: url("assets/fonts/Gloock-Regular.ttf"); }}
    @font-face {{ font-family: "PB"; src: url("assets/fonts/Poppins-Bold.ttf"); font-weight: 700; }}
    #root {{ position: absolute; inset: 0; overflow: hidden; }}
    .c {{ position: absolute; left: 0; right: 0; text-align: center; }}
    .t {{ font-family: {"GL" if HOR else "BB"}; color: #fff; letter-spacing: {"6px" if HOR else "18px"}; text-transform: uppercase;
          text-shadow: 0 0 30px rgba(0,0,0,0.9), 0 0 80px {ACC}55; }}
    .s {{ font-family: PB; font-weight: 700; color: #e8e0ff; letter-spacing: 8px; text-transform: uppercase; text-shadow: 0 2px 18px rgba(0,0,0,0.95); }}
    .ip {{ display: inline-block; font-family: PB; font-weight: 700; color: #fff; border: 3px solid {ACC}; border-radius: 14px;
           padding: 12px 30px; font-size: 44px; background: rgba(0,0,0,0.55); }}
"""
BAR = 140 if not HOR else 120   # letterbox (2.39:1 ~ 138 px at 1080p)


def comp(cid, html, js, d):
    return f"""<template>
  <style>{CSS}</style>
  <div id="root" data-composition-id="{cid}" data-width="1920" data-height="1080" data-layout-allow-overflow>
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


# camera: the background video inside a wrapper that pushes in on every shot (and drifts sideways in horror)
cam_js = ""
for n, ((s, _, _), e) in enumerate(zip(SH, END)):
    z0, z1 = (1.0, 1.08) if not HOR else (1.04, 1.14)
    dx = 0 if not HOR else (-30 if n % 2 else 30)
    cam_js += f'    tl.fromTo("#camw", {{ scale: {z0}, x: 0 }}, {{ scale: {z1}, x: {dx}, duration: {e - s:.3f}, ease: "none", immediateRender: {"true" if n == 0 else "false"} }}, {s:.3f});\n'
cam = comp("cam", f'    <div id="camw" style="position:absolute;inset:0;transform-origin:50% 50%;">'
                  f'<video id="bgv" src="assets/bg.mp4" muted playsinline data-start="0" data-duration="{TOTAL}" data-track-index="0" '
                  'style="position:absolute;inset:0;width:1920px;height:1080px;object-fit:cover;"></video></div>', cam_js, TOTAL)

T = []   # (start, end, html, extra_js)
if not HOR:
    T += [(w("world") - 0.2, w("one") - 0.3, '<div class="c t" style="top:470px;font-size:120px;">BLOCK BY BLOCK</div>', ""),
          (w("Vibrant") - 0.05, w("Open") - 0.2, '<div style="position:absolute;left:810px;top:230px;width:300px;height:300px;"><img src="assets/img/vlogo.png" style="width:300px;" alt="Vibrant SMP logo"></div>'
                                                  f'<div class="c t" style="top:560px;font-size:150px;">VIBRANT <span style="color:{ACC};">SMP</span></div>', ""),
          (w("Open") - 0.05, w("Vote") - 0.1, '<div class="c t" style="top:780px;font-size:90px;">OPEN THE CRATES</div>', "")]
    for word, label in (("Vote", "VOTE CRATE"), ("Rare", "RARE CRATE"), ("Epic", "EPIC CRATE"), ("Spawner", "SPAWNER CRATE")):
        T.append((w(word) - 0.05, w(word) + 0.75, f'<div class="c t" style="top:800px;font-size:80px;">{label}</div>', ""))
    T += [(w("Trade") - 0.05, w("Jump") - 0.2, '<div class="c t" style="top:800px;font-size:90px;">AUCTION HOUSE</div>', ""),
          (w("RTP") - 0.1, w("Climb") - 0.2, '<div class="c t" style="top:800px;font-size:110px;">RTP</div>', ""),
          (w("deadly") - 0.05, w("carve") - 0.2, f'<div class="c t" style="top:780px;font-size:96px;">DEADLY <span style="color:{ACC};">&#8594;</span> LEGEND</div>', ""),
          (w("leaderboards") - 0.1, w("Free") - 0.2, '<div class="c t" style="top:800px;font-size:90px;">LEADERBOARDS</div>', ""),
          (w("Free") - 0.05, w("Vibrant", 2) - 0.2, '<div class="c t" style="top:430px;font-size:120px;">FREE TO PLAY</div><div class="c s" style="top:590px;font-size:44px;">JAVA &amp; BEDROCK</div>', ""),
          (w("Vibrant", 2) - 0.05, w("Your", 2) - 0.15, f'<div class="c t" style="top:440px;font-size:170px;">VIBRANT <span style="color:{ACC};">SMP</span></div>', ""),
          (w("Your", 2) - 0.05, TOTAL, '<div style="position:absolute;inset:0;background:rgba(0,0,0,0.55);"></div>'
                                    '<div style="position:absolute;left:835px;top:170px;width:250px;"><img src="assets/img/vlogo.png" style="width:250px;" alt="Vibrant SMP logo"></div>'
                                    '<div class="c t" style="top:440px;font-size:96px;">YOUR LEGEND STARTS NOW</div>'
                                    '<div class="c" style="top:600px;"><span class="ip">play.vibrantsmp.fun</span></div>'
                                    '<div class="c s" style="top:720px;font-size:30px;">JAVA &amp; BEDROCK &#183; PORT 62222</div>'
                                    '<div class="c" style="top:790px;"><span class="ip" style="border-color:#5865f2;font-size:36px;">discord.gg/W7zqUp2kbM</span></div>', "")]
else:
    T += [(w("They") - 0.1, w("They", 2) - 0.3, '<div class="c t" style="top:780px;font-size:70px;">THE SPAWN WAS SAFE.</div>', ""),
          (w("crates") - 0.1, w("But") - 0.3, '<div class="c t" style="top:780px;font-size:70px;">THE CRATES...</div>', ""),
          (w("night") - 0.1, w("another") - 0.2, f'<div class="c t" style="top:780px;font-size:70px;color:{ACC};">EVERY NIGHT</div>', ""),
          (w("missing") - 0.1, w("auction") - 0.3, '<div class="c t" style="top:780px;font-size:70px;">ANOTHER KEY GOES MISSING</div>', ""),
          (w("watching") - 0.1, w("once") - 0.3, f'<div class="c t" style="top:780px;font-size:70px;">THEY ARE <span style="color:{ACC};">WATCHING</span></div>', ""),
          (w("back") - 0.4, w("Vibrant") - 0.4, '<div class="c t" style="top:780px;font-size:76px;">NO GOING BACK</div>', ""),
          (w("Vibrant") - 0.1, TOTAL, '<div style="position:absolute;inset:0;background:rgba(0,0,0,0.6);"></div>'
                                      '<div id="hl" style="position:absolute;left:810px;top:150px;width:300px;"><img src="assets/img/vlogo.png" style="width:300px;filter:hue-rotate(95deg) saturate(1.6) brightness(0.8);" alt="Vibrant SMP logo"></div>'
                                      f'<div class="c t" style="top:470px;font-size:140px;">VIBRANT <span style="color:{ACC};">SMP</span></div>'
                                      '<div class="c t" id="hd" style="top:650px;font-size:64px;opacity:0;">JOIN... IF YOU DARE</div>'
                                      '<div class="c" id="hi" style="top:780px;opacity:0;"><span class="ip">play.vibrantsmp.fun</span></div>',
           f'    tl.to("#hd", {{ opacity: 1, duration: 0.6 }}, {w("Join") - (w("Vibrant") - 0.1):.2f});\n'
           f'    tl.to("#hi", {{ opacity: 1, duration: 0.8 }}, {w("dare") + 0.6 - (w("Vibrant") - 0.1):.2f});\n'
           '    tl.fromTo("#hl", { opacity: 0.3 }, { opacity: 1, duration: 0.07, repeat: 9, yoyo: true, ease: "steps(1)" }, 0.1);\n')]

titles = ""
for n, (s, e, html, xj) in enumerate(T):
    d = round(e - s, 2)
    fade_in = 0.5 if not HOR else 0.9
    js = (f'    tl.fromTo("#tw{n}", {{ opacity: 0, scale: {1.06 if not HOR else 1.0}, filter: "blur(10px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: {min(fade_in, d / 2):.2f}, ease: "power2.out" }}, 0);\n'
          + (f'    tl.to("#tw{n}", {{ opacity: 0, duration: 0.25 }}, {d - 0.25:.2f});\n' if e < TOTAL else "") + xj)
    titles += f'      <div id="t{n}" data-composition-id="t{n}" data-composition-src="compositions/t{n}.html" data-start="{s}" data-duration="{d}" data-track-index="{2 + n % 2}" data-track-kind="graphics" data-width="1920" data-height="1080" style="z-index: 3"></div>\n'
    open_c = comp(f"t{n}", f'    <div id="tw{n}" style="position:absolute;inset:0;">{html}</div>', js, d)
    T[n] = (s, e, open_c, "")

# overlays: letterbox, flash on cuts (trailer) / flicker (horror)
ov_js = f'    gsap.set("#bt", {{ y: 0 }}); gsap.set("#bb", {{ y: 0 }});\n'
if not HOR:
    ov_js += "".join(f'    tl.fromTo("#fl", {{ opacity: {0.55 if s in (w("Vibrant") - 0.1, w("Climb") - 0.1, w("Vibrant", 2) - 0.1) else 0.18} }}, {{ opacity: 0, duration: 0.18, ease: "power2.out", immediateRender: false }}, {s:.2f});\n' for s, _, _ in SH[1:])
else:
    import random
    rnd = random.Random(9)
    fl = sorted(set([round(rnd.uniform(0.5, TOTAL - 1), 2) for _ in range(14)] + [w("once") - 0.2, w("there") - 0.2]))
    ov_js += "".join(f'    tl.fromTo("#dk", {{ opacity: {rnd.choice((0.55, 0.75, 0.9))} }}, {{ opacity: 0, duration: {rnd.choice((0.06, 0.1, 0.16))}, ease: "steps(2)", immediateRender: false }}, {t:.2f});\n' for t in fl)
    ov_js += f'    tl.fromTo("#fl", {{ opacity: 0.7 }}, {{ opacity: 0, duration: 0.25, immediateRender: false }}, {w("Vibrant") - 0.3:.2f});\n'
ov = comp("ov", f'    <div id="fl" style="position:absolute;inset:0;background:{"#fff" if not HOR else "#5a0008"};opacity:0;"></div>\n'
                '    <div id="dk" style="position:absolute;inset:0;background:#000;opacity:0;"></div>\n'
                f'    <div id="bt" style="position:absolute;left:0;right:0;top:0;height:{BAR}px;background:#000;"></div>\n'
                f'    <div id="bb" style="position:absolute;left:0;right:0;bottom:0;height:{BAR}px;background:#000;"></div>', ov_js, TOTAL)

if __name__ == "__main__":
    if not os.path.exists("assets/bg.mp4") or os.environ.get("REBUILD_BG"):
        make_bg()
    os.makedirs("compositions", exist_ok=True)
    for f in os.listdir("compositions"):
        os.remove(os.path.join("compositions", f))
    open("compositions/cam.html", "w").write(cam)
    open("compositions/ov.html", "w").write(ov)
    for n, (_, _, c, _) in enumerate(T):
        open(f"compositions/t{n}.html", "w").write(c)
    sfx = lambda n: f"assets/sfx/{n}.mp3"
    A = [("mix", "assets/audio/mix.wav", 0, TOTAL, 1.0, 10)]
    if not HOR:
        for n, t in enumerate([w("Vibrant") - 0.1, w("Climb") - 0.1, w("Vibrant", 2) - 0.1]):
            A.append((f"b{n}", sfx(["impact-boom", "sub-drop", "impact-boom"][n]), t, dur(sfx(["impact-boom", "sub-drop", "impact-boom"][n])), 0.55, 20 + n))
        for n, (s, _, _) in enumerate(SH[1:]):
            if s not in (w("Vibrant") - 0.1, w("Climb") - 0.1, w("Vibrant", 2) - 0.1):
                A.append((f"wh{n}", sfx(["whoosh-fast-0.3s", "swish-4"][n % 2]), round(max(0, s - 0.12), 2), dur(sfx(["whoosh-fast-0.3s", "swish-4"][n % 2])), 0.3, 30 + n % 3))
        A.append(("ris", sfx("riser-2s"), round(w("Climb") - 0.1 - 1.698, 2), dur(sfx("riser-2s")), 0.45, 40))
    else:
        A += [("hb", sfx("heartbeat"), 0.2, dur(sfx("heartbeat")), 0.7, 20), ("hb2", sfx("heartbeat"), round(w("watching"), 2), dur(sfx("heartbeat")), 0.7, 21),
              ("st", sfx("static-noise"), round(w("once") - 0.2, 2), 0.6, 0.35, 22), ("gl", sfx("glitch-short"), round(w("there") - 0.2, 2), dur(sfx("glitch-short")), 0.6, 23),
              ("ris", sfx("riser-2s"), round(w("Vibrant") - 0.3 - 1.698, 2), dur(sfx("riser-2s")), 0.5, 24),
              ("sd", sfx("sub-drop"), round(w("Vibrant") - 0.3, 2), dur(sfx("sub-drop")), 0.7, 25)]
    aud = "\n".join(f'      <audio id="{a}" src="{s}" data-start="{b}" data-duration="{min(dd, round(TOTAL - b, 3))}" data-volume="{v}" data-track-index="{ln}"></audio>'
                    for a, s, b, dd, v, ln in A)
    open("index.html", "w").write(f"""<!doctype html>
<html lang="en" data-resolution="landscape">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="assets/vendor/gsap-3.14.2.min.js"></script>
    <style>* {{ margin: 0; padding: 0; box-sizing: border-box; }} html, body {{ margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: #000; }}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1920" data-height="1080">
      <div id="cam" data-composition-id="cam" data-composition-src="compositions/cam.html" data-start="0" data-duration="{TOTAL}" data-track-index="0" data-track-kind="graphics" data-width="1920" data-height="1080" style="z-index: 0"></div>
{titles}      <div id="ov" data-composition-id="ov" data-composition-src="compositions/ov.html" data-start="0" data-duration="{TOTAL}" data-track-index="5" data-track-kind="graphics" data-width="1920" data-height="1080" style="z-index: 5"></div>
{aud}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
""")
    print("built", MODE, TOTAL, len(SH), "shots,", len(T), "titles")
