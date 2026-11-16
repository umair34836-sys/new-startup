#!/usr/bin/env python3
"""Hosting-partner pitch (16:9): hook from real in-game clips -> the host's problem -> mock "Your Hosting" ad
-> how it works for the host -> closing line. English captions under a Hinglish VO.

python3 build_hosting_pitch.py PROJECT [--brand "Your Hosting"] [--domain panel.yourhosting.com]
PROJECT needs: assets/vendor/gsap-3.14.2.min.js, assets/fonts/{SpaceGrotesk,Manrope,JetBrainsMono}-Variable.ttf,
assets/clips/{a_chat,b_mon,c_studio,c_tunnel,d_mon2,d_green,d_arena,e_tp,f_mon3,panel}.mp4 (1536x864, 30 fps),
assets/img/{discord,done}.png (done = the "Sir done" chat lines, 1536x221), assets/audio/vo_placed.wav (VO placed at 0.3 s), assets/sfx/*.mp3.
Scene times below are the VO's own pauses (silencedetect -36 dB) + 0.3 s; change T for a new VO.
"""
import argparse, html, os, subprocess, sys

ap = argparse.ArgumentParser(); ap.add_argument("project"); ap.add_argument("--brand", default="Your Hosting")
ap.add_argument("--domain", default="panel.yourhosting.com"); ap.add_argument("--music", default="cc0/upbeat-electronic--loyalty-freak-music--monarch-of-the-street.mp3")
A = ap.parse_args(); os.chdir(A.project)
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
PV, TL = "/home/user/tools/perc-venv/bin/python", f"{REPO}/library/tools"
E = html.escape; BRAND, DOMAIN = E(A.brand), E(A.domain)
TOTAL = 69.38
T = [0, 2.73, 4.78, 9.73, 14.02, 20.95, 24.48, 30.47, 34.87, 40.69, 46.59, 49.42, 54.78, 59.33, 63.06, TOTAL]
CAP = ["He typed one line.", "The server built it.", "A studio. A tunnel. A Discord post. One line each.",
       "Not a mod. An AI built into the server.", "Every host sells the same thing.",
       "So customers just pick the cheapest.", "Now imagine your host says: AI-integrated servers.",
       "Your customer talks. Their server works.", "Everyone wants AI. Be the first host to offer it.",
       "The whole panel is yours. Your domain. Your brand.", "No ports to open. Just install the plugin.",
       "It only listens to allowed players. Other chat stays private.",
       "Risky commands are blocked. The owner stays in control.", "Your price. Your plans. Your customers.",
       "Everyone sells servers. You sell AI servers."]
BG, INK, MUT, AC, PAN = "#0b0d10", "#f4f1ec", "#9aa3ad", "#e8914d", "#151a20"
r2 = lambda x: round(x, 2)
body, js, aud = [], [], []
def tw(sel, fr, to, at): js.append(f'tl.fromTo("{sel}", {fr}, {to}, {r2(at)});')
def show(sel, t0, t1):
    js.append(f'gsap.set("{sel}", {{visibility:"hidden"}});'); js.append(f'tl.set("{sel}", {{visibility:"visible"}}, {r2(t0)});')
    if t1 < TOTAL: js.append(f'tl.set("{sel}", {{visibility:"hidden"}}, {r2(t1)});')
def sfx(name, at, dur, vol=0.3):
    aud.append(f'<audio id="fx{len(aud)}" src="assets/sfx/{name}.mp3" data-start="{r2(at)}" data-duration="{dur}" data-volume="{vol}" data-track-index="{11 + len(aud) % 3}"></audio>')
WIN = "position:absolute;left:192px;top:44px;width:1536px;height:864px;border-radius:18px;overflow:hidden;background:#000;box-shadow:0 30px 80px rgba(0,0,0,0.6), 0 0 0 2px #262d36;"
def vid(i, clip, t0, t1, extra="", z0=1.0, z1=1.06, origin="50% 50%"):
    d = r2(t1 - t0)
    body.append(f'<div id="s{i}" style="{WIN}"><div id="s{i}z" style="position:absolute;inset:0;transform-origin:{origin};">'
                f'<video id="s{i}v" src="assets/clips/{clip}.mp4" data-start="{r2(t0)}" data-duration="{d}" muted playsinline style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;"></video></div>{extra}</div>')
    show(f"#s{i}", t0, t1); tw(f"#s{i}z", f"{{scale:{z0}}}", f'{{scale:{z1}, duration:{d}, ease:"none"}}', t0)
def stage(i, t0, t1, inner):
    body.append(f'<div id="s{i}" style="position:absolute;left:0;top:0;width:1920px;height:920px;">{inner}</div>'); show(f"#s{i}", t0, t1)
