# Kohinoor promo (Pakistani auto parts dealer, main brand NPR piston rings), 9:16, ~30 s, English VO. First used 2026-11-21.
# The client gave no footage, logo or site ("Kuch nahi, stock se banao"), so the picture is free Mixkit 4K b-roll
# (each page checked: data-license="videoFree") cropped to 9:16, cut on the VO lines (exchange-promo pattern).
# Every on-screen fact: library/clients/kohinoor/site-data.md (owner's words + NPR-RIKEN's own pages, 2026-11-21).
# Hallmark floor (references/gates.md s.4): no eyebrow labels, no tracked caps, no single coloured word in a headline,
# no gradient where footage belongs, one accent (amber bar), real footage behind every card, no em dashes.
#   cd <project>; python3 build_kohinoor.py
# Project (scratchpad, never git): assets/stock/mk_<id>.mp4 (4K Mixkit), assets/vo/lines.json, assets/audio/mix.wav,
# assets/fonts/Manrope-Variable.ttf, assets/sfx/*.mp3, assets/vendor/gsap-3.14.2.min.js
import json, os, subprocess

WD, HT = 1080, 1920
VO_START = 0.5
TOTAL = float(os.environ.get("TOTAL", 30.0))
BG, INK, AMBER, MUTED = "#0b0c0e", "#f4f2ee", "#f2a23a", "#b9b5ad"
L = json.load(open("assets/vo/lines.json"))
st = [round(VO_START + a - 0.12, 2) for a, _ in L]
st[0] = 0.0
SCENES = [(f"s{i + 1}", st[i], st[i + 1] if i + 1 < len(st) else TOTAL) for i in range(len(st))]
W = {k: (s, e) for k, s, e in SCENES}

# scene -> list of (clip id, source start s, x-focus 0..1 of the 9:16 crop, speed). Long scenes get two shots.
# Starts skip what must not show (contact sheets 2026-11-21): mk_65 0-1.5 s shows a radiator cap with a maker's
# badge; mk_44284 0-1.5 s shows the trailer's lettering close up. mk_29995 was dropped (Scotch/brand labels on a desk).
SHOTS = {
    "s1": [("65", 3.0, 0.62, 0.8)],                       # dark engine close-up: hook, slow push
    "s2": [("4716", 1.0, 0.30, 1.0)],                     # mechanic's hands under the hood
    "s3": [("2675", 0.5, 0.47, 1.0)],                     # rev counter climbing: the NPR / Japan / 1934 card
    "s4": [("41937", 0.5, 0.52, 1.0), ("4716", 7.0, 0.62, 1.0)],   # oil into an engine, back to the workshop
    "s5": [("44284", 2.0, 0.42, 1.0)],                    # trucks on the highway under the end card
}


def run(*a):
    subprocess.run(a, check=True, capture_output=True)


def rel(i, frac):
    a, b = L[i]
    return round(max(0.05, VO_START + a + frac * (b - a) - st[i]), 2)


os.makedirs("assets/clips", exist_ok=True)
parts = []
PUSH = {"s1": 0.06, "s3": 0.04, "s5": 0.035}   # slow eased push-in, different per scene (skill #154)
for k, s, e in SCENES:
    d = round(e - s, 3)
    shots = SHOTS[k]
    each = [round(d / len(shots), 3)] * len(shots)
    each[-1] = round(d - sum(each[:-1]), 3)
    for j, ((cid, a, fx, sp), dd) in enumerate(zip(shots, each)):
        out = f"assets/clips/{k}_{j}.mp4"
        cw = int(2160 * 9 / 16) // 2 * 2   # 1214 px wide 9:16 window out of the 3840x2160 source (downscale only)
        vf = (f"setpts=(PTS-STARTPTS)/{sp},fps=30,crop={cw}:2160:{int((3840 - cw) * fx)}:0,"
              f"scale={WD}:{HT}:flags=lanczos,eq=saturation=0.88:contrast=1.04")
        if k in PUSH:
            amt = PUSH[k]
            vf += (f",scale=w='trunc({WD}*(1+{amt}*min(t/{dd},1)*min(t/{dd},1)*(3-2*min(t/{dd},1)))/2)*2':h=-2:eval=frame:flags=bicubic,"
                   f"crop={WD}:{HT}")
        vf += f",tpad=stop_mode=clone:stop_duration={dd},trim=0:{dd},setpts=PTS-STARTPTS,format=yuv420p"
        run("ffmpeg", "-y", "-ss", str(a), "-t", str(dd * sp + 0.5), "-i", f"assets/stock/mk_{cid}.mp4", "-an", "-vf", vf,
            "-t", str(dd), "-c:v", "libx264", "-crf", "16", "-r", "30", out)
        parts.append(out)
