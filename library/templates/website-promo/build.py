# Build the TalkEmber Studio song video (HyperFrames) from timing.json (lyric line times) + real site screenshots.
#   python3 build.py   -> index.html + compositions/*.html
import json, os, sys, html, random

sys.path.insert(0, "/home/user/new-startup/library/tools")
import blocky_character as bc

HERE = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(os.path.join(HERE, "timing.json")))
D = T["duration"]
L = T["lines"]  # [{"start","end","roman"}] one per sung line, in order
ORANGE, GREEN, BG, CARD, LINE = "#FC8802", "#25D366", "#070A12", "#0E1119", "#20232A"
SC = 1180 / 1440  # page screenshot scale inside the browser frame
URL = {"home": "visit.talkember.site", "price_guide": "visit.talkember.site/website-design-price-pakistan/"}
for k in ("isp", "solar", "school", "clinic", "travel", "housing", "exporter"):
    URL["demo_" + k] = f"visit.talkember.site/demo/{k}/"
DEMO_NOTE = "Demo names &amp; data are samples (site FAQ)"

# Per sung line: page, scroll from y0 to y1 (screenshot px), panel (label, title, chips) or None for chorus lines.
S = {
    0: ("home", 0, 0, ("TalkEmber Studio", "Websites for Pakistani businesses", ["Your business, online — built to win customers."])),
    1: ("home", 0, 1020, ("What we build", "Fast, modern, mobile-first websites", ["Made for your industry"])),
    2: ("home", 2310, 2310, ("More than a pretty page", "English + Urdu, fast on every phone", ["English + Urdu (Nastaliq)", "Mobile-first &amp; fast"])),
    3: ("home", 2310, 2310, ("More than a pretty page", "Found on Google, leads on WhatsApp", ["Google-ready SEO", "Leads on WhatsApp"])),
    8: ("demo_isp", 0, 1020, ("Demo · Internet &amp; WiFi providers", "NetSafar Fiber", ["Pick your speed", "Is NetSafar in your area?"])),
    9: ("demo_isp", 3300, 3300, ("Demo · Internet &amp; WiFi providers", "Register a complaint, get a ticket number", ["Resolved within 3 working days (PTA rules)"])),
    10: ("demo_solar", 0, 1200, ("Demo · Solar installers", "SunNest Solar", ["How much solar do you need?", "Savings calculator"])),
    11: ("demo_solar", 3300, 3870, ("Demo · Solar installers", "The new rules, in plain words", ["NEPRA net billing 2026 guide", "Recent installations"])),
    12: ("demo_school", 0, 1500, ("Demo · Schools &amp; academies", "Bright Path School", ["Apply online in 2 minutes", "Clear fees, no surprises"])),
    13: ("demo_school", 2880, 3990, ("Demo · Schools &amp; academies", "Notices, results &amp; events", ["Latest news for parents", "Check your child's result"])),
    14: ("demo_clinic", 0, 900, ("Demo · Clinics &amp; doctors", "HealWay Family Clinic", ["Experienced, PMDC-registered doctors", "Clinic timings"])),
    15: ("demo_clinic", 1800, 1800, ("Demo · Clinics &amp; doctors", "Pick a doctor, day and time", ["Token number instantly", "Lab test prices"])),
    20: ("demo_travel", 0, 1020, ("Demo · Umrah &amp; travel agents", "Al-Rahla Travel &amp; Tours", ["Umrah packages", "Hotels near the Haram", "Visa help"])),
    21: ("demo_travel", 1850, 1850, ("Demo · Umrah &amp; travel agents", "Work out your family's total", ["Send the quote on WhatsApp"])),
    22: ("demo_housing", 0, 1750, ("Demo · Housing societies", "Green Vista Residencia", ["Pick your plot — availability map"])),
    23: ("demo_housing", 2460, 2460, ("Demo · Housing societies", "Instalment calculator", ["Approved by the development authority"])),
    24: ("demo_exporter", 0, 1020, ("Demo · Exporters &amp; manufacturers", "Kestrel Sports, Sialkot", ["What we manufacture — catalogue"])),
    25: ("demo_exporter", 3060, 3900, ("Demo · Exporters &amp; manufacturers", "Quote requests (RFQ)", ["Certifications for foreign buyers"])),
    26: ("home", 1020, 1020, ("Your business?", "Shop, restaurant, salon, factory or office", ["Tell us and we’ll plan it"])),
    27: ("home", 1020, 1020, ("Your business?", "Tell us and we’ll plan it", ["Talk to us on WhatsApp"])),
    28: ("home", 3120, 3120, ("How it works · 01", "Tell us", ["Share your business details, logo and photos on WhatsApp"])),
    29: ("home", 3120, 3120, ("How it works · 02", "Pick a demo", ["We adapt colours and content to your brand"])),
    30: ("home", 3120, 3120, ("How it works · 03", "Review", ["A preview link — ask for changes before anything goes live"])),
    31: ("home", 3120, 3120, ("How it works · 04", "Go live", ["Domain, hosting, SSL and Google setup"])),
    32: ("home", 3690, 3690, ("Packages", "Starter — PKR 25,000", ["Up to 5 pages, industry design", "Ready in about 7 days"])),
    33: ("home", 3690, 3690, ("Packages · Most popular", "Business — PKR 55,000", ["Up to 12 pages, English + Urdu", "Ready in about 14 days"])),
    34: ("home", 3690, 3690, ("Packages", "Premium — PKR 110,000+", ["Custom 3D design &amp; animations"])),
    35: ("home", 3690, 3690, ("Packages", "Premium — PKR 110,000+", ["Admin panel", "Customer portal / booking / online payments"])),
    36: ("home", 3690, 4250, ("Care plan", "PKR 2,500 / month", ["Hosting, SSL, daily backups"])),
    37: ("home", 4250, 4250, ("Care plan", "PKR 2,500 / month", ["Updates and small text/photo changes every month"])),
    38: ("home", 4770, 4770, ("FAQ · How do I pay?", "50% advance, 50% before going live", [])),
    39: ("home", 4770, 4770, ("FAQ · How do I pay?", "Bank transfer, JazzCash or Easypaisa", [])),
    44: ("home", 5700, 5700, ("Let’s build your website", "visit.talkember.site", ["Free plan and quote on WhatsApp"])),
    45: ("home", 5700, 5700, ("Phone / WhatsApp (Pakistan)", "+92 301 8858303", ["support@talkember.site"])),
    46: ("home", 5700, 5700, ("TalkEmber Studio", "Websites for Pakistani businesses", ["English + Urdu · Mobile-first · Google-ready"])),
}
# Chorus lines: browser shows these pages underneath the big text.
CHORUS = {4: ("home", 0), 5: ("home", 0), 6: ("home", 0), 7: ("home", 0),
          16: ("home", 1020), 17: ("home", 1020), 18: ("home", 1020), 19: ("home", 1020),
          40: ("price_guide", 690), 41: ("price_guide", 690), 42: ("price_guide", 3210), 43: ("price_guide", 3210)}
