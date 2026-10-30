# HostLixo 9:16 30 s Minecraft-hosting promo (free VoxCPM2 Hindi VO, designed "hostlixo-promo" voice). 2026-10-27.
# Based on build_pakwebhoster.py (scene starts = VO line starts from assets/vo/lines.json).
# Every on-screen claim is quoted from hostlixo.in read in Playwright on 2026-10-27 (library/clients/hostlixo/site-data.md):
# "Minecraft Server Hosting in India from ₹90/mo", "Starting price per month", "9 Plans", "2–32 GB DDR5 ECC RAM" [/];
# "Enterprise L3/L4 DDoS Protection", "2 Automated Backup Allocation", "Order on Discord" [/minecraft.html];
# software Vanilla, Paper, Purpur, Spigot, Fabric, Forge, NeoForge [/support.html]; "24-Hour Refund Policy" [footer];
# "24-HOUR MONEY-BACK GUARANTEE" [/terms.html]; payment badges VISA MASTERCARD UPI PAYTM CRYPTO [footer].
# Visual language = the site's own: black #050505 cards, white text, #999 secondary, thin white borders, Space Grotesk 700
# headings, Plus Jakarta Sans body, JetBrains Mono uppercase pill labels, white primary button; icons are the site's
# own inline SVGs (shield-check, server, box, Discord). Images: site logo/mark, /images/mc_*.jpg, real page screenshots.
# Needs in the project (scratchpad, never git): assets/img/{logo.png,hero-logo.png,mc_world.jpg,mc_1.jpg,mc_2.jpg,
# plans-grid.jpg,feat-ddos.jpg,refund.jpg} (library/clients/hostlixo/site/tools/shots.js), assets/fonts (library/fonts),
# assets/sfx, assets/music/music.mp3, assets/vo/{vo.wav,lines.json}.
import json, os, subprocess

VO_START = 0.35
BG, CARD, WHITE, GREY, MUTED = "#050505", "#0c0c0c", "#ffffff", "#999999", "#5e5e5e"
if os.path.exists("assets/vo/lines.json"):
    L = json.load(open("assets/vo/lines.json"))           # [[start, end], ...] per script line inside vo.wav
else:  # layout preview before the VO exists
    L = [[0, 1.8], [2.3, 5.4], [5.9, 8.6], [9.1, 12.4], [12.9, 15.3], [15.8, 18.6], [19.1, 23.0]]
VO_END = VO_START + L[-1][1]
TOTAL = float(os.environ.get("TOTAL", 30.0))  # owner asked for 30 s
st = [round(VO_START + a - 0.12, 2) for a, _ in L]
st[0] = 0.0
SCENES = [(f"s{i + 1}", st[i], st[i + 1] if i + 1 < len(st) else TOTAL) for i in range(len(st))]
W = {k: (s, e) for k, s, e in SCENES}
MUSIC_FROM = 12.89  # first drop of the track (listen.py hits/sections, 2026-10-27)


def dur(p):
    return round(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                      capture_output=True, text=True).stdout), 3)


def rel(i, frac):
    a, b = L[i]
    return round(max(0.05, VO_START + a + frac * (b - a) - st[i]), 2)


def d_of(k):
    s, e = W[k]
    return round(e - s, 2)


