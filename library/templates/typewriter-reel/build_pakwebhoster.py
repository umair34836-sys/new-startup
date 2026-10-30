# PakWebHoster typewriter reel (9:16, 20 s, text + CC0 music, no VO). 2026-10-25.
# Claims from pakwebhoster.com read in Playwright on 2026-10-25 (library/clients/pakwebhoster/site-data.md):
# meta "Cheap web hosting in Pakistan" [/]; Starter Lite "PKR 200 /mo", "PKR 2000 / Year (2 Month Free)",
# "10 GB NVMe Storage", "Unlimited Bandwidth", "Free SSL Certificate", "24/7 Live Support" [/shared-hosting];
# "LiteSpeed Webserver" [/wordpress, /business-hosting]; phone +923243458649 [footer].
# Skills: #408 typewriter text (vary the gaps between characters, everything on the GSAP timeline, no timers),
# #2560 typing on the timeline; characters shown with tl.set(display) so a caret follows the last typed char.
import random, subprocess

W, H, TOTAL = 1080, 1920, 20.0
GREEN, NAVY, LIME, BG = "#2a862e", "#1a2f3b", "#01c062", "#f0f7fd"   # site CSS --color-one, logo navy/green, --color-four
rnd = random.Random(7)


def dur(p):
    return round(float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                      capture_output=True, text=True).stdout), 3)


T, A, PRE = [], [], []
LINES = []   # (id, html_before, text, html_after, style, start)


def type_line(lid, text, t0, rate=0.045, cls="", style=""):
    """characters appear one by one with uneven gaps (#408); returns end time"""
    spans, t = [], t0
    times = []
    for i, ch in enumerate(text):
        c = "&nbsp;" if ch == " " else ch.replace("&", "&amp;").replace("<", "&lt;")
        spans.append(f'<span id="{lid}c{i}" class="ch">{c}</span>')
        times.append(round(t, 3))
        gap = rate * rnd.uniform(0.55, 1.6) * (2.2 if ch in ",?." else 1.0)
        t += gap
    LINES.append(f'<div id="{lid}" class="line {cls}" style="{style}">{"".join(spans)}<span id="{lid}k" class="caret"></span></div>')
    PRE.append(f'gsap.set("#{lid}", {{display:"none"}});')
    T.append(f'tl.set("#{lid}", {{display:"block"}}, {t0});')
    for i, tt in enumerate(times):
        T.append(f'tl.set("#{lid}c{i}", {{display:"inline"}}, {tt});')
    end = round(t, 3)
    # caret: visible while typing this line, then hidden when the next line starts (set by caller via hide_caret)
    PRE.append(f'gsap.set("#{lid}k", {{display:"none"}});')
    T.append(f'tl.set("#{lid}k", {{display:"inline-block"}}, {t0});')
    # typing sound for the length of the line (keyboard loop, different offset per line)
    A.append((f"ty_{lid}", "typing-keyboard-medium", t0, round(end - t0 + 0.05, 3), 0.55, round(rnd.uniform(0.3, 2.5), 2)))
    return end


def caret_off(lid, t):
    T.append(f'tl.set("#{lid}k", {{display:"none"}}, {t});')


def enter(t):
    A.append((f"en{len(A)}", "keypress", t, None, 0.7, 0))


# ---- the editor card ---------------------------------------------------------------------------------------------
seq = [("l1", "> Apni website banani hai?", 0.35, "", ""),
       ("l2", "> Cheap aur fast hosting chahiye?", 1.95, "", ""),
       ("l3", "Starter Lite plan", 4.3, "head", ""),
       ("l4", "✓ 10 GB NVMe Storage", 5.45, "spec", ""),
       ("l5", "✓ Unlimited Bandwidth", 6.65, "spec", ""),
       ("l6", "✓ Free SSL Certificate", 7.85, "spec", ""),
       ("l7", "✓ LiteSpeed Webserver", 9.05, "spec", ""),
       ("l8", "✓ 24/7 Live Support", 10.25, "spec", ""),
       ("l9", "PKR 200 /mo", 11.55, "price", ""),
       ("l10", "PKR 2000 / Year (2 Month Free)", 12.95, "year", "")]
