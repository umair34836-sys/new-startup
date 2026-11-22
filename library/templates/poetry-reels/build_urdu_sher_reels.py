#!/usr/bin/env python3
"""Urdu-script sher reels in the style the owner pointed at (2026-11-22): very dark, faceless moving footage,
one 2-line sher in Nastaliq in the upper third with a thin red bar, poet name, small handle. Silent (song in-app).
Couplets are classical (Ghalib d. 1869, Mir d. 1810), copied exactly from rekhta.org (?lang=ur, read 2026-11-22).
python3 build_urdu_sher_reels.py OUTDIR   (env MIXDIR = folder with Mixkit videoFree clips <id>.mp4)
"""
import html, json, os, subprocess, sys
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
OUT = os.path.abspath(sys.argv[1]); os.makedirs(OUT, exist_ok=True); MIX = os.environ.get("MIXDIR", "")
HANDLE = os.environ.get("HANDLE", "Ahmad Ali ✍️")
REELS = [
  dict(id="u1-dil-e-nadaan", src="stock:city-night/night-city-lights-rain.mp4", cropx=0.5,
       l1="دل ناداں تجھے ہوا کیا ہے", l2="آخر اس درد کی دوا کیا ہے", poet="غالبؔ",
       ref="https://www.rekhta.org/couplets/dil-e-naadaan-tujhe-huaa-kyaa-hai-mirza-ghalib-couplets?lang=ur"),
  dict(id="u2-shaam-se", src="mx:4808", cropx=0.12,
       l1="شام سے کچھ بجھا سا رہتا ہوں", l2="دل ہوا ہے چراغ مفلس کا", poet="میرؔ",
       ref="https://www.rekhta.org/poets/meer-taqi-meer/couplets?lang=ur"),
  dict(id="u3-wafa-ki-umeed", src="mx:231", cropx=0.62,
       l1="ہم کو ان سے وفا کی ہے امید", l2="جو نہیں جانتے وفا کیا ہے", poet="غالبؔ",
       ref="https://www.rekhta.org/poets/mirza-ghalib/couplets?lang=ur"),
]
DUR = 12.0
for R in REELS:
    P = os.path.join(OUT, R["id"]); A = os.path.join(P, "assets"); os.makedirs(f"{A}/vendor", exist_ok=True); os.makedirs(f"{A}/fonts", exist_ok=True)
    subprocess.run(["cp", f"{REPO}/library/vendor/gsap-3.14.2.min.js", f"{A}/vendor/"], check=True)
    for f in ("NotoNastaliqUrdu-Variable.ttf", "Manrope-Variable.ttf"): subprocess.run(["cp", f"{REPO}/library/fonts/{f}", f"{A}/fonts/"], check=True)
    for f in ("hyperframes.json", "meta.json", "package.json"): subprocess.run(["cp", f"{REPO}/video/{f}", P], check=True)
    src = f"{MIX}/{R['src'][3:]}.mp4" if R["src"].startswith("mx:") else f"{REPO}/library/stock/{R['src'][6:]}"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-stream_loop", "-1", "-i", src, "-t", str(DUR), "-an", "-vf",
                    f"crop=ih*9/16:ih:(iw-ih*9/16)*{R['cropx']}:0,scale=1080:1920:flags=lanczos,setpts=1.25*PTS,fps=30,"
                    "eq=brightness=-0.08:saturation=0.7:contrast=1.08,format=yuv420p",
                    "-c:v", "libx264", "-crf", "18", "-preset", "fast", f"{A}/bg.mp4"], check=True)
    E = html.escape
    open(f"{P}/index.html", "w").write(f'''<!doctype html>
<html lang="ur" data-resolution="portrait"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080, height=1920">
<script src="assets/vendor/gsap-3.14.2.min.js"></script><style>
@font-face {{ font-family:"NN"; src:url("assets/fonts/NotoNastaliqUrdu-Variable.ttf"); font-weight:400 700; }}
@font-face {{ font-family:"MR"; src:url("assets/fonts/Manrope-Variable.ttf"); font-weight:200 800; }}
* {{ margin:0; padding:0; box-sizing:border-box; }} html, body {{ width:1080px; height:1920px; overflow:hidden; background:#000; }}
.ur {{ direction:rtl; text-align:center; font-family:NN; font-size:66px; line-height:1.9; color:#f3efe8; text-shadow:0 3px 18px rgba(0,0,0,0.85); white-space:nowrap; }}
</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920" style="position:absolute;inset:0;overflow:hidden;background:#000;">
<div id="bgz" style="position:absolute;inset:0;transform-origin:50% 60%;"><video id="bgv" src="assets/bg.mp4" data-start="0" data-duration="{DUR}" muted playsinline style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;"></video></div>
<div style="position:absolute;inset:0;background:linear-gradient(180deg, rgba(0,0,0,0.72) 0%, rgba(0,0,0,0.35) 45%, rgba(0,0,0,0.55) 100%);"></div>
<div id="blk" style="position:absolute;left:150px;width:780px;top:470px;">
  <div id="bar" style="position:absolute;right:-26px;top:22px;width:6px;height:250px;background:#d2163b;border-radius:3px;transform-origin:50% 0;"></div>
  <div id="l1" class="ur">{E(R["l1"])}</div>
  <div id="l2" class="ur">{E(R["l2"])}</div>
  <div id="po" class="ur" style="font-size:40px;color:#d9c9a8;margin-top:6px;">{E(R["poet"])}</div>
</div>
<div id="hd" style="position:absolute;left:0;right:0;top:1700px;text-align:center;font-family:MR;font-weight:700;font-size:34px;color:rgba(255,255,255,0.7);">{E(HANDLE)}</div>
</div><script>
const tl = gsap.timeline({{ paused: true }});
tl.fromTo("#bgz", {{scale:1.0}}, {{scale:1.08, duration:{DUR}, ease:"none"}}, 0);
tl.fromTo("#bar", {{scaleY:0}}, {{scaleY:1, duration:0.6, ease:"power2.out"}}, 0.3);
tl.fromTo("#l1", {{opacity:0, y:16, filter:"blur(6px)"}}, {{opacity:1, y:0, filter:"blur(0px)", duration:0.9, ease:"power2.out"}}, 0.6);
tl.fromTo("#l2", {{opacity:0, y:16, filter:"blur(6px)"}}, {{opacity:1, y:0, filter:"blur(0px)", duration:0.9, ease:"power2.out"}}, 2.4);
tl.fromTo("#po", {{opacity:0}}, {{opacity:1, duration:0.8}}, 4.2);
tl.fromTo("#hd", {{opacity:0}}, {{opacity:1, duration:0.8}}, 5.0);
tl.to({{}}, {{ duration: {DUR} }}, 0);
window.__timelines = window.__timelines || {{}}; window.__timelines["main"] = tl;
</script></body></html>''')
    json.dump(R, open(f"{P}/reel.json", "w"), ensure_ascii=False, indent=1)
print("built", len(REELS), "in", OUT)
