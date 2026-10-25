# One 9:16 topic reel per VO script: each VO line gets its own kinetic scene (hook, chips, stat, flags, limited, cta).
# Made for SkilloraClouds on 2026-10-25 (4 topics: DDoS, low ping, game reselling, VPS + coupon), same look as build.py.
# Every claim is from skilloraclouds.com / minecraft.resell.skilloraclouds.com read in Playwright on 2026-10-25, except
# "AMD EPYC 9" and "Budget & Standard plans LIMITED" (the client's own approved wording).
# Usage (in a project folder with assets/{img,fonts,vendor,sfx,music} and vo_parts/000.wav ...):
#   python3 build_topics.py <r1|r2|r3|r4>
# It joins the VO parts with a 0.3 s gap into assets/vo/vo.wav (loudnorm -16 LUFS), times one scene per line, writes index.html.
import json, subprocess, sys
import numpy as np

W, H = 1080, 1920
GREEN, GREEN2, DARK, AMBER = "#22c55e", "#16a34a", "#070b12", "#fbbf24"   # site CSS: #22c55e x17, #16a34a x5
SR, GAP, TAIL = 48000, 0.3, 2.6

FLAG = {"India": "india-flag.png", "Singapore": "singapore-flag.png", "Dubai": "dubai-flag.png", "Germany": "germany-flag.png"}
ICON = {"shield": "M12 3l8 3.5v5.5c0 5-3.5 8.5-8 9.5-4.5-1-8-4.5-8-9.5V6.5z", "cpu": "M8 8h8v8H8zM10 4v3M14 4v3M10 17v3M14 17v3M4 10h3M4 14h3M17 10h3M17 14h3",
        "ssd": "M5 7h14v10H5zM8 11h5M16 12h.01", "layers": "M12 4l8 4-8 4-8-4zM4 12l8 4 8-4M4 16l8 4 8-4", "brain": "M9 5a3 3 0 0 0-3 3v1a3 3 0 0 0 0 6v1a3 3 0 0 0 6 0V5zM15 5a3 3 0 0 1 3 3v1a3 3 0 0 1 0 6v1a3 3 0 0 1-6 0",
        "key": "M8 15a4 4 0 1 1 3-6.5L20 9v3h-2v2h-2v-2h-3.5A4 4 0 0 1 8 15z", "plug": "M9 3v5M15 3v5M7 8h10v3a5 5 0 0 1-10 0zM12 16v5",
        "import": "M12 4v11M7 10l5 5 5-5M5 20h14", "user": "M12 12a4 4 0 1 0 0-8a4 4 0 1 0 0 8M4 21c0-4 4-6 8-6s8 2 8 6",
        "link": "M10 14a4 4 0 0 0 6 0l3-3a4 4 0 0 0-6-6l-1 1M14 10a4 4 0 0 0-6 0l-3 3a4 4 0 0 0 6 6l1-1", "lock": "M6 11h12v9H6zM8 11V8a4 4 0 0 1 8 0v3",
        "image": "M4 5h16v14H4zM8 10a1.5 1.5 0 1 0 0-.01M20 16l-5-5-9 8", "tag": "M4 4h7l9 9-7 7-9-9zM8 8h.01", "palette": "M12 3a9 9 0 1 0 0 18c1 0 1.5-.8 1.5-1.5 0-1.2 1-1.5 2-1.5h2A3.5 3.5 0 0 0 21 14.5 9 9 0 0 0 12 3zM7.5 11h.01M10 7.5h.01M14 7.5h.01",
        "root": "M5 7l5 5-5 5M12 17h7", "disc": "M12 3a9 9 0 1 0 0 18a9 9 0 1 0 0-18M12 10a2 2 0 1 0 0 4a2 2 0 1 0 0-4",
        "wifi": "M5 12a10 10 0 0 1 14 0M8 15a6 6 0 0 1 8 0M12 19h.01", "check": "M5 12l5 5 9-10"}

