"""Infected Bloomie - generates assets/fpe/bbmodels/infected_bloomie.bbmodel.
References (only these are trusted): docs/ref/confirmed/infected_bloomie_window.jpg / _3d.jpg / _note.jpg.
Tall spindly pitch-black monster: small hunched ribcage torso, skull head with two huge hollow round eyes (pale glow),
ragged hair tufts + a forehead horn, long drooling under-jaw with jagged teeth and ink drool strands, very long thin
forelimbs ending in three long claw fingers that reach the ground, long digitigrade hind legs with claw toes, and two
mantis-like blade arms rising from the back: a segmented serrated "saw" (her right) and a long straight knife (her left).
Hitbox 1.3 x 3.2 blocks -> body ~51 px; the blades tower slightly above.
Blockbench space: Y up, ground 0, faces -Z, character's RIGHT = +X.  Animation rotations are OFFSETS from the built rest pose.
Signs: hanging limb rx>0 swings forward; upward part (torso/blade) rx>0 tilts back, rx<0 tilts forward;
rz>0: hanging part swings toward +X (upward part tilts toward -X). ry>0 turns to her left.
Run: python3 tools/bbgen/chars/infected_bloomie.py
"""
import math, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))
from bbgen import mix  # noqa: E402
from alice import Builder, A, combo  # noqa: E402

DIR = os.path.join(os.path.dirname(__file__), "../../../src/main/resources/assets/fpe/bbmodels/")


class Pal:
    pass


C = Pal()
C.BLK, C.BLK_D, C.BLK_HI = 0x15141B, 0x09090C, 0x302E3C
C.RIB, C.RIB_D = 0x34323F, 0x0D0C11
C.CLAW, C.CLAW_HI = 0x0B0B0E, 0x4A4858
C.EYE, C.EYE_D, C.PUPIL = 0xF2F0FF, 0xA8A6C8, 0xFFFFFF
C.TEETH, C.TEETH_D = 0xD9D4C8, 0x8A857C
C.MOUTH = 0x2A0A12
C.DROOL, C.DROOL_HI = 0x050507, 0x55536A
C.STEEL, C.STEEL_D, C.STEEL_HI = 0xA4A6B2, 0x5E6070, 0xE2E4EE
C.SAW, C.SAW_D = 0x4A4856, 0x22212A