open("assets/clips/list.txt", "w").write("".join(f"file '{os.path.basename(p)}'\n" for p in parts))
run("ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "assets/clips/list.txt", "-c", "copy", "assets/screen.mp4")

CSS = f"""
    @font-face {{ font-family: "Manrope"; src: url("assets/fonts/Manrope-Variable.ttf"); font-weight: 200 800; }}
    #root {{ position: absolute; inset: 0; overflow: hidden; font-family: Manrope; color: {INK}; }}
    .veil {{ position: absolute; left: 0; right: 0; bottom: 0; height: 1000px;
             background: linear-gradient(180deg, rgba(11,12,14,0) 0%, rgba(11,12,14,0.93) 30%, rgba(11,12,14,0.97) 100%); }}
    .veilt {{ position: absolute; left: 0; right: 0; top: 0; height: 900px;
              background: linear-gradient(0deg, rgba(11,12,14,0) 0%, rgba(11,12,14,0.9) 35%, rgba(11,12,14,0.95) 100%); }}
    .blk {{ position: absolute; left: 76px; right: 76px; top: 1180px; }}
    .h {{ font-weight: 800; font-size: 108px; line-height: 1.02; letter-spacing: -0.025em; text-shadow: 0 4px 18px rgba(0,0,0,0.5); }}
    .sub {{ font-weight: 500; font-size: 44px; line-height: 1.3; color: {MUTED}; margin-top: 24px; }}
    .bar {{ width: 130px; height: 10px; background: {AMBER}; border-radius: 5px; margin-bottom: 36px; }}
    .chip {{ display: inline-block; font-weight: 700; font-size: 46px; padding: 14px 28px; margin: 0 14px 16px 0;
             border-radius: 14px; background: rgba(20,21,24,0.94); border: 2px solid rgba(242,162,58,0.6); }}
    .amber {{ background: {AMBER}; color: #17110a; border-color: {AMBER}; }}
"""


def comp(cid, html, js):
    return f"""<template>
  <style>{CSS}</style>
  <div id="root" data-composition-id="{cid}" data-width="{WD}" data-height="{HT}">
{html}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{js}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
"""


IN = 'ease: "expo.out"'
C = {}
# s1: title on screen at 0 s (first frame = thumbnail): brand name at the top + the hook line low
C["s1"] = comp("s1", f"""    <div class="veilt" style="height:620px;"></div><div class="veil"></div>
    <div id="s1-b" style="position:absolute;left:76px;top:200px;font-weight:800;font-size:96px;letter-spacing:-0.02em;">Kohinoor</div>
    <div id="s1-bs" style="position:absolute;left:80px;top:318px;font-weight:500;font-size:42px;color:{MUTED};">Auto parts dealer</div>
    <div class="blk"><div class="h" id="s1-h">Your engine deserves genuine parts.</div></div>""",
               f'    tl.fromTo("#s1-h", {{ y: 24 }}, {{ y: 0, duration: 1.0, {IN} }}, 0);\n'
               f'    tl.fromTo("#s1-b", {{ x: -16 }}, {{ x: 0, duration: 1.0, {IN} }}, 0);\n')

# s2: who + the dealer claim (owner's words); headline rises with the amber bar
C["s2"] = comp("s2", f"""    <div class="veil"></div>
    <div class="blk"><div class="bar" id="s2-bar"></div><div class="h" id="s2-h">Kohinoor</div>
      <div class="sub" id="s2-s" style="color:{INK};font-weight:700;font-size:58px;">Authorized NPR dealer</div></div>""",
               f'    tl.fromTo("#s2-bar", {{ scaleX: 0, transformOrigin: "left center" }}, {{ scaleX: 1, duration: 0.5, {IN} }}, {rel(1, 0.0)});\n'
               f'    tl.fromTo("#s2-h", {{ y: 60, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.6, {IN} }}, {rel(1, 0.05)});\n'
               f'    tl.fromTo("#s2-s", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5 }}, {rel(1, 0.45)});\n')

# s3: the brand facts at the TOP of the frame (rev counter stays visible below), slide-in from the left
C["s3"] = comp("s3", f"""    <div class="veilt"></div>
    <div class="blk" style="top:190px;"><div class="h" id="s3-h" style="font-size:180px;">NPR</div>
      <div class="sub" id="s3-s" style="color:{INK};font-weight:700;font-size:60px;margin-top:6px;">Nippon Piston Ring</div>
      <div style="margin-top:34px;"><span class="chip" id="s3-c0">Japan</span><span class="chip amber" id="s3-c1">Since 1934</span></div></div>""",
               f'    tl.fromTo("#s3-h", {{ x: -140, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.6, {IN} }}, {rel(2, 0.02)});\n'
               f'    tl.fromTo("#s3-s", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5 }}, {rel(2, 0.15)});\n'
               f'    tl.fromTo("#s3-c0", {{ x: -40, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.4, {IN} }}, {rel(2, 0.45)});\n'
               f'    tl.fromTo("#s3-c1", {{ x: -40, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.4, {IN} }}, {rel(2, 0.72)});\n')

# s4: what they sell, clip-path wipe (different look from s2/s3)
C["s4"] = comp("s4", f"""    <div class="veil"></div>
    <div class="blk"><div class="h" id="s4-h">Genuine NPR piston rings</div>
      <div class="sub" id="s4-s">and more auto parts, all in one place</div></div>""",
               f'    tl.fromTo("#s4-h", {{ clipPath: "inset(0 100% 0 0)" }}, {{ clipPath: "inset(0 0% 0 0)", duration: 0.8, {IN} }}, {rel(3, 0.02)});\n'
               f'    tl.fromTo("#s4-s", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5 }}, {rel(3, 0.45)});\n')

# s5: end card over dimmed highway footage (real material behind the card); credit line (CLAUDE.md white label)
C["s5"] = comp("s5", f"""    <div style="position:absolute;inset:0;background:rgba(11,12,14,0.72);"></div>
    <div id="e-t" style="position:absolute;left:0;right:0;top:640px;text-align:center;">
      <div class="h" style="font-size:150px;">Kohinoor</div>
      <div class="sub" style="color:{INK};font-weight:700;font-size:58px;margin-top:14px;">Authorized NPR dealer</div>
      <div class="sub" style="margin-top:10px;">Auto parts, Pakistan</div>
      <div style="margin-top:56px;"><span class="chip amber" id="e-c">Ask for genuine NPR</span></div></div>
    <div id="e-cr" style="position:absolute;left:0;right:0;bottom:90px;text-align:center;font-weight:500;font-size:30px;color:{MUTED};">Edited by MrCopper804</div>""",
               f'    tl.fromTo("#e-t", {{ y: 50, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.7, {IN} }}, 0.1);\n'
               f'    tl.fromTo("#e-c", {{ scale: 0.9, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.5, {IN} }}, {rel(4, 0.5)});\n'
               f'    tl.fromTo("#e-cr", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5 }}, 1.2);\n')

os.makedirs("compositions", exist_ok=True)
for k, v in C.items():
    open(f"compositions/{k}.html", "w").write(v)

divs = [f'      <video id="screen" src="assets/screen.mp4" muted playsinline data-start="0" data-duration="{TOTAL}" data-track-index="0" '
        f'style="position:absolute;inset:0;width:{WD}px;height:{HT}px;object-fit:cover;"></video>']
for k, s, e in SCENES:
    divs.append(f'      <div id="{k}" data-composition-id="{k}" data-composition-src="compositions/{k}.html" data-start="{s}" '
                f'data-duration="{round(e - s, 3)}" data-track-index="1" data-track-kind="graphics" data-width="{WD}" data-height="{HT}" style="z-index: 1"></div>')


def dur(p):
    return round(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                      capture_output=True, text=True).stdout), 3)


