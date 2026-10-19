"""Lord Hansel - Juvenile form (FPE Advanced Class, faction OUTSIDER) - generates assets/fpe/bbmodels/hansel_juvenile.bbmodel.
Reference: docs/ref/confirmed/hansel_juvenile.png. Slender forest boy (hitbox 0.7 x 2.0): long spiky pale-blond hair swept over his
RIGHT eye, dark-brown branching antlers wearing a flower crown (white + pink flowers), a fanged lopsided grin, green leafy top with a
red tie, a long green leaf cloak dotted with white flowers that flares to the ground, a ragged dark-grey sash, torn dark-brown leg
wraps, bare feet, grey-bandaged tan arms with clawed hands.
Blockbench space: Y up, ground 0, faces -Z. Character's RIGHT = +X.
Rotation signs: arm/leg rx>0 = swing forward, torso/head rx>0 = lean back / look up, ry>0 = turn to the character's left,
rz>0 = toward +X. Position z<0 = forward, y>0 = up.
Every key tick matches entity/characters/HanselJuvenile.java.
Run: python3 tools/bbgen/chars/hansel_juvenile.py
"""
import math, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from bbgen import Model, mix  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "../../../src/main/resources/assets/fpe/bbmodels/hansel_juvenile.bbmodel")

# ------------------------------------------------------------------ palette (from the confirmed art)
SKIN, SKIN_D, SKIN_L = 0xE4B88C, 0xC08E66, 0xF2D2AC
HAIR, HAIR_D, HAIR_L, HAIR_DD = 0xEDE5BF, 0xCBBE8E, 0xFBF8E6, 0xA8996A
G, G_D, G_L, G_DD, G_LL = 0x3F7C33, 0x26521F, 0x6CA94A, 0x15331A, 0x9BCB6A
WRAP, WRAP_D, WRAP_L = 0x5C3A28, 0x3C2418, 0x7D5640
BAND, BAND_D, BAND_L = 0x6E6E74, 0x46464C, 0x96969C
ANT, ANT_D, ANT_L = 0x4C3121, 0x2E1C12, 0x6E4A32
SASH, SASH_D = 0x4A4A50, 0x2C2C32
RED, RED_D = 0x9A2C24, 0x5E1612
FLW, FLW_D, FLW_Y, PINK, PINK_D = 0xFBFAF0, 0xD8D6C4, 0xF2C94A, 0xE88EA2, 0xC0607A
LINE = 0x2A1A14
MOUTH = 0x5A1A1E
CLEAR = (0, 0, 0, 0)

m = Model("hansel_juvenile", S=8, atlas=2048)
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


def clear(F):
    F.rect(0, 0, F.w, F.h, CLEAR)


def flat(c):
    return lambda F: F.rect(0, 0, F.w, F.h, c)


def skinp(F):
    for y in range(F.h):
        for x in range(F.w):
            F.px(x, y, mix(SKIN_L, SKIN_D, 0.15 + 0.5 * y / max(1, F.h)))


