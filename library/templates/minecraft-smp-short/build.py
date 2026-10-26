# ALOO SMP YouTube Short (9:16). VO = client's own "smp promo.mp3" (retakes removed, see vo_map.json).
# Every on-screen claim is a word the VO says, or what the client sent (IP, port, Discord), or what the footage shows.
# Edit log: library/clients/mraloo/edit-log-short-v1.md
import json, os, subprocess

IN = "/tmp/claude-0/-home-user-new-startup/d818cf68-9ee4-503e-aa36-a24c445c7006/scratchpad/in"
LIB = "/home/user/new-startup/library"
W = json.load(open("words.json"))                       # [start, end, word] on the final VO clock
MUS = json.load(open("../music/upbeat-electronic--loyalty-freak-music--monarch-of-the-street.json"))
BEATS = MUS["rhythm"]["beats_s"]                        # music starts at t=0, so beats are timeline times
VO_END = 60.875
TOTAL = 62.6
GOLD, ORANGE, ICE, ICE2, NAVY = "#fcb43c", "#fc9c24", "#84ccfc", "#cce4fc", "#0c0c24"   # sampled from the emblem


def ws(i):
    return W[i][0]


def beat(t):
    """nearest music beat to t (cuts land on the beat, skill #96 / CLAUDE.md 'cut on bars')"""
    return min(BEATS, key=lambda b: abs(b - t))


# ---------------------------------------------------------------- shots
# (end_time, source, in_point, mode)  mode: crop = full-height 9:16 crop, fill = whole frame over blurred copy (#168),
# blur = blurred background plate for cards. Ends snap to beats except hard section points.
R, SP = "rec.mkv", "spawn.mkv"
RAW = [
    (beat(ws(4)), R, 102.8, "crop"),            # hook (102.8: no chat line in the crop): flying over spawn (most-motion seconds 102-107)
    (beat(ws(9)), R, 104.5, "crop"),
    (beat(ws(14)), R, 109.5, "crop"),
    (beat(ws(20)), R, 132.0, "crop"),
    (7.85, R, 136.5, "crop"),                   # "kyunki aaj"
    (9.6, R, 113.0, "blur"),                    # logo reveal plate
    (11.0, SP, 6.0, "fill"),                    # "ALOO SMP >> Welcome" chat must stay readable
    (beat(ws(32)), R, 119.0, "crop"),           # survival
    (beat(ws(34)), SP, 32.0, "crop"),           # OP PvP: another player close up
    (16.6, R, 140.0, "crop"),                   # mini games combo
    (beat(ws(45)), R, 116.0, "crop"),           # custom terrain
    (beat(ws(47)), R, 128.5, "crop"),           # custom enchantments
    (beat(ws(50)), SP, 26.5, "crop"),           # khatarnak PvP (punch-in)
    (beat(ws(52)), R, 168.5, "crop"),           # spawner, crates: market stalls with chests
    (beat(ws(55)), R, 63.6, "crop"),            # 55.6-61.5 had a chat line in the crop            # player economy: shop
    (26.43, R, 66.0, "crop"),
    (beat(ws(64)), R, 145.0, "crop"),           # 24x7 online
    (31.15, R, 150.8, "crop"),                  # no whitelist
    (beat(ws(76)), SP, 34.5, "crop"),           # Java + Bedrock players together
    (35.41, SP, 38.0, "crop"),
    (beat(ws(90)), R, 154.0, "crop"),           # banao apna base
    (39.36, R, 124.5, "crop"),                  # kamao paise
    (beat(ws(97)), R, 166.0, "crop"),           # crates kholo, OP items
    (42.78, R, 175.0, "crop"),
    (44.7, SP, 41.0, "crop"),                   # bano server ke...
    (46.1, SP, 44.5, "crop"),                   # ...sabse khatarnak player (punch-in on the hit)
    (48.1, SP, 46.5, "crop"),                   # doston ke saath (ends 48.1 so the tab-list clip fits its 1.03 s of source: QA2)
    (beat(ws(118)), SP, 50.0, "crop"),          # tab list: real online players on ALOO SMP
    (50.9, R, 172.4, "crop"),                   # QA1: 178.0 opened on a wall right in front of the camera
    (TOTAL, R, 170.0, "blur"),                  # end card plate
]
SHOTS, t = [], 0.0
for i, (e, src, inp, mode) in enumerate(RAW):
    SHOTS.append({"id": f"k{i:02d}", "start": round(t, 3), "dur": round(e - t, 3), "src": src, "in": inp, "mode": mode})
    t = e
