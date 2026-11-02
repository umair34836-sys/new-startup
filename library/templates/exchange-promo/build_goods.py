# GOOD's promo (crypto + currency exchange), ~46 s, English or Hinglish, 9:16 or 16:9. First used 2026-11-02.
# Picture = real screen recordings of goodss.store (flow_goods.js, cursor + ripple on every click) speed-fitted to the
# VO lines (site-panel-reel idea) + the client's own logo GIF and banner GIF as stings + type overlays.
# Every on-screen fact is from library/clients/goods/site-data.md (Playwright + Discord invite API, 2026-11-02).
# Hallmark floor for video graphics (references/gates.md section 4): no eyebrow labels, no tracked caps, no single
# coloured word inside a headline, no purple/cyan gradients or glow blobs, no em dashes, no invented numbers,
# real material (site recordings, the client's GIFs) behind every card. Display face = Outfit (the site's own font).
#   cd <project>; LANG_=en FMT=portrait python3 build_goods.py
# Project folder (scratchpad, never git): rec/<shot>/{recording.mp4,events.json}, assets/img/{logo.mp4,banner.mp4,
# flags/*}, assets/fonts/Outfit-Variable.ttf, assets/sfx/*, assets/audio/mix.wav, assets/vo/lines.json,
# assets/vendor/gsap-3.14.2.min.js
import json, os, subprocess

LANG = os.environ.get("LANG_", "en")
FMT = os.environ.get("FMT", "portrait")
PORT = FMT == "portrait"
WD, HT = (1080, 1920) if PORT else (1920, 1080)
VO_START = 0.5
TOTAL = float(os.environ.get("TOTAL", 46.0))
BG, INK, GOLD, MUTED = "#060b17", "#f0f6ff", "#e8c02f", "#a9b4c6"
L = json.load(open("assets/vo/lines.json"))
st = [round(VO_START + a - 0.12, 2) for a, _ in L]
st[0] = 0.0
SCENES = [(f"s{i + 1}", st[i], st[i + 1] if i + 1 < len(st) else TOTAL) for i in range(len(st))]
W = {k: (s, e) for k, s, e in SCENES}

# scene -> [recording, from s, to s, (zoom, x-focus 0..1, y-focus 0..1)] ; None = designed card on the client's GIF
if PORT:
    SEG = {"s2": ["hero", 0.4, 6.8], "s3": ["rates", 2.0, 5.6], "s4": ["rates", 8.6, 13.4], "s5": ["rates", 5.0, 8.4],
           "s6": ["calc", 8.8, 18.2], "s7": ["how", 2.4, 9.8], "s8": ["how", 6.0, 10.0], "s9": ["contact", 2.4, 8.0],
           "s11": ["contact", 7.0, 14.6]}
else:
    SEG = {"s2": ["hero", 0.4, 6.4], "s3": ["rates", 2.2, 5.2, (1.25, 0.5, 0.25)], "s4": ["rates", 8.0, 12.8, (1.3, 0.35, 0.3)],
           "s5": ["rates", 4.6, 7.8, (1.3, 0.4, 0.3)], "s6": ["calc", 10.0, 22.8, (1.25, 0.4, 0.55)],
           "s7": ["how", 2.4, 9.6, (1.15, 0.5, 0.55)], "s8": ["how", 6.0, 9.8, (1.15, 0.5, 0.55)],
           "s9": ["contact", 2.4, 8.0], "s11": ["contact", 8.0, 17.2, (1.2, 0.2, 0.6)]}