# ---------------- scene specs (one per VO line) ----------------
REELS = {
 "r1": {"music": "upbeat-electronic--loyalty-freak-music--high-technologic-beat-explosion.mp3", "scenes": [
   ("hook", {"a": "SERVER BAAR BAAR", "b": "DOWN?", "pill": "DDoS ATTACK?"}),
   ("big", {"icon": "shield", "title": "SkillGuard", "sub": "aapke server ki hifazat"}),
   ("stat", {"top": "DDoS MITIGATION", "big": "500 Tbps+", "sub": "Cloudflare Magic Transit"}),
   ("chips", {"head": "PROTECTION", "items": [("layers", "Multi-layered"), ("brain", "ML-powered mitigation")]}),
   ("chips", {"head": "LAG-FREE GAMING", "items": [("cpu", "AMD EPYC 9"), ("ssd", "NVMe SSD")]}),
   ("limited", {}), ("cta", {"url": "skilloraclouds.com"})]},
 "r2": {"music": "upbeat-electronic--loyalty-freak-music--people-are-spinning.mp3", "scenes": [
   ("hook", {"a": "HIGH PING SE", "b": "HAAR RAHE HO?", "pill": "LAG?"}),
   ("flags", {"head": "MINECRAFT SERVERS IN", "items": ["India", "Singapore", "Dubai"]}),
   ("ping", {"head": "PING (site)", "items": [("Dubai", 5), ("Singapore", 15), ("India", 35)]}),
   ("big", {"icon": "wifi", "title": "Closest location", "sub": "= lowest ping"}),
   ("big", {"icon": "check", "title": "Test My Ping", "sub": "skilloraclouds.com"}),
   ("stat", {"top": "BUDGET PLAN", "big": "₹20/mo", "sub": "AMD EPYC 9 ke saath"}),
   ("limited", {}), ("cta", {"url": "skilloraclouds.com"})]},
 "r3": {"music": "upbeat-electronic--loyalty-freak-music--you-know-why.mp3", "scenes": [
   ("hook", {"a": "APNI GAME HOSTING", "b": "COMPANY?", "pill": "SHURU KARO!"}),
   ("big", {"icon": "tag", "title": "Game Reselling", "sub": "apne brand ke naam se"}),
   ("chips", {"head": "CONNECT IN A MINUTE", "items": [("plug", "Pterodactyl panel"), ("key", "Client API key"), ("import", "Import servers")]}),
   ("chips", {"head": "CUSTOMERS", "items": [("user", "Customer logins"), ("link", "Assign servers")]}),
   ("big", {"icon": "lock", "title": "panel.yourdomain.com", "sub": "one-click HTTPS", "small": True}),
   ("chips", {"head": "YOUR BRAND", "items": [("image", "Your logo"), ("tag", "Your name"), ("palette", "Your colors")]}),
   ("limited", {"epyc": True}), ("cta", {"url": "minecraft.resell.skilloraclouds.com", "small": True})]},
 "r4": {"music": "upbeat-electronic--loyalty-freak-music--monarch-of-the-street.mp3", "scenes": [
   ("hook", {"a": "FULL CONTROL", "b": "CHAHIYE?", "pill": "SKILLORACLOUDS VPS"}),
   ("chips", {"head": "VPS", "items": [("root", "Full root access"), ("disc", "Custom ISO"), ("ssd", "NVMe SSD")]}),
   ("big", {"icon": "cpu", "title": "Linux / Windows", "sub": "jo aap chahein"}),
   ("flags", {"head": "LOCATIONS", "items": ["India", "Singapore", "Germany"]}),
   ("stat", {"top": "VPS PLANS", "big": "₹250/mo", "sub": "se shuru"}),
   ("coupon", {}),
   ("limited", {"epyc": True, "games": True}), ("cta", {"url": "skilloraclouds.com"})]},
}