DARK = {"k14", "k15"}    # watch.py: shop scenes luma 50-70 (dark) -> brighten (decision-guide section 12)
POP = {"k00", "k01", "k02"}  # skill #5250: grade should pop in the first 3 s

os.makedirs("assets/clips", exist_ok=True)
for s in SHOTS:
    out = f"assets/clips/{s['id']}.mp4"
    s["file"] = out
    if os.path.exists(out) and not os.environ.get("RECUT"):
        continue
    d = s["dur"] + 0.1
    eq = ",eq=gamma=1.28:brightness=0.03:saturation=1.08" if s["id"] in DARK else (",eq=saturation=1.2" if s["id"] in POP else "")
    if s["mode"] == "crop":
        vf = f"crop=ih*9/16:ih,scale=1080:1920:flags=lanczos,cas=strength=0.5{eq},fps=30,format=yuv420p"   # skill #489 (QA3: soft)
        args = ["-vf", vf]
    else:
        fg = "[fg]scale=1080:-2:flags=lanczos,cas=strength=0.5[fgs];[bgb][fgs]overlay=(W-w)/2:(H-h)/2" if s["mode"] == "fill" else ""
        bg = "[0:v]split[bg][fg];[bg]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=20:10" + \
             (",eq=brightness=-0.12" if s["mode"] == "blur" else "") + "[bgb]"
        if s["mode"] == "blur":
            fc = bg.replace("split[bg][fg];[bg]", "") + ";[bgb]fps=30,format=yuv420p[o]"
        else:
            fc = bg + ";" + fg + ",fps=30,format=yuv420p[o]"
        args = ["-filter_complex", fc, "-map", "[o]"]
    subprocess.run(["ffmpeg", "-v", "error", "-ss", str(s["in"]), "-t", f"{d:.3f}", "-i", f"{IN}/{s['src']}", *args,
                    "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-y", out], check=True)
json.dump(SHOTS, open("shots.json", "w"), indent=1)

CSS = f"""
    @font-face {{ font-family: "Anton"; src: url("assets/fonts/Anton-Regular.ttf"); }}
    @font-face {{ font-family: "Jakarta"; src: url("assets/fonts/PlusJakartaSans-Variable.ttf"); font-weight: 200 800; }}
    #root {{ position: absolute; inset: 0; overflow: hidden; }}
    .c {{ position: absolute; left: 0; right: 0; text-align: center; }}
    .anton {{ font-family: Anton; letter-spacing: 2px; line-height: 0.95; }}
    .jk {{ font-family: Jakarta; }}
    .stroke {{ -webkit-text-stroke: 10px {NAVY}; paint-order: stroke fill; }}
    .sh {{ text-shadow: 0 8px 28px rgba(0,0,0,0.75); }}
    .chip {{ display: inline-flex; align-items: center; gap: 18px; padding: 16px 34px; border-radius: 22px;
             background: rgba(12,12,36,0.86); border: 3px solid {ICE}; color: #fff; font-family: Jakarta; font-weight: 800;
             font-size: 50px; box-shadow: 0 14px 40px rgba(0,0,0,0.5), 0 0 30px rgba(132,204,252,0.35); }}
    .pill {{ display: inline-block; padding: 18px 44px; border-radius: 999px; background: {GOLD}; color: {NAVY};
             font-family: Jakarta; font-weight: 800; font-size: 60px; box-shadow: 0 0 50px rgba(252,180,60,0.55); }}
"""


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