CSS = f"""
    @font-face {{ font-family: "SG"; src: url("assets/fonts/SpaceGrotesk-Variable.ttf"); font-weight: 300 700; }}
    @font-face {{ font-family: "PJ"; src: url("assets/fonts/PlusJakartaSans-Variable.ttf"); font-weight: 200 800; }}
    @font-face {{ font-family: "JB"; src: url("assets/fonts/JetBrainsMono-Variable.ttf"); font-weight: 100 800; }}
    #root {{ position: absolute; inset: 0; overflow: hidden; }}
    .c {{ position: absolute; left: 0; right: 0; text-align: center; }}
    .sg {{ font-family: SG; font-weight: 700; letter-spacing: -2px; line-height: 0.98; color: {WHITE}; text-shadow: 0 6px 30px rgba(0,0,0,0.6); }}
    .pj {{ font-family: PJ; }}
    .lab {{ display: inline-block; font-family: JB; font-weight: 700; font-size: 30px; letter-spacing: 3px; color: {WHITE};
            padding: 12px 24px; border: 2px solid rgba(255,255,255,0.32); border-radius: 8px; background: rgba(10,10,10,0.85); }}
    .lab.w {{ background: {WHITE}; color: #080808; border-color: {WHITE}; }}
    .card {{ background: {CARD}; border: 2px solid rgba(255,255,255,0.16); border-radius: 24px; }}
    .shot {{ border: 2px solid rgba(255,255,255,0.32); border-radius: 22px; overflow: hidden; box-shadow: 0 30px 90px rgba(0,0,0,0.7); }}
    .btn {{ display: inline-flex; align-items: center; gap: 22px; background: {WHITE}; color: #080808; font-family: PJ;
            font-weight: 800; border-radius: 16px; padding: 28px 52px; font-size: 58px; }}
"""

# the site's own inline SVG icons (hostlixo.in, 2026-10-27)
ICON = {
    "shield": '<path d="M12 22s8-4 8-11V5l-8-3-8 3v6c0 7 8 11 8 11z"></path><path d="m9 12 2 2 4-4"></path>',
    "server": '<rect x="2" y="2" width="20" height="8" rx="2"></rect><rect x="2" y="14" width="20" height="8" rx="2"></rect><line x1="6" y1="6" x2="6.01" y2="6"></line><line x1="6" y1="18" x2="6.01" y2="18"></line>',
    "box": '<path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line>',
}
DISCORD = '<path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0 12.64 12.64 0 0 0-.617-1.25.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 0 0 .031.057 19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028c.462-.63.874-1.295 1.226-1.994a.076.076 0 0 0-.041-.106 13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.128 10.2 10.2 0 0 0 .372-.292.074.074 0 0 1 .077-.01c3.929 1.793 8.18 1.793 12.061 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127 12.299 12.299 0 0 1-1.873.894.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.028zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.955-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.946 2.418-2.157 2.418z"></path>'


def icon(k, size=96):
    return (f'<div style="width:{size + 48}px;height:{size + 48}px;flex:none;border:2px solid rgba(255,255,255,0.32);border-radius:18px;'
            f'display:flex;align-items:center;justify-content:center;background:#111;">'
            f'<svg viewBox="0 0 24 24" style="width:{size}px;height:{size}px;" fill="none" stroke="#fff" stroke-width="2">{ICON[k]}</svg></div>')


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


def photo_bg(key, img, d, dim=0.55, z0=1.0, z1=1.12, blur=0):
    """full-bleed site image with a slow push-in and a dark veil (site look: black, white type)"""
    html = (f'<div id="{key}-ph" style="position:absolute;inset:0;background:url(assets/img/{img}) center/cover;filter:blur({blur}px);"></div>'
            f'<div style="position:absolute;inset:0;background:linear-gradient(180deg, rgba(5,5,5,{dim}) 0%, rgba(5,5,5,{dim - 0.2}) 40%, rgba(5,5,5,0.92) 100%);"></div>')
    js = f'    tl.fromTo("#{key}-ph", {{ scale: {z0} }}, {{ scale: {z1}, duration: {d}, ease: "none" }}, 0);\n'
    return html, js


C = {}
# global background: the site's #050505 with its faint white grid lines and a soft white glow
C["bg"] = comp("bg", f"""    <div style="position:absolute;inset:0;background:{BG};"></div>
    <div id="bg-g1" style="position:absolute;left:240px;top:-300px;width:1100px;height:1100px;border-radius:50%;background:radial-gradient(circle, rgba(255,255,255,0.09), rgba(255,255,255,0) 70%);" data-layout-allow-overflow></div>
    <div id="bg-grid" style="position:absolute;left:0;top:0;width:1080px;height:2200px;background-image:linear-gradient(rgba(255,255,255,0.05) 2px, transparent 2px),linear-gradient(90deg, rgba(255,255,255,0.05) 2px, transparent 2px);background-size:72px 72px;" data-layout-allow-overflow></div>""",
               f'    tl.fromTo("#bg-grid", {{ y: 0 }}, {{ y: -216, duration: {TOTAL}, ease: "none" }}, 0);\n'
               f'    tl.fromTo("#bg-g1", {{ scale: 0.9, x: 0 }}, {{ scale: 1.25, x: -300, duration: {TOTAL}, ease: "sine.inOut" }}, 0);\n')