CHORUS_IDS = set(CHORUS)
CHORUS_PAGES = [("home", 0), ("home", 1020), ("home", 2310), ("price_guide", 690)]
blk = -1
for k, s_ in enumerate(L):
    s_["chorus"] = s_["id"] in CHORUS_IDS
    if s_["chorus"] and (k == 0 or not L[k - 1]["chorus"]):
        blk += 1
    if s_["chorus"]:
        s_["page"] = CHORUS_PAGES[min(blk, len(CHORUS_PAGES) - 1)]
        if s_["page"][0] == "price_guide" and s_["id"] in (42, 43):
            s_["page"] = ("price_guide", 3210)
SCN = lambda k: S[L[k]["id"]]
ACCENT = {"online", "TalkEmber", "Studio", "grahak", "WhatsApp", "Google", "25,000", "55,000", "1,10,000", "2,500", "3D",
          "ticket", "token", "calculator", "admission", "Umrah", "plot", "RFQ", "live", "visit.talkember.site"}
TITLES = T.get("titles", [])
first, last = L[0]["start"], L[-1]["end"]
END_CARD = min(D - 4.5, last + 0.8)
F = lambda x: f"{x:.3f}"


def esc(s):
    return html.escape(s, quote=False)


def words(text, cls):
    out = []
    for w in text.split(" "):
        acc = any(a in w for a in ACCENT)
        out.append(f'<span class="w {cls}{" acc" if acc else ""}">{esc(w)}</span>')
    return " ".join(out)


