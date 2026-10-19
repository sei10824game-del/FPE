"""Green Thavel (FPE Green, lab teacher) - generates assets/fpe/bbmodels/green_thavel.bbmodel.
Reference: docs/ref/confirmed/green_thavel.jpg - messy shoulder-length near-black hair, two small white antler-like horns
on top, green goggles pushed up on the head, pale face with closed happy eyes and a wide toothy grin, long white lab coat
(open, rolled cuffs, pockets) with a green lanyard + ID badge and a small green triangle pin, black high-waisted skirt,
BIG lime-green gloves each holding a clipboard, tall lime-green boots with flared cuffs.
Blockbench space: Y up, ground 0, faces -Z. Character's RIGHT = +X.
Rotation signs (file values): arm/leg rx>0 = swing forward, torso/head rx>0 = lean back / look up,
ry>0 = turn to the character's left, rz>0 = hanging part swings toward +X (character's right).
Melee-only moveset; every key tick matches entity/characters/GreenThavel.java.
Run: python3 tools/bbgen/chars/green_thavel.py
"""
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from bbgen import Model, mix  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "../../../src/main/resources/assets/fpe/bbmodels/green_thavel.bbmodel")

# ------------------------------------------------------------------ palette
HAIR, HAIR_HI, HAIR_D = 0x221E28, 0x3E3848, 0x110F16
SKIN, SKIN_D = 0xF4F1EC, 0xCFCAD0
COAT, COAT_D, COAT_L = 0xF1F2EF, 0xC4C8CC, 0xFFFFFF
DRESS, DRESS_D, DRESS_L = 0x1E1D24, 0x101015, 0x34333D
GRN, GRN_D, GRN_L, GRN_DD = 0x9CCB3B, 0x5F8A1E, 0xC9EC74, 0x3C5A12
HORN, HORN_D = 0xF6F5F1, 0xB9B8BE
BOARD, BOARD_D = 0x9A7B55, 0x6A5236
PAPER, PAPER_D, INKL = 0xFBFBF8, 0xD6D8D4, 0x9AA0A8
STEEL, STEEL_D = 0xC8CCD2, 0x7E848C
LENS, LENS_L = 0x7FD23A, 0xD4FF8E
MOUTH, TEETH, LINE = 0x2A1218, 0xFFFFFF, 0x15121A
TOX, TOX_L = 0x8CFF3A, 0xE8FFB0