# S1 hook over the site's own Minecraft world image (on screen at 0 s = thumbnail)
d = d_of("s1")
ph, phjs = photo_bg("s1", "mc_world.jpg", d, dim=0.68, z0=1.18, z1=1.05)
C["s1"] = comp("s1", f"""    <div id="s1-w" style="position:absolute;inset:0;">
      {ph}
      <div class="c" id="s1-l" style="top:430px;"><span class="lab">● MINECRAFT HOSTING • INDIA</span></div>
      <div class="c sg" id="s1-a" style="top:560px;font-size:150px;">APNA</div>
      <div class="c sg" id="s1-b" style="top:710px;font-size:168px;">MINECRAFT</div>
      <div class="c sg" id="s1-c" style="top:880px;font-size:168px;">SERVER?</div>
    </div>""",
               phjs +
               '    tl.fromTo("#s1-b", { scale: 1.06 }, { scale: 1, duration: 1.2, ease: "power2.out" }, 0);\n'
               f'    tl.fromTo("#s1-c", {{ y: 70, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "back.out(2)" }}, {rel(0, 0.55)});\n'
               + enter_exit("#s1-w", d, enter=False))

# S2 logo + "from ₹90/mo"
d = d_of("s2")
C["s2"] = comp("s2", f"""    <div id="s2-w" style="position:absolute;inset:0;">
      <div class="c" id="s2-logo" style="top:420px;"><img src="assets/img/logo.png" style="width:760px;height:250px;" alt="HostLixo logo"></div>
      <div class="c" id="s2-lab" style="top:760px;"><span class="lab">STARTING PRICE PER MONTH</span></div>
      <div class="c sg" id="s2-p" style="top:860px;font-size:300px;letter-spacing:-8px;">₹90<span style="font-size:110px;color:{GREY};letter-spacing:0;">/mo</span></div>
      <div class="c pj" id="s2-s" style="top:1180px;font-weight:600;font-size:46px;color:{GREY};">Minecraft Server Hosting in India</div>
    </div>""",
               enter_exit("#s2-w", d) +
               '    tl.fromTo("#s2-logo", { scale: 0.5, opacity: 0, filter: "blur(20px)" }, { scale: 1, opacity: 1, filter: "blur(0px)", duration: 0.5, ease: "back.out(1.6)" }, 0.08);\n'
               f'    tl.fromTo("#s2-lab", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, {max(0.3, rel(1, 0.35) - 0.25):.2f});\n'
               f'    tl.fromTo("#s2-p", {{ scale: 0.2, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.45, ease: "back.out(2.2)" }}, {rel(1, 0.45)});\n'
               f'    tl.to("#s2-p", {{ scale: 1.07, duration: {max(0.5, d - rel(1, 0.45) - 0.7):.2f}, ease: "none" }}, {rel(1, 0.45) + 0.45:.2f});\n'
               f'    tl.fromTo("#s2-s", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {rel(1, 0.5)});\n')

