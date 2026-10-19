"""Green Circle (FPE Green) - generates assets/fpe/bbmodels/green_circle.bbmodel.
Reference: docs/ref/confirmed/green_circle.png - HUGE spiky black hair (cat-ear spikes on top, mane down to the knees with
sideways spikes), green-tinted safety goggles pushed up on the forehead, black scarf/mask at the neck, wide sharp-toothed grin,
white lab coat over white shorts, green tie, black gloves, tall black boots with pointed cuffs and heels,
a big green-liquid sprayer/canister gun in her left hand with a grey hose hanging in a loop. 292 cm tall (~2.9 blocks w/ hair).
Blockbench space: Y up, ground 0, faces -Z. Character's RIGHT = +X.
Rotation signs (file values): arm/leg rx>0 = swing forward, torso/head rx>0 = lean back / look up,
ry>0 = turn to the character's left, rz>0 = hanging part swings toward +X (character's right).
Melee-focused moveset + crowd control (grin_bite hold, hose_lasso pull/choke, specimen_pin, glove_snatch disarm); every key tick matches entity/characters/GreenCircle.java.
Run: python3 tools/bbgen/chars/green_circle.py
"""
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from bbgen import Model, mix  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "../../../src/main/resources/assets/fpe/bbmodels/green_circle.bbmodel")

# ------------------------------------------------------------------ palette
HAIR, HAIR_HI, HAIR_D = 0x1B1A22, 0x3A3846, 0x0B0A10
SKIN, SKIN_D = 0xF3F2EF, 0xC9C9CF
COAT, COAT_D, COAT_L = 0xEDEFF1, 0xAEB7C2, 0xFFFFFF
SHORT, SHORT_D = 0xF5F4F0, 0xB9BEC6
BLK, BLK_L, BLK_D = 0x1A1920, 0x34333E, 0x0A0A0E
GRN, GRN_D, GRN_L, GRN_DD = 0x8FCF3E, 0x5C8F22, 0xCBF28A, 0x34541A
LENS, LENS_L, LENS_D = 0x9DD86A, 0xE2FFC0, 0x5E9A3A
STEEL, STEEL_D, STEEL_L = 0xB9C2CC, 0x6F7884, 0xE4E9EE
GUN, GUN_D = 0xF2F3F4, 0xA3ACB7
LIQ, LIQ_L, LIQ_D = 0x86D13A, 0xD9FF9A, 0x4E8A1E
HOSE, HOSE_D = 0x9BA6B2, 0x5E6772
MOUTH, TEETH, LINE = 0x24121A, 0xFFFFFF, 0x121016
TOX, TOX_L = 0x8CFF3A, 0xE8FFB0

m = Model("green_circle", S=8, atlas=2048)
R = m.rng


# ------------------------------------------------------------------ painters
def all_faces(fn, skip=()):
    return {k: fn for k in ("north", "south", "east", "west", "up", "down") if k not in skip}


def combo(*fns):
    def f(F):
        for fn in fns: fn(F)
    return f