T = {  # on-screen copy per language (Roman Hinglish for the Hinglish cut; brand words stay English)
    "en": dict(h2="Currency and crypto exchange,<br>in one place", h3="7 currencies", h4="Send crypto,<br>or swap a Binance gift card",
               h5="Fixed rates,<br>listed on the site", h6="See what you receive<br>before you send", steps=["Check the rate", "Send your request", "Receive your funds"],
               h8="Most exchanges done in<br>5 to 30 minutes", h8s="after payment confirmation", h9="Every transaction verified<br>by the GOOD's team",
               h10="Join the community", members="members", since="on Discord since May 2024", h11="Start your exchange"),
    "hi": dict(h2="Currency aur crypto exchange,<br>ek hi jagah", h3="7 currencies", h4="Crypto bhejein,<br>ya Binance gift card swap karein",
               h5="Fixed rates,<br>site par likhe hue", h6="Bhejne se pehle dekhein<br>kitna milega", steps=["Rate check karein", "Request bhejein", "Funds paayein"],
               h8="Zyada tar exchange<br>5 se 30 minute mein", h8s="payment confirm hone ke baad", h9="Har transaction GOOD's team<br>verify karti hai",
               h10="Community join karein", members="members", since="Discord par, May 2024 se", h11="Aaj hi exchange shuru karein"),
}[LANG]
RATE_NOTE = "Rates on goodss.store, 2 Nov 2026. Subject to change."
CALC_NOTE = "Example from the site's calculator, 2 Nov 2026"
MEMBERS = "3,500+"   # Discord invite API 2026-11-02: approximate_member_count 3532


def run(*a):
    subprocess.run(a, check=True, capture_output=True)


def rel(i, frac):
    a, b = L[i]
    return round(max(0.05, VO_START + a + frac * (b - a) - st[i]), 2)


# ---------- picture track ----------
os.makedirs("assets/clips", exist_ok=True)
CLICKS, parts = [], []
for k, s, e in SCENES:
    d = round(e - s, 3)
    out = f"assets/clips/{k}.mp4"
    seg = SEG.get(k)
    if seg is None:
        run("ffmpeg", "-y", "-f", "lavfi", "-i", f"color=c={BG}:s={WD}x{HT}:r=30:d={d}", "-c:v", "libx264", "-crf", "16",
            "-pix_fmt", "yuv420p", out)
    else:
        shot, a, b = seg[:3]
        speed = (b - a) / d
        vf = f"setpts=(PTS-STARTPTS)/{speed:.5f},fps=30,trim=0:{d},setpts=PTS-STARTPTS"
        if len(seg) > 3:
            z, fx, fy = seg[3]
            vf += f",scale={int(WD * z)}:{int(HT * z)}:flags=lanczos,crop={WD}:{HT}:{int(WD * (z - 1) * fx)}:{int(HT * (z - 1) * fy)}"
        run("ffmpeg", "-y", "-ss", str(a), "-t", str(b - a + 0.5), "-i", f"rec/{shot}/recording.mp4", "-an", "-vf",
            vf + f",tpad=stop_mode=clone:stop_duration={d}", "-t", str(d), "-c:v", "libx264", "-crf", "16",
            "-pix_fmt", "yuv420p", "-r", "30", out)
        for x in json.load(open(f"rec/{shot}/events.json"))["events"]:
            if x["type"] in ("click", "fakeclick") and a <= x["t"] <= b:
                CLICKS.append(round(s + (x["t"] - a) / speed, 2))
    parts.append(out)
