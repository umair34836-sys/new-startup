#!/usr/bin/env python3
"""Shangla UPVC 9:16 promo reel (2026-11-20) from the company's own Facebook clips + YouTube project thumbnails.
python3 build_shangla.py PROJECT
PROJECT needs assets/clips/{install1,install2,install3,prof1,prof2,prof3,prod1,prod2,prod3}.mp4 (1080x1920 30 fps),
assets/img/{dha,farm,logo}.(jpg|png), assets/audio/vo_placed.wav (VO at 0.3 s), fonts Poppins + Manrope, sfx.
Line starts T = VO pauses (silencedetect -36 dB) + 0.3 s. Facts: library/clients/shanglaupvc/brief.md.
"""
import os, subprocess, sys
os.chdir(sys.argv[1])
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
PV, TL = "/home/user/tools/perc-venv/bin/python", f"{REPO}/library/tools"
TOTAL = 36.6
T = [0, 3.2, 8.2, 15.9, 19.9, 23.8, 30.0, TOTAL]
GREEN, PUR, INK = "#5bbf2a", "#3d2b8f", "#ffffff"
r2 = lambda x: round(x, 2)
body, js, aud = [], [], []
def tw(sel, fr, to, at): js.append(f'tl.fromTo("{sel}", {fr}, {to}, {r2(at)});')
def show(sel, t0, t1):
    js.append(f'gsap.set("{sel}", {{visibility:"hidden"}});'); js.append(f'tl.set("{sel}", {{visibility:"visible"}}, {r2(t0)});')
    if t1 < TOTAL: js.append(f'tl.set("{sel}", {{visibility:"hidden"}}, {r2(t1)});')
def sfx(n, at, d, v=0.3): aud.append(f'<audio id="fx{len(aud)}" src="assets/sfx/{n}.mp3" data-start="{r2(at)}" data-duration="{d}" data-volume="{v}" data-track-index="{11 + len(aud) % 3}"></audio>')
def clip(i, name, t0, t1, z0=1.0, z1=1.08, origin="50% 50%"):
    d = r2(t1 - t0)
    body.append(f'<div id="v{i}" style="position:absolute;inset:0;overflow:hidden;"><div id="v{i}z" style="position:absolute;inset:0;transform-origin:{origin};">'
                f'<video id="v{i}v" src="assets/clips/{name}.mp4" data-start="{r2(t0)}" data-duration="{d}" muted playsinline style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;"></video></div></div>')
    show(f"#v{i}", t0, t1); tw(f"#v{i}z", f"{{scale:{z0}}}", f'{{scale:{z1}, duration:{d}, ease:"none"}}', t0)
VEIL = '<div style="position:absolute;left:0;right:0;bottom:0;height:900px;background:linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.78) 100%);"></div>'
def title(i, t0, t1, lines, top=1380, size=96):
    h = "".join(f'<div class="ln" id="t{i}_{k}" style="color:{c};">{w}</div>' for k, (w, c) in enumerate(lines))
    body.append(f'<div id="t{i}" style="position:absolute;inset:0;">{VEIL}<div style="position:absolute;left:70px;right:70px;top:{top}px;font-family:PB;font-size:{size}px;line-height:1.05;">{h}</div></div>')
    show(f"#t{i}", t0, t1)
    for k in range(len(lines)): tw(f"#t{i}_{k}", "{y:60, opacity:0}", '{y:0, opacity:1, duration:0.45, ease:"power3.out"}', t0 + 0.15 + k * 0.35)