def svg(path, size, stroke="#04140a", bg=GREEN):
    return (f'<svg viewBox="0 0 24 24" style="width:{size}px;height:{size}px;flex:none;"><rect width="24" height="24" rx="7" fill="{bg}"/>'
            f'<path d="{path}" stroke="{stroke}" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def load(f):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def trim(a, thr=0.01):
    i = np.where(np.abs(a) > thr)[0]
    return a if not len(i) else a[max(0, i[0] - int(0.03 * SR)):min(len(a), i[-1] + int(0.08 * SR))]


def dur(p):
    return round(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                      capture_output=True, text=True).stdout), 3)


reel = sys.argv[1]
spec = REELS[reel]
n = len(spec["scenes"])
VO0 = 0.5
parts = [trim(load(f"vo_parts/{i:03d}.wav")) for i in range(n)]
spans, t, chunks = [], VO0, [np.zeros(int(VO0 * SR), np.float32)]
for a in parts:
    spans.append((round(t, 2), round(t + len(a) / SR, 2)))
    chunks += [a, np.zeros(int(GAP * SR), np.float32)]
    t += len(a) / SR + GAP
np.concatenate(chunks).tofile("vo_raw.f32")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "vo_raw.f32", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
                "-ar", str(SR), "assets/vo/vo.wav"], check=True)
TOTAL = round(spans[-1][1] + TAIL, 2)
starts = [0.0] + [round(s - 0.15, 2) for s, _ in spans[1:]]
ends = starts[1:] + [TOTAL]
json.dump({"spans": spans, "scenes": list(zip(starts, ends)), "total": TOTAL}, open("timing.json", "w"))

T, A, HT = [], [], []
sfx = lambda name, at, vol, lane: A.append((name, at, vol, lane))


def word_in(sel, t0, d=0.4, y=30):
    T.append(f'tl.fromTo("{sel}", {{opacity:0, filter:"blur(14px)", y:{y}}}, {{opacity:1, filter:"blur(0px)", y:0, duration:{d}, ease:"power3.out"}}, {t0:.2f});')


def pop_in(sel, t0):
    T.append(f'tl.fromTo("{sel}", {{opacity:0, scale:0.5, filter:"blur(10px)"}}, {{opacity:1, scale:1, filter:"blur(0px)", duration:0.4, ease:"back.out(2)"}}, {t0:.2f});')


