"""Red Circle (DANGER AU Miss Circle, "pyromaniac") - generates assets/fpe/bbmodels/red_circle.bbmodel.
Reference: docs/ref/confirmed/red_circle.jpg - purple-black very long hair, black wolf-ear hat with an orange band over the eyes,
huge shark-tooth grin, orange fringed poncho over a dark top, peach-orange trousers, bandaged right forearm + black claw glove,
strapped black boots, orange hip pouch, FLAMETHROWER in the left hand.
Blockbench space: Y up, ground 0, faces -Z. Character's RIGHT = +X.
Rotation sign cheat-sheet (file values): arm/leg rx>0 = swing forward, torso/head rx>0 = lean back / look up,
ry>0 = turn to the character's left, rz>0 = hanging part swings toward +X (character's right).
Run: python3 tools/bbgen/chars/red_circle.py
"""
import math, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from bbgen import Model, mix  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "../../../src/main/resources/assets/fpe/bbmodels/red_circle.bbmodel")

# ------------------------------------------------------------------ palette
HAIR, HAIR_HI, HAIR_D = 0x2C2142, 0x4E3B70, 0x150F22
SKIN, SKIN_D = 0xD9D3DC, 0xA79EB0
TOP, TOP_D, TOP_L = 0x2A2433, 0x1B1722, 0x3A3346
PON, PON_D, PON_L = 0xF2962A, 0xC4661C, 0xFBB458
PANT, PANT_D, PANT_L = 0xEDBB86, 0xB98450, 0xF8D6AE
BAND, BAND_D = 0xE8872A, 0xB05A18
HAT, HAT_L = 0x17141D, 0x2E2938
BOOT, BOOT_L = 0x18161E, 0x302C38
STRAP, STRAP_D = 0xDA8232, 0x9A5520
GLOVE, GLOVE_L = 0x141219, 0x2C2834
CLAW, CLAW_L = 0x3C3846, 0xE4E0EA
BANDAGE, BANDAGE_D = 0xEEE9DE, 0xB9B1A2
STEEL, STEEL_D, STEEL_L = 0x7C828E, 0x42464F, 0xA9AFBA
TANK, TANK_D = 0x3A2E2A, 0x241C1A
MOUTH, TEETH, LIP = 0x2B0C14, 0xF6F2F2, 0x1A1018
F_CORE, F_MID, F_OUT, F_TIP = 0xFFF2B0, 0xFFB028, 0xFF6418, 0xD02A10

m = Model("red_circle", S=8, atlas=1024)
R = m.rng


# ------------------------------------------------------------------ painters
def strands(base, hi, dark, every=3):
    """vertical hair streaks + darker roots/tips."""
    def f(F):
        cols = [R.random() for _ in range(F.w)]
        for x in range(F.w):
            c = base
            if cols[x] > 0.78: c = hi
            elif cols[x] < 0.22: c = dark
            for y in range(F.h):
                t = y / max(1, F.h - 1)
                cc = mix(c, dark, 0.35 * abs(t - 0.4))
                if (x + int(y / 7)) % every == 0 and R.random() < 0.5:
                    cc = mix(cc, hi, 0.4)
                F.px(x, y, cc)
    return f


def all_faces(fn, skip=()):
    return {k: fn for k in ("north", "south", "east", "west", "up", "down") if k not in skip}


def hstripe(c, y0, h):
    def f(F):
        F.rect(0, y0, F.w, h, c)
    return f


def frame(c):
    def f(F):
        F.rect(0, 0, F.w, 1, c); F.rect(0, F.h - 1, F.w, 1, c)
    return f


def combo(*fns):
    def f(F):
        for fn in fns: fn(F)
    return f


def cloth_folds(base, dark, light, n=4):
    def f(F):
        for i in range(n):
            x = int((i + 0.5) * F.w / n) + R.randint(-1, 1)
            for y in range(F.h):
                F.px(x, y, mix(base, dark, 0.55))
                F.px(x + 1, y, mix(base, light, 0.35))
        F.rect(0, F.h - 2, F.w, 2, mix(base, dark, 0.4))
    return f


def bandage(F):
    for y in range(F.h):
        for x in range(F.w):
            v = (x + y * 2) % 9
            c = BANDAGE if v > 1 else BANDAGE_D
            if R.random() < 0.06: c = mix(BANDAGE, BANDAGE_D, 0.5)
            F.px(x, y, c)
    for y in range(0, F.h, 6):
        F.rect(0, y, F.w, 1, mix(BANDAGE, BANDAGE_D, 0.6))


def face_front(F):
    W, H = F.w, F.h  # 48 x 48 (6 x 6 units), top = y 33.4
    for y in range(H):
        for x in range(W):
            F.px(x, y, mix(SKIN, SKIN_D, max(0, (14 - y) / 14) * 0.6))  # shadow under the hat band
    cx = W / 2
    # huge shark grin: corners pulled up
    for x in range(3, W - 3):
        u = (x + .5 - cx) / (cx - 3)
        top = 30 - 2.2 * (1 - u * u) - 6 * u * u
        bot = 42 - 13 * u * u
        if bot <= top + 1: continue
        for y in range(int(top), int(bot) + 1):
            F.px(x, y, MOUTH if y > top + 0.5 else LIP)
        F.px(x, int(bot) + 1, LIP)
        F.px(x, int(top) - 1, mix(SKIN_D, LIP, 0.4))
    # teeth: upper row pointing down, lower row pointing up
    for i in range(10):
        x0 = 4 + i * 4
        u = (x0 + 2 - cx) / (cx - 3)
        top = 30 - 2.2 * (1 - u * u) - 6 * u * u
        bot = 42 - 13 * u * u
        span = bot - top
        if span < 3: continue
        th = min(5.5, span * 0.48)
        F.poly([(x0, top), (x0 + 4, top), (x0 + 2, top + th)], TEETH)
        F.poly([(x0 + 2, bot + 1), (x0 + 6, bot + 1), (x0 + 4, bot + 1 - th)], TEETH)
    for x in range(W):  # cheek dimples
        pass
    F.px(4, 22, SKIN_D); F.px(W - 5, 22, SKIN_D)


def flame_paint(c1, c2):
    def f(F):
        for y in range(F.h):
            for x in range(F.w):
                t = y / max(1, F.h - 1)
                c = mix(c1, c2, t)
                if R.random() < 0.15: c = mix(c, 0xFFFFFF, 0.25)
                F.px(x, y, c, glow=True)
    return f


# ------------------------------------------------------------------ skeleton
m.group("root", (0, 0, 0))
m.group("body", (0, 15.5, 0), parent="root")
m.group("chest", (0, 18, 0), parent="body")
m.group("poncho", (0, 26.4, 0), parent="chest")
m.group("poncho_f", (0, 23.6, -2.4), parent="poncho")
m.group("fringe_f", (0, 20.2, -2.5), parent="poncho_f")
m.group("poncho_b", (0, 23.6, 2.4), parent="poncho")
m.group("fringe_b", (0, 17.6, 2.6), parent="poncho_b")
m.group("head", (0, 27.4, 0), parent="chest")
m.group("hat", (0, 33, 0), parent="head")
m.group("ear_r", (2.0, 35.0, 0.2), parent="hat")
m.group("ear_l", (-2.0, 35.0, 0.2), parent="hat")
m.group("hair_b1", (0, 31.5, 3.0), parent="head")
m.group("hair_b2", (0, 21.0, 3.8), parent="hair_b1")
m.group("hair_b3", (0, 11.5, 4.4), parent="hair_b2")
m.group("hair_r1", (3.3, 31.5, 0.3), parent="head")
m.group("hair_r2", (4.3, 22.0, 0.8), parent="hair_r1")
m.group("hair_l1", (-3.3, 31.5, 0.3), parent="head")
m.group("hair_l2", (-4.3, 22.0, 0.8), parent="hair_l1")
m.group("arm_r", (3.95, 25.6, 0), parent="chest")
m.group("fore_r", (4.0, 21.4, 0), parent="arm_r")
m.group("band_tail", (4.9, 19.5, 0.6), parent="fore_r")
m.group("hand_r", (4.0, 16.9, 0), parent="fore_r")
m.group("claws_r", (4.0, 15.0, -0.2), parent="hand_r")
m.group("bottle", (4.0, 15.0, -0.4), parent="hand_r")
m.group("arm_l", (-3.95, 25.6, 0), parent="chest")
m.group("fore_l", (-4.0, 21.4, 0), parent="arm_l")
m.group("hand_l", (-4.0, 16.9, 0), parent="fore_l")
m.group("gun", (-4.0, 15.6, 0), parent="hand_l")
m.group("flame", (-4.0, 2.2, 0), parent="gun")
m.group("tail1", (0, 16.6, 2.0), parent="body")
m.group("tail2", (0, 9.5, 2.6), parent="tail1")
for s, k in ((1, "r"), (-1, "l")):
    m.group("leg_" + k, (1.6 * s, 15.5, 0), parent="root")
    m.group("shin_" + k, (1.6 * s, 8.8, 0), parent="leg_" + k)
    m.group("foot_" + k, (1.6 * s, 1.3, 0), parent="shin_" + k)

