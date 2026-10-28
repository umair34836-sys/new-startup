# Heaven Developer 9:16 ~30 s Discord-server promo (free VoxCPM2 English VO, field voice promo-male). 2026-10-28.
# Based on library/templates/hosting-promo-reel/build_hostlixo.py (scene starts = VO line starts from assets/vo/lines.json).
# Every on-screen claim is read from the client's own Discord server in the owner's screen recording (Drive
# 1QMS1Hctwo9_0H7jxdUWhux0IRsTGTY8T), listed with times in library/clients/heavendeveloper/brief.md (2026-10-28):
# profile "Premium Discord development: websites, Discord bots, Minecraft mods, plugins and texture packs. Free, Paid and
# Premium plans", 2,521 Members; footer "Premium development, delivered"; #services list; #pricing "Limited Edition
# Perks" starting prices (owner chose these, 2026-10-28); #invite-rewards "3 invites: one small project", "7 invites: one
# medium project"; #reviews 5/5; welcome "Open a ticket ... share your idea ... we deliver"; banner "JOIN HEAVEN DEVELOPER".
# Look = the client's own: black marble + gold logo, Discord blurple banner/buttons, gold left bar of the bot embeds.
# Needs in the project (scratchpad, never git): assets/img/{logo,banner,services,pricing,invite,review}.jpg (crops of
# recording frames), assets/clips/services.mp4 (recording 45-50 s, status bar cropped), assets/fonts (library/fonts:
# Poppins, PlayfairDisplay-Italic, JetBrainsMono), assets/sfx, assets/vendor/gsap, assets/audio/mix.wav (VO + music,
# mix_vo_music.py) or assets/vo/vo.wav, assets/vo/lines.json.
import json, os, subprocess

VO_START = 0.35
BG, GOLD, GOLD2, BLURPLE, WHITE, GREY = "#07060a", "#e2b85c", "#f7dc94", "#5865f2", "#ffffff", "#b9b4c4"
if os.path.exists("assets/vo/lines.json"):
    L = json.load(open("assets/vo/lines.json"))           # [[start, end], ...] per script line inside vo.wav
else:  # layout preview before the VO exists
    L = [[0, 2.6], [3.1, 6.0], [6.5, 10.4], [10.9, 14.2], [14.7, 17.8], [18.3, 21.0], [21.5, 25.6]]
VO_END = VO_START + L[-1][1]
TOTAL = float(os.environ.get("TOTAL", 30.0))  # owner chose ~30 s
st = [round(VO_START + a - 0.12, 2) for a, _ in L]
st[0] = 0.0
SCENES = [(f"s{i + 1}", st[i], st[i + 1] if i + 1 < len(st) else TOTAL) for i in range(len(st))]
W = {k: (s, e) for k, s, e in SCENES}


def dur(p):
    return round(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                      capture_output=True, text=True).stdout), 3)


def rel(i, frac):
    a, b = L[i]
    return round(max(0.05, VO_START + a + frac * (b - a) - st[i]), 2)


def d_of(k):
    s, e = W[k]
    return round(e - s, 2)


GOLDTXT = (f"background: linear-gradient(180deg, {GOLD2} 0%, {GOLD} 55%, #a97a2c 100%); -webkit-background-clip: text; "
           "background-clip: text; color: transparent;")
