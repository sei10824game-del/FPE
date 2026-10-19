"""Lord Hansel - TRUE FORM / "Windeigo" (variant 2) -> assets/fpe/bbmodels/lord_hansel_true.bbmodel.
Reference: docs/ref/confirmed/hansel_true_form.png. Towering black tree-man (hitbox 2.6 x 8.0 = 128 px): stick-thin black legs that
split into roots at the ground, narrow torso with a glowing red "Γ" mark, a round black head with a glowing red face (ring eye + slit
mouth), black antler-branches, streaming red flame hair, RIGHT arm grown into a huge thorny branch crown, LEFT arm long and thin with
twig claws. Every key tick matches entity/characters/LordHansel.java (true-form abilities, transform2 t80-120).
Run: python3 tools/bbgen/chars/lord_hansel_true.py
"""
import math
from lh_common import Model, Kit, A, ROOT, mix, sinekeys

BLK, BLK_L, BLK_D = 0x111012, 0x2C2A2E, 0x050405
RED, RED_L, RED_D = 0xE01E24, 0xFF6060, 0x7A0A0E
FL, FL_L, FL_D = 0xE8282C, 0xFF7A5A, 0x9A0E14

m = Model("lord_hansel_true", S=4, atlas=2048)
NB = 6
K = Kit(m)
R = m.rng
af, flat, clear = K.all_faces, K.flat, K.clear
barkp = K.bark(BLK, BLK_L, BLK_D)


def chest_front(F):
    barkp(F)
    W, H = F.w, F.h
    # the red "Γ" mark (glowing)
    x0, y0 = W * 0.36, H * 0.18
    F.rect(x0, y0, W * 0.34, H * 0.1, RED, glow=True)
    F.rect(x0, y0, W * 0.1, H * 0.55, RED, glow=True)
    F.rect(x0 + 1, y0 + 1, W * 0.32, 1, RED_L, glow=True)


def face_front(F):
    W, H = F.w, F.h
    for y in range(H):
        for x in range(W):
            F.px(x, y, mix(BLK_L, BLK_D, y / H))
    cx, cy = W * 0.5, H * 0.46
    F.disc(cx, cy, W * 0.42, RED_D, glow=True)
    F.disc(cx, cy, W * 0.38, RED, glow=True)
    F.disc(cx - 1, cy - 1, W * 0.3, RED_L, glow=True)
    F.disc(cx, cy, W * 0.22, RED, glow=True)
    F.disc(cx + 1, cy - 2, W * 0.13, BLK_D)            # the dark eye / mark
    F.disc(cx + 2, cy - 3, 1.0, 0xFFD0D0, glow=True)
    for x in range(int(W * 0.25), int(W * 0.78)):    # jagged slit mouth across the glow
        yy = cy + W * 0.2 + 1.5 * math.sin(x * 1.3)
        F.rect(x, int(yy), 1, 2, BLK_D)


def flamep(F):
    """flame lick: bright core, dark red edges, wavy pointed end at the top (F.h axis)"""
    W, H = F.w, F.h
    for y in range(H):
        u = y / max(1, H - 1)
        half = 0.5 * (0.45 + 0.55 * u) + 0.05 * math.sin(y * 0.6)
        for x in range(W):
            d = abs((x + .5) / W - 0.5)
            if d > half: F.px(x, y, (0, 0, 0, 0))
            elif d > half - 0.12: F.px(x, y, FL_D, glow=True)
            else: F.px(x, y, mix(FL_L, FL, min(1, d * 3 + 0.2)), glow=True)


# ------------------------------------------------------------------ skeleton
m.group("root", (0, 0, 0))
m.group("body", (0, 62, 0), parent="root")
m.group("chest", (0, 64, 0), rot=(-6, 0, 0), parent="body")
m.group("head", (0, 100, -0.5), rot=(4, 0, 0), parent="chest")
m.group("jaw", (0, 104, -6), parent="head")
m.group("antler_r", (3, 112, 0), parent="head")
m.group("antler_l", (-3, 112, 0), parent="head")
for i in range(6):
    m.group(f"hair{i}", (-2.0 - i * 0.6, 108 - i * 1.6, 2.5), parent="head")
# branch arm (character right, +X): raised up and out like a tree crown
m.group("arm_r", (7.5, 96, 0), rot=(0, 0, 150), parent="chest")
m.group("fore_r", (7.5, 76, 0), rot=(0, 0, -30), parent="arm_r")
for j in range(NB):
    m.group(f"br{j}", (7.5, 58, 0), rot=(((j * 37) % 50) - 25, 0, -70 + j * 28), parent="fore_r")
    m.group(f"br{j}b", (7.5, 58 - 16, 0), rot=(0, 0, (-1) ** j * 28), parent=f"br{j}")
    m.group(f"br{j}c", (7.5, 58 - 16 - 13, 0), rot=(10, 0, (-1) ** (j + 1) * 30), parent=f"br{j}b")
m.group("arm_l", (-7.5, 96, 0), rot=(0, 0, -8), parent="chest")
m.group("fore_l", (-7.5, 74, 0), parent="arm_l")
m.group("hand_l", (-7.5, 52, 0), parent="fore_l")
for s, k in ((1, "r"), (-1, "l")):
    m.group("leg_" + k, (4.2 * s, 62, 0), rot=(0, 0, 8 * s), parent="body")
    m.group("shin_" + k, (4.2 * s, 32, 0), rot=(0, 0, -4 * s), parent="leg_" + k)
    m.group("roots_" + k, (4.2 * s, 3, 0), parent="shin_" + k)
m.group("groundroots", (0, 0, 0), parent="root")

