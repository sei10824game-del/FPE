"""Miss Circle (normal teacher, black-and-white) - generates assets/fpe/bbmodels/miss_circle.bbmodel.
Reference: docs/ref/confirmed/miss_circle.jpg - huge spiky near-black hair (to the boots, fanning far out to both sides,
two wolf-ear spikes on top), pale grey face half hidden by a bang, one white eye + shark-tooth grin, dark top with a lapel and
teal buttons, short puffy sleeves, grey skin, big black clawed right hand, black gauntlet with a teal stud on the left
forearm holding a GIANT steel COMPASS (needle leg + pencil leg), loose white trousers with rolled cuffs, black boots with
three grey stripes and pointed toes.
Blockbench space: Y up, ground 0, faces -Z. Character's RIGHT = +X.
Rotation sign cheat-sheet (file values): arm/leg rx>0 = swing forward, torso/head rx>0 = lean back / look up,
ry>0 = turn to the character's left, rz>0 = hanging part swings toward +X (character's right).
Compass ("comp", child of hand_l): legs point FORWARD (-Z) at rot 0; comp rx=-90 = blade continues the forearm line.
Run: python3 tools/bbgen/chars/miss_circle.py
"""
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from bbgen import Model, mix  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "../../../src/main/resources/assets/fpe/bbmodels/miss_circle.bbmodel")

# ------------------------------------------------------------------ palette (reference is a 3-tone ink drawing)
DARK, DARK_D, DARK_HI = 0x3A3247, 0x221D2A, 0x554B66
LINE = 0x8E889E                     # light ink lines drawn inside the black shapes
SKIN, SKIN_D, SKIN_L = 0xC8CBD3, 0x8F94A2, 0xDADCE2
PANT, PANT_D, PANT_L = 0xE4E4DF, 0xA9ADB2, 0xF5F5F1
TEAL, TEAL_D = 0x8CA8A8, 0x5C7678
STEEL, STEEL_D, STEEL_L = 0xD9DBD7, 0x8F949B, 0xF3F4F1
STRIPE = 0x98A4AA
GRAPH = 0x23202A
WOOD = 0xE9E2CF
MOUTH, TEETH = 0x1A1520, 0xF4F4F2
EYE = 0xF7F7FA

m = Model("miss_circle", S=8, atlas=2048)
R = m.rng


# ------------------------------------------------------------------ painters
def all_faces(fn, skip=()):
    return {k: fn for k in ("north", "south", "east", "west", "up", "down") if k not in skip}


def combo(*fns):
    def f(F):
        for fn in fns: fn(F)
    return f


