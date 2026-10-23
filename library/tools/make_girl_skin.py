# Paint a 64x64 classic Minecraft skin: a girl with long black hair, maroon kurta with gold trim,
# a gold dupatta across the chest, bangles, cream salwar and gold juttis.
#   python3 make_girl_skin.py out.png
import random, sys
from PIL import Image

rnd = random.Random(26)
img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
px = img.load()

SKIN, SKIN_D = (224, 169, 130), (201, 145, 108)
HAIR, HAIR_L = (26, 17, 16), (58, 37, 32)
KURTA, KURTA_D = (122, 20, 48), (98, 14, 38)
GOLD, GOLD_D = (214, 163, 58), (176, 126, 36)
SALWAR, SALWAR_D = (239, 227, 207), (214, 200, 178)
EYE_W, EYE = (245, 245, 245), (74, 44, 28)
LIPS, BLUSH = (192, 82, 90), (232, 150, 140)

def put(x, y, c, jitter=6):
    j = rnd.randint(-jitter, jitter)
    px[x, y] = tuple(max(0, min(255, v + j)) for v in c[:3]) + (255,)

def fill(x, y, w, h, c, c2=None, jitter=6):
    for i in range(w):
        for k in range(h):
            put(x + i, y + k, c2 if (c2 and rnd.random() < 0.18) else c, jitter)

def box_faces(u, v, w, h, d):
    return {"top": (u + d, v, w, d), "bottom": (u + d + w, v, w, d), "right": (u, v + d, d, h),
            "front": (u + d, v + d, w, h), "left": (u + d + w, v + d, d, h), "back": (u + 2 * d + w, v + d, w, h)}

# Head: hair everywhere, face on the front.
H = box_faces(0, 0, 8, 8, 8)
for f in ("top", "right", "left", "back"):
    fill(*H[f], HAIR, HAIR_L)
fill(*H["bottom"], SKIN, SKIN_D)
fx, fy = H["front"][:2]
fill(fx, fy, 8, 8, SKIN, SKIN_D, 4)
fill(fx, fy, 8, 2, HAIR, HAIR_L)                       # fringe
for x in (0, 7):                                      # hair framing the face
    for y in range(2, 8):
        put(fx + x, fy + y, HAIR)
put(fx + 1, fy + 2, HAIR); put(fx + 6, fy + 2, HAIR)
for x, c in ((1, EYE_W), (2, EYE), (5, EYE), (6, EYE_W)):
    put(fx + x, fy + 4, c, 0)
put(fx + 1, fy + 3, HAIR_L, 0); put(fx + 2, fy + 3, HAIR_L, 0); put(fx + 5, fy + 3, HAIR_L, 0); put(fx + 6, fy + 3, HAIR_L, 0)
put(fx + 1, fy + 5, BLUSH, 0); put(fx + 6, fy + 5, BLUSH, 0)
put(fx + 3, fy + 6, LIPS, 0); put(fx + 4, fy + 6, LIPS, 0)
put(fx + 3, fy + 2, (196, 40, 50), 0)                 # bindi
# Hair volume layer (hat): sides and back fully, fringe and side strands at the front.
HO = box_faces(32, 0, 8, 8, 8)
for f in ("top", "right", "left", "back"):
    fill(*HO[f], HAIR, HAIR_L)
ox, oy = HO["front"][:2]
fill(ox, oy, 8, 1, HAIR, HAIR_L)
for y in range(1, 8):
    put(ox, oy + y, HAIR); put(ox + 7, oy + y, HAIR)

# Body: maroon kurta with a gold neckline and hem; long hair down the back.
B = box_faces(16, 16, 8, 12, 4)
for f in B:
    fill(*B[f], KURTA, KURTA_D)
bx, by = B["front"][:2]
for x, y in ((2, 0), (5, 0), (3, 1), (4, 1), (3, 2), (4, 2)):
    put(bx + x, by + y, SKIN)
for x in (1, 2, 5, 6):
    put(bx + x, by + 1 if x in (2, 5) else by, GOLD)
fill(bx, by + 11, 8, 1, GOLD, GOLD_D)
for x, y in ((2, 5), (5, 5), (3, 8), (4, 8), (1, 9), (6, 9)):
    put(bx + x, by + y, GOLD)                          # embroidery dots
kx, ky = B["back"][:2]
fill(kx, ky, 8, 8, HAIR, HAIR_L)
for x in range(1, 7):
    put(kx + x, ky + 8, HAIR)
fill(B["top"][0], B["top"][1], 8, 2, KURTA, KURTA_D)
fill(B["top"][0], B["top"][1] + 2, 8, 2, HAIR, HAIR_L)
for f in ("right", "left"):
    fill(B[f][0], B[f][1] + 11, 4, 1, GOLD, GOLD_D)
# Dupatta (jacket layer): a gold band from the left shoulder to the right hip, front and back.
J = box_faces(16, 32, 8, 12, 4)
jx, jy = J["front"][:2]
for y in range(12):
    for dx in (0, 1, 2):
        x = 7 - int(y * 0.62) - dx
        if 0 <= x < 8:
            put(jx + x, jy + y, GOLD if dx < 2 else GOLD_D)
jx, jy = J["back"][:2]
for y in range(12):
    for dx in (0, 1, 2):
        x = int(y * 0.62) + dx
        if 0 <= x < 8:
            put(jx + x, jy + y, GOLD if dx < 2 else GOLD_D)

def arm(u, v):
    A = box_faces(u, v, 4, 12, 4)
    for f in A:
        x, y, w, h = A[f]
        if f in ("top",):
            fill(x, y, w, h, KURTA, KURTA_D)
        elif f == "bottom":
            fill(x, y, w, h, SKIN, SKIN_D)
        else:
            fill(x, y, w, 6, KURTA, KURTA_D)
            fill(x, y + 6, w, 1, GOLD, GOLD_D)
            fill(x, y + 7, w, 5, SKIN, SKIN_D, 4)
            fill(x, y + 9, w, 1, GOLD, (196, 40, 50))  # bangles

def leg(u, v):
    L = box_faces(u, v, 4, 12, 4)
    for f in L:
        x, y, w, h = L[f]
        if f == "top":
            fill(x, y, w, h, KURTA, KURTA_D)
        elif f == "bottom":
            fill(x, y, w, h, GOLD_D, GOLD)
        else:
            fill(x, y, w, 4, KURTA, KURTA_D)
            fill(x, y + 4, w, 1, GOLD, GOLD_D)
            fill(x, y + 5, w, 6, SALWAR, SALWAR_D)
            fill(x, y + 11, w, 1, GOLD, GOLD_D)

arm(40, 16); arm(32, 48)
leg(0, 16); leg(16, 48)
img.save(sys.argv[1])
print("wrote", sys.argv[1])