CSS = f"""
    @font-face {{ font-family: "PX"; src: url("assets/fonts/Poppins-ExtraBold.ttf"); font-weight: 800; }}
    @font-face {{ font-family: "PB"; src: url("assets/fonts/Poppins-Bold.ttf"); font-weight: 700; }}
    @font-face {{ font-family: "PS"; src: url("assets/fonts/Poppins-SemiBold.ttf"); font-weight: 600; }}
    @font-face {{ font-family: "PF"; src: url("assets/fonts/PlayfairDisplay-Italic.ttf"); font-style: italic; }}
    @font-face {{ font-family: "JB"; src: url("assets/fonts/JetBrainsMono-Variable.ttf"); font-weight: 100 800; }}
    #root {{ position: absolute; inset: 0; overflow: hidden; }}
    .c {{ position: absolute; left: 0; right: 0; text-align: center; }}
    .h {{ font-family: PX; font-weight: 800; line-height: 1.0; letter-spacing: -1px; color: {WHITE}; text-shadow: 0 8px 34px rgba(0,0,0,0.65); }}
    .gold {{ {GOLDTXT} text-shadow: none; filter: drop-shadow(0 6px 22px rgba(226,184,92,0.35)); }}
    .pf {{ font-family: PF; font-style: italic; }}
    .lab {{ display: inline-block; font-family: JB; font-weight: 700; font-size: 30px; letter-spacing: 3px; color: {GOLD2};
            padding: 12px 26px; border: 2px solid rgba(226,184,92,0.55); border-radius: 999px; background: rgba(12,10,16,0.85); }}
    .card {{ background: rgba(16,14,22,0.92); border: 2px solid rgba(226,184,92,0.28); border-left: 8px solid {GOLD}; border-radius: 22px; }}
    .shot {{ border: 3px solid rgba(226,184,92,0.55); border-radius: 26px; overflow: hidden; box-shadow: 0 30px 90px rgba(0,0,0,0.75), 0 0 60px rgba(226,184,92,0.18); }}
    .btn {{ display: inline-flex; align-items: center; gap: 24px; background: {BLURPLE}; color: #fff; font-family: PX;
            font-weight: 800; border-radius: 22px; padding: 30px 56px; font-size: 56px; box-shadow: 0 18px 60px rgba(88,101,242,0.55); }}
"""

# simple line icons (drawn here, stroke style); Discord mark = the official glyph path
ICON = {
    "bot": '<rect x="4" y="7" width="16" height="12" rx="3"></rect><path d="M12 3v4"></path><circle cx="9" cy="13" r="1.3"></circle><circle cx="15" cy="13" r="1.3"></circle><path d="M2 12v3M22 12v3"></path>',
    "code": '<rect x="2" y="4" width="20" height="16" rx="2"></rect><path d="m9 10-2 2 2 2M15 10l2 2-2 2"></path>',
    "cube": '<path d="M21 16V8l-9-5-9 5v8l9 5 9-5z"></path><path d="M3.3 7.5 12 12l8.7-4.5M12 22V12"></path>',
    "sword": '<path d="M14.5 17.5 3 6V3h3l11.5 11.5"></path><path d="m13 19 6-6M16 16l4 4M19 21l2-2"></path>',
    "grid": '<rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect>',
    "gift": '<rect x="3" y="8" width="18" height="4" rx="1"></rect><path d="M12 8v13M19 12v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7"></path><path d="M7.5 8a2.5 2.5 0 0 1 0-5C11 3 12 8 12 8s1-5 4.5-5a2.5 2.5 0 0 1 0 5"></path>',
    "ticket": '<path d="M3 7a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v3a2 2 0 0 0 0 4v3a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-3a2 2 0 0 0 0-4z"></path><path d="M13 5v14" stroke-dasharray="2 2"></path>',
    "idea": '<path d="M9 18h6M10 22h4"></path><path d="M12 2a7 7 0 0 0-4 12.7V17h8v-2.3A7 7 0 0 0 12 2z"></path>',
    "check": '<circle cx="12" cy="12" r="10"></circle><path d="m8 12 3 3 5-6"></path>',
}
DISCORD = '<path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0 12.64 12.64 0 0 0-.617-1.25.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 0 0 .031.057 19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028c.462-.63.874-1.295 1.226-1.994a.076.076 0 0 0-.041-.106 13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.128 10.2 10.2 0 0 0 .372-.292.074.074 0 0 1 .077-.01c3.929 1.793 8.18 1.793 12.061 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127 12.299 12.299 0 0 1-1.873.894.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.028zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.955-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.946 2.418-2.157 2.418z"></path>'


def icon(k, size=64, box=True, col=GOLD2):
    svg = f'<svg viewBox="0 0 24 24" style="width:{size}px;height:{size}px;" fill="none" stroke="{col}" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">{ICON[k]}</svg>'
    if not box:
        return svg
    return (f'<div style="width:{size + 40}px;height:{size + 40}px;flex:none;border:2px solid rgba(226,184,92,0.5);border-radius:18px;'
            f'display:flex;align-items:center;justify-content:center;background:rgba(226,184,92,0.08);">{svg}</div>')


