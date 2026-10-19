"""Lord Hansel - MATURED form (variant 0) -> assets/fpe/bbmodels/lord_hansel.bbmodel.
Reference: docs/ref/confirmed/hansel_matured.png. Lanky hunched beast-man (hitbox 0.9 x 2.6 = ~42 px + antlers):
pale cream fur hood/mane + fur cloak, big black branching antlers, pale grinning face with narrow dark eyes, black thorny
shoulder armour, bandaged/scarred tan torso, long black arms - RIGHT hand with very long black claws, LEFT hand holding a
bloody red-black crystalline claw-heart dripping blood, striped trousers, tall dark-brown X-laced wrapped boots, huge fluffy tail
curling out to his right. Every key tick matches entity/characters/LordHansel.java.
Run: python3 tools/bbgen/chars/lord_hansel.py
"""
import math
from lh_common import Model, Kit, A, ROOT, mix, sinekeys, CLEAR

FUR, FUR_L, FUR_D, FUR_DD = 0xE9DDBF, 0xF8F2E0, 0xC6B58F, 0x9A8862
SKIN, SKIN_D, SKIN_L = 0xC9A589, 0x9A7A60, 0xE0C2A6
BAND, BAND_D = 0xDCD2BE, 0xA89C86
BLK, BLK_L, BLK_D, GREY = 0x1C191A, 0x3C3537, 0x0B0909, 0x67605F
BOOT, BOOT_D, BOOT_L, LACE = 0x4C3123, 0x2C1A12, 0x6E4C38, 0xA08C76
TROU, TROU_D = 0x8C7860, 0x4E3C2C
RED, RED_D, RED_L = 0xB3121C, 0x55060B, 0xE8353C
FACE, FACE_D = 0xF0EADC, 0xBDB3A2
ANT, ANT_L = 0x161314, 0x3A3334

m = Model("lord_hansel", S=8, atlas=2048)
K = Kit(m)
R = m.rng
af, flat, clear = K.all_faces, K.flat, K.clear


# ------------------------------------------------------------------ painters
def furp(base=FUR, ink=None):
    return K.strands(base, FUR_L, FUR_DD, ink)


