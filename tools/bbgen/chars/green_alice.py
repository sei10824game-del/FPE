"""Green Alice - generates BOTH assets/fpe/bbmodels/green_alice.bbmodel (phase 1) and green_alice_boss.bbmodel (phase 2).
References: docs/ref/confirmed/green_alice_phase1.png / green_alice_phase2.png (the green tint of those frames is lighting).
Phase 1: girl with messy brown jaw-length hair and a huge curling ahoge, glowing toxic-green eyes, white lab coat with wide lapels
over a dark green-grey shirt, black trousers with white piping, black shoes, a black cord crossing into an X that holds a triangle
pendant (toxic-green core). Her power: thin black SPIDER LEGS burst out of her back, webs, toxic flasks.
Phase 2 (boss): a giant pitch-black silhouette of the same girl (tiny head + ahoge, lab-coat hem shredded into long floor spikes)
carried by EIGHT huge jointed spider legs from her back and a bulbous abdomen with a glowing red hourglass / red veins.
Blockbench space: Y up, ground 0, faces -Z. Character's RIGHT = +X.
Rest poses live in the GROUP rotations; every animation key is a DELTA from rest.
Rotation signs (deltas): arm/leg rx>0 = swing forward, torso/head rx>0 = lean back / look up, ry>0 = turn to the character's left,
rz>0 = hanging part swings toward +X. Spider legs (helper L/SL): f=(twist, forward, up), tb/tp>0 = straighten the knee/tip.
Run: python3 tools/bbgen/chars/green_alice.py
"""
import math, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from bbgen import Model, mix  # noqa: E402

DIR = os.path.join(os.path.dirname(__file__), "../../../src/main/resources/assets/fpe/bbmodels/")
HIDE = (.001, .001, .001)


class Pal:
    pass


P1 = Pal()
P1.HAIR, P1.HAIR_D, P1.HAIR_HI = 0x6E4B34, 0x45301F, 0x96694A
P1.SKIN, P1.SKIN_D, P1.SKIN_L = 0xEEDACA, 0xC8AC9B, 0xF8ECE2
P1.EYE, P1.EYE_HI, P1.EYE_D, P1.EYE_RIM = 0x5CF03A, 0xE6FFD0, 0x1F7A16, 0x10200C
P1.LID = 0x231914
P1.COAT, P1.COAT_D, P1.COAT_HI, P1.COAT_S = 0xE4E8E2, 0xBEC6BF, 0xFBFDF9, 0x8E9893
P1.SHIRT, P1.SHIRT_D, P1.SHIRT_HI = 0x3B4B3D, 0x27322A, 0x52664F
P1.PANTS, P1.PANTS_D, P1.PANTS_HI = 0x1B1B20, 0x0F0F12, 0x30303A
P1.PIPE = 0xD6DBD4
P1.SHOE, P1.SHOE_HI = 0x111113, 0x34343E
P1.TOX, P1.TOX_D = 0x7CFF3A, 0x2F9E22
P1.CORD = 0x141418
P1.LEG, P1.LEG_HI, P1.LEG_GL = 0x0B0B0E, 0x2B3A2A, 0x6CFF40
P1.MOUTH = 0x5A3530
P1.GLASS, P1.GLASS_D = 0xCDEFD6, 0x8FB79B
P1.WEB = 0xF2F5F0
P1.RED = 0xC21A1A