def comp(cid, style, body, js):
    return f"""<template>
  <style>
    @font-face {{ font-family: "Jakarta"; src: url("assets/fonts/PlusJakartaSans-Variable.ttf"); font-weight: 200 800; }}
    #root {{ position: absolute; inset: 0; pointer-events: none; font-family: "Jakarta", sans-serif; }}
{style}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="1920" data-height="1080" data-layout-allow-overflow data-layout-allow-occlusion>
{body}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{js}
    tl.to({{}}, {{ duration: {F(D)} }}, 0);
    window.__timelines["{cid}"] = tl;
  </script>
</template>
"""


# ---------- background: dark brand base, drifting ember glow, rising embers ----------
rnd = random.Random(7)
embers, ejs = [], []
for i in range(46):
    x, s = rnd.uniform(0, 1920), rnd.uniform(3, 7)
    embers.append(f'<i class="em" id="em{i}" style="left:{x:.0f}px; width:{s:.1f}px; height:{s:.1f}px"></i>')
    period = rnd.uniform(9, 16)
    t = rnd.uniform(0, period)
    while t < D:
        ejs.append(f'    tl.fromTo("#em{i}", {{ y: 1120, opacity: 0 }}, {{ y: -60, opacity: 0, duration: {F(period)}, ease: "none", '
                   f'keyframes: {{ opacity: [0, {rnd.uniform(0.35, 0.8):.2f}, {rnd.uniform(0.2, 0.6):.2f}, 0] }} }}, {F(t)});')
        t += period + 0.05
bg = comp("bg", f"""    #base {{ position: absolute; inset: 0; background: radial-gradient(ellipse 70% 60% at 80% 35%, #1a1208 0%, {BG} 60%), {BG}; }}
    #grid {{ position: absolute; inset: 0; background-image: linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px); background-size: 60px 60px; }}
    #orb {{ position: absolute; left: 1380px; top: 120px; width: 620px; height: 620px; border-radius: 50%; background: radial-gradient(circle at 40% 40%, rgba(252,136,2,0.55), rgba(252,136,2,0.12) 45%, transparent 70%); }}
    #orb2 {{ position: absolute; left: -200px; top: 640px; width: 700px; height: 700px; border-radius: 50%; background: radial-gradient(circle, rgba(37,211,102,0.10), transparent 65%); }}
    .em {{ position: absolute; top: 0; border-radius: 50%; background: #ffb347; box-shadow: 0 0 10px 2px rgba(252,136,2,0.7); }}""",
          '    <div id="base"></div><div id="grid"></div><div id="orb"></div><div id="orb2"></div>\n    ' + "\n    ".join(embers),
          f"""    gsap.set(".em", {{ y: 1120, opacity: 0 }});
    tl.fromTo("#orb", {{ x: 0, y: 0, scale: 1 }}, {{ x: -160, y: 90, scale: 1.15, duration: {F(D / 2)}, ease: "sine.inOut", yoyo: true, repeat: 1 }}, 0);
    tl.fromTo("#orb2", {{ x: 0 }}, {{ x: 220, duration: {F(D / 2)}, ease: "sine.inOut", yoyo: true, repeat: 1 }}, 0);
""" + "\n".join(ejs))

