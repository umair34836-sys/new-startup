#!/usr/bin/env python3
"""brand.json -> HyperFrames brand blocks + a demo index.html.

  python3 build_brand.py brand.json <project-dir> [--size 1080x1920|1920x1080]

Writes into <project-dir>:
  compositions/brand-sting.html      3 s logo intro (circle wipe, logo pop, name, tagline)
  compositions/brand-lower.html      4 s lower third (name + tagline, slides in and out)
  compositions/brand-offer.html      3 s price/offer badge
  compositions/brand-cta.html        2.5 s call-to-action sticker ("cta" + phone)
  compositions/brand-end.html        4 s contact end card (logo, phone, WhatsApp, address, socials, QR)
  compositions/brand-bug.html        watermark logo in a corner (host sets the duration)
  compositions/brand-bg.html         plain brand gradient, a stand-in for footage in the demo
  assets/brand/logo.png, assets/brand/qr.png (wa.me link, or website, made locally with the qrcode package)
  assets/fonts/* (copied from library/fonts), assets/vendor/gsap-3.14.2.min.js (copied if found)
  index.html                          demo that plays every block once (16.5 s)
Then: npx hyperframes check --json / snapshot / render inside <project-dir>.
To use one block in a real video, copy its composition file + assets/brand + fonts and add a host div
(the demo index.html shows the host attributes).
"""
import html
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.normpath(os.path.join(HERE, "..", ".."))
REPO = os.path.dirname(LIB)
E = html.escape


def scene(cid, W, H, css, body, js):
    return f"""<template>
  <style>
{css}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="{W}" data-height="{H}" data-layout-allow-overflow>
{body}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{js}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
"""