def strands(base=DARK, hi=DARK_HI, dark=DARK_D, ink=True):
    """black hair: streaks + darker roots + an occasional thin light ink line like the drawing."""
    def f(F):
        cols = [R.random() for _ in range(F.w)]
        for x in range(F.w):
            c = mix(base, hi, 0.35) if cols[x] > 0.93 else mix(base, dark, 0.35) if cols[x] < 0.12 else base
            for y in range(F.h):
                t = y / max(1, F.h - 1)
                F.px(x, y, mix(c, dark, 0.3 * abs(t - 0.35)))
        if ink and F.w >= 4 and F.h >= 10 and R.random() < 0.18:
            x = R.randint(1, F.w - 2)
            y0 = R.randint(0, F.h // 3)
            for y in range(y0, min(F.h, y0 + R.randint(F.h // 3, F.h // 2 + 2))):
                F.px(x + (y // 9) % 2, y, LINE)
    return f


def hstripe(c, y0, h):
    def f(F):
        F.rect(0, y0, F.w, h, c)
    return f


def edge_lines(c):
    def f(F):
        F.rect(0, 0, 1, F.h, c); F.rect(F.w - 1, 0, 1, F.h, c)
    return f


def folds(base, dark, light, n=3):
    def f(F):
        for i in range(n):
            x = int((i + 0.5) * F.w / n) + R.randint(-1, 1)
            for y in range(F.h):
                if R.random() < 0.85:
                    F.px(x, y, mix(base, dark, 0.45)); F.px(x + 1, y, mix(base, light, 0.5))
    return f


def face_front(F):
    W, H = F.w, F.h  # 45 x 45; texture left = her right (+X); her left half is under the bang
    for y in range(H):
        for x in range(W):
            F.px(x, y, mix(SKIN, SKIN_D, max(0, (16 - y) / 16) * 0.7 + (0.25 if y > 40 else 0)))
    # one visible eye: narrow, slanted up toward the temple, heavy dark upper lid
    F.poly([(4, 21), (16, 17), (19, 21), (8, 24)], EYE, glow=True)
    F.disc(13, 20.6, 1.9, GRAPH)
    F.px(12, 20, EYE, glow=True)
    F.line(3, 20, 19, 15.5, DARK_D, 1.6)
    F.line(14, 13.5, 21, 12.5, SKIN_D, 1)
    # huge shark grin under the eye, corners curling up to the cheek
    cx, hw = 19.0, 16.0
    def tb(x):
        u = (x + .5 - cx) / hw
        return 29.5 - 1.0 * (1 - u * u) - 6.5 * u * u, 39.5 - 10.5 * u * u
    for x in range(int(cx - hw), int(cx + hw) + 1):
        top, bot = tb(x)
        if bot <= top + 0.5: continue
        F.rect(x, int(top), 1, int(bot) - int(top) + 1, MOUTH)
    for i in range(8):
        x0 = cx - hw + 2 + i * 3.9
        top, bot = tb(x0 + 2)
        span = bot - top
        if span < 2: continue
        th = min(5.0, span * 0.55)
        F.poly([(x0, top), (x0 + 3.9, top), (x0 + 1.95, top + th)], TEETH)
        x1 = x0 + 1.9
        top2, bot2 = tb(x1 + 2)
        if bot2 - top2 > 2: F.poly([(x1, bot2 + 1), (x1 + 3.9, bot2 + 1), (x1 + 1.95, bot2 + 1 - min(4.5, (bot2 - top2) * 0.5))], TEETH)
    F.line(cx - hw - 1, 27, cx - hw + 2, 24.5, SKIN_D, 1)  # cheek crease
    F.line(22, 23, 21, 25, SKIN_D, 1)  # nose hint


def chest_front(F):
    W, H = F.w, F.h
    folds(DARK, DARK_D, DARK_HI, 2)(F)
    # lapel / collar flap on her right (texture left) + placket line
    F.poly([(2, 0), (W * 0.45, 0), (W * 0.36, H * 0.42), (W * 0.18, H * 0.30)], 0x8F95A3)
    F.line(2, 0, W * 0.18, H * 0.30, LINE, 1)
    F.line(W * 0.55, 0, W * 0.5, H, DARK_D, 1)
    for i, yy in enumerate((0.22, 0.5, 0.78)):  # teal buttons on her left
        F.disc(W * 0.66, H * yy, 2.3, TEAL_D); F.disc(W * 0.66 - 0.3, H * yy - 0.3, 1.6, TEAL)
    F.line(W * 0.15, H * 0.7, W * 0.3, H * 0.55, LINE, 1)  # little ink fold marks


def boot_paint(F):
    for k, yy in enumerate((0.42, 0.55, 0.68)):
        F.rect(0, int(F.h * yy), F.w, 3, STRIPE)
    F.rect(0, 0, F.w, 2, DARK_HI)


# ------------------------------------------------------------------ skeleton
m.group("root", (0, 0, 0))
m.group("body", (0, 16, 0), parent="root")
m.group("chest", (0, 19, 0), parent="body")
m.group("head", (0, 27.4, 0), parent="chest")
m.group("ear_r", (1.6, 33.6, 0.4), parent="head")
m.group("ear_l", (-1.4, 33.6, 0.4), parent="head")
m.group("bang", (-1.2, 32.4, -3.0), parent="head")
m.group("hair_b1", (0, 32.5, 2.8), parent="head")
m.group("hair_b2", (0, 22.0, 3.8), parent="hair_b1")
m.group("hair_b3", (0, 11.5, 4.4), parent="hair_b2")
for s, k in ((1, "r"), (-1, "l")):
    m.group("hair_" + k + "1", (3.0 * s, 32.0, 0.8), parent="head")
    m.group("hair_" + k + "2", (4.6 * s, 22.0, 1.2), parent="hair_" + k + "1")
    m.group("hair_" + k + "3", (5.6 * s, 12.0, 1.6), parent="hair_" + k + "2")
m.group("arm_r", (3.55, 25.4, 0), parent="chest")
m.group("fore_r", (3.55, 21.4, 0), parent="arm_r")
m.group("hand_r", (3.55, 17.9, 0), parent="fore_r")
m.group("claws_r", (3.55, 15.8, -0.1), parent="hand_r")
m.group("pencils", (3.55, 16.4, 0), parent="hand_r")
m.group("arm_l", (-3.55, 25.4, 0), parent="chest")
m.group("fore_l", (-3.55, 21.4, 0), parent="arm_l")
m.group("hand_l", (-3.55, 17.2, 0), parent="fore_l")
m.group("comp", (-3.55, 16.2, 0), parent="hand_l")
m.group("c_needle", (-3.2, 16.2, -1.6), parent="comp")
m.group("c_pencil", (-3.9, 16.2, -1.6), parent="comp")
for s, k in ((1, "r"), (-1, "l")):
    m.group("leg_" + k, (1.45 * s, 16, 0), parent="root")
    m.group("shin_" + k, (1.45 * s, 8.6, 0), parent="leg_" + k)
    m.group("foot_" + k, (1.45 * s, 1.1, 0), parent="shin_" + k)

# ------------------------------------------------------------------ legs: loose white trousers, rolled cuffs, striped boots
def outline(c, top=True, sides=True, bottom=False):
    def f(F):
        if sides: F.rect(0, 0, 1, F.h, c); F.rect(F.w - 1, 0, 1, F.h, c)
        if top: F.rect(0, 0, F.w, 1, c)
        if bottom: F.rect(0, F.h - 1, F.w, 1, c)
    return f


for s, k in ((1, "r"), (-1, "l")):
    x = 1.45 * s
    # loose trousers, slightly flared toward the knee, inner gap between the legs
    pf = combo(folds(PANT, PANT_D, PANT_L, 2), lambda F: F.line(F.w * 0.3, 0, F.w * 0.45, F.h, PANT_D, 1))
    m.cube("thigh_" + k, "leg_" + k, (x - 1.25, 12.0, -1.5), (x + 1.25, 16.2, 1.5), PANT, color2=mix(PANT, PANT_D, 0.35), grad=True,
           faces={"north": pf, "south": pf, "east": folds(PANT, PANT_D, PANT_L, 1), "west": folds(PANT, PANT_D, PANT_L, 1)})
    m.cube("knee_" + k, "leg_" + k, (x - 1.4, 8.4, -1.65), (x + 1.4, 12.2, 1.6), PANT, color2=PANT_D, grad=True,
           faces={"north": combo(folds(PANT, PANT_D, PANT_L, 2), lambda F: F.line(F.w * 0.2, F.h * 0.2, F.w * 0.7, F.h * 0.55, PANT_D, 1)),
                  "east": folds(PANT, PANT_D, PANT_L, 1), "west": folds(PANT, PANT_D, PANT_L, 1)})
    m.cube("seam_" + k, "leg_" + k, (x + 1.25 * s - 0.15, 9.0, -0.3), (x + 1.25 * s + 0.15, 15.8, 0.3), PANT_D, inflate=0.04)
    m.cube("crease_" + k, "leg_" + k, (x - 0.1, 9.0, -1.7), (x + 0.3, 14.5, -1.55), mix(PANT, PANT_D, 0.6), origin=(x, 12, -1.6), rot=(0, 0, 6 * s))
    m.cube("calf_" + k, "shin_" + k, (x - 1.3, 7.6, -1.45), (x + 1.3, 8.9, 1.45), PANT, color2=PANT_D, grad=True)
    # rolled cuffs: two fat bands
    m.cube("cuff_" + k, "shin_" + k, (x - 1.75, 6.9, -1.8), (x + 1.75, 7.9, 1.8), PANT_L, faces=all_faces(combo(hstripe(PANT_D, 0, 1), hstripe(PANT_D, 7, 1))))
    m.cube("cuff2_" + k, "shin_" + k, (x - 1.6, 6.1, -1.65), (x + 1.6, 7.0, 1.65), mix(PANT_L, PANT_D, 0.25), faces=all_faces(hstripe(PANT_D, 6, 1)))
    # bare grey shin between cuff and boot
    m.cube("ankle_" + k, "shin_" + k, (x - 0.8, 5.0, -0.8), (x + 0.8, 6.3, 0.8), SKIN_D, color2=SKIN, grad=True)
    m.cube("boot_" + k, "shin_" + k, (x - 1.15, 1.0, -1.25), (x + 1.15, 5.0, 1.25), DARK, color2=DARK_D, grad=True,
           faces={f: combo(boot_paint, outline(LINE, top=False)) for f in ("north", "south", "east", "west")})
    m.cube("bootlip_" + k, "shin_" + k, (x - 1.45, 4.6, -1.55), (x + 1.45, 5.6, 1.55), DARK, origin=(x, 5, 0), rot=(-6, 0, 0),
           faces={f: outline(LINE, sides=False, top=True) for f in ("north", "east", "west", "south")})
    m.cube("sole_" + k, "foot_" + k, (x - 1.3, 0, -2.8), (x + 1.3, 1.25, 1.4), DARK, faces={"down": lambda F: F.rect(0, 0, F.w, F.h, DARK_D), "north": hstripe(LINE, 0, 1),
           "east": hstripe(LINE, 0, 1), "west": hstripe(LINE, 0, 1)})
    m.cube("toe_" + k, "foot_" + k, (x - 0.8, 0, -4.6), (x + 0.8, 0.95, -2.7), DARK, origin=(x, 0, -2.8), rot=(-6, 0, 0), faces={"up": outline(LINE, top=False)})
    m.cube("toetip_" + k, "foot_" + k, (x - 0.35, 0, -6.0), (x + 0.35, 0.6, -4.4), DARK_D, origin=(x, 0, -4.5), rot=(-10, 0, 0))
    m.cube("heel_" + k, "foot_" + k, (x - 0.6, -0.01, 0.3), (x + 0.6, 1.0, 1.5), DARK_D)

# ------------------------------------------------------------------ hips + torso
m.cube("hips", "body", (-2.7, 15.4, -1.55), (2.7, 17.8, 1.55), PANT, color2=PANT_D, grad=True,
       faces={"north": lambda F: (F.rect(0, 0, F.w, 2, PANT_L), F.line(F.w * 0.6, 2, F.w * 0.7, F.h, PANT_D, 1))})
m.cube("fly", "body", (-0.15, 15.0, -1.7), (0.15, 17.4, -1.55), PANT_D)
m.cube("waist", "chest", (-2.3, 17.4, -1.4), (2.3, 20.6, 1.4), DARK, color2=DARK_D, grad=True, faces={"north": combo(folds(DARK, DARK_D, DARK_HI, 2), outline(LINE, top=False)),
       "east": outline(LINE, top=False), "west": outline(LINE, top=False)})
m.cube("hem", "chest", (-2.55, 17.0, -1.6), (2.55, 17.9, 1.6), DARK_D, faces={"north": hstripe(LINE, 0, 1)})
m.cube("torso", "chest", (-2.85, 20.3, -1.65), (2.85, 25.9, 1.65), DARK, color2=DARK_D, grad=True,
       faces={"north": combo(chest_front, outline(LINE, top=False)), "south": combo(folds(DARK, DARK_D, DARK_HI, 3), outline(LINE, top=False)),
              "east": outline(LINE, top=False), "west": outline(LINE, top=False)})
m.cube("bust", "chest", (-2.4, 21.6, -2.0), (2.4, 24.6, -1.5), DARK, faces={"north": lambda F: F.disc(F.w * 0.66, F.h * 0.5, 2.0, TEAL)})
m.cube("collar", "chest", (-1.9, 25.4, -1.85), (1.9, 26.9, 1.4), DARK_D, faces={"north": hstripe(LINE, 0, 1)})
m.cube("lapel", "chest", (0.3, 23.6, -2.05), (2.6, 26.6, -1.75), 0xB4B8C2, origin=(1.3, 26.6, -1.9), rot=(0, 0, -18))
m.cube("neck", "chest", (-0.8, 25.8, -0.8), (0.8, 27.6, 0.8), SKIN_D, color2=SKIN, grad=True)

# ------------------------------------------------------------------ head
m.cube("skull", "head", (-2.8, 27.4, -2.8), (2.8, 33.0, 2.8), SKIN, faces={"north": face_front, "up": lambda F: F.rect(0, 0, F.w, F.h, DARK_D)})
m.cube("jaw_l", "head", (-2.85, 27.4, -2.0), (-2.6, 29.0, 1.0), SKIN_D)
m.cube("crown", "head", (-3.2, 30.6, -3.15), (3.2, 34.4, 3.3), DARK, faces=all_faces(strands()))
m.cube("crown2", "head", (-2.6, 34.0, -2.2), (2.4, 35.2, 2.6), DARK, faces=all_faces(strands()))
m.cube("fringe", "head", (-3.25, 31.4, -3.45), (3.25, 33.2, -2.9), DARK, faces=all_faces(strands()))
# bangs over the forehead (spikes down), the right eye stays visible
for i, (x, ln, rz) in enumerate([(2.6, 2.0, 18), (1.6, 1.6, 8), (0.4, 3.4, -4)]):
    m.cube(f"bangtip{i}", "head", (x - 0.5, 31.6 - ln, -3.5), (x + 0.5, 31.6, -3.0), DARK, origin=(x, 31.6, -3.2), rot=(6, 0, rz),
           faces=all_faces(strands(ink=False)))
# big bang covering her left eye (own bone so it can flick)
m.cube("bang_main", "bang", (-3.3, 27.0, -3.55), (-0.9, 32.6, -3.0), DARK, origin=(-1.2, 32.4, -3.2), rot=(4, 0, -6), faces=all_faces(strands()))
m.cube("bang_tip", "bang", (-3.0, 24.8, -3.5), (-1.6, 27.4, -3.0), DARK, origin=(-2.3, 27.2, -3.2), rot=(6, 0, -18), faces=all_faces(strands(ink=False)))
m.cube("bang_tip2", "bang", (-1.2, 25.6, -3.45), (-0.3, 27.4, -3.05), DARK_D, origin=(-0.8, 27.2, -3.2), rot=(6, 0, 14))
# wolf-ear hair spikes (the right one wide, the left one tall and thin, like the drawing)
m.cube("ear_r0", "ear_r", (0.3, 33.4, -1.0), (3.0, 36.6, 1.6), DARK, origin=(1.6, 33.6, 0.4), rot=(0, 0, -10), faces=all_faces(strands()))
m.cube("ear_r1", "ear_r", (0.8, 36.2, -0.6), (2.6, 39.0, 1.2), DARK, origin=(1.7, 36.4, 0.4), rot=(0, 0, -16),
       faces={"north": lambda F: F.line(2, F.h - 1, F.w / 2, 2, LINE, 1)})
m.cube("ear_r2", "ear_r", (1.3, 38.6, -0.25), (2.3, 41.0, 0.8), DARK, origin=(1.8, 38.8, 0.3), rot=(0, 0, -24))
m.cube("ear_l0", "ear_l", (-2.6, 33.4, -0.6), (-0.4, 36.4, 1.4), DARK, origin=(-1.4, 33.6, 0.4), rot=(0, 0, 8), faces=all_faces(strands()))
m.cube("ear_l1", "ear_l", (-2.0, 36.0, -0.3), (-0.8, 39.6, 1.0), DARK, origin=(-1.4, 36.2, 0.4), rot=(0, 0, 12))
m.cube("ear_l2", "ear_l", (-1.75, 39.3, -0.05), (-1.05, 42.0, 0.7), DARK_D, origin=(-1.4, 39.4, 0.3), rot=(0, 0, 18),
       faces={"north": lambda F: F.rect(1, 0, 1, F.h, LINE)})
for i, (x, z, rz, rx) in enumerate([(2.6, 2.2, -50, -20), (-2.8, 2.2, 52, -20), (0.2, 2.8, 4, -40)]):
    m.cube(f"crown_spike{i}", "head", (x - 0.55, 33.4, z - 0.55), (x + 0.55, 36.6, z + 0.55), DARK, origin=(x, 33.6, z), rot=(rx, 0, rz))

# ------------------------------------------------------------------ hair: huge jagged mantle built from cut-out "cards" (flat, painted silhouettes
# like the ink drawing) layered over a few solid volume blocks
CLEAR = (0, 0, 0, 0)
CLEAR_UV = m._alloc(8, 8)  # atlas starts transparent


def inside(px, py, polys):
    hit = False
    for pts in polys:
        n, c = len(pts), False
        for i in range(n):
            (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % n]
            if (y1 > py) != (y2 > py) and px < x1 + (py - y1) * (x2 - x1) / (y2 - y1):
                c = not c
        hit = hit or c
    return hit


def card(name, parent, x0, x1, y0, y1, z, polys, d=0.0, origin=None, rot=(0, 0, 0)):
    """flat hair plate in the XY plane; polys in model (x, y) coords; outside = transparent (cutout)."""
    S = m.S

    def paint(fs):
        for f, F in fs.items():
            if f not in ("north", "south"):
                F.rect(0, 0, F.w, F.h, CLEAR); continue
            base = strands(ink=False)
            base(F)
            for j in range(F.h):
                for i in range(F.w):
                    mx = (x1 - (i + .5) / S) if f == "north" else (x0 + (i + .5) / S)
                    my = y1 - (j + .5) / S
                    if i < 2 or j < 2 or i >= F.w - 2 or j >= F.h - 2 or not inside(mx, my, polys):
                        F.px(i, j, CLEAR)
                    elif not inside(mx + 0.3, my, polys) or not inside(mx - 0.3, my, polys) or not inside(mx, my - 0.3, polys):
                        F.px(i, j, DARK_D)  # dark rim
    c = m.cube(name, parent, (x0, y0, z), (x1, y1, z + d), DARK, paint=paint, origin=origin, rot=rot)
    for f in ("north", "south"):  # inset 1 texel: edge sampling hits our own cleared border, never the atlas neighbour
        u0, v0, u1, v1 = c["faces"][f]["uv"]
        c["faces"][f]["uv"] = [u0 + 1, v0 + 1, u1 - 1, v1 - 1]
    for f in ("east", "west", "up", "down"):  # edges sample a padded fully transparent block (no bleeding lines)
        c["faces"][f]["uv"] = [CLEAR_UV[0] + 3, CLEAR_UV[1] + 3, CLEAR_UV[0] + 5, CLEAR_UV[1] + 5]


def side_spikes(xb, ytop, n, h, length, s, droop=0.8, jitter=0.45):
    out = []
    for i in range(n):
        ya = ytop - i * h
        ln = length * (1 - jitter + 2 * jitter * R.random())
        w = h * R.uniform(1.2, 1.9)
        out.append([(xb - s * 1.0, ya + 0.3), (xb + s * ln, ya - h * droop - ln * R.uniform(0.25, 0.7)), (xb - s * 1.0, ya - w)])
    return out


def bottom_spikes(xa, xb, yb, n, length):
    out, w = [], (xb - xa) / n
    for i in range(n):
        x = xa + i * w
        ln = length * (0.6 + 0.6 * R.random())
        out.append([(x - 0.2, yb + 1.0), (x + w + 0.2, yb + 1.0), (x + w * R.uniform(0.3, 0.7), yb - ln)])
    return out


# solid volume (gives the mantle thickness from the side)
m.cube("hb_main", "hair_b1", (-4.4, 21.6, 2.4), (4.4, 33.4, 5.0), DARK, faces=all_faces(strands()))
m.cube("hb_lower", "hair_b2", (-5.2, 11.2, 2.8), (5.2, 22.2, 5.4), DARK, faces=all_faces(strands()))
m.cube("hb_base", "hair_b3", (-5.6, 4.0, 3.2), (5.6, 11.8, 5.8), DARK, faces=all_faces(strands()))
for s, k in ((1, "r"), (-1, "l")):
    m.cube("hs_top_" + k, "hair_" + k + "1", (3.0 * s - 0.9, 22.0, -1.6), (3.0 * s + 0.9, 32.6, 3.6), DARK, faces=all_faces(strands()))
    m.cube("hs_mid_" + k, "hair_" + k + "2", (5.0 * s - 1.1, 12.0, 0.6), (5.0 * s + 1.1, 22.6, 4.4), DARK, faces=all_faces(strands()))
    m.cube("hs_low_" + k, "hair_" + k + "3", (6.0 * s - 1.0, 3.0, 1.0), (6.0 * s + 1.0, 12.6, 4.6), DARK, faces=all_faces(strands()))

# back cards: one per chain bone, wider going down; her right side (+X) flares further, like the drawing
core1 = [(-4.6, 34.2), (4.6, 34.2), (6.4, 28), (7.2, 21.0), (-7.0, 21.0), (-6.0, 28)]
p1 = [core1] + side_spikes(6.0, 32.0, 3, 3.6, 6.5, 1) + side_spikes(-5.8, 31.5, 3, 3.6, 4.8, -1)
card("hcard_b1", "hair_b1", -11, 12, 19.5, 35, 5.0, p1)
core2 = [(-7.0, 22.6), (7.4, 22.6), (8.8, 16), (9.0, 10.0), (-8.6, 10.0), (-8.0, 16)]
p2 = [core2] + side_spikes(8.2, 22.5, 4, 3.4, 7.5, 1) + side_spikes(-7.8, 22.0, 4, 3.4, 5.6, -1)
card("hcard_b2", "hair_b2", -14, 16, 7.5, 23, 5.4, p2)
core3 = [(-8.6, 12.0), (9.0, 12.0), (9.6, 6), (9.4, 2.0), (-8.8, 2.0), (-9.0, 6)]
p3 = [core3] + side_spikes(9.0, 12.0, 3, 3.4, 6.5, 1) + side_spikes(-8.6, 11.5, 3, 3.4, 5.0, -1) + bottom_spikes(-8.8, 9.4, 2.0, 6, 2.8)
card("hcard_b3", "hair_b3", -14, 16, -1.0, 12.5, 5.8, p3)
# side wing cards (just behind the arms) - fan of blades sweeping outward/down
for s, k in ((1, "r"), (-1, "l")):
    big = 1.2 if s > 0 else 1.0
    xa = 3.4 * s
    pw1 = [[(xa, 32.5), (xa + 2.4 * s, 31), (xa + 2.8 * s, 22), (xa, 22)]] + side_spikes(xa + 2.4 * s, 31, 4, 2.4, 4.0 * big, s, droop=0.9)
    card("hcard_" + k + "1", "hair_" + k + "1", min(xa, xa + 9 * s), max(xa, xa + 9 * s), 18.5, 33, 2.4, pw1)
    xb = 4.6 * s
    pw2 = [[(xb, 23), (xb + 3.0 * s, 22), (xb + 3.4 * s, 11.5), (xb, 11.5)]] + side_spikes(xb + 3.0 * s, 22, 4, 2.6, 4.6 * big, s, droop=1.0)
    card("hcard_" + k + "2", "hair_" + k + "2", min(xb, xb + 11 * s), max(xb, xb + 11 * s), 7.5, 23.2, 2.0, pw2)
    xc = 5.4 * s
    pw3 = [[(xc, 13), (xc + 3.0 * s, 12), (xc + 2.6 * s, 2.5), (xc, 1.5)]] + side_spikes(xc + 2.8 * s, 12, 4, 2.4, 4.2 * big, s, droop=1.1) \
        + [[(xc - 0.4 * s, 2.5), (xc + 1.6 * s, 2.5), (xc + 0.4 * s, -0.4)], [(xc + 1.2 * s, 3.0), (xc + 3.0 * s, 3.0), (xc + 2.6 * s, 0.2)]]
    card("hcard_" + k + "3", "hair_" + k + "3", min(xc, xc + 10 * s), max(xc, xc + 10 * s), -0.8, 13.2, 2.4, pw3)
# a few chunky 3D spikes so it does not look flat from the side
for i, (y, rx) in enumerate([(30, -40), (24, -34), (17, -30), (10, -26)]):
    bone = "hair_b1" if i < 2 else "hair_b2" if i < 3 else "hair_b3"
    m.cube(f"hb_spike{i}", bone, (-0.9 + (i % 2) * 1.6, y - 5.0, 4.6), (0.9 + (i % 2) * 1.6, y, 6.4), DARK, origin=(0, y, 5.2), rot=(rx, 0, (-1) ** i * 12),
           faces=all_faces(strands(ink=False)))
# the little white tick marks drawn on the hair (ink detail on the lower right wing)
m.cube("hair_mark", "hair_r3", (6.6, 8.0, 2.2), (7.9, 8.3, 2.75), LINE)
m.cube("hair_mark2", "hair_r3", (6.8, 7.2, 2.2), (8.1, 7.5, 2.75), LINE)

# ------------------------------------------------------------------ right arm: puffy sleeve, grey skin, BIG black clawed hand
m.cube("sleeve_r", "arm_r", (2.55, 22.2, -1.3), (4.75, 26.0, 1.3), DARK, color2=DARK_D, grad=True, faces={"north": folds(DARK, DARK_D, DARK_HI, 1)})
m.cube("sleevecuff_r", "arm_r", (2.5, 22.0, -1.35), (4.8, 22.6, 1.35), DARK_D, faces=all_faces(hstripe(LINE, 0, 1)))
m.cube("uarm_r", "arm_r", (3.0, 20.9, -0.6), (4.1, 22.4, 0.6), SKIN, color2=SKIN_D, grad=True)
m.cube("forearm_r", "fore_r", (3.0, 18.4, -0.6), (4.1, 21.5, 0.6), SKIN, color2=SKIN_D, grad=True)
m.cube("glove_r", "fore_r", (2.8, 17.6, -0.85), (4.3, 19.0, 0.85), DARK, faces=all_faces(hstripe(LINE, 0, 1)))
m.cube("palm_r", "hand_r", (2.35, 15.4, -1.25), (4.75, 18.0, 1.25), DARK, color2=DARK_D, grad=True,
       faces={"north": outline(LINE), "east": outline(LINE), "west": outline(LINE), "south": outline(LINE)})
m.cube("knuck_r", "hand_r", (2.3, 15.2, -1.4), (4.8, 15.9, 0.6), DARK_D, faces={"north": hstripe(LINE, 0, 1)})
m.cube("thumb_r", "hand_r", (1.9, 14.0, -1.5), (2.6, 16.8, -0.75), DARK, origin=(2.4, 16.8, -1.0), rot=(14, 0, -28), faces={"north": edge_lines(LINE)})
m.cube("thumbclaw_r", "hand_r", (1.95, 12.2, -1.45), (2.45, 14.2, -0.95), DARK_D, origin=(2.4, 16.8, -1.0), rot=(18, 0, -34),
       faces={"north": lambda F: F.rect(0, 0, 1, F.h, LINE)})
for i in range(4):
    x = 2.4 + i * 0.6
    ln = (3.6, 4.4, 4.2, 3.4)[i]
    m.cube(f"finger{i}_r", "claws_r", (x, 15.9 - ln, -0.95), (x + 0.52, 15.9, -0.3), DARK, origin=(x + 0.26, 15.8, -0.6), rot=(10, 0, (i - 1.5) * -5),
           faces={"north": edge_lines(LINE), "south": edge_lines(LINE)})
    m.cube(f"claw{i}_r", "claws_r", (x + 0.08, 15.9 - ln - 2.8, -0.9), (x + 0.44, 15.9 - ln + 0.2, -0.4), DARK_D, origin=(x + 0.26, 15.9 - ln, -0.65),
           rot=(24, 0, (i - 1.5) * -7), faces={"north": lambda F: F.rect(0, 0, 1, F.h, LINE), "east": lambda F: F.rect(0, 0, 1, F.h, LINE)})
# three pencils clenched between the claws like daggers (only visible in pencilStab)
for i in range(3):
    m.cube(f"pen{i}", "pencils", (3.25 + (i - 1) * 0.6, 14.5, -6.2), (3.85 + (i - 1) * 0.6, 15.1, 1.0), PANT_L, origin=(3.55, 14.8, -0.5), rot=(0, (i - 1) * 14, 0),
           faces={"west": hstripe(STRIPE, 1, 1), "east": hstripe(STRIPE, 1, 1)})
    m.cube(f"pentip{i}", "pencils", (3.4 + (i - 1) * 0.6, 14.65, -7.6), (3.7 + (i - 1) * 0.6, 14.95, -6.2), GRAPH, origin=(3.55, 14.8, -0.5), rot=(0, (i - 1) * 14, 0))

# ------------------------------------------------------------------ left arm: gauntlet with teal stud + GIANT COMPASS
m.cube("sleeve_l", "arm_l", (-4.75, 22.2, -1.3), (-2.55, 26.0, 1.3), DARK, color2=DARK_D, grad=True)
m.cube("sleevecuff_l", "arm_l", (-4.8, 22.0, -1.35), (-2.5, 22.6, 1.35), DARK_D, faces=all_faces(hstripe(LINE, 0, 1)))
m.cube("uarm_l", "arm_l", (-4.1, 20.9, -0.6), (-3.0, 22.4, 0.6), SKIN, color2=SKIN_D, grad=True)
m.cube("forearm_l", "fore_l", (-4.1, 19.4, -0.6), (-3.0, 21.5, 0.6), SKIN, color2=SKIN_D, grad=True)
m.cube("gauntlet", "fore_l", (-4.45, 16.8, -0.95), (-2.65, 19.8, 0.95), DARK, color2=DARK_D, grad=True,
       faces={"west": combo(hstripe(LINE, 0, 1), lambda F: F.disc(F.w / 2, F.h * 0.45, 2.2, TEAL)),
              "north": combo(hstripe(LINE, 0, 1), lambda F: F.disc(F.w / 2, F.h * 0.45, 1.6, TEAL)), "east": hstripe(LINE, 0, 1)})
m.cube("fist_l", "hand_l", (-4.3, 15.2, -1.0), (-2.8, 17.2, 1.0), DARK, color2=DARK_D, grad=True, faces={"north": edge_lines(LINE)})
# compass: hinge + handle pass through the fist, legs point forward (-Z)
m.cube("c_handle", "comp", (-3.95, 15.75, -1.2), (-3.15, 16.65, 2.2), STEEL_D, faces={"up": hstripe(STEEL_L, 0, 1)})
m.cube("c_knob", "comp", (-4.15, 15.55, 2.2), (-2.95, 16.85, 3.2), STEEL_L, faces={"south": lambda F: F.disc(F.w / 2, F.h / 2, 3, STEEL_D)})
m.cube("c_hinge", "comp", (-4.75, 15.0, -2.6), (-2.35, 17.4, -0.9), STEEL, color2=STEEL_D, grad=True,
       faces={"west": lambda F: F.disc(F.w / 2, F.h / 2, 5, STEEL_D), "east": lambda F: F.disc(F.w / 2, F.h / 2, 5, STEEL_D),
              "north": outline(STEEL_D)})
m.cube("c_screw", "comp", (-4.95, 15.75, -2.1), (-2.15, 16.65, -1.4), STEEL_L, faces={"west": lambda F: F.disc(F.w / 2, F.h / 2, 2, GRAPH)})
# needle leg (flat steel blade, long needle)
m.cube("cn_rod", "c_needle", (-3.35, 15.6, -13.0), (-2.35, 16.8, -2.0), STEEL, color2=STEEL_D, grad=True,
       faces={"up": combo(lambda F: F.rect(0, 0, 1, F.h, STEEL_L), lambda F: F.rect(F.w - 1, 0, 1, F.h, STEEL_D)),
              "east": combo(hstripe(STEEL_D, 0, 1), hstripe(STEEL_L, 3, 1)), "west": combo(hstripe(STEEL_D, 0, 1), hstripe(STEEL_L, 3, 1))})
m.cube("cn_groove", "c_needle", (-3.0, 16.8, -12.0), (-2.7, 16.9, -3.0), STEEL_D)
m.cube("cn_clamp", "c_needle", (-3.5, 15.45, -14.4), (-2.2, 16.95, -12.8), STEEL_D, faces=all_faces(hstripe(GRAPH, 0, 1)))
m.cube("cn_shaft", "c_needle", (-3.15, 15.8, -18.2), (-2.55, 16.6, -14.3), STEEL_L)
m.cube("cn_needle", "c_needle", (-2.98, 16.05, -22.6), (-2.72, 16.35, -18.1), STEEL_D)
m.cube("cn_tip", "c_needle", (-2.92, 16.12, -23.6), (-2.78, 16.28, -22.5), GRAPH)
# pencil leg (thick white pencil, black band near the top, sharpened wood + lead)
m.cube("cp_rod", "c_pencil", (-4.85, 15.6, -9.5), (-3.75, 16.8, -2.0), STEEL, color2=STEEL_D, grad=True,
       faces={"up": lambda F: F.rect(F.w - 1, 0, 1, F.h, STEEL_L), "east": hstripe(STEEL_D, 0, 1), "west": hstripe(STEEL_D, 0, 1)})
m.cube("cp_band", "c_pencil", (-5.15, 15.3, -12.6), (-3.45, 17.1, -9.4), GRAPH, faces=all_faces(combo(hstripe(STEEL_D, 0, 1), hstripe(STEEL_D, 13, 1))))
m.cube("cp_pencil", "c_pencil", (-5.0, 15.45, -19.4), (-3.6, 16.95, -12.5), PANT_L,
       faces={"up": combo(lambda F: F.rect(F.w // 2, 0, 1, F.h, PANT_D), lambda F: F.rect(0, 0, 1, F.h, PANT_D)),
              "west": lambda F: F.rect(0, F.h // 2, F.w, 1, PANT_D), "east": lambda F: F.rect(0, F.h // 2, F.w, 1, PANT_D),
              "down": lambda F: F.rect(F.w // 2, 0, 1, F.h, PANT_D)})
m.cube("cp_wood", "c_pencil", (-4.75, 15.7, -20.8), (-3.85, 16.7, -19.4), WOOD)
m.cube("cp_wood2", "c_pencil", (-4.55, 15.9, -21.7), (-4.05, 16.5, -20.7), WOOD)
m.cube("cp_lead", "c_pencil", (-4.42, 16.05, -22.6), (-4.18, 16.35, -21.6), GRAPH)

# ================================================================== animation
class A:
    """ticks-based keyframe author. tracks: bone -> channel -> [(tick, x, y, z)]"""
    def __init__(self, name, ticks, loop=False):
        self.name, self.ticks, self.loop, self.tr = name, ticks, loop, {}

    def k(self, bone, ch, keys):
        self.tr.setdefault(bone, {}).setdefault(ch, []).extend(keys)
        return self

    def rot(self, bone, *keys): return self.k(bone, "rotation", keys)
    def pos(self, bone, *keys): return self.k(bone, "position", keys)
    def scl(self, bone, *keys): return self.k(bone, "scale", keys)

    def drape(self, chain, keys, delay=2, gain=0.8):
        """secondary motion: the first bone gets `keys`, every next one the same keys delayed + damped."""
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

    def rest(self, bone, *ticks):
        """the idle rest pose of a bone at the given ticks"""
        return self.rot(bone, *[(t, *REST[bone]) for t in ticks])

    def done(self):
        if "pencils" not in self.tr:
            self.scl("pencils", (0, .001, .001, .001))
        for b, v in REST.items():  # anything not authored keeps the rest pose (no snapping to the bind pose)
            if b not in self.tr or "rotation" not in self.tr[b]:
                self.rot(b, (0, *v))
        tracks = {}
        for b, chs in self.tr.items():
            tracks[b] = {ch: sorted([(t / 20.0, x, y, z) for (t, x, y, z) in v], key=lambda q: q[0]) for ch, v in chs.items()}
        m.anim(self.name, self.ticks / 20.0, tracks, loop=self.loop)


# rest pose = the reference stance: compass raised in the left fist, claw hand hanging, slight slouch
REST = {
    "arm_r": (4, 0, 9), "fore_r": (12, 0, 0), "claws_r": (14, 0, 0),
    "arm_l": (14, 0, -20), "fore_l": (42, 0, 0), "hand_l": (0, 0, 0),
    "comp": (16, 34, 0), "c_needle": (0, 4, 0), "c_pencil": (0, -4, 0),
}
HAIR_B = ["hair_b1", "hair_b2", "hair_b3"]
HAIR_R = ["hair_r1", "hair_r2", "hair_r3"]
HAIR_L = ["hair_l1", "hair_l2", "hair_l3"]


def legs_both(a, keys_leg, keys_shin, keys_foot=None):
    """symmetric keys; z values mirrored for the left side"""
    for s, k in ((1, "r"), (-1, "l")):
        a.rot("leg_" + k, *[(t, x, y * s, z * s) for (t, x, y, z) in keys_leg])
        a.rot("shin_" + k, *keys_shin)
        if keys_foot: a.rot("foot_" + k, *keys_foot)


# ------------------------------------------------------------------ idle (4 s loop): looming slouch, compass bob, claws twitch
a = A("idle", 80, loop=True)
a.rot("body", (0, 2, 0, 0), (40, 3, 0, 0), (80, 2, 0, 0))
a.rot("chest", (0, -6, 4, 0), (20, -5, 2, 1), (40, -6, 4, 0), (60, -5, 6, -1), (80, -6, 4, 0))
a.pos("chest", (0, 0, 0, 0), (20, 0, 0.18, 0), (40, 0, 0, 0), (60, 0, 0.18, 0), (80, 0, 0, 0))
a.rot("head", (0, 2, -4, 6), (20, 3, -2, 4), (40, 2, -4, 7), (60, 3, -6, 4), (80, 2, -4, 6))
a.rot("arm_r", (0, 4, 0, 9), (40, 6, 0, 11), (80, 4, 0, 9))
a.rot("fore_r", (0, 12, 0, 0), (40, 16, 0, 0), (80, 12, 0, 0))
a.rot("claws_r", (0, 14, 0, 0), (28, 20, 0, 0), (32, 4, 0, 0), (35, 22, 0, 0), (38, 10, 0, 0), (80, 14, 0, 0))
a.rot("arm_l", (0, 14, 0, -20), (20, 16, 0, -19), (40, 14, 0, -20), (60, 16, 0, -21), (80, 14, 0, -20))
a.rot("fore_l", (0, 42, 0, 0), (20, 46, 0, 0), (40, 42, 0, 0), (60, 46, 0, 0), (80, 42, 0, 0))
a.rot("comp", (0, 16, 34, 0), (40, 12, 38, 0), (52, 14, 34, 6), (56, 16, 34, -4), (80, 16, 34, 0))
a.rot("c_pencil", (0, 0, -4, 0), (48, 0, -4, 0), (51, 0, -14, 0), (54, 0, -2, 0), (57, 0, -12, 0), (60, 0, -4, 0), (80, 0, -4, 0))  # click click
a.rot("c_needle", (0, 0, 4, 0), (80, 0, 4, 0))
a.drape(HAIR_B, [(0, -2, 0, 1), (20, -3.5, 0, 0), (40, -2, 0, -1), (60, -3.5, 0, 0), (80, -2, 0, 1)], delay=4, gain=0.9)
a.drape(HAIR_R, [(0, 0, 0, 1), (30, 0, 0, 3), (55, 0, 0, 0), (80, 0, 0, 1)], delay=4)
a.drape(HAIR_L, [(0, 0, 0, -1), (25, 0, 0, -3), (50, 0, 0, 0), (80, 0, 0, -1)], delay=4)
a.rot("bang", (0, 0, 0, 0), (30, 0, 0, 2), (60, 0, 0, -1), (80, 0, 0, 0))
a.rot("ear_r", (0, 0, 0, 0), (62, 0, 0, 0), (64, 0, 0, -10), (67, 0, 0, 0), (80, 0, 0, 0))
a.rot("ear_l", (0, 0, 0, 0), (63, 0, 0, 0), (65, 0, 0, 10), (68, 0, 0, 0), (80, 0, 0, 0))
a.done()

# ------------------------------------------------------------------ walk (one stride): long stalking strides, compass bouncing
a = A("walk", 20, loop=True)
a.rot("leg_r", (0, 30, 0, 0), (5, 0, 0, 0), (10, -28, 0, 0), (15, 0, 0, 0), (20, 30, 0, 0))
a.rot("shin_r", (0, -4, 0, 0), (5, -10, 0, 0), (10, -12, 0, 0), (13, -55, 0, 0), (17, -30, 0, 0), (20, -4, 0, 0))
a.rot("foot_r", (0, -12, 0, 0), (5, 0, 0, 0), (10, 12, 0, 0), (15, 6, 0, 0), (20, -12, 0, 0))
a.rot("leg_l", (0, -28, 0, 0), (5, 0, 0, 0), (10, 30, 0, 0), (15, 0, 0, 0), (20, -28, 0, 0))
a.rot("shin_l", (0, -12, 0, 0), (3, -55, 0, 0), (7, -30, 0, 0), (10, -4, 0, 0), (15, -10, 0, 0), (20, -12, 0, 0))
a.rot("foot_l", (0, 12, 0, 0), (5, 6, 0, 0), (10, -12, 0, 0), (15, 0, 0, 0), (20, 12, 0, 0))
a.pos("body", (0, 0, -0.4, 0), (5, 0, 0.5, 0), (10, 0, -0.4, 0), (15, 0, 0.5, 0), (20, 0, -0.4, 0))
a.rot("body", (0, -5, 5, 0), (10, -5, -5, 0), (20, -5, 5, 0))
a.rot("chest", (0, -3, -5, 2), (10, -3, 5, -2), (20, -3, -5, 2))
a.rot("arm_r", (0, -24, 0, 6), (10, 26, 0, 5), (20, -24, 0, 6))
a.rot("fore_r", (0, 6, 0, 0), (10, 26, 0, 0), (20, 6, 0, 0))
a.rot("arm_l", (0, 10, 0, -2), (5, 6, 0, 0), (10, -6, 0, -2), (15, 6, 0, 0), (20, 10, 0, -2))
a.rot("fore_l", (0, 0, 0, 0), (5, 6, 0, 0), (10, 0, 0, 0), (15, 6, 0, 0), (20, 0, 0, 0))
a.rot("comp", (0, 0, 0, 0), (5, 6, 0, 0), (10, 0, 0, 0), (15, 6, 0, 0), (20, 0, 0, 0))
a.drape(HAIR_B, [(0, -8, 2, 2), (5, -12, 0, 0), (10, -8, -2, -2), (15, -12, 0, 0), (20, -8, 2, 2)], delay=2, gain=0.85)
a.drape(HAIR_R, [(0, -4, 0, 4), (10, -6, 0, 1), (20, -4, 0, 4)], delay=2)
a.drape(HAIR_L, [(0, -6, 0, -1), (10, -4, 0, -4), (20, -6, 0, -1)], delay=2)
a.rot("bang", (0, 0, 0, 0), (5, -6, 0, 2), (10, 0, 0, 0), (15, -6, 0, -2), (20, 0, 0, 0))
# walk is layered on top of idle: rest values already come from idle, so no REST fill here
a.tr.setdefault("pencils", {})["scale"] = [(0, .001, .001, .001)]
tracks = {b: {ch: sorted([(t / 20.0, x, y, z) for (t, x, y, z) in v]) for ch, v in chs.items()} for b, chs in a.tr.items()}
m.anim("walk", 1.0, tracks, loop=True)

# ------------------------------------------------------------------ sweep (34): wind left, full spinning compass sweep peaking 15
a = A("sweep", 34)
a.rot("root", (0, 0, 0, 0), (9, 0, 40, 0), (11, 0, 30, 0), (13, 0, -120, 0), (15, 0, -230, 0), (17, 0, -330, 0), (20, 0, -395, 0), (26, 0, -350, 0), (34, 0, -360, 0))
a.pos("body", (0, 0, 0, 0), (9, 0, -2.2, 0), (15, 0, -1.6, 0), (20, 0, -2.0, 0), (34, 0, 0, 0))
a.rot("body", (0, 0, 0, 0), (9, -10, 10, 0), (15, -8, -10, -6), (20, -6, -6, 0), (34, 0, 0, 0))
a.rot("chest", (0, 0, 0, 0), (9, 4, 20, 0), (13, -2, -10, 0), (16, -4, -20, 0), (22, 0, -8, 0), (34, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (9, -4, -30, 0), (14, 6, 10, 0), (18, 8, 20, 6), (26, 2, 0, 0), (34, 0, 0, 0))
a.rot("arm_l", (0, *REST["arm_l"]), (9, 30, -40, -70), (12, 50, 0, -88), (15, 60, 0, -92), (18, 50, 0, -86), (24, 30, 0, -40), (34, *REST["arm_l"]))
a.rot("fore_l", (0, *REST["fore_l"]), (9, 30, 0, 0), (12, 0, 0, 0), (18, 0, 0, 0), (26, 30, 0, 0), (34, *REST["fore_l"]))
a.rot("comp", (0, *REST["comp"]), (9, -90, 30, 0), (12, -90, 0, 0), (18, -90, 0, 0), (26, -30, 10, 0), (34, *REST["comp"]))
a.rot("c_needle", (0, 0, 4, 0), (12, 0, 14, 0), (20, 0, 14, 0), (30, 0, 4, 0))
a.rot("c_pencil", (0, 0, -4, 0), (12, 0, -14, 0), (20, 0, -14, 0), (30, 0, -4, 0))
a.rot("arm_r", (0, *REST["arm_r"]), (9, -20, 0, 50), (13, 10, 0, 70), (18, 0, 0, 60), (26, 0, 0, 20), (34, *REST["arm_r"]))
a.rot("fore_r", (0, 12, 0, 0), (9, 40, 0, 0), (15, 10, 0, 0), (34, 12, 0, 0))
a.rot("claws_r", (0, 14, 0, 0), (9, -10, 0, 0), (15, 30, 0, 0), (34, 14, 0, 0))
legs_both(a, [(0, 0, 0, 0), (9, 22, 0, 8), (15, 14, 0, 12), (20, 18, 0, 10), (34, 0, 0, 0)],
          [(0, 0, 0, 0), (9, -40, 0, 0), (15, -26, 0, 0), (20, -34, 0, 0), (34, 0, 0, 0)])
a.drape(HAIR_B, [(0, -2, 0, 0), (9, 6, -20, 0), (13, -40, 30, 0), (16, -70, 40, 0), (20, -66, 30, 0), (26, -20, 0, 0), (34, -2, 0, 0)], delay=2, gain=0.85)
a.drape(HAIR_R, [(0, 0, 0, 1), (9, 0, 0, -10), (14, -20, 0, 50), (20, -20, 0, 60), (28, 0, 0, 8), (34, 0, 0, 1)], delay=2)
a.drape(HAIR_L, [(0, 0, 0, -1), (9, 0, 0, 6), (14, -20, 0, -50), (20, -20, 0, -60), (28, 0, 0, -8), (34, 0, 0, -1)], delay=2)
a.rot("bang", (0, 0, 0, 0), (14, -30, 0, -10), (22, -10, 0, 4), (34, 0, 0, 0))
a.done()

# ------------------------------------------------------------------ lunge (30): fencing crouch, dash 10, needle stab held 11..14
a = A("lunge", 30)
a.pos("body", (0, 0, 0, 0), (8, 0, -2.4, 1.2), (10, 0, -2.0, 0), (12, 0, -2.8, -1.2), (16, 0, -2.6, -1.0), (30, 0, 0, 0))
a.rot("body", (0, 0, 0, 0), (8, 6, 30, 0), (10, -6, 0, 0), (12, -18, -30, 0), (16, -16, -28, 0), (24, -4, -6, 0), (30, 0, 0, 0))
a.rot("chest", (0, 0, 0, 0), (8, 4, 20, 0), (12, -8, -18, 0), (16, -6, -16, 0), (30, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (8, -8, -40, 0), (12, 14, 40, 0), (16, 12, 36, 0), (24, 4, 10, 6), (30, 0, 0, 0))
a.rot("arm_l", (0, *REST["arm_l"]), (8, -20, 0, -8), (10, 40, 0, -4), (12, 88, 0, 2), (15, 86, 0, 2), (22, 40, 0, -10), (30, *REST["arm_l"]))
a.rot("fore_l", (0, *REST["fore_l"]), (8, 104, 0, 0), (10, 50, 0, 0), (12, 0, 0, 0), (15, 2, 0, 0), (22, 30, 0, 0), (30, *REST["fore_l"]))
a.rot("comp", (0, *REST["comp"]), (8, -100, 0, 0), (12, -90, 0, 0), (15, -90, 0, 0), (22, -40, 10, 0), (30, *REST["comp"]))
a.rot("c_needle", (0, 0, 4, 0), (8, 0, 0, 0), (16, 0, 0, 0), (30, 0, 4, 0))
a.rot("c_pencil", (0, 0, -4, 0), (8, 0, 0, 0), (16, 0, 0, 0), (30, 0, -4, 0))
a.rot("arm_r", (0, *REST["arm_r"]), (8, 30, 0, 30), (12, -50, 0, 30), (16, -46, 0, 28), (30, *REST["arm_r"]))
a.rot("fore_r", (0, 12, 0, 0), (8, 40, 0, 0), (12, 20, 0, 0), (30, 12, 0, 0))
a.rot("claws_r", (0, 14, 0, 0), (8, 40, 0, 0), (12, -10, 0, 0), (30, 14, 0, 0))
a.rot("leg_l", (0, 0, 0, 0), (8, 30, 0, -4), (10, 10, 0, 0), (12, 58, 0, -6), (16, 56, 0, -6), (30, 0, 0, 0))
a.rot("shin_l", (0, 0, 0, 0), (8, -50, 0, 0), (10, -20, 0, 0), (12, -50, 0, 0), (16, -48, 0, 0), (30, 0, 0, 0))
a.rot("foot_l", (0, 0, 0, 0), (12, -8, 0, 0), (30, 0, 0, 0))
a.rot("leg_r", (0, 0, 0, 0), (8, -10, 0, 6), (10, -30, 0, 0), (12, -40, 0, 4), (16, -38, 0, 4), (30, 0, 0, 0))
a.rot("shin_r", (0, 0, 0, 0), (8, -30, 0, 0), (12, -6, 0, 0), (16, -8, 0, 0), (30, 0, 0, 0))
a.rot("foot_r", (0, 0, 0, 0), (12, 40, 0, 0), (16, 38, 0, 0), (30, 0, 0, 0))
a.drape(HAIR_B, [(0, -2, 0, 0), (8, 8, 20, 0), (11, -50, 0, 0), (14, -40, -10, 0), (20, -14, 0, 0), (30, -2, 0, 0)], delay=2, gain=0.85)
a.drape(HAIR_R, [(0, 0, 0, 1), (8, 10, 0, -6), (12, -30, 0, 20), (20, -6, 0, 6), (30, 0, 0, 1)], delay=2)
a.drape(HAIR_L, [(0, 0, 0, -1), (8, 10, 0, 6), (12, -30, 0, -20), (20, -6, 0, -6), (30, 0, 0, -1)], delay=2)
a.rot("bang", (0, 0, 0, 0), (12, -30, 0, 0), (18, 6, 0, 0), (30, 0, 0, 0))
a.done()

# ------------------------------------------------------------------ splitSlam (40): two-hand raise, hop 8, legs spread, SLAM on 20
a = A("splitSlam", 40)
a.pos("root", (0, 0, 0, 0), (7, 0, 0, 0), (10, 0, 4.5, -1), (14, 0, 6.0, -2), (18, 0, 2.5, -3), (20, 0, 0, -3), (40, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (6, 0, -3.0, 0), (9, 0, 0, 0), (14, 0, -0.5, 0), (20, 0, -4.0, 0), (28, 0, -3.6, 0), (40, 0, 0, 0))
a.rot("body", (0, 0, 0, 0), (6, -14, 0, 0), (10, 10, 0, 0), (15, 14, 0, 0), (18, -10, 0, 0), (20, -30, 0, 0), (28, -26, 0, 0), (40, 0, 0, 0))
a.rot("chest", (0, 0, 0, 0), (10, 10, 0, 0), (15, 12, 0, 0), (20, -12, 0, 0), (28, -10, 0, 0), (40, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (6, 10, 0, 0), (14, -10, 0, 0), (20, 30, 0, 0), (26, 34, 0, 8), (40, 0, 0, 0))
for s, k in ((1, "r"), (-1, "l")):
    a.rot("arm_" + k, (0, *REST["arm_" + k]), (6, 60, 0, -20 * s), (10, 160, 0, -14 * s), (15, 175, 0, -10 * s), (18, 120, 0, -12 * s),
          (20, 60, 0, -16 * s), (28, 64, 0, -16 * s), (34, 30, 0, 4 * s), (40, *REST["arm_" + k]))
    a.rot("fore_" + k, (0, *REST["fore_" + k]), (6, 30, 0, 0), (10, 20, 0, 0), (15, 30, 0, 0), (20, 0, 0, 0), (28, 4, 0, 0), (40, *REST["fore_" + k]))
a.rot("comp", (0, *REST["comp"]), (6, -40, 0, 0), (10, -20, 0, 0), (15, -10, 0, 0), (18, -60, 0, 0), (20, -126, 0, 0), (28, -122, 0, 0), (34, -60, 10, 0), (40, *REST["comp"]))
a.rot("c_needle", (0, 0, 4, 0), (10, 0, 30, 0), (18, 0, 30, 0), (20, 0, 26, 0), (28, 0, 26, 0), (36, 0, 4, 0))
a.rot("c_pencil", (0, 0, -4, 0), (10, 0, -30, 0), (18, 0, -30, 0), (20, 0, -26, 0), (28, 0, -26, 0), (36, 0, -4, 0))
a.rot("claws_r", (0, 14, 0, 0), (10, -20, 0, 0), (20, 40, 0, 0), (40, 14, 0, 0))
legs_both(a, [(0, 0, 0, 0), (6, 40, 0, 6), (9, -6, 0, 4), (14, 40, 0, 10), (18, 20, 0, 14), (20, 54, 0, 16), (28, 50, 0, 16), (40, 0, 0, 0)],
          [(0, 0, 0, 0), (6, -70, 0, 0), (9, -4, 0, 0), (14, -80, 0, 0), (18, -30, 0, 0), (20, -84, 0, 0), (28, -80, 0, 0), (40, 0, 0, 0)],
          [(0, 0, 0, 0), (6, 30, 0, 0), (9, -20, 0, 0), (14, 20, 0, 0), (20, 30, 0, 0), (28, 28, 0, 0), (40, 0, 0, 0)])
a.drape(HAIR_B, [(0, -2, 0, 0), (6, 8, 0, 0), (10, 30, 0, 0), (15, 20, 0, 0), (19, -30, 0, 0), (21, -60, 0, 0), (26, -20, 0, 0), (40, -2, 0, 0)], delay=2, gain=0.85)
a.drape(HAIR_R, [(0, 0, 0, 1), (10, 20, 0, -10), (20, -10, 0, 50), (28, 0, 0, 20), (40, 0, 0, 1)], delay=2)
a.drape(HAIR_L, [(0, 0, 0, -1), (10, 20, 0, 10), (20, -10, 0, -50), (28, 0, 0, -20), (40, 0, 0, -1)], delay=2)
a.rot("bang", (0, 0, 0, 0), (12, 20, 0, 0), (20, -40, 0, 0), (28, -10, 0, 0), (40, 0, 0, 0))
a.rot("ear_r", (0, 0, 0, 0), (14, 20, 0, 10), (20, -30, 0, -20), (28, 0, 0, 0))
a.rot("ear_l", (0, 0, 0, 0), (14, 20, 0, -10), (20, -30, 0, 20), (28, 0, 0, 0))
a.done()

# ------------------------------------------------------------------ drawCircle (46): crouch, pencil to the ground, one full turn 6..30, flourish
a = A("drawCircle", 46)
a.rot("root", (0, 0, 0, 0), (6, 0, 0, 0), (12, 0, -80, 0), (18, 0, -170, 0), (24, 0, -265, 0), (30, 0, -360, 0), (46, 0, -360, 0))
a.pos("body", (0, 0, 0, 0), (5, 0, -3.4, 0), (30, 0, -3.4, 0), (36, 0, 0.4, 0), (46, 0, 0, 0))
a.rot("body", (0, 0, 0, 0), (5, -24, 6, 0), (30, -24, 6, 0), (34, 8, 0, 0), (40, 6, 0, 0), (46, 0, 0, 0))
a.rot("chest", (0, 0, 0, 0), (5, -8, 10, 6), (30, -8, 10, 6), (34, 10, 0, 0), (40, 8, 0, 0), (46, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (5, 30, 20, 0), (18, 34, 24, 6), (30, 30, 20, 0), (34, 34, 0, 10), (38, 28, 0, -8), (42, 30, 0, 8), (46, 0, 0, 0))
a.rot("arm_l", (0, *REST["arm_l"]), (5, 40, 0, -24), (30, 40, 0, -24), (34, 150, 0, -24), (40, 160, 0, -20), (46, *REST["arm_l"]))
a.rot("fore_l", (0, *REST["fore_l"]), (5, 0, 0, 0), (30, 0, 0, 0), (34, 10, 0, 0), (46, *REST["fore_l"]))
a.rot("comp", (0, *REST["comp"]), (5, -100, 0, 0), (30, -100, 0, 0), (34, -80, 0, 0), (40, -86, 10, 0), (46, *REST["comp"]))
a.rot("c_needle", (0, 0, 4, 0), (5, 0, 6, 0), (30, 0, 6, 0), (34, 0, 30, 0), (42, 0, 30, 0), (46, 0, 4, 0))
a.rot("c_pencil", (0, 0, -4, 0), (5, 0, -26, 0), (30, 0, -26, 0), (34, 0, -30, 0), (42, 0, -30, 0), (46, 0, -4, 0))
a.rot("arm_r", (0, *REST["arm_r"]), (5, -10, 0, 60), (30, -10, 0, 64), (34, 30, 0, 40), (40, 20, 0, 30), (46, *REST["arm_r"]))
a.rot("fore_r", (0, 12, 0, 0), (5, 30, 0, 0), (30, 30, 0, 0), (34, 60, 0, 0), (46, 12, 0, 0))
a.rot("claws_r", (0, 14, 0, 0), (5, -16, 0, 0), (30, -16, 0, 0), (34, 40, 0, 0), (46, 14, 0, 0))
legs_both(a, [(0, 0, 0, 0), (5, 50, 0, 14), (30, 50, 0, 14), (34, 0, 0, 2), (46, 0, 0, 0)],
          [(0, 0, 0, 0), (5, -76, 0, 0), (30, -76, 0, 0), (34, -6, 0, 0), (46, 0, 0, 0)],
          [(0, 0, 0, 0), (5, 26, 0, 0), (30, 26, 0, 0), (34, 0, 0, 0)])
a.drape(HAIR_B, [(0, -2, 0, 0), (5, 10, 0, 0), (10, -30, 30, 0), (30, -36, 30, 0), (34, -10, 0, 0), (40, -4, 0, 0), (46, -2, 0, 0)], delay=2, gain=0.85)
a.drape(HAIR_R, [(0, 0, 0, 1), (10, -14, 0, 36), (30, -14, 0, 40), (36, 0, 0, 4), (46, 0, 0, 1)], delay=2)
a.drape(HAIR_L, [(0, 0, 0, -1), (10, -14, 0, -36), (30, -14, 0, -40), (36, 0, 0, -4), (46, 0, 0, -1)], delay=2)
a.rot("bang", (0, 0, 0, 0), (10, -14, 0, -10), (30, -14, 0, -10), (36, 6, 0, 4), (46, 0, 0, 0))
a.done()

# ------------------------------------------------------------------ charge (34): sprint 6..24 with the compass scraping behind, rising slash 27
a = A("charge", 34)
a.pos("body", (0, 0, 0, 0), (5, 0, -2.4, 0), (8, 0, -1.4, 0), (11, 0, -2.0, 0), (14, 0, -1.4, 0), (17, 0, -2.0, 0), (20, 0, -1.4, 0), (23, 0, -2.0, 0),
      (25, 0, -3.0, 0), (27, 0, -0.6, 0), (34, 0, 0, 0))
a.rot("body", (0, 0, 0, 0), (5, -30, 0, 0), (24, -30, 0, 0), (25, -10, 24, 0), (27, 10, -30, 0), (30, 6, -20, 0), (34, 0, 0, 0))
a.rot("chest", (0, 0, 0, 0), (5, -6, 0, 0), (24, -6, 0, 0), (27, 10, -10, 0), (34, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (5, 34, 0, 0), (24, 34, 0, 0), (27, 6, 30, 0), (34, 0, 0, 0))
a.rot("arm_l", (0, *REST["arm_l"]), (5, -50, 0, -16), (24, -50, 0, -16), (25, -60, 0, -20), (27, 90, 0, -10), (29, 160, 0, -14), (34, *REST["arm_l"]))
a.rot("fore_l", (0, *REST["fore_l"]), (5, 0, 0, 0), (24, 0, 0, 0), (27, 0, 0, 0), (30, 20, 0, 0), (34, *REST["fore_l"]))
a.rot("comp", (0, *REST["comp"]), (5, -120, 0, 0), (24, -120, 0, 0), (25, -110, 0, 0), (27, -90, 0, 0), (30, -80, 0, 0), (34, *REST["comp"]))
a.rot("hand_l", (0, 0, 0, 0), (8, 4, 0, 4), (11, -4, 0, -4), (14, 4, 0, 4), (17, -4, 0, -4), (20, 4, 0, 4), (23, -4, 0, -4), (24, 0, 0, 0))
a.rot("arm_r", (0, *REST["arm_r"]), (5, 40, 0, 10)) .rot("arm_r", *[(t, -40 if (t // 3) % 2 else 50, 0, 10) for t in (8, 11, 14, 17, 20, 23)]) \
    .rot("arm_r", (25, 30, 0, 50), (27, -30, 0, 30), (34, *REST["arm_r"]))
a.rot("fore_r", (0, 12, 0, 0), (5, 50, 0, 0), (24, 50, 0, 0), (27, 20, 0, 0), (34, 12, 0, 0))
a.rot("claws_r", (0, 14, 0, 0), (5, -10, 0, 0), (24, -10, 0, 0), (27, 30, 0, 0), (34, 14, 0, 0))
run = [(0, 0, 0, 0), (5, 30, 0, 0)]
runs = [(0, 0, 0, 0), (5, -60, 0, 0)]
for i, t in enumerate((8, 11, 14, 17, 20, 23)):
    run.append((t, 60 if i % 2 == 0 else -40, 0, 0)); runs.append((t, -20 if i % 2 == 0 else -80, 0, 0))
a.rot("leg_r", *run, (25, 40, 0, 6), (27, -20, 0, 4), (34, 0, 0, 0))
a.rot("shin_r", *runs, (25, -60, 0, 0), (27, -10, 0, 0), (34, 0, 0, 0))
a.rot("leg_l", *[(t, -x if t > 5 else x, 0, 0) for (t, x, _, __) in run], (25, -30, 0, -6), (27, 30, 0, -4), (34, 0, 0, 0))
a.rot("shin_l", *[(t, (-80 if x == -20 else -20) if t > 5 else x, 0, 0) for (t, x, _, __) in runs], (25, -20, 0, 0), (27, -30, 0, 0), (34, 0, 0, 0))
a.drape(HAIR_B, [(0, -2, 0, 0), (5, -50, 0, 0), (12, -60, 6, 0), (18, -60, -6, 0), (24, -56, 0, 0), (27, -20, 20, 0), (34, -2, 0, 0)], delay=2, gain=0.85)
a.drape(HAIR_R, [(0, 0, 0, 1), (5, -40, 0, 20), (24, -44, 0, 24), (28, -10, 0, 10), (34, 0, 0, 1)], delay=2)
a.drape(HAIR_L, [(0, 0, 0, -1), (5, -40, 0, -20), (24, -44, 0, -24), (28, -10, 0, -10), (34, 0, 0, -1)], delay=2)
a.rot("bang", (0, 0, 0, 0), (5, -30, 0, 0), (24, -30, 0, 0), (28, 6, 0, 0), (34, 0, 0, 0))
a.rot("ear_r", (0, 0, 0, 0), (5, -30, 0, 0), (24, -30, 0, 0), (28, 0, 0, 0))
a.rot("ear_l", (0, 0, 0, 0), (5, -30, 0, 0), (24, -30, 0, 0), (28, 0, 0, 0))
a.done()

# ------------------------------------------------------------------ hairWhip (28): twist left, whip a half turn so the hair mane lashes on 13
a = A("hairWhip", 28)
a.rot("root", (0, 0, 0, 0), (8, 0, 50, 0), (10, 0, 30, 0), (13, 0, -180, 0), (16, 0, -300, 0), (20, 0, -370, 0), (28, 0, -360, 0))
a.pos("body", (0, 0, 0, 0), (8, 0, -1.8, 0), (13, 0, -0.6, 0), (18, 0, -1.4, 0), (28, 0, 0, 0))
a.rot("body", (0, 0, 0, 0), (8, -12, 0, 0), (13, 10, 0, 0), (18, -4, 0, 0), (28, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (8, -16, -20, 0), (11, -20, 20, 0), (13, -30, 30, 0), (18, 10, 0, 0), (28, 0, 0, 0))
a.rot("arm_l", (0, *REST["arm_l"]), (8, 30, 0, -50), (13, 20, 0, -80), (18, 20, 0, -60), (28, *REST["arm_l"]))
a.rot("comp", (0, *REST["comp"]), (8, -40, 0, 0), (13, -90, 0, 0), (20, -60, 0, 0), (28, *REST["comp"]))
a.rot("arm_r", (0, *REST["arm_r"]), (8, -20, 0, 30), (13, 10, 0, 80), (18, 10, 0, 60), (28, *REST["arm_r"]))
legs_both(a, [(0, 0, 0, 0), (8, 24, 0, 6), (13, 6, 0, 10), (18, 18, 0, 8), (28, 0, 0, 0)],
          [(0, 0, 0, 0), (8, -40, 0, 0), (13, -10, 0, 0), (18, -30, 0, 0), (28, 0, 0, 0)])
a.rot("hair_b1", (0, -2, 0, 0), (8, 14, 0, 0), (11, -50, -30, 0), (13, -86, -40, 0), (15, -80, -20, 0), (18, -50, 10, 0), (22, -10, 0, 0), (28, -2, 0, 0))
a.rot("hair_b2", (0, 0, 0, 0), (9, 14, 0, 0), (13, -20, -20, 0), (16, -30, 0, 0), (20, -10, 0, 0), (28, 0, 0, 0))
a.rot("hair_b3", (0, 0, 0, 0), (10, 14, 0, 0), (14, -16, -20, 0), (17, -24, 0, 0), (22, -8, 0, 0), (28, 0, 0, 0))
a.drape(HAIR_R, [(0, 0, 0, 1), (8, 0, 0, -10), (12, -30, 0, 70), (16, -30, 0, 74), (22, 0, 0, 10), (28, 0, 0, 1)], delay=2)
a.drape(HAIR_L, [(0, 0, 0, -1), (8, 0, 0, 10), (12, -30, 0, -70), (16, -30, 0, -74), (22, 0, 0, -10), (28, 0, 0, -1)], delay=2)
a.rot("bang", (0, 0, 0, 0), (11, -20, 0, 20), (14, -40, 0, -10), (22, 0, 0, 0))
a.rot("ear_r", (0, 0, 0, 0), (13, -30, 0, -20), (20, 0, 0, 0))
a.rot("ear_l", (0, 0, 0, 0), (13, -30, 0, 20), (20, 0, 0, 0))
a.done()

# ------------------------------------------------------------------ combo (44, rage): forehand slash 8, rising backhand 17, leaping plunge 30
a = A("combo", 44)
a.rot("body", (0, 0, 0, 0), (4, -6, 40, 0), (8, -14, -40, 0), (11, -10, -50, 0), (14, -12, -40, 0), (17, 6, 36, 0), (20, 6, 40, 0),
      (24, 14, 0, 0), (27, 10, 0, 0), (30, -30, 0, 0), (36, -26, 0, 0), (44, 0, 0, 0))
a.pos("root", (0, 0, 0, 0), (21, 0, 0, 0), (24, 0, 5, -1), (27, 0, 6, -2), (29, 0, 2, -3), (30, 0, 0, -3), (44, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (4, 0, -1.6, 0), (8, 0, -2.2, -1), (14, 0, -2.6, 0), (17, 0, -1.0, -1), (21, 0, -3.0, 0), (24, 0, 0, 0), (30, 0, -4.0, 0), (36, 0, -3.6, 0), (44, 0, 0, 0))
a.rot("chest", (0, 0, 0, 0), (4, 4, 20, 0), (8, -6, -20, 0), (17, 8, 16, 0), (24, 10, 0, 0), (30, -12, 0, 0), (44, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (4, -4, -40, 0), (8, 6, 40, 0), (14, 0, 30, 0), (17, 10, -30, 0), (24, -10, 0, 0), (30, 30, 0, 0), (38, 30, 0, 10), (44, 0, 0, 0))
a.rot("arm_l", (0, *REST["arm_l"]), (4, 20, -30, -80), (6, 60, 0, -80), (8, 80, 0, 10), (10, 70, 0, 40), (14, 30, 0, 40),
      (17, 150, 0, -40), (20, 160, 0, -36), (24, 175, 0, -10), (27, 178, 0, -8), (30, 60, 0, -14), (36, 62, 0, -14), (44, *REST["arm_l"]))
a.rot("fore_l", (0, *REST["fore_l"]), (4, 20, 0, 0), (8, 0, 0, 0), (14, 20, 0, 0), (17, 0, 0, 0), (24, 20, 0, 0), (30, 0, 0, 0), (44, *REST["fore_l"]))
a.rot("comp", (0, *REST["comp"]), (4, -90, 30, 0), (8, -90, 0, 0), (14, -90, 0, 0), (17, -90, 0, 0), (24, -10, 0, 0), (27, -10, 0, 0),
      (30, -126, 0, 0), (36, -122, 0, 0), (44, *REST["comp"]))
a.rot("c_needle", (0, 0, 4, 0), (8, 0, 10, 0), (24, 0, 30, 0), (30, 0, 24, 0), (40, 0, 4, 0))
a.rot("c_pencil", (0, 0, -4, 0), (8, 0, -10, 0), (24, 0, -30, 0), (30, 0, -24, 0), (40, 0, -4, 0))
a.rot("arm_r", (0, *REST["arm_r"]), (4, -10, 0, 50), (8, 30, 0, 20), (14, 20, 0, 40), (17, -30, 0, 50), (24, 175, 0, 10), (27, 178, 0, 8),
      (30, 60, 0, 14), (36, 62, 0, 14), (44, *REST["arm_r"]))
a.rot("fore_r", (0, 12, 0, 0), (8, 30, 0, 0), (24, 20, 0, 0), (30, 0, 0, 0), (44, 12, 0, 0))
a.rot("claws_r", (0, 14, 0, 0), (8, 40, 0, 0), (17, -20, 0, 0), (30, 40, 0, 0), (44, 14, 0, 0))
a.rot("leg_l", (0, 0, 0, 0), (4, -10, 0, 0), (8, 40, 0, -4), (14, 30, 0, -4), (17, -20, 0, -4), (21, 40, 0, -6), (24, -10, 0, 0), (27, 40, 0, 0), (30, 56, 0, -14), (36, 54, 0, -14), (44, 0, 0, 0))
a.rot("shin_l", (0, 0, 0, 0), (8, -40, 0, 0), (17, -10, 0, 0), (21, -70, 0, 0), (24, -10, 0, 0), (27, -80, 0, 0), (30, -84, 0, 0), (36, -80, 0, 0), (44, 0, 0, 0))
a.rot("leg_r", (0, 0, 0, 0), (4, 14, 0, 0), (8, -30, 0, 4), (14, -20, 0, 4), (17, 30, 0, 4), (21, 40, 0, 6), (24, -10, 0, 0), (27, 40, 0, 0), (30, 50, 0, 14), (36, 50, 0, 14), (44, 0, 0, 0))
a.rot("shin_r", (0, 0, 0, 0), (8, -10, 0, 0), (17, -40, 0, 0), (21, -70, 0, 0), (24, -10, 0, 0), (27, -80, 0, 0), (30, -84, 0, 0), (36, -80, 0, 0), (44, 0, 0, 0))
a.drape(HAIR_B, [(0, -2, 0, 0), (4, 4, -20, 0), (8, -30, 30, 0), (14, -20, 20, 0), (17, -30, -30, 0), (24, 30, 0, 0), (28, 20, 0, 0), (31, -60, 0, 0), (36, -20, 0, 0), (44, -2, 0, 0)], delay=2, gain=0.85)
a.drape(HAIR_R, [(0, 0, 0, 1), (8, -10, 0, 40), (17, -10, 0, -10), (24, 20, 0, -10), (31, -10, 0, 50), (38, 0, 0, 10), (44, 0, 0, 1)], delay=2)
a.drape(HAIR_L, [(0, 0, 0, -1), (8, -10, 0, 10), (17, -10, 0, -40), (24, 20, 0, 10), (31, -10, 0, -50), (38, 0, 0, -10), (44, 0, 0, -1)], delay=2)
a.rot("bang", (0, 0, 0, 0), (8, -20, 0, 0), (17, 10, 0, 0), (24, 20, 0, 0), (30, -40, 0, 0), (38, -10, 0, 0), (44, 0, 0, 0))
a.done()

# ------------------------------------------------------------------ scissorSnip (30): legs flung open like shears, step in, SNAP shut on 14, wrench
a = A("scissorSnip", 30)
a.pos("body", (0, 0, 0, 0), (6, 0, -1.4, 1.0), (11, 0, -1.2, -0.6), (14, 0, -2.4, -1.6), (19, 0, -2.2, -1.4), (30, 0, 0, 0))
a.rot("body", (0, 0, 0, 0), (6, 4, 20, 0), (11, -6, -6, 0), (14, -16, -16, 0), (17, -14, -10, 0), (19, -14, 10, 0), (22, -10, -6, 0), (30, 0, 0, 0))
a.rot("chest", (0, 0, 0, 0), (6, 6, 10, 0), (14, -8, -10, 0), (30, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (6, -10, -20, -10), (11, 4, 10, 0), (14, 16, 20, 10), (20, 10, 20, -8), (30, 0, 0, 0))
a.rot("arm_l", (0, *REST["arm_l"]), (6, 40, 0, -40), (11, 70, 0, -10), (14, 88, 0, 4), (19, 86, 0, 4), (22, 80, 0, -6), (30, *REST["arm_l"]))
a.rot("fore_l", (0, *REST["fore_l"]), (6, 60, 0, 0), (11, 20, 0, 0), (14, 0, 0, 0), (22, 10, 0, 0), (30, *REST["fore_l"]))
a.rot("comp", (0, *REST["comp"]), (6, -40, 0, 0), (11, -84, 0, 0), (14, -92, 0, 0), (19, -90, 0, 30), (21, -90, 0, -30), (23, -90, 0, 0), (30, *REST["comp"]))
a.rot("c_needle", (0, 0, 4, 0), (5, 0, 36, 0), (11, 0, 40, 0), (13, 0, 30, 0), (14, 0, -3, 0), (15, 0, 1, 0), (24, 0, 1, 0), (30, 0, 4, 0))
a.rot("c_pencil", (0, 0, -4, 0), (5, 0, -36, 0), (11, 0, -40, 0), (13, 0, -30, 0), (14, 0, 3, 0), (15, 0, -1, 0), (24, 0, -1, 0), (30, 0, -4, 0))
a.rot("arm_r", (0, *REST["arm_r"]), (6, 100, 0, 30), (11, 80, 0, 10), (14, 70, 0, -14), (19, 66, 0, -14), (30, *REST["arm_r"]))
a.rot("fore_r", (0, 12, 0, 0), (6, 50, 0, 0), (14, 20, 0, 0), (30, 12, 0, 0))
a.rot("claws_r", (0, 14, 0, 0), (6, -30, 0, 0), (11, -30, 0, 0), (14, 50, 0, 0), (30, 14, 0, 0))
a.rot("leg_l", (0, 0, 0, 0), (6, -10, 0, 0), (11, 30, 0, -4), (14, 44, 0, -4), (19, 42, 0, -4), (30, 0, 0, 0))
a.rot("shin_l", (0, 0, 0, 0), (11, -30, 0, 0), (14, -40, 0, 0), (30, 0, 0, 0))
a.rot("leg_r", (0, 0, 0, 0), (6, 10, 0, 0), (11, -20, 0, 4), (14, -30, 0, 4), (19, -28, 0, 4), (30, 0, 0, 0))
a.rot("shin_r", (0, 0, 0, 0), (11, -10, 0, 0), (14, -6, 0, 0), (30, 0, 0, 0))
a.drape(HAIR_B, [(0, -2, 0, 0), (6, 6, 10, 0), (14, -40, -10, 0), (19, -30, 10, 0), (24, -10, 0, 0), (30, -2, 0, 0)], delay=2, gain=0.85)
a.drape(HAIR_R, [(0, 0, 0, 1), (6, 6, 0, 10), (14, -20, 0, 24), (22, 0, 0, 4), (30, 0, 0, 1)], delay=2)
a.drape(HAIR_L, [(0, 0, 0, -1), (6, 6, 0, -10), (14, -20, 0, -24), (22, 0, 0, -4), (30, 0, 0, -1)], delay=2)
a.rot("bang", (0, 0, 0, 0), (14, -24, 0, 0), (20, 6, 0, 0), (30, 0, 0, 0))
a.done()

# ------------------------------------------------------------------ arcSlash (36): step-in huge diagonal slash 14 (bleeds), backhand return 24
a = A("arcSlash", 36)
a.pos("body", (0, 0, 0, 0), (9, 0, -0.8, 1.4), (14, 0, -2.8, -1.4), (18, 0, -2.6, -1.2), (24, 0, -2.4, -0.6), (36, 0, 0, 0))
a.rot("body", (0, 0, 0, 0), (9, 12, 34, 0), (12, 0, 10, 0), (14, -20, -40, 0), (18, -18, -44, 0), (21, -10, -40, 0), (24, -6, 40, 0), (28, -4, 30, 0), (36, 0, 0, 0))
a.rot("chest", (0, 0, 0, 0), (9, 14, 16, 0), (14, -12, -20, 0), (24, -4, 20, 0), (36, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (9, 10, -30, 0), (14, 10, 40, 0), (21, 6, 30, 0), (24, 4, -30, 0), (30, 4, -10, 8), (36, 0, 0, 0))
a.rot("arm_l", (0, *REST["arm_l"]), (9, 170, 0, -40), (11, 160, 0, -20), (14, 50, 0, 40), (18, 30, 0, 50), (21, 40, 0, 50), (24, 90, 0, -70), (28, 80, 0, -76), (36, *REST["arm_l"]))
a.rot("fore_l", (0, *REST["fore_l"]), (9, 30, 0, 0), (14, 0, 0, 0), (24, 0, 0, 0), (30, 20, 0, 0), (36, *REST["fore_l"]))
a.rot("comp", (0, *REST["comp"]), (9, -60, 0, 0), (12, -90, 0, 0), (24, -90, 0, 0), (30, -60, 0, 0), (36, *REST["comp"]))
a.rot("c_needle", (0, 0, 4, 0), (9, 0, 20, 0), (14, 0, 20, 0), (30, 0, 4, 0))
a.rot("c_pencil", (0, 0, -4, 0), (9, 0, -20, 0), (14, 0, -20, 0), (30, 0, -4, 0))
a.rot("arm_r", (0, *REST["arm_r"]), (9, 150, 0, 30), (11, 140, 0, 10), (14, 40, 0, 30), (21, 30, 0, 40), (24, -20, 0, 60), (30, 0, 0, 30), (36, *REST["arm_r"]))
a.rot("fore_r", (0, 12, 0, 0), (9, 20, 0, 0), (14, 30, 0, 0), (36, 12, 0, 0))
a.rot("claws_r", (0, 14, 0, 0), (9, -20, 0, 0), (14, 40, 0, 0), (24, -10, 0, 0), (36, 14, 0, 0))
a.rot("leg_l", (0, 0, 0, 0), (9, -10, 0, -4), (14, 50, 0, -6), (21, 48, 0, -6), (24, 30, 0, -6), (36, 0, 0, 0))
a.rot("shin_l", (0, 0, 0, 0), (9, -20, 0, 0), (14, -50, 0, 0), (24, -30, 0, 0), (36, 0, 0, 0))
a.rot("leg_r", (0, 0, 0, 0), (9, 14, 0, 4), (14, -30, 0, 6), (21, -28, 0, 6), (24, -20, 0, 6), (36, 0, 0, 0))
a.rot("shin_r", (0, 0, 0, 0), (9, -16, 0, 0), (14, -10, 0, 0), (36, 0, 0, 0))
a.drape(HAIR_B, [(0, -2, 0, 0), (9, 16, -20, 0), (14, -50, 30, 0), (20, -30, 20, 0), (24, -30, -30, 0), (30, -10, 0, 0), (36, -2, 0, 0)], delay=2, gain=0.85)
a.drape(HAIR_R, [(0, 0, 0, 1), (9, 10, 0, -10), (14, -20, 0, 50), (24, -10, 0, -10), (30, 0, 0, 6), (36, 0, 0, 1)], delay=2)
a.drape(HAIR_L, [(0, 0, 0, -1), (9, 10, 0, 6), (14, -20, 0, 10), (24, -10, 0, -50), (30, 0, 0, -6), (36, 0, 0, -1)], delay=2)
a.rot("bang", (0, 0, 0, 0), (9, 14, 0, 0), (14, -30, 0, 0), (24, -20, 0, 10), (36, 0, 0, 0))
a.done()

# ------------------------------------------------------------------ perfectCircle (64, rage): raise open compass, leap, plant 20, two drawing turns 22..46,
# rip it up overhead 48 (all circles burst), cackle
a = A("perfectCircle", 64)
a.rot("root", (0, 0, 0, 0), (22, 0, 0, 0), (34, 0, -360, 0), (46, 0, -720, 0), (64, 0, -720, 0))
a.pos("root", (0, 0, 0, 0), (12, 0, 0, 0), (15, 0, 5, 0), (17, 0, 6.5, -1), (19, 0, 2.5, -1.5), (20, 0, 0, -1.5), (46, 0, 0, -1.5), (52, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (8, 0, 0, 0), (12, 0, -3.0, 0), (14, 0, 0, 0), (20, 0, -4.0, 0), (46, 0, -3.6, 0), (48, 0, 0.6, 0), (54, 0, 0, 0), (64, 0, 0, 0))
a.rot("body", (0, 0, 0, 0), (8, 10, 0, 0), (12, -16, 0, 0), (16, 10, 0, 0), (20, -26, 0, 0), (22, -22, 6, 0), (46, -22, 6, 0), (48, 12, 0, 0), (56, 8, 0, 0), (64, 0, 0, 0))
a.rot("chest", (0, 0, 0, 0), (8, 10, 0, 0), (20, -10, 0, 0), (22, -8, 10, 6), (46, -8, 10, 6), (48, 14, 0, 0), (56, 10, 0, 0), (64, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (6, 30, 0, 10), (8, 26, 0, -10), (10, 30, 0, 10), (14, 0, 0, 0), (20, 30, 0, 0), (22, 30, 20, 0), (46, 30, 20, 0),
      (48, 36, 0, 0), (51, 30, 0, -10), (54, 36, 0, 10), (57, 30, 0, -10), (64, 0, 0, 0))
a.rot("arm_l", (0, *REST["arm_l"]), (6, 170, 0, -20), (12, 160, 0, -20), (16, 176, 0, -10), (18, 120, 0, -12), (20, 56, 0, -18), (22, 40, 0, -24),
      (46, 40, 0, -24), (48, 172, 0, -14), (56, 168, 0, -16), (64, *REST["arm_l"]))
a.rot("fore_l", (0, *REST["fore_l"]), (6, 10, 0, 0), (20, 0, 0, 0), (46, 0, 0, 0), (48, 6, 0, 0), (64, *REST["fore_l"]))
a.rot("comp", (0, *REST["comp"]), (6, -90, 0, 0), (16, -90, 0, 0), (18, -100, 0, 0), (20, -126, 0, 0), (22, -100, 0, 0), (46, -100, 0, 0),
      (48, -90, 0, 0), (56, -90, 0, 0), (64, *REST["comp"]))
a.rot("c_needle", (0, 0, 4, 0), (6, 0, 40, 0), (16, 0, 40, 0), (20, 0, 10, 0), (22, 0, 6, 0), (46, 0, 6, 0), (48, 0, 40, 0), (58, 0, 40, 0), (64, 0, 4, 0))
a.rot("c_pencil", (0, 0, -4, 0), (6, 0, -40, 0), (16, 0, -40, 0), (20, 0, -26, 0), (22, 0, -30, 0), (46, 0, -30, 0), (48, 0, -40, 0), (58, 0, -40, 0), (64, 0, -4, 0))
a.rot("arm_r", (0, *REST["arm_r"]), (6, 20, 0, 70), (12, 10, 0, 60), (16, 160, 0, 10), (20, 50, 0, 16), (22, -10, 0, 64), (46, -10, 0, 64),
      (48, 40, 0, 80), (56, 30, 0, 76), (64, *REST["arm_r"]))
a.rot("fore_r", (0, 12, 0, 0), (6, 60, 0, 0), (20, 10, 0, 0), (22, 30, 0, 0), (46, 30, 0, 0), (48, 50, 0, 0), (64, 12, 0, 0))
a.rot("claws_r", (0, 14, 0, 0), (6, -30, 0, 0), (12, 40, 0, 0), (20, 40, 0, 0), (22, -16, 0, 0), (46, -16, 0, 0), (48, -40, 0, 0), (64, 14, 0, 0))
legs_both(a, [(0, 0, 0, 0), (8, 0, 0, 2), (12, 40, 0, 8), (15, -10, 0, 4), (17, 40, 0, 8), (20, 54, 0, 16), (22, 50, 0, 14), (46, 50, 0, 14),
              (48, 0, 0, 6), (54, 0, 0, 4), (64, 0, 0, 0)],
          [(0, 0, 0, 0), (12, -70, 0, 0), (15, -6, 0, 0), (17, -80, 0, 0), (20, -84, 0, 0), (22, -76, 0, 0), (46, -76, 0, 0), (48, -4, 0, 0), (64, 0, 0, 0)],
          [(0, 0, 0, 0), (12, 30, 0, 0), (15, -20, 0, 0), (20, 30, 0, 0), (46, 26, 0, 0), (48, 0, 0, 0)])
a.drape(HAIR_B, [(0, -2, 0, 0), (6, 10, 0, 0), (12, 0, 0, 0), (16, 30, 0, 0), (21, -50, 0, 0), (24, -40, 30, 0), (46, -44, 30, 0), (49, -60, 0, 0),
                 (54, -16, 0, 0), (64, -2, 0, 0)], delay=2, gain=0.85)
a.drape(HAIR_R, [(0, 0, 0, 1), (6, 0, 0, 14), (16, 20, 0, -10), (21, -10, 0, 50), (24, -14, 0, 40), (46, -14, 0, 44), (49, -20, 0, 60), (56, 0, 0, 10), (64, 0, 0, 1)], delay=2)
a.drape(HAIR_L, [(0, 0, 0, -1), (6, 0, 0, -14), (16, 20, 0, 10), (21, -10, 0, -50), (24, -14, 0, -40), (46, -14, 0, -44), (49, -20, 0, -60), (56, 0, 0, -10), (64, 0, 0, -1)], delay=2)
a.rot("bang", (0, 0, 0, 0), (6, 20, 0, 0), (21, -40, 0, 0), (24, -16, 0, -10), (46, -16, 0, -10), (49, -30, 0, 10), (58, 0, 0, 0))
a.rot("ear_r", (0, 0, 0, 0), (6, 0, 0, -16), (10, 0, 0, 0), (21, -30, 0, -20), (30, 0, 0, 0), (49, -20, 0, -20), (58, 0, 0, 0))
a.rot("ear_l", (0, 0, 0, 0), (7, 0, 0, 16), (11, 0, 0, 0), (21, -30, 0, 20), (30, 0, 0, 0), (49, -20, 0, 20), (58, 0, 0, 0))
a.done()

# ------------------------------------------------------------------ impale (40, canon): coil back, needle thrust 11, hoist the skewered victim
# overhead 12..22 (grin, claws flex), SLAM it down in front on 26, wrench the needle free 30, recover
a = A("impale", 40)
a.pos("body", (0, 0, 0, 0), (8, 0, -2.0, 1.4), (11, 0, -2.4, -1.4), (14, 0, -1.2, -0.8), (22, 0, 0.4, 0.2), (26, 0, -3.2, -1.6), (30, 0, -2.6, -1.0), (40, 0, 0, 0))
a.rot("body", (0, 0, 0, 0), (8, 8, 28, 0), (11, -14, -24, 0), (14, -8, -16, 0), (18, 8, -6, 0), (22, 14, 0, 0), (25, -18, 0, 0), (26, -30, 0, 0), (30, -24, 0, 0), (40, 0, 0, 0))
a.rot("chest", (0, 0, 0, 0), (8, 6, 18, 0), (11, -6, -14, 0), (22, 10, 0, -4), (26, -14, 0, 0), (30, -10, 6, 0), (40, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (8, -6, -30, 0), (11, 8, 28, 0), (16, 26, 10, 8), (22, 34, 0, -6), (26, 6, 0, 0), (30, -6, -10, 10), (34, -4, 0, 6), (40, 0, 0, 0))
a.rot("arm_l", (0, *REST["arm_l"]), (8, -24, 0, -10), (10, 40, 0, -4), (11, 88, 0, 2), (14, 96, 0, 0), (18, 140, 0, -6), (22, 168, 0, -8),
      (24, 150, 0, -6), (26, 54, 0, -4), (29, 50, 0, -4), (31, 74, 0, -10), (40, *REST["arm_l"]))
a.rot("fore_l", (0, *REST["fore_l"]), (8, 104, 0, 0), (11, 0, 0, 0), (22, 4, 0, 0), (26, 0, 0, 0), (31, 40, 0, 0), (40, *REST["fore_l"]))
a.rot("comp", (0, *REST["comp"]), (8, -100, 0, 0), (11, -90, 0, 0), (22, -90, 0, 0), (26, -96, 0, 0), (29, -96, 0, 0), (31, -60, 14, 0), (40, *REST["comp"]))
a.rot("hand_l", (0, 0, 0, 0), (14, 0, 0, 0), (16, 0, 0, 12), (18, 0, 0, -10), (20, 0, 0, 8), (22, 0, 0, 0), (29, 0, 0, 0), (30, 0, 30, 0), (31, 0, -20, 0), (34, 0, 0, 0))
a.rot("c_needle", (0, 0, 4, 0), (8, 0, 0, 0), (29, 0, 0, 0), (40, 0, 4, 0))
a.rot("c_pencil", (0, 0, -4, 0), (8, 0, -10, 0), (12, 0, -18, 0), (29, 0, -18, 0), (34, 0, -4, 0))
a.rot("arm_r", (0, *REST["arm_r"]), (8, 30, 0, 34), (11, -40, 0, 26), (16, 20, 0, 40), (20, 30, 0, 50), (22, 40, 0, 46), (26, -30, 0, 20), (32, 0, 0, 14), (40, *REST["arm_r"]))
a.rot("fore_r", (0, 12, 0, 0), (8, 40, 0, 0), (11, 20, 0, 0), (20, 60, 0, 0), (26, 10, 0, 0), (40, 12, 0, 0))
a.rot("claws_r", (0, 14, 0, 0), (8, 40, 0, 0), (11, -10, 0, 0), (16, 50, 0, 0), (18, 10, 0, 0), (20, 55, 0, 0), (22, 10, 0, 0), (26, -20, 0, 0), (40, 14, 0, 0))
a.rot("leg_l", (0, 0, 0, 0), (8, 24, 0, -4), (11, 50, 0, -6), (22, 34, 0, -4), (26, 56, 0, -6), (30, 50, 0, -6), (40, 0, 0, 0))
a.rot("shin_l", (0, 0, 0, 0), (8, -46, 0, 0), (11, -44, 0, 0), (22, -20, 0, 0), (26, -60, 0, 0), (30, -54, 0, 0), (40, 0, 0, 0))
a.rot("foot_l", (0, 0, 0, 0), (11, -6, 0, 0), (26, 4, 0, 0), (40, 0, 0, 0))
a.rot("leg_r", (0, 0, 0, 0), (8, -12, 0, 6), (11, -34, 0, 4), (22, -14, 0, 4), (26, -36, 0, 6), (30, -32, 0, 6), (40, 0, 0, 0))
a.rot("shin_r", (0, 0, 0, 0), (8, -30, 0, 0), (11, -8, 0, 0), (22, -6, 0, 0), (26, -20, 0, 0), (40, 0, 0, 0))
a.rot("foot_r", (0, 0, 0, 0), (11, 30, 0, 0), (22, 14, 0, 0), (26, 40, 0, 0), (40, 0, 0, 0))
a.drape(HAIR_B, [(0, -2, 0, 0), (8, 10, 20, 0), (11, -40, -10, 0), (16, -16, 0, 0), (22, 10, 0, 0), (26, -60, 0, 0), (31, -30, 0, 0), (40, -2, 0, 0)], delay=2, gain=0.85)
a.drape(HAIR_R, [(0, 0, 0, 1), (8, 10, 0, -8), (11, -24, 0, 18), (22, 6, 0, 4), (26, -30, 0, 34), (34, -4, 0, 4), (40, 0, 0, 1)], delay=2)
a.drape(HAIR_L, [(0, 0, 0, -1), (8, 10, 0, 8), (11, -24, 0, -18), (22, 6, 0, -4), (26, -30, 0, -34), (34, -4, 0, -4), (40, 0, 0, -1)], delay=2)
a.rot("bang", (0, 0, 0, 0), (11, -24, 0, 0), (22, 14, 0, 6), (26, -36, 0, -6), (32, 4, 0, 0), (40, 0, 0, 0))
a.rot("ear_r", (0, 0, 0, 0), (20, 0, 0, -12), (26, -20, 0, 0), (32, 0, 0, 0))
a.rot("ear_l", (0, 0, 0, 0), (20, 0, 0, 12), (26, -20, 0, 0), (32, 0, 0, 0))
a.done()

# ------------------------------------------------------------------ death (40 scrubbed): stagger, compass slips & sticks in the floor, kneel, slump forward
a = A("death", 40)
a.rot("head", (0, 0, 0, 0), (5, 30, 0, 10), (12, -10, 0, 16), (22, -30, 10, 20), (40, -24, 20, 24))
a.rot("chest", (0, 0, 0, 0), (5, 14, 0, 0), (12, -10, 0, 6), (22, -24, 0, 6), (40, -20, 0, 4))
a.pos("body", (0, 0, 0, 0), (5, 0, 0, 0.8), (14, 0, -6.0, 0), (40, 0, -6.0, 0))
a.rot("body", (0, 0, 0, 0), (5, 8, 0, 0), (14, -6, 0, 0), (40, -6, 0, 0))
legs_both(a, [(0, 0, 0, 0), (5, -6, 0, 2), (14, 84, 0, 6), (40, 84, 0, 6)], [(0, 0, 0, 0), (5, -10, 0, 0), (14, -96, 0, 0), (40, -96, 0, 0)],
          [(0, 0, 0, 0), (14, 40, 0, 0), (40, 40, 0, 0)])
a.pos("root", (0, 0, 0, 0), (20, 0, 0, 0), (32, 0, 1.6, -2.4), (40, 0, 1.4, -3.0))
a.rot("root", (0, 0, 0, 0), (20, 0, 0, 0), (30, -76, 0, 4), (34, -70, 0, 4), (40, -78, 0, 6))
a.rot("arm_l", (0, *REST["arm_l"]), (5, -20, 0, -30), (14, 50, 0, -20), (24, 60, 0, -20), (32, 150, 0, -30), (40, 160, 0, -30))
a.rot("fore_l", (0, *REST["fore_l"]), (5, 20, 0, 0), (14, 0, 0, 0), (40, 0, 0, 0))
a.rot("comp", (0, *REST["comp"]), (5, -40, 30, 0), (14, -130, 0, 0), (24, -126, 0, 0), (30, -200, 0, 30), (40, -210, 0, 40))
a.rot("hand_l", (0, 0, 0, 0), (24, 0, 0, 0), (30, 40, 0, 0), (40, 50, 0, 0))
a.rot("c_needle", (0, 0, 4, 0), (14, 0, 2, 0), (30, 0, 20, 0), (40, 0, 24, 0))
a.rot("c_pencil", (0, 0, -4, 0), (14, 0, -2, 0), (30, 0, -20, 0), (40, 0, -24, 0))
a.rot("arm_r", (0, *REST["arm_r"]), (5, 50, 0, -40), (12, 60, 0, -50), (24, 40, 0, -30), (32, 150, 0, 30), (40, 160, 0, 30))
a.rot("fore_r", (0, 12, 0, 0), (5, 80, 0, 0), (14, 70, 0, 0), (32, 10, 0, 0), (40, 10, 0, 0))
a.rot("claws_r", (0, 14, 0, 0), (5, 60, 0, 0), (24, 60, 0, 0), (40, 0, 0, 0))
a.drape(HAIR_B, [(0, -2, 0, 0), (5, -20, 0, 0), (14, 10, 0, 0), (30, 70, 0, 0), (34, 50, 0, 0), (40, 60, 0, 0)], delay=2, gain=0.85)
a.drape(HAIR_R, [(0, 0, 0, 1), (14, 0, 0, 20), (30, 30, 0, 40), (40, 30, 0, 44)], delay=2)
a.drape(HAIR_L, [(0, 0, 0, -1), (14, 0, 0, -20), (30, 30, 0, -40), (40, 30, 0, -44)], delay=2)
a.rot("bang", (0, 0, 0, 0), (14, 10, 0, 0), (30, 30, 0, 0), (40, 34, 0, 0))
a.rot("ear_r", (0, 0, 0, 0), (14, 0, 0, 0), (30, 30, 0, 20), (40, 40, 0, 30))
a.rot("ear_l", (0, 0, 0, 0), (14, 0, 0, 0), (30, 30, 0, -20), (40, 40, 0, -30))
a.done()

# ------------------------------------------------------------------ devour (44, canon): coil, claw lunge GRAB 10, haul the victim up to the
# shark grin, BITE 18, chew-shake, BITE 25, shake, toss aside 33, licks-her-lips recovery
a = A("devour", 44)
a.pos("body", (0, 0, 0, 0), (6, 0, -1.6, 1.2), (10, 0, -2.2, -1.4), (14, 0, -0.8, -0.6), (17, 0, -1.0, 0.2), (18, 0, -1.6, -1.0), (21, 0, -1.0, -0.4),
      (24, 0, -1.0, 0.2), (25, 0, -1.6, -1.0), (30, 0, -1.0, -0.4), (33, 0, -1.8, 0), (44, 0, 0, 0))
a.rot("body", (0, 0, 0, 0), (6, 10, -24, 0), (10, -16, 20, 0), (14, 6, 10, 0), (17, 10, 6, 0), (18, -12, 6, 0), (24, 8, 6, 0), (25, -12, 6, 0),
      (30, -4, 0, 0), (33, -6, 40, 0), (36, -4, 30, 0), (44, 0, 0, 0))
a.rot("chest", (0, 0, 0, 0), (6, 8, -14, 0), (10, -8, 14, 0), (15, 10, 0, 0), (18, -14, 0, 0), (21, -6, 0, 0), (23, 10, 0, 0), (25, -14, 0, 0),
      (30, -4, 0, 0), (33, -4, 20, 0), (44, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (3, 20, 0, 14), (6, 10, 30, 0), (10, -6, -10, 0), (15, 30, 0, 0), (18, -26, 0, 0), (19, -24, 0, 12), (20, -22, 0, -12),
      (21, -24, 0, 10), (23, 30, 0, 0), (25, -26, 0, 0), (26, -24, 0, -12), (27, -22, 0, 12), (28, -24, 0, -10), (30, -10, 0, 0),
      (33, 10, -20, 0), (38, 20, -10, 14), (44, 0, 0, 0))
# claw arm: drawn back, lunge-grab 10, haul up to the face, hold through the bites, fling out to her right on 33
a.rot("arm_r", (0, *REST["arm_r"]), (6, -40, 0, 34), (8, 20, 0, 20), (10, 92, 0, 4), (14, 120, 0, 0), (17, 116, 0, -2), (18, 108, 0, -4),
      (24, 116, 0, -2), (25, 108, 0, -4), (30, 112, 0, 0), (32, 100, 0, 30), (33, 60, 0, 90), (36, 40, 0, 70), (44, *REST["arm_r"]))
a.rot("fore_r", (0, 12, 0, 0), (6, 50, 0, 0), (10, 0, 0, 0), (14, 30, 0, 0), (30, 30, 0, 0), (33, 0, 0, 0), (44, 12, 0, 0))
a.rot("hand_r", (0, 0, 0, 0), (10, -20, 0, 0), (14, -40, 0, 0), (30, -40, 0, 0), (33, 0, 0, 0))
a.rot("claws_r", (0, 14, 0, 0), (6, -10, 0, 0), (9, -40, 0, 0), (11, 60, 0, 0), (30, 60, 0, 0), (32, 60, 0, 0), (33, -40, 0, 0), (38, -20, 0, 0), (44, 14, 0, 0))
# compass arm swung out wide for balance, clicks shut on each bite
a.rot("arm_l", (0, *REST["arm_l"]), (6, 30, 0, -40), (10, -20, 0, -50), (18, -10, 0, -56), (25, -10, 0, -56), (33, 20, 0, -30), (44, *REST["arm_l"]))
a.rot("fore_l", (0, *REST["fore_l"]), (10, 30, 0, 0), (33, 30, 0, 0), (44, *REST["fore_l"]))
a.rot("comp", (0, *REST["comp"]), (10, -30, 20, 0), (33, -30, 20, 0), (44, *REST["comp"]))
a.rot("c_needle", (0, 0, 4, 0), (10, 0, 20, 0), (17, 0, 20, 0), (18, 0, 1, 0), (22, 0, 20, 0), (25, 0, 1, 0), (29, 0, 20, 0), (40, 0, 4, 0))
a.rot("c_pencil", (0, 0, -4, 0), (10, 0, -20, 0), (17, 0, -20, 0), (18, 0, -1, 0), (22, 0, -20, 0), (25, 0, -1, 0), (29, 0, -20, 0), (40, 0, -4, 0))
a.rot("leg_r", (0, 0, 0, 0), (6, -14, 0, 4), (10, 40, 0, 4), (30, 34, 0, 4), (33, 20, 0, 8), (44, 0, 0, 0))
a.rot("shin_r", (0, 0, 0, 0), (6, -20, 0, 0), (10, -40, 0, 0), (30, -34, 0, 0), (44, 0, 0, 0))
a.rot("foot_r", (0, 0, 0, 0), (10, 4, 0, 0), (44, 0, 0, 0))
a.rot("leg_l", (0, 0, 0, 0), (6, 20, 0, -4), (10, -30, 0, -4), (30, -26, 0, -4), (44, 0, 0, 0))
a.rot("shin_l", (0, 0, 0, 0), (6, -40, 0, 0), (10, -10, 0, 0), (44, 0, 0, 0))
a.rot("foot_l", (0, 0, 0, 0), (10, 36, 0, 0), (30, 30, 0, 0), (44, 0, 0, 0))
a.drape(HAIR_B, [(0, -2, 0, 0), (6, 10, 10, 0), (10, -36, -10, 0), (15, -6, 0, 0), (18, -24, 0, 0), (21, -8, 0, 0), (25, -24, 0, 0), (29, -8, 0, 0),
                 (33, -20, -20, 0), (38, -6, 0, 0), (44, -2, 0, 0)], delay=2, gain=0.85)
a.drape(HAIR_R, [(0, 0, 0, 1), (6, 8, 0, -8), (10, -24, 0, 20), (18, -10, 0, 12), (25, -10, 0, 14), (33, -16, 0, 40), (40, 0, 0, 4), (44, 0, 0, 1)], delay=2)
a.drape(HAIR_L, [(0, 0, 0, -1), (6, 8, 0, 8), (10, -24, 0, -20), (18, -10, 0, -12), (25, -10, 0, -14), (33, -6, 0, -8), (40, 0, 0, -4), (44, 0, 0, -1)], delay=2)
a.rot("bang", (0, 0, 0, 0), (10, -20, 0, 0), (15, 14, 0, 4), (18, -24, 0, -6), (23, 14, 0, 4), (25, -24, 0, -6), (32, 0, 0, 0), (44, 0, 0, 0))
a.rot("ear_r", (0, 0, 0, 0), (3, 0, 0, -14), (6, 0, 0, 0), (18, -16, 0, -10), (24, 0, 0, 0), (25, -16, 0, -10), (31, 0, 0, 0))
a.rot("ear_l", (0, 0, 0, 0), (4, 0, 0, 14), (7, 0, 0, 0), (18, -16, 0, 10), (24, 0, 0, 0), (25, -16, 0, 10), (31, 0, 0, 0))
a.done()

# ------------------------------------------------------------------ pencilStab (32): pull pencils from the hip (4), clench them in the claw like
# daggers, three jabs 9/13/17 (right shoulder driving in), then a compass-needle finisher thrust 23 off the left side, recover
a = A("pencilStab", 32)
a.scl("pencils", (0, .001, .001, .001), (4, .001, .001, .001), (5, 1, 1, 1), (28, 1, 1, 1), (29, .001, .001, .001))
JAB = [(9, True), (11, False), (13, True), (15, False), (17, True), (19, False)]
arm_r = [(0, *REST["arm_r"]), (4, -36, 0, 24), (7, 30, 0, 14)]
fore_r = [(0, 12, 0, 0), (4, 40, 0, 0), (7, 90, 0, 0)]
hand_r = [(0, 0, 0, 0), (4, 0, 0, 0), (7, -110, 0, 0)]
body = [(0, 0, 0, 0), (4, 0, -16, 0), (7, -4, -10, 0)]
for t, ext in JAB:
    arm_r.append((t, 88 if ext else 30, 0, 4 if ext else 14))
    fore_r.append((t, 0 if ext else 90, 0, 0))
    hand_r.append((t, -86 if ext else -112, 0, 0))
    body.append((t, -10 if ext else -4, 24 if ext else 6, 0))
arm_r += [(21, 10, 0, 30), (23, -30, 0, 36), (26, -20, 0, 30), (32, *REST["arm_r"])]
fore_r += [(21, 60, 0, 0), (23, 40, 0, 0), (32, 12, 0, 0)]
hand_r += [(21, -40, 0, 0), (26, -20, 0, 0), (32, 0, 0, 0)]
body += [(21, 4, 10, 0), (23, -16, -30, 0), (27, -14, -26, 0), (32, 0, 0, 0)]
a.rot("arm_r", *arm_r).rot("fore_r", *fore_r).rot("hand_r", *hand_r).rot("body", *body)
a.rot("claws_r", (0, 14, 0, 0), (4, -20, 0, 0), (5, 60, 0, 0), (28, 60, 0, 0), (32, 14, 0, 0))
a.pos("body", (0, 0, 0, 0), (4, 0, -0.8, 0.6), (8, 0, -1.6, -0.6), (12, 0, -1.4, -0.4), (16, 0, -1.8, -1.0), (21, 0, -1.2, 0.4), (23, 0, -2.6, -1.4),
      (27, 0, -2.4, -1.2), (32, 0, 0, 0))
a.rot("chest", (0, 0, 0, 0), (4, 0, -10, 0), (9, -6, 10, 0), (11, -2, 4, 0), (13, -6, 10, 0), (15, -2, 4, 0), (17, -8, 12, 0), (21, 6, 6, 0),
      (23, -8, -16, 0), (32, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (4, -16, 20, 0), (7, 6, -10, 8), (9, 10, -24, 0), (13, 10, -24, -6), (17, 12, -26, 6), (21, 4, 0, 0), (23, 14, 30, 0),
      (28, 8, 20, 8), (32, 0, 0, 0))
a.rot("arm_l", (0, *REST["arm_l"]), (8, 20, 0, -36), (17, 20, 0, -36), (20, -20, 0, -8), (21, -24, 0, -10), (23, 88, 0, 2), (26, 86, 0, 2), (32, *REST["arm_l"]))
a.rot("fore_l", (0, *REST["fore_l"]), (17, 50, 0, 0), (21, 104, 0, 0), (23, 0, 0, 0), (26, 2, 0, 0), (32, *REST["fore_l"]))
a.rot("comp", (0, *REST["comp"]), (17, 0, 30, 0), (21, -100, 0, 0), (23, -90, 0, 0), (26, -90, 0, 0), (32, *REST["comp"]))
a.rot("c_needle", (0, 0, 4, 0), (21, 0, 0, 0), (27, 0, 0, 0), (32, 0, 4, 0))
a.rot("c_pencil", (0, 0, -4, 0), (21, 0, -12, 0), (27, 0, -12, 0), (32, 0, -4, 0))
a.rot("leg_r", (0, 0, 0, 0), (8, 34, 0, 4), (16, 40, 0, 4), (21, 10, 0, 4), (23, -34, 0, 4), (27, -32, 0, 4), (32, 0, 0, 0))
a.rot("shin_r", (0, 0, 0, 0), (8, -30, 0, 0), (16, -34, 0, 0), (21, -20, 0, 0), (23, -8, 0, 0), (32, 0, 0, 0))
a.rot("foot_r", (0, 0, 0, 0), (23, 34, 0, 0), (27, 30, 0, 0), (32, 0, 0, 0))
a.rot("leg_l", (0, 0, 0, 0), (8, -24, 0, -4), (16, -28, 0, -4), (21, 10, 0, -4), (23, 50, 0, -6), (27, 48, 0, -6), (32, 0, 0, 0))
a.rot("shin_l", (0, 0, 0, 0), (8, -10, 0, 0), (16, -10, 0, 0), (21, -40, 0, 0), (23, -46, 0, 0), (27, -44, 0, 0), (32, 0, 0, 0))
a.rot("foot_l", (0, 0, 0, 0), (8, 30, 0, 0), (16, 34, 0, 0), (21, 0, 0, 0), (32, 0, 0, 0))
a.drape(HAIR_B, [(0, -2, 0, 0), (4, 6, 10, 0), (9, -16, -14, 0), (11, -8, -6, 0), (13, -16, -14, 0), (15, -8, -6, 0), (17, -20, -16, 0),
                 (21, 4, 10, 0), (23, -34, 16, 0), (27, -16, 10, 0), (32, -2, 0, 0)], delay=2, gain=0.85)
a.drape(HAIR_R, [(0, 0, 0, 1), (9, -10, 0, 14), (13, -10, 0, 10), (17, -12, 0, 16), (23, -14, 0, 4), (32, 0, 0, 1)], delay=2)
a.drape(HAIR_L, [(0, 0, 0, -1), (9, -6, 0, -4), (17, -6, 0, -6), (23, -16, 0, -24), (30, -4, 0, -4), (32, 0, 0, -1)], delay=2)
a.rot("bang", (0, 0, 0, 0), (9, -10, 0, 6), (13, -6, 0, -4), (17, -12, 0, 6), (23, -24, 0, 0), (29, 4, 0, 0), (32, 0, 0, 0))
a.done()

# ------------------------------------------------------------------ pounce (40): deep crouch + compass cocked back, LEAP 8, airborne tuck with the
# compass raised overhead 10..16, needle-first plunge landing 20 (legs split), hold, wrench it free 27, straighten up
a = A("pounce", 40)
a.pos("root", (0, 0, 0, 0), (8, 0, 0, 0), (11, 0, 7.0, 0), (14, 0, 9.0, 0), (17, 0, 6.0, 0), (19, 0, 1.6, 0), (20, 0, 0, 0), (40, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (6, 0, -3.6, 0.8), (8, 0, -0.4, 0), (12, 0, 0.6, 0), (17, 0, 0, 0), (20, 0, -4.2, -0.6), (26, 0, -3.8, -0.6),
      (29, 0, -1.6, 0), (40, 0, 0, 0))
a.rot("body", (0, 0, 0, 0), (6, -26, 0, 0), (8, 10, 0, 0), (12, 16, 0, 0), (17, 6, 0, 0), (20, -32, 0, 0), (26, -28, 0, 0), (29, 6, 0, 0), (34, 4, 0, 0), (40, 0, 0, 0))
a.rot("chest", (0, 0, 0, 0), (6, -10, 6, 0), (12, 14, 0, 0), (17, 8, 0, 0), (20, -14, 0, 0), (26, -12, 0, 0), (29, 10, 0, 0), (40, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (3, 10, 0, 12), (6, 40, 0, 0), (12, 0, 0, 0), (17, -10, 0, 0), (20, 30, 0, 0), (24, 34, 0, 8), (27, 30, 0, -6),
      (29, 10, 0, 0), (34, 14, 0, 10), (40, 0, 0, 0))
a.rot("arm_l", (0, *REST["arm_l"]), (6, -50, 0, -20), (8, 30, 0, -16), (12, 172, 0, -10), (16, 176, 0, -8), (18, 120, 0, -12), (20, 58, 0, -14),
      (26, 60, 0, -14), (28, 120, 0, -20), (30, 130, 0, -22), (40, *REST["arm_l"]))
a.rot("fore_l", (0, *REST["fore_l"]), (6, 20, 0, 0), (12, 20, 0, 0), (18, 0, 0, 0), (26, 4, 0, 0), (29, 30, 0, 0), (40, *REST["fore_l"]))
a.rot("comp", (0, *REST["comp"]), (6, -100, 0, 0), (12, -20, 0, 0), (16, -10, 0, 0), (18, -70, 0, 0), (20, -126, 0, 0), (26, -124, 0, 0),
      (28, -60, 10, 0), (31, -40, 20, 0), (40, *REST["comp"]))
a.rot("hand_l", (0, 0, 0, 0), (21, 0, 0, 0), (22, 0, 0, 8), (23, 0, 0, -6), (24, 0, 0, 4), (25, 0, 0, 0), (26, 0, 20, 0), (27, 0, -24, 0), (29, 0, 0, 0))
a.rot("c_needle", (0, 0, 4, 0), (12, 0, 0, 0), (20, 0, 0, 0), (27, 0, 0, 0), (34, 0, 4, 0))
a.rot("c_pencil", (0, 0, -4, 0), (12, 0, -24, 0), (20, 0, -30, 0), (27, 0, -30, 0), (34, 0, -4, 0))
a.rot("arm_r", (0, *REST["arm_r"]), (6, -50, 0, 30), (8, 40, 0, 40), (12, 100, 0, 60), (17, 90, 0, 50), (20, 30, 0, 50), (26, 30, 0, 46),
      (30, 10, 0, 30), (40, *REST["arm_r"]))
a.rot("fore_r", (0, 12, 0, 0), (6, 40, 0, 0), (12, 20, 0, 0), (20, 40, 0, 0), (40, 12, 0, 0))
a.rot("claws_r", (0, 14, 0, 0), (6, 30, 0, 0), (10, -40, 0, 0), (17, -30, 0, 0), (20, 50, 0, 0), (28, 50, 0, 0), (40, 14, 0, 0))
legs_both(a, [(0, 0, 0, 0), (6, 50, 0, 8), (8, -20, 0, 4), (11, 60, 0, 6), (16, 64, 0, 8), (19, 30, 0, 14), (20, 54, 0, 16), (26, 52, 0, 16),
              (29, 20, 0, 6), (40, 0, 0, 0)],
          [(0, 0, 0, 0), (6, -84, 0, 0), (8, -4, 0, 0), (11, -100, 0, 0), (16, -104, 0, 0), (19, -40, 0, 0), (20, -84, 0, 0), (26, -80, 0, 0),
           (29, -30, 0, 0), (40, 0, 0, 0)],
          [(0, 0, 0, 0), (6, 34, 0, 0), (8, -30, 0, 0), (12, 20, 0, 0), (19, 0, 0, 0), (20, 30, 0, 0), (26, 28, 0, 0), (32, 0, 0, 0)])
a.drape(HAIR_B, [(0, -2, 0, 0), (6, 14, 0, 0), (9, -40, 0, 0), (13, -50, 0, 0), (16, 20, 0, 0), (19, 40, 0, 0), (21, -60, 0, 0), (26, -24, 0, 0),
                 (30, -8, 0, 0), (40, -2, 0, 0)], delay=2, gain=0.85)
a.drape(HAIR_R, [(0, 0, 0, 1), (6, 10, 0, 10), (9, -30, 0, 30), (16, 20, 0, -6), (21, -20, 0, 50), (28, -4, 0, 16), (40, 0, 0, 1)], delay=2)
a.drape(HAIR_L, [(0, 0, 0, -1), (6, 10, 0, -10), (9, -30, 0, -30), (16, 20, 0, 6), (21, -20, 0, -50), (28, -4, 0, -16), (40, 0, 0, -1)], delay=2)
a.rot("bang", (0, 0, 0, 0), (6, 16, 0, 0), (9, -30, 0, 0), (16, 20, 0, 4), (21, -40, 0, 0), (28, -8, 0, 0), (40, 0, 0, 0))
a.rot("ear_r", (0, 0, 0, 0), (9, -30, 0, -10), (16, 10, 0, 6), (21, -30, 0, -20), (30, 0, 0, 0))
a.rot("ear_l", (0, 0, 0, 0), (9, -30, 0, 10), (16, 10, 0, -6), (21, -30, 0, 20), (30, 0, 0, 0))
a.done()

# ------------------------------------------------------------------ scale: the shipped model was hand-scaled to 2.92 blocks (max y 46.72)
SCALE = 1.1124
for c in m.cubes:
    for key in ("from", "to", "origin"):
        c[key] = [round(v * SCALE, 3) for v in c[key]]
    c["inflate"] = round(c["inflate"] * SCALE, 3)
for g in m.groups.values():
    g["origin"] = [round(v * SCALE, 3) for v in g["origin"]]
for an in m.anims:
    for bone in an["animators"].values():
        for kf in bone["keyframes"]:
            if kf["channel"] == "position":
                kf["data_points"] = [{k: round(v * SCALE, 3) for k, v in dp.items()} for dp in kf["data_points"]]

os.makedirs(os.path.dirname(OUT), exist_ok=True)
m.save(OUT)
print("max y", max(c["to"][1] for c in m.cubes))
print("cubes", len(m.cubes), "anims", [x["name"] for x in m.anims], "atlas rows used", m.cy + m.rowh)
