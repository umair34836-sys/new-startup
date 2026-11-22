#!/usr/bin/env python3
"""Silent 9:16 poetry/quote reels for an Instagram poetry account (2026-11-21, Ahmad Ali).
The trending song is added INSIDE the Instagram app (copyrighted songs are never put in the file).
Each reel = CC0 stock footage (vertical crop, darkened, slow zoom) + lines revealed word by word + handle.
A 4:5 post image is cut from the last frame (text sits inside y 300-1620).
python3 build_poetry_reels.py OUTDIR
"""
import html, json, os, subprocess, sys
MIX = os.environ.get("MIXDIR")  # Mixkit videoFree clips fetched per job: name "mx:<id>"
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
OUT = os.path.abspath(sys.argv[1]); os.makedirs(OUT, exist_ok=True)
HANDLE = os.environ.get("HANDLE", "Ahmad Ali ✍️")
REELS = json.load(open(os.environ["SPEC"])) if os.environ.get("SPEC") else [
  dict(id="r1-dilruba", song="Dilruba Dilnasheen (Rito Riba, Siddhant Kaushal)", bg="fire/candles-many-flames.mp4", tint="rgba(40,10,0,0.55)", acc="#ffb36b",
       tag="Dil ki baat", lines=["Tum saamne ho to", "dil ko qaraar aata hai,", "warna har lamha", "bas intezaar aata hai."]),
  dict(id="r2-inkaar", song="Inkaar (Azan Ahmad)", bg="city-night/night-city-lights-rain.mp4", tint="rgba(5,8,25,0.55)", acc="#8fb8ff",
       tag="Khamoshi", lines=["Usne inkaar kiya,", "maine shikayat nahi ki,", "bas us din ke baad", "kisi se dil ki baat nahi ki."]),
  dict(id="r3-vintage-november", song="Vintage November (Peaceful Reveries)", bg="nature-sky/night-sky-stars-clouds-timelapse.mp4", tint="rgba(5,5,20,0.45)", acc="#cfe3ff",
       tag="Faith reminder 🤲", lines=["Dua maangte raho.", "Jawab der se aaye,", "magar aata zaroor hai.", "Woh sunta hai, hamesha."]),
  dict(id="r4-november-rain", song="November Rain (Guns N' Roses)", bg="weather/rain-dripping-from-roof.mp4", tint="rgba(10,15,25,0.55)", acc="#a9c7d8",
       tag="November", lines=["Baarish to har saal", "aati hai,", "bas woh log nahi aate", "jo saath bheegte the."]),
  dict(id="r5-coming-up-roses", song="Coming Up Roses (Harry Styles) - trend: I feel like I haven't done much this year", bg="sunrise-sunset/sunrise-timelapse-orange-sky.mp4", tint="rgba(25,10,0,0.45)", acc="#ffd39a",
       tag="Is saal maine...", lines=["✓ chup rehna seekha", "✓ log pehchaane", "✓ khud ko chuna", "Yeh bhi kamyabi hai. 🖤"]),
]
DUR = 10.0
for R in REELS:
    P = os.path.join(OUT, R["id"]); A = os.path.join(P, "assets"); os.makedirs(os.path.join(A, "vendor"), exist_ok=True); os.makedirs(os.path.join(A, "fonts"), exist_ok=True)
    subprocess.run(["cp", f"{REPO}/library/vendor/gsap-3.14.2.min.js", f"{A}/vendor/"], check=True)
    for f in ("PlayfairDisplay-Italic.ttf", "Poppins-SemiBold.ttf", "Manrope-Variable.ttf"): subprocess.run(["cp", f"{REPO}/library/fonts/{f}", f"{A}/fonts/"], check=True)
    for f in ("hyperframes.json", "meta.json", "package.json"): subprocess.run(["cp", f"{REPO}/video/{f}", P], check=True)
    src = f"{MIX}/{R['bg'][3:]}.mp4" if R["bg"].startswith("mx:") else f"{REPO}/library/stock/{R['bg']}"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-stream_loop", "-1", "-i", src, "-t", str(DUR), "-an",
                    "-vf", f"crop=ih*9/16:ih:(iw-ih*9/16)*{R.get('cropx', 0.5)}:0,scale=1080:1920:flags=lanczos,fps=30,format=yuv420p", "-c:v", "libx264", "-crf", "18", "-preset", "fast", f"{A}/bg.mp4"], check=True)
    E = html.escape; body, js = [], []
    words = []
    for li, ln in enumerate(R["lines"]):
        ws = "".join(f'<span class="w" id="w{li}_{k}">{E(w)}</span> ' for k, w in enumerate(ln.split(" ")))
        body.append(f'<div class="ln" style="top:{620 + li * 150}px;{"color:" + R["acc"] + ";" if li == len(R["lines"]) - 1 else ""}">{ws}</div>')
        words += [f"#w{li}_{k}" for k in range(len(ln.split(" ")))]
    t = 1.0
    for i, w in enumerate(words):
        js.append(f'tl.fromTo("{w}", {{opacity:0, y:24, filter:"blur(8px)"}}, {{opacity:1, y:0, filter:"blur(0px)", duration:0.45, ease:"power2.out"}}, {t:.2f});')
        t += 0.28 if not R["lines"][0] else 0.28
    open(f"{P}/index.html", "w").write(f'''<!doctype html>
<html lang="en" data-resolution="portrait"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080, height=1920">
<script src="assets/vendor/gsap-3.14.2.min.js"></script><style>
@font-face {{ font-family:"PF"; src:url("assets/fonts/PlayfairDisplay-Italic.ttf"); }}
@font-face {{ font-family:"PS"; src:url("assets/fonts/Poppins-SemiBold.ttf"); }}
@font-face {{ font-family:"MR"; src:url("assets/fonts/Manrope-Variable.ttf"); font-weight:200 800; }}
* {{ margin:0; padding:0; box-sizing:border-box; }} html, body {{ width:1080px; height:1920px; overflow:hidden; background:#000; }}
.ln {{ position:absolute; left:90px; right:90px; text-align:center; font-family:PF; font-size:84px; line-height:1.15; color:#fff; text-shadow:0 4px 22px rgba(0,0,0,0.7); }}
.w {{ display:inline-block; }}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920" style="position:absolute;inset:0;overflow:hidden;background:#000;">
<div id="bgz" style="position:absolute;inset:0;transform-origin:50% 50%;"><video id="bgv" src="assets/bg.mp4" data-start="0" data-duration="{DUR}" muted playsinline style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;"></video></div>
<div style="position:absolute;inset:0;background:{R['tint']};"></div>
<div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 50%, rgba(0,0,0,0) 30%, rgba(0,0,0,0.6) 100%);"></div>
<div id="tg" style="position:absolute;left:60px;right:60px;top:{R.get('tagtop', 470)}px;text-align:center;font-family:PS;font-size:{R.get('tagsize', 44)}px;line-height:1.2;color:{R['acc']};">{E(R['tag'])}</div>
{chr(10).join(body)}
<div id="hd" style="position:absolute;left:0;right:0;top:1290px;text-align:center;font-family:MR;font-weight:700;font-size:38px;color:rgba(255,255,255,0.85);">{E(HANDLE)}</div>
</div><script>
const tl = gsap.timeline({{ paused: true }});
tl.fromTo("#bgz", {{scale:1.0}}, {{scale:1.12, duration:{DUR}, ease:"none"}}, 0);
tl.fromTo("#tg", {{opacity:0, y:-20}}, {{opacity:1, y:0, duration:0.6}}, 0.2);
{chr(10).join(js)}
tl.fromTo("#hd", {{opacity:0}}, {{opacity:1, duration:0.6}}, {t + 0.4:.2f});
tl.to({{}}, {{ duration: {DUR} }}, 0);
window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;
</script></body></html>''')
    json.dump(R, open(f"{P}/reel.json", "w"), ensure_ascii=False, indent=1)
print("built", len(REELS), "reels in", OUT)