def badge(i):
    return (f'<div id="s{i}b" style="position:absolute;left:36px;top:36px;padding:16px 26px;border-radius:14px;background:rgba(11,13,16,0.86);'
            f'font-family:SG;font-weight:700;font-size:38px;color:{INK};"><span style="color:{AC};">{BRAND}</span> &nbsp;AI-Integrated Servers</div>')

# 1 hook: the typed line (zoom toward the chat, bottom-left of the frame)
vid("1", "a_chat", T[0], T[1], z0=1.0, z1=1.5, origin="18% 86%")
# 2 the result
vid("2", "b_mon", T[1], T[2], z0=1.12, z1=1.0); sfx("impact-punch", T[1], 0.6, 0.32)
# 3 studio, tunnel, Discord proof
vid("3a", "c_studio", T[2], 5.71); vid("3b", "c_tunnel", 5.71, 6.6); sfx("whoosh-fast-0.3s", 5.6, 0.3); sfx("swish-1", 6.5, 0.35)
stage("3c", 6.6, T[3], f'<img id="s3ci" src="assets/img/discord.png" alt="Discord announcement posted by the server" data-start="6.6" data-duration="{r2(T[3] - 6.6)}" '
      f'style="position:absolute;left:296px;top:240px;width:1328px;height:400px;border-radius:16px;box-shadow:0 30px 80px rgba(0,0,0,0.6), 0 0 0 2px #262d36;">'
      f'<div id="s3ct" style="position:absolute;left:296px;top:150px;font-family:SG;font-weight:600;font-size:40px;color:{MUT};">Posted to Discord by the server</div>')
tw("#s3ci", "{y:60, opacity:0}", '{y:0, opacity:1, duration:0.4, ease:"power3.out"}', 6.6); tw("#s3ct", "{opacity:0}", "{opacity:1, duration:0.3}", 6.9)
# 4 the reply, read off the real chat
stage("4", T[3], T[4], f'<img id="s4i" src="assets/img/done.png" alt="Server reply in chat: Sir done" data-start="{T[3]}" data-duration="{r2(T[4] - T[3])}" '
      f'style="position:absolute;left:192px;top:340px;width:1536px;height:221px;border-radius:16px;box-shadow:0 30px 80px rgba(0,0,0,0.6), 0 0 0 2px {AC};">'
      f'<div id="s4t" style="position:absolute;left:192px;top:190px;font-family:SG;font-weight:700;font-size:76px;color:{INK};">An AI built into the server</div>')
tw("#s4i", "{scale:0.92, opacity:0}", '{scale:1, opacity:1, duration:0.45, ease:"power3.out"}', T[3]); tw("#s4t", "{y:30, opacity:0}", '{y:0, opacity:1, duration:0.4, ease:"power3.out"}', 11.36)
sfx("pop-low", T[3], 0.2)
# 5-6 three identical hosts, then the price race
cards = ""
for k, nm in enumerate(["Host A", "Host B", "Host C"]):
    rows = "".join(f'<div style="display:flex;align-items:center;gap:18px;margin-top:34px;"><span style="width:150px;font-size:36px;color:{MUT};">{lab}</span>'
                   f'<span id="c{k}{lab}" style="display:block;width:250px;height:22px;border-radius:11px;background:{col};transform-origin:0 50%;"></span></div>'
                   for lab, col in (("RAM", "#3a444f"), ("Uptime", "#3a444f"), ("Price", AC)))
    cards += (f'<div id="c{k}" style="position:absolute;left:{210 + k * 520}px;top:250px;width:460px;height:470px;border-radius:22px;background:{PAN};'
              f'box-shadow:0 0 0 2px #262d36;padding:44px;font-family:MR;"><div style="font-family:SG;font-weight:700;font-size:54px;color:{INK};">{nm}</div>{rows}'
              f'<div id="c{k}x" style="margin-top:30px;font-size:32px;color:{AC};font-weight:700;">cheaper</div></div>')
stage("5", T[4], T[6], f'<div id="s5t" style="position:absolute;left:210px;top:110px;font-family:SG;font-weight:700;font-size:72px;color:{INK};">Same servers. Same pitch.</div>{cards}')
tw("#s5t", "{y:30, opacity:0}", '{y:0, opacity:1, duration:0.4, ease:"power3.out"}', T[4])
for k in range(3):
    tw(f"#c{k}", "{y:70, opacity:0}", '{y:0, opacity:1, duration:0.45, ease:"power3.out"}', 15.6 + k * 0.22)
    js.append(f'gsap.set("#c{k}x", {{opacity:0}});'); js.append(f'tl.to("#c{k}x", {{opacity:1, duration:0.2}}, {r2(21.2 + k * 0.7)});')
    js.append(f'tl.to("#c{k}Price", {{scaleX:{[0.7, 0.5, 0.3][k]}, duration:0.5, ease:"power2.inOut"}}, {r2(21.2 + k * 0.7)});'); sfx(["pop-high", "pop-low", "pop-high"][k], 21.2 + k * 0.7, 0.15, 0.25)
