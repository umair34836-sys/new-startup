# Preview/copyright watermark for client videos sent before payment: a diagonal tiled text layer over the whole frame
# (hard to crop or blur out), a solid corner tag, and copyright/artist metadata in the file. After payment, send the
# clean render instead.
#
#   python3 watermark.py IN.mp4 OUT.mp4 [--text "Made by MrCopper804"] [--tag "PREVIEW  ·  © 2026 MrCopper804"]
#          [--opacity 0.16] [--crf 18]
import argparse, math, os, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "..", "fonts", "Anton-Regular.ttf")

ap = argparse.ArgumentParser()
ap.add_argument("inp"); ap.add_argument("out")
ap.add_argument("--text", default="Made by MrCopper804")
ap.add_argument("--tag", default="PREVIEW  ·  © 2026 MrCopper804")
ap.add_argument("--opacity", type=float, default=0.16, help="tiled text alpha, 0-1")
ap.add_argument("--crf", type=int, default=18)
a = ap.parse_args()

w, h = map(int, subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                                "-of", "csv=p=0", a.inp], capture_output=True, text=True, check=True).stdout.strip().split(","))

# diagonal tiles: draw on a big square canvas, rotate, crop to the frame
side = int(math.hypot(w, h)) + 200
tile = Image.new("RGBA", (side, side), (0, 0, 0, 0))
d = ImageDraw.Draw(tile)
f = ImageFont.truetype(FONT, max(28, min(w, h) // 16))  # short side: same look in 9:16 and 16:9
tw, th = d.textbbox((0, 0), a.text, font=f)[2:]
alpha = int(255 * a.opacity)
for row, y in enumerate(range(0, side, int(th * 3.2))):
    for x in range(-tw + (row % 2) * tw // 2, side, int(tw * 1.35)):
        d.text((x, y), a.text, font=f, fill=(255, 255, 255, alpha), stroke_width=2, stroke_fill=(0, 0, 0, alpha // 2))
tile = tile.rotate(30, resample=Image.BICUBIC)
L = (side - w) // 2; T = (side - h) // 2
layer = tile.crop((L, T, L + w, T + h))

# corner tag: dark pill, full-opacity text, top-left (away from end-card URLs at the bottom)
d = ImageDraw.Draw(layer)
ft = ImageFont.truetype(FONT, max(18, min(w, h) // 30))
bw, bh = d.textbbox((0, 0), a.tag, font=ft)[2:]
pad = bh // 2; x0 = y0 = min(w, h) // 30
d.rounded_rectangle((x0, y0, x0 + bw + 2 * pad, y0 + bh + 2 * pad), radius=bh, fill=(0, 0, 0, 150))
d.text((x0 + pad, y0 + pad * 0.7), a.tag, font=ft, fill=(255, 255, 255, 235))

png = os.path.join(tempfile.mkdtemp(prefix="wm_"), "wm.png")
layer.save(png)
owner = a.text.split()[-1]
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.inp, "-i", png, "-filter_complex", "[0:v][1:v]overlay=0:0:format=auto[v]",
                "-map", "[v]", "-map", "0:a?", "-c:v", "libx264", "-crf", str(a.crf), "-preset", "medium", "-pix_fmt", "yuv420p",
                "-c:a", "copy", "-movflags", "+faststart",
                "-metadata", f"copyright=© 2026 {owner}. All rights reserved. Preview only, not licensed for use.",
                "-metadata", f"artist={owner}", "-metadata", f"comment={a.text}. Unpaid preview: no licence granted.",
                a.out], check=True)
print("wrote", a.out)