ends = []
for i, (lid, txt, t0, cls, st) in enumerate(seq):
    rate = 0.06 if cls == "price" else 0.045
    e = type_line(lid, txt, t0, rate=rate, cls=cls, style=st)
    ends.append(e)
    if i:
        caret_off(seq[i - 1][0], t0)
    enter(round(e + 0.08, 3))
    assert i + 1 == len(seq) or e < seq[i + 1][2], (lid, e)
caret_off("l10", 14.6)
# price line: pop + cash when it finishes
T.append(f'tl.fromTo("#l9", {{scale:1}}, {{scale:1.08, duration:0.18, yoyo:true, repeat:1, ease:"power2.out"}}, {ends[8]});')
A.append(("cash", "cash-register", ends[8], None, 0.45, 0))
for k, t in (("l3", ends[2]), ("l4", ends[3]), ("l5", ends[4]), ("l6", ends[5]), ("l7", ends[6]), ("l8", ends[7])):
    A.append((f"pl{k}", "pluck", t, None, 0.45, 0))

# card leaves, end screen with the URL typed in an address bar
T.append('tl.to(["#card","#top-logo"], {y:-80, opacity:0, duration:0.45, ease:"power3.in"}, 14.6);')
A.append(("wh", "whoosh-down-0.6s", 14.5, None, 0.45, 0))
T.append('tl.fromTo("#end", {opacity:0}, {opacity:1, duration:0.4}, 15.0);')
T.append('tl.fromTo("#e-logo", {scale:0.6, opacity:0}, {scale:1, opacity:1, duration:0.5, ease:"back.out(1.7)"}, 15.1);')
T.append('tl.fromTo("#e-bar", {width:120, opacity:0}, {width:900, opacity:1, duration:0.5, ease:"power3.inOut"}, 15.55);')
e_url = type_line("eu", "pakwebhoster.com", 16.1, rate=0.055, style="font-size:66px;font-weight:700;margin:0;")
A.append(("conf", "confirm-1", round(e_url + 0.1, 3), None, 0.6, 0))
T.append(f'tl.fromTo("#e-bar", {{boxShadow:"0 0 0 0 rgba(1,192,98,0)"}}, {{boxShadow:"0 0 0 14px rgba(1,192,98,0.35)", duration:0.3, yoyo:true, repeat:1}}, {round(e_url + 0.1, 3)});')
e_ph = type_line("ep", "Call / WhatsApp: +92 324 3458649", round(e_url + 0.45, 3), rate=0.03, cls="phone")
assert e_ph < TOTAL - 0.8, e_ph
caret_off("eu", round(e_url + 0.45, 3))

card_lines = "\n".join(LINES[:10])
end_lines = LINES[10:]

CSS = f"""
@font-face {{ font-family: "Manrope"; src: url("assets/fonts/Manrope-Variable.ttf"); font-weight: 200 800; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:{BG}; }}
#root {{ position:absolute; inset:0; overflow:hidden; }}
.line {{ font-family:"JetBrains Mono", monospace; font-size:42px; color:{NAVY}; line-height:1.25; margin-bottom:30px; white-space:nowrap; }}
.ch {{ display:none; }}
.caret {{ display:inline-block; width:22px; height:52px; margin-left:4px; vertical-align:-8px; background:{GREEN}; }}
.head {{ font-weight:800; color:{GREEN}; font-size:60px; margin-top:40px; }}
.spec {{ font-size:50px; }}
.price {{ font-family:Manrope; font-weight:800; font-size:126px; color:{GREEN}; margin-top:30px; line-height:1.05; transform-origin:0 50%; }}
.price .caret {{ height:120px; vertical-align:-14px; }}
.year {{ font-size:42px; color:#4a5568; }}
.phone {{ font-size:46px; color:{NAVY}; text-align:center; }}
"""