# S3 real plans grid screenshot scrolling + "9 PLANS" / "2–32 GB DDR5 ECC RAM"
d = d_of("s3")
C["s3"] = comp("s3", f"""    <div id="s3-w" style="position:absolute;inset:0;">
      <div class="shot" style="position:absolute;left:70px;top:300px;width:940px;height:1000px;background:#080808;">
        <div style="position:relative;z-index:2;background:#080808;height:64px;border-bottom:2px solid rgba(255,255,255,0.16);display:flex;align-items:center;gap:12px;padding-left:24px;">
          <span style="width:16px;height:16px;border-radius:50%;background:#5e5e5e;"></span><span style="width:16px;height:16px;border-radius:50%;background:#5e5e5e;"></span><span style="width:16px;height:16px;border-radius:50%;background:#5e5e5e;"></span>
          <span style="margin-left:24px;font-family:JB;font-size:30px;color:{GREY};">hostlixo.in/minecraft</span></div>
        <img id="s3-img" src="assets/img/plans-grid.jpg" style="position:absolute;left:0;top:64px;width:940px;height:1307px;" alt="HostLixo Minecraft plans">
      </div>
      <div class="c" id="s3-a" style="top:1330px;"><span class="lab w" style="font-size:44px;padding:16px 34px;">9 PLANS</span></div>
      <div class="c sg" id="s3-b" style="top:1430px;font-size:76px;letter-spacing:-1px;">2–32 GB DDR5 ECC RAM</div>
    </div>""",
               enter_exit("#s3-w", d) +
               f'    tl.fromTo("#s3-img", {{ y: 0 }}, {{ y: -370, duration: {d:.2f}, ease: "sine.inOut" }}, 0);\n'
               f'    tl.fromTo("#s3-a", {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2.4)" }}, {rel(2, 0.05)});\n'
               f'    tl.fromTo("#s3-b", {{ y: 40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "power3.out" }}, {rel(2, 0.3)});\n')
POPS = [W["s3"][0] + rel(2, 0.05)]


def feature_row(key, i, ic, title, sub, top):
    return (f'<div class="card" id="{key}-c{i}" style="position:absolute;left:90px;top:{top}px;width:900px;height:210px;display:flex;align-items:center;gap:40px;padding-left:44px;">'
            f'{icon(ic, 72)}<div><div class="pj" style="font-weight:800;font-size:52px;color:#fff;line-height:1.1;">{title}</div>'
            f'<div style="font-family:JB;font-weight:700;font-size:28px;letter-spacing:2px;color:{GREY};margin-top:10px;">{sub}</div></div></div>')


# S4 site's own DDoS feature card + DDoS / backups rows
d = d_of("s4")
C["s4"] = comp("s4", f"""    <div id="s4-w" style="position:absolute;inset:0;">
      <div class="c" style="top:330px;"><span class="lab">EVERY PLAN INCLUDES</span></div>
      <div class="shot" id="s4-shot" style="position:absolute;left:90px;top:440px;width:900px;height:506px;"><img src="assets/img/feat-ddos.jpg" style="width:900px;height:506px;" alt="HostLixo DDoS feature card"></div>
      {feature_row("s4", 0, "shield", "Enterprise L3/L4", "DDOS PROTECTION", 990)}
      {feature_row("s4", 1, "server", "2 Automated Backups", "PER PLAN", 1230)}
    </div>""",
               enter_exit("#s4-w", d) +
               '    tl.fromTo("#s4-shot", { y: 80, opacity: 0, rotationX: 18 }, { y: 0, opacity: 1, rotationX: 0, duration: 0.5, ease: "power3.out" }, 0.05);\n'
               f'    tl.fromTo("#s4-c0", {{ x: -900, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.4, ease: "power3.out" }}, {rel(3, 0.2)});\n'
               f'    tl.fromTo("#s4-c1", {{ x: 900, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.4, ease: "power3.out" }}, {rel(3, 0.62)});\n')
POPS += [W["s4"][0] + rel(3, 0.2), W["s4"][0] + rel(3, 0.62)]

# S5 server software over the site's castle image
SOFT = ["Paper", "Purpur", "Spigot", "Fabric", "Forge", "NeoForge", "Vanilla"]
d = d_of("s5")
ph, phjs = photo_bg("s5", "mc_1.jpg", d, dim=0.6, z0=1.05, z1=1.18)
chips = "".join(f'<div class="card pj" id="s5-k{i}" style="position:absolute;left:{110 + (i % 2) * 450}px;top:{690 + (i // 2) * 150}px;width:410px;height:120px;'
                f'display:flex;align-items:center;justify-content:center;font-weight:800;font-size:52px;color:#fff;background:rgba(12,12,12,0.88);">{n}</div>'
                for i, n in enumerate(SOFT))