open("assets/clips/list.txt", "w").write("".join(f"file '{os.path.basename(p)}'\n" for p in parts))
run("ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "assets/clips/list.txt", "-c", "copy", "assets/screen.mp4")

# ---------- overlays ----------
HEAD = 104 if PORT else 92
CSS = f"""
    @font-face {{ font-family: "Outfit"; src: url("assets/fonts/Outfit-Variable.ttf"); font-weight: 100 900; }}
    #root {{ position: absolute; inset: 0; overflow: hidden; font-family: Outfit; color: {INK}; }}
    .veil {{ position: absolute; left: 0; right: 0; bottom: 0; height: {1000 if PORT else 640}px;
             background: linear-gradient(180deg, rgba(6,11,23,0) 0%, rgba(6,11,23,0.86) 38%, rgba(6,11,23,0.96) 100%); }}
    .blk {{ position: absolute; {'left: 70px; right: 70px; top: 1130px; text-align: left;' if PORT else 'left: 110px; width: 1200px; top: 640px;'} }}
    .h {{ font-weight: 800; font-size: {HEAD}px; line-height: 1.04; letter-spacing: -0.02em; text-shadow: 0 4px 18px rgba(0,0,0,0.55); }}
    .sub {{ font-weight: 500; font-size: {40 if PORT else 36}px; line-height: 1.3; color: {MUTED}; margin-top: 22px; }}
    .note {{ position: absolute; {'left: 70px; top: 1560px;' if PORT else 'right: 70px; bottom: 44px;'} font-weight: 500; font-size: 26px; color: {MUTED}; }}
    .bar {{ width: 120px; height: 10px; background: {GOLD}; border-radius: 5px; margin-bottom: 34px; }}
    .chip {{ display: inline-flex; align-items: center; gap: 14px; font-weight: 700; font-size: {44 if PORT else 40}px; color: {INK};
             padding: 14px 26px; margin: 0 14px 16px 0; border-radius: 16px; background: rgba(13,21,38,0.94); border: 2px solid rgba(232,192,47,0.55); }}
    .chip img {{ width: 58px; height: 40px; object-fit: cover; border-radius: 6px; }}
    .gold {{ background: {GOLD}; color: #14110a; border-color: {GOLD}; }}
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


POPS = []
IN = 'ease: "expo.out"'


def scene(k, i, head, sub="", items=None, note="", frac=0.08):
    """headline block on a bottom veil; items = [(html, frac of the VO line)] appear as chips on their words"""
    s, e = W[k]
    d = round(e - s, 2)
    chips = "".join(f'<span class="chip{c}" id="{k}-c{j}">{h}</span>' for j, (h, fr, c) in enumerate(items or []))
    html = (f'<div class="veil"></div><div class="blk"><div class="bar" id="{k}-bar"></div>'
            f'<div class="h" id="{k}-h">{head}</div>' + (f'<div class="sub" id="{k}-s">{sub}</div>' if sub else "") +
            (f'<div style="margin-top:34px;">{chips}</div>' if chips else "") + "</div>" +
            (f'<div class="note" id="{k}-n">{note}</div>' if note else ""))
    t0 = rel(i, frac)
    js = (f'    tl.fromTo("#{k}-bar", {{ scaleX: 0, transformOrigin: "left center" }}, {{ scaleX: 1, duration: 0.5, {IN} }}, {max(0.05, t0 - 0.1)});\n'
          f'    tl.fromTo("#{k}-h", {{ y: 60, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.6, {IN} }}, {t0});\n')
    if sub:
        js += f'    tl.fromTo("#{k}-s", {{ y: 30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, {IN} }}, {t0 + 0.35:.2f});\n'
    if note:
        js += f'    tl.fromTo("#{k}-n", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {t0 + 0.5:.2f});\n'
    for j, (h, fr, c) in enumerate(items or []):
        t = max(rel(i, fr), t0 + 0.25 + 0.12 * j)
        js += f'    tl.fromTo("#{k}-c{j}", {{ y: 40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.45, {IN} }}, {t:.2f});\n'
        POPS.append(round(s + t, 2))
    js += f'    tl.to("#root", {{ opacity: 0, duration: 0.15 }}, {d - 0.15:.2f});\n'
    return comp(k, html, js)


C = {}
LOGO = 760 if PORT else 640
# s1 hook / thumbnail at 0 s: the client's own animated logo (GIF -> mp4) in its round badge + slogan
s1d = round(W["s1"][1], 2)
C["s1"] = comp("s1", f"""    <div style="position:absolute;inset:0;background:{BG};"></div>
    <video id="s1-v" src="assets/img/logo.mp4" muted playsinline data-start="0" data-duration="{s1d}" data-track-index="0"
      style="position:absolute;left:{(WD - LOGO) // 2}px;top:{300 if PORT else 90}px;width:{LOGO}px;height:{LOGO}px;border-radius:50%;object-fit:cover;"></video>
    <div id="s1-t" style="position:absolute;left:0;right:0;top:{1150 if PORT else 760}px;text-align:center;">
      <div class="h" style="font-size:{150 if PORT else 120}px;">GOOD's</div>
      <div class="sub" style="font-size:{62 if PORT else 52}px;color:{GOLD};font-weight:700;margin-top:10px;">Where trust is built.</div></div>""",
               f'    tl.fromTo("#s1-t", {{ y: 50, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.7, {IN} }}, 0.1);\n'
               f'    tl.to("#root", {{ opacity: 0, duration: 0.15 }}, {s1d - 0.15:.2f});\n')

FL = [("bd", "BDT"), ("pk", "PKR"), ("in", "INR"), ("np", "NPR"), ("eg", "EGP"), ("ph", "PHP"), ("sa", "SAR")]
C["s2"] = scene("s2", 1, T["h2"])
C["s3"] = scene("s3", 2, T["h3"], items=[(f'<img src="assets/img/flags/{f}.png" alt="">{c}', 0.1 + 0.11 * j, "") for j, (f, c) in enumerate(FL)])
C["s4"] = scene("s4", 3, T["h4"], items=[("USDT", 0.1, ""), ("LTC", 0.2, ""), ("ETH", 0.3, ""), ("SOL", 0.4, ""), ("Binance gift card", 0.75, " gold")])
C["s5"] = scene("s5", 4, T["h5"], note=RATE_NOTE)
C["s6"] = scene("s6", 5, T["h6"], items=[("32,500 PKR = $100", 0.55, " gold")], note=CALC_NOTE + ". " + RATE_NOTE.split(". ")[1])
C["s7"] = scene("s7", 6, "", items=[(f"{n + 1}. {x}", 0.05 + 0.3 * n, " gold" if n == 2 else "") for n, x in enumerate(T["steps"])])
C["s8"] = scene("s8", 7, T["h8"], sub=T["h8s"])
C["s9"] = scene("s9", 8, T["h9"])

# s10 Discord: the client's animated banner GIF + verified member count
s10s, s10e = W["s10"]
s10d = round(s10e - s10s, 2)
BW = 1000 if PORT else 1100
C["s10"] = comp("s10", f"""    <div style="position:absolute;inset:0;background:{BG};"></div>
    <video id="s10-v" src="assets/img/banner.mp4" muted playsinline data-start="0" data-duration="{s10d}" data-track-index="0"
      style="position:absolute;left:{(WD - BW) // 2 if PORT else 90}px;top:{330 if PORT else 200}px;width:{BW}px;height:{int(BW * 450 / 800)}px;border-radius:24px;object-fit:cover;border:3px solid rgba(232,192,47,0.6);"></video>
    <div class="blk" style="{'top:1000px;' if PORT else 'left:1260px;width:600px;top:260px;'}">
      <div class="bar" id="s10-bar"></div>
      <div class="h" id="s10-h" style="font-size:{HEAD - 10}px;">{T['h10']}</div>
      <div id="s10-m" style="margin-top:30px;"><span style="font-weight:800;font-size:{150 if PORT else 120}px;color:{GOLD};">{MEMBERS}</span>
        <span style="font-weight:600;font-size:{52 if PORT else 44}px;"> {T['members']}</span></div>
      <div class="sub" id="s10-s">{T['since']}</div>
      <div style="margin-top:34px;"><span class="chip" id="s10-c">discord.gg/goods</span></div></div>
    <div class="note" id="s10-n">Discord member count, 2 Nov 2026</div>""",
                f'    tl.fromTo("#s10-v", {{ scale: 0.92, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.6, {IN} }}, 0.05);\n'
                f'    tl.fromTo("#s10-bar", {{ scaleX: 0, transformOrigin: "left center" }}, {{ scaleX: 1, duration: 0.5, {IN} }}, 0.2);\n'
                f'    tl.fromTo("#s10-h", {{ y: 50, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.6, {IN} }}, 0.3);\n'
                f'    tl.fromTo("#s10-m", {{ y: 50, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.6, {IN} }}, {rel(9, 0.35)});\n'
                f'    tl.fromTo(["#s10-s", "#s10-n"], {{ opacity: 0 }}, {{ opacity: 1, duration: 0.4 }}, {rel(9, 0.35) + 0.4:.2f});\n'
                f'    tl.fromTo("#s10-c", {{ y: 30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.45, {IN} }}, {rel(9, 0.7)});\n'
                f'    tl.to("#root", {{ opacity: 0, duration: 0.15 }}, {s10d - 0.15:.2f});\n')
POPS += [round(s10s + rel(9, 0.35), 2), round(s10s + rel(9, 0.7), 2)]

C["s11"] = scene("s11", 10, T["h11"], items=[("goodss.store", 0.2, " gold"), ("discord.gg/goods", 0.4, ""), ("Telegram @goodss05", 0.6, ""),
                                             ("WhatsApp group", 0.75, ""), ("goodsstorebd@gmail.com", 0.85, "")])

# s12 end card: logo GIF again + slogan + where to go + credit
s12s, s12e = W["s12"]
s12d = round(s12e - s12s, 2)
EL = 560 if PORT else 470
C["s12"] = comp("s12", f"""    <div style="position:absolute;inset:0;background:{BG};"></div>
    <video id="e-v" src="assets/img/logo.mp4" muted playsinline data-start="0" data-duration="{s12d}" data-track-index="0"
      style="position:absolute;left:{(WD - EL) // 2}px;top:{330 if PORT else 70}px;width:{EL}px;height:{EL}px;border-radius:50%;object-fit:cover;"></video>
    <div id="e-t" style="position:absolute;left:0;right:0;top:{960 if PORT else 570}px;text-align:center;">
      <div class="h" style="font-size:{130 if PORT else 100}px;">GOOD's</div>
      <div class="sub" style="font-size:{58 if PORT else 46}px;color:{GOLD};font-weight:700;margin-top:6px;">Where trust is built.</div>
      <div style="margin-top:46px;"><span class="chip gold">goodss.store</span><span class="chip">discord.gg/goods</span></div></div>
    <div id="e-cr" style="position:absolute;left:0;right:0;bottom:{70 if PORT else 34}px;text-align:center;font-weight:500;font-size:26px;color:{MUTED};">Edited by MrCopper804</div>""",
                f'    tl.fromTo("#e-t", {{ y: 50, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.7, {IN} }}, 0.15);\n'
                f'    tl.fromTo("#e-cr", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5 }}, 1.0);\n')

os.makedirs("compositions", exist_ok=True)
for k, v in C.items():
    open(f"compositions/{k}.html", "w").write(v)

divs = [f'      <video id="screen" src="assets/screen.mp4" muted playsinline data-start="0" data-duration="{TOTAL}" data-track-index="0" '
        f'style="position:absolute;inset:0;width:{WD}px;height:{HT}px;object-fit:cover;"></video>']
for k, s, e in SCENES:
    divs.append(f'      <div id="{k}" data-composition-id="{k}" data-composition-src="compositions/{k}.html" data-start="{s}" data-duration="{round(e - s, 3)}" data-track-index="1" data-track-kind="graphics" data-width="{WD}" data-height="{HT}" style="z-index: 1"></div>')


def dur(p):
    return round(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                      capture_output=True, text=True).stdout), 3)


# SFX: rotate 2-3 variants per type (Mr Aloo feedback 2026-10-28: one repeated pop sounds cheap)
WH = ["swish-1", "whoosh-fast-0.3s", "swish-4"]
PO = ["pop-high", "pluck", "glass-tap"]
CK = ["mouse-click", "click-1", "click-2"]
sfx = lambda n: f"assets/sfx/{n}.mp3"
A = [("mix", "assets/audio/mix.wav", 0, min(dur("assets/audio/mix.wav"), TOTAL), 1.0, 10)]
A.append(("thud0", sfx("soft-thud"), 0.05, dur(sfx("soft-thud")), 0.35, 11))
for i, (k, s, e) in enumerate(SCENES[1:]):
    n = WH[i % 3]
    A.append((f"wh{i}", sfx(n), round(max(0, s - 0.12), 2), dur(sfx(n)), 0.4, 12 + i % 2))
for i, t in enumerate(sorted(set(POPS))):
    n = PO[i % 3]
    A.append((f"pop{i}", sfx(n), t, dur(sfx(n)), 0.22, 14 + i % 2))
for i, t in enumerate(CLICKS):
    n = CK[i % 3]
    A.append((f"clk{i}", sfx(n), t, dur(sfx(n)), 0.5, 16 + i % 2))
A.append(("thud1", sfx("soft-thud"), round(W["s12"][0] + 0.05, 2), dur(sfx("soft-thud")), 0.35, 18))
aud = "\n".join(f'      <audio id="{i}" src="{s}" data-start="{a}" data-duration="{dd}" data-volume="{v}" data-track-index="{ln}"></audio>'
                for i, s, a, dd, v, ln in A)
open("index.html", "w").write(f"""<!doctype html>
<html lang="en" data-resolution="{FMT}">
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
print("built", LANG, FMT, TOTAL, "clicks", CLICKS, "\n", SCENES)
