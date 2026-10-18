"""Aiden (delta-iden) - generates assets/fpe/bbmodels/aiden.bbmodel.
Reference (only trusted one): docs/ref/confirmed/aiden.jpg - small silent boy in a dark workshop in front of a wall of
knives / axes / saws / pliers: big round paper head, pale skin, huge tired eyes with dark bags, scarred & blood-smeared face,
long straight BLACK hair (bangs + long side strands falling past the shoulders), shaggy light-grey FUR USHANKA with a dark
triangle (delta) mark on the folded front flap and hanging ear flaps, dark navy parka with fur collar, blood stains.
He fights with the tool wall: axe, sledgehammer, hand saw, knives, crowbar, pliers, drill, nail gun, bear trap.
Hitbox 0.6 x 1.7 blocks -> ~27 px; hat top ~28.7 px.
Blockbench space: Y up, ground 0, faces -Z, character's RIGHT = +X.
Signs (file values): limb rx>0 swings forward, torso/head rx>0 leans back / looks up, ry>0 turns to the character's left,
hanging part rz>0 swings toward +X. Tools are held along the forearm axis (pointing -Y out of the fist at rest),
edges / teeth on the +Z side so they lead on forward-down swings.
Run: python3 tools/bbgen/chars/aiden.py
"""
import math, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))
from bbgen import mix  # noqa: E402
from alice import Builder, A, HIDE  # noqa: E402

DIR = os.path.join(os.path.dirname(__file__), "../../../src/main/resources/assets/fpe/bbmodels/")

FUR, FUR_D, FUR_HI, FUR_SH = 0xD6D3CE, 0xA3A0A2, 0xF3F1EC, 0x77747C
HAIR, HAIR_HI, HAIR_D = 0x17161C, 0x36343F, 0x09090C
SKIN, SKIN_D, SKIN_SH, SKIN_L = 0xEDE6E3, 0xCBBFC1, 0xA2949C, 0xF8F4F2
BAG = 0x8E7E8C
COAT, COAT_D, COAT_HI = 0x2C3142, 0x1B1E29, 0x41475C
PANTS, PANTS_D = 0x24252D, 0x17171D
BOOT, BOOT_D = 0x3A2C25, 0x1C1512
BLOOD, BLOOD_D, BLOOD_HI = 0x7C1118, 0x48080D, 0xA6202A
METAL, METAL_D, METAL_HI = 0xB4BAC3, 0x666B76, 0xEEF1F5
DARKM = 0x3B3E46
WOOD, WOOD_D, WOOD_HI = 0x6E4527, 0x46291A, 0x8E6038
RED, RED_D = 0xA3232A, 0x661318
YEL, YEL_D = 0xD9A92C, 0x8C6A16
TAPE, TAPE_D = 0xE0D6BE, 0xAFA48C
LEATHER, LEATHER_D = 0x4B3424, 0x2E1F15
INK = 0x1E1A20


# ================================================================== painters
def splat(F, R, x, y, r, drip=True):
    F.disc(x, y, r, BLOOD)
    F.disc(x - r * 0.3, y - r * 0.3, r * 0.45, BLOOD_HI)
    for _ in range(3):
        F.disc(x + R.uniform(-2.2, 2.2) * r, y + R.uniform(-2.2, 2.2) * r, max(0.6, r * 0.3), BLOOD_D)
    if drip:
        for _ in range(R.randint(1, 2)):
            dx = x + R.uniform(-r, r)
            F.line(dx, y, dx, y + R.uniform(2, 6) * max(1, r * 0.6), BLOOD, 1)