def strands(base=HAIR, hi=HAIR_HI, dark=HAIR_D):
    def f(F):
        cols = [R.random() for _ in range(F.w)]
        for x in range(F.w):
            c = hi if cols[x] > 0.82 else dark if cols[x] < 0.25 else base
            for y in range(F.h):
                cc = mix(c, dark, 0.45 * abs(y / max(1, F.h - 1) - 0.3))
                if (x + y // 7) % 5 == 0 and R.random() < 0.35: cc = mix(cc, hi, 0.55)
                F.px(x, y, cc)
    return f


HS = strands()


def folds(base, dark, light, n=3, hem=True):
    def f(F):
        for i in range(n):
            x = int((i + 0.5) * F.w / n) + R.randint(-1, 1)
            for y in range(F.h):
                k = y / max(1, F.h - 1)
                F.px(x, y, mix(base, dark, 0.25 + 0.35 * k))
                F.px(x + 1, y, mix(base, light, 0.3 * k))
        if hem: F.rect(0, F.h - 2, F.w, 2, mix(base, dark, 0.45))
    return f


def outline(c):
    return lambda F: (F.rect(0, 0, F.w, 1, c), F.rect(0, F.h - 1, F.w, 1, c), F.rect(0, 0, 1, F.h, c), F.rect(F.w - 1, 0, 1, F.h, c))


def leather(F):
    for y in range(F.h):
        for x in range(F.w):
            c = mix(BLK_L, BLK, min(1, y / max(1, F.h - 1) * 1.3))
            if x < 2 or x >= F.w - 2: c = mix(c, BLK_D, 0.5)
            F.px(x, y, c)
    F.rect(F.w // 3, 2, 2, max(1, F.h - 6), mix(BLK_L, 0x8890A0, 0.35))  # gloss streak


def face_front(F):
    W, H = F.w, F.h  # ~61 x 64
    for y in range(H):
        for x in range(W):
            F.px(x, y, mix(SKIN, SKIN_D, max(0, (26 - y) / 26) * 0.75))
    # sharp narrow grinning eyes, slanted, green glint
    for s in (-1, 1):
        cx = W / 2 + s * 14
        pts = [(cx - 8 * s, 25), (cx + 9 * s, 21), (cx + 7 * s, 27), (cx - 6 * s, 29)]
        F.poly(pts, LINE)
        F.disc(cx + 1 * s, 25.5, 1.6, TOX, glow=True)
        F.line(cx + 9 * s, 21, cx + 12 * s, 18, LINE, 1.4)  # lash flick
        F.line(cx - 9 * s, 20, cx + 6 * s, 15, mix(LINE, SKIN_D, 0.2), 1.3)  # brow
    # huge wide grin full of sharp teeth
    cx = W / 2
    for x in range(5, W - 5):
        u_ = (x + .5 - cx) / (cx - 5)
        top = 36 - 5 * u_ * u_
        bot = 57 - 18 * u_ * u_
        if bot <= top + 0.5: continue
        for y in range(int(top), int(bot) + 1):
            F.px(x, y, MOUTH)
        F.px(x, int(top) - 1, LINE); F.px(x, int(bot) + 1, LINE)
    for i in range(9):  # upper fangs (triangles pointing down) + lower fangs (pointing up)
        x0 = 9 + i * 5
        u_ = (x0 + 2.5 - cx) / (cx - 5)
        top = 36 - 5 * u_ * u_
        bot = 57 - 18 * u_ * u_
        ln = max(2, (bot - top) * 0.45)
        F.poly([(x0, top), (x0 + 5, top), (x0 + 2.5, top + ln)], TEETH)
        if i > 0 and i < 8:
            F.poly([(x0 - 2.5, bot + 0.5), (x0 + 2.5, bot + 0.5), (x0, bot - ln * 0.8)], TEETH)
    F.rect(4, 33, 3, 1, LINE); F.rect(W - 7, 33, 3, 1, LINE)  # grin dimples


def coat_front(F):
    W, H = F.w, F.h
    folds(COAT, COAT_D, COAT_L, 2, hem=False)(F)
    g0, g1 = W // 2 - 7, W // 2 + 7  # open front: shirt + green tie + black scarf triangle
    for y in range(H):
        for x in range(g0, g1):
            F.px(x, y, mix(SHORT, SHORT_D, 0.15 + 0.2 * y / H))
    F.rect(g0 - 1, 0, 2, H, COAT_D); F.rect(g1 - 1, 0, 2, H, COAT_D)
    F.poly([(W / 2 - 3, 6), (W / 2 + 3, 6), (W / 2 + 4, 40), (W / 2, 46), (W / 2 - 4, 40)], GRN)  # tie
    F.rect(W / 2 - 1, 8, 1, 34, GRN_D)
    F.poly([(g0, 0), (g1, 0), (W / 2, 22)], BLK)  # scarf tip over the tie knot
    for b in (50, 60):
        F.disc(g0 - 4, b, 1.2, COAT_D)


def gun_side(F):
    F.rect(0, 0, F.w, F.h, GUN)
    outline(GUN_D)(F)
    # liquid window with level, bubbles and gauge marks
    wx, wy, ww, wh = 3, 4, F.w - 6, int(F.h * 0.55)
    F.rect(wx - 1, wy - 1, ww + 2, wh + 2, STEEL_D)
    for y in range(wh):
        for x in range(ww):
            c = mix(LIQ_L, LIQ_D, y / max(1, wh - 1)) if y > wh * 0.2 else mix(LIQ, 0xFFFFFF, 0.5)
            F.px(wx + x, wy + y, c, glow=y > wh * 0.2)
    for _ in range(6):
        F.disc(wx + R.uniform(2, ww - 2), wy + R.uniform(wh * 0.35, wh - 2), R.uniform(0.8, 1.6), LIQ_L, glow=True)
    for y in range(wy, wy + wh, 5):
        F.rect(wx, y, 3, 1, LINE)
    F.rect(3, wy + wh + 4, F.w - 6, 2, GUN_D)
    F.rect(3, wy + wh + 8, (F.w - 6) // 2, 2, GUN_D)


def glow_fill(c1, c2):
    def f(F):
        for y in range(F.h):
            for x in range(F.w):
                c = mix(c1, c2, y / max(1, F.h - 1))
                if R.random() < 0.3: c = mix(c, 0xFFFFFF, 0.4)
                F.px(x, y, c, glow=True)
    return f


GF = lambda a, b: (lambda fs: [glow_fill(a, b)(f) for f in fs.values()])


def lens(F):
    for y in range(F.h):
        for x in range(F.w):
            F.px(x, y, mix(LENS_L, LENS, min(1, (x * 0.6 + y) / max(1, F.h))), glow=True)
    F.rect(2, 1, 3, 1, 0xFFFFFF, glow=True); F.rect(F.w - 8, F.h - 3, 5, 1, mix(LENS_L, 0xFFFFFF, 0.5), glow=True)
    outline(GRN_D)(F)


# ------------------------------------------------------------------ skeleton
m.group("root", (0, 0, 0))
m.group("body", (0, 20, 0), parent="root")
m.group("chest", (0, 21.5, 0), parent="body")
m.group("coat_b", (0, 21.5, 2.2), parent="body")
m.group("coat_b2", (0, 17.0, 2.6), parent="coat_b")
m.group("coat_fr", (2.2, 21.5, -2.2), parent="body")
m.group("coat_fl", (-2.2, 21.5, -2.2), parent="body")
m.group("scarf", (0, 30.5, -2.4), parent="chest")
m.group("head", (0, 31.4, 0), parent="chest")
m.group("goggles", (0, 37.8, 0), parent="head")
m.group("bangs", (0, 39.6, -3.6), parent="head")
m.group("ear_r", (2.6, 40.6, 0.6), parent="head")
m.group("ear_l", (-2.6, 40.6, 0.6), parent="head")
m.group("hair_b", (0, 39.0, 3.4), parent="head")
m.group("hair_b2", (0, 28.0, 4.6), parent="hair_b")
m.group("hair_b3", (0, 17.0, 5.6), parent="hair_b2")
m.group("hair_r", (3.9, 37.5, -1.0), parent="head")
m.group("hair_r2", (4.6, 29.5, -1.0), parent="hair_r")
m.group("hair_l", (-3.9, 37.5, -1.0), parent="head")
m.group("hair_l2", (-4.6, 29.5, -1.0), parent="hair_l")
for s, k in ((1, "r"), (-1, "l")):
    m.group("arm_" + k, (4.3 * s, 29.6, 0), parent="chest")
    m.group("fore_" + k, (4.5 * s, 25.4, 0), parent="arm_" + k)
    m.group("hand_" + k, (4.5 * s, 21.4, 0), parent="fore_" + k)
    m.group("leg_" + k, (1.6 * s, 18.6, 0), parent="root")
    m.group("shin_" + k, (1.6 * s, 11.8, 0), parent="leg_" + k)
    m.group("foot_" + k, (1.6 * s, 1.8, 0.2), parent="shin_" + k)
m.group("gun", (-4.5, 19.6, 0), parent="hand_l")
m.group("spray", (-4.5, 3.0, 0), parent="gun")
m.group("hose1", (-4.5, 24.5, 0.9), parent="gun")
m.group("hose2", (-4.5, 21.0, 0.9), parent="hose1")
m.group("hose3", (-4.5, 17.5, 0.9), parent="hose2")
m.group("hose4", (-4.5, 14.0, 0.9), parent="hose3")
m.group("tox", (0, 0.3, 0), parent="root")
m.group("lash", (4.5, 17.8, -0.2), parent="hand_r")
m.group("lash2", (4.5, 10.6, -0.2), parent="lash")
m.group("lash3", (4.5, 3.4, -0.2), parent="lash2")

# ------------------------------------------------------------------ legs: pale legs, tall black boots w/ pointed cuffs + spike heels
for s, k in ((1, "r"), (-1, "l")):
    x = 1.6 * s
    m.cube("thigh_" + k, "leg_" + k, (x - 1.15, 11.4, -1.15), (x + 1.15, 18.8, 1.15), SKIN, color2=SKIN_D, grad=True)
    m.cube("knee_" + k, "shin_" + k, (x - 1.1, 11.0, -1.1), (x + 1.1, 12.6, 1.1), SKIN_D)
    m.cube("boot_" + k, "shin_" + k, (x - 1.3, 1.6, -1.35), (x + 1.3, 11.6, 1.35), BLK, faces=all_faces(leather, ("up", "down")))
    m.cube("bcuff_" + k, "shin_" + k, (x - 1.75, 10.4, -1.8), (x + 1.75, 12.6, 1.8), BLK_L, color2=BLK, grad=True)
    m.cube("bflap_" + k, "shin_" + k, (x - 1.2, 11.0, -2.3), (x + 1.2, 14.4, -1.7), BLK, origin=(x, 11.5, -2.0), rot=(-14, 0, 0),
           faces={"north": lambda F: F.poly([(0, F.h), (F.w, F.h), (F.w, F.h * 0.4), (F.w / 2, 0), (0, F.h * 0.4)], BLK_L)})
    m.cube("bflapo_" + k, "shin_" + k, (x + 1.5 * s - 0.3, 10.6, -1.0), (x + 1.5 * s + 0.3, 14.0, 1.0), BLK, origin=(x + 1.5 * s, 11.0, 0), rot=(0, 0, 18 * s))
    m.cube("foot_" + k, "foot_" + k, (x - 1.3, 0.4, -3.4), (x + 1.3, 2.4, 1.4), BLK, color2=BLK_D, grad=True)
    m.cube("toe_" + k, "foot_" + k, (x - 0.8, 0.4, -5.2), (x + 0.8, 1.6, -3.2), BLK_L, color2=BLK, grad=True, origin=(x, 0.6, -3.4), rot=(-8, 0, 0))
    m.cube("toetip_" + k, "foot_" + k, (x - 0.35, 0.3, -6.4), (x + 0.35, 1.0, -5.0), BLK, origin=(x, 0.6, -5.0), rot=(-12, 0, 0))
    m.cube("heel_" + k, "foot_" + k, (x - 0.4, 0.0, 1.0), (x + 0.4, 2.0, 3.4), BLK, origin=(x, 1.0, 1.2), rot=(20, 0, 0))
    m.cube("sole_" + k, "foot_" + k, (x - 1.35, 0.0, -3.5), (x + 1.35, 0.45, 1.45), BLK_D)

# ------------------------------------------------------------------ hips: white shorts + lab-coat tails
m.cube("shorts", "body", (-3.1, 16.6, -1.9), (3.1, 21.0, 1.9), SHORT, color2=SHORT_D, grad=True,
       faces={"north": lambda F: (F.rect(F.w // 2, 8, 1, F.h - 8, SHORT_D), F.rect(0, 0, F.w, 3, SHORT_D))})
for s, k in ((1, "r"), (-1, "l")):
    m.cube("shleg_" + k, "body", (1.6 * s - 1.5, 15.6, -1.6), (1.6 * s + 1.5, 17.4, 1.6), SHORT, color2=SHORT_D, grad=True,
           faces={"north": lambda F: F.rect(0, F.h - 2, F.w, 2, SHORT_D)})
m.cube("belt", "body", (-3.2, 20.4, -2.0), (3.2, 21.2, 2.0), STEEL_D)
m.cube("cb_up", "coat_b", (-3.5, 16.8, 2.0), (3.5, 21.8, 2.7), COAT, color2=COAT_D, grad=True, faces={"south": folds(COAT, COAT_D, COAT_L, 3, False)})
m.cube("cb_lo", "coat_b2", (-3.7, 12.8, 2.3), (3.7, 17.2, 3.0), COAT, color2=COAT_D, grad=True,
       faces={"south": combo(folds(COAT, COAT_D, COAT_L, 3), lambda F: F.rect(F.w // 2, 0, 1, F.h, COAT_D))})
for s, k in ((1, "r"), (-1, "l")):
    m.cube("cf_" + k, "coat_f" + k, (1.0 * s if s > 0 else -3.6, 13.0, -2.5), (3.6 if s > 0 else -1.0, 21.6, -1.9), COAT, color2=COAT_D, grad=True,
           origin=(2.2 * s, 21.5, -2.2), rot=(4, 0, 6 * s),
           faces={"north": combo(folds(COAT, COAT_D, COAT_L, 2), lambda F: F.rect(3, 26, F.w - 6, 1, COAT_D), lambda F: F.rect(3, 26, 1, 14, COAT_D),
                                 lambda F: F.rect(F.w - 4, 26, 1, 14, COAT_D))})
    m.cube("cs_" + k, "coat_f" + k, (3.4 * s - 0.3, 13.2, -1.9), (3.4 * s + 0.3, 21.6, 2.3), COAT, color2=COAT_D, grad=True,
           origin=(3.4 * s, 21.5, 0.2), rot=(0, 0, 7 * s), faces={"east": folds(COAT, COAT_D, COAT_L, 2), "west": folds(COAT, COAT_D, COAT_L, 2)})

# ------------------------------------------------------------------ torso: coat, collar, scarf, tie, hose strap
m.cube("torso", "chest", (-3.0, 21.0, -1.8), (3.0, 30.2, 1.8), COAT, color2=COAT_D, grad=True,
       faces={"north": coat_front, "south": folds(COAT, COAT_D, COAT_L, 3, False)})
for s, k in ((1, "r"), (-1, "l")):
    x0, x1 = (1.0, 3.1) if s > 0 else (-3.1, -1.0)
    m.cube("lapel_" + k, "chest", (x0, 23.0, -2.3), (x1, 30.0, -1.8), COAT_L, color2=COAT, grad=True,
           origin=((x0 + x1) / 2, 29.6, -2), rot=(0, 0, -8 * s), faces={"north": lambda F: F.rect(0, 0, 1, F.h, COAT_D)})
    m.cube("collar_" + k, "chest", (0.8 * s if s > 0 else -3.0, 29.0, -2.3), (3.0 if s > 0 else -0.8, 31.6, 2.0), COAT_L, color2=COAT, grad=True,
           origin=(1.9 * s, 30.2, 0), rot=(0, 0, 16 * s))
m.cube("neck", "chest", (-1.0, 29.6, -0.9), (1.0, 31.8, 0.9), SKIN_D)
m.cube("scarf_ring", "chest", (-2.2, 29.6, -2.2), (2.2, 32.4, 2.2), BLK, faces=all_faces(lambda F: F.rect(0, F.h - 3, F.w, 1, BLK_L)))
m.cube("scarf_knot", "scarf", (-1.0, 28.6, -2.8), (1.0, 30.6, -2.1), BLK_L)
m.cube("scarf_tail", "scarf", (-1.3, 25.2, -2.7), (1.3, 29.2, -2.3), BLK, origin=(0, 29, -2.4), rot=(-4, 0, 10),
       faces={"north": lambda F: F.poly([(0, 0), (F.w, 0), (F.w * 0.5, F.h)], BLK_L)})
m.cube("tie", "chest", (-0.6, 23.0, -2.05), (0.6, 28.6, -1.85), GRN, faces={"north": lambda F: F.rect(F.w // 2, 0, 1, F.h, GRN_D)})
m.cube("strap", "chest", (-0.5, 21.0, -2.15), (0.5, 31.0, -1.95), HOSE, origin=(0, 26, -2), rot=(0, 0, 38))
m.cube("strap_b", "chest", (-0.5, 21.0, 1.95), (0.5, 31.0, 2.15), HOSE_D, origin=(0, 26, 2), rot=(0, 0, -38))
m.cube("tank", "chest", (1.0, 20.8, 1.9), (3.2, 26.0, 3.6), GUN, color2=GUN_D, grad=True,
       faces={"south": lambda F: (F.rect(3, 6, F.w - 6, F.h - 14, LIQ, glow=True), outline(GUN_D)(F))})
m.cube("tank_cap", "chest", (1.4, 26.0, 2.2), (2.8, 26.8, 3.3), STEEL_D)
m.cube("pen", "chest", (-2.6, 26.4, -2.1), (-2.2, 28.6, -1.85), GRN_D)

# ------------------------------------------------------------------ head: big pale face + toothy grin, goggles, spiky hair
m.cube("skull", "head", (-3.8, 31.6, -3.6), (3.8, 39.6, 3.6), SKIN, faces={"north": face_front, "up": lambda F: F.rect(0, 0, F.w, F.h, HAIR_D)})
m.cube("mask_l", "head", (-3.9, 31.4, -3.7), (-2.4, 33.6, 3.7), BLK)  # black mask/scarf wrapping the jaw sides
m.cube("mask_r", "head", (2.4, 31.4, -3.7), (3.9, 33.6, 3.7), BLK)
m.cube("mask_b", "head", (-3.9, 31.4, 1.0), (3.9, 33.6, 3.7), BLK)
m.cube("hair_cap", "head", (-4.2, 38.4, -3.9), (4.2, 41.0, 4.0), HAIR, faces=all_faces(HS))
m.cube("hair_top", "head", (-3.6, 40.8, -3.2), (3.6, 42.0, 3.6), HAIR, faces=all_faces(HS))
for i, (x, ln, rz) in enumerate([(-3.4, 4.2, 20), (-2.1, 2.6, 10), (-0.8, 3.4, -4), (0.6, 2.2, 12), (1.9, 3.0, -10), (3.3, 4.6, -22)]):
    m.cube(f"bang{i}", "bangs", (x - 0.8, 39.8 - ln, -4.25), (x + 0.8, 40.0, -3.75), HAIR if i % 2 else HAIR_D,
           origin=(x, 39.8, -4.0), rot=(6, 0, rz), faces=all_faces(HS))
for s, k in ((1, "r"), (-1, "l")):  # two big cat-ear-like spikes + a crown of smaller ones
    ex = 2.6 * s
    m.cube("earA_" + k, "ear_" + k, (ex - 1.3, 40.4, -0.6), (ex + 1.3, 44.0, 1.8), HAIR, origin=(ex, 40.6, 0.6), rot=(-6, 0, -16 * s), faces=all_faces(HS))
    m.cube("earB_" + k, "ear_" + k, (ex - 0.8, 43.4, -0.2), (ex + 0.8, 46.2, 1.4), HAIR_D, origin=(ex, 43.6, 0.6), rot=(-10, 0, -26 * s), faces=all_faces(HS))
    m.cube("earC_" + k, "ear_" + k, (ex - 0.35, 45.6, 0.3), (ex + 0.35, 47.6, 0.9), HAIR, origin=(ex, 45.8, 0.6), rot=(-10, 0, -36 * s))
for i in range(5):
    x = (i - 2) * 1.5
    m.cube(f"crown{i}", "head", (x - 0.6, 41.2, 0.6), (x + 0.6, 44.0 - abs(i - 2) * 0.5, 2.6), HAIR_D if i % 2 else HAIR,
           origin=(x, 41.4, 1.6), rot=(-40, 0, (i - 2) * 14), faces=all_faces(HS))
# back mane, 3 hanging segments getting wider, with jagged spikes
m.cube("hb1", "hair_b", (-4.6, 27.6, 2.6), (4.6, 40.0, 5.2), HAIR, faces=all_faces(HS))
m.cube("hb2", "hair_b2", (-5.6, 16.6, 3.4), (5.6, 28.4, 6.0), HAIR, faces=all_faces(HS))
m.cube("hb3", "hair_b3", (-5.0, 11.0, 4.4), (5.0, 17.2, 6.6), HAIR_D, faces=all_faces(HS))
for i in range(7):
    x = -4.4 + i * 1.47
    ln = 3.0 + (i % 3) * 1.6 + R.uniform(0, 1.2)
    m.cube(f"hb_tip{i}", "hair_b3", (x - 0.7, 11.2 - ln, 4.8), (x + 0.7, 11.6, 6.2), HAIR if i % 2 else HAIR_D,
           origin=(x, 11.4, 5.5), rot=(-12, 0, (i - 3) * 10), faces=all_faces(HS))
for side, kk in ((1, "r"), (-1, "l")):  # sideways spikes jutting from the mane (zig-zag silhouette)
    for j, (y, ln, ang, seg) in enumerate([(35.0, 4.0, 60, "hair_b"), (30.0, 5.0, 70, "hair_b"), (25.0, 6.0, 64, "hair_b2"),
                                            (20.5, 7.0, 74, "hair_b2"), (15.5, 5.5, 62, "hair_b3")]):
        bx = (4.2 if seg == "hair_b" else 5.2 if seg == "hair_b2" else 4.6) * side
        m.cube(f"hs_spk{j}_" + kk, seg, (bx - 0.8, y - ln, 3.6 + j * 0.3), (bx + 0.8, y, 5.2 + j * 0.3), HAIR_D if j % 2 else HAIR,
               origin=(bx, y - 0.4, 4.4), rot=(-8, 0, ang * side), faces=all_faces(HS))
for i in range(4):  # upward flicks on the back of the head
    x = (i - 1.5) * 2.4
    m.cube(f"hb_up{i}", "hair_b", (x - 0.7, 38.0, 4.4), (x + 0.7, 42.6, 5.6), HAIR, origin=(x, 38.5, 5.0), rot=(-38, 0, (i - 1.5) * 20), faces=all_faces(HS))
for s, k in ((1, "r"), (-1, "l")):  # long locks framing the face, in front of the shoulders
    m.cube("hs_main_" + k, "hair_" + k, (3.9 * s - 0.9, 29.4, -2.4), (3.9 * s + 0.9, 38.0, 2.6), HAIR, faces=all_faces(HS))
    m.cube("hs_lo_" + k, "hair_" + k + "2", (4.6 * s - 0.8, 22.0, -2.0), (4.6 * s + 0.8, 29.8, 0.4), HAIR_D, faces=all_faces(HS))
    m.cube("hs_tip_" + k, "hair_" + k + "2", (4.6 * s - 0.5, 18.8, -1.6), (4.6 * s + 0.5, 22.4, -0.2), HAIR, origin=(4.6 * s, 22.2, -0.9), rot=(0, 0, 14 * s))
    for i in range(3):
        y = 36.0 - i * 2.6
        m.cube(f"hs_flick{i}_" + k, "hair_" + k, (4.6 * s - 0.45, y - 3.2, -1.4 + i * 1.2), (4.6 * s + 0.45, y, -0.4 + i * 1.2), HAIR_D,
               origin=(4.6 * s, y, i * 1.2 - 0.9), rot=(0, 0, (50 + i * 10) * s))
# goggles: big wraparound safety visor pushed up on the forehead
m.cube("gog_strap", "goggles", (-4.3, 37.4, -3.95), (4.3, 38.4, 4.15), BLK_L)
m.cube("gog_frame", "goggles", (-4.0, 36.6, -4.8), (4.0, 39.6, -3.7), GRN_D, origin=(0, 38.0, -4.2), rot=(-14, 0, 0))
m.cube("gog_lens", "goggles", (-3.7, 36.9, -5.05), (3.7, 39.3, -4.6), LENS, origin=(0, 38.0, -4.2), rot=(-14, 0, 0), glow=True, faces={"north": lens})
for s, k in ((1, "r"), (-1, "l")):
    m.cube("gog_side_" + k, "goggles", (3.6 * s - 0.5, 36.8, -4.6), (3.6 * s + 0.5, 39.4, -2.8), GRN_D, origin=(3.6 * s, 38, -3.6), rot=(-10, 0, 0))
m.cube("gog_vent", "goggles", (-0.6, 39.3, -4.9), (0.6, 39.9, -4.0), GRN_DD, origin=(0, 38.0, -4.2), rot=(-14, 0, 0))

# ------------------------------------------------------------------ arms: lab-coat sleeves, cuffs, black gloves
for s, k in ((1, "r"), (-1, "l")):
    x = 4.4 * s
    m.cube("shoulder_" + k, "arm_" + k, (x - 1.45, 27.6, -1.5), (x + 1.45, 30.6, 1.5), COAT, color2=COAT_D, grad=True, origin=(x, 29.6, 0), rot=(0, 0, 10 * s))
    m.cube("sleeve_" + k, "arm_" + k, (x - 1.2, 25.0, -1.25), (x + 1.2, 28.6, 1.25), COAT, color2=COAT_D, grad=True, faces={"north": folds(COAT, COAT_D, COAT_L, 2, False)})
    x = 4.5 * s
    m.cube("forearm_" + k, "fore_" + k, (x - 1.25, 22.0, -1.3), (x + 1.25, 25.8, 1.3), COAT, color2=COAT_D, grad=True, faces={"north": folds(COAT, COAT_D, COAT_L, 2, False)})
    m.cube("cuff_" + k, "fore_" + k, (x - 1.5, 21.2, -1.55), (x + 1.5, 22.6, 1.55), COAT_L, color2=COAT_D, grad=True,
           faces={"north": lambda F: F.rect(0, 0, F.w, 1, COAT_D)})
    m.cube("palm_" + k, "hand_" + k, (x - 1.15, 18.4, -1.1), (x + 1.15, 21.6, 1.1), BLK, faces=all_faces(leather, ("up",)))
    for i in range(3):  # knuckle ridges
        fz = -0.8 + i * 0.75
        m.cube(f"knuck{i}_" + k, "hand_" + k, (x - 1.3, 17.2, fz - 0.3), (x + 1.3, 17.8, fz + 0.3), BLK)
    m.cube("fist_" + k, "hand_" + k, (x - 1.25, 17.4, -1.25), (x + 1.25, 18.6, 1.0), BLK_L, color2=BLK, grad=True)
    m.cube("thumb_" + k, "hand_" + k, (x - 0.5, 18.0, -1.7), (x + 0.5, 20.0, -0.9), BLK, origin=(x, 19.6, -1.2), rot=(-14, 0, 0))

# ------------------------------------------------------------------ sprayer gun (built along -Y = along the forearm), hose loop
G = -4.5
m.cube("g_body", "gun", (G - 1.7, 8.4, -1.5), (G + 1.7, 22.0, 1.5), GUN, faces={"east": gun_side, "west": gun_side, "north": outline(GUN_D), "south": outline(GUN_D)})
m.cube("g_top", "gun", (G - 1.2, 8.8, -2.2), (G + 1.2, 21.4, -1.5), GUN_D, faces={"north": lambda F: [F.rect(1, y, F.w - 2, 1, STEEL_D) for y in range(3, F.h - 3, 6)]})
m.cube("g_cap", "gun", (G - 1.9, 21.6, -1.7), (G + 1.9, 23.2, 1.7), STEEL, color2=STEEL_D, grad=True)
m.cube("g_rear", "gun", (G - 1.0, 23.0, -1.0), (G + 1.0, 24.8, 1.0), STEEL_D)
m.cube("g_grip", "gun", (G - 0.8, 17.6, 1.4), (G + 0.8, 20.8, 3.2), BLK_L, origin=(G, 19.6, 1.5), rot=(-15, 0, 0))
m.cube("g_trig", "gun", (G - 0.3, 16.6, 1.4), (G + 0.3, 17.8, 2.4), STEEL_D)
m.cube("g_neck", "gun", (G - 1.1, 6.6, -1.1), (G + 1.1, 8.6, 1.1), STEEL, color2=STEEL_D, grad=True)
m.cube("g_barrel", "gun", (G - 0.55, 1.6, -0.55), (G + 0.55, 6.8, 0.55), STEEL_L, color2=STEEL, grad=True)
m.cube("g_ring", "gun", (G - 0.8, 4.0, -0.8), (G + 0.8, 4.6, 0.8), STEEL_D)
m.cube("g_paddle", "gun", (G - 1.5, -0.6, -0.4), (G + 1.5, 1.8, 0.4), STEEL, color2=STEEL_D, grad=True,
       faces={"east": outline(STEEL_D), "west": outline(STEEL_D), "north": lambda F: F.rect(F.w // 2 - 1, 0, 2, F.h, STEEL_D)})
m.cube("g_tip", "gun", (G - 0.35, -1.4, -0.35), (G + 0.35, -0.5, 0.35), LIQ, glow=True)
m.cube("g_drip", "gun", (G - 0.2, -2.4, -0.2), (G + 0.2, -1.4, 0.2), LIQ_L, glow=True)
for i, hb in enumerate(["hose1", "hose2", "hose3", "hose4"]):
    y0 = 24.5 - i * 3.5
    m.cube("hose_" + str(i), hb, (G - 0.45, y0 - 3.8, 0.45), (G + 0.45, y0 + 0.2, 1.35), HOSE if i % 2 else HOSE_D,
           faces=all_faces(lambda F: [F.rect(0, y, F.w, 1, HOSE_D) for y in range(1, F.h, 4)]))
m.cube("hose_end", "hose4", (G - 0.7, 9.6, 0.2), (G + 0.7, 10.8, 1.6), STEEL_D)
# long hose length pulled out as a whip (hose_whip only), held in the right glove
for i, (hb, y0) in enumerate((("lash", 17.8), ("lash2", 10.6), ("lash3", 3.4))):
    m.cube("lash_" + str(i), hb, (4.1, y0 - 7.4, -0.6), (4.9, y0 + 0.2, 0.2), HOSE if i % 2 else HOSE_D,
           faces=all_faces(lambda F: [F.rect(0, y, F.w, 1, HOSE_D) for y in range(1, F.h, 4)]))
m.cube("lash_tip", "lash3", (3.9, -4.6, -0.8), (5.1, -3.4, 0.4), STEEL_D)
# spray cone (acid) - shown only while spraying
for i in range(5):
    w = 0.8 + i * 0.75
    y0 = 2.0 - i * 2.2
    m.cube(f"spray{i}", "spray", (G - w, y0 - 2.4, -w), (G + w, y0, w), TOX if i % 2 else TOX_L, glow=True, origin=(G, y0, 0), rot=(0, 45 * (i % 2), 0),
           paint=GF(TOX_L, TOX))
# ground acid puddle (zone moves)
m.cube("tox_a", "tox", (-5, 0.05, -14), (5, 0.35, -4), TOX, glow=True, paint=GF(TOX, LIQ_D))
m.cube("tox_b", "tox", (-3.5, 0.1, -16), (3.5, 0.45, -2), TOX_L, glow=True, origin=(0, 0.2, -9), rot=(0, 45, 0), paint=GF(TOX_L, TOX))


# ================================================================== animation
PROPS = ["spray", "tox", "lash"]
HIDE = (.001, .001, .001)

REST = {
    "arm_r": (6, 0, 18), "fore_r": (40, 0, 0), "hand_r": (0, 0, -10),
    "arm_l": (10, 0, -34), "fore_l": (56, 0, 0), "hand_l": (0, 0, 0), "gun": (50, 0, -32),
    "hose1": (-150, 0, 0), "hose2": (40, 0, 0), "hose3": (70, 0, 0), "hose4": (50, 0, 0),
    "head": (0, 0, 4), "scarf": (0, 0, 0), "hair_r": (0, 0, 6), "hair_l": (0, 0, -6), "goggles": (0, 0, 0),
}


def rest(b):
    return REST.get(b, (0, 0, 0))


def R_(b, t):
    return (t, *rest(b))


class A:
    def __init__(self, name, ticks, loop=False):
        self.name, self.ticks, self.loop, self.tr = name, ticks, loop, {}

    def k(self, bone, ch, keys):
        self.tr.setdefault(bone, {}).setdefault(ch, []).extend(keys)
        return self

    def rot(self, bone, *keys): return self.k(bone, "rotation", keys)
    def pos(self, bone, *keys): return self.k(bone, "position", keys)
    def scl(self, bone, *keys): return self.k(bone, "scale", keys)

    def r(self, bone, *keys):
        """rotation keys framed by the rest pose at 0 and at the end"""
        ks = list(keys)
        if ks[0][0] > 0: ks.insert(0, R_(bone, 0))
        if ks[-1][0] < self.ticks: ks.append(R_(bone, self.ticks))
        return self.rot(bone, *ks)

    def show(self, bone, t0, t1, pulse=True):
        keys = [(0, *HIDE)] if t0 > 0 else []
        if t0 > 0: keys.append((t0 - 1, *HIDE))
        keys += [(t0, 1, 1, 1)]
        if pulse:
            tt = t0 + 2
            while tt < t1 - 1:
                keys += [(tt, 1.2, 1.1, 1.2), (tt + 2, 0.95, 1, 0.95)]
                tt += 4
        if t1 < self.ticks: keys += [(t1, 1, 1, 1), (t1 + 1.5, *HIDE)]
        return self.scl(bone, *keys)

    def drape(self, chain, keys, delay=2, gain=0.8, base=None):
        g = 1.0
        for i, b in enumerate(chain):
            seen, out = set(), []
            bx, by, bz = rest(b)
            for (t, x, y, z) in keys:
                tt = min(self.ticks, t + delay * i)
                if tt in seen: continue
                seen.add(tt); out.append((tt, bx + x * g, by + y * g, bz + z * g))
            self.rot(b, *out)
            g *= gain
        return self

    def hair(self, keys, delay=2):
        """x>0 = mane flicks backward/up (lifts), z>0 = sways toward +X"""
        self.drape(["hair_b", "hair_b2", "hair_b3"], [(t, -x * 0.6, 0, z * 0.5) for (t, x, y, z) in keys], delay=delay, gain=1.1)
        self.drape(["hair_r", "hair_r2"], [(t, -x * 0.3, 0, z * 0.6 + max(0, x) * 0.25) for (t, x, y, z) in keys], delay=delay)
        self.drape(["hair_l", "hair_l2"], [(t, -x * 0.3, 0, z * 0.6 - max(0, x) * 0.25) for (t, x, y, z) in keys], delay=delay)
        self.drape(["bangs"], [(t, -x * 0.15, 0, z * 0.2) for (t, x, y, z) in keys], delay=delay)
        self.drape(["ear_r"], [(t, -x * 0.12, 0, z * 0.15) for (t, x, y, z) in keys], delay=delay + 1)
        self.drape(["ear_l"], [(t, -x * 0.12, 0, z * 0.15) for (t, x, y, z) in keys], delay=delay + 1)
        self.drape(["scarf"], [(t, x * 0.5, 0, z * 0.6) for (t, x, y, z) in keys], delay=delay)
        return self

    def coat(self, keys, delay=2):
        """x>0 = tails fly backward (front flaps lift forward too), z>0 = flare toward +X"""
        self.drape(["coat_b", "coat_b2"], [(t, -x * 0.8, 0, z * 0.5) for (t, x, y, z) in keys], delay=delay, gain=0.9)
        self.drape(["coat_fr"], [(t, x * 0.5, 0, z * 0.6 + abs(z) * 0.3) for (t, x, y, z) in keys], delay=delay)
        self.drape(["coat_fl"], [(t, x * 0.5, 0, z * 0.6 - abs(z) * 0.3) for (t, x, y, z) in keys], delay=delay)
        return self

    def hose(self, keys, delay=2):
        """swings the hose loop: x>0 swings it forward, z sideways"""
        self.drape(["hose2", "hose3", "hose4"], [(t, x, 0, z) for (t, x, y, z) in keys], delay=delay, gain=0.85)
        return self

    def lean(self, *bones):
        """keys of these bones were authored with x>0 = lean FORWARD; the file convention is x<0 = forward"""
        for b in bones:
            self.tr[b]["rotation"] = [(t, -x, y, z) for (t, x, y, z) in self.tr[b]["rotation"]]
        return self

    def done(self, length=None):
        for p in PROPS:
            if p not in self.tr or "scale" not in self.tr[p]:
                self.scl(p, (0, *HIDE))
        for b, v in REST.items():
            if b not in self.tr or "rotation" not in self.tr[b]:
                self.rot(b, (0, *v))
        tracks = {b: {ch: sorted([(t / 20.0, x, y, z) for (t, x, y, z) in v], key=lambda q: q[0]) for ch, v in chs.items()}
                  for b, chs in self.tr.items()}
        m.anim(self.name, (length or self.ticks) / 20.0, tracks, loop=self.loop)


def legs(a, kr, kl=None, sr=None, sl=None, fr=None, fl=None):
    """leg keys for the right leg; left mirrors y/z unless given"""
    a.rot("leg_r", *kr)
    a.rot("leg_l", *(kl or [(t, x, -y, -z) for (t, x, y, z) in kr]))
    if sr: a.rot("shin_r", *sr)
    if sl or sr: a.rot("shin_l", *(sl or sr))
    if fr: a.rot("foot_r", *fr)
    if fl or fr: a.rot("foot_l", *(fl or fr))


def plus(b, dx=0, dy=0, dz=0):
    x, y, z = rest(b)
    return (x + dx, y + dy, z + dz)


def K(b, t, dx=0, dy=0, dz=0):
    return (t, *plus(b, dx, dy, dz))


# ------------------------------------------------------------------ idle (80 loop): slouched predator sway, taps the canister, grin-head tilt
a = A("idle", 80, loop=True)
a.pos("body", (0, 0, 0, 0), (20, 0, -0.25, 0), (40, 0, 0, 0), (60, 0, -0.25, 0), (80, 0, 0, 0))
a.rot("body", (0, 2, 0, 2), (40, 2, 0, -2), (80, 2, 0, 2))
a.rot("chest", (0, -4, 0, -1), (20, -3, 4, 0), (40, -4, 0, 1), (60, -5, -4, 0), (80, -4, 0, -1))
a.rot("head", K("head", 0), K("head", 20, -4, 8, 6), K("head", 34, -6, 10, 10), K("head", 46, 0, 0, 0), K("head", 60, 4, -10, -8), K("head", 80))
a.rot("arm_l", K("arm_l", 0), K("arm_l", 40, -4, 0, 2), K("arm_l", 80))
a.rot("fore_l", K("fore_l", 0), K("fore_l", 40, 6, 0, 0), K("fore_l", 80))
a.rot("gun", K("gun", 0), K("gun", 40, 6, 0, 0), K("gun", 80))
# right glove taps the canister twice
a.rot("arm_r", K("arm_r", 0), K("arm_r", 44), K("arm_r", 50, 34, 30, -14), K("arm_r", 64, 34, 30, -14), K("arm_r", 70), K("arm_r", 80))
a.rot("fore_r", K("fore_r", 0), K("fore_r", 44), K("fore_r", 50, 50), K("fore_r", 54, 30), K("fore_r", 56, 50), K("fore_r", 58, 30), K("fore_r", 60, 50),
      K("fore_r", 64, 50), K("fore_r", 70), K("fore_r", 80))
legs(a, [(0, 0, -4, 3), (40, 0, -4, 4), (80, 0, -4, 3)], [(0, 4, 6, -4), (40, 6, 6, -5), (80, 4, 6, -4)],
     sr=[(0, 0, 0, 0), (80, 0, 0, 0)], sl=[(0, -8, 0, 0), (40, -12, 0, 0), (80, -8, 0, 0)])
a.hair([(0, 0, 0, 2), (20, 2, 0, 0), (40, 0, 0, -2), (60, 2, 0, 0), (80, 0, 0, 2)], delay=5)
a.coat([(0, 1, 0, 1), (40, 0, 0, -1), (80, 1, 0, 1)], delay=4)
a.hose([(0, 0, 0, 3), (40, 0, 0, -3), (80, 0, 0, 3)], delay=4)
a.done()

# ------------------------------------------------------------------ walk (20 loop): long stalking stride, gun swaying, mane bouncing
a = A("walk", 20, loop=True)
a.rot("leg_r", (0, 30, 0, 0), (5, 0, 0, 0), (10, -28, 0, 0), (15, 0, 0, 0), (20, 30, 0, 0))
a.rot("shin_r", (0, -4, 0, 0), (5, -8, 0, 0), (10, -10, 0, 0), (13, -55, 0, 0), (17, -28, 0, 0), (20, -4, 0, 0))
a.rot("foot_r", (0, -12, 0, 0), (10, 12, 0, 0), (20, -12, 0, 0))
a.rot("leg_l", (0, -28, 0, 0), (5, 0, 0, 0), (10, 30, 0, 0), (15, 0, 0, 0), (20, -28, 0, 0))
a.rot("shin_l", (0, -10, 0, 0), (3, -55, 0, 0), (7, -28, 0, 0), (10, -4, 0, 0), (15, -8, 0, 0), (20, -10, 0, 0))
a.rot("foot_l", (0, 12, 0, 0), (10, -12, 0, 0), (20, 12, 0, 0))
a.pos("body", (0, 0, -0.5, 0), (5, 0, 0.5, 0), (10, 0, -0.5, 0), (15, 0, 0.5, 0), (20, 0, -0.5, 0))
a.rot("body", (0, -6, 6, -2), (10, -6, -6, 2), (20, -6, 6, -2))
a.rot("chest", (0, -2, -6, 2), (10, -2, 6, -2), (20, -2, -6, 2))
a.rot("head", K("head", 0, 4, 6), K("head", 5, 0, 0, 3), K("head", 10, 4, -6), K("head", 15, 0, 0, 3), K("head", 20, 4, 6))
a.rot("arm_r", K("arm_r", 0, -30), K("arm_r", 10, 26), K("arm_r", 20, -30))
a.rot("fore_r", K("fore_r", 0, -20), K("fore_r", 10, 10), K("fore_r", 20, -20))
a.rot("arm_l", K("arm_l", 0, 8), K("arm_l", 10, -8), K("arm_l", 20, 8))
a.rot("gun", K("gun", 0, -4), K("gun", 5, 4), K("gun", 10, -4), K("gun", 15, 4), K("gun", 20, -4))
a.hair([(0, 6, 0, 3), (5, 10, 0, 0), (10, 6, 0, -3), (15, 10, 0, 0), (20, 6, 0, 3)], delay=2)
a.coat([(0, 8, 0, 3), (5, 4, 0, 0), (10, 8, 0, -3), (15, 4, 0, 0), (20, 8, 0, 3)], delay=2)
a.hose([(0, 10, 0, 4), (5, -6, 0, 0), (10, 10, 0, -4), (15, -6, 0, 0), (20, 10, 0, 4)], delay=2)
a.done()

# ------------------------------------------------------------------ canister_bash (34): sideways club hit t9, overhead two-hand slam t18
a = A("canister_bash", 34)
a.r("arm_l", K("arm_l", 4, -10, 50, -40), K("arm_l", 6, -14, 60, -46), K("arm_l", 9, 60, -40, -10), K("arm_l", 11, 66, -56, -6),
    K("arm_l", 14, 150, 0, 10), K("arm_l", 16, 168, 0, 12), K("arm_l", 18, 60, 0, 10), K("arm_l", 21, 52, 0, 10), K("arm_l", 28, 20, 0, 4))
a.r("fore_l", K("fore_l", 4, -20), K("fore_l", 9, -50), K("fore_l", 13, -40), K("fore_l", 16, -30), K("fore_l", 18, -60), K("fore_l", 22, -50))
a.r("gun", K("gun", 4, 10, 0, -30), K("gun", 9, -10, 0, 20), K("gun", 13, -20), K("gun", 18, -40), K("gun", 22, -40), K("gun", 28, 0))
a.r("arm_r", K("arm_r", 6, -20, 0, 20), K("arm_r", 9, -30, 0, 30), K("arm_r", 14, 150, 0, -24), K("arm_r", 16, 166, 0, -30), K("arm_r", 18, 70, 0, -30),
    K("arm_r", 22, 60, 0, -26))
a.r("fore_r", K("fore_r", 14, -30), K("fore_r", 18, -20), K("fore_r", 24, 0))
a.r("chest", (4, -4, 34, 0), (6, -4, 40, 2), (9, 2, -30, -4), (11, 2, -38, -4), (14, 14, 0, 0), (16, 18, 0, 0), (18, -30, 0, 0), (21, -32, 0, 0), (28, -8, 0, 0))
a.r("head", K("head", 4, 0, -14, 6), K("head", 9, -6, 18, -4), K("head", 14, 14), K("head", 18, -12), K("head", 22, -6), K("head", 28, 2))
a.rot("body", (0, 0, 0, 0), (6, 0, 14, 0), (9, 0, -16, 0), (12, 0, -8, 0), (16, 6, 0, 0), (18, -14, 0, 0), (22, -12, 0, 0), (34, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (6, 0, -0.4, 0.6), (9, 0, -0.6, -1.0), (16, 0, 0.6, -0.6), (18, 0, -2.0, -2.0), (22, 0, -1.8, -1.8), (34, 0, 0, 0))
legs(a, [(0, 0, 0, 2), (9, -20, 0, 3), (16, -14, 0, 2), (18, -40, 0, 4), (22, -36, 0, 4), (34, 0, 0, 2)],
     [(0, 3, 0, -3), (9, 22, 0, -3), (16, 10, 0, -3), (18, 30, 0, -4), (22, 26, 0, -4), (34, 3, 0, -3)],
     sr=[(0, 0, 0, 0), (9, 8, 0, 0), (18, 40, 0, 0), (22, 36, 0, 0), (34, 0, 0, 0)], sl=[(0, -8, 0, 0), (18, -34, 0, 0), (34, -8, 0, 0)])
a.hair([(0, 0, 0, 0), (6, 0, 0, -12), (10, 4, 0, 16), (14, -8, 0, 4), (18, 18, 0, 0), (22, 6, 0, 0), (34, 0, 0, 0)])
a.coat([(0, 0, 0, 0), (6, 0, 0, -10), (10, 4, 0, 12), (18, 14, 0, 0), (34, 0, 0, 0)])
a.hose([(0, 0, 0, 0), (6, -20, 0, 20), (10, 30, 0, -30), (16, -30, 0, 0), (18, 40, 0, 0), (24, -10, 0, 0), (34, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ nozzle_jab (22): cocks the gun back, rapier thrust t7 (acid puff), recoil
a = A("nozzle_jab", 22)
a.r("arm_l", K("arm_l", 3, -40, 0, -10), K("arm_l", 5, -46, 0, -8), K("arm_l", 7, 60, 0, 14), K("arm_l", 9, 62, 0, 14), K("arm_l", 14, 30, 0, 6))
a.r("fore_l", K("fore_l", 3, 30), K("fore_l", 5, 34), K("fore_l", 7, -56), K("fore_l", 9, -58), K("fore_l", 14, -20))
a.r("gun", K("gun", 3, -20), K("gun", 7, -34, 0, 28), K("gun", 11, -32, 0, 24), K("gun", 16, -6))
a.r("arm_r", K("arm_r", 4, 30, 0, 20), K("arm_r", 7, -40, 0, 30), K("arm_r", 12, -20, 0, 20))
a.r("chest", (3, -6, 40, 0), (5, -8, 44, 0), (7, 8, -16, 0), (9, 10, -18, 0), (14, 2, -6, 0), (22, 0, 0, 0))
a.r("head", K("head", 3, 0, -20), K("head", 7, -6, 12), K("head", 12, 0, 6))
a.rot("body", (0, 0, 0, 0), (5, 0, 20, 0), (7, 10, -20, 0), (11, 8, -16, 0), (22, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (5, 0, -0.6, 1.0), (7, 0, -1.2, -2.6), (10, 0, -1.0, -2.4), (22, 0, 0, 0))
legs(a, [(0, 0, 0, 2), (5, 10, 0, 2), (7, -46, 0, 4), (11, -42, 0, 4), (22, 0, 0, 2)], [(0, 3, 0, -3), (5, -6, 0, -3), (7, 30, 0, -3), (11, 26, 0, -3), (22, 3, 0, -3)],
     sr=[(0, 0, 0, 0), (7, 30, 0, 0), (11, 26, 0, 0), (22, 0, 0, 0)], sl=[(0, -8, 0, 0), (7, -10, 0, 0), (22, -8, 0, 0)])
a.hair([(0, 0, 0, 0), (5, -6, 0, 6), (7, 16, 0, -4), (11, 6, 0, 0), (22, 0, 0, 0)])
a.coat([(0, 0, 0, 0), (5, -4, 0, 4), (7, 14, 0, -4), (22, 0, 0, 0)])
a.hose([(0, 0, 0, 0), (5, 20, 0, 0), (7, -30, 0, 0), (12, 10, 0, 0), (22, 0, 0, 0)])
a.scl("spray", (0, *HIDE), (6, *HIDE), (7, 0.6, 0.5, 0.6), (9, 0.9, 0.7, 0.9), (11, *HIDE))
a.lean("body", "chest")
a.done()

# ------------------------------------------------------------------ acid_spray (40): braces, aims level, sprays a sweeping acid cone t10-t28, shakes off
a = A("acid_spray", 40)
a.r("arm_l", K("arm_l", 6, 40, 0, 16), K("arm_l", 9, 66, 0, 20), K("arm_l", 14, 66, 20, 20), K("arm_l", 20, 66, -20, 20), K("arm_l", 26, 66, 16, 20),
    K("arm_l", 29, 66, 0, 20), K("arm_l", 34, 30, 0, 0))
a.r("fore_l", K("fore_l", 6, -40), K("fore_l", 9, -60), K("fore_l", 29, -60), K("fore_l", 34, -20))
a.r("gun", K("gun", 6, -30), K("gun", 9, -42), K("gun", 11, -40), K("gun", 12, -44), K("gun", 29, -42), K("gun", 34, -10))
a.r("arm_r", K("arm_r", 6, 50, 0, -10), K("arm_r", 9, 66, -30, -20), K("arm_r", 29, 66, -30, -20), K("arm_r", 34, 20, 0, 0))
a.r("fore_r", K("fore_r", 9, 10), K("fore_r", 29, 10))
a.r("chest", (6, -6, 0, 0), (9, 4, 14, 0), (14, 4, 34, 0), (20, 4, -6, 0), (26, 4, 28, 0), (29, 4, 14, 0), (34, -4, 0, 0), (40, 0, 0, 0))
a.r("head", K("head", 6, -8), K("head", 9, -4, 0, -8), K("head", 14, -4, 10, -10), K("head", 20, -4, -6, -10), K("head", 29, -4, 4, -8), K("head", 34, 4, 0, 10))
a.rot("body", (0, 0, 0, 0), (6, 0, 0, 0), (9, 0, -10, 0), (14, 0, 10, 0), (20, 0, -26, 0), (26, 0, 6, 0), (29, 0, -6, 0), (40, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (6, 0, -0.8, 0), (9, 0, -1.2, 0.6), (29, 0, -1.2, 0.6), (40, 0, 0, 0))
legs(a, [(0, 0, 0, 2), (9, -24, 0, 6), (29, -24, 0, 6), (40, 0, 0, 2)], [(0, 3, 0, -3), (9, 20, 0, -6), (29, 20, 0, -6), (40, 3, 0, -3)],
     sr=[(0, 0, 0, 0), (9, 22, 0, 0), (29, 22, 0, 0), (40, 0, 0, 0)], sl=[(0, -8, 0, 0), (9, -14, 0, 0), (29, -14, 0, 0), (40, -8, 0, 0)])
a.hair([(0, 0, 0, 0), (9, 6, 0, 0), (13, 8, 0, 6), (17, 6, 0, -6), (21, 8, 0, 6), (25, 6, 0, -6), (29, 6, 0, 0), (40, 0, 0, 0)], delay=2)
a.coat([(0, 0, 0, 0), (9, 6, 0, 0), (12, 8, 0, 3), (16, 6, 0, -3), (20, 8, 0, 3), (24, 6, 0, -3), (29, 6, 0, 0), (40, 0, 0, 0)])
a.hose([(0, 0, 0, 0), (10, 10, 0, 6), (12, 4, 0, -6), (14, 10, 0, 6), (16, 4, 0, -6), (18, 10, 0, 6), (20, 4, 0, -6), (22, 10, 0, 6), (24, 4, 0, -6),
        (26, 10, 0, 6), (28, 4, 0, 0), (40, 0, 0, 0)], delay=1)
a.show("spray", 10, 29)
a.done()

# ------------------------------------------------------------------ hair_lash (32): coils low, full 360 spin t9-t15 whipping the mane (hit t12)
a = A("hair_lash", 32)
a.rot("body", (0, 0, 0, 0), (6, 10, 50, 0), (8, 12, 60, 0), (10, 8, -60, 0), (12, 6, -180, 0), (14, 4, -300, 0), (16, 2, -340, 0), (20, 0, -360, 0),
      (32, 0, -360, 0))
a.pos("body", (0, 0, 0, 0), (6, 0, -2.4, 0), (8, 0, -2.6, 0), (12, 0, -0.8, 0), (16, 0, -1.2, 0), (20, 0, -0.4, 0), (32, 0, 0, 0))
a.r("chest", (6, -14, 20, 0), (8, -16, 24, 0), (12, 6, -20, 0), (16, 0, -10, 0), (24, -4, 0, 0))
a.r("head", K("head", 6, -10, 20), K("head", 8, -14, 24), K("head", 12, 10, -30, -10), K("head", 16, 6, -10), K("head", 24, -4, 0, 10))
a.r("arm_l", K("arm_l", 6, 30, 0, 30), K("arm_l", 12, 10, 0, -80), K("arm_l", 18, 10, 0, -50), K("arm_l", 24, 10, 0, -20))
a.r("fore_l", K("fore_l", 6, 20), K("fore_l", 12, -40), K("fore_l", 18, -20))
a.r("gun", K("gun", 12, 0, 0, -30), K("gun", 18, 0, 0, -10))
a.r("arm_r", K("arm_r", 6, 30, 0, -30), K("arm_r", 12, 10, 0, 80), K("arm_r", 18, 10, 0, 50), K("arm_r", 24, 10, 0, 20))
legs(a, [(0, 0, 0, 2), (6, -30, 0, 6), (8, -32, 0, 6), (12, -6, 0, 10), (16, -4, 0, 6), (32, 0, 0, 2)],
     [(0, 3, 0, -3), (6, 20, 0, -6), (8, 22, 0, -6), (12, 6, 0, -10), (16, 4, 0, -6), (32, 3, 0, -3)],
     sr=[(0, 0, 0, 0), (6, 40, 0, 0), (8, 44, 0, 0), (12, 6, 0, 0), (32, 0, 0, 0)], sl=[(0, -8, 0, 0), (6, -20, 0, 0), (12, -4, 0, 0), (32, -8, 0, 0)])
# mane flung out horizontally by the spin
a.rot("hair_b", K("hair_b", 0), K("hair_b", 6, 10, 0, 20), K("hair_b", 10, -40, 0, 50), K("hair_b", 12, -70, 0, 70), K("hair_b", 15, -64, 0, 60),
      K("hair_b", 20, -20, 0, 10), K("hair_b", 26, 4, 0, -6), K("hair_b", 32))
a.rot("hair_b2", K("hair_b2", 0), K("hair_b2", 8, 6, 0, 10), K("hair_b2", 12, -20, 0, 20), K("hair_b2", 16, -24, 0, 20), K("hair_b2", 22, 10, 0, -10), K("hair_b2", 32))
a.rot("hair_b3", K("hair_b3", 0), K("hair_b3", 10, 4, 0, 10), K("hair_b3", 14, -16, 0, 14), K("hair_b3", 18, -16, 0, 10), K("hair_b3", 24, 10, 0, -8), K("hair_b3", 32))
for kk, s in (("hair_r", 1), ("hair_l", -1)):
    a.rot(kk, K(kk, 0), K(kk, 12, 0, 0, 60 * s), K(kk, 16, 0, 0, 50 * s), K(kk, 24, 0, 0, -6 * s), K(kk, 32))
a.coat([(0, 0, 0, 0), (8, -4, 0, 10), (12, 20, 0, 30), (16, 16, 0, 20), (22, -4, 0, -6), (32, 0, 0, 0)])
a.hose([(0, 0, 0, 0), (12, -40, 0, 50), (18, -10, 0, 20), (24, 10, 0, -10), (32, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ hose_whip (30): right hand grabs the hose, windmill t4-t10, crack t12, yank t18
a = A("hose_whip", 30)
a.r("arm_r", K("arm_r", 3, 20, 0, -30), K("arm_r", 6, 150, 0, -20), K("arm_r", 8, 170, 0, -10), K("arm_r", 10, 190, 0, 0), K("arm_r", 12, 70, 0, -10),
    K("arm_r", 14, 60, 0, -10), K("arm_r", 18, -10, 0, 10), K("arm_r", 22, 0, 0, 10))
a.r("fore_r", K("fore_r", 3, 70), K("fore_r", 8, 10), K("fore_r", 12, -30), K("fore_r", 18, 60), K("fore_r", 22, 50))
a.r("arm_l", K("arm_l", 4, -10), K("arm_l", 12, 10, 0, 6), K("arm_l", 18, -6))
a.r("hose1", K("hose1", 3, 0, 0, 60), K("hose1", 8, -40, 0, 70), K("hose1", 12, 40, 0, 50), K("hose1", 18, 0, 0, 30), K("hose1", 24))
a.rot("hose2", K("hose2", 0), K("hose2", 6, -60, 0, 20), K("hose2", 10, -80), K("hose2", 12, -40), K("hose2", 13, -40), K("hose2", 18, 40), K("hose2", 30))
a.rot("hose3", K("hose3", 0), K("hose3", 7, -80, 0, 20), K("hose3", 11, -60), K("hose3", 12, -80), K("hose3", 14, -60), K("hose3", 19, 40), K("hose3", 30))
a.rot("hose4", K("hose4", 0), K("hose4", 8, -60), K("hose4", 12, -90), K("hose4", 15, -30), K("hose4", 20, 30), K("hose4", 30))
a.r("chest", (4, -10, -10, 0), (8, -14, -16, 0), (12, 14, 16, 0), (14, 16, 18, 0), (18, -10, -10, 0), (22, -6, -6, 0))
a.r("head", K("head", 4, -10), K("head", 8, -12, -10), K("head", 12, 8, 10, -6), K("head", 18, -6, 0, 8))
a.rot("body", (0, 0, 0, 0), (8, -4, -14, 0), (12, 8, 12, 0), (18, -10, -6, 0), (30, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (8, 0, 0.2, 0.4), (12, 0, -0.8, -1.2), (18, 0, -0.4, 0.8), (30, 0, 0, 0))
legs(a, [(0, 0, 0, 2), (8, 10, 0, 2), (12, -30, 0, 3), (18, -10, 0, 2), (30, 0, 0, 2)], [(0, 3, 0, -3), (8, -10, 0, -3), (12, 24, 0, -3), (18, 14, 0, -3), (30, 3, 0, -3)],
     sr=[(0, 0, 0, 0), (12, 26, 0, 0), (30, 0, 0, 0)], sl=[(0, -8, 0, 0), (12, -12, 0, 0), (30, -8, 0, 0)])
a.hair([(0, 0, 0, 0), (8, -6, 0, -6), (12, 14, 0, 8), (18, -8, 0, 0), (30, 0, 0, 0)])
a.coat([(0, 0, 0, 0), (8, -4, 0, -6), (12, 12, 0, 6), (18, -6, 0, 0), (30, 0, 0, 0)])
a.show("lash", 3, 24, pulse=False)
a.rot("lash", (0, 0, 0, 0), (4, -20, 0, 0), (8, -50, 0, 0), (10, -60, 0, 0), (12, 10, 0, 0), (13, 20, 0, 0), (16, -10, 0, 0), (22, 0, 0, 0), (30, 0, 0, 0))
a.rot("lash2", (0, 0, 0, 0), (5, -30, 0, 0), (9, -60, 0, 0), (11, -70, 0, 0), (12, -10, 0, 0), (13, 30, 0, 0), (15, 20, 0, 0), (18, -10, 0, 0), (24, 0, 0, 0))
a.rot("lash3", (0, 0, 0, 0), (6, -30, 0, 0), (10, -70, 0, 0), (12, -40, 0, 0), (13, 20, 0, 0), (14, 40, 0, 0), (17, 0, 0, 0), (20, -10, 0, 0), (26, 0, 0, 0))
a.lean("body", "chest")
a.done()

# ------------------------------------------------------------------ boot_kick (26): knee chamber, pointed-boot push kick t9, hop back
a = A("boot_kick", 26)
a.rot("leg_r", (0, 0, 0, 2), (4, 70, 0, 4), (6, 80, 0, 4), (9, 96, 0, 2), (11, 92, 0, 2), (15, 40, 0, 2), (19, -10, 0, 2), (26, 0, 0, 2))
a.rot("shin_r", (0, 0, 0, 0), (4, -100, 0, 0), (6, -110, 0, 0), (9, -4, 0, 0), (11, -2, 0, 0), (15, -60, 0, 0), (20, -10, 0, 0), (26, 0, 0, 0))
a.rot("foot_r", (0, 0, 0, 0), (6, 30, 0, 0), (9, -30, 0, 0), (12, -20, 0, 0), (18, 0, 0, 0), (26, 0, 0, 0))
a.rot("leg_l", (0, 3, 0, -3), (6, -14, 0, -3), (9, -20, 0, -3), (15, -10, 0, -3), (26, 3, 0, -3))
a.rot("shin_l", (0, -8, 0, 0), (6, 20, 0, 0), (9, 16, 0, 0), (26, -8, 0, 0))
a.rot("body", (0, 0, 0, 0), (6, -20, 6, 0), (9, -34, 0, 0), (11, -32, 0, 0), (16, -10, 0, 0), (26, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (6, 0, -0.4, 0.4), (9, 0, -0.8, -0.6), (15, 0, 0.4, 1.0), (19, 0, 0, 1.4), (26, 0, 0, 0))
a.r("chest", (6, 14, -6, 0), (9, 20, 0, 0), (16, 6, 0, 0))
a.r("head", K("head", 6, 6, 6), K("head", 9, 16, 0), K("head", 16, 4))
a.r("arm_r", K("arm_r", 6, -50, 0, 40), K("arm_r", 9, -60, 0, 50), K("arm_r", 16, -10, 0, 30))
a.r("arm_l", K("arm_l", 6, 20, 0, -40), K("arm_l", 9, 30, 0, -50), K("arm_l", 16, 10, 0, -30))
a.r("gun", K("gun", 9, 20), K("gun", 16, 10))
a.hair([(0, 0, 0, 0), (6, -6, 0, 0), (9, -12, 0, 0), (12, 10, 0, 0), (18, -4, 0, 0), (26, 0, 0, 0)])
a.coat([(0, 0, 0, 0), (6, -4, 0, 2), (9, -10, 0, 0), (13, 8, 0, 0), (26, 0, 0, 0)])
a.hose([(0, 0, 0, 0), (9, 30, 0, 0), (14, -20, 0, 0), (26, 0, 0, 0)])
a.lean("body", "chest")
a.done()

# ------------------------------------------------------------------ lab_lunge (36): sinks low, dashes t9, nozzle stab t12, rising canister uppercut t20
a = A("lab_lunge", 36)
a.r("arm_l", K("arm_l", 4, -30, 0, -6), K("arm_l", 8, -40, 0, -6), K("arm_l", 12, 66, 0, 16), K("arm_l", 14, 64, 0, 16), K("arm_l", 17, -10, 0, -20),
    K("arm_l", 20, 150, 0, -10), K("arm_l", 22, 168, 0, -10), K("arm_l", 28, 60, 0, -14))
a.r("fore_l", K("fore_l", 4, 30), K("fore_l", 8, 40), K("fore_l", 12, -60), K("fore_l", 15, -50), K("fore_l", 17, 20), K("fore_l", 20, -30), K("fore_l", 24, -20))
a.r("gun", K("gun", 8, -10), K("gun", 12, -20, 0, 26), K("gun", 16, -14, 0, 20), K("gun", 20, -10), K("gun", 26, 0))
a.r("arm_r", K("arm_r", 4, 40, 0, 30), K("arm_r", 8, 50, 0, 40), K("arm_r", 12, -50, 0, 30), K("arm_r", 20, -20, 0, 40), K("arm_r", 28, 0, 0, 20))
a.r("chest", (4, 16, 30, 0), (8, 22, 34, 0), (12, 16, -20, 0), (15, 14, -16, 0), (17, 22, 10, 0), (20, -20, -10, 0), (22, -24, -10, 0), (28, -6, 0, 0))
a.r("head", K("head", 4, -16, -20), K("head", 8, -20, -26), K("head", 12, -14, 16), K("head", 17, -14), K("head", 20, 20, 0, -6), K("head", 26, 4))
a.rot("body", (0, 0, 0, 0), (4, 18, 20, 0), (8, 22, 24, 0), (12, 20, -10, 0), (15, 18, -6, 0), (17, 20, 0, 0), (20, -6, 0, 0), (24, -4, 0, 0), (36, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (4, 0, -3.0, 1.0), (8, 0, -3.4, 1.2), (10, 0, -2.4, -2.0), (12, 0, -2.6, -3.0), (16, 0, -2.6, -3.0), (17, 0, -3.0, -3.0),
      (20, 0, 0.8, -3.2), (22, 0, 1.0, -3.0), (28, 0, 0, -1.0), (36, 0, 0, 0))
legs(a, [(0, 0, 0, 2), (4, -50, 0, 4), (8, -56, 0, 4), (12, -60, 0, 6), (17, -56, 0, 4), (20, -10, 0, 2), (28, -4, 0, 2), (36, 0, 0, 2)],
     [(0, 3, 0, -3), (4, 20, 0, -4), (8, 24, 0, -4), (12, 40, 0, -6), (17, 34, 0, -4), (20, 30, 0, -3), (28, 6, 0, -3), (36, 3, 0, -3)],
     sr=[(0, 0, 0, 0), (4, 70, 0, 0), (8, 76, 0, 0), (12, 50, 0, 0), (17, 60, 0, 0), (20, 6, 0, 0), (36, 0, 0, 0)],
     sl=[(0, -8, 0, 0), (4, -50, 0, 0), (8, -56, 0, 0), (12, -30, 0, 0), (17, -40, 0, 0), (20, -20, 0, 0), (36, -8, 0, 0)])
a.hair([(0, 0, 0, 0), (4, -10, 0, 0), (10, 20, 0, 0), (13, 26, 0, 4), (17, 10, 0, 0), (20, -16, 0, 0), (24, 10, 0, 0), (36, 0, 0, 0)])
a.coat([(0, 0, 0, 0), (4, -6, 0, 0), (10, 20, 0, 0), (13, 24, 0, 0), (17, 10, 0, 0), (21, -10, 0, 0), (36, 0, 0, 0)])
a.hose([(0, 0, 0, 0), (8, 20, 0, 10), (12, -40, 0, 0), (17, 30, 0, 0), (21, -40, 0, 0), (28, 10, 0, 0), (36, 0, 0, 0)])
a.lean("body", "chest", "head")
a.done()

# ------------------------------------------------------------------ acid_puddle (36): aims at the ground, sweeps a hissing puddle t8-t20 (trap armed t14)
a = A("acid_puddle", 36)
a.r("arm_l", K("arm_l", 5, 50, 0, 10), K("arm_l", 8, 40, 30, 10), K("arm_l", 14, 40, -20, 14), K("arm_l", 20, 40, 20, 10), K("arm_l", 24, 20, 0, 0))
a.r("fore_l", K("fore_l", 5, -30), K("fore_l", 8, -50), K("fore_l", 20, -50), K("fore_l", 26, -10))
a.r("gun", K("gun", 5, -60), K("gun", 8, -76), K("gun", 20, -76), K("gun", 26, -20))
a.r("arm_r", K("arm_r", 5, -10, 0, 40), K("arm_r", 8, -20, 0, 50), K("arm_r", 20, -20, 0, 50), K("arm_r", 26, 0, 0, 20))
a.r("chest", (5, 10, 10, 0), (8, 20, 24, 0), (14, 22, -10, 0), (20, 20, 20, 0), (24, 8, 0, 0), (28, -10, 0, 0))
a.r("head", K("head", 8, -20, 10), K("head", 14, -24, -8), K("head", 20, -20, 10), K("head", 26, 10, 0, 12), K("head", 30, 6, 0, 8))
a.rot("body", (0, 0, 0, 0), (8, 10, 6, 0), (14, 12, -8, 0), (20, 10, 6, 0), (26, -4, 0, 0), (36, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (8, 0, -1.2, 0.6), (20, 0, -1.2, 0.6), (28, 0, 0, 0), (36, 0, 0, 0))
legs(a, [(0, 0, 0, 2), (8, -20, 0, 6), (20, -20, 0, 6), (36, 0, 0, 2)], [(0, 3, 0, -3), (8, 14, 0, -6), (20, 14, 0, -6), (36, 3, 0, -3)],
     sr=[(0, 0, 0, 0), (8, 24, 0, 0), (20, 24, 0, 0), (36, 0, 0, 0)], sl=[(0, -8, 0, 0), (8, -10, 0, 0), (36, -8, 0, 0)])
a.hair([(0, 0, 0, 0), (8, -8, 0, 4), (14, -6, 0, -4), (20, -8, 0, 4), (28, 6, 0, 0), (36, 0, 0, 0)], delay=3)
a.coat([(0, 0, 0, 0), (8, 4, 0, 0), (20, 4, 0, 0), (36, 0, 0, 0)])
a.hose([(0, 0, 0, 0), (8, 10, 0, 10), (14, -6, 0, -10), (20, 10, 0, 10), (28, 0, 0, 0), (36, 0, 0, 0)])
a.show("spray", 8, 20)
a.scl("tox", (0, *HIDE), (9, *HIDE), (10, 0.3, 1, 0.3), (14, 0.8, 1, 0.8), (20, 1.1, 1, 1.1), (32, 1.0, 1, 1.0), (35, *HIDE))
a.lean("body", "chest")
a.done()

# ------------------------------------------------------------------ goggle_charge (38): snaps goggles down t4-8, lowers the spiked head, rams t16, t20
a = A("goggle_charge", 38)
a.rot("goggles", K("goggles", 0), K("goggles", 3, -20), K("goggles", 6, 30), K("goggles", 34, 30), K("goggles", 38))
a.pos("goggles", (0, 0, 0, 0), (3, 0, 0.6, 0), (6, 0, -2.6, -0.6), (34, 0, -2.6, -0.6), (38, 0, 0, 0))
a.r("arm_r", K("arm_r", 2, 150, 0, -20), K("arm_r", 5, 120, 0, -30), K("arm_r", 8, -40, 0, 30), K("arm_r", 12, -60, 0, 40), K("arm_r", 24, -60, 0, 40),
    K("arm_r", 30, -10, 0, 20))
a.r("fore_r", K("fore_r", 2, 90), K("fore_r", 5, 100), K("fore_r", 8, 20))
a.r("arm_l", K("arm_l", 8, -40, 0, -20), K("arm_l", 12, -60, 0, -30), K("arm_l", 24, -60, 0, -30), K("arm_l", 30, -10, 0, -20))
a.r("gun", K("gun", 8, 40), K("gun", 24, 40), K("gun", 30, 10))
a.r("chest", (8, 20, 0, 0), (12, 30, 0, 0), (16, 34, 0, 0), (18, 26, 0, 0), (20, 36, 0, 0), (24, 30, 0, 0), (30, 4, 0, 0))
a.r("head", K("head", 6, -10), K("head", 10, 20), K("head", 16, 30), K("head", 18, 14), K("head", 20, 30), K("head", 26, 10), K("head", 32, -6))
a.rot("body", (0, 0, 0, 0), (8, 14, 0, 0), (12, 26, 0, 0), (24, 26, 0, 0), (30, 0, 0, 0), (38, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (8, 0, -1.6, 0.6), (12, 0, -2.2, 0), (16, 0, -1.6, -2.0), (20, 0, -1.6, -2.0), (24, 0, -1.8, -1.6), (30, 0, 0, 0))
legs(a, [(0, 0, 0, 2), (8, -30, 0, 2), (12, -50, 0, 2), (14, 10, 0, 2), (16, -50, 0, 2), (18, 10, 0, 2), (20, -50, 0, 2), (24, -30, 0, 2), (30, 0, 0, 2)],
     [(0, 3, 0, -3), (8, 10, 0, -3), (12, 30, 0, -3), (14, -40, 0, -3), (16, 30, 0, -3), (18, -40, 0, -3), (20, 30, 0, -3), (24, 10, 0, -3), (30, 3, 0, -3)],
     sr=[(0, 0, 0, 0), (8, 30, 0, 0), (12, 50, 0, 0), (14, 70, 0, 0), (16, 30, 0, 0), (18, 70, 0, 0), (20, 30, 0, 0), (30, 0, 0, 0)],
     sl=[(0, -8, 0, 0), (12, -40, 0, 0), (14, -10, 0, 0), (16, -70, 0, 0), (18, -10, 0, 0), (20, -70, 0, 0), (30, -8, 0, 0)])
# ear spikes + crown point forward like horns
for kk in ("ear_r", "ear_l"):
    a.rot(kk, K(kk, 0), K(kk, 8, 0), K(kk, 12, -30), K(kk, 26, -30), K(kk, 32, 0), K(kk, 38))
a.rot("hair_b", K("hair_b", 0), K("hair_b", 12, 40), K("hair_b", 16, 50, 0, 4), K("hair_b", 20, 46, 0, -4), K("hair_b", 26, 30), K("hair_b", 34, -4), K("hair_b", 38))
a.rot("hair_b2", K("hair_b2", 0), K("hair_b2", 14, 20), K("hair_b2", 20, 24), K("hair_b2", 28, 10), K("hair_b2", 34, -6), K("hair_b2", 38))
a.rot("hair_b3", K("hair_b3", 0), K("hair_b3", 16, 16), K("hair_b3", 22, 20), K("hair_b3", 30, 0), K("hair_b3", 38))
a.coat([(0, 0, 0, 0), (12, 20, 0, 0), (16, 26, 0, 4), (20, 26, 0, -4), (26, 16, 0, 0), (34, -4, 0, 0), (38, 0, 0, 0)])
a.hose([(0, 0, 0, 0), (12, -30, 0, 0), (20, -40, 0, 10), (28, 10, 0, 0), (38, 0, 0, 0)])
a.lean("body", "chest", "head")
a.done()

# ------------------------------------------------------------------ grin_bite (40): glove grab t10, pulls in, chomps t20 + t28, shoves away t34
a = A("grin_bite", 40)
a.r("arm_r", K("arm_r", 4, -20, 0, 20), K("arm_r", 8, 80, 0, -10), K("arm_r", 10, 86, 0, -14), K("arm_r", 14, 60, 0, -20), K("arm_r", 20, 50, 0, -24),
    K("arm_r", 28, 50, 0, -24), K("arm_r", 32, 40, 0, -20), K("arm_r", 34, 90, 0, -10), K("arm_r", 36, 86, 0, -10))
a.r("fore_r", K("fore_r", 4, 60), K("fore_r", 8, -10), K("fore_r", 14, 40), K("fore_r", 20, 70), K("fore_r", 32, 70), K("fore_r", 34, -10), K("fore_r", 37, 0))
a.r("hand_r", K("hand_r", 10, 30), K("hand_r", 32, 30), K("hand_r", 34, -30))
a.r("arm_l", K("arm_l", 4, -10, 0, -40), K("arm_l", 20, -10, 0, -50), K("arm_l", 34, 0, 0, -40))
a.r("gun", K("gun", 10, 20), K("gun", 34, 10))
a.r("chest", (4, -6, 20, 0), (8, 10, -10, 0), (10, 14, -14, 0), (16, 6, 0, 0), (18, -4, 0, 0), (20, 22, 0, 0), (24, 6, 0, 0), (26, -4, 0, 0), (28, 24, 0, 0),
    (31, 6, 0, 0), (34, 10, -10, 0), (40, 0, 0, 0))
a.r("head", K("head", 4, -6), K("head", 8, 6), K("head", 16, 6, 0, 6), K("head", 18, 24, 0, 10), K("head", 20, -26, 0, -4), K("head", 23, -16), K("head", 26, 26, 0, -10),
    K("head", 28, -28, 0, 4), K("head", 31, -14), K("head", 35, 14, 0, 14))
a.rot("body", (0, 0, 0, 0), (8, 14, -10, 0), (10, 16, -14, 0), (16, 4, 0, 0), (20, 10, 0, 0), (28, 10, 0, 0), (34, 10, -6, 0), (40, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (4, 0, -0.6, 0.6), (9, 0, -1.0, -2.4), (14, 0, -0.6, -1.4), (34, 0, -0.6, -1.4), (38, 0, 0, 0.4), (40, 0, 0, 0))
legs(a, [(0, 0, 0, 2), (9, -40, 0, 4), (14, -26, 0, 3), (34, -26, 0, 3), (40, 0, 0, 2)], [(0, 3, 0, -3), (9, 30, 0, -3), (14, 20, 0, -3), (34, 20, 0, -3), (40, 3, 0, -3)],
     sr=[(0, 0, 0, 0), (9, 30, 0, 0), (34, 20, 0, 0), (40, 0, 0, 0)], sl=[(0, -8, 0, 0), (9, -20, 0, 0), (40, -8, 0, 0)])
a.hair([(0, 0, 0, 0), (9, 14, 0, 0), (14, 4, 0, 0), (18, -8, 0, 6), (20, 12, 0, -4), (26, -8, 0, -6), (28, 12, 0, 4), (34, 8, 0, 0), (40, 0, 0, 0)])
a.coat([(0, 0, 0, 0), (9, 14, 0, 0), (14, 4, 0, 0), (34, 6, 0, 0), (40, 0, 0, 0)])
a.hose([(0, 0, 0, 0), (9, -20, 0, 0), (20, 10, 0, 6), (28, -10, 0, -6), (34, 20, 0, 0), (40, 0, 0, 0)])
a.lean("body", "chest")
a.done()

# ------------------------------------------------------------------ acid_mortar (40): points the gun skyward, pumps, lobs 3 globs t12/t16/t20
a = A("acid_mortar", 40)
a.r("arm_l", K("arm_l", 6, 130, 0, -10), K("arm_l", 10, 140, 0, -10), K("arm_l", 12, 130, 0, -14), K("arm_l", 13, 140, 0, -10), K("arm_l", 16, 128, 0, -6),
    K("arm_l", 17, 140, 0, -10), K("arm_l", 20, 126, 0, -18), K("arm_l", 22, 138, 0, -10), K("arm_l", 30, 40, 0, -20))
a.r("fore_l", K("fore_l", 6, -40), K("fore_l", 22, -40), K("fore_l", 30, 0))
a.r("gun", K("gun", 6, -30), K("gun", 22, -30), K("gun", 30, 0))
# right hand pumps the canister body
a.r("arm_r", K("arm_r", 4, 100, 0, -30), K("arm_r", 7, 120, 0, -40), K("arm_r", 9, 100, 0, -40), K("arm_r", 11, 124, 0, -40), K("arm_r", 14, 100, 0, -40),
    K("arm_r", 15, 124, 0, -40), K("arm_r", 18, 100, 0, -40), K("arm_r", 19, 124, 0, -40), K("arm_r", 24, 40, 0, 0))
a.r("fore_r", K("fore_r", 4, 40), K("fore_r", 9, 60), K("fore_r", 11, 30), K("fore_r", 14, 60), K("fore_r", 15, 30), K("fore_r", 18, 60), K("fore_r", 19, 30),
    K("fore_r", 24, 30))
a.r("chest", (6, 16, -10, 0), (12, 12, -10, 0), (13, 18, -10, 0), (16, 12, -10, 0), (17, 18, -10, 0), (20, 12, -10, 0), (21, 18, -10, 0), (30, -4, 0, 0))
a.r("head", K("head", 6, 24, -10), K("head", 22, 26, -10), K("head", 28, -6, 0, 10), K("head", 34, 4, 0, 12))
a.rot("body", (0, 0, 0, 0), (6, 8, 16, 0), (22, 8, 16, 0), (30, 0, 0, 0), (40, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (6, 0, -1.0, 0.8), (12, 0, -1.4, 1.0), (13, 0, -0.8, 1.0), (16, 0, -1.4, 1.0), (17, 0, -0.8, 1.0), (20, 0, -1.4, 1.0),
      (21, 0, -0.8, 1.0), (30, 0, 0, 0), (40, 0, 0, 0))
legs(a, [(0, 0, 0, 2), (6, -22, 0, 8), (22, -22, 0, 8), (32, 0, 0, 2), (40, 0, 0, 2)], [(0, 3, 0, -3), (6, 20, 0, -8), (22, 20, 0, -8), (32, 3, 0, -3), (40, 3, 0, -3)],
     sr=[(0, 0, 0, 0), (6, 24, 0, 0), (22, 24, 0, 0), (32, 0, 0, 0)], sl=[(0, -8, 0, 0), (6, -14, 0, 0), (32, -8, 0, 0)])
a.hair([(0, 0, 0, 0), (6, -4, 0, 0), (12, 8, 0, 0), (14, -2, 0, 0), (16, 8, 0, 0), (18, -2, 0, 0), (20, 8, 0, 0), (26, -2, 0, 0), (40, 0, 0, 0)], delay=2)
a.coat([(0, 0, 0, 0), (12, 6, 0, 0), (16, 6, 0, 0), (20, 6, 0, 0), (28, 0, 0, 0), (40, 0, 0, 0)])
a.hose([(0, 0, 0, 0), (12, 20, 0, 10), (14, -10, 0, 0), (16, 20, 0, -10), (18, -10, 0, 0), (20, 20, 0, 10), (26, 0, 0, 0), (40, 0, 0, 0)])
a.scl("spray", (0, *HIDE), (11, *HIDE), (12, 0.8, 0.6, 0.8), (13, *HIDE), (15, *HIDE), (16, 0.8, 0.6, 0.8), (17, *HIDE), (19, *HIDE), (20, 0.8, 0.6, 0.8), (21, *HIDE))
a.done()

# ------------------------------------------------------------------ toxic_overdrive (56, enraged): goggles down, spray-spins twice t14-t38 (hits every 4t),
#                                                                    then overhead canister crash t46 + toxic shockwave
a = A("toxic_overdrive", 56)
a.rot("goggles", K("goggles", 0), K("goggles", 3, -20), K("goggles", 6, 30), K("goggles", 50, 30), K("goggles", 56))
a.pos("goggles", (0, 0, 0, 0), (3, 0, 0.6, 0), (6, 0, -2.6, -0.6), (50, 0, -2.6, -0.6), (56, 0, 0, 0))
a.r("arm_r", K("arm_r", 2, 150, 0, -20), K("arm_r", 5, 120, 0, -30), K("arm_r", 10, 10, 0, 80), K("arm_r", 38, 10, 0, 80), K("arm_r", 42, 160, 0, -20),
    K("arm_r", 44, 170, 0, -30), K("arm_r", 46, 60, 0, -30), K("arm_r", 50, 50, 0, -20))
a.r("fore_r", K("fore_r", 2, 90), K("fore_r", 5, 100), K("fore_r", 10, 0), K("fore_r", 42, -30), K("fore_r", 46, -20))
a.r("arm_l", (10, 30, 0, -60), (14, 4, 0, -92), (38, 4, 0, -92), K("arm_l", 42, 160, 0, 10), K("arm_l", 44, 170, 0, 20),
    K("arm_l", 46, 60, 0, 20), K("arm_l", 50, 50, 0, 10))
a.r("fore_l", (10, 10, 0, 0), (14, 0, 0, 0), (38, 0, 0, 0), K("fore_l", 42, -30), K("fore_l", 46, -60))
a.r("gun", (10, 20, 0, 0), (14, 0, 0, 0), (38, 0, 0, 0), K("gun", 42, -20), K("gun", 46, -40, 0, 30), K("gun", 50, -30, 0, 20))
a.rot("body", (0, 0, 0, 0), (10, 4, 30, 0), (14, 0, 0, 0), (20, 0, -180, 0), (26, 0, -360, 0), (32, 0, -540, 0), (38, 0, -720, 0), (42, 10, -720, 0),
      (44, 12, -720, 0), (46, -16, -720, 0), (50, -14, -720, 0), (56, 0, -720, 0))
a.pos("body", (0, 0, 0, 0), (10, 0, -1.4, 0), (14, 0, -1.0, 0), (38, 0, -1.0, 0), (42, 0, 0.6, 0), (44, 0, 1.0, 0), (46, 0, -2.4, -2.0), (50, 0, -2.2, -1.8),
      (56, 0, 0, 0))
a.r("chest", (10, -6, 20, 0), (14, 6, 0, 0), (38, 6, 0, 0), (42, 14, 0, 0), (44, 18, 0, 0), (46, -32, 0, 0), (50, -30, 0, 0))
a.r("head", K("head", 10, -10, 10), K("head", 14, 10, 0, -14), K("head", 38, 10, 0, 14), K("head", 44, 20), K("head", 46, -14), K("head", 52, 10, 0, 16))
legs(a, [(0, 0, 0, 2), (10, -24, 0, 8), (14, -10, 0, 12), (38, -10, 0, 12), (44, -6, 0, 2), (46, -40, 0, 4), (50, -36, 0, 4), (56, 0, 0, 2)],
     [(0, 3, 0, -3), (10, 20, 0, -8), (14, 10, 0, -12), (38, 10, 0, -12), (44, 6, 0, -3), (46, 30, 0, -4), (50, 26, 0, -4), (56, 3, 0, -3)],
     sr=[(0, 0, 0, 0), (10, 30, 0, 0), (14, 10, 0, 0), (38, 10, 0, 0), (46, 40, 0, 0), (50, 36, 0, 0), (56, 0, 0, 0)],
     sl=[(0, -8, 0, 0), (10, -20, 0, 0), (38, -10, 0, 0), (46, -34, 0, 0), (56, -8, 0, 0)])
a.rot("hair_b", K("hair_b", 0), K("hair_b", 10, 10, 0, 20), K("hair_b", 16, -60, 0, 60), K("hair_b", 36, -60, 0, 60), K("hair_b", 42, -10, 0, 0),
      K("hair_b", 44, -20), K("hair_b", 47, 20), K("hair_b", 52, 6), K("hair_b", 56))
a.rot("hair_b2", K("hair_b2", 0), K("hair_b2", 18, -20, 0, 20), K("hair_b2", 38, -20, 0, 20), K("hair_b2", 44, 0), K("hair_b2", 48, 16), K("hair_b2", 56))
a.rot("hair_b3", K("hair_b3", 0), K("hair_b3", 20, -14, 0, 14), K("hair_b3", 40, -14, 0, 14), K("hair_b3", 46, 0), K("hair_b3", 50, 14), K("hair_b3", 56))
for kk, s in (("hair_r", 1), ("hair_l", -1)):
    a.rot(kk, K(kk, 0), K(kk, 16, 0, 0, 60 * s), K(kk, 38, 0, 0, 60 * s), K(kk, 46, 20, 0, 0), K(kk, 56))
a.coat([(0, 0, 0, 0), (14, 20, 0, 30), (38, 20, 0, 30), (44, 4, 0, 0), (47, 20, 0, 0), (56, 0, 0, 0)])
a.hose([(0, 0, 0, 0), (16, -40, 0, 60), (38, -40, 0, 60), (44, 10, 0, 0), (47, 40, 0, 0), (56, 0, 0, 0)])
a.show("spray", 14, 38)
a.scl("tox", (0, *HIDE), (45, *HIDE), (46, 0.6, 1, 0.6), (48, 1.4, 1, 1.4), (53, 1.3, 1, 1.3), (55, *HIDE))
a.pos("tox", (0, 0, 0, 0), (46, 0, 0, 6), (56, 0, 0, 6))
a.done()

# ------------------------------------------------------------------ hair_eruption (44, enraged): flips the mane over her head and stabs it into the
#                                                                  floor t12 -> spikes race toward the target t14-t28, rips it out t32
a = A("hair_eruption", 44)
a.rot("hair_b", K("hair_b", 0), K("hair_b", 4, -20), K("hair_b", 8, -40), K("hair_b", 11, 150), K("hair_b", 13, 160), K("hair_b", 28, 160), K("hair_b", 31, 150),
      K("hair_b", 34, -20), K("hair_b", 38, 6), K("hair_b", 44))
a.rot("hair_b2", K("hair_b2", 0), K("hair_b2", 8, -10), K("hair_b2", 12, 20), K("hair_b2", 14, 10), K("hair_b2", 28, 10), K("hair_b2", 33, 30), K("hair_b2", 36, -16),
      K("hair_b2", 40, 6), K("hair_b2", 44))
a.rot("hair_b3", K("hair_b3", 0), K("hair_b3", 10, -10), K("hair_b3", 13, 10), K("hair_b3", 28, 10), K("hair_b3", 34, 30), K("hair_b3", 38, -14), K("hair_b3", 44))
for kk, s in (("hair_r", 1), ("hair_l", -1)):
    a.rot(kk, K(kk, 0), K(kk, 8, 0, 0, 20 * s), K(kk, 12, -30, 0, 0), K(kk, 28, -30, 0, 0), K(kk, 34, 10, 0, 10 * s), K(kk, 44))
for kk in ("ear_r", "ear_l"):
    a.rot(kk, K(kk, 0), K(kk, 8, 20), K(kk, 12, -30), K(kk, 28, -30), K(kk, 34, 10), K(kk, 44))
a.r("chest", (4, -16, 0, 0), (8, -22, 0, 0), (11, 40, 0, 0), (13, 46, 0, 0), (28, 44, 0, 0), (31, 40, 0, 0), (34, -18, 0, 0), (38, -6, 0, 0))
a.r("head", K("head", 4, -20), K("head", 8, -26), K("head", 11, 30), K("head", 14, 36), K("head", 28, 36), K("head", 34, -20), K("head", 38, 6, 0, 10))
a.r("arm_r", K("arm_r", 4, 30, 0, 50), K("arm_r", 8, 40, 0, 60), K("arm_r", 11, 60, 0, 20), K("arm_r", 28, 60, 0, 20), K("arm_r", 34, -10, 0, 60), K("arm_r", 38, 0, 0, 30))
a.r("arm_l", K("arm_l", 4, 30, 0, -50), K("arm_l", 8, 40, 0, -60), K("arm_l", 11, 60, 0, -20), K("arm_l", 28, 60, 0, -20), K("arm_l", 34, -10, 0, -60), K("arm_l", 38, 0, 0, -30))
a.r("fore_r", K("fore_r", 11, 60), K("fore_r", 28, 60))
a.r("fore_l", K("fore_l", 11, 10), K("fore_l", 28, 10))
a.rot("body", (0, 0, 0, 0), (4, -10, 0, 0), (8, -14, 0, 0), (11, 30, 0, 0), (13, 36, 0, 0), (28, 34, 0, 0), (31, 30, 0, 0), (34, -12, 0, 0), (38, -4, 0, 0), (44, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (8, 0, 0.6, 1.0), (11, 0, -2.4, -0.6), (28, 0, -2.4, -0.6), (34, 0, 0.4, 0.6), (44, 0, 0, 0))
legs(a, [(0, 0, 0, 2), (8, 0, 0, 6), (11, -50, 0, 8), (28, -50, 0, 8), (34, 0, 0, 4), (44, 0, 0, 2)],
     [(0, 3, 0, -3), (8, 0, 0, -6), (11, 6, 0, -8), (28, 6, 0, -8), (34, 3, 0, -4), (44, 3, 0, -3)],
     sr=[(0, 0, 0, 0), (11, 60, 0, 0), (28, 60, 0, 0), (34, 0, 0, 0)], sl=[(0, -8, 0, 0), (11, -40, 0, 0), (28, -40, 0, 0), (34, -8, 0, 0), (44, -8, 0, 0)])
a.coat([(0, 0, 0, 0), (8, -6, 0, 0), (11, 16, 0, 0), (28, 16, 0, 0), (34, -10, 0, 0), (44, 0, 0, 0)])
a.hose([(0, 0, 0, 0), (11, -30, 0, 0), (16, -10, 0, 0), (28, -10, 0, 0), (34, 20, 0, 0), (44, 0, 0, 0)])
a.lean("body", "chest", "head")
a.done()

# ------------------------------------------------------------------ hose_lasso (64, CC grab): pulls the hose out, windmills it overhead t2-t9, casts t10,
#   reels hand-over-hand (yanks t12/t15/t18), choke hold t21-t45 (squeezes t26/t33/t40), hoists t46-49, hurls t50
a = A("hose_lasso", 64)
# lasso hose: visible t1-t56, full length for the cast, shortened while reeling, coiled short during the choke
a.scl("lash", (0, *HIDE), (0.5, *HIDE), (1, 0.6, 0.6, 0.6), (3, 1, 1, 1), (10, 1, 1.15, 1), (12, 1, 0.85, 1), (15, 1, 0.65, 1), (18, 1, 0.45, 1),
      (21, 1, 0.3, 1), (45, 1, 0.3, 1), (50, 1, 0.5, 1), (54, 1, 0.5, 1), (56, *HIDE))
# spin: the whole hand turns about the arm axis while the hose sticks out sideways
a.r("hand_r", K("hand_r", 1), K("hand_r", 2, 0, 0, 0), K("hand_r", 4, 0, 180, 0), K("hand_r", 6, 0, 360, 0), K("hand_r", 8, 0, 540, 0), K("hand_r", 9, 0, 630, 0),
    K("hand_r", 10, 0, 720, 0), K("hand_r", 21, 0, 720, 0), K("hand_r", 26, 30, 720, 0), K("hand_r", 45, 30, 720, 0), K("hand_r", 50, -20, 720, 0),
    K("hand_r", 56, 0, 720, 0), K("hand_r", 64, 0, 720, 0))
a.rot("lash", (0, 0, 0, 0), (2, -70, 0, 0), (9, -80, 0, 0), (10, -6, 0, 0), (11, 6, 0, 0), (12, 30, 0, 0), (13, 10, 0, 0), (15, 34, 0, 0), (16, 12, 0, 0),
      (18, 36, 0, 0), (20, 20, 0, 0), (21, 60, 0, 0), (45, 60, 0, 0), (48, -30, 0, 0), (50, 40, 0, 0), (56, 0, 0, 0), (64, 0, 0, 0))
a.rot("lash2", (0, 0, 0, 0), (2, -20, 0, 0), (6, -26, 0, 0), (9, -20, 0, 0), (10, 4, 0, 0), (12, 20, 0, 0), (14, 10, 0, 0), (17, 24, 0, 0), (21, 50, 0, 0),
      (45, 50, 0, 0), (50, 30, 0, 0), (64, 0, 0, 0))
a.rot("lash3", (0, 0, 0, 0), (3, -24, 0, 0), (9, -20, 0, 0), (10, 2, 0, 0), (13, 26, 0, 0), (16, 14, 0, 0), (19, 30, 0, 0), (21, 60, 0, 0), (45, 60, 0, 0),
      (51, 40, 0, 0), (64, 0, 0, 0))
# right arm: overhead windmill -> whip forward cast -> three hand-over-hand yanks -> up in front for the choke -> hoist -> throw
a.r("arm_r", K("arm_r", 1, 20, 0, -10), K("arm_r", 2, 160, 0, 6), K("arm_r", 5, 170, 0, 0), K("arm_r", 8, 168, 0, 6), K("arm_r", 9, 176, 0, 10),
    K("arm_r", 10, 96, 0, -14), K("arm_r", 11, 92, 0, -16), K("arm_r", 12, 20, 0, -4), K("arm_r", 13, 80, 0, -14), K("arm_r", 15, 14, 0, -4),
    K("arm_r", 16, 80, 0, -14), K("arm_r", 18, 16, 0, -6), K("arm_r", 20, 60, 0, -20), K("arm_r", 22, 92, 0, -36), K("arm_r", 25, 90, 0, -36),
    K("arm_r", 26, 84, 0, -6), K("arm_r", 29, 90, 0, -30), K("arm_r", 33, 82, 0, -2), K("arm_r", 36, 90, 0, -30), K("arm_r", 40, 82, 0, -2),
    K("arm_r", 44, 92, 0, -30), K("arm_r", 47, 160, 0, -20), K("arm_r", 49, 166, 0, -18), K("arm_r", 50, 70, 0, -20), K("arm_r", 52, 40, 0, -24),
    K("arm_r", 58, 10, 0, -4))
a.r("fore_r", K("fore_r", 1, 70), K("fore_r", 2, 10), K("fore_r", 9, 0), K("fore_r", 10, -36), K("fore_r", 11, -30), K("fore_r", 12, 70), K("fore_r", 13, -10),
    K("fore_r", 15, 76), K("fore_r", 16, -10), K("fore_r", 18, 76), K("fore_r", 20, 40), K("fore_r", 22, -44, 0, 0), K("fore_r", 25, -44), K("fore_r", 26, -28),
    K("fore_r", 29, -44), K("fore_r", 33, -28), K("fore_r", 36, -44), K("fore_r", 40, -28), K("fore_r", 44, -44), K("fore_r", 47, 10), K("fore_r", 50, -40),
    K("fore_r", 54, -10), K("fore_r", 60, 0))
# left arm (gun hand) braces during the cast, then joins the choke from the other side
a.r("arm_l", K("arm_l", 2, -20, 0, -20), K("arm_l", 9, -24, 0, -24), K("arm_l", 10, 20, 0, -10), K("arm_l", 18, 26, 0, -12), K("arm_l", 22, 82, 0, 32),
    K("arm_l", 25, 80, 0, 32), K("arm_l", 26, 74, 0, 4), K("arm_l", 29, 80, 0, 28), K("arm_l", 33, 72, 0, 2), K("arm_l", 36, 80, 0, 28),
    K("arm_l", 40, 72, 0, 2), K("arm_l", 44, 82, 0, 28), K("arm_l", 47, 160, 0, 20), K("arm_l", 49, 166, 0, 18), K("arm_l", 50, 70, 0, 20),
    K("arm_l", 52, 40, 0, 10), K("arm_l", 58, 10, 0, 0))
a.r("fore_l", K("fore_l", 10, -10), K("fore_l", 18, -10), K("fore_l", 22, -60), K("fore_l", 26, -44), K("fore_l", 29, -60), K("fore_l", 33, -44), K("fore_l", 36, -60),
    K("fore_l", 40, -44), K("fore_l", 44, -60), K("fore_l", 47, -50), K("fore_l", 50, -90), K("fore_l", 54, -60))
a.r("gun", K("gun", 10, 20), K("gun", 22, -70, 0, -10), K("gun", 44, -70, 0, -10), K("gun", 50, -20), K("gun", 56, 30))
# torso: coil for the cast, sit back on each yank, rise up and lean back through the choke, arch + twist into the throw
a.rot("chest", (0, 0, 0, 0), (2, -10, 10, 0), (9, -12, 16, 0), (10, 14, -14, 0), (11, 16, -16, 0), (12, -14, 8, 0), (13, 6, -6, 0), (15, -16, 8, 0),
      (16, 6, -6, 0), (18, -18, 8, 0), (20, -6, 0, 0), (22, 4, 0, 0), (25, 4, 0, 0), (26, -14, 0, 0), (29, -4, 0, 0), (33, -16, 0, 0), (36, -4, 0, 0),
      (40, -18, 0, 0), (44, -6, 0, 0), (47, -26, 24, 0), (49, -28, 30, 0), (50, 22, -30, 0), (52, 26, -34, 0), (58, 4, -6, 0), (64, 0, 0, 0))
a.r("head", K("head", 2, 10, 14), K("head", 9, 12, 10), K("head", 10, -6, -10), K("head", 12, 4), K("head", 18, 6), K("head", 22, -10, 0, 0),
    K("head", 26, -18, 0, 12), K("head", 29, -12, 0, 6), K("head", 33, -20, 0, -12), K("head", 36, -12), K("head", 40, -22, 0, 14), K("head", 44, -10),
    K("head", 48, 18, 20), K("head", 50, -14, -20), K("head", 56, 6, 0, 14), K("head", 64))
a.rot("body", (0, 0, 0, 0), (2, -4, 20, 0), (9, -4, 26, 0), (10, 10, -12, 0), (11, 12, -14, 0), (12, -10, -4, 0), (15, -12, -2, 0), (18, -14, 0, 0),
      (20, -4, 0, 0), (22, -8, 0, 0), (44, -8, 0, 0), (47, -14, 30, 0), (49, -16, 36, 0), (50, 16, -34, 0), (53, 14, -40, 0), (60, 2, -6, 0), (64, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (2, 0, -0.6, 0.4), (9, 0, -0.8, 0.6), (10, 0, -1.2, -1.4), (12, 0, -1.4, 0.6), (15, 0, -1.4, 0.8), (18, 0, -1.6, 1.0),
      (21, 0, -0.6, 0.4), (24, 0, 0.4, 0.4), (44, 0, 0.4, 0.4), (47, 0, 0.8, 0.8), (49, 0, 0.8, 0.8), (50, 0, -1.6, -1.6), (53, 0, -1.4, -1.6),
      (64, 0, 0, 0))
legs(a, [(0, 0, 0, 2), (2, 10, 0, 4), (9, 10, 0, 4), (10, -34, 0, 4), (12, -24, 0, 6), (18, -28, 0, 6), (22, -14, 0, 4), (44, -14, 0, 4),
         (47, 10, 0, 4), (50, -44, 0, 4), (54, -40, 0, 4), (64, 0, 0, 2)],
     [(0, 3, 0, -3), (2, -10, 0, -4), (9, -12, 0, -4), (10, 24, 0, -4), (12, 30, 0, -6), (18, 34, 0, -6), (22, 18, 0, -4), (44, 18, 0, -4),
      (47, -14, 0, -4), (50, 30, 0, -4), (54, 26, 0, -4), (64, 3, 0, -3)],
     sr=[(0, 0, 0, 0), (10, 30, 0, 0), (12, 40, 0, 0), (18, 44, 0, 0), (22, 10, 0, 0), (44, 10, 0, 0), (50, 40, 0, 0), (54, 36, 0, 0), (64, 0, 0, 0)],
     sl=[(0, -8, 0, 0), (10, -16, 0, 0), (12, -30, 0, 0), (18, -34, 0, 0), (22, -14, 0, 0), (44, -14, 0, 0), (50, -30, 0, 0), (64, -8, 0, 0)])
a.hair([(0, 0, 0, 0), (2, -6, 0, -8), (5, -4, 0, 10), (8, -6, 0, -10), (10, 16, 0, 6), (12, -8, 0, 0), (15, 8, 0, 0), (18, -8, 0, 0), (22, 4, 0, 0),
        (26, -6, 0, 4), (33, -8, 0, -4), (40, -8, 0, 4), (47, -14, 0, 10), (50, 22, 0, -12), (54, 10, 0, -6), (64, 0, 0, 0)])
a.coat([(0, 0, 0, 0), (2, -4, 0, -6), (10, 12, 0, 6), (12, -6, 0, 0), (18, -8, 0, 0), (26, 2, 0, 0), (44, 2, 0, 0), (47, -8, 0, 8), (50, 20, 0, -10),
        (56, 4, 0, 0), (64, 0, 0, 0)])
a.hose([(0, 0, 0, 0), (2, -20, 0, 20), (6, 20, 0, -20), (10, -30, 0, 0), (14, 20, 0, 0), (18, -20, 0, 0), (24, 6, 0, 6), (40, 6, 0, -6), (47, -30, 0, 10),
        (50, 40, 0, -10), (58, -6, 0, 0), (64, 0, 0, 0)])
a.lean("body", "chest")
a.done()

# ------------------------------------------------------------------ specimen_pin (52, CC grab): crouch, leg reap + glove shove t7, knee chamber, boot stomp
#   t12 pins the victim, grinds the heel, aims the sprayer down and hoses its face t18-t34, chambers t40, punts it away t42
a = A("specimen_pin", 52)
legs(a, [(0, 0, 0, 2), (3, -20, 0, 6), (5, -30, 0, 8), (7, -10, 0, 6), (9, 96, 0, 6), (10, 104, 0, 6), (12, 48, 0, 4), (13, 44, 0, 4), (16, 48, 4, 4),
         (20, 46, -4, 4), (24, 48, 4, 4), (28, 46, -4, 4), (32, 48, 4, 4), (36, 46, 0, 4), (38, 48, 0, 4), (40, 100, 0, 4), (42, 92, 0, 2),
         (44, 86, 0, 2), (47, 20, 0, 2), (52, 0, 0, 2)],
     [(0, 3, 0, -3), (3, 20, 0, -6), (5, 46, 0, -26), (7, 54, 0, -32), (8, 30, 0, -14), (10, -10, 0, -4), (12, -26, 0, -4), (38, -26, 0, -4),
      (40, -18, 0, -4), (42, -30, 0, -4), (46, -20, 0, -3), (52, 3, 0, -3)],
     sr=[(0, 0, 0, 0), (3, 30, 0, 0), (5, 40, 0, 0), (7, 20, 0, 0), (9, -110, 0, 0), (10, -116, 0, 0), (12, -50, 0, 0), (13, -46, 0, 0), (38, -50, 0, 0),
         (40, -120, 0, 0), (42, -4, 0, 0), (44, -2, 0, 0), (47, -30, 0, 0), (52, 0, 0, 0)],
     sl=[(0, -8, 0, 0), (3, -30, 0, 0), (5, -4, 0, 0), (7, 0, 0, 0), (10, -20, 0, 0), (12, -34, 0, 0), (38, -34, 0, 0), (42, -20, 0, 0), (52, -8, 0, 0)])
a.rot("foot_r", (0, 0, 0, 0), (9, 40, 0, 0), (12, -30, 0, 0), (16, -26, 10, 0), (20, -30, -10, 0), (24, -26, 10, 0), (28, -30, -10, 0), (32, -26, 10, 0),
      (38, -30, 0, 0), (40, 30, 0, 0), (42, -40, 0, 0), (46, -10, 0, 0), (52, 0, 0, 0))
a.rot("foot_l", (0, 0, 0, 0), (5, -30, 0, 0), (7, -40, 0, 0), (10, 0, 0, 0), (52, 0, 0, 0))
a.rot("body", (0, 0, 0, 0), (3, 10, 16, 0), (5, 16, -10, 0), (7, 20, -20, 0), (9, -16, -6, 0), (10, -20, -4, 0), (12, 14, 0, 0), (13, 16, 0, 0),
      (16, 10, -10, 0), (34, 10, -10, 0), (38, 8, 0, 0), (40, -18, 0, 0), (42, -30, 0, 0), (45, -24, 0, 0), (52, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (3, 0, -2.0, 0.6), (5, 0, -2.6, -0.8), (7, 0, -2.4, -1.4), (9, 0, 0.6, -0.6), (10, 0, 0.8, -0.6), (12, 0, -1.4, -1.6),
      (13, 0, -1.8, -1.8), (38, 0, -1.4, -1.6), (40, 0, 0.4, -0.6), (42, 0, 0, 0.4), (46, 0, 0, 0.8), (52, 0, 0, 0))
a.r("chest", (3, 10, 10, 0), (5, 14, -14, 0), (7, 18, -20, 0), (9, -10, 0, 0), (10, -14, 0, 0), (12, 10, 0, 0), (13, 12, 0, 0), (16, 10, -14, 0),
    (34, 10, -14, 0), (38, 6, 0, 0), (40, -16, 0, 0), (42, -22, 0, 0), (46, -10, 0, 0))
a.r("head", K("head", 3, -10, 10), K("head", 7, -14, -14), K("head", 10, 16, 0), K("head", 12, -30, 0, 10), K("head", 16, -32, 6, 14), K("head", 22, -34, -4, 18),
    K("head", 28, -32, 6, 14), K("head", 34, -34, 0, 18), K("head", 38, -20, 0, 8), K("head", 40, -10), K("head", 42, -6, 0, -10), K("head", 47, 10, 0, 14))
# right glove shoves the victim down on the reap, then hangs ready; left (gun) aims straight down at the pinned face
a.r("arm_r", K("arm_r", 3, -30, 0, 30), K("arm_r", 5, 30, 0, 10), K("arm_r", 7, 70, 0, -10), K("arm_r", 9, 40, 0, 30), K("arm_r", 12, -20, 0, 50),
    K("arm_r", 16, 10, 0, 40), K("arm_r", 34, 10, 0, 40), K("arm_r", 40, -40, 0, 40), K("arm_r", 42, -50, 0, 50), K("arm_r", 47, 0, 0, 30))
a.r("fore_r", K("fore_r", 3, 80), K("fore_r", 7, -10), K("fore_r", 9, 20), K("fore_r", 12, 30), K("fore_r", 16, 60), K("fore_r", 34, 60), K("fore_r", 42, 20))
a.r("arm_l", K("arm_l", 3, -20, 0, -30), K("arm_l", 7, 10, 0, -40), K("arm_l", 10, 20, 0, -30), K("arm_l", 14, 60, 0, 10), K("arm_l", 16, 64, 20, 14),
    K("arm_l", 18, 66, 10, 16), K("arm_l", 34, 66, 10, 16), K("arm_l", 37, 40, 0, 0), K("arm_l", 42, 10, 0, -40), K("arm_l", 47, 10, 0, -30))
a.r("fore_l", K("fore_l", 7, 20), K("fore_l", 14, -30), K("fore_l", 18, -50), K("fore_l", 34, -50), K("fore_l", 37, -30), K("fore_l", 42, 0))
a.r("gun", K("gun", 10, 30), K("gun", 14, -60), K("gun", 18, -80), K("gun", 20, -76), K("gun", 22, -82), K("gun", 26, -76), K("gun", 30, -82),
    K("gun", 34, -78), K("gun", 37, -40), K("gun", 44, -10))
a.show("spray", 18, 35)
a.hair([(0, 0, 0, 0), (3, -6, 0, 6), (7, 10, 0, -10), (10, -12, 0, 0), (12, 16, 0, 0), (14, -8, 0, 4), (18, -6, 0, 6), (26, -8, 0, 4), (34, -6, 0, 6),
        (40, -10, 0, 0), (42, 18, 0, -6), (46, 6, 0, 0), (52, 0, 0, 0)], delay=3)
a.coat([(0, 0, 0, 0), (5, -6, 0, -8), (7, 8, 0, -12), (10, -8, 0, 0), (12, 14, 0, 0), (16, 6, 0, 0), (38, 6, 0, 0), (40, -10, 0, 0), (42, 14, 0, 0),
        (52, 0, 0, 0)])
a.hose([(0, 0, 0, 0), (7, -20, 0, 10), (12, 30, 0, 0), (16, 10, 0, 6), (34, 10, 0, -6), (42, -30, 0, 0), (52, 0, 0, 0)])
a.lean("body", "chest")
a.done()

# ------------------------------------------------------------------ glove_snatch (30, CC disarm): nozzle feint t3, glove darts in and snatches t7,
#   yanks the loot back, squirts the eyes t12, tosses the loot over her shoulder t14-15, backhand t17
a = A("glove_snatch", 30)
a.r("arm_l", K("arm_l", 2, 40, 0, 6), K("arm_l", 3, 64, 0, 14), K("arm_l", 5, 30, 0, -10), K("arm_l", 8, 20, 0, -20), K("arm_l", 10, 50, 0, 6),
    K("arm_l", 12, 76, 0, 18), K("arm_l", 14, 70, 0, 14), K("arm_l", 18, 20, 0, -20), K("arm_l", 24, 10, 0, -30))
a.r("fore_l", K("fore_l", 3, -50), K("fore_l", 5, 20), K("fore_l", 10, -20), K("fore_l", 12, -64), K("fore_l", 15, -50), K("fore_l", 20, 0))
a.r("gun", K("gun", 3, -30, 0, 20), K("gun", 6, 10), K("gun", 12, -38, 0, 24), K("gun", 15, -30, 0, 20), K("gun", 20, 0))
a.scl("spray", (0, *HIDE), (2.5, *HIDE), (3, 0.4, 0.3, 0.4), (4, *HIDE), (11, *HIDE), (12, 0.8, 0.7, 0.8), (13, 1.0, 0.9, 1.0), (14.5, *HIDE))
a.r("arm_r", K("arm_r", 2, -30, 0, 30), K("arm_r", 4, -40, 0, 36), K("arm_r", 6, 90, 0, -24), K("arm_r", 7, 100, 0, -26), K("arm_r", 9, 30, 0, -10),
    K("arm_r", 11, 20, 0, -6), K("arm_r", 13, 150, 0, 10), K("arm_r", 14, 170, 0, 20), K("arm_r", 15, 140, 0, 40), K("arm_r", 16, 80, 40, -60),
    K("arm_r", 17, 84, -20, 50), K("arm_r", 19, 80, -30, 70), K("arm_r", 24, 20, 0, 30))
a.r("fore_r", K("fore_r", 2, 90), K("fore_r", 4, 100), K("fore_r", 6, -10), K("fore_r", 7, -14), K("fore_r", 9, 90), K("fore_r", 11, 110), K("fore_r", 13, 30),
    K("fore_r", 15, -20), K("fore_r", 16, 60), K("fore_r", 17, -10), K("fore_r", 20, 10))
a.r("hand_r", K("hand_r", 5, -40), K("hand_r", 7, 40), K("hand_r", 11, 40), K("hand_r", 14, -40), K("hand_r", 16, 0, 0, -30), K("hand_r", 17, 0, 0, 30),
    K("hand_r", 22, 0))
a.rot("chest", (0, 0, 0, 0), (3, 6, -20, 0), (5, 10, 24, 0), (7, 14, 30, 0), (9, -6, -10, 0), (11, -8, -14, 0), (12, 8, -18, 0), (14, -16, 6, 0),
      (16, 4, 34, 0), (17, 10, -30, 0), (19, 8, -36, 0), (24, 2, -6, 0), (30, 0, 0, 0))
a.r("head", K("head", 3, -6, 16), K("head", 6, 6, -14), K("head", 9, 10, 0, 14), K("head", 11, 14, 10, 18), K("head", 12, -6, 10), K("head", 14, 20, 30, 10),
    K("head", 16, 0, -10), K("head", 17, -10, 20, -8), K("head", 22, 4, 0, 12))
a.rot("body", (0, 0, 0, 0), (3, 4, -14, 0), (5, 8, 16, 0), (7, 12, 20, 0), (9, -2, 0, 0), (12, 6, -10, 0), (14, -6, 10, 0), (16, 2, 24, 0),
      (17, 8, -20, 0), (20, 6, -24, 0), (30, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (3, 0, -0.4, -0.4), (5, 0, -0.8, -1.0), (7, 0, -1.2, -2.0), (9, 0, -0.6, -0.6), (12, 0, -0.8, -1.0), (14, 0, 0, -0.6),
      (17, 0, -0.8, -1.2), (22, 0, -0.4, -0.6), (30, 0, 0, 0))
legs(a, [(0, 0, 0, 2), (3, -10, 0, 2), (7, -40, 0, 4), (9, -24, 0, 3), (12, -30, 0, 3), (17, -36, 0, 4), (22, -20, 0, 3), (30, 0, 0, 2)],
     [(0, 3, 0, -3), (3, 10, 0, -3), (7, 30, 0, -4), (9, 18, 0, -3), (12, 22, 0, -3), (17, 28, 0, -4), (22, 14, 0, -3), (30, 3, 0, -3)],
     sr=[(0, 0, 0, 0), (7, 40, 0, 0), (9, 20, 0, 0), (17, 34, 0, 0), (30, 0, 0, 0)], sl=[(0, -8, 0, 0), (7, -20, 0, 0), (17, -24, 0, 0), (30, -8, 0, 0)])
a.hair([(0, 0, 0, 0), (3, -4, 0, 8), (7, 14, 0, -10), (9, -4, 0, 4), (12, 6, 0, 6), (14, -10, 0, -6), (16, 4, 0, -12), (17, 10, 0, 14), (22, -4, 0, 4),
        (30, 0, 0, 0)])
a.coat([(0, 0, 0, 0), (7, 12, 0, -8), (9, -4, 0, 4), (14, -6, 0, -4), (17, 10, 0, 10), (24, 0, 0, 0), (30, 0, 0, 0)])
a.hose([(0, 0, 0, 0), (3, -20, 0, 0), (7, 20, 0, -10), (12, -30, 0, 10), (17, 20, 0, -20), (24, -6, 0, 0), (30, 0, 0, 0)])
a.lean("body", "chest")
a.done()

# ------------------------------------------------------------------ death (40): staggers, gun slips, knees buckle, falls backward, hair spills
a = A("death", 40)
a.rot("body", (0, 0, 0, 0), (6, 10, 10, 6), (12, -10, -6, -4), (18, -16, 0, 4), (26, 6, 0, 0), (40, 6, 0, 0))
a.pos("body", (0, 0, 0, 0), (6, 0, -0.4, 0.4), (12, 0, -1.0, 0.4), (18, 0, -1.6, 0), (26, 0, 0, 0), (40, 0, 0, 0))
a.rot("root", (0, 0, 0, 0), (18, 0, 0, 0), (24, 30, 0, 6), (29, 90, 0, 8), (32, 82, 0, 8), (35, 88, 0, 8), (40, 88, 0, 8))
a.pos("root", (0, 0, 0, 0), (18, 0, 0, 0), (29, 0, 3, 0), (40, 0, 3, 0))
a.r("chest", (6, -10, 10, 0), (12, 14, -10, 0), (18, 20, 0, 0), (26, -10, 0, 0), (32, -16, 0, 0))
a.r("head", K("head", 6, 20, 10), K("head", 12, -14, -10), K("head", 18, -24), K("head", 26, 20, 20), K("head", 32, 10, 30, 10))
a.r("arm_l", K("arm_l", 6, 10, 0, -40), K("arm_l", 14, -10, 0, -60), K("arm_l", 26, 60, 0, -100), K("arm_l", 32, 80, 0, -110))
a.r("fore_l", K("fore_l", 6, 30), K("fore_l", 14, 0), K("fore_l", 32, 0))
a.r("gun", K("gun", 6, 70), K("gun", 12, 120, 0, 30), K("gun", 18, 140, 0, 60), K("gun", 40, 140, 0, 60))
a.r("arm_r", K("arm_r", 6, 40, 0, 40), K("arm_r", 14, 20, 0, 60), K("arm_r", 26, 60, 0, 100), K("arm_r", 32, 80, 0, 110))
a.r("fore_r", K("fore_r", 6, 60), K("fore_r", 14, 10), K("fore_r", 32, 0))
legs(a, [(0, 0, 0, 2), (6, -14, 0, 3), (12, 16, 0, 4), (18, 30, 0, 6), (26, 14, 0, 10), (30, 10, 0, 12), (33, 2, 0, 12), (40, 4, 0, 12)],
     [(0, 3, 0, -3), (6, 12, 0, -4), (12, -6, 0, -4), (18, 26, 0, -6), (26, 6, 0, -10), (30, 8, 0, -12), (33, -2, 0, -12), (40, 0, 0, -12)],
     sr=[(0, 0, 0, 0), (12, -20, 0, 0), (18, -50, 0, 0), (26, -30, 0, 0), (30, -6, 0, 0), (40, -10, 0, 0)],
     sl=[(0, -8, 0, 0), (12, -10, 0, 0), (18, -46, 0, 0), (26, -24, 0, 0), (30, -4, 0, 0), (40, -6, 0, 0)])
a.hair([(0, 0, 0, 0), (6, -6, 0, 10), (12, 6, 0, -10), (18, 10, 0, 0), (26, 40, 0, 10), (32, 50, 0, 6), (40, 50, 0, 6)], delay=3)
a.coat([(0, 0, 0, 0), (12, -6, 0, 0), (18, 10, 0, 0), (26, 30, 0, 0), (32, 40, 0, 0), (40, 40, 0, 0)])
a.hose([(0, 0, 0, 0), (12, 20, 0, 20), (20, -30, 0, 0), (30, 20, 0, 20), (40, 20, 0, 20)])
a.done()

m.save(OUT)
print("wrote", os.path.abspath(OUT), len(m.cubes), "cubes")
