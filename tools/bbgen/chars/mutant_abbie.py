"""Mutant Abbie (FPE Green mutant student, ABBIE 005) - generates assets/fpe/bbmodels/mutant_abbie.bbmodel.
Reference: docs/ref/confirmed/mutant_abbie.png. All-black ink silhouette with thin white crack lines, a huge spiky mane,
a zig-zag white stalk with one leaf sprouting from the crown, hunched and hugging herself (arms crossed over the chest, claw
fingers gripping the opposite arm), long thin legs with pointed feet, a big clawed mutant limb growing from her right hip
(viewer left) and a jagged tail rising on her left (viewer right). Only colour: a faint pink mouth / eye slits (glow).
Blockbench space: Y up, ground 0, faces -Z. Character's RIGHT = +X.
Rotation signs: arm/leg rx>0 = swing forward, torso/head rx>0 = lean back / look up, ry>0 = turn to the character's left,
rz>0 = toward +X / (for a +X pointing chain) up. Position z<0 = forward, y>0 = up.
Rest rotations live in the groups (hunch, crossed arms, tail curve, limb bend); animations add on top of them.
Every key tick matches entity/characters/MutantAbbie.java.  Run: python3 tools/bbgen/chars/mutant_abbie.py
"""
import math, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from bbgen import Model, mix  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "../../../src/main/resources/assets/fpe/bbmodels/mutant_abbie.bbmodel")

BLK, BLK2, BLK3 = 0x100F14, 0x1B1A21, 0x2A2832
CRACK, CRACK_D = 0xC9C7D2, 0x6E6B7A
STEM, STEM_D, LEAF, LEAF_D, LEAF_L = 0xE9EDE6, 0x9EA59A, 0xEEF3EA, 0xA9B3A4, 0xFFFFFF
PINK, PINK_D, PINK_G = 0xA8586A, 0x3A1B24, 0x7A3446
CLEAR = (0, 0, 0, 0)
ALL = ("north", "south", "east", "west", "up", "down")

m = Model("mutant_abbie", S=8, atlas=2048)
R = m.rng


# ------------------------------------------------------------------ painters
def all_faces(fn, skip=()):
    return {k: fn for k in ALL if k not in skip}