def torso_front(F):
    """tan skin, bandage wraps across, rib lines and red scratch scars"""
    for y in range(F.h):
        for x in range(F.w):
            F.px(x, y, mix(SKIN_L, SKIN_D, 0.2 + 0.5 * y / F.h))
    for j in range(5):                                   # ribs
        yy = 6 + j * 5
        F.line(F.w / 2 - 3, yy, 3, yy + 3, SKIN_D, 1)
        F.line(F.w / 2 + 3, yy, F.w - 4, yy + 3, SKIN_D, 1)
    F.line(F.w / 2, 2, F.w / 2, F.h - 4, SKIN_D, 1)
    for (y, h) in ((F.h - 14, 4), (F.h - 7, 3)):         # bandage bands
        for x in range(F.w):
            for yy in range(h):
                F.px(x, y + yy + (x // 6) % 2, BAND if (x + yy) % 5 else BAND_D)
    for k in range(3):                                   # red claw scratches
        x0 = 8 + k * 4
        F.line(x0, 8 + k, x0 + 10, 24 + k, RED, 1)
        F.line(x0 + 1, 8 + k, x0 + 11, 24 + k, RED_D, 1)


def torso_side(F):
    for y in range(F.h):
        for x in range(F.w):
            F.px(x, y, mix(SKIN, SKIN_D, 0.3 + 0.5 * y / F.h))
    for x in range(F.w):
        for yy in range(4):
            F.px(x, F.h - 12 + yy + (x // 5) % 2, BAND if (x + yy) % 4 else BAND_D)


def armourp(F):
    """black thorn armour: dark plates, grey ridges"""
    for y in range(F.h):
        for x in range(F.w):
            F.px(x, y, mix(BLK_L, BLK_D, 0.2 + 0.6 * y / max(1, F.h)))
    for i in range(0, F.w, 5):
        F.line(i, 0, i + 3, F.h, BLK_D, 1)
        F.line(i + 1, 0, i + 2, F.h * 0.6, GREY, 1)
    K.outline(BLK_D)(F)


def armp(F):
    for y in range(F.h):
        for x in range(F.w):
            F.px(x, y, mix(BLK_L, BLK, 0.3 + 0.5 * y / max(1, F.h)))
    for _ in range(F.w * F.h // 40):
        x, y = R.randint(0, F.w - 1), R.randint(0, F.h - 1)
        F.line(x, y, x + 1, y + 3, GREY, 1)


def bootp(F):
    """dark brown wraps with X lacing"""
    for y in range(F.h):
        for x in range(F.w):
            band = (y + x * 0.4) % 7
            c = BOOT_L if band < 1.3 else (BOOT_D if band > 5.8 else BOOT)
            F.px(x, y, mix(c, BOOT_D, 0.3 * y / F.h))
    cx = F.w / 2
    for y in range(2, F.h - 6, 8):
        F.line(cx - 4, y, cx + 4, y + 6, LACE, 1)
        F.line(cx + 4, y, cx - 4, y + 6, LACE, 1)


def bootside(F):
    for y in range(F.h):
        for x in range(F.w):
            band = (y - x * 0.4) % 7
            F.px(x, y, BOOT_L if band < 1.3 else (BOOT_D if band > 5.8 else BOOT))


def trouserp(F):
    for y in range(F.h):
        for x in range(F.w):
            s = (x + y * 0.3) % 9
            F.px(x, y, TROU_D if s < 2.2 else mix(TROU, TROU_D, 0.2 * y / F.h))


def heartp(F):
    for y in range(F.h):
        for x in range(F.w):
            F.px(x, y, mix(RED_L, RED_D, 0.2 + 0.6 * ((x * 3 + y * 5) % 13) / 13))
    for _ in range(4):
        x, y = R.uniform(0, F.w), R.uniform(0, F.h)
        F.line(x, y, x + R.uniform(-5, 5), y + R.uniform(-5, 5), BLK_D, 1)
    F.disc(F.w * 0.35, F.h * 0.35, 1.2, 0xFF8A8A, glow=True)


def face_front(F):
    W, H = F.w, F.h
    for y in range(H):
        for x in range(W):
            F.px(x, y, mix(FACE, FACE_D, 0.1 + 0.5 * y / H))
    # fur fringe hanging over the forehead (spiky)
    for x in range(W):
        top = 8 + int(4 * abs(math.sin(x * 0.55))) + (3 if x % 7 == 3 else 0)
        for y in range(top):
            F.px(x, y, mix(FUR_L, FUR_D, y / 14))
        F.px(x, top, FUR_DD)
    # narrow, slanted, menacing eyes: black almond with a tiny red glowing pupil
    for s in (-1, 1):
        ex = W / 2 + s * 9
        for x in range(-6, 7):
            yy = 19 + int(-s * x * 0.35)
            th = 3 if abs(x) < 4 else 2
            F.rect(ex + x, yy, 1, th, BLK_D)
        F.rect(ex - s * 1 - 1, 19 + 1, 2, 1, 0xFF3030, glow=True)
        F.line(ex - 7, 15 + s * 0, ex + 7, 16 - s * 4, FUR_DD, 1)     # angry brow
        F.line(ex - 5, 25, ex + 5, 24, FACE_D, 1)
    F.line(W / 2 - 1, 23, W / 2 - 1, 27, FACE_D, 1)   # nose ridge
    F.rect(W / 2 - 2, 28, 4, 1, BLK)
    # wide jagged grin with many teeth
    for x in range(6, W - 6):
        u = (x - 6) / (W - 12)
        top = 33 - 3 * math.sin(math.pi * u) * 0.3 - (4 if u < 0.08 or u > 0.92 else 0) * 0
        bot = 34 + 5 * math.sin(math.pi * u)
        for y in range(int(top), int(bot) + 1):
            F.px(x, y, BLK_D)
        if x % 2 == 0:
            F.px(x, int(top), 0xFFFFFF); F.px(x, int(top) + 1, 0xFFFFFF)
            F.px(x, int(bot) - 1, 0xF4F0E8)
        F.px(x, int(top) - 1, BLK)
    F.line(5, 30, 7, 33, BLK, 1); F.line(W - 6, 30, W - 8, 33, BLK, 1)       # grin corners
    F.line(W - 9, 38, W - 9, 43, RED, 1); F.px(W - 9, 44, RED_D)             # blood drip


def faceside(F):
    for y in range(F.h):
        for x in range(F.w):
            F.px(x, y, mix(FACE, FACE_D, 0.3 + 0.4 * y / F.h))


# ------------------------------------------------------------------ skeleton
m.group("root", (0, 0, 0))
m.group("body", (0, 20, 0), parent="root")
m.group("chest", (0, 23, 0), rot=(-12, 0, 0), parent="body")
m.group("head", (0, 33.4, -0.8), rot=(10, 0, 0), parent="chest")
m.group("jaw", (0, 35.0, -2.0), parent="head")
m.group("hood", (0, 37, 1), parent="head")
m.group("antler_r", (1.6, 39.0, 0.2), parent="head")
m.group("antler_l", (-1.6, 39.0, 0.2), parent="head")
m.group("mane", (0, 31.5, 0.5), parent="chest")
m.group("cloak", (0, 31.5, 2.2), parent="chest")
m.group("cloak_r", (3.6, 31.0, 1.4), parent="cloak")
m.group("cloak_l", (-3.6, 31.0, 1.4), parent="cloak")
m.group("arm_r", (4.6, 30.6, 0), rot=(0, 0, 6), parent="chest")
m.group("fore_r", (5.0, 23.4, 0), parent="arm_r")
m.group("hand_r", (5.0, 16.4, 0), parent="fore_r")
m.group("claws_r", (5.0, 15.2, -0.2), parent="hand_r")
m.group("shard", (5.0, 14.4, -0.6), parent="hand_r")
m.group("arm_l", (-4.6, 30.6, 0), rot=(0, 0, -6), parent="chest")
m.group("fore_l", (-5.0, 23.4, 0), parent="arm_l")
m.group("hand_l", (-5.0, 16.6, 0), parent="fore_l")
m.group("heart", (-5.0, 14.2, -0.8), parent="hand_l")
m.group("tail", (0.6, 20.6, 2.2), rot=(26, 38, 0), parent="body")
m.group("tail1", (0.6, 20.6, 7.4), parent="tail")
m.group("tail2", (0.6, 20.6, 14.0), rot=(-28, 0, 0), parent="tail1")
m.group("tail3", (0.6, 20.6, 19.6), rot=(-26, 0, 0), parent="tail2")
for s, k in ((1, "r"), (-1, "l")):
    m.group("leg_" + k, (1.8 * s, 20, 0), parent="body")
    m.group("shin_" + k, (1.8 * s, 10.6, 0), parent="leg_" + k)

# ------------------------------------------------------------------ legs: striped trousers, tall laced boots
for s, k in ((1, "r"), (-1, "l")):
    x = 1.8 * s
    m.cube("thigh_" + k, "leg_" + k, (x - 1.35, 10.2, -1.35), (x + 1.35, 20.4, 1.35), TROU, faces=af(trouserp))
    m.cube("boot_" + k, "shin_" + k, (x - 1.5, 1.2, -1.5), (x + 1.5, 11.4, 1.5), BOOT, faces={"north": bootp, "south": bootside, "east": bootside, "west": bootside, "up": flat(BOOT_L), "down": flat(BOOT_D)})
    m.cube("bootcuff_" + k, "shin_" + k, (x - 1.75, 10.4, -1.75), (x + 1.75, 12.6, 1.75), BOOT_L, origin=(x, 11.5, 0), rot=(0, 0, 5 * s), faces=af(bootside))
    m.cube("bootwrap_" + k, "shin_" + k, (x - 1.65, 5.6, -1.65), (x + 1.65, 6.6, 1.65), BOOT_D, origin=(x, 6.1, 0), rot=(0, 0, -9 * s), faces=af(bootside))
    m.cube("foot_" + k, "shin_" + k, (x - 1.5, 0, -4.4), (x + 1.5, 1.8, 1.6), BOOT_D, faces=af(bootside) | {"up": flat(BOOT)})
    m.cube("toe_" + k, "shin_" + k, (x - 1.0, 0, -5.8), (x + 1.0, 1.2, -4.2), BOOT_D, origin=(x, 0.6, -5), rot=(0, 0, 0), faces=af(flat(BOOT_D)))
    m.cube("strip_" + k, "shin_" + k, (x + 1.3 * s - 0.25, 6.8, -0.6), (x + 1.3 * s + 0.25, 10.6, -0.2), BOOT_L, origin=(x + 1.3 * s, 10.6, -0.4), rot=(0, 0, 14 * s), faces=af(K.pointed(bootside, 4)))
    for j in range(2):   # trouser stripes wraps / tears
        y = 13.2 + j * 3.6
        m.cube(f"twrap{j}_{k}", "leg_" + k, (x - 1.5, y - 0.4, -1.5), (x + 1.5, y + 0.4, 1.5), TROU_D, origin=(x, y, 0), rot=(0, 0, (10 - j * 20) * s), faces=af(flat(TROU_D)))

# ------------------------------------------------------------------ hips + torso
m.cube("belt", "body", (-3.4, 18.8, -1.9), (3.4, 21.4, 1.9), BLK, faces=af(armourp))
m.cube("belt_buckle", "body", (-0.8, 19.2, -2.1), (0.8, 20.8, -1.8), GREY, faces=af(flat(GREY)))
for i, (x, z, rz) in enumerate(((-2.8, -1.9, -10), (2.6, -1.9, 12), (-3.2, 0.6, -18), (3.2, 0.4, 20), (0, 1.9, 4))):   # loincloth tatters
    K.plane(f"tatter{i}", "body", (x, 19.2, z), 1.6, 4.5, K.pointed(furp(FUR_D), 4), rot=(0, 90 if abs(z) < 1 else 0, rz))
m.cube("belly", "chest", (-2.7, 21.0, -1.6), (2.7, 26.6, 1.6), SKIN, faces={"north": torso_front, "south": torso_side, "east": torso_side, "west": torso_side, "up": flat(SKIN), "down": flat(SKIN_D)})
m.cube("ribcage", "chest", (-3.4, 26.0, -1.9), (3.4, 31.6, 2.0), SKIN, faces={"north": torso_front, "south": armourp, "east": torso_side, "west": torso_side, "up": flat(SKIN_D), "down": flat(SKIN_D)})
m.cube("bandage_x", "chest", (-3.6, 25.2, -2.1), (3.6, 26.2, 2.1), BAND, origin=(0, 25.7, 0), rot=(0, 0, 12), faces=af(flat(BAND)))
m.cube("neck", "chest", (-1.2, 31.0, -1.4), (1.2, 34.2, 1.2), SKIN_D, faces=af(flat(SKIN_D)))

# black thorny shoulder armour
for s, k in ((1, "r"), (-1, "l")):
    x = 4.4 * s
    m.cube("pauldron_" + k, "chest", (x - 2.0, 29.6, -2.3), (x + 2.0, 32.4, 2.3), BLK, origin=(x, 31, 0), rot=(0, 0, -16 * s), faces=af(armourp))
    m.cube("pauldron2_" + k, "chest", (x + 0.6 * s - 1.6, 28.4, -2.0), (x + 0.6 * s + 1.6, 30.2, 2.0), BLK_L, origin=(x, 29.3, 0), rot=(0, 0, -26 * s), faces=af(armourp))
    for j, (dz, L, rz, rx) in enumerate(((-1.4, 4.2, -30, -15), (0.2, 5.2, -42, 0), (1.6, 4.0, -55, 18), (-0.4, 3.0, -75, -10))):
        K.thorn(f"pthorn{j}_{k}", "chest", (x + 0.8 * s, 31.8, dz), L, 1.1, rx, rz * s, BLK, GREY)
    m.cube("collarplate_" + k, "chest", (1.0 * s - 1.6, 30.6, -2.4), (1.0 * s + 1.6, 32.0, -1.9), BLK, origin=(1.0 * s, 31.3, -2.1), rot=(0, 0, 20 * s), faces=af(armourp))

# fur mane / hood collar: big pale ruff around the neck + shoulders
m.cube("ruff", "mane", (-4.4, 30.4, -2.2), (4.4, 34.6, 3.4), FUR, faces=af(furp()))
for i in range(12):
    a = math.radians(i * 30)
    x, z = math.sin(a) * 4.0, 0.6 - math.cos(a) * 2.9
    K.plane(f"ruftuft{i}", "mane", (x, 31.6, z), 2.2, 3.6, K.pointed(furp(), 5), rot=(-20 * math.cos(a), -math.degrees(a), 0))
for i, (x, y, z, L, rz, rx) in enumerate(((4.0, 33.4, 0.4, 3.4, -70, 0), (-4.0, 33.4, 0.4, 3.4, 70, 0), (3.2, 34.2, 2.2, 3.0, -50, 30), (-3.2, 34.2, 2.2, 3.0, 50, 30), (0, 34.6, 3.0, 3.2, 0, 50))):
    K.thorn(f"manespk{i}", "mane", (x, y, z), L, 1.6, rx, rz, FUR, FUR_D)

# fur cloak hanging down the back, jagged hem
m.cube("cloak_main", "cloak", (-4.6, 13.0, 2.0), (4.6, 31.8, 2.9), FUR, origin=(0, 31.5, 2.4), rot=(-8, 0, 0),
       faces={"south": K.jagged(furp(), 3, 1.4), "north": K.jagged(furp(FUR_D), 3, 1.4), "east": furp(), "west": furp(), "up": furp(), "down": clear})
for s, k in ((1, "r"), (-1, "l")):
    m.cube("cloakside_" + k, "cloak_" + k, (3.6 * s - 0.4, 15.0, -0.4), (3.6 * s + 0.4, 31.0, 2.6), FUR_D, origin=(3.6 * s, 31.0, 1.4), rot=(0, 0, 10 * s),
           faces={"east": K.jagged(furp(FUR_D), 2, 1.4), "west": K.jagged(furp(FUR_D), 2, 1.4), "north": furp(), "south": furp(), "up": furp(), "down": clear})
for i in range(5):
    K.plane(f"hemtuft{i}", "cloak", (-3.6 + i * 1.8, 14.6, 3.0 + 0.3 * i % 2), 2.0, 3.4, K.pointed(furp(FUR_D), 5), rot=(-12, 0, (i - 2) * 9))

# ------------------------------------------------------------------ arms (long, black, thorny) + claws + heart
for s, k in ((1, "r"), (-1, "l")):
    x = 5.0 * s
    m.cube("upper_" + k, "arm_" + k, (x - 1.0, 23.0, -1.0), (x + 1.0, 30.4, 1.0), BLK, faces=af(armp))
    m.cube("elbow_" + k, "fore_" + k, (x - 1.1, 22.0, -1.1), (x + 1.1, 23.8, 1.1), BLK_L, faces=af(armourp))
    K.thorn("elbowspike_" + k, "fore_" + k, (x, 23.0, 1.0), 2.4, 0.8, 120, 0, BLK, GREY)
    m.cube("fore_c_" + k, "fore_" + k, (x - 0.9, 16.2, -0.9), (x + 0.9, 23.2, 0.9), BLK, faces=af(armp))
    m.cube("wrist_" + k, "fore_" + k, (x - 1.0, 16.6, -1.0), (x + 1.0, 17.6, 1.0), BAND_D, origin=(x, 17.1, 0), rot=(0, 0, 10 * s), faces=af(flat(BAND_D)))
    for j in range(2):
        K.thorn(f"forethorn{j}_{k}", "fore_" + k, (x + 0.8 * s, 19 + j * 2.4, 0), 1.6, 0.6, 0, -70 * s, BLK, GREY)
    m.cube("palm_" + k, "hand_" + k, (x - 1.1, 14.6, -1.1), (x + 1.1, 16.8, 1.1), BLK_L, faces=af(armp))
# RIGHT: very long hooked black claws (two-segment fingers)
for f in range(4):
    fz = -0.9 + f * 0.6
    fx = 5.0 + (0.5 if f in (0, 3) else 0.0) - 0.25
    tipy = 15.2 - 7.0
    m.cube(f"claw{f}", "claws_r", (fx - 0.22, tipy, fz - 0.22), (fx + 0.22, 15.2, fz + 0.22), BLK, origin=(fx, 15.2, fz), rot=(-8 + f * 4, 0, 4),
           faces=af(K.grad(BLK_L, BLK_D)))
    m.cube(f"clawtip{f}", "claws_r", (fx - 0.16, tipy - 3.0, fz - 0.16 - 0.5), (fx + 0.16, tipy + 0.2, fz + 0.16 - 0.5), GREY, origin=(fx, tipy, fz), rot=(-26 + f * 4, 0, 4),
           faces=af(K.grad(BLK, GREY)))
m.cube("thumbclaw", "claws_r", (4.0 - 0.2, 12.2, -1.2), (4.0 + 0.2, 15.4, -0.8), BLK, origin=(4.2, 15.2, -1.0), rot=(-20, 0, -18), faces=af(K.grad(BLK_L, BLK_D)))
# LEFT: shorter claws wrapped around the heart
for f in range(3):
    fz = -1.6 + f * 0.9
    m.cube(f"lclaw{f}", "hand_l", (-5.0 - 0.2, 12.4, fz - 0.2), (-5.0 + 0.2, 15.0, fz + 0.2), BLK, origin=(-5.0, 15.0, fz), rot=(-30 + f * 30, 0, -14), faces=af(K.grad(BLK_L, BLK_D)))
# the bloody claw-heart: red-black crystal cluster, dripping
m.cube("heart_core", "heart", (-6.6, 12.0, -2.6), (-3.4, 15.6, 0.8), RED, faces=af(heartp))
for i, (dx, dy, dz, L, rx, rz) in enumerate(((0, 1.2, 0, 2.6, -30, 20), (-1.2, 0.6, -0.6, 2.4, -10, 55), (1.0, 0.4, -0.4, 2.2, 10, -50), (0, -1.6, -0.8, 2.0, 160, 10), (-0.6, 1.4, 0.8, 2.4, 35, 25), (0.9, -0.4, 1.0, 1.8, 120, -40))):
    K.thorn(f"heartshard{i}", "heart", (-5.0 + dx, 13.8 + dy, -0.9 + dz), L, 1.0, rx, rz, RED_D if i % 2 else BLK, RED)
for i, (dx, dz, L) in enumerate(((-0.8, -1.0, 2.4), (0.6, -0.4, 3.4), (-0.2, 0.4, 1.6))):
    m.cube(f"drip{i}", "heart", (-5.0 + dx - 0.15, 12.0 - L, -0.9 + dz - 0.15), (-5.0 + dx + 0.15, 12.1, -0.9 + dz + 0.15), RED, faces=af(K.grad(RED, RED_D)))
    m.cube(f"dripb{i}", "heart", (-5.0 + dx - 0.25, 12.0 - L - 0.5, -0.9 + dz - 0.25), (-5.0 + dx + 0.25, 12.0 - L, -0.9 + dz + 0.25), RED_D, faces=af(flat(RED_D)))
# thrown thorn shards (prop in the right claw)
for i in range(3):
    K.thorn(f"shardp{i}", "shard", (5.0 + (i - 1) * 0.6, 14.2, -0.6), 3.6, 0.9, 170, (i - 1) * 18, BLK, GREY)

# ------------------------------------------------------------------ head: pale face, fur hood with spikes, antlers
m.cube("skull", "head", (-2.7, 33.4, -3.0), (2.7, 39.2, 2.4), FACE, faces={"north": face_front, "south": furp(), "east": faceside, "west": faceside, "up": furp(), "down": faceside})
m.cube("jawc", "jaw", (-2.3, 33.0, -3.1), (2.3, 34.4, -0.4), FACE_D, faces={"north": K.combo(flat(FACE_D), lambda F: [F.px(x, 0, 0xFFFFFF) for x in range(0, F.w, 2)]), "south": flat(FACE_D), "east": flat(FACE_D), "west": flat(FACE_D), "up": flat(BLK_D), "down": flat(FACE_D)})
m.cube("hood_c", "hood", (-3.3, 35.2, -2.4), (3.3, 40.2, 3.2), FUR, faces=af(furp(), ("north",)) | {"north": clear})
for s, k in ((1, "r"), (-1, "l")):   # spiky fur framing the face (art: pale shaggy points flaring out)
    for j, (y, z, L, rz, rx) in enumerate(((39.6, -1.6, 3.6, -40, -10), (38.4, -2.4, 3.2, -70, -20), (36.6, -2.0, 3.6, -100, -10), (34.6, -1.0, 3.0, -125, 0), (40.2, 1.0, 3.0, -25, 25))):
        K.thorn(f"hoodspk{j}_{k}", "hood", (2.6 * s, y, z), L, 1.7, rx, rz * s, FUR, FUR_D)
    K.thorn(f"ear_{k}", "hood", (2.2 * s, 39.6, 0.6), 3.4, 1.4, 10, -24 * s, FUR_D, FUR_DD)
for j, (x, z, L, rx) in enumerate(((-1.2, -2.6, 2.4, -40), (0.6, -2.7, 2.8, -38), (1.8, -2.5, 2.0, -45))):   # forelock spikes over the brow
    K.thorn(f"forelock{j}", "hood", (x, 40.0, z), L, 1.3, 180 + rx, 0, FUR_L, FUR_D)
# antlers: big, black, branching up and out
for s, k in ((1, "r"), (-1, "l")):
    g = "antler_" + k
    p0 = (1.6 * s, 39.0, 0.2)
    p1 = K.seg(f"ab0_{k}", g, p0, 4.0, 1.1, 10, -30 * s, ANT, K.bark(ANT, ANT_L, BLK_D))
    p2 = K.seg(f"ab1_{k}", g, p1, 4.2, 0.95, 4, -8 * s, ANT, K.bark(ANT, ANT_L, BLK_D))
    p3 = K.seg(f"ab2_{k}", g, p2, 3.6, 0.8, -4, 14 * s, ANT, K.bark(ANT, ANT_L, BLK_D))
    K.seg(f"ab3_{k}", g, p3, 2.6, 0.6, -8, 30 * s, ANT)
    K.seg(f"at0_{k}", g, p1, 3.4, 0.7, -12, -68 * s, ANT)
    t1 = K.seg(f"at1_{k}", g, p2, 3.2, 0.65, -24, -52 * s, ANT)
    K.seg(f"at1b_{k}", g, t1, 1.6, 0.45, -12, -20 * s, ANT)
    K.seg(f"at2_{k}", g, p3, 2.4, 0.55, 18, -44 * s, ANT)
    K.seg(f"at3_{k}", g, p2, 2.2, 0.55, 40, -10 * s, ANT)
    K.seg(f"at4_{k}", g, Kit.tip(p0, 1.6, 10, -30 * s), 2.0, 0.6, -38, 6 * s, ANT)

# ------------------------------------------------------------------ the huge fluffy tail (segments for sway), curling out to his right
TAILP = {"north": furp(), "south": furp(), "east": furp(), "west": furp(), "up": furp(), "down": furp(FUR_D)}
m.cube("tail0c", "tail", (-1.6 + 0.6, 18.6, 1.8), (1.6 + 0.6, 22.6, 7.6), FUR, faces=TAILP)
m.cube("tail1c", "tail1", (-2.8 + 0.6, 17.4, 7.0), (2.8 + 0.6, 23.6, 14.4), FUR, faces=TAILP)
m.cube("tail2c", "tail2", (-3.0 + 0.6, 17.2, 13.6), (3.0 + 0.6, 23.8, 20.2), FUR, faces=TAILP)
m.cube("tail3c", "tail3", (-2.2 + 0.6, 18.0, 19.4), (2.2 + 0.6, 23.2, 24.4), FUR_L, faces=af(furp(FUR_L)))
for i, (g, z, L) in enumerate((("tail1", 10.6, 3.2), ("tail2", 16.6, 3.4), ("tail3", 22.0, 2.6))):
    for s in (1, -1):
        K.thorn(f"tailfluff{i}_{'r' if s > 0 else 'l'}", g, (0.6 + 2.2 * s, 20.6, z), L, 2.6, 0, -80 * s, FUR, FUR_D)
    K.thorn(f"tailtop{i}", g, (0.6, 22.6, z), L * 0.8, 2.4, 20, 0, FUR_L, FUR_D)
K.thorn("tailtip", "tail3", (0.6, 20.6, 24.0), 3.0, 2.4, 90, 0, FUR_L, FUR_D)


# ================================================================== animation
PROPS = ("shard",)


def NA(name, ticks, loop=False):
    return A(m, name, ticks, loop, PROPS)


def legs(a, kr, kl=None, sr=None, sl=None):
    a.r("leg_r", *kr)
    a.r("leg_l", *(kl or [(t, x, -y, -z) for (t, x, y, z) in kr]))
    if sr: a.r("shin_r", *sr)
    if sl or sr: a.r("shin_l", *(sl or sr))


def fur(a, keys, delay=2):
    """secondary motion: keys (t, x, _, z) x>0 = body thrown forward (fur flung back), z = sideways swing"""
    a.lag("cloak", [(t, -x * 0.9, 0, z * 0.3) for (t, x, y, z) in keys], delay + 1)
    a.lag("cloak_r", [(t, -x * 0.4, 0, z * 0.4 + abs(x) * 0.3) for (t, x, y, z) in keys], delay + 2)
    a.lag("cloak_l", [(t, -x * 0.4, 0, z * 0.4 - abs(x) * 0.3) for (t, x, y, z) in keys], delay + 2)
    a.lag("hood", [(t, -x * 0.15, 0, z * 0.2) for (t, x, y, z) in keys], delay)
    a.lag("mane", [(t, -x * 0.1, 0, z * 0.15) for (t, x, y, z) in keys], delay)
    a.wave(("tail", "tail1", "tail2", "tail3"), [(t, -x * 0.5, z * 0.8, 0) for (t, x, y, z) in keys], 1.5)
    return a


# ------------------------------------------------------------------ idle (80 loop): hunched breathing, heart pulses, claws twitch, tail swishes
a = NA("idle", 80, loop=True)
a.pos("body", (0, 0, 0, 0), (20, 0, -0.3, 0), (40, 0, 0, 0), (60, 0, -0.3, 0), (80, 0, 0, 0))
a.rot("chest", (0, 0, 0, 0), (20, 2, 3, 0), (40, 0, 0, 0), (60, 2, -3, 0), (80, 0, 0, 0))
a.rot("head", (0, 0, 0, 6), (24, -2, 6, 10), (40, 0, 0, 6), (64, -2, -6, 2), (80, 0, 0, 6))
a.rot("arm_r", (0, 4, 0, 3), (40, 8, 0, 5), (80, 4, 0, 3))
a.rot("fore_r", (0, 10, 0, 0), (40, 14, 0, 0), (80, 10, 0, 0))
a.rot("hand_r", (0, 0, 0, 0), (50, 0, 0, 0), (53, -16, 0, 0), (56, 6, 0, 0), (59, -12, 0, 0), (62, 0, 0, 0), (80, 0, 0, 0))
a.rot("arm_l", (0, 30, 0, -4), (40, 34, 0, -6), (80, 30, 0, -4))
a.rot("fore_l", (0, 40, 0, 0), (40, 44, 0, 0), (80, 40, 0, 0))
a.scl("heart", (0, 1, 1, 1), (4, 1.15, 1.15, 1.15), (7, 1, 1, 1), (10, 1.1, 1.1, 1.1), (14, 1, 1, 1), (44, 1, 1, 1), (48, 1.15, 1.15, 1.15), (51, 1, 1, 1), (54, 1.1, 1.1, 1.1), (58, 1, 1, 1), (80, 1, 1, 1))
a.rot("leg_r", (0, -4, 0, 2), (80, -4, 0, 2))
a.rot("leg_l", (0, 6, 0, -2), (80, 6, 0, -2))
a.rot("shin_l", (0, -8, 0, 0), (80, -8, 0, 0))
for b, ph, amp in (("tail", 0, (3, 8, 0)), ("tail1", 6, (3, 10, 0)), ("tail2", 12, (4, 12, 0)), ("tail3", 18, (4, 14, 0)),
                   ("cloak", 5, (-2, 0, 1)), ("cloak_r", 15, (0, 0, 2)), ("cloak_l", 30, (0, 0, -2)), ("hood", 20, (1, 0, 1.5)), ("antler_r", 30, (0, 0, 0.6)), ("antler_l", 30, (0, 0, -0.6))):
    a.rot(b, *sinekeys(80, 10, amp, ph))
a.done()

# ------------------------------------------------------------------ walk (24 loop): long stalking strides, low hunch, claws dragging, tail swaying
a = NA("walk", 24, loop=True)
a.pos("body", (0, 0, 0, 0), (6, 0, 0.7, 0), (12, 0, 0, 0), (18, 0, 0.7, 0), (24, 0, 0, 0))
a.rot("body", (0, -6, 6, 0), (6, -8, 0, 2), (12, -6, -6, 0), (18, -8, 0, -2), (24, -6, 6, 0))
a.rot("chest", (0, -4, -5, 0), (12, -4, 5, 0), (24, -4, -5, 0))
a.rot("leg_r", (0, 32, 0, 0), (6, 0, 0, 0), (12, -30, 0, 0), (18, 0, 0, 0), (24, 32, 0, 0))
a.rot("leg_l", (0, -30, 0, 0), (6, 0, 0, 0), (12, 32, 0, 0), (18, 0, 0, 0), (24, -30, 0, 0))
a.rot("shin_r", (0, 0, 0, 0), (14, -46, 0, 0), (19, -16, 0, 0), (24, 0, 0, 0))
a.rot("shin_l", (0, 0, 0, 0), (2, -46, 0, 0), (7, -16, 0, 0), (12, 0, 0, 0), (24, 0, 0, 0))
a.rot("arm_r", (0, -22, 0, 4), (12, 26, 0, 6), (24, -22, 0, 4))
a.rot("fore_r", (0, 8, 0, 0), (12, 24, 0, 0), (24, 8, 0, 0))
a.rot("arm_l", (0, 40, 0, -4), (12, 24, 0, -6), (24, 40, 0, -4))
a.rot("fore_l", (0, 40, 0, 0), (12, 46, 0, 0), (24, 40, 0, 0))
a.rot("head", (0, 6, 0, -3), (6, 4, 0, 0), (12, 6, 0, 3), (18, 4, 0, 0), (24, 6, 0, -3))
a.rot("tail", (0, 6, 10, 0), (12, 6, -10, 0), (24, 6, 10, 0))
a.rot("tail1", (0, 2, 6, 0), (4, 2, 12, 0), (16, 2, -12, 0), (24, 2, 6, 0))
a.rot("tail2", (0, 0, 0, 0), (6, 0, 14, 0), (18, 0, -14, 0), (24, 0, 0, 0))
a.rot("tail3", (0, 0, -6, 0), (8, 0, 16, 0), (20, 0, -16, 0), (24, 0, -6, 0))
a.rot("cloak", (0, -8, 0, 2), (6, -5, 0, 0), (12, -8, 0, -2), (18, -5, 0, 0), (24, -8, 0, 2))
a.rot("cloak_r", (0, -3, 0, 4), (12, -3, 0, 1), (24, -3, 0, 4))
a.rot("cloak_l", (0, -3, 0, -1), (12, -3, 0, -4), (24, -3, 0, -1))
a.done()

# ------------------------------------------------------------------ claw_rake (30): right claw cocked high 0-8, DOWNWARD rake t11, wind under, rising backhand t19, recover
a = NA("claw_rake", 30)
a.r("chest", (6, 6, 30, -6), (8, 8, 34, -8), (11, -14, -30, 6), (13, -14, -34, 6), (16, -4, -20, 0), (19, -6, 30, 4), (21, -4, 34, 4), (26, 0, 0, 0))
a.r("head", (8, 4, -20, 6), (11, -8, 16, -4), (16, 0, 10, 0), (19, -4, -18, 0), (26, 0, 0, 0))
a.r("arm_r", (5, 150, 20, 40), (8, 170, 20, 46), (10, 90, 0, 10), (11, 40, -20, -10), (13, 20, -30, -20), (16, 30, -40, -40), (18, 70, -10, -10), (19, 120, 30, 50), (21, 140, 30, 60), (25, 30, 0, 10), (30, 0, 0, 0))
a.r("fore_r", (8, 50, 0, 0), (11, 0, 0, 0), (16, 60, 0, 0), (19, 0, 0, 0), (24, 20, 0, 0))
a.r("hand_r", (8, -30, 0, 0), (11, 30, 0, 0), (16, -20, 0, 0), (19, 30, 0, 0), (24, 0, 0, 0))
a.r("arm_l", (8, 10, 0, -30), (11, 40, 0, -14), (19, 20, 0, -30), (26, 0, 0, 0))
a.p("body", (6, 0, -0.4, 0.8), (8, 0, -0.6, 1.0), (11, 0, -1.2, -2.2), (16, 0, -0.8, -1.6), (19, 0, -0.4, -2.6), (24, 0, -0.2, -0.8), (28, 0, 0, 0))
legs(a, [(6, 10, 0, 0), (11, -30, 0, 0), (16, -20, 0, 0), (19, -26, 0, 0), (26, 0, 0, 0)], [(6, -8, 0, 0), (11, 24, 0, 0), (19, 18, 0, 0), (26, 0, 0, 0)],
     sr=[(11, -14, 0, 0), (19, -10, 0, 0), (26, 0, 0, 0)], sl=[(11, -30, 0, 0), (19, -24, 0, 0), (26, 0, 0, 0)])
fur(a, [(0, 0, 0, 0), (8, -6, 0, -10), (11, 14, 0, 14), (16, 4, 0, 4), (19, 12, 0, -14), (26, 0, 0, 0)], 1)
a.done()

# ------------------------------------------------------------------ antler_charge (34): paw + head lowered 0-9, burst t10, gallop low through 12-20 (antlers forward), skid + toss 20-24, recover
a = NA("antler_charge", 34)
a.r("chest", (4, -10, 0, 0), (8, -26, 0, 0), (10, -40, 0, 0), (14, -44, 0, 0), (18, -42, 0, 0), (20, -20, 0, 0), (22, 4, 0, 0), (26, -6, 0, 0), (32, 0, 0, 0))
a.r("head", (4, -10, 0, 0), (8, -30, 0, 0), (10, -36, 0, 0), (18, -36, 0, 0), (20, -10, 0, 0), (22, 24, 0, 0), (26, 4, 0, 0), (32, 0, 0, 0))
a.r("arm_r", (6, -30, 0, 10), (10, -60, 0, 20), (14, -50, 0, 24), (18, -60, 0, 20), (22, 20, 0, 30), (28, 0, 0, 0))
a.r("arm_l", (6, -20, 0, -10), (10, -50, 0, -20), (14, -40, 0, -24), (18, -50, 0, -20), (22, 30, 0, -20), (28, 0, 0, 0))
a.p("body", (8, 0, -1.6, 1.4), (10, 0, -2.0, -1.0), (14, 0, -1.4, -2.0), (18, 0, -1.8, -2.0), (20, 0, -1.0, -1.0), (22, 0, 0.4, 0), (28, 0, 0, 0))
legs(a, [(2, 0, 0, 0), (4, 30, 0, 0), (6, 0, 0, 0), (8, -20, 0, 0), (11, 50, 0, 0), (13, -40, 0, 0), (15, 50, 0, 0), (17, -40, 0, 0), (19, 40, 0, 0), (22, -10, 0, 0), (28, 0, 0, 0)],
     [(8, 30, 0, 0), (11, -40, 0, 0), (13, 50, 0, 0), (15, -40, 0, 0), (17, 50, 0, 0), (19, -30, 0, 0), (22, 20, 0, 0), (28, 0, 0, 0)],
     sr=[(4, -40, 0, 0), (6, 0, 0, 0), (11, -20, 0, 0), (13, -60, 0, 0), (15, -20, 0, 0), (17, -60, 0, 0), (20, -10, 0, 0), (26, 0, 0, 0)],
     sl=[(8, -30, 0, 0), (11, -60, 0, 0), (13, -20, 0, 0), (15, -60, 0, 0), (17, -20, 0, 0), (20, -40, 0, 0), (26, 0, 0, 0)])
a.r("antler_r", (10, 0, 0, 6), (20, 0, 0, 6), (22, 0, 0, -4), (26, 0, 0, 0))
a.r("antler_l", (10, 0, 0, -6), (20, 0, 0, -6), (22, 0, 0, 4), (26, 0, 0, 0))
fur(a, [(0, 0, 0, 0), (10, 20, 0, 0), (18, 22, 0, 0), (22, -14, 0, 0), (28, 2, 0, 0), (32, 0, 0, 0)], 1)
a.done()

# ------------------------------------------------------------------ thorn_throw (32): shards bloom in the right claw 3-8, sidearm fling t11, reload 14-17, overhand fling t20, recover
a = NA("thorn_throw", 32)
a.show("shard", 3, 21, grow=2)
a.s("shard", (11, 1, 1, 1), (12, 0.2, 0.2, 0.2), (14, 0.3, 0.3, 0.3), (17, 1.1, 1.1, 1.1), (18, 1, 1, 1))
a.r("chest", (6, 0, 40, 0), (9, 0, 44, 0), (11, -6, -30, 0), (13, -6, -24, 0), (17, 10, 20, 0), (20, -16, -14, 0), (23, -12, -10, 0), (28, 0, 0, 0))
a.r("head", (8, 0, -24, 0), (11, -4, 20, 0), (17, 6, -10, 0), (20, -8, 10, 0), (27, 0, 0, 0))
a.r("arm_r", (4, 20, 30, 60), (8, 10, 40, 90), (10, 70, 0, 60), (11, 90, -30, 30), (13, 70, -30, 10), (16, 140, 0, 30), (18, 170, 0, 20), (20, 100, 0, 0), (21, 70, 0, -6), (24, 40, 0, 0), (30, 0, 0, 0))
a.r("fore_r", (8, 50, 0, 0), (11, 0, 0, 0), (17, 60, 0, 0), (20, 0, 0, 0), (26, 10, 0, 0))
a.r("hand_r", (8, -20, 0, 0), (11, 30, 0, 0), (18, -40, 0, 0), (20, 30, 0, 0), (26, 0, 0, 0))
a.r("arm_l", (8, 10, 0, -40), (11, 30, 0, -20), (18, 0, 0, -40), (20, 40, 0, -20), (28, 0, 0, 0))
a.p("body", (8, 0, -0.3, 1.0), (11, 0, -0.6, -1.4), (17, 0, -0.2, 0.6), (20, 0, -0.6, -1.6), (26, 0, 0, -0.3), (30, 0, 0, 0))
legs(a, [(8, 14, 0, 0), (11, -24, 0, 0), (17, 10, 0, 0), (20, -26, 0, 0), (28, 0, 0, 0)], [(8, -12, 0, 0), (11, 20, 0, 0), (17, -6, 0, 0), (20, 22, 0, 0), (28, 0, 0, 0)],
     sr=[(11, -10, 0, 0), (20, -12, 0, 0), (28, 0, 0, 0)], sl=[(11, -24, 0, 0), (20, -26, 0, 0), (28, 0, 0, 0)])
fur(a, [(0, 0, 0, 0), (8, -4, 0, -12), (11, 10, 0, 14), (17, -6, 0, -6), (20, 12, 0, 8), (28, 0, 0, 0)], 1)
a.done()

# ------------------------------------------------------------------ heart_pulse (40): heart lifted to the face 0-10, beats t12 / t22 / t32 (heart swells, body jolts, head snaps back), lowers
a = NA("heart_pulse", 40)
a.r("arm_l", (6, 110, -20, -10), (10, 150, -30, -20), (12, 160, -30, -24), (14, 150, -30, -20), (22, 162, -30, -24), (24, 150, -30, -20), (32, 165, -30, -26), (34, 150, -30, -20), (37, 60, 0, 0), (40, 0, 0, 0))
a.r("fore_l", (6, 40, 0, 0), (10, 20, 0, 0), (34, 20, 0, 0), (38, 30, 0, 0))
a.s("heart", (10, 1, 1, 1), (12, 1.6, 1.6, 1.6), (15, 1.05, 1.05, 1.05), (20, 1, 1, 1), (22, 1.75, 1.75, 1.75), (25, 1.05, 1.05, 1.05), (30, 1, 1, 1), (32, 1.9, 1.9, 1.9), (35, 1.1, 1.1, 1.1), (38, 1, 1, 1))
a.r("chest", (8, 10, -16, 0), (12, 18, -16, 0), (14, 8, -16, 0), (22, 20, -16, 0), (24, 8, -16, 0), (32, 22, -16, 0), (34, 8, -16, 0), (38, 0, 0, 0))
a.r("head", (8, 6, 20, 0), (12, 24, 20, 0), (14, 8, 20, 0), (22, 26, 20, 0), (24, 8, 20, 0), (32, 30, 20, 0), (34, 10, 20, 0), (38, 0, 0, 0))
a.r("jaw", (11, 0, 0, 0), (12, 26, 0, 0), (15, 6, 0, 0), (22, 30, 0, 0), (25, 6, 0, 0), (32, 34, 0, 0), (35, 0, 0, 0))
a.r("arm_r", (8, 10, 0, 40), (12, 0, 0, 60), (14, 10, 0, 40), (22, 0, 0, 62), (24, 10, 0, 40), (32, 0, 0, 66), (34, 10, 0, 40), (38, 0, 0, 0))
a.r("fore_r", (12, 30, 0, 0), (32, 30, 0, 0), (38, 0, 0, 0))
a.p("body", (8, 0, 0.3, 0), (12, 0, 0.8, 0.4), (14, 0, 0.2, 0), (22, 0, 0.9, 0.4), (24, 0, 0.2, 0), (32, 0, 1.0, 0.4), (34, 0, 0.2, 0), (38, 0, 0, 0))
legs(a, [(8, 0, 0, 6), (34, 0, 0, 6), (38, 0, 0, 0)])
fur(a, [(0, 0, 0, 0), (12, -8, 0, 4), (14, 2, 0, 0), (22, -8, 0, -4), (24, 2, 0, 0), (32, -10, 0, 4), (34, 2, 0, 0), (40, 0, 0, 0)], 1)
a.done()

# ------------------------------------------------------------------ tail_sweep (28): crouch + twist 0-8, full spin with the tail extended peaking t13, settle 16-28
a = NA("tail_sweep", 28)
a.r("root", (6, 0, -30, 0), (8, 0, -40, 0), (11, 0, 120, 0), (13, 0, 230, 0), (16, 0, 330, 0), (18, 0, 360, 0), (28, 0, 360, 0))
a.p("body", (6, 0, -1.2, 0), (8, 0, -1.6, 0), (13, 0, -0.6, 0), (18, 0, -1.0, 0), (24, 0, 0, 0))
a.r("tail", (6, 10, -30, 0), (10, 30, 30, 0), (13, 60, 40, 0), (16, 40, 20, 0), (20, -10, -14, 0), (26, 0, 0, 0))
a.r("tail1", (8, 0, -20, 0), (11, 16, 30, 0), (14, 20, 40, 0), (18, -6, -20, 0), (26, 0, 0, 0))
a.r("tail2", (9, 0, -24, 0), (12, 14, 30, 0), (15, 16, 40, 0), (19, -6, -24, 0), (26, 0, 0, 0))
a.r("tail3", (10, 0, -30, 0), (13, 10, 34, 0), (16, 10, 44, 0), (20, -6, -24, 0), (26, 0, 0, 0))
a.r("chest", (8, -10, 20, 0), (13, -20, -16, 0), (18, -10, -10, 0), (24, 0, 0, 0))
a.r("arm_r", (8, -20, 0, 50), (13, -10, 0, 80), (18, 0, 0, 40), (26, 0, 0, 0))
a.r("arm_l", (8, 10, 0, -40), (13, 0, 0, -80), (18, 10, 0, -40), (26, 0, 0, 0))
legs(a, [(6, -20, 0, 10), (13, -30, 0, 14), (18, -20, 0, 6), (24, 0, 0, 0)], [(6, 10, 0, -14), (13, 20, 0, -18), (18, 6, 0, -8), (24, 0, 0, 0)],
     sr=[(6, 30, 0, 0), (13, 40, 0, 0), (24, 0, 0, 0)], sl=[(6, -20, 0, 0), (13, -30, 0, 0), (24, 0, 0, 0)])
a.r("cloak_r", (11, -20, 0, 50), (16, -10, 0, 30), (22, 0, 0, 0))
a.r("cloak_l", (11, -20, 0, -50), (16, -10, 0, -30), (22, 0, 0, 0))
a.r("cloak", (11, -40, 0, 0), (16, -20, 0, 0), (22, 0, 0, 0))
a.done()

# ------------------------------------------------------------------ pounce_maul (44): deep crouch 0-9, LEAP t10 (airborne 10-16), slam both claws t16-17, pin, BITE t28, rise
a = NA("pounce_maul", 44)
a.p("root", (6, 0, -3.0, 1.0), (9, 0, -3.4, 1.4), (11, 0, 4.0, -2), (13, 0, 6.0, -4), (15, 0, 2.0, -6), (16, 0, -3.0, -6.5), (18, 0, -3.6, -6.6), (30, 0, -3.4, -6.6), (36, 0, -1.2, -6.6), (42, 0, 0, -6.6), (44, 0, 0, -6.6))
a.r("root", (9, 10, 0, 0), (11, -20, 0, 0), (13, -30, 0, 0), (16, 20, 0, 0), (18, 26, 0, 0), (26, 22, 0, 0), (28, 34, 0, 0), (32, 20, 0, 0), (40, 0, 0, 0))
a.r("chest", (9, -30, 0, 0), (11, 10, 0, 0), (14, 20, 0, 0), (16, -10, 0, 0), (26, -6, 0, 0), (28, -26, 0, 0), (32, -10, 0, 0), (40, 0, 0, 0))
a.r("head", (9, 20, 0, 0), (12, 10, 0, 0), (16, -10, 0, 0), (26, 10, 0, 0), (28, -30, 0, 0), (31, -20, 0, 0), (38, 0, 0, 0))
a.r("jaw", (24, 0, 0, 0), (26, 40, 0, 0), (28, 0, 0, 0), (30, 10, 0, 0), (33, 0, 0, 0))
for s, k in ((1, "r"), (-1, "l")):
    a.r("arm_" + k, (9, -40, 0, 30 * s), (11, 20, 0, 20 * s), (13, 160, 0, 20 * s), (15, 150, 0, 10 * s), (16, 80, 0, 6 * s), (18, 70, 0, 10 * s), (28, 80, 0, 14 * s), (34, 40, 0, 10 * s), (42, 0, 0, 0))
    a.r("fore_" + k, (11, 20, 0, 0), (13, 30, 0, 0), (16, 0, 0, 0), (34, 20, 0, 0), (42, 0, 0, 0))
legs(a, [(6, 50, 0, 0), (9, 60, 0, 0), (11, -30, 0, 0), (13, 30, 0, 0), (16, 60, 0, 0), (30, 60, 0, 0), (38, 20, 0, 0), (44, 0, 0, 0)], None,
     sr=[(6, -80, 0, 0), (9, -90, 0, 0), (11, 0, 0, 0), (13, -60, 0, 0), (16, -90, 0, 0), (30, -90, 0, 0), (38, -30, 0, 0), (44, 0, 0, 0)])
a.wave(("tail", "tail1", "tail2", "tail3"), [(0, 0, 0, 0), (9, -20, 0, 0), (12, 40, 0, 0), (16, -30, 0, 0), (20, 10, 0, 0), (28, -10, 0, 0), (36, 0, 0, 0)], 1.5)
fur(a, [(0, 0, 0, 0), (11, -16, 0, 0), (14, 10, 0, 0), (16, 20, 0, 0), (22, 4, 0, 0), (28, 10, 0, 0), (40, 0, 0, 0)], 1)
a.done()

# ------------------------------------------------------------------ blood_spikes (36): heart raised overhead 0-12, SLAMMED into the ground t15 (kneel), grind 16-24, rise
a = NA("blood_spikes", 36)
a.r("arm_l", (6, 140, 0, -20), (11, 175, 0, -10), (13, 120, 0, -6), (15, 30, 0, 0), (24, 30, 0, 0), (30, 10, 0, -4), (36, 0, 0, 0))
a.r("fore_l", (11, 20, 0, 0), (15, 0, 0, 0), (26, 0, 0, 0))
a.s("heart", (11, 1.2, 1.2, 1.2), (15, 1.5, 0.8, 1.5), (17, 1.1, 1.1, 1.1), (24, 1, 1, 1))
a.r("chest", (6, 14, 10, 0), (11, 20, 14, 0), (15, -46, -6, 0), (24, -40, -6, 0), (30, -10, 0, 0), (36, 0, 0, 0))
a.r("head", (11, 14, 0, 0), (15, -10, 0, 0), (17, 20, 0, 0), (24, 16, 0, 0), (32, 0, 0, 0))
a.r("jaw", (15, 0, 0, 0), (17, 30, 0, 0), (24, 20, 0, 0), (28, 0, 0, 0))
a.r("arm_r", (6, -10, 0, 50), (11, -20, 0, 60), (15, 40, 0, 30), (24, 40, 0, 30), (32, 0, 0, 0))
a.p("body", (11, 0, 0.6, 0.6), (15, 0, -4.6, -1.0), (24, 0, -4.4, -1.0), (30, 0, -1.2, -0.4), (36, 0, 0, 0))
legs(a, [(11, -6, 0, 0), (15, -70, 0, 0), (24, -70, 0, 0), (30, -20, 0, 0), (36, 0, 0, 0)], [(11, 6, 0, 0), (15, 40, 0, 0), (24, 40, 0, 0), (30, 10, 0, 0), (36, 0, 0, 0)],
     sr=[(15, 70, 0, 0), (24, 70, 0, 0), (30, 20, 0, 0), (36, 0, 0, 0)], sl=[(15, -100, 0, 0), (24, -100, 0, 0), (30, -30, 0, 0), (36, 0, 0, 0)])
fur(a, [(0, 0, 0, 0), (11, -10, 0, 0), (15, 24, 0, 0), (20, 8, 0, 0), (30, 0, 0, 0)], 1)
a.done()

# ------------------------------------------------------------------ howl (40): gather breath, chest swells 0-12, head THROWN back, jaw wide t16-32, claws spread, settle
a = NA("howl", 40)
a.r("chest", (6, -16, 0, 0), (12, -20, 0, 0), (16, 26, 0, 0), (30, 30, 0, 0), (34, 10, 0, 0), (40, 0, 0, 0))
a.r("head", (6, -10, 0, 0), (12, -14, 0, 0), (16, 44, 0, 0), (22, 48, 0, 4), (30, 46, 0, -4), (34, 10, 0, 0), (40, 0, 0, 0))
a.r("jaw", (14, 0, 0, 0), (16, 40, 0, 0), (30, 42, 0, 0), (34, 0, 0, 0))
a.s("chest", (12, 1.06, 1.04, 1.08), (16, 1, 1, 1))
for s, k in ((1, "r"), (-1, "l")):
    a.r("arm_" + k, (6, -20, 0, 10 * s), (12, -30, 0, 14 * s), (16, -30, 0, 70 * s), (30, -34, 0, 74 * s), (36, 0, 0, 10 * s), (40, 0, 0, 0))
    a.r("fore_" + k, (12, 40, 0, 0), (16, 10, 0, 0), (30, 10, 0, 0), (38, 0, 0, 0))
a.p("body", (12, 0, -0.8, 0.4), (16, 0, 0.6, 0), (30, 0, 0.6, 0), (36, 0, 0, 0))
legs(a, [(12, 10, 0, 6), (16, -6, 0, 10), (30, -6, 0, 10), (38, 0, 0, 0)], sr=[(12, -20, 0, 0), (16, 0, 0, 0)])
a.r("antler_r", (16, 0, 0, 4), (17, 0, 0, -2), (18, 0, 0, 3), (19, 0, 0, -1), (20, 0, 0, 2), (22, 0, 0, 0))
a.r("antler_l", (16, 0, 0, -4), (17, 0, 0, 2), (18, 0, 0, -3), (19, 0, 0, 1), (20, 0, 0, -2), (22, 0, 0, 0))
a.wave(("tail", "tail1", "tail2", "tail3"), [(0, 0, 0, 0), (12, 10, 0, 0), (16, -30, 0, 0), (30, -34, 0, 0), (38, 0, 0, 0)], 1.5)
fur(a, [(0, 0, 0, 0), (16, -14, 0, 0), (20, -10, 0, 6), (24, -12, 0, -6), (30, -10, 0, 0), (36, 0, 0, 0)], 1)
a.done()

# ------------------------------------------------------------------ heart_harvest (56): lunge t8, right claw IMPALES t12, holds victim up, carves t22 / t32 (heart squeezed - lifesteal), flings t44
a = NA("heart_harvest", 56)
a.r("arm_r", (6, -20, 0, 30), (8, 30, 0, 20), (11, 95, 0, 0), (12, 100, 0, 0), (16, 115, 0, 0), (20, 110, 0, 0), (22, 135, 0, -10), (26, 112, 0, 0), (30, 110, 0, 0), (32, 140, 0, -14), (36, 112, 0, 0), (42, 120, 30, 20), (44, 60, -40, -40), (47, 20, -40, -40), (54, 0, 0, 0))
a.r("fore_r", (8, 40, 0, 0), (12, 0, 0, 0), (20, 10, 0, 0), (22, -10, 0, 0), (30, 10, 0, 0), (32, -10, 0, 0), (42, 30, 0, 0), (44, 0, 0, 0), (52, 0, 0, 0))
a.r("hand_r", (12, 30, 0, 0), (22, 50, 0, 0), (26, 30, 0, 0), (32, 50, 0, 0), (40, 30, 0, 0), (46, 0, 0, 0))
a.r("arm_l", (8, 20, 0, -30), (12, 60, 0, -20), (20, 70, 0, -20), (22, 90, 20, -20), (26, 70, 0, -20), (32, 92, 20, -20), (36, 70, 0, -20), (46, 10, 0, -10), (54, 0, 0, 0))
a.s("heart", (20, 1, 1, 1), (22, 1.5, 1.5, 1.5), (25, 1, 1, 1), (32, 1.6, 1.6, 1.6), (35, 1, 1, 1))
a.r("chest", (6, 6, 20, 0), (8, -10, 10, 0), (12, -24, 0, 0), (20, -10, 0, 0), (22, -20, 6, 0), (26, -10, 0, 0), (32, -22, -6, 0), (40, 4, 20, 0), (44, -14, -34, 0), (48, -10, -20, 0), (54, 0, 0, 0))
a.r("head", (8, -6, 0, 0), (12, -10, 0, 0), (16, 10, 0, 6), (22, -10, 0, 0), (32, -14, 0, 0), (40, 10, -10, 0), (44, -10, 20, 0), (52, 0, 0, 0))
a.r("jaw", (12, 0, 0, 0), (14, 30, 0, 0), (18, 10, 0, 0), (22, 34, 0, 0), (26, 6, 0, 0), (32, 36, 0, 0), (36, 0, 0, 0))
a.p("body", (6, 0, -0.6, 1.0), (8, 0, -1.0, -1.0), (12, 0, -0.8, -2.6), (40, 0, -0.4, -2.0), (44, 0, -0.8, -3.2), (52, 0, 0, -0.4), (56, 0, 0, 0))
legs(a, [(6, 10, 0, 0), (12, -40, 0, 0), (40, -30, 0, 0), (44, -40, 0, 0), (52, 0, 0, 0)], [(6, -10, 0, 0), (12, 30, 0, 0), (40, 20, 0, 0), (44, 30, 0, 0), (52, 0, 0, 0)],
     sr=[(12, -16, 0, 0), (44, -16, 0, 0), (52, 0, 0, 0)], sl=[(12, -40, 0, 0), (44, -40, 0, 0), (52, 0, 0, 0)])
fur(a, [(0, 0, 0, 0), (8, 14, 0, 0), (12, 18, 0, 0), (22, 6, 0, 4), (32, 6, 0, -4), (40, -6, 0, 10), (44, 16, 0, -16), (52, 0, 0, 0)], 1)
a.done()

# ------------------------------------------------------------------ transform (90; this model shows 0-60): heart raised 0-14, CRUSHED into the chest t22, convulsions 22-50
# (bandages / fur shed), arching back with arms flung wide and swelling 50-60 -> premature model takes over at t60
a = NA("transform", 90)
a.r("arm_l", (8, 120, -20, -20), (14, 165, -20, -24), (18, 120, 40, -10), (22, 70, 70, 30), (34, 74, 70, 30), (40, 60, 60, 20), (50, 20, 0, -80), (60, 30, 0, -110), (90, 30, 0, -110))
a.r("fore_l", (14, 20, 0, 0), (22, 90, 0, 0), (40, 90, 0, 0), (50, 10, 0, 0), (90, 10, 0, 0))
a.s("heart", (14, 1.3, 1.3, 1.3), (20, 1.4, 1.4, 1.4), (22, 0.6, 0.6, 0.6), (24, 0.001, 0.001, 0.001), (90, 0.001, 0.001, 0.001))
a.r("arm_r", (8, 10, 0, 30), (22, 60, -40, -40), (26, 70, -40, -50), (34, 66, -40, -44), (40, 80, -40, -50), (50, 20, 0, 80), (60, 30, 0, 110), (90, 30, 0, 110))
a.r("chest", (8, 10, 0, 0), (14, 18, 0, 0), (22, -30, 0, 0), (26, -36, 8, 0), (28, -30, -8, 0), (30, -38, 6, 0), (32, -30, -6, 0), (36, -40, 0, 8), (40, -34, 0, -8), (44, -42, 0, 0), (50, 20, 0, 0), (60, 34, 0, 0), (90, 34, 0, 0))
a.r("head", (14, 20, 0, 0), (22, -20, 0, 0), (26, -10, 20, 10), (30, -14, -20, -10), (34, -6, 24, 6), (38, -16, -20, -6), (44, -30, 0, 0), (50, 40, 0, 0), (60, 50, 0, 0), (90, 50, 0, 0))
a.r("jaw", (20, 0, 0, 0), (22, 30, 0, 0), (26, 10, 0, 0), (30, 30, 0, 0), (40, 20, 0, 0), (50, 44, 0, 0), (90, 44, 0, 0))
a.p("body", (14, 0, 0.4, 0), (22, 0, -2.4, 0), (44, 0, -3.0, 0), (50, 0, 0.8, 0), (60, 0, 1.2, 0), (90, 0, 1.2, 0))
a.s("body", (40, 1, 1, 1), (50, 1.08, 1.08, 1.08), (56, 1.18, 1.2, 1.18), (60, 1.3, 1.32, 1.3), (90, 1.3, 1.32, 1.3))
legs(a, [(22, -40, 0, 8), (44, -44, 0, 10), (50, -6, 0, 12), (60, 0, 0, 14), (90, 0, 0, 14)], None,
     sr=[(22, 50, 0, 0), (44, 56, 0, 0), (50, 0, 0, 0), (90, 0, 0, 0)])
a.r("antler_r", (26, 0, 0, 6), (28, 0, 0, -4), (30, 0, 0, 6), (32, 0, 0, -4), (50, 0, 0, 12), (90, 0, 0, 12))
a.r("antler_l", (26, 0, 0, -6), (28, 0, 0, 4), (30, 0, 0, -6), (32, 0, 0, 4), (50, 0, 0, -12), (90, 0, 0, -12))
a.wave(("tail", "tail1", "tail2", "tail3"), [(0, 0, 0, 0), (22, 30, 20, 0), (28, 10, -20, 0), (34, 30, 20, 0), (40, 10, -20, 0), (50, -40, 0, 0), (60, -50, 0, 0), (90, -50, 0, 0)], 1.2)
a.r("cloak", (22, -20, 0, 0), (40, -30, 0, 0), (50, -60, 0, 0), (60, -70, 0, 0), (90, -70, 0, 0))
a.r("cloak_r", (40, -10, 0, 30), (60, -20, 0, 60), (90, -20, 0, 60))
a.r("cloak_l", (40, -10, 0, -30), (60, -20, 0, -60), (90, -20, 0, -60))
a.done()

# ------------------------------------------------------------------ death (40, scrubbed by death 0..1): heart slips and drops, knees buckle, topples forward onto the claws
a = NA("death", 40)
a.r("arm_l", (6, 40, 0, -20), (10, -10, 0, -30), (40, -10, 0, -30))
a.p("heart", (6, 0, 0, 0), (12, 0, -6, -1), (14, 0, -5.4, -1), (40, 0, -5.4, -1))
a.r("heart", (12, 40, 0, 30), (40, 40, 0, 30))
a.r("chest", (4, 20, 0, 0), (10, 30, 0, 8), (18, -20, 0, 0), (28, -40, 0, 0), (40, -40, 0, 0))
a.r("head", (4, 30, 0, 0), (10, 20, 10, 10), (18, -10, 0, 20), (40, -10, 0, 24))
a.r("jaw", (4, 30, 0, 0), (40, 24, 0, 0))
legs(a, [(10, -10, 0, 0), (18, -80, 0, 4), (40, -84, 0, 4)], [(10, 10, 0, 0), (18, -80, 0, -4), (40, -84, 0, -4)], sr=[(18, 100, 0, 0), (40, 100, 0, 0)])
a.p("root", (10, 0, 0, 0), (18, 0, -5, 0), (26, 0, -3, -4), (40, 0, -2.6, -6))
a.r("root", (18, 0, 0, 0), (28, -70, 0, 0), (32, -84, 0, 0), (36, -80, 0, 0), (40, -82, 0, 0))
a.r("arm_r", (10, 40, 0, 40), (24, 120, 0, 20), (40, 130, 0, 30))
a.wave(("tail", "tail1", "tail2", "tail3"), [(0, 0, 0, 0), (18, 20, 20, 0), (30, -20, 30, 0), (40, -24, 30, 0)], 2)
a.done()

m.save(ROOT + "lord_hansel.bbmodel")
print("cubes", len(m.cubes), "anims", len(m.anims))