def comp(cid, html, js):
    return f"""<template>
  <style>{CSS}</style>
  <div id="root" data-composition-id="{cid}" data-width="1080" data-height="1920">
{html}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{js}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
"""


def enter_exit(sel, d, enter=True, exit_=True):
    js = ""
    if enter:
        js += f'    tl.fromTo("{sel}", {{ scale: 1.12, filter: "blur(14px)", opacity: 0 }}, {{ scale: 1, filter: "blur(0px)", opacity: 1, duration: 0.3, ease: "power3.out" }}, 0);\n'
    if exit_:
        js += f'    tl.to("{sel}", {{ scale: 1.3, filter: "blur(16px)", opacity: 0, duration: 0.22, ease: "power3.in" }}, {d - 0.22:.2f});\n'
    return js


C = {}
# global background: deep black-violet with slow gold + blurple glows, faint gold dot grid and a light sweep
C["bg"] = comp("bg", f"""    <div style="position:absolute;inset:0;background:radial-gradient(120% 80% at 50% 30%, #15111d 0%, {BG} 65%);"></div>
    <div id="bg-g1" style="position:absolute;left:-200px;top:-200px;width:1100px;height:1100px;border-radius:50%;background:radial-gradient(circle, rgba(226,184,92,0.16), rgba(226,184,92,0) 70%);" data-layout-allow-overflow></div>
    <div id="bg-g2" style="position:absolute;left:300px;top:1100px;width:1100px;height:1100px;border-radius:50%;background:radial-gradient(circle, rgba(88,101,242,0.16), rgba(88,101,242,0) 70%);" data-layout-allow-overflow></div>
    <div id="bg-dots" style="position:absolute;left:0;top:0;width:1080px;height:2200px;background-image:radial-gradient(rgba(226,184,92,0.16) 2px, transparent 2.5px);background-size:54px 54px;" data-layout-allow-overflow></div>
    <div id="bg-sw" style="position:absolute;left:-900px;top:-400px;width:500px;height:2800px;transform:rotate(18deg);background:linear-gradient(90deg, rgba(247,220,148,0), rgba(247,220,148,0.07), rgba(247,220,148,0));" data-layout-allow-overflow></div>""",
               f'    tl.fromTo("#bg-dots", {{ y: 0 }}, {{ y: -162, duration: {TOTAL}, ease: "none" }}, 0);\n'
               f'    tl.fromTo("#bg-g1", {{ scale: 0.9, x: 0 }}, {{ scale: 1.25, x: 400, duration: {TOTAL}, ease: "sine.inOut" }}, 0);\n'
               f'    tl.fromTo("#bg-g2", {{ scale: 1.1, x: 0 }}, {{ scale: 0.9, x: -500, duration: {TOTAL}, ease: "sine.inOut" }}, 0);\n'
               f'    tl.fromTo("#bg-sw", {{ x: 0 }}, {{ x: 2600, duration: 6, ease: "none", repeat: {int(TOTAL // 6)} }}, 0);\n')