# ---------- browser frame with the real pages ----------
pages = sorted({v[0] for v in S.values()} | {p for p, _ in CHORUS_PAGES})
imgs = "\n".join(f'      <img id="pg-{p}" class="pg" src="assets/pages/{p}.png" />' for p in pages)
urls = "\n".join(f'        <span id="u-{p}" class="u">{URL[p]}</span>' for p in pages)
plan = []  # (t, page, y0, y1, dur)
for i in range(len(L)):
    t0 = L[i]["start"] - 0.35
    t1 = (L[i + 1]["start"] - 0.35) if i + 1 < len(L) else END_CARD
    if not L[i]["chorus"]:
        p, y0, y1, _ = SCN(i)
    else:
        p, y0 = L[i]["page"]; y1 = y0
    plan.append((t0, p, y0, y1, t1 - t0))
bjs = [f'    gsap.set("#sweep", {{ x: -400, opacity: 0 }}); gsap.set(".pg", {{ opacity: 0, x: 0, y: 0 }}); gsap.set(".u", {{ opacity: 0 }}); gsap.set("#bw", {{ opacity: 0, scale: 0.92, y: 40 }});',
       f'    tl.to("#bw", {{ opacity: 1, scale: 1, y: 0, duration: 0.9, ease: "power3.out" }}, {F(max(0.2, first - 1.2))});',
       f'    tl.to("#bw", {{ opacity: 0, scale: 0.94, duration: 0.6, ease: "power2.in" }}, {F(END_CARD - 0.2)});']
cur, cy = None, None
for t, p, y0, y1, dur in plan:
    if p != cur:
        if cur:
            bjs.append(f'    tl.to("#pg-{cur}", {{ opacity: 0, x: -90, duration: 0.45, ease: "power2.in" }}, {F(t)});')
            bjs.append(f'    tl.to("#u-{cur}", {{ opacity: 0, duration: 0.2 }}, {F(t)});')
            bjs.append(f'    tl.fromTo("#sweep", {{ x: -400, opacity: 0.9 }}, {{ x: 1400, opacity: 0, duration: 0.7, ease: "power2.inOut" }}, {F(t + 0.1)});')
        bjs.append(f'    tl.fromTo("#pg-{p}", {{ opacity: 0, x: 90, y: {-y0 * SC:.1f} }}, {{ opacity: 1, x: 0, y: {-y0 * SC:.1f}, duration: 0.55, ease: "power3.out" }}, {F(t + (0.3 if cur else 0))});')
        bjs.append(f'    tl.to("#u-{p}", {{ opacity: 1, duration: 0.25 }}, {F(t + 0.3)});')
        cur, cy = p, y0
    elif y0 != cy:
        bjs.append(f'    tl.to("#pg-{p}", {{ y: {-y0 * SC:.1f}, duration: 0.9, ease: "power2.inOut" }}, {F(t)});')
        cy = y0
    if y1 != cy:
        st = t + 0.9
        bjs.append(f'    tl.to("#pg-{p}", {{ y: {-y1 * SC:.1f}, duration: {F(max(0.8, min(2.6, dur - 1.2)))}, ease: "power2.inOut" }}, {F(st)});')
        cy = y1