# ------------------------------------------------------------------ legs: stick-thin, splitting into roots
for s, k in ((1, "r"), (-1, "l")):
    x = 4.2 * s
    m.cube("thigh_" + k, "leg_" + k, (x - 2.2, 31, -2.2), (x + 2.2, 62.5, 2.2), BLK, faces=af(barkp))
    m.cube("knee_" + k, "shin_" + k, (x - 2.5, 29.5, -2.6), (x + 2.5, 34, 2.2), BLK_L, faces=af(barkp))
    K.thorn("kneethorn_" + k, "shin_" + k, (x, 32, -2.0), 5, 1.6, -70, 0, BLK, BLK_L)
    m.cube("shinc_" + k, "shin_" + k, (x - 1.7, 3, -1.7), (x + 1.7, 32, 1.7), BLK, faces=af(barkp))
    for j, (ry, rx, L) in enumerate(((0, 66, 12), (70, 70, 10), (140, 72, 11), (210, 70, 9), (290, 68, 12))):
        m.cube(f"root{j}_{k}", "roots_" + k, (x - 1.1, 3, -1.1), (x + 1.1, 3 + L, 1.1), BLK, origin=(x, 3, 0), rot=(180 - rx, ry + (40 if s < 0 else 0), 0),
               faces=af(K.grad(BLK_L, BLK_D)))
    for j in range(2):
        K.thorn(f"legthorn{j}_{k}", "leg_" + k, (x + 2 * s, 40 + j * 12, 0), 4, 1.3, 0, -70 * s, BLK, BLK_L)
# loose roots spreading on the ground (art: the silhouette widens into roots)
for j in range(8):
    a = j * 45 + 20
    L = 14 + (j % 3) * 4
    m.cube(f"groot{j}", "groundroots", (-1.0, 0, -1.0), (1.0, L, 1.0), BLK, origin=(0, 0.6, 0), rot=(84, a, 0), faces=af(K.grad(BLK_L, BLK_D)))

# ------------------------------------------------------------------ torso: thin waist, narrow chest, red Γ mark
m.cube("hips", "body", (-5, 58, -3), (5, 64, 3), BLK, faces=af(barkp))
m.cube("waist", "chest", (-3.5, 63, -2.6), (3.5, 78, 2.6), BLK, faces=af(barkp))
m.cube("torso", "chest", (-6.5, 76, -3.4), (6.5, 98, 3.4), BLK, faces={"north": chest_front, "south": barkp, "east": barkp, "west": barkp, "up": barkp, "down": barkp})
for s in (1, -1):
    m.cube(f"shoulder{s}", "chest", (7 * s - 3, 92, -3.2), (7 * s + 3, 98, 3.2), BLK_L, origin=(7 * s, 95, 0), rot=(0, 0, -18 * s), faces=af(barkp))
for j in range(6):   # back branches / spine thorns
    K.thorn(f"spine{j}", "chest", ((-1) ** j * 2, 70 + j * 5, 3), 6 - j * 0.4, 1.6, 64, (-1) ** j * 20, BLK, BLK_L)
m.cube("neck", "chest", (-2, 96, -2), (2, 102, 2), BLK_D, faces=af(barkp))

# ------------------------------------------------------------------ head: round black, glowing red face, antler-branches, flame hair
m.cube("skull", "head", (-6, 100, -6), (6, 113, 5), BLK, faces={"north": face_front, "south": barkp, "east": barkp, "west": barkp, "up": barkp, "down": flat(BLK_D)})
m.cube("cheek_r", "head", (5, 101, -5), (6.8, 108, 3), BLK_L, faces=af(barkp))
m.cube("cheek_l", "head", (-6.8, 101, -5), (-5, 108, 3), BLK_L, faces=af(barkp))
m.cube("jawc", "jaw", (-4.5, 100, -6.4), (4.5, 103.5, -1), BLK_D, faces={"north": K.combo(flat(BLK_D), lambda F: [F.px(x, 0, RED_L, glow=True) for x in range(0, F.w, 3)]), "south": flat(BLK_D), "east": flat(BLK_D), "west": flat(BLK_D), "up": flat(RED, True), "down": flat(BLK_D)})
for s, k in ((1, "r"), (-1, "l")):
    g = "antler_" + k
    p0 = (3 * s, 112, 0)
    p1 = K.seg(f"ab0_{k}", g, p0, 7, 1.8, 6, -20 * s, BLK, barkp)
    p2 = K.seg(f"ab1_{k}", g, p1, 6, 1.5, -6, 14 * s, BLK, barkp)
    p3 = K.seg(f"ab2_{k}", g, p2, 5, 1.2, 4, -20 * s, BLK)
    K.seg(f"ab3_{k}", g, p3, 4, 0.9, 0, 18 * s, BLK)
    K.seg(f"at0_{k}", g, p1, 5, 1.0, -10, -70 * s, BLK)
    K.seg(f"at1_{k}", g, p2, 4.5, 0.9, 16, -60 * s, BLK)
    K.seg(f"at2_{k}", g, p3, 3, 0.7, 0, 50 * s, BLK)
# flame hair: licks streaming up and out to the character's left (-X), glowing
m.cube("hairbase", "head", (-6.6, 104, -2), (3, 114.5, 6.2), FL_D, faces=af(K.combo(flat(FL_D, True), lambda F: [F.line(x, 0, x - 2, F.h, FL, 1, glow=True) for x in range(0, F.w, 3)])))
for i in range(6):
    g = f"hair{i}"
    bx, by = -2.0 - i * 0.6, 108 - i * 1.6
    for j in range(3):
        L = 22 - i * 1.2 + j * 4
        w = 7 - j * 1.4
        rz = 36 + i * 13 + (j - 1) * 14
        m.cube(f"flame{i}{j}", g, (bx - w / 2, by, 2.5 + j * 1.2 - w * 0.3), (bx + w / 2, by + L, 2.5 + j * 1.2 + w * 0.3), FL, origin=(bx, by, 2.5 + j * 1.2),
               rot=(24 + j * 10, j * 20 - 20, rz), faces={"north": flamep, "south": flamep, "east": flamep, "west": flamep, "up": clear, "down": flat(FL_D, True)})

# ------------------------------------------------------------------ branch arm: thick bark limb splitting into thorny branches
m.cube("bupper", "arm_r", (5.5, 76, -2.2), (9.5, 96.5, 2.2), BLK, faces=af(barkp))
m.cube("bfore", "fore_r", (5.8, 56, -2.0), (9.2, 76.5, 2.0), BLK, faces=af(barkp))
for j in range(3):
    K.thorn(f"armthorn{j}", "arm_r", (9.4, 80 + j * 5, 0), 4.5, 1.4, 0, -80, BLK, BLK_L)