# S1 hook (on screen at 0 s = thumbnail): the client's own "JOIN HEAVEN DEVELOPER" banner behind, three asks stacked
d = d_of("s1")
C["s1"] = comp("s1", f"""    <div id="s1-w" style="position:absolute;inset:0;">
      <div id="s1-ph" style="position:absolute;left:-60px;top:120px;width:1200px;height:566px;background:url(assets/img/banner.jpg) center/cover;filter:blur(3px) brightness(0.55);opacity:0.9;" data-layout-allow-overflow></div>
      <div style="position:absolute;inset:0;background:linear-gradient(180deg, rgba(7,6,10,0.2) 0%, rgba(7,6,10,0.85) 38%, rgba(7,6,10,0.96) 100%);"></div>
      <div class="c" id="s1-l" style="top:380px;"><span class="lab">DISCORD • WEB • MINECRAFT</span></div>
      <div class="c h" id="s1-a" style="top:500px;font-size:120px;">NEED A</div>
      <div class="c h" id="s1-b" style="top:645px;font-size:112px;color:#8f99ff;">DISCORD BOT?</div>
      <div class="c h" id="s1-c" style="top:790px;font-size:132px;">WEBSITE?</div>
      <div class="c h gold" id="s1-d" style="top:940px;font-size:112px;">MINECRAFT<br>PLUGIN?</div>
    </div>""",
               f'    tl.fromTo("#s1-ph", {{ scale: 1.15 }}, {{ scale: 1.0, duration: {d}, ease: "none" }}, 0);\n'
               '    tl.fromTo("#s1-b", { scale: 1.08 }, { scale: 1, duration: 0.9, ease: "power2.out" }, 0);\n'
               f'    tl.fromTo("#s1-c", {{ x: 600, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.32, ease: "back.out(1.8)" }}, {rel(0, 0.42)});\n'
               f'    tl.fromTo("#s1-d", {{ y: 80, scale: 0.7, opacity: 0 }}, {{ y: 0, scale: 1, opacity: 1, duration: 0.36, ease: "back.out(2)" }}, {rel(0, 0.62)});\n'
               + enter_exit("#s1-w", d, enter=False))
POPS = [W["s1"][0] + rel(0, 0.42), W["s1"][0] + rel(0, 0.62)]

# S2 logo reveal: the client's gold H logo (portfolio post) in a glowing ring + name + footer tagline
d = d_of("s2")
C["s2"] = comp("s2", f"""    <div id="s2-w" style="position:absolute;inset:0;">
      <div id="s2-glow" style="position:absolute;left:190px;top:250px;width:700px;height:700px;border-radius:50%;background:radial-gradient(circle, rgba(226,184,92,0.45), rgba(226,184,92,0) 68%);"></div>
      <div id="s2-logo" style="position:absolute;left:265px;top:325px;width:550px;height:550px;border-radius:50%;overflow:hidden;border:4px solid {GOLD};box-shadow:0 0 80px rgba(226,184,92,0.5);">
        <img src="assets/img/logo.jpg" style="width:560px;height:552px;margin:-4px 0 0 -6px;" alt="Heaven Developer logo">
        <div id="s2-shine" style="position:absolute;left:-400px;top:-100px;width:160px;height:800px;transform:rotate(20deg);background:linear-gradient(90deg, rgba(255,255,255,0), rgba(255,246,214,0.55), rgba(255,255,255,0));"></div>
      </div>
      <div class="c h gold" id="s2-n" style="top:960px;font-size:118px;">HEAVEN</div>
      <div class="c h" id="s2-n2" style="top:1080px;font-size:74px;letter-spacing:14px;">DEVELOPER</div>
      <div class="c pf" id="s2-t" style="top:1190px;font-size:56px;color:{GREY};">Premium development, <span style="color:{GOLD2};">delivered.</span></div>
    </div>""",
               enter_exit("#s2-w", d, enter=False) +
               '    tl.fromTo("#s2-logo", { scale: 0.3, opacity: 0, rotation: -25 }, { scale: 1, opacity: 1, rotation: 0, duration: 0.6, ease: "back.out(1.6)" }, 0.02);\n'
               '    tl.fromTo("#s2-glow", { scale: 0.4, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.7, ease: "power2.out" }, 0.05);\n'
               '    tl.fromTo("#s2-shine", { x: 0 }, { x: 1100, duration: 0.9, ease: "power2.inOut" }, 0.55);\n'
               f'    tl.fromTo("#s2-n", {{ y: 50, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "power3.out" }}, {rel(1, 0.12)});\n'
               f'    tl.fromTo("#s2-n2", {{ opacity: 0, scaleX: 0.6 }}, {{ opacity: 1, scaleX: 1, duration: 0.4, ease: "power3.out" }}, {rel(1, 0.22)});\n'
               f'    tl.fromTo("#s2-t", {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "power2.out" }}, {rel(1, 0.55)});\n'
               f'    tl.to("#s2-logo", {{ scale: 1.05, duration: {max(0.5, d - 0.9):.2f}, ease: "none" }}, 0.62);\n')
SHIMMER = W["s2"][0] + 0.55