browser = comp("browser", f"""    #bw {{ position: absolute; left: 70px; top: 96px; width: 1180px; height: 698px; border-radius: 18px; overflow: hidden; background: {CARD}; border: 1px solid {LINE}; box-shadow: 0 30px 80px rgba(0,0,0,0.55), 0 0 0 1px rgba(252,136,2,0.08); }}
    #bar {{ position: absolute; left: 0; top: 0; right: 0; height: 34px; background: #0B0E15; border-bottom: 1px solid {LINE}; }}
    .dot {{ position: absolute; top: 12px; width: 11px; height: 11px; border-radius: 50%; }}
    #url {{ position: absolute; left: 92px; right: 18px; top: 6px; height: 22px; border-radius: 11px; background: #151924; }}
    .u {{ position: absolute; left: 14px; top: 2px; font-size: 13px; color: #A6AEBD; letter-spacing: 0.2px; white-space: nowrap; }}
    #vp {{ position: absolute; left: 0; top: 34px; width: 1180px; height: 664px; overflow: hidden; background: {BG}; }}
    .pg {{ position: absolute; left: 0; top: 0; width: 1180px; }}
    #sweep {{ position: absolute; top: 0; left: 0; width: 260px; height: 664px; background: linear-gradient(90deg, transparent, rgba(252,136,2,0.35), transparent); opacity: 0; }}""",
               f"""    <div id="bw">
      <div id="bar"><i class="dot" style="left:16px;background:#ff5f57"></i><i class="dot" style="left:34px;background:#febc2e"></i><i class="dot" style="left:52px;background:#28c840"></i>
        <div id="url">
{urls}
        </div></div>
      <div id="vp">
{imgs}
        <div id="sweep"></div>
      </div>
    </div>""", "\n".join(bjs))

# ---------- side panel with the real section text ----------
pbody, pjs, prev, starts = [], ['    gsap.set(".card", { opacity: 0 });'], None, []
for i in range(len(L)):
    if L[i]["chorus"]:
        prev = None
        continue
    lab, title, chips = SCN(i)[3]
    key = (lab, title, tuple(chips))
    if key == prev:
        continue
    prev = key
    demo = SCN(i)[0].startswith("demo_")
    chip_html = "".join(f'<div class="chip c{i}">{c}</div>' for c in chips)
    note = f'<div class="note c{i}">{DEMO_NOTE}</div>' if demo else ""
    starts.append(i)
    pbody.append(f'    <div class="card" id="card{i}"><div class="lab c{i}">{lab}</div><div class="ttl c{i}">{title}</div>{chip_html}{note}</div>')
for k, i in enumerate(starts):
    t = L[i]["start"] - 0.2
    nxt = starts[k + 1] if k + 1 < len(starts) else None
    # hide at the next card, or before a chorus line, whichever comes first
    hide = END_CARD - 0.3
    for j in range(i + 1, len(L)):
        if L[j]["chorus"] or (nxt is not None and j == nxt):
            hide = L[j]["start"] - 0.45
            break
    for ti in TITLES:
        if t < ti["t"] < hide:
            hide = ti["t"] - 0.3
    pjs.append(f'    tl.set("#card{i}", {{ opacity: 1 }}, {F(t)});')
    pjs.append(f'    tl.fromTo("#card{i} .c{i}", {{ opacity: 0, y: 26, filter: "blur(6px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.5, ease: "power3.out", stagger: 0.12 }}, {F(t)});')
    pjs.append(f'    tl.to("#card{i}", {{ opacity: 0, x: 40, duration: 0.35, ease: "power2.in" }}, {F(hide)});')
panel = comp("panel", f"""    .card {{ position: absolute; left: 1300px; top: 110px; width: 560px; }}
    .lab {{ font-size: 20px; font-weight: 800; letter-spacing: 2.5px; text-transform: uppercase; color: {ORANGE}; margin-bottom: 14px; }}
    .ttl {{ font-size: 50px; font-weight: 800; line-height: 1.08; color: #F3F4F6; margin-bottom: 22px; }}
    .chip {{ display: block; width: fit-content; max-width: 560px; font-size: 25px; font-weight: 600; color: #E5E7EB; background: {CARD}; border: 1px solid {LINE}; border-left: 4px solid {ORANGE}; border-radius: 14px; padding: 12px 18px; margin-bottom: 12px; }}
    .note {{ display: inline-block; margin-top: 10px; font-size: 17px; color: #A6AEBD; border: 1px dashed #3a3f4b; border-radius: 999px; padding: 6px 14px; }}""",
               "\n".join(pbody), "\n".join(pjs))

