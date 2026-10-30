# Rounded card PNG with a coloured border and a soft shadow, for thumb_make.py stickers (real post crops, logos).
#   python3 thumb_card.py in.jpg out.png "#e2b85c" [radius] [x0,y0,x1,y1 crop]
import sys
from PIL import Image, ImageDraw, ImageFilter
src, out, border, rad = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 36
crop = [int(v) for v in sys.argv[5].split(",")] if len(sys.argv) > 5 else None
im = Image.open(src).convert("RGBA")
if crop: im = im.crop(crop)
w, h = im.size; b = max(6, w // 90); pad = 60
card = Image.new("RGBA", (w + 2 * b, h + 2 * b), border)
m = Image.new("L", im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w, h), rad, fill=255)
card.paste(im, (b, b), m)
cm = Image.new("L", card.size, 0); ImageDraw.Draw(cm).rounded_rectangle((0, 0, *card.size), rad + b, fill=255)
card.putalpha(cm)
can = Image.new("RGBA", (card.width + 2 * pad, card.height + 2 * pad), (0, 0, 0, 0))
sh = Image.new("L", can.size, 0); ImageDraw.Draw(sh).rounded_rectangle((pad, pad + 20, pad + card.width, pad + card.height + 20), rad, fill=170)
can.putalpha(sh.filter(ImageFilter.GaussianBlur(26))); can = Image.alpha_composite(Image.new("RGBA", can.size, (0, 0, 0, 0)), Image.merge("RGBA", (*[Image.new("L", can.size, 0)] * 3, can.getchannel("A"))))
can.alpha_composite(card, (pad, pad)); can.save(out)
print(out, can.size)