C = {}
# ---------------------------------------------------------------- footage (one composition, wrappers carry motion)
SECTION_IN = {"k07", "k10", "k16", "k18", "k20", "k22", "k24", "k26", "k28"}   # zoom-through settles (template enter_exit)
PUNCH = {"k12": ws(49), "k25": ws(105)}   # punch-in + shake on the hit word (skills #150, #161; memes.md rule 4)
html, js = [], []
for s in SHOTS:
    i, st, d = s["id"], s["start"], s["dur"]
    html.append(f'    <div id="{i}-w" style="position:absolute;inset:0;" data-layout-allow-overflow><video id="{i}" class="clip" src="{s["file"]}" '
                f'data-start="{st}" data-duration="{d}" muted playsinline style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;"></video></div>')
    if i in SECTION_IN:
        js.append(f'    tl.fromTo("#{i}-w", {{ scale: 1.5, filter: "blur(14px)" }}, {{ scale: 1.0, filter: "blur(0px)", duration: 0.32, ease: "power3.out" }}, {st});')
    if i in PUNCH:
        h = PUNCH[i]
        js.append(f'    tl.fromTo("#{i}-w", {{ scale: 1.0 }}, {{ scale: 1.22, duration: 0.12, ease: "power4.out" }}, {h - 0.04:.2f});')
        js.append(f'    tl.fromTo("#{i}-w", {{ x: -18, y: 12 }}, {{ x: 16, y: -10, duration: 0.05, repeat: 5, yoyo: true, ease: "none" }}, {h:.2f});')
        js.append(f'    tl.to("#{i}-w", {{ x: 0, y: 0, duration: 0.06 }}, {h + 0.3:.2f});')
    if s["mode"] == "blur":
        js.append(f'    tl.fromTo("#{i}-w", {{ scale: 1.0 }}, {{ scale: 1.08, duration: {d}, ease: "none" }}, {st});')
# exits: zoom-through out of the shot before each section start
for s in SHOTS:
    nxt = [x for x in SHOTS if x["start"] == round(s["start"] + s["dur"], 3)]
    if nxt and nxt[0]["id"] in SECTION_IN:
        e = s["start"] + s["dur"]
        js.append(f'    tl.to("#{s["id"]}-w", {{ scale: 1.4, filter: "blur(14px)", duration: 0.2, ease: "power3.in" }}, {e - 0.2:.2f});')
C["footage"] = comp("footage", "\n".join(html), "\n".join(js))

# ---------------------------------------------------------------- graphics overlays (one composition per beat of the story)
def tick(color=ICE):
    return (f'<svg viewBox="0 0 40 40" style="width:46px;height:46px;flex:none;"><circle cx="20" cy="20" r="19" fill="{color}"/>'
            f'<path d="M11 21 L18 27 L29 14" stroke="{NAVY}" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>')


G = []   # (cid, start, dur)
# hook title on screen at t=0 (frame 0 = thumbnail, CLAUDE.md; vertical.md "one bold line already on screen")
d = round(ws(14) - 0.02, 2)
C["hook"] = comp("hook", f"""    <div id="h-veil" style="position:absolute;left:0;right:0;top:0;height:900px;background:linear-gradient(to bottom, rgba(12,12,36,0.75), rgba(12,12,36,0));"></div>
    <div id="h-w" class="c" style="top:260px;">
      <div id="h-a" class="anton stroke sh" style="font-size:150px;color:#fff;">DHAASU</div>
      <div id="h-b" class="anton stroke sh" style="font-size:190px;color:{GOLD};margin-top:6px;">INDIAN SMP</div>
      <div id="h-c" class="jk stroke sh" style="font-weight:800;font-size:64px;color:{ICE2};margin-top:22px;">DHOONDH RAHE HO?</div>
    </div>""",
    f'    tl.fromTo("#h-b", {{ scale: 1.12 }}, {{ scale: 1, duration: 1.0, ease: "power2.out" }}, 0);\n'
    f'    tl.fromTo("#h-b", {{ x: -10 }}, {{ x: 10, duration: 0.05, repeat: 5, yoyo: true, ease: "none" }}, {ws(9):.2f});\n'
    f'    tl.to("#h-b", {{ x: 0, duration: 0.05 }}, {ws(9) + 0.3:.2f});\n'
    f'    tl.fromTo("#h-c", {{ scale: 0.6 }}, {{ scale: 1, duration: 0.3, ease: "back.out(2.2)" }}, {ws(11):.2f});\n'
    f'    tl.to("#h-w", {{ scale: 1.35, filter: "blur(14px)", opacity: 0, duration: 0.22, ease: "power3.in" }}, {d - 0.22:.2f});\n'
    f'    tl.to("#h-veil", {{ opacity: 0, duration: 0.22 }}, {d - 0.22:.2f});')
G.append(("hook", 0, d))