def fur_p(B, base=FUR, bloody=0.0):
    R = B.R

    def f(F):
        for y in range(F.h):
            for x in range(F.w):
                n = R.random()
                c = mix(base, FUR_HI, 0.5) if n > 0.86 else mix(base, FUR_D, 0.55) if n < 0.16 else base
                F.px(x, y, mix(c, FUR_SH, 0.25 * y / max(1, F.h - 1)))
        for _ in range(max(2, F.w * F.h // 40)):  # clumped strands
            x, y = R.uniform(0, F.w), R.uniform(0, F.h)
            F.line(x, y, x + R.uniform(-2, 2), y + R.uniform(1, 3), FUR_D, 1)
        for _ in range(max(1, F.w * F.h // 90)):  # grime / dark tufts like the art
            if R.random() < 0.25:
                x, y = R.uniform(0, F.w), R.uniform(0, F.h)
                F.line(x, y, x + R.uniform(-3, 3), y + R.uniform(-2, 2), FUR_SH, 1)
        if bloody and R.random() < bloody:
            splat(F, R, R.uniform(2, F.w - 2), R.uniform(2, F.h - 2), 1.2)
    return f


def emblem_p(B):
    furf = fur_p(B, FUR_HI)

    def f(F):
        furf(F)
        W, H = F.w, F.h
        cx, top, bot, hw = W * 0.52, H * 0.12, H * 0.86, H * 0.42
        pts = [(cx, top), (cx + hw, bot), (cx - hw, bot)]
        for i in range(3):
            (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % 3]
            F.line(x1, y1, x2, y2, INK, 2.2)
        F.line(cx - hw * 0.2, bot - 3, cx + hw * 0.5, bot - 6, FUR_SH, 1)  # scratch through the mark
    return f


def coat_p(B, blood=0.35, hem=False):
    R = B.R
    folds = B.folds(COAT, COAT_D, COAT_HI, 3)

    def f(F):
        folds(F)
        if hem:
            F.rect(0, F.h - 3, F.w, 3, COAT_D)
            for x in range(0, F.w, 3):
                F.px(x, F.h - 2, COAT_HI)
        if R.random() < blood:
            splat(F, R, R.uniform(2, max(3, F.w - 2)), R.uniform(2, max(3, F.h * 0.7)), R.uniform(1.0, 2.4))
        if R.random() < blood * 0.6:
            F.disc(R.uniform(0, F.w), R.uniform(0, F.h), 0.8, BLOOD_D)
    return f


def chest_front_p(B):
    R = B.R
    base = coat_p(B, 0)

    def f(F):
        base(F)
        W, H = F.w, F.h
        # big dried blood stain like the art (right chest down to the belly)
        F.poly([(W * 0.55, H * 0.15), (W * 0.9, H * 0.25), (W * 0.82, H * 0.7), (W * 0.6, H * 0.9), (W * 0.45, H * 0.55)], BLOOD_D)
        F.poly([(W * 0.6, H * 0.22), (W * 0.83, H * 0.3), (W * 0.76, H * 0.6), (W * 0.58, H * 0.66)], BLOOD)
        for _ in range(4):
            x = R.uniform(W * 0.5, W * 0.85)
            F.line(x, H * 0.6, x, H * 0.6 + R.uniform(3, 10), BLOOD_D, 1)
        F.disc(W * 0.3, H * 0.4, 1.3, BLOOD)
    return f


def pants_p(B):
    folds = B.folds(PANTS, PANTS_D, 0x34353F, 2)
    return folds


def boot_p(F):
    F.rect(0, 0, F.w, F.h, BOOT)
    F.rect(0, F.h - 2, F.w, 2, BOOT_D)
    F.rect(0, 0, F.w, 1, mix(BOOT, 0xFFFFFF, 0.15))


def lace_p(F):
    boot_p(F)
    for y in range(1, F.h - 2, 2):
        F.line(1, y, F.w - 2, y + 1, TAPE_D, 1)


def strands(B, base=HAIR, hi=HAIR_HI, dark=HAIR_D):
    return B.strands(base, hi, dark)


def face_p(F):
    W, H = F.w, F.h  # 64 x 61 ; top 7 px under the hat, bangs reach ~px 18
    for y in range(H):
        F.rect(0, y, W, 1, mix(SKIN_L, SKIN, y / H))
    F.rect(0, 0, W, 14, mix(SKIN, HAIR_D, 0.55))  # hat / bangs shadow
    F.rect(0, 14, W, 4, mix(SKIN, SKIN_SH, 0.4))
    for cx, side in ((0.29 * W, -1), (0.71 * W, 1)):
        ey, rx, ry = 0.47 * H, 0.15 * W, 0.15 * H
        # dark bags under the eyes
        F.poly([(cx - rx, ey + ry * 0.6), (cx + rx, ey + ry * 0.6), (cx + rx * 0.8, ey + ry * 1.5), (cx - rx * 0.8, ey + ry * 1.5)], BAG)
        F.line(cx - rx * 0.8, ey + ry * 1.25, cx + rx * 0.8, ey + ry * 1.25, mix(BAG, INK, 0.4), 1)
        # big round staring eye
        F.disc(cx, ey, rx + 1.2, INK)
        F.disc(cx, ey, rx, 0xFBFBFB)
        F.disc(cx, ey + ry * 0.55, rx * 0.95, 0xE2DEE4)  # lower-lid shade
        px = cx + side * 1.5
        F.disc(px, ey + 1, rx * 0.36, 0x2A2530)
        F.disc(px, ey + 1, rx * 0.2, 0x050507)
        F.disc(px - 1.2, ey - 0.8, 0.9, 0xFFFFFF, glow=True)
        # heavy, droopy upper lid line
        F.line(cx - rx - 1.5, ey - ry * 0.55, cx + rx + 1.5, ey - ry * 0.55 - side * 1.2, INK, 2.4)
        F.line(cx + side * (rx + 1), ey - ry * 0.4, cx + side * (rx + 3), ey - ry * 0.9, INK, 1)  # lash flick
    # nose dot + tiny flat mouth
    F.px(int(W * 0.5), int(H * 0.68), SKIN_SH)
    F.line(W * 0.44, H * 0.83, W * 0.56, H * 0.82, INK, 1.2)
    # scars: long diagonal stitched cut across the face, short one on the forehead
    F.line(W * 0.12, H * 0.62, W * 0.62, H * 0.95, mix(SKIN_SH, BLOOD, 0.4), 1.4)
    for i in range(6):
        u = 0.1 + 0.15 * i
        x, y = W * (0.12 + 0.5 * u), H * (0.62 + 0.33 * u)
        F.line(x - 1.5, y + 1.5, x + 1.5, y - 1.5, INK, 1)
    F.line(W * 0.62, H * 0.26, W * 0.85, H * 0.32, mix(SKIN_SH, BLOOD, 0.5), 1)
    # band-aid on the right cheek (viewer's left)
    F.poly([(W * 0.08, H * 0.73), (W * 0.24, H * 0.66), (W * 0.27, H * 0.74), (W * 0.11, H * 0.81)], TAPE)
    F.disc(W * 0.175, H * 0.735, 1.3, TAPE_D)
    # blood smear + drips (cheek, chin, under the nose)
    F.poly([(W * 0.66, H * 0.72), (W * 0.86, H * 0.68), (W * 0.9, H * 0.8), (W * 0.7, H * 0.86)], BLOOD)
    F.disc(W * 0.74, H * 0.76, 1.6, BLOOD_HI)
    for x, l in ((0.7, 9), (0.8, 6), (0.86, 11), (0.47, 5)):
        F.line(W * x, H * 0.82, W * x, min(H - 1, H * 0.82 + l), BLOOD, 1)
    F.disc(W * 0.35, H * 0.97, 1.8, BLOOD_D)


def skin_p(B, bloody=0.3, bandage=False):
    R = B.R

    def f(F):
        F.rect(0, 0, F.w, F.h, SKIN)
        F.rect(0, F.h - 1, F.w, 1, SKIN_D)
        if bandage:
            for y in range(1, F.h, 3):
                F.rect(0, y, F.w, 2, TAPE)
                F.rect(0, y + 1, F.w, 1, TAPE_D)
        if R.random() < bloody:
            splat(F, R, R.uniform(1, F.w - 1), R.uniform(1, F.h - 1), 1.0, drip=False)
    return f


def metal_p(B, base=METAL, blood=0.0, edge=None):
    R = B.R

    def f(F):
        for y in range(F.h):
            for x in range(F.w):
                F.px(x, y, mix(METAL_HI if base == METAL else mix(base, 0xFFFFFF, 0.3), mix(base, METAL_D, 0.6),
                               x / max(1, F.w - 1) * 0.8 + R.uniform(0, 0.15)))
        for _ in range(max(1, F.w * F.h // 60)):
            x, y = R.uniform(0, F.w), R.uniform(0, F.h)
            F.line(x, y, x + R.uniform(-3, 3), y + R.uniform(-1, 1), METAL_D, 1)
        if edge:
            F.rect(0, 0, F.w, 1, edge)
        if blood and R.random() < blood:
            splat(F, R, R.uniform(1, F.w - 1), R.uniform(1, F.h - 1), R.uniform(0.8, 1.8))
    return f


def wood_p(B, base=WOOD):
    R = B.R

    def f(F):
        for x in range(F.w):
            c = mix(base, WOOD_D, R.uniform(0, 0.4)) if x % 2 else mix(base, WOOD_HI, R.uniform(0, 0.3))
            F.rect(x, 0, 1, F.h, c)
        for _ in range(max(1, F.h // 8)):
            y = R.uniform(0, F.h)
            F.line(0, y, F.w, y + R.uniform(-1, 1), WOOD_D, 1)
    return f


def paint_p(B, base, dark):
    R = B.R

    def f(F):
        F.rect(0, 0, F.w, F.h, base)
        F.rect(0, F.h - 1, F.w, 1, dark)
        for _ in range(max(1, F.w * F.h // 30)):  # chipped paint
            F.disc(R.uniform(0, F.w), R.uniform(0, F.h), 0.7, METAL_D)
    return f


def tape_p(F):
    F.rect(0, 0, F.w, F.h, TAPE)
    for y in range(0, F.h, 3):
        F.line(0, y, F.w, y + 2, TAPE_D, 1)


def teeth_p(F):
    F.rect(0, 0, F.w, F.h, METAL_D)
    for y in range(0, F.h, 3):
        F.poly([(0, y), (F.w, y + 1.5), (0, y + 3)], METAL_HI)


def spiral_p(F):
    F.rect(0, 0, F.w, F.h, METAL)
    for y in range(-F.w, F.h, 3):
        F.line(0, y, F.w, y + F.w, METAL_D, 1)


def drill_p(B, base=YEL, dark=YEL_D):
    def f(F):
        F.rect(0, 0, F.w, F.h, base)
        F.rect(0, 0, F.w, 2, mix(base, 0xFFFFFF, 0.3))
        F.rect(0, F.h - 2, F.w, 2, dark)
        F.rect(F.w // 3, F.h // 3, max(1, F.w // 3), max(1, F.h // 3), INK)
    return f


# ================================================================== model
def build(B):
    g, c = B.g, B.c
    fur = B.all(fur_p(B))
    fur_hi = B.all(fur_p(B, FUR_HI))
    furb = B.all(fur_p(B, FUR, 0.5))
    hair = B.all(strands(B))
    hairm = B.all(strands(B, mix(HAIR, HAIR_HI, 0.25)))
    coat = B.all(coat_p(B))
    coat_hem = B.all(coat_p(B, 0.4, True))
    pants = B.all(pants_p(B))
    metal = B.all(metal_p(B))
    metal_b = B.all(metal_p(B, blood=0.7))
    dark_m = B.all(metal_p(B, DARKM, blood=0.4))
    wood = B.all(wood_p(B))
    wood_d = B.all(wood_p(B, WOOD_D))
    red = B.all(paint_p(B, RED, RED_D))
    tape = B.all(tape_p)
    yel = B.all(drill_p(B))
    orange = B.all(drill_p(B, 0xD8642A, 0x8E3A16))
    teeth = B.all(teeth_p)

    g("root", (0, 0, 0))
    # ---------------- pelvis / legs
    g("pelvis", (0, 9, 0), "root")
    c("hips", "pelvis", (-3.1, 7.8, -1.8), (3.1, 10.0, 1.8), PANTS, faces=pants)
    c("belt", "pelvis", (-3.25, 9.3, -1.95), (3.25, 10.1, 1.95), LEATHER, faces=B.all(paint_p(B, LEATHER, LEATHER_D)))
    c("buckle", "pelvis", (-0.6, 9.2, -2.1), (0.6, 10.2, -1.9), METAL, faces=metal)
    c("pouch", "pelvis", (-3.4, 7.6, -1.2), (-2.6, 9.4, 1.0), LEATHER, faces=B.all(paint_p(B, LEATHER, LEATHER_D)))
    # belt tools: wrench (left hip) and screwdriver (right hip)
    c("wrench", "pelvis", (-3.75, 5.2, -0.3), (-3.35, 9.4, 0.3), METAL, faces=metal_b, origin=(-3.5, 9.3, 0), rot=(0, 0, -12))
    c("wrenchh", "pelvis", (-3.85, 4.6, -0.8), (-3.25, 5.6, 0.8), METAL, faces=metal, origin=(-3.5, 9.3, 0), rot=(0, 0, -12))
    c("screwh", "pelvis", (3.3, 8.0, 0.4), (3.9, 9.8, 1.0), RED, faces=red)
    c("screwb", "pelvis", (3.5, 5.6, 0.6), (3.7, 8.0, 0.8), METAL, faces=metal)
    THL, SHL = 4.0, 3.6
    for s, k in ((1, "r"), (-1, "l")):
        x = 1.55 * s
        g("leg_" + k, (x, 9, 0), "pelvis")
        c("thigh_" + k, "leg_" + k, (x - 1.35, 5.0, -1.35), (x + 1.35, 9.2, 1.35), PANTS, faces=pants)
        c("knee_" + k, "leg_" + k, (x - 1.0, 5.2, -1.45), (x + 0.9, 6.4, -1.3), PANTS_D)  # knee patch
        g("shin_" + k, (x, 5, 0), "leg_" + k)
        c("calf_" + k, "shin_" + k, (x - 1.25, 2.4, -1.25), (x + 1.25, 5.1, 1.25), PANTS, faces=pants)
        c("bootc_" + k, "shin_" + k, (x - 1.42, 1.2, -1.42), (x + 1.42, 3.4, 1.42), BOOT, faces=B.all(lace_p))
        c("bootr_" + k, "shin_" + k, (x - 1.5, 3.1, -1.5), (x + 1.5, 3.6, 1.5), FUR_D, faces=fur)  # fur rim
        g("foot_" + k, (x, 1.4, 0), "shin_" + k)
        c("boot_" + k, "foot_" + k, (x - 1.4, 0.35, -2.7), (x + 1.4, 1.6, 1.4), BOOT, faces={"north": boot_p, "up": lace_p, "east": boot_p, "west": boot_p})
        c("sole_" + k, "foot_" + k, (x - 1.5, 0.0, -2.85), (x + 1.5, 0.4, 1.5), BOOT_D)

    # parka skirt (secondary motion panels)
    g("coat_f", (0, 10, -2.0), "pelvis")
    c("coatfr", "coat_f", (0.1, 5.4, -2.3), (3.2, 10.1, -1.85), COAT, faces=coat_hem)
    c("coatfl", "coat_f", (-3.2, 5.6, -2.3), (-0.1, 10.1, -1.85), COAT, faces=coat_hem)
    c("coatft", "coat_f", (-3.2, 5.3, -2.35), (3.2, 5.8, -1.8), FUR_D, faces=fur)
    g("coat_b", (0, 10, 2.0), "pelvis")
    c("coatb", "coat_b", (-3.2, 5.2, 1.85), (3.2, 10.1, 2.3), COAT, faces=coat_hem)
    c("coatbt", "coat_b", (-3.2, 4.9, 1.8), (3.2, 5.4, 2.35), FUR_D, faces=fur)
    for s, k in ((1, "r"), (-1, "l")):
        g("coat_" + k, (3.2 * s, 10, 0), "pelvis")
        x0, x1 = sorted((3.0 * s, 3.4 * s))
        c("coats_" + k, "coat_" + k, (x0, 5.5, -2.1), (x1, 10.1, 2.1), COAT, faces=coat_hem)

    # ---------------- torso
    g("body", (0, 10, 0), "pelvis")
    c("waist", "body", (-3.0, 10.0, -1.9), (3.0, 13.6, 1.9), COAT, faces=coat)
    c("chest", "body", (-3.4, 13.4, -2.1), (3.4, 17.0, 2.1), COAT, faces={**coat, "north": chest_front_p(B)})
    c("zip", "body", (-0.25, 10.0, -2.2), (0.25, 16.8, -2.0), DARKM, faces=dark_m)
    for i, y in enumerate((11.4, 13.2, 15.0)):
        c(f"toggle{i}", "body", (-0.5, y, -2.35), (0.5, y + 0.5, -2.15), FUR_HI)
    for s, k in ((1, "r"), (-1, "l")):
        x0, x1 = sorted((1.0 * s, 2.8 * s))
        c("pocket_" + k, "body", (x0, 10.5, -2.05), (x1, 12.3, -1.88), COAT_D)
        c("pocketf_" + k, "body", (x0 - 0.1, 12.0, -2.12), (x1 + 0.1, 12.5, -1.9), COAT_HI)
    # fur collar + folded hood
    c("collarf", "body", (-2.9, 16.4, -2.6), (2.9, 17.7, -1.5), FUR, faces=furb)
    for s, k in ((1, "r"), (-1, "l")):
        x0, x1 = sorted((1.9 * s, 3.3 * s))
        c("collars_" + k, "body", (x0, 16.4, -2.3), (x1, 18.0, 2.4), FUR, faces=fur, origin=(2.6 * s, 17, 0), rot=(0, 0, -10 * s))
    c("collarb", "body", (-3.1, 16.4, 1.3), (3.1, 18.3, 2.7), FUR, faces=fur)
    g("hood", (0, 17.0, 2.4), "body")
    c("hoodc", "hood", (-2.9, 13.6, 2.1), (2.9, 17.2, 3.4), COAT, faces=coat)
    c("hoodr", "hood", (-3.0, 13.2, 2.5), (3.0, 14.0, 3.7), FUR, faces=fur)
    # bandolier strap of knives (right shoulder -> left hip)
    c("strap", "body", (-0.45, 9.6, -2.45), (0.45, 18.0, -2.15), LEATHER, faces=B.all(paint_p(B, LEATHER, LEATHER_D)),
      origin=(0, 13.8, -2.3), rot=(0, 0, -38))
    for i, (x, y) in enumerate(((1.5, 15.6), (0.0, 13.8), (-1.5, 12.0))):
        c(f"sheath{i}", "body", (x - 0.35, y - 1.6, -2.75), (x + 0.35, y + 0.2, -2.4), LEATHER_D, origin=(x, y, -2.5), rot=(0, 0, -38))
        c(f"skn{i}", "body", (x - 0.25, y + 0.2, -2.7), (x + 0.25, y + 1.5, -2.45), INK, origin=(x, y, -2.5), rot=(0, 0, -38))
    c("neck", "body", (-1.0, 16.8, -1.0), (1.0, 17.9, 1.0), SKIN_D)

    # ---------------- arms
    for s, k in ((1, "r"), (-1, "l")):
        x = 4.2 * s
        g("arm_" + k, (x, 16.4, 0), "body")
        c("shoulder_" + k, "arm_" + k, (x - 1.3, 14.2, -1.4), (x + 1.3, 17.2, 1.4), COAT, faces=coat)
        c("upper_" + k, "arm_" + k, (x - 1.15, 12.4, -1.2), (x + 1.15, 14.4, 1.2), COAT, faces=coat)
        g("fore_" + k, (x, 12.6, 0), "arm_" + k)
        c("forearm_" + k, "fore_" + k, (x - 1.1, 10.4, -1.15), (x + 1.1, 12.8, 1.15), COAT, faces=coat)
        c("cuff_" + k, "fore_" + k, (x - 1.3, 9.7, -1.3), (x + 1.3, 10.7, 1.3), FUR, faces=fur)
        g("hand_" + k, (x, 10.0, 0), "fore_" + k)
        c("palm_" + k, "hand_" + k, (x - 0.85, 8.2, -0.9), (x + 0.85, 10.0, 0.9), SKIN, faces=B.all(skin_p(B, 0.6, k == "r")))
        c("fingers_" + k, "hand_" + k, (x - 0.9, 8.0, -1.15), (x + 0.9, 9.3, -0.55), SKIN_D)
        c("thumb_" + k, "hand_" + k, (x - 0.35 - 0.6 * s, 8.8, -1.0), (x + 0.35 - 0.6 * s, 9.9, -0.5), SKIN_D)

    # ---------------- head
    g("head", (0, 17.6, 0), "body")
    c("skull", "head", (-4.0, 17.6, -3.6), (4.0, 25.2, 3.4), SKIN, faces={"north": face_p, **{f: skin_p(B, 0) for f in ("east", "west", "down")}})
    c("hback", "head", (-4.35, 17.4, 0.0), (4.35, 25.0, 3.8), HAIR, faces=hair)
    for s, k in ((1, "r"), (-1, "l")):
        x0, x1 = sorted((3.95 * s, 4.45 * s))
        c("hside_" + k, "head", (x0, 17.6, -3.2), (x1, 25.0, 0.2), HAIR, faces=hair)
    g("bangs", (0, 25.0, -3.8), "head")
    for i, (x, ln, rz) in enumerate(((-3.3, 4.6, -8), (-1.7, 3.3, -4), (-0.2, 2.8, 2), (1.3, 3.2, 5), (2.8, 3.6, 8), (3.6, 4.8, 10))):
        B.lock(f"bang{i}", "bangs", (x, 25.4, -3.95), ln, 1.9, 0.8, (-6, 0, rz), HAIR if i % 2 else mix(HAIR, HAIR_HI, 0.2),
               tip=HAIR_D, paint=hair["north"])
    for s, k in ((1, "r"), (-1, "l")):  # long strands framing the face, falling past the shoulders
        g("hair_" + k, (3.5 * s, 24.6, -2.6), "head")
        B.lock("hf0_" + k, "hair_" + k, (3.55 * s, 24.6, -3.0), 11.0, 1.7, 1.2, (-4, 0, 4 * s), HAIR, tip=HAIR_D, paint=hair["north"])
        B.lock("hf1_" + k, "hair_" + k, (4.3 * s, 24.4, -1.6), 9.5, 1.5, 1.6, (2, 0, 9 * s), mix(HAIR, HAIR_HI, 0.2), tip=HAIR_D, paint=hairm["north"])
        B.lock("hf2_" + k, "hair_" + k, (3.0 * s, 23.8, -3.5), 7.0, 1.0, 0.7, (-6, 0, 2 * s), HAIR_D, tip=HAIR_D, paint=hair["north"])
    g("hair_b", (0, 24.6, 3.6), "head")
    c("hbp", "hair_b", (-4.3, 13.2, 3.3), (4.3, 24.8, 4.5), HAIR, faces=hair)
    for i, x in enumerate((-3.4, -1.2, 1.2, 3.4)):
        B.lock(f"hbl{i}", "hair_b", (x, 13.6, 3.9), 2.6 + 0.8 * (i % 2), 2.0, 1.0, (8, 0, x * 3), HAIR if i % 2 else HAIR_D, tip=HAIR_D,
               paint=hair["north"])

    # ---------------- ushanka
    g("hat", (0, 24.4, 0), "head")
    c("crown", "hat", (-4.6, 24.1, -4.2), (4.6, 27.8, 4.3), FUR, faces=furb)
    c("crowntop", "hat", (-4.0, 27.6, -3.6), (4.0, 28.7, 3.7), FUR_HI, faces=fur_hi)
    c("seam", "hat", (-0.3, 28.6, -3.4), (0.3, 28.85, 3.5), FUR_D)
    c("flapfront", "hat", (-4.95, 23.8, -5.05), (4.95, 27.5, -4.05), FUR_HI, faces={**fur_hi, "north": emblem_p(B)},
      origin=(0, 24.0, -4.5), rot=(-10, 0, 0))
    c("flapback", "hat", (-4.85, 22.4, 4.05), (4.85, 26.9, 5.0), FUR, faces=fur, origin=(0, 26.5, 4.5), rot=(8, 0, 0))
    for i, (x, y, z, rx, rz) in enumerate(((4.6, 27.6, -3.0, 0, -30), (-4.6, 27.6, -3.0, 0, 30), (4.4, 27.8, 2.6, 0, -40), (-4.4, 27.8, 2.6, 0, 40),
                                             (2.2, 28.6, -4.6, -40, 0), (-2.0, 28.4, -4.7, -35, 0), (0.6, 28.9, 3.6, 30, 0), (-2.8, 28.8, 3.3, 35, 0))):
        B.blade(f"tuft{i}", "hat", (x, y - 0.6, z), 1.6, 1.4, 1.2, (rx, 0, rz), FUR, tip=FUR_HI)
    for s, k in ((1, "r"), (-1, "l")):
        g("flap_" + k, (4.75 * s, 25.4, 0.3), "hat")
        x0, x1 = sorted((4.45 * s, 5.4 * s))
        c("flapc_" + k, "flap_" + k, (x0, 19.4, -2.6), (x1, 25.4, 2.7), FUR, faces=fur)
        c("flapt_" + k, "flap_" + k, (x0 - 0.05, 19.0, -2.2), (x1 + 0.05, 19.6, 2.3), FUR_D, faces=fur)  # rounded bottom
        c("tie_" + k, "flap_" + k, (4.9 * s - 0.12, 15.6, -0.12), (4.9 * s + 0.12, 19.2, 0.12), INK)
        c("pom_" + k, "flap_" + k, (4.9 * s - 0.45, 15.0, -0.45), (4.9 * s + 0.45, 15.9, 0.45), FUR_D, faces=fur)

    # ---------------- tools (along -Y out of the fist; edge on +Z)
    def tool_grip(k):
        return (4.2 * (1 if k == "r" else -1), 9.0, 0.0)

    def T(grp, nm, gp, a, b, col, **kw):
        gx, gy, gz = gp
        o = kw.pop("origin", None)
        c(nm, grp, (gx + a[0], gy + a[1], gz + a[2]), (gx + b[0], gy + b[1], gz + b[2]), col,
          origin=(gx + o[0], gy + o[1], gz + o[2]) if o else None, **kw)

    def axe(grp, k):
        G = tool_grip(k)
        g(grp, G, "hand_" + k)
        T(grp, grp + "_h", G, (-0.33, -8.6, -0.33), (0.33, 1.2, 0.33), WOOD, faces=wood)
        T(grp, grp + "_t", G, (-0.42, -0.9, -0.42), (0.42, 0.9, 0.42), TAPE, faces=tape)
        T(grp, grp + "_e", G, (-0.5, -9.4, -0.9), (0.5, -7.4, 0.9), DARKM, faces=dark_m)
        T(grp, grp + "_b", G, (-0.22, -10.0, 0.8), (0.22, -6.8, 3.0), METAL, faces=metal_b)
        T(grp, grp + "_x", G, (-0.14, -10.4, 2.95), (0.14, -6.4, 3.45), METAL_HI, faces=metal)
        T(grp, grp + "_p", G, (-0.4, -9.0, -1.7), (0.4, -7.8, -0.8), DARKM, faces=dark_m)

    axe("axe", "r")
    axe("axe2", "l")
    # sledgehammer
    G = tool_grip("r")
    g("hammer", G, "hand_r")
    T("hammer", "hm_h", G, (-0.35, -9.6, -0.35), (0.35, 1.2, 0.35), WOOD_D, faces=wood_d)
    T("hammer", "hm_t", G, (-0.45, -1.0, -0.45), (0.45, 1.0, 0.45), TAPE, faces=tape)
    T("hammer", "hm_k", G, (-1.05, -11.4, -2.4), (1.05, -9.2, 2.4), DARKM, faces=dark_m)
    T("hammer", "hm_c", G, (-0.75, -9.4, -0.75), (0.75, -8.9, 0.75), METAL, faces=metal)
    for z0, z1 in ((2.35, 2.75), (-2.75, -2.35)):
        T("hammer", f"hm_f{int(z0 > 0)}", G, (-0.9, -11.25, z0), (0.9, -9.35, z1), METAL, faces=metal_b)
    # hand saw
    g("saw", G, "hand_r")
    T("saw", "sw_h", G, (-0.5, -1.3, -0.9), (0.5, 1.4, 1.7), WOOD, faces=wood)
    T("saw", "sw_o", G, (-0.52, -0.4, 0.2), (0.52, 0.8, 1.0), WOOD_D)
    T("saw", "sw_b", G, (-0.1, -8.8, -0.5), (0.1, -1.1, 2.7), METAL, faces=metal_b)
    T("saw", "sw_c", G, (-0.1, -11.2, -0.5), (0.1, -8.6, 1.7), METAL, faces=metal)
    T("saw", "sw_t", G, (-0.13, -11.0, 2.55), (0.13, -1.2, 2.95), METAL_D, faces=teeth)
    T("saw", "sw_tc", G, (-0.13, -11.2, 1.55), (0.13, -8.6, 1.9), METAL_D, faces=teeth)
    # knives (one per hand)
    for nm, k in (("knife_r", "r"), ("knife_l", "l")):
        Gk = tool_grip(k)
        g(nm, Gk, "hand_" + k)
        T(nm, nm + "h", Gk, (-0.32, -0.8, -0.38), (0.32, 1.3, 0.38), INK)
        T(nm, nm + "g", Gk, (-0.45, -1.15, -0.6), (0.45, -0.8, 0.6), METAL_D)
        T(nm, nm + "b", Gk, (-0.1, -5.0, -0.45), (0.1, -1.1, 0.6), METAL, faces=metal_b)
        T(nm, nm + "t", Gk, (-0.08, -6.0, -0.45), (0.08, -4.8, 0.2), METAL_HI, origin=(0, -5.0, 0.1), rot=(-14, 0, 0))
    # crowbar
    g("crowbar", G, "hand_r")
    T("crowbar", "cb_r", G, (-0.3, -9.0, -0.3), (0.3, 1.8, 0.3), RED, faces=red)
    T("crowbar", "cb_n", G, (-0.3, -9.7, -0.3), (0.3, -8.8, 1.8), RED, faces=red)
    T("crowbar", "cb_c", G, (-0.3, -9.6, 1.5), (0.3, -7.8, 2.1), METAL, faces=metal_b, origin=(0, -9.0, 1.8), rot=(-20, 0, 0))
    T("crowbar", "cb_s", G, (-0.25, 1.7, -0.7), (0.25, 2.3, 0.3), METAL, faces=metal, origin=(0, 2.0, 0), rot=(30, 0, 0))
    # pliers (two jaws open/close)
    g("pliers", G, "hand_r")
    T("pliers", "pl_h0", G, (-0.32, -1.4, -0.75), (0.32, 2.4, -0.1), RED, faces=red)
    T("pliers", "pl_h1", G, (-0.32, -1.4, 0.1), (0.32, 2.4, 0.75), RED, faces=red)
    T("pliers", "pl_rv", G, (-0.45, -1.9, -0.45), (0.45, -1.2, 0.45), METAL_HI)
    for nm, z0, z1, ofs in (("pjaw_a", -0.7, -0.05, -0.2), ("pjaw_b", 0.05, 0.7, 0.2)):
        g(nm, (G[0], G[1] - 1.5, G[2]), "pliers")
        T(nm, nm + "c", G, (-0.25, -6.4, z0), (0.25, -1.5, z1), METAL, faces=metal_b)
        T(nm, nm + "t", G, (-0.22, -6.9, z0 + ofs * 0.5), (0.22, -6.2, z1 + ofs * 0.5), DARKM)
    # drill (body in front of the fist)
    g("drill", G, "hand_r")
    T("drill", "dr_g", G, (-0.6, -1.0, -0.7), (0.6, 1.2, 0.7), INK)
    T("drill", "dr_bat", G, (-0.9, 1.0, -1.3), (0.9, 2.1, 1.2), YEL, faces=yel)
    T("drill", "dr_b", G, (-0.9, -4.4, -3.0), (0.9, 0.9, -0.9), YEL, faces=yel)
    T("drill", "dr_m", G, (-0.95, 0.4, -3.05), (0.95, 1.2, -0.85), INK)
    T("drill", "dr_ch", G, (-0.6, -5.4, -2.5), (0.6, -4.3, -1.4), METAL, faces=metal)
    g("bit", (G[0], G[1] - 5.4, G[2] - 1.95), "drill")
    T("bit", "dr_bit", G, (-0.22, -9.4, -2.17), (0.22, -5.3, -1.73), METAL, faces=B.all(spiral_p))
    T("bit", "dr_tip", G, (-0.12, -10.0, -2.07), (0.12, -9.3, -1.83), METAL_HI)
    # nail gun
    g("nailgun", G, "hand_r")
    T("nailgun", "ng_g", G, (-0.55, -1.0, -0.65), (0.55, 1.4, 0.65), INK)
    T("nailgun", "ng_b", G, (-0.85, -4.8, -2.8), (0.85, 1.1, -0.9), 0xD8642A, faces=orange)
    T("nailgun", "ng_mag", G, (-0.4, -4.4, -0.9), (0.4, -1.2, 0.6), DARKM, faces=dark_m)
    T("nailgun", "ng_mz", G, (-0.45, -5.8, -2.3), (0.45, -4.7, -1.4), METAL, faces=metal)
    T("nailgun", "ng_hose", G, (-0.2, 1.3, -0.2), (0.2, 3.6, 0.2), INK, origin=(0, 1.3, 0), rot=(30, 0, 0))
    # bear trap (two jaws, chain)
    g("trap", G, "hand_r")
    T("trap", "tp_base", G, (-0.5, -2.2, -3.6), (0.5, -1.6, -0.4), DARKM, faces=dark_m)
    T("trap", "tp_sp", G, (-2.4, -2.1, -2.4), (2.4, -1.7, -1.6), DARKM, faces=dark_m)
    for nm, sgn in (("tjaw_a", 1), ("tjaw_b", -1)):
        g(nm, (G[0], G[1] - 1.9, G[2] - 2.0), "trap")
        xo = 2.2 * sgn
        a0, a1 = sorted((xo - 0.25 * sgn, xo + 0.25 * sgn))
        T(nm, nm + "s", G, (a0, -2.1, -4.2), (a1, -1.7, 0.2), METAL, faces=metal_b)
        T(nm, nm + "f", G, (-2.2 if sgn > 0 else -2.2, -2.1, -4.25 if sgn > 0 else 0.0), (2.2, -1.7, -3.9 if sgn > 0 else 0.25), METAL, faces=metal)
        for i in range(4):
            zt = (-3.9 if sgn > 0 else -0.05) + 0.0
            xt = -1.5 + i
            T(nm, f"{nm}t{i}", G, (xt - 0.15, -1.75, zt - 0.2), (xt + 0.15, -0.9, zt + 0.2), METAL_HI)
    for i in range(3):
        T("trap", f"tp_ch{i}", G, (-0.2, -2.9 - 0.8 * i, -2.2), (0.2, -2.0 - 0.8 * i, -1.8), METAL_D)


# ================================================================== animation
def m3(v):
    return (v[0], -v[1], -v[2])


THIGH, SHIN = 4.0, 3.6
PROPS = ("axe", "axe2", "hammer", "saw", "knife_r", "knife_l", "crowbar", "pliers", "drill", "nailgun", "trap")


def drop(a, k):
    return THIGH + SHIN - THIGH * math.cos(math.radians(a)) - SHIN * math.cos(math.radians(a - k))


CARRY_R = ((22, 0, 10), (100, 0, 0), (36, 0, 0))   # axe resting on the shoulder
REST = {"body": (0, 0, 0), "head": (0, 0, 0),
        "arm_r": CARRY_R[0], "fore_r": CARRY_R[1], "hand_r": CARRY_R[2],
        "arm_l": (2, 0, -6), "fore_l": (10, 0, 0), "hand_l": (0, 0, 0),
        "leg_r": (0, 0, 1), "leg_l": (0, 0, -1), "shin_r": (0, 0, 0), "shin_l": (0, 0, 0), "foot_r": (0, 0, 0), "foot_l": (0, 0, 0)}


class F(A):
    def legs(self, t, a=0, k=0, al=None, kl=None, up=0.0, fwd=0.0, spread=0.0, setpos=True):
        al = a if al is None else al
        kl = k if kl is None else kl
        d = min(drop(a, k), drop(al, kl))
        self.at(t, leg_r=(a, 0, 1 + spread), shin_r=(-k, 0, 0), foot_r=(k - a, 0, 0),
                leg_l=(al, 0, -1 - spread), shin_l=(-kl, 0, 0), foot_l=(kl - al, 0, 0))
        if setpos: self.pos("pelvis", (t, 0, -d + up, fwd))
        return self

    def arm(self, t, k, a, f=None, h=None):
        mm = (lambda v: v) if k == "r" else m3
        self.rot("arm_" + k, (t, *mm(a)))
        if f is not None: self.rot("fore_" + k, (t, *mm(f if isinstance(f, tuple) else (f, 0, 0))))
        if h is not None: self.rot("hand_" + k, (t, *mm(h if isinstance(h, tuple) else (h, 0, 0))))
        return self

    def arms(self, t, a, f=None, h=None, al=None, fl=None, hl=None):
        self.arm(t, "r", a, f, h)
        return self.arm(t, "l", al if al is not None else a, fl if fl is not None else f, hl if hl is not None else h)

    def carry(self, t):
        return self.arm(t, "r", *CARRY_R)

    def sec(self, keys, delay=2):
        """hair / flaps / parka lag: (t, x, z) x>0 = lurch forward (things fly back), z>0 = sway toward +X"""
        self.drape("hair_b", [(t, -x * 0.7, 0, z * 0.5) for (t, x, z) in keys], delay)
        self.drape("hair_r", [(t, -x * 0.5, 0, z * 0.6 + abs(x) * 0.25) for (t, x, z) in keys], delay)
        self.drape("hair_l", [(t, -x * 0.5, 0, z * 0.6 - abs(x) * 0.25) for (t, x, z) in keys], delay)
        self.drape("bangs", [(t, -x * 0.25, 0, z * 0.3) for (t, x, z) in keys], delay)
        self.drape("flap_r", [(t, -x * 0.6, 0, z * 0.7 + abs(x) * 0.5) for (t, x, z) in keys], delay + 1)
        self.drape("flap_l", [(t, -x * 0.6, 0, z * 0.7 - abs(x) * 0.5) for (t, x, z) in keys], delay + 1)
        self.drape("coat_f", [(t, -x * 0.5, 0, 0) for (t, x, z) in keys], delay)
        self.drape("coat_b", [(t, -x * 0.6, 0, 0) for (t, x, z) in keys], delay + 1)
        self.drape("coat_r", [(t, 0, 0, z * 0.5 + abs(x) * 0.3) for (t, x, z) in keys], delay)
        self.drape("coat_l", [(t, 0, 0, z * 0.5 - abs(x) * 0.3) for (t, x, z) in keys], delay)
        self.drape("hood", [(t, -x * 0.4, 0, z * 0.3) for (t, x, z) in keys], delay + 1)
        return self

    def tilt(self, t, v):  # creepy head tilt helper
        return self.rot("head", (t, *v))


def anims(B):
    def mk(name, ticks, loop=False):
        return F(B, name, ticks, REST, PROPS, loop)

    # ================= idle (60): stands too still, axe on the shoulder, slow breath, slow unsettling head tilt + twitch
    a = mk("idle", 60, loop=True)
    for t, j in ((0, 0), (15, 1), (30, 0), (45, -1), (60, 0)):
        b = abs(j)
        a.at(t, body=(1.5 * b, 0, 1 * j))
        a.arm(t, "r", (22 + 2 * b, 0, 10), (100 - 3 * b, 0, 0), (36, 0, 0))
        a.arm(t, "l", (2 + 2 * b, 0, -6 - b), (10 + 4 * b, 0, 0), (0, 0, 0))
        a.at(t, leg_r=(0, 0, 1), leg_l=(0, 0, -1), shin_r=(0, 0, 0), shin_l=(0, 0, 0), foot_r=(0, 0, 0), foot_l=(0, 0, 0))
    a.pos("pelvis", (0, 0, 0, 0), (15, 0, -0.15, 0), (30, 0, 0, 0), (45, 0, -0.15, 0), (60, 0, 0, 0))
    a.rot("head", (0, 0, 0, 0), (18, -3, 4, 10), (30, -4, 6, 14), (36, -4, 6, 15), (37, 2, -4, -6), (40, 0, -2, -4), (50, -2, 0, -2), (60, 0, 0, 0))
    a.rot("fore_l", (0, 10, 0, 0), (38, 14, 0, 0), (39, 26, 0, 0), (42, 12, 0, 0), (60, 10, 0, 0))  # finger-twitch of the free hand
    a.sec([(0, 0, 1), (15, 1, -1), (30, 0, 1), (37, -2, -3), (45, 1, -1), (60, 0, 1)], delay=4)
    for p in PROPS:
        a.scl(p, (0, *((1, 1, 1) if p == "axe" else HIDE)))
    a.done(base_layer=True)

    # ================= walk (24, additive over idle): small stiff steps, free arm swings, hair/flaps bounce
    a = mk("walk", 24, loop=True)
    for t, sw in ((0, 1), (6, 0), (12, -1), (18, 0), (24, 1)):
        a.at(t, leg_r=(28 * sw, 0, 0), leg_l=(-28 * sw, 0, 0),
             shin_r=(-36 if (sw == 0 and t == 18) else -8 * max(0, -sw), 0, 0),
             shin_l=(-36 if (sw == 0 and t == 6) else -8 * max(0, sw), 0, 0),
             foot_r=(10 if (sw == 0 and t == 18) else -6 * sw, 0, 0), foot_l=(10 if (sw == 0 and t == 6) else 6 * sw, 0, 0))
        a.arm(t, "l", (-26 * sw, 0, 0), (6 + 6 * max(0, -sw), 0, 0))
        a.arm(t, "r", (5 * sw, 0, 0), (0, 0, 0))
    a.rot("body", (0, -4, 4, -2), (6, -5, 0, 0), (12, -4, -4, 2), (18, -5, 0, 0), (24, -4, 4, -2))
    a.rot("head", (0, 2, -4, 2), (6, 3, 0, 0), (12, 2, 4, -2), (18, 3, 0, 0), (24, 2, -4, 2))
    a.pos("pelvis", (0, 0, -0.4, 0), (6, 0, 0.3, 0), (12, 0, -0.4, 0), (18, 0, 0.3, 0), (24, 0, -0.4, 0))
    a.sec([(0, 3, 2), (6, 1, 0), (12, 3, -2), (18, 1, 0), (24, 3, 2)], delay=2)
    a.done(base_layer=True)

    # ================= axechop (36): heave overhead 0-13, SWING 15, CHOP 16 (axe bites ground), yank out 24, recover
    a = mk("axechop", 36)
    a.show("axe", 0, 36)
    a.at(4, body=(10, -14, 0), head=(4, 10, 0))
    a.arm(4, "r", (150, -10, 12), 50, 20).arm(4, "l", (70, 25, -10), 50, 0)
    a.legs(4, -8, 10, 14, 20)
    a.at(10, body=(20, -24, -4), head=(10, 16, 4))
    a.arm(10, "r", (196, -14, 10), 36, 26).arm(10, "l", (176, 28, -12), 30, 10)
    a.legs(10, -12, 14, 22, 30)
    a.at(13, body=(22, -26, -5), head=(12, 18, 6))
    a.arm(13, "r", (204, -14, 10), 40, 30).arm(13, "l", (182, 28, -12), 34, 12)
    a.at(15, body=(-14, 4, 2), head=(-4, 0, 0))
    a.arm(15, "r", (120, 0, 6), 10, 8).arm(15, "l", (110, 10, -8), 10, 4)
    a.legs(15, 26, 40, -16, 6, fwd=-0.6)
    a.at(16, body=(-40, 8, 4), head=(-16, -4, 0))
    a.arm(16, "r", (56, 4, 4), 0, 4).arm(16, "l", (62, -6, -4), 4, 0)
    a.legs(16, 44, 70, -24, 6, fwd=-1.2)
    a.at(18, body=(-44, 8, 4), head=(-20, -4, 0))
    a.arm(18, "r", (48, 4, 4), 0, 6).arm(18, "l", (54, -6, -4), 4, 0)
    a.at(21, body=(-38, 4, 2), head=(-14, 0, 6))
    a.arm(21, "r", (52, 2, 4), 6, 0).arm(21, "l", (56, -4, -4), 8, 0)
    a.at(24, body=(-18, -6, -2), head=(-4, 6, 0))
    a.arm(24, "r", (84, 0, 8), 24, -12).arm(24, "l", (40, 0, -8), 30, 0)
    a.legs(24, 30, 46, -14, 6, fwd=-0.8)
    a.at(28, body=(-4, 0, 0), head=(0, 0, 4))
    a.arm(28, "r", (40, 0, 10), 70, 26).arm(28, "l", (10, 0, -6), 16, 0)
    a.legs(28, 10, 14, -4, 2)
    a.legs(34, 0, 0)
    a.sec([(0, 0, 0), (4, -2, -2), (10, -5, -3), (13, -6, -3), (16, 10, 2), (18, 8, 0), (24, -4, 0), (28, 2, 0), (36, 0, 0)])
    a.done()

    # ================= axethrow (30): right wind 6-9, THROW 12; draw 2nd axe, left wind 16, THROW 20; catch the boomerang 27
    a = mk("axethrow", 30)
    a.scl("axe", (0, 1, 1, 1), (11.9, 1, 1, 1), (12, *HIDE), (26.9, *HIDE), (27.5, 1, 1, 1), (30, 1, 1, 1))
    a.show("axe2", 4, 20.5, grow=1)
    a.rot("axe2", (0, 0, 0, 0), (20, 0, 0, 0))
    a.arm(3, "l", (-40, 0, -24), 30, 0)
    a.at(6, body=(6, -30, -4), head=(4, 22, 0))
    a.arm(6, "r", (200, -20, 16), 30, 20).arm(6, "l", (40, 30, -20), 30, 0)
    a.legs(6, -14, 10, 20, 24)
    a.at(9, body=(10, -38, -6), head=(6, 28, 0))
    a.arm(9, "r", (216, -26, 18), 44, 30)
    a.at(12, body=(-20, 24, 4), head=(-4, -10, 0))
    a.arm(12, "r", (84, 10, 0), 0, -20)
    a.legs(12, 30, 40, -18, 6, fwd=-0.6)
    a.at(14, body=(-26, 30, 6), head=(-6, -14, 0))
    a.arm(14, "r", (40, 22, -6), 10, -10)
    a.at(16, body=(6, 28, 4), head=(4, -18, 0))
    a.arm(16, "l", (206, 22, -16), 36, 24).arm(16, "r", (30, 0, 12), 40, 0)
    a.legs(16, 20, 24, -14, 10)
    a.at(20, body=(-22, -24, -4), head=(-4, 12, 0))
    a.arm(20, "l", (84, -10, 0), 0, -20)
    a.legs(20, -18, 6, 30, 40, fwd=-0.6)
    a.at(22, body=(-26, -30, -6), head=(-6, 16, 0))
    a.arm(22, "l", (40, -22, 6), 10, -10)
    a.at(25, body=(-4, 0, 0), head=(6, 0, 0))
    a.arm(25, "r", (130, 4, 24), 30, 0).arm(25, "l", (20, 0, -10), 20, 0)
    a.legs(25, 6, 8)
    a.arm(27, "r", (110, 0, 20), 50, 10)
    a.at(27, body=(4, 0, 2))
    a.legs(30, 0, 0)
    a.sec([(0, 0, 0), (6, -2, -3), (9, -3, -4), (12, 7, 4), (14, 6, 5), (16, -2, 3), (20, 7, -4), (22, 6, -5), (27, -2, 0), (30, 0, 0)])
    a.done()

    # ================= hammer (38): drag + squat 3, heave up 7, coil 11, HOP 12-15, SLAM 17 + shockwave, lift, recover
    a = mk("hammer", 38)
    a.show("hammer", 0, 38, grow=1)
    a.at(3, body=(-16, 0, 0), head=(4, 0, 0))
    a.arms(3, (20, 0, 8), 30, 0, al=(30, 0, -8), fl=40)
    a.legs(3, 30, 60)
    a.at(7, body=(12, -8, 0), head=(10, 4, 0))
    a.arms(7, (196, -6, 10), 24, 10, al=(196, 6, -10), fl=24)
    a.legs(7, 18, 36)
    a.at(11, body=(-4, 0, 0), head=(6, 0, 0))
    a.arms(11, (214, -4, 10), 32, 16, al=(214, 4, -10), fl=32)
    a.legs(11, 44, 84)
    a.at(14, body=(18, 0, 0), head=(14, 0, 0))
    a.arms(14, (228, 0, 10), 22, 20, al=(228, 0, -10), fl=22)
    a.legs(14, 50, 96, up=4.5, fwd=-1)
    a.at(16, body=(-26, 0, 0), head=(-6, 0, 0))
    a.arms(16, (130, 0, 6), 6, 4, al=(130, 0, -6), fl=6)
    a.legs(16, 30, 50, up=2, fwd=-1.6)
    a.at(17, body=(-52, 0, 0), head=(-22, 0, 0))
    a.arms(17, (52, 0, 4), 0, 0, al=(52, 0, -4), fl=0)
    a.legs(17, 62, 114, fwd=-1.8)
    a.at(19, body=(-56, 0, 2), head=(-24, 0, 4))
    a.arms(19, (46, 0, 4), 0, 0, al=(46, 0, -4), fl=0)
    a.legs(19, 66, 120, fwd=-1.8)
    a.at(24, body=(-46, 0, 0), head=(-16, 6, 8))
    a.arms(24, (50, 0, 4), 4, 0, al=(50, 0, -4), fl=4)
    a.legs(24, 58, 104, fwd=-1.6)
    a.at(29, body=(-18, 0, 0), head=(-2, 0, 0))
    a.arms(29, (70, 0, 8), 40, 10, al=(30, 0, -8), fl=40)
    a.legs(29, 30, 50, fwd=-0.6)
    a.at(33, body=(-4, 0, 0))
    a.arm(33, "r", (30, 0, 10), 80, 30).arm(33, "l", (6, 0, -6), 16, 0)
    a.legs(33, 6, 10)
    a.sec([(0, 0, 0), (3, 3, 0), (7, -4, 0), (11, 2, 0), (14, -8, 0), (17, 12, 0), (19, 10, 0), (24, 2, 0), (29, -2, 0), (38, 0, 0)])
    a.done()

    # ================= hacksaw (40): close in 4-7, four push cuts 10/16/22/28 with pull strokes between, rip up 31
    a = mk("hacksaw", 40)
    a.show("saw", 0, 40, grow=1)
    a.at(4, body=(-10, -12, 0), head=(-2, 8, 0))
    a.arm(4, "r", (66, -20, 10), 70, -16).arm(4, "l", (66, 22, -12), 50, 0)
    a.legs(4, 22, 34, -14, 6)
    a.legs(8, 30, 46, -18, 6, fwd=-0.8)
    for i, pk in enumerate((10, 16, 22, 28)):
        hi = (0, 12, -8, 6)[i]
        a.at(pk - 3, body=(-6, -18, -2), head=(-2, 10, 0))
        a.arm(pk - 3, "r", (60 + hi, -26, 10), 92, -30)
        a.at(pk, body=(-24, 12, 2), head=(-8, -6, 2 * (i % 2 * 2 - 1)))
        a.arm(pk, "r", (96 + hi, 10, 4), 4, -4)
        a.arm(pk, "l", (60, 26, -14), 46, 0)
        a.arm(pk + 1, "r", (98 + hi, 12, 4), 2, -4)
    a.at(31, body=(4, -6, 0), head=(6, 4, 0))
    a.arm(31, "r", (150, 0, 10), 10, 10).arm(31, "l", (30, 10, -10), 30, 0)
    a.legs(31, 14, 20, -6, 4)
    a.at(35, body=(-2, 0, 0), head=(0, 0, 6))
    a.arm(35, "r", (50, 0, 10), 70, 20).arm(35, "l", (8, 0, -6), 14, 0)
    a.legs(36, 0, 0)
    a.sec([(0, 0, 0), (4, 2, -2)] + [(p, 5, 2 * (1 if i % 2 else -1)) for i, p in enumerate((10, 16, 22, 28))]
          + [(p - 3, -1, 0) for p in (13, 19, 25)] + [(31, -5, 0), (35, 1, 0), (40, 0, 0)])
    a.done()

    # ================= knives (28): pull two knives from the bandolier 3-5, right sidearm throw 10, left throw 18
    a = mk("knives", 28)
    a.scl("knife_r", (0, *HIDE), (3.9, *HIDE), (5, 1, 1, 1), (9.9, 1, 1, 1), (10, *HIDE), (28, *HIDE))
    a.scl("knife_l", (0, *HIDE), (3.9, *HIDE), (5, 1, 1, 1), (17.9, 1, 1, 1), (18, *HIDE), (28, *HIDE))
    a.at(4, body=(-8, 0, 0), head=(-8, 0, 0))
    a.arm(4, "r", (50, 40, -30), 110, 0).arm(4, "l", (50, -40, 30), 110, 0)
    a.legs(4, 6, 10)
    a.at(7, body=(6, -30, -4), head=(2, 22, 0))
    a.arm(7, "r", (150, -34, 40), 40, 30).arm(7, "l", (40, -20, 20), 80, 0)
    a.legs(7, -10, 8, 16, 20)
    a.at(10, body=(-16, 26, 4), head=(-4, -12, 0))
    a.arm(10, "r", (86, 40, -10), 0, -30)
    a.legs(10, 24, 34, -14, 6, fwd=-0.5)
    a.arm(12, "r", (60, 52, -20), 10, -20)
    a.at(15, body=(6, 30, 4), head=(2, -22, 0))
    a.arm(15, "l", (150, 34, -40), 40, 30).arm(15, "r", (30, 20, 10), 40, 0)
    a.legs(15, 16, 20, -10, 8)
    a.at(18, body=(-16, -26, -4), head=(-4, 12, 0))
    a.arm(18, "l", (86, -40, 10), 0, -30)
    a.legs(18, -14, 6, 24, 34, fwd=-0.5)
    a.arm(20, "l", (60, -52, 20), 10, -20)
    a.at(23, body=(-2, 0, 0), head=(2, 0, 8))
    a.arm(23, "r", (30, 0, 10), 70, 20).arm(23, "l", (6, 0, -6), 20, 0)
    a.legs(24, 0, 0)
    a.sec([(0, 0, 0), (4, 2, 0), (7, -2, -4), (10, 6, 4), (15, -2, 4), (18, 6, -4), (23, 0, 0), (28, 0, 0)])
    a.done()

    # ================= crowbar (28): low coil 3-7, rising UPPERCUT 10, cock across 15, horizontal HOOK 19, recover
    a = mk("crowbar", 28)
    a.show("crowbar", 0, 28, grow=1)
    a.at(3, body=(-22, -18, -4), head=(-4, 12, 0))
    a.arm(3, "r", (-28, -10, 14), 30, 0).arm(3, "l", (40, 10, -10), 50, 0)
    a.legs(3, 30, 60)
    a.at(7, body=(-30, -24, -6), head=(-8, 16, 0))
    a.arm(7, "r", (-46, -10, 18), 34, 0)
    a.legs(7, 40, 78, 30, 60)
    a.at(10, body=(14, 18, 4), head=(14, -10, 0))
    a.arm(10, "r", (172, 10, 0), 10, 10).arm(10, "l", (-20, 0, -20), 20, 0)
    a.legs(10, 10, 10, -6, 4, up=0.6)
    a.arm(12, "r", (188, 12, 0), 14, 14)
    a.at(12, body=(16, 20, 4), head=(16, -10, 0))
    a.at(15, body=(-4, -34, -4), head=(0, 24, 0))
    a.arm(15, "r", (100, -92, 0), 22, 0).arm(15, "l", (40, 30, -20), 40, 0)
    a.legs(15, -6, 10, 18, 24)
    a.at(19, body=(-16, 34, 6), head=(-4, -18, 0))
    a.arm(19, "r", (96, 62, 0), 0, 0).arm(19, "l", (-10, -10, -20), 20, 0)
    a.legs(19, 28, 40, -14, 6, fwd=-0.6)
    a.arm(21, "r", (86, 82, 0), 6, 0)
    a.at(24, body=(-4, 0, 0), head=(2, 0, 6))
    a.arm(24, "r", (40, 0, 10), 70, 20).arm(24, "l", (6, 0, -6), 16, 0)
    a.legs(25, 0, 0)
    a.sec([(0, 0, 0), (3, 3, -3), (7, 4, -4), (10, -8, 3), (12, -6, 3), (15, -2, -4), (19, 6, 5), (21, 5, 5), (24, 0, 0), (28, 0, 0)])
    a.done()

    # ================= pliers (36): jaws open + draw 4-9, LUNGE SNAP 11 (stretch), two-hand YANK 13-20, TWIST 22, release
    a = mk("pliers", 36)
    a.show("pliers", 0, 36, grow=1)
    a.rot("pjaw_a", (0, 0, 0, 0), (4, -24, 0, 0), (10.5, -30, 0, 0), (11.5, 2, 0, 0), (23, 2, 0, 0), (25, -24, 0, 0), (30, 0, 0, 0))
    a.rot("pjaw_b", (0, 0, 0, 0), (4, 24, 0, 0), (10.5, 30, 0, 0), (11.5, -2, 0, 0), (23, -2, 0, 0), (25, 24, 0, 0), (30, 0, 0, 0))
    a.scl("pliers", (0, 1, 1, 1), (10, 1, 1, 1), (11, 1, 2.2, 1), (12.5, 1, 1.6, 1), (15, 1, 1, 1), (36, 1, 1, 1))
    a.at(4, body=(6, -10, 0), head=(2, 6, 0))
    a.arm(4, "r", (70, -10, 10), 60, 0).arm(4, "l", (20, 0, -10), 30, 0)
    a.legs(4, -8, 8, 12, 16)
    a.at(9, body=(10, -16, -2), head=(4, 10, 0))
    a.arm(9, "r", (60, -14, 14), 92, 0)
    a.at(11, body=(-26, 6, 2), head=(-6, -4, 0))
    a.arm(11, "r", (94, 0, 4), 0, 0).arm(11, "l", (10, 0, -20), 10, 0)
    a.legs(11, 40, 60, -26, 6, fwd=-1.2)
    for t, j in ((13, 0), (14, 1), (16, -1), (18, 1), (20, 0)):
        a.at(t, body=(16 + 2 * j, -4 * j, 0), head=(8, 2 * j, 0))
        a.arm(t, "r", (52 + 4 * j, 0, 8), 70, 0).arm(t, "l", (54 - 4 * j, -14, -8), 72, 0)
        a.legs(t, 20 + 3 * j, 24, -10, 4, fwd=0.8)
    a.at(22, body=(-12, 24, 4), head=(-4, -10, 0))
    a.arm(22, "r", (80, 10, -30), 20, (0, 110, 0)).arm(22, "l", (60, -20, -10), 40, 0)
    a.legs(22, 24, 34, -12, 6)
    a.arm(25, "r", (70, 10, 10), 40, (0, 60, 0))
    a.at(28, body=(-2, 0, 0), head=(0, 0, 8))
    a.arm(28, "r", (34, 0, 10), 76, (20, 0, 0)).arm(28, "l", (6, 0, -6), 16, 0)
    a.legs(30, 0, 0)
    a.sec([(0, 0, 0), (4, -2, -2), (9, -3, -2), (11, 10, 0), (13, -6, 0), (14, -6, 2), (16, -6, -2), (18, -6, 2), (22, 4, 4), (28, 0, 0), (36, 0, 0)])
    a.done()

    # ================= drill (36): rev 3-7, four drilling THRUSTS 10/16/22/28 (bit spinning), pull back
    a = mk("drill", 36)
    a.show("drill", 0, 36, grow=1)
    a.rot("bit", *[(t, 0, max(0, t - 3) * 150, 0) for t in range(0, 37, 3)])
    a.at(4, body=(-6, -6, 0), head=(-2, 4, 0))
    a.arm(4, "r", (90, 0, 6), 0, 0).arm(4, "l", (72, 24, -14), 40, 0)
    a.legs(4, 14, 20, -8, 4)
    for i, pk in enumerate((10, 16, 22, 28)):
        a.at(pk - 3, body=(-2, -8, 0), head=(0, 6, 0))
        a.arm(pk - 3, "r", (78, 0, 6), 46, 0).arm(pk - 3, "l", (70, 26, -14), 56, 0)
        a.legs(pk - 3, 12, 18, -6, 4)
        a.at(pk, body=(-24, 4, 2 * (1 if i % 2 else -1)), head=(-8, -2, 0))
        a.arm(pk, "r", (96, 0, 4), 0, 0).arm(pk, "l", (84, 16, -12), 20, 0)
        a.legs(pk, 34, 52, -20, 6, fwd=-0.8)
        a.rot("hand_r", (pk + 1, 0, 0, 4), (pk + 2, 0, 0, -4))
    a.at(31, body=(-4, 0, 0), head=(0, 0, 0))
    a.arm(31, "r", (70, 0, 8), 30, 0).arm(31, "l", (20, 0, -8), 20, 0)
    a.legs(32, 0, 0)
    a.sec([(0, 0, 0), (4, 1, 0)] + [(p, 6, 1) for p in (10, 16, 22, 28)] + [(p - 3, -1, 0) for p in (13, 19, 25)] + [(31, -2, 0), (36, 0, 0)])
    a.done()

    # ================= nailgun (32): shoulder the gun 4, burst 8-24 (recoil every 2 ticks, spray sweep), lower
    a = mk("nailgun", 32)
    a.show("nailgun", 0, 32, grow=1)
    a.at(5, body=(4, -10, 0), head=(-2, 6, 0))
    a.arm(5, "r", (90, -6, 4), 0, 0).arm(5, "l", (80, 26, -12), 32, 0)
    a.legs(5, -8, 6, 14, 18)
    for t in range(8, 25):
        sweep = -10 + 20 * (t - 8) / 16
        if t % 2 == 0:
            a.at(t, body=(6, sweep, 0), head=(-2, -sweep * 0.3, 0))
            a.arm(t, "r", (102, -6, 4), 10, 8)
        else:
            a.at(t, body=(3, sweep, 0))
            a.arm(t, "r", (90, -6, 4), 0, 0)
    a.at(27, body=(0, 0, 0), head=(4, 0, 6))
    a.arm(27, "r", (40, 0, 10), 70, 20).arm(27, "l", (10, 0, -6), 16, 0)
    a.legs(28, 0, 0)
    a.sec([(0, 0, 0), (5, -1, -2)] + [(t, -2 if t % 4 == 0 else 0, 0) for t in range(8, 25, 2)] + [(27, 1, 0), (32, 0, 0)])
    a.done()

    # ================= workshop (64, enraged): knife fan 8 -> swap saw, dash 14, slashes 18/22 -> hammer hop 30 slam 34
    #                   -> axe chop 48 -> both axes thrown 56
    a = mk("workshop", 64)
    a.scl("knife_r", (0, *HIDE), (1.9, *HIDE), (3, 1, 1, 1), (7.9, 1, 1, 1), (8, *HIDE), (64, *HIDE))
    a.scl("saw", (0, *HIDE), (10.9, *HIDE), (12, 1, 1, 1), (25.5, 1, 1, 1), (26.5, *HIDE), (64, *HIDE))
    a.scl("hammer", (0, *HIDE), (25.9, *HIDE), (27, 1, 1, 1), (39.5, 1, 1, 1), (40.5, *HIDE), (64, *HIDE))
    a.scl("axe", (0, *HIDE), (40.4, *HIDE), (41.5, 1, 1, 1), (55.9, 1, 1, 1), (56, *HIDE), (62, *HIDE), (63, 1, 1, 1), (64, 1, 1, 1))
    a.scl("axe2", (0, *HIDE), (49.9, *HIDE), (51, 1, 1, 1), (55.9, 1, 1, 1), (56, *HIDE), (64, *HIDE))
    # knife fan
    a.at(4, body=(6, -30, -4), head=(2, 22, 0))
    a.arm(4, "r", (150, -34, 40), 40, 30).arm(4, "l", (40, 10, -20), 40, 0)
    a.legs(4, -10, 8, 16, 20)
    a.at(8, body=(-16, 26, 4), head=(-4, -12, 0))
    a.arm(8, "r", (86, 40, -10), 0, -30)
    a.legs(8, 24, 34, -14, 6)
    # swap to saw (reach behind the back)
    a.at(11, body=(4, -10, 0), head=(4, 10, 0))
    a.arm(11, "r", (-50, 0, 20), 40, 0)
    a.at(14, body=(-34, 0, 0), head=(-10, 0, 0))
    a.arm(14, "r", (170, -30, 10), 30, 20).arm(14, "l", (-30, 0, -20), 10, 0)
    a.legs(14, 40, 60, -28, 6, fwd=-1.2)
    a.at(18, body=(-26, 30, 6), head=(-6, -14, 0))
    a.arm(18, "r", (60, 34, 0), 0, 0)
    a.legs(18, 30, 46, -18, 6)
    a.at(20, body=(-10, 30, 4))
    a.arm(20, "r", (106, 66, 0), 30, 0)
    a.at(22, body=(-24, -34, -6), head=(-4, 16, 0))
    a.arm(22, "r", (98, -88, 0), 0, 0)
    a.legs(22, -14, 6, 26, 40)
    # hammer leap + slam
    a.at(26, body=(10, -6, 0), head=(6, 4, 0))
    a.arms(26, (180, -6, 10), 30, 10, al=(180, 6, -10), fl=30)
    a.legs(26, 30, 60)
    a.at(29, body=(-4, 0, 0))
    a.arms(29, (214, -4, 10), 32, 16, al=(214, 4, -10), fl=32)
    a.legs(29, 44, 84)
    a.at(31, body=(18, 0, 0), head=(14, 0, 0))
    a.arms(31, (228, 0, 10), 22, 20, al=(228, 0, -10), fl=22)
    a.legs(31, 50, 96, up=4.5, fwd=-1)
    a.at(33, body=(-26, 0, 0))
    a.arms(33, (130, 0, 6), 6, 4, al=(130, 0, -6), fl=6)
    a.legs(33, 30, 50, up=2, fwd=-1.6)
    a.at(34, body=(-52, 0, 0), head=(-22, 0, 0))
    a.arms(34, (52, 0, 4), 0, 0, al=(52, 0, -4), fl=0)
    a.legs(34, 62, 114, fwd=-1.8)
    a.at(38, body=(-44, 0, 0), head=(-14, 0, 0))
    a.arms(38, (50, 0, 4), 4, 0, al=(50, 0, -4), fl=4)
    a.legs(38, 54, 96, fwd=-1.4)
    # swap to axe, overhead chop
    a.at(41, body=(-10, 0, 0), head=(0, 0, 0))
    a.arms(41, (90, 0, 10), 40, 0, al=(40, 0, -10), fl=30)
    a.legs(41, 20, 30)
    a.at(45, body=(20, -24, -4), head=(10, 16, 4))
    a.arm(45, "r", (200, -14, 10), 38, 28).arm(45, "l", (176, 28, -12), 30, 10)
    a.legs(45, -12, 14, 22, 30)
    a.at(47, body=(-14, 4, 2))
    a.arm(47, "r", (120, 0, 6), 10, 8).arm(47, "l", (110, 10, -8), 10, 4)
    a.at(48, body=(-40, 8, 4), head=(-16, -4, 0))
    a.arm(48, "r", (56, 4, 4), 0, 4).arm(48, "l", (62, -6, -4), 4, 0)
    a.legs(48, 44, 70, -24, 6, fwd=-1.2)
    # both axes up, double throw 56
    a.at(52, body=(14, 0, 0), head=(10, 0, 0))
    a.arms(52, (200, -16, 14), 30, 20, al=(200, 16, -14), fl=30)
    a.legs(52, -8, 8, 10, 14)
    a.at(54, body=(18, 0, 0))
    a.arms(54, (216, -16, 16), 40, 26, al=(216, 16, -16), fl=40)
    a.at(56, body=(-24, 0, 0), head=(-4, 0, 0))
    a.arms(56, (84, 14, 0), 0, -20, al=(84, -14, 0), fl=0)
    a.legs(56, 28, 40, -16, 6, fwd=-0.6)
    a.arms(58, (50, 24, -6), 10, -10, al=(50, -24, 6), fl=10)
    a.at(61, body=(-4, 0, 0), head=(4, 0, 10))
    a.arm(61, "r", (40, 0, 10), 70, 20).arm(61, "l", (8, 0, -6), 16, 0)
    a.legs(62, 0, 0)
    a.sec([(0, 0, 0), (4, -2, -4), (8, 6, 4), (11, -2, 0), (14, 9, 0), (18, 5, 5), (22, 5, -5), (26, -3, 0), (31, -8, 0), (34, 12, 0),
           (38, 4, 0), (45, -6, -3), (48, 10, 2), (52, -5, 0), (56, 8, 0), (61, 0, 0), (64, 0, 0)])
    a.done()

    # ================= bladewave (30): wind the saw far back 5-9, flat SWEEP 12 (wave), reverse coil 17, BACKHAND 21 (wave)
    a = mk("bladewave", 30)
    a.show("saw", 0, 30, grow=1)
    a.at(5, body=(-6, -40, -6), head=(0, 30, 0))
    a.arm(5, "r", (100, -100, 0), 10, 0).arm(5, "l", (40, 30, -20), 40, 0)
    a.legs(5, -10, 10, 20, 30)
    a.at(9, body=(-8, -50, -8), head=(0, 36, 0))
    a.arm(9, "r", (102, -118, 0), 16, 0)
    a.legs(9, -14, 12, 24, 36)
    a.at(12, body=(-20, 40, 6), head=(-4, -20, 0))
    a.arm(12, "r", (95, 68, 0), 0, 0).arm(12, "l", (-20, -10, -30), 20, 0)
    a.legs(12, 30, 46, -18, 6, fwd=-0.8)
    a.at(14, body=(-22, 48, 6))
    a.arm(14, "r", (90, 96, 0), 6, 0)
    a.at(17, body=(-10, 40, 6), head=(0, -24, 0))
    a.arm(17, "r", (112, 74, 0), 34, 0)
    a.legs(17, 20, 30, -10, 6)
    a.at(21, body=(-22, -40, -6), head=(-4, 18, 0))
    a.arm(21, "r", (98, -92, 0), 0, 0).arm(21, "l", (-10, 20, -20), 20, 0)
    a.legs(21, -18, 6, 30, 46, fwd=-0.8)
    a.at(23, body=(-24, -48, -6))
    a.arm(23, "r", (94, -112, 0), 6, 0)
    a.at(26, body=(-4, 0, 0), head=(0, 0, 8))
    a.arm(26, "r", (40, 0, 10), 70, 20).arm(26, "l", (6, 0, -6), 16, 0)
    a.legs(27, 0, 0)
    a.sec([(0, 0, 0), (5, -2, -4), (9, -3, -5), (12, 7, 6), (14, 6, 6), (17, -1, 4), (21, 7, -6), (23, 6, -6), (26, 0, 0), (30, 0, 0)])
    a.done()

    # ================= beartrap (34): pull the trap out 3, crank the jaws open 6, swing low 9, underhand TOSS 12, watch, head-tilt
    a = mk("beartrap", 34)
    a.scl("trap", (0, *HIDE), (1.9, *HIDE), (3, 1, 1, 1), (12, 1, 1, 1), (12.6, *HIDE), (34, *HIDE))
    a.rot("tjaw_a", (0, 70, 0, 0), (4, 70, 0, 0), (7, 0, 0, 0), (34, 0, 0, 0))
    a.rot("tjaw_b", (0, -70, 0, 0), (4, -70, 0, 0), (7, 0, 0, 0), (34, 0, 0, 0))
    a.at(3, body=(-10, 0, 0), head=(-12, 0, 0))
    a.arm(3, "r", (46, 22, -20), 60, 0).arm(3, "l", (46, -22, 20), 60, 0)
    a.legs(3, 8, 12)
    a.at(6, body=(-12, 0, 0), head=(-14, 0, 4))
    a.arm(6, "r", (56, 4, 14), 40, 0).arm(6, "l", (56, -4, -14), 40, 0)
    a.at(9, body=(-24, 0, 0), head=(-4, 0, 0))
    a.arms(9, (-40, 0, 10), 10, 0, al=(-40, 0, -10), fl=10)
    a.legs(9, 34, 64)
    a.at(12, body=(8, 0, 0), head=(8, 0, 0))
    a.arms(12, (120, 0, 10), 0, 0, al=(120, 0, -10), fl=0)
    a.legs(12, 6, 6, up=0.4)
    a.arms(15, (140, 0, 14), 6, 0, al=(140, 0, -14), fl=6)
    a.at(15, body=(10, 0, 0), head=(10, 0, 0))
    a.at(20, body=(0, 0, 0), head=(-6, 0, 22))
    a.arms(20, (10, 0, 10), 10, 0, al=(6, 0, -8), fl=10)
    a.legs(20, 0, 0)
    a.at(26, head=(-6, 0, -18))
    a.at(30, head=(0, 0, 4))
    a.carry(30)
    a.sec([(0, 0, 0), (3, 2, 0), (9, 5, 0), (12, -8, 0), (15, -4, 0), (20, 0, 4), (26, 0, -4), (34, 0, 0)])
    a.done()

    # ================= toolrain (50, enraged): hunch 4, fling a fistful of blades skyward 10, conduct the rain 16-40, final drop 42
    a = mk("toolrain", 50)
    a.scl("knife_r", (0, *HIDE), (3.9, *HIDE), (5, 1, 1, 1), (9.9, 1, 1, 1), (10, *HIDE), (50, *HIDE))
    a.scl("knife_l", (0, *HIDE), (3.9, *HIDE), (5, 1, 1, 1), (9.9, 1, 1, 1), (10, *HIDE), (50, *HIDE))
    a.at(4, body=(-22, 0, 0), head=(-18, 0, 0))
    a.arm(4, "r", (40, 40, -30), 110, 0).arm(4, "l", (40, -40, 30), 110, 0)
    a.legs(4, 30, 60)
    a.at(7, body=(-26, 0, 0), head=(-20, 0, 0))
    a.legs(7, 36, 70)
    a.at(10, body=(16, 0, 0), head=(30, 0, 0))
    a.arms(10, (196, 0, 36), 0, 0, al=(196, 0, -36), fl=0)
    a.legs(10, 0, 0, up=0.6)
    a.at(13, body=(12, 0, 0), head=(26, 0, 0))
    a.arms(13, (180, 0, 30), 10, 0, al=(180, 0, -30), fl=10)
    for i, pk in enumerate((16, 22, 28, 34, 40)):
        k, o = ("r", "l") if i % 2 == 0 else ("l", "r")
        s = 1 if k == "r" else -1
        a.arm(pk - 3, k, (170, -10 * s, 20), 10, 0)
        a.at(pk - 3, body=(4, -10 * s, 0), head=(10, 6 * s, 0))
        a.arm(pk, k, (96, 10 * s, 6), 0, 0)
        a.arm(pk, o, (40, 0, 12), 30, 0)
        a.at(pk, body=(-12, 12 * s, 2 * s), head=(-4, -6 * s, 0))
    a.legs(16, 10, 12, -4, 4).legs(28, -4, 4, 10, 12).legs(40, 6, 8)
    a.at(43, body=(6, 0, 0), head=(10, 0, 0))
    a.arms(43, (170, 0, 20), 10, 0, al=(170, 0, -20), fl=10)
    a.at(45, body=(-30, 0, 0), head=(-14, 0, 0))
    a.arms(45, (40, 0, 10), 0, 0, al=(40, 0, -10), fl=0)
    a.legs(45, 24, 44)
    a.at(48, body=(-6, 0, 0), head=(0, 0, 12))
    a.carry(49)
    a.arm(49, "l", (4, 0, -6), 12, 0)
    a.legs(49, 0, 0)
    a.sec([(0, 0, 0), (4, 4, 0), (10, -8, 0), (13, -6, 0)] + [(p, 4, 3 if i % 2 == 0 else -3) for i, p in enumerate((16, 22, 28, 34, 40))]
          + [(43, -5, 0), (45, 8, 0), (50, 0, 0)])
    a.done()

    # ================= death (40): jolt back 4, axe slips 8, knees give 12, kneel slump 18, topple sideways 26, hat rolls off, twitch
    a = mk("death", 40)
    a.scl("axe", (0, 1, 1, 1), (8, 1, 1, 1), (9, *HIDE), (40, *HIDE))
    a.at(4, body=(16, 0, 8), head=(20, 0, 12))
    a.arm(4, "r", (40, 0, 30), 30, 0).arm(4, "l", (30, 0, -40), 30, 0)
    a.legs(4, -6, 4, 4, 6, setpos=False)
    a.at(8, body=(8, 0, 4), head=(10, 0, 8))
    a.arms(8, (10, 0, 16), 10, 0, al=(10, 0, -16), fl=10)
    a.legs(12, 20, 70, setpos=False)
    a.at(12, body=(-10, 0, 0), head=(-10, 0, 6))
    a.legs(18, 10, 92, setpos=False)
    a.at(18, body=(-34, 0, 4), head=(-30, 0, 10))
    a.arms(18, (6, 0, 4), 4, 0, al=(6, 0, -4), fl=4)
    a.rot("pelvis", (0, 0, 0, 0), (18, 0, 0, 0), (22, 0, 0, 30), (26, 0, 0, 88), (29, 0, 0, 84), (32, 0, 0, 86), (40, 0, 0, 86))
    a.pos("pelvis", (0, 0, 0, 0), (12, 0, -drop(20, 70), 0), (18, 0, -drop(10, 92), 0), (22, 0, -3.6, 0), (26, 0, -6.4, 0), (29, 0, -6.0, 0),
          (32, 0, -6.4, 0), (40, 0, -6.4, 0))
    a.at(26, body=(-10, 0, 0), head=(-6, 0, -10))
    a.arms(26, (30, 0, 50), 20, 0, al=(60, 0, -20), fl=30)
    a.legs(26, 40, 100, 20, 60, setpos=False)
    a.at(40, body=(-12, 0, 0), head=(-8, 0, -12))
    a.arm(34, "r", (34, 0, 54), 40, 20).arm(36, "r", (30, 0, 50), 20, 0).arm(40, "r", (30, 0, 50), 22, 0)
    a.pos("hat", (0, 0, 0, 0), (20, 0, 0, 0), (24, 0, 1.5, -1), (28, 0, 0.5, -3), (32, 0, -1.5, -4), (40, 0, -1.5, -4))
    a.rot("hat", (0, 0, 0, 0), (20, 0, 0, 0), (24, -30, 0, 20), (28, -70, 10, 50), (32, -90, 20, 70), (40, -90, 20, 70))
    a.sec([(0, 0, 0), (4, -6, 3), (8, -2, 0), (12, 4, 0), (18, 6, 0), (22, 0, 6), (26, 0, 10), (29, 0, -4), (40, 0, 0)])
    a.done()


def main():
    B = Builder("aiden", 1.0, False, 8)
    build(B)
    anims(B)
    B.m.save(os.path.join(DIR, "aiden.bbmodel"))
    print("cubes", len(B.m.cubes), "anims", [a["name"] for a in B.m.anims])


if __name__ == "__main__":
    main()