# ================================================================== painters
def skin(B, base=None, dark=None, hi=None, streak=0.12):
    R = B.R
    base, dark, hi = base or C.BLK, dark or C.BLK_D, hi or C.BLK_HI

    def f(F):
        for y in range(F.h):
            for x in range(F.w):
                r = R.random()
                c = mix(base, dark, 0.35 * (y / max(1, F.h - 1)))
                if r < streak: c = mix(c, hi, 0.5)
                elif r > 0.93: c = dark
                F.px(x, y, c)
        for _ in range(max(1, F.w // 5)):  # sinew lines
            x = R.randint(0, max(0, F.w - 1))
            for y in range(F.h):
                if R.random() < 0.8: F.px(x, y, mix(base, hi, 0.35))
    return f


def ribs(B):
    def f(F):
        skin(B)(F)
        n = max(3, F.h // 5)
        for i in range(n):
            y = int((i + 0.6) * F.h / (n + 0.4))
            for x in range(F.w):
                cx = abs(x - F.w / 2) / (F.w / 2)
                yy = y + int(cx * 2)
                F.px(x, yy, C.RIB); F.px(x, yy + 1, C.RIB_D)
        F.rect(F.w // 2, 0, 1, F.h, C.BLK_D)  # sternum split
    return f


def face(B):
    def f(F):
        W, H = F.w, F.h
        skin(B, streak=0.06)(F)
        for cx in (0.28 * W, 0.72 * W):
            cy = 0.5 * H
            F.disc(cx, cy, 0.27 * W, C.BLK_D)
            F.disc(cx, cy, 0.235 * W, C.EYE, glow=True)
            F.disc(cx, cy, 0.18 * W, C.EYE_D, glow=True)
            F.disc(cx, cy, 0.13 * W, 0x060608)
            F.disc(cx + (0.03 * W if cx < W / 2 else -0.03 * W), cy + 0.02 * H, 0.04 * W, C.PUPIL, glow=True)
        F.line(0.5 * W, 0.25 * H, 0.5 * W, 0.42 * H, C.BLK_D, 1)  # brow crease
        F.line(0.05 * W, 0.15 * H, 0.45 * W, 0.24 * H, C.BLK_HI, 1)
        F.line(0.95 * W, 0.15 * H, 0.55 * W, 0.24 * H, C.BLK_HI, 1)
        for x in (0.1, 0.9):  # ink tear streaks under the eyes
            F.line(x * W + (2 if x < .5 else -2), 0.72 * H, x * W + (2 if x < .5 else -2), H, C.DROOL, 1)
    return f


def teeth_row(n):
    def f(F):
        F.rect(0, 0, F.w, F.h, C.MOUTH)
        tw = F.w / n
        for i in range(n):
            x0 = i * tw
            F.poly([(x0, 0), (x0 + tw, 0), (x0 + tw * 0.5, F.h)], C.TEETH)
            F.line(x0 + tw * 0.5, 0, x0 + tw * 0.5, F.h * 0.6, C.TEETH_D, 1)
    return f


def teeth_up(n):
    def f(F):
        F.rect(0, 0, F.w, F.h, C.MOUTH)
        tw = F.w / n
        for i in range(n):
            x0 = i * tw
            F.poly([(x0, F.h), (x0 + tw, F.h), (x0 + tw * 0.5, 0)], C.TEETH)
    return f


def steel(edge_side=None):
    def f(F):
        for y in range(F.h):
            for x in range(F.w):
                u = x / max(1, F.w - 1)
                F.px(x, y, mix(C.STEEL_D, C.STEEL, min(1, u * 1.6)) if u < 0.75 else mix(C.STEEL, C.STEEL_HI, (u - 0.75) * 4))
        for y in range(0, F.h, 5):  # nicks / grime
            F.px(F.w - 1, y, C.STEEL_D); F.px(F.w // 3, y + 2, mix(C.STEEL_D, C.BLK, 0.5))
        F.rect(0, 0, 1, F.h, C.BLK)
    return f


def saw_p(B):
    def f(F):
        skin(B, C.SAW, C.SAW_D, C.STEEL_D, 0.1)(F)
        F.rect(F.w - 1, 0, 1, F.h, C.STEEL)
        for y in range(0, F.h, 3):
            F.px(F.w - 2, y, C.STEEL_HI)
    return f


def drool_p(F):
    for y in range(F.h):
        for x in range(F.w):
            F.px(x, y, C.DROOL_HI if x == 0 and y % 4 < 2 else C.DROOL)


def claw_p(F):
    for y in range(F.h):
        for x in range(F.w):
            F.px(x, y, mix(C.CLAW, C.CLAW_HI, 0.5 * (y / max(1, F.h - 1))) if x != 0 else C.CLAW_HI)


# ================================================================== model
ARM = {"arm_r": (98, 0, 14), "arm_l": (98, 0, -14), "fore_r": (-14, 0, 0), "fore_l": (-14, 0, 0),
       "hand_r": (-44, 0, 0), "hand_l": (-44, 0, 0)}


def build(B):
    g, c, blade, lock = B.g, B.c, B.blade, B.lock
    sk = skin(B)
    st = B.strands(C.BLK, C.BLK_HI, C.BLK_D, ink=C.BLK_D)

    def S(fn):
        return B.all(fn)

    g("root", (0, 0, 0))
    g("pelvis", (0, 29, 2), "root")
    c("hipbone", "pelvis", (-2.6, 27.4, 0.2), (2.6, 30.6, 4.2), C.BLK, faces=S(sk))
    c("tailbone", "pelvis", (-0.8, 26.2, 3.2), (0.8, 28.4, 5.2), C.BLK_D, rot=(30, 0, 0), origin=(0, 28, 4))
    for s, k in ((1, "r"), (-1, "l")):
        c("hipknob_" + k, "pelvis", (2.2 * s - 0.9, 27.6, 1.0), (2.2 * s + 0.9, 29.8, 3.4), C.BLK_HI)

    # ---------------- torso (built upward, leaned forward by the group)
    g("body", (0, 29.5, 2), "pelvis", rot=(-58, 0, 0))
    c("waist", "body", (-1.6, 29.5, 0.8), (1.6, 34.5, 3.4), C.BLK, faces=S(sk))
    c("ribcage", "body", (-3.3, 33.6, -0.6), (3.3, 41.2, 4.0), C.BLK, faces={**S(sk), "north": ribs(B), "east": ribs(B), "west": ribs(B)})
    c("chestplate", "body", (-2.4, 35, -1.1), (2.4, 40.6, -0.5), C.BLK_D, faces={"north": ribs(B)})
    for i in range(7):  # spine ridges
        y = 30 + i * 1.7
        c(f"spine{i}", "body", (-0.6, y, 3.6 if y > 33.5 else 3.0), (0.6, y + 1.0, 5.0 if y > 33.5 else 4.4), C.BLK_HI, rot=(-25, 0, 0), origin=(0, y, 4))
    for s, k in ((1, "r"), (-1, "l")):
        c("shoulder_" + k, "body", (3.6 * s - 1.4, 38.6, 0.2), (3.6 * s + 1.4, 41.6, 3.0), C.BLK, faces=S(sk))
        c("scap_" + k, "body", (1.4 * s - 1.2, 37, 3.8), (1.4 * s + 1.2, 41, 4.6), C.BLK_HI, rot=(0, 0, -12 * s), origin=(1.4 * s, 39, 4.2))
    # shoulder fur tufts
    g("mane", (0, 41, 3), "body")
    for i, (x, rx, rz, ln) in enumerate(((-1.6, 30, 30, 4.5), (0, 40, 0, 5.5), (1.6, 30, -30, 4.5), (-2.8, 10, 55, 3.5), (2.8, 10, -55, 3.5))):
        blade(f"mane{i}", "mane", (x, 40.6, 3.4), ln, 1.0, 0.5, (rx, 0, rz), C.BLK, tip=C.BLK_D, paint=st)
    # belly strands (ragged hair hanging from the ribcage)
    g("strands_b", (0, 34, 0), "body", rot=(58, 0, 0))
    for i, x in enumerate((-2.2, -0.6, 1.0, 2.4)):
        lock(f"bs{i}", "strands_b", (x, 34, -0.3), 4.5 + (i % 2) * 2, 0.9, 0.4, (0, 0, (i - 1.5) * 6), C.BLK, tip=C.BLK_D, paint=st)

    # ---------------- neck / head / jaw
    g("neck", (0, 41, 1.6), "body", rot=(26, 0, 0))
    c("neck0", "neck", (-1.1, 40.8, 0.6), (1.1, 44.2, 2.8), C.BLK, faces=S(sk))
    c("neckridge", "neck", (-0.5, 41, 2.6), (0.5, 44, 3.4), C.BLK_HI)
    g("head", (0, 44, 1.6), "neck", rot=(26, 0, 0))
    c("cranium", "head", (-3.4, 44.4, -3.6), (3.4, 50.2, 3.2), C.BLK, faces={**S(sk), "north": face(B)})
    c("skulltop", "head", (-2.8, 50.0, -2.8), (2.8, 51.0, 2.6), C.BLK_D)
    c("brow", "head", (-3.6, 48.6, -4.2), (3.6, 49.5, -3.4), C.BLK_D, rot=(-10, 0, 0))
    for s, k in ((1, "r"), (-1, "l")):
        c("cheek_" + k, "head", (3.0 * s - 0.8, 44.0, -3.4), (3.0 * s + 0.8, 46.4, 0.4), C.BLK_HI)
        c("ear_" + k, "head", (3.4 * s - 0.4, 46, 0.2), (3.4 * s + 0.4, 48.6, 1.8), C.BLK_D)
    c("snout", "head", (-2.4, 43.0, -5.0), (2.4, 45.0, -2.6), C.BLK, faces={**S(sk), "down": teeth_row(6)})
    c("upteeth", "head", (-2.3, 42.0, -4.9), (2.3, 43.0, -2.8), C.TEETH, faces={"north": teeth_row(6), "east": teeth_row(3), "west": teeth_row(3)})
    c("nose", "head", (-0.9, 44.3, -5.3), (0.9, 45.0, -4.6), C.BLK_D, faces={"north": lambda F: (F.rect(0, 0, F.w, F.h, C.BLK_D), F.rect(1, 1, 2, F.h - 1, 0), F.rect(F.w - 3, 1, 2, F.h - 1, 0))})
    blade("horn", "head", (0, 50.6, -2.6), 4.0, 1.2, 1.2, (-28, 0, 0), C.BLK, tip=C.CLAW_HI)
    # hair tufts
    for grp, org in (("hair_t", (0, 50.5, 0)), ("hair_b", (0, 49, 3)), ("hair_r", (3.2, 48.5, 0)), ("hair_l", (-3.2, 48.5, 0))):
        g(grp, org, "head")
    tufts = [("hair_t", (-1.6, 50.6, -0.6), 5.0, (40, 0, 30)), ("hair_t", (1.4, 50.6, -0.2), 5.5, (45, 0, -28)),
             ("hair_t", (0, 50.6, 0.6), 6.0, (55, 0, 4)), ("hair_t", (-2.6, 50.2, 1.2), 4.0, (30, 0, 58)),
             ("hair_t", (2.6, 50.2, 1.0), 4.5, (35, 0, -60)), ("hair_b", (-1.2, 49.5, 3.0), 5.0, (78, 0, 14)),
             ("hair_b", (1.2, 49.3, 3.0), 5.5, (82, 0, -12)), ("hair_b", (0, 47.5, 3.0), 4.0, (100, 0, 0))]
    for i, (grp, base, ln, rot) in enumerate(tufts):
        blade(f"tuft{i}", grp, base, ln, 1.3, 0.7, rot, C.BLK, tip=C.BLK_D, paint=st)
    for i, (grp, x, rz) in enumerate((("hair_r", 3.3, 18), ("hair_r", 3.4, 34), ("hair_l", -3.3, -18), ("hair_l", -3.4, -34))):
        lock(f"side{i}", grp, (x, 48.8 - (i % 2) * 1.2, -1.0 + (i % 2) * 1.6), 4.5 + (i % 2), 1.0, 0.6, (8, 0, rz), C.BLK, tip=C.BLK_D, paint=st)
    lock("fringe0", "hair_t", (-1.8, 49.8, -3.7), 3.0, 1.0, 0.4, (-12, 0, -6), C.BLK, tip=C.BLK_D, paint=st)
    lock("fringe1", "hair_t", (1.9, 49.8, -3.7), 2.4, 0.9, 0.4, (-12, 0, 8), C.BLK, tip=C.BLK_D, paint=st)

    g("jaw", (0, 44.4, 0.8), "head", rot=(-14, 0, 0))
    c("jawbone", "jaw", (-2.5, 40.6, -5.6), (2.5, 42.4, 0.6), C.BLK, faces={**S(sk), "up": lambda F: F.rect(0, 0, F.w, F.h, C.MOUTH)})
    c("chin", "jaw", (-1.6, 39.4, -5.8), (1.6, 40.8, -3.2), C.BLK_D)
    c("lowteeth", "jaw", (-2.3, 42.4, -5.5), (2.3, 43.4, -3.0), C.TEETH, faces={"north": teeth_up(6), "east": teeth_up(3), "west": teeth_up(3)})
    c("fang_r", "jaw", (1.6, 42.4, -5.6), (2.2, 44.2, -5.0), C.TEETH, rot=(0, 0, -8), origin=(1.9, 42.4, -5.3))
    c("fang_l", "jaw", (-2.2, 42.4, -5.6), (-1.6, 44.2, -5.0), C.TEETH, rot=(0, 0, 8), origin=(-1.9, 42.4, -5.3))
    c("tongue", "jaw", (-1.0, 42.2, -4.6), (1.0, 42.7, 0), C.MOUTH)
    # drool strands (3 chains of 3 links)
    for k, (x, z, ln) in (("a", (-1.4, -5.3, 3.2)), ("b", (0.6, -5.6, 4.0)), ("c", (1.9, -4.6, 2.6))):
        y = 40.0
        parent = "jaw"
        for j in range(3):
            gn = f"drool_{k}{j}"
            g(gn, (x, y, z), parent)
            w = 0.7 - j * 0.15
            c(gn, gn, (x - w / 2, y - ln, z - w / 2), (x + w / 2, y, z + w / 2), C.DROOL, faces=S(drool_p))
            parent, y = gn, y - ln
        c(f"drop_{k}", parent, (x - 0.45, y - 0.8, z - 0.45), (x + 0.45, y, z + 0.45), C.DROOL_HI)

    # ---------------- forelimbs (built hanging, rest rotation brings them to the ground)
    for s, k in ((1, "r"), (-1, "l")):
        x = 3.8 * s
        g("arm_" + k, (x, 40, 1.6), "body", rot=ARM["arm_" + k])
        c("upper_" + k, "arm_" + k, (x - 0.8, 27, 0.8), (x + 0.8, 40, 2.4), C.BLK, faces=S(sk))
        c("bicep_" + k, "arm_" + k, (x - 1.0, 33, 0.6), (x + 1.0, 38.5, 2.4), C.BLK_D)
        g("fore_" + k, (x, 27, 1.6), "arm_" + k, rot=ARM["fore_" + k])
        c("elbow_" + k, "fore_" + k, (x - 1.0, 26, 1.4), (x + 1.0, 28.2, 3.2), C.BLK_HI)
        c("forearm_" + k, "fore_" + k, (x - 0.65, 13, 0.95), (x + 0.65, 27, 2.25), C.BLK, faces=S(sk))
        c("wrist_" + k, "fore_" + k, (x - 0.8, 12.6, 0.8), (x + 0.8, 14.2, 2.4), C.BLK_D)
        g("fstr_" + k, (x, 26.5, 2.8), "fore_" + k)
        for i in range(3):
            lock(f"fs{i}_{k}", "fstr_" + k, (x + (i - 1) * 0.5 * s, 26.5 - i * 2.2, 2.6), 4.0 - i * 0.6, 0.8, 0.35, (-20, 0, 0), C.BLK, tip=C.BLK_D, paint=st)
        g("hand_" + k, (x, 13, 1.6), "fore_" + k, rot=ARM["hand_" + k])
        c("palm_" + k, "hand_" + k, (x - 1.2, 11, 0.8), (x + 1.2, 13, 2.6), C.BLK, faces=S(sk))
        for i, (dx, dz, sp) in enumerate(((-1.0, 0.2, -10), (0, 0.0, 0), (1.0, 0.2, 10))):
            fn = f"fing{i}_{k}"
            fx = x + dx * s
            g(fn, (fx, 11, 1.4 + dz), "hand_" + k, rot=(0, 0, sp * s))
            c(fn + "a", fn, (fx - 0.35, 7.0, 1.05 + dz), (fx + 0.35, 11, 1.75 + dz), C.BLK, faces=S(sk))
            g(fn + "t", (fx, 7.0, 1.4 + dz), fn, rot=(16, 0, 0))
            c(fn + "b", fn + "t", (fx - 0.28, 3.2, 1.12 + dz), (fx + 0.28, 7.1, 1.68 + dz), C.CLAW, faces=S(claw_p))
            c(fn + "c", fn + "t", (fx - 0.14, 1.4, 1.26 + dz), (fx + 0.14, 3.3, 1.54 + dz), C.CLAW_HI, rot=(14, 0, 0), origin=(fx, 3.3, 1.4 + dz))
        c("thumb_" + k, "hand_" + k, (x - 0.25, 8.6, 0.0), (x + 0.25, 11.4, 0.6), C.CLAW, rot=(-30, 0, 0), origin=(x, 11, 0.4))

    # ---------------- hind legs (long, digitigrade, splayed)
    for s, k in ((1, "r"), (-1, "l")):
        x = 2.4 * s
        g("leg_" + k, (x, 29, 2), "pelvis", rot=(30, 0, 17 * s))
        c("thigh_" + k, "leg_" + k, (x - 1.1, 17, 1.0), (x + 1.1, 29.4, 3.0), C.BLK, faces=S(sk))
        c("thighm_" + k, "leg_" + k, (x - 1.3, 22, 0.8), (x + 1.3, 28, 3.2), C.BLK_D)
        g("shin_" + k, (x, 17, 2), "leg_" + k, rot=(-62, 0, 0))
        c("knee_" + k, "shin_" + k, (x - 1.0, 16, 0.8), (x + 1.0, 18.2, 2.8), C.BLK_HI)
        c("shin_" + k, "shin_" + k, (x - 0.6, 4, 1.4), (x + 0.6, 17, 2.6), C.BLK, faces=S(sk))
        c("calfspur_" + k, "shin_" + k, (x - 0.3, 12, 2.4), (x + 0.3, 15, 3.4), C.BLK_D, rot=(20, 0, 0), origin=(x, 13.5, 2.6))
        g("ank_" + k, (x, 4, 2), "shin_" + k, rot=(38, 0, 0))
        c("heel_" + k, "ank_" + k, (x - 0.8, 3.0, 1.2), (x + 0.8, 4.8, 2.8), C.BLK_HI)
        c("meta_" + k, "ank_" + k, (x - 0.5, -2.6, 1.5), (x + 0.5, 4, 2.5), C.BLK, faces=S(sk))
        g("foot_" + k, (x, -2.6, 2), "ank_" + k, rot=(-6, 0, 0))
        c("pad_" + k, "foot_" + k, (x - 1.1, -3.4, 0.6), (x + 1.1, -2.2, 2.8), C.BLK_D)
        for i, (dx, ry) in enumerate(((-0.8, 18), (0, 0), (0.8, -18))):
            tn = f"toe{i}_{k}"
            tx = x + dx * s
            c(tn + "a", "foot_" + k, (tx - 0.3, -3.3, -2.2), (tx + 0.3, -2.7, 1.0), C.BLK, rot=(0, ry * s, 0), origin=(tx, -3, 1.0))
            c(tn + "b", "foot_" + k, (tx - 0.2, -3.6, -4.6), (tx + 0.2, -3.0, -2.0), C.CLAW, rot=(0, ry * s, 0), origin=(tx, -3, 1.0), faces=S(claw_p))
        c("spur_" + k, "foot_" + k, (x - 0.2, -3.4, 2.6), (x + 0.2, -2.8, 4.4), C.CLAW, rot=(-10, 0, 0), origin=(x, -3, 2.6))

    # ---------------- back blade arms
    # saw (her right, +X): 3 joints, the tip is a curled serrated chain of plates
    g("saw_a", (1.8, 40, 4), "body", rot=(84, 0, -22))
    c("saw_a", "saw_a", (1.1, 40, 3.3), (2.5, 49, 4.7), C.BLK, faces=S(sk))
    c("saw_aj", "saw_a", (0.9, 48.2, 3.1), (2.7, 50, 4.9), C.BLK_HI)
    g("saw_b", (1.8, 49, 4), "saw_a", rot=(-60, 0, 0))
    c("saw_b", "saw_b", (1.25, 49, 3.45), (2.35, 57, 4.55), C.BLK, faces=S(sk))
    c("saw_bj", "saw_b", (1.0, 56.4, 3.2), (2.6, 58, 4.8), C.BLK_HI)
    parent, y = "saw_b", 57.5
    for i in range(5):
        gn = f"saw_s{i}"
        g(gn, (1.8, y, 4), parent, rot=(-24 if i else -40, 0, 0))
        c(gn, gn, (1.3, y, 2.2), (2.3, y + 3.4, 5.0), C.SAW, faces=S(saw_p(B)))
        for j in range(2):
            c(f"{gn}t{j}", gn, (1.5, y + 0.4 + j * 1.6, 0.9), (2.1, y + 1.4 + j * 1.6, 2.3), C.STEEL_HI, rot=(-30, 0, 0), origin=(1.8, y + 0.9 + j * 1.6, 2.2))
        parent, y = gn, y + 3.4
    # knife (her left, -X): long straight blade with jagged back
    g("knife_a", (-1.8, 40, 4), "body", rot=(80, 0, 20))
    c("knife_a", "knife_a", (-2.5, 40, 3.3), (-1.1, 49.5, 4.7), C.BLK, faces=S(sk))
    c("knife_aj", "knife_a", (-2.7, 48.6, 3.1), (-0.9, 50.4, 4.9), C.BLK_HI)
    g("knife_b", (-1.8, 49.5, 4), "knife_a", rot=(-38, 0, 0))
    c("knife_b", "knife_b", (-2.35, 49.5, 3.45), (-1.25, 56.5, 4.55), C.BLK, faces=S(sk))
    g("knife", (-1.8, 56.5, 4), "knife_b", rot=(-30, 0, 0))
    c("k_hilt", "knife", (-2.6, 56.2, 3.0), (-1.0, 58.2, 5.0), C.BLK_D)
    c("k_blade", "knife", (-2.0, 58, 2.2), (-1.6, 72, 5.4), C.STEEL, faces={"east": steel(), "west": steel(), "north": lambda F: F.rect(0, 0, F.w, F.h, C.STEEL_HI), "south": lambda F: F.rect(0, 0, F.w, F.h, C.STEEL_D)})
    c("k_tip", "knife", (-1.95, 71.8, 2.8), (-1.65, 75, 4.6), C.STEEL_HI, rot=(-14, 0, 0), origin=(-1.8, 72, 3.6))
    for j in range(4):
        c(f"k_notch{j}", "knife", (-2.05, 60 + j * 3, 5.2), (-1.55, 61.2 + j * 3, 6.0), C.STEEL_D, rot=(35, 0, 0), origin=(-1.8, 60.5 + j * 3, 5.4))
    for j in range(3):  # rag strips hanging from the knife joint
        lock(f"krag{j}", "knife_b", (-1.8 + (j - 1) * 0.5, 50 + j * 2.0, 3.4), 3.6, 0.7, 0.3, (30, 0, 10), C.BLK, tip=C.BLK_D, paint=st)


# ================================================================== animation
REST = {}  # offsets from the built pose (built pose = rest)


class IB(A):
    def blades(self, t, saw=(0, 0, 0), knife=(0, 0, 0), sb=(0, 0, 0), kb=(0, 0, 0), curl=0, kn=(0, 0, 0)):
        self.at(t, saw_a=saw, knife_a=knife, saw_b=sb, knife_b=kb, knife=kn)
        return self

    def curl(self, keys, delay=1):
        """saw chain curl (x<0 curls further forward), lagging plate by plate"""
        for i in range(5):
            self.drape(f"saw_s{i}", [(t, x * (0.6 + 0.15 * i), 0, z) for (t, x, z) in keys], delay * i)
        return self

    def claws(self, t, curl=0, spread=0, side=None):
        for k in (("r", "l") if side is None else (side,)):
            for i in range(3):
                sp = (i - 1) * spread * (1 if k == "r" else -1)
                self.rot(f"fing{i}_{k}", (t, curl, 0, sp))
                self.rot(f"fing{i}_{k}t", (t, curl * 0.8, 0, 0))
        return self

    def sec(self, keys, delay=2):
        """secondary motion from a body-motion signal: x = lurch forward(+)/back, z = sway toward +X"""
        for k, gain in (("a", 1.0), ("b", 1.2), ("c", 0.9)):
            for j in range(3):
                self.drape(f"drool_{k}{j}", [(t, -x * gain * (0.8 + 0.3 * j), 0, z * gain * (0.8 + 0.3 * j)) for (t, x, z) in keys], delay + j)
        self.drape("hair_t", [(t, -x * 0.5, 0, z * 0.5) for (t, x, z) in keys], delay)
        self.drape("hair_b", [(t, -x * 0.7, 0, z * 0.4) for (t, x, z) in keys], delay + 1)
        self.drape("hair_r", [(t, x * 0.3, 0, z * 0.6 + abs(x) * 0.2) for (t, x, z) in keys], delay)
        self.drape("hair_l", [(t, x * 0.3, 0, z * 0.6 - abs(x) * 0.2) for (t, x, z) in keys], delay)
        self.drape("mane", [(t, -x * 0.5, 0, z * 0.4) for (t, x, z) in keys], delay)
        self.drape("strands_b", [(t, -x * 0.8, 0, z * 0.8) for (t, x, z) in keys], delay)
        for s in ("r", "l"):
            self.drape("fstr_" + s, [(t, -x * 0.7, 0, z * 0.7) for (t, x, z) in keys], delay + 1)
        self.curl([(t, -abs(x) * 0.5, z * 0.3) for (t, x, z) in keys], 1)
        return self

    def legs(self, t, r=(0, 0, 0), l=(0, 0, 0), sr=(0, 0, 0), sl=(0, 0, 0), ar=(0, 0, 0), al=(0, 0, 0), fr=(0, 0, 0), fl=(0, 0, 0)):
        self.at(t, leg_r=r, leg_l=l, shin_r=sr, shin_l=sl, ank_r=ar, ank_l=al, foot_r=fr, foot_l=fl)
        return self

    def crouch(self, t, d, lean=0):
        """bend both hind legs: d>0 lowers the pelvis by ~d px (legs fold at knee/ankle)"""
        k = d * 4.0
        self.legs(t, r=(k, 0, 0), l=(k, 0, 0), sr=(-k * 1.6, 0, 0), sl=(-k * 1.6, 0, 0), ar=(k * 1.0, 0, 0), al=(k * 1.0, 0, 0),
                  fr=(-k * 0.4, 0, 0), fl=(-k * 0.4, 0, 0))
        self.pos("pelvis", (t, 0, -d, lean))
        return self


def anims(B):
    def mk(name, ticks, loop=False):
        return IB(B, name, ticks, REST, (), loop)

    # ---------------- idle (60): heavy breathing, head twitches, drool sways, blades flex
    a = mk("idle", 60, loop=True)
    for t, j in ((0, 0), (15, 1), (30, 0), (45, -1), (60, 0)):
        a.at(t, body=(2 * abs(j), 2 * j, 1.5 * j), neck=(-2 * abs(j), 0, 0), head=(3 * abs(j), -5 * j, 6 * j),
             P_pelvis=(0, -0.3 * abs(j), 0), arm_r=(-2 * abs(j), 0, 0), arm_l=(-2 * abs(j), 0, 0), jaw=(-4 * abs(j), 0, 0))
        a.blades(t, saw=(-3 * abs(j), 0, 2 * j), knife=(-3 * abs(j), 0, -2 * j), kb=(4 * j, 0, 0))
    a.at(36, head=(2, 4, 14)).at(38, head=(1, 0, -8))  # insect head twitch
    a.claws(0, 0).claws(20, -8, 4).claws(40, 6).claws(60, 0)
    a.curl([(0, 0, 0), (20, -10, 2), (40, 6, -2), (60, 0, 0)])
    a.sec([(0, 0, 1), (15, 2, -1), (30, 0, 1), (45, 2, -1), (60, 0, 1)], delay=4)
    a.done(base_layer=True)

    # ---------------- walk (24): long spider-legged stalk, diagonal gait (R leg + L arm), body bobs and sways
    a = mk("walk", 24, loop=True)
    a.rot("leg_r", (0, 22, 0, 0), (12, -18, 0, 0), (24, 22, 0, 0))
    a.rot("shin_r", (0, -4, 0, 0), (12, 6, 0, 0), (16, -40, 0, 0), (20, -26, 0, 0), (24, -4, 0, 0))
    a.rot("ank_r", (0, 0, 0, 0), (12, -12, 0, 0), (16, 20, 0, 0), (24, 0, 0, 0))
    a.rot("leg_l", (0, -18, 0, 0), (12, 22, 0, 0), (24, -18, 0, 0))
    a.rot("shin_l", (0, 6, 0, 0), (4, -40, 0, 0), (8, -26, 0, 0), (12, -4, 0, 0), (24, 6, 0, 0))
    a.rot("ank_l", (0, -12, 0, 0), (4, 20, 0, 0), (12, 0, 0, 0), (24, -12, 0, 0))
    a.rot("arm_l", (0, 24, 0, 0), (6, 30, 0, -6), (12, -16, 0, 0), (24, 24, 0, 0))
    a.rot("fore_l", (0, 0, 0, 0), (4, -24, 0, 0), (8, -10, 0, 0), (12, 6, 0, 0), (24, 0, 0, 0))
    a.rot("arm_r", (0, -16, 0, 0), (12, 24, 0, 0), (18, 30, 0, 6), (24, -16, 0, 0))
    a.rot("fore_r", (0, 6, 0, 0), (12, 0, 0, 0), (16, -24, 0, 0), (20, -10, 0, 0), (24, 6, 0, 0))
    a.pos("pelvis", (0, 0, -0.6, 0), (6, 0, 0.4, 0), (12, 0, -0.6, 0), (18, 0, 0.4, 0), (24, 0, -0.6, 0))
    a.rot("pelvis", (0, 0, 6, 3), (12, 0, -6, -3), (24, 0, 6, 3))
    a.rot("body", (0, 3, -6, -3), (6, -2, 0, 0), (12, 3, 6, 3), (18, -2, 0, 0), (24, 3, -6, -3))
    a.rot("head", (0, -4, 6, 4), (12, -4, -6, -4), (24, -4, 6, 4))
    a.rot("jaw", (0, -6, 0, 0), (6, -2, 0, 0), (12, -6, 0, 0), (18, -2, 0, 0), (24, -6, 0, 0))
    a.blades(0, saw=(4, 0, 3), knife=(-4, 0, 3)).blades(12, saw=(-4, 0, -3), knife=(4, 0, -3)).blades(24, saw=(4, 0, 3), knife=(-4, 0, 3))
    a.sec([(0, 4, 3), (6, -3, 0), (12, 4, -3), (18, -3, 0), (24, 4, 3)], delay=2)
    a.done(base_layer=True)

    # ---------------- cross (34): both blades rear high 0-10, X-SLASH down at 14 (blades cross), follow-through 18, recover
    a = mk("cross", 34)
    a.at(0, body=(0, 0, 0), P_pelvis=(0, 0, 0))
    a.at(9, body=(22, 0, 0), neck=(-12, 0, 0), head=(-14, 0, 0), jaw=(-30, 0, 0), arm_r=(-16, 0, 8), arm_l=(-16, 0, -8))
    a.blades(9, saw=(40, 0, -26), knife=(40, 0, 26), sb=(30, 0, 0), kb=(30, 0, 0), kn=(20, 0, 0))
    a.at(12, body=(26, 0, 0), head=(-18, 0, 0))
    a.blades(12, saw=(48, 0, -30), knife=(48, 0, 30), sb=(36, 0, 0), kb=(34, 0, 0), kn=(24, 0, 0))
    a.at(14, body=(-26, 0, 0), neck=(8, 0, 0), head=(12, 0, 0), jaw=(-40, 0, 0), arm_r=(50, 0, 0), arm_l=(50, 0, 0))
    a.blades(14, saw=(-60, 0, 34), knife=(-60, 0, -34), sb=(-30, 0, 0), kb=(-30, 0, 0), kn=(-10, 0, 0))
    a.at(18, body=(-30, 0, 0), head=(14, 0, 0), jaw=(-20, 0, 0), arm_r=(55, 0, 0), arm_l=(55, 0, 0))
    a.blades(18, saw=(-74, 0, 44), knife=(-74, 0, -44), sb=(-36, 0, 0), kb=(-36, 0, 0))
    a.crouch(0, 0).crouch(9, -0.8, 0.6).crouch(14, 1.4, -1.2).crouch(20, 1.2, -1.2).crouch(34, 0)
    a.at(24, body=(-18, 0, 0), head=(8, 0, 0), arm_r=(30, 0, 0), arm_l=(30, 0, 0)).blades(24, saw=(-50, 0, 30), knife=(-50, 0, -30), sb=(-20, 0, 0), kb=(-20, 0, 0))
    a.at(34, body=(0, 0, 0), neck=(0, 0, 0), head=(0, 0, 0), jaw=(0, 0, 0), arm_r=(0, 0, 0), arm_l=(0, 0, 0)).blades(34)
    a.claws(0).claws(9, -20, 8).claws(14, 20).claws(34)
    a.curl([(0, 0, 0), (9, 20, 0), (14, -30, 0), (20, -40, 0), (34, 0, 0)])
    a.sec([(0, 0, 0), (9, -8, 0), (14, 12, 0), (20, 6, 0), (34, 0, 0)])
    a.done()

    # ---------------- whirl (42): wind 0-10 (coil to the right), 4 spinning sweeps 12-30 (two full turns), dizzy recover
    a = mk("whirl", 42)
    a.at(0, pelvis=(0, 0, 0))
    a.at(9, pelvis=(0, -50, 0), body=(-6, -20, 8), head=(0, 30, 0))
    a.blades(9, saw=(-30, 0, -50), knife=(-30, 0, 50), sb=(-20, 0, 0), kb=(-20, 0, 0), kn=(0, 0, 0))
    for i, t in enumerate((12, 18, 24, 30)):
        a.at(t, pelvis=(0, 120 + i * 180, 0), body=(-14, 0, 0), head=(0, -10, 0))
    a.at(15, pelvis=(0, 210, 0)).at(21, pelvis=(0, 390, 0)).at(27, pelvis=(0, 570, 0))
    a.at(34, pelvis=(0, 720, 0), body=(-4, 0, -6), head=(0, 0, 12))
    a.at(42, pelvis=(0, 720, 0), body=(0, 0, 0), head=(0, 0, 0))
    for t in (12, 30):
        a.blades(t, saw=(-50, 0, -75), knife=(-50, 0, 75), sb=(-10, 0, 0), kb=(-10, 0, 0), kn=(10, 0, 0))
    a.blades(42)
    a.at(12, arm_r=(-30, 0, 50), arm_l=(-30, 0, -50), fore_r=(20, 0, 0), fore_l=(20, 0, 0))
    a.at(30, arm_r=(-30, 0, 50), arm_l=(-30, 0, -50))
    a.at(42, arm_r=(0, 0, 0), arm_l=(0, 0, 0), fore_r=(0, 0, 0), fore_l=(0, 0, 0))
    a.crouch(0, 0).crouch(9, 2.0).crouch(12, 1.0).crouch(30, 1.0).crouch(36, 1.6).crouch(42, 0)
    a.at(0, jaw=(0, 0, 0)).at(12, jaw=(-30, 0, 0)).at(30, jaw=(-30, 0, 0)).at(42, jaw=(0, 0, 0))
    a.curl([(0, 0, 0), (9, 20, 0), (12, -20, 20), (30, -20, 20), (36, 10, -10), (42, 0, 0)])
    a.sec([(0, 0, 0), (9, 0, -10), (12, 0, 20), (30, 0, 20), (36, 0, -14), (42, 0, 0)])
    a.done()

    # ---------------- impale (38): knife blade draws far back 0-12, coil low, THRUST at 17 (body lunges), hold, pull out 26
    a = mk("impale", 38)
    a.at(0, body=(0, 0, 0))
    a.at(12, body=(18, 14, 0), neck=(-10, 0, 0), head=(-10, -16, 0), arm_l=(-20, 0, 0), arm_r=(10, 0, 0))
    a.blades(12, knife=(60, 10, 10), kb=(50, 0, 0), kn=(30, 0, 0), saw=(10, 0, -10))
    a.at(15, body=(20, 16, 0)).blades(15, knife=(64, 10, 10), kb=(56, 0, 0), kn=(32, 0, 0), saw=(10, 0, -10))
    a.at(17, body=(-30, -10, 0), neck=(10, 0, 0), head=(10, 8, 0), jaw=(-34, 0, 0), arm_l=(55, 0, 0), arm_r=(50, 0, 0))
    a.blades(17, knife=(-86, -10, 4), kb=(-54, 0, 0), kn=(-26, 0, 0), saw=(-20, 0, -14))
    a.at(24, body=(-28, -8, 0), arm_l=(50, 0, 0), arm_r=(46, 0, 0)).blades(24, knife=(-82, -8, 4), kb=(-50, 0, 0), kn=(-24, 0, 0), saw=(-16, 0, -14))
    a.at(28, body=(-6, 0, 0), jaw=(-10, 0, 0)).blades(28, knife=(-20, 0, 0), kb=(-10, 0, 0), kn=(-6, 0, 0), saw=(0, 0, 0))
    a.at(38, body=(0, 0, 0), neck=(0, 0, 0), head=(0, 0, 0), jaw=(0, 0, 0), arm_l=(0, 0, 0), arm_r=(0, 0, 0)).blades(38)
    a.crouch(0, 0).crouch(12, 2.2, 1.4).crouch(17, 0.6, -3.5).crouch(24, 0.6, -3.5).crouch(38, 0)
    a.claws(0).claws(12, 20).claws(17, -20, 8).claws(38)
    a.curl([(0, 0, 0), (12, 10, 0), (17, -20, 0), (38, 0, 0)])
    a.sec([(0, 0, 0), (12, -10, 0), (17, 14, 0), (26, 4, 0), (38, 0, 0)])
    a.done()

    # ---------------- pounce (46): deep crouch 0-14, LEAP 16 (stretch), airborne tuck 20-24, LAND ~26 (splat), rise
    a = mk("pounce", 46)
    a.at(0, body=(0, 0, 0), P_root=(0, 0, 0))
    a.at(14, body=(-12, 0, 0), neck=(-14, 0, 0), head=(-14, 0, 0), jaw=(-20, 0, 0), arm_r=(-30, 0, 10), arm_l=(-30, 0, -10), fore_r=(30, 0, 0), fore_l=(30, 0, 0))
    a.blades(14, saw=(30, 0, -20), knife=(30, 0, 20), sb=(20, 0, 0), kb=(20, 0, 0))
    a.at(17, body=(30, 0, 0), neck=(-10, 0, 0), head=(-10, 0, 0), jaw=(-50, 0, 0), arm_r=(70, 0, 30), arm_l=(70, 0, -30), fore_r=(10, 0, 0), fore_l=(10, 0, 0), P_root=(0, 4, 0))
    a.blades(17, saw=(-40, 0, -40), knife=(-40, 0, 40), sb=(-20, 0, 0), kb=(-20, 0, 0))
    a.legs(17, r=(-50, 0, 0), l=(-50, 0, 0), sr=(40, 0, 0), sl=(40, 0, 0), ar=(-20, 0, 0), al=(-20, 0, 0))
    a.at(22, body=(10, 0, 0), arm_r=(90, 0, 30), arm_l=(90, 0, -30), fore_r=(-10, 0, 0), fore_l=(-10, 0, 0), P_root=(0, 6, 0))
    a.legs(22, r=(30, 0, 0), l=(30, 0, 0), sr=(-60, 0, 0), sl=(-60, 0, 0), ar=(40, 0, 0), al=(40, 0, 0))
    a.at(26, body=(-30, 0, 0), neck=(16, 0, 0), head=(10, 0, 0), jaw=(-30, 0, 0), arm_r=(60, 0, 30), arm_l=(60, 0, -30), fore_r=(-10, 0, 0), fore_l=(-10, 0, 0), P_root=(0, 0, 0))
    a.blades(26, saw=(-70, 0, -10), knife=(-70, 0, 10), sb=(-30, 0, 0), kb=(-30, 0, 0))
    a.crouch(0, 0).crouch(14, 3.5, 1.5).crouch(26, 3.0, -1).crouch(32, 2.6, -1).crouch(46, 0)
    a.at(32, body=(-24, 0, 0), arm_r=(45, 0, 20), arm_l=(45, 0, -20))
    a.at(46, body=(0, 0, 0), neck=(0, 0, 0), head=(0, 0, 0), jaw=(0, 0, 0), arm_r=(0, 0, 0), arm_l=(0, 0, 0), fore_r=(0, 0, 0), fore_l=(0, 0, 0)).blades(46)
    a.claws(0).claws(14, 20).claws(17, -30, 10).claws(26, 30, 6).claws(46)
    a.curl([(0, 0, 0), (14, 20, 0), (17, -30, 0), (22, 20, 0), (26, -40, 0), (46, 0, 0)])
    a.sec([(0, 0, 0), (14, -6, 0), (17, -16, 0), (22, 10, 0), (26, 20, 0), (32, -6, 0), (46, 0, 0)])
    a.done()

    # ---------------- rake (30): forelimb rakes R 8, L 14, R 20 (rearing slightly, swinging claws across)
    a = mk("rake", 30)
    a.at(0, body=(0, 0, 0))
    a.crouch(0, 0).crouch(4, -1.0, 0.5).crouch(8, 0.8, -1).crouch(14, 0.8, -1).crouch(20, 1.2, -1.2).crouch(30, 0)
    for t, s, wind in ((5, 1, True), (8, 1, False), (11, -1, True), (14, -1, False), (17, 1, True), (20, 1, False)):
        k, o = ("r", "l") if s > 0 else ("l", "r")
        if wind:
            a.at(t, body=(14, 16 * s, 4 * s), head=(-6, -12 * s, 0), **{"arm_" + k: (-50, 0, 40 * s), "fore_" + k: (-30, 0, 0), "arm_" + o: (0, 0, 0), "fore_" + o: (0, 0, 0)})
            a.claws(t, -30, 10, side=k)
        else:
            a.at(t, body=(-10, -18 * s, -4 * s), head=(6, 14 * s, 0), jaw=(-26, 0, 0), **{"arm_" + k: (40, 0, -30 * s), "fore_" + k: (10, 0, 0)})
            a.claws(t, 30, 0, side=k)
    a.at(26, body=(-4, 0, 0), arm_r=(10, 0, 0), arm_l=(0, 0, 0), fore_r=(0, 0, 0), jaw=(-8, 0, 0))
    a.at(30, body=(0, 0, 0), head=(0, 0, 0), jaw=(0, 0, 0), arm_r=(0, 0, 0), arm_l=(0, 0, 0), fore_r=(0, 0, 0), fore_l=(0, 0, 0))
    a.claws(0).claws(30)
    a.blades(0).blades(8, saw=(-10, 0, -6), knife=(10, 0, 6)).blades(14, saw=(10, 0, 6), knife=(-10, 0, -6)).blades(20, saw=(-10, 0, -6), knife=(10, 0, 6)).blades(30)
    a.sec([(0, 0, 0), (5, -4, 8), (8, 6, -10), (11, -4, -8), (14, 6, 10), (17, -4, 8), (20, 6, -10), (30, 0, 0)], delay=1)
    a.done()

    # ---------------- spit (40): head rears back, throat swells 0-14, three spits 16/20/24 (head snaps forward each), recover
    a = mk("spit", 40)
    a.at(0, body=(0, 0, 0), neck=(0, 0, 0), head=(0, 0, 0))
    a.at(12, body=(16, 0, 0), neck=(-24, 0, 0), head=(-20, 0, 0), jaw=(-6, 0, 0))
    a.scl("neck", (0, 1, 1, 1), (10, 1.3, 1.1, 1.3), (14, 1.4, 1.1, 1.4), (16, 1, 1, 1), (18, 1.25, 1, 1.25), (20, 1, 1, 1), (22, 1.2, 1, 1.2), (24, 1, 1, 1), (40, 1, 1, 1))
    for t, yaw in ((16, -8), (20, 0), (24, 8)):
        a.at(t - 2, neck=(-14, 0, 0), head=(-14, yaw, 0), jaw=(-10, 0, 0), body=(10, 0, 0))
        a.at(t, neck=(14, 0, 0), head=(16, yaw, 0), jaw=(-50, 0, 0), body=(-10, yaw * 0.5, 0))
    a.at(30, neck=(4, 0, 0), head=(4, 0, 0), jaw=(-20, 0, 0), body=(-4, 0, 0))
    a.at(40, body=(0, 0, 0), neck=(0, 0, 0), head=(0, 0, 0), jaw=(0, 0, 0))
    a.crouch(0, 0).crouch(12, -0.6, 0.8).crouch(16, 0.8, -0.6).crouch(24, 1.0, -0.8).crouch(40, 0)
    a.blades(0).blades(12, saw=(16, 0, -14), knife=(16, 0, 14)).blades(20, saw=(-6, 0, -8), knife=(-6, 0, 8)).blades(40)
    a.claws(0).claws(12, 20, 6).claws(40)
    a.sec([(0, 0, 0), (12, -10, 0), (16, 12, 0), (18, -4, 0), (20, 12, 0), (22, -4, 0), (24, 12, 0), (32, 0, 0), (40, 0, 0)], delay=1)
    a.done()

    # ---------------- screech (46): rear UP on the hind legs, arms and blades flare out, jaw gapes wide 14-32, shudder, drop
    a = mk("screech", 46)
    a.at(0, body=(0, 0, 0), P_pelvis=(0, 0, 0))
    a.at(10, body=(40, 0, 0), neck=(-20, 0, 0), head=(-26, 0, 0), jaw=(-6, 0, 0), arm_r=(-50, 0, 30), arm_l=(-50, 0, -30), fore_r=(30, 0, 0), fore_l=(30, 0, 0))
    a.blades(10, saw=(-26, 0, -36), knife=(-26, 0, 36), sb=(20, 0, 0), kb=(10, 0, 0))
    for t, j in ((14, 0), (17, 1), (20, -1), (23, 1), (26, -1), (29, 1), (32, 0)):
        a.at(t, body=(48 + j, 0, j * 2), neck=(-6, 0, 0), head=(-8 + j * 2, j * 3, j * 3), jaw=(-62, 0, 0),
             arm_r=(-70, 0, 70 + j * 4), arm_l=(-70, 0, -70 + j * 4), fore_r=(40, 0, 0), fore_l=(40, 0, 0))
        a.blades(t, saw=(-36, 0, -50 - j * 4), knife=(-36, 0, 50 + j * 4), sb=(20, 0, 0), kb=(10, 0, 0))
    a.at(38, body=(-10, 0, 0), neck=(6, 0, 0), head=(8, 0, 0), jaw=(-20, 0, 0), arm_r=(20, 0, 0), arm_l=(20, 0, 0), fore_r=(0, 0, 0), fore_l=(0, 0, 0))
    a.blades(38, saw=(-10, 0, 0), knife=(-10, 0, 0))
    a.at(46, body=(0, 0, 0), neck=(0, 0, 0), head=(0, 0, 0), jaw=(0, 0, 0), arm_r=(0, 0, 0), arm_l=(0, 0, 0)).blades(46)
    a.legs(0).legs(10, r=(-10, 0, 0), l=(-10, 0, 0), sr=(20, 0, 0), sl=(20, 0, 0)).legs(32, r=(-10, 0, 0), l=(-10, 0, 0), sr=(20, 0, 0), sl=(20, 0, 0))
    a.legs(38, r=(16, 0, 0), l=(16, 0, 0), sr=(-26, 0, 0), sl=(-26, 0, 0), ar=(10, 0, 0), al=(10, 0, 0)).legs(46)
    a.pos("pelvis", (0, 0, 0, 0), (10, 0, 1.6, 0.5), (32, 0, 1.6, 0.5), (38, 0, -1.4, -0.6), (46, 0, 0, 0))
    a.claws(0).claws(10, -30, 12).claws(32, -30, 12).claws(46)
    a.curl([(0, 0, 0), (10, 20, 0), (14, 40, 0), (32, 40, 0), (38, -20, 0), (46, 0, 0)])
    a.sec([(0, 0, 0), (10, -14, 0), (14, 0, 6), (17, 0, -6), (20, 0, 6), (23, 0, -6), (26, 0, 6), (32, 0, 0), (38, 14, 0), (46, 0, 0)], delay=1)
    a.done()

    # ---------------- spikes (44): rears with both forelimbs high 0-12, slams claws into floor 16, holds (spikes run forward) to 32, rip out
    a = mk("spikes", 44)
    a.at(0, body=(0, 0, 0))
    a.at(11, body=(30, 0, 0), neck=(-16, 0, 0), head=(-14, 0, 0), jaw=(-30, 0, 0), arm_r=(-100, 0, 20), arm_l=(-100, 0, -20), fore_r=(40, 0, 0), fore_l=(40, 0, 0))
    a.blades(11, saw=(20, 0, -20), knife=(20, 0, 20), sb=(20, 0, 0), kb=(20, 0, 0))
    a.at(16, body=(-34, 0, 0), neck=(18, 0, 0), head=(16, 0, 0), jaw=(-40, 0, 0), arm_r=(45, 0, 0), arm_l=(45, 0, 0), fore_r=(-20, 0, 0), fore_l=(-20, 0, 0))
    a.blades(16, saw=(-40, 0, -10), knife=(-40, 0, 10))
    for t, j in ((20, 1), (24, -1), (28, 1), (32, 0)):
        a.at(t, body=(-32 + j * 2, 0, j * 2), head=(16, 0, j * 4), arm_r=(46, 0, 0), arm_l=(46, 0, 0))
    a.at(36, body=(4, 0, 0), arm_r=(-20, 0, 6), arm_l=(-20, 0, -6), fore_r=(10, 0, 0), fore_l=(10, 0, 0), jaw=(-10, 0, 0))
    a.at(44, body=(0, 0, 0), neck=(0, 0, 0), head=(0, 0, 0), jaw=(0, 0, 0), arm_r=(0, 0, 0), arm_l=(0, 0, 0), fore_r=(0, 0, 0), fore_l=(0, 0, 0)).blades(44)
    a.crouch(0, 0).crouch(11, -1.0, 1.0).crouch(16, 2.4, -1.5).crouch(32, 2.2, -1.5).crouch(36, 1.0).crouch(44, 0)
    a.claws(0).claws(11, -30, 12).claws(16, 40, 4).claws(32, 40, 4).claws(36, -10).claws(44)
    a.curl([(0, 0, 0), (11, 20, 0), (16, -30, 0), (32, -20, 0), (44, 0, 0)])
    a.sec([(0, 0, 0), (11, -12, 0), (16, 18, 0), (24, 4, 4), (32, 0, 0), (36, -8, 0), (44, 0, 0)])
    a.done()

    # ---------------- bite (32): head pulls back, jaw gapes 0-11, SNAP lunge 14, shake 16-22 (tearing), spit out
    a = mk("bite", 32)
    a.at(0, body=(0, 0, 0))
    a.at(10, body=(14, 0, 0), neck=(-28, 0, 0), head=(-20, 0, 0), jaw=(-60, 0, 0))
    a.at(14, body=(-28, 0, 0), neck=(30, 0, 0), head=(18, 0, 0), jaw=(4, 0, 0), arm_r=(48, 0, 0), arm_l=(48, 0, 0))
    for t, j in ((16, 1), (18, -1), (20, 1), (22, -1)):
        a.at(t, head=(16, 18 * j, 14 * j), jaw=(2, 0, 0), body=(-26, 6 * j, 0), arm_r=(46, 0, 0), arm_l=(46, 0, 0))
    a.at(26, body=(-4, 0, 0), neck=(-6, 0, 0), head=(-4, 0, 0), jaw=(-34, 0, 0))
    a.at(32, body=(0, 0, 0), neck=(0, 0, 0), head=(0, 0, 0), jaw=(0, 0, 0), arm_r=(0, 0, 0), arm_l=(0, 0, 0))
    a.crouch(0, 0).crouch(10, 1.0, 1.2).crouch(14, 0.6, -2.6).crouch(22, 0.6, -2.4).crouch(32, 0)
    a.blades(0).blades(10, saw=(14, 0, -10), knife=(14, 0, 10)).blades(14, saw=(-16, 0, -6), knife=(-16, 0, 6)).blades(32)
    a.claws(0).claws(14, 30).claws(22, 30).claws(32)
    a.sec([(0, 0, 0), (10, -12, 0), (14, 16, 0), (16, 0, 14), (18, 0, -14), (20, 0, 14), (22, 0, -14), (26, -6, 0), (32, 0, 0)], delay=1)
    a.done()

    # ---------------- blade_storm (62, enraged): frenzied stilt-walk spin, blades flailing every 5 ticks 10-46, spikes 30/40
    a = mk("blade_storm", 62)
    a.at(0, pelvis=(0, 0, 0))
    a.at(8, pelvis=(0, -40, 0), body=(10, 0, 0), jaw=(-50, 0, 0), head=(-12, 0, 0))
    a.blades(8, saw=(30, 0, -50), knife=(30, 0, 50), sb=(30, 0, 0), kb=(30, 0, 0))
    deg = 0
    for i, t in enumerate(range(10, 48, 5)):
        deg += 135
        s = 1 if i % 2 == 0 else -1
        a.at(t, pelvis=(0, deg, 0), body=(-16, 0, 10 * s), head=(4, 0, -12 * s), jaw=(-56, 0, 0),
             arm_r=(-40 + 30 * s, 0, 60), arm_l=(-40 - 30 * s, 0, -60), fore_r=(20, 0, 0), fore_l=(20, 0, 0))
        a.blades(t, saw=(-60 + 40 * s, 0, -70), knife=(-60 - 40 * s, 0, 70), sb=(-20 * s, 0, 0), kb=(20 * s, 0, 0))
    a.at(52, pelvis=(0, deg + 45, 0), body=(-30, 0, 0), head=(10, 0, 0), arm_r=(10, 0, 20), arm_l=(10, 0, -20))
    a.blades(52, saw=(-50, 0, -20), knife=(-50, 0, 20))
    a.at(62, pelvis=(0, 360 * round((deg + 45) / 360), 0), body=(0, 0, 0), head=(0, 0, 0), jaw=(0, 0, 0), arm_r=(0, 0, 0), arm_l=(0, 0, 0), fore_r=(0, 0, 0), fore_l=(0, 0, 0))
    a.blades(62)
    a.crouch(0, 0).crouch(8, 2.0)
    for i, t in enumerate(range(10, 48, 5)):
        a.crouch(t, 1.0 + (i % 2) * 0.8)
    a.crouch(52, 2.6).crouch(62, 0)
    a.curl([(0, 0, 0), (8, 20, 0)] + [(t, -30 * (1 if i % 2 else -1), 20) for i, t in enumerate(range(10, 48, 5))] + [(52, -20, 0), (62, 0, 0)])
    a.claws(0).claws(8, -30, 12).claws(48, -30, 12).claws(62)
    a.sec([(0, 0, 0), (8, -6, 0)] + [(t, 0, 20 * (1 if i % 2 else -1)) for i, t in enumerate(range(10, 48, 5))] + [(52, 10, 0), (62, 0, 0)], delay=1)
    a.done()

    # ---------------- hook (38): saw arm coils back 0-11, LASH forward 14 (chain fully extended), REEL in 14-22, knife JAB 24, recover
    a = mk("hook", 38)
    a.at(0, body=(0, 0, 0))
    a.at(11, body=(16, -18, 0), head=(-10, 20, 0), jaw=(-20, 0, 0), arm_r=(-20, 0, 10))
    a.blades(11, saw=(60, 0, -30), sb=(60, 0, 0), knife=(10, 0, 10))
    a.at(14, body=(-20, 16, 0), head=(10, -10, 0), jaw=(-36, 0, 0), arm_r=(10, 0, 0))
    a.blades(14, saw=(-90, 0, 10), sb=(56, 0, 0), knife=(0, 0, 10))
    a.at(19, body=(10, -6, 0), head=(-6, 4, 0)).blades(19, saw=(20, 0, -10), sb=(-20, 0, 0), knife=(40, 0, 20), kb=(30, 0, 0), kn=(20, 0, 0))
    a.at(21, body=(14, -10, 0)).blades(21, saw=(30, 0, -14), sb=(-30, 0, 0), knife=(50, 0, 20), kb=(40, 0, 0), kn=(24, 0, 0))
    a.at(24, body=(-28, -10, 0), head=(12, 6, 0), jaw=(-40, 0, 0))
    a.blades(24, saw=(10, 0, -10), sb=(-20, 0, 0), knife=(-84, 0, -6), kb=(-46, 0, 0), kn=(-20, 0, 0))
    a.at(30, body=(-12, -4, 0), jaw=(-14, 0, 0)).blades(30, knife=(-40, 0, 0), kb=(-20, 0, 0))
    a.at(38, body=(0, 0, 0), head=(0, 0, 0), jaw=(0, 0, 0), arm_r=(0, 0, 0)).blades(38)
    a.curl([(0, 0, 0), (11, 30, 0), (14, 40, 0), (16, 30, 0), (19, -50, 0), (24, -30, 0), (38, 0, 0)])  # straight on lash, hooked on reel
    a.crouch(0, 0).crouch(11, 1.6, 1).crouch(14, 1.0, -1.5).crouch(19, 1.6, 0.6).crouch(24, 1.2, -2.6).crouch(38, 0)
    a.claws(0).claws(14, -20, 8).claws(24, 30).claws(38)
    a.sec([(0, 0, 0), (11, -8, -6), (14, 12, 6), (19, -8, 0), (24, 14, 0), (38, 0, 0)])
    a.done()

    # ---------------- stomp (42): rears up tall 0-15 (forelimbs raised, blades flared), CRASH both claws down at 20, shudder, push up
    a = mk("stomp", 42)
    a.at(0, body=(0, 0, 0))
    a.at(12, body=(52, 0, 0), neck=(-28, 0, 0), head=(-20, 0, 0), jaw=(-40, 0, 0), arm_r=(-120, 0, 30), arm_l=(-120, 0, -30), fore_r=(50, 0, 0), fore_l=(50, 0, 0))
    a.blades(12, saw=(20, 0, -40), knife=(20, 0, 40), sb=(40, 0, 0), kb=(30, 0, 0))
    a.at(16, body=(58, 0, 0), arm_r=(-130, 0, 26), arm_l=(-130, 0, -26), fore_r=(60, 0, 0), fore_l=(60, 0, 0))
    a.at(20, body=(-30, 0, 0), neck=(20, 0, 0), head=(16, 0, 0), jaw=(-50, 0, 0), arm_r=(52, 0, 6), arm_l=(52, 0, -6), fore_r=(-16, 0, 0), fore_l=(-16, 0, 0))
    a.blades(20, saw=(-50, 0, -10), knife=(-50, 0, 10), sb=(-20, 0, 0), kb=(-20, 0, 0))
    a.at(24, body=(-26, 0, 0), head=(12, 0, 4), arm_r=(50, 0, 6), arm_l=(50, 0, -6)).at(28, body=(-28, 0, 0), head=(14, 0, -4), arm_r=(50, 0, 6), arm_l=(50, 0, -6))
    a.at(34, body=(-6, 0, 0), arm_r=(-10, 0, 0), arm_l=(-10, 0, 0), fore_r=(6, 0, 0), fore_l=(6, 0, 0), jaw=(-10, 0, 0)).blades(34, saw=(-10, 0, 0), knife=(-10, 0, 0))
    a.at(42, body=(0, 0, 0), neck=(0, 0, 0), head=(0, 0, 0), jaw=(0, 0, 0), arm_r=(0, 0, 0), arm_l=(0, 0, 0), fore_r=(0, 0, 0), fore_l=(0, 0, 0)).blades(42)
    a.legs(0).legs(12, r=(-14, 0, 0), l=(-14, 0, 0), sr=(24, 0, 0), sl=(24, 0, 0)).legs(16, r=(-16, 0, 0), l=(-16, 0, 0), sr=(26, 0, 0), sl=(26, 0, 0))
    a.legs(20, r=(20, 0, 0), l=(20, 0, 0), sr=(-34, 0, 0), sl=(-34, 0, 0), ar=(14, 0, 0), al=(14, 0, 0)).legs(28, r=(18, 0, 0), l=(18, 0, 0), sr=(-30, 0, 0), sl=(-30, 0, 0), ar=(12, 0, 0), al=(12, 0, 0)).legs(42)
    a.pos("pelvis", (0, 0, 0, 0), (12, 0, 2.2, 1.0), (16, 0, 2.6, 1.2), (20, 0, -2.4, -1.4), (28, 0, -2.2, -1.2), (42, 0, 0, 0))
    a.claws(0).claws(12, -40, 14).claws(20, 40, 4).claws(28, 40, 4).claws(42)
    a.curl([(0, 0, 0), (12, 30, 0), (20, -40, 0), (42, 0, 0)])
    a.sec([(0, 0, 0), (12, -16, 0), (20, 20, 0), (24, 0, 6), (28, 0, -6), (34, -6, 0), (42, 0, 0)])
    a.done()

    # ---------------- ooze (60): retching heaves 0-14 (throat pulses), jaw unhinges and vomits ink 16-26, drips, recover
    a = mk("ooze", 60)
    a.at(0, body=(0, 0, 0))
    for t, j in ((4, 1), (8, 0), (12, 1)):
        a.at(t, body=(-10 * j + 6, 0, 0), neck=(16 * j - 6, 0, 0), head=(14 * j - 4, 0, 0), jaw=(-20 * j, 0, 0))
    a.scl("neck", (0, 1, 1, 1), (4, 1.3, 1, 1.3), (8, 1, 1, 1), (12, 1.4, 1, 1.4), (16, 1.1, 1, 1.1), (26, 1.1, 1, 1.1), (30, 1, 1, 1), (60, 1, 1, 1))
    for t, j in ((16, 0), (19, 1), (22, -1), (26, 0)):
        a.at(t, body=(-22, 0, 0), neck=(26, j * 4, 0), head=(18, j * 6, j * 4), jaw=(-70, 0, 0))
    a.at(32, body=(-12, 0, 0), neck=(10, 0, 0), head=(10, 0, 0), jaw=(-30, 0, 0))
    a.at(44, body=(-6, 0, 0), neck=(4, 0, 0), head=(4, 0, 6), jaw=(-16, 0, 0))
    a.at(60, body=(0, 0, 0), neck=(0, 0, 0), head=(0, 0, 0), jaw=(0, 0, 0))
    a.at(0, arm_r=(0, 0, 0), arm_l=(0, 0, 0)).at(12, arm_r=(-10, 0, 10), arm_l=(-10, 0, -10)).at(20, arm_r=(10, 0, 0), arm_l=(10, 0, 0)).at(60, arm_r=(0, 0, 0), arm_l=(0, 0, 0))
    a.crouch(0, 0).crouch(4, 1.0).crouch(8, 0.2).crouch(12, 1.4).crouch(16, 2.0, -1).crouch(26, 2.0, -1).crouch(40, 0.8).crouch(60, 0)
    a.blades(0).blades(12, saw=(16, 0, -16), knife=(16, 0, 16)).blades(20, saw=(-10, 0, -20), knife=(-10, 0, 20)).blades(44, saw=(-4, 0, -6), knife=(-4, 0, 6)).blades(60)
    for k in ("a", "b", "c"):  # drool stretches long while vomiting
        a.scl(f"drool_{k}0", (0, 1, 1, 1), (14, 1, 1, 1), (18, 1.4, 2.2, 1.4), (26, 1.4, 2.2, 1.4), (40, 1, 1.4, 1), (60, 1, 1, 1))
    a.claws(0).claws(12, 30, 6).claws(26, 30, 6).claws(60)
    a.curl([(0, 0, 0), (12, 10, 0), (20, -10, 0), (60, 0, 0)])
    a.sec([(0, 0, 0), (4, 8, 0), (8, -6, 0), (12, 8, 0), (16, 12, 0), (19, 4, 6), (22, 4, -6), (26, 6, 0), (34, -4, 0), (60, 0, 0)], delay=1)
    a.done()

    # ---------------- skitter (32): crouch 0-3, sidestep hop 4-10 (body tilts, legs scuttle), lunge 12, crossed claw RAKE 17, recover
    a = mk("skitter", 32)
    a.at(0, body=(0, 0, 0), P_root=(0, 0, 0))
    a.at(3, body=(6, 0, 0), pelvis=(0, 0, 0))
    a.at(6, pelvis=(0, 0, -14), body=(0, 0, 10), head=(0, 0, -16), P_root=(0, 2.0, 0))
    a.at(10, pelvis=(0, 0, 8), body=(10, 0, -6), head=(-6, 0, 8), P_root=(0, 0, 0))
    a.at(12, pelvis=(0, 0, 0), body=(-20, 0, 0), head=(8, 0, 0), jaw=(-40, 0, 0), arm_r=(-60, 0, 50), arm_l=(-60, 0, -50), fore_r=(-30, 0, 0), fore_l=(-30, 0, 0))
    a.blades(12, saw=(30, 0, -40), knife=(30, 0, 40), sb=(20, 0, 0), kb=(20, 0, 0))
    a.at(17, body=(-30, 0, 0), head=(14, 0, 0), jaw=(-50, 0, 0), arm_r=(60, 0, -40), arm_l=(60, 0, 40), fore_r=(10, 0, 0), fore_l=(10, 0, 0))
    a.blades(17, saw=(-70, 0, 30), knife=(-70, 0, -30), sb=(-30, 0, 0), kb=(-30, 0, 0))
    a.at(22, body=(-22, 0, 0), arm_r=(50, 0, -30), arm_l=(50, 0, 30)).blades(22, saw=(-50, 0, 20), knife=(-50, 0, -20))
    a.at(32, body=(0, 0, 0), head=(0, 0, 0), jaw=(0, 0, 0), arm_r=(0, 0, 0), arm_l=(0, 0, 0), fore_r=(0, 0, 0), fore_l=(0, 0, 0), pelvis=(0, 0, 0)).blades(32)
    a.legs(0).legs(3, r=(10, 0, 0), l=(10, 0, 0), sr=(-16, 0, 0), sl=(-16, 0, 0))
    a.legs(6, r=(-10, 0, 20), l=(30, 0, 10), sr=(-30, 0, 0), sl=(-50, 0, 0), ar=(20, 0, 0), al=(30, 0, 0))
    a.legs(8, r=(30, 0, -6), l=(-20, 0, -14), sr=(-50, 0, 0), sl=(-10, 0, 0))
    a.legs(10, r=(16, 0, 0), l=(16, 0, 0), sr=(-26, 0, 0), sl=(-26, 0, 0), ar=(10, 0, 0), al=(10, 0, 0))
    a.legs(14, r=(-30, 0, 0), l=(10, 0, 0), sr=(10, 0, 0), sl=(-30, 0, 0))
    a.legs(17, r=(-20, 0, 0), l=(24, 0, 0), sr=(0, 0, 0), sl=(-40, 0, 0), ar=(-10, 0, 0), al=(20, 0, 0))
    a.legs(32)
    a.claws(0).claws(12, -40, 14).claws(17, 40, 0).claws(32)
    a.curl([(0, 0, 0), (6, 10, 20), (12, 30, 0), (17, -40, 0), (32, 0, 0)])
    a.sec([(0, 0, 0), (6, 0, -18), (10, 0, 12), (12, -8, 0), (17, 16, 0), (24, 4, 0), (32, 0, 0)], delay=1)
    a.done()

    # ---------------- infest (60, enraged): blades rise overhead 0-14, PLUNGE into the floor 18, held in the ground (pulsing) 18-44, rip out 50
    a = mk("infest", 60)
    a.at(0, body=(0, 0, 0))
    a.at(12, body=(36, 0, 0), neck=(-20, 0, 0), head=(-24, 0, 0), jaw=(-46, 0, 0), arm_r=(-40, 0, 40), arm_l=(-40, 0, -40))
    a.blades(12, saw=(50, 0, -20), knife=(50, 0, 20), sb=(50, 0, 0), kb=(50, 0, 0), kn=(30, 0, 0))
    a.at(15, body=(40, 0, 0)).blades(15, saw=(56, 0, -20), knife=(56, 0, 20), sb=(56, 0, 0), kb=(56, 0, 0), kn=(34, 0, 0))
    a.at(18, body=(-40, 0, 0), neck=(20, 0, 0), head=(20, 0, 0), jaw=(-60, 0, 0), arm_r=(55, 0, 30), arm_l=(55, 0, -30), fore_r=(-10, 0, 0), fore_l=(-10, 0, 0))
    a.blades(18, saw=(-100, 0, -8), knife=(-100, 0, 8), sb=(-20, 0, 0), kb=(-30, 0, 0), kn=(-20, 0, 0))
    for t, j in ((22, 1), (26, 0), (30, 1), (34, 0), (38, 1), (42, 0)):
        a.at(t, body=(-38 + j * 4, 0, j * 2), head=(14 + j * 6, 0, 0), jaw=(-50 - j * 14, 0, 0), arm_r=(55, 0, 30), arm_l=(55, 0, -30))
        a.blades(t, saw=(-100 + j * 4, 0, -8), knife=(-100 + j * 4, 0, 8), sb=(-20, 0, 0), kb=(-30, 0, 0), kn=(-20, 0, 0))
    a.at(48, body=(20, 0, 0), head=(-10, 0, 0), jaw=(-20, 0, 0), arm_r=(-10, 0, 10), arm_l=(-10, 0, -10), fore_r=(10, 0, 0), fore_l=(10, 0, 0))
    a.blades(48, saw=(30, 0, -20), knife=(30, 0, 20), sb=(30, 0, 0), kb=(20, 0, 0))
    a.at(60, body=(0, 0, 0), neck=(0, 0, 0), head=(0, 0, 0), jaw=(0, 0, 0), arm_r=(0, 0, 0), arm_l=(0, 0, 0), fore_r=(0, 0, 0), fore_l=(0, 0, 0)).blades(60)
    a.crouch(0, 0).crouch(12, -0.8, 1).crouch(18, 2.6, -1.5).crouch(42, 2.4, -1.5).crouch(48, 1.0).crouch(60, 0)
    a.claws(0).claws(12, -30, 10).claws(18, 40).claws(42, 40).claws(60)
    a.curl([(0, 0, 0), (12, 20, 0), (18, -50, 0), (42, -50, 0), (48, 20, 0), (60, 0, 0)])
    a.sec([(0, 0, 0), (12, -14, 0), (18, 20, 0), (22, 6, 0), (26, 12, 0), (30, 6, 0), (34, 12, 0), (42, 6, 0), (48, -10, 0), (60, 0, 0)])
    a.done()

    # ---------------- death (40): convulse/shriek 0-8, hind legs buckle 16, topples sideways 28, blades go limp, splays flat
    a = mk("death", 40)
    a.at(0, body=(0, 0, 0), root=(0, 0, 0), P_root=(0, 0, 0))
    a.at(4, body=(30, 0, 6), neck=(-20, 0, 0), head=(-30, 10, 10), jaw=(-60, 0, 0), arm_r=(-60, 0, 40), arm_l=(-60, 0, -40))
    a.blades(4, saw=(30, 0, -50), knife=(30, 0, 50), sb=(40, 0, 0), kb=(40, 0, 0))
    a.at(8, body=(24, 0, -6), head=(-20, -10, -10))
    a.at(16, body=(-20, 0, 0), head=(20, 0, 0), jaw=(-30, 0, 0), arm_r=(20, 0, 30), arm_l=(20, 0, -30))
    a.blades(16, saw=(-30, 0, -40), knife=(-30, 0, 40), sb=(-30, 0, 0), kb=(-30, 0, 0))
    a.at(28, root=(0, 0, 80), P_root=(4, 2.0, 0), body=(-10, 0, 0), head=(10, 0, 20), jaw=(-50, 0, 0), arm_r=(40, 0, 60), arm_l=(10, 0, -20))
    a.blades(28, saw=(-60, 0, -70), knife=(-40, 0, 60), sb=(-50, 0, 0), kb=(-50, 0, 0), kn=(-30, 0, 0))
    a.at(40, root=(0, 0, 88), P_root=(5, 1.0, 0), body=(-6, 0, 0), head=(14, 0, 24), jaw=(-60, 0, 0))
    a.blades(40, saw=(-70, 0, -80), knife=(-50, 0, 70), sb=(-60, 0, 0), kb=(-60, 0, 0), kn=(-30, 0, 0))
    a.crouch(0, 0).crouch(4, -0.6).crouch(16, 6.0).crouch(28, 5.0).crouch(40, 4.0)
    a.claws(0).claws(4, -40, 14).claws(16, 40).claws(40, 60, 6)
    a.curl([(0, 0, 0), (4, 30, 0), (16, -30, 0), (28, -60, 0), (40, -70, 0)])
    a.sec([(0, 0, 0), (4, -16, 10), (8, -10, -10), (16, 16, 0), (28, 0, 30), (40, 0, 40)], delay=1)
    a.done()


if __name__ == "__main__":
    b = Builder("infected_bloomie", 1.0, False, 6)
    b.C = C
    build(b)
    anims(b)
    b.m.save(DIR + "infected_bloomie.bbmodel")
    print("infected_bloomie cubes", len(b.m.cubes), "anims", [x["name"] for x in b.m.anims])
