"""Fen - generates assets/fpe/bbmodels/fen.bbmodel.
Reference (only trusted one): docs/ref/confirmed/fen.jpg - lanky feral girl in wolf-like crouching / crawling poses:
huge flowing ORANGE hair (bangs hide the eyes, one eye peeks through, curled ahoge, mane trailing behind like a fox tail /
flames), wide sharp-toothed grin, black tee, rolled blue denim shorts, bandaged knees / shins / feet, barefoot,
very long arms that turn into long BLACK claw-forearms with four long black claws reaching the ground,
white diamond sparkles around her, a curved dark-red blade (blade attacks only) and her small black cat with orange ring eyes.
Hitbox 0.7 x 2.0 blocks -> ~31 px upright, hunched rest pose ~27 px.
Blockbench space: Y up, ground 0, faces -Z, character's RIGHT = +X.
Signs (file values): limb rx>0 swings forward, torso/head rx>0 leans back / looks up, ry>0 turns to the character's left,
hanging part rz>0 swings toward +X. Upward part rx<0 tilts forward. Jaw rx<0 opens.
Run: python3 tools/bbgen/chars/fen.py
"""
import math, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))
from bbgen import mix  # noqa: E402
from alice import Builder, A, HIDE  # noqa: E402

DIR = os.path.join(os.path.dirname(__file__), "../../../src/main/resources/assets/fpe/bbmodels/")

HAIR, HAIR_M, HAIR_D, HAIR_HI = 0xF39A30, 0xE6801F, 0xBF5A16, 0xFFC466
SKIN, SKIN_D, SKIN_L = 0xF1D0B5, 0xD2A88E, 0xFBE3CF
SHIRT, SHIRT_D, SHIRT_HI = 0x1D1D26, 0x111117, 0x30303E
DENIM, DENIM_D, DENIM_L, DENIM_HI = 0x3F5F96, 0x2B4470, 0x7B9FD0, 0xA9C4E8
BAND, BAND_D = 0xEFE8DA, 0xB9AF9E
CLAW, CLAW_HI, CLAW_RED, CLAW_D = 0x15151C, 0x3C3C4C, 0x5A1522, 0x08080B
BLADE, BLADE_D, BLADE_E = 0x5C0E1A, 0x2E060C, 0xE0324A
TEETH, TEETH_D, MOUTH, LINE = 0xFAF6EE, 0xB8B0A4, 0x4A0F18, 0x24161A
CAT, CAT_HI, CAT_EYE = 0x17171E, 0x2C2C38, 0xFF8A1E
SPARK = 0xFFFFFF