# logo reveal on "ALOO SMP": white flash (skill #122 impact) + emblem + shake (#161)
st = round(ws(23) - 0.08, 2); d = round(9.6 - st, 2)
C["logo"] = comp("logo", f"""    <div id="l-glow" style="position:absolute;left:90px;top:280px;width:900px;height:900px;border-radius:50%;background:radial-gradient(circle, rgba(252,180,60,0.45), rgba(252,180,60,0) 70%);"></div>
    <div id="l-card" style="position:absolute;left:220px;top:380px;width:640px;height:640px;border-radius:60px;overflow:hidden;border:6px solid {GOLD};box-shadow:0 30px 80px rgba(0,0,0,0.6), 0 0 80px rgba(252,180,60,0.5);">
      <img src="assets/img/emblem.jpg" style="width:100%;height:100%;object-fit:cover;" alt="ALOO SMP emblem">
    </div>
    <div id="l-flash" style="position:absolute;inset:0;background:#fffdf5;"></div>""",
    '    tl.fromTo("#l-flash", { opacity: 0.95 }, { opacity: 0, duration: 0.45, ease: "power2.out" }, 0);\n'
    '    tl.fromTo("#l-card", { scale: 1.6, rotation: -6, opacity: 0 }, { scale: 1, rotation: 0, opacity: 1, duration: 0.35, ease: "power4.out" }, 0);\n'
    '    tl.fromTo("#l-card", { x: -14, y: 10 }, { x: 12, y: -8, duration: 0.05, repeat: 5, yoyo: true, ease: "none" }, 0.33);\n'
    '    tl.to("#l-card", { x: 0, y: 0, duration: 0.05 }, 0.63);\n'
    f'    tl.to("#l-card", {{ scale: 1.06, duration: {d - 0.9:.2f}, ease: "sine.inOut" }}, 0.65);\n'
    '    tl.fromTo("#l-glow", { scale: 0.7, opacity: 0 }, { scale: 1.1, opacity: 1, duration: 0.6, ease: "power2.out" }, 0.05);\n'
    f'    tl.to(["#l-card", "#l-glow"], {{ scale: 1.4, filter: "blur(14px)", opacity: 0, duration: 0.22, ease: "power3.in" }}, {d - 0.22:.2f});')
G.append(("logo", st, d))


def checklist(cid, items, start, end, top=300):
    """feature chips popping on the spoken word, stacked (template s3 chips)"""
    h = "".join(f'      <div class="c" id="{cid}-{n}" style="top:{top + n * 118}px;"><span class="chip">{tick()}{txt}</span></div>\n'
                for n, (txt, _) in enumerate(items))
    j = "".join(f'    tl.fromTo("#{cid}-{n}", {{ x: -700, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.3, ease: "back.out(1.6)" }}, {t - start:.2f});\n'
                for n, (_, t) in enumerate(items))
    j += f'    tl.to("#{cid}-w", {{ x: 900, opacity: 0, duration: 0.22, ease: "power3.in" }}, {end - start - 0.22:.2f});\n'
    C[cid] = comp(cid, f'    <div id="{cid}-w" style="position:absolute;inset:0;">\n{h}    </div>', j)
    G.append((cid, round(start, 2), round(end - start, 2)))
    return [t for _, t in items]


POPS = []
POPS += checklist("f1", [("SURVIVAL", ws(31)), ("OP PvP", ws(32)), ("MINI GAMES", ws(36))], ws(29), 16.6)
POPS += checklist("f2", [("CUSTOM TERRAIN", ws(43)), ("CUSTOM ENCHANTMENTS", ws(45)), ("KHATARNAK PvP", ws(47)),
                         ("SPAWNER", ws(50)), ("CRATES", ws(51))], 16.6, ws(52) + 0.3, top=280)
POPS += checklist("f3", [("PLAYER ECONOMY", ws(55))], ws(53), 26.43, top=330)

