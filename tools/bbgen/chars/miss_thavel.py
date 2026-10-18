"""Miss Bloomie (normal teacher, black-and-white) - generates assets/fpe/bbmodels/miss_thavel.bbmodel.
Reference: docs/ref/confirmed/miss_thavel.jpg - wild spiky near-black hair falling to the shoulders, a headband of three
alphabet blocks (A B C) with little white petals and a square-spiral squiggle floating above, pale face shadowed by the
bangs with a huge shark-tooth grin, white short-sleeved blouse with pointed collar + round pendant, long flared white skirt
with a grey diagonal wedge and a torn, ragged hem, thin pale legs in pointed dark ankle boots, long black opera gloves:
her RIGHT arm ends in a GIANT jagged black shard-claw, the left in small black talons.
Blockbench space: Y up, ground 0, faces -Z. Character's RIGHT = +X.
Rotation signs (file values): arm/leg rx>0 = swing forward, torso/head rx>0 = lean back / look up,
ry>0 = turn to the character's left, rz>0 = hanging part swings toward +X (character's right).
Run: python3 tools/bbgen/chars/miss_thavel.py
"""
import math, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from bbgen import Model, mix  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "../../../src/main/resources/assets/fpe/bbmodels/miss_thavel.bbmodel")

# ------------------------------------------------------------------ palette (ink drawing: blue-black ink, paper white, two greys)
INK, INK_D, INK_HI = 0x2E2A3D, 0x1B1826, 0x4B4661
LINE = 0x8B88A0
PAPER, PAPER_D, PAPER_L = 0xE4E5E8, 0xB3B7BE, 0xF5F5F7
GREY, GREY_D = 0x9FA7AE, 0x737C85
SKIN, SKIN_D, SKIN_L = 0xE8E7EA, 0xAFAEBB, 0xF6F6F8
BLOCK, BLOCK_D = 0xD8DBDE, 0x8E959C
MOUTH, TOOTH = 0x14111C, 0xF4F4F6
EYE = 0xE8E4FF

m = Model("miss_thavel", S=8, atlas=2048)
R = m.rng


def all_faces(fn, skip=()):
    return {k: fn for k in ("north", "south", "east", "west", "up", "down") if k not in skip}


def combo(*fns):
    def f(F):
        for fn in fns: fn(F)
    return f


def fill(c):
    return lambda F: F.rect(0, 0, F.w, F.h, c)