# ================================================================== painters
def denim_p(B):
    R = B.R

    def f(F):
        for y in range(F.h):
            for x in range(F.w):
                c = mix(DENIM, DENIM_L, 0.18 * math.sin(math.pi * x / max(1, F.w)) + R.uniform(-0.04, 0.06))
                F.px(x, y, c)
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
    for x in range(0, F.w, 5):
        F.px(x, F.h // 2, DENIM_D)


def band_p(B, base=SKIN, full=False):
    R = B.R

    def f(F):
        F.rect(0, 0, F.w, F.h, base)
        y = R.randint(0, 3)
        while y < F.h + F.w:
            if full or R.random() < 0.8:
                th = 3 + R.randint(0, 1)
                F.poly([(0, y), (F.w, y - F.w * 0.35), (F.w, y - F.w * 0.35 + th), (0, y + th)], BAND)
                F.line(0, y + th, F.w, y - F.w * 0.35 + th, BAND_D, 1)
            y += 4 + R.randint(0, 3)
        if R.random() < 0.6:  # a little blood spot on the bandage
            F.disc(R.uniform(2, F.w - 2), R.uniform(2, F.h - 2), 1.2, 0xB4505A)
    return f


def claw_p(F):
    for y in range(F.h):
        for x in range(F.w):
            F.px(x, y, mix(CLAW, CLAW_RED, 0.75 * y / max(1, F.h - 1)))
    F.rect(1, 0, 1, F.h, CLAW_HI)
    F.rect(F.w - 1, 0, 1, F.h, CLAW_D)


def ink_arm_p(B):
    R = B.R

    def f(F):
        for y in range(F.h):
            for x in range(F.w):
                F.px(x, y, mix(CLAW, CLAW_HI, 0.25) if R.random() < 0.08 else CLAW)
        for _ in range(F.w // 3):
            x = R.uniform(0, F.w)
            F.line(x, R.uniform(0, F.h * 0.3), x + R.uniform(-1, 1), F.h, CLAW_HI, 1)
    return f


def elbow_p(B):
    R = B.R

    def f(F):
        F.rect(0, 0, F.w, F.h, SKIN)
        F.rect(0, 0, F.w, 2, SKIN_D)
        edge = [F.h * 0.45 + R.uniform(-2, 3) for _ in range(F.w + 1)]
        for x in range(F.w):  # ragged ink creeping up the arm
            for y in range(int(edge[x]), F.h):
                F.px(x, y, CLAW)
            if x % 4 == 0:
                F.line(x, edge[x], x, edge[x] - R.uniform(1, 4), CLAW, 1)
    return f


def face_p(F):
    W, H = F.w, F.h
    for y in range(H):
        F.rect(0, y, W, 1, mix(SKIN_L, SKIN, y / H))
    F.rect(0, 0, W, int(H * 0.22), mix(SKIN, HAIR_D, 0.35))  # hair shadow on the brow
    # peeking eye (character's left): big white eye, small dark pupil, dark upper lash
    ex, ey = 0.68 * W, 0.44 * H
    F.disc(ex, ey, 0.13 * W, LINE)
    F.disc(ex, ey, 0.11 * W, 0xFFFFFF)
    F.disc(ex - 0.02 * W, ey + 0.01 * H, 0.045 * W, 0x101014)
    F.disc(ex + 0.02 * W, ey - 0.04 * H, 0.016 * W, 0xFFFFFF, glow=True)
    F.line(ex - 0.14 * W, ey - 0.12 * H, ex + 0.14 * W, ey - 0.15 * H, LINE, 2)
    # hidden eye under the bangs: dark socket shadow
    F.disc(0.3 * W, 0.45 * H, 0.1 * W, mix(SKIN_D, LINE, 0.3))
    # wide grin (upper half of the mouth; jaw carries the lower teeth)
    top = H * 0.8
    F.poly([(0.08 * W, H * 0.62), (0.16 * W, top), (0.84 * W, top), (0.92 * W, H * 0.62), (0.95 * W, H), (0.05 * W, H)], LINE)
    F.poly([(0.11 * W, H * 0.68), (0.18 * W, top + 1), (0.82 * W, top + 1), (0.89 * W, H * 0.68), (0.91 * W, H), (0.09 * W, H)], MOUTH)
    n = 9
    for i in range(n):
        x0 = 0.1 * W + i * 0.8 * W / n
        tw = 0.8 * W / n
        F.poly([(x0, top + 1), (x0 + tw, top + 1), (x0 + tw * 0.5, H)], TEETH)
        F.line(x0 + tw * 0.5, top + 1, x0 + tw * 0.5, top + (H - top) * 0.5, TEETH_D, 1)
    F.disc(0.18 * W, 0.6 * H, 0.04 * W, mix(SKIN, 0xE58C8C, 0.5))
    F.disc(0.82 * W, 0.6 * H, 0.04 * W, mix(SKIN, 0xE58C8C, 0.5))


def jaw_p(F):
    W, H = F.w, F.h
    F.rect(0, 0, W, H, SKIN)
    F.rect(0, H - 2, W, 2, SKIN_D)
    F.rect(int(0.07 * W), 0, int(0.86 * W), int(H * 0.62), LINE)
    F.rect(int(0.09 * W), 0, int(0.82 * W), int(H * 0.55), MOUTH)
    n = 8
    for i in range(n):
        x0 = 0.1 * W + i * 0.8 * W / n
        tw = 0.8 * W / n
        F.poly([(x0, H * 0.55), (x0 + tw, H * 0.55), (x0 + tw * 0.5, 0)], TEETH)


def mouth_p(F):
    F.rect(0, 0, F.w, F.h, MOUTH)
    F.rect(0, 0, F.w, 2, TEETH)


def toes_p(F):
    F.rect(0, 0, F.w, F.h, SKIN)
    F.rect(0, 0, F.w, 3, BAND)
    for x in range(2, F.w, 4):
        F.line(x, F.h * 0.4, x, F.h, SKIN_D, 1)


def blade_p(B):
    R = B.R

    def f(F):
        for y in range(F.h):
            for x in range(F.w):
                F.px(x, y, mix(BLADE, BLADE_D, 0.5 * x / max(1, F.w - 1) + R.uniform(-0.05, 0.05)))
        for _ in range(3):
            y = R.uniform(0, F.h)
            F.line(0, y, F.w, y + R.uniform(-3, 3), BLADE_D, 1)
    return f


def cat_face_p(F):
    W, H = F.w, F.h
    F.rect(0, 0, W, H, CAT)
    for cx in (0.3 * W, 0.7 * W):
        F.disc(cx, 0.5 * H, 0.19 * W, CAT_EYE, glow=True)
        F.disc(cx, 0.5 * H, 0.11 * W, 0x050507, glow=True)
        F.disc(cx + 0.05 * W, 0.42 * H, 0.03 * W, 0xFFFFFF, glow=True)


def shirt_p(B):
    folds = B.folds(SHIRT, SHIRT_D, SHIRT_HI, 3)

    def f(F):
        folds(F)
        F.rect(0, 0, F.w, 1, SHIRT_HI)
    return f


# ================================================================== model
def build(B):
    g, c = B.g, B.c
    hair = B.all(B.strands(HAIR, HAIR_HI, HAIR_D))
    hairm = B.all(B.strands(HAIR_M, HAIR, HAIR_D))
    shirt = B.all(shirt_p(B))
    denim = B.all(denim_p(B))
    band = B.all(band_p(B))
    band_full = B.all(band_p(B, BAND, True))
    ink = B.all(ink_arm_p(B))
    claw = claw_p

    g("root", (0, 0, 0))
    # ---------------- pelvis / legs
    g("pelvis", (0, 12, 0), "root")
    c("hips", "pelvis", (-3, 11, -1.8), (3, 13.6, 1.8), DENIM, faces=denim)
    c("belt", "pelvis", (-3.1, 13.0, -1.9), (3.1, 13.7, 1.9), DENIM_D)
    c("fly", "pelvis", (-0.3, 11.3, -1.95), (0.3, 13.0, -1.8), DENIM_D)
    c("pocket", "pelvis", (1.0, 12.0, 1.8), (2.6, 13.0, 1.95), DENIM_L)
    for s, k in ((1, "r"), (-1, "l")):
        x = 1.5 * s
        g("leg_" + k, (x, 12, 0), "pelvis")
        c("thigh_" + k, "leg_" + k, (x - 1.45, 8.8, -1.55), (x + 1.45, 12.2, 1.55), DENIM, faces=denim)
        c("cuff_" + k, "leg_" + k, (x - 1.7, 8.1, -1.75), (x + 1.7, 9.4, 1.75), DENIM_L, faces=B.all(cuff_p))
        c("knee_" + k, "leg_" + k, (x - 1.0, 6.7, -1.0), (x + 1.0, 8.3, 1.0), SKIN, faces=band)
        g("shin_" + k, (x, 7, 0), "leg_" + k)
        c("calf_" + k, "shin_" + k, (x - 0.95, 1.4, -0.95), (x + 0.95, 7.1, 0.95), SKIN, faces=band)
        c("wrap_" + k, "shin_" + k, (x - 1.1, 2.6, -1.1), (x + 1.1, 4.8, 1.1), BAND, faces=band_full)
        g("foot_" + k, (x, 1.5, 0), "shin_" + k)
        c("sole_" + k, "foot_" + k, (x - 1.0, 0, -2.9), (x + 1.0, 1.5, 0.9), SKIN, faces={"north": toes_p, "up": toes_p})
        c("anktape_" + k, "foot_" + k, (x - 1.06, 0.9, -1.06), (x + 1.06, 1.9, 1.06), BAND, faces=band_full)

    # ---------------- torso
    g("body", (0, 13.5, 0), "pelvis")
    c("waist", "body", (-2.6, 13.4, -1.6), (2.6, 17.2, 1.6), SHIRT, faces=shirt)
    c("chest", "body", (-3.0, 17.0, -1.8), (3.0, 21.6, 1.8), SHIRT, faces=shirt)
    for i, x in enumerate((-2.4, -0.8, 0.9, 2.3)):  # ragged tee hem
        c(f"hem{i}", "body", (x - 0.7, 12.7 + 0.3 * (i % 2), -1.75), (x + 0.7, 13.8, 1.75), SHIRT_D, rot=(0, 0, (i - 1.5) * 6))
    c("collar", "body", (-1.6, 21.4, -1.9), (1.6, 21.9, 1.2), SHIRT_HI)
    c("neck", "body", (-0.9, 21.5, -0.9), (0.9, 23.0, 0.9), SKIN_D)

    # ---------------- head
    g("head", (0, 22.6, 0), "body")
    c("skull", "head", (-3.4, 24.0, -3.4), (3.4, 30.0, 3.4), SKIN, faces={"north": face_p, "down": mouth_p})
    g("jaw", (0, 24.0, 1.0), "head")
    c("jawc", "jaw", (-3.1, 22.2, -3.3), (3.1, 24.05, 1.6), SKIN, faces={"north": jaw_p, "up": mouth_p})
    c("cap", "head", (-3.9, 27.4, -3.9), (3.9, 30.7, 3.9), HAIR, faces=hair)
    c("capb", "head", (-3.9, 23.2, 0.2), (3.9, 27.5, 3.9), HAIR_M, faces=hairm)
    for s, k in ((1, "r"), (-1, "l")):
        x0, x1 = sorted((3.3 * s - 0.55 * s, 3.3 * s + 0.6 * s))
        c("sideh_" + k, "head", (x0, 22.8, -3.6), (x1, 27.6, 3.2), HAIR, faces=hair)
        g("side_" + k, (3.6 * s, 28.0, -1.6), "head", rot=(-6, 0, 14 * s))
        B.lock("sl0_" + k, "side_" + k, (3.6 * s, 28.0, -1.6), 9.0, 1.8, 1.4, (0, 0, 4 * s), HAIR, tip=HAIR_D, paint=hair["north"])
        B.lock("sl1_" + k, "side_" + k, (3.8 * s, 27.6, 0.8), 7.0, 1.6, 1.4, (8, 0, 10 * s), HAIR_M, tip=HAIR_D, paint=hair["north"])
    g("bangs", (0, 30.2, -3.9), "head")
    for i, (x, ln, rz) in enumerate(((3.1, 4.4, 12), (1.7, 5.4, 8), (0.3, 5.8, 4), (-2.3, 5.0, -2), (-3.5, 4.0, -10))):
        B.lock(f"bang{i}", "bangs", (x, 30.6, -4.0), ln, 2.0, 0.9, (-10, 0, rz), HAIR if i % 2 else HAIR_M, tip=HAIR_D, paint=hair["north"])
    for i, (x, rz) in enumerate(((2.4, 50), (-1.2, -40), (0.6, 15))):  # spiky top tufts
        B.blade(f"tuft{i}", "head", (x, 30.2, 0.5 * i - 1), 2.6, 1.6, 1.4, (-30 + 20 * i, 0, -rz), HAIR, tip=HAIR_HI, paint=hair["north"])
    g("ahoge", (0.5, 30.5, -0.6), "head")
    c("ah0", "ahoge", (0.15, 30.3, -0.95), (0.85, 33.2, -0.25), HAIR, origin=(0.5, 30.5, -0.6), rot=(-28, 0, -12))
    c("ah1", "ahoge", (0.7, 32.5, -3.3), (1.4, 33.2, -1.3), HAIR, origin=(1.0, 32.8, -2.3), rot=(10, 0, 0))
    c("ah2", "ahoge", (0.7, 31.3, -3.6), (1.4, 32.7, -2.9), HAIR_D, origin=(1.0, 32.0, -3.2), rot=(-15, 0, 0))

    # ---------------- mane: 4-segment chain trailing behind like a fox tail / flames
    g("manec", (0, 28.8, 3.0), "head")  # pitch-compensation pivot (animated automatically, see F.done)
    g("mane0", (0, 28.8, 3.0), "manec", rot=(-28, 0, 0))
    c("m0a", "mane0", (-4.4, 21.0, 2.4), (4.4, 30.6, 5.8), HAIR, faces=hair)
    for s in (1, -1):
        B.lock(f"m0f{'r' if s > 0 else 'l'}", "mane0", (4.4 * s, 28.0, 3.6), 9.0, 2.0, 2.4, (0, 0, 22 * s), HAIR_M, tip=HAIR_D, paint=hair["north"])
    g("mane1", (0, 21.6, 4.2), "mane0", rot=(-18, 0, 0))
    c("m1a", "mane1", (-4.9, 14.6, 2.8), (4.9, 22.0, 5.8), HAIR_M, faces=hairm)
    for i, x in enumerate((-4.6, -1.6, 1.6, 4.6)):
        B.lock(f"m1l{i}", "mane1", (x, 15.4, 4.3), 4.2 + (i % 2), 2.6, 2.2, (0, 0, x * 4), HAIR if i % 2 else HAIR_M, tip=HAIR_D, paint=hair["north"])
    g("mane2", (0, 15.0, 4.3), "mane1", rot=(-14, 0, 0))
    c("m2a", "mane2", (-4.5, 9.0, 3.0), (4.5, 15.4, 5.6), HAIR, faces=hair)
    for s in (1, -1):  # flame flicks curling up off the sides
        B.blade(f"m2k{'r' if s > 0 else 'l'}", "mane2", (4.4 * s, 11.0, 4.3), 5.0, 1.8, 1.8, (-35, 0, -60 * s), HAIR, tip=HAIR_HI, paint=hair["north"])
    g("mane3", (0, 9.4, 4.3), "mane2", rot=(-12, 0, 0))
    for i, (x, ln) in enumerate(((-3.6, 7.0), (-1.2, 8.5), (1.2, 8.0), (3.6, 6.5))):
        B.lock(f"m3l{i}", "mane3", (x, 9.8, 4.3), ln, 2.6, 2.4, (0, 0, x * 5), HAIR_M if i % 2 else HAIR, tip=HAIR_D, paint=hair["north"])
    for s in (1, -1):
        B.blade(f"m3k{'r' if s > 0 else 'l'}", "mane3", (2.6 * s, 3.4, 4.3), 5.0, 1.8, 1.8, (-70, 0, -30 * s), HAIR, tip=HAIR_HI, paint=hair["north"])

    # ---------------- arms: short black sleeve, skinny upper arm, ink-black forearm, 4 long claws
    for s, k in ((1, "r"), (-1, "l")):
        x = 3.5 * s
        g("arm_" + k, (x, 21.2, 0), "body")
        c("sleeve_" + k, "arm_" + k, (x - 1.15, 18.6, -1.15), (x + 1.15, 21.9, 1.15), SHIRT, faces=shirt)
        c("upper_" + k, "arm_" + k, (x - 0.8, 15.4, -0.8), (x + 0.8, 18.8, 0.8), SKIN)
        g("fore_" + k, (x, 15.6, 0), "arm_" + k)
        c("elbow_" + k, "fore_" + k, (x - 0.9, 13.6, -0.9), (x + 0.9, 15.9, 0.9), SKIN, faces=B.all(elbow_p(B)))
        c("forearm_" + k, "fore_" + k, (x - 1.0, 9.6, -1.0), (x + 1.0, 13.8, 1.0), CLAW, faces=ink)
        c("wrist_" + k, "fore_" + k, (x - 1.25, 8.7, -1.25), (x + 1.25, 10.4, 1.25), CLAW, faces=ink)
        for i, y in enumerate((12.6, 10.6)):  # ragged ink spikes on the outer forearm
            B.blade(f"aspk{i}_{k}", "fore_" + k, (x + 0.9 * s, y, 0.4), 2.0 - 0.4 * i, 0.8, 0.8, (-50, 0, -40 * s), CLAW, tip=CLAW_HI)
        g("hand_" + k, (x, 8.9, 0), "fore_" + k)
        c("palm_" + k, "hand_" + k, (x - 1.3, 7.0, -1.4), (x + 1.3, 9.0, 1.4), CLAW, faces=ink)
        for i, (dx, dz, ln) in enumerate(((0.8, -1.0, 6.2), (0.1, -0.2, 7.2), (-0.6, 0.6, 6.8), (1.1, 0.9, 4.6))):
            fx = x + dx * s
            g(f"fing{i}_{k}", (fx, 7.2, dz), "hand_" + k, rot=(10 if i < 3 else -10, 0, (i - 1) * 5 * s))
            B.lock(f"cl{i}_{k}", f"fing{i}_{k}", (fx, 7.3, dz), ln, 0.95, 0.75, (0, 0, 0), CLAW, tip=CLAW_RED, paint=claw)
            c(f"clh{i}_{k}", f"fing{i}_{k}", (fx - 0.12, 7.3 - ln - 0.9, dz - 0.9), (fx + 0.12, 7.3 - ln + 0.2, dz - 0.4),
              CLAW_RED, origin=(fx, 7.3 - ln, dz), rot=(35, 0, 0))  # hooked tip

    # ---------------- props: dark-red curved blade (right hand), sparkles, the cat
    g("blade", (3.5, 8.2, 0), "hand_r")
    c("grip", "blade", (3.0, 7.4, -1.9), (4.0, 8.6, 1.9), 0x2A1418)
    c("guard", "blade", (2.8, 6.8, -1.2), (4.2, 7.5, 1.2), CLAW)
    bp = B.all(blade_p(B))
    pv, prev = (3.5, 6.9, 0.0), "blade"
    for i, (ln, w, bend) in enumerate(((4.0, 2.4, 0), (3.6, 2.2, 16), (3.2, 1.8, 18), (2.8, 1.3, 22))):
        nm = f"bl{i}"
        g(nm, pv, prev, rot=(bend, 0, 0))
        x, y, z = pv
        c(nm + "c", nm, (x - 0.3, y - ln, z - w * 0.4), (x + 0.3, y, z + w * 0.6), BLADE, faces=bp)
        c(nm + "e", nm, (x - 0.2, y - ln, z - w * 0.4 - 0.35), (x + 0.2, y, z - w * 0.4), BLADE_E, glow=True)
        pv, prev = (x, y - ln, z), nm
    x, y, z = pv
    c("bltip", prev, (x - 0.2, y - 2.2, z - 0.5), (x + 0.2, y, z + 0.4), BLADE_E, origin=(x, y, z), rot=(25, 0, 0), glow=True)

    g("sparkles", (0, 30, 0), "root")
    for i, (x, y, z, sz) in enumerate(((-7.0, 31.0, 1.0, 1.0), (6.4, 34.0, 2.0, 0.8), (7.6, 28.0, -1.0, 0.6), (-5.4, 35.0, -1.0, 0.5))):
        c(f"spark{i}", "sparkles", (x - 0.55 * sz, y - 0.55 * sz, z - 0.15), (x + 0.55 * sz, y + 0.55 * sz, z + 0.15), SPARK,
          rot=(0, 0, 45), glow=True)

    g("cat", (-7, 0, -3), "root")
    c("catbody", "cat", (-8.3, 1.0, -4.2), (-5.7, 3.4, 0.4), CAT, color2=CAT_HI, grad=True)
    for i, (dx, dz) in enumerate(((-0.9, -3.6), (0.9, -3.6), (-0.9, -0.2), (0.9, -0.2))):
        c(f"catleg{i}", "cat", (-7 + dx - 0.4, 0, dz - 0.4), (-7 + dx + 0.4, 1.3, dz + 0.4), CAT)
    g("cathead", (-7, 3.0, -4.2), "cat")
    c("catskull", "cathead", (-8.6, 2.2, -7.0), (-5.4, 5.4, -3.8), CAT, faces={"north": cat_face_p})
    for s in (1, -1):
        c(f"catear{'r' if s > 0 else 'l'}", "cathead", (-7 + 1.1 * s - 0.5, 5.2, -6.0), (-7 + 1.1 * s + 0.5, 6.6, -5.2), CAT,
          origin=(-7 + 1.1 * s, 5.4, -5.6), rot=(0, 0, -14 * s))
    g("cattail", (-7, 2.8, 0.3), "cat", rot=(-30, 0, 0))
    c("cattail0", "cattail", (-7.3, 2.6, 0.0), (-6.7, 6.4, 0.6), CAT)
    c("cattail1", "cattail", (-7.3, 6.0, -1.2), (-6.7, 6.6, 0.6), CAT, origin=(-7, 6.3, 0.3), rot=(-20, 0, 0))


# ================================================================== animation
def m3(v):
    return (v[0], -v[1], -v[2])


THIGH, SHIN_L = 5.0, 5.5


def drop(a, k):
    """pelvis drop needed so a foot with thigh angle a and knee bend k stays on the ground"""
    return 10.5 - THIGH * math.cos(math.radians(a)) - SHIN_L * math.cos(math.radians(a - k))


REST = {"body": (-26, 0, 0), "head": (20, 0, 0), "jaw": (0, 0, 0),
        "arm_r": (30, 0, 8), "arm_l": (30, 0, -8), "fore_r": (14, 0, 0), "fore_l": (14, 0, 0), "hand_r": (8, 0, 0), "hand_l": (8, 0, 0),
        "leg_r": (40, 0, 4), "leg_l": (40, 0, -4), "shin_r": (-70, 0, 0), "shin_l": (-70, 0, 0), "foot_r": (30, 0, 0), "foot_l": (30, 0, 0)}
RESTP = {"pelvis": (0, -drop(40, 70), 0)}
PROPS = ("blade", "cat")


class F(A):
    def done(self, base_layer=False):
        if not base_layer:
            for b, v in RESTP.items():
                ks = self.tr.get(b, {}).get("position")
                if not ks:
                    self.pos(b, (0, *v))
                else:
                    ts = [q[0] for q in ks]
                    if 0 not in ts: ks.append((0, *v))
                    if max(ts) < self.ticks: ks.append((self.ticks, *v))
            self._mane_comp()
        return A.done(self, base_layer)

    def _mane_comp(self, gain=0.8):
        """hair hangs with gravity: counter-rotate the mane root against the summed body+head(+pelvis) pitch change"""
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
        bones = ["body", "head"] + ([] if self.name in ("backflip", "hairwhip") else ["pelvis"])
        ts = sorted({q[0] for b in bones for q in self.tr.get(b, {}).get("rotation", [])} | {0, self.ticks})
        rest = REST["body"][0] + REST["head"][0]
        for t in ts:
            p = sum(sample(b, t) for b in bones)
            self.rot("manec", (t, max(-80, min(60, -(p - rest) * gain)), 0, 0))

    # ---- pose helpers
    def legs(self, t, a=40, k=70, al=None, kl=None, up=0.0, fwd=0.0, spread=0.0, setpos=True):
        al = a if al is None else al
        kl = k if kl is None else kl
        d = min(drop(a, k), drop(al, kl))
        self.at(t, leg_r=(a, 0, 4 + spread), shin_r=(-k, 0, 0), foot_r=(k - a, 0, 0),
                leg_l=(al, 0, -4 - spread), shin_l=(-kl, 0, 0), foot_l=(kl - al, 0, 0))
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
                base = 10 if i < 3 else -10
                self.rot(f"fing{i}_{k}", (t, base + curl, 0, (i - 1) * (5 + spread) * s))
        return self

    def sec(self, keys, delay=2):
        """hair secondary motion from body signal (t, x, z): x>0 = lurch forward (hair flies back), z>0 = sway toward +X"""
        for i in range(4):
            g = 0.45 + 0.2 * i
            self.drape(f"mane{i}", [(t, -x * g, z * 0.25 * i, z * g * 0.6) for (t, x, z) in keys], delay + i)
        self.drape("bangs", [(t, -x * 0.25, 0, z * 0.3) for (t, x, z) in keys], delay)
        self.drape("side_r", [(t, -x * 0.5, 0, z * 0.6 + abs(x) * 0.3) for (t, x, z) in keys], delay)
        self.drape("side_l", [(t, -x * 0.5, 0, z * 0.6 - abs(x) * 0.3) for (t, x, z) in keys], delay)
        self.drape("ahoge", [(t, -x * 0.9, 0, z * 0.8) for (t, x, z) in keys], delay + 1)
        return self

    def hold(self, bone, val, t0, t1):
        return self.rot(bone, (t0, *val), (t1, *val))


Z0 = (0, 0, 0)


def anims(B):
    def mk(name, ticks, loop=False):
        return F(B, name, ticks, REST, PROPS, loop)

    # ================= idle (60): predator crouch, breathing, head-cock, claws flex, hair sways, sparkles orbit
    a = mk("idle", 60, loop=True)
    for t, j in ((0, 0), (15, 1), (30, 0), (45, -1), (60, 0)):
        b = abs(j)
        a.at(t, body=(-26 - 2 * b, 2 * j, 0), head=(20 + 2 * b, -4 * j, 3 * j), jaw=(-2 * b, 0, 0))
        a.arm(t, "r", (30 + 3 * b, 0, 8 + j), (14 + 4 * b, 0, 0), (8, 0, 0))
        a.arm(t, "l", (30 + 3 * b, 0, 8 - j), (14 + 4 * b, 0, 0), (8, 0, 0))
        a.legs(t, 40 + 2 * b, 70 + 4 * b)
    a.at(34, head=(22, 10, 16)).at(38, head=(21, 8, 18)).at(41, head=(22, -2, -4))  # curious head-cock
    a.claws(0, 0).claws(12, 20).claws(16, -8).claws(30, 0).claws(48, 25).claws(52, -5).claws(60, 0)
    a.sec([(0, 0, 1), (15, 2, -1), (30, 0, 1), (45, 2, -1), (60, 0, 1)], delay=4)
    a.rot("sparkles", (0, 0, 0, 0), (15, 0, 90, 0), (30, 0, 180, 0), (45, 0, 270, 0), (60, 0, 360, 0))
    a.pos("sparkles", (0, 0, 0, 0), (15, 0, 0.8, 0), (30, 0, 0, 0), (45, 0, -0.6, 0), (60, 0, 0, 0))
    a.scl("blade", (0, *HIDE)).scl("cat", (0, *HIDE))
    a.done(base_layer=True)

    # ================= walk (24, additive over idle): low wolf lope on all fours, diagonal pairs
    a = mk("walk", 24, loop=True)
    for t, sw in ((0, 1), (6, 0), (12, -1), (18, 0), (24, 1)):
        a.arm(t, "r", (24 + 22 * sw, 0, 0), (4 + 22 * max(0, -sw) + (14 if t == 18 else 0), 0, 0), (-10 * sw, 0, 0))
        a.arm(t, "l", (24 - 22 * sw, 0, 0), (4 + 22 * max(0, sw) + (14 if t == 6 else 0), 0, 0), (10 * sw, 0, 0))
        a.at(t, leg_l=(26 * sw, 0, 0), leg_r=(-26 * sw, 0, 0),
             shin_l=(-30 * max(0, -sw) - (24 if sw == 0 and t == 18 else 0), 0, 0),
             shin_r=(-30 * max(0, sw) - (24 if sw == 0 and t == 6 else 0), 0, 0))
    a.rot("body", (0, -30, 6, -3), (6, -27, 0, 0), (12, -30, -6, 3), (18, -27, 0, 0), (24, -30, 6, -3))
    a.rot("head", (0, 26, -6, 3), (6, 22, 0, 0), (12, 26, 6, -3), (18, 22, 0, 0), (24, 26, -6, 3))
    a.pos("pelvis", (0, 0, -0.6, 0), (6, 0, 0.6, 0), (12, 0, -0.6, 0), (18, 0, 0.6, 0), (24, 0, -0.6, 0))
    a.rot("pelvis", (0, 0, -6, 3), (12, 0, 6, -3), (24, 0, -6, 3))
    for t, cv in ((0, 20), (6, -10), (12, 20), (18, -10), (24, 20)):
        a.claws(t, cv - 10)
    a.sec([(0, 5, 3), (6, 1, 0), (12, 5, -3), (18, 1, 0), (24, 5, 3)], delay=2)
    a.done(base_layer=True)

    # ================= pounce (28): crouch+wiggle 0-7, LAUNCH 8, airborne claws-first 11-15, LAND slash 16, absorb, recover
    a = mk("pounce", 28)
    a.legs(4, 70, 120, fwd=1.0).legs(7, 74, 126, fwd=1.2).legs(8, -10, 10, up=3, fwd=-1).legs(11, -30, 50, up=6, fwd=-2) \
        .legs(14, 20, 60, up=3, fwd=-2).legs(16, 70, 120, fwd=-1).legs(19, 76, 130).legs(23, 50, 90)
    a.at(4, body=(-42, 0, 0), head=(36, 0, 0), jaw=(-8, 0, 0))
    a.rot("pelvis", (3, 0, 7, 0), (5, 0, -7, 0), (7, 0, 0, 0), (28, 0, 0, 0))
    a.at(7, body=(-46, 0, 0), head=(42, 0, 0), jaw=(-14, 0, 0))
    a.at(8, body=(-66, 0, 0), head=(56, 0, 0), jaw=(-30, 0, 0))
    a.at(11, body=(-78, 0, 0), head=(60, 0, 0), jaw=(-36, 0, 0))
    a.at(14, body=(-62, 0, 0), head=(48, 0, 0), jaw=(-30, 0, 0))
    a.at(16, body=(-50, 0, 0), head=(30, 0, 0), jaw=(0, 0, 0))
    a.at(19, body=(-46, 0, 0), head=(26, 0, 0), jaw=(-6, 0, 0))
    a.at(23, body=(-34, 0, 0), head=(22, 0, 0))
    a.arms(4, (-30, 0, 14), (30, 0, 0), (20, 0, 0)).arms(7, (-36, 0, 16), (34, 0, 0), (24, 0, 0))
    a.arms(8, (150, 0, 18), (0, 0, 0), (-10, 0, 0)).arms(11, (172, 0, 24), (-6, 0, 0), (-16, 0, 0))
    a.arms(14, (150, 0, 18), (6, 0, 0), (10, 0, 0)).arms(16, (66, 0, 10), (20, 0, 0), (30, 0, 0))
    a.arms(19, (60, 0, 12), (24, 0, 0), (20, 0, 0)).arms(23, (40, 0, 10), (18, 0, 0), (10, 0, 0))
    a.claws(4, 30).claws(8, -24, spread=6).claws(14, -20, spread=6).claws(16, 45).claws(20, 30).claws(28, 0)
    a.sec([(0, 0, 0), (5, -3, 0), (8, 10, 0), (12, 4, 0), (16, -8, 0), (20, 3, 0), (28, 0, 0)])
    a.done()

    # ================= rake (30): right swipe 7, left swipe 14, overhead double slam 23
    a = mk("rake", 30)
    a.at(4, body=(-28, -28, -6), head=(22, 18, 0), jaw=(-6, 0, 0))
    a.arm(4, "r", (124, -76, 0), (10, 0, 0), (-20, 0, 0)).arm(4, "l", (40, 10, -6), (20, 0, 0))
    a.at(7, body=(-34, 30, 6), head=(18, -16, 0), jaw=(-14, 0, 0))
    a.arm(7, "r", (112, 50, 0), (0, 0, 0), (10, 0, 0))
    a.arm(9, "r", (92, 66, 0), (14, 0, 0), (16, 0, 0))
    a.at(11, body=(-30, 26, 6), head=(20, -14, 0))
    a.arm(11, "l", (124, -76, 0), (10, 0, 0), (-20, 0, 0)).arm(11, "r", (60, 30, 0), (20, 0, 0))
    a.at(14, body=(-34, -30, -6), head=(18, 16, 0), jaw=(-14, 0, 0))
    a.arm(14, "l", (112, 50, 0), (0, 0, 0), (10, 0, 0))
    a.arm(16, "l", (92, 66, 0), (14, 0, 0), (16, 0, 0)).arm(16, "r", (40, 0, 10), (16, 0, 0))
    a.at(19, body=(-6, 0, 0), head=(34, 0, 0), jaw=(-26, 0, 0))
    a.arms(19, (196, 0, 16), (14, 0, 0), (-10, 0, 0))
    a.arms(21, (204, 0, 18), (20, 0, 0), (-16, 0, 0))
    a.at(21, body=(-2, 0, 0), head=(38, 0, 0))
    a.at(23, body=(-54, 0, 0), head=(16, 0, 0), jaw=(-4, 0, 0))
    a.arms(23, (78, 0, 10), (6, 0, 0), (24, 0, 0))
    a.at(26, body=(-50, 0, 0), head=(18, 0, 0))
    a.arms(26, (70, 0, 12), (12, 0, 0), (24, 0, 0))
    a.legs(4, 44, 76, 34, 60).legs(7, 30, 56, 50, 90, fwd=-0.8).legs(11, 50, 90, 30, 56).legs(14, 34, 60, 50, 90, fwd=-0.8) \
        .legs(19, 20, 30, up=0.5).legs(23, 70, 124).legs(26, 66, 116)
    a.claws(4, -20).claws(7, 20, "r").claws(11, -20, "l").claws(14, 20, "l").claws(19, -24).claws(23, 40).claws(27, 30)
    a.sec([(0, 0, 0), (4, -2, -3), (7, 6, 4), (11, -2, 4), (14, 6, -4), (19, -6, 0), (23, 10, 0), (26, 2, 0), (30, 0, 0)])
    a.done()

    # ================= sprint (36): screech 4, all-fours gallop 7-27, skid stop 28
    a = mk("sprint", 36)
    a.at(3, body=(-14, 0, 0), head=(46, 0, 0), jaw=(-34, 0, 0)).at(6, body=(-16, 0, 0), head=(48, 0, 0), jaw=(-36, 0, 0))
    a.arms(3, (10, 0, 30), (20, 0, 0), (-20, 0, 0)).arms(6, (14, 0, 34), (20, 0, 0))
    a.legs(3, 30, 50).legs(6, 32, 54)
    a.claws(3, -26, spread=6)
    for i, t in enumerate(range(7, 28, 3)):
        ph = i % 2
        a.at(t, body=(-64 if ph else -58, 0, 0), head=(56 if ph else 50, 0, 0), jaw=(-10, 0, 0))
        a.arms(t, (110, 0, 6) if ph == 0 else (24, 0, 6), (-10, 0, 0) if ph == 0 else (30, 0, 0), (-20, 0, 0) if ph == 0 else (30, 0, 0))
        a.legs(t, -24 if ph == 0 else 74, 30 if ph == 0 else 100, up=(1.5 if ph == 0 else -0.5))
        a.claws(t, -10 if ph == 0 else 30)
    a.at(28, body=(-40, 0, 0), head=(34, 0, 0), jaw=(-6, 0, 0)).at(31, body=(-36, 0, 0), head=(26, 0, 0))
    a.arms(28, (80, 0, 16), (6, 0, 0), (30, 0, 0)).arms(31, (60, 0, 12), (14, 0, 0), (20, 0, 0))
    a.legs(28, 10, 40, fwd=1.5).legs(31, 50, 90)
    a.claws(28, 50).claws(32, 20)
    a.sec([(0, 0, 0), (4, -4, 0), (7, 8, 0), (10, 10, 2), (13, 8, -2), (16, 10, 2), (19, 8, -2), (22, 10, 2), (25, 8, -2),
           (28, -8, 0), (31, 2, 0), (36, 0, 0)])
    a.done()

    # ================= blade (38): draw 0-4, horizontal sweep 10, backhand 19 (wave), overhead cleave 29
    a = mk("blade", 38)
    a.show("blade", 2, 36)
    a.rot("hand_r", (2, 0, -160, 0), (5, 0, 0, 0))
    a.at(3, body=(-22, -10, 0), head=(22, 6, 0))
    a.arm(3, "r", (40, -30, 34), (20, 0, 0))
    a.at(7, body=(-30, -42, -6), head=(24, 26, 0), jaw=(-8, 0, 0))
    a.arm(7, "r", (104, -96, 0), (8, 0, 0)).arm(7, "l", (64, 24, -10), (20, 0, 0))
    a.at(10, body=(-34, 36, 6), head=(20, -18, 0), jaw=(-16, 0, 0))
    a.arm(10, "r", (98, 62, 0), (0, 0, 0)).arm(10, "l", (20, -10, -20), (30, 0, 0))
    a.arm(12, "r", (86, 82, 0), (10, 0, 0))
    a.at(16, body=(-30, 48, 4), head=(22, -26, 0))
    a.arm(16, "r", (104, 92, 0), (34, 0, 0), (0, 40, 0))
    a.at(19, body=(-34, -36, -6), head=(20, 18, 0), jaw=(-16, 0, 0))
    a.arm(19, "r", (100, -72, 0), (0, 0, 0), (0, 20, 0)).arm(19, "l", (60, 30, -10), (20, 0, 0))
    a.arm(21, "r", (90, -88, 0), (10, 0, 0), (0, 0, 0))
    a.at(25, body=(-4, 0, 0), head=(30, 0, 0), jaw=(-24, 0, 0))
    a.arm(25, "r", (196, 0, 10), (20, 0, 0)).arm(25, "l", (140, 0, -30), (10, 0, 0))
    a.at(27, body=(0, 0, 0), head=(34, 0, 0))
    a.arm(27, "r", (206, 0, 8), (26, 0, 0))
    a.at(29, body=(-56, 0, 0), head=(14, 0, 0), jaw=(-4, 0, 0))
    a.arm(29, "r", (58, 0, 0), (0, 0, 0)).arm(29, "l", (40, 0, -20), (20, 0, 0))
    a.at(32, body=(-52, 0, 0), head=(16, 0, 0))
    a.arm(32, "r", (52, 0, 4), (6, 0, 0))
    a.legs(7, 50, 90, 30, 56).legs(10, 30, 56, 54, 96, fwd=-1).legs(16, 40, 70).legs(19, 54, 96, 30, 56, fwd=-1) \
        .legs(25, 20, 30, up=0.5).legs(29, 72, 128, fwd=-1).legs(32, 68, 120)
    a.claws(0, 0, "l").claws(7, -16, "l").claws(25, -20, "l").claws(29, 30, "l")
    a.claws(3, 60, "r").claws(36, 60, "r")
    a.sec([(0, 0, 0), (7, -3, -4), (10, 7, 5), (16, -2, 4), (19, 7, -5), (25, -7, 0), (29, 11, 0), (32, 2, 0), (38, 0, 0)])
    a.done()

    # ================= crescent (34): twirl the blade 2-10, diagonal wave 12, rising wave 19, wide sweep 26
    a = mk("crescent", 34)
    a.show("blade", 1, 32)
    a.rot("hand_r", (2, 0, 0, 0), (4, 0, 180, 0), (6, 0, 360, 0), (8, 0, 540, 0), (10, 0, 720, 0), (34, 0, 720, 0))
    a.at(4, body=(-24, -20, 0), head=(24, 12, 0))
    a.arm(4, "r", (70, -40, 40), (20, 0, 0)).arm(4, "l", (40, 20, -10), (20, 0, 0))
    a.at(10, body=(-14, -30, -4), head=(28, 20, 0), jaw=(-12, 0, 0))
    a.arm(10, "r", (176, -40, 0), (10, 0, 0))
    a.at(12, body=(-36, 30, 6), head=(20, -14, 0), jaw=(-20, 0, 0))
    a.arm(12, "r", (66, 46, 0), (0, 0, 0))
    a.arm(14, "r", (42, 56, 0), (10, 0, 0))
    a.at(17, body=(-38, 34, 4), head=(20, -10, 0))
    a.arm(17, "r", (36, 62, 0), (20, 0, 0))
    a.at(19, body=(-14, -30, -6), head=(30, 16, 0), jaw=(-22, 0, 0))
    a.arm(19, "r", (168, -54, 0), (0, 0, 0))
    a.arm(21, "r", (180, -64, 0), (6, 0, 0))
    a.at(24, body=(-28, -46, -4), head=(22, 26, 0))
    a.arm(24, "r", (102, -92, 0), (6, 0, 0)).arm(24, "l", (90, 40, -20), (10, 0, 0))
    a.at(26, body=(-32, 42, 6), head=(20, -20, 0), jaw=(-18, 0, 0))
    a.arm(26, "r", (100, 66, 0), (0, 0, 0)).arm(26, "l", (30, -10, -30), (30, 0, 0))
    a.arm(28, "r", (90, 84, 0), (10, 0, 0))
    a.legs(4, 44, 76).legs(10, 30, 50, up=0.4).legs(12, 34, 60, 56, 100, fwd=-1).legs(19, 24, 40, up=0.6).legs(24, 50, 90, 30, 56) \
        .legs(26, 30, 56, 56, 100, fwd=-1).legs(30, 44, 76)
    a.claws(0, 0, "l").claws(4, -16, "l").claws(26, 20, "l").claws(2, 60, "r").claws(32, 60, "r")
    a.sec([(0, 0, 0), (4, -2, -3), (10, -4, -3), (12, 7, 5), (17, 2, 4), (19, -6, -4), (24, -2, -4), (26, 8, 5), (30, 1, 0), (34, 0, 0)])
    a.done()

    # ================= hairwhip (30): coil 0-8, full SPIN 9-17 (hit 13) with the mane flung out, settle
    a = mk("hairwhip", 30)
    a.rot("root", (0, 0, 0, 0), (8, 0, -12, 0), (9, 0, 0, 0), (11, 0, 100, 0), (13, 0, 200, 0), (15, 0, 290, 0), (17, 0, 350, 0),
          (20, 0, 364, 0), (24, 0, 360, 0), (30, 0, 360, 0))
    a.at(6, body=(-34, -46, -8), head=(26, 30, 0), jaw=(-6, 0, 0))
    a.arms(6, (50, 0, -10), (60, 0, 0), (20, 0, 0))
    a.at(10, body=(-20, 10, 0), head=(26, -10, 0), jaw=(-20, 0, 0))
    a.arms(10, (40, 0, 70), (10, 0, 0), (-10, 0, 0))
    a.at(13, body=(-18, 24, 6), head=(24, -14, 0), jaw=(-22, 0, 0))
    a.arms(13, (30, 0, 84), (6, 0, 0), (-16, 0, 0))
    a.arms(17, (40, 0, 50), (20, 0, 0), (0, 0, 0))
    a.at(18, body=(-30, 10, 0), head=(22, -6, 0), jaw=(-6, 0, 0))
    a.legs(6, 62, 110).legs(10, 30, 50, up=0.8).legs(14, 34, 56, up=0.6).legs(18, 56, 100).legs(24, 46, 80)
    for b, g0 in (("mane0", 1.0), ("mane1", 0.7), ("mane2", 0.5), ("mane3", 0.4)):
        a.rot(b, (0, 0, 0, 0), (6, 6 * g0, -30 * g0, 0), (9, -4 * g0, -10 * g0, 0), (11, -16 * g0, 40 * g0, 0),
              (13, -20 * g0, 58 * g0, 0), (15, -18 * g0, 54 * g0, 0), (17, -10 * g0, 36 * g0, 0),
              (20, 4 * g0, -16 * g0, 0), (24, 2 * g0, 6 * g0, 0), (30, 0, 0, 0))
    for k, s in (("side_r", 1), ("side_l", -1)):
        a.rot(k, (0, 0, 0, 0), (9, 0, 0, 10 * s), (13, -10, 0, 60 * s), (17, -6, 0, 30 * s), (22, 0, 0, -6 * s), (30, 0, 0, 0))
    a.rot("bangs", (0, 0, 0, 0), (13, -14, 0, -14), (20, 4, 0, 6), (30, 0, 0, 0))
    a.rot("ahoge", (0, 0, 0, 0), (13, 30, 0, -30), (19, -20, 0, 14), (24, 6, 0, -4), (30, 0, 0, 0))
    a.claws(6, 50).claws(10, -24, spread=6).claws(17, -10).claws(24, 0)
    a.done()

    # ================= diamonds (32): summon 0-8, right fling 9, left fling 17, both-hand overhead volley 24
    a = mk("diamonds", 32)
    a.rot("sparkles", (0, 0, 0, 0), (4, 0, 200, 0), (8, 0, 400, 0), (9, 0, 440, 0), (16, 0, 620, 0), (17, 0, 660, 0),
          (24, 0, 900, 0), (28, 0, 1000, 0), (32, 0, 1080, 0))
    a.pos("sparkles", (0, 0, 0, 0), (6, 0, 4, 0), (9, 0, 2, -3), (12, 0, 4, 0), (17, 0, 2, -3), (21, 0, 6, 0), (24, 0, 3, -4), (30, 0, 0, 0))
    a.scl("sparkles", (0, 1, 1, 1), (6, 1.6, 1.6, 1.6), (9, 1.2, 1.2, 1.2), (12, 1.6, 1.6, 1.6), (17, 1.2, 1.2, 1.2), (21, 2.0, 2.0, 2.0),
          (24, 1.1, 1.1, 1.1), (32, 1, 1, 1))
    a.at(4, body=(-8, 0, 0), head=(44, 0, 0), jaw=(-10, 0, 0))
    a.arm(4, "l", (176, 0, 16), (10, 0, 0), (-20, 0, 0)).arm(4, "r", (40, 0, 20), (20, 0, 0))
    a.at(7, body=(-14, -24, -4), head=(30, 16, 0))
    a.arm(7, "r", (-40, -10, 36), (40, 0, 0), (30, 0, 0)).arm(7, "l", (150, 0, 20), (10, 0, 0))
    a.at(9, body=(-30, 26, 6), head=(22, -14, 0), jaw=(-16, 0, 0))
    a.arm(9, "r", (112, 30, 0), (0, 0, 0), (-20, 0, 0)).arm(9, "l", (90, 0, 10), (20, 0, 0))
    a.arm(11, "r", (90, 40, 0), (10, 0, 0), (0, 0, 0))
    a.at(15, body=(-14, 24, 4), head=(30, -16, 0), jaw=(-6, 0, 0))
    a.arm(15, "l", (-40, -10, 36), (40, 0, 0), (30, 0, 0)).arm(15, "r", (60, 0, 20), (20, 0, 0))
    a.at(17, body=(-30, -26, -6), head=(22, 14, 0), jaw=(-16, 0, 0))
    a.arm(17, "l", (112, 30, 0), (0, 0, 0), (-20, 0, 0))
    a.arm(19, "l", (90, 40, 0), (10, 0, 0), (0, 0, 0))
    a.at(21, body=(-2, 0, 0), head=(44, 0, 0), jaw=(-28, 0, 0))
    a.arms(21, (192, 0, 22), (10, 0, 0), (-20, 0, 0))
    a.at(24, body=(-42, 0, 0), head=(26, 0, 0), jaw=(-20, 0, 0))
    a.arms(24, (104, 0, 12), (0, 0, 0), (-24, 0, 0))
    a.arms(27, (80, 0, 12), (16, 0, 0), (0, 0, 0))
    a.legs(4, 24, 36, up=0.6).legs(7, 44, 76).legs(9, 30, 56, 54, 96, fwd=-1).legs(15, 44, 76).legs(17, 54, 96, 30, 56, fwd=-1) \
        .legs(21, 20, 30, up=0.8).legs(24, 60, 106).legs(28, 48, 84)
    a.claws(4, -24, spread=8).claws(9, -24, "r", 8).claws(17, -24, "l", 8).claws(24, -24, spread=8).claws(30, 0)
    a.sec([(0, 0, 0), (4, -4, 0), (7, -2, -3), (9, 6, 4), (15, -2, 3), (17, 6, -4), (21, -6, 0), (24, 8, 0), (32, 0, 0)])
    a.done()

    # ================= backflip (32): jab 5, crouch 6, flip 7-17 (claw crescent 13 upside down), land 19, rise
    a = mk("backflip", 32)
    a.rot("pelvis", (0, 0, 0, 0), (7, 0, 0, 0), (9, 70, 0, 0), (11, 150, 0, 0), (13, 220, 0, 0), (15, 295, 0, 0), (17, 350, 0, 0),
          (19, 362, 0, 0), (22, 360, 0, 0), (32, 360, 0, 0))
    a.at(3, body=(-26, -24, 0), head=(22, 14, 0))
    a.arm(3, "r", (-30, -40, 20), (40, 0, 0))
    a.at(5, body=(-34, 24, 4), head=(18, -12, 0), jaw=(-14, 0, 0))
    a.arm(5, "r", (104, 40, 0), (0, 0, 0)).arm(5, "l", (40, 0, 10), (20, 0, 0))
    a.at(7, body=(-40, 0, 0), head=(30, 0, 0))
    a.arms(7, (-30, 0, 20), (30, 0, 0))
    a.at(9, body=(-30, 0, 0), head=(10, 0, 0), jaw=(-20, 0, 0))
    a.arms(11, (200, 0, 22), (10, 0, 0), (-20, 0, 0))
    a.at(13, body=(-44, 0, 0), head=(4, 0, 0), jaw=(-30, 0, 0))
    a.arms(13, (40, 0, 14), (0, 0, 0), (20, 0, 0))
    a.arms(16, (70, 0, 20), (20, 0, 0))
    a.at(17, body=(-30, 0, 0), head=(30, 0, 0), jaw=(-6, 0, 0))
    a.at(19, body=(-56, 0, 0), head=(46, 0, 0))
    a.arms(19, (96, 0, 24), (0, 0, 0), (30, 0, 0))
    a.at(24, body=(-44, 0, 0), head=(34, 0, 0))
    a.arms(24, (70, 0, 16), (14, 0, 0), (16, 0, 0))
    a.legs(5, 46, 80, 34, 60).legs(7, 76, 130).legs(9, 100, 140, up=12).legs(11, 110, 150, up=17).legs(13, 110, 150, up=17) \
        .legs(15, 90, 120, up=13).legs(17, 30, 40, up=4).legs(19, 76, 132).legs(24, 64, 112)
    a.claws(5, 20, "r").claws(11, -24, spread=6).claws(13, 30).claws(19, 50).claws(26, 10)
    a.sec([(0, 0, 0), (5, 4, 3), (7, -4, 0), (9, -10, 0), (13, -8, 0), (17, 6, 0), (19, 8, 0), (24, 2, 0), (32, 0, 0)])
    a.done()

    # ================= scuttle (34): drop flat 0-5, spider skitter 6-21, coil 22, rising UPPERCUT rake 24
    a = mk("scuttle", 34)
    a.at(5, body=(-70, 0, 0), head=(62, 0, 0), jaw=(-10, 0, 0))
    a.arms(5, (96, 0, 34), (-6, 0, 0), (30, 0, 0))
    a.legs(5, 86, 146, spread=24)
    for i, t in enumerate(range(6, 22, 2)):
        ph = 1 if i % 2 else -1
        a.at(t, body=(-72, 8 * ph, 4 * ph), head=(64, -8 * ph, -4 * ph), jaw=(-8 - 4 * (i % 2), 0, 0))
        a.arm(t, "r", (96 + 20 * ph, 0, 34), (-6 - 10 * ph, 0, 0), (30, 0, 0))
        a.arm(t, "l", (96 - 20 * ph, 0, 34), (-6 + 10 * ph, 0, 0), (30, 0, 0))
        a.legs(t, 86 - 12 * ph, 146, 86 + 12 * ph, 146, spread=24)
        a.rot("pelvis", (t, 0, 6 * ph, 3 * ph))
        a.claws(t, 30 if ph > 0 else -10, "r").claws(t, -10 if ph > 0 else 30, "l")
    a.rot("pelvis", (22, 0, 0, 0), (34, 0, 0, 0))
    a.at(22, body=(-74, -16, 0), head=(64, 10, 0), jaw=(-20, 0, 0))
    a.arm(22, "r", (-10, 0, 30), (30, 0, 0), (30, 0, 0)).arm(22, "l", (96, 0, 34), (0, 0, 0))
    a.legs(22, 92, 150, spread=20)
    a.at(24, body=(-4, 22, 6), head=(30, -14, 0), jaw=(-30, 0, 0))
    a.arm(24, "r", (200, 20, 10), (-6, 0, 0), (-20, 0, 0)).arm(24, "l", (-40, 0, 20), (30, 0, 0))
    a.legs(24, 10, 14, up=3, spread=4)
    a.at(26, body=(2, 26, 6), head=(34, -16, 0))
    a.arm(26, "r", (218, 20, 10), (0, 0, 0))
    a.at(29, body=(-40, 0, 0), head=(26, 0, 0), jaw=(-6, 0, 0))
    a.arms(29, (70, 0, 14), (20, 0, 0))
    a.legs(29, 66, 116)
    a.claws(22, 50, "r").claws(24, -26, "r", 8).claws(28, 10)
    a.sec([(0, 0, 0), (5, 6, 0), (8, 6, 3), (12, 6, -3), (16, 6, 3), (20, 6, -3), (22, 2, 0), (24, -10, 0), (27, 4, 0), (34, 0, 0)])
    a.done()

    # ================= catswarm (42): kneel + call the cat 0-8, HISS 9, cat dashes & bites 16/22/28 while Fen directs, recall
    a = mk("catswarm", 42)
    a.show("cat", 3, 40, grow=2)
    a.pos("cat", (0, 0, 0, 0), (8, 0, 0, 0), (10, 0, 3, -6), (13, 2, 2, -14), (16, 0, 0, -22), (19, -3, 3, -20), (22, 2, 0, -28),
          (25, 4, 3, -24), (28, -1, 0, -32), (31, 0, 2, -22), (35, 0, 1, -8), (38, 0, 0, 0), (42, 0, 0, 0))
    a.rot("cat", (0, 0, 0, 0), (8, 10, 0, 0), (10, -30, 0, 0), (13, 10, 0, 0), (16, 20, 0, 0), (19, -20, 20, 0), (22, 20, -10, 0),
          (25, -20, -20, 0), (28, 20, 10, 0), (31, -10, 180, 0), (35, 0, 180, 0), (38, 0, 360, 0), (42, 0, 360, 0))
    a.rot("cattail", (0, 0, 0, 0), (6, 20, 20, 0), (9, -30, 0, 0), (14, 10, -20, 0), (18, -10, 20, 0), (22, 10, -20, 0), (26, -10, 20, 0),
          (30, 10, -20, 0), (36, 20, 0, 0), (42, 0, 0, 0))
    a.rot("cathead", (0, 0, 0, 0), (9, 20, 0, 0), (16, -20, 0, 0), (22, -20, 0, 0), (28, -20, 0, 0), (32, 0, 0, 0), (42, 0, 0, 0))
    a.at(5, body=(-50, 10, 0), head=(30, 20, 10), jaw=(-4, 0, 0))
    a.arm(5, "l", (70, 0, -20), (10, 0, 0), (20, 0, 0)).arm(5, "r", (30, 0, 10), (20, 0, 0))
    a.legs(5, 70, 124, 40, 70)
    a.at(9, body=(-30, 0, 0), head=(36, 0, 0), jaw=(-40, 0, 0))
    a.arms(9, (40, 0, 60), (20, 0, 0), (-20, 0, 0))
    a.legs(9, 50, 90)
    a.at(13, body=(-28, 0, 0), head=(26, 0, 0), jaw=(-14, 0, 0))
    a.arm(14, "r", (60, -30, 20), (40, 0, 0))
    a.at(16, body=(-34, 18, 0), head=(22, -10, 0), jaw=(-24, 0, 0))
    a.arm(16, "r", (112, 10, 0), (0, 0, 0), (-20, 0, 0)).arm(16, "l", (40, 0, 20), (20, 0, 0))
    a.arm(19, "r", (60, 0, 10), (20, 0, 0)).arm(20, "l", (60, -30, 20), (40, 0, 0))
    a.at(22, body=(-34, -18, 0), head=(22, 10, 0), jaw=(-24, 0, 0))
    a.arm(22, "l", (112, 10, 0), (0, 0, 0), (-20, 0, 0))
    a.at(26, body=(-20, 0, 0), head=(30, 0, 0), jaw=(-10, 0, 0))
    a.arms(26, (150, -30, 20), (20, 0, 0))
    a.at(28, body=(-42, 0, 0), head=(20, 0, 0), jaw=(-34, 0, 0))
    a.arms(28, (100, 30, 0), (0, 0, 0), (-20, 0, 0))
    a.at(30, body=(-40, 0, 0), head=(24, 0, 0), jaw=(-20, 0, 0))
    a.arms(30, (96, 0, 10), (0, 0, 0), (-30, 0, 0))
    a.arms(34, (50, 0, 10), (20, 0, 0))
    a.legs(13, 40, 70).legs(16, 34, 60, 54, 96, fwd=-0.6).legs(22, 54, 96, 34, 60, fwd=-0.6).legs(28, 60, 106, fwd=-1).legs(34, 44, 76)
    a.claws(5, -10, "l").claws(9, -26, spread=8).claws(16, -20, "r").claws(22, -20, "l").claws(28, -24, spread=6).claws(36, 0)
    a.sec([(0, 0, 0), (5, 4, 2), (9, -6, 0), (16, 5, 3), (22, 5, -3), (26, -4, 0), (28, 7, 0), (34, 1, 0), (42, 0, 0)])
    a.done()

    # ================= maul (44): gape 0-5, lunge BITE 7 + grab, lift/slam 14, 23, 32, wind 35, FLING 37
    a = mk("maul", 44)
    a.at(4, body=(-40, 0, 0), head=(40, 0, 0), jaw=(-48, 0, 0))
    a.arms(4, (84, 0, 40), (0, 0, 0), (-20, 0, 0))
    a.at(6, body=(-50, 0, 0), head=(34, 0, 0), jaw=(-54, 0, 0))
    a.at(7, body=(-56, 0, 0), head=(14, 0, 0), jaw=(0, 0, 0))
    a.arms(7, (104, 0, 4), (10, 0, 0), (10, 0, 0))
    for t0, t1, big in ((9, 14, 1.0), (18, 23, 1.0), (27, 32, 1.3)):
        a.at(t0 + 2, body=(-14, 0, 0), head=(30, 0, 0), jaw=(-10, 0, 0))
        a.arms(t0 + 2, (168, 0, 8), (20, 0, 0), (10, 0, 0))
        a.legs(t0 + 2, 26, 40, up=0.6)
        a.at(t1, body=(-56 - 6 * (big - 1) * 10, 0, 0), head=(12, 0, 0), jaw=(-26 * big, 0, 0))
        a.arms(t1, (62, 0, 6), (6, 0, 0), (24, 0, 0))
        a.legs(t1, 70, 124)
        a.at(t1 + 2, body=(-50, 0, 0), head=(16, 0, 0), jaw=(-8, 0, 0))
    a.at(35, body=(-36, -50, -6), head=(24, 30, 0), jaw=(-10, 0, 0))
    a.arms(35, (94, -72, 0), (20, 0, 0), (0, 0, 0), al=(80, 60, 0))
    a.at(37, body=(-30, 46, 6), head=(20, -24, 0), jaw=(-30, 0, 0))
    a.arms(37, (100, 66, 0), (0, 0, 0), (-10, 0, 0), al=(100, -50, 0))
    a.arms(40, (70, 40, 10), (16, 0, 0), al=(60, -20, 0))
    a.legs(4, 50, 90).legs(7, 30, 56, 64, 110, fwd=-1.5).legs(35, 56, 100).legs(37, 30, 56, 60, 106).legs(40, 44, 76)
    a.claws(4, -24, spread=8).claws(7, 60).claws(34, 60).claws(37, -26, spread=8).claws(41, 0)
    a.sec([(0, 0, 0), (4, -3, 0), (7, 8, 0), (11, -6, 0), (14, 8, 0), (20, -6, 0), (23, 8, 0), (29, -6, 0), (32, 10, 0), (35, 0, -5),
           (37, 6, 6), (44, 0, 0)])
    a.done()

    # ================= frenzy (48): ROAR 0-6, six alternating slashes 10..35, X-finisher 42
    a = mk("frenzy", 48)
    a.at(3, body=(4, 0, 0), head=(50, 0, 0), jaw=(-50, 0, 0))
    a.arms(3, (20, 0, 80), (10, 0, 0), (-20, 0, 0))
    a.legs(3, 20, 30, up=0.6, spread=6)
    a.at(6, body=(2, 0, 0), head=(52, 4, 4), jaw=(-52, 0, 0))
    a.claws(3, -28, spread=10).claws(7, 0)
    for i in range(6):
        pk = 10 + 5 * i
        k, o = ("r", "l") if i % 2 == 0 else ("l", "r")
        s = 1 if k == "r" else -1
        a.arm(pk - 3, k, (124, -76, 0), (10, 0, 0), (-20, 0, 0))
        a.at(pk - 3, body=(-30, -26 * s, -5 * s), head=(22, 16 * s, 0), jaw=(-18, 0, 0))
        a.arm(pk, k, (108, 52, 0), (0, 0, 0), (10, 0, 0))
        a.arm(pk, o, (60, 20, 0), (24, 0, 0), (0, 0, 0))
        a.at(pk, body=(-36, 30 * s, 6 * s), head=(18, -14 * s, 0), jaw=(-26, 0, 0))
        if k == "r": a.legs(pk, 30, 56, 54, 96, fwd=-0.6)
        else: a.legs(pk, 54, 96, 30, 56, fwd=-0.6)
        a.claws(pk - 3, -20, k).claws(pk, 24, k)
    a.at(39, body=(-4, 0, 0), head=(38, 0, 0), jaw=(-40, 0, 0))
    a.arms(39, (200, 0, 30), (14, 0, 0), (-16, 0, 0))
    a.legs(39, 20, 30, up=0.6)
    a.at(42, body=(-58, 0, 0), head=(14, 0, 0), jaw=(-20, 0, 0))
    a.arms(42, (78, 40, 0), (0, 0, 0), (20, 0, 0))
    a.legs(42, 74, 128)
    a.at(45, body=(-52, 0, 0), head=(18, 0, 0), jaw=(-6, 0, 0))
    a.arms(45, (70, 36, 0), (14, 0, 0))
    a.claws(39, -26, spread=10).claws(42, 40).claws(46, 20)
    sk = [(0, 0, 0), (3, -8, 0)] + [(10 + 5 * i, 7, 5 if i % 2 == 0 else -5) for i in range(6)] + [(39, -8, 0), (42, 11, 0), (48, 0, 0)]
    a.sec(sk)
    a.done()

    # ================= howl (36): crouch 0-8, rear up 11-13, HOWL shock 14 (sustain), 2nd pulse 24, drop back
    a = mk("howl", 36)
    a.at(6, body=(-50, 0, 0), head=(-6, 0, 0), jaw=(-6, 0, 0))
    a.arms(6, (86, 0, 20), (0, 0, 0), (30, 0, 0))
    a.legs(6, 70, 124)
    a.at(9, body=(-56, 0, 0), head=(-10, 0, 0), jaw=(-10, 0, 0))
    a.at(12, body=(8, 0, 0), head=(56, 0, 0), jaw=(-46, 0, 0))
    a.arms(12, (-24, 0, 50), (20, 0, 0), (-20, 0, 0))
    a.legs(12, 18, 26, up=0.6)
    for t, j in ((14, 1), (16, -1), (18, 1), (20, -1), (22, 1)):
        a.at(t, body=(10 + j, 2 * j, 0), head=(62 + 2 * j, 3 * j, 2 * j), jaw=(-52 + 2 * j, 0, 0))
    a.arms(14, (-30, 0, 60), (16, 0, 0), (-24, 0, 0)).arms(22, (-26, 0, 56), (20, 0, 0))
    a.at(24, body=(12, 0, 0), head=(66, 0, 0), jaw=(-54, 0, 0))
    a.arms(24, (-36, 0, 72), (10, 0, 0), (-26, 0, 0))
    a.legs(24, 14, 20, up=0.8)
    a.at(28, body=(-34, 0, 0), head=(26, 0, 0), jaw=(-8, 0, 0))
    a.arms(28, (50, 0, 14), (20, 0, 0), (10, 0, 0))
    a.legs(28, 56, 100)
    a.claws(6, 50).claws(12, -26, spread=10).claws(26, -26, spread=10).claws(30, 10)
    a.sec([(0, 0, 0), (6, 4, 0), (9, 5, 0), (12, -12, 0), (14, -10, 2), (16, -12, -2), (18, -10, 2), (20, -12, -2), (24, -14, 0),
           (28, 6, 0), (36, 0, 0)])
    a.done()

    # ================= clawspikes (40): rear up claws high 0-12, SLAM into the ground 14, rip claws forward 16-31, pull out
    a = mk("clawspikes", 40)
    a.at(6, body=(0, 0, 0), head=(36, 0, 0), jaw=(-30, 0, 0))
    a.arms(6, (186, 0, 16), (10, 0, 0), (-20, 0, 0))
    a.legs(6, 18, 26, up=0.6)
    a.at(11, body=(8, 0, 0), head=(40, 0, 0), jaw=(-36, 0, 0))
    a.arms(11, (212, 0, 22), (20, 0, 0), (-26, 0, 0))
    a.legs(11, 14, 20, up=1.0)
    a.at(14, body=(-66, 0, 0), head=(30, 0, 0), jaw=(-14, 0, 0))
    a.arms(14, (78, 0, 10), (0, 0, 0), (40, 0, 0))
    a.legs(14, 78, 136)
    for i, t in enumerate(range(16, 32, 3)):
        j = 1 if i % 2 else -1
        a.at(t, body=(-64 + 2 * j, 3 * j, 2 * j), head=(32, -4 * j, 0), jaw=(-12 - 4 * (i % 2), 0, 0))
        a.arms(t, (84 + 6 * j, 0, 10), (0, 0, 0), (36, 0, 0), al=(84 - 6 * j, 0, 10))
        a.legs(t, 76, 132)
    a.at(34, body=(-24, 0, 0), head=(24, 0, 0), jaw=(-4, 0, 0))
    a.arms(34, (124, 0, 20), (20, 0, 0), (-10, 0, 0))
    a.legs(34, 40, 70)
    a.claws(6, -26, spread=10).claws(12, -26, spread=10).claws(14, 46).claws(31, 46).claws(34, -10).claws(38, 0)
    a.sec([(0, 0, 0), (6, -6, 0), (11, -8, 0), (14, 12, 0), (17, 4, 2), (22, 4, -2), (28, 4, 2), (34, -4, 0), (40, 0, 0)])
    a.done()

    # ================= death (40): stagger back, knees buckle, collapse face-down, hair spills, last claw twitch
    a = mk("death", 40)
    a.at(6, body=(0, 10, 6), head=(46, -10, 10), jaw=(-30, 0, 0))
    a.arms(6, (-20, 0, 40), (30, 0, 0), (-20, 0, 0), al=(30, 0, 50))
    a.legs(6, 20, 30, setpos=False)
    a.at(14, body=(-30, 4, 0), head=(-10, 0, -10), jaw=(-20, 0, 0))
    a.arms(14, (20, 0, 20), (30, 0, 0))
    a.legs(14, 90, 160, setpos=False)
    a.rot("pelvis", (0, 0, 0, 0), (14, 0, 0, 0), (20, -40, 0, 0), (26, -78, 0, 6), (40, -80, 0, 6))
    a.pos("pelvis", (0, 0, -drop(40, 70), 0), (14, 0, -6, 0), (20, 0, -7, -2), (26, 0, -10, -4), (40, 0, -10.5, -4))
    a.at(26, body=(-6, 0, 0), head=(20, 20, 20), jaw=(-10, 0, 0))
    a.arms(26, (150, 0, 34), (0, 0, 0), (10, 0, 0), al=(140, 10, 40))
    a.legs(26, 30, 20, setpos=False)
    a.at(40, body=(-4, 0, 0), head=(18, 22, 22), jaw=(-12, 0, 0))
    a.arms(40, (156, 0, 36), (0, 0, 0), (14, 0, 0), al=(144, 10, 42))
    a.claws(26, 0).claws(32, 30, "r").claws(34, -10, "r").claws(36, 20, "r").claws(40, 20)
    a.sec([(0, 0, 0), (6, -8, 0), (14, 6, 0), (20, 8, 0), (26, 4, 0), (40, 0, 0)])
    a.done()


def main():
    B = Builder("fen", 1.0, False, 8)
    build(B)
    anims(B)
    B.m.save(os.path.join(DIR, "fen.bbmodel"))
    print("cubes", len(B.m.cubes), "anims", [a["name"] for a in B.m.anims])


if __name__ == "__main__":
    main()