# ------------------------------------------------------------------ legs: baggy peach trousers + strapped pointy boots
for s, k in ((1, "r"), (-1, "l")):
    x = 1.6 * s
    m.cube("thigh_" + k, "leg_" + k, (x - 1.55, 8.6, -1.6), (x + 1.55, 15.6, 1.6), PANT, color2=PANT_D, grad=True,
           faces={"north": cloth_folds(PANT, PANT_D, PANT_L, 2), "south": cloth_folds(PANT, PANT_D, PANT_L, 2)})
    m.cube("knee_" + k, "shin_" + k, (x - 1.7, 6.6, -1.75), (x + 1.7, 8.9, 1.7), PANT_D, color2=PANT, grad=True)
    m.cube("boot_" + k, "shin_" + k, (x - 1.45, 1.0, -1.55), (x + 1.45, 6.8, 1.5), BOOT, color2=BOOT_L, grad=True,
           faces={"north": combo(lambda F: F.rect(F.w // 2 - 1, 2, 2, F.h - 4, BOOT_L))})
    m.cube("cuff_" + k, "shin_" + k, (x - 1.8, 6.0, -1.85), (x + 1.8, 7.6, 1.8), BOOT_L,
           faces={"north": lambda F: [F.poly([(i, F.h), (i + 3, F.h), (i + 1.5, 0)], BOOT) for i in range(0, F.w, 3)]})
    for j, y in enumerate((4.6, 2.6)):
        m.cube(f"strap{j}_" + k, "shin_" + k, (x - 1.6, y, -1.7), (x + 1.6, y + 0.65, 1.65), STRAP, color2=STRAP_D, grad=True)
        m.cube(f"buckle{j}_" + k, "shin_" + k, (x + 0.5 * s - 0.4, y - 0.1, -1.85), (x + 0.5 * s + 0.4, y + 0.75, -1.6), STEEL_L)
    m.cube("sole_" + k, "foot_" + k, (x - 1.55, 0, -3.3), (x + 1.55, 1.4, 1.6), BOOT, faces={"down": lambda F: F.rect(0, 0, F.w, F.h, 0x0C0B10)})
    m.cube("toe_" + k, "foot_" + k, (x - 1.0, 0, -5.0), (x + 1.0, 1.0, -3.2), BOOT, origin=(x, 0, -3.2), rot=(-8, 0, 0))
    m.cube("heel_" + k, "foot_" + k, (x - 0.7, -0.01, 0.4), (x + 0.7, 0.9, 1.5), BOOT_L)

# ------------------------------------------------------------------ hips / belt / pouch / back cloth
m.cube("hips", "body", (-3.0, 14.4, -1.75), (3.0, 17.6, 1.75), PANT, color2=PANT_D, grad=True)
m.cube("belt", "body", (-3.1, 16.8, -1.85), (3.1, 17.7, 1.85), TANK_D, faces={"north": lambda F: F.rect(F.w // 2 - 3, 0, 6, F.h, STEEL_L)})
m.cube("pouch", "body", (-4.3, 13.6, -1.3), (-2.9, 16.6, 1.0), PON_D, color2=STRAP_D, grad=True,
       faces={"west": combo(frame(STRAP_D), lambda F: F.rect(0, 0, F.w, 5, PON))})
m.cube("canister", "body", (-3.4, 13.2, 1.0), (-1.4, 17.0, 2.9), TANK, color2=TANK_D, grad=True,
       faces={"south": combo(hstripe(STRAP, 6, 3), hstripe(STRAP, 22, 3))})
m.cube("canister_cap", "body", (-2.8, 17.0, 1.5), (-2.0, 17.7, 2.3), STEEL_L)
m.cube("tail_top", "tail1", (-2.4, 9.6, 1.7), (2.4, 16.8, 2.4), TOP_D, color2=HAT, grad=True, faces={"south": cloth_folds(TOP_D, HAT, TOP_L, 3)})
m.cube("tail_bot", "tail2", (-2.0, 3.2, 2.0), (2.0, 9.8, 2.6), HAT, color2=TOP_D, grad=True,
       faces={"south": lambda F: [F.poly([(i, F.h), (i + 6, F.h), (i + 3, F.h - 9)], (0, 0, 0, 0)) for i in range(0, F.w, 6)]})
m.cube("tail_tip", "tail2", (-1.0, 0.8, 2.1), (1.0, 3.4, 2.5), HAT, origin=(0, 3.4, 2.3), rot=(-6, 0, 0))

# ------------------------------------------------------------------ torso
m.cube("waist", "chest", (-2.5, 17.5, -1.5), (2.5, 21.0, 1.5), TOP_D, color2=TOP, grad=True)
m.cube("torso", "chest", (-2.9, 20.8, -1.7), (2.9, 26.0, 1.7), TOP, color2=TOP_D, grad=True,
       faces={"north": cloth_folds(TOP, TOP_D, TOP_L, 3)})
m.cube("neck", "chest", (-1.0, 25.8, -0.9), (1.0, 27.6, 0.9), SKIN_D, color2=SKIN, grad=True)
# poncho mantle + panels (+ fringe)
m.cube("mantle", "poncho", (-3.6, 23.3, -2.35), (3.6, 26.9, 2.35), PON, color2=PON_D, grad=True,
       faces={"up": lambda F: F.rect(F.w // 2 - 6, F.h // 2 - 5, 12, 10, PON_D), "north": cloth_folds(PON, PON_D, PON_L, 4)})
m.cube("collar", "poncho", (-1.7, 26.2, -1.5), (1.7, 27.5, 1.4), PON_D, color2=PON, grad=True)
m.cube("pf_a", "poncho_f", (-3.5, 20.8, -2.75), (3.5, 23.8, -2.1), PON, color2=PON_D, grad=True,
       origin=(0, 23.6, -2.4), rot=(6, 0, -4), faces={"north": cloth_folds(PON, PON_D, PON_L, 4)})
m.cube("pf_b", "poncho_f", (-2.7, 20.0, -2.95), (2.3, 21.0, -2.3), PON, color2=PON_D, grad=True,
       origin=(0, 21, -2.6), rot=(8, 0, -6), faces={"north": cloth_folds(PON, PON_D, PON_L, 3)})
m.cube("pb_a", "poncho_b", (-3.6, 19.5, 2.1), (3.6, 23.8, 2.75), PON, color2=PON_D, grad=True,
       origin=(0, 23.6, 2.4), rot=(-6, 0, 0), faces={"south": cloth_folds(PON, PON_D, PON_L, 4)})
m.cube("pb_b", "poncho_b", (-2.8, 17.6, 2.3), (2.8, 19.7, 2.95), PON, color2=PON_D, grad=True,
       origin=(0, 19.7, 2.6), rot=(-8, 0, 0))
for i in range(9):  # front fringe
    x = -2.8 + i * 0.62
    ln = 1.7 + (i % 2) * 0.5
    y0 = 20.2 if abs(x) < 2.4 else 20.9
    m.cube(f"ff{i}", "fringe_f", (x, y0 - ln, -3.0), (x + 0.38, y0, -2.6), PON, color2=PON_D, grad=True,
           origin=(x + 0.2, y0, -2.8), rot=(4 + R.uniform(-3, 3), 0, R.uniform(-5, 5)))
for i in range(10):  # back fringe
    x = -2.9 + i * 0.62
    ln = 1.8 + (i % 2) * 0.6
    m.cube(f"fb{i}", "fringe_b", (x, 17.7 - ln, 2.55), (x + 0.38, 17.7, 2.95), PON, color2=PON_D, grad=True,
           origin=(x + 0.2, 17.7, 2.75), rot=(-4 + R.uniform(-3, 3), 0, R.uniform(-5, 5)))

# ------------------------------------------------------------------ head: grin, orange band over the eyes, wolf-ear hat
m.cube("skull", "head", (-3.0, 27.4, -3.0), (3.0, 33.4, 3.0), SKIN, faces={"north": face_front, "up": lambda F: F.rect(0, 0, F.w, F.h, HAIR_D)})
m.cube("band", "head", (-3.2, 30.5, -3.2), (3.2, 32.6, 3.2), BAND, color2=BAND_D, grad=True,
       faces={"north": lambda F: F.rect(0, F.h - 2, F.w, 2, BAND_D)})
m.cube("hat_cap", "hat", (-3.35, 32.4, -3.35), (3.35, 35.0, 3.35), HAT, color2=HAT_L, grad=True,
       faces={"north": lambda F: F.rect(0, 0, F.w, 2, HAT_L)})
m.cube("hat_top", "hat", (-2.8, 35.0, -2.8), (2.8, 35.8, 2.8), HAT)
m.cube("hat_brim", "hat", (-3.4, 32.1, -4.2), (3.4, 32.7, -3.2), HAT, origin=(0, 32.4, -3.2), rot=(-12, 0, 0))
for s, k in ((1, "r"), (-1, "l")):
    ex = 2.0 * s
    m.cube("earb_" + k, "ear_" + k, (ex - 1.2, 35.0, -0.8), (ex + 1.2, 37.8, 1.1), HAT, origin=(ex, 35.0, 0.2), rot=(0, 0, -10 * s),
           faces={"north": lambda F: F.poly([(2, F.h), (F.w - 2, F.h), (F.w / 2, 3)], 0x3A3046)})
    m.cube("eart_" + k, "ear_" + k, (ex - 0.7, 37.4, -0.5), (ex + 0.7, 40.2, 0.8), HAT, origin=(ex, 37.6, 0.2), rot=(0, 0, -20 * s))
    m.cube("earp_" + k, "ear_" + k, (ex - 0.3, 39.9, -0.25), (ex + 0.3, 41.2, 0.5), HAT, origin=(ex, 40.0, 0.2), rot=(0, 0, -30 * s))
# hair mass under the hat, bangs framing the face
m.cube("hair_crown", "head", (-3.6, 27.6, 0.2), (3.6, 33.6, 3.9), HAIR, faces=all_faces(strands(HAIR, HAIR_HI, HAIR_D)))
for i, (x, y0, ln, rz) in enumerate([(2.6, 32.6, 5.8, 6), (1.9, 32.4, 3.2, 2), (-2.6, 32.6, 6.4, -6), (-1.7, 32.4, 2.6, -3), (0.6, 32.5, 2.2, 10)]):
    m.cube(f"bang{i}", "head", (x - 0.5, y0 - ln, -3.45), (x + 0.5, y0, -2.9), HAIR, origin=(x, y0, -3.2), rot=(4, 0, rz),
           faces=all_faces(strands(HAIR, HAIR_HI, HAIR_D, 2)))
m.cube("hb_main", "hair_b1", (-4.2, 20.6, 2.0), (4.2, 31.8, 4.8), HAIR, faces=all_faces(strands(HAIR, HAIR_HI, HAIR_D)))
m.cube("hb_lower", "hair_b2", (-4.7, 11.2, 2.4), (4.7, 21.2, 5.2), HAIR, color2=HAIR_D, grad=True, faces=all_faces(strands(HAIR, HAIR_HI, HAIR_D)))
for i in range(9):  # long jagged tips down to the boots
    x = -4.2 + i * 1.05
    ln = 4.5 + (i % 3) * 2.2 + R.uniform(0, 1.2)
    m.cube(f"hb_tip{i}", "hair_b3", (x - 0.55, 11.6 - ln, 2.9 + (i % 2) * 0.3), (x + 0.55, 11.6, 4.5 + (i % 2) * 0.3), HAIR if i % 2 else HAIR_D,
           origin=(x, 11.6, 3.8), rot=(-6 - (i % 3) * 4, 0, (i - 4) * 4.5), faces=all_faces(strands(HAIR, HAIR_HI, HAIR_D, 2)))
for s, k in ((1, "r"), (-1, "l")):
    m.cube("hs_main_" + k, "hair_" + k + "1", (3.55 * s - 0.75, 21.5, -2.3), (3.55 * s + 0.75, 31.6, 2.6),
           HAIR, faces=all_faces(strands(HAIR, HAIR_HI, HAIR_D)))
    for i in range(5):  # flared spiky locks fanning outward (big silhouette of the reference)
        z = -1.6 + i * 1.0
        ln = 8.5 + (i % 2) * 3.2 + R.uniform(0, 1.5)
        m.cube(f"hs_lock{i}_" + k, "hair_" + k + "2", (4.2 * s - 0.55, 22.4 - ln, z - 0.5), (4.2 * s + 0.55, 22.4, z + 0.5),
               HAIR if i % 2 else HAIR_HI if i == 2 else HAIR_D, origin=(4.2 * s, 22.4, z), rot=(-4 - i * 3, 0, (20 + i * 5) * s),
               faces=all_faces(strands(HAIR, HAIR_HI, HAIR_D, 2)))
    for i in range(3):  # volume puffs at cheek height
        m.cube(f"hs_puff{i}_" + k, "hair_" + k + "1", (4.0 * s - 0.6, 24.5 - i * 1.5, -1.8 + i * 1.4), (4.0 * s + 0.6, 30.5 - i * 1.2, -0.6 + i * 1.4),
               HAIR_HI if i == 1 else HAIR, origin=(4.0 * s, 30.5, 0), rot=(0, 0, (12 + i * 6) * s), faces=all_faces(strands(HAIR, HAIR_HI, HAIR_D, 2)))
    for i in range(3):  # wild flicks
        ln = 4 + i
        m.cube(f"hs_flick{i}_" + k, "hair_" + k + "2", (4.6 * s - 0.4, 16 - i * 3 - ln, -0.4 + i * 0.6), (4.6 * s + 0.4, 16 - i * 3, 0.4 + i * 0.6),
               HAIR_D, origin=(4.6 * s, 16 - i * 3, i * 0.6), rot=(-6, 0, (16 + i * 6) * s))

# ------------------------------------------------------------------ right arm: bandaged forearm + black claw glove
m.cube("sleeve_r", "arm_r", (3.0, 21.3, -1.05), (4.95, 25.9, 1.05), TOP, color2=TOP_D, grad=True)
m.cube("shoulder_r", "arm_r", (2.8, 23.9, -1.45), (5.25, 26.6, 1.45), PON, color2=PON_D, grad=True, origin=(3.95, 25.6, 0), rot=(0, 0, 8))
m.cube("forearm_r", "fore_r", (3.08, 17.6, -0.98), (4.92, 21.5, 0.98), BANDAGE, faces=all_faces(bandage))
m.cube("bt0", "band_tail", (4.75, 17.0, 0.4), (5.05, 19.6, 0.9), BANDAGE, origin=(4.9, 19.6, 0.6), rot=(-14, 0, 18))
m.cube("glove_r", "fore_r", (2.95, 16.6, -1.12), (5.05, 18.1, 1.12), GLOVE, faces=all_faces(hstripe(STRAP, 3, 3)))
m.cube("palm_r", "hand_r", (3.1, 14.9, -1.05), (4.9, 16.9, 1.05), GLOVE, color2=GLOVE_L, grad=True)
m.cube("thumb_r", "hand_r", (3.0, 14.2, -1.3), (3.5, 16.2, -0.7), GLOVE, origin=(3.2, 16.2, -1), rot=(18, 0, 22))
for i in range(4):
    x = 3.15 + i * 0.45
    m.cube(f"finger{i}_r", "claws_r", (x, 12.6, -0.75), (x + 0.38, 15.0, -0.3), GLOVE, origin=(x + 0.19, 15.0, -0.5), rot=(8, 0, (i - 1.5) * -3))
    m.cube(f"claw{i}_r", "claws_r", (x + 0.04, 10.0, -0.72), (x + 0.36, 12.8, -0.34), CLAW, color2=CLAW_L, grad=True,
           origin=(x + 0.19, 12.8, -0.5), rot=(18, 0, (i - 1.5) * -4))
# molotov bottle (only shown during "molotov")
m.cube("bottle_body", "bottle", (3.4, 11.8, -1.0), (4.6, 14.4, 0.2), 0x8A4A1A, color2=0x5A2A0A, grad=True)
m.cube("bottle_neck", "bottle", (3.75, 14.4, -0.65), (4.25, 15.8, -0.15), 0x6A3A12)
m.cube("bottle_rag", "bottle", (3.7, 15.8, -0.7), (4.3, 16.8, -0.1), F_MID, glow=True)

# ------------------------------------------------------------------ left arm + FLAMETHROWER
m.cube("sleeve_l", "arm_l", (-4.95, 21.3, -1.05), (-3.0, 25.9, 1.05), TOP, color2=TOP_D, grad=True)
m.cube("shoulder_l", "arm_l", (-5.25, 23.9, -1.45), (-2.8, 26.6, 1.45), PON, color2=PON_D, grad=True, origin=(-3.95, 25.6, 0), rot=(0, 0, -8))
m.cube("forearm_l", "fore_l", (-4.92, 17.6, -0.98), (-3.08, 21.5, 0.98), TOP, color2=TOP_D, grad=True)
m.cube("glove_l", "fore_l", (-5.05, 16.6, -1.12), (-2.95, 18.1, 1.12), GLOVE, faces=all_faces(hstripe(STRAP, 3, 3)))
m.cube("palm_l", "hand_l", (-4.9, 14.9, -1.05), (-3.1, 16.9, 1.05), GLOVE, color2=GLOVE_L, grad=True)
m.cube("gun_grip", "gun", (-4.4, 14.0, -0.4), (-3.6, 16.6, 0.4), STEEL_D)
m.cube("gun_body", "gun", (-4.9, 9.2, -1.25), (-3.1, 14.2, 1.0), STEEL, color2=STEEL_D, grad=True,
       faces={"west": combo(hstripe(STRAP, 8, 4), frame(STEEL_D)), "east": combo(hstripe(STRAP, 8, 4), frame(STEEL_D)), "north": frame(STEEL_L)})
m.cube("gun_tank", "gun", (-5.0, 10.0, 0.9), (-3.0, 13.8, 2.6), TANK, color2=TANK_D, grad=True, faces={"south": hstripe(STRAP, 10, 3)})
m.cube("gun_valve", "gun", (-4.3, 13.8, 1.4), (-3.7, 14.6, 2.0), STEEL_L)
m.cube("gun_trigger", "gun", (-4.15, 13.0, -1.7), (-3.85, 14.2, -1.2), STEEL_D)
m.cube("gun_barrel", "gun", (-4.42, 3.4, -0.42), (-3.58, 9.4, 0.42), STEEL, color2=STEEL_L, grad=True)
m.cube("gun_shroud", "gun", (-4.65, 5.0, -0.65), (-3.35, 8.6, 0.65), STEEL_D, faces=all_faces(lambda F: [F.rect(0, y, F.w, 2, STEEL) for y in range(1, F.h, 5)]))
m.cube("gun_fgrip", "gun", (-4.3, 7.0, -1.9), (-3.7, 8.4, -0.6), TANK_D, origin=(-4, 8.4, -0.6), rot=(-20, 0, 0))
m.cube("gun_nozzle", "gun", (-4.7, 2.2, -0.7), (-3.3, 3.6, 0.7), STEEL_D, faces={"down": lambda F: F.disc(F.w / 2, F.h / 2, F.w / 3, 0xFF8A20, glow=True)})
m.cube("gun_pilot", "gun", (-4.2, 2.6, -1.05), (-3.8, 3.0, -0.7), 0x8AD0FF, glow=True)
m.cube("gun_hose", "gun", (-4.2, 9.4, 1.6), (-3.8, 10.2, 2.0), STEEL_D)
# flame jet (scaled 0 unless an animation turns it on)
m.cube("fl_core", "flame", (-4.35, -4.0, -0.35), (-3.65, 2.2, 0.35), F_CORE, glow=True, paint=lambda fs: [flame_paint(F_CORE, F_MID)(f) for f in fs.values()])
m.cube("fl_mid", "flame", (-4.8, -7.0, -0.8), (-3.2, 1.6, 0.8), F_MID, glow=True, origin=(-4, 2.2, 0), rot=(0, 45, 0),
       paint=lambda fs: [flame_paint(F_MID, F_OUT)(f) for f in fs.values()])
m.cube("fl_out", "flame", (-5.3, -10.5, -1.3), (-2.7, -2.0, 1.3), F_OUT, glow=True, paint=lambda fs: [flame_paint(F_MID, F_TIP)(f) for f in fs.values()])
m.cube("fl_tip1", "flame", (-5.0, -13.5, -0.6), (-3.6, -9.0, 0.8), F_TIP, glow=True, origin=(-4, -9, 0), rot=(12, 20, 14),
       paint=lambda fs: [flame_paint(F_OUT, F_TIP)(f) for f in fs.values()])
m.cube("fl_tip2", "flame", (-4.4, -12.5, -0.9), (-3.0, -8.5, 0.5), F_TIP, glow=True, origin=(-4, -8.5, 0), rot=(-10, -25, -16),
       paint=lambda fs: [flame_paint(F_OUT, F_TIP)(f) for f in fs.values()])


# ================================================================== animation
class A:
    """ticks-based keyframe author. tracks: bone -> channel -> [(tick, x, y, z)]"""
    def __init__(self, name, ticks, loop=False):
        self.name, self.ticks, self.loop, self.tr = name, ticks, loop, {}

    def k(self, bone, ch, keys):
        self.tr.setdefault(bone, {}).setdefault(ch, []).extend(keys)
        return self

    def rot(self, bone, *keys): return self.k(bone, "rotation", keys)
    def pos(self, bone, *keys): return self.k(bone, "position", keys)
    def scl(self, bone, *keys): return self.k(bone, "scale", keys)

    def drape(self, chain, keys, delay=2, gain=0.8):
        """secondary motion: the first bone gets `keys`, every next one the same keys delayed + damped (+ settles)."""
        g = 1.0
        for i, b in enumerate(chain):
            d = delay * i
            ks = [(min(self.ticks, t + d), x * g, y * g, z * g) for (t, x, y, z) in keys]
            # de-duplicate clamped times
            seen, out = set(), []
            for kk in ks:
                if kk[0] in seen: continue
                seen.add(kk[0]); out.append(kk)
            self.rot(b, *out)
            g *= gain
        return self

    def done(self, flame=None, bottle=None):
        if "flame" not in self.tr:
            self.scl("flame", *(flame or [(0, 0.001, 0.001, 0.001)]))
        if "bottle" not in self.tr:
            self.scl("bottle", *(bottle or [(0, 0.001, 0.001, 0.001)]))
        tracks = {}
        for b, chs in self.tr.items():
            tracks[b] = {ch: sorted([(t / 20.0, x, y, z) for (t, x, y, z) in v], key=lambda q: q[0]) for ch, v in chs.items()}
        m.anim(self.name, self.ticks / 20.0, tracks, loop=self.loop)


def flame_on(t0, t1, size=1.0, flick=2, grow=2, shrink=2):
    """scale keys for the flame jet: grows at t0, flickers, dies at t1"""
    ks = [(0, .001, .001, .001), (max(0, t0 - 0.5), .001, .001, .001), (t0 + grow, size, size * 1.1, size)]
    t, i = t0 + grow, 0
    while t + flick < t1:
        t += flick; i += 1
        f = size * (1.12 if i % 2 else 0.92)
        ks.append((t, f * 0.95, f * 1.15 if i % 2 else f, f * 0.95))
    ks += [(t1, size * 0.7, size * 0.5, size * 0.7), (t1 + shrink, .001, .001, .001)]
    return ks


HAIR_B = ["hair_b1", "hair_b2", "hair_b3"]
HAIR_R, HAIR_L = ["hair_r1", "hair_r2"], ["hair_l1", "hair_l2"]
CLOTH = ["poncho_f", "fringe_f"]
CLOTH_B = ["poncho_b", "fringe_b"]
TAIL = ["tail1", "tail2"]

# ------------------------------------------------------------------ idle (4 s loop): slouched, grinning, gun dangling, breathing
a = A("idle", 80, loop=True)
a.rot("chest", (0, -3, 0, 0), (20, -1.5, 1.5, 0), (40, -3, 0, 0), (60, -1.5, -1.5, 0), (80, -3, 0, 0))
a.rot("head", (0, 4, 0, 3), (20, 5, 2, 1), (40, 4, 0, -2), (60, 5, -2, 1), (80, 4, 0, 3))
a.pos("body", (0, 0, 0, 0), (20, 0, -0.15, 0), (40, 0, 0, 0), (60, 0, -0.15, 0), (80, 0, 0, 0))
a.rot("arm_r", (0, 3, 0, 6), (40, 5, 0, 8), (80, 3, 0, 6))
a.rot("fore_r", (0, 12, 0, 0), (40, 16, 0, 0), (80, 12, 0, 0))
a.rot("claws_r", (0, 20, 0, 0), (30, 26, 0, 0), (36, 10, 0, 0), (44, 26, 0, 0), (80, 20, 0, 0))
a.rot("arm_l", (0, 6, 0, -8), (40, 8, 0, -10), (80, 6, 0, -8))
a.rot("fore_l", (0, 16, 0, 0), (40, 20, 0, 0), (80, 16, 0, 0))
a.rot("hand_l", (0, 20, 0, 0), (40, 24, 0, 0), (80, 20, 0, 0))
a.rot("ear_r", (0, 0, 0, 0), (50, 0, 0, 0), (53, 0, 0, -14), (57, 0, 0, 0), (80, 0, 0, 0))
a.rot("ear_l", (0, 0, 0, 0), (52, 0, 0, 0), (55, 0, 0, 14), (59, 0, 0, 0), (80, 0, 0, 0))
a.drape(HAIR_B, [(0, -3, 0, 1), (20, -5, 0, 0), (40, -3, 0, -1), (60, -5, 0, 0), (80, -3, 0, 1)], delay=4, gain=0.9)
a.drape(HAIR_R, [(0, 0, 0, 3), (30, 0, 0, 5), (55, 0, 0, 2), (80, 0, 0, 3)], delay=4)
a.drape(HAIR_L, [(0, 0, 0, -3), (25, 0, 0, -5), (50, 0, 0, -2), (80, 0, 0, -3)], delay=4)
a.drape(CLOTH, [(0, 0, 0, 0), (20, 2, 0, 1), (40, 0, 0, 0), (60, 2, 0, -1), (80, 0, 0, 0)], delay=4)
a.drape(CLOTH_B, [(0, -1, 0, 0), (30, -3, 0, 0), (80, -1, 0, 0)], delay=4)
a.drape(TAIL, [(0, -4, 0, 0), (40, -7, 0, 2), (80, -4, 0, 0)], delay=6)
a.rot("band_tail", (0, 0, 0, 0), (25, -10, 0, 8), (55, 6, 0, -4), (80, 0, 0, 0))
a.done()

# ------------------------------------------------------------------ walk (one stride): loose predatory prowl, gun swinging
a = A("walk", 20, loop=True)
a.rot("leg_r", (0, 30, 0, 0), (5, 0, 0, 0), (10, -26, 0, 0), (15, 0, 0, 0), (20, 30, 0, 0))
a.rot("shin_r", (0, -6, 0, 0), (5, -12, 0, 0), (10, -10, 0, 0), (13, -50, 0, 0), (17, -28, 0, 0), (20, -6, 0, 0))
a.rot("foot_r", (0, -10, 0, 0), (5, 0, 0, 0), (10, 10, 0, 0), (15, 6, 0, 0), (20, -10, 0, 0))
a.rot("leg_l", (0, -26, 0, 0), (5, 0, 0, 0), (10, 30, 0, 0), (15, 0, 0, 0), (20, -26, 0, 0))
a.rot("shin_l", (0, -10, 0, 0), (3, -50, 0, 0), (7, -28, 0, 0), (10, -6, 0, 0), (15, -12, 0, 0), (20, -10, 0, 0))
a.rot("foot_l", (0, 10, 0, 0), (5, 6, 0, 0), (10, -10, 0, 0), (15, 0, 0, 0), (20, 10, 0, 0))
a.pos("body", (0, 0, -0.3, 0), (5, 0, 0.5, 0), (10, 0, -0.3, 0), (15, 0, 0.5, 0), (20, 0, -0.3, 0))
a.rot("body", (0, -6, 6, 0), (10, -6, -6, 0), (20, -6, 6, 0))
a.rot("chest", (0, -4, -4, 2), (10, -4, 4, -2), (20, -4, -4, 2))
a.rot("arm_r", (0, -22, 0, 8), (10, 26, 0, 6), (20, -22, 0, 8))
a.rot("fore_r", (0, 8, 0, 0), (10, 30, 0, 0), (20, 8, 0, 0))
a.rot("arm_l", (0, 18, 0, -8), (10, -12, 0, -10), (20, 18, 0, -8))
a.rot("fore_l", (0, 22, 0, 0), (10, 12, 0, 0), (20, 22, 0, 0))
a.drape(HAIR_B, [(0, -10, 2, 2), (5, -14, 0, 0), (10, -10, -2, -2), (15, -14, 0, 0), (20, -10, 2, 2)], delay=2, gain=0.9)
a.drape(HAIR_R, [(0, -6, 0, 6), (10, -8, 0, 2), (20, -6, 0, 6)], delay=2)
a.drape(HAIR_L, [(0, -8, 0, -2), (10, -6, 0, -6), (20, -8, 0, -2)], delay=2)
a.drape(CLOTH, [(0, 4, 0, 2), (5, 8, 0, 0), (10, 4, 0, -2), (15, 8, 0, 0), (20, 4, 0, 2)], delay=2)
a.drape(CLOTH_B, [(0, -6, 0, 0), (5, -10, 0, 0), (10, -6, 0, 0), (15, -10, 0, 0), (20, -6, 0, 0)], delay=2)
a.drape(TAIL, [(0, -14, 0, 4), (10, -14, 0, -4), (20, -14, 0, 4)], delay=3)
a.done()

# ------------------------------------------------------------------ flame_stream (58): pump - spray sweeping 14..46 - recover
a = A("flame_stream", 58)
a.pos("body", (0, 0, 0, 0), (8, 0, -1.2, 0.4), (14, 0, -0.8, 0.6), (46, 0, -0.8, 0.6), (58, 0, 0, 0))
a.rot("body", (0, 0, 0, 0), (8, -4, -18, 0), (14, -8, 22, 0), (22, -8, -24, 0), (30, -8, 26, 0), (38, -8, -26, 0), (46, -8, 18, 0), (52, -2, 6, 0), (58, 0, 0, 0))
a.rot("chest", (0, 0, 0, 0), (8, 6, 0, 0), (12, -4, 0, 0), (14, -2, 0, 0), (46, -2, 0, 0), (58, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (8, -6, 0, 0), (14, 4, -10, 0), (22, 6, 12, 0), (30, 4, -12, 0), (38, 6, 12, 0), (46, 4, 0, 0), (58, 0, 0, 0))
a.rot("arm_l", (0, 6, 0, -8), (8, 40, 0, -6), (12, 80, 0, -4), (14, 86, 0, 0), (46, 86, 0, 0), (52, 30, 0, -8), (58, 6, 0, -8))
a.rot("fore_l", (0, 16, 0, 0), (8, 30, 0, 0), (14, 6, 0, 0), (17, 2, 0, 0), (46, 4, 0, 0), (58, 16, 0, 0))
a.rot("hand_l", (0, 20, 0, 0), (12, 0, 0, 0), (46, 0, 0, 0), (58, 20, 0, 0))
a.rot("arm_r", (0, 3, 0, 6), (8, 50, 30, -20), (14, 60, 40, -30), (46, 60, 40, -30), (52, 20, 0, 6), (58, 3, 0, 6))  # claw braces the barrel
a.rot("fore_r", (0, 12, 0, 0), (14, 40, 0, 0), (46, 40, 0, 0), (58, 12, 0, 0))
a.rot("leg_r", (0, 0, 0, 0), (8, 20, 0, 4), (14, 26, 0, 6), (46, 26, 0, 6), (58, 0, 0, 0))
a.rot("shin_r", (0, 0, 0, 0), (8, -20, 0, 0), (14, -24, 0, 0), (46, -24, 0, 0), (58, 0, 0, 0))
a.rot("leg_l", (0, 0, 0, 0), (8, -18, 0, -4), (14, -20, 0, -6), (46, -20, 0, -6), (58, 0, 0, 0))
a.rot("shin_l", (0, 0, 0, 0), (14, -10, 0, 0), (46, -10, 0, 0), (58, 0, 0, 0))
a.drape(HAIR_B, [(0, -3, 0, 0), (14, -16, -10, -8), (22, -22, 12, 10), (30, -22, -12, -10), (38, -22, 12, 10), (46, -18, -8, -6), (58, -3, 0, 0)], delay=3)
a.drape(HAIR_R, [(0, 0, 0, 3), (14, -10, 0, 16), (30, -12, 0, 6), (46, -10, 0, 16), (58, 0, 0, 3)], delay=3)
a.drape(HAIR_L, [(0, 0, 0, -3), (14, -10, 0, -6), (30, -12, 0, -16), (46, -10, 0, -6), (58, 0, 0, -3)], delay=3)
a.drape(CLOTH, [(0, 0, 0, 0), (14, 8, 0, 6), (22, 10, 0, -8), (30, 10, 0, 8), (38, 10, 0, -8), (46, 6, 0, 0), (58, 0, 0, 0)], delay=2)
a.drape(TAIL, [(0, -4, 0, 0), (14, -20, 0, 10), (30, -24, 0, -10), (46, -20, 0, 10), (58, -4, 0, 0)], delay=4)
a.rot("band_tail", (0, 0, 0, 0), (16, -40, 0, 20), (30, -30, 0, 30), (46, -40, 0, 20), (58, 0, 0, 0))
a.scl("flame", *flame_on(13, 46, 1.4))
a.done()

# ------------------------------------------------------------------ fireball (34): cock back - aim - BOOM on 15 (+19, 23 rage) - recover
a = A("fireball", 34)
a.rot("body", (0, 0, 0, 0), (8, 6, -30, 0), (13, -4, 6, 0), (15, -2, 10, 0), (18, 10, 4, 0), (23, 6, 6, 0), (34, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (8, 0, -0.8, 1), (13, 0, -1.2, -0.6), (16, 0, -0.6, 1.2), (34, 0, 0, 0))
a.rot("chest", (0, 0, 0, 0), (8, 8, -10, 0), (13, -6, 0, 0), (15, -4, 0, 0), (17, 10, 0, 0), (21, 4, 0, 0), (34, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (8, -4, 20, 0), (13, 2, 0, 0), (16, 12, 0, 6), (20, 8, 0, 0), (34, 0, 0, 0))
a.rot("arm_l", (0, 6, 0, -8), (8, 40, -30, -30), (13, 92, 0, 0), (15, 90, 0, 0), (16, 106, 0, 0), (19, 92, 0, 0), (20, 102, 0, 0), (23, 92, 0, 0),
      (24, 100, 0, 0), (28, 70, 0, -4), (34, 6, 0, -8))
a.rot("fore_l", (0, 16, 0, 0), (8, 60, 0, 0), (13, 2, 0, 0), (16, 10, 0, 0), (34, 16, 0, 0))
a.rot("hand_l", (0, 20, 0, 0), (13, 0, 0, 0), (28, 0, 0, 0), (34, 20, 0, 0))
a.rot("arm_r", (0, 3, 0, 6), (8, -30, 0, 24), (13, 20, 0, 10), (16, -20, 0, 30), (34, 3, 0, 6))
a.rot("fore_r", (0, 12, 0, 0), (8, 50, 0, 0), (16, 40, 0, 0), (34, 12, 0, 0))
a.rot("claws_r", (0, 20, 0, 0), (8, 40, 0, 0), (16, -10, 0, 0), (34, 20, 0, 0))
a.rot("leg_r", (0, 0, 0, 0), (8, -10, 0, 0), (13, 24, 0, 4), (34, 0, 0, 0))
a.rot("shin_r", (0, 0, 0, 0), (13, -16, 0, 0), (34, 0, 0, 0))
a.rot("leg_l", (0, 0, 0, 0), (8, 12, 0, 0), (13, -22, 0, -4), (34, 0, 0, 0))
a.rot("shin_l", (0, 0, 0, 0), (8, -18, 0, 0), (13, -8, 0, 0), (34, 0, 0, 0))
a.drape(HAIR_B, [(0, -3, 0, 0), (8, -6, 20, 6), (13, -10, -4, 0), (16, -26, 0, 0), (22, -12, 0, 0), (34, -3, 0, 0)], delay=2)
a.drape(HAIR_R, [(0, 0, 0, 3), (13, 0, 0, 6), (16, -14, 0, 14), (34, 0, 0, 3)], delay=2)
a.drape(HAIR_L, [(0, 0, 0, -3), (13, 0, 0, -6), (16, -14, 0, -14), (34, 0, 0, -3)], delay=2)
a.drape(CLOTH, [(0, 0, 0, 0), (8, 4, 0, 4), (16, 14, 0, 0), (24, 4, 0, 0), (34, 0, 0, 0)], delay=2)
a.drape(TAIL, [(0, -4, 0, 0), (8, -8, 0, -10), (16, -24, 0, 0), (34, -4, 0, 0)], delay=3)
a.scl("flame", (0, .001, .001, .001), (14.5, .001, .001, .001), (15.5, 1.3, 0.8, 1.3), (17, 0.4, 0.3, 0.4), (18, .001, .001, .001),
      (19, .001, .001, .001), (19.6, 1.0, 0.6, 1.0), (21, .001, .001, .001), (23, .001, .001, .001), (23.6, 1.0, 0.6, 1.0), (25, .001, .001, .001))
a.done()

# ------------------------------------------------------------------ flame_burst (40): crouch, nozzle aimed down, 17 GROUND BLAST ring
a = A("flame_burst", 40)
a.pos("body", (0, 0, 0, 0), (10, 0, -2.6, 0), (15, 0, -3.4, 0), (17, 0, -1.0, 0), (19, 0, 0.4, 0), (28, 0, -0.6, 0), (40, 0, 0, 0))
a.rot("body", (0, 0, 0, 0), (10, -18, 0, 0), (15, -26, 0, 0), (17, -10, 0, 0), (19, 6, 0, 0), (28, 2, 0, 0), (40, 0, 0, 0))
a.rot("chest", (0, 0, 0, 0), (15, -8, 0, 0), (17, 2, 0, 0), (19, 14, 0, 0), (28, 4, 0, 0), (40, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (15, 10, 0, 0), (17, 2, 0, 0), (20, 28, 0, 0), (28, 14, 0, 0), (40, 0, 0, 0))
a.rot("arm_l", (0, 6, 0, -8), (10, 60, 0, -4), (15, 30, 0, 0), (17, 20, 0, -6), (20, 30, 0, -70), (30, 20, 0, -40), (40, 6, 0, -8))
a.rot("fore_l", (0, 16, 0, 0), (10, 60, 0, 0), (15, 10, 0, 0), (20, 20, 0, 0), (40, 16, 0, 0))
a.rot("arm_r", (0, 3, 0, 6), (10, 30, 0, 20), (15, 10, 0, 30), (17, 10, 0, 40), (20, 30, 0, 80), (30, 20, 0, 40), (40, 3, 0, 6))
a.rot("fore_r", (0, 12, 0, 0), (15, 50, 0, 0), (20, 10, 0, 0), (40, 12, 0, 0))
a.rot("claws_r", (0, 20, 0, 0), (15, 40, 0, 0), (20, -20, 0, 0), (40, 20, 0, 0))
for s, k in ((1, "r"), (-1, "l")):
    a.rot("leg_" + k, (0, 0, 0, 0), (10, 36, 0, 8 * s), (15, 48, 0, 10 * s), (17, 30, 0, 12 * s), (19, 6, 0, 14 * s), (28, 14, 0, 6 * s), (40, 0, 0, 0))
    a.rot("shin_" + k, (0, 0, 0, 0), (10, -52, 0, 0), (15, -70, 0, 0), (17, -40, 0, 0), (19, -8, 0, 0), (28, -20, 0, 0), (40, 0, 0, 0))
    a.rot("foot_" + k, (0, 0, 0, 0), (15, 22, 0, 0), (19, 2, 0, 0), (40, 0, 0, 0))
a.drape(HAIR_B, [(0, -3, 0, 0), (15, 10, 0, 0), (17, -10, 0, 0), (20, -40, 0, 0), (28, -14, 0, 0), (40, -3, 0, 0)], delay=2)
a.drape(HAIR_R, [(0, 0, 0, 3), (15, 0, 0, 0), (20, -10, 0, 40), (30, 0, 0, 10), (40, 0, 0, 3)], delay=2)
a.drape(HAIR_L, [(0, 0, 0, -3), (15, 0, 0, 0), (20, -10, 0, -40), (30, 0, 0, -10), (40, 0, 0, -3)], delay=2)
a.drape(CLOTH, [(0, 0, 0, 0), (15, -10, 0, 0), (20, 30, 0, 0), (28, 6, 0, 0), (40, 0, 0, 0)], delay=2)
a.drape(CLOTH_B, [(0, 0, 0, 0), (15, 6, 0, 0), (20, -30, 0, 0), (28, -6, 0, 0), (40, 0, 0, 0)], delay=2)
a.drape(TAIL, [(0, -4, 0, 0), (15, -2, 0, 0), (20, -50, 0, 0), (30, -12, 0, 0), (40, -4, 0, 0)], delay=3)
a.rot("ear_r", (0, 0, 0, 0), (15, 0, 0, 0), (20, -20, 0, -20), (30, 0, 0, 0), (40, 0, 0, 0))
a.rot("ear_l", (0, 0, 0, 0), (15, 0, 0, 0), (20, -20, 0, 20), (30, 0, 0, 0), (40, 0, 0, 0))
a.scl("flame", (0, .001, .001, .001), (15, .001, .001, .001), (16, 1.0, 0.5, 1.0), (17, 2.4, 0.5, 2.4), (19, 1.6, 0.3, 1.6), (21, .001, .001, .001))
a.done()

# ------------------------------------------------------------------ claw (30): two claw-glove rakes on 9 and 17
a = A("claw", 30)
a.rot("body", (0, 0, 0, 0), (5, 0, 40, 0), (9, -8, -30, 0), (11, -8, -36, 0), (13, -2, -40, 0), (17, -10, 26, 0), (20, -6, 30, 0), (30, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (5, 0, -0.8, 0.8), (9, 0, -1.2, -1.4), (13, 0, -0.8, -0.4), (17, 0, -1.4, -1.8), (30, 0, 0, 0))
a.rot("chest", (0, 0, 0, 0), (5, 6, 20, 0), (9, -10, -20, 0), (13, 0, -26, 0), (17, -14, 16, 0), (21, -8, 10, 0), (30, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (5, 0, -40, 0), (9, -4, 30, 0), (13, 4, 30, 0), (17, -8, -20, 0), (30, 0, 0, 0))
# swipe 1: wide horizontal rake right->left; swipe 2: overhead downward rake
a.rot("arm_r", (0, 3, 0, 6), (5, 40, 50, 80), (8, 90, -30, 40), (9, 90, -60, 10), (11, 70, -80, 0), (13, 150, 0, 30), (16, 120, 0, 10),
      (17, 40, 0, -10), (19, 0, 0, -6), (24, 10, 0, 6), (30, 3, 0, 6))
a.rot("fore_r", (0, 12, 0, 0), (5, 70, 0, 0), (9, 10, 0, 0), (13, 60, 0, 0), (17, 0, 0, 0), (24, 20, 0, 0), (30, 12, 0, 0))
a.rot("claws_r", (0, 20, 0, 0), (5, -20, 0, 0), (9, 40, 0, 0), (13, -30, 0, 0), (17, 50, 0, 0), (30, 20, 0, 0))
a.rot("arm_l", (0, 6, 0, -8), (5, -20, 0, -30), (9, 20, 0, -20), (13, -10, 0, -30), (17, 30, 0, -14), (30, 6, 0, -8))
a.rot("fore_l", (0, 16, 0, 0), (9, 40, 0, 0), (30, 16, 0, 0))
a.rot("leg_r", (0, 0, 0, 0), (5, -12, 0, 0), (9, 26, 0, 0), (13, 20, 0, 0), (17, 34, 0, 0), (30, 0, 0, 0))
a.rot("shin_r", (0, 0, 0, 0), (9, -20, 0, 0), (17, -30, 0, 0), (30, 0, 0, 0))
a.rot("leg_l", (0, 0, 0, 0), (5, 16, 0, 0), (9, -20, 0, 0), (17, -26, 0, 0), (30, 0, 0, 0))
a.rot("shin_l", (0, 0, 0, 0), (9, -16, 0, 0), (17, -22, 0, 0), (30, 0, 0, 0))
a.drape(HAIR_B, [(0, -3, 0, 0), (5, -6, -30, -10), (9, -14, 30, 14), (13, -10, 30, 10), (17, -20, -24, -10), (30, -3, 0, 0)], delay=2)
a.drape(HAIR_R, [(0, 0, 0, 3), (5, 0, 0, -10), (9, -6, 0, 30), (17, -10, 0, 0), (30, 0, 0, 3)], delay=2)
a.drape(HAIR_L, [(0, 0, 0, -3), (5, 0, 0, 10), (9, -6, 0, 10), (17, -10, 0, -26), (30, 0, 0, -3)], delay=2)
a.drape(CLOTH, [(0, 0, 0, 0), (5, 0, 0, -10), (9, 6, 0, 16), (17, 10, 0, -12), (30, 0, 0, 0)], delay=2)
a.drape(TAIL, [(0, -4, 0, 0), (9, -10, 0, -20), (17, -16, 0, 20), (30, -4, 0, 0)], delay=3)
a.rot("band_tail", (0, 0, 0, 0), (9, -30, 0, 50), (17, 40, 0, -20), (30, 0, 0, 0))
a.done()

# ------------------------------------------------------------------ hair_whip (32): wind, spin 1.5 turns, hair lashes on 14 and 20
a = A("hair_whip", 32)
a.rot("root", (0, 0, 0, 0), (8, 0, 40, 0), (10, 0, 30, 0), (14, 0, -150, 0), (17, 0, -260, 0), (20, 0, -390, 0), (24, 0, -440, 0), (28, 0, -360, 0), (32, 0, -360, 0))
a.pos("body", (0, 0, 0, 0), (8, 0, -1.6, 0), (14, 0, -0.4, 0), (20, 0, -0.4, 0), (26, 0, -1, 0), (32, 0, 0, 0))
a.rot("body", (0, 0, 0, 0), (8, -10, 0, 0), (14, -4, 0, 8), (20, -4, 0, 8), (32, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (8, -10, -10, 0), (14, -16, 0, 0), (20, -16, 0, 0), (26, 6, 0, 0), (32, 0, 0, 0))
a.rot("arm_r", (0, 3, 0, 6), (8, -20, 0, 30), (14, 10, 0, 80), (20, 10, 0, 84), (26, 10, 0, 30), (32, 3, 0, 6))
a.rot("arm_l", (0, 6, 0, -8), (8, 30, 0, -20), (14, 20, 0, -70), (20, 20, 0, -74), (26, 10, 0, -20), (32, 6, 0, -8))
for s, k in ((1, "r"), (-1, "l")):
    a.rot("leg_" + k, (0, 0, 0, 0), (8, 24, 0, 6 * s), (14, 10, 0, 10 * s), (20, 10, 0, 10 * s), (26, 20, 0, 4 * s), (32, 0, 0, 0))
    a.rot("shin_" + k, (0, 0, 0, 0), (8, -40, 0, 0), (14, -16, 0, 0), (20, -16, 0, 0), (26, -30, 0, 0), (32, 0, 0, 0))
# hair flies out horizontally (lagging behind the spin direction)
a.rot("hair_b1", (0, -3, 0, 0), (8, 6, 0, 0), (12, -60, 30, 0), (14, -78, 50, 0), (17, -80, 40, 0), (20, -82, 50, 0), (24, -50, 20, 0), (28, -14, 0, 0), (32, -3, 0, 0))
a.rot("hair_b2", (0, 0, 0, 0), (10, 10, 0, 0), (14, -10, 30, 0), (20, -12, 30, 0), (26, -20, 10, 0), (32, 0, 0, 0))
a.rot("hair_b3", (0, 0, 0, 0), (12, 10, 0, 0), (16, -6, 30, 0), (22, -10, 30, 0), (28, -10, 0, 0), (32, 0, 0, 0))
a.rot("hair_r1", (0, 0, 0, 3), (12, -20, 0, 70), (20, -24, 0, 76), (28, 0, 0, 10), (32, 0, 0, 3))
a.rot("hair_r2", (0, 0, 0, 0), (14, 0, 0, 20), (22, 0, 0, 24), (30, 0, 0, 0), (32, 0, 0, 0))
a.rot("hair_l1", (0, 0, 0, -3), (12, -20, 0, -70), (20, -24, 0, -76), (28, 0, 0, -10), (32, 0, 0, -3))
a.rot("hair_l2", (0, 0, 0, 0), (14, 0, 0, -20), (22, 0, 0, -24), (30, 0, 0, 0), (32, 0, 0, 0))
a.drape(CLOTH, [(0, 0, 0, 0), (14, 40, 0, 0), (20, 44, 0, 0), (28, 6, 0, 0), (32, 0, 0, 0)], delay=2)
a.drape(CLOTH_B, [(0, 0, 0, 0), (14, -40, 0, 0), (20, -44, 0, 0), (28, -6, 0, 0), (32, 0, 0, 0)], delay=2)
a.drape(TAIL, [(0, -4, 0, 0), (14, -70, 0, 0), (20, -74, 0, 0), (28, -10, 0, 0), (32, -4, 0, 0)], delay=2)
a.done()

# ------------------------------------------------------------------ flame_rush (52): crouch, jet-propelled by a backward flame 20..36, claw first
a = A("flame_rush", 52)
a.pos("body", (0, 0, 0, 0), (10, 0, -2.6, 0), (18, 0, -3.0, 0), (20, 0, -2.0, 0), (36, 0, -2.0, 0), (42, 0, -1.0, 0), (52, 0, 0, 0))
a.rot("body", (0, 0, 0, 0), (10, -20, 0, 0), (14, -22, 0, 0), (18, -26, 0, 0), (20, -40, 0, 0), (36, -40, 0, 0), (40, -10, 0, 0), (44, 6, 0, 0), (52, 0, 0, 0))
a.rot("chest", (0, 0, 0, 0), (14, -6, 6, 0), (16, -6, -6, 0), (18, -6, 6, 0), (20, 4, 0, 0), (36, 4, 0, 0), (52, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (18, 20, 0, 0), (20, 34, 0, 0), (36, 34, 0, 0), (44, 0, 0, 0), (52, 0, 0, 0))
a.rot("arm_l", (0, 6, 0, -8), (10, -30, 0, -10), (18, -40, 0, -10), (20, -52, 0, -14), (36, -52, 0, -14), (42, -20, 0, -10), (52, 6, 0, -8))
a.rot("fore_l", (0, 16, 0, 0), (18, 0, 0, 0), (36, 0, 0, 0), (52, 16, 0, 0))
a.rot("hand_l", (0, 20, 0, 0), (18, 0, 0, 0), (36, 0, 0, 0), (52, 20, 0, 0))
a.rot("arm_r", (0, 3, 0, 6), (10, 30, 0, 20), (18, 20, 0, 20), (20, 120, 0, 10), (36, 120, 0, 10), (42, 40, 0, 10), (52, 3, 0, 6))
a.rot("fore_r", (0, 12, 0, 0), (18, 60, 0, 0), (20, 10, 0, 0), (36, 10, 0, 0), (52, 12, 0, 0))
a.rot("claws_r", (0, 20, 0, 0), (18, 30, 0, 0), (20, -20, 0, 0), (36, -20, 0, 0), (52, 20, 0, 0))
# rev: legs crouched + stamping; dash: running cycle every 6 ticks
run_r = [(0, 0, 0, 0), (10, 40, 0, 6), (18, 46, 0, 6)]
run_l = [(0, 0, 0, 0), (10, -10, 0, -6), (18, -16, 0, -6)]
sh_r = [(0, 0, 0, 0), (10, -50, 0, 0), (18, -60, 0, 0)]
sh_l = [(0, 0, 0, 0), (10, -60, 0, 0), (18, -70, 0, 0)]
for i, t in enumerate(range(20, 37, 4)):
    ph = i % 2
    run_r.append((t, 70 if ph else -20, 0, 0)); run_l.append((t, -20 if ph else 70, 0, 0))
    sh_r.append((t, -20 if ph else -80, 0, 0)); sh_l.append((t, -80 if ph else -20, 0, 0))
run_r += [(42, 20, 0, 0), (52, 0, 0, 0)]; run_l += [(42, -14, 0, 0), (52, 0, 0, 0)]
sh_r += [(42, -20, 0, 0), (52, 0, 0, 0)]; sh_l += [(42, -10, 0, 0), (52, 0, 0, 0)]
a.rot("leg_r", *run_r); a.rot("leg_l", *run_l); a.rot("shin_r", *sh_r); a.rot("shin_l", *sh_l)
a.drape(HAIR_B, [(0, -3, 0, 0), (18, -10, 0, 0), (20, -70, 0, 0), (28, -76, 0, 4), (36, -70, 0, -4), (44, -20, 0, 0), (52, -3, 0, 0)], delay=2, gain=0.7)
a.drape(HAIR_R, [(0, 0, 0, 3), (20, -50, 0, 14), (36, -50, 0, 18), (46, 0, 0, 3), (52, 0, 0, 3)], delay=2)
a.drape(HAIR_L, [(0, 0, 0, -3), (20, -50, 0, -14), (36, -50, 0, -18), (46, 0, 0, -3), (52, 0, 0, -3)], delay=2)
a.drape(CLOTH, [(0, 0, 0, 0), (20, 50, 0, 0), (36, 54, 0, 0), (44, 0, 0, 0), (52, 0, 0, 0)], delay=2)
a.drape(CLOTH_B, [(0, 0, 0, 0), (20, -50, 0, 0), (36, -56, 0, 0), (44, 0, 0, 0), (52, 0, 0, 0)], delay=2)
a.drape(TAIL, [(0, -4, 0, 0), (20, -70, 0, 6), (36, -76, 0, -6), (44, -10, 0, 0), (52, -4, 0, 0)], delay=2)
a.rot("ear_r", (0, 0, 0, 0), (20, -40, 0, 0), (36, -40, 0, 0), (44, 0, 0, 0))
a.rot("ear_l", (0, 0, 0, 0), (20, -40, 0, 0), (36, -40, 0, 0), (44, 0, 0, 0))
fl = [(0, .001, .001, .001)]
for t in range(2, 18, 4):   # sputtering revs while charging
    fl += [(t, .001, .001, .001), (t + 1, 0.6, 0.35, 0.6), (t + 2.5, .001, .001, .001)]
fl += flame_on(19, 36, 1.5)[1:]
a.scl("flame", *fl)
a.done()

# ------------------------------------------------------------------ molotov (46): fish a bottle out, light it, overhand throw at 14
a = A("molotov", 46)
a.scl("bottle", (0, .001, .001, .001), (2, .001, .001, .001), (4, 1, 1, 1), (14, 1, 1, 1), (14.5, .001, .001, .001))
a.rot("body", (0, 0, 0, 0), (5, 4, 10, 0), (11, 12, -34, 0), (14, -12, 24, 0), (18, -16, 30, 0), (30, -4, 6, 0), (46, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (11, 0, -0.6, 1.4), (14, 0, -1.2, -1.4), (20, 0, -1.0, -1.0), (46, 0, 0, 0))
a.rot("chest", (0, 0, 0, 0), (11, 10, -10, 0), (14, -14, 10, 0), (20, -10, 6, 0), (46, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (5, -20, 0, 0), (11, 4, 26, 0), (14, 0, -10, 0), (22, 6, 0, 0), (46, 0, 0, 0))
a.rot("arm_r", (0, 3, 0, 6), (3, -20, 0, -10), (5, 40, 0, -20), (8, 50, 0, -10), (11, 170, 0, 20), (13, 140, 0, 10), (14, 80, 0, 0), (16, 20, 0, -10),
      (22, 10, 0, -6), (32, 6, 0, 6), (46, 3, 0, 6))
a.rot("fore_r", (0, 12, 0, 0), (3, 40, 0, 0), (5, 80, 0, 0), (8, 90, 0, 0), (11, 70, 0, 0), (14, 10, 0, 0), (22, 30, 0, 0), (46, 12, 0, 0))
a.rot("claws_r", (0, 20, 0, 0), (4, 60, 0, 0), (14, 60, 0, 0), (15, -20, 0, 0), (24, 10, 0, 0), (46, 20, 0, 0))
# left lights the rag with the pilot light (gun nozzle to the bottle) at 5-8
a.rot("arm_l", (0, 6, 0, -8), (5, 60, -30, 30), (8, 64, -36, 34), (11, 20, 0, -30), (14, -10, 0, -20), (24, 0, 0, -10), (46, 6, 0, -8))
a.rot("fore_l", (0, 16, 0, 0), (5, 50, 0, 0), (11, 20, 0, 0), (46, 16, 0, 0))
a.rot("leg_r", (0, 0, 0, 0), (11, -20, 0, 0), (14, 6, 0, 0), (46, 0, 0, 0))
a.rot("leg_l", (0, 0, 0, 0), (11, 24, 0, 0), (14, -10, 0, 0), (46, 0, 0, 0))
a.rot("shin_l", (0, 0, 0, 0), (11, -20, 0, 0), (14, -6, 0, 0), (46, 0, 0, 0))
a.rot("shin_r", (0, 0, 0, 0), (14, -30, 0, 0), (22, -14, 0, 0), (46, 0, 0, 0))
a.drape(HAIR_B, [(0, -3, 0, 0), (11, -2, -14, 0), (14, -26, 16, 0), (20, -20, 10, 0), (30, -6, 0, 0), (46, -3, 0, 0)], delay=2)
a.drape(HAIR_R, [(0, 0, 0, 3), (11, 0, 0, 10), (15, -10, 0, 0), (46, 0, 0, 3)], delay=2)
a.drape(HAIR_L, [(0, 0, 0, -3), (11, 0, 0, -8), (15, -10, 0, -16), (46, 0, 0, -3)], delay=2)
a.drape(CLOTH, [(0, 0, 0, 0), (11, -4, 0, -6), (15, 14, 0, 8), (26, 2, 0, 0), (46, 0, 0, 0)], delay=2)
a.drape(TAIL, [(0, -4, 0, 0), (11, 0, 0, 10), (15, -26, 0, -10), (30, -4, 0, 0), (46, -4, 0, 0)], delay=3)
a.rot("band_tail", (0, 0, 0, 0), (11, 30, 0, 0), (15, -40, 0, 30), (30, 0, 0, 0))
a.done()

# ------------------------------------------------------------------ inferno (74, enraged): cackling, gun to the sky, fire pulses on 20/34/48/62
a = A("inferno", 74)
pulse = [20, 34, 48, 62]
bk = [(0, 0, 0, 0), (10, 8, 0, 0), (18, -10, 0, 0)]
dip = [(0, 0, 0, 0), (10, -0.6, 0, 0), (18, -1.4, 0, 0)]
for p in pulse:
    bk += [(p, 16, 0, 0), (p + 4, 4, 0, 0), (p + 10, -6, 0, 0)]
    dip += [(p, 0.4, 0, 0), (p + 4, -1.2, 0, 0), (p + 10, -1.6, 0, 0)]
bk += [(74, 0, 0, 0)]; dip += [(74, 0, 0, 0)]
a.rot("chest", *bk)
a.pos("body", *[(t, 0, y, 0) for (t, y, _, __) in dip])
a.rot("body", (0, 0, 0, 0), (18, 0, 20, 0), (34, 0, -20, 0), (48, 0, 20, 0), (62, 0, -20, 0), (74, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (10, -14, 0, 0), (18, 30, 0, 0), (21, 36, 0, 8), (24, 26, 0, -8), (27, 36, 0, 8), (30, 26, 0, -8), (34, 36, 0, 8),
      (40, 26, 0, -8), (48, 36, 0, 8), (55, 26, 0, -8), (62, 36, 0, 8), (68, 10, 0, 0), (74, 0, 0, 0))   # head-thrown-back laughing shudder
a.rot("arm_l", (0, 6, 0, -8), (10, 40, 0, -20), (18, 170, 0, -10), (62, 170, 0, -10), (68, 60, 0, -10), (74, 6, 0, -8))
a.rot("fore_l", (0, 16, 0, 0), (18, 0, 0, 0), (62, 0, 0, 0), (74, 16, 0, 0))
a.rot("hand_l", (0, 20, 0, 0), (18, 0, 0, 0), (62, 0, 0, 0), (74, 20, 0, 0))
a.rot("arm_r", (0, 3, 0, 6), (10, -10, 0, 40), (18, 20, 0, 100), (34, 30, 0, 110), (48, 20, 0, 100), (62, 30, 0, 110), (70, 10, 0, 20), (74, 3, 0, 6))
a.rot("claws_r", (0, 20, 0, 0), (18, -30, 0, 0), (62, -30, 0, 0), (74, 20, 0, 0))
for s, k in ((1, "r"), (-1, "l")):
    a.rot("leg_" + k, (0, 0, 0, 0), (18, 10, 0, 14 * s), (62, 10, 0, 14 * s), (74, 0, 0, 0))
    a.rot("shin_" + k, (0, 0, 0, 0), (18, -20, 0, 0), (62, -20, 0, 0), (74, 0, 0, 0))
hb = [(0, -3, 0, 0), (18, -10, 0, 0)]
for p in pulse:
    hb += [(p + 1, -60, 0, 0), (p + 6, -30, 0, 0), (p + 12, -46, 0, 0)]
hb += [(74, -3, 0, 0)]
a.drape(HAIR_B, hb, delay=2, gain=0.8)
a.drape(HAIR_R, [(0, 0, 0, 3)] + [(p + 1, -20, 0, 50) for p in pulse] + [(p + 7, -10, 0, 26) for p in pulse] + [(74, 0, 0, 3)], delay=2)
a.drape(HAIR_L, [(0, 0, 0, -3)] + [(p + 1, -20, 0, -50) for p in pulse] + [(p + 7, -10, 0, -26) for p in pulse] + [(74, 0, 0, -3)], delay=2)
a.drape(CLOTH, [(0, 0, 0, 0)] + [(p + 1, 40, 0, 0) for p in pulse] + [(p + 7, 14, 0, 0) for p in pulse] + [(74, 0, 0, 0)], delay=2)
a.drape(CLOTH_B, [(0, 0, 0, 0)] + [(p + 1, -40, 0, 0) for p in pulse] + [(p + 7, -14, 0, 0) for p in pulse] + [(74, 0, 0, 0)], delay=2)
a.drape(TAIL, [(0, -4, 0, 0)] + [(p + 1, -60, 0, 0) for p in pulse] + [(p + 7, -24, 0, 0) for p in pulse] + [(74, -4, 0, 0)], delay=2)
a.rot("ear_r", (0, 0, 0, 0), (18, 0, 0, -24), (62, 0, 0, -24), (74, 0, 0, 0))
a.rot("ear_l", (0, 0, 0, 0), (18, 0, 0, 24), (62, 0, 0, 24), (74, 0, 0, 0))
fl = [(0, .001, .001, .001), (17, .001, .001, .001), (19, 1.2, 1.4, 1.2)]
for p in pulse:
    fl += [(p, 1.8, 2.2, 1.8), (p + 3, 1.2, 1.3, 1.2)] + ([(p + 8, 1.4, 1.6, 1.4)] if p < 60 else [])
fl += [(64, 1.0, 1.0, 1.0), (67, .001, .001, .001)]
a.scl("flame", *fl)
a.done()

# ------------------------------------------------------------------ fire_wall (44): low wide sweep right->left across the ground 12..24
a = A("fire_wall", 44)
a.pos("body", (0, 0, 0, 0), (10, 0, -2.0, 0), (24, 0, -2.0, 0), (34, 0, -0.6, 0), (44, 0, 0, 0))
a.rot("body", (0, 0, 0, 0), (10, -14, -50, 0), (12, -16, -46, 0), (24, -16, 46, 0), (28, -12, 52, 0), (36, -4, 10, 0), (44, 0, 0, 0))
a.rot("chest", (0, 0, 0, 0), (10, -10, -10, 0), (24, -10, 10, 0), (44, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (10, -10, 40, 0), (12, -6, 30, 0), (24, -6, -30, 0), (30, 4, -20, 0), (44, 0, 0, 0))
a.rot("arm_l", (0, 6, 0, -8), (10, 60, 0, 10), (12, 64, 0, 10), (24, 64, 0, -30), (30, 40, 0, -20), (44, 6, 0, -8))
a.rot("fore_l", (0, 16, 0, 0), (12, 0, 0, 0), (24, 0, 0, 0), (44, 16, 0, 0))
a.rot("hand_l", (0, 20, 0, 0), (12, -10, 0, 0), (24, -10, 0, 0), (44, 20, 0, 0))
a.rot("arm_r", (0, 3, 0, 6), (10, -30, 0, 40), (24, -20, 0, 50), (32, 0, 0, 20), (44, 3, 0, 6))
a.rot("fore_r", (0, 12, 0, 0), (24, 30, 0, 0), (44, 12, 0, 0))
a.rot("leg_r", (0, 0, 0, 0), (10, 30, 0, 10), (24, 30, 0, 10), (44, 0, 0, 0))
a.rot("shin_r", (0, 0, 0, 0), (10, -40, 0, 0), (24, -40, 0, 0), (44, 0, 0, 0))
a.rot("leg_l", (0, 0, 0, 0), (10, -16, 0, -16), (24, -16, 0, -16), (44, 0, 0, 0))
a.rot("shin_l", (0, 0, 0, 0), (10, -20, 0, 0), (24, -20, 0, 0), (44, 0, 0, 0))
a.drape(HAIR_B, [(0, -3, 0, 0), (10, -10, 40, 10), (24, -20, -40, -14), (30, -16, -30, -10), (44, -3, 0, 0)], delay=3)
a.drape(HAIR_R, [(0, 0, 0, 3), (10, -6, 0, -6), (24, -10, 0, 30), (44, 0, 0, 3)], delay=3)
a.drape(HAIR_L, [(0, 0, 0, -3), (10, -6, 0, -30), (24, -10, 0, 6), (44, 0, 0, -3)], delay=3)
a.drape(CLOTH, [(0, 0, 0, 0), (10, 4, 0, 14), (24, 8, 0, -16), (34, 2, 0, 0), (44, 0, 0, 0)], delay=2)
a.drape(TAIL, [(0, -4, 0, 0), (10, -10, 0, 30), (24, -20, 0, -30), (44, -4, 0, 0)], delay=3)
a.scl("flame", *flame_on(11, 25, 1.6))
a.done()

# ------------------------------------------------------------------ napalm_rain (50): lean back, fire 4 gouts into the sky 14..26, watch them fall
a = A("napalm_rain", 50)
a.pos("body", (0, 0, 0, 0), (10, 0, -1.0, 1.0), (26, 0, -1.0, 1.0), (40, 0, 0, 0), (50, 0, 0, 0))
a.rot("body", (0, 0, 0, 0), (10, 14, 0, 0), (26, 14, 0, 0), (40, 0, 0, 0), (50, 0, 0, 0))
a.rot("chest", (0, 0, 0, 0), (10, 16, 0, 0), (14, 20, 0, 0), (17, 12, 0, 0), (20, 20, 0, 0), (23, 12, 0, 0), (26, 20, 0, 0), (30, 6, 0, 0), (50, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (10, 30, 0, 0), (26, 34, 0, 0), (32, -10, 0, 0), (40, -14, 0, 4), (50, 0, 0, 0))   # then looks down at the target as it rains
a.rot("arm_l", (0, 6, 0, -8), (10, 150, 0, -4), (14, 160, 0, -4), (15, 170, 0, -4), (17, 158, 0, -4), (18, 172, 0, -4), (20, 158, 0, -4), (21, 172, 0, -4),
      (23, 158, 0, -4), (24, 172, 0, -4), (27, 150, 0, -4), (34, 40, 0, -8), (50, 6, 0, -8))
a.rot("fore_l", (0, 16, 0, 0), (10, 0, 0, 0), (27, 0, 0, 0), (50, 16, 0, 0))
a.rot("hand_l", (0, 20, 0, 0), (10, 0, 0, 0), (27, 0, 0, 0), (50, 20, 0, 0))
a.rot("arm_r", (0, 3, 0, 6), (10, 140, -20, -24), (27, 140, -20, -24), (34, 30, 0, 10), (40, 60, 0, 40), (46, 10, 0, 6), (50, 3, 0, 6))  # points at the target
a.rot("fore_r", (0, 12, 0, 0), (10, 20, 0, 0), (27, 20, 0, 0), (40, 0, 0, 0), (50, 12, 0, 0))
a.rot("claws_r", (0, 20, 0, 0), (40, -20, 0, 0), (50, 20, 0, 0))
a.rot("leg_r", (0, 0, 0, 0), (10, -14, 0, 6), (26, -14, 0, 6), (50, 0, 0, 0))
a.rot("leg_l", (0, 0, 0, 0), (10, 22, 0, -6), (26, 22, 0, -6), (50, 0, 0, 0))
a.rot("shin_l", (0, 0, 0, 0), (10, -24, 0, 0), (26, -24, 0, 0), (50, 0, 0, 0))
a.drape(HAIR_B, [(0, -3, 0, 0), (10, 4, 0, 0)] + [(t, -12 if (t // 3) % 2 else -2, 0, 0) for t in (14, 17, 20, 23, 26)] + [(34, -6, 0, 0), (50, -3, 0, 0)], delay=2)
a.drape(HAIR_R, [(0, 0, 0, 3), (14, 0, 0, 10), (26, 0, 0, 12), (50, 0, 0, 3)], delay=3)
a.drape(HAIR_L, [(0, 0, 0, -3), (14, 0, 0, -10), (26, 0, 0, -12), (50, 0, 0, -3)], delay=3)
a.drape(CLOTH, [(0, 0, 0, 0), (14, -4, 0, 0), (26, -4, 0, 0), (50, 0, 0, 0)], delay=2)
a.drape(TAIL, [(0, -4, 0, 0), (14, 6, 0, 0), (26, 6, 0, 0), (50, -4, 0, 0)], delay=3)
fl = [(0, .001, .001, .001)]
for t in (14, 17, 20, 23):
    fl += [(t - 0.5, .001, .001, .001), (t, 1.6, 2.0, 1.6), (t + 1.5, 0.8, 1.0, 0.8), (t + 2.5, .001, .001, .001)]
a.scl("flame", *fl)
a.done()

# ------------------------------------------------------------------ pounce (36): wolf crouch, leap 9..16, claw slam landing on 17
a = A("pounce", 36)
a.pos("root", (0, 0, 0, 0), (8, 0, 0, 0), (10, 0, 3, 0), (13, 0, 5, 0), (16, 0, 1.5, 0), (17, 0, 0, 0), (36, 0, 0, 0))
a.pos("body", (0, 0, 0, 0), (7, 0, -3.2, 0), (9, 0, -0.6, 0), (13, 0, -0.8, 0), (17, 0, -3.4, 0), (22, 0, -3.0, 0), (30, 0, -0.8, 0), (36, 0, 0, 0))
a.rot("body", (0, 0, 0, 0), (7, -28, 0, 0), (10, -10, 0, 0), (14, -24, 0, 0), (17, -34, 0, 0), (22, -30, 0, 0), (30, -8, 0, 0), (36, 0, 0, 0))
a.rot("chest", (0, 0, 0, 0), (7, -6, 0, 0), (10, 10, 0, 0), (17, -10, 0, 0), (36, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (7, 34, 0, 0), (13, 20, 0, 0), (17, 40, 0, 0), (24, 30, 0, 0), (36, 0, 0, 0))
a.rot("arm_r", (0, 3, 0, 6), (7, -30, 0, 20), (10, 160, 0, 20), (14, 170, 0, 16), (17, 60, 0, 6), (19, 40, 0, 6), (28, 20, 0, 6), (36, 3, 0, 6))
a.rot("fore_r", (0, 12, 0, 0), (7, 30, 0, 0), (10, 10, 0, 0), (17, 0, 0, 0), (36, 12, 0, 0))
a.rot("claws_r", (0, 20, 0, 0), (10, -30, 0, 0), (17, 50, 0, 0), (28, 30, 0, 0), (36, 20, 0, 0))
a.rot("arm_l", (0, 6, 0, -8), (7, -40, 0, -20), (10, 30, 0, -50), (17, 20, 0, -40), (28, 0, 0, -10), (36, 6, 0, -8))
for s, k in ((1, "r"), (-1, "l")):
    a.rot("leg_" + k, (0, 0, 0, 0), (7, 60, 0, 8 * s), (9, -20, 0, 4 * s), (12, 50, 0, 6 * s), (15, 60, 0, 6 * s), (17, 70, 0, 10 * s), (24, 60, 0, 10 * s), (32, 10, 0, 0), (36, 0, 0, 0))
    a.rot("shin_" + k, (0, 0, 0, 0), (7, -90, 0, 0), (9, -10, 0, 0), (12, -90, 0, 0), (15, -60, 0, 0), (17, -100, 0, 0), (24, -90, 0, 0), (32, -20, 0, 0), (36, 0, 0, 0))
    a.rot("foot_" + k, (0, 0, 0, 0), (7, 30, 0, 0), (9, -30, 0, 0), (17, 30, 0, 0), (24, 30, 0, 0), (36, 0, 0, 0))
a.drape(HAIR_B, [(0, -3, 0, 0), (7, 6, 0, 0), (10, -50, 0, 0), (14, -30, 0, 0), (17, 30, 0, 0), (22, -10, 0, 0), (36, -3, 0, 0)], delay=2)
a.drape(HAIR_R, [(0, 0, 0, 3), (10, -30, 0, 20), (17, 20, 0, 30), (26, 0, 0, 6), (36, 0, 0, 3)], delay=2)
a.drape(HAIR_L, [(0, 0, 0, -3), (10, -30, 0, -20), (17, 20, 0, -30), (26, 0, 0, -6), (36, 0, 0, -3)], delay=2)
a.drape(CLOTH, [(0, 0, 0, 0), (10, 40, 0, 0), (17, -10, 0, 0), (24, 10, 0, 0), (36, 0, 0, 0)], delay=2)
a.drape(TAIL, [(0, -4, 0, 0), (10, -60, 0, 0), (17, 10, 0, 0), (26, -20, 0, 0), (36, -4, 0, 0)], delay=2)
a.rot("ear_r", (0, 0, 0, 0), (7, -30, 0, 0), (17, 20, 0, -20), (26, 0, 0, 0))
a.rot("ear_l", (0, 0, 0, 0), (7, -30, 0, 0), (17, 20, 0, 20), (26, 0, 0, 0))
a.done()

# ------------------------------------------------------------------ pyre_spin (60, enraged): flame arm out, two full turns of fire 14..44
a = A("pyre_spin", 60)
a.rot("root", (0, 0, 0, 0), (10, 0, 30, 0), (14, 0, 0, 0), (29, 0, -360, 0), (44, 0, -720, 0), (50, 0, -760, 0), (60, 0, -720, 0))
a.pos("body", (0, 0, 0, 0), (10, 0, -1.6, 0), (14, 0, -1.2, 0), (44, 0, -1.2, 0), (52, 0, -0.4, 0), (60, 0, 0, 0))
a.rot("body", (0, 0, 0, 0), (10, -10, 0, 0), (14, -6, 0, 12), (44, -6, 0, 12), (52, 0, 0, 0), (60, 0, 0, 0))
a.rot("head", (0, 0, 0, 0), (10, -6, 0, 0), (14, 20, 0, -10), (44, 20, 0, -10), (52, 0, 0, 0), (60, 0, 0, 0))
a.rot("arm_l", (0, 6, 0, -8), (10, 40, 0, -30), (14, 0, 0, -88), (44, 0, 0, -88), (50, 20, 0, -30), (60, 6, 0, -8))
a.rot("fore_l", (0, 16, 0, 0), (14, 0, 0, 0), (44, 0, 0, 0), (60, 16, 0, 0))
a.rot("hand_l", (0, 20, 0, 0), (14, 0, 0, 0), (44, 0, 0, 0), (60, 20, 0, 0))
a.rot("arm_r", (0, 3, 0, 6), (10, 20, 0, 30), (14, -10, 0, 70), (44, -10, 0, 70), (52, 10, 0, 20), (60, 3, 0, 6))
a.rot("claws_r", (0, 20, 0, 0), (14, -20, 0, 0), (44, -20, 0, 0), (60, 20, 0, 0))
for s, k in ((1, "r"), (-1, "l")):
    a.rot("leg_" + k, (0, 0, 0, 0), (10, 24, 0, 8 * s), (14, 10, 0, 12 * s), (44, 10, 0, 12 * s), (52, 10, 0, 4 * s), (60, 0, 0, 0))
    a.rot("shin_" + k, (0, 0, 0, 0), (10, -40, 0, 0), (14, -20, 0, 0), (44, -20, 0, 0), (60, 0, 0, 0))
a.rot("hair_b1", (0, -3, 0, 0), (10, 4, 0, 0), (16, -70, 40, 0), (44, -76, 40, 0), (50, -30, 10, 0), (56, -6, 0, 0), (60, -3, 0, 0))
a.rot("hair_b2", (0, 0, 0, 0), (18, -10, 30, 0), (44, -10, 30, 0), (52, -16, 0, 0), (60, 0, 0, 0))
a.rot("hair_b3", (0, 0, 0, 0), (20, -6, 30, 0), (46, -6, 30, 0), (54, -10, 0, 0), (60, 0, 0, 0))
a.drape(HAIR_R, [(0, 0, 0, 3), (16, -20, 0, 66), (44, -20, 0, 70), (54, 0, 0, 8), (60, 0, 0, 3)], delay=2)
a.drape(HAIR_L, [(0, 0, 0, -3), (16, -20, 0, -66), (44, -20, 0, -70), (54, 0, 0, -8), (60, 0, 0, -3)], delay=2)
a.drape(CLOTH, [(0, 0, 0, 0), (16, 44, 0, 0), (44, 46, 0, 0), (54, 4, 0, 0), (60, 0, 0, 0)], delay=2)
a.drape(CLOTH_B, [(0, 0, 0, 0), (16, -44, 0, 0), (44, -46, 0, 0), (54, -4, 0, 0), (60, 0, 0, 0)], delay=2)
a.drape(TAIL, [(0, -4, 0, 0), (16, -76, 0, 0), (44, -78, 0, 0), (54, -10, 0, 0), (60, -4, 0, 0)], delay=2)
a.scl("flame", *flame_on(13, 44, 1.7))
a.done()

# ------------------------------------------------------------------ death (40 ticks scrubbed): flame sputters, knees buckle, falls forward
a = A("death", 40)
a.scl("flame", (0, .001, .001, .001), (2, 0.8, 0.5, 0.8), (4, .001, .001, .001), (7, 0.5, 0.3, 0.5), (9, .001, .001, .001))
a.rot("head", (0, 0, 0, 0), (6, 30, 0, 10), (14, -20, 0, 14), (30, -10, 20, 20), (40, -10, 20, 20))
a.rot("chest", (0, 0, 0, 0), (6, 16, 0, 0), (16, -20, 0, 0), (40, -10, 0, 0))
a.pos("body", (0, 0, 0, 0), (6, 0, 0, 0), (16, 0, -5.0, 0), (40, 0, -5.0, 0))
a.rot("body", (0, 0, 0, 0), (6, 6, 0, 0), (16, -10, 0, 0), (40, -10, 0, 0))
for s, k in ((1, "r"), (-1, "l")):
    a.rot("leg_" + k, (0, 0, 0, 0), (6, 0, 0, 0), (16, 80, 0, 6 * s), (40, 80, 0, 6 * s))
    a.rot("shin_" + k, (0, 0, 0, 0), (6, -10, 0, 0), (16, -90, 0, 0), (40, -90, 0, 0))
a.pos("root", (0, 0, 0, 0), (16, 0, 0, 0), (30, 0, 2.0, -2), (40, 0, 1.6, -3))
a.rot("root", (0, 0, 0, 0), (16, 0, 0, 0), (30, -80, 0, 6), (34, -74, 0, 6), (40, -80, 0, 6))
a.rot("arm_l", (0, 6, 0, -8), (6, -30, 0, -30), (16, 20, 0, -20), (30, 150, 0, -30), (40, 160, 0, -30))
a.rot("hand_l", (0, 20, 0, 0), (16, 60, 0, 0), (40, 80, 0, 0))   # gun slips
a.rot("arm_r", (0, 3, 0, 6), (6, -30, 0, 30), (16, 30, 0, 20), (30, 150, 0, 30), (40, 160, 0, 30))
a.drape(HAIR_B, [(0, -3, 0, 0), (6, -20, 0, 0), (16, 10, 0, 0), (30, 60, 0, 0), (34, 40, 0, 0), (40, 50, 0, 0)], delay=2)
a.drape(HAIR_R, [(0, 0, 0, 3), (16, 0, 0, 20), (30, 30, 0, 30), (40, 30, 0, 30)], delay=2)
a.drape(HAIR_L, [(0, 0, 0, -3), (16, 0, 0, -20), (30, 30, 0, -30), (40, 30, 0, -30)], delay=2)
a.drape(TAIL, [(0, -4, 0, 0), (16, -20, 0, 0), (30, 60, 0, 0), (40, 70, 0, 0)], delay=2)
a.rot("ear_r", (0, 0, 0, 0), (16, 0, 0, 0), (30, 30, 0, 20), (40, 40, 0, 30))
a.rot("ear_l", (0, 0, 0, 0), (16, 0, 0, 0), (30, 30, 0, -20), (40, 40, 0, -30))
a.done()

os.makedirs(os.path.dirname(OUT), exist_ok=True)
m.save(OUT)
print("cubes", len(m.cubes), "anims", [x["name"] for x in m.anims], "atlas rows used", m.cy + m.rowh)