# 24x7 online + no whitelist stamp (meme format: stamp + hit SFX, memes.md rule 4)
st = 26.43; d = round(31.15 - st, 2)
C["online"] = comp("online", f"""    <div id="o-w" style="position:absolute;inset:0;">
      <div class="c anton stroke sh" id="o-num" style="top:300px;font-size:250px;color:#fff;">24x7</div>
      <div class="c" id="o-on" style="top:570px;"><span class="chip" style="font-size:60px;border-color:#22c55e;"><span id="o-dot" style="width:34px;height:34px;border-radius:50%;background:#22c55e;box-shadow:0 0 24px #22c55e;"></span>ONLINE</span></div>
      <div class="c" id="o-wl" style="top:760px;"><span class="anton" style="display:inline-block;padding:14px 40px;border:10px solid #ef4444;border-radius:24px;color:#ef4444;font-size:120px;background:rgba(12,12,36,0.7);">NO WHITELIST</span></div>
    </div>""",
    f'    tl.fromTo("#o-num", {{ scale: 0.3, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2.2)" }}, {ws(62) - st:.2f});\n'
    f'    tl.fromTo("#o-on", {{ y: 40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.3, ease: "power3.out" }}, {ws(63) - st:.2f});\n'
    f'    tl.fromTo("#o-dot", {{ opacity: 1 }}, {{ opacity: 0.3, duration: 0.4, repeat: 5, yoyo: true, ease: "sine.inOut" }}, {ws(63) - st + 0.3:.2f});\n'
    f'    tl.fromTo("#o-wl", {{ scale: 2.6, rotation: -14, opacity: 0 }}, {{ scale: 1, rotation: -6, opacity: 1, duration: 0.22, ease: "power4.in" }}, {ws(67) - st:.2f});\n'
    f'    tl.fromTo("#o-wl", {{ x: -12 }}, {{ x: 12, duration: 0.05, repeat: 5, yoyo: true, ease: "none" }}, {ws(67) - st + 0.22:.2f});\n'
    f'    tl.to("#o-wl", {{ x: 0, duration: 0.05 }}, {ws(67) - st + 0.52:.2f});\n'
    f'    tl.to("#o-w", {{ scale: 1.35, filter: "blur(14px)", opacity: 0, duration: 0.22, ease: "power3.in" }}, {d - 0.22:.2f});')
G.append(("online", st, d))

# Java + Bedrock
st = 31.15; d = round(35.41 - st, 2)
C["jb"] = comp("jb", f"""    <div id="jb-w" style="position:absolute;inset:0;">
      <div class="c jk stroke sh" style="top:290px;font-weight:800;font-size:58px;color:{ICE2};letter-spacing:6px;">SABSE BADI BAAT</div>
      <div class="c" id="jb-j" style="top:420px;"><span class="chip" style="font-size:96px;padding:22px 60px;border-color:{GOLD};">JAVA</span></div>
      <div class="c anton stroke" id="jb-p" style="top:590px;font-size:130px;color:{GOLD};">+</div>
      <div class="c" id="jb-b" style="top:740px;"><span class="chip" style="font-size:96px;padding:22px 60px;border-color:{ICE};">BEDROCK</span></div>
    </div>""",
    f'    tl.fromTo("#jb-j", {{ x: -900 }}, {{ x: 0, duration: 0.35, ease: "power3.out" }}, {ws(74) - st:.2f});\n'
    f'    tl.fromTo("#jb-p", {{ scale: 0, rotation: -90 }}, {{ scale: 1, rotation: 0, duration: 0.3, ease: "back.out(2.4)" }}, {ws(75) - st - 0.15:.2f});\n'
    f'    tl.fromTo("#jb-b", {{ x: 900 }}, {{ x: 0, duration: 0.35, ease: "power3.out" }}, {ws(75) - st:.2f});\n'
    f'    tl.fromTo("#jb-w", {{ scale: 1 }}, {{ scale: 1.05, duration: 0.25, ease: "power2.out", yoyo: true, repeat: 1 }}, {ws(78) - st:.2f});\n'
    f'    tl.to("#jb-w", {{ scale: 1.35, filter: "blur(14px)", opacity: 0, duration: 0.22, ease: "power3.in" }}, {d - 0.22:.2f});')
G.append(("jb", st, d))

POPS += checklist("f4", [("APNA BASE", ws(89)), ("PAISE", ws(91))], ws(87), 39.36, top=330)
POPS += checklist("f5", [("CRATES", ws(92)), ("OP ITEMS", ws(95))], ws(92) - 0.05, 42.78, top=330)