C["s5"] = comp("s5", f"""    <div id="s5-w" style="position:absolute;inset:0;">
      {ph}
      <div class="c" id="s5-ic" style="top:330px;display:flex;justify-content:center;">{icon("box", 84)}</div>
      <div class="c sg" id="s5-t" style="top:510px;font-size:92px;">SERVER SOFTWARE</div>
      {chips}
    </div>""",
               phjs + enter_exit("#s5-w", d) +
               '    tl.fromTo("#s5-ic", { scale: 0.3, opacity: 0, rotation: -20 }, { scale: 1, opacity: 1, rotation: 0, duration: 0.45, ease: "back.out(2)" }, 0.05);\n'
               + "".join(f'    tl.fromTo("#s5-k{i}", {{ y: 60, scale: 0.6, opacity: 0 }}, {{ y: 0, scale: 1, opacity: 1, duration: 0.3, ease: "back.out(2)" }}, {rel(4, 0.1) + i * 0.16:.2f});\n'
                         for i in range(len(SOFT))))
POPS += [W["s5"][0] + rel(4, 0.1) + i * 0.16 for i in (0, 2, 4, 6)]

# S6 24-hour refund: real terms-page badge + headline, big "24h"
d = d_of("s6")
C["s6"] = comp("s6", f"""    <div id="s6-w" style="position:absolute;inset:0;">
      <div class="c sg" id="s6-n" style="top:380px;font-size:400px;letter-spacing:-14px;">24<span style="font-size:200px;color:{GREY};">h</span></div>
      <div class="c sg" id="s6-t" style="top:800px;font-size:96px;">REFUND POLICY</div>
      <div class="shot" id="s6-shot" style="position:absolute;left:70px;top:980px;width:940px;height:172px;"><img src="assets/img/refund.jpg" style="width:940px;height:172px;" alt="HostLixo 24-hour money-back guarantee"></div>
    </div>""",
               enter_exit("#s6-w", d) +
               f'    tl.fromTo("#s6-n", {{ scale: 0.3, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.45, ease: "back.out(2)" }}, 0.12);\n'
               f'    tl.to("#s6-n", {{ scale: 1.06, duration: {d - 0.8:.2f}, ease: "none" }}, 0.6);\n'
               f'    tl.fromTo("#s6-t", {{ y: 40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "power3.out" }}, {rel(5, 0.3)});\n'
               f'    tl.fromTo("#s6-shot", {{ y: 80, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.45, ease: "power3.out" }}, {rel(5, 0.65)});\n')
IMPACT = W["s6"][0] + 0.12

# S7 end card: mark, wordmark, "Order on Discord" button, URL pill, payment badges (site footer), mc_2 behind
d = d_of("s7")
ph, phjs = photo_bg("s7", "mc_2.jpg", d, dim=0.78, z0=1.05, z1=1.15, blur=8)  # blur hides the in-game crosshair behind the CTA
pay = "".join(f'<span style="font-family:JB;font-weight:700;font-size:30px;letter-spacing:1px;color:{GREY};border:2px solid rgba(255,255,255,0.16);border-radius:8px;padding:10px 16px;">{p}</span>'
              for p in ["VISA", "MASTERCARD", "UPI", "PAYTM", "CRYPTO"])