def hairp(base=HAIR, ink=True):
    def f(F):
        for y in range(F.h):
            for x in range(F.w):
                F.px(x, y, mix(HAIR_L, base, min(1, 0.4 + 0.7 * y / max(1, F.h))))
        for x in range(0, F.w, 3):
            xx = x + R.randint(0, 1)
            for y in range(R.randint(0, 4), F.h):
                F.px(xx, y, mix(base, HAIR_D, 0.6))
        hb = int(F.h * 0.2)
        for x in range(F.w):
            if (x // 2) % 3: F.px(x, hb + (x % 2), HAIR_L)
        if ink: outline(HAIR_DD)(F)
    return f


def pointed(fn, tip=6):
    """paint, then cut a pointed tip at the bottom of the face"""
    def f(F):
        fn(F)
        n = min(tip, F.h)
        for yy in range(F.h - n, F.h):
            for xx in range(F.w):
                if abs(xx + .5 - F.w / 2) > (F.h - yy) * F.w / (2 * n):
                    F.px(xx, yy, CLEAR)
    return f


def leafy(base=G, dark=G_D, light=G_L, ink=True, flowers=0, jag=0):
    """leaf cloak: gradient, overlapping leaf shapes, vein lines, optional white flowers and a jagged leaf hem"""
    def f(F):
        for y in range(F.h):
            for x in range(F.w):
                F.px(x, y, mix(base, dark, 0.15 + 0.45 * y / max(1, F.h)))
        for _ in range(max(2, F.w * F.h // 50)):
            cx, cy = R.uniform(0, F.w), R.uniform(0, F.h)
            r = R.uniform(1.6, 3.4)
            c = R.choice((light, dark, G_LL if R.random() < 0.2 else light, mix(base, light, 0.5)))
            ang = R.uniform(0, math.pi)
            for j in range(int(cy - r * 2) - 1, int(cy + r * 2) + 2):
                for i in range(int(cx - r * 2) - 1, int(cx + r * 2) + 2):
                    dx, dy = i + .5 - cx, j + .5 - cy
                    u = dx * math.cos(ang) + dy * math.sin(ang)
                    v = -dx * math.sin(ang) + dy * math.cos(ang)
                    if (u / (r * 1.6)) ** 2 + (v / (r * 0.7)) ** 2 <= 1:
                        F.px(i, j, c)
            F.line(cx - math.cos(ang) * r, cy - math.sin(ang) * r, cx + math.cos(ang) * r, cy + math.sin(ang) * r, mix(c, G_DD, 0.35), 1)
        for _ in range(flowers):
            flower_paint(F, R.uniform(3, F.w - 3), R.uniform(3, F.h - 4), R.uniform(2.0, 2.8), FLW)
        if jag:
            for x in range(F.w):
                zz = int(abs((x % (2 * jag)) - jag) * 1.2)
                for y in range(F.h - zz, F.h):
                    F.px(x, y, CLEAR)
                F.px(x, F.h - zz - 1, G_DD)
        if ink:
            F.rect(0, 0, 1, F.h - (jag * 1 if jag else 0), G_DD); F.rect(F.w - 1, 0, 1, F.h - (jag if jag else 0), G_DD)
    return f


def flower_paint(F, cx, cy, r, col=FLW):
    dcol = FLW_D if col == FLW else PINK_D
    for k in range(5):
        a = k * 2 * math.pi / 5 - math.pi / 2
        F.disc(cx + math.cos(a) * r * 0.62, cy + math.sin(a) * r * 0.62, r * 0.5, col)
    for k in range(5):
        a = k * 2 * math.pi / 5 - math.pi / 2 + 0.6
        F.px(int(cx + math.cos(a) * r * 0.75), int(cy + math.sin(a) * r * 0.75), dcol)
    F.disc(cx, cy, max(0.8, r * 0.28), FLW_Y)


def flowerface(col=FLW):
    def f(F):
        F.rect(0, 0, F.w, F.h, CLEAR)
        flower_paint(F, F.w / 2, F.h / 2, min(F.w, F.h) / 2, col)
    return f


def leafface(col=G, dark=G_D):
    """pointed leaf filling the face, long axis along the longer side"""
    def f(F):
        vert = F.h >= F.w
        L, W = (F.h, F.w) if vert else (F.w, F.h)
        for y in range(F.h):
            for x in range(F.w):
                u, v = ((y + .5) / F.h, (x + .5) / F.w) if vert else ((x + .5) / F.w, (y + .5) / F.h)
                half = 0.5 * math.sin(math.pi * u) ** 0.8
                d = abs(v - 0.5)
                if d > half: F.px(x, y, CLEAR)
                elif d < 0.6 / W + 0.02: F.px(x, y, mix(col, G_LL, 0.4))
                elif d > half - 1.2 / W: F.px(x, y, dark)
                else: F.px(x, y, mix(col, dark, 0.35 * u))
    return f


def wrapp(base=WRAP, dark=WRAP_D, light=WRAP_L, torn=True):
    """wrapped bandage cloth: diagonal bands, dark gaps, frayed holes showing skin"""
    def f(F):
        for y in range(F.h):
            for x in range(F.w):
                band = ((y + x * 0.45) % 6)
                c = light if band < 1.2 else (dark if band > 5.0 else base)
                F.px(x, y, mix(c, dark, 0.25 * y / max(1, F.h)))
        if torn:
            for _ in range(max(1, F.w * F.h // 160)):
                cx, cy = R.randint(1, max(1, F.w - 2)), R.randint(1, max(1, F.h - 3))
                F.disc(cx, cy, R.uniform(0.8, 1.6), SKIN_D)
                F.px(cx, cy - 1, dark)
    return f


def bandp(F):
    for y in range(F.h):
        for x in range(F.w):
            band = ((y - x * 0.5) % 5)
            F.px(x, y, BAND_L if band < 1 else (BAND_D if band > 4 else BAND))


def sashp(F):
    for y in range(F.h):
        for x in range(F.w):
            F.px(x, y, mix(SASH, SASH_D, 0.3 + 0.3 * math.sin(x * 0.7 + y * 0.2) ** 2))
    for x in range(F.w):
        zz = int(abs((x % 6) - 3) * 1.3)
        for y in range(F.h - zz, F.h):
            F.px(x, y, CLEAR)


def antp(F):
    for y in range(F.h):
        for x in range(F.w):
            F.px(x, y, mix(ANT_L, ANT, 0.3 + 0.5 * x / max(1, F.w)))
    for _ in range(max(1, F.h // 3)):
        y = R.randint(0, F.h - 1)
        F.rect(0, y, F.w, 1, ANT_D)


def spikep(tip_left, col, dark):
    def f(F):
        for y in range(F.h):
            for x in range(F.w):
                u = (x + .5) / F.w
                u = 1 - u if not tip_left else u
                half = 0.5 * u
                v = abs((y + .5) / F.h - 0.5)
                if v > half: F.px(x, y, CLEAR)
                elif v > half - 1.2 / F.h: F.px(x, y, dark)
                else: F.px(x, y, mix(col, dark, 0.3 * (1 - u) + 0.2 * (y / F.h)))
    return f


def thornp(F):
    for y in range(F.h):
        for x in range(F.w):
            v = (y + .5) / F.h
            half = 0.5 * v
            if abs((x + .5) / F.w - 0.5) > half: F.px(x, y, CLEAR)
            else: F.px(x, y, mix(ANT_L, ANT_D, v))


# ------------------------------------------------------------------ face
def face_front(F):
    W, H = F.w, F.h
    skinp(F)
    # hairline / fringe across the top
    for x in range(W):
        top = 9 + int(3 * abs(math.sin(x * 0.45)))
        for y in range(top):
            F.px(x, y, mix(HAIR_L, HAIR, y / 12))
        F.px(x, top, HAIR_DD)
    # long swoop of hair over the RIGHT eye (texel left), strand lines, pointed tips
    sw = [(0, 6), (36, 6), (30, 18), (24, 30), (18, 40), (10, 46), (0, 50)]
    F.poly(sw, HAIR)
    for i in range(7):
        x0 = 4 + i * 5
        F.line(x0, 6, x0 - 10 + i, 36 + i * 1.5, HAIR_D, 1)
    for i in range(5):
        x0 = 6 + i * 6
        F.line(x0, 10, x0 - 8, 30, HAIR_L, 1)
    F.line(36, 6, 30, 18, HAIR_DD, 1); F.line(30, 18, 18, 40, HAIR_DD, 1); F.line(18, 40, 10, 46, HAIR_DD, 1)
    # shadow of the hair on the skin
    F.line(31, 20, 20, 41, SKIN_D, 2)
    # visible LEFT eye (texel right): heavy dark lid, sleepy smug almond, amber iris
    ex, ey = 40, 25
    for y in range(-4, 5):
        for x in range(-8, 9):
            if (x / 7.5) ** 2 + (y / 3.4) ** 2 <= 1 and y > -2:
                F.px(ex + x, ey + y, 0xF6F0E2)
    F.disc(ex - 1, ey + 1, 2.8, 0x6A4A1E)
    F.disc(ex - 1, ey + 1, 1.4, LINE)
    F.px(ex - 2, ey, 0xFFF2B0, glow=True)
    for x in range(-9, 10):
        yy = ey - 2 - int(2.2 * math.cos(x / 9 * math.pi / 2))
        F.rect(ex + x, yy, 1, 2, LINE)
    F.line(ex + 8, ey - 3, ex + 12, ey - 6, LINE, 1)          # lash flick
    F.line(ex + 7, ey - 1, ex + 11, ey - 2, LINE, 1)
    F.line(ex - 6, ey + 4, ex + 6, ey + 4, SKIN_D, 1)         # lower lid crease
    F.line(ex - 6, ey - 9, ex + 7, ey - 10, HAIR_D, 2)        # pale brow
    F.disc(ex + 4, ey + 9, 3, mix(SKIN, PINK, 0.35))          # blush
    F.line(33, 31, 34, 34, SKIN_D, 1)                          # nose
    # lopsided fanged grin (wider toward his left)
    top = lambda x: 39 - 0.12 * (x - 22) - 2.5 * math.exp(-((x - 50) / 3) ** 2)
    bot = lambda x: 40 + 6.5 * math.sin(math.pi * min(1, max(0, (x - 22) / 29)))
    for x in range(22, 52):
        for y in range(int(top(x)), int(bot(x)) + 1):
            F.px(x, y, MOUTH)
        F.px(x, int(top(x)), 0xF8F4EA)
        F.px(x, int(top(x)) + 1, 0xF8F4EA if x % 4 else MOUTH)
        F.px(x, int(top(x)) - 1, LINE)
        F.px(x, int(bot(x)) + 1, LINE)
    for x in range(30, 44):
        F.px(x, int(bot(x)) - 1, 0xB04A4E)                      # tongue
    F.poly([(40, top(40)), (44, top(44)), (42, top(42) + 6)], 0xFFFFFF)   # big fang
    F.poly([(28, top(28)), (31, top(31)), (29.5, top(29.5) + 4)], 0xFFFFFF)
    F.line(50, 37, 53, 35, LINE, 1)                             # smirk corner


# ------------------------------------------------------------------ shape helpers
def tip(start, L, rx, rz):
    a, c = math.radians(rx), math.radians(rz)
    y = L * math.cos(a)
    return (start[0] - y * math.sin(c), start[1] + y * math.cos(c), start[2] + L * math.sin(a))


def seg(name, parent, start, L, t, rx, rz, col=ANT, painter=None):
    x, y, z = start
    p = painter or antp
    m.cube(name, parent, (x - t / 2, y, z - t / 2), (x + t / 2, y + L, z + t / 2), col, origin=start, rot=(rx, 0, rz),
           faces={"north": p, "south": p, "east": p, "west": p, "up": flat(ANT_L), "down": flat(ANT_D)})
    return tip(start, L, rx, rz)


def spike(name, parent, base, length, h, d, yaw, roll, col, dark, side=1):
    x, y, z = base
    x0, x1 = (x, x + length) if side > 0 else (x - length, x)
    m.cube(name, parent, (x0, y - h / 2, z - d / 2), (x1, y + h / 2, z + d / 2), col, origin=base, rot=(0, yaw, roll),
           faces={"north": spikep(side > 0, col, dark), "south": spikep(side < 0, col, dark), "up": clear, "down": clear, "east": clear, "west": clear})


def leaf(name, parent, c, w, h, rot=(0, 0, 0), col=G, dark=G_D, d=0.15):
    x, y, z = c
    lf = leafface(col, dark)
    m.cube(name, parent, (x - w / 2, y - h, z - d / 2), (x + w / 2, y, z + d / 2), col, origin=(x, y, z), rot=rot,
           faces={"north": lf, "south": lf, "east": clear, "west": clear, "up": clear, "down": clear})


def flower(name, parent, c, s, ry=0, col=FLW, rx=0):
    x, y, z = c
    fp = flowerface(col)
    m.cube(name, parent, (x - s / 2, y - s / 2, z - 0.2), (x + s / 2, y + s / 2, z + 0.2), col, origin=c, rot=(rx, ry, 0),
           faces={"north": fp, "south": fp, "up": clear, "down": clear, "east": clear, "west": clear})
    m.cube(name + "_c", parent, (x - s * 0.15, y - s * 0.15, z - 0.32), (x + s * 0.15, y + s * 0.15, z + 0.32), FLW_Y, origin=c, rot=(rx, ry, 0))


# ------------------------------------------------------------------ skeleton
m.group("root", (0, 0, 0))
m.group("body", (0, 12, 0), parent="root")
m.group("chest", (0, 14, 0), parent="body")
m.group("head", (0, 20.6, 0), parent="chest")
m.group("bangs", (1.5, 27.4, -3.4), parent="head")
m.group("hair_b", (0, 27.0, 3.3), parent="head")
m.group("lock_r", (3.7, 27.0, 0), parent="head")
m.group("lock_l", (-3.7, 27.0, 0), parent="head")
m.group("tufts", (0, 28.2, 0), parent="head")
m.group("antler_r", (2.0, 27.8, 0.4), parent="head")
m.group("antler_l", (-2.0, 27.8, 0.4), parent="head")
m.group("crown", (0, 27.2, 0), parent="head")
m.group("cape", (0, 20.4, 1.0), parent="chest")
m.group("cape_b", (0, 20.4, 2.2), parent="cape")
m.group("cape_r", (3.0, 20.4, 0.8), parent="cape")
m.group("cape_l", (-3.0, 20.4, 0.8), parent="cape")
m.group("arm_r", (3.5, 19.8, 0), parent="chest")
m.group("fore_r", (3.6, 15.2, 0), parent="arm_r")
m.group("hand_r", (3.6, 11.0, 0), parent="fore_r")
m.group("vine", (3.6, 10.0, 0), parent="hand_r")
m.group("arm_l", (-3.5, 19.8, 0), parent="chest")
m.group("fore_l", (-3.6, 15.2, 0), parent="arm_l")
m.group("hand_l", (-3.6, 11.0, 0), parent="fore_l")
m.group("sash", (0, 12.6, 0), parent="body")
for s, k in ((1, "r"), (-1, "l")):
    m.group("leg_" + k, (1.25 * s, 12, 0), parent="body")
    m.group("shin_" + k, (1.25 * s, 6.6, 0), parent="leg_" + k)

# ------------------------------------------------------------------ legs: torn dark-brown wraps, bare tan feet
for s, k in ((1, "r"), (-1, "l")):
    x = 1.25 * s
    m.cube("thigh_" + k, "leg_" + k, (x - 0.95, 6.4, -0.95), (x + 0.95, 12.2, 0.95), WRAP, faces=all_faces(wrapp()))
    m.cube("calf_" + k, "shin_" + k, (x - 0.85, 1.0, -0.85), (x + 0.85, 6.8, 0.85), WRAP, faces=all_faces(wrapp()))
    m.cube("knee_" + k, "shin_" + k, (x - 1.0, 6.0, -1.05), (x + 1.0, 7.0, 0.7), WRAP_L, origin=(x, 6.5, 0), rot=(0, 0, 6 * s), faces=all_faces(wrapp(WRAP_L, WRAP, WRAP_L, False)))
    m.cube("ankle_" + k, "shin_" + k, (x - 0.95, 1.0, -0.95), (x + 0.95, 1.9, 0.95), WRAP_D, origin=(x, 1.5, 0), rot=(0, 0, -5 * s), faces=all_faces(wrapp(WRAP_D, LINE, WRAP, False)))
    for j, (y, rz) in enumerate(((10.4, 9), (8.2, -8))):
        m.cube(f"lband{j}_{k}", "leg_" + k, (x - 1.05, y - 0.45, -1.05), (x + 1.05, y + 0.45, 1.05), WRAP_L, origin=(x, y, 0), rot=(0, 0, rz * s), faces=all_faces(wrapp(WRAP_L, WRAP_D, WRAP_L, False)))
    m.cube(f"lband2_{k}", "shin_" + k, (x - 0.95, 3.6, -0.95), (x + 0.95, 4.4, 0.95), WRAP_L, origin=(x, 4.0, 0), rot=(0, 0, 10 * s), faces=all_faces(wrapp(WRAP_L, WRAP_D, WRAP_L, False)))
    # dangling torn strips
    m.cube(f"strip0_{k}", "leg_" + k, (x + 0.7 * s - 0.2, 6.6, -0.6), (x + 0.7 * s + 0.2, 8.8, -0.4), WRAP_D, origin=(x + 0.7 * s, 8.8, -0.5), rot=(0, 0, 12 * s), faces=all_faces(pointed(wrapp(WRAP_D, LINE, WRAP, False), 3)))
    m.cube(f"strip1_{k}", "shin_" + k, (x - 0.2, 2.2, -1.0), (x + 0.2, 4.0, -0.85), WRAP_D, origin=(x, 4.0, -0.9), rot=(-8, 0, -10 * s), faces=all_faces(pointed(wrapp(WRAP_D, LINE, WRAP, False), 3)))
    # bare foot + toes
    m.cube("foot_" + k, "shin_" + k, (x - 0.95, 0.0, -2.1), (x + 0.95, 1.1, 0.9), SKIN, faces=all_faces(skinp) | {"down": flat(SKIN_D)})
    m.cube("heel_" + k, "shin_" + k, (x - 0.85, 0.0, 0.6), (x + 0.85, 1.3, 1.1), SKIN_D, faces=all_faces(skinp))
    for t in range(4):
        tx = x - 0.75 + t * 0.48 + (0.05 if s > 0 else 0)
        m.cube(f"toe{t}_{k}", "shin_" + k, (tx - 0.2, 0.0, -2.5), (tx + 0.2, 0.55 + (0.12 if t == (0 if s < 0 else 3) else 0), -2.05), SKIN, faces=all_faces(lambda F: (skinp(F), F.rect(0, 0, F.w, 1, SKIN_D))))

# ------------------------------------------------------------------ hips: ragged dark-grey sash with tatters + leaf skirt bits
m.cube("sash_c", "sash", (-2.9, 11.3, -1.75), (2.9, 14.2, 1.75), SASH, faces=all_faces(sashp, ("up", "down")) | {"up": flat(SASH_D), "down": clear})
m.cube("sash_knot", "sash", (-2.4, 12.4, -2.05), (-0.9, 13.8, -1.7), SASH_D, origin=(-1.6, 13.1, -1.9), rot=(0, 0, 20), faces=all_faces(outline(LINE)))
for i, (x, z, ry, rz, L) in enumerate(((-2.6, -1.8, 0, -16, 3.6), (-1.0, -1.85, 0, 8, 2.6), (1.6, -1.85, 0, -6, 3.2), (2.8, -0.6, 90, 14, 3.0),
                                       (-2.9, 0.6, 90, -10, 3.4), (0.6, 1.8, 0, 6, 2.8), (-1.8, 1.8, 0, -8, 3.0), (2.2, 1.8, 0, 12, 2.4))):
    m.cube(f"tatter{i}", "sash", (x - 0.55, 11.4 - L, z - 0.1), (x + 0.55, 11.6, z + 0.1), SASH_D, origin=(x, 11.6, z), rot=(0, ry, rz),
           faces={"north": pointed(sashp, 4), "south": pointed(sashp, 4), "east": clear, "west": clear, "up": clear, "down": clear})
for i, (x, z, rz) in enumerate(((-2.2, -1.95, -20), (2.4, -1.9, 24), (0.2, -1.95, 4))):
    leaf(f"hipleaf{i}", "sash", (x, 12.4, z), 1.2, 2.6, rot=(-10, 0, rz), col=G_D, dark=G_DD)

# ------------------------------------------------------------------ torso: green leaf top, red tie, leafy collar
def torso_front(F):
    leafy(G, G_D, G_L, ink=False)(F)
    F.rect(F.w // 2 - 3, 0, 6, 6, G_DD)                       # neckline
    F.rect(F.w // 2 - 2, 0, 4, 4, SKIN_D)
    F.poly([(F.w / 2 - 3, 5), (F.w / 2 + 3, 5), (F.w / 2 + 1.5, 9), (F.w / 2 - 1.5, 9)], RED)   # tie knot
    F.poly([(F.w / 2 - 1.5, 9), (F.w / 2 + 1.5, 9), (F.w / 2 + 3, 26), (F.w / 2, 30), (F.w / 2 - 3, 26)], RED)
    F.line(F.w / 2, 9, F.w / 2, 28, RED_D, 1)
    F.rect(0, F.h - 3, F.w, 3, G_DD)                          # hem


m.cube("torso", "chest", (-2.5, 13.8, -1.45), (2.5, 20.6, 1.45), G, faces={"north": torso_front, "south": leafy(), "east": leafy(), "west": leafy(), "up": leafy(), "down": flat(G_DD)})
m.cube("waist", "chest", (-2.3, 13.0, -1.3), (2.3, 14.2, 1.3), G_D, faces=all_faces(leafy(G_D, G_DD, G)))
for i in range(10):
    a = math.radians(i * 36 + 18)
    x, z = math.sin(a) * 2.6, -math.cos(a) * 1.8
    leaf(f"collar{i}", "chest", (x, 21.3, z), 1.3, 2.2, rot=(-25 * math.cos(a), -math.degrees(a), 0), col=G_L if i % 2 else G)
for s, k in ((1, "r"), (-1, "l")):     # leafy shoulder mantles
    m.cube("mantle_" + k, "chest", (2.0 * s - 1.6, 19.4, -1.7), (2.0 * s + 1.6, 21.0, 1.9), G, origin=(2.0 * s, 20.2, 0), rot=(0, 0, -14 * s),
           faces=all_faces(leafy(G, G_D, G_L)))
    for j in range(3):
        leaf(f"mleaf{j}_{k}", "chest", ((3.0 + j * 0.2) * s, 19.8, -1.2 + j * 1.2), 1.4, 2.6, rot=(0, 0, (30 + j * 10) * s), col=(G, G_L, G_D)[j])

# ------------------------------------------------------------------ cloak: back panel + flaring sides + front flaps, leaf hem, white flowers
m.cube("capeb_main", "cape_b", (-4.4, 0.6, 1.8), (4.4, 20.6, 2.5), G, origin=(0, 20.4, 2.2), rot=(-5, 0, 0),
       faces={"south": leafy(G, G_D, G_L, flowers=4, jag=3), "north": leafy(G_D, G_DD, G, jag=3), "east": leafy(), "west": leafy(), "up": leafy(), "down": clear})
for s, k in ((1, "r"), (-1, "l")):
    g = "cape_" + k
    m.cube("capes_" + k, g, (3.0 * s - 0.3, 0.8, -0.6), (3.0 * s + 0.3, 20.4, 2.4), G, origin=(3.0 * s, 20.4, 0.8), rot=(0, 0, 11 * s),
           faces={"east": leafy(G, G_D, G_L, flowers=3, jag=2), "west": leafy(G, G_D, G_L, flowers=3, jag=2), "north": leafy(), "south": leafy(), "up": leafy(), "down": clear})
    m.cube("capef_" + k, g, (2.3 * s - 0.7, 2.2, -1.85), (2.3 * s + 0.7, 19.8, -1.55), G, origin=(2.3 * s, 19.8, -1.7), rot=(0, 0, 9 * s),
           faces={"north": leafy(G, G_D, G_L, flowers=2, jag=2), "south": leafy(G_D, G_DD, G, jag=2), "east": leafy(), "west": leafy(), "up": leafy(), "down": clear})
    # outer flare wing (art: cloak spreads wide near the ground)
    m.cube("capew_" + k, g, (3.6 * s - 0.25, 0.4, 0.2), (3.6 * s + 0.25, 11.5, 2.8), G_D, origin=(3.6 * s, 11.5, 1.4), rot=(0, 0, 22 * s),
           faces={"east": leafy(G_D, G_DD, G, flowers=1, jag=2), "west": leafy(G_D, G_DD, G, flowers=1, jag=2), "north": leafy(), "south": leafy(), "up": leafy(), "down": clear})
    # hanging edge leaves
    for j in range(5):
        y = 3.0 + j * 3.6
        leaf(f"cleaf{j}_{k}", g, ((3.4 + 0.12 * (20 - y) / 3) * s, y, -0.4 + (j % 2) * 1.6), 1.3, 2.6, rot=(0, 90, (18 + j * 4) * s), col=(G_L, G, G_D)[j % 3])
    # flowers on the side panel + front flap
    for j, (y, z) in enumerate(((15.5, 0.6), (8.5, 1.6), (3.4, 0.2))):
        flower(f"cflw{j}_{k}", g, ((3.0 + 0.2 * (20 - y) / 3.5) * s + 0.35 * s, y, z), 1.5 - j * 0.1, ry=90 * s)
    flower(f"fflw_{k}", g, (2.3 * s + 0.12 * s, 10.5 + 3 * s, -1.95), 1.5)
# back hem leaves + flowers
for j in range(6):
    leaf(f"bleaf{j}", "cape_b", (-3.8 + j * 1.5, 1.6, 2.7), 1.4, 2.4, rot=(-14, 0, (j - 2.5) * 8), col=(G_L, G, G_D)[j % 3])
for j, (x, y) in enumerate(((-2.4, 14.0), (2.2, 9.0), (-1.0, 5.0), (1.2, 17.2))):
    flower(f"bflw{j}", "cape_b", (x, y, 2.75 + (20.4 - y) * 0.09), 1.6, ry=180)

# ------------------------------------------------------------------ arms: tan skin, grey bandage wraps, clawed hands
for s, k in ((1, "r"), (-1, "l")):
    x = 3.6 * s
    m.cube("upper_" + k, "arm_" + k, (x - 0.8, 15.0, -0.8), (x + 0.8, 20.0, 0.8), SKIN, faces=all_faces(skinp))
    m.cube("ubandA_" + k, "arm_" + k, (x - 0.9, 17.4, -0.9), (x + 0.9, 18.6, 0.9), BAND, origin=(x, 18, 0), rot=(0, 0, 12 * s), faces=all_faces(bandp))
    m.cube("ubandB_" + k, "arm_" + k, (x - 0.88, 15.4, -0.88), (x + 0.88, 16.6, 0.88), BAND, origin=(x, 16, 0), rot=(0, 0, -10 * s), faces=all_faces(bandp))
    m.cube("fore_c_" + k, "fore_" + k, (x - 0.72, 10.9, -0.72), (x + 0.72, 15.4, 0.72), BAND, faces=all_faces(bandp))
    m.cube("fband_" + k, "fore_" + k, (x - 0.82, 12.6, -0.82), (x + 0.82, 13.5, 0.82), BAND_D, origin=(x, 13, 0), rot=(0, 0, 14 * s), faces=all_faces(bandp))
    m.cube("fstrip_" + k, "fore_" + k, (x + 0.6 * s - 0.15, 10.4, 0.3), (x + 0.6 * s + 0.15, 12.6, 0.6), BAND_D, origin=(x + 0.6 * s, 12.6, 0.45), rot=(10, 0, 18 * s), faces=all_faces(pointed(bandp, 3)))
    m.cube("palm_" + k, "hand_" + k, (x - 0.75, 9.8, -0.7), (x + 0.75, 11.2, 0.7), SKIN, faces=all_faces(skinp))
    for f in range(3):
        fz = -0.5 + f * 0.5
        m.cube(f"claw{f}_{k}", "hand_" + k, (x - 0.15, 8.4, fz - 0.15), (x + 0.15, 9.9, fz + 0.15), SKIN, origin=(x, 9.9, fz), rot=(-14 + f * 4, 0, 6 * s),
               faces=all_faces(lambda F: (skinp(F), F.rect(0, F.h - 3, F.w, 3, LINE))))
    m.cube("thumb_" + k, "hand_" + k, (x - 0.8 * s - 0.15, 9.0, -0.6), (x - 0.8 * s + 0.15, 10.3, -0.3), SKIN, origin=(x - 0.6 * s, 10.3, -0.45), rot=(-20, 0, -20 * s),
           faces=all_faces(lambda F: (skinp(F), F.rect(0, F.h - 2, F.w, 2, LINE))))

# ------------------------------------------------------------------ vine prop (vine_lash / thorn_cage): long thorny vine grown out of the right hand
for i in range(6):
    y0 = 10.0 - i * 3.0
    m.cube(f"vine{i}", "vine", (3.6 - 0.32, y0 - 3.1, -0.32), (3.6 + 0.32, y0, 0.32), G_D, origin=(3.6, y0, 0), rot=(0, 0, (-1) ** i * 4),
           faces=all_faces(leafy(G_D, G_DD, G, ink=False)))
    spike(f"vthorn{i}", "vine", (3.6 + 0.3 * (-1) ** i, y0 - 1.5, 0), 0.9, 0.6, 0.2, 0, -30 * (-1) ** i, ANT_L, ANT_D, side=(-1) ** i)
    if i % 2 == 0:
        leaf(f"vleaf{i}", "vine", (3.6 - 0.35 * (-1) ** i, y0 - 0.6, 0.1), 0.9, 1.6, rot=(0, 30, 50 * (-1) ** i), col=G_L)
flower("vflw", "vine", (3.6, -8.4, 0), 1.4, ry=0)

# ------------------------------------------------------------------ head
m.cube("skull", "head", (-3.4, 20.6, -3.1), (3.4, 27.6, 3.1), SKIN,
       faces={"north": face_front, "south": hairp(), "east": hairp(), "west": hairp(), "up": hairp(), "down": skinp})
m.cube("neck", "head", (-0.8, 19.8, -0.8), (0.8, 21.0, 0.8), SKIN_D, faces=all_faces(skinp))
m.cube("hair_cap", "head", (-3.8, 24.6, -2.9), (3.8, 28.3, 3.7), HAIR, faces=all_faces(hairp()))
for s, k in ((1, "r"), (-1, "l")):   # ears poking from the hair (pointed, elfish)
    m.cube("ear_" + k, "head", (3.3 * s - 0.2, 23.4, -0.6), (3.3 * s + 0.2, 24.6, 0.4), SKIN, origin=(3.4 * s, 24.0, 0), rot=(0, 0, -30 * s), faces=all_faces(skinp))
# fringe strands in front of the RIGHT eye (3D), sweeping from the part toward his right
for i, (x, w, yb, rz, z) in enumerate(((0.2, 1.4, 23.6, -18, -3.45), (1.3, 1.4, 22.4, -14, -3.55), (2.3, 1.3, 21.6, -10, -3.5), (3.1, 1.0, 22.4, -4, -3.4), (-0.9, 1.2, 25.4, -26, -3.35))):
    m.cube(f"bang{i}", "bangs", (x, yb, z - 0.2), (x + w, 27.9, z + 0.2), HAIR, origin=(x + w / 2, 27.9, z), rot=(0, 0, rz),
           faces={"north": pointed(hairp(), 7), "south": pointed(hairp(), 7), "east": hairp(), "west": hairp(), "up": hairp(), "down": clear})
# long side locks reaching the hips, flaring and spiky
for s, k in ((1, "r"), (-1, "l")):
    g = "lock_" + k
    x = 3.7 * s
    for j, (z, yb, rz, w) in enumerate(((-2.3, 19.0, 4, 1.0), (1.1, 12.5, 10, 1.4), (2.0, 11.2, 13, 1.5), (2.9, 12.8, 9, 1.4))):
        m.cube(f"lock{j}_{k}", g, (x - w / 2, yb, z - 0.7), (x + w / 2, 27.6, z + 0.8), HAIR, origin=(x, 27.4, z), rot=(0, 0, rz * s),
               faces={"north": pointed(hairp(), 6), "south": pointed(hairp(), 6), "east": pointed(hairp(), 6), "west": pointed(hairp(), 6), "up": hairp(), "down": flat(HAIR_DD)})
    for j, (y, rz, L) in enumerate(((22.5, 26, 2.6), (19.0, 34, 2.8), (15.6, 40, 2.4), (25.0, 18, 2.0))):
        spike(f"lockspk{j}_{k}", g, (x + 0.4 * s, y, 1.2 + j * 0.5), L, 1.4, 0.6, 0, -rz * s, HAIR, HAIR_DD, side=s)
# back hair: panel + pointed strands to the waist
m.cube("back_panel", "hair_b", (-4.0, 12.6, 3.0), (4.0, 27.8, 4.1), HAIR, origin=(0, 27.6, 3.5), rot=(-6, 0, 0), faces=all_faces(hairp()))
for i, (x, yb, rz) in enumerate(((-3.4, 9.8, -10), (-1.7, 9.0, -4), (0.0, 8.4, 0), (1.7, 9.0, 4), (3.4, 10.0, 10))):
    m.cube(f"backstr{i}", "hair_b", (x - 0.95, yb, 3.7), (x + 0.95, 15.0, 4.6), HAIR, origin=(x, 15, 4.1), rot=(-10, 0, rz),
           faces={"south": pointed(hairp(), 7), "north": pointed(hairp(), 7), "east": hairp(), "west": hairp(), "up": clear, "down": clear})
# spiky tufts on top (art: messy points sticking up through the crown)
for i, (x, z, rz, rx, L) in enumerate(((-1.6, -1.6, 28, 0, 2.6), (1.4, -1.8, -30, 0, 2.4), (0.0, -0.4, 6, 10, 3.0), (-2.8, 0.8, 52, 0, 2.2), (2.8, 0.6, -50, 0, 2.2), (0.6, 1.8, -12, -24, 2.4))):
    s_ = 1 if rz < 0 else -1
    m.cube(f"tuft{i}", "tufts", (x - 0.7, 27.8, z - 0.45), (x + 0.7, 27.8 + L, z + 0.45), HAIR, origin=(x, 27.8, z), rot=(rx, 0, rz),
           faces={"north": combo(hairp(), lambda F: [F.px(xx, yy, CLEAR) for yy in range(F.h) for xx in range(F.w) if abs(xx + .5 - F.w / 2) > (yy + 1) * F.w / (2 * F.h)]),
                  "south": combo(hairp(), lambda F: [F.px(xx, yy, CLEAR) for yy in range(F.h) for xx in range(F.w) if abs(xx + .5 - F.w / 2) > (yy + 1) * F.w / (2 * F.h)]),
                  "east": clear, "west": clear, "up": clear, "down": clear})

# ------------------------------------------------------------------ antlers: dark brown, branching, curving up and out
for s, k in ((1, "r"), (-1, "l")):
    g = "antler_" + k
    p0 = (2.0 * s, 27.8, 0.4)
    p1 = seg(f"ab0_{k}", g, p0, 3.6, 0.85, 8, -34 * s)
    p2 = seg(f"ab1_{k}", g, p1, 3.4, 0.75, 6, -12 * s)
    p3 = seg(f"ab2_{k}", g, p2, 3.0, 0.65, 4, 10 * s)
    seg(f"ab3_{k}", g, p3, 2.0, 0.5, 0, 28 * s)
    seg(f"at0_{k}", g, p1, 2.6, 0.55, -6, -72 * s)
    t1 = seg(f"at1_{k}", g, p2, 2.4, 0.55, -28, -50 * s)
    seg(f"at1b_{k}", g, t1, 1.2, 0.4, -10, -20 * s)
    seg(f"at2_{k}", g, p3, 1.8, 0.45, 10, -48 * s)
    seg(f"at3_{k}", g, tip(p0, 1.4, 8, -34 * s), 1.6, 0.5, -30, 10 * s)     # brow tine pointing forward

# ------------------------------------------------------------------ flower crown: woven leaves + white and pink flowers
CR = [(0, FLW, 1.5), (35, PINK, 1.3), (70, FLW, 1.5), (115, None, 0), (150, FLW, 1.3), (180, None, 0), (210, FLW, 1.3), (245, None, 0), (290, FLW, 1.5), (325, PINK, 1.3)]
for i, (deg, col, sz) in enumerate(CR):
    a = math.radians(deg)
    x, z = math.sin(a) * 4.1, -math.cos(a) * 3.9
    y = 27.9 + 0.4 * math.cos(a)
    if col is not None:
        flower(f"crf{i}", "crown", (x, y, z), sz * 1.35, ry=-deg, col=col, rx=-20)
    for j in (-1, 1):
        b = math.radians(deg + j * 15)
        leaf(f"crl{i}_{j}", "crown", (math.sin(b) * 4.05, y + 0.5, -math.cos(b) * 3.85), 0.9, 1.6, rot=(0, -deg - j * 15, 70 * j), col=G_L if j > 0 else G)
m.cube("crown_band", "crown", (-4.0, 27.4, -3.75), (4.0, 27.9, 3.85), G_D, faces=all_faces(leafy(G_D, G_DD, G, ink=False), ("up", "down")) | {"up": clear, "down": clear})


# ================================================================== animation
PROPS = ["vine"]
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

    def r(self, bone, *keys): return self.rot(bone, *self._frame(keys, (0, 0, 0)))
    def p(self, bone, *keys): return self.pos(bone, *self._frame(keys, (0, 0, 0)))
    def s(self, bone, *keys): return self.scl(bone, *self._frame(keys, (1, 1, 1)))

    def show(self, bone, t0, t1, grow=2):
        return self.scl(bone, (0, *HIDE), (max(0, t0 - 0.5), *HIDE), (t0, .3, .3, .3), (t0 + grow, 1.15, 1.15, 1.15), (t0 + grow + 1, 1, 1, 1),
                        (t1, 1, 1, 1), (t1 + 1, .3, .3, .3), (t1 + 1.5, *HIDE), (self.ticks, *HIDE))

    def lag(self, bone, keys, delay=2, gain=1.0):
        seen, out = set(), []
        for (t, x, y, z) in keys:
            tt = min(self.ticks, t + delay)
            if tt in seen: continue
            seen.add(tt); out.append((tt, x * gain, y * gain, z * gain))
        return self.r(bone, *out)

    def hair(self, keys, delay=2):
        """keys (t, x, _, z): x>0 = hair/cloak flung back (body moved forward), z>0 = swung toward +X. Chain lag."""
        self.lag("bangs", [(t, -abs(x) * 0.2, 0, z * 0.3) for (t, x, y, z) in keys], delay)
        self.lag("hair_b", [(t, -x * 0.9, 0, z * 0.4) for (t, x, y, z) in keys], delay + 1)
        self.lag("lock_r", [(t, -x * 0.6, 0, z * 0.7 + max(0, x) * 0.4) for (t, x, y, z) in keys], delay + 1)
        self.lag("lock_l", [(t, -x * 0.6, 0, z * 0.7 - max(0, x) * 0.4) for (t, x, y, z) in keys], delay + 1)
        self.lag("tufts", [(t, -x * 0.2, 0, z * 0.25) for (t, x, y, z) in keys], delay)
        self.lag("cape_b", [(t, -x * 1.1, 0, z * 0.3) for (t, x, y, z) in keys], delay + 2)
        self.lag("cape_r", [(t, -x * 0.5, 0, z * 0.5 + abs(x) * 0.5) for (t, x, y, z) in keys], delay + 2)
        self.lag("cape_l", [(t, -x * 0.5, 0, z * 0.5 - abs(x) * 0.5) for (t, x, y, z) in keys], delay + 2)
        return self

    def done(self):
        for p in PROPS:
            if p not in self.tr or "scale" not in self.tr[p]:
                self.scl(p, (0, *HIDE))
        tracks = {b: {ch: sorted([(t / 20.0, x, y, z) for (t, x, y, z) in v], key=lambda q: q[0]) for ch, v in chs.items()}
                  for b, chs in self.tr.items()}
        m.anim(self.name, self.ticks / 20.0, tracks, loop=self.loop)


def legs(a, kr, kl=None, sr=None, sl=None):
    a.r("leg_r", *kr)
    a.r("leg_l", *(kl or [(t, x, -y, -z) for (t, x, y, z) in kr]))
    if sr: a.r("shin_r", *sr)
    if sl or sr: a.r("shin_l", *(sl or sr))


def mirror(keys):
    return [(t, x, -y, -z) for (t, x, y, z) in keys]


def sinekeys(n, step, amp, ph=0, period=None):
    period = period or n
    return [(t, amp[0] * math.sin((t + ph) / period * 2 * math.pi), amp[1] * math.sin((t + ph) / period * 2 * math.pi), amp[2] * math.sin((t + ph) / period * 2 * math.pi)) for t in range(0, n + 1, step)]


# ------------------------------------------------------------------ idle (80 loop): slouched sly sway, head tilt, right hand flexes its claws (pose of the art)
a = A("idle", 80, loop=True)
a.pos("body", (0, 0, 0, 0), (20, 0, -0.25, 0), (40, 0, 0, 0), (60, 0, -0.25, 0), (80, 0, 0, 0))
a.rot("body", (0, 0, 0, 2), (40, 0, 0, -2), (80, 0, 0, 2))
a.rot("chest", (0, 2, 0, -2), (20, 4, 4, -3), (40, 2, 0, -2), (60, 4, -4, -1), (80, 2, 0, -2))
a.rot("head", (0, 0, 0, 6), (20, 2, 6, 10), (36, 2, 6, 10), (44, -2, -4, 4), (60, -2, -6, 3), (80, 0, 0, 6))
a.rot("arm_r", (0, 0, 0, 6), (24, 0, 0, 6), (30, 40, -10, 34), (46, 44, -12, 36), (54, 0, 0, 6), (80, 0, 0, 6))
a.rot("fore_r", (0, 0, 0, 0), (24, 0, 0, 0), (30, 70, 0, 0), (46, 74, 0, 0), (54, 0, 0, 0), (80, 0, 0, 0))
a.rot("hand_r", (0, 0, 0, 0), (32, 0, 0, 0), (35, -20, 0, 0), (38, 10, 0, 0), (41, -20, 0, 0), (44, 0, 0, 0), (80, 0, 0, 0))
a.rot("arm_l", (0, 2, 0, -5), (40, -2, 0, -7), (80, 2, 0, -5))
a.rot("fore_l", (0, 8, 0, 0), (40, 12, 0, 0), (80, 8, 0, 0))
a.rot("leg_r", (0, 0, 0, 2), (80, 0, 0, 2))
a.rot("leg_l", (0, 0, 0, -3), (40, 0, 0, -1), (80, 0, 0, -3))
for b, ph, amp in (("hair_b", 0, (-3, 0, 2)), ("lock_r", 10, (-2, 0, 3)), ("lock_l", 25, (-2, 0, -3)), ("cape_b", 5, (-2, 0, 1)), ("cape_r", 15, (0, 0, 2)),
                   ("cape_l", 30, (0, 0, -2)), ("tufts", 20, (2, 0, 2)), ("bangs", 30, (0, 0, 1.5)), ("crown", 40, (0, 0, 1))):
    a.rot(b, *sinekeys(80, 10, amp, ph))
a.done()

# ------------------------------------------------------------------ walk (20 loop): light barefoot prowl, slight forward hunch, cloak swishing
a = A("walk", 20, loop=True)
a.pos("body", (0, 0, 0, 0), (5, 0, 0.6, 0), (10, 0, 0, 0), (15, 0, 0.6, 0), (20, 0, 0, 0))
a.rot("body", (0, -4, 5, 0), (5, -6, 0, 0), (10, -4, -5, 0), (15, -6, 0, 0), (20, -4, 5, 0))
a.rot("chest", (0, -4, -4, 0), (10, -4, 4, 0), (20, -4, -4, 0))
a.rot("leg_r", (0, 28, 0, 0), (5, 0, 0, 0), (10, -26, 0, 0), (15, 0, 0, 0), (20, 28, 0, 0))
a.rot("leg_l", (0, -26, 0, 0), (5, 0, 0, 0), (10, 28, 0, 0), (15, 0, 0, 0), (20, -26, 0, 0))
a.rot("shin_r", (0, 0, 0, 0), (12, -40, 0, 0), (16, -14, 0, 0), (20, 0, 0, 0))
a.rot("shin_l", (0, 0, 0, 0), (2, -40, 0, 0), (6, -14, 0, 0), (10, 0, 0, 0), (20, 0, 0, 0))
a.rot("arm_r", (0, -20, 0, 6), (10, 22, 0, 6), (20, -20, 0, 6))
a.rot("arm_l", (0, 22, 0, -6), (10, -20, 0, -6), (20, 22, 0, -6))
a.rot("fore_r", (0, 10, 0, 0), (10, 26, 0, 0), (20, 10, 0, 0))
a.rot("fore_l", (0, 26, 0, 0), (10, 10, 0, 0), (20, 26, 0, 0))
a.rot("head", (0, 4, 0, -3), (5, 2, 0, 0), (10, 4, 0, 3), (15, 2, 0, 0), (20, 4, 0, -3))
a.rot("hair_b", (0, -10, 0, 0), (5, -6, 0, 3), (10, -10, 0, 0), (15, -6, 0, -3), (20, -10, 0, 0))
a.rot("lock_r", (0, -6, 0, 6), (5, -3, 0, 2), (10, -6, 0, 8), (15, -3, 0, 2), (20, -6, 0, 6))
a.rot("lock_l", (0, -6, 0, -8), (5, -3, 0, -2), (10, -6, 0, -6), (15, -3, 0, -2), (20, -6, 0, -8))
a.rot("cape_b", (0, -10, 0, 2), (5, -7, 0, 0), (10, -10, 0, -2), (15, -7, 0, 0), (20, -10, 0, 2))
a.rot("cape_r", (0, -4, 0, 4), (10, -4, 0, 1), (20, -4, 0, 4))
a.rot("cape_l", (0, -4, 0, -1), (10, -4, 0, -4), (20, -4, 0, -1))
a.rot("tufts", (0, 0, 0, 3), (10, 0, 0, -3), (20, 0, 0, 3))
a.done()

# ------------------------------------------------------------------ antler_gore (28): rear up 0-8, head DROPS + lunge t10-12 (hit t12), toss upward t15, recover
a = A("antler_gore", 28)
a.r("chest", (6, 14, 0, 0), (8, 18, 0, 0), (11, -30, 0, 0), (12, -34, 0, 0), (15, -10, 0, 0), (18, -6, 0, 0), (24, 0, 0, 0))
a.r("head", (6, 16, 0, 0), (8, 20, 0, 0), (11, -40, 0, 0), (12, -46, 0, 0), (15, 20, 0, 0), (18, 8, 0, 0), (24, 0, 0, 0))
a.r("arm_r", (6, -30, 0, 30), (8, -36, 0, 34), (12, -40, 0, 20), (16, -10, 0, 16), (24, 0, 0, 0))
a.r("arm_l", (6, -30, 0, -30), (8, -36, 0, -34), (12, -40, 0, -20), (16, -10, 0, -16), (24, 0, 0, 0))
a.r("fore_r", (8, 40, 0, 0), (12, 10, 0, 0), (20, 0, 0, 0))
a.r("fore_l", (8, 40, 0, 0), (12, 10, 0, 0), (20, 0, 0, 0))
a.p("body", (6, 0, 0.6, 1.2), (8, 0, 0.8, 1.6), (11, 0, -0.8, -3.0), (12, 0, -1.0, -3.6), (15, 0, -0.2, -2.6), (20, 0, 0, -1.0), (26, 0, 0, 0))
legs(a, [(6, -10, 0, 0), (8, -14, 0, 0), (11, -40, 0, 0), (12, -44, 0, 0), (16, -20, 0, 0), (24, 0, 0, 0)],
     [(6, 10, 0, 0), (8, 12, 0, 0), (11, 34, 0, 0), (12, 38, 0, 0), (16, 16, 0, 0), (24, 0, 0, 0)],
     sr=[(8, -10, 0, 0), (12, 0, 0, 0), (16, -20, 0, 0)], sl=[(8, -20, 0, 0), (12, -30, 0, 0), (18, -10, 0, 0)])
a.hair([(0, 0, 0, 0), (8, -8, 0, 0), (12, 20, 0, 0), (15, -6, 0, 0), (20, 4, 0, 0), (26, 0, 0, 0)], delay=1)
a.done()

# ------------------------------------------------------------------ thorn_claw (30): right claw cocked 0-7, rake across t9, left claw back-rake t18, recover
a = A("thorn_claw", 30)
a.r("chest", (6, 4, 34, 0), (8, 0, 20, 0), (9, -6, -26, 0), (11, -6, -30, 0), (15, 2, 24, 0), (18, -6, -24, 0), (20, -6, -30, 0), (26, 0, 0, 0))
a.r("head", (6, 0, -20, 8), (9, -6, 14, -6), (15, 0, -16, 6), (18, -6, 16, -6), (24, 0, 0, 0))
a.r("arm_r", (5, 30, -10, 80), (7, 40, -20, 90), (9, 80, 30, 10), (11, 70, 40, -10), (15, 30, 0, 10), (22, 0, 0, 0))
a.r("fore_r", (7, 40, 0, 0), (9, 0, 0, 0), (12, 30, 0, 0), (20, 0, 0, 0))
a.r("hand_r", (7, -30, 0, 0), (9, 20, 0, 0), (13, 0, 0, 0))
a.r("arm_l", (8, 10, 0, -20), (14, 30, 10, -80), (16, 40, 20, -90), (18, 80, -30, -10), (20, 70, -40, 10), (26, 0, 0, 0))
a.r("fore_l", (16, 40, 0, 0), (18, 0, 0, 0), (21, 30, 0, 0), (28, 0, 0, 0))
a.r("hand_l", (16, -30, 0, 0), (18, 20, 0, 0), (22, 0, 0, 0))
a.p("body", (6, 0, -0.4, 0.4), (9, 0, -0.8, -1.4), (15, 0, -0.5, -0.6), (18, 0, -0.8, -2.0), (24, 0, -0.2, -0.6), (28, 0, 0, 0))
legs(a, [(6, 8, 0, 0), (9, -24, 0, 0), (15, -10, 0, 0), (18, 20, 0, 0), (24, 0, 0, 0)], [(6, -8, 0, 0), (9, 20, 0, 0), (15, 8, 0, 0), (18, -24, 0, 0), (24, 0, 0, 0)],
     sr=[(9, -10, 0, 0), (18, -24, 0, 0), (24, 0, 0, 0)], sl=[(9, -24, 0, 0), (18, -8, 0, 0), (24, 0, 0, 0)])
a.hair([(0, 0, 0, 0), (6, -4, 0, -10), (9, 10, 0, 16), (15, 2, 0, -8), (18, 12, 0, -16), (24, 4, 0, 4), (28, 0, 0, 0)], delay=1)
a.done()

# ------------------------------------------------------------------ vine_lash (32): vine sprouts from the right hand 3-8, arm wound back high, WHIP forward t14 (hit), yank back t20
a = A("vine_lash", 32)
a.show("vine", 3, 26, grow=3)
a.r("vine", (3, 30, 0, 20), (8, 60, 0, 30), (12, 40, 0, 10), (14, -20, 0, 0), (16, 10, 0, 0), (20, 40, 0, -10), (24, 60, 0, 0), (27, 20, 0, 0))
a.s("vine", (14, 1, 1.5, 1), (17, 1, 1.4, 1), (20, 1, 1.0, 1))
a.r("arm_r", (4, 40, 0, 40), (8, 160, 0, 30), (11, 170, 0, 20), (13, 100, 0, 0), (14, 80, 0, 0), (17, 70, 0, 4), (20, 120, 0, 20), (24, 60, 0, 10), (30, 0, 0, 0))
a.r("fore_r", (8, 20, 0, 0), (14, -10, 0, 0), (20, 30, 0, 0), (28, 0, 0, 0))
a.r("chest", (8, 14, 24, 0), (11, 16, 30, 0), (14, -12, -20, 0), (17, -10, -16, 0), (20, 10, 14, 0), (26, 0, 0, 0))
a.r("head", (8, 6, -16, 0), (14, -10, 14, 0), (20, 4, -6, 0), (26, 0, 0, 0))
a.r("arm_l", (8, -20, 0, -30), (14, 20, 0, -40), (20, -10, 0, -30), (28, 0, 0, 0))
a.p("body", (8, 0, 0, 1.0), (14, 0, -0.5, -1.6), (17, 0, -0.5, -1.4), (20, 0, 0, 0.6), (26, 0, 0, 0))
legs(a, [(8, 12, 0, 0), (14, -26, 0, 0), (20, 6, 0, 0), (26, 0, 0, 0)], [(8, -12, 0, 0), (14, 22, 0, 0), (20, -6, 0, 0), (26, 0, 0, 0)],
     sr=[(14, -12, 0, 0), (22, 0, 0, 0)], sl=[(14, -20, 0, 0), (22, 0, 0, 0)])
a.hair([(0, 0, 0, 0), (8, -10, 0, -6), (14, 16, 0, 10), (20, -8, 0, -4), (26, 0, 0, 0)], delay=2)
a.done()

# ------------------------------------------------------------------ petal_storm (36): cloak opens 0-10, three twirling flings of petals t14 / t20 / t26, cloak settles
a = A("petal_storm", 36)
a.r("root", (10, 0, -30, 0), (14, 0, 30, 0), (17, 0, -24, 0), (20, 0, 28, 0), (23, 0, -24, 0), (26, 0, 32, 0), (31, 0, 0, 0))
a.r("cape_r", (6, -10, 0, 30), (10, -14, 0, 50), (14, -6, 0, 62), (20, -10, 0, 56), (26, -6, 0, 64), (32, -6, 0, 10))
a.r("cape_l", (6, -10, 0, -30), (10, -14, 0, -50), (14, -6, 0, -62), (20, -10, 0, -56), (26, -6, 0, -64), (32, -6, 0, -10))
a.r("cape_b", (6, -20, 0, 0), (10, -30, 0, 0), (14, -44, 0, 0), (20, -40, 0, 0), (26, -46, 0, 0), (32, -6, 0, 0))
a.r("arm_r", (8, -10, 0, 60), (10, -10, 0, 70), (13, 60, 30, 70), (14, 80, 30, 40), (17, -10, 0, 70), (25, 30, 0, 80), (26, 50, 0, 60), (32, 0, 0, 0))
a.r("arm_l", (8, -10, 0, -60), (10, -10, 0, -70), (17, -10, 0, -70), (19, 60, -30, -70), (20, 80, -30, -40), (24, -10, 0, -70), (26, 50, 0, -60), (32, 0, 0, 0))
a.r("chest", (10, 10, 0, 0), (14, -6, 0, 0), (20, -6, 0, 0), (26, -8, 0, 0), (32, 0, 0, 0))
a.r("head", (10, 20, 0, 0), (14, 0, -20, 0), (20, 0, 20, 0), (26, -4, 0, 0), (32, 0, 0, 0))
a.p("body", (10, 0, 0.6, 0), (14, 0, 0, 0), (17, 0, 0.6, 0), (20, 0, 0, 0), (23, 0, 0.6, 0), (26, 0, 0, 0), (32, 0, 0, 0))
legs(a, [(10, 0, 0, 8), (14, -10, 0, 4), (20, 10, 0, 4), (26, -6, 0, 6), (32, 0, 0, 0)], [(10, 0, 0, -8), (14, 10, 0, -4), (20, -10, 0, -4), (26, 6, 0, -6), (32, 0, 0, 0)])
a.hair([(0, 0, 0, 0), (10, 4, 0, 0), (14, 6, 0, 20), (17, 6, 0, -20), (20, 6, 0, 20), (23, 6, 0, -20), (26, 8, 0, 20), (32, 0, 0, 0)], delay=2)
a.r("crown", (14, 0, 0, 6), (20, 0, 0, -6), (26, 0, 0, 6), (30, 0, 0, 0))
a.done()

# ------------------------------------------------------------------ thorn_spikes (34): right knee raised high 0-10, bare-foot STOMP t14 (thorn line erupts), claws spread, settle
a = A("thorn_spikes", 34)
a.r("leg_r", (6, 50, 0, 6), (10, 70, 0, 8), (12, 40, 0, 4), (14, -6, 0, 0), (20, -6, 0, 0), (26, 0, 0, 0))
a.r("shin_r", (6, -60, 0, 0), (10, -80, 0, 0), (13, -20, 0, 0), (14, 0, 0, 0))
a.r("leg_l", (10, -6, 0, -4), (14, 14, 0, -6), (20, 12, 0, -6), (26, 0, 0, 0))
a.r("shin_l", (14, -24, 0, 0), (20, -20, 0, 0), (26, 0, 0, 0))
a.p("body", (6, 0, 0.8, 0.6), (10, 0, 1.0, 0.8), (13, 0, 0, -0.4), (14, 0, -1.6, -0.6), (20, 0, -1.4, -0.6), (26, 0, 0, 0))
a.r("chest", (6, 10, 0, -6), (10, 14, 0, -8), (14, -24, 0, 0), (20, -20, 0, 0), (28, 0, 0, 0))
a.r("head", (10, 10, 0, 6), (14, -14, 0, 0), (17, 10, 0, 0), (22, 4, 0, 0), (28, 0, 0, 0))
a.r("arm_r", (10, -20, 0, 50), (14, 10, 0, 80), (20, 6, 0, 76), (28, 0, 0, 0))
a.r("arm_l", (10, -20, 0, -50), (14, 10, 0, -80), (20, 6, 0, -76), (28, 0, 0, 0))
a.r("fore_r", (10, 40, 0, 0), (14, 10, 0, 0), (24, 0, 0, 0))
a.r("fore_l", (10, 40, 0, 0), (14, 10, 0, 0), (24, 0, 0, 0))
a.hair([(0, 0, 0, 0), (10, -10, 0, 0), (14, -20, 0, 0), (17, 10, 0, 0), (22, 0, 0, 0)], delay=1)
a.r("cape_b", (14, -10, 0, 0), (16, 14, 0, 0), (22, 0, 0, 0))
a.done()

# ------------------------------------------------------------------ root_snare (40): drops to one knee 0-10, RIGHT PALM driven into the soil t14, fingers dig/clench 16-30 (roots squeeze), rises
a = A("root_snare", 40)
a.p("body", (8, 0, -2.8, 0), (12, 0, -3.6, -0.4), (14, 0, -3.8, -0.6), (30, 0, -3.6, -0.4), (36, 0, 0, 0))
a.r("chest", (8, -30, 0, 10), (12, -40, 0, 12), (14, -46, 0, 14), (30, -40, 0, 12), (36, 0, 0, 0))
a.r("head", (8, 24, 0, -6), (14, 36, 0, -10), (22, 34, 6, -10), (30, 30, 0, -8), (36, 0, 0, 0))
a.r("arm_r", (8, 30, 0, 10), (12, 60, 0, 16), (14, 70, 0, 18), (30, 66, 0, 18), (36, 0, 0, 0))
a.r("fore_r", (12, 0, 0, 0), (14, 6, 0, 0), (30, 6, 0, 0), (36, 0, 0, 0))
a.r("hand_r", (14, -30, 0, 0), (17, 30, 0, 0), (20, -10, 0, 0), (23, 30, 0, 0), (26, -10, 0, 0), (29, 30, 0, 0), (34, 0, 0, 0))
a.r("arm_l", (8, -30, 0, -40), (14, -40, 0, -60), (30, -36, 0, -56), (36, 0, 0, 0))
a.r("fore_l", (14, 50, 0, 0), (30, 50, 0, 0), (36, 0, 0, 0))
legs(a, [(8, 70, 0, 0), (14, 80, 0, 0), (30, 80, 0, 0), (36, 0, 0, 0)], [(8, -10, 0, 0), (14, -16, 0, 0), (30, -14, 0, 0), (36, 0, 0, 0)],
     sr=[(8, -60, 0, 0), (14, -70, 0, 0), (30, -70, 0, 0), (36, 0, 0, 0)], sl=[(8, -90, 0, 0), (14, -100, 0, 0), (30, -96, 0, 0), (36, 0, 0, 0)])
a.hair([(0, 0, 0, 0), (8, 10, 0, 0), (14, 16, 0, 0), (18, 10, 0, 4), (24, 14, 0, -4), (30, 12, 0, 0), (36, 0, 0, 0)], delay=2)
a.done()

# ------------------------------------------------------------------ antler_charge (40): pawing head-down crouch 0-10, CHARGE t10-24 (antlers first, galloping legs), skid t24-30, shake head
a = A("antler_charge", 40)
a.r("chest", (4, -20, 0, 0), (10, -36, 0, 0), (24, -38, 0, 0), (27, -10, 0, 0), (30, 4, 0, 0), (36, 0, 0, 0))
a.r("head", (4, -24, 0, 0), (10, -40, 0, 0), (24, -42, 0, 0), (27, 6, 0, 0), (30, 10, 10, 6), (32, 10, -10, -6), (34, 6, 8, 4), (38, 0, 0, 0))
a.p("body", (4, 0, -0.8, 0), (10, 0, -1.4, 0), (24, 0, -1.4, 0), (28, 0, -0.6, 0.6), (34, 0, 0, 0))
legs(a, [(2, -30, 0, 0), (4, 10, 0, 0), (6, -30, 0, 0), (8, 10, 0, 0), (10, -40, 0, 0), (12, 40, 0, 0), (14, -40, 0, 0), (16, 40, 0, 0), (18, -40, 0, 0), (20, 40, 0, 0), (22, -40, 0, 0), (24, 30, 0, 0), (27, -30, 0, 0), (32, -10, 0, 0), (36, 0, 0, 0)],
     [(2, 6, 0, 0), (10, 10, 0, 0), (12, -40, 0, 0), (14, 40, 0, 0), (16, -40, 0, 0), (18, 40, 0, 0), (20, -40, 0, 0), (22, 40, 0, 0), (24, -20, 0, 0), (27, 30, 0, 0), (32, 10, 0, 0), (36, 0, 0, 0)],
     sr=[(2, -40, 0, 0), (4, 0, 0, 0), (6, -40, 0, 0), (8, 0, 0, 0), (11, -60, 0, 0), (13, -10, 0, 0), (15, -60, 0, 0), (17, -10, 0, 0), (19, -60, 0, 0), (21, -10, 0, 0), (23, -60, 0, 0), (26, -10, 0, 0), (32, 0, 0, 0)],
     sl=[(10, -20, 0, 0), (13, -60, 0, 0), (15, -10, 0, 0), (17, -60, 0, 0), (19, -10, 0, 0), (21, -60, 0, 0), (23, -10, 0, 0), (26, -40, 0, 0), (32, 0, 0, 0)])
a.r("arm_r", (4, -40, 0, 20), (10, -60, 0, 24), (24, -60, 0, 24), (27, 30, 0, 30), (32, 0, 0, 10), (36, 0, 0, 0))
a.r("arm_l", (4, -40, 0, -20), (10, -60, 0, -24), (24, -60, 0, -24), (27, 30, 0, -30), (32, 0, 0, -10), (36, 0, 0, 0))
a.r("fore_r", (10, 50, 0, 0), (24, 50, 0, 0), (30, 0, 0, 0))
a.r("fore_l", (10, 50, 0, 0), (24, 50, 0, 0), (30, 0, 0, 0))
a.hair([(0, 0, 0, 0), (10, 4, 0, 0), (12, 10, 0, 0), (24, 10, 0, 0), (27, -14, 0, 0), (31, 6, 0, 10), (36, 0, 0, 0)], delay=2)
a.done()

# ------------------------------------------------------------------ bramble_ring (38): crouch gathering 0-12, explosive SPIN t12-18 (thorn ring t16), arms flung wide, land crouched, rise
a = A("bramble_ring", 38)
a.r("root", (12, 0, 0, 0), (14, 0, 120, 0), (16, 0, 250, 0), (18, 0, 340, 0), (20, 0, 360, 0), (38, 0, 360, 0))
a.p("body", (8, 0, -2.0, 0), (12, 0, -2.6, 0), (14, 0, 0.4, 0), (16, 0, 0.8, 0), (18, 0, -1.6, 0), (24, 0, -1.8, 0), (32, 0, 0, 0))
a.r("chest", (8, -26, 0, 0), (12, -30, 0, 0), (14, 4, 0, 0), (16, 8, 0, 0), (19, -20, 0, 0), (24, -16, 0, 0), (32, 0, 0, 0))
a.r("head", (8, 20, 0, 0), (12, 24, 0, 0), (16, -4, 0, 0), (19, 14, 0, 0), (26, 0, 0, 0))
sym = [(8, 20, 0, -10), (12, 30, 0, -20), (14, 0, 0, 90), (16, 0, 0, 100), (18, 0, 0, 80), (22, -10, 0, 50), (30, 0, 0, 0)]
a.r("arm_r", *sym)
a.r("arm_l", *mirror(sym))
legs(a, [(8, 40, 0, 6), (12, 50, 0, 8), (14, 0, 0, 14), (16, 0, 0, 16), (18, 30, 0, 10), (24, 26, 0, 8), (32, 0, 0, 0)],
     sr=[(8, -60, 0, 0), (12, -76, 0, 0), (14, -10, 0, 0), (18, -40, 0, 0), (24, -36, 0, 0), (32, 0, 0, 0)])
a.r("cape_r", (14, -10, 0, 50), (16, -10, 0, 70), (18, -10, 0, 60), (22, 0, 0, 20), (28, 0, 0, 0))
a.r("cape_l", (14, -10, 0, -50), (16, -10, 0, -70), (18, -10, 0, -60), (22, 0, 0, -20), (28, 0, 0, 0))
a.r("cape_b", (14, -30, 0, 0), (16, -50, 0, 0), (18, -40, 0, 0), (22, -10, 0, 0), (28, 0, 0, 0))
a.r("lock_r", (14, 0, 0, 30), (18, 0, 0, 40), (22, 0, 0, 10), (28, 0, 0, 0))
a.r("lock_l", (14, 0, 0, -30), (18, 0, 0, -40), (22, 0, 0, -10), (28, 0, 0, 0))
a.r("hair_b", (12, 10, 0, 0), (16, -30, 0, 0), (20, -10, 0, 0), (28, 0, 0, 0))
a.done()

# ------------------------------------------------------------------ seed_volley (32): reaches into the cloak 0-8, underhand LOB of three seed pods t12, watches them arc, recover
a = A("seed_volley", 32)
a.r("arm_r", (4, -30, 0, 10), (8, -50, 0, -10), (10, -30, 0, 0), (12, 110, 0, 10), (14, 130, 0, 14), (18, 100, 0, 10), (26, 0, 0, 0))
a.r("fore_r", (6, 80, 0, 0), (8, 90, 0, 0), (12, -10, 0, 0), (16, 0, 0, 0))
a.r("hand_r", (8, 30, 0, 0), (12, -40, 0, 0), (15, 0, 0, 0))
a.r("chest", (4, 4, 20, 0), (8, 10, 30, 0), (12, -8, -18, 0), (14, -4, -22, 0), (20, 6, -10, 0), (28, 0, 0, 0))
a.r("head", (8, -8, -16, 0), (12, 6, 10, 0), (16, 22, 10, 0), (20, 14, 6, 0), (28, 0, 0, 0))
a.r("arm_l", (8, 20, 0, -10), (12, -20, 0, -20), (18, -10, 0, -10), (26, 0, 0, 0))
a.r("cape_r", (4, -10, 0, 20), (8, -10, 0, 28), (12, 0, 0, 6), (18, 0, 0, 0))
a.p("body", (8, 0, -1.0, 0.6), (12, 0, 0.2, -1.0), (16, 0, 0, -0.6), (24, 0, 0, 0))
legs(a, [(8, 12, 0, 0), (12, -20, 0, 0), (18, -10, 0, 0), (26, 0, 0, 0)], [(8, -12, 0, 0), (12, 16, 0, 0), (18, 8, 0, 0), (26, 0, 0, 0)],
     sr=[(8, -30, 0, 0), (12, -6, 0, 0), (20, 0, 0, 0)], sl=[(8, -20, 0, 0), (12, -30, 0, 0), (20, 0, 0, 0)])
a.hair([(0, 0, 0, 0), (8, -6, 0, -6), (12, 10, 0, 8), (18, 4, 0, 0), (26, 0, 0, 0)], delay=2)
a.done()

# ------------------------------------------------------------------ pollen_cloud (34): deep inhale (lean back, chest swells) 0-10, BLOWS t14-22 (hands cupped at the mouth), shake off
a = A("pollen_cloud", 34)
a.r("chest", (6, 14, 0, 0), (10, 20, 0, 0), (13, -16, 0, 0), (14, -20, 0, 0), (22, -16, 0, 0), (26, 0, 0, 0))
a.s("chest", (6, 1.05, 1.03, 1.08), (10, 1.1, 1.05, 1.14), (14, 1, 1, 1), (22, 0.96, 1, 0.94), (26, 1, 1, 1))
a.r("head", (6, 20, 0, 0), (10, 28, 0, 0), (13, -6, 0, 0), (14, -10, 0, 0), (18, -12, 6, 0), (22, -10, -6, 0), (26, 10, 0, 12), (30, 0, 0, 0))
sym = [(6, 20, 0, -10), (10, 30, 0, -20), (13, 80, 20, -30), (14, 90, 26, -30), (22, 90, 26, -30), (26, 20, 0, 0)]
a.r("arm_r", *sym)
a.r("arm_l", *mirror(sym))
a.r("fore_r", (10, 40, 0, 0), (14, 70, 0, 0), (22, 70, 0, 0), (26, 0, 0, 0))
a.r("fore_l", (10, 40, 0, 0), (14, 70, 0, 0), (22, 70, 0, 0), (26, 0, 0, 0))
a.p("body", (10, 0, 0.4, 1.0), (14, 0, -0.4, -0.8), (22, 0, -0.4, -0.8), (28, 0, 0, 0))
legs(a, [(10, -10, 0, 0), (14, -18, 0, 0), (22, -18, 0, 0), (28, 0, 0, 0)], [(10, 10, 0, 0), (14, 20, 0, 0), (22, 20, 0, 0), (28, 0, 0, 0)],
     sl=[(14, -16, 0, 0), (22, -16, 0, 0), (28, 0, 0, 0)])
a.hair([(0, 0, 0, 0), (10, -10, 0, 0), (14, 10, 0, 0), (18, 14, 0, 6), (22, 12, 0, -6), (28, 0, 0, 0)], delay=1)
a.r("crown", (26, 0, 0, 10), (28, 0, 0, -8), (30, 0, 0, 4), (32, 0, 0, 0))
a.done()

# ------------------------------------------------------------------ bloom_heal (44): kneels, hands folded to the chest 0-12, crown BLOOMS t20 (heal + petal burst), sways, rises
a = A("bloom_heal", 44)
a.p("body", (10, 0, -3.0, 0), (14, 0, -3.4, 0), (30, 0, -3.4, 0), (38, 0, 0, 0))
legs(a, [(10, 80, 0, 0), (30, 80, 0, 0), (38, 0, 0, 0)], [(10, -6, 0, 0), (30, -6, 0, 0), (38, 0, 0, 0)],
     sr=[(10, -90, 0, 0), (30, -90, 0, 0), (38, 0, 0, 0)], sl=[(10, -110, 0, 0), (30, -110, 0, 0), (38, 0, 0, 0)])
a.r("chest", (10, -14, 0, 0), (16, -18, 0, 0), (20, 14, 0, 0), (24, 18, 0, 0), (30, 10, 0, 0), (38, 0, 0, 0))
a.r("head", (10, -20, 0, 0), (16, -26, 0, 0), (20, 30, 0, 0), (24, 34, 0, 0), (30, 20, 0, 6), (38, 0, 0, 0))
sym = [(8, 40, 30, -30), (12, 50, 40, -36), (18, 50, 40, -36), (20, 10, 0, 100), (24, 0, 0, 110), (30, 10, 0, 60), (38, 0, 0, 0)]
a.r("arm_r", *sym)
a.r("arm_l", *mirror(sym))
a.r("fore_r", (12, 80, 0, 0), (18, 84, 0, 0), (20, 0, 0, 0), (38, 0, 0, 0))
a.r("fore_l", (12, 80, 0, 0), (18, 84, 0, 0), (20, 0, 0, 0), (38, 0, 0, 0))
a.s("crown", (14, 1, 1, 1), (18, 0.9, 0.9, 0.9), (20, 1.5, 1.5, 1.5), (22, 1.4, 1.4, 1.4), (32, 1.4, 1.4, 1.4), (38, 1, 1, 1))
a.r("crown", (20, 0, 20, 0), (32, 0, 60, 0), (38, 0, 0, 0))
a.r("cape_r", (20, -10, 0, 40), (26, -6, 0, 30), (34, 0, 0, 0))
a.r("cape_l", (20, -10, 0, -40), (26, -6, 0, -30), (34, 0, 0, 0))
a.r("cape_b", (20, -30, 0, 0), (26, -20, 0, 0), (34, 0, 0, 0))
a.hair([(0, 0, 0, 0), (10, 4, 0, 0), (20, 20, 0, 0), (26, 12, 0, 6), (32, 6, 0, -6), (38, 0, 0, 0)], delay=2)
a.done()

# ------------------------------------------------------------------ leap_stomp (40): deer-like crouch 0-8, LEAP t8-18 (knees tucked, arms up), crashes down t20 (shockwave), recover
a = A("leap_stomp", 40)
a.p("root", (6, 0, -2.4, 0), (8, 0, -2.8, 0), (11, 0, 5.0, 0), (14, 0, 7.0, 0), (17, 0, 4.0, 0), (20, 0, -2.6, 0), (26, 0, -2.0, 0), (34, 0, 0, 0))
a.r("root", (8, 10, 0, 0), (11, -16, 0, 0), (15, 0, 0, 0), (18, -20, 0, 0), (20, -10, 0, 0), (28, 0, 0, 0))
a.r("chest", (6, -20, 0, 0), (8, -26, 0, 0), (12, 10, 0, 0), (17, -10, 0, 0), (20, -40, 0, 0), (26, -34, 0, 0), (34, 0, 0, 0))
a.r("head", (6, 20, 0, 0), (12, -10, 0, 0), (17, 10, 0, 0), (20, -20, 0, 0), (26, -10, 0, 0), (34, 0, 0, 0))
sym = [(6, -40, 0, 20), (8, -50, 0, 24), (12, 170, 0, 20), (16, 160, 0, 30), (19, 60, 0, 40), (20, 20, 0, 50), (26, 20, 0, 46), (34, 0, 0, 0)]
a.r("arm_r", *sym)
a.r("arm_l", *mirror(sym))
legs(a, [(6, 50, 0, 0), (8, 60, 0, 0), (11, -20, 0, 0), (14, 70, 0, 0), (17, 40, 0, 0), (20, 70, 0, 4), (26, 60, 0, 4), (34, 0, 0, 0)],
     [(6, 50, 0, 0), (8, 60, 0, 0), (11, -10, 0, 0), (14, 60, 0, 0), (17, 30, 0, 0), (20, 10, 0, -4), (26, 10, 0, -4), (34, 0, 0, 0)],
     sr=[(6, -80, 0, 0), (8, -100, 0, 0), (11, -10, 0, 0), (14, -110, 0, 0), (17, -40, 0, 0), (20, -100, 0, 0), (26, -90, 0, 0), (34, 0, 0, 0)],
     sl=[(6, -80, 0, 0), (8, -100, 0, 0), (11, -10, 0, 0), (14, -100, 0, 0), (17, -30, 0, 0), (20, -40, 0, 0), (26, -36, 0, 0), (34, 0, 0, 0)])
a.hair([(0, 0, 0, 0), (8, -10, 0, 0), (11, -30, 0, 0), (15, 6, 0, 0), (18, 26, 0, 0), (20, -24, 0, 0), (24, 8, 0, 0), (32, 0, 0, 0)], delay=1)
a.done()

# ------------------------------------------------------------------ verdant_wrath (52, enraged): arms raised to the sky 0-14 (hair + cloak lift), SLAMS both palms t18, then two more waves t28 / t38
a = A("verdant_wrath", 52)
sym = [(6, 140, 0, 30), (12, 170, 0, 20), (14, 176, 0, 16), (17, 60, 0, 10), (18, 40, 0, 10), (24, 150, 0, 20), (27, 60, 0, 10), (28, 40, 0, 10), (34, 160, 0, 20),
       (37, 60, 0, 10), (38, 36, 0, 10), (44, 30, 0, 10), (50, 0, 0, 0)]
a.r("arm_r", *sym)
a.r("arm_l", *mirror(sym))
a.r("chest", (6, 14, 0, 0), (14, 24, 0, 0), (18, -40, 0, 0), (24, 16, 0, 0), (28, -40, 0, 0), (34, 18, 0, 0), (38, -46, 0, 0), (44, -36, 0, 0), (50, 0, 0, 0))
a.r("head", (6, 20, 0, 0), (14, 34, 0, 0), (18, -20, 0, 0), (24, 26, 0, 0), (28, -20, 0, 0), (34, 30, 0, 0), (38, -24, 0, 0), (44, -10, 0, 0), (50, 0, 0, 0))
a.p("body", (6, 0, 0.6, 0), (14, 0, 1.0, 0), (18, 0, -3.0, -0.6), (24, 0, -0.6, 0), (28, 0, -3.0, -0.6), (34, 0, -0.4, 0), (38, 0, -3.4, -0.6), (44, 0, -3.0, -0.4), (50, 0, 0, 0))
legs(a, [(14, 0, 0, 10), (18, 60, 0, 12), (24, 20, 0, 10), (28, 60, 0, 12), (34, 20, 0, 10), (38, 66, 0, 12), (44, 60, 0, 10), (50, 0, 0, 0)],
     sr=[(18, -80, 0, 0), (24, -30, 0, 0), (28, -80, 0, 0), (34, -30, 0, 0), (38, -90, 0, 0), (44, -80, 0, 0), (50, 0, 0, 0)])
a.s("crown", (14, 1.2, 1.2, 1.2), (18, 1.3, 1.3, 1.3), (44, 1.3, 1.3, 1.3), (50, 1, 1, 1))
a.s("antler_r", (10, 1.1, 1.1, 1.1), (14, 1.25, 1.25, 1.25), (44, 1.25, 1.25, 1.25), (50, 1, 1, 1))
a.s("antler_l", (10, 1.1, 1.1, 1.1), (14, 1.25, 1.25, 1.25), (44, 1.25, 1.25, 1.25), (50, 1, 1, 1))
a.r("hair_b", (6, -8, 0, 0), (14, -16, 0, 0), (18, 10, 0, 0), (24, -14, 0, 0), (28, 10, 0, 0), (34, -16, 0, 0), (38, 12, 0, 0), (46, 0, 0, 0))
a.r("lock_r", (14, 0, 0, 34), (18, 0, 0, 10), (24, 0, 0, 30), (28, 0, 0, 10), (34, 0, 0, 34), (38, 0, 0, 10), (46, 0, 0, 0))
a.r("lock_l", (14, 0, 0, -34), (18, 0, 0, -10), (24, 0, 0, -30), (28, 0, 0, -10), (34, 0, 0, -34), (38, 0, 0, -10), (46, 0, 0, 0))
a.r("cape_r", (14, -10, 0, 40), (18, 0, 0, 10), (24, -10, 0, 36), (28, 0, 0, 10), (34, -10, 0, 40), (38, 0, 0, 12), (46, 0, 0, 0))
a.r("cape_l", (14, -10, 0, -40), (18, 0, 0, -10), (24, -10, 0, -36), (28, 0, 0, -10), (34, -10, 0, -40), (38, 0, 0, -12), (46, 0, 0, 0))
a.r("cape_b", (14, -36, 0, 0), (18, -6, 0, 0), (24, -30, 0, 0), (28, -6, 0, 0), (34, -36, 0, 0), (38, -6, 0, 0), (46, 0, 0, 0))
a.done()

# ------------------------------------------------------------------ thorn_cage (46, enraged): vine sprouts, right arm POINTS t10-12 (cage drawn round the target), fist slowly closes, CLENCH t30 (cage bursts)
a = A("thorn_cage", 46)
a.show("vine", 4, 34, grow=3)
a.r("vine", (4, 40, 0, 0), (10, 10, 0, 20), (14, -10, 0, -20), (18, 10, 0, 20), (22, -10, 0, -20), (26, 10, 0, 20), (30, 30, 0, 0), (34, 20, 0, 0))
a.s("vine", (10, 1, 1.4, 1), (28, 1, 1.4, 1), (30, 1, 0.7, 1))
a.r("arm_r", (4, 30, 0, 20), (8, 60, 0, 30), (10, 96, 0, 6), (12, 100, 0, 0), (26, 96, 0, 2), (29, 120, 0, 0), (30, 110, 0, 0), (36, 80, 0, 4), (42, 0, 0, 0))
a.r("fore_r", (10, -6, 0, 0), (26, -6, 0, 0), (30, 20, 0, 0), (40, 0, 0, 0))
a.r("hand_r", (10, -40, 0, 0), (20, -10, 0, 0), (28, 20, 0, 0), (30, 50, 0, 0), (38, 0, 0, 0))
a.r("arm_l", (8, -10, 0, -30), (12, -20, 0, -40), (30, 20, 0, -60), (38, 0, 0, -10), (44, 0, 0, 0))
a.r("chest", (6, 6, 20, 0), (10, -6, -14, 0), (12, -10, -18, 0), (28, -8, -14, 0), (30, -16, -22, 0), (36, -4, -6, 0), (42, 0, 0, 0))
a.r("head", (6, 0, -16, 0), (12, -8, 10, -8), (20, -6, 14, -12), (28, -6, 10, -8), (30, -12, 14, 0), (36, 4, 0, 10), (42, 0, 0, 0))
a.p("body", (10, 0, -0.4, -1.0), (28, 0, -0.4, -1.0), (30, 0, -0.8, -1.4), (38, 0, 0, 0))
legs(a, [(10, -20, 0, 0), (30, -24, 0, 0), (38, 0, 0, 0)], [(10, 18, 0, 0), (30, 22, 0, 0), (38, 0, 0, 0)], sl=[(10, -16, 0, 0), (30, -20, 0, 0), (38, 0, 0, 0)])
a.hair([(0, 0, 0, 0), (6, -4, 0, -6), (12, 8, 0, 8), (24, 4, 0, 4), (30, 14, 0, 6), (36, -4, 0, 0), (42, 0, 0, 0)], delay=2)
a.done()

# ------------------------------------------------------------------ death (40): staggers, flowers droop, knees give t10-18, slumps sideways onto the cloak t18-30, crown slips
a = A("death", 40)
a.r("chest", (4, 16, 0, -10), (8, -10, 0, 8), (12, -30, 0, 6), (18, -36, 0, 0), (40, -30, 0, 0))
a.r("head", (4, 26, 0, -10), (8, -16, 0, 14), (12, -20, 0, 20), (18, -30, 0, 26), (40, -20, 0, 30))
a.r("arm_r", (4, -20, 0, 50), (8, 20, 0, 20), (14, 10, 0, 10), (24, 20, 0, 60), (40, 10, 0, 70))
a.r("arm_l", (4, -20, 0, -50), (8, 20, 0, -20), (14, 30, 0, -10), (24, 10, 0, -30), (40, 0, 0, -20))
legs(a, [(8, 0, 0, 0), (12, 60, 0, 6), (18, 90, 0, 6), (40, 90, 0, 6)], sr=[(8, 0, 0, 0), (12, -80, 0, 0), (18, -110, 0, 0), (40, -110, 0, 0)])
a.p("body", (8, 0, 0, 0), (12, 0, -3.6, 0), (18, 0, -6.5, 1.0), (40, 0, -6.5, 1.0))
a.r("root", (18, 0, 0, 0), (24, 0, 0, 40), (28, 0, 0, 76), (30, 0, 0, 70), (32, 0, 0, 74), (40, 0, 0, 74))
a.p("root", (18, 0, 0, 0), (28, 2.0, -1.0, 0), (40, 2.0, -1.0, 0))
a.r("crown", (18, 0, 0, 0), (26, -20, 0, 20), (32, -24, 0, 24), (40, -24, 0, 24))
a.s("crown", (18, 1, 1, 1), (30, 0.9, 0.85, 0.9), (40, 0.9, 0.85, 0.9))
a.hair([(0, 0, 0, 0), (4, -10, 0, 10), (8, 8, 0, -10), (14, 6, 0, 4), (24, -10, 0, -16), (30, 10, 0, -20), (40, 6, 0, -20)], delay=2)
a.done()

m.save(OUT)
print("cubes", len(m.cubes), "anims", [x["name"] for x in m.anims])