# end section: emblem, IP, port, join, Discord (client's message 2026-10-25; invite checked via discord.com API)
st = 50.9; d = round(TOTAL - st, 2)
C["end"] = comp("end", f"""    <div id="e-w" style="position:absolute;inset:0;">
      <div id="e-logo" style="position:absolute;left:350px;top:200px;width:380px;height:380px;border-radius:40px;overflow:hidden;border:5px solid {GOLD};box-shadow:0 0 60px rgba(252,180,60,0.45);">
        <img src="assets/img/emblem.jpg" style="width:100%;height:100%;object-fit:cover;" alt="ALOO SMP emblem"></div>
      <div class="c" id="e-ip" style="top:640px;"><span class="chip" style="font-size:58px;border-color:{GOLD};"><span style="color:{GOLD};">IP</span>play.aloosmp.fun</span></div>
      <div class="c" id="e-port" style="top:790px;"><span class="chip" style="font-size:50px;"><span style="color:{ICE};">PORT</span>19132 <span style="font-size:36px;color:{ICE2};">(Bedrock)</span></span></div>
      <div class="c" id="e-join" style="top:930px;"><span class="pill">ABHI JOIN KARO!</span></div>
      <div class="c" id="e-dc" style="top:640px;"><span class="chip" style="font-size:52px;border-color:#5865f2;"><span style="color:#8b93ff;">DISCORD</span>discord.gg/e89HSbjd5Y</span></div>
      <div class="c jk stroke sh" id="e-desc" style="top:790px;font-weight:800;font-size:46px;color:#fff;">Link description mein</div>
      <div class="c" id="e-ip2" style="top:930px;"><span class="chip" style="font-size:58px;border-color:{GOLD};"><span style="color:{GOLD};">IP</span>play.aloosmp.fun</span></div>
    </div>""",
    '    tl.fromTo("#e-logo", { scale: 0.3, rotation: -20, opacity: 0 }, { scale: 1, rotation: 0, opacity: 1, duration: 0.5, ease: "back.out(1.8)" }, 0.1);\n'
    f'    tl.to("#e-logo", {{ scale: 0.6, opacity: 0, duration: 0.25, ease: "power2.in" }}, {ws(133) - st - 0.25:.2f});\n'
    f'    tl.to("#e-logo", {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(1.8)" }}, {ws(147) - st:.2f});\n'
    f'    tl.fromTo("#e-ip", {{ scale: 0.4, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2)" }}, {ws(129) - st:.2f});\n'
    f'    tl.fromTo("#e-port", {{ scale: 0.4, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2)" }}, {ws(132) - st:.2f});\n'
    f'    tl.fromTo("#e-join", {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2.2)" }}, {ws(136) - st:.2f});\n'
    f'    tl.to("#e-join", {{ scale: 1.07, duration: 0.3, ease: "sine.inOut", yoyo: true, repeat: 5 }}, {ws(136) - st + 0.4:.2f});\n'
    f'    tl.to(["#e-ip", "#e-port", "#e-join"], {{ y: -40, opacity: 0, duration: 0.25, ease: "power2.in" }}, {ws(147) - st:.2f});\n'
    f'    tl.fromTo("#e-dc", {{ scale: 0.4, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2)" }}, {ws(150) - st:.2f});\n'
    f'    tl.fromTo("#e-desc", {{ y: 30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.3, ease: "power3.out" }}, {ws(152) - st:.2f});\n'
    f'    tl.fromTo("#e-ip2", {{ scale: 0.4, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2)" }}, {ws(152) - st + 0.5:.2f});')
G.append(("end", st, d))

# ---------------------------------------------------------------- captions: Roman Urdu (Hinglish) groups, words appear as spoken
GROUPS = [([0, 1, 2], "Bhai agar tum"), ([3, 4, 5, 6], "*Minecraft khelne ke liye"), ([7, 8], "ek *dhaasu"),
    ([9, 10], "*Indian SMP"), ([11, 12, 13], "dhoondh rahe ho"), ([14, 15, 16], "to ye video"), ([17, 18, 19], "*tumhare liye hai"),
    ([20, 21], "kyunki aaj"), ([23, 24], "*ALOO SMP"), ([25, 26], "ek aisa"), ([27, 28], "*Minecraft server"),
    ([29, 30, 31], "jahan milega *Survival"), ([32, 33], "*OP PvP"), ([34, 35], "aur mazedaar"), ([36, 37], "*mini games"),
    ([38, 39, 40], "ka tagda *combo"), ([41, 42], "yahan hai"), ([43, 44], "*custom terrain"), ([45, 46], "*custom enchantments"),
    ([47, 49], "*khatarnak PvP"), ([50], "*spawner"), ([51], "*crates"), ([52, 53, 54], "aur ek shandaar"),
    ([55, 56], "*player economy"), ([57, 58, 59], "aur haan bhai"), ([60, 61], "server hai"), ([62, 63], "*24x7 online"),
    ([64, 65, 66], "aur koi bhi"), ([67, 68, 69], "*whitelist nahi hai"), ([70, 71, 72, 73], "aur sabse *badi baat"),
    ([74, 75], "*Java Bedrock"), ([76, 77], "khiladi saath_mein"), ([78, 79, 80], "*khel sakte hain"), ([81, 82], "to bhai"),
    ([83, 84, 85, 86], "der kis baat ka"), ([87, 88, 89], "banao apna *base"), ([90, 91], "kamao *paise"),
    ([92, 93], "*crates kholo"), ([94, 95, 96], "khareedo *OP items"), ([97, 98, 99], "apne rival se"),
    ([100, 101, 102, 103], "aur bano server ke"), ([104, 105, 106], "sabse *khatarnak player"), ([107, 108, 109], "to bhai jaldi"),
    ([110, 111], "apne *doston"), ([112, 113, 114], "ke saath aao"), ([115, 116, 117], "aur apni *SMP"),
    ([118, 119, 120], "journey shuru karo"), ([121, 122, 123], "to der kis"), ([124, 125, 126], "baat ka bhai"),
    ([127, 128, 129], "ye raha *IP"), ([130, 131, 132], "ye raha *port"), ([133, 134, 135], "abhi server ko"),
    ([136, 137], "*join karo"), ([138, 139, 140], "aur agar tumhe"), ([141, 142], "server ke"), ([144, 145, 146], "*update rehna hai"),
    ([147, 148, 149], "to join karo"), ([150, 151], "apna *Discord"), ([152, 153, 154, 155], "*description mein link hai")]
