"""Mutant Lana (FPE Green mutant student, LANA 004) - generates assets/fpe/bbmodels/mutant_lana.bbmodel.
Reference: docs/ref/confirmed/mutant_lana.png. Chibi girl (hitbox 0.7 x 2.0): long grey hair with a parted fringe, a curly
ahoge and two little clips, HUGE round black eyes, a wide toothy grin, black mutation goo eating her LEFT side (half the face,
the left arm, the left leg), grey turtleneck with a "004" badge, a white jagged spiky shawl, white shorts, chunky white boots.
Right hand = a white animal-skull puppet maw with fangs, left hand = a big black bag-monster with huge white teeth.
Blockbench space: Y up, ground 0, faces -Z. Character's RIGHT = +X.
Rotation signs: arm/leg rx>0 = swing forward, torso/head rx>0 = lean back / look up, ry>0 = turn to the character's left,
rz>0 = toward +X. Jaws point forward: rx<0 = open. Position z<0 = forward, y>0 = up.
Rest pose = modelled pose (rest rotations 0). Every key tick matches entity/characters/MutantLana.java.
Run: python3 tools/bbgen/chars/mutant_lana.py
"""
import math, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from bbgen import Model, mix  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "../../../src/main/resources/assets/fpe/bbmodels/mutant_lana.bbmodel")

# ------------------------------------------------------------------ palette (grey-scale ink art + a hint of colour in the goo)
SKIN, SKIN_D = 0xF2F1F3, 0xCFCDD5
HAIR, HAIR_D, HAIR_L, HAIR_DD = 0x9C9EA9, 0x70737F, 0xC5C7CF, 0x55586A
WH, WH_D, WH_DD, WH_L = 0xF3F3F6, 0xCBCCD4, 0x9C9EA9, 0xFFFFFF
TOP, TOP_D, TOP_L = 0x8A90A0, 0x666C7C, 0xA9AEBB
LEGW, LEGW_D = 0xD4D6DD, 0xA7AAB6
LINE = 0x23232B
GOO, GOO_L, GOO_S = 0x131217, 0x34313E, 0x4C4658
MOUTH = 0x2A1C26
TONGUE, TONGUE_D = 0x5A3348, 0x34202E
CLEAR = (0, 0, 0, 0)

m = Model("mutant_lana", S=8, atlas=2048)
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


def cloth(base=WH, dark=WH_D, n=2, ink=True, fold=WH_DD):
    def f(F):
        for y in range(F.h):
            for x in range(F.w):
                k = y / max(1, F.h - 1)
                F.px(x, y, mix(base, dark, 0.05 + 0.3 * k * k + (0.12 if x < 2 or x > F.w - 3 else 0)))
        for i in range(n):
            x = int((i + 0.5) * F.w / n) + R.randint(-2, 2)
            for y in range(int(F.h * 0.25), F.h):
                F.px(x, y, mix(base, fold, 0.45))
                F.px(x + 1, y, mix(base, WH_L, 0.4))
        if ink: outline()(F)
    return f


def knit(F):
    """turtleneck: vertical rib lines + soft shading"""
    for y in range(F.h):
        for x in range(F.w):
            k = y / max(1, F.h - 1)
            c = mix(TOP_L, TOP, 0.4 + 0.5 * k)
            if x % 4 == 0: c = mix(c, TOP_D, 0.35)
            F.px(x, y, c)
    outline(mix(TOP_D, LINE, 0.5))(F)


