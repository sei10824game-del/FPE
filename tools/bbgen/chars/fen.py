"""Fen - generates assets/fpe/bbmodels/fen.bbmodel  (~3.9 blocks tall, ONE form, shape-shifting ink arms).
References: docs/ref/confirmed/fen.jpg (main) + fen_new.jpg: very tall + thin, huge orange-red mane flowing out like a tail with
curled flame tips, curled ahoge, bangs hiding the eyes (one eye peeking), shark grin, black tee, rolled blue denim shorts,
bandaged legs, bare feet with black claws, forearms turning into ink-black arms that end in LONG black blade claws.
No form change: every "monster" attack (m_*) is a normal attack of this single model.
Shape-shift props (hidden unless an attack shows them): scythe_r/l, whip_r(+kama), hook_l, needles_r/l, wing_r/l, hammer_r, maw_r,
spider, drill_r, pincer_r/l, wire_r/l, grapnel_r, bwing_r/l, roots_r/l, barrage, boom_r, spiral, ahblade.
Blockbench space: Y up, ground 0, faces -Z, character's RIGHT = +X.
Signs (file values): limb rx>0 swings forward, torso/head rx>0 leans back / looks up, ry>0 turns to the character's left,
hanging part rz>0 swings toward +X.  Jaw rx<0 opens.
Size: max cube top 62.5 px (~3.9 blocks, hitbox 3.2) straight from this script - no rescale needed.
Run: python3 tools/bbgen/chars/fen.py
"""
import math, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))
from bbgen import mix  # noqa: E402
from alice import Builder, A, HIDE  # noqa: E402

DIR = os.path.join(os.path.dirname(__file__), "../../../src/main/resources/assets/fpe/bbmodels/")

HAIR, HAIR_M, HAIR_D, HAIR_HI, HAIR_R = 0xF39232, 0xE2702A, 0xB4471E, 0xFFC064, 0xC9452A
SKIN, SKIN_D, SKIN_L = 0xF1D0B5, 0xD2A88E, 0xFBE3CF
SHIRT, SHIRT_D, SHIRT_HI = 0x1C1C25, 0x101016, 0x30303E
DENIM, DENIM_D, DENIM_L, DENIM_HI = 0x46679E, 0x2B4470, 0x7B9FD0, 0xA9C4E8
BAND, BAND_D = 0xEFE8DA, 0xB9AF9E
CLAW, CLAW_HI, CLAW_RED, CLAW_D = 0x14141B, 0x3A3A4A, 0x4A1220, 0x08080B
EDGE = 0xE0324A
TEETH, TEETH_D, MOUTH, LINE = 0xFAF6EE, 0xB8B0A4, 0x4A0F18, 0x24161A
MON, MON_HI, MON_RED = 0x0B0A0E, 0x1E1C26, 0xFF2A2A
MREDD = 0x8A0E14