# 1 hook: real install, a man sliding the door
clip("1", "install1", T[0], T[1], 1.0, 1.12, "60% 40%")
title("1", T[0], T[1], [("Ghar ki khidki", INK), ("sirf sheesha", INK), ("nahi hoti.", GREEN)])
# 2 logo card on white
body.append(f'<div id="lg" style="position:absolute;inset:0;background:#f4f5f2;"><img id="lgi" src="assets/img/logo.png" alt="Shangla UPVC logo" data-start="{T[1]}" data-duration="{r2(T[2] - T[1])}" '
            f'style="position:absolute;left:90px;top:660px;width:900px;height:460px;object-fit:contain;mix-blend-mode:multiply;">'
            f'<div id="lgt" style="position:absolute;left:0;right:0;top:1180px;text-align:center;font-family:PS;font-size:58px;letter-spacing:2px;color:{PUR};">Windows &amp; Doors</div></div>')
show("#lg", T[1], T[2]); tw("#lgi", "{scale:0.7, opacity:0}", '{scale:1, opacity:1, duration:0.6, ease:"back.out(1.6)"}', T[1]); tw("#lgt", "{opacity:0, y:30}", '{opacity:1, y:0, duration:0.5}', T[1] + 1.2)
sfx("impact-punch", T[1], 0.6, 0.3)
# 3 the profile: workshop shots
clip("3a", "prof1", T[2], 11.5, 1.05, 1.0); clip("3b", "prof2", 11.5, T[3], 1.0, 1.08)
title("3", T[2], T[3], [("Imported uPVC profile", INK), ("Single &amp; double", GREEN), ("glazed", GREEN)], size=88)
sfx("whoosh-fast-0.3s", 11.4, 0.3)
# 4 fabrication to installation
clip("4a", "prof3", T[3], 17.6, 1.0, 1.06); clip("4b", "install2", 17.6, T[4], 1.08, 1.0)
title("4", T[3], T[4], [("Fabrication", INK), ("se installation", INK), ("tak.", GREEN)])
sfx("swish-1", 17.5, 0.35)
# 5 three words over the product animation
clip("5", "prod2", T[4], T[5], 1.0, 1.05)
w5 = "".join(f'<div class="ln" id="w{k}" style="color:{c};">{w}</div>' for k, (w, c) in enumerate([("Mazboot.", INK), ("Khoobsurat.", INK), ("Shor bahar.", GREEN)]))
body.append(f'<div id="t5" style="position:absolute;inset:0;">{VEIL}<div style="position:absolute;left:70px;top:1360px;font-family:PB;font-size:110px;line-height:1.05;">{w5}</div></div>')
show("#t5", T[4], T[5])
for k, at in enumerate([20.0, 20.9, 22.0]): tw(f"#w{k}", "{x:-60, opacity:0}", '{x:0, opacity:1, duration:0.4, ease:"power3.out"}', at); sfx("swish-4" if k == 2 else "whoosh-fast-0.3s", at, 0.3, 0.25)
# 6 real projects
cards = ""
for k, (img, lab, top) in enumerate([("dha.jpg", "DHA Overseas Tower", 260), ("farm.jpg", "Farmhouse, Islamabad", 980)]):
    cards += (f'<div id="pc{k}" style="position:absolute;left:110px;top:{top}px;width:860px;">'
              f'<img id="pci{k}" src="assets/img/{img}" alt="{lab} project" data-start="{T[5]}" data-duration="{r2(T[6] - T[5])}" style="display:block;width:860px;height:560px;object-fit:cover;border-radius:28px;border:6px solid #fff;box-shadow:0 30px 70px rgba(0,0,0,0.5);">'
              f'<div style="margin-top:20px;font-family:PB;font-size:62px;color:#fff;">{lab}</div></div>')