def main():
    a = sys.argv[1:]
    if len(a) < 2:
        sys.exit(__doc__)
    bpath, proj = a[0], a[1]
    W, H = (1080, 1920)
    if "--size" in a:
        W, H = map(int, a[a.index("--size") + 1].split("x"))
    portrait = H > W
    b = json.load(open(bpath, encoding="utf-8"))
    bdir = os.path.dirname(os.path.abspath(bpath))
    c = b["colors"]
    P, OP = c["primary"], c["on_primary"]
    S, OS_ = c.get("secondary", P), c.get("on_secondary", OP)
    A, D = c.get("accent", S), c.get("dark", "#0b0d10")
    f = b.get("fonts", {})
    fdisp, fbody, furdu = f.get("display", "Anton-Regular.ttf"), f.get("body", "PlusJakartaSans-Variable.ttf"), \
        f.get("urdu", "NotoNastaliqUrdu-Variable.ttf")
    for d in ("compositions", "assets/brand", "assets/fonts", "assets/vendor"):
        os.makedirs(os.path.join(proj, d), exist_ok=True)
    for ff in (fdisp, fbody, furdu):
        shutil.copy(os.path.join(LIB, "fonts", ff), os.path.join(proj, "assets/fonts", ff))
    gsap = os.path.join(REPO, "video/assets/vendor/gsap-3.14.2.min.js")
    if os.path.exists(gsap):
        shutil.copy(gsap, os.path.join(proj, "assets/vendor/gsap-3.14.2.min.js"))
    if b.get("logo"):
        shutil.copy(os.path.join(bdir, b["logo"]), os.path.join(proj, "assets/brand/logo.png"))
    qr_data = ("https://wa.me/" + b["whatsapp"]) if b.get("whatsapp") else (
        ("https://" + b["website"]) if b.get("website") else None)
    if qr_data:
        import qrcode
        q = qrcode.QRCode(border=2, box_size=20, error_correction=qrcode.constants.ERROR_CORRECT_M)
        q.add_data(qr_data)
        q.make(fit=True)
        q.make_image(fill_color="black", back_color="white").save(os.path.join(proj, "assets/brand/qr.png"))

    rtl_dir = "rtl"
    ur_font_lh = "2.0" if "Nastaliq" in furdu else "1.7"
    css0 = f"""    @font-face {{ font-family: "BrandDisplay"; src: url("assets/fonts/{fdisp}"); }}
    @font-face {{ font-family: "BrandBody"; src: url("assets/fonts/{fbody}"); font-weight: 200 800; }}
    @font-face {{ font-family: "BrandUrdu"; src: url("assets/fonts/{furdu}"); font-weight: 400 700; }}
    #root {{ position: absolute; inset: 0; pointer-events: none; --p: {P}; --op: {OP}; --s: {S}; --os: {OS_}; --a: {A}; --d: {D}; }}
    .ur {{ font-family: "BrandUrdu", serif; direction: {rtl_dir}; unicode-bidi: isolate; line-height: {ur_font_lh}; word-spacing: 0.25em; }}"""
    name, tag = E(b["name"]), E(b.get("tagline", ""))
    name_ur, tag_ur = E(b.get("name_ur", "")), E(b.get("tagline_ur", ""))
    logo = '<img id="%s" src="assets/brand/logo.png" alt="logo">' if b.get("logo") else '<div id="%s"></div>'
    files = {}

    # 1. sting
    L = int(min(W, H) * 0.34)
    LY = int(H * 0.36)
    files["brand-sting"] = scene("brand-sting", W, H, css0 + f"""
    #st-bg {{ position: absolute; inset: 0; background: var(--d); }}
    #st-wipe {{ position: absolute; left: 50%; top: {LY}px; width: {int(max(W, H) * 2.4)}px; height: {int(max(W, H) * 2.4)}px;
      margin: -{int(max(W, H) * 1.2)}px 0 0 -{int(max(W, H) * 1.2)}px; border-radius: 50%;
      background: radial-gradient(circle, var(--p) 0%, var(--p) 55%, var(--d) 100%); }}
    #st-logo {{ position: absolute; left: 50%; top: {LY}px; width: {L}px; height: {L}px; margin: -{L // 2}px 0 0 -{L // 2}px; object-fit: contain;
      filter: drop-shadow(0 18px 40px rgba(0, 0, 0, 0.45)); }}
    #st-txt {{ position: absolute; left: 6%; right: 6%; top: {LY + L // 2 + 24}px; display: flex; flex-direction: column; align-items: center; text-align: center; }}
    #st-name {{ color: var(--op); font-family: "BrandDisplay", sans-serif; font-size: {int(min(W, H) * 0.115)}px; line-height: 1.05; text-transform: uppercase; }}
    #st-name .ch {{ display: inline-block; }}
    #st-ur {{ color: var(--op); font-size: {int(min(W, H) * 0.07)}px; }}
    #st-tag {{ color: var(--s); font-family: "BrandBody", sans-serif; font-weight: 700; font-size: {int(min(W, H) * 0.045)}px; margin-top: 10px; }}""",
        f"""    <div id="st-bg"></div>
    <div id="st-wipe"></div>
    {logo % "st-logo"}
    <div id="st-txt">
      <div id="st-name">{" ".join('<span class="ch">%s</span>' % E(w) for w in b["name"].split())}</div>
      {'<div id="st-ur" class="ur" lang="ur" dir="rtl">%s</div>' % name_ur if name_ur else ''}
      {'<div id="st-tag">%s</div>' % tag if tag else ''}
    </div>""",
        """    gsap.set("#st-wipe", { scale: 0 });
    gsap.set("#st-logo", { scale: 0.2, rotation: -25, opacity: 0 });
    gsap.set(["#st-name .ch", "#st-ur", "#st-tag"], { opacity: 0 });
    tl.to("#st-wipe", { scale: 1, duration: 0.7, ease: "power3.out" }, 0.05);
    tl.to("#st-logo", { scale: 1, rotation: 0, opacity: 1, duration: 0.7, ease: "back.out(1.8)" }, 0.3);
    tl.fromTo("#st-name .ch", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out", stagger: 0.09 }, 0.8);
    tl.fromTo("#st-ur", { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.4, ease: "power2.out" }, 1.25);
    tl.fromTo("#st-tag", { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.4, ease: "power2.out" }, 1.45);
    tl.to("#st-logo", { scale: 1.04, duration: 1.0, ease: "sine.inOut" }, 1.6);
    tl.to("#root > *", { opacity: 0, duration: 0.3, ease: "power2.in" }, 2.68);""")

    # 2. lower third
    lw = int(W * (0.84 if portrait else 0.5))
    ly = int(H * (0.70 if portrait else 0.74))
    files["brand-lower"] = scene("brand-lower", W, H, css0 + f"""
    #lt {{ position: absolute; left: {int(W * 0.06)}px; top: {ly}px; width: {lw}px; }}
    #lt-bar {{ position: absolute; left: 0; top: 0; width: {lw}px; height: {int(min(W, H) * 0.13)}px; background: var(--p);
      border-radius: 14px; box-shadow: 0 12px 40px rgba(0, 0, 0, 0.35); transform-origin: left center; }}
    #lt-acc {{ position: absolute; left: 0; top: 0; width: 14px; height: {int(min(W, H) * 0.13)}px; background: var(--a); border-radius: 14px 0 0 14px; }}
    #lt-name {{ position: absolute; left: 44px; top: {int(min(W, H) * 0.018)}px; right: 24px; color: var(--op); font-family: "BrandDisplay", sans-serif;
      font-size: {int(min(W, H) * 0.062)}px; line-height: 1.1; text-transform: uppercase; white-space: nowrap; }}
    #lt-tag {{ position: absolute; left: 44px; top: {int(min(W, H) * 0.085)}px; color: var(--op); opacity: 0.9; font-family: "BrandBody", sans-serif;
      font-weight: 600; font-size: {int(min(W, H) * 0.032)}px; white-space: nowrap; }}
    #lt-ur {{ position: absolute; right: 30px; top: {int(min(W, H) * 0.005)}px; color: var(--op); font-size: {int(min(W, H) * 0.05)}px; }}""",
        f"""    <div id="lt">
      <div id="lt-bar"></div><div id="lt-acc"></div>
      <div id="lt-name">{name}</div>
      {'<div id="lt-tag">%s</div>' % tag if tag else ''}
      {'<div id="lt-ur" class="ur" lang="ur" dir="rtl">%s</div>' % name_ur if name_ur else ''}
    </div>""",
        """    gsap.set("#lt-bar", { scaleX: 0 });
    gsap.set(["#lt-name", "#lt-tag", "#lt-ur", "#lt-acc"], { opacity: 0 });
    tl.to("#lt-bar", { scaleX: 1, duration: 0.45, ease: "power3.out" }, 0.1);
    tl.to("#lt-acc", { opacity: 1, duration: 0.2 }, 0.2);
    tl.fromTo("#lt-name", { opacity: 0, x: -30 }, { opacity: 1, x: 0, duration: 0.35, ease: "power3.out" }, 0.35);
    tl.fromTo("#lt-tag", { opacity: 0, x: -20 }, { opacity: 1, x: 0, duration: 0.35, ease: "power3.out" }, 0.5);
    tl.fromTo("#lt-ur", { opacity: 0 }, { opacity: 1, duration: 0.35 }, 0.6);
    tl.to("#lt", { x: -60, opacity: 0, duration: 0.35, ease: "power2.in" }, 3.55);""")

    # 3. offer badge
    o = b.get("offer", {})
    R = int(min(W, H) * 0.56)
    files["brand-offer"] = scene("brand-offer", W, H, css0 + f"""
    #of {{ position: absolute; left: 50%; top: {int(H * 0.42)}px; width: {R}px; height: {R}px; margin: -{R // 2}px 0 0 -{R // 2}px; }}
    #of-star {{ position: absolute; inset: 0; background: var(--s);
      clip-path: polygon(50% 0%, 59% 13%, 75% 7%, 77% 23%, 93% 25%, 87% 41%, 100% 50%, 87% 59%, 93% 75%, 77% 77%, 75% 93%, 59% 87%, 50% 100%, 41% 87%, 25% 93%, 23% 77%, 7% 75%, 13% 59%, 0% 50%, 13% 41%, 7% 25%, 23% 23%, 25% 7%, 41% 13%); }}
    #of-in {{ position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; color: var(--os); text-align: center; }}
    #of-title {{ font-family: "BrandBody", sans-serif; font-weight: 800; font-size: {int(R * 0.085)}px; text-transform: uppercase; letter-spacing: 1px; }}
    #of-price {{ font-family: "BrandDisplay", sans-serif; font-size: {int(R * 0.27)}px; line-height: 1.0; }}
    #of-note {{ font-family: "BrandBody", sans-serif; font-weight: 600; font-size: {int(R * 0.06)}px; opacity: 0.85; }}""",
        f"""    <div id="of"><div id="of-star"></div><div id="of-in">
      <div id="of-title">{E(o.get("title", ""))}</div><div id="of-price">{E(o.get("price", ""))}</div><div id="of-note">{E(o.get("note", ""))}</div>
    </div></div>""",
        """    gsap.set("#of", { scale: 0, rotation: -40 });
    tl.to("#of", { scale: 1, rotation: -8, duration: 0.55, ease: "back.out(2)" }, 0.05);
    tl.to("#of-star", { rotation: 30, duration: 2.4, ease: "none" }, 0.1);
    tl.to("#of", { scale: 1.06, duration: 0.3, ease: "sine.inOut", yoyo: true, repeat: 3 }, 0.8);
    tl.to("#of", { scale: 0, rotation: 20, duration: 0.3, ease: "power2.in" }, 2.68);""")

    # 4. CTA sticker
    files["brand-cta"] = scene("brand-cta", W, H, css0 + f"""
    #ct {{ position: absolute; left: 50%; top: {int(H * (0.62 if portrait else 0.7))}px; transform-origin: center; }}
    #ct-box {{ position: relative; left: -50%; padding: {int(min(W, H) * 0.03)}px {int(min(W, H) * 0.06)}px; background: var(--p); color: var(--op);
      border-radius: 999px; border: 6px solid var(--a); box-shadow: 0 16px 44px rgba(0, 0, 0, 0.45); text-align: center; white-space: nowrap; }}
    #ct-main {{ font-family: "BrandBody", sans-serif; font-weight: 800; font-size: {int(min(W, H) * 0.07)}px; line-height: 1.1; }}
    #ct-phone {{ font-family: "BrandBody", sans-serif; font-weight: 700; font-size: {int(min(W, H) * 0.045)}px; color: var(--a); margin-top: 6px; }}""",
        f"""    <div id="ct"><div id="ct-box" data-layout-allow-overlap><div id="ct-main">{E(b.get("cta", "Call now"))}</div>
      {'<div id="ct-phone">%s</div>' % E(b["phone"]) if b.get("phone") else ''}</div></div>""",
        """    gsap.set("#ct", { scale: 0, rotation: -12 });
    tl.to("#ct", { scale: 1, rotation: -4, duration: 0.45, ease: "back.out(2.2)" }, 0.05);
    tl.to("#ct", { scale: 1.07, duration: 0.25, ease: "sine.inOut", yoyo: true, repeat: 5 }, 0.6);
    tl.to("#ct", { scale: 0, duration: 0.25, ease: "power2.in" }, 2.22);""")

    # 5. end card
    socials = "".join('<div class="ec-row ec-soc">%s %s</div>' % (E(k.capitalize()), E(v)) for k, v in b.get("socials", {}).items())
    info = []
    if b.get("phone"):
        info.append('<div class="ec-row"><span class="ec-k">Call</span> %s</div>' % E(b["phone"]))
    if b.get("whatsapp"):
        info.append('<div class="ec-row"><span class="ec-k">WhatsApp</span> +%s</div>' % E(b["whatsapp"]))
    if b.get("address"):
        info.append('<div class="ec-row">%s</div>' % E(b["address"]))
    if b.get("website"):
        info.append('<div class="ec-row">%s</div>' % E(b["website"]))
    if socials:
        info.append(socials)
    EL = int(min(W, H) * (0.3 if portrait else 0.2))
    Q = int(min(W, H) * (0.3 if portrait else 0.32))
    FS = min(W, H) * (0.042 if portrait else 0.036)
    QR = ('<div id="ec-qrw"><img id="ec-qr" src="assets/brand/qr.png" alt="QR code"><div id="ec-qrl">%s</div></div>'
          % ("Scan for WhatsApp" if b.get("whatsapp") else "Scan")) if qr_data else ""
    qpos = "" if portrait else "position: absolute; right: %dpx; top: 50%%; margin-top: -%dpx;" % (int(W * 0.08), Q // 2 + 30)
    files["brand-end"] = scene("brand-end", W, H, css0 + f"""
    #ec-bg {{ position: absolute; inset: 0; background: radial-gradient(circle at 50% 30%, var(--p), var(--d) 75%); }}
    #ec-col {{ position: absolute; top: 0; bottom: 0; left: {int(W * 0.06)}px; right: {int(W * (0.06 if portrait else 0.36))}px;
      display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; gap: {int(min(W, H) * 0.012)}px; }}
    #ec-logo {{ width: {EL}px; height: {EL}px; object-fit: contain; }}
    #ec-name {{ color: var(--op); font-family: "BrandDisplay", sans-serif; font-size: {int(min(W, H) * 0.09)}px; line-height: 1.05; text-transform: uppercase; }}
    #ec-ur {{ color: var(--op); font-size: {int(min(W, H) * 0.055)}px; }}
    #ec-info {{ color: #ffffff; font-family: "BrandBody", sans-serif; font-weight: 600; font-size: {int(FS)}px; line-height: 1.55; margin-top: 10px; }}
    .ec-k {{ color: var(--a); font-weight: 800; }}
    .ec-soc {{ font-size: {int(FS * 0.82)}px; opacity: 0.9; }}
    #ec-qrw {{ display: flex; flex-direction: column; align-items: center; margin-top: {int(min(W, H) * 0.03)}px; {qpos} }}
    #ec-qr {{ width: {Q}px; height: {Q}px; border-radius: 18px; border: 10px solid #ffffff; background: #ffffff; }}
    #ec-qrl {{ margin-top: 14px; color: #ffffff; font-family: "BrandBody", sans-serif; font-weight: 700; font-size: {int(min(W, H) * 0.03)}px; }}""",
        f"""    <div id="ec-bg"></div>
    <div id="ec-col">
      {logo % "ec-logo"}
      <div id="ec-name">{name}</div>
      {'<div id="ec-ur" class="ur" lang="ur" dir="rtl">%s</div>' % name_ur if name_ur else ''}
      <div id="ec-info">{"".join(info)}</div>
      {QR if portrait else ''}
    </div>
    {'' if portrait else QR}""",
        """    gsap.set(["#ec-logo", "#ec-name", "#ec-ur", ".ec-row", "#ec-qr", "#ec-qrl"], { opacity: 0 });
    tl.fromTo("#ec-logo", { opacity: 0, scale: 0.6 }, { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(1.7)" }, 0.1);
    tl.fromTo(["#ec-name", "#ec-ur"], { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.4, ease: "power3.out", stagger: 0.12 }, 0.35);
    tl.fromTo(".ec-row", { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: 0.35, ease: "power3.out", stagger: 0.1 }, 0.6);
    tl.fromTo(["#ec-qr", "#ec-qrl"], { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(1.6)" }, 1.1);""")

    # 6. watermark bug
    BG = int(min(W, H) * 0.12)
    files["brand-bug"] = scene("brand-bug", W, H, css0 + f"""
    #bug {{ position: absolute; right: {int(W * 0.06)}px; top: {int(H * (0.06 if portrait else 0.07))}px; width: {BG}px; height: {BG}px; object-fit: contain;
      filter: drop-shadow(0 4px 12px rgba(0, 0, 0, 0.5)); }}""",
        f"    {logo % 'bug'}",
        """    gsap.set("#bug", { opacity: 0 });
    tl.to("#bug", { opacity: 0.85, duration: 0.4, ease: "power2.out" }, 0.1);""")

    # stand-in background for the demo
    files["brand-bg"] = scene("brand-bg", W, H, f"""    #root {{ position: absolute; inset: 0; background: linear-gradient(160deg, #3d4a57, #8c7a66 60%, #c9b79c); }}
    #bg-glow {{ position: absolute; width: {W}px; height: {W}px; left: 0; top: {int(H * 0.2)}px; border-radius: 50%;
      background: radial-gradient(circle, rgba(255, 236, 200, 0.55), rgba(255, 236, 200, 0)); }}""",
        '    <div id="bg-glow"></div>',
        '    tl.fromTo("#bg-glow", { y: 0 }, { y: %d, duration: 16.5, ease: "none" }, 0);' % int(H * 0.15))

    for k, v in files.items():
        open(os.path.join(proj, "compositions", k + ".html"), "w", encoding="utf-8").write(v)

    hosts = [("brand-sting", 0, 3, 1), ("brand-bg", 3, 9.5, 0), ("brand-lower", 3, 4, 1), ("brand-offer", 7, 3, 1),
             ("brand-cta", 10, 2.5, 1), ("brand-bug", 3, 9.5, 2), ("brand-end", 12.5, 4, 1)]
    hd = "\n".join(
        f'      <div id="{k}" data-composition-id="{k}" data-composition-src="compositions/{k}.html" data-start="{s}" data-duration="{d}" '
        f'data-track-index="{i}" data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index: {i}"></div>'
        for i, (k, s, d, _z) in enumerate(hosts))
    open(os.path.join(proj, "index.html"), "w", encoding="utf-8").write(f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="assets/vendor/gsap-3.14.2.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: {W}px; height: {H}px; overflow: hidden; background: {D}; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="16.5" data-width="{W}" data-height="{H}">
{hd}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
""")
    for fn in ("hyperframes.json", "package.json"):
        src = os.path.join(REPO, "video", fn)
        if os.path.exists(src) and not os.path.exists(os.path.join(proj, fn)):
            shutil.copy(src, os.path.join(proj, fn))
    print("wrote", len(files), "blocks + index.html into", proj, "| QR:", qr_data)


if __name__ == "__main__":
    main()
