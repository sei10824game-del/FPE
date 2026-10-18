"""Danger AU Alice - generates assets/fpe/bbmodels/danger_alice.bbmodel (variant 0) and danger_alice_boss.bbmodel (variant 1).
References: docs/ref/confirmed/danger_alice_phase1.jpg / danger_alice_phase2.jpg (only these are trusted).
Phase 1: messy brown bob + long arching ahoge, tilted spiky black crown, eyes hidden under the bangs, pale skin, grey ragged
patched poncho/cape over a grey top, cord necklace with a brown warning-triangle pendant, long ragged black skirt with tan
diamond patches + grey under-layer, bandaged arms (ragged grey cuffs) and bandaged scratched legs, black sandals (ankle strap
with a ring on her right leg), six long black curved spikes fanning out of her back.
Phase 2 (boss, 5.2 blocks): pitch-black spindly monster - round head with hair tufts + ahoge, glowing red eyes, huge white grin,
two black horns arching from the back, four pale insect wings, very long arms ending in giant blocky claws, bent spindly legs
with clawed feet; back tentacles come out for attacks.
Blockbench space: Y up, ground 0, faces -Z, character's RIGHT = +X.  Animation rotations are OFFSETS from the built rest pose.
Signs: arm/leg rx>0 swing forward; torso/head rx>0 lean back; ry>0 turn to her left; rz>0 hanging part swings toward +X.
Run: python3 tools/bbgen/chars/danger_alice.py
"""
import math, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))
from bbgen import mix  # noqa: E402
from alice import Builder, A, HIDE, combo  # noqa: E402  (shared rig/animation helpers)

DIR = os.path.join(os.path.dirname(__file__), "../../../src/main/resources/assets/fpe/bbmodels/")
CLEAR = (0, 0, 0, 0)


class Pal:
    pass


C1 = Pal()
C1.HAIR, C1.HAIR_D, C1.HAIR_HI = 0x6A4636, 0x45291F, 0x8C634D
C1.SKIN, C1.SKIN_D, C1.BLUSH = 0xEED8CA, 0xCDB1A2, 0xD9837E
C1.LID = 0x2A1C18
C1.BAND, C1.BAND_D, C1.BAND_L = 0xD6D0CA, 0x9C958F, 0xEDE9E4
C1.SCRATCH = 0xA2383A
C1.CAPE, C1.CAPE_D, C1.CAPE_HI = 0x5E6168, 0x44464D, 0x7A7D85
C1.SKIRT, C1.SKIRT_D, C1.SKIRT_HI = 0x1F1F24, 0x121215, 0x34343C
C1.UNDER = 0x6A6C73
C1.PATCH, C1.PATCH_D = 0xB09482, 0x6E5649
C1.PEND, C1.PEND_D = 0xA05F3D, 0x5B2E1E
C1.BLACK, C1.BLACK_HI = 0x111114, 0x34343E
C1.SPIKE, C1.SPIKE_HI = 0x0E0E12, 0x3A3A48

C2 = Pal()
C2.BODY, C2.BODY_D, C2.BODY_HI = 0x0D0D10, 0x050506, 0x24242C
C2.EYE, C2.EYE_D = 0xFF2A4A, 0xA0102A
C2.TEETH, C2.TEETH_D = 0xF4F2EE, 0x9A98A0
C2.WING, C2.WING_D, C2.WING_V = 0xE4E0EA, 0xB8B2C4, 0x2A2832
C2.CLAW, C2.CLAW_HI = 0x101014, 0x464656


# ================================================================== painters
def bandage(C, scratches=False, R=None):
    def f(F):
        for y in range(F.h):
            for x in range(F.w):
                F.px(x, y, C.BAND)
        y = 0
        while y < F.h:
            off = (y * 3) % 5
            for x in range(F.w):
                yy = y + (x + off) // 6
                F.px(x, yy, C.BAND_D)
                F.px(x, yy + 1, C.BAND_L)
            y += 3
        if R and F.w > 3 and R.random() < 0.5:
            x0 = R.randint(0, F.w - 2)
            F.rect(x0, R.randint(0, max(0, F.h - 3)), 2, 2, C.SKIN)
        if scratches and R:
            for _ in range(2):
                x0, y0 = R.randint(0, F.w - 1), R.randint(1, max(1, F.h - 4))
                F.line(x0, y0, x0 + 3, y0 + 2, C.SCRATCH, 1)
    return f


def diamond(col, edge, cx=0.5, cy=0.5, s=0.32):
    def f(F):
        W, H = F.w, F.h
        r = s * min(W, H)
        pts = [(cx * W, cy * H - r * 1.3), (cx * W + r, cy * H), (cx * W, cy * H + r * 1.3), (cx * W - r, cy * H)]
        F.poly(pts, edge)
        F.poly([(p[0] * 0.8 + cx * W * 0.2, p[1] * 0.8 + cy * H * 0.2) for p in pts], col)
        F.line(cx * W - r * 0.4, cy * H, cx * W + r * 0.4, cy * H, edge, 1)  # stitch
    return f


def face_p1(C):
    def f(F):
        W, H = F.w, F.h
        for y in range(H):
            for x in range(W):
                F.px(x, y, mix(C.SKIN, C.SKIN_D, max(0, (0.45 - y / H) / 0.45) * 0.8))
        # eyes hidden: just thin closed-lid lines peeking under the fringe
        for cx in (0.3 * W, 0.7 * W):
            F.line(cx - 0.12 * W, 0.5 * H, cx + 0.12 * W, 0.53 * H, C.LID, max(1, W * 0.03))
        F.disc(0.24 * W, 0.66 * H, 0.08 * W, mix(C.SKIN, C.BLUSH, 0.6))
        F.disc(0.76 * W, 0.66 * H, 0.08 * W, mix(C.SKIN, C.BLUSH, 0.6))
        F.line(0.5 * W, 0.6 * H, 0.52 * W, 0.66 * H, C.SKIN_D, 1)
        F.line(0.42 * W, 0.8 * H, 0.58 * W, 0.79 * H, C.LID, 1.2)  # flat, tired mouth
    return f


def face_p2(C):
    def f(F):
        W, H = F.w, F.h
        F.rect(0, 0, W, H, C.BODY)
        for cx, s in ((0.3 * W, 1), (0.7 * W, -1)):  # angry red slanted eyes
            ey = 0.42 * H
            F.poly([(cx - 0.15 * W, ey - (0.07 * H if s > 0 else 0)), (cx + 0.15 * W, ey - (0.07 * H if s < 0 else 0)),
                    (cx + 0.11 * W, ey + 0.07 * H), (cx - 0.11 * W, ey + 0.07 * H)], C.EYE, glow=True)
            F.rect(cx - 0.03 * W, ey - 0.03 * H, max(1, 0.06 * W), 0.08 * H, 0xFFC0C8, glow=True)
        top = [(0.14 * W + i * 0.072 * W, 0.6 * H + 0.03 * H * math.sin(math.pi * i / 10)) for i in range(11)]
        bot = [(0.86 * W - i * 0.072 * W, 0.66 * H + 0.17 * H * math.sin(math.pi * i / 10)) for i in range(11)]
        F.poly(top + bot, C.TEETH, glow=True)
        for i in range(1, 14):
            x = 0.15 * W + i * 0.052 * W
            F.line(x, 0.6 * H, x, 0.82 * H, C.TEETH_D, 1)
        F.line(0.15 * W, 0.7 * H, 0.85 * W, 0.7 * H, C.BODY, 1)
    return f


def wing_paint(C, R):
    def f(F):
        W, H = F.w, F.h
        for y in range(H):
            for x in range(W):
                u, v = (x + .5) / W * 2 - 1, (y + .5) / H
                half = math.sin(math.pi * min(1, v * 1.02)) ** 0.7  # teardrop, root at v=1 (bottom)
                if abs(u) > half:
                    F.px(x, y, CLEAR)
                elif abs(u) > half - 2.2 / W * 2:
                    F.px(x, y, C.WING_V)
                else:
                    F.px(x, y, mix(C.WING, C.WING_D, v * 0.6))
        for k in range(3):  # veins fanning from the root
            x0 = W / 2
            F.line(x0, H - 1, x0 + (k - 1) * W * 0.3, H * 0.15, C.WING_V, 1)
    return f


def solid(col):
    return lambda F: F.rect(0, 0, F.w, F.h, col)


# ================================================================== PHASE 1 model
SP_REST = {}  # spike rest rotations (built into the groups)


