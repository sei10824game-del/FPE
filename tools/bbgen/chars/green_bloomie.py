"""Green Bloomie (FPE Green, science teacher) - generates assets/fpe/bbmodels/green_bloomie.bbmodel.
Reference: docs/ref/confirmed/green_bloomie.jpg - tall slim figure, wild spiky black hair (tall crown spikes, a grey tuft on
her left, jagged bangs + long face-framing locks), grey gas mask with big angular white goggles and a snout respirator,
long white lab coat (grey shirt collar, black tie, buttons, pockets, ID badge on the left chest), black tights,
knee-high lime boots with pointed toes and stiletto heels, a GIANT syringe full of green liquid (left hand) and a grey
briefcase with a triangle emblem (right hand).
Blockbench space: Y up, ground 0, faces -Z. Character's RIGHT = +X.
Rotation signs (file values): arm/leg rx>0 = swing forward, torso/head rx>0 = lean back / look up,
ry>0 = turn to the character's left, rz>0 = hanging part swings toward +X (character's right).
Every key tick matches entity/characters/GreenBloomie.java.
Run: python3 tools/bbgen/chars/green_bloomie.py
"""
import math, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from bbgen import Model, mix, u  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "../../../src/main/resources/assets/fpe/bbmodels/green_bloomie.bbmodel")

# ------------------------------------------------------------------ palette
HAIR, HAIR_HI, HAIR_D = 0x1B1A20, 0x3A3944, 0x0C0C10
TUFT, TUFT_D = 0xB4B6BC, 0x7C7F86
SKIN, SKIN_D = 0xEDEBEE, 0xC9C6CE
COAT, COAT_D, COAT_L, COAT_LN = 0xF1F1EF, 0xC3C6CC, 0xFFFFFF, 0x8E9299
SHIRT, SHIRT_D = 0xA9ADB4, 0x80848C
TIE = 0x16161A
TIGHT, TIGHT_L, TIGHT_D = 0x1C1B22, 0x34333E, 0x0E0E12
GRN, GRN_D, GRN_L, GRN_DD = 0x92B654, 0x5F7D2E, 0xC1DB86, 0x3D521C
MASK, MASK_D, MASK_L, MASK_DD = 0x9DA1A8, 0x6C7078, 0xC4C7CC, 0x404349
LENS, LENS_D = 0xF4FFF2, 0xB8CCC0
GLASS, GLASS_D = 0xE6EDF0, 0xA9B4BA
LIQ, LIQ_L, LIQ_D = 0x9CCB4A, 0xD8F28E, 0x5E8A22
STEEL, STEEL_D = 0xCBCFD5, 0x7C828A
CASE, CASE_D, CASE_L, CASE_DD = 0xB7BBC2, 0x7F848C, 0xD6D9DE, 0x4C5057
PAPER, INKL = 0xFBFBF8, 0x9AA0A8
LINE = 0x15121A
TOX, TOX_L = 0x8CFF3A, 0xE8FFB0