for lab, at in (("RAM", 18.5), ("Price", 19.15), ("Uptime", 19.75)):
    for k in range(3): js.append(f'tl.to("#c{k}{lab}", {{scaleY:2.2, duration:0.18, yoyo:true, repeat:1, ease:"power2.out"}}, {at + k * 0.05});')
# 7 the mock ad
ad = (f'<div style="position:absolute;inset:0;background:linear-gradient(90deg, rgba(11,13,16,0.94) 0%, rgba(11,13,16,0.7) 55%, rgba(11,13,16,0.15) 100%);"></div>'
      f'<div id="s7a" style="position:absolute;left:80px;top:210px;font-family:SG;font-weight:700;font-size:64px;color:{AC};">{BRAND}</div>'
      f'<div id="s7b" style="position:absolute;left:80px;top:300px;width:1000px;font-family:SG;font-weight:700;font-size:112px;line-height:1.02;letter-spacing:-3px;color:{INK};">AI-Integrated Servers</div>'
      f'<div id="s7c" style="position:absolute;left:80px;top:560px;font-family:MR;font-weight:600;font-size:42px;color:{INK};">Every server comes with a built-in AI.</div>')
vid("7", "f_mon3", T[6], T[7], extra=ad, z0=1.0, z1=1.08); sfx("swish-4", T[6], 0.4)
tw("#s7a", "{x:-40, opacity:0}", '{x:0, opacity:1, duration:0.4, ease:"power3.out"}', 24.7); tw("#s7b", "{x:-60, opacity:0}", '{x:0, opacity:1, duration:0.5, ease:"power3.out"}', 26.4)
tw("#s7c", "{opacity:0}", "{opacity:1, duration:0.4}", 27.5)
# 8 customer talks, server works
vid("8", "e_tp", T[7], T[8], extra=badge("8"), z0=1.0, z1=1.05)
# 9 montage under the host's name
for k, (c, a, b) in enumerate([("d_mon2", T[8], 36.8), ("d_green", 36.8, 38.7), ("d_arena", 38.7, T[9])]):
    vid(f"9{k}", c, a, b, extra=badge(f"9{k}"), z0=1.08, z1=1.0); sfx(["whoosh-fast-0.3s", "swish-1", "swish-4"][k], a - 0.1, 0.3, 0.28)
# 10 the panel in a drawn browser window on the host's own domain
bar = (f'<div style="position:absolute;left:0;top:0;right:0;height:64px;background:#1b2129;display:flex;align-items:center;gap:12px;padding:0 24px;">'
       f'<span style="width:16px;height:16px;border-radius:50%;background:#ff5f57;"></span><span style="width:16px;height:16px;border-radius:50%;background:#febc2e;"></span><span style="width:16px;height:16px;border-radius:50%;background:#28c840;"></span>'
       f'<div style="margin-left:28px;flex:1;height:40px;border-radius:20px;background:#0b0d10;font-family:JB;font-size:28px;line-height:40px;padding:0 22px;color:{INK};">https://{DOMAIN}</div></div>')
d10 = r2(T[10] - T[9])
body.append(f'<div id="s10" style="{WIN}">{bar}<video id="s10v" src="assets/clips/panel.mp4" data-start="{T[9]}" data-duration="{d10}" muted playsinline '
            f'style="position:absolute;left:-152px;top:64px;width:1840px;height:1035px;"></video></div>')
show("#s10", T[9], T[10]); tw("#s10", "{y:50, opacity:0}", '{y:0, opacity:1, duration:0.45, ease:"power3.out"}', T[9]); sfx("confirm-1", T[9], 0.4, 0.22)
# 11-13 three assurances, one list that fills up
pts = [("No ports to open", "The plugin only makes outbound HTTPS calls.", T[10]),
       ("It listens only when asked", "A set prefix + an allowed player. Other chat never leaves the server.", T[11]),
       ("The owner stays in control", "Risky commands like /stop and /op are blocked. Big changes ask first.", T[12])]
lst = "".join(f'<div id="p{k}" style="position:absolute;left:210px;top:{150 + k * 235}px;width:1500px;"><div style="font-family:JB;font-size:34px;color:{AC};">0{k + 1}</div>'
              f'<div style="font-family:SG;font-weight:700;font-size:76px;letter-spacing:-2px;color:{INK};line-height:1.1;">{E(a)}</div>'
              f'<div id="p{k}s" style="font-family:MR;font-weight:500;font-size:36px;color:{MUT};margin-top:6px;">{E(b)}</div>'
              f'<div id="p{k}l" style="width:1500px;height:4px;margin-top:14px;background:{AC};transform-origin:0 50%;"></div></div>' for k, (a, b, _) in enumerate(pts))