# S3 services: the real #services channel scrolling in a phone frame + the 5 services popping on the right
SERV = [("bot", "Discord Bots"), ("code", "Websites"), ("cube", "Minecraft Plugins"), ("sword", "Minecraft Mods"), ("grid", "Texture Packs")]
d = d_of("s3")
rows = "".join(f'<div class="card" id="s3-k{i}" style="position:absolute;left:540px;top:{360 + i * 172}px;width:500px;height:146px;display:flex;align-items:center;gap:22px;padding-left:22px;">'
               f'{icon(k, 50)}<div style="font-family:PB;font-weight:700;font-size:38px;color:#fff;line-height:1.1;">{n}</div></div>'
               for i, (k, n) in enumerate(SERV))
C["s3"] = comp("s3", f"""    <div id="s3-w" style="position:absolute;inset:0;">
      <div class="c" id="s3-l" style="top:236px;"><span class="lab">OUR SERVICES</span></div>
      <div class="shot" id="s3-ph" style="position:absolute;left:46px;top:330px;width:466px;height:1004px;background:#fff;">
        <video id="s3-v" src="assets/clips/services.mp4" data-start="0" data-duration="{d}" muted playsinline style="width:466px;height:1003px;object-fit:cover;"></video>
      </div>
      {rows}
      <div class="c pf" id="s3-x" style="top:1236px;left:500px;font-size:40px;color:{GREY};">+ Python &amp; Node.js tools</div>
    </div>""",
               enter_exit("#s3-w", d) +
               '    tl.fromTo("#s3-ph", { x: -520, rotation: -8, opacity: 0 }, { x: 0, rotation: 0, opacity: 1, duration: 0.5, ease: "power3.out" }, 0.05);\n'
               + "".join(f'    tl.fromTo("#s3-k{i}", {{ x: 560, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.3, ease: "back.out(1.6)" }}, {rel(2, 0.04 + i * 0.17):.2f});\n'
                         for i in range(len(SERV))) +
               f'    tl.fromTo("#s3-x", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {rel(2, 0.85)});\n')
POPS += [W["s3"][0] + rel(2, 0.04 + i * 0.17) for i in range(len(SERV))]

# S4 Limited Edition Perks prices (owner chose these): label, "STARTING FROM $4", the five starting prices
PR = [("bot", "Discord Bot", "$5"), ("code", "Website", "$4"), ("cube", "Minecraft Plugin", "$4"), ("sword", "Minecraft Mod", "$5"), ("grid", "Texture Pack", "$4")]
d = d_of("s4")
prow = "".join(f'<div class="card" id="s4-r{i}" style="position:absolute;left:110px;top:{780 + i * 104}px;width:860px;height:88px;display:flex;align-items:center;gap:20px;padding:0 30px 0 22px;">'
               f'{icon(k, 40, box=False)}<div style="flex:1;font-family:PS;font-weight:600;font-size:38px;color:#fff;">{n}</div>'
               f'<div style="font-family:JB;font-weight:700;font-size:30px;color:{GREY};">from</div><div class="h gold" style="font-size:50px;width:100px;text-align:right;">{p}</div></div>'
               for i, (k, n, p) in enumerate(PR))
C["s4"] = comp("s4", f"""    <div id="s4-w" style="position:absolute;inset:0;">
      <div class="c" id="s4-l" style="top:290px;"><span class="lab">★ LIMITED EDITION PERKS ★</span></div>
      <div class="c h" id="s4-a" style="top:400px;font-size:66px;letter-spacing:4px;">STARTING FROM</div>
      <div class="c h gold" id="s4-p" style="top:470px;font-size:290px;letter-spacing:-6px;">$4</div>
      {prow}
      <div class="c pf" id="s4-f" style="top:1312px;font-size:36px;color:{GREY};">Final prices depend on scope.</div>
    </div>""",
               enter_exit("#s4-w", d) +
               '    tl.fromTo("#s4-l", { scale: 0.6, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2)" }, 0.08);\n'
               f'    tl.fromTo("#s4-a", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, {max(0.25, rel(3, 0.3) - 0.3):.2f});\n'
               f'    tl.fromTo("#s4-p", {{ scale: 0.2, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.45, ease: "back.out(2.4)" }}, {rel(3, 0.55)});\n'
               f'    tl.to("#s4-p", {{ scale: 1.06, duration: {max(0.5, d - rel(3, 0.55) - 0.7):.2f}, ease: "none" }}, {rel(3, 0.55) + 0.45:.2f});\n'
               + "".join(f'    tl.fromTo("#s4-r{i}", {{ x: {-900 if i % 2 == 0 else 900}, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.3, ease: "power3.out" }}, {0.25 + i * 0.12:.2f});\n'
                         for i in range(len(PR))) +
               f'    tl.fromTo("#s4-f", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {rel(3, 0.8)});\n')
