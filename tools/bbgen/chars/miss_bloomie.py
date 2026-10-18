"""Miss Bloomie (normal teacher, black-and-white) - generates assets/fpe/bbmodels/miss_bloomie.bbmodel.
Reference: docs/ref/confirmed/miss_bloomie.jpg - spiky near-black bob with a tall tuft and a pale bow on top, pale face with
closed smug eyes, dark long-sleeved jacket with pale collar + two white buttons, flared grey A-line skirt (darker upper band,
pale lower wedge), very long thin dark legs ending in points, big pale CLAWED right hand, a long striped cleaver blade held
point-down in the left hand. Box-cutter teacher, pure melee kit (grenade/launcher/detonator/fuse prop bones stay in the rig but are always hidden).
Blockbench space: Y up, ground 0, faces -Z. Character's RIGHT = +X.
Rotation signs (file values): arm/leg rx>0 = swing forward, torso/head rx>0 = lean back / look up,
ry>0 = turn to the character's left, rz>0 = hanging part swings toward +X (character's right).
Blade (child of hand_l) points DOWN at rot 0; blade rx>0 swings its point forward.
Run: python3 tools/bbgen/chars/miss_bloomie.py
"""
import math, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from bbgen import Model, mix  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "../../../src/main/resources/assets/fpe/bbmodels/miss_bloomie.bbmodel")

# ------------------------------------------------------------------ palette (3-tone ink drawing, slight blue-violet ink)
DARK, DARK_D, DARK_HI = 0x312C42, 0x1D1A29, 0x4D4762
LINE = 0x8D8AA0
SKIN, SKIN_D, SKIN_L = 0xE4E4E8, 0xA9AAB6, 0xF4F4F6
SKIRT, SKIRT_D, SKIRT_L = 0x8D9C9F, 0x66777B, 0xDCE1DF
BOW, BOW_D = 0xD9DEDE, 0x98A3A6
BLADE, BLADE_D, BLADE_L = 0xCDD3D2, 0x7E8A8D, 0xF1F3F2
GRN, GRN_D = 0x8E9A82, 0x55604C
METAL = 0xB6BBBE
FIRE, FIRE2 = 0xFFB030, 0xFFF0A0
MOUTH = 0x1A1520

m = Model("miss_bloomie", S=8, atlas=2048)
R = m.rng


# ------------------------------------------------------------------ painters
def all_faces(fn, skip=()):
    return {k: fn for k in ("north", "south", "east", "west", "up", "down") if k not in skip}


def combo(*fns):
    def f(F):
        for fn in fns: fn(F)
    return f