def strands(base=INK, hi=INK_HI, dark=INK_D, ink=True):
    def f(F):
        cols = [R.random() for _ in range(F.w)]
        for x in range(F.w):
            c = mix(base, hi, 0.6) if cols[x] > 0.86 else mix(base, dark, 0.6) if cols[x] < 0.2 else base
            for y in range(F.h):
                F.px(x, y, mix(c, dark, 0.4 * abs(y / max(1, F.h - 1) - 0.3)))
        if ink and F.w >= 4 and F.h >= 8 and R.random() < 0.6:
            x = R.randint(1, F.w - 2)
            for y in range(R.randint(0, F.h // 3), F.h - 2):
                F.px(x, y, LINE)
    return f


def edge_lines(c):
    return lambda F: (F.rect(0, 0, 1, F.h, c), F.rect(F.w - 1, 0, 1, F.h, c))


def hstripe(c, y0, h):
    return lambda F: F.rect(0, y0, F.w, h, c)


def folds(base, dark, light, n=3):
    def f(F):
        for i in range(n):
            x = int((i + 0.5) * F.w / n) + R.randint(-1, 1)
            for y in range(F.h):
                if R.random() < 0.85:
                    F.px(x, y, mix(base, dark, 0.45)); F.px(x + 1, y, mix(base, light, 0.45))
    return f


def glove(F):
    """black glove: glossy streak + ink edge"""
    for y in range(F.h):
        for x in range(F.w):
            F.px(x, y, mix(INK, INK_D, x / max(1, F.w - 1) * 0.7))
    F.rect(max(0, F.w // 4), 0, 1, F.h, INK_HI)


def face_front(F):
    W, H = F.w, F.h  # 43 x 45
    for y in range(H):
        for x in range(W):
            F.px(x, y, mix(SKIN, SKIN_D, max(0, (20 - y) / 20) * 0.95))  # heavy shadow under the bangs
    # narrow, mad eyes deep in the shadow: dark lids with pale pinpoint glints (glow)
    for cx, s in ((13, 1), (30, -1)):
        F.poly([(cx - 6, 19 + 2 * s * 0), (cx + 6, 17 + 4 * (s < 0)), (cx + 5, 21), (cx - 5, 22)], INK_D)
        F.disc(cx + 1 * s, 19.8, 1.4, EYE, glow=True)
        F.line(cx - 5, 15.5 + (2 if s > 0 else 0), cx + 5, 15.5 + (0 if s > 0 else 2), INK, 1.3)  # angry brows
    F.line(21, 25, 22, 28, SKIN_D, 1)  # nose
    for x in (6, 8, 35, 37):
        F.line(x, 30, x + 1.5, 28.5, SKIN_D, 1)


def grin(F):
    """huge shark-tooth grin, corners curling up (mouth cube front)"""
    W, H = F.w, F.h
    F.rect(0, 0, W, H, SKIN)
    top = lambda x: 1.0 + 2.6 * ((x - W / 2) / (W / 2)) ** 2 * -1 + 2.6
    pts_u = [(x, 1.2 + 2.2 * (1 - ((x - W / 2) / (W / 2)) ** 2) * 0 + 0.0 + 3.0 * ((x - W / 2) / (W / 2)) ** 2 * -1 + 3.0) for x in range(0, W + 1, 2)]
    # lower lip: deep U
    pts_l = [(x, H - 1.2 - (H - 4) * (((x - W / 2) / (W / 2)) ** 2)) for x in range(W, -1, -2)]
    F.poly([(x, 3.6 - 3.0 * ((x - W / 2) / (W / 2)) ** 2) for x in range(0, W + 1, 2)] + pts_l, MOUTH)
    # teeth: upper row pointing down, lower row pointing up
    n = 9
    for i in range(n):
        x0 = 2 + i * (W - 4) / n
        x1 = x0 + (W - 4) / n
        u = ((x0 + x1) / 2 - W / 2) / (W / 2)
        yt = 3.6 - 3.0 * u * u
        yb = H - 1.2 - (H - 4) * u * u
        F.poly([(x0, yt), (x1, yt), ((x0 + x1) / 2, yt + (yb - yt) * 0.45)], TOOTH)
        if 0 < i < n - 1:
            F.poly([(x0 + 1, yb), (x1 + 1, yb), ((x0 + x1) / 2 + 1, yb - (yb - yt) * 0.42)], TOOTH)
    F.line(0, 0.5, 2, 3, INK, 1)
    F.line(W - 1, 0.5, W - 3, 3, INK, 1)


def letter(ch):
    """paint an alphabet-block face: pale block, dark border, inset square, letter"""
    def f(F):
        W, H = F.w, F.h
        for y in range(H):
            for x in range(W):
                F.px(x, y, mix(BLOCK, BLOCK_D, 0.25 * y / H))
        F.rect(0, 0, W, 1, INK); F.rect(0, H - 1, W, 1, INK); F.rect(0, 0, 1, H, INK); F.rect(W - 1, 0, 1, H, INK)
        F.rect(2, 2, W - 4, 1, BLOCK_D); F.rect(2, H - 3, W - 4, 1, BLOCK_D); F.rect(2, 2, 1, H - 4, BLOCK_D); F.rect(W - 3, 2, 1, H - 4, BLOCK_D)
        a, b, c, d = W * 0.28, H * 0.24, W * 0.72, H * 0.76
        t = 1.8
        if ch == "A":
            F.line(a, d, W / 2, b, INK, t); F.line(W / 2, b, c, d, INK, t); F.line(a + 2, H * 0.58, c - 2, H * 0.58, INK, t)
        elif ch == "B":
            F.line(a, b, a, d, INK, t); F.line(a, b, c - 2, b, INK, t); F.line(a, H / 2, c - 1, H / 2, INK, t); F.line(a, d, c - 1, d, INK, t)
            F.line(c - 2, b, c - 1, H / 2 - 1, INK, t); F.line(c, H / 2 + 1, c - 1, d, INK, t)
        elif ch == "C":
            for k in range(40, 321, 8):
                r = math.radians(k)
                F.disc(W / 2 + math.cos(r) * W * 0.24, H / 2 - math.sin(r) * H * 0.26, t / 2, INK)
        else:
            F.line(a, b, c, d, INK, t)
    return f


def skirt_paint(light_side, wedge=True):
    """white skirt with the grey diagonal wedge, ink fold lines and a ragged dark hem line"""
    def f(F):
        for y in range(F.h):
            for x in range(F.w):
                u = x / max(1, F.w - 1)
                v = y / max(1, F.h - 1)
                edge = 0.15 + 0.7 * (u if light_side else 1 - u)
                c = mix(PAPER_L, PAPER, v * 0.6)
                if wedge and v > edge and v < edge + 0.38:
                    c = mix(GREY, GREY_D, (v - edge) * 0.6)
                F.px(x, y, c)
        for i in range(3):
            x = int((i + 0.6) * F.w / 3.2)
            F.line(x, F.h * 0.25, x + (3 if light_side else -3), F.h - 2, PAPER_D, 1)
        for x in range(F.w):  # torn hem
            h = 1 + int(R.random() * 3)
            F.rect(x, F.h - h, 1, h, PAPER_D if R.random() < 0.6 else LINE)
    return f


def blouse_front(F):
    W, H = F.w, F.h
    folds(PAPER, PAPER_D, PAPER_L, 2)(F)
    F.line(W * 0.5, 0, W * 0.5, H, PAPER_D, 1)
    F.disc(W * 0.5, H * 0.38, 2.6, LINE); F.disc(W * 0.5, H * 0.38, 1.7, PAPER_L)  # round pendant
    F.line(W * 0.5, 0, W * 0.5, H * 0.38 - 2.6, LINE, 1)
    F.line(W * 0.15, H * 0.9, W * 0.35, H * 0.65, PAPER_D, 1)


# ------------------------------------------------------------------ skeleton
m.group("root", (0, 0, 0))
m.group("body", (0, 14.5, 0), parent="root")
for k in ("f", "b", "r", "l"):
    m.group("skirt_" + k, (0, 18.6, 0), parent="body")
m.group("chest", (0, 18.8, 0), parent="body")
m.group("head", (0, 25.6, 0), parent="chest")
m.group("jaw", (0, 26.9, -2.8), parent="head")
m.group("bangs", (0, 30.8, -2.8), parent="head")
m.group("hair_r", (2.9, 30, 0), parent="head")
m.group("hair_l", (-2.9, 30, 0), parent="head")
m.group("hair_b", (0, 30, 2.6), parent="head")
m.group("blocks", (0, 32.2, -0.6), parent="head")
for k, x in (("blk_a", 2.9), ("blk_b", 0.0), ("blk_c", -2.9)):
    m.group(k, (x, 33.4, -1.2), parent="blocks")
m.group("squiggle", (2.0, 36.0, -0.8), parent="blocks")
m.group("arm_r", (3.4, 24.2, 0), parent="chest")
m.group("fore_r", (3.7, 20.2, 0), parent="arm_r")
m.group("hand_r", (3.9, 15.6, 0), parent="fore_r")
for i in range(4):
    m.group(f"fing{i}", (3.9 + (i - 1.5) * 0.8, 13.6, -0.2 + abs(i - 1.5) * 0.25), parent="hand_r")
m.group("thumb_r", (2.6, 14.4, -0.8), parent="hand_r")
m.group("held_r", (3.9, 12.6, -1.6), parent="hand_r")
m.group("arm_l", (-3.4, 24.2, 0), parent="chest")
m.group("fore_l", (-3.6, 20.2, 0), parent="arm_l")
m.group("hand_l", (-3.7, 16.4, 0), parent="fore_l")
m.group("claws_l", (-3.7, 15.0, 0), parent="hand_l")
m.group("held_l", (-3.7, 14.0, -1.0), parent="hand_l")
for s, k in ((1, "r"), (-1, "l")):
    m.group("leg_" + k, (1.1 * s, 14, 0), parent="root")
    m.group("shin_" + k, (1.1 * s, 8, 0), parent="leg_" + k)
    m.group("foot_" + k, (1.1 * s, 2.6, 0), parent="shin_" + k)

# ------------------------------------------------------------------ legs: thin pale legs, pointed dark ankle boots with flared cuffs
for s, k in ((1, "r"), (-1, "l")):
    x = 1.1 * s
    m.cube("thigh_" + k, "leg_" + k, (x - 0.9, 7.8, -0.9), (x + 0.9, 14.4, 0.9), SKIN_D, color2=SKIN, grad=True)
    m.cube("knee_" + k, "shin_" + k, (x - 0.75, 7.2, -0.8), (x + 0.75, 8.4, 0.8), SKIN, faces={"north": lambda F: F.disc(F.w / 2, F.h / 2, 2, SKIN_D)})
    m.cube("calf_" + k, "shin_" + k, (x - 0.7, 2.6, -0.7), (x + 0.7, 7.4, 0.75), SKIN, color2=SKIN_D, grad=True,
           faces={"north": lambda F: F.rect(F.w - 2, 0, 1, F.h, LINE), "east": edge_lines(SKIN_D)})
    m.cube("boot_" + k, "foot_" + k, (x - 0.85, 0, -1.2), (x + 0.85, 2.8, 0.9), INK, color2=INK_D, grad=True, faces={"north": edge_lines(INK_HI)})
    m.cube("cuff_" + k, "foot_" + k, (x - 1.05, 2.4, -1.15), (x + 1.05, 3.4, 1.05), INK_D, faces=all_faces(hstripe(INK_HI, 0, 1)))
    m.cube("cuffpt_" + k, "foot_" + k, (x - 0.35, 2.8, -1.4), (x + 0.35, 4.4, -1.0), INK_D, origin=(x, 3.0, -1.2), rot=(-14, 0, 0))
    m.cube("cuffpt2_" + k, "foot_" + k, (x + 0.6 * s - 0.3, 2.8, -0.3), (x + 0.6 * s + 0.3, 4.2, 0.3), INK_D, origin=(x + 0.6 * s, 3.0, 0), rot=(0, 0, 18 * s))
    m.cube("toe_" + k, "foot_" + k, (x - 0.55, 0, -2.6), (x + 0.55, 1.1, -1.0), INK, origin=(x, 0, -1.2), rot=(-4, 0, 0))
    m.cube("tip_" + k, "foot_" + k, (x - 0.25, 0.1, -3.6), (x + 0.25, 0.7, -2.4), INK_D, origin=(x, 0.3, -2.4), rot=(-12, 0, 0))
    m.cube("heel_" + k, "foot_" + k, (x - 0.35, 0, 0.5), (x + 0.35, 1.0, 1.1), INK_D)

# ------------------------------------------------------------------ hips + long flared torn skirt
m.cube("hips", "body", (-2.2, 14.0, -1.5), (2.2, 19.0, 1.5), PAPER_D)
SK, TOP = 13.6, 19.0
m.cube("sk_front", "skirt_f", (-3.0, TOP - SK, -2.0), (3.0, TOP, -1.5), PAPER, origin=(0, 18.6, -1.7), rot=(15, 0, 0),
       faces={"north": skirt_paint(True), "south": fill(GREY_D)})
m.cube("sk_back", "skirt_b", (-3.0, TOP - SK, 1.5), (3.0, TOP, 2.0), PAPER, origin=(0, 18.6, 1.7), rot=(-15, 0, 0),
       faces={"south": skirt_paint(False, False), "north": fill(GREY_D)})
m.cube("sk_right", "skirt_r", (2.1, TOP - SK, -2.5), (2.6, TOP, 2.5), PAPER, origin=(2.3, 18.6, 0), rot=(0, 0, 15),
       faces={"east": skirt_paint(True, False), "west": fill(GREY_D)})
m.cube("sk_left", "skirt_l", (-2.6, TOP - SK, -2.5), (-2.1, TOP, 2.5), PAPER, origin=(-2.3, 18.6, 0), rot=(0, 0, -15),
       faces={"west": skirt_paint(False), "east": fill(GREY_D)})
m.cube("sk_front2", "skirt_f", (-4.4, TOP - SK, -2.05), (4.4, TOP - 6.0, -1.55), PAPER, origin=(0, 18.6, -1.7), rot=(15, 0, 0),
       faces={"north": skirt_paint(True), "south": fill(GREY_D)})
m.cube("sk_back2", "skirt_b", (-4.4, TOP - SK, 1.55), (4.4, TOP - 6.0, 2.05), PAPER, origin=(0, 18.6, 1.7), rot=(-15, 0, 0),
       faces={"south": skirt_paint(False, False), "north": fill(GREY_D)})
m.cube("sk_right2", "skirt_r", (2.15, TOP - SK, -4.0), (2.65, TOP - 6.0, 4.0), PAPER, origin=(2.3, 18.6, 0), rot=(0, 0, 15),
       faces={"east": skirt_paint(True, False), "west": fill(GREY_D)})
m.cube("sk_left2", "skirt_l", (-2.65, TOP - SK, -4.0), (-2.15, TOP - 6.0, 4.0), PAPER, origin=(-2.3, 18.6, 0), rot=(0, 0, -15),
       faces={"west": skirt_paint(False), "east": fill(GREY_D)})
for i, (x, z, ry) in enumerate([(2.3, -1.8, 45), (-2.3, -1.8, -45), (2.3, 1.8, -45), (-2.3, 1.8, 45)]):
    sx, sz = (1 if x > 0 else -1), (1 if z > 0 else -1)
    bone = "skirt_f" if z < 0 else "skirt_b"
    m.cube(f"sk_corner{i}", bone, (x - 1.4, TOP - SK + 0.3, z - 0.25), (x + 1.4, TOP, z + 0.25), PAPER, origin=(x, 18.6, z),
           rot=(-sz * 13, ry, sx * 13), faces={"north": skirt_paint(x > 0, z < 0), "south": skirt_paint(x < 0, False)})
# ragged tatters hanging off the hem (rotated triangles-ish)
PANEL = {"skirt_f": ((0, 18.6, -1.7), (15, 0, 0), "z", -1.8), "skirt_b": ((0, 18.6, 1.7), (-15, 0, 0), "z", 1.8),
         "skirt_r": ((2.3, 18.6, 0), (0, 0, 15), "x", 2.4), "skirt_l": ((-2.3, 18.6, 0), (0, 0, -15), "x", -2.4)}
k = 0
for bone, (org, rr, ax, off) in PANEL.items():
    for j, u in enumerate((-3.6, -1.8, 0.2, 2.0, 3.6)):
        ln = 1.0 + R.random() * 1.6
        w = 0.6 + R.random() * 0.6
        yb = TOP - SK + 0.3
        if ax == "z":
            frm, to = (u - w, yb - ln, off - 0.2), (u + w, yb, off + 0.2)
        else:
            frm, to = (off - 0.2, yb - ln, u - w), (off + 0.2, yb, u + w)
        m.cube(f"tatter{k}", bone, frm, to, PAPER if j % 2 else PAPER_D, origin=org, rot=rr, faces=all_faces(lambda F: F.rect(0, F.h - 1, F.w, 1, LINE)))
        k += 1
m.cube("waistband", "body", (-2.4, 18.4, -1.75), (2.4, 19.3, 1.75), GREY, faces=all_faces(hstripe(GREY_D, 0, 1)))

# ------------------------------------------------------------------ torso: white blouse, pointed collar, pendant
m.cube("waist", "chest", (-1.9, 18.8, -1.25), (1.9, 21.0, 1.25), PAPER, color2=PAPER_D, grad=True, faces={"north": folds(PAPER, PAPER_D, PAPER_L, 2)})
m.cube("torso", "chest", (-2.5, 20.6, -1.5), (2.5, 24.6, 1.5), PAPER, color2=PAPER_D, grad=True,
       faces={"north": blouse_front, "south": folds(PAPER, PAPER_D, PAPER_L, 3)})
m.cube("bust", "chest", (-2.1, 21.6, -1.85), (2.1, 23.6, -1.4), PAPER, faces={"north": folds(PAPER, PAPER_D, PAPER_L, 1)})
m.cube("shoulders", "chest", (-2.9, 23.6, -1.4), (2.9, 24.8, 1.4), PAPER, faces={"up": fill(PAPER_L)})
m.cube("neck", "chest", (-0.65, 24.5, -0.65), (0.65, 25.9, 0.65), SKIN_D, color2=SKIN, grad=True)
m.cube("collar_r", "chest", (0.0, 23.7, -1.95), (2.0, 25.3, -1.55), PAPER_L, origin=(0.1, 25.1, -1.75), rot=(0, 0, 28),
       faces={"north": lambda F: (F.line(0, 0, F.w - 1, F.h - 1, LINE, 1), F.rect(0, 0, F.w, 1, LINE))})
m.cube("collar_l", "chest", (-2.0, 23.7, -1.95), (0.0, 25.3, -1.55), PAPER_L, origin=(-0.1, 25.1, -1.75), rot=(0, 0, -28),
       faces={"north": lambda F: (F.line(F.w - 1, 0, 0, F.h - 1, LINE, 1), F.rect(0, 0, F.w, 1, LINE))})
m.cube("collar_back", "chest", (-1.6, 24.5, -0.6), (1.6, 25.6, 1.5), PAPER_L)
m.cube("blouse_hem", "chest", (-2.3, 18.6, -1.65), (2.3, 19.4, 1.65), PAPER_D)

# ------------------------------------------------------------------ head
m.cube("skull", "head", (-2.7, 25.7, -2.7), (2.7, 31.3, 2.6), SKIN, faces={"north": face_front, "up": fill(INK_D)})
m.cube("chin", "head", (-1.5, 25.4, -2.5), (1.5, 26.0, 0.8), SKIN_D)
m.cube("mouth", "jaw", (-2.3, 26.0, -2.95), (2.3, 27.9, -2.7), SKIN, faces={"north": grin})
m.cube("crown", "head", (-3.0, 29.6, -2.95), (3.0, 32.4, 3.0), INK, faces=all_faces(strands()))
m.cube("crown2", "head", (-2.5, 32.2, -2.3), (2.5, 33.0, 2.5), INK, faces=all_faces(strands()))
m.cube("nape", "hair_b", (-3.0, 25.4, 1.8), (3.0, 30.4, 3.4), INK, faces=all_faces(strands()))
m.cube("side_r", "hair_r", (2.5, 25.0, -2.5), (3.8, 31.0, 2.9), INK, faces=all_faces(strands()))
m.cube("side_l", "hair_l", (-3.8, 25.0, -2.5), (-2.5, 31.0, 2.9), INK, faces=all_faces(strands()))
m.cube("fringe", "bangs", (-3.0, 30.0, -3.2), (3.0, 31.8, -2.6), INK, faces=all_faces(strands()))


def spike(name, parent, base, ln, w, rx, ry, rz, col=INK, segs=3):
    """hair spike: flat tapered blade growing +Y from `base`, rotated about the base."""
    x, y, z = base
    d = max(0.6, w * 0.42)
    m.cube(name, parent, (x - w / 2, y, z - d / 2), (x + w / 2, y + ln * 0.5, z + d / 2), col, origin=base, rot=(rx, ry, rz),
           faces=all_faces(strands(ink=False)))
    if segs >= 2:
        m.cube(name + "m", parent, (x - w * 0.32, y + ln * 0.45, z - d * 0.4), (x + w * 0.32, y + ln * 0.8, z + d * 0.4), col,
               origin=base, rot=(rx, ry, rz), faces=all_faces(strands(ink=False)))
    if segs >= 3:
        m.cube(name + "t", parent, (x - w * 0.14, y + ln * 0.75, z - d * 0.3), (x + w * 0.14, y + ln, z + d * 0.3), INK_D,
               origin=base, rot=(rx, ry, rz))


# side spikes: wild jagged hair flaring out and down to the shoulders
for i, (y, z, ln, rz, rx) in enumerate([(31.2, 0.0, 4.4, -84, 0), (30.0, -1.2, 6.4, -118, -8), (28.6, 0.8, 7.4, -136, 10), (27.2, -0.6, 7.0, -152, -6),
                                        (25.8, 1.2, 5.6, -168, 10), (29.4, 2.0, 6.0, -128, 30)]):
    spike(f"spk_r{i}", "hair_r", (3.0, y, z), ln, 3.0, rx, 0, rz)
for i, (y, z, ln, rz, rx) in enumerate([(31.4, 0.4, 5.2, 80, 0), (30.0, -1.0, 6.8, 114, -8), (28.6, 0.8, 7.6, 132, 10), (27.2, -0.4, 7.2, 150, -6),
                                        (25.6, 1.0, 5.8, 168, 8), (29.2, 2.0, 5.6, 124, 30)]):
    spike(f"spk_l{i}", "hair_l", (-3.0, y, z), ln, 3.0, rx, 0, rz)
# back spikes fanning down
for i, (x, y, ln, rz, rx) in enumerate([(-2.2, 29.0, 6.0, 160, -10), (-0.6, 28.6, 7.0, 176, -14), (1.0, 28.8, 6.6, -172, -12), (2.4, 29.2, 5.6, -156, -8),
                                        (0.0, 31.0, 4.4, 180, -40)]):
    spike(f"spk_b{i}", "hair_b", (x, y, 3.0), ln, 3.0, rx, 0, rz)
# bangs: jagged spikes hanging over the eyes
for i, (x, ln, rz) in enumerate([(2.4, 3.0, -22), (1.3, 4.2, -8), (0.1, 3.4, 6), (-1.1, 4.4, 12), (-2.3, 3.2, 26)]):
    spike(f"bang{i}", "bangs", (x, 31.6, -2.9), ln, 1.5, -172, 0, rz)
# a few crown spikes sticking up / back (messy top)
for i, (x, z, ln, rz, rx) in enumerate([(1.6, 1.2, 3.6, -40, -30), (-1.8, 1.0, 3.4, 44, -26), (0.2, 2.0, 3.0, 4, -60), (2.4, -1.0, 2.6, -64, 10)]):
    spike(f"top{i}", "head", (x, 32.6, z), ln, 1.7, rx, 0, rz, segs=2)

# ------------------------------------------------------------------ ABC blocks headband, white petals, squiggle
m.cube("band", "blocks", (-3.2, 32.0, -2.0), (3.2, 32.7, -1.2), INK_D, faces={"north": hstripe(INK_HI, 0, 1)})
for k, ch, x, rz, rx in (("blk_a", "A", 2.9, -24, 8), ("blk_b", "B", 0.0, 4, 10), ("blk_c", "C", -2.9, 22, 6)):
    m.cube("cube_" + k, k, (x - 1.35, 32.2, -2.6), (x + 1.35, 34.9, 0.1), BLOCK, origin=(x, 33.4, -1.2), rot=(rx, 0, rz),
           faces={"north": letter(ch), "east": letter("ABC"[("ABC".index(ch) + 1) % 3]), "west": letter("ABC"[("ABC".index(ch) + 2) % 3]),
                  "up": letter(ch), "south": letter(ch), "down": fill(BLOCK_D)})
for i, (x, y, rz) in enumerate([(4.2, 32.0, -60), (-4.0, 32.6, 50), (3.6, 30.8, -100)]):
    m.cube(f"petal{i}", "blocks", (x - 0.5, y, -1.9), (x + 0.5, y + 1.6, -1.4), PAPER_L, origin=(x, y, -1.6), rot=(0, 0, rz),
           faces={"north": edge_lines(PAPER_D)})
    m.cube(f"petalb{i}", "blocks", (x - 0.35, y, -1.85), (x + 0.35, y + 1.2, -1.45), PAPER, origin=(x, y, -1.6), rot=(0, 0, rz + 40))
# square spiral squiggle hovering above (5 thin ink strokes)
sq = [(-1.0, 0.0, 2.0, 0.3), (0.7, 0.0, 0.3, 2.0), (-1.0, 1.7, 2.0, 0.3), (-1.0, 0.6, 0.3, 1.4), (-0.4, 0.6, 1.0, 0.3), (0.1, 0.6, 0.3, 0.8)]
for i, (x, y, w, h) in enumerate(sq):
    m.cube(f"sq{i}", "squiggle", (2.0 + x * 1.6, 36.6 + y * 1.6, -1.0), (2.0 + (x + w) * 1.6, 36.6 + (y + h) * 1.6, -0.6), INK_D)

# ------------------------------------------------------------------ arms: puffed white sleeves, long black opera gloves
for s, k in ((1, "r"), (-1, "l")):
    m.cube("sleeve_" + k, "arm_" + k, (3.4 * s - 1.35, 22.2, -1.35), (3.4 * s + 1.35, 24.9, 1.35), PAPER, color2=PAPER_D, grad=True,
           faces={"north": folds(PAPER, PAPER_D, PAPER_L, 2), "east": folds(PAPER, PAPER_D, PAPER_L, 1)})
    m.cube("sleevehem_" + k, "arm_" + k, (3.4 * s - 1.45, 21.9, -1.45), (3.4 * s + 1.45, 22.5, 1.45), PAPER_D)
    m.cube("upper_" + k, "arm_" + k, (3.5 * s - 0.85, 19.9, -0.85), (3.5 * s + 0.85, 22.4, 0.85), INK, faces=all_faces(glove))
    m.cube("glovetop_" + k, "arm_" + k, (3.5 * s - 1.0, 21.6, -1.0), (3.5 * s + 1.0, 22.2, 1.0), INK_D, faces=all_faces(hstripe(INK_HI, 0, 1)))
# right forearm: thick black, widening into the giant shard hand
m.cube("fore_r1", "fore_r", (3.7 - 1.0, 18.0, -1.0), (3.7 + 1.0, 20.4, 1.0), INK, faces=all_faces(glove))
m.cube("fore_r2", "fore_r", (3.8 - 1.3, 15.6, -1.25), (3.8 + 1.3, 18.2, 1.25), INK, faces=all_faces(glove))
for i, (y, ln, rz, rx) in enumerate([(19.0, 2.0, -60, 0), (17.6, 2.8, -70, 10), (16.4, 2.4, -54, -10), (17.2, 1.8, 0, -70)]):
    base = (4.9 if rz else 3.8, y, 0 if rz else 1.2)
    spike(f"shard_f{i}", "fore_r", base, ln, 1.0, rx, 0, rz, segs=2)
m.cube("palm_r", "hand_r", (3.9 - 2.0, 12.8, -1.4), (3.9 + 2.0, 15.8, 1.2), INK, faces=all_faces(glove))
m.cube("knuck_r", "hand_r", (3.9 - 2.2, 12.6, -1.6), (3.9 + 2.2, 13.8, 0.8), INK_D, faces={"north": hstripe(INK_HI, 0, 1)})
# four long jagged blade-fingers (3 kinked segments each) + thumb
FAN = [16, 5, -6, -17]
LEN = [7.6, 9.6, 9.2, 7.0]
for i in range(4):
    g = f"fing{i}"
    x0, y0, z0 = m.groups[g]["origin"]
    L = LEN[i]
    m.cube(f"f{i}a", g, (x0 - 0.7, y0 - L * 0.42, z0 - 0.3), (x0 + 0.7, y0 + 0.3, z0 + 0.3), INK, origin=(x0, y0, z0), rot=(6, 0, FAN[i]),
           faces=all_faces(glove))
    m.cube(f"f{i}b", g, (x0 - 0.55, y0 - L * 0.76, z0 - 0.25), (x0 + 0.55, y0 - L * 0.38, z0 + 0.25), INK, origin=(x0, y0, z0), rot=(16, 0, FAN[i] * 1.3),
           faces=all_faces(glove))
    m.cube(f"f{i}c", g, (x0 - 0.3, y0 - L, z0 - 0.2), (x0 + 0.3, y0 - L * 0.72, z0 + 0.2), INK_D, origin=(x0, y0, z0), rot=(28, 0, FAN[i] * 1.6),
           faces={"north": edge_lines(LINE)})
    m.cube(f"f{i}j", g, (x0 + 0.4, y0 - L * 0.56, z0 - 0.2), (x0 + 1.3, y0 - L * 0.4, z0 + 0.2), INK_D, origin=(x0, y0, z0), rot=(10, 0, FAN[i] - 30))
x0, y0, z0 = m.groups["thumb_r"]["origin"]
m.cube("thumb_a", "thumb_r", (x0 - 0.4, y0 - 2.6, z0 - 0.4), (x0 + 0.4, y0 + 0.2, z0 + 0.4), INK, origin=(x0, y0, z0), rot=(20, 0, 40), faces=all_faces(glove))
m.cube("thumb_b", "thumb_r", (x0 - 0.22, y0 - 4.6, z0 - 0.22), (x0 + 0.22, y0 - 2.4, z0 + 0.22), INK_D, origin=(x0, y0, z0), rot=(34, 0, 58))
# left forearm + small talons
m.cube("fore_l1", "fore_l", (-3.6 - 0.75, 16.4, -0.75), (-3.6 + 0.75, 20.4, 0.75), INK, faces=all_faces(glove))
m.cube("palm_l", "hand_l", (-3.7 - 0.8, 15.0, -0.75), (-3.7 + 0.8, 16.6, 0.75), INK, faces=all_faces(glove))
for i in range(4):
    x = -3.7 + (i - 1.5) * 0.42
    m.cube(f"tal{i}", "claws_l", (x - 0.17, 12.4 + 0.3 * abs(i - 1.5), -0.5), (x + 0.17, 15.2, -0.15), INK_D, origin=(x, 15.0, -0.3), rot=(12, 0, (i - 1.5) * -9),
           faces={"north": edge_lines(LINE)})
m.cube("tal_th", "claws_l", (-3.0 - 0.17, 13.2, -0.9), (-3.0 + 0.17, 15.2, -0.55), INK_D, origin=(-3.0, 15.0, -0.7), rot=(30, 0, 30))
# held ABC blocks (props for throws)
for g, sz in (("held_l", 1.0), ("held_r", 1.25)):
    x0, y0, z0 = m.groups[g]["origin"]
    ch = "C" if g == "held_l" else "A"
    m.cube("prop_" + g, g, (x0 - sz, y0 - sz, z0 - sz), (x0 + sz, y0 + sz, z0 + sz), BLOCK, origin=(x0, y0, z0), rot=(20, 30, 10),
           faces={"north": letter(ch), "south": letter("B"), "east": letter("B"), "west": letter(ch), "up": letter("C"), "down": letter("A")})

# ================================================================== animation
PROPS = {"held_l": 1, "held_r": 1}
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
        keys = [(0, *HIDE)] if t0 > 0 else []
        if t0 > 0: keys.append((t0 - 0.5, *HIDE))
        keys.append((t0, 1, 1, 1))
        if t1 < self.ticks:
            keys += [(t1, 1, 1, 1), (t1 + 0.5, *HIDE)]
        return self.scl(bone, *keys)

    def pluck(self, bone, t0, t1):
        """crown block vanishes at t0 and grows back at t1"""
        return self.scl(bone, (0, 1, 1, 1), (t0 - 0.5, 1, 1, 1), (t0, *HIDE), (t1, *HIDE), (t1 + 2, 1.3, 1.3, 1.3), (t1 + 4, 1, 1, 1))

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
        """hair secondary motion from one whip curve (x = forward/back flick, z = sideways)"""
        self.drape(["hair_b"], keys, delay=delay)
        self.drape(["hair_r"], [(t, x * 0.5, 0, z * 0.6 - abs(x) * 0.15) for (t, x, y, z) in keys], delay=delay)
        self.drape(["hair_l"], [(t, x * 0.5, 0, z * 0.6 + abs(x) * 0.15) for (t, x, y, z) in keys], delay=delay)
        self.drape(["bangs"], [(t, x * 0.3, 0, z * 0.3) for (t, x, y, z) in keys], delay=delay)
        self.drape(["blocks"], [(t, x * 0.25, 0, z * 0.3) for (t, x, y, z) in keys], delay=delay + 1)
        self.drape(["squiggle"], [(t, x * 0.8, 0, z * 0.9) for (t, x, y, z) in keys], delay=delay + 2)
        return self

    def skirt(self, keys, delay=2):
        """x>0 kicks the front out (back in), z>0 flares the right side out"""
        self.drape(["skirt_f"], [(t, x, 0, 0) for (t, x, y, z) in keys], delay=delay)
        self.drape(["skirt_b"], [(t, x * 0.7, 0, 0) for (t, x, y, z) in keys], delay=delay)
        self.drape(["skirt_r"], [(t, 0, 0, z) for (t, x, y, z) in keys], delay=delay)
        self.drape(["skirt_l"], [(t, 0, 0, z) for (t, x, y, z) in keys], delay=delay)
        return self

    def grip(self, *keys):
        """claw hand: keys (t, curl, spread). curl>0 = fingers hook forward/in, spread>0 = fan wider"""
        for i in range(4):
            self.rot(f"fing{i}", *[(t, c, 0, (1.5 - i) * sp) for (t, c, sp) in keys])
        self.rot("thumb_r", *[(t, c * 0.6, 0, -sp * 1.2) for (t, c, sp) in keys])
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


# rest pose = the reference: claw arm bent up in front, talon hand hanging at the skirt, slight hunch + head tilt
REST = {
    "arm_r": (14, -10, 30), "fore_r": (48, 0, -14), "hand_r": (0, 0, 14),
    "arm_l": (6, 0, -12), "fore_l": (16, 0, 8), "claws_l": (20, 0, 0),
    "chest": (-6, 0, 0), "head": (2, 0, 8),
}
for i in range(4): REST[f"fing{i}"] = (18, 0, (1.5 - i) * 6)
REST["thumb_r"] = (10, 0, 0)


def rest(b):
    return REST.get(b, (0, 0, 0))


def legs_both(a, keys_leg, keys_shin, keys_foot=None):
    for s, k in ((1, "r"), (-1, "l")):
        a.rot("leg_" + k, *[(t, x, y * s, z * s) for (t, x, y, z) in keys_leg])
        a.rot("shin_" + k, *keys_shin)
        if keys_foot: a.rot("foot_" + k, *keys_foot)


def R_(b, t):
    return (t, *rest(b))


# ------------------------------------------------------------------ idle (80 loop): hunched creepy sway, claw flexes, head ticks sideways, squiggle bobs
a = A("idle", 80, loop=True)
a.pos("body", (0, 0, 0, 0), (20, 0, -0.2, 0), (40, 0, 0, 0), (60, 0, -0.2, 0), (80, 0, 0, 0))
a.rot("body", (0, 0, 0, 2), (40, 0, 0, -2), (80, 0, 0, 2))
a.rot("chest", (0, -6, 4, -2), (20, -5, 2, 0), (40, -6, 4, 2), (60, -7, 6, 0), (80, -6, 4, -2))
a.rot("head", (0, 2, 0, 8), (24, 2, 0, 8), (26, 4, -6, 20), (34, 4, -6, 22), (37, 2, 0, 6), (60, 0, 4, 10), (80, 2, 0, 8))
a.rot("arm_r", (0, 14, -10, 30), (40, 18, -10, 33), (80, 14, -10, 30))
a.rot("fore_r", (0, 48, 0, -14), (40, 54, 0, -14), (80, 48, 0, -14))
a.grip((0, 18, 0), (44, 18, 0), (47, -10, 14), (50, 40, -4), (53, 0, 10), (56, 30, 0), (62, 18, 0), (80, 18, 0))
a.rot("arm_l", (0, 6, 0, -12), (40, 8, 0, -14), (80, 6, 0, -12))
a.rot("claws_l", (0, 20, 0, 0), (12, 20, 0, 0), (14, 50, 0, 0), (16, 10, 0, 0), (18, 50, 0, 0), (20, 20, 0, 0), (80, 20, 0, 0))
legs_both(a, [(0, 0, 0, 1), (80, 0, 0, 1)], [(0, 0, 0, 0), (80, 0, 0, 0)])
a.rot("leg_r", (0, -6, 0, 3), (40, -7, 0, 4), (80, -6, 0, 3))
a.rot("shin_r", (0, -8, 0, 0), (40, -10, 0, 0), (80, -8, 0, 0))
a.hair([(0, 0, 0, 2), (20, -3, 0, 0), (26, 0, 0, 8), (40, 0, 0, -2), (60, -3, 0, 0), (80, 0, 0, 2)], delay=4)
a.rot("squiggle", (0, 0, 0, 0), (20, 0, 40, 6), (40, 0, 0, 0), (60, 0, -40, -6), (80, 0, 0, 0))
a.pos("squiggle", (0, 0, 0, 0), (20, 0, 0.5, 0), (40, 0, 0, 0), (60, 0, 0.5, 0), (80, 0, 0, 0))
a.skirt([(0, 2, 0, 1), (40, 1, 0, -1), (80, 2, 0, 1)], delay=4)
a.done()

# ------------------------------------------------------------------ walk (20 loop): lurching stride, heavy claw swinging with lag, skirt swish
a = A("walk", 20, loop=True)
a.rot("leg_r", (0, 28, 0, 0), (5, 0, 0, 0), (10, -26, 0, 0), (15, 0, 0, 0), (20, 28, 0, 0))
a.rot("shin_r", (0, -4, 0, 0), (5, -6, 0, 0), (10, -10, 0, 0), (13, -50, 0, 0), (17, -24, 0, 0), (20, -4, 0, 0))
a.rot("foot_r", (0, -12, 0, 0), (10, 12, 0, 0), (20, -12, 0, 0))
a.rot("leg_l", (0, -26, 0, 0), (5, 0, 0, 0), (10, 28, 0, 0), (15, 0, 0, 0), (20, -26, 0, 0))
a.rot("shin_l", (0, -10, 0, 0), (3, -50, 0, 0), (7, -24, 0, 0), (10, -4, 0, 0), (15, -6, 0, 0), (20, -10, 0, 0))
a.rot("foot_l", (0, 12, 0, 0), (10, -12, 0, 0), (20, 12, 0, 0))
a.pos("body", (0, 0, -0.5, 0), (5, 0, 0.3, 0), (10, 0, -0.5, 0), (15, 0, 0.3, 0), (20, 0, -0.5, 0))
a.rot("body", (0, -6, 6, -3), (10, -6, -6, 3), (20, -6, 6, -3))
a.rot("chest", (0, -2, -5, 2), (10, -2, 5, -2), (20, -2, -5, 2))
a.rot("head", (0, 0, 4, -3), (10, 0, -4, 3), (20, 0, 4, -3))
a.rot("arm_r", (2, -16, 0, 2), (12, 18, 0, 6), (20, -14, 0, 2))
a.rot("fore_r", (0, 4, 0, 0), (6, -6, 0, 0), (12, 10, 0, 0), (20, 4, 0, 0))
a.grip((0, 0, 0), (4, 10, -4), (12, -6, 4), (20, 0, 0))
a.rot("arm_l", (0, 20, 0, -2), (10, -18, 0, -2), (20, 20, 0, -2))
a.rot("fore_l", (0, 10, 0, 0), (10, 2, 0, 0), (20, 10, 0, 0))
a.hair([(0, -8, 0, 4), (5, -11, 0, 0), (10, -8, 0, -4), (15, -11, 0, 0), (20, -8, 0, 4)], delay=2)
a.skirt([(0, 7, 0, 4), (5, 3, 0, 0), (10, 7, 0, -4), (15, 3, 0, 0), (20, 7, 0, 4)], delay=1)
tracks = {b: {ch: sorted([(t / 20.0, x, y, z) for (t, x, y, z) in v]) for ch, v in chs.items()} for b, chs in a.tr.items()}
m.anim("walk", 1.0, tracks, loop=True)

# ------------------------------------------------------------------ abc_throw (32): pluck C from crown 6, left side-arm throw 12, claw plucks A 16, overhand hurl 22
a = A("abc_throw", 32)
a.pluck("blk_c", 6, 26).pluck("blk_a", 16, 28)
a.show("held_l", 6, 12).show("held_r", 16, 22)
a.rot("arm_l", R_("arm_l", 0), (4, 150, 0, 20), (6, 165, 0, 26), (9, 200, 30, -30), (11, 140, 0, -20), (12, 80, 0, -10), (15, 30, 0, -16),
      (20, 10, 0, -20), (32, *rest("arm_l")))
a.rot("fore_l", R_("fore_l", 0), (4, 60, 0, 0), (6, 70, 0, 0), (9, 60, 0, 0), (12, 0, 0, 0), (20, 10, 0, 0), (32, *rest("fore_l")))
a.rot("claws_l", (0, 20, 0, 0), (5, -10, 0, 0), (6, 60, 0, 0), (11, 60, 0, 0), (12, -20, 0, 0), (18, 20, 0, 0))
a.rot("arm_r", R_("arm_r", 0), (8, 30, -10, 30), (12, 60, 0, 40), (14, 150, 0, 10), (16, 170, 0, -6), (19, 215, 0, 14), (21, 140, 0, 6), (22, 80, 0, 0),
      (25, 40, 0, 10), (32, *rest("arm_r")))
a.rot("fore_r", R_("fore_r", 0), (12, 60, 0, -20), (16, 60, 0, 0), (19, 70, 0, 0), (22, 0, 0, 0), (25, 10, 0, 0), (32, *rest("fore_r")))
a.rot("hand_r", R_("hand_r", 0), (16, 20, 0, 0), (22, -10, 0, 0), (32, *rest("hand_r")))
a.grip((0, 18, 0), (14, -10, 12), (16, 50, -4), (21, 50, -4), (22, -20, 14), (26, 10, 4), (32, 18, 0))
a.rot("chest", R_("chest", 0), (6, 0, 14, 0), (9, 6, 30, 0), (12, -10, -24, 0), (16, 4, -6, 0), (19, 12, 30, 0), (22, -16, -34, 0), (26, -10, -20, 0), (32, *rest("chest")))
a.rot("body", (0, 0, 0, 0), (9, 0, 14, 0), (12, -6, -10, 0), (19, 4, 16, 0), (22, -10, -16, 0), (32, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (19, 0, 0, 0.8), (22, 0, -1.2, -1.4), (27, 0, -0.6, -0.6), (32, 0, 0, 0))
a.rot("head", R_("head", 0), (5, 24, 20, 12), (9, 0, -20, 0), (12, -6, 16, 0), (16, 20, -16, -10), (19, 6, -20, 0), (22, -10, 20, 6), (27, 0, 0, 14), (32, *rest("head")))
a.rot("leg_r", (0, 0, 0, 0), (19, 10, 0, 4), (22, -24, 0, 4), (28, -8, 0, 0), (32, 0, 0, 0))
a.rot("leg_l", (0, 0, 0, 0), (12, 16, 0, -4), (19, -10, 0, -4), (22, 34, 0, -4), (28, 10, 0, 0), (32, 0, 0, 0))
a.rot("shin_l", (0, 0, 0, 0), (12, -10, 0, 0), (22, -30, 0, 0), (32, 0, 0, 0))
a.hair([(0, 0, 0, 0), (6, 8, 0, 8), (9, 12, 0, -6), (12, -14, 0, 8), (19, 16, 0, -8), (22, -26, 0, 10), (26, -10, 0, 0), (32, 0, 0, 0)])
a.skirt([(0, 0, 0, 0), (12, 6, 0, -6), (19, -4, 0, 6), (22, 14, 0, -8), (27, 4, 0, 0), (32, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ letter_rain (56): arms to the sky 10, left writes glyphs 10-22, claw conducts each drop 22..43, final point 44
a = A("letter_rain", 56)
arm_r = [R_("arm_r", 0), (8, 170, 0, 30), (12, 175, 0, 26), (21, 175, 0, 26)]
fing = [(0, 18, 0), (8, -20, 16), (21, -20, 16)]
for k, t in enumerate(range(22, 44, 3)):
    arm_r += [(t, 120, 0, 34 if k % 2 else 14), (t + 1.5, 165, 0, 24)]
    fing += [(t, 40, -4), (t + 1.5, -10, 12)]
arm_r += [(44, 80, 0, 6), (48, 76, 0, 8), (56, *rest("arm_r"))]
fing += [(44, -24, 18), (48, -16, 14), (56, 18, 0)]
a.rot("arm_r", *arm_r).grip(*fing)
a.rot("fore_r", R_("fore_r", 0), (8, 10, 0, 0), (21, 10, 0, 0), (44, 0, 0, 0), (50, 10, 0, 0), (56, *rest("fore_r")))
a.rot("hand_r", R_("hand_r", 0), (8, 0, 0, 0), (44, -20, 0, 0), (56, *rest("hand_r")))
arm_l = [R_("arm_l", 0), (8, 160, 0, -30)]
for k, t in enumerate(range(10, 22, 2)):
    arm_l.append((t, 150 + (10 if k % 2 else -10), 20 * (1 if k % 3 else -1), -30 + (14 if k % 2 else -8)))
arm_l += [(22, 140, 0, -40), (43, 140, 0, -44), (44, 70, 0, -20), (56, *rest("arm_l"))]
a.rot("arm_l", *arm_l)
a.rot("fore_l", R_("fore_l", 0), (8, 20, 0, 0), (22, 30, 0, 0), (44, 0, 0, 0), (56, *rest("fore_l")))
a.rot("claws_l", (0, 20, 0, 0), (8, -10, 0, 0), (44, -20, 0, 0), (56, 20, 0, 0))
chest = [R_("chest", 0), (8, 18, 0, 0), (21, 16, 0, 0)]
body = [(0, 0, 0, 0), (8, 0, 0, 0)]
for k, t in enumerate(range(22, 44, 3)):
    chest += [(t, 6, 8 if k % 2 else -8, 0), (t + 1.5, 14, 0, 0)]
    body.append((t, 0, 0, 3 if k % 2 else -3))
chest += [(44, -18, -10, 0), (48, -14, -8, 0), (56, *rest("chest"))]
body += [(44, -8, 0, 0), (56, 0, 0, 0)]
a.rot("chest", *chest).rot("body", *body)
a.pos("body", (0, 0, 0, 0), (8, 0, 0.8, 0), (21, 0, 0.8, 0), (22, 0, -0.4, 0), (43, 0, -0.4, 0), (44, 0, -1.6, -1.0), (50, 0, -1.0, -0.6), (56, 0, 0, 0))
a.rot("head", R_("head", 0), (8, 34, 0, 0), (14, 30, 0, 10), (20, 30, 0, -10), (22, 10, 0, 14), (32, 10, 0, -14), (43, 10, 0, 14), (44, -10, 0, 0), (56, *rest("head")))
a.scl("jaw", (0, 1, 1, 1), (8, 1, 1.5, 1), (12, 1, 1.1, 1), (16, 1, 1.5, 1), (20, 1, 1, 1), (56, 1, 1, 1))
legs_both(a, [(0, 0, 0, 0), (8, 0, 0, 3), (21, 0, 0, 3), (44, 0, 0, 8), (56, 0, 0, 0)], [(0, 0, 0, 0), (56, 0, 0, 0)])
a.rot("leg_r", (44, -20, 0, 6), (50, -14, 0, 4), (56, 0, 0, 0))
a.rot("leg_l", (44, 24, 0, -6), (50, 14, 0, -4), (56, 0, 0, 0))
a.rot("shin_l", (0, 0, 0, 0), (44, -30, 0, 0), (56, 0, 0, 0))
a.pos("root", (0, 0, 0, 0), (7, 0, 0, 0), (9, 0, 0.8, 0), (12, 0, 0, 0), (56, 0, 0, 0))
a.hair([(0, 0, 0, 0), (8, 16, 0, 0), (14, 10, 0, 8), (20, 10, 0, -8), (22, -6, 0, 0), (34, -6, 0, 6), (43, -6, 0, -6), (44, -24, 0, 0), (50, -8, 0, 0), (56, 0, 0, 0)])
a.skirt([(0, 0, 0, 0), (8, -4, 0, 0), (22, 4, 0, 4), (32, 4, 0, -4), (44, 14, 0, 6), (56, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ rake (40): forehand 9, backhand 18, overhead rake 30 (dashes 7/16/27)
a = A("rake", 40)
a.rot("arm_r", R_("arm_r", 0), (5, -30, 0, 70), (7, 10, 0, 70), (9, 80, 0, -30), (11, 80, 0, -50), (14, 70, -20, -56), (16, 80, 0, -20), (18, 80, 0, 60),
      (20, 70, 0, 74), (23, 140, 0, 30), (26, 200, 0, 10), (28, 170, 0, 6), (30, 50, 0, -4), (33, 30, 0, 0), (40, *rest("arm_r")))
a.rot("fore_r", R_("fore_r", 0), (5, 40, 0, 0), (9, 0, 0, 0), (14, 30, 0, 0), (18, 0, 0, 0), (23, 30, 0, 0), (26, 40, 0, 0), (30, 0, 0, 0), (34, 10, 0, 0), (40, *rest("fore_r")))
a.rot("hand_r", R_("hand_r", 0), (5, 0, 0, 30), (9, 0, 0, -30), (14, 0, 0, -30), (18, 0, 0, 40), (26, -30, 0, 0), (30, 30, 0, 0), (40, *rest("hand_r")))
a.grip((0, 18, 0), (5, -10, 14), (8, -10, 14), (9, 40, 6), (12, 20, 4), (16, -10, 14), (18, 40, 6), (22, 10, 4), (26, -30, 18), (29, -20, 16), (30, 60, 4),
       (34, 40, 0), (40, 18, 0))
a.rot("arm_l", R_("arm_l", 0), (5, 20, 0, -30), (9, -30, 0, -40), (14, 20, 0, -50), (18, -10, 0, -30), (26, -30, 0, -40), (30, 40, 0, -30), (40, *rest("arm_l")))
a.rot("chest", R_("chest", 0), (5, 2, -34, 6), (9, -10, 36, -4), (12, -8, 40, 0), (14, -6, 36, 0), (18, -10, -36, 6), (21, -6, -30, 4), (26, 16, -6, 0),
      (30, -34, 6, 0), (34, -26, 4, 0), (40, *rest("chest")))
a.rot("body", (0, 0, 0, 0), (5, 0, -14, 0), (9, -8, 16, 0), (18, -8, -16, 0), (26, 6, 0, 0), (30, -16, 0, 0), (36, -6, 0, 0), (40, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (7, 0, -0.6, 0), (9, 0, -1.2, -1.2), (16, 0, -0.6, -0.6), (18, 0, -1.2, -1.4), (26, 0, 0.6, 0), (30, 0, -2.6, -1.8), (34, 0, -2.4, -1.4), (40, 0, 0, 0))
a.rot("head", R_("head", 0), (5, 0, 20, 8), (9, -8, -20, 0), (14, -6, -16, 10), (18, -8, 20, 0), (26, 20, 0, -10), (30, -14, 0, 0), (34, -10, 0, 12), (40, *rest("head")))
a.rot("leg_r", (0, 0, 0, 0), (9, -24, 0, 4), (16, 10, 0, 4), (18, -20, 0, 4), (26, 0, 0, 4), (30, -36, 0, 4), (34, -32, 0, 4), (40, 0, 0, 0))
a.rot("shin_r", (0, 0, 0, 0), (30, -20, 0, 0), (36, -10, 0, 0), (40, 0, 0, 0))
a.rot("leg_l", (0, 0, 0, 0), (9, 20, 0, -4), (16, -10, 0, -4), (18, 24, 0, -4), (26, 4, 0, -4), (30, 30, 0, -4), (34, 28, 0, -4), (40, 0, 0, 0))
a.rot("shin_l", (0, 0, 0, 0), (9, -30, 0, 0), (18, -30, 0, 0), (30, -50, 0, 0), (36, -30, 0, 0), (40, 0, 0, 0))
a.hair([(0, 0, 0, 0), (5, 6, 0, -12), (9, -18, 0, 16), (12, -12, 0, 18), (18, -18, 0, -16), (21, -12, 0, -18), (26, 14, 0, 0), (30, -30, 0, 0), (34, -14, 0, 4), (40, 0, 0, 0)])
a.skirt([(0, 0, 0, 0), (5, -4, 0, -6), (9, 10, 0, 12), (18, 12, 0, -14), (26, -4, 0, 0), (30, 20, 0, 10), (36, 6, 0, 2), (40, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ claw_smash (44): crouch 6, rear up on toes 18 (claw high), quiver, SLAM 22, hold, rise
a = A("claw_smash", 44)
a.rot("arm_r", R_("arm_r", 0), (6, -20, 0, 40), (14, 190, 0, 20), (18, 205, 0, 14), (20, 200, 0, 16), (21, 140, 0, 10), (22, 40, 0, 0), (30, 36, 0, 2), (36, 30, 0, 10), (44, *rest("arm_r")))
a.rot("fore_r", R_("fore_r", 0), (6, 50, 0, 0), (14, 40, 0, 0), (18, 50, 0, 0), (22, 0, 0, 0), (30, 0, 0, 0), (38, 30, 0, 0), (44, *rest("fore_r")))
a.rot("hand_r", R_("hand_r", 0), (18, -30, 0, 0), (22, 20, 0, 0), (30, 30, 0, 0), (44, *rest("hand_r")))
a.grip((0, 18, 0), (14, -20, 20), (18, -30, 22), (19, -20, 18), (20, -30, 22), (22, 30, 20), (30, 34, 22), (36, 20, 6), (44, 18, 0))
a.rot("arm_l", R_("arm_l", 0), (6, -20, 0, -40), (14, 150, 0, -30), (18, 160, 0, -30), (22, 20, 0, -50), (30, 16, 0, -50), (44, *rest("arm_l")))
a.rot("fore_l", R_("fore_l", 0), (14, 40, 0, 0), (22, 0, 0, 0), (44, *rest("fore_l")))
a.rot("chest", R_("chest", 0), (6, -16, 0, 0), (14, 22, 10, 0), (18, 26, 14, 0), (22, -42, -6, 0), (30, -40, -6, 0), (38, -14, 0, 0), (44, *rest("chest")))
a.rot("body", (0, 0, 0, 0), (6, -10, 0, 0), (14, 10, 0, 0), (18, 12, 0, 0), (22, -22, 0, 0), (30, -20, 0, 0), (38, -6, 0, 0), (44, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (6, 0, -1.6, 0), (14, 0, 0.8, 0.8), (18, 0, 1.0, 1.0), (22, 0, -3.0, -1.6), (23, 0, -3.4, -1.6), (30, 0, -3.0, -1.6), (38, 0, -1.0, -0.4), (44, 0, 0, 0))
a.pos("root", (0, 0, 0, 0), (12, 0, 0, 0), (16, 0, 0.8, 0), (20, 0, 0.8, 0), (22, 0, 0, 0), (23, 0, -0.3, 0), (24, 0, 0, 0), (44, 0, 0, 0))
a.rot("head", R_("head", 0), (6, -10, 0, 0), (14, 30, 0, 0), (18, 30, 0, -6), (19, 30, 0, 6), (20, 30, 0, -6), (22, -6, 0, 0), (26, 10, 0, 14), (30, 10, 0, 12), (44, *rest("head")))
a.scl("jaw", (0, 1, 1, 1), (14, 1, 1.6, 1), (20, 1, 1.6, 1), (22, 1, 1, 1))
legs_both(a, [(0, 0, 0, 0), (6, 30, 0, 6), (14, 0, 0, 2), (18, 0, 0, 2), (22, 40, 0, 10), (30, 38, 0, 10), (38, 14, 0, 4), (44, 0, 0, 0)],
          [(0, 0, 0, 0), (6, -50, 0, 0), (14, 0, 0, 0), (22, -70, 0, 0), (30, -66, 0, 0), (38, -24, 0, 0), (44, 0, 0, 0)],
          [(0, 0, 0, 0), (6, 20, 0, 0), (14, -20, 0, 0), (18, -24, 0, 0), (22, 30, 0, 0), (30, 28, 0, 0), (44, 0, 0, 0)])
a.rot("leg_l", (22, -10, 0, -8), (30, -10, 0, -8))
a.rot("shin_l", (22, -20, 0, 0), (30, -20, 0, 0))
a.hair([(0, 0, 0, 0), (6, 6, 0, 0), (14, -16, 0, 0), (18, -20, 0, 0), (22, 40, 0, 0), (25, 28, 0, 6), (30, 10, 0, 0), (44, 0, 0, 0)])
a.skirt([(0, 0, 0, 0), (6, 8, 0, 6), (14, -8, 0, -2), (22, 26, 0, 24), (26, 18, 0, 18), (36, 6, 0, 4), (44, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ scratch_lunge (30): coil low 10, dash 10, rising uppercut claw 14, airborne follow-through, land
a = A("scratch_lunge", 30)
a.rot("arm_r", R_("arm_r", 0), (6, -50, 0, 30), (10, -60, 0, 24), (12, 40, 0, 10), (14, 160, 0, -10), (17, 200, 0, -16), (22, 150, 0, 0), (30, *rest("arm_r")))
a.rot("fore_r", R_("fore_r", 0), (6, 10, 0, 0), (10, 0, 0, 0), (14, 10, 0, 0), (17, 30, 0, 0), (30, *rest("fore_r")))
a.rot("hand_r", R_("hand_r", 0), (10, -30, 0, 0), (14, 30, 0, 0), (30, *rest("hand_r")))
a.grip((0, 18, 0), (6, -20, 18), (10, -24, 20), (13, -20, 18), (14, 50, 8), (18, 40, 4), (24, 20, 0), (30, 18, 0))
a.rot("arm_l", R_("arm_l", 0), (6, 30, 0, -40), (10, 40, 0, -50), (14, -40, 0, -50), (20, -20, 0, -30), (30, *rest("arm_l")))
a.rot("chest", R_("chest", 0), (6, -34, -20, 0), (10, -40, -24, 0), (12, -30, -10, 0), (14, 10, 20, 0), (17, 18, 24, 0), (24, 0, 6, 0), (30, *rest("chest")))
a.rot("body", (0, 0, 0, 0), (6, -26, -10, 0), (10, -30, -12, 0), (12, -34, 0, 0), (14, -4, 14, 0), (17, 6, 16, 0), (24, 0, 4, 0), (30, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (6, 0, -4.0, 1.0), (10, 0, -4.4, 1.2), (12, 0, -2.0, -1.8), (14, 0, 0.4, -1.0), (17, 0, 0.8, 0), (22, 0, -1.6, 0), (30, 0, 0, 0))
a.pos("root", (0, 0, 0, 0), (12, 0, 0, 0), (14, 0, 1.6, 0), (17, 0, 2.2, 0), (20, 0, 0.6, 0), (21, 0, 0, 0), (30, 0, 0, 0))
a.rot("head", R_("head", 0), (6, 30, 0, 0), (10, 36, 0, 0), (12, 30, 0, 0), (14, 6, -10, 0), (17, 14, -10, 0), (24, 4, 0, 12), (30, *rest("head")))
legs_both(a, [(0, 0, 0, 0), (6, 70, 0, 10), (10, 76, 0, 10), (12, 10, 0, 6), (14, -14, 0, 4), (17, 10, 0, 6), (21, 30, 0, 6), (24, 16, 0, 4), (30, 0, 0, 0)],
          [(0, 0, 0, 0), (6, -110, 0, 0), (10, -116, 0, 0), (12, -20, 0, 0), (14, -10, 0, 0), (17, -50, 0, 0), (21, -50, 0, 0), (24, -20, 0, 0), (30, 0, 0, 0)],
          [(0, 0, 0, 0), (6, 40, 0, 0), (10, 40, 0, 0), (14, -30, 0, 0), (21, 20, 0, 0), (30, 0, 0, 0)])
a.rot("leg_l", (6, 10, 0, -6), (10, 12, 0, -6), (12, 50, 0, -4))
a.rot("shin_l", (6, -60, 0, 0), (10, -64, 0, 0), (12, -40, 0, 0))
a.hair([(0, 0, 0, 0), (6, 10, 0, 0), (10, 14, 0, 0), (12, -30, 0, 0), (14, -40, 0, 6), (17, -20, 0, 0), (21, 24, 0, 0), (26, 4, 0, 0), (30, 0, 0, 0)])
a.skirt([(0, 0, 0, 0), (6, 20, 0, 10), (10, 22, 0, 12), (12, -16, 0, 6), (14, -22, 0, 4), (17, -10, 0, 0), (21, 20, 0, 14), (26, 4, 0, 2), (30, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ shard_throw (34): claw coiled across to left shoulder 12, backhand flick 14 (fingers fan), hold, recover
a = A("shard_throw", 34)
a.rot("arm_r", R_("arm_r", 0), (6, 60, 0, -40), (11, 80, -20, -70), (12, 82, -20, -72), (14, 86, 0, 80), (17, 80, 0, 84), (22, 50, 0, 60), (34, *rest("arm_r")))
a.rot("fore_r", R_("fore_r", 0), (6, 70, 0, 0), (12, 90, 0, 0), (14, 0, 0, 0), (22, 10, 0, 0), (34, *rest("fore_r")))
a.rot("hand_r", R_("hand_r", 0), (12, 0, 0, -40), (14, 0, 0, 30), (17, 0, 0, 40), (34, *rest("hand_r")))
a.grip((0, 18, 0), (6, 50, -4), (12, 60, -6), (13, 50, -4), (14, -20, 24), (16, -24, 26), (20, 0, 14), (26, 10, 4), (34, 18, 0))
a.rot("arm_l", R_("arm_l", 0), (12, 30, 0, -50), (14, -20, 0, -40), (22, -10, 0, -30), (34, *rest("arm_l")))
a.rot("chest", R_("chest", 0), (6, -4, 24, 0), (12, -10, 44, 4), (14, -4, -36, -6), (17, -2, -40, -6), (24, -4, -14, 0), (34, *rest("chest")))
a.rot("body", (0, 0, 0, 0), (12, -6, 18, 0), (14, -2, -16, 0), (22, 0, -8, 0), (34, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (12, 0, -1.2, 0.4), (14, 0, -0.8, -0.8), (22, 0, -0.4, -0.4), (34, 0, 0, 0))
a.rot("head", R_("head", 0), (12, -4, -36, 10), (14, -4, 30, 0), (18, 4, 34, -10), (26, 0, 10, 10), (34, *rest("head")))
a.rot("leg_r", (0, 0, 0, 0), (12, 16, 0, 4), (14, -24, 0, 10), (24, -10, 0, 4), (34, 0, 0, 0))
a.rot("leg_l", (0, 0, 0, 0), (12, -14, 0, -4), (14, 16, 0, -4), (24, 6, 0, 0), (34, 0, 0, 0))
a.rot("shin_r", (0, 0, 0, 0), (12, -20, 0, 0), (14, 0, 0, 0), (34, 0, 0, 0))
a.hair([(0, 0, 0, 0), (12, 4, 0, -16), (14, -10, 0, 24), (17, -8, 0, 26), (24, 0, 0, 4), (34, 0, 0, 0)])
a.skirt([(0, 0, 0, 0), (12, 2, 0, -10), (14, 6, 0, 18), (18, 6, 0, 20), (26, 2, 0, 2), (34, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ spelling_test (50): writes the word 0-8 (thrust 8), scribbles + claw points 8-30, jabs each burst 32/36/38/40/44, cheer 38+
a = A("spelling_test", 50)
arm_l = [R_("arm_l", 0), (3, 90, 0, -20), (5, 100, 30, -40), (7, 90, -30, -10), (8, 100, 0, -20)]
for k, t in enumerate(range(10, 31, 2)):
    arm_l.append((t, 80 + (8 if k % 2 else -6), 30 * math.sin(k * 1.3), -24 + (6 if k % 3 else -6)))
arm_l += [(32, 60, 0, -30), (38, 170, 0, -40), (42, 160, 0, -30), (50, *rest("arm_l"))]
a.rot("arm_l", *arm_l)
a.rot("fore_l", R_("fore_l", 0), (5, 30, 0, 0), (8, 0, 0, 0), (20, 20, 0, 0), (32, 10, 0, 0), (38, 0, 0, 0), (50, *rest("fore_l")))
a.rot("claws_l", (0, 20, 0, 0), (3, -20, 0, 0), (32, -20, 0, 0), (38, -40, 0, 0), (50, 20, 0, 0))
arm_r = [R_("arm_r", 0), (8, 40, 0, 30), (12, 80, 0, 10), (30, 80, 0, 14)]
fing = [(0, 18, 0), (8, 30, 0), (12, 60, -10), (30, 60, -10)]
for t in (32, 36, 38, 40, 44):
    big = t == 38
    arm_r += [(t - 1.5, 110 if big else 95, 0, 10), (t, 70 if big else 78, 0, 8)]
    fing += [(t - 1, 60, -10), (t, 20 if big else 50, 10 if big else -6)]
arm_r += [(47, 80, 0, 20), (50, *rest("arm_r"))]
fing += [(50, 18, 0)]
a.rot("arm_r", *arm_r).grip(*fing)
a.rot("fore_r", R_("fore_r", 0), (12, 10, 0, 0), (30, 10, 0, 0), (44, 0, 0, 0), (50, *rest("fore_r")))
a.rot("hand_r", R_("hand_r", 0), (12, -30, 0, 0), (44, -20, 0, 0), (50, *rest("hand_r")))
a.rot("chest", R_("chest", 0), (5, 0, -20, 0), (8, -4, 20, 0), (14, -2, 10, 4), (22, -2, 14, -4), (30, -2, 10, 4), (32, -8, -10, 0), (38, 14, 0, 0), (42, 10, 0, 0), (50, *rest("chest")))
a.rot("head", R_("head", 0), (5, -10, -20, 0), (8, -6, 10, 10), (16, 4, 0, -16), (24, 4, 0, 18), (30, 0, 0, -10), (36, -4, 0, 10), (38, 24, 0, 0), (42, 22, 0, 10), (46, 20, 0, -10), (50, *rest("head")))
a.scl("jaw", (0, 1, 1, 1), (36, 1, 1, 1), (38, 1.1, 1.8, 1), (44, 1, 1.4, 1), (48, 1, 1, 1))
a.rot("body", (0, 0, 0, 0), (8, 0, 10, 0), (30, 0, 6, 0), (38, 6, 0, 0), (44, 0, 0, 0), (50, 0, 0, 0))
a.pos("root", (0, 0, 0, 0), (37, 0, 0, 0), (39, 0, 1.0, 0), (41, 0, 0, 0), (43, 0, 0.8, 0), (45, 0, 0, 0), (50, 0, 0, 0))
legs_both(a, [(0, 0, 0, 0), (38, 0, 0, 2), (50, 0, 0, 0)], [(0, 0, 0, 0), (50, 0, 0, 0)])
a.rot("leg_r", (8, -10, 0, 4), (30, -10, 0, 4), (38, -4, 0, 2), (39, 20, 0, 4), (41, -4, 0, 2), (43, 20, 0, 4), (45, 0, 0, 0))
a.rot("shin_r", (38, 0, 0, 0), (39, -40, 0, 0), (41, 0, 0, 0), (43, -40, 0, 0), (45, 0, 0, 0))
a.hair([(0, 0, 0, 0), (8, 4, 0, 10), (16, 0, 0, -10), (24, 0, 0, 10), (32, -6, 0, 0), (38, 16, 0, 0), (40, -10, 0, 6), (44, 10, 0, -6), (50, 0, 0, 0)])
a.skirt([(0, 0, 0, 0), (8, 2, 0, 4), (30, 2, 0, -4), (39, -6, 0, 10), (41, 6, 0, -6), (44, -4, 0, 8), (50, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ grab_rip (52): lean + claw opens 6, GRAB 10, hoist 16, squeezes 16/22/28, wind back 34, RIP & fling 36
a = A("grab_rip", 52)
a.rot("arm_r", R_("arm_r", 0), (6, 60, 0, 30), (9, 90, 0, 10), (10, 92, 0, 6), (13, 110, 0, 8), (16, 130, 0, 10), (22, 132, 0, 12), (28, 130, 0, 10),
      (33, 150, -20, 50), (35, 150, -20, 54), (36, 70, 0, -60), (39, 60, 0, -70), (44, 40, 0, -30), (52, *rest("arm_r")))
a.rot("fore_r", R_("fore_r", 0), (6, 20, 0, 0), (10, 0, 0, 0), (16, 20, 0, 0), (34, 40, 0, 0), (36, 0, 0, 0), (44, 20, 0, 0), (52, *rest("fore_r")))
a.rot("hand_r", R_("hand_r", 0), (6, -30, 0, 0), (10, -10, 0, 0), (16, -20, 0, 0), (36, 0, 0, -40), (52, *rest("hand_r")))
a.grip((0, 18, 0), (6, -30, 26), (9, -30, 26), (10, 70, -6), (15, 70, -6), (16, 85, -12), (18, 70, -6), (22, 85, -12), (24, 70, -6), (28, 88, -14),
       (30, 70, -6), (35, 72, -6), (36, -24, 28), (40, -20, 24), (46, 10, 6), (52, 18, 0))
a.rot("arm_l", R_("arm_l", 0), (6, 40, 0, -30), (10, 20, 0, -40), (16, 40, 0, -20), (28, 40, 0, -20), (36, -30, 0, -50), (44, -10, 0, -30), (52, *rest("arm_l")))
a.rot("claws_l", (0, 20, 0, 0), (16, -20, 0, 0), (17, 40, 0, 0), (28, 40, 0, 0), (52, 20, 0, 0))
a.rot("chest", R_("chest", 0), (6, -26, 10, 0), (10, -30, 0, 0), (16, 6, 0, 0), (22, 8, 0, 4), (28, 6, 0, -4), (35, 4, -40, 0), (36, -16, 40, 0), (40, -12, 44, 0), (48, -6, 10, 0), (52, *rest("chest")))
a.rot("body", (0, 0, 0, 0), (6, -14, 0, 0), (10, -18, 0, 0), (16, 0, 0, 0), (35, 0, -20, 0), (36, -6, 20, 0), (44, 0, 6, 0), (52, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (6, 0, -1.4, -0.6), (10, 0, -1.8, -1.6), (16, 0, 0, 0), (22, 0, -0.3, 0), (28, 0, 0, 0), (36, 0, -1.0, -0.6), (52, 0, 0, 0))
a.rot("head", R_("head", 0), (6, -10, 0, 0), (10, -6, 0, 0), (16, 20, 0, 16), (19, 22, 0, -10), (22, 20, 0, 18), (25, 22, 0, -10), (28, 20, 0, 18), (35, 6, -30, 0),
      (36, -4, 30, 0), (44, 0, 10, 10), (52, *rest("head")))
a.scl("jaw", (0, 1, 1, 1), (14, 1, 1, 1), (16, 1.1, 1.6, 1), (28, 1.1, 1.6, 1), (32, 1, 1, 1))
legs_both(a, [(0, 0, 0, 0), (6, 10, 0, 4), (10, 0, 0, 4), (16, 0, 0, 6), (36, 0, 0, 6), (52, 0, 0, 0)], [(0, 0, 0, 0), (52, 0, 0, 0)])
a.rot("leg_r", (6, -30, 0, 4), (10, -40, 0, 4), (16, -16, 0, 4), (36, -20, 0, 8), (44, -6, 0, 2))
a.rot("leg_l", (6, 30, 0, -4), (10, 36, 0, -4), (16, 10, 0, -4), (36, 20, 0, -4), (44, 6, 0, 0))
a.rot("shin_l", (6, -40, 0, 0), (10, -40, 0, 0), (16, -10, 0, 0), (52, 0, 0, 0))
a.hair([(0, 0, 0, 0), (6, 10, 0, 0), (10, -16, 0, 0), (16, 10, 0, 10), (22, 10, 0, -10), (28, 10, 0, 10), (35, 6, 0, -20), (36, -10, 0, 30), (40, -8, 0, 26), (52, 0, 0, 0)])
a.skirt([(0, 0, 0, 0), (6, 8, 0, 4), (10, 16, 0, 6), (16, 0, 0, 0), (35, 2, 0, -10), (36, 8, 0, 22), (44, 2, 0, 4), (52, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ screech (36): inhale 0-10 (lean back), SHRIEK 12 (mouth wide, arms flung back), vibrating 12-22, recover
a = A("screech", 36)
a.scl("jaw", (0, 1, 1, 1), (8, 0.9, 0.7, 1), (10, 0.9, 0.7, 1), (12, 1.3, 2.6, 1), (22, 1.3, 2.5, 1), (28, 1, 1, 1))
a.pos("jaw", (0, 0, 0, 0), (10, 0, 0, 0), (12, 0, -0.6, -0.1), (22, 0, -0.6, -0.1), (28, 0, 0, 0))
head = [R_("head", 0), (8, 30, 0, 0), (10, 34, 0, 0), (12, -14, 0, 0)]
for t in range(13, 23):
    head.append((t, -14 + (2 if t % 2 else -2), 0, 5 if t % 2 else -5))
head += [(26, -4, 0, 8), (36, *rest("head"))]
a.rot("head", *head)
a.rot("chest", R_("chest", 0), (8, 20, 0, 0), (10, 22, 0, 0), (12, -24, 0, 0), (22, -20, 0, 0), (28, -8, 0, 0), (36, *rest("chest")))
a.rot("body", (0, 0, 0, 0), (10, 8, 0, 0), (12, -12, 0, 0), (22, -10, 0, 0), (36, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (10, 0, 0.6, 0.6), (12, 0, -1.4, -1.0), (22, 0, -1.2, -0.8), (36, 0, 0, 0))
a.rot("arm_r", R_("arm_r", 0), (8, 30, 0, 30), (10, 34, 0, 34), (12, -40, 0, 70), (22, -36, 0, 72), (28, 0, 0, 40), (36, *rest("arm_r")))
a.rot("fore_r", R_("fore_r", 0), (10, 40, 0, 0), (12, 10, 0, 0), (22, 10, 0, 0), (36, *rest("fore_r")))
a.grip((0, 18, 0), (10, 40, -6), (12, -30, 30), (22, -30, 30), (28, 0, 10), (36, 18, 0))
a.rot("arm_l", R_("arm_l", 0), (8, 30, 0, -30), (10, 34, 0, -34), (12, -40, 0, -70), (22, -36, 0, -72), (28, 0, 0, -40), (36, *rest("arm_l")))
a.rot("claws_l", (0, 20, 0, 0), (12, -30, 0, 0), (22, -30, 0, 0), (36, 20, 0, 0))
legs_both(a, [(0, 0, 0, 0), (10, -4, 0, 4), (12, 0, 0, 10), (22, 0, 0, 10), (36, 0, 0, 0)], [(0, 0, 0, 0), (12, -16, 0, 0), (22, -16, 0, 0), (36, 0, 0, 0)])
a.rot("leg_r", (12, -16, 0, 10), (22, -16, 0, 10))
hair = [(0, 0, 0, 0), (10, 10, 0, 0), (12, 50, 0, 0)]
for t in range(13, 23):
    hair.append((t, 46 + (6 if t % 2 else -6), 0, 6 if t % 2 else -6))
hair += [(28, 6, 0, 0), (36, 0, 0, 0)]
a.hair(hair, delay=1)
a.skirt([(0, 0, 0, 0), (10, -4, 0, 0), (12, -14, 0, 16), (16, -16, 0, 20), (22, -12, 0, 16), (30, 0, 0, 2), (36, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ alphabet_barrage (80, enraged): rears up laughing 0-14, A..Z machine-gun throws 16..66 (left 16+4k, claw 18+4k), pant
a = A("alphabet_barrage", 80)
a.show("held_l", 8, 67).show("held_r", 8, 67)
arm_l = [R_("arm_l", 0), (8, 170, 0, -30), (14, 180, 0, -34)]
arm_r = [R_("arm_r", 0), (8, 170, 0, 30), (14, 180, 0, 34)]
chest = [R_("chest", 0), (8, 22, 0, 0), (14, 26, 0, 0)]
fl = [(0, 20, 0, 0), (14, 60, 0, 0)]
fing = [(0, 18, 0), (14, 50, -6)]
for t in range(16, 67, 2):
    if (t - 16) % 4 == 0:  # left releases
        arm_l += [(t, 70, 0, -16), (t + 2, 190, 0, -30)]
        fl += [(t, -20, 0, 0), (t + 1.5, 60, 0, 0)]
        chest.append((t, -10, -16, 0))
    else:                  # claw releases
        arm_r += [(t, 70, 0, 14), (t + 2, 190, 0, 30)] if t + 2 <= 66 else [(t, 70, 0, 14)]
        fing += [(t, -20, 20), (t + 1.5, 50, -6)]
        chest.append((t, -10, 16, 0))
arm_r[2:2] = [(16, 190, 0, 30)]
arm_l += [(72, 30, 0, -30), (80, *rest("arm_l"))]
arm_r += [(72, 30, 0, 40), (80, *rest("arm_r"))]
chest += [(70, -30, 0, 0), (74, -26, 0, 0), (80, *rest("chest"))]
fing += [(72, 0, 4), (80, 18, 0)]
a.rot("arm_l", *arm_l).rot("arm_r", *arm_r).rot("chest", *chest).rot("claws_l", *fl).grip(*fing)
a.rot("fore_l", R_("fore_l", 0), (8, 40, 0, 0), (66, 30, 0, 0), (72, 10, 0, 0), (80, *rest("fore_l")))
a.rot("fore_r", R_("fore_r", 0), (8, 40, 0, 0), (66, 30, 0, 0), (72, 10, 0, 0), (80, *rest("fore_r")))
a.rot("head", R_("head", 0), (6, 36, 0, 0), (9, 30, 0, 10), (12, 36, 0, -10), (14, 30, 0, 0), (16, -6, 0, 6), (40, -6, 0, -6), (66, -6, 0, 6),
      (70, -20, 0, 0), (73, -12, 0, 0), (76, -20, 0, 0), (80, *rest("head")))
a.scl("jaw", (0, 1, 1, 1), (6, 1.1, 1.8, 1), (9, 1, 1.2, 1), (12, 1.1, 1.8, 1), (16, 1.1, 1.5, 1), (66, 1.1, 1.5, 1), (72, 1, 1, 1))
a.rot("blocks", (0, 0, 0, 0), (14, 0, 0, 0), (16, 0, 0, 0), (66, 0, 0, 0), (80, 0, 0, 0))
a.rot("body", (0, 0, 0, 0), (14, 8, 0, 0), (16, -6, 0, 0), (66, -6, 0, 0), (70, -16, 0, 0), (80, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (14, 0, 0.8, 0), (16, 0, -1.0, 0), (66, 0, -1.0, 0), (70, 0, -2.2, -0.6), (80, 0, 0, 0))
legs_both(a, [(0, 0, 0, 0), (14, 0, 0, 3), (16, 0, 0, 8), (66, 0, 0, 8), (70, 20, 0, 6), (80, 0, 0, 0)],
          [(0, 0, 0, 0), (16, -16, 0, 0), (66, -16, 0, 0), (70, -40, 0, 0), (80, 0, 0, 0)])
a.rot("leg_r", (16, -20, 0, 8), (66, -20, 0, 8))
a.rot("leg_l", (16, 18, 0, -8), (66, 18, 0, -8))
hair = [(0, 0, 0, 0), (8, 14, 0, 0), (14, 18, 0, 0), (16, -10, 0, 0)]
for t in range(18, 67, 4):
    hair.append((t, -14, 0, 8 if (t // 4) % 2 else -8))
hair += [(70, -20, 0, 0), (80, 0, 0, 0)]
a.hair(hair)
a.skirt([(0, 0, 0, 0), (14, -4, 0, 0), (16, 6, 0, 8), (40, 6, 0, -8), (66, 6, 0, 8), (72, 10, 0, 4), (80, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ shard_quake (40, new): both hands raised 12, DOUBLE SLAM into the floor 14 (shard line erupts), dig, rip claw up 24, recover
a = A("shard_quake", 40)
a.rot("arm_r", R_("arm_r", 0), (6, 120, 0, 10), (12, 190, 0, -8), (13, 150, 0, -6), (14, 40, 0, -6), (20, 36, 0, -6), (22, 30, 0, 0), (24, 130, 0, 20), (27, 150, 0, 24),
      (32, 80, 0, 20), (40, *rest("arm_r")))
a.rot("arm_l", R_("arm_l", 0), (6, 120, 0, -10), (12, 190, 0, 8), (13, 150, 0, 6), (14, 40, 0, 6), (24, 40, 0, 6), (30, 20, 0, -20), (40, *rest("arm_l")))
a.rot("fore_r", R_("fore_r", 0), (12, 40, 0, 0), (14, 0, 0, 0), (22, 0, 0, 0), (24, 20, 0, 0), (40, *rest("fore_r")))
a.rot("fore_l", R_("fore_l", 0), (12, 40, 0, 0), (14, 0, 0, 0), (30, 10, 0, 0), (40, *rest("fore_l")))
a.rot("hand_r", R_("hand_r", 0), (12, -20, 0, 0), (14, 40, 0, 0), (22, 40, 0, 0), (24, -20, 0, 0), (40, *rest("hand_r")))
a.grip((0, 18, 0), (10, -20, 16), (13, -20, 16), (14, 40, 22), (18, 60, 18), (22, 70, 10), (24, -20, 24), (28, -10, 20), (40, 18, 0))
a.rot("claws_l", (0, 20, 0, 0), (12, -20, 0, 0), (14, 50, 0, 0), (24, 60, 0, 0), (40, 20, 0, 0))
a.rot("chest", R_("chest", 0), (6, 10, 0, 0), (12, 24, 0, 0), (14, -46, 0, 0), (22, -44, 0, 0), (24, 10, -20, 0), (28, 14, -24, 0), (34, 0, -6, 0), (40, *rest("chest")))
a.rot("body", (0, 0, 0, 0), (12, 10, 0, 0), (14, -26, 0, 0), (22, -24, 0, 0), (24, 0, -10, 0), (40, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (12, 0, 1.0, 0.6), (14, 0, -4.0, -1.8), (16, 0, -4.4, -1.8), (22, 0, -4.0, -1.8), (24, 0, -0.6, 0), (30, 0, -0.4, 0), (40, 0, 0, 0))
a.pos("root", (0, 0, 0, 0), (10, 0, 0.8, 0), (12, 0, 1.0, 0), (14, 0, 0, 0), (15, 0, -0.3, 0), (16, 0, 0, 0), (40, 0, 0, 0))
a.rot("head", R_("head", 0), (12, 30, 0, 0), (14, 10, 0, 0), (18, 16, 0, 10), (22, 16, 0, -10), (24, 20, -20, 0), (30, 10, 0, 14), (40, *rest("head")))
a.scl("jaw", (0, 1, 1, 1), (10, 1.1, 1.7, 1), (14, 1, 1.3, 1), (24, 1.1, 1.8, 1), (30, 1, 1, 1))
legs_both(a, [(0, 0, 0, 0), (12, 0, 0, 2), (14, 50, 0, 14), (22, 48, 0, 14), (26, 20, 0, 6), (40, 0, 0, 0)],
          [(0, 0, 0, 0), (12, 0, 0, 0), (14, -90, 0, 0), (22, -88, 0, 0), (26, -30, 0, 0), (40, 0, 0, 0)],
          [(0, 0, 0, 0), (12, -20, 0, 0), (14, 40, 0, 0), (22, 40, 0, 0), (26, 0, 0, 0)])
a.hair([(0, 0, 0, 0), (12, -16, 0, 0), (14, 44, 0, 0), (17, 30, 0, 6), (22, 20, 0, -6), (24, -20, 0, 10), (30, -6, 0, 0), (40, 0, 0, 0)])
a.skirt([(0, 0, 0, 0), (12, -8, 0, 0), (14, 30, 0, 30), (18, 24, 0, 26), (24, 4, 0, 6), (40, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ spin_shred (36, new): coil 8 (claw flung out), whirling triple spin with hits 10/16/22, dizzy wobble stop
a = A("spin_shred", 36)
a.rot("root", (0, 0, 0, 0), (8, 0, -50, 0), (10, 0, 30, 0), (16, 0, 390, 0), (22, 0, 750, 0), (27, 0, 1030, 0), (31, 0, 1074, 0), (36, 0, 1080, 0))
a.pos("root", (0, 0, 0, 0), (9, 0, 0, 0), (13, 0, 1.0, 0), (16, 0, 0.4, 0), (19, 0, 1.0, 0), (22, 0, 0.4, 0), (26, 0, 0, 0), (36, 0, 0, 0))
a.rot("arm_r", R_("arm_r", 0), (6, 0, 0, 60), (8, -10, 0, 80), (10, 0, 20, 92), (22, 0, 20, 92), (26, 10, 0, 70), (30, 30, 0, 40), (36, *rest("arm_r")))
a.rot("fore_r", R_("fore_r", 0), (8, 20, 0, 0), (10, 0, 0, 0), (24, 0, 0, 0), (36, *rest("fore_r")))
a.rot("hand_r", R_("hand_r", 0), (10, 0, -30, 0), (24, 0, -30, 0), (36, *rest("hand_r")))
a.grip((0, 18, 0), (8, -20, 22), (10, 10, 26), (24, 10, 26), (30, 20, 6), (36, 18, 0))
a.rot("arm_l", R_("arm_l", 0), (8, 30, 0, -60), (10, 0, 0, -80), (22, 0, 0, -80), (26, -10, 0, -60), (30, 30, 0, -30), (36, *rest("arm_l")))
a.rot("chest", R_("chest", 0), (6, -10, -40, 0), (8, -14, -50, 0), (10, -10, 20, 0), (22, -10, 20, 0), (26, -4, 0, 10), (30, 0, 0, -10), (33, 0, 0, 6), (36, *rest("chest")))
a.rot("body", (0, 0, 0, 0), (8, -10, -10, 0), (10, -6, 0, 0), (22, -6, 0, 0), (26, 0, 0, -8), (30, 0, 0, 8), (33, 0, 0, -4), (36, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (8, 0, -1.8, 0), (10, 0, -1.0, 0), (24, 0, -1.0, 0), (36, 0, 0, 0))
a.rot("head", R_("head", 0), (8, -6, 30, 0), (10, -4, -20, 0), (24, -4, -20, 0), (26, 10, 0, 24), (29, 10, 0, -24), (32, 6, 0, 18), (36, *rest("head")))
legs_both(a, [(0, 0, 0, 0), (8, 30, 0, 6), (10, 0, 0, 10), (22, 0, 0, 10), (26, 0, 0, 4), (36, 0, 0, 0)],
          [(0, 0, 0, 0), (8, -50, 0, 0), (10, -10, 0, 0), (36, 0, 0, 0)])
a.rot("leg_l", (12, 30, 0, -20), (14, 0, 0, -10), (18, 30, 0, -20), (20, 0, 0, -10), (24, 20, 0, -14), (28, -14, 0, -4))
a.rot("shin_l", (12, -60, 0, 0), (14, -10, 0, 0), (18, -60, 0, 0), (20, -10, 0, 0), (24, -30, 0, 0), (30, 0, 0, 0))
a.hair([(0, 0, 0, 0), (8, 6, 0, 20), (10, -20, 0, -50), (22, -20, 0, -54), (26, -6, 0, 20), (29, 0, 0, -20), (32, 0, 0, 10), (36, 0, 0, 0)], delay=1)
a.skirt([(0, 0, 0, 0), (8, 6, 0, -8), (10, 20, 0, 24), (22, 20, 0, 26), (26, 10, 0, 10), (30, 4, 0, -6), (36, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ death (40): recoil 4, claw drags her down, blocks tumble off 10-20, knees buckle 18, falls face-down 28, twitch
a = A("death", 40)
for k, (dx, d) in (("blk_a", (2.0, 0)), ("blk_b", (0.0, 3)), ("blk_c", (-2.0, 6))):
    a.pos(k, (0, 0, 0, 0), (8 + d, 0, 0, 0), (12 + d, dx, 2.0, -1.0), (16 + d, dx * 2, -8, -3), (20 + d, dx * 2.2, -9, -3.5), (40, dx * 2.2, -9, -3.5))
    a.rot(k, (0, 0, 0, 0), (8 + d, 0, 0, 0), (16 + d, 160, 40, 90), (20 + d, 180, 45, 90), (40, 180, 45, 90))
a.rot("squiggle", (0, 0, 0, 0), (6, 0, 0, 0), (14, 0, 0, 60), (40, 0, 0, 80))
a.scl("squiggle", (0, 1, 1, 1), (10, 1, 1, 1), (16, *HIDE))
a.rot("head", R_("head", 0), (4, 30, 0, -10), (10, 10, 0, 20), (18, -20, 0, 26), (28, 20, 0, 30), (34, 14, 0, 34), (40, 16, 0, 34))
a.scl("jaw", (0, 1, 1, 1), (4, 1.1, 1.9, 1), (12, 1, 1.4, 1), (28, 1, 1.2, 1))
a.rot("chest", R_("chest", 0), (4, 20, 0, 0), (10, -10, 0, 16), (18, -30, 0, 20), (28, -10, 0, 10), (40, -10, 0, 10))
a.rot("arm_r", R_("arm_r", 0), (4, 80, 0, 40), (10, 10, 0, 20), (18, 0, 0, 10), (26, 150, 0, 20), (32, 160, 0, 30), (36, 156, 0, 30), (40, 160, 0, 30))
a.rot("fore_r", R_("fore_r", 0), (4, 30, 0, 0), (10, 0, 0, 0), (40, 0, 0, 0))
a.grip((0, 18, 0), (4, -30, 26), (10, 10, 6), (28, -10, 20), (32, 20, 10), (34, -6, 14), (36, 30, 8), (40, 26, 8))
a.rot("arm_l", R_("arm_l", 0), (4, 40, 0, -40), (18, 10, 0, -20), (26, 150, 0, -30), (32, 160, 0, -40), (40, 160, 0, -40))
a.rot("claws_l", (0, 20, 0, 0), (36, 20, 0, 0), (37, 60, 0, 0), (38, 20, 0, 0))
a.pos("body", (0, 0, 0, 0), (4, 0, 0.4, 1.0), (10, 0, -1.0, 0.4), (18, 0, -5.0, 0), (24, 0, -6.0, 0), (29, 0, -0.6, 0), (40, 0, -0.6, 0))
a.rot("body", (0, 0, 0, 0), (4, 10, 0, 0), (10, -6, 0, 10), (18, -10, 0, 6), (24, -16, 0, 0), (40, -16, 0, 0))
a.rot("root", (0, 0, 0, 0), (22, 0, 0, 0), (26, -40, 0, 0), (29, -86, 0, 0), (31, -80, 0, 0), (34, -88, 0, 0), (40, -88, 0, 0))
a.pos("root", (0, 0, 0, 0), (22, 0, 0, 0), (26, 0, 0.6, -1.5), (29, 0, 2.6, -3), (31, 0, 3.0, -3), (34, 0, 2.6, -3), (40, 0, 2.6, -3))
legs_both(a, [(0, 0, 0, 0), (10, -10, 0, 4), (18, 80, 0, 6), (24, 90, 0, 6), (29, 20, 0, 4), (40, 20, 0, 4)],
          [(0, 0, 0, 0), (10, -10, 0, 0), (18, -120, 0, 0), (24, -130, 0, 0), (29, -20, 0, 0), (40, -24, 0, 0)])
a.hair([(0, 0, 0, 0), (4, -20, 0, 0), (10, 10, 0, 20), (18, 20, 0, 10), (26, -30, 0, 0), (29, 30, 0, 10), (34, 20, 0, 14), (40, 20, 0, 14)])
a.skirt([(0, 0, 0, 0), (4, -6, 0, 0), (18, 10, 0, 20), (24, 16, 0, 26), (29, -20, 0, 10), (34, -14, 0, 10), (40, -14, 0, 10)])
a.done()

os.makedirs(os.path.dirname(OUT), exist_ok=True)
m.save(OUT)
print("cubes", len(m.cubes), "anims", [x["name"] for x in m.anims], "atlas rows used", m.cy + m.rowh)