CASH = W["s4"][0] + rel(3, 0.55)

# S5 invite rewards: gift icon, "INVITE 3 FRIENDS = 1 FREE PROJECT", 7 invites line, the real #invite-rewards post
d = d_of("s5")
C["s5"] = comp("s5", f"""    <div id="s5-w" style="position:absolute;inset:0;">
      <div class="c" id="s5-ic" style="top:250px;display:flex;justify-content:center;">{icon("gift", 96)}</div>
      <div class="c" id="s5-l" style="top:420px;"><span class="lab">FREE ACCESS: INVITE REWARDS</span></div>
      <div class="c h" id="s5-a" style="top:520px;font-size:104px;">INVITE <span class="gold">3</span> FRIENDS</div>
      <div class="c h gold" id="s5-b" style="top:650px;font-size:96px;">= 1 FREE PROJECT</div>
      <div class="c" id="s5-c" style="top:790px;font-family:PS;font-weight:600;font-size:42px;color:{GREY};">7 invites = one medium project</div>
      <div class="shot" id="s5-shot" style="position:absolute;left:190px;top:880px;width:700px;height:420px;background:#fff;"><img src="assets/img/invite.jpg" style="width:700px;height:1446px;margin-top:-6px;" alt="Heaven Developer invite rewards post"></div>
    </div>""",
               enter_exit("#s5-w", d) +
               '    tl.fromTo("#s5-ic", { scale: 0.2, opacity: 0, rotation: -30 }, { scale: 1, opacity: 1, rotation: 0, duration: 0.5, ease: "back.out(2.2)" }, 0.05);\n'
               '    tl.to("#s5-ic", { rotation: 8, duration: 0.12, ease: "sine.inOut", yoyo: true, repeat: 4 }, 0.6);\n'
               f'    tl.fromTo("#s5-a", {{ y: 50, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "power3.out" }}, {rel(4, 0.05)});\n'
               f'    tl.fromTo("#s5-b", {{ scale: 0.4, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2)" }}, {rel(4, 0.55)});\n'
               f'    tl.fromTo("#s5-c", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.35 }}, {rel(4, 0.75)});\n'
               f'    tl.fromTo("#s5-shot", {{ y: 300, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "power3.out" }}, 0.25);\n'
               f'    tl.fromTo("#s5-shot img", {{ y: -170 }}, {{ y: -600, duration: {d:.2f}, ease: "sine.inOut" }}, 0);\n')
GIFT = W["s5"][0] + rel(4, 0.55)