# SFX: each file once (owner rule, GOOD's 2026-11-02), only where the picture changes a lot (skill #2032, #147):
# a metal hit under the NPR card (the brand moment), one whoosh into the end card, a soft thud under the end chip.
sfx = lambda n: f"assets/sfx/{n}.mp3"
A = [("mix", "assets/audio/mix.wav", 0, min(dur("assets/audio/mix.wav"), TOTAL), 1.0, 10)]
ONE = [("hit", "metal-hit", round(W["s3"][0] + rel(2, 0.02) + 0.1, 2), 0.35),
       ("wh", "whoosh-down-0.6s", round(W["s5"][0] - 0.3, 2), 0.35),
       ("thud", "soft-thud", round(W["s5"][0] + rel(4, 0.5), 2), 0.35)]
assert len({n for _, n, _, _ in ONE}) == len(ONE), "an SFX file repeats"
for ln, (i, n, t, v) in enumerate(ONE):
    A.append((i, sfx(n), t, dur(sfx(n)), v, 11 + ln))
aud = "\n".join(f'      <audio id="{i}" src="{s}" data-start="{a}" data-duration="{dd}" data-volume="{v}" data-track-index="{ln}"></audio>'
                for i, s, a, dd, v, ln in A)
open("index.html", "w").write(f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={WD}, height={HT}" />
    <script src="assets/vendor/gsap-3.14.2.min.js"></script>
    <style>* {{ margin: 0; padding: 0; box-sizing: border-box; }} html, body {{ margin: 0; width: {WD}px; height: {HT}px; overflow: hidden; background: {BG}; }}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="{WD}" data-height="{HT}">
{chr(10).join(divs)}
{aud}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
""")
print("built", TOTAL, SCENES)