m = Model("green_thavel", S=8, atlas=2048)
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
                cc = mix(c, dark, 0.4 * abs(y / max(1, F.h - 1) - 0.35))
                if (x + y // 6) % 4 == 0 and R.random() < 0.4: cc = mix(cc, hi, 0.5)
                F.px(x, y, cc)
    return f


HS = strands()


def folds(base, dark, light, n=3, hem=True):
    def f(F):
        for i in range(n):
            x = int((i + 0.5) * F.w / n) + R.randint(-1, 1)
            for y in range(F.h):
                k = y / max(1, F.h - 1)
                F.px(x, y, mix(base, dark, 0.2 + 0.35 * k))
                F.px(x + 1, y, mix(base, light, 0.3 * k))
        if hem: F.rect(0, F.h - 2, F.w, 2, mix(base, dark, 0.4))
    return f


def outline(c):
    return lambda F: (F.rect(0, 0, F.w, 1, c), F.rect(0, F.h - 1, F.w, 1, c), F.rect(0, 0, 1, F.h, c), F.rect(F.w - 1, 0, 1, F.h, c))


def glove(F):
    for y in range(F.h):
        for x in range(F.w):
            c = mix(GRN_L, GRN, min(1, y / max(1, F.h - 1) * 1.4))
            if x < 2 or x >= F.w - 2: c = mix(c, GRN_D, 0.45)
            F.px(x, y, c)
    F.rect(F.w // 4, 2, 2, max(1, F.h // 3), mix(GRN_L, 0xFFFFFF, 0.4))  # gloss streak


def boot(F):
    for y in range(F.h):
        for x in range(F.w):
            c = mix(GRN_L, GRN_D, (y / max(1, F.h - 1)) ** 1.5 * 0.8)
            if x < 2 or x >= F.w - 2: c = mix(c, GRN_DD, 0.35)
            F.px(x, y, c)
    F.rect(F.w // 3, 3, 2, F.h - 8, mix(GRN_L, 0xFFFFFF, 0.35))


def paper(F):
    F.rect(0, 0, F.w, F.h, PAPER)
    F.rect(0, 0, F.w, 2, BOARD_D)
    for y in range(9, F.h - 4, 4):
        ln = F.w - 8 - R.randint(0, 10)
        F.rect(4, y, ln, 1, INKL)
    F.rect(4, 9, 3, 3, GRN)  # little green checkbox column
    F.rect(4, 21, 3, 3, GRN)
    F.rect(F.w // 2 - 5, 2, 10, 5, STEEL)  # clip
    F.rect(F.w // 2 - 3, 3, 6, 2, STEEL_D)
    outline(PAPER_D)(F)


def board_back(F):
    for y in range(F.h):
        for x in range(F.w):
            F.px(x, y, mix(BOARD, BOARD_D, 0.25 + 0.3 * ((x * 7 + y * 3) % 11) / 11))
    outline(BOARD_D)(F)


def face_front(F):
    W, H = F.w, F.h  # 54 x 54
    for y in range(H):
        for x in range(W):
            F.px(x, y, mix(SKIN, SKIN_D, max(0, (14 - y) / 14) * 0.6))
    # closed, happy "^ ^" eyes (thick arcs) + lashes
    for cx in (14, 40):
        for i in range(-8, 9):
            F.disc(cx + i, 28 - (64 - i * i) / 10.0, 1.9, LINE)
        F.rect(cx + 7 if cx > 27 else cx - 10, 19, 3, 3, LINE)  # outer lash flick
    # wide grin, corners hooked up, upper teeth row
    cx = W / 2
    for x in range(8, W - 8):
        u = (x + .5 - cx) / (cx - 8)
        top = 35 - 4.5 * u * u
        bot = 46 - 11 * u * u
        if bot <= top + 0.5: continue
        for y in range(int(top), int(bot) + 1):
            F.px(x, y, MOUTH)
        F.px(x, int(top) - 1, LINE); F.px(x, int(bot) + 1, LINE)
        if bot - top > 3:
            for y in range(int(top), int(top + min(3, (bot - top) * 0.35)) + 1):
                F.px(x, y, TEETH if x % 4 else PAPER_D)
    F.disc(cx, 44, 2.4, 0xB0485A)  # tongue hint
    F.rect(6, 30, 4, 1, mix(SKIN, 0xB8E07A, 0.5)); F.rect(44, 30, 4, 1, mix(SKIN, 0xB8E07A, 0.5))


def coat_front(F):
    W, H = F.w, F.h
    folds(COAT, COAT_D, COAT_L, 2, hem=False)(F)
    g0, g1 = W // 2 - 6, W // 2 + 6  # open front: black dress under a white collar
    for y in range(H):
        for x in range(g0, g1):
            F.px(x, y, DRESS if y > 18 else COAT_L)
    F.poly([(g0, 0), (W / 2, 18), (g1, 0)], DRESS)
    F.poly([(g0 + 2, 0), (W / 2, 12), (g1 - 2, 0)], COAT_L)
    F.rect(g0 - 1, 0, 1, H, COAT_D); F.rect(g1, 0, 1, H, COAT_D)
    # green lanyard V
    F.line(g0 + 1, 0, W / 2 - 1, 20, GRN, 1.4); F.line(g1 - 1, 0, W / 2 + 1, 20, GRN, 1.4)


def skirt_paint(F):
    for y in range(F.h):
        for x in range(F.w):
            c = DRESS
            if x % 6 == 0: c = DRESS_D
            elif x % 6 == 1: c = DRESS_L
            F.px(x, y, mix(c, DRESS_D, 0.4 * y / max(1, F.h - 1)))


def glow_fill(c1, c2):
    def f(F):
        for y in range(F.h):
            for x in range(F.w):
                c = mix(c1, c2, y / max(1, F.h - 1))
                if R.random() < 0.25: c = mix(c, 0xFFFFFF, 0.4)
                F.px(x, y, c, glow=True)
    return f


GF = lambda a, b: (lambda fs: [glow_fill(a, b)(f) for f in fs.values()])


def lens(F):
    for y in range(F.h):
        for x in range(F.w):
            F.px(x, y, mix(LENS_L, LENS, (x + y) / max(1, F.w + F.h)), glow=True)
    F.rect(1, 1, 2, 2, 0xFFFFFF, glow=True)


# ------------------------------------------------------------------ skeleton
m.group("root", (0, 0, 0))
m.group("body", (0, 17, 0), parent="root")
m.group("skirt_f", (0, 18.5, -1.9), parent="body")
m.group("skirt_b", (0, 18.5, 1.9), parent="body")
m.group("skirt_r", (2.7, 18.5, 0), parent="body")
m.group("skirt_l", (-2.7, 18.5, 0), parent="body")
m.group("coat_b", (0, 19.6, 2.1), parent="body")
m.group("coat_b2", (0, 15.2, 2.5), parent="coat_b")
m.group("coat_fr", (2.0, 19.6, -2.1), parent="body")
m.group("coat_fl", (-2.0, 19.6, -2.1), parent="body")
m.group("coat_sr", (3.0, 19.6, 0.2), parent="body")
m.group("coat_sl", (-3.0, 19.6, 0.2), parent="body")
m.group("chest", (0, 19, 0), parent="body")
m.group("badge", (0, 24.6, -2.2), parent="chest")
m.group("head", (0, 27.4, 0), parent="chest")
m.group("goggles", (0, 31.0, 0), parent="head")
m.group("bangs", (0, 34.0, -3.2), parent="head")
m.group("hair_b", (0, 33.5, 2.6), parent="head")
m.group("hair_r", (3.4, 33.0, 0.4), parent="head")
m.group("hair_l", (-3.4, 33.0, 0.4), parent="head")
m.group("horn_r", (1.9, 35.6, 0.6), parent="head")
m.group("horn_l", (-1.9, 35.6, 0.6), parent="head")
for s, k in ((1, "r"), (-1, "l")):
    m.group("arm_" + k, (3.9 * s, 26.2, 0), parent="chest")
    m.group("fore_" + k, (3.9 * s, 22.2, 0), parent="arm_" + k)
    m.group("hand_" + k, (3.9 * s, 18.4, 0), parent="fore_" + k)
    m.group("board_" + k, (3.9 * s, 14.0, 0), parent="hand_" + k)
    m.group("tox_" + k, (3.9 * s, 15.5, 0), parent="hand_" + k)
    m.group("leg_" + k, (1.35 * s, 16.0, 0), parent="root")
    m.group("shin_" + k, (1.35 * s, 9.6, 0), parent="leg_" + k)
    m.group("foot_" + k, (1.35 * s, 1.8, 0.2), parent="shin_" + k)

# ------------------------------------------------------------------ legs: black tights, tall lime boots with flared cuffs
for s, k in ((1, "r"), (-1, "l")):
    x = 1.35 * s
    m.cube("thigh_" + k, "leg_" + k, (x - 1.1, 9.4, -1.1), (x + 1.1, 16.2, 1.1), DRESS_L, color2=DRESS, grad=True)
    m.cube("boot_" + k, "shin_" + k, (x - 1.25, 1.6, -1.3), (x + 1.25, 9.8, 1.3), GRN, faces=all_faces(boot, ("up", "down")))
    m.cube("bcuff_" + k, "shin_" + k, (x - 1.6, 8.6, -1.65), (x + 1.6, 10.6, 1.65), GRN_L, color2=GRN, grad=True,
           faces={"north": lambda F: F.rect(0, F.h - 2, F.w, 2, GRN_D)})
    m.cube("bcuffr_" + k, "shin_" + k, (x - 1.75, 10.3, -1.8), (x + 1.75, 10.8, 1.8), GRN_D)
    m.cube("bstrap_" + k, "shin_" + k, (x - 1.32, 4.2, -1.38), (x + 1.32, 4.8, 1.38), GRN_D)
    m.cube("foot_" + k, "foot_" + k, (x - 1.3, 0.4, -3.1), (x + 1.3, 2.2, 1.35), GRN, color2=GRN_D, grad=True)
    m.cube("toe_" + k, "foot_" + k, (x - 1.0, 0.4, -3.8), (x + 1.0, 1.8, -2.6), GRN_L, color2=GRN, grad=True)
    m.cube("sole_" + k, "foot_" + k, (x - 1.35, 0.0, -3.9), (x + 1.35, 0.5, 1.4), GRN_DD)

# ------------------------------------------------------------------ hips: black skirt + open lab-coat tails
m.cube("hips", "body", (-2.8, 15.6, -1.85), (2.8, 19.6, 1.85), DRESS, faces=all_faces(skirt_paint, ("up", "down")))
m.cube("waist", "body", (-2.65, 19.0, -1.75), (2.65, 19.9, 1.75), DRESS_L)
m.cube("sk_f", "skirt_f", (-2.7, 10.8, -2.3), (2.7, 18.6, -1.7), DRESS, origin=(0, 18.5, -1.9), rot=(5, 0, 0), faces=all_faces(skirt_paint))
m.cube("sk_b", "skirt_b", (-2.6, 11.0, 1.2), (2.6, 18.6, 1.8), DRESS, origin=(0, 18.5, 1.9), rot=(-5, 0, 0), faces=all_faces(skirt_paint))
for s, k in ((1, "r"), (-1, "l")):
    m.cube("sk_" + k, "skirt_" + k, (2.7 * s - 0.35, 10.8, -2.2), (2.7 * s + 0.35, 18.6, 2.2), DRESS, origin=(2.7 * s, 18.5, 0), rot=(0, 0, 5 * s),
           faces=all_faces(skirt_paint))
# coat tails: back panel (2 segments, centre slit), front flaps with pockets, side panels
m.cube("cb_up", "coat_b", (-3.1, 15.0, 2.0), (3.1, 19.8, 2.6), COAT, color2=COAT_D, grad=True, faces={"south": folds(COAT, COAT_D, COAT_L, 3, False)})
m.cube("cb_lo", "coat_b2", (-3.2, 11.4, 2.25), (3.2, 15.4, 2.85), COAT, color2=COAT_D, grad=True,
       faces={"south": combo(folds(COAT, COAT_D, COAT_L, 3), lambda F: F.rect(F.w // 2, 0, 1, F.h, COAT_D))})
for s, k in ((1, "r"), (-1, "l")):
    m.cube("cf_" + k, "coat_f" + k, (0.9 * s if s > 0 else -3.2, 11.6, -2.45), (3.2 if s > 0 else -0.9, 19.8, -1.85), COAT, color2=COAT_D, grad=True,
           origin=(2.0 * s, 19.6, -2.1), rot=(4, 0, 4 * s),
           faces={"north": combo(folds(COAT, COAT_D, COAT_L, 2), lambda F: F.rect(3, 22, F.w - 6, 1, COAT_D), lambda F: F.rect(3, 22, 1, 14, COAT_D),
                                 lambda F: F.rect(F.w - 4, 22, 1, 14, COAT_D))})
    m.cube("cs_" + k, "coat_s" + k, (3.0 * s - 0.3, 11.8, -1.9), (3.0 * s + 0.3, 19.8, 2.3), COAT, color2=COAT_D, grad=True,
           origin=(3.0 * s, 19.6, 0.2), rot=(0, 0, 6 * s), faces={"east": folds(COAT, COAT_D, COAT_L, 2), "west": folds(COAT, COAT_D, COAT_L, 2)})
    m.cube("pocket_" + k, "coat_f" + k, (1.3 * s if s > 0 else -2.9, 13.6, -2.6), (2.9 if s > 0 else -1.3, 15.6, -2.35), COAT_L,
           origin=(2.0 * s, 19.6, -2.1), rot=(4, 0, 4 * s), faces={"north": lambda F: F.rect(0, 0, F.w, 2, COAT_D)})

# ------------------------------------------------------------------ torso: coat over black dress, lapels, lanyard + badge, triangle pin
m.cube("torso", "chest", (-2.7, 19.4, -1.7), (2.7, 26.4, 1.7), COAT, color2=COAT_D, grad=True,
       faces={"north": coat_front, "south": folds(COAT, COAT_D, COAT_L, 3, False)})
m.cube("bust", "chest", (-2.4, 21.8, -2.05), (2.4, 24.6, -1.6), DRESS, faces={"north": lambda F: F.rect(0, 0, F.w, 2, DRESS_L)})
for s, k in ((1, "r"), (-1, "l")):
    x0, x1 = (1.0, 2.9) if s > 0 else (-2.9, -1.0)
    m.cube("lapel_" + k, "chest", (x0, 19.4, -2.25), (x1, 26.4, -1.7), COAT_L, color2=COAT, grad=True,
           origin=((x0 + x1) / 2, 26, -2), rot=(0, 0, -6 * s), faces={"north": lambda F: F.rect(0, 0, 1, F.h, COAT_D)})
    m.cube("collar_" + k, "chest", (0.6 * s if s > 0 else -2.6, 25.6, -2.2), (2.6 if s > 0 else -0.6, 27.0, 1.9), COAT_L, color2=COAT, grad=True,
           origin=(1.6 * s, 26.3, 0), rot=(0, 0, 14 * s))
m.cube("neck", "chest", (-0.9, 26.0, -0.8), (0.9, 27.8, 0.8), SKIN_D, color2=SKIN, grad=True)
m.cube("lany_r", "badge", (0.25, 22.4, -2.4), (0.65, 26.4, -2.1), GRN, origin=(0.45, 24.6, -2.2), rot=(0, 0, 12))
m.cube("lany_l", "badge", (-0.65, 22.4, -2.4), (-0.25, 26.4, -2.1), GRN, origin=(-0.45, 24.6, -2.2), rot=(0, 0, -12))
m.cube("id_card", "badge", (-0.95, 20.0, -2.6), (0.95, 22.6, -2.3), PAPER,
       faces={"north": lambda F: (F.rect(0, 0, F.w, 5, GRN), F.rect(2, 8, 5, 6, INKL), F.rect(9, 9, 5, 1, INKL), F.rect(9, 12, 4, 1, INKL), outline(PAPER_D)(F))})
m.cube("id_clip", "badge", (-0.3, 22.5, -2.55), (0.3, 23.0, -2.25), STEEL)
m.cube("tri_pin", "chest", (1.4, 23.3, -2.4), (2.4, 24.3, -2.2), COAT_L, origin=(1.9, 23.8, -2.3), rot=(0, 0, 0),
       faces={"north": lambda F: (F.poly([(F.w / 2, 0), (F.w, F.h), (0, F.h)], GRN), F.disc(F.w / 2, F.h * 0.65, 1.2, LINE))})
m.cube("button0", "chest", (-0.2, 20.4, -2.0), (0.2, 20.8, -1.75), DRESS_L)

# ------------------------------------------------------------------ head: pale face + grin, messy dark hair, goggles, white antlers
m.cube("skull", "head", (-3.4, 27.6, -3.3), (3.4, 34.4, 3.3), SKIN, faces={"north": face_front, "up": lambda F: F.rect(0, 0, F.w, F.h, HAIR_D)})
m.cube("hair_cap", "head", (-3.8, 33.6, -3.6), (3.8, 35.7, 3.7), HAIR, faces=all_faces(HS))
m.cube("hair_top", "head", (-3.2, 35.5, -2.8), (3.2, 36.4, 3.0), HAIR, faces=all_faces(HS))
for i, (x, ln, rz, z) in enumerate([(-3.2, 3.2, 18, 0), (-2.0, 1.2, 8, 0.05), (-0.8, 1.6, -6, 0), (0.5, 1.1, 10, 0.05), (1.7, 1.5, -10, 0), (3.0, 3.4, -20, 0.05)]):
    m.cube(f"bang{i}", "bangs", (x - 0.75, 34.0 - ln, -3.85 - z), (x + 0.75, 34.2, -3.35 - z), HAIR if i % 2 else HAIR_HI if i == 2 else HAIR_D,
           origin=(x, 34.0, -3.6), rot=(4, 0, rz), faces=all_faces(HS))
m.cube("hb_main", "hair_b", (-3.9, 25.6, 2.0), (3.9, 33.8, 4.1), HAIR, faces=all_faces(HS))
for i in range(8):  # jagged ends at the nape / shoulders
    x = -3.6 + i * 1.03
    ln = 2.2 + (i % 3) * 1.1 + R.uniform(0, 0.8)
    m.cube(f"hb_tip{i}", "hair_b", (x - 0.55, 25.8 - ln, 2.4 + (i % 2) * 0.4), (x + 0.55, 26.2, 3.9 + (i % 2) * 0.4), HAIR if i % 2 else HAIR_D,
           origin=(x, 26, 3.2), rot=(-14, 0, (i - 3.5) * 9), faces=all_faces(HS))
for i in range(5):  # messy spikes poking out of the crown/back
    a_ = -60 + i * 30
    m.cube(f"hb_spk{i}", "hair_b", (-0.6 + (i - 2) * 1.4, 32.6, 3.2), (0.6 + (i - 2) * 1.4, 36.2, 4.4), HAIR_D if i % 2 else HAIR,
           origin=((i - 2) * 1.4, 33.6, 3.8), rot=(-35, 0, a_ * 0.5), faces=all_faces(HS))
for s, k in ((1, "r"), (-1, "l")):
    m.cube("hs_main_" + k, "hair_" + k, (3.4 * s - 0.7, 26.2, -2.6), (3.4 * s + 0.7, 33.6, 2.6), HAIR, faces=all_faces(HS))
    for i in range(4):
        z = -2.4 + i * 1.5
        ln = 6.6 + (i % 2) * 1.6 + R.uniform(0, 1.0)
        m.cube(f"hs_lock{i}_" + k, "hair_" + k, (3.9 * s - 0.5, 32.4 - ln, z - 0.55), (3.9 * s + 0.5, 32.4, z + 0.55), HAIR_HI if i == 1 else HAIR_D if i == 3 else HAIR,
               origin=(3.9 * s, 32.4, z), rot=(-4, 0, (10 + i * 5) * s), faces=all_faces(HS))
    for i in range(3):  # flicks sticking out sideways (messy silhouette)
        y = 30.5 - i * 1.8
        m.cube(f"hs_flick{i}_" + k, "hair_" + k, (4.0 * s - 0.4, y - 3.0, -0.4 + i * 0.9), (4.0 * s + 0.4, y, 0.4 + i * 0.9), HAIR_D,
               origin=(4.0 * s, y, i * 0.9), rot=(0, 0, (45 + i * 12) * s))
    # antlers: curved main beam + two tines, white with grey shading
    hx = 1.9 * s
    m.cube("hn_base_" + k, "horn_" + k, (hx - 0.55, 35.3, 0.05), (hx + 0.55, 37.4, 1.15), HORN, color2=HORN_D, grad=True, origin=(hx, 35.6, 0.6), rot=(0, 0, -14 * s))
    m.cube("hn_beam_" + k, "horn_" + k, (hx - 0.4, 37.0, 0.2), (hx + 0.4, 40.6, 1.0), HORN, color2=HORN_D, grad=True, origin=(hx, 37.2, 0.6), rot=(0, 0, -30 * s))
    m.cube("hn_tip_" + k, "horn_" + k, (hx - 0.3, 39.6, 0.3), (hx + 0.3, 41.6, 0.9), HORN, origin=(hx, 39.8, 0.6), rot=(0, 0, -6 * s))
    m.cube("hn_tine_" + k, "horn_" + k, (hx - 0.3, 37.4, 0.3), (hx + 0.3, 39.6, 0.9), HORN, color2=HORN_D, grad=True, origin=(hx, 37.4, 0.6), rot=(0, 0, 32 * s))
    m.cube("hn_tine2_" + k, "horn_" + k, (hx - 0.25, 37.0, 0.35), (hx + 0.25, 38.6, 0.85), HORN, origin=(hx, 37.0, 0.6), rot=(-40, 0, -50 * s))
# goggles pushed up on the forehead: strap around the head, two round-ish green lenses with frames
m.cube("gog_strap", "goggles", (-3.95, 33.5, -3.75), (3.95, 34.3, 3.85), GRN_DD)
for s, k in ((1, "r"), (-1, "l")):
    m.cube("gog_rim_" + k, "goggles", (1.55 * s - 1.35, 33.0, -4.55), (1.55 * s + 1.35, 35.6, -3.6), GRN_D, origin=(1.55 * s, 34.3, -4), rot=(-20, 0, 0))
    m.cube("gog_lens_" + k, "goggles", (1.55 * s - 1.05, 33.3, -4.75), (1.55 * s + 1.05, 35.3, -4.3), LENS, origin=(1.55 * s, 34.3, -4), rot=(-20, 0, 0),
           glow=True, faces={"north": lens})
m.cube("gog_bridge", "goggles", (-0.35, 33.9, -4.3), (0.35, 34.5, -3.7), GRN_DD, origin=(0, 34.3, -4), rot=(-20, 0, 0))

# ------------------------------------------------------------------ arms: lab-coat sleeves, rolled cuffs, BIG green gloves, clipboards
for s, k in ((1, "r"), (-1, "l")):
    x = 3.9 * s
    m.cube("shoulder_" + k, "arm_" + k, (x - 1.25, 24.2, -1.35), (x + 1.25, 26.8, 1.35), COAT, color2=COAT_D, grad=True, origin=(x, 26, 0), rot=(0, 0, 8 * s))
    m.cube("sleeve_" + k, "arm_" + k, (x - 1.05, 22.0, -1.1), (x + 1.05, 25.4, 1.1), COAT, color2=COAT_D, grad=True, faces={"north": folds(COAT, COAT_D, COAT_L, 2, False)})
    m.cube("forearm_" + k, "fore_" + k, (x - 1.1, 19.0, -1.15), (x + 1.1, 22.4, 1.15), COAT, color2=COAT_D, grad=True, faces={"north": folds(COAT, COAT_D, COAT_L, 2, False)})
    m.cube("cuff_" + k, "fore_" + k, (x - 1.4, 18.4, -1.45), (x + 1.4, 19.9, 1.45), COAT_L, color2=COAT_D, grad=True,
           faces={"north": lambda F: F.rect(0, 0, F.w, 1, COAT_D)})
    m.cube("gcuff_" + k, "hand_" + k, (x - 1.75, 16.6, -1.75), (x + 1.75, 18.8, 1.75), GRN_L, color2=GRN, grad=True,
           faces={"north": lambda F: F.rect(0, 0, F.w, 2, GRN_D), "south": lambda F: F.rect(0, 0, F.w, 2, GRN_D)})
    m.cube("palm_" + k, "hand_" + k, (x - 1.6, 13.4, -1.45), (x + 1.6, 16.8, 1.45), GRN, faces=all_faces(glove, ("up",)))
    for i in range(4):  # big fingers curling over the board edge, front side
        fx = x - 1.2 + i * 0.8
        m.cube(f"fing{i}_" + k, "hand_" + k, (fx - 0.38, 11.9, -1.75), (fx + 0.38, 14.2, -0.75), GRN, color2=GRN_D, grad=True,
               origin=(fx, 14, -1.2), rot=(-10, 0, 0))
        m.cube(f"knuck{i}_" + k, "hand_" + k, (fx - 0.42, 13.6, -1.8), (fx + 0.42, 14.4, -0.9), GRN_L)
    m.cube("thumb_" + k, "hand_" + k, (x - 2.1 * s - 0.5, 13.6, -1.0), (x - 2.1 * s + 0.5, 16.2, 0.4), GRN, color2=GRN_D, grad=True,
           origin=(x - 1.6 * s, 16, 0), rot=(0, 0, 20 * s))
    # clipboard (paper faces outward/front), held by its top corner
    bx = x + 0.6 * s
    m.cube("brd_" + k, "board_" + k, (bx - 2.4, 7.0, 0.2), (bx + 2.4, 14.6, 0.55), BOARD, faces={"north": board_back, "south": board_back})
    m.cube("ppr_" + k, "board_" + k, (bx - 2.1, 7.3, -0.05), (bx + 2.1, 14.2, 0.2), PAPER, faces={"north": paper})
    m.cube("ppr2_" + k, "board_" + k, (bx - 2.2, 7.25, 0.05), (bx + 2.0, 13.9, 0.15), PAPER_D, origin=(bx, 14, 0), rot=(0, 0, 3 * s))
    m.cube("clip_" + k, "board_" + k, (bx - 0.9, 14.2, -0.2), (bx + 0.9, 15.0, 0.6), STEEL, color2=STEEL_D, grad=True)
    # toxic glow aura on the glove (enraged moves only)
    m.cube("toxa_" + k, "tox_" + k, (x - 2.2, 12.6, -2.2), (x + 2.2, 18.8, 2.2), TOX, glow=True, paint=GF(TOX_L, TOX))
    m.cube("toxb_" + k, "tox_" + k, (x - 1.6, 11.8, -1.6), (x + 1.6, 17.6, 1.6), TOX_L, glow=True, origin=(x, 15, 0), rot=(0, 45, 0), paint=GF(TOX, TOX_L))


# ================================================================== animation
PROPS = ["tox_r", "tox_l"]
HIDE = (.001, .001, .001)

REST = {
    "arm_r": (-4, 0, 12), "fore_r": (22, 0, 0), "hand_r": (0, -8, -4),
    "arm_l": (-4, 0, -12), "fore_l": (22, 0, 0), "hand_l": (0, 8, 4),
    "head": (0, 0, 5), "chest": (0, 0, 0),
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
        self.drape(["horn_r"], [(t, x * 0.15, 0, z * 0.2) for (t, x, y, z) in keys], delay=delay + 1)
        self.drape(["horn_l"], [(t, x * 0.15, 0, z * 0.2) for (t, x, y, z) in keys], delay=delay + 1)
        self.drape(["badge"], [(t, -x * 0.8, 0, z * 0.8) for (t, x, y, z) in keys], delay=delay)
        return self

    def coat(self, keys, delay=2):
        """x>0 = front tails kick forward (back tail lifts back), z>0 = flares toward +X"""
        self.drape(["coat_b", "coat_b2"], [(t, -x * 0.8, 0, z * 0.5) for (t, x, y, z) in keys], delay=delay, gain=0.9)
        self.drape(["coat_fr"], [(t, x, 0, z * 0.6 + abs(z) * 0.3) for (t, x, y, z) in keys], delay=delay)
        self.drape(["coat_fl"], [(t, x, 0, z * 0.6 - abs(z) * 0.3) for (t, x, y, z) in keys], delay=delay)
        self.drape(["coat_sr"], [(t, x * 0.3, 0, z + abs(x) * 0.2) for (t, x, y, z) in keys], delay=delay)
        self.drape(["coat_sl"], [(t, x * 0.3, 0, z - abs(x) * 0.2) for (t, x, y, z) in keys], delay=delay)
        self.drape(["skirt_f"], [(t, x * 0.6, 0, 0) for (t, x, y, z) in keys], delay=delay - 1 if delay > 1 else 1)
        self.drape(["skirt_b"], [(t, x * 0.5, 0, 0) for (t, x, y, z) in keys], delay=delay - 1 if delay > 1 else 1)
        self.drape(["skirt_r"], [(t, 0, 0, z * 0.6) for (t, x, y, z) in keys], delay=delay)
        self.drape(["skirt_l"], [(t, 0, 0, z * 0.6) for (t, x, y, z) in keys], delay=delay)
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


def legs(a, kr, kl=None, sr=None, sl=None, fr=None, fl=None):
    """leg keys for the right leg; left mirrors y/z unless given"""
    a.rot("leg_r", *kr)
    a.rot("leg_l", *(kl or [(t, x, -y, -z) for (t, x, y, z) in kr]))
    if sr: a.rot("shin_r", *sr)
    if sl or sr: a.rot("shin_l", *(sl or sr))
    if fr: a.rot("foot_r", *fr)
    if fl or fr: a.rot("foot_l", *(fl or fr))


def mirror(keys):
    return [(t, x, -y, -z) for (t, x, y, z) in keys]


# ------------------------------------------------------------------ idle (80 loop): giggly sway, lifts the left clipboard to read it, taps the right one
a = A("idle", 80, loop=True)
a.pos("body", (0, 0, 0, 0), (20, 0, -0.2, 0), (40, 0, 0, 0), (60, 0, -0.2, 0), (80, 0, 0, 0))
a.rot("body", (0, 0, 0, 2), (40, 0, 0, -2), (80, 0, 0, 2))
a.rot("chest", (0, 0, 0, -1), (20, 1, 3, 0), (34, -2, -4, 0), (56, -3, -6, 0), (66, 0, 0, 1), (80, 0, 0, -1))
a.rot("head", (0, 0, 0, 5), (16, 2, 0, 8), (30, 0, 0, 5), (36, -16, -16, 2), (58, -18, -18, 4), (61, -10, -18, 10), (63, -18, -18, 2), (68, 0, 0, 6), (80, 0, 0, 5))
a.rot("arm_r", (0, -4, 0, 12), (20, -2, 0, 14), (24, 8, 0, 6), (26, -6, 0, 14), (28, 8, 0, 6), (30, -4, 0, 12), (80, -4, 0, 12))
a.rot("fore_r", (0, 22, 0, 0), (24, 36, 0, 0), (26, 18, 0, 0), (28, 36, 0, 0), (30, 22, 0, 0), (80, 22, 0, 0))
a.rot("hand_r", R_("hand_r", 0), R_("hand_r", 80))
a.rot("arm_l", (0, -4, 0, -12), (32, -4, 0, -12), (38, 30, -20, -4), (56, 32, -22, -4), (62, -4, 0, -12), (80, -4, 0, -12))
a.rot("fore_l", (0, 22, 0, 0), (32, 22, 0, 0), (38, 72, 0, 0), (56, 76, 0, 0), (62, 22, 0, 0), (80, 22, 0, 0))
a.rot("hand_l", (0, 0, 8, 4), (32, 0, 8, 4), (38, -40, -30, 0), (56, -40, -30, 0), (62, 0, 8, 4), (80, 0, 8, 4))
legs(a, [(0, 0, 0, 2), (40, 0, 0, 2), (80, 0, 0, 2)], [(0, 3, 0, -3), (40, 5, 0, -4), (80, 3, 0, -3)],
     sr=[(0, 0, 0, 0), (80, 0, 0, 0)], sl=[(0, -6, 0, 0), (40, -9, 0, 0), (80, -6, 0, 0)])
a.hair([(0, 0, 0, 2), (20, -2, 0, 0), (40, 0, 0, -2), (60, 2, 0, 3), (62, 0, 0, -3), (64, 1, 0, 2), (80, 0, 0, 2)], delay=4)
a.coat([(0, 1, 0, 1), (40, 0, 0, -1), (80, 1, 0, 1)], delay=4)
a.done()

# ------------------------------------------------------------------ walk (20 loop): brisk bouncy lab stride, clipboards swinging, coat tails flapping
a = A("walk", 20, loop=True)
a.rot("leg_r", (0, 28, 0, 0), (5, 0, 0, 0), (10, -26, 0, 0), (15, 0, 0, 0), (20, 28, 0, 0))
a.rot("shin_r", (0, -4, 0, 0), (5, -8, 0, 0), (10, -10, 0, 0), (13, -50, 0, 0), (17, -26, 0, 0), (20, -4, 0, 0))
a.rot("foot_r", (0, -12, 0, 0), (10, 12, 0, 0), (20, -12, 0, 0))
a.rot("leg_l", (0, -26, 0, 0), (5, 0, 0, 0), (10, 28, 0, 0), (15, 0, 0, 0), (20, -26, 0, 0))
a.rot("shin_l", (0, -10, 0, 0), (3, -50, 0, 0), (7, -26, 0, 0), (10, -4, 0, 0), (15, -8, 0, 0), (20, -10, 0, 0))
a.rot("foot_l", (0, 12, 0, 0), (10, -12, 0, 0), (20, 12, 0, 0))
a.pos("body", (0, 0, -0.4, 0), (5, 0, 0.5, 0), (10, 0, -0.4, 0), (15, 0, 0.5, 0), (20, 0, -0.4, 0))
a.rot("body", (0, -4, 6, -2), (10, -4, -6, 2), (20, -4, 6, -2))
a.rot("chest", (0, 0, -5, 2), (10, 0, 5, -2), (20, 0, -5, 2))
a.rot("head", (0, 2, 4, 3), (5, 4, 0, 7), (10, 2, -4, 3), (15, 4, 0, 7), (20, 2, 4, 3))
a.rot("arm_r", (0, -24, 0, 12), (10, 26, 0, 10), (20, -24, 0, 12))
a.rot("fore_r", (0, 14, 0, 0), (10, 34, 0, 0), (20, 14, 0, 0))
a.rot("arm_l", (0, 26, 0, -10), (10, -24, 0, -12), (20, 26, 0, -10))
a.rot("fore_l", (0, 34, 0, 0), (10, 14, 0, 0), (20, 34, 0, 0))
a.rot("hand_r", (0, -6, -8, -4), (10, 8, -8, -4), (20, -6, -8, -4))
a.rot("hand_l", (0, 8, 8, 4), (10, -6, 8, 4), (20, 8, 8, 4))
a.hair([(0, -6, 0, 3), (5, -9, 0, 0), (10, -6, 0, -3), (15, -9, 0, 0), (20, -6, 0, 3)], delay=2)
a.coat([(0, 6, 0, 3), (5, 2, 0, 0), (10, 6, 0, -3), (15, 2, 0, 0), (20, 6, 0, 3)], delay=2)
tracks = {b: {ch: sorted([(t / 20.0, x, y, z) for (t, x, y, z) in v]) for ch, v in chs.items()} for b, chs in a.tr.items()}
for p in PROPS: tracks[p] = {"scale": [(0, *HIDE)]}
for b, v in REST.items():
    tracks.setdefault(b, {}).setdefault("rotation", [(0, *v)])
m.anim("walk", 1.0, tracks, loop=True)

# ------------------------------------------------------------------ clip_slap (32): forehand board slap 8, backhand 16, double overhead whack 25
a = A("clip_slap", 32)
a.r("arm_r", (4, 60, -70, 0), (6, 66, -76, 0), (8, 82, 30, 0), (10, 78, 46, 0), (14, 40, 10, 0), (19, 150, 0, 20), (22, 176, 0, 14), (25, 64, 0, 6),
    (27, 54, 0, 6), (30, 10, 0, 10))
a.r("fore_r", (4, 40, 0, 0), (8, 6, 0, 0), (14, 30, 0, 0), (22, 20, 0, 0), (25, 0, 0, 0), (28, 20, 0, 0))
a.r("hand_r", (4, 0, 70, 0), (8, 0, 90, 0), (12, 0, 60, 0), (18, 0, 0, 0), (25, -20, 0, 0), (29, 0, 0, 0))
a.r("arm_l", (6, -4, 0, -12), (10, 40, -50, 0), (13, 60, -66, 0), (16, 82, 50, 0), (18, 78, 64, 0), (21, 160, 0, -18), (22, 176, 0, -14), (25, 64, 0, -6),
    (27, 54, 0, -6), (30, 10, 0, -10))
a.r("fore_l", (10, 50, 0, 0), (16, 4, 0, 0), (19, 30, 0, 0), (22, 20, 0, 0), (25, 0, 0, 0), (28, 20, 0, 0))
a.r("hand_l", (10, 0, -60, 0), (16, 0, -90, 0), (19, 0, -40, 0), (22, 0, 0, 0), (25, -20, 0, 0), (29, 0, 0, 0))
a.r("chest", (4, 0, -26, 0), (6, 0, -30, 2), (8, 0, 24, -2), (10, 0, 28, -2), (13, 0, 26, 0), (16, 0, -26, 2), (18, 0, -28, 2), (21, 8, 0, 0),
    (25, -22, 0, 0), (27, -24, 0, 0), (32, 0, 0, 0))
a.r("head", (4, 0, 14, 8), (8, -4, -14, 0), (13, 0, -16, 8), (16, -4, 16, -4), (21, 10, 0, 6), (25, -6, 0, 0), (28, 4, 0, 10))
a.rot("body", (0, 0, 0, 0), (6, 0, -10, 0), (8, 0, 10, 0), (13, 0, 8, 0), (16, 0, -10, 0), (21, 6, 0, 0), (25, -10, 0, 0), (28, -8, 0, 0), (32, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (8, 0, -0.3, -0.6), (16, 0, -0.3, -1.0), (21, 0, 0.3, -0.6), (25, 0, -1.4, -1.6), (28, 0, -1.2, -1.4), (32, 0, 0, 0))
legs(a, [(0, 0, 0, 2), (8, -16, 0, 2), (16, -22, 0, 2), (25, -34, 0, 2), (28, -30, 0, 2), (32, 0, 0, 2)],
     [(0, 3, 0, -3), (8, 14, 0, -3), (16, 18, 0, -3), (25, 24, 0, -3), (28, 20, 0, -3), (32, 3, 0, -3)],
     sr=[(0, 0, 0, 0), (8, 6, 0, 0), (25, 30, 0, 0), (32, 0, 0, 0)], sl=[(0, -6, 0, 0), (16, -20, 0, 0), (25, -30, 0, 0), (32, -6, 0, 0)])
a.hair([(0, 0, 0, 0), (6, 0, 0, 10), (9, -4, 0, -14), (13, 0, 0, -8), (17, -4, 0, 14), (21, -8, 0, 0), (25, 14, 0, 0), (28, 4, 0, 0), (32, 0, 0, 0)])
a.coat([(0, 0, 0, 0), (8, -4, 0, -10), (16, -6, 0, 10), (21, -2, 0, 0), (25, 14, 0, 0), (32, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ glove_haymaker (34): coils far back 0-13, huge right hook lands 16, spins through, recover
a = A("glove_haymaker", 34)
a.r("arm_r", (5, -30, 0, 50), (10, -50, 0, 70), (13, -54, 0, 74), (15, 60, -10, 10), (16, 90, 24, 0), (18, 92, 48, 0), (22, 70, 40, 0), (28, 10, 0, 6))
a.r("fore_r", (5, 60, 0, 0), (13, 90, 0, 0), (16, 0, 0, 0), (20, 10, 0, 0), (28, 20, 0, 0))
a.r("hand_r", (5, 0, 0, 30), (13, 0, 0, 40), (16, 0, 90, 0), (22, 0, 60, 0), (30, *rest("hand_r")))
a.r("arm_l", (6, 40, 0, -20), (13, 60, 0, -10), (16, -30, 0, -30), (22, -20, 0, -24), (30, -4, 0, -12))
a.r("fore_l", (6, 50, 0, 0), (13, 70, 0, 0), (16, 30, 0, 0))
a.rot("body", (0, 0, 0, 0), (10, -4, -28, 0), (13, -6, -34, 0), (16, 4, 30, 0), (19, 6, 40, 0), (24, 2, 16, 0), (34, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (13, 0, -1.2, 1.0), (16, 0, -0.8, -2.0), (20, 0, -0.6, -2.2), (34, 0, 0, 0))
a.r("chest", (10, 6, -10, 0), (13, 8, -14, 0), (16, -14, 20, 0), (19, -16, 26, 0), (26, -4, 4, 0))
a.r("head", (10, 0, 30, 10), (13, -4, 38, 10), (16, -8, -16, 0), (22, -4, -20, 0), (28, 2, 0, 12))
legs(a, [(0, 0, 0, 2), (13, 20, 0, 6), (16, -30, 0, 4), (22, -26, 0, 4), (34, 0, 0, 2)],
     [(0, 3, 0, -3), (13, -16, 0, -6), (16, 30, 0, -4), (22, 22, 0, -4), (34, 3, 0, -3)],
     sr=[(0, 0, 0, 0), (13, -30, 0, 0), (16, 10, 0, 0), (34, 0, 0, 0)], sl=[(0, -6, 0, 0), (13, -10, 0, 0), (16, -40, 0, 0), (24, -20, 0, 0), (34, -6, 0, 0)])
a.hair([(0, 0, 0, 0), (13, 4, 0, 16), (17, -10, 0, -22), (22, -4, 0, -10), (34, 0, 0, 0)])
a.coat([(0, 0, 0, 0), (13, 4, 0, 14), (17, -8, 0, -20), (24, -2, 0, -6), (34, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ clap_crush (30): spreads both boards wide 0-10, SLAMS them together on the target at 13, grinds, lets go
a = A("clap_crush", 30)
a.r("arm_r", (6, 70, -80, 0), (10, 80, -90, 0), (12, 86, -30, 0), (13, 88, -6, 0), (15, 86, -2, 0), (20, 80, -4, 0), (26, 20, 0, 12))
a.r("arm_l", (6, 70, 80, 0), (10, 80, 90, 0), (12, 86, 30, 0), (13, 88, 6, 0), (15, 86, 2, 0), (20, 80, 4, 0), (26, 20, 0, -12))
a.r("fore_r", (6, 10, 0, 0), (13, 0, 0, 0), (20, 10, 0, 0))
a.r("fore_l", (6, 10, 0, 0), (13, 0, 0, 0), (20, 10, 0, 0))
a.r("hand_r", (6, 0, 90, 0), (13, 0, 90, 0), (16, 0, 90, -6), (18, 0, 90, 6), (22, 0, 60, 0))
a.r("hand_l", (6, 0, -90, 0), (13, 0, -90, 0), (16, 0, -90, 6), (18, 0, -90, -6), (22, 0, -60, 0))
a.r("chest", (6, 14, 0, 0), (10, 18, 0, 0), (13, -16, 0, 0), (18, -14, 0, 0), (24, 0, 0, 0))
a.r("head", (6, 14, 0, 0), (10, 18, 0, 0), (13, -10, 0, 0), (16, -6, 0, 8), (18, -6, 0, -8), (22, 4, 0, 6))
a.pos("body", (0, 0, 0, 0), (10, 0, 0.6, 0.4), (13, 0, -0.8, -1.6), (20, 0, -0.6, -1.4), (30, 0, 0, 0))
legs(a, [(0, 0, 0, 2), (10, 4, 0, 4), (13, -24, 0, 2), (22, -20, 0, 2), (30, 0, 0, 2)], [(0, 3, 0, -3), (10, 4, 0, -4), (13, 16, 0, -3), (22, 12, 0, -3), (30, 3, 0, -3)],
     sr=[(0, 0, 0, 0), (13, 20, 0, 0), (30, 0, 0, 0)], sl=[(0, -6, 0, 0), (13, -26, 0, 0), (30, -6, 0, 0)])
a.hair([(0, 0, 0, 0), (10, -6, 0, 0), (13, 14, 0, 0), (17, 4, 0, 6), (19, 4, 0, -6), (30, 0, 0, 0)])
a.coat([(0, 0, 0, 0), (10, -4, 0, 0), (13, 10, 0, 0), (30, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ lab_grab (50): lunging grab 10, lifts the specimen 10-34 (squeezes 18/26), body-slams it down 36
a = A("lab_grab", 50)
a.r("arm_r", (5, -20, 0, 30), (8, 40, 0, 20), (10, 92, 0, -8), (14, 110, 0, -12), (18, 150, 0, -14), (20, 140, 0, -10), (26, 160, 0, -14), (28, 150, 0, -10),
    (32, 186, 0, -6), (36, 50, 0, -4), (39, 40, 0, 0), (46, 0, 0, 10))
a.r("fore_r", (5, 60, 0, 0), (10, 0, 0, 0), (18, 10, 0, 0), (32, 30, 0, 0), (36, 0, 0, 0), (44, 20, 0, 0))
a.r("hand_r", (8, 0, 0, 0), (10, -40, 0, 0), (18, -50, 0, 0), (19, -60, 0, 0), (26, -50, 0, 0), (27, -60, 0, 0), (36, -20, 0, 0), (44, 0, -8, -4))
a.r("arm_l", (6, 30, 0, -20), (10, 50, 0, -10), (18, 20, 0, -30), (26, 20, 0, -34), (32, 40, 0, -20), (36, -20, 0, -30), (46, -4, 0, -12))
a.r("fore_l", (10, 60, 0, 0), (18, 80, 0, 0), (36, 20, 0, 0))
a.r("chest", (5, 10, 14, 0), (10, -16, -10, 0), (18, 10, -6, 0), (26, 12, -4, 0), (32, 20, 0, 0), (36, -30, 0, 0), (40, -26, 0, 0), (48, 0, 0, 0))
a.r("head", (5, 6, 10, 0), (10, -6, 0, 0), (18, 22, 0, 16), (22, 22, 0, -12), (26, 24, 0, 16), (32, 26, 0, 0), (36, -16, 0, 0), (42, 4, 0, 14))
a.pos("body", (0, 0, 0, 0), (5, 0, -0.8, 0.6), (10, 0, -0.6, -2.0), (14, 0, 0, -1.2), (32, 0, 0.4, -0.8), (36, 0, -2.0, -1.4), (40, 0, -1.8, -1.2), (50, 0, 0, 0))
legs(a, [(0, 0, 0, 2), (5, 10, 0, 2), (10, -30, 0, 2), (14, -16, 0, 2), (32, -10, 0, 4), (36, -40, 0, 2), (42, -30, 0, 2), (50, 0, 0, 2)],
     [(0, 3, 0, -3), (5, -10, 0, -3), (10, 26, 0, -3), (14, 14, 0, -3), (32, 6, 0, -4), (36, 30, 0, -3), (42, 20, 0, -3), (50, 3, 0, -3)],
     sr=[(0, 0, 0, 0), (5, -20, 0, 0), (10, 10, 0, 0), (36, 40, 0, 0), (50, 0, 0, 0)], sl=[(0, -6, 0, 0), (10, -30, 0, 0), (14, -10, 0, 0), (36, -40, 0, 0), (50, -6, 0, 0)])
a.hair([(0, 0, 0, 0), (10, -12, 0, 0), (18, -4, 0, 10), (22, -4, 0, -10), (26, -4, 0, 10), (32, -10, 0, 0), (36, 18, 0, 0), (42, 4, 0, 0), (50, 0, 0, 0)])
a.coat([(0, 0, 0, 0), (10, -10, 0, 0), (20, -2, 0, 0), (36, 16, 0, 0), (42, 4, 0, 0), (50, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ antler_charge (34): lowers the horns 0-8, bull-rushes 9-17 (gores 12 + 15), skids, tosses head 20
a = A("antler_charge", 34)
a.rot("body", (0, 0, 0, 0), (6, -30, 0, 0), (8, -34, 0, 0), (10, -40, 0, 0), (16, -38, 0, 0), (19, -10, 0, 0), (21, 8, 0, 0), (26, 4, 0, 0), (34, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (8, 0, -2.4, 1.0), (12, 0, -2.0, -1.0), (16, 0, -2.2, -0.6), (20, 0, -0.6, 0.6), (34, 0, 0, 0))
a.r("chest", (8, -10, 0, 0), (12, -14, 0, 0), (15, -10, 0, 0), (19, -6, 0, 0), (21, 12, 0, 0), (26, 4, 0, 0))
a.r("head", (6, -26, 0, 0), (12, -34, 0, 0), (13, -18, 0, 6), (15, -34, 0, 0), (16, -20, 0, -6), (19, -20, 0, 0), (21, 30, 0, 10), (25, 20, 0, 0), (30, 4, 0, 8))
a.r("arm_r", (6, -60, 0, 30), (8, -70, 0, 34), (10, -50, 0, 30), (12, -80, 0, 30), (14, -40, 0, 30), (16, -80, 0, 30), (21, 30, 0, 40), (28, -4, 0, 12))
a.r("arm_l", (6, -60, 0, -30), (8, -70, 0, -34), (10, -80, 0, -30), (12, -40, 0, -30), (14, -80, 0, -30), (16, -40, 0, -30), (21, 30, 0, -40), (28, -4, 0, -12))
a.r("fore_r", (8, 20, 0, 0), (21, 50, 0, 0))
a.r("fore_l", (8, 20, 0, 0), (21, 50, 0, 0))
a.rot("leg_r", (0, 0, 0, 2), (6, 40, 0, 2), (8, 50, 0, 2), (10, -30, 0, 0), (12, 40, 0, 0), (14, -30, 0, 0), (16, 40, 0, 0), (19, 30, 0, 2), (24, 10, 0, 2), (34, 0, 0, 2))
a.rot("leg_l", (0, 3, 0, -3), (6, 10, 0, -3), (8, 0, 0, -3), (10, 40, 0, 0), (12, -30, 0, 0), (14, 40, 0, 0), (16, -30, 0, 0), (19, 50, 0, -3), (24, 14, 0, -3), (34, 3, 0, -3))
a.rot("shin_r", (0, 0, 0, 0), (8, -60, 0, 0), (10, -20, 0, 0), (12, -60, 0, 0), (14, -20, 0, 0), (16, -60, 0, 0), (19, -30, 0, 0), (34, 0, 0, 0))
a.rot("shin_l", (0, -6, 0, 0), (8, -30, 0, 0), (10, -60, 0, 0), (12, -20, 0, 0), (14, -60, 0, 0), (16, -20, 0, 0), (19, -10, 0, 0), (34, -6, 0, 0))
a.hair([(0, 0, 0, 0), (8, 8, 0, 0), (12, -20, 0, 0), (16, -22, 0, 0), (21, 16, 0, 10), (26, 4, 0, -4), (34, 0, 0, 0)])
a.coat([(0, 0, 0, 0), (8, 4, 0, 0), (11, -22, 0, 4), (16, -24, 0, -4), (20, 10, 0, 0), (34, 0, 0, 0)], delay=1)
a.done()

# ------------------------------------------------------------------ clip_spin (36): coils 0-8, three whirling board sweeps (10/16/22), wobbly dizzy finish
a = A("clip_spin", 36)
a.rot("root", (0, 0, 0, 0), (6, 0, 30, 0), (8, 0, 36, 0), (10, 0, -90, 0), (13, 0, -200, 0), (16, 0, -450, 0), (19, 0, -560, 0), (22, 0, -810, 0), (26, 0, -900, 0),
      (28, 0, -904, 0), (32, 0, -898, 0), (36, 0, -900, 0))
a.pos("root", (0, 0, 0, 0), (8, 0, -1.0, 0), (10, 0, 0.4, 0), (16, 0, 0.6, 0), (22, 0, 0.4, 0), (26, 0, 0, 0), (36, 0, 0, 0))
a.r("arm_r", (6, 30, 0, 30), (8, 20, 0, 40), (10, 0, 0, 96), (22, 0, 0, 100), (26, 30, 0, 50), (30, -4, 0, 20))
a.r("arm_l", (6, 40, 0, -60), (8, 50, 0, -70), (10, 0, 0, -96), (22, 0, 0, -100), (26, 30, 0, -50), (30, -4, 0, -20))
a.r("fore_r", (8, 50, 0, 0), (10, 0, 0, 0), (24, 10, 0, 0))
a.r("fore_l", (8, 60, 0, 0), (10, 0, 0, 0), (24, 10, 0, 0))
a.r("hand_r", (10, 0, 0, 0), (12, 90, 0, 0), (22, 90, 0, 0), (26, 0, 0, 0))
a.r("hand_l", (10, 0, 0, 0), (12, 90, 0, 0), (22, 90, 0, 0), (26, 0, 0, 0))
a.r("chest", (8, 0, 20, 0), (10, -6, -10, 0), (22, -6, -10, 0), (26, 0, 0, 8), (29, 0, 0, -8), (32, 0, 0, 6))
a.r("head", (8, 0, 20, 0), (10, 10, -10, 0), (22, 10, -10, 0), (26, 4, 0, 18), (29, 4, 0, -18), (32, 4, 0, 14))
legs(a, [(0, 0, 0, 2), (8, 10, 0, 6), (10, 0, 0, 10), (22, 0, 0, 10), (26, -10, 0, 4), (30, 0, 0, 4), (36, 0, 0, 2)],
     sr=[(0, 0, 0, 0), (8, -20, 0, 0), (10, 0, 0, 0), (26, -10, 0, 0), (36, 0, 0, 0)], sl=[(0, -6, 0, 0), (8, -20, 0, 0), (10, 0, 0, 0), (26, -20, 0, 0), (36, -6, 0, 0)])
a.hair([(0, 0, 0, 0), (8, 0, 0, -10), (11, -10, 0, 30), (22, -10, 0, 30), (26, 0, 0, -14), (29, 0, 0, 10), (36, 0, 0, 0)])
a.coat([(0, 0, 0, 0), (8, 0, 0, -6), (11, -14, 0, 30), (22, -14, 0, 30), (26, 4, 0, -10), (30, 0, 0, 6), (36, 0, 0, 0)], delay=1)
a.done()

# ------------------------------------------------------------------ boot_stomp (40): crouch 0-7, leaps 8, tucks in the air, both boots crash down 20, shockwave
a = A("boot_stomp", 40)
a.pos("root", (0, 0, 0, 0), (6, 0, -3.0, 0), (8, 0, -1.0, 0), (11, 0, 10, -2), (15, 0, 13, -4), (18, 0, 6, -6), (20, 0, -3.4, -7), (24, 0, -3.0, -7),
      (30, 0, -1.0, -7), (36, 0, 0, -7), (40, 0, 0, -7))
a.rot("root", (0, 0, 0, 0), (6, 0, 0, 0), (10, -10, 0, 0), (15, 10, 0, 0), (20, 0, 0, 0), (40, 0, 0, 0))
a.rot("body", (0, 0, 0, 0), (6, -26, 0, 0), (8, 6, 0, 0), (14, -10, 0, 0), (18, 4, 0, 0), (20, -28, 0, 0), (24, -24, 0, 0), (32, -6, 0, 0), (40, 0, 0, 0))
a.r("arm_r", (6, -50, 0, 20), (8, 150, 0, 30), (14, 170, 0, 40), (18, 140, 0, 60), (20, 20, 0, 80), (24, 10, 0, 76), (32, 0, 0, 30))
a.r("arm_l", (6, -50, 0, -20), (8, 150, 0, -30), (14, 170, 0, -40), (18, 140, 0, -60), (20, 20, 0, -80), (24, 10, 0, -76), (32, 0, 0, -30))
a.r("fore_r", (8, 10, 0, 0), (20, 0, 0, 0), (30, 30, 0, 0))
a.r("fore_l", (8, 10, 0, 0), (20, 0, 0, 0), (30, 30, 0, 0))
a.r("head", (6, -20, 0, 0), (8, 20, 0, 0), (14, 10, 0, 10), (18, -10, 0, 0), (20, -24, 0, 0), (24, -18, 0, 0), (32, 4, 0, 10))
legs(a, [(0, 0, 0, 2), (6, 60, 0, 4), (8, -10, 0, 2), (12, 70, 0, 4), (16, 80, 0, 4), (18, 20, 0, 4), (20, 50, 0, 8), (24, 46, 0, 8), (32, 10, 0, 4), (40, 0, 0, 2)],
     sr=[(0, 0, 0, 0), (6, -90, 0, 0), (8, 0, 0, 0), (12, -110, 0, 0), (16, -110, 0, 0), (18, -10, 0, 0), (20, -84, 0, 0), (24, -80, 0, 0), (32, -20, 0, 0), (40, 0, 0, 0)],
     fr=[(0, 0, 0, 0), (6, 30, 0, 0), (8, -30, 0, 0), (16, 20, 0, 0), (18, 0, 0, 0), (20, 34, 0, 0), (32, 6, 0, 0), (40, 0, 0, 0)])
a.hair([(0, 0, 0, 0), (6, 8, 0, 0), (9, -20, 0, 0), (15, -6, 0, 0), (18, -16, 0, 0), (21, 24, 0, 0), (26, 6, 0, 0), (40, 0, 0, 0)])
a.coat([(0, 0, 0, 0), (6, 6, 0, 0), (9, -30, 0, 0), (15, -10, 0, 0), (18, -40, 0, 0), (21, 30, 0, 0), (27, 6, 0, 0), (40, 0, 0, 0)], delay=1)
a.done()

# ------------------------------------------------------------------ front_kick (26): chambers the knee 6, snaps a tall-boot push kick out 10, hops back 16
a = A("front_kick", 26)
a.rot("leg_r", (0, 0, 0, 2), (4, 50, 0, 4), (7, 90, 0, 4), (10, 96, 0, 0), (12, 92, 0, 0), (15, 50, 0, 2), (19, 6, 0, 2), (26, 0, 0, 2))
a.rot("shin_r", (0, 0, 0, 0), (4, -60, 0, 0), (7, -110, 0, 0), (10, 0, 0, 0), (12, -4, 0, 0), (15, -70, 0, 0), (19, -10, 0, 0), (26, 0, 0, 0))
a.rot("foot_r", (0, 0, 0, 0), (7, 20, 0, 0), (10, -30, 0, 0), (13, -20, 0, 0), (19, 0, 0, 0), (26, 0, 0, 0))
a.rot("leg_l", (0, 3, 0, -3), (7, -14, 0, -3), (10, -26, 0, -3), (15, -14, 0, -3), (26, 3, 0, -3))
a.rot("shin_l", (0, -6, 0, 0), (7, -20, 0, 0), (10, -10, 0, 0), (15, -30, 0, 0), (26, -6, 0, 0))
a.rot("body", (0, 0, 0, 0), (7, 10, 0, 6), (10, 26, 0, 4), (13, 22, 0, 4), (17, 4, 0, 0), (26, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (7, 0, 0.6, 0), (10, 0, 0.2, 0.6), (16, 0, 0.8, 1.4), (19, 0, -0.4, 1.2), (26, 0, 0, 0))
a.r("chest", (7, 4, 10, 0), (10, -14, 0, 0), (14, -10, 0, 0), (20, 0, 0, 0))
a.r("head", (7, -10, 0, 8), (10, -26, 0, 0), (14, -20, 0, 6), (20, 0, 0, 10))
a.r("arm_r", (7, 20, 0, 50), (10, -40, 0, 60), (15, -20, 0, 30))
a.r("arm_l", (7, 30, 0, -50), (10, -30, 0, -66), (15, -20, 0, -30))
a.r("fore_r", (7, 40, 0, 0), (10, 30, 0, 0))
a.r("fore_l", (7, 40, 0, 0), (10, 30, 0, 0))
a.hair([(0, 0, 0, 0), (7, -4, 0, 4), (10, 14, 0, 0), (14, 4, 0, 0), (26, 0, 0, 0)])
a.coat([(0, 0, 0, 0), (7, 20, 0, 6), (10, 30, 0, 0), (15, -6, 0, 0), (26, 0, 0, 0)], delay=1)
a.done()

# ------------------------------------------------------------------ pummel (36): rapid alternating glove jabs 6/10/14/18/22, big two-glove shove 28
a = A("pummel", 36)
ar, al_, fr_, fl_, ch, bd = [R_("arm_r", 0), (4, 20, 0, 20)], [R_("arm_l", 0), (4, 20, 0, -20)], [R_("fore_r", 0), (4, 90, 0, 0)], [R_("fore_l", 0), (4, 90, 0, 0)], \
    [(0, 0, 0, 0), (4, 6, 0, 0)], [(0, 0, 0, 0)]
for i, tk in enumerate((6, 10, 14, 18, 22)):
    right = i % 2 == 0
    (ar if right else al_).extend([(tk - 2, 30, 0, 20 if right else -20), (tk, 92, 0, -6 if right else 6), (tk + 1, 88, 0, -4 if right else 4)])
    (fr_ if right else fl_).extend([(tk - 2, 100, 0, 0), (tk, 0, 0, 0), (tk + 1, 6, 0, 0)])
    (al_ if right else ar).extend([(tk, 24, 0, -18 if right else 18)])
    (fl_ if right else fr_).extend([(tk, 96, 0, 0)])
    ch.append((tk, -6, 16 if right else -16, 0))
    bd.append((tk, 0, 8 if right else -8, 0))
ar += [(25, 20, 0, 30), (28, 90, 0, 8), (30, 92, 0, 10), (33, 30, 0, 12), R_("arm_r", 36)]
al_ += [(25, 20, 0, -30), (28, 90, 0, -8), (30, 92, 0, -10), (33, 30, 0, -12), R_("arm_l", 36)]
fr_ += [(25, 110, 0, 0), (28, 0, 0, 0), (33, 20, 0, 0), R_("fore_r", 36)]
fl_ += [(25, 110, 0, 0), (28, 0, 0, 0), (33, 20, 0, 0), R_("fore_l", 36)]
ch += [(25, 10, 0, 0), (28, -18, 0, 0), (31, -14, 0, 0), (36, 0, 0, 0)]
bd += [(25, 0, 0, 0), (36, 0, 0, 0)]
a.rot("arm_r", *ar); a.rot("arm_l", *al_); a.rot("fore_r", *fr_); a.rot("fore_l", *fl_); a.rot("chest", *ch); a.rot("body", *bd)
a.r("hand_r", (4, 0, 90, 0), (26, 0, 90, 0), (28, -30, 0, 0), (32, -20, 0, 0))
a.r("hand_l", (4, 0, -90, 0), (26, 0, -90, 0), (28, -30, 0, 0), (32, -20, 0, 0))
a.r("head", (4, -10, 0, 0), (12, -12, 0, 6), (20, -12, 0, -6), (25, 6, 0, 0), (28, -14, 0, 0), (32, 0, 0, 12))
a.pos("body", (0, 0, 0, 0), (4, 0, -0.6, 0), (22, 0, -0.6, -0.8), (25, 0, -0.4, 0.4), (28, 0, -1.0, -1.8), (32, 0, -0.6, -1.4), (36, 0, 0, 0))
legs(a, [(0, 0, 0, 2), (4, -16, 0, 2), (24, -16, 0, 2), (28, -30, 0, 2), (36, 0, 0, 2)], [(0, 3, 0, -3), (4, 16, 0, -3), (24, 16, 0, -3), (28, 26, 0, -3), (36, 3, 0, -3)],
     sr=[(0, 0, 0, 0), (4, 14, 0, 0), (28, 26, 0, 0), (36, 0, 0, 0)], sl=[(0, -6, 0, 0), (4, -20, 0, 0), (28, -30, 0, 0), (36, -6, 0, 0)])
a.hair([(0, 0, 0, 0), (6, 0, 0, -8), (10, 0, 0, 8), (14, 0, 0, -8), (18, 0, 0, 8), (22, 0, 0, -8), (25, -6, 0, 0), (28, 14, 0, 0), (36, 0, 0, 0)], delay=1)
a.coat([(0, 0, 0, 0), (6, -4, 0, -6), (14, -4, 0, -6), (10, -4, 0, 6), (18, -4, 0, 6), (28, 12, 0, 0), (36, 0, 0, 0)], delay=1)
a.done()

# ------------------------------------------------------------------ clip_chop (36): hop forward 6-12 with the right board raised edge-first, guillotine chop 16
a = A("clip_chop", 36)
a.pos("root", (0, 0, 0, 0), (5, 0, -1.6, 0), (8, 0, 4.0, -2), (12, 0, 5.0, -5), (16, 0, -1.6, -7), (20, 0, -1.2, -7), (28, 0, 0, -7), (36, 0, 0, -7))
a.rot("body", (0, 0, 0, 0), (5, -12, 0, 0), (10, 12, 0, 0), (13, 16, 0, 0), (16, -34, 0, 0), (20, -30, 0, 0), (28, -6, 0, 0), (36, 0, 0, 0))
a.r("arm_r", (5, -30, 0, 30), (9, 170, 0, 10), (13, 196, 0, 4), (16, 50, 0, 0), (19, 30, 0, 0), (26, 20, 0, 10))
a.r("fore_r", (9, 30, 0, 0), (13, 40, 0, 0), (16, 0, 0, 0), (26, 30, 0, 0))
a.r("hand_r", (9, 0, 90, 0), (16, 0, 90, -10), (22, 0, 80, 0), (28, *rest("hand_r")))
a.r("arm_l", (5, -30, 0, -30), (9, 60, 0, -50), (13, 70, 0, -60), (16, -30, 0, -40), (26, -10, 0, -20))
a.r("fore_l", (9, 60, 0, 0), (16, 20, 0, 0))
a.r("head", (5, -10, 0, 0), (10, 20, 0, 0), (13, 24, 0, 6), (16, -24, 0, 0), (20, -20, 0, 10), (28, 0, 0, 6))
legs(a, [(0, 0, 0, 2), (5, 30, 0, 2), (9, -20, 0, 2), (13, 50, 0, 4), (16, -10, 0, 2), (20, -16, 0, 2), (36, 0, 0, 2)],
     [(0, 3, 0, -3), (5, 30, 0, -3), (9, 20, 0, -3), (13, 10, 0, -3), (16, 50, 0, -3), (20, 46, 0, -3), (36, 3, 0, -3)],
     sr=[(0, 0, 0, 0), (5, -50, 0, 0), (9, -10, 0, 0), (13, -80, 0, 0), (16, -10, 0, 0), (36, 0, 0, 0)],
     sl=[(0, -6, 0, 0), (5, -50, 0, 0), (9, -60, 0, 0), (13, -90, 0, 0), (16, -80, 0, 0), (20, -76, 0, 0), (36, -6, 0, 0)])
a.hair([(0, 0, 0, 0), (5, 6, 0, 0), (9, -16, 0, 0), (13, -10, 0, 0), (16, 22, 0, 0), (22, 6, 0, 0), (36, 0, 0, 0)])
a.coat([(0, 0, 0, 0), (5, 6, 0, 0), (9, -26, 0, 0), (13, -16, 0, 0), (16, 26, 0, 0), (24, 4, 0, 0), (36, 0, 0, 0)], delay=1)
a.done()

# ------------------------------------------------------------------ toxic_palm (ENRAGED, 40): goggles snap down, gloves ooze glow 0-12, lunge 13, palm to the face 15,
#                                                                   grinds, toxic burst shove 26
a = A("toxic_palm", 40)
a.pos("goggles", (0, 0, 0, 0), (3, 0, 0.4, 0), (5, 0, -3.3, -0.6), (6, 0, -3.0, -0.6), (34, 0, -3.0, -0.6), (37, 0, 0.3, 0), (40, 0, 0, 0))
a.rot("goggles", (0, 0, 0, 0), (5, 18, 0, 0), (34, 18, 0, 0), (38, 0, 0, 0))
a.show("tox_r", 6, 32); a.show("tox_l", 8, 28)
a.r("arm_r", (3, 140, 0, 30), (5, 150, 0, 20), (9, 30, 0, 40), (12, -30, 0, 50), (14, 90, 0, -6), (15, 96, 0, -8), (22, 92, 0, -6), (25, 70, 0, -4), (26, 100, 0, -2),
    (29, 96, 0, 0), (36, 10, 0, 12))
a.r("fore_r", (3, 60, 0, 0), (12, 90, 0, 0), (15, 0, 0, 0), (25, 20, 0, 0), (26, 0, 0, 0), (34, 30, 0, 0))
a.r("hand_r", (5, -30, 0, 0), (12, 0, 0, 0), (15, -80, 0, 0), (17, -76, 0, 4), (20, -80, 0, -4), (23, -76, 0, 4), (26, -90, 0, 0), (32, -20, 0, 0))
a.r("arm_l", (8, 40, 0, -40), (12, 60, 0, -40), (15, -20, 0, -40), (24, -10, 0, -30), (26, 70, 0, -16), (30, 60, 0, -14), (36, -4, 0, -12))
a.r("fore_l", (8, 80, 0, 0), (15, 40, 0, 0), (26, 0, 0, 0), (34, 20, 0, 0))
a.r("chest", (5, 10, 10, 0), (12, 16, -20, 0), (15, -16, 14, 0), (22, -14, 10, 0), (26, -20, 4, 0), (32, -6, 0, 0))
a.r("head", (3, 10, 0, 0), (5, -10, 0, 0), (8, 0, 0, 14), (12, -6, 12, 10), (15, -12, -10, 0), (19, -10, -10, 16), (22, -10, -10, -6), (26, -14, 0, 0), (34, 6, 0, 12))
a.rot("body", (0, 0, 0, 0), (12, 0, -20, 0), (15, -6, 14, 0), (24, -4, 10, 0), (27, -8, 0, 0), (40, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (12, 0, -1.4, 1.0), (15, 0, -0.8, -2.6), (24, 0, -0.8, -2.4), (27, 0, -1.0, -3.0), (40, 0, 0, 0))
legs(a, [(0, 0, 0, 2), (12, 20, 0, 4), (15, -34, 0, 2), (24, -30, 0, 2), (27, -36, 0, 2), (40, 0, 0, 2)],
     [(0, 3, 0, -3), (12, -16, 0, -4), (15, 28, 0, -3), (24, 24, 0, -3), (27, 30, 0, -3), (40, 3, 0, -3)],
     sr=[(0, 0, 0, 0), (12, -40, 0, 0), (15, 20, 0, 0), (40, 0, 0, 0)], sl=[(0, -6, 0, 0), (12, -10, 0, 0), (15, -34, 0, 0), (40, -6, 0, 0)])
a.hair([(0, 0, 0, 0), (5, 8, 0, 0), (12, 4, 0, 14), (15, -14, 0, -10), (20, -6, 0, 0), (26, 14, 0, 0), (32, 2, 0, 0), (40, 0, 0, 0)])
a.coat([(0, 0, 0, 0), (12, 4, 0, 10), (15, -16, 0, -10), (24, -6, 0, -4), (27, 14, 0, 0), (40, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ experiment (ENRAGED signature, 60): "Hold still, specimen!" - dash 6, slap 10, backslap 16,
#   double-glove uppercut 24 (launches), leaps after it 30, both clipboards spike it into the floor 38 (shockwave), goggles flash, giggle
a = A("experiment", 60)
a.pos("goggles", (0, 0, 0, 0), (2, 0, -3.3, -0.6), (52, 0, -3.3, -0.6), (55, 0, 0.3, 0), (58, 0, 0, 0))
a.rot("goggles", (0, 0, 0, 0), (2, 18, 0, 0), (52, 18, 0, 0), (56, 0, 0, 0))
a.show("tox_r", 3, 44); a.show("tox_l", 3, 44)
a.pos("root", (0, 0, 0, 0), (4, 0, -1.4, 1), (6, 0, -0.6, -3), (8, 0, -0.6, -6), (26, 0, -0.6, -6), (28, 0, -2.4, -6), (31, 0, 10, -8), (34, 0, 14, -9), (36, 0, 8, -10),
      (38, 0, -3.0, -10), (44, 0, -2.6, -10), (52, 0, 0, -10), (60, 0, 0, -10))
a.rot("root", (0, 0, 0, 0), (31, 0, 0, 0), (34, 14, 0, 0), (38, 0, 0, 0), (60, 0, 0, 0))
a.rot("body", (0, 0, 0, 0), (4, -24, 0, 0), (8, -10, 0, 0), (10, -4, 24, 0), (13, -4, 20, 0), (16, -4, -24, 0), (19, -4, -20, 0), (22, -20, 0, 0), (24, 14, 0, 0),
      (28, -26, 0, 0), (31, 10, 0, 0), (35, 16, 0, 0), (38, -36, 0, 0), (44, -32, 0, 0), (52, -4, 0, 0), (60, 0, 0, 0))
a.r("arm_r", (4, -40, 0, 30), (8, 60, -70, 0), (10, 84, 36, 0), (13, 70, 40, 0), (16, 40, 0, 20), (21, -30, 0, 20), (24, 176, 0, 4), (27, 150, 0, 10),
    (31, 160, 0, 20), (35, 190, 0, 10), (38, 60, 0, 4), (44, 54, 0, 6), (50, 140, 0, 30), (53, 150, 0, 40), (56, 20, 0, 14))
a.r("arm_l", (4, -40, 0, -30), (8, 20, 0, -20), (12, 40, -50, 0), (14, 60, -66, 0), (16, 84, 50, 0), (19, 70, 60, 0), (21, -30, 0, -20), (24, 176, 0, -4),
    (27, 150, 0, -10), (31, 160, 0, -20), (35, 190, 0, -10), (38, 60, 0, -4), (44, 54, 0, -6), (50, 30, 0, -20), (56, -4, 0, -12))
a.r("fore_r", (8, 30, 0, 0), (10, 4, 0, 0), (16, 50, 0, 0), (21, 100, 0, 0), (24, 10, 0, 0), (31, 30, 0, 0), (35, 30, 0, 0), (38, 0, 0, 0), (50, 60, 0, 0), (56, 22, 0, 0))
a.r("fore_l", (8, 60, 0, 0), (16, 4, 0, 0), (21, 100, 0, 0), (24, 10, 0, 0), (31, 30, 0, 0), (35, 30, 0, 0), (38, 0, 0, 0), (50, 30, 0, 0))
a.r("hand_r", (8, 0, 80, 0), (10, 0, 90, 0), (16, 0, 0, 0), (24, -30, 0, 0), (31, 0, 90, 0), (38, 0, 90, -10), (46, 0, 90, 0), (50, 0, 0, 0))
a.r("hand_l", (12, 0, -60, 0), (16, 0, -90, 0), (20, 0, 0, 0), (24, -30, 0, 0), (31, 0, -90, 0), (38, 0, -90, 10), (46, 0, -90, 0), (50, 0, 0, 0))
a.r("chest", (4, 10, 0, 0), (8, 0, -24, 0), (10, 0, 22, 0), (14, 0, -20, 0), (16, 0, -28, 0), (19, 0, -20, 0), (22, 16, 0, 0), (24, -10, 0, 0), (28, 6, 0, 0),
    (31, 10, 0, 0), (38, -20, 0, 0), (44, -18, 0, 0), (50, 4, 0, 10), (53, 4, 0, -10), (56, 4, 0, 8))
a.r("head", (4, -14, 0, 0), (10, -6, -16, 0), (16, -6, 16, 0), (22, -16, 0, 0), (24, 30, 0, 0), (28, 24, 0, 0), (31, 10, 0, 0), (38, -26, 0, 0), (44, -20, 0, 0),
    (48, 20, 0, 14), (50, 26, 0, -10), (52, 24, 0, 12), (54, 26, 0, -10), (58, 6, 0, 8))
legs(a, [(0, 0, 0, 2), (4, 40, 0, 2), (6, -40, 0, 2), (8, -20, 0, 2), (22, -10, 0, 4), (24, -40, 0, 2), (28, 50, 0, 4), (31, 70, 0, 4), (35, 30, 0, 4), (38, 50, 0, 8),
          (44, 46, 0, 8), (52, 0, 0, 2), (60, 0, 0, 2)],
     [(0, 3, 0, -3), (4, -10, 0, -3), (6, 40, 0, -3), (8, 20, 0, -3), (22, 30, 0, -4), (24, 20, 0, -3), (28, 50, 0, -4), (31, 70, 0, -4), (35, 30, 0, -4),
      (38, 50, 0, -8), (44, 46, 0, -8), (52, 3, 0, -3), (60, 3, 0, -3)],
     sr=[(0, 0, 0, 0), (4, -60, 0, 0), (6, -10, 0, 0), (22, -40, 0, 0), (24, 0, 0, 0), (28, -90, 0, 0), (31, -110, 0, 0), (35, -20, 0, 0), (38, -84, 0, 0), (44, -80, 0, 0),
         (52, 0, 0, 0), (60, 0, 0, 0)],
     sl=[(0, -6, 0, 0), (4, -30, 0, 0), (6, -40, 0, 0), (22, -40, 0, 0), (24, -10, 0, 0), (28, -90, 0, 0), (31, -110, 0, 0), (35, -20, 0, 0), (38, -84, 0, 0),
         (44, -80, 0, 0), (52, -6, 0, 0), (60, -6, 0, 0)])
a.hair([(0, 0, 0, 0), (4, 6, 0, 0), (7, -16, 0, 0), (10, -6, 0, -16), (16, -6, 0, 16), (22, 6, 0, 0), (25, -20, 0, 0), (31, -16, 0, 0), (35, -10, 0, 0), (39, 26, 0, 0),
        (44, 8, 0, 0), (49, 0, 0, 10), (53, 0, 0, -10), (60, 0, 0, 0)], delay=1)
a.coat([(0, 0, 0, 0), (4, 6, 0, 0), (7, -26, 0, 0), (10, -10, 0, -14), (16, -10, 0, 14), (25, -20, 0, 0), (31, -30, 0, 0), (36, -36, 0, 0), (39, 30, 0, 0),
        (46, 6, 0, 0), (60, 0, 0, 0)], delay=1)
a.done()

# ------------------------------------------------------------------ death (40): drops both clipboards, wobbles, a last giggle, topples onto her back
a = A("death", 40)
a.pos("board_r", (0, 0, 0, 0), (6, 0, 0, 0), (10, 0, -6, -1), (12, 0, -7.2, -1), (40, 0, -7.2, -1))
a.rot("board_r", (0, 0, 0, 0), (6, 0, 0, 0), (12, -80, 0, 20), (40, -86, 0, 20))
a.pos("board_l", (0, 0, 0, 0), (8, 0, 0, 0), (12, 0, -6, -1), (14, 0, -7.2, -1), (40, 0, -7.2, -1))
a.rot("board_l", (0, 0, 0, 0), (8, 0, 0, 0), (14, -84, 0, -16), (40, -88, 0, -16))
a.r("arm_r", (6, 20, 0, 20), (12, 10, 0, 30), (18, 40, 0, 20), (24, 160, 0, 60), (30, 170, 0, 80), (40, 170, 0, 80))
a.r("arm_l", (8, 20, 0, -20), (14, 10, 0, -30), (18, 30, 0, -20), (24, 160, 0, -60), (30, 170, 0, -80), (40, 170, 0, -80))
a.r("fore_r", (6, 60, 0, 0), (18, 80, 0, 0), (24, 10, 0, 0), (40, 20, 0, 0))
a.r("fore_l", (8, 60, 0, 0), (18, 80, 0, 0), (24, 10, 0, 0), (40, 20, 0, 0))
a.r("head", (4, -24, 0, 0), (10, -20, 0, 20), (14, -20, 0, -16), (18, 20, 0, 6), (24, 30, 0, 0), (32, 20, 0, 20), (40, 16, 30, 20))
a.r("chest", (4, -16, 0, 0), (10, -12, 0, 8), (14, -12, 0, -8), (18, 10, 0, 0), (24, 16, 0, 0), (40, 10, 0, 0))
a.pos("root", (0, 0, 0, 0), (18, 0, 0, 0), (22, 0, 3.0, 1.0), (26, 0, 3.4, 1.2), (29, 0, 2.6, 1.0), (31, 0, 3.0, 1.0), (34, 0, 2.6, 1.0), (40, 0, 2.6, 1.0))
a.rot("root", (0, 0, 0, 0), (18, 0, 0, 0), (22, 40, 0, 0), (26, 82, 0, 4), (29, 90, 0, 4), (31, 84, 0, 4), (34, 90, 0, 4), (40, 90, 0, 4))
legs(a, [(0, 0, 0, 2), (10, 4, 0, 4), (14, -6, 0, 0), (18, 0, 0, 2), (22, 40, 0, 10), (26, 60, 0, 16), (30, 30, 0, 14), (40, 26, 0, 14)],
     [(0, 3, 0, -3), (10, -6, 0, 0), (14, 6, 0, -4), (18, 3, 0, -3), (22, 30, 0, -10), (26, 46, 0, -16), (30, 10, 0, -14), (40, 10, 0, -14)],
     sr=[(0, 0, 0, 0), (10, -14, 0, 0), (18, -20, 0, 0), (26, -50, 0, 0), (30, -20, 0, 0), (40, -26, 0, 0)],
     sl=[(0, -6, 0, 0), (14, -20, 0, 0), (26, -30, 0, 0), (30, -6, 0, 0), (40, -10, 0, 0)])
a.hair([(0, 0, 0, 0), (10, -4, 0, 10), (14, -4, 0, -10), (18, 0, 0, 0), (22, 30, 0, 0), (27, -30, 0, 0), (31, -40, 0, 0), (40, -40, 0, 0)])
a.coat([(0, 0, 0, 0), (18, 0, 0, 0), (22, 30, 0, 0), (27, 10, 0, 0), (31, 20, 0, 0), (40, 16, 0, 0)])
a.done()

os.makedirs(os.path.dirname(OUT), exist_ok=True)
m.save(OUT)
print("cubes", len(m.cubes), "anims", [x["name"] for x in m.anims], "maxY", max(c["to"][1] for c in m.cubes), "atlas rows", m.cy + m.rowh)