for j in range(NB):
    g, gb, gc = f"br{j}", f"br{j}b", f"br{j}c"
    L1, L2, L3 = 16.3, 13.3, 9 - j * 0.5
    m.cube(f"brseg{j}", g, (6.0, 58 - L1, -1.6), (9.0, 58.3, 1.6), BLK, faces=af(barkp))
    m.cube(f"brsegb{j}", gb, (6.5, 42 - L2, -1.1), (8.5, 42.3, 1.1), BLK, faces=af(barkp))
    m.cube(f"brsegc{j}", gc, (7.0, 29 - L3, -0.6), (8.0, 29.3, 0.6), BLK, faces=af(K.grad(BLK_L, BLK_D)))
    for q in range(3):
        yy = 58 - L1 * (0.2 + 0.3 * q)
        m.cube(f"brth{j}{q}", g, (7.5 - 0.5, yy - 5.0, -0.5), (7.5 + 0.5, yy, 0.5), BLK, origin=(7.5, yy, 0), rot=(q * 30 - 30, q * 60, (-1) ** q * 50), faces=af(K.grad(BLK_L, BLK_D)))
        yy = 42 - L2 * (0.2 + 0.3 * q)
        m.cube(f"brthb{j}{q}", gb, (7.5 - 0.35, yy - 3.4, -0.35), (7.5 + 0.35, yy, 0.35), BLK, origin=(7.5, yy, 0), rot=(q * 40 - 40, 0, (-1) ** (q + j) * 55), faces=af(K.grad(BLK_L, BLK_D)))
    K.thorn(f"brtip{j}", gc, (7.5, 29 - L3, 0), 3.0, 0.8, 180, 0, BLK, BLK_L)

# ------------------------------------------------------------------ left arm: long, thin, twig claws
x = -7.5
m.cube("lupper", "arm_l", (x - 1.8, 73, -1.8), (x + 1.8, 96.5, 1.8), BLK, faces=af(barkp))
m.cube("lfore", "fore_l", (x - 1.5, 52, -1.5), (x + 1.5, 74, 1.5), BLK, faces=af(barkp))
K.thorn("lelbow", "fore_l", (x, 73, 1.4), 4, 1.2, 120, 0, BLK, BLK_L)
m.cube("lpalm", "hand_l", (x - 2.0, 48, -2.0), (x + 2.0, 52.5, 2.0), BLK_L, faces=af(barkp))
for f in range(5):
    fz = -1.6 + f * 0.8
    m.cube(f"lfinger{f}", "hand_l", (x - 0.4, 38, fz - 0.4), (x + 0.4, 48.5, fz + 0.4), BLK, origin=(x, 48.5, fz), rot=(-20 + f * 10, 0, -10 + f * 4), faces=af(K.grad(BLK_L, BLK_D)))


# ================================================================== animation
PROPS = ()
BR = [f"br{j}" for j in range(NB)]
BRB = [f"br{j}b" for j in range(NB)]
BRC = [f"br{j}c" for j in range(NB)]
HAIR = [f"hair{i}" for i in range(6)]


def NA(name, ticks, loop=False):
    return A(m, name, ticks, loop, PROPS)


def legs(a, kr, kl=None, sr=None, sl=None):
    a.r("leg_r", *kr)
    a.r("leg_l", *(kl or [(t, x, -y, -z) for (t, x, y, z) in kr]))
    if sr: a.r("shin_r", *sr)
    if sl or sr: a.r("shin_l", *(sl or sr))


def hair(a, keys, delay=1.5):
    """flame hair: x>0 = blown back, z>0 = blown toward +X"""
    for i, b in enumerate(HAIR):
        a.lag(b, [(t, -x * (0.6 + 0.1 * i), 0, -z * 0.5 + x * 0.2) for (t, x, y, z) in keys], delay + i * 0.5)
    return a


def branches(a, keys, delay=1.0, gain=1.0):
    for j in range(NB):
        a.lag(BR[j], keys, delay + j * 0.4, gain * 0.5)
        a.lag(BRB[j], keys, delay * 2 + j * 0.4, gain * 0.7)
        a.lag(BRC[j], keys, delay * 3 + j * 0.4, gain * 0.8)
    return a


# ------------------------------------------------------------------ idle (80 loop): slow swaying like a tree in wind, flame hair flickering, branches creaking
a = NA("idle", 80, loop=True)
a.rot("body", (0, 0, 0, 1.5), (40, 0, 0, -1.5), (80, 0, 0, 1.5))
a.rot("chest", (0, 0, 0, -1), (20, 2, 3, -2), (40, 0, 0, 1), (60, 2, -3, 2), (80, 0, 0, -1))
a.rot("head", (0, 0, 0, 4), (30, 4, 6, 8), (50, 0, -4, 0), (80, 0, 0, 4))
a.rot("arm_r", (0, 0, 0, 0), (40, 0, 0, -6), (80, 0, 0, 0))
a.rot("arm_l", (0, 4, 0, -2), (40, 8, 0, -4), (80, 4, 0, -2))
a.rot("hand_l", (0, 0, 0, 0), (56, 0, 0, 0), (59, -20, 0, 0), (62, 10, 0, 0), (65, 0, 0, 0), (80, 0, 0, 0))
for j in range(NB):
    a.rot(BR[j], *sinekeys(80, 10, (2, 0, 4), j * 9))
    a.rot(BRB[j], *sinekeys(80, 10, (3, 0, 6), j * 9 + 10))
for i in range(6):
    a.rot(HAIR[i], *sinekeys(20, 2, (6, 4, 8), i * 3))   # flicker (fast 1 s loop inside the 4 s loop)
a.rot("jaw", (0, 0, 0, 0), (60, 0, 0, 0), (64, 10, 0, 0), (70, 0, 0, 0), (80, 0, 0, 0))
a.done()