C["s7"] = comp("s7", f"""    <div id="s7-w" style="position:absolute;inset:0;">
      {ph}
      <div class="c" id="s7-mark" style="top:300px;"><img src="assets/img/hero-logo.png" style="width:300px;height:300px;" alt="HostLixo mark"></div>
      <div class="c sg" id="s7-name" style="top:630px;font-size:130px;">HostLixo</div>
      <div class="c" id="s7-btn" style="top:810px;"><span class="btn"><svg viewBox="0 0 24 24" style="width:64px;height:64px;" fill="#080808">{DISCORD}</svg>Order on Discord</span></div>
      <div class="c" id="s7-url" style="top:1000px;"><span class="lab" style="font-size:56px;padding:18px 40px;border-radius:14px;">hostlixo.in</span></div>
      <div class="c" id="s7-pay" style="top:1150px;display:flex;justify-content:center;gap:14px;">{pay}</div>
    </div>""",
               phjs +
               '    tl.fromTo("#s7-w", { scale: 1.12, filter: "blur(14px)", opacity: 0 }, { scale: 1, filter: "blur(0px)", opacity: 1, duration: 0.3, ease: "power3.out" }, 0);\n'
               '    tl.fromTo("#s7-mark", { scale: 0.3, opacity: 0, rotation: -12 }, { scale: 1, opacity: 1, rotation: 0, duration: 0.55, ease: "back.out(1.8)" }, 0.08);\n'
               '    tl.fromTo("#s7-name", { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: "power3.out" }, 0.3);\n'
               f'    tl.fromTo("#s7-btn", {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2.2)" }}, {rel(6, 0.2)});\n'
               f'    tl.fromTo("#s7-url", {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2.2)" }}, {rel(6, 0.62)});\n'
               f'    tl.to("#s7-url", {{ scale: 1.06, duration: 0.45, ease: "sine.inOut", yoyo: true, repeat: 3 }}, {rel(6, 0.62) + 0.45:.2f});\n'
               f'    tl.fromTo("#s7-mark", {{ y: 0 }}, {{ y: -26, duration: {d - 0.7:.2f}, ease: "sine.inOut" }}, 0.65);\n'
               f'    tl.to("#s7-name", {{ scale: 1.05, duration: {d - 0.8:.2f}, ease: "none" }}, 0.7);\n'
               f'    tl.fromTo("#s7-pay", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.4 }}, {rel(6, 0.62) + 0.5:.2f});\n')

os.makedirs("compositions", exist_ok=True)
for k, v in C.items():
    open(f"compositions/{k}.html", "w").write(v)

divs = [f'      <div id="bg" data-composition-id="bg" data-composition-src="compositions/bg.html" data-start="0" data-duration="{TOTAL}" data-track-index="0" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: 0"></div>']
for k, s, e in SCENES:
    divs.append(f'      <div id="{k}" data-composition-id="{k}" data-composition-src="compositions/{k}.html" data-start="{s}" data-duration="{round(e - s, 3)}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: 1"></div>')

sfx = lambda n: f"assets/sfx/{n}.mp3"
A = []
if os.path.exists("assets/vo/vo.wav"):
    A.append(("vo", "assets/vo/vo.wav", VO_START, min(dur("assets/vo/vo.wav"), TOTAL - VO_START), 1.0, 10, 0))
loud_at = round(min(TOTAL - 2.6, VO_END + 0.3), 2)
A += [("m1", "assets/music/music.mp3", 0, loud_at, 0.17, 11, MUSIC_FROM),
      ("m2", "assets/music/music.mp3", loud_at, round(TOTAL - loud_at, 2), 0.45, 12, round(MUSIC_FROM + loud_at, 2)),
      ("hit0", sfx("sub-drop"), 0.0, dur(sfx("sub-drop")), 0.35, 13, 0)]
for i, (k, s, e) in enumerate(SCENES[1:]):
    A.append((f"wh{i}", sfx("whoosh-fast-0.3s"), round(max(0, s - 0.1), 2), dur(sfx("whoosh-fast-0.3s")), 0.5, 14 + i % 2, 0))
for i, t in enumerate(POPS):
    A.append((f"pop{i}", sfx("pop-high"), round(t, 2), dur(sfx("pop-high")), 0.4, 16 + i % 2, 0))
A += [("cash", sfx("cash-register"), round(W["s2"][0] + rel(1, 0.45), 2), dur(sfx("cash-register")), 0.35, 18, 0),
      ("imp", sfx("impact-boom"), round(IMPACT, 2), dur(sfx("impact-boom")), 0.35, 19, 0),
      ("clk", sfx("click-1"), round(W["s7"][0] + rel(6, 0.2), 2), dur(sfx("click-1")), 0.5, 20, 0),
      ("ok", sfx("confirm-1"), round(W["s7"][0] + rel(6, 0.62), 2), dur(sfx("confirm-1")), 0.35, 21, 0)]
aud = "\n".join(f'      <audio id="{i}" src="{s}" data-start="{a}" data-duration="{dd}" data-volume="{v}" data-track-index="{ln}"'
                + (f' data-media-start="{ms}"' if ms else "") + (' data-fade-out="1.5"' if i == "m2" else "") + "></audio>"
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