stage("11", T[10], T[13], lst)
for k, (_, _, at) in enumerate(pts):
    tw(f"#p{k}", "{x:-50, opacity:0}", '{x:0, opacity:1, duration:0.45, ease:"power3.out"}', at); sfx(["pop-high", "pop-low", "pop-high"][k], at, 0.15, 0.25)
    tw(f"#p{k}s", "{opacity:0}", "{opacity:1, duration:0.4}", at + 1.1); tw(f"#p{k}l", "{scaleX:0}", f'{{scaleX:1, duration:{r2([T[11], T[12], T[13]][k] - at - 1.6)}, ease:"none"}}', at + 1.5)
# 14 yours
w14 = "".join(f'<div id="y{k}" style="font-family:SG;font-weight:700;font-size:150px;letter-spacing:-5px;line-height:1.08;color:{INK};">Your {w}.</div>' for k, w in enumerate(["price", "plans", "customers"]))
stage("14", T[13], T[14], f'<div style="position:absolute;left:210px;top:190px;">{w14}</div>')
for k, at in enumerate([59.33, 60.45, 61.3]): tw(f"#y{k}", "{y:50, opacity:0}", '{y:0, opacity:1, duration:0.35, ease:"power3.out"}', at)
# 15 close
stage("15", T[14], TOTAL, f'<div id="e1" style="position:absolute;left:210px;top:230px;font-family:SG;font-weight:600;font-size:72px;color:{MUT};">Everyone sells servers.</div>'
      f'<div id="e2" style="position:absolute;left:210px;top:330px;font-family:SG;font-weight:700;font-size:148px;letter-spacing:-5px;color:{INK};">You sell AI servers.</div>'
      f'<div id="e3" style="position:absolute;left:210px;top:620px;font-family:JB;font-weight:700;font-size:56px;color:{AC};">copper_work</div>'
      f'<div id="e4" style="position:absolute;left:210px;top:700px;font-family:MR;font-weight:500;font-size:36px;color:{MUT};">The AI layer for Minecraft hosts</div>')
tw("#e1", "{opacity:0}", "{opacity:1, duration:0.4}", T[14]); tw("#e2", "{y:40, opacity:0}", '{y:0, opacity:1, duration:0.5, ease:"power3.out"}', 65.1)
tw("#e3", "{opacity:0}", "{opacity:1, duration:0.5}", 66.4); tw("#e4", "{opacity:0}", "{opacity:1, duration:0.5}", 66.7); sfx("impact-punch", 65.1, 0.6, 0.3)
# captions
for i, c in enumerate(CAP):
    body.append(f'<div id="cp{i}" style="position:absolute;left:160px;right:160px;top:948px;text-align:center;font-family:MR;font-weight:700;font-size:46px;color:{INK};">{E(c)}</div>')
    show(f"#cp{i}", T[i], T[i + 1]); tw(f"#cp{i}", "{y:14, opacity:0}", '{y:0, opacity:1, duration:0.25, ease:"power2.out"}', T[i])

run = lambda *a: subprocess.run(a, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
run(PV, f"{TL}/music_fit.py", f"{REPO}/library/music/{A.music}", "assets/audio/music.wav", "--length", str(TOTAL), "--end", "fade", "--fade", "2.0")
run(PV, f"{TL}/mix_vo_music.py", "assets/audio/vo_placed.wav", "assets/audio/music.wav", "assets/audio/mix.wav", "--lufs", "-16")
open("index.html", "w").write(f'''<!doctype html>
<html lang="en" data-resolution="landscape"><head><meta charset="UTF-8"><meta name="viewport" content="width=1920, height=1080">
<script src="assets/vendor/gsap-3.14.2.min.js"></script><style>
@font-face {{ font-family:"SG"; src:url("assets/fonts/SpaceGrotesk-Variable.ttf"); font-weight:300 700; }}
@font-face {{ font-family:"MR"; src:url("assets/fonts/Manrope-Variable.ttf"); font-weight:200 800; }}
@font-face {{ font-family:"JB"; src:url("assets/fonts/JetBrainsMono-Variable.ttf"); font-weight:100 800; }}
* {{ margin:0; padding:0; box-sizing:border-box; }} html, body {{ width:1920px; height:1080px; overflow:hidden; background:{BG}; }}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1920" data-height="1080" style="position:absolute;inset:0;overflow:hidden;background:{BG};">
{chr(10).join(body)}
<audio id="mix" src="assets/audio/mix.wav" data-start="0" data-duration="{TOTAL}" data-volume="1.0" data-track-index="10"></audio>
{chr(10).join(aud)}
</div><script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
tl.to({{}}, {{ duration: {TOTAL} }}, 0);
window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;
</script></body></html>''')
print(f"built hosting pitch: {TOTAL} s, brand {A.brand}, domain {A.domain}")