body.append(f'<div id="s6" style="position:absolute;inset:0;background:{PUR};">{cards}<div id="s6t" style="position:absolute;left:110px;top:1820px;font-family:PS;font-size:40px;color:{GREEN};">Project delivered</div></div>')
show("#s6", T[5], T[6])
for k, at in enumerate([T[5] + 0.1, 26.6]): tw(f"#pc{k}", "{y:120, opacity:0}", '{y:0, opacity:1, duration:0.55, ease:"power3.out"}', at); sfx("swish-1", at, 0.35, 0.25)
tw("#s6t", "{opacity:0}", "{opacity:1, duration:0.4}", 28.3)
# 7 end card
body.append(f'<div id="e" style="position:absolute;inset:0;background:#f4f5f2;">'
            f'<img id="ei" src="assets/img/logo.png" alt="Shangla UPVC logo" data-start="{T[6]}" data-duration="{r2(TOTAL - T[6])}" style="position:absolute;left:90px;top:200px;width:900px;height:460px;object-fit:contain;mix-blend-mode:multiply;">'
            f'<div id="e1" style="position:absolute;left:0;right:0;top:720px;text-align:center;font-family:PS;font-size:56px;color:{PUR};">Rawalpindi &middot; Islamabad</div>'
            f'<div id="e2" style="position:absolute;left:90px;right:90px;top:880px;padding:40px 0;border-radius:36px;background:#2e7d1a;text-align:center;font-family:PB;font-size:104px;color:#fff;">0311-0444465</div>'
            f'<div id="e3" style="position:absolute;left:0;right:0;top:1150px;text-align:center;font-family:PS;font-size:52px;color:#222;">Abhi call karein</div>'
            f'<div id="e4" style="position:absolute;left:0;right:0;top:1300px;text-align:center;font-family:MR;font-weight:600;font-size:44px;color:#444;">facebook.com/shanglaupvc</div></div>')
show("#e", T[6], TOTAL)
tw("#ei", "{scale:0.8, opacity:0}", '{scale:1, opacity:1, duration:0.5, ease:"back.out(1.6)"}', T[6]); tw("#e1", "{opacity:0}", "{opacity:1, duration:0.4}", 30.4)
tw("#e2", "{scale:0.6, opacity:0}", '{scale:1, opacity:1, duration:0.45, ease:"back.out(2)"}', 32.3); tw("#e3", "{opacity:0}", "{opacity:1, duration:0.4}", 32.8)
tw("#e4", "{opacity:0}", "{opacity:1, duration:0.4}", 33.6); js.append('tl.to("#e2", {scale:1.05, duration:0.4, yoyo:true, repeat:5, ease:"sine.inOut"}, 33.3);')
sfx("confirm-1", 32.3, 0.4, 0.3)

run = lambda *a: subprocess.run(a, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
run(PV, f"{TL}/music_fit.py", f"{REPO}/library/music/" + os.environ.get("MUSIC", "cc0/upbeat-electronic--holiznacc0--pantheon.mp3"), "assets/audio/music.wav", "--length", str(TOTAL), "--end", "fade", "--fade", "1.8")
run(PV, f"{TL}/mix_vo_music.py", "assets/audio/vo_placed.wav", "assets/audio/music.wav", "assets/audio/mix.wav", "--lufs", "-16")
open("index.html", "w").write(f'''<!doctype html>
<html lang="en" data-resolution="portrait"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080, height=1920">
<script src="assets/vendor/gsap-3.14.2.min.js"></script><style>
@font-face {{ font-family:"PB"; src:url("assets/fonts/Poppins-ExtraBold.ttf"); }}
@font-face {{ font-family:"PS"; src:url("assets/fonts/Poppins-SemiBold.ttf"); }}
@font-face {{ font-family:"MR"; src:url("assets/fonts/Manrope-Variable.ttf"); font-weight:200 800; }}
* {{ margin:0; padding:0; box-sizing:border-box; }} html, body {{ width:1080px; height:1920px; overflow:hidden; background:#000; }}
.ln {{ text-shadow:0 4px 18px rgba(0,0,0,0.55); }}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920" style="position:absolute;inset:0;overflow:hidden;background:#000;">
{chr(10).join(body)}
<audio id="mix" src="assets/audio/mix.wav" data-start="0" data-duration="{TOTAL}" data-volume="1.0" data-track-index="10"></audio>
{chr(10).join(aud)}
</div><script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
tl.to({{}}, {{ duration: {TOTAL} }}, 0);
window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;
</script></body></html>''')
print("built shangla reel", TOTAL)