def build_p1(B):
    C = B.C
    g, c, blade = B.g, B.c, B.blade
    st = B.strands(C.HAIR, C.HAIR_HI, C.HAIR_D, ink=C.HAIR_D)
    stp = B.strands(C.HAIR, C.HAIR_HI, C.HAIR_D)
    R = B.R

    g("root", (0, 0, 0))
    g("body", (0, 13, 0), "root")
    g("dress_f", (0, 17, -1.4), "body"); g("dress_b", (0, 17, 1.4), "body")
    g("dress_r", (2.2, 17, 0), "body"); g("dress_l", (-2.2, 17, 0), "body")
    g("chest", (0, 17, 0), "body")
    g("coat_b", (0, 24.5, 1.6), "chest"); g("coat_r", (2.6, 24.5, -0.4), "chest"); g("coat_l", (-2.6, 24.5, -0.4), "chest")
    g("pendant", (0, 24.8, -1.85), "chest")
    g("head", (0, 25.4, 0), "chest", rot=(0, 0, -5))
    g("hair_b", (0, 30, 2.4), "head"); g("hair_r", (2.8, 30, 0), "head"); g("hair_l", (-2.8, 30, 0), "head")
    g("bangs", (0, 30.6, -2.9), "head")
    g("crown", (0, 32.4, 0), "head", rot=(-4, 0, 12))
    g("ah0", (0.3, 32.6, 0.4), "head", rot=(8, 0, -18)); g("ah1", (0.3, 35.6, 0.4), "ah0", rot=(0, 0, -42)); g("ah2", (0.3, 38.2, 0.4), "ah1", rot=(0, 0, -55))
    g("spikes", (0, 22.6, 1.5), "chest")
    for s, k in ((1, "r"), (-1, "l")):
        for i, (rz, rx, y) in enumerate(((68, 18, 23.2), (90, 8, 21.9), (114, 0, 20.6))):
            SP_REST[f"spk_{k}{i}"] = (rx, -8 * s, -rz * s)
            g(f"spk_{k}{i}", (0.7 * s, y, 1.4), "spikes", rot=SP_REST[f"spk_{k}{i}"])
            ln = (12.5, 14.0, 11.0)[i]
            g(f"spk_{k}{i}b", (0.7 * s, y + ln * 0.5, 1.4), f"spk_{k}{i}", rot=(0, 0, s * (14 - i * 12)))
    g("arm_r", (3.0, 24.4, 0), "chest", rot=(0, 0, 7)); g("fore_r", (3.0, 19.6, 0), "arm_r", rot=(-10, 0, 0)); g("hand_r", (3.0, 15.4, 0), "fore_r")
    g("arm_l", (-3.0, 24.4, 0), "chest", rot=(0, 0, -7)); g("fore_l", (-3.0, 19.6, 0), "arm_l", rot=(-10, 0, 0)); g("hand_l", (-3.0, 15.4, 0), "fore_l")
    for s, k in ((1, "r"), (-1, "l")):
        g("leg_" + k, (1.05 * s, 13, 0), "root", rot=(0, 0, (3 if s > 0 else -5)))
        g("shin_" + k, (1.05 * s, 7, 0), "leg_" + k)
        g("foot_" + k, (1.05 * s, 1.3, 0), "shin_" + k)

    # ---- legs: bandaged, scratched, black sandals
    for s, k in ((1, "r"), (-1, "l")):
        x = 1.05 * s
        bp = bandage(C, True, R)
        c("thigh_" + k, "leg_" + k, (x - 0.78, 6.8, -0.78), (x + 0.78, 13.4, 0.78), C.BAND, faces=B.all(bp, skip=("up", "down")))
        c("knee_" + k, "shin_" + k, (x - 0.8, 6.2, -0.85), (x + 0.8, 7.4, 0.7), C.BAND_D)
        c("calf_" + k, "shin_" + k, (x - 0.7, 1.3, -0.7), (x + 0.7, 7.1, 0.7), C.BAND, faces=B.all(bandage(C, True, R), skip=("up", "down")))
        c("ankle_" + k, "shin_" + k, (x - 0.78, 1.4, -0.78), (x + 0.78, 2.2, 0.78), C.BLACK, faces=B.all(lambda F: F.rect(0, 0, F.w, 1, C.BLACK_HI)))
        c("sole_" + k, "foot_" + k, (x - 0.9, 0, -2.3), (x + 0.9, 0.45, 1.0), C.BLACK, faces={"up": solid(C.BLACK_HI)})
        c("heelstrap_" + k, "foot_" + k, (x - 0.82, 0.4, 0.3), (x + 0.82, 1.4, 0.95), C.BLACK)
        c("foot_" + k, "foot_" + k, (x - 0.72, 0.45, -2.1), (x + 0.72, 1.3, 0.6), C.SKIN, color2=C.SKIN_D, grad=True)
        c("strap_" + k, "foot_" + k, (x - 0.8, 0.45, -1.5), (x + 0.8, 1.4, -0.9), C.BLACK, faces={"north": lambda F: F.rect(0, 0, F.w, 1, C.BLACK_HI)})
        c("toestrap_" + k, "foot_" + k, (x - 0.1, 0.45, -2.15), (x + 0.1, 1.2, -1.5), C.BLACK)
    c("ring", "shin_r", (1.95, 1.2, -0.25), (2.15, 1.9, 0.25), C.BLACK_HI)
    c("ring2", "shin_r", (1.95, 0.9, -0.1), (2.15, 1.25, 0.1), C.BLACK_HI)

    # ---- skirt: long, ragged, patched; grey under-layer peeks out on her left
    c("hips", "body", (-2.1, 12.6, -1.3), (2.1, 17.2, 1.3), C.SKIRT_D)
    skp = combo(B.folds(C.SKIRT, C.SKIRT_D, C.SKIRT_HI, 3))
    c("sk_front", "dress_f", (-2.6, 7.6, -1.75), (2.6, 17.2, -1.35), C.SKIRT, origin=(0, 17, -1.4), rot=(5, 0, 0),
      faces={"north": combo(skp, diamond(C.PATCH, C.PATCH_D, 0.72, 0.45, 0.22), lambda F: F.line(0, F.h * 0.4, F.w * 0.5, F.h * 0.38, C.SKIRT_HI, 1)), "south": skp})
    c("sk_back", "dress_b", (-2.6, 6.6, 1.35), (2.6, 17.2, 1.75), C.SKIRT, origin=(0, 17, 1.4), rot=(-5, 0, 0),
      faces={"south": combo(skp, diamond(C.PATCH, C.PATCH_D, 0.3, 0.5, 0.2)), "north": skp})
    c("sk_right", "dress_r", (2.15, 7.4, -1.6), (2.55, 17.2, 1.6), C.SKIRT, origin=(2.2, 17, 0), rot=(0, 0, 6),
      faces={"east": combo(skp, diamond(C.PATCH, C.PATCH_D, 0.5, 0.35, 0.25))})
    c("sk_left", "dress_l", (-2.55, 7.0, -1.6), (-2.15, 17.2, 1.6), C.SKIRT, origin=(-2.2, 17, 0), rot=(0, 0, -6), faces={"west": skp})
    for i, (x, z, ry) in enumerate([(2.25, -1.45, 45), (-2.25, -1.45, -45), (2.25, 1.45, -45), (-2.25, 1.45, 45)]):
        bone = "dress_f" if z < 0 else "dress_b"
        sx, sz = (1 if x > 0 else -1), (1 if z > 0 else -1)
        c(f"sk_corner{i}", bone, (x - 0.7, 7.8, z - 0.2), (x + 0.7, 17.0, z + 0.2), C.SKIRT_D, origin=(x, 17, z), rot=(-sz * 5, ry, sx * 6))
    # ragged hem points
    for i in range(6):
        x = -2.2 + i * 0.88
        B.lock(f"hem_f{i}", "dress_f", (x, 7.9, -1.55), 1.6 + (i * 7 % 3) * 0.7, 0.9, 0.3, (5, 0, (i - 2.5) * 7), C.SKIRT, C.SKIRT_D)
        B.lock(f"hem_b{i}", "dress_b", (x, 6.9, 1.55), 1.8 + (i * 5 % 3) * 0.8, 0.9, 0.3, (-5, 0, (i - 2.5) * 7), C.SKIRT, C.SKIRT_D)
    for i in range(3):
        B.lock(f"hem_r{i}", "dress_r", (2.35, 7.7, -1.0 + i), 1.5 + i * 0.5, 0.3, 0.9, (0, 0, 8), C.SKIRT, C.SKIRT_D)
        B.lock(f"under_l{i}", "dress_l", (-2.45, 7.4, -1.1 + i * 1.1), 2.2 + (i % 2) * 1.2, 0.3, 1.0, (0, 0, -10 - i * 4), C.UNDER, C.CAPE_D)
    c("sk_stitch", "dress_f", (-2.0, 12.2, -1.8), (2.0, 12.4, -1.7), C.SKIRT_HI, origin=(0, 17, -1.4), rot=(5, 0, 0))

    # ---- torso: grey top, waistband, cape
    c("waist", "chest", (-2.0, 16.8, -1.25), (2.0, 18.4, 1.25), C.SKIRT, faces={"north": lambda F: F.rect(0, F.h - 2, F.w, 1, C.SKIRT_HI)})
    c("torso", "chest", (-2.15, 18.2, -1.2), (2.15, 24.0, 1.2), C.CAPE_D, faces={"north": B.folds(C.CAPE_D, C.SKIRT_D, C.CAPE, 2)})
    c("collar", "chest", (-1.2, 23.6, -1.1), (1.2, 25.6, 1.1), C.CAPE, faces=B.all(lambda F: [F.rect(0, int(F.h * q), F.w, 1, C.CAPE_D) for q in (0.35, 0.7)], skip=("up", "down")))
    cp = B.folds(C.CAPE, C.CAPE_D, C.CAPE_HI, 3)

    def cape_front(F):
        cp(F)
        W, H = F.w, F.h
        F.line(0.3 * W, 0, 0.48 * W, 0.62 * H, C.LID, 1)  # cord
        F.line(0.7 * W, 0, 0.52 * W, 0.62 * H, C.LID, 1)
        diamond(C.PATCH, C.PATCH_D, 0.8, 0.3, 0.18)(F)
        F.line(0.05 * W, 0.15 * H, 0.2 * W, 0.2 * H, C.CAPE_D, 1)
    c("cape_sh", "chest", (-3.4, 21.0, -1.8), (3.4, 25.0, 1.8), C.CAPE, faces={"north": cape_front, "south": combo(cp, diamond(C.UNDER, C.CAPE_D, 0.25, 0.5, 0.2)), "east": cp, "west": cp, "up": solid(C.CAPE_HI)})
    for s, k in ((1, "r"), (-1, "l")):
        bx = "coat_" + k
        for i in range(4):
            x = s * (0.9 + i * 0.75)
            B.lock(f"cape_f{k}{i}", bx, (x, 21.2, -1.7), 1.8 + (i % 2) * 1.4, 0.95, 0.3, (4, 0, s * (5 + i * 6)), C.CAPE, C.CAPE_D)
        for i in range(2):
            B.lock(f"cape_s{k}{i}", bx, (s * 3.3, 21.2, -0.9 + i * 1.6), 2.2 + i * 1.0, 0.3, 1.2, (0, 0, s * 10), C.CAPE, C.CAPE_D)
    for i in range(6):
        B.lock(f"cape_b{i}", "coat_b", (-2.8 + i * 1.1, 21.2, 1.7), 2.0 + (i * 5 % 3) * 0.9, 1.0, 0.3, (-6, 0, (i - 2.5) * 6), C.CAPE, C.CAPE_D)
    # pendant: brown warning triangle on a cord
    def tri(F):
        W, H = F.w, F.h
        F.rect(0, 0, W, H, CLEAR)
        F.poly([(W / 2, 0), (W, H), (0, H)], C.PEND_D)
        F.poly([(W / 2, 2), (W - 1.8, H - 1), (1.8, H - 1)], C.PEND)
        F.rect(W / 2 - 0.7, H * 0.4, 1.4, H * 0.3, C.PEND_D)
        F.rect(W / 2 - 0.7, H * 0.78, 1.4, 1, C.PEND_D)
    c("pend_plate", "pendant", (-1.15, 19.6, -2.0), (1.15, 21.8, -1.85), C.PEND, faces={"north": tri, "south": tri, "east": solid(CLEAR), "west": solid(CLEAR), "up": solid(CLEAR), "down": solid(C.PEND_D)})
    c("pend_bail", "pendant", (-0.2, 21.7, -1.98), (0.2, 22.2, -1.87), C.LID)

    # ---- arms: bandaged, ragged grey cuffs
    for s, k in ((1, "r"), (-1, "l")):
        x = 3.0 * s
        c("upper_" + k, "arm_" + k, (x - 0.72, 19.5, -0.72), (x + 0.72, 24.8, 0.72), C.BAND, faces=B.all(bandage(C, False, R), skip=("up", "down")))
        c("shoulder_" + k, "arm_" + k, (x - 0.95, 22.6, -1.0), (x + 0.95, 25.1, 1.0), C.CAPE, faces={"up": solid(C.CAPE_HI)})
        c("fore_" + k, "fore_" + k, (x - 0.66, 15.3, -0.66), (x + 0.66, 19.8, 0.66), C.BAND, faces=B.all(bandage(C, False, R), skip=("up", "down")))
        c("cuff_" + k, "fore_" + k, (x - 0.88, 16.2, -0.88), (x + 0.88, 18.6, 0.88), C.CAPE, faces=B.all(B.folds(C.CAPE, C.CAPE_D, C.CAPE_HI, 1), skip=("up", "down")))
        for i in range(3):
            B.lock(f"shred_{k}{i}", "fore_" + k, (x + (i - 1) * 0.55, 16.4, -0.6 + i * 0.6), 1.6 + i * 0.6, 0.6, 0.25, (0, 0, (i - 1) * 16), C.CAPE, C.CAPE_D)
        c("hand_" + k, "hand_" + k, (x - 0.58, 13.5, -0.55), (x + 0.58, 15.5, 0.55), C.SKIN, color2=C.SKIN_D, grad=True)
        c("thumb_" + k, "hand_" + k, (x - 0.22 - 0.42 * s, 14.0, -0.85), (x + 0.22 - 0.42 * s, 15.0, -0.45), C.SKIN_D)
        c("wrap_" + k, "hand_" + k, (x - 0.62, 14.6, -0.6), (x + 0.62, 15.3, 0.6), C.BAND_D)
    # shard prop (snapped spike tip) in the right hand
    g("shard", (3.0, 13.8, 0), "hand_r")
    blade("shardb", "shard", (3.0, 13.8, 0), 3.4, 0.6, 0.35, (-90, 0, 0), C.SPIKE, C.SPIKE_HI)
    # bandage whip (prop): 6 links hanging from the right hand
    g("band0", (3.0, 13.6, 0), "hand_r")
    prev = "band0"
    for i in range(6):
        y = 13.6 - i * 1.8
        if i:
            g(f"band{i}", (3.0, y, 0), prev); prev = f"band{i}"
        c(f"bands{i}", prev, (2.75, y - 1.9, -0.12), (3.25, y, 0.12), C.BAND, faces=B.all(lambda F: [F.rect(0, j, F.w, 1, C.BAND_D) for j in range(0, F.h, 3)]))
    c("band_end", prev, (2.7, 13.6 - 6 * 1.8 - 0.6, -0.15), (3.3, 13.6 - 6 * 1.8 + 0.1, 0.15), C.BAND_D)

    # ---- head
    c("skull", "head", (-2.8, 25.6, -2.7), (2.8, 31.0, 2.7), C.SKIN, faces={"north": face_p1(C)})
    c("jaw", "head", (-1.8, 25.3, -2.5), (1.8, 25.8, 0.6), C.SKIN_D)
    c("hair_cap", "head", (-3.1, 28.9, -3.0), (3.1, 32.4, 3.0), C.HAIR, faces=B.all(st))
    c("hair_top", "head", (-2.6, 32.2, -2.5), (2.6, 33.0, 2.6), C.HAIR, faces=B.all(stp))
    c("hair_back", "hair_b", (-3.2, 26.0, 1.5), (3.2, 30.4, 3.3), C.HAIR, faces=B.all(st))
    for i, (x, ln, rz) in enumerate([(-2.4, 2.8, 160), (-1.0, 3.4, 176), (0.6, 3.2, 186), (2.2, 2.6, 204)]):
        blade(f"hb{i}", "hair_b", (x, 27.0, 2.7), ln, 1.8, 0.8, (-14, 0, rz), C.HAIR, C.HAIR_D, paint=stp)
    for s, k in ((1, "r"), (-1, "l")):
        x0, x1 = (2.6, 3.4) if s > 0 else (-3.4, -2.6)
        c("side_" + k, "hair_" + k, (x0, 26.2, -2.3), (x1, 30.4, 2.4), C.HAIR, faces=B.all(st))
        # messy flicks outward at jaw level (strong on both sides in the art)
        for i, (y, z, ln, rz) in enumerate([(30.0, -1.0, 2.4, 70), (28.6, 0.6, 3.0, 100), (27.4, -1.2, 3.0, 128), (26.6, 1.0, 2.8, 140), (26.4, -0.2, 2.6, 120)]):
            blade(f"hs_{k}{i}", "hair_" + k, (3.0 * s, y, z), ln, 1.6, 0.8, (0, 0, -rz * s), C.HAIR, C.HAIR_D, paint=stp)
    # bangs cover the eyes
    c("fringe", "bangs", (-3.05, 29.2, -3.1), (3.05, 31.0, -2.65), C.HAIR, faces=B.all(st))
    for i, (x, ln, rz) in enumerate([(-2.5, 2.4, 8), (-1.4, 2.9, 2), (-0.2, 2.6, -6), (1.0, 3.0, -10), (2.2, 2.5, -16)]):
        B.lock(f"bang{i}", "bangs", (x, 29.6, -2.95), ln, 1.4, 0.4, (8, 0, rz), C.HAIR, C.HAIR_D, paint=stp)
    # ahoge
    c("ahs0", "ah0", (0.0, 32.6, 0.1), (0.6, 35.8, 0.7), C.HAIR, faces=B.all(stp))
    c("ahs1", "ah1", (0.05, 35.6, 0.15), (0.55, 38.4, 0.65), C.HAIR, faces=B.all(stp))
    c("ahs2", "ah2", (0.1, 38.2, 0.2), (0.5, 40.4, 0.6), C.HAIR_D)
    # crown
    c("crown_band", "crown", (-2.6, 32.0, -2.6), (2.6, 33.0, 2.6), C.BLACK, faces=B.all(lambda F: F.rect(0, 0, F.w, 1, C.BLACK_HI)))
    for i, (ang, ln, w) in enumerate([(0, 3.6, 1.5), (55, 2.8, 1.2), (-55, 2.8, 1.2), (115, 2.4, 1.1), (-115, 2.4, 1.1), (180, 2.6, 1.2)]):
        a = math.radians(ang)
        bx, bz = -math.sin(a) * 2.3, -math.cos(a) * 2.3
        blade(f"cpt{i}", "crown", (bx, 32.9, bz), ln, w, 0.4, (-10 * math.cos(a), -ang, 10 * math.sin(a)), C.BLACK, C.BLACK_HI)

    # ---- back spikes: long, curved, black
    sp = lambda F: (F.rect(0, 0, F.w, F.h, C.SPIKE), F.rect(0, 0, 1, F.h, C.SPIKE_HI))
    for s, k in ((1, "r"), (-1, "l")):
        for i in range(3):
            y = (23.2, 21.9, 20.6)[i]
            ln = (12.5, 14.0, 11.0)[i]
            o = (0.7 * s, y, 1.4)
            c(f"spkA_{k}{i}", f"spk_{k}{i}", (o[0] - 0.65, y - 0.3, 1.0), (o[0] + 0.65, y + ln * 0.5, 1.8), C.SPIKE, faces=B.all(sp))
            blade(f"spkB_{k}{i}", f"spk_{k}{i}b", (o[0], y + ln * 0.5 - 0.1, 1.4), ln * 0.5, 0.95, 0.6, (0, 0, 0), C.SPIKE, C.SPIKE_HI, paint=sp)
            blade(f"spkC_{k}{i}", f"spk_{k}{i}", (o[0], y + ln * 0.2, 1.4), 2.0, 0.5, 0.4, (0, 0, -s * 50), C.SPIKE, C.SPIKE_HI)  # thorn
    c("spike_root", "spikes", (-1.2, 20.0, 1.2), (1.2, 24.0, 1.9), C.SPIKE)


# ================================================================== animation helpers
class DA(A):
    """A with spike helpers; rest dict empty (rest pose is built in), props hidden unless shown"""

    def spk(self, t, spread=0, lift=0, back=0, curl=0, only=None, **over):
        """offsets for all six spikes: spread = extra outward fan (deg), lift = raise tips, back = sweep tips backward, curl = tip bend"""
        for s, k in ((1, "r"), (-1, "l")):
            for i in range(3):
                b = f"spk_{k}{i}"
                if only and b not in only: continue
                v = over.get(b, (back, 0, -s * spread + s * lift))
                self.rot(b, (t, *v))
                self.rot(b + "b", (t, 0, 0, s * curl))
        return self

    def fwd(self, t, b, yaw=0, curl=0):
        """point spike b straight forward (final -90,yaw,0) expressed as offset from its rest"""
        rx, ry, rz = SP_REST[b]
        self.rot(b, (t, -95 - rx, yaw - ry, -rz))
        self.rot(b + "b", (t, 0, 0, -SP_REST[b][2] / abs(SP_REST[b][2]) * curl if curl else 0))
        return self