# S6 community + proof: member count-up to the profile's 2,521 (skill #425: start at 0, ease out) + the real 5/5 review
d = d_of("s6")
C["s6"] = comp("s6", f"""    <div id="s6-w" style="position:absolute;inset:0;">
      <div class="c h gold" id="s6-n" style="top:270px;font-size:220px;letter-spacing:-4px;">0</div>
      <div class="c h" id="s6-t" style="top:500px;font-size:84px;letter-spacing:10px;">MEMBERS</div>
      <div class="c" id="s6-s" style="top:620px;font-family:PX;font-size:64px;color:{GOLD2};letter-spacing:8px;">★★★★★ <span style="font-family:JB;font-size:44px;color:#fff;letter-spacing:2px;">5/5 CLIENT REVIEW</span></div>
      <div class="shot" id="s6-shot" style="position:absolute;left:205px;top:730px;width:670px;height:580px;background:#fff;"><img src="assets/img/review.jpg" style="width:670px;height:866px;" alt="Heaven Developer client review"></div>
    </div>""",
               enter_exit("#s6-w", d) +
               '    const cnt = { v: 0 };\n'
               '    tl.to(cnt, { v: 2521, duration: 1.3, ease: "power2.out", onUpdate: () => { document.querySelector("#s6-n").textContent = Math.round(cnt.v).toLocaleString("en-US"); } }, 0.1);\n'
               '    tl.fromTo("#s6-n", { scale: 0.7 }, { scale: 1, duration: 1.3, ease: "power2.out" }, 0.1);\n'
               '    tl.fromTo("#s6-t", { opacity: 0, scaleX: 0.6 }, { opacity: 1, scaleX: 1, duration: 0.35, ease: "power3.out" }, 0.3);\n'
               f'    tl.fromTo("#s6-s", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.35 }}, {rel(5, 0.45)});\n'
               f'    tl.fromTo("#s6-shot", {{ y: 260, rotation: 4, opacity: 0 }}, {{ y: 0, rotation: 0, opacity: 1, duration: 0.5, ease: "power3.out" }}, {rel(5, 0.45) + 0.1:.2f});\n'
               f'    tl.fromTo("#s6-shot img", {{ y: 0 }}, {{ y: -280, duration: {max(1, d - rel(5, 0.45)):.2f}, ease: "sine.inOut" }}, {rel(5, 0.45) + 0.2:.2f});\n')
STARS = W["s6"][0] + rel(5, 0.45)

# S7 end card: logo, name, the welcome post's 3 steps, Discord "JOIN" button, plans line; banner behind (blurred)
d = d_of("s7")
STEPS = [("ticket", "Open a ticket"), ("idea", "Share your idea"), ("check", "We deliver")]
steps = "".join(f'<div id="s7-k{i}" style="display:flex;flex-direction:column;align-items:center;gap:14px;width:290px;">{icon(k, 60)}'
                f'<div style="font-family:PB;font-weight:700;font-size:36px;color:#fff;">{n}</div></div>' for i, (k, n) in enumerate(STEPS))
C["s7"] = comp("s7", f"""    <div id="s7-w" style="position:absolute;inset:0;">
      <div id="s7-ph" style="position:absolute;left:-60px;top:1240px;width:1200px;height:566px;background:url(assets/img/banner.jpg) center/cover;filter:blur(10px) brightness(0.45);" data-layout-allow-overflow></div>
      <div style="position:absolute;inset:0;background:linear-gradient(180deg, rgba(7,6,10,0) 50%, rgba(7,6,10,0.6) 75%, rgba(7,6,10,0.9) 100%);"></div>
      <div id="s7-logo" style="position:absolute;left:390px;top:270px;width:300px;height:300px;border-radius:50%;overflow:hidden;border:4px solid {GOLD};box-shadow:0 0 70px rgba(226,184,92,0.5);"><img src="assets/img/logo.jpg" style="width:306px;height:301px;margin:-2px 0 0 -3px;" alt="Heaven Developer logo"></div>
      <div class="c h gold" id="s7-n" style="top:600px;font-size:96px;">HEAVEN DEVELOPER</div>
      <div class="c" id="s7-st" style="top:740px;display:flex;justify-content:center;gap:20px;">{steps}</div>
      <div class="c" id="s7-btn" style="top:1000px;"><span class="btn"><svg viewBox="0 0 24 24" style="width:70px;height:70px;" fill="#fff">{DISCORD}</svg>JOIN ON DISCORD</span></div>
      <div class="c" id="s7-p" style="top:1170px;font-family:JB;font-weight:700;font-size:32px;letter-spacing:3px;color:{GOLD2};">FREE • PAID • PREMIUM PLANS</div>
    </div>""",
               '    tl.fromTo("#s7-w", { scale: 1.12, filter: "blur(14px)", opacity: 0 }, { scale: 1, filter: "blur(0px)", opacity: 1, duration: 0.3, ease: "power3.out" }, 0);\n'
               '    tl.fromTo("#s7-logo", { scale: 0.3, opacity: 0, rotation: -15 }, { scale: 1, opacity: 1, rotation: 0, duration: 0.55, ease: "back.out(1.8)" }, 0.05);\n'
               '    tl.fromTo("#s7-n", { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: "power3.out" }, 0.25);\n'
               + "".join(f'    tl.fromTo("#s7-k{i}", {{ y: 60, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.32, ease: "back.out(2)" }}, {rel(6, 0.02 + i * 0.16):.2f});\n'
                         for i in range(3)) +
               f'    tl.fromTo("#s7-btn", {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.42, ease: "back.out(2.2)" }}, {rel(6, 0.6)});\n'
               f'    tl.to("#s7-btn", {{ scale: 1.06, duration: 0.45, ease: "sine.inOut", yoyo: true, repeat: 5 }}, {rel(6, 0.6) + 0.45:.2f});\n'
               f'    tl.fromTo("#s7-p", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.4 }}, {rel(6, 0.6) + 0.4:.2f});\n'
               f'    tl.fromTo("#s7-ph", {{ scale: 1.0 }}, {{ scale: 1.12, duration: {d}, ease: "none" }}, 0);\n')
