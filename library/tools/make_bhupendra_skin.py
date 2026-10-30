# Paint a 64x64 classic Minecraft skin that looks like Bhupendra's own avatar on https://bhupendra.pages.dev/avatar.jpg
# (Heaven Developer client, owner chose "Bhupendra ka look-alike" on 2026-10-29): white body, arms and legs, black
# sunglasses across the face, a small grey mouth line, a grey/white/black checker cap (hat layer) and the green pixel
# emblem on the chest. Colours sampled by eye from that avatar; nothing else invented.
#   python3 make_bhupendra_skin.py out.png
import random, sys
from PIL import Image

rnd = random.Random(29)
img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
px = img.load()

WHITE, WHITE_D = (236, 236, 240), (214, 214, 222)
GLASS, GLASS_L = (18, 18, 20), (46, 46, 50)
MOUTH = (150, 150, 158)
CAP = [(240, 240, 244), (176, 176, 184), (64, 64, 70), (210, 210, 216)]
GREEN, GREEN_L, GREEN_D = (88, 178, 52), (124, 206, 72), (40, 96, 28)
DARK = (20, 30, 18)


def put(x, y, c, jitter=5):
    j = rnd.randint(-jitter, jitter)
    px[x, y] = tuple(max(0, min(255, v + j)) for v in c[:3]) + (255,)


def fill(x, y, w, h, c, c2=None, jitter=5):
    for i in range(w):
        for k in range(h):
            put(x + i, y + k, c2 if (c2 and rnd.random() < 0.15) else c, jitter)


def box_faces(u, v, w, h, d):
    return {"top": (u + d, v, w, d), "bottom": (u + d + w, v, w, d), "right": (u, v + d, d, h),
            "front": (u + d, v + d, w, h), "left": (u + d + w, v + d, d, h), "back": (u + 2 * d + w, v + d, w, h)}


# head: white, sunglasses band on the front and round the sides, mouth line
H = box_faces(0, 0, 8, 8, 8)
for f in H:
    fill(*H[f], WHITE, WHITE_D)
fx, fy = H["front"][:2]
fill(fx, fy + 3, 8, 2, GLASS, GLASS_L, 3)
put(fx + 3, fy + 4, WHITE, 2); put(fx + 4, fy + 4, WHITE, 2)      # bridge gap between the lenses
for x in range(2, 6):
    put(fx + x, fy + 6, MOUTH, 3)
for f in ("right", "left"):                                         # arms of the glasses
    gx, gy = H[f][:2]
    fill(gx, gy + 3, 8, 1, GLASS, GLASS_L, 3)
# hat layer: checker cap on the top half of the head
HO = box_faces(32, 0, 8, 8, 8)
for f in ("top",):
    x0, y0, w, h = HO[f]
    for i in range(w):
        for k in range(h):
            put(x0 + i, y0 + k, CAP[(i // 2 + k // 2) % 4], 6)
for f in ("front", "right", "left", "back"):
    x0, y0, w, h = HO[f]
    for i in range(w):
        for k in range(3):                                          # cap covers the top 3 rows of each side
            put(x0 + i, y0 + k, CAP[(i // 2 + k + 1) % 4], 6)

# body: white shirt with the green pixel emblem on the front
B = box_faces(16, 16, 8, 12, 4)
for f in B:
    fill(*B[f], WHITE, WHITE_D)
bx, by = B["front"][:2]
EMBLEM = ["...GG...",
          "..GDDG..",
          ".GGLLGG.",
          "DGLGGLGD",
          ".GGDDGG.",
          "GLGLLGLG",
          ".DGGGGD.",
          "GGDLLDGG"]
cols = {"G": GREEN, "L": GREEN_L, "D": DARK}
for y, row in enumerate(EMBLEM):
    for x, ch in enumerate(row):
        if ch in cols:
            put(bx + x, by + 3 + y, cols[ch], 4)

# arms and legs: white (base layers of the classic layout)
for u, v in ((40, 16), (32, 48), (0, 16), (16, 48)):
    F = box_faces(u, v, 4, 12, 4)
    for f in F:
        fill(*F[f], WHITE, WHITE_D)

img.save(sys.argv[1] if len(sys.argv) > 1 else "bhupendra-skin.png")
print("wrote", sys.argv[1] if len(sys.argv) > 1 else "bhupendra-skin.png")