# ------------------------------------------------------------------ walk (32 loop): ponderous giant strides, whole body swaying, branches rocking
a = NA("walk", 32, loop=True)
a.pos("body", (0, 0, 0, 0), (8, 0, 1.6, 0), (16, 0, 0, 0), (24, 0, 1.6, 0), (32, 0, 0, 0))
a.rot("body", (0, -2, 6, 3), (8, -3, 0, 0), (16, -2, -6, -3), (24, -3, 0, 0), (32, -2, 6, 3))
a.rot("leg_r", (0, 24, 0, 0), (8, 0, 0, 0), (16, -22, 0, 0), (24, 0, 0, 0), (32, 24, 0, 0))
a.rot("leg_l", (0, -22, 0, 0), (8, 0, 0, 0), (16, 24, 0, 0), (24, 0, 0, 0), (32, -22, 0, 0))
a.rot("shin_r", (0, 0, 0, 0), (18, -34, 0, 0), (25, -10, 0, 0), (32, 0, 0, 0))
a.rot("shin_l", (0, 0, 0, 0), (2, -34, 0, 0), (9, -10, 0, 0), (16, 0, 0, 0), (32, 0, 0, 0))
a.rot("arm_l", (0, 20, 0, -4), (16, -16, 0, -4), (32, 20, 0, -4))
a.rot("arm_r", (0, -6, 0, 4), (16, 6, 0, -4), (32, -6, 0, 4))
a.rot("head", (0, 4, 0, -3), (16, 4, 0, 3), (32, 4, 0, -3))
for j in range(NB):
    a.rot(BR[j], (0, 4, 0, 6), (16, -4, 0, -6), (32, 4, 0, 6))
for i in range(6):
    a.rot(HAIR[i], (0, -14, 0, 6), (8 + i, -8, 0, 0), (16, -14, 0, -6), (24 + i * 0.5, -8, 0, 0), (32, -14, 0, 6))
a.done()

