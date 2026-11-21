# Kohinoor promo v3: "cooler video" style (owner 2026-11-21: "Ek cooler wali video ki trah bhi bana do ussi ka music use
# ker k"). Timing copied from the reference's own cut list (watch.py on the reference, 2026-11-21), on its own audio.
# MUSIC EXCEPTION: the audio is the reference TikTok's "original sound" (not CC0). The owner was told the copyright risk
# and still chose it ("Same wahi link wali video ka music use kerlo"). The audio stays in the scratchpad, never in git.
# 9:16, 17.1 s (= the reference audio). Exploded view = a generic piston illustration (owner chose "Piston + rings, bara
# version"): piston, top ring, second ring, oil ring, wrist pin, two pin clips.
#   cd <project>; python3 build_kohinoor_v3.py   (assets/audio/refB_audio.wav = the reference's audio track)
import os, subprocess

WD, HT = 1080, 1920
TOTAL = 17.1
RED = "#e0161f"
# reference cut times (watch.py content cuts) from the beat section, and its end card start
CUTS = [5.2, 5.93, 6.57, 7.27, 7.83, 8.43, 9.73, 10.33, 11.07, 11.7, 12.4, 12.97, 13.67, 14.2, 14.87, 15.47]
EXP0, EXP1 = 2.97, 5.2        # exploded hold, parts slam together on the 4.95 beat
END = 15.47


def run(*a):
    subprocess.run(a, check=True, capture_output=True)


# ---------- footage track (0 .. END); "P" = piston shot (dark blurred engine bed, the piston is drawn in HTML) ----------
# (start, end, clip, source start, x-focus, zoom, look) ; look: "" | "bed" (blurred dark bed for the piston)
SH = [(0.0, 1.37, "65", 1.6, 0.70, 1.0, "dark"), (1.37, EXP0, "4716", 0.5, 0.40, 1.0, "push"),
      (EXP0, EXP1, "65", 4.0, 0.5, 1.0, "bed")]
SEQ = ["P", ("65", 2.0, 0.30, 1.2), ("4716", 6.0, 0.55, 1.0), "P", ("2675", 2.0, 0.47, 1.3), ("41937", 2.0, 0.50, 1.0),
       "P", ("65", 6.5, 0.80, 1.25), ("4716", 3.5, 0.20, 1.0), "P", ("2675", 6.0, 0.55, 1.6), "P", ("44284", 6.0, 0.42, 1.0),
       ("41937", 5.0, 0.30, 1.3), "P"]
PSHOTS = []
for k, item in enumerate(SEQ):
    t0, t1 = CUTS[k], CUTS[k + 1]
    if item == "P":
        SH.append((t0, t1, "65", 3.0 + k * 0.3, 0.5, 1.0, "bed"))
        PSHOTS.append((k, t0, t1))
    else:
        c, a, fx, z = item
        SH.append((t0, t1, c, a, fx, z, ""))
os.makedirs("assets/clips", exist_ok=True)
parts = []
for j, (t0, t1, cid, a, fx, z, look) in enumerate(SH):
    # frame-exact length: per-clip -t rounding lost 0.14 s over 18 clips, so footage cut before the HTML piston layer
    # and left 2-4 near-black frames (blackdetect 9.67 s and 12.87 s, first render 2026-11-21)
    nf = round(t1 * 30) - round(t0 * 30)
    d = round(nf / 30, 4)
    cw = int(1214 / z) // 2 * 2
    ch = int(2160 / z) // 2 * 2
    vf = f"fps=30,crop={cw}:{ch}:{int((3840 - cw) * fx)}:{(2160 - ch) // 2},scale={WD}:{HT}:flags=lanczos,eq=contrast=1.22:saturation=0.85"
    if look == "dark":
        vf += ",eq=brightness=-0.28"
    if look == "bed":
        vf += ",boxblur=22:2,eq=brightness=-0.22:saturation=0.5"
    if look == "push":
        vf += f",scale=w='trunc({WD}*(1+0.12*t/{d})/2)*2':h=-2:eval=frame,crop={WD}:{HT}"
    vf += f",setpts=PTS-STARTPTS,tpad=stop_mode=clone:stop_duration={d + 1},fps=30,format=yuv420p"   # trim by -frames:v
    out = f"assets/clips/v3_{j:02d}.mp4"
    run("ffmpeg", "-y", "-ss", str(a), "-t", str(d + 0.5), "-i", f"assets/stock/mk_{cid}.mp4", "-an", "-vf", vf,
        "-frames:v", str(nf), "-fps_mode", "cfr", "-c:v", "libx264", "-crf", "16", "-r", "30", out)
    parts.append(out)