def strands(base=DARK, hi=DARK_HI, dark=DARK_D, ink=True):
    def f(F):
        cols = [R.random() for _ in range(F.w)]
        for x in range(F.w):
            c = mix(base, hi, 0.55) if cols[x] > 0.88 else mix(base, dark, 0.6) if cols[x] < 0.18 else base
            for y in range(F.h):
                F.px(x, y, mix(c, dark, 0.35 * abs(y / max(1, F.h - 1) - 0.3)))
        if ink and F.w >= 4 and F.h >= 8 and R.random() < 0.5:
            x = R.randint(1, F.w - 2)
            for y in range(R.randint(0, F.h // 3), F.h - 2):
                F.px(x, y, LINE)
    return f


def hstripe(c, y0, h):
    return lambda F: F.rect(0, y0, F.w, h, c)


def edge_lines(c):
    return lambda F: (F.rect(0, 0, 1, F.h, c), F.rect(F.w - 1, 0, 1, F.h, c))


def folds(base, dark, light, n=3):
    def f(F):
        for i in range(n):
            x = int((i + 0.5) * F.w / n) + R.randint(-1, 1)
            for y in range(F.h):
                if R.random() < 0.85:
                    F.px(x, y, mix(base, dark, 0.45)); F.px(x + 1, y, mix(base, light, 0.45))
    return f


def face_front(F):
    W, H = F.w, F.h  # 44 x 46
    for y in range(H):
        for x in range(W):
            F.px(x, y, mix(SKIN, SKIN_D, max(0, (14 - y) / 14) * 0.8))
    # closed, smug eyes (heavy lid arcs with lashes flicking outward), right eye half under the bangs
    for cx, s in ((13, 1), (31, -1)):
        for i in range(-6, 7):
            y = 22 + 0.08 * i * i
            F.disc(cx + i, y, 1.0, DARK_D)
        F.line(cx - 6 * s, 22 + 2.8, cx - 9 * s, 20.5, DARK_D, 1.2)  # outer lash flick
        F.line(cx - 3, 25.5, cx + 3, 25.5, SKIN_D, 1)                  # under-lid crease
        F.line(cx - 4, 17.5, cx + 4, 16.5 if s > 0 else 18.5, DARK, 1.2)  # brow (raised on one side = smug)
    # small sideways smirk, corner pulled up on her left
    F.line(17, 34, 24, 34.6, MOUTH, 1.3)
    F.line(24, 34.6, 28, 32.4, MOUTH, 1.3)
    F.disc(28.4, 32.0, 0.8, MOUTH)
    F.line(21, 29, 22, 31, SKIN_D, 1)  # nose hint
    for x in (8, 10, 33, 35):  # blush hatches
        F.line(x, 30, x + 1.5, 28.5, SKIN_D, 1)


def chest_front(F):
    W, H = F.w, F.h
    folds(DARK, DARK_D, DARK_HI, 2)(F)
    F.line(W * 0.5, 0, W * 0.5, H, DARK_D, 1)       # placket
    for yy in (0.42, 0.7):                          # two white buttons
        F.disc(W * 0.38, H * yy, 2.1, SKIN_D); F.disc(W * 0.38 - 0.3, H * yy - 0.3, 1.5, SKIN_L)
    F.line(W * 0.12, H * 0.85, W * 0.3, H * 0.6, LINE, 1)


def skirt_paint(light_side):
    """grey A-line skirt: darker upper band with a diagonal edge, pale lower wedge, ink fold lines."""
    def f(F):
        for y in range(F.h):
            for x in range(F.w):
                u = x / max(1, F.w - 1)
                edge = F.h * (0.62 - 0.35 * (u if light_side else 1 - u))
                c = mix(SKIRT, SKIRT_D, 0.3 * (1 - y / F.h)) if y < edge else mix(SKIRT_L, SKIRT, 0.15 * (y / F.h))
                F.px(x, y, c)
        for i in range(3):
            x = int((i + 0.7) * F.w / 3.2)
            F.line(x, F.h * 0.45, x + (2 if light_side else -2), F.h - 1, SKIRT_D, 1)
        F.rect(0, F.h - 1, F.w, 1, SKIRT_D)
    return f


def blade_paint(F):
    for y in range(F.h):
        for x in range(F.w):
            F.px(x, y, mix(BLADE_L, BLADE, x / max(1, F.w - 1)))
    for k in range(1, 9):  # the drawing's horizontal bands
        y = int(k * F.h / 9)
        F.rect(0, y, F.w, 2, BLADE_D)
        F.rect(0, y + 2, F.w, 1, BLADE_L)
    F.rect(F.w - 2, 0, 2, F.h, BLADE_D)  # spine


# ------------------------------------------------------------------ skeleton
m.group("root", (0, 0, 0))
m.group("body", (0, 15, 0), parent="root")
for k in ("f", "b", "r", "l"):
    m.group("skirt_" + k, (0, 18.4, 0), parent="body")
m.group("belt_bombs", (0, 18, 1.6), parent="body")
m.group("chest", (0, 18.4, 0), parent="body")
m.group("head", (0, 25.4, 0), parent="chest")
m.group("bangs", (0, 30.6, -3.0), parent="head")
m.group("hair_r", (3.0, 30, 0), parent="head")
m.group("hair_l", (-3.0, 30, 0), parent="head")
m.group("hair_b", (0, 30, 2.8), parent="head")
m.group("tuft", (0, 31.6, 0.4), parent="head")
m.group("bow", (0, 34.0, -1.5), parent="tuft")
m.group("fuse", (0.4, 37.6, 0.9), parent="tuft")
m.group("launcher", (4.8, 25.5, 0.4), parent="chest")
m.group("arm_r", (3.2, 24.2, 0), parent="chest")
m.group("fore_r", (3.6, 19.8, 0), parent="arm_r")
m.group("hand_r", (3.8, 15.8, 0), parent="fore_r")
m.group("claws_r", (3.8, 14.6, -0.2), parent="hand_r")
m.group("grenade", (3.8, 13.6, -0.8), parent="hand_r")
m.group("pin", (3.8, 14.8, -0.8), parent="grenade")
m.group("detonator", (3.8, 14.6, -0.6), parent="hand_r")
m.group("arm_l", (-3.2, 24.2, 0), parent="chest")
m.group("fore_l", (-3.6, 19.8, 0), parent="arm_l")
m.group("hand_l", (-3.8, 15.8, 0), parent="fore_l")
m.group("blade", (-3.8, 15.0, 0), parent="hand_l")
for s, k in ((1, "r"), (-1, "l")):
    m.group("leg_" + k, (1.2 * s, 15, 0), parent="root")
    m.group("shin_" + k, (1.2 * s, 7.8, 0), parent="leg_" + k)
    m.group("foot_" + k, (1.2 * s, 1.2, 0), parent="shin_" + k)

# ------------------------------------------------------------------ legs: long thin dark tights tapering to points
for s, k in ((1, "r"), (-1, "l")):
    x = 1.2 * s
    m.cube("thigh_" + k, "leg_" + k, (x - 1.05, 7.6, -1.05), (x + 1.05, 15.6, 1.05), DARK, color2=DARK_D, grad=True,
           faces={"north": edge_lines(DARK_HI)})
    m.cube("knee_" + k, "shin_" + k, (x - 0.9, 7.0, -0.95), (x + 0.9, 8.4, 0.95), DARK_D)
    m.cube("calf_" + k, "shin_" + k, (x - 0.85, 3.4, -0.85), (x + 0.85, 7.4, 0.95), DARK, color2=DARK_D, grad=True,
           faces={"north": lambda F: F.rect(1, 0, 1, F.h, LINE)})
    m.cube("ankle_" + k, "shin_" + k, (x - 0.6, 1.0, -0.6), (x + 0.6, 3.6, 0.6), DARK_D)
    m.cube("foot_" + k, "foot_" + k, (x - 0.55, 0, -2.0), (x + 0.55, 1.3, 0.6), DARK, faces={"down": lambda F: F.rect(0, 0, F.w, F.h, DARK_D)})
    m.cube("toe_" + k, "foot_" + k, (x - 0.3, 0, -3.8), (x + 0.3, 0.7, -1.8), DARK_D, origin=(x, 0, -2.0), rot=(-6, 0, 0))

# ------------------------------------------------------------------ hips, flared skirt, little bomb belt
m.cube("hips", "body", (-2.3, 14.4, -1.5), (2.3, 18.8, 1.5), DARK_D)
SK = 7.4  # skirt length
m.cube("sk_front", "skirt_f", (-3.2, 18.6 - SK, -2.1), (3.2, 18.8, -1.6), SKIRT, origin=(0, 18.4, -1.8), rot=(18, 0, 0),
       faces={"north": skirt_paint(True), "south": lambda F: F.rect(0, 0, F.w, F.h, SKIRT_D)})
m.cube("sk_back", "skirt_b", (-3.2, 18.6 - SK, 1.6), (3.2, 18.8, 2.1), SKIRT, origin=(0, 18.4, 1.8), rot=(-18, 0, 0),
       faces={"south": skirt_paint(False), "north": lambda F: F.rect(0, 0, F.w, F.h, SKIRT_D)})
m.cube("sk_right", "skirt_r", (2.3, 18.6 - SK, -2.6), (2.8, 18.8, 2.6), SKIRT, origin=(2.5, 18.4, 0), rot=(0, 0, 18),
       faces={"east": skirt_paint(True), "west": lambda F: F.rect(0, 0, F.w, F.h, SKIRT_D)})
m.cube("sk_left", "skirt_l", (-2.8, 18.6 - SK, -2.6), (-2.3, 18.8, 2.6), SKIRT, origin=(-2.5, 18.4, 0), rot=(0, 0, -18),
       faces={"west": skirt_paint(False), "east": lambda F: F.rect(0, 0, F.w, F.h, SKIRT_D)})
for i, (x, z, ry) in enumerate([(2.4, -1.9, 45), (-2.4, -1.9, -45), (2.4, 1.9, -45), (-2.4, 1.9, 45)]):
    sx, sz = (1 if x > 0 else -1), (1 if z > 0 else -1)
    bone = "skirt_f" if z < 0 else "skirt_b"
    m.cube(f"sk_corner{i}", bone, (x - 1.3, 18.6 - SK + 0.4, z - 0.25), (x + 1.3, 18.8, z + 0.25), SKIRT, origin=(x, 18.4, z),
           rot=(-sz * 14, ry, sx * 14), faces={"north": skirt_paint(x > 0), "south": skirt_paint(x < 0)})
m.cube("waistband", "body", (-2.55, 18.0, -1.85), (2.55, 19.0, 1.85), SKIRT_D, faces=all_faces(hstripe(SKIRT, 0, 1)))
# bomb belt at the back of the waist: three little grenades
for i in range(3):
    x = -1.6 + i * 1.6
    m.cube(f"bb{i}", "belt_bombs", (x - 0.6, 17.0, 1.7), (x + 0.6, 18.4, 2.7), GRN, color2=GRN_D, grad=True,
           faces={"south": hstripe(GRN_D, 5, 1)})
    m.cube(f"bbcap{i}", "belt_bombs", (x - 0.3, 18.3, 2.0), (x + 0.3, 18.8, 2.4), METAL)

# ------------------------------------------------------------------ torso: dark jacket, pale collar, white buttons
m.cube("waist", "chest", (-2.2, 18.4, -1.4), (2.2, 21.0, 1.4), DARK, color2=DARK_D, grad=True, faces={"north": folds(DARK, DARK_D, DARK_HI, 2)})
m.cube("torso", "chest", (-2.7, 20.6, -1.6), (2.7, 24.8, 1.6), DARK, color2=DARK_D, grad=True,
       faces={"north": chest_front, "south": folds(DARK, DARK_D, DARK_HI, 3)})
m.cube("bust", "chest", (-2.3, 21.4, -1.95), (2.3, 23.6, -1.5), DARK, faces={"north": folds(DARK, DARK_D, DARK_HI, 1)})
m.cube("shoulders", "chest", (-3.1, 23.6, -1.5), (3.1, 24.9, 1.5), DARK, faces={"up": lambda F: F.rect(0, 0, F.w, F.h, DARK_HI)})
m.cube("neck", "chest", (-0.7, 24.6, -0.7), (0.7, 25.8, 0.7), SKIN_D, color2=SKIN, grad=True)
m.cube("collar_r", "chest", (0.0, 24.0, -1.95), (1.7, 25.4, -1.6), SKIN, origin=(0.1, 25.2, -1.8), rot=(0, 0, 24),
       faces={"north": lambda F: F.line(0, 0, F.w - 1, F.h - 1, SKIN_D, 1)})
m.cube("collar_l", "chest", (-1.7, 24.0, -1.95), (0.0, 25.4, -1.6), SKIN, origin=(-0.1, 25.2, -1.8), rot=(0, 0, -24),
       faces={"north": lambda F: F.line(F.w - 1, 0, 0, F.h - 1, SKIN_D, 1)})
m.cube("collar_back", "chest", (-1.6, 24.6, -0.6), (1.6, 25.6, 1.5), DARK_D)
m.cube("hem_r", "chest", (0.2, 17.6, -1.7), (2.4, 18.8, -1.45), DARK_D, origin=(1.2, 18.6, -1.6), rot=(0, 0, -10))  # jacket tail

# ------------------------------------------------------------------ head
m.cube("skull", "head", (-2.7, 25.6, -2.75), (2.7, 31.2, 2.6), SKIN, faces={"north": face_front, "up": lambda F: F.rect(0, 0, F.w, F.h, DARK_D)})
m.cube("chin", "head", (-1.6, 25.3, -2.6), (1.6, 25.9, 0.8), SKIN_D)
m.cube("crown", "head", (-3.05, 29.4, -3.0), (3.05, 32.6, 3.05), DARK, faces=all_faces(strands()))
m.cube("crown2", "head", (-2.6, 32.4, -2.4), (2.6, 33.4, 2.6), DARK, faces=all_faces(strands()))
m.cube("nape", "hair_b", (-3.0, 26.0, 1.8), (3.0, 30.4, 3.4), DARK, faces=all_faces(strands()))
m.cube("side_r", "hair_r", (2.55, 25.4, -2.6), (3.9, 31.0, 2.9), DARK, faces=all_faces(strands()))
m.cube("side_l", "hair_l", (-4.1, 25.0, -2.6), (-2.55, 31.0, 2.9), DARK, faces=all_faces(strands()))
m.cube("lock_r", "hair_r", (2.0, 24.6, -3.2), (3.4, 28.0, -2.2), DARK, origin=(2.7, 28.0, -2.7), rot=(0, 0, 8), faces=all_faces(strands(ink=False)))
m.cube("lock_l", "hair_l", (-3.6, 24.0, -3.2), (-2.0, 28.0, -2.2), DARK, origin=(-2.8, 28.0, -2.7), rot=(0, 0, -10), faces=all_faces(strands(ink=False)))


def spike(name, parent, base, ln, w, rx, ry, rz, col=DARK, tip=True):
    """hair spike: flat tapered blade growing +Y from `base` (3 segments), rotated about the base."""
    x, y, z = base
    d = max(0.7, w * 0.45)
    m.cube(name, parent, (x - w / 2, y, z - d / 2), (x + w / 2, y + ln * 0.5, z + d / 2), col, origin=base, rot=(rx, ry, rz),
           faces=all_faces(strands(ink=False)))
    if tip:
        m.cube(name + "m", parent, (x - w * 0.32, y + ln * 0.45, z - d * 0.4), (x + w * 0.32, y + ln * 0.8, z + d * 0.4), col,
               origin=base, rot=(rx, ry, rz), faces=all_faces(strands(ink=False)))
        m.cube(name + "t", parent, (x - w * 0.14, y + ln * 0.75, z - d * 0.3), (x + w * 0.14, y + ln, z + d * 0.3), DARK_D,
               origin=base, rot=(rx, ry, rz))


# side spikes: the jagged bob flaring out (her left side flares more, like the drawing)
for i, (y, z, ln, rz) in enumerate([(30.8, 0.2, 4.0, -84), (29.4, -0.8, 6.0, -108), (27.8, 0.8, 6.8, -128), (26.2, 0.0, 5.0, -150)]):
    spike(f"spk_r{i}", "hair_r", (3.0, y, z), ln, 2.2, 0, 0, rz)
for i, (y, z, ln, rz) in enumerate([(31.6, 0.4, 7.4, 70), (30.0, -0.6, 6.0, 102), (28.4, 0.8, 8.0, 120), (26.8, 0.0, 6.2, 140), (25.4, 1.2, 4.2, 164)]):
    spike(f"spk_l{i}", "hair_l", (-3.0, y, z), ln, 2.4, 0, 0, rz)
# back spikes fanning down/out
for i, (x, y, ln, rz) in enumerate([(-2.0, 29.4, 4.6, 150), (0.0, 29.0, 5.4, 180), (2.0, 29.4, 4.4, -150)]):
    spike(f"spk_b{i}", "hair_b", (x, y, 3.0), ln, 2.4, 0, 0, rz)
# bangs: spikes hanging over the forehead (eyes half hidden)
for i, (x, ln, rz) in enumerate([(2.3, 2.8, -18), (1.1, 3.6, -6), (-0.2, 2.6, 4), (-1.4, 3.8, 10), (-2.5, 3.0, 22)]):
    spike(f"bang{i}", "bangs", (x, 31.6, -3.0), ln, 1.5, -174, 0, rz)
m.cube("fringe", "bangs", (-3.1, 30.0, -3.25), (3.1, 32.0, -2.7), DARK, faces=all_faces(strands()))
# tuft: tall spikes shooting up/back from the crown (the bow sits at their base)
for i, (x, ln, rz, rx) in enumerate([(0.2, 7.0, -8, 14), (-0.9, 5.6, 26, 20), (1.2, 5.0, -34, 18), (0.0, 4.6, 2, 44)]):
    spike(f"tuft{i}", "tuft", (x, 32.6, 0.6), ln, 2.2 if i == 0 else 1.7, rx, 0, rz)
# bow (pale ribbon, two loops + knot + tails)
m.cube("bow_knot", "bow", (-0.7, 33.4, -2.0), (0.7, 34.6, -1.0), BOW_D)
m.cube("bow_lr", "bow", (0.5, 33.0, -1.9), (3.2, 35.6, -1.1), BOW, origin=(0.5, 34.0, -1.5), rot=(0, 0, -16),
       faces={"north": lambda F: (F.line(1, F.h / 2, F.w - 2, 1, BOW_D, 1), F.rect(F.w - 1, 0, 1, F.h, BOW_D), F.rect(0, F.h - 1, F.w, 1, BOW_D))})
m.cube("bow_ll", "bow", (-3.2, 33.0, -1.9), (-0.5, 35.6, -1.1), BOW, origin=(-0.5, 34.0, -1.5), rot=(0, 0, 16),
       faces={"north": lambda F: (F.line(1, 1, F.w - 2, F.h / 2, BOW_D, 1), F.rect(0, 0, 1, F.h, BOW_D), F.rect(0, F.h - 1, F.w, 1, BOW_D))})
m.cube("bow_tr", "bow", (0.1, 31.8, -1.85), (0.8, 33.8, -1.35), BOW_D, origin=(0.3, 33.6, -1.6), rot=(0, 0, -22))
m.cube("bow_tl", "bow", (-0.8, 31.9, -1.85), (-0.1, 33.8, -1.35), BOW_D, origin=(-0.3, 33.6, -1.6), rot=(0, 0, 20))
# lit fuse flame on the tuft tip (kamikaze only)
m.group("flame_g", (0.4, 37.4, 0.9), parent="fuse")
m.cube("flame", "flame_g", (0.0, 37.3, 0.5), (0.8, 38.6, 1.3), FIRE, glow=True)
m.cube("flame2", "flame_g", (0.15, 38.4, 0.65), (0.65, 39.4, 1.15), FIRE2, glow=True)

# ------------------------------------------------------------------ arms: long dark sleeves with wide cuffs
for s, k in ((1, "r"), (-1, "l")):
    m.cube("sleeve_" + k, "arm_" + k, (3.2 * s - 1.05, 19.6, -1.05), (3.2 * s + 1.05, 24.6, 1.05), DARK, color2=DARK_D, grad=True,
           faces={"north": folds(DARK, DARK_D, DARK_HI, 1), "east": folds(DARK, DARK_D, DARK_HI, 1)})
    m.cube("fsleeve_" + k, "fore_" + k, (3.6 * s - 1.0, 16.6, -1.0), (3.6 * s + 1.0, 20.0, 1.0), DARK, color2=DARK_D, grad=True)
    m.cube("cuff_" + k, "fore_" + k, (3.7 * s - 1.4, 15.3, -1.4), (3.7 * s + 1.4, 17.0, 1.4), DARK_D,
           faces=all_faces(hstripe(LINE, 0, 1)))
    m.cube("wrist_" + k, "hand_" + k, (3.8 * s - 0.6, 14.8, -0.6), (3.8 * s + 0.6, 15.8, 0.6), SKIN_D)
# right hand: big pale claws
m.cube("palm_r", "hand_r", (3.0, 13.2, -0.9), (4.6, 15.2, 0.9), SKIN, color2=SKIN_D, grad=True, faces={"north": edge_lines(SKIN_D)})
m.cube("thumb_r", "hand_r", (2.6, 12.6, -1.2), (3.2, 14.8, -0.6), SKIN, origin=(2.9, 14.8, -0.9), rot=(16, 0, -28))
for i in range(4):
    x = 2.9 + i * 0.5
    m.cube(f"finger{i}_r", "claws_r", (x, 10.6, -0.75), (x + 0.48, 13.6, -0.05), SKIN, origin=(x + 0.24, 13.4, -0.4), rot=(10, 0, (i - 1.5) * -10),
           faces={"north": edge_lines(SKIN_D)})
    m.cube(f"claw{i}_r", "claws_r", (x + 0.06, 7.9, -0.65), (x + 0.42, 10.9, -0.15), SKIN_L, origin=(x + 0.24, 10.8, -0.4), rot=(26, 0, (i - 1.5) * -16),
           faces={"north": lambda F: F.rect(0, 0, 1, F.h, SKIN_D)})
# left hand: fist around the cleaver
m.cube("fist_l", "hand_l", (-4.6, 13.6, -0.9), (-3.0, 15.2, 0.9), SKIN, color2=SKIN_D, grad=True, faces={"north": edge_lines(SKIN_D)})
m.cube("hilt", "blade", (-4.1, 12.6, -0.45), (-3.5, 16.4, 0.45), DARK_D, faces=all_faces(hstripe(LINE, 3, 1)))
m.cube("guard", "blade", (-5.4, 11.8, -0.6), (-2.2, 12.8, 0.6), BLADE_D, faces=all_faces(hstripe(BLADE, 0, 1)))
m.cube("blade_main", "blade", (-5.3, 0.8, -0.28), (-2.3, 12.0, 0.28), BLADE, faces={"north": blade_paint, "south": blade_paint,
       "east": lambda F: F.rect(0, 0, F.w, F.h, BLADE_D), "west": lambda F: F.rect(0, 0, F.w, F.h, BLADE_L)})
m.cube("blade_tip", "blade", (-5.0, -1.6, -0.26), (-2.6, 1.4, 0.26), BLADE, origin=(-2.6, 1.0, 0), rot=(0, 0, 24),
       faces={"north": blade_paint, "south": blade_paint})
m.cube("blade_notch", "blade", (-2.6, 1.4, -0.3), (-1.7, 3.0, 0.3), BLADE_L, origin=(-2.3, 3.0, 0), rot=(0, 0, -30))
m.cube("blade_edge", "blade", (-5.45, 0.8, -0.12), (-5.25, 12.0, 0.12), BLADE_L)
# grenade prop (right hand)
m.cube("gren_body", "grenade", (3.2, 12.6, -1.4), (4.4, 14.2, -0.2), GRN, color2=GRN_D, grad=True,
       faces=all_faces(combo(hstripe(GRN_D, 4, 1), hstripe(GRN_D, 8, 1), edge_lines(GRN_D))))
m.cube("gren_cap", "grenade", (3.5, 14.1, -1.1), (4.1, 14.7, -0.5), METAL)
m.cube("gren_lever", "grenade", (4.1, 13.0, -1.0), (4.5, 14.6, -0.6), METAL, origin=(4.3, 14.6, -0.8), rot=(0, 0, -10))
m.cube("pin_ring", "pin", (3.0, 14.4, -0.95), (3.6, 15.0, -0.65), METAL, faces=all_faces(lambda F: F.rect(1, 1, max(1, F.w - 2), max(1, F.h - 2), GRN_D)))
m.cube("spark", "grenade", (3.6, 14.7, -1.0), (4.0, 15.1, -0.6), FIRE, glow=True)
# detonator (right hand, carpet bomb)
m.cube("det_box", "detonator", (3.1, 12.6, -1.5), (4.5, 14.6, -0.3), DARK_D, faces={"north": lambda F: F.disc(F.w / 2, F.h * 0.6, 3, 0xC03030, glow=True)})
m.cube("det_ant", "detonator", (3.9, 14.5, -1.1), (4.15, 16.6, -0.85), METAL)
m.cube("det_bulb", "detonator", (3.8, 16.5, -1.2), (4.25, 17.0, -0.75), 0xFF4040, glow=True)
# rocket tube (shoulder-mounted, rocket)
m.cube("tube", "launcher", (4.00, 25.00, -6.00), (5.60, 26.60, 4.40), GRN, color2=GRN_D, grad=True,
       faces={"up": combo(hstripe(GRN_D, 10, 2), hstripe(GRN_D, 70, 2)), "east": hstripe(GRN_D, 6, 1), "west": hstripe(GRN_D, 6, 1)})
m.cube("tube_mouth", "launcher", (3.80, 24.80, -6.60), (5.80, 26.80, -5.60), GRN_D, faces={"north": lambda F: F.disc(F.w / 2, F.h / 2, 6, 0x0E0E10)})
m.cube("tube_back", "launcher", (3.85, 24.85, 4.20), (5.75, 26.75, 5.20), GRN_D)
m.cube("tube_grip", "launcher", (4.50, 23.40, -2.60), (5.10, 25.00, -1.80), DARK_D)
m.cube("tube_sight", "launcher", (4.00, 26.60, -3.00), (4.50, 27.40, -2.20), METAL)
m.group("rocket_tip", (4.80, 25.80, -6.40), parent="launcher")
m.cube("rocket_head", "rocket_tip", (4.30, 25.30, -7.60), (5.30, 26.30, -6.40), 0xA03030)

# ================================================================== animation
PROPS = {"grenade": 1, "detonator": 1, "launcher": 1, "fuse": 1}
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

    def show(self, bone, t0, t1):
        """prop visible from t0 to t1 (pops in/out over half a tick)"""
        keys = [(0, *HIDE)] if t0 > 0 else []
        if t0 > 0: keys.append((t0 - 0.5, *HIDE))
        keys.append((t0, 1, 1, 1))
        if t1 < self.ticks:
            keys += [(t1, 1, 1, 1), (t1 + 0.5, *HIDE)]
        return self.scl(bone, *keys)

    def drape(self, chain, keys, delay=2, gain=0.8):
        g = 1.0
        for i, b in enumerate(chain):
            seen, out = set(), []
            for (t, x, y, z) in keys:
                tt = min(self.ticks, t + delay * i)
                if tt in seen: continue
                seen.add(tt); out.append((tt, x * g, y * g, z * g))
            self.rot(b, *out)
            g *= gain
        return self

    def hair(self, keys, delay=2):
        """whole-hair secondary motion from one 'whip' curve (x = forward/back flick, z = sideways)"""
        self.drape(["hair_b"], keys, delay=delay)
        self.drape(["hair_r"], [(t, x * 0.5, 0, z * 0.6 - abs(x) * 0.15) for (t, x, y, z) in keys], delay=delay)
        self.drape(["hair_l"], [(t, x * 0.5, 0, z * 0.6 + abs(x) * 0.15) for (t, x, y, z) in keys], delay=delay)
        self.drape(["tuft"], [(t, x * 0.6, 0, z * 0.5) for (t, x, y, z) in keys], delay=delay + 1)
        self.drape(["bangs"], [(t, x * 0.35, 0, z * 0.3) for (t, x, y, z) in keys], delay=delay)
        return self

    def skirt(self, keys, delay=2):
        """skirt panels flare: x>0 kicks the front out (back in), z>0 flares the right side out"""
        self.drape(["skirt_f"], [(t, x, 0, 0) for (t, x, y, z) in keys], delay=delay)
        self.drape(["skirt_b"], [(t, x * 0.7, 0, 0) for (t, x, y, z) in keys], delay=delay)
        self.drape(["skirt_r"], [(t, 0, 0, z) for (t, x, y, z) in keys], delay=delay)
        self.drape(["skirt_l"], [(t, 0, 0, z) for (t, x, y, z) in keys], delay=delay)
        return self

    def done(self):
        for p in PROPS:
            if p not in self.tr or "scale" not in self.tr[p]:
                self.scl(p, (0, *HIDE))
        for b, v in REST.items():
            if b not in self.tr or "rotation" not in self.tr[b]:
                self.rot(b, (0, *v))
        tracks = {b: {ch: sorted([(t / 20.0, x, y, z) for (t, x, y, z) in v], key=lambda q: q[0]) for ch, v in chs.items()}
                  for b, chs in self.tr.items()}
        m.anim(self.name, self.ticks / 20.0, tracks, loop=self.loop)


# rest pose = the reference: claw hand hanging open out to the side, blade hanging point-down/forward, slight lean
REST = {
    "arm_r": (6, 0, 14), "fore_r": (10, 0, 4), "claws_r": (12, 0, 0),
    "arm_l": (8, 0, -10), "fore_l": (16, 0, 0), "hand_l": (0, 0, 0), "blade": (12, 0, -16),
}


def rest(b):
    return REST.get(b, (0, 0, 0))


def legs_both(a, keys_leg, keys_shin, keys_foot=None):
    for s, k in ((1, "r"), (-1, "l")):
        a.rot("leg_" + k, *[(t, x, y * s, z * s) for (t, x, y, z) in keys_leg])
        a.rot("shin_" + k, *keys_shin)
        if keys_foot: a.rot("foot_" + k, *keys_foot)


# ------------------------------------------------------------------ idle (80 loop): smug sway, claws flex, blade tapping
a = A("idle", 80, loop=True)
a.rot("body", (0, 0, 0, 2), (40, 0, 0, -1), (80, 0, 0, 2))
a.pos("body", (0, 0, 0, 0), (20, 0, -0.15, 0), (40, 0, 0, 0), (60, 0, -0.15, 0), (80, 0, 0, 0))
a.rot("chest", (0, -4, 6, -2), (20, -3, 4, 0), (40, -4, 6, 2), (60, -3, 8, 0), (80, -4, 6, -2))
a.rot("head", (0, -6, -8, 8), (20, -5, -6, 6), (40, -6, -8, 9), (60, -4, -10, 6), (80, -6, -8, 8))
a.rot("arm_r", (0, 6, 0, 14), (40, 8, 0, 16), (80, 6, 0, 14))
a.rot("fore_r", (0, 10, 0, 4), (40, 14, 0, 4), (80, 10, 0, 4))
a.rot("claws_r", (0, 12, 0, 0), (30, 18, 0, 0), (33, -6, 0, 0), (36, 24, 0, 0), (39, 0, 0, 0), (44, 12, 0, 0), (80, 12, 0, 0))
a.rot("arm_l", (0, 8, 0, -10), (40, 10, 0, -12), (80, 8, 0, -10))
a.rot("fore_l", (0, 16, 0, 0), (40, 18, 0, 0), (80, 16, 0, 0))
a.rot("blade", (0, 12, 0, -16), (56, 12, 0, -16), (60, 22, 0, -12), (63, 10, 0, -16), (66, 20, 0, -12), (70, 12, 0, -16), (80, 12, 0, -16))
legs_both(a, [(0, 0, 0, 1), (80, 0, 0, 1)], [(0, 0, 0, 0), (80, 0, 0, 0)])
a.rot("leg_l", (0, -4, 0, -4), (40, -5, 0, -3), (80, -4, 0, -4))
a.hair([(0, 0, 0, 2), (20, -3, 0, 0), (40, 0, 0, -2), (60, -3, 0, 0), (80, 0, 0, 2)], delay=4)
a.skirt([(0, 2, 0, 1), (40, 1, 0, -1), (80, 2, 0, 1)], delay=4)
a.done()

# ------------------------------------------------------------------ walk (20 loop): long scissor strides on her stilt legs, blade swinging
a = A("walk", 20, loop=True)
a.rot("leg_r", (0, 32, 0, 0), (5, 0, 0, 0), (10, -30, 0, 0), (15, 0, 0, 0), (20, 32, 0, 0))
a.rot("shin_r", (0, -4, 0, 0), (5, -8, 0, 0), (10, -10, 0, 0), (13, -60, 0, 0), (17, -30, 0, 0), (20, -4, 0, 0))
a.rot("foot_r", (0, -14, 0, 0), (5, 0, 0, 0), (10, 14, 0, 0), (20, -14, 0, 0))
a.rot("leg_l", (0, -30, 0, 0), (5, 0, 0, 0), (10, 32, 0, 0), (15, 0, 0, 0), (20, -30, 0, 0))
a.rot("shin_l", (0, -10, 0, 0), (3, -60, 0, 0), (7, -30, 0, 0), (10, -4, 0, 0), (15, -8, 0, 0), (20, -10, 0, 0))
a.rot("foot_l", (0, 14, 0, 0), (10, -14, 0, 0), (20, 14, 0, 0))
a.pos("body", (0, 0, -0.5, 0), (5, 0, 0.4, 0), (10, 0, -0.5, 0), (15, 0, 0.4, 0), (20, 0, -0.5, 0))
a.rot("body", (0, -4, 6, 0), (10, -4, -6, 0), (20, -4, 6, 0))
a.rot("chest", (0, -2, -6, 1), (10, -2, 6, -1), (20, -2, -6, 1))
a.rot("arm_r", (0, -26, 0, 4), (10, 26, 0, 6), (20, -26, 0, 4))
a.rot("fore_r", (0, 6, 0, 0), (10, 24, 0, 0), (20, 6, 0, 0))
a.rot("arm_l", (0, 22, 0, -4), (10, -20, 0, -4), (20, 22, 0, -4))
a.rot("blade", (0, -10, 0, 0), (10, 14, 0, 0), (20, -10, 0, 0))
a.hair([(0, -8, 0, 3), (5, -11, 0, 0), (10, -8, 0, -3), (15, -11, 0, 0), (20, -8, 0, 3)], delay=2)
a.skirt([(0, 8, 0, 4), (5, 3, 0, 0), (10, 8, 0, -4), (15, 3, 0, 0), (20, 8, 0, 4)], delay=1)
tracks = {b: {ch: sorted([(t / 20.0, x, y, z) for (t, x, y, z) in v]) for ch, v in chs.items()} for b, chs in a.tr.items()}
m.anim("walk", 1.0, tracks, loop=True)

# ------------------------------------------------------------------ claw_rake (28): claw cocked high 6, downward rake 9, backhand return rake 17, recover
a = A("claw_rake", 28)
a.rot("arm_r", (0, *rest("arm_r")), (6, 150, 0, 40), (8, 110, 0, 10), (9, 60, 0, -20), (11, 40, 0, -40), (14, 60, 0, -50), (16, 80, 0, 0),
      (17, 84, 0, 50), (19, 70, 0, 70), (24, 20, 0, 30), (28, *rest("arm_r")))
a.rot("fore_r", (0, *rest("fore_r")), (6, 30, 0, 0), (9, 0, 0, 0), (14, 30, 0, 0), (17, 0, 0, 0), (24, 14, 0, 0), (28, *rest("fore_r")))
a.rot("claws_r", (0, 12, 0, 0), (6, -30, 0, 0), (9, 50, 0, 0), (13, 20, 0, 0), (17, 50, 0, 0), (22, 30, 0, 0), (28, 12, 0, 0))
a.rot("hand_r", (0, 0, 0, 0), (14, 0, 0, 0), (16, 0, 80, 0), (20, 0, 60, 0), (26, 0, 0, 0))
a.rot("arm_l", (0, *rest("arm_l")), (6, -20, 0, -30), (9, 20, 0, -20), (17, -10, 0, -30), (28, *rest("arm_l")))
a.rot("blade", (0, *rest("blade")), (9, 10, 0, 0), (17, 40, 0, -10), (28, *rest("blade")))
a.rot("chest", (0, 0, 0, 0), (6, 10, 30, 0), (9, -14, -24, 0), (12, -12, -30, 0), (17, -8, 30, 0), (20, -6, 34, 0), (28, 0, 0, 0))
a.rot("body", (0, 0, 0, 0), (6, 4, 14, 0), (9, -12, -16, 0), (17, -10, 16, 0), (22, -4, 8, 0), (28, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (6, 0, -0.6, 0.6), (9, 0, -1.6, -1.2), (17, 0, -1.6, -1.6), (28, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (6, 10, -20, 0), (9, -10, 20, 0), (17, -6, -24, 0), (24, 0, -6, 8), (28, 0, 0, 0))
a.rot("leg_r", (0, 0, 0, 0), (9, -30, 0, 4), (17, -36, 0, 4), (24, -10, 0, 0), (28, 0, 0, 0))
a.rot("leg_l", (0, 0, 0, 0), (9, 24, 0, -4), (17, 30, 0, -4), (24, 10, 0, 0), (28, 0, 0, 0))
a.rot("shin_l", (0, 0, 0, 0), (9, -30, 0, 0), (17, -36, 0, 0), (28, 0, 0, 0))
a.hair([(0, 0, 0, 0), (6, 8, 0, -12), (9, -20, 0, 14), (12, -14, 0, 18), (17, -20, 0, -16), (20, -14, 0, -18), (28, 0, 0, 0)])
a.skirt([(0, 0, 0, 0), (6, -4, 0, -6), (9, 10, 0, 12), (17, 12, 0, -14), (22, 4, 0, -4), (28, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ cleaver_slash (34): blade dragged back low 10, huge horizontal sweep peaking 15, spin-through, reset
a = A("cleaver_slash", 34)
a.rot("arm_l", (0, *rest("arm_l")), (6, -20, 0, -30), (10, -40, 40, -70), (13, 60, 0, -90), (15, 90, -20, -40), (17, 80, -40, 20), (20, 60, -40, 40),
      (26, 20, 0, 0), (34, *rest("arm_l")))
a.rot("fore_l", (0, *rest("fore_l")), (10, 30, 0, 0), (15, 0, 0, 0), (20, 20, 0, 0), (34, *rest("fore_l")))
a.rot("blade", (0, *rest("blade")), (6, 40, 0, 0), (10, 90, 0, 40), (13, 90, 0, 0), (15, 90, 0, -10), (18, 90, 0, -30), (24, 60, 0, 0), (34, *rest("blade")))
a.rot("arm_r", (0, *rest("arm_r")), (10, 40, 0, 40), (15, -30, 0, 60), (20, -20, 0, 50), (34, *rest("arm_r")))
a.rot("claws_r", (0, 12, 0, 0), (10, 40, 0, 0), (15, -20, 0, 0), (34, 12, 0, 0))
a.rot("root", (0, 0, 0, 0), (10, 0, 30, 0), (13, 0, 0, 0), (15, 0, -40, 0), (18, 0, -80, 0), (24, 0, -30, 0), (34, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (10, 0, -2.4, 0.6), (15, 0, -2.6, -1.0), (20, 0, -2.2, -0.6), (34, 0, 0, 0))
a.rot("body", (0, 0, 0, 0), (10, -6, 30, 0), (13, -12, 0, 0), (15, -16, -30, 0), (20, -10, -30, 0), (34, 0, 0, 0))
a.rot("chest", (0, 0, 0, 0), (10, 6, 30, -6), (13, -6, 0, 0), (15, -10, -30, 6), (20, -6, -24, 4), (34, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (10, 0, -50, 0), (13, -4, -10, 0), (15, -8, 30, 0), (20, 0, 50, 10), (28, 0, 10, 0), (34, 0, 0, 0))
legs_both(a, [(0, 0, 0, 0), (10, 30, 0, 10), (15, 20, 0, 14), (20, 24, 0, 12), (34, 0, 0, 0)],
          [(0, 0, 0, 0), (10, -54, 0, 0), (15, -40, 0, 0), (20, -46, 0, 0), (34, 0, 0, 0)], [(0, 0, 0, 0), (10, 20, 0, 0), (20, 20, 0, 0), (34, 0, 0, 0)])
a.rot("leg_r", (10, -10, 0, 14), (15, -24, 0, 18), (20, -20, 0, 16))
a.hair([(0, 0, 0, 0), (10, 4, 0, 20), (13, -10, 0, 0), (16, -20, 0, -34), (20, -16, 0, -30), (28, -4, 0, 0), (34, 0, 0, 0)])
a.skirt([(0, 0, 0, 0), (10, 6, 0, -10), (15, 10, 0, 30), (20, 10, 0, 34), (28, 2, 0, 4), (34, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ stomp (32): knee high 9 (hop), heel SLAM 13, ground shock, settle
a = A("stomp", 32)
a.pos("root", (0, 0, 0, 0), (8, 0, 0, 0), (10, 0, 1.4, 0), (13, 0, 0, 0), (32, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (6, 0, -1.4, 0), (10, 0, 0.5, 0), (13, 0, -2.4, 0), (18, 0, -2.0, 0), (32, 0, 0, 0))
a.rot("body", (0, 0, 0, 0), (6, -8, 0, 4), (10, 8, 0, 8), (13, -16, 0, -4), (18, -12, 0, -2), (32, 0, 0, 0))
a.rot("chest", (0, 0, 0, 0), (10, 12, 0, 4), (13, -14, 0, 0), (20, -8, 0, 0), (32, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (10, 10, 0, 0), (13, -24, 0, 0), (16, -16, 0, 6), (24, 0, 0, 8), (32, 0, 0, 0))
a.rot("leg_r", (0, 0, 0, 0), (6, 30, 0, 4), (10, 100, 0, 6), (12, 40, 0, 4), (13, 10, 0, 6), (20, 8, 0, 4), (32, 0, 0, 0))
a.rot("shin_r", (0, 0, 0, 0), (6, -50, 0, 0), (10, -110, 0, 0), (12, -30, 0, 0), (13, 0, 0, 0), (32, 0, 0, 0))
a.rot("foot_r", (0, 0, 0, 0), (10, 40, 0, 0), (13, 0, 0, 0))
a.rot("leg_l", (0, 0, 0, 0), (6, -6, 0, -4), (13, -20, 0, -8), (20, -16, 0, -6), (32, 0, 0, 0))
a.rot("shin_l", (0, 0, 0, 0), (6, -10, 0, 0), (13, -30, 0, 0), (20, -20, 0, 0), (32, 0, 0, 0))
a.rot("arm_r", (0, *rest("arm_r")), (8, -40, 0, 50), (12, -30, 0, 70), (13, 20, 0, 80), (18, 10, 0, 50), (32, *rest("arm_r")))
a.rot("arm_l", (0, *rest("arm_l")), (8, -40, 0, -50), (12, -30, 0, -70), (13, 20, 0, -80), (18, 10, 0, -50), (32, *rest("arm_l")))
a.rot("blade", (0, *rest("blade")), (10, -30, 0, 0), (13, 30, 0, 20), (32, *rest("blade")))
a.rot("claws_r", (0, 12, 0, 0), (10, -20, 0, 0), (13, 40, 0, 0), (32, 12, 0, 0))
a.hair([(0, 0, 0, 0), (8, -10, 0, 0), (11, -20, 0, 0), (13, 36, 0, 0), (16, 20, 0, 0), (22, -6, 0, 0), (32, 0, 0, 0)])
a.skirt([(0, 0, 0, 0), (9, -10, 0, -6), (13, 24, 0, 28), (16, 18, 0, 22), (24, 2, 0, 2), (32, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ kick_back (38): hop-in chamber 10-14, high roundhouse KICK 16, follow-through, recover
a = A("kick_back", 38)
a.rot("arm_r", (0, *rest("arm_r")), (4, 20, 0, 30), (6, 30, 0, 40), (10, 20, 0, 50), (16, -20, 0, 70), (22, 0, 0, 40), (38, *rest("arm_r")))
a.rot("fore_r", (0, *rest("fore_r")), (4, 30, 0, 0), (6, 30, 0, 0), (16, 0, 0, 0), (38, *rest("fore_r")))
a.rot("arm_l", (0, *rest("arm_l")), (10, -10, 0, -40), (16, 50, 0, -60), (22, 20, 0, -40), (38, *rest("arm_l")))
a.rot("blade", (0, *rest("blade")), (10, 30, 0, 0), (16, -20, 0, -20), (38, *rest("blade")))
a.rot("body", (0, 0, 0, 0), (10, 10, -20, 0), (14, 14, -26, 0), (16, -20, 20, 0), (20, -16, 26, 0), (28, -4, 6, 0), (38, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (14, 0, -1, 0.6), (16, 0, 0.2, -0.6), (22, 0, 0, -0.4), (38, 0, 0, 0))
a.rot("chest", (0, 0, 0, 0), (14, 6, -10, 0), (16, -10, 14, 0), (22, -6, 10, 0), (38, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (6, -6, -10, 0), (10, -4, -14, 0), (14, -10, 0, 0), (16, -16, 0, 0), (22, -6, 0, 8), (38, 0, 0, 0))
a.rot("leg_r", (0, 0, 0, 0), (10, -30, 0, 4), (14, -60, 0, 6), (16, 100, 0, 6), (19, 120, 0, 6), (24, 40, 0, 4), (30, 0, 0, 0), (38, 0, 0, 0))
a.rot("shin_r", (0, 0, 0, 0), (10, -50, 0, 0), (14, -110, 0, 0), (16, -10, 0, 0), (19, 0, 0, 0), (24, -40, 0, 0), (30, 0, 0, 0))
a.rot("foot_r", (0, 0, 0, 0), (14, 20, 0, 0), (16, -30, 0, 0), (24, 0, 0, 0))
a.rot("leg_l", (0, 0, 0, 0), (14, 10, 0, -4), (16, -16, 0, -4), (22, -10, 0, -4), (38, 0, 0, 0))
a.rot("shin_l", (0, 0, 0, 0), (14, -30, 0, 0), (16, -20, 0, 0), (38, 0, 0, 0))
a.hair([(0, 0, 0, 0), (10, 8, 0, 0), (14, 12, 0, -10), (16, -30, 0, 10), (20, -20, 0, 6), (30, 0, 0, 0), (38, 0, 0, 0)])
a.skirt([(0, 0, 0, 0), (14, -6, 0, -4), (16, 34, 0, 12), (20, 30, 0, 10), (26, 6, 0, 2), (38, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ overhead_chop (36): two-hand overhead raise 12, vertical chop biting the floor 18, blade stuck, wrench free
a = A("overhead_chop", 36)
a.rot("arm_l", (0, *rest("arm_l")), (6, 100, 0, -10), (12, 190, 0, 10), (14, 196, 0, 12), (16, 140, 0, 6), (18, 60, 0, 4), (24, 54, 0, 4), (28, 70, 0, 0),
      (30, 40, 0, -10), (36, *rest("arm_l")))
a.rot("fore_l", (0, *rest("fore_l")), (6, 40, 0, 0), (12, 30, 0, 0), (18, 0, 0, 0), (28, 20, 0, 0), (36, *rest("fore_l")))
a.rot("arm_r", (0, *rest("arm_r")), (6, 100, 0, 10), (12, 190, 0, -6), (14, 196, 0, -8), (16, 140, 0, -10), (18, 60, 0, -14), (24, 54, 0, -14),
      (30, 20, 0, 20), (36, *rest("arm_r")))
a.rot("fore_r", (0, *rest("fore_r")), (12, 30, 0, 0), (18, 0, 0, 0), (36, *rest("fore_r")))
a.rot("blade", (0, *rest("blade")), (6, 100, 0, 0), (12, 120, 0, 0), (16, 90, 0, 0), (18, 70, 0, 0), (24, 70, 0, 0), (28, 40, 0, 0), (30, 70, 0, 0), (36, *rest("blade")))
a.rot("body", (0, 0, 0, 0), (12, 14, 0, 0), (16, -10, 0, 0), (18, -30, 0, 0), (24, -28, 0, 0), (28, -10, 0, 0), (36, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (12, 0, 0.4, 0.6), (18, 0, -3.0, -1.0), (24, 0, -2.8, -1.0), (30, 0, -0.6, 0), (36, 0, 0, 0))
a.rot("chest", (0, 0, 0, 0), (12, 16, 0, 0), (18, -20, 0, 0), (24, -18, 0, 0), (28, 4, 0, 0), (36, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (12, 20, 0, 0), (18, 10, 0, 0), (24, 16, 0, 0), (28, 6, 0, 10), (36, 0, 0, 0))
a.rot("leg_r", (0, 0, 0, 0), (12, 6, 0, 2), (18, -50, 0, 4), (24, -48, 0, 4), (32, 0, 0, 0), (36, 0, 0, 0))
a.rot("shin_r", (0, 0, 0, 0), (18, -10, 0, 0), (32, 0, 0, 0))
a.rot("leg_l", (0, 0, 0, 0), (12, -6, 0, -2), (18, 40, 0, -4), (24, 40, 0, -4), (32, 0, 0, 0), (36, 0, 0, 0))
a.rot("shin_l", (0, 0, 0, 0), (18, -60, 0, 0), (24, -60, 0, 0), (32, 0, 0, 0))
a.rot("foot_l", (0, 0, 0, 0), (18, 30, 0, 0), (24, 30, 0, 0), (32, 0, 0, 0))
a.hair([(0, 0, 0, 0), (12, -10, 0, 0), (18, 40, 0, 0), (22, 26, 0, 0), (28, -10, 0, 0), (36, 0, 0, 0)])
a.skirt([(0, 0, 0, 0), (12, -6, 0, 0), (18, 26, 0, 14), (24, 22, 0, 12), (30, 4, 0, 2), (36, 0, 0, 0)])
a.done()


# ------------------------------------------------------------------ leg_slash (26): sink into a deep lunge 5, drag the blade back low, ankle-height sweep 11, follow-through, rise
a = A("leg_slash", 26)
a.rot("root", (0, 0, 0, 0), (5, 0, 30, 0), (9, 0, 10, 0), (11, 0, -30, 0), (14, 0, -50, 0), (20, 0, -20, 0), (26, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (5, 0, -3.6, 0.6), (9, 0, -4.4, -0.6), (11, 0, -4.6, -1.2), (16, 0, -4.2, -1.0), (22, 0, -1.0, 0), (26, 0, 0, 0))
a.rot("body", (0, 0, 0, 0), (5, -18, 20, 0), (11, -30, -16, 0), (16, -26, -20, 0), (22, -8, -4, 0), (26, 0, 0, 0))
a.rot("chest", (0, 0, 0, 0), (5, -6, 26, -6), (9, -14, 10, 0), (11, -20, -26, 8), (16, -16, -24, 6), (26, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (5, 20, -30, 0), (11, 26, 20, 0), (16, 22, 30, -6), (22, 6, 10, 6), (26, 0, 0, 0))
a.rot("arm_l", (0, *rest("arm_l")), (5, -30, 40, -70), (8, -10, 30, -80), (10, 40, 0, -80), (11, 60, -30, -30), (13, 56, -50, 10), (16, 50, -50, 30),
      (22, 20, -10, 0), (26, *rest("arm_l")))
a.rot("fore_l", (0, *rest("fore_l")), (5, 30, 0, 0), (11, 0, 0, 0), (16, 10, 0, 0), (26, *rest("fore_l")))
a.rot("blade", (0, *rest("blade")), (5, 80, 0, 40), (9, 95, 0, 20), (11, 100, 0, -20), (14, 100, 0, -40), (20, 60, 0, -10), (26, *rest("blade")))
a.rot("arm_r", (0, *rest("arm_r")), (5, 30, 0, 50), (11, -30, 0, 70), (16, -20, 0, 60), (26, *rest("arm_r")))
a.rot("claws_r", (0, 12, 0, 0), (5, 40, 0, 0), (11, -20, 0, 0), (20, 20, 0, 0), (26, 12, 0, 0))
a.rot("leg_l", (0, 0, 0, 0), (5, 50, 0, -10), (11, 60, 0, -14), (16, 60, 0, -14), (22, 20, 0, -4), (26, 0, 0, 0))
a.rot("shin_l", (0, 0, 0, 0), (5, -70, 0, 0), (11, -80, 0, 0), (16, -80, 0, 0), (22, -30, 0, 0), (26, 0, 0, 0))
a.rot("foot_l", (0, 0, 0, 0), (5, 20, 0, 0), (11, 20, 0, 0), (22, 0, 0, 0))
a.rot("leg_r", (0, 0, 0, 0), (5, -24, 0, 8), (11, -36, 0, 10), (16, -34, 0, 10), (22, -10, 0, 2), (26, 0, 0, 0))
a.rot("shin_r", (0, 0, 0, 0), (5, -30, 0, 0), (11, -20, 0, 0), (16, -24, 0, 0), (26, 0, 0, 0))
a.hair([(0, 0, 0, 0), (5, 10, 0, 16), (9, 6, 0, 6), (11, -16, 0, -26), (15, -12, 0, -30), (21, -4, 0, -4), (26, 0, 0, 0)])
a.skirt([(0, 0, 0, 0), (5, 16, 0, -10), (11, 22, 0, 26), (16, 20, 0, 22), (22, 4, 0, 4), (26, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ blade_extend (34): raise the box-cutter, click-click-click 6/9/12 (blade grows), draw back 15, long thrust 18, retract 26-30
a = A("blade_extend", 34)
a.scl("blade", (0, 1, 1, 1), (5.5, 1, 1, 1), (6, 1.08, 1.32, 1.08), (7, 1, 1.25, 1), (8.5, 1, 1.25, 1), (9, 1.08, 1.6, 1.08), (10, 1, 1.5, 1),
      (11.5, 1, 1.5, 1), (12, 1.08, 1.9, 1.08), (13, 1, 1.8, 1), (25, 1, 1.8, 1), (27, 1, 1.4, 1), (29, 1, 1.15, 1), (30, 1, 1, 1))
a.rot("arm_l", (0, *rest("arm_l")), (4, 70, 0, -10), (12, 72, 0, -8), (15, 20, 30, -30), (17, 70, 0, -6), (18, 92, -6, 0), (22, 90, -6, 0), (26, 60, 0, -10),
      (34, *rest("arm_l")))
a.rot("fore_l", (0, *rest("fore_l")), (4, 40, 0, 0), (12, 40, 0, 0), (15, 90, 0, 0), (17, 30, 0, 0), (18, 0, 0, 0), (22, 0, 0, 0), (26, 30, 0, 0), (34, *rest("fore_l")))
a.rot("blade", (0, *rest("blade")), (4, 60, 0, 0), (6, 64, 0, 0), (7, 58, 0, 0), (9, 64, 0, 0), (10, 58, 0, 0), (12, 64, 0, 0), (13, 60, 0, 0),
      (15, 10, 0, 0), (18, 0, 0, 0), (22, 0, 0, 0), (26, 40, 0, 0), (34, *rest("blade")))
a.rot("arm_r", (0, *rest("arm_r")), (4, 30, 0, 30), (12, 30, 0, 30), (15, 60, 0, 10), (18, -20, 0, 40), (24, -10, 0, 30), (34, *rest("arm_r")))
a.rot("claws_r", (0, 12, 0, 0), (6, 30, 0, 0), (7, 0, 0, 0), (9, 30, 0, 0), (10, 0, 0, 0), (12, 30, 0, 0), (13, 0, 0, 0), (18, 40, 0, 0), (34, 12, 0, 0))
a.rot("chest", (0, 0, 0, 0), (4, 6, 10, 0), (12, 6, 10, 0), (15, 4, 34, 0), (18, -10, -30, 0), (22, -8, -28, 0), (28, 0, -6, 0), (34, 0, 0, 0))
a.rot("body", (0, 0, 0, 0), (12, 2, 0, 0), (15, 6, 16, 0), (18, -16, -14, 0), (22, -14, -12, 0), (34, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (15, 0, -1.0, 1.0), (18, 0, -2.2, -2.0), (22, 0, -2.0, -1.8), (30, 0, -0.4, 0), (34, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (4, 10, 26, 10), (6, 12, 28, 14), (9, 10, 28, 6), (12, 12, 26, 14), (15, 0, -20, 0), (18, -4, 20, 0), (24, 0, 10, 6), (34, 0, 0, 0))
a.rot("leg_l", (0, 0, 0, 0), (15, -10, 0, -4), (18, 50, 0, -6), (24, 46, 0, -6), (32, 0, 0, 0))
a.rot("shin_l", (0, 0, 0, 0), (18, -40, 0, 0), (24, -40, 0, 0), (32, 0, 0, 0))
a.rot("leg_r", (0, 0, 0, 0), (15, 10, 0, 4), (18, -34, 0, 6), (24, -30, 0, 6), (32, 0, 0, 0))
a.rot("shin_r", (0, 0, 0, 0), (18, -10, 0, 0), (32, 0, 0, 0))
a.hair([(0, 0, 0, 0), (6, 4, 0, 4), (9, 2, 0, -4), (12, 4, 0, 4), (15, 10, 0, 10), (18, -20, 0, -12), (22, -14, 0, -8), (30, 0, 0, 0), (34, 0, 0, 0)])
a.skirt([(0, 0, 0, 0), (15, -6, 0, -4), (18, 20, 0, 10), (24, 14, 0, 6), (34, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ lunge_stab (30): coil low 8, launch 12 (stretched dash), point-first stab 16, hold, recover
a = A("lunge_stab", 30)
a.pos("body", (0, 0, 0, 0), (8, 0, -4.4, 1.0), (11, 0, -4.6, 1.2), (12, 0, -2.0, -0.6), (14, 0, -1.6, -1.6), (16, 0, -2.2, -2.4), (20, 0, -2.4, -2.0),
      (26, 0, -0.6, 0), (30, 0, 0, 0))
a.rot("body", (0, 0, 0, 0), (8, -30, 14, 0), (12, -40, 6, 0), (16, -26, -16, 0), (20, -24, -14, 0), (30, 0, 0, 0))
a.rot("chest", (0, 0, 0, 0), (8, -8, 20, 0), (12, -6, 16, 0), (16, -10, -34, 0), (20, -8, -30, 0), (30, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (8, 34, -14, 0), (12, 40, -10, 0), (16, 26, 30, 0), (20, 22, 30, -6), (26, 6, 6, 8), (30, 0, 0, 0))
a.rot("arm_l", (0, *rest("arm_l")), (8, -40, 0, -24), (12, -30, 0, -20), (14, 40, 0, -6), (16, 98, -8, 0), (20, 96, -8, 0), (24, 60, 0, -6), (30, *rest("arm_l")))
a.rot("fore_l", (0, *rest("fore_l")), (8, 70, 0, 0), (12, 70, 0, 0), (14, 30, 0, 0), (16, 0, 0, 0), (20, 0, 0, 0), (30, *rest("fore_l")))
a.rot("blade", (0, *rest("blade")), (8, 50, 0, 0), (12, 50, 0, 0), (16, -4, 0, 0), (20, -4, 0, 0), (24, 20, 0, 0), (30, *rest("blade")))
a.rot("arm_r", (0, *rest("arm_r")), (8, -50, 0, 30), (12, -60, 0, 40), (16, -40, 0, 50), (22, -10, 0, 30), (30, *rest("arm_r")))
a.rot("claws_r", (0, 12, 0, 0), (8, 40, 0, 0), (16, -10, 0, 0), (30, 12, 0, 0))
legs_both(a, [(0, 0, 0, 0), (8, 56, 0, 6), (11, 58, 0, 6), (26, 10, 0, 0), (30, 0, 0, 0)], [(0, 0, 0, 0), (8, -100, 0, 0), (11, -100, 0, 0), (26, -10, 0, 0), (30, 0, 0, 0)],
          [(0, 0, 0, 0), (8, 40, 0, 0), (11, 40, 0, 0), (13, -30, 0, 0), (18, 0, 0, 0)])
a.rot("leg_r", (12, -50, 0, 6), (14, -40, 0, 6), (16, -44, 0, 8), (20, -40, 0, 8))
a.rot("shin_r", (12, 0, 0, 0), (16, -10, 0, 0), (20, -10, 0, 0))
a.rot("leg_l", (12, 30, 0, -6), (14, 60, 0, -6), (16, 56, 0, -6), (20, 54, 0, -6))
a.rot("shin_l", (12, -20, 0, 0), (14, -50, 0, 0), (16, -40, 0, 0), (20, -40, 0, 0))
a.hair([(0, 0, 0, 0), (8, 10, 0, 0), (12, 30, 0, 0), (15, 34, 0, 0), (17, -10, 0, -8), (21, -6, 0, -4), (30, 0, 0, 0)])
a.skirt([(0, 0, 0, 0), (8, 14, 0, 8), (12, -20, 0, 6), (16, 20, 0, 10), (22, 8, 0, 4), (30, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ claw_grab (40): claws spread 6, SNATCH 10, hoist 11-22 with squeeze 17, SLAM 25, shake off
a = A("claw_grab", 40)
a.rot("arm_r", (0, *rest("arm_r")), (6, 40, 0, 56), (8, 70, 0, 30), (10, 96, 0, 4), (13, 120, 0, 4), (17, 150, 0, 6), (22, 166, 0, 8), (24, 150, 0, 6),
      (25, 40, 0, 0), (28, 30, 0, 4), (32, 30, 0, 10), (34, 40, 0, 20), (40, *rest("arm_r")))
a.rot("fore_r", (0, *rest("fore_r")), (6, 30, 0, 0), (10, 0, 0, 0), (17, 10, 0, 0), (22, 14, 0, 0), (25, 10, 0, 0), (40, *rest("fore_r")))
a.rot("claws_r", (0, 12, 0, 0), (6, -40, 0, 0), (9, -30, 0, 0), (10, 64, 0, 0), (16, 60, 0, 0), (17, 82, 0, 0), (18, 66, 0, 0), (24, 66, 0, 0),
      (26, -20, 0, 0), (30, 20, 0, 0), (34, -10, 0, 0), (40, 12, 0, 0))
a.rot("hand_r", (0, 0, 0, 0), (16, 0, 0, 0), (17, 0, 20, 10), (18, 0, -16, -8), (19, 0, 10, 6), (20, 0, 0, 0), (32, 0, 0, 0), (33, 0, 0, 30), (34, 0, 0, -30),
      (35, 0, 0, 20), (36, 0, 0, 0))
a.rot("arm_l", (0, *rest("arm_l")), (6, 0, 0, -30), (10, -20, 0, -46), (22, -10, 0, -60), (25, 30, 0, -40), (32, 10, 0, -20), (40, *rest("arm_l")))
a.rot("blade", (0, *rest("blade")), (10, 30, 0, -30), (22, 30, 0, -40), (25, 0, 0, -10), (40, *rest("blade")))
a.rot("chest", (0, 0, 0, 0), (6, 4, -26, 0), (10, -8, 20, 0), (17, 10, 16, 0), (22, 14, 14, 0), (25, -18, 10, 0), (30, -12, 6, 0), (40, 0, 0, 0))
a.rot("body", (0, 0, 0, 0), (6, 0, -14, 0), (10, -10, 10, 0), (22, 6, 10, 0), (25, -24, 6, 0), (30, -18, 4, 0), (40, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (6, 0, -0.8, 0.6), (10, 0, -1.4, -1.2), (22, 0, 0, -0.6), (25, 0, -2.8, -1.2), (30, 0, -2.4, -1.0), (40, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (6, 0, -20, 0), (10, -6, 16, 0), (17, 20, 14, 10), (22, 26, 10, -8), (25, -14, 10, 0), (30, -6, 0, 10), (36, 4, 0, -8), (40, 0, 0, 0))
a.rot("leg_r", (0, 0, 0, 0), (10, -30, 0, 6), (22, -20, 0, 6), (25, -36, 0, 8), (32, -20, 0, 4), (40, 0, 0, 0))
a.rot("leg_l", (0, 0, 0, 0), (10, 30, 0, -6), (22, 20, 0, -4), (25, 40, 0, -8), (32, 24, 0, -4), (40, 0, 0, 0))
a.rot("shin_l", (0, 0, 0, 0), (10, -30, 0, 0), (25, -50, 0, 0), (32, -30, 0, 0), (40, 0, 0, 0))
a.rot("shin_r", (0, 0, 0, 0), (25, -16, 0, 0), (40, 0, 0, 0))
a.hair([(0, 0, 0, 0), (6, 6, 0, -10), (10, -14, 0, 10), (17, 8, 0, 6), (22, 14, 0, 4), (25, -30, 0, 0), (29, -16, 0, 6), (36, 0, 0, -4), (40, 0, 0, 0)])
a.skirt([(0, 0, 0, 0), (10, 10, 0, -8), (22, -4, 0, -4), (25, 24, 0, 16), (30, 14, 0, 10), (40, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ slice_flurry (36): forehand 9, backhand 13, forehand 17, backhand 21, overhead wind 24, X-cut 27 (blade + claws cross)
a = A("slice_flurry", 36)
FH, BH = (86, -36, -18), (70, 36, -82)
a.rot("arm_l", (0, *rest("arm_l")), (6, *BH), (9, *FH), (11, 82, -40, -12), (13, *BH), (15, 66, 38, -84), (17, *FH), (19, 82, -40, -12), (21, *BH),
      (24, 176, 10, -24), (27, 46, -24, 6), (30, 40, -24, 8), (36, *rest("arm_l")))
a.rot("fore_l", (0, *rest("fore_l")), (6, 10, 0, 0), (21, 10, 0, 0), (24, 30, 0, 0), (27, 0, 0, 0), (36, *rest("fore_l")))
a.rot("blade", (0, *rest("blade")), (6, 90, 0, 20), (9, 92, 0, -24), (13, 92, 0, 24), (17, 92, 0, -24), (21, 92, 0, 24), (24, 110, 0, 0), (27, 70, 0, -30),
      (31, 60, 0, -30), (36, *rest("blade")))
a.rot("arm_r", (0, *rest("arm_r")), (6, 30, 0, 50), (21, 30, 0, 50), (24, 160, 0, 40), (27, 50, 0, -36), (30, 44, 0, -36), (36, *rest("arm_r")))
a.rot("claws_r", (0, 12, 0, 0), (21, 30, 0, 0), (24, -30, 0, 0), (27, 60, 0, 0), (36, 12, 0, 0))
a.rot("chest", (0, 0, 0, 0), (6, -4, 24, 0), (9, -8, -22, 0), (13, -8, 22, 0), (17, -8, -22, 0), (21, -8, 22, 0), (24, 14, 0, 0), (27, -18, 0, 0), (31, -14, 0, 0), (36, 0, 0, 0))
a.rot("body", (0, 0, 0, 0), (6, -6, 10, 0), (9, -10, -10, 0), (13, -10, 10, 0), (17, -10, -10, 0), (21, -10, 10, 0), (24, 6, 0, 0), (27, -20, 0, 0), (36, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (9, 0, -1.4, -0.6), (17, 0, -1.4, -1.0), (24, 0, 0.2, 0), (27, 0, -2.6, -1.6), (31, 0, -2.4, -1.4), (36, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (6, 0, -20, 0), (9, -4, 16, 0), (13, -4, -16, 0), (17, -4, 16, 0), (21, -4, -16, 0), (24, 20, 0, 0), (27, -10, 0, 0), (32, 0, 0, 8), (36, 0, 0, 0))
a.rot("leg_r", (0, 0, 0, 0), (9, -20, 0, 4), (13, 10, 0, 4), (17, -24, 0, 4), (21, 10, 0, 4), (27, -34, 0, 6), (32, -20, 0, 4), (36, 0, 0, 0))
a.rot("leg_l", (0, 0, 0, 0), (9, 20, 0, -4), (13, -10, 0, -4), (17, 24, 0, -4), (21, -10, 0, -4), (27, 44, 0, -6), (32, 30, 0, -4), (36, 0, 0, 0))
a.rot("shin_l", (0, 0, 0, 0), (9, -24, 0, 0), (13, -10, 0, 0), (17, -24, 0, 0), (21, -10, 0, 0), (27, -50, 0, 0), (32, -30, 0, 0), (36, 0, 0, 0))
a.rot("shin_r", (0, 0, 0, 0), (13, -24, 0, 0), (21, -24, 0, 0), (27, -10, 0, 0), (36, 0, 0, 0))
a.hair([(0, 0, 0, 0), (6, 4, 0, 12), (9, -6, 0, -14), (13, -6, 0, 14), (17, -6, 0, -14), (21, -6, 0, 14), (24, 14, 0, 0), (27, -26, 0, 0), (31, -16, 0, 0), (36, 0, 0, 0)], delay=1)
a.skirt([(0, 0, 0, 0), (9, 6, 0, 14), (13, 6, 0, -14), (17, 6, 0, 14), (21, 6, 0, -14), (27, 22, 0, 6), (32, 10, 0, 2), (36, 0, 0, 0)], delay=1)
a.done()

# ------------------------------------------------------------------ pirouette_cut (40): wind-up 6, three ballet spins with the blade held flat out (slashes 10/17/24), final forward cut 31
a = A("pirouette_cut", 40)
a.rot("root", (0, 0, 0, 0), (6, 0, 34, 0), (10, 0, -170, 0), (14, 0, -360, 0), (17, 0, -530, 0), (21, 0, -720, 0), (24, 0, -890, 0), (28, 0, -1080, 0), (40, 0, -1080, 0))
a.pos("root", (0, 0, 0, 0), (8, 0, 0.8, 0), (28, 0, 0.8, 0), (30, 0, 0, 0), (40, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (6, 0, -2.0, 0), (9, 0, 0.4, 0), (28, 0, 0.4, 0), (31, 0, -2.6, -1.4), (35, 0, -2.2, -1.0), (40, 0, 0, 0))
a.rot("body", (0, 0, 0, 0), (6, -10, 0, 0), (10, 0, 0, -8), (28, 0, 0, -10), (31, -22, -14, 0), (35, -18, -12, 0), (40, 0, 0, 0))
a.rot("chest", (0, 0, 0, 0), (6, 0, 30, 0), (10, 4, -10, 0), (28, 4, -10, 0), (29, 4, 30, 0), (31, -14, -30, 0), (35, -10, -26, 0), (40, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (6, 0, -30, 0), (10, 16, 20, 8), (28, 16, 20, 8), (31, -4, 26, 0), (36, 0, 10, 8), (40, 0, 0, 0))
a.rot("arm_l", (0, *rest("arm_l")), (6, -20, 30, -60), (10, 86, 0, -88), (28, 86, 0, -88), (29, 60, 40, -80), (31, 80, -30, -16), (35, 70, -40, 10), (40, *rest("arm_l")))
a.rot("fore_l", (0, *rest("fore_l")), (6, 30, 0, 0), (10, 0, 0, 0), (35, 0, 0, 0), (40, *rest("fore_l")))
a.rot("blade", (0, *rest("blade")), (6, 70, 0, 30), (10, 90, 0, -20), (28, 90, 0, -20), (29, 90, 0, 30), (31, 90, 0, -30), (36, 70, 0, -20), (40, *rest("blade")))
a.rot("arm_r", (0, *rest("arm_r")), (6, 30, 0, 50), (10, 10, 0, 100), (28, 10, 0, 100), (31, -20, 0, 60), (40, *rest("arm_r")))
a.rot("claws_r", (0, 12, 0, 0), (10, -20, 0, 0), (28, -20, 0, 0), (31, 40, 0, 0), (40, 12, 0, 0))
a.rot("leg_r", (0, 0, 0, 0), (6, 30, 0, 6), (9, 0, 0, 2), (28, 0, 0, 2), (31, -30, 0, 6), (36, -20, 0, 4), (40, 0, 0, 0))
a.rot("shin_r", (0, 0, 0, 0), (6, -50, 0, 0), (9, 0, 0, 0), (28, 0, 0, 0), (31, -16, 0, 0), (40, 0, 0, 0))
a.rot("foot_r", (0, 0, 0, 0), (9, -30, 0, 0), (28, -30, 0, 0), (31, 0, 0, 0))
a.rot("leg_l", (0, 0, 0, 0), (6, 30, 0, -6), (10, 40, 0, -36), (28, 40, 0, -36), (31, 46, 0, -8), (36, 30, 0, -4), (40, 0, 0, 0))
a.rot("shin_l", (0, 0, 0, 0), (6, -50, 0, 0), (10, -90, 0, 0), (28, -90, 0, 0), (31, -50, 0, 0), (36, -30, 0, 0), (40, 0, 0, 0))
a.hair([(0, 0, 0, 0), (6, 6, 0, 14), (10, -10, 0, -36), (28, -12, 0, -40), (31, -20, 0, 10), (35, -10, 0, 6), (40, 0, 0, 0)])
a.skirt([(0, 0, 0, 0), (6, 6, 0, 0), (10, 10, 0, 40), (28, 10, 0, 44), (31, 20, 0, 10), (36, 6, 0, 4), (40, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ pounce (42): deep coil 8, LEAP 12, tucked in the air with the blade raised 16-23, blade-first landing 27, wrench free 34
a = A("pounce", 42)
a.pos("body", (0, 0, 0, 0), (8, 0, -4.6, 1.0), (11, 0, -4.8, 1.2), (12, 0, 0.4, -0.4), (16, 0, 0.6, 0), (23, 0, 0, 0), (27, 0, -4.6, -1.2), (32, 0, -4.4, -1.0),
      (36, 0, -2.0, 0), (42, 0, 0, 0))
a.rot("body", (0, 0, 0, 0), (8, -30, 0, 0), (12, -10, 0, 0), (16, 10, 0, 0), (23, 6, 0, 0), (27, -34, 0, 0), (32, -30, 0, 0), (36, -6, 0, 0), (42, 0, 0, 0))
a.rot("chest", (0, 0, 0, 0), (8, -6, 0, 0), (16, 14, 0, 0), (23, 16, 0, 0), (27, -20, 0, 0), (32, -16, 0, 0), (35, 10, 0, 0), (42, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (8, 34, 0, 0), (12, 20, 0, 0), (16, -10, 0, 0), (23, -20, 0, 0), (27, 20, 0, 0), (32, 14, 0, 10), (36, 0, 0, -6), (42, 0, 0, 0))
a.rot("arm_l", (0, *rest("arm_l")), (8, -50, 0, -20), (12, 60, 0, -10), (16, 180, 0, -6), (23, 196, 0, -4), (25, 120, 0, -2), (27, 44, 0, 0), (32, 42, 0, 0),
      (34, 70, 0, -6), (36, 40, 0, -10), (42, *rest("arm_l")))
a.rot("fore_l", (0, *rest("fore_l")), (8, 40, 0, 0), (16, 20, 0, 0), (23, 30, 0, 0), (27, 20, 0, 0), (32, 20, 0, 0), (42, *rest("fore_l")))
a.rot("blade", (0, *rest("blade")), (8, 60, 0, 0), (16, 110, 0, 0), (23, 120, 0, 0), (27, 24, 0, 0), (32, 24, 0, 0), (34, 50, 0, 0), (42, *rest("blade")))
a.rot("arm_r", (0, *rest("arm_r")), (8, -50, 0, 30), (12, 40, 0, 30), (16, 130, 0, 50), (23, 140, 0, 60), (27, -20, 0, 70), (32, -10, 0, 60), (42, *rest("arm_r")))
a.rot("claws_r", (0, 12, 0, 0), (12, -30, 0, 0), (23, -30, 0, 0), (27, 50, 0, 0), (42, 12, 0, 0))
legs_both(a, [(0, 0, 0, 0), (8, 60, 0, 8), (11, 62, 0, 8), (12, -16, 0, 4), (16, 70, 0, 10), (23, 76, 0, 10), (27, 60, 0, 14), (32, 58, 0, 14), (36, 20, 0, 4), (42, 0, 0, 0)],
          [(0, 0, 0, 0), (8, -110, 0, 0), (11, -112, 0, 0), (12, 0, 0, 0), (16, -110, 0, 0), (23, -100, 0, 0), (27, -100, 0, 0), (32, -96, 0, 0), (36, -30, 0, 0), (42, 0, 0, 0)],
          [(0, 0, 0, 0), (8, 46, 0, 0), (12, -40, 0, 0), (16, -10, 0, 0), (27, 40, 0, 0), (36, 10, 0, 0), (42, 0, 0, 0)])
a.hair([(0, 0, 0, 0), (8, 10, 0, 0), (12, 34, 0, 0), (16, 20, 0, 0), (21, -20, 0, 0), (27, 40, 0, 0), (30, -10, 0, 0), (36, 0, 0, 4), (42, 0, 0, 0)])
a.skirt([(0, 0, 0, 0), (8, 14, 0, 10), (12, -24, 0, 0), (18, -30, 0, 20), (24, -20, 0, 10), (27, 30, 0, 30), (32, 20, 0, 24), (38, 4, 0, 4), (42, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ massacre_dance (52, enraged): three spinning slashes 12/20/28, wind up 32, hop 34, raised blade, PLUNGE 40, laugh
a = A("massacre_dance", 52)
a.rot("root", (0, 0, 0, 0), (8, 0, 40, 0), (12, 0, -100, 0), (16, 0, -200, 0), (20, 0, -340, 0), (24, 0, -440, 0), (28, 0, -580, 0), (32, 0, -700, 0),
      (34, 0, -720, 0), (52, 0, -720, 0))
a.pos("root", (0, 0, 0, 0), (20, 0, 1.2, 0), (24, 0, 0, 0), (28, 0, 1.6, 0), (32, 0, 0, 0), (52, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (8, 0, -2, 0), (12, 0, -1.2, 0), (31, 0, -1.2, 0), (33, 0, -3.4, 0.6), (35, 0, 0.6, 0), (38, 0, 0.4, 0), (40, 0, -4.6, -1.2),
      (45, 0, -4.4, -1.0), (52, 0, 0, 0))
a.rot("body", (0, 0, 0, 0), (8, -10, 0, 0), (12, -8, 0, -10), (20, -8, 0, -14), (28, -8, 0, -16), (33, -24, 0, 0), (36, 10, 0, 0), (40, -34, 0, 0), (45, -30, 0, 0),
      (48, -10, 0, 0), (52, 0, 0, 0))
a.rot("chest", (0, 0, 0, 0), (33, -10, 0, 0), (36, 16, 0, 0), (40, -20, 0, 0), (45, -16, 0, 0), (48, 10, 0, 0), (52, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (8, -10, 30, 0), (12, -6, 0, 0), (31, -6, 0, 0), (33, 26, 0, 0), (36, -16, 0, 0), (40, 24, 0, 0), (44, 30, 0, -12), (47, 30, 0, 12),
      (50, 20, 0, -6), (52, 0, 0, 0))
a.rot("arm_l", (0, *rest("arm_l")), (8, 40, 0, -40), (12, 90, 0, -90), (31, 90, 0, -90), (33, -40, 0, -30), (35, 170, 0, -6), (38, 196, 0, -4), (39, 120, 0, -2),
      (40, 44, 0, 0), (45, 42, 0, 0), (47, 70, 0, -6), (52, *rest("arm_l")))
a.rot("fore_l", (0, *rest("fore_l")), (12, 0, 0, 0), (31, 0, 0, 0), (33, 50, 0, 0), (36, 20, 0, 0), (40, 20, 0, 0), (52, *rest("fore_l")))
a.rot("blade", (0, *rest("blade")), (8, 60, 0, 0), (12, 90, 0, -20), (31, 90, 0, -20), (33, 60, 0, 0), (36, 110, 0, 0), (38, 120, 0, 0), (40, 24, 0, 0),
      (45, 24, 0, 0), (47, 50, 0, 0), (52, *rest("blade")))
a.rot("arm_r", (0, *rest("arm_r")), (8, 40, 0, 40), (12, 20, 0, 90), (31, 20, 0, 90), (33, -40, 0, 30), (36, 140, 0, 50), (38, 150, 0, 60), (40, -20, 0, 70),
      (45, -10, 0, 60), (52, *rest("arm_r")))
a.rot("claws_r", (0, 12, 0, 0), (12, -20, 0, 0), (33, 40, 0, 0), (36, -30, 0, 0), (40, 50, 0, 0), (52, 12, 0, 0))
legs_both(a, [(0, 0, 0, 0), (8, 20, 0, 8), (12, 0, 0, 14), (31, 0, 0, 14), (33, 50, 0, 8), (35, -10, 0, 4), (37, 70, 0, 10), (40, 60, 0, 14), (45, 58, 0, 14),
              (49, 20, 0, 4), (52, 0, 0, 0)],
          [(0, 0, 0, 0), (8, -40, 0, 0), (12, -10, 0, 0), (31, -10, 0, 0), (33, -90, 0, 0), (35, 0, 0, 0), (37, -110, 0, 0), (40, -100, 0, 0), (45, -96, 0, 0),
           (49, -30, 0, 0), (52, 0, 0, 0)],
          [(0, 0, 0, 0), (33, 30, 0, 0), (35, -30, 0, 0), (40, 40, 0, 0), (49, 0, 0, 0)])
a.rot("leg_l", (14, 0, 0, -14), (18, 40, 0, -30), (22, 0, 0, -14), (26, 40, 0, -30), (30, 0, 0, -14))
a.hair([(0, 0, 0, 0), (8, 6, 0, 10), (12, -16, 0, -40), (31, -16, 0, -44), (33, 10, 0, 0), (36, 30, 0, 0), (39, -20, 0, 0), (40, 44, 0, 0), (43, -10, 0, 8),
        (47, 6, 0, -8), (52, 0, 0, 0)])
a.skirt([(0, 0, 0, 0), (8, 6, 0, 0), (12, 12, 0, 40), (31, 12, 0, 44), (34, -20, 0, 10), (38, -26, 0, 16), (40, 30, 0, 34), (46, 12, 0, 12), (52, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ frenzy_chase (60, enraged): three dash-cuts (dash 10/26/42 -> cut 14/30/46): diagonal down, rising backhand, ankle sweep; cackle
a = A("frenzy_chase", 60)
body_p, body_r, chest_r, head_r = [(0, 0, 0, 0)], [(0, 0, 0, 0)], [(0, 0, 0, 0)], [(0, 0, 0, 0)]
arm_l, blade, arm_r, fore_l = [(0, *rest("arm_l"))], [(0, *rest("blade"))], [(0, *rest("arm_r"))], [(0, *rest("fore_l"))]
leg_r, leg_l, shin_r, shin_l = [(0, 0, 0, 0)], [(0, 0, 0, 0)], [(0, 0, 0, 0)], [(0, 0, 0, 0)]
hair, skirt = [(0, 0, 0, 0)], [(0, 0, 0, 0)]
CUT = [  # (wind arm_l, wind blade, strike arm_l, strike blade, crouch)
    ((170, 30, -50), (100, 0, 20), (40, -30, 14), (60, 0, -30), -1.4),
    ((30, -40, 14), (90, 0, -30), (150, 36, -70), (100, 0, 30), -1.4),
    ((-20, 40, -70), (90, 0, 40), (60, -30, -30), (100, 0, -30), -4.4),
]
for i, b in enumerate((0, 16, 32)):
    w_arm, w_bl, s_arm, s_bl, cr = CUT[i]
    body_p += [(b + 6, 0, -2.4, 0.8), (b + 10, 0, -1.2, -1.4), (b + 14, 0, cr, -2.0), (b + 18, 0, cr * 0.8, -1.4)]
    body_r += [(b + 6, -22, 10, 0), (b + 10, -38, 0, 0), (b + 14, -30 if i < 2 else -36, -14, 0), (b + 18, -24, -10, 0)]
    chest_r += [(b + 6, -4, 26, 0), (b + 10, -6, 20, 0), (b + 14, -14, -28, 0), (b + 18, -10, -22, 0)]
    head_r += [(b + 6, 30, -16, 0), (b + 10, 40, -10, 0), (b + 14, 30, 24, 0), (b + 18, 24, 20, -6)]
    arm_l += [(b + 6, *w_arm), (b + 11, *w_arm), (b + 14, *s_arm), (b + 18, *[v * 0.9 for v in s_arm])]
    blade += [(b + 6, *w_bl), (b + 11, *w_bl), (b + 14, *s_bl), (b + 18, *s_bl)]
    fore_l += [(b + 6, 20, 0, 0), (b + 14, 0, 0, 0)]
    arm_r += [(b + 6, -40, 0, 30), (b + 10, 50, 0, 20), (b + 14, -30, 0, 60), (b + 18, -10, 0, 40)]
    leg_l += [(b + 6, 40, 0, -4), (b + 10, -40, 0, -4), (b + 12, 50, 0, -4), (b + 14, 60 if i == 2 else 46, 0, -8), (b + 18, 40, 0, -6)]
    leg_r += [(b + 6, -10, 0, 4), (b + 10, 50, 0, 4), (b + 12, -40, 0, 4), (b + 14, -36, 0, 8), (b + 18, -26, 0, 6)]
    shin_l += [(b + 6, -60, 0, 0), (b + 10, -20, 0, 0), (b + 12, -60, 0, 0), (b + 14, -90 if i == 2 else -50, 0, 0), (b + 18, -40, 0, 0)]
    shin_r += [(b + 6, -20, 0, 0), (b + 10, -70, 0, 0), (b + 12, -10, 0, 0), (b + 14, -16, 0, 0), (b + 18, -10, 0, 0)]
    hair += [(b + 6, 10, 0, 10), (b + 10, 34, 0, 0), (b + 14, -20, 0, -20 if i != 1 else 20), (b + 18, -12, 0, -10 if i != 1 else 10)]
    skirt += [(b + 6, 10, 0, -6), (b + 10, -20, 0, 4), (b + 14, 24, 0, 20 if i != 1 else -20), (b + 18, 14, 0, 10)]
# cackle + recover
body_p += [(54, 0, 0, 0), (60, 0, 0, 0)]
body_r += [(52, 6, 0, 0), (54, 10, 0, 0), (60, 0, 0, 0)]
chest_r += [(52, 10, 0, 0), (54, 16, 0, 0), (56, 12, 0, 0), (60, 0, 0, 0)]
head_r += [(52, 30, 0, 8), (54, 36, 0, -8), (56, 30, 0, 8), (58, 20, 0, 0), (60, 0, 0, 0)]
arm_l += [(54, 20, 0, -20), (60, rest("arm_l")[0], rest("arm_l")[1], rest("arm_l")[2])]
blade += [(54, 30, 0, -16), (60, *rest("blade"))]
fore_l += [(60, *rest("fore_l"))]
arm_r += [(54, 20, 0, 30), (60, *rest("arm_r"))]
for L in (leg_l, leg_r, shin_l, shin_r): L += [(56, 0, 0, 0), (60, 0, 0, 0)]
hair += [(52, 10, 0, 6), (54, -6, 0, -6), (56, 6, 0, 6), (60, 0, 0, 0)]
skirt += [(54, 4, 0, 0), (60, 0, 0, 0)]
a.pos("body", *body_p); a.rot("body", *body_r); a.rot("chest", *chest_r); a.rot("head", *head_r)
a.rot("arm_l", *arm_l); a.rot("blade", *blade); a.rot("arm_r", *arm_r); a.rot("fore_l", *fore_l)
a.rot("leg_l", *leg_l); a.rot("leg_r", *leg_r); a.rot("shin_l", *shin_l); a.rot("shin_r", *shin_r)
a.rot("claws_r", (0, 12, 0, 0), (10, -30, 0, 0), (14, 40, 0, 0), (26, -30, 0, 0), (30, 40, 0, 0), (42, -30, 0, 0), (46, 40, 0, 0), (60, 12, 0, 0))
a.hair(hair, delay=1)
a.skirt(skirt, delay=1)
a.done()

# ------------------------------------------------------------------ death (40): struck 0-4 (recoil), blade slips from her fingers 10, knees buckle 16, topple sideways 22-30, settle
a = A("death", 40)
a.rot("chest", (0, 0, 0, 0), (3, 22, 0, 6), (8, 10, 0, 4), (14, -20, 0, 0), (22, -10, 0, 10), (40, -6, 0, 10))
a.rot("head", (0, 0, 0, 0), (3, 30, 0, -10), (8, 10, 0, 0), (14, -34, 0, 10), (22, -20, 0, 20), (30, 10, 0, 24), (40, 6, 0, 30))
a.rot("arm_r", (0, *rest("arm_r")), (3, 40, 0, 50), (8, 20, 0, 30), (14, 0, 0, 10), (22, 140, 0, 60), (28, 120, 0, 80), (34, 70, 0, 90), (40, 60, 0, 90))
a.rot("claws_r", (0, 12, 0, 0), (3, -30, 0, 0), (14, 40, 0, 0), (40, 30, 0, 0))
a.rot("arm_l", (0, *rest("arm_l")), (3, 30, 0, -50), (8, 10, 0, -20), (14, 0, 0, -6), (22, 140, 0, -60), (28, 120, 0, -80), (34, 40, 0, -40), (40, 30, 0, -30))
a.rot("hand_l", (0, 0, 0, 0), (8, 0, 0, 0), (10, 0, 0, -30), (40, 0, 0, -30))
a.rot("blade", (0, *rest("blade")), (8, 12, 0, -16), (10, 30, 0, -40), (14, 80, 0, -80), (18, 90, 0, -90), (40, 90, 0, -90))
a.pos("blade", (0, 0, 0, 0), (9, 0, 0, 0), (12, 0, -4, 0), (16, 0, -10, -1), (18, 0, -11, -1), (40, 0, -11, -1))
a.pos("body", (0, 0, 0, 0), (3, 0, 0.4, 1.0), (14, 0, -5.0, 0), (20, 0, -5.2, 0), (40, 0, -5.2, 0))
a.rot("body", (0, 0, 0, 0), (3, 10, 0, 0), (14, -16, 0, 0), (20, -10, 0, 0), (40, -10, 0, 0))
legs_both(a, [(0, 0, 0, 0), (3, -10, 0, 2), (14, 80, 0, 8), (20, 84, 0, 8), (40, 70, 0, 6)],
          [(0, 0, 0, 0), (14, -120, 0, 0), (20, -124, 0, 0), (40, -110, 0, 0)], [(0, 0, 0, 0), (14, 40, 0, 0), (40, 30, 0, 0)])
a.rot("root", (0, 0, 0, 0), (20, 0, 0, 0), (24, 0, 10, -30), (28, 0, 20, -80), (31, 0, 20, -94), (34, 0, 20, -86), (40, 0, 20, -90))
a.pos("root", (0, 0, 0, 0), (20, 0, 0, 0), (28, 0, 1.4, 0), (40, 0, 1.4, 0))
a.hair([(0, 0, 0, 0), (3, -24, 0, 10), (8, 4, 0, 0), (14, 20, 0, 0), (24, -20, 0, 30), (30, 10, 0, 56), (34, 4, 0, 50), (40, 6, 0, 54)])
a.skirt([(0, 0, 0, 0), (3, -10, 0, 0), (14, 20, 0, 20), (24, 26, 0, 30), (30, 10, 0, 34), (40, 10, 0, 30)])
a.done()

os.makedirs(os.path.dirname(OUT), exist_ok=True)
m.save(OUT)
print("cubes", len(m.cubes), "anims", [x["name"] for x in m.anims], "atlas rows used", m.cy + m.rowh)
