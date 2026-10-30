# Check a thumbnail before delivery: size/ratio/file size, how it reads at the sizes YouTube really serves, and the
# contrast of every text box against what is behind it.
#
#   python3 library/tools/thumb_check.py out.png            # uses out.boxes.json + out_bgonly.png from thumb_make.py --variants
#   python3 library/tools/thumb_check.py any.jpg            # without boxes: only size checks + preview sheet
#
# Writes out_check.png: the thumbnail at 1280 (top) and at the served sizes 320x180 / 168x94 (phone list) / 120x90,
# a 4:3 letterbox (480x360) and a grey (luminance) version to judge value contrast. Prints a JSON report.
# Rules (sources in library/research/editing/skills2/16-thumbnails.md): >= 1280x720 or A/B tests fall back to 480p
# (#4181); JPG < 2 MB for phone upload (#4163); exactly 16:9 for long videos (#4175), 9:16 for Shorts covers (#4165);
# WCAG contrast ratio >= 4.5 for text (>= 3 for large text) - the outline counts when it is >= 4 px.
import json, os, re, sys
from PIL import Image, ImageDraw, ImageOps

path = sys.argv[1]
stem = os.path.splitext(path)[0]
im = Image.open(path).convert("RGB")
W, H = im.size
rep = {"file": path, "size": [W, H], "bytes": os.path.getsize(path), "issues": []}
ratio = W / H
if abs(ratio - 16 / 9) < 0.01:
    rep["format"] = "16:9"
    if W < 1280:
        rep["issues"].append("under 1280x720: A/B tests would downscale every variant to 480p")
elif abs(ratio - 9 / 16) < 0.01:
    rep["format"] = "9:16"
    if W < 1080:
        rep["issues"].append("Shorts cover under 1080x1920")
elif abs(ratio - 1) < 0.01 or abs(ratio - 0.8) < 0.01:
    rep["format"] = "1:1 post" if abs(ratio - 1) < 0.01 else "4:5 post"  # Instagram/Facebook feed posts, podcast covers
else:
    rep["format"] = f"{W}x{H}"
    rep["issues"].append("not 16:9, 9:16, 1:1 or 4:5: YouTube adds black bars (it never crops)")
jpg = stem + ".jpg"
if os.path.exists(jpg):
    rep["jpg_mb"] = round(os.path.getsize(jpg) / 1e6, 2)
    if rep["jpg_mb"] >= 2:
        rep["issues"].append("JPG >= 2 MB: phone upload will refuse it")


def lum(rgb):
    def ch(c):
        c = c / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb[:3]
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def contrast(a, b):
    la, lb = sorted([lum(a), lum(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


boxes_f, bg_f = stem + ".boxes.json", stem + "_bgonly.png"
if os.path.exists(boxes_f) and os.path.exists(bg_f):
    bg = Image.open(bg_f).convert("RGB")
    rep["text"] = []
    for b in json.load(open(boxes_f))["boxes"]:
        x0, y0 = max(0, int(b["x"])), max(0, int(b["y"]))
        x1, y1 = min(W, int(b["x"] + b["w"])), min(H, int(b["y"] + b["h"]))
        if x1 <= x0 or y1 <= y0:
            rep["issues"].append(f"text {b['id']} is outside the canvas")
            continue
        crop = bg.crop((x0, y0, x1, y1)).resize((32, 32))
        px = sorted(crop.get_flattened_data() if hasattr(crop, 'get_flattened_data') else crop.getdata(), key=lum)
        med = px[len(px) // 2]
        boxc = [int(v) for v in re.findall(r"[\d.]+", b.get("box") or "")]
        if len(boxc) == 3 or (len(boxc) == 4 and float(boxc[3]) > 0):  # text sits on its own box: compare with the box
            med = tuple(boxc[:3])
        fill = tuple(int(v) for v in re.findall(r"\d+", b["color"])[:3])
        stroke_px = float(re.findall(r"[\d.]+", b.get("stroke") or "0")[0] or 0)
        c_fill = round(contrast(fill, med), 2)
        # an outline of >= 4 px separates the letters from the background on its own (the fill then only needs to
        # contrast with the outline, which is black or white in our templates)
        ok = c_fill >= (3 if b["size"] >= 24 else 4.5) or stroke_px >= 4
        cut = x1 - x0 < b["w"] - 2 or y1 - y0 < b["h"] - 2
        rep["text"].append({"id": b["id"], "text": b["text"][:40], "font_px": b["size"], "fill_vs_bg": c_fill,
                            "outline_px": stroke_px, "readable": ok, "cut_off": cut,
                            "height_share": round(b["h"] / H, 3)})
        if not ok:
            rep["issues"].append(f"text '{b['text'][:20]}' contrast {c_fill} with no outline: add stroke or a box")
        if cut:
            rep["issues"].append(f"text '{b['text'][:20]}' runs off the canvas")
        if b["size"] * (320 / W) < 14:
            rep["issues"].append(f"text '{b['text'][:20]}' is {b['size'] * 320 / W:.0f} px tall at 320 px wide: too small on phones")

# preview sheet
if rep["format"] == "9:16":
    sizes = [(360, 640), (180, 320), (108, 192)]
else:
    sizes = [(320, 180), (168, 94), (120, 90)]
sheet_w = max(W // 2, 640) + 40
top = im.resize((sheet_w - 40, int((sheet_w - 40) * H / W)))
row_h = max(s[1] for s in sizes) + 30
lb = ImageOps.pad(im.resize((480, int(480 * H / W))), (480, 360), color=(0, 0, 0)) if rep["format"] == "16:9" else None
grey = ImageOps.grayscale(im).resize((sizes[0][0], sizes[0][1])).convert("RGB")
sheet_h = top.height + row_h + (360 + 30 if lb else 0) + 40
sheet = Image.new("RGB", (max(sheet_w, 1100), sheet_h), (40, 40, 40))
d = ImageDraw.Draw(sheet)
sheet.paste(top, (20, 20))
x, y = 20, top.height + 40
for s in sizes:
    sheet.paste(im.resize(s, Image.LANCZOS), (x, y))
    d.text((x, y + s[1] + 4), f"{s[0]}x{s[1]}", fill=(220, 220, 220))
    x += s[0] + 20
sheet.paste(grey, (x, y))
d.text((x, y + grey.height + 4), "luminance only", fill=(220, 220, 220))
if lb:
    sheet.paste(lb, (20, y + row_h))
    d.text((20, y + row_h + 362), "4:3 letterbox (480x360)", fill=(220, 220, 220))
sheet.save(stem + "_check.png")
rep["sheet"] = stem + "_check.png"
rep["ok"] = not rep["issues"]
print(json.dumps(rep, indent=1, ensure_ascii=False))