def crack(F, n=None, col=CRACK):
    """thin white crack lines like the sketch: random walks with small branches"""
    n = n if n is not None else (F.w * F.h) // 900 + (1 if R.random() < 0.6 else 0)
    for _ in range(n):
        x, y = R.uniform(1, F.w - 2), R.uniform(0, F.h * 0.4)
        dx = R.uniform(-0.6, 0.6)
        for k in range(R.randint(F.h // 3, F.h)):
            F.px(int(x), int(y), col if k % 9 else CRACK_D)
            x += dx + R.uniform(-0.7, 0.7); y += 1
            if R.random() < 0.05:
                bx, by = x, y
                for j in range(R.randint(2, 6)):
                    bx += R.choice((-1, 1)); by += R.uniform(0, 1)
                    F.px(int(bx), int(by), CRACK_D)
            if not (0 <= x < F.w): break


def ink(cracks=True, rim=True):
    def f(F):
        for y in range(F.h):
            for x in range(F.w):
                k = y / max(1, F.h - 1)
                c = mix(BLK2, BLK, min(1, 0.3 + k)) if rim else BLK
                F.px(x, y, BLK3 if R.random() < 0.025 else c)
        if rim: F.rect(0, 0, F.w, 1, BLK3)
        if cracks: crack(F)
    return f


def tri(col=BLK, accent=False, tipup=True):
    """triangle on a side face (tip at top when tipup), outside transparent, faint rim, optional crack down the middle"""
    def f(F):
        for y in range(F.h):
            for x in range(F.w):
                v = (y + .5) / F.h
                v = v if tipup else 1 - v          # 0 at tip, 1 at base
                half = 0.5 * v
                d = abs((x + .5) / F.w - 0.5)
                if d > half + 0.02: F.px(x, y, CLEAR)
                elif d > half - 1.2 / F.w: F.px(x, y, BLK3)
                else: F.px(x, y, mix(BLK2, col, 0.4 + 0.6 * v))
        if accent:
            for y in range(int(F.h * 0.25), F.h):
                F.px(F.w // 2 + (1 if (y // 5) % 2 else 0), y, CRACK_D if y % 7 else CRACK)
    return f


def clear(F):
    F.rect(0, 0, F.w, F.h, CLEAR)


def fill(c):
    return lambda F: F.rect(0, 0, F.w, F.h, c)


# ------------------------------------------------------------------ shape helpers
def edged(F):
    """ink + a thin grey contour so overlapping black limbs stay readable (the sketch's white outlines)"""
    ink(True)(F)
    for x in range(F.w):
        F.px(x, 0, CRACK_D); F.px(x, F.h - 1, CRACK_D)
    for y in range(F.h):
        F.px(0, y, CRACK_D); F.px(F.w - 1, y, CRACK_D)


def box(name, parent, a, b, faces=None, rot=(0, 0, 0), origin=None, cracks=True, col=BLK, edge=False):
    return m.cube(name, parent, a, b, col, origin=origin, rot=rot, faces=faces or all_faces(edged if edge else ink(cracks)))


def spk(name, parent, base, h, w, rot=(0, 0, 0), d=None, accent=None, col=BLK):
    """pyramid spike from base pointing +Y (before rot), base face filled"""
    x, y, z = base
    d = d or w
    p = tri(col, R.random() < 0.3 if accent is None else accent)
    m.cube(name, parent, (x - w / 2, y, z - d / 2), (x + w / 2, y + h, z + d / 2), col, origin=base, rot=rot,
           faces={"north": p, "south": p, "east": p, "west": p, "up": clear, "down": fill(BLK)})


def spk_dir(name, parent, base, h, w, yaw, pitch, d=None, accent=None):
    """spike pointing along a direction: yaw 0 = +X, 90 = up (rz), pitch tilts toward -Z (forward) / +Z"""
    spk(name, parent, base, h, w, rot=(pitch, 0, yaw - 90 if yaw <= 90 else yaw - 90), d=d, accent=accent)


# ------------------------------------------------------------------ skeleton (rest rotations = the reference pose)
m.group("root", (0, 0, 0))
m.group("body", (0, 13.4, 0), parent="root")
m.group("chest", (0, 15.2, 0), rot=(-16, 0, 0), parent="body")
m.group("head", (0, 23.4, -0.4), rot=(10, 0, -4), parent="chest")
m.group("mouth", (-0.9, 25.0, -3.3), parent="head")
m.group("hair_f", (0, 28.4, -3.3), parent="head")
m.group("hair_r", (3.3, 27.8, 0), parent="head")
m.group("hair_l", (-3.3, 27.8, 0), parent="head")
m.group("hair_b", (0, 28.6, 3.2), parent="head")
m.group("sprout", (0.2, 30.4, 0.0), rot=(0, 0, -6), parent="head")
m.group("stem2", (0.9, 33.4, 0.0), rot=(0, 0, 28), parent="sprout")
m.group("stem3", (-0.4, 36.0, 0.0), rot=(0, 0, -30), parent="stem2")
m.group("leaf", (0.4, 38.6, 0.0), rot=(0, 0, 20), parent="stem3")
# arms: upper arm hangs from the shoulder, forearm modelled crossing the chest (hug); unfolding = ry
m.group("arm_r", (3.5, 22.4, 0.0), rot=(18, 0, 6), parent="chest")
m.group("fore_r", (3.7, 17.6, -0.3), rot=(0, 0, -24), parent="arm_r")
m.group("hand_r", (-2.3, 17.6, -2.9), parent="fore_r")
m.group("arm_l", (-3.5, 22.4, 0.0), rot=(14, 0, -6), parent="chest")
m.group("fore_l", (-3.7, 17.9, -0.3), rot=(0, 0, 28), parent="arm_l")
m.group("hand_l", (2.4, 17.9, -2.1), parent="fore_l")
for s, k in ((1, "r"), (-1, "l")):
    m.group("leg_" + k, (1.3 * s, 13.4, 0), rot=(0, 0, 3 * s), parent="body")
    m.group("shin_" + k, (1.3 * s, 7.0, 0), parent="leg_" + k)
# mutant limb from the right hip (+X), modelled straight along +X, bent by rest rotations
m.group("limb", (2.4, 12.9, 0.9), rot=(0, 18, -22), parent="body")
m.group("limb_fore", (6.6, 12.9, 0.9), rot=(0, 0, -34), parent="limb")
m.group("limb_hand", (10.4, 12.9, 0.9), rot=(0, 0, -12), parent="limb_fore")
# jagged tail from the left hip (-X), modelled straight along -X
m.group("tail1", (-1.2, 13.2, 1.5), rot=(0, 24, -22), parent="body")
m.group("tail2", (-4.8, 13.2, 1.5), rot=(0, 0, -26), parent="tail1")
m.group("tail3", (-8.2, 13.2, 1.5), rot=(0, 0, -22), parent="tail2")
m.group("tail4", (-11.2, 13.2, 1.5), rot=(0, 0, 14), parent="tail3")
# props
m.group("hleaf", (-2.3, 16.6, -3.6), parent="hand_r")
m.group("thorns", (0, 0, 0), parent="root")

# ------------------------------------------------------------------ legs: long, thin, flaring a little to pointed feet
for s, k in ((1, "r"), (-1, "l")):
    x = 1.3 * s
    box("thigh_" + k, "leg_" + k, (x - 0.95, 7.0, -0.95), (x + 0.95, 13.6, 0.95))
    box("knee_" + k, "shin_" + k, (x - 0.85, 6.0, -0.9), (x + 0.85, 7.4, 0.9), cracks=False)
    box("calf_" + k, "shin_" + k, (x - 1.0, 1.4, -1.0), (x + 1.0, 6.2, 1.0))
    box("cuff_" + k, "shin_" + k, (x - 1.25, 0.6, -1.25), (x + 1.25, 2.2, 1.2), cracks=False)
    box("foot_" + k, "shin_" + k, (x - 1.05, 0.0, -2.6), (x + 1.05, 1.1, 1.1), cracks=False)
    spk("toe_" + k, "shin_" + k, (x + 0.1 * s, 0.55, -2.5), 2.0, 1.1, rot=(-90, 0, 0), accent=False)
    spk("heel_" + k, "shin_" + k, (x, 0.6, 1.0), 1.1, 0.9, rot=(100, 0, 0), accent=False)

# ------------------------------------------------------------------ hips + torso (slim waist, raised hunched shoulders, spine spikes)
box("pelvis", "body", (-2.4, 12.6, -1.5), (2.4, 15.6, 1.6))
box("waist", "chest", (-2.1, 15.2, -1.35), (2.1, 18.4, 1.45))
box("ribs", "chest", (-2.9, 18.2, -1.75), (2.9, 22.4, 1.85))
box("collar", "chest", (-2.2, 22.2, -1.4), (2.2, 23.2, 1.5), cracks=False)
box("neck", "chest", (-0.9, 22.8, -0.9), (0.9, 24.4, 0.8), cracks=False)
for s, k in ((1, "r"), (-1, "l")):
    box("shoulder_" + k, "chest", (2.3 * s - 1.4, 21.0, -1.4), (2.3 * s + 1.4, 23.6, 1.5), rot=(0, 0, -14 * s), origin=(2.3 * s, 22.3, 0))
for i, (y, h) in enumerate(((16.6, 1.3), (18.6, 1.7), (20.8, 2.0), (22.8, 1.6))):
    spk(f"spine{i}", "chest", (0, y, 1.6), h, 0.9, rot=(70, 0, 0))

# ------------------------------------------------------------------ arms: crossed over the chest, claw fingers gripping the other arm
for s, k in ((1, "r"), (-1, "l")):
    box("upper_" + k, "arm_" + k, (3.5 * s - 0.85, 17.4, -1.15), (3.5 * s + 0.85, 22.6, 0.75), edge=True)
    box("elbow_" + k, "arm_" + k, (3.6 * s - 0.9, 16.9, -1.2), (3.6 * s + 0.9, 18.3, 0.8), cracks=False)
# right forearm crosses in front (z -3.5..-2.2), left one behind it (z -2.9..-1.6)
box("forearm_r", "fore_r", (-2.3, 16.85, -3.6), (3.8, 18.35, -2.1), edge=True)
box("wrist_r", "fore_r", (-2.6, 16.95, -3.75), (-1.6, 18.25, -1.95), cracks=False)
box("forearm_l", "fore_l", (-3.8, 17.15, -2.9), (2.4, 18.65, -1.4), edge=True)
box("wrist_l", "fore_l", (1.9, 17.25, -3.05), (2.9, 18.55, -1.25), cracks=False)
for s, k in ((1, "r"), (-1, "l")):
    hx = -2.3 if s > 0 else 2.4
    hy = 17.6 if s > 0 else 17.9
    hz = -2.9 if s > 0 else -2.1
    box("palm_" + k, "hand_" + k, (hx - 0.6, hy - 0.9, hz - 0.8), (hx + 0.6, hy + 0.9, hz + 0.9), cracks=False)
    for i, (dy, ln) in enumerate(((0.6, 2.4), (0.0, 2.8), (-0.6, 2.3))):
        # claw fingers curl down over the opposite upper arm
        spk(f"claw{i}_{k}", "hand_" + k, (hx - 0.9 * s, hy + dy, hz + 0.3), ln, 0.55, rot=(14, 0, 150 * s + i * 8 * s), accent=False)
    spk(f"thumb_{k}", "hand_" + k, (hx - 0.2 * s, hy + 0.8, hz - 0.7), 1.6, 0.5, rot=(-30, 0, 30 * s), accent=False)

# ------------------------------------------------------------------ the mutant limb: thick arm out of the right hip ending in a huge claw
box("limb_up", "limb", (2.2, 11.9, 0.0), (6.8, 13.9, 1.8), edge=True)
box("limb_bulge", "limb", (3.2, 11.5, -0.2), (5.6, 14.2, 2.0), cracks=False)
box("limb_lo", "limb_fore", (6.4, 12.0, 0.1), (10.6, 13.8, 1.7), edge=True)
box("limb_wrist", "limb_fore", (9.6, 11.7, -0.1), (10.9, 14.1, 1.9), cracks=False)
box("lpalm", "limb_hand", (10.4, 11.3, -0.6), (13.0, 14.6, 2.4), edge=True)
box("lknuck", "limb_hand", (12.6, 11.6, -0.3), (13.6, 14.3, 2.1), cracks=False)
for i, (dy, yaw, ln) in enumerate(((1.6, 26, 4.6), (0.4, 0, 5.4), (-0.8, -24, 5.0), (-1.4, -52, 3.8))):
    # fingers along +X: rz = yaw - 90 maps +Y spike onto +X, then spread
    spk(f"lclaw{i}", "limb_hand", (13.3, 12.9 + dy, 0.9 - 0.5 * i + 0.8), ln, 1.4, rot=(0, 0, -90 + yaw), d=1.1, accent=False)
spk("lthumb", "limb_hand", (11.2, 14.4, 0.4), 3.0, 1.2, rot=(-20, 0, -30), accent=False)
for i, x in enumerate((3.6, 5.6, 8.0)):
    spk(f"limbspk{i}", "limb" if x < 6.5 else "limb_fore", (x, 13.8, 1.0), 1.4, 0.7, rot=(10, 0, -20))

# ------------------------------------------------------------------ tail: tapering segments with jagged spikes on both edges, spiky tip
TAIL = [("tail1", -1.0, -4.9, 1.8), ("tail2", -4.7, -8.3, 1.6), ("tail3", -8.1, -11.3, 1.35), ("tail4", -11.1, -13.6, 1.1)]
for j, (g, x0, x1, t) in enumerate(TAIL):
    box(f"{g}_c", g, (x1, 13.2 - t / 2, 1.5 - t / 2), (x0, 13.2 + t / 2, 1.5 + t / 2))
    for i in range(2):
        x = x0 + (x1 - x0) * (0.3 + 0.45 * i)
        spk(f"{g}_su{i}", g, (x, 13.2 + t / 2 - 0.1, 1.5), 1.2 + 0.5 * (j % 2) + 0.3 * i, 0.8, rot=(0, 0, 38 + 10 * i))
        spk(f"{g}_sd{i}", g, (x + 0.6, 13.2 - t / 2 + 0.1, 1.5), 0.9 + 0.4 * i, 0.7, rot=(0, 0, 180 - 30), accent=False)
spk("tail_tip", "tail4", (-13.4, 13.2, 1.5), 3.6, 1.2, rot=(0, 0, 90), accent=True)
spk("tail_tip2", "tail4", (-12.8, 13.5, 1.5), 2.2, 0.9, rot=(0, 0, 50))
spk("tail_tip3", "tail4", (-12.8, 12.9, 1.5), 1.8, 0.8, rot=(0, 0, 130), accent=False)


# ------------------------------------------------------------------ head: black skull, faint pink eye slits + small mouth (glow)
def face(F):
    W, H = F.w, F.h
    ink(cracks=False, rim=False)(F)
    for y in range(H):        # hair shadow at the top
        for x in range(W):
            if y < 8: F.px(x, y, BLK)
    ey = int(H * 0.47)
    for (cx, wl, sl) in ((W * 0.30, 7, 0.25), (W * 0.70, 9, -0.3)):
        for i in range(-wl, wl + 1):
            yy = ey + int(i * sl) + (1 if abs(i) > wl - 2 else 0)
            F.px(int(cx + i), yy, PINK_G, glow=True)
            if abs(i) < wl - 2: F.px(int(cx + i), yy + 1, PINK_D)
    F.line(W * 0.62, H * 0.18, W * 0.55, H * 0.36, CRACK_D, 1)
    F.line(W * 0.18, H * 0.65, W * 0.08, H * 0.9, CRACK_D, 1)


box("skull", "head", (-3.2, 23.4, -3.2), (3.2, 29.4, 3.0), faces={"north": face, "south": ink(), "east": ink(), "west": ink(), "up": ink(False), "down": ink(False)})
box("jaw", "head", (-2.6, 23.0, -3.0), (2.6, 24.2, 2.2), cracks=False)


def mouthp(F):
    F.rect(0, 0, F.w, F.h, PINK_D)
    for x in range(F.w):
        y = int(F.h / 2 + math.sin(x / max(1, F.w) * math.pi * 3) * F.h * 0.2)
        F.px(x, y, PINK, glow=True)
    F.rect(0, 0, F.w, 1, PINK_G, glow=True)


m.cube("mouth_c", "mouth", (-2.3, 24.6, -3.42), (0.5, 25.4, -3.15), PINK_D, faces={"north": mouthp, "south": fill(PINK_D), "east": fill(PINK_D), "west": fill(PINK_D),
                                                                                   "up": fill(PINK_D), "down": fill(PINK_D)})
# mane volume
box("hair_cap", "head", (-3.7, 26.0, -3.5), (3.7, 30.3, 3.6))
box("hair_back", "hair_b", (-3.6, 22.8, 2.6), (3.6, 29.6, 4.0))
# front fringe: downward spikes over the face
for i, (x, h, rz) in enumerate(((-2.8, 3.2, 10), (-1.5, 4.2, 4), (-0.2, 3.4, -6), (1.1, 4.6, 8), (2.5, 3.6, -10), (3.3, 2.6, -24))):
    spk(f"fringe{i}", "hair_f", (x, 29.0, -3.4), h, 1.5, rot=(-180 + 8, 0, 180 + rz), d=0.9)
# side mane: long spikes flaring out (right side longer, like the art)
SIDE = {"r": [(28.4, 10.0, 10, -6), (27.0, 11.5, -8, 4), (25.6, 9.0, -26, 0), (24.2, 7.0, -42, 6), (29.6, 7.5, 34, 0), (23.2, 5.0, -60, -6)],
        "l": [(28.6, 8.0, 14, -4), (27.0, 9.0, -6, 2), (25.4, 7.0, -26, 4), (23.8, 5.2, -46, 0), (29.8, 6.0, 42, 0)]}
for k, s in (("r", 1), ("l", -1)):
    for i, (y, ln, yaw, pz) in enumerate(SIDE[k]):
        # spike points +X (s=1) / -X (s=-1), tilted up by yaw degrees
        rz = (-90 + yaw) if s > 0 else (90 - yaw)
        spk(f"mane{i}_{k}", "hair_" + k, (3.0 * s, y, -0.6 + 0.5 * (i % 3)), ln, 2.8 - 0.2 * i, rot=(pz, 0, rz), d=1.8)
# crown spikes up/back
for i, (x, z, h, rz, rx) in enumerate(((-2.4, 0.5, 4.0, 30, 10), (-0.8, -1.0, 5.2, 8, -6), (1.0, 0.2, 4.6, -16, 4), (2.6, 1.4, 3.8, -38, 16),
                                         (0.0, 2.2, 4.2, 0, 40), (-1.8, 2.6, 3.4, 26, 46), (1.8, 2.4, 3.6, -26, 50))):
    spk(f"crown{i}", "head", (x, 29.9, z), h, 1.8, rot=(rx, 0, rz), d=1.6)
# back mane hanging down to the shoulders
for i, (x, h, rz) in enumerate(((-3.0, 5.6, -14), (-1.5, 6.6, -6), (0.0, 7.2, 0), (1.5, 6.4, 6), (3.0, 5.4, 16))):
    spk(f"backm{i}", "hair_b", (x, 23.4, 3.4), h, 1.8, rot=(180 - 18, 0, 180 + rz), d=1.2)


# ------------------------------------------------------------------ sprout: zig-zag white stalk + one leaf (FPE Green)
def stemp(F):
    for y in range(F.h):
        for x in range(F.w):
            F.px(x, y, mix(STEM, STEM_D, 0.15 + 0.5 * abs(x / max(1, F.w - 1) - 0.5)))
    F.rect(0, 0, 1, F.h, STEM_D); F.rect(F.w - 1, 0, 1, F.h, STEM_D)


for i, (g, y0, y1, x) in enumerate((("sprout", 29.8, 33.6, 0.2), ("stem2", 33.2, 36.2, 0.9), ("stem3", 35.8, 38.8, -0.4))):
    m.cube(f"stem{i}", g, (x - 0.24, y0 - 0.3, -0.24), (x + 0.24, y1 + 0.4, 0.24), STEM, faces=all_faces(stemp))


def leafp(F):
    W, H = F.w, F.h
    F.rect(0, 0, W, H, CLEAR)
    for y in range(H):
        for x in range(W):
            u = (x + .5) / W                     # 0 = stem end, 1 = tip
            half = 0.5 * math.sin(math.pi * min(1, u * 1.05)) ** 0.8 * (1 - 0.25 * u)
            v = abs((y + .5) / H - 0.5)
            if v < half - 1.4 / H: F.px(x, y, mix(LEAF_L, LEAF_D, 0.15 + 0.4 * v / max(0.01, half)))
            elif v < half: F.px(x, y, STEM_D)
    F.line(0, H / 2, W - 2, H / 2 - 1, LEAF_D, 1)
    for i in range(1, 4):
        x0 = W * i / 4.5
        F.line(x0, H / 2, x0 + W * 0.1, H * 0.25, LEAF_D, 1)
        F.line(x0, H / 2, x0 + W * 0.1, H * 0.75, LEAF_D, 1)


def leafp_s(F):
    """south face: mirrored so the stem end stays at +X"""
    leafp(F)
    for y in range(F.h):
        row = [F.cv.get(F.x + x, F.y + y) for x in range(F.w)]
        for x in range(F.w):
            F.cv.set(F.x + x, F.y + y, row[F.w - 1 - x])


# leaf points toward the viewer's right (-X); north texel 0 = +X side = stem end
m.cube("leaf_c", "leaf", (-5.6, 37.6, -0.1), (0.4, 40.0, 0.1), LEAF,
       faces={"north": leafp, "south": leafp_s, "east": clear, "west": clear, "up": clear, "down": clear})
m.cube("hleaf_c", "hleaf", (-2.6, 16.0, -6.4), (-2.4, 17.6, -3.6), LEAF,
       faces={"east": leafp, "west": leafp, "north": clear, "south": clear, "up": clear, "down": clear})

# ------------------------------------------------------------------ props: ring of black thorns (curl_guard / bramble_bloom)
for i in range(10):
    a = math.radians(i * 36 + 18)
    x, z = math.sin(a) * 7.5, math.cos(a) * 7.5
    spk(f"thorn{i}", "thorns", (x, 0, z), 7.0 if i % 2 else 5.0, 1.8, rot=(math.degrees(math.cos(a)) * 0.35, 0, -math.degrees(math.sin(a)) * 0.35), accent=True)
    spk(f"thornb{i}", "thorns", (x * 0.7, 0, z * 0.7), 3.0, 1.1, rot=(-math.degrees(math.cos(a)) * 0.3, 0, math.degrees(math.sin(a)) * 0.3), accent=False)


# ================================================================== animation
PROPS = ["thorns", "hleaf"]
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

    def show(self, bone, t0, t1, grow=2, size=1.0):
        g = size
        return self.scl(bone, (0, *HIDE), (max(0, t0 - 0.5), *HIDE), (t0, .3 * g, .3 * g, .3 * g), (t0 + grow, 1.15 * g, 1.15 * g, 1.15 * g),
                        (t0 + grow + 1, g, g, g), (t1, g, g, g), (t1 + 1, .3 * g, .3 * g, .3 * g), (t1 + 1.5, *HIDE), (self.ticks, *HIDE))

    def lag(self, bone, keys, delay=2, gain=1.0):
        seen, out = set(), []
        for (t, x, y, z) in keys:
            tt = min(self.ticks, t + delay)
            if tt in seen: continue
            seen.add(tt); out.append((tt, x * gain, y * gain, z * gain))
        return self.r(bone, *out)

    def sec(self, keys, delay=2, tail=True):
        """secondary motion. keys (t, x, y, z): x>0 = whipped back, z>0 = toward +X. Mane, stalk, leaf and tail lag in a chain"""
        self.lag("hair_f", [(t, -abs(x) * 0.25, 0, z * 0.2) for (t, x, y, z) in keys], delay)
        self.lag("hair_b", [(t, x * 0.7, 0, z * 0.3) for (t, x, y, z) in keys], delay + 1)
        self.lag("hair_r", [(t, x * 0.3, 0, z * 0.5 + max(0, x) * 0.4) for (t, x, y, z) in keys], delay + 1)
        self.lag("hair_l", [(t, x * 0.3, 0, z * 0.5 - max(0, x) * 0.4) for (t, x, y, z) in keys], delay + 1)
        self.lag("sprout", [(t, x * 0.8, 0, z * 0.9) for (t, x, y, z) in keys], delay + 1)
        self.lag("stem2", [(t, x * 0.6, 0, z * 0.7) for (t, x, y, z) in keys], delay + 2)
        self.lag("leaf", [(t, x * 0.8, 0, z * 1.2) for (t, x, y, z) in keys], delay + 3)
        if tail:
            self.lag("tail2", [(t, 0, z * 0.5, -x * 0.4) for (t, x, y, z) in keys], delay + 1)
            self.lag("tail3", [(t, 0, z * 0.6, -x * 0.5) for (t, x, y, z) in keys], delay + 2)
            self.lag("tail4", [(t, 0, z * 0.8, -x * 0.6) for (t, x, y, z) in keys], delay + 3)
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


UNF_R = -95   # fore_r ry that points the forearm forward (unfolded)
UNF_L = 95

# ------------------------------------------------------------------ idle (80 loop): shallow nervous breathing, hug tightens, glances aside, tail + claw twitch
a = A("idle", 80, loop=True)
a.rot("chest", *[(t, -2.5 * math.sin(t / 80 * 4 * math.pi), 0, 0) for t in range(0, 81, 10)])
a.pos("body", *[(t, 0, -0.25 + 0.25 * math.cos(t / 80 * 4 * math.pi), 0) for t in range(0, 81, 10)])
a.rot("body", (0, 0, 0, 0), (20, 0, 3, 0), (40, 0, 0, 0), (60, 0, -3, 0), (80, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (24, 0, 0, 0), (27, -4, 22, 6), (36, -4, 24, 6), (39, 0, 0, 0), (56, 0, 0, 0), (60, -8, 0, -6), (68, -8, -4, -8), (72, 0, 0, 0), (80, 0, 0, 0))
a.rot("arm_r", (0, 0, 0, 0), (20, 2, 0, -2), (40, 0, 0, 0), (60, 2, 0, -2), (80, 0, 0, 0))
a.rot("arm_l", (0, 0, 0, 0), (20, 2, 0, 2), (40, 0, 0, 0), (60, 2, 0, 2), (80, 0, 0, 0))
a.rot("fore_r", (0, 0, 0, 0), (20, 0, 6, 0), (40, 0, 0, 0), (60, 0, 6, 0), (80, 0, 0, 0))
a.rot("fore_l", (0, 0, 0, 0), (20, 0, -6, 0), (40, 0, 0, 0), (60, 0, -6, 0), (80, 0, 0, 0))
a.rot("hand_r", (0, 0, 0, 0), (44, 0, 0, 0), (46, 0, 0, 14), (48, 0, 0, 0), (50, 0, 0, 12), (52, 0, 0, 0), (80, 0, 0, 0))
a.rot("limb", *[(t, 0, 4 * math.sin(t / 80 * 2 * math.pi), 4 * math.sin(t / 80 * 4 * math.pi)) for t in range(0, 81, 10)])
a.rot("limb_hand", (0, 0, 0, 0), (10, 0, 0, 0), (13, 0, 0, 16), (16, 0, 0, -4), (19, 0, 0, 10), (24, 0, 0, 0), (80, 0, 0, 0))
for b, ph, amp in (("tail1", 0, 5), ("tail2", 6, 6), ("tail3", 12, 8), ("tail4", 18, 12)):
    a.rot(b, *[(t, 0, amp * math.sin((t + ph) / 80 * 2 * math.pi), amp * 0.6 * math.sin((t + ph) / 40 * 2 * math.pi)) for t in range(0, 81, 10)])
for b, ph, amp in (("hair_b", 0, 2), ("hair_r", 10, 3), ("hair_l", 25, -3), ("sprout", 5, 5), ("stem2", 12, 6), ("leaf", 20, 10)):
    a.rot(b, *[(t, amp * 0.5 * math.sin((t + ph) / 80 * 2 * math.pi), 0, amp * math.sin((t + ph) / 40 * 2 * math.pi)) for t in range(0, 81, 10)])
a.done()

# ------------------------------------------------------------------ walk (20 loop): hunched shuffling stalk, hugging, head bobbing low, tail swings counter
a = A("walk", 20, loop=True)
a.pos("body", (0, 0, 0, 0), (3, 0, -0.5, 0), (5, 0, 0.2, 0), (10, 0, 0, 0), (13, 0, -0.5, 0), (15, 0, 0.2, 0), (20, 0, 0, 0))
a.rot("body", (0, 0, 7, 2), (5, -2, 0, 0), (10, 0, -7, -2), (15, -2, 0, 0), (20, 0, 7, 2))
a.rot("chest", (0, -4, -4, 0), (5, -6, 0, 0), (10, -4, 4, 0), (15, -6, 0, 0), (20, -4, -4, 0))
a.rot("leg_r", (0, 24, 0, 0), (5, 0, 0, 0), (10, -22, 0, 0), (15, 0, 0, 0), (20, 24, 0, 0))
a.rot("leg_l", (0, -22, 0, 0), (5, 0, 0, 0), (10, 24, 0, 0), (15, 0, 0, 0), (20, -22, 0, 0))
a.rot("shin_r", (0, 0, 0, 0), (12, -34, 0, 0), (16, -12, 0, 0), (20, 0, 0, 0))
a.rot("shin_l", (0, 0, 0, 0), (2, -34, 0, 0), (6, -12, 0, 0), (10, 0, 0, 0), (20, 0, 0, 0))
a.rot("head", (0, 4, -4, 3), (5, -2, 0, 0), (10, 4, 4, -3), (15, -2, 0, 0), (20, 4, -4, 3))
a.rot("arm_r", (0, 3, 0, 0), (5, -2, 0, 0), (10, 3, 0, 0), (15, -2, 0, 0), (20, 3, 0, 0))
a.rot("arm_l", (0, 3, 0, 0), (5, -2, 0, 0), (10, 3, 0, 0), (15, -2, 0, 0), (20, 3, 0, 0))
a.rot("limb", (0, 0, -10, 6), (5, 0, 0, 0), (10, 0, 10, -4), (15, 0, 0, 0), (20, 0, -10, 6))
a.rot("limb_hand", (0, 0, 0, -6), (10, 0, 0, 8), (20, 0, 0, -6))
a.rot("tail1", (0, 0, -12, 0), (5, 0, 0, 4), (10, 0, 12, 0), (15, 0, 0, 4), (20, 0, -12, 0))
a.rot("tail2", (0, 0, -6, 0), (7, 0, 0, 6), (12, 0, 10, 0), (17, 0, 0, 6), (20, 0, -6, 0))
a.rot("tail3", (0, 0, 0, 0), (4, 0, -10, 0), (9, 0, 0, 8), (14, 0, 10, 0), (20, 0, 0, 0))
a.rot("tail4", (0, 0, 8, 0), (6, 0, -12, 0), (11, 0, 0, 10), (16, 0, 12, 0), (20, 0, 8, 0))
a.rot("sprout", (0, -8, 0, 6), (5, 6, 0, 0), (10, -8, 0, -6), (15, 6, 0, 0), (20, -8, 0, 6))
a.rot("stem2", (0, 6, 0, -8), (5, -6, 0, 4), (10, 6, 0, 8), (15, -6, 0, -4), (20, 6, 0, -8))
a.rot("leaf", (0, 0, 0, 14), (5, 10, 0, -6), (10, 0, 0, -14), (15, 10, 0, 6), (20, 0, 0, 14))
a.rot("hair_b", (0, 6, 0, 0), (5, 2, 0, 2), (10, 6, 0, 0), (15, 2, 0, -2), (20, 6, 0, 0))
a.done()

# ------------------------------------------------------------------ claw_swipe (24, hit 9): right claw unfolds + cocks back 0-6, SWIPE across t9, follow-through, re-hug
a = A("claw_swipe", 24)
a.r("chest", (4, 8, -24, 0), (6, 10, -30, 0), (8, -6, 10, 0), (9, -10, 26, 0), (12, -8, 32, 0), (17, -2, 10, 0))
a.r("head", (4, 0, 14, -6), (6, 0, 18, -8), (9, -6, -16, 4), (13, -4, -12, 2), (18, 0, 0, 0))
a.r("arm_r", (3, -10, 0, 40), (6, -30, 0, 70), (8, 40, 0, 40), (9, 70, 0, 10), (11, 74, 0, -20), (14, 56, 0, -24), (19, 10, 0, 0))
a.r("fore_r", (3, 0, -60, 30), (6, 0, UNF_R, 50), (8, 0, UNF_R, 20), (9, 0, UNF_R, 0), (12, 0, UNF_R + 10, 0), (17, 0, -40, 0), (21, 0, -6, 0))
a.r("hand_r", (6, 0, 0, 20), (9, 0, 0, -30), (12, 0, 0, -20), (17, 0, 0, 0))
a.r("arm_l", (6, -8, 0, -10), (9, 10, 0, -16), (14, 6, 0, -8))
a.r("limb", (6, 0, -10, 10), (9, 0, 20, -6), (14, 0, 10, 0))
a.p("body", (6, 0, -0.5, 0.6), (9, 0, -0.6, -1.4), (12, 0, -0.5, -1.6), (18, 0, 0, -0.4))
legs(a, [(6, 10, 0, 0), (9, -22, 0, 0), (13, -18, 0, 0), (19, 0, 0, 0)], [(6, -12, 0, 0), (9, 22, 0, 0), (13, 16, 0, 0), (19, 0, 0, 0)],
     sr=[(6, -8, 0, 0), (9, 0, 0, 0)], sl=[(6, 0, 0, 0), (9, -24, 0, 0), (15, -8, 0, 0)])
a.sec([(0, 0, 0, 0), (6, -6, 0, 8), (9, 14, 0, -12), (13, 6, 0, -6), (20, 0, 0, 0)], delay=1)
a.done()

# ------------------------------------------------------------------ double_rake (30): right claw rakes t8, left claw backhands t15, re-hug
a = A("double_rake", 30)
a.r("chest", (4, 6, -26, 0), (7, -8, 14, 0), (8, -10, 22, 0), (11, 4, 30, 0), (14, -10, -22, 0), (15, -12, -28, 0), (19, -6, -10, 0), (25, 0, 0, 0))
a.r("head", (4, 0, 16, -4), (8, -6, -14, 4), (11, 0, -10, 0), (15, -6, 16, -4), (21, 0, 0, 0))
a.r("arm_r", (4, -26, 0, 64), (7, 50, 0, 30), (8, 72, 0, 8), (10, 70, 0, -18), (13, 30, 0, -10), (18, 10, 0, 0))
a.r("fore_r", (4, 0, UNF_R, 50), (8, 0, UNF_R, 0), (10, 0, UNF_R, -6), (14, 0, -50, 0), (18, 0, -10, 0))
a.r("arm_l", (8, -10, 0, -20), (11, -24, 0, -64), (14, 50, 0, -30), (15, 74, 0, -8), (17, 70, 0, 18), (21, 30, 0, 10), (26, 0, 0, 0))
a.r("fore_l", (8, 0, 40, 0), (11, 0, UNF_L, -50), (15, 0, UNF_L, 0), (17, 0, UNF_L, 6), (21, 0, 50, 0), (26, 0, 0, 0))
a.r("hand_r", (8, 0, 0, -26), (12, 0, 0, 0))
a.r("hand_l", (15, 0, 0, 26), (19, 0, 0, 0))
a.r("limb", (8, 0, 16, -8), (15, 0, -12, 8), (22, 0, 0, 0))
a.p("body", (4, 0, -0.4, 0.4), (8, 0, -0.6, -1.2), (11, 0, -0.4, -1.0), (15, 0, -0.6, -2.0), (20, 0, -0.2, -1.0), (27, 0, 0, 0))
legs(a, [(4, 8, 0, 0), (8, -20, 0, 0), (11, -6, 0, 0), (15, 14, 0, 0), (22, 0, 0, 0)], [(4, -8, 0, 0), (8, 18, 0, 0), (11, 4, 0, 0), (15, -24, 0, 0), (22, 0, 0, 0)],
     sr=[(8, -4, 0, 0), (15, -22, 0, 0), (22, 0, 0, 0)], sl=[(8, -22, 0, 0), (15, -4, 0, 0), (22, 0, 0, 0)])
a.sec([(0, 0, 0, 0), (4, -4, 0, 10), (8, 10, 0, -12), (11, 2, 0, 8), (15, 12, 0, 14), (21, 4, 0, 4), (28, 0, 0, 0)], delay=1)
a.done()

# ------------------------------------------------------------------ tail_whip (32, hit 13): crouch + turn away 0-9, full SPIN t9-18 with the tail straightened (hit t13), wobble recover
a = A("tail_whip", 32)
a.r("root", (6, 0, 30, 0), (9, 0, 40, 0), (11, 0, -40, 0), (13, 0, -150, 0), (15, 0, -250, 0), (18, 0, -340, 0), (22, 0, -365, 0), (26, 0, -360, 0), (32, 0, -360, 0))
a.p("body", (6, 0, -1.4, 0), (9, 0, -1.8, 0), (13, 0, -1.0, 0), (18, 0, -1.2, 0), (24, 0, 0, 0))
a.r("chest", (6, -10, 14, 0), (9, -12, 20, 0), (13, -4, -10, 0), (18, -6, -14, 0), (24, 0, 0, 0))
a.r("head", (6, 0, -20, 0), (9, 0, -26, 0), (13, -4, 16, 0), (18, 0, 20, 0), (24, 6, 0, -10), (28, 0, 0, 0))
# tail1 rest (0,24,-22): straighten out sideways + low, sweep
a.r("tail1", (6, 0, 30, 10), (9, 0, 40, 16), (11, 0, -10, 24), (13, 0, -30, 26), (18, 0, -20, 22), (22, 0, 20, 4), (28, 0, 0, 0))
a.r("tail2", (6, 0, 10, 10), (11, 0, 20, 26), (13, 0, -10, 26), (18, 0, -16, 22), (23, 0, 16, 0), (28, 0, 0, 0))
a.r("tail3", (6, 0, 14, 10), (11, 0, 30, 20), (13, 0, -14, 22), (19, 0, -24, 18), (24, 0, 20, 0), (29, 0, 0, 0))
a.r("tail4", (6, 0, 20, 0), (11, 0, 40, -10), (14, 0, -20, -10), (20, 0, -30, -10), (25, 0, 24, 0), (30, 0, 0, 0))
a.r("limb", (9, 0, -20, 20), (13, 0, 20, 30), (18, 0, 10, 20), (24, 0, 0, 0))
a.r("arm_r", (9, 0, 0, -4), (13, 10, 0, 10), (20, 0, 0, 0))
a.r("arm_l", (9, 0, 0, 4), (13, 10, 0, -10), (20, 0, 0, 0))
legs(a, [(6, 20, 0, 6), (9, 26, 0, 8), (13, -14, 0, 10), (18, -10, 0, 8), (22, 14, 0, 0), (28, 0, 0, 0)], [(6, -20, 0, -6), (9, -24, 0, -8), (13, 16, 0, -10), (18, 10, 0, -8), (22, -8, 0, 0), (28, 0, 0, 0)],
     sr=[(9, -34, 0, 0), (18, -16, 0, 0), (24, 0, 0, 0)], sl=[(9, -12, 0, 0), (18, -26, 0, 0), (24, 0, 0, 0)])
a.sec([(0, 0, 0, 0), (9, 6, 0, -10), (13, 12, 0, 22), (18, 16, 0, 26), (22, -6, 0, -10), (28, 0, 0, 0)], delay=2, tail=False)
a.done()

# ------------------------------------------------------------------ tail_spear (28, hit 12): tail arches high over the shoulder 0-9 (scorpion), STABS forward t12, yanks back
a = A("tail_spear", 28)
a.r("tail1", (4, 0, 40, -30), (8, 0, 56, -44), (9, 0, 58, -46), (11, 0, -20, -40), (12, 0, -62, -32), (15, 0, -56, -34), (20, 0, -20, -20), (26, 0, 0, 0))
a.r("tail2", (4, 0, 0, -24), (9, 0, 0, -40), (11, 0, 0, 0), (12, 0, 0, 22), (15, 0, 0, 18), (21, 0, 0, 0))
a.r("tail3", (4, 0, 0, -20), (9, 0, 0, -34), (11, 0, 0, 4), (12, 0, 0, 20), (15, 0, 0, 16), (22, 0, 0, 0))
a.r("tail4", (4, 0, 0, -16), (9, 0, 0, -30), (12, 0, 0, -10), (14, 0, 0, 6), (22, 0, 0, 0))
a.s("tail1", (4, 1.35, 1.25, 1.35), (9, 1.6, 1.35, 1.6), (11, 1.7, 1.35, 1.7), (12, 1.8, 1.35, 1.8), (15, 1.65, 1.3, 1.65), (21, 1.1, 1.05, 1.1), (26, 1, 1, 1))
a.r("chest", (4, 6, 10, 0), (9, 10, 14, 0), (12, -16, -10, 0), (15, -12, -8, 0), (22, 0, 0, 0))
a.r("head", (4, 6, -10, 0), (9, 8, -16, 0), (12, -10, -20, 4), (18, 0, -8, 0), (24, 0, 0, 0))
a.p("body", (9, 0, -0.6, 0.8), (12, 0, -0.8, -1.4), (16, 0, -0.6, -1.0), (24, 0, 0, 0))
a.r("body", (9, 0, 14, 0), (12, 0, -26, 0), (18, 0, -16, 0), (24, 0, 0, 0))
a.r("limb", (9, 0, 0, 14), (12, 0, -20, -10), (20, 0, 0, 0))
a.r("hand_r", (8, 0, 0, 10), (12, 0, 0, -6), (16, 0, 0, 0))
legs(a, [(9, 6, 0, 0), (12, -26, 0, 0), (18, -14, 0, 0), (24, 0, 0, 0)], [(9, -10, 0, 0), (12, 24, 0, 0), (18, 12, 0, 0), (24, 0, 0, 0)],
     sl=[(12, -26, 0, 0), (18, -10, 0, 0), (24, 0, 0, 0)])
a.sec([(0, 0, 0, 0), (9, -6, 0, 6), (12, 12, 0, -8), (16, 6, 0, -4), (24, 0, 0, 0)], delay=1, tail=False)
a.done()

# ------------------------------------------------------------------ limb_crush (32, hit 14): mutant claw rears up overhead 0-10 (fingers splay), SLAMS down in front t14, grinds, lifts
a = A("limb_crush", 32)
a.r("body", (6, 0, 20, 0), (10, 0, 26, 0), (14, 0, 34, 0), (22, 0, 30, 0), (28, 0, 0, 0))
a.r("limb", (4, 0, 20, 60), (8, 0, 30, 100), (10, 0, 34, 110), (12, 0, 50, 40), (14, 0, 60, -10), (22, 0, 60, -8), (26, 0, 30, 20), (30, 0, 0, 0))
a.r("limb_fore", (4, 0, 0, 20), (10, 0, 0, 30), (12, 0, 0, -10), (14, 0, 0, -30), (22, 0, 0, -30), (28, 0, 0, 0))
a.r("limb_hand", (6, 0, 0, 30), (10, 0, 0, 40), (13, 0, 0, -20), (14, 0, 0, -50), (16, 0, 0, -40), (22, 0, 0, -44), (28, 0, 0, 0))
a.s("limb_hand", (8, 1.15, 1.15, 1.15), (14, 1.3, 1.3, 1.3), (22, 1.2, 1.2, 1.2), (28, 1, 1, 1))
a.r("chest", (6, 10, 0, -10), (10, 14, 0, -14), (13, -14, 0, 6), (14, -24, 0, 10), (22, -20, 0, 8), (28, 0, 0, 0))
a.r("head", (6, 14, -10, 0), (10, 18, -14, 0), (14, -10, -20, 0), (22, -4, -16, 0), (28, 0, 0, 0))
a.p("body", (6, 0, 0.6, 0), (10, 0, 0.8, 0.4), (14, 0, -2.2, -0.8), (22, 0, -2.0, -0.6), (28, 0, 0, 0))
legs(a, [(10, -6, 0, 0), (14, 40, 0, 6), (22, 40, 0, 6), (28, 0, 0, 0)], [(10, 6, 0, 0), (14, -10, 0, -6), (22, -10, 0, -6), (28, 0, 0, 0)],
     sr=[(14, -60, 0, 0), (22, -60, 0, 0), (28, 0, 0, 0)], sl=[(14, -20, 0, 0), (22, -20, 0, 0), (28, 0, 0, 0)])
a.sec([(0, 0, 0, 0), (10, 10, 0, -6), (14, -16, 0, 10), (18, 6, 0, 4), (26, 0, 0, 0)], delay=2)
a.done()

# ------------------------------------------------------------------ shy_lunge (34, hit 16): curls lower and lower 0-8, LEAPS t9 (arms unfold wide), lands with both claws raking down t16, re-hugs
a = A("shy_lunge", 34)
a.p("root", (5, 0, -2.0, 0.6), (8, 0, -2.8, 1.0), (10, 0, 2.6, -2.0), (13, 0, 3.6, -3.4), (15, 0, 1.0, -3.6), (16, 0, -1.6, -3.4), (19, 0, -1.0, -2.6), (26, 0, 0, -0.6), (32, 0, 0, 0))
a.r("root", (8, 10, 0, 0), (10, -16, 0, 0), (13, -24, 0, 0), (16, -14, 0, 0), (20, -8, 0, 0), (28, 0, 0, 0))
a.r("chest", (5, -16, 0, 0), (8, -22, 0, 0), (11, 10, 0, 0), (14, 6, 0, 0), (16, -30, 0, 0), (21, -14, 0, 0), (28, 0, 0, 0))
a.r("head", (5, -10, 0, 0), (8, 20, 0, 0), (13, 20, 0, 0), (16, 0, 0, 0), (24, 0, 0, 0))
for s, k, unf in ((1, "r", UNF_R), (-1, "l", UNF_L)):
    a.r("arm_" + k, (8, 0, 0, 0), (10, 40, 0, 70 * s), (13, 120, 0, 50 * s), (15, 150, 0, 20 * s), (16, 90, 0, 0), (19, 50, 0, 6 * s), (26, 10, 0, 0))
    a.r("fore_" + k, (8, 0, 0, 0), (10, 0, unf, 0), (19, 0, unf, 0), (24, 0, unf * 0.4, 0), (29, 0, 0, 0))
    a.r("hand_" + k, (13, 0, 0, 20 * s), (16, 0, 0, -20 * s), (20, 0, 0, 0))
a.r("limb", (8, 0, 0, 20), (12, 0, 10, 40), (16, 0, 30, -20), (22, 0, 10, 0), (28, 0, 0, 0))
legs(a, [(5, 50, 0, 0), (8, 64, 0, 0), (10, -30, 0, 0), (13, -20, 0, 0), (15, 30, 0, 0), (16, 50, 0, 0), (20, 30, 0, 0), (28, 0, 0, 0)],
     [(5, 50, 0, 0), (8, 64, 0, 0), (10, -40, 0, 0), (13, -10, 0, 0), (15, 40, 0, 0), (16, 30, 0, 0), (20, 16, 0, 0), (28, 0, 0, 0)],
     sr=[(5, -70, 0, 0), (8, -96, 0, 0), (10, -10, 0, 0), (13, -60, 0, 0), (16, -80, 0, 0), (20, -50, 0, 0), (28, 0, 0, 0)])
a.sec([(0, 0, 0, 0), (8, -10, 0, 0), (10, 26, 0, 0), (14, 20, 0, 0), (16, -14, 0, 0), (21, 8, 0, 0), (28, 0, 0, 0)], delay=2)
a.done()

# ------------------------------------------------------------------ thorn_volley (30, shot 14): head ducks + shakes 2-10 (mane bristles), WHIPS up t14 flinging quills, shudder
a = A("thorn_volley", 30)
a.r("head", (3, -26, 0, 0), (5, -28, 14, 6), (7, -28, -14, -6), (9, -30, 14, 6), (11, -30, -6, 0), (13, 4, 0, 0), (14, 16, 0, 0), (17, 8, 0, 0), (24, 0, 0, 0))
a.r("chest", (3, -14, 0, 0), (11, -18, 0, 0), (14, 12, 0, 0), (18, 4, 0, 0), (24, 0, 0, 0))
for b, k in (("hair_r", 1), ("hair_l", -1)):
    a.r(b, (3, 0, 0, -6 * k), (11, 0, 0, -10 * k), (14, 10, 0, 30 * k), (17, 6, 0, 20 * k), (24, 0, 0, 0))
a.s("head", (5, 1, 1, 1), (11, 1.1, 1.08, 1.1), (14, 1.22, 1.15, 1.22), (17, 1.05, 1.05, 1.05), (22, 1, 1, 1))
a.r("hair_b", (11, -16, 0, 0), (14, 40, 0, 0), (18, 20, 0, 0), (24, 0, 0, 0))
a.r("hair_f", (11, 10, 0, 0), (14, -30, 0, 0), (20, -6, 0, 0))
a.r("arm_r", (3, 6, 0, -4), (11, 10, 0, -6), (14, -10, 0, 20), (20, 0, 0, 0))
a.r("arm_l", (3, 6, 0, 4), (11, 10, 0, 6), (14, -10, 0, -20), (20, 0, 0, 0))
a.r("fore_r", (11, 0, 10, 0), (14, 0, -30, 0), (20, 0, 0, 0))
a.r("fore_l", (11, 0, -10, 0), (14, 0, 30, 0), (20, 0, 0, 0))
a.p("body", (3, 0, -0.8, 0.3), (11, 0, -1.2, 0.4), (14, 0, 0.2, -0.4), (18, 0, 0, 0))
a.r("tail1", (11, 0, 0, -10), (14, 0, 0, 20), (20, 0, 0, 0))
legs(a, [(3, 14, 0, 2), (11, 18, 0, 3), (14, -6, 0, 3), (20, 0, 0, 0)], sr=[(3, -24, 0, 0), (11, -30, 0, 0), (14, 0, 0, 0)])
a.lag("sprout", [(5, 0, 0, 14), (7, 0, 0, -14), (9, 0, 0, 14), (11, -10, 0, 0), (14, 30, 0, 0), (18, -10, 0, 0), (24, 0, 0, 0)], 1)
a.lag("leaf", [(5, 0, 0, 20), (7, 0, 0, -20), (9, 0, 0, 20), (11, -14, 0, 0), (14, 40, 0, 0), (18, -14, 0, 0), (24, 0, 0, 0)], 2)
a.done()

# ------------------------------------------------------------------ leaf_boomerang (36, throw 12): right claw reaches up and plucks the leaf t3-6, winds back, SIDEARM throw t12, leaf regrows 24-32
a = A("leaf_boomerang", 36)
a.r("arm_r", (3, 140, 0, 10), (5, 166, 0, -4), (7, 150, 0, 6), (9, 20, 0, 80), (10, -10, 0, 90), (12, 60, 0, 30), (13, 80, 0, -10), (16, 60, 0, -20), (22, 10, 0, 0))
a.r("fore_r", (3, 0, UNF_R, 0), (7, 0, UNF_R, 0), (10, 0, UNF_R + 20, 30), (12, 0, UNF_R, 0), (16, 0, UNF_R + 30, 0), (22, 0, -30, 0), (26, 0, 0, 0))
a.r("hand_r", (5, 0, 0, 20), (6, 0, 0, -10), (12, 0, 0, -30), (16, 0, 0, 0))
a.show("hleaf", 6, 12, grow=1)
a.s("leaf", (5, 1, 1, 1), (6, 0.2, 0.2, 0.2), (6.5, *HIDE), (24, *HIDE), (25, 0.3, 0.3, 0.3), (29, 1.2, 1.2, 1.2), (31, 1, 1, 1))
a.r("head", (3, 20, -6, 0), (6, 24, 0, 0), (9, 0, 20, 0), (12, -6, -10, 0), (16, -4, -6, 0), (24, 6, 0, 0), (30, 14, 0, 0), (34, 0, 0, 0))
a.r("chest", (3, 10, 0, 6), (6, 12, 0, 8), (9, 4, -30, 0), (10, 4, -36, 0), (12, -8, 20, 0), (13, -10, 26, 0), (17, -6, 10, 0), (24, 0, 0, 0))
a.r("arm_l", (3, 6, 0, -6), (10, 0, 0, -20), (13, 10, 0, -10), (20, 0, 0, 0))
a.p("body", (3, 0, 0.4, 0), (6, 0, 0.6, 0), (10, 0, -0.3, 0.6), (12, 0, -0.5, -0.8), (18, 0, 0, -0.4), (24, 0, 0, 0))
legs(a, [(6, 0, 0, 0), (10, 14, 0, 0), (12, -20, 0, 0), (18, -10, 0, 0), (24, 0, 0, 0)], [(6, 0, 0, 0), (10, -14, 0, 0), (12, 20, 0, 0), (18, 10, 0, 0), (24, 0, 0, 0)],
     sl=[(12, -20, 0, 0), (18, -6, 0, 0), (24, 0, 0, 0)])
a.lag("sprout", [(3, 0, 0, 20), (6, 20, 0, -20), (9, -10, 0, 10), (14, 4, 0, 0), (30, -6, 0, 0)], 0)
a.lag("hair_b", [(9, -6, 0, 0), (12, 10, 0, 0), (18, 0, 0, 0)], 1)
a.lag("tail2", [(9, 0, 10, 0), (12, 0, -16, 0), (18, 0, 0, 0)], 2)
a.lag("tail4", [(9, 0, 16, 0), (12, 0, -24, 0), (18, 0, 0, 0)], 3)
a.done()

# ------------------------------------------------------------------ root_snare (36, spikes 14-22): mutant claw lifted 0-8, PLUNGED into the floor t12, trembles while roots run t14-24, rips out
a = A("root_snare", 36)
a.r("body", (6, 0, 24, 0), (12, 0, 40, 0), (26, 0, 40, 0), (32, 0, 0, 0))
a.r("limb", (4, 0, 20, 50), (8, 0, 30, 70), (11, 0, 56, -20), (12, 0, 60, -40), (14, 0, 60, -36), (16, 0, 60, -40), (18, 0, 60, -36), (20, 0, 60, -40), (22, 0, 60, -36), (26, 0, 60, -38), (28, 0, 40, 30), (32, 0, 0, 0))
a.r("limb_fore", (8, 0, 0, 20), (12, 0, 0, -40), (26, 0, 0, -40), (29, 0, 0, 10), (32, 0, 0, 0))
a.r("limb_hand", (8, 0, 0, 30), (12, 0, 0, -60), (26, 0, 0, -60), (29, 0, 0, 20), (33, 0, 0, 0))
a.p("body", (8, 0, 0.4, 0), (12, 0, -3.0, -0.6), (26, 0, -3.0, -0.6), (29, 0, 0.4, 0), (33, 0, 0, 0))
a.r("chest", (8, 8, 0, -6), (12, -30, 0, 14), (14, -28, 2, 14), (18, -28, -2, 14), (22, -28, 2, 14), (26, -30, 0, 14), (29, 4, 0, 0), (33, 0, 0, 0))
a.r("head", (8, 10, 0, 0), (12, 20, 0, -10), (26, 22, 0, -8), (30, 0, 0, 0))
a.r("arm_r", (12, 30, 0, 10), (26, 30, 0, 10), (32, 0, 0, 0))
legs(a, [(8, -4, 0, 0), (12, 60, 0, 10), (26, 60, 0, 10), (31, 0, 0, 0)], [(8, 4, 0, 0), (12, 10, 0, -10), (26, 10, 0, -10), (31, 0, 0, 0)],
     sr=[(12, -90, 0, 0), (26, -90, 0, 0), (31, 0, 0, 0)], sl=[(12, -30, 0, 0), (26, -30, 0, 0), (31, 0, 0, 0)])
a.sec([(0, 0, 0, 0), (8, 10, 0, -4), (12, -14, 0, 8), (16, -10, 0, 12), (20, -14, 0, 4), (24, -10, 0, 10), (29, 12, 0, 0), (34, 0, 0, 0)], delay=1)
a.done()

# ------------------------------------------------------------------ shriek (32, t12 + pulses 16/20): inhale curled 0-8, UNCURLS arms flung wide + head thrust, pink mouth gapes, shudders, re-hugs
a = A("shriek", 32)
a.r("chest", (4, -10, 0, 0), (8, -14, 0, 0), (11, 16, 0, 0), (12, 20, 0, 0), (16, 18, 0, 0), (20, 20, 0, 0), (24, 6, 0, 0), (28, 0, 0, 0))
a.r("head", (4, -20, 0, 0), (8, -26, 0, 0), (11, 16, 0, 0), (12, 22, 0, 0), (14, 18, -4, 4), (16, 22, 4, -4), (18, 18, -4, 4), (20, 22, 4, -4), (24, 0, 0, 0))
a.s("mouth", (8, 1, 1, 1), (11, 1.2, 3.2, 1), (12, 1.3, 3.8, 1), (22, 1.25, 3.5, 1), (25, 1, 1, 1))
a.p("mouth", (8, 0, 0, 0), (12, 0, -0.6, 0), (22, 0, -0.6, 0), (25, 0, 0, 0))
for s, k, unf in ((1, "r", UNF_R), (-1, "l", UNF_L)):
    a.r("arm_" + k, (4, 6, 0, -6 * s), (8, 10, 0, -10 * s), (11, -20, 0, 80 * s), (12, -24, 0, 90 * s), (22, -20, 0, 86 * s), (26, 0, 0, 10 * s))
    a.r("fore_" + k, (8, 0, -10 * s, 0), (11, 0, unf * 0.9, 0), (22, 0, unf * 0.9, 0), (27, 0, 0, 0))
    a.r("hand_" + k, (12, 0, 0, 30 * s), (22, 0, 0, 30 * s), (26, 0, 0, 0))
a.r("limb", (8, 0, 0, -10), (12, 0, 0, 40), (22, 0, 0, 36), (26, 0, 0, 0))
a.r("limb_hand", (12, 0, 0, 30), (22, 0, 0, 30), (26, 0, 0, 0))
a.r("tail1", (8, 0, 0, 10), (12, 0, 0, -30), (22, 0, 0, -26), (26, 0, 0, 0))
a.p("body", (8, 0, -0.8, 0.4), (12, 0, 0.2, -0.4), (22, 0, 0.2, -0.4), (28, 0, 0, 0))
legs(a, [(8, 10, 0, 0), (12, -6, 0, 10), (22, -6, 0, 10), (28, 0, 0, 0)], sr=[(8, -20, 0, 0), (12, 0, 0, 0)])
a.r("hair_r", (8, 0, 0, -10), (12, 20, 0, 30), (16, 16, 0, 22), (20, 20, 0, 30), (24, 0, 0, 0))
a.r("hair_l", (8, 0, 0, 10), (12, 20, 0, -30), (16, 16, 0, -22), (20, 20, 0, -30), (24, 0, 0, 0))
a.r("hair_b", (8, -10, 0, 0), (12, 40, 0, 0), (16, 30, 0, 0), (20, 40, 0, 0), (26, 0, 0, 0))
a.r("sprout", (8, -16, 0, 0), (12, 30, 0, 0), (14, 20, 0, 10), (16, 30, 0, -10), (20, 30, 0, 10), (26, 0, 0, 0))
a.r("leaf", (10, -20, 0, 0), (14, 40, 0, 20), (18, 30, 0, -20), (22, 40, 0, 10), (28, 0, 0, 0))
a.done()

# ------------------------------------------------------------------ hug_crush (40): arms thrown open 0-6, lunge + CLAMP t10, squeezes t14/20/26, flings the victim aside t32, re-hug
a = A("hug_crush", 40)
for s, k, unf in ((1, "r", UNF_R), (-1, "l", UNF_L)):
    a.r("arm_" + k, (4, 20, 0, 70 * s), (7, 30, 0, 90 * s), (10, 80, 0, 10 * s), (14, 84, 0, -4 * s), (16, 80, 0, 6 * s), (20, 86, 0, -6 * s), (22, 80, 0, 6 * s),
        (26, 88, 0, -8 * s), (29, 80, 0, 4 * s), (32, 60, 0, (60 if s > 0 else -20)), (35, 20, 0, 20 * s), (39, 0, 0, 0))
    a.r("fore_" + k, (4, 0, unf, 0), (7, 0, unf, 0), (10, 0, unf * 0.35, 0), (26, 0, unf * 0.3, 0), (32, 0, unf * 0.8, 0), (37, 0, 0, 0))
a.r("chest", (4, 10, 0, 0), (7, 14, 0, 0), (10, -24, 0, 0), (14, -30, 0, 0), (16, -24, 0, 0), (20, -32, 0, 0), (22, -24, 0, 0), (26, -34, 0, 0), (29, -26, 0, 0),
    (32, -10, -40, 0), (35, 0, -20, 0), (39, 0, 0, 0))
a.r("head", (4, 16, 0, 0), (7, 20, 0, 0), (10, 0, 0, 0), (14, -6, 0, 10), (20, -6, 0, -10), (26, -8, 0, 12), (32, 0, 20, 0), (38, 0, 0, 0))
a.p("root", (7, 0, 0.6, 0.6), (9, 0, 0.6, -2.4), (10, 0, 0, -2.8), (30, 0, 0, -2.8), (36, 0, 0, -0.6), (40, 0, 0, 0))
a.s("chest", (14, 0.94, 1.03, 0.94), (16, 1, 1, 1), (20, 0.92, 1.04, 0.92), (22, 1, 1, 1), (26, 0.9, 1.05, 0.9), (29, 1, 1, 1))
a.r("limb", (7, 0, 10, 40), (10, 0, 50, 10), (26, 0, 50, 10), (32, 0, 70, 30), (37, 0, 0, 0))
a.r("tail1", (10, 0, 10, 10), (14, 0, -6, 20), (20, 0, 6, 10), (26, 0, -6, 24), (32, 0, 20, 0), (38, 0, 0, 0))
legs(a, [(7, 20, 0, 0), (9, -30, 0, 0), (12, -20, 0, 0), (30, -20, 0, 0), (36, 0, 0, 0)], [(7, -20, 0, 0), (9, 30, 0, 0), (12, 20, 0, 0), (30, 20, 0, 0), (36, 0, 0, 0)],
     sl=[(9, -30, 0, 0), (12, -20, 0, 0), (30, -20, 0, 0), (36, 0, 0, 0)])
a.sec([(0, 0, 0, 0), (7, -10, 0, 0), (10, 14, 0, 0), (14, 6, 0, 6), (20, 6, 0, -6), (26, 6, 0, 6), (32, -6, 0, -20), (38, 0, 0, 0)], delay=2, tail=False)
a.done()

# ------------------------------------------------------------------ curl_guard (40): curls into a tight spiky ball 0-6, trembles 6-22 (armoured), BURSTS open t26 with a thorn ring, unfold
a = A("curl_guard", 40)
a.p("body", (4, 0, -4.4, 1.0), (6, 0, -5.0, 1.2), (22, 0, -5.0, 1.2), (24, 0, -5.4, 1.2), (26, 0, 0.8, 0), (29, 0, 0.4, 0), (34, 0, 0, 0))
a.r("chest", (4, -30, 0, 0), (6, -34, 0, 0), (8, -34, 3, 0), (10, -34, -3, 0), (12, -34, 3, 0), (14, -34, -3, 0), (16, -34, 3, 0), (18, -34, -3, 0), (20, -34, 3, 0), (22, -36, 0, 0),
    (24, -38, 0, 0), (26, 22, 0, 0), (29, 14, 0, 0), (34, 0, 0, 0))
a.r("head", (4, -30, 0, 0), (24, -34, 0, 0), (26, 30, 0, 0), (30, 10, 0, 0), (34, 0, 0, 0))
for s, k, unf in ((1, "r", UNF_R), (-1, "l", UNF_L)):
    a.r("arm_" + k, (4, 10, 0, -10 * s), (24, 12, 0, -12 * s), (26, -30, 0, 100 * s), (29, -20, 0, 80 * s), (34, 0, 0, 10 * s))
    a.r("fore_" + k, (4, 0, -10 * s, 0), (24, 0, -12 * s, 0), (26, 0, unf, 0), (30, 0, unf * 0.8, 0), (36, 0, 0, 0))
legs(a, [(4, 70, 0, 8), (24, 72, 0, 8), (26, -10, 0, 16), (29, -6, 0, 10), (34, 0, 0, 0)], sr=[(4, -125, 0, 0), (24, -128, 0, 0), (26, 0, 0, 0)])
a.r("limb", (4, 0, -40, -10), (24, 0, -44, -10), (26, 0, 0, 70), (30, 0, 0, 50), (36, 0, 0, 0))
a.r("limb_fore", (4, 0, 0, -60), (24, 0, 0, -60), (26, 0, 0, 20), (32, 0, 0, 0))
a.r("tail1", (4, 0, 70, 20), (24, 0, 74, 20), (26, 0, 0, -40), (30, 0, 0, -30), (36, 0, 0, 0))
a.r("tail2", (4, 0, 30, 10), (24, 0, 30, 10), (26, 0, 0, 20), (32, 0, 0, 0))
a.r("tail3", (4, 0, 30, 10), (24, 0, 30, 10), (27, 0, 0, 20), (33, 0, 0, 0))
a.s("head", (6, 1, 1, 1), (20, 1.08, 1.08, 1.08), (24, 1.12, 1.12, 1.12), (26, 1.25, 1.2, 1.25), (30, 1, 1, 1))
a.scl("thorns", (0, *HIDE), (25.5, *HIDE), (26, 0.3, 0.3, 0.3), (28, 0.7, 1.4, 0.7), (30, 0.7, 1.0, 0.7), (35, 0.7, 0.2, 0.7), (35.5, *HIDE), (40, *HIDE))
a.sec([(0, 0, 0, 0), (4, -10, 0, 0), (24, -10, 0, 0), (26, 30, 0, 0), (30, 10, 0, 0), (36, 0, 0, 0)], delay=1, tail=False)
a.done()

# ------------------------------------------------------------------ frenzy (46, enraged): twitching crouch 0-6, dash t8, slashes R12 L16 R20 L24, limb + claws hammer t30, panting recover
a = A("frenzy", 46)
a.p("root", (4, 0, -1.6, 0.4), (6, 0, -1.8, 0.6), (8, 0, -0.4, -2.0), (10, 0, -0.6, -3.0), (30, 0, -0.6, -3.0), (32, 0, -1.4, -3.2), (40, 0, 0, -1.0), (46, 0, 0, 0))
a.r("chest", (2, -20, 6, 0), (4, -20, -6, 0), (6, -24, 0, 0), (10, -10, -24, 0), (12, -14, 26, 0), (14, -12, -24, 0), (16, -14, 26, 0), (18, -12, -24, 0), (20, -14, 26, 0),
    (22, -12, -24, 0), (24, -14, 26, 0), (27, 12, 0, 0), (30, -30, 0, 0), (34, -26, 0, 0), (40, -10, 0, 0))
a.r("head", (2, -6, 10, 10), (4, -6, -10, -10), (6, 10, 0, 0), (12, -6, -14, 4), (16, -6, 14, -4), (20, -6, -14, 4), (24, -6, 14, -4), (27, 20, 0, 0), (30, -10, 0, 0), (36, 6, 0, 0), (42, 0, 0, 0))
a.r("arm_r", (6, -20, 0, 40), (10, -30, 0, 70), (12, 74, 0, -10), (14, 30, 0, 30), (18, -30, 0, 70), (20, 76, 0, -12), (22, 30, 0, 30), (27, 150, 0, 20), (30, 70, 0, 0),
    (34, 60, 0, 0), (40, 10, 0, 0))
a.r("arm_l", (6, -20, 0, -40), (10, -10, 0, -20), (14, -30, 0, -70), (16, 74, 0, 10), (18, 30, 0, -30), (22, -30, 0, -70), (24, 76, 0, 12), (27, 150, 0, -20), (30, 70, 0, 0),
    (34, 60, 0, 0), (40, 10, 0, 0))
a.r("fore_r", (6, 0, UNF_R, 0), (34, 0, UNF_R, 0), (40, 0, -30, 0), (44, 0, 0, 0))
a.r("fore_l", (6, 0, UNF_L, 0), (34, 0, UNF_L, 0), (40, 0, 30, 0), (44, 0, 0, 0))
a.r("limb", (6, 0, 0, 20), (12, 0, 20, 10), (20, 0, 20, 30), (27, 0, 40, 110), (30, 0, 60, -20), (34, 0, 60, -16), (40, 0, 0, 0))
a.r("limb_hand", (27, 0, 0, 40), (30, 0, 0, -50), (34, 0, 0, -40), (40, 0, 0, 0))
a.r("body", (12, 0, -10, 0), (16, 0, 10, 0), (20, 0, -10, 0), (24, 0, 10, 0), (27, 0, 20, 0), (32, 0, 20, 0), (40, 0, 0, 0))
legs(a, [(4, 40, 0, 0), (8, -30, 0, 0), (12, -20, 0, 0), (16, 10, 0, 0), (20, -20, 0, 0), (24, 10, 0, 0), (30, 40, 0, 0), (38, 0, 0, 0)],
     [(4, 40, 0, 0), (8, 30, 0, 0), (12, 16, 0, 0), (16, -16, 0, 0), (20, 16, 0, 0), (24, -16, 0, 0), (30, 0, 0, 0), (38, 0, 0, 0)],
     sr=[(4, -70, 0, 0), (8, -20, 0, 0), (30, -60, 0, 0), (38, 0, 0, 0)])
a.sec([(0, 0, 0, 0), (4, -8, 0, 10), (8, 20, 0, 0), (12, 8, 0, -14), (16, 8, 0, 14), (20, 8, 0, -14), (24, 8, 0, 14), (27, -14, 0, 0), (30, 20, 0, 0), (36, 6, 0, 0), (44, 0, 0, 0)], delay=1)
a.done()

# ------------------------------------------------------------------ bramble_bloom (44, enraged): kneels hugging tight, the sprout swells huge 4-16, head flung back t18 (inner thorns) + t26 (outer ring), wilts back
a = A("bramble_bloom", 44)
a.p("body", (4, 0, -2.4, 0), (16, 0, -3.0, 0), (18, 0, 0.6, 0), (26, 0, 1.0, 0), (34, 0, 0, 0))
a.r("chest", (4, -20, 0, 0), (8, -24, 0, 3), (10, -24, 0, -3), (12, -26, 0, 3), (14, -26, 0, -3), (16, -28, 0, 0), (18, 20, 0, 0), (22, 14, 0, 0), (26, 24, 0, 0), (32, 8, 0, 0), (38, 0, 0, 0))
a.r("head", (4, -20, 0, 0), (16, -24, 0, 0), (18, 34, 0, 0), (22, 26, 0, 0), (26, 36, 0, 0), (32, 10, 0, 0), (38, 0, 0, 0))
a.s("sprout", (2, 1, 1, 1), (8, 1.6, 1.6, 1.6), (14, 1.9, 1.9, 1.9), (16, 2.1, 2.1, 2.1), (18, 2.4, 2.4, 2.4), (26, 2.5, 2.5, 2.5), (32, 1.7, 1.7, 1.7), (38, 1, 1, 1))
a.r("sprout", (8, 20, 0, 10), (12, 22, 0, -10), (16, 24, 0, 6), (18, -26, 0, 0), (22, -18, 0, 0), (26, -30, 0, 0), (34, 0, 0, 0))
a.r("leaf", (8, 0, 0, 20), (12, 0, 0, -10), (16, 0, 0, 30), (18, 0, 0, -20), (26, 0, 0, 20), (34, 0, 0, 0))
for s, k in ((1, "r"), (-1, "l")):
    a.r("arm_" + k, (4, 10, 0, -10 * s), (16, 14, 0, -14 * s), (18, -20, 0, 90 * s), (22, -14, 0, 80 * s), (26, -24, 0, 100 * s), (32, 0, 0, 30 * s), (38, 0, 0, 0))
    a.r("fore_" + k, (16, 0, -10 * s, 0), (18, 0, (UNF_R if s > 0 else UNF_L), 0), (30, 0, (UNF_R if s > 0 else UNF_L) * 0.8, 0), (38, 0, 0, 0))
a.r("limb", (4, 0, 0, -20), (16, 0, 0, -24), (18, 0, 0, 60), (26, 0, 0, 70), (34, 0, 0, 0))
a.r("tail1", (4, 0, 0, 10), (16, 0, 0, 14), (18, 0, 0, -40), (26, 0, 0, -50), (34, 0, 0, 0))
legs(a, [(4, 50, 0, 0), (16, 60, 0, 0), (18, 0, 0, 12), (26, 0, 0, 14), (34, 0, 0, 0)], sr=[(4, -90, 0, 0), (16, -100, 0, 0), (18, 0, 0, 0)])
a.scl("thorns", (0, *HIDE), (17.5, *HIDE), (18, 0.3, 0.3, 0.3), (20, 0.55, 1.3, 0.55), (22, 0.55, 0.8, 0.55), (25.5, 0.6, 0.7, 0.6), (26, 1.1, 0.5, 1.1), (28, 1.1, 1.6, 1.1),
      (32, 1.1, 1.1, 1.1), (36, 1.1, 0.2, 1.1), (36.5, *HIDE), (44, *HIDE))
a.rot("thorns", (0, 0, 0, 0), (18, 0, 0, 0), (26, 0, 18, 0), (36, 0, 26, 0), (44, 0, 26, 0))
a.lag("hair_b", [(16, -10, 0, 0), (18, 30, 0, 0), (26, 34, 0, 0), (34, 0, 0, 0)], 1)
a.lag("hair_r", [(16, 0, 0, -6), (18, 10, 0, 24), (26, 14, 0, 30), (34, 0, 0, 0)], 1)
a.lag("hair_l", [(16, 0, 0, 6), (18, 10, 0, -24), (26, 14, 0, -30), (34, 0, 0, 0)], 1)
a.done()

# ------------------------------------------------------------------ death (40): flinch t2, hugs herself tighter, knees buckle t10-18, keels over sideways t18-28, sprout wilts, tail goes limp
a = A("death", 40)
a.r("chest", (2, 10, 0, 6), (6, -20, 0, -4), (12, -30, 0, 0), (18, -36, 0, 0), (40, -30, 0, 0))
a.r("head", (2, 20, 0, 10), (6, -16, 0, -10), (12, -20, 0, 14), (20, -10, 0, 24), (40, -16, 0, 30))
a.r("fore_r", (6, 0, 10, 0), (14, 0, 14, 0), (40, 0, 10, 0))
a.r("fore_l", (6, 0, -10, 0), (14, 0, -14, 0), (40, 0, -10, 0))
legs(a, [(8, 0, 0, 0), (12, 50, 0, 6), (18, 90, 0, 6), (40, 90, 0, 6)], sr=[(8, 0, 0, 0), (12, -70, 0, 0), (18, -100, 0, 0), (40, -100, 0, 0)])
a.p("body", (8, 0, 0, 0), (12, 0, -3.5, 0), (18, 0, -6.6, 1.0), (40, 0, -6.6, 1.0))
a.r("root", (18, 0, 0, 0), (24, 0, 0, -40), (28, 0, 0, -84), (30, 0, 0, -78), (32, 0, 0, -82), (40, 0, 0, -82))
a.p("root", (18, 0, 0, 0), (28, -2.0, -1.0, 0), (40, -2.0, -1.0, 0))
a.r("limb", (4, 0, 0, 20), (10, 0, 0, -10), (24, 0, 0, 20), (30, 0, 0, -20), (40, 0, 0, -16))
a.r("limb_hand", (6, 0, 0, 30), (14, 0, 0, -10), (40, 0, 0, -20))
a.r("tail1", (4, 0, 0, -20), (12, 0, 0, 10), (24, 0, 0, 30), (40, 0, 0, 26))
a.r("tail2", (6, 0, 0, -10), (24, 0, 0, 20), (40, 0, 0, 20))
a.r("tail3", (8, 0, 0, -10), (26, 0, 0, 24), (40, 0, 0, 24))
a.r("sprout", (4, 20, 0, 10), (10, -10, 0, -10), (20, -30, 0, 0), (30, -60, 0, 20), (40, -64, 0, 20))
a.r("stem2", (14, 0, 0, 20), (30, -30, 0, 30), (40, -30, 0, 30))
a.r("leaf", (8, 0, 0, -30), (24, 0, 0, 40), (32, 0, 0, 60), (40, 0, 0, 60))
a.s("mouth", (2, 1, 3, 1), (6, 1, 1, 1))
a.done()

m.save(OUT)
print("cubes", len(m.cubes), "anims", [x["name"] for x in m.anims])