P2 = Pal()
P2.HAIR, P2.HAIR_D, P2.HAIR_HI = 0x15111A, 0x09080C, 0x231D2A
P2.SKIN, P2.SKIN_D, P2.SKIN_L = 0x0E0E12, 0x07070A, 0x1A1A21
P2.EYE, P2.EYE_HI, P2.EYE_D, P2.EYE_RIM = 0xA8FF5A, 0xF4FFE4, 0x3E9E24, 0x050506
P2.LID = 0x050506
P2.COAT, P2.COAT_D, P2.COAT_HI, P2.COAT_S = 0x111115, 0x08080A, 0x1E1E25, 0x050506
P2.SHIRT, P2.SHIRT_D, P2.SHIRT_HI = 0x0C0C0F, 0x060607, 0x17171C
P2.PANTS, P2.PANTS_D, P2.PANTS_HI = 0x0A0A0C, 0x050506, 0x18181E
P2.PIPE = 0x1C1C22
P2.SHOE, P2.SHOE_HI = 0x070709, 0x18181E
P2.TOX, P2.TOX_D = 0xFF2A22, 0x8E0E0E
P2.CORD = 0x050506
P2.LEG, P2.LEG_HI, P2.LEG_GL = 0x09090C, 0x3A1418, 0xFF3020
P2.MOUTH = 0x050506
P2.GLASS, P2.GLASS_D = 0x1A1A20, 0x0E0E12
P2.WEB = 0xD8DAD4
P2.RED, P2.RED_D, P2.ABD, P2.ABD_D = 0xE0201A, 0x5A0A0C, 0x140A0D, 0x0A0507


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
        f2 = tuple(min(a, b) for a, b in zip(frm, to))
        t2 = tuple(max(a, b) for a, b in zip(frm, to))
        return self.m.cube(name, parent, self.sc(f2), self.sc(t2), color, origin=self.sc(origin) if origin else None, rot=rot, **kw)

    # ------------------------------------------------------------ painters
    def strands(self, base, hi, dark, ink=None):
        R = self.R

        def f(F):
            cols = [R.random() for _ in range(F.w)]
            for x in range(F.w):
                c = mix(base, hi, 0.6) if cols[x] > 0.82 else mix(base, dark, 0.6) if cols[x] < 0.22 else base
                for y in range(F.h):
                    F.px(x, y, mix(c, dark, 0.45 * (y / max(1, F.h - 1))))
            if ink and F.w >= 4 and F.h >= 6:
                for _ in range(max(1, F.w // 9)):
                    x = R.randint(1, F.w - 2)
                    for y in range(R.randint(0, F.h // 3), F.h - 1):
                        F.px(x, y, ink)
        return f

    def folds(self, base, dark, light, n=3):
        R = self.R

        def f(F):
            for y in range(F.h):
                for x in range(F.w):
                    F.px(x, y, mix(base, dark, 0.22 * (y / max(1, F.h - 1))))
            for i in range(n):
                x = int((i + 0.5) * F.w / n) + R.randint(-1, 1)
                for y in range(F.h):
                    if R.random() < 0.85:
                        F.px(x, y, mix(base, dark, 0.45)); F.px(x + 1, y, mix(base, light, 0.4))
        return f

    def edges(self, col):
        return lambda F: (F.rect(0, 0, 1, F.h, col), F.rect(F.w - 1, 0, 1, F.h, col))

    def frame(self, col):
        return lambda F: (F.rect(0, 0, 1, F.h, col), F.rect(F.w - 1, 0, 1, F.h, col), F.rect(0, 0, F.w, 1, col), F.rect(0, F.h - 1, F.w, 1, col))

    def all(self, fn, skip=()):
        return {k: fn for k in ("north", "south", "east", "west", "up", "down") if k not in skip}

    def blade(self, name, parent, base, ln, w, d, rot, col, tip=None, paint=None):
        """tapered spike pointing UP (+Y) from `base` before rotation"""
        x, y, z = base
        fc = self.all(paint) if paint else None
        self.c(name, parent, (x - w / 2, y, z - d / 2), (x + w / 2, y + ln * 0.5, z + d / 2), col, origin=base, rot=rot, faces=fc)
        self.c(name + "m", parent, (x - w * 0.33, y + ln * 0.45, z - d * 0.4), (x + w * 0.33, y + ln * 0.8, z + d * 0.4), col, origin=base, rot=rot, faces=fc)
        self.c(name + "t", parent, (x - w * 0.15, y + ln * 0.76, z - d * 0.3), (x + w * 0.15, y + ln, z + d * 0.3), tip or col, origin=base, rot=rot)

    def lock(self, name, parent, base, ln, w, d, rot, col, tip=None, paint=None):
        """tapered blade hanging DOWN (-Y) from `base`"""
        x, y, z = base
        fc = self.all(paint) if paint else None
        self.c(name, parent, (x - w / 2, y - ln * 0.5, z - d / 2), (x + w / 2, y, z + d / 2), col, origin=base, rot=rot, faces=fc)
        self.c(name + "m", parent, (x - w * 0.33, y - ln * 0.8, z - d * 0.4), (x + w * 0.33, y - ln * 0.45, z + d * 0.4), col, origin=base, rot=rot, faces=fc)
        self.c(name + "t", parent, (x - w * 0.15, y - ln, z - d * 0.3), (x + w * 0.15, y - ln * 0.76, z + d * 0.3), tip or col, origin=base, rot=rot)


def combo(*fns):
    def f(F):
        for fn in fns: fn(F)
    return f


# ================================================================== face painters
def face_p1(C):
    def f(F):
        W, H = F.w, F.h
        for y in range(H):
            for x in range(W):
                F.px(x, y, mix(C.SKIN, C.SKIN_D, max(0, (0.38 - y / H) / 0.38) * 0.8))
        # big glowing toxic-green eyes (dark rim, bright core, small pupil), tired lower lids
        for cx in (0.29 * W, 0.71 * W):
            ey = 0.55 * H
            F.disc(cx, ey, 0.15 * W, C.EYE_RIM)
            F.disc(cx, ey, 0.115 * W, C.EYE, glow=True)
            F.disc(cx - 0.02 * W, ey - 0.02 * H, 0.06 * W, C.EYE_HI, glow=True)
            F.disc(cx + 0.01 * W, ey + 0.01 * H, max(0.8, 0.025 * W), C.EYE_D)
            F.line(cx - 0.17 * W, ey - 0.12 * H, cx + 0.15 * W, ey - 0.15 * H, C.LID, max(1.5, W * 0.04))  # heavy upper lid
            F.line(cx - 0.1 * W, ey + 0.16 * H, cx + 0.1 * W, ey + 0.16 * H, C.SKIN_D, 1)  # eye bag
            F.line(cx - 0.12 * W, ey - 0.24 * H, cx + 0.1 * W, ey - 0.27 * H, C.HAIR_D, 1)  # brow
        F.line(0.5 * W, 0.68 * H, 0.52 * W, 0.73 * H, C.SKIN_D, 1)  # nose
        F.line(0.42 * W, 0.86 * H, 0.58 * W, 0.85 * H, C.MOUTH, 1.3)  # flat unimpressed mouth
        F.px(int(0.59 * W), int(0.84 * H), C.MOUTH)
    return f


def face_p2(C):
    def f(F):
        W, H = F.w, F.h
        for y in range(H):
            for x in range(W):
                F.px(x, y, mix(C.SKIN_L, C.SKIN, y / H))
        for cx, s in ((0.3 * W, 1), (0.7 * W, -1)):  # narrow glowing slits angled down to the middle
            ey = 0.52 * H
            F.poly([(cx - 0.16 * W, ey - (0.07 * H if s > 0 else 0)), (cx + 0.16 * W, ey - (0.07 * H if s < 0 else 0)),
                    (cx + 0.12 * W, ey + 0.06 * H), (cx - 0.12 * W, ey + 0.06 * H)], C.EYE, glow=True)
            F.rect(cx - 0.02 * W, ey - 0.05 * H, max(1, 0.04 * W), 0.1 * H, C.EYE_HI, glow=True)
        # thin red mouth slit (spider fangs)
        F.line(0.4 * W, 0.8 * H, 0.6 * W, 0.8 * H, C.RED, 1, glow=True)
        F.line(0.42 * W, 0.8 * H, 0.44 * W, 0.88 * H, C.RED, 1, glow=True)
        F.line(0.58 * W, 0.8 * H, 0.56 * W, 0.88 * H, C.RED, 1, glow=True)
    return f


def pendant_paint(C, boss):
    def f(F):
        W, H = F.w, F.h
        F.rect(0, 0, W, H, C.SHIRT_D)
        F.poly([(W / 2, 0), (W, H), (0, H)], C.CORD)
        F.poly([(W / 2, 2), (W - 2, H - 1), (2, H - 1)], C.TOX, glow=True)
        F.poly([(W / 2, 4), (W - 3.5, H - 2), (3.5, H - 2)], C.CORD)
        F.disc(W / 2, H * 0.68, max(1, W * 0.1), C.TOX, glow=True)
    return f


def shirt_front(B, C):
    base = B.folds(C.SHIRT, C.SHIRT_D, C.SHIRT_HI, 2)

    def f(F):
        base(F)
        W, H = F.w, F.h
        # black cord: from the neck sides, crossing into an X, down to the pendant
        F.line(0.15 * W, 0, 0.75 * W, 0.62 * H, C.CORD, max(1, W * 0.04))
        F.line(0.85 * W, 0, 0.25 * W, 0.62 * H, C.CORD, max(1, W * 0.04))
        F.rect(0, 0, W, max(1, H * 0.05), C.SHIRT_HI)
    return f


# ================================================================== spider leg
def spider_leg(B, k, s, i, P, L, W, rest, parent="back"):
    C = B.C
    c, g = B.c, B.g
    L1, L2, L3 = L
    W1, W2, W3 = W
    ry, rz1, rz2, rz3 = rest
    x, y, z = P
    lp = B.all(combo(lambda F: F.rect(0, 0, F.w, F.h, C.LEG), lambda F: F.rect(0, 0, F.w, max(1, F.h // 5), C.LEG_HI)))
    f, t, p = f"lf_{k}{i}", f"lt_{k}{i}", f"lp_{k}{i}"
    g(f, P, parent, rot=(0, s * ry, s * rz1))
    c(f + "a", f, (x, y - W1 / 2, z - W1 / 2), (x + s * L1 * 0.55, y + W1 / 2, z + W1 / 2), C.LEG, faces=lp)
    c(f + "b", f, (x + s * L1 * 0.5, y - W1 * 0.42, z - W1 * 0.42), (x + s * L1, y + W1 * 0.42, z + W1 * 0.42), C.LEG, faces=lp)
    c(f + "k", f, (x + s * (L1 - W1 * 0.5), y - W1 * 0.55, z - W1 * 0.55), (x + s * (L1 + W1 * 0.4), y + W1 * 0.55, z + W1 * 0.55), C.LEG_HI)
    c(f + "g", f, (x + s * (L1 - W1 * 0.2), y + W1 * 0.5, z - W1 * 0.2), (x + s * (L1 + W1 * 0.1), y + W1 * 0.62, z + W1 * 0.2), C.LEG_GL, glow=True)
    for j in range(1):  # bristle on top of the femur
        bx = x + s * L1 * 0.45
        B.blade(f"{f}h{j}", f, (bx, y + W1 * 0.4, z), W1 * 1.1, W1 * 0.3, W1 * 0.3, (0, 0, -s * 50), C.LEG, C.LEG_HI)
    x1 = x + s * L1
    g(t, (x1, y, z), f, rot=(0, 0, -s * rz2))
    c(t + "a", t, (x1, y - W2 / 2, z - W2 / 2), (x1 + s * L2 * 0.6, y + W2 / 2, z + W2 / 2), C.LEG, faces=lp)
    c(t + "b", t, (x1 + s * L2 * 0.55, y - W2 * 0.38, z - W2 * 0.38), (x1 + s * L2, y + W2 * 0.38, z + W2 * 0.38), C.LEG, faces=lp)
    c(t + "k", t, (x1 + s * (L2 - W2 * 0.4), y - W2 * 0.48, z - W2 * 0.48), (x1 + s * (L2 + W2 * 0.3), y + W2 * 0.48, z + W2 * 0.48), C.LEG_HI)
    B.blade(f"{t}h", t, (x1 + s * L2 * 0.4, y + W2 * 0.4, z), W2 * 1.2, W2 * 0.3, W2 * 0.3, (0, 0, -s * 60), C.LEG, C.LEG_HI)
    x2 = x1 + s * L2
    g(p, (x2, y, z), t, rot=(0, 0, -s * rz3))
    c(p + "a", p, (x2, y - W3 / 2, z - W3 / 2), (x2 + s * L3 * 0.5, y + W3 / 2, z + W3 / 2), C.LEG, faces=lp)
    c(p + "b", p, (x2 + s * L3 * 0.45, y - W3 * 0.33, z - W3 * 0.33), (x2 + s * L3 * 0.82, y + W3 * 0.33, z + W3 * 0.33), C.LEG)
    c(p + "c", p, (x2 + s * L3 * 0.78, y - W3 * 0.16, z - W3 * 0.16), (x2 + s * L3, y + W3 * 0.16, z + W3 * 0.16), C.LEG_HI)


# ================================================================== model
P1_LEGS = {  # i: (root, (L1, L2, L3), (W1, W2, W3), (ry, rz1, rz2, rz3))
    0: ((0.7, 23.6, 1.7), (8.5, 10, 4), (1.05, 0.8, 0.6), (20, 50, 105, 20)),
    1: ((0.9, 21.6, 1.8), (7.5, 9, 3.5), (1.0, 0.75, 0.55), (-15, 22, 95, 15)),
}
P2_LEGS = {
    0: ((1.0, 24.4, 2.0), (20, 18, 9), (1.5, 1.1, 0.75), (22, 56, 104, 18)),
    1: ((1.2, 23.0, 2.3), (16, 17, 8), (1.4, 1.0, 0.7), (6, 34, 100, 14)),
    2: ((1.3, 21.6, 2.6), (14, 16, 8), (1.35, 1.0, 0.7), (-12, 14, 92, 10)),
    3: ((1.2, 20.2, 2.9), (13, 15, 8), (1.3, 0.95, 0.7), (-32, 0, 82, 10)),
}


def build(B):
    C, boss = B.C, B.boss
    g, c, blade, lock = B.g, B.c, B.blade, B.lock
    st = B.strands(C.HAIR, C.HAIR_HI, C.HAIR_D, ink=C.HAIR_D)
    st_plain = B.strands(C.HAIR, C.HAIR_HI, C.HAIR_D)
    cp = B.folds(C.COAT, C.COAT_D, C.COAT_HI, 2)
    cedge = B.edges(C.COAT_S)

    # ---------------- skeleton
    g("root", (0, 0, 0))
    g("body", (0, 13.6, 0), "root")
    g("chest", (0, 17.4, 0), "body")
    g("coat_b", (0, 17.4, 1.5), "chest")
    g("coat_r", (1.9, 17.4, -1.0), "chest")
    g("coat_l", (-1.9, 17.4, -1.0), "chest")
    g("pendant", (0, 24.6, -1.45), "chest")
    g("head", (0, 26.2, 0), "chest")
    g("hair_b", (0, 30.6, 2.0), "head")
    g("hair_r", (2.5, 30.6, 0), "head")
    g("hair_l", (-2.5, 30.6, 0), "head")
    g("bangs", (0, 32.0, -2.6), "head")
    g("ah0", (0.0, 32.9, 0.3), "head", rot=(-14, 0, 8))
    g("ah1", (0.0, 35.6, 0.3), "ah0", rot=(0, 0, 34))
    g("ah2", (0.0, 38.0, 0.3), "ah1", rot=(0, 0, 50))
    g("ah3", (0.0, 40.0, 0.3), "ah2", rot=(0, 0, 62))
    g("back", (0, 22.4, 1.5), "chest")
    g("arm_r", (3.2, 25.0, 0), "chest", rot=(0, 0, 5)); g("fore_r", (3.2, 20.0, 0), "arm_r", rot=(6, 0, 0)); g("hand_r", (3.2, 15.2, 0), "fore_r")
    g("arm_l", (-3.2, 25.0, 0), "chest", rot=(0, 0, -5)); g("fore_l", (-3.2, 20.0, 0), "arm_l", rot=(6, 0, 0)); g("hand_l", (-3.2, 15.2, 0), "fore_l")
    for s, k in ((1, "r"), (-1, "l")):
        g("leg_" + k, (1.05 * s, 13.6, 0), "root", rot=(0, 0, s * 1.5))
        g("shin_" + k, (1.05 * s, 7.4, 0), "leg_" + k)
        g("foot_" + k, (1.05 * s, 1.6, 0), "shin_" + k)

    # ---------------- legs: black trousers with white piping, black shoes
    for s, k in ((1, "r"), (-1, "l")):
        x = 1.05 * s
        pipe = lambda F, s=s: F.rect(F.w // 2, 0, 1, F.h, C.PIPE)
        c("thigh_" + k, "leg_" + k, (x - 1.0, 7.2, -1.0), (x + 1.0, 14.0, 1.0), C.PANTS, color2=C.PANTS_D, grad=True,
          faces={"north": B.edges(C.PANTS_HI), ("east" if s > 0 else "west"): pipe})
        c("calf_" + k, "shin_" + k, (x - 0.95, 1.4, -0.95), (x + 0.95, 7.6, 0.95), C.PANTS, color2=C.PANTS_D, grad=True,
          faces={"north": B.edges(C.PANTS_HI), ("east" if s > 0 else "west"): pipe})
        c("hem_" + k, "shin_" + k, (x - 1.05, 1.3, -1.05), (x + 1.05, 2.0, 1.05), C.PANTS_D)
        c("shoe_" + k, "foot_" + k, (x - 0.95, 0, -1.3), (x + 0.95, 1.5, 1.1), C.SHOE, faces={"up": lambda F: F.rect(0, 0, F.w, F.h, C.SHOE_HI)})
        c("toe_" + k, "foot_" + k, (x - 0.85, 0, -2.4), (x + 0.85, 1.1, -1.2), C.SHOE, faces={"up": B.edges(C.SHOE_HI)})
        c("sole_" + k, "foot_" + k, (x - 1.0, 0, -2.5), (x + 1.0, 0.25, 1.15), C.SHOE_HI)

    # ---------------- hips / belt
    c("hips", "body", (-2.1, 12.8, -1.25), (2.1, 17.6, 1.25), C.PANTS, color2=C.PANTS_D, grad=True)
    c("belt", "body", (-2.15, 16.6, -1.32), (2.15, 17.4, 1.32), C.CORD, faces=B.all(lambda F: F.rect(0, 0, F.w, 1, C.PANTS_HI)))
    c("buckle", "body", (-0.5, 16.5, -1.42), (0.5, 17.5, -1.3), C.PIPE)

    # ---------------- torso: shirt + cord + pendant
    c("shirt", "chest", (-2.0, 17.2, -1.2), (2.0, 25.0, 1.2), C.SHIRT, faces={"north": shirt_front(B, C), "south": B.folds(C.SHIRT, C.SHIRT_D, C.SHIRT_HI, 2)})
    c("bust", "chest", (-1.8, 21.4, -1.45), (1.8, 23.2, -1.15), C.SHIRT, faces={"north": shirt_front(B, C)})
    c("neck", "chest", (-0.75, 24.6, -0.7), (0.75, 26.8, 0.7), C.SKIN_D)
    c("pend_plate", "pendant", (-0.85, 21.4, -1.68), (0.85, 23.0, -1.5), C.TOX, faces={"north": pendant_paint(C, boss)})
    c("pend_ring", "pendant", (-0.15, 22.9, -1.7), (0.15, 23.3, -1.5), C.CORD)

    # ---------------- lab coat (upper)
    c("coat_sh", "chest", (-3.0, 24.0, -1.65), (3.0, 25.7, 1.65), C.COAT, faces={"up": lambda F: F.rect(0, 0, F.w, F.h, C.COAT_HI), "north": cedge})
    c("coat_bu", "chest", (-2.95, 17.0, 1.2), (2.95, 25.7, 1.7), C.COAT, faces={"south": combo(cp, lambda F: F.rect(F.w // 2, 0, 1, F.h, C.COAT_D))})
    c("coat_collar", "chest", (-2.0, 25.2, 0.4), (2.0, 27.2, 1.9), C.COAT, origin=(0, 25.4, 1.2), rot=(-14, 0, 0), faces={"north": B.frame(C.COAT_S)})
    for s, k in ((1, "r"), (-1, "l")):
        x0, x1 = (0.95, 2.95) if s > 0 else (-2.95, -0.95)
        c("coat_fu_" + k, "chest", (x0, 17.0, -1.7), (x1, 25.4, -1.25), C.COAT, faces={"north": combo(cp, B.edges(C.COAT_S))})
        c("coat_su_" + k, "chest", (2.55 * s, 17.0, -1.55), (2.95 * s, 25.4, 1.55), C.COAT, faces={"east": cp, "west": cp})
        # wide lapels (art: big pointed white collar flaps)
        lx = 1.15 * s
        c("lapel_" + k, "chest", (lx - 0.6, 21.0, -1.95), (lx + 0.6, 25.6, -1.72), C.COAT_HI, origin=(lx, 25.6, -1.85), rot=(0, 0, -16 * s),
          faces={"north": B.frame(C.COAT_S)})
        c("lapelw_" + k, "chest", (lx + 0.3 * s - 0.6, 23.4, -2.0), (lx + 0.3 * s + 0.6, 25.8, -1.75), C.COAT_HI, origin=(lx, 25.8, -1.85), rot=(0, 0, 38 * s),
          faces={"north": B.frame(C.COAT_S)})
        c("bpocket_" + k, "chest", (1.4 * s - 0.6, 21.2, -1.78), (1.4 * s + 0.6, 22.2, -1.68), C.COAT_D) if s < 0 else None
        # lower coat panels (own bones -> flutter), flared open
        bx = "coat_" + k
        fx0, fx1 = (0.75, 3.1) if s > 0 else (-3.1, -0.75)
        ylow = 3.0 if boss else 8.4
        org = (1.9 * s, 17.4, -1.0)
        c("coat_fl_" + k, bx, (fx0, ylow, -1.85), (fx1, 17.5, -1.4), C.COAT, origin=org, rot=(4, 0, 6 * s),
          faces={"north": combo(cp, B.edges(C.COAT_S), lambda F: F.rect(0, F.h - 1, F.w, 1, C.COAT_S))})
        c("coat_sl_" + k, bx, (2.7 * s, ylow, -1.6), (3.1 * s, 17.5, 1.6), C.COAT, origin=org, rot=(4, 0, 6 * s), faces={"east": cp, "west": cp})
        c("pocket_" + k, bx, (1.3 * s, 11.0 if not boss else 12.0, -1.95), (2.7 * s, 12.6 if not boss else 13.6, -1.82), C.COAT_HI, origin=org, rot=(4, 0, 6 * s),
          faces={"north": B.frame(C.COAT_S)})
        if s > 0:  # test tube + pen sticking out of the right pocket
            c("tube", bx, (1.6, 12.2, -1.9), (2.0, 14.4, -1.6), C.GLASS, origin=org, rot=(4, 0, 6), faces={"north": lambda F: F.rect(0, F.h // 3, F.w, F.h, C.TOX, glow=True)})
            c("pen", bx, (2.2, 12.2, -1.9), (2.4, 14.0, -1.7), C.TOX_D, origin=org, rot=(4, 0, 6))
        if boss:  # shredded hem -> long spikes down to the floor (art: jagged skirt silhouette)
            for j in range(4):
                lock(f"crag_{k}{j}", bx, (s * (0.9 + j * 0.6), ylow + 0.3, -1.6 + j * 0.25), 2.4 + (j % 2) * 1.2, 0.8, 0.3,
                     (8, 0, s * (6 + j * 7)), C.COAT, C.COAT_HI)
    c("coat_bl", "coat_b", (-3.15, 3.0 if boss else 8.4, 1.3), (3.15, 17.5, 1.8), C.COAT, origin=(0, 17.4, 1.5), rot=(-5, 0, 0),
      faces={"south": combo(cp, lambda F: F.rect(F.w // 2, 0, 1, F.h, C.COAT_S)), "north": lambda F: F.rect(0, 0, F.w, F.h, C.COAT_D)})
    c("coat_belt", "coat_b", (-1.6, 14.6, 1.75), (1.6, 15.3, 1.95), C.COAT_D, origin=(0, 17.4, 1.5), rot=(-5, 0, 0))
    if boss:
        for j in range(6):
            lock(f"crag_b{j}", "coat_b", (-2.6 + j * 1.05, 3.3, 1.6), 2.2 + (j % 3) * 0.9, 0.9, 0.3, (-8, 0, (j - 2.5) * 7), C.COAT, C.COAT_HI)

    # ---------------- arms: white sleeves, green-striped cuffs
    for s, k in ((1, "r"), (-1, "l")):
        x = 3.2 * s
        c("sleeve_" + k, "arm_" + k, (x - 0.9, 19.8, -0.95), (x + 0.9, 25.5, 0.95), C.COAT, faces={"north": cp, "south": cp, "east": cedge, "west": cedge})
        c("shpad_" + k, "arm_" + k, (x - 1.0, 23.8, -1.05), (x + 1.0, 25.8, 1.05), C.COAT, faces={"up": lambda F: F.rect(0, 0, F.w, F.h, C.COAT_HI)})
        c("fsleeve_" + k, "fore_" + k, (x - 0.88, 15.8, -0.9), (x + 0.88, 20.2, 0.9), C.COAT, faces={"north": B.folds(C.COAT, C.COAT_D, C.COAT_HI, 1)})
        c("cuff_" + k, "fore_" + k, (x - 1.0, 14.9, -1.02), (x + 1.0, 16.2, 1.02), C.COAT_HI,
          faces=B.all(lambda F: F.rect(0, F.h // 2 - 1, F.w, max(1, F.h // 4), C.TOX, glow=not boss), skip=("up", "down")))
        if not boss:
            c("hand_" + k, "hand_" + k, (x - 0.55, 12.9, -0.55), (x + 0.55, 15.0, 0.55), C.SKIN, color2=C.SKIN_D, grad=True)
            c("thumb_" + k, "hand_" + k, (x - 0.25 - 0.4 * s, 13.4, -0.85), (x + 0.25 - 0.4 * s, 14.5, -0.45), C.SKIN_D)
        else:  # black clawed hands
            c("palm_" + k, "hand_" + k, (x - 0.7, 13.0, -0.6), (x + 0.7, 15.0, 0.6), C.SKIN, color2=C.SKIN_L, grad=True)
            for j in range(4):
                lock(f"fclw_{k}{j}", "hand_" + k, (x - 0.5 + j * 0.33, 13.1, -0.3 + abs(j - 1.5) * 0.15), 2.4, 0.3, 0.3, (-14, 0, (j - 1.5) * 8),
                     C.SKIN_L, C.TOX)
        # props: flask (right) / web glob (left), web line out of the left palm (along local -Y, scaled to extend)
        if s > 0 and not boss:
            g("flask", (x, 13.6, -0.2), "hand_r")
            c("fl_body", "flask", (x - 0.75, 11.4, -0.95), (x + 0.75, 13.2, 0.55), C.GLASS, faces=B.all(lambda F: F.rect(0, F.h // 3, F.w, F.h, C.TOX, glow=True)))
            c("fl_neck", "flask", (x - 0.3, 13.1, -0.5), (x + 0.3, 14.4, 0.1), C.GLASS)
            c("fl_cork", "flask", (x - 0.36, 14.3, -0.56), (x + 0.36, 14.8, 0.16), C.SHOE_HI)
        if s < 0 and not boss:
            g("webline", (x, 13.0, 0), "hand_l")
            c("web_core", "webline", (x - 0.2, -27.0, -0.2), (x + 0.2, 13.0, 0.2), C.WEB, glow=False)
            for j in range(5):
                yy = 13.0 - 7.0 * (j + 0.5)
                c(f"web_knot{j}", "webline", (x - 0.35, yy - 0.3, -0.35), (x + 0.35, yy + 0.3, 0.35), C.WEB)
            c("web_glob", "webline", (x - 1.0, -28.5, -1.0), (x + 1.0, -26.5, 1.0), C.WEB, faces=B.all(B.frame(C.GLASS_D)))

    # ---------------- head
    c("skull", "head", (-2.6, 26.6, -2.5), (2.6, 31.8, 2.5), C.SKIN, faces={"north": face_p2(C) if boss else face_p1(C)})
    c("jaw", "head", (-1.7, 26.3, -2.35), (1.7, 26.9, 0.8), C.SKIN_D)
    for s, k in ((1, "r"), (-1, "l")):
        c("ear_" + k, "head", (2.5 * s - 0.2, 28.4, -0.4), (2.5 * s + 0.2, 30.2, 0.6), C.SKIN_D)
    # hair mass: messy bob, strands flaring out at the jaw
    c("hair_cap", "head", (-2.9, 30.0, -2.8), (2.9, 33.4, 2.9), C.HAIR, faces=B.all(st))
    c("hair_top", "head", (-2.5, 33.2, -2.3), (2.5, 34.0, 2.5), C.HAIR, faces=B.all(st_plain))
    for j, (x, z, rz, rx) in enumerate([(-1.4, -1.2, 30, -20), (1.2, -0.8, -26, -16), (0.0, 1.6, 6, 30), (-1.8, 1.2, 40, 24), (1.8, 1.4, -38, 26)]):
        blade(f"tuft{j}", "head", (x, 33.6, z), 1.6, 1.4, 0.8, (rx, 0, rz), C.HAIR, C.HAIR_HI, paint=st_plain)
    c("hair_back", "hair_b", (-3.0, 26.4, 1.6), (3.0, 31.2, 3.2), C.HAIR, faces=B.all(st))
    for j, (x, ln, rz) in enumerate([(-2.3, 3.0, 162), (-1.0, 3.8, 174), (0.4, 3.4, 184), (1.7, 3.6, 192), (2.6, 2.6, 204)]):
        blade(f"hb{j}", "hair_b", (x, 27.2, 2.6), ln, 1.6, 0.8, (-14, 0, rz), C.HAIR, C.HAIR_D, paint=st_plain)
    for s, k in ((1, "r"), (-1, "l")):
        c("side_" + k, "hair_" + k, (2.4 * s, 26.8, -2.3), (3.3 * s, 31.2, 2.4), C.HAIR, faces=B.all(st))
        for j, (y, z, ln, rz) in enumerate([(31.0, -1.2, 2.4, 100), (30.0, 0.6, 3.2, 122), (28.8, -1.6, 3.0, 140), (27.8, 1.0, 3.0, 150),
                                            (27.2, -0.6, 2.6, 162), (29.4, 2.0, 2.4, 110)]):
            blade(f"hs_{k}{j}", "hair_" + k, (3.0 * s, y, z), ln, 1.5, 0.8, (0, 0, -rz * s), C.HAIR, C.HAIR_D, paint=st_plain)
    # bangs: choppy, parted, long lock between the eyes
    c("fringe", "bangs", (-2.9, 31.0, -2.95), (2.9, 32.6, -2.5), C.HAIR, faces=B.all(st))
    for j, (x, ln, rz) in enumerate([(-2.4, 2.2, 10), (-1.3, 1.7, -8), (-0.2, 2.6, 4), (1.0, 1.9, -12), (2.2, 2.3, -6)]):
        lock(f"bang{j}", "bangs", (x, 31.3, -2.85), ln, 1.4, 0.4, (8, 0, rz), C.HAIR, C.HAIR_D, paint=st_plain)
    # ahoge: thick curling loop (arches up and curls over to her left)
    c("ahs0", "ah0", (-0.35, 32.9, 0.0), (0.35, 35.8, 0.6), C.HAIR, faces=B.all(st_plain))
    c("ahs1", "ah1", (-0.3, 35.6, 0.05), (0.3, 38.2, 0.55), C.HAIR, faces=B.all(st_plain))
    c("ahs2", "ah2", (-0.25, 38.0, 0.1), (0.25, 40.2, 0.5), C.HAIR, faces=B.all(st_plain))
    c("ahs3", "ah3", (-0.2, 40.0, 0.12), (0.2, 41.8, 0.48), C.HAIR_D)

    # ---------------- spider legs (phase 1: 4 thin legs = hidden prop "back"; boss: 8 huge legs + abdomen, always out)
    legs = P2_LEGS if boss else P1_LEGS
    for s, k in ((1, "r"), (-1, "l")):
        for i, (root, L, W, rest) in legs.items():
            spider_leg(B, k, s, i, (root[0] * s, root[1], root[2]), L, W, rest)
    c("back_node", "back", (-0.8, 20.8, 1.5), (0.8, 24.4, 2.2), C.LEG, faces={"south": B.frame(C.LEG_HI)})
    if boss:
        # cephalothorax plate on her back + bulbous abdomen with red hourglass
        c("ceph", "back", (-2.6, 18.6, 1.6), (2.6, 25.6, 3.6), C.LEG, faces=B.all(B.frame(C.LEG_HI)))
        g("abdomen", (0, 20.0, 3.4), "back", rot=(-18, 0, 0))

        def hourglass(F):
            W, H = F.w, F.h
            for y in range(H):
                for x in range(W):
                    F.px(x, y, mix(C.ABD, C.ABD_D, y / H))
            for j in range(6):  # red veins
                x0 = B.R.randint(0, W)
                F.line(x0, 0, x0 + B.R.randint(-W // 4, W // 4), H, C.RED_D, 1)
            F.poly([(W * 0.3, H * 0.15), (W * 0.7, H * 0.15), (W * 0.53, H * 0.5), (W * 0.7, H * 0.85), (W * 0.3, H * 0.85), (W * 0.47, H * 0.5)], C.RED, glow=True)

        def veins(F):
            W, H = F.w, F.h
            for y in range(H):
                for x in range(W):
                    F.px(x, y, mix(C.ABD, C.ABD_D, y / H))
            for j in range(4):
                x0 = B.R.randint(1, max(2, W - 1))
                F.line(x0, 0, x0 + B.R.randint(-3, 3), H, C.RED_D, 1)
            x0 = W // 2
            F.line(x0, H * 0.2, x0, H * 0.8, C.RED, 1, glow=True)
        c("abd_core", "abdomen", (-4.4, 14.0, 3.6), (4.4, 24.0, 12.4), C.ABD, faces={"south": hourglass, "east": veins, "west": veins, "up": veins, "north": veins, "down": veins})
        c("abd_mid", "abdomen", (-5.2, 15.2, 4.6), (5.2, 22.8, 11.4), C.ABD, faces=B.all(veins))
        c("abd_top", "abdomen", (-3.4, 12.8, 5.0), (3.4, 25.0, 11.0), C.ABD, faces=B.all(veins))
        c("abd_end", "abdomen", (-3.0, 15.6, 12.2), (3.0, 22.4, 14.0), C.ABD_D, faces={"south": hourglass})
        c("spinneret", "abdomen", (-0.8, 17.4, 13.8), (0.8, 19.0, 15.0), C.RED_D, faces={"south": lambda F: F.rect(1, 1, F.w - 2, F.h - 2, C.RED, glow=True)})
        for j in range(6):  # bristly spines along the abdomen ridge
            blade(f"abd_sp{j}", "abdomen", ((j % 2 - 0.5) * 2.4, 24.6, 5.0 + j * 1.2), 1.8, 0.5, 0.5, (30, 0, (j % 2 - 0.5) * 30), C.LEG, C.LEG_HI)
        # fangs (chelicerae) under the chin - glow red tips
        for s, k in ((1, "r"), (-1, "l")):
            lock("fang_" + k, "head", (0.8 * s, 26.6, -2.0), 1.8, 0.5, 0.5, (16, 0, -s * 14), C.LEG, C.RED)


# ================================================================== animation framework
class A:
    def __init__(self, B, name, ticks, props, loop=False):
        self.B, self.name, self.ticks, self.loop, self.tr = B, name, ticks, loop, {}
        self.props = props

    def k(self, bone, ch, keys):
        self.tr.setdefault(bone, {}).setdefault(ch, []).extend(keys)
        return self

    def rot(self, bone, *keys): return self.k(bone, "rotation", keys)
    def pos(self, bone, *keys): return self.k(bone, "position", [(t, x * self.B.K, y * self.B.K, z * self.B.K) for (t, x, y, z) in keys])
    def scl(self, bone, *keys): return self.k(bone, "scale", keys)

    def at(self, t, **bones):
        """pose snapshot: bone=(rx,ry,rz) rotation DELTA keys; key 'P_<bone>' = position"""
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
            seen.add(tt); out.append((tt, x * gain, y * gain, z * gain))
        return self.rot(bone, *out)

    def hair(self, keys, delay=2):
        """x = forward(+)/back flick, z = sideways"""
        self.drape("hair_b", [(t, -x * 0.8, 0, z * 0.5) for (t, x, y, z) in keys], delay)
        self.drape("hair_r", [(t, x * 0.4, 0, z * 0.6 + abs(x) * 0.2) for (t, x, y, z) in keys], delay)
        self.drape("hair_l", [(t, x * 0.4, 0, z * 0.6 - abs(x) * 0.2) for (t, x, y, z) in keys], delay)
        self.drape("bangs", [(t, x * 0.3, 0, z * 0.3) for (t, x, y, z) in keys], delay)
        self.drape("ah0", [(t, -x * 0.5, 0, z * 0.5) for (t, x, y, z) in keys], delay + 1)
        self.drape("ah1", [(t, -x * 0.6, 0, z * 0.5) for (t, x, y, z) in keys], delay + 2)
        self.drape("ah2", [(t, -x * 0.7, 0, z * 0.6) for (t, x, y, z) in keys], delay + 4)
        self.drape("ah3", [(t, -x * 0.9, 0, z * 0.7) for (t, x, y, z) in keys], delay + 5)
        self.drape("pendant", [(t, x * 0.6, 0, z * 0.6) for (t, x, y, z) in keys], delay)
        return self

    def cloth(self, keys, delay=2):
        """x>0 = hem kicks forward, z>0 = flare toward +X, w = flare both sides out"""
        k4 = [(q + (0,))[:5] if len(q) == 4 else q for q in keys]
        self.drape("coat_b", [(t, x - w * 0.8, 0, z * 0.4) for (t, x, y, z, w) in k4], delay)
        self.drape("coat_r", [(t, x * 0.8 + w * 0.2, 0, z + w) for (t, x, y, z, w) in k4], delay)
        self.drape("coat_l", [(t, x * 0.8 + w * 0.2, 0, z - w) for (t, x, y, z, w) in k4], delay)
        return self

    def legs(self, keys_leg, keys_shin, keys_foot=None):
        for s, k in ((1, "r"), (-1, "l")):
            self.rot("leg_" + k, *[(t, x, y * s, z * s) for (t, x, y, z) in keys_leg])
            self.rot("shin_" + k, *keys_shin)
            if keys_foot: self.rot("foot_" + k, *keys_foot)
        return self

    def SL(self, i, t, f=(0, 0, 0), tb=0, tp=0, side="rl", lag=0.0):
        """spider leg i, mirrored: f=(twist, forward, up) femur delta, tb/tp = knee/tip straighten"""
        if self.B.boss and i == 0 and f[2] > 0:  # top legs already rest steep: raising them fully would cross overhead
            f = (f[0], f[1], f[2] * 0.45)
        for k in side:
            s = 1 if k == "r" else -1
            self.rot(f"lf_{k}{i}", (t, f[0], s * f[1], s * f[2]))
            self.rot(f"lt_{k}{i}", (min(self.ticks, t + lag), 0, 0, s * tb))
            self.rot(f"lp_{k}{i}", (min(self.ticks, t + lag * 2), 0, 0, s * tp))
        return self

    def done(self, base_layer=False):
        if not base_layer:
            for p in self.props:
                if p not in self.tr or "scale" not in self.tr[p]:
                    self.scl(p, (0, *HIDE))
        end = self.ticks
        for b, chs in self.tr.items():
            for ch, ks in chs.items():
                if ch == "scale": continue
                ts = [q[0] for q in ks]
                if 0 not in ts and min(ts) > 0: ks.append((0, 0, 0, 0))
                if max(ts) < end: ks.append((end, *((0, 0, 0) if not self.loop else sorted(ks)[0][1:])))
        tracks = {}
        for b, chs in self.tr.items():
            tracks[b] = {}
            for ch, v in chs.items():
                d = {}
                for q in v: d[round(q[0], 3)] = q  # last key at a time wins
                tracks[b][ch] = sorted([(t / 20.0, x, y, z) for (t, x, y, z) in d.values()], key=lambda q: q[0])
        self.B.m.anim(self.name, self.ticks / 20.0, tracks, loop=self.loop)


Z = (0, 0, 0)


PROPS1 = ("back", "flask", "webline")


def legs4(a, t, f0=Z, tb0=0, f1=Z, tb1=0, tp=0, side="rl", lag=1.0):
    """both phase-1 spider leg pairs at once"""
    a.SL(0, t, f0, tb0, tp, side, lag)
    a.SL(1, t, f1, tb1, tp, side, lag)


def web(a, t0, t_full, t_hold, t_gone):
    """web line out of the left palm: shoots out (scale Y) and snaps back"""
    a.scl("webline", (0, *HIDE), (t0 - 0.01, *HIDE), (t0, 1, 0.05, 1), (t_full, 1, 1.1, 1), (t_full + 1, 1, 1, 1), (t_hold, 1, 1, 1),
          (t_gone - 0.01, 1, 0.05, 1), (t_gone, *HIDE), (a.ticks, *HIDE))


def anims_p1(B):
    def mk(name, ticks, loop=False):
        return A(B, name, ticks, PROPS1, loop)

    # ---------------------------------------------------------------- idle (80): slouched, bored breathing, head tilts, ahoge bobs, fingers fidget
    a = mk("idle", 80, loop=True)
    a.at(0, chest=Z, head=(0, 0, -3), P_body=Z, body=(0, 0, 1))
    a.at(20, chest=(1.6, 0, 0), head=(3, 4, -6), P_body=(0, -0.08, 0))
    a.at(40, chest=Z, head=(0, 0, -2), P_body=Z, body=(0, 0, 1.6))
    a.at(55, head=(-2, -6, 4)).at(60, chest=(1.6, 0, 0), P_body=(0, -0.08, 0))
    a.at(80, chest=Z, head=(0, 0, -3), P_body=Z, body=(0, 0, 1))
    a.at(0, arm_r=Z, arm_l=Z, fore_r=Z, fore_l=Z)
    a.at(40, arm_r=(3, 0, 2), arm_l=(3, 0, -2), fore_r=(6, 0, 0), fore_l=(4, 0, 0))
    a.at(62, fore_l=(14, 0, 0)).at(66, fore_l=(6, 0, 0))
    a.at(80, arm_r=Z, arm_l=Z, fore_r=Z, fore_l=Z)
    a.at(0, leg_l=(-2, 0, -1), leg_r=(1, 0, 1)).at(40, leg_l=(-3, 0, -1.5), leg_r=(2, 0, 1.5)).at(80, leg_l=(-2, 0, -1), leg_r=(1, 0, 1))
    a.hair([(0, 0, 0, 1), (20, 3, 0, -2), (40, 0, 0, 2), (60, 3, 0, -2), (80, 0, 0, 1)], delay=5)
    a.cloth([(0, 0, 0, 0.5), (20, 1, 0, -0.5), (40, 0, 0, 0.5), (60, 1, 0, -0.5), (80, 0, 0, 0.5)], delay=5)
    a.done()

    # ---------------------------------------------------------------- walk (20, additive): brisk lab-walk, coat flapping behind
    a = mk("walk", 20, loop=True)
    a.rot("leg_r", (0, 26, 0, 0), (5, 0, 0, 0), (10, -24, 0, 0), (15, 0, 0, 0), (20, 26, 0, 0))
    a.rot("shin_r", (0, -4, 0, 0), (5, -6, 0, 0), (10, -10, 0, 0), (13, -46, 0, 0), (17, -22, 0, 0), (20, -4, 0, 0))
    a.rot("foot_r", (0, -12, 0, 0), (10, 12, 0, 0), (20, -12, 0, 0))
    a.rot("leg_l", (0, -24, 0, 0), (5, 0, 0, 0), (10, 26, 0, 0), (15, 0, 0, 0), (20, -24, 0, 0))
    a.rot("shin_l", (0, -10, 0, 0), (3, -46, 0, 0), (7, -22, 0, 0), (10, -4, 0, 0), (15, -6, 0, 0), (20, -10, 0, 0))
    a.rot("foot_l", (0, 12, 0, 0), (10, -12, 0, 0), (20, 12, 0, 0))
    a.pos("body", (0, 0, -0.4, 0), (5, 0, 0.25, 0), (10, 0, -0.4, 0), (15, 0, 0.25, 0), (20, 0, -0.4, 0))
    a.rot("body", (0, -3, 5, 0), (10, -3, -5, 0), (20, -3, 5, 0))
    a.rot("chest", (0, -2, -6, 0), (10, -2, 6, 0), (20, -2, -6, 0))
    a.rot("arm_r", (0, -16, 0, 0), (10, 18, 0, 0), (20, -16, 0, 0))
    a.rot("arm_l", (0, 18, 0, 0), (10, -16, 0, 0), (20, 18, 0, 0))
    a.rot("fore_r", (0, 0, 0, 0), (10, 14, 0, 0), (20, 0, 0, 0))
    a.rot("fore_l", (0, 14, 0, 0), (10, 0, 0, 0), (20, 14, 0, 0))
    a.hair([(0, -4, 0, 2), (5, -6, 0, 0), (10, -4, 0, -2), (15, -6, 0, 0), (20, -4, 0, 2)], delay=2)
    a.cloth([(0, -8, 0, 3), (5, -11, 0, 0), (10, -8, 0, -3), (15, -11, 0, 0), (20, -8, 0, 3)], delay=1)
    a.done(base_layer=True)

    # ---------------------------------------------------------------- leg_lance (36): legs burst 3-6, R pair LANCES 12, L pair LANCES 22, fold 30
    a = mk("leg_lance", 36).show("back", 3, 33, grow=3)
    legs4(a, 3, (0, 0, -30), -40, (0, 0, -20), -30)
    legs4(a, 7, (0, -10, 15), -10, (0, -10, 10), -10)
    a.at(0, chest=Z, head=Z, arm_r=Z, arm_l=Z, P_body=Z)
    a.at(5, chest=(-14, 0, 0), head=(12, 0, 0), arm_r=(14, 0, 18), arm_l=(14, 0, -18), fore_r=(30, 0, 0), fore_l=(30, 0, 0), P_body=(0, -0.6, 0.3))
    a.at(9, chest=(-8, -22, 0), head=(4, 16, 0), arm_r=(-20, 0, 20), arm_l=(30, 0, -14), P_body=(0, -0.8, 0.6))
    a.SL(0, 9, (0, -40, 30), -20, 0, "r").SL(1, 9, (0, -40, 20), -20, 0, "r")
    a.at(12, chest=(-12, 24, 0), head=(2, -16, 0), arm_r=(84, 0, 8), fore_r=(-6, 0, 0), arm_l=(-14, 0, -20), P_body=(0, -0.6, -1.4))
    a.SL(0, 12, (40, 80, -30), 95, 20, "r").SL(1, 12, (40, 85, -10), 85, 15, "r")
    a.SL(0, 16, (20, 40, 0), 30, 0, "r").SL(1, 16, (20, 40, 0), 30, 0, "r")
    a.SL(0, 18, (0, -40, 30), -20, 0, "l").SL(1, 18, (0, -40, 20), -20, 0, "l")
    a.at(18, chest=(-8, -16, 0), arm_r=(20, 0, 14), arm_l=(-30, 0, -24), head=(4, 10, 0), P_body=(0, -0.7, -0.6))
    a.at(22, chest=(-12, -26, 0), head=(2, 16, 0), arm_l=(86, 0, -8), fore_l=(-6, 0, 0), arm_r=(-14, 0, 20), P_body=(0, -0.6, -2.2))
    a.SL(0, 22, (40, 80, -30), 95, 20, "l").SL(1, 22, (40, 85, -10), 85, 15, "l")
    a.SL(0, 26, (20, 40, 0), 30, 0, "l").SL(1, 26, (20, 40, 0), 30, 0, "l")
    legs4(a, 30, (0, 0, 20), -20, (0, 0, 10), -20)
    legs4(a, 34, (0, 0, -40), -60, (0, 0, -30), -50)
    a.at(30, chest=(-2, -4, 0), arm_l=(10, 0, -8), arm_r=(6, 0, 8), fore_l=(14, 0, 0), fore_r=(12, 0, 0), head=(0, 0, -2), P_body=(0, -0.2, -1.6))
    a.at(36, chest=Z, P_body=Z, head=Z, arm_l=Z, arm_r=Z, fore_l=Z, fore_r=Z)
    a.legs([(0, 0, 0, 0), (5, -6, 0, 0), (12, 0, 0, 0), (36, 0, 0, 0)], [(0, 0, 0, 0), (5, -14, 0, 0), (12, -8, 0, 0), (30, -4, 0, 0), (36, 0, 0, 0)])
    a.at(12, leg_r=(-26, 0, 2), leg_l=(18, 0, -2)).at(22, leg_l=(-26, 0, -2), leg_r=(18, 0, 2))
    a.hair([(0, 0, 0, 0), (5, 8, 0, 0), (12, -10, 0, 8), (18, 4, 0, -2), (22, -10, 0, -8), (30, 2, 0, 0), (36, 0, 0, 0)])
    a.cloth([(0, 0, 0, 0), (5, 2, 0, 0, 4), (12, -8, 0, 5), (22, -8, 0, -5), (30, -2, 0, 0), (36, 0, 0, 0)])
    a.done()

    # ---------------------------------------------------------------- coat_whirl (32): coil 2-9 with legs flattened, SPIN 10-18 (hit 15), wobble, fold
    a = mk("coat_whirl", 32).show("back", 2, 29, grow=2)
    legs4(a, 4, (0, 20, 10), -10, (0, 10, 5), -10)
    for t in (10, 18):
        legs4(a, t, (0, 0, -50), 95, (0, 0, -22), 90, tp=15, lag=0)
    a.scl("back", (0, *HIDE), (1.99, *HIDE), (4, 1, 1, 1), (9, 1, 1, 1), (12, 1.25, 1, 1.25), (18, 1.25, 1, 1.25), (22, 1, 1, 1), (27, 1, 1, 1), (29, *HIDE), (32, *HIDE))
    legs4(a, 24, (0, -10, 0), -20, (0, -10, 0), -20)
    a.at(0, root=Z, chest=Z, P_root=Z)
    a.at(8, root=(0, -40, 0), chest=(-16, 20, 0), head=(14, -10, 0), arm_r=(30, 0, 70), arm_l=(30, 0, -70), fore_r=(40, 0, 0), fore_l=(40, 0, 0), P_root=(0, -1.2, 0))
    a.at(10, root=(0, -20, 0), chest=(-8, 10, 0), arm_r=(0, 0, 85), arm_l=(0, 0, -85), fore_r=Z, fore_l=Z, P_root=(0, 0.6, 0))
    a.at(13, root=(0, 120, 0), P_root=(0, 1.4, 0))
    a.at(15, root=(0, 200, 0), chest=(-4, 0, 0), head=(-6, 0, 0), P_root=(0, 1.6, 0))
    a.at(18, root=(0, 320, 0), P_root=(0, 0.6, 0), arm_r=(10, 0, 70), arm_l=(10, 0, -70))
    a.at(21, root=(0, 360, 0), chest=(-10, -8, 0), head=(8, 6, 0), P_root=(0, -0.6, 0), arm_r=(20, 0, 30), arm_l=(20, 0, -30), fore_r=(20, 0, 0), fore_l=(20, 0, 0))
    a.at(26, root=(0, 364, 0), chest=(-3, 0, 0), P_root=Z)
    a.at(32, root=(0, 360, 0), chest=Z, head=Z, arm_r=Z, arm_l=Z, fore_r=Z, fore_l=Z)
    a.legs([(0, 0, 0, 0), (8, -18, 0, 4), (13, 0, 0, 14), (18, 0, 0, 14), (22, -14, 0, 3), (32, 0, 0, 0)],
           [(0, 0, 0, 0), (8, -30, 0, 0), (13, -6, 0, 0), (22, -24, 0, 0), (32, 0, 0, 0)])
    a.hair([(0, 0, 0, 0), (8, 6, 0, 10), (13, -4, 0, -24), (18, -4, 0, -24), (22, 4, 0, 10), (27, 0, 0, -3), (32, 0, 0, 0)])
    a.cloth([(0, 0, 0, 0), (8, 0, 0, 4, 2), (12, -6, 0, -8, 26), (18, -6, 0, -8, 28), (22, 2, 0, 6, 6), (32, 0, 0, 0)])
    a.done()

    # ---------------------------------------------------------------- web_shot (30): draw the palm back 4-10, SHOOT 13 (web line), hold, snap back 20, recover
    a = mk("web_shot", 30)
    web(a, 12, 13.5, 17, 20)
    a.at(0, chest=Z, arm_l=Z, fore_l=Z, head=Z, P_body=Z)
    a.at(5, chest=(4, 18, 0), head=(2, -12, 0), arm_l=(30, 0, -40), fore_l=(90, 0, 0), arm_r=(10, 0, 10), P_body=(0, -0.3, 0.4))
    a.at(10, chest=(8, 30, 0), head=(4, -20, 0), arm_l=(20, 30, -60), fore_l=(110, 0, 0), arm_r=(20, 0, 20), fore_r=(20, 0, 0), P_body=(0, -0.5, 0.8))
    a.at(13, chest=(-10, -24, 0), head=(-2, 18, 0), arm_l=(92, -10, 6), fore_l=(-4, 0, 0), arm_r=(-20, 0, 24), fore_r=(10, 0, 0), P_body=(0, -0.6, -1.0))
    a.at(15, chest=(-12, -26, 0), arm_l=(96, -10, 6), P_body=(0, -0.7, -1.1))
    a.at(18, chest=(-8, -18, 0), arm_l=(86, -6, 4), fore_l=(4, 0, 0))
    a.at(20, chest=(2, -6, 0), arm_l=(60, 0, -10), fore_l=(50, 0, 0), head=(4, 8, 0), P_body=(0, -0.3, -0.4))
    a.at(25, chest=(0, -2, 0), arm_l=(10, 0, -6), fore_l=(20, 0, 0), arm_r=(4, 0, 4), fore_r=(6, 0, 0), head=(0, 2, 0), P_body=Z)
    a.at(30, chest=Z, arm_l=Z, fore_l=Z, arm_r=Z, fore_r=Z, head=Z)
    a.rot("leg_l", (0, 0, 0, 0), (10, 10, 0, -2), (13, -24, 0, -2), (20, -18, 0, -2), (28, 0, 0, 0))
    a.rot("leg_r", (0, 0, 0, 0), (10, -8, 0, 2), (13, 14, 0, 2), (20, 10, 0, 2), (28, 0, 0, 0))
    a.rot("shin_l", (0, 0, 0, 0), (13, -8, 0, 0), (28, 0, 0, 0)).rot("shin_r", (0, 0, 0, 0), (13, -16, 0, 0), (28, 0, 0, 0))
    a.hair([(0, 0, 0, 0), (10, 6, 0, 4), (13, -12, 0, -6), (18, -4, 0, 0), (24, 2, 0, 0), (30, 0, 0, 0)])
    a.cloth([(0, 0, 0, 0), (10, 4, 0, 2), (13, -8, 0, -4), (20, -2, 0, 0), (30, 0, 0, 0)])
    a.done()

    # ---------------------------------------------------------------- toxic_flask (60): pull flask from the coat 0-6, wind up 10, LOB 14, follow-through, smug watch, push hair
    a = mk("toxic_flask", 60).show("flask", 5, 14.2, grow=1)
    a.at(0, chest=Z, arm_r=Z, fore_r=Z, head=Z, P_body=Z)
    a.at(5, chest=(-4, 10, 0), head=(-8, -6, 0), arm_r=(30, 30, -40), fore_r=(90, 0, 0), P_body=(0, -0.2, 0))
    a.at(10, chest=(12, -28, 0), head=(4, 22, 0), arm_r=(190, 0, 22), fore_r=(40, 0, 0), arm_l=(60, 0, -20), fore_l=(20, 0, 0), P_body=(0, -0.4, 0.8))
    a.at(14, chest=(-16, 22, 0), head=(-2, -14, 0), arm_r=(70, 0, -6), fore_r=(0, 0, 0), arm_l=(-20, 0, -20), fore_l=(10, 0, 0), P_body=(0, -0.8, -1.0))
    a.at(18, chest=(-20, 30, 0), arm_r=(30, 0, -20), head=(0, -18, 0), P_body=(0, -1.0, -1.2))
    a.at(24, chest=(-6, 10, 0), arm_r=(10, 0, 4), fore_r=(20, 0, 0), arm_l=(0, 0, -6), head=(4, -6, 4), P_body=(0, -0.4, -0.6))
    a.at(32, chest=(2, 0, 0), head=(6, 0, 10), arm_r=(4, 0, 2), fore_r=(10, 0, 0), arm_l=Z, P_body=(0, 0, -0.3))   # head tilt: watching it fume
    a.at(40, head=(4, 4, 12), arm_r=(150, -30, -20), fore_r=(110, 0, 0))   # pushes hair back
    a.at(46, head=(10, 0, 4), arm_r=(160, -30, -10), fore_r=(120, 0, 0))
    a.at(52, chest=Z, head=(0, 0, -2), arm_r=(10, 0, 4), fore_r=(10, 0, 0), P_body=Z)
    a.at(60, chest=Z, head=Z, arm_r=Z, fore_r=Z, arm_l=Z, fore_l=Z)
    a.rot("leg_l", (0, 0, 0, 0), (10, 16, 0, -2), (14, -26, 0, -2), (24, -12, 0, -2), (34, 0, 0, 0))
    a.rot("leg_r", (0, 0, 0, 0), (10, -14, 0, 2), (14, 18, 0, 2), (24, 8, 0, 2), (34, 0, 0, 0))
    a.rot("shin_r", (0, 0, 0, 0), (14, -20, 0, 0), (30, 0, 0, 0))
    a.hair([(0, 0, 0, 0), (10, -6, 0, 4), (14, 14, 0, -6), (20, 2, 0, 0), (32, 0, 0, 6), (42, -8, 0, 2), (52, 0, 0, 0), (60, 0, 0, 0)])
    a.cloth([(0, 0, 0, 0), (10, 4, 0, 4), (14, -10, 0, -6, 4), (24, -2, 0, 0), (36, 0, 0, 0), (60, 0, 0, 0)])
    a.done()

    # ---------------------------------------------------------------- web_snare (40): hop + raise hands 0-10, both palms SLAM the floor 16, legs stab down, clench, rise
    a = mk("web_snare", 40).show("back", 4, 36, grow=3)
    a.at(0, chest=Z, P_body=Z)
    a.at(6, chest=(10, 0, 0), head=(14, 0, 0), arm_r=(160, 0, 30), arm_l=(160, 0, -30), fore_r=(20, 0, 0), fore_l=(20, 0, 0), P_body=(0, 1.0, 0))
    a.at(11, chest=(14, 0, 0), head=(18, 0, 0), arm_r=(176, 0, 20), arm_l=(176, 0, -20), P_body=(0, 1.4, 0.2))
    legs4(a, 6, (0, 0, 30), 0, (0, 0, 30), 0); legs4(a, 11, (0, 10, 50), -20, (0, 0, 50), -20)
    a.at(16, chest=(-42, 0, 0), head=(30, 0, 0), arm_r=(70, 0, 20), arm_l=(70, 0, -20), fore_r=(0, 0, 0), fore_l=(0, 0, 0), P_body=(0, -6.0, -1.2))
    legs4(a, 16, (0, 30, -10), -40, (0, -10, -20), -40, tp=-10, lag=0)
    a.at(20, chest=(-38, 0, 2), head=(28, 0, 0), P_body=(0, -5.6, -1.1))
    a.at(28, chest=(-36, 0, -2), head=(26, 4, 0), arm_r=(66, 0, 14), arm_l=(66, 0, -14), P_body=(0, -5.4, -1.0))
    legs4(a, 28, (0, 30, -10), -40, (0, -10, -20), -40, lag=0)
    a.at(33, chest=(-8, 0, 0), head=(4, 0, 0), arm_r=(10, 0, 8), arm_l=(10, 0, -8), fore_r=(14, 0, 0), fore_l=(14, 0, 0), P_body=(0, -0.8, -0.2))
    legs4(a, 33, (0, 0, 20), -20, (0, 0, 10), -20)
    a.at(40, chest=Z, head=Z, arm_r=Z, arm_l=Z, fore_r=Z, fore_l=Z, P_body=Z)
    a.rot("leg_r", (0, 0, 0, 0), (11, -10, 0, 2), (16, 74, 0, 6), (28, 74, 0, 6), (33, 14, 0, 2), (40, 0, 0, 0))
    a.rot("shin_r", (0, 0, 0, 0), (11, -10, 0, 0), (16, -96, 0, 0), (28, -96, 0, 0), (33, -18, 0, 0), (40, 0, 0, 0))
    a.rot("leg_l", (0, 0, 0, 0), (11, -10, 0, -2), (16, 74, 0, -6), (28, 74, 0, -6), (33, 14, 0, -2), (40, 0, 0, 0))
    a.rot("shin_l", (0, 0, 0, 0), (11, -10, 0, 0), (16, -96, 0, 0), (28, -96, 0, 0), (33, -18, 0, 0), (40, 0, 0, 0))
    a.rot("foot_r", (0, 0, 0, 0), (16, 22, 0, 0), (28, 22, 0, 0), (36, 0, 0, 0)).rot("foot_l", (0, 0, 0, 0), (16, 22, 0, 0), (28, 22, 0, 0), (36, 0, 0, 0))
    a.hair([(0, 0, 0, 0), (11, -8, 0, 0), (16, 22, 0, 0), (20, -6, 0, 0), (28, 0, 0, 0), (33, -6, 0, 0), (40, 0, 0, 0)])
    a.cloth([(0, 0, 0, 0), (11, -4, 0, 0), (16, 14, 0, 0, 18), (22, 6, 0, 0, 12), (33, 2, 0, 0), (40, 0, 0, 0)])
    a.done()

    # ---------------------------------------------------------------- skitter_pounce (28): drop to all fours 0-6, DASH 7 (legs scuttling), claw + leg strike 15, skid
    a = mk("skitter_pounce", 28).show("back", 2, 25, grow=2)
    a.at(0, chest=Z, P_body=Z)
    a.at(5, chest=(-50, 0, 0), head=(42, 0, 0), arm_r=(60, 0, 14), arm_l=(60, 0, -14), fore_r=(10, 0, 0), fore_l=(10, 0, 0), P_body=(0, -4.0, 1.0))
    legs4(a, 5, (0, -20, -30), -10, (0, -30, -40), -10)
    for t, j in ((7, 1), (9, -1), (11, 1)):
        legs4(a, t, (0, 20 * j, -20), -30, (0, -20 * j, -30), -30, lag=0)
    a.at(10, chest=(-56, 0, 0), head=(48, 0, 0), arm_r=(-40, 0, 14), arm_l=(-40, 0, -14), P_body=(0, -4.4, -0.8))
    a.at(13, chest=(-30, 0, 0), head=(26, 0, 0), arm_r=(160, 0, 20), arm_l=(160, 0, -20), fore_r=(20, 0, 0), fore_l=(20, 0, 0), P_body=(0, -2.4, -1.8))
    a.at(15, chest=(-34, 0, 0), head=(26, 0, 0), arm_r=(60, -20, -10), arm_l=(60, 20, 10), fore_r=Z, fore_l=Z, P_body=(0, -2.8, -2.4))
    legs4(a, 13, (0, -30, 40), -30, (0, -30, 30), -30, lag=0); legs4(a, 15, (40, 80, -20), 90, (40, 80, -10), 80, tp=20, lag=0)
    a.at(20, chest=(-14, 0, 0), head=(10, 0, 0), arm_r=(20, 0, 14), arm_l=(20, 0, -14), fore_r=(20, 0, 0), fore_l=(20, 0, 0), P_body=(0, -1.0, -1.2))
    legs4(a, 20, (0, 10, 0), -10, (0, 10, 0), -10)
    a.at(28, chest=Z, head=Z, arm_r=Z, arm_l=Z, fore_r=Z, fore_l=Z, P_body=Z)
    a.rot("leg_r", (0, 0, 0, 0), (5, 60, 0, 6), (7, -20, 0, 4), (9, 40, 0, 4), (11, -20, 0, 4), (13, 40, 0, 4), (15, 50, 0, 4), (20, 20, 0, 2), (28, 0, 0, 0))
    a.rot("leg_l", (0, 0, 0, 0), (5, 50, 0, -6), (7, 40, 0, -4), (9, -20, 0, -4), (11, 40, 0, -4), (13, -20, 0, -4), (15, -20, 0, -4), (20, 6, 0, -2), (28, 0, 0, 0))
    a.rot("shin_r", (0, 0, 0, 0), (5, -100, 0, 0), (9, -60, 0, 0), (13, -60, 0, 0), (15, -80, 0, 0), (20, -30, 0, 0), (28, 0, 0, 0))
    a.rot("shin_l", (0, 0, 0, 0), (5, -100, 0, 0), (9, -70, 0, 0), (13, -60, 0, 0), (15, -20, 0, 0), (20, -10, 0, 0), (28, 0, 0, 0))
    a.hair([(0, 0, 0, 0), (5, 10, 0, 0), (8, -24, 0, 0), (13, -24, 0, 0), (15, 12, 0, 0), (20, -4, 0, 0), (28, 0, 0, 0)], delay=1)
    a.cloth([(0, 0, 0, 0), (5, 4, 0, 0, 6), (8, -20, 0, 0, 4), (13, -20, 0, 0, 4), (16, 8, 0, 0, 6), (28, 0, 0, 0)], delay=1)
    a.done()

    # ---------------------------------------------------------------- leg_sweep (34): legs out and wound to her left 0-9, low SWEEP to the right 14, overshoot, fold
    a = mk("leg_sweep", 34).show("back", 2, 31, grow=2)
    a.at(0, chest=Z, P_body=Z, root=Z)
    a.at(8, chest=(-10, 46, 0), head=(4, -30, 0), arm_r=(40, 0, 50), arm_l=(10, 0, -30), fore_r=(40, 0, 0), P_body=(0, -1.4, 0))
    legs4(a, 8, (-30, -60, -30), 60, (-30, -70, -10), 60, lag=0.5)
    a.at(14, chest=(-14, -50, 0), head=(6, 30, 0), arm_r=(20, 0, 20), arm_l=(30, 0, -80), fore_l=(10, 0, 0), P_body=(0, -1.8, -0.4))
    legs4(a, 14, (30, 70, -40), 95, (30, 80, -25), 90, tp=10, lag=0.5)
    a.at(18, chest=(-10, -62, 0), head=(4, 36, 0), P_body=(0, -1.6, -0.4))
    legs4(a, 18, (20, 90, -30), 80, (20, 95, -20), 80)
    a.at(24, chest=(-4, -20, 0), head=(2, 10, 0), arm_r=(10, 0, 10), arm_l=(10, 0, -20), fore_l=(20, 0, 0), P_body=(0, -0.6, 0))
    legs4(a, 24, (0, 10, 0), 0, (0, 10, 0), 0); legs4(a, 30, (0, 0, -40), -60, (0, 0, -30), -50)
    a.at(34, chest=Z, head=Z, arm_r=Z, arm_l=Z, fore_r=Z, fore_l=Z, P_body=Z)
    a.legs([(0, 0, 0, 0), (8, -14, 0, 6), (14, -20, 0, 8), (24, -6, 0, 2), (34, 0, 0, 0)], [(0, 0, 0, 0), (8, -26, 0, 0), (14, -36, 0, 0), (24, -10, 0, 0), (34, 0, 0, 0)])
    a.hair([(0, 0, 0, 0), (8, 4, 0, 14), (14, -6, 0, -22), (18, -6, 0, -18), (24, 2, 0, 6), (34, 0, 0, 0)])
    a.cloth([(0, 0, 0, 0), (8, 2, 0, 10, 6), (14, -4, 0, -16, 14), (20, -2, 0, -8, 8), (34, 0, 0, 0)])
    a.done()

    # ---------------------------------------------------------------- venom_volley (40): legs rise like antennae, arms spread 0-9, legs jerk & fire 12/16/20/24, settle
    a = mk("venom_volley", 40).show("back", 2, 37, grow=2)
    a.at(0, chest=Z, head=Z, P_body=Z)
    a.at(8, chest=(10, 0, 0), head=(-4, 0, 0), arm_r=(20, 0, 40), arm_l=(20, 0, -40), fore_r=(40, 0, 0), fore_l=(40, 0, 0), P_body=(0, 0.3, 0.3))
    legs4(a, 8, (60, 30, 30), 70, (60, 20, 50), 70, tp=10)
    for t, (i, k) in zip((12, 16, 20, 24), ((0, "r"), (0, "l"), (1, "r"), (1, "l"))):
        a.SL(i, t - 1, (60, 30, 40) if i == 0 else (60, 20, 60), 80, 10, k)
        a.SL(i, t, (75, 50, 20) if i == 0 else (75, 40, 40), 95, 20, k)
        a.SL(i, t + 2, (60, 30, 30) if i == 0 else (60, 20, 50), 70, 10, k)
        s = 1 if k == "r" else -1
        a.at(t, chest=(6, 6 * s, 0), head=(-6, -4 * s, 0), P_body=(0, 0.2, 0.5))
        a.at(t + 2, chest=(10, 0, 0), head=(-4, 0, 0), P_body=(0, 0.3, 0.3))
    a.at(30, chest=(4, 0, 0), arm_r=(10, 0, 20), arm_l=(10, 0, -20), fore_r=(20, 0, 0), fore_l=(20, 0, 0))
    legs4(a, 30, (20, 10, 10), 20, (20, 10, 10), 20); legs4(a, 36, (0, 0, -40), -60, (0, 0, -30), -50)
    a.at(40, chest=Z, head=Z, arm_r=Z, arm_l=Z, fore_r=Z, fore_l=Z, P_body=Z)
    a.legs([(0, 0, 0, 0), (8, -4, 0, 4), (30, -4, 0, 4), (40, 0, 0, 0)], [(0, 0, 0, 0), (8, -8, 0, 0), (30, -8, 0, 0), (40, 0, 0, 0)])
    a.hair([(0, 0, 0, 0), (8, -6, 0, 0), (12, -4, 0, 4), (16, -4, 0, -4), (20, -4, 0, 4), (24, -4, 0, -4), (30, -2, 0, 0), (40, 0, 0, 0)], delay=2)
    a.cloth([(0, 0, 0, 0), (8, 2, 0, 0, 6), (12, 4, 0, 2, 8), (20, 4, 0, -2, 8), (30, 2, 0, 0, 4), (40, 0, 0, 0)], delay=2)
    a.done()

    # ---------------------------------------------------------------- grab_bite (48): crouch 0-7, POUNCE 8-11 (arms + legs clamp), BITE 18 & 28, hurl 38
    a = mk("grab_bite", 48).show("back", 5, 44, grow=2)
    a.at(0, chest=Z, P_body=Z)
    a.at(6, chest=(-26, 0, 0), head=(22, 0, 0), arm_r=(-30, 0, 30), arm_l=(-30, 0, -30), fore_r=(40, 0, 0), fore_l=(40, 0, 0), P_body=(0, -2.4, 1.0))
    legs4(a, 6, (0, -20, 40), -20, (0, -20, 30), -20)
    a.at(9, chest=(-20, 0, 0), head=(16, 0, 0), arm_r=(110, 0, 14), arm_l=(110, 0, -14), fore_r=Z, fore_l=Z, P_body=(0, 0.6, -2.4))
    a.at(11, chest=(-14, 0, 0), arm_r=(80, -24, -6), arm_l=(80, 24, 6), fore_r=(50, 0, 0), fore_l=(50, 0, 0), P_body=(0, -0.6, -2.6))
    legs4(a, 9, (30, 60, 20), 40, (30, 60, 0), 40, lag=0); legs4(a, 11, (40, 80, -10), -20, (40, 85, -20), -30, tp=-20, lag=0)
    for t in (18, 28):
        a.at(t - 3, chest=(-4, 0, 0), head=(-12, 0, 0))
        a.at(t, chest=(-24, 0, 0), head=(20, 0, 0), P_body=(0, -1.0, -2.6))
        a.at(t + 2, chest=(-18, 0, 0), head=(10, 0, 0))
        legs4(a, t, (40, 85, -14), -30, (40, 90, -24), -40, tp=-30, lag=0)
        legs4(a, t + 3, (40, 80, -10), -20, (40, 85, -20), -30, tp=-20, lag=0)
    a.at(14, arm_r=(74, -30, -10), arm_l=(74, 30, 10), fore_r=(60, 0, 0), fore_l=(60, 0, 0))
    a.at(34, chest=(-6, -30, 0), head=(4, 20, 0), arm_r=(60, -40, -20), arm_l=(70, -10, 10), fore_r=(50, 0, 0), fore_l=(50, 0, 0), P_body=(0, -1.0, -2.0))
    legs4(a, 34, (40, 40, 0), -10, (40, 40, -10), -20)
    a.at(38, chest=(-14, 40, 0), head=(0, -24, 0), arm_r=(40, 40, 60), arm_l=(80, 40, 10), fore_r=Z, fore_l=(10, 0, 0), P_body=(0, -0.8, -2.0))
    legs4(a, 38, (0, 60, 40), 80, (0, 60, 30), 80, lag=0)
    a.at(42, chest=(-6, 20, 0), arm_r=(20, 0, 30), arm_l=(30, 0, -10), P_body=(0, -0.4, -1.2))
    legs4(a, 42, (0, 0, -20), -40, (0, 0, -20), -40)
    a.at(48, chest=Z, head=Z, arm_r=Z, arm_l=Z, fore_r=Z, fore_l=Z, P_body=Z)
    a.rot("leg_r", (0, 0, 0, 0), (6, 30, 0, 4), (9, -40, 0, 2), (11, -30, 0, 2), (38, -30, 0, 2), (44, -6, 0, 0), (48, 0, 0, 0))
    a.rot("leg_l", (0, 0, 0, 0), (6, 20, 0, -4), (9, 30, 0, -2), (11, 24, 0, -2), (38, 24, 0, -2), (44, 4, 0, 0), (48, 0, 0, 0))
    a.rot("shin_r", (0, 0, 0, 0), (6, -60, 0, 0), (9, -10, 0, 0), (11, -20, 0, 0), (38, -20, 0, 0), (48, 0, 0, 0))
    a.rot("shin_l", (0, 0, 0, 0), (6, -70, 0, 0), (9, -30, 0, 0), (11, -40, 0, 0), (38, -40, 0, 0), (48, 0, 0, 0))
    a.hair([(0, 0, 0, 0), (6, 6, 0, 0), (9, -16, 0, 0), (18, 10, 0, 0), (28, 10, 0, 0), (38, -6, 0, -12), (44, 0, 0, 0)])
    a.cloth([(0, 0, 0, 0), (6, 4, 0, 0, 4), (9, -14, 0, 0), (18, -4, 0, 2), (28, -4, 0, -2), (38, -4, 0, 10), (48, 0, 0, 0)])
    a.done()

    # ---------------------------------------------------------------- web_pull (34): cock the left arm 4-9, SHOOT 12 (line sticks), taut 12-20, YANK 22, reel in, recover
    a = mk("web_pull", 34)
    web(a, 11, 12.5, 23, 27)
    a.scl("webline", (22, 1, 1, 1), (24, 1, 0.6, 1), (26.9, 1, 0.1, 1))
    a.at(0, chest=Z, arm_l=Z, fore_l=Z, P_body=Z)
    a.at(6, chest=(4, 24, 0), head=(4, -16, 0), arm_l=(150, 20, -30), fore_l=(40, 0, 0), arm_r=(10, 0, 14), P_body=(0, -0.3, 0.6))
    a.at(12, chest=(-8, -20, 0), head=(-2, 14, 0), arm_l=(94, -6, 4), fore_l=(-4, 0, 0), arm_r=(-14, 0, 20), P_body=(0, -0.5, -0.8))
    a.at(18, chest=(-6, -16, 0), arm_l=(92, -6, 4), fore_l=(-4, 0, 0), P_body=(0, -0.6, -0.8))
    a.at(20, chest=(-10, -18, 0), arm_l=(96, -6, 4), fore_l=(-2, 0, 0), head=(-4, 14, 0), P_body=(0, -0.8, -1.0))
    a.at(23, chest=(14, 26, 0), head=(6, -12, 0), arm_l=(30, 30, -20), fore_l=(100, 0, 0), arm_r=(40, 0, 30), fore_r=(30, 0, 0), P_body=(0, -0.8, 1.0))
    a.at(27, chest=(8, 14, 0), arm_l=(20, 20, -14), fore_l=(80, 0, 0), P_body=(0, -0.4, 0.6))
    a.at(34, chest=Z, head=Z, arm_l=Z, fore_l=Z, arm_r=Z, fore_r=Z, P_body=Z)
    a.rot("leg_l", (0, 0, 0, 0), (12, -22, 0, -2), (20, -22, 0, -2), (23, 16, 0, -2), (30, 0, 0, 0))
    a.rot("leg_r", (0, 0, 0, 0), (12, 14, 0, 2), (20, 14, 0, 2), (23, -24, 0, 2), (30, 0, 0, 0))
    a.rot("shin_r", (0, 0, 0, 0), (12, -14, 0, 0), (23, -6, 0, 0), (30, 0, 0, 0)).rot("shin_l", (0, 0, 0, 0), (23, -20, 0, 0), (30, 0, 0, 0))
    a.hair([(0, 0, 0, 0), (6, 6, 0, 6), (12, -10, 0, -6), (20, -4, 0, 0), (23, 14, 0, 6), (30, 0, 0, 0)])
    a.cloth([(0, 0, 0, 0), (6, 4, 0, 2), (12, -8, 0, -4), (23, 10, 0, 4), (34, 0, 0, 0)])
    a.done()

    # ---------------------------------------------------------------- shriek (36): curl, hands over ears 4-11, SHRIEK 14 (arched, arms + legs flung wide), shake, recover
    a = mk("shriek", 36).show("back", 11, 31, grow=2)
    a.at(0, chest=Z, P_body=Z)
    a.at(5, chest=(-20, 0, 0), head=(-24, 0, 0), arm_r=(130, 30, 40), arm_l=(130, -30, -40), fore_r=(110, 0, 0), fore_l=(110, 0, 0), P_body=(0, -1.2, 0.4))
    a.at(11, chest=(-30, 0, 4), head=(-30, 0, 6), arm_r=(140, 30, 30), arm_l=(140, -30, -30), fore_r=(120, 0, 0), fore_l=(120, 0, 0), P_body=(0, -1.8, 0.6))
    a.at(14, chest=(22, 0, 0), head=(26, 0, 0), arm_r=(10, 0, 100), arm_l=(10, 0, -100), fore_r=(-10, 0, 0), fore_l=(-10, 0, 0), P_body=(0, 0.4, 0.8))
    legs4(a, 11, (0, 0, -20), -40, (0, 0, -20), -40); legs4(a, 14, (0, 20, 30), 60, (0, -10, 20), 60, tp=20, lag=0)
    for t in (16, 18, 20, 22):
        j = 1 if t % 4 == 0 else -1
        a.at(t, chest=(20, 0, 2 * j), head=(24, 3 * j, -3 * j), arm_r=(10, 0, 96 + 4 * j), arm_l=(10, 0, -96 + 4 * j))
        legs4(a, t, (0, 20 + 4 * j, 30 + 4 * j), 60, (0, -10 - 4 * j, 20 - 4 * j), 60, tp=20, lag=0)
    a.at(27, chest=(-6, 0, 0), head=(-6, 0, -2), arm_r=(10, 0, 20), arm_l=(10, 0, -20), fore_r=(20, 0, 0), fore_l=(20, 0, 0), P_body=(0, -0.4, 0.2))
    legs4(a, 27, (0, 0, -20), -30, (0, 0, -20), -30)
    a.at(36, chest=Z, head=Z, arm_r=Z, arm_l=Z, fore_r=Z, fore_l=Z, P_body=Z)
    a.legs([(0, 0, 0, 0), (11, 10, 0, 0), (14, -6, 0, 8), (24, -6, 0, 8), (36, 0, 0, 0)], [(0, 0, 0, 0), (11, -24, 0, 0), (14, 0, 0, 0), (36, 0, 0, 0)])
    a.hair([(0, 0, 0, 0), (11, 10, 0, 0), (14, -26, 0, 0), (17, -22, 0, 6), (20, -24, 0, -6), (23, -22, 0, 4), (28, 0, 0, 0), (36, 0, 0, 0)], delay=1)
    a.cloth([(0, 0, 0, 0), (11, 4, 0, 0), (14, -10, 0, 0, 22), (22, -8, 0, 0, 18), (30, 0, 0, 0, 2), (36, 0, 0, 0)], delay=1)
    a.done()

    # ---------------------------------------------------------------- transform (130; phase-1 model plays 0-90): clutch head, legs tear out (40/62/80), hunch, swell
    a = mk("transform", 130).show("back", 38, 130, grow=4)
    a.scl("root", (0, 1, 1, 1), (40, 1, 1, 1), (62, 1.1, 1.1, 1.1), (80, 1.25, 1.25, 1.25), (90, 1.5, 1.5, 1.5), (130, 1.5, 1.5, 1.5))
    a.at(0, chest=Z, head=Z, P_body=Z)
    a.at(8, chest=(-16, 0, 0), head=(-26, 0, 0), arm_r=(140, 30, 30), arm_l=(140, -30, -30), fore_r=(120, 0, 0), fore_l=(120, 0, 0), P_body=(0, -0.8, 0))
    for t in range(12, 38, 4):
        j = 1 if (t // 4) % 2 else -1
        a.at(t, chest=(-24 - t * 0.3, 3 * j, 3 * j), head=(-30, 4 * j, -4 * j), P_body=(0, -1.0 - t * 0.04, 0))
    for t0 in (40, 62, 80):
        big = 1 + (t0 - 40) / 40
        a.at(t0 - 2, chest=(-34, 0, 0), head=(-30, 0, 0), arm_r=(140, 30, 30), arm_l=(140, -30, -30), fore_r=(120, 0, 0), fore_l=(120, 0, 0), P_body=(0, -2.0, 0))
        a.at(t0, chest=(24 * big, 0, 0), head=(30, 0, 0), arm_r=(20, 0, 70 * big), arm_l=(20, 0, -70 * big), fore_r=Z, fore_l=Z, P_body=(0, 0.4, 0))
        legs4(a, t0, (0, 0, 30 * big), 60, (0, 0, 20 * big), 60, tp=20, lag=0)
        legs4(a, t0 + 5, (0, 0, -10), -20, (0, 0, -10), -20)
        if t0 < 80:
            a.at(t0 + 6, chest=(-20, 0, 6), head=(-20, 10, 0), arm_r=(60, 0, 30), arm_l=(60, 0, -30), fore_r=(60, 0, 0), fore_l=(60, 0, 0), P_body=(0, -1.6, 0))
    legs4(a, 90, (0, 0, 40), 70, (0, 0, 30), 70, tp=20)
    a.at(90, chest=(16, 0, 0), head=(20, 0, 0), arm_r=(10, 0, 90), arm_l=(10, 0, -90), fore_r=(-10, 0, 0), fore_l=(-10, 0, 0), P_body=(0, 0.6, 0))
    a.at(130, chest=(16, 0, 0), head=(20, 0, 0), arm_r=(10, 0, 90), arm_l=(10, 0, -90), fore_r=(-10, 0, 0), fore_l=(-10, 0, 0), P_body=(0, 0.6, 0))
    legs4(a, 130, (0, 0, 40), 70, (0, 0, 30), 70, tp=20)
    a.legs([(0, 0, 0, 0), (12, 10, 0, 4), (38, 14, 0, 6), (40, -4, 0, 8), (60, 14, 0, 6), (80, -4, 0, 10), (90, 0, 0, 12), (130, 0, 0, 12)],
           [(0, 0, 0, 0), (12, -20, 0, 0), (38, -30, 0, 0), (40, 0, 0, 0), (60, -30, 0, 0), (80, 0, 0, 0), (130, 0, 0, 0)])
    a.hair([(0, 0, 0, 0), (8, 10, 0, 0), (20, 10, 0, 6), (30, 10, 0, -6), (40, -24, 0, 0), (50, 10, 0, 6), (62, -26, 0, 0), (72, 10, 0, -6), (80, -30, 0, 0), (90, -30, 0, 8), (130, -30, 0, 8)], delay=1)
    a.cloth([(0, 0, 0, 0), (12, 2, 0, 0, 4), (40, -10, 0, 0, 20), (50, 2, 0, 0, 8), (62, -10, 0, 0, 26), (72, 2, 0, 0, 10), (80, -12, 0, 0, 34), (130, -12, 0, 0, 34)], delay=1)
    a.done()

    # ---------------------------------------------------------------- death (40): clutch chest, knees give, topple sideways, legs curl up like a dead spider, fade flat
    a = mk("death", 40).show("back", 6, 40, grow=4)
    a.at(0, chest=Z, P_root=Z, root=Z)
    a.at(5, chest=(-20, 0, 0), head=(-14, 0, 0), arm_r=(60, 40, 0), arm_l=(60, -40, 0), fore_r=(90, 0, 0), fore_l=(90, 0, 0), P_body=(0, -0.6, 0))
    a.at(14, chest=(-30, 0, 10), head=(-20, 0, 14), arm_r=(10, 0, 30), arm_l=(60, -40, 0), P_body=(0, -5.0, 0))
    a.at(24, root=(0, 0, 80), P_root=(4, 0.8, 0), chest=(-10, 0, 6), head=(10, 0, 10), arm_r=(10, 0, 70), fore_r=(10, 0, 0))
    a.at(40, root=(0, 0, 90), P_root=(5.5, 0.0, 0))
    legs4(a, 10, (0, 0, 20), 40, (0, 0, 10), 40); legs4(a, 18, (0, 0, -10), -10, (0, 0, -10), -10)
    legs4(a, 30, (0, 0, -40), -60, (0, 0, -40), -60, tp=-40); legs4(a, 40, (0, 0, -50), -70, (0, 0, -50), -70, tp=-50)
    a.scl("root", (0, 1, 1, 1), (32, 1, 1, 1), (40, 1.1, 0.4, 1.1))
    a.legs([(0, 0, 0, 0), (14, 60, 0, 4), (24, 30, 0, 8), (40, 20, 0, 6)], [(0, 0, 0, 0), (14, -100, 0, 0), (24, -50, 0, 0), (40, -40, 0, 0)])
    a.hair([(0, 0, 0, 0), (5, 10, 0, 0), (14, 10, 0, 10), (24, -10, 0, 30), (32, 0, 0, 24), (40, 0, 0, 24)], delay=2)
    a.cloth([(0, 0, 0, 0), (14, 10, 0, 0, 20), (24, -6, 0, 20, 6), (40, -6, 0, 20, 6)])
    a.done()


# ================================================================== PHASE 2 animations
def L8(a, t, f=Z, tb=0, tp=0, legs=(0, 1, 2, 3), side="rl", lag=1.0):
    for i in legs:
        a.SL(i, t, f, tb, tp, side, lag)


def calm8(a, t, lag=1.0):
    L8(a, t, Z, 0, 0, lag=lag)


def anims_p2(B):
    def mk(name, ticks, loop=False):
        return A(B, name, ticks, (), loop)

    def abd(a, *keys):  # abdomen rotation deltas (rx = tip up/down)
        a.rot("abdomen", *keys)

    # ---------------------------------------------------------------- idle (80): heavy breathing, legs flex one after another, abdomen pulses, head twitches
    a = mk("idle", 80, loop=True)
    a.at(0, chest=Z, head=(0, 0, -4), P_body=Z)
    a.at(20, chest=(2, 0, 0), head=(4, -4, -6), P_body=(0, 0.12, 0))
    a.at(40, chest=Z, head=(0, 0, -4), P_body=Z)
    a.at(48, head=(0, 0, -4)).at(50, head=(-6, 16, 10)).at(53, head=(-2, 14, 8)).at(56, head=(0, 0, -4))
    a.at(60, chest=(2, 0, 0), P_body=(0, 0.12, 0))
    a.at(80, chest=Z, head=(0, 0, -4), P_body=Z)
    a.at(0, arm_r=Z, arm_l=Z).at(40, arm_r=(4, 0, 4), arm_l=(4, 0, -4)).at(80, arm_r=Z, arm_l=Z)
    for i in range(4):
        for k, ph in (("r", 0), ("l", 10)):
            t0 = (i * 20 + ph) % 80
            keys = sorted({0: 0, t0: 0, (t0 + 8) % 80: 8, (t0 + 16) % 80: 0, 80: 0}.items())
            kk = {}
            for t, v in keys:
                kk[t] = v
            kk[80] = kk.get(0, 0)
            for t, v in sorted(kk.items()):
                a.SL(i, t, (0, 0, v * (0.6 if i > 1 else 1)), -v * 0.8, v * 0.5, k, 0)
    abd(a, (0, 0, 0, 0), (20, 4, 0, 0), (40, 0, 0, 0), (60, 4, 0, 0), (80, 0, 0, 0))
    a.scl("abdomen", (0, 1, 1, 1), (20, 1.04, 1.04, 1.03), (40, 1, 1, 1), (60, 1.04, 1.04, 1.03), (80, 1, 1, 1))
    a.hair([(0, 0, 0, 1), (20, 2, 0, -1), (40, 0, 0, 1), (60, 2, 0, -1), (80, 0, 0, 1)], delay=5)
    a.cloth([(0, 0, 0, 1), (20, 1, 0, -1), (40, 0, 0, 1), (60, 1, 0, -1), (80, 0, 0, 1)], delay=5)
    a.done()

    # ---------------------------------------------------------------- walk (20, additive): alternating-tetrapod spider gait + gliding body
    a = mk("walk", 20, loop=True)
    grpA = (("r", 0), ("l", 1), ("r", 2), ("l", 3))
    grpB = (("l", 0), ("r", 1), ("l", 2), ("r", 3))
    for grp, off in ((grpA, 0), (grpB, 10)):
        for k, i in grp:
            ks = [(0, 1), (5, 0), (10, -1), (15, 0), (20, 1)] if off == 0 else [(0, -1), (5, 0), (10, 1), (15, 0), (20, -1)]
            lift = {0: 0, 5: 0, 10: 0, 15: 1, 20: 0} if off == 0 else {0: 0, 5: 1, 10: 0, 15: 0, 20: 0}
            for t, sw in ks:
                a.SL(i, t, (0, 16 * sw, 14 * lift[t]), -10 * lift[t], 0, k, 0)
    a.pos("body", (0, 0, -0.3, 0), (5, 0, 0.2, 0), (10, 0, -0.3, 0), (15, 0, 0.2, 0), (20, 0, -0.3, 0))
    a.rot("chest", (0, -2, -4, 0), (10, -2, 4, 0), (20, -2, -4, 0))
    a.rot("leg_r", (0, 18, 0, 0), (10, -16, 0, 0), (20, 18, 0, 0)).rot("leg_l", (0, -16, 0, 0), (10, 18, 0, 0), (20, -16, 0, 0))
    a.rot("arm_r", (0, -8, 0, 0), (10, 8, 0, 0), (20, -8, 0, 0)).rot("arm_l", (0, 8, 0, 0), (10, -8, 0, 0), (20, 8, 0, 0))
    a.rot("abdomen", (0, 0, 4, 0), (10, 0, -4, 0), (20, 0, 4, 0))
    a.hair([(0, -3, 0, 2), (10, -3, 0, -2), (20, -3, 0, 2)], delay=2)
    a.cloth([(0, -5, 0, 2), (5, -7, 0, 0), (10, -5, 0, -2), (15, -7, 0, 0), (20, -5, 0, 2)], delay=1)
    a.done(base_layer=True)

    # ---------------------------------------------------------------- leg_impale (40): rear back, top legs cocked 0-12, R leg IMPALES 16, L leg IMPALES 24, wrench free, settle
    a = mk("leg_impale", 40)
    a.at(0, chest=Z, head=Z, P_root=Z)
    a.at(10, chest=(14, 0, 0), head=(10, 0, 0), arm_r=(20, 0, 30), arm_l=(20, 0, -30), P_root=(0, 1.6, 0.6))
    L8(a, 10, (0, -20, 30), -30, -10, legs=(0,)); L8(a, 10, (0, 0, 10), -10, 0, legs=(1,)); L8(a, 10, (0, 0, -6), 10, 0, legs=(2, 3))
    a.SL(0, 13, (40, -10, 40), -40, -10, "r")
    a.SL(0, 16, (60, 60, -20), 70, 20, "r", 0.5).SL(0, 20, (60, 50, -14), 60, 16, "r")
    a.at(16, chest=(-20, 16, 0), head=(14, -10, 0), arm_r=(60, 0, 20), P_root=(0, -0.6, -1.4))
    a.SL(0, 21, (40, -10, 40), -40, -10, "l")
    a.SL(0, 24, (60, 60, -20), 70, 20, "l", 0.5).SL(0, 28, (60, 50, -14), 60, 16, "l")
    a.SL(0, 24, (0, 0, 20), -10, 0, "r")
    a.at(24, chest=(-22, -16, 0), head=(14, 10, 0), arm_l=(60, 0, -20), arm_r=(10, 0, 20), P_root=(0, -0.8, -1.6))
    a.at(32, chest=(-4, 0, 0), head=(2, 0, 0), arm_r=Z, arm_l=(10, 0, -10), P_root=(0, 0, -0.4))
    L8(a, 32, Z, 0, 0, legs=(0, 1, 2, 3), side="r"); L8(a, 33, (0, 0, 10), -10, 0, legs=(0,), side="l")
    a.at(40, chest=Z, head=Z, arm_l=Z, P_root=Z)
    L8(a, 40, Z, 0, 0)
    abd(a, (0, 0, 0, 0), (10, -16, 0, 0), (16, 10, 0, 0), (24, 12, 0, 0), (32, 0, 0, 0))
    a.hair([(0, 0, 0, 0), (10, -6, 0, 0), (16, 12, 0, 6), (24, 12, 0, -6), (32, 0, 0, 0)])
    a.cloth([(0, 0, 0, 0), (10, -4, 0, 0, 4), (16, 6, 0, 4, 8), (24, 6, 0, -4, 8), (34, 0, 0, 0)])
    a.done()

    # ---------------------------------------------------------------- leg_barrage (48): crouch forward 0-10, five machine-gun jabs 12/17/22/27/32 (front legs alternate), recoil
    a = mk("leg_barrage", 48)
    a.at(0, chest=Z, P_root=Z)
    a.at(9, chest=(-18, 0, 0), head=(16, 0, 0), arm_r=(30, 0, 20), arm_l=(30, 0, -20), fore_r=(60, 0, 0), fore_l=(60, 0, 0), P_root=(0, -1.0, 0.6))
    L8(a, 9, (0, -30, 30), -40, -10, legs=(0, 1)); L8(a, 9, (0, 0, -8), 8, 0, legs=(2, 3))
    jabs = ((12, 0, "r"), (17, 0, "l"), (22, 1, "r"), (27, 1, "l"), (32, 0, "r"))
    for t, i, k in jabs:
        o = "l" if k == "r" else "r"
        a.SL(i, t - 2, (20, -30, 40), -50, -10, k)
        a.SL(i, t, (70, 70, -10), 80, 20, k, 0.3)
        a.SL(i, t + 2.5, (30, 0, 30), -30, -10, k)
        s = 1 if k == "r" else -1
        a.at(t, chest=(-24, 10 * s, 0), head=(18, -6 * s, 0), P_root=(0, -1.2, -0.6))
        a.at(t + 2, chest=(-18, 2 * s, 0), head=(16, 0, 0), P_root=(0, -1.0, 0))
    a.at(38, chest=(-6, 0, 0), head=(4, 0, 0), arm_r=Z, arm_l=Z, fore_r=Z, fore_l=Z, P_root=(0, -0.2, 0))
    L8(a, 38, Z, 0, 0)
    a.at(48, chest=Z, head=Z, P_root=Z)
    abd(a, (0, 0, 0, 0), (9, -10, 0, 0), (12, -4, 0, 0), (22, -4, 0, 0), (32, -4, 0, 0), (40, 0, 0, 0))
    a.hair([(0, 0, 0, 0), (9, 8, 0, 0), (12, -4, 0, 4), (17, -4, 0, -4), (22, -4, 0, 4), (27, -4, 0, -4), (32, -4, 0, 4), (40, 0, 0, 0)], delay=1)
    a.cloth([(0, 0, 0, 0), (9, 4, 0, 0, 4), (12, -4, 0, 3, 6), (22, -4, 0, -3, 6), (32, -4, 0, 3, 6), (40, 0, 0, 0)], delay=1)
    a.done()

    # ---------------------------------------------------------------- web_net (44): front legs lift, abdomen swings under her 0-14, WEB BLAST 18 (spinneret aimed forward), recoil, reset
    a = mk("web_net", 44)
    a.at(0, chest=Z, P_root=Z)
    a.at(12, chest=(16, 0, 0), head=(-6, 0, 0), arm_r=(20, 0, 40), arm_l=(20, 0, -40), P_root=(0, 2.0, 1.0))
    L8(a, 12, (0, 10, 40), -20, 0, legs=(0, 1)); L8(a, 12, (0, -10, -10), -10, 0, legs=(2, 3))
    abd(a, (0, 0, 0, 0), (12, 110, 0, 0), (16, 120, 0, 0), (18, 100, 0, 0), (22, 116, 0, 0), (32, 40, 0, 0), (40, 0, 0, 0))
    a.scl("abdomen", (0, 1, 1, 1), (14, 0.94, 0.94, 0.94), (17, 0.92, 0.92, 0.92), (18, 1.15, 1.15, 1.15), (22, 1, 1, 1), (44, 1, 1, 1))
    a.at(18, chest=(6, 0, 0), head=(-2, 0, 0), arm_r=(10, 0, 60), arm_l=(10, 0, -60), P_root=(0, 2.4, 1.6))
    L8(a, 18, (0, 20, 50), 20, 10, legs=(0, 1), lag=0); L8(a, 18, (0, -20, -14), -14, 0, legs=(2, 3), lag=0)
    a.at(24, chest=(10, 0, 0), P_root=(0, 1.8, 1.2))
    a.at(34, chest=(2, 0, 0), arm_r=(4, 0, 10), arm_l=(4, 0, -10), P_root=(0, 0.4, 0.2))
    L8(a, 34, Z, 0, 0)
    a.at(44, chest=Z, head=Z, arm_r=Z, arm_l=Z, P_root=Z)
    a.hair([(0, 0, 0, 0), (12, -8, 0, 0), (18, 10, 0, 0), (24, -4, 0, 0), (34, 0, 0, 0)])
    a.cloth([(0, 0, 0, 0), (12, -4, 0, 0, 6), (18, 6, 0, 0, 12), (30, 0, 0, 0)])
    a.done()

    # ---------------------------------------------------------------- tentacle_field (46): rear up 0-14, ALL legs plunge into the floor 18, hold (shaking), rip out 36-40
    a = mk("tentacle_field", 46)
    a.at(0, chest=Z, P_root=Z)
    a.at(8, chest=(10, 0, 0), head=(14, 0, 0), arm_r=(150, 0, 30), arm_l=(150, 0, -30), fore_r=(30, 0, 0), fore_l=(30, 0, 0), P_root=(0, 1.6, 0.4))
    a.at(14, chest=(16, 0, 0), head=(20, 0, 0), arm_r=(175, 0, 20), arm_l=(175, 0, -20), fore_r=(20, 0, 0), fore_l=(20, 0, 0), P_root=(0, 2.4, 0.6))
    L8(a, 8, (0, 0, 30), 20, 0); L8(a, 14, (0, 0, 44), 30, 10)
    a.at(18, chest=(-40, 0, 0), head=(30, 0, 0), arm_r=(60, 0, 14), arm_l=(60, 0, -14), fore_r=Z, fore_l=Z, P_root=(0, -2.6, -1.0))
    L8(a, 18, (0, 0, -16), -24, -20, lag=0)
    for t in (22, 26, 30):
        j = 1 if t % 8 == 6 else -1
        a.at(t, chest=(-38, 0, 2 * j), head=(28, 4 * j, 0), P_root=(0, -2.4, -0.9))
        L8(a, t, (0, 0, -14 + 2 * j), -22, -20, lag=0)
    a.at(36, chest=(-20, 0, 0), head=(16, 0, 0), arm_r=(80, 0, 30), arm_l=(80, 0, -30), fore_r=(40, 0, 0), fore_l=(40, 0, 0), P_root=(0, -1.0, -0.4))
    L8(a, 38, (0, 0, 20), 20, 10); L8(a, 46, Z, 0, 0)
    a.at(46, chest=Z, head=Z, arm_r=Z, arm_l=Z, fore_r=Z, fore_l=Z, P_root=Z)
    abd(a, (0, 0, 0, 0), (14, -20, 0, 0), (18, 16, 0, 0), (34, 14, 0, 0), (46, 0, 0, 0))
    a.hair([(0, 0, 0, 0), (14, -10, 0, 0), (18, 22, 0, 0), (24, -6, 0, 0), (34, 0, 0, 0), (40, -6, 0, 0), (46, 0, 0, 0)])
    a.cloth([(0, 0, 0, 0), (14, -4, 0, 0), (18, 10, 0, 0, 20), (26, 4, 0, 0, 12), (40, 0, 0, 0, 2), (46, 0, 0, 0)])
    a.done()

    # ---------------------------------------------------------------- spike_carpet (48): front legs reach far forward 0-11, RAKE back across the floor 16, crouched hold, rise
    a = mk("spike_carpet", 48)
    a.at(0, chest=Z, P_root=Z)
    a.at(10, chest=(-16, 0, 0), head=(14, 0, 0), arm_r=(60, 0, 30), arm_l=(60, 0, -30), P_root=(0, 0.6, -0.6))
    L8(a, 10, (30, 70, 10), 50, 10, legs=(0, 1))
    a.at(16, chest=(-34, 0, 0), head=(26, 0, 0), arm_r=(40, 0, 20), arm_l=(40, 0, -20), P_root=(0, -2.4, -0.6))
    L8(a, 13, (30, 50, -20), 30, 0, legs=(0, 1), lag=0); L8(a, 16, (20, -10, -30), -10, -20, legs=(0, 1), lag=0)
    L8(a, 16, (0, 0, -12), -12, -10, legs=(2, 3))
    a.at(30, chest=(-30, 0, 0), head=(24, 0, 0), P_root=(0, -2.2, -0.5))
    L8(a, 30, (20, -14, -26), -10, -20, legs=(0, 1)); L8(a, 30, (0, 0, -10), -10, -10, legs=(2, 3))
    a.at(40, chest=(-8, 0, 0), head=(6, 0, 0), arm_r=Z, arm_l=Z, P_root=(0, -0.4, 0))
    L8(a, 40, Z, 0, 0)
    a.at(48, chest=Z, head=Z, P_root=Z)
    abd(a, (0, 0, 0, 0), (10, -14, 0, 0), (16, 14, 0, 0), (32, 10, 0, 0), (44, 0, 0, 0))
    a.hair([(0, 0, 0, 0), (10, 6, 0, 0), (16, 16, 0, 0), (22, -4, 0, 0), (32, 0, 0, 0), (40, -4, 0, 0), (48, 0, 0, 0)])
    a.cloth([(0, 0, 0, 0), (10, 4, 0, 0, 4), (16, 10, 0, 0, 14), (32, 6, 0, 0, 10), (44, 0, 0, 0)])
    a.done()

    # ---------------------------------------------------------------- scythe_sweep (46): R mid-leg cocked back 0-11, SCYTHES forward 15, L cocked 22, SCYTHES 27, recover
    a = mk("scythe_sweep", 46)
    a.at(0, chest=Z, P_root=Z)
    for t0, k, s in ((15, "r", 1), (27, "l", -1)):
        a.SL(1, t0 - 5, (0, -60, 34), -10, 0, k).SL(0, t0 - 5, (0, -30, 20), -10, 0, k)
        a.SL(1, t0, (20, 70, -4), 80, 20, k, 0.4).SL(0, t0, (20, 40, -10), 50, 10, k, 0.4)
        a.SL(1, t0 + 4, (10, 90, 4), 60, 10, k).SL(0, t0 + 4, (10, 60, 0), 40, 0, k)
        a.SL(1, t0 + 8, Z, 0, 0, k).SL(0, t0 + 8, Z, 0, 0, k)
        a.at(t0 - 5, chest=(-6, 30 * s, 0), head=(4, -20 * s, 0), arm_r=(30, 0, 40) if s > 0 else (10, 0, 10), arm_l=(10, 0, -10) if s > 0 else (30, 0, -40), P_root=(0, -0.6, 0.4))
        a.at(t0, chest=(-14, -36 * s, 0), head=(8, 24 * s, 0), arm_r=(60, 0, 10) if s > 0 else (10, 0, 30), arm_l=(10, 0, -30) if s > 0 else (60, 0, -10), P_root=(0, -1.2, -0.8))
        a.at(t0 + 4, chest=(-10, -44 * s, 0), head=(6, 28 * s, 0))
    a.at(38, chest=(-2, 0, 0), head=Z, arm_r=Z, arm_l=Z, P_root=Z)
    a.at(46, chest=Z)
    L8(a, 15, (0, 0, -6), 6, 0, legs=(2, 3)); L8(a, 27, (0, 0, -6), 6, 0, legs=(2, 3)); L8(a, 40, Z, 0, 0, legs=(2, 3))
    abd(a, (0, 0, 0, 0), (10, 0, -20, 0), (15, 0, 24, 0), (22, 0, 20, 0), (27, 0, -24, 0), (36, 0, 0, 0))
    a.hair([(0, 0, 0, 0), (10, 4, 0, -10), (15, -6, 0, 16), (22, 4, 0, 10), (27, -6, 0, -16), (36, 0, 0, 0)])
    a.cloth([(0, 0, 0, 0), (10, 2, 0, -8, 4), (15, -4, 0, 12, 10), (22, 2, 0, 8, 4), (27, -4, 0, -12, 10), (38, 0, 0, 0)])
    a.done()

    # ---------------------------------------------------------------- body_slam (44): rears up tall on the hind legs 0-16, front legs high, CRASHES down 21, shudder, rise
    a = mk("body_slam", 44)
    a.at(0, chest=Z, P_root=Z, root=Z)
    a.at(14, root=(16, 0, 0), chest=(14, 0, 0), head=(10, 0, 0), arm_r=(160, 0, 30), arm_l=(160, 0, -30), P_root=(0, 3.4, 1.6))
    L8(a, 14, (0, 10, 40), 30, 10, legs=(0, 1)); L8(a, 14, (0, 0, -10), -10, -6, legs=(2,)); L8(a, 14, (0, -10, -16), -12, -8, legs=(3,))
    a.at(18, root=(18, 0, 0), P_root=(0, 3.8, 1.8))
    a.at(21, root=(-14, 0, 0), chest=(-30, 0, 0), head=(26, 0, 0), arm_r=(50, 0, 14), arm_l=(50, 0, -14), P_root=(0, -1.3, -1.6))
    L8(a, 21, (40, 60, -24), 40, 0, legs=(0, 1), lag=0); L8(a, 21, (0, 0, -10), -14, -10, legs=(2, 3), lag=0)
    a.at(24, root=(-12, 0, 0), P_root=(0, -1.0, -1.5)).at(27, root=(-14, 0, 0), P_root=(0, -1.2, -1.6))
    a.at(34, root=(-4, 0, 0), chest=(-10, 0, 0), head=(6, 0, 0), arm_r=(20, 0, 10), arm_l=(20, 0, -10), P_root=(0, -0.6, -0.4))
    L8(a, 34, Z, 0, 0)
    a.at(44, root=Z, chest=Z, head=Z, arm_r=Z, arm_l=Z, P_root=Z)
    abd(a, (0, 0, 0, 0), (14, -30, 0, 0), (21, 24, 0, 0), (26, 14, 0, 0), (36, 0, 0, 0))
    a.hair([(0, 0, 0, 0), (14, -10, 0, 0), (21, 24, 0, 0), (26, -6, 0, 0), (34, 0, 0, 0)])
    a.cloth([(0, 0, 0, 0), (14, -8, 0, 0, 4), (21, 12, 0, 0, 22), (28, 2, 0, 0, 8), (40, 0, 0, 0)])
    a.done()

    # ---------------------------------------------------------------- web_cocoon (56): front legs open wide 0-12, SNAP shut 16 (grab), hoist + spin silk 20-44, squeeze 26/36, SLAM 46
    a = mk("web_cocoon", 56)
    a.at(0, chest=Z, P_root=Z)
    a.at(12, chest=(-10, 0, 0), head=(10, 0, 0), arm_r=(70, -30, 50), arm_l=(70, 30, -50), P_root=(0, 0.4, -0.4))
    L8(a, 12, (20, 40, 30), 50, 10, legs=(0, 1))
    a.at(16, chest=(-16, 0, 0), head=(14, 0, 0), arm_r=(80, -30, -10), arm_l=(80, 30, 10), fore_r=(50, 0, 0), fore_l=(50, 0, 0), P_root=(0, -0.4, -1.0))
    L8(a, 16, (40, 90, 0), -30, -30, legs=(0, 1), lag=0)
    for t in (22, 26, 30, 36, 40):
        sq = 1 if t in (26, 36) else 0
        a.at(t, chest=(4 - 4 * sq, 0, 0), head=(-4, 0, 0), arm_r=(120, -30, -10), arm_l=(120, 30, 10), fore_r=(60 + 20 * sq, 0, 0), fore_l=(60 + 20 * sq, 0, 0), P_root=(0, 1.0, 0))
        L8(a, t, (50, 90, 30 - 6 * sq), -40 - 15 * sq, -30 - 10 * sq, legs=(0, 1), lag=0)
    a.rot("abdomen", (0, 0, 0, 0), (16, 0, 0, 0), (20, 60, 0, 0), (24, 50, 10, 0), (28, 60, -10, 0), (32, 50, 10, 0), (36, 60, -10, 0), (40, 50, 0, 0), (46, 0, 0, 0), (56, 0, 0, 0))
    a.at(44, chest=(14, 0, 0), arm_r=(170, -20, -10), arm_l=(170, 20, 10), fore_r=(20, 0, 0), fore_l=(20, 0, 0), P_root=(0, 1.6, 0.6))
    L8(a, 44, (40, 60, 50), -10, -10, legs=(0, 1))
    a.at(46, chest=(-36, 0, 0), head=(26, 0, 0), arm_r=(50, 0, 10), arm_l=(50, 0, -10), fore_r=Z, fore_l=Z, P_root=(0, -2.0, -1.4))
    L8(a, 46, (40, 70, -24), 30, 0, legs=(0, 1), lag=0); L8(a, 46, (0, 0, -10), -10, -10, legs=(2, 3), lag=0)
    a.at(52, chest=(-10, 0, 0), head=(6, 0, 0), P_root=(0, -0.4, -0.3))
    L8(a, 52, Z, 0, 0)
    a.at(56, chest=Z, head=Z, arm_r=Z, arm_l=Z, P_root=Z)
    a.hair([(0, 0, 0, 0), (12, 6, 0, 0), (16, -8, 0, 0), (26, 4, 0, 4), (36, 4, 0, -4), (44, -10, 0, 0), (46, 20, 0, 0), (52, 0, 0, 0)])
    a.cloth([(0, 0, 0, 0), (12, 2, 0, 0, 6), (16, -4, 0, 0), (30, 2, 0, 0, 6), (44, -6, 0, 0), (46, 10, 0, 0, 20), (56, 0, 0, 0)])
    a.done()

    # ---------------------------------------------------------------- venom_barrage (52): rear up, head + chest tilted back 0-12, spits venom 14..38 (recoil every 3t), settle
    a = mk("venom_barrage", 52)
    a.at(0, chest=Z, head=Z, P_root=Z)
    a.at(10, chest=(18, 0, 0), head=(14, 0, 0), arm_r=(30, 0, 50), arm_l=(30, 0, -50), P_root=(0, 2.4, 0.8))
    L8(a, 10, (0, 10, 30), 10, 0, legs=(0, 1)); L8(a, 10, (0, -6, -10), -10, 0, legs=(2, 3))
    for n, t in enumerate(range(14, 39, 3)):
        s = 1 if n % 2 == 0 else -1
        a.at(t, chest=(4, 6 * s, 0), head=(-10, -8 * s, 0), P_root=(0, 2.2, 1.0))
        a.at(t + 1.5, chest=(14, 2 * s, 0), head=(8, 0, 0), P_root=(0, 2.4, 0.8))
        L8(a, t, (0, 10, 36), 16, 6, legs=(0,), side="r" if s > 0 else "l", lag=0)
        L8(a, t + 1.5, (0, 10, 30), 10, 0, legs=(0,), side="r" if s > 0 else "l", lag=0)
    a.at(44, chest=(4, 0, 0), head=(2, 0, 0), arm_r=(10, 0, 10), arm_l=(10, 0, -10), P_root=(0, 0.4, 0.2))
    L8(a, 44, Z, 0, 0)
    a.at(52, chest=Z, head=Z, arm_r=Z, arm_l=Z, P_root=Z)
    abd(a, (0, 0, 0, 0), (10, -20, 0, 0), (40, -20, 0, 0), (48, 0, 0, 0))
    a.hair([(0, 0, 0, 0), (10, -8, 0, 0), (14, 6, 0, 3), (20, 6, 0, -3), (26, 6, 0, 3), (32, 6, 0, -3), (38, 6, 0, 3), (44, 0, 0, 0)], delay=1)
    a.cloth([(0, 0, 0, 0), (10, -4, 0, 0, 6), (24, -2, 0, 2, 8), (36, -2, 0, -2, 8), (46, 0, 0, 0)])
    a.done()

    # ---------------------------------------------------------------- roar (50): crouch, legs drawn in 0-14, ROAR 18 (legs flare wide + up, chest arched), shake 20-34, settle
    a = mk("roar", 50)
    a.at(0, chest=Z, head=Z, P_root=Z)
    a.at(12, chest=(-30, 0, 0), head=(-10, 0, 0), arm_r=(40, 30, 10), arm_l=(40, -30, -10), fore_r=(90, 0, 0), fore_l=(90, 0, 0), P_root=(0, -2.0, 0.4))
    L8(a, 12, (0, 0, -20), -30, -20)
    a.at(18, chest=(24, 0, 0), head=(30, 0, 0), arm_r=(20, 0, 100), arm_l=(20, 0, -100), fore_r=(-10, 0, 0), fore_l=(-10, 0, 0), P_root=(0, 1.4, 0.6))
    L8(a, 18, (0, 0, 30), 40, 20, legs=(0, 1), lag=0); L8(a, 18, (0, 0, 14), 20, 10, legs=(2, 3), lag=0)
    for t in range(20, 36, 2):
        j = 1 if t % 4 == 0 else -1
        a.at(t, chest=(22, 2 * j, 2 * j), head=(28, 4 * j, -3 * j), arm_r=(20, 0, 96 + 5 * j), arm_l=(20, 0, -96 + 5 * j))
        L8(a, t, (0, 0, 28 + 3 * j), 38, 20, legs=(0, 1), lag=0)
    a.scl("abdomen", (0, 1, 1, 1), (12, 0.95, 0.95, 0.95), (18, 1.12, 1.12, 1.12), (34, 1.1, 1.1, 1.1), (42, 1, 1, 1), (50, 1, 1, 1))
    a.at(42, chest=(-4, 0, 0), head=(0, 0, 0), arm_r=(10, 0, 10), arm_l=(10, 0, -10), fore_r=(10, 0, 0), fore_l=(10, 0, 0), P_root=Z)
    L8(a, 42, Z, 0, 0)
    a.at(50, chest=Z, head=Z, arm_r=Z, arm_l=Z, fore_r=Z, fore_l=Z)
    abd(a, (0, 0, 0, 0), (12, 20, 0, 0), (18, -30, 0, 0), (34, -26, 0, 0), (44, 0, 0, 0))
    a.hair([(0, 0, 0, 0), (12, 10, 0, 0), (18, -26, 0, 0), (22, -22, 0, 6), (26, -24, 0, -6), (30, -22, 0, 4), (38, 0, 0, 0)], delay=1)
    a.cloth([(0, 0, 0, 0), (12, 4, 0, 0), (18, -10, 0, 0, 22), (30, -8, 0, 0, 18), (42, 0, 0, 0)], delay=1)
    a.done()

    # ---------------------------------------------------------------- leap_slam (52): crouch deep 0-13, LAUNCH 14 (legs trail), airborne splay 18-24, LAND 26 (legs spear down), rise
    a = mk("leap_slam", 52)
    a.at(0, chest=Z, P_root=Z)
    a.at(12, chest=(-26, 0, 0), head=(20, 0, 0), arm_r=(-30, 0, 30), arm_l=(-30, 0, -30), P_root=(0, -3.4, 0.6))
    L8(a, 12, (0, 0, 24), -40, -20)
    a.at(14, chest=(10, 0, 0), head=(4, 0, 0), arm_r=(20, 0, 60), arm_l=(20, 0, -60), P_root=(0, 1.0, 0))
    L8(a, 14, (0, -20, -30), 30, 10, lag=0)
    a.at(20, chest=(-10, 0, 0), head=(10, 0, 0), arm_r=(100, 0, 40), arm_l=(100, 0, -40), P_root=(0, 2.0, 0))
    L8(a, 20, (20, 30, 30), 40, 10, legs=(0, 1)); L8(a, 20, (0, 10, 10), 20, 10, legs=(2, 3))
    a.at(26, chest=(-34, 0, 0), head=(26, 0, 0), arm_r=(60, 0, 20), arm_l=(60, 0, -20), P_root=(0, -3.0, -0.6))
    L8(a, 26, (0, 0, -6), -34, -20, lag=0)
    a.at(30, P_root=(0, -2.6, -0.5)).at(34, chest=(-30, 0, 0), P_root=(0, -2.8, -0.6))
    a.at(42, chest=(-8, 0, 0), head=(4, 0, 0), arm_r=Z, arm_l=Z, P_root=(0, -0.4, 0))
    L8(a, 42, Z, 0, 0)
    a.at(52, chest=Z, head=Z, P_root=Z)
    abd(a, (0, 0, 0, 0), (12, 16, 0, 0), (14, -30, 0, 0), (20, -10, 0, 0), (26, 24, 0, 0), (34, 14, 0, 0), (46, 0, 0, 0))
    a.hair([(0, 0, 0, 0), (12, 10, 0, 0), (14, -24, 0, 0), (20, -10, 0, 0), (26, 26, 0, 0), (32, -6, 0, 0), (42, 0, 0, 0)], delay=1)
    a.cloth([(0, 0, 0, 0), (12, 4, 0, 0, 4), (14, -14, 0, 0), (20, -6, 0, 0, 10), (26, 12, 0, 0, 26), (34, 4, 0, 0, 10), (46, 0, 0, 0)], delay=1)
    a.done()

    # ---------------------------------------------------------------- eruption (60): front legs raised high 0-12, DRIVE into the ground 16, legs shudder, second pulse 40, pull out
    a = mk("eruption", 60)
    a.at(0, chest=Z, P_root=Z)
    a.at(12, chest=(14, 0, 0), head=(16, 0, 0), arm_r=(160, 0, 20), arm_l=(160, 0, -20), P_root=(0, 1.8, 0.4))
    L8(a, 12, (0, 20, 50), 30, 10, legs=(0, 1)); L8(a, 12, (0, 0, -6), 6, 0, legs=(2, 3))
    a.at(16, chest=(-44, 0, 0), head=(30, 0, 0), arm_r=(56, 0, 10), arm_l=(56, 0, -10), P_root=(0, -2.8, -1.2))
    L8(a, 16, (30, 40, -40), 10, -20, legs=(0, 1), lag=0); L8(a, 16, (0, 0, -12), -14, -10, legs=(2, 3), lag=0)
    for t in (20, 24, 28, 32, 36):
        j = 1 if t % 8 == 4 else -1
        a.at(t, chest=(-42, 0, 2 * j), head=(28, 3 * j, 0), P_root=(0, -2.6, -1.1))
        L8(a, t, (30, 40, -38 + 2 * j), 10, -20, legs=(0, 1), lag=0)
    a.at(39, chest=(-34, 0, 0), P_root=(0, -2.0, -1.0))
    a.at(40, chest=(-50, 0, 0), head=(34, 0, 0), P_root=(0, -3.2, -1.4))
    L8(a, 40, (30, 40, -44), 6, -24, legs=(0, 1), lag=0)
    a.scl("abdomen", (0, 1, 1, 1), (38, 1, 1, 1), (40, 1.14, 1.14, 1.14), (44, 1, 1, 1), (60, 1, 1, 1))
    a.at(50, chest=(-14, 0, 0), head=(8, 0, 0), arm_r=(30, 0, 20), arm_l=(30, 0, -20), P_root=(0, -0.6, -0.3))
    L8(a, 50, (0, 0, 20), 20, 0, legs=(0, 1)); L8(a, 56, Z, 0, 0)
    a.at(60, chest=Z, head=Z, arm_r=Z, arm_l=Z, P_root=Z)
    abd(a, (0, 0, 0, 0), (12, -20, 0, 0), (16, 20, 0, 0), (40, 26, 0, 0), (52, 0, 0, 0))
    a.hair([(0, 0, 0, 0), (12, -10, 0, 0), (16, 22, 0, 0), (22, 4, 0, 0), (40, 20, 0, 0), (46, -4, 0, 0), (56, 0, 0, 0)])
    a.cloth([(0, 0, 0, 0), (12, -6, 0, 0, 4), (16, 12, 0, 0, 22), (30, 6, 0, 0, 14), (40, 12, 0, 0, 24), (54, 0, 0, 0)])
    a.done()

    # ---------------------------------------------------------------- stomp (30): both front-mid legs lift 0-9, STOMP 12, quick recover
    a = mk("stomp", 30)
    a.at(0, chest=Z, P_root=Z)
    a.at(9, chest=(8, 0, 0), head=(10, 0, 0), arm_r=(20, 0, 30), arm_l=(20, 0, -30), P_root=(0, 1.0, 0.3))
    L8(a, 9, (20, 30, 50), 20, 10, legs=(0, 1))
    a.at(12, chest=(-22, 0, 0), head=(18, 0, 0), arm_r=(30, 0, 10), arm_l=(30, 0, -10), P_root=(0, -1.6, -0.6))
    L8(a, 12, (20, 30, -20), -10, -10, legs=(0, 1), lag=0); L8(a, 12, (0, 0, -8), -10, -6, legs=(2, 3), lag=0)
    a.at(15, P_root=(0, -1.3, -0.5)).at(22, chest=(-6, 0, 0), head=(4, 0, 0), arm_r=Z, arm_l=Z, P_root=(0, -0.2, 0))
    L8(a, 22, Z, 0, 0)
    a.at(30, chest=Z, head=Z, P_root=Z)
    abd(a, (0, 0, 0, 0), (9, -14, 0, 0), (12, 16, 0, 0), (22, 0, 0, 0))
    a.hair([(0, 0, 0, 0), (9, -6, 0, 0), (12, 16, 0, 0), (18, -4, 0, 0), (26, 0, 0, 0)], delay=1)
    a.cloth([(0, 0, 0, 0), (9, -4, 0, 0), (12, 8, 0, 0, 16), (22, 0, 0, 0)], delay=1)
    a.done()

    # ---------------------------------------------------------------- abyss (86, enraged): rear + shriek 0-8, legs spear into floor 20, throbbing pulses 34/42/50, rear high 54-62, CATACLYSM slam 66
    a = mk("abyss", 86)
    a.at(0, chest=Z, P_root=Z, root=Z)
    a.at(6, chest=(24, 0, 0), head=(30, 0, 0), arm_r=(20, 0, 100), arm_l=(20, 0, -100), P_root=(0, 1.4, 0.4))
    L8(a, 6, (0, 0, 30), 40, 20, legs=(0, 1)); L8(a, 6, (0, 0, 10), 20, 10, legs=(2, 3))
    a.at(14, chest=(18, 0, 0), head=(26, 0, 0), P_root=(0, 2.0, 0.4))
    L8(a, 14, (0, 0, 44), 30, 10)
    a.at(20, chest=(-36, 0, 0), head=(26, 0, 0), arm_r=(50, 0, 20), arm_l=(50, 0, -20), P_root=(0, -2.6, -0.8))
    L8(a, 20, (0, 0, -16), -24, -20, lag=0)
    for t in (34, 42, 50):
        a.at(t - 2, chest=(-30, 0, 0), P_root=(0, -2.2, -0.7))
        a.at(t, chest=(-42, 0, 0), head=(32, 0, 0), P_root=(0, -3.0, -0.9))
        L8(a, t - 2, (0, 0, -12), -22, -20, lag=0); L8(a, t, (0, 0, -18), -26, -22, lag=0)
    a.scl("abdomen", (0, 1, 1, 1), (32, 1, 1, 1), (34, 1.12, 1.12, 1.12), (38, 1, 1, 1), (42, 1.16, 1.16, 1.16), (46, 1, 1, 1), (50, 1.2, 1.2, 1.2),
          (56, 1.05, 1.05, 1.05), (66, 1.2, 1.2, 1.2), (72, 1, 1, 1), (86, 1, 1, 1))
    a.at(58, root=(18, 0, 0), chest=(16, 0, 0), head=(14, 0, 0), arm_r=(170, 0, 30), arm_l=(170, 0, -30), P_root=(0, 4.0, 1.8))
    L8(a, 58, (0, 20, 50), 40, 10, legs=(0, 1)); L8(a, 58, (0, -10, -14), -12, -8, legs=(2, 3))
    a.at(63, root=(20, 0, 0), P_root=(0, 4.4, 2.0))
    a.at(66, root=(-16, 0, 0), chest=(-40, 0, 0), head=(30, 0, 0), arm_r=(50, 0, 10), arm_l=(50, 0, -10), P_root=(0, -1.5, -1.8))
    L8(a, 66, (40, 60, -30), 30, -10, legs=(0, 1), lag=0); L8(a, 66, (0, 0, -14), -16, -10, legs=(2, 3), lag=0)
    a.at(70, root=(-13, 0, 0), P_root=(0, -1.2, -1.6)).at(74, root=(-15, 0, 0), P_root=(0, -1.4, -1.7))
    a.at(80, root=(-4, 0, 0), chest=(-10, 0, 0), head=(6, 0, 0), arm_r=(20, 0, 10), arm_l=(20, 0, -10), P_root=(0, -0.6, -0.4))
    L8(a, 80, Z, 0, 0)
    a.at(86, root=Z, chest=Z, head=Z, arm_r=Z, arm_l=Z, P_root=Z)
    abd(a, (0, 0, 0, 0), (6, -26, 0, 0), (20, 16, 0, 0), (50, 20, 0, 0), (58, -30, 0, 0), (66, 26, 0, 0), (80, 0, 0, 0))
    a.hair([(0, 0, 0, 0), (6, -24, 0, 0), (14, -10, 0, 0), (20, 20, 0, 0), (34, 10, 0, 0), (42, 10, 0, 0), (50, 10, 0, 0), (58, -12, 0, 0), (66, 26, 0, 0), (74, -4, 0, 0), (84, 0, 0, 0)], delay=1)
    a.cloth([(0, 0, 0, 0), (6, -8, 0, 0, 16), (20, 10, 0, 0, 20), (50, 6, 0, 0, 14), (58, -8, 0, 0, 4), (66, 12, 0, 0, 26), (80, 0, 0, 0)], delay=1)
    a.done()

    # ---------------------------------------------------------------- transform (130; boss model plays 90-130): curled ball at 90, legs unfurl 90-104, inhale 108, ROAR 112, settle
    a = mk("transform", 130)
    a.scl("root", (0, 0.5, 0.5, 0.5), (90, 0.5, 0.5, 0.5), (96, 0.75, 0.75, 0.75), (104, 1.0, 1.0, 1.0), (112, 1.06, 1.06, 1.06), (118, 1.0, 1.0, 1.0), (130, 1, 1, 1))
    ball = dict(chest=(-50, 0, 0), head=(-10, 0, 0), arm_r=(120, 40, 20), arm_l=(120, -40, -20), fore_r=(110, 0, 0), fore_l=(110, 0, 0), P_root=(0, -3.0, 0))
    a.at(0, **ball); a.at(90, **ball)
    L8(a, 0, (0, 0, -40), -60, -40, lag=0); L8(a, 90, (0, 0, -40), -60, -40, lag=0)
    a.at(98, chest=(-20, 0, 0), head=(10, 0, 0), arm_r=(40, 0, 60), arm_l=(40, 0, -60), fore_r=(40, 0, 0), fore_l=(40, 0, 0), P_root=(0, -1.0, 0))
    L8(a, 98, (0, 0, -10), -20, -10)
    a.at(106, chest=(-24, 0, 0), head=(-10, 0, 0), arm_r=(60, 30, 30), arm_l=(60, -30, -30), fore_r=(90, 0, 0), fore_l=(90, 0, 0), P_root=(0, 0.6, 0.6))
    L8(a, 106, (0, 0, -16), -20, -10)
    a.at(112, chest=(24, 0, 0), head=(30, 0, 0), arm_r=(30, 0, 110), arm_l=(30, 0, -110), fore_r=(-10, 0, 0), fore_l=(-10, 0, 0), P_root=(0, 1.0, -0.6))
    L8(a, 112, (0, 0, 30), 40, 20, legs=(0, 1), lag=0); L8(a, 112, (0, 0, 10), 20, 10, legs=(2, 3), lag=0)
    for t in range(114, 124, 2):
        j = 1 if t % 4 == 0 else -1
        a.at(t, chest=(22, 2 * j, 2 * j), head=(28, 4 * j, -3 * j), arm_r=(30, 0, 106 + 4 * j), arm_l=(30, 0, -106 + 4 * j))
    a.at(130, chest=Z, head=Z, arm_r=Z, arm_l=Z, fore_r=Z, fore_l=Z, P_root=Z)
    L8(a, 124, (0, 0, 20), 30, 10, legs=(0, 1)); L8(a, 130, Z, 0, 0)
    abd(a, (0, 40, 0, 0), (90, 40, 0, 0), (104, 0, 0, 0), (112, -26, 0, 0), (124, -20, 0, 0), (130, 0, 0, 0))
    a.hair([(0, 10, 0, 0), (90, 10, 0, 0), (100, -10, 0, 0), (106, 10, 0, 0), (112, -30, 0, 0), (116, -26, 0, 8), (120, -30, 0, -8), (126, -10, 0, 0), (130, 0, 0, 0)], delay=1)
    a.cloth([(0, 10, 0, 0, 30), (90, 10, 0, 0, 30), (100, -6, 0, 0, 10), (112, -16, 0, 0, 26), (124, -14, 0, 0, 20), (130, 0, 0, 0)], delay=1)
    a.done()

    # ---------------------------------------------------------------- death (40): convulse 0-8, legs curl inward (dead spider) 8-26, body sinks and tips back, melts flat 30-40
    a = mk("death", 40)
    a.at(0, chest=Z, head=Z, P_root=Z, root=Z)
    a.at(4, chest=(24, 0, 0), head=(36, 0, 0), arm_r=(20, 0, 100), arm_l=(20, 0, -100), P_root=(0, 0.8, 0))
    L8(a, 4, (0, 0, 30), 40, 20, lag=0)
    a.at(8, chest=(18, 0, 4), head=(30, 6, 6))
    a.at(16, chest=(-30, 0, 0), head=(20, 0, -16), arm_r=(60, 30, 10), arm_l=(60, -30, -10), fore_r=(80, 0, 0), fore_l=(80, 0, 0), P_root=(0, -3.0, 0))
    L8(a, 16, (0, 0, -20), -50, -30)
    a.at(26, root=(-30, 0, 0), chest=(-20, 0, 0), head=(10, 0, -20), P_root=(0, -4.0, 2.0))
    L8(a, 26, (0, 0, -50), -80, -50)
    a.at(40, root=(-36, 0, 0), P_root=(0, -4.6, 2.4))
    L8(a, 40, (0, 0, -60), -90, -60)
    a.scl("root", (0, 1, 1, 1), (30, 1, 1, 1), (40, 1.1, 0.25, 1.1))
    abd(a, (0, 0, 0, 0), (4, -30, 0, 0), (16, 20, 0, 0), (40, 30, 0, 0))
    a.hair([(0, 0, 0, 0), (4, -24, 0, 0), (16, 16, 0, 0), (26, 20, 0, 10), (40, 10, 0, 10)], delay=2)
    a.cloth([(0, 0, 0, 0), (4, -10, 0, 0, 20), (16, 10, 0, 0, 24), (26, -10, 0, 0, 10), (40, -10, 0, 0, 10)])
    a.done()


if __name__ == "__main__":
    b1 = Builder("green_alice", 1.0, False, 8)
    build(b1)
    anims_p1(b1)
    b1.m.save(DIR + "green_alice.bbmodel")
    print("green_alice cubes", len(b1.m.cubes))
    b2 = Builder("green_alice_boss", 2.8, True, 3)
    build(b2)
    anims_p2(b2)
    b2.m.save(DIR + "green_alice_boss.bbmodel")
    print("green_alice_boss cubes", len(b2.m.cubes))