for k, ((kind, d), (s0, s1), (vs, ve)) in enumerate(zip(spec["scenes"], zip(starts, ends), spans)):
    sid, L = f"sc{k}", ve - vs
    beat = lambda f: vs + L * f          # a moment inside this line
    T.append(f'tl.set("#{sid}", {{visibility:"visible"}}, {s0:.2f}); tl.set("#{sid}", {{visibility:"hidden"}}, {s1:.2f});')
    if k:
        T.append(f'tl.fromTo("#{sid}", {{scale:1.12, filter:"blur(14px)", opacity:0}}, {{scale:1, filter:"blur(0px)", opacity:1, duration:0.3, ease:"power3.out"}}, {s0:.2f});')
        sfx("whoosh-short", s0 - 0.12, 0.45, 14 + k % 2)
    if k < n - 1:
        T.append(f'tl.to("#{sid}", {{scale:1.3, filter:"blur(16px)", opacity:0, duration:0.22, ease:"power3.in"}}, {s1 - 0.22:.2f});')
    c = f'<div id="{sid}" class="scene">'
    if kind == "hook":
        c += (f'<div class="fill" style="background:url(assets/img/hero-minecraft.jpg) center/cover;"></div>'
              f'<div class="fill" style="background:linear-gradient(to bottom, rgba(7,11,18,0.5), rgba(7,11,18,0.2) 35%, rgba(7,11,18,0.88) 68%, {DARK});"></div>'
              f'<div id="{sid}a" class="c jk sh" style="top:1000px;font-weight:800;font-size:64px;color:#e5e7eb;letter-spacing:4px;">{d["a"]}</div>'
              f'<div id="{sid}b" class="c anton sh g" style="top:1090px;font-size:{190 if len(d["b"]) <= 9 else 140}px;">{d["b"]}</div>'
              f'<div id="{sid}p" class="c" style="top:1360px;"><span class="pill" style="background:{AMBER};box-shadow:0 0 60px rgba(251,191,36,0.5);">{d["pill"]}</span></div>')
        word_in(f"#{sid}a", 0.05); T.append(f'tl.fromTo("#{sid}b", {{scale:1.15}}, {{scale:1, duration:1.0, ease:"power2.out"}}, 0);')
        pop_in(f"#{sid}p", beat(0.6)); sfx("impact-bass-1", beat(0.6), 0.3, 13)
    elif kind == "big":
        fs = 72 if d.get("small") else 110
        c += (f'<div id="{sid}i" class="c" style="top:520px;">{svg(ICON[d["icon"]], 260)}</div>'
              f'<div id="{sid}t" class="c jk" style="top:880px;font-weight:800;font-size:{fs}px;color:#fff;">{d["title"]}</div>'
              f'<div id="{sid}s" class="c jk" style="top:{900 + fs + 40}px;font-weight:700;font-size:58px;color:{GREEN};">{d["sub"]}</div>')
        pop_in(f"#{sid}i", s0 + 0.1); word_in(f"#{sid}t", s0 + 0.3); word_in(f"#{sid}s", beat(0.55))
        sfx("pop", s0 + 0.1, 0.5, 16)
    elif kind == "stat":
        c += (f'<div id="{sid}t" class="c jk" style="top:560px;font-weight:800;font-size:60px;letter-spacing:6px;color:{GREEN};">{d["top"]}</div>'
              f'<div id="{sid}b" class="c anton" style="top:680px;font-size:250px;color:#fff;text-shadow:0 0 70px rgba(34,197,94,0.55);">{d["big"]}</div>'
              f'<div id="{sid}s" class="c jk" style="top:1020px;font-weight:700;font-size:60px;color:#e5e7eb;">{d["sub"]}</div>')
        word_in(f"#{sid}t", s0 + 0.1); T.append(f'tl.fromTo("#{sid}b", {{scale:0.2, opacity:0}}, {{scale:1, opacity:1, duration:0.45, ease:"back.out(2.4)"}}, {beat(0.3):.2f});')
        word_in(f"#{sid}s", beat(0.6)); sfx("impact-bass-1", beat(0.3), 0.3, 13)
    elif kind == "chips":
        m = len(d["items"])
        c += f'<div id="{sid}h" class="c jk" style="top:{860 - m * 120}px;font-weight:800;font-size:60px;letter-spacing:6px;color:{GREEN};">{d["head"]}</div>'
        word_in(f"#{sid}h", s0 + 0.1)
        for j, (ic, txt) in enumerate(d["items"]):
            top = 980 - m * 120 + j * 230
            c += (f'<div id="{sid}c{j}" class="card jk" style="position:absolute;left:110px;top:{top}px;width:860px;height:190px;display:flex;align-items:center;gap:34px;'
                  f'padding-left:44px;font-weight:800;font-size:{60 if len(txt) < 16 else 52}px;color:#fff;">{svg(ICON[ic], 104)}{txt}</div>')
            at = vs + 0.15 + j * min(0.9, L * 0.7 / m)
            pop_in(f"#{sid}c{j}", at); sfx("pop", at, 0.5, 16 + j % 2)
    elif kind == "flags":
        m = len(d["items"])
        c += f'<div id="{sid}h" class="c jk" style="top:420px;font-weight:800;font-size:60px;letter-spacing:4px;color:#fff;">{d["head"]}</div>'
        word_in(f"#{sid}h", s0 + 0.1)
        for j, nm in enumerate(d["items"]):
            c += (f'<div id="{sid}c{j}" class="card jk" style="position:absolute;left:140px;top:{580 + j * 240}px;width:800px;height:200px;display:flex;align-items:center;gap:44px;'
                  f'padding-left:54px;font-weight:800;font-size:76px;color:#fff;"><img src="assets/img/{FLAG[nm]}" style="width:160px;height:108px;object-fit:cover;border-radius:14px;" alt="{nm} flag">{nm}</div>')
            at = vs + 0.2 + j * min(0.8, L * 0.6 / m)
            T.append(f'tl.fromTo("#{sid}c{j}", {{x:900, opacity:0}}, {{x:0, opacity:1, duration:0.4, ease:"power3.out"}}, {at:.2f});'); sfx("pop", at, 0.5, 16 + j % 2)
    elif kind == "ping":
        c += f'<div id="{sid}h" class="c jk" style="top:440px;font-weight:800;font-size:60px;letter-spacing:4px;color:#fff;">PING</div>'
        word_in(f"#{sid}h", s0 + 0.1)
        for j, (nm, ms) in enumerate(d["items"]):
            top = 600 + j * 260
            c += (f'<div id="{sid}c{j}" style="position:absolute;left:110px;top:{top}px;width:860px;">'
                  f'<div class="jk" style="display:flex;align-items:center;gap:26px;font-weight:800;font-size:60px;color:#fff;"><img src="assets/img/{FLAG[nm]}" style="width:110px;height:74px;object-fit:cover;border-radius:10px;" alt="{nm} flag">{nm}'
                  f'<span class="anton g" style="margin-left:auto;font-size:84px;">~{ms} ms</span></div>'
                  f'<div style="margin-top:22px;height:26px;border-radius:13px;background:rgba(255,255,255,0.10);"><div id="{sid}b{j}" style="height:26px;width:{int(860 * ms / 40)}px;border-radius:13px;background:{GREEN};transform-origin:0 50%;"></div></div></div>')
            at = vs + 0.1 + j * min(0.9, L * 0.75 / 3)
            word_in(f"#{sid}c{j}", at); T.append(f'tl.fromTo("#{sid}b{j}", {{scaleX:0}}, {{scaleX:1, duration:0.6, ease:"power2.out"}}, {at + 0.1:.2f});')
            sfx("pop", at, 0.5, 16 + j % 2)
    elif kind == "coupon":
        c += (f'<div id="{sid}h" class="c jk" style="top:440px;font-weight:800;font-size:60px;color:#fff;letter-spacing:4px;">PREMIUM PLANS PAR</div>'
              f'<div id="{sid}k" style="position:absolute;left:140px;top:600px;width:800px;height:420px;border-radius:40px;border:8px dashed {GREEN};background:rgba(17,24,39,0.85);box-shadow:0 0 70px rgba(34,197,94,0.3);">'
              f'<div class="c jk" style="top:60px;font-weight:700;font-size:50px;color:#9ca3af;letter-spacing:12px;">CODE</div><div class="c anton" style="top:140px;font-size:200px;color:#fff;">SKILL26</div></div>'
              f'<div id="{sid}o" class="c anton g" style="top:1080px;font-size:250px;text-shadow:0 0 70px rgba(34,197,94,0.55);">10% OFF</div>')
        word_in(f"#{sid}h", s0 + 0.1)
        T.append(f'tl.fromTo("#{sid}k", {{rotation:-6, scale:0.6, opacity:0}}, {{rotation:0, scale:1, opacity:1, duration:0.5, ease:"back.out(1.8)"}}, {beat(0.35):.2f});')
        T.append(f'tl.fromTo("#{sid}o", {{scale:0.2, opacity:0}}, {{scale:1, opacity:1, duration:0.45, ease:"back.out(2.4)"}}, {beat(0.65):.2f});')
        sfx("sparkle", beat(0.65), 0.35, 18)
    elif kind == "limited":
        top_line = "GAME SERVERS" if d.get("games") else "DHYAN DEIN!"
        c += (f'<div id="{sid}a" class="c jk" style="top:330px;font-weight:800;font-size:58px;color:{AMBER};letter-spacing:6px;">{top_line}</div>'
              + (f'<div id="{sid}e" class="c" style="top:430px;"><span class="card jk" style="display:inline-flex;align-items:center;gap:18px;padding:16px 40px;font-weight:800;font-size:52px;color:#fff;">{svg(ICON["cpu"], 70)}AMD EPYC 9</span></div>' if d.get("epyc") else "")
              + f'<div id="{sid}t" class="c" style="top:590px;display:flex;justify-content:center;gap:24px;"><div class="card jk tier">BUDGET</div><div class="card jk tier">STANDARD</div></div>'
              f'<div class="c jk" style="top:730px;font-weight:600;font-size:44px;color:#9ca3af;">plans</div>'
              f'<div id="{sid}l" class="c anton" style="top:820px;font-size:230px;color:#fff;text-shadow:0 0 60px rgba(34,197,94,0.7), 0 8px 30px rgba(0,0,0,0.8);">LIMITED!</div>'
              f'<div id="{sid}d" class="card jk" style="position:absolute;left:110px;top:1180px;width:860px;height:150px;display:flex;align-items:center;gap:30px;padding-left:46px;font-weight:800;font-size:50px;color:#fff;">{svg("M6 6h12v9h-7l-4 3v-3H6z", 76)}discord.gg/skilloraclouds</div>'
              f'<div id="{sid}w" class="card jk" style="position:absolute;left:110px;top:1360px;width:860px;height:150px;display:flex;align-items:center;gap:30px;padding-left:46px;font-weight:800;font-size:50px;color:#fff;">{svg("M12 3a9 9 0 1 0 0 18a9 9 0 1 0 0-18M3 12h18M12 3c-3.5 4-3.5 14 0 18M12 3c3.5 4 3.5 14 0 18", 76)}skilloraclouds.com</div>')
        word_in(f"#{sid}a", s0 + 0.1)
        if d.get("epyc"):
            pop_in(f"#{sid}e", s0 + 0.35)
        word_in(f"#{sid}t", beat(0.12))
        T.append(f'tl.fromTo("#{sid}l", {{scale:2.6, rotation:-8, opacity:0}}, {{scale:1, rotation:-4, opacity:1, duration:0.3, ease:"power4.in"}}, {beat(0.35):.2f});')
        T.append(f'tl.fromTo("#{sid}l", {{x:-12}}, {{x:12, duration:0.05, repeat:5, yoyo:true, ease:"none"}}, {beat(0.35) + 0.3:.2f});')
        T.append(f'tl.to("#{sid}l", {{x:0, duration:0.05}}, {beat(0.35) + 0.6:.2f});')
        sfx("impact-bass-1", beat(0.35) + 0.3, 0.35, 13)
        for j, sel in enumerate(("d", "w")):
            at = beat(0.6) + j * 0.3
            T.append(f'tl.fromTo("#{sid}{sel}", {{x:{-900 if j == 0 else 900}, opacity:0}}, {{x:0, opacity:1, duration:0.4, ease:"power3.out"}}, {at:.2f});'); sfx("pop", at, 0.5, 16 + j)
    elif kind == "cta":
        fs = 50 if d.get("small") else 70
        c += (f'<img id="{sid}g" src="assets/img/logo.png" style="position:absolute;left:390px;top:380px;width:300px;height:300px;" alt="SkilloraClouds logo">'
              f'<div id="{sid}n" class="c jk" style="top:720px;font-weight:800;font-size:100px;color:#fff;">Skillora<span class="g">Clouds</span></div>'
              f'<div id="{sid}c" class="c jk" style="top:930px;font-weight:700;font-size:56px;color:#e5e7eb;">Aaj hi visit karein</div>'
              f'<div id="{sid}u" class="c" style="top:1040px;"><span class="pill" style="font-size:{fs}px;">{d["url"]}</span></div>'
              f'<div id="{sid}d" class="c jk" style="top:1250px;font-weight:600;font-size:44px;color:#9ca3af;">discord.gg/skilloraclouds</div>')
        T.append(f'tl.fromTo("#{sid}g", {{scale:0.3, rotation:-25, opacity:0}}, {{scale:1, rotation:0, opacity:1, duration:0.6, ease:"back.out(1.8)"}}, {s0 + 0.1:.2f});')
        word_in(f"#{sid}n", s0 + 0.4); word_in(f"#{sid}c", s0 + 0.7)
        pop_in(f"#{sid}u", beat(0.5)); T.append(f'tl.to("#{sid}u", {{scale:1.05, duration:0.45, yoyo:true, repeat:3, ease:"sine.inOut"}}, {beat(0.5) + 0.5:.2f});')
        word_in(f"#{sid}d", beat(0.5) + 0.4); sfx("sparkle", beat(0.5), 0.35, 19)
    HT.append(c + "</div>")