html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width={W}, height={H}">
<script src="assets/vendor/gsap-3.14.2.min.js"></script>
<style>{CSS}</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="{W}" data-height="{H}">
  <div style="position:absolute;inset:0;background-image:linear-gradient(rgba(26,47,59,0.05) 2px, transparent 2px),linear-gradient(90deg, rgba(26,47,59,0.05) 2px, transparent 2px);background-size:60px 60px;"></div>
  <div id="top-logo" style="position:absolute;left:170px;top:140px;width:740px;height:200px;background:#fff;border-radius:30px;box-shadow:0 14px 40px rgba(26,47,59,0.10);display:flex;align-items:center;justify-content:center;"><img src="assets/img/logo.png" style="width:680px;height:157px;" alt="PakWebHoster logo"></div>
  <div id="card" style="position:absolute;left:60px;top:400px;width:960px;height:1190px;background:#fff;border-radius:34px;box-shadow:0 30px 80px rgba(26,47,59,0.14);overflow:hidden;">
    <div style="height:84px;background:{NAVY};display:flex;align-items:center;gap:16px;padding-left:34px;">
      <div style="width:22px;height:22px;border-radius:50%;background:#ff5f57;"></div>
      <div style="width:22px;height:22px;border-radius:50%;background:#febc2e;"></div>
      <div style="width:22px;height:22px;border-radius:50%;background:#28c840;"></div>
      <div style="margin-left:24px;font-family:'JetBrains Mono';font-size:30px;color:#cbd5e1;">pakwebhoster.txt</div>
    </div>
    <div style="padding:46px 50px 0;">
{card_lines}
    </div>
  </div>
  <div id="end" style="position:absolute;inset:0;opacity:0;">
    <div id="e-logo" style="position:absolute;left:90px;top:520px;width:900px;height:250px;background:#fff;border-radius:40px;box-shadow:0 20px 60px rgba(26,47,59,0.15);display:flex;align-items:center;justify-content:center;"><img src="assets/img/logo.png" style="width:820px;height:189px;" alt="PakWebHoster logo"></div>
    <div id="e-bar" style="position:absolute;left:50%;top:860px;width:900px;height:130px;transform:translateX(-50%);background:#fff;border-radius:65px;
         box-shadow:0 20px 60px rgba(26,47,59,0.15);display:flex;align-items:center;justify-content:center;overflow:hidden;">
      <div style="font-family:'JetBrains Mono';font-size:62px;font-weight:700;color:{NAVY};">{end_lines[0]}</div>
    </div>
    <div style="position:absolute;left:0;right:0;top:1060px;">{end_lines[1]}</div>
  </div>
{chr(10).join(f'  <audio id="{i}" src="assets/sfx/{f}.mp3" data-start="{round(s, 2)}" data-duration="{d if d else dur(f"assets/sfx/{f}.mp3")}" data-volume="{v}" data-track-index="{2 + n}"' + (f' data-media-start="{ms}"' if ms else '') + '></audio>' for n, (i, f, s, d, v, ms) in enumerate(A))}
  <audio id="music" src="assets/music/music.mp3" data-start="0" data-duration="{TOTAL}" data-volume="0.45" data-track-index="1" data-fade-out="1.2"></audio>
</div>
<script>
  {chr(10).join("  " + l for l in PRE)}
  const tl = gsap.timeline({{ paused: true }});
  {chr(10).join("  " + l for l in T)}
  window.__timelines = window.__timelines || {{}};
  window.__timelines["main"] = tl;
</script>
</body>
</html>
"""
open("index.html", "w").write(html)
print("built", TOTAL, "s; line ends", ends, "url", e_url, "phone", e_ph)
