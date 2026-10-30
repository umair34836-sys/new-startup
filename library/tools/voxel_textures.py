# Paint 16x16 Minecraft-style block textures (procedural, seeded) for CSS voxel worlds.
#   python3 voxel_textures.py OUT_DIR
# Writes: grass_top, grass_side, dirt, cobble, stone_brick, planks, dark_planks, log, leaves,
#         window_lit, door, awning, wool_red, lantern, iron, diamond_ore, emerald_ore, gold_block, tnt_side, tnt_top, obsidian.
import os, random, sys
from PIL import Image

out = sys.argv[1]
os.makedirs(out, exist_ok=True)

def tex(name, fn, seed):
    rnd = random.Random(seed)
    im = Image.new("RGBA", (16, 16))
    px = im.load()
    for y in range(16):
        for x in range(16):
            c = fn(x, y, rnd)
            px[x, y] = tuple(max(0, min(255, int(v))) for v in c) + (() if len(c) == 4 else (255,))
    im.save(os.path.join(out, name + ".png"))

def jit(c, rnd, a=10):
    j = rnd.randint(-a, a)
    return tuple(v + j for v in c[:3]) + tuple(c[3:])

GRASS = (88, 140, 52)
DIRT = (121, 85, 58)
tex("grass_top", lambda x, y, r: jit(GRASS if r.random() > 0.15 else (70, 120, 42), r, 12), 1)
tex("dirt", lambda x, y, r: jit(DIRT if r.random() > 0.2 else (96, 66, 44), r, 10), 2)
tex("grass_side", lambda x, y, r: jit(GRASS, r, 10) if (y < 3 or (y == 3 and r.random() < 0.5)) else jit(DIRT if r.random() > 0.2 else (96, 66, 44), r, 10), 3)

stones = [(random.Random(4).randint(0, 15), random.Random(5 + i).randint(0, 15)) for i in range(9)]
def cobble(x, y, r):
    d = sorted(((x - sx) % 16) ** 2 + ((y - sy) % 16) ** 2 for sx, sy in [(1, 1), (8, 2), (13, 6), (4, 7), (10, 10), (2, 13), (14, 14), (7, 14), (12, 0)])
    edge = d[1] - d[0] < 6
    return jit((70, 70, 72) if edge else (128, 128, 128), r, 12)
tex("cobble", cobble, 6)
tex("stone_brick", lambda x, y, r: jit((80, 80, 82) if (y % 8 == 7 or (x + (4 if (y // 8) % 2 else 0)) % 16 == 15) else (122, 122, 124), r, 8), 7)
def planks(c, dark):
    def f(x, y, r):
        line = y % 4 == 3
        seam = (y // 4) % 2 == 0 and x == 11 or (y // 4) % 2 == 1 and x == 4
        base = tuple(v * 0.7 for v in c) if (line or seam) else c
        return jit(base, r, 8)
    return f
tex("planks", planks((162, 130, 78), False), 8)
tex("dark_planks", planks((66, 44, 22), True), 9)
tex("log", lambda x, y, r: jit((92, 70, 42) if x % 4 else (64, 48, 28), r, 10), 10)
tex("leaves", lambda x, y, r: (0, 0, 0, 0) if r.random() < 0.12 else jit((44, 96, 34) if r.random() > 0.3 else (30, 72, 24), r, 12), 11)
def window(x, y, r):
    if x in (0, 15) or y in (0, 15) or x in (7, 8) or y in (7, 8):
        return jit((104, 78, 46), r, 6)
    glow = 1.0 - 0.25 * (abs(x - 7.5) + abs(y - 7.5)) / 15
    return jit((255 * glow, 182 * glow, 80 * glow), r, 8)
tex("window_lit", window, 12)
tex("door", lambda x, y, r: jit((70, 48, 26) if (x in (0, 15) or y in (0, 7, 15) or x == 8) else (118, 86, 50), r, 8) if not (x == 12 and y == 9) else (200, 170, 70), 13)
tex("awning", lambda x, y, r: jit((196, 40, 44) if (x // 4) % 2 == 0 else (236, 230, 222), r, 6), 14)
tex("wool_red", lambda x, y, r: jit((176, 32, 40), r, 8), 15)
tex("lantern", lambda x, y, r: jit((52, 52, 58), r, 6) if (x < 3 or x > 12 or y < 2 or y > 13) else jit((255, 200, 96) if 5 <= x <= 10 and 4 <= y <= 11 else (255, 160, 60), r, 10), 16)
tex("iron", lambda x, y, r: jit((44, 44, 50), r, 6), 17)
# added 2026-10-29 (Heaven Developer Minecraft phonk promo): ore / gold / TNT / obsidian for floating "item" blocks
def ore(colour, seed):
    spots = [(random.Random(seed + i).randint(1, 14), random.Random(seed + 50 + i).randint(1, 14)) for i in range(6)]
    def f(x, y, r):
        near = min(abs(x - sx) + abs(y - sy) for sx, sy in spots)
        return jit(colour if near <= 1 else (122, 122, 124), r, 10)
    return f
tex("diamond_ore", ore((92, 219, 213), 40), 18)
tex("emerald_ore", ore((23, 221, 98), 60), 19)
tex("gold_block", lambda x, y, r: jit((250, 210, 60) if 0 < x < 15 and 0 < y < 15 else (204, 150, 30), r, 10), 20)
tex("tnt_side", lambda x, y, r: jit((230, 230, 220), r, 6) if 6 <= y <= 9 else jit((200, 46, 34) if x % 4 else (150, 30, 24), r, 8), 21)
tex("tnt_top", lambda x, y, r: jit((40, 40, 40), r, 4) if abs(x - 7.5) + abs(y - 7.5) < 3 else jit((200, 46, 34), r, 8), 22)
tex("obsidian", lambda x, y, r: jit((40, 26, 60) if r.random() > 0.2 else (80, 56, 110), r, 8), 23)
print("textures written to", out)