open("assets/clips/list3.txt", "w").write("".join(f"file '{os.path.basename(p)}'\n" for p in parts))
run("ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "assets/clips/list3.txt", "-c", "copy", "assets/v3.mp4")
# reference audio is very loud (-5.5 LUFS integrated, measured): bring it to -14 LUFS with a -1 dBTP ceiling
run("ffmpeg", "-y", "-i", "assets/audio/refB_audio.wav", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "assets/audio/music3.wav")

# ---------- piston (side view, 700 px wide); every part its own group so it can fly ----------
PISTON = f"""
<svg id="pv" viewBox="-200 -260 1100 1300" width="1100" height="1300" style="position:absolute;left:-10px;top:330px;overflow:visible">
  <defs>
    <linearGradient id="m1" x1="0" x2="1"><stop offset="0" stop-color="#5d6168"/><stop offset="0.3" stop-color="#eef0f2"/>
      <stop offset="0.55" stop-color="#b4b8be"/><stop offset="1" stop-color="#4b4f55"/></linearGradient>
    <linearGradient id="m2" x1="0" x2="1"><stop offset="0" stop-color="#2d2f33"/><stop offset="0.45" stop-color="#d9dce0"/>
      <stop offset="1" stop-color="#26282b"/></linearGradient>
    <linearGradient id="m3" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f2f3f5"/><stop offset="0.5" stop-color="#9da2a8"/>
      <stop offset="1" stop-color="#55595f"/></linearGradient>
  </defs>
  <g id="pbody">
    <path d="M60 120 Q60 70 110 64 L590 64 Q640 70 640 120 L640 560 Q600 600 560 610 L560 760 Q350 820 140 760 L140 610 Q100 600 60 560 Z" fill="url(#m1)"/>
    <ellipse cx="350" cy="70" rx="290" ry="26" fill="#d8dbdf"/>
    <rect x="60" y="138" width="580" height="18" fill="#1f2124"/>
    <rect x="60" y="190" width="580" height="18" fill="#1f2124"/>
    <rect x="60" y="244" width="580" height="28" fill="#1f2124"/>
    <circle cx="350" cy="470" r="78" fill="#3e4146"/><circle cx="350" cy="470" r="52" fill="#1b1c1f"/>
  </g>
  <g id="r0"><ellipse cx="350" cy="147" rx="300" ry="34" fill="none" stroke="url(#m2)" stroke-width="18"/></g>
  <g id="r1"><ellipse cx="350" cy="199" rx="300" ry="34" fill="none" stroke="url(#m2)" stroke-width="18"/></g>
  <g id="r2"><ellipse cx="350" cy="258" rx="300" ry="34" fill="none" stroke="url(#m2)" stroke-width="28"/>
    <ellipse cx="350" cy="258" rx="300" ry="34" fill="none" stroke="#141517" stroke-width="4" stroke-dasharray="14 10"/></g>
  <g id="pin"><rect x="250" y="432" width="200" height="76" rx="38" fill="url(#m3)"/><ellipse cx="450" cy="470" rx="14" ry="38" fill="#8d9298"/></g>
  <g id="c0"><circle cx="262" cy="470" r="34" fill="none" stroke="#c9ccd0" stroke-width="7" stroke-dasharray="190 24"/></g>
  <g id="c1"><circle cx="438" cy="470" r="34" fill="none" stroke="#c9ccd0" stroke-width="7" stroke-dasharray="190 24"/></g>
</svg>"""
# exploded positions (x, y, rotation) for each part, then they slam back on the 4.95 beat
EXP = {"pbody": (0, 170, -6), "r0": (-40, -330, -8), "r1": (40, -215, 7), "r2": (-20, -95, -5),
       "pin": (330, 230, 12), "c0": (-420, 160, -30), "c1": (560, 120, 40)}

html, js = [], []
J = js.append
html.append(f'<div id="pw" style="position:absolute;inset:0;opacity:0;">{PISTON}</div>')
# exploded section: parts fly out on the beat after the cut, drift while held, slam back on 4.95
J('    tl.set("#pw", { opacity: 1 }, %s);' % EXP0)
J(f'    tl.fromTo("#pv", {{ scale: 0.62, x: 0, y: 0, rotation: 0, transformOrigin: "50% 50%" }}, {{ scale: 0.7, duration: 2.2, ease: "none" }}, {EXP0});')
for i, (pid, (x, y, r)) in enumerate(EXP.items()):
    J(f'    tl.fromTo("#{pid}", {{ x: 0, y: 0, rotation: 0, transformOrigin: "50% 50%" }}, {{ x: {x}, y: {y}, rotation: {r}, duration: 0.32, ease: "expo.out" }}, {EXP0 + 0.02 * i:.2f});')
    J(f'    tl.to("#{pid}", {{ x: {x * 1.06:.0f}, y: {y * 1.06 - 12:.0f}, rotation: {r * 1.3:.1f}, duration: 1.25, ease: "sine.inOut" }}, {EXP0 + 0.45:.2f});')
    J(f'    tl.to("#{pid}", {{ x: 0, y: 0, rotation: 0, duration: 0.2, ease: "power4.in" }}, {4.75 + 0.01 * i:.2f});')
J('    tl.to("#pw", { x: -260, filter: "blur(18px)", duration: 0.12, ease: "power2.in" }, 5.08);')
J('    tl.set("#pw", { opacity: 0, x: 0, filter: "blur(0px)" }, 5.2);')
# assembled piston shots in the beat section: each one framed differently (ref grammar: same object, new angle per beat)
FRAMES = [dict(scale=0.66, rotation=-8, x=0, y=0), dict(scale=1.25, rotation=4, x=80, y=330),
          dict(scale=0.78, rotation=10, x=-40, y=170), dict(scale=1.6, rotation=-6, x=-160, y=520),
          dict(scale=0.9, rotation=0, x=0, y=200), dict(scale=0.7, rotation=-12, x=0, y=40)]
for n, (k, t0, t1) in enumerate(PSHOTS):
    f = FRAMES[n % len(FRAMES)]
    J(f'    tl.set("#pw", {{ opacity: 1 }}, {t0});')
    J(f'    tl.fromTo("#pv", {{ scale: {f["scale"] * 1.08:.2f}, rotation: {f["rotation"] - 3}, x: {f["x"]}, y: {f["y"]} }}, '
      f'{{ scale: {f["scale"]}, rotation: {f["rotation"]}, duration: {t1 - t0:.2f}, ease: "expo.out", immediateRender: false }}, {t0});')
    J(f'    tl.set("#pw", {{ opacity: 0 }}, {t1});')
    if n == len(PSHOTS) - 1:   # last beat: rings pop out and back once more
        for i in range(3):
            J(f'    tl.to("#r{i}", {{ y: {-120 - 60 * (2 - i)}, duration: 0.14, ease: "expo.out" }}, {t0 + 0.04 * i:.2f});')
            J(f'    tl.to("#r{i}", {{ y: 0, duration: 0.16, ease: "power4.in" }}, {t0 + 0.32 + 0.03 * i:.2f});')

# frame treatments on some beat shots: white slice bands (ref) or black letterbox
html.append('<div id="wt" style="position:absolute;left:0;right:0;top:0;height:330px;background:#f1f1ef;opacity:0;"></div>'
            '<div id="wb" style="position:absolute;left:0;right:0;bottom:0;height:330px;background:#f1f1ef;opacity:0;"></div>'
            '<div id="lt" style="position:absolute;left:0;right:0;top:0;height:250px;background:#000;opacity:0;"></div>'
            '<div id="lb" style="position:absolute;left:0;right:0;bottom:0;height:250px;background:#000;opacity:0;"></div>')
for k in [3, 8, 13]:
    J(f'    tl.set(["#wt", "#wb"], {{ opacity: 1 }}, {CUTS[k]}); tl.set(["#wt", "#wb"], {{ opacity: 0 }}, {CUTS[k + 1]});')
for k in [5, 10]:
    J(f'    tl.set(["#lt", "#lb"], {{ opacity: 1 }}, {CUTS[k]}); tl.set(["#lt", "#lb"], {{ opacity: 0 }}, {CUTS[k + 1]});')

# top caption bar (ref's opening caption), glow name low in frame + red light, two fact lines on the strong kicks
html.append('<div id="cap" style="position:absolute;left:0;right:0;top:0;padding:46px 60px 40px;background:#fff;text-align:center;'
            'font-weight:800;font-size:58px;line-height:1.12;color:#111;">Genuine NPR piston rings<br>at Kohinoor</div>')
J('    tl.fromTo("#cap", { y: 0 }, { y: -360, duration: 0.25, ease: "power3.in" }, 2.72);')
html.append('<div id="gl" style="position:absolute;left:0;right:0;top:1580px;text-align:center;font-weight:800;font-size:76px;color:#fff;'
            f'text-shadow:0 0 16px rgba(255,255,255,0.8),0 0 40px {RED};opacity:0;">Kohinoor</div>')
html.append(f'<div id="rl" style="position:absolute;left:640px;top:1598px;width:16px;height:40px;border-radius:8px;background:{RED};'
            f'box-shadow:0 0 22px {RED},0 0 60px {RED};opacity:0;"></div>')
J('    tl.fromTo("#gl", { opacity: 0 }, { opacity: 1, duration: 0.2 }, 1.37);')
J('    tl.to("#gl", { opacity: 0, duration: 0.05 }, %s); tl.to("#gl", { opacity: 1, duration: 0.1 }, %s);' % (EXP0, EXP1))
J('    tl.to("#gl", { opacity: 0, duration: 0.05 }, %s);' % END)
for t in [1.42, 2.07, 6.33, 7.63, 8.9, 10.19, 11.47, 12.77, 14.04]:     # reference beat grid (beat_events.py)
    J(f'    tl.fromTo("#rl", {{ opacity: 0.95 }}, {{ opacity: 0, duration: 0.35, ease: "power2.out", immediateRender: false }}, {t});')
for tid, txt, t0, t1 in [("f1", "Authorized NPR dealer", 9.73, 11.07), ("f2", "Nippon Piston Ring<br>Japan, since 1934", 12.97, 14.2)]:
    html.append(f'<div id="{tid}" style="position:absolute;left:70px;right:70px;top:300px;text-align:center;font-weight:800;font-size:92px;'
                f'line-height:1.05;color:#fff;text-shadow:0 6px 28px rgba(0,0,0,0.7);opacity:0;">{txt}</div>')
    J(f'    tl.fromTo("#{tid}", {{ opacity: 0, scale: 1.3, filter: "blur(12px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.22, ease: "expo.out" }}, {t0});')
    J(f'    tl.set("#{tid}", {{ opacity: 0 }}, {t1});')

# whip-pans into the cuts where the reference whips (1.37, 5.2) and a camera punch on every beat cut
for t in [1.37, 5.2]:
    J(f'    tl.to("#cam", {{ x: -260, filter: "blur(18px)", duration: 0.1, ease: "power2.in" }}, {t - 0.1:.2f});')
    J(f'    tl.fromTo("#cam", {{ x: 260, filter: "blur(18px)" }}, {{ x: 0, filter: "blur(0px)", duration: 0.16, ease: "power2.out", immediateRender: false }}, {t});')
for n, t in enumerate(CUTS[1:-1]):
    J(f'    tl.fromTo("#cam", {{ scale: 1.07 }}, {{ scale: 1, duration: 0.22, ease: "expo.out", immediateRender: false }}, {t});')

# end: black, glitch-glow name + "edited by" (as in the reference end)
NAME = "Kohinoor"
html.append('<div id="ec" style="position:absolute;inset:0;background:#000;visibility:hidden;">'
            '<div id="en" style="position:absolute;left:0;right:0;top:820px;text-align:center;font-weight:800;font-size:150px;color:#ffe9ea;'
            f'letter-spacing:-0.02em;text-shadow:0 0 18px rgba(255,120,130,0.9),0 0 60px {RED};">'
            + "".join(f'<span id="el{i}" style="display:inline-block;">{c}</span>' for i, c in enumerate(NAME))
            + '</div><div id="eby" style="position:absolute;left:0;right:0;top:1010px;text-align:center;font-weight:600;font-size:34px;color:#f3d6d8;">'
              'Authorized NPR dealer</div>'
            '<div id="ecr" style="position:absolute;left:0;right:0;top:1062px;text-align:center;font-weight:500;font-size:28px;color:#c9a9ab;">'
            'Edited by MrCopper804</div></div>')
J(f'    tl.set("#ec", {{ visibility: "visible" }}, {END});')
for i in range(len(NAME)):
    J(f'    tl.fromTo("#el{i}", {{ opacity: 0, x: {[-30, 24, -14, 30][i % 4]}, skewX: {[-20, 15][i % 2]} }}, {{ opacity: 1, x: 0, skewX: 0, duration: 0.18, ease: "steps(3)" }}, {END + 0.04 * i:.2f});')
J(f'    tl.fromTo("#en", {{ x: -10 }}, {{ x: 0, duration: 0.06, repeat: 4, yoyo: true, ease: "none" }}, {END + 0.55:.2f});')
J(f'    tl.fromTo(["#eby", "#ecr"], {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25 }}, {END + 0.4:.2f});')
J(f'    tl.to("#ec", {{ opacity: 0, filter: "blur(8px)", duration: 0.35 }}, {TOTAL - 0.45:.2f});')

open("index.html", "w").write(f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={WD}, height={HT}" />
    <script src="assets/vendor/gsap-3.14.2.min.js"></script>
    <style>
      @font-face {{ font-family: "Manrope"; src: url("assets/fonts/Manrope-Variable.ttf"); font-weight: 200 800; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: {WD}px; height: {HT}px; overflow: hidden; background: #000; font-family: Manrope; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="{WD}" data-height="{HT}">
      <div id="cam" style="position:absolute;inset:0;">
        <video id="fv" src="assets/v3.mp4" muted playsinline data-start="0" data-duration="{END}" data-track-index="0"
          style="position:absolute;inset:0;width:{WD}px;height:{HT}px;object-fit:cover;"></video>
        <div id="ov" style="position:absolute;inset:0;">
{chr(10).join(html)}
        </div>
      </div>
      <audio id="mu" src="assets/audio/music3.wav" data-start="0" data-duration="{TOTAL}" data-volume="1" data-track-index="10"></audio>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
""")
print("built v3", TOTAL, "piston shots", PSHOTS)
