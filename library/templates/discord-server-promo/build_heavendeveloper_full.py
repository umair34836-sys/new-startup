# Heaven Developer FULL promo: 9:16, one scene per VO line (24 lines; 2 recordings), every promotional fact in the client's Discord
# server (owner 2026-10-28: "everything cover kro, her ek chote se choti jizz"). Free VoxCPM2 English VO, field voice
# explainer-pro. Facts + frame times: library/clients/heavendeveloper/brief.md; log: edit-log-full-v1.md.
# Same look as build_heavendeveloper.py (black + gold logo, Discord blurple). Needs in the project (scratchpad, never git):
# assets/img/{logo,banner,services,pricing,invite,review,rules,botpost}.jpg, assets/clips/services.mp4, fonts, sfx, gsap,
# assets/audio/mix.wav (mix_vo_music.py), assets/vo/lines.json (per-line [start, end] inside the VO).
import json, os, subprocess

VO_START = 0.35
BG, GOLD, GOLD2, BLURPLE, WHITE, GREY = "#07060a", "#e2b85c", "#f7dc94", "#5865f2", "#ffffff", "#b9b4c4"
L = json.load(open("assets/vo/lines.json"))
VO_END = VO_START + L[-1][1]
TOTAL = round(float(os.environ.get("TOTAL", VO_END + 2.6)), 2)
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


def d_of(i):
    s, e = W[f"s{i + 1}"]
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
    .h {{ font-family: PX; font-weight: 800; line-height: 1.02; letter-spacing: -1px; color: {WHITE}; text-shadow: 0 8px 34px rgba(0,0,0,0.65); }}
    .gold {{ {GOLDTXT} text-shadow: none; filter: drop-shadow(0 6px 22px rgba(226,184,92,0.35)); }}
    .pf {{ font-family: PF; font-style: italic; }}
    .lab {{ display: inline-block; font-family: JB; font-weight: 700; font-size: 30px; letter-spacing: 3px; color: {GOLD2};
            padding: 12px 26px; border: 2px solid rgba(226,184,92,0.55); border-radius: 999px; background: rgba(12,10,16,0.85); }}
    .card {{ background: rgba(16,14,22,0.92); border: 2px solid rgba(226,184,92,0.28); border-left: 8px solid {GOLD}; border-radius: 22px; }}
    .chip {{ display: inline-flex; align-items: center; gap: 14px; font-family: PS; font-weight: 600; font-size: 40px; color: #fff;
             padding: 18px 30px; border-radius: 18px; background: rgba(16,14,22,0.92); border: 2px solid rgba(226,184,92,0.35); }}
    .chip i {{ width: 14px; height: 14px; border-radius: 50%; background: {GOLD}; display: inline-block; }}
    .shot {{ border: 3px solid rgba(226,184,92,0.55); border-radius: 26px; overflow: hidden; box-shadow: 0 30px 90px rgba(0,0,0,0.75), 0 0 60px rgba(226,184,92,0.18); }}
    .btn {{ display: inline-flex; align-items: center; gap: 24px; background: {BLURPLE}; color: #fff; font-family: PX;
            font-weight: 800; border-radius: 22px; padding: 30px 56px; font-size: 56px; box-shadow: 0 18px 60px rgba(88,101,242,0.55); }}
