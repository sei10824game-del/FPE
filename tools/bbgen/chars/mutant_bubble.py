"""Mutant Bubble (FPE Green mutant student, BUBBLE 003) - generates assets/fpe/bbmodels/mutant_bubble.bbmodel.
Reference: docs/ref/confirmed/mutant_bubble.png. SMALL kid (hitbox 0.6 x 1.2): huge fluffy foam-cloud hair with pointed side
tufts, foam "beard" puffing over the mouth and cheeks, mismatched eyes (char-right = black with a white star, char-left = pink
swirl), a little rubber duck with a blue comb stuck in the hair, white straitjacket jumpsuit with long closed sleeves,
"003" patch, black harness (centre strap + H belt), legs strapped together at the shins, sitting in a cloud of foam,
soap bubbles floating around the head.
Blockbench space: Y up, ground 0, faces -Z. Character's RIGHT = +X.
Rotation signs (file values): arm/leg rx>0 = swing forward, torso/head rx>0 = lean back / look up, ry>0 = turn to the
character's left, rz>0 = part swings toward +X (char right). Position z<0 = forward, y>0 = up.
Rest pose is the modelled pose (all rest rotations 0), so idle + walk layers add cleanly.
Every key tick matches entity/characters/MutantBubble.java.
Run: python3 tools/bbgen/chars/mutant_bubble.py
"""
import math, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from bbgen import Model, mix  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "../../../src/main/resources/assets/fpe/bbmodels/mutant_bubble.bbmodel")

# ------------------------------------------------------------------ palette (ink drawing, mostly white + grey, accents)
WH, WH_D, WH_DD, WH_L = 0xF3F3F6, 0xCDCED6, 0x9EA0AC, 0xFFFFFF
FOAM, FOAM_D, FOAM_S = 0xF8F9FC, 0xC9CCD8, 0x8F93A3
LINE = 0x2A2A33
BLK, BLK_L = 0x16161B, 0x3A3A45
METAL, METAL_D = 0xC8CCD4, 0x7C808C
GREY, GREY_D = 0xA9ABB6, 0x7D808D
PINK, PINK_D = 0xF08AB0, 0xB0406E
DUCK, DUCK_D, BEAK = 0xFFF6CC, 0xE6D08A, 0xF09A50
COMB, COMB_D = 0x9CC8DC, 0x5E8EA8
BUB, BUB_RIM, BUB_HI, BUB_TINT = 0xEAF5FF, 0x9FC2DA, 0xFFFFFF, 0xF4D8F0
CLEAR = (0, 0, 0, 0)

m = Model("mutant_bubble", S=8, atlas=2048)
R = m.rng
ALL = ("north", "south", "east", "west", "up", "down")


# ------------------------------------------------------------------ painters
def all_faces(fn, skip=()):
    return {k: fn for k in ALL if k not in skip}


def combo(*fns):
    def f(F):
        for fn in fns: fn(F)
    return f


def outline(c=LINE):
    return lambda F: (F.rect(0, 0, F.w, 1, c), F.rect(0, F.h - 1, F.w, 1, c), F.rect(0, 0, 1, F.h, c), F.rect(F.w - 1, 0, 1, F.h, c))


def cloth(base=WH, dark=WH_D, n=2, ink=True):
    """white canvas: vertical shading, soft fold lines, ink edge"""
    def f(F):
        for y in range(F.h):
            for x in range(F.w):
                k = y / max(1, F.h - 1)
                F.px(x, y, mix(base, dark, 0.06 + 0.3 * k * k + (0.1 if x < 2 or x > F.w - 3 else 0)))
        for i in range(n):
            x = int((i + 0.5) * F.w / n) + R.randint(-2, 2)
            for y in range(int(F.h * 0.3), F.h):
                F.px(x, y, mix(base, WH_DD, 0.4))
                F.px(x + 1, y, mix(base, WH_L, 0.5))
        if ink: outline()(F)
    return f