m = Model("green_bloomie", S=8, atlas=2048)
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
            c = hi if cols[x] > 0.8 else dark if cols[x] < 0.22 else base
            for y in range(F.h):
                cc = mix(c, dark, 0.45 * abs(y / max(1, F.h - 1) - 0.3))
                if (x + y // 5) % 4 == 0 and R.random() < 0.35: cc = mix(cc, hi, 0.5)
                F.px(x, y, cc)
    return f


HS = strands()
TS = strands(TUFT, 0xDADCE0, TUFT_D)


def folds(base, dark, light, n=3, hem=True):
    def f(F):
        for i in range(n):
            x = int((i + 0.5) * F.w / n) + R.randint(-1, 1)
            for y in range(F.h):
                k = y / max(1, F.h - 1)
                F.px(x, y, mix(base, dark, 0.2 + 0.35 * k))
                F.px(x + 1, y, mix(base, light, 0.3 * k))
        if hem: F.rect(0, F.h - 2, F.w, 2, mix(base, dark, 0.45))
    return f


def outline(c):
    return lambda F: (F.rect(0, 0, F.w, 1, c), F.rect(0, F.h - 1, F.w, 1, c), F.rect(0, 0, 1, F.h, c), F.rect(F.w - 1, 0, 1, F.h, c))


def edge_dark(c, k=0.35):
    def f(F):
        for y in range(F.h):
            for x in (0, F.w - 1):
                F.px(x, y, c)
    return f


def boot(F):
    for y in range(F.h):
        for x in range(F.w):
            c = mix(GRN_L, GRN_D, (y / max(1, F.h - 1)) ** 1.3 * 0.75)
            if x < 2 or x >= F.w - 2: c = mix(c, GRN_DD, 0.4)
            F.px(x, y, c)
    F.rect(F.w // 3, 4, 2, F.h - 10, mix(GRN_L, 0xFFFFFF, 0.35))
    for y in range(8, F.h - 6, 11):  # slouchy wrinkles
        F.line(2, y, F.w - 3, y + 3, mix(GRN, GRN_DD, 0.5), 1)


def glow_fill(c1, c2, sparkle=0.25):
    def f(F):
        for y in range(F.h):
            for x in range(F.w):
                c = mix(c1, c2, y / max(1, F.h - 1))
                if R.random() < sparkle: c = mix(c, 0xFFFFFF, 0.4)
                F.px(x, y, c, glow=True)
    return f


GF = lambda a, b: (lambda fs: [glow_fill(a, b)(f) for f in fs.values()])


def face_front(F):
    W, H = F.w, F.h
    for y in range(H):
        for x in range(W):
            F.px(x, y, mix(SKIN, SKIN_D, max(0, (16 - y) / 16) * 0.7))
    F.rect(0, int(H * 0.36), W, int(H * 0.22), MASK_DD)  # shadow behind the goggle band


def coat_front(F):
    W, H = F.w, F.h  # torso front 43 x 56
    folds(COAT, COAT_D, COAT_L, 3, hem=False)(F)
    cx = W / 2
    F.poly([(cx - 9, 0), (cx, 22), (cx + 9, 0)], SHIRT)  # open collar: grey shirt
    F.poly([(cx - 5, 0), (cx, 12), (cx + 5, 0)], SHIRT_D)
    F.line(cx - 10, 0, cx - 1, 24, COAT_LN, 1.2)  # lapel edges
    F.line(cx + 10, 0, cx + 1, 24, COAT_LN, 1.2)
    F.line(cx - 1, 24, cx - 3, H, COAT_LN, 1)  # closing seam, slightly off-centre
    for y in (28, 38, 48):
        F.disc(cx - 6, y, 1.3, COAT_LN); F.px(int(cx - 6), y, COAT_D)
    F.rect(0, H - 3, W, 3, mix(COAT, COAT_D, 0.4))  # belt shadow


def glass(F):
    for y in range(F.h):
        for x in range(F.w):
            c = mix(GLASS, GLASS_D, abs(x / max(1, F.w - 1) - 0.35) * 1.2)
            F.px(x, y, c)
    F.rect(2, 0, 2, F.h, 0xFFFFFF)  # specular streak
    for y in range(4, F.h, 5):  # graduation ticks
        F.rect(F.w - 8, y, 5 if (y // 5) % 2 else 3, 1, STEEL_D)
    F.rect(0, 0, F.w, 3, MASK_DD)  # rubber plunger seal seen through the glass
    outline(GLASS_D)(F)


def liquid(F):
    for y in range(F.h):
        for x in range(F.w):
            c = mix(LIQ_L, LIQ, min(1, y / max(1, F.h - 1) * 1.3))
            if x < 2 or x >= F.w - 2: c = mix(c, LIQ_D, 0.4)
            F.px(x, y, c)
    F.rect(0, 0, F.w, 2, mix(LIQ_L, 0xFFFFFF, 0.5), glow=True)  # meniscus
    for _ in range(6):  # bubbles
        bx, by = R.randint(4, F.w - 5), R.randint(5, F.h - 4)
        F.disc(bx, by, R.choice((1.2, 1.8, 2.4)), mix(LIQ_L, 0xFFFFFF, 0.5), glow=True)
    F.rect(2, 3, 2, F.h - 6, mix(LIQ_L, 0xFFFFFF, 0.4))
    outline(LIQ_D)(F)


def lens_paint(F):
    W, H = F.w, F.h
    F.rect(0, 0, W, H, MASK_DD)
    pts = [(2, 2), (W - 2, 1), (W - 1, H - 3), (W * 0.45, H - 2), (2, H - 4)]
    F.poly(pts, LENS_D, glow=True)
    F.poly([(3, 3), (W - 3, 2.5), (W - 2.5, H - 4.5), (W * 0.45, H - 3.5), (3, H - 5)], LENS, glow=True)
    F.rect(4, 4, 3, 1, 0xFFFFFF, glow=True)


def case_side(F):
    for y in range(F.h):
        for x in range(F.w):
            c = mix(CASE_L, CASE, min(1, y / max(1, F.h - 1) * 1.2))
            F.px(x, y, c)
    outline(CASE_D)(F)
    F.rect(0, 3, F.w, 1, CASE_D)


def case_emblem(F):
    case_side(F)
    W, H = F.w, F.h
    cx, cy = W / 2, H / 2 + 3
    s = min(W, H) * 0.32
    for t in range(2):  # outlined triangle with a cross-bar (lab hazard / alchemy sign)
        F.line(cx - s, cy + s * 0.8, cx + s, cy + s * 0.8, CASE_DD, 2)
        F.line(cx - s, cy + s * 0.8, cx, cy - s, CASE_DD, 2)
        F.line(cx + s, cy + s * 0.8, cx, cy - s, CASE_DD, 2)
    F.line(cx - s * 0.75, cy + s * 0.1, cx + s * 0.75, cy + s * 0.1, CASE_DD, 2)
    F.rect(W - 9, 6, 6, 3, CASE_DD)  # label plate


def badge_paint(F):
    F.rect(0, 0, F.w, F.h, PAPER)
    F.rect(2, 3, 6, 7, INKL)
    F.rect(10, 3, 5, 1, INKL); F.rect(10, 6, 4, 1, INKL); F.rect(10, 9, 5, 1, INKL)
    F.rect(0, 0, F.w, 2, GRN)
    outline(COAT_LN)(F)


# ------------------------------------------------------------------ skeleton
m.group("root", (0, 0, 0))
m.group("body", (0, 16.5, 0), parent="root")
m.group("coat_b", (0, 18.6, 2.0), parent="body")
m.group("coat_b2", (0, 14.8, 2.3), parent="coat_b")
m.group("coat_fr", (1.6, 18.6, -2.0), parent="body")
m.group("coat_fl", (-1.6, 18.6, -2.0), parent="body")
m.group("coat_sr", (3.0, 18.6, 0.2), parent="body")
m.group("coat_sl", (-3.0, 18.6, 0.2), parent="body")
m.group("chest", (0, 19.2, 0), parent="body")
m.group("badge", (-1.6, 24.4, -2.0), parent="chest")
m.group("tie", (0, 26.2, -2.0), parent="chest")
m.group("head", (0, 27.6, 0), parent="chest")
m.group("mask", (0, 30.0, -3.4), parent="head")
m.group("gas", (0, 29.2, -5.0), parent="head")
m.group("bangs", (0, 34.4, -3.4), parent="head")
m.group("hair_top", (0, 35.0, 0.2), parent="head")
m.group("tuft", (-2.6, 35.0, 0.4), parent="head")
m.group("hair_b", (0, 33.6, 2.8), parent="head")
m.group("hair_r", (3.5, 33.2, 0.0), parent="head")
m.group("hair_l", (-3.5, 33.2, 0.0), parent="head")
for s, k in ((1, "r"), (-1, "l")):
    m.group("arm_" + k, (3.85 * s, 26.0, 0), parent="chest")
    m.group("fore_" + k, (3.85 * s, 22.3, 0), parent="arm_" + k)
    m.group("hand_" + k, (3.85 * s, 18.7, 0), parent="fore_" + k)
    m.group("leg_" + k, (1.2 * s, 16.0, 0), parent="root")
    m.group("shin_" + k, (1.2 * s, 10.2, 0), parent="leg_" + k)
    m.group("foot_" + k, (1.2 * s, 2.0, 0.3), parent="shin_" + k)
m.group("syr", (-3.85, 17.4, 0), parent="hand_l")
m.group("plunger", (-3.85, 17.8, 0), parent="syr")
m.group("liquid", (-3.85, 6.4, 0), parent="syr")
m.group("drip", (-3.85, -1.6, 0), parent="syr")
m.group("case", (3.85, 17.4, 0), parent="hand_r")
m.group("lid", (4.6, 9.4, 0), parent="case")
m.group("flask", (4.0, 12.6, 0), parent="case")

# ------------------------------------------------------------------ legs: thin black tights, lime knee boots, pointed toes, stilettos
for s, k in ((1, "r"), (-1, "l")):
    x = 1.2 * s
    m.cube("thigh_" + k, "leg_" + k, (x - 1.0, 9.8, -1.0), (x + 1.0, 16.4, 1.0), TIGHT_L, color2=TIGHT, grad=True)
    m.cube("knee_" + k, "shin_" + k, (x - 0.9, 9.4, -0.95), (x + 0.9, 10.6, 0.95), TIGHT)
    m.cube("boot_" + k, "shin_" + k, (x - 1.05, 2.0, -1.1), (x + 1.05, 8.6, 1.1), GRN, faces=all_faces(boot, ("up", "down")))
    m.cube("bcuff_" + k, "shin_" + k, (x - 1.4, 7.6, -1.45), (x + 1.4, 9.4, 1.45), GRN_L, color2=GRN, grad=True,
           faces={"north": lambda F: (F.rect(0, F.h - 2, F.w, 2, GRN_D), F.line(3, 0, 8, F.h - 1, GRN_D, 1)),
                  "east": lambda F: F.line(2, 0, 6, F.h - 1, GRN_D, 1), "west": lambda F: F.line(F.w - 3, 0, F.w - 7, F.h - 1, GRN_D, 1)})
    m.cube("bfold_" + k, "shin_" + k, (x - 1.5, 9.0, -1.55), (x + 1.5, 9.7, 1.55), GRN_D, origin=(x, 9.3, 0), rot=(4, 0, 3 * s))
    m.cube("bflap_" + k, "shin_" + k, (x - 0.9, 8.6, -1.8), (x + 0.9, 10.6, -1.3), GRN_L, color2=GRN, grad=True, origin=(x, 9.4, -1.5), rot=(-12, 0, 0))
    m.cube("ankle_" + k, "foot_" + k, (x - 0.95, 1.4, -1.0), (x + 0.95, 2.6, 1.05), GRN, color2=GRN_D, grad=True)
    m.cube("foot_" + k, "foot_" + k, (x - 0.9, 0.3, -2.6), (x + 0.9, 1.9, 0.4), GRN, color2=GRN_D, grad=True, origin=(x, 1.0, -1), rot=(-8, 0, 0))
    m.cube("toe_" + k, "foot_" + k, (x - 0.55, 0.0, -3.9), (x + 0.55, 1.0, -2.3), GRN_L, color2=GRN, grad=True)
    m.cube("toetip_" + k, "foot_" + k, (x - 0.3, 0.0, -4.5), (x + 0.3, 0.6, -3.7), GRN_D)
    m.cube("heel_" + k, "foot_" + k, (x - 0.35, 0.0, 0.5), (x + 0.35, 1.6, 1.2), GRN_DD, origin=(x, 1.2, 0.85), rot=(10, 0, 0))
    m.cube("sole_" + k, "foot_" + k, (x - 0.85, 0.0, -2.4), (x + 0.85, 0.35, -0.6), GRN_DD)

# ------------------------------------------------------------------ hips + long lab-coat tails
m.cube("hips", "body", (-2.5, 15.4, -1.6), (2.5, 19.4, 1.6), TIGHT, color2=TIGHT_D, grad=True)
m.cube("belt", "body", (-2.75, 18.4, -1.85), (2.75, 19.3, 1.85), COAT_D, color2=COAT, grad=True)
m.cube("cb_up", "coat_b", (-3.0, 14.6, 1.8), (3.0, 19.0, 2.4), COAT, color2=COAT_D, grad=True, faces={"south": folds(COAT, COAT_D, COAT_L, 3, False)})
m.cube("cb_lo", "coat_b2", (-3.2, 12.6, 2.05), (3.2, 15.0, 2.65), COAT, color2=COAT_D, grad=True,
       faces={"south": combo(folds(COAT, COAT_D, COAT_L, 3), lambda F: F.rect(F.w // 2, 0, 1, F.h, COAT_LN))})
m.cube("cb_belt", "coat_b", (-1.6, 17.6, 2.3), (1.6, 18.3, 2.6), COAT_D, faces={"south": lambda F: (F.disc(3, 3, 1.4, COAT_LN), F.disc(F.w - 4, 3, 1.4, COAT_LN))})
for s, k in ((1, "r"), (-1, "l")):
    x0, x1 = (-0.35, 3.1) if s > 0 else (-3.1, 0.35)
    m.cube("cf_" + k, "coat_f" + k, (x0, 13.4, -2.3 - (0.06 if s < 0 else 0)), (x1, 19.2, -1.7), COAT, color2=COAT_D, grad=True,
           origin=(1.6 * s, 18.6, -2.0), rot=(3, 0, 3 * s),
           faces={"north": combo(folds(COAT, COAT_D, COAT_L, 2),
                                 (lambda F: F.rect(0, 0, 1, F.h, COAT_LN)) if s < 0 else (lambda F: F.rect(F.w - 1, 0, 1, F.h, COAT_LN)))})
    m.cube("pocket_" + k, "coat_f" + k, (x0 + 0.5 * (1 if s > 0 else 0.6), 14.4, -2.45), (x1 - 0.5 * (0.6 if s > 0 else 1), 16.4, -2.25), COAT_L,
           origin=(1.6 * s, 18.6, -2.0), rot=(3, 0, 3 * s), faces={"north": combo(lambda F: F.rect(0, 0, F.w, 2, COAT_LN), outline(COAT_D))})
    m.cube("cs_" + k, "coat_s" + k, (3.0 * s - 0.3, 13.6, -1.8), (3.0 * s + 0.3, 19.2, 2.2), COAT, color2=COAT_D, grad=True,
           origin=(3.0 * s, 18.6, 0.2), rot=(0, 0, 5 * s), faces={"east": folds(COAT, COAT_D, COAT_L, 2), "west": folds(COAT, COAT_D, COAT_L, 2)})

# ------------------------------------------------------------------ torso: coat, collar + lapels, shirt + tie, badge
m.cube("torso", "chest", (-2.7, 19.2, -1.6), (2.7, 26.2, 1.6), COAT, color2=COAT_D, grad=True,
       faces={"north": coat_front, "south": folds(COAT, COAT_D, COAT_L, 3, False)})
for s, k in ((1, "r"), (-1, "l")):
    x0, x1 = (0.9, 2.9) if s > 0 else (-2.9, -0.9)
    m.cube("lapel_" + k, "chest", (x0, 22.6, -2.0), (x1, 26.4, -1.55), COAT_L, color2=COAT, grad=True,
           origin=((x0 + x1) / 2, 26, -1.8), rot=(0, 0, -10 * s), faces={"north": lambda F: (F.rect(0, 0, 1, F.h, COAT_LN), F.rect(F.w - 1, 0, 1, F.h, COAT_D))})
    m.cube("collar_" + k, "chest", (0.5 * s if s > 0 else -2.9, 25.6, -2.0), (2.9 if s > 0 else -0.5, 27.4, 1.9), COAT_L, color2=COAT, grad=True,
           origin=(1.6 * s, 26.4, 0), rot=(0, 0, 16 * s), faces={"north": lambda F: F.rect(0, F.h - 1, F.w, 1, COAT_LN)})
    m.cube("sh_coll_" + k, "chest", (0.15 * s if s > 0 else -1.3, 26.0, -1.75), (1.3 if s > 0 else -0.15, 26.9, -1.3), SHIRT, origin=(0.6 * s, 26.4, -1.5), rot=(0, 0, -25 * s))
m.cube("neck", "chest", (-0.85, 26.0, -0.8), (0.85, 27.9, 0.8), SKIN_D, color2=SKIN, grad=True)
m.cube("tie_knot", "tie", (-0.45, 25.4, -2.0), (0.45, 26.2, -1.6), TIE)
m.cube("tie_blade", "tie", (-0.5, 21.6, -1.95), (0.5, 25.5, -1.6), TIE, faces={"north": lambda F: F.rect(1, 3, F.w - 2, 1, HAIR_HI)})
m.cube("tie_tip", "tie", (-0.35, 21.0, -1.95), (0.35, 21.7, -1.6), TIE, origin=(0, 21.6, -1.8), rot=(0, 0, 45))
m.cube("pocket_c", "chest", (-2.5, 22.2, -1.8), (-0.8, 23.8, -1.55), COAT_L, faces={"north": combo(lambda F: F.rect(0, 0, F.w, 2, COAT_LN), outline(COAT_D))})
m.cube("pen", "chest", (-2.2, 23.2, -1.9), (-1.9, 24.6, -1.6), GRN_D)
m.cube("id_clip", "badge", (-0.25, 23.8, -2.0), (0.25, 24.6, -1.7), STEEL)
m.cube("id_card", "badge", (-1.0, 21.6, -2.05), (1.0, 24.0, -1.8), PAPER, origin=(-1.6, 24.4, -2.0), rot=(0, 0, 4), faces={"north": badge_paint})

# ------------------------------------------------------------------ head: skull, gas mask + goggles, spiky black hair
m.cube("skull", "head", (-3.3, 27.6, -3.2), (3.3, 34.4, 3.2), SKIN, faces={"north": face_front, "up": lambda F: F.rect(0, 0, F.w, F.h, HAIR_D)})
m.cube("strap", "mask", (-3.45, 30.6, -3.35), (3.45, 31.4, 3.35), TIE)
m.cube("strap_lo", "mask", (-3.42, 28.6, -2.0), (3.42, 29.2, 3.3), TIE, origin=(0, 28.9, 0), rot=(14, 0, 0))
m.cube("gog_band", "mask", (-3.35, 30.3, -3.75), (3.35, 32.6, -3.2), MASK, color2=MASK_D, grad=True, faces={"north": outline(MASK_DD)})
for s, k in ((1, "r"), (-1, "l")):
    m.cube("lens_" + k, "mask", (1.65 * s - 1.45, 30.2, -4.15), (1.65 * s + 1.45, 32.6, -3.6), LENS, origin=(1.65 * s, 31.4, -3.9), rot=(0, -10 * s, 0),
           faces={"north": lens_paint if s > 0 else (lambda F: (lens_paint(F)))})
    m.cube("lrim_" + k, "mask", (1.65 * s - 1.65, 32.4, -4.25), (1.65 * s + 1.65, 32.9, -3.5), MASK_DD, origin=(1.65 * s, 31.4, -3.9), rot=(0, -10 * s, -6 * s))
    m.cube("cheek_" + k, "mask", (1.0 * s - 1.0, 27.7, -3.85), (1.0 * s + 1.0, 30.4, -3.25), MASK, color2=MASK_D, grad=True,
           origin=(1.2 * s, 29, -3.5), rot=(0, 24 * s, 0), faces={"north": outline(MASK_D)})
    m.cube("filter_" + k, "mask", (2.3 * s - 0.75, 28.0, -4.3), (2.3 * s + 0.75, 29.6, -3.4), MASK_DD, origin=(2.3 * s, 28.8, -3.8), rot=(0, 34 * s, 0),
           faces={"north": lambda F: (F.disc(F.w / 2, F.h / 2, F.w / 2 - 1, MASK_D), F.disc(F.w / 2, F.h / 2, 2, MASK_DD))})
m.cube("snout", "mask", (-1.3, 27.6, -4.4), (1.3, 30.4, -3.4), MASK, color2=MASK_D, grad=True, faces={"north": outline(MASK_D)})
m.cube("snout_tip", "mask", (-0.95, 28.0, -5.0), (0.95, 30.0, -4.35), MASK_L, color2=MASK, grad=True,
       faces={"north": lambda F: (outline(MASK_DD)(F), [F.rect(2, y, F.w - 4, 1, MASK_DD) for y in range(3, F.h - 2, 3)])})
m.cube("nose_ridge", "mask", (-0.45, 30.1, -4.1), (0.45, 31.0, -3.6), MASK_D)
# hair: cap + crown spikes + tuft + bangs + face-framing locks + back spikes
m.cube("hair_cap", "head", (-3.6, 33.4, -3.5), (3.6, 35.4, 3.6), HAIR, faces=all_faces(HS))
m.cube("hair_cap2", "head", (-3.1, 35.2, -2.8), (3.1, 36.2, 3.0), HAIR, faces=all_faces(HS))
for i, (x, z, h, rx, rz, w) in enumerate([(0.0, 0.0, 6.4, -6, 4, 2.2), (-1.6, -0.6, 5.6, 4, 26, 2.0), (1.5, -0.4, 5.8, -2, -24, 2.0),
                                          (2.6, 0.6, 4.4, -8, -48, 1.9), (-2.7, 0.8, 4.6, -6, 44, 1.9), (0.8, 1.6, 5.0, -30, -12, 2.0),
                                          (-0.9, 1.8, 4.8, -32, 16, 2.0), (0.1, 2.6, 4.2, -55, 4, 1.9), (-0.2, -1.6, 3.0, 24, -6, 1.8)]):
    c = HAIR_D if i % 3 == 1 else HAIR
    org = (x, 35.4, z)
    m.cube(f"spk{i}", "hair_top", (x - w / 2, 35.2, z - w / 2), (x + w / 2, 35.2 + h * 0.6, z + w / 2), c, origin=org, rot=(rx, 0, rz), faces=all_faces(HS))
    m.cube(f"spkt{i}", "hair_top", (x - w * 0.28, 35.0 + h * 0.55, z - w * 0.28), (x + w * 0.28, 35.2 + h, z + w * 0.28), HAIR_HI if i % 2 else c,
           origin=org, rot=(rx, 0, rz), faces=all_faces(HS))
m.cube("tuft_a", "tuft", (-3.4, 34.6, -0.4), (-2.0, 38.2, 1.2), TUFT, origin=(-2.6, 35.0, 0.4), rot=(0, 0, 30), faces=all_faces(TS))
m.cube("tuft_b", "tuft", (-3.0, 37.8, 0.0), (-2.3, 39.4, 0.8), TUFT_D, origin=(-2.6, 35.0, 0.4), rot=(0, 0, 38), faces=all_faces(TS))
for i, (x, ln, rz) in enumerate([(-3.0, 3.0, 14), (-2.0, 2.0, -8), (-1.0, 3.0, 10), (0.0, 2.2, -12), (1.0, 3.2, 8), (2.0, 2.0, -10), (3.0, 3.0, -16)]):
    m.cube(f"bang{i}", "bangs", (x - 0.65, 34.3 - ln, -3.95 - (i % 2) * 0.15), (x + 0.65, 34.5, -3.45), HAIR if i % 2 else HAIR_D,
           origin=(x, 34.3, -3.7), rot=(6, 0, rz), faces=all_faces(HS))
    m.cube(f"bangt{i}", "bangs", (x - 0.3, 34.3 - ln - 1.0, -3.95), (x + 0.3, 34.3 - ln + 0.2, -3.55), HAIR_D,
           origin=(x, 34.3, -3.7), rot=(6, 0, rz))
m.cube("hb_main", "hair_b", (-3.7, 27.2, 2.0), (3.7, 33.8, 4.0), HAIR, faces=all_faces(HS))
for i in range(8):
    x = -3.4 + i * 0.97
    ln = 2.4 + (i % 3) * 1.2 + R.uniform(0, 0.8)
    m.cube(f"hb_tip{i}", "hair_b", (x - 0.5, 27.4 - ln, 2.3 + (i % 2) * 0.4), (x + 0.5, 27.8, 3.7 + (i % 2) * 0.4), HAIR if i % 2 else HAIR_D,
           origin=(x, 27.6, 3.0), rot=(-18, 0, (i - 3.5) * 10), faces=all_faces(HS))
for i in range(5):
    m.cube(f"hb_spk{i}", "hair_b", (-0.6 + (i - 2) * 1.4, 31.0, 3.0), (0.6 + (i - 2) * 1.4, 34.6, 4.2), HAIR_D if i % 2 else HAIR,
           origin=((i - 2) * 1.4, 32.0, 3.6), rot=(-55, 0, (i - 2) * 16), faces=all_faces(HS))
for s, k in ((1, "r"), (-1, "l")):
    m.cube("hs_main_" + k, "hair_" + k, (3.4 * s - 0.6, 28.4, -2.4), (3.4 * s + 0.6, 33.6, 2.6), HAIR, faces=all_faces(HS))
    for i, (z, ln, rx) in enumerate([(-2.9, 6.6, 6), (-2.0, 5.2, 2), (0.0, 4.2, -6), (1.8, 4.6, -10)]):  # long face-framing locks
        m.cube(f"hs_lock{i}_" + k, "hair_" + k, (3.6 * s - 0.5, 33.2 - ln, z - 0.5), (3.6 * s + 0.5, 33.2, z + 0.5), HAIR_HI if i == 1 else HAIR_D if i == 3 else HAIR,
               origin=(3.6 * s, 33.2, z), rot=(rx, 0, (6 + i * 4) * s), faces=all_faces(HS))
        m.cube(f"hs_ltip{i}_" + k, "hair_" + k, (3.6 * s - 0.25, 33.2 - ln - 1.2, z - 0.25), (3.6 * s + 0.25, 33.2 - ln + 0.2, z + 0.25), HAIR_D,
               origin=(3.6 * s, 33.2, z), rot=(rx, 0, (6 + i * 4) * s))
    for i in range(3):  # spikes sticking out sideways (wild silhouette)
        y = 34.2 - i * 1.7
        m.cube(f"hs_flick{i}_" + k, "hair_" + k, (3.9 * s - 0.45, y - 0.2, -0.45 + i * 0.9), (3.9 * s + 0.45, y + 2.6 - i * 0.5, 0.45 + i * 0.9), HAIR_D if i % 2 else HAIR,
               origin=(3.9 * s, y, i * 0.9), rot=(0, 0, -(30 + i * 22) * s), faces=all_faces(HS))
# toxic gas puffs out of the respirator (gas_vent / overdose only)
for i, (x, y, z, r) in enumerate([(0, 29.2, -6.0, 1.4), (-1.2, 30.4, -7.4, 1.8), (1.3, 28.4, -8.0, 2.0)]):
    m.cube(f"gas{i}", "gas", (x - r, y - r, z - r), (x + r, y + r, z + r), TOX, glow=True, origin=(x, y, z), rot=(i * 20, i * 35, 0), paint=GF(TOX_L, TOX))

# ------------------------------------------------------------------ arms: lab-coat sleeves, cuffs, pale hands
for s, k in ((1, "r"), (-1, "l")):
    x = 3.85 * s
    m.cube("shoulder_" + k, "arm_" + k, (x - 1.2, 24.0, -1.3), (x + 1.2, 26.6, 1.3), COAT, color2=COAT_D, grad=True, origin=(x, 25.8, 0), rot=(0, 0, 6 * s))
    m.cube("sleeve_" + k, "arm_" + k, (x - 1.0, 22.0, -1.05), (x + 1.0, 25.0, 1.05), COAT, color2=COAT_D, grad=True, faces={"north": folds(COAT, COAT_D, COAT_L, 2, False)})
    m.cube("elbow_" + k, "fore_" + k, (x - 0.95, 21.6, -1.0), (x + 0.95, 22.8, 1.0), COAT_D)
    m.cube("forearm_" + k, "fore_" + k, (x - 1.05, 19.4, -1.1), (x + 1.05, 22.2, 1.1), COAT, color2=COAT_D, grad=True, faces={"north": folds(COAT, COAT_D, COAT_L, 2, False)})
    m.cube("cuff_" + k, "fore_" + k, (x - 1.25, 18.6, -1.3), (x + 1.25, 19.8, 1.3), COAT_L, color2=COAT_D, grad=True,
           faces={"north": lambda F: (F.rect(0, 0, F.w, 1, COAT_LN), F.disc(F.w - 4, F.h / 2, 1.2, COAT_LN))})
    m.cube("palm_" + k, "hand_" + k, (x - 0.85, 16.4, -0.9), (x + 0.85, 18.8, 0.9), SKIN, color2=SKIN_D, grad=True)
    m.cube("fist_" + k, "hand_" + k, (x - 0.95, 16.2, -1.15), (x + 0.95, 17.4, -0.5), SKIN_D)
    m.cube("thumb_" + k, "hand_" + k, (x - 1.1 * s - 0.35, 16.8, -1.0), (x - 1.1 * s + 0.35, 18.2, -0.2), SKIN, origin=(x - 0.8 * s, 18, -0.6), rot=(0, 0, 12 * s))

# ------------------------------------------------------------------ GIANT syringe (left hand): pad, rod, flange, glass barrel, green liquid, hub, needle
SX = -3.85
_syr0 = len(m.cubes)
m.cube("pad", "plunger", (SX - 1.7, 24.2, -1.7), (SX + 1.7, 24.8, 1.7), STEEL, color2=STEEL_D, grad=True, faces={"up": lambda F: (outline(STEEL_D)(F), F.disc(F.w / 2, F.h / 2, 4, STEEL_D))})
m.cube("rod", "plunger", (SX - 0.45, 17.8, -0.45), (SX + 0.45, 24.3, 0.45), STEEL, faces=all_faces(lambda F: F.rect(0, 0, 2, F.h, 0xFFFFFF)))
m.cube("rod_x", "plunger", (SX - 0.9, 18.4, -0.15), (SX + 0.9, 24.1, 0.15), STEEL_D)  # cross-shaped rod fins
m.cube("rod_z", "plunger", (SX - 0.15, 18.4, -0.9), (SX + 0.15, 24.1, 0.9), STEEL_D)
m.cube("flange", "syr", (SX - 3.0, 17.5, -0.85), (SX + 3.0, 18.2, 0.85), STEEL, color2=STEEL_D, grad=True, faces={"north": outline(STEEL_D)})
m.cube("collar_s", "syr", (SX - 1.75, 16.8, -1.75), (SX + 1.75, 17.6, 1.75), STEEL_D)
m.cube("barrel", "syr", (SX - 1.5, 11.8, -1.5), (SX + 1.5, 16.9, 1.5), GLASS, faces=all_faces(glass, ("up", "down")))
m.cube("liq", "liquid", (SX - 1.5, 6.4, -1.5), (SX + 1.5, 11.85, 1.5), LIQ, faces=all_faces(liquid, ("down",)))
m.cube("tip_cap", "syr", (SX - 1.6, 5.4, -1.6), (SX + 1.6, 6.5, 1.6), STEEL, color2=STEEL_D, grad=True)
m.cube("hub", "syr", (SX - 0.9, 4.2, -0.9), (SX + 0.9, 5.5, 0.9), GLASS_D, color2=STEEL_D, grad=True)
m.cube("hub2", "syr", (SX - 0.5, 3.4, -0.5), (SX + 0.5, 4.3, 0.5), STEEL_D)
m.cube("needle", "syr", (SX - 0.2, -1.6, -0.2), (SX + 0.2, 3.5, 0.2), STEEL, faces=all_faces(lambda F: F.rect(0, 0, 1, F.h, 0xFFFFFF)))
m.cube("drop", "drip", (SX - 0.35, -2.6, -0.35), (SX + 0.35, -1.6, 0.35), LIQ_L, glow=True, paint=GF(LIQ_L, LIQ))
# syringe axis sits just in front of the fist (gripped at the knuckles) so the plunger never hides inside the forearm
SZ = -1.25
for c in m.cubes[_syr0:]:
    c["from"][2] += SZ; c["to"][2] += SZ; c["origin"][2] += SZ
for g in ("plunger", "liquid", "drip"):
    m.groups[g]["origin"][2] += SZ

# ------------------------------------------------------------------ briefcase (right hand): shell + lid, handle, latches, triangle emblem, flask inside
CX = 4.0
m.cube("handle", "case", (CX - 0.3, 16.4, -1.2), (CX + 0.3, 16.9, 1.2), CASE_DD)
m.cube("handle_f", "case", (CX - 0.3, 15.6, -1.4), (CX + 0.3, 16.9, -0.9), CASE_DD)
m.cube("handle_b", "case", (CX - 0.3, 15.6, 0.9), (CX + 0.3, 16.9, 1.4), CASE_DD)
m.cube("shell", "case", (CX - 0.9, 9.4, -3.6), (CX + 0.6, 15.7, 3.6), CASE, faces={"west": case_side, "north": case_side, "south": case_side})
m.cube("lidc", "lid", (CX + 0.55, 9.4, -3.6), (CX + 1.0, 15.7, 3.6), CASE, faces={"east": case_emblem})
m.cube("latch_f", "lid", (CX + 0.4, 15.0, -2.6), (CX + 1.15, 15.9, -1.8), STEEL_D)
m.cube("latch_b", "lid", (CX + 0.4, 15.0, 1.8), (CX + 1.15, 15.9, 2.6), STEEL_D)
m.cube("rim", "case", (CX - 1.0, 15.4, -3.7), (CX + 1.1, 15.8, 3.7), CASE_D)
for z in (-3.7, 3.3):
    m.cube(f"corner{int(z)}", "case", (CX - 1.0, 9.3, z), (CX + 1.1, 10.0, z + 0.4), CASE_DD)
m.cube("flask_b", "flask", (CX - 0.7, 10.4, -0.9), (CX + 0.5, 12.6, 0.9), TOX, glow=True, paint=GF(TOX_L, TOX))
m.cube("flask_n", "flask", (CX - 0.4, 12.6, -0.35), (CX + 0.2, 13.8, 0.35), GLASS)
m.cube("flask_c", "flask", (CX - 0.45, 13.8, -0.45), (CX + 0.25, 14.3, 0.45), CASE_DD)
# knockout gas billowing out of the opened briefcase (knockout_gas only); +X local = out of the lid side
m.group("case_gas", (CX + 1.0, 12.6, 0), parent="case")
for i, (x, y, z, r) in enumerate([(CX + 2.0, 12.6, 0.0, 1.1), (CX + 3.8, 13.2, -0.8, 1.6), (CX + 6.2, 12.4, 0.7, 2.1), (CX + 8.8, 13.4, -0.4, 2.5)]):
    m.cube(f"kgas{i}", "case_gas", (x - r, y - r, z - r), (x + r, y + r, z + r), TOX_L, glow=True, origin=(x, y, z), rot=(i * 25, i * 40, i * 15),
           paint=GF(0xF4FFE0, TOX_L))
# the same briefcase dropped on the floor at her right foot (specimen_grab frees her hand); a copy of the hand case's cubes
m.group("case_drop", (6.5, 0, -1.5), parent="root")
_DROP = (2.5, -9.3, -1.5)
for c in [c for c in m.cubes if c["name"] in ("handle", "handle_f", "handle_b", "shell", "lidc", "latch_f", "latch_b", "rim", "corner-3", "corner3")]:
    d = {**c, "uuid": u(), "name": c["name"] + "_drop",
         "from": [c["from"][i] + _DROP[i] for i in range(3)], "to": [c["to"][i] + _DROP[i] for i in range(3)],
         "origin": [c["origin"][i] + _DROP[i] for i in range(3)]}
    m.cubes.append(d)
    m.groups["case_drop"]["children"].append(d["uuid"])


# ================================================================== animation
PROPS = ["gas", "flask", "case_gas", "case_drop"]
HIDE = (.001, .001, .001)

REST = {
    "arm_r": (-2, 0, 10), "fore_r": (8, 0, 0), "hand_r": (0, 0, 0), "case": (-6, 0, -10),
    "arm_l": (6, 0, -14), "fore_l": (20, 0, 0), "hand_l": (0, 0, 0), "syr": (8, 0, -8),
    "head": (2, 0, -4), "chest": (0, 0, 0),
    "leg_r": (0, 0, 2), "leg_l": (0, 0, -2),
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

    def show(self, bone, t0, t1):
        keys = [(0, *HIDE)] if t0 > 0 else []
        if t0 > 0: keys.append((t0 - 1, *HIDE))
        keys += [(t0, 1, 1, 1), (t0 + 1, 1.15, 1.15, 1.15), (t0 + 2, 1, 1, 1)]
        if t1 < self.ticks: keys += [(t1, 1, 1, 1), (t1 + 1.5, *HIDE)]
        return self.scl(bone, *keys)

    def puff(self, t0, t1):
        """gas cloud from the respirator: grows from nothing, drifts forward, fades"""
        self.scl("gas", (0, *HIDE), (t0 - 1, *HIDE), (t0, 0.4, 0.4, 0.4), (t0 + 2, 0.8, 0.8, 0.8), (t1 - 2, 1.0, 1.0, 1.0), (t1, *HIDE))
        self.pos("gas", (0, 0, 0, 0), (t0, 0, 0, 0), (t1, 0, 1.5, -3.0))

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
        """x>0 = hair flicks forward, z>0 = flicks toward +X"""
        self.drape(["hair_b"], [(t, x * 0.7, 0, z * 0.6) for (t, x, y, z) in keys], delay=delay)
        self.drape(["hair_r"], [(t, x * 0.5, 0, z * 0.7 + max(0, -x) * 0.2) for (t, x, y, z) in keys], delay=delay)
        self.drape(["hair_l"], [(t, x * 0.5, 0, z * 0.7 - max(0, -x) * 0.2) for (t, x, y, z) in keys], delay=delay)
        self.drape(["bangs"], [(t, x * 0.3, 0, z * 0.3) for (t, x, y, z) in keys], delay=delay)
        self.drape(["hair_top"], [(t, x * 0.25, 0, z * 0.3) for (t, x, y, z) in keys], delay=delay + 1)
        self.drape(["tuft"], [(t, x * 0.4, 0, z * 0.5) for (t, x, y, z) in keys], delay=delay + 1)
        self.drape(["badge"], [(t, -x * 0.8, 0, z * 0.8) for (t, x, y, z) in keys], delay=delay)
        self.drape(["tie"], [(t, -x * 0.6, 0, z * 0.6) for (t, x, y, z) in keys], delay=delay)
        return self

    def coat(self, keys, delay=2):
        """x>0 = front tails kick forward (back tail lifts back), z>0 = flares toward +X"""
        self.drape(["coat_b", "coat_b2"], [(t, -x * 0.8, 0, z * 0.5) for (t, x, y, z) in keys], delay=delay, gain=0.9)
        self.drape(["coat_fr"], [(t, x, 0, z * 0.6 + abs(z) * 0.3) for (t, x, y, z) in keys], delay=delay)
        self.drape(["coat_fl"], [(t, x, 0, z * 0.6 - abs(z) * 0.3) for (t, x, y, z) in keys], delay=delay)
        self.drape(["coat_sr"], [(t, x * 0.3, 0, z + abs(x) * 0.2) for (t, x, y, z) in keys], delay=delay)
        self.drape(["coat_sl"], [(t, x * 0.3, 0, z - abs(x) * 0.2) for (t, x, y, z) in keys], delay=delay)
        return self

    def plant(self):
        """keep the supporting boot on the ground: lower root by the smaller foot lift (thigh 5.8 + shin 8.2 px),
        and give back the same amount from any authored body dip so the hips do not sink into the thighs."""
        if "position" in self.tr.get("root", {}): return
        def track(b):
            ks = sorted(self.tr.get(b, {}).get("rotation", []))
            if not ks: return lambda t: 0.0
            def f(t):
                if t <= ks[0][0]: return ks[0][1]
                for (t0, x0, *_), (t1, x1, *_) in zip(ks, ks[1:]):
                    if t0 <= t <= t1: return x0 + (x1 - x0) * (t - t0) / max(1e-6, t1 - t0)
                return ks[-1][1]
            return f
        lr, sr, ll, sl = track("leg_r"), track("shin_r"), track("leg_l"), track("shin_l")
        ln = lambda a, s: 5.8 * math.cos(math.radians(a)) + 8.2 * math.cos(math.radians(a + s))
        drop = lambda t: max(0.0, 14.0 - max(ln(lr(t), sr(t)), ln(ll(t), sl(t))))
        times = sorted({k[0] for b in ("leg_r", "shin_r", "leg_l", "shin_l") for k in self.tr.get(b, {}).get("rotation", [])} | {0, self.ticks})
        if max(drop(t) for t in times) < 0.3: return
        self.pos("root", *[(t, 0, -drop(t), 0) for t in times])
        bp = self.tr.get("body", {}).get("position")
        if bp:
            self.tr["body"]["position"] = [(t, x, min(0.0, y + drop(t)), z) for (t, x, y, z) in bp]

    def done(self):
        self.plant()
        for p in PROPS:
            if p not in self.tr or "scale" not in self.tr[p]:
                self.scl(p, (0, *HIDE))
        for b, v in REST.items():
            if b not in self.tr or "rotation" not in self.tr[b]:
                self.rot(b, (0, *v))
        tracks = {b: {ch: sorted([(t / 20.0, x, y, z) for (t, x, y, z) in v], key=lambda q: q[0]) for ch, v in chs.items()}
                  for b, chs in self.tr.items()}
        m.anim(self.name, self.ticks / 20.0, tracks, loop=self.loop)


def L(a, r, l, sr=None, sl=None, fr=None, fl=None):
    """legs: full right / left keys (no mirroring), optional shins/feet"""
    a.rot("leg_r", *r); a.rot("leg_l", *l)
    if sr: a.rot("shin_r", *sr)
    if sl: a.rot("shin_l", *sl)
    if fr: a.rot("foot_r", *fr)
    if fl: a.rot("foot_l", *fl)


# ------------------------------------------------------------------ idle (80 loop): leans on the syringe like a cane, slow mask breathing,
#   lifts the syringe to eye level at 30-52 and flicks the barrel (wrist taps 40/44), a drip falls, settles back
a = A("idle", 80, loop=True)
a.pos("body", (0, 0, 0, 0), (20, 0, -0.2, 0), (40, 0, 0, 0), (60, 0, -0.2, 0), (80, 0, 0, 0))
a.rot("body", (0, 0, 0, 2), (40, 0, 0, -1), (80, 0, 0, 2))
a.rot("chest", (0, 0, 0, -1), (10, 3, 0, 0), (20, 0, 0, -1), (30, 2, 8, 0), (52, 2, 10, 0), (62, 0, 0, -1), (70, 3, 0, 0), (80, 0, 0, -1))
a.rot("head", (0, 2, 0, -4), (10, 5, 0, -6), (20, 2, 0, -4), (30, 4, 14, -2), (38, 0, 16, 6), (46, 0, 16, 8), (52, 2, 10, 0), (62, 2, 0, -4), (70, 5, 0, -6), (80, 2, 0, -4))
a.rot("arm_l", (0, 6, 0, -14), (28, 6, 0, -14), (34, 50, 30, -10), (52, 52, 32, -10), (60, 6, 0, -14), (80, 6, 0, -14))
a.rot("fore_l", (0, 20, 0, 0), (28, 20, 0, 0), (34, 70, 0, 0), (52, 72, 0, 0), (60, 20, 0, 0), (80, 20, 0, 0))
a.rot("hand_l", (0, 0, 0, 0), (28, 0, 0, 0), (34, 0, -20, 0), (38, 0, -20, 0), (40, 0, -20, -14), (41, 0, -20, 4), (44, 0, -20, -14), (45, 0, -20, 4), (47, 0, -20, 0),
      (52, 0, -20, 0), (60, 0, 0, 0), (80, 0, 0, 0))
a.rot("syr", (0, 8, 0, -8), (28, 8, 0, -8), (34, -60, 0, 0), (52, -62, 0, 0), (60, 8, 0, -8), (80, 8, 0, -8))
a.scl("drip", (0, *HIDE), (44, *HIDE), (45, 1, 1, 1), (49, 1, 1.4, 1), (50, *HIDE), (80, *HIDE))
a.pos("drip", (0, 0, 0, 0), (45, 0, 0, 0), (49, 0, -1.6, 0), (50, 0, 0, 0), (80, 0, 0, 0))
a.rot("arm_r", (0, -2, 0, 10), (40, 2, 0, 12), (80, -2, 0, 10))
a.rot("case", (0, -6, 0, -10), (20, -3, 0, -12), (40, -8, 0, -12), (60, -4, 0, -9), (80, -6, 0, -10))
L(a, [(0, 0, 0, 2), (40, 0, 0, 2), (80, 0, 0, 2)], [(0, 4, 0, -4), (40, 6, 0, -5), (80, 4, 0, -4)],
  sr=[(0, 0, 0, 0), (80, 0, 0, 0)], sl=[(0, -8, 0, 0), (40, -11, 0, 0), (80, -8, 0, 0)], fl=[(0, 6, 0, 0), (80, 6, 0, 0)])
a.hair([(0, 0, 0, 1), (20, -2, 0, 0), (40, 0, 0, -2), (60, 2, 0, 2), (80, 0, 0, 1)], delay=4)
a.coat([(0, 1, 0, 1), (40, 0, 0, -1), (80, 1, 0, 1)], delay=4)
a.done()

# ------------------------------------------------------------------ walk (20 loop): long-legged heel-clicking stride, syringe swung like a cane,
#   briefcase swinging opposite, coat tails flapping
a = A("walk", 20, loop=True)
a.rot("leg_r", (0, 26, 0, 1), (5, 0, 0, 1), (10, -24, 0, 1), (15, 0, 0, 1), (20, 26, 0, 1))
a.rot("shin_r", (0, -4, 0, 0), (5, -8, 0, 0), (10, -12, 0, 0), (13, -48, 0, 0), (17, -24, 0, 0), (20, -4, 0, 0))
a.rot("foot_r", (0, -10, 0, 0), (10, 14, 0, 0), (20, -10, 0, 0))
a.rot("leg_l", (0, -24, 0, -1), (5, 0, 0, -1), (10, 26, 0, -1), (15, 0, 0, -1), (20, -24, 0, -1))
a.rot("shin_l", (0, -12, 0, 0), (3, -48, 0, 0), (7, -24, 0, 0), (10, -4, 0, 0), (15, -8, 0, 0), (20, -12, 0, 0))
a.rot("foot_l", (0, 14, 0, 0), (10, -10, 0, 0), (20, 14, 0, 0))
a.pos("body", (0, 0, -0.4, 0), (5, 0, 0.4, 0), (10, 0, -0.4, 0), (15, 0, 0.4, 0), (20, 0, -0.4, 0))
a.rot("body", (0, -3, 5, -1), (10, -3, -5, 1), (20, -3, 5, -1))
a.rot("chest", (0, 0, -6, 1), (10, 0, 6, -1), (20, 0, -6, 1))
a.rot("head", (0, 2, 5, -4), (5, 4, 0, -2), (10, 2, -5, -4), (15, 4, 0, -2), (20, 2, 5, -4))
a.rot("arm_r", (0, -22, 0, 10), (10, 22, 0, 8), (20, -22, 0, 10))
a.rot("fore_r", (0, 6, 0, 0), (10, 24, 0, 0), (20, 6, 0, 0))
a.rot("case", (0, 18, 0, -10), (5, 4, 0, -8), (10, -30, 0, -8), (15, -10, 0, -10), (20, 18, 0, -10))
a.rot("arm_l", (0, 30, 0, -14), (10, -6, 0, -16), (20, 30, 0, -14))
a.rot("fore_l", (0, 30, 0, 0), (10, 14, 0, 0), (20, 30, 0, 0))
a.rot("syr", (0, -14, 0, -8), (5, 4, 0, -6), (10, 26, 0, -8), (15, 10, 0, -10), (20, -14, 0, -8))
a.hair([(0, -6, 0, 3), (5, -9, 0, 0), (10, -6, 0, -3), (15, -9, 0, 0), (20, -6, 0, 3)], delay=2)
a.coat([(0, 6, 0, 3), (5, 2, 0, 0), (10, 6, 0, -3), (15, 2, 0, 0), (20, 6, 0, 3)], delay=2)
tracks = {b: {ch: sorted([(t / 20.0, x, y, z) for (t, x, y, z) in v]) for ch, v in chs.items()} for b, chs in a.tr.items()}
for p in PROPS: tracks[p] = {"scale": [(0, *HIDE)]}
for b, v in REST.items():
    tracks.setdefault(b, {}).setdefault("rotation", [(0, *v)])
m.anim("walk", 1.0, tracks, loop=True)

# ------------------------------------------------------------------ death (40): drops the briefcase, clutches the mask, knees buckle,
#   falls forward; the syringe slips out of her hand and rolls flat
a = A("death", 40)
a.rot("case", (0, -6, 0, -10), (4, -6, 0, -10), (9, -60, 0, -30), (16, -100, 0, -20), (28, -20, 0, -60), (40, -10, 0, -80))
a.r("arm_r", (4, 10, 0, 14), (9, 130, 0, 30), (16, 140, 0, 24), (22, 120, 0, 20), (28, 160, 0, 40), (40, 170, 0, 40))
a.r("fore_r", (9, 100, 0, 0), (16, 110, 0, 0), (28, 20, 0, 0), (40, 20, 0, 0))
a.r("arm_l", (6, 0, 0, -10), (14, -10, 0, -20), (22, 20, 0, -30), (28, 160, 0, -40), (40, 170, 0, -40))
a.r("fore_l", (6, 10, 0, 0), (28, 20, 0, 0), (40, 20, 0, 0))
a.r("syr", (6, 0, 0, -6), (12, -10, 0, -40), (18, -20, 0, -80), (26, -20, 0, -90), (40, -20, 0, -90))
a.pos("syr", (0, 0, 0, 0), (12, 0, 0, 0), (18, 0, -3, 0), (40, 0, -3, 0))
a.r("head", (4, -24, 0, 0), (9, -16, 0, 12), (13, -20, 0, -12), (17, -30, 0, 0), (24, -10, 0, 0), (32, 20, 20, 0), (40, 18, 30, 0))
a.r("chest", (4, -18, 0, 0), (12, -24, 0, 6), (16, -26, 0, -6), (22, -10, 0, 0), (40, 0, 0, 0))
a.pos("root", (0, 0, 0, 0), (14, 0, 0, 0), (18, 0, -3.5, -1.0), (22, 0, -4.0, -1.5), (27, 0, 2.8, -4), (30, 0, 2.2, -5), (33, 0, 2.7, -5), (40, 0, 2.4, -5))
a.rot("root", (0, 0, 0, 0), (14, 0, 0, 0), (22, -10, 0, 0), (27, -70, 0, 4), (30, -90, 0, 4), (33, -84, 0, 4), (36, -90, 0, 4), (40, -90, 0, 4))
L(a, [(0, 0, 0, 2), (10, 6, 0, 4), (16, 40, 0, 4), (22, 70, 0, 4), (27, 20, 0, 6), (32, 0, 0, 8), (40, 0, 0, 8)],
  [(0, 4, 0, -4), (10, 0, 0, -6), (16, 36, 0, -6), (22, 66, 0, -4), (27, 16, 0, -6), (32, 0, 0, -8), (40, 0, 0, -8)],
  sr=[(0, 0, 0, 0), (16, -60, 0, 0), (22, -100, 0, 0), (27, -40, 0, 0), (32, -14, 0, 0), (40, -16, 0, 0)],
  sl=[(0, -8, 0, 0), (16, -60, 0, 0), (22, -96, 0, 0), (27, -30, 0, 0), (32, -10, 0, 0), (40, -12, 0, 0)])
a.hair([(0, 0, 0, 0), (9, -6, 0, 10), (13, -6, 0, -10), (18, 10, 0, 0), (24, -10, 0, 0), (28, 30, 0, 0), (32, 20, 0, 0), (40, 24, 0, 0)])
a.coat([(0, 0, 0, 0), (16, 10, 0, 0), (22, 16, 0, 0), (28, -30, 0, 0), (33, -20, 0, 0), (40, -24, 0, 0)])
a.done()

# ------------------------------------------------------------------ needle_jab (24): draws the syringe back (0-6), fencing lunge + stab peaks t9, retracts
a = A("needle_jab", 24)
a.r("arm_l", (4, -34, 0, -20), (6, -40, 0, -22), (8, 62, 0, -6), (9, 84, 0, 0), (11, 82, 0, 0), (14, 44, 0, -8), (18, 14, 0, -14))
a.r("fore_l", (4, 80, 0, 0), (6, 86, 0, 0), (8, 14, 0, 0), (9, 0, 0, 0), (11, 2, 0, 0), (14, 30, 0, 0))
a.r("syr", (4, 50, 0, 0), (6, 56, 0, 0), (8, 14, 0, 0), (9, 6, 0, 0), (11, 6, 0, 0), (14, 16, 0, -4))
a.r("hand_l", (6, 0, 0, 10), (9, 0, 0, 0))
a.r("chest", (4, 4, 26, 0), (6, 6, 30, 0), (9, -8, -24, 0), (11, -8, -22, 0), (16, 0, -6, 0))
a.r("head", (4, -4, -14, -2), (6, -6, -18, -2), (9, -10, 18, 0), (12, -8, 14, 0), (18, 2, 4, -4))
a.r("arm_r", (4, 24, 0, 22), (6, 26, 0, 24), (9, -40, 0, 30), (12, -34, 0, 26), (18, -10, 0, 14))
a.r("fore_r", (6, 30, 0, 0), (9, 10, 0, 0))
a.r("case", (6, -20, 0, -20), (9, 30, 0, -26), (12, 10, 0, -14), (16, -14, 0, -8))
a.rot("body", (0, 0, 0, 0), (6, 4, 10, 0), (9, -10, -14, 0), (12, -8, -12, 0), (24, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (6, 0, -0.6, 0.8), (9, 0, -1.2, -1.8), (12, 0, -1.0, -1.6), (24, 0, 0, 0))
L(a, [(0, 0, 0, 2), (6, 6, 0, 2), (9, -30, 0, 4), (12, -26, 0, 4), (24, 0, 0, 2)],
  [(0, 4, 0, -4), (6, -6, 0, -4), (9, 44, 0, -4), (12, 40, 0, -4), (24, 4, 0, -4)],
  sr=[(0, 0, 0, 0), (6, -10, 0, 0), (9, -6, 0, 0), (24, 0, 0, 0)], sl=[(0, -8, 0, 0), (6, -30, 0, 0), (9, -24, 0, 0), (12, -26, 0, 0), (24, -8, 0, 0)],
  fl=[(0, 6, 0, 0), (9, -16, 0, 0), (13, -12, 0, 0), (24, 6, 0, 0)])
a.hair([(0, 0, 0, 0), (6, 6, 0, -6), (9, -14, 0, 8), (13, -4, 0, 4), (24, 0, 0, 0)])
a.coat([(0, 0, 0, 0), (6, 4, 0, -4), (9, -12, 0, 8), (14, -4, 0, 2), (24, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ needle_sweep (30): winds the syringe across her chest to the right (0-10),
#   wide backhand sweep out to the left, needle crosses the front at t13, overshoot 15, recover
a = A("needle_sweep", 30)
a.r("arm_l", (5, 60, -40, 20), (9, 80, -70, 30), (10, 82, -74, 30), (12, 88, -20, 0), (13, 90, 10, -10), (15, 86, 70, -20), (18, 70, 80, -24), (24, 20, 20, -16))
a.r("fore_l", (5, 50, 0, 0), (10, 60, 0, 0), (13, 4, 0, 0), (16, 6, 0, 0), (24, 20, 0, 0))
a.r("syr", (5, 20, 0, 0), (10, 30, 0, 0), (13, 4, 0, 0), (16, 0, 0, 0), (22, 6, 0, -6))
a.r("hand_l", (10, 0, -40, 0), (13, 0, 0, 0), (16, 0, 20, 0), (24, 0, 0, 0))
a.r("chest", (5, 2, -24, 0), (10, 4, -34, 0), (13, -4, 10, 0), (15, -6, 34, 0), (18, -4, 30, 0), (26, 0, 0, 0))
a.r("head", (5, -2, 14, -4), (10, -4, 22, -2), (13, -6, -6, 0), (16, -6, -20, 2), (24, 0, -4, -4))
a.r("arm_r", (5, 10, 0, 30), (10, 14, 0, 40), (13, -10, 0, 50), (16, -20, 0, 54), (24, -6, 0, 18))
a.r("fore_r", (10, 30, 0, 0), (16, 20, 0, 0))
a.r("case", (10, 0, 0, -50), (14, 0, 0, -30), (17, 0, 0, -58), (24, -4, 0, -16))
a.rot("body", (0, 0, 0, 0), (10, 0, -16, 0), (13, -4, 8, 0), (16, -6, 20, 0), (22, -2, 6, 0), (30, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (10, 0, -1.0, 0.4), (13, 0, -1.2, -1.2), (17, 0, -1.0, -1.4), (30, 0, 0, 0))
L(a, [(0, 0, 0, 2), (10, 14, 0, 6), (13, -20, 0, 6), (17, -22, 0, 6), (30, 0, 0, 2)],
  [(0, 4, 0, -4), (10, -14, 0, -6), (13, 30, 0, -8), (17, 30, 0, -8), (30, 4, 0, -4)],
  sr=[(0, 0, 0, 0), (10, -24, 0, 0), (13, -10, 0, 0), (30, 0, 0, 0)], sl=[(0, -8, 0, 0), (10, -14, 0, 0), (13, -30, 0, 0), (17, -32, 0, 0), (30, -8, 0, 0)])
a.hair([(0, 0, 0, 0), (10, 2, 0, 14), (13, -6, 0, -10), (16, -6, 0, -22), (21, 0, 0, -6), (30, 0, 0, 0)])
a.coat([(0, 0, 0, 0), (10, 2, 0, 10), (14, -6, 0, -14), (18, -4, 0, -18), (24, 0, 0, -4), (30, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ case_bash (28): hauls the briefcase back (0-9), rising uppercut swing lands t12,
#   case flies high (14), she stumbles after its weight, recovers
a = A("case_bash", 28)
a.r("arm_r", (5, -50, 0, 24), (9, -66, 0, 20), (11, 40, 0, 6), (12, 100, 0, -6), (14, 140, 0, -10), (17, 120, 0, -4), (22, 30, 0, 10))
a.r("fore_r", (5, 10, 0, 0), (9, 20, 0, 0), (12, 0, 0, 0), (14, 6, 0, 0), (22, 14, 0, 0))
a.r("case", (5, 20, 0, -14), (9, 40, 0, -10), (11, -20, 0, -4), (12, -50, 0, 0), (14, -10, 0, 0), (17, 30, 0, -4), (22, -14, 0, -10))
a.r("chest", (5, 4, -20, 0), (9, 6, -32, 0), (12, -10, 20, 0), (14, -14, 26, 0), (18, -6, 14, 0), (26, 0, 0, 0))
a.r("head", (5, -4, 18, -6), (9, -8, 26, -6), (12, 8, -14, 0), (14, 12, -18, 4), (20, 2, -6, -4))
a.r("arm_l", (5, 30, 0, -24), (9, 34, 0, -30), (12, -20, 0, -24), (16, -10, 0, -20))
a.r("fore_l", (9, 40, 0, 0), (12, 10, 0, 0))
a.r("syr", (9, -20, 0, -14), (12, 20, 0, -10), (16, 12, 0, -8))
a.rot("body", (0, 0, 0, 0), (9, -10, -18, 0), (12, 6, 14, 0), (15, 10, 18, 0), (28, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (9, 0, -1.6, 0.6), (12, 0, 0.2, -1.2), (15, 0, 0.0, -1.6), (19, 0, -0.6, -1.4), (28, 0, 0, 0))
L(a, [(0, 0, 0, 2), (9, 24, 0, 4), (12, -24, 0, 4), (16, -20, 0, 4), (28, 0, 0, 2)],
  [(0, 4, 0, -4), (9, -20, 0, -4), (12, 26, 0, -4), (16, 20, 0, -4), (28, 4, 0, -4)],
  sr=[(0, 0, 0, 0), (9, -40, 0, 0), (12, -4, 0, 0), (28, 0, 0, 0)], sl=[(0, -8, 0, 0), (9, -20, 0, 0), (12, -18, 0, 0), (28, -8, 0, 0)])
a.hair([(0, 0, 0, 0), (9, 8, 0, 8), (12, -10, 0, -8), (15, -16, 0, -10), (20, 4, 0, 0), (28, 0, 0, 0)])
a.coat([(0, 0, 0, 0), (9, 6, 0, 6), (12, -10, 0, -8), (16, -8, 0, -8), (28, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ inoculate (44): quick jab t8, second jab t15, wind-up 18-23, drives the needle in t26
#   and empties the plunger (26-32, liquid drains), yanks out 34, plunger springs back 40
a = A("inoculate", 44)
a.r("arm_l", (4, -10, 0, -16), (6, 40, 0, -8), (8, 84, 0, 0), (10, 70, 0, -4), (12, 30, 0, -10), (15, 86, 0, 2), (17, 70, 0, -4), (21, -30, 0, -20), (23, -36, 0, -22),
    (25, 80, 0, -2), (26, 90, 0, 2), (32, 90, 0, 2), (34, 60, 0, -4), (36, 70, 0, -6), (42, 10, 0, -14))
a.r("fore_l", (4, 60, 0, 0), (8, 0, 0, 0), (12, 50, 0, 0), (15, 0, 0, 0), (19, 50, 0, 0), (23, 90, 0, 0), (26, 0, 0, 0), (32, 0, 0, 0), (36, 30, 0, 0))
a.r("syr", (4, 30, 0, 0), (8, 6, 0, 0), (12, 30, 0, 0), (15, 4, 0, 0), (23, 60, 0, 0), (26, 4, 0, 0), (32, 4, 0, 0), (36, 20, 0, -4))
a.pos("plunger", (0, 0, 0, 0), (26, 0, 0, 0), (28, 0, -2.4, 0), (31, 0, -4.4, 0), (36, 0, -4.4, 0), (39, 0, 0.4, 0), (41, 0, 0, 0), (44, 0, 0, 0))
a.scl("liquid", (0, 1, 1, 1), (26, 1, 1, 1), (31, 1, 0.3, 1), (36, 1, 0.3, 1), (40, 1, 1.05, 1), (42, 1, 1, 1), (44, 1, 1, 1))
a.r("chest", (4, 2, 14, 0), (8, -6, -20, 0), (12, 0, 10, 0), (15, -6, -22, 0), (19, 0, 10, 0), (23, 6, 30, 0), (26, -10, -26, 0), (32, -10, -24, 0), (36, 0, -8, 0))
a.r("head", (4, -4, -8, 0), (8, -8, 14, 0), (12, -2, -6, 0), (15, -8, 16, 0), (23, -6, -20, 0), (26, -14, 18, 0), (30, -16, 16, 6), (33, -16, 16, -4), (38, 0, 4, -4))
a.r("arm_r", (6, -20, 0, 24), (8, -30, 0, 28), (15, -30, 0, 28), (23, 30, 0, 20), (26, -40, 0, 30), (32, -36, 0, 30), (38, -6, 0, 14))
a.r("case", (8, 20, 0, -24), (15, 20, 0, -24), (23, -20, 0, -16), (26, 30, 0, -26), (30, 10, 0, -24), (38, -6, 0, -10))
a.rot("body", (0, 0, 0, 0), (8, -6, -10, 0), (12, 0, 4, 0), (15, -6, -12, 0), (23, 4, 14, 0), (26, -12, -16, 0), (32, -12, -14, 0), (44, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (8, 0, -0.8, -1.0), (12, 0, -0.4, -0.4), (15, 0, -0.8, -1.2), (23, 0, -0.8, 0.0), (26, 0, -1.6, -2.0), (32, 0, -1.6, -1.8), (36, 0, -0.6, -0.6), (44, 0, 0, 0))
L(a, [(0, 0, 0, 2), (8, -16, 0, 4), (15, -20, 0, 4), (23, 6, 0, 4), (26, -34, 0, 4), (32, -32, 0, 4), (44, 0, 0, 2)],
  [(0, 4, 0, -4), (8, 30, 0, -4), (15, 34, 0, -4), (23, 10, 0, -4), (26, 46, 0, -4), (32, 44, 0, -4), (44, 4, 0, -4)],
  sr=[(0, 0, 0, 0), (8, -6, 0, 0), (23, -20, 0, 0), (26, -4, 0, 0), (44, 0, 0, 0)], sl=[(0, -8, 0, 0), (8, -20, 0, 0), (23, -24, 0, 0), (26, -30, 0, 0), (32, -30, 0, 0), (44, -8, 0, 0)],
  fl=[(0, 6, 0, 0), (26, -16, 0, 0), (32, -14, 0, 0), (44, 6, 0, 0)])
a.hair([(0, 0, 0, 0), (8, -8, 0, 6), (12, 2, 0, -4), (15, -8, 0, 6), (23, 6, 0, -8), (26, -14, 0, 8), (30, -6, 0, 4), (36, 4, 0, 0), (44, 0, 0, 0)], delay=1)
a.coat([(0, 0, 0, 0), (8, -6, 0, 4), (15, -6, 0, 4), (23, 4, 0, -4), (26, -12, 0, 6), (36, -2, 0, 0), (44, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ heel_kick (26): weight back, raises the stiletto boot straight up (8),
#   axe-kick chops down t11, heel plants 13, hops back to stance
a = A("heel_kick", 26)
a.rot("leg_r", (0, 0, 0, 2), (4, 50, 0, 4), (7, 120, 0, 6), (8, 136, 0, 6), (10, 90, 0, 4), (11, 40, 0, 2), (13, 26, 0, 2), (18, 10, 0, 2), (26, 0, 0, 2))
a.rot("shin_r", (0, 0, 0, 0), (4, -70, 0, 0), (7, -20, 0, 0), (8, -4, 0, 0), (11, 0, 0, 0), (13, -10, 0, 0), (17, -30, 0, 0), (26, 0, 0, 0))
a.rot("foot_r", (0, 0, 0, 0), (4, 20, 0, 0), (8, -40, 0, 0), (11, -30, 0, 0), (14, 0, 0, 0), (26, 0, 0, 0))
a.rot("leg_l", (0, 4, 0, -4), (4, -6, 0, -4), (8, -14, 0, -4), (11, -24, 0, -4), (14, -20, 0, -4), (20, -4, 0, -4), (26, 4, 0, -4))
a.rot("shin_l", (0, -8, 0, 0), (4, -16, 0, 0), (8, -8, 0, 0), (11, -24, 0, 0), (14, -20, 0, 0), (26, -8, 0, 0))
a.rot("foot_l", (0, 6, 0, 0), (8, 10, 0, 0), (11, 30, 0, 0), (26, 6, 0, 0))
a.rot("body", (0, 0, 0, 0), (4, 6, 0, 0), (8, 16, 0, 4), (10, 4, 0, 2), (11, -18, 0, 0), (14, -14, 0, 0), (20, -2, 0, 0), (26, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (8, 0, 0.8, 0.8), (11, 0, -1.4, -1.6), (14, 0, -1.0, -1.4), (20, 0, 0.3, 0.4), (26, 0, 0, 0))
a.r("chest", (8, 10, 0, 0), (11, -14, 0, 0), (16, -6, 0, 0))
a.r("head", (8, -12, 0, -4), (11, -20, 0, 0), (14, -16, 0, 4), (20, 2, 0, -4))
a.r("arm_r", (6, 30, 0, 40), (8, 40, 0, 56), (11, -20, 0, 50), (16, -10, 0, 30))
a.r("fore_r", (8, 30, 0, 0), (11, 10, 0, 0))
a.r("case", (8, -30, 0, -50), (11, 30, 0, -40), (15, 0, 0, -20))
a.r("arm_l", (6, 20, 0, -36), (8, 30, 0, -50), (11, -10, 0, -44), (16, 0, 0, -24))
a.r("fore_l", (8, 40, 0, 0), (11, 20, 0, 0))
a.r("syr", (8, -30, 0, -10), (11, 20, 0, -20), (16, 10, 0, -10))
a.hair([(0, 0, 0, 0), (8, -10, 0, 0), (11, 18, 0, 0), (14, 6, 0, 0), (26, 0, 0, 0)], delay=1)
a.coat([(0, 0, 0, 0), (5, 14, 0, 4), (8, 26, 0, 6), (11, -10, 0, 0), (16, 4, 0, 0), (26, 0, 0, 0)], delay=1)
a.done()

# ------------------------------------------------------------------ plunger_slam (38): both hands hoist the syringe overhead needle-up (0-14),
#   whips it over and spikes it into the floor t18 (crouched), pries 22-26, yanks it free, stands
a = A("plunger_slam", 38)
a.r("arm_l", (6, 100, 0, -20), (12, 166, 0, -8), (14, 172, 0, -6), (16, 110, 0, -4), (18, 50, 0, 0), (22, 48, 0, 0), (25, 56, 0, 0), (26, 90, 0, -6), (30, 60, 0, -10), (36, 10, 0, -14))
a.r("fore_l", (6, 30, 0, 0), (14, 10, 0, 0), (18, 0, 0, 0), (25, 6, 0, 0), (26, 30, 0, 0), (32, 20, 0, 0))
a.r("syr", (6, 10, 0, -10), (14, 0, 0, 0), (16, -10, 0, 0), (18, -18, 0, 0), (22, -18, 0, 0), (25, -22, 0, 0), (26, -40, 0, 0), (30, -10, 0, -6))
a.r("arm_r", (6, 90, 0, 10), (12, 160, 0, 10), (14, 166, 0, 10), (16, 110, 0, 10), (18, 40, 0, 20), (24, 30, 0, 24), (30, 10, 0, 14))
a.r("fore_r", (12, 20, 0, 0), (18, 10, 0, 0), (30, 10, 0, 0))
a.r("case", (8, -60, 0, -10), (14, -120, 0, -10), (16, -100, 0, -10), (18, 20, 0, -20), (21, -10, 0, -24), (26, 0, 0, -14))
a.r("chest", (6, 10, 0, 0), (12, 20, 0, 0), (14, 22, 0, 0), (16, 0, 0, 0), (18, -26, 0, 0), (24, -24, 0, 0), (26, -10, 0, 0), (32, 0, 0, 0))
a.r("head", (6, 10, 0, 0), (12, 22, 0, 0), (16, 0, 0, 0), (18, -14, 0, 0), (22, -10, 0, 6), (24, -10, 0, -6), (26, 6, 0, 0), (32, 2, 0, -4))
a.rot("body", (0, 0, 0, 0), (12, 8, 0, 0), (14, 10, 0, 0), (18, -24, 0, 0), (24, -22, 0, 0), (27, -6, 0, 0), (38, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (6, 0, -0.8, 0), (12, 0, 0.6, 0.6), (14, 0, 0.8, 0.6), (18, 0, -2.6, -1.4), (24, 0, -2.4, -1.4), (27, 0, -0.6, -0.4), (38, 0, 0, 0))
L(a, [(0, 0, 0, 2), (6, 10, 0, 4), (14, 0, 0, 4), (18, -30, 0, 6), (24, -28, 0, 6), (28, -8, 0, 4), (38, 0, 0, 2)],
  [(0, 4, 0, -4), (6, 10, 0, -4), (14, 6, 0, -4), (18, 50, 0, -6), (24, 48, 0, -6), (28, 16, 0, -4), (38, 4, 0, -4)],
  sr=[(0, 0, 0, 0), (6, -20, 0, 0), (14, 0, 0, 0), (18, -10, 0, 0), (28, -4, 0, 0), (38, 0, 0, 0)],
  sl=[(0, -8, 0, 0), (6, -20, 0, 0), (14, -6, 0, 0), (18, -70, 0, 0), (24, -68, 0, 0), (28, -24, 0, 0), (38, -8, 0, 0)],
  fr=[(0, 0, 0, 0), (18, 20, 0, 0), (24, 20, 0, 0), (38, 0, 0, 0)])
a.hair([(0, 0, 0, 0), (8, -6, 0, 0), (14, -10, 0, 0), (18, 24, 0, 0), (22, 8, 0, 6), (24, 8, 0, -6), (28, -4, 0, 0), (38, 0, 0, 0)], delay=1)
a.coat([(0, 0, 0, 0), (12, -6, 0, 0), (18, 20, 0, 0), (24, 10, 0, 0), (30, 0, 0, 0), (38, 0, 0, 0)], delay=1)
a.done()

# ------------------------------------------------------------------ lunge_inject (34): low crouch aiming the needle (0-8), explosive lunge 9-14
#   (skewer t12 + t14), skids with the coat flaring (15-22), stands up
a = A("lunge_inject", 34)
a.r("arm_l", (4, 60, 0, -10), (8, 70, 0, -6), (10, 88, 0, 0), (14, 90, 0, 2), (18, 80, 0, -4), (24, 40, 0, -10), (30, 10, 0, -14))
a.r("fore_l", (4, 40, 0, 0), (8, 50, 0, 0), (10, 0, 0, 0), (14, 0, 0, 0), (20, 10, 0, 0))
a.r("syr", (4, -10, 0, 0), (8, -20, 0, 0), (10, 4, 0, 0), (14, 4, 0, 0), (20, 8, 0, -4))
a.r("hand_l", (8, 0, 0, 0), (12, 0, 0, 20), (14, 0, 0, -10), (16, 0, 0, 0))
a.r("arm_r", (4, -40, 0, 30), (8, -50, 0, 34), (12, -70, 0, 30), (16, -50, 0, 30), (22, 10, 0, 30), (30, -6, 0, 12))
a.r("fore_r", (8, 30, 0, 0), (16, 20, 0, 0))
a.r("case", (8, 20, 0, -30), (12, 50, 0, -26), (17, -20, 0, -30), (22, 20, 0, -20), (30, -6, 0, -10))
a.rot("body", (0, 0, 0, 0), (4, -24, 0, 0), (8, -30, 6, 0), (10, -40, -6, 0), (14, -40, -6, 0), (16, -10, 0, 0), (19, 8, 0, 0), (24, 2, 0, 0), (34, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (4, 0, -2.6, 1.0), (8, 0, -3.0, 1.4), (10, 0, -2.0, -1.6), (14, 0, -2.2, -1.8), (17, 0, -1.6, -0.8), (20, 0, -0.6, 0), (34, 0, 0, 0))
a.r("chest", (8, 10, 6, 0), (10, 4, -10, 0), (14, 4, -10, 0), (18, 10, 0, 0), (22, 4, 0, 0))
a.r("head", (4, 20, 0, 0), (8, 26, -6, 0), (10, 30, 10, 0), (14, 28, 10, 0), (18, 0, 0, 6), (24, 2, 0, -4))
L(a, [(0, 0, 0, 2), (4, 50, 0, 4), (8, 60, 0, 4), (10, -30, 0, 4), (12, 50, 0, 4), (14, 70, 0, 4), (17, 50, 0, 6), (20, 20, 0, 4), (34, 0, 0, 2)],
  [(0, 4, 0, -4), (4, -20, 0, -4), (8, -30, 0, -4), (10, 60, 0, -4), (12, -20, 0, -4), (14, -40, 0, -4), (17, -20, 0, -6), (20, -6, 0, -4), (34, 4, 0, -4)],
  sr=[(0, 0, 0, 0), (4, -90, 0, 0), (8, -100, 0, 0), (10, -20, 0, 0), (12, -80, 0, 0), (14, -70, 0, 0), (17, -50, 0, 0), (22, -10, 0, 0), (34, 0, 0, 0)],
  sl=[(0, -8, 0, 0), (4, -40, 0, 0), (8, -50, 0, 0), (10, -60, 0, 0), (12, -10, 0, 0), (14, -20, 0, 0), (17, -10, 0, 0), (34, -8, 0, 0)],
  fr=[(0, 0, 0, 0), (8, 30, 0, 0), (14, 10, 0, 0), (34, 0, 0, 0)], fl=[(0, 6, 0, 0), (8, 30, 0, 0), (14, 30, 0, 0), (34, 6, 0, 0)])
a.hair([(0, 0, 0, 0), (8, 8, 0, 0), (11, -28, 0, 0), (14, -26, 0, 0), (17, 18, 0, 0), (22, 4, 0, 0), (34, 0, 0, 0)], delay=1)
a.coat([(0, 0, 0, 0), (8, 6, 0, 0), (11, -36, 0, 4), (15, -38, 0, -4), (19, 20, 0, 0), (25, 4, 0, 0), (34, 0, 0, 0)], delay=1)
a.done()

# ------------------------------------------------------------------ syringe_spin (36): coils (0-6), three whirling turns with syringe + briefcase
#   held straight out (hits t10/t18/t26), dizzy wobble, steadies on the syringe
a = A("syringe_spin", 36)
a.rot("root", (0, 0, 0, 0), (6, 0, 34, 0), (10, 0, -120, 0), (14, 0, -300, 0), (18, 0, -480, 0), (22, 0, -660, 0), (26, 0, -840, 0), (29, 0, -1060, 0), (31, 0, -1084, 0),
      (33, 0, -1076, 0), (36, 0, -1080, 0))
a.pos("root", (0, 0, 0, 0), (6, 0, -1.2, 0), (10, 0, 0.3, 0), (18, 0, 0.5, 0), (26, 0, 0.3, 0), (29, 0, 0, 0), (36, 0, 0, 0))
a.r("arm_l", (6, 30, 0, -50), (9, 0, 0, -96), (26, 0, 0, -98), (29, 20, 0, -60), (32, 20, 0, -30))
a.r("fore_l", (6, 40, 0, 0), (9, 0, 0, 0), (26, 0, 0, 0), (30, 30, 0, 0))
a.r("syr", (6, 20, 0, 0), (9, 0, 0, 0), (26, 0, 0, 0), (30, 20, 0, -6))
a.r("arm_r", (6, 30, 0, 50), (9, 0, 0, 96), (26, 0, 0, 98), (29, 20, 0, 50), (32, 0, 0, 20))
a.r("fore_r", (6, 30, 0, 0), (9, 0, 0, 0), (26, 0, 0, 0))
a.r("case", (6, 0, 0, -40), (9, 0, 0, -96), (26, 0, 0, -100), (29, 0, 0, -40), (33, -6, 0, -14))
a.r("chest", (6, 0, 24, 0), (9, -4, -10, 0), (26, -4, -10, 0), (29, 0, 0, 10), (31, 0, 0, -10), (34, 0, 0, 6))
a.r("head", (6, 0, 20, 0), (9, 6, -12, 0), (26, 6, -12, 0), (29, 6, 0, 18), (31, 6, 0, -16), (34, 4, 0, 10))
L(a, [(0, 0, 0, 2), (6, 14, 0, 6), (9, 0, 0, 8), (26, 0, 0, 8), (29, -10, 0, 6), (32, 0, 0, 4), (36, 0, 0, 2)],
  [(0, 4, 0, -4), (6, -10, 0, -6), (9, 0, 0, -8), (26, 0, 0, -8), (29, 10, 0, -6), (32, 6, 0, -4), (36, 4, 0, -4)],
  sr=[(0, 0, 0, 0), (6, -24, 0, 0), (9, 0, 0, 0), (29, -14, 0, 0), (36, 0, 0, 0)], sl=[(0, -8, 0, 0), (6, -24, 0, 0), (9, 0, 0, 0), (29, -20, 0, 0), (36, -8, 0, 0)])
a.hair([(0, 0, 0, 0), (6, 0, 0, -10), (10, -12, 0, 30), (26, -12, 0, 30), (29, 0, 0, -16), (32, 0, 0, 10), (36, 0, 0, 0)])
a.coat([(0, 0, 0, 0), (6, 0, 0, -6), (10, -16, 0, 34), (26, -16, 0, 34), (29, 4, 0, -12), (32, 0, 0, 6), (36, 0, 0, 0)], delay=1)
a.done()

# ------------------------------------------------------------------ gas_vent (44): hunches, deep breaths (head back 8/16/24) then exhales gas
#   through the respirator t12 / t20 / t28 (arms spread), shakes off the fumes
a = A("gas_vent", 44)
a.puff(12, 36)
a.r("head", (4, -10, 0, 0), (8, 24, 0, 0), (12, -22, 0, 0), (14, -18, 0, 0), (16, 22, 0, 0), (20, -24, 0, 0), (22, -20, 0, 0), (24, 24, 0, 0), (28, -26, 0, 0), (32, -22, 0, 0),
    (36, 0, 0, 14), (38, 0, 0, -14), (40, 0, 0, 10), (44, 2, 0, -4))
a.r("chest", (4, -16, 0, 0), (8, 10, 0, 0), (12, -20, 0, 0), (16, 8, 0, 0), (20, -20, 0, 0), (24, 8, 0, 0), (28, -22, 0, 0), (34, -10, 0, 0), (40, 0, 0, 0))
a.r("arm_l", (4, 20, 0, -30), (8, 10, 0, -50), (12, 30, 0, -70), (16, 10, 0, -50), (20, 30, 0, -72), (24, 10, 0, -50), (28, 30, 0, -74), (34, 20, 0, -40), (40, 6, 0, -14))
a.r("fore_l", (8, 30, 0, 0), (12, 10, 0, 0), (28, 10, 0, 0), (36, 20, 0, 0))
a.r("syr", (8, -20, 0, 10), (12, 0, 0, 20), (28, 0, 0, 20), (36, 4, 0, -4))
a.r("arm_r", (4, 20, 0, 30), (8, 10, 0, 50), (12, 30, 0, 70), (16, 10, 0, 50), (20, 30, 0, 72), (24, 10, 0, 50), (28, 30, 0, 74), (34, 20, 0, 40), (40, -2, 0, 10))
a.r("fore_r", (8, 30, 0, 0), (12, 10, 0, 0), (28, 10, 0, 0), (36, 14, 0, 0))
a.r("case", (8, -10, 0, -40), (12, -10, 0, -70), (16, -10, 0, -46), (20, -10, 0, -72), (24, -10, 0, -46), (28, -10, 0, -74), (34, -6, 0, -40), (40, -6, 0, -10))
a.rot("body", (0, 0, 0, 0), (4, -12, 0, 0), (8, 0, 0, 0), (12, -14, 0, 0), (16, 0, 0, 0), (20, -14, 0, 0), (24, 0, 0, 0), (28, -16, 0, 0), (36, -4, 0, 0), (44, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (4, 0, -1.2, 0), (8, 0, 0, 0), (12, 0, -1.4, -0.4), (16, 0, 0, 0), (20, 0, -1.4, -0.4), (24, 0, 0, 0), (28, 0, -1.6, -0.4), (36, 0, -0.4, 0), (44, 0, 0, 0))
L(a, [(0, 0, 0, 2), (4, 10, 0, 6), (28, 10, 0, 6), (36, 4, 0, 4), (44, 0, 0, 2)], [(0, 4, 0, -4), (4, 10, 0, -6), (28, 10, 0, -6), (36, 6, 0, -4), (44, 4, 0, -4)],
  sr=[(0, 0, 0, 0), (4, -20, 0, 0), (12, -24, 0, 0), (28, -24, 0, 0), (40, 0, 0, 0)], sl=[(0, -8, 0, 0), (4, -20, 0, 0), (28, -24, 0, 0), (44, -8, 0, 0)])
a.hair([(0, 0, 0, 0), (8, -8, 0, 0), (12, 10, 0, 0), (16, -8, 0, 0), (20, 10, 0, 0), (24, -8, 0, 0), (28, 12, 0, 0), (36, 0, 0, 12), (38, 0, 0, -12), (44, 0, 0, 0)], delay=1)
a.coat([(0, 0, 0, 0), (12, 6, 0, 0), (16, -2, 0, 0), (20, 6, 0, 0), (28, 8, 0, 0), (38, 0, 0, 0), (44, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ flask_lob (34): swings the briefcase back (0-9), underhand heave forward-up,
#   lid pops open t13 and the flask flies out t14 (prop), snaps the case shut 20-24, settles
a = A("flask_lob", 34)
a.show("flask", 11, 14)
a.pos("flask", (0, 0, 0, 0), (12, 0, 0, 0), (14, 0, 3.0, 0), (15, 0, 3.0, 0))
a.r("lid", (11, 0, 0, 0), (13, 0, 0, 80), (15, 0, 0, 100), (19, 0, 0, 90), (22, 0, 0, 0))
a.r("arm_r", (4, -40, 0, 20), (9, -70, 0, 20), (12, 40, 0, 10), (14, 110, 0, 4), (16, 120, 0, 4), (20, 80, 0, 10), (26, 20, 0, 12))
a.r("fore_r", (9, 20, 0, 0), (14, 0, 0, 0), (20, 30, 0, 0), (26, 14, 0, 0))
a.r("case", (4, 20, 0, -14), (9, 40, 0, -14), (12, -20, 0, -10), (14, -80, 0, -10), (16, -100, 0, -10), (20, -70, 0, -10), (26, -20, 0, -10))
a.r("hand_r", (12, 0, 0, 0), (14, 0, -60, 0), (18, 0, -60, 0), (24, 0, 0, 0))
a.r("chest", (5, 4, -20, 0), (9, 8, -28, 0), (13, -4, 14, 0), (15, -8, 18, 0), (22, 0, 6, 0), (30, 0, 0, 0))
a.r("head", (5, 6, 16, -4), (9, 6, 22, -4), (13, 14, -10, 0), (16, 18, -14, 0), (22, 8, -4, -2))
a.r("arm_l", (5, 20, 0, -30), (9, 26, 0, -34), (14, -10, 0, -26), (20, 0, 0, -18))
a.r("fore_l", (9, 40, 0, 0), (14, 20, 0, 0))
a.r("syr", (9, -20, 0, -10), (14, 14, 0, -14))
a.rot("body", (0, 0, 0, 0), (9, -8, -14, 0), (13, 4, 12, 0), (16, 8, 14, 0), (24, 2, 4, 0), (34, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (9, 0, -1.6, 0.6), (13, 0, 0, -0.8), (16, 0, 0.3, -1.0), (24, 0, 0, -0.4), (34, 0, 0, 0))
L(a, [(0, 0, 0, 2), (9, 26, 0, 4), (13, -18, 0, 4), (17, -14, 0, 4), (34, 0, 0, 2)],
  [(0, 4, 0, -4), (9, -20, 0, -4), (13, 24, 0, -4), (17, 20, 0, -4), (34, 4, 0, -4)],
  sr=[(0, 0, 0, 0), (9, -40, 0, 0), (13, -4, 0, 0), (34, 0, 0, 0)], sl=[(0, -8, 0, 0), (9, -16, 0, 0), (13, -10, 0, 0), (34, -8, 0, 0)],
  fr=[(0, 0, 0, 0), (13, -20, 0, 0), (18, -10, 0, 0), (34, 0, 0, 0)])
a.hair([(0, 0, 0, 0), (9, 6, 0, 8), (13, -8, 0, -6), (17, -10, 0, -8), (24, 2, 0, 0), (34, 0, 0, 0)])
a.coat([(0, 0, 0, 0), (9, 6, 0, 6), (13, -6, 0, -6), (18, -6, 0, -6), (34, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ needle_spray (34): levels the syringe like a rifle, briefcase braced under it
#   (0-10), thumb pumps the plunger: three jets t14 / t18 / t22 (recoil each, liquid drops), lowers, refills
a = A("needle_spray", 34)
a.r("arm_l", (5, 60, 10, -6), (10, 84, 14, 0), (13, 84, 14, 0), (14, 90, 14, 0), (16, 84, 14, 0), (18, 90, 14, 0), (20, 84, 14, 0), (22, 92, 14, 0), (25, 82, 14, 0), (30, 20, 0, -12))
a.r("fore_l", (5, 30, 0, 0), (10, 4, 0, 0), (25, 4, 0, 0), (30, 20, 0, 0))
a.r("syr", (5, -10, 0, 0), (10, 2, 0, 0), (14, 6, 0, 0), (25, 2, 0, 0), (30, 8, 0, -8))
a.pos("plunger", (0, 0, 0, 0), (12, 0, 0, 0), (14, 0, -1.4, 0), (16, 0, -1.4, 0), (18, 0, -2.8, 0), (20, 0, -2.8, 0), (22, 0, -4.2, 0), (27, 0, -4.2, 0), (31, 0, 0.3, 0), (34, 0, 0, 0))
a.scl("liquid", (0, 1, 1, 1), (12, 1, 1, 1), (14, 1, 0.78, 1), (18, 1, 0.56, 1), (22, 1, 0.34, 1), (27, 1, 0.34, 1), (32, 1, 1, 1), (34, 1, 1, 1))
a.r("arm_r", (5, 40, -30, 0), (10, 70, -40, 0), (14, 74, -40, 0), (25, 74, -40, 0), (30, 10, 0, 12))
a.r("fore_r", (5, 40, 0, 0), (10, 50, 0, 0), (25, 50, 0, 0), (30, 10, 0, 0))
a.r("case", (10, -100, 0, -10), (25, -100, 0, -10), (30, -10, 0, -10))
a.r("chest", (5, 2, 20, 0), (10, 2, 30, 0), (14, 6, 30, 0), (16, 2, 30, 0), (18, 6, 30, 0), (20, 2, 30, 0), (22, 8, 30, 0), (25, 2, 26, 0), (30, 0, 0, 0))
a.r("head", (5, -2, -16, 0), (10, -4, -26, -6), (14, 0, -26, -6), (22, 2, -26, -6), (26, -2, -20, -4), (32, 2, 0, -4))
a.rot("body", (0, 0, 0, 0), (10, 0, 10, 0), (25, 0, 10, 0), (34, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (10, 0, -0.8, 0), (14, 0, -0.8, 0.4), (16, 0, -0.8, 0.1), (18, 0, -0.8, 0.5), (20, 0, -0.8, 0.2), (22, 0, -0.8, 0.6), (26, 0, -0.6, 0.2), (34, 0, 0, 0))
L(a, [(0, 0, 0, 2), (10, -20, 0, 4), (25, -20, 0, 4), (34, 0, 0, 2)], [(0, 4, 0, -4), (10, 24, 0, -4), (25, 24, 0, -4), (34, 4, 0, -4)],
  sr=[(0, 0, 0, 0), (10, -6, 0, 0), (34, 0, 0, 0)], sl=[(0, -8, 0, 0), (10, -26, 0, 0), (25, -26, 0, 0), (34, -8, 0, 0)])
a.hair([(0, 0, 0, 0), (10, 0, 0, -4), (14, 4, 0, -4), (18, 4, 0, -4), (22, 6, 0, -4), (28, 0, 0, 0), (34, 0, 0, 0)], delay=1)
a.coat([(0, 0, 0, 0), (10, 0, 0, -4), (22, 2, 0, -4), (34, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ overdose (ENRAGED, 50): hoists the syringe needle-up (0-12), stabs it straight
#   down into the floor t16 (crouched over it), hammers the plunger pad with the briefcase t22 / t28 / t34 (toxic shockwaves),
#   gas pours out of the respirator, yanks the syringe free t42, plunger springs back + refills
a = A("overdose", 50)
a.puff(34, 46)
a.r("arm_l", (6, 120, 0, -20), (11, 160, 0, -10), (13, 166, 0, -8), (15, 90, 0, -4), (16, 50, 0, 0), (40, 50, 0, 0), (42, 100, 0, -6), (45, 80, 0, -10), (50, *rest("arm_l")))
a.r("fore_l", (6, 30, 0, 0), (13, 10, 0, 0), (16, 0, 0, 0), (40, 0, 0, 0), (42, 30, 0, 0))
a.r("syr", (6, 10, 0, -8), (13, 0, 0, 0), (15, -10, 0, 0), (16, -26, 0, 0), (40, -26, 0, 0), (42, -50, 0, 0), (45, -10, 0, -6))
a.pos("plunger", (0, 0, 0, 0), (21, 0, 0, 0), (22, 0, -1.5, 0), (27, 0, -1.5, 0), (28, 0, -3.0, 0), (33, 0, -3.0, 0), (34, 0, -4.6, 0), (43, 0, -4.6, 0), (47, 0, 0.3, 0), (50, 0, 0, 0))
a.scl("liquid", (0, 1, 1, 1), (21, 1, 1, 1), (22, 1, 0.74, 1), (27, 1, 0.74, 1), (28, 1, 0.48, 1), (33, 1, 0.48, 1), (34, 1, 0.18, 1), (43, 1, 0.18, 1), (48, 1, 1, 1), (50, 1, 1, 1))
# briefcase hammer: wind overhead 19/25/31, slam on the pad 22/28/34
ar, cs, ch, hd, bd, bp = [R_("arm_r", 0), (8, 40, 0, 30), (14, 30, 0, 30)], [R_("case", 0), (14, -20, 0, -20)], \
    [(0, 0, 0, 0), (13, 16, 0, 0), (16, -10, 0, 0)], [R_("head", 0), (13, 20, 0, 0), (16, -16, 0, 0)], [(0, 0, 0, 0), (13, 8, 0, 0), (16, -16, 0, 0)], \
    [(0, 0, 0, 0), (13, 0, 0.6, 0.4), (16, 0, -3.0, -0.6)]
for hit in (22, 28, 34):
    big = hit == 34
    ar += [(hit - 3, 176 if big else 160, 20, 10), (hit - 1, 130, 26, 4), (hit, 104, 30, 0), (hit + 1, 108, 30, 0), (hit + 2, 120, 26, 4)]
    cs += [(hit - 3, -150, 0, -10), (hit, -64, 0, -10), (hit + 2, -80, 0, -10)]
    ch += [(hit - 3, 0, 14, 4), (hit, -16, 22, 0), (hit + 2, -12, 18, 0)]
    hd += [(hit - 3, 10, 10, 0), (hit, -22, 0, 0), (hit + 1, -18, 0, 8 if hit != 28 else -8), (hit + 2, -18, 0, 0)]
    bd += [(hit - 3, -10, 8, 0), (hit, -22 if big else -18, 14, 0), (hit + 2, -16, 12, 0)]
    bp += [(hit - 3, 0, -2.4, -0.6), (hit, 0, -3.6 if big else -3.2, -0.8), (hit + 2, 0, -3.0, -0.7)]
ar += [(40, 60, 10, 20), (46, 0, 0, 14), (50, *rest("arm_r"))]
cs += [(40, -20, 0, -20), (46, -6, 0, -10), (50, *rest("case"))]
ch += [(38, -6, 6, 0), (42, 10, 0, 0), (46, 0, 0, 0), (50, 0, 0, 0)]
hd += [(38, 20, 0, 0), (40, 26, 0, 8), (42, 10, 0, 0), (50, *rest("head"))]
bd += [(40, -12, 6, 0), (42, 4, 0, 0), (50, 0, 0, 0)]
bp += [(40, 0, -2.4, -0.6), (42, 0, 0.4, 0.2), (46, 0, 0, 0), (50, 0, 0, 0)]
a.rot("arm_r", *ar); a.rot("case", *cs); a.rot("chest", *ch); a.rot("head", *hd); a.rot("body", *bd); a.pos("body", *bp)
a.r("fore_r", (14, 10, 0, 0), (19, 20, 0, 0), (22, 0, 0, 0), (34, 0, 0, 0), (42, 20, 0, 0))
L(a, [(0, 0, 0, 2), (13, 0, 0, 4), (16, -34, 0, 10), (40, -34, 0, 10), (42, -10, 0, 4), (50, 0, 0, 2)],
  [(0, 4, 0, -4), (13, 6, 0, -4), (16, 20, 0, -10), (40, 20, 0, -10), (42, 10, 0, -4), (50, 4, 0, -4)],
  sr=[(0, 0, 0, 0), (13, 0, 0, 0), (16, -40, 0, 0), (40, -40, 0, 0), (42, -10, 0, 0), (50, 0, 0, 0)],
  sl=[(0, -8, 0, 0), (13, -8, 0, 0), (16, -60, 0, 0), (40, -60, 0, 0), (42, -20, 0, 0), (50, -8, 0, 0)],
  fr=[(0, 0, 0, 0), (16, 30, 0, 0), (40, 30, 0, 0), (50, 0, 0, 0)], fl=[(0, 6, 0, 0), (16, 30, 0, 0), (40, 30, 0, 0), (50, 6, 0, 0)])
a.hair([(0, 0, 0, 0), (10, -8, 0, 0), (16, 20, 0, 0), (19, -6, 0, 6), (22, 18, 0, 0), (25, -6, 0, -6), (28, 18, 0, 0), (31, -8, 0, 6), (34, 26, 0, 0),
        (38, 6, 0, 0), (42, -10, 0, 0), (50, 0, 0, 0)], delay=1)
a.coat([(0, 0, 0, 0), (13, -4, 0, 0), (16, 14, 0, 0), (22, 10, 0, 6), (28, 10, 0, -6), (34, 22, 0, 0), (40, 8, 0, 0), (44, -4, 0, 0), (50, 0, 0, 0)], delay=1)
a.done()

# ------------------------------------------------------------------ lethal_dose (ENRAGED signature, 60): coils with the syringe drawn back (0-6), dashes t8,
#   impales upward t12, hoists the victim on the needle (12-28, leaning back), slams the plunger home with the briefcase t30,
#   grinds (30-36, liquid drains), flings the body off with a whip of the syringe t40, recovers + refills
a = A("lethal_dose", 60)
a.puff(31, 40)
a.r("arm_l", (4, -30, 0, -20), (6, -36, 0, -22), (9, 30, 0, -10), (11, 100, 0, -2), (12, 112, 0, 0), (14, 108, 0, 0), (20, 128, 0, 0), (28, 140, 0, 0), (30, 136, 0, 0),
    (36, 138, 0, 0), (38, 150, 0, -4), (40, 50, 0, -6), (42, 40, 0, -8), (48, 30, 0, -12), (56, 6, 0, -14))
a.r("fore_l", (4, 80, 0, 0), (6, 86, 0, 0), (9, 40, 0, 0), (12, 0, 0, 0), (36, 0, 0, 0), (38, 20, 0, 0), (40, 0, 0, 0), (48, 30, 0, 0))
a.r("syr", (4, 50, 0, 0), (6, 56, 0, 0), (9, 30, 0, 0), (12, 0, 0, 0), (36, 0, 0, 0), (38, -20, 0, 0), (40, 30, 0, 0), (43, 40, 0, 0), (50, 10, 0, -8))
a.pos("plunger", (0, 0, 0, 0), (28, 0, 0, 0), (30, 0, -3.4, 0), (34, 0, -4.6, 0), (48, 0, -4.6, 0), (52, 0, 0.3, 0), (55, 0, 0, 0), (60, 0, 0, 0))
a.scl("liquid", (0, 1, 1, 1), (28, 1, 1, 1), (30, 1, 0.45, 1), (34, 1, 0.12, 1), (48, 1, 0.12, 1), (54, 1, 1.05, 1), (56, 1, 1, 1), (60, 1, 1, 1))
a.r("arm_r", (4, 30, 0, 24), (8, -40, 0, 30), (12, -50, 0, 34), (20, -30, 0, 30), (26, -60, 0, 30), (28, -66, 0, 28), (30, 120, 40, 0), (32, 116, 40, 0), (36, 118, 40, 0),
    (38, 40, 0, 20), (40, -30, 0, 34), (46, -10, 0, 20), (56, *rest("arm_r")))
a.r("fore_r", (8, 30, 0, 0), (28, 40, 0, 0), (30, 0, 0, 0), (36, 0, 0, 0), (40, 20, 0, 0))
a.r("case", (8, 10, 0, -26), (28, 40, 0, -20), (30, -110, 0, -10), (36, -110, 0, -10), (40, 30, 0, -30), (46, -10, 0, -16))
a.r("chest", (4, 4, 26, 0), (6, 6, 30, 0), (9, -4, 0, 0), (12, -6, -20, 0), (20, 8, -14, 0), (28, 14, -10, 0), (30, 6, 24, 0), (36, 6, 22, 0), (38, 12, 0, 0),
    (40, -20, -16, 0), (44, -14, -10, 0), (52, 0, 0, 0))
a.r("head", (4, -10, -14, 0), (8, -14, 0, 0), (12, 10, 10, 0), (20, 24, 10, 0), (28, 30, 10, 0), (30, 20, -10, 0), (32, 20, -10, 8), (34, 20, -10, -8), (36, 22, -10, 4),
    (40, -14, 10, 0), (46, -6, 6, 0), (52, 4, 0, 12), (55, 4, 0, -8), (58, 2, 0, -4))
a.rot("body", (0, 0, 0, 0), (4, -16, 8, 0), (6, -20, 10, 0), (9, -34, 0, 0), (11, -20, -10, 0), (12, -4, -14, 0), (20, 8, -10, 0), (28, 12, -8, 0), (30, 0, 10, 0), (36, 2, 8, 0),
      (38, 8, 0, 0), (40, -22, -10, 0), (44, -16, -6, 0), (52, 0, 0, 0), (60, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (4, 0, -2.4, 1.0), (6, 0, -2.8, 1.2), (9, 0, -1.6, -1.2), (12, 0, -1.2, -1.6), (20, 0, -1.0, -1.0), (28, 0, -0.8, -0.6), (30, 0, -1.4, -1.2),
      (36, 0, -1.2, -1.0), (40, 0, -2.0, -2.0), (44, 0, -1.6, -1.6), (52, 0, 0, 0), (60, 0, 0, 0))
L(a, [(0, 0, 0, 2), (4, 40, 0, 4), (6, 46, 0, 4), (8, -30, 0, 4), (10, 50, 0, 4), (12, -24, 0, 6), (28, -30, 0, 8), (30, -34, 0, 8), (40, -40, 0, 6), (44, -34, 0, 4), (52, 0, 0, 2), (60, 0, 0, 2)],
  [(0, 4, 0, -4), (4, -20, 0, -4), (6, -24, 0, -4), (8, 50, 0, -4), (10, -10, 0, -4), (12, 40, 0, -6), (28, 34, 0, -8), (30, 40, 0, -8), (40, 50, 0, -6), (44, 40, 0, -4),
   (52, 4, 0, -4), (60, 4, 0, -4)],
  sr=[(0, 0, 0, 0), (4, -80, 0, 0), (6, -90, 0, 0), (8, -10, 0, 0), (10, -70, 0, 0), (12, -10, 0, 0), (40, -10, 0, 0), (52, 0, 0, 0), (60, 0, 0, 0)],
  sl=[(0, -8, 0, 0), (4, -40, 0, 0), (8, -60, 0, 0), (10, -10, 0, 0), (12, -30, 0, 0), (28, -20, 0, 0), (40, -40, 0, 0), (52, -8, 0, 0), (60, -8, 0, 0)],
  fl=[(0, 6, 0, 0), (12, -14, 0, 0), (40, -20, 0, 0), (52, 6, 0, 0), (60, 6, 0, 0)])
a.hair([(0, 0, 0, 0), (6, 8, 0, -6), (9, -24, 0, 0), (12, -10, 0, 8), (20, -12, 0, 4), (28, -16, 0, 0), (30, 6, 0, -10), (32, 0, 0, 8), (34, 0, 0, -8), (38, -10, 0, 0),
        (41, 24, 0, 6), (46, 6, 0, 0), (52, 0, 0, 10), (55, 0, 0, -8), (60, 0, 0, 0)], delay=1)
a.coat([(0, 0, 0, 0), (6, 6, 0, -4), (9, -30, 0, 0), (12, -10, 0, 6), (20, -8, 0, 4), (30, 4, 0, -8), (38, -10, 0, 0), (41, 22, 0, 6), (48, 4, 0, 0), (60, 0, 0, 0)], delay=1)
a.done()

# ================================================================== crowd control
# ------------------------------------------------------------------ paralytic_jab (30): sidles in, syringe cocked by her cheek like a dart (0-8),
#   darts it into the victim's neck t11, leans in and slowly empties the plunger (11-17, paralytic), yanks it out 19, plunger springs back
a = A("paralytic_jab", 30)
a.r("arm_l", (3, -10, 0, -20), (6, -28, 0, -18), (8, -30, 0, -16), (10, 80, 0, -4), (11, 100, 0, 0), (17, 98, 0, 0), (19, 70, 0, -6), (21, 50, 0, -10), (27, 12, 0, -14))
a.r("fore_l", (3, 70, 0, 0), (6, 104, 0, 0), (8, 108, 0, 0), (10, 20, 0, 0), (11, 0, 0, 0), (17, 2, 0, 0), (19, 40, 0, 0), (24, 30, 0, 0))
a.r("syr", (3, 40, 0, 0), (6, 66, 0, 0), (8, 70, 0, 0), (10, 10, 0, 0), (11, 0, 0, 0), (17, 0, 0, 0), (19, 20, 0, 0), (23, 30, 0, -10), (26, 8, 0, -8))
a.r("hand_l", (8, 0, 0, 0), (11, 0, 0, 6), (13, 0, 0, -4), (15, 0, 0, 6), (17, 0, 0, 0))
a.pos("plunger", (0, 0, 0, 0), (11, 0, 0, 0), (12, 0, -0.8, 0), (15, 0, -2.6, 0), (17, 0, -4.4, 0), (22, 0, -4.4, 0), (25, 0, 0.4, 0), (27, 0, 0, 0), (30, 0, 0, 0))
a.scl("liquid", (0, 1, 1, 1), (11, 1, 1, 1), (15, 1, 0.55, 1), (17, 1, 0.2, 1), (22, 1, 0.2, 1), (26, 1, 1.05, 1), (28, 1, 1, 1), (30, 1, 1, 1))
a.r("arm_r", (4, 10, 0, 18), (8, 14, 0, 22), (11, -44, 0, 34), (17, -40, 0, 32), (20, -20, 0, 24), (27, -4, 0, 12))
a.r("fore_r", (8, 20, 0, 0), (11, 6, 0, 0), (20, 16, 0, 0))
a.r("case", (8, -10, 0, -20), (11, 34, 0, -34), (14, 14, 0, -30), (20, -14, 0, -18), (26, -4, 0, -10))
a.r("chest", (4, 2, 14, 0), (8, 4, 22, 0), (11, -10, -18, 0), (17, -12, -16, 0), (20, -2, -6, 0), (26, 0, 0, 0))
a.r("head", (3, -4, -10, 12), (8, -6, -18, 16), (11, -14, 14, 0), (14, -16, 12, 10), (17, -16, 12, 12), (20, -4, 6, -6), (24, 4, 0, 8), (28, 2, 0, -4))
a.rot("body", (0, 0, 0, 0), (4, 2, 8, 0), (8, 4, 12, 0), (11, -12, -12, 0), (17, -12, -10, 0), (21, -4, -2, 0), (30, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (4, 1.2, -0.6, 0.4), (8, 1.6, -0.8, 0.6), (11, 0.6, -1.4, -2.0), (17, 0.6, -1.4, -2.0), (21, 0.2, -0.6, -0.6), (30, 0, 0, 0))
L(a, [(0, 0, 0, 2), (4, 10, 0, 8), (8, 12, 0, 6), (11, -26, 0, 4), (17, -24, 0, 4), (22, -8, 0, 2), (30, 0, 0, 2)],
  [(0, 4, 0, -4), (4, -4, 0, -2), (8, -10, 0, -4), (11, 40, 0, -4), (17, 38, 0, -4), (22, 14, 0, -4), (30, 4, 0, -4)],
  sr=[(0, 0, 0, 0), (8, -24, 0, 0), (11, -8, 0, 0), (30, 0, 0, 0)], sl=[(0, -8, 0, 0), (8, -20, 0, 0), (11, -26, 0, 0), (17, -26, 0, 0), (30, -8, 0, 0)],
  fl=[(0, 6, 0, 0), (11, -14, 0, 0), (17, -14, 0, 0), (30, 6, 0, 0)])
a.hair([(0, 0, 0, 0), (8, 4, 0, -8), (11, -12, 0, 8), (14, -6, 0, 4), (18, -6, 0, 6), (22, 4, 0, -4), (30, 0, 0, 0)], delay=1)
a.coat([(0, 0, 0, 0), (8, 2, 0, -6), (11, -10, 0, 6), (16, -6, 0, 4), (22, 2, 0, 0), (30, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ knockout_gas (42): turns her right side to the target and lifts the briefcase out
#   at arm's length (0-8), flicks the latches 8-10, the lid bursts open t12 and knockout gas billows out in three shaken pumps t14 / t20 / t26,
#   snaps the lid shut t32, turns back
a = A("knockout_gas", 42)
a.scl("case_gas", (0, *HIDE), (12, *HIDE), (13, 0.35, 0.35, 0.35), (14, 0.8, 0.8, 0.8), (17, 0.9, 0.9, 0.9), (20, 1.15, 1.15, 1.15), (23, 1.0, 1.0, 1.0),
      (26, 1.3, 1.3, 1.3), (30, 1.1, 1.1, 1.1), (32, 0.4, 0.4, 0.4), (33, *HIDE), (42, *HIDE))
a.pos("case_gas", (0, 0, 0, 0), (13, 0, 0, 0), (14, 1.0, 0, 0), (17, 0.4, 0.3, 0), (20, 2.0, 0.2, 0), (23, 0.8, 0.6, 0), (26, 2.6, 0.4, 0), (30, 3.4, 1.0, 0), (32, 0.5, 0, 0), (42, 0, 0, 0))
a.rot("case_gas", (0, 0, 0, 0), (14, 0, 0, 0), (20, 20, 0, 0), (26, -20, 0, 0), (32, 0, 0, 0), (42, 0, 0, 0))
a.r("lid", (8, 0, 0, 0), (9, 0, 0, 8), (10, 0, 0, 0), (11, 0, 0, 6), (12, 0, 0, 100), (13, 0, 0, 86), (14, 0, 0, 96), (20, 0, 0, 104), (26, 0, 0, 106),
    (30, 0, 0, 96), (32, 0, 0, 0), (33, 0, 0, 6), (34, 0, 0, 0))
a.r("arm_r", (4, 10, 0, 50), (8, 6, 0, 76), (12, 4, 0, 82), (14, 10, 0, 74), (16, 2, 0, 82), (20, 10, 0, 72), (22, 2, 0, 82), (26, 12, 0, 70), (28, 2, 0, 80),
    (32, 0, 0, 84), (34, 4, 0, 74), (38, 0, 0, 30))
a.r("fore_r", (4, 20, 0, 0), (8, 6, 0, 0), (32, 6, 0, 0), (38, 14, 0, 0))
a.r("case", (4, 0, 0, -50), (8, 0, 0, -78), (12, 0, 0, -86), (14, 0, 0, -70), (16, 0, 0, -84), (20, 0, 0, -68), (22, 0, 0, -84), (26, 0, 0, -66), (28, 0, 0, -82),
    (32, 0, 0, -86), (34, 0, 0, -74), (38, -4, 0, -30))
a.r("hand_r", (8, 0, 0, 0), (9, 0, 0, -8), (10, 0, 0, 6), (11, 0, 0, -6), (12, 0, 0, 0))
a.r("arm_l", (4, 30, 0, 10), (8, 50, 0, 30), (12, 54, 0, 34), (32, 54, 0, 34), (36, 20, 0, 0))
a.r("fore_l", (4, 40, 0, 0), (8, 60, 0, 0), (32, 60, 0, 0), (36, 30, 0, 0))
a.r("syr", (8, -60, 0, 20), (32, -60, 0, 20), (36, -10, 0, 0))
a.r("chest", (4, 0, 20, 0), (8, 0, 30, 0), (12, -4, 34, 0), (14, 2, 34, 0), (20, -4, 34, 0), (26, -6, 36, 0), (32, 0, 30, 0), (36, 0, 10, 0))
a.r("head", (4, 0, -16, 0), (8, -4, -40, 0), (12, -2, -50, 6), (20, 0, -52, -4), (26, -4, -52, 6), (30, 6, -50, 0), (32, 0, -44, 0), (36, 0, -14, -4))
a.rot("body", (0, 0, 0, 0), (4, 0, 24, 0), (8, 0, 34, 0), (12, -4, 36, -4), (20, -4, 36, -4), (26, -6, 38, -5), (32, 0, 34, 0), (36, 0, 10, 0), (42, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (8, 0, -0.8, 0), (12, 0, -1.2, -0.3), (26, 0, -1.2, -0.4), (32, 0, -0.8, 0), (42, 0, 0, 0))
L(a, [(0, 0, 0, 2), (6, 4, 0, 10), (32, 4, 0, 10), (38, 0, 0, 4), (42, 0, 0, 2)], [(0, 4, 0, -4), (6, 12, 0, -10), (32, 12, 0, -10), (38, 6, 0, -4), (42, 4, 0, -4)],
  sr=[(0, 0, 0, 0), (6, -16, 0, 0), (32, -16, 0, 0), (42, 0, 0, 0)], sl=[(0, -8, 0, 0), (6, -22, 0, 0), (32, -22, 0, 0), (42, -8, 0, 0)])
a.hair([(0, 0, 0, 0), (8, 0, 0, -10), (12, -6, 0, 8), (14, 0, 0, -4), (20, -4, 0, 6), (26, -6, 0, 8), (32, 4, 0, -8), (36, 0, 0, 6), (42, 0, 0, 0)], delay=1)
a.coat([(0, 0, 0, 0), (8, 0, 0, -8), (12, -2, 0, 6), (20, -2, 0, 4), (26, -4, 0, 6), (34, 2, 0, -6), (42, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ specimen_grab (64): lets the briefcase drop at her feet (2-7), coils (4-8), lunges and
#   snatches the victim by the collar t10, hoists it up at arm's length (10-18, leaning back), drives the syringe into it three times t20 / t28 / t36
#   (plunger steps down, paralytic), heaves it overhead 38-41 and slams it to the floor t44, squats to pick the briefcase back up (52-56), stands
a = A("specimen_grab", 64)
a.scl("case", (0, 1, 1, 1), (3, 1, 1, 1), (4, *HIDE), (55, *HIDE), (56, 1, 1, 1), (64, 1, 1, 1))
a.scl("case_drop", (0, *HIDE), (3, *HIDE), (4, 1, 1, 1), (55, 1, 1, 1), (56, *HIDE), (64, *HIDE))
a.pos("case_drop", (0, 0, 7, 0), (4, 0, 7, 0), (6, 0, 0.6, 0), (7, 0, 0, 0), (8, 0, 0.5, 0), (9, 0, 0, 0), (55, 0, 0, 0), (56, 0, 7, 0), (64, 0, 7, 0))
a.rot("case_drop", (0, 0, 0, 0), (4, 0, 0, 0), (7, 0, 0, -10), (8, 0, 0, 6), (10, 0, 0, 0), (64, 0, 0, 0))
# right arm: open hand 3, cock back 6-8, snatch 10, hoist 18, hold (squeezes 24/32), heave 38-41, slam 44, reach down for the case 52-55
a.r("arm_r", (3, 6, 0, 14), (6, -40, 0, 20), (8, -44, 0, 22), (10, 96, 0, -4), (12, 104, 0, -6), (18, 140, 0, -8), (20, 136, 0, -8), (24, 142, 0, -10),
    (28, 136, 0, -8), (32, 142, 0, -10), (36, 136, 0, -8), (38, 160, 0, -4), (41, 178, 0, 0), (43, 90, 0, 0), (44, 50, 0, 4), (46, 44, 0, 6),
    (50, 10, 0, 16), (53, 30, 0, 24), (55, 34, 0, 26), (58, 10, 0, 16))
a.r("fore_r", (3, 10, 0, 0), (6, 70, 0, 0), (8, 80, 0, 0), (10, 4, 0, 0), (18, 0, 0, 0), (38, 10, 0, 0), (41, 30, 0, 0), (44, 0, 0, 0), (50, 10, 0, 0),
    (55, 20, 0, 0), (58, 14, 0, 0))
a.r("hand_r", (2, 0, 0, 0), (3, 0, 0, -20), (5, 0, 0, 0), (9, 0, 0, 0), (10, -20, 0, 0), (12, 10, 0, 0), (24, 16, 0, 0), (26, 6, 0, 0), (32, 16, 0, 0),
    (34, 6, 0, 0), (44, -30, 0, 0), (46, 0, 0, 0))
# left arm / syringe: cocked back, three upward stabs into the held body
al, fl, sy = [(4, -20, 0, -20), (8, -24, 0, -22), (14, -10, 0, -18), (17, -30, 0, -20)], [(4, 60, 0, 0), (8, 70, 0, 0), (17, 90, 0, 0)], [(4, 40, 0, 0), (8, 50, 0, 0), (17, 60, 0, 0)]
for h in (20, 28, 36):
    al += [(h - 1, 90, 0, -4), (h, 122, 0, 0), (h + 3, 120, 0, 0), (h + 5, -24, 0, -20)]
    fl += [(h - 1, 20, 0, 0), (h, 0, 0, 0), (h + 3, 0, 0, 0), (h + 5, 90, 0, 0)]
    sy += [(h - 1, 10, 0, 0), (h, 0, 0, 0), (h + 3, 0, 0, 0), (h + 5, 60, 0, 0)]
al, fl, sy = al[:-1], fl[:-1], sy[:-1]  # stay out after the last stab
al += [(44, -10, 0, -30), (50, 10, 0, -20), (56, 24, 0, -20), (62, 8, 0, -14)]
fl += [(44, 60, 0, 0), (50, 40, 0, 0), (60, 22, 0, 0)]
sy += [(44, 20, 0, -10), (50, 10, 0, -10), (60, 8, 0, -8)]
a.r("arm_l", *al); a.r("fore_l", *fl); a.r("syr", *sy)
a.pos("plunger", (0, 0, 0, 0), (20, 0, 0, 0), (22, 0, -1.5, 0), (28, 0, -1.5, 0), (30, 0, -3.0, 0), (36, 0, -3.0, 0), (38, 0, -4.5, 0), (52, 0, -4.5, 0),
      (56, 0, 0.3, 0), (58, 0, 0, 0), (64, 0, 0, 0))
a.scl("liquid", (0, 1, 1, 1), (20, 1, 1, 1), (22, 1, 0.7, 1), (28, 1, 0.7, 1), (30, 1, 0.42, 1), (36, 1, 0.42, 1), (38, 1, 0.14, 1), (52, 1, 0.14, 1),
      (57, 1, 1.05, 1), (59, 1, 1, 1), (64, 1, 1, 1))
a.r("chest", (4, 4, 0, 0), (8, 8, 10, 0), (10, -10, -10, 0), (18, 10, -4, 0), (20, 4, -14, 0), (23, 10, -4, 0), (28, 4, -14, 0), (31, 10, -4, 0), (36, 4, -14, 0),
    (39, 16, 0, 0), (41, 20, 0, 0), (44, -24, 0, 0), (47, -20, 0, 0), (50, -6, 0, 0), (54, -20, 0, 8), (57, -14, 0, 4), (62, 0, 0, 0))
a.r("head", (2, -16, 0, 6), (4, -20, 0, 0), (8, -8, 0, 0), (10, 4, -6, 0), (18, 26, 0, 0), (20, 22, 6, 0), (24, 28, 0, 8), (28, 22, 6, 0), (32, 28, 0, -8),
    (36, 22, 6, 0), (41, 30, 0, 0), (44, -24, 0, 0), (46, -20, 0, 6), (48, -14, 0, -4), (54, -26, 0, 0), (60, 0, 0, -4))
a.rot("body", (0, 0, 0, 0), (4, -6, 0, 0), (8, -14, 6, 0), (10, -16, -6, 0), (14, 4, 0, 0), (18, 10, 0, 0), (36, 10, 0, 0), (39, 14, 0, 0), (41, 16, 0, 0),
      (44, -26, 0, 0), (47, -22, 0, 0), (50, -6, 0, 0), (54, -30, -10, 4), (56, -28, -10, 4), (60, -6, 0, 0), (64, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (4, 0, -1.0, 0.4), (8, 0, -1.8, 0.8), (10, 0, -1.2, -1.8), (14, 0, -0.6, -1.2), (18, 0, -0.4, -0.4), (36, 0, -0.4, -0.4),
      (41, 0, -0.2, 0.2), (44, 0, -2.4, -1.8), (47, 0, -2.0, -1.6), (50, 0, -0.6, -0.6), (54, 0.8, -3.0, -0.6), (56, 0.8, -3.0, -0.6), (60, 0.2, -0.6, 0), (64, 0, 0, 0))
L(a, [(0, 0, 0, 2), (4, 10, 0, 4), (8, 20, 0, 4), (10, -24, 0, 6), (14, -20, 0, 8), (36, -20, 0, 8), (41, -14, 0, 6), (44, -30, 0, 6), (48, -26, 0, 6),
      (52, 30, 0, 8), (56, 36, 0, 8), (60, 8, 0, 4), (64, 0, 0, 2)],
  [(0, 4, 0, -4), (4, 0, 0, -4), (8, -16, 0, -4), (10, 40, 0, -6), (14, 30, 0, -8), (36, 30, 0, -8), (41, 24, 0, -6), (44, 46, 0, -6), (48, 40, 0, -6),
   (52, 20, 0, -6), (56, 24, 0, -6), (60, 8, 0, -4), (64, 4, 0, -4)],
  sr=[(0, 0, 0, 0), (8, -40, 0, 0), (10, -6, 0, 0), (36, -6, 0, 0), (44, -10, 0, 0), (52, -60, 0, 0), (56, -66, 0, 0), (60, -16, 0, 0), (64, 0, 0, 0)],
  sl=[(0, -8, 0, 0), (8, -24, 0, 0), (10, -24, 0, 0), (36, -24, 0, 0), (44, -50, 0, 0), (48, -44, 0, 0), (52, -40, 0, 0), (56, -46, 0, 0), (60, -14, 0, 0), (64, -8, 0, 0)],
  fl=[(0, 6, 0, 0), (10, -12, 0, 0), (44, -20, 0, 0), (52, 10, 0, 0), (64, 6, 0, 0)])
a.hair([(0, 0, 0, 0), (4, 8, 0, 0), (8, 4, 0, 4), (10, -20, 0, -4), (14, -6, 0, 0), (18, -14, 0, 0), (20, -10, 0, 6), (28, -10, 0, 6), (36, -10, 0, 6),
        (41, -18, 0, 0), (44, 26, 0, 0), (47, 10, 0, 0), (54, 16, 0, -6), (58, 0, 0, 4), (64, 0, 0, 0)], delay=1)
a.coat([(0, 0, 0, 0), (8, 6, 0, 0), (10, -18, 0, -4), (15, -8, 0, 0), (20, -2, 0, 4), (36, -2, 0, 4), (41, -8, 0, 0), (44, 18, 0, 0), (48, 6, 0, 0),
        (54, 14, 0, -6), (60, 0, 0, 0), (64, 0, 0, 0)], delay=1)
a.done()

os.makedirs(os.path.dirname(OUT), exist_ok=True)
m.save(OUT)
print("cubes", len(m.cubes), "anims", [x["name"] for x in m.anims], "maxY", max(c["to"][1] for c in m.cubes), "atlas rows", m.cy + m.rowh)