# ================================================================== painters
def denim_p(B):
    R = B.R

    def f(F):
        for y in range(F.h):
            for x in range(F.w):
                F.px(x, y, mix(DENIM, DENIM_L, 0.18 * math.sin(math.pi * x / max(1, F.w)) + R.uniform(-0.04, 0.06)))
        for i in range(1, max(2, F.w // 9)):
            x = i * 9 + R.randint(-1, 1)
            F.line(x, 0, x, F.h, DENIM_D, 1)
            for y in range(1, F.h, 3):
                F.px(x + 1, y, DENIM_HI)
        F.rect(0, 0, F.w, 1, DENIM_D)
    return f


def cuff_p(F):
    F.rect(0, 0, F.w, F.h, DENIM_L)
    F.rect(0, 0, F.w, 2, DENIM_HI)
    F.rect(0, F.h - 2, F.w, 2, DENIM)
    F.rect(0, F.h // 2, F.w, 1, DENIM)


def band_p(B, base=SKIN, full=False):
    R = B.R

    def f(F):
        F.rect(0, 0, F.w, F.h, base)
        y = R.randint(0, 3)
        while y < F.h + F.w:
            if full or R.random() < 0.85:
                th = 3 + R.randint(0, 1)
                F.poly([(0, y), (F.w, y - F.w * 0.35), (F.w, y - F.w * 0.35 + th), (0, y + th)], BAND)
                F.line(0, y + th, F.w, y - F.w * 0.35 + th, BAND_D, 1)
            y += 4 + R.randint(0, 2)
        if R.random() < 0.5:
            F.disc(R.uniform(2, F.w - 2), R.uniform(2, F.h - 2), 1.2, 0xB4505A)
    return f


def claw_p(F):
    for y in range(F.h):
        for x in range(F.w):
            F.px(x, y, mix(CLAW, CLAW_RED, 0.6 * y / max(1, F.h - 1)))
    F.rect(0, 0, 1, F.h, CLAW_HI)
    F.rect(F.w - 1, 0, 1, F.h, CLAW_D)


def ink_p(B):
    R = B.R

    def f(F):
        for y in range(F.h):
            for x in range(F.w):
                F.px(x, y, mix(CLAW, CLAW_HI, 0.3) if R.random() < 0.07 else CLAW)
        for _ in range(max(1, F.w // 3)):
            x = R.uniform(0, F.w)
            F.line(x, R.uniform(0, F.h * 0.3), x + R.uniform(-1, 1), F.h, CLAW_HI, 1)
    return f


def elbow_p(B):
    R = B.R

    def f(F):
        F.rect(0, 0, F.w, F.h, SKIN)
        F.rect(0, 0, F.w, 2, SKIN_D)
        edge = [F.h * 0.4 + R.uniform(-3, 3) for _ in range(F.w + 1)]
        for x in range(F.w):  # ragged ink creeping up the arm
            for y in range(int(edge[x]), F.h):
                F.px(x, y, CLAW)
            if x % 3 == 0:
                F.line(x, edge[x], x, edge[x] - R.uniform(1, 6), CLAW, 1)
    return f


def face_p(F):
    W, H = F.w, F.h
    for y in range(H):
        F.rect(0, y, W, 1, mix(SKIN_L, SKIN, y / H))
    F.rect(0, 0, W, int(H * 0.3), mix(SKIN, HAIR_D, 0.45))  # shadow of the bangs
    ex, ey = 0.7 * W, 0.47 * H  # peeking eye (character's left)
    F.disc(ex, ey, 0.13 * W, LINE)
    F.disc(ex, ey, 0.105 * W, 0xFFFFFF)
    F.disc(ex - 0.01 * W, ey + 0.01 * H, 0.05 * W, 0x101014)
    F.disc(ex + 0.025 * W, ey - 0.03 * H, 0.018 * W, 0xFFFFFF, glow=True)
    F.line(ex - 0.15 * W, ey - 0.13 * H, ex + 0.15 * W, ey - 0.16 * H, LINE, 2)
    F.disc(0.3 * W, 0.47 * H, 0.1 * W, mix(SKIN_D, LINE, 0.3))
    top = H * 0.78  # wide shark grin (upper teeth; the jaw carries the lower teeth)
    F.poly([(0.06 * W, H * 0.6), (0.15 * W, top), (0.85 * W, top), (0.94 * W, H * 0.6), (0.96 * W, H), (0.04 * W, H)], LINE)
    F.poly([(0.09 * W, H * 0.66), (0.17 * W, top + 1), (0.83 * W, top + 1), (0.91 * W, H * 0.66), (0.93 * W, H), (0.07 * W, H)], MOUTH)
    n = 10
    for i in range(n):
        x0 = 0.08 * W + i * 0.84 * W / n
        tw = 0.84 * W / n
        F.poly([(x0, top + 1), (x0 + tw, top + 1), (x0 + tw * 0.5, H)], TEETH)
        F.line(x0 + tw * 0.5, top + 1, x0 + tw * 0.5, top + (H - top) * 0.5, TEETH_D, 1)
    F.disc(0.16 * W, 0.6 * H, 0.04 * W, mix(SKIN, 0xE58C8C, 0.5))
    F.disc(0.84 * W, 0.6 * H, 0.04 * W, mix(SKIN, 0xE58C8C, 0.5))


def jaw_p(F):
    W, H = F.w, F.h
    F.rect(0, 0, W, H, SKIN)
    F.rect(0, H - 2, W, 2, SKIN_D)
    F.rect(int(0.06 * W), 0, int(0.88 * W), int(H * 0.62), LINE)
    F.rect(int(0.08 * W), 0, int(0.84 * W), int(H * 0.55), MOUTH)
    n = 9
    for i in range(n):
        x0 = 0.09 * W + i * 0.82 * W / n
        tw = 0.82 * W / n
        F.poly([(x0, H * 0.55), (x0 + tw, H * 0.55), (x0 + tw * 0.5, 0)], TEETH)


def mouth_p(F):
    F.rect(0, 0, F.w, F.h, MOUTH)
    F.rect(0, 0, F.w, 2, TEETH)


def toes_p(F):
    F.rect(0, 0, F.w, F.h, SKIN)
    F.rect(0, 0, F.w, 3, BAND)
    for x in range(2, F.w, 4):
        F.line(x, F.h * 0.4, x, F.h, SKIN_D, 1)


def shirt_p(B):
    folds = B.folds(SHIRT, SHIRT_D, SHIRT_HI, 3)

    def f(F):
        folds(F)
        F.rect(0, 0, F.w, 1, SHIRT_HI)
    return f


def blade_p(B):
    R = B.R

    def f(F):
        for y in range(F.h):
            for x in range(F.w):
                F.px(x, y, mix(CLAW, CLAW_RED, 0.5 * x / max(1, F.w - 1) + R.uniform(-0.05, 0.05)))
        for _ in range(3):
            y = R.uniform(0, F.h)
            F.line(0, y, F.w, y + R.uniform(-3, 3), CLAW_HI, 1)
    return f


def maw_in_p(F):
    F.rect(0, 0, F.w, F.h, MREDD)
    for x in range(0, F.w, 5):
        F.poly([(x, 0), (x + 4, 0), (x + 2, min(F.h, 6))], TEETH)


# ================================================================== model
PROPS = ("scythe_r", "scythe_l", "whip_r", "hook_l", "needles_r", "needles_l", "wing_r", "wing_l", "hammer_r", "maw_r", "spider",
         "drill_r", "pincer_r", "pincer_l", "wire_r", "wire_l", "kama", "grapnel_r", "bwing_r", "bwing_l", "roots_r", "roots_l",
         "barrage", "boom_r", "spiral", "ahblade")
SIDES = ((1, "r"), (-1, "l"))


def build(B):
    g, c = B.g, B.c
    hair = B.all(B.strands(HAIR, HAIR_HI, HAIR_D))
    hairm = B.all(B.strands(HAIR_M, HAIR, HAIR_R))
    shirt = B.all(shirt_p(B))
    denim = B.all(denim_p(B))
    band = B.all(band_p(B))
    bandf = B.all(band_p(B, BAND, True))
    ink = B.all(ink_p(B))
    bl = B.all(blade_p(B))


    g("root", (0, 0, 0))
    # ---------------- pelvis / legs (knee 15, ankle 2)
    g("pelvis", (0, 27, 0), "root")
    c("hips", "pelvis", (-3.2, 24.6, -2.0), (3.2, 28.4, 2.0), DENIM, faces=denim)
    c("belt", "pelvis", (-3.3, 27.6, -2.1), (3.3, 28.5, 2.1), DENIM_D)
    c("fly", "pelvis", (-0.3, 25.2, -2.15), (0.3, 27.6, -1.95), DENIM_D)
    for s in (1, -1):
        c(f"pocket{s}", "pelvis", (1.0 * s - 0.9, 25.4, 2.0), (1.0 * s + 0.9, 27.0, 2.15), DENIM_L)
    for s, k in SIDES:
        x = 1.6 * s
        g("leg_" + k, (x, 26, 0), "pelvis")
        c("thigh_" + k, "leg_" + k, (x - 1.4, 19.0, -1.5), (x + 1.4, 26.2, 1.5), DENIM, faces=denim)
        c("cuff_" + k, "leg_" + k, (x - 1.65, 18.2, -1.75), (x + 1.65, 19.9, 1.75), DENIM_L, faces=B.all(cuff_p))
        c("lthigh_" + k, "leg_" + k, (x - 0.95, 15.0, -0.95), (x + 0.95, 18.4, 0.95), SKIN, faces=band)
        g("shin_" + k, (x, 15, 0), "leg_" + k)
        c("knee_" + k, "shin_" + k, (x - 1.05, 13.6, -1.1), (x + 1.05, 15.6, 1.05), BAND, faces=bandf)
        c("calf_" + k, "shin_" + k, (x - 0.85, 2.0, -0.85), (x + 0.85, 14.0, 0.85), SKIN, faces=band)
        c("wrap_" + k, "shin_" + k, (x - 1.0, 5.0, -1.0), (x + 1.0, 9.5, 1.0), BAND, faces=bandf)
        g("foot_" + k, (x, 2, 0), "shin_" + k)
        c("sole_" + k, "foot_" + k, (x - 1.0, 0, -3.0), (x + 1.0, 1.6, 0.9), SKIN, faces={"north": toes_p, "up": toes_p})
        c("anktape_" + k, "foot_" + k, (x - 1.05, 1.0, -1.05), (x + 1.05, 2.4, 1.05), BAND, faces=bandf)
        for i, dx in enumerate((-0.6, 0.0, 0.6)):  # black toe claws
            B.blade(f"toe{i}_{k}", "foot_" + k, (x + dx * s, 0.5, -2.9), 1.5, 0.5, 0.6, (-80, 0, 0), CLAW, tip=CLAW_HI)

    # ---------------- torso (tall, thin)
    g("body", (0, 28.5, 0), "pelvis")
    c("waist", "body", (-2.5, 28.0, -1.55), (2.5, 34.0, 1.55), SHIRT, faces=shirt)
    c("chest", "body", (-3.2, 33.6, -1.8), (3.2, 41.0, 1.8), SHIRT, faces=shirt)
    for i, x in enumerate((-2.4, -0.8, 0.9, 2.3)):  # ragged tee hem
        c(f"hem{i}", "body", (x - 0.75, 27.3 + 0.3 * (i % 2), -1.75), (x + 0.75, 28.6, 1.75), SHIRT_D, rot=(0, 0, (i - 1.5) * 6))
    c("collar", "body", (-1.6, 40.7, -1.9), (1.6, 41.2, 1.2), SHIRT_HI)
    c("neck", "body", (-0.85, 40.8, -0.85), (0.85, 44.0, 0.85), SKIN_D)

    # ---------------- head
    g("head", (0, 43.5, 0), "body")
    g("hface", (0, 43.5, 0), "head")
    c("skull", "hface", (-3.3, 44.0, -3.2), (3.3, 51.2, 3.2), SKIN, faces={"north": face_p, "down": mouth_p})
    g("jaw", (0, 44.0, 1.0), "hface")
    c("jawc", "jaw", (-3.0, 42.3, -3.1), (3.0, 44.05, 1.5), SKIN, faces={"north": jaw_p, "up": mouth_p})

    g("hair", (0, 48, 0), "head")
    c("cap", "hair", (-3.8, 49.6, -3.8), (3.8, 52.6, 3.8), HAIR, faces=hair)
    c("capb", "hair", (-3.8, 43.0, 0.3), (3.8, 49.8, 3.9), HAIR_M, faces=hairm)
    for s, k in SIDES:
        c("sideh_" + k, "hair", (3.3 * s - 0.6, 43.0, -3.6) if s > 0 else (-3.9, 43.0, -3.6), (3.9, 50.0, 3.4) if s > 0 else (-3.3 + 0.6, 50.0, 3.4),
          HAIR, faces=hair)
        g("side_" + k, (3.7 * s, 49.5, -1.8), "hair", rot=(-4, 0, 8 * s))
        B.lock("sl0_" + k, "side_" + k, (3.7 * s, 49.5, -1.8), 13.0, 2.0, 1.4, (0, 0, 3 * s), HAIR, tip=HAIR_D, paint=hair["north"])
        B.lock("sl1_" + k, "side_" + k, (3.9 * s, 49.0, 0.8), 10.0, 1.8, 1.6, (6, 0, 9 * s), HAIR_M, tip=HAIR_R, paint=hair["north"])
    g("bangs", (0, 52.0, -3.9), "hair")
    for i, (x, ln, rz) in enumerate(((3.0, 5.6, 10), (1.6, 6.4, 6), (0.2, 6.6, 2), (-1.2, 3.2, -4), (-2.5, 5.4, -6), (-3.4, 4.6, -12))):
        B.lock(f"bang{i}", "bangs", (x, 52.4, -4.0), ln, 2.1, 0.9, (-8, 0, rz), HAIR if i % 2 else HAIR_M, tip=HAIR_D, paint=hair["north"])
    for i, (x, z, rz, rx) in enumerate(((2.6, -1, 55, -20), (-2.2, 0, -45, -10), (0.4, 1.5, 12, 20), (-3.2, 2.5, -70, 30), (3.2, 2.5, 70, 30))):
        B.blade(f"tuft{i}", "hair", (x, 52.0, z), 3.2, 1.8, 1.6, (rx, 0, -rz), HAIR, tip=HAIR_HI, paint=hair["north"])
    # curled ahoge: stem, bend to the right, hook down
    g("ahoge", (0.4, 52.4, -0.6), "hair")
    c("ah0", "ahoge", (0.0, 52.2, -1.0), (0.8, 56.4, -0.2), HAIR, origin=(0.4, 52.4, -0.6), rot=(-10, 0, -10))
    c("ah1", "ahoge", (0.6, 55.9, -1.0), (3.6, 56.7, -0.2), HAIR, origin=(0.8, 56.2, -0.6), rot=(0, 0, 18))
    c("ah2", "ahoge", (3.0, 54.4, -1.0), (3.8, 56.6, -0.2), HAIR_D, origin=(3.4, 56.4, -0.6), rot=(0, 0, -20))

    # ---------------- mane: central chain down the back + two big side sweeps with curled flame tips
    g("manec", (0, 49.0, 3.2), "hair")
    g("mane0", (0, 49.0, 3.2), "manec", rot=(-14, 0, 0))
    c("m0a", "mane0", (-4.6, 38.0, 2.8), (4.6, 49.6, 6.4), HAIR, faces=hair)
    for s, k in SIDES:
        B.lock(f"m0f_{k}", "mane0", (4.5 * s, 47.0, 4.0), 12.0, 2.4, 2.6, (0, 0, 14 * s), HAIR_M, tip=HAIR_R, paint=hair["north"])
    g("mane1", (0, 38.6, 4.6), "mane0", rot=(-10, 0, 0))
    c("m1a", "mane1", (-5.4, 29.0, 3.0), (5.4, 39.2, 6.4), HAIR_M, faces=hairm)
    for i, x in enumerate((-5.0, -1.8, 1.8, 5.0)):
        B.lock(f"m1l{i}", "mane1", (x, 30.0, 4.7), 5.0 + (i % 2), 2.8, 2.6, (0, 0, x * 3), HAIR if i % 2 else HAIR_M, tip=HAIR_D, paint=hair["north"])
    g("mane2", (0, 29.6, 4.8), "mane1", rot=(-10, 0, 0))
    c("m2a", "mane2", (-5.6, 21.0, 3.2), (5.6, 30.0, 6.2), HAIR, faces=hair)
    g("mane3", (0, 21.5, 4.8), "mane2", rot=(-12, 0, 0))
    for i, (x, ln) in enumerate(((-4.4, 9.0), (-1.5, 11.0), (1.5, 10.0), (4.4, 8.0))):
        B.lock(f"m3l{i}", "mane3", (x, 22.0, 4.8), ln, 2.8, 2.6, (0, 0, x * 4), HAIR_M if i % 2 else HAIR_R, tip=HAIR_D, paint=hair["north"])
    for s, k in SIDES:
        B.blade(f"m3k_{k}", "mane3", (3.0 * s, 14.0, 4.8), 6.0, 2.0, 2.0, (-40, 0, -70 * s), HAIR, tip=HAIR_HI, paint=hair["north"])
    # side sweeps (asymmetric like the ref: right one lower and longer)
    for s, k, y0, par in ((1, "r", 31.0, "mane1"), (-1, "l", 38.0, "mane1")):
        x0 = 4.4 * s
        g(f"sw0_{k}", (x0, y0, 5.0), par, rot=(16, 0, 34 * s))
        c(f"sw0c_{k}", f"sw0_{k}", (x0 - 2.8, y0 - 10.0, 4.2), (x0 + 2.8, y0, 6.0), HAIR_M, faces=hairm)
        g(f"sw1_{k}", (x0, y0 - 9.5, 5.0), f"sw0_{k}", rot=(0, 0, 26 * s))
        c(f"sw1c_{k}", f"sw1_{k}", (x0 - 2.3, y0 - 18.0, 4.3), (x0 + 2.3, y0 - 9.0, 5.9), HAIR, faces=hair)
        g(f"sw2_{k}", (x0, y0 - 17.5, 5.0), f"sw1_{k}", rot=(0, 0, 62 * s))
        B.lock(f"sw2c_{k}", f"sw2_{k}", (x0, y0 - 17.5, 5.0), 8.0, 3.6, 1.6, (0, 0, 0), HAIR_R, tip=HAIR_D, paint=hair["north"])
        B.blade(f"sw2h_{k}", f"sw2_{k}", (x0, y0 - 24.0, 5.0), 5.0, 2.0, 1.4, (0, 0, 140 * s), HAIR_D, tip=HAIR_HI)  # curl hook
        B.blade(f"sw1f_{k}", f"sw1_{k}", (x0, y0 - 13.0, 5.0), 5.0, 1.8, 1.4, (0, 0, -125 * s), HAIR, tip=HAIR_HI)  # flame flick
        B.lock(f"sw0l_{k}", f"sw0_{k}", (x0 - 2.4 * s, y0 - 4.0, 5.0), 9.0, 2.2, 1.4, (0, 0, -18 * s), HAIR_R, tip=HAIR_D, paint=hair["north"])

    # ---------------- arms: short sleeve, skinny upper arm, ink forearm, long blade claws to the ground
    for s, k in SIDES:
        x = 3.9 * s
        g("arm_" + k, (x, 40.5, 0), "body")
        c("sleeve_" + k, "arm_" + k, (x - 1.2, 36.8, -1.2), (x + 1.2, 41.2, 1.2), SHIRT, faces=shirt)
        c("upper_" + k, "arm_" + k, (x - 0.7, 31.0, -0.7), (x + 0.7, 37.0, 0.7), SKIN)
        g("fore_" + k, (x, 31, 0), "arm_" + k)
        c("elbow_" + k, "fore_" + k, (x - 0.85, 28.0, -0.85), (x + 0.85, 31.3, 0.85), SKIN, faces=B.all(elbow_p(B)))
        c("forearm_" + k, "fore_" + k, (x - 1.0, 22.5, -1.0), (x + 1.0, 28.4, 1.0), CLAW, faces=ink)
        for i, y in enumerate((27.0, 25.0, 23.4)):  # ragged ink spikes on the outer forearm
            B.blade(f"aspk{i}_{k}", "fore_" + k, (x + 0.9 * s, y, 0.3 - 0.4 * i), 2.6 - 0.4 * i, 0.8, 0.8, (-40, 0, -50 * s), CLAW, tip=CLAW_HI)
        g("hand_" + k, (x, 22.5, 0), "fore_" + k)
        c("palm_" + k, "hand_" + k, (x - 1.25, 20.0, -1.3), (x + 1.25, 22.8, 1.3), CLAW, faces=ink)
        g("claws_" + k, (x, 20.2, 0), "hand_" + k)
        for i, (dx, dz, ln) in enumerate(((0.8, -0.9, 16.0), (0.0, -0.1, 17.5), (-0.8, 0.7, 15.0), (1.1, 1.0, 8.0))):
            fx = x + dx * s
            g(f"fing{i}_{k}", (fx, 20.4, dz), "claws_" + k, rot=(4 if i < 3 else -14, 0, (i - 1) * 3 * s))
            B.lock(f"cl{i}_{k}", f"fing{i}_{k}", (fx, 20.5, dz), ln, 1.2, 2.0, (0, 0, 0), CLAW, tip=CLAW_RED, paint=claw_p)
            c(f"clh{i}_{k}", f"fing{i}_{k}", (fx - 0.12, 20.5 - ln - 0.6, dz - 0.9), (fx + 0.12, 20.5 - ln + 0.6, dz - 0.3),
              CLAW_RED, origin=(fx, 20.5 - ln, dz), rot=(30, 0, 0))

        # ---- shape-shift: scythe (mantis blade from the wrist, curving forward)
        g("scythe_" + k, (x, 22.5, 0), "hand_" + k)
        c(f"scy_root_{k}", "scythe_" + k, (x - 1.3, 19.5, -1.6), (x + 1.3, 23.0, 1.6), CLAW, faces=ink)
        pv, prev = (x, 20.0, 0.0), "scythe_" + k
        for i, (ln, w, bend) in enumerate(((7.0, 3.6, 0), (6.5, 3.2, 14), (6.0, 2.6, 20), (5.0, 1.8, 28))):
            nm = f"scy{i}_{k}"
            g(nm, pv, prev, rot=(bend, 0, 0))
            px, py, pz = pv
            c(nm + "c", nm, (px - 0.35, py - ln, pz - w * 0.35), (px + 0.35, py, pz + w * 0.65), CLAW, faces=bl)
            c(nm + "e", nm, (px - 0.2, py - ln, pz - w * 0.35 - 0.45), (px + 0.2, py, pz - w * 0.35), EDGE, glow=True)
            pv, prev = (px, py - ln, pz), nm
        px, py, pz = pv
        c(f"scytip_{k}", prev, (px - 0.2, py - 3.0, pz - 0.6), (px + 0.2, py, pz + 0.4), EDGE, origin=(px, py, pz), rot=(30, 0, 0), glow=True)
        B.blade(f"scyspur_{k}", "scythe_" + k, (x, 21.0, 1.4), 4.0, 0.7, 1.0, (130, 0, 0), CLAW, tip=CLAW_RED)

        # ---- needles: forearm splits into a fan of long needles
        g("needles_" + k, (x, 22.5, 0), "hand_" + k)
        c(f"ndl_base_{k}", "needles_" + k, (x - 1.5, 19.0, -1.5), (x + 1.5, 22.8, 1.5), CLAW, faces=ink)
        for i, (rx, rz, ln) in enumerate(((0, 0, 16), (12, 10, 13), (-12, 10, 13), (12, -10, 13), (-12, -10, 13))):
            B.lock(f"ndl{i}_{k}", "needles_" + k, (x, 19.5, 0), ln, 0.6, 0.6, (rx, 0, rz), CLAW, tip=EDGE)

        # ---- wings: ragged ink feathers along the forearm (hang down when the arm is spread sideways)
        g("wing_" + k, (x, 31, 0), "fore_" + k)
        for i, (y, ln) in enumerate(((30.0, 9.0), (27.5, 11.0), (25.0, 12.5), (22.5, 13.5), (20.5, 12.0))):
            B.lock(f"wf{i}_{k}", "wing_" + k, (x - 0.6 * s, y, 0.2 * i), ln, 2.6, 0.4, (8 * i, 0, -88 * s), CLAW, tip=CLAW_RED, paint=claw_p)

    # ---- hammer (right): forearm swells into a spiked mace
    g("hammer_r", (3.9, 22.5, 0), "hand_r")
    c("ham_arm", "hammer_r", (2.2, 21.0, -1.8), (5.6, 30.0, 1.8), CLAW, faces=ink)
    c("ham_head", "hammer_r", (0.4, 12.0, -3.5), (7.4, 21.5, 3.5), CLAW, faces=ink)
    c("ham_band", "hammer_r", (0.2, 15.6, -3.7), (7.6, 17.2, 3.7), CLAW_RED)
    for i, (px, py, pz, rot) in enumerate(((3.9, 12.2, 0, (180, 0, 0)), (7.2, 17, 0, (0, 0, -90)), (0.6, 17, 0, (0, 0, 90)),
                                           (3.9, 17, -3.3, (-90, 0, 0)), (3.9, 17, 3.3, (90, 0, 0)), (6.8, 13, -3, (-135, 0, -45)),
                                           (1.0, 13, -3, (-135, 0, 45)), (6.8, 20.5, 3, (45, 0, -45)))):
        B.blade(f"hspk{i}", "hammer_r", (px, py, pz), 4.0, 1.4, 1.4, rot, CLAW, tip=EDGE)

    # ---- maw (right): forearm opens into a fanged jaw with red eyes
    g("maw_r", (3.9, 22.5, 0), "hand_r")
    c("maw_arm", "maw_r", (2.2, 20.0, -1.8), (5.6, 29.0, 1.8), CLAW, faces=ink)
    c("maw_top", "maw_r", (1.2, 10.0, -3.6), (6.6, 21.0, -0.1), CLAW, faces={**ink, "south": maw_in_p})
    for s2 in (1, -1):
        c(f"maw_eye{s2}", "maw_r", (3.9 + 1.4 * s2 - 0.5, 18.0, -3.75), (3.9 + 1.4 * s2 + 0.5, 18.8, -3.55), MON_RED, glow=True)
    for i in range(4):
        B.blade(f"mawt{i}", "maw_r", (1.8 + i * 1.4, 11.0, -0.4), 1.8, 0.6, 0.6, (90, 0, 0), TEETH)
    g("mawj_r", (3.9, 20.5, 0), "maw_r")
    c("maw_bot", "mawj_r", (1.4, 11.5, 0.1), (6.4, 20.5, 3.2), CLAW, faces={**ink, "north": maw_in_p})
    for i in range(4):
        B.blade(f"mawb{i}", "mawj_r", (2.1 + i * 1.3, 12.5, 0.2), 1.6, 0.6, 0.6, (-90, 0, 0), TEETH)

    # ---- whip (right): long segmented tentacle with a barbed tip
    g("whip_r", (3.9, 21.0, 0), "hand_r")
    pv, prev = (3.9, 21.0, 0.0), "whip_r"
    for i in range(10):
        nm = f"wh{i}"
        g(nm, pv, prev)
        w = 1.5 - 0.1 * i
        c(nm + "c", nm, (pv[0] - w / 2, pv[1] - 3.6, -w / 2), (pv[0] + w / 2, pv[1] + 0.2, w / 2), CLAW, faces=ink)
        if i % 3 == 1:
            B.blade(nm + "b", nm, (pv[0] + w / 2, pv[1] - 1.5, 0), 1.6, 0.5, 0.5, (0, 0, -120), CLAW, tip=EDGE)
        pv, prev = (pv[0], pv[1] - 3.6, 0.0), nm
    B.lock("whtip", prev, pv, 4.0, 1.4, 0.6, (0, 0, 0), CLAW, tip=EDGE)

    # ---- hook (left): chain-tentacle ending in a big hook
    g("hook_l", (-3.9, 21.0, 0), "hand_l")
    pv, prev = (-3.9, 21.0, 0.0), "hook_l"
    for i in range(8):
        nm = f"hk{i}"
        g(nm, pv, prev)
        c(nm + "c", nm, (pv[0] - 0.6, pv[1] - 3.6, -0.6), (pv[0] + 0.6, pv[1] + 0.2, 0.6), CLAW, faces=ink)
        pv, prev = (pv[0], pv[1] - 3.6, 0.0), nm
    c("hk_shank", prev, (pv[0] - 0.7, pv[1] - 5.0, -0.7), (pv[0] + 0.7, pv[1] + 0.2, 0.7), CLAW_RED)
    c("hk_bend", prev, (pv[0] - 0.6, pv[1] - 5.6, -4.0), (pv[0] + 0.6, pv[1] - 4.4, 0.6), CLAW_RED)
    c("hk_barb", prev, (pv[0] - 0.4, pv[1] - 5.2, -4.6), (pv[0] + 0.4, pv[1] - 1.8, -3.5), EDGE, origin=(pv[0], pv[1] - 5, -4), rot=(-20, 0, 0), glow=True)

    # ---- spider arms: six spindly extra arms bursting from the back
    g("spider", (0, 37, 2.0), "body")
    for i, (sx, y, out) in enumerate(((1, 39.5, 30), (-1, 39.5, 30), (1, 36.5, 55), (-1, 36.5, 55), (1, 33.5, 80), (-1, 33.5, 80))):
        k = f"sp{i}"
        g(k, (1.2 * sx, y, 2.0), "spider", rot=(-25, 0, -out * sx))
        c(k + "u", k, (1.2 * sx - 0.5, y, 1.5), (1.2 * sx + 0.5, y + 10.0, 2.5), CLAW, faces=ink)
        g(k + "j", (1.2 * sx, y + 10.0, 2.0), k, rot=(-30, 0, (out + 70) * sx))
        c(k + "f", k + "j", (1.2 * sx - 0.4, y + 10.0, 1.6), (1.2 * sx + 0.4, y + 20.0, 2.4), CLAW, faces=ink)
        c(k + "t", k + "j", (1.2 * sx - 0.25, y + 19.5, 1.75), (1.2 * sx + 0.25, y + 23.0, 2.25), EDGE, glow=True)
    shift_parts(B, ink, bl, hair)


STEEL, STEEL_D = 0xA4A9B8, 0x5E6270
MEMB = 0x2A0E16


def shift_parts(B, ink, bl, hair):
    g, c = B.g, B.c
    # ---- drill (right): wrist collar + spinning cone of offset plates with glowing spiral grooves
    g("drill_r", (3.9, 22.5, 0), "hand_r")
    c("drl_coll", "drill_r", (2.1, 19.0, -1.8), (5.7, 23.0, 1.8), CLAW, faces=ink)
    c("drl_ring", "drill_r", (1.9, 19.3, -2.0), (5.9, 20.1, 2.0), EDGE, glow=True)
    g("drillspin", (3.9, 19.0, 0), "drill_r")
    for i in range(9):
        w, y0 = 5.6 * (1 - i / 9.6), 19.0 - i * 2.3
        c(f"drl{i}", "drillspin", (3.9 - w / 2, y0 - 2.4, -w / 2), (3.9 + w / 2, y0, w / 2), CLAW if i % 2 else CLAW_HI,
          origin=(3.9, y0 - 1, 0), rot=(0, i * 20 % 90, 0), faces=bl)
        c(f"drg{i}", "drillspin", (3.9 + w / 2 - 0.1, y0 - 1.9, -0.35), (3.9 + w / 2 + 0.2, y0 - 0.1, 0.35), EDGE,
          origin=(3.9, y0 - 1, 0), rot=(0, i * 20 % 90, 0), glow=True)
    c("drltip", "drillspin", (3.6, -5.6, -0.3), (4.2, -1.0, 0.3), EDGE, glow=True)

    for s, k in SIDES:
        x = 3.9 * s
        # ---- crushing pincer: heavy wrist block + two hinged curved jaws with teeth (open in the hand's z plane)
        g("pincer_" + k, (x, 22.5, 0), "hand_" + k)
        c(f"pin_base_{k}", "pincer_" + k, (x - 1.9, 17.8, -2.1), (x + 1.9, 23.0, 2.1), CLAW, faces=ink)
        c(f"pin_band_{k}", "pincer_" + k, (x - 2.0, 19.0, -2.2), (x + 2.0, 19.7, 2.2), EDGE, glow=True)
        for zs, jn in ((-1, "A"), (1, "B")):
            nm = f"pin{jn}_{k}"
            g(nm, (x, 18.4, 0.7 * zs), "pincer_" + k)
            z0, z1 = sorted((0.3 * zs, 2.8 * zs))
            c(nm + "a", nm, (x - 1.4, 10.6, z0), (x + 1.4, 18.6, z1), CLAW, origin=(x, 18.4, 0.7 * zs), rot=(-10 * zs, 0, 0), faces=bl)
            z0, z1 = sorted((-0.4 * zs, 1.6 * zs))
            c(nm + "b", nm, (x - 1.0, 7.0, z0), (x + 1.0, 11.4, z1), CLAW_RED, origin=(x, 11.0, 1.2 * zs), rot=(30 * zs, 0, 0), faces=bl)
            c(nm + "e", nm, (x - 0.3, 6.6, -0.3), (x + 0.3, 8.0, 0.3), EDGE, origin=(x, 11.0, 1.2 * zs), rot=(30 * zs, 0, 0), glow=True)
            for i in range(3):
                B.blade(f"{nm}t{i}", nm, (x - 0.6 + 0.6 * i, 16.6 - 2.2 * i, 0.4 * zs), 1.5, 0.6, 0.6, (-90 * zs, 0, 0), TEETH)
        # ---- razor wires: five steel threads from the fingertips with glowing barbs
        g("wire_" + k, (x, 20.2, 0), "hand_" + k)
        for i in range(5):
            wx = x + (i - 2) * 0.45 * s
            nm = f"wr{i}_{k}"
            g(nm, (wx, 20.2, -0.3 + 0.15 * i), "wire_" + k, rot=(0, 0, (i - 2) * 7 * s))
            c(nm + "c", nm, (wx - 0.17, -1.6, -0.3 + 0.15 * i - 0.17), (wx + 0.17, 20.2, -0.3 + 0.15 * i + 0.17), STEEL,
              faces=B.all(B.edges(STEEL_D)))
            for j in range(4):
                c(f"{nm}b{j}", nm, (wx - 0.35, 15.5 - 5 * j, -0.3 + 0.15 * i - 0.35), (wx + 0.35, 16.2 - 5 * j, -0.3 + 0.15 * i + 0.35), EDGE,
                  glow=True, origin=(wx, 15.8 - 5 * j, 0), rot=(45, 0, 45))
        # ---- blade wings: mirrored fan of long blade plates + dark membrane along the forearm
        g("bwing_" + k, (x, 31, 0), "fore_" + k)
        c(f"bwm_{k}", "bwing_" + k, (x - 0.1, 19.0, 0.4), (x + 0.1, 31.0, 9.5), MEMB, origin=(x, 31, 0), rot=(14, 0, 0))
        for i, (y, ln) in enumerate(((30.0, 10.0), (27.5, 13.0), (25.0, 15.5), (22.5, 18.0), (20.5, 20.0))):
            nm = f"bwp{i}_{k}"
            c(nm, "bwing_" + k, (x - 0.28, y - 2.2, -0.4), (x + 0.28, y, ln), CLAW, origin=(x, y, 0), rot=(6 + 8 * i, 0, 0), faces=bl)
            c(nm + "e", "bwing_" + k, (x - 0.16, y - 2.6, -0.4), (x + 0.16, y - 2.1, ln), EDGE, origin=(x, y, 0), rot=(6 + 8 * i, 0, 0), glow=True)
        # ---- roots: tendril bundle that plunges into the ground (rootsg_ scales the length)
        g("roots_" + k, (x, 21.0, 0), "hand_" + k)
        c(f"rt_base_{k}", "roots_" + k, (x - 1.5, 18.5, -1.5), (x + 1.5, 22.6, 1.5), CLAW, faces=ink)
        g("rootsg_" + k, (x, 19.0, 0), "roots_" + k)
        for i, (rx, rz, ln) in enumerate(((0, 0, 15), (16, 12, 12), (-16, 12, 13), (14, -14, 12), (-14, -14, 13))):
            B.lock(f"rt{i}_{k}", "rootsg_" + k, (x, 19.0, 0), ln, 1.0, 1.0, (rx, 0, rz * s), CLAW, tip=EDGE, paint=ink["north"])

    # ---- kusarigama sickle at the end of the whip chain
    g("kama", (3.9, -15.0, 0), "wh9")
    c("kama_h", "kama", (3.4, -20.0, -0.5), (4.4, -14.8, 0.5), CLAW_RED)
    c("kama_b0", "kama", (3.65, -20.6, -5.0), (4.15, -19.0, 0.4), CLAW, faces=bl)
    c("kama_b1", "kama", (3.7, -20.4, -8.6), (4.1, -19.2, -4.6), CLAW, origin=(3.9, -19.8, -4.8), rot=(-28, 0, 0), faces=bl)
    c("kama_e0", "kama", (3.75, -21.0, -5.0), (4.05, -20.5, 0.0), EDGE, glow=True)
    c("kama_e1", "kama", (3.78, -20.8, -8.6), (4.02, -20.3, -4.6), EDGE, origin=(3.9, -19.8, -4.8), rot=(-28, 0, 0), glow=True)

    # ---- grappling hook (right): chain (grchain scales its reach) + four-fluke grapnel head (grhead)
    g("grapnel_r", (3.9, 21.0, 0), "hand_r")
    c("gr_cuff", "grapnel_r", (2.6, 19.6, -1.3), (5.2, 22.4, 1.3), CLAW, faces=ink)
    g("grchain", (3.9, 20.0, 0), "grapnel_r")
    for i in range(6):
        y = 20.0 - 2.4 * i
        if i % 2:
            c(f"grl{i}", "grchain", (3.75, y - 2.8, -0.7), (4.05, y, 0.7), STEEL_D)
        else:
            c(f"grl{i}", "grchain", (3.2, y - 2.8, -0.15), (4.6, y, 0.15), STEEL_D)
    g("grhead", (3.9, 5.6, 0), "grchain")
    c("gr_shank", "grhead", (3.4, 1.4, -0.5), (4.4, 6.0, 0.5), CLAW_RED)
    c("gr_eye", "grhead", (3.2, 5.6, -0.7), (4.6, 6.4, 0.7), STEEL)
    for i, r in enumerate(((0, 0, 50), (0, 0, -50), (50, 0, 0), (-50, 0, 0))):
        B.blade(f"grf{i}", "grhead", (3.9, 1.6, 0), 3.4, 0.8, 0.8, r, CLAW_RED, tip=EDGE)
    B.lock("gr_point", "grhead", (3.9, 1.6, 0), 2.6, 0.9, 0.9, (0, 0, 0), CLAW_RED, tip=EDGE)

    # ---- back barrage arms: eight ink arms arch over the shoulders and punch forward (ba{i}e = forearm + fist)
    g("barrage", (0, 37, 2.0), "body")
    for i in range(8):
        s, lv = (1 if i % 2 == 0 else -1), i // 2
        px, py, pz = 1.6 * s, 40.0 - 2.2 * lv, 2.2
        ln = 7.0 - 0.6 * lv
        g(f"ba{i}", (px, py, pz), "barrage", rot=(28 + 6 * lv, 0, -s * (22 + 16 * lv)))
        c(f"ba{i}u", f"ba{i}", (px - 0.55, py, pz - 0.55), (px + 0.55, py + ln, pz + 0.55), CLAW, faces=ink)
        ey = py + ln
        g(f"ba{i}e", (px, ey, pz), f"ba{i}", rot=(-28 - 6 * lv, 0, s * (22 + 16 * lv) * 0.6))
        c(f"ba{i}f", f"ba{i}e", (px - 0.5, ey - 0.5, pz - 13.0), (px + 0.5, ey + 0.5, pz + 0.3), CLAW, faces=ink)
        c(f"ba{i}k", f"ba{i}e", (px - 0.9, ey - 0.9, pz - 14.6), (px + 0.9, ey + 0.9, pz - 12.8), CLAW_HI)
        for j, (dx, dy) in enumerate(((-0.5, 0.4), (0.5, 0.4), (0, -0.5))):
            B.blade(f"ba{i}c{j}", f"ba{i}e", (px + dx, ey + dy, pz - 14.4), 2.8, 0.4, 0.4, (-90, 0, 0), CLAW, tip=EDGE)

    # ---- boomerang: three-bladed claw star held in the right hand (boomspin spins it)
    g("boom_r", (3.9, 19.5, 0), "hand_r")
    g("boomspin", (3.9, 17.0, 0), "boom_r")
    c("bm_hub", "boomspin", (2.7, 15.8, -0.8), (5.1, 18.2, 0.8), CLAW_RED)
    c("bm_eye", "boomspin", (3.4, 16.5, -0.95), (4.4, 17.5, 0.95), EDGE, glow=True)
    for j in range(3):
        a = j * 120
        B.lock(f"bmb{j}", "boomspin", (3.9, 17.0, 0), 12.0, 3.2, 0.6, (0, 0, a), CLAW, tip=EDGE, paint=claw_p)
        r = math.radians(a)
        bx, by = 3.9 + math.sin(r) * 9.5, 17.0 - math.cos(r) * 9.5
        B.blade(f"bmh{j}", "boomspin", (bx, by, 0), 4.0, 1.2, 0.5, (0, 0, a + 115), CLAW, tip=EDGE)

    # ---- spiral lance: both arms twist into a double helix of tendrils around a glowing core (spiralspin)
    g("spiral", (3.9, 20.0, 0), "hand_r")
    c("sp_cuff", "spiral", (2.3, 18.6, -1.6), (5.5, 22.6, 1.6), CLAW, faces=ink)
    g("spiralspin", (3.9, 19.0, 0), "spiral")
    c("sp_core", "spiralspin", (3.5, -14.0, -0.4), (4.3, 19.0, 0.4), EDGE, glow=True)
    for h in range(2):
        for i in range(16):
            ang = math.radians(i * 40 + h * 180)
            r = 4.2 * (1 - i / 18.0)
            y = 18.0 - i * 2.0
            px, pz = 3.9 + r * math.cos(ang), r * math.sin(ang)
            sz = 2.0 - 0.07 * i
            c(f"sph{h}_{i}", "spiralspin", (px - sz / 2, y - 1.0, pz - sz / 2), (px + sz / 2, y + 1.0, pz + sz / 2), CLAW if (i + h) % 2 else CLAW_HI,
              origin=(px, y, pz), rot=(0, -(i * 40 + h * 180) % 90, 24), faces=ink)

    # ---- ahoge blade: the ahoge hardens into a long curved hair-blade
    g("ahblade", (0.4, 52.4, -0.6), "ahoge")
    B.blade("ahb0", "ahblade", (0.4, 52.6, -0.6), 7.5, 1.8, 0.7, (-55, 0, -4), HAIR, tip=HAIR_HI, paint=hair["north"])
    B.blade("ahb1", "ahblade", (0.4, 56.6, -6.4), 5.5, 1.3, 0.6, (-95, 0, -4), HAIR_R, tip=EDGE, paint=hair["north"])
    c("ahbe", "ahblade", (0.25, 52.4, -0.9), (0.55, 59.8, -0.6), EDGE, origin=(0.4, 52.6, -0.6), rot=(-55, 0, -4), glow=True)

# ================================================================== animation
def m3(v):
    return (v[0], -v[1], -v[2])


THIGH, SHIN_L = 11.0, 13.0


def drop(a, k):
    """pelvis drop so a foot with thigh angle a and knee bend k stays on the ground"""
    return 24.0 - THIGH * math.cos(math.radians(a)) - SHIN_L * math.cos(math.radians(a - k))


REST = {"body": (-6, 0, 0), "head": (6, 0, 0), "jaw": (0, 0, 0),
        "arm_r": (4, 0, 6), "arm_l": (4, 0, -6), "fore_r": (6, 0, 0), "fore_l": (6, 0, 0), "hand_r": (4, 0, 0), "hand_l": (4, 0, 0),
        "leg_r": (8, 0, 2), "leg_l": (8, 0, -2), "shin_r": (-14, 0, 0), "shin_l": (-14, 0, 0), "foot_r": (6, 0, 0), "foot_l": (6, 0, 0)}
RESTP = {"pelvis": (0, -drop(8, 14), 0)}
ELONG = 1.35  # feral attacks: the ink forearms stretch


class F(A):
    def __init__(self, B, name, ticks, loop=False):
        A.__init__(self, B, name, ticks, REST, PROPS, loop)
        self.prest = dict(RESTP)

    def done(self, base_layer=False, additive=False):
        if not additive:
            if base_layer:
                for p in PROPS:
                    if "scale" not in self.tr.get(p, {}): self.scl(p, (0, *HIDE))
            self._mane_comp()
        return A.done(self, base_layer or additive)

    def _mane_comp(self, gain=0.75):
        """hair hangs with gravity: counter-rotate the mane root against the summed body+head pitch change"""
        def sample(b, t):
            ks = sorted(self.tr.get(b, {}).get("rotation", []))
            r = self.rest.get(b, Z0)
            if not ks: return r[0]
            if ks[0][0] > 0: ks.insert(0, (0, *r))
            if ks[-1][0] < self.ticks: ks.append((self.ticks, *r))
            if t <= ks[0][0]: return ks[0][1]
            for p, q in zip(ks, ks[1:]):
                if p[0] <= t <= q[0]: return p[1] + (q[1] - p[1]) * (t - p[0]) / max(1e-6, q[0] - p[0])
            return ks[-1][1]
        bones = ("body", "head")
        ts = sorted({q[0] for b in bones for q in self.tr.get(b, {}).get("rotation", [])} | {0, self.ticks})
        rest = REST["body"][0] + REST["head"][0]
        for t in ts:
            p = sum(sample(b, t) for b in bones)
            self.rot("manec", (t, max(-85, min(60, -(p - rest) * gain)), 0, 0))

    def full(self, t, **over):
        """absolute pose for base layers: every rest bone keyed"""
        for b, v in self.rest.items():
            self.rot(b, (t, *over.get(b, v)))
        return self

    # ---- pose helpers
    def legs(self, t, a=None, k=None, al=None, kl=None, up=0.0, fwd=0.0, spread=0.0, setpos=True):
        r = self.rest
        a = r["leg_r"][0] if a is None else a
        k = -r["shin_r"][0] if k is None else k
        al = a if al is None else al
        kl = k if kl is None else kl
        d = min(drop(a, k), drop(al, kl))
        sp = 2
        self.at(t, leg_r=(a, 0, sp + spread), shin_r=(-k, 0, 0), foot_r=(k - a, 0, 0),
                leg_l=(al, 0, -sp - spread), shin_l=(-kl, 0, 0), foot_l=(kl - al, 0, 0))
        if setpos: self.pos("pelvis", (t, 0, -d + up, fwd))
        return self

    def arm(self, t, k, a, f=None, h=None):
        mm = (lambda v: v) if k == "r" else m3
        self.rot("arm_" + k, (t, *mm(a)))
        if f is not None: self.rot("fore_" + k, (t, *mm(f)))
        if h is not None: self.rot("hand_" + k, (t, *mm(h)))
        return self

    def arms(self, t, a, f=None, h=None, al=None, fl=None, hl=None):
        self.arm(t, "r", a, f, h)
        return self.arm(t, "l", al if al is not None else a, fl if fl is not None else f, hl if hl is not None else h)

    def claws(self, t, curl=0.0, side=None, spread=0.0):
        for k in (("r", "l") if side is None else (side,)):
            s = 1 if k == "r" else -1
            for i in range(4):
                base = 4 if i < 3 else -14
                self.rot(f"fing{i}_{k}", (t, base + curl, 0, (i - 1) * (3 + spread) * s))
        return self

    def hide(self, bone, t0, t1, fade=2):
        keys = [(0, 1, 1, 1), (t0, 1, 1, 1), (t0 + fade, *HIDE)]
        if t1 < self.ticks: keys += [(t1 - fade, *HIDE), (t1, 1, 1, 1), (self.ticks, 1, 1, 1)]
        else: keys += [(self.ticks, *HIDE)]
        return self.scl(bone, *keys)

    def morph(self, prop, t0, t1, side, grow=4):
        """arm reshapes: claws melt away, the weapon grows out of the wrist"""
        self.show(prop, t0, t1, grow)
        if side: self.hide("claws_" + side, t0, t1)
        return self

    def sec(self, keys, delay=2):
        """hair secondary motion from body signal (t, x, z): x>0 = lurch forward (hair flies back), z>0 = sway toward +X"""
        for i in range(4):
            g = 0.45 + 0.2 * i
            self.drape(f"mane{i}", [(t, -x * g, z * 0.25 * i, z * g * 0.6) for (t, x, z) in keys], delay + i)
        for k, s in (("r", 1), ("l", -1)):
            for i in range(3):
                self.drape(f"sw{i}_{k}", [(t, -x * 0.4, 0, z * 0.5 + x * 0.6 * s * (0.6 + 0.3 * i)) for (t, x, z) in keys], delay + 1 + i)
        self.drape("bangs", [(t, -x * 0.25, 0, z * 0.3) for (t, x, z) in keys], delay)
        self.drape("side_r", [(t, -x * 0.5, 0, z * 0.6 + abs(x) * 0.3) for (t, x, z) in keys], delay)
        self.drape("side_l", [(t, -x * 0.5, 0, z * 0.6 - abs(x) * 0.3) for (t, x, z) in keys], delay)
        self.drape("ahoge", [(t, -x * 0.9, 0, z * 0.8) for (t, x, z) in keys], delay + 1)
        return self

    def wave(self, prefix, n, keys, delay=1.0):
        """travelling bend through a chain: keys (t, rx, rz) applied to segment i with i*delay lag"""
        for i in range(n):
            out, seen = [], set()
            for (t, rx, rz) in keys:
                tt = min(self.ticks, round(t + i * delay, 2))
                if tt in seen: continue
                seen.add(tt)
                out.append((tt, rx, 0, rz))
            self.rot(f"{prefix}{i}", *out)
        return self


    def spin(self, bone, keys, axis=1, base=(0, 0, 0)):
        """continuous spin: keys (t, angle) piecewise-linear, sampled every tick so catmullrom never shortcuts.
        End on a multiple of 360 at the last tick so the loop back to rest is seamless."""
        def ang(t):
            for (t0, a0), (t1, a1) in zip(keys, keys[1:]):
                if t0 <= t <= t1: return a0 + (a1 - a0) * (t - t0) / max(1e-6, t1 - t0)
            return keys[-1][1]
        out = []
        for t in range(int(keys[0][0]), int(keys[-1][0]) + 1):
            v = list(base); v[axis] += ang(t)
            out.append((t, *v))
        return self.rot(bone, *out)

    def stretch(self, t0, t1, amt=ELONG, ramp=4):
        """feral attacks: ink forearms elongate"""
        for b in ("fore_r", "fore_l"):
            self.scl(b, (0, 1, 1, 1), (t0, 1, 1, 1), (t0 + ramp, 1, amt, 1), (t1 - ramp, 1, amt, 1), (t1, 1, 1, 1), (self.ticks, 1, 1, 1))
        return self

Z0 = (0, 0, 0)


def anims(B):
    def mk(name, ticks, loop=False):
        return F(B, name, ticks, loop)

    # ================= idle (80): tall looming sway, breathing, head-cock, claw twitches, mane flowing
    a = mk("idle", 80, loop=True)
    for t, j in ((0, 0), (20, 1), (40, 0), (60, -1), (80, 0)):
        b = abs(j)
        a.full(t, body=(-6 - 2 * b, 3 * j, -1.5 * j), head=(6 + 2 * b, -4 * j, 3 * j),
               arm_r=(4 + 2 * b, 0, 6 + 2 * j), arm_l=(4 + 2 * b, 0, -6 + 2 * j), fore_r=(6 + 3 * b, 0, 0), fore_l=(6 + 3 * b, 0, 0))
        a.pos("pelvis", (t, 0, -drop(8, 14) - 0.4 * b, 0))
    a.at(46, head=(10, 12, 20)).at(52, head=(9, 10, 22)).at(56, head=(8, -2, -2))  # creepy head tilt
    a.claws(0, 0).claws(14, 14).claws(17, -6).claws(40, 0).claws(64, 18, "r").claws(67, -4, "r").claws(80, 0)
    a.sec([(0, 0, 1), (20, 2, -2), (40, 0, 1), (60, 2, -2), (80, 0, 1)], delay=5)
    a.done(base_layer=True)

    # ================= walk (24, additive): long stalking strides, claws dragging, shoulders rolling
    a = mk("walk", 24, loop=True)
    for t, sw in ((0, 1), (6, 0), (12, -1), (18, 0), (24, 1)):
        a.rot("leg_r", (t, 28 * sw, 0, 0)).rot("leg_l", (t, -28 * sw, 0, 0))
        a.rot("shin_r", (t, -34 * max(0, -sw) - (30 if t == 18 else 0), 0, 0))
        a.rot("shin_l", (t, -34 * max(0, sw) - (30 if t == 6 else 0), 0, 0))
        a.rot("foot_r", (t, 10 * max(0, -sw), 0, 0)).rot("foot_l", (t, 10 * max(0, sw), 0, 0))
        a.rot("arm_r", (t, -20 * sw, 0, 2)).rot("arm_l", (t, 20 * sw, 0, -2))
        a.rot("fore_r", (t, 10 + 8 * sw, 0, 0)).rot("fore_l", (t, 10 - 8 * sw, 0, 0))
    a.rot("body", (0, -6, 8, 0), (6, -4, 0, 0), (12, -6, -8, 0), (18, -4, 0, 0), (24, -6, 8, 0))
    a.rot("head", (0, 2, -8, 0), (6, 0, 0, 0), (12, 2, 8, 0), (18, 0, 0, 0), (24, 2, -8, 0))
    a.pos("pelvis", (0, 0, -0.9, 0), (6, 0, 0.5, 0), (12, 0, -0.9, 0), (18, 0, 0.5, 0), (24, 0, -0.9, 0))
    a.rot("pelvis", (0, 0, -6, 0), (12, 0, 6, 0), (24, 0, -6, 0))
    a.sec([(0, 4, 3), (6, 2, 0), (12, 4, -3), (18, 2, 0), (24, 4, 3)], delay=2)
    a.done(additive=True)

    abilities(mk)
    monster_abilities(mk)
    shift_abilities(mk)

    # ================= death (40): stagger, knees buckle, topple forward, claws twitch (any form reverts to the girl)
    a = mk("death", 40)
    a.at(6, body=(4, 12, 8), head=(40, -10, 12), jaw=(-30, 0, 0))
    a.arms(6, (-20, 0, 40), (30, 0, 0), (-20, 0, 0), al=(30, 0, 50))
    a.legs(6, 4, 10)
    a.at(14, body=(-30, 4, 0), head=(-10, 0, -10), jaw=(-20, 0, 0))
    a.arms(14, (20, 0, 20), (30, 0, 0))
    a.legs(14, 90, 170, setpos=False)
    a.rot("pelvis", (0, 0, 0, 0), (14, 0, 0, 0), (21, -40, 0, 0), (28, -82, 0, 6), (40, -84, 0, 6))
    a.pos("pelvis", (0, 0, -drop(8, 14), 0), (14, 0, -11, 0), (21, 0, -15, -3), (28, 0, -22, -6), (40, 0, -22.5, -6))
    a.at(28, body=(-4, 0, 0), head=(20, 20, 20), jaw=(-10, 0, 0))
    a.arms(28, (150, 0, 34), (0, 0, 0), (10, 0, 0), al=(140, 10, 40))
    a.legs(28, 30, 20, setpos=False)
    a.at(40, body=(-2, 0, 0), head=(18, 22, 22), jaw=(-12, 0, 0))
    a.arms(40, (156, 0, 36), (0, 0, 0), (14, 0, 0), al=(144, 10, 42))
    a.claws(28, 0).claws(32, 30, "r").claws(34, -10, "r").claws(36, 20, "r").claws(40, 20)
    a.sec([(0, 0, 0), (6, -8, 0), (14, 6, 0), (21, 8, 0), (28, 4, 0), (40, 0, 0)])
    a.done()


def abilities(mk):
    # ================= scythe (40): arms reshape into scythes 1-7, coil 8-12, X-CROSS sweep 14, overhead double chop 24, revert 34
    a = mk("scythe", 40)
    a.morph("scythe_r", 1, 36, "r").morph("scythe_l", 1, 36, "l")
    a.at(4, body=(-10, 0, 0), head=(14, 0, 0), jaw=(-14, 0, 0))
    a.arms(4, (40, 0, 30), (40, 0, 0), (10, 0, 0))
    a.at(10, body=(-16, -40, -6), head=(14, 30, 0), jaw=(-20, 0, 0))
    a.arms(10, (100, -80, 30), (30, 0, 0), (0, 0, 0), al=(90, 70, 10), fl=(50, 0, 0))
    a.at(12, body=(-18, -46, -8), head=(14, 34, 0))
    a.arms(12, (110, -95, 40), (24, 0, 0), (0, 0, 0), al=(80, 80, 20), fl=(60, 0, 0))
    a.at(14, body=(-26, 34, 6), head=(10, -20, 0), jaw=(-30, 0, 0))
    a.arms(14, (96, 70, 0), (0, 0, 0), (-10, 0, 0), al=(100, -76, -10), fl=(0, 0, 0))
    a.at(16, body=(-26, 46, 8), head=(10, -26, 0))
    a.arms(16, (90, 90, 0), (10, 0, 0), (0, 0, 0), al=(96, -96, -10), fl=(10, 0, 0))
    a.at(20, body=(4, 0, 0), head=(26, 0, 0), jaw=(-24, 0, 0))
    a.arms(20, (196, 0, 24), (20, 0, 0), (-10, 0, 0))
    a.at(22, body=(8, 0, 0), head=(30, 0, 0))
    a.arms(22, (206, 0, 22), (26, 0, 0), (-20, 0, 0))
    a.at(24, body=(-44, 0, 0), head=(4, 0, 0), jaw=(-8, 0, 0))
    a.arms(24, (84, 0, 8), (0, 0, 0), (20, 0, 0))
    a.at(28, body=(-40, 0, 0), head=(8, 0, 0))
    a.arms(28, (70, 0, 10), (10, 0, 0), (24, 0, 0))
    a.at(34, body=(-14, 0, 0), head=(10, 0, 0))
    a.arms(34, (24, 0, 14), (20, 0, 0), (6, 0, 0))
    a.legs(10, 30, 50, 10, 20).legs(14, 14, 24, 40, 70, fwd=-1.5).legs(20, 10, 16, up=0.4).legs(24, 50, 92, fwd=-2).legs(28, 46, 84, fwd=-2) \
        .legs(34, 20, 30)
    a.sec([(0, 0, 0), (4, -2, 0), (10, -2, -4), (14, 8, 5), (16, 6, 6), (20, -6, 0), (24, 12, 0), (28, 4, 0), (40, 0, 0)])
    a.done()

    # ================= lash (36): right arm becomes a whip 1-6, wind back 6-11, CRACK forward 13 (pull), horizontal sweep 22, reel in
    a = mk("lash", 36)
    a.hide("claws_r", 1, 33)
    a.scl("whip_r", (0, *HIDE), (0.99, *HIDE), (6, 1, 1, 1), (11, 1, 1, 1), (13, 1, 2.6, 1), (17, 1, 2.4, 1), (20, 1, 2.2, 1), (22, 1, 2.6, 1),
          (26, 1, 1.8, 1), (31, 1, 1, 1), (33, *HIDE), (36, *HIDE))
    a.at(5, body=(-4, -20, 0), head=(10, 12, 0))
    a.arm(5, "r", (40, -30, 30), (30, 0, 0)).arm(5, "l", (20, 0, -20), (20, 0, 0))
    a.at(10, body=(8, -36, -4), head=(14, 24, 0), jaw=(-12, 0, 0))
    a.arm(10, "r", (210, -20, 30), (20, 0, 0), (0, 0, 0))
    a.at(13, body=(-24, 20, 4), head=(6, -10, 0), jaw=(-28, 0, 0))
    a.arm(13, "r", (90, 10, 0), (0, 0, 0), (0, 0, 0)).arm(13, "l", (-20, 0, -30), (20, 0, 0))
    a.at(18, body=(-14, -30, -4), head=(10, 20, 0))
    a.arm(18, "r", (90, -70, 0), (0, 0, 0))
    a.at(22, body=(-18, 40, 6), head=(8, -26, 0), jaw=(-24, 0, 0))
    a.arm(22, "r", (88, 80, 0), (0, 0, 0))
    a.at(26, body=(-10, 20, 0), head=(10, -10, 0))
    a.arm(26, "r", (70, 30, 10), (30, 0, 0)).arm(31, "r", (20, 0, 10), (20, 0, 0))
    a.wave("wh", 10, [(0, 0, 0), (6, -20, 10), (10, -40, 0), (13, 4, 0), (15, 8, 0), (18, 0, 30), (22, 0, -16), (26, 30, 0), (31, 20, 0), (36, 0, 0)], 0.6)
    a.legs(10, 0, 10, 30, 50).legs(13, 40, 70, -6, 10, fwd=-1).legs(22, 30, 50).legs(30, 10, 16)
    a.sec([(0, 0, 0), (10, -4, -2), (13, 8, 2), (18, -2, -4), (22, 6, 5), (28, 0, 0), (36, 0, 0)])
    a.done()

    # ================= needles (34): forearms unfold into needle fans 1-7, right volley 12, left volley 18, both arms 24 (enraged)
    a = mk("needles", 34)
    a.morph("needles_r", 1, 31, "r").morph("needles_l", 4, 31, "l")
    a.at(6, body=(-10, -20, 0), head=(10, 14, 0), jaw=(-10, 0, 0))
    a.arm(6, "r", (60, -30, 40), (60, 0, 0), (0, 0, 0)).arm(6, "l", (20, 0, -20), (20, 0, 0))
    a.at(10, body=(0, -30, -4), head=(14, 22, 0))
    a.arm(10, "r", (120, -40, 30), (60, 0, 0))
    a.at(12, body=(-20, 20, 4), head=(6, -10, 0), jaw=(-26, 0, 0))
    a.arm(12, "r", (92, 10, 0), (0, 0, 0), (0, 0, 0)).arm(12, "l", (110, -30, -30), (60, 0, 0))
    a.arm(14, "r", (100, 14, 0), (10, 0, 0))
    a.at(16, body=(0, 30, 4), head=(14, -20, 0))
    a.arm(16, "l", (130, -40, -30), (60, 0, 0))
    a.at(18, body=(-20, -20, -4), head=(6, 10, 0), jaw=(-26, 0, 0))
    a.arm(18, "l", (92, -10, 0), (0, 0, 0), (0, 0, 0)).arm(18, "r", (50, 0, 20), (40, 0, 0))
    a.at(21, body=(10, 0, 0), head=(20, 0, 0))
    a.arms(21, (170, 0, 30), (40, 0, 0))
    a.at(24, body=(-26, 0, 0), head=(2, 0, 0), jaw=(-30, 0, 0))
    a.arms(24, (96, 0, 6), (0, 0, 0), (0, 0, 0))
    a.at(28, body=(-16, 0, 0), head=(8, 0, 0))
    a.arms(28, (70, 0, 12), (14, 0, 0))
    a.legs(6, 20, 30).legs(12, 30, 50, 0, 10, fwd=-0.6).legs(18, 0, 10, 30, 50, fwd=-0.6).legs(21, 10, 16).legs(24, 34, 60, fwd=-1).legs(30, 14, 20)
    a.sec([(0, 0, 0), (6, -2, -2), (12, 6, 3), (16, -2, 3), (18, 6, -3), (21, -5, 0), (24, 8, 0), (34, 0, 0)])
    a.done()

    # ================= wingglide (44): wings unfurl 1-8, crouch 9-11, LEAP 12, glide 13-26, dive 27, SLASH 28 on landing, fold
    a = mk("wingglide", 44)
    a.morph("wing_r", 1, 40, None, grow=6).morph("wing_l", 1, 40, None, grow=6)
    a.arms(5, (10, 0, 60), (10, 0, 0), (0, 0, 0)).arms(8, (0, 0, 92), (0, 0, 0))
    a.at(5, body=(-4, 0, 0), head=(16, 0, 0), jaw=(-20, 0, 0))
    a.at(10, body=(-30, 0, 0), head=(30, 0, 0), jaw=(-6, 0, 0))
    a.arms(10, (-30, 0, 70), (10, 0, 0))
    a.legs(10, 66, 120, fwd=1)
    a.at(12, body=(-20, 0, 0), head=(20, 0, 0), jaw=(-26, 0, 0))
    a.arms(12, (-10, 0, 110), (0, 0, 0))
    a.legs(12, -10, 10, up=3)
    for i, t in enumerate(range(14, 27, 3)):  # flaps
        u = 1 if i % 2 == 0 else -1
        a.at(t, body=(-60, 0, 2 * u), head=(54, 0, 0), jaw=(-20, 0, 0))
        a.arms(t, (-10 + 6 * u, 0, 88 + 18 * u), (6, 0, 0))
        a.legs(t, -20, 30, up=4 + u, setpos=True)
    a.at(27, body=(-70, 0, 0), head=(60, 0, 0), jaw=(-36, 0, 0))
    a.arms(27, (160, 0, 40), (0, 0, 0), (-10, 0, 0))
    a.legs(27, 30, 60, up=3)
    a.at(28, body=(-50, 0, 0), head=(30, 0, 0), jaw=(-10, 0, 0))
    a.arms(28, (60, 0, 30), (0, 0, 0), (20, 0, 0))
    a.legs(28, 70, 130)
    a.at(32, body=(-46, 0, 0), head=(28, 0, 0))
    a.arms(32, (50, 0, 40), (10, 0, 0))
    a.legs(32, 64, 120)
    a.at(38, body=(-14, 0, 0), head=(10, 0, 0))
    a.arms(38, (10, 0, 30), (10, 0, 0))
    a.legs(38, 20, 30)
    a.claws(10, 30).claws(27, -20, spread=8).claws(28, 40).claws(36, 0)
    a.sec([(0, 0, 0), (8, -2, 0), (10, 4, 0), (12, 10, 0), (14, 12, 2), (18, 12, -2), (22, 12, 2), (26, 12, 0), (28, -10, 0), (32, 4, 0), (44, 0, 0)])
    a.done()

    # ================= guard (40): wing-shields wrap in front 1-6, brace 6-26 (absorbs hits), BURST open 28, recover
    a = mk("guard", 40)
    a.morph("wing_r", 0, 34, None, grow=4).morph("wing_l", 0, 34, None, grow=4)
    a.at(5, body=(-20, 0, 0), head=(-4, 0, 0), jaw=(0, 0, 0))
    a.arms(5, (100, 40, 10), (80, 0, 0), (0, 0, 0))
    for t, j in ((8, 1), (12, -1), (16, 1), (20, -1), (24, 1)):
        a.at(t, body=(-22 + j, 0, j), head=(-6, 0, 0))
        a.arms(t, (104 + j, 44, 6), (90, 0, 0), (0, 0, 0))
    a.legs(6, 40, 70).legs(24, 44, 76)
    a.at(26, body=(-30, 0, 0), head=(-10, 0, 0), jaw=(-6, 0, 0))
    a.arms(26, (110, 54, 0), (100, 0, 0))
    a.legs(26, 50, 90)
    a.at(28, body=(10, 0, 0), head=(30, 0, 0), jaw=(-40, 0, 0))
    a.arms(28, (40, 0, 110), (0, 0, 0), (0, 0, 0))
    a.legs(28, 6, 10, up=0.5)
    a.at(31, body=(12, 0, 0), head=(32, 0, 0), jaw=(-38, 0, 0))
    a.arms(31, (30, 0, 118), (4, 0, 0))
    a.at(36, body=(-8, 0, 0), head=(8, 0, 0), jaw=(-6, 0, 0))
    a.arms(36, (10, 0, 20), (10, 0, 0))
    a.legs(36, 10, 16)
    a.claws(28, -26, spread=10).claws(34, 0)
    a.sec([(0, 0, 0), (5, 3, 0), (24, 3, 0), (26, 5, 0), (28, -12, 0), (31, -10, 0), (36, 2, 0), (40, 0, 0)])
    a.done()

    # ================= hammer (42): right arm swells into a mace 1-8, heave overhead 10-18, SLAM 20, stuck, wrench free 30, shrink
    a = mk("hammer", 42)
    a.morph("hammer_r", 1, 38, "r", grow=6)
    a.at(6, body=(-12, -10, 0), head=(10, 6, 0), jaw=(-10, 0, 0))
    a.arm(6, "r", (20, 0, 20), (10, 0, 0)).arm(6, "l", (30, 0, -20), (30, 0, 0))
    a.at(12, body=(10, -20, -4), head=(24, 12, 0), jaw=(-20, 0, 0))
    a.arm(12, "r", (170, -10, 20), (20, 0, 0), (0, 0, 0)).arm(12, "l", (60, 0, -30), (40, 0, 0))
    a.at(17, body=(18, -24, -6), head=(30, 14, 0), jaw=(-30, 0, 0))
    a.arm(17, "r", (220, -10, 16), (30, 0, 0))
    a.legs(17, -6, 10, 24, 40, up=0.6)
    a.at(20, body=(-50, 6, 2), head=(10, -4, 0), jaw=(-14, 0, 0))
    a.arm(20, "r", (60, 0, 4), (0, 0, 0), (10, 0, 0)).arm(20, "l", (10, 0, -50), (20, 0, 0))
    a.legs(20, 70, 120, 30, 60, fwd=-2)
    a.at(23, body=(-46, 4, 2), head=(14, -4, 0))
    a.arm(23, "r", (66, 0, 6), (0, 0, 0))
    a.at(28, body=(-44, 0, 0), head=(20, 0, 0), jaw=(-6, 0, 0))
    a.arm(28, "r", (70, 0, 6), (6, 0, 0))
    a.at(31, body=(-10, -14, 0), head=(16, 8, 0))
    a.arm(31, "r", (110, -10, 20), (40, 0, 0))
    a.legs(28, 66, 116, 30, 60, fwd=-2).legs(31, 30, 50).legs(38, 10, 16)
    a.at(36, body=(-8, 0, 0), head=(8, 0, 0))
    a.arm(36, "r", (20, 0, 10), (14, 0, 0)).arm(36, "l", (10, 0, -10), (10, 0, 0))
    a.sec([(0, 0, 0), (12, -4, -2), (17, -8, -3), (20, 14, 0), (24, 6, 0), (31, -3, 0), (36, 0, 0), (42, 0, 0)])
    a.done()

    # ================= spider (46): six spider arms burst from the back 2-8, flurry 12/16/20/24/28, all-arm PIN 34, retract
    a = mk("spider", 46)
    a.show("spider", 2, 42, grow=5)
    a.at(4, body=(-30, 0, 0), head=(30, 0, 0), jaw=(-30, 0, 0))
    a.arms(4, (-20, 0, 40), (30, 0, 0), (-20, 0, 0))
    a.legs(4, 40, 70)
    a.at(8, body=(-18, 0, 0), head=(20, 0, 0), jaw=(-20, 0, 0))
    a.arms(8, (60, 0, 50), (40, 0, 0))
    for n in range(6):  # sp0..5 base rot is baked; animate offsets
        s = 1 if n % 2 == 0 else -1
        keys = [(0, 0, 0, 0), (2, -30, 0, 40 * s), (8, 10, 0, 0)]
        for i, t in enumerate((12, 16, 20, 24, 28)):
            hit = (i + n) % 3 == 0
            keys += [(t - 2, -30 if hit else 4, 0, -10 * s), (t, 70 if hit else 10, 0, 16 * s if hit else 0)]
        keys += [(32, -40, 0, -10 * s), (34, 80, 0, 24 * s), (38, 70, 0, 20 * s), (42, -20, 0, 30 * s), (46, 0, 0, 0)]
        a.rot(f"sp{n}", *keys)
        a.rot(f"sp{n}j", (0, 0, 0, 0), (8, 10, 0, 0), (12, -20, 0, 0), (16, 20, 0, 0), (20, -20, 0, 0), (24, 20, 0, 0), (28, -20, 0, 0),
              (32, -40, 0, 0), (34, 30, 0, 0), (40, 20, 0, 0), (46, 0, 0, 0))
    for i, t in enumerate((12, 16, 20, 24, 28)):
        j = 1 if i % 2 else -1
        a.at(t, body=(-24, 14 * j, 4 * j), head=(16, -10 * j, 0), jaw=(-24, 0, 0))
        a.arms(t, (90 + 10 * j, 30 * j, 10), (10, 0, 0), (0, 0, 0), al=(90 - 10 * j, 30 * j, -10))
    a.at(32, body=(6, 0, 0), head=(30, 0, 0), jaw=(-40, 0, 0))
    a.arms(32, (150, 0, 50), (20, 0, 0))
    a.at(34, body=(-50, 0, 0), head=(14, 0, 0), jaw=(-14, 0, 0))
    a.arms(34, (80, 0, 10), (0, 0, 0), (20, 0, 0))
    a.legs(12, 30, 50).legs(28, 30, 50).legs(32, 10, 16, up=0.5).legs(34, 60, 110, fwd=-1.5).legs(40, 50, 90).legs(44, 16, 24)
    a.at(40, body=(-40, 0, 0), head=(16, 0, 0))
    a.claws(4, -20, spread=8).claws(12, 20).claws(32, -20, spread=8).claws(34, 40).claws(44, 0)
    a.sec([(0, 0, 0), (4, -4, 0), (8, -6, 0), (12, 4, 3), (16, 4, -3), (20, 4, 3), (24, 4, -3), (28, 4, 3), (32, -8, 0), (34, 12, 0), (46, 0, 0)])
    a.done()

    # ================= hook (40): left arm becomes a hooked chain 1-6, whirl 6-9, THROW 10 (reach 12), catch 12, YANK 14-20, right slash 22
    a = mk("hook", 40)
    a.hide("claws_l", 1, 36)
    a.scl("hook_l", (0, *HIDE), (0.99, *HIDE), (6, 1, 1, 1), (9, 1, 1, 1), (11, 1, 3.2, 1), (13, 1, 3.4, 1), (16, 1, 2.2, 1), (20, 1, 1.0, 1),
          (34, 1, 1, 1), (36, *HIDE), (40, *HIDE))
    a.rot("hand_l", (0, *m3((4, 0, 0))), (5, 0, 0, 0), (6, 0, 200, 0), (7, 0, 400, 0), (8, 0, 600, 0), (9, 0, 720, 0), (40, 0, 720, 0))
    a.at(5, body=(-6, 20, 0), head=(10, -14, 0), jaw=(-10, 0, 0))
    a.arm(5, "l", (150, 0, 0), (20, 0, 0)).arm(5, "r", (20, 0, 20), (30, 0, 0))
    a.at(9, body=(6, 30, 4), head=(16, -20, 0))
    a.arm(9, "l", (190, 10, 0), (30, 0, 0))
    a.at(11, body=(-24, -20, -4), head=(4, 10, 0), jaw=(-30, 0, 0))
    a.arm(11, "l", (94, 0, 0), (0, 0, 0))
    a.arm(13, "l", (92, 0, 0), (0, 0, 0))
    a.at(14, body=(8, 30, 6), head=(16, -16, 0), jaw=(-20, 0, 0))
    a.arm(14, "l", (40, 20, 10), (60, 0, 0))
    a.arm(18, "l", (10, 0, 20), (80, 0, 0))
    a.at(20, body=(4, -36, -4), head=(14, 24, 0), jaw=(-10, 0, 0))
    a.arm(20, "r", (110, -90, 30), (20, 0, 0)).arm(20, "l", (30, 0, -20), (60, 0, 0))
    a.at(22, body=(-30, 40, 6), head=(6, -24, 0), jaw=(-30, 0, 0))
    a.arm(22, "r", (96, 76, 0), (0, 0, 0)).arm(24, "r", (86, 90, 0), (10, 0, 0))
    a.at(28, body=(-20, 20, 0), head=(10, -10, 0))
    a.arm(30, "r", (30, 20, 10), (20, 0, 0)).arm(34, "l", (10, 0, -10), (10, 0, 0))
    a.wave("hk", 8, [(0, 0, 0), (6, 0, 40), (9, 0, 60), (11, 10, 0), (13, 4, 0), (16, -30, 0), (20, -20, 10), (26, 10, 0), (40, 0, 0)], 0.5)
    a.legs(9, 0, 10, 30, 50).legs(11, 40, 70, -10, 10, fwd=-1).legs(14, 10, 20, 40, 70, fwd=1).legs(22, 44, 80, 10, 20, fwd=-1).legs(30, 14, 20)
    a.claws(20, -20, "r", 8).claws(22, 30, "r").claws(30, 0, "r")
    a.sec([(0, 0, 0), (9, -4, 2), (11, 8, -2), (14, -6, 3), (20, -2, -4), (22, 8, 5), (28, 2, 0), (40, 0, 0)])
    a.done()

    # ================= maw (44): right arm opens into a fanged maw 1-7, LUNGE BITE 10 (grab), chomp 18 / 26 / 34, fling 38
    a = mk("maw", 44)
    a.morph("maw_r", 1, 41, "r", grow=6)
    jaw = [(0, 0, 0, 0), (6, 0, 0, 0), (9, 70, 0, 0), (10, 0, 0, 0)]
    for t in (18, 26, 34):
        jaw += [(t - 4, 60, 0, 0), (t, -4, 0, 0), (t + 2, 6, 0, 0)]
    jaw += [(37, 50, 0, 0), (39, 70, 0, 0), (42, 0, 0, 0), (44, 0, 0, 0)]
    a.rot("mawj_r", *jaw)
    a.at(6, body=(-14, -20, 0), head=(14, 12, 0), jaw=(-20, 0, 0))
    a.arm(6, "r", (50, -20, 30), (60, 0, 0)).arm(6, "l", (20, 0, -20), (20, 0, 0))
    a.at(9, body=(-4, -24, 0), head=(20, 16, 0), jaw=(-30, 0, 0))
    a.arm(9, "r", (120, -10, 20), (40, 0, 0))
    a.at(10, body=(-36, 14, 4), head=(4, -6, 0), jaw=(-40, 0, 0))
    a.arm(10, "r", (90, 10, 0), (0, 0, 0), (0, 0, 0))
    a.legs(9, 10, 20, 40, 70).legs(10, 50, 90, -10, 10, fwd=-2)
    for t in (18, 26, 34):
        a.at(t - 4, body=(-20, -6, 0), head=(14, 4, 0), jaw=(-30, 0, 0)).arm(t - 4, "r", (120, -6, 10), (20, 0, 0))
        a.at(t, body=(-34, 6, 2), head=(6, -4, 0), jaw=(-10, 0, 0)).arm(t, "r", (70, 6, 0), (0, 0, 0))
    a.at(37, body=(-10, -30, -4), head=(16, 20, 0), jaw=(-30, 0, 0))
    a.arm(37, "r", (110, -60, 30), (20, 0, 0))
    a.at(39, body=(-26, 40, 6), head=(8, -20, 0), jaw=(-40, 0, 0))
    a.arm(39, "r", (80, 90, 20), (0, 0, 0))
    a.legs(20, 40, 70).legs(36, 30, 50).legs(42, 10, 16)
    a.sec([(0, 0, 0), (9, -4, 0), (10, 10, 2), (14, 0, 0), (18, 6, 0), (22, 0, 0), (26, 6, 0), (30, 0, 0), (34, 6, 0), (37, -2, -4), (39, 6, 5), (44, 0, 0)])
    a.done()

    # ================= pounce (30): drop into a crouch 0-7, LEAP 8, claws-first in the air 10-13, LAND rake 15, absorb, rise
    a = mk("pounce", 30)
    a.legs(4, 70, 130, fwd=1.0).legs(7, 76, 140, fwd=1.4).legs(8, -10, 10, up=3, fwd=-1).legs(11, -30, 60, up=6, fwd=-2) \
        .legs(13, 20, 70, up=3, fwd=-2).legs(15, 74, 132, fwd=-1).legs(19, 78, 136).legs(25, 30, 50)
    a.at(4, body=(-50, 0, 0), head=(44, 0, 0), jaw=(-10, 0, 0))
    a.rot("pelvis", (3, 0, 7, 0), (5, 0, -7, 0), (7, 0, 0, 0), (30, 0, 0, 0))
    a.at(7, body=(-56, 0, 0), head=(50, 0, 0), jaw=(-16, 0, 0))
    a.at(8, body=(-66, 0, 0), head=(58, 0, 0), jaw=(-30, 0, 0))
    a.at(11, body=(-76, 0, 0), head=(62, 0, 0), jaw=(-40, 0, 0))
    a.at(13, body=(-62, 0, 0), head=(48, 0, 0), jaw=(-30, 0, 0))
    a.at(15, body=(-56, 0, 0), head=(32, 0, 0), jaw=(-4, 0, 0))
    a.at(19, body=(-50, 0, 0), head=(30, 0, 0), jaw=(-8, 0, 0))
    a.at(25, body=(-20, 0, 0), head=(14, 0, 0))
    a.arms(4, (-30, 0, 24), (30, 0, 0), (20, 0, 0)).arms(7, (-40, 0, 26), (34, 0, 0), (24, 0, 0))
    a.arms(8, (150, 0, 18), (0, 0, 0), (-10, 0, 0)).arms(11, (172, 0, 24), (-6, 0, 0), (-16, 0, 0))
    a.arms(13, (150, 0, 18), (6, 0, 0), (10, 0, 0)).arms(15, (60, 0, 12), (20, 0, 0), (30, 0, 0))
    a.arms(19, (56, 0, 14), (24, 0, 0), (20, 0, 0)).arms(25, (20, 0, 10), (14, 0, 0), (6, 0, 0))
    a.claws(4, 30).claws(8, -24, spread=8).claws(13, -20, spread=8).claws(15, 45).claws(20, 30).claws(30, 0)
    a.sec([(0, 0, 0), (5, -3, 0), (8, 10, 0), (12, 4, 0), (15, -8, 0), (20, 3, 0), (30, 0, 0)])
    a.done()


def monster_abilities(mk):
    # ================= m_frenzy (48): six savage alternating slashes 10..35 (each lunging), crossing finisher 42
    a = mk("m_frenzy", 48)
    a.at(4, body=(-50, 0, 0), head=(46, 0, 0), jaw=(-40, 0, 0))
    a.arms(4, (-30, 0, 40), (40, 0, 0), (10, 0, 0))
    a.legs(4, 50, 90)
    for i in range(6):
        t = 10 + 5 * i
        s = "r" if i % 2 == 0 else "l"
        o = "l" if s == "r" else "r"
        j = 1 if s == "r" else -1
        a.at(t - 3, body=(-30, -30 * j, -6 * j), head=(30, 20 * j, 0), jaw=(-30, 0, 0))
        a.arm(t - 3, s, (140, -70, 40), (20, 0, 0), (0, 0, 0))
        a.at(t, body=(-46, 34 * j, 8 * j), head=(28, -20 * j, 0), jaw=(-50, 0, 0))
        a.arm(t, s, (90, 80, 0), (0, 0, 0), (10, 0, 0)).arm(t, o, (60, 0, 20), (40, 0, 0))
        a.legs(t, 40 if s == "r" else 20, 70 if s == "r" else 40, 20 if s == "r" else 40, 40 if s == "r" else 70, fwd=-1)
    a.at(39, body=(-10, 0, 0), head=(50, 0, 0), jaw=(-56, 0, 0))
    a.arms(39, (200, 0, 30), (20, 0, 0), (-20, 0, 0))
    a.legs(39, 20, 30, up=0.5)
    a.at(42, body=(-66, 0, 0), head=(30, 0, 0), jaw=(-30, 0, 0))
    a.arms(42, (80, 40, -10), (0, 0, 0), (20, 0, 0), al=(80, 40, 10))
    a.legs(42, 70, 120, fwd=-2)
    a.at(46, body=(-46, 0, 0), head=(34, 0, 0), jaw=(-16, 0, 0))
    a.arms(46, (40, 0, 20), (14, 0, 0))
    a.claws(4, -26, spread=12).claws(10, 30).claws(20, 30).claws(39, -26, spread=12).claws(42, 40).claws(48, 0, spread=6)
    a.stretch(3, 46)
    a.sec([(0, 0, 0), (4, -4, 0), (10, 6, 4), (15, 6, -4), (20, 6, 4), (25, 6, -4), (30, 6, 4), (35, 6, -4), (39, -6, 0), (42, 12, 0), (48, 0, 0)])
    a.done()

    # ================= m_impale (40): rears up 0-12, both claws plunge into the ground 14, rip forward 16-31 (spike line), wrench out
    a = mk("m_impale", 40)
    a.at(6, body=(-6, 0, 0), head=(46, 0, 0), jaw=(-46, 0, 0))
    a.arms(6, (186, 0, 20), (10, 0, 0), (-20, 0, 0))
    a.legs(6, 20, 30, up=0.6)
    a.at(11, body=(6, 0, 0), head=(54, 0, 0), jaw=(-56, 0, 0))
    a.arms(11, (212, 0, 26), (20, 0, 0), (-26, 0, 0))
    a.legs(11, 14, 20, up=1.0)
    a.at(14, body=(-72, 0, 0), head=(40, 0, 0), jaw=(-24, 0, 0))
    a.arms(14, (66, 0, 14), (0, 0, 0), (40, 0, 0))
    a.legs(14, 70, 124)
    for i, t in enumerate(range(16, 32, 3)):
        j = 1 if i % 2 else -1
        a.at(t, body=(-70 + 2 * j, 3 * j, 2 * j), head=(42, -4 * j, 0), jaw=(-30 - 6 * (i % 2), 0, 0))
        a.arms(t, (70 + 6 * j, 0, 14), (0, 0, 0), (36, 0, 0), al=(70 - 6 * j, 0, 14))
        a.legs(t, 68, 120)
    a.at(34, body=(-30, 0, 0), head=(36, 0, 0), jaw=(-10, 0, 0))
    a.arms(34, (124, 0, 24), (20, 0, 0), (-10, 0, 0))
    a.legs(34, 40, 70)
    a.claws(6, -26, spread=12).claws(12, -26, spread=12).claws(14, 46).claws(31, 46).claws(34, -10).claws(38, 0, spread=6)
    a.stretch(4, 38, 1.5)
    a.sec([(0, 0, 0), (6, -4, 0), (11, -8, 0), (14, 12, 0), (17, 8, 3), (23, 8, -3), (29, 8, 3), (34, -2, 0), (40, 0, 0)])
    a.done()

    # ================= m_lunge (32): coils low 0-8, LAUNCHES 9 (all limbs forward), mauls 10-20, skids to a stop 22
    a = mk("m_lunge", 32)
    a.at(4, body=(-60, 0, 0), head=(56, 0, 0), jaw=(-20, 0, 0))
    a.arms(4, (10, 0, 30), (30, 0, 0), (20, 0, 0))
    a.legs(4, 76, 136, fwd=1.2)
    a.at(8, body=(-66, 0, 0), head=(62, 0, 0), jaw=(-50, 0, 0))
    a.arms(8, (-10, 0, 34), (40, 0, 0))
    a.legs(8, 80, 140, fwd=1.4)
    a.at(9, body=(-80, 0, 0), head=(70, 0, 0), jaw=(-60, 0, 0))
    a.arms(9, (170, 0, 16), (0, 0, 0), (-10, 0, 0))
    a.legs(9, -30, 10, up=2)
    for i, t in enumerate((12, 15, 18)):
        j = 1 if i % 2 else -1
        a.at(t, body=(-76, 6 * j, 4 * j), head=(66, -6 * j, 0), jaw=(-50 + 30 * (i % 2), 0, 0))
        a.arms(t, (120 + 30 * j, 0, 16), (0, 0, 0), (10, 0, 0), al=(120 - 30 * j, 0, 16))
        a.legs(t, -10 if j > 0 else 40, 30, 40 if j > 0 else -10, 30, up=1.5)
    a.at(22, body=(-50, 0, 0), head=(40, 0, 0), jaw=(-20, 0, 0))
    a.arms(22, (90, 0, 30), (10, 0, 0), (30, 0, 0))
    a.legs(22, 20, 50, fwd=1.5)
    a.at(27, body=(-40, 0, 0), head=(36, 0, 0), jaw=(-12, 0, 0))
    a.arms(27, (40, 0, 20), (14, 0, 0))
    a.legs(27, 40, 70)
    a.claws(8, 30).claws(9, -26, spread=12).claws(12, 40).claws(15, -10).claws(18, 40).claws(26, 0, spread=6)
    a.stretch(5, 28)
    a.sec([(0, 0, 0), (4, 4, 0), (8, 6, 0), (9, 14, 0), (12, 12, 3), (15, 12, -3), (18, 12, 3), (22, -6, 0), (27, 2, 0), (32, 0, 0)])
    a.done()

    # ================= m_tendrils (50): hunch + shudder 0-12, ERUPTION 14 (extra arms + ground tendrils), thrash 16-30, recoil
    a = mk("m_tendrils", 50)
    a.scl("spider", (0, *HIDE), (11.99, *HIDE), (14, 1.6, 1.6, 1.6), (16, 1.4, 1.4, 1.4), (44, 1.4, 1.4, 1.4), (46, *HIDE), (50, *HIDE))
    for t, j in ((3, 1), (6, -1), (9, 1), (12, -1)):
        a.at(t, body=(-70 + 2 * j, 4 * j, 4 * j), head=(20, 6 * j, 0), jaw=(-6, 0, 0))
        a.arms(t, (40, 40, -20), (100, 0, 0), (20, 0, 0))
        a.legs(t, 56, 100)
    a.at(14, body=(10, 0, 0), head=(56, 0, 0), jaw=(-60, 0, 0))
    a.arms(14, (-10, 0, 110), (10, 0, 0), (-30, 0, 0))
    a.legs(14, 16, 24, up=0.6)
    for n in range(6):
        s = 1 if n % 2 == 0 else -1
        keys = [(0, 0, 0, 0), (12, 0, 0, 0), (14, -20, 0, 50 * s)]
        for i, t in enumerate(range(17, 31, 3)):
            keys.append((t, (25 if (i + n) % 2 else -25), 0, (20 if (i + n) % 2 else 60) * s))
        keys += [(36, 20, 0, 30 * s), (44, 0, 0, 10 * s), (50, 0, 0, 0)]
        a.rot(f"sp{n}", *keys)
    for t, j in ((18, 1), (22, -1), (26, 1), (30, -1)):
        a.at(t, body=(6 + 2 * j, 8 * j, 4 * j), head=(52, -8 * j, 4 * j), jaw=(-54, 0, 0))
        a.arms(t, (0, 0, 100 + 10 * j), (14, 0, 0), (-24, 0, 0), al=(0, 0, 100 - 10 * j))
    a.at(36, body=(-40, 0, 0), head=(36, 0, 0), jaw=(-30, 0, 0))
    a.arms(36, (40, 0, 30), (20, 0, 0))
    a.legs(36, 40, 70)
    a.claws(3, 40).claws(14, -30, spread=14).claws(30, -26, spread=14).claws(38, 0, spread=6)
    a.stretch(10, 42)
    a.sec([(0, 0, 0), (3, 6, 3), (6, 6, -3), (9, 6, 3), (12, 6, -3), (14, -12, 0), (18, -6, 5), (22, -6, -5), (26, -6, 5), (30, -6, -5), (36, 4, 0), (50, 0, 0)])
    a.done()

    # ================= m_reap (36): black scythes, crouch-twist 0-9, SPIN 10-14 (hit 12), second SPIN 18-22 (hit 20), unwind
    a = mk("m_reap", 36)
    a.morph("scythe_r", 1, 33, "r").morph("scythe_l", 1, 33, "l")
    a.rot("root", (0, 0, 0, 0), (8, 0, -30, 0), (10, 0, 30, 0), (12, 0, 190, 0), (14, 0, 330, 0), (16, 0, 360, 0),
          (18, 0, 400, 0), (20, 0, 550, 0), (22, 0, 690, 0), (25, 0, 726, 0), (30, 0, 720, 0), (36, 0, 720, 0))
    a.at(8, body=(-50, -30, 0), head=(40, 30, 0), jaw=(-30, 0, 0))
    a.arms(8, (60, 0, 60), (30, 0, 0), (0, 0, 0))
    a.legs(8, 60, 110)
    for t in (12, 20):
        a.at(t, body=(-36, 0, 0), head=(34, 0, 0), jaw=(-50, 0, 0))
        a.arms(t, (90, 0, 92), (0, 0, 0), (0, 0, 0))
        a.legs(t, 30, 50, up=0.5)
    a.at(16, body=(-46, 0, 0), head=(38, 0, 0), jaw=(-30, 0, 0))
    a.arms(16, (70, 0, 70), (20, 0, 0))
    a.legs(16, 50, 90)
    a.at(26, body=(-50, 0, 0), head=(40, 0, 0), jaw=(-20, 0, 0))
    a.arms(26, (50, 0, 40), (20, 0, 0))
    a.legs(26, 46, 80)
    a.claws(8, 20).claws(12, -10, spread=10).claws(26, 0)
    a.sec([(0, 0, 0), (8, 4, -4), (10, 2, 10), (12, 4, 16), (14, 4, 16), (16, 4, 6), (18, 4, 10), (20, 4, 16), (22, 4, 16), (26, 2, 0), (36, 0, 0)])
    a.done()


def shift_abilities(mk):
    # ================= drill (36): right arm twists into a drill 1-6, cock back 6-9, THRUST 10 (dash), grind 12-22, BURST 24, pull out
    a = mk("drill", 36)
    a.morph("drill_r", 1, 33, "r", grow=5)
    a.spin("drillspin", [(0, 0), (3, 0), (9, 300), (24, 2700), (30, 3060), (36, 3240)])
    a.at(3, body=(-8, -10, 0), head=(10, 8, 0), jaw=(-10, 0, 0))
    a.arm(3, "r", (30, 0, 20), (30, 0, 0)).arm(3, "l", (20, 0, -10), (20, 0, 0))
    a.at(8, body=(-14, -38, -4), head=(12, 30, 0), jaw=(-24, 0, 0))
    a.arm(8, "r", (-30, -10, 30), (100, 0, 0), (0, 0, 0)).arm(8, "l", (60, 20, -20), (40, 0, 0))
    a.legs(3, 16, 26).legs(8, -10, 20, 50, 90, fwd=0.5)
    a.at(10, body=(-34, 24, 6), head=(4, -16, 0), jaw=(-40, 0, 0))
    a.arm(10, "r", (94, 6, 0), (-4, 0, 0), (0, 0, 0)).arm(10, "l", (-30, 0, -30), (30, 0, 0))
    a.legs(10, 64, 104, -24, 10, fwd=-2.5)
    for i, t in enumerate(range(12, 23, 2)):
        j = 1 if i % 2 else -1
        a.at(t, body=(-34 + 2 * j, 24 + 2 * j, 6), head=(4 + 3 * j, -16, 2 * j), jaw=(-44 - 4 * j, 0, 0))
        a.arm(t, "r", (92 + 2 * j, 6, 2 * j), (0, 0, 0), (0, 0, 0))
        a.legs(t, 62, 102, -22, 12, fwd=-2.5)
    a.at(24, body=(-42, 22, 8), head=(2, -14, 0), jaw=(-56, 0, 0))
    a.arm(24, "r", (98, 4, 0), (-8, 0, 0), (0, 0, 0))
    a.legs(24, 70, 112, -28, 10, fwd=-3)
    a.at(28, body=(-18, 6, 0), head=(12, -4, 0), jaw=(-20, 0, 0))
    a.arm(28, "r", (50, -10, 20), (40, 0, 0)).arm(28, "l", (10, 0, -20), (20, 0, 0))
    a.legs(28, 30, 50).legs(33, 12, 18)
    a.at(33, body=(-8, 0, 0), head=(8, 0, 0))
    a.arm(33, "r", (14, 0, 10), (16, 0, 0))
    a.claws(8, 30, "l").claws(10, -20, "l", 10).claws(28, 0, "l")
    a.sec([(0, 0, 0), (8, -4, -3), (10, 12, 3), (14, 7, 1), (18, 7, -1), (22, 7, 1), (24, 12, 3), (28, -3, 0), (36, 0, 0)])
    a.done()

    # ================= crusher (40): both arms become crushing claws 1-6, spread open 10, CLAMP 12 (grab), lift 16,
    #                   CRUSH 20 (squeeze), heave 24, SLAM 28, release
    a = mk("crusher", 40)
    a.morph("pincer_r", 1, 37, "r", grow=5).morph("pincer_l", 1, 37, "l", grow=5)
    for k in ("r", "l"):
        for jn, sg in (("A", 1), ("B", -1)):
            a.rot(f"pin{jn}_{k}", *[(t, v * sg, 0, 0) for t, v in ((0, 0), (6, 10), (10, 44), (11.5, 48), (12, -6), (14, 2), (19, 4), (20, -10),
                                                                   (21, 4), (27, 0), (29, 30), (33, 36), (37, 0), (40, 0))])
    a.at(5, body=(-6, 0, 0), head=(18, 0, 0), jaw=(-30, 0, 0))
    a.arms(5, (60, 0, 40), (30, 0, 0), (0, 0, 0))
    a.at(10, body=(-20, 0, 0), head=(12, 0, 0), jaw=(-46, 0, 0))
    a.arms(10, (100, -50, 30), (10, 0, 0), (0, 0, 0))
    a.legs(5, 20, 30).legs(10, 40, 70)
    a.at(12, body=(-34, 0, 0), head=(4, 0, 0), jaw=(-10, 0, 0))
    a.arms(12, (92, 14, -4), (0, 0, 0), (0, 0, 0))
    a.legs(12, 34, 56, fwd=-1.5)
    a.at(16, body=(4, 0, 0), head=(30, 0, 0), jaw=(-36, 0, 0))
    a.arms(16, (150, 10, 0), (10, 0, 0), (0, 0, 0))
    a.legs(16, 6, 10, up=0.4)
    a.at(19, body=(6, 0, 0), head=(32, 0, 0), jaw=(-40, 0, 0)).arms(19, (160, 10, 0), (8, 0, 0))
    a.at(20, body=(9, 0, 3), head=(34, 0, 0), jaw=(-54, 0, 0)).arms(20, (156, 13, -3), (4, 0, 0))
    a.at(22, body=(8, 0, -3), head=(34, 0, 0)).arms(22, (164, 9, 2), (8, 0, 0))
    a.at(25, body=(14, 0, 0), head=(36, 0, 0), jaw=(-30, 0, 0)).arms(25, (178, 8, 0), (16, 0, 0))
    a.legs(25, 0, 10, up=0.8)
    a.at(28, body=(-56, 0, 0), head=(10, 0, 0), jaw=(-24, 0, 0))
    a.arms(28, (62, 10, 0), (0, 0, 0), (20, 0, 0))
    a.legs(28, 70, 120, fwd=-2)
    a.at(31, body=(-52, 0, 0), head=(14, 0, 0)).arms(31, (58, 10, 0), (4, 0, 0))
    a.legs(31, 66, 116, fwd=-2)
    a.at(36, body=(-14, 0, 0), head=(10, 0, 0), jaw=(-6, 0, 0)).arms(36, (20, 0, 14), (20, 0, 0))
    a.legs(36, 14, 20)
    a.sec([(0, 0, 0), (5, -2, 0), (10, 4, 0), (12, 8, 0), (16, -6, 0), (20, -6, 3), (22, -6, -3), (25, -8, 0), (28, 14, 0), (32, 4, 0), (40, 0, 0)])
    a.done()

    # ================= lattice (38): fingers spin out razor wire 1-11, arms cross 9, RIP OPEN 13 (horizontal lattice),
    #                   overhead 18, DOWN-CUT 22, cinch / YANK 28 (pulls victims in), retract
    a = mk("lattice", 38)
    a.morph("wire_r", 1, 35, "r", grow=4).morph("wire_l", 1, 35, "l", grow=4)
    for k in ("r", "l"):
        for i in range(5):
            a.scl(f"wr{i}_{k}", (0, 1, 0.3, 1), (5, 1, 0.5, 1), (11, 1, 2.3, 1), (30, 1, 2.3, 1), (35, 1, 0.5, 1), (38, 1, 0.5, 1))
            sp = (i - 2) * 6
            a.rot(f"wr{i}_{k}", (0, 0, 0, 0), (9, 0, 0, sp * 0.5), (12, -20, 0, sp), (14, 30, 0, sp * 1.6), (17, 10, 0, sp), (20, -30, 0, sp * 0.6),
                  (22, 20, 0, sp), (24, 30, 0, sp * 1.4), (28, -40, 0, sp * 0.4), (31, -10, 0, sp * 0.2), (38, 0, 0, 0))
    a.at(4, body=(-4, 0, 0), head=(14, 0, 0), jaw=(-14, 0, 0))
    a.arms(4, (40, 0, 20), (40, 0, 0))
    a.at(9, body=(-16, 0, 0), head=(6, 0, 0), jaw=(-8, 0, 0))
    a.arms(9, (100, 70, 10), (30, 0, 0), (0, 0, 0))
    a.at(11, body=(-18, 0, 0)).arms(11, (104, 78, 8), (34, 0, 0))
    a.legs(9, 36, 64)
    a.at(13, body=(-6, 0, 0), head=(20, 0, 0), jaw=(-50, 0, 0))
    a.arms(13, (92, -86, 0), (0, 0, 0), (0, 0, 0))
    a.legs(13, 20, 30, up=0.3)
    a.at(15, body=(-4, 0, 0)).arms(15, (90, -98, 0), (-4, 0, 0))
    a.at(18, body=(8, 0, 0), head=(30, 0, 0), jaw=(-30, 0, 0))
    a.arms(18, (176, -10, 20), (10, 0, 0))
    a.legs(18, 10, 16, up=0.4)
    a.at(22, body=(-40, 0, 0), head=(10, 0, 0), jaw=(-44, 0, 0))
    a.arms(22, (50, -8, 8), (0, 0, 0), (0, 0, 0))
    a.legs(22, 50, 90, fwd=-1.5)
    a.at(24, body=(-38, 0, 0)).arms(24, (44, -8, 8), (0, 0, 0))
    a.at(26, body=(-20, 0, 0), head=(14, 0, 0), jaw=(-20, 0, 0)).arms(26, (80, -30, 20), (10, 0, 0))
    a.at(28, body=(10, 0, 0), head=(26, 0, 0), jaw=(-40, 0, 0))
    a.arms(28, (30, 30, 30), (110, 0, 0), (0, 0, 0))
    a.legs(26, 30, 50).legs(28, -6, 10, 30, 50)
    a.at(31, body=(8, 0, 0)).arms(31, (26, 30, 30), (120, 0, 0))
    a.at(35, body=(-6, 0, 0), head=(8, 0, 0), jaw=(0, 0, 0)).arms(35, (10, 0, 10), (20, 0, 0))
    a.legs(35, 10, 16)
    a.claws(9, -10, spread=24).claws(13, -24, spread=30).claws(22, -24, spread=30).claws(28, 40).claws(34, 0)
    a.sec([(0, 0, 0), (9, 3, 0), (13, -4, 0), (15, -4, 0), (18, -6, 0), (22, 10, 0), (26, 2, 0), (28, -8, 0), (38, 0, 0)])
    a.done()

    # ================= kusari (44): whip arm + sickle (kusarigama) - whirl overhead 6-12, SWEEP 14, BACKHAND 22, overhead CHOP 30, YANK 34
    a = mk("kusari", 44)
    a.hide("claws_r", 1, 41)
    a.scl("whip_r", (0, *HIDE), (0.99, *HIDE), (5, 1, 1, 1), (9, 1, 1.2, 1), (13, 1, 1.6, 1), (30, 1, 1.7, 1), (34, 1, 1.3, 1), (38, 1, 1, 1),
          (40, *HIDE), (44, *HIDE))
    a.show("kama", 4, 41, grow=3)
    a.spin("hand_r", [(0, 0), (6, 0), (12, 1080), (44, 1080)], base=(4, 0, 0))
    a.at(3, body=(-6, -14, 0), head=(12, 8, 0))
    a.arm(3, "r", (60, 0, 30), (40, 0, 0)).arm(3, "l", (20, 0, -20), (20, 0, 0))
    a.at(7, body=(4, -10, -4), head=(22, 6, 0), jaw=(-20, 0, 0))
    a.arm(7, "r", (176, 0, 12), (10, 0, 0)).arm(7, "l", (30, 0, -30), (40, 0, 0))
    a.at(12, body=(2, 10, 4), head=(20, -6, 0)).arm(12, "r", (172, 0, 14), (10, 0, 0))
    a.legs(7, 10, 16, up=0.3)
    a.at(13, body=(-10, -30, -4), head=(12, 20, 0), jaw=(-30, 0, 0)).arm(13, "r", (110, -80, 20), (0, 0, 0))
    a.at(15, body=(-26, 30, 6), head=(6, -20, 0), jaw=(-44, 0, 0)).arm(15, "r", (90, 40, 0), (0, 0, 0))
    a.at(17, body=(-24, 44, 6), head=(8, -26, 0)).arm(17, "r", (86, 90, 0), (0, 0, 0))
    a.legs(13, 0, 10, 30, 50).legs(15, 40, 70, -6, 10, fwd=-1)
    a.at(20, body=(-20, 40, 4), head=(12, -26, 0), jaw=(-20, 0, 0)).arm(20, "r", (96, 96, 10), (30, 0, 0))
    a.at(22, body=(-24, -30, -6), head=(8, 20, 0), jaw=(-44, 0, 0)).arm(22, "r", (90, -20, 0), (0, 0, 0))
    a.at(24, body=(-22, -44, -6), head=(10, 26, 0)).arm(24, "r", (88, -90, 0), (0, 0, 0))
    a.legs(20, 30, 50, 10, 20).legs(22, -6, 10, 40, 70, fwd=-1)
    a.at(27, body=(12, -10, 0), head=(30, 6, 0), jaw=(-30, 0, 0)).arm(27, "r", (200, -10, 10), (20, 0, 0))
    a.legs(27, 10, 16, up=0.4)
    a.at(30, body=(-44, 0, 0), head=(8, 0, 0), jaw=(-40, 0, 0)).arm(30, "r", (70, 0, 4), (0, 0, 0))
    a.arm(30, "l", (-20, 0, -40), (30, 0, 0))
    a.legs(30, 50, 90, fwd=-1.6)
    a.at(34, body=(-6, -14, 0), head=(20, 10, 0), jaw=(-24, 0, 0)).arm(34, "r", (20, 0, 30), (100, 0, 0))
    a.legs(34, -4, 10, 30, 56)
    a.at(40, body=(-6, 0, 0), head=(8, 0, 0), jaw=(0, 0, 0)).arm(40, "r", (16, 0, 10), (16, 0, 0)).arm(40, "l", (10, 0, -10), (10, 0, 0))
    a.legs(40, 10, 16)
    a.wave("wh", 10, [(0, 0, 0), (5, -10, 10), (7, -20, 50), (12, -20, 50), (13, 0, 30), (14, 10, -10), (16, 0, -30), (18, 0, -20), (20, 0, 30),
                      (22, 0, 10), (24, 0, -30), (27, -30, 0), (29, -40, 0), (30, 10, 0), (32, 20, 0), (34, -30, 0), (37, -10, 0), (44, 0, 0)], 0.5)
    a.sec([(0, 0, 0), (7, -4, 0), (12, -4, 2), (14, 6, 5), (17, 4, 6), (22, 6, -5), (24, 4, -6), (27, -6, 0), (30, 12, 0), (34, -4, 0), (44, 0, 0)])
    a.done()

    # ================= grapple (40): right arm grows a grappling hook 2-6, wind 7, THROW 9, anchor 10, REEL herself in 11-18,
    #                   left-claw RAKE on arrival 20, land 24
    a = mk("grapple", 40)
    a.show("grapnel_r", 2, 37, grow=3).hide("claws_r", 2, 37)
    a.scl("grchain", (0, 1, 1, 1), (8, 1, 1, 1), (10, 1, 5, 1), (12, 1, 5.2, 1), (13, 1, 5, 1), (19, 1, 0.8, 1), (21, 1, 1, 1), (40, 1, 1, 1))
    a.scl("grhead", (0, 1, 1, 1), (8, 1, 1, 1), (10, 1, 0.2, 1), (12, 1, 0.19, 1), (13, 1, 0.2, 1), (19, 1, 1.25, 1), (21, 1, 1, 1), (40, 1, 1, 1))
    a.at(3, body=(-8, -20, 0), head=(12, 14, 0), jaw=(-10, 0, 0))
    a.arm(3, "r", (40, -20, 30), (50, 0, 0))
    a.at(7, body=(-4, -40, -6), head=(14, 34, 0), jaw=(-16, 0, 0))
    a.arm(7, "r", (-40, -10, 30), (90, 0, 0), (0, 0, 0)).arm(7, "l", (60, 10, -20), (20, 0, 0))
    a.legs(7, 0, 10, 40, 70)
    a.at(9, body=(-26, 16, 4), head=(6, -10, 0), jaw=(-34, 0, 0))
    a.arm(9, "r", (96, 4, 0), (0, 0, 0), (0, 0, 0)).arm(9, "l", (-20, 0, -30), (20, 0, 0))
    a.legs(9, 40, 70, -10, 10, fwd=-1)
    a.at(11, body=(-40, 6, 0), head=(30, -4, 0), jaw=(-30, 0, 0)).arm(11, "r", (120, 0, 0), (0, 0, 0))
    a.legs(11, 20, 60, -10, 30, up=1.5)
    for t, j in ((13, 1), (16, -1)):
        a.at(t, body=(-64 + 2 * j, 0, 3 * j), head=(54, 0, 0), jaw=(-40, 0, 0))
        a.arm(t, "r", (158, 0, 0), (0, 0, 0)).arm(t, "l", (170, 0, -10), (10, 0, 0))
        a.legs(t, -10, 60, 10, 90, up=2.5)
    a.at(18, body=(-50, -10, 0), head=(44, 8, 0), jaw=(-50, 0, 0))
    a.arm(18, "r", (110, 0, 10), (30, 0, 0)).arm(18, "l", (210, 0, -20), (20, 0, 0))
    a.legs(18, 30, 90, 30, 90, up=2.0)
    a.at(20, body=(-40, 20, 4), head=(30, -10, 0), jaw=(-50, 0, 0))
    a.arm(20, "l", (80, 0, 0), (0, 0, 0), (20, 0, 0)).arm(20, "r", (60, 0, 30), (40, 0, 0))
    a.legs(20, 40, 80, 20, 60, up=1.0)
    a.at(24, body=(-44, 10, 0), head=(30, 0, 0), jaw=(-20, 0, 0))
    a.arm(24, "r", (60, 0, 20), (30, 0, 0)).arm(24, "l", (50, 0, -10), (20, 0, 0))
    a.legs(24, 66, 120)
    a.at(30, body=(-20, 0, 0), head=(16, 0, 0), jaw=(-8, 0, 0)).legs(30, 30, 50)
    a.at(36, body=(-8, 0, 0), head=(8, 0, 0)).arms(36, (10, 0, 10), (14, 0, 0)).legs(36, 12, 18)
    a.claws(16, -24, "l", 10).claws(20, 40, "l").claws(28, 0, "l")
    a.sec([(0, 0, 0), (7, -4, -2), (9, 8, 2), (11, 10, 0), (13, 16, 2), (16, 16, -2), (18, 6, 0), (20, 12, 3), (24, -8, 0), (30, 2, 0), (40, 0, 0)])
    a.done()

    # ================= wingrake (46): arms unfurl into mirrored blade-wings 1-8 (screech), crouch 11, LEAP 12, low glide 13-24
    #                   (wings slice everything), SPIN 26-30 (buzzsaw hit 28), land 32
    a = mk("wingrake", 46)
    a.morph("bwing_r", 1, 42, None, grow=6).morph("bwing_l", 1, 42, None, grow=6)
    a.at(5, body=(-6, 0, 0), head=(16, 0, 0), jaw=(-24, 0, 0)).arms(5, (10, 0, 60), (10, 0, 0), (0, 0, 0))
    a.at(8, body=(-4, 0, 0), head=(22, 0, 0), jaw=(-40, 0, 0)).arms(8, (0, 0, 94), (0, 0, 0))
    a.at(11, body=(-40, 0, 0), head=(36, 0, 0), jaw=(-10, 0, 0)).arms(11, (-20, 0, 80), (0, 0, 0))
    a.legs(8, 10, 16).legs(11, 70, 126, fwd=1)
    a.at(12, body=(-60, 0, 0), head=(50, 0, 0), jaw=(-30, 0, 0)).arms(12, (-10, 0, 96), (0, 0, 0))
    a.legs(12, -10, 10, up=3)
    for i, t in enumerate((14, 17, 20, 23)):
        j = 1 if i % 2 else -1
        a.at(t, body=(-76, 0, 8 * j), head=(64, 0, -4 * j), jaw=(-34, 0, 0))
        a.arms(t, (-4, 4 * j, 90 + 4 * j), (0, 0, 0), al=(-4, -4 * j, 90 - 4 * j))
        a.legs(t, -24, 20, up=4.5)
    a.at(25, body=(-76, 0, 0), head=(64, 0, 0), jaw=(-50, 0, 0)).arms(25, (-6, 0, 92), (0, 0, 0))
    a.spin("root", [(0, 0), (25, 0), (32, 360), (46, 360)])
    a.at(28, body=(-70, 0, 0), head=(58, 0, 0), jaw=(-56, 0, 0)).arms(28, (0, 0, 96), (0, 0, 0))
    a.legs(28, -10, 30, up=3)
    a.at(32, body=(-50, 0, 0), head=(30, 0, 0), jaw=(-14, 0, 0)).arms(32, (60, 0, 40), (10, 0, 0))
    a.legs(32, 70, 130)
    a.at(36, body=(-44, 0, 0), head=(28, 0, 0)).legs(36, 64, 120)
    a.at(42, body=(-14, 0, 0), head=(10, 0, 0), jaw=(0, 0, 0)).arms(42, (10, 0, 30), (10, 0, 0)).legs(42, 20, 30)
    a.claws(8, -20, spread=10).claws(30, -20, spread=10).claws(32, 30).claws(40, 0)
    a.sec([(0, 0, 0), (8, -2, 0), (11, 4, 0), (12, 10, 0), (14, 14, 3), (17, 14, -3), (20, 14, 3), (23, 14, -3), (26, 12, 14), (30, 12, 14),
           (32, -10, 0), (36, 4, 0), (46, 0, 0)])
    a.done()

    # ================= rootspikes (44): arms sprout root-tendrils 3-7, REAR up 9, PLUNGE into the ground 12, roots writhe 14-24
    #                   (spikes erupt under the target ~20), RIP them up 26 (ring of spikes around her), recover
    a = mk("rootspikes", 44)
    a.morph("roots_r", 3, 40, "r", grow=4).morph("roots_l", 3, 40, "l", grow=4)
    for k in ("r", "l"):
        a.scl("rootsg_" + k, (0, 1, 1, 1), (11, 1, 1, 1), (13, 1, 2.3, 1), (25, 1, 2.4, 1), (27, 1, 1.3, 1), (40, 1, 1, 1), (44, 1, 1, 1))
    a.at(4, body=(4, 0, 0), head=(30, 0, 0), jaw=(-40, 0, 0)).arms(4, (150, 0, 30), (20, 0, 0))
    a.at(9, body=(10, 0, 0), head=(36, 0, 0), jaw=(-56, 0, 0)).arms(9, (196, 0, 20), (10, 0, 0), (-10, 0, 0))
    a.legs(4, 10, 16).legs(9, 6, 10, up=0.6)
    a.at(12, body=(-70, 0, 0), head=(40, 0, 0), jaw=(-20, 0, 0)).arms(12, (70, 0, 12), (0, 0, 0), (10, 0, 0))
    a.legs(12, 70, 124, fwd=-1)
    for i, t in enumerate(range(14, 25, 2)):
        j = 1 if i % 2 else -1
        a.at(t, body=(-70 + 3 * j, 4 * j, 3 * j), head=(42 - 4 * j, -6 * j, 4 * j), jaw=(-24 - 10 * (i % 2), 0, 0))
        a.arms(t, (70 + 6 * j, 0, 12), (0, 0, 0), (10, 0, 0), al=(70 - 6 * j, 0, 12))
        a.legs(t, 70, 124, fwd=-1)
    a.at(26, body=(8, 0, 0), head=(40, 0, 0), jaw=(-60, 0, 0)).arms(26, (150, 0, 40), (20, 0, 0), (-20, 0, 0))
    a.legs(26, 10, 16, up=0.5)
    a.at(28, body=(10, 0, 0), head=(42, 0, 0)).arms(28, (160, 0, 50), (20, 0, 0))
    a.at(33, body=(-14, 0, 0), head=(16, 0, 0), jaw=(-14, 0, 0)).arms(33, (40, 0, 30), (20, 0, 0)).legs(33, 30, 50)
    a.at(40, body=(-6, 0, 0), head=(8, 0, 0), jaw=(0, 0, 0)).arms(40, (10, 0, 10), (10, 0, 0)).legs(40, 10, 16)
    a.sec([(0, 0, 0), (4, -6, 0), (9, -8, 0), (12, 14, 0), (16, 10, 3), (20, 10, -3), (24, 10, 3), (26, -10, 0), (30, -4, 0), (44, 0, 0)])
    a.done()

    # ================= barrage (44): eight ink arms burst from her back 2-8, rapid punches 10..30 (every 2 ticks),
    #                   all-arm FINISHER 34, retract
    a = mk("barrage", 44)
    a.show("barrage", 2, 41, grow=5)
    pk = {i: [] for i in range(8)}
    for j, t in enumerate(range(10, 31, 2)):
        pk[[0, 5, 2, 7, 4, 1, 6, 3][j % 8]].append(t)
    for i in range(8):
        keys, rk = [(0, 0, 0, 0), (8, 0, 0, 0)], [(0, 0, 0, 0), (2, 40, 0, 0), (8, 0, 0, 0)]
        for t in pk[i]:
            keys += [(t - 1.5, 0, 0, 2.0), (t, 0, -1.0, -9.0), (t + 1.5, 0, 0, 0)]
            rk += [(t, -14, 0, 0), (t + 1.5, 0, 0, 0)]
        keys += [(32, 0, 1.0, 3.0), (34, 0, -1.0, -11.0), (37, 0, -0.8, -10.0), (41, 0, 0, 0), (44, 0, 0, 0)]
        rk += [(32, 20, 0, 0), (34, -20, 0, 0), (38, -14, 0, 0), (41, 30, 0, 0), (44, 0, 0, 0)]
        a.pos(f"ba{i}e", *sorted(keys))
        a.rot(f"ba{i}", *sorted(rk))
    a.at(3, body=(-30, 0, 0), head=(30, 0, 0), jaw=(-50, 0, 0)).arms(3, (-20, 0, 40), (30, 0, 0))
    a.at(8, body=(-24, 0, 0), head=(24, 0, 0), jaw=(-30, 0, 0)).arms(8, (40, 0, 30), (70, 0, 0))
    a.legs(3, 30, 50).legs(8, 40, 70)
    for n, t in enumerate(range(10, 31, 2)):
        j = 1 if n % 2 else -1
        a.at(t, body=(-26, 8 * j, 2 * j), head=(22, -6 * j, 0), jaw=(-36 - 6 * (n % 2), 0, 0))
        if n % 2 == 0: a.arm(t, "r", (92, 10, 0), (0, 0, 0)).arm(t, "l", (40, 0, -30), (80, 0, 0))
        else: a.arm(t, "l", (92, 10, 0), (0, 0, 0)).arm(t, "r", (40, 0, 30), (80, 0, 0))
        a.legs(t, 44, 76, fwd=-0.6)
    a.at(32, body=(4, 0, 0), head=(30, 0, 0), jaw=(-50, 0, 0)).arms(32, (150, 0, 40), (20, 0, 0))
    a.legs(32, 10, 16, up=0.4)
    a.at(34, body=(-44, 0, 0), head=(10, 0, 0), jaw=(-30, 0, 0)).arms(34, (90, 8, -4), (0, 0, 0), (0, 0, 0))
    a.legs(34, 50, 90, fwd=-1.6)
    a.at(38, body=(-36, 0, 0), head=(14, 0, 0)).arms(38, (80, 8, 0), (6, 0, 0))
    a.at(42, body=(-10, 0, 0), head=(8, 0, 0), jaw=(0, 0, 0)).arms(42, (20, 0, 14), (20, 0, 0)).legs(42, 12, 18)
    a.claws(8, 30).claws(32, -20, spread=10).claws(34, 40).claws(42, 0)
    a.sec([(0, 0, 0), (3, -6, 0), (8, -2, 0), (12, 4, 3), (16, 4, -3), (20, 4, 3), (24, 4, -3), (28, 4, 3), (32, -8, 0), (34, 12, 0), (44, 0, 0)])
    a.done()

    # ================= boomerang (44): right hand grows a three-bladed claw star 1-5, wind 10, THROW 13, sprint after it 15-22,
    #                   left-claw SLASH 24, CATCH the returning star 32
    a = mk("boomerang", 44)
    a.scl("boom_r", (0, *HIDE), (0.99, *HIDE), (4, 1, 1, 1), (12.5, 1, 1, 1), (13, *HIDE), (30.5, *HIDE), (32, 1.15, 1.15, 1.15),
          (34, 1, 1, 1), (40, 1, 1, 1), (42, *HIDE), (44, *HIDE))
    a.hide("claws_r", 1, 42)
    a.spin("boomspin", [(0, 0), (5, 0), (12, 720), (31, 720), (32, 1000), (36, 1440), (44, 1440)], axis=2)
    a.at(4, body=(-6, -10, 0), head=(12, 6, 0)).arm(4, "r", (40, -10, 40), (40, 0, 0))
    a.at(10, body=(-10, -60, -6), head=(12, 46, 0), jaw=(-14, 0, 0))
    a.arm(10, "r", (20, -80, 60), (60, 0, 0), (0, 0, 0)).arm(10, "l", (70, 30, -20), (20, 0, 0))
    a.legs(10, -6, 10, 40, 70)
    a.at(13, body=(-24, 40, 6), head=(4, -30, 0), jaw=(-40, 0, 0))
    a.arm(13, "r", (92, 60, 0), (0, 0, 0), (0, 0, 0)).arm(13, "l", (-20, 0, -30), (20, 0, 0))
    a.legs(13, 40, 70, -10, 10, fwd=-1)
    a.at(15, body=(-26, 48, 6)).arm(15, "r", (80, 90, 0), (0, 0, 0))
    for t, j in ((17, 1), (19, -1), (21, 1)):
        a.at(t, body=(-40, 6 * j, 0), head=(36, 0, 0), jaw=(-30, 0, 0))
        a.arm(t, "r", (-30, 0, 20), (30, 0, 0))
        a.legs(t, 50 if j > 0 else -30, 90 if j > 0 else 30, -30 if j > 0 else 50, 30 if j > 0 else 90, fwd=-1.2)
    a.arm(17, "l", (-30, 0, -20), (30, 0, 0))
    a.at(22, body=(-30, 20, 0), head=(26, -14, 0), jaw=(-30, 0, 0)).arm(22, "l", (140, -70, 40), (20, 0, 0))
    a.at(24, body=(-36, -40, -6), head=(10, 26, 0), jaw=(-46, 0, 0)).arm(24, "l", (90, 80, 0), (0, 0, 0))
    a.legs(24, 30, 50, 50, 90, fwd=-1.6)
    a.at(28, body=(-30, -30, 0), head=(14, 16, 0)).arm(28, "l", (70, 90, 0), (10, 0, 0))
    a.at(31, body=(-14, -20, 0), head=(20, -30, 0), jaw=(-20, 0, 0)).arm(31, "r", (100, -50, 40), (20, 0, 0), (0, 0, 0))
    a.arm(31, "l", (30, 30, -10), (40, 0, 0))
    a.at(32, body=(-16, -24, -2)).arm(32, "r", (84, -46, 40), (30, 0, 0))
    a.at(34, body=(-12, -10, 0), head=(14, -10, 0), jaw=(-30, 0, 0)).arm(34, "r", (70, -30, 30), (60, 0, 0))
    a.legs(28, 30, 50).legs(32, 20, 30)
    a.at(40, body=(-8, 0, 0), head=(8, 0, 0), jaw=(0, 0, 0)).arms(40, (16, 0, 10), (20, 0, 0)).legs(40, 10, 16)
    a.claws(22, -20, "l", 10).claws(24, 40, "l").claws(30, 0, "l")
    a.sec([(0, 0, 0), (10, -4, -4), (13, 8, 5), (15, 6, 6), (17, 12, 2), (19, 12, -2), (21, 12, 2), (24, 8, -5), (28, 2, 0), (32, -4, -3), (44, 0, 0)])
    a.done()

    # ================= spiral (40): arms twist into a spiral lance 2-8 (deep crouch), LAUNCH 10, corkscrew flight 11-21
    #                   (drilling multi-hits), BURST 22 (helix unravels), land 24
    a = mk("spiral", 40)
    a.show("spiral", 2, 36, grow=6)
    a.hide("claws_r", 2, 36)
    a.spin("spiralspin", [(0, 0), (2, 0), (9, 360), (22, 3240), (30, 3780), (40, 3960)])
    a.scl("spiralspin", (0, 1, 1, 1), (21, 1, 1, 1), (22, 1.5, 1.3, 1.5), (24, 1, 1, 1), (40, 1, 1, 1))
    a.at(4, body=(-10, 0, 0), head=(10, 0, 0), jaw=(-10, 0, 0)).arms(4, (60, 10, 10), (40, 0, 0))
    a.at(8, body=(-30, -20, 0), head=(20, 16, 0), jaw=(-30, 0, 0)).arms(8, (94, 14, -6), (0, 0, 0), (0, 0, 0))
    a.legs(4, 20, 30).legs(8, 70, 126, fwd=1, setpos=False)
    rp = -drop(8, 14)
    a.rot("pelvis", (0, 0, 0, 0), (9, 0, 0, 0), (10, -62, 0, 0))
    for i, t in enumerate(range(12, 22, 2)):
        a.rot("pelvis", (t, -62, 0, 8 if i % 2 else -8))
    a.rot("pelvis", (22, -50, 0, 0), (24, -20, 0, 0), (30, 0, 0, 0))
    a.at(10, body=(-12, 0, 0), head=(58, 0, 0), jaw=(-50, 0, 0)).arms(10, (164, 10, -4), (0, 0, 0), (0, 0, 0))
    fly = dict(shin_r=(-10, 0, 0), shin_l=(-10, 0, 0), foot_r=(30, 0, 0), foot_l=(30, 0, 0))
    a.at(10, leg_r=(-8, 0, 2), leg_l=(-8, 0, -2), **fly)
    for i, t in enumerate(range(12, 22, 2)):
        j = 1 if i % 2 else -1
        a.at(t, body=(-12, 0, 4 * j), head=(58, 0, -4 * j), jaw=(-54, 0, 0)).arms(t, (164 + 2 * j, 10, -4), (0, 0, 0))
        a.at(t, leg_r=(-8 + 6 * j, 0, 2), leg_l=(-8 - 6 * j, 0, -2), **fly)
    a.pos("pelvis", (0, 0, rp, 0), (8, 0, -drop(70, 126), 1), (10, 0, rp + 3, -1), (21, 0, rp + 3, -1), (22, 0, rp + 2, -1))
    a.at(22, body=(-16, 0, 0), head=(50, 0, 0), jaw=(-64, 0, 0)).arms(22, (150, -40, 30), (0, 0, 0))
    a.at(22, leg_r=(10, 0, 2), leg_l=(10, 0, -2), shin_r=(-30, 0, 0), shin_l=(-30, 0, 0), foot_r=(20, 0, 0), foot_l=(20, 0, 0))
    a.at(24, body=(-30, 0, 0), head=(30, 0, 0), jaw=(-20, 0, 0)).arms(24, (60, 0, 40), (20, 0, 0))
    a.legs(24, 60, 110).legs(30, 40, 70).legs(36, 12, 18)
    a.at(30, body=(-20, 0, 0), head=(16, 0, 0)).at(36, body=(-8, 0, 0), head=(8, 0, 0), jaw=(0, 0, 0)).arms(36, (14, 0, 10), (14, 0, 0))
    a.sec([(0, 0, 0), (8, -4, -2), (10, 16, 0), (12, 16, 6), (16, 16, -6), (20, 16, 6), (22, 4, 0), (24, -8, 0), (30, 2, 0), (40, 0, 0)])
    a.done()

    # ================= hairwhip (40): crouch-twist 0-8, SPIN 10-16 (the mane lashes all around, hit 13),
    #                   cock back 21 (ahoge hardens into a blade), HEAD-STAB 24, recover
    a = mk("hairwhip", 40)
    a.show("ahblade", 16, 34, grow=4)
    a.spin("root", [(0, 0), (8, -50), (10, -40), (13, 180), (16, 330), (18, 360), (40, 360)])
    a.rot("mane0", (0, 0, 0, 0), (8, 10, 0, 0), (11, -30, 0, 0), (13, -55, 0, 0), (17, -50, 0, 0), (21, -20, 0, 0), (24, 30, 0, 0),
          (28, 10, 0, 0), (33, -4, 0, 0), (40, 0, 0, 0))
    for i in (1, 2, 3):
        a.rot(f"mane{i}", (0, 0, 0, 0), (9 + i, 6, 0, 0), (12 + i, -10, 0, 0), (16 + i, -12, 0, 20), (20 + i, 10, 0, -10),
              (25 + i, 30, 0, 0), (30 + i, -6, 0, 0), (40, 0, 0, 0))
    for k, s in (("r", 1), ("l", -1)):
        for i in range(3):
            a.rot(f"sw{i}_{k}", (0, 0, 0, 0), (8 + i, 0, 0, -10 * s), (12 + i, -10, 0, 40 * s), (15 + i, -20, 0, 50 * s), (20 + i, 0, 0, 10 * s),
                  (25 + i, 20, 0, -10 * s), (32 + i, 0, 0, 0), (40, 0, 0, 0))
    a.rot("ahoge", (0, 0, 0, 0), (16, 0, 0, 0), (21, 16, 0, 0), (24, -10, 0, 0), (28, -8, 0, 0), (34, 0, 0, 0), (40, 0, 0, 0))
    a.rot("bangs", (0, 0, 0, 0), (13, -14, 0, 10), (24, 16, 0, 0), (30, 4, 0, 0), (40, 0, 0, 0))
    a.at(4, body=(-20, -30, -6), head=(14, 20, 0), jaw=(-20, 0, 0)).arms(4, (40, -30, 40), (40, 0, 0))
    a.at(8, body=(-30, -50, -8), head=(20, 36, 0), jaw=(-30, 0, 0)).arms(8, (30, 0, 60), (30, 0, 0))
    a.legs(4, 40, 70).legs(8, 56, 100)
    a.at(13, body=(-14, 10, 6), head=(16, -10, 0), jaw=(-56, 0, 0)).arms(13, (10, 0, 80), (10, 0, 0))
    a.legs(13, 20, 30, up=0.5)
    a.at(17, body=(-10, 0, 0), head=(10, 0, 0), jaw=(-30, 0, 0)).arms(17, (20, 0, 60), (20, 0, 0)).legs(17, 24, 40)
    a.at(21, body=(14, 0, 0), head=(40, 0, 0), jaw=(-40, 0, 0)).arms(21, (-20, 0, 40), (40, 0, 0))
    a.legs(21, -6, 10, 30, 50)
    a.at(24, body=(-42, 0, 0), head=(8, 0, 0), jaw=(-30, 0, 0)).arms(24, (-30, 0, 30), (20, 0, 0))
    a.legs(24, 60, 100, -20, 10, fwd=-2.5)
    a.at(27, body=(-38, 0, 0), head=(6, 0, 0)).legs(27, 58, 98, -18, 12, fwd=-2.5)
    a.at(32, body=(-20, 0, 0), head=(4, 0, 0), jaw=(-10, 0, 0)).arms(32, (10, 0, 20), (20, 0, 0)).legs(32, 30, 50)
    a.at(38, body=(-8, 0, 0), head=(6, 0, 0), jaw=(0, 0, 0)).legs(38, 12, 18)
    a.claws(8, 20).claws(13, -20, spread=10).claws(24, 30).claws(34, 0)
    a.done()




def main():
    B = Builder("fen", 1.0, False, 6)
    build(B)
    anims(B)
    B.m.save(os.path.join(DIR, "fen.bbmodel"))
    tops = max(cb["to"][1] for cb in B.m.cubes)  # 62.5 px = 3.9 blocks (spider arms / ahoge blade), body ~61
    print("cubes", len(B.m.cubes), "top", tops, "anims", len(B.m.anims), [a["name"] for a in B.m.anims])

if __name__ == "__main__":
    main()