STEP_T = [W["s7"][0] + rel(6, 0.02 + i * 0.16) for i in range(3)]

os.makedirs("compositions", exist_ok=True)
for k, v in C.items():
    open(f"compositions/{k}.html", "w").write(v)

divs = [f'      <div id="bg" data-composition-id="bg" data-composition-src="compositions/bg.html" data-start="0" data-duration="{TOTAL}" data-track-index="0" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: 0"></div>']
for k, s, e in SCENES:
    divs.append(f'      <div id="{k}" data-composition-id="{k}" data-composition-src="compositions/{k}.html" data-start="{s}" data-duration="{round(e - s, 3)}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: 1"></div>')

sfx = lambda n: f"assets/sfx/{n}.mp3"
A = []
if os.path.exists("assets/audio/mix.wav"):  # VO + music bed, ducked and loudness-set by mix_vo_music.py
    A.append(("mix", "assets/audio/mix.wav", 0, min(dur("assets/audio/mix.wav"), TOTAL), 1.0, 10, 0))
elif os.path.exists("assets/vo/vo.wav"):
    A.append(("vo", "assets/vo/vo.wav", VO_START, min(dur("assets/vo/vo.wav"), TOTAL - VO_START), 1.0, 10, 0))
A.append(("hit0", sfx("sub-drop"), 0.0, dur(sfx("sub-drop")), 0.35, 13, 0))
for i, (k, s, e) in enumerate(SCENES[1:]):
    A.append((f"wh{i}", sfx("whoosh-fast-0.3s"), round(max(0, s - 0.1), 2), dur(sfx("whoosh-fast-0.3s")), 0.5, 14 + i % 2, 0))
for i, t in enumerate(POPS):
    A.append((f"pop{i}", sfx("pop-high"), round(t, 2), dur(sfx("pop-high")), 0.35, 16 + i % 2, 0))
for i, t in enumerate(STEP_T):
    A.append((f"stp{i}", sfx("click-1"), round(t, 2), dur(sfx("click-1")), 0.45, 22 + i % 2, 0))
A += [("shim", sfx("sparkle"), round(SHIMMER, 2), dur(sfx("sparkle")), 0.4, 18, 0),
      ("cash", sfx("cash-register"), round(CASH, 2), dur(sfx("cash-register")), 0.35, 19, 0),
      ("gift", sfx("sparkle"), round(GIFT, 2), dur(sfx("sparkle")), 0.35, 20, 0),
      ("imp", sfx("impact-boom"), round(STARS, 2), dur(sfx("impact-boom")), 0.3, 21, 0),
      ("ok", sfx("confirm-1"), round(W["s7"][0] + rel(6, 0.6), 2), dur(sfx("confirm-1")), 0.4, 24, 0)]
aud = "\n".join(f'      <audio id="{i}" src="{s}" data-start="{a}" data-duration="{dd}" data-volume="{v}" data-track-index="{ln}"'
                + (f' data-media-start="{ms}"' if ms else "") + "></audio>"
                for i, s, a, dd, v, ln, ms in A)
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
print("built", TOTAL, SCENES)