def foamp(dark=0.0):
    """soap foam: white with tiny grey bubble rings, darker toward the bottom, soft grey edge"""
    def f(F):
        for y in range(F.h):
            for x in range(F.w):
                k = y / max(1, F.h - 1)
                F.px(x, y, mix(FOAM, FOAM_D, min(1, dark + 0.35 * k * k)))
        for _ in range(max(1, F.w * F.h // 150)):
            cx, cy, r = R.uniform(1, F.w - 1), R.uniform(1, F.h - 1), R.uniform(0.8, 2.2)
            for a in range(0, 360, 30):
                F.px(int(cx + math.cos(math.radians(a)) * r), int(cy + math.sin(math.radians(a)) * r), mix(FOAM, FOAM_D, 0.7))
            F.px(int(cx - r * 0.4), int(cy - r * 0.4), WH_L)
        outline(mix(FOAM_D, FOAM_S, 0.5))(F)
    return f


def blackp(F):
    for y in range(F.h):
        for x in range(F.w):
            F.px(x, y, BLK_L if R.random() < 0.05 else BLK)
    F.rect(0, 1, F.w, 1, BLK_L)


def bubblep(F):
    """round soap bubble on a square face: clear corners, blue rim, iridescent band, white glint"""
    cx, cy = F.w / 2, F.h / 2
    r = min(F.w, F.h) / 2
    for y in range(F.h):
        for x in range(F.w):
            d = math.hypot(x + .5 - cx, y + .5 - cy) / r
            if d > 1: F.px(x, y, CLEAR)
            elif d > 0.8: F.px(x, y, BUB_RIM)
            elif d > 0.62 and (x + y) % 3 == 0: F.px(x, y, BUB_TINT)
            else: F.px(x, y, mix(BUB, BUB_RIM, 0.25 * d))
    F.disc(cx - r * 0.38, cy - r * 0.38, max(0.6, r * 0.22), BUB_HI)
    F.disc(cx + r * 0.35, cy + r * 0.42, max(0.4, r * 0.1), BUB_HI)


def shellp(F):
    """giant shield bubble: almost all clear, thin rim + glints so the kid shows through"""
    cx, cy = F.w / 2, F.h / 2
    for y in range(F.h):
        for x in range(F.w):
            d = math.hypot((x + .5 - cx) / (F.w / 2), (y + .5 - cy) / (F.h / 2))
            if 0.9 < d <= 1.0: F.px(x, y, BUB_RIM)
            elif 0.84 < d <= 0.9 and (x * 3 + y) % 5 == 0: F.px(x, y, BUB_TINT)
            else: F.px(x, y, CLEAR)
    F.line(F.w * 0.22, F.h * 0.34, F.w * 0.34, F.h * 0.16, BUB_HI, 2)
    F.disc(F.w * 0.7, F.h * 0.75, 1.5, BUB_HI)


def eye_star(F, ex, ey, r):
    F.disc(ex, ey, r + 1, LINE)
    F.disc(ex, ey, r, BLK)
    F.disc(ex - r * 0.45, ey - r * 0.5, 1.0, 0x5A5A68)
    pts = []
    for i in range(10):
        a = math.radians(-90 + i * 36)
        rr = r * (0.62 if i % 2 == 0 else 0.26)
        pts.append((ex + math.cos(a) * rr, ey + math.sin(a) * rr))
    F.poly(pts, WH_L, glow=True)


def eye_swirl(F, ex, ey, r):
    F.disc(ex, ey, r + 1, LINE)
    F.disc(ex, ey, r, 0xFFF4F8)
    for k in range(70):
        a = k * 0.32
        rr = 0.6 + k * (r - 1.2) / 70
        F.px(int(ex + math.cos(a) * rr), int(ey + math.sin(a) * rr), PINK, glow=True)
        F.px(int(ex + math.cos(a) * rr + .5), int(ey + math.sin(a) * rr), PINK_D)
    F.disc(ex, ey, 1.0, PINK_D, glow=True)


def face_front(F):
    W, H = F.w, F.h
    for y in range(H):
        for x in range(W):
            F.px(x, y, mix(WH, WH_D, 0.08 + 0.25 * (y / H)))
    ey = int(H * 0.46)
    eye_star(F, W * 0.3, ey, 7.2)        # char RIGHT eye (texel left)
    eye_swirl(F, W * 0.7, ey, 7.2)       # char LEFT eye (texel right)
    for ex in (W * 0.3, W * 0.7):        # little lower lashes like the art
        for i in (-4, 0, 4):
            F.line(ex + i, ey + 8.5, ex + i * 1.4, ey + 11.5, LINE, 1)
    outline(WH_DD)(F)


def digits003(F):
    F.rect(0, 0, F.w, F.h, BLK_L)
    outline(WH_DD)(F)
    font = {"0": ["111", "101", "101", "101", "111"], "3": ["111", "001", "011", "001", "111"]}
    x0, y0 = (F.w - 11) // 2, (F.h - 5) // 2
    for n, ch in enumerate("003"):
        for j, row in enumerate(font[ch]):
            for i, b in enumerate(row):
                if b == "1": F.px(x0 + n * 4 + i, y0 + j, WH_L)


def strapp(F):
    blackp(F)
    for x in range(2, F.w - 1, 6):
        F.px(x, F.h // 2, METAL)


# ------------------------------------------------------------------ shape helpers
def blob(name, parent, c, r, col=FOAM, sq=1.0, dark=0.0, rot=(0, 0, 0)):
    """rounded foam puff = three crossed boxes"""
    x, y, z = c
    p = foamp(dark)
    m.cube(name + "a", parent, (x - r, y - r * .68 * sq, z - r * .68), (x + r, y + r * .68 * sq, z + r * .68), col, origin=c, rot=rot, faces=all_faces(p))
    m.cube(name + "b", parent, (x - r * .68, y - r * sq, z - r * .68), (x + r * .68, y + r * sq, z + r * .68), col, origin=c, rot=rot, faces=all_faces(p))
    m.cube(name + "c", parent, (x - r * .68, y - r * .68 * sq, z - r), (x + r * .68, y + r * .68 * sq, z + r), col, origin=c, rot=rot, faces=all_faces(p))


def bubble(name, parent, c, r):
    x, y, z = c
    m.cube(name, parent, (x - r, y - r, z - r), (x + r, y + r, z + r), BUB, faces=all_faces(bubblep))


# ------------------------------------------------------------------ skeleton
m.group("root", (0, 0, 0))
m.group("foam", (0, 0, 0), parent="root")
FOAM_PUFFS = [((3.6, 1.6, 0.6), 2.0, 0.1), ((-3.4, 1.5, 0.4), 1.8, 0.1), ((0.4, 1.4, 3.4), 2.0, 0.15), ((0.0, 1.0, -3.0), 1.5, 0.0),
              ((3.0, 1.2, -2.4), 1.5, 0.05), ((-2.8, 1.1, -2.2), 1.4, 0.05), ((-2.6, 1.4, 3.0), 1.6, 0.15), ((3.0, 1.5, 3.0), 1.7, 0.15),
              ((4.6, 3.4, 1.6), 1.2, 0.0), ((-4.4, 3.0, 1.0), 1.0, 0.0)]
for i, (c, r, dk) in enumerate(FOAM_PUFFS):
    m.group(f"puff{i}", c, parent="foam")
m.group("body", (0, 6.0, 0), parent="root")
m.group("chest", (0, 6.2, 0), parent="body")
m.group("head", (0, 11.8, 0), parent="chest")
m.group("beard", (0, 13.4, -3.0), parent="head")
m.group("hair_top", (0, 17.6, 0), parent="head")
m.group("hair_b", (0, 16.0, 2.8), parent="head")
m.group("duck", (0.6, 19.4, 0.2), parent="hair_top")
for s, k in ((1, "r"), (-1, "l")):
    m.group("hair_" + k, (3.0 * s, 16.4, -0.4), parent="head")
    m.group("tuft_" + k, (3.0 * s, 18.0, -0.8), parent="head")
    m.group("arm_" + k, (3.4 * s, 11.0, 0), parent="chest")
    m.group("fore_" + k, (3.4 * s, 8.4, 0), parent="arm_" + k)
    m.group("leg_" + k, (1.1 * s, 6.0, 0), parent="body")
    m.group("shin_" + k, (1.1 * s, 3.3, 0), parent="leg_" + k)
m.group("wand", (3.4, 5.8, -0.6), parent="fore_r")
m.group("bubbles", (0, 15.0, 0), parent="body")
BUBS = [((-2.2, 21.6, 0.4), 0.55), ((-3.6, 20.0, -0.4), 1.0), ((4.6, 16.2, 1.0), 0.6), ((-5.0, 14.4, 0.8), 0.8), ((3.9, 20.6, -1.0), 0.5)]
for i, (c, r) in enumerate(BUBS):
    m.group(f"bub{i}", c, parent="bubbles")
m.group("spout", (0, 13.4, -4.2), parent="head")      # mouth bubble (spray / volley charge)
m.group("shell", (0, 9.5, 0), parent="root")         # shield bubble
m.group("surf", (0, 0, -1.0), parent="root")         # foam surge in front (wave / geyser)

# ------------------------------------------------------------------ foam cloud base
for i, (c, r, dk) in enumerate(FOAM_PUFFS):
    blob(f"puff{i}_", f"puff{i}", c, r, dark=dk, sq=0.8)

# ------------------------------------------------------------------ legs: white trousers strapped together, little boots
for s, k in ((1, "r"), (-1, "l")):
    x = 1.1 * s
    m.cube("thigh_" + k, "leg_" + k, (x - 1.05, 3.1, -1.1), (x + 1.05, 6.3, 1.1), WH,
           faces={"north": cloth(n=1), "south": cloth(n=1), "east": cloth(n=1), "west": cloth(n=1)})
    m.cube("calf_" + k, "shin_" + k, (x - 1.0, 0.8, -1.05), (x + 1.0, 3.5, 1.05), WH,
           faces={"north": cloth(n=1), "south": cloth(n=1), "east": cloth(n=1), "west": cloth(n=1)})
    m.cube("boot_" + k, "shin_" + k, (x - 1.1, 0.0, -1.4), (x + 1.1, 1.0, 1.15), WH_D, color2=GREY, grad=True, faces=all_faces(outline()))
    m.cube("sole_" + k, "shin_" + k, (x - 1.12, -0.02, -1.42), (x + 1.12, 0.25, 1.17), GREY_D)
    m.cube("kstrap_" + k, "leg_" + k, (x - 1.2, 3.5, -1.2), (x + 1.2, 4.1, 1.2), BLK, faces=all_faces(strapp))
    m.cube("sstrap_" + k, "shin_" + k, (x - 1.15, 1.6, -1.15), (x + 1.15, 2.2, 1.15), BLK, faces=all_faces(strapp))
    m.cube("sstrap2_" + k, "shin_" + k, (x - 1.15, 2.6, -1.15), (x + 1.15, 3.1, 1.15), BLK, faces=all_faces(strapp))
m.cube("kbuckle", "leg_r", (-0.2, 3.4, -1.35), (0.5, 4.2, -1.15), METAL, faces={"north": outline(METAL_D)})
m.cube("sbuckle", "shin_r", (-0.2, 1.5, -1.3), (0.5, 2.3, -1.1), METAL, faces={"north": outline(METAL_D)})
m.cube("sbuckle2", "shin_r", (-0.2, 2.5, -1.3), (0.5, 3.2, -1.1), METAL, faces={"north": outline(METAL_D)})

# ------------------------------------------------------------------ torso: straitjacket jumpsuit + harness
m.cube("torso", "chest", (-2.9, 6.0, -1.9), (2.9, 11.6, 1.9), WH,
       faces={"north": combo(cloth(n=2), lambda F: F.rect(F.w // 2, 0, 1, F.h, WH_DD)), "south": cloth(n=3), "east": cloth(n=1), "west": cloth(n=1),
              "up": cloth(n=1)})
m.cube("hips", "body", (-3.0, 5.4, -2.0), (3.0, 6.6, 2.0), WH, faces=all_faces(cloth(n=2), ("up",)))
m.cube("collar", "chest", (-2.3, 11.3, -1.7), (2.3, 12.1, 1.7), GREY, color2=GREY_D, grad=True, faces=all_faces(outline()))
m.cube("collar_f", "chest", (-1.6, 10.6, -2.05), (1.6, 11.7, -1.85), GREY, faces={"north": outline()})
m.cube("patch", "chest", (0.6, 9.7, -2.05), (2.5, 10.7, -1.9), BLK_L, faces={"north": digits003})
m.cube("strap_v", "chest", (-0.42, 6.2, -2.1), (0.42, 11.3, -1.88), BLK, faces=all_faces(strapp))
m.cube("strap_vb", "chest", (-0.42, 6.2, 1.88), (0.42, 11.3, 2.1), BLK, faces=all_faces(strapp))
m.cube("strap_sh", "chest", (-0.42, 11.2, -2.1), (0.42, 11.75, 2.1), BLK)
m.cube("belt", "chest", (-3.05, 7.0, -2.08), (3.05, 7.8, 2.08), BLK, faces=all_faces(strapp))
for s, k in ((1, "r"), (-1, "l")):
    m.cube("hbar_" + k, "chest", (2.0 * s - 0.35, 6.2, -2.12), (2.0 * s + 0.35, 8.8, -1.9), BLK, faces=all_faces(strapp))
    m.cube("buckle_" + k, "chest", (2.0 * s - 0.5, 7.0, -2.25), (2.0 * s + 0.5, 7.8, -2.05), METAL, faces={"north": combo(outline(METAL_D), lambda F: F.rect(2, 2, F.w - 4, F.h - 4, BLK))})
for i, y in enumerate((8.6, 9.6, 10.6)):
    m.cube(f"rivet{i}", "chest", (-0.22, y, -2.2), (0.22, y + 0.4, -2.08), METAL)
m.cube("dring", "chest", (-0.5, 10.9, -2.25), (0.5, 11.5, -2.05), METAL, faces={"north": combo(outline(METAL_D), lambda F: F.rect(2, 2, F.w - 4, F.h - 4, BLK))})
m.cube("buckle_c", "chest", (-0.55, 6.9, -2.25), (0.55, 7.9, -2.05), METAL, faces={"north": combo(outline(METAL_D), lambda F: F.rect(2, 2, F.w - 4, F.h - 4, BLK))})

# ------------------------------------------------------------------ arms: long closed straitjacket sleeves
for s, k in ((1, "r"), (-1, "l")):
    x = 3.6 * s
    m.cube("shoulder_" + k, "arm_" + k, (x - 1.0, 9.8, -1.2), (x + 1.0, 11.6, 1.2), WH, origin=(3.4 * s, 11, 0), rot=(0, 0, 6 * s),
           faces=all_faces(cloth(n=1)))
    m.cube("upsleeve_" + k, "arm_" + k, (x - 0.9, 8.0, -1.05), (x + 0.9, 10.4, 1.05), WH, faces=all_faces(cloth(n=1), ("up",)))
    m.cube("fsleeve_" + k, "fore_" + k, (x - 0.95, 5.9, -1.1), (x + 0.95, 8.6, 1.1), WH, faces=all_faces(cloth(n=1), ("up",)))
    m.cube("cuff_" + k, "fore_" + k, (x - 1.05, 5.1, -1.2), (x + 1.05, 6.1, 1.2), WH_L, color2=WH_D, grad=True, faces=all_faces(outline()))
    m.cube("sltip_" + k, "fore_" + k, (x - 0.7, 4.5, -0.8), (x + 0.7, 5.2, 0.8), WH_D, faces=all_faces(outline()))
    m.cube("abelt_" + k, "fore_" + k, (x - 1.05, 7.0, -1.18), (x + 1.05, 7.8, 1.18), BLK, faces=all_faces(strapp))
    m.cube("adangle_" + k, "fore_" + k, (x - 0.25, 3.4, -0.25), (x + 0.25, 5.2, 0.25), BLK, origin=(x, 5.1, 0), rot=(8, 0, 6 * s))
    m.cube("aring_" + k, "fore_" + k, (x - 0.35, 3.0, -0.35), (x + 0.35, 3.6, 0.35), METAL)
# bubble wand (hidden: pulled from the sleeve in bubble_volley)
m.cube("wand_stick", "wand", (3.2, 1.0, -0.8), (3.6, 5.8, -0.4), COMB, color2=COMB_D, grad=True)
for i, (a, b) in enumerate((((2.0, -1.4), (4.8, -1.0)), ((2.0, -3.0), (4.8, -2.6)), ((2.0, -3.0), (2.4, -1.0)), ((4.4, -3.0), (4.8, -1.0)))):
    m.cube(f"wand_ring{i}", "wand", (a[0], 0.4 + (0 if i < 2 else 0), -0.8 + a[1] + 1.4 - 1.4), (b[0], 0.8, -0.8 + b[1] + 1.4 - 1.4), PINK)
m.cube("wand_film", "wand", (2.4, 0.5, -2.6), (4.4, 0.7, -1.4), BUB, faces={"up": bubblep, "down": bubblep})

# ------------------------------------------------------------------ head, face, foam beard
m.cube("skull", "head", (-3.2, 12.0, -3.0), (3.2, 17.8, 3.0), WH, faces={"north": face_front, "south": foamp(), "east": foamp(), "west": foamp(), "down": foamp(0.2)})
m.cube("neck", "head", (-1.2, 11.4, -1.0), (1.2, 12.4, 1.0), GREY_D)
BEARD = [((0, 13.4, -3.25), 1.35), ((1.7, 12.9, -3.0), 1.25), ((-1.7, 12.9, -3.0), 1.25), ((2.9, 12.5, -2.1), 1.05), ((-2.9, 12.5, -2.1), 1.05),
         ((0, 12.0, -2.8), 1.0), ((0.9, 11.6, -2.6), 0.75), ((-0.9, 11.6, -2.6), 0.75), ((0, 15.0, -3.15), 0.55)]
for i, (c, r) in enumerate(BEARD):
    blob(f"brd{i}_", "beard", c, r, sq=0.9)

# ------------------------------------------------------------------ foam-cloud hair: cap puffs, fringe curls, side + back fluff, pointed tufts
TOP = [((0, 18.4, 0), 2.4), ((-2.2, 18.0, -1.6), 1.6), ((2.2, 18.2, -1.4), 1.6), ((-2.2, 18.3, 1.6), 1.7), ((2.0, 18.1, 1.8), 1.6),
       ((0.2, 19.6, -0.6), 1.3), ((-0.8, 17.8, -2.9), 1.15), ((1.0, 17.6, -3.1), 1.0), ((-2.6, 17.0, -3.0), 0.9), ((2.6, 16.9, -3.0), 0.9)]
for i, (c, r) in enumerate(TOP):
    blob(f"top{i}_", "hair_top", c, r, sq=0.8)
m.cube("curl", "hair_top", (-1.3, 16.7, -3.75), (-0.3, 17.5, -3.35), FOAM, origin=(-0.8, 17.1, -3.5), rot=(0, 0, 45), faces=all_faces(foamp()))
for s, k in ((1, "r"), (-1, "l")):
    for i, (dy, dz, r) in enumerate(((0.0, -1.8, 1.2), (-0.6, 0.4, 1.3), (-1.8, -1.0, 1.0), (-2.6, 1.0, 0.95), (0.4, 2.0, 1.1))):
        blob(f"side{i}_{k}", "hair_" + k, (3.3 * s, 16.0 + dy, dz), r, sq=0.9, dark=0.05)
    # pointed tufts poking up/out (cat-ear look of the art)
    m.cube("tuftA_" + k, "tuft_" + k, (3.0 * s - 0.8, 17.2, -1.4), (3.0 * s + 0.8, 20.2, -0.2), FOAM, origin=(3.0 * s, 17.6, -0.8), rot=(0, 0, 38 * s),
           faces=all_faces(foamp()))
    m.cube("tuftB_" + k, "tuft_" + k, (3.0 * s - 0.5, 17.0, 0.2), (3.0 * s + 0.5, 19.2, 1.2), FOAM, origin=(3.0 * s, 17.4, 0.7), rot=(-10, 0, 56 * s),
           faces=all_faces(foamp(0.05)))
    m.cube("tuftC_" + k, "tuft_" + k, (3.2 * s - 0.45, 14.6, -2.6), (3.2 * s + 0.45, 16.6, -1.6), FOAM, origin=(3.2 * s, 16.4, -2.1), rot=(0, 0, -30 * s),
           faces=all_faces(foamp()))
for i, (x, y, r) in enumerate(((-2.0, 15.6, 1.4), (0.0, 15.2, 1.6), (2.0, 15.6, 1.4), (-1.0, 13.4, 1.2), (1.1, 13.3, 1.2), (0, 17.0, 1.5))):
    blob(f"back{i}_", "hair_b", (x, y, 3.0 + (0.3 if i == 1 else 0)), r, sq=0.9, dark=0.08)

# ------------------------------------------------------------------ rubber duck + blue comb on the hair
dk = (0.6, 19.4, 0.2)
def D(a, b): return (dk[0] + a[0], dk[1] + a[1], dk[2] + a[2]), (dk[0] + b[0], dk[1] + b[1], dk[2] + b[2])
duckp = lambda F: (F.rect(0, 0, F.w, F.h, DUCK), F.rect(0, F.h - 2, F.w, 2, DUCK_D), outline(0x8A7A50)(F))
m.cube("duck_body", "duck", *D((-1.2, 0.0, -0.9), (1.2, 1.4, 1.5)), DUCK, faces=all_faces(duckp))
m.cube("duck_wing_r", "duck", *D((1.15, 0.4, -0.3), (1.35, 1.1, 1.0)), DUCK_D)
m.cube("duck_wing_l", "duck", *D((-1.35, 0.4, -0.3), (-1.15, 1.1, 1.0)), DUCK_D)
m.cube("duck_head", "duck", *D((-0.75, 1.2, -1.3), (0.75, 2.6, 0.1)), DUCK,
       faces={"east": lambda F: (duckp(F), F.rect(F.w // 2 - 2, 3, 2, 2, BLK)), "west": lambda F: (duckp(F), F.rect(F.w // 2, 3, 2, 2, BLK)),
              "north": duckp, "south": duckp, "up": duckp})
m.cube("duck_beak", "duck", *D((-0.45, 1.45, -1.9), (0.45, 1.9, -1.2)), BEAK, faces=all_faces(outline(0xA05A20)))
m.cube("duck_tail", "duck", *D((-0.4, 1.1, 1.3), (0.4, 1.9, 1.8)), DUCK, origin=(dk[0], dk[1] + 1.1, dk[2] + 1.4), rot=(-30, 0, 0))
combp = lambda F: (F.rect(0, 0, F.w, F.h, COMB), [F.rect(x, F.h // 2, 1, F.h, COMB_D) for x in range(1, F.w, 3)], outline(COMB_D)(F))
m.cube("comb", "duck", *D((-3.2, 0.9, -0.1), (2.0, 1.5, 0.3)), COMB, origin=(dk[0], dk[1] + 1.2, dk[2]), rot=(0, -20, -24),
       faces={"north": combp, "south": combp, "up": combp, "down": combp})

# ------------------------------------------------------------------ floating bubbles, mouth bubble, shield bubble, foam surge
for i, (c, r) in enumerate(BUBS):
    bubble(f"bub{i}_s", f"bub{i}", c, r)
bubble("spout_bub", "spout", (0, 13.4, -5.6), 1.4)
m.cube("shell_s", "shell", (-5.4, -0.6, -5.4), (5.4, 20.4, 5.4), BUB, faces=all_faces(shellp))
for i, (x, z, r) in enumerate(((0, -3.6, 1.6), (-2.0, -3.0, 1.3), (2.0, -3.0, 1.3), (-1.0, -5.0, 1.1), (1.2, -5.2, 1.2), (0, -6.6, 1.0))):
    blob(f"surf{i}_", "surf", (x, 1.0 + r * 0.4, z - 1.0), r, sq=1.1)


# ================================================================== animation
PROPS = ["wand", "spout", "shell", "surf"]
HIDE = (.001, .001, .001)


class A:
    def __init__(self, name, ticks, loop=False):
        self.name, self.ticks, self.loop, self.tr = name, ticks, loop, {}

    def k(self, bone, ch, keys):
        self.tr.setdefault(bone, {}).setdefault(ch, []).extend(keys)
        return self

    def rot(self, bone, *keys): return self.k(bone, "rotation", keys)
    def pos(self, bone, *keys): return self.k(bone, "position", keys)
    def scl(self, bone, *keys): return self.k(bone, "scale", keys)

    def _frame(self, keys, zero):
        ks = list(keys)
        if ks[0][0] > 0: ks.insert(0, (0, *zero))
        if ks[-1][0] < self.ticks and not self.loop: ks.append((self.ticks, *zero))
        return ks

    def r(self, bone, *keys):
        """rotation keys, framed by the rest pose (0) at the start and the end"""
        return self.rot(bone, *self._frame(keys, (0, 0, 0)))

    def p(self, bone, *keys):
        return self.pos(bone, *self._frame(keys, (0, 0, 0)))

    def s(self, bone, *keys):
        return self.scl(bone, *self._frame(keys, (1, 1, 1)))

    def show(self, bone, *wins):
        """prop visible inside [t0,t1] with a pop-in overshoot"""
        keys = [(0, *HIDE)]
        for (t0, t1) in wins:
            keys += [(max(0, t0 - 0.5), *HIDE), (t0, 1, 1, 1), (t0 + 1, 1.25, 1.25, 1.25), (t0 + 2, 1, 1, 1), (t1, 1, 1, 1), (t1 + 0.5, *HIDE)]
        return self.scl(bone, *keys)

    def lag(self, bone, keys, delay=2, gain=1.0):
        """secondary motion: same curve, delayed"""
        seen, out = set(), []
        for (t, x, y, z) in keys:
            tt = min(self.ticks, t + delay)
            if tt in seen: continue
            seen.add(tt); out.append((tt, x * gain, y * gain, z * gain))
        return self.r(bone, *out)

    def hair(self, keys, delay=2):
        """keys: x>0 = fluff flicks back/up, z>0 = toward +X. top/back/sides/tufts/duck lag in a chain"""
        self.lag("hair_top", [(t, x * 0.5, 0, z * 0.5) for (t, x, y, z) in keys], delay)
        self.lag("hair_b", [(t, x * 0.8, 0, z * 0.5) for (t, x, y, z) in keys], delay + 1)
        self.lag("hair_r", [(t, x * 0.4, 0, z * 0.6 + max(0, x) * 0.4) for (t, x, y, z) in keys], delay + 1)
        self.lag("hair_l", [(t, x * 0.4, 0, z * 0.6 - max(0, x) * 0.4) for (t, x, y, z) in keys], delay + 1)
        self.lag("tuft_r", [(t, x * 0.3, 0, z * 0.8 + abs(x) * 0.5) for (t, x, y, z) in keys], delay + 2)
        self.lag("tuft_l", [(t, x * 0.3, 0, z * 0.8 - abs(x) * 0.5) for (t, x, y, z) in keys], delay + 2)
        self.lag("duck", [(t, x * 1.2, 0, z * 1.4) for (t, x, y, z) in keys], delay + 3)
        self.lag("beard", [(t, x * 0.3, 0, z * 0.3) for (t, x, y, z) in keys], delay)
        return self

    def foam(self, amp=1.0, t0=0, t1=None, speed=1.0):
        """each puff of the foam cloud breathes with its own phase"""
        t1 = self.ticks if t1 is None else t1
        for i in range(len(FOAM_PUFFS)):
            ks, n = [], max(2, int((t1 - t0) / (10 / speed)))
            for j in range(n + 1):
                t = t0 + (t1 - t0) * j / n
                v = 1 + 0.08 * amp * math.sin(j * 2.1 + i * 1.7)
                ks.append((round(t, 2), v, 1 + 0.12 * amp * math.sin(j * 2.1 + i * 1.7 + 1), v))
            self.scl(f"puff{i}", *ks)
        return self

    def bubs(self, amp=1.0, t0=0, t1=None):
        """floating bubbles bob in place"""
        t1 = self.ticks if t1 is None else t1
        for i in range(len(BUBS)):
            n = max(2, int((t1 - t0) / 10))
            ks = [(round(t0 + (t1 - t0) * j / n, 2), 0, 0.5 * amp * math.sin(j * 1.9 + i * 2.3), 0.2 * amp * math.cos(j * 1.9 + i)) for j in range(n + 1)]
            if self.loop: ks[-1] = (ks[-1][0], *ks[0][1:])
            self.pos(f"bub{i}", *ks)
        return self

    def done(self):
        for p in PROPS:
            if p not in self.tr or "scale" not in self.tr[p]:
                self.scl(p, (0, *HIDE))
        tracks = {b: {ch: sorted([(t / 20.0, x, y, z) for (t, x, y, z) in v], key=lambda q: q[0]) for ch, v in chs.items()}
                  for b, chs in self.tr.items()}
        m.anim(self.name, self.ticks / 20.0, tracks, loop=self.loop)


def sym(a, bone_r, keys_r, bone_l=None):
    """same keys for both sides (mirrored y/z)"""
    a.r(bone_r, *keys_r)
    a.r(bone_l or bone_r.replace("_r", "_l"), *[(t, x, -y, -z) for (t, x, y, z) in keys_r])


def legs(a, kr, kl=None, sr=None, sl=None):
    a.r("leg_r", *kr)
    a.r("leg_l", *(kl or [(t, x, -y, -z) for (t, x, y, z) in kr]))
    if sr: a.r("shin_r", *sr)
    if sl or sr: a.r("shin_l", *(sl or sr))


# ------------------------------------------------------------------ idle (80 loop): breathing, head tilts, sleeves sway, duck wobble, bubbles bob
a = A("idle", 80, loop=True)
a.pos("body", (0, 0, 0, 0), (20, 0, -0.18, 0), (40, 0, 0, 0), (60, 0, -0.18, 0), (80, 0, 0, 0))
a.rot("chest", (0, 0, 0, 0), (20, 2, 0, 1), (40, 0, 0, 0), (60, 2, 0, -1), (80, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (16, 0, 0, 0), (22, 2, 8, 12), (34, 2, 8, 12), (40, 0, 0, 0), (56, 0, 0, 0), (62, -4, -10, -8), (72, -4, -10, -8), (80, 0, 0, 0))
a.rot("arm_r", (0, 0, 0, 2), (20, 3, 0, 4), (40, 0, 0, 2), (60, -3, 0, 3), (80, 0, 0, 2))
a.rot("arm_l", (0, 0, 0, -2), (20, -3, 0, -3), (40, 0, 0, -2), (60, 3, 0, -4), (80, 0, 0, -2))
a.rot("fore_r", (0, 4, 0, 0), (40, 8, 0, 0), (80, 4, 0, 0))
a.rot("fore_l", (0, 8, 0, 0), (40, 4, 0, 0), (80, 8, 0, 0))
a.rot("beard", (0, 0, 0, 0), (10, 3, 0, 0), (20, 0, 0, 0), (50, 3, 0, 0), (60, 0, 0, 0), (80, 0, 0, 0))
a.rot("duck", (0, 0, 0, 0), (24, 0, 0, 0), (27, -8, 0, 14), (30, 4, 0, -8), (33, 0, 0, 4), (36, 0, 0, 0), (64, 0, 0, 0), (67, -6, 0, -12), (71, 0, 0, 6),
      (74, 0, 0, 0), (80, 0, 0, 0))
for b, ph in (("hair_top", 0), ("hair_b", 4), ("tuft_r", 8), ("tuft_l", 12), ("hair_r", 6), ("hair_l", 10)):
    a.rot(b, *[(t, 2 * math.sin((t + ph) / 80 * 6.283), 0, 3 * math.sin((t + ph) / 40 * 6.283) * (1 if "l" not in b[-1] else -1)) for t in range(0, 81, 10)])
a.foam(1.0).bubs(1.0)
a.rot("bubbles", (0, 0, 0, 0), (40, 0, 180, 0), (80, 0, 360, 0))
a.done()

# ------------------------------------------------------------------ walk (20 loop): bound legs -> little waddle-hop, body rolls, sleeves flap
a = A("walk", 20, loop=True)
a.pos("body", (0, 0, 0, 0), (3, 0, 0.7, 0), (5, 0, 0, 0), (8, 0, 0.0, 0), (10, 0, 0, 0), (13, 0, 0.7, 0), (15, 0, 0, 0), (20, 0, 0, 0))
a.rot("body", (0, 0, 0, 5), (5, 4, 0, 0), (10, 0, 0, -5), (15, 4, 0, 0), (20, 0, 0, 5))
a.rot("leg_r", (0, 16, 0, 0), (5, 0, 0, 0), (10, -14, 0, 0), (15, 0, 0, 0), (20, 16, 0, 0))
a.rot("leg_l", (0, -14, 0, 0), (5, 0, 0, 0), (10, 16, 0, 0), (15, 0, 0, 0), (20, -14, 0, 0))
a.rot("shin_r", (0, 0, 0, 0), (12, -14, 0, 0), (16, -6, 0, 0), (20, 0, 0, 0))
a.rot("shin_l", (0, 0, 0, 0), (2, -14, 0, 0), (6, -6, 0, 0), (10, 0, 0, 0), (20, 0, 0, 0))
a.rot("arm_r", (0, -20, 0, 8), (10, 22, 0, 10), (20, -20, 0, 8))
a.rot("arm_l", (0, 22, 0, -10), (10, -20, 0, -8), (20, 22, 0, -10))
a.rot("fore_r", (0, 6, 0, 0), (3, 18, 0, 0), (10, 6, 0, 0), (13, 2, 0, 0), (20, 6, 0, 0))
a.rot("fore_l", (0, 6, 0, 0), (3, 2, 0, 0), (10, 6, 0, 0), (13, 18, 0, 0), (20, 6, 0, 0))
a.rot("head", (0, 0, 0, -4), (5, -3, 0, 0), (10, 0, 0, 4), (15, -3, 0, 0), (20, 0, 0, -4))
a.rot("hair_top", (0, 0, 0, 3), (5, 4, 0, 0), (10, 0, 0, -3), (15, 4, 0, 0), (20, 0, 0, 3))
a.rot("tuft_r", (0, 0, 0, 8), (5, 0, 0, -4), (10, 0, 0, 8), (15, 0, 0, -4), (20, 0, 0, 8))
a.rot("tuft_l", (0, 0, 0, 4), (5, 0, 0, -8), (10, 0, 0, 4), (15, 0, 0, -8), (20, 0, 0, 4))
a.rot("duck", (0, -6, 0, 6), (5, 8, 0, 0), (10, -6, 0, -6), (15, 8, 0, 0), (20, -6, 0, 6))
a.rot("hair_b", (0, 4, 0, 0), (5, -4, 0, 0), (10, 4, 0, 0), (15, -4, 0, 0), (20, 4, 0, 0))
a.rot("beard", (0, 0, 0, 0), (4, 6, 0, 0), (10, 0, 0, 0), (14, 6, 0, 0), (20, 0, 0, 0))
a.foam(1.6, speed=2).bubs(0.6)
a.done()

# ------------------------------------------------------------------ foam_slap (26): R sleeve cocks back 0-6, slaps across t8, L cocks 9-13, slaps t15, recover
a = A("foam_slap", 26)
a.r("chest", (5, 0, -26, 2), (8, -6, 34, -4), (10, -4, 30, -2), (13, 0, 30, 2), (15, -6, -34, 4), (17, -4, -30, 2), (22, 0, -6, 0))
a.r("head", (5, 0, 14, 6), (8, 4, -20, -4), (12, 0, -14, 0), (15, 4, 22, 6), (19, 0, 10, 0))
a.r("arm_r", (5, -30, 0, 70), (7, -10, 0, 82), (8, 60, -40, 20), (10, 66, -50, 4), (13, 30, -20, 10), (18, 4, 0, 4))
a.r("fore_r", (5, 30, 0, 0), (8, -10, 0, 0), (10, 20, 0, 0), (16, 10, 0, 0))
a.r("arm_l", (6, 10, 0, -10), (10, -20, 0, -60), (13, -30, 0, -78), (15, 60, 40, -20), (17, 64, 48, -6), (21, 20, 10, -6))
a.r("fore_l", (12, 30, 0, 0), (15, -10, 0, 0), (17, 20, 0, 0), (22, 6, 0, 0))
a.p("body", (5, 0.4, 0, 0.4), (8, -0.4, 0, -0.8), (13, -0.4, 0, -0.4), (15, 0.4, 0, -1.2), (20, 0, 0, -0.6))
legs(a, [(5, -6, 0, 0), (8, 8, 0, 0), (13, -6, 0, 0), (15, 8, 0, 0), (20, 0, 0, 0)])
a.hair([(0, 0, 0, 0), (5, 2, 0, 8), (8, -4, 0, -14), (12, 2, 0, -6), (15, -4, 0, 14), (19, 2, 0, 4), (26, 0, 0, 0)], delay=1)
a.foam(1.4).bubs(1.4)
a.done()

# ------------------------------------------------------------------ bubble_bonk (28): squash 0-8, hop forward t9, head SLAM down t12, bounce + wobble recover
a = A("bubble_bonk", 28)
a.p("body", (4, 0, -1.4, 1.0), (8, 0, -1.8, 1.4), (10, 0, 2.6, -1.6), (12, 0, 0.6, -3.2), (14, 0, -0.8, -3.0), (17, 0, 0.6, -2.0), (21, 0, 0, -0.8))
a.r("chest", (4, -14, 0, 0), (8, 18, 0, 0), (10, 6, 0, 0), (12, -44, 0, 0), (14, -40, 0, 0), (17, -10, 0, 0), (21, 4, 0, 0))
a.r("head", (4, -6, 0, 0), (8, 22, 0, 0), (10, 10, 0, 0), (12, -30, 0, 0), (14, -26, 0, 6), (16, -10, 0, -8), (19, 4, 0, 6), (23, 0, 0, -2))
sym(a, "arm_r", [(4, -20, 0, 20), (8, -40, 0, 40), (10, -90, 0, 30), (12, -130, 0, 10), (15, -60, 0, 30), (20, -10, 0, 10)])
sym(a, "fore_r", [(8, 20, 0, 0), (12, -10, 0, 0), (17, 20, 0, 0)])
legs(a, [(4, 40, 0, 0), (8, 50, 0, 0), (10, -30, 0, 0), (12, 10, 0, 0), (14, 30, 0, 0), (19, 0, 0, 0)],
     sr=[(4, -70, 0, 0), (8, -80, 0, 0), (10, -10, 0, 0), (12, -30, 0, 0), (14, -50, 0, 0), (19, 0, 0, 0)])
a.s("head", (8, 1.08, 0.9, 1.08), (12, 1.0, 1.0, 1.0), (13, 1.14, 0.84, 1.14), (15, 0.95, 1.06, 0.95), (17, 1, 1, 1))
a.hair([(0, 0, 0, 0), (6, -8, 0, 0), (10, -16, 0, 0), (12, 26, 0, 0), (14, 20, 0, 8), (17, -6, 0, -8), (21, 4, 0, 4), (28, 0, 0, 0)], delay=1)
a.foam(2.0).bubs(1.6)
a.done()

# ------------------------------------------------------------------ soap_spray (36): inhale 0-8 (lean back, beard puffs), SPRAY t10-26 sweeping L-R, recover
a = A("soap_spray", 36)
a.r("chest", (6, 16, 0, 0), (8, 18, 0, 0), (10, -10, -16, 0), (14, -12, 14, 0), (18, -12, -14, 0), (22, -12, 14, 0), (26, -10, 0, 0), (30, 4, 0, 0))
a.r("head", (6, 16, 0, 0), (8, 20, 0, 0), (10, -14, -12, 0), (14, -14, 14, 0), (18, -14, -14, 0), (22, -14, 14, 0), (26, -10, 0, 0), (30, 4, 0, 0))
a.s("beard", (4, 1.1, 1.1, 1.1), (8, 1.35, 1.25, 1.4), (10, 1.1, 1.0, 1.2), (26, 1.15, 1.0, 1.2), (29, 0.95, 0.95, 0.95), (32, 1, 1, 1))
a.r("beard", (8, 10, 0, 0), (10, -20, 0, 0), (12, -14, 0, 0), (26, -18, 0, 0), (30, 0, 0, 0))
a.scl("spout", (0, *HIDE), (9.5, *HIDE), (10, 0.6, 0.6, 0.6), (11, 1.3, 1.3, 1.3), (12, 0.8, 0.8, 0.8), (13, 1.2, 1.2, 1.2), (14, 0.8, 0.8, 0.8),
      (16, 1.2, 1.2, 1.2), (18, 0.8, 0.8, 0.8), (20, 1.2, 1.2, 1.2), (22, 0.8, 0.8, 0.8), (24, 1.2, 1.2, 1.2), (26, 1, 1, 1), (27, *HIDE), (36, *HIDE))
a.pos("spout", (0, 0, 0, 0), (10, 0, 0, 0), (11, 0, 0, -1.2), (12, 0, 0, 0), (13, 0, 0, -1.2), (14, 0, 0, 0), (16, 0, 0, -1.2), (18, 0, 0, 0), (20, 0, 0, -1.2),
      (22, 0, 0, 0), (24, 0, 0, -1.2), (26, 0, 0, 0), (36, 0, 0, 0))
sym(a, "arm_r", [(6, -10, 0, 30), (8, -14, 0, 36), (10, 10, 0, 50), (26, 10, 0, 46), (30, 0, 0, 10)])
sym(a, "fore_r", [(8, 20, 0, 0), (10, -10, 0, 0), (26, -6, 0, 0), (30, 10, 0, 0)])
a.p("body", (8, 0, 0.3, 0.6), (10, 0, -0.3, -0.4), (26, 0, -0.3, -0.2), (30, 0, 0, 0))
legs(a, [(8, -6, 0, 0), (10, 8, 0, 0), (26, 8, 0, 0), (30, 0, 0, 0)])
a.hair([(0, 0, 0, 0), (8, -6, 0, 0), (10, 14, 0, 0), (14, 12, 0, -8), (18, 12, 0, 8), (22, 12, 0, -8), (26, 10, 0, 0), (32, 0, 0, 0)], delay=2)
a.foam(1.2).bubs(1.2)
a.done()

# ------------------------------------------------------------------ bubble_volley (30): wand slides out of the sleeve 0-6, wind back 6-11, sweeping wave t14 (fan), follow-through, tuck
a = A("bubble_volley", 30)
a.show("wand", (4, 25))
a.r("arm_r", (4, -40, 0, 20), (8, -20, 30, 70), (11, -10, 40, 90), (13, 50, -20, 40), (14, 70, -40, 20), (17, 60, -60, -10), (22, 20, -10, 10), (26, 0, 0, 4))
a.r("fore_r", (4, 40, 0, 0), (8, 30, 0, 0), (11, 40, 0, 0), (14, -10, 0, 0), (17, 10, 0, 0), (24, 6, 0, 0))
a.r("wand", (11, 0, 0, -30), (14, 30, 0, 20), (17, 20, 0, 40), (22, 0, 0, 0))
a.r("arm_l", (4, -30, 0, -20), (8, -10, 0, -30), (14, 20, 0, -40), (20, 0, 0, -16))
a.r("chest", (8, 4, -24, -4), (11, 6, -34, -6), (13, -4, 10, 2), (14, -8, 30, 4), (17, -6, 34, 2), (22, 0, 10, 0))
a.r("head", (8, 6, 20, 4), (11, 6, 26, 0), (14, -4, -20, 0), (17, -2, -24, -4), (22, 0, -8, 0))
a.p("body", (8, 0.3, 0, 0.6), (11, 0.4, 0, 0.8), (14, -0.4, 0, -1.0), (17, -0.4, 0, -0.8), (24, 0, 0, 0))
legs(a, [(8, -10, 0, 0), (14, 10, 0, 0), (20, 0, 0, 0)])
a.s("bubbles", (10, 1.2, 1.2, 1.2), (14, 1.5, 1.5, 1.5), (16, 0.6, 0.6, 0.6), (22, 1, 1, 1))
a.r("bubbles", (14, 0, -40, 0), (22, 0, -90, 0), (30, 0, -90, 0))
a.hair([(0, 0, 0, 0), (8, 2, 0, 8), (11, 4, 0, 12), (14, -6, 0, -14), (18, 2, 0, -8), (24, 0, 0, 0)], delay=2)
a.foam(1.3)
a.done()

# ------------------------------------------------------------------ bubble_trap (44): sleeves rise conjuring 0-10, thrust forward t14 (target enveloped t16), hold-sway 16-36, CLAP t38 = pop, recover
a = A("bubble_trap", 44)
sym(a, "arm_r", [(4, -40, 0, 40), (10, -150, 0, 30), (12, -160, 0, 20), (14, 80, 0, 12), (16, 90, 0, 16), (24, 92, 0, 24), (32, 92, 0, 30), (36, 100, 0, 40),
                 (38, 96, 0, 2), (39, 94, 0, 0), (42, 40, 0, 10)])
sym(a, "fore_r", [(10, 10, 0, 0), (14, -10, 0, 0), (36, 0, 0, 0), (38, -6, 0, 0), (42, 10, 0, 0)])
a.r("chest", (6, 10, 0, 0), (10, 16, 0, 0), (14, -16, 0, 0), (16, -14, 0, 0), (24, -10, 8, 0), (32, -10, -8, 0), (36, -6, 0, 0), (38, -18, 0, 0), (42, -4, 0, 0))
a.r("head", (10, 20, 0, 0), (14, -10, 0, 0), (20, -6, 0, 10), (28, -6, 0, -10), (36, 2, 0, 0), (38, -14, 0, 0), (41, 6, 0, 0))
a.p("body", (10, 0, 0.6, 0.4), (14, 0, -0.2, -0.8), (36, 0, 0, -0.4), (38, 0, -0.4, -1.0), (42, 0, 0, -0.2))
legs(a, [(10, -6, 0, 0), (14, 10, 0, 0), (36, 6, 0, 0), (38, 12, 0, 0)])
a.s("bubbles", (6, 1.2, 1.2, 1.2), (12, 1.6, 1.6, 1.6), (14, 0.2, 0.2, 0.2), (30, 0.4, 0.4, 0.4), (38, 0.5, 0.5, 0.5), (40, 1.1, 1.1, 1.1), (42, 1, 1, 1))
a.r("bubbles", (12, 0, 360, 0), (14, 0, 400, 0), (44, 0, 400, 0))
a.hair([(0, 0, 0, 0), (10, -8, 0, 0), (14, 14, 0, 0), (20, 4, 0, 8), (28, 4, 0, -8), (36, 0, 0, 0), (38, 12, 0, 0), (42, 0, 0, 0)], delay=2)
a.foam(1.2).bubs(0.8, 16, 36)
a.done()

# ------------------------------------------------------------------ foam_wave (32): sinks into the foam 0-10 (foam swells), both sleeves heave forward t14 = surf rolls out, recover
a = A("foam_wave", 32)
a.p("body", (6, 0, -1.6, 0.6), (10, 0, -2.2, 0.8), (13, 0, 0.6, -0.6), (14, 0, 0.8, -1.2), (18, 0, 0.2, -0.8), (24, 0, 0, 0))
a.r("chest", (6, -18, 0, 0), (10, -24, 0, 0), (13, -30, 0, 0), (14, -34, 0, 0), (18, -20, 0, 0), (24, -4, 0, 0))
a.r("head", (6, 10, 0, 0), (10, 16, 0, 0), (14, 8, 0, 0), (20, 4, 0, 0))
sym(a, "arm_r", [(6, -20, 0, 50), (10, -30, 0, 60), (13, 60, 0, 30), (14, 90, 0, 12), (18, 80, 0, 16), (24, 20, 0, 10)])
sym(a, "fore_r", [(10, 30, 0, 0), (14, -10, 0, 0), (20, 10, 0, 0)])
legs(a, [(6, 40, 0, 0), (10, 50, 0, 0), (14, 20, 0, 0), (22, 0, 0, 0)], sr=[(6, -60, 0, 0), (10, -70, 0, 0), (14, -30, 0, 0), (22, 0, 0, 0)])
a.scl("foam", (0, 1, 1, 1), (6, 1.2, 1.3, 1.2), (10, 1.35, 1.6, 1.35), (13, 1.1, 1.0, 1.1), (16, 1, 1, 1), (32, 1, 1, 1))
a.scl("surf", (0, *HIDE), (12.5, *HIDE), (13, 0.5, 0.5, 0.5), (14, 1.3, 1.5, 1.2), (16, 1.6, 1.2, 1.8), (20, 1.8, 0.9, 2.2), (24, 1.5, 0.4, 2.4), (25, *HIDE), (32, *HIDE))
a.pos("surf", (0, 0, 0, 0), (13, 0, 0, 0), (16, 0, 0, -3), (20, 0, 0, -6), (24, 0, 0, -9), (32, 0, 0, -9))
a.hair([(0, 0, 0, 0), (8, 8, 0, 0), (12, -10, 0, 0), (14, 14, 0, 0), (20, 4, 0, 0), (28, 0, 0, 0)], delay=2)
a.foam(0.6).bubs(1.4)
a.done()

# ------------------------------------------------------------------ lather_slide (30): lean 0-6, belly-flop t8, slides on foam 8-18 (hits), pushes up 20-26
a = A("lather_slide", 30)
a.r("body", (5, -14, 0, 0), (8, -70, 0, 0), (10, -80, 0, 0), (16, -80, 0, 0), (18, -76, 0, 0), (22, -30, 0, 0), (26, 4, 0, 0))
a.p("body", (5, 0, -0.4, 0.6), (8, 0, -2.6, -1.0), (10, 0, -3.6, -2.0), (16, 0, -3.6, -2.0), (18, 0, -3.4, -1.6), (22, 0, -1.2, -0.6), (26, 0, 0.3, 0))
a.r("head", (5, 6, 0, 0), (8, 40, 0, 0), (12, 46, 0, 6), (16, 46, 0, -6), (20, 20, 0, 0), (26, -4, 0, 0))
sym(a, "arm_r", [(5, -30, 0, 20), (8, -160, 0, 20), (16, -164, 0, 14), (18, -120, 0, 20), (22, -40, 0, 20), (26, 0, 0, 4)])
legs(a, [(5, 10, 0, 0), (8, -20, 0, 0), (16, -24, 0, 0), (20, 10, 0, 0), (26, 0, 0, 0)],
     sr=[(8, -30, 0, 0), (11, -10, 0, 0), (14, -30, 0, 0), (17, -10, 0, 0), (22, 0, 0, 0)])
a.scl("surf", (0, *HIDE), (7.5, *HIDE), (8, 0.6, 0.4, 0.6), (10, 1.2, 0.6, 1.4), (18, 1.2, 0.6, 1.4), (21, 0.4, 0.2, 0.4), (21.5, *HIDE), (30, *HIDE))
a.pos("surf", (0, 0, 0, 2), (10, 0, 0, 2), (18, 0, 0, 2), (30, 0, 0, 2))
a.hair([(0, 0, 0, 0), (6, 4, 0, 0), (9, 24, 0, 0), (12, 28, 0, 6), (16, 28, 0, -6), (20, 6, 0, 0), (26, -4, 0, 0)], delay=2)
a.foam(2.0, speed=2).bubs(1.6)
a.done()

# ------------------------------------------------------------------ duck_toss (30): reach up, grab duck t6, wind back 8-13, THROW t16 (duck leaves), new duck pops onto head t26
a = A("duck_toss", 30)
a.r("arm_r", (4, -140, 0, 20), (6, -170, 0, 14), (9, -160, -20, 30), (13, -150, -10, 40), (15, -60, 0, 20), (16, -30, 0, 10), (19, 30, 0, 10), (24, 10, 0, 4))
a.r("fore_r", (6, 20, 0, 0), (13, 60, 0, 0), (16, 0, 0, 0), (20, 10, 0, 0))
a.r("arm_l", (8, -30, 0, -20), (13, -50, 0, -30), (16, 30, 0, -10), (22, 0, 0, -4))
a.r("chest", (6, 8, 0, 0), (9, 14, -14, 0), (13, 18, -28, -4), (16, -16, 22, 4), (19, -14, 16, 0), (24, 0, 0, 0))
a.r("head", (4, 20, 0, 0), (6, 26, 0, 0), (10, 6, 10, 0), (13, 4, 20, 0), (16, -10, -14, 0), (20, -6, -8, 0), (26, 10, 0, 0), (28, 0, 0, 0))
a.p("body", (9, 0, 0.2, 0.6), (13, 0, 0, 1.0), (16, 0, -0.2, -0.8), (22, 0, 0, 0))
legs(a, [(9, -8, 0, 0), (13, -14, 0, 0), (16, 10, 0, 0), (22, 0, 0, 0)])
# duck rides in the right sleeve: lift off head, follow the hand, gone at release, new one pops back
a.pos("duck", (0, 0, 0, 0), (6, 0, 0, 0), (9, 1.6, 0.4, 2.0), (13, 2.2, -0.6, 4.2), (15.5, 2.0, -2.0, 0), (16, 2.0, -2.0, -2.0), (25, 0, 0, 0), (30, 0, 0, 0))
a.scl("duck", (0, 1, 1, 1), (15.5, 1, 1, 1), (16, *HIDE), (25, *HIDE), (25.5, 0.4, 0.4, 0.4), (26.5, 1.3, 1.3, 1.3), (28, 1, 1, 1), (30, 1, 1, 1))
a.r("duck", (6, 0, 0, 0), (10, 30, 0, -20), (13, 50, 0, -30), (16, 0, 0, 0), (26, -10, 0, 10), (28, 0, 0, 0))
a.hair([(0, 0, 0, 0), (6, 6, 0, 0), (13, 8, 0, 10), (16, -8, 0, -10), (20, 0, 0, -4), (26, 8, 0, 0), (30, 0, 0, 0)], delay=2)
a.foam(1.2).bubs(1.2)
a.done()

# ------------------------------------------------------------------ swirl_gaze (34): head tilts, pink eye spins up 0-12, hypnotic STARE beam t14-24 with swaying body, blink recover
a = A("swirl_gaze", 34)
a.r("head", (4, 4, 0, -16), (8, 8, 0, -24), (12, -2, 0, -10), (14, -8, 0, 0), (17, -8, 0, 8), (20, -8, 0, -8), (23, -8, 0, 6), (24, -8, 0, 0), (28, 6, 0, 10), (31, 0, 0, 0))
a.s("head", (12, 1.0, 1.0, 1.0), (13, 1.12, 1.12, 1.12), (14, 1.06, 1.06, 1.06), (24, 1.06, 1.06, 1.06), (26, 0.96, 1.0, 0.96), (28, 1, 1, 1))
a.r("chest", (8, 6, 0, -6), (14, -10, 0, 0), (17, -10, 0, 6), (20, -10, 0, -6), (23, -10, 0, 6), (26, 0, 0, 0))
a.r("body", (14, 0, 0, 0), (17, 0, 0, 5), (20, 0, 0, -5), (23, 0, 0, 5), (26, 0, 0, 0))
sym(a, "arm_r", [(6, 0, 0, 30), (12, -20, 0, 70), (14, -30, 0, 80), (24, -30, 0, 84), (28, 0, 0, 20)])
sym(a, "fore_r", [(12, 30, 0, 0), (14, 20, 0, 0), (17, 40, 0, 0), (20, 20, 0, 0), (23, 40, 0, 0), (28, 6, 0, 0)])
a.r("bubbles", (14, 0, 90, 0), (24, 0, 450, 0), (34, 0, 540, 0))
a.s("bubbles", (12, 1.3, 1.3, 1.3), (24, 1.3, 1.3, 1.3), (28, 1, 1, 1))
a.hair([(0, 0, 0, 0), (8, 2, 0, -10), (14, -6, 0, 0), (17, -6, 0, 8), (20, -6, 0, -8), (23, -6, 0, 6), (28, 2, 0, 0), (34, 0, 0, 0)], delay=2)
a.foam(1.0).bubs(1.0)
a.done()

# ------------------------------------------------------------------ bubble_shield (40): curls up 0-8, shell blooms t8, bobs inside 8-30, BURST t32 (arms fling), recover
a = A("bubble_shield", 40)
a.scl("shell", (0, *HIDE), (7.5, *HIDE), (8, 0.3, 0.3, 0.3), (10, 1.15, 1.15, 1.15), (12, 0.95, 0.95, 0.95), (14, 1, 1, 1), (20, 1.04, 0.97, 1.04), (26, 0.97, 1.04, 0.97),
      (30, 1.08, 1.08, 1.08), (31, 1.25, 1.25, 1.25), (32, 1.45, 1.45, 1.45), (32.5, *HIDE), (40, *HIDE))
a.p("body", (4, 0, -1.2, 0), (8, 0, -1.4, 0), (14, 0, 0.6, 0), (20, 0, 1.0, 0), (26, 0, 0.6, 0), (30, 0, 0.2, 0), (32, 0, 0.8, 0), (36, 0, 0, 0))
a.r("chest", (4, -20, 0, 0), (8, -26, 0, 0), (20, -22, 0, 4), (26, -22, 0, -4), (30, -26, 0, 0), (32, 14, 0, 0), (36, 4, 0, 0))
a.r("head", (4, -16, 0, 0), (8, -20, 0, 0), (20, -16, 0, 8), (26, -16, 0, -8), (30, -20, 0, 0), (32, 20, 0, 0), (36, 0, 0, 0))
sym(a, "arm_r", [(4, -60, -30, -10), (8, -80, -40, -20), (30, -80, -40, -20), (31, -40, 0, 40), (32, -20, 0, 100), (34, -10, 0, 90), (38, 0, 0, 20)])
sym(a, "fore_r", [(8, 60, 0, 0), (30, 60, 0, 0), (32, 0, 0, 0)])
legs(a, [(4, 40, 0, 0), (8, 60, 0, 0), (30, 60, 0, 0), (32, -10, 0, 0), (36, 0, 0, 0)], sr=[(4, -60, 0, 0), (8, -90, 0, 0), (30, -90, 0, 0), (32, 0, 0, 0)])
a.s("foam", (8, 0.8, 0.7, 0.8), (30, 0.8, 0.7, 0.8), (32, 1.4, 1.2, 1.4), (35, 1, 1, 1))
a.hair([(0, 0, 0, 0), (6, -6, 0, 0), (14, 4, 0, 4), (20, 6, 0, -4), (26, 4, 0, 4), (30, -4, 0, 0), (32, 20, 0, 0), (36, 0, 0, 0)], delay=2)
a.bubs(1.0)
a.done()

# ------------------------------------------------------------------ pop_storm (44, enraged): bubbles swell + spin 0-12, three spin-pops t16 / t24 / t32, dizzy wobble recover
a = A("pop_storm", 44)
a.r("body", (6, 0, -30, 0), (12, 0, -60, 0), (16, 0, 120, 0), (20, 0, 240, 0), (24, 0, 360, 0), (28, 0, 480, 0), (32, 0, 600, 0), (36, 0, 690, 0), (40, 0, 720, 0), (44, 0, 720, 0))
a.p("body", (6, 0, -0.6, 0), (12, 0, -1.0, 0), (16, 0, 1.2, 0), (20, 0, 0.4, 0), (24, 0, 1.4, 0), (28, 0, 0.4, 0), (32, 0, 1.6, 0), (36, 0, 0, 0))
sym(a, "arm_r", [(6, -20, 0, 30), (12, -10, 0, 40), (16, 0, 0, 95), (24, 0, 0, 100), (32, 0, 0, 105), (36, 10, 0, 40), (40, 0, 0, 20), (44, 0, 0, 0)])
sym(a, "fore_r", [(12, 40, 0, 0), (16, 0, 0, 0), (32, 0, 0, 0), (38, 20, 0, 0)])
a.r("chest", (12, -14, 0, 0), (16, 6, 0, 0), (32, 6, 0, 0), (36, 0, 0, 10), (39, 0, 0, -10), (42, 0, 0, 4))
a.r("head", (12, -10, 0, 0), (16, 10, 0, 0), (32, 10, 0, 0), (36, 0, 0, 16), (39, 4, 0, -16), (42, 0, 0, 6))
a.scl("bubbles", (0, 1, 1, 1), (6, 1.4, 1.4, 1.4), (12, 1.8, 1.8, 1.8), (15, 2.2, 2.2, 2.2), (16, 0.3, 0.3, 0.3), (20, 1.8, 1.8, 1.8), (23, 2.2, 2.2, 2.2), (24, 0.3, 0.3, 0.3),
      (28, 2.0, 2.0, 2.0), (31, 2.6, 2.6, 2.6), (32, 0.2, 0.2, 0.2), (40, 1, 1, 1), (44, 1, 1, 1))
a.r("bubbles", (12, 0, -200, 0), (32, 0, -900, 0), (44, 0, -1080, 0))
legs(a, [(6, 10, 0, 6), (16, -6, 0, 12), (32, -6, 0, 12), (36, 0, 0, 0)])
a.hair([(0, 0, 0, 0), (8, 6, 0, 8), (16, 16, 0, -20), (24, 16, 0, -20), (32, 18, 0, -22), (36, 0, 0, 14), (39, 4, 0, -12), (44, 0, 0, 0)], delay=2)
a.foam(2.4, speed=2)
a.done()

# ------------------------------------------------------------------ geyser_burst (40, enraged): crouch 0-8, HOP t10 (warning foam under target), squats + both sleeves heave UP t22 = geysers, recover
a = A("geyser_burst", 40)
a.p("body", (6, 0, -1.6, 0), (8, 0, -1.8, 0), (10, 0, 3.0, 0), (12, 0, 3.4, 0), (14, 0, 0, 0), (16, 0, -1.4, 0), (20, 0, -1.8, 0), (22, 0, 1.2, 0), (25, 0, 0.6, 0), (30, 0, 0, 0))
a.r("chest", (6, -20, 0, 0), (10, 10, 0, 0), (14, -24, 0, 0), (20, -30, 0, 0), (22, 16, 0, 0), (26, 10, 0, 0), (32, 0, 0, 0))
a.r("head", (6, 10, 0, 0), (10, -10, 0, 0), (14, 14, 0, 0), (20, 20, 0, 0), (22, 26, 0, 0), (28, 10, 0, 0))
sym(a, "arm_r", [(6, 30, 0, 30), (8, 40, 0, 30), (10, -60, 0, 60), (14, 40, 0, 40), (20, 50, 0, 30), (22, -170, 0, 20), (26, -160, 0, 24), (32, -20, 0, 10)])
sym(a, "fore_r", [(8, 30, 0, 0), (14, 30, 0, 0), (20, 40, 0, 0), (22, 0, 0, 0), (30, 10, 0, 0)])
legs(a, [(6, 40, 0, 0), (8, 50, 0, 0), (10, -10, 0, 0), (14, 30, 0, 0), (20, 50, 0, 0), (22, 0, 0, 0), (30, 0, 0, 0)],
     sr=[(6, -60, 0, 0), (8, -80, 0, 0), (10, -10, 0, 0), (14, -50, 0, 0), (20, -80, 0, 0), (22, 0, 0, 0)])
a.scl("foam", (0, 1, 1, 1), (14, 1.3, 0.8, 1.3), (20, 1.4, 1.2, 1.4), (22, 1.2, 2.0, 1.2), (26, 1.1, 1.3, 1.1), (32, 1, 1, 1), (40, 1, 1, 1))
a.scl("surf", (0, *HIDE), (21.5, *HIDE), (22, 0.6, 1.8, 0.6), (24, 1.0, 2.6, 1.0), (28, 1.2, 1.4, 1.2), (31, 0.6, 0.4, 0.6), (31.5, *HIDE), (40, *HIDE))
a.pos("surf", (0, 0, 0, 0.6), (40, 0, 0, 0.6))
a.hair([(0, 0, 0, 0), (8, 6, 0, 0), (10, -16, 0, 0), (14, 14, 0, 0), (20, 6, 0, 0), (22, -20, 0, 0), (26, -8, 0, 0), (32, 0, 0, 0)], delay=2)
a.bubs(2.0)
a.done()

# ------------------------------------------------------------------ death (40): wobble, bubbles pop, deflates into the foam, duck tumbles off, foam spreads
a = A("death", 40)
a.r("chest", (4, 10, 0, 8), (8, 4, 0, -10), (14, -20, 0, 0), (22, -50, 0, 6), (40, -54, 0, 6))
a.r("head", (4, 16, 0, 14), (8, 10, 0, -18), (14, -10, 0, 10), (22, -30, 0, 26), (40, -30, 0, 28))
a.p("body", (4, 0, 0.4, 0), (8, 0, 0.2, 0), (14, 0, -1.6, 0), (22, 0, -2.2, 0.6), (40, 0, -2.4, 0.6))
a.r("body", (8, 0, 0, 0), (14, -10, 0, 0), (22, -30, 0, 0), (40, -34, 0, 0))
sym(a, "arm_r", [(4, -30, 0, 50), (8, -20, 0, 60), (14, 10, 0, 30), (22, -40, 0, 70), (40, -44, 0, 76)])
sym(a, "fore_r", [(8, 20, 0, 0), (22, 0, 0, 0), (40, 0, 0, 0)])
legs(a, [(8, 0, 0, 0), (14, 40, 0, 0), (22, 80, 0, 0), (40, 84, 0, 0)], sr=[(14, -60, 0, 0), (22, -90, 0, 0), (40, -90, 0, 0)])
a.scl("bubbles", (0, 1, 1, 1), (3, 1.4, 1.4, 1.4), (4, *HIDE), (40, *HIDE))
a.pos("duck", (0, 0, 0, 0), (8, 0, 0, 0), (12, 2.0, 3.0, -1.0), (16, 4.0, 0.0, -2.0), (19, 5.0, -10.0, -2.4), (40, 5.0, -10.0, -2.4))
a.rot("duck", (0, 0, 0, 0), (8, 0, 0, 0), (12, 40, 0, 90), (16, 90, 0, 180), (19, 90, 0, 200), (40, 90, 0, 200))
a.scl("foam", (0, 1, 1, 1), (14, 1.2, 1.0, 1.2), (22, 1.5, 1.4, 1.5), (40, 1.6, 1.3, 1.6))
a.scl("head", (0, 1, 1, 1), (22, 1, 1, 1), (30, 1.04, 0.96, 1.04), (40, 1.04, 0.96, 1.04))
a.hair([(0, 0, 0, 0), (4, 10, 0, 10), (8, 6, 0, -14), (14, -10, 0, 0), (22, 20, 0, 10), (40, 18, 0, 10)], delay=2)
a.done()

m.save(OUT)
print("cubes", len(m.cubes), "anims", [x["name"] for x in m.anims])