CSS = f"""
@font-face {{ font-family:"Anton"; src:url("assets/fonts/Anton-Regular.ttf"); }}
@font-face {{ font-family:"Jakarta"; src:url("assets/fonts/PlusJakartaSans-Variable.ttf"); font-weight:200 800; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:{DARK}; }}
#root {{ position:absolute; inset:0; overflow:hidden; }}
.scene {{ position:absolute; inset:0; visibility:hidden; }} .fill {{ position:absolute; inset:0; }}
.c {{ position:absolute; left:0; right:0; text-align:center; }} .anton {{ font-family:Anton; letter-spacing:2px; line-height:0.95; }}
.jk {{ font-family:Jakarta; }} .g {{ color:{GREEN}; }} .sh {{ text-shadow:0 6px 30px rgba(0,0,0,0.85); }}
.pill {{ display:inline-block; padding:18px 44px; border-radius:999px; background:{GREEN}; color:#04140a; font-family:Jakarta; font-weight:800; font-size:64px; box-shadow:0 0 60px rgba(34,197,94,0.55); }}
.card {{ border-radius:34px; background:rgba(17,24,39,0.82); border:2px solid rgba(34,197,94,0.45); box-shadow:0 20px 60px rgba(0,0,0,0.5), 0 0 40px rgba(34,197,94,0.18); }}
.tier {{ padding:22px 46px; font-weight:800; font-size:64px; color:#fff; }}
"""
mus = spec["music"]
aud = [f'<audio id="vo" src="assets/vo/vo.wav" data-start="0" data-duration="{dur("assets/vo/vo.wav")}" data-volume="1" data-track-index="10"></audio>',
       f'<audio id="mus" src="assets/music/{mus}" data-start="0" data-duration="{TOTAL}" data-volume="0.16" data-track-index="11" data-fade-out="2"></audio>']