# ---------- hero layer: intro, chorus big text, end card ----------
hb, hj = [], ['    gsap.set(["#ov", ".big", "#endc", ".sect"], { opacity: 0 });']
chorus_blocks, run = [], []
for i in range(len(L)):
    if L[i]["chorus"] and L[i].get("sung", True):
        run.append(i)
    elif run:
        chorus_blocks.append(run); run = []
if run:
    chorus_blocks.append(run)
for blk in chorus_blocks:
    a, b = L[blk[0]]["start"] - 0.5, L[blk[-1]]["end"] + 0.25
    hj.append(f'    tl.to("#ov", {{ opacity: 1, duration: 0.45, ease: "power2.out" }}, {F(a)});')
    hj.append(f'    tl.to("#ov", {{ opacity: 0, duration: 0.45, ease: "power2.in" }}, {F(b)});')
    for i in blk:
        hb.append(f'    <div class="big" id="big{i}">{words(L[i]["roman"], f"bw{i}")}</div>')
        s, e = L[i]["start"] - 0.1, (L[i + 1]["start"] - 0.25 if i + 1 < len(L) and L[i + 1]["chorus"] else L[i]["end"] + 0.2)
        hj.append(f'    tl.set("#big{i}", {{ opacity: 1 }}, {F(s)});')
        hj.append(f'    tl.fromTo(".bw{i}", {{ opacity: 0, y: 40, scale: 0.9, filter: "blur(10px)" }}, {{ opacity: 1, y: 0, scale: 1, filter: "blur(0px)", duration: 0.45, ease: "back.out(1.6)", stagger: 0.09 }}, {F(s)});')
        hj.append(f'    tl.to("#big{i}", {{ opacity: 0, y: -30, duration: 0.25, ease: "power2.in" }}, {F(max(s + 0.6, e))});')
for n, ti in enumerate(TITLES):
    hb.append(f'    <div class="sect" id="sect{n}"><div class="slab">{ti["label"]}</div><div class="stl">{ti["title"]}</div><div class="ssub">{ti.get("sub", "")}</div></div>')
    a, b = ti["t"], ti["t"] + ti["dur"]
    hj += [f'    tl.to("#ov", {{ opacity: 1, duration: 0.4, ease: "power2.out" }}, {F(a)});',
           f'    tl.set("#sect{n}", {{ opacity: 1 }}, {F(a + 0.1)});',
           f'    tl.fromTo("#sect{n} > *", {{ opacity: 0, y: 40, filter: "blur(10px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.6, ease: "power3.out", stagger: 0.18 }}, {F(a + 0.1)});',
           f'    tl.to("#sect{n}", {{ opacity: 0, scale: 1.06, duration: 0.4, ease: "power2.in" }}, {F(b - 0.45)});',
           f'    tl.to("#ov", {{ opacity: 0, duration: 0.4, ease: "power2.in" }}, {F(b - 0.3)});']
intro_end = max(1.6, first - 0.6)
hb.append(f"""    <div id="intro"><img id="logo" src="assets/logo.png" /><div id="in1">{words("TalkEmber Studio", "iw")}</div>
      <div id="in2">Websites for Pakistani businesses · English + Urdu</div></div>
    <div id="endc"><img id="logo2" src="assets/logo.png" /><div id="e1">visit.talkember.site</div>
      <div id="e2"><span class="wa">WhatsApp</span> +92 301 8858303</div><div id="e3">support@talkember.site</div></div>""")