html, js = [], []
for g, (idx, text) in enumerate(GROUPS):
    words = text.split()
    assert len(words) == len(idx), text
    st = W[idx[0]][0]
    end = min(GROUPS[g + 1] and W[GROUPS[g + 1][0][0]][0], W[idx[-1]][1] + 0.6) if g + 1 < len(GROUPS) else VO_END + 0.3
    end = max(end, W[idx[-1]][0] + 0.25)
    if g + 1 < len(GROUPS):
        end = min(end, W[GROUPS[g + 1][0][0]][0])   # never overlap the next group (QA1: 17.6 s)
    sp = []
    for k, (wi, w) in enumerate(zip(idx, words)):
        gold = w.startswith("*")
        w = w.lstrip("*").replace("_", " ")
        sp.append(f'<span id="g{g}w{k}" style="display:inline-block;margin:0 0.13em;color:{GOLD if gold else "#fff"};">{w}</span>')
        js.append(f'    tl.fromTo("#g{g}w{k}", {{ opacity: 0, scale: 0.6, y: 16 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.12, ease: "back.out(2.5)" }}, {max(W[wi][0], st):.2f});')
    html.append(f'    <div id="g{g}" class="c jk stroke" style="top:1130px;padding:0 70px;font-weight:800;font-size:84px;line-height:1.08;opacity:0;'
                f'text-shadow:0 6px 22px rgba(0,0,0,0.8);">{" ".join(sp)}</div>')
    js.append(f'    tl.set("#g{g}", {{ opacity: 1, visibility: "visible" }}, {st:.2f});')
    js.append(f'    tl.to("#g{g}", {{ opacity: 0, duration: 0.1, ease: "power2.in" }}, {end - 0.1:.2f});')
    js.append(f'    tl.set("#g{g}", {{ opacity: 0, visibility: "hidden" }}, {end:.2f});')
C["captions"] = comp("captions", "\n".join(html), "\n".join(js))

# ---------------------------------------------------------------- PiP overlays from the spawn recording (skill #439/#578,
# hyperframes overlays.md; owner request 2026-10-26). Card = real footage, ice border, drop shadow.
def pipcard(cid, src, x, y, w, h, start, end, vstart=0):
    d = round(end - start, 2)
    media = (f'<img id="{cid}-v" class="clip" src="{src}" data-start="0" data-duration="{d}" alt="ALOO SMP server list entry" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;">'
             if src.endswith(".jpg") else
             f'<video id="{cid}-v" class="clip" src="{src}" data-start="0" data-duration="{d}" muted playsinline style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;"></video>')
    C[cid] = comp(cid, f"""    <div id="{cid}-w" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:26px;overflow:hidden;border:5px solid {ICE};box-shadow:0 24px 60px rgba(0,0,0,0.65), 0 0 40px rgba(132,204,252,0.35);">
      {media}
    </div>""",
        f'    tl.fromTo("#{cid}-w", {{ scale: 0.5, y: 80, opacity: 0 }}, {{ scale: 1, y: 0, opacity: 1, duration: 0.35, ease: "back.out(1.7)" }}, 0);\n'
        f'    tl.to("#{cid}-w", {{ scale: 0.6, y: 60, opacity: 0, duration: 0.22, ease: "power2.in" }}, {d - 0.22:.2f});')
    G.append((cid, round(start, 2), d))