for i, (name, at, vol, lane) in enumerate(A):
    aud.append(f'<audio id="fx{i}" src="assets/sfx/{name}.mp3" data-start="{max(0, round(at, 2))}" data-duration="{dur(f"assets/sfx/{name}.mp3")}" data-volume="{vol}" data-track-index="{lane}"></audio>')
html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
<head><meta charset="UTF-8"><meta name="viewport" content="width={W}, height={H}">
<script src="assets/vendor/gsap-3.14.2.min.js"></script><style>{CSS}</style></head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="{W}" data-height="{H}">
  <div style="position:absolute;inset:0;background:radial-gradient(ellipse 80% 60% at 50% 35%, #0f2a1a 0%, {DARK} 60%);"></div>
  <div id="grid" data-layout-allow-overflow style="position:absolute;inset:-200px;background-image:linear-gradient(rgba(34,197,94,0.10) 2px, transparent 2px),linear-gradient(90deg, rgba(34,197,94,0.10) 2px, transparent 2px);background-size:90px 90px;"></div>
  {"".join(HT)}
  {"".join(aud)}
</div>
<script>
  const tl = gsap.timeline({{ paused: true }});
  tl.fromTo("#grid", {{ y: 0 }}, {{ y: 180, duration: {TOTAL}, ease: "none" }}, 0);
  {chr(10).join("  " + l for l in T)}
  window.__timelines = window.__timelines || {{}};
  window.__timelines["main"] = tl;
</script>
</body></html>
"""
open("index.html", "w").write(html)
print(reel, "built", TOTAL, "s,", n, "scenes,", len(A), "sfx")