def hairp(base=HAIR, ink=True):
    """grey strands: random darker strand lines, highlight band, inked edge"""
    def f(F):
        for y in range(F.h):
            for x in range(F.w):
                F.px(x, y, mix(HAIR_L, base, min(1, 0.55 + 0.6 * y / max(1, F.h))))
        for x in range(0, F.w, 3):
            xx = x + R.randint(0, 1)
            for y in range(R.randint(0, 3), F.h):
                F.px(xx, y, mix(base, HAIR_D, 0.55))
        hb = int(F.h * 0.22)
        for x in range(F.w):
            if (x // 2) % 3: F.px(x, hb + (x % 2), HAIR_L)
        if ink: outline(HAIR_DD)(F)
    return f


def goop(F):
    """black goo: glossy streaks, violet sheen, bumpy"""
    for y in range(F.h):
        for x in range(F.w):
            F.px(x, y, GOO_L if R.random() < 0.06 else GOO)
    for _ in range(max(1, F.w // 5)):
        x = R.randint(0, F.w - 1)
        y0 = R.randint(0, max(0, F.h // 2))
        for y in range(y0, min(F.h, y0 + R.randint(2, 6))):
            F.px(x, y, GOO_S)
    F.rect(0, 0, F.w, 1, GOO_L)


def spikep(tip_left, col=WH):
    """flat triangle (spike) on a rectangle face, outside = transparent"""
    def f(F):
        for y in range(F.h):
            for x in range(F.w):
                u = (x + .5) / F.w
                u = 1 - u if not tip_left else u
                # u=0 at tip, 1 at base -> half-height allowed grows with u
                half = 0.5 * u
                v = abs((y + .5) / F.h - 0.5)
                if v > half: F.px(x, y, CLEAR)
                elif v > half - 1.2 / F.h: F.px(x, y, LINE)
                else: F.px(x, y, mix(col, WH_D if col == WH else GOO_L, 0.35 * (1 - u) + 0.2 * (y / F.h)))
    return f


def toothp(down, col=WH_L):
    """tooth triangle: base at top (down=True) or bottom"""
    def f(F):
        for y in range(F.h):
            for x in range(F.w):
                v = (y + .5) / F.h
                v = v if down else 1 - v           # 0 at base, 1 at tip
                half = 0.5 * (1 - v)
                d = abs((x + .5) / F.w - 0.5)
                if d > half + 0.02: F.px(x, y, CLEAR)
                elif d > half - 1.0 / F.w: F.px(x, y, mix(col, WH_DD, 0.7))
                else: F.px(x, y, mix(col, WH_D, 0.5 * v))
    return f


def clear(F):
    F.rect(0, 0, F.w, F.h, CLEAR)


def eye(F, ex, ey, r, look):
    F.disc(ex, ey, r + 1.4, LINE)
    F.disc(ex, ey, r, WH_L)
    F.disc(ex + look, ey + 0.8, r - 3.0, GOO)
    F.disc(ex + look - r * 0.3, ey - r * 0.3, 2.2, WH_L, glow=True)
    F.disc(ex + look + r * 0.3, ey + r * 0.3, 0.8, 0x8A8A9A)


def face_front(F):
    W, H = F.w, F.h
    for y in range(H):
        for x in range(W):
            F.px(x, y, mix(SKIN, SKIN_D, 0.05 + 0.25 * (y / H)))
    # black goo eating the character's LEFT half (texel right), wavy border, drips toward the chin
    for y in range(H):
        b = 33 + 3.5 * math.sin(y / 4.5) + (y > 34) * (y - 34) * 0.25
        for x in range(int(b), W):
            F.px(x, y, GOO_L if R.random() < 0.05 else GOO)
        F.px(int(b) - 1, y, mix(GOO, SKIN_D, 0.5))
    for (dx, l) in ((27, 7), (30, 11), (24, 4)):
        F.rect(dx, H - l, 2, l, GOO)
        F.disc(dx + 1, H - l, 1.3, GOO)
    F.line(36, 12, 41, 30, GOO_S, 1)
    ey = 25
    eye(F, 19, ey, 10.5, 1.5)          # char RIGHT eye (texel left)
    eye(F, 46, ey, 10.5, -1.0)         # char LEFT eye, ringed in goo
    for (ex, s) in ((19, -1), (46, 1)):    # lashes flicking out like the art
        for i in range(3):
            a = math.radians(-150 + i * 22) if s < 0 else math.radians(-30 - i * 22)
            F.line(ex + math.cos(a) * 11, ey + math.sin(a) * 11, ex + math.cos(a) * 14.5, ey + math.sin(a) * 14.5, LINE, 1)
    # wide grin: white teeth, zig-zag bite line, inked outline, corners curl up
    top = lambda x: 39 - 3.2 * math.exp(-((x - 10) / 3.5) ** 2) - 3.2 * math.exp(-((x - 55) / 3.5) ** 2)
    bot = lambda x: 41 + 12 * math.sin(math.pi * min(1, max(0, (x - 9) / 47)))
    for x in range(8, 58):
        for y in range(int(top(x)), int(bot(x)) + 1):
            F.px(x, y, WH_L)
    for x in range(8, 58):
        F.px(x, int(top(x)) - 1, LINE); F.px(x, int(top(x)) - 2, LINE)
        F.px(x, int(bot(x)) + 1, LINE); F.px(x, int(bot(x)) + 2, LINE)
    mid = lambda x: (top(x) + bot(x)) / 2
    for x in range(10, 56):
        zz = mid(x) + (2.2 if (x // 3) % 2 else -2.2) * min(1, (bot(x) - top(x)) / 10)
        F.px(x, int(zz), LINE)
        F.px(x, int(zz) + 1, mix(LINE, WH_D, 0.4))
    for x in range(13, 55, 5):
        F.line(x, top(x), x, mid(x) - 2, WH_DD, 1)
    # nose dot + goo cheek veins
    F.rect(31, 33, 2, 1, SKIN_D)
    for (x0, y0, x1, y1) in ((52, 36, 60, 32), (50, 55, 58, 58)):
        F.line(x0, y0, x1, y1, GOO_S, 1)


def badge004(F):
    F.rect(0, 0, F.w, F.h, WH)
    outline(LINE)(F)
    font = {"0": ["111", "101", "101", "101", "111"], "4": ["101", "101", "111", "001", "001"]}
    x0, y0 = (F.w - 11) // 2, (F.h - 5) // 2
    for n, ch in enumerate("004"):
        for j, row in enumerate(font[ch]):
            for i, b in enumerate(row):
                if b == "1": F.px(x0 + n * 4 + i, y0 + j, LINE)


def skullp(F):
    """white animal skull: bone shading, cracks, ink edge"""
    for y in range(F.h):
        for x in range(F.w):
            F.px(x, y, mix(WH_L, WH_D, 0.08 + 0.35 * (y / F.h)))
    for _ in range(2):
        x, y = R.randint(2, F.w - 3), R.randint(1, F.h - 3)
        for k in range(R.randint(3, 6)):
            F.px(x, y, WH_DD); x += R.choice((-1, 0, 1)); y += 1
    outline()(F)


def skull_side(F, front_left):
    skullp(F)
    ex = F.w * (0.75 if front_left else 0.25)
    F.disc(ex, F.h * 0.4, min(F.h, F.w) * 0.27, LINE)
    F.disc(ex, F.h * 0.4, min(F.h, F.w) * 0.2, GOO)


# ------------------------------------------------------------------ shape helpers
def spike(name, parent, base, length, h, d, yaw, roll, col=WH, side=1):
    """flat spike pointing along +X (side=1) / -X (side=-1) from base point, rotated by yaw (ry) and roll (rz)"""
    x, y, z = base
    x0, x1 = (x, x + length) if side > 0 else (x - length, x)
    p_n, p_s = spikep(side > 0, col), spikep(side < 0, col)
    m.cube(name, parent, (x0, y - h / 2, z - d / 2), (x1, y + h / 2, z + d / 2), col, origin=base, rot=(0, yaw, roll),
           faces={"north": p_n, "south": p_s, "up": clear, "down": clear, "east": clear, "west": clear})


def tooth(name, parent, c, w, h, down=True, col=WH_L, rot=(0, 0, 0), d=None):
    x, y, z = c
    d = d or w
    y0, y1 = (y - h, y) if down else (y, y + h)
    p = toothp(down, col)
    m.cube(name, parent, (x - w / 2, y0, z - d / 2), (x + w / 2, y1, z + d / 2), col, origin=c, rot=rot,
           faces={"north": p, "south": p, "east": p, "west": p, "up": clear, "down": clear})


# ------------------------------------------------------------------ skeleton
m.group("root", (0, 0, 0))
m.group("body", (0, 12, 0), parent="root")
m.group("chest", (0, 14, 0), parent="body")
m.group("head", (0, 21, 0), parent="chest")
m.group("bangs", (0, 28.6, -3.7), parent="head")
m.group("hair_b", (0, 27.5, 3.6), parent="head")
m.group("lock_r", (4.1, 27.0, -1.0), parent="head")
m.group("lock_l", (-4.1, 27.0, -1.0), parent="head")
m.group("ahoge", (0.4, 29.3, -0.6), parent="head")
m.group("shawl", (0, 20.0, 0), parent="chest")
m.group("spk_r", (4.0, 19.4, 0), parent="shawl")
m.group("spk_l", (-4.0, 19.4, 0), parent="shawl")
m.group("arm_r", (3.7, 19.8, 0), parent="chest")
m.group("fore_r", (3.9, 16.6, 0), parent="arm_r")
m.group("wmaw", (2.4, 16.6, -3.6), parent="fore_r")
m.group("wjaw", (1.6, 16.3, -3.8), parent="wmaw")
m.group("arm_l", (-3.7, 19.8, 0), parent="chest")
m.group("fore_l", (-3.9, 16.0, 0), parent="arm_l")
m.group("bmaw", (-4.0, 12.8, -0.4), parent="fore_l")
m.group("bjaw", (-4.6, 9.8, 0.8), parent="bmaw")
m.group("tongue", (-4.6, 9.9, -3.8), parent="bmaw")
for s, k in ((1, "r"), (-1, "l")):
    m.group("leg_" + k, (1.4 * s, 12, 0), parent="body")
    m.group("shin_" + k, (1.4 * s, 7, 0), parent="leg_" + k)
m.group("puddle", (0, 0, -9), parent="root")
m.group("goospk", (0, 0, 0), parent="root")

# ------------------------------------------------------------------ legs: right = pale tights, left = black goo; chunky white boots
for s, k in ((1, "r"), (-1, "l")):
    x = 1.4 * s
    goo = k == "l"
    lp = goop if goo else cloth(LEGW, LEGW_D, n=1, fold=LEGW_D)
    m.cube("thigh_" + k, "leg_" + k, (x - 0.85, 7.0, -0.85), (x + 0.85, 12.0, 0.85), GOO if goo else LEGW, faces=all_faces(lp))
    m.cube("calf_" + k, "shin_" + k, (x - 0.8, 3.0, -0.8), (x + 0.8, 7.2, 0.8), GOO if goo else LEGW, faces=all_faces(lp))
    m.cube("boot_" + k, "shin_" + k, (x - 1.55, 0.0, -2.0), (x + 1.55, 2.6, 1.4), WH,
           faces={"north": cloth(n=1), "south": cloth(n=1), "east": cloth(n=2), "west": cloth(n=2), "up": cloth(n=1), "down": outline(WH_DD)})
    m.cube("bootcuff_" + k, "shin_" + k, (x - 1.35, 2.4, -1.35), (x + 1.35, 4.2, 1.25), WH, origin=(x, 2.4, 0), rot=(0, 0, 4 * s),
           faces=all_faces(cloth(n=2), ("down",)))
    m.cube("bootfold_" + k, "shin_" + k, (x - 1.45, 3.6, -1.45), (x + 1.45, 4.3, 1.35), WH_L, faces=all_faces(outline()))
    m.cube("sole_" + k, "shin_" + k, (x - 1.6, -0.02, -2.05), (x + 1.6, 0.35, 1.45), WH_DD)
    m.cube("toe_" + k, "shin_" + k, (x - 1.3, 0.3, -2.4), (x + 1.3, 1.9, -1.9), WH, faces=all_faces(cloth(n=1)))
# goo drips oozing down the left leg + a blob on the right boot
for i, (y, z, h) in enumerate(((10.4, -0.95, 2.2), (8.6, 0.95, 1.6), (5.6, -0.9, 2.4))):
    m.cube(f"legdrip{i}", "leg_l" if y > 7 else "shin_l", (-1.4 - 0.4 + i * 0.3, y - h, z - 0.15), (-1.4 + 0.1 + i * 0.3, y, z + 0.15), GOO, faces=all_faces(goop))
m.cube("bootgoo_l", "shin_l", (-3.0, 2.0, -2.1), (-0.2, 2.8, 1.5), GOO, faces=all_faces(goop))

# ------------------------------------------------------------------ hips: white shorts, flared cuffs
m.cube("shorts", "body", (-3.1, 11.6, -1.95), (3.1, 14.5, 1.95), WH, faces=all_faces(cloth(n=3), ("up",)))
for s, k in ((1, "r"), (-1, "l")):
    m.cube("shortleg_" + k, "leg_" + k, (1.4 * s - 1.5, 9.8, -1.6), (1.4 * s + 1.5, 12.2, 1.6), WH, origin=(1.4 * s, 12, 0), rot=(0, 0, 5 * s),
           faces=all_faces(cloth(n=2), ("up",)))
m.cube("shortseam", "body", (-0.12, 11.4, -2.0), (0.12, 14.2, -1.92), WH_DD)

# ------------------------------------------------------------------ torso: grey turtleneck, 004 badge, goo seeping over the left side
m.cube("torso", "chest", (-3.0, 14.0, -1.8), (3.0, 20.4, 1.8), TOP, faces=all_faces(knit))
m.cube("turtle", "chest", (-2.3, 20.0, -2.0), (2.3, 21.4, 2.0), TOP, faces=all_faces(knit))
m.cube("turtle_fold", "chest", (-2.45, 20.1, -2.15), (2.45, 20.6, 2.15), TOP_L, faces=all_faces(outline(TOP_D)))
m.cube("badge", "chest", (-2.7, 16.9, -2.0), (-0.6, 18.3, -1.82), WH, faces={"north": badge004})
m.cube("badgeclip", "chest", (-1.9, 18.2, -2.0), (-1.4, 18.8, -1.85), WH_DD)
m.cube("hem", "chest", (-3.1, 13.9, -1.9), (3.1, 14.6, 1.9), TOP_D, faces=all_faces(outline(LINE)))
m.cube("goo_side", "chest", (-3.25, 14.2, -1.6), (-2.7, 19.4, 1.6), GOO, faces=all_faces(goop))
for i, (y, h) in enumerate(((19.0, 2.4), (17.2, 3.2), (15.4, 1.6))):
    m.cube(f"goodrip{i}", "chest", (-2.75, y - h, -1.95), (-2.15 + 0.2 * i, y, -1.8), GOO, faces=all_faces(goop))

# ------------------------------------------------------------------ shawl: white jagged collar + spikes radiating sideways like the art
def shawlp(F):
    cloth(n=3)(F)
    for x in range(F.w):          # jagged lower edge
        zz = int(abs(((x % 8) - 4)) * 0.8)
        for y in range(F.h - zz, F.h):
            F.px(x, y, CLEAR)
        F.px(x, F.h - zz - 1, LINE)


m.cube("shawl_ring", "shawl", (-4.1, 18.0, -2.45), (4.1, 20.7, 2.45), WH, faces={"north": shawlp, "south": shawlp, "east": shawlp, "west": shawlp, "up": cloth(n=2), "down": clear})
m.cube("shawl_top", "shawl", (-3.4, 20.4, -2.2), (3.4, 21.0, 2.2), WH_L, faces=all_faces(cloth(n=1)))
for s, k in ((1, "r"), (-1, "l")):
    sp = "spk_" + k
    bx = 4.0 * s
    spike(f"spA_{k}", sp, (bx, 19.6, -0.6), 7.0, 2.8, 0.5, 15 * s, 18 * s, side=s)
    spike(f"spB_{k}", sp, (bx, 19.0, 0.8), 6.0, 2.4, 0.5, -20 * s, -14 * s, side=s)
    spike(f"spC_{k}", sp, (bx - 0.4 * s, 18.4, 1.6), 4.6, 2.0, 0.5, -45 * s, -38 * s, side=s)
    spike(f"spD_{k}", sp, (bx - 0.6 * s, 18.5, -1.8), 3.6, 1.6, 0.5, 40 * s, -30 * s, side=s)
# front/back drooping points
for i, (x, z, rz) in enumerate(((2.0, -2.5, 70), (-1.4, -2.5, -75), (1.6, 2.5, 80), (-1.8, 2.5, -70))):
    spike(f"spF{i}", "shawl", (x, 18.6, z), 2.4, 1.4, 0.4, 0, rz, side=1 if rz > 0 else -1)

# ------------------------------------------------------------------ right arm: short grey sleeve, white forearm bent forward, white skull-puppet maw
m.cube("sleeve_r", "arm_r", (3.0, 16.2, -0.9), (4.7, 20.2, 0.9), TOP, faces=all_faces(knit))
m.cube("cuff_r", "arm_r", (2.95, 16.0, -0.95), (4.75, 16.7, 0.95), TOP_D)
m.cube("forearm_r", "fore_r", (3.15, 15.85, -3.9), (4.65, 17.35, 0.4), SKIN, origin=(3.9, 16.6, 0), rot=(0, 22, 0), faces=all_faces(cloth(SKIN, SKIN_D, n=1)))
# skull: snout block + cranium + brow, black sockets, nostril slits, fangs, lower jaw on its own bone
m.cube("wskull", "wmaw", (0.4, 16.4, -8.4), (4.0, 19.0, -3.0), WH,
       faces={"north": combo(skullp, lambda F: (F.rect(F.w * 0.3, 2, 2, 3, LINE), F.rect(F.w * 0.62, 2, 2, 3, LINE))),
              "south": skullp, "up": skullp, "down": lambda F: F.rect(0, 0, F.w, F.h, MOUTH),
              "east": lambda F: skull_side(F, False), "west": lambda F: skull_side(F, True)})
m.cube("wcran", "wmaw", (0.1, 16.8, -4.6), (4.3, 20.2, -1.6), WH,
       faces={"north": skullp, "south": skullp, "up": skullp, "down": skullp,
              "east": lambda F: (skullp(F), F.disc(F.w * 0.4, F.h * 0.45, 1.6, LINE), F.disc(F.w * 0.4, F.h * 0.45, 1.0, GOO)),
              "west": lambda F: (skullp(F), F.disc(F.w * 0.6, F.h * 0.45, 1.6, LINE), F.disc(F.w * 0.6, F.h * 0.45, 1.0, GOO))})
m.cube("wbrow", "wmaw", (0.0, 19.4, -5.4), (4.4, 20.0, -3.4), WH_L, origin=(2.2, 19.7, -4.4), rot=(-12, 0, 0), faces=all_faces(skullp))
m.cube("wthroat", "wmaw", (0.8, 15.6, -7.8), (3.6, 16.6, -3.2), MOUTH, faces=all_faces(lambda F: F.rect(0, 0, F.w, F.h, MOUTH)))
for i in range(5):
    tooth(f"wtU{i}", "wmaw", (0.65 + i * 0.68, 16.45, -8.2 + (0.0 if i in (1, 2, 3) else 0.4)), 0.55, 1.0 + (0.4 if i in (0, 4) else 0), down=True)
for i, z in enumerate((-7.2, -6.2, -5.2, -4.2)):
    tooth(f"wtR{i}", "wmaw", (3.75, 16.45, z), 0.45, 0.8, down=True)
    tooth(f"wtL{i}", "wmaw", (0.65, 16.45, z), 0.45, 0.8, down=True)
m.cube("wjawb", "wjaw", (0.5, 14.4, -8.0), (3.9, 15.6, -3.4), WH, origin=(2.2, 16.3, -3.8), rot=(-18, 0, 0),
       faces={"north": skullp, "south": skullp, "east": skullp, "west": skullp, "down": skullp, "up": lambda F: F.rect(0, 0, F.w, F.h, MOUTH)})
for i in range(4):
    z = -7.6 + i * 1.1
    yy = 15.6 + (abs(z + 3.8)) * math.tan(math.radians(18)) * 0.0
    tooth(f"wtD{i}", "wjaw", (0.8 + i * 0.6 + (1.2 if i > 1 else 0), 15.5, -7.6), 0.5, 1.0, down=False, rot=(-18, 0, 0))
for i, z in enumerate((-6.6, -5.4)):
    tooth(f"wtDr{i}", "wjaw", (3.55, 15.6, z), 0.42, 0.8, down=False, rot=(-18, 0, 0))
    tooth(f"wtDl{i}", "wjaw", (0.85, 15.6, z), 0.42, 0.8, down=False, rot=(-18, 0, 0))

# ------------------------------------------------------------------ left arm: black goo arm, ring + strap, big black bag-monster with white teeth
m.cube("arm_l_up", "arm_l", (-4.75, 15.6, -0.9), (-3.0, 20.2, 0.9), GOO, faces=all_faces(goop))
m.cube("arm_l_blob", "arm_l", (-5.0, 18.4, -1.1), (-2.9, 20.4, 1.1), GOO, faces=all_faces(goop))
m.cube("fore_l_c", "fore_l", (-4.7, 12.4, -0.85), (-3.1, 16.2, 0.85), GOO, faces=all_faces(goop))
m.cube("ring_l", "fore_l", (-4.95, 13.4, -1.05), (-2.85, 14.0, 1.05), WH_D, faces=all_faces(outline()))


def bagp_front(F):
    """front of the monster: black, huge mouth band filled with dark throat"""
    goop(F)
    F.rect(1, int(F.h * 0.55), F.w - 2, F.h, MOUTH)


m.cube("bhead", "bmaw", (-7.0, 9.8, -3.6), (-2.2, 13.4, 1.2), GOO,
       faces={"north": bagp_front, "south": goop, "east": goop, "west": goop, "up": goop, "down": lambda F: F.rect(0, 0, F.w, F.h, MOUTH)})
m.cube("bhead_top", "bmaw", (-6.6, 13.2, -3.2), (-2.6, 13.9, 0.8), GOO, faces=all_faces(goop))
m.cube("bcheek_r", "bmaw", (-2.4, 9.4, -3.3), (-1.8, 12.6, 0.8), GOO, faces=all_faces(goop))
m.cube("bcheek_l", "bmaw", (-7.4, 9.4, -3.3), (-6.8, 12.6, 0.8), GOO, faces=all_faces(goop))
m.cube("bthroat", "bmaw", (-6.6, 9.0, -3.0), (-2.6, 10.2, 0.6), MOUTH, faces=all_faces(lambda F: F.rect(0, 0, F.w, F.h, MOUTH)))
m.cube("bjaw_c", "bjaw", (-7.0, 7.4, -3.6), (-2.2, 9.0, 1.2), GOO, origin=(-4.6, 9.8, 0.8), rot=(-14, 0, 0),
       faces={"north": goop, "south": goop, "east": goop, "west": goop, "down": goop, "up": lambda F: F.rect(0, 0, F.w, F.h, MOUTH)})
for i in range(5):     # big upper fangs (front)
    tooth(f"btU{i}", "bmaw", (-6.5 + i * 1.0, 9.8, -3.55), 0.9, 1.5 if i % 2 == 0 else 1.1, down=True, d=0.5)
for i, z in enumerate((-2.4, -1.2, 0.0)):
    tooth(f"btUr{i}", "bmaw", (-2.55, 9.8, z), 0.5, 1.0, down=True, d=0.8)
    tooth(f"btUl{i}", "bmaw", (-6.65, 9.8, z), 0.5, 1.0, down=True, d=0.8)
for i in range(4):     # lower fangs ride the jaw
    tooth(f"btD{i}", "bjaw", (-6.0 + i * 1.0, 8.95, -3.45), 0.9, 1.3, down=False, d=0.5, rot=(-14, 0, 0))
# bag handle loop + strap ring on top (it is carried like a bag)
m.cube("handle_a", "bmaw", (-5.9, 13.8, -0.9), (-5.5, 15.3, -0.5), WH_D, faces=all_faces(outline()))
m.cube("handle_b", "bmaw", (-3.7, 13.8, -0.9), (-3.3, 15.3, -0.5), WH_D, faces=all_faces(outline()))
m.cube("handle_c", "bmaw", (-5.9, 15.0, -0.9), (-3.3, 15.4, -0.5), WH_D, faces=all_faces(outline()))
m.cube("bring", "bmaw", (-2.4, 11.6, -3.0), (-1.6, 12.4, -2.2), WH_L, faces=all_faces(lambda F: (F.rect(0, 0, F.w, F.h, WH_L), outline()(F), F.rect(2, 2, F.w - 4, F.h - 4, GOO))))
# tongue (tongue_lash / maw_trap): long, extends forward out of the bag-monster
def tonguep(F):
    for y in range(F.h):
        for x in range(F.w):
            F.px(x, y, mix(TONGUE, TONGUE_D, 0.3 + 0.4 * abs(x / max(1, F.w - 1) - 0.5)))
    F.rect(F.w // 2, 0, 1, F.h, TONGUE_D)
    outline(GOO)(F)


m.cube("tongue_a", "tongue", (-5.3, 9.5, -12.0), (-3.9, 10.2, -3.6), TONGUE, faces=all_faces(tonguep))
m.cube("tongue_tip", "tongue", (-5.6, 9.3, -13.6), (-3.6, 10.4, -11.8), TONGUE, faces=all_faces(tonguep))

# ------------------------------------------------------------------ head, face, hair
m.cube("skull", "head", (-4.0, 21.0, -3.5), (4.0, 28.5, 3.5), SKIN,
       faces={"north": face_front, "south": hairp(), "east": hairp(), "west": hairp(), "up": hairp(), "down": cloth(SKIN, SKIN_D, n=0)})
m.cube("hair_cap", "head", (-4.35, 25.6, -3.2), (4.35, 29.4, 3.85), HAIR, faces={k: hairp() for k in ALL if k != "north"} | {"north": hairp()})
# fringe strands (parted, pointy tips) - tips at different heights, a gap over the goo eye
BANGS = [(-4.1, 1.3, 26.4, -6), (-2.9, 1.3, 26.7, -3), (-1.7, 1.3, 27.0, 2), (-0.5, 1.1, 27.6, 5), (0.7, 1.2, 26.9, -4), (1.9, 1.3, 26.6, -2),
         (3.0, 1.3, 26.2, 4)]
for i, (x, w, yb, rz) in enumerate(BANGS):
    m.cube(f"bang{i}", "bangs", (x, yb, -3.95), (x + w, 29.2, -3.55), HAIR, origin=(x + w / 2, 29.2, -3.75), rot=(0, 0, rz),
           faces={"north": combo(hairp(), lambda F: [F.px(xx, yy, CLEAR) for yy in range(F.h - 5, F.h) for xx in range(F.w)
                                                     if abs(xx + .5 - F.w / 2) > (F.h - yy) * F.w / 10]),
                  "south": hairp(), "east": hairp(), "west": hairp(), "up": hairp(), "down": clear})
# side locks: long, flaring past the shoulders like the art (right side longer)
for s, k in ((1, "r"), (-1, "l")):
    g = "lock_" + k
    x = 4.1 * s
    L = (19.0, 17.4, 20.6) if s > 0 else (20.0, 18.0, 21.4)
    for j, (z, yb, rz) in enumerate(((-2.8, L[0], 6), (-1.2, L[1], 10), (0.6, L[2], 14))):
        m.cube(f"lock{j}_{k}", g, (x - 0.55 if s > 0 else x - 0.45, yb, z - 0.7), (x + 0.45 if s > 0 else x + 0.55, 28.6, z + 0.9), HAIR,
               origin=(x, 28.4, z), rot=(0, 0, rz * s),
               faces={"north": hairp(), "south": hairp(), "east": hairp(), "west": hairp(), "up": hairp(),
                      "down": lambda F: F.rect(0, 0, F.w, F.h, HAIR_DD)})
    for j, (yb, rz) in enumerate(((21.6, 30), (23.4, 42))):
        spike(f"lockspk{j}_{k}", g, (x + 0.2 * s, 23.0 + j * 1.5, -0.4 - j), 2.0 + j * 0.4, 1.2, 0.8, 0, -rz * s, col=HAIR, side=s)
m.cube("clip0", "head", (2.0, 28.0, -3.98), (2.35, 29.4, -3.7), LINE)
m.cube("clip1", "head", (2.7, 27.9, -3.98), (3.05, 29.3, -3.7), LINE)
# long back hair: panel + strands with pointed tips
m.cube("back_panel", "hair_b", (-4.4, 16.4, 3.0), (4.4, 29.2, 4.2), HAIR, origin=(0, 29.2, 3.6), rot=(8, 0, 0), faces=all_faces(hairp()))
for i, (x, yb, rz) in enumerate(((-3.6, 14.6, -8), (-1.8, 13.8, -3), (0.0, 13.2, 0), (1.8, 13.9, 3), (3.6, 14.8, 8))):
    m.cube(f"backstr{i}", "hair_b", (x - 0.9, yb, 3.6), (x + 0.9, 18.0, 4.5), HAIR, origin=(x, 18, 4), rot=(10, 0, rz),
           faces={"south": combo(hairp(), lambda F: [F.px(xx, yy, CLEAR) for yy in range(F.h - 6, F.h) for xx in range(F.w)
                                                     if abs(xx + .5 - F.w / 2) > (F.h - yy) * F.w / 12]),
                  "north": hairp(), "east": hairp(), "west": hairp(), "up": clear, "down": clear})
# ahoge: stalk + spiral curl
m.cube("aho0", "ahoge", (0.1, 29.2, -0.85), (0.7, 31.2, -0.35), HAIR, origin=(0.4, 29.3, -0.6), rot=(0, 0, -10), faces=all_faces(hairp(ink=False)))
CURL = [(0.9, 31.4, 40), (1.6, 32.2, 80), (1.3, 33.0, 140), (0.4, 33.1, 200), (-0.1, 32.4, 260), (0.4, 31.9, 320)]
for i, (x, y, rz) in enumerate(CURL):
    m.cube(f"aho{i + 1}", "ahoge", (x - 0.6, y - 0.3, -0.85), (x + 0.6, y + 0.3, -0.35), HAIR, origin=(x, y, -0.6), rot=(0, 0, rz),
           faces=all_faces(hairp(ink=False)))

# ------------------------------------------------------------------ props: goo puddle with jutting fangs (ink_puddle), goo spikes ring (mutation_burst)
for i, (x, z, w, d) in enumerate(((0, 0, 7, 5), (-2.5, 1.5, 4, 4), (2.6, -1.4, 4, 3.4), (0.5, -2.6, 3.4, 2.4))):
    m.cube(f"pud{i}", "puddle", (x - w / 2, 0.02 + i * 0.03, -9 + z - d / 2), (x + w / 2, 0.3 + i * 0.03, -9 + z + d / 2), GOO, faces=all_faces(goop))
for i, (x, z, h, rr) in enumerate(((-1.5, -9.8, 3.2, -14), (1.4, -8.4, 2.6, 12), (0.0, -10.8, 2.0, 4), (2.6, -10.2, 1.8, 20))):
    tooth(f"pudfang{i}", "puddle", (x, 0.2, z), 0.9, h, down=False, col=WH, rot=(rr * 0.4, 0, rr))
for i in range(8):
    a = math.radians(i * 45 + 22.5)
    x, z = math.sin(a) * 8.5, math.cos(a) * 8.5
    for j, (h, w, off) in enumerate(((6.0, 1.6, 0.0), (3.5, 1.0, 1.4))):
        ox, oz = x + math.cos(a) * off * (1 if j else 0), z - math.sin(a) * off * (1 if j else 0)
        m.cube(f"gsp{i}_{j}", "goospk", (ox - w / 2, 0, oz - w / 2), (ox + w / 2, h, oz + w / 2), GOO, origin=(ox, 0, oz),
               rot=(math.degrees(math.cos(a)) * 0.25, 0, -math.degrees(math.sin(a)) * 0.25),
               faces={"north": toothp(False, GOO_L), "south": toothp(False, GOO_L), "east": toothp(False, GOO_L), "west": toothp(False, GOO_L),
                      "up": clear, "down": clear})


# ================================================================== animation
PROPS = ["tongue", "puddle", "goospk"]
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
        """prop visible inside [t0,t1]: grows in over `grow` ticks with overshoot"""
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
        """keys: x>0 = hair flicks back, z>0 = toward +X. Fringe, sides, back, ahoge, shawl spikes lag in a chain"""
        self.lag("bangs", [(t, -abs(x) * 0.25, 0, z * 0.3) for (t, x, y, z) in keys], delay)
        self.lag("hair_b", [(t, x * 0.9, 0, z * 0.4) for (t, x, y, z) in keys], delay + 1)
        self.lag("lock_r", [(t, x * 0.6, 0, z * 0.7 + max(0, x) * 0.5) for (t, x, y, z) in keys], delay + 1)
        self.lag("lock_l", [(t, x * 0.6, 0, z * 0.7 - max(0, x) * 0.5) for (t, x, y, z) in keys], delay + 1)
        self.lag("ahoge", [(t, x * 1.4, 0, z * 1.6) for (t, x, y, z) in keys], delay + 2)
        self.lag("spk_r", [(t, 0, 0, z * 0.4 + abs(x) * 0.5) for (t, x, y, z) in keys], delay + 1)
        self.lag("spk_l", [(t, 0, 0, z * 0.4 - abs(x) * 0.5) for (t, x, y, z) in keys], delay + 1)
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


def chomp(a, bone, times, open_=-35, closed=6):
    """jaw snapping: open before, slam shut on each time t"""
    ks = []
    for t in times:
        ks += [(t - 3, open_, 0, 0), (t - 1, open_ * 1.15, 0, 0), (t, closed, 0, 0), (t + 1.5, closed * 0.3, 0, 0)]
    a.r(bone, *ks)


# ------------------------------------------------------------------ idle (80 loop): sways, creepy head tilt, both maws chew, ahoge bounces
a = A("idle", 80, loop=True)
a.pos("body", (0, 0, 0, 0), (20, 0, -0.2, 0), (40, 0, 0, 0), (60, 0, -0.2, 0), (80, 0, 0, 0))
a.rot("body", (0, 0, 0, 0), (20, 0, 4, 0), (40, 0, 0, 0), (60, 0, -4, 0), (80, 0, 0, 0))
a.rot("chest", (0, 0, 0, 0), (20, 3, 0, -1), (40, 0, 0, 0), (60, 3, 0, 1), (80, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (14, 0, 0, 0), (20, -2, 6, -16), (36, -2, 6, -18), (42, 0, 0, 0), (58, 0, 0, 0), (62, 4, -4, 8), (72, 4, -4, 8), (80, 0, 0, 0))
a.rot("arm_r", (0, 0, 0, 0), (20, 4, 0, 2), (40, 0, 0, 0), (60, 4, 0, 2), (80, 0, 0, 0))
a.rot("fore_r", (0, 0, 0, 0), (20, 6, 0, 0), (40, 0, 0, 0), (60, 6, 0, 0), (80, 0, 0, 0))
a.rot("wmaw", (0, 0, 0, 0), (24, 0, -8, 4), (30, 0, 6, -6), (40, 0, 0, 0), (80, 0, 0, 0))
a.rot("wjaw", (0, 0, 0, 0), (8, -14, 0, 0), (10, 4, 0, 0), (12, -8, 0, 0), (14, 4, 0, 0), (16, 0, 0, 0), (48, 0, 0, 0), (52, -18, 0, 0), (54, 4, 0, 0), (56, 0, 0, 0), (80, 0, 0, 0))
a.rot("arm_l", (0, 6, 0, -4), (20, 2, 0, -6), (40, 6, 0, -4), (60, 10, 0, -2), (80, 6, 0, -4))
a.rot("bmaw", (0, 0, 0, 0), (20, 0, 10, 4), (40, 0, 0, 0), (60, 0, -10, -4), (80, 0, 0, 0))
a.rot("bjaw", (0, 0, 0, 0), (12, 0, 0, 0), (16, -22, 0, 0), (20, 0, 0, 0), (24, -12, 0, 0), (27, 0, 0, 0), (64, 0, 0, 0), (68, -26, 0, 0), (72, 2, 0, 0), (76, 0, 0, 0), (80, 0, 0, 0))
a.rot("ahoge", *[(t, 6 * math.sin(t / 80 * 4 * math.pi), 0, 10 * math.sin(t / 80 * 2 * math.pi)) for t in range(0, 81, 10)])
for b, ph, amp in (("hair_b", 0, 3), ("lock_r", 10, 4), ("lock_l", 25, -4), ("spk_r", 5, 3), ("spk_l", 15, -3), ("bangs", 30, 1)):
    a.rot(b, *[(t, amp * 0.5 * math.sin((t + ph) / 80 * 2 * math.pi), 0, amp * math.sin((t + ph) / 40 * 2 * math.pi)) for t in range(0, 81, 10)])
a.done()

# ------------------------------------------------------------------ walk (20 loop): bouncy skip, skull hugged close, bag-monster swings like a purse
a = A("walk", 20, loop=True)
a.pos("body", (0, 0, 0, 0), (3, 0, 0.8, 0), (5, 0, 0, 0), (10, 0, 0, 0), (13, 0, 0.8, 0), (15, 0, 0, 0), (20, 0, 0, 0))
a.rot("body", (0, 3, 6, 0), (5, 6, 0, 0), (10, 3, -6, 0), (15, 6, 0, 0), (20, 3, 6, 0))
a.rot("leg_r", (0, 26, 0, 0), (5, 0, 0, 0), (10, -24, 0, 0), (15, 0, 0, 0), (20, 26, 0, 0))
a.rot("leg_l", (0, -24, 0, 0), (5, 0, 0, 0), (10, 26, 0, 0), (15, 0, 0, 0), (20, -24, 0, 0))
a.rot("shin_r", (0, 0, 0, 0), (12, -30, 0, 0), (16, -10, 0, 0), (20, 0, 0, 0))
a.rot("shin_l", (0, 0, 0, 0), (2, -30, 0, 0), (6, -10, 0, 0), (10, 0, 0, 0), (20, 0, 0, 0))
a.rot("arm_r", (0, -6, 0, 2), (10, 6, 0, 4), (20, -6, 0, 2))
a.rot("wmaw", (0, 4, 0, 0), (5, -4, 0, 0), (10, 4, 0, 0), (15, -4, 0, 0), (20, 4, 0, 0))
a.rot("wjaw", (0, 0, 0, 0), (3, -12, 0, 0), (6, 0, 0, 0), (13, -12, 0, 0), (16, 0, 0, 0), (20, 0, 0, 0))
a.rot("arm_l", (0, 24, 0, -6), (10, -22, 0, -8), (20, 24, 0, -6))
a.rot("bmaw", (0, -14, 0, 0), (4, 6, 0, 0), (10, 14, 0, 0), (14, -6, 0, 0), (20, -14, 0, 0))
a.rot("bjaw", (0, 0, 0, 0), (4, -16, 0, 0), (8, 0, 0, 0), (14, -16, 0, 0), (18, 0, 0, 0), (20, 0, 0, 0))
a.rot("head", (0, 0, 0, -5), (5, -4, 0, 0), (10, 0, 0, 5), (15, -4, 0, 0), (20, 0, 0, -5))
a.rot("ahoge", (0, -10, 0, 12), (5, 12, 0, 0), (10, -10, 0, -12), (15, 12, 0, 0), (20, -10, 0, 12))
a.rot("hair_b", (0, 8, 0, 0), (5, 2, 0, 3), (10, 8, 0, 0), (15, 2, 0, -3), (20, 8, 0, 0))
a.rot("lock_r", (0, 4, 0, 6), (5, 0, 0, 0), (10, 4, 0, 10), (15, 0, 0, 0), (20, 4, 0, 6))
a.rot("lock_l", (0, 4, 0, -10), (5, 0, 0, 0), (10, 4, 0, -6), (15, 0, 0, 0), (20, 4, 0, -10))
a.rot("spk_r", (0, 0, 0, 6), (5, 0, 0, -4), (10, 0, 0, 6), (15, 0, 0, -4), (20, 0, 0, 6))
a.rot("spk_l", (0, 0, 0, 4), (5, 0, 0, -6), (10, 0, 0, 4), (15, 0, 0, -6), (20, 0, 0, 4))
a.done()

# ------------------------------------------------------------------ maw_snap (24): skull pulled back + jaw gapes 0-7, thrust t9, SNAP t10, shake, recover
a = A("maw_snap", 24)
a.r("chest", (5, 6, 22, 0), (7, 8, 26, 0), (9, -10, -14, 0), (10, -12, -18, 0), (13, -8, -10, 0), (18, 0, -2, 0))
a.r("head", (5, 6, -12, 8), (7, 8, -14, 10), (10, -8, 10, -4), (14, -4, 6, 0), (18, 0, 0, 0))
a.r("arm_r", (5, -20, 0, 30), (7, -26, 0, 34), (9, 70, 0, 4), (10, 80, 0, 0), (13, 66, 0, 6), (18, 20, 0, 2))
a.r("fore_r", (7, 30, 0, 0), (9, -50, 0, 0), (10, -60, 0, 0), (14, -40, 0, 0), (18, -10, 0, 0))
a.r("wmaw", (7, 20, 0, 0), (9, -20, 0, 0), (10, -18, 0, 0), (12, -14, -10, 8), (14, -16, 10, -8), (16, -10, 0, 0))
a.r("wjaw", (4, -30, 0, 0), (7, -42, 0, 0), (9, -48, 0, 0), (10, 8, 0, 0), (12, 2, 0, 0), (14, 6, 0, 0))
a.r("arm_l", (7, -10, 0, -12), (10, 20, 0, -18), (16, 8, 0, -8))
a.r("bmaw", (7, 0, 0, 0), (10, 18, 0, 0), (14, -6, 0, 0))
a.p("body", (7, 0, -0.4, 1.0), (9, 0, -0.2, -1.6), (10, 0, -0.3, -2.0), (14, 0, -0.2, -1.4), (20, 0, 0, -0.4))
legs(a, [(7, 10, 0, 0), (10, -24, 0, 0), (14, -18, 0, 0), (20, 0, 0, 0)], [(7, -14, 0, 0), (10, 24, 0, 0), (14, 16, 0, 0), (20, 0, 0, 0)],
     sr=[(7, -10, 0, 0), (10, 0, 0, 0)], sl=[(7, 0, 0, 0), (10, -26, 0, 0), (16, -10, 0, 0)])
a.hair([(0, 0, 0, 0), (7, -6, 0, -6), (10, 14, 0, 10), (14, 6, 0, -4), (20, 0, 0, 0)], delay=1)
a.done()

# ------------------------------------------------------------------ double_chomp (30): white maw bites t9 (twist right), black bag-monster swings up and bites t17
a = A("double_chomp", 30)
a.r("chest", (5, 4, 28, 0), (8, -8, -16, 0), (9, -10, -20, 0), (12, -4, 0, 0), (15, -6, 30, 0), (17, -10, 34, 0), (21, -4, 14, 0), (26, 0, 0, 0))
a.r("head", (5, 4, -16, 6), (9, -6, 14, -6), (12, 0, 0, 0), (17, -6, -18, 8), (22, 0, -6, 0))
a.r("arm_r", (5, -20, 0, 26), (8, 74, 0, 2), (9, 82, 0, 0), (12, 50, 0, 10), (17, 10, 0, 20), (24, 0, 0, 0))
a.r("fore_r", (5, 30, 0, 0), (8, -50, 0, 0), (9, -56, 0, 0), (13, -30, 0, 0), (20, 0, 0, 0))
a.r("wmaw", (9, -24, 0, 0), (13, -10, 0, 0), (18, 0, 0, 0))
chomp(a, "wjaw", [9], -48, 8)
a.r("arm_l", (8, -20, 0, -10), (12, -30, 0, -40), (14, -20, 0, -60), (16, 90, 0, -20), (17, 104, 0, -14), (20, 84, 0, -16), (25, 20, 0, -6))
a.r("fore_l", (12, 20, 0, 0), (16, -10, 0, 0), (17, -14, 0, 0), (22, 0, 0, 0))
a.r("bmaw", (12, 20, 0, 30), (16, -86, 0, 0), (17, -100, 0, 0), (20, -80, 0, 0), (25, -10, 0, 0))
chomp(a, "bjaw", [17], -50, 6)
a.p("body", (5, 0, -0.3, 0.6), (9, 0, -0.3, -1.4), (13, 0, 0, -1.0), (17, 0, -0.4, -2.2), (22, 0, 0, -1.2), (28, 0, 0, 0))
legs(a, [(5, 8, 0, 0), (9, -20, 0, 0), (13, -6, 0, 0), (17, 14, 0, 0), (24, 0, 0, 0)], [(5, -8, 0, 0), (9, 18, 0, 0), (13, 4, 0, 0), (17, -24, 0, 0), (24, 0, 0, 0)],
     sr=[(9, -4, 0, 0), (17, -20, 0, 0), (24, 0, 0, 0)], sl=[(9, -22, 0, 0), (17, -4, 0, 0), (24, 0, 0, 0)])
a.hair([(0, 0, 0, 0), (5, -4, 0, -10), (9, 10, 0, 12), (13, 4, 0, 0), (17, 12, 0, -14), (22, 4, 0, -4), (28, 0, 0, 0)], delay=1)
a.done()

# ------------------------------------------------------------------ bag_swing (34): bag-monster wound back 0-10, full SPIN t10-18 (hit t14), bag dragged round, stumble recover
a = A("bag_swing", 34)
a.r("root", (8, 0, -40, 0), (10, 0, -50, 0), (12, 0, 40, 0), (14, 0, 160, 0), (16, 0, 260, 0), (18, 0, 340, 0), (22, 0, 365, 0), (26, 0, 360, 0), (34, 0, 360, 0))
a.r("chest", (8, 4, -24, 0), (10, 6, -30, 0), (14, -6, 10, 0), (18, -4, 16, 0), (24, 2, 0, 0))
a.r("head", (8, 0, 20, 10), (10, 0, 26, 12), (14, -6, -10, -6), (18, 0, -16, -8), (24, 6, 0, 14), (28, 0, 0, 0))
a.r("arm_l", (6, 10, 0, -40), (10, 14, 0, -60), (12, 6, 0, -90), (14, 0, 0, -96), (18, 4, 0, -88), (22, 20, 0, -40), (28, 4, 0, -8))
a.r("fore_l", (10, 10, 0, 0), (14, -6, 0, 0), (22, 10, 0, 0))
a.r("bmaw", (10, 0, 30, -20), (14, 0, -20, 30), (18, 0, -30, 20), (22, 0, 20, -10), (26, 0, 0, 0))
chomp(a, "bjaw", [14, 18], -44, 4)
a.r("arm_r", (8, -10, 0, 16), (14, -20, 0, 50), (18, -10, 0, 40), (24, 0, 0, 6))
a.r("wjaw", (12, -30, 0, 0), (18, -30, 0, 0), (21, 0, 0, 0))
a.p("body", (8, 0, -1.0, 0), (10, 0, -1.2, 0), (14, 0, -0.4, 0), (18, 0, -0.6, 0), (22, 0, -1.0, 0), (26, 0, 0, 0))
legs(a, [(8, 20, 0, 6), (10, 24, 0, 8), (14, -16, 0, 12), (18, -10, 0, 8), (22, 16, 0, 0), (28, 0, 0, 0)], [(8, -20, 0, -6), (10, -24, 0, -8), (14, 16, 0, -12), (18, 10, 0, -8), (22, -8, 0, 0), (28, 0, 0, 0)],
     sr=[(10, -30, 0, 0), (18, -14, 0, 0), (24, 0, 0, 0)], sl=[(10, -10, 0, 0), (18, -24, 0, 0), (24, 0, 0, 0)])
a.hair([(0, 0, 0, 0), (8, 6, 0, 10), (12, 14, 0, -20), (16, 18, 0, -26), (20, 14, 0, -20), (24, -6, 0, 10), (30, 0, 0, 0)], delay=2)
a.done()

# ------------------------------------------------------------------ tongue_lash (32): bag-monster raised level 0-10, tongue whips out t12-14 (hit), yank t18, reel in to t24
a = A("tongue_lash", 32)
a.r("arm_l", (6, 50, 0, -10), (10, 80, 0, -6), (12, 92, 0, -2), (14, 94, 0, 0), (18, 70, 0, -6), (22, 80, 0, -4), (26, 30, 0, -6))
a.r("fore_l", (10, 10, 0, 0), (14, -6, 0, 0), (18, 30, 0, 0), (22, 0, 0, 0))
a.r("bmaw", (6, -50, 0, 0), (10, -80, 0, 0), (14, -92, 0, 0), (18, -60, 0, 0), (22, -80, 0, 0), (26, -20, 0, 0))
a.r("bjaw", (6, -30, 0, 0), (10, -40, 0, 0), (12, -58, 0, 0), (21, -54, 0, 0), (24, 6, 0, 0), (26, 0, 0, 0))
a.show("tongue", 11.5, 23, grow=2)
a.pos("tongue", (0, 0, 0, 0), (12, 0, 0, 0), (14, 0, 0, -1.0), (18, 0, 0, 0.6), (21, 0, 0, 3.0), (23, 0, 0, 4.0), (32, 0, 0, 0))
a.r("tongue", (12, 0, -10, 0), (14, 6, 8, 0), (16, -4, -4, 0), (18, 10, 0, 0), (21, 4, 0, 0))
a.r("chest", (6, 6, -20, 0), (10, 8, -26, 0), (13, -10, -10, 0), (18, 12, -30, 0), (22, 6, -14, 0), (28, 0, 0, 0))
a.r("head", (10, 2, 20, -10), (13, -6, 18, -6), (18, 10, 10, 8), (24, 0, 0, 0))
a.r("arm_r", (10, -16, 0, 24), (14, -10, 0, 16), (18, -24, 0, 36), (24, 0, 0, 6))
a.r("wjaw", (12, -34, 0, 0), (20, -34, 0, 0), (24, 0, 0, 0))
a.p("body", (10, 0, -0.4, 0.4), (13, 0, -0.4, -1.0), (18, 0, -0.2, 1.4), (22, 0, 0, 0.8), (28, 0, 0, 0))
legs(a, [(10, -10, 0, 0), (13, -18, 0, 0), (18, 10, 0, 0), (24, 0, 0, 0)], [(10, 14, 0, 0), (13, 22, 0, 0), (18, -6, 0, 0), (24, 0, 0, 0)],
     sl=[(10, -16, 0, 0), (13, -20, 0, 0), (18, -6, 0, 0), (24, 0, 0, 0)])
a.hair([(0, 0, 0, 0), (10, -4, 0, 8), (13, 10, 0, -6), (18, -10, 0, 6), (24, 0, 0, 0)], delay=2)
a.done()

# ------------------------------------------------------------------ goo_spit (36): bag-monster hoisted on the shoulder like a cannon, three gulping SPITS t12/18/24
a = A("goo_spit", 36)
a.r("arm_l", (6, 110, 0, -20), (10, 120, 0, -16), (12, 108, 0, -14), (14, 122, 0, -16), (18, 108, 0, -14), (20, 122, 0, -16), (24, 106, 0, -14), (27, 120, 0, -16), (32, 30, 0, -6))
a.r("fore_l", (6, 20, 0, 0), (30, 20, 0, 0))
a.r("bmaw", (6, -130, 0, 0), (10, -140, 0, 0), (12, -150, 0, 0), (14, -138, 0, 0), (18, -150, 0, 0), (20, -138, 0, 0), (24, -152, 0, 0), (27, -138, 0, 0), (32, -20, 0, 0))
a.s("bmaw", (10, 1.0, 1.0, 1.0), (11, 1.2, 1.15, 1.2), (12, 0.9, 1.05, 0.9), (17, 1.2, 1.15, 1.2), (18, 0.9, 1.05, 0.9), (23, 1.25, 1.2, 1.25), (24, 0.9, 1.05, 0.9), (26, 1, 1, 1))
a.r("bjaw", (10, -6, 0, 0), (11, 4, 0, 0), (12, -60, 0, 0), (14, -10, 0, 0), (17, 4, 0, 0), (18, -60, 0, 0), (20, -10, 0, 0), (23, 4, 0, 0), (24, -64, 0, 0), (27, -10, 0, 0))
a.r("chest", (6, 6, -16, -6), (10, 8, -22, -8), (12, 14, -18, -6), (14, 6, -20, -8), (18, 14, -18, -6), (20, 6, -20, -8), (24, 16, -18, -6), (28, 4, -10, -2))
a.r("head", (6, -4, 22, 10), (12, 2, 20, 6), (18, 2, 20, 6), (24, 4, 20, 6), (30, 0, 0, 0))
a.r("arm_r", (6, 20, 0, 10), (12, 30, 0, 6), (24, 30, 0, 6), (30, 0, 0, 0))
a.r("wjaw", (12, -24, 0, 0), (14, 0, 0, 0), (24, -24, 0, 0), (26, 0, 0, 0))
a.p("body", (6, 0, -0.3, 0), (12, 0, -0.3, 0.6), (14, 0, -0.3, 0), (18, 0, -0.3, 0.6), (20, 0, -0.3, 0), (24, 0, -0.3, 0.8), (30, 0, 0, 0))
legs(a, [(6, -14, 0, 4), (30, -14, 0, 4)], [(6, 16, 0, -4), (30, 16, 0, -4)], sl=[(6, -14, 0, 0), (30, -14, 0, 0)])
a.hair([(0, 0, 0, 0), (12, 6, 0, 4), (14, 0, 0, 0), (18, 6, 0, 4), (20, 0, 0, 0), (24, 8, 0, 4), (30, 0, 0, 0)], delay=1)
a.done()

# ------------------------------------------------------------------ tooth_volley (30): skull drawn to the mouth, inhale 0-10 (lean back), spits a fan of teeth t14, recoil
a = A("tooth_volley", 30)
a.r("arm_r", (6, 50, 0, -10), (10, 60, 0, -14), (13, 96, 0, 0), (14, 100, 0, 0), (17, 86, 0, 4), (24, 20, 0, 4))
a.r("fore_r", (10, 30, 0, 0), (14, -10, 0, 0), (18, 0, 0, 0))
a.r("wmaw", (6, -30, 30, 0), (10, -40, 30, 0), (13, -14, 0, 0), (14, -20, 0, 0), (17, 6, 0, 0), (24, 0, 0, 0))
a.s("wmaw", (6, 1.0, 1.0, 1.0), (10, 1.2, 1.15, 1.25), (13, 1.15, 1.1, 1.2), (14, 0.9, 0.95, 0.85), (16, 1.05, 1.0, 1.05), (18, 1, 1, 1))
a.r("wjaw", (6, 4, 0, 0), (10, 6, 0, 0), (13, -30, 0, 0), (14, -64, 0, 0), (18, -40, 0, 0), (22, -10, 0, 0))
a.r("chest", (6, 12, 10, 0), (10, 18, 14, 0), (13, -6, -6, 0), (14, -12, -8, 0), (17, 4, -4, 0), (24, 0, 0, 0))
a.r("head", (6, 14, -10, 0), (10, 20, -14, 0), (14, -10, 0, 0), (17, 6, 0, 0), (22, 0, 0, 0))
a.r("arm_l", (10, -16, 0, -16), (14, 16, 0, -20), (20, 4, 0, -6))
a.r("bjaw", (10, -20, 0, 0), (14, -40, 0, 0), (18, 0, 0, 0))
a.p("body", (10, 0, 0.2, 1.0), (14, 0, -0.3, -0.6), (17, 0, 0, 0.8), (24, 0, 0, 0))
legs(a, [(10, -10, 0, 0), (14, 8, 0, 0), (17, -4, 0, 0), (24, 0, 0, 0)], [(10, 8, 0, 0), (14, -12, 0, 0), (24, 0, 0, 0)])
a.hair([(0, 0, 0, 0), (10, -10, 0, 0), (14, 14, 0, 0), (18, -4, 0, 0), (24, 0, 0, 0)], delay=1)
a.done()

# ------------------------------------------------------------------ lunge_bite (34): deep crouch 0-8, LEAP t9-15 (both maws forward, jaws wide), land + double BITE t17, recover
a = A("lunge_bite", 34)
a.p("root", (6, 0, -2.4, 0.8), (8, 0, -3.0, 1.0), (10, 0, 2.6, -2.0), (13, 0, 4.0, -3.0), (15, 0, 1.6, -3.0), (17, 0, -1.4, -2.4), (19, 0, -0.8, -2.0),
    (24, 0, 0, -0.6), (30, 0, 0, 0))
a.r("root", (8, 14, 0, 0), (10, -20, 0, 0), (13, -30, 0, 0), (16, -8, 0, 0), (17, -16, 0, 0), (20, -10, 0, 0), (26, 0, 0, 0))
a.r("chest", (6, -16, 0, 0), (8, -20, 0, 0), (12, -10, 0, 0), (17, -24, 0, 0), (22, -8, 0, 0), (28, 0, 0, 0))
a.r("head", (6, 26, 0, 0), (8, 30, 0, 0), (12, 22, 0, 0), (17, 10, 0, 0), (24, 0, 0, 0))
a.r("arm_r", (6, -30, 0, 30), (8, -40, 0, 36), (11, 120, 0, 0), (15, 110, 0, 0), (17, 70, 0, 0), (22, 40, 0, 6), (28, 0, 0, 0))
a.r("fore_r", (8, 20, 0, 0), (11, -50, 0, 0), (17, -40, 0, 0), (24, 0, 0, 0))
a.r("wmaw", (11, -40, 0, 0), (17, -10, 0, 0), (24, 0, 0, 0))
a.r("arm_l", (6, -30, 0, -30), (8, -40, 0, -36), (11, 120, 0, 0), (15, 110, 0, 0), (17, 70, 0, 0), (22, 40, 0, -6), (28, 0, 0, 0))
a.r("bmaw", (11, -110, 0, 0), (15, -100, 0, 0), (17, -60, 0, 0), (22, -30, 0, 0), (28, 0, 0, 0))
chomp(a, "wjaw", [17], -55, 8)
chomp(a, "bjaw", [17], -60, 6)
legs(a, [(6, 60, 0, 0), (8, 70, 0, 0), (10, -30, 0, 0), (13, -20, 0, 0), (15, 30, 0, 0), (17, 50, 0, 0), (20, 30, 0, 0), (26, 0, 0, 0)],
     [(6, 60, 0, 0), (8, 70, 0, 0), (10, -40, 0, 0), (13, -10, 0, 0), (15, 40, 0, 0), (17, 40, 0, 0), (20, 20, 0, 0), (26, 0, 0, 0)],
     sr=[(6, -80, 0, 0), (8, -100, 0, 0), (10, -10, 0, 0), (13, -60, 0, 0), (17, -80, 0, 0), (20, -50, 0, 0), (26, 0, 0, 0)])
a.hair([(0, 0, 0, 0), (8, -10, 0, 0), (10, 26, 0, 0), (14, 20, 0, 0), (17, -14, 0, 0), (21, 8, 0, 0), (28, 0, 0, 0)], delay=2)
a.done()

# ------------------------------------------------------------------ ink_puddle (36): bag-monster heaved overhead 0-10, SLAMMED into the floor t14 -> goo puddle with fangs, hold, pull out
a = A("ink_puddle", 36)
a.r("arm_l", (4, -40, 0, -20), (8, 170, 0, -10), (10, 180, 0, -6), (12, 120, 0, -4), (14, 40, 0, -4), (22, 40, 0, -4), (26, 10, 0, -10), (32, 0, 0, 0))
a.r("fore_l", (10, 30, 0, 0), (14, -10, 0, 0), (24, 0, 0, 0))
a.r("bmaw", (10, -20, 0, 0), (14, 30, 0, 0), (16, 20, 0, 0), (24, 0, 0, 0))
a.s("bmaw", (12, 1, 1, 1), (14, 1.3, 0.7, 1.3), (17, 1.0, 1.05, 1.0), (20, 1, 1, 1))
a.r("bjaw", (8, -40, 0, 0), (12, -50, 0, 0), (14, 10, 0, 0), (20, 0, 0, 0))
a.r("chest", (4, 6, 0, 0), (8, 18, 0, 10), (10, 20, 0, 12), (12, -10, 0, 4), (14, -40, 0, -6), (22, -36, 0, -6), (28, -8, 0, 0))
a.r("head", (8, 10, 0, -6), (12, -4, 0, 0), (14, -20, 0, 0), (17, 10, 0, 16), (22, 10, 0, 18), (28, 0, 0, 0))
a.r("arm_r", (8, -20, 0, 30), (14, 20, 0, 40), (22, 16, 0, 36), (28, 0, 0, 0))
a.r("wjaw", (14, -40, 0, 0), (17, 0, 0, 0), (20, -30, 0, 0), (23, 0, 0, 0))
a.p("body", (8, 0, 0.6, 0.4), (12, 0, 0, -0.4), (14, 0, -3.0, -1.0), (22, 0, -2.8, -1.0), (28, 0, -0.4, 0), (32, 0, 0, 0))
legs(a, [(8, -6, 0, 0), (14, 60, 0, 0), (22, 60, 0, 0), (28, 6, 0, 0)], [(8, 6, 0, 0), (14, 20, 0, 0), (22, 20, 0, 0), (28, 0, 0, 0)],
     sr=[(14, -90, 0, 0), (22, -90, 0, 0), (28, -10, 0, 0)], sl=[(14, -40, 0, 0), (22, -40, 0, 0), (28, 0, 0, 0)])
a.scl("puddle", (0, *HIDE), (13.5, *HIDE), (14, 0.3, 1, 0.3), (16, 1.2, 1.5, 1.2), (18, 1, 1, 1), (30, 1, 1, 1), (32, 0.4, 0.4, 0.4), (32.5, *HIDE), (36, *HIDE))
a.hair([(0, 0, 0, 0), (8, 10, 0, 0), (12, -10, 0, 0), (14, -18, 0, 0), (17, 10, 0, 8), (22, 4, 0, 6), (28, 0, 0, 0)], delay=2)
a.done()

# ------------------------------------------------------------------ grin_scream (32): head rolls back 0-8, grin stretches, SCREAM t12-22 (head + shawl + maws all flare), sag
a = A("grin_scream", 32)
a.r("chest", (4, 10, 0, 0), (8, 22, 0, 0), (11, -10, 0, 0), (12, -16, 0, 0), (16, -14, 0, 0), (22, -12, 0, 0), (26, 0, 0, 0))
a.r("head", (4, 24, 0, 10), (8, 40, 0, 14), (11, -10, 0, -2), (12, -18, 0, 0), (14, -16, -6, 4), (16, -18, 6, -4), (18, -16, -6, 4), (20, -18, 6, -4), (22, -14, 0, 0), (26, 6, 0, 18), (30, 0, 0, 0))
a.s("head", (8, 1.0, 1.0, 1.0), (11, 1.12, 1.1, 1.12), (12, 1.18, 1.14, 1.18), (22, 1.16, 1.12, 1.16), (26, 1, 1, 1))
sym_r = [(4, -20, 0, 30), (8, -30, 0, 40), (12, -10, 0, 70), (22, -10, 0, 66), (26, 0, 0, 10)]
a.r("arm_r", *sym_r)
a.r("arm_l", *[(t, x, -y, -z) for (t, x, y, z) in sym_r])
a.r("wjaw", (10, -20, 0, 0), (12, -60, 0, 0), (22, -60, 0, 0), (25, 0, 0, 0))
a.r("bjaw", (10, -20, 0, 0), (12, -64, 0, 0), (22, -64, 0, 0), (25, 0, 0, 0))
a.r("wmaw", (12, 30, -30, 0), (22, 30, -30, 0), (26, 0, 0, 0))
a.r("bmaw", (12, -20, 30, 0), (22, -20, 30, 0), (26, 0, 0, 0))
a.s("shawl", (8, 1, 1, 1), (12, 1.25, 1.1, 1.25), (14, 1.15, 1.05, 1.15), (16, 1.25, 1.1, 1.25), (18, 1.15, 1.05, 1.15), (20, 1.25, 1.1, 1.25), (22, 1.2, 1.1, 1.2), (26, 1, 1, 1))
a.r("spk_r", (8, 0, 0, -10), (12, 0, 0, 30), (22, 0, 0, 28), (26, 0, 0, 0))
a.r("spk_l", (8, 0, 0, 10), (12, 0, 0, -30), (22, 0, 0, -28), (26, 0, 0, 0))
a.p("body", (8, 0, 0.4, 0.6), (12, 0, -0.6, -0.6), (22, 0, -0.6, -0.6), (28, 0, 0, 0))
legs(a, [(8, -6, 0, 4), (12, 10, 0, 14), (22, 10, 0, 14), (28, 0, 0, 0)], sr=[(12, -16, 0, 0), (22, -16, 0, 0), (28, 0, 0, 0)])
a.r("hair_b", (8, -20, 0, 0), (12, 40, 0, 0), (14, 34, 0, 4), (16, 42, 0, -4), (18, 34, 0, 4), (20, 42, 0, -4), (22, 36, 0, 0), (28, 0, 0, 0))
a.r("lock_r", (12, 20, 0, 40), (16, 24, 0, 34), (20, 20, 0, 42), (24, 0, 0, 0))
a.r("lock_l", (12, 20, 0, -40), (16, 24, 0, -34), (20, 20, 0, -42), (24, 0, 0, 0))
a.r("bangs", (12, -20, 0, 0), (22, -20, 0, 0), (26, 0, 0, 0))
a.r("ahoge", (8, -30, 0, 0), (12, 40, 0, 20), (16, 30, 0, -20), (20, 40, 0, 20), (24, -10, 0, 0), (28, 0, 0, 0))
a.done()

# ------------------------------------------------------------------ maw_trap (34): bag-monster flung out on its tongue t12 (grabs target), held 12-20, YANKED back t22, catch
a = A("maw_trap", 34)
a.r("arm_l", (4, -40, 0, -30), (8, -60, 0, -40), (11, 100, 0, -6), (12, 104, 0, 0), (20, 96, 0, -2), (22, 60, 0, -10), (24, 30, 0, -8), (30, 0, 0, 0))
a.r("fore_l", (8, 30, 0, 0), (12, -6, 0, 0), (22, 40, 0, 0), (26, 0, 0, 0))
a.r("bmaw", (8, 30, 0, 0), (11, -96, 0, 0), (12, -100, 0, 0), (20, -96, 0, 0), (22, -60, 0, 0), (26, 0, 0, 0))
a.p("bmaw", (8, 0, 0, 0), (11, 0, -10, 0), (12, 0, -18, 0), (14, 0, -20, 0), (20, 0, -20, 0), (22, 0, -6, 0), (24, 0, 0, 0))
a.r("bjaw", (8, -30, 0, 0), (11, -60, 0, 0), (12, 8, 0, 0), (20, 6, 0, 0), (23, -20, 0, 0), (25, 0, 0, 0))
a.s("bmaw", (10, 1, 1, 1), (12, 1.3, 1.3, 1.3), (14, 1.2, 1.2, 1.2), (20, 1.2, 1.2, 1.2), (23, 1, 1, 1))
a.show("tongue", 10.5, 22, grow=1)
a.p("tongue", (10, 0, 0, 0), (12, 0, 0, 6), (20, 0, 0, 6), (22, 0, 0, 2))
a.r("chest", (4, 6, -20, 0), (8, 10, -30, 0), (11, -10, -6, 0), (12, -14, 0, 0), (20, -12, 0, 0), (22, 20, -24, 0), (24, 10, -14, 0), (30, 0, 0, 0))
a.r("head", (8, 4, 22, -10), (12, -10, 6, 0), (16, -8, 2, 12), (20, -10, 6, -8), (22, 12, 16, 10), (28, 0, 0, 0))
a.r("arm_r", (8, -10, 0, 20), (12, -30, 0, 34), (22, -6, 0, 16), (28, 0, 0, 0))
a.r("wjaw", (12, -36, 0, 0), (20, -36, 0, 0), (24, 0, 0, 0))
a.p("body", (8, 0, -0.3, 0.6), (12, 0, -0.6, -1.4), (20, 0, -0.6, -1.4), (22, 0, -0.2, 1.4), (26, 0, 0, 0.6), (30, 0, 0, 0))
legs(a, [(8, 10, 0, 0), (12, -20, 0, 0), (20, -20, 0, 0), (22, 14, 0, 0), (28, 0, 0, 0)], [(8, -10, 0, 0), (12, 26, 0, 0), (20, 26, 0, 0), (22, -14, 0, 0), (28, 0, 0, 0)],
     sl=[(12, -30, 0, 0), (20, -30, 0, 0), (24, 0, 0, 0)])
a.hair([(0, 0, 0, 0), (8, -6, 0, 6), (12, 10, 0, -6), (20, 6, 0, 0), (22, -16, 0, 8), (26, 6, 0, 0), (30, 0, 0, 0)], delay=2)
a.done()

# ------------------------------------------------------------------ devour (46, enraged): both maws SWELL 0-10, lunge t10, three crushing chomps t16/24/32 alternating, gulp, recover
a = A("devour", 46)
for b in ("wmaw", "bmaw"):
    a.s(b, (4, 1.3, 1.3, 1.3), (8, 1.7, 1.7, 1.7), (10, 1.8, 1.8, 1.8), (34, 1.8, 1.8, 1.8), (38, 1.3, 1.3, 1.3), (42, 1, 1, 1))
a.p("root", (8, 0, -1.0, 0.6), (10, 0, 1.6, -2.4), (13, 0, 0, -3.0), (34, 0, 0, -2.4), (40, 0, 0, 0))
a.r("arm_r", (6, -30, 0, 30), (10, 80, 0, 10), (14, 70, 0, 20), (16, 90, 0, 0), (20, 70, 0, 20), (24, 60, 0, 30), (30, 70, 0, 20), (32, 92, 0, 0), (36, 60, 0, 10), (42, 0, 0, 0))
a.r("fore_r", (10, -40, 0, 0), (32, -40, 0, 0), (40, 0, 0, 0))
a.r("wmaw", (10, -30, 0, 0), (16, -20, 0, -20), (24, -30, 0, 0), (32, -20, 0, -20), (38, 0, 0, 0))
a.r("arm_l", (6, -30, 0, -30), (10, 100, 0, -6), (14, 80, 0, -20), (20, 90, 0, -6), (24, 110, 0, 0), (28, 80, 0, -20), (32, 90, 0, -10), (36, 60, 0, -10), (42, 0, 0, 0))
a.r("bmaw", (10, -100, 0, 0), (24, -110, 0, 20), (32, -100, 0, 0), (38, -40, 0, 0))
chomp(a, "wjaw", [16, 32], -60, 8)
chomp(a, "bjaw", [24, 32], -64, 6)
a.r("chest", (6, 10, 0, 0), (10, -20, 0, 0), (16, -26, 20, 0), (24, -26, -20, 0), (32, -30, 0, 0), (36, -10, 0, 0), (42, 0, 0, 0))
a.r("head", (6, 20, 0, 0), (10, 10, 0, 0), (16, 0, -14, 10), (24, 0, 14, -10), (32, -4, 0, 0), (36, 20, 0, 0), (38, 10, 0, 0), (44, 0, 0, 0))
a.p("body", (6, 0, -1.2, 0), (10, 0, 0, -1.0), (16, 0, -0.6, -1.4), (24, 0, -0.6, -1.4), (32, 0, -1.0, -1.8), (38, 0, 0, 0))
legs(a, [(6, 40, 0, 0), (10, -30, 0, 0), (16, -20, 0, 0), (32, -24, 0, 0), (40, 0, 0, 0)], [(6, 40, 0, 0), (10, 30, 0, 0), (16, 24, 0, 0), (32, 28, 0, 0), (40, 0, 0, 0)],
     sr=[(6, -60, 0, 0), (10, -10, 0, 0), (40, 0, 0, 0)], sl=[(6, -60, 0, 0), (10, -30, 0, 0), (32, -30, 0, 0), (40, 0, 0, 0)])
a.hair([(0, 0, 0, 0), (6, -8, 0, 0), (10, 16, 0, 0), (16, 8, 0, -12), (24, 8, 0, 12), (32, 14, 0, 0), (36, -8, 0, 0), (42, 0, 0, 0)], delay=2)
a.done()

# ------------------------------------------------------------------ mutation_burst (44, enraged): hunched, trembling 0-14 as goo swells, ERUPTS t18 (inner spikes) + t26 (outer ring), sag
a = A("mutation_burst", 44)
a.r("chest", (4, -20, 0, 0), (8, -26, 0, 4), (10, -26, 0, -4), (12, -28, 0, 4), (14, -30, 0, -4), (16, -10, 0, 0), (18, 24, 0, 0), (22, 20, 0, 0), (26, 28, 0, 0), (32, 10, 0, 0), (38, 0, 0, 0))
a.r("head", (4, -24, 0, 0), (14, -30, 0, 0), (18, 34, 0, 0), (22, 26, 6, 10), (26, 36, 0, 0), (32, 10, 0, -10), (38, 0, 0, 0))
sym_r = [(4, 20, 0, 10), (14, 40, 0, -10), (18, -20, 0, 100), (22, -10, 0, 90), (26, -20, 0, 110), (32, 0, 0, 40), (38, 0, 0, 0)]
a.r("arm_r", *sym_r)
a.r("arm_l", *[(t, x, -y, -z) for (t, x, y, z) in sym_r])
a.s("bmaw", (4, 1.1, 1.1, 1.1), (14, 1.4, 1.4, 1.4), (18, 1.7, 1.7, 1.7), (26, 1.8, 1.8, 1.8), (32, 1.2, 1.2, 1.2), (38, 1, 1, 1))
a.r("bjaw", (14, -10, 0, 0), (18, -70, 0, 0), (30, -70, 0, 0), (34, 0, 0, 0))
a.r("wjaw", (14, 0, 0, 0), (18, -60, 0, 0), (30, -60, 0, 0), (34, 0, 0, 0))
a.s("arm_l", (6, 1.1, 1.0, 1.1), (14, 1.3, 1.05, 1.3), (18, 1.4, 1.1, 1.4), (30, 1.3, 1.05, 1.3), (38, 1, 1, 1))
a.s("leg_l", (6, 1.1, 1.0, 1.1), (14, 1.25, 1.0, 1.25), (30, 1.2, 1.0, 1.2), (38, 1, 1, 1))
a.p("body", (4, 0, -1.4, 0), (14, 0, -2.0, 0), (18, 0, 1.0, 0), (22, 0, 0.4, 0), (26, 0, 1.2, 0), (32, 0, 0, 0))
legs(a, [(4, 30, 0, 0), (14, 40, 0, 0), (18, 0, 0, 14), (26, 0, 0, 16), (32, 0, 0, 0)], sr=[(4, -50, 0, 0), (14, -70, 0, 0), (18, 0, 0, 0)])
a.scl("goospk", (0, *HIDE), (17.5, *HIDE), (18, 0.4, 0.3, 0.4), (20, 0.5, 1.3, 0.5), (22, 0.5, 0.8, 0.5), (25.5, 0.55, 0.7, 0.55), (26, 1.0, 0.5, 1.0), (28, 1.0, 1.4, 1.0),
      (32, 1.0, 1.0, 1.0), (36, 1.0, 0.2, 1.0), (36.5, *HIDE), (44, *HIDE))
a.rot("goospk", (0, 0, 0, 0), (18, 0, 0, 0), (26, 0, 22, 0), (36, 0, 30, 0), (44, 0, 30, 0))
a.hair([(0, 0, 0, 0), (4, -8, 0, 0), (8, -6, 0, 6), (12, -6, 0, -6), (14, -10, 0, 0), (18, 30, 0, 0), (22, 20, 0, 10), (26, 34, 0, -8), (32, 10, 0, 0), (38, 0, 0, 0)], delay=1)
a.done()

# ------------------------------------------------------------------ puppet_feint (28): grin wide, skull "talks" (clack clack), then a sudden sideways hop-dodge t14 + snap t18
a = A("puppet_feint", 28)
a.r("arm_r", (4, 40, 0, -10), (12, 50, 0, -14), (14, 30, 0, 10), (18, 80, 0, 0), (24, 10, 0, 0))
a.r("wmaw", (4, 0, 40, 0), (8, 6, 50, 6), (12, 0, 40, -6), (14, 0, 0, 0), (18, -20, 0, 0), (24, 0, 0, 0))
a.r("wjaw", (4, -20, 0, 0), (5, 0, 0, 0), (6, -24, 0, 0), (7, 0, 0, 0), (8, -20, 0, 0), (9, 0, 0, 0), (10, -26, 0, 0), (11, 0, 0, 0), (16, -50, 0, 0), (18, 8, 0, 0), (21, 0, 0, 0))
a.r("head", (4, 0, 20, -20), (12, 0, 20, -24), (14, 0, -10, 10), (18, -8, 0, 0), (24, 0, 0, 0))
a.r("chest", (4, 0, 10, -6), (12, 0, 12, -8), (14, 0, 0, 14), (18, -10, 0, 4), (24, 0, 0, 0))
a.p("root", (12, 0, 0, 0), (13, 0, 1.2, 0), (14, 2.0, 2.6, 0), (16, 2.4, 0, -1.0), (18, 1.6, -0.4, -2.0), (22, 0.4, 0, -0.6), (26, 0, 0, 0))
a.r("root", (13, 0, 0, 0), (14, 0, 0, 18), (16, 0, 0, -6), (18, 0, 0, 0))
a.r("arm_l", (12, 0, 0, 0), (14, -20, 0, -50), (18, 10, 0, -20), (24, 0, 0, 0))
legs(a, [(12, 0, 0, 0), (13, 20, 0, 20), (14, 0, 0, 30), (16, 10, 0, 10), (18, -10, 0, 0), (24, 0, 0, 0)],
     [(12, 0, 0, 0), (13, 20, 0, 10), (14, 0, 0, 30), (16, 20, 0, 6), (18, 10, 0, 0), (24, 0, 0, 0)],
     sr=[(13, -40, 0, 0), (15, -10, 0, 0), (17, -30, 0, 0), (20, 0, 0, 0)])
a.hair([(0, 0, 0, 0), (4, 0, 0, -8), (12, 0, 0, -10), (14, 10, 0, -30), (17, -4, 0, 10), (22, 0, 0, 0)], delay=2)
a.done()

# ------------------------------------------------------------------ bag_swallow (56, GRAB): crouch + bag gapes 0-8, lunge t9, SNAP shut t10 (swollen bag
# swallows the victim), hoisted in front 11-16, CHEWS t20/t28/t36 (bag squashes, skull cheers), heaves back 40-43, SPITS t44, recover
a = A("bag_swallow", 56)
CH = (20, 28, 36)
a.r("arm_l", (4, -40, 0, -30), (8, -56, 0, -36), (9, 70, 0, -8), (10, 92, 0, -2), (13, 110, 0, -4), (16, 124, 0, -6),
    *[(t + d, 124 + o, 0, -6) for t in CH for (d, o) in ((-3, 6), (0, -12), (2, 0))],
    (40, 140, 0, -6), (43, 168, 0, -4), (44, 70, 0, -2), (46, 52, 0, -4), (50, 30, 0, -6))
a.r("fore_l", (8, 30, 0, 0), (10, -10, 0, 0), (16, 10, 0, 0), (40, 10, 0, 0), (43, 30, 0, 0), (44, -20, 0, 0), (50, 0, 0, 0))
a.r("bmaw", (4, 20, 0, 0), (8, 30, 0, 0), (9, -80, 0, 0), (10, -92, 0, 0), (16, -150, 0, 0), *[(t, -150, 0, 6 if i % 2 else -6) for i, t in enumerate(CH)],
    (40, -150, 0, 0), (43, -170, 0, 0), (44, -80, 0, 0), (48, -50, 0, 0), (52, -10, 0, 0))
a.s("bmaw", (4, 1.2, 1.2, 1.2), (8, 1.45, 1.45, 1.45), (9, 1.8, 1.8, 1.8), (10, 2.2, 2.0, 2.2), (12, 2.4, 2.2, 2.4), (16, 2.3, 2.2, 2.3),
    *[(t + d, *sc) for t in CH for (d, sc) in ((-2, (2.15, 2.5, 2.15)), (0, (2.6, 1.8, 2.6)), (2, (2.3, 2.2, 2.3)))],
    (40, 2.3, 2.2, 2.3), (43, 2.5, 2.4, 2.5), (44, 1.9, 2.3, 1.6), (46, 1.2, 1.2, 1.2), (49, 0.9, 1.05, 0.9), (52, 1, 1, 1))
a.r("bjaw", (4, -30, 0, 0), (8, -56, 0, 0), (9, -70, 0, 0), (10, 8, 0, 0), *[(t + d, x, 0, 0) for t in CH for (d, x) in ((-3, -26), (0, 8), (2, 0))],
    (42, 4, 0, 0), (44, -76, 0, 0), (47, -40, 0, 0), (50, 0, 0, 0))
a.r("chest", (4, -10, -20, 0), (8, -14, -26, 0), (9, -16, 10, 0), (10, -18, 14, 0), (16, 10, 6, 0),
    *[(t + d, x, 6, 0) for t in CH for (d, x) in ((-3, 14), (0, 4), (2, 10))], (40, 16, 4, 0), (43, 24, 0, 0), (44, -18, 10, 0), (48, -8, 4, 0), (54, 0, 0, 0))
a.r("head", (4, 10, 20, -6), (8, 14, 24, -10), (10, -6, -10, 4), (16, 10, -10, 14), (22, 8, -8, -16), (30, 8, -8, 16), (38, 8, -8, -14),
    (43, 16, 0, 0), (44, -12, 0, 0), (48, 6, 0, 10), (54, 0, 0, 0))
a.r("arm_r", (8, -20, 0, 26), (10, 20, 0, 14), (16, 30, 0, -10), *[(t + d, 40 + o, 0, -10) for t in CH for (d, o) in ((-2, -20), (0, 20), (2, 0))],
    (43, -30, 0, 30), (44, 20, 0, 20), (50, 0, 0, 0))
a.r("wmaw", (16, 0, 40, 0), *[(t, -20, 40, 0) for t in CH], (40, 0, 0, 0))
chomp(a, "wjaw", [21, 29, 37], -40, 6)
a.p("body", (4, 0, -1.6, 0.8), (8, 0, -2.2, 1.0), (9, 0, -0.6, -1.4), (10, 0, -0.8, -2.0), (16, 0, 0, -0.8),
    *[(t + d, 0, y, -0.8) for t in CH for (d, y) in ((-2, 0.4), (0, -0.6), (2, 0))], (43, 0, 0.2, 0.6), (44, 0, -0.8, -1.4), (48, 0, -0.2, -0.6), (54, 0, 0, 0))
legs(a, [(4, 40, 0, 0), (8, 50, 0, 0), (10, -26, 0, 0), (16, -14, 0, 4), (40, -14, 0, 4), (44, -30, 0, 0), (50, 0, 0, 0)],
     [(4, 30, 0, 0), (8, 40, 0, 0), (10, 26, 0, 0), (16, 16, 0, -4), (40, 16, 0, -4), (44, 24, 0, 0), (50, 0, 0, 0)],
     sr=[(4, -60, 0, 0), (8, -80, 0, 0), (10, -6, 0, 0), (16, -14, 0, 0), (44, -6, 0, 0), (50, 0, 0, 0)],
     sl=[(4, -50, 0, 0), (8, -66, 0, 0), (10, -30, 0, 0), (16, -20, 0, 0), (44, -32, 0, 0), (50, 0, 0, 0)])
a.hair([(0, 0, 0, 0), (8, -10, 0, 6), (10, 18, 0, -6), (16, 6, 0, 0), *[(t, 10, 0, 6 if i % 2 else -6) for i, t in enumerate(CH)],
        (43, -10, 0, 0), (44, 20, 0, 0), (50, 4, 0, 0), (54, 0, 0, 0)], delay=2)
a.done()

# ------------------------------------------------------------------ tongue_reel (46, PULL+HOLD): bag levelled 0-10, tongue SHOOTS t12 (long), reeled in
# 13-21 (she heaves back), wrapped victim held at the bag 21-33 while the skull BITES t26/t32, hoisted 34-37, SLAMMED down t38, recover
a = A("tongue_reel", 46)
a.r("arm_l", (6, 60, 0, -14), (10, 84, 0, -8), (12, 96, 0, 0), (14, 92, 0, 0), (17, 70, 0, -10), (21, 56, 0, -12), (26, 60, 0, -10), (33, 60, 0, -10),
    (36, 150, 0, -6), (37, 160, 0, -4), (38, 30, 0, -4), (40, 20, 0, -6), (44, 0, 0, 0))
a.r("fore_l", (10, 10, 0, 0), (12, -6, 0, 0), (17, 30, 0, 0), (21, 40, 0, 0), (33, 40, 0, 0), (37, 10, 0, 0), (38, -10, 0, 0), (42, 0, 0, 0))
a.r("bmaw", (6, -60, 0, 0), (10, -94, 0, 0), (12, -92, 0, 0), (17, -102, 0, 0), (21, -100, 0, 0), (33, -100, 0, 0), (37, -164, 0, 0), (38, 10, 0, 0),
    (40, 20, 0, 0), (44, 0, 0, 0))
a.s("bmaw", (10, 1, 1, 1), (12, 1.15, 1.15, 1.15), (21, 1.25, 1.25, 1.25), (33, 1.25, 1.25, 1.25), (37, 1.35, 1.35, 1.35), (38, 1.5, 0.9, 1.5),
    (40, 1.1, 1.05, 1.1), (43, 1, 1, 1))
a.r("bjaw", (6, -30, 0, 0), (10, -46, 0, 0), (12, -64, 0, 0), (21, -50, 0, 0), (23, -20, 0, 0), (33, -20, 0, 0), (38, -50, 0, 0), (41, 0, 0, 0))
# tongue: shoots out long at t12 (z-scale from its root), reeled in 13-21, stays short + coiled while holding, retracts at the slam
a.scl("tongue", (0, *HIDE), (11.5, *HIDE), (12, 1.2, 1.2, 4.5), (13, 1.1, 1.1, 5.2), (15, 1.2, 1.2, 4.0), (18, 1.3, 1.3, 2.4), (21, 1.4, 1.4, 1.0),
      (33, 1.4, 1.4, 1.0), (37, 1.4, 1.4, 1.2), (38, 1.2, 1.2, 0.6), (39, 0.4, 0.4, 0.3), (39.5, *HIDE), (46, *HIDE))
a.rot("tongue", (0, 0, 0, 0), (12, 2, -4, 0), (13, -2, 4, 0), (15, 4, -2, 0), (18, -4, 0, 0), (21, -10, 0, 0), (26, -8, 0, 6), (32, -8, 0, -6),
      (37, 10, 0, 0), (38, 0, 0, 0), (46, 0, 0, 0))
a.r("chest", (6, 6, -20, 0), (10, 8, -26, 0), (12, -12, -10, 0), (14, -14, -6, 0), (17, 14, -24, 0), (21, 18, -20, 0), (24, 6, -10, 0),
    (26, -8, 10, 0), (28, 4, 0, 0), (32, -8, 10, 0), (34, 4, 0, 0), (37, 22, -6, 0), (38, -24, 0, 0), (41, -14, 0, 0), (45, 0, 0, 0))
a.r("head", (10, 2, 20, -10), (12, -6, 18, -6), (17, 12, 10, 8), (21, 4, 0, -12), (26, -6, 6, 6), (32, -6, 6, -6), (37, 16, 0, 0), (38, -16, 0, 0),
    (42, 6, 0, 14), (46, 0, 0, 0))
a.r("arm_r", (10, -16, 0, 24), (17, -24, 0, 36), (23, -30, 0, 30), (26, 76, 0, 10), (29, 30, 0, 20), (32, 80, 0, 10), (35, -20, 0, 30), (38, 10, 0, 30),
    (44, 0, 0, 0))
a.r("fore_r", (23, 30, 0, 0), (26, -40, 0, 0), (29, 0, 0, 0), (32, -44, 0, 0), (36, 0, 0, 0))
a.r("wmaw", (23, 20, 0, 0), (26, -24, 0, 0), (29, 0, 0, 0), (32, -24, 0, 0), (36, 0, 0, 0))
chomp(a, "wjaw", [26, 32], -50, 8)
a.p("body", (10, 0, -0.4, 0.4), (12, 0, -0.4, -1.0), (14, 0, -0.5, -1.2), (17, 0, -0.6, 1.2), (21, 0, -0.4, 1.4), (26, 0, -0.2, 0), (33, 0, 0, 0),
    (37, 0, 0.6, 0.4), (38, 0, -1.6, -0.8), (41, 0, -0.8, -0.4), (45, 0, 0, 0))
legs(a, [(10, -10, 0, 0), (12, -20, 0, 0), (17, 14, 0, 0), (21, 18, 0, 0), (26, 0, 0, 0), (37, 0, 0, 0), (38, -24, 0, 0), (44, 0, 0, 0)],
     [(10, 14, 0, 0), (12, 24, 0, 0), (17, -14, 0, 0), (21, -10, 0, 0), (26, 0, 0, 0), (37, 0, 0, 0), (38, 30, 0, 0), (44, 0, 0, 0)],
     sr=[(12, -6, 0, 0), (17, -24, 0, 0), (21, -20, 0, 0), (26, 0, 0, 0), (38, -10, 0, 0), (44, 0, 0, 0)],
     sl=[(12, -24, 0, 0), (17, -4, 0, 0), (26, 0, 0, 0), (38, -40, 0, 0), (44, 0, 0, 0)])
a.hair([(0, 0, 0, 0), (10, -4, 0, 8), (12, 10, 0, -6), (17, -12, 0, 6), (21, -8, 0, 0), (26, 6, 0, -4), (32, 6, 0, 4), (37, -12, 0, 0), (38, 20, 0, 0),
        (42, 4, 0, 0), (46, 0, 0, 0)], delay=2)
a.done()

# ------------------------------------------------------------------ goo_pin (44, PIN): bag hoisted overhead 0-9 (swells), hop t10, SLAM t13 - bag pins the
# victim in a goo puddle; leans on it 13-33, skull pecks t20/t26, goo rips the weapon away t23 (bag tugs), springs off backward t34, recover
a = A("goo_pin", 44)
a.r("arm_l", (4, 60, 0, -14), (8, 168, 0, -8), (10, 180, 0, -4), (12, 120, 0, -2), (13, 26, 0, 0), (16, 22, 0, 0), (22, 20, 0, 0), (23, 40, 0, -6),
    (25, 22, 0, 0), (33, 22, 0, 0), (34, 80, 0, -10), (37, 30, 0, -12), (42, 0, 0, 0))
a.r("fore_l", (8, 20, 0, 0), (12, -10, 0, 0), (13, 10, 0, 0), (33, 10, 0, 0), (36, 30, 0, 0), (42, 0, 0, 0))
a.r("bmaw", (4, -30, 0, 0), (8, -10, 0, 0), (10, -20, 0, 0), (13, 20, 0, 0), *[(t, 20, 0, z) for t, z in ((17, 4), (21, -4), (25, 4), (29, -4), (33, 0))],
    (23, 34, 0, 0), (34, -20, 0, 0), (38, -10, 0, 0), (42, 0, 0, 0))
a.s("bmaw", (4, 1.2, 1.2, 1.2), (8, 1.5, 1.5, 1.5), (12, 1.7, 1.6, 1.7), (13, 2.3, 1.2, 2.3), (15, 2.0, 1.5, 2.0),
    *[(t, *sc) for t, sc in ((18, (2.1, 1.4, 2.1)), (21, (2.0, 1.55, 2.0)), (24, (2.15, 1.35, 2.15)), (27, (2.0, 1.55, 2.0)), (30, (2.1, 1.4, 2.1)))],
    (33, 2.0, 1.5, 2.0), (35, 1.3, 1.3, 1.3), (38, 0.95, 1.05, 0.95), (41, 1, 1, 1))
a.r("bjaw", (4, -30, 0, 0), (8, -50, 0, 0), (12, -64, 0, 0), (13, -14, 0, 0), (22, -14, 0, 0), (23, -50, 0, 0), (24, 6, 0, 0), (33, -10, 0, 0), (36, 0, 0, 0))
a.r("chest", (4, 8, 0, 0), (8, 18, 0, 8), (10, 20, 0, 10), (12, -6, 0, 4), (13, -42, 0, -4), (16, -38, 0, -4), (20, -44, 0, 0), (26, -44, 0, 0),
    (30, -38, 0, -4), (33, -38, 0, -4), (34, 10, 0, 0), (37, 6, 0, 0), (42, 0, 0, 0))
a.r("head", (8, 14, 0, -6), (12, -6, 0, 0), (13, -14, 0, 0), (16, 20, 0, 18), (20, 24, -8, -14), (23, 28, 0, 20), (26, 24, 8, -14), (30, 22, 0, 18),
    (34, -8, 0, 0), (38, 6, 0, -8), (42, 0, 0, 0))
a.r("arm_r", (8, -20, 0, 30), (12, -40, 0, 34), (13, 20, 0, 20), (17, 10, 0, 10), (20, 70, 0, -4), (22, 20, 0, 6), (26, 74, 0, -4), (28, 20, 0, 6),
    (33, 20, 0, 10), (34, -30, 0, 30), (38, -10, 0, 10), (42, 0, 0, 0))
a.r("fore_r", (17, 20, 0, 0), (20, -40, 0, 0), (22, 10, 0, 0), (26, -40, 0, 0), (28, 10, 0, 0), (33, 0, 0, 0))
a.r("wmaw", (17, 20, 0, 0), (20, 30, 0, 0), (26, 30, 0, 0), (30, 0, 0, 0))
chomp(a, "wjaw", [20, 26], -50, 6)
a.p("root", (8, 0, -1.2, 0.4), (9, 0, -1.4, 0.4), (10, 0, 2.0, -1.0), (11, 0, 3.6, -2.4), (12, 0, 2.6, -3.4), (13, 0, -0.8, -4.0), (16, 0, -1.2, -4.0),
    (33, 0, -1.2, -4.0), (34, 0, 2.4, -1.2), (36, 0, 0.6, 0.6), (37, 0, -0.6, 0.4), (40, 0, 0, 0))
a.r("root", (10, -10, 0, 0), (12, -14, 0, 0), (13, -6, 0, 0), (16, 0, 0, 0), (34, 14, 0, 0), (37, 4, 0, 0), (40, 0, 0, 0))
legs(a, [(8, 40, 0, 0), (9, 46, 0, 0), (10, -20, 0, 0), (12, 30, 0, 0), (13, 40, 0, 6), (33, 40, 0, 6), (34, -30, 0, 0), (37, 20, 0, 0), (41, 0, 0, 0)],
     [(8, 40, 0, 0), (9, 46, 0, 0), (10, -30, 0, 0), (12, 10, 0, 0), (13, -10, 0, -6), (33, -10, 0, -6), (34, -20, 0, 0), (37, 30, 0, 0), (41, 0, 0, 0)],
     sr=[(8, -70, 0, 0), (9, -80, 0, 0), (10, -10, 0, 0), (12, -50, 0, 0), (13, -60, 0, 0), (33, -60, 0, 0), (34, -20, 0, 0), (37, -40, 0, 0), (41, 0, 0, 0)],
     sl=[(8, -70, 0, 0), (9, -80, 0, 0), (10, -10, 0, 0), (12, -30, 0, 0), (13, -14, 0, 0), (33, -14, 0, 0), (34, -40, 0, 0), (37, -30, 0, 0), (41, 0, 0, 0)])
a.scl("puddle", (0, *HIDE), (12.5, *HIDE), (13, 0.4, 1, 0.4), (15, 1.3, 1.6, 1.3), (17, 1.1, 1, 1.1), (33, 1.1, 1, 1.1), (35, 0.5, 0.5, 0.5), (35.5, *HIDE), (44, *HIDE))
a.hair([(0, 0, 0, 0), (8, 10, 0, 0), (10, -14, 0, 0), (12, -20, 0, 0), (13, 24, 0, 0), (16, 8, 0, 6), (23, 10, 0, -8), (30, 6, 0, 6), (34, -18, 0, 0),
        (37, 12, 0, 0), (42, 0, 0, 0)], delay=2)
a.done()

# ------------------------------------------------------------------ death (40): goo convulses, skull jaw falls slack, knees buckle t10-18, topples forward t18-30, bag-monster slumps away
a = A("death", 40)
a.r("chest", (4, -16, 0, 10), (8, 10, 0, -14), (12, -20, 0, 6), (18, -30, 0, 0), (40, -20, 0, 0))
a.r("head", (4, 20, 0, 18), (8, -10, 0, -20), (12, 10, 0, 30), (18, -20, 0, 20), (26, -10, 0, 30), (40, -10, 0, 34))
a.r("arm_r", (4, -10, 0, 40), (8, 40, 0, 10), (14, 10, 0, 20), (20, 150, 0, 20), (40, 160, 0, 26))
a.r("arm_l", (4, -10, 0, -40), (8, 40, 0, -10), (14, 10, 0, -20), (20, 150, 0, -20), (40, 160, 0, -20))
a.r("wjaw", (4, -50, 0, 0), (8, -10, 0, 0), (14, -40, 0, 0), (40, -44, 0, 0))
a.r("bjaw", (4, -40, 0, 0), (8, -60, 0, 0), (14, -30, 0, 0), (40, -30, 0, 0))
a.s("bmaw", (8, 1.2, 1.2, 1.2), (14, 1.0, 0.9, 1.0), (30, 0.95, 0.6, 1.1), (40, 0.95, 0.6, 1.1))
legs(a, [(8, 0, 0, 0), (12, 50, 0, 6), (18, 90, 0, 6), (40, 90, 0, 6)], sr=[(8, 0, 0, 0), (12, -70, 0, 0), (18, -100, 0, 0), (40, -100, 0, 0)])
a.p("body", (8, 0, 0, 0), (12, 0, -3.5, 0), (18, 0, -6.5, 1.0), (40, 0, -6.5, 1.0))
a.r("root", (18, 0, 0, 0), (24, -40, 0, 0), (28, -78, 0, 0), (30, -72, 0, 0), (32, -76, 0, 0), (40, -76, 0, 0))
a.p("root", (18, 0, 0, 0), (28, 0, -1.0, -2.0), (40, 0, -1.0, -2.0))
a.r("ahoge", (4, 30, 0, 20), (8, -20, 0, -30), (14, 20, 0, 10), (24, 0, 0, 0), (30, 60, 0, 0), (34, 40, 0, 10), (40, 50, 0, 10))
a.hair([(0, 0, 0, 0), (4, 10, 0, 16), (8, -8, 0, -16), (14, 10, 0, 10), (24, -20, 0, 0), (30, 20, 0, 0), (40, 16, 0, 6)], delay=2)
a.done()

m.save(OUT)
print("cubes", len(m.cubes), "anims", [x["name"] for x in m.anims])
