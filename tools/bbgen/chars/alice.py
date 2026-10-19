"""Alice (normal) - generates BOTH assets/fpe/bbmodels/alice.bbmodel (phase 1) and alice_boss.bbmodel (phase 2).
References: docs/ref/confirmed/alice_phase1.jpg / alice_phase2.jpg.
Phase 1: tall slim girl, messy brown hair + long arching ahoge, tilted spiky BLACK crown, half-lidded yellow eyes (right eye
under the bangs), blush, small frown, black earrings, grey turtleneck dress to the ankles with black belt, necklace with a
yellow warning-triangle pendant, long open black coat with long sleeves, pointed black heeled boots.
Her powers are shadow: black spike "wings", shadow claws and a shadow whip burst out of her for attacks.
Phase 2 (boss): the same silhouette scaled to a 6.5-block giant and gone PITCH BLACK - glowing yellow slit eyes and a huge
glowing grin, spines bursting from the shoulders, huge hooked claws, ragged spiked coat/dress hem, a long tail and four
back tentacles. Phase 2 also has a QUADRUPED stance (anims_quad: quad_idle / quad_walk loops, drop_down / rise_up transitions,
quad_* attacks) - lowered root, pitched torso, splayed bent arms planted on the claws.
Blockbench space: Y up, ground 0, faces -Z. Character's RIGHT = +X.
Rotation signs (file values): arm/leg rx>0 = swing forward, torso/head rx>0 = lean back / look up,
ry>0 = turn to the character's left, rz>0 = hanging part swings toward +X (character's right).
Run: python3 tools/bbgen/chars/alice.py
"""
import math, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from bbgen import Model, mix  # noqa: E402

DIR = os.path.join(os.path.dirname(__file__), "../../../src/main/resources/assets/fpe/bbmodels/")
HIDE = (.001, .001, .001)


# ================================================================== palettes
class Pal:
    pass


P1 = Pal()
P1.HAIR, P1.HAIR_D, P1.HAIR_HI = 0x5E4033, 0x3F2B23, 0x7D5A48
P1.SKIN, P1.SKIN_D, P1.SKIN_L = 0xEFD9CB, 0xCFB2A3, 0xF7E9DF
P1.BLUSH = 0xE39092
P1.EYE, P1.EYE_D, P1.LID = 0xF0C24E, 0xB8862A, 0x2A1D19
P1.DRESS, P1.DRESS_D, P1.DRESS_HI = 0x4B4A52, 0x37363D, 0x5E5D66
P1.COAT, P1.COAT_D, P1.COAT_HI = 0x1E1E23, 0x121215, 0x2E2E36
P1.BOOT, P1.BOOT_HI = 0x141417, 0x2A2A31
P1.CROWN, P1.CROWN_HI = 0x17171B, 0x34343D
P1.GOLD, P1.GOLD_D = 0xF2B65E, 0xB07A2C
P1.SHADOW, P1.SHADOW_HI = 0x0B0A10, 0x3B3150
P1.GLOW = 0xFFD45A
P1.MOUTH = 0x5A3530

P2 = Pal()
P2.HAIR, P2.HAIR_D, P2.HAIR_HI = 0x1F1714, 0x0F0B0A, 0x33261F
P2.SKIN, P2.SKIN_D, P2.SKIN_L = 0x121216, 0x08080A, 0x1E1E25
P2.BLUSH = 0x1A1418
P2.EYE, P2.EYE_D, P2.LID = 0xFFD25A, 0xE09A2A, 0x050506
P2.DRESS, P2.DRESS_D, P2.DRESS_HI = 0x18181D, 0x0C0C0F, 0x26262E
P2.COAT, P2.COAT_D, P2.COAT_HI = 0x0E0E11, 0x060607, 0x1C1C22
P2.BOOT, P2.BOOT_HI = 0x09090B, 0x1A1A20
P2.CROWN, P2.CROWN_HI = 0x0A0A0C, 0x22222A
P2.GOLD, P2.GOLD_D = 0xD9A04E, 0x8E6224
P2.SHADOW, P2.SHADOW_HI = 0x0A0A0D, 0x22202A
P2.GLOW = 0xFFD45A
P2.MOUTH = 0x050506
P2.CLAW, P2.CLAW_HI = 0x16161C, 0x4A4A5A