hj += [f'    gsap.set("#intro", {{ opacity: 1 }}); tl.set("#intro", {{ opacity: 1 }}, 0);',
       f'    tl.fromTo("#logo", {{ scale: 0.82 }}, {{ scale: 1, duration: 1.2, ease: "back.out(1.7)" }}, 0);',
       f'    tl.fromTo(".iw", {{ y: 24 }}, {{ y: 0, duration: 0.9, ease: "power3.out", stagger: 0.18 }}, 0);',
       f'    tl.fromTo("#in2", {{ opacity: 0, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power2.out" }}, 1.3);',
       f'    tl.to("#intro", {{ opacity: 0, scale: 1.08, filter: "blur(8px)", duration: 0.6, ease: "power2.in" }}, {F(intro_end)});',
       f'    tl.set("#endc", {{ opacity: 1 }}, {F(END_CARD)});',
       f'    tl.fromTo("#endc > *", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.6, ease: "power3.out", stagger: 0.2 }}, {F(END_CARD)});']
hero = comp("hero", f"""    #ov {{ position: absolute; inset: 0; background: radial-gradient(ellipse 80% 70% at 50% 50%, rgba(7,10,18,0.72), rgba(7,10,18,0.92)); }}
    .big {{ position: absolute; left: 120px; right: 120px; top: 380px; text-align: center; font-size: 104px; font-weight: 800; line-height: 1.1; color: #fff; text-shadow: 0 8px 40px rgba(0,0,0,0.7); }}
    .w {{ display: inline-block; }}
    .acc {{ color: {ORANGE}; }}
    #intro, #endc {{ position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; }}
    #logo, #logo2 {{ width: 440px; margin-bottom: 30px; }}
    #in1 {{ font-size: 120px; font-weight: 800; color: #fff; }}
    #in2 {{ margin-top: 18px; font-size: 38px; font-weight: 600; color: #A6AEBD; }}
    #e1 {{ font-size: 86px; font-weight: 800; color: #fff; }}
    #e2 {{ margin-top: 26px; font-size: 52px; font-weight: 700; color: #F3F4F6; }}
    .wa {{ background: {GREEN}; color: #052E16; border-radius: 999px; padding: 6px 26px; margin-right: 14px; }}
    #e3 {{ margin-top: 22px; font-size: 34px; color: #A6AEBD; }}
    .sect {{ position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; }}
    .slab {{ font-size: 30px; font-weight: 800; letter-spacing: 4px; text-transform: uppercase; color: {ORANGE}; }}
    .stl {{ margin-top: 18px; font-size: 96px; font-weight: 800; line-height: 1.05; color: #fff; max-width: 1500px; }}
    .ssub {{ margin-top: 22px; font-size: 36px; font-weight: 600; color: #A6AEBD; max-width: 1400px; }}""",
              '    <div id="ov"></div>\n' + "\n".join(hb), "\n".join(hj))

# ---------- captions: Roman Urdu, per-word blur-in, not during chorus (the hero shows those lines) ----------
cb, cj = [], ['    gsap.set(".cap", { opacity: 0 });']
for i, ln in enumerate(L):
    if L[i]["chorus"] or not L[i].get("sung", True):
        continue
    cb.append(f'    <div class="cap" id="cap{i}">{words(ln["roman"], f"cw{i}")}</div>')
    s = ln["start"] - 0.12
    e = min(ln["end"] + 0.35, L[i + 1]["start"] - 0.2) if i + 1 < len(L) else ln["end"] + 0.6
    cj.append(f'    tl.set("#cap{i}", {{ opacity: 1 }}, {F(s)});')
    cj.append(f'    tl.fromTo(".cw{i}", {{ opacity: 0, y: 14, filter: "blur(8px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.32, ease: "power2.out", stagger: 0.09 }}, {F(s)});')
    cj.append(f'    tl.to("#cap{i}", {{ opacity: 0, duration: 0.22 }}, {F(max(s + 0.5, e))});')
