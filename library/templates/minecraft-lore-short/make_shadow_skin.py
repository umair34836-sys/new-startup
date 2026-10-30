# Own 64x64 classic skin: a hooded shadow figure (charcoal hoodie, dark face) with glowing white eyes.
import random, sys
from PIL import Image
rnd = random.Random(13)
img = Image.new("RGBA", (64, 64), (0, 0, 0, 0)); px = img.load()
HOOD, HOOD_D = (44, 46, 54), (32, 33, 40)
FACE, FACE_D = (58, 52, 50), (48, 43, 42)
PANTS, PANTS_D = (26, 28, 36), (20, 21, 28)
EYE = (255, 255, 255)
def put(x, y, c, j=5):
    k = rnd.randint(-j, j); px[x, y] = tuple(max(0, min(255, v + k)) for v in c[:3]) + (255,)
def fill(x, y, w, h, c, c2=None, j=5):
    for i in range(w):
        for k in range(h):
            put(x + i, y + k, c2 if (c2 and rnd.random() < 0.2) else c, j)
def faces(u, v, w, h, d):
    return {"top": (u + d, v, w, d), "bottom": (u + d + w, v, w, d), "right": (u, v + d, d, h),
            "front": (u + d, v + d, w, h), "left": (u + d + w, v + d, d, h), "back": (u + 2 * d + w, v + d, w, h)}
H = faces(0, 0, 8, 8, 8)
for f in H: fill(*H[f], HOOD, HOOD_D)
fx, fy = H["front"][:2]
fill(fx + 1, fy + 2, 6, 6, FACE, FACE_D)
for x in (2, 5):
    put(fx + x, fy + 4, EYE, 0)
put(fx + 3, fy + 4, FACE_D, 0); put(fx + 4, fy + 4, FACE_D, 0)
for (u, v) in ((16, 16), (40, 16), (32, 48)):
    w = 8 if u == 16 else 4
    F = faces(u, v, w, 12, 4)
    for f in F: fill(*F[f], HOOD, HOOD_D)
for (u, v) in ((0, 16), (16, 48)):
    F = faces(u, v, 4, 12, 4)
    for f in F: fill(*F[f], PANTS, PANTS_D)
img.save(sys.argv[1])