pipcard("pip1", "assets/img/pip_slist.jpg",    40, 560, 1000, 232, ws(20), 7.85)          # "kyunki aaj ... ALOO SMP": real server-list entry
pipcard("pip2", "assets/clips/pip_join.mp4", 140, 175, 800, 450, ws(133), ws(147))      # "abhi server ko join karo": real join sequence

os.makedirs("compositions", exist_ok=True)
for k, v in C.items():
    open(f"compositions/{k}.html", "w").write(v)

hosts = [f'      <div id="footage-h" data-composition-id="footage" data-composition-src="compositions/footage.html" data-start="0" data-duration="{TOTAL}" data-track-index="0" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: 0"></div>']
for n, (cid, st, d) in enumerate(G):
    hosts.append(f'      <div id="{cid}-h" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" data-start="{st}" data-duration="{d}" data-track-index="{1 + n % 2}" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: 2"></div>')
hosts.append(f'      <div id="captions-h" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{TOTAL}" data-track-index="3" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index: 3"></div>')

# ---------------------------------------------------------------- audio
def dur(p):
    return round(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                      capture_output=True, text=True).stdout), 3)


SFX = {"whoosh": "transition/whoosh-fast-0.3s.mp3", "pop": "pop/pop-high.mp3", "boom": "impact/impact-boom.mp3",
       "punch": "impact/impact-punch.mp3", "coin": "game/game-coin.mp3", "level": "game/game-levelup.mp3",
       "chime": "notification/success-chime.mp3", "sparkle": "magic/sparkle.mp3", "sub": "impact/sub-drop.mp3"}
os.makedirs("assets/sfx", exist_ok=True)
for k, f in SFX.items():
    subprocess.run(["cp", f"{LIB}/sfx/{f}", f"assets/sfx/{k}.mp3"], check=True)
HIT = {"whoosh": 0.172, "sparkle": 0.451, "chime": 0.276}   # index.json hit_s: peak lands on the cut / word
A = [("vo", "assets/vo/vo.wav", 0, dur("assets/vo/vo.wav"), 1.0, 10, 0, 0),
     ("m1", "assets/music/music.mp3", 0, round(VO_END + 0.1, 2), 0.16, 11, 0, 0),
     ("m2", "assets/music/music.mp3", round(VO_END + 0.1, 2), round(TOTAL - VO_END - 0.1, 2), 0.45, 12, round(VO_END + 0.1, 2), 1.4)]
n = 0


def sfx(k, t, v):
    global n
    n += 1
    A.append((f"{k}{n}", f"assets/sfx/{k}.mp3", round(max(0, t - HIT.get(k, 0)), 2), dur(f"assets/sfx/{k}.mp3"), v, 13 + n, 0, 0))


for s in SHOTS:
    if s["id"] in SECTION_IN:
        sfx("whoosh", s["start"], 0.4)
for t in POPS:
    sfx("pop", t, 0.3)
sfx("boom", ws(23) - 0.08, 0.32)            # logo hit
sfx("sub", ws(9), 0.12)                     # hook "INDIAN SMP" shake
sfx("punch", ws(49), 0.3)                  # khatarnak PvP punch-in
sfx("punch", ws(67), 0.32)                 # NO WHITELIST stamp
sfx("coin", ws(56), 0.12)                  # economy
sfx("coin", ws(91), 0.12)                  # paise
sfx("boom", ws(105), 0.32)                  # khatarnak player punch-in
sfx("level", ws(119), 0.07)                # "SMP journey shuru karo"
sfx("chime", ws(136), 0.3)                 # join karo
sfx("sparkle", ws(150), 0.3)               # Discord card
sfx("whoosh", 50.9, 0.4)
sfx("pop", ws(20), 0.3)                   # PiP 1 card pops in
sfx("whoosh", ws(133), 0.35)              # PiP 2 join-sequence card
aud = "\n".join(
    f'      <audio id="{i}" src="{s}" data-start="{st}" data-duration="{d}" data-volume="{v}" data-track-index="{ln}"'
    + (f' data-media-start="{ms}"' if ms else "") + (f' data-fade-out="{fo}"' if fo else "") + "></audio>"
    for i, s, st, d, v, ln, ms, fo in A)

open("index.html", "w").write(f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap-3.14.2.min.js"></script>
    <style>* {{ margin: 0; padding: 0; box-sizing: border-box; }} html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: {NAVY}; }}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
{chr(10).join(hosts)}
{aud}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
""")
print("built", TOTAL, "shots", len(SHOTS), "groups", len(GROUPS), "sfx", n)