def anims_p1(B):
    def mk(name, ticks, loop=False):
        return DA(B, name, ticks, {}, PROPS1, loop)

    def legs0(a, t):
        a.at(t, leg_r=(0, 0, 0), leg_l=(0, 0, 0), shin_r=(0, 0, 0), shin_l=(0, 0, 0))

    # ---------------- idle (80): slouched, weight on one leg, breathing, spikes slowly flex like fingers
    a = mk("idle", 80, loop=True)
    for t, j in ((0, 0), (20, 1), (40, 0), (60, -1), (80, 0)):
        a.at(t, chest=(1.5 * abs(j), 2 * j, 0), head=(-2 + abs(j) * 2, 4 * j, -2 * j), P_body=(0, -0.1 * abs(j), 0), body=(0, 0, 1),
             arm_r=(2 * abs(j), 0, 2 + j), arm_l=(2 * abs(j), 0, -2 + j), fore_r=(3 * abs(j), 0, 0), fore_l=(3 * abs(j), 0, 0))
        a.spk(t, spread=4 * j, lift=3 * abs(j), curl=6 * abs(j))
    a.hair([(0, 0, 0, 1), (20, 2, 0, -1), (40, 0, 0, 1), (60, 2, 0, -1), (80, 0, 0, 1)], delay=5)
    a.cloth([(0, 0, 0, 0.5), (20, 1, 0, -0.5), (40, 0, 0, 0.5), (60, 1, 0, -0.5), (80, 0, 0, 0.5)], delay=5)
    for p in PROPS1: a.scl(p, (0, *HIDE))
    a.done(base_layer=True)

    # ---------------- walk (20): slouchy shuffling stride, arms dangling, spikes bob
    a = mk("walk", 20, loop=True)
    a.rot("leg_r", (0, 24, 0, 0), (5, 0, 0, 0), (10, -22, 0, 0), (15, 0, 0, 0), (20, 24, 0, 0))
    a.rot("shin_r", (0, -4, 0, 0), (10, -8, 0, 0), (13, -44, 0, 0), (17, -20, 0, 0), (20, -4, 0, 0))
    a.rot("foot_r", (0, -10, 0, 0), (10, 12, 0, 0), (20, -10, 0, 0))
    a.rot("leg_l", (0, -22, 0, 0), (5, 0, 0, 0), (10, 24, 0, 0), (15, 0, 0, 0), (20, -22, 0, 0))
    a.rot("shin_l", (0, -8, 0, 0), (3, -44, 0, 0), (7, -20, 0, 0), (10, -4, 0, 0), (20, -8, 0, 0))
    a.rot("foot_l", (0, 12, 0, 0), (10, -10, 0, 0), (20, 12, 0, 0))
    a.pos("body", (0, 0, -0.4, 0), (5, 0, 0.2, 0), (10, 0, -0.4, 0), (15, 0, 0.2, 0), (20, 0, -0.4, 0))
    a.rot("body", (0, -4, 6, 0), (10, -4, -6, 0), (20, -4, 6, 0))
    a.rot("chest", (0, 4, -6, 0), (10, 4, 6, 0), (20, 4, -6, 0))
    a.rot("head", (0, 2, 4, 0), (10, 2, -4, 0), (20, 2, 4, 0))
    a.rot("arm_r", (0, -18, 0, 0), (10, 18, 0, 0), (20, -18, 0, 0))
    a.rot("arm_l", (0, 18, 0, 0), (10, -18, 0, 0), (20, 18, 0, 0))
    a.rot("fore_r", (0, 0, 0, 0), (10, 12, 0, 0), (20, 0, 0, 0))
    a.rot("fore_l", (0, 12, 0, 0), (10, 0, 0, 0), (20, 12, 0, 0))
    for t, j in ((0, 1), (5, 0), (10, -1), (15, 0), (20, 1)):
        a.spk(t, lift=4 * j, back=6, curl=4)
    a.hair([(0, -4, 0, 2), (5, -6, 0, 0), (10, -4, 0, -2), (15, -6, 0, 0), (20, -4, 0, 2)], delay=2)
    a.cloth([(0, -6, 0, 3), (5, -9, 0, 0), (10, -6, 0, -3), (15, -9, 0, 0), (20, -6, 0, 3)], delay=1)
    a.done(base_layer=True)

    # ---------------- spike_lash (38): coil 0-8, RIGHT spikes sweep 11, LEFT spikes sweep 18, gather 22, lunge 25 + STAB 27, recover
    a = mk("spike_lash", 38)
    a.at(0, chest=(0, 0, 0), P_body=(0, 0, 0))
    a.at(7, chest=(-6, 34, 0), head=(4, -20, 4), arm_r=(10, 0, 30), arm_l=(-10, 0, -20), P_body=(0, -0.6, 0.4))
    a.spk(0).spk(7, only=("spk_r0", "spk_r1", "spk_r2"), back=40, spread=-10, curl=-10)
    a.spk(7, only=("spk_l0", "spk_l1", "spk_l2"), back=10, curl=4)
    a.at(11, chest=(-8, -30, 0), head=(2, 18, -2), arm_r=(-20, 0, 40), arm_l=(10, 0, -30), P_body=(0, -0.8, -0.4))
    for i, b in enumerate(("spk_r0", "spk_r1", "spk_r2")):
        a.rot(b, (11, -70 + i * 10, -60, 20)).rot(b + "b", (9, 0, 0, -20), (12, 0, 0, 25))
    a.at(14, chest=(-6, -34, 0), head=(2, 20, 0))
    a.spk(15, only=("spk_r0", "spk_r1", "spk_r2"), back=-20, spread=-30, curl=10)
    a.spk(14, only=("spk_l0", "spk_l1", "spk_l2"), back=40, spread=-10, curl=10)
    a.at(18, chest=(-8, 30, 0), head=(2, -18, 2), arm_l=(-20, 0, -40), arm_r=(10, 0, 20), P_body=(0, -0.8, -0.6))
    for i, b in enumerate(("spk_l0", "spk_l1", "spk_l2")):
        a.rot(b, (18, -70 + i * 10, 60, -20)).rot(b + "b", (16, 0, 0, 20), (19, 0, 0, -25))
    a.at(22, chest=(6, 0, 0), head=(-6, 0, -2), arm_r=(30, 0, 10), arm_l=(30, 0, -10), P_body=(0, -0.2, 0.6))
    a.spk(22, back=40, spread=-30, curl=-12)
    for b in SP_REST:
        a.fwd(27, b, yaw=(6 if "_r" in b else -6))
        a.fwd(31, b, yaw=(4 if "_r" in b else -4))
    a.scl("spikes", (0, 1, 1, 1), (24, 1, 1, 1), (27, 1.0, 1.0, 1.35), (31, 1, 1, 1.25), (34, 1, 1, 1))
    a.at(27, chest=(-16, 0, 0), head=(8, 0, 0), arm_r=(-30, 0, 20), arm_l=(-30, 0, -20), P_body=(0, -1.0, -2.2))
    a.at(31, chest=(-12, 0, 0), P_body=(0, -0.9, -2.0))
    a.spk(36, back=4, curl=2)
    a.at(36, chest=(-2, 0, 0), head=(0, 0, 0), arm_r=(4, 0, 0), arm_l=(4, 0, 0), P_body=(0, -0.2, -0.4))
    a.legs([(0, 0, 0, 0), (7, -8, 0, 2), (22, -4, 0, 0), (38, 0, 0, 0)], [(0, 0, 0, 0), (7, -14, 0, 0), (22, -8, 0, 0), (38, 0, 0, 0)])
    a.at(25, leg_r=(-30, 0, 2), leg_l=(22, 0, -2), shin_r=(-20, 0, 0), shin_l=(-10, 0, 0)).at(31, leg_r=(-32, 0, 2), leg_l=(24, 0, -2)).at(36, leg_r=(-8, 0, 0), leg_l=(6, 0, 0))
    a.hair([(0, 0, 0, 0), (7, 4, 0, -6), (11, -6, 0, 10), (18, -6, 0, -10), (22, 4, 0, 0), (27, -14, 0, 0), (34, 2, 0, 0), (38, 0, 0, 0)])
    a.cloth([(0, 0, 0, 0), (7, 2, 0, -3), (11, -4, 0, 6), (18, -4, 0, -6), (27, -10, 0, 0, 6), (38, 0, 0, 0)])
    a.done()

    # ---------------- spike_barrage (46): spikes rear back 0-14, fire r0 16, l0 18, r1 20, l1 22, r2 24, l2 26, recoil, retract
    a = mk("spike_barrage", 46)
    a.at(0, chest=(0, 0, 0), P_body=(0, 0, 0))
    a.at(12, chest=(14, 0, 0), head=(-10, 0, 0), arm_r=(-20, 0, 26), arm_l=(-20, 0, -26), fore_r=(30, 0, 0), fore_l=(30, 0, 0), P_body=(0, -0.6, 0.6))
    a.spk(0).spk(12, back=50, lift=20, curl=-18)
    order = ("spk_r0", "spk_l0", "spk_r1", "spk_l1", "spk_r2", "spk_l2")
    for i, b in enumerate(order):
        t = 16 + i * 2
        sgn = 1 if "_r" in b else -1
        rx, ry, rz = SP_REST[b]
        a.rot(b, (t - 2, 50, 0, -sgn * 0 + sgn * 20), (t, -95 - rx, -ry + sgn * 4, -rz), (t + 6, -95 - rx, -ry + sgn * 4, -rz), (t + 12, 40, 0, 0), (44, 0, 0, 0))
        a.rot(b + "b", (t - 2, 0, 0, -sgn * 18), (t, 0, 0, 0), (t + 12, 0, 0, sgn * 6), (44, 0, 0, 0))
        a.scl(b, (0, 1, 1, 1), (t - 0.5, 1, 1, 1), (t, 1, 1.7, 1), (t + 2, 1, 1.55, 1), (t + 6, 1, 1.0, 1), (46, 1, 1, 1))
    for t in range(16, 28, 2):
        a.at(t, chest=(8 + (t % 4) * 1.5, (3 if t % 4 == 0 else -3), 0), P_body=(0, -0.6, 0.6 + (t % 4) * 0.1))
    a.at(30, chest=(10, 0, 0), head=(-6, 0, 0))
    a.at(40, chest=(2, 0, 0), head=(0, 0, 0), arm_r=(0, 0, 4), arm_l=(0, 0, -4), fore_r=(6, 0, 0), fore_l=(6, 0, 0), P_body=(0, -0.1, 0.1))
    a.legs([(0, 0, 0, 0), (12, 10, 0, 4), (30, 10, 0, 4), (46, 0, 0, 0)], [(0, 0, 0, 0), (12, -20, 0, 0), (30, -20, 0, 0), (46, 0, 0, 0)])
    a.hair([(0, 0, 0, 0), (12, -6, 0, 0), (16, 6, 0, 2), (20, 6, 0, -2), (24, 6, 0, 2), (30, 0, 0, 0), (46, 0, 0, 0)])
    a.cloth([(0, 0, 0, 0), (12, 2, 0, 0, 4), (16, -4, 0, 0, 6), (26, -4, 0, 0, 6), (40, 0, 0, 0)])
    a.done()

    # ---------------- spike_impale (42): spikes braid behind 0-14 (crouch), LUNGE 19 one giant lance, hold, wrench free 28, retract
    a = mk("spike_impale", 42)
    a.at(0, chest=(0, 0, 0), P_body=(0, 0, 0))
    a.at(14, chest=(20, 0, 0), head=(-14, 0, 0), arm_r=(-30, 0, 30), arm_l=(-30, 0, -30), P_body=(0, -1.6, 1.2))
    a.spk(0).spk(8, back=40, spread=-40, curl=-10).spk(14, back=70, spread=-70, curl=-20)
    for b in SP_REST:
        a.fwd(19, b, yaw=(-3 if "_r" in b else 3)).fwd(26, b, yaw=(-3 if "_r" in b else 3))
    a.scl("spikes", (0, 1, 1, 1), (17, 1, 1, 1), (19, 0.6, 0.6, 1.9), (26, 0.6, 0.6, 1.8), (30, 1, 1, 1))
    a.at(19, chest=(-22, 0, 0), head=(14, 0, 0), arm_r=(-50, 0, 20), arm_l=(-50, 0, -20), P_body=(0, -1.2, -2.6))
    a.at(26, chest=(-20, 0, 0), P_body=(0, -1.1, -2.4))
    a.at(29, chest=(10, -10, 0), head=(-8, 6, 0), P_body=(0, -0.4, -1.0))
    a.spk(30, back=30, curl=6).spk(38, back=4)
    a.at(38, chest=(0, 0, 0), head=(0, 0, 0), arm_r=(0, 0, 0), arm_l=(0, 0, 0), P_body=(0, 0, -0.2))
    a.rot("leg_r", (0, 0, 0, 0), (14, 30, 0, 0), (19, -40, 0, 0), (26, -40, 0, 0), (34, -10, 0, 0), (42, 0, 0, 0))
    a.rot("shin_r", (0, 0, 0, 0), (14, -50, 0, 0), (19, -10, 0, 0), (34, -6, 0, 0), (42, 0, 0, 0))
    a.rot("leg_l", (0, 0, 0, 0), (14, 10, 0, 0), (19, 30, 0, 0), (26, 30, 0, 0), (34, 8, 0, 0), (42, 0, 0, 0))
    a.rot("shin_l", (0, 0, 0, 0), (14, -40, 0, 0), (19, -30, 0, 0), (34, -6, 0, 0), (42, 0, 0, 0))
    a.hair([(0, 0, 0, 0), (14, 6, 0, 0), (19, -16, 0, 0), (26, -6, 0, 0), (30, 6, 0, 0), (42, 0, 0, 0)])
    a.cloth([(0, 0, 0, 0), (14, 4, 0, 0, 4), (19, -12, 0, 0, 8), (28, -2, 0, 0), (42, 0, 0, 0)])
    a.done()

    # ---------------- blink_stab (34): sink into her shadow 0-9, (teleport 9) rise behind 10-14, coil, STAB 20 lower spikes, recover
    a = mk("blink_stab", 34)
    a.scl("root", (0, 1, 1, 1), (4, 1.1, 0.9, 1.1), (8, 1.5, 0.06, 1.5), (9.9, 0.4, 0.02, 0.4), (10, 0.4, 0.02, 0.4), (13, 0.9, 1.15, 0.9), (14.5, 1, 1, 1), (34, 1, 1, 1))
    a.at(0, chest=(0, 0, 0), P_body=(0, 0, 0))
    a.at(5, chest=(-24, 0, 0), head=(16, 0, 0), arm_r=(-10, 0, 40), arm_l=(-10, 0, -40), P_body=(0, -1.8, 0))
    a.spk(0).spk(5, lift=-30, back=40)
    a.at(13, chest=(10, 0, 0), head=(-10, 0, 0), arm_r=(10, 0, 20), arm_l=(10, 0, -20), P_body=(0, 0.4, 0))
    a.spk(13, spread=30, lift=30, curl=20)
    a.at(17, chest=(12, 20, 0), head=(-6, -14, 0), P_body=(0, -0.8, 0.6))
    for b in ("spk_r2", "spk_l2", "spk_r1", "spk_l1"):
        a.fwd(20, b, yaw=(-4 if "_r" in b else 4)).fwd(24, b)
    a.spk(17, back=50, spread=-20, curl=-10, only=("spk_r1", "spk_l1", "spk_r2", "spk_l2"))
    a.spk(20, lift=40, only=("spk_r0", "spk_l0"))
    a.scl("spk_r2", (0, 1, 1, 1), (18, 1, 1, 1), (20, 1, 1.6, 1), (24, 1, 1.4, 1), (28, 1, 1, 1))
    a.scl("spk_l2", (0, 1, 1, 1), (18, 1, 1, 1), (20, 1, 1.6, 1), (24, 1, 1.4, 1), (28, 1, 1, 1))
    a.at(20, chest=(-18, -6, 0), head=(10, 4, 0), arm_r=(30, 0, 30), arm_l=(30, 0, -30), P_body=(0, -1.0, -1.6))
    a.at(24, chest=(-14, -4, 0), P_body=(0, -0.9, -1.4))
    a.spk(30, back=6)
    a.at(30, chest=(-2, 0, 0), head=(0, 0, 0), arm_r=(0, 0, 0), arm_l=(0, 0, 0), P_body=(0, -0.2, -0.3))
    a.legs([(0, 0, 0, 0), (5, 20, 0, 6), (13, 0, 0, 0), (17, 16, 0, 4), (20, -20, 0, 0), (28, -4, 0, 0), (34, 0, 0, 0)],
           [(0, 0, 0, 0), (5, -40, 0, 0), (13, 0, 0, 0), (17, -30, 0, 0), (20, -10, 0, 0), (34, 0, 0, 0)])
    a.hair([(0, 0, 0, 0), (5, -12, 0, 0), (13, 16, 0, 0), (17, 6, 0, 4), (20, -12, 0, 0), (28, 2, 0, 0), (34, 0, 0, 0)], delay=1)
    a.cloth([(0, 0, 0, 0), (5, -4, 0, 0, 10), (13, 6, 0, 0, 12), (20, -10, 0, 0, 6), (34, 0, 0, 0)], delay=1)
    a.done()

    # ---------------- pendant_pulse (40): grabs the pendant 4-10, raises it 14, PULSE 18 (arms flung out, head back), spikes flare, recover
    a = mk("pendant_pulse", 40)
    a.at(0, chest=(0, 0, 0), arm_r=(0, 0, 0), P_body=(0, 0, 0))
    a.at(8, chest=(-10, 0, 0), head=(14, 0, 0), arm_r=(60, 0, -40), fore_r=(70, 0, 0), arm_l=(20, 0, -10), P_body=(0, -0.6, 0))
    a.rot("pendant", (0, 0, 0, 0), (8, -20, 0, 0), (14, -70, 0, 0), (18, -40, 0, 0), (24, 10, 0, 0), (30, 0, 0, 0))
    a.at(14, chest=(6, 0, 0), head=(0, 0, 0), arm_r=(120, 0, -20), fore_r=(30, 0, 0), arm_l=(30, 0, -20), P_body=(0, 0.3, 0))
    a.at(18, chest=(14, 0, 0), head=(-20, 0, 0), arm_r=(20, 0, 80), arm_l=(20, 0, -80), fore_r=(0, 0, 0), fore_l=(0, 0, 0), P_body=(0, 0.5, 0.4))
    a.spk(0).spk(14, back=20, lift=-10).spk(18, spread=24, lift=24, curl=24).spk(26, spread=10, lift=10, curl=10).spk(36, back=0)
    a.at(24, chest=(8, 0, 0), head=(-10, 0, 0), arm_r=(16, 0, 60), arm_l=(16, 0, -60))
    a.at(34, chest=(0, 0, 0), head=(0, 0, 0), arm_r=(4, 0, 6), arm_l=(4, 0, -6), fore_r=(0, 0, 0), fore_l=(0, 0, 0), P_body=(0, 0, 0))
    a.legs([(0, 0, 0, 0), (8, -6, 0, 0), (18, 0, 0, 8), (28, 0, 0, 4), (40, 0, 0, 0)], [(0, 0, 0, 0), (8, -10, 0, 0), (18, 0, 0, 0), (40, 0, 0, 0)])
    a.hair([(0, 0, 0, 0), (8, 4, 0, 0), (18, -20, 0, 0), (22, -16, 0, 6), (26, -8, 0, -6), (34, 0, 0, 0), (40, 0, 0, 0)], delay=1)
    a.cloth([(0, 0, 0, 0), (14, 0, 0, 0, 0), (18, -6, 0, 0, 22), (24, -4, 0, 0, 14), (34, 0, 0, 0)], delay=1)
    a.done()

    # ---------------- bandage_snare (44): unwrap + swing back 4-10, FLING 12 (bandage shoots out), REEL 14-22, spikes STAB 25, recover
    a = mk("bandage_snare", 44).show("band0", 4, 30, grow=2)
    a.at(0, chest=(0, 0, 0), arm_r=(0, 0, 0), P_body=(0, 0, 0))
    a.at(6, chest=(4, -24, 0), head=(4, 16, 0), arm_r=(-40, 0, 40), fore_r=(40, 0, 0), arm_l=(20, 0, -20), P_body=(0, -0.3, 0.4))
    a.at(10, chest=(6, -36, 0), head=(4, 22, 0), arm_r=(150, 0, 40), fore_r=(30, 0, 0), P_body=(0, -0.4, 0.8))
    a.rot("band0", (4, 30, 0, 0), (10, 80, 0, 0), (12, 0, 0, 0), (16, -30, 0, 0), (22, -30, 0, 0), (24, 20, 0, 0), (30, 20, 0, 0))
    for i in range(1, 6):
        a.rot(f"band{i}", (4, 20, 0, 0), (10 + i * 0.3, 30, 0, 0), (12 + i * 0.3, -6, 0, 0), (14, 0, 0, 0), (22, 0, 0, 0), (24 + i * 0.4, 30, 0, 0), (30, 20, 0, 0))
    a.scl("band0", (0, *HIDE), (3.99, *HIDE), (6, 1, 1, 1), (11, 1, 1, 1), (12, 1, 4.2, 1), (14, 1, 4.0, 1), (22, 1, 1.0, 1), (28, 1, 1, 1), (30, *HIDE), (44, *HIDE))
    a.at(12, chest=(-10, 22, 0), head=(0, -12, 0), arm_r=(90, 0, 4), fore_r=(0, 0, 0), arm_l=(-20, 0, -20), P_body=(0, -0.5, -1.0))
    a.at(16, chest=(14, 10, 0), head=(-6, -6, 0), arm_r=(60, 0, 10), fore_r=(60, 0, 0), arm_l=(10, 0, -30), P_body=(0, -0.5, 0.8))
    a.at(22, chest=(16, 4, 0), arm_r=(30, 0, 20), fore_r=(90, 0, 0), P_body=(0, -0.6, 1.0))
    a.spk(0).spk(16, back=40, spread=-20, curl=-10).spk(22, back=60, spread=-40, curl=-16)
    for b in SP_REST:
        a.fwd(25, b, yaw=(5 if "_r" in b else -5)).fwd(29, b)
    a.scl("spikes", (0, 1, 1, 1), (23, 1, 1, 1), (25, 1, 1, 1.3), (29, 1, 1, 1.2), (32, 1, 1, 1))
    a.at(25, chest=(-14, 0, 0), head=(8, 0, 0), arm_r=(20, 0, 30), fore_r=(20, 0, 0), arm_l=(20, 0, -30), P_body=(0, -0.8, -1.2))
    a.spk(34, back=6)
    a.at(36, chest=(-2, 0, 0), head=(0, 0, 0), arm_r=(0, 0, 4), fore_r=(6, 0, 0), arm_l=(0, 0, -4), P_body=(0, -0.1, -0.2))
    a.legs([(0, 0, 0, 0), (10, 0, 0, 0), (44, 0, 0, 0)], [(0, 0, 0, 0), (10, -10, 0, 0), (25, -14, 0, 0), (44, 0, 0, 0)])
    a.at(10, leg_r=(14, 0, 2), leg_l=(-10, 0, -2)).at(12, leg_r=(-22, 0, 2), leg_l=(16, 0, -2)).at(18, leg_r=(10, 0, 2), leg_l=(-20, 0, -2)).at(25, leg_r=(-26, 0, 0), leg_l=(18, 0, 0)).at(36, leg_r=(0, 0, 0), leg_l=(0, 0, 0))
    a.hair([(0, 0, 0, 0), (10, 8, 0, 6), (12, -12, 0, -8), (18, 10, 0, 4), (25, -12, 0, 0), (36, 0, 0, 0)])
    a.cloth([(0, 0, 0, 0), (10, 4, 0, 4), (12, -8, 0, -6), (18, 6, 0, 2), (25, -8, 0, 0, 4), (44, 0, 0, 0)])
    a.done()

    # ---------------- shard_throw (34): reach back, snap a spike tip 4-8, THROW 13 (overarm), reach 17, THROW 22 (sidearm), recover
    a = mk("shard_throw", 34)
    a.scl("shard", (0, *HIDE), (6.9, *HIDE), (7.5, 1, 1, 1), (13, 1, 1, 1), (13.1, *HIDE), (17.9, *HIDE), (18.5, 1, 1, 1), (22, 1, 1, 1), (22.1, *HIDE), (34, *HIDE))
    a.at(0, chest=(0, 0, 0), arm_r=(0, 0, 0), P_body=(0, 0, 0))
    a.at(6, chest=(6, -30, 0), head=(0, 20, 0), arm_r=(150, 0, 60), fore_r=(80, 0, 0), arm_l=(30, 0, -20), P_body=(0, -0.3, 0.6))
    a.rot("spk_r0", (0, 0, 0, 0), (6, 0, 0, 0), (7, 0, 0, 14), (9, 0, 0, -6), (12, 0, 0, 0))
    a.at(9, chest=(8, -36, 0), head=(2, 24, 0), arm_r=(170, 0, 30), fore_r=(70, 0, 0), P_body=(0, -0.4, 0.8))
    a.at(13, chest=(-12, 26, 0), head=(4, -16, 0), arm_r=(60, 0, -10), fore_r=(0, 0, 0), arm_l=(-20, 0, -30), P_body=(0, -0.7, -0.9))
    a.at(17, chest=(4, -30, 0), head=(0, 18, 0), arm_r=(40, -40, 90), fore_r=(60, 0, 0), P_body=(0, -0.4, 0.4))
    a.rot("spk_r1", (0, 0, 0, 0), (16, 0, 0, 0), (17.5, 0, 0, 16), (19, 0, 0, -6), (22, 0, 0, 0))
    a.at(22, chest=(-8, 34, 0), head=(2, -20, 0), arm_r=(80, 30, -30), fore_r=(0, 0, 0), arm_l=(-10, 0, -40), P_body=(0, -0.6, -0.8))
    a.at(30, chest=(0, 0, 0), head=(0, 0, 0), arm_r=(4, 0, 4), fore_r=(6, 0, 0), arm_l=(0, 0, -4), P_body=(0, 0, 0))
    a.spk(0).spk(9, back=20, curl=-6).spk(13, back=-10, curl=8).spk(17, back=20, curl=-6).spk(22, back=-10, curl=8).spk(30, back=0)
    a.legs([(0, 0, 0, 0), (34, 0, 0, 0)], [(0, 0, 0, 0), (9, -12, 0, 0), (13, -10, 0, 0), (22, -10, 0, 0), (34, 0, 0, 0)])
    a.at(9, leg_r=(16, 0, 2), leg_l=(-10, 0, -2)).at(13, leg_r=(-24, 0, 2), leg_l=(18, 0, -2)).at(17, leg_r=(10, 0, 2), leg_l=(-10, 0, -2)).at(22, leg_r=(-22, 0, 2), leg_l=(16, 0, -2)).at(30, leg_r=(0, 0, 0), leg_l=(0, 0, 0))
    a.hair([(0, 0, 0, 0), (9, 6, 0, 6), (13, -10, 0, -8), (17, 6, 0, 6), (22, -10, 0, -10), (30, 0, 0, 0)])
    a.cloth([(0, 0, 0, 0), (9, 3, 0, 3), (13, -6, 0, -6), (17, 3, 0, 4), (22, -6, 0, -6), (34, 0, 0, 0)])
    a.done()

    # ---------------- spike_whirl (34): crouch + spikes fan flat 0-9, SPIN two turns 10-24 (hits 14, 20), stagger, recover
    a = mk("spike_whirl", 34)
    a.at(0, root=(0, 0, 0), chest=(0, 0, 0), P_root=(0, 0, 0))
    a.at(8, root=(0, -40, 0), chest=(-16, 20, 0), head=(12, -10, 0), arm_r=(20, 0, 50), arm_l=(20, 0, -50), P_root=(0, -1.2, 0))
    a.spk(0).spk(8, spread=-30, back=20).spk(11, spread=16, back=-14, curl=-20).spk(24, spread=16, back=-14, curl=-20).spk(28, back=0, curl=6).spk(34)
    a.at(11, root=(0, 0, 0), chest=(-4, 0, 0), head=(-4, 0, 0), arm_r=(0, 0, 80), arm_l=(0, 0, -80), P_root=(0, 0.4, 0))
    a.at(14, root=(0, 260, 0), P_root=(0, 0.8, 0))
    a.at(17, root=(0, 420, 0), P_root=(0, 0.5, 0))
    a.at(20, root=(0, 620, 0), P_root=(0, 0.8, 0))
    a.at(24, root=(0, 720, 0), chest=(-10, -8, 0), head=(8, 8, 0), arm_r=(20, 0, 30), arm_l=(20, 0, -30), P_root=(0, -0.4, 0))
    a.at(28, root=(0, 726, 0), chest=(-4, 4, 0), P_root=(0, 0, 0))
    a.at(34, root=(0, 720, 0), chest=(0, 0, 0), head=(0, 0, 0), arm_r=(0, 0, 0), arm_l=(0, 0, 0))
    a.legs([(0, 0, 0, 0), (8, -18, 0, 6), (11, 0, 0, 12), (24, 0, 0, 12), (28, -10, 0, 3), (34, 0, 0, 0)],
           [(0, 0, 0, 0), (8, -32, 0, 0), (11, -6, 0, 0), (24, -14, 0, 0), (34, 0, 0, 0)])
    a.hair([(0, 0, 0, 0), (8, 6, 0, 10), (12, -4, 0, -24), (24, -4, 0, -24), (28, 4, 0, 10), (34, 0, 0, 0)])
    a.cloth([(0, 0, 0, 0), (8, 0, 0, 4, 2), (12, -4, 0, -8, 24), (24, -4, 0, -8, 24), (28, 2, 0, 6, 6), (34, 0, 0, 0)])
    a.done()

    # ---------------- shadow_spikes (40): knee up 4-11 (spikes lift), STAMP 14 (spikes stab down at the floor), hold, recover
    a = mk("shadow_spikes", 40)
    a.at(0, chest=(0, 0, 0), P_body=(0, 0, 0))
    a.rot("leg_r", (0, 0, 0, 0), (6, 50, 0, 4), (11, 70, 0, 6), (14, -6, 0, 2), (24, -6, 0, 2), (34, 0, 0, 0))
    a.rot("shin_r", (0, 0, 0, 0), (6, -60, 0, 0), (11, -80, 0, 0), (14, 0, 0, 0), (40, 0, 0, 0))
    a.rot("leg_l", (0, 0, 0, 0), (11, -4, 0, -2), (14, 10, 0, -4), (24, 10, 0, -4), (34, 0, 0, 0))
    a.rot("shin_l", (0, 0, 0, 0), (11, -6, 0, 0), (14, -30, 0, 0), (24, -26, 0, 0), (34, 0, 0, 0))
    a.at(11, chest=(8, 6, 0), head=(-4, -4, 0), arm_r=(-20, 0, 40), arm_l=(30, 0, -40), fore_r=(20, 0, 0), fore_l=(20, 0, 0), P_body=(0, 0.8, 0))
    a.at(14, chest=(-24, 0, 0), head=(20, 0, 0), arm_r=(20, 0, 50), arm_l=(20, 0, -50), P_body=(0, -1.6, -0.4))
    a.at(24, chest=(-20, 0, 0), head=(18, 0, 0), P_body=(0, -1.4, -0.3))
    a.spk(0).spk(11, lift=40, back=-20, curl=16).spk(14, lift=-50, back=-30, curl=-20).spk(24, lift=-46, back=-26, curl=-16).spk(34, back=0)
    a.at(34, chest=(0, 0, 0), head=(0, 0, 0), arm_r=(0, 0, 0), arm_l=(0, 0, 0), fore_r=(0, 0, 0), fore_l=(0, 0, 0), P_body=(0, 0, 0))
    a.hair([(0, 0, 0, 0), (11, -6, 0, 0), (14, 18, 0, 0), (18, 4, 0, 0), (24, 2, 0, 0), (34, 0, 0, 0)])
    a.cloth([(0, 0, 0, 0), (11, -4, 0, 0, 2), (14, 8, 0, 0, 14), (22, 3, 0, 0, 6), (34, 0, 0, 0)])
    a.done()

    # ---------------- reveal (80, phase-1 model plays 0-50): clutch head 0-12, spasms, spikes thrash, bandages snap 20/34/44, curl up at 50
    a = mk("reveal", 80)
    a.at(0, chest=(0, 0, 0), head=(0, 0, 0), P_body=(0, 0, 0))
    a.at(8, chest=(-26, 0, 0), head=(-20, 0, 0), arm_r=(140, -30, -40), fore_r=(100, 0, 0), arm_l=(140, 30, 40), fore_l=(100, 0, 0), P_body=(0, -1.4, 0))
    for t in range(12, 48, 4):
        j = 1 if (t // 4) % 2 else -1
        big = t in (20, 32, 44)
        a.at(t, chest=(-30 + (16 if big else 0), 6 * j, 4 * j), head=(-24 + (30 if big else 0), 8 * j, 0), P_body=(0, -1.8, 0))
        a.spk(t, spread=(30 if big else 8) * j, lift=(40 if big else 10), curl=20 * j)
    a.at(50, chest=(-60, 0, 0), head=(-10, 0, 0), arm_r=(120, 40, 20), arm_l=(120, -40, -20), fore_r=(110, 0, 0), fore_l=(110, 0, 0), P_body=(0, -5.0, 0))
    a.spk(50, spread=-40, back=60, curl=-30)
    a.scl("spikes", (0, 1, 1, 1), (20, 1, 1, 1), (22, 1.3, 1.3, 1.3), (44, 1.5, 1.5, 1.5), (50, 1.8, 1.8, 1.8), (80, 1.8, 1.8, 1.8))
    a.legs([(0, 0, 0, 0), (8, 20, 0, 6), (44, 30, 0, 8), (50, 70, 0, 10), (80, 70, 0, 10)], [(0, 0, 0, 0), (8, -40, 0, 0), (44, -60, 0, 0), (50, -130, 0, 0), (80, -130, 0, 0)])
    a.hair([(0, 0, 0, 0), (8, 10, 0, 0), (20, -16, 0, 10), (32, -16, 0, -10), (44, -20, 0, 8), (50, 10, 0, 0), (80, 10, 0, 0)], delay=1)
    a.cloth([(0, 0, 0, 0), (8, 4, 0, 0, 6), (20, -6, 0, 0, 20), (32, -6, 0, 0, 20), (44, -8, 0, 0, 26), (50, 10, 0, 0, 30), (80, 10, 0, 0, 30)], delay=1)
    a.done()

    # ---------------- death (40): stagger back 0-6, knees buckle 14, spikes wilt, topple sideways 28, still
    a = mk("death", 40)
    a.at(0, chest=(0, 0, 0), head=(0, 0, 0), P_body=(0, 0, 0), root=(0, 0, 0))
    a.at(5, chest=(20, 0, 0), head=(-26, 0, 0), arm_r=(-20, 0, 40), arm_l=(-20, 0, -40), P_body=(0, 0.2, 0.6))
    a.at(14, chest=(-30, 0, 6), head=(30, 0, -10), arm_r=(10, 0, 10), arm_l=(10, 0, -10), P_body=(0, -4.0, 0))
    a.at(28, root=(0, 0, 80), P_root=(-3.0, 1.2, 0), chest=(-20, 0, 0), head=(10, 0, 10), arm_r=(20, 0, 80), arm_l=(-10, 0, -10))
    a.at(34, root=(0, 0, 90), P_root=(-3.6, 0.8, 0))
    a.at(40, root=(0, 0, 88), P_root=(-3.6, 0.8, 0))
    a.spk(0).spk(5, spread=30, lift=30, curl=20).spk(14, lift=-30, curl=-30).spk(28, lift=-50, curl=-40).spk(40, lift=-60, curl=-40)
    a.legs([(0, 0, 0, 0), (5, -10, 0, 0), (14, 60, 0, 10), (28, 30, 0, 6), (40, 24, 0, 6)], [(0, 0, 0, 0), (14, -100, 0, 0), (28, -50, 0, 0), (40, -40, 0, 0)])
    a.hair([(0, 0, 0, 0), (5, -20, 0, 0), (14, 16, 0, 0), (28, 10, 0, 20), (40, 6, 0, 20)], delay=2)
    a.cloth([(0, 0, 0, 0), (5, -8, 0, 0, 10), (14, 10, 0, 0, 20), (28, 0, 0, 16, 6), (40, 0, 0, 18, 4)])
    a.done()


PROPS1 = ("shard", "band0")


# ================================================================== PHASE 2 model (boss)
W_REST = {"wing_ur": (16, -22, -36), "wing_ul": (16, 22, 36), "wing_lr": (24, -30, -122), "wing_ll": (24, 30, 122)}


def build_p2(B):
    C = B.C
    g, c, blade = B.g, B.c, B.blade
    body = lambda F: (F.rect(0, 0, F.w, F.h, C.BODY), F.rect(0, 0, 1, F.h, C.BODY_HI))
    bd = B.all(body)
    R = B.R

    g("root", (0, 0, 0))
    g("body", (0, 14, 0), "root")
    g("chest", (0, 15, 0), "body", rot=(-8, 0, 0))
    g("head", (0, 24.4, -0.4), "chest", rot=(8, 0, -4))
    g("hair_b", (0, 29, 2.0), "head"); g("hair_r", (2.8, 29, 0), "head"); g("hair_l", (-2.8, 29, 0), "head"); g("bangs", (0, 30.4, -2.6), "head")
    g("ah0", (0.2, 31.2, 0.2), "head", rot=(4, 0, 16)); g("ah1", (0.2, 34.0, 0.2), "ah0", rot=(0, 0, 40)); g("ah2", (0.2, 36.4, 0.2), "ah1", rot=(0, 0, 60))
    g("jaw", (0, 26.6, -1.0), "head")
    g("wings", (0, 22.0, 1.0), "chest")
    for k, r in W_REST.items():
        g(k, (0.5 if k.endswith("r") else -0.5, 22.0 if k[5] == "u" else 20.6, 1.1), "wings", rot=r)
    for s, k in ((1, "r"), (-1, "l")):
        g("horn_" + k + "0", (0.7 * s, 23.2, 1.2), "chest", rot=(16, 0, -s * 6))
        for i in range(1, 6):
            g(f"horn_{k}{i}", (0.7 * s, 23.2 + i * 3.4, 1.2), f"horn_{k}{i - 1}", rot=(0, 0, -s * 31))
    g("tents", (0, 19, 1.0), "chest")
    for t in range(4):
        g(f"tent{t}_0", ((1, -1, 0.8, -0.8)[t], (20.5, 20.5, 18.0, 18.0)[t], 1.0), "tents")
        for i in range(1, 4):
            g(f"tent{t}_{i}", ((1, -1, 0.8, -0.8)[t], (20.5, 20.5, 18.0, 18.0)[t], 1.0 + i * 3), f"tent{t}_{i - 1}")
    big = {"r": 1.5, "l": 1.3}
    for s, k in ((1, "r"), (-1, "l")):
        g("arm_" + k, (2.4 * s, 22.6, 0), "chest", rot=(10, 0, s * 18))
        g("fore_" + k, (2.4 * s, 14.6, 0), "arm_" + k, rot=(-26, 0, -s * 10))
        g("hand_" + k, (2.4 * s, 6.4, 0), "fore_" + k, rot=(0, 0, 0))
        for i in range(4):
            g(f"fing_{k}{i}", (2.4 * s + (i - 1.5) * 0.7 * big[k], 3.4, -0.4 + abs(i - 1.5) * 0.2), "hand_" + k)
        g("thumb_" + k, (2.4 * s - 1.1 * s, 4.6, -0.8), "hand_" + k)
        g("leg_" + k, (1.0 * s, 14, 0), "root", rot=(-30, 0, s * 24))
        g("shin_" + k, (1.0 * s, 7.4, 0), "leg_" + k, rot=(56, 0, -s * 26))
        g("foot_" + k, (1.0 * s, 1.2, 0), "shin_" + k, rot=(-26, 0, 0))

    # torso: thin, ribbed
    c("pelvis", "body", (-1.4, 13.0, -0.9), (1.4, 15.2, 0.9), C.BODY, faces=bd)
    c("waist", "chest", (-0.9, 15.0, -0.7), (0.9, 18.4, 0.7), C.BODY, faces=bd)
    c("ribs", "chest", (-1.7, 18.2, -1.1), (1.7, 22.6, 1.1), C.BODY, faces=bd)
    c("shoulders", "chest", (-2.6, 21.8, -1.0), (2.6, 23.4, 1.0), C.BODY, faces=bd)
    c("neck", "chest", (-0.5, 23.0, -0.9), (0.5, 25.0, 0.1), C.BODY)
    for i in range(3):  # back ridge spikes
        blade(f"ridge{i}", "chest", (0, 19.0 + i * 1.4, 1.0), 1.2, 0.4, 0.3, (60, 0, 0), C.BODY, C.BODY_HI)
    # head: big round skull, face with red eyes + white grin
    c("skull", "head", (-3.0, 25.0, -2.8), (3.0, 31.2, 2.8), C.BODY, faces={"north": face_p2(C), "south": body, "east": body, "west": body, "up": body, "down": body})
    c("skull_r", "head", (2.9, 25.8, -2.2), (3.4, 30.4, 2.2), C.BODY, faces=bd)
    c("skull_l", "head", (-3.4, 25.8, -2.2), (-2.9, 30.4, 2.2), C.BODY, faces=bd)
    c("cheek", "head", (-2.4, 24.6, -2.6), (2.4, 25.2, 1.2), C.BODY)
    c("maw", "jaw", (-2.0, 25.6, -2.9), (2.0, 26.6, -2.6), C.TEETH, glow=True, faces={"north": lambda F: [F.px(x, y, C.TEETH_D, glow=True) for x in range(0, F.w, 3) for y in range(F.h)]})
    c("hair_cap", "head", (-3.2, 29.6, -3.0), (3.2, 31.8, 3.0), C.BODY, faces=bd)
    for i, (x, z, ln, rx, rz) in enumerate([(-2.0, -1.0, 2.6, -10, 30), (-0.6, -1.8, 2.2, -20, 6), (1.0, -1.2, 2.6, -14, -24), (2.2, 0.6, 2.2, 0, -50), (-2.4, 1.2, 2.4, 20, 50), (0.4, 1.6, 2.0, 30, -10)]):
        blade(f"tuft{i}", "head", (x, 31.4, z), ln, 1.4, 0.8, (rx, 0, rz), C.BODY, C.BODY_HI)
    c("hair_back", "hair_b", (-3.1, 26.0, 1.8), (3.1, 30.0, 3.1), C.BODY, faces=bd)
    for s, k in ((1, "r"), (-1, "l")):
        for i, (y, z, ln, rz) in enumerate([(29.0, -0.6, 2.2, 80), (27.6, 0.8, 2.6, 110), (26.4, -0.4, 2.0, 140)]):
            blade(f"hs_{k}{i}", "hair_" + k, (3.0 * s, y, z), ln, 1.2, 0.7, (0, 0, -rz * s), C.BODY, C.BODY_HI)
    for i, (x, rz) in enumerate([(-1.6, 10), (0.2, -4), (1.8, -16)]):
        B.lock(f"bang{i}", "bangs", (x, 30.6, -2.8), 1.4, 1.4, 0.4, (10, 0, rz), C.BODY, C.BODY_HI)
    c("ahs0", "ah0", (-0.1, 31.2, -0.1), (0.5, 34.2, 0.5), C.BODY, faces=bd)
    c("ahs1", "ah1", (-0.05, 34.0, -0.05), (0.45, 36.6, 0.45), C.BODY, faces=bd)
    c("ahs2", "ah2", (0.0, 36.4, 0.0), (0.4, 38.4, 0.4), C.BODY)

    # horns: long thin black arcs from the upper back, curving up-out-down
    for s, k in ((1, "r"), (-1, "l")):
        for i in range(6):
            w = 0.55 - i * 0.06
            y = 23.2 + i * 3.4
            c(f"hornc_{k}{i}", f"horn_{k}{i}", (0.7 * s - w, y, 1.2 - w), (0.7 * s + w, y + 3.5, 1.2 + w), C.BODY, faces=bd)
        blade(f"horntip_{k}", f"horn_{k}5", (0.7 * s, 23.2 + 6 * 3.4 - 0.1, 1.2), 2.0, 0.45, 0.45, (0, 0, 0), C.BODY, C.BODY_HI)

    # wings: pale teardrop membranes (cutout) with black rims/veins
    wp = wing_paint(C, R)
    for k in W_REST:
        upper = k[5] == "u"
        L, Wd = (14.0, 6.0) if upper else (9.5, 4.2)
        x0 = 0.5 if k.endswith("r") else -0.5
        y0 = 22.0 if upper else 20.6
        c("wingm_" + k, k, (x0 - Wd / 2, y0, 1.05), (x0 + Wd / 2, y0 + L, 1.15), C.WING, faces={"north": wp, "south": wp, "east": solid(C.WING_V), "west": solid(C.WING_V), "up": solid(C.WING_V), "down": solid(C.WING_V)})
        c("wingr_" + k, k, (x0 - 0.2, y0, 0.95), (x0 + 0.2, y0 + L * 0.85, 1.25), C.WING_V)

    # back tentacles (props)
    for t in range(4):
        tx, ty = (1, -1, 0.8, -0.8)[t], (20.5, 20.5, 18.0, 18.0)[t]
        for i in range(4):
            w = 0.6 - i * 0.11
            z0 = 1.0 + i * 3
            c(f"tentc{t}_{i}", f"tent{t}_{i}", (tx - w, ty - w, z0), (tx + w, ty + w, z0 + 3.1), C.BODY, faces=bd)
        blade(f"tent{t}_tip", f"tent{t}_3", (tx, ty, 1.0 + 12 - 0.2), 1.8, 0.5, 0.4, (90, 0, 0), C.BODY, C.BODY_HI)

    # arms: very long, forearms thicken into huge blocky claws
    for s, k in ((1, "r"), (-1, "l")):
        x = 2.4 * s
        bk = big[k]
        c("upper_" + k, "arm_" + k, (x - 0.55, 14.4, -0.55), (x + 0.55, 23.2, 0.55), C.BODY, faces=bd)
        c("delt_" + k, "arm_" + k, (x - 0.8, 21.2, -0.8), (x + 0.8, 23.4, 0.8), C.BODY, faces=bd)
        for i in range(3):
            blade(f"armspk_{k}{i}", "arm_" + k, (x + 0.5 * s, 16.0 + i * 2.2, 0.2), 1.3, 0.3, 0.3, (10, 0, -s * 60), C.BODY, C.BODY_HI)
        c("foreA_" + k, "fore_" + k, (x - 0.6, 10.4, -0.6), (x + 0.6, 14.8, 0.6), C.BODY, faces=bd)
        c("foreB_" + k, "fore_" + k, (x - 0.9 * bk, 6.2, -0.85 * bk), (x + 0.9 * bk, 10.8, 0.85 * bk), C.BODY, faces=bd)
        for i in range(2):
            blade(f"forespk_{k}{i}", "fore_" + k, (x + 0.8 * s * bk, 7.5 + i * 2.0, 0.3), 1.6, 0.35, 0.3, (20, 0, -s * 75), C.BODY, C.BODY_HI)
        c("palm_" + k, "hand_" + k, (x - 1.5 * bk, 3.2, -1.2 * bk), (x + 1.5 * bk, 6.6, 1.2 * bk), C.BODY, faces=bd)
        c("knuck_" + k, "hand_" + k, (x - 1.6 * bk, 3.0, -1.35 * bk), (x + 1.6 * bk, 3.8, 0.4), C.BODY_HI)
        for i in range(4):
            fx = x + (i - 1.5) * 0.7 * bk
            fz = -0.4 + abs(i - 1.5) * 0.2
            c(f"fseg_{k}{i}", f"fing_{k}{i}", (fx - 0.32, 1.6, fz - 0.32), (fx + 0.32, 3.5, fz + 0.32), C.BODY, faces=bd)
            B.lock(f"talon_{k}{i}", f"fing_{k}{i}", (fx, 1.8, fz), 3.8 * bk, 0.6, 0.5, (-22, 0, (i - 1.5) * 5), C.CLAW, C.CLAW_HI, paint=B.edges(C.CLAW_HI))
        B.lock("thumbc_" + k, "thumb_" + k, (x - 1.1 * s, 4.6, -0.8), 3.0 * bk, 0.55, 0.45, (-30, 0, -s * 30), C.CLAW, C.CLAW_HI, paint=B.edges(C.CLAW_HI))

    # legs: spindly, knees bent out, clawed feet
    for s, k in ((1, "r"), (-1, "l")):
        x = 1.0 * s
        c("thigh_" + k, "leg_" + k, (x - 0.55, 7.2, -0.55), (x + 0.55, 14.2, 0.55), C.BODY, faces=bd)
        c("knee_" + k, "shin_" + k, (x - 0.6, 6.8, -0.7), (x + 0.6, 7.8, 0.5), C.BODY_HI)
        c("shin_" + k, "shin_" + k, (x - 0.45, 1.2, -0.45), (x + 0.45, 7.6, 0.45), C.BODY, faces=bd)
        c("foot_" + k, "foot_" + k, (x - 0.7, 0, -1.4), (x + 0.7, 1.3, 0.7), C.BODY, faces=bd)
        for i in range(3):
            blade(f"toe_{k}{i}", "foot_" + k, (x + (i - 1) * 0.45, 0.3, -1.3), 1.8, 0.4, 0.35, (-95, (i - 1) * 25, 0), C.CLAW, C.CLAW_HI)


class DB(A):
    """boss animation: hair = tufts + horns + ahoge, cloth = wing flutter"""

    def hair(self, keys, delay=2):
        self.drape("hair_b", [(t, -x * 0.6, 0, z * 0.5) for (t, x, y, z) in keys], delay)
        self.drape("hair_r", [(t, x * 0.3, 0, z * 0.5) for (t, x, y, z) in keys], delay)
        self.drape("hair_l", [(t, x * 0.3, 0, z * 0.5) for (t, x, y, z) in keys], delay)
        self.drape("ah0", [(t, -x * 0.5, 0, z * 0.5) for (t, x, y, z) in keys], delay + 1)
        self.drape("ah1", [(t, -x * 0.6, 0, z * 0.4) for (t, x, y, z) in keys], delay + 3)
        self.drape("ah2", [(t, -x * 0.8, 0, z * 0.4) for (t, x, y, z) in keys], delay + 5)
        for s, k in ((1, "r"), (-1, "l")):
            for i in range(1, 6):
                self.drape(f"horn_{k}{i}", [(t, -x * 0.25, 0, z * 0.25 + s * abs(x) * 0.15) for (t, x, y, z) in keys], delay + i)
        return self

    def cloth(self, keys, delay=2):
        """(t, flap, _, _) flap>0 = wings raise/open"""
        for k, (rx, ry, rz) in W_REST.items():
            s = 1 if k.endswith("r") else -1
            self.drape(k, [(t, 0, 0, -s * x) for (t, x, y, z) in keys], delay if k[5] == "u" else delay + 1)
        return self

    def wings(self, t, open_=0, fold=0, fwd=0):
        """explicit wing pose: open_ = spread (deg), fold = fold back (deg), fwd = sweep forward (deg)"""
        for k in W_REST:
            s = 1 if k.endswith("r") else -1
            self.rot(k, (t, -fold + fwd * 0.3, s * (fold - fwd), -s * open_))
        return self

    def claws(self, t, curl=0, spread=0):
        for k in ("r", "l"):
            for i in range(4):
                self.rot(f"fing_{k}{i}", (t, curl, 0, (i - 1.5) * spread))
            self.rot("thumb_" + k, (t, curl * 0.6, 0, 0))
        return self

    def tents(self, keys, lag=1.0):
        """keys: (t, base_rx, curl, reach_scale or None)"""
        for tt in range(4):
            j = (1, -1, 1, -1)[tt]
            ks0 = []
            for (t, rx, cu, sc) in keys:
                ks0.append((t, rx, j * 20, 0))
            self.rot(f"tent{tt}_0", *ks0)
            for i in range(1, 4):
                self.rot(f"tent{tt}_{i}", *[(min(self.ticks, t + i * lag), cu, j * cu * 0.3, 0) for (t, rx, cu, sc) in keys])
        return self


PROPS2 = ("tents",)


def anims_p2(B):
    def mk(name, ticks, loop=False):
        return DB(B, name, ticks, {}, PROPS2, loop)

    def show_tents(a, t0, t1):
        a.show("tents", t0, t1, grow=3)

    # ---------------- idle (60): hunched predator sway, grin twitch, wings quiver, claws flex
    a = mk("idle", 60, loop=True)
    for t, j in ((0, 0), (15, 1), (30, 0), (45, -1), (60, 0)):
        a.at(t, chest=(2 * abs(j), 3 * j, 2 * j), head=(-3 * abs(j), -6 * j, 4 * j), P_body=(0, -0.15 * abs(j), 0),
             arm_r=(3 * abs(j), 0, 2 * j), arm_l=(3 * abs(j), 0, 2 * j), fore_r=(4 * abs(j), 0, 0), fore_l=(4 * abs(j), 0, 0))
        a.claws(t, curl=10 * abs(j), spread=2)
    a.wings(0).wings(30, open_=4).wings(60)
    a.scl("tents", (0, *HIDE))
    a.hair([(0, 0, 0, 1), (15, 2, 0, -1), (30, 0, 0, 1), (45, 2, 0, -1), (60, 0, 0, 1)], delay=4)
    a.done(base_layer=True)

    # ---------------- walk (24): loping stalk, knuckles nearly dragging, wings bob
    a = mk("walk", 24, loop=True)
    a.rot("leg_r", (0, 26, 0, 0), (12, -24, 0, 0), (24, 26, 0, 0))
    a.rot("shin_r", (0, -6, 0, 0), (12, -10, 0, 0), (16, -50, 0, 0), (20, -24, 0, 0), (24, -6, 0, 0))
    a.rot("leg_l", (0, -24, 0, 0), (12, 26, 0, 0), (24, -24, 0, 0))
    a.rot("shin_l", (0, -10, 0, 0), (4, -50, 0, 0), (8, -24, 0, 0), (12, -6, 0, 0), (24, -10, 0, 0))
    a.pos("body", (0, 0, -0.5, 0), (6, 0, 0.3, 0), (12, 0, -0.5, 0), (18, 0, 0.3, 0), (24, 0, -0.5, 0))
    a.rot("body", (0, 0, 8, 0), (12, 0, -8, 0), (24, 0, 8, 0))
    a.rot("chest", (0, 6, -10, 3), (12, 6, 10, -3), (24, 6, -10, 3))
    a.rot("head", (0, -6, 8, 0), (12, -6, -8, 0), (24, -6, 8, 0))
    a.rot("arm_r", (0, -24, 0, 0), (12, 24, 0, 0), (24, -24, 0, 0))
    a.rot("arm_l", (0, 24, 0, 0), (12, -24, 0, 0), (24, 24, 0, 0))
    a.rot("fore_r", (0, 0, 0, 0), (12, 16, 0, 0), (24, 0, 0, 0))
    a.rot("fore_l", (0, 16, 0, 0), (12, 0, 0, 0), (24, 16, 0, 0))
    a.hair([(0, -4, 0, 2), (6, -6, 0, 0), (12, -4, 0, -2), (18, -6, 0, 0), (24, -4, 0, 2)], delay=2)
    a.cloth([(0, 4, 0, 0), (6, -2, 0, 0), (12, 4, 0, 0), (18, -2, 0, 0), (24, 4, 0, 0)], delay=1)
    a.done(base_layer=True)

    # ---------------- claw_rake (40): R wind 4-9, RAKE 12; L wind 15, RAKE 19; both claws up 24, CRASH 28; recover
    a = mk("claw_rake", 40)
    a.at(0, chest=(0, 0, 0), P_body=(0, 0, 0))
    a.at(8, chest=(4, 36, 0), head=(4, -24, 0), arm_r=(60, 0, 70), fore_r=(-30, 0, 0), arm_l=(10, 0, -10), P_body=(0, -0.6, 0.4))
    a.at(12, chest=(-14, -30, 0), head=(6, 22, 0), arm_r=(80, 40, -30), fore_r=(0, 0, 0), arm_l=(-20, 0, -30), P_body=(0, -1.0, -0.8))
    a.at(15, chest=(4, -34, 0), head=(4, 22, 0), arm_l=(60, 0, -70), fore_l=(-30, 0, 0), arm_r=(20, 0, 20), P_body=(0, -0.7, 0.2))
    a.at(19, chest=(-14, 30, 0), head=(6, -22, 0), arm_l=(80, -40, 30), fore_l=(0, 0, 0), arm_r=(-10, 0, 30), P_body=(0, -1.0, -0.8))
    a.at(24, chest=(16, 0, 0), head=(-10, 0, 0), arm_r=(170, 0, 20), arm_l=(170, 0, -20), fore_r=(-20, 0, 0), fore_l=(-20, 0, 0), P_body=(0, 0.4, 0.4))
    a.at(28, chest=(-34, 0, 0), head=(20, 0, 0), arm_r=(70, 0, 0), arm_l=(70, 0, 0), fore_r=(-10, 0, 0), fore_l=(-10, 0, 0), P_body=(0, -1.6, -1.2))
    a.at(32, chest=(-30, 0, 0), P_body=(0, -1.5, -1.1))
    a.at(40, chest=(0, 0, 0), head=(0, 0, 0), arm_r=(0, 0, 0), arm_l=(0, 0, 0), P_body=(0, 0, 0))
    a.claws(0).claws(8, curl=-30, spread=6).claws(12, curl=30).claws(15, curl=-30, spread=6).claws(19, curl=30).claws(24, curl=-40, spread=8).claws(28, curl=20).claws(40)
    a.wings(0).wings(12, open_=10).wings(24, open_=26, fold=-10).wings(28, open_=-10).wings(40)
    a.legs([(0, 0, 0, 0), (8, -10, 0, 4), (12, 10, 0, 4), (24, 0, 0, 0), (28, 30, 0, 6), (40, 0, 0, 0)], [(0, 0, 0, 0), (8, -10, 0, 0), (28, -40, 0, 0), (40, 0, 0, 0)])
    a.hair([(0, 0, 0, 0), (8, 4, 0, -8), (12, -8, 0, 10), (15, 4, 0, 8), (19, -8, 0, -10), (24, 10, 0, 0), (28, -14, 0, 0), (40, 0, 0, 0)])
    a.done()

    # ---------------- claw_slam (46): rise tall, claws high 4-16, SLAM 22 (whole body crashes forward), hold 22-30, recover
    a = mk("claw_slam", 46)
    a.at(0, chest=(0, 0, 0), P_body=(0, 0, 0))
    a.at(10, chest=(24, 0, 0), head=(-14, 0, 0), arm_r=(180, 0, 30), arm_l=(180, 0, -30), fore_r=(-20, 0, 0), fore_l=(-20, 0, 0), P_body=(0, 1.6, 0.6))
    a.at(16, chest=(30, 0, 0), head=(-20, 0, 0), arm_r=(200, -20, 10), arm_l=(200, 20, -10), fore_r=(-10, 0, 0), fore_l=(-10, 0, 0), P_body=(0, 2.0, 0.8))
    a.at(22, chest=(-46, 0, 0), head=(30, 0, 0), arm_r=(70, -20, 0), arm_l=(70, 20, 0), fore_r=(0, 0, 0), fore_l=(0, 0, 0), P_body=(0, -3.0, -1.6))
    a.at(30, chest=(-42, 0, 0), head=(26, 0, 0), P_body=(0, -2.8, -1.5))
    a.at(46, chest=(0, 0, 0), head=(0, 0, 0), arm_r=(0, 0, 0), arm_l=(0, 0, 0), fore_r=(0, 0, 0), fore_l=(0, 0, 0), P_body=(0, 0, 0))
    a.claws(0).claws(16, curl=-40, spread=10).claws(22, curl=30).claws(30, curl=30).claws(46)
    a.wings(0).wings(16, open_=40, fold=-20).wings(22, open_=-20, fwd=20).wings(32, open_=-10).wings(46)
    a.legs([(0, 0, 0, 0), (16, -16, 0, 0), (22, 40, 0, 6), (30, 40, 0, 6), (46, 0, 0, 0)], [(0, 0, 0, 0), (16, 10, 0, 0), (22, -60, 0, 0), (30, -60, 0, 0), (46, 0, 0, 0)])
    a.hair([(0, 0, 0, 0), (16, -14, 0, 0), (22, 24, 0, 0), (28, 6, 0, 0), (36, -4, 0, 0), (46, 0, 0, 0)])
    a.cloth([(0, 0, 0, 0), (16, 20, 0, 0), (22, -16, 0, 0), (32, 4, 0, 0), (46, 0, 0, 0)])
    a.done()

    # ---------------- eruption (50): both claws raised 4-12, PLUNGE into the floor 16, crouched + claws churning 18-36, rip out 40
    a = mk("eruption", 50)
    a.at(0, chest=(0, 0, 0), P_body=(0, 0, 0))
    a.at(12, chest=(16, 0, 0), head=(-10, 0, 0), arm_r=(150, 0, 30), arm_l=(150, 0, -30), fore_r=(-30, 0, 0), fore_l=(-30, 0, 0), P_body=(0, 1.0, 0.4))
    a.at(16, chest=(-50, 0, 0), head=(36, 0, 0), arm_r=(40, 0, 10), arm_l=(40, 0, -10), fore_r=(10, 0, 0), fore_l=(10, 0, 0), P_body=(0, -4.0, -1.0))
    for t in range(20, 38, 4):
        j = 1 if (t // 4) % 2 else -1
        a.at(t, chest=(-48, 4 * j, 2 * j), head=(34, -4 * j, 0), arm_r=(40 + 4 * j, 0, 10), arm_l=(40 - 4 * j, 0, -10), P_body=(0, -3.8, -1.0))
    a.at(40, chest=(10, 0, 0), head=(-6, 0, 0), arm_r=(100, 0, 40), arm_l=(100, 0, -40), fore_r=(-20, 0, 0), fore_l=(-20, 0, 0), P_body=(0, 0.4, 0.4))
    a.at(50, chest=(0, 0, 0), head=(0, 0, 0), arm_r=(0, 0, 0), arm_l=(0, 0, 0), fore_r=(0, 0, 0), fore_l=(0, 0, 0), P_body=(0, 0, 0))
    a.claws(0).claws(12, curl=-30, spread=8).claws(16, curl=40).claws(36, curl=40).claws(40, curl=-30, spread=8).claws(50)
    a.wings(0).wings(12, open_=30).wings(16, open_=-10, fwd=10).wings(36, open_=-6).wings(40, open_=24).wings(50)
    a.legs([(0, 0, 0, 0), (12, -10, 0, 0), (16, 50, 0, 8), (36, 50, 0, 8), (40, 0, 0, 0), (50, 0, 0, 0)], [(0, 0, 0, 0), (16, -70, 0, 0), (36, -70, 0, 0), (40, -10, 0, 0), (50, 0, 0, 0)])
    a.hair([(0, 0, 0, 0), (12, -10, 0, 0), (16, 24, 0, 0), (24, 10, 0, 6), (32, 10, 0, -6), (40, -10, 0, 0), (50, 0, 0, 0)])
    a.done()

    # ---------------- tentacle_grasp (46): tentacles writhe out 2-10, right claw raised 10, STAB into the ground 16, hold (tentacles burst far away), pull 36
    a = mk("tentacle_grasp", 46)
    show_tents(a, 2, 42)
    a.at(0, chest=(0, 0, 0), P_body=(0, 0, 0))
    a.at(10, chest=(14, -20, 0), head=(-6, 10, 0), arm_r=(160, 0, 20), fore_r=(-20, 0, 0), arm_l=(20, 0, -40), P_body=(0, 0.6, 0.4))
    a.at(16, chest=(-40, 10, 0), head=(30, -6, 0), arm_r=(50, 0, 0), fore_r=(0, 0, 0), arm_l=(30, 0, -50), P_body=(0, -3.0, -0.8))
    a.at(30, chest=(-36, 6, 0), head=(26, -4, 0), P_body=(0, -2.8, -0.7))
    a.at(36, chest=(10, 0, 0), head=(-4, 0, 0), arm_r=(80, 0, 20), fore_r=(-10, 0, 0), P_body=(0, 0.2, 0.3))
    a.at(46, chest=(0, 0, 0), head=(0, 0, 0), arm_r=(0, 0, 0), fore_r=(0, 0, 0), arm_l=(0, 0, 0), P_body=(0, 0, 0))
    a.tents([(0, 0, 0, None), (4, -60, 30, None), (10, -30, -30, None), (16, 50, 40, None), (24, 40, -30, None), (32, 50, 30, None), (40, 0, 0, None), (46, 0, 0, None)], lag=1.5)
    a.claws(0).claws(10, curl=-40, spread=10).claws(16, curl=30).claws(30, curl=30).claws(46)
    a.wings(0).wings(10, open_=30).wings(16, open_=-6).wings(46)
    a.legs([(0, 0, 0, 0), (10, -6, 0, 0), (16, 40, 0, 6), (30, 40, 0, 6), (46, 0, 0, 0)], [(0, 0, 0, 0), (16, -50, 0, 0), (30, -50, 0, 0), (46, 0, 0, 0)])
    a.hair([(0, 0, 0, 0), (10, -8, 0, 0), (16, 20, 0, 0), (26, 8, 0, 0), (46, 0, 0, 0)])
    a.done()

    # ---------------- wing_gust (44): wings rise 6-14, BEAT 16 (body pitches forward), rise 23, BEAT 27, glide down
    a = mk("wing_gust", 44)
    a.at(0, chest=(0, 0, 0), P_body=(0, 0, 0))
    a.at(12, chest=(16, 0, 0), head=(-10, 0, 0), arm_r=(-20, 0, 50), arm_l=(-20, 0, -50), P_body=(0, 1.0, 0.4))
    a.at(16, chest=(-20, 0, 0), head=(14, 0, 0), arm_r=(30, 0, 30), arm_l=(30, 0, -30), P_body=(0, -0.8, -0.4))
    a.at(23, chest=(14, 0, 0), head=(-8, 0, 0), arm_r=(-20, 0, 50), arm_l=(-20, 0, -50), P_body=(0, 0.9, 0.3))
    a.at(27, chest=(-22, 0, 0), head=(16, 0, 0), arm_r=(30, 0, 30), arm_l=(30, 0, -30), P_body=(0, -0.9, -0.5))
    a.at(36, chest=(-4, 0, 0), head=(2, 0, 0), arm_r=(4, 0, 6), arm_l=(4, 0, -6), P_body=(0, -0.2, 0))
    a.wings(0).wings(8, open_=50, fold=-20).wings(14, open_=70, fold=-30).wings(16, open_=-30, fwd=50).wings(19, open_=-20, fwd=30)
    a.wings(23, open_=70, fold=-30).wings(27, open_=-30, fwd=50).wings(31, open_=-20, fwd=30).wings(40, open_=6).wings(44)
    a.legs([(0, 0, 0, 0), (12, -10, 0, 4), (16, 20, 0, 6), (23, -10, 0, 4), (27, 20, 0, 6), (44, 0, 0, 0)], [(0, 0, 0, 0), (16, -30, 0, 0), (23, 0, 0, 0), (27, -30, 0, 0), (44, 0, 0, 0)])
    a.hair([(0, 0, 0, 0), (12, -10, 0, 0), (16, -26, 0, 0), (23, -12, 0, 0), (27, -28, 0, 0), (36, -6, 0, 0), (44, 0, 0, 0)])
    a.done()

    # ---------------- grin_volley (48): rears back, jaw unhinges 4-12, SPIT 14,17,...,32 (head jerks), jaw shuts 38
    a = mk("grin_volley", 48)
    a.at(0, chest=(0, 0, 0), head=(0, 0, 0), P_body=(0, 0, 0))
    a.at(10, chest=(20, 0, 0), head=(-26, 0, 0), arm_r=(-10, 0, 40), arm_l=(-10, 0, -40), P_body=(0, 0.6, 0.6))
    a.pos("jaw", (0, 0, 0, 0), (8, 0, 0, 0), (12, 0, -1.4, 0), (34, 0, -1.4, 0), (38, 0, 0, 0))
    a.scl("jaw", (0, 1, 1, 1), (8, 1, 1, 1), (12, 1.2, 2.6, 1), (34, 1.2, 2.6, 1), (38, 1, 1, 1))
    for i, t in enumerate(range(14, 33, 3)):
        j = 1 if i % 2 else -1
        a.at(t, chest=(-6, 6 * j, 0), head=(14, -6 * j, 0), P_body=(0, -0.4, -0.3))
        a.at(t + 1.5, chest=(4, 4 * j, 0), head=(-4, -4 * j, 0), P_body=(0, 0, 0))
    a.at(40, chest=(0, 0, 0), head=(0, 0, 0), arm_r=(0, 0, 0), arm_l=(0, 0, 0), P_body=(0, 0, 0))
    a.claws(0).claws(10, curl=-20, spread=8).claws(36, curl=-20, spread=8).claws(48)
    a.wings(0).wings(10, open_=30).wings(34, open_=20).wings(48)
    a.legs([(0, 0, 0, 0), (10, -8, 0, 4), (34, -8, 0, 4), (48, 0, 0, 0)], [(0, 0, 0, 0), (10, -16, 0, 0), (34, -16, 0, 0), (48, 0, 0, 0)])
    a.hair([(0, 0, 0, 0), (10, -16, 0, 0), (14, 8, 0, 0), (20, 6, 0, 4), (26, 6, 0, -4), (32, 6, 0, 0), (40, 0, 0, 0), (48, 0, 0, 0)])
    a.done()

    # ---------------- pounce (50): drop to all fours 4-12, LEAP 14 (stretched, claws forward), airborne 16-22, LAND 24 crouch, rise 40
    a = mk("pounce", 50)
    a.at(0, chest=(0, 0, 0), P_body=(0, 0, 0))
    a.at(12, chest=(-60, 0, 0), head=(44, 0, 0), arm_r=(70, 0, 20), arm_l=(70, 0, -20), fore_r=(10, 0, 0), fore_l=(10, 0, 0), P_body=(0, -4.6, 0))
    a.at(14, chest=(-40, 0, 0), head=(30, 0, 0), arm_r=(150, 0, 20), arm_l=(150, 0, -20), fore_r=(-10, 0, 0), fore_l=(-10, 0, 0), P_body=(0, 0.6, -1.0))
    a.at(19, chest=(-30, 0, 0), head=(24, 0, 0), arm_r=(130, 0, 30), arm_l=(130, 0, -30), P_body=(0, 1.0, -0.6))
    a.at(24, chest=(-56, 0, 0), head=(40, 0, 0), arm_r=(60, 0, 20), arm_l=(60, 0, -20), fore_r=(10, 0, 0), fore_l=(10, 0, 0), P_body=(0, -4.2, -0.6))
    a.at(32, chest=(-50, 0, 0), head=(36, 0, 0), P_body=(0, -3.8, -0.5))
    a.at(42, chest=(0, 0, 0), head=(0, 0, 0), arm_r=(0, 0, 0), arm_l=(0, 0, 0), fore_r=(0, 0, 0), fore_l=(0, 0, 0), P_body=(0, 0, 0))
    a.claws(0).claws(12, curl=20).claws(14, curl=-40, spread=10).claws(22, curl=-40, spread=10).claws(24, curl=40).claws(34, curl=30).claws(50)
    a.wings(0).wings(12, open_=-10).wings(14, open_=60, fold=-20).wings(19, open_=40, fold=-10).wings(24, open_=-20, fwd=20).wings(36, open_=0).wings(50)
    a.legs([(0, 0, 0, 0), (12, 60, 0, 10), (14, -40, 0, 0), (19, -20, 0, 0), (24, 60, 0, 10), (32, 60, 0, 10), (42, 0, 0, 0), (50, 0, 0, 0)],
           [(0, 0, 0, 0), (12, -90, 0, 0), (14, 0, 0, 0), (19, -40, 0, 0), (24, -90, 0, 0), (32, -90, 0, 0), (42, 0, 0, 0), (50, 0, 0, 0)])
    a.hair([(0, 0, 0, 0), (12, 10, 0, 0), (14, -30, 0, 0), (19, -24, 0, 0), (24, 30, 0, 0), (30, 10, 0, 0), (42, 0, 0, 0), (50, 0, 0, 0)], delay=1)
    a.done()

    # ---------------- grab_crush (56): reach 8, SNATCH 14 (right claw forward), lift 14-22, SQUEEZE 24, 34, SMASH down 44, recover
    a = mk("grab_crush", 56)
    a.at(0, chest=(0, 0, 0), P_body=(0, 0, 0))
    a.at(8, chest=(10, -30, 0), head=(-4, 20, 0), arm_r=(40, 0, 60), fore_r=(-20, 0, 0), arm_l=(20, 0, -20), P_body=(0, -0.4, 0.4))
    a.at(14, chest=(-24, 20, 0), head=(14, -10, 0), arm_r=(90, 0, 0), fore_r=(0, 0, 0), arm_l=(-10, 0, -30), P_body=(0, -1.2, -1.2))
    a.at(22, chest=(10, 10, 0), head=(-14, -6, 0), arm_r=(150, 0, 0), fore_r=(-30, 0, 0), arm_l=(10, 0, -30), P_body=(0, 0.6, 0.2))
    for t in (24, 34):
        a.at(t, chest=(14, 6, 0), head=(-18, -4, 4), arm_r=(150, 0, -6), P_body=(0, 0.6, 0.2))
        a.at(t + 4, chest=(8, 10, 0), head=(-12, -6, -4), arm_r=(148, 0, 4), P_body=(0, 0.6, 0.2))
    a.at(40, chest=(20, 0, 0), head=(-16, 0, 0), arm_r=(190, 0, 0), fore_r=(-20, 0, 0), P_body=(0, 1.2, 0.6))
    a.at(44, chest=(-44, 10, 0), head=(26, -6, 0), arm_r=(60, 0, 0), fore_r=(0, 0, 0), arm_l=(20, 0, -40), P_body=(0, -3.0, -1.4))
    a.at(50, chest=(-38, 6, 0), head=(22, -4, 0), P_body=(0, -2.6, -1.2))
    a.at(56, chest=(0, 0, 0), head=(0, 0, 0), arm_r=(0, 0, 0), fore_r=(0, 0, 0), arm_l=(0, 0, 0), P_body=(0, 0, 0))
    for k in ("r",):
        for i in range(4):
            a.rot(f"fing_{k}{i}", (0, 0, 0, 0), (10, -40, 0, (i - 1.5) * 12), (14, 50, 0, 0), (24, 70, 0, 0), (28, 50, 0, 0), (34, 75, 0, 0), (38, 50, 0, 0), (44, -30, 0, (i - 1.5) * 12), (56, 0, 0, 0))
        a.rot("thumb_r", (0, 0, 0, 0), (10, -30, 0, 0), (14, 40, 0, 20), (34, 50, 0, 24), (44, -20, 0, 0), (56, 0, 0, 0))
    a.wings(0).wings(14, open_=20).wings(24, open_=30, fold=-10).wings(34, open_=30, fold=-10).wings(44, open_=-20, fwd=20).wings(56)
    a.legs([(0, 0, 0, 0), (8, -10, 0, 4), (14, 20, 0, 4), (22, 0, 0, 0), (44, 40, 0, 6), (50, 40, 0, 6), (56, 0, 0, 0)], [(0, 0, 0, 0), (14, -30, 0, 0), (22, 0, 0, 0), (44, -60, 0, 0), (50, -60, 0, 0), (56, 0, 0, 0)])
    a.hair([(0, 0, 0, 0), (8, 6, 0, 6), (14, -10, 0, -6), (24, -4, 0, 4), (34, -4, 0, -4), (40, -10, 0, 0), (44, 20, 0, 0), (56, 0, 0, 0)])
    a.done()

    # ---------------- spin_rend (40): coil 0-9, SPIN two turns 10-26 (hits 15, 22), claws wide, wobble, recover
    a = mk("spin_rend", 40)
    a.at(0, root=(0, 0, 0), chest=(0, 0, 0), P_root=(0, 0, 0))
    a.at(9, root=(0, -50, 0), chest=(-20, 30, 0), head=(16, -16, 0), arm_r=(30, 0, 60), arm_l=(30, 0, -60), P_root=(0, -1.6, 0))
    a.at(12, root=(0, 0, 0), chest=(-10, 0, 0), head=(4, 0, 0), arm_r=(10, 0, 90), arm_l=(10, 0, -90), fore_r=(0, 0, 0), fore_l=(0, 0, 0), P_root=(0, 0.2, 0))
    a.at(15, root=(0, 200, 0)).at(19, root=(0, 400, 0)).at(22, root=(0, 560, 0))
    a.at(26, root=(0, 720, 0), chest=(-14, -10, 0), head=(10, 8, 0), arm_r=(30, 0, 40), arm_l=(30, 0, -40), P_root=(0, -0.8, 0))
    a.at(31, root=(0, 726, 0), chest=(-4, 4, 0), P_root=(0, 0, 0))
    a.at(40, root=(0, 720, 0), chest=(0, 0, 0), head=(0, 0, 0), arm_r=(0, 0, 0), arm_l=(0, 0, 0))
    a.claws(0).claws(9, curl=20).claws(12, curl=-40, spread=12).claws(26, curl=-40, spread=12).claws(31, curl=10).claws(40)
    a.wings(0).wings(9, open_=-10).wings(12, open_=60, fold=-20).wings(26, open_=60, fold=-20).wings(31, open_=10).wings(40)
    a.legs([(0, 0, 0, 0), (9, -20, 0, 8), (12, 0, 0, 14), (26, 0, 0, 14), (31, -10, 0, 4), (40, 0, 0, 0)], [(0, 0, 0, 0), (9, -40, 0, 0), (12, -10, 0, 0), (26, -20, 0, 0), (40, 0, 0, 0)])
    a.hair([(0, 0, 0, 0), (9, 6, 0, 10), (13, -4, 0, -26), (26, -4, 0, -26), (31, 4, 0, 10), (40, 0, 0, 0)])
    a.done()

    # ---------------- welcome_home (72, enraged): rise 0-10, ROAR 12, claws into the floor 24 (tentacle cage), three pounds 32/38/44,
    #                  rear up 48, wings + tentacles spray lances 50-60, recover
    a = mk("welcome_home", 72)
    show_tents(a, 20, 66)
    a.at(0, chest=(0, 0, 0), head=(0, 0, 0), P_body=(0, 0, 0))
    a.at(8, chest=(20, 0, 0), head=(-10, 0, 0), arm_r=(40, 0, 40), arm_l=(40, 0, -40), fore_r=(40, 0, 0), fore_l=(40, 0, 0), P_body=(0, 1.2, 0.4))
    a.at(12, chest=(-26, 0, 0), head=(-36, 0, 0), arm_r=(20, 0, 100), arm_l=(20, 0, -100), fore_r=(-10, 0, 0), fore_l=(-10, 0, 0), P_body=(0, -0.6, -0.6))
    for t in (14, 16, 18):
        j = 1 if t % 4 == 0 else -1
        a.at(t, head=(-34, 4 * j, -4 * j), chest=(-24, 2 * j, 2 * j))
    a.pos("jaw", (0, 0, 0, 0), (10, 0, 0, 0), (12, 0, -1.6, 0), (20, 0, -1.6, 0), (24, 0, 0, 0), (48, 0, 0, 0), (50, 0, -1.2, 0), (60, 0, -1.2, 0), (64, 0, 0, 0))
    a.scl("jaw", (0, 1, 1, 1), (10, 1, 1, 1), (12, 1.3, 3.0, 1), (20, 1.3, 3.0, 1), (24, 1, 1, 1), (48, 1, 1, 1), (50, 1.2, 2.4, 1), (60, 1.2, 2.4, 1), (64, 1, 1, 1))
    a.at(21, chest=(14, 0, 0), head=(-6, 0, 0), arm_r=(170, 0, 20), arm_l=(170, 0, -20), fore_r=(-20, 0, 0), fore_l=(-20, 0, 0), P_body=(0, 1.0, 0.4))
    a.at(24, chest=(-52, 0, 0), head=(36, 0, 0), arm_r=(40, 0, 10), arm_l=(40, 0, -10), fore_r=(10, 0, 0), fore_l=(10, 0, 0), P_body=(0, -4.0, -1.0))
    for k, t in enumerate((32, 38, 44)):
        s = 1 if k % 2 == 0 else -1
        a.at(t - 3, chest=(-14, 0, 0), head=(20, 0, 0), arm_r=(150 if s > 0 else 50, 0, 24), arm_l=(150 if s < 0 else 50, 0, -24), P_body=(0, -1.4, -0.3))
        a.at(t, chest=(-50, 10 * s, 0), head=(36, 0, 0), arm_r=(40, 0, 14), arm_l=(40, 0, -14), P_body=(0, -4.0, -1.0))
    a.at(48, chest=(24, 0, 0), head=(-10, 0, 0), arm_r=(30, 0, 70), arm_l=(30, 0, -70), fore_r=(20, 0, 0), fore_l=(20, 0, 0), P_body=(0, 1.4, 0.6))
    for t in range(50, 61, 2):
        j = 1 if (t // 2) % 2 else -1
        a.at(t, chest=(18 - 4 * j, 4 * j, 0), head=(-6, -4 * j, 0), P_body=(0, 1.2, 0.5))
    a.at(66, chest=(4, 0, 0), head=(0, 0, 0), arm_r=(10, 0, 10), arm_l=(10, 0, -10), fore_r=(0, 0, 0), fore_l=(0, 0, 0), P_body=(0, 0, 0))
    a.claws(0).claws(12, curl=-40, spread=12).claws(21, curl=-40, spread=10).claws(24, curl=40).claws(44, curl=40).claws(48, curl=-30, spread=10).claws(66)
    a.wings(0).wings(8, open_=-10).wings(12, open_=80, fold=-30).wings(20, open_=70, fold=-30).wings(24, open_=-20, fwd=20).wings(44, open_=-10)
    for t in range(48, 61, 2):
        a.wings(t, open_=70 if t % 4 == 0 else 50, fold=-20, fwd=(30 if t % 4 else 10))
    a.wings(66, open_=10).wings(72)
    a.tents([(0, 0, 0, None), (20, -70, 40, None), (24, 120, -20, None), (44, 120, -20, None), (48, -60, 20, None), (50, -10, 0, None), (52, -40, 10, None),
             (54, -10, 0, None), (56, -40, 10, None), (58, -10, 0, None), (60, -30, 10, None), (66, 0, 0, None)], lag=1)
    a.legs([(0, 0, 0, 0), (8, -10, 0, 0), (12, 20, 0, 10), (21, -10, 0, 0), (24, 50, 0, 8), (44, 50, 0, 8), (48, -10, 0, 4), (60, -10, 0, 4), (72, 0, 0, 0)],
           [(0, 0, 0, 0), (12, -30, 0, 0), (21, 0, 0, 0), (24, -70, 0, 0), (44, -70, 0, 0), (48, -6, 0, 0), (72, 0, 0, 0)])
    a.hair([(0, 0, 0, 0), (12, -30, 0, 0), (16, -26, 0, 8), (20, -30, 0, -8), (24, 26, 0, 0), (32, 16, 0, 4), (38, 16, 0, -4), (44, 16, 0, 4), (48, -14, 0, 0), (60, -10, 0, 0), (72, 0, 0, 0)], delay=1)
    a.done()

    # ---------------- reveal (80; boss model plays 50-80): curled mass at 50 unfurls 50-58, wings snap open, ROAR 62, settle
    a = mk("reveal", 80)
    a.scl("root", (0, 0.45, 0.45, 0.45), (50, 0.45, 0.45, 0.45), (54, 0.7, 0.7, 0.7), (58, 1.0, 1.0, 1.0), (62, 1.06, 1.06, 1.06), (68, 1, 1, 1), (80, 1, 1, 1))
    ball = dict(chest=(-60, 0, 0), head=(-10, 0, 0), arm_r=(100, 40, 20), arm_l=(100, -40, -20), fore_r=(80, 0, 0), fore_l=(80, 0, 0), P_body=(0, -4.0, 0))
    a.at(0, **ball).at(50, **ball)
    a.at(56, chest=(-20, 0, 0), head=(10, 0, 0), arm_r=(40, 0, 50), arm_l=(40, 0, -50), fore_r=(30, 0, 0), fore_l=(30, 0, 0), P_body=(0, -1.6, 0))
    a.at(60, chest=(18, 0, 0), head=(20, 0, 0), arm_r=(50, 30, 30), arm_l=(50, -30, -30), fore_r=(60, 0, 0), fore_l=(60, 0, 0), P_body=(0, 0.8, 0.4))
    a.at(62, chest=(-28, 0, 0), head=(-34, 0, 0), arm_r=(20, 0, 105), arm_l=(20, 0, -105), fore_r=(-10, 0, 0), fore_l=(-10, 0, 0), P_body=(0, -0.8, -0.8))
    for t in range(64, 72, 2):
        j = 1 if t % 4 == 0 else -1
        a.at(t, chest=(-26, 2 * j, 2 * j), head=(-32, 4 * j, -3 * j), arm_r=(20, 0, 102 + 4 * j), arm_l=(20, 0, -102 + 4 * j))
    a.at(80, chest=(0, 0, 0), head=(0, 0, 0), arm_r=(0, 0, 0), arm_l=(0, 0, 0), fore_r=(0, 0, 0), fore_l=(0, 0, 0), P_body=(0, 0, 0))
    a.pos("jaw", (0, 0, 0, 0), (60, 0, 0, 0), (62, 0, -1.6, 0), (70, 0, -1.6, 0), (74, 0, 0, 0))
    a.scl("jaw", (0, 1, 1, 1), (60, 1, 1, 1), (62, 1.3, 3, 1), (70, 1.3, 3, 1), (74, 1, 1, 1))
    a.wings(0, open_=-30, fold=60).wings(50, open_=-30, fold=60).wings(56, open_=20).wings(62, open_=80, fold=-30).wings(70, open_=70, fold=-26).wings(80)
    a.claws(0, curl=40).claws(50, curl=40).claws(56, curl=-20).claws(62, curl=-40, spread=12).claws(72, curl=-30, spread=10).claws(80)
    a.legs([(0, 60, 0, 10), (50, 60, 0, 10), (56, 30, 0, 8), (60, 0, 0, 4), (62, 20, 0, 10), (72, 20, 0, 10), (80, 0, 0, 0)],
           [(0, -100, 0, 0), (50, -100, 0, 0), (56, -50, 0, 0), (60, -6, 0, 0), (62, -30, 0, 0), (72, -30, 0, 0), (80, 0, 0, 0)])
    a.hair([(0, 10, 0, 0), (50, 10, 0, 0), (56, -10, 0, 0), (60, 10, 0, 0), (62, -30, 0, 0), (66, -26, 0, 8), (70, -30, 0, -8), (76, -10, 0, 0), (80, 0, 0, 0)], delay=1)
    a.done()

    # ---------------- death (40): shriek 0-6, claws clutch head, collapse to knees 16, fall forward 28, dissolve flat 32-40
    a = mk("death", 40)
    a.at(0, chest=(0, 0, 0), head=(0, 0, 0), P_body=(0, 0, 0), root=(0, 0, 0))
    a.at(5, chest=(-20, 0, 0), head=(-36, 0, 0), arm_r=(20, 0, 100), arm_l=(20, 0, -100), P_body=(0, 0.6, 0))
    a.at(10, chest=(-30, 0, 4), head=(-20, 6, 6), arm_r=(150, -40, -20), arm_l=(150, 40, 20), fore_r=(90, 0, 0), fore_l=(90, 0, 0))
    a.at(16, chest=(-40, 0, 0), head=(20, 0, -10), arm_r=(20, 0, 20), arm_l=(20, 0, -20), fore_r=(10, 0, 0), fore_l=(10, 0, 0), P_body=(0, -4.0, 0))
    a.at(28, root=(70, 0, 0), P_root=(0, 1.0, -4.0), chest=(-10, 0, 0), head=(10, 0, -20), arm_r=(150, 0, 40), arm_l=(140, 0, -30))
    a.at(40, root=(86, 0, 0), P_root=(0, 0.3, -5.0))
    a.scl("root", (0, 1, 1, 1), (32, 1, 1, 1), (40, 1.3, 1.3, 0.05))
    a.wings(0).wings(5, open_=80, fold=-30).wings(16, open_=20).wings(28, open_=-40, fold=40).wings(40, open_=-50, fold=50)
    a.claws(0).claws(5, curl=-40, spread=12).claws(16, curl=30).claws(40, curl=50)
    a.legs([(0, 0, 0, 0), (5, 0, 0, 10), (16, 70, 0, 10), (28, 20, 0, 6), (40, 10, 0, 6)], [(0, 0, 0, 0), (16, -100, 0, 0), (28, -40, 0, 0), (40, -30, 0, 0)])
    a.hair([(0, 0, 0, 0), (5, -26, 0, 0), (16, 16, 0, 0), (28, 20, 0, 10), (40, 10, 0, 10)], delay=2)
    a.done()


# ================================================================== main
if __name__ == "__main__":
    b1 = Builder("danger_alice", 1.0, False, 8)
    b1.C = C1
    build_p1(b1)
    anims_p1(b1)
    b1.m.save(DIR + "danger_alice.bbmodel")
    print("danger_alice cubes", len(b1.m.cubes))
    b2 = Builder("danger_alice_boss", 2.6, True, 3)
    b2.C = C2
    build_p2(b2)
    anims_p2(b2)
    b2.m.save(DIR + "danger_alice_boss.bbmodel")
    print("danger_alice_boss cubes", len(b2.m.cubes))
