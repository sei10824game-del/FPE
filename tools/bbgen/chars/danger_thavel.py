"""Danger Thavel (DANGER AU Miss Thavel, "the bomb") - generates assets/fpe/bbmodels/danger_thavel.bbmodel.
Reference: docs/ref/confirmed/danger_thavel.jpg - very long spiky dark-purple hair, orange/brown/cream striped knit beanie with a
black antenna ending in a square spiral, white face with a glowing orange triangle eye + huge shark grin, bangs over the other eye,
cropped orange jacket (high collar, black frog clasps, wide cuffs), shell bandolier, bandaged midriff, brown belt + hip bag with a
warning triangle, long peach-orange skirt, black gloves, pineapple grenade in the left hand, striped socks, tall pointed black boots.
Blockbench space: Y up, ground 0, faces -Z. Character's RIGHT = +X.
Rotation cheat-sheet (file values): arm/leg rx>0 = swing forward, torso/head rx>0 = lean back / look up,
ry>0 = turn to the character's left, rz>0 = hanging part swings toward +X (character's right).
Run: python3 tools/bbgen/chars/danger_thavel.py
"""
import math, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from bbgen import Model, mix  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "../../../src/main/resources/assets/fpe/bbmodels/danger_thavel.bbmodel")

# ------------------------------------------------------------------ palette
HAIR, HAIR_HI, HAIR_D = 0x3B2457, 0x5C3C82, 0x1E1230
SKIN, SKIN_D = 0xF3EFE9, 0xC6BFCB
JACK, JACK_D, JACK_L = 0xEE8A3A, 0xBF5E1E, 0xF9B068
SKIRT, SKIRT_D, SKIRT_L = 0xF2AE62, 0xC97C38, 0xFAD09A
HAT_O, HAT_B, HAT_C = 0xE9792E, 0x8C3A1E, 0xF6C27A
BLACK, BLACK_L = 0x1B1724, 0x363145
BROWN, BROWN_D, BROWN_L = 0x8A4426, 0x5A2A16, 0xB4683C
SHELL, SHELL_D, BRASS = 0xEB9A3E, 0xA65822, 0xE8C468
BAND, BAND_D = 0xF2EEE6, 0xBDB4A8
HAZ = 0xF6C51E
NADE, NADE_D, NADE_L = 0x6E5C2C, 0x43381A, 0x93803F
STEEL, STEEL_D = 0x8A8E98, 0x4A4C55
SOCK_C = 0xEBDDBA
MOUTH, TEETH, LIP = 0x2B0C14, 0xFAF6F2, 0x1A1018
EYE, EYE_D = 0xFF8A1E, 0xB2420C
F_CORE, F_MID, F_OUT = 0xFFF2B0, 0xFFB028, 0xFF5A14
SMOKE, SMOKE_D = 0x8A8790, 0x55525C
LAUNCH, LAUNCH_D = 0x5E6B3A, 0x3A4424

m = Model("danger_thavel", S=8, atlas=2048)
R = m.rng


# ------------------------------------------------------------------ painters
def strands(base, hi, dark, every=3):
    def f(F):
        cols = [R.random() for _ in range(F.w)]
        for x in range(F.w):
            c = base
            if cols[x] > 0.78: c = hi
            elif cols[x] < 0.22: c = dark
            for y in range(F.h):
                t = y / max(1, F.h - 1)
                cc = mix(c, dark, 0.35 * abs(t - 0.4))
                if (x + int(y / 7)) % every == 0 and R.random() < 0.5:
                    cc = mix(cc, hi, 0.4)
                F.px(x, y, cc)
    return f


HS = strands(HAIR, HAIR_HI, HAIR_D)
HS2 = strands(HAIR, HAIR_HI, HAIR_D, 2)


def all_faces(fn, skip=()):
    return {k: fn for k in ("north", "south", "east", "west", "up", "down") if k not in skip}


def combo(*fns):
    def f(F):
        for fn in fns: fn(F)
    return f


def hstripe(c, y0, h):
    return lambda F: F.rect(0, y0, F.w, h, c)


def frame(c):
    def f(F):
        F.rect(0, 0, F.w, 1, c); F.rect(0, F.h - 1, F.w, 1, c); F.rect(0, 0, 1, F.h, c); F.rect(F.w - 1, 0, 1, F.h, c)
    return f


def cloth_folds(base, dark, light, n=4):
    def f(F):
        for i in range(n):
            x = int((i + 0.5) * F.w / n) + R.randint(-1, 1)
            for y in range(F.h):
                k = y / max(1, F.h - 1)
                F.px(x, y, mix(base, dark, 0.25 + 0.4 * k))
                F.px(x + 1, y, mix(base, light, 0.3 * k))
        F.rect(0, F.h - 2, F.w, 2, mix(base, dark, 0.45))
    return f


