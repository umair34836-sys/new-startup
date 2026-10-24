# Draws demo-logo.png for the FAKE example brand (a cup-like circle mark + initials). Test asset only.
import os, sys
from PIL import Image, ImageDraw, ImageFont
here = os.path.dirname(os.path.abspath(__file__))
font = os.path.join(here, "..", "..", "fonts", "Anton-Regular.ttf")
im = Image.new("RGBA", (800, 800), (0, 0, 0, 0))
d = ImageDraw.Draw(im)
d.ellipse((40, 40, 760, 760), fill=(138, 59, 18, 255))
d.ellipse((110, 110, 690, 690), outline=(242, 193, 78, 255), width=26)
f = ImageFont.truetype(font, 300)
d.text((400, 420), "DC", font=f, fill=(255, 246, 230, 255), anchor="mm")
im.save(sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "demo-logo.png"))