# ================================================================== builder
class Builder:
    def __init__(self, name, K, boss, S):
        self.m = Model(name, S=S, atlas=2048)
        self.K, self.boss = K, boss
        self.C = P2 if boss else P1
        self.R = self.m.rng

    def sc(self, v):
        return tuple(x * self.K for x in v)

    def g(self, name, origin, parent=None, rot=(0, 0, 0)):
        return self.m.group(name, self.sc(origin), rot=rot, parent=parent)

    def c(self, name, parent, frm, to, color, origin=None, rot=(0, 0, 0), **kw):
        return self.m.cube(name, parent, self.sc(frm), self.sc(to), color, origin=self.sc(origin) if origin else None, rot=rot, **kw)

    # ------------------------------------------------------------ painters
    def strands(self, base, hi, dark, ink=None):
        R = self.R

        def f(F):
            cols = [R.random() for _ in range(F.w)]
            for x in range(F.w):
                c = mix(base, hi, 0.6) if cols[x] > 0.85 else mix(base, dark, 0.6) if cols[x] < 0.2 else base
                for y in range(F.h):
                    F.px(x, y, mix(c, dark, 0.4 * (y / max(1, F.h - 1))))
            if ink and F.w >= 4 and F.h >= 6:
                for _ in range(max(1, F.w // 10)):
                    x = R.randint(1, F.w - 2)
                    for y in range(R.randint(0, F.h // 3), F.h - 1):
                        F.px(x, y, ink)
        return f

    def folds(self, base, dark, light, n=3):
        R = self.R

        def f(F):
            for y in range(F.h):
                for x in range(F.w):
                    F.px(x, y, mix(base, dark, 0.25 * (y / max(1, F.h - 1))))
            for i in range(n):
                x = int((i + 0.5) * F.w / n) + R.randint(-1, 1)
                for y in range(F.h):
                    if R.random() < 0.85:
                        F.px(x, y, mix(base, dark, 0.5)); F.px(x + 1, y, mix(base, light, 0.4))
        return f

    def edges(self, col):
        return lambda F: (F.rect(0, 0, 1, F.h, col), F.rect(F.w - 1, 0, 1, F.h, col))

    def all(self, fn, skip=()):
        return {k: fn for k in ("north", "south", "east", "west", "up", "down") if k not in skip}

    def lock(self, name, parent, base, ln, w, d, rot, col, tip=None, paint=None):
        """tapered blade hanging DOWN (-Y) from `base` (no 180-degree flips)"""
        x, y, z = base
        fc = self.all(paint) if paint else None
        self.c(name, parent, (x - w / 2, y - ln * 0.5, z - d / 2), (x + w / 2, y, z + d / 2), col, origin=base, rot=rot, faces=fc)
        self.c(name + "m", parent, (x - w * 0.33, y - ln * 0.8, z - d * 0.4), (x + w * 0.33, y - ln * 0.45, z + d * 0.4), col, origin=base, rot=rot, faces=fc)
        self.c(name + "t", parent, (x - w * 0.15, y - ln, z - d * 0.3), (x + w * 0.15, y - ln * 0.76, z + d * 0.3), tip or col, origin=base, rot=rot)

    # ------------------------------------------------------------ generic tapered blade (spike / hair lock / claw / crown point)
    def blade(self, name, parent, base, ln, w, d, rot, col, tip=None, paint=None):
        x, y, z = base
        fc = self.all(paint) if paint else None
        self.c(name, parent, (x - w / 2, y, z - d / 2), (x + w / 2, y + ln * 0.5, z + d / 2), col, origin=base, rot=rot, faces=fc)
        self.c(name + "m", parent, (x - w * 0.33, y + ln * 0.45, z - d * 0.4), (x + w * 0.33, y + ln * 0.8, z + d * 0.4), col,
               origin=base, rot=rot, faces=fc)
        self.c(name + "t", parent, (x - w * 0.15, y + ln * 0.76, z - d * 0.3), (x + w * 0.15, y + ln, z + d * 0.3), tip or col,
               origin=base, rot=rot)


# ================================================================== face painters
def face_p1(C):
    def f(F):
        W, H = F.w, F.h
        for y in range(H):
            for x in range(W):
                F.px(x, y, mix(C.SKIN, C.SKIN_D, max(0, (0.3 - y / H) / 0.3) * 0.7))
        # eyes: half-lidded, heavy upper lid, yellow iris, slit pupil (her right = texture-left, under the bangs)
        for cx in (0.3 * W, 0.7 * W):
            ey = 0.52 * H
            ew = 0.13 * W
            F.poly([(cx - ew, ey), (cx + ew, ey - 0.02 * H), (cx + ew * 0.8, ey + 0.08 * H), (cx - ew * 0.8, ey + 0.08 * H)], C.EYE)
            F.rect(cx - ew * 0.2, ey, max(1, W * 0.04), 0.08 * H, C.EYE_D)
            F.line(cx - ew * 1.15, ey - 0.005 * H, cx + ew * 1.15, ey - 0.03 * H, C.LID, max(1.5, W * 0.045))
            F.line(cx + ew * 1.1, ey - 0.03 * H, cx + ew * 1.4, ey - 0.07 * H, C.LID, 1)
            F.line(cx - ew * 0.7, ey + 0.1 * H, cx + ew * 0.7, ey + 0.1 * H, C.SKIN_D, 1)
            F.line(cx - ew, ey - 0.12 * H, cx + ew, ey - 0.14 * H, C.HAIR_D, 1)  # brow
        for cx in (0.2 * W, 0.8 * W):  # blush
            F.disc(cx, 0.7 * H, 0.09 * W, mix(C.SKIN, C.BLUSH, 0.75))
            F.disc(cx, 0.7 * H, 0.05 * W, C.BLUSH)
        F.line(0.5 * W, 0.62 * H, 0.52 * W, 0.68 * H, C.SKIN_D, 1)  # nose
        # small frown
        F.line(0.43 * W, 0.83 * H, 0.57 * W, 0.83 * H, C.MOUTH, 1.3)
        F.px(int(0.42 * W), int(0.85 * H), C.MOUTH); F.px(int(0.58 * W), int(0.85 * H), C.MOUTH)
    return f


def face_p2(C):
    def f(F):
        W, H = F.w, F.h
        for y in range(H):
            for x in range(W):
                F.px(x, y, mix(C.SKIN_L, C.SKIN, y / H))
        # glowing slanted slit eyes
        for cx, s in ((0.3 * W, 1), (0.7 * W, -1)):
            ey = 0.42 * H
            F.poly([(cx - 0.17 * W, ey - s * 0.0 * H - (0.04 * H if s < 0 else 0)), (cx + 0.15 * W, ey - (0.04 * H if s > 0 else 0)),
                    (cx + 0.12 * W, ey + 0.09 * H), (cx - 0.12 * W, ey + 0.09 * H)], C.EYE, glow=True)
            F.rect(cx - 0.02 * W, ey - 0.02 * H, max(1, 0.04 * W), 0.07 * H, C.EYE_D, glow=True)
        # huge grin, crescent from cheek to cheek
        pts_top = [(0.1 * W + i * 0.08 * W, 0.66 * H - 0.11 * H * math.sin(math.pi * i / 10) * -0.4 - (0.06 * H if i in (0, 10) else 0)) for i in range(11)]
        pts_bot = [(0.9 * W - i * 0.08 * W, 0.7 * H + 0.16 * H * math.sin(math.pi * i / 10)) for i in range(11)]
        F.poly(pts_top + pts_bot, C.EYE, glow=True)
        for i in range(1, 12):  # teeth gaps
            x = 0.12 * W + i * 0.065 * W
            F.line(x, 0.64 * H, x, 0.84 * H, C.MOUTH, 1)
        F.line(0.12 * W, 0.73 * H, 0.88 * W, 0.73 * H, C.MOUTH, 1)
    return f


def pendant_paint(C):
    def f(F):
        W, H = F.w, F.h
        F.rect(0, 0, W, H, C.DRESS)
        F.poly([(W / 2, 0), (W, H), (0, H)], C.GOLD_D)
        F.poly([(W / 2, 1.5), (W - 1.6, H - 0.8), (1.6, H - 0.8)], C.GOLD)
        F.rect(W / 2 - 0.6, H * 0.3, 1.4, H * 0.38, C.LID)
        F.rect(W / 2 - 0.6, H * 0.76, 1.4, 1.2, C.LID)
    return f


# ================================================================== model
def build(B):
    C, K, boss = B.C, B.K, B.boss
    g, c, blade = B.g, B.c, B.blade
    st = B.strands(C.HAIR, C.HAIR_HI, C.HAIR_D, ink=C.HAIR_D)
    st_plain = B.strands(C.HAIR, C.HAIR_HI, C.HAIR_D)

    # ---------------- skeleton
    g("root", (0, 0, 0))
    g("body", (0, 14, 0), "root")
    for k, o in (("dress_f", (0, 19, -1.45)), ("dress_b", (0, 19, 1.45)), ("dress_r", (2.3, 19, 0)), ("dress_l", (-2.3, 19, 0))):
        g(k, o, "body")
    g("chest", (0, 19, 0), "body")
    g("coat_b", (0, 12, 1.6), "chest")
    g("coat_r", (2.4, 12, -0.6), "chest")
    g("coat_l", (-2.4, 12, -0.6), "chest")
    g("pendant", (0, 25.2, -1.6), "chest")
    g("head", (0, 27.2, 0), "chest")
    g("hair_b", (0, 31, 2.2), "head")
    g("hair_r", (2.6, 31, 0), "head")
    g("hair_l", (-2.6, 31, 0), "head")
    g("bangs", (0, 32.4, -2.8), "head")
    g("crown", (0, 34.2, 0), "head", rot=(0, 0, -8))
    g("ah0", (0.4, 34.3, 0.2), "head", rot=(10, 0, -24))
    g("ah1", (0.4, 37.0, 0.2), "ah0", rot=(0, 0, -40))
    g("ah2", (0.4, 39.4, 0.2), "ah1", rot=(0, 0, -50))
    g("wings", (0, 23.5, 1.7), "chest")
    for i in range(3):
        g(f"wing_r{i}", (0.8, 23.5 - i * 1.2, 1.7), "wings")
        g(f"wing_l{i}", (-0.8, 23.5 - i * 1.2, 1.7), "wings")
    if boss:
        g("arm_r", (3.3, 25, 0), "chest"); g("fore_r", (3.3, 17.8, 0), "arm_r"); g("hand_r", (3.3, 10.6, 0), "fore_r")
        g("arm_l", (-3.3, 25, 0), "chest"); g("fore_l", (-3.3, 17.8, 0), "arm_l"); g("hand_l", (-3.3, 10.6, 0), "fore_l")
    else:
        g("arm_r", (3.3, 25, 0), "chest"); g("fore_r", (3.3, 20.0, 0), "arm_r"); g("hand_r", (3.3, 14.8, 0), "fore_r")
        g("arm_l", (-3.3, 25, 0), "chest"); g("fore_l", (-3.3, 20.0, 0), "arm_l"); g("hand_l", (-3.3, 14.8, 0), "fore_l")
    for s, k in ((1, "r"), (-1, "l")):
        g("leg_" + k, (1.1 * s, 14, 0), "root")
        g("shin_" + k, (1.1 * s, 7.6, 0), "leg_" + k)
        g("foot_" + k, (1.1 * s, 2.4, 0), "shin_" + k)

    # ---------------- legs: black tights, pointed heeled boots
    for s, k in ((1, "r"), (-1, "l")):
        x = 1.1 * s
        c("thigh_" + k, "leg_" + k, (x - 0.9, 7.4, -0.85), (x + 0.9, 14.4, 0.85), C.BOOT, color2=C.COAT_D, grad=True)
        c("calf_" + k, "shin_" + k, (x - 0.8, 2.4, -0.8), (x + 0.8, 7.8, 0.8), C.BOOT, faces={"north": B.edges(C.BOOT_HI)})
        c("boot_" + k, "foot_" + k, (x - 0.95, 0.4, -1.1), (x + 0.95, 3.4, 1.0), C.BOOT, faces={"north": B.edges(C.BOOT_HI), "up": lambda F: F.rect(0, 0, F.w, F.h, C.BOOT_HI)})
        c("toe_" + k, "foot_" + k, (x - 0.6, 0, -3.2), (x + 0.6, 1.1, -0.9), C.BOOT, origin=(x, 0.4, -1.0), rot=(-4, 0, 0))
        c("toetip_" + k, "foot_" + k, (x - 0.3, 0, -4.2), (x + 0.3, 0.7, -3.0), C.BOOT_HI, origin=(x, 0.4, -1.0), rot=(-4, 0, 0))
        c("heel_" + k, "foot_" + k, (x - 0.4, 0, 0.5), (x + 0.4, 1.4, 1.2), C.BOOT_HI)
        if boss:
            for i, ry in enumerate((-30, 0, 30)):
                blade(f"fclaw_{k}{i}", "foot_" + k, (x + i * 0.5 - 0.5, 0.3, -2.6), 2.6, 0.5, 0.35, (-95, ry, 0), C.BOOT, C.SHADOW_HI)

    # ---------------- hips + long grey dress (A-line panels)
    c("hips", "body", (-2.1, 13.4, -1.3), (2.1, 19, 1.3), C.DRESS_D)
    dl = 1.6
    dpaint = B.folds(C.DRESS, C.DRESS_D, C.DRESS_HI, 3)
    c("dr_front", "dress_f", (-2.5, dl, -1.65), (2.5, 19.2, -1.25), C.DRESS, origin=(0, 19, -1.45), rot=(5, 0, 0),
      faces={"north": dpaint, "south": dpaint})
    c("dr_back", "dress_b", (-2.5, dl, 1.25), (2.5, 19.2, 1.65), C.DRESS, origin=(0, 19, 1.45), rot=(-5, 0, 0),
      faces={"north": dpaint, "south": dpaint})
    c("dr_right", "dress_r", (2.1, dl, -1.6), (2.5, 19.2, 1.6), C.DRESS, origin=(2.3, 19, 0), rot=(0, 0, 5), faces={"east": dpaint})
    c("dr_left", "dress_l", (-2.5, dl, -1.6), (-2.1, 19.2, 1.6), C.DRESS, origin=(-2.3, 19, 0), rot=(0, 0, -5), faces={"west": dpaint})
    for i, (x, z, ry) in enumerate([(2.2, -1.45, 45), (-2.2, -1.45, -45), (2.2, 1.45, -45), (-2.2, 1.45, 45)]):
        bone = "dress_f" if z < 0 else "dress_b"
        sx, sz = (1 if x > 0 else -1), (1 if z > 0 else -1)
        c(f"dr_corner{i}", bone, (x - 0.7, dl + 0.3, z - 0.2), (x + 0.7, 19.0, z + 0.2), C.DRESS_D, origin=(x, 19, z), rot=(-sz * 5, ry, sx * 5))
    c("dr_slit", "dress_f", (0.9, dl, -1.75), (1.1, 9.0, -1.6), C.DRESS_D, origin=(0, 19, -1.45), rot=(5, 0, 0))  # slit seam (art: leg shows)
    if boss:  # ragged dress hem
        for i in range(7):
            x = -2.3 + i * 0.77
            blade(f"drag_f{i}", "dress_f", (x, dl + 0.4, -1.5), 2.2 + (i % 3) * 0.7, 0.7, 0.3, (180 - 12, 0, (i - 3) * 6), C.DRESS, C.DRESS_D)
            blade(f"drag_b{i}", "dress_b", (x, dl + 0.4, 1.5), 2.0 + ((i + 1) % 3) * 0.7, 0.7, 0.3, (180 + 12, 0, (i - 3) * 6), C.DRESS, C.DRESS_D)

    # ---------------- torso: grey turtleneck, black belt, pendant
    def torso_front(F):
        B.folds(C.DRESS, C.DRESS_D, C.DRESS_HI, 2)(F)
        W, H = F.w, F.h
        F.line(0.3 * W, 0, 0.47 * W, 0.24 * H, C.LID, 1)  # necklace cord
        F.line(0.7 * W, 0, 0.53 * W, 0.24 * H, C.LID, 1)
    c("waist", "chest", (-2.0, 18.6, -1.25), (2.0, 20.8, 1.25), C.DRESS, faces={"north": B.folds(C.DRESS, C.DRESS_D, C.DRESS_HI, 2)})
    c("belt", "chest", (-2.15, 18.8, -1.4), (2.15, 19.8, 1.4), C.COAT_D, faces=B.all(lambda F: F.rect(0, 0, F.w, 1, C.COAT_HI)))
    c("buckle", "chest", (-0.6, 18.7, -1.6), (0.6, 19.9, -1.38), C.COAT_HI, faces={"north": lambda F: F.rect(2, 2, F.w - 4, F.h - 4, C.COAT_D)})
    c("torso", "chest", (-2.4, 20.6, -1.35), (2.4, 25.2, 1.35), C.DRESS, faces={"north": torso_front, "south": B.folds(C.DRESS, C.DRESS_D, C.DRESS_HI, 2)})
    c("bust", "chest", (-2.1, 21.6, -1.6), (2.1, 23.4, -1.3), C.DRESS, faces={"north": B.folds(C.DRESS, C.DRESS_D, C.DRESS_HI, 2)})
    c("collar", "chest", (-1.35, 25.0, -1.25), (1.35, 27.6, 1.25), C.DRESS,
      faces=B.all(lambda F: [F.rect(0, int(F.h * q), F.w, 1, C.DRESS_D) for q in (0.3, 0.55, 0.8)], skip=("up", "down")))
    c("collar_fold", "chest", (-1.5, 26.6, -1.4), (1.5, 27.5, 1.4), C.DRESS_HI)
    c("pend_plate", "pendant", (-1.05, 22.4, -1.82), (1.05, 24.3, -1.62), C.GOLD, faces={"north": pendant_paint(C)},
      glow=False)
    if boss:
        c("pend_glow", "pendant", (-0.3, 23.0, -1.86), (0.3, 23.4, -1.8), C.GLOW, glow=True)

    # ---------------- coat: open, long, standing collar; lower panels on their own bones for flutter
    cp = B.folds(C.COAT, C.COAT_D, C.COAT_HI, 2)
    c("coat_sh", "chest", (-3.15, 24.0, -1.65), (3.15, 25.9, 1.65), C.COAT, faces={"up": lambda F: F.rect(0, 0, F.w, F.h, C.COAT_HI)})
    c("coat_bu", "chest", (-3.0, 12.0, 1.35), (3.0, 25.9, 1.8), C.COAT, faces={"south": cp})
    c("coat_collar", "chest", (-1.9, 25.4, 0.5), (1.9, 27.4, 1.9), C.COAT, origin=(0, 25.6, 1.2), rot=(-10, 0, 0))
    for s, k in ((1, "r"), (-1, "l")):
        x0, x1 = (1.6, 3.15) if s > 0 else (-3.15, -1.6)
        c("coat_fu_" + k, "chest", (x0, 12.0, -1.85), (x1, 25.6, -1.45), C.COAT, faces={"north": B.edges(C.COAT_HI)})
        xs0, xs1 = (2.75, 3.15) if s > 0 else (-3.15, -2.75)
        c("coat_su_" + k, "chest", (xs0, 12.0, -1.6), (xs1, 25.6, 1.6), C.COAT, faces={"east": cp, "west": cp})
        lx = 1.3 * s
        c("lapel_" + k, "chest", (lx - 0.45, 21.5, -2.0), (lx + 0.45, 25.6, -1.8), C.COAT_HI, origin=(lx, 25.6, -1.9), rot=(0, 0, -14 * s))
        # lower front + side panel (bone coat_r / coat_l)
        bx = "coat_" + k
        fx0, fx1 = (1.9, 3.4) if s > 0 else (-3.4, -1.9)
        c("coat_fl_" + k, bx, (fx0, 1.2, -1.95), (fx1, 12.3, -1.5), C.COAT, origin=(2.4 * s, 12, -0.6), rot=(4, 0, 5 * s),
          faces={"north": combo(cp, lambda F: F.rect(0, F.h - 2, F.w, 2, C.COAT_D))})
        sx0, sx1 = (2.95, 3.4) if s > 0 else (-3.4, -2.95)
        c("coat_sl_" + k, bx, (sx0, 1.2, -1.7), (sx1, 12.3, 1.7), C.COAT, origin=(2.4 * s, 12, -0.6), rot=(4, 0, 5 * s), faces={"east": cp, "west": cp})
        c("pocket_" + k, bx, (fx0 + 0.2, 8.5, -2.05), (fx1 - 0.2, 9.0, -1.9), C.COAT_D, origin=(2.4 * s, 12, -0.6), rot=(4, 0, 5 * s))
        if boss:
            for i in range(4):
                blade(f"crag_{k}{i}", bx, (2.0 * s + i * 0.45 * s, 1.5, -1.7 + i * 0.9), 2.4 + (i % 2) * 1.6, 0.8, 0.3,
                      (180 - 10, 0, -s * (8 + i * 6)), C.COAT, C.SHADOW_HI)
    c("coat_bl", "coat_b", (-3.2, 1.2, 1.4), (3.2, 12.3, 1.9), C.COAT, origin=(0, 12, 1.6), rot=(-5, 0, 0),
      faces={"south": cp, "north": lambda F: F.rect(0, 0, F.w, F.h, C.COAT_D)})
    c("coat_vent", "coat_b", (-0.1, 1.2, 1.92), (0.1, 7.0, 2.0), C.COAT_D, origin=(0, 12, 1.6), rot=(-5, 0, 0))
    if boss:
        for i in range(6):
            blade(f"crag_b{i}", "coat_b", (-2.8 + i * 1.1, 1.5, 1.75), 2.6 + (i % 3) * 1.2, 0.9, 0.3, (180 + 10, 0, (i - 2.5) * 8), C.COAT, C.SHADOW_HI)

    # ---------------- arms
    for s, k in ((1, "r"), (-1, "l")):
        x = 3.3 * s
        if not boss:
            c("sleeve_" + k, "arm_" + k, (x - 0.9, 19.8, -0.95), (x + 0.9, 25.6, 0.95), C.COAT, faces={"north": B.folds(C.COAT, C.COAT_D, C.COAT_HI, 1)})
            c("shpad_" + k, "arm_" + k, (x - 1.0, 23.9, -1.05), (x + 1.0, 25.9, 1.05), C.COAT, faces={"up": lambda F: F.rect(0, 0, F.w, F.h, C.COAT_HI)})
            c("fsleeve_" + k, "fore_" + k, (x - 0.85, 15.6, -0.9), (x + 0.85, 20.2, 0.9), C.COAT, faces={"north": B.edges(C.COAT_HI)})
            c("cuff_" + k, "fore_" + k, (x - 1.0, 14.5, -1.05), (x + 1.0, 16.0, 1.05), C.COAT_D, faces=B.all(lambda F: F.rect(0, 0, F.w, 1, C.COAT_HI)))
            c("hand_" + k, "hand_" + k, (x - 0.55, 12.7, -0.55), (x + 0.55, 14.8, 0.55), C.SKIN, color2=C.SKIN_D, grad=True)
            c("thumb_" + k, "hand_" + k, (x - 0.25 - 0.4 * s, 13.2, -0.85), (x + 0.25 - 0.4 * s, 14.4, -0.45), C.SKIN_D)
            # shadow claws (hidden until rake/maul)
            g("claws_" + k, (x, 13.0, 0), "hand_" + k)
            for i in range(4):
                cx = x - 0.45 + i * 0.3
                blade(f"sclaw_{k}{i}", "claws_" + k, (cx, 13.0, -0.2), 4.2, 0.35, 0.3, (180 + 18, 0, (i - 1.5) * 10 * s), C.SHADOW, C.SHADOW_HI)
            # shadow whip in the right hand
            if s > 0:
                g("whip0", (x, 12.8, 0), "hand_r")
                prev = "whip0"
                for i in range(6):
                    y = 12.8 - i * 2.2
                    if i:
                        g(f"whip{i}", (x, y, 0), prev); prev = f"whip{i}"
                    w = 0.6 - i * 0.07
                    c(f"whips{i}", prev, (x - w / 2, y - 2.3, -w / 2), (x + w / 2, y, w / 2), C.SHADOW, faces=B.all(B.edges(C.SHADOW_HI)))
                blade("whiptip", prev, (x, 12.8 - 6 * 2.2 + 0.1, 0), 1.6, 0.6, 0.3, (180, 0, 0), C.SHADOW, C.SHADOW_HI)
                # giant shadow hand (shadow_clutch): ink arm continuing the forearm (scaled along -Y to reach) + clawed palm
                # (palm bone is moved along -Y to stay on the arm tip); 4 talons in a ring that open / clutch
                g("shand", (x, 12.8, 0), "hand_r")
                g("sharm", (x, 12.8, 0), "shand")
                c("sharm_c", "sharm", (x - 0.6, 4.8, -0.6), (x + 0.6, 12.8, 0.6), C.SHADOW, faces=B.all(B.edges(C.SHADOW_HI)))
                c("sharm_w", "sharm", (x - 0.8, 9.0, -0.8), (x + 0.8, 12.4, 0.8), C.SHADOW, faces=B.all(B.edges(C.SHADOW_HI)))
                for i in range(3):  # ink wisps trailing off the arm
                    blade(f"swisp{i}", "sharm", (x + (i - 1) * 0.5, 6.0 + i * 2.2, 0.5 - i * 0.4), 1.8, 0.4, 0.3, (30 + i * 10, 0, (i - 1) * 50), C.SHADOW, C.SHADOW_HI)
                g("spalm", (x, 4.8, 0), "shand")
                c("spalm_c", "spalm", (x - 2.0, 1.4, -2.0), (x + 2.0, 4.9, 2.0), C.SHADOW,
                  faces=B.all(lambda F: (F.rect(0, 0, F.w, F.h, C.SHADOW), F.rect(1, 1, F.w - 2, 1, C.SHADOW_HI))))
                c("spalm_k", "spalm", (x - 1.5, 0.8, -1.5), (x + 1.5, 1.6, 1.5), C.SHADOW_HI)
                for i, ang in enumerate((45, 135, 225, 315)):
                    ux, uz = math.cos(math.radians(ang)), math.sin(math.radians(ang))
                    fx, fz = x + ux * 1.6, uz * 1.6
                    g(f"sfing{i}", (fx, 1.8, fz), "spalm")
                    B.lock(f"sfc{i}", f"sfing{i}", (fx, 1.8, fz), 6.0 if i != 3 else 4.6, 0.9, 0.8, (0, 0, 0), C.SHADOW, C.SHADOW_HI,
                           paint=B.edges(C.SHADOW_HI))
                    blade(f"sfk{i}", f"sfing{i}", (fx, 1.0, fz), 0.9, 0.9, 0.8, (180, 0, 0), C.SHADOW_HI)
        else:
            c("sleeve_" + k, "arm_" + k, (x - 1.0, 17.6, -1.05), (x + 1.0, 25.6, 1.05), C.COAT, faces={"north": B.folds(C.COAT, C.COAT_D, C.COAT_HI, 1)})
            c("shpad_" + k, "arm_" + k, (x - 1.15, 23.6, -1.15), (x + 1.15, 25.9, 1.15), C.COAT)
            c("fore_" + k, "fore_" + k, (x - 0.85, 10.6, -0.85), (x + 0.85, 18.0, 0.85), C.SKIN, color2=C.SKIN_D, grad=True,
              faces={"north": B.edges(C.SKIN_L)})
            for i in range(3):  # torn sleeve shreds
                blade(f"shred_{k}{i}", "fore_" + k, (x + (i - 1) * 0.6, 17.2, -0.6 + i * 0.6), 3.0 + i * 0.6, 0.7, 0.25, (180 - 8, 0, (i - 1) * 14), C.COAT, C.SHADOW_HI)
            for i in range(3):  # forearm thorns
                blade(f"thorn_{k}{i}", "fore_" + k, (x + 0.7 * s, 12.0 + i * 2.0, 0.2), 1.6, 0.4, 0.3, (20, 0, -s * 70), C.SKIN, C.SHADOW_HI)
            big = 1.25 if s > 0 else 1.0
            c("palm_" + k, "hand_" + k, (x - 1.1 * big, 10.6 - 3.2 * big, -0.8 * big), (x + 1.1 * big, 10.8, 0.8 * big), C.SKIN, color2=C.SKIN_L, grad=True)
            for i in range(4):
                fx = x - 0.85 * big + i * 0.57 * big
                fz = -0.6 * big + abs(i - 1.5) * 0.3
                g(f"fing_{k}{i}", (fx, 10.6 - 3.0 * big, fz), "hand_" + k)
                c(f"fseg_{k}{i}", f"fing_{k}{i}", (fx - 0.36, 10.6 - 6.4 * big, fz - 0.36), (fx + 0.36, 10.6 - 3.0 * big, fz + 0.36), C.SKIN,
                  faces=B.all(B.edges(C.SKIN_L)))
                B.lock(f"fclw_{k}{i}", f"fing_{k}{i}", (fx, 10.6 - 6.2 * big, fz), 4.6 * big, 0.6, 0.5, (-28, 0, (i - 1.5) * 6), C.CLAW, C.CLAW_HI,
                       paint=B.edges(C.CLAW_HI))
            g("thumb_" + k, (x - 1.0 * s, 9.0, -0.8), "hand_" + k)
            B.lock("thumbc_" + k, "thumb_" + k, (x - 1.0 * s, 9.0, -0.8), 4.0 * big, 0.6, 0.5, (-30, 0, -s * 30), C.CLAW, C.CLAW_HI, paint=B.edges(C.CLAW_HI))

    # ---------------- head
    c("skull", "head", (-2.7, 27.2, -2.6), (2.7, 32.6, 2.6), C.SKIN, faces={"north": face_p2(C) if boss else face_p1(C)})
    c("jaw", "head", (-1.7, 26.8, -2.45), (1.7, 27.4, 0.8), C.SKIN_D)
    for s, k in ((1, "r"), (-1, "l")):
        c("ear_" + k, "head", (2.6 * s - 0.2, 28.8, -0.4), (2.6 * s + 0.2, 30.6, 0.6), C.SKIN_D)
    c("earring1", "head", (-3.05, 28.3, -0.1), (-2.75, 28.9, 0.3), C.COAT_D)
    c("earring2", "head", (-3.05, 29.3, 0.3), (-2.75, 29.8, 0.6), C.COAT_D)
    # hair mass
    c("hair_cap", "head", (-3.0, 30.4, -2.9), (3.0, 33.9, 3.0), C.HAIR, faces=B.all(st))
    c("hair_top", "head", (-2.6, 33.7, -2.4), (2.6, 34.5, 2.6), C.HAIR, faces=B.all(st_plain))
    c("hair_back", "hair_b", (-3.1, 27.0, 1.6), (3.1, 31.6, 3.3), C.HAIR, faces=B.all(st))
    for i, (x, ln, rz) in enumerate([(-2.2, 3.4, 168), (-0.8, 4.2, 178), (0.7, 3.8, 186), (2.1, 3.2, 196)]):
        blade(f"hb{i}", "hair_b", (x, 28.0, 2.8), ln, 1.8, 0.8, (-12, 0, rz), C.HAIR, C.HAIR_D, paint=st_plain)
    for s, k in ((1, "r"), (-1, "l")):
        x0, x1 = (2.5, 3.4) if s > 0 else (-3.4, -2.5)
        c("side_" + k, "hair_" + k, (x0, 27.4, -2.2), (x1, 31.6, 2.4), C.HAIR, faces=B.all(st))
        for i, (y, z, ln, rz) in enumerate([(31.6, -0.8, 2.6, 100), (30.6, 0.8, 3.6, 128), (29.4, -1.2, 3.4, 146), (28.6, 1.2, 3.2, 160), (28.0, -0.2, 2.8, 170)]):
            blade(f"hs_{k}{i}", "hair_" + k, (3.0 * s, y, z), ln + (0.5 if s < 0 else 0), 1.7, 0.9, (0, 0, -rz * s), C.HAIR, C.HAIR_D, paint=st_plain)
    # bangs: heavy sweep from her left over her right eye
    c("fringe", "bangs", (-3.0, 31.0, -3.05), (3.0, 32.8, -2.6), C.HAIR, faces=B.all(st))
    for i, (x, ln, rz) in enumerate([(2.6, 2.6, -6), (-0.6, 1.0, -16), (-1.7, 1.2, -20), (-2.7, 1.6, -10)]):
        B.lock(f"bang{i}", "bangs", (x, 31.4, -2.95), ln, 1.6, 0.4, (6, 0, rz), C.HAIR, C.HAIR_D, paint=st_plain)
    B.lock("bang_long", "bangs", (1.3, 31.6, -3.0), 3.2, 2.2, 0.4, (6, 0, -10), C.HAIR, C.HAIR_D, paint=st_plain)
    B.lock("bang_long2", "bangs", (2.2, 31.4, -3.0), 3.0, 1.8, 0.4, (6, 0, -12), C.HAIR, C.HAIR_D, paint=st_plain)
    # ahoge: long arching strand
    c("ahs0", "ah0", (0.1, 34.3, -0.1), (0.7, 37.2, 0.5), C.HAIR, faces=B.all(st_plain))
    c("ahs1", "ah1", (0.15, 37.0, -0.05), (0.65, 39.6, 0.45), C.HAIR, faces=B.all(st_plain))
    c("ahs2", "ah2", (0.2, 39.4, 0.0), (0.6, 41.6, 0.4), C.HAIR_D)
    # crown: black band with spiky points, tilted
    c("crown_band", "crown", (-2.85, 33.9, -2.85), (2.85, 35.0, 2.85), C.CROWN, faces=B.all(lambda F: F.rect(0, 0, F.w, 1, C.CROWN_HI)))
    for i, (ang, ln, w) in enumerate([(0, 4.2, 1.7), (50, 3.0, 1.3), (-50, 3.0, 1.3), (110, 2.8, 1.3), (-110, 2.8, 1.3), (180, 2.8, 1.3)]):
        a = math.radians(ang)
        bx, bz = -math.sin(a) * 2.5, -math.cos(a) * 2.5
        blade(f"cpt{i}", "crown", (bx, 34.9, bz), ln, w, 0.4, (-8 * math.cos(a), -ang, 8 * math.sin(a)), C.CROWN, C.CROWN_HI)

    # ---------------- shadow wings (phase 1: hidden props) / shoulder spines (boss: always out)
    for s, k in ((1, "r"), (-1, "l")):
        for i in range(3):
            b = f"wing_{k}{i}"
            ln = (15, 18, 13)[i] * (0.9 if boss else 1.0)
            wp = B.all(lambda F: (F.rect(0, 0, F.w, F.h, C.SHADOW), F.rect(0, 0, 1, F.h, C.SHADOW_HI), F.rect(F.w - 1, 0, 1, F.h, C.SHADOW_HI)))
            blade(f"wg_{k}{i}", b, (0.8 * s, 23.5 - i * 1.2, 1.7), ln, 2.0, 0.6, (0, 0, 0), C.SHADOW, C.SHADOW_HI, paint=wp["north"])
            blade(f"wgb_{k}{i}", b, (0.8 * s, 23.5 - i * 1.2 + ln * 0.35, 1.7), ln * 0.4, 1.2, 0.5, (0, 0, -40 * s), C.SHADOW, C.SHADOW_HI)
            blade(f"wgc_{k}{i}", b, (0.8 * s, 23.5 - i * 1.2 + ln * 0.6, 1.7), ln * 0.28, 0.9, 0.4, (0, 0, 35 * s), C.SHADOW, C.SHADOW_HI)
    if boss:
        for s, k in ((1, "r"), (-1, "l")):
            g("spines_" + k, (2.6 * s, 24.6, 0.6), "chest")
            for i, (rx, rz, ln) in enumerate([(-10, 70, 8), (10, 52, 10), (28, 84, 9), (-25, 100, 7), (40, 64, 6)]):
                blade(f"sp_{k}{i}", "spines_" + k, (2.6 * s, 24.6 - i * 0.4, 0.6 + i * 0.2), ln, 0.8, 0.5, (rx, 0, -rz * s), C.SHADOW, C.SHADOW_HI)
        # tail: 6 tapering segments from under the coat
        g("tail0", (0.4, 13.0, 1.8), "body", rot=(55, 20, 0))
        prev = "tail0"
        for i in range(6):
            w = 0.9 - i * 0.12
            z0 = 1.8 + i * 3.0
            if i:
                g(f"tail{i}", (0.4, 13.0, z0), prev, rot=((-22, -26, -30, -30, -20)[i - 1], 6, 0)); prev = f"tail{i}"
            c(f"tails{i}", prev, (0.4 - w, 13.0 - w, z0), (0.4 + w, 13.0 + w, z0 + 3.1), C.COAT, faces=B.all(B.edges(C.COAT_HI)))
            if i in (1, 3):
                blade(f"tspk{i}", prev, (0.4, 13.0 + w * 0.8, z0 + 1.5), 1.4, 0.5, 0.4, (0, 0, 0), C.COAT, C.SHADOW_HI)
        blade("ttip", prev, (0.4, 13.0, 1.8 + 6 * 3.0 - 0.2), 2.4, 1.0, 0.4, (90, 0, 0), C.COAT, C.SHADOW_HI)
        # back tentacles: 4 x 4 segments, root on the back, extending +Z
        for t, (tx, ty) in enumerate([(1.2, 22.4), (-1.2, 22.4), (1.6, 19.6), (-1.6, 19.6)]):
            prev = None
            for i in range(4):
                w = 0.75 - i * 0.13
                z0 = 1.6 + i * 3.0
                nm = f"tent{t}_{i}"
                g(nm, (tx, ty, z0), prev or "chest"); prev = nm
                c(nm + "c", nm, (tx - w, ty - w, z0), (tx + w, ty + w, z0 + 3.1), C.SHADOW, faces=B.all(B.edges(C.SHADOW_HI)))
            blade(f"tent{t}_tip", prev, (tx, ty, 1.6 + 12 - 0.2), 2.0, 0.6, 0.4, (90, 0, 0), C.SHADOW, C.SHADOW_HI)
        # eye beam (hidden unless eye_beam)
        g("beam", (0, 30.0, -2.7), "head")
        c("beam_core", "beam", (-0.35, 29.65, -60), (0.35, 30.35, -2.7), C.GLOW, glow=True)
        c("beam_halo", "beam", (-0.8, 29.2, -40), (0.8, 30.8, -2.8), 0xFF9A2A, glow=True)


def combo(*fns):
    def f(F):
        for fn in fns: fn(F)
    return f


# ================================================================== animation framework
class A:
    def __init__(self, B, name, ticks, rest, props, loop=False):
        self.B, self.name, self.ticks, self.loop, self.tr = B, name, ticks, loop, {}
        self.rest, self.props = rest, props
        self.prest = {}   # default positions (base units) for bones not keyed, e.g. the lowered quad root
        self.base = {}    # rotation offsets added by drape() (quad stance: cloth/hair hang from a pitched torso)

    def k(self, bone, ch, keys):
        self.tr.setdefault(bone, {}).setdefault(ch, []).extend(keys)
        return self

    def rot(self, bone, *keys): return self.k(bone, "rotation", keys)
    def pos(self, bone, *keys): return self.k(bone, "position", [(t, x * self.B.K, y * self.B.K, z * self.B.K) for (t, x, y, z) in keys])
    def scl(self, bone, *keys): return self.k(bone, "scale", keys)

    def at(self, t, **bones):
        """pose snapshot: bone=(rx,ry,rz) rotation keys; key 'P_<bone>' = position"""
        for b, v in bones.items():
            if b.startswith("P_"):
                self.pos(b[2:], (t, *v))
            else:
                self.rot(b, (t, *v))
        return self

    def show(self, bone, t0, t1, grow=1.5):
        keys = []
        if t0 > 0: keys += [(0, *HIDE), (t0 - 0.01, *HIDE), (t0 + grow, 1, 1, 1)]
        else: keys += [(0, 1, 1, 1)]
        if t1 < self.ticks: keys += [(t1 - grow, 1, 1, 1), (t1, *HIDE), (self.ticks, *HIDE)]
        else: keys += [(self.ticks, 1, 1, 1)]
        return self.scl(bone, *keys)

    def drape(self, bone, keys, delay=2, gain=1.0):
        seen, out = set(), []
        for (t, x, y, z) in keys:
            tt = min(self.ticks, t + delay)
            if tt in seen: continue
            b0 = self.base.get(bone, (0, 0, 0))
            seen.add(tt); out.append((tt, x * gain + b0[0], y * gain + b0[1], z * gain + b0[2]))
        return self.rot(bone, *out)

    def hair(self, keys, delay=2):
        """x = forward(+)/back flick, z = sideways"""
        self.drape("hair_b", [(t, -x * 0.8, 0, z * 0.5) for (t, x, y, z) in keys], delay)
        self.drape("hair_r", [(t, x * 0.4, 0, z * 0.6 + abs(x) * 0.2) for (t, x, y, z) in keys], delay)
        self.drape("hair_l", [(t, x * 0.4, 0, z * 0.6 - abs(x) * 0.2) for (t, x, y, z) in keys], delay)
        self.drape("bangs", [(t, x * 0.3, 0, z * 0.3) for (t, x, y, z) in keys], delay)
        self.drape("ah0", [(t, -x * 0.5, 0, z * 0.5) for (t, x, y, z) in keys], delay + 1)
        self.drape("ah1", [(t, -x * 0.6, 0, z * 0.4) for (t, x, y, z) in keys], delay + 3)
        self.drape("ah2", [(t, -x * 0.8, 0, z * 0.4) for (t, x, y, z) in keys], delay + 5)
        self.drape("pendant", [(t, x * 0.6, 0, z * 0.6) for (t, x, y, z) in keys], delay)
        return self

    def cloth(self, keys, delay=2):
        """x>0 = hem kicks forward (front panels out / back panels in), z>0 = flare toward +X, w = flare both sides out"""
        k4 = [(q + (0,))[:5] if len(q) == 4 else q for q in keys]
        self.drape("dress_f", [(t, x * 0.5 + w * 0.5, 0, 0) for (t, x, y, z, w) in k4], delay)
        self.drape("dress_b", [(t, x * 0.5 - w * 0.5, 0, 0) for (t, x, y, z, w) in k4], delay)
        self.drape("dress_r", [(t, 0, 0, z * 0.5 + w * 0.5) for (t, x, y, z, w) in k4], delay)
        self.drape("dress_l", [(t, 0, 0, z * 0.5 - w * 0.5) for (t, x, y, z, w) in k4], delay)
        self.drape("coat_b", [(t, x - w * 0.8, 0, z * 0.4) for (t, x, y, z, w) in k4], delay + 1)
        self.drape("coat_r", [(t, x * 0.8 + w * 0.3, 0, z + w) for (t, x, y, z, w) in k4], delay + 1)
        self.drape("coat_l", [(t, x * 0.8 + w * 0.3, 0, z - w) for (t, x, y, z, w) in k4], delay + 1)
        return self

    def legs(self, keys_leg, keys_shin, keys_foot=None):
        for s, k in ((1, "r"), (-1, "l")):
            self.rot("leg_" + k, *[(t, x, y * s, z * s) for (t, x, y, z) in keys_leg])
            self.rot("shin_" + k, *keys_shin)
            if keys_foot: self.rot("foot_" + k, *keys_foot)
        return self

    def done(self, base_layer=False):
        if not base_layer:
            for p in self.props:
                if p not in self.tr or "scale" not in self.tr[p]:
                    self.scl(p, (0, *HIDE))
            for b, v in self.rest.items():
                if b not in self.tr or "rotation" not in self.tr[b]:
                    self.rot(b, (0, *v))
            for b, v in self.prest.items():
                if b not in self.tr or "position" not in self.tr[b]:
                    self.pos(b, (0, *v))
        end = self.ticks
        for b, chs in self.tr.items():
            for ch, ks in chs.items():
                ts = [q[0] for q in ks]
                if ch == "scale": continue
                dflt = self.rest.get(b, (0, 0, 0)) if ch == "rotation" else tuple(q * self.B.K for q in self.prest.get(b, (0, 0, 0)))
                if base_layer and ch == "rotation" and b not in self.rest: dflt = (0, 0, 0)
                if 0 not in ts and min(ts) > 0: ks.append((0, *dflt))
                if max(ts) < end: ks.append((end, *(dflt if not self.loop else sorted(ks)[0][1:])))
        tracks = {b: {ch: sorted([(t / 20.0, x, y, z) for (t, x, y, z) in v], key=lambda q: q[0]) for ch, v in chs.items()}
                  for b, chs in self.tr.items()}
        self.B.m.anim(self.name, self.ticks / 20.0, tracks, loop=self.loop)


def lerp3(a, b, u):
    return tuple(a[i] + (b[i] - a[i]) * u for i in range(3))


def add3(a, b):
    return tuple(a[i] + b[i] for i in range(3))


# ================================================================== PHASE 1 animations
WR = {"wing_r0": (20, 0, -45), "wing_r1": (28, 0, -78), "wing_r2": (36, 0, -112),
      "wing_l0": (20, 0, 45), "wing_l1": (28, 0, 78), "wing_l2": (36, 0, 112)}
REST1 = {"arm_r": (2, 0, 5), "fore_r": (8, 0, 0), "arm_l": (2, 0, -5), "fore_l": (8, 0, 0), "head": (0, 0, -4),
         "leg_l": (-3, 0, -1), "leg_r": (2, 0, 1), **WR}
PROPS1 = ("wings", "claws_r", "claws_l", "whip0", "shand")
SF = [(math.cos(math.radians(a)), math.sin(math.radians(a))) for a in (45, 135, 225, 315)]


def sgrip(a, t, f):
    """shadow-hand talons: f>0 splay open, f<0 clutch shut"""
    for i, (ux, uz) in enumerate(SF):
        a.rot(f"sfing{i}", (t, -uz * f, 0, ux * f))


def sreach(a, *keys):
    """shadow arm length: keys (t, s) -> arm scaled s along its axis, palm kept on the tip (arm base length 8 px)"""
    a.scl("sharm", *[(t, 1, s, 1) for (t, s) in keys])
    a.pos("spalm", *[(t, 0, -8 * (s - 1), 0) for (t, s) in keys])


def wings_at(a, t, spread=1.0, lift=0.0, **over):
    """all six wings: rest spread scaled by `spread`, plus `lift` added to rx; per-wing overrides"""
    for b, (x, y, z) in WR.items():
        v = over.get(b, (x + lift, y, z * spread))
        a.rot(b, (t, *v))


def anims_p1(B):
    def mk(name, ticks, loop=False):
        return A(B, name, ticks, REST1, PROPS1, loop)

    r = REST1
    # ---------------------------------------------------------------- idle (80): bored contrapposto, breathing, head lolls, ahoge bobs
    a = mk("idle", 80, loop=True)
    a.at(0, chest=(0, 0, 0), head=(0, 0, -4), P_body=(0, 0, 0), body=(0, 0, 1))
    a.at(20, chest=(1.6, 0, 0), head=(2, 3, -6), P_body=(0, -0.08, 0))
    a.at(40, chest=(0, 0, 0), head=(0, 0, -3), P_body=(0, 0, 0), body=(0, 0, 1.5))
    a.at(60, chest=(1.6, 0, 0), head=(-1, -4, -5), P_body=(0, -0.08, 0))
    a.at(80, chest=(0, 0, 0), head=(0, 0, -4), P_body=(0, 0, 0), body=(0, 0, 1))
    a.at(0, arm_r=r["arm_r"], arm_l=r["arm_l"], fore_r=r["fore_r"], fore_l=r["fore_l"])
    a.at(40, arm_r=(3, 0, 6), arm_l=(3, 0, -6), fore_r=(10, 0, 0), fore_l=(10, 0, 0))
    a.at(80, arm_r=r["arm_r"], arm_l=r["arm_l"], fore_r=r["fore_r"], fore_l=r["fore_l"])
    a.at(0, leg_l=r["leg_l"], leg_r=r["leg_r"]).at(80, leg_l=r["leg_l"], leg_r=r["leg_r"])
    a.hair([(0, 0, 0, 1), (20, 2, 0, -1), (40, 0, 0, 1.5), (60, 2, 0, -1), (80, 0, 0, 1)], delay=5)
    a.cloth([(0, 0, 0, 0.5), (20, 1, 0, -0.5), (40, 0, 0, 0.5), (60, 1, 0, -0.5), (80, 0, 0, 0.5)], delay=5)
    a.done()

    # ---------------------------------------------------------------- walk (20): long gliding strides, coat swinging behind
    a = mk("walk", 20, loop=True)
    a.rot("leg_r", (0, 26, 0, 0), (5, 0, 0, 0), (10, -24, 0, 0), (15, 0, 0, 0), (20, 26, 0, 0))
    a.rot("shin_r", (0, -4, 0, 0), (5, -6, 0, 0), (10, -10, 0, 0), (13, -46, 0, 0), (17, -22, 0, 0), (20, -4, 0, 0))
    a.rot("foot_r", (0, -12, 0, 0), (10, 12, 0, 0), (20, -12, 0, 0))
    a.rot("leg_l", (0, -24, 0, 0), (5, 0, 0, 0), (10, 26, 0, 0), (15, 0, 0, 0), (20, -24, 0, 0))
    a.rot("shin_l", (0, -10, 0, 0), (3, -46, 0, 0), (7, -22, 0, 0), (10, -4, 0, 0), (15, -6, 0, 0), (20, -10, 0, 0))
    a.rot("foot_l", (0, 12, 0, 0), (10, -12, 0, 0), (20, 12, 0, 0))
    a.pos("body", (0, 0, -0.4, 0), (5, 0, 0.25, 0), (10, 0, -0.4, 0), (15, 0, 0.25, 0), (20, 0, -0.4, 0))
    a.rot("body", (0, -3, 5, 0), (10, -3, -5, 0), (20, -3, 5, 0))
    a.rot("chest", (0, -1, -6, 0), (10, -1, 6, 0), (20, -1, -6, 0))
    a.rot("arm_r", (0, -14, 0, 0), (10, 16, 0, 0), (20, -14, 0, 0))
    a.rot("arm_l", (0, 16, 0, 0), (10, -14, 0, 0), (20, 16, 0, 0))
    a.rot("fore_r", (0, 0, 0, 0), (10, 10, 0, 0), (20, 0, 0, 0))
    a.rot("fore_l", (0, 10, 0, 0), (10, 0, 0, 0), (20, 10, 0, 0))
    a.hair([(0, -4, 0, 2), (5, -6, 0, 0), (10, -4, 0, -2), (15, -6, 0, 0), (20, -4, 0, 2)], delay=2)
    a.cloth([(0, -6, 0, 3), (5, -9, 0, 0), (10, -6, 0, -3), (15, -9, 0, 0), (20, -6, 0, 3)], delay=1)
    a.done(base_layer=True)

    # ---------------------------------------------------------------- wing_stab (36): wings burst 3-6, RIGHT lance 12, LEFT lance 23, fold 30
    a = mk("wing_stab", 36).show("wings", 3, 33, grow=3)
    a.at(0, chest=(0, 0, 0), head=r["head"], arm_r=r["arm_r"], arm_l=r["arm_l"])
    a.at(5, chest=(-14, 0, 0), head=(12, 0, 0), arm_r=(14, 0, 18), arm_l=(14, 0, -18), fore_r=(30, 0, 0), fore_l=(30, 0, 0), P_body=(0, -0.6, 0.3))
    wings_at(a, 3, spread=0.3, lift=20); wings_at(a, 7, spread=1.1, lift=10)
    a.at(9, chest=(-8, -20, 0), head=(4, 14, 0), arm_r=(-20, 0, 20), arm_l=(30, 0, -14), P_body=(0, -0.8, 0.6))
    a.at(9, wing_r1=(70, 0, -55))
    a.at(12, chest=(-10, 22, 0), head=(2, -14, 0), arm_r=(82, 0, 8), fore_r=(0, 0, 0), arm_l=(-10, 0, -20), P_body=(0, -0.6, -1.4),
         wing_r1=(-95, -8, -4), wing_r0=(-20, 0, -40))
    a.scl("wing_r1", (0, 1, 1, 1), (10, 1, 1, 1), (12, 1, 1.5, 1), (15, 1, 1.2, 1), (17, 1, 1, 1), (26, 1, 1, 1))
    a.at(15, wing_r1=(-80, 0, -10), wing_r0=(10, 0, -45))
    a.at(18, chest=(-8, 14, 0), arm_r=(20, 0, 14), arm_l=(-30, 0, -24), head=(4, -8, 0), wing_r1=(30, 0, -80), wing_l1=(70, 0, 55), P_body=(0, -0.7, -0.6))
    a.at(23, chest=(-10, -24, 0), head=(2, 14, 0), arm_l=(84, 0, -8), fore_l=(0, 0, 0), arm_r=(-14, 0, 20), P_body=(0, -0.6, -2.2),
         wing_l1=(-95, 8, 4), wing_l0=(-20, 0, 40))
    a.scl("wing_l1", (0, 1, 1, 1), (21, 1, 1, 1), (23, 1, 1.5, 1), (26, 1, 1.2, 1), (28, 1, 1, 1))
    a.at(26, wing_l1=(-80, 0, 10), wing_l0=(10, 0, 45), chest=(-6, -16, 0))
    wings_at(a, 30, spread=0.8, lift=20); wings_at(a, 34, spread=0.2, lift=40)
    a.at(30, chest=(-2, -4, 0), arm_l=(10, 0, -8), arm_r=(6, 0, 8), fore_l=(14, 0, 0), fore_r=(12, 0, 0), head=(0, 0, -2), P_body=(0, -0.2, -1.6))
    a.at(36, chest=(0, 0, 0), P_body=(0, 0, 0))
    a.legs([(0, 0, 0, 0), (5, -6, 0, 0), (12, 0, 0, 0), (36, 0, 0, 0)], [(0, 0, 0, 0), (5, -14, 0, 0), (12, -8, 0, 0), (30, -4, 0, 0), (36, 0, 0, 0)])
    a.at(12, leg_r=(-26, 0, 2), leg_l=(18, 0, -2)).at(23, leg_l=(-26, 0, -2), leg_r=(18, 0, 2))
    a.hair([(0, 0, 0, 0), (5, 8, 0, 0), (12, -10, 0, 8), (18, 4, 0, -2), (23, -10, 0, -8), (30, 2, 0, 0), (36, 0, 0, 0)])
    a.cloth([(0, 0, 0, 0), (5, 2, 0, 0, 4), (12, -8, 0, 5), (23, -8, 0, -5), (30, -2, 0, 0), (36, 0, 0, 0)])
    a.done()

    # ---------------------------------------------------------------- wing_whirl (32): coil 2-9 (wings flat), SPIN 10-18 (hit 15), wobble, fold
    a = mk("wing_whirl", 32)
    for t, sp in ((2, 0.3), (6, 1.0)):
        wings_at(a, t, spread=sp, lift=30)
    flat = {"wing_r0": (-10, 20, -88), "wing_r1": (0, 0, -92), "wing_r2": (10, -20, -96), "wing_l0": (-10, -20, 88), "wing_l1": (0, 0, 92), "wing_l2": (10, 20, 96)}
    for t in (10, 18):
        for b, v in flat.items(): a.rot(b, (t, *v))
    a.scl("wings", (0, *HIDE), (1.99, *HIDE), (4, 1, 1, 1), (9, 1, 1, 1), (12, 1.35, 1, 1.35), (18, 1.35, 1, 1.35), (22, 1, 1, 1), (27, 1, 1, 1), (29, *HIDE), (32, *HIDE))
    wings_at(a, 24, spread=0.7, lift=30)
    a.at(0, root=(0, 0, 0), chest=(0, 0, 0))
    a.at(8, root=(0, -40, 0), chest=(-16, 20, 0), head=(14, -10, 0), arm_r=(30, 0, 70), arm_l=(30, 0, -70), fore_r=(40, 0, 0), fore_l=(40, 0, 0), P_root=(0, -1.2, 0))
    a.at(10, root=(0, -20, 0), chest=(-8, 10, 0), arm_r=(0, 0, 85), arm_l=(0, 0, -85), fore_r=(0, 0, 0), fore_l=(0, 0, 0), P_root=(0, 0.6, 0))
    a.at(13, root=(0, 120, 0), P_root=(0, 1.4, 0))
    a.at(15, root=(0, 200, 0), chest=(-4, 0, 0), head=(-6, 0, 0), P_root=(0, 1.6, 0))
    a.at(18, root=(0, 320, 0), P_root=(0, 0.6, 0), arm_r=(10, 0, 70), arm_l=(10, 0, -70))
    a.at(21, root=(0, 360, 0), chest=(-10, -8, 0), head=(8, 6, 0), P_root=(0, -0.6, 0), arm_r=(20, 0, 30), arm_l=(20, 0, -30), fore_r=(20, 0, 0), fore_l=(20, 0, 0))
    a.at(26, root=(0, 364, 0), chest=(-3, 0, 0), P_root=(0, 0, 0))
    a.at(32, root=(0, 360, 0), chest=(0, 0, 0), head=r["head"], arm_r=r["arm_r"], arm_l=r["arm_l"], fore_r=r["fore_r"], fore_l=r["fore_l"])
    a.legs([(0, 0, 0, 0), (8, -18, 0, 4), (13, 0, 0, 14), (18, 0, 0, 14), (22, -14, 0, 3), (32, 0, 0, 0)],
           [(0, 0, 0, 0), (8, -30, 0, 0), (13, -6, 0, 0), (22, -24, 0, 0), (32, 0, 0, 0)])
    a.hair([(0, 0, 0, 0), (8, 6, 0, 10), (13, -4, 0, -24), (18, -4, 0, -24), (22, 4, 0, 10), (27, 0, 0, -3), (32, 0, 0, 0)])
    a.cloth([(0, 0, 0, 0), (8, 0, 0, 4, 2), (12, -4, 0, -8, 22), (18, -4, 0, -8, 24), (22, 2, 0, 6, 6), (32, 0, 0, 0)])
    a.done()

    # ---------------------------------------------------------------- shadow_whip (34): whip forms 4, cock back 9, LASH 12 (forward), hold, YANK 22, coil, dissolve
    a = mk("shadow_whip", 34).show("whip0", 4, 31, grow=2)
    a.at(0, arm_r=r["arm_r"], fore_r=r["fore_r"], chest=(0, 0, 0))
    a.at(5, arm_r=(40, 0, 30), fore_r=(60, 0, 0), chest=(0, -14, 0), head=(4, 10, 0), P_body=(0, -0.3, 0.3))
    a.at(9, arm_r=(150, 0, 30), fore_r=(40, 0, 0), chest=(4, -26, 0), head=(6, 16, 0), arm_l=(30, 0, -20), P_body=(0, -0.4, 0.8))
    a.rot("whip0", (4, 40, 0, 0), (9, 100, 0, 0), (12, -10, 0, 0), (14, -6, 0, 0), (20, -4, 0, 0), (22, 30, 0, 0), (26, 60, 0, 0), (34, 0, 0, 0))
    for i in range(1, 6):
        d = i * 0.6
        a.rot(f"whip{i}", (4, 30, 0, 0), (9 + d, 40, 0, 0), (11 + d, -24, 0, 0), (13 + d, 8, 0, 0), (16, 0, 0, 0), (21, 0, 0, 0), (22 + d, -30, 0, 0),
              (25 + d, 40, 0, 0), (30, 30, 0, 0))
    a.scl("whip1", (0, 1, 1, 1), (10, 1, 1, 1), (12, 1, 2.2, 1), (20, 1, 2.2, 1), (24, 1, 1, 1))
    a.at(12, arm_r=(92, 0, 6), fore_r=(0, 0, 0), chest=(-8, 20, 0), head=(0, -12, 0), arm_l=(-20, 0, -20), P_body=(0, -0.6, -1.0))
    a.at(18, arm_r=(88, 0, 6), chest=(-6, 16, 0), P_body=(0, -0.6, -0.8))
    a.at(22, arm_r=(40, 0, 20), fore_r=(80, 0, 0), chest=(6, -16, 0), head=(4, 12, 0), arm_l=(20, 0, -20), P_body=(0, -0.4, 0.8))
    a.at(26, arm_r=(10, 0, 18), fore_r=(60, 0, 0), chest=(2, -6, 0), P_body=(0, 0, 0.3))
    a.legs([(0, 0, 0, 0), (34, 0, 0, 0)], [(0, 0, 0, 0), (9, -10, 0, 0), (12, -16, 0, 0), (22, -8, 0, 0), (34, 0, 0, 0)])
    a.at(9, leg_r=(14, 0, 2), leg_l=(-10, 0, -2)).at(12, leg_r=(-22, 0, 2), leg_l=(16, 0, -2)).at(22, leg_r=(10, 0, 2), leg_l=(-22, 0, -2)).at(30, leg_r=r["leg_r"], leg_l=r["leg_l"])
    a.hair([(0, 0, 0, 0), (9, 8, 0, 6), (12, -12, 0, -8), (22, 10, 0, 6), (30, 0, 0, 0)])
    a.cloth([(0, 0, 0, 0), (9, 4, 0, 4), (12, -8, 0, -6), (22, 6, 0, 4), (34, 0, 0, 0)])
    a.done()

    # ---------------------------------------------------------------- spike_line (38): hand raised 4-10, drop to knee + palm SLAM 14, shadow ripples, rise
    a = mk("spike_line", 38).show("claws_r", 6, 30)
    a.at(0, chest=(0, 0, 0), arm_r=r["arm_r"])
    a.at(5, chest=(6, -10, 0), head=(10, 6, 0), arm_r=(160, 0, 20), fore_r=(20, 0, 0), arm_l=(20, 0, -30), P_body=(0, 0.6, 0))
    a.at(10, chest=(10, -14, 0), head=(14, 8, 0), arm_r=(176, 0, 14), fore_r=(10, 0, 0), arm_l=(30, 0, -40), P_body=(0, 0.9, 0.2))
    a.at(14, chest=(-38, 6, 0), head=(26, -4, 0), arm_r=(70, 0, 6), fore_r=(10, 0, 0), arm_l=(-10, 0, -40), P_body=(0, -6.0, -1.4))
    a.at(18, chest=(-34, 4, 0), head=(30, -2, 0), arm_r=(64, 0, 6), P_body=(0, -5.6, -1.2))
    a.at(26, chest=(-30, 2, 0), head=(24, 0, 0), arm_r=(60, 0, 8), P_body=(0, -5.4, -1.0))
    a.at(32, chest=(-8, 0, 0), head=(4, 0, -2), arm_r=(10, 0, 8), fore_r=(14, 0, 0), arm_l=(6, 0, -8), P_body=(0, -0.8, -0.2))
    a.at(38, chest=(0, 0, 0), head=r["head"], arm_r=r["arm_r"], fore_r=r["fore_r"], arm_l=r["arm_l"], P_body=(0, 0, 0))
    a.rot("leg_r", (0, *r["leg_r"]), (10, 6, 0, 2), (14, 70, 0, 4), (26, 70, 0, 4), (32, 14, 0, 2), (38, *r["leg_r"]))
    a.rot("shin_r", (0, 0, 0, 0), (14, -80, 0, 0), (26, -80, 0, 0), (32, -18, 0, 0), (38, 0, 0, 0))
    a.rot("leg_l", (0, *r["leg_l"]), (10, -4, 0, -2), (14, -20, 0, -4), (26, -20, 0, -4), (32, -6, 0, -2), (38, *r["leg_l"]))
    a.rot("shin_l", (0, 0, 0, 0), (14, -110, 0, 0), (26, -110, 0, 0), (32, -20, 0, 0), (38, 0, 0, 0))
    a.rot("foot_l", (0, 0, 0, 0), (14, 40, 0, 0), (26, 40, 0, 0), (32, 4, 0, 0), (38, 0, 0, 0))
    a.hair([(0, 0, 0, 0), (10, 4, 0, 0), (14, 20, 0, 4), (18, -6, 0, 0), (26, 0, 0, 0), (32, -4, 0, 0), (38, 0, 0, 0)])
    a.cloth([(0, 0, 0, 0), (10, 0, 0, 0), (14, 12, 0, 0, 14), (20, 4, 0, 0, 8), (32, 2, 0, 0), (38, 0, 0, 0)])
    a.done()

    # ---------------------------------------------------------------- blink_rake (30): melt into the floor 4-9, rise behind 10-13, RAKE 15 (R), RAKE 21 (L)
    a = mk("blink_rake", 30).show("claws_r", 10, 27).show("claws_l", 10, 27)
    a.scl("root", (0, 1, 1, 1), (4, 1.1, 0.9, 1.1), (8, 1.6, 0.05, 1.6), (9.9, 0.4, 0.02, 0.4), (10, 0.4, 0.02, 0.4), (12, 0.9, 1.15, 0.9), (13.5, 1, 1, 1), (30, 1, 1, 1))
    a.at(0, chest=(0, 0, 0))
    a.at(4, chest=(-20, 0, 0), head=(16, 0, 0), arm_r=(-10, 0, 40), arm_l=(-10, 0, -40), P_body=(0, -1.6, 0))
    a.at(8, chest=(-30, 0, 0), arm_r=(-20, 0, 70), arm_l=(-20, 0, -70), P_body=(0, -3.0, 0))
    a.at(12, chest=(10, 0, 0), head=(-10, 0, 0), arm_r=(120, 0, 40), arm_l=(120, 0, -40), fore_r=(20, 0, 0), fore_l=(20, 0, 0), P_body=(0, 0.6, 0))
    a.at(13, chest=(-4, -30, 0), arm_r=(150, -20, 50), fore_r=(30, 0, 0), arm_l=(40, 0, -30), head=(4, 20, 0), P_body=(0, 0, 0))
    a.at(15, chest=(-14, 30, 0), head=(6, -16, 0), arm_r=(40, 30, -30), fore_r=(10, 0, 0), arm_l=(20, 0, -20), P_body=(0, -0.6, -1.2))
    a.at(18, chest=(-8, 26, 0), arm_r=(10, 20, -20), arm_l=(150, 20, -50), fore_l=(30, 0, 0), head=(4, -14, 0))
    a.at(21, chest=(-16, -32, 0), head=(6, 18, 0), arm_l=(40, -30, 30), fore_l=(10, 0, 0), arm_r=(20, 0, 20), P_body=(0, -0.8, -2.0))
    a.at(25, chest=(-8, -16, 0), arm_l=(20, 0, -10), arm_r=(10, 0, 10), P_body=(0, -0.4, -1.6))
    a.at(30, chest=(0, 0, 0), head=r["head"], arm_r=r["arm_r"], arm_l=r["arm_l"], fore_r=r["fore_r"], fore_l=r["fore_l"], P_body=(0, 0, 0))
    a.legs([(0, 0, 0, 0), (8, -30, 0, 0), (12, 0, 0, 0), (30, 0, 0, 0)], [(0, 0, 0, 0), (8, -40, 0, 0), (12, 0, 0, 0), (15, -14, 0, 0), (21, -16, 0, 0), (30, 0, 0, 0)])
    a.at(15, leg_r=(-24, 0, 2), leg_l=(16, 0, -2)).at(21, leg_l=(-28, 0, -2), leg_r=(18, 0, 2)).at(27, leg_l=r["leg_l"], leg_r=r["leg_r"])
    a.hair([(0, 0, 0, 0), (6, -10, 0, 0), (12, 16, 0, 0), (15, -6, 0, -10), (21, -6, 0, 10), (27, 0, 0, 0)])
    a.cloth([(0, 0, 0, 0), (8, 0, 0, 0, 20), (12, -4, 0, 0, 6), (15, -6, 0, -8), (21, -8, 0, 8), (30, 0, 0, 0)])
    a.done()

    # ---------------------------------------------------------------- shadow_volley (40): float up, wings fan open, arms flick 10/14/18/22/26 (orbs from the wing tips)
    a = mk("shadow_volley", 40).show("wings", 2, 37, grow=3)
    a.pos("root", (0, 0, 0, 0), (8, 0, 3.2, 0), (14, 0, 3.6, 0), (20, 0, 3.0, 0), (26, 0, 3.6, 0), (32, 0, 3.0, 0), (40, 0, 0, 0))
    a.at(0, chest=(0, 0, 0))
    a.at(6, chest=(8, 0, 0), head=(8, 0, 0), arm_r=(10, 0, 40), arm_l=(10, 0, -40), fore_r=(30, 0, 0), fore_l=(30, 0, 0))
    wings_at(a, 3, spread=0.4, lift=10)
    for i, t in enumerate((10, 14, 18, 22, 26)):
        s = 1 if i % 2 == 0 else -1
        arm = "arm_r" if s > 0 else "arm_l"
        fore = "fore_r" if s > 0 else "fore_l"
        a.rot(arm, (t - 2, 20, 0, 50 * s), (t, 80, -10 * s, 20 * s), (t + 1.5, 70, 0, 26 * s))
        a.rot(fore, (t - 2, 60, 0, 0), (t, 0, 0, 0), (t + 1.5, 10, 0, 0))
        a.rot("chest", (t, 4, 10 * s, 0), (t + 1.5, 6, 6 * s, 0))
        wings_at(a, t - 1, spread=1.25, lift=-5)
        wings_at(a, t + 1, spread=1.1, lift=6)
    a.at(30, chest=(6, 0, 0), arm_r=(20, 0, 40), arm_l=(20, 0, -40), fore_r=(20, 0, 0), fore_l=(20, 0, 0), head=(6, 0, 0))
    wings_at(a, 34, spread=0.5, lift=30)
    a.at(40, chest=(0, 0, 0), head=r["head"], arm_r=r["arm_r"], arm_l=r["arm_l"], fore_r=r["fore_r"], fore_l=r["fore_l"])
    a.legs([(0, 0, 0, 0), (8, 10, 0, 2), (20, 6, 0, 4), (32, 10, 0, 2), (40, 0, 0, 0)], [(0, 0, 0, 0), (8, -30, 0, 0), (20, -24, 0, 0), (32, -30, 0, 0), (40, 0, 0, 0)],
           [(0, 0, 0, 0), (8, 40, 0, 0), (32, 40, 0, 0), (40, 0, 0, 0)])
    a.hair([(0, 0, 0, 0), (8, -6, 0, 0), (14, -4, 0, 4), (22, -4, 0, -4), (30, -6, 0, 0), (40, 0, 0, 0)], delay=3)
    a.cloth([(0, 0, 0, 0), (8, 6, 0, 0, 6), (16, 2, 0, 3, 8), (24, 2, 0, -3, 8), (32, 6, 0, 0, 6), (40, 0, 0, 0)], delay=3)
    a.done()

    # ---------------------------------------------------------------- grab_maul (48): crouch 0-7, POUNCE 8-11 grab, wing-stabs 18 & 28, hurl 38
    a = mk("grab_maul", 48).show("claws_r", 6, 42).show("claws_l", 6, 42).show("wings", 12, 42, grow=2)
    a.at(0, chest=(0, 0, 0), P_body=(0, 0, 0))
    a.at(6, chest=(-26, 0, 0), head=(22, 0, 0), arm_r=(-30, 0, 30), arm_l=(-30, 0, -30), fore_r=(40, 0, 0), fore_l=(40, 0, 0), P_body=(0, -2.4, 1.0))
    a.at(9, chest=(-20, 0, 0), head=(16, 0, 0), arm_r=(110, 0, 14), arm_l=(110, 0, -14), fore_r=(0, 0, 0), fore_l=(0, 0, 0), P_body=(0, 0.6, -2.4))
    a.at(11, chest=(-14, 0, 0), arm_r=(80, -20, -6), arm_l=(80, 20, 6), fore_r=(40, 0, 0), fore_l=(40, 0, 0), P_body=(0, -0.6, -2.6))
    wings_at(a, 12, spread=0.4, lift=40)
    for t, sgn in ((18, 1), (28, -1)):
        a.at(t - 3, chest=(-4, -8 * sgn, 0), head=(-4, 6 * sgn, 0))
        a.at(t, chest=(-22, 6 * sgn, 0), head=(14, -4 * sgn, 0), P_body=(0, -1.0, -2.6))
        wr, wl = ("wing_r1", "wing_l1") if sgn > 0 else ("wing_l1", "wing_r1")
        a.rot(wr, (t - 4, 80, 0, -50 * sgn), (t, -120, 0, -10 * sgn), (t + 3, -60, 0, -30 * sgn))
        a.rot(wl, (t - 4, 30, 0, 70 * sgn), (t, 40, 0, 80 * sgn))
    a.at(14, arm_r=(70, -30, -10), arm_l=(70, 30, 10), fore_r=(60, 0, 0), fore_l=(60, 0, 0))
    a.at(34, chest=(-6, -30, 0), head=(4, 20, 0), arm_r=(60, -40, -20), arm_l=(70, -10, 10), fore_r=(50, 0, 0), fore_l=(50, 0, 0), P_body=(0, -1.0, -2.0))
    a.at(38, chest=(-14, 40, 0), head=(0, -24, 0), arm_r=(40, 40, 60), arm_l=(80, 40, 10), fore_r=(0, 0, 0), fore_l=(10, 0, 0), P_body=(0, -0.8, -2.0))
    wings_at(a, 36, spread=1.2, lift=0); wings_at(a, 42, spread=0.4, lift=40)
    a.at(42, chest=(-6, 20, 0), arm_r=(20, 0, 30), arm_l=(30, 0, -10), P_body=(0, -0.4, -1.2))
    a.at(48, chest=(0, 0, 0), head=r["head"], arm_r=r["arm_r"], arm_l=r["arm_l"], fore_r=r["fore_r"], fore_l=r["fore_l"], P_body=(0, 0, 0))
    a.rot("leg_r", (0, *r["leg_r"]), (6, 30, 0, 4), (9, -40, 0, 2), (11, -30, 0, 2), (38, -30, 0, 2), (44, -6, 0, 0), (48, *r["leg_r"]))
    a.rot("leg_l", (0, *r["leg_l"]), (6, 20, 0, -4), (9, 30, 0, -2), (11, 24, 0, -2), (38, 24, 0, -2), (44, 4, 0, 0), (48, *r["leg_l"]))
    a.rot("shin_r", (0, 0, 0, 0), (6, -60, 0, 0), (9, -10, 0, 0), (11, -20, 0, 0), (38, -20, 0, 0), (48, 0, 0, 0))
    a.rot("shin_l", (0, 0, 0, 0), (6, -70, 0, 0), (9, -30, 0, 0), (11, -40, 0, 0), (38, -40, 0, 0), (48, 0, 0, 0))
    a.hair([(0, 0, 0, 0), (6, 6, 0, 0), (9, -16, 0, 0), (18, 8, 0, 4), (28, 8, 0, -4), (38, -6, 0, -12), (44, 0, 0, 0)])
    a.cloth([(0, 0, 0, 0), (6, 4, 0, 0, 4), (9, -14, 0, 0), (18, -4, 0, 2), (28, -4, 0, -2), (38, -4, 0, 10), (48, 0, 0, 0)])
    a.done()

    # ---------------------------------------------------------------- scream (36): hands to head, curl 4-11, SCREAM 14 (head thrown back, arms flung), shake, recover
    a = mk("scream", 36).show("wings", 12, 30, grow=1)
    a.at(0, chest=(0, 0, 0))
    a.at(5, chest=(-20, 0, 0), head=(-24, 0, 0), arm_r=(130, 30, 40), arm_l=(130, -30, -40), fore_r=(110, 0, 0), fore_l=(110, 0, 0), P_body=(0, -1.2, 0.4))
    a.at(11, chest=(-30, 0, 4), head=(-30, 0, 6), arm_r=(140, 30, 30), arm_l=(140, -30, -30), fore_r=(120, 0, 0), fore_l=(120, 0, 0), P_body=(0, -1.8, 0.6))
    a.at(14, chest=(22, 0, 0), head=(30, 0, 0), arm_r=(10, 0, 100), arm_l=(10, 0, -100), fore_r=(-10, 0, 0), fore_l=(-10, 0, 0), P_body=(0, 0.4, 0.8))
    for t in (16, 18, 20, 22):
        j = 1 if t % 4 == 0 else -1
        a.at(t, chest=(20, 0, 2 * j), head=(28, 3 * j, -3 * j), arm_r=(10, 0, 96 + 4 * j), arm_l=(10, 0, -96 + 4 * j))
    wings_at(a, 12, spread=0.3, lift=0); wings_at(a, 14, spread=1.3, lift=-20); wings_at(a, 24, spread=1.3, lift=-10); wings_at(a, 30, spread=0.5, lift=30)
    a.at(27, chest=(-6, 0, 0), head=(-6, 0, -2), arm_r=(10, 0, 20), arm_l=(10, 0, -20), fore_r=(20, 0, 0), fore_l=(20, 0, 0), P_body=(0, -0.4, 0.2))
    a.at(36, chest=(0, 0, 0), head=r["head"], arm_r=r["arm_r"], arm_l=r["arm_l"], fore_r=r["fore_r"], fore_l=r["fore_l"], P_body=(0, 0, 0))
    a.legs([(0, 0, 0, 0), (11, 10, 0, 0), (14, -6, 0, 8), (24, -6, 0, 8), (36, 0, 0, 0)], [(0, 0, 0, 0), (11, -24, 0, 0), (14, 0, 0, 0), (36, 0, 0, 0)])
    a.hair([(0, 0, 0, 0), (11, 10, 0, 0), (14, -26, 0, 0), (17, -22, 0, 6), (20, -24, 0, -6), (23, -22, 0, 4), (28, 0, 0, 0), (36, 0, 0, 0)], delay=1)
    a.cloth([(0, 0, 0, 0), (11, 4, 0, 0), (14, -10, 0, 0, 22), (22, -8, 0, 0, 18), (30, 0, 0, 0, 2), (36, 0, 0, 0)], delay=1)
    a.done()

    # ---------------------------------------------------------------- wing_burrow (40): rise 0-10, all wings plunge into the floor 12-14, hang over the rings 14-28, rip out 30-34
    a = mk("wing_burrow", 40).show("wings", 2, 37, grow=2)
    wings_at(a, 2, spread=0.4, lift=30); wings_at(a, 9, spread=1.2, lift=-30)
    down = {"wing_r0": (20, 0, -160), "wing_r1": (0, 0, -170), "wing_r2": (-20, 0, -160), "wing_l0": (20, 0, 160), "wing_l1": (0, 0, 170), "wing_l2": (-20, 0, 160)}
    for t in (14, 28):
        for b, v in down.items(): a.rot(b, (t, *v))
    a.scl("wing_r1", (0, 1, 1, 1), (12, 1, 1, 1), (14, 1, 1.4, 1), (28, 1, 1.4, 1), (32, 1, 1, 1))
    a.scl("wing_l1", (0, 1, 1, 1), (12, 1, 1, 1), (14, 1, 1.4, 1), (28, 1, 1.4, 1), (32, 1, 1, 1))
    wings_at(a, 32, spread=1.2, lift=-20); wings_at(a, 37, spread=0.3, lift=40)
    a.pos("root", (0, 0, 0, 0), (10, 0, 3.6, 0), (14, 0, 2.4, 0), (20, 0, 2.8, 0), (26, 0, 2.4, 0), (30, 0, 3.4, 0), (36, 0, 0, 0), (40, 0, 0, 0))
    a.at(0, chest=(0, 0, 0))
    a.at(10, chest=(14, 0, 0), head=(20, 0, 0), arm_r=(-20, 0, 60), arm_l=(-20, 0, -60), fore_r=(10, 0, 0), fore_l=(10, 0, 0))
    a.at(14, chest=(-24, 0, 0), head=(18, 0, 0), arm_r=(-30, 0, 40), arm_l=(-30, 0, -40), fore_r=(30, 0, 0), fore_l=(30, 0, 0))
    a.at(20, chest=(-22, 0, 3), head=(16, 0, 4))
    a.at(26, chest=(-22, 0, -3), head=(16, 0, -4))
    a.at(31, chest=(10, 0, 0), head=(4, 0, 0), arm_r=(10, 0, 50), arm_l=(10, 0, -50))
    a.at(40, chest=(0, 0, 0), head=r["head"], arm_r=r["arm_r"], arm_l=r["arm_l"], fore_r=r["fore_r"], fore_l=r["fore_l"])
    a.legs([(0, 0, 0, 0), (10, 4, 0, 4), (14, 20, 0, 6), (28, 20, 0, 6), (34, 4, 0, 2), (40, 0, 0, 0)], [(0, 0, 0, 0), (10, -20, 0, 0), (14, -50, 0, 0), (28, -50, 0, 0), (36, -6, 0, 0), (40, 0, 0, 0)],
           [(0, 0, 0, 0), (10, 30, 0, 0), (28, 30, 0, 0), (36, 0, 0, 0)])
    a.hair([(0, 0, 0, 0), (10, -10, 0, 0), (14, 14, 0, 0), (20, 6, 0, 4), (26, 6, 0, -4), (31, -10, 0, 0), (40, 0, 0, 0)])
    a.cloth([(0, 0, 0, 0), (10, -6, 0, 0, 6), (14, 6, 0, 0, 16), (28, 4, 0, 0, 12), (34, -4, 0, 0, 2), (40, 0, 0, 0)])
    a.done()

    # ---------------------------------------------------------------- skitter (26): drop low 0-5, DASH 6-13 (wings swept back), lance with both wings 15, skid
    a = mk("skitter", 26).show("wings", 3, 23, grow=2)
    a.at(0, chest=(0, 0, 0), P_body=(0, 0, 0))
    a.at(5, chest=(-40, 0, 0), head=(34, 0, 0), arm_r=(-50, 0, 20), arm_l=(-50, 0, -20), fore_r=(20, 0, 0), fore_l=(20, 0, 0), P_body=(0, -3.0, 1.0))
    a.at(10, chest=(-50, 0, 0), head=(44, 0, 0), arm_r=(-70, 0, 14), arm_l=(-70, 0, -14), P_body=(0, -3.4, -0.6))
    sweep = {"wing_r0": (70, 0, -30), "wing_r1": (80, 0, -40), "wing_r2": (90, 0, -50), "wing_l0": (70, 0, 30), "wing_l1": (80, 0, 40), "wing_l2": (90, 0, 50)}
    for t in (8, 12):
        for b, v in sweep.items(): a.rot(b, (t, *v))
    a.rot("wing_r1", (15, -100, 0, 14)).rot("wing_l1", (15, -100, 0, -14)).rot("wing_r0", (15, -80, 0, -30)).rot("wing_l0", (15, -80, 0, 30))
    a.scl("wing_r1", (0, 1, 1, 1), (13, 1, 1, 1), (15, 1, 1.5, 1), (19, 1, 1, 1)).scl("wing_l1", (0, 1, 1, 1), (13, 1, 1, 1), (15, 1, 1.5, 1), (19, 1, 1, 1))
    a.at(15, chest=(-24, 0, 0), head=(20, 0, 0), arm_r=(30, 0, 30), arm_l=(30, 0, -30), P_body=(0, -2.2, -1.2))
    wings_at(a, 20, spread=0.8, lift=20); wings_at(a, 23, spread=0.3, lift=40)
    a.at(20, chest=(-10, 0, 0), head=(6, 0, 0), arm_r=(10, 0, 20), arm_l=(10, 0, -20), P_body=(0, -1.0, 0))
    a.at(26, chest=(0, 0, 0), head=r["head"], arm_r=r["arm_r"], arm_l=r["arm_l"], fore_r=r["fore_r"], fore_l=r["fore_l"], P_body=(0, 0, 0))
    a.rot("leg_r", (0, *r["leg_r"]), (5, 50, 0, 6), (7, -30, 0, 4), (9, 40, 0, 4), (11, -30, 0, 4), (13, 40, 0, 4), (15, 50, 0, 4), (20, 20, 0, 2), (26, *r["leg_r"]))
    a.rot("leg_l", (0, *r["leg_l"]), (5, 40, 0, -6), (7, 40, 0, -4), (9, -30, 0, -4), (11, 40, 0, -4), (13, -30, 0, -4), (15, -20, 0, -4), (20, 6, 0, -2), (26, *r["leg_l"]))
    a.rot("shin_r", (0, 0, 0, 0), (5, -90, 0, 0), (9, -60, 0, 0), (13, -60, 0, 0), (15, -80, 0, 0), (20, -30, 0, 0), (26, 0, 0, 0))
    a.rot("shin_l", (0, 0, 0, 0), (5, -90, 0, 0), (9, -70, 0, 0), (13, -60, 0, 0), (15, -20, 0, 0), (20, -10, 0, 0), (26, 0, 0, 0))
    a.hair([(0, 0, 0, 0), (5, 10, 0, 0), (8, -24, 0, 0), (13, -24, 0, 0), (15, 10, 0, 0), (20, -4, 0, 0), (26, 0, 0, 0)], delay=1)
    a.cloth([(0, 0, 0, 0), (5, 4, 0, 0, 6), (8, -18, 0, 0, 4), (13, -18, 0, 0, 4), (16, 8, 0, 0, 6), (26, 0, 0, 0)], delay=1)
    a.done()

    # ---------------------------------------------------------------- ground_grasp (40): heel lifted 6-11, STOMP 14 (shadow hands erupt), clawing hand raised and CLENCHED 20-32
    a = mk("ground_grasp", 40).show("claws_r", 16, 36)
    a.at(0, chest=(0, 0, 0), P_body=(0, 0, 0))
    a.at(8, chest=(10, 10, 0), head=(4, -6, 0), arm_r=(20, 0, 40), arm_l=(20, 0, -40), fore_r=(30, 0, 0), fore_l=(30, 0, 0), P_body=(0, 0.6, 0))
    a.at(11, chest=(12, 12, 0), head=(6, -8, 0), P_body=(0, 0.9, 0))
    a.at(14, chest=(-12, -6, 0), head=(16, 4, 0), arm_r=(-20, 0, 30), arm_l=(-20, 0, -30), fore_r=(10, 0, 0), fore_l=(10, 0, 0), P_body=(0, -1.0, 0))
    a.at(20, chest=(4, 0, 0), head=(10, 0, 0), arm_r=(110, 0, 10), fore_r=(10, 0, 0), arm_l=(10, 0, -20), P_body=(0, 0, 0))
    a.at(24, arm_r=(150, 0, 10), fore_r=(30, 0, 0), chest=(8, 0, 0), head=(14, 0, 0))
    a.at(32, arm_r=(150, 0, 10), fore_r=(30, 0, 0), chest=(8, 0, 0))
    a.rot("claws_r", (0, 0, 0, 0), (20, 0, 0, 0), (24, -80, 0, 0), (32, -80, 0, 0), (36, 0, 0, 0))
    a.at(40, chest=(0, 0, 0), head=r["head"], arm_r=r["arm_r"], arm_l=r["arm_l"], fore_r=r["fore_r"], fore_l=r["fore_l"])
    a.rot("leg_r", (0, *r["leg_r"]), (8, 70, 0, 4), (11, 76, 0, 4), (14, -4, 0, 2), (18, 0, 0, 2), (40, *r["leg_r"]))
    a.rot("shin_r", (0, 0, 0, 0), (8, -70, 0, 0), (11, -60, 0, 0), (14, 0, 0, 0), (40, 0, 0, 0))
    a.rot("leg_l", (0, *r["leg_l"]), (8, -4, 0, -2), (14, -10, 0, -2), (40, *r["leg_l"]))
    a.rot("shin_l", (0, 0, 0, 0), (14, -20, 0, 0), (20, -4, 0, 0), (40, 0, 0, 0))
    a.hair([(0, 0, 0, 0), (11, -4, 0, 0), (14, 16, 0, 0), (18, -6, 0, 0), (24, -4, 0, 0), (40, 0, 0, 0)])
    a.cloth([(0, 0, 0, 0), (8, 4, 0, 6), (14, 4, 0, 0, 20), (20, 0, 0, 0, 6), (40, 0, 0, 0)], delay=1)
    a.done()

    # ---------------------------------------------------------------- shadow_clutch (60): ink pools in the palm 2-9, arm cocked back 10,
    # THRUST 12-14 (shadow arm shoots ~5 blocks out, talons open) SNATCH 14, reel in 14-24, hold aloft, SQUEEZE 28 & 37, hoist 42, SLAM 46, recover
    a = mk("shadow_clutch", 60).show("shand", 3, 54, grow=3)
    a.at(0, chest=(0, 0, 0), head=r["head"], arm_r=r["arm_r"], fore_r=r["fore_r"], arm_l=r["arm_l"], fore_l=r["fore_l"], P_body=(0, 0, 0))
    a.at(5, chest=(2, -10, 0), head=(6, 8, -2), arm_r=(30, 0, 16), fore_r=(50, 0, 0), arm_l=(10, 0, -14), P_body=(0, -0.2, 0.2))
    a.at(10, chest=(6, -30, 0), head=(4, 22, 0), arm_r=(60, -10, 30), fore_r=(70, 0, 0), arm_l=(40, 0, -30), fore_l=(30, 0, 0), P_body=(0, -0.6, 0.8))
    a.at(12, chest=(-8, 18, 0), head=(-2, -14, 0), arm_r=(84, 0, 4), fore_r=(0, 0, 0), arm_l=(-20, 0, -26), fore_l=(10, 0, 0), P_body=(0, -0.8, -1.4))
    a.at(14, chest=(-12, 24, 0), head=(-4, -18, 0), arm_r=(86, 0, 2), P_body=(0, -1.0, -1.8))
    a.at(17, chest=(-6, 20, 0), head=(-6, -14, 0), arm_r=(88, 0, 4), fore_r=(6, 0, 0))
    a.at(24, chest=(8, 10, 0), head=(6, -8, -4), arm_r=(96, 0, 6), fore_r=(4, 0, 0), arm_l=(10, 0, -20), fore_l=(20, 0, 0), P_body=(0, -0.2, 0.4))
    for t in (28, 37):  # squeeze: hunch into it, arm shudders, cruel head tilt
        a.at(t - 2, chest=(6, 6, 0), head=(8, -6, -6), arm_r=(98, 0, 6), fore_r=(0, 0, 0))
        a.at(t, chest=(-6, 12, 3), head=(-4, -10, 8), arm_r=(90, 4, 2), fore_r=(16, 0, 0), arm_l=(30, 0, -36), fore_l=(70, 0, 0), P_body=(0, -0.5, -0.2))
        a.at(t + 3, chest=(4, 8, -1), head=(6, -6, -4), arm_r=(96, 0, 6), fore_r=(6, 0, 0), arm_l=(12, 0, -20), fore_l=(24, 0, 0), P_body=(0, -0.2, 0.2))
    a.at(42, chest=(14, -6, 0), head=(16, 4, 0), arm_r=(168, 0, 10), fore_r=(10, 0, 0), arm_l=(40, 0, -40), fore_l=(20, 0, 0), P_body=(0, 0.4, 0.6))
    a.at(44, chest=(-10, 6, 0), arm_r=(120, 0, 6))
    a.at(46, chest=(-36, 10, 0), head=(26, -6, 0), arm_r=(52, 0, 4), fore_r=(0, 0, 0), arm_l=(-10, 0, -40), fore_l=(10, 0, 0), P_body=(0, -4.0, -1.4))
    a.at(50, chest=(-32, 8, 0), head=(24, -4, 0), arm_r=(54, 0, 6), P_body=(0, -3.6, -1.2))
    a.at(55, chest=(-8, 2, 0), head=(4, 0, -2), arm_r=(16, 0, 8), fore_r=(20, 0, 0), arm_l=(6, 0, -8), fore_l=(14, 0, 0), P_body=(0, -0.6, -0.2))
    a.at(60, chest=(0, 0, 0), head=r["head"], arm_r=r["arm_r"], fore_r=r["fore_r"], arm_l=r["arm_l"], fore_l=r["fore_l"], P_body=(0, 0, 0))
    sreach(a, (0, 0.4), (3, 0.4), (9, 0.9), (11, 1.0), (13, 7.5), (14, 8.2), (16, 7.6), (20, 4.0), (24, 1.6), (41, 1.6), (42, 1.3), (44, 1.8), (46, 2.1), (52, 1.8), (56, 0.6), (60, 0.4))
    sgrip(a, 0, 0); sgrip(a, 9, 10); sgrip(a, 12, 40); sgrip(a, 13.5, 46); sgrip(a, 14.5, -24); sgrip(a, 16, -18)
    for t in (28, 37):
        sgrip(a, t - 2, -16); sgrip(a, t, -34); sgrip(a, t + 3, -18)
    sgrip(a, 45, -18); sgrip(a, 47, 36); sgrip(a, 52, 20); sgrip(a, 60, 0)
    a.rot("shand", (0, 0, 0, 0), (12, 0, 0, 0), (14, -6, 0, 0), (24, 2, 0, 0), (28, 6, 0, 6), (31, 2, 0, -2), (37, 6, 0, -6), (40, 2, 0, 2),
          (42, 10, 0, 0), (46, -20, 0, 0), (52, -14, 0, 0), (60, 0, 0, 0))
    a.rot("leg_r", (0, *r["leg_r"]), (10, 14, 0, 2), (12, -24, 0, 2), (24, -16, 0, 2), (42, -10, 0, 2), (46, -34, 0, 4), (52, -30, 0, 4), (60, *r["leg_r"]))
    a.rot("leg_l", (0, *r["leg_l"]), (10, -12, 0, -2), (12, 22, 0, -2), (24, 12, 0, -2), (42, 6, 0, -2), (46, 30, 0, -4), (52, 28, 0, -4), (60, *r["leg_l"]))
    a.rot("shin_r", (0, 0, 0, 0), (12, -10, 0, 0), (24, -6, 0, 0), (46, -24, 0, 0), (52, -22, 0, 0), (60, 0, 0, 0))
    a.rot("shin_l", (0, 0, 0, 0), (12, -14, 0, 0), (24, -8, 0, 0), (46, -70, 0, 0), (52, -66, 0, 0), (60, 0, 0, 0))
    a.hair([(0, 0, 0, 0), (10, 8, 0, 6), (13, -14, 0, -8), (17, -6, 0, -4), (24, 4, 0, 0), (28, -4, 0, 4), (37, -4, 0, -4), (42, 8, 0, 0),
            (46, 22, 0, 4), (50, -6, 0, 0), (60, 0, 0, 0)])
    a.cloth([(0, 0, 0, 0), (10, 4, 0, 4), (13, -10, 0, -6), (24, 0, 0, 0, 2), (28, -2, 0, 0, 4), (37, -2, 0, 0, 4), (42, -4, 0, 0),
             (46, 12, 0, 0, 16), (52, 4, 0, 0, 8), (60, 0, 0, 0)])
    a.done()

    # ---------------------------------------------------------------- shadow_pin (50): arms flung up, rise on toes 0-10, DROP into a squat and drive
    # both palms into her shadow 14 (hands burst up under the victims), grind 16-28, CLENCH 30 (squeeze), strain, RIP arms up 44 (victims hurled), recover
    a = mk("shadow_pin", 50).show("claws_r", 8, 46).show("claws_l", 8, 46)
    a.scl("claws_r", (0, *HIDE), (7.99, *HIDE), (10, 1, 1, 1), (13, 1.3, 1.5, 1.3), (44, 1.3, 1.5, 1.3), (45.5, 1, 1, 1), (46, *HIDE), (50, *HIDE))
    a.scl("claws_l", (0, *HIDE), (7.99, *HIDE), (10, 1, 1, 1), (13, 1.3, 1.5, 1.3), (44, 1.3, 1.5, 1.3), (45.5, 1, 1, 1), (46, *HIDE), (50, *HIDE))
    a.at(0, chest=(0, 0, 0), head=r["head"], arm_r=r["arm_r"], fore_r=r["fore_r"], arm_l=r["arm_l"], fore_l=r["fore_l"], P_root=(0, 0, 0))
    a.at(6, chest=(4, 0, 0), head=(10, 0, 0), arm_r=(160, 0, 34), fore_r=(20, 0, 0), arm_l=(160, 0, -34), fore_l=(20, 0, 0), P_root=(0, 0.6, 0.2))
    a.at(10, chest=(6, 0, 0), head=(14, 0, 0), arm_r=(168, 0, 30), fore_r=(10, 0, 0), arm_l=(168, 0, -30), fore_l=(10, 0, 0), P_root=(0, 0.9, 0.2))
    a.at(12, chest=(-10, 0, 0), arm_r=(120, 0, 14), arm_l=(120, 0, -14))
    a.at(14, chest=(-44, 0, 0), head=(36, 0, 0), arm_r=(46, 0, 10), fore_r=(0, 0, 0), arm_l=(46, 0, -10), fore_l=(0, 0, 0), P_root=(0, -6.0, -1.0))
    for t in (17, 20, 23, 26):
        j = 1 if t % 2 else -1
        a.at(t, chest=(-42, 2 * j, 2 * j), head=(34, -4 * j, 3 * j), arm_r=(47, 0, 10 + j), arm_l=(47, 0, -10 + j), P_root=(0, -5.8, -1.0))
    a.at(28, chest=(-46, 0, 0), head=(30, 0, 0), arm_r=(44, 0, 12), arm_l=(44, 0, -12), P_root=(0, -6.0, -1.0))
    a.at(30, chest=(-36, 0, 0), head=(44, 0, -8), arm_r=(52, 0, 8), fore_r=(24, 0, 0), arm_l=(52, 0, -8), fore_l=(24, 0, 0), P_root=(0, -5.6, -1.0))
    a.at(33, chest=(-40, 0, 2), head=(40, 4, -6), arm_r=(48, 0, 10), fore_r=(18, 0, 0), arm_l=(48, 0, -10), fore_l=(18, 0, 0))
    a.at(40, chest=(-42, 0, -2), head=(38, -4, -6), arm_r=(46, 0, 10), fore_r=(20, 0, 0), arm_l=(46, 0, -10), fore_l=(20, 0, 0), P_root=(0, -5.8, -1.0))
    a.at(42, chest=(-48, 0, 0), head=(30, 0, 0), arm_r=(40, 0, 10), arm_l=(40, 0, -10), P_root=(0, -6.2, -1.1))
    a.at(44, chest=(20, 0, 0), head=(26, 0, 0), arm_r=(178, 0, 24), fore_r=(6, 0, 0), arm_l=(178, 0, -24), fore_l=(6, 0, 0), P_root=(0, 0.6, 0.2))
    a.at(46, chest=(16, 0, 0), head=(20, 0, 0), arm_r=(170, 0, 28), arm_l=(170, 0, -28), P_root=(0, 0.4, 0.2))
    a.at(50, chest=(0, 0, 0), head=r["head"], arm_r=r["arm_r"], fore_r=r["fore_r"], arm_l=r["arm_l"], fore_l=r["fore_l"], P_root=(0, 0, 0))
    for k in ("claws_r", "claws_l"):
        a.rot(k, (0, 0, 0, 0), (13, 20, 0, 0), (28, 20, 0, 0), (30, -80, 0, 0), (42, -80, 0, 0), (44, -20, 0, 0), (50, 0, 0, 0))
    for s, k in ((1, "r"), (-1, "l")):
        a.rot("leg_" + k, (0, *r["leg_" + k]), (10, -4, 0, 2 * s), (14, 80, 0, 22 * s), (42, 80, 0, 22 * s), (44, -6, 0, 6 * s), (50, *r["leg_" + k]))
        a.rot("shin_" + k, (0, 0, 0, 0), (10, 0, 0, 0), (14, -120, 0, 0), (42, -120, 0, 0), (44, 0, 0, 0), (50, 0, 0, 0))
        a.rot("foot_" + k, (0, 0, 0, 0), (8, 26, 0, 0), (12, 0, 0, 0), (14, 40, 0, 0), (42, 40, 0, 0), (44, 20, 0, 0), (47, 0, 0, 0), (50, 0, 0, 0))
    a.hair([(0, 0, 0, 0), (10, -10, 0, 0), (14, 26, 0, 0), (18, 8, 0, 4), (24, 8, 0, -4), (30, -10, 0, 0), (34, 6, 0, 0), (42, 8, 0, 0), (44, -24, 0, 0), (48, 4, 0, 0), (50, 0, 0, 0)])
    a.cloth([(0, 0, 0, 0), (10, -4, 0, 0, 2), (14, 8, 0, 0, 26), (28, 6, 0, 0, 22), (30, 4, 0, 0, 26), (42, 6, 0, 0, 22), (44, -8, 0, 0, 4), (50, 0, 0, 0)])
    a.done()

    # ---------------------------------------------------------------- transform (130; phase-1 model plays 0-90): clutch head, convulse (40/62/80), wings tear out, swell
    a = mk("transform", 130).show("wings", 38, 130, grow=4).show("claws_r", 60, 130).show("claws_l", 60, 130)
    a.scl("root", (0, 1, 1, 1), (40, 1, 1, 1), (62, 1.08, 1.08, 1.08), (80, 1.2, 1.2, 1.2), (90, 1.5, 1.5, 1.5), (130, 1.5, 1.5, 1.5))
    a.at(0, chest=(0, 0, 0), head=r["head"])
    a.at(8, chest=(-16, 0, 0), head=(-26, 0, 0), arm_r=(140, 30, 30), arm_l=(140, -30, -30), fore_r=(120, 0, 0), fore_l=(120, 0, 0), P_body=(0, -0.8, 0))
    for t in range(12, 38, 4):  # trembling hunch
        j = 1 if (t // 4) % 2 else -1
        a.at(t, chest=(-24 - t * 0.3, 3 * j, 3 * j), head=(-30, 4 * j, -4 * j), P_body=(0, -1.0 - t * 0.04, 0))
    for t0 in (40, 62, 80):  # convulsions
        big = 1 + (t0 - 40) / 40
        a.at(t0 - 2, chest=(-34, 0, 0), head=(-30, 0, 0), arm_r=(140, 30, 30), arm_l=(140, -30, -30), P_body=(0, -2.0, 0))
        a.at(t0, chest=(24 * big, 0, 0), head=(30, 0, 0), arm_r=(20, 0, 70 * big), arm_l=(20, 0, -70 * big), fore_r=(0, 0, 0), fore_l=(0, 0, 0), P_body=(0, 0.4, 0))
        if t0 < 80:
            a.at(t0 + 6, chest=(-20, 0, 6), head=(-20, 10, 0), arm_r=(60, 0, 30), arm_l=(60, 0, -30), fore_r=(60, 0, 0), fore_l=(60, 0, 0), P_body=(0, -1.6, 0))
    wings_at(a, 40, spread=0.6, lift=-10); wings_at(a, 50, spread=0.6, lift=20); wings_at(a, 62, spread=1.2, lift=-20); wings_at(a, 72, spread=0.9, lift=10)
    wings_at(a, 80, spread=1.4, lift=-30); wings_at(a, 90, spread=1.5, lift=-35)
    a.at(90, chest=(16, 0, 0), head=(20, 0, 0), arm_r=(10, 0, 90), arm_l=(10, 0, -90), fore_r=(-10, 0, 0), fore_l=(-10, 0, 0), P_body=(0, 0.6, 0))
    a.at(130, chest=(16, 0, 0), head=(20, 0, 0), arm_r=(10, 0, 90), arm_l=(10, 0, -90), fore_r=(-10, 0, 0), fore_l=(-10, 0, 0), P_body=(0, 0.6, 0))
    a.legs([(0, 0, 0, 0), (12, 10, 0, 4), (38, 14, 0, 6), (40, -4, 0, 8), (60, 14, 0, 6), (80, -4, 0, 10), (90, 0, 0, 12), (130, 0, 0, 12)],
           [(0, 0, 0, 0), (12, -20, 0, 0), (38, -30, 0, 0), (40, 0, 0, 0), (60, -30, 0, 0), (80, 0, 0, 0), (130, 0, 0, 0)])
    a.hair([(0, 0, 0, 0), (8, 10, 0, 0), (20, 10, 0, 6), (30, 10, 0, -6), (40, -24, 0, 0), (50, 10, 0, 6), (62, -26, 0, 0), (72, 10, 0, -6), (80, -30, 0, 0), (90, -30, 0, 8), (130, -30, 0, 8)], delay=1)
    a.cloth([(0, 0, 0, 0), (12, 2, 0, 0, 4), (40, -10, 0, 0, 20), (50, 2, 0, 0, 8), (62, -10, 0, 0, 26), (72, 2, 0, 0, 10), (80, -12, 0, 0, 34), (130, -12, 0, 0, 34)], delay=1)
    a.done()

    # ---------------------------------------------------------------- death (40): clutch chest, knees give 8-16, topple sideways 22, dissolve into shadow 28-40
    a = mk("death", 40).show("wings", 4, 30, grow=3)
    wings_at(a, 4, spread=1.3, lift=-20); wings_at(a, 14, spread=0.6, lift=40); wings_at(a, 30, spread=0.2, lift=80)
    a.at(0, chest=(0, 0, 0), P_root=(0, 0, 0), root=(0, 0, 0))
    a.at(5, chest=(-20, 0, 0), head=(-14, 0, 0), arm_r=(60, 40, 0), arm_l=(60, -40, 0), fore_r=(90, 0, 0), fore_l=(90, 0, 0), P_body=(0, -0.6, 0))
    a.at(14, chest=(-30, 0, 10), head=(-20, 0, 14), arm_r=(10, 0, 30), arm_l=(60, -40, 0), P_body=(0, -5.0, 0))
    a.at(24, root=(0, 0, 80), P_root=(4, 0.8, 0), chest=(-10, 0, 6), head=(10, 0, 10), arm_r=(10, 0, 70), fore_r=(10, 0, 0))
    a.at(40, root=(0, 0, 90), P_root=(5.5, 0.0, 0))
    a.scl("root", (0, 1, 1, 1), (28, 1, 1, 1), (40, 1.2, 0.05, 1.2))
    a.legs([(0, 0, 0, 0), (14, 60, 0, 4), (24, 30, 0, 8), (40, 20, 0, 6)], [(0, 0, 0, 0), (14, -100, 0, 0), (24, -50, 0, 0), (40, -40, 0, 0)])
    a.hair([(0, 0, 0, 0), (5, 10, 0, 0), (14, 10, 0, 10), (24, -10, 0, 30), (32, 0, 0, 24), (40, 0, 0, 24)], delay=2)
    a.cloth([(0, 0, 0, 0), (14, 10, 0, 0, 20), (24, -6, 0, 20, 6), (40, -6, 0, 20, 6)])
    a.done()


# ================================================================== PHASE 2 animations
TENT_REST = {0: (-50, 25, 0), 1: (-50, -25, 0), 2: (-25, 45, 0), 3: (-25, -45, 0)}
REST2 = {"chest": (-14, 0, 0), "head": (12, 0, -6), "arm_r": (14, 0, 36), "fore_r": (46, 0, 0), "arm_l": (6, 0, -10), "fore_l": (14, 0, 0),
         "leg_r": (10, 0, 6), "leg_l": (10, 0, -6), "shin_r": (-16, 0, 0), "shin_l": (-16, 0, 0), "foot_r": (6, 0, 0), "foot_l": (6, 0, 0),
         **{f"tent{t}_0": v for t, v in TENT_REST.items()}, **{f"tent{t}_{i}": (26, 0, 0) for t in range(4) for i in (1, 2, 3)},
         **{f"fing_{k}{i}": (14, 0, 0) for k in "rl" for i in range(4)}, **WR}
PROPS2 = ("wings", "beam")


def anims_p2(B):
    def mk(name, ticks, loop=False):
        return A(B, name, ticks, REST2, PROPS2, loop)
    r = REST2

    def claw(a, side, t, curl, spread=0.0):
        for i in range(4):
            a.rot(f"fing_{side}{i}", (t, 14 + curl, 0, (i - 1.5) * spread * (1 if side == "r" else -1)))
        a.rot("thumb_" + side, (t, curl * 0.6, 0, 0))

    def claws(a, t, curl, spread=0.0):
        claw(a, "r", t, curl, spread); claw(a, "l", t, curl, spread)

    def tent(a, i, keys, lag=1.5):
        """keys: (t, (rx,ry,rz) of root, curl per segment)"""
        for (t, base, curl) in keys:
            a.rot(f"tent{i}_0", (t, *base))
            for s in (1, 2, 3):
                a.rot(f"tent{i}_{s}", (min(a.ticks, t + lag * s), curl, 0, 0))

    def tents(a, keys, lag=1.5, spread=1.0):
        """all four: keys (t, rx_add, curl, splay) relative to rest"""
        for i in range(4):
            bx, by, bz = TENT_REST[i]
            tent(a, i, [(t, (bx + rx, by * (spread if sp is None else sp), bz), c) for (t, rx, c, sp) in keys], lag)

    def tail(a, keys, lag=1.5):
        """keys (t, yaw, lift, curl): tail0 gets yaw+lift, rest get yaw*0.4 and curl"""
        for (t, yaw, lift, curl) in keys:
            a.rot("tail0", (t, lift, yaw, 0))
            for i in range(1, 6):
                a.rot(f"tail{i}", (min(a.ticks, t + lag * i), curl, yaw * 0.35, 0))

    def spines(a, t, flare):
        a.rot("spines_r", (t, -flare * 0.3, 0, -flare)); a.rot("spines_l", (t, -flare * 0.3, 0, flare))

    def rest_tail_tents(a, t):
        tail(a, [(t, 0, 0, 0)]); tents(a, [(t, 0, 26, None)])

    # ---------------------------------------------------------------- idle (80): heavy breathing, twitching head, tail + tentacles undulate, claws flex
    a = mk("idle", 80, loop=True)
    a.at(0, chest=(-14, 0, 0), head=(12, 0, -6), P_body=(0, 0, 0))
    a.at(20, chest=(-10, 2, 0), head=(14, -4, -4), P_body=(0, 0.12, 0))
    a.at(40, chest=(-14, 0, 0), head=(12, 0, -6), P_body=(0, 0, 0))
    a.at(48, head=(12, 0, -6)).at(50, head=(6, 14, 10)).at(53, head=(10, 12, 8)).at(56, head=(12, 0, -6))
    a.at(60, chest=(-10, -2, 0), P_body=(0, 0.12, 0))
    a.at(80, chest=(-14, 0, 0), head=(12, 0, -6), P_body=(0, 0, 0))
    a.at(0, arm_r=r["arm_r"], arm_l=r["arm_l"]).at(40, arm_r=(18, 0, 40), arm_l=(8, 0, -12)).at(80, arm_r=r["arm_r"], arm_l=r["arm_l"])
    claws(a, 0, 0); claws(a, 30, 0); claws(a, 34, 40); claws(a, 38, -10); claws(a, 44, 0); claws(a, 80, 0)
    tail(a, [(0, -12, 0, -6), (20, 0, 4, 0), (40, 12, 0, -6), (60, 0, 4, 0), (80, -12, 0, -6)], lag=3)
    for i in range(4):
        ph = i * 10
        bx, by, bz = TENT_REST[i]
        tent(a, i, [(0, (bx, by, bz), 26), (20, (bx + 8, by + 6, bz), 34), (40, (bx, by, bz), 22), (60, (bx - 6, by - 6, bz), 30), (80, (bx, by, bz), 26)], lag=3)
    spines(a, 0, 0); spines(a, 20, 6); spines(a, 40, 0); spines(a, 60, 6); spines(a, 80, 0)
    a.hair([(0, 0, 0, 1), (20, 2, 0, -1), (40, 0, 0, 1), (60, 2, 0, -1), (80, 0, 0, 1)], delay=5)
    a.cloth([(0, 0, 0, 1), (20, 1, 0, -1), (40, 0, 0, 1), (60, 1, 0, -1), (80, 0, 0, 1)], delay=5)
    a.done()

    # ---------------------------------------------------------------- walk (20, additive): lumbering, heavy stomps, claws dragging, tail swinging opposite
    a = mk("walk", 20, loop=True)
    a.rot("leg_r", (0, 22, 0, 0), (5, 0, 0, 0), (10, -20, 0, 0), (15, 0, 0, 0), (20, 22, 0, 0))
    a.rot("shin_r", (0, 0, 0, 0), (10, -6, 0, 0), (13, -40, 0, 0), (17, -20, 0, 0), (20, 0, 0, 0))
    a.rot("leg_l", (0, -20, 0, 0), (5, 0, 0, 0), (10, 22, 0, 0), (15, 0, 0, 0), (20, -20, 0, 0))
    a.rot("shin_l", (0, -6, 0, 0), (3, -40, 0, 0), (7, -20, 0, 0), (10, 0, 0, 0), (20, -6, 0, 0))
    a.pos("body", (0, 0, -0.6, 0), (2, 0, -0.8, 0), (6, 0, 0.3, 0), (10, 0, -0.6, 0), (12, 0, -0.8, 0), (16, 0, 0.3, 0), (20, 0, -0.6, 0))
    a.rot("body", (0, 0, 6, 3), (10, 0, -6, -3), (20, 0, 6, 3))
    a.rot("chest", (0, -3, -8, -2), (10, -3, 8, 2), (20, -3, -8, -2))
    a.rot("arm_r", (0, -16, 0, 0), (10, 18, 0, 0), (20, -16, 0, 0))
    a.rot("arm_l", (0, 18, 0, 0), (10, -16, 0, 0), (20, 18, 0, 0))
    a.rot("head", (0, 2, 4, 0), (10, 2, -4, 0), (20, 2, 4, 0))
    a.rot("tail0", (0, 0, -12, 0), (10, 0, 12, 0), (20, 0, -12, 0))
    for i in range(1, 6):
        d = i * 1.5
        a.rot(f"tail{i}", (0, 0, -6, 0), (d % 20, 0, -8, 0), ((10 + d) % 20, 0, 8, 0), (20, 0, -6, 0))
    a.hair([(0, -3, 0, 2), (10, -3, 0, -2), (20, -3, 0, 2)], delay=2)
    a.cloth([(0, -5, 0, 3), (5, -7, 0, 0), (10, -5, 0, -3), (15, -7, 0, 0), (20, -5, 0, 3)], delay=1)
    a.done(base_layer=True)

    # ---------------------------------------------------------------- tentacle_field (46): rear up 0-14, SMASH 18 (claws + tentacles dive into the floor), hold, rip out 34-40
    a = mk("tentacle_field", 46)
    a.at(0, chest=r["chest"], head=r["head"], arm_r=r["arm_r"], arm_l=r["arm_l"], fore_r=r["fore_r"], fore_l=r["fore_l"], P_body=(0, 0, 0))
    a.at(8, chest=(12, 0, 0), head=(24, 0, 0), arm_r=(150, 0, 30), arm_l=(150, 0, -30), fore_r=(30, 0, 0), fore_l=(30, 0, 0), P_body=(0, 1.0, 0.4))
    a.at(14, chest=(18, 0, 0), head=(28, 0, 0), arm_r=(175, 0, 20), arm_l=(175, 0, -20), fore_r=(20, 0, 0), fore_l=(20, 0, 0), P_body=(0, 1.4, 0.6))
    a.at(18, chest=(-56, 0, 0), head=(40, 0, 0), arm_r=(60, 0, 14), arm_l=(60, 0, -14), fore_r=(0, 0, 0), fore_l=(0, 0, 0), P_body=(0, -3.6, -1.4))
    a.at(22, chest=(-52, 0, 2), head=(36, 0, 0), P_body=(0, -3.3, -1.3))
    a.at(30, chest=(-50, 0, -2), head=(34, 4, 0), arm_r=(62, 0, 16), arm_l=(62, 0, -16), P_body=(0, -3.2, -1.2))
    a.at(36, chest=(-30, 0, 0), head=(20, 0, 0), arm_r=(80, 0, 30), arm_l=(80, 0, -30), fore_r=(40, 0, 0), fore_l=(40, 0, 0), P_body=(0, -1.6, -0.6))
    a.at(46, chest=r["chest"], head=r["head"], arm_r=r["arm_r"], arm_l=r["arm_l"], fore_r=r["fore_r"], fore_l=r["fore_l"], P_body=(0, 0, 0))
    claws(a, 0, 0); claws(a, 14, -20, 10); claws(a, 18, 50, 16); claws(a, 34, 50, 16); claws(a, 40, 0); claws(a, 46, 0)
    tents(a, [(0, 0, 26, None), (10, -40, 40, 1.3), (16, -50, 50, 1.3), (19, 200, -6, 0.8), (34, 200, -6, 0.8), (40, -20, 30, None), (46, 0, 26, None)], lag=1)
    tail(a, [(0, 0, 0, 0), (14, 0, -20, 10), (18, 0, 30, -20), (34, 0, 30, -20), (46, 0, 0, 0)])
    spines(a, 0, 0); spines(a, 14, -10); spines(a, 18, 20); spines(a, 34, 16); spines(a, 46, 0)
    a.legs([(0, 10, 0, 6), (14, 0, 0, 4), (18, 40, 0, 12), (34, 40, 0, 12), (46, 10, 0, 6)], [(0, -16, 0, 0), (14, -4, 0, 0), (18, -60, 0, 0), (34, -60, 0, 0), (46, -16, 0, 0)])
    a.hair([(0, 0, 0, 0), (14, -10, 0, 0), (18, 22, 0, 0), (24, -6, 0, 0), (34, 0, 0, 0), (40, -6, 0, 0), (46, 0, 0, 0)])
    a.cloth([(0, 0, 0, 0), (14, -4, 0, 0), (18, 10, 0, 0, 20), (26, 4, 0, 0, 12), (40, 0, 0, 0, 2), (46, 0, 0, 0)])
    a.done()

    # ---------------------------------------------------------------- spike_carpet (48): crouch + claws wide 0-10, RAKE the floor right-to-left 12-16, left follows 18, hold, rise
    a = mk("spike_carpet", 48)
    a.at(0, chest=r["chest"], head=r["head"], arm_r=r["arm_r"], arm_l=r["arm_l"], fore_r=r["fore_r"], fore_l=r["fore_l"], P_body=(0, 0, 0), body=(0, 0, 0))
    a.at(9, chest=(-40, -34, 0), head=(30, 24, 0), arm_r=(50, 0, 80), fore_r=(10, 0, 0), arm_l=(30, 0, -40), P_body=(0, -2.6, 0))
    a.at(13, chest=(-50, 10, 0), head=(36, -6, 0), arm_r=(60, 40, 20), fore_r=(0, 0, 0), P_body=(0, -3.0, -0.8))
    a.at(16, chest=(-50, 34, 0), head=(34, -20, 0), arm_r=(50, 60, -30), arm_l=(60, 0, -60), fore_l=(0, 0, 0), P_body=(0, -3.0, -1.2))
    a.at(20, chest=(-48, 10, 0), arm_l=(60, -50, 20), arm_r=(40, 30, 10), P_body=(0, -2.8, -1.2))
    a.at(32, chest=(-44, 6, 0), head=(32, 0, 0), arm_l=(56, -40, 10), arm_r=(44, 20, 10), P_body=(0, -2.6, -1.0))
    a.at(40, chest=(-24, 0, 0), head=(18, 0, 0), arm_r=(30, 0, 40), arm_l=(20, 0, -20), fore_r=(40, 0, 0), fore_l=(20, 0, 0), P_body=(0, -0.8, -0.3))
    a.at(48, chest=r["chest"], head=r["head"], arm_r=r["arm_r"], arm_l=r["arm_l"], fore_r=r["fore_r"], fore_l=r["fore_l"], P_body=(0, 0, 0))
    claws(a, 0, 0); claws(a, 9, -20, 18); claws(a, 13, 60, 10); claws(a, 20, 60, 10); claws(a, 36, 30); claws(a, 48, 0)
    tents(a, [(0, 0, 26, None), (9, -20, 40, 1.4), (16, 20, 10, 1.6), (32, 10, 20, 1.4), (48, 0, 26, None)])
    tail(a, [(0, 0, 0, 0), (9, 30, 0, -10), (16, -40, 10, -20), (24, -20, 0, -10), (48, 0, 0, 0)])
    spines(a, 0, 0); spines(a, 13, 18); spines(a, 30, 12); spines(a, 48, 0)
    a.legs([(0, 10, 0, 6), (9, 40, 0, 16), (32, 40, 0, 16), (40, 20, 0, 8), (48, 10, 0, 6)], [(0, -16, 0, 0), (9, -70, 0, 0), (32, -70, 0, 0), (48, -16, 0, 0)])
    a.hair([(0, 0, 0, 0), (9, 6, 0, 10), (14, 10, 0, -14), (20, 6, 0, -6), (40, 0, 0, 0), (48, 0, 0, 0)])
    a.cloth([(0, 0, 0, 0), (9, 6, 0, 6, 10), (16, 6, 0, -10, 14), (32, 4, 0, -4, 10), (48, 0, 0, 0)])
    a.done()

    # ---------------------------------------------------------------- claw_slam (44): right claw hauled up and back 4-16, SLAM 21 (body follows), crater hold, recover
    a = mk("claw_slam", 44)
    a.at(0, chest=r["chest"], head=r["head"], arm_r=r["arm_r"], fore_r=r["fore_r"], arm_l=r["arm_l"], P_body=(0, 0, 0))
    a.at(8, chest=(6, -20, 0), head=(20, 10, 0), arm_r=(170, 0, 30), fore_r=(60, 0, 0), arm_l=(40, 0, -30), P_body=(0, 0.6, 0.8))
    a.at(16, chest=(16, -26, 0), head=(26, 14, 0), arm_r=(200, 0, 20), fore_r=(70, 0, 0), arm_l=(50, 0, -40), P_body=(0, 1.0, 1.2))
    a.at(19, chest=(-30, 10, 0), arm_r=(130, 0, 10), fore_r=(10, 0, 0))
    a.at(21, chest=(-58, 14, 0), head=(42, -8, 0), arm_r=(70, 0, 4), fore_r=(0, 0, 0), arm_l=(-20, 0, -40), P_body=(0, -3.6, -1.6))
    a.at(24, chest=(-54, 12, 2), head=(38, -6, 0), arm_r=(72, 0, 6), P_body=(0, -3.4, -1.5))
    a.at(32, chest=(-46, 8, 0), head=(30, 0, 0), arm_r=(68, 0, 8), P_body=(0, -3.0, -1.2))
    a.at(38, chest=(-24, 0, 0), arm_r=(40, 0, 30), fore_r=(40, 0, 0), arm_l=(10, 0, -16), P_body=(0, -1.0, -0.4))
    a.at(44, chest=r["chest"], head=r["head"], arm_r=r["arm_r"], fore_r=r["fore_r"], arm_l=r["arm_l"], P_body=(0, 0, 0))
    claw(a, "r", 0, 0); claw(a, "r", 14, -30, 24); claw(a, "r", 21, 40, 30); claw(a, "r", 32, 40, 24); claw(a, "r", 44, 0)
    tents(a, [(0, 0, 26, None), (14, -40, 40, 1.5), (21, 30, 0, 1.6), (32, 20, 10, 1.4), (44, 0, 26, None)])
    tail(a, [(0, 0, 0, 0), (16, 20, -30, 20), (21, -10, 40, -30), (34, 0, 20, -10), (44, 0, 0, 0)])
    spines(a, 0, 0); spines(a, 16, -8); spines(a, 21, 22); spines(a, 44, 0)
    a.rot("leg_r", (0, *r["leg_r"]), (16, 0, 0, 6), (21, -30, 0, 8), (32, -30, 0, 8), (44, *r["leg_r"]))
    a.rot("leg_l", (0, *r["leg_l"]), (16, 20, 0, -6), (21, 40, 0, -10), (32, 40, 0, -10), (44, *r["leg_l"]))
    a.rot("shin_l", (0, *r["shin_l"]), (16, -30, 0, 0), (21, -70, 0, 0), (32, -70, 0, 0), (44, *r["shin_l"]))
    a.hair([(0, 0, 0, 0), (16, -10, 0, 6), (21, 24, 0, -4), (26, -6, 0, 0), (44, 0, 0, 0)])
    a.cloth([(0, 0, 0, 0), (16, -6, 0, 4), (21, 12, 0, 0, 22), (28, 4, 0, 0, 10), (44, 0, 0, 0)])
    a.done()

    # ---------------------------------------------------------------- double_sweep (46): right claw out wide 4-11, SWEEP 15, left claw cocked 20-23, BACKSWEEP 27
    a = mk("double_sweep", 46)
    a.at(0, chest=r["chest"], head=r["head"], arm_r=r["arm_r"], arm_l=r["arm_l"], fore_r=r["fore_r"], fore_l=r["fore_l"], body=(0, 0, 0))
    a.at(10, body=(0, -30, 0), chest=(-10, -30, 0), head=(14, 40, 0), arm_r=(30, 0, 100), fore_r=(10, 0, 0), arm_l=(30, 0, -20), P_body=(0, -0.8, 0))
    a.at(15, body=(0, 30, 0), chest=(-20, 40, 0), head=(18, -30, 0), arm_r=(80, 80, 70), fore_r=(0, 0, 0), P_body=(0, -1.4, -0.8))
    a.at(18, body=(0, 34, 0), chest=(-18, 44, 0), arm_r=(60, 80, 40), arm_l=(30, 0, -100), fore_l=(10, 0, 0))
    a.at(23, body=(0, 34, 0), chest=(-12, 44, 0), head=(14, -40, 0), arm_l=(30, 0, -104), arm_r=(30, 30, 40), fore_r=(40, 0, 0))
    a.at(27, body=(0, -30, 0), chest=(-20, -40, 0), head=(18, 30, 0), arm_l=(80, -80, -70), fore_l=(0, 0, 0), P_body=(0, -1.4, -1.6))
    a.at(31, body=(0, -34, 0), chest=(-18, -44, 0), arm_l=(60, -80, -40))
    a.at(38, body=(0, -10, 0), chest=(-14, -10, 0), head=(12, 6, 0), arm_l=(20, 0, -20), arm_r=r["arm_r"], fore_l=(20, 0, 0), P_body=(0, -0.4, -0.6))
    a.at(46, body=(0, 0, 0), chest=r["chest"], head=r["head"], arm_r=r["arm_r"], arm_l=r["arm_l"], fore_r=r["fore_r"], fore_l=r["fore_l"], P_body=(0, 0, 0))
    claw(a, "r", 0, 0); claw(a, "r", 10, -24, 30); claw(a, "r", 15, 10, 30); claw(a, "r", 22, 20); claw(a, "r", 46, 0)
    claw(a, "l", 0, 0); claw(a, "l", 20, -24, 30); claw(a, "l", 27, 10, 30); claw(a, "l", 34, 20); claw(a, "l", 46, 0)
    tail(a, [(0, 0, 0, 0), (10, 40, 0, -10), (15, -50, 10, -14), (23, -40, 0, -10), (27, 50, 10, -14), (34, 30, 0, -6), (46, 0, 0, 0)], lag=1.2)
    tents(a, [(0, 0, 26, None), (10, -20, 30, 1.5), (15, -10, 16, 1.7), (27, -10, 16, 1.7), (36, -10, 22, 1.4), (46, 0, 26, None)])
    spines(a, 0, 0); spines(a, 15, 16); spines(a, 27, 16); spines(a, 46, 0)
    a.legs([(0, 10, 0, 6), (10, 16, 0, 10), (15, 16, 0, 12), (27, 16, 0, 12), (46, 10, 0, 6)], [(0, -16, 0, 0), (15, -34, 0, 0), (27, -34, 0, 0), (46, -16, 0, 0)])
    a.hair([(0, 0, 0, 0), (10, 4, 0, 14), (15, -6, 0, -20), (23, 0, 0, -10), (27, -6, 0, 20), (34, 0, 0, 6), (46, 0, 0, 0)], delay=1)
    a.cloth([(0, 0, 0, 0), (10, 2, 0, 10, 4), (15, -4, 0, -16, 14), (27, -4, 0, 16, 14), (36, 0, 0, 4, 4), (46, 0, 0, 0)], delay=1)
    a.done()

    # ---------------------------------------------------------------- grab_crush (56): reach 6-14, SNATCH 16, hoist 16-24, CRUSH 26 & 36, overhead 42, SMASH down 46
    a = mk("grab_crush", 56)
    a.at(0, chest=r["chest"], head=r["head"], arm_r=r["arm_r"], fore_r=r["fore_r"], arm_l=r["arm_l"], P_body=(0, 0, 0))
    a.at(10, chest=(-30, 10, 0), head=(26, -6, 0), arm_r=(90, 0, 10), fore_r=(0, 0, 0), arm_l=(30, 0, -30), P_body=(0, -1.0, -0.8))
    a.at(16, chest=(-34, 14, 0), head=(28, -8, 0), arm_r=(96, 0, 4), P_body=(0, -1.2, -1.2))
    a.at(22, chest=(-6, 4, 0), head=(26, -4, 0), arm_r=(150, 0, 12), fore_r=(20, 0, 0), arm_l=(20, 0, -20), P_body=(0, 0, -0.4))
    for t in (26, 36):
        a.at(t - 2, chest=(-2, 0, 0), head=(30, -6, 0), arm_r=(150, 0, 14), fore_r=(30, 0, 0))
        a.at(t, chest=(-12, 8, 4), head=(20, 10, 8), arm_r=(140, 0, 8), fore_r=(50, 0, 0), arm_l=(40, 0, -50), P_body=(0, -0.4, -0.4))
        a.at(t + 3, chest=(-8, 2, -2), head=(28, -4, -4), arm_r=(148, 0, 12), fore_r=(36, 0, 0), arm_l=(20, 0, -24))
    a.at(42, chest=(12, -10, 0), head=(30, 6, 0), arm_r=(200, 0, 10), fore_r=(40, 0, 0), arm_l=(60, 0, -40), P_body=(0, 0.8, 0.6))
    a.at(46, chest=(-56, 10, 0), head=(40, -6, 0), arm_r=(60, 0, 6), fore_r=(0, 0, 0), arm_l=(0, 0, -40), P_body=(0, -3.4, -1.4))
    a.at(50, chest=(-50, 8, 0), arm_r=(64, 0, 8), P_body=(0, -3.0, -1.2))
    a.at(56, chest=r["chest"], head=r["head"], arm_r=r["arm_r"], fore_r=r["fore_r"], arm_l=r["arm_l"], P_body=(0, 0, 0))
    claw(a, "r", 0, 0); claw(a, "r", 12, -30, 30); claw(a, "r", 16, 70, 4); claw(a, "r", 25, 70); claw(a, "r", 26, 95); claw(a, "r", 29, 75)
    claw(a, "r", 35, 75); claw(a, "r", 36, 95); claw(a, "r", 39, 75); claw(a, "r", 45, 75); claw(a, "r", 47, -30, 30); claw(a, "r", 56, 0)
    claw(a, "l", 0, 0); claw(a, "l", 26, 40); claw(a, "l", 36, 40); claw(a, "l", 46, -20, 20); claw(a, "l", 56, 0)
    tents(a, [(0, 0, 26, None), (14, -30, 30, 1.5), (26, -60, 50, 0.9), (36, -60, 50, 0.9), (42, -70, 40, 1.2), (46, 30, 0, 1.6), (56, 0, 26, None)])
    tail(a, [(0, 0, 0, 0), (16, -20, 0, -10), (26, 20, 10, -24), (36, -20, 10, -24), (46, 0, 40, -30), (56, 0, 0, 0)])
    spines(a, 0, 0); spines(a, 26, 14); spines(a, 36, 14); spines(a, 46, 24); spines(a, 56, 0)
    a.legs([(0, 10, 0, 6), (16, 20, 0, 8), (24, 6, 0, 6), (46, 30, 0, 12), (56, 10, 0, 6)], [(0, -16, 0, 0), (16, -36, 0, 0), (24, -10, 0, 0), (46, -50, 0, 0), (56, -16, 0, 0)])
    a.hair([(0, 0, 0, 0), (16, 10, 0, 0), (26, -6, 0, 10), (36, -6, 0, -10), (42, -14, 0, 0), (46, 22, 0, 0), (56, 0, 0, 0)])
    a.cloth([(0, 0, 0, 0), (16, -6, 0, 0, 4), (26, 2, 0, 6, 6), (36, 2, 0, -6, 6), (46, 10, 0, 0, 20), (56, 0, 0, 0)])
    a.done()

    # ---------------------------------------------------------------- tentacle_bind (70): rear back, tentacles coil overhead 0-12, PLUNGE into the floor 16,
    # bind 20 (claws snap shut), puppeteer-hoist 20-30, SQUEEZE 34 & 44 (claws crush, tentacles jolt), haul overhead 50, SLAM 54, rip out 58-64, recover
    a = mk("tentacle_bind", 70)
    a.at(0, chest=r["chest"], head=r["head"], arm_r=r["arm_r"], fore_r=r["fore_r"], arm_l=r["arm_l"], fore_l=r["fore_l"], P_body=(0, 0, 0))
    a.at(8, chest=(8, 0, 0), head=(26, 0, 0), arm_r=(40, 0, 70), fore_r=(30, 0, 0), arm_l=(40, 0, -70), fore_l=(30, 0, 0), P_body=(0, 0.8, 0.6))
    a.at(12, chest=(12, 0, 0), head=(30, 0, 0), arm_r=(50, 0, 80), fore_r=(20, 0, 0), arm_l=(50, 0, -80), fore_l=(20, 0, 0), P_body=(0, 1.0, 0.8))
    a.at(16, chest=(-34, 0, 0), head=(36, 0, 0), arm_r=(80, 0, 20), fore_r=(0, 0, 0), arm_l=(80, 0, -20), fore_l=(0, 0, 0), P_body=(0, -2.4, -1.2))
    a.at(20, chest=(-30, 0, 0), head=(34, 0, 0), arm_r=(92, 0, 14), fore_r=(10, 0, 0), arm_l=(92, 0, -14), fore_l=(10, 0, 0), P_body=(0, -2.0, -1.0))
    a.at(30, chest=(0, 0, 0), head=(36, 0, -6), arm_r=(140, 0, 44), fore_r=(30, 0, 0), arm_l=(140, 0, -44), fore_l=(30, 0, 0), P_body=(0, 0.2, 0))
    for t in (34, 44):
        a.at(t - 2, chest=(2, 0, 0), head=(36, 0, -6), arm_r=(142, 0, 46), fore_r=(24, 0, 0), arm_l=(142, 0, -46), fore_l=(24, 0, 0), P_body=(0, 0.2, 0))
        a.at(t, chest=(-16, 0, 2), head=(26, 8, 8), arm_r=(122, 0, 30), fore_r=(70, 0, 0), arm_l=(122, 0, -30), fore_l=(70, 0, 0), P_body=(0, -0.6, -0.3))
        a.at(t + 4, chest=(-2, 0, -1), head=(34, -4, -4), arm_r=(138, 0, 42), fore_r=(36, 0, 0), arm_l=(138, 0, -42), fore_l=(36, 0, 0), P_body=(0, 0, 0))
    a.at(50, chest=(16, 0, 0), head=(34, 0, 0), arm_r=(196, 0, 14), fore_r=(30, 0, 0), arm_l=(196, 0, -14), fore_l=(30, 0, 0), P_body=(0, 1.0, 0.6))
    a.at(52, chest=(-20, 0, 0), arm_r=(130, 0, 12), arm_l=(130, 0, -12))
    a.at(54, chest=(-56, 0, 0), head=(42, 0, 0), arm_r=(56, 0, 10), fore_r=(0, 0, 0), arm_l=(56, 0, -10), fore_l=(0, 0, 0), P_body=(0, -3.6, -1.4))
    a.at(58, chest=(-50, 0, 0), head=(38, 0, 0), arm_r=(60, 0, 12), arm_l=(60, 0, -12), P_body=(0, -3.2, -1.2))
    a.at(64, chest=(-26, 0, 0), head=(20, 0, 0), arm_r=(30, 0, 30), fore_r=(40, 0, 0), arm_l=(20, 0, -20), fore_l=(30, 0, 0), P_body=(0, -1.0, -0.4))
    a.at(70, chest=r["chest"], head=r["head"], arm_r=r["arm_r"], fore_r=r["fore_r"], arm_l=r["arm_l"], fore_l=r["fore_l"], P_body=(0, 0, 0))
    claws(a, 0, 0); claws(a, 12, -30, 30); claws(a, 18, -30, 34); claws(a, 20, 80, 4); claws(a, 30, 70, 4)
    for t in (34, 44):
        claws(a, t - 2, 66); claws(a, t, 100); claws(a, t + 4, 72)
    claws(a, 50, 80); claws(a, 54, 90); claws(a, 58, -20, 24); claws(a, 70, 0)
    tents(a, [(0, 0, 26, None), (8, -60, 44, 1.3), (12, -70, 50, 1.2), (15, 120, 10, 0.9), (17, 205, -8, 0.7), (20, 200, -4, 0.7),
              (30, 186, -10, 0.7), (34, 196, 8, 0.6), (38, 188, -6, 0.7), (44, 196, 8, 0.6), (48, 186, -8, 0.7),
              (50, 176, -12, 0.7), (54, 212, -2, 0.7), (58, 210, 0, 0.7), (62, -40, 40, 1.3), (70, 0, 26, None)], lag=1)
    tail(a, [(0, 0, 0, 0), (12, 0, -24, 16), (16, 0, 30, -20), (30, 20, 10, -10), (34, -20, 20, -24), (44, 20, 20, -24), (50, 0, -30, 20),
             (54, 0, 40, -30), (62, 0, 10, -6), (70, 0, 0, 0)])
    spines(a, 0, 0); spines(a, 12, -8); spines(a, 16, 18); spines(a, 30, 10); spines(a, 34, 26); spines(a, 38, 12); spines(a, 44, 26); spines(a, 48, 12)
    spines(a, 54, 30); spines(a, 62, 8); spines(a, 70, 0)
    a.legs([(0, 10, 0, 6), (12, 0, 0, 6), (16, 30, 0, 10), (30, 10, 0, 8), (50, 0, 0, 8), (54, 40, 0, 12), (62, 30, 0, 10), (70, 10, 0, 6)],
           [(0, -16, 0, 0), (12, -8, 0, 0), (16, -46, 0, 0), (30, -18, 0, 0), (50, -10, 0, 0), (54, -60, 0, 0), (62, -40, 0, 0), (70, -16, 0, 0)])
    a.hair([(0, 0, 0, 0), (12, -12, 0, 0), (16, 20, 0, 0), (22, -4, 0, 0), (30, -8, 0, 0), (34, 8, 0, 6), (40, -4, 0, 0), (44, 8, 0, -6),
            (50, -16, 0, 0), (54, 26, 0, 0), (60, -4, 0, 0), (70, 0, 0, 0)])
    a.cloth([(0, 0, 0, 0), (12, -6, 0, 0, 4), (16, 10, 0, 0, 16), (30, -2, 0, 0, 6), (34, 4, 0, 0, 10), (44, 4, 0, 0, 10), (50, -8, 0, 0, 4),
             (54, 12, 0, 0, 24), (62, 4, 0, 0, 8), (70, 0, 0, 0)])
    a.done()

    # ---------------------------------------------------------------- wing_gust (48): huge shadow wings unfurl 2-12, BEATS 18 / 26 / 34 (forward claps), fold 44
    a = mk("wing_gust", 48)
    a.scl("wings", (0, *HIDE), (1.99, *HIDE), (6, 1.6, 1.6, 1.6), (40, 1.6, 1.6, 1.6), (44, 0.4, 0.4, 0.4), (45, *HIDE), (48, *HIDE))
    wings_at(a, 2, spread=0.3, lift=40); wings_at(a, 10, spread=1.25, lift=30)
    for t in (18, 26, 34):
        wings_at(a, t - 4, spread=1.3, lift=50)
        wings_at(a, t, spread=1.0, lift=-60)
        a.at(t - 4, chest=(4, 0, 0), head=(18, 0, 0), arm_r=(40, 0, 90), arm_l=(40, 0, -90), P_body=(0, 0.8, 0.6))
        a.at(t, chest=(-34, 0, 0), head=(32, 0, 0), arm_r=(80, 0, 40), arm_l=(80, 0, -40), P_body=(0, -1.4, -0.6))
        spines(a, t - 4, -6); spines(a, t, 26)
    wings_at(a, 40, spread=1.0, lift=30); wings_at(a, 44, spread=0.3, lift=60)
    a.at(0, chest=r["chest"], head=r["head"], arm_r=r["arm_r"], arm_l=r["arm_l"], P_body=(0, 0, 0))
    a.at(40, chest=(-14, 0, 0), head=(12, 0, 0), arm_r=(20, 0, 40), arm_l=(10, 0, -20), P_body=(0, 0, 0))
    a.at(48, chest=r["chest"], head=r["head"], arm_r=r["arm_r"], arm_l=r["arm_l"], P_body=(0, 0, 0))
    claws(a, 0, 0); claws(a, 14, -30, 30); claws(a, 34, -30, 30); claws(a, 44, 0); claws(a, 48, 0)
    tents(a, [(0, 0, 26, None), (12, -40, 10, 1.8), (18, 40, 10, 1.6), (26, 40, 10, 1.6), (34, 40, 10, 1.6), (44, 0, 26, None)])
    tail(a, [(0, 0, 0, 0), (12, 0, -20, 20), (40, 0, -20, 20), (48, 0, 0, 0)])
    a.legs([(0, 10, 0, 6), (12, 0, 0, 10), (40, 0, 0, 10), (48, 10, 0, 6)], [(0, -16, 0, 0), (12, -20, 0, 0), (40, -20, 0, 0), (48, -16, 0, 0)])
    a.hair([(0, 0, 0, 0), (14, -6, 0, 0), (18, 16, 0, 0), (22, -8, 0, 0), (26, 16, 0, 0), (30, -8, 0, 0), (34, 16, 0, 0), (40, 0, 0, 0)], delay=1)
    a.cloth([(0, 0, 0, 0), (14, 0, 0, 0, 4), (18, -12, 0, 0, 16), (22, 2, 0, 0, 6), (26, -12, 0, 0, 16), (30, 2, 0, 0, 6), (34, -12, 0, 0, 16), (44, 0, 0, 0)], delay=1)
    a.done()

    # ---------------------------------------------------------------- orb_barrage (52): rear back 0-12, jaw thrust spitting orbs every 3 ticks 14-38, tentacles splay as cannons
    a = mk("orb_barrage", 52)
    a.at(0, chest=r["chest"], head=r["head"], arm_r=r["arm_r"], arm_l=r["arm_l"], fore_r=r["fore_r"], fore_l=r["fore_l"], P_body=(0, 0, 0))
    a.at(10, chest=(20, 0, 0), head=(40, 0, 0), arm_r=(40, 0, 70), arm_l=(40, 0, -70), fore_r=(20, 0, 0), fore_l=(20, 0, 0), P_body=(0, 1.0, 0.6))
    for i, t in enumerate(range(14, 39, 3)):
        j = 1 if i % 2 else -1
        a.at(t - 1, head=(26, 4 * j, 0), chest=(10, 3 * j, 0))
        a.at(t, head=(6, -6 * j, 0), chest=(4, -4 * j, 0))
    a.at(42, chest=(6, 0, 0), head=(20, 0, 0), arm_r=(30, 0, 60), arm_l=(30, 0, -60), P_body=(0, 0.6, 0.4))
    a.at(52, chest=r["chest"], head=r["head"], arm_r=r["arm_r"], arm_l=r["arm_l"], fore_r=r["fore_r"], fore_l=r["fore_l"], P_body=(0, 0, 0))
    claws(a, 0, 0); claws(a, 10, -30, 34); claws(a, 42, -30, 34); claws(a, 52, 0)
    tents(a, [(0, 0, 26, None), (10, -60, -4, 2.2), (40, -60, -4, 2.2), (46, -20, 20, None), (52, 0, 26, None)])
    tail(a, [(0, 0, 0, 0), (10, 0, -10, 20), (26, 10, -10, 26), (40, -10, -10, 20), (52, 0, 0, 0)], lag=2)
    spines(a, 0, 0); spines(a, 10, 20); spines(a, 40, 20); spines(a, 52, 0)
    a.legs([(0, 10, 0, 6), (10, -6, 0, 10), (42, -6, 0, 10), (52, 10, 0, 6)], [(0, -16, 0, 0), (10, -6, 0, 0), (42, -6, 0, 0), (52, -16, 0, 0)])
    a.hair([(0, 0, 0, 0), (10, -14, 0, 0), (14, 8, 0, 4), (20, 8, 0, -4), (26, 8, 0, 4), (32, 8, 0, -4), (38, 8, 0, 0), (52, 0, 0, 0)], delay=1)
    a.cloth([(0, 0, 0, 0), (10, -4, 0, 0, 6), (26, -2, 0, 0, 10), (42, -2, 0, 0, 6), (52, 0, 0, 0)])
    a.done()

    # ---------------------------------------------------------------- roar (50): inhale 0-14 (rear, arms gather), ROAR 18 (lunge, arms flung, spines + tentacles flare), tremble to 38
    a = mk("roar", 50)
    a.at(0, chest=r["chest"], head=r["head"], arm_r=r["arm_r"], arm_l=r["arm_l"], fore_r=r["fore_r"], fore_l=r["fore_l"], P_body=(0, 0, 0))
    a.at(12, chest=(24, 0, 0), head=(34, 0, 0), arm_r=(60, 30, 20), arm_l=(60, -30, -20), fore_r=(90, 0, 0), fore_l=(90, 0, 0), P_body=(0, 1.2, 0.8))
    a.at(18, chest=(-36, 0, 0), head=(54, 0, 0), arm_r=(30, 0, 110), arm_l=(30, 0, -110), fore_r=(-10, 0, 0), fore_l=(-10, 0, 0), P_body=(0, -1.8, -1.4))
    for t in range(20, 38, 2):
        j = 1 if t % 4 == 0 else -1
        a.at(t, chest=(-34, 2 * j, 2 * j), head=(52, 4 * j, -3 * j), arm_r=(30, 0, 108 + 4 * j), arm_l=(30, 0, -108 + 4 * j), P_body=(0, -1.8, -1.4))
    a.at(44, chest=(-20, 0, 0), head=(20, 0, 0), arm_r=(20, 0, 50), arm_l=(10, 0, -30), fore_r=(30, 0, 0), fore_l=(20, 0, 0), P_body=(0, -0.6, -0.4))
    a.at(50, chest=r["chest"], head=r["head"], arm_r=r["arm_r"], arm_l=r["arm_l"], fore_r=r["fore_r"], fore_l=r["fore_l"], P_body=(0, 0, 0))
    claws(a, 0, 0); claws(a, 12, 50); claws(a, 18, -40, 40); claws(a, 38, -40, 40); claws(a, 50, 0)
    tents(a, [(0, 0, 26, None), (12, 40, 50, 0.6), (18, -50, -10, 2.4), (38, -50, -10, 2.4), (46, -10, 20, None), (50, 0, 26, None)], lag=1)
    tail(a, [(0, 0, 0, 0), (12, 0, 20, 30), (18, 0, -30, -20), (38, 0, -30, -20), (50, 0, 0, 0)])
    spines(a, 0, 0); spines(a, 12, -14); spines(a, 18, 34); spines(a, 38, 30); spines(a, 50, 0)
    a.legs([(0, 10, 0, 6), (12, 0, 0, 6), (18, 30, 0, 14), (38, 30, 0, 14), (50, 10, 0, 6)], [(0, -16, 0, 0), (12, -6, 0, 0), (18, -44, 0, 0), (38, -44, 0, 0), (50, -16, 0, 0)])
    a.hair([(0, 0, 0, 0), (12, 10, 0, 0), (18, -30, 0, 0), (21, -26, 0, 8), (24, -30, 0, -8), (27, -26, 0, 6), (30, -30, 0, -6), (38, -20, 0, 0), (50, 0, 0, 0)], delay=1)
    a.cloth([(0, 0, 0, 0), (12, 4, 0, 0), (18, -16, 0, 0, 24), (30, -14, 0, 0, 20), (44, 0, 0, 0, 2), (50, 0, 0, 0)], delay=1)
    a.done()

    # ---------------------------------------------------------------- leap_slam (52): coil 0-13, LAUNCH 14, tuck in the air 16-22, LAND/SLAM ~24-26, crater crouch, rise
    a = mk("leap_slam", 52)
    a.at(0, chest=r["chest"], head=r["head"], arm_r=r["arm_r"], arm_l=r["arm_l"], fore_r=r["fore_r"], fore_l=r["fore_l"], P_body=(0, 0, 0))
    a.at(12, chest=(-50, 0, 0), head=(44, 0, 0), arm_r=(-50, 0, 30), arm_l=(-50, 0, -30), fore_r=(20, 0, 0), fore_l=(20, 0, 0), P_body=(0, -3.4, 0.6))
    a.at(14, chest=(-10, 0, 0), head=(20, 0, 0), arm_r=(-60, 0, 20), arm_l=(-60, 0, -20), P_body=(0, 0.6, 0))
    a.at(18, chest=(10, 0, 0), head=(20, 0, 0), arm_r=(190, 0, 30), arm_l=(190, 0, -30), fore_r=(30, 0, 0), fore_l=(30, 0, 0), P_body=(0, 0.4, 0))
    a.at(22, chest=(16, 0, 0), arm_r=(200, 0, 24), arm_l=(200, 0, -24))
    a.at(25, chest=(-60, 0, 0), head=(46, 0, 0), arm_r=(60, 0, 20), arm_l=(60, 0, -20), fore_r=(0, 0, 0), fore_l=(0, 0, 0), P_body=(0, -4.0, -1.2))
    a.at(34, chest=(-54, 0, 0), head=(40, 0, 0), P_body=(0, -3.6, -1.0))
    a.at(42, chest=(-26, 0, 0), head=(20, 0, 0), arm_r=(30, 0, 40), arm_l=(20, 0, -20), fore_r=(40, 0, 0), fore_l=(20, 0, 0), P_body=(0, -1.2, -0.3))
    a.at(52, chest=r["chest"], head=r["head"], arm_r=r["arm_r"], arm_l=r["arm_l"], fore_r=r["fore_r"], fore_l=r["fore_l"], P_body=(0, 0, 0))
    claws(a, 0, 0); claws(a, 12, 30); claws(a, 18, -30, 30); claws(a, 25, 50, 30); claws(a, 40, 30); claws(a, 52, 0)
    a.legs([(0, 10, 0, 6), (12, 50, 0, 12), (14, -10, 0, 4), (18, 60, 0, 6), (22, 70, 0, 6), (25, 50, 0, 16), (34, 50, 0, 16), (42, 26, 0, 10), (52, 10, 0, 6)],
           [(0, -16, 0, 0), (12, -90, 0, 0), (14, 0, 0, 0), (18, -100, 0, 0), (22, -110, 0, 0), (25, -80, 0, 0), (34, -80, 0, 0), (42, -40, 0, 0), (52, -16, 0, 0)])
    tents(a, [(0, 0, 26, None), (12, -20, 40, 1.4), (16, 60, 6, 1.0), (22, 60, 6, 1.0), (25, 160, 0, 1.6), (34, 160, 0, 1.6), (44, 0, 26, None)], lag=1)
    tail(a, [(0, 0, 0, 0), (12, 0, 20, 10), (16, 0, 60, -40), (22, 0, 50, -30), (25, 0, 30, -10), (40, 0, 10, 0), (52, 0, 0, 0)], lag=1)
    spines(a, 0, 0); spines(a, 14, -10); spines(a, 25, 30); spines(a, 52, 0)
    a.hair([(0, 0, 0, 0), (12, 10, 0, 0), (16, -26, 0, 0), (22, -20, 0, 0), (25, 30, 0, 0), (30, -6, 0, 0), (52, 0, 0, 0)], delay=1)
    a.cloth([(0, 0, 0, 0), (12, 6, 0, 0, 10), (16, -20, 0, 0, 4), (22, -16, 0, 0, 6), (25, 14, 0, 0, 30), (32, 4, 0, 0, 10), (52, 0, 0, 0)], delay=1)
    a.done()

    # ---------------------------------------------------------------- eye_beam (62): claws cradle the face, charge trembling 2-28, head snaps up 30 -> BEAM 30-52, brace, recover
    a = mk("eye_beam", 62).show("beam", 30, 53, grow=1)
    a.at(0, chest=r["chest"], head=r["head"], arm_r=r["arm_r"], arm_l=r["arm_l"], fore_r=r["fore_r"], fore_l=r["fore_l"], P_body=(0, 0, 0))
    a.at(8, chest=(-36, 0, 0), head=(-10, 0, 0), arm_r=(150, 30, 20), arm_l=(150, -30, -20), fore_r=(100, 0, 0), fore_l=(100, 0, 0), P_body=(0, -1.6, 0))
    for t in range(10, 29, 3):
        j = 1 if (t // 3) % 2 else -1
        a.at(t, chest=(-40 + t * 0.3, 2 * j, 2 * j), head=(-12 + t * 0.2, 3 * j, 0), P_body=(0, -1.8, 0))
    a.at(30, chest=(-10, 0, 0), head=(16, 0, 0), arm_r=(30, 0, 70), arm_l=(30, 0, -70), fore_r=(20, 0, 0), fore_l=(20, 0, 0), P_body=(0, -0.6, 0.4))
    for t in range(32, 52, 4):
        j = 1 if (t // 4) % 2 else -1
        a.at(t, chest=(-8, 0, j), head=(14 + j, 0, 0), arm_r=(30, 0, 66 + 3 * j), arm_l=(30, 0, -66 + 3 * j))
    a.at(54, chest=(-24, 0, 0), head=(-6, 0, 0), arm_r=(60, 0, 30), arm_l=(60, 0, -30), fore_r=(60, 0, 0), fore_l=(60, 0, 0), P_body=(0, -1.0, 0))
    a.at(62, chest=r["chest"], head=r["head"], arm_r=r["arm_r"], arm_l=r["arm_l"], fore_r=r["fore_r"], fore_l=r["fore_l"], P_body=(0, 0, 0))
    claws(a, 0, 0); claws(a, 8, 40); claws(a, 28, 50); claws(a, 30, -40, 40); claws(a, 52, -40, 40); claws(a, 62, 0)
    tents(a, [(0, 0, 26, None), (8, 30, 50, 0.6), (28, 30, 50, 0.6), (30, -40, 0, 2.0), (52, -40, 0, 2.0), (62, 0, 26, None)], lag=1)
    tail(a, [(0, 0, 0, 0), (8, 0, 10, 30), (28, 0, 10, 30), (30, 0, 40, -20), (52, 0, 40, -20), (62, 0, 0, 0)])
    spines(a, 0, 0); spines(a, 28, -10); spines(a, 30, 30); spines(a, 52, 26); spines(a, 62, 0)
    a.legs([(0, 10, 0, 6), (8, 20, 0, 8), (28, 20, 0, 8), (30, 24, 0, 14), (52, 24, 0, 14), (62, 10, 0, 6)], [(0, -16, 0, 0), (8, -40, 0, 0), (28, -40, 0, 0), (30, -36, 0, 0), (52, -36, 0, 0), (62, -16, 0, 0)])
    a.hair([(0, 0, 0, 0), (8, 10, 0, 0), (28, 10, 0, 0), (30, -24, 0, 0), (36, -20, 0, 4), (44, -20, 0, -4), (52, -16, 0, 0), (62, 0, 0, 0)], delay=1)
    a.cloth([(0, 0, 0, 0), (8, 4, 0, 0, 2), (30, -12, 0, 0, 18), (52, -10, 0, 0, 16), (62, 0, 0, 0)], delay=1)
    a.done()

    # ---------------------------------------------------------------- vortex (72): spread everything 6-18, swirling pull 18-58 (body turns, tentacles orbit), CLAP 60, recover
    a = mk("vortex", 72).show("wings", 6, 66, grow=4)
    a.at(0, chest=r["chest"], head=r["head"], arm_r=r["arm_r"], arm_l=r["arm_l"], fore_r=r["fore_r"], fore_l=r["fore_l"], body=(0, 0, 0), P_body=(0, 0, 0))
    a.at(16, chest=(14, 0, 0), head=(26, 0, 0), arm_r=(10, 0, 120), arm_l=(10, 0, -120), fore_r=(-10, 0, 0), fore_l=(-10, 0, 0), P_body=(0, 0.8, 0))
    for k, t in enumerate(range(20, 58, 6)):
        j = 1 if k % 2 else -1
        a.at(t, body=(0, 14 * j, 0), chest=(12, 10 * j, 0), arm_r=(10 + 6 * j, 0, 116), arm_l=(10 - 6 * j, 0, -116))
    wings_at(a, 6, spread=0.3, lift=40); wings_at(a, 16, spread=1.4, lift=0)
    for t in range(20, 58, 8):
        wings_at(a, t, spread=1.4, lift=-10 if (t // 8) % 2 else 10)
    a.at(57, body=(0, 0, 0), chest=(18, 0, 0), head=(30, 0, 0), arm_r=(20, 0, 130), arm_l=(20, 0, -130), P_body=(0, 1.0, 0.4))
    a.at(60, chest=(-40, 0, 0), head=(36, 0, 0), arm_r=(90, -60, 0), arm_l=(90, 60, 0), fore_r=(0, 0, 0), fore_l=(0, 0, 0), P_body=(0, -2.4, -1.2))
    wings_at(a, 58, spread=1.5, lift=30); wings_at(a, 60, spread=0.8, lift=-70); wings_at(a, 66, spread=0.3, lift=40)
    a.at(64, chest=(-36, 0, 0), arm_r=(86, -56, 0), arm_l=(86, 56, 0), P_body=(0, -2.2, -1.1))
    a.at(72, body=(0, 0, 0), chest=r["chest"], head=r["head"], arm_r=r["arm_r"], arm_l=r["arm_l"], fore_r=r["fore_r"], fore_l=r["fore_l"], P_body=(0, 0, 0))
    claws(a, 0, 0); claws(a, 16, -40, 40); claws(a, 57, -40, 40); claws(a, 60, 60); claws(a, 72, 0)
    keys = [(0, 0, 26, None)]
    for k, t in enumerate(range(16, 58, 4)):
        keys.append((t, -30 + (k % 2) * 30, 10 + (k % 3) * 16, 2.0 + (k % 2) * 0.6))
    keys += [(60, 120, 0, 0.6), (66, 60, 10, 0.8), (72, 0, 26, None)]
    tents(a, keys, lag=1.5)
    tail(a, [(0, 0, 0, 0), (16, 30, 0, -10), (28, -30, 0, -14), (40, 30, 0, -10), (52, -30, 0, -14), (60, 0, 20, -20), (72, 0, 0, 0)], lag=2)
    spines(a, 0, 0); spines(a, 16, 30); spines(a, 57, 30); spines(a, 60, 10); spines(a, 72, 0)
    a.legs([(0, 10, 0, 6), (16, 0, 0, 14), (57, 0, 0, 14), (60, 30, 0, 8), (72, 10, 0, 6)], [(0, -16, 0, 0), (16, -10, 0, 0), (57, -10, 0, 0), (60, -40, 0, 0), (72, -16, 0, 0)])
    a.hair([(0, 0, 0, 0), (16, -10, 0, 0), (24, -6, 0, 14), (32, -6, 0, -14), (40, -6, 0, 14), (48, -6, 0, -14), (57, -10, 0, 0), (60, 24, 0, 0), (72, 0, 0, 0)], delay=2)
    a.cloth([(0, 0, 0, 0), (16, -4, 0, 0, 12), (24, -6, 0, 14, 16), (32, -6, 0, -14, 16), (40, -6, 0, 14, 16), (48, -6, 0, -14, 16), (60, 12, 0, 0, 20), (72, 0, 0, 0)], delay=2)
    a.done()

    # ---------------------------------------------------------------- black_rain (66): arms to the sky 4-16, fists pump the spikes up (beats every 9 ticks 20-56), drop arms 60
    a = mk("black_rain", 66)
    a.at(0, chest=r["chest"], head=r["head"], arm_r=r["arm_r"], arm_l=r["arm_l"], fore_r=r["fore_r"], fore_l=r["fore_l"], P_body=(0, 0, 0))
    a.at(14, chest=(20, 0, 0), head=(40, 0, 0), arm_r=(170, 0, 30), arm_l=(170, 0, -30), fore_r=(10, 0, 0), fore_l=(10, 0, 0), P_body=(0, 1.2, 0.4))
    for t in range(20, 58, 9):
        a.at(t - 3, chest=(24, 0, 0), arm_r=(175, 0, 26), arm_l=(175, 0, -26), fore_r=(0, 0, 0), fore_l=(0, 0, 0), P_body=(0, 1.4, 0.4))
        a.at(t, chest=(10, 0, 0), arm_r=(150, 0, 34), arm_l=(150, 0, -34), fore_r=(50, 0, 0), fore_l=(50, 0, 0), P_body=(0, 0.6, 0.2))
        spines(a, t - 3, 10); spines(a, t, 30)
    a.at(62, chest=(-20, 0, 0), head=(14, 0, 0), arm_r=(40, 0, 40), arm_l=(30, 0, -30), fore_r=(40, 0, 0), fore_l=(20, 0, 0), P_body=(0, -0.6, 0))
    a.at(66, chest=r["chest"], head=r["head"], arm_r=r["arm_r"], arm_l=r["arm_l"], fore_r=r["fore_r"], fore_l=r["fore_l"], P_body=(0, 0, 0))
    claws(a, 0, 0); claws(a, 14, -30, 40); claws(a, 18, 90); claws(a, 58, 90); claws(a, 62, 10); claws(a, 66, 0)
    spines(a, 0, 0); spines(a, 66, 0)
    tents(a, [(0, 0, 26, None), (14, -80, 6, 1.4), (30, -90, 14, 1.6), (44, -80, 6, 1.4), (58, -90, 14, 1.6), (66, 0, 26, None)], lag=2)
    tail(a, [(0, 0, 0, 0), (14, 0, -20, 30), (30, 20, -20, 30), (44, -20, -20, 30), (58, 0, -20, 30), (66, 0, 0, 0)], lag=2)
    a.legs([(0, 10, 0, 6), (14, 0, 0, 10), (58, 0, 0, 10), (66, 10, 0, 6)], [(0, -16, 0, 0), (14, -4, 0, 0), (58, -4, 0, 0), (66, -16, 0, 0)])
    a.hair([(0, 0, 0, 0), (14, -16, 0, 0), (20, -10, 0, 0), (29, -10, 0, 0), (38, -10, 0, 0), (47, -10, 0, 0), (56, -10, 0, 0), (66, 0, 0, 0)], delay=1)
    a.cloth([(0, 0, 0, 0), (14, -6, 0, 0, 8), (20, -2, 0, 0, 12), (38, -2, 0, 0, 12), (56, -2, 0, 0, 12), (66, 0, 0, 0)], delay=2)
    a.done()

    # ---------------------------------------------------------------- stomp (30): knee up 4-10, STOMP 12, shock crouch, recover
    a = mk("stomp", 30)
    a.at(0, chest=r["chest"], head=r["head"], arm_r=r["arm_r"], arm_l=r["arm_l"], P_body=(0, 0, 0))
    a.at(9, chest=(4, 10, 0), head=(20, -6, 0), arm_r=(20, 0, 60), arm_l=(20, 0, -60), P_body=(0, 1.0, 0))
    a.at(12, chest=(-36, -4, 0), head=(36, 4, 0), arm_r=(-10, 0, 40), arm_l=(-10, 0, -40), P_body=(0, -1.6, -0.4))
    a.at(18, chest=(-30, 0, 0), head=(30, 0, 0), P_body=(0, -1.4, -0.3))
    a.at(30, chest=r["chest"], head=r["head"], arm_r=r["arm_r"], arm_l=r["arm_l"], P_body=(0, 0, 0))
    a.rot("leg_r", (0, *r["leg_r"]), (9, 80, 0, 10), (12, -6, 0, 6), (22, -6, 0, 6), (30, *r["leg_r"]))
    a.rot("shin_r", (0, *r["shin_r"]), (9, -80, 0, 0), (12, 0, 0, 0), (22, -4, 0, 0), (30, *r["shin_r"]))
    a.rot("leg_l", (0, *r["leg_l"]), (9, 4, 0, -6), (12, 30, 0, -10), (22, 30, 0, -10), (30, *r["leg_l"]))
    a.rot("shin_l", (0, *r["shin_l"]), (9, -10, 0, 0), (12, -50, 0, 0), (22, -50, 0, 0), (30, *r["shin_l"]))
    claws(a, 0, 0); claws(a, 9, -20, 20); claws(a, 12, 30); claws(a, 30, 0)
    tents(a, [(0, 0, 26, None), (9, -20, 36, 1.2), (12, 30, 10, 1.6), (22, 10, 20, 1.3), (30, 0, 26, None)], lag=1)
    tail(a, [(0, 0, 0, 0), (9, -20, -10, 10), (12, 10, 30, -20), (22, 0, 10, -6), (30, 0, 0, 0)], lag=1)
    spines(a, 0, 0); spines(a, 12, 22); spines(a, 30, 0)
    a.hair([(0, 0, 0, 0), (9, -8, 0, 0), (12, 20, 0, 0), (16, -6, 0, 0), (30, 0, 0, 0)], delay=1)
    a.cloth([(0, 0, 0, 0), (9, 6, 0, 8), (12, 6, 0, 0, 20), (18, 0, 0, 0, 8), (30, 0, 0, 0)], delay=1)
    a.done()

    # ---------------------------------------------------------------- tail_lash (40): crouch + wind 0-10, SPIN 10-20 (tail flat out, hit 16), stagger to a stop
    a = mk("tail_lash", 40)
    a.at(0, root=(0, 0, 0), chest=r["chest"], head=r["head"], arm_r=r["arm_r"], arm_l=r["arm_l"], P_root=(0, 0, 0))
    a.at(9, root=(0, 50, 0), chest=(-30, 20, 0), head=(26, -20, 0), arm_r=(30, 0, 60), arm_l=(30, 0, -60), P_root=(0, -1.0, 0))
    a.at(13, root=(0, -60, 0), chest=(-26, -10, 0))
    a.at(16, root=(0, -170, 0), chest=(-24, -14, 0), head=(24, 10, 0), arm_r=(20, 0, 90), arm_l=(20, 0, -90))
    a.at(20, root=(0, -330, 0), chest=(-28, -6, 0))
    a.at(24, root=(0, -380, 0), chest=(-30, 6, 0), head=(26, -6, 0), arm_r=(40, 0, 50), arm_l=(40, 0, -50), P_root=(0, -0.8, 0))
    a.at(30, root=(0, -362, 0), chest=(-20, 0, 0), P_root=(0, -0.3, 0))
    a.at(40, root=(0, -360, 0), chest=r["chest"], head=r["head"], arm_r=r["arm_r"], arm_l=r["arm_l"], P_root=(0, 0, 0))
    tail(a, [(0, 0, 0, 0), (9, -40, -10, 10), (12, 20, -46, 18), (16, 40, -50, 22), (20, 40, -50, 22), (24, 0, -20, 4), (30, -10, 0, 0), (40, 0, 0, 0)], lag=0.8)
    tents(a, [(0, 0, 26, None), (9, -10, 40, 1.4), (16, 0, 0, 2.6), (22, 0, 0, 2.4), (30, 0, 20, None), (40, 0, 26, None)], lag=1)
    claws(a, 0, 0); claws(a, 9, 30); claws(a, 16, -30, 30); claws(a, 30, 0); claws(a, 40, 0)
    spines(a, 0, 0); spines(a, 16, 24); spines(a, 40, 0)
    a.legs([(0, 10, 0, 6), (9, 40, 0, 14), (16, 30, 0, 18), (24, 40, 0, 14), (40, 10, 0, 6)], [(0, -16, 0, 0), (9, -60, 0, 0), (16, -40, 0, 0), (24, -60, 0, 0), (40, -16, 0, 0)])
    a.hair([(0, 0, 0, 0), (9, 4, 0, -10), (16, -6, 0, 28), (22, -6, 0, 28), (28, 0, 0, -8), (40, 0, 0, 0)], delay=1)
    a.cloth([(0, 0, 0, 0), (9, 4, 0, -6, 6), (16, -6, 0, 14, 26), (22, -6, 0, 14, 26), (30, 0, 0, -4, 4), (40, 0, 0, 0)], delay=1)
    a.done()

    # ---------------------------------------------------------------- tentacle_lash (44): tentacles rear over the shoulders 2-10, LASH 14 / 19 / 24 / 29 in turn, recoil, settle
    a = mk("tentacle_lash", 44)
    a.at(0, chest=r["chest"], head=r["head"], arm_r=r["arm_r"], arm_l=r["arm_l"], P_body=(0, 0, 0))
    a.at(10, chest=(6, 0, 0), head=(24, 0, 0), arm_r=(30, 0, 60), arm_l=(30, 0, -60), P_body=(0, 0.6, 0.4))
    for i, t in enumerate((14, 19, 24, 29)):
        bx, by, bz = TENT_REST[i]
        s = 1 if i % 2 == 0 else -1
        tent(a, i, [(0, (bx, by, bz), 26), (8, (bx - 50, by * 0.5, bz), 40), (t - 2, (bx - 70, by * 0.3, bz), 44), (t, (172, by * 0.7, bz), -6),
                    (t + 4, (150, by * 0.8, bz), 4), (t + 9, (bx - 30, by * 0.6, bz), 30), (44, (bx, by, bz), 26)], lag=0.7)
        a.scl(f"tent{i}_0", (0, 1, 1, 1), (t - 1, 1, 1, 1), (t, 1.5, 1.5, 3.0), (t + 4, 1.3, 1.3, 2.4), (t + 9, 1, 1, 1), (44, 1, 1, 1))
        a.at(t, chest=(-24, 10 * s, 0), head=(30, -6 * s, 0), P_body=(0, -0.6, -0.8))
        a.at(t + 2.5, chest=(-14, 4 * s, 0), head=(24, 0, 0))
    a.at(36, chest=(-14, 0, 0), head=(16, 0, 0), arm_r=(20, 0, 40), arm_l=(10, 0, -20), P_body=(0, 0, 0))
    a.at(44, chest=r["chest"], head=r["head"], arm_r=r["arm_r"], arm_l=r["arm_l"], P_body=(0, 0, 0))
    claws(a, 0, 0); claws(a, 10, -30, 30); claws(a, 32, -30, 30); claws(a, 44, 0)
    tail(a, [(0, 0, 0, 0), (10, 0, -10, 20), (19, 20, -10, 20), (29, -20, -10, 20), (44, 0, 0, 0)], lag=1.5)
    spines(a, 0, 0); spines(a, 10, 14); spines(a, 32, 14); spines(a, 44, 0)
    a.legs([(0, 10, 0, 6), (10, 4, 0, 10), (14, 20, 0, 12), (32, 20, 0, 12), (44, 10, 0, 6)], [(0, -16, 0, 0), (10, -10, 0, 0), (14, -30, 0, 0), (32, -30, 0, 0), (44, -16, 0, 0)])
    a.hair([(0, 0, 0, 0), (10, -8, 0, 0), (14, 10, 0, 6), (19, 10, 0, -6), (24, 10, 0, 6), (29, 10, 0, -6), (36, 0, 0, 0), (44, 0, 0, 0)], delay=1)
    a.cloth([(0, 0, 0, 0), (10, -2, 0, 0, 4), (14, 4, 0, 4, 8), (19, 4, 0, -4, 8), (24, 4, 0, 4, 8), (29, 4, 0, -4, 8), (44, 0, 0, 0)], delay=1)
    a.done()

    # ---------------------------------------------------------------- eruption (60): rise, claws high 0-12, PLUNGE both claws + tentacles into the floor 16, hold (spike lines race out), RIP free 40
    a = mk("eruption", 60)
    a.at(0, chest=r["chest"], head=r["head"], arm_r=r["arm_r"], arm_l=r["arm_l"], fore_r=r["fore_r"], fore_l=r["fore_l"], P_body=(0, 0, 0))
    a.at(12, chest=(20, 0, 0), head=(36, 0, 0), arm_r=(190, 0, 16), arm_l=(190, 0, -16), fore_r=(0, 0, 0), fore_l=(0, 0, 0), P_body=(0, 1.6, 0.4))
    a.at(16, chest=(-70, 0, 0), head=(56, 0, 0), arm_r=(40, 0, 8), arm_l=(40, 0, -8), P_body=(0, -5.0, -0.6))
    for t in range(18, 38, 3):
        j = 1 if (t // 3) % 2 else -1
        a.at(t, chest=(-68, 2 * j, 2 * j), head=(54, 3 * j, 0), arm_r=(42, 0, 8 + j), arm_l=(42, 0, -8 + j), P_body=(0, -5.0, -0.6))
    a.at(40, chest=(10, 0, 0), head=(30, 0, 0), arm_r=(120, 0, 60), arm_l=(120, 0, -60), fore_r=(30, 0, 0), fore_l=(30, 0, 0), P_body=(0, 0.8, 0.2))
    a.at(50, chest=(-20, 0, 0), head=(16, 0, 0), arm_r=(30, 0, 40), arm_l=(20, 0, -24), fore_r=(40, 0, 0), fore_l=(20, 0, 0), P_body=(0, -0.4, 0))
    a.at(60, chest=r["chest"], head=r["head"], arm_r=r["arm_r"], arm_l=r["arm_l"], fore_r=r["fore_r"], fore_l=r["fore_l"], P_body=(0, 0, 0))
    claws(a, 0, 0); claws(a, 12, -30, 30); claws(a, 16, 30, 40); claws(a, 38, 30, 40); claws(a, 40, -40, 40); claws(a, 50, 10); claws(a, 60, 0)
    tents(a, [(0, 0, 26, None), (12, -60, 30, 1.6), (16, 190, -4, 1.0), (38, 190, -4, 1.0), (40, -60, 10, 2.2), (50, -10, 20, None), (60, 0, 26, None)], lag=1)
    tail(a, [(0, 0, 0, 0), (12, 0, -20, 20), (16, 0, 60, -20), (38, 0, 60, -20), (42, 0, -20, 20), (60, 0, 0, 0)], lag=1.2)
    spines(a, 0, 0); spines(a, 12, -10); spines(a, 16, 36); spines(a, 38, 36); spines(a, 42, 10); spines(a, 60, 0)
    a.legs([(0, 10, 0, 6), (12, -6, 0, 6), (16, 60, 0, 16), (38, 60, 0, 16), (40, 10, 0, 8), (60, 10, 0, 6)], [(0, -16, 0, 0), (12, 0, 0, 0), (16, -100, 0, 0), (38, -100, 0, 0), (40, -10, 0, 0), (60, -16, 0, 0)])
    a.hair([(0, 0, 0, 0), (12, -16, 0, 0), (16, 30, 0, 0), (22, 10, 0, 4), (30, 10, 0, -4), (40, -20, 0, 0), (50, 0, 0, 0), (60, 0, 0, 0)], delay=1)
    a.cloth([(0, 0, 0, 0), (12, -6, 0, 0, 4), (16, 16, 0, 0, 34), (38, 10, 0, 0, 26), (40, -10, 0, 0, 10), (60, 0, 0, 0)], delay=1)
    a.done()

    # ---------------------------------------------------------------- abyss (86, enraged): ROAR 4, claws into the floor 20 (tentacle cage), three pounds 34/42/50, hands clasped high 58-63, WORLD SLAM 66
    a = mk("abyss", 86).show("wings", 2, 80, grow=4)
    a.at(0, chest=r["chest"], head=r["head"], arm_r=r["arm_r"], arm_l=r["arm_l"], fore_r=r["fore_r"], fore_l=r["fore_l"], P_body=(0, 0, 0))
    a.at(4, chest=(-30, 0, 0), head=(56, 0, 0), arm_r=(30, 0, 110), arm_l=(30, 0, -110), fore_r=(-10, 0, 0), fore_l=(-10, 0, 0), P_body=(0, -1.2, -0.8))
    a.at(12, chest=(-26, 0, 2), head=(50, 4, 0), arm_r=(30, 0, 106), arm_l=(30, 0, -106))
    a.at(17, chest=(16, 0, 0), head=(30, 0, 0), arm_r=(180, 0, 20), arm_l=(180, 0, -20), fore_r=(10, 0, 0), fore_l=(10, 0, 0), P_body=(0, 1.0, 0.2))
    a.at(20, chest=(-60, 0, 0), head=(48, 0, 0), arm_r=(50, 0, 10), arm_l=(50, 0, -10), fore_r=(0, 0, 0), fore_l=(0, 0, 0), P_body=(0, -4.0, -0.8))
    a.at(28, chest=(-56, 0, 0), P_body=(0, -3.8, -0.8))
    for k, t in enumerate((34, 42, 50)):
        s = 1 if k % 2 == 0 else -1
        a.at(t - 4, chest=(-10, 0, 0), head=(30, 0, 0), arm_r=(160 if s > 0 else 60, 0, 24), arm_l=(160 if s < 0 else 60, 0, -24), P_body=(0, -1.0, -0.2))
        a.at(t, chest=(-50, 8 * s, 0), head=(44, 0, 0), arm_r=(50, 0, 14), arm_l=(50, 0, -14), P_body=(0, -3.6, -0.8))
    a.at(58, chest=(22, 0, 0), head=(30, 0, 0), arm_r=(190, -20, -10), arm_l=(190, 20, 10), fore_r=(20, 0, 0), fore_l=(20, 0, 0), P_body=(0, 2.0, 0.6))
    a.at(63, chest=(26, 0, 0), head=(36, 0, 0), arm_r=(200, -20, -12), arm_l=(200, 20, 12), P_body=(0, 2.4, 0.8))
    a.at(66, chest=(-70, 0, 0), head=(56, 0, 0), arm_r=(50, -30, -6), arm_l=(50, 30, 6), fore_r=(0, 0, 0), fore_l=(0, 0, 0), P_body=(0, -5.0, -1.6))
    a.at(74, chest=(-64, 0, 0), head=(50, 0, 0), P_body=(0, -4.6, -1.4))
    a.at(86, chest=r["chest"], head=r["head"], arm_r=r["arm_r"], arm_l=r["arm_l"], fore_r=r["fore_r"], fore_l=r["fore_l"], P_body=(0, 0, 0))
    wings_at(a, 2, spread=0.3, lift=40); wings_at(a, 4, spread=1.5, lift=-10); wings_at(a, 20, spread=1.2, lift=-50); wings_at(a, 58, spread=1.6, lift=30)
    wings_at(a, 66, spread=1.2, lift=-70); wings_at(a, 80, spread=0.3, lift=40)
    claws(a, 0, 0); claws(a, 4, -40, 40); claws(a, 17, -30, 30); claws(a, 20, 40, 30); claws(a, 30, 80); claws(a, 58, 90); claws(a, 66, 90); claws(a, 76, 40); claws(a, 86, 0)
    tents(a, [(0, 0, 26, None), (4, -50, -10, 2.4), (14, -50, -10, 2.4), (17, -70, 40, 1.2), (20, 190, -4, 1.0), (54, 190, -4, 1.0), (58, -70, 30, 1.6), (66, 170, 0, 2.0), (78, 100, 10, 1.4), (86, 0, 26, None)], lag=1)
    tail(a, [(0, 0, 0, 0), (4, 0, -30, -20), (17, 0, -10, 20), (20, 0, 50, -20), (54, 0, 50, -20), (60, 0, -30, 30), (66, 0, 60, -30), (86, 0, 0, 0)], lag=1.2)
    spines(a, 0, 0); spines(a, 4, 34); spines(a, 20, 20); spines(a, 58, -10); spines(a, 66, 36); spines(a, 86, 0)
    a.legs([(0, 10, 0, 6), (4, 30, 0, 14), (17, 0, 0, 10), (20, 50, 0, 16), (54, 50, 0, 16), (58, 0, 0, 8), (66, 60, 0, 18), (76, 50, 0, 16), (86, 10, 0, 6)],
           [(0, -16, 0, 0), (4, -44, 0, 0), (17, -6, 0, 0), (20, -80, 0, 0), (54, -80, 0, 0), (58, -6, 0, 0), (66, -100, 0, 0), (76, -80, 0, 0), (86, -16, 0, 0)])
    a.hair([(0, 0, 0, 0), (4, -30, 0, 0), (12, -26, 0, 6), (17, -10, 0, 0), (20, 24, 0, 0), (34, 16, 0, 4), (42, 16, 0, -4), (50, 16, 0, 4), (58, -20, 0, 0), (66, 34, 0, 0), (76, 4, 0, 0), (86, 0, 0, 0)], delay=1)
    a.cloth([(0, 0, 0, 0), (4, -14, 0, 0, 22), (17, -4, 0, 0, 4), (20, 12, 0, 0, 26), (54, 10, 0, 0, 22), (58, -10, 0, 0, 6), (66, 18, 0, 0, 36), (78, 4, 0, 0, 10), (86, 0, 0, 0)], delay=1)
    a.done()

    # ---------------------------------------------------------------- transform (130; boss model plays 90-130): crouched mass at 90 unfurls 90-104, inhale 108, ROAR 112, settle
    a = mk("transform", 130)
    a.scl("root", (0, 0.5, 0.5, 0.5), (90, 0.5, 0.5, 0.5), (96, 0.75, 0.75, 0.75), (104, 1.0, 1.0, 1.0), (112, 1.06, 1.06, 1.06), (118, 1.0, 1.0, 1.0), (130, 1, 1, 1))
    pose_ball = dict(chest=(-70, 0, 0), head=(-10, 0, 0), arm_r=(120, 40, 20), arm_l=(120, -40, -20), fore_r=(110, 0, 0), fore_l=(110, 0, 0), P_body=(0, -5.0, 0))
    a.at(0, **pose_ball)
    for t in range(4, 90, 6):
        j = 1 if (t // 6) % 2 else -1
        a.at(t, chest=(-70 + j * 2, j * 2, j * 2), head=(-10, j * 4, 0))
    a.at(90, **pose_ball)
    a.at(98, chest=(-30, 0, 0), head=(10, 0, 0), arm_r=(40, 0, 60), arm_l=(40, 0, -60), fore_r=(40, 0, 0), fore_l=(40, 0, 0), P_body=(0, -2.0, 0))
    a.at(106, chest=(22, 0, 0), head=(36, 0, 0), arm_r=(60, 30, 30), arm_l=(60, -30, -30), fore_r=(90, 0, 0), fore_l=(90, 0, 0), P_body=(0, 1.0, 0.6))
    a.at(112, chest=(-36, 0, 0), head=(56, 0, 0), arm_r=(30, 0, 115), arm_l=(30, 0, -115), fore_r=(-10, 0, 0), fore_l=(-10, 0, 0), P_body=(0, -1.8, -1.4))
    for t in range(114, 124, 2):
        j = 1 if t % 4 == 0 else -1
        a.at(t, chest=(-34, 2 * j, 2 * j), head=(54, 4 * j, -3 * j), arm_r=(30, 0, 112 + 4 * j), arm_l=(30, 0, -112 + 4 * j))
    a.at(130, chest=r["chest"], head=r["head"], arm_r=r["arm_r"], arm_l=r["arm_l"], fore_r=r["fore_r"], fore_l=r["fore_l"], P_body=(0, 0, 0))
    claws(a, 0, 60); claws(a, 90, 60); claws(a, 100, -30, 30); claws(a, 106, 50); claws(a, 112, -40, 40); claws(a, 124, -40, 40); claws(a, 130, 0)
    tents(a, [(0, 60, 60, 0.4), (90, 60, 60, 0.4), (100, -20, 20, 1.6), (106, 30, 50, 0.6), (112, -50, -10, 2.4), (124, -50, -10, 2.4), (130, 0, 26, None)], lag=1)
    tail(a, [(0, 0, 0, 40), (90, 0, 0, 40), (104, 0, 20, 10), (112, 0, -30, -20), (124, 0, -30, -20), (130, 0, 0, 0)], lag=1.5)
    spines(a, 0, -30); spines(a, 90, -30); spines(a, 104, 10); spines(a, 112, 36); spines(a, 124, 30); spines(a, 130, 0)
    a.legs([(0, 70, 0, 10), (90, 70, 0, 10), (100, 30, 0, 10), (106, 0, 0, 8), (112, 30, 0, 14), (124, 30, 0, 14), (130, 10, 0, 6)],
           [(0, -130, 0, 0), (90, -130, 0, 0), (100, -60, 0, 0), (106, -10, 0, 0), (112, -44, 0, 0), (124, -44, 0, 0), (130, -16, 0, 0)])
    a.hair([(0, 10, 0, 0), (90, 10, 0, 0), (100, -10, 0, 0), (106, 10, 0, 0), (112, -30, 0, 0), (116, -26, 0, 8), (120, -30, 0, -8), (126, -10, 0, 0), (130, 0, 0, 0)], delay=1)
    a.cloth([(0, 10, 0, 0, 30), (90, 10, 0, 0, 30), (100, -6, 0, 0, 10), (112, -16, 0, 0, 26), (124, -14, 0, 0, 20), (130, 0, 0, 0)], delay=1)
    a.done()

    # ---------------------------------------------------------------- death (40): convulse 0-8, sag to the knees 14, topple forward 26, melt into a puddle 30-40
    a = mk("death", 40)
    a.at(0, chest=r["chest"], head=r["head"], arm_r=r["arm_r"], arm_l=r["arm_l"], P_body=(0, 0, 0), root=(0, 0, 0))
    a.at(4, chest=(20, 0, 0), head=(50, 0, 0), arm_r=(20, 0, 100), arm_l=(20, 0, -100), P_body=(0, 0.6, 0))
    a.at(8, chest=(14, 0, 4), head=(44, 6, 6))
    a.at(14, chest=(-40, 0, 0), head=(20, 0, -20), arm_r=(10, 0, 20), arm_l=(10, 0, -20), fore_r=(10, 0, 0), fore_l=(10, 0, 0), P_body=(0, -5.0, 0))
    a.at(26, root=(70, 0, 0), P_root=(0, 1.0, -3.0), chest=(-20, 0, 0), head=(10, 0, -20), arm_r=(160, 0, 40), arm_l=(150, 0, -30))
    a.at(40, root=(86, 0, 0), P_root=(0, 0.2, -4.0))
    a.scl("root", (0, 1, 1, 1), (30, 1, 1, 1), (40, 1.3, 1.3, 0.06))
    claws(a, 0, 0); claws(a, 4, -40, 40); claws(a, 14, 30); claws(a, 26, 60); claws(a, 40, 60)
    tents(a, [(0, 0, 26, None), (4, -50, -10, 2.4), (14, 40, 30, 1.0), (26, 80, 50, 1.4), (40, 90, 40, 1.4)], lag=2)
    tail(a, [(0, 0, 0, 0), (4, 0, -30, -20), (14, 0, 20, 10), (26, 0, 40, 30), (40, 20, 40, 20)], lag=2)
    spines(a, 0, 0); spines(a, 4, 34); spines(a, 26, -20); spines(a, 40, -30)
    a.legs([(0, 10, 0, 6), (4, 0, 0, 10), (14, 80, 0, 10), (26, 30, 0, 6), (40, 20, 0, 6)], [(0, -16, 0, 0), (4, -6, 0, 0), (14, -130, 0, 0), (26, -60, 0, 0), (40, -40, 0, 0)])
    a.hair([(0, 0, 0, 0), (4, -24, 0, 0), (14, 16, 0, 0), (26, 20, 0, 10), (40, 10, 0, 10)], delay=2)
    a.cloth([(0, 0, 0, 0), (4, -10, 0, 0, 20), (14, 10, 0, 0, 24), (26, -10, 0, 0, 10), (40, -10, 0, 0, 10)])
    a.done()

    anims_quad(B, claw, claws, tent, tents, tail, spines)


# >>>QUAD
# ================================================================== PHASE 2 quadruped stance (FpeEntity stance 1)
# The giant drops onto her huge clawed hands (arms are longer than the legs -> gorilla/wolf gait, haunches high).
# Root is lowered QPOS and the hips/torso pitch forward; the legs fold so the boots stay on the floor.
QP = {"body": (-36, 0, 0), "chest": (-50, 0, 0), "head": (80, 0, -4),
      "arm_r": (55, 0, 22), "fore_r": (75, 0, 0), "hand_r": (-44, 0, 0),
      "arm_l": (55, 0, -22), "fore_l": (75, 0, 0), "hand_l": (-44, 0, 0),
      "leg_r": (46, 0, 10), "shin_r": (-99, 0, 0), "foot_r": (53, 0, 0),
      "leg_l": (46, 0, -10), "shin_l": (-99, 0, 0), "foot_l": (53, 0, 0)}
QPOS = (0, -4, 0)
QBASE = {"dress_f": (24, 0, 0), "dress_b": (24, 0, 0), "coat_b": (40, 0, 0), "coat_r": (55, 0, 6), "coat_l": (55, 0, -6)}
UP = {"body": (0, 0, 0), "chest": (-14, 0, 0), "head": (12, 0, -6),
      "arm_r": (14, 0, 36), "fore_r": (46, 0, 0), "hand_r": (0, 0, 0),
      "arm_l": (6, 0, -10), "fore_l": (14, 0, 0), "hand_l": (0, 0, 0),
      "leg_r": (10, 0, 6), "shin_r": (-16, 0, 0), "foot_r": (6, 0, 0),
      "leg_l": (10, 0, -6), "shin_l": (-16, 0, 0), "foot_l": (6, 0, 0)}
QTAIL = -30  # tail lift while on all fours (tail streams out behind)
QTENT = -20  # tentacles rear a little higher


def anims_quad(B, claw, claws, tent, tents, tail, spines):
    REST_Q = {**REST2, **QP, **QBASE}

    def mk(name, ticks, loop=False, cloth_base=True):
        a = A(B, name, ticks, REST_Q, PROPS2, loop)
        a.prest = {"root": QPOS}
        if cloth_base: a.base = dict(QBASE)
        return a

    def q(a, t, pos=(0, 0, 0), **d):
        """full quad pose at t: QP + per-bone deltas, root position = QPOS + pos"""
        for b, v in QP.items():
            a.rot(b, (t, *add3(v, d.get(b, (0, 0, 0)))))
        a.pos("root", (t, *add3(QPOS, pos)))
        for b, v in d.items():
            if b not in QP: a.rot(b, (t, *v))
        return a

    def up(a, t, pos=(0, 0, 0), **d):
        for b, v in UP.items():
            a.rot(b, (t, *add3(v, d.get(b, (0, 0, 0)))))
        a.pos("root", (t, *pos))
        for b, v in d.items():
            if b not in UP: a.rot(b, (t, *v))
        return a

    def qtail(a, keys, lag=1.5):
        tail(a, [(t, y, l + QTAIL, c) for (t, y, l, c) in keys], lag)

    def qtents(a, keys, lag=1.5):
        tents(a, [(t, rx + QTENT, c, sp) for (t, rx, c, sp) in keys], lag)

    # ---------------------------------------------------------------- quad_idle (80): low prowl, ribs heave, head hangs and sways, tail + tentacles snake
    a = mk("quad_idle", 80, loop=True)
    for t, k in ((0, 0), (20, 1), (40, 0), (60, 1), (80, 0)):
        sw = (0, -5, 0, 5, 0)[t // 20]
        q(a, t, pos=(0, 0.14 * k, 0.05 * k), chest=(3 * k, sw * 0.4, 0), head=(-3 * k, sw, 2 * k),
          arm_r=(-2 * k, 0, 0), arm_l=(-2 * k, 0, 0), fore_r=(3 * k, 0, 0), fore_l=(3 * k, 0, 0))
    a.at(46, head=(QP["head"][0], 0, -4)).at(48, head=(QP["head"][0] - 10, 18, 12)).at(51, head=(QP["head"][0] - 6, 14, 9)).at(55, head=(QP["head"][0], 5, -4))
    claws(a, 0, -10, 12); claws(a, 26, -10, 12); claws(a, 30, 20, 4); claws(a, 34, -18, 16); claws(a, 40, -10, 12); claws(a, 80, -10, 12)
    qtail(a, [(0, -18, 0, -8), (20, 0, 6, 4), (40, 18, 0, -8), (60, 0, 6, 4), (80, -18, 0, -8)], lag=3)
    for i in range(4):
        bx, by, bz = TENT_REST[i]
        bx += QTENT
        tent(a, i, [(0, (bx, by, bz), 26), (20, (bx + 10, by + 8, bz), 36), (40, (bx, by, bz), 20), (60, (bx - 8, by - 8, bz), 32), (80, (bx, by, bz), 26)], lag=3)
    spines(a, 0, 4); spines(a, 20, 12); spines(a, 40, 4); spines(a, 60, 12); spines(a, 80, 4)
    a.hair([(0, 0, 0, 1), (20, 3, 0, -1), (40, 0, 0, 1), (60, 3, 0, -1), (80, 0, 0, 1)], delay=5)
    a.cloth([(0, 0, 0, 1), (20, 2, 0, -1), (40, 0, 0, 1), (60, 2, 0, -1), (80, 0, 0, 1)], delay=5)
    a.done()

    # ---------------------------------------------------------------- quad_walk (20, additive on quad_idle): lateral-sequence gait RH, RF, LH, LF
    def gait(a):
        R, Pp = a.rot, a.pos
        TW = 2 * math.pi / 20
        for t in range(0, 21, 2):
            for k, s, ph in (("r", 1, 0), ("l", -1, 10)):
                u = TW * (t - ph)
                sw = max(0.0, -math.sin(u))                       # 0..1 while the limb swings forward
                R("leg_" + k, (t, 24 * math.cos(u), 0, 0))
                R("shin_" + k, (t, -38 * sw, 0, 0))
                R("foot_" + k, (t, 10 * math.cos(u) + 18 * sw, 0, 0))
                ua = TW * (t - ph - 5)                            # front limb of the same side lands a quarter later
                swa = max(0.0, -math.sin(ua))
                R("arm_" + k, (t, 26 * math.cos(ua), 0, 4 * s * swa))
                R("fore_" + k, (t, 40 * swa, 0, 0))
                R("hand_" + k, (t, -10 * math.cos(ua) + 24 * swa, 0, 0))
            u = TW * t
            Pp("root", (t, 0, -0.35 * math.cos(2 * u), 0))
            R("body", (t, 2 * math.cos(2 * u), 6 * math.sin(u), 3 * math.sin(u)))
            R("chest", (t, -3 * math.cos(2 * u + 0.6), -7 * math.sin(u - 0.8), -4 * math.sin(u - 0.8)))
            R("head", (t, 4 * math.cos(2 * u + 1.2), 6 * math.sin(u - 1.6), 0))
            R("tail0", (t, 4 * math.cos(2 * u), -16 * math.sin(u), 0))
            for i in range(1, 6):
                R(f"tail{i}", (t, 3 * math.cos(2 * u - 0.5 * i), -9 * math.sin(u - 0.45 * i), 0))
            for i in range(4):
                R(f"tent{i}_0", (t, 8 * math.sin(2 * u - 0.7 - i), (1 if i % 2 == 0 else -1) * 5 * math.sin(u - 1.0), 0))
                for sgm in (1, 2, 3):
                    R(f"tent{i}_{sgm}", (t, 10 * math.sin(2 * u - 0.7 - i - 0.6 * sgm), 0, 0))
            R("spines_r", (t, 0, 0, -5 * math.cos(2 * u))); R("spines_l", (t, 0, 0, 5 * math.cos(2 * u)))
            for bn, amp, lagp in (("hair_b", -6, 1.4), ("hair_r", 4, 1.2), ("hair_l", 4, 1.2), ("bangs", 3, 1.0), ("ah0", -6, 1.6), ("ah1", -8, 2.0), ("ah2", -10, 2.4),
                                  ("coat_b", -6, 1.6), ("coat_r", 5, 1.6), ("coat_l", 5, 1.6), ("dress_f", 4, 1.2), ("dress_b", -4, 1.2), ("pendant", 8, 1.4)):
                R(bn, (t, amp * math.cos(2 * u - lagp), 0, 0.6 * amp * math.sin(u - lagp)))

    a = A(B, "quad_walk", 20, {}, (), loop=True)
    gait(a)
    a.done(base_layer=True)

    # ---------------------------------------------------------------- drop_down (26): rear back 0-4, topple forward 10, claws SLAM the floor 14, rebound 18, prowl 26
    a = mk("drop_down", 26, cloth_base=False)
    up(a, 0)
    up(a, 4, pos=(0, 0.8, 0.5), chest=(12, 0, 0), head=(20, 0, 6), arm_r=(30, 0, 40), arm_l=(30, 0, 60), fore_r=(-20, 0, 0), fore_l=(10, 0, 0))
    up(a, 10, pos=(0, -1.2, -1.6), body=(-18, 0, 0), chest=(-40, 0, 0), head=(46, 0, 0), arm_r=(130, 0, -16), arm_l=(130, 0, 26),
       fore_r=(-36, 0, 0), fore_l=(-4, 0, 0), leg_r=(18, 0, 0), shin_r=(-30, 0, 0), leg_l=(-14, 0, 0))
    q(a, 14, pos=(0, -0.9, -0.4), chest=(-8, 0, 0), head=(-8, 0, 0), arm_r=(4, 0, 6), arm_l=(4, 0, -6), fore_r=(-6, 0, 0), fore_l=(-6, 0, 0))
    q(a, 18, pos=(0, 0.4, 0.1), chest=(4, 0, 0), head=(6, 0, 4))
    q(a, 22, pos=(0, -0.15, 0))
    q(a, 26)
    claws(a, 0, 0); claws(a, 8, -40, 36); claws(a, 14, 10, 20); claws(a, 26, -10, 12)
    tents(a, [(0, 0, 26, None), (6, -30, 40, 1.3), (14, 40 + QTENT, 4, 1.8), (20, QTENT - 10, 30, None), (26, QTENT, 26, None)], lag=1)
    tail(a, [(0, 0, 0, 0), (6, 0, -10, 20), (14, 0, QTAIL + 30, -24), (20, 0, QTAIL - 6, 6), (26, 0, QTAIL, 0)], lag=1.2)
    spines(a, 0, 0); spines(a, 6, -12); spines(a, 14, 30); spines(a, 26, 4)
    for b, v in QBASE.items():
        a.rot(b, (0, 0, 0, 0), (8, v[0] * 0.3, 0, v[2] * 0.3), (14, v[0] * 1.3, 0, v[2] * 2), (18, v[0] * 0.8, 0, v[2]), (26, *v))
    a.hair([(0, 0, 0, 0), (6, -12, 0, 0), (14, 26, 0, 0), (18, -8, 0, 0), (26, 0, 0, 0)], delay=1)
    a.done()

    # ---------------------------------------------------------------- rise_up (26): shove off the floor 5, REAR up 10-13 with a roar, settle upright 26
    a = mk("rise_up", 26, cloth_base=False)
    q(a, 0)
    q(a, 5, pos=(0, -0.8, 0.6), chest=(-4, 0, 0), head=(6, 0, 0), arm_r=(-22, 0, 0), arm_l=(-22, 0, 0), fore_r=(-8, 0, 0), fore_l=(-8, 0, 0))
    up(a, 10, pos=(0, 0.9, 0.8), chest=(26, 0, 0), head=(26, 0, 6), arm_r=(130, 0, 30), arm_l=(130, 0, -20), fore_r=(-30, 0, 0), fore_l=(10, 0, 0),
       leg_r=(-10, 0, 0), shin_r=(10, 0, 0), leg_l=(-10, 0, 0), shin_l=(10, 0, 0))
    up(a, 13, pos=(0, 1.1, 0.8), chest=(30, 0, 0), head=(36, 0, 6), arm_r=(140, 0, 50), arm_l=(140, 0, 0), fore_r=(-40, 0, 0), fore_l=(0, 0, 0),
       leg_r=(-10, 0, 0), shin_r=(10, 0, 0), leg_l=(-10, 0, 0), shin_l=(10, 0, 0))
    up(a, 18, pos=(0, -0.5, -0.2), chest=(-10, 0, 0), head=(4, 0, 0), arm_r=(10, 0, 10), arm_l=(10, 0, -4))
    up(a, 26)
    claws(a, 0, -10, 12); claws(a, 5, 30); claws(a, 10, -40, 40); claws(a, 16, -40, 40); claws(a, 26, 0)
    tents(a, [(0, QTENT, 26, None), (5, QTENT + 20, 40, 0.8), (11, -60, -10, 2.4), (17, -50, -6, 2.2), (26, 0, 26, None)], lag=1)
    tail(a, [(0, 0, QTAIL, 0), (5, 0, QTAIL + 10, 10), (11, 0, 30, -26), (18, 0, 6, 6), (26, 0, 0, 0)], lag=1.2)
    spines(a, 0, 4); spines(a, 5, -8); spines(a, 11, 36); spines(a, 18, 20); spines(a, 26, 0)
    for b, v in QBASE.items():
        a.rot(b, (0, *v), (5, v[0] * 1.1, 0, v[2]), (11, -v[0] * 0.3, 0, v[2] * 3), (16, v[0] * 0.2, 0, v[2]), (26, 0, 0, 0))
    a.hair([(0, 0, 0, 0), (5, 8, 0, 0), (11, -24, 0, 0), (14, -20, 0, 6), (18, 6, 0, 0), (26, 0, 0, 0)], delay=1)
    a.done()

    def gallop_stride(a, t0, per=6, reach=1.0):
        """one rotary-gallop stride starting at t0: fronts reach while hinds push, suspension, then swap"""
        h = per / 2
        q(a, t0, pos=(0, -0.4, 0), chest=(-4, 0, 0), head=(-24, 0, 0),
          arm_r=(40 * reach, 0, -6), arm_l=(34 * reach, 0, 6), fore_r=(-40, 0, 0), fore_l=(-34, 0, 0), hand_r=(30, 0, 0), hand_l=(30, 0, 0),
          leg_r=(-34, 0, 0), leg_l=(-28, 0, 0), shin_r=(28, 0, 0), shin_l=(22, 0, 0), foot_r=(-20, 0, 0), foot_l=(-16, 0, 0))
        q(a, t0 + h * 0.5, pos=(0, 0.9, 0), chest=(4, 0, 0), head=(-28, 0, 0),
          arm_r=(10, 0, 0), arm_l=(6, 0, 0), fore_r=(-10, 0, 0), fore_l=(-6, 0, 0),
          leg_r=(-10, 0, 0), leg_l=(-6, 0, 0), shin_r=(-20, 0, 0), shin_l=(-14, 0, 0))
        q(a, t0 + h, pos=(0, -0.3, 0), chest=(6, 0, 0), head=(-22, 0, 0),
          arm_r=(-34, 0, 0), arm_l=(-28, 0, 0), fore_r=(36, 0, 0), fore_l=(30, 0, 0), hand_r=(-10, 0, 0), hand_l=(-10, 0, 0),
          leg_r=(34 * reach, 0, 0), leg_l=(28 * reach, 0, 0), shin_r=(-36, 0, 0), shin_l=(-30, 0, 0), foot_r=(16, 0, 0), foot_l=(14, 0, 0))
        q(a, t0 + h * 1.5, pos=(0, 0.5, 0), chest=(0, 0, 0), head=(-26, 0, 0),
          arm_r=(4, 0, 0), arm_l=(0, 0, 0), fore_r=(30, 0, 0), fore_l=(26, 0, 0), leg_r=(10, 0, 0), leg_l=(6, 0, 0))

    # ---------------------------------------------------------------- quad_charge (52): roar 3, paw the floor 6 / 9, coil 12, GALLOP 13-33 (head down, ramming),
    #                                                                   skid 34, HEAD-TOSS 37, shake it off, prowl
    a = mk("quad_charge", 52)
    q(a, 0)
    q(a, 3, pos=(0, 0.4, 0.4), chest=(10, 0, 0), head=(24, 0, 6))
    q(a, 5, pos=(0, 0.2, 0.4), chest=(6, 6, 0), head=(4, -6, 0), arm_r=(44, 0, 0), fore_r=(20, 0, 0))
    q(a, 6.5, pos=(0, 0, 0.5), chest=(2, 4, 0), head=(-6, -4, 0), arm_r=(-36, 0, 0), fore_r=(30, 0, 0))
    q(a, 8, pos=(0, 0.2, 0.5), chest=(6, 6, 0), head=(-4, -6, 0), arm_r=(44, 0, 0), fore_r=(20, 0, 0))
    q(a, 9.5, pos=(0, 0, 0.6), chest=(2, 4, 0), head=(-10, -4, 0), arm_r=(-36, 0, 0), fore_r=(30, 0, 0))
    q(a, 12, pos=(0, -1.4, 1.4), chest=(-8, 0, 0), head=(-26, 0, 0), arm_r=(-14, 0, 0), arm_l=(-14, 0, 0), fore_r=(24, 0, 0), fore_l=(24, 0, 0),
      leg_r=(16, 0, 0), leg_l=(16, 0, 0), shin_r=(-14, 0, 0), shin_l=(-14, 0, 0))
    for t0 in (13, 19, 25):
        gallop_stride(a, t0, 6, 1.15)
    q(a, 31, pos=(0, -0.4, 0), chest=(-4, 0, 0), head=(-26, 0, 0), arm_r=(40, 0, -6), arm_l=(34, 0, 6), fore_r=(-40, 0, 0), fore_l=(-34, 0, 0),
      leg_r=(-30, 0, 0), leg_l=(-26, 0, 0), shin_r=(24, 0, 0), shin_l=(20, 0, 0))
    q(a, 34, pos=(0, -1.2, 0.6), chest=(12, 0, 0), head=(-14, 0, 0), arm_r=(36, 0, 0), arm_l=(36, 0, 0), fore_r=(-50, 0, 0), fore_l=(-50, 0, 0),
      hand_r=(40, 0, 0), hand_l=(40, 0, 0), leg_r=(26, 0, 0), leg_l=(20, 0, 0), shin_r=(-20, 0, 0), shin_l=(-16, 0, 0))
    q(a, 35.5, pos=(0, -1.4, 0.4), chest=(-10, 0, 0), head=(-44, 0, 0), arm_r=(20, 0, 0), arm_l=(20, 0, 0), fore_r=(-30, 0, 0), fore_l=(-30, 0, 0))
    q(a, 37, pos=(0, 1.0, -0.8), chest=(30, -6, 0), head=(52, 10, 8), arm_r=(30, 0, 10), arm_l=(14, 0, -6), fore_r=(-20, 0, 0), fore_l=(0, 0, 0))
    q(a, 40, pos=(0, 0.8, -0.6), chest=(24, -4, 0), head=(40, 6, 4))
    q(a, 44, pos=(0, -0.3, 0), chest=(-2, 2, 0), head=(-6, -10, -10))
    q(a, 46, head=(0, 10, 10))
    q(a, 52)
    claws(a, 0, -10, 12); claws(a, 3, -40, 36); claws(a, 12, 30); claws(a, 34, 60); claws(a, 37, -40, 40); claws(a, 44, -10, 12); claws(a, 52, -10, 12)
    qtents(a, [(0, 0, 26, None), (3, -40, -6, 2.2), (12, 30, 40, 0.8), (14, 60, 10, 0.6), (33, 60, 10, 0.6), (37, -30, 30, 1.8), (44, 0, 26, None), (52, 0, 26, None)], lag=1)
    qtail(a, [(0, 0, 0, 0), (3, 0, -20, -16), (12, 0, 10, 20), (14, 0, -24, -6), (20, 8, -20, -4), (26, -8, -24, -6), (33, 6, -20, -4),
              (35, 0, 10, 24), (37, 0, -16, -14), (44, -14, 0, 6), (52, 0, 0, 0)], lag=1)
    spines(a, 0, 4); spines(a, 3, 34); spines(a, 12, -6); spines(a, 14, -14); spines(a, 33, -14); spines(a, 37, 30); spines(a, 52, 4)
    a.hair([(0, 0, 0, 0), (3, -10, 0, 0), (12, 8, 0, 0), (15, -26, 0, 0), (33, -26, 0, 4), (35, 16, 0, 0), (37, -20, 0, -10), (44, 6, 0, 8), (52, 0, 0, 0)], delay=1)
    a.cloth([(0, 0, 0, 0), (3, -4, 0, 0, 6), (12, 4, 0, 0), (15, -30, 0, 0, 10), (33, -30, 0, 0, 12), (35, 14, 0, 0, 8), (40, -6, 0, 0, 4), (52, 0, 0, 0)], delay=1)
    a.done()

    # ---------------------------------------------------------------- quad_pounce (46): crouch + butt-wiggle 3-11, LAUNCH 13, airborne claws high 17, CRASH down 23,
    #                                                                   pin + grind 24-30, bite at 28, back off
    a = mk("quad_pounce", 46)
    q(a, 0)
    crouch = dict(chest=(-12, 0, 0), head=(14, 0, 0), arm_r=(-10, 0, 0), arm_l=(-10, 0, 0), fore_r=(12, 0, 0), fore_l=(12, 0, 0),
                  leg_r=(16, 0, 0), leg_l=(16, 0, 0), shin_r=(-18, 0, 0), shin_l=(-18, 0, 0), foot_r=(6, 0, 0), foot_l=(6, 0, 0))
    q(a, 3, pos=(0, -1.2, 1.2), **crouch)
    for k, t in enumerate((5, 7, 9, 11)):
        s = 1 if k % 2 == 0 else -1
        q(a, t, pos=(0.5 * s, -1.6, 1.6), body=(0, 9 * s, 3 * s), **crouch)
    q(a, 13, pos=(0, 1.2, -1.2), chest=(22, 0, 0), head=(-10, 0, 0), arm_r=(84, 0, -4), arm_l=(84, 0, 4), fore_r=(-64, 0, 0), fore_l=(-64, 0, 0),
      hand_r=(40, 0, 0), hand_l=(40, 0, 0), leg_r=(-52, 0, 0), leg_l=(-46, 0, 0), shin_r=(84, 0, 0), shin_l=(80, 0, 0), foot_r=(-30, 0, 0), foot_l=(-30, 0, 0))
    q(a, 17, pos=(0, 3.2, -1.8), chest=(26, 0, 0), head=(-14, 0, 0), arm_r=(112, 0, 14), arm_l=(112, 0, -14), fore_r=(-56, 0, 0), fore_l=(-56, 0, 0),
      hand_r=(30, 0, 0), hand_l=(30, 0, 0), leg_r=(-30, 0, 0), leg_l=(-26, 0, 0), shin_r=(30, 0, 0), shin_l=(26, 0, 0))
    q(a, 21, pos=(0, 1.6, -2.0), chest=(8, 0, 0), head=(-6, 0, 0), arm_r=(64, 0, 6), arm_l=(64, 0, -6), fore_r=(-40, 0, 0), fore_l=(-40, 0, 0),
      leg_r=(4, 0, 0), leg_l=(4, 0, 0), shin_r=(-10, 0, 0), shin_l=(-10, 0, 0))
    q(a, 23, pos=(0, -1.8, -2.0), chest=(-14, 0, 0), head=(-6, 0, 0), arm_r=(12, 0, 0), arm_l=(12, 0, 0), fore_r=(-26, 0, 0), fore_l=(-26, 0, 0),
      leg_r=(14, 0, 0), leg_l=(14, 0, 0), shin_r=(-18, 0, 0), shin_l=(-18, 0, 0))
    q(a, 25, pos=(0, -1.3, -2.0), chest=(-10, 3, 2), head=(-10, -6, 0), arm_r=(14, 0, 0), arm_l=(10, 0, 0), fore_r=(-24, 0, 0), fore_l=(-26, 0, 0))
    q(a, 28, pos=(0, -1.6, -2.0), chest=(-16, -3, -2), head=(-26, 8, 6), arm_r=(10, 0, 0), arm_l=(14, 0, 0), fore_r=(-26, 0, 0), fore_l=(-22, 0, 0))
    q(a, 31, pos=(0, -1.2, -1.9), chest=(-10, 2, 0), head=(0, 0, 0), arm_r=(12, 0, 0), arm_l=(12, 0, 0), fore_r=(-24, 0, 0), fore_l=(-24, 0, 0))
    q(a, 38, pos=(0, -0.2, -0.8), chest=(4, 0, 0), head=(4, 0, -4))
    q(a, 46)
    a.scl("head", (0, 1, 1, 1), (26, 1, 1, 1), (28, 1.2, 1.2, 1.2), (31, 1, 1, 1), (46, 1, 1, 1))
    claws(a, 0, -10, 12); claws(a, 3, 20); claws(a, 11, 20); claws(a, 13, -40, 40); claws(a, 21, -40, 40); claws(a, 23, 60, 30); claws(a, 30, 80, 10)
    claws(a, 36, 20); claws(a, 46, -10, 12)
    qtents(a, [(0, 0, 26, None), (3, -10, 40, 0.8), (11, -10, 40, 0.8), (13, 50, 4, 1.0), (19, 40, 10, 1.4), (23, 200, -6, 1.0), (31, 200, -6, 1.0), (37, -10, 30, None), (46, 0, 26, None)], lag=1)
    qtail(a, [(0, 0, 0, 0), (3, 0, 20, 10), (5, 30, 20, 10), (7, -30, 20, 10), (9, 30, 20, 10), (11, -30, 20, 10), (13, 0, -40, -20), (19, 0, -50, -14),
              (23, 0, 20, 20), (30, 10, 0, 6), (46, 0, 0, 0)], lag=1)
    spines(a, 0, 4); spines(a, 3, -10); spines(a, 13, 20); spines(a, 23, 36); spines(a, 31, 24); spines(a, 46, 4)
    a.hair([(0, 0, 0, 0), (3, 4, 0, 0), (13, -24, 0, 0), (19, -16, 0, 0), (23, 28, 0, 0), (26, -8, 0, 4), (29, 6, 0, -6), (36, 0, 0, 0), (46, 0, 0, 0)], delay=1)
    a.cloth([(0, 0, 0, 0), (3, 4, 0, 0), (5, 2, 0, 6), (7, 2, 0, -6), (9, 2, 0, 6), (11, 2, 0, -6), (13, -26, 0, 0, 6), (19, -20, 0, 0, 10),
             (23, 20, 0, 0, 26), (30, 6, 0, 0, 10), (46, 0, 0, 0)], delay=1)
    a.done()

    # ---------------------------------------------------------------- quad_rake (40): rear half-up 4-10 (right claw cocked), RAKE R 12, left cocked 17, RAKE L 20,
    #                                                                 both claws high 25, DOUBLE SLAM 28, grind, drop back down
    a = mk("quad_rake", 40)
    q(a, 0)
    rear = dict(leg_r=(-12, 0, 0), leg_l=(-12, 0, 0), shin_r=(16, 0, 0), shin_l=(16, 0, 0), foot_r=(-4, 0, 0), foot_l=(-4, 0, 0))
    q(a, 5, pos=(0, 1.2, 0.8), body=(10, 0, 0), chest=(30, 10, 0), head=(-34, -8, 0), arm_r=(96, 0, 30), fore_r=(-50, 0, 0), hand_r=(40, 0, 0),
      arm_l=(26, 0, 0), fore_l=(-20, 0, 0), **rear)
    q(a, 10, pos=(0, 1.5, 0.9), body=(12, 0, 0), chest=(36, 20, 0), head=(-38, -16, 0), arm_r=(124, -20, 46), fore_r=(-56, 0, 0), hand_r=(40, 0, 0),
      arm_l=(30, 0, 0), fore_l=(-24, 0, 0), **rear)
    q(a, 12, pos=(0, 0.6, -0.8), body=(6, 0, 0), chest=(18, -24, 0), head=(-22, 18, 0), arm_r=(20, 34, -34), fore_r=(-16, 0, 0), hand_r=(10, 0, 0),
      arm_l=(26, 0, 0), fore_l=(-20, 0, 0), **rear)
    q(a, 14, pos=(0, 0.6, -0.8), body=(6, 0, 0), chest=(20, -28, 0), head=(-24, 20, 0), arm_r=(-6, 36, -36), fore_r=(10, 0, 0), **rear)
    q(a, 17, pos=(0, 1.4, 0.4), body=(12, 0, 0), chest=(34, -20, 0), head=(-36, 16, 0), arm_l=(124, 20, -46), fore_l=(-56, 0, 0), hand_l=(40, 0, 0),
      arm_r=(26, 0, 0), fore_r=(-20, 0, 0), **rear)
    q(a, 20, pos=(0, 0.6, -1.4), body=(6, 0, 0), chest=(18, 24, 0), head=(-22, -18, 0), arm_l=(20, -34, 34), fore_l=(-16, 0, 0), hand_l=(10, 0, 0),
      arm_r=(26, 0, 0), fore_r=(-20, 0, 0), **rear)
    q(a, 22, pos=(0, 0.6, -1.4), body=(6, 0, 0), chest=(20, 28, 0), head=(-24, -20, 0), arm_l=(-6, -36, 36), fore_l=(10, 0, 0), **rear)
    q(a, 25, pos=(0, 2.0, 0.4), body=(14, 0, 0), chest=(42, 0, 0), head=(-36, 0, 0), arm_r=(132, 0, 16), arm_l=(132, 0, -16), fore_r=(-46, 0, 0), fore_l=(-46, 0, 0),
      hand_r=(30, 0, 0), hand_l=(30, 0, 0), **rear)
    q(a, 28, pos=(0, -1.4, -1.6), chest=(-14, 0, 0), head=(-8, 0, 0), arm_r=(16, 0, -4), arm_l=(16, 0, 4), fore_r=(-30, 0, 0), fore_l=(-30, 0, 0),
      leg_r=(10, 0, 0), leg_l=(10, 0, 0), shin_r=(-12, 0, 0), shin_l=(-12, 0, 0))
    q(a, 30, pos=(0, -1.1, -1.5), chest=(-10, 2, 2), head=(-4, 0, 4), arm_r=(16, 0, -4), arm_l=(16, 0, 4), fore_r=(-30, 0, 0), fore_l=(-30, 0, 0))
    q(a, 32, pos=(0, -1.3, -1.5), chest=(-12, -2, -2), head=(-6, 0, -4), arm_r=(16, 0, -4), arm_l=(16, 0, 4), fore_r=(-30, 0, 0), fore_l=(-30, 0, 0))
    q(a, 40)
    claw(a, "r", 0, -10, 12); claw(a, "r", 5, -40, 40); claw(a, "r", 12, 30, 30); claw(a, "r", 15, 10); claw(a, "r", 25, -40, 40); claw(a, "r", 28, 60, 20); claw(a, "r", 40, -10, 12)
    claw(a, "l", 0, -10, 12); claw(a, "l", 14, -40, 40); claw(a, "l", 20, 30, 30); claw(a, "l", 23, 10); claw(a, "l", 25, -40, 40); claw(a, "l", 28, 60, 20); claw(a, "l", 40, -10, 12)
    qtents(a, [(0, 0, 26, None), (5, -30, 40, 1.4), (12, -10, 20, 1.8), (20, -10, 20, 1.8), (25, -50, 40, 1.4), (28, 40, 6, 1.6), (34, 10, 20, None), (40, 0, 26, None)])
    qtail(a, [(0, 0, 0, 0), (5, 0, 20, 10), (10, 30, 20, 10), (12, -30, 10, -10), (17, -30, 20, 10), (20, 30, 10, -10), (25, 0, 20, 20), (28, 0, -30, -20), (40, 0, 0, 0)], lag=1.2)
    spines(a, 0, 4); spines(a, 10, 20); spines(a, 12, 30); spines(a, 20, 30); spines(a, 25, 10); spines(a, 28, 40); spines(a, 40, 4)
    a.hair([(0, 0, 0, 0), (5, -10, 0, 0), (10, -10, 0, -8), (12, 8, 0, 18), (17, -8, 0, 8), (20, 8, 0, -18), (25, -16, 0, 0), (28, 24, 0, 0), (32, -4, 0, 0), (40, 0, 0, 0)], delay=1)
    a.cloth([(0, 0, 0, 0), (5, -10, 0, 0, 6), (12, 6, 0, -14, 10), (20, 6, 0, 14, 10), (25, -12, 0, 0, 8), (28, 14, 0, 0, 24), (34, 4, 0, 0, 8), (40, 0, 0, 0)], delay=1)
    a.done()

    # ---------------------------------------------------------------- quad_tail_sweep (40): claws planted, hindquarters coil 3-9, WHIP round 10-20 (hit 16), skid out
    a = mk("quad_tail_sweep", 40)
    plant = dict(arm_r=(10, 0, 8), arm_l=(10, 0, -8), fore_r=(-10, 0, 0), fore_l=(-10, 0, 0))
    q(a, 0, root=(0, 0, 0))
    q(a, 9, pos=(0, -1.0, 0), root=(0, 50, 0), body=(0, 10, 0), chest=(-6, -24, 0), head=(4, -26, 0), leg_r=(20, 0, 0), leg_l=(-6, 0, 0),
      shin_r=(-18, 0, 0), **plant)
    q(a, 12, pos=(0, -0.6, 0), root=(0, -60, 0), body=(0, -14, 0), chest=(-8, 10, 0), head=(0, 16, 0), **plant)
    q(a, 16, pos=(0, -0.4, 0), root=(0, -175, 0), body=(0, -16, 0), chest=(-10, 14, 0), head=(4, 20, 0), leg_r=(-20, 0, 0), leg_l=(20, 0, 0), **plant)
    q(a, 20, pos=(0, -0.6, 0), root=(0, -320, 0), body=(0, -12, 0), chest=(-10, 10, 0), head=(4, 14, 0), leg_r=(20, 0, 0), leg_l=(-20, 0, 0), **plant)
    q(a, 24, pos=(0, -1.0, 0), root=(0, -378, 0), body=(0, 8, 0), chest=(-8, -8, 0), head=(6, -10, 0), leg_r=(-10, 0, 0), leg_l=(14, 0, 0))
    q(a, 30, pos=(0, -0.3, 0), root=(0, -362, 0), chest=(-2, -2, 0))
    q(a, 40, root=(0, -360, 0))
    claws(a, 0, -10, 12); claws(a, 9, 50, 10); claws(a, 22, 50, 10); claws(a, 30, -10, 12); claws(a, 40, -10, 12)
    tail(a, [(0, 0, QTAIL, 0), (9, -50, QTAIL - 6, 16), (12, 20, -46, 16), (16, 44, -54, 22), (20, 44, -54, 22), (24, 0, -30, 4), (30, -12, QTAIL, 0), (40, 0, QTAIL, 0)], lag=0.8)
    qtents(a, [(0, 0, 26, None), (9, -10, 40, 1.4), (16, 10, 0, 2.6), (22, 10, 0, 2.4), (30, 0, 20, None), (40, 0, 26, None)], lag=1)
    spines(a, 0, 4); spines(a, 9, -6); spines(a, 16, 28); spines(a, 24, 12); spines(a, 40, 4)
    a.hair([(0, 0, 0, 0), (9, 4, 0, -12), (16, -6, 0, 30), (22, -6, 0, 30), (28, 0, 0, -8), (40, 0, 0, 0)], delay=1)
    a.cloth([(0, 0, 0, 0), (9, 4, 0, -8, 6), (16, -6, 0, 18, 28), (22, -6, 0, 18, 28), (30, 0, 0, -4, 4), (40, 0, 0, 0)], delay=1)
    a.done()

    # ---------------------------------------------------------------- quad_eruption (54): rear up roaring 4-14, PLUNGE both claws + tentacles into the floor 18,
    #                                                                     buried + trembling, second pulse 30, RIP free 40, prowl
    a = mk("quad_eruption", 54)
    q(a, 0)
    tall = dict(leg_r=(-20, 0, 0), leg_l=(-20, 0, 0), shin_r=(26, 0, 0), shin_l=(26, 0, 0), foot_r=(-8, 0, 0), foot_l=(-8, 0, 0))
    q(a, 6, pos=(0, 2.0, 1.0), body=(18, 0, 0), chest=(50, 0, 0), head=(-34, 0, 0), arm_r=(120, 0, 30), arm_l=(120, 0, -30), fore_r=(-70, 0, 0), fore_l=(-70, 0, 0),
      hand_r=(40, 0, 0), hand_l=(40, 0, 0), **tall)
    q(a, 13, pos=(0, 2.4, 1.2), body=(22, 0, 0), chest=(56, 0, 0), head=(-50, 0, 0), arm_r=(150, 0, 12), arm_l=(150, 0, -12), fore_r=(-70, 0, 0), fore_l=(-70, 0, 0),
      hand_r=(40, 0, 0), hand_l=(40, 0, 0), **tall)
    q(a, 16, pos=(0, -1.4, -0.4), body=(-4, 0, 0), chest=(-10, 0, 0), head=(-10, 0, 0), arm_r=(30, 0, 0), arm_l=(30, 0, 0), fore_r=(-50, 0, 0), fore_l=(-50, 0, 0))
    q(a, 18, pos=(0, -2.2, -0.8), body=(-6, 0, 0), chest=(-14, 0, 0), head=(-6, 0, 0), arm_r=(24, 0, -4), arm_l=(24, 0, 4), fore_r=(-46, 0, 0), fore_l=(-46, 0, 0),
      hand_r=(10, 0, 0), hand_l=(10, 0, 0), leg_r=(12, 0, 0), leg_l=(12, 0, 0), shin_r=(-14, 0, 0), shin_l=(-14, 0, 0))
    for t in range(21, 39, 3):
        j = 1 if (t // 3) % 2 else -1
        jolt = -6 if t == 30 else 0
        q(a, t, pos=(0.15 * j, -2.0 + (0.6 if t == 30 else 0), -0.8), body=(-6, 0, 0), chest=(-12 + 2 * j + jolt, 2 * j, 2 * j), head=(-4 + 6 * (t == 30), 4 * j, 0),
          arm_r=(24, 0, -4), arm_l=(24, 0, 4), fore_r=(-46, 0, 0), fore_l=(-46, 0, 0), hand_r=(10, 0, 0), hand_l=(10, 0, 0),
          leg_r=(12, 0, 0), leg_l=(12, 0, 0), shin_r=(-14, 0, 0), shin_l=(-14, 0, 0))
    q(a, 40, pos=(0, 1.2, 0.8), body=(10, 0, 0), chest=(32, 0, 0), head=(-26, 0, 0), arm_r=(96, 0, 40), arm_l=(96, 0, -40), fore_r=(-50, 0, 0), fore_l=(-50, 0, 0), **tall)
    q(a, 46, pos=(0, -0.3, 0), chest=(-4, 0, 0), head=(4, 0, 0))
    q(a, 54)
    claws(a, 0, -10, 12); claws(a, 6, -40, 40); claws(a, 16, 20, 30); claws(a, 18, 40, 40); claws(a, 38, 40, 40); claws(a, 40, -40, 40); claws(a, 46, 10); claws(a, 54, -10, 12)
    qtents(a, [(0, 0, 26, None), (6, -60, 30, 1.8), (13, -70, 20, 2.0), (16, 140, 0, 1.2), (18, 200, -4, 1.0), (38, 200, -4, 1.0), (40, -60, 10, 2.2), (48, -10, 20, None), (54, 0, 26, None)], lag=1)
    qtail(a, [(0, 0, 0, 0), (6, 0, 30, -20), (13, 0, 40, -24), (18, 0, -40, 20), (30, 0, -50, 26), (38, 0, -40, 20), (42, 0, 20, -10), (54, 0, 0, 0)], lag=1.2)
    spines(a, 0, 4); spines(a, 6, 30); spines(a, 13, 20); spines(a, 18, 40); spines(a, 30, 46); spines(a, 38, 36); spines(a, 42, 10); spines(a, 54, 4)
    a.hair([(0, 0, 0, 0), (6, -20, 0, 0), (13, -26, 0, 0), (18, 30, 0, 0), (22, 10, 0, 4), (30, 18, 0, -4), (38, 10, 0, 0), (40, -20, 0, 0), (48, 4, 0, 0), (54, 0, 0, 0)], delay=1)
    a.cloth([(0, 0, 0, 0), (6, -12, 0, 0, 8), (13, -16, 0, 0, 10), (18, 18, 0, 0, 30), (30, 12, 0, 0, 34), (38, 10, 0, 0, 24), (40, -10, 0, 0, 10), (54, 0, 0, 0)], delay=1)
    a.done()

    # ---------------------------------------------------------------- quad_bite (32): sniff 3, head drawn back + grin opens 7, LUNGE-BITE 11, thrash 13-16, FLING 18, recover
    a = mk("quad_bite", 32)
    q(a, 0)
    q(a, 3, pos=(0, 0.2, 0), chest=(4, 0, 0), head=(10, 8, 12))
    q(a, 7, pos=(0, 0.5, 1.8), chest=(16, 0, 0), head=(30, 0, 0), arm_r=(-16, 0, 0), arm_l=(-16, 0, 0), fore_r=(16, 0, 0), fore_l=(16, 0, 0),
      leg_r=(12, 0, 0), leg_l=(12, 0, 0), shin_r=(-10, 0, 0), shin_l=(-10, 0, 0))
    q(a, 9, pos=(0, 0.3, 1.6), chest=(18, 0, 0), head=(34, 0, 0), arm_r=(-18, 0, 0), arm_l=(-18, 0, 0), fore_r=(18, 0, 0), fore_l=(18, 0, 0))
    q(a, 11, pos=(0, -0.9, -1.6), chest=(-18, 0, 0), head=(-26, 0, 0), arm_r=(24, 0, 0), arm_l=(24, 0, 0), fore_r=(-30, 0, 0), fore_l=(-30, 0, 0),
      leg_r=(-22, 0, 0), leg_l=(-22, 0, 0), shin_r=(26, 0, 0), shin_l=(26, 0, 0))
    q(a, 13, pos=(0.3, -0.8, -1.5), chest=(-16, 10, 4), head=(-20, 28, 18), arm_r=(20, 0, 0), arm_l=(24, 0, 0), fore_r=(-26, 0, 0), fore_l=(-30, 0, 0))
    q(a, 15, pos=(-0.3, -0.8, -1.5), chest=(-16, -10, -4), head=(-20, -28, -18), arm_r=(24, 0, 0), arm_l=(20, 0, 0), fore_r=(-30, 0, 0), fore_l=(-26, 0, 0))
    q(a, 16.5, pos=(0.2, -0.8, -1.4), chest=(-14, 12, 4), head=(-14, 30, 16))
    q(a, 18, pos=(0, 0.4, -1.1), chest=(14, -16, 0), head=(44, -36, -12), arm_r=(10, 0, 0), arm_l=(30, 0, 0), fore_r=(-10, 0, 0), fore_l=(-30, 0, 0))
    q(a, 21, pos=(0, 0.3, -0.9), chest=(10, -10, 0), head=(32, -24, -6))
    q(a, 26, pos=(0, -0.2, -0.3), chest=(-2, 0, 0), head=(-2, 0, 0))
    q(a, 32)
    a.scl("head", (0, 1, 1, 1), (7, 1.08, 1.08, 1.08), (10, 1.05, 1.05, 1.05), (11, 1.32, 1.32, 1.32), (14, 1.22, 1.22, 1.22), (18, 1.25, 1.25, 1.25), (22, 1, 1, 1), (32, 1, 1, 1))
    claws(a, 0, -10, 12); claws(a, 7, 40); claws(a, 11, -30, 30); claws(a, 14, 50); claws(a, 18, -30, 30); claws(a, 26, -10, 12); claws(a, 32, -10, 12)
    qtents(a, [(0, 0, 26, None), (7, 30, 50, 0.6), (11, -60, -6, 2.0), (16, -50, 0, 2.2), (18, -30, 20, 1.6), (26, 0, 26, None), (32, 0, 26, None)], lag=1)
    qtail(a, [(0, 0, 0, 0), (7, 0, 20, 20), (11, 0, -30, -20), (13, 20, -26, -10), (15, -20, -26, -10), (18, 30, -10, 10), (26, 0, 0, 0), (32, 0, 0, 0)], lag=1)
    spines(a, 0, 4); spines(a, 7, -10); spines(a, 11, 34); spines(a, 18, 26); spines(a, 32, 4)
    a.hair([(0, 0, 0, 0), (3, 0, 0, 8), (7, -12, 0, 0), (11, 26, 0, 0), (13, 10, 0, 24), (15, 10, 0, -24), (17, 10, 0, 20), (18, -20, 0, -16), (24, 4, 0, 0), (32, 0, 0, 0)], delay=1)
    a.cloth([(0, 0, 0, 0), (7, -6, 0, 0), (11, 14, 0, 0, 10), (13, 6, 0, 10, 6), (15, 6, 0, -10, 6), (18, -8, 0, -6, 4), (32, 0, 0, 0)], delay=1)
    a.done()

    # ---------------------------------------------------------------- quad_spine_volley (44): back arches like a cat + hiss 4-14, spines bristle,
    #                                                                       VOLLEYS 18 / 24 / 30 (shudder, spines snap forward), settle
    a = mk("quad_spine_volley", 44)
    q(a, 0)
    arch = dict(body=(16, 0, 0), chest=(-14, 0, 0), head=(-20, 0, 0), arm_r=(16, 0, 4), arm_l=(16, 0, -4), fore_r=(-40, 0, 0), fore_l=(-40, 0, 0),
                hand_r=(22, 0, 0), hand_l=(22, 0, 0), leg_r=(-26, 0, 0), leg_l=(-26, 0, 0), shin_r=(42, 0, 0), shin_l=(42, 0, 0), foot_r=(-16, 0, 0), foot_l=(-16, 0, 0))
    q(a, 6, pos=(0, 1.6, 0.2), **{**arch, "head": (-26, 10, 14)})
    q(a, 8, pos=(0, 1.7, 0.2), **{**arch, "head": (-26, -10, -14)})
    q(a, 12, pos=(0, 1.8, 0.2), **arch)
    for t in (18, 24, 30):
        q(a, t - 2, pos=(0, 1.5, 0.4), **{**arch, "chest": (-8, 0, 0), "head": (-14, 0, 0)})
        q(a, t, pos=(0, 2.1, -0.4), **{**arch, "chest": (-22, 0, 0), "head": (-8, 0, 0), "body": (20, 0, 0)})
        spines(a, t - 2, 56); spines(a, t, -16); spines(a, t + 2.5, 30)
        a.scl("spines_r", (t - 2, 1.5, 1.5, 1.5), (t, 1.15, 1.15, 1.15), (t + 2.5, 1.4, 1.4, 1.4))
        a.scl("spines_l", (t - 2, 1.5, 1.5, 1.5), (t, 1.15, 1.15, 1.15), (t + 2.5, 1.4, 1.4, 1.4))
    q(a, 36, pos=(0, 0.6, 0), chest=(-4, 0, 0), head=(-6, 0, 0))
    q(a, 44)
    a.scl("spines_r", (0, 1, 1, 1), (12, 1.4, 1.4, 1.4), (36, 1.1, 1.1, 1.1), (44, 1, 1, 1))
    a.scl("spines_l", (0, 1, 1, 1), (12, 1.4, 1.4, 1.4), (36, 1.1, 1.1, 1.1), (44, 1, 1, 1))
    spines(a, 0, 4); spines(a, 6, 30); spines(a, 12, 44); spines(a, 36, 14); spines(a, 44, 4)
    claws(a, 0, -10, 12); claws(a, 6, 50, 10); claws(a, 34, 50, 10); claws(a, 44, -10, 12)
    qtents(a, [(0, 0, 26, None), (8, -60, 10, 2.0), (16, -70, 20, 2.2), (18, 20, -4, 1.6), (22, -60, 20, 2.2), (24, 20, -4, 1.6), (28, -60, 20, 2.2),
               (30, 20, -4, 1.6), (36, -10, 20, None), (44, 0, 26, None)], lag=0.8)
    qtail(a, [(0, 0, 0, 0), (6, 0, -60, 30), (12, 0, -70, 34), (18, 10, -64, 30), (24, -10, -64, 30), (30, 10, -64, 30), (36, 0, -20, 10), (44, 0, 0, 0)], lag=1.5)
    a.hair([(0, 0, 0, 0), (6, 0, 0, 10), (8, 0, 0, -10), (12, 6, 0, 0), (18, -14, 0, 0), (24, -14, 0, 0), (30, -14, 0, 0), (36, 0, 0, 0), (44, 0, 0, 0)], delay=1)
    a.cloth([(0, 0, 0, 0), (12, -4, 0, 0, 10), (18, -10, 0, 0, 14), (24, -10, 0, 0, 14), (30, -10, 0, 0, 14), (44, 0, 0, 0)], delay=1)
    a.done()

    # ---------------------------------------------------------------- quad_stampede (64, enraged): roar 3-8, three BOUNDS (launch 10/22/34, SLAM 16/28/40),
    #                                                                   rear up to the sky 44-49, CRATER double-claw slam 52, tremble, prowl
    a = mk("quad_stampede", 64)
    q(a, 0)
    q(a, 4, pos=(0, 0.8, 0.6), chest=(22, 0, 0), head=(36, 0, 0), arm_r=(10, 0, 20), arm_l=(10, 0, -20))
    q(a, 8, pos=(0, -1.0, 1.0), chest=(-8, 0, 0), head=(-10, 0, 0), leg_r=(16, 0, 0), leg_l=(16, 0, 0), shin_r=(-16, 0, 0), shin_l=(-16, 0, 0))
    for t in (10, 22, 34):
        q(a, t, pos=(0, 1.4, -1.0), chest=(12, 0, 0), head=(-12, 0, 0), arm_r=(80, 0, -4), arm_l=(80, 0, 4), fore_r=(-60, 0, 0), fore_l=(-60, 0, 0),
          leg_r=(-46, 0, 0), leg_l=(-46, 0, 0), shin_r=(64, 0, 0), shin_l=(64, 0, 0), foot_r=(-20, 0, 0), foot_l=(-20, 0, 0))
        q(a, t + 3, pos=(0, 2.8, -1.6), chest=(20, 0, 0), head=(-16, 0, 0), arm_r=(104, 0, 14), arm_l=(104, 0, -14), fore_r=(-46, 0, 0), fore_l=(-46, 0, 0),
          leg_r=(30, 0, 0), leg_l=(30, 0, 0), shin_r=(-30, 0, 0), shin_l=(-30, 0, 0))
        q(a, t + 6, pos=(0, -1.5, -1.2), chest=(-14, 0, 0), head=(-12, 0, 0), arm_r=(12, 0, 0), arm_l=(12, 0, 0), fore_r=(-30, 0, 0), fore_l=(-30, 0, 0),
          leg_r=(16, 0, 0), leg_l=(16, 0, 0), shin_r=(-18, 0, 0), shin_l=(-18, 0, 0))
        q(a, t + 9, pos=(0, -0.6, -0.4), chest=(-4, 0, 0), head=(-4, 0, 0), leg_r=(10, 0, 0), leg_l=(10, 0, 0), shin_r=(-10, 0, 0), shin_l=(-10, 0, 0))
    q(a, 46, pos=(0, 2.4, 0.9), body=(20, 0, 0), chest=(58, 0, 0), head=(-44, 0, 0), arm_r=(150, 0, 14), arm_l=(150, 0, -14), fore_r=(-64, 0, 0), fore_l=(-64, 0, 0),
      hand_r=(40, 0, 0), hand_l=(40, 0, 0), leg_r=(-22, 0, 0), leg_l=(-22, 0, 0), shin_r=(28, 0, 0), shin_l=(28, 0, 0))
    q(a, 49, pos=(0, 2.6, 1.0), body=(22, 0, 0), chest=(62, 0, 0), head=(-30, 0, 0), arm_r=(160, -10, 4), arm_l=(160, 10, -4), fore_r=(-60, 0, 0), fore_l=(-60, 0, 0),
      hand_r=(40, 0, 0), hand_l=(40, 0, 0), leg_r=(-22, 0, 0), leg_l=(-22, 0, 0), shin_r=(28, 0, 0), shin_l=(28, 0, 0))
    q(a, 52, pos=(0, -2.4, -1.4), body=(-6, 0, 0), chest=(-16, 0, 0), head=(-8, 0, 0), arm_r=(22, -10, -6), arm_l=(22, 10, 6), fore_r=(-44, 0, 0), fore_l=(-44, 0, 0),
      leg_r=(14, 0, 0), leg_l=(14, 0, 0), shin_r=(-16, 0, 0), shin_l=(-16, 0, 0))
    q(a, 55, pos=(0, -2.1, -1.3), body=(-6, 0, 0), chest=(-12, 3, 3), head=(-4, 6, 0), arm_r=(22, -10, -6), arm_l=(22, 10, 6), fore_r=(-44, 0, 0), fore_l=(-44, 0, 0))
    q(a, 58, pos=(0, -1.4, -0.8), chest=(-8, -2, -2), head=(0, -4, 0))
    q(a, 64)
    claws(a, 0, -10, 12); claws(a, 4, -40, 40)
    for t in (10, 22, 34):
        claws(a, t, -40, 40); claws(a, t + 6, 60, 20); claws(a, t + 9, 20)
    claws(a, 46, -40, 40); claws(a, 52, 80, 20); claws(a, 58, 40); claws(a, 64, -10, 12)
    keys = [(0, 0, 26, None), (4, -50, -10, 2.4)]
    for t in (10, 22, 34):
        keys += [(t, 40, 10, 1.0), (t + 3, 50, 6, 0.9), (t + 6, -40, 30, 2.0)]
    keys += [(46, -70, 20, 2.0), (52, 200, -4, 1.0), (58, 190, -4, 1.0), (64, 0, 26, None)]
    qtents(a, keys, lag=1)
    tk = [(0, 0, 0, 0), (4, 0, -30, -20)]
    for t in (10, 22, 34):
        tk += [(t, 0, -40, -20), (t + 3, 0, -50, -10), (t + 6, 0, 20, 24)]
    tk += [(46, 0, 40, -24), (52, 0, -40, 30), (64, 0, 0, 0)]
    qtail(a, tk, lag=1)
    spines(a, 0, 4); spines(a, 4, 40)
    for t in (10, 22, 34):
        spines(a, t, 10); spines(a, t + 6, 40)
    spines(a, 46, 20); spines(a, 52, 50); spines(a, 64, 4)
    hk = [(0, 0, 0, 0), (4, -20, 0, 0)]
    for t in (10, 22, 34):
        hk += [(t, -20, 0, 0), (t + 3, -26, 0, 0), (t + 6, 26, 0, 0)]
    hk += [(46, -24, 0, 0), (52, 32, 0, 0), (58, 6, 0, 0), (64, 0, 0, 0)]
    a.hair(hk, delay=1)
    ck = [(0, 0, 0, 0), (4, -8, 0, 0, 10)]
    for t in (10, 22, 34):
        ck += [(t, -24, 0, 0, 6), (t + 3, -26, 0, 0, 8), (t + 6, 20, 0, 0, 26)]
    ck += [(46, -16, 0, 0, 10), (52, 22, 0, 0, 36), (58, 8, 0, 0, 14), (64, 0, 0, 0)]
    a.cloth(ck, delay=1)
    a.done()

# <<<QUAD
# ================================================================== main
if __name__ == "__main__":
    b1 = Builder("alice", 1.0, False, 8)
    build(b1)
    anims_p1(b1)
    b1.m.save(DIR + "alice.bbmodel")
    print("alice cubes", len(b1.m.cubes))
    if "anims_p2" in globals():
        b2 = Builder("alice_boss", 3.0, True, 3)
        build(b2)
        anims_p2(b2)
        b2.m.save(DIR + "alice_boss.bbmodel")
        print("alice_boss cubes", len(b2.m.cubes))