def knit(cols, h=4):
    """horizontal knit stripes with a stitch texture"""
    def f(F):
        for y in range(F.h):
            c = cols[(y // h) % len(cols)]
            for x in range(F.w):
                cc = c
                if (x + (y % 2)) % 2 == 0: cc = mix(c, 0x000000, 0.12)
                if y % h == 0: cc = mix(c, 0x000000, 0.25)
                F.px(x, y, cc)
    return f


def ribs(c, dark):
    def f(F):
        for x in range(F.w):
            for y in range(F.h):
                F.px(x, y, dark if x % 3 == 0 else c)
    return f


def bandage(F):
    for y in range(F.h):
        for x in range(F.w):
            v = (x + y * 2) % 9
            c = BAND if v > 1 else BAND_D
            if R.random() < 0.06: c = mix(BAND, BAND_D, 0.5)
            F.px(x, y, c)
    for y in range(0, F.h, 6):
        F.rect(0, y, F.w, 1, mix(BAND, BAND_D, 0.6))


def socks(F):
    for y in range(F.h):
        F.rect(0, y, F.w, 1, SOCK_C if (y // 4) % 2 == 0 else BLACK)


def grenade_paint(F):
    for y in range(F.h):
        for x in range(F.w):
            c = NADE
            if x % 4 == 0 or y % 4 == 0: c = NADE_D
            elif (x % 4 == 1 and y % 4 == 1): c = NADE_L
            F.px(x, y, c)


def warning(F):
    W, H = F.w, F.h
    F.rect(0, 0, W, 5, BROWN_D)
    F.rect(0, 5, W, 1, BROWN_L)
    cx, top, bot = W / 2, H * 0.36, H - 3
    hw = (bot - top) * 0.62
    F.poly([(cx, top - 1.5), (cx + hw + 1.5, bot + 1), (cx - hw - 1.5, bot + 1)], BLACK)
    F.poly([(cx, top), (cx + hw, bot), (cx - hw, bot)], HAZ)
    F.rect(int(cx) - 1, int(top) + 4, 2, int((bot - top) * 0.45), BLACK)
    F.rect(int(cx) - 1, int(bot) - 3, 2, 2, BLACK)


def face_front(F):
    W, H = F.w, F.h  # 48 x 48
    for y in range(H):
        for x in range(W):
            F.px(x, y, mix(SKIN, SKIN_D, max(0, (10 - y) / 10) * 0.55))
    cx = W / 2
    # glowing orange triangle eye on the character's LEFT (viewer's right)
    pts = [(26, 15), (43, 14), (35, 27)]
    F.poly([(25, 13.5), (44.5, 12.5), (35, 29.5)], EYE_D)
    F.poly(pts, EYE, glow=True)
    F.poly([(30, 16), (39, 15.5), (35, 22)], 0xFFC060, glow=True)
    F.rect(34, 16, 2, 5, 0x3A1004)
    # cheek mark (small ring) under the eye
    F.disc(42, 30, 2.0, SKIN_D); F.disc(42, 30, 1.0, SKIN)
    # huge shark grin, corners pulled up
    for x in range(3, W - 3):
        u = (x + .5 - cx) / (cx - 3)
        top = 33 - 1.6 * (1 - u * u) - 6 * u * u
        bot = 44.5 - 11 * u * u
        if bot <= top + 1: continue
        for y in range(int(top), int(bot) + 1):
            F.px(x, y, MOUTH if y > top + 0.5 else LIP)
        F.px(x, int(bot) + 1, LIP)
    for i in range(10):
        x0 = 4 + i * 4
        u = (x0 + 2 - cx) / (cx - 3)
        top = 33 - 1.6 * (1 - u * u) - 6 * u * u
        bot = 44.5 - 11 * u * u
        span = bot - top
        if span < 3: continue
        th = min(5.5, span * 0.48)
        F.poly([(x0, top), (x0 + 4, top), (x0 + 2, top + th)], TEETH)
        F.poly([(x0 + 2, bot + 1), (x0 + 6, bot + 1), (x0 + 4, bot + 1 - th)], TEETH)


def glow_fill(c1, c2):
    def f(F):
        for y in range(F.h):
            for x in range(F.w):
                c = mix(c1, c2, y / max(1, F.h - 1))
                if R.random() < 0.18: c = mix(c, 0xFFFFFF, 0.3)
                F.px(x, y, c, glow=True)
    return f


def smoke_paint(F):
    for y in range(F.h):
        for x in range(F.w):
            F.px(x, y, mix(SMOKE, SMOKE_D, R.random() * 0.7))


GF = lambda a, b: (lambda fs: [glow_fill(a, b)(f) for f in fs.values()])

# ------------------------------------------------------------------ skeleton
m.group("root", (0, 0, 0))
m.group("smoke", (0, 1, 0))  # not under root: the cloud stays where she slammed it while she hops away
m.group("air_bomb", (0, 6, -4), parent="root")
m.group("body", (0, 15.5, 0), parent="root")
m.group("blast", (0, 21, -1), parent="body")
m.group("skirt_f", (0, 15.0, -2.1), parent="body")
m.group("skirt_f2", (0, 12.2, -2.5), parent="skirt_f")
m.group("skirt_b", (0, 15.0, 2.1), parent="body")
m.group("skirt_b2", (0, 12.2, 2.5), parent="skirt_b")
m.group("skirt_r", (3.0, 15.0, 0), parent="body")
m.group("skirt_l", (-3.0, 15.0, 0), parent="body")
m.group("bag", (2.6, 17.2, -1.6), parent="body")
m.group("chest", (0, 18, 0), parent="body")
m.group("shells", (0, 22, 0), parent="chest")
m.group("launcher", (3.6, 26.4, 0), parent="chest")
m.group("rflash", (3.6, 26.6, -8.4), parent="launcher")
m.group("bblast", (3.6, 26.6, 6.0), parent="launcher")
m.group("head", (0, 27.4, 0), parent="chest")
m.group("hat", (0, 32.6, 0), parent="head")
m.group("antenna", (2.65, 34.6, 1.0), parent="hat")
m.group("spiral", (2.65, 41.6, 1.0), parent="antenna")
m.group("spark", (1.0, 43.0, 1.0), parent="spiral")
m.group("bangs", (0, 33.2, -3.2), parent="head")
m.group("hair_b1", (0, 31.5, 3.0), parent="head")
m.group("hair_b2", (0, 21.0, 4.0), parent="hair_b1")
m.group("hair_b3", (0, 11.0, 4.6), parent="hair_b2")
for s, k in ((1, "r"), (-1, "l")):
    m.group("hair_" + k + "1", (3.3 * s, 31.5, 0.3), parent="head")
    m.group("hair_" + k + "2", (4.3 * s, 22.5, 0.8), parent="hair_" + k + "1")
    m.group("arm_" + k, (3.6 * s, 25.4, 0), parent="chest")
    m.group("fore_" + k, (3.6 * s, 21.2, 0), parent="arm_" + k)
    m.group("hand_" + k, (3.6 * s, 17.2, 0), parent="fore_" + k)
m.group("grenade", (-3.6, 15.0, 0), parent="hand_l")
m.group("fist_flash", (-3.6, 14.0, -1.0), parent="hand_l")
m.group("bomb_r", (3.6, 14.6, 0), parent="hand_r")
m.group("det", (3.6, 15.0, 0), parent="hand_r")
m.group("c4", (3.6, 15.0, 0), parent="hand_r")
for s, k in ((1, "r"), (-1, "l")):
    m.group("leg_" + k, (1.45 * s, 15.0, 0), parent="root")
    m.group("shin_" + k, (1.45 * s, 9.0, 0), parent="leg_" + k)
    m.group("foot_" + k, (1.45 * s, 1.6, 0), parent="shin_" + k)

# ------------------------------------------------------------------ legs: dark tights, striped socks, tall pointed heeled boots
for s, k in ((1, "r"), (-1, "l")):
    x = 1.45 * s
    m.cube("thigh_" + k, "leg_" + k, (x - 1.3, 11.4, -1.3), (x + 1.3, 15.2, 1.3), BLACK, color2=BLACK_L, grad=True)
    m.cube("sock_" + k, "leg_" + k, (x - 1.25, 9.0, -1.25), (x + 1.25, 11.6, 1.25), SOCK_C, faces=all_faces(socks, ("up", "down")))
    m.cube("sockb_" + k, "shin_" + k, (x - 1.2, 7.6, -1.2), (x + 1.2, 9.1, 1.2), SOCK_C, faces=all_faces(socks, ("up", "down")))
    m.cube("boot_" + k, "shin_" + k, (x - 1.35, 1.4, -1.45), (x + 1.35, 7.0, 1.4), BLACK, color2=BLACK_L, grad=True,
           faces={"north": lambda F: F.rect(F.w // 2 - 1, 3, 2, F.h - 6, BLACK_L),
                  "east": lambda F: F.rect(2, 0, 1, F.h, 0x0E0C14), "west": lambda F: F.rect(F.w - 3, 0, 1, F.h, 0x0E0C14)})
    m.cube("cuff_" + k, "shin_" + k, (x - 1.6, 6.6, -1.7), (x + 1.6, 8.0, 1.6), BLACK_L, color2=BLACK, grad=True,
           origin=(x, 7.3, 0), rot=(-6, 0, 0))
    m.cube("ankle_" + k, "foot_" + k, (x - 1.25, 0.6, -2.0), (x + 1.25, 2.0, 1.35), BLACK)
    m.cube("toe_" + k, "foot_" + k, (x - 0.9, 0.0, -3.9), (x + 0.9, 1.3, -1.6), BLACK, origin=(x, 0, -1.6), rot=(-6, 0, 0))
    m.cube("tip_" + k, "foot_" + k, (x - 0.45, 0.0, -5.2), (x + 0.45, 0.8, -3.7), BLACK_L, origin=(x, 0, -3.7), rot=(-10, 0, 0))
    m.cube("heel_" + k, "foot_" + k, (x - 0.5, -0.01, 0.4), (x + 0.5, 1.0, 1.3), BLACK_L)

# ------------------------------------------------------------------ hips: belt, skirt (A-line, 6 panels), bag + radio
m.cube("hips", "body", (-3.0, 15.0, -2.0), (3.0, 17.6, 2.0), SKIRT, color2=SKIRT_D, grad=True)
m.cube("belt", "body", (-3.15, 16.9, -2.15), (3.15, 17.9, 2.15), BROWN, color2=BROWN_D, grad=True,
       faces={"north": lambda F: (F.rect(F.w // 2 - 3, 0, 6, F.h, BRASS), F.rect(F.w // 2 - 1, 2, 2, F.h - 4, BROWN_D))})
m.cube("sk_f", "skirt_f", (-3.2, 12.0, -2.55), (3.2, 15.4, -1.95), SKIRT, color2=SKIRT_D, grad=True, origin=(0, 15.0, -2.1), rot=(5, 0, 0),
       faces={"north": cloth_folds(SKIRT, SKIRT_D, SKIRT_L, 3)})
m.cube("sk_f2", "skirt_f2", (-3.5, 10.2, -2.95), (3.5, 12.4, -2.3), SKIRT, color2=SKIRT_D, grad=True, origin=(0, 12.2, -2.5), rot=(6, 0, 0),
       faces={"north": cloth_folds(SKIRT, SKIRT_D, SKIRT_L, 4)})
m.cube("sk_b", "skirt_b", (-3.2, 12.0, 1.95), (3.2, 15.4, 2.55), SKIRT, color2=SKIRT_D, grad=True, origin=(0, 15.0, 2.1), rot=(-6, 0, 0),
       faces={"south": cloth_folds(SKIRT, SKIRT_D, SKIRT_L, 3)})
m.cube("sk_b2", "skirt_b2", (-3.5, 9.8, 2.3), (3.5, 12.4, 2.95), SKIRT, color2=SKIRT_D, grad=True, origin=(0, 12.2, 2.5), rot=(-8, 0, 0),
       faces={"south": cloth_folds(SKIRT, SKIRT_D, SKIRT_L, 4)})
for s, k in ((1, "r"), (-1, "l")):
    m.cube("sk_" + k, "skirt_" + k, (3.0 * s - 0.35, 10.2, -2.4), (3.0 * s + 0.35, 15.3, 2.4), SKIRT, color2=SKIRT_D, grad=True,
           origin=(3.0 * s, 15.0, 0), rot=(0, 0, 7 * s), faces={"east": cloth_folds(SKIRT, SKIRT_D, SKIRT_L, 3), "west": cloth_folds(SKIRT, SKIRT_D, SKIRT_L, 3)})
    m.cube("sk_hem_" + k, "skirt_" + k, (3.0 * s - 0.4, 10.0, -2.6), (3.0 * s + 0.4, 10.7, 2.6), SKIRT_D, origin=(3.0 * s, 15.0, 0), rot=(0, 0, 7 * s))
m.cube("bag_body", "bag", (1.3, 13.2, -3.3), (4.5, 16.4, -1.7), BROWN, color2=BROWN_D, grad=True, origin=(2.9, 16.4, -2.5), rot=(4, 14, 0),
       faces={"north": warning, "east": frame(BROWN_D), "west": frame(BROWN_D)})
m.cube("bag_flap", "bag", (1.2, 15.6, -3.45), (4.6, 16.6, -1.6), BROWN_L, color2=BROWN, grad=True, origin=(2.9, 16.4, -2.5), rot=(4, 14, 0))
m.cube("bag_strap", "bag", (2.0, 16.4, -2.3), (2.6, 17.8, -1.9), BROWN_D, origin=(2.3, 17.2, -2.1), rot=(0, 14, -10))
m.cube("radio", "body", (-4.0, 14.4, -1.0), (-3.0, 17.0, 0.9), BROWN, color2=BROWN_D, grad=True,
       faces={"west": lambda F: (F.rect(2, 3, F.w - 4, 7, 0xD8C47A), F.rect(3, 13, F.w - 6, 4, BLACK))})
m.cube("radio_ant", "body", (-3.7, 17.0, 0.4), (-3.4, 18.6, 0.7), BLACK)

# ------------------------------------------------------------------ torso: bandaged midriff, cropped orange jacket, bandolier
m.cube("midriff", "chest", (-2.5, 17.6, -1.5), (2.5, 20.6, 1.5), BAND, faces=all_faces(bandage))
m.cube("torso", "chest", (-2.8, 20.4, -1.8), (2.8, 25.9, 1.8), JACK, color2=JACK_D, grad=True,
       faces={"north": combo(cloth_folds(JACK, JACK_D, JACK_L, 3), lambda F: F.rect(F.w // 2, 0, 1, F.h, JACK_D)),
              "south": cloth_folds(JACK, JACK_D, JACK_L, 3)})
m.cube("hem", "chest", (-3.0, 19.8, -2.0), (3.0, 20.8, 2.0), JACK_D, color2=JACK, grad=True)
m.cube("bust", "chest", (-2.4, 22.6, -2.15), (2.4, 25.0, -1.7), JACK, color2=JACK_D, grad=True)
for i, y in enumerate((21.6, 23.0, 24.4)):  # black frog clasps
    m.cube(f"frog{i}", "chest", (-1.3, y, -2.35), (1.3, y + 0.42, -2.0), BLACK)
    m.cube(f"knot{i}", "chest", (-0.35, y - 0.15, -2.5), (0.35, y + 0.57, -2.1), BLACK_L)
m.cube("collar", "chest", (-2.3, 25.6, -2.1), (2.3, 27.3, 2.0), JACK, color2=JACK_D, grad=True,
       faces={"north": lambda F: F.rect(F.w // 2 - 3, 0, 6, F.h, JACK_D), "up": lambda F: F.rect(3, 3, F.w - 6, F.h - 6, BLACK)})
m.cube("collar_r", "chest", (0.5, 25.4, -2.4), (2.4, 27.5, -1.9), JACK_L, origin=(1.4, 26, -2.1), rot=(0, -12, 8))
m.cube("collar_l", "chest", (-2.4, 25.4, -2.4), (-0.5, 27.5, -1.9), JACK_L, origin=(-1.4, 26, -2.1), rot=(0, 12, -8))
m.cube("neck", "chest", (-1.0, 25.8, -0.9), (1.0, 27.8, 0.9), SKIN_D, color2=SKIN, grad=True)
# bandolier: right shoulder -> left hip, front + back, with shells
ang = math.degrees(math.atan2(5.6, 8.0))
for side, z0 in (("f", -2.05), ("b", 1.85)):
    zz = z0 if side == "f" else z0
    m.cube("band_" + side, "shells", (-0.65, 17.4, zz - 0.2), (0.65, 27.2, zz + 0.2), BROWN, color2=BROWN_D, grad=True,
           origin=(0, 22.2, zz), rot=(0, 0, -ang))
for i in range(9):
    t = i / 8
    cx, cy = 2.4 - 4.9 * t, 25.6 - 7.0 * t
    m.cube(f"shell{i}", "shells", (cx - 0.28, cy - 0.75, -2.75), (cx + 0.28, cy + 0.75, -2.15), SHELL if i % 2 else SHELL_D,
           origin=(cx, cy, -2.4), rot=(0, 0, 90 - ang), faces={"north": lambda F: F.rect(0, 0, F.w, 3, BRASS)})
for i in range(6):
    t = (i + 0.5) / 6
    cx, cy = 2.4 - 4.9 * t, 25.6 - 7.0 * t
    m.cube(f"shellb{i}", "shells", (cx - 0.28, cy - 0.7, 2.05), (cx + 0.28, cy + 0.7, 2.6), SHELL, origin=(cx, cy, 2.3), rot=(0, 0, 90 - ang))

# ------------------------------------------------------------------ head: white face, grin, orange eye, bangs, knit beanie + antenna
m.cube("skull", "head", (-3.0, 27.4, -3.0), (3.0, 33.4, 3.0), SKIN, faces={"north": face_front, "up": lambda F: F.rect(0, 0, F.w, F.h, HAIR_D)})
m.cube("hat_brim", "hat", (-3.45, 32.5, -3.45), (3.45, 33.8, 3.45), HAT_O, faces=all_faces(ribs(HAT_O, HAT_B), ("up", "down")))
m.cube("hat_mid", "hat", (-3.6, 33.4, -3.6), (3.6, 36.0, 3.6), HAT_O, faces=all_faces(knit([HAT_O, HAT_C, HAT_B], 4), ("down",)))
m.cube("hat_top", "hat", (-3.0, 35.9, -3.0), (3.0, 37.3, 3.0), HAT_O, faces=all_faces(knit([HAT_C, HAT_B, HAT_O], 4), ("down",)))
m.cube("hat_crown", "hat", (-2.0, 37.2, -2.0), (2.0, 38.0, 2.0), HAT_B, faces=all_faces(knit([HAT_B, HAT_O], 3)))
m.cube("hat_fold", "hat", (-3.7, 33.6, -3.75), (3.7, 34.1, 3.75), HAT_B)
m.cube("ant_base", "antenna", (2.2, 34.4, 0.55), (3.1, 35.4, 1.45), BLACK_L)
m.cube("ant_stick", "antenna", (2.45, 35.3, 0.8), (2.85, 41.8, 1.2), BLACK, color2=BLACK_L, grad=True)
# square spiral (flat in XY), from the stick top inward
path = [(2.65, 41.6), (2.65, 44.0), (-1.4, 44.0), (-1.4, 41.6), (1.6, 41.6), (1.6, 43.1), (-0.5, 43.1), (-0.5, 42.4), (0.8, 42.4)]
for i in range(len(path) - 1):
    (x1, y1), (x2, y2) = path[i], path[i + 1]
    lo, hi = (min(x1, x2) - 0.2, min(y1, y2) - 0.2), (max(x1, x2) + 0.2, max(y1, y2) + 0.2)
    m.cube(f"spir{i}", "spiral", (lo[0], lo[1], 0.8), (hi[0], hi[1], 1.2), BLACK)
m.cube("spark_core", "spark", (0.5, 42.5, 0.5), (1.5, 43.5, 1.5), F_CORE, glow=True, paint=GF(F_CORE, F_MID))
m.cube("spark_out", "spark", (0.1, 42.2, 0.1), (1.9, 44.4, 1.9), F_MID, glow=True, origin=(1, 43, 1), rot=(0, 45, 0), inflate=0.0,
       paint=GF(F_MID, F_OUT))
# hair under the hat + bangs (cover the character's right eye)
m.cube("hair_crown", "head", (-3.7, 27.0, 0.0), (3.7, 33.6, 3.9), HAIR, faces=all_faces(HS))
m.cube("bang_main", "bangs", (0.3, 29.0, -3.55), (3.5, 33.3, -3.0), HAIR, origin=(1.9, 33.2, -3.2), rot=(2, 0, -6), faces=all_faces(HS2))
for i, (x, ln, rz) in enumerate([(3.0, 6.6, 6), (2.0, 5.4, 2), (0.9, 4.6, -12), (-0.6, 1.4, -20), (-1.9, 1.0, -26), (-3.0, 4.4, -4)]):
    m.cube(f"bang{i}", "bangs", (x - 0.55, 33.2 - ln, -3.7), (x + 0.55, 33.2, -3.05), HAIR if i % 2 else HAIR_HI if i == 2 else HAIR_D,
           origin=(x, 33.2, -3.3), rot=(5, 0, rz), faces=all_faces(HS2))
m.cube("hb_main", "hair_b1", (-4.4, 20.4, 2.1), (4.4, 31.8, 5.0), HAIR, faces=all_faces(HS))
m.cube("hb_lower", "hair_b2", (-5.0, 10.8, 2.6), (5.0, 21.2, 5.6), HAIR, color2=HAIR_D, grad=True, faces=all_faces(HS))
for i in range(11):  # long jagged tips below the knees
    x = -4.8 + i * 0.96
    ln = 4.0 + (i % 3) * 2.4 + R.uniform(0, 1.5)
    m.cube(f"hb_tip{i}", "hair_b3", (x - 0.55, 11.2 - ln, 3.1 + (i % 2) * 0.3), (x + 0.55, 11.2, 4.9 + (i % 2) * 0.3), HAIR if i % 2 else HAIR_D,
           origin=(x, 11.2, 4.0), rot=(-8 - (i % 3) * 5, 0, (i - 5) * 6), faces=all_faces(HS2))
for i in range(4):  # spiky locks flaring sideways off the back (big silhouette of the art)
    for s in (1, -1):
        y = 18 - i * 3.2
        m.cube(f"hb_spike{i}_{'r' if s > 0 else 'l'}", "hair_b2", (4.6 * s - 0.5, y - 5.5, 3.3), (4.6 * s + 0.5, y, 4.6), HAIR_D if i % 2 else HAIR,
               origin=(4.6 * s, y, 4.0), rot=(-10, 0, (22 + i * 7) * s), faces=all_faces(HS2))
for s, k in ((1, "r"), (-1, "l")):
    m.cube("hs_main_" + k, "hair_" + k + "1", (3.5 * s - 0.75, 21.8, 0.3), (3.5 * s + 0.75, 31.6, 2.9), HAIR, faces=all_faces(HS))
    for i in range(5):
        z = 0.7 + i * 0.55
        ln = 8.0 + (i % 2) * 3.0 + R.uniform(0, 1.5)
        m.cube(f"hs_lock{i}_" + k, "hair_" + k + "2", (4.2 * s - 0.55, 22.8 - ln, z - 0.5), (4.2 * s + 0.55, 22.8, z + 0.5),
               HAIR if i % 2 else HAIR_HI if i == 2 else HAIR_D, origin=(4.2 * s, 22.8, z), rot=(-4 - i * 3, 0, (6 + i * 4) * s), faces=all_faces(HS2))
    for i in range(3):
        m.cube(f"hs_puff{i}_" + k, "hair_" + k + "1", (3.9 * s - 0.6, 24.5 - i * 1.5, -1.9 + i * 1.4), (3.9 * s + 0.6, 30.8 - i * 1.2, -0.7 + i * 1.4),
               HAIR_HI if i == 1 else HAIR, origin=(3.9 * s, 30.8, 0), rot=(0, 0, (10 + i * 6) * s), faces=all_faces(HS2))
    for i in range(3):
        ln = 4 + i
        m.cube(f"hs_flick{i}_" + k, "hair_" + k + "2", (4.8 * s - 0.4, 16 - i * 2.6 - ln, -0.4 + i * 0.6), (4.8 * s + 0.4, 16 - i * 2.6, 0.4 + i * 0.6),
               HAIR_D, origin=(4.8 * s, 16 - i * 2.6, i * 0.6), rot=(-6, 0, (24 + i * 8) * s))

# ------------------------------------------------------------------ arms: orange sleeves, wide cuffs, black gloves with claw tips
for s, k in ((1, "r"), (-1, "l")):
    x = 3.6 * s
    m.cube("sleeve_" + k, "arm_" + k, (x - 0.95, 21.0, -1.0), (x + 0.95, 25.8, 1.0), JACK, color2=JACK_D, grad=True,
           faces={"north": cloth_folds(JACK, JACK_D, JACK_L, 2)})
    m.cube("shoulder_" + k, "arm_" + k, (x - 1.2, 23.8, -1.3), (x + 1.2, 26.3, 1.3), JACK, color2=JACK_D, grad=True, origin=(x, 25.4, 0), rot=(0, 0, 6 * s))
    m.cube("forearm_" + k, "fore_" + k, (x - 0.9, 18.2, -0.95), (x + 0.9, 21.3, 0.95), JACK, color2=JACK_D, grad=True)
    m.cube("cuff_s_" + k, "fore_" + k, (x - 1.2, 17.6, -1.25), (x + 1.2, 19.4, 1.25), JACK_D, color2=JACK, grad=True,
           faces={"north": lambda F: F.rect(F.w // 2 - 1, 5, 3, 3, BLACK), "south": hstripe(BROWN_D, 1, 1)})
    m.cube("glove_" + k, "hand_" + k, (x - 0.92, 15.4, -0.98), (x + 0.92, 17.8, 0.98), BLACK, color2=BLACK_L, grad=True)
    m.cube("thumb_" + k, "hand_" + k, (x - 0.25 * s - 0.3, 14.8, -1.35), (x - 0.25 * s + 0.3, 16.6, -0.75), BLACK, origin=(x, 16.6, -1), rot=(16, 0, -18 * s))
    for i in range(3):
        fx = x - 0.65 + i * 0.6
        m.cube(f"claw{i}_" + k, "hand_" + k, (fx - 0.15, 14.3, -0.9), (fx + 0.15, 15.5, -0.5), STEEL_D, color2=STEEL, grad=True,
               origin=(fx, 15.5, -0.7), rot=(14, 0, 0))

# grenade (left hand)
m.cube("nade", "grenade", (-4.5, 12.6, -0.95), (-2.7, 15.2, 0.95), NADE, faces=all_faces(grenade_paint))
m.cube("nade_top", "grenade", (-4.0, 15.2, -0.45), (-3.2, 15.9, 0.45), BRASS)
m.cube("nade_lever", "grenade", (-4.75, 13.2, -0.3), (-4.45, 15.8, 0.3), STEEL, origin=(-4.6, 15.7, 0), rot=(0, 0, 8))
m.cube("nade_ring", "grenade", (-3.2, 15.5, -0.1), (-2.2, 16.5, 0.1), BRASS, origin=(-2.7, 16, 0), rot=(0, 30, 0))
m.cube("ff_a", "fist_flash", (-5.8, 11.8, -3.0), (-1.4, 16.2, 1.4), F_MID, glow=True, paint=GF(F_CORE, F_OUT))
m.cube("ff_b", "fist_flash", (-5.2, 12.4, -4.6), (-2.0, 15.6, -1.4), F_CORE, glow=True, origin=(-3.6, 14, -1.0), rot=(45, 0, 45), paint=GF(F_CORE, F_MID))
# right-hand props
m.cube("bomb_body", "bomb_r", (2.7, 12.6, -0.9), (4.5, 14.4, 0.9), BLACK, color2=BLACK_L, grad=True, inflate=0.1,
       faces={"north": lambda F: F.rect(3, 3, 3, 3, 0x5A5468)})
m.cube("bomb_fuse", "bomb_r", (3.45, 14.4, -0.15), (3.75, 15.6, 0.15), 0xD8C48A, origin=(3.6, 14.4, 0), rot=(0, 0, 20))
m.cube("det_box", "det", (2.9, 12.6, -0.9), (4.3, 15.0, 0.7), 0xB02A20, color2=0x6A1610, grad=True,
       faces={"north": lambda F: (F.rect(2, 3, F.w - 4, 4, 0xF0E0A0), F.rect(2, 10, F.w - 4, 3, BLACK))})
m.cube("det_btn", "det", (3.3, 15.0, -0.5), (3.9, 15.5, 0.1), 0xFF3020, glow=True)
m.cube("det_ant", "det", (4.0, 15.0, 0.2), (4.2, 17.4, 0.4), BLACK)
m.cube("c4_brick", "c4", (2.7, 12.4, -1.1), (4.5, 14.8, 0.9), 0xC8B880, color2=0x9A8A58, grad=True,
       faces={"north": lambda F: (F.rect(0, 4, F.w, 2, BLACK), F.rect(0, 13, F.w, 2, BLACK))})
m.cube("c4_led", "c4", (3.3, 14.8, -0.6), (3.9, 15.3, 0.0), 0xFF2010, glow=True)
# rocket launcher on the right shoulder (only during "rocket")
m.cube("rl_tube", "launcher", (2.6, 25.6, -7.0), (4.6, 27.6, 5.0), LAUNCH, color2=LAUNCH_D, grad=True,
       faces={"east": lambda F: [F.rect(x, 0, 3, F.h, HAZ) for x in range(4, 30, 8)], "west": lambda F: [F.rect(x, 0, 3, F.h, HAZ) for x in range(4, 30, 8)],
              "up": lambda F: [F.rect(0, y, F.w, 3, HAZ) for y in range(4, 30, 8)]})
m.cube("rl_head", "launcher", (2.85, 25.85, -8.6), (4.35, 27.35, -7.0), 0xC03020, color2=0x7A1A10, grad=True)
m.cube("rl_tip", "launcher", (3.25, 26.25, -9.3), (3.95, 26.95, -8.6), 0xE0D0C0)
m.cube("rl_rear", "launcher", (2.35, 25.35, 5.0), (4.85, 27.85, 6.2), LAUNCH_D)
m.cube("rl_grip", "launcher", (3.3, 23.6, -2.8), (3.9, 25.6, -1.9), BLACK, origin=(3.6, 25.6, -2.3), rot=(-12, 0, 0))
m.cube("rl_sight", "launcher", (2.2, 26.4, -3.5), (2.6, 27.8, -2.3), BLACK)
m.cube("rf_a", "rflash", (2.6, 25.6, -11.5), (4.6, 27.6, -8.4), F_CORE, glow=True, paint=GF(F_CORE, F_MID))
m.cube("rf_b", "rflash", (2.2, 25.2, -10.6), (5.0, 28.0, -8.6), F_MID, glow=True, origin=(3.6, 26.6, -9.6), rot=(0, 0, 45), paint=GF(F_MID, F_OUT))
m.cube("bb_a", "bblast", (2.3, 25.3, 6.0), (4.9, 27.9, 10.5), F_MID, glow=True, paint=GF(F_MID, F_OUT))
m.cube("bb_b", "bblast", (1.8, 24.8, 8.0), (5.4, 28.4, 13.0), SMOKE, paint=lambda fs: [smoke_paint(f) for f in fs.values()])
# kamikaze blast ball
m.cube("bl_core", "blast", (-3, 18, -4), (3, 24, 2), F_CORE, glow=True, paint=GF(F_CORE, F_MID))
m.cube("bl_mid", "blast", (-4.5, 16.5, -5.5), (4.5, 25.5, 3.5), F_MID, glow=True, origin=(0, 21, -1), rot=(45, 45, 0), paint=GF(F_MID, F_OUT))
m.cube("bl_out", "blast", (-5.5, 15.5, -6.5), (5.5, 26.5, 4.5), F_OUT, glow=True, origin=(0, 21, -1), rot=(0, 45, 45), paint=GF(F_OUT, 0xC02010))
# smoke cloud
for i in range(10):  # billowing puffs at several heights, tilted so the cloud reads round
    a = i / 10 * math.tau + (i % 2) * 0.3
    rr = 5.0 if i % 2 else 3.0
    cx, cz = math.cos(a) * rr, math.sin(a) * rr
    sz = 2.6 + (i % 3) * 0.9
    cy = 2.5 + (i % 4) * 3.2
    m.cube(f"smk{i}", "smoke", (cx - sz, cy - sz, cz - sz), (cx + sz, cy + sz, cz + sz), SMOKE if i % 3 else SMOKE_D, origin=(cx, cy, cz),
           rot=(30 + i * 17, i * 23, 20 + i * 11), paint=lambda fs: [smoke_paint(f) for f in fs.values()])
m.cube("smk_c", "smoke", (-3.5, 0, -3.5), (3.5, 7, 3.5), SMOKE_D, origin=(0, 3.5, 0), rot=(0, 45, 0), paint=lambda fs: [smoke_paint(f) for f in fs.values()])
# airborne grenade for kick_back
m.cube("ab_nade", "air_bomb", (-0.9, 5.0, -4.9), (0.9, 7.4, -3.1), NADE, faces=all_faces(grenade_paint))
m.cube("ab_top", "air_bomb", (-0.4, 7.4, -4.4), (0.4, 8.0, -3.6), BRASS)


# ================================================================== animation
PROPS = ["launcher", "rflash", "bblast", "blast", "smoke", "air_bomb", "spark", "fist_flash", "bomb_r", "det", "c4"]
HIDE = (0, .001, .001, .001)


class A:
    def __init__(self, name, ticks, loop=False):
        self.name, self.ticks, self.loop, self.tr = name, ticks, loop, {}

    def k(self, bone, ch, keys):
        self.tr.setdefault(bone, {}).setdefault(ch, []).extend(keys)
        return self

    def rot(self, bone, *keys): return self.k(bone, "rotation", keys)
    def pos(self, bone, *keys): return self.k(bone, "position", keys)
    def scl(self, bone, *keys): return self.k(bone, "scale", keys)

    def drape(self, chain, keys, delay=2, gain=0.8):
        g = 1.0
        for i, b in enumerate(chain):
            d = delay * i
            seen, out = set(), []
            for (t, x, y, z) in keys:
                tt = min(self.ticks, t + d)
                if tt in seen: continue
                seen.add(tt); out.append((tt, x * g, y * g, z * g))
            self.rot(b, *out)
            g *= gain
        return self

    def show(self, bone, t0, t1, s=1.0, grow=1.5):
        """prop visible (scale s) between t0 and t1"""
        ks = [HIDE]
        if t0 > 0: ks += [(max(0.01, t0 - grow), .001, .001, .001)]
        ks += [(t0, s, s, s)]
        if t1 < self.ticks: ks += [(t1, s, s, s), (min(self.ticks, t1 + grow), .001, .001, .001)]
        if t0 <= 0: ks[0] = (0, s, s, s)
        self.scl(bone, *ks)

    def done(self):
        for p in PROPS:
            if p not in self.tr or "scale" not in self.tr[p]:
                if p in ("rflash", "bblast"): continue  # follow launcher
                self.scl(p, HIDE)
        for p in ("rflash", "bblast"):
            if p not in self.tr or "scale" not in self.tr[p]:
                self.scl(p, HIDE)
        tracks = {}
        for b, chs in self.tr.items():
            tracks[b] = {ch: sorted([(t / 20.0, x, y, z) for (t, x, y, z) in v], key=lambda q: q[0]) for ch, v in chs.items()}
        m.anim(self.name, self.ticks / 20.0, tracks, loop=self.loop)


def nade_hide(a, t0, t1):
    """grenade in the left hand gone between t0 (thrown) and t1 (new one drawn)"""
    a.scl("grenade", (0, 1, 1, 1), (t0 - 0.3, 1, 1, 1), (t0 + 0.3, .001, .001, .001), (t1 - 1.5, .001, .001, .001), (t1, 1, 1, 1))


HAIR_B = ["hair_b1", "hair_b2", "hair_b3"]
HAIR_R, HAIR_L = ["hair_r1", "hair_r2"], ["hair_l1", "hair_l2"]
SK_F, SK_B = ["skirt_f", "skirt_f2"], ["skirt_b", "skirt_b2"]


def hair_all(a, back, side_r, side_l=None, delay=2):
    # the back chain is ~30 px long: damp authored values so it whips instead of flagging out horizontally
    back = [(t, x * 0.6 if x < 0 else x * 0.75, y * 0.6, z * 0.6) for (t, x, y, z) in back]
    a.drape(HAIR_B, back, delay=delay, gain=0.8)
    a.drape(HAIR_R, side_r, delay=delay)
    a.drape(HAIR_L, side_l if side_l is not None else [(t, x, y, -z) for (t, x, y, z) in side_r], delay=delay)


def skirt(a, front, back=None, sides=None, delay=2):
    a.drape(SK_F, front, delay=delay, gain=0.9)
    a.drape(SK_B, back if back is not None else [(t, -x, y, z) for (t, x, y, z) in front], delay=delay, gain=0.9)
    if sides:
        a.rot("skirt_r", *sides)
        a.rot("skirt_l", *[(t, x, y, -z) for (t, x, y, z) in sides])


def legs(a, keys_r, keys_l=None, shin_r=None, shin_l=None, foot_r=None, foot_l=None):
    a.rot("leg_r", *keys_r)
    a.rot("leg_l", *(keys_l or [(t, x, y, -z) for (t, x, y, z) in keys_r]))
    if shin_r: a.rot("shin_r", *shin_r)
    if shin_l or shin_r: a.rot("shin_l", *(shin_l or shin_r))
    if foot_r: a.rot("foot_r", *foot_r)
    if foot_l or foot_r: a.rot("foot_l", *(foot_l or foot_r))


# ------------------------------------------------------------------ idle (4 s): hip cocked, tossing the grenade up and catching it
a = A("idle", 80, loop=True)
a.pos("body", (0, 0, 0, 0), (20, 0, -0.15, 0), (40, 0, 0, 0), (60, 0, -0.15, 0), (80, 0, 0, 0))
a.rot("body", (0, 0, 0, 3), (40, 0, 0, 2), (80, 0, 0, 3))
a.rot("chest", (0, -2, 0, -3), (20, -1, 2, -2), (40, -2, 0, -3), (60, -1, -2, -2), (80, -2, 0, -3))
a.rot("head", (0, 2, 0, 5), (20, 4, 3, 4), (40, 6, 0, 2), (46, 10, 0, 0), (52, 2, 0, 6), (80, 2, 0, 5))
a.rot("arm_r", (0, -4, 0, 18), (40, -2, 0, 16), (80, -4, 0, 18))      # hand on hip
a.rot("fore_r", (0, 70, 30, 0), (40, 66, 30, 0), (80, 70, 30, 0))
a.rot("arm_l", (0, 14, 0, -6), (36, 16, 0, -6), (40, 26, 0, -6), (43, 18, 0, -6), (50, 30, 0, -6), (54, 16, 0, -6), (80, 14, 0, -6))
a.rot("fore_l", (0, 40, 0, 0), (36, 44, 0, 0), (40, 64, 0, 0), (43, 40, 0, 0), (50, 60, 0, 0), (54, 42, 0, 0), (80, 40, 0, 0))
a.pos("grenade", (0, 0, 0, 0), (40, 0, 0, 0), (42, 0, 4.5, -0.5), (45, 0, 6.5, -0.8), (48, 0, 4.0, -0.5), (50, 0, 0, 0), (80, 0, 0, 0))
a.rot("grenade", (0, 0, 0, 0), (40, 0, 0, 0), (50, 360, 0, 0), (80, 360, 0, 0))
legs(a, [(0, 0, 0, 2), (40, 0, 0, 3), (80, 0, 0, 2)], [(0, 4, 0, -4), (40, 5, 0, -5), (80, 4, 0, -4)],
     shin_r=[(0, 0, 0, 0), (80, 0, 0, 0)], shin_l=[(0, -8, 0, 0), (40, -10, 0, 0), (80, -8, 0, 0)])
hair_all(a, [(0, -3, 0, 1), (20, -5, 0, 0), (40, -3, 0, -1), (60, -5, 0, 0), (80, -3, 0, 1)],
         [(0, 0, 0, 3), (30, 0, 0, 5), (55, 0, 0, 2), (80, 0, 0, 3)], [(0, 0, 0, -3), (25, 0, 0, -5), (50, 0, 0, -2), (80, 0, 0, -3)], delay=4)
skirt(a, [(0, 0, 0, 0), (20, 1.5, 0, 1), (40, 0, 0, 0), (60, 1.5, 0, -1), (80, 0, 0, 0)], delay=4)
a.rot("antenna", (0, 0, 0, 0), (20, 0, 0, 4), (40, 0, 0, -2), (46, -6, 0, 6), (52, 0, 0, -3), (80, 0, 0, 0))
a.rot("spiral", (0, 0, 0, 0), (22, 0, 0, 6), (42, 0, 0, -4), (48, 0, 0, 8), (56, 0, 0, -3), (80, 0, 0, 0))
a.done()

# ------------------------------------------------------------------ walk (one stride): bouncy confident strut, skirt swish
a = A("walk", 20, loop=True)
a.rot("leg_r", (0, 30, 0, 0), (5, 0, 0, 0), (10, -26, 0, 0), (15, 0, 0, 0), (20, 30, 0, 0))
a.rot("shin_r", (0, -6, 0, 0), (5, -12, 0, 0), (10, -10, 0, 0), (13, -50, 0, 0), (17, -28, 0, 0), (20, -6, 0, 0))
a.rot("foot_r", (0, -10, 0, 0), (5, 0, 0, 0), (10, 10, 0, 0), (15, 6, 0, 0), (20, -10, 0, 0))
a.rot("leg_l", (0, -26, 0, 0), (5, 0, 0, 0), (10, 30, 0, 0), (15, 0, 0, 0), (20, -26, 0, 0))
a.rot("shin_l", (0, -10, 0, 0), (3, -50, 0, 0), (7, -28, 0, 0), (10, -6, 0, 0), (15, -12, 0, 0), (20, -10, 0, 0))
a.rot("foot_l", (0, 10, 0, 0), (5, 6, 0, 0), (10, -10, 0, 0), (15, 0, 0, 0), (20, 10, 0, 0))
a.pos("body", (0, 0, -0.3, 0), (5, 0, 0.6, 0), (10, 0, -0.3, 0), (15, 0, 0.6, 0), (20, 0, -0.3, 0))
a.rot("body", (0, -3, 8, -2), (10, -3, -8, 2), (20, -3, 8, -2))
a.rot("chest", (0, 0, -6, 2), (10, 0, 6, -2), (20, 0, -6, 2))
a.rot("head", (0, 2, 4, -3), (10, 2, -4, 3), (20, 2, 4, -3))
a.rot("arm_r", (0, -26, 0, 8), (10, 30, 0, 6), (20, -26, 0, 8))
a.rot("fore_r", (0, 10, 0, 0), (10, 34, 0, 0), (20, 10, 0, 0))
a.rot("arm_l", (0, 26, 0, -6), (10, -20, 0, -8), (20, 26, 0, -6))
a.rot("fore_l", (0, 40, 0, 0), (10, 20, 0, 0), (20, 40, 0, 0))
hair_all(a, [(0, -12, 2, 2), (5, -16, 0, 0), (10, -12, -2, -2), (15, -16, 0, 0), (20, -12, 2, 2)],
         [(0, -6, 0, 6), (10, -8, 0, 2), (20, -6, 0, 6)], [(0, -8, 0, -2), (10, -6, 0, -6), (20, -8, 0, -2)])
skirt(a, [(0, 8, 0, 3), (5, 3, 0, 0), (10, 8, 0, -3), (15, 3, 0, 0), (20, 8, 0, 3)], [(0, -4, 0, -2), (5, -9, 0, 0), (10, -4, 0, 2), (15, -9, 0, 0), (20, -4, 0, -2)],
      sides=[(0, 0, 0, 4), (10, 0, 0, -2), (20, 0, 0, 4)])
a.rot("antenna", (0, -4, 0, 4), (5, 2, 0, 0), (10, -4, 0, -4), (15, 2, 0, 0), (20, -4, 0, 4))
a.rot("spiral", (0, 0, 0, -6), (10, 0, 0, 6), (20, 0, 0, -6))
a.done()

# ------------------------------------------------------------------ grenade_lob (30): pin bitten off 6, overhand throw 16, new grenade 26
a = A("grenade_lob", 30)
a.rot("arm_l", (0, 14, 0, -6), (4, 120, 30, 20), (6, 126, 34, 22), (8, 100, 20, 10), (13, 190, 0, -10), (15, 150, 0, -6), (16, 100, 0, -4),
      (19, 40, 0, 6), (24, 10, 0, -4), (30, 14, 0, -6))
a.rot("fore_l", (0, 40, 0, 0), (4, 110, 0, 0), (6, 112, 0, 0), (10, 70, 0, 0), (13, 90, 0, 0), (16, 10, 0, 0), (20, 20, 0, 0), (30, 40, 0, 0))
a.rot("head", (0, 0, 0, 0), (4, -6, -20, 0), (6, -2, 22, -10), (8, 6, 10, 0), (13, 10, -10, 0), (16, -8, -6, 0), (22, 4, 0, 0), (30, 0, 0, 0))
a.rot("chest", (0, 0, 0, 0), (6, -2, 10, 0), (13, 12, 40, 4), (16, -16, -30, 0), (19, -20, -36, 0), (24, -6, -10, 0), (30, 0, 0, 0))
a.rot("body", (0, 0, 0, 0), (13, 4, 14, 0), (16, -6, -14, 0), (22, -4, -8, 0), (30, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (13, 0, -0.4, 1.0), (16, 0, -0.8, -1.0), (22, 0, -0.5, -0.6), (30, 0, 0, 0))
a.rot("arm_r", (0, -4, 0, 18), (6, 10, 0, 20), (13, 70, 0, 30), (16, -20, 0, 26), (20, -30, 0, 18), (30, -4, 0, 18))
a.rot("fore_r", (0, 70, 30, 0), (13, 20, 0, 0), (18, 40, 0, 0), (30, 70, 30, 0))
legs(a, [(0, 0, 0, 2), (13, -20, 0, 2), (16, 26, 0, 2), (24, 14, 0, 2), (30, 0, 0, 2)], [(0, 4, 0, -4), (13, 30, 0, -4), (16, -24, 0, -4), (24, -10, 0, -4), (30, 4, 0, -4)],
     shin_r=[(0, 0, 0, 0), (13, -10, 0, 0), (16, -20, 0, 0), (30, 0, 0, 0)], shin_l=[(0, -8, 0, 0), (13, -30, 0, 0), (16, -6, 0, 0), (30, -8, 0, 0)])
nade_hide(a, 16, 27)
a.rot("grenade", (0, 0, 0, 0), (13, -40, 0, 0), (16, 20, 0, 0), (30, 0, 0, 0))
hair_all(a, [(0, -3, 0, 0), (6, -4, -10, 0), (13, 6, -20, 0), (16, -24, 16, 0), (21, -14, 6, 0), (30, -3, 0, 0)],
         [(0, 0, 0, 3), (13, 6, 0, 10), (16, -16, 0, 6), (30, 0, 0, 3)])
skirt(a, [(0, 0, 0, 0), (13, -6, 0, 2), (16, 14, 0, -2), (22, 6, 0, 0), (30, 0, 0, 0)], sides=[(0, 0, 0, 0), (16, 0, 0, 8), (30, 0, 0, 0)])
a.rot("antenna", (0, 0, 0, 0), (6, 0, 0, -16), (13, 14, 0, 6), (17, -20, 0, -6), (24, 6, 0, 2), (30, 0, 0, 0))
a.done()

# ------------------------------------------------------------------ bandolier_burst (36): grab strap 6, hunch, fling the fan of shells on 14
a = A("bandolier_burst", 36)
a.pos("body", (0, 0, 0, 0), (6, 0, -1.2, 0), (12, 0, -2.0, 0.5), (14, 0, -0.2, -0.6), (18, 0, 0, -0.4), (36, 0, 0, 0))
a.rot("body", (0, 0, 0, 0), (6, -8, 0, 0), (12, -16, 0, 0), (14, 6, 0, 0), (18, 8, 0, 0), (36, 0, 0, 0))
a.rot("chest", (0, 0, 0, 0), (6, -10, -10, 0), (12, -18, 6, 0), (14, 16, 0, 0), (18, 14, 0, 0), (26, 4, 0, 0), (36, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (6, 10, 0, 0), (12, 16, 0, 0), (14, 20, 0, 0), (20, 26, 0, 8), (28, 10, 0, 0), (36, 0, 0, 0))
a.rot("arm_r", (0, -4, 0, 18), (5, 40, 30, -40), (8, 46, 36, -48), (12, 30, 20, -60), (14, 110, 0, 70), (17, 120, 0, 80), (26, 60, 0, 30), (36, -4, 0, 18))
a.rot("fore_r", (0, 70, 30, 0), (5, 60, 0, 0), (12, 70, 0, 0), (14, 0, 0, 0), (26, 20, 0, 0), (36, 70, 30, 0))
a.rot("arm_l", (0, 14, 0, -6), (5, 50, -30, 40), (8, 56, -30, 46), (12, 40, -20, 56), (14, 110, 0, -70), (17, 120, 0, -80), (26, 60, 0, -30), (36, 14, 0, -6))
a.rot("fore_l", (0, 40, 0, 0), (5, 70, 0, 0), (12, 80, 0, 0), (14, 0, 0, 0), (26, 20, 0, 0), (36, 40, 0, 0))
a.rot("shells", (0, 0, 0, 0), (6, 0, 0, 0), (8, 0, 0, 6), (12, -6, 0, 8), (13.5, 0, 0, 0))
a.scl("shells", (0, 1, 1, 1), (13.5, 1, 1, 1), (14.2, 1.3, 1.3, 1.6), (14.8, .001, .001, .001), (28, .001, .001, .001), (31, 1, 1, 1))
legs(a, [(0, 0, 0, 2), (6, 20, 0, 6), (12, 34, 0, 10), (14, 10, 0, 14), (18, 4, 0, 12), (36, 0, 0, 2)],
     [(0, 4, 0, -4), (6, 20, 0, -6), (12, 34, 0, -10), (14, 10, 0, -14), (18, 4, 0, -12), (36, 4, 0, -4)],
     shin_r=[(0, 0, 0, 0), (6, -30, 0, 0), (12, -50, 0, 0), (14, -10, 0, 0), (36, 0, 0, 0)])
hair_all(a, [(0, -3, 0, 0), (12, 10, 0, 0), (14, -40, 0, 0), (19, -26, 0, 0), (28, -8, 0, 0), (36, -3, 0, 0)],
         [(0, 0, 0, 3), (12, 0, 0, 0), (14, -10, 0, 40), (22, 0, 0, 14), (36, 0, 0, 3)])
skirt(a, [(0, 0, 0, 0), (12, -4, 0, 0), (14, 16, 0, 0), (20, 6, 0, 0), (36, 0, 0, 0)], sides=[(0, 0, 0, 0), (14, 0, 0, 16), (24, 0, 0, 4), (36, 0, 0, 0)])
a.rot("antenna", (0, 0, 0, 0), (12, 10, 0, 0), (14, -24, 0, 0), (20, 10, 0, 0), (28, -4, 0, 0), (36, 0, 0, 0))
a.done()

# ------------------------------------------------------------------ mine_field (44): kneel 0..10, pirouette sowing mines 12..28, toss 20, hop away 32
a = A("mine_field", 44)
a.pos("root", (0, 0, 0, 0), (8, 0, -5.0, 0), (12, 0, -5.4, 0), (28, 0, -5.4, 0), (31, 0, -6.0, 0), (34, 0, 3.0, 3.0), (37, 0, 1.5, 4.5), (40, 0, -0.8, 4.5), (44, 0, 0, 4.0))
a.rot("root", (0, 0, 0, 0), (10, 0, 0, 0), (12, 0, 0, 0), (20, 0, -180, 0), (28, 0, -360, 0), (44, 0, -360, 0))
a.rot("body", (0, 0, 0, 0), (8, -10, 0, 0), (28, -10, 0, 0), (32, -16, 0, 0), (34, 14, 0, 0), (40, 4, 0, 0), (44, 0, 0, 0))
legs(a, [(0, 0, 0, 2), (8, 0, 0, 4), (28, 0, 0, 4), (31, 30, 0, 4), (34, -20, 0, 6), (37, 40, 0, 4), (41, 6, 0, 2), (44, 0, 0, 2)],
     [(0, 4, 0, -4), (8, 84, 0, -6), (28, 84, 0, -6), (31, 70, 0, -6), (34, -10, 0, -6), (37, 50, 0, -4), (41, 10, 0, -4), (44, 4, 0, -4)],
     shin_r=[(0, 0, 0, 0), (8, -84, 0, 0), (28, -84, 0, 0), (31, -90, 0, 0), (34, -10, 0, 0), (37, -70, 0, 0), (41, -14, 0, 0), (44, 0, 0, 0)],
     shin_l=[(0, -8, 0, 0), (8, -84, 0, 0), (28, -84, 0, 0), (31, -80, 0, 0), (34, -6, 0, 0), (37, -80, 0, 0), (41, -14, 0, 0), (44, -8, 0, 0)],
     foot_r=[(0, 0, 0, 0), (8, 40, 0, 0), (28, 40, 0, 0), (34, 0, 0, 0), (44, 0, 0, 0)], foot_l=[(0, 0, 0, 0), (8, 0, 0, 0), (34, 10, 0, 0), (44, 0, 0, 0)])
# right arm sows mines: flicks every 4 ticks from 12
ar = [(0, -4, 0, 18), (8, 30, 0, 60)]
fr = [(0, 70, 30, 0), (8, 10, 0, 0)]
for tk in (12, 16, 20, 24, 28):
    ar += [(tk - 1.5, 40, 0, 70), (tk, 10, 0, 50)]
    fr += [(tk - 1.5, 30, 0, 0), (tk, 0, 0, 0)]
ar += [(32, 150, 0, 30), (36, 160, 0, 40), (40, 30, 0, 20), (44, -4, 0, 18)]
fr += [(32, 10, 0, 0), (44, 70, 30, 0)]
a.rot("arm_r", *ar)
a.rot("fore_r", *fr)
a.rot("arm_l", (0, 14, 0, -6), (8, 20, 0, -20), (16, -30, 0, -30), (19, 60, 0, -20), (20, 80, 0, -14), (24, 30, 0, -40), (28, 20, 0, -50),
      (32, 150, 0, -30), (36, 160, 0, -40), (40, 30, 0, -20), (44, 14, 0, -6))
a.rot("fore_l", (0, 40, 0, 0), (16, 60, 0, 0), (20, 0, 0, 0), (28, 10, 0, 0), (44, 40, 0, 0))
a.rot("chest", (0, 0, 0, 0), (8, -10, 0, 0), (12, -14, 0, -8), (28, -14, 0, -8), (32, -10, 0, 0), (34, 14, 0, 0), (44, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (8, -4, 0, 0), (12, -10, 20, 0), (28, -10, 20, 0), (34, 24, 0, 6), (40, 10, 0, 0), (44, 0, 0, 0))
hair_all(a, [(0, -3, 0, 0), (8, 6, 0, 0), (12, -30, 30, 0), (28, -34, 30, 0), (32, -10, 0, 0), (34, 30, 0, 0), (38, -20, 0, 0), (44, -3, 0, 0)],
         [(0, 0, 0, 3), (12, -10, 0, 50), (28, -10, 0, 50), (34, 20, 0, -10), (40, 0, 0, 6), (44, 0, 0, 3)],
         [(0, 0, 0, -3), (12, -10, 0, -20), (28, -10, 0, -20), (34, 20, 0, 10), (40, 0, 0, -6), (44, 0, 0, -3)])
skirt(a, [(0, 0, 0, 0), (8, 30, 0, 0), (12, 26, 0, 0), (28, 26, 0, 0), (34, -10, 0, 0), (38, 10, 0, 0), (44, 0, 0, 0)],
      [(0, 0, 0, 0), (8, -10, 0, 0), (28, -10, 0, 0), (34, -26, 0, 0), (38, -6, 0, 0), (44, 0, 0, 0)],
      sides=[(0, 0, 0, 0), (12, 0, 0, 26), (28, 0, 0, 26), (34, 0, 0, 6), (44, 0, 0, 0)])
a.rot("antenna", (0, 0, 0, 0), (12, 0, 0, 20), (28, 0, 0, 20), (34, -20, 0, 0), (40, 8, 0, 0), (44, 0, 0, 0))
a.done()

# ------------------------------------------------------------------ rocket (44): yank launcher from hair 8, kneel + shoulder it, load 20, FIRE 24
a = A("rocket", 44)
a.show("launcher", 8.5, 39, 1.0, grow=1.5)
a.scl("rflash", HIDE, (23.6, .001, .001, .001), (24.2, 1.3, 1.3, 1.0), (26, 0.8, 0.8, 1.6), (27.5, .001, .001, .001))
a.scl("bblast", HIDE, (23.6, .001, .001, .001), (24.4, 1, 1, 1), (27, 1.2, 1.2, 1.8), (30, .001, .001, .001))
a.rot("launcher", (0, -40, 0, 0), (8.5, -60, 30, 0), (12, -10, 10, 0), (16, 0, 0, 0), (23.5, 0, 0, 0), (24.5, 9, 0, 0), (28, 2, 0, 0), (34, 0, 0, 0), (38, -30, 0, 0))
a.pos("launcher", (0, 0, 4, 2), (8.5, 0, 4, 2), (14, 0, 0, 0), (23.5, 0, 0, 0), (24.5, 0, 0.4, 1.4), (28, 0, 0, 0.3), (34, 0, 0, 0), (39, 0, 2, 2))
a.rot("arm_r", (0, -4, 0, 18), (4, 150, -20, 10), (8, 170, -30, 10), (12, 110, 0, 10), (16, 60, 0, 4), (24, 60, 0, 4), (25, 70, 0, 4), (34, 60, 0, 4), (40, 20, 0, 14), (44, -4, 0, 18))
a.rot("fore_r", (0, 70, 30, 0), (4, 80, 0, 0), (8, 70, 0, 0), (16, 70, 0, 0), (34, 70, 0, 0), (44, 70, 30, 0))
a.rot("arm_l", (0, 14, 0, -6), (8, 30, 0, -10), (14, 80, 30, 30), (18, 60, 40, 40), (20, 86, 30, 30), (24, 80, 30, 30), (25, 60, 30, 30), (34, 76, 30, 30), (40, 30, 0, -6), (44, 14, 0, -6))
a.rot("fore_l", (0, 40, 0, 0), (14, 40, 0, 0), (18, 70, 0, 0), (20, 30, 0, 0), (34, 30, 0, 0), (44, 40, 0, 0))
a.pos("root", (0, 0, 0, 0), (10, 0, -1.0, 0), (16, 0, -3.6, 0), (24, 0, -3.6, 0), (25, 0, -3.6, 1.2), (34, 0, -3.6, 0.8), (40, 0, -0.5, 0.4), (44, 0, 0, 0))
legs(a, [(0, 0, 0, 2), (16, -10, 0, 4), (34, -10, 0, 4), (40, 0, 0, 2), (44, 0, 0, 2)], [(0, 4, 0, -4), (16, 70, 0, -6), (34, 70, 0, -6), (40, 20, 0, -4), (44, 4, 0, -4)],
     shin_r=[(0, 0, 0, 0), (16, -90, 0, 0), (34, -90, 0, 0), (40, -20, 0, 0), (44, 0, 0, 0)],
     shin_l=[(0, -8, 0, 0), (16, -70, 0, 0), (34, -70, 0, 0), (40, -20, 0, 0), (44, -8, 0, 0)])
a.rot("chest", (0, 0, 0, 0), (4, 6, 20, 0), (8, 10, 30, 0), (16, -4, 10, 0), (23.5, -6, 10, 0), (24.5, 8, 10, 0), (28, 2, 10, 0), (34, 0, 6, 0), (44, 0, 0, 0))
a.rot("body", (0, 0, 0, 0), (16, -6, 0, 0), (24, -6, 0, 0), (25, 6, 0, 0), (30, -2, 0, 0), (44, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (6, -10, 30, 0), (12, 0, 0, 0), (16, -4, 6, -10), (24, -4, 6, -10), (25, 14, 0, -4), (30, 0, 0, -6), (44, 0, 0, 0))
hair_all(a, [(0, -3, 0, 0), (6, -10, 10, 0), (12, 10, 0, 0), (16, -6, 0, 0), (25, -30, 0, 0), (30, -12, 0, 0), (44, -3, 0, 0)],
         [(0, 0, 0, 3), (8, -10, 0, 20), (16, 0, 0, 4), (25, -20, 0, 20), (34, 0, 0, 6), (44, 0, 0, 3)])
skirt(a, [(0, 0, 0, 0), (16, 24, 0, 0), (24, 24, 0, 0), (25, 34, 0, 0), (34, 24, 0, 0), (44, 0, 0, 0)],
      [(0, 0, 0, 0), (16, -14, 0, 0), (34, -14, 0, 0), (44, 0, 0, 0)])
a.rot("antenna", (0, 0, 0, 0), (8, 10, 0, -10), (25, -24, 0, 0), (30, 10, 0, 0), (36, 0, 0, 0))
a.done()

# ------------------------------------------------------------------ bomb_rain (56): cheer, crouch with bombs 13, hurl skyward 15, gleeful conducting 22..46
a = A("bomb_rain", 56)
a.show("bomb_r", 0, 15, 1.0, grow=1.0)
nade_hide(a, 15, 50)
a.pos("root", (0, 0, 0, 0), (2, 0, 1.5, 0), (4, 0, 0, 0), (13, 0, -1.5, 0), (15, 0, 2.5, 0), (17, 0, 0.5, 0), (19, 0, 0, 0), (56, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (13, 0, -1.8, 0), (15, 0, 0.4, 0), (18, 0, 0, 0), *[(t, 0, -0.6 if (t - 22) % 6 == 0 else 0, 0) for t in range(22, 47, 3)], (56, 0, 0, 0))
a.rot("arm_r", (0, -4, 0, 18), (2, 160, 0, 30), (4, 150, 0, 20), (8, -10, 0, 20), (13, -40, 0, 16), (15, 175, 0, 6), (18, 168, 0, 10),
      *[(t, 120 + (20 if (t - 22) % 6 == 0 else -10), 0, 30) for t in range(22, 47, 3)], (50, 30, 0, 18), (56, -4, 0, 18))
a.rot("fore_r", (0, 70, 30, 0), (4, 10, 0, 0), (13, 20, 0, 0), (15, 0, 0, 0), (46, 20, 0, 0), (56, 70, 30, 0))
a.rot("arm_l", (0, 14, 0, -6), (2, 160, 0, -30), (4, 150, 0, -20), (8, -10, 0, -20), (13, -40, 0, -16), (15, 175, 0, -6), (18, 168, 0, -10),
      *[(t, 120 + (-10 if (t - 22) % 6 == 0 else 20), 0, -30) for t in range(22, 47, 3)], (50, 30, 0, -10), (56, 14, 0, -6))
a.rot("fore_l", (0, 40, 0, 0), (4, 10, 0, 0), (13, 20, 0, 0), (15, 0, 0, 0), (46, 20, 0, 0), (56, 40, 0, 0))
a.rot("chest", (0, 0, 0, 0), (13, -16, 0, 0), (15, 16, 0, 0), (20, 12, 0, 0), (34, 10, 10, 0), (46, 10, -10, 0), (56, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (2, 10, 0, 8), (13, -6, 0, 0), (15, 30, 0, 0), (20, 36, 0, 0), (30, 20, 20, 0), (40, 20, -20, 0), (46, 14, 0, 0), (56, 0, 0, 0))
legs(a, [(0, 0, 0, 2), (2, -10, 0, 6), (4, 0, 0, 2), (13, 30, 0, 6), (15, -6, 0, 4), (18, 0, 0, 2), (56, 0, 0, 2)],
     [(0, 4, 0, -4), (2, 20, 0, -6), (4, 4, 0, -4), (13, 30, 0, -6), (15, -6, 0, -4), (18, 4, 0, -4), (56, 4, 0, -4)],
     shin_r=[(0, 0, 0, 0), (2, -30, 0, 0), (4, 0, 0, 0), (13, -50, 0, 0), (15, 0, 0, 0), (56, 0, 0, 0)])
hair_all(a, [(0, -3, 0, 0), (2, 20, 0, 0), (13, 6, 0, 0), (15, 26, 0, 0), (19, -20, 0, 0)] + [(t, -6 if t % 2 else -12, 0, 0) for t in range(24, 47, 6)] + [(56, -3, 0, 0)],
         [(0, 0, 0, 3), (15, 20, 0, 20), (22, 0, 0, 8), (46, 0, 0, 8), (56, 0, 0, 3)])
skirt(a, [(0, 0, 0, 0), (2, -10, 0, 0), (13, 10, 0, 0), (15, -12, 0, 0), (20, 4, 0, 0), (56, 0, 0, 0)], sides=[(0, 0, 0, 0), (15, 0, 0, 14), (22, 0, 0, 4), (56, 0, 0, 0)])
a.rot("antenna", (0, 0, 0, 0), (2, -16, 0, 0), (15, 20, 0, 0), (18, -10, 0, 0), *[(t, 0, 0, 8 if (t // 6) % 2 else -8) for t in range(22, 47, 6)], (56, 0, 0, 0))
a.done()

# ------------------------------------------------------------------ kamikaze (50): light antenna 6, sprint crouch, dive-hug 16, squeeze, BOOM 28, blown back
a = A("kamikaze", 50)
a.scl("spark", HIDE, (5.5, .001, .001, .001), (6.5, 1.2, 1.2, 1.2), *[(t, 1.4 if t % 2 else 0.9, 1.6 if t % 2 else 1.0, 1.4 if t % 2 else 0.9) for t in range(8, 28)], (28, 2.0, 2.0, 2.0), (29, .001, .001, .001))
a.scl("blast", HIDE, (27.6, .001, .001, .001), (28.4, 0.7, 0.7, 0.7), (30, 1.3, 1.3, 1.3), (32, 1.0, 1.0, 1.0), (34, .001, .001, .001))
a.rot("blast", (0, 0, 0, 0), (28, 0, 0, 0), (34, 0, 90, 0))
a.rot("arm_r", (0, -4, 0, 18), (4, 170, -30, 0), (6, 176, -30, 0), (7, 150, -30, 0), (10, -40, 0, 30), (15, -50, 0, 40), (17, 90, -40, 40), (20, 90, -60, 20),
      (27, 90, -70, 10), (29, 160, 0, 90), (33, 170, 0, 110), (40, 40, 0, 40), (50, -4, 0, 18))
a.rot("fore_r", (0, 70, 30, 0), (4, 60, 0, 0), (7, 40, 0, 0), (10, 10, 0, 0), (17, 20, 0, 0), (20, 50, 0, 0), (27, 60, 0, 0), (29, 0, 0, 0), (50, 70, 30, 0))
a.rot("arm_l", (0, 14, 0, -6), (6, 20, 0, -10), (10, -40, 0, -30), (15, -50, 0, -40), (17, 90, 40, -40), (20, 90, 60, -20), (27, 90, 70, -10),
      (29, 160, 0, -90), (33, 170, 0, -110), (40, 40, 0, -40), (50, 14, 0, -6))
a.rot("fore_l", (0, 40, 0, 0), (10, 10, 0, 0), (17, 20, 0, 0), (20, 50, 0, 0), (27, 60, 0, 0), (29, 0, 0, 0), (50, 40, 0, 0))
a.rot("head", (0, 0, 0, 0), (4, 20, 0, 6), (6, 26, 0, 10), (9, 10, 0, -14), (12, 16, 0, 14), (15, 16, 0, 0), (20, -6, 0, 0), (24, 10, 0, 10), (27, -10, 0, -8),
      (29, 30, 0, 0), (34, 20, 30, 10), (38, 10, -30, -10), (42, 6, 20, 6), (50, 0, 0, 0))
a.rot("body", (0, 0, 0, 0), (10, -24, 0, 0), (15, -30, 0, 0), (17, -50, 0, 0), (20, -40, 0, 0), (27, -40, 0, 0), (29, 30, 0, 0), (33, 40, 0, 0), (38, 0, 0, 6), (42, 0, 0, -6), (50, 0, 0, 0))
a.rot("chest", (0, 0, 0, 0), (6, 10, 0, 0), (10, -10, 0, 0), (20, 0, 0, 0), *[(t, 0, 0, 4 if t % 2 else -4) for t in range(21, 28)], (29, 20, 0, 0), (50, 0, 0, 0))
a.pos("root", (0, 0, 0, 0), (10, 0, -1.2, 0), (15, 0, -1.8, 0), (17, 0, 1.4, -2), (20, 0, 0.6, -2.5), (27, 0, 0.6, -2.5), (30, 0, 3.0, 2.0), (34, 0, 1.0, 4.0), (37, 0, 0, 4.0), (50, 0, 0, 0))
legs(a, [(0, 0, 0, 2), (10, 40, 0, 4), (15, 50, 0, 4), (17, -40, 0, 4), (20, -30, 0, 10), (27, -30, 0, 10), (30, 60, 0, 20), (34, 50, 0, 10), (38, 10, 0, 4), (50, 0, 0, 2)],
     [(0, 4, 0, -4), (10, -10, 0, -4), (15, -20, 0, -4), (17, -50, 0, -4), (20, -40, 0, -10), (27, -40, 0, -10), (30, 70, 0, -20), (34, 50, 0, -10), (38, 6, 0, -4), (50, 4, 0, -4)],
     shin_r=[(0, 0, 0, 0), (10, -60, 0, 0), (15, -70, 0, 0), (17, -10, 0, 0), (20, -40, 0, 0), (27, -40, 0, 0), (30, -10, 0, 0), (34, -40, 0, 0), (38, -10, 0, 0), (50, 0, 0, 0)],
     shin_l=[(0, -8, 0, 0), (10, -30, 0, 0), (17, -20, 0, 0), (20, -60, 0, 0), (27, -60, 0, 0), (30, -10, 0, 0), (34, -40, 0, 0), (38, -10, 0, 0), (50, -8, 0, 0)])
hair_all(a, [(0, -3, 0, 0), (10, -10, 0, 0), (17, -50, 0, 0), (27, -40, 0, 0), (29, 50, 0, 0), (33, 60, 0, 0), (38, -10, 0, 0), (44, -6, 0, 0), (50, -3, 0, 0)],
         [(0, 0, 0, 3), (17, -30, 0, 20), (27, -30, 0, 20), (29, 30, 0, 50), (36, 0, 0, 10), (50, 0, 0, 3)])
skirt(a, [(0, 0, 0, 0), (10, 10, 0, 0), (17, -20, 0, 0), (27, -16, 0, 0), (29, 50, 0, 0), (34, 30, 0, 0), (40, 0, 0, 0), (50, 0, 0, 0)],
      sides=[(0, 0, 0, 0), (29, 0, 0, 30), (36, 0, 0, 6), (50, 0, 0, 0)])
a.rot("antenna", (0, 0, 0, 0), (4, -20, 0, 0), (6, 10, 0, 0), (10, -16, 0, 0), (17, -30, 0, 0), (27, -24, 0, 0), (29, 40, 0, 0), (34, 20, 0, 30), (40, -10, 0, -10), (46, 4, 0, 0), (50, 0, 0, 0))
a.rot("spiral", (0, 0, 0, 0), (29, 0, 0, 0), (32, 0, 0, 60), (38, 0, 0, -20), (44, 0, 0, 0))
a.done()

# ------------------------------------------------------------------ stomp (32): knee up 0..9, hop 9, explosive STOMP 13, dust settle
a = A("stomp", 32)
a.pos("root", (0, 0, 0, 0), (7, 0, 0, 0), (10, 0, 2.2, 0), (12.5, 0, 0.4, 0), (13, 0, -0.4, 0), (16, 0, -1.0, 0), (24, 0, -0.4, 0), (32, 0, 0, 0))
legs(a, [(0, 0, 0, 2), (7, 100, 0, 8), (10, 110, 0, 8), (12.5, 30, 0, 4), (13, 14, 0, 6), (16, 20, 0, 8), (32, 0, 0, 2)],
     [(0, 4, 0, -4), (7, -6, 0, -4), (10, 10, 0, -4), (13, -10, 0, -8), (16, -14, 0, -8), (32, 4, 0, -4)],
     shin_r=[(0, 0, 0, 0), (7, -100, 0, 0), (10, -110, 0, 0), (12.5, -20, 0, 0), (13, -10, 0, 0), (16, -30, 0, 0), (32, 0, 0, 0)],
     shin_l=[(0, -8, 0, 0), (7, -6, 0, 0), (10, -50, 0, 0), (13, -10, 0, 0), (16, -26, 0, 0), (32, -8, 0, 0)],
     foot_r=[(0, 0, 0, 0), (7, 30, 0, 0), (12.5, 0, 0, 0), (32, 0, 0, 0)])
a.rot("body", (0, 0, 0, 0), (7, 10, 0, -6), (10, 12, 0, -6), (13, -18, 0, 4), (16, -22, 0, 4), (24, -6, 0, 0), (32, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (13, 0, -1.6, 0), (16, 0, -2.2, 0), (24, 0, -0.6, 0), (32, 0, 0, 0))
a.rot("arm_r", (0, -4, 0, 18), (7, 20, 0, 70), (10, 30, 0, 90), (13, -30, 0, 40), (16, -40, 0, 50), (24, -10, 0, 20), (32, -4, 0, 18))
a.rot("arm_l", (0, 14, 0, -6), (7, 20, 0, -70), (10, 30, 0, -90), (13, -30, 0, -40), (16, -40, 0, -50), (24, 0, 0, -10), (32, 14, 0, -6))
a.rot("fore_r", (0, 70, 30, 0), (7, 20, 0, 0), (13, 30, 0, 0), (32, 70, 30, 0))
a.rot("fore_l", (0, 40, 0, 0), (7, 20, 0, 0), (13, 40, 0, 0), (32, 40, 0, 0))
a.rot("head", (0, 0, 0, 0), (7, 16, 0, 6), (10, 20, 0, 6), (13, -16, 0, 0), (16, -20, 0, 0), (20, 10, 0, 0), (32, 0, 0, 0))
hair_all(a, [(0, -3, 0, 0), (10, 20, 0, 0), (13, -30, 0, 0), (16, 20, 0, 0), (22, -10, 0, 0), (32, -3, 0, 0)],
         [(0, 0, 0, 3), (10, -10, 0, 6), (13, -20, 0, 30), (18, 0, 0, 10), (32, 0, 0, 3)])
skirt(a, [(0, 0, 0, 0), (7, 30, 0, 0), (10, 34, 0, 0), (13, -10, 0, 0), (15, 16, 0, 0), (20, 4, 0, 0), (32, 0, 0, 0)],
      [(0, 0, 0, 0), (10, -6, 0, 0), (13, -24, 0, 0), (18, -6, 0, 0), (32, 0, 0, 0)], sides=[(0, 0, 0, 0), (13, 0, 0, 24), (18, 0, 0, 6), (32, 0, 0, 0)])
a.rot("antenna", (0, 0, 0, 0), (10, -14, 0, 0), (13, 30, 0, 0), (16, -16, 0, 0), (22, 6, 0, 0), (32, 0, 0, 0))
a.done()

# ------------------------------------------------------------------ kick_back (38): flick grenade up 4, it drops, wind leg 12, VOLLEY 16
a = A("kick_back", 38)
nade_hide(a, 5, 30)
a.scl("air_bomb", HIDE, (4.6, .001, .001, .001), (5, 1, 1, 1), (16.5, 1, 1, 1), (18, .001, .001, .001))
a.pos("air_bomb", (0, -3.5, 10, 3.5), (5, -3.5, 10, 3.5), (9, -2.0, 16, 2), (12, -1, 13, 0.5), (15, 0, 4, 0), (16, 0, 2, 0), (17.5, 0, 4, -12))
a.rot("air_bomb", (0, 0, 0, 0), (16, 300, 0, 0), (18, 500, 0, 0))
a.rot("arm_l", (0, 14, 0, -6), (3, 40, 0, -10), (5, 90, 0, -10), (8, 40, 0, -40), (16, -20, 0, -70), (20, -10, 0, -60), (30, 10, 0, -10), (38, 14, 0, -6))
a.rot("fore_l", (0, 40, 0, 0), (3, 60, 0, 0), (5, 10, 0, 0), (16, 10, 0, 0), (38, 40, 0, 0))
a.rot("arm_r", (0, -4, 0, 18), (8, 10, 0, 40), (12, 40, 0, 60), (16, -40, 0, 70), (22, -20, 0, 40), (38, -4, 0, 18))
a.rot("fore_r", (0, 70, 30, 0), (12, 20, 0, 0), (38, 70, 30, 0))
legs(a, [(0, 0, 0, 2), (8, 0, 0, 2), (12, -60, 0, 6), (14, -10, 0, 4), (16, 100, 0, 4), (19, 110, 0, 4), (26, 20, 0, 2), (38, 0, 0, 2)],
     [(0, 4, 0, -4), (12, 16, 0, -4), (16, -12, 0, -4), (20, -8, 0, -4), (38, 4, 0, -4)],
     shin_r=[(0, 0, 0, 0), (12, -90, 0, 0), (14, -60, 0, 0), (16, -4, 0, 0), (19, 0, 0, 0), (26, -20, 0, 0), (38, 0, 0, 0)],
     shin_l=[(0, -8, 0, 0), (12, -20, 0, 0), (16, -10, 0, 0), (38, -8, 0, 0)], foot_r=[(0, 0, 0, 0), (12, 30, 0, 0), (16, -20, 0, 0), (26, 0, 0, 0)])
a.rot("body", (0, 0, 0, 0), (12, -8, 10, 0), (16, 24, -10, 0), (19, 28, -14, 0), (26, 6, 0, 0), (38, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (12, 0, -0.6, 0), (16, 0, 0, 0.6), (26, 0, 0, 0), (38, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (5, 24, 0, 0), (9, 30, 0, 0), (12, 0, 0, 0), (15, -24, 0, 0), (16, -26, 0, 0), (20, -10, 0, 8), (38, 0, 0, 0))
hair_all(a, [(0, -3, 0, 0), (12, -10, 0, 0), (16, -40, -10, 0), (20, -30, 0, 0), (28, -8, 0, 0), (38, -3, 0, 0)],
         [(0, 0, 0, 3), (16, -20, 0, 20), (26, 0, 0, 6), (38, 0, 0, 3)])
skirt(a, [(0, 0, 0, 0), (12, -12, 0, 0), (16, 50, 0, 0), (19, 55, 0, 0), (24, 14, 0, 0), (38, 0, 0, 0)],
      [(0, 0, 0, 0), (12, -6, 0, 0), (16, -20, 0, 0), (24, -6, 0, 0), (38, 0, 0, 0)], sides=[(0, 0, 0, 0), (16, 0, 0, 20), (26, 0, 0, 4), (38, 0, 0, 0)])
a.rot("antenna", (0, 0, 0, 0), (5, -10, 0, 0), (16, 20, 0, 10), (22, -8, 0, 0), (30, 0, 0, 0))
a.done()

# ------------------------------------------------------------------ boom_punch (24): grenade fist cocked 0..8, dash 8, BOOM 11, shake out
a = A("boom_punch", 24)
a.scl("fist_flash", HIDE, (10.6, .001, .001, .001), (11.2, 1.1, 1.1, 1.1), (12.5, 1.4, 1.4, 1.4), (14, .001, .001, .001))
a.rot("arm_l", (0, 14, 0, -6), (5, -50, 0, -20), (8, -60, 0, -24), (10, 70, 0, -4), (11, 96, 0, 0), (13, 100, 0, 0), (17, 60, 0, -10), (24, 14, 0, -6))
a.rot("fore_l", (0, 40, 0, 0), (5, 100, 0, 0), (8, 110, 0, 0), (10, 20, 0, 0), (11, 0, 0, 0), (17, 30, 0, 0), (24, 40, 0, 0))
a.rot("chest", (0, 0, 0, 0), (5, 4, 36, 0), (8, 6, 40, 0), (11, -14, -34, 0), (14, -10, -30, 0), (24, 0, 0, 0))
a.rot("body", (0, 0, 0, 0), (8, -6, 16, 0), (11, -16, -16, 0), (16, -8, -6, 0), (24, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (8, 0, -1.0, 0.6), (11, 0, -1.4, -1.6), (16, 0, -0.6, -0.8), (24, 0, 0, 0))
a.rot("arm_r", (0, -4, 0, 18), (8, 40, 0, 30), (11, -40, 0, 30), (16, -20, 0, 24), (24, -4, 0, 18))
a.rot("fore_r", (0, 70, 30, 0), (8, 80, 0, 0), (11, 40, 0, 0), (24, 70, 30, 0))
a.rot("head", (0, 0, 0, 0), (8, -6, -20, 0), (11, -4, 20, 0), (13, 10, 20, 0), (24, 0, 0, 0))
legs(a, [(0, 0, 0, 2), (8, 20, 0, 4), (11, -30, 0, 4), (16, -20, 0, 2), (24, 0, 0, 2)], [(0, 4, 0, -4), (8, -10, 0, -4), (11, 50, 0, -4), (16, 30, 0, -4), (24, 4, 0, -4)],
     shin_r=[(0, 0, 0, 0), (8, -40, 0, 0), (11, -10, 0, 0), (24, 0, 0, 0)], shin_l=[(0, -8, 0, 0), (8, -20, 0, 0), (11, -50, 0, 0), (16, -30, 0, 0), (24, -8, 0, 0)])
hair_all(a, [(0, -3, 0, 0), (8, 4, 20, 0), (11, -30, -20, 0), (14, -40, 0, 0), (19, -12, 0, 0), (24, -3, 0, 0)], [(0, 0, 0, 3), (11, -10, 0, 20), (24, 0, 0, 3)])
skirt(a, [(0, 0, 0, 0), (8, 6, 0, 0), (11, 30, 0, 0), (16, 10, 0, 0), (24, 0, 0, 0)], sides=[(0, 0, 0, 0), (11, 0, 0, 12), (24, 0, 0, 0)])
a.rot("antenna", (0, 0, 0, 0), (8, 6, 0, 10), (11, -20, 0, -10), (16, 8, 0, 0), (24, 0, 0, 0))
a.done()

# ------------------------------------------------------------------ carpet_bomb (72, enraged): cackle, detonator out of the bag, CLICK 15, conduct the rockets 18..57
a = A("carpet_bomb", 72)
a.show("det", 8, 64, 1.0)
a.rot("head", (0, 0, 0, 0), (2, 30, 0, 6), (4, 34, 0, -6), (6, 30, 0, 6), (10, -14, 10, 0), (15, 10, 0, 0), (17, 24, 0, 0),
      *[(t, 6 + (6 if (t - 18) % 6 == 0 else 0), 6 * math.sin(t / 4), 4 * math.sin(t / 3)) for t in range(18, 58, 3)], (64, 6, 0, 0), (72, 0, 0, 0))
a.rot("chest", (0, 0, 0, 0), (3, 16, 0, 0), (6, 10, 0, 0), (10, -10, -20, 0), (15, 6, 10, 0), (18, 4, 0, 0),
      *[(t, 4, 8 * math.sin(t / 5), 0) for t in range(20, 58, 4)], (64, 2, 0, 0), (72, 0, 0, 0))
a.rot("arm_r", (0, -4, 0, 18), (6, -4, 0, 18), (9, 20, 20, -10), (12, 120, 0, 10), (14, 150, 0, 10), (15, 156, 0, 6), (16, 140, 0, 10),
      *[(t, 90 + 10 * math.sin(t / 3), -20 * math.sin(t / 6), 10) for t in range(20, 58, 3)], (62, 60, 0, 10), (72, -4, 0, 18))
a.rot("fore_r", (0, 70, 30, 0), (9, 90, 0, 0), (12, 20, 0, 0), (16, 10, 0, 0), (58, 6, 0, 0), (72, 70, 30, 0))
a.rot("hand_r", (0, 0, 0, 0), (14.5, 0, 0, 0), (15, -20, 0, 0), (16, 0, 0, 0), (72, 0, 0, 0))
a.rot("arm_l", (0, 14, 0, -6), (2, -20, 0, -30), (6, -20, 0, -30), (12, 20, 0, -10), (18, 140, 0, -40),
      *[(t, 140 + (20 if (t // 3) % 2 else -20), 0, -40) for t in range(21, 58, 3)], (62, 40, 0, -10), (72, 14, 0, -6))
a.rot("fore_l", (0, 40, 0, 0), (2, 100, 0, 0), (6, 100, 0, 0), (18, 20, 0, 0), (58, 20, 0, 0), (72, 40, 0, 0))
a.pos("root", (0, 0, 0, 0), (18, 0, 0, 0), *[(t, 0, 1.4 if (t - 18) % 6 == 3 else 0, 0) for t in range(18, 58, 3)], (72, 0, 0, 0))
legs(a, [(0, 0, 0, 2)] + [(t, (16 if (t - 18) % 12 == 3 else 0), 0, 2) for t in range(18, 58, 3)] + [(72, 0, 0, 2)],
     [(0, 4, 0, -4)] + [(t, (16 if (t - 18) % 12 == 9 else 4), 0, -4) for t in range(18, 58, 3)] + [(72, 4, 0, -4)],
     shin_r=[(0, 0, 0, 0)] + [(t, (-40 if (t - 18) % 12 == 3 else 0), 0, 0) for t in range(18, 58, 3)] + [(72, 0, 0, 0)],
     shin_l=[(0, -8, 0, 0)] + [(t, (-40 if (t - 18) % 12 == 9 else -8), 0, 0) for t in range(18, 58, 3)] + [(72, -8, 0, 0)])
hair_all(a, [(0, -3, 0, 0), (3, -16, 0, 0), (10, -6, 10, 0), (15, -14, 0, 0)] + [(t, -6 if (t // 3) % 2 else -14, 4 * math.sin(t / 4), 0) for t in range(18, 58, 3)] + [(72, -3, 0, 0)],
         [(0, 0, 0, 3)] + [(t, 0, 0, 3 + (8 if (t // 3) % 2 else 0)) for t in range(18, 58, 3)] + [(72, 0, 0, 3)])
skirt(a, [(0, 0, 0, 0)] + [(t, 4 if (t // 3) % 2 else -4, 0, 0) for t in range(18, 58, 3)] + [(72, 0, 0, 0)],
      sides=[(0, 0, 0, 0)] + [(t, 0, 0, 8 if (t // 3) % 2 else 0) for t in range(18, 58, 3)] + [(72, 0, 0, 0)])
a.rot("antenna", (0, 0, 0, 0), (3, -10, 0, 0), (15, 10, 0, 0), *[(t, 0, 0, 10 if (t // 3) % 2 else -10) for t in range(18, 58, 3)], (72, 0, 0, 0))
a.scl("spark", HIDE, (14.5, .001, .001, .001), *[(t, 0.6 if t % 2 else 1.0, 0.6 if t % 2 else 1.0, 0.6 if t % 2 else 1.0) for t in range(15, 58)], (60, .001, .001, .001))
a.done()

# ------------------------------------------------------------------ claw_swipe (30): canon claw rake 9, rising backhand 17
a = A("claw_swipe", 30)
a.rot("body", (0, 0, 0, 0), (5, 0, 40, 0), (9, -8, -30, 0), (13, -2, -36, 0), (17, -10, 26, 0), (21, -6, 20, 0), (30, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (5, 0, -0.8, 0.8), (9, 0, -1.2, -1.4), (13, 0, -0.8, -0.4), (17, 0, -1.0, -1.6), (30, 0, 0, 0))
a.rot("chest", (0, 0, 0, 0), (5, 6, 20, 0), (9, -10, -20, 0), (13, 0, -20, 0), (17, 6, 16, 0), (21, 4, 10, 0), (30, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (5, 0, -40, 0), (9, -4, 30, 0), (13, 4, 30, 0), (17, 10, -20, 0), (30, 0, 0, 0))
a.rot("arm_r", (0, -4, 0, 18), (5, 40, 50, 80), (8, 90, -30, 40), (9, 90, -60, 10), (11, 70, -80, 0), (13, 30, 0, 40), (15, 10, 0, 30),
      (17, 160, 0, 30), (19, 170, 0, 20), (24, 40, 0, 20), (30, -4, 0, 18))
a.rot("fore_r", (0, 70, 30, 0), (5, 70, 0, 0), (9, 10, 0, 0), (13, 60, 0, 0), (17, 0, 0, 0), (24, 30, 0, 0), (30, 70, 30, 0))
a.rot("hand_r", (0, 0, 0, 0), (5, -30, 0, 0), (9, 30, 0, 0), (13, -10, 0, 0), (17, -40, 0, 0), (30, 0, 0, 0))
a.rot("arm_l", (0, 14, 0, -6), (5, -20, 0, -30), (9, 20, 0, -20), (13, -10, 0, -30), (17, -30, 0, -14), (30, 14, 0, -6))
a.rot("fore_l", (0, 40, 0, 0), (9, 60, 0, 0), (30, 40, 0, 0))
legs(a, [(0, 0, 0, 2), (5, -12, 0, 2), (9, 26, 0, 2), (13, 20, 0, 2), (17, 34, 0, 2), (30, 0, 0, 2)],
     [(0, 4, 0, -4), (5, 16, 0, -4), (9, -20, 0, -4), (13, -16, 0, -4), (17, -26, 0, -4), (30, 4, 0, -4)],
     shin_r=[(0, 0, 0, 0), (9, -20, 0, 0), (17, -24, 0, 0), (30, 0, 0, 0)], shin_l=[(0, -8, 0, 0), (5, -30, 0, 0), (9, -10, 0, 0), (30, -8, 0, 0)])
hair_all(a, [(0, -3, 0, 0), (5, -6, -30, 0), (9, -16, 30, 0), (13, -10, 20, 0), (17, -24, -20, 0), (22, -10, -6, 0), (30, -3, 0, 0)],
         [(0, 0, 0, 3), (5, 0, 0, -10), (9, -10, 0, 24), (17, -10, 0, -6), (30, 0, 0, 3)])
skirt(a, [(0, 0, 0, 0), (5, -4, 0, -6), (9, 14, 0, 10), (13, 8, 0, 6), (17, 18, 0, -8), (24, 4, 0, 0), (30, 0, 0, 0)],
      sides=[(0, 0, 0, 0), (9, 0, 0, 14), (17, 0, 0, -6), (30, 0, 0, 0)])
a.rot("antenna", (0, 0, 0, 0), (5, 0, 0, 14), (9, 0, 0, -18), (17, -10, 0, 14), (24, 4, 0, -4), (30, 0, 0, 0))
a.done()

# ------------------------------------------------------------------ smoke_bomb (40): raise 0..8, SLAM 10 (cloud), spin-hop out 14..22, lob a bomb back 26
a = A("smoke_bomb", 40)
nade_hide(a, 10, 34)
a.show("bomb_r", 18, 26, 1.0)
a.scl("smoke", HIDE, (9.6, .001, .001, .001), (11, 0.6, 0.5, 0.6), (16, 1.1, 1.0, 1.1), (26, 1.3, 1.2, 1.3), (32, 1.0, 0.6, 1.0), (37, .001, .001, .001))
a.rot("smoke", (0, 0, 0, 0), (10, 0, 0, 0), (37, 0, 80, 0))
a.rot("arm_l", (0, 14, 0, -6), (6, 160, 0, -10), (8, 170, 0, -6), (10, 20, 0, -10), (12, 10, 0, -14), (16, 120, 0, -60), (22, 100, 0, -40), (30, 20, 0, -10), (40, 14, 0, -6))
a.rot("fore_l", (0, 40, 0, 0), (6, 20, 0, 0), (10, 0, 0, 0), (16, 20, 0, 0), (40, 40, 0, 0))
a.rot("arm_r", (0, -4, 0, 18), (8, -20, 0, 30), (10, -30, 0, 40), (16, 120, 0, 60), (22, 60, 0, 30), (24, -50, 0, 30), (26, 120, 0, 10), (28, 110, 0, 10), (34, 20, 0, 18), (40, -4, 0, 18))
a.rot("fore_r", (0, 70, 30, 0), (16, 20, 0, 0), (24, 70, 0, 0), (26, 10, 0, 0), (40, 70, 30, 0))
a.pos("root", (0, 0, 0, 0), (8, 0, 0.6, 0), (10, 0, -2.4, 0), (13, 0, -2.6, 0), (17, 0, 3.6, 0), (20, 0, 2.6, 0), (22, 0, -1.0, 0), (25, 0, 0, 0), (40, 0, 0, 0))
a.rot("root", (0, 0, 0, 0), (13, 0, 0, 0), (22, 0, 360, 0), (40, 0, 360, 0))
a.rot("body", (0, 0, 0, 0), (8, 10, 0, 0), (10, -30, 0, 0), (13, -30, 0, 0), (17, 6, 0, 0), (22, -10, 0, 0), (24, 10, 20, 0), (26, -10, -20, 0), (32, 0, 0, 0), (40, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (8, 24, 0, 0), (10, -20, 0, 0), (13, -10, 0, 0), (18, 20, 0, 10), (26, 0, -20, 0), (32, 10, 0, 0), (40, 0, 0, 0))
legs(a, [(0, 0, 0, 2), (8, 0, 0, 2), (10, 50, 0, 8), (13, 56, 0, 8), (17, 70, 0, 6), (20, 60, 0, 6), (22, 20, 0, 4), (26, -20, 0, 2), (32, 0, 0, 2), (40, 0, 0, 2)],
     [(0, 4, 0, -4), (10, -10, 0, -8), (13, -6, 0, -8), (17, 60, 0, -6), (20, 50, 0, -6), (22, 20, 0, -4), (26, 30, 0, -4), (32, 4, 0, -4), (40, 4, 0, -4)],
     shin_r=[(0, 0, 0, 0), (10, -90, 0, 0), (13, -96, 0, 0), (17, -110, 0, 0), (22, -30, 0, 0), (26, -10, 0, 0), (40, 0, 0, 0)],
     shin_l=[(0, -8, 0, 0), (10, -40, 0, 0), (17, -110, 0, 0), (22, -30, 0, 0), (26, -30, 0, 0), (40, -8, 0, 0)])
hair_all(a, [(0, -3, 0, 0), (8, -10, 0, 0), (10, 30, 0, 0), (13, 10, 0, 0), (17, -50, 40, 0), (22, -30, 30, 0), (26, -10, 0, 0), (40, -3, 0, 0)],
         [(0, 0, 0, 3), (10, 20, 0, 20), (17, -20, 0, 50), (24, 0, 0, 10), (40, 0, 0, 3)])
skirt(a, [(0, 0, 0, 0), (10, 30, 0, 0), (17, 20, 0, 0), (19, -20, 0, 0), (24, 10, 0, 0), (40, 0, 0, 0)], sides=[(0, 0, 0, 0), (17, 0, 0, 40), (24, 0, 0, 8), (40, 0, 0, 0)])
a.rot("antenna", (0, 0, 0, 0), (10, 30, 0, 0), (17, -20, 0, 20), (24, 10, 0, 0), (32, 0, 0, 0))
a.done()

# ------------------------------------------------------------------ sticky_bomb (50): pull charge 0..8, sidearm throw 12, beep countdown, detonator CLICK 42..44, glee
a = A("sticky_bomb", 50)
a.show("c4", 4, 12, 1.0, grow=1.0)
a.show("det", 17, 47, 1.0)
a.scl("spark", HIDE, *[(t, 1.0 if t in (20, 28, 34, 38, 41, 43) else .001, 1.0 if t in (20, 28, 34, 38, 41, 43) else .001, 1.0 if t in (20, 28, 34, 38, 41, 43) else .001)
                       for t in range(19, 45)], (45, .001, .001, .001))
a.rot("arm_r", (0, -4, 0, 18), (3, 10, 0, 6), (5, 0, 0, 10), (9, 30, 70, 60), (11, 60, 40, 70), (12, 90, -30, 30), (14, 80, -60, 10), (17, 20, 0, 20),
      (22, 60, 0, 20), (40, 70, 0, 20), (42, 140, 0, 10), (43, 150, 0, 10), (44, 156, 0, 6), (47, 120, 0, 20), (50, -4, 0, 18))
a.rot("fore_r", (0, 70, 30, 0), (3, 80, 0, 0), (9, 50, 0, 0), (12, 0, 0, 0), (17, 60, 0, 0), (22, 70, 0, 0), (40, 70, 0, 0), (43, 10, 0, 0), (50, 70, 30, 0))
a.rot("hand_r", (0, 0, 0, 0), (43.5, 0, 0, 0), (44, -24, 0, 0), (45, 0, 0, 0), (50, 0, 0, 0))
# left hand: finger-wag "tick tock" on each beep
al = [(0, 14, 0, -6), (12, -20, 0, -30), (17, 60, 0, -20)]
for t in (20, 28, 34, 38, 41):
    al += [(t - 1, 100, 0, -14), (t, 100, -20, -6)]
al += [(44, 40, 0, -60), (47, 30, 0, -40), (50, 14, 0, -6)]
a.rot("arm_l", *al)
a.rot("fore_l", (0, 40, 0, 0), (17, 60, 0, 0), (20, 70, 0, 0), (41, 70, 0, 0), (44, 20, 0, 0), (50, 40, 0, 0))
a.rot("chest", (0, 0, 0, 0), (5, -6, -16, 0), (9, 6, -40, 0), (12, -10, 30, 0), (15, -6, 20, 0), (20, 4, 0, 0), (40, 4, 0, 0), (44, 14, -10, 0), (47, 20, 0, 0), (50, 0, 0, 0))
a.rot("body", (0, 0, 0, 0), (9, 0, -10, 0), (12, -10, 16, 0), (17, 0, 0, 0), (44, 6, 0, 0), (50, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (5, -14, -30, 0), (9, 0, 10, 0), (12, -4, 0, 0), (20, 4, 0, 12), (28, 4, 0, -12), (34, 4, 0, 12), (38, 4, 0, -12), (41, 4, 0, 12),
      (44, 26, 0, 0), (47, 30, 0, -8), (50, 0, 0, 0))
legs(a, [(0, 0, 0, 2), (9, -20, 0, 2), (12, 24, 0, 2), (17, 10, 0, 2), (44, 10, 0, 2), (46, -10, 0, 4), (50, 0, 0, 2)],
     [(0, 4, 0, -4), (9, 26, 0, -4), (12, -20, 0, -4), (17, -6, 0, -4), (44, -6, 0, -4), (46, 30, 0, -4), (50, 4, 0, -4)],
     shin_r=[(0, 0, 0, 0), (9, -10, 0, 0), (12, -10, 0, 0), (50, 0, 0, 0)], shin_l=[(0, -8, 0, 0), (9, -30, 0, 0), (12, -6, 0, 0), (44, -6, 0, 0), (46, -60, 0, 0), (50, -8, 0, 0)])
a.pos("root", (0, 0, 0, 0), (44, 0, 0, 0), (46, 0, 1.6, 0), (48, 0, 0, 0), (50, 0, 0, 0))
hair_all(a, [(0, -3, 0, 0), (9, 0, 20, 0), (12, -20, -20, 0), (17, -8, 0, 0), (44, -6, 0, 0), (46, 20, 0, 0), (50, -3, 0, 0)],
         [(0, 0, 0, 3), (12, -10, 0, 16), (20, 0, 0, 4), (46, 10, 0, 16), (50, 0, 0, 3)])
skirt(a, [(0, 0, 0, 0), (9, -6, 0, 0), (12, 14, 0, 0), (18, 4, 0, 0), (44, 2, 0, 0), (46, -16, 0, 0), (50, 0, 0, 0)], sides=[(0, 0, 0, 0), (12, 0, 0, 10), (46, 0, 0, 14), (50, 0, 0, 0)])
a.rot("antenna", (0, 0, 0, 0), *[(t, -8, 0, 0) for t in (20, 28, 34, 38, 41)], *[(t + 1, 4, 0, 0) for t in (20, 28, 34, 38, 41)], (44, -20, 0, 0), (47, 10, 0, 0), (50, 0, 0, 0))
a.done()

# ------------------------------------------------------------------ death (40): pin drops out, she freezes, "oops" - little blast, knocked flat on her back
a = A("death", 40)
a.scl("blast", HIDE, (13.5, .001, .001, .001), (14.5, 0.5, 0.5, 0.5), (16, 0.8, 0.8, 0.8), (18, .001, .001, .001))
a.rot("arm_l", (0, 14, 0, -6), (4, 60, 0, -6), (8, 80, 0, -10), (13, 84, 0, -10), (16, 150, 0, -60), (24, 170, 0, -80), (40, 170, 0, -80))
a.rot("fore_l", (0, 40, 0, 0), (8, 20, 0, 0), (16, 0, 0, 0), (40, 10, 0, 0))
a.rot("arm_r", (0, -4, 0, 18), (6, 30, 0, 20), (13, 40, 0, 20), (16, 150, 0, 60), (24, 170, 0, 80), (40, 170, 0, 80))
a.rot("fore_r", (0, 70, 30, 0), (13, 20, 0, 0), (40, 20, 0, 0))
a.rot("head", (0, 0, 0, 0), (6, -20, 0, 0), (10, -24, 0, 10), (13, -24, 0, 10), (16, 30, 0, 0), (24, 20, 0, 20), (40, 10, 30, 20))
a.rot("chest", (0, 0, 0, 0), (8, -10, 0, 0), (13, -10, 0, 0), (16, 20, 0, 0), (40, 10, 0, 0))
a.rot("grenade", (0, 0, 0, 0), (13, 0, 0, 0), (14, 0, 0, 0))
nade_hide(a, 14, 41)
a.pos("root", (0, 0, 0, 0), (13, 0, 0, 0), (16, 0, 3.6, 1.0), (22, 0, 3.6, 1.2), (26, 0, 2.4, 1.0), (29, 0, 3.2, 1.0), (32, 0, 2.4, 1.0), (40, 0, 2.4, 1.0))
a.rot("root", (0, 0, 0, 0), (13, 0, 0, 0), (16, 30, 0, 0), (22, 70, 0, 0), (26, 90, 0, 4), (29, 82, 0, 4), (32, 90, 0, 4), (40, 90, 0, 4))
legs(a, [(0, 0, 0, 2), (13, 0, 0, 2), (16, 50, 0, 10), (22, 70, 0, 16), (26, 30, 0, 14), (40, 26, 0, 14)],
     [(0, 4, 0, -4), (13, 4, 0, -4), (16, 30, 0, -10), (22, 50, 0, -16), (26, 10, 0, -14), (40, 10, 0, -14)],
     shin_r=[(0, 0, 0, 0), (16, -50, 0, 0), (26, -20, 0, 0), (40, -26, 0, 0)], shin_l=[(0, -8, 0, 0), (16, -30, 0, 0), (26, -6, 0, 0), (40, -10, 0, 0)])
hair_all(a, [(0, -3, 0, 0), (13, -6, 0, 0), (16, 60, 0, 0), (22, 30, 0, 0), (26, -40, 0, 0), (30, -60, 0, 0), (40, -60, 0, 0)],
         [(0, 0, 0, 3), (16, 20, 0, 40), (26, -10, 0, 30), (40, -20, 0, 40)])
skirt(a, [(0, 0, 0, 0), (13, 0, 0, 0), (16, 40, 0, 0), (26, 10, 0, 0), (30, 20, 0, 0), (40, 16, 0, 0)])
a.rot("antenna", (0, 0, 0, 0), (13, 0, 0, 0), (16, 50, 0, 20), (26, -40, 0, -20), (32, -60, 0, 30), (40, -70, 0, 30))
a.rot("spiral", (0, 0, 0, 0), (26, 0, 0, 0), (32, 0, 0, -40), (40, 0, 0, -50))
a.done()

os.makedirs(os.path.dirname(OUT), exist_ok=True)
m.save(OUT)
print("cubes", len(m.cubes), "anims", [x["name"] for x in m.anims], "atlas rows used", m.cy + m.rowh)