caps = comp("captions", f"""    #veil {{ position: absolute; left: 0; right: 0; bottom: 0; height: 300px; background: linear-gradient(transparent, rgba(7,10,18,0.85)); }}
    .cap {{ position: absolute; left: 70px; width: 1180px; top: 838px; text-align: center; font-size: 46px; font-weight: 700; line-height: 1.2; color: #fff; text-shadow: 0 4px 20px rgba(0,0,0,0.8); }}
    .w {{ display: inline-block; }}
    .acc {{ color: {ORANGE}; }}""", '    <div id="veil"></div>\n' + "\n".join(cb), "\n".join(cj))

# ---------- host (owner's skin) ----------
HS, HX, HY = 9.5, 1600, 1050
moves = [[0, "idle"], [0.6, "wave"]]
lastp = None
for i, ln in enumerate(L):
    p = None if L[i]["chorus"] else SCN(i)[0]
    if L[i]["chorus"]:
        if i == 0 or not L[i - 1]["chorus"]:
            moves.append([ln["start"] - 0.2, "spin"])
            moves.append([ln["start"] + 1.4, "talk"])
        continue
    if p != lastp:
        moves.append([ln["start"] - 0.3, "point"])
        moves.append([ln["start"] + 1.3, "talk"])
    lastp = p
moves.append([END_CARD - 0.2, "wave"])
moves = sorted([m for m in moves if 0 <= m[0] < D], key=lambda m: m[0])
hjs = bc.pose_js("host", HS, moves, D, -28)
host = f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; pointer-events: none; }}
    #shadow {{ position: absolute; left: {HX - 110}px; top: {HY - 22}px; width: 220px; height: 44px; border-radius: 50%; background: radial-gradient(ellipse, rgba(0,0,0,0.55), transparent 70%); }}
    .host-stage {{ position: absolute; left: {HX}px; top: {HY}px; width: 0; height: 0; perspective: {80 * HS:g}px; perspective-origin: 0 {-16 * HS:g}px; }}
    .host-cam {{ position: absolute; left: 0; top: 0; width: 0; height: 0; transform-style: preserve-3d; }}
    {bc.css("host", "assets/characters/host-skin.png")}
  </style>
  <div id="root" data-composition-id="host" data-layout-allow-overflow data-width="1920" data-height="1080">
    <div id="shadow"></div>
    <div class="host-stage"><div class="host-cam" style="transform: rotateX(-6deg)">
{bc.rig_html("host", HS, "      ")}
    </div></div>
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{chr(10).join(hjs)}
    gsap.set("#root", {{ opacity: 0 }});
    tl.to("#root", {{ opacity: 1, duration: 0.6 }}, 0.3);
    tl.to({{}}, {{ duration: {F(D)} }}, 0);
    window.__timelines["host"] = tl;
  </script>
</template>
"""

os.makedirs(os.path.join(HERE, "compositions"), exist_ok=True)
for name, src in (("bg", bg), ("browser", browser), ("panel", panel), ("hero", hero), ("captions", caps), ("host", host)):
    open(os.path.join(HERE, "compositions", name + ".html"), "w").write(src)
layers = ["bg", "browser", "panel", "host", "captions", "hero"]
divs = "\n".join(f'      <div id="{n}" data-composition-id="{n}" data-composition-src="compositions/{n}.html" data-start="0" data-duration="{F(D)}" '
                 f'data-track-index="{k}" data-track-kind="graphics" data-width="1920" data-height="1080" style="z-index: {k}"></div>'
                 for k, n in enumerate(layers))
open(os.path.join(HERE, "index.html"), "w").write(f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="assets/vendor/gsap-3.14.2.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1920px; height: 1080px; overflow: hidden; background: {BG}; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{F(D)}" data-width="1920" data-height="1080">
{divs}
      <audio id="song" src="assets/music/song.wav" data-start="0" data-duration="{F(D)}" data-volume="1" data-track-index="{len(layers)}"></audio>
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
""")
print(f"built: {D:.1f}s, {len(L)} lines, {len(pbody)} panel cards, {len(moves)} host moves, end card at {END_CARD:.1f}s")