"""

ICON = {
    "bot": '<rect x="4" y="7" width="16" height="12" rx="3"></rect><path d="M12 3v4"></path><circle cx="9" cy="13" r="1.3"></circle><circle cx="15" cy="13" r="1.3"></circle><path d="M2 12v3M22 12v3"></path>',
    "code": '<rect x="2" y="4" width="20" height="16" rx="2"></rect><path d="m9 10-2 2 2 2M15 10l2 2-2 2"></path>',
    "cube": '<path d="M21 16V8l-9-5-9 5v8l9 5 9-5z"></path><path d="M3.3 7.5 12 12l8.7-4.5M12 22V12"></path>',
    "sword": '<path d="M14.5 17.5 3 6V3h3l11.5 11.5"></path><path d="m13 19 6-6M16 16l4 4M19 21l2-2"></path>',
    "grid": '<rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect>',
    "term": '<rect x="2" y="4" width="20" height="16" rx="2"></rect><path d="m6 9 3 3-3 3M12 15h6"></path>',
    "gift": '<rect x="3" y="8" width="18" height="4" rx="1"></rect><path d="M12 8v13M19 12v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7"></path><path d="M7.5 8a2.5 2.5 0 0 1 0-5C11 3 12 8 12 8s1-5 4.5-5a2.5 2.5 0 0 1 0 5"></path>',
    "ticket": '<path d="M3 7a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v3a2 2 0 0 0 0 4v3a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-3a2 2 0 0 0 0-4z"></path><path d="M13 5v14" stroke-dasharray="2 2"></path>',
    "idea": '<path d="M9 18h6M10 22h4"></path><path d="M12 2a7 7 0 0 0-4 12.7V17h8v-2.3A7 7 0 0 0 12 2z"></path>',
    "check": '<circle cx="12" cy="12" r="10"></circle><path d="m8 12 3 3 5-6"></path>',
    "crown": '<path d="M3 18h18M4 18 3 7l5 4 4-7 4 7 5-4-1 11"></path>',
    "shield": '<path d="M12 22s8-4 8-11V5l-8-3-8 3v6c0 7 8 11 8 11z"></path><path d="M9.5 9.5 14.5 14.5M14.5 9.5 9.5 14.5"></path>',
    "users": '<circle cx="9" cy="8" r="4"></circle><path d="M2 21a7 7 0 0 1 14 0"></path><circle cx="17" cy="9" r="3"></circle><path d="M17 15a5 5 0 0 1 5 5"></path>',
    "clock": '<circle cx="12" cy="12" r="10"></circle><path d="M12 6v6l4 2"></path>',
    "star": '<path d="m12 2 3 6.5 7 .9-5.1 4.8 1.3 7L12 17.8 5.8 21.2l1.3-7L2 9.4l7-.9z"></path>',
}
DISCORD = '<path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0 12.64 12.64 0 0 0-.617-1.25.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 0 0 .031.057 19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028c.462-.63.874-1.295 1.226-1.994a.076.076 0 0 0-.041-.106 13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.128 10.2 10.2 0 0 0 .372-.292.074.074 0 0 1 .077-.01c3.929 1.793 8.18 1.793 12.061 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127 12.299 12.299 0 0 1-1.873.894.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.028zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.955-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.946 2.418-2.157 2.418z"></path>'


def icon(k, size=64, box=True, col=GOLD2):
    svg = f'<svg viewBox="0 0 24 24" style="width:{size}px;height:{size}px;" fill="none" stroke="{col}" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">{ICON[k]}</svg>'
    if not box:
        return svg
    return (f'<div style="width:{size + 44}px;height:{size + 44}px;flex:none;border:2px solid rgba(226,184,92,0.5);border-radius:22px;'
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


C, POPS, SPECIAL = {}, [], []


def feature(i, label, ic, title, chips, shot=None, shot_y=0, shot_h=360, title_px=96, gold_title=True, note=None):
    """one VO line = label pill, icon, title, chips popping across the line, optional proof crop of the real post"""
    k = f"s{i + 1}"
    d = d_of(i)
    chip_html = "".join(f'<span class="chip" id="{k}-k{j}"><i></i>{c}</span>' for j, c in enumerate(chips))
    sh = ""
    if shot:
        sh = (f'<div class="shot" id="{k}-shot" style="position:absolute;left:150px;top:{1330 - shot_h}px;width:780px;height:{shot_h}px;background:#fff;">'
              f'<img id="{k}-img" src="assets/img/{shot}" style="position:absolute;left:0;top:{-shot_y}px;width:780px;" alt="Heaven Developer post"></div>')
    nt = f'<div class="c pf" id="{k}-n" style="top:{1330 - shot_h - 70 if shot else 1220}px;font-size:40px;color:{GREY};">{note}</div>' if note else ""
    html = f"""    <div id="{k}-w" style="position:absolute;inset:0;">
      <div class="c" id="{k}-l" style="top:236px;"><span class="lab">{label}</span></div>
      <div class="c" id="{k}-ic" style="top:320px;display:flex;justify-content:center;">{icon(ic, 76)}</div>
      <div class="c h{' gold' if gold_title else ''}" id="{k}-t" style="top:470px;font-size:{title_px}px;">{title}</div>
      <div class="c" id="{k}-ch" style="top:{480 + int(title_px * 1.15 * (title.count('<br>') + 1)) + 30}px;padding:0 70px;display:flex;flex-wrap:wrap;justify-content:center;gap:18px;">{chip_html}</div>
      {nt}{sh}
    </div>"""
    js = enter_exit(f"#{k}-w", d)
    js += f'    tl.fromTo("#{k}-ic", {{ scale: 0.3, opacity: 0, rotation: -20 }}, {{ scale: 1, opacity: 1, rotation: 0, duration: 0.45, ease: "back.out(2)" }}, 0.05);\n'
    js += f'    tl.fromTo("#{k}-t", {{ y: 50, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "power3.out" }}, 0.12);\n'
    n = max(1, len(chips))
    for j in range(len(chips)):
        t = rel(i, 0.18 + 0.72 * j / n)
        js += f'    tl.fromTo("#{k}-k{j}", {{ y: 40, scale: 0.6, opacity: 0 }}, {{ y: 0, scale: 1, opacity: 1, duration: 0.3, ease: "back.out(2)" }}, {t});\n'
        POPS.append(W[k][0] + t)
    if note:
        js += f'    tl.fromTo("#{k}-n", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {rel(i, 0.6)});\n'
    if shot:
        js += f'    tl.fromTo("#{k}-shot", {{ y: 240, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.45, ease: "power3.out" }}, 0.2);\n'
        js += f'    tl.fromTo("#{k}-img", {{ y: 0 }}, {{ y: -60, duration: {d:.2f}, ease: "none" }}, 0);\n'
    C[k] = comp(k, html, js)


# global background
C["bg"] = comp("bg", f"""    <div style="position:absolute;inset:0;background:radial-gradient(120% 80% at 50% 30%, #15111d 0%, {BG} 65%);"></div>
    <div id="bg-g1" style="position:absolute;left:-200px;top:-200px;width:1100px;height:1100px;border-radius:50%;background:radial-gradient(circle, rgba(226,184,92,0.16), rgba(226,184,92,0) 70%);" data-layout-allow-overflow></div>
    <div id="bg-g2" style="position:absolute;left:300px;top:1100px;width:1100px;height:1100px;border-radius:50%;background:radial-gradient(circle, rgba(88,101,242,0.16), rgba(88,101,242,0) 70%);" data-layout-allow-overflow></div>
    <div id="bg-dots" style="position:absolute;left:0;top:0;width:1080px;height:2400px;background-image:radial-gradient(rgba(226,184,92,0.16) 2px, transparent 2.5px);background-size:54px 54px;" data-layout-allow-overflow></div>
    <div id="bg-sw" style="position:absolute;left:-900px;top:-400px;width:500px;height:2800px;transform:rotate(18deg);background:linear-gradient(90deg, rgba(247,220,148,0), rgba(247,220,148,0.07), rgba(247,220,148,0));" data-layout-allow-overflow></div>""",
               f'    tl.fromTo("#bg-dots", {{ y: 0 }}, {{ y: -378, duration: {TOTAL}, ease: "none" }}, 0);\n'
               f'    tl.fromTo("#bg-g1", {{ scale: 0.9, x: 0 }}, {{ scale: 1.25, x: 400, duration: {TOTAL}, ease: "sine.inOut" }}, 0);\n'
               f'    tl.fromTo("#bg-g2", {{ scale: 1.1, x: 0 }}, {{ scale: 0.9, x: -500, duration: {TOTAL}, ease: "sine.inOut" }}, 0);\n'
               f'    tl.fromTo("#bg-sw", {{ x: 0 }}, {{ x: 2600, duration: 6, ease: "none", repeat: {int(TOTAL // 6)} }}, 0);\n')

# 1 hook
d = d_of(0)
C["s1"] = comp("s1", f"""    <div id="s1-w" style="position:absolute;inset:0;">
      <div id="s1-ph" style="position:absolute;left:-60px;top:120px;width:1200px;height:566px;background:url(assets/img/banner.jpg) center/cover;filter:blur(3px) brightness(0.55);" data-layout-allow-overflow></div>
      <div style="position:absolute;inset:0;background:linear-gradient(180deg, rgba(7,6,10,0.2) 0%, rgba(7,6,10,0.85) 38%, rgba(7,6,10,0.96) 100%);"></div>
      <div class="c" style="top:380px;"><span class="lab">DISCORD • WEB • MINECRAFT</span></div>
      <div class="c h" style="top:500px;font-size:120px;">NEED A</div>
      <div class="c h" id="s1-b" style="top:645px;font-size:112px;color:#8f99ff;">DISCORD BOT?</div>
      <div class="c h" id="s1-c" style="top:790px;font-size:132px;">WEBSITE?</div>
      <div class="c h gold" id="s1-d" style="top:940px;font-size:112px;">MINECRAFT<br>PLUGIN?</div>
    </div>""",
               f'    tl.fromTo("#s1-ph", {{ scale: 1.15 }}, {{ scale: 1.0, duration: {d}, ease: "none" }}, 0);\n'
               '    tl.fromTo("#s1-b", { scale: 1.08 }, { scale: 1, duration: 0.9, ease: "power2.out" }, 0);\n'
               f'    tl.fromTo("#s1-c", {{ x: 600, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.32, ease: "back.out(1.8)" }}, {rel(0, 0.42)});\n'
               f'    tl.fromTo("#s1-d", {{ y: 80, scale: 0.7, opacity: 0 }}, {{ y: 0, scale: 1, opacity: 1, duration: 0.36, ease: "back.out(2)" }}, {rel(0, 0.62)});\n'
               + enter_exit("#s1-w", d, enter=False))
POPS += [W["s1"][0] + rel(0, 0.42), W["s1"][0] + rel(0, 0.62)]

# 2 logo
d = d_of(1)
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
               f'    tl.fromTo("#s2-n", {{ y: 50, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "power3.out" }}, {rel(1, 0.3)});\n'
               f'    tl.fromTo("#s2-n2", {{ opacity: 0, scaleX: 0.6 }}, {{ opacity: 1, scaleX: 1, duration: 0.4, ease: "power3.out" }}, {rel(1, 0.38)});\n'
               f'    tl.fromTo("#s2-t", {{ opacity: 0, y: 24 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "power2.out" }}, {rel(1, 0.6)});\n'
               f'    tl.to("#s2-logo", {{ scale: 1.05, duration: {max(0.5, d - 0.9):.2f}, ease: "none" }}, 0.62);\n')
SPECIAL.append(("sparkle", W["s2"][0] + 0.55, 0.4))

# 3-8 services, each with the real #services post panned to that entry (y offsets in services.jpg, 780 px wide)
SY = 780 / 741  # services.jpg is 741 px wide
feature(2, "SERVICE 01 • DISCORD BOTS", "bot", "DISCORD BOTS", ["Moderation", "Tickets", "Economy", "Music", "Custom dashboards"], "services.jpg", int(110 * SY), 300)
feature(3, "SERVICE 02 • WEBSITES", "code", "WEBSITES", ["Portfolios", "Business sites", "Landing pages", "Web apps"], "services.jpg", int(308 * SY), 300)
feature(4, "SERVICE 03 • MINECRAFT", "cube", "MINECRAFT<br>PLUGINS", ["Custom gameplay", "Commands", "GUIs", "Server systems"], "services.jpg", int(505 * SY), 300)
feature(5, "SERVICE 04 • MINECRAFT", "sword", "MINECRAFT<br>MODS", ["Custom items", "Blocks", "Mobs", "Mechanics"], "services.jpg", int(702 * SY), 300)
feature(6, "SERVICE 05 • TEXTURE PACKS", "grid", "TEXTURE PACKS", ["Custom UI", "Items", "Blocks", "Full themes"], "services.jpg", int(900 * SY), 300)
feature(7, "SERVICE 06 • CUSTOM DEV", "term", "CUSTOM<br>DEVELOPMENT", ["Python", "Node.js", "Automation", "APIs", "C++: quoted"], "services.jpg", int(1048 * SY), 300)

# 9 prices (Limited Edition Perks)
PR = [("bot", "Discord Bot", "$5"), ("code", "Website", "$4"), ("cube", "Minecraft Plugin", "$4"), ("sword", "Minecraft Mod", "$5"), ("grid", "Texture Pack", "$4"), ("star", "Custom / C++", "quoted")]
i = 8; k = "s9"; d = d_of(i)
prow = "".join(f'<div class="card" id="{k}-r{j}" style="position:absolute;left:110px;top:{640 + j * 104}px;width:860px;height:88px;display:flex;align-items:center;gap:20px;padding:0 30px 0 22px;">'
               f'{icon(ic, 40, box=False)}<div style="flex:1;font-family:PS;font-weight:600;font-size:38px;color:#fff;">{n}</div>'
               + (f'<div style="font-family:JB;font-weight:700;font-size:30px;color:{GREY};">from</div>' if p != "quoted" else "")
               + f'<div class="h gold" style="font-size:{50 if p != "quoted" else 40}px;min-width:100px;text-align:right;">{p}</div></div>'
               for j, (ic, n, p) in enumerate(PR))
C[k] = comp(k, f"""    <div id="{k}-w" style="position:absolute;inset:0;">
      <div class="c" style="top:250px;"><span class="lab">★ LIMITED EDITION PERKS ★</span></div>
      <div class="c h" style="top:350px;font-size:60px;letter-spacing:4px;">STARTING PRICES (USD)</div>
      <div class="c h gold" id="{k}-p" style="top:430px;font-size:170px;letter-spacing:-4px;">FROM $4</div>
      {prow}
    </div>""",
            enter_exit(f"#{k}-w", d) +
            f'    tl.fromTo("#{k}-p", {{ scale: 0.3, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.45, ease: "back.out(2.2)" }}, {rel(i, 0.72)});\n'
            + "".join(f'    tl.fromTo("#{k}-r{j}", {{ x: {-900 if j % 2 == 0 else 900}, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.3, ease: "power3.out" }}, {rel(i, 0.05 + j * 0.1):.2f});\n'
                      for j in range(len(PR))))
SPECIAL.append(("cash-register", W[k][0] + rel(i, 0.72), 0.35))

# 10 plans
PL = [("gift", "FREE", "Earned through invites, for small projects"), ("ticket", "PAID", "Standard queue, full projects"), ("crown", "PREMIUM", "Priority queue, faster delivery, direct support, free minor revisions")]
i = 9; k = "s10"; d = d_of(i)
pc = "".join(f'<div class="card" id="{k}-p{j}" style="position:absolute;left:90px;top:{470 + j * 260}px;width:900px;height:230px;display:flex;align-items:center;gap:34px;padding:0 36px;{"border-color:rgba(226,184,92,0.8);" if j == 2 else ""}">'
             f'{icon(ic, 64)}<div><div class="h {"gold" if j == 2 else ""}" style="font-size:64px;">{t}</div>'
             f'<div style="font-family:PS;font-weight:600;font-size:34px;color:{GREY};line-height:1.25;margin-top:6px;">{s}</div></div></div>'
             for j, (ic, t, s) in enumerate(PL))
C[k] = comp(k, f"""    <div id="{k}-w" style="position:absolute;inset:0;">
      <div class="c" style="top:250px;"><span class="lab">PLANS</span></div>
      <div class="c h" style="top:330px;font-size:84px;">CHOOSE YOUR PLAN</div>
      {pc}
    </div>""",
            enter_exit(f"#{k}-w", d) +
            "".join(f'    tl.fromTo("#{k}-p{j}", {{ y: 120, opacity: 0, scale: 0.9 }}, {{ y: 0, opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.6)" }}, {rel(i, 0.35 + j * 0.2):.2f});\n'
                    for j in range(3)))
POPS += [W[k][0] + rel(i, 0.35 + j * 0.2) for j in range(3)]

# 11 premium perks
feature(10, "PREMIUM PLAN", "crown", "PREMIUM", ["Priority queue", "Faster delivery", "Direct support", "Free minor revisions"], "pricing.jpg", int(1010 * 780 / 748), 260)

# 12 premium lounge (recording 2, #premium-lounge)
feature(11, "PREMIUM • PRIVATE CHANNEL", "crown", "PREMIUM<br>LOUNGE", ["Premium members only", "Early looks", "Priority talk", "Direct access to the team"], "lounge.jpg", 0, 330, title_px=90)

# 13 ordering flow (#create-ticket "HEAVEN ORDERS & SUPPORT"): 3 steps + the real orders banner
i = 12; k = "s13"; d = d_of(i)
OS = [("check", "1", "Choose"), ("term", "2", "Fill the form"), ("ticket", "3", "Private ticket")]
osteps = "".join(f'<div class="card" id="{k}-k{j}" style="position:absolute;left:90px;top:{430 + j * 190}px;width:900px;height:160px;display:flex;align-items:center;gap:30px;padding:0 36px;">'
                 f'<div class="h gold" style="font-size:90px;width:70px;">{n}</div>{icon(ic, 52)}<div class="h" style="font-size:58px;">{t}</div></div>' for j, (ic, n, t) in enumerate(OS))
C[k] = comp(k, f"""    <div id="{k}-w" style="position:absolute;inset:0;">
      <div class="c" style="top:250px;"><span class="lab">HEAVEN ORDERS &amp; SUPPORT</span></div>
      <div class="c h" style="top:320px;font-size:72px;">ORDERING IS EASY</div>
      {osteps}
      <div class="shot" id="{k}-shot" style="position:absolute;left:110px;top:1010px;width:860px;height:327px;"><img src="assets/img/orders.jpg" style="width:860px;height:327px;" alt="Heaven Developer orders banner"></div>
    </div>""",
            enter_exit(f"#{k}-w", d) +
            "".join(f'    tl.fromTo("#{k}-k{j}", {{ x: {-900 if j % 2 == 0 else 900}, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.35, ease: "power3.out" }}, {rel(i, 0.3 + j * 0.22):.2f});\n' for j in range(3)) +
            f'    tl.fromTo("#{k}-shot", {{ y: 240, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.45, ease: "power3.out" }}, 0.15);\n')
POPS += [W[k][0] + rel(i, 0.3 + j * 0.22) for j in range(3)]

# 16 invite rewards
i = 15; k = "s16"; d = d_of(i)
C[k] = comp(k, f"""    <div id="{k}-w" style="position:absolute;inset:0;">
      <div class="c" style="top:250px;display:flex;justify-content:center;" id="{k}-ic">{icon("gift", 90)}</div>
      <div class="c" style="top:420px;"><span class="lab">FREE ACCESS: INVITE REWARDS</span></div>
      <div class="card" id="{k}-a" style="position:absolute;left:90px;top:520px;width:900px;height:250px;display:flex;align-items:center;gap:36px;padding:0 40px;">
        <div class="h gold" style="font-size:170px;">3</div><div><div class="h" style="font-size:58px;">INVITES</div><div style="font-family:PS;font-size:36px;color:{GREY};line-height:1.25;">one small project: simple bot commands, a single-page site, a small plugin or a texture pack edit</div></div></div>
      <div class="card" id="{k}-b" style="position:absolute;left:90px;top:800px;width:900px;height:200px;display:flex;align-items:center;gap:36px;padding:0 40px;">
        <div class="h gold" style="font-size:150px;">7</div><div><div class="h" style="font-size:58px;">INVITES</div><div style="font-family:PS;font-size:36px;color:{GREY};">one medium project</div></div></div>
      <div class="c pf" id="{k}-n" style="top:1040px;font-size:40px;color:{GREY};">Claim your reward by opening a ticket.</div>
    </div>""",
            enter_exit(f"#{k}-w", d) +
            f'    tl.fromTo("#{k}-ic", {{ scale: 0.2, opacity: 0, rotation: -30 }}, {{ scale: 1, opacity: 1, rotation: 0, duration: 0.5, ease: "back.out(2.2)" }}, 0.05);\n'
            f'    tl.fromTo("#{k}-a", {{ x: -900, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.4, ease: "power3.out" }}, {rel(i, 0.1)});\n'
            f'    tl.fromTo("#{k}-b", {{ x: 900, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.4, ease: "power3.out" }}, {rel(i, 0.62)});\n'
            f'    tl.fromTo("#{k}-n", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {rel(i, 0.8)});\n')
SPECIAL += [("sparkle", W[k][0] + rel(i, 0.1), 0.35), ("pop-high", W[k][0] + rel(i, 0.62), 0.35)]

# 17 invite tracker buttons (#invite-rewards)
feature(16, "INVITE TRACKER", "users", "TRACK YOUR<br>INVITES", ["My progress", "My invite link", "Leaderboard"], "invite.jpg", int(1340 * 780 / 748), 210, title_px=96)

# 18 how invites count: three stat tiles
i = 17; k = "s18"; d = d_of(i)
TL = [("clock", "7 DAYS", "invited member stays at least"), ("users", "30 DAYS", "account at least this old"), ("shield", "NO ALTS", "fake or alt accounts are disqualified")]
tiles = "".join(f'<div class="card" id="{k}-t{j}" style="position:absolute;left:90px;top:{460 + j * 250}px;width:900px;height:220px;display:flex;align-items:center;gap:34px;padding:0 36px;">'
                f'{icon(ic, 64)}<div><div class="h gold" style="font-size:80px;">{t}</div><div style="font-family:PS;font-size:34px;color:{GREY};">{s}</div></div></div>'
                for j, (ic, t, s) in enumerate(TL))
C[k] = comp(k, f"""    <div id="{k}-w" style="position:absolute;inset:0;">
      <div class="c" style="top:250px;"><span class="lab">HOW INVITES COUNT</span></div>
      <div class="c h" style="top:330px;font-size:76px;">FAIR RULES</div>
      {tiles}
    </div>""",
            enter_exit(f"#{k}-w", d) +
            "".join(f'    tl.fromTo("#{k}-t{j}", {{ scale: 0.6, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2)" }}, {rel(i, 0.1 + j * 0.3):.2f});\n'
                    for j in range(3)))
POPS += [W[k][0] + rel(i, 0.1 + j * 0.3) for j in range(3)]

# 14 quote in ticket
feature(13, "BEFORE WORK BEGINS", "ticket", "A QUOTE IN YOUR<br>TICKET FIRST", ["Every order", "Quoted before work begins", "Final price depends on scope"], "pricing.jpg", int(1190 * 780 / 748), 250, title_px=84)

# 15 support option in the order menu
feature(14, "ALREADY A CLIENT?", "check", "SUPPORT", ["Help with an existing project", "Pick it in the order menu"], "dropdown.jpg", 560, 360, title_px=110)

# 20 safety
feature(19, "SERVER RULES • SAFETY", "shield", "STAFF NEVER ASK<br>FOR PASSWORDS", ["No passwords", "No tokens", "Orders stay in tickets", "Honest invites only"], "rules.jpg", int(430 * 780 / 743), 300, title_px=84)

# 19 security: verify to enter + honeypot channel
i = 18; k = "s19"; d = d_of(i)
C[k] = comp(k, f"""    <div id="{k}-w" style="position:absolute;inset:0;">
      <div class="c" style="top:250px;"><span class="lab">SAFETY FIRST</span></div>
      <div class="c" style="top:330px;display:flex;justify-content:center;">{icon("shield", 80)}</div>
      <div class="c h gold" style="top:470px;font-size:80px;">VERIFY TO ENTER</div>
      <div class="shot" id="{k}-a" style="position:absolute;left:90px;top:580px;width:430px;height:350px;background:#fff;"><img src="assets/img/verify.jpg" style="width:430px;" alt="verify post"></div>
      <div class="shot" id="{k}-b" style="position:absolute;left:560px;top:580px;width:430px;height:350px;background:#fff;"><img src="assets/img/honeypot.jpg" style="width:430px;" alt="honeypot post"></div>
      <div class="c h" id="{k}-t" style="top:980px;font-size:66px;">HONEYPOT vs BAD BOTS</div>
      <div class="c" id="{k}-s" style="top:1080px;font-family:PS;font-size:38px;color:{GREY};padding:0 90px;">Post there: message deleted, recent messages bulk-removed, banned.</div>
    </div>""",
            enter_exit(f"#{k}-w", d) +
            f'    tl.fromTo("#{k}-a", {{ x: -600, rotation: -6, opacity: 0 }}, {{ x: 0, rotation: 0, opacity: 1, duration: 0.45, ease: "power3.out" }}, {rel(i, 0.15)});\n'
            f'    tl.fromTo("#{k}-b", {{ x: 600, rotation: 6, opacity: 0 }}, {{ x: 0, rotation: 0, opacity: 1, duration: 0.45, ease: "power3.out" }}, {rel(i, 0.55)});\n'
            f'    tl.fromTo("#{k}-t", {{ scale: 0.6, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2)" }}, {rel(i, 0.6)});\n'
            f'    tl.fromTo("#{k}-s", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {rel(i, 0.75)});\n')
SPECIAL.append(("impact-boom", W[k][0] + rel(i, 0.6), 0.25))

# 21 the Heaven bot
i = 20; k = "s21"; d = d_of(i)
C[k] = comp(k, f"""    <div id="{k}-w" style="position:absolute;inset:0;">
      <div class="c" style="top:250px;"><span class="lab">@HEAVEN • BOT PORTFOLIO</span></div>
      <div id="{k}-logo" style="position:absolute;left:390px;top:340px;width:300px;height:300px;border-radius:50%;overflow:hidden;border:4px solid {GOLD};box-shadow:0 0 70px rgba(226,184,92,0.5);"><img src="assets/img/logo.jpg" style="width:306px;height:301px;margin:-2px 0 0 -3px;" alt="Heaven bot"></div>
      <div class="c h gold" id="{k}-t" style="top:680px;font-size:84px;">THE OFFICIAL BOT</div>
      <div class="c" id="{k}-s" style="top:790px;font-family:PS;font-size:42px;color:#fff;">All services from A to Z • welcome to leave</div>
      <div class="shot" id="{k}-shot" style="position:absolute;left:150px;top:880px;width:780px;height:450px;background:#fff;"><img src="assets/img/botpost.jpg" style="width:780px;" alt="Heaven bot portfolio post"></div>
    </div>""",
            enter_exit(f"#{k}-w", d) +
            f'    tl.fromTo("#{k}-logo", {{ scale: 0.3, opacity: 0, rotation: -15 }}, {{ scale: 1, opacity: 1, rotation: 0, duration: 0.5, ease: "back.out(1.8)" }}, 0.05);\n'
            f'    tl.fromTo("#{k}-t", {{ y: 40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35 }}, {rel(i, 0.15)});\n'
            f'    tl.fromTo("#{k}-s", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {rel(i, 0.55)});\n'
            f'    tl.fromTo("#{k}-shot", {{ y: 240, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.45, ease: "power3.out" }}, 0.3);\n')
SPECIAL.append(("sparkle", W[k][0] + 0.1, 0.35))

# 22 review
i = 21; k = "s22"; d = d_of(i)
C[k] = comp(k, f"""    <div id="{k}-w" style="position:absolute;inset:0;">
      <div class="c" style="top:250px;"><span class="lab">CLIENT REVIEW</span></div>
      <div class="c" id="{k}-st" style="top:330px;font-family:PX;font-size:120px;color:{GOLD2};letter-spacing:10px;">★★★★★</div>
      <div class="c h gold" id="{k}-n" style="top:480px;font-size:130px;">5/5</div>
      <div class="shot" id="{k}-shot" style="position:absolute;left:205px;top:660px;width:670px;height:680px;background:#fff;"><img src="assets/img/review.jpg" style="width:670px;" alt="Heaven Developer client review"></div>
    </div>""",
            enter_exit(f"#{k}-w", d) +
            f'    tl.fromTo("#{k}-st", {{ scale: 0.3, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.45, ease: "back.out(2.4)" }}, 0.08);\n'
            f'    tl.fromTo("#{k}-n", {{ y: 40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35 }}, {rel(i, 0.3)});\n'
            f'    tl.fromTo("#{k}-shot", {{ y: 260, rotation: 4, opacity: 0 }}, {{ y: 0, rotation: 0, opacity: 1, duration: 0.5, ease: "power3.out" }}, 0.25);\n')
SPECIAL.append(("impact-boom", W[k][0] + 0.08, 0.3))

# 23 members + boosts (count-up, skill #425)
i = 22; k = "s23"; d = d_of(i)
C[k] = comp(k, f"""    <div id="{k}-w" style="position:absolute;inset:0;">
      <div class="c" style="top:300px;display:flex;justify-content:center;">{icon("users", 90)}</div>
      <div class="c h gold" id="{k}-n" style="top:470px;font-size:230px;letter-spacing:-4px;">0</div>
      <div class="c h" style="top:710px;font-size:90px;letter-spacing:10px;">MEMBERS</div>
      <div class="c" id="{k}-b" style="top:860px;display:flex;justify-content:center;gap:24px;">
        <span class="chip"><i style="background:#f47fff;"></i>17 Boosts</span><span class="chip"><i style="background:#f47fff;"></i>Level 3</span><span class="chip"><i></i>Tag HD</span></div>
    </div>""",
            enter_exit(f"#{k}-w", d) +
            '    const cnt = { v: 0 };\n'
            f'    tl.to(cnt, {{ v: 2521, duration: 1.3, ease: "power2.out", onUpdate: () => {{ document.querySelector("#{k}-n").textContent = Math.round(cnt.v).toLocaleString("en-US"); }} }}, 0.1);\n'
            f'    tl.fromTo("#{k}-n", {{ scale: 0.7 }}, {{ scale: 1, duration: 1.3, ease: "power2.out" }}, 0.1);\n'
            f'    tl.fromTo("#{k}-b", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.4 }}, {rel(i, 0.6)});\n')

# 24 end card
i = 23; k = "s24"; d = d_of(i)
STEPS = [("ticket", "Open a ticket"), ("idea", "Share your idea"), ("check", "We deliver")]
steps = "".join(f'<div id="{k}-k{j}" style="display:flex;flex-direction:column;align-items:center;gap:14px;width:290px;">{icon(ic, 60)}'
                f'<div style="font-family:PB;font-weight:700;font-size:36px;color:#fff;">{n}</div></div>' for j, (ic, n) in enumerate(STEPS))
C[k] = comp(k, f"""    <div id="{k}-w" style="position:absolute;inset:0;">
      <div id="{k}-ph" style="position:absolute;left:-60px;top:1240px;width:1200px;height:566px;background:url(assets/img/banner.jpg) center/cover;filter:blur(10px) brightness(0.45);" data-layout-allow-overflow></div>
      <div id="{k}-logo" style="position:absolute;left:390px;top:270px;width:300px;height:300px;border-radius:50%;overflow:hidden;border:4px solid {GOLD};box-shadow:0 0 70px rgba(226,184,92,0.5);"><img src="assets/img/logo.jpg" style="width:306px;height:301px;margin:-2px 0 0 -3px;" alt="Heaven Developer logo"></div>
      <div class="c h gold" id="{k}-n" style="top:605px;font-size:86px;">HEAVEN DEVELOPER</div>
      <div class="c" style="top:740px;display:flex;justify-content:center;gap:20px;">{steps}</div>
      <div class="c" id="{k}-btn" style="top:1000px;"><span class="btn"><svg viewBox="0 0 24 24" style="width:70px;height:70px;" fill="#fff">{DISCORD}</svg>JOIN ON DISCORD</span></div>
      <div class="c" id="{k}-url" style="top:1160px;"><span class="lab" style="font-size:44px;padding:16px 36px;color:#fff;">discord.gg/<span style="color:{GOLD2};">heavendeveloper</span></span></div>
      <div class="c" id="{k}-p" style="top:1270px;font-family:JB;font-weight:700;font-size:32px;letter-spacing:3px;color:{GOLD2};">FREE • PAID • PREMIUM PLANS</div>
    </div>""",
            f'    tl.fromTo("#{k}-w", {{ scale: 1.12, filter: "blur(14px)", opacity: 0 }}, {{ scale: 1, filter: "blur(0px)", opacity: 1, duration: 0.3, ease: "power3.out" }}, 0);\n'
            f'    tl.fromTo("#{k}-logo", {{ scale: 0.3, opacity: 0, rotation: -15 }}, {{ scale: 1, opacity: 1, rotation: 0, duration: 0.55, ease: "back.out(1.8)" }}, 0.05);\n'
            f'    tl.fromTo("#{k}-n", {{ y: 40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "power3.out" }}, 0.25);\n'
            + "".join(f'    tl.fromTo("#{k}-k{j}", {{ y: 60, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.32, ease: "back.out(2)" }}, {rel(i, 0.02 + j * 0.16):.2f});\n' for j in range(3)) +
            f'    tl.fromTo("#{k}-btn", {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.42, ease: "back.out(2.2)" }}, {rel(i, 0.6)});\n'
            f'    tl.to("#{k}-btn", {{ scale: 1.06, duration: 0.45, ease: "sine.inOut", yoyo: true, repeat: 5 }}, {rel(i, 0.6) + 0.45:.2f});\n'
            f'    tl.fromTo("#{k}-url", {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2.2)" }}, {rel(i, 0.6) + 0.3:.2f});\n'
            f'    tl.fromTo("#{k}-p", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.4 }}, {rel(i, 0.6) + 0.6:.2f});\n'
            f'    tl.fromTo("#{k}-ph", {{ scale: 1.0 }}, {{ scale: 1.12, duration: {d}, ease: "none" }}, 0);\n')
STEP_T = [W[k][0] + rel(i, 0.02 + j * 0.16) for j in range(3)]
SPECIAL.append(("confirm-1", W[k][0] + rel(i, 0.6), 0.4))

os.makedirs("compositions", exist_ok=True)
for kk, v in C.items():
    open(f"compositions/{kk}.html", "w").write(v)
divs = [f'      <div id="bg" data-composition-id="bg" data-composition-src="compositions/bg.html" data-start="0" data-duration="{TOTAL}" data-track-index="0" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: 0"></div>']
for kk, s, e in SCENES:
    divs.append(f'      <div id="{kk}" data-composition-id="{kk}" data-composition-src="compositions/{kk}.html" data-start="{s}" data-duration="{round(e - s, 3)}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: 1"></div>')
sfx = lambda n: f"assets/sfx/{n}.mp3"
A = [("mix", "assets/audio/mix.wav", 0, min(dur("assets/audio/mix.wav"), TOTAL), 1.0, 10),
     ("hit0", sfx("sub-drop"), 0.0, dur(sfx("sub-drop")), 0.35, 11)]
for j, (kk, s, e) in enumerate(SCENES[1:]):
    A.append((f"wh{j}", sfx("whoosh-fast-0.3s"), round(max(0, s - 0.1), 2), dur(sfx("whoosh-fast-0.3s")), 0.45, 12 + j % 2))
for j, t in enumerate(POPS):
    A.append((f"pop{j}", sfx("pop-high"), round(t, 2), dur(sfx("pop-high")), 0.3, 14 + j % 3))
for j, t in enumerate(STEP_T):
    A.append((f"stp{j}", sfx("click-1"), round(t, 2), dur(sfx("click-1")), 0.45, 17 + j % 2))
for j, (n, t, v) in enumerate(SPECIAL):
    A.append((f"fx{j}", sfx(n), round(t, 2), dur(sfx(n)), v, 19 + j % 3))
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
print("built", TOTAL, len(SCENES), "scenes")