# ------------------------------------------------------------------ branch_sweep (44): branch crown hauled back + across the body 0-16, SWEEPS through the front arc t20, overshoot, recover
a = NA("branch_sweep", 44)
a.r("chest", (8, 4, 40, 0), (16, 8, 50, 0), (20, -10, -36, 0), (24, -10, -44, 0), (32, -4, -16, 0), (42, 0, 0, 0))
a.r("head", (16, 0, -30, 0), (20, -6, 20, 0), (30, 0, 10, 0), (40, 0, 0, 0))
a.r("arm_r", (8, 20, 40, 10), (16, 30, 60, 20), (18, 10, 20, -20), (20, -30, -40, -70), (24, -34, -50, -80), (32, -10, -20, -30), (42, 0, 0, 0))
a.r("fore_r", (16, 0, 0, -20), (20, 0, 0, 20), (26, 0, 0, 10), (40, 0, 0, 0))
branches(a, [(0, 0, 0, 0), (16, -20, 0, 20), (20, 30, 0, -30), (26, 10, 0, -10), (40, 0, 0, 0)], 1.0)
a.r("arm_l", (16, -20, 0, -30), (20, 30, 0, -20), (30, 10, 0, -10), (42, 0, 0, 0))
legs(a, [(16, 10, 0, 0), (20, -20, 0, 0), (32, -10, 0, 0), (42, 0, 0, 0)], [(16, -10, 0, 0), (20, 16, 0, 0), (32, 8, 0, 0), (42, 0, 0, 0)])
a.p("body", (16, 0, -1, 1), (20, 0, -2, -2), (30, 0, -1, -1), (42, 0, 0, 0))
hair(a, [(0, 0, 0, 0), (16, -6, 0, 20), (20, 10, 0, -30), (28, 4, 0, -10), (40, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ root_eruption (46): raises the right leg high 0-14, STAMPS t18 (whole body drops, roots flare), roots twist, recovers
a = NA("root_eruption", 46)
a.r("leg_r", (8, 50, 0, 10), (14, 70, 0, 14), (16, 30, 0, 6), (18, -6, 0, 0), (30, -6, 0, 0), (40, 0, 0, 0))
a.r("shin_r", (8, -60, 0, 0), (14, -80, 0, 0), (18, 0, 0, 0))
a.r("leg_l", (14, -10, 0, -6), (18, 10, 0, -10), (30, 10, 0, -8), (40, 0, 0, 0))
a.r("shin_l", (14, 20, 0, 0), (18, -20, 0, 0), (30, -16, 0, 0), (40, 0, 0, 0))
a.r("chest", (14, 10, 0, -8), (18, -16, 0, 0), (30, -12, 0, 0), (40, 0, 0, 0))
a.r("head", (14, 10, 0, 0), (18, -10, 0, 0), (20, 6, 0, 0), (36, 0, 0, 0))
a.r("jaw", (16, 0, 0, 0), (18, 30, 0, 0), (28, 20, 0, 0), (34, 0, 0, 0))
a.p("body", (14, 0, 2, 0), (18, 0, -5, 0), (30, 0, -4, 0), (40, 0, 0, 0))
a.r("arm_l", (14, -20, 0, -40), (18, 20, 0, -30), (30, 10, 0, -30), (42, 0, 0, 0))
a.r("arm_r", (14, 0, 0, 20), (18, 0, 0, -20), (30, 0, 0, -10), (42, 0, 0, 0))
a.s("roots_r", (16, 1, 1, 1), (18, 1.8, 0.6, 1.8), (22, 1.4, 0.9, 1.4), (34, 1, 1, 1))
a.s("groundroots", (16, 1, 1, 1), (18, 1.5, 2.5, 1.5), (24, 1.3, 1.6, 1.3), (36, 1, 1, 1))
branches(a, [(0, 0, 0, 0), (14, -10, 0, 0), (18, 20, 0, 0), (24, -6, 0, 0), (34, 0, 0, 0)])
hair(a, [(0, 0, 0, 0), (14, -10, 0, 0), (18, 16, 0, 0), (26, 4, 0, 0), (38, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ impale_roots (44): left claw thrust down + up three times, each pull summons a root: peaks t14 / t24 / t34
a = NA("impale_roots", 44)
a.r("arm_l", (4, 60, 0, -30), (10, 80, 0, -40), (14, -40, 0, -20), (18, 60, 0, -30), (24, -40, 0, -20), (28, 60, 0, -30), (34, -50, 0, -16), (40, 10, 0, -10), (44, 0, 0, 0))
a.r("fore_l", (10, 40, 0, 0), (14, 0, 0, 0), (18, 40, 0, 0), (24, 0, 0, 0), (28, 40, 0, 0), (34, 0, 0, 0), (42, 0, 0, 0))
a.r("hand_l", (10, -40, 0, 0), (14, 40, 0, 0), (18, -40, 0, 0), (24, 40, 0, 0), (28, -40, 0, 0), (34, 50, 0, 0), (42, 0, 0, 0))
a.r("chest", (10, -10, -10, 0), (14, 6, -16, 0), (18, -10, -10, 0), (24, 6, -16, 0), (28, -10, -10, 0), (34, 8, -18, 0), (42, 0, 0, 0))
a.r("head", (10, -14, 0, 0), (14, -20, 0, 0), (24, -20, 0, 0), (34, -22, 0, 0), (42, 0, 0, 0))
a.r("jaw", (14, 20, 0, 0), (24, 24, 0, 0), (34, 30, 0, 0), (40, 0, 0, 0))
a.p("body", (10, 0, -1.6, 0), (14, 0, 0.4, 0), (18, 0, -1.6, 0), (24, 0, 0.4, 0), (28, 0, -1.6, 0), (34, 0, 0.6, 0), (42, 0, 0, 0))
branches(a, [(0, 0, 0, 0), (14, 10, 0, 6), (24, 10, 0, -6), (34, 14, 0, 6), (42, 0, 0, 0)])
legs(a, [(10, -10, 0, 4), (34, -10, 0, 4), (42, 0, 0, 0)], sr=[(10, 20, 0, 0), (34, 20, 0, 0), (42, 0, 0, 0)])
hair(a, [(0, 0, 0, 0), (14, 6, 0, 0), (24, 6, 0, 0), (34, 8, 0, 0), (42, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ branch_grab (60): branch crown reaches forward + closes t18 (grab), lifts high 18-28, crushes t30 / t38, SLAMS down t48, recover
a = NA("branch_grab", 60)
a.r("arm_r", (8, 20, 0, 10), (14, 60, 0, -40), (18, 80, 0, -70), (22, 70, 0, -60), (28, 30, 0, -10), (30, 34, 0, -14), (32, 28, 0, -10), (38, 34, 0, -14), (40, 28, 0, -10), (44, 20, 0, -6), (48, 120, 0, -110), (52, 110, 0, -100), (58, 0, 0, 0))
a.r("fore_r", (14, 0, 0, 30), (18, 0, 0, 40), (30, 0, 0, 10), (48, 0, 0, 40), (58, 0, 0, 0))
for j in range(NB):   # branches clamp shut like fingers on t18, squeeze on t30 / t38
    s = 1 if j < 2 else -1
    a.r(BR[j], (14, -20 * s, 0, 30 * s), (18, 30 * s, 0, -30 * s), (28, 30 * s, 0, -30 * s), (30, 40 * s, 0, -40 * s), (32, 30 * s, 0, -30 * s), (38, 40 * s, 0, -40 * s), (40, 30 * s, 0, -30 * s), (48, 30 * s, 0, -30 * s), (50, -20 * s, 0, 30 * s), (58, 0, 0, 0))
    a.r(BRB[j], (14, 0, 0, 20 * s), (18, 0, 0, -40 * s), (48, 0, 0, -40 * s), (51, 0, 0, 20 * s), (58, 0, 0, 0))
a.r("chest", (14, -20, 20, 0), (18, -24, 10, 0), (28, 8, 0, 0), (44, 10, 0, 0), (48, -30, 0, 0), (52, -26, 0, 0), (58, 0, 0, 0))
a.r("head", (14, -10, 10, 0), (28, 20, 0, 0), (44, 20, 0, 0), (48, -14, 0, 0), (56, 0, 0, 0))
a.r("jaw", (28, 20, 0, 0), (30, 34, 0, 0), (34, 20, 0, 0), (38, 36, 0, 0), (44, 20, 0, 0), (48, 40, 0, 0), (56, 0, 0, 0))
a.r("arm_l", (14, 30, 0, -30), (28, -20, 0, -20), (48, 40, 0, -20), (58, 0, 0, 0))
a.p("body", (14, 0, -1.6, -1.6), (18, 0, -2, -2.4), (28, 0, 0, -0.6), (44, 0, 0.6, 0), (48, 0, -3.6, -1.4), (54, 0, -2, -1), (60, 0, 0, 0))
legs(a, [(14, -20, 0, 0), (28, -6, 0, 0), (48, -30, 0, 0), (58, 0, 0, 0)], [(14, 16, 0, 0), (28, 6, 0, 0), (48, 20, 0, 0), (58, 0, 0, 0)])
hair(a, [(0, 0, 0, 0), (18, 10, 0, 0), (28, -8, 0, 0), (48, 20, 0, 0), (56, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ flame_hair (50): head dips + coils 0-14, WHIPS forward t16 and sweeps the flame hair left-right across the front 16-38, flames flare (scale), settle
a = NA("flame_hair", 50)
a.r("head", (8, 20, 30, 0), (14, 26, 40, 0), (16, -30, 30, 0), (22, -34, 0, 0), (28, -34, -30, 0), (34, -34, 0, 0), (38, -30, 30, 0), (44, 0, 0, 0))
a.r("chest", (14, 10, 20, 0), (16, -14, 16, 0), (22, -16, 0, 0), (28, -16, -16, 0), (34, -16, 0, 0), (38, -14, 16, 0), (46, 0, 0, 0))
a.r("jaw", (14, 0, 0, 0), (16, 40, 0, 0), (38, 40, 0, 0), (44, 0, 0, 0))
for i in range(6):
    a.r(HAIR[i], (8, 30, 0, 20), (14, 40, 0, 30), (16 + i * 0.5, -110, 0, 30), (22 + i * 0.5, -120, 0, 0), (28 + i * 0.5, -110, 0, -40), (34 + i * 0.5, -120, 0, 0), (38 + i * 0.5, -110, 0, 30), (44 + i * 0.5, -10, 0, 0), (50, 0, 0, 0))
    a.s(HAIR[i], (14, 1, 1, 1), (16, 1.6, 2.2, 1.6), (38, 1.7, 2.2, 1.7), (44, 1.1, 1.1, 1.1), (50, 1, 1, 1))
a.r("arm_l", (14, 20, 0, -40), (22, 20, 0, -50), (38, 20, 0, -40), (46, 0, 0, 0))
branches(a, [(0, 0, 0, 0), (16, 10, 0, 10), (28, 10, 0, -10), (38, 10, 0, 10), (46, 0, 0, 0)])
a.p("body", (14, 0, -1, 1), (16, 0, -1.6, -1.4), (38, 0, -1.6, -1.4), (46, 0, 0, 0))
legs(a, [(14, 10, 0, 0), (16, -16, 0, 0), (38, -16, 0, 0), (46, 0, 0, 0)], [(14, -8, 0, 0), (16, 14, 0, 0), (38, 14, 0, 0), (46, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ thorn_rain (64): both arms flung up 0-18, branches bristle; pumping the claws down/up every 6 ticks while thorns rain (20-56), lower
a = NA("thorn_rain", 64)
a.r("arm_l", (10, 150, 0, -30), (18, 175, 0, -20), (56, 175, 0, -20), (62, 0, 0, 0))
a.r("hand_l", (20, 0, 0, 0), (23, -40, 0, 0), (26, 20, 0, 0), (29, -40, 0, 0), (32, 20, 0, 0), (35, -40, 0, 0), (38, 20, 0, 0), (41, -40, 0, 0), (44, 20, 0, 0), (47, -40, 0, 0), (50, 20, 0, 0), (53, -40, 0, 0), (56, 0, 0, 0))
a.r("arm_r", (10, 0, 0, 20), (18, 0, 0, 30), (56, 0, 0, 30), (62, 0, 0, 0))
for j in range(NB):
    a.r(BR[j], (18, -10, 0, (j - 2) * 12), (56, -10, 0, (j - 2) * 12), (62, 0, 0, 0))
    a.r(BRB[j], *[(t, 0, 0, ((-1) ** (t // 3)) * 10) for t in range(20, 57, 3)])
a.r("chest", (10, 14, 0, 0), (18, 20, 0, 0), (56, 20, 0, 0), (62, 0, 0, 0))
a.r("head", (10, 30, 0, 0), (18, 40, 0, 0), (56, 40, 0, 0), (62, 0, 0, 0))
a.r("jaw", (18, 40, 0, 0), (56, 40, 0, 0), (62, 0, 0, 0))
a.p("body", *[(t, 0, (0.8 if (t // 3) % 2 else 0), 0) for t in range(18, 57, 3)])
legs(a, [(18, 0, 0, 6), (56, 0, 0, 6), (62, 0, 0, 0)])
hair(a, [(0, 0, 0, 0), (18, -20, 0, 0), (56, -20, 0, 0), (62, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ forest_cage (50): kneels and drives the branch crown into the ground t16 (ring rises), holds; twists it t32 (center root bursts), pulls free
a = NA("forest_cage", 50)
a.r("arm_r", (8, 40, 0, 40), (12, 60, 0, 10), (16, 100, 0, -80), (30, 100, 0, -80), (32, 100, 40, -80), (38, 90, 40, -70), (46, 0, 0, 0))
a.r("fore_r", (16, 0, 0, 40), (38, 0, 0, 40), (46, 0, 0, 0))
branches(a, [(0, 0, 0, 0), (12, -20, 0, 0), (16, 40, 0, 0), (30, 40, 0, 0), (32, 50, 0, 20), (40, 10, 0, 0), (48, 0, 0, 0)])
a.r("chest", (8, 10, 0, 0), (16, -34, 10, 0), (30, -34, 10, 0), (32, -38, 20, 0), (40, -20, 0, 0), (48, 0, 0, 0))
a.r("head", (16, 10, 0, 0), (32, 20, -10, 0), (44, 0, 0, 0))
a.r("jaw", (16, 30, 0, 0), (32, 40, 0, 0), (42, 0, 0, 0))
a.p("body", (8, 0, 1, 0), (16, 0, -14, -2), (30, 0, -14, -2), (32, 0, -15, -2), (40, 0, -6, 0), (48, 0, 0, 0))
legs(a, [(16, -70, 0, 6), (40, -30, 0, 4), (48, 0, 0, 0)], [(16, 10, 0, -6), (40, 4, 0, -4), (48, 0, 0, 0)], sr=[(16, 100, 0, 0), (40, 40, 0, 0), (48, 0, 0, 0)], sl=[(16, -80, 0, 0), (40, -30, 0, 0), (48, 0, 0, 0)])
a.r("arm_l", (16, 40, 0, -30), (40, 20, 0, -20), (48, 0, 0, 0))
a.s("groundroots", (14, 1, 1, 1), (16, 1.6, 3, 1.6), (30, 1.4, 2.4, 1.4), (32, 1.8, 3.2, 1.8), (44, 1, 1, 1))
hair(a, [(0, 0, 0, 0), (16, 20, 0, 0), (32, 10, 0, 10), (44, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ stomp (30): lifts the left leg 0-10, STOMP t13, shudder, recover
a = NA("stomp", 30)
a.r("leg_l", (6, 40, 0, -8), (10, 56, 0, -10), (13, -4, 0, 0), (20, -4, 0, 0), (28, 0, 0, 0))
a.r("shin_l", (6, -50, 0, 0), (10, -70, 0, 0), (13, 0, 0, 0))
a.r("leg_r", (10, -8, 0, 4), (13, 10, 0, 6), (22, 6, 0, 4), (28, 0, 0, 0))
a.r("shin_r", (13, -12, 0, 0), (22, -8, 0, 0), (28, 0, 0, 0))
a.r("chest", (10, 10, 0, 6), (13, -12, 0, 0), (20, -8, 0, 0), (28, 0, 0, 0))
a.r("head", (10, 10, 0, 0), (13, -10, 0, 0), (15, 6, 0, 0), (24, 0, 0, 0))
a.p("body", (10, 0, 2, 0), (13, 0, -4, 0), (18, 0, -2.6, 0), (28, 0, 0, 0))
a.r("arm_l", (10, -10, 0, -30), (13, 20, 0, -20), (24, 0, 0, 0))
a.s("roots_l", (12, 1, 1, 1), (13, 1.8, 0.6, 1.8), (17, 1.3, 0.9, 1.3), (26, 1, 1, 1))
branches(a, [(0, 0, 0, 0), (10, -10, 0, 0), (13, 16, 0, 0), (18, -6, 0, 0), (26, 0, 0, 0)])
hair(a, [(0, 0, 0, 0), (10, -8, 0, 0), (13, 14, 0, 0), (22, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ hunger_roar (50): hunches + draws in 0-14, RAISES the head and ROARS t18 (face flares, jaw wide), branches + arms spread, shakes to 40, settles
a = NA("hunger_roar", 50)
a.r("chest", (8, -20, 0, 0), (14, -24, 0, 0), (18, 24, 0, 0), (40, 20, 0, 0), (48, 0, 0, 0))
a.r("head", (8, -20, 0, 0), (14, -26, 0, 0), (18, 36, 0, 0), (22, 30, 4, 4), (26, 36, -4, -4), (30, 30, 4, 4), (34, 36, -4, -4), (40, 30, 0, 0), (48, 0, 0, 0))
a.r("jaw", (14, 0, 0, 0), (18, 50, 0, 0), (40, 50, 0, 0), (46, 0, 0, 0))
a.s("head", (14, 1, 1, 1), (18, 1.15, 1.15, 1.15), (40, 1.1, 1.1, 1.1), (46, 1, 1, 1))
a.r("arm_l", (14, 30, 0, 10), (18, -20, 0, -70), (40, -24, 0, -72), (48, 0, 0, 0))
a.r("arm_r", (14, -10, 0, -20), (18, 0, 0, 20), (40, 0, 0, 20), (48, 0, 0, 0))
branches(a, [(0, 0, 0, 0), (14, -20, 0, 0), (18, 30, 0, 0), (22, 20, 0, 6), (26, 30, 0, -6), (30, 20, 0, 6), (40, 24, 0, 0), (48, 0, 0, 0)])
a.p("body", (14, 0, -2, 0), (18, 0, 1, 0), (40, 0, 1, 0), (48, 0, 0, 0))
legs(a, [(14, 10, 0, 4), (18, 0, 0, 8), (40, 0, 0, 8), (48, 0, 0, 0)], sr=[(14, -16, 0, 0), (18, 0, 0, 0)])
for i in range(6):
    a.r(HAIR[i], (14, 20, 0, 0), (18 + i * 0.4, -30, 0, -20), (40, -30, 0, -20), (48, 0, 0, 0))
    a.s(HAIR[i], (14, 0.9, 0.9, 0.9), (18, 1.7, 2.0, 1.7), (40, 1.6, 1.9, 1.6), (48, 1, 1, 1))
a.done()

# ------------------------------------------------------------------ windeigo_feast (86): roar to the sky 0-14, claws down t20 (cage), three ground-punches with the branch crown t34 / t42 / t50,
# rises to full height 54-62, then BOTH arms crash down t66, hold, recover
a = NA("windeigo_feast", 86)
a.r("chest", (8, 26, 0, 0), (14, 30, 0, 0), (20, -20, 0, 0), (30, -10, 0, 0), (34, -30, 0, 0), (38, -10, 0, 0), (42, -30, 0, 0), (46, -10, 0, 0), (50, -32, 0, 0), (56, 10, 0, 0), (62, 24, 0, 0), (66, -44, 0, 0), (76, -40, 0, 0), (86, 0, 0, 0))
a.r("head", (8, 40, 0, 0), (14, 44, 0, 0), (20, -10, 0, 0), (34, -6, 0, 0), (56, 20, 0, 0), (62, 30, 0, 0), (66, -10, 0, 0), (72, 10, 0, 0), (84, 0, 0, 0))
a.r("jaw", (6, 50, 0, 0), (16, 40, 0, 0), (20, 20, 0, 0), (62, 40, 0, 0), (66, 50, 0, 0), (78, 30, 0, 0), (86, 0, 0, 0))
a.r("arm_l", (8, -30, 0, -60), (14, -30, 0, -70), (20, 40, 0, -20), (30, 20, 0, -30), (56, 120, 0, -20), (62, 170, 0, -16), (66, 40, 0, -10), (76, 40, 0, -10), (86, 0, 0, 0))
a.r("arm_r", (8, 0, 0, 20), (20, 40, 0, -20), (30, 30, 0, 0), (34, 90, 0, -80), (38, 40, 0, -20), (42, 90, 0, -80), (46, 40, 0, -20), (50, 95, 0, -84), (56, -20, 0, 20), (62, -30, 0, 30), (66, 100, 0, -90), (76, 96, 0, -86), (86, 0, 0, 0))
branches(a, [(0, 0, 0, 0), (14, 20, 0, 0), (34, 40, 0, 0), (38, -10, 0, 0), (42, 40, 0, 0), (46, -10, 0, 0), (50, 40, 0, 0), (62, -20, 0, 0), (66, 40, 0, 0), (78, 10, 0, 0), (86, 0, 0, 0)], 0.6)
a.p("body", (14, 0, 1.6, 0), (20, 0, -2, 0), (34, 0, -5, -1), (38, 0, -2, 0), (42, 0, -5, -1), (46, 0, -2, 0), (50, 0, -5, -1), (62, 0, 2, 0), (66, 0, -8, -2), (76, -0, -7, -2), (86, 0, 0, 0))
legs(a, [(20, -20, 0, 6), (34, -40, 0, 8), (50, -40, 0, 8), (62, 0, 0, 6), (66, -60, 0, 10), (76, -56, 0, 10), (86, 0, 0, 0)], sr=[(34, 50, 0, 0), (50, 50, 0, 0), (62, 0, 0, 0), (66, 80, 0, 0), (76, 76, 0, 0), (86, 0, 0, 0)])
a.s("groundroots", (32, 1, 1, 1), (34, 1.4, 2, 1.4), (42, 1.6, 2.4, 1.6), (50, 1.8, 2.8, 1.8), (66, 2.2, 3.4, 2.2), (78, 1.4, 1.6, 1.4), (86, 1, 1, 1))
for i in range(6):
    a.r(HAIR[i], (8, -40, 0, -10), (14, -50, 0, -10), (20, 20, 0, 0), (34, 30, 0, 10), (50, 30, 0, -10), (62, -40, 0, 0), (66 + i * 0.4, 40, 0, 0), (80, 10, 0, 0), (86, 0, 0, 0))
    a.s(HAIR[i], (6, 1.5, 1.8, 1.5), (60, 1.5, 1.8, 1.5), (66, 2, 2.4, 2), (80, 1.2, 1.2, 1.2), (86, 1, 1, 1))
a.done()

# ------------------------------------------------------------------ transform2 (120; this model shows t80-120): grows out of the premature husk 80-92 (scale 0.45 -> 1.05 -> 1),
# branches unfurl, hair ignites, ROAR t100 with arms flung up, settle by 120
a = NA("transform2", 120)
a.s("root", (80, 0.45, 0.45, 0.45), (86, 0.8, 0.85, 0.8), (92, 1.05, 1.06, 1.05), (96, 1, 1, 1), (120, 1, 1, 1))
a.r("chest", (80, -30, 0, 0), (92, -10, 0, 0), (98, -16, 0, 0), (100, 24, 0, 0), (110, 20, 0, 0), (120, 0, 0, 0))
a.r("head", (80, -20, 0, 0), (96, -20, 0, 0), (100, 40, 0, 0), (104, 34, 4, 4), (108, 40, -4, -4), (112, 30, 0, 0), (120, 0, 0, 0))
a.r("jaw", (96, 0, 0, 0), (100, 50, 0, 0), (112, 46, 0, 0), (120, 0, 0, 0))
a.r("arm_l", (80, 60, 0, 30), (92, 40, 0, 0), (98, 50, 0, 10), (100, -20, 0, -80), (112, -20, 0, -76), (120, 0, 0, 0))
a.r("arm_r", (80, 0, 0, -130), (88, 0, 0, -80), (94, 0, 0, -20), (100, 0, 0, 20), (112, 0, 0, 16), (120, 0, 0, 0))
for j in range(NB):
    a.r(BR[j], (80, 0, 0, 60), (88 + j, 0, 0, 30), (94 + j, 0, 0, -10), (100, 10, 0, 6), (120, 0, 0, 0))
    a.s(BR[j], (80, 0.2, 0.2, 0.2), (88 + j, 0.7, 0.7, 0.7), (94 + j, 1.15, 1.15, 1.15), (98 + j, 1, 1, 1), (120, 1, 1, 1))
for i in range(6):
    a.s(HAIR[i], (80, 0.05, 0.05, 0.05), (90 + i, 0.05, 0.05, 0.05), (94 + i, 1.4, 1.8, 1.4), (100, 1.8, 2.2, 1.8), (112, 1.4, 1.6, 1.4), (120, 1, 1, 1))
    a.r(HAIR[i], (94, -20, 0, 0), (100, -40, 0, -20), (112, -30, 0, -10), (120, 0, 0, 0))
a.p("body", (80, 0, -8, 0), (92, 0, -2, 0), (98, 0, -3, 0), (100, 0, 2, 0), (112, 0, 1, 0), (120, 0, 0, 0))
legs(a, [(80, -40, 0, 10), (92, -10, 0, 6), (98, -16, 0, 6), (100, 0, 0, 10), (112, 0, 0, 8), (120, 0, 0, 0)], sr=[(80, 60, 0, 0), (92, 16, 0, 0), (98, 24, 0, 0), (100, 0, 0, 0)])
a.s("groundroots", (80, 0.1, 0.1, 0.1), (100, 1.6, 2.6, 1.6), (112, 1.2, 1.4, 1.2), (120, 1, 1, 1))
a.done()

# ------------------------------------------------------------------ death (40): the fire goes out, branches droop, knees give, topples backward like a felled tree
a = NA("death", 40)
for i in range(6):
    a.s(HAIR[i], (4, 1.4, 1.6, 1.4), (14, 0.5, 0.5, 0.5), (22, 0.05, 0.05, 0.05), (40, 0.05, 0.05, 0.05))
a.r("head", (4, 30, 0, 0), (14, -20, 0, 10), (40, -26, 0, 14))
a.r("jaw", (4, 40, 0, 0), (40, 30, 0, 0))
for j in range(NB):
    a.r(BR[j], (10 + j, 0, 0, 0), (20 + j, 40, 0, 30), (40, 44, 0, 34))
a.r("arm_r", (14, 0, 0, 0), (24, 0, 0, -60), (40, 0, 0, -64))
a.r("arm_l", (14, 20, 0, -20), (24, 0, 0, -40), (40, 0, 0, -44))
legs(a, [(10, -10, 0, 0), (18, -30, 0, 6), (40, -30, 0, 6)], sr=[(18, 40, 0, 0), (40, 40, 0, 0)])
a.r("root", (14, 0, 0, 0), (22, 30, 0, 0), (30, 84, 0, 0), (34, 78, 0, 0), (38, 82, 0, 0), (40, 82, 0, 0))
a.p("root", (14, 0, 0, 0), (22, 0, -6, 0), (40, 0, -8, 0))
a.done()

m.save(ROOT + "lord_hansel_true.bbmodel")
print("cubes", len(m.cubes), "anims", len(m.anims))
