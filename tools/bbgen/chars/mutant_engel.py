"""Mutant Engel (FPE Green mutant student, ENGEL 002) - generates assets/fpe/bbmodels/mutant_engel.bbmodel.
Reference: docs/ref/confirmed/mutant_engel.png. TALL lanky boy: big spiky white hair with two striped feathers (teal / red / black),
pale cracked face with a WIDE black grin, white shirt with a torn jagged hem and jagged back flaps, striped (red + green) short sleeves,
the LEFT arm is a huge ink-black clawed limb, black baggy overall-trousers, white striped leg warmers, black pointed boots,
white swirl ribbons at the left hip. Ink-outlined, monochrome + red/green accents.
Blockbench space: Y up, ground 0, faces -Z. Character's RIGHT = +X (left = -X = the big claw).
Rotation signs (file values): arm/leg rx>0 = swing forward, torso/head rx>0 = lean back / look up, jaw rx<0 = open,
ry>0 = turn to the character's left, rz>0 = hanging part swings toward +X (character's right).
Every key tick matches entity/characters/MutantEngel.java.  Hitbox 0.8 x 2.8 -> ~45 px tall.
Run: python3 tools/bbgen/chars/mutant_engel.py
"""
import math, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from bbgen import Model, mix  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "../../../src/main/resources/assets/fpe/bbmodels/mutant_engel.bbmodel")

# ------------------------------------------------------------------ palette
WH, WH_D, WH_DD, WH_L = 0xF0F0F3, 0xC8C9D0, 0x9A9CA6, 0xFFFFFF
SKIN, SKIN_D = 0xE4E4E8, 0xB4B6BE
BLK, BLK_L, BLK_D = 0x16161B, 0x33333D, 0x09090C
LINE = 0x24242C
RED, GRN = 0xB8474B, 0x5C9C80
TEAL, TEAL_D = 0x4F8E8C, 0x2F5E5E
MOUTH, GUM = 0x0B0A0E, 0x3A2630
TOOTH, TOOTH_D = 0xFCFCFC, 0xBFC0C8

m = Model("mutant_engel", S=8, atlas=2048)
R = m.rng


# ------------------------------------------------------------------ painters
def all_faces(fn, skip=()):
    return {k: fn for k in ("north", "south", "east", "west", "up", "down") if k not in skip}


def combo(*fns):
    def f(F):
        for fn in fns: fn(F)
    return f


def outline(c=LINE):
    return lambda F: (F.rect(0, 0, F.w, 1, c), F.rect(0, F.h - 1, F.w, 1, c), F.rect(0, 0, 1, F.h, c), F.rect(F.w - 1, 0, 1, F.h, c))


def cloth(base=WH, dark=WH_D, n=2, ink=True):
    def f(F):
        for y in range(F.h):
            for x in range(F.w):
                k = y / max(1, F.h - 1)
                F.px(x, y, mix(base, dark, 0.06 + 0.34 * k * k))
        for i in range(n):
            x = int((i + 0.5) * F.w / n) + R.randint(-2, 2)
            for y in range(int(F.h * 0.3), F.h):
                F.px(x, y, mix(base, WH_DD, 0.45))
                F.px(x + 1, y, mix(base, WH_L, 0.5))
        if ink: outline()(F)
    return f


def stripes(base=WH, ys=((0.3, RED), (0.55, GRN)), th=2):
    """white band with red / green rings (fractions of the face height)"""
    def f(F):
        cloth(base, WH_D, 1)(F)
        for fy, c in ys:
            F.rect(0, int(F.h * fy), F.w, th, c)
            F.rect(0, int(F.h * fy) + th, F.w, 1, mix(c, BLK, 0.4))
    return f


def hairp(F):
    cols = [R.random() for _ in range(F.w)]
    for x in range(F.w):
        for y in range(F.h):
            c = WH_L if cols[x] > 0.8 else mix(WH, WH_D, 0.55) if cols[x] < 0.14 else WH
            c = mix(c, WH_D, 0.5 * (y / max(1, F.h - 1)) ** 2)
            F.px(x, y, c)
    outline(WH_DD)(F)


def tipp(F):
    """hair spike: white, greyer toward the root (bottom), ink edges"""
    for y in range(F.h):
        for x in range(F.w):
            F.px(x, y, mix(WH_L, WH_D, (y / max(1, F.h - 1)) ** 1.5 * 0.7))
    F.rect(0, 0, 1, F.h, WH_DD); F.rect(F.w - 1, 0, 1, F.h, WH_DD)


def inkp(F):
    """ink-black limb: cool sheen streak, specks, a white highlight line (like the art's line-work)"""
    for y in range(F.h):
        for x in range(F.w):
            c = mix(BLK_L, BLK, min(1, y / max(1, F.h - 1) * 1.4))
            if R.random() < 0.05: c = BLK_L
            F.px(x, y, c)
    F.rect(max(1, F.w // 4), 1, max(1, F.w // 10), max(1, F.h - 3), mix(BLK_L, WH_DD, 0.3))


def clawp(F):
    for y in range(F.h):
        for x in range(F.w):
            F.px(x, y, mix(BLK_L, 0x5A5A66, (y / max(1, F.h - 1))))


def teethp(F):
    for y in range(F.h):
        for x in range(F.w):
            F.px(x, y, mix(TOOTH, TOOTH_D, y / max(1, F.h - 1) * 0.5))
    outline(0x50505A)(F)


def skinp(F):
    for y in range(F.h):
        for x in range(F.w):
            F.px(x, y, mix(SKIN, SKIN_D, 0.1 + 0.4 * y / max(1, F.h - 1)))


def face_upper(F):
    """upper face: char right = texel left. big round staring eye (char right), narrow crack-eye (char left),
    heavy brow shadow, cracks, the grin corners curling up the cheeks, upper teeth row at the bottom."""
    W, H = F.w, F.h
    skinp(F)
    F.rect(0, 0, W, 6, mix(SKIN_D, WH_DD, 0.4))  # hair shadow
    # right eye: dark socket + white ring + black pupil
    ex, ey = 17, 17
    F.disc(ex, ey, 8.0, LINE)
    F.disc(ex, ey, 6.6, 0x3A3A44)
    F.disc(ex, ey, 4.4, WH_L)
    F.disc(ex + 1, ey + 1, 2.4, BLK_D)
    F.disc(ex - 0.5, ey - 0.5, 0.9, 0xEFFFFF, glow=True)
    F.line(ex - 9, ey - 10, ex + 7, ey - 8, LINE, 1.5)
    # left eye: squinted crescent
    lx, ly = W - 17, 18
    F.poly([(lx - 8, ly), (lx, ly - 4), (lx + 8, ly - 1), (lx + 1, ly + 2)], LINE)
    F.disc(lx + 1, ly - 1, 1.0, 0xEFFFFF, glow=True)
    F.line(lx - 8, ly - 9, lx + 8, ly - 6, LINE, 1.5)
    # cracks
    F.line(lx + 2, ly + 3, lx + 6, ly + 9, WH_DD); F.line(lx + 6, ly + 9, lx + 4, ly + 13, WH_DD)
    F.line(ex - 3, 2, ex - 6, 8, WH_DD)
    # grin: mouth opening along the bottom, corners sweeping up the cheeks
    F.rect(4, H - 7, W - 8, 7, MOUTH)
    F.poly([(0, H - 16), (6, H - 7), (4, H), (0, H)], MOUTH)
    F.poly([(W, H - 16), (W - 6, H - 7), (W - 4, H), (W, H)], MOUTH)
    F.line(0, H - 17, 5, H - 8, LINE, 1.5); F.line(W - 1, H - 17, W - 6, H - 8, LINE, 1.5)
    # upper teeth (triangular, hanging)
    for i in range(9):
        tx = 6 + i * (W - 12) / 9
        F.poly([(tx, H - 7), (tx + (W - 12) / 9 - 0.5, H - 7), (tx + (W - 12) / 18, H - 1)], TOOTH)
    F.rect(4, H - 8, W - 8, 1, LINE)
    outline()(F)


def face_lower(F):
    """jaw front: lower teeth along the top, grin line, chin"""
    W, H = F.w, F.h
    skinp(F)
    F.rect(4, 0, W - 8, 6, MOUTH)
    F.poly([(0, 0), (4, 0), (5, 6), (0, 3)], MOUTH); F.poly([(W, 0), (W - 4, 0), (W - 5, 6), (W, 3)], MOUTH)
    for i in range(8):
        tx = 6 + i * (W - 12) / 8
        F.poly([(tx, 6), (tx + (W - 12) / 8 - 0.5, 6), (tx + (W - 12) / 16, 0)], TOOTH)
    F.rect(4, 6, W - 8, 1, LINE)
    F.line(W // 2 - 3, H - 4, W // 2 + 3, H - 4, WH_DD)
    F.line(8, 9, 12, 14, WH_DD)  # crack
    outline()(F)


def featherp(band):
    def f(F):
        for y in range(F.h):
            for x in range(F.w):
                fy = y / max(1, F.h - 1)
                c = band[min(len(band) - 1, int(fy * len(band)))]
                F.px(x, y, c)
        F.rect(F.w // 2, 0, 1, F.h, mix(WH_L, LINE, 0.4))  # quill
        for y in range(2, F.h, 4):
            F.px(0, y, WH_L); F.px(F.w - 1, y + 1, WH_L)  # ragged barbs
    return f


def pocketp(F):
    inkp(F)
    F.rect(1, 1, F.w - 2, 1, mix(BLK_L, WH_DD, 0.4)); F.rect(1, 1, 1, F.h - 2, mix(BLK_L, WH_DD, 0.4))
    F.rect(F.w - 2, 1, 1, F.h - 2, mix(BLK_L, WH_DD, 0.4)); F.rect(1, F.h - 2, F.w - 2, 1, mix(BLK_L, WH_DD, 0.4))


def seamp(F):
    inkp(F)
    F.rect(F.w // 2, 0, 1, F.h, mix(BLK_L, WH_DD, 0.35))


# ------------------------------------------------------------------ skeleton
m.group("root", (0, 0, 0))
m.group("body", (0, 21, 0), parent="root")
m.group("chest", (0, 23, 0), parent="body")
m.group("hem_f", (0, 22.6, -2.6), parent="chest")
m.group("hem_b", (0, 22.6, 2.6), parent="chest")
m.group("cape", (0, 32.2, 2.6), parent="chest")
m.group("head", (0, 34.0, -0.3), parent="chest")
m.group("jaw", (0, 37.0, 1.6), parent="head")
m.group("hair_b", (0, 40.5, 3.0), parent="head")
m.group("hair_top", (0, 42.0, 0), parent="head")
m.group("bangs", (0, 41.6, -3.8), parent="head")
m.group("feather", (2.4, 42.2, 0.4), parent="head")
m.group("swirl", (-4.6, 21.6, 1.0), parent="body")
m.group("swirl2", (-5.6, 16.6, 1.6), parent="swirl")
m.group("arm_r", (4.9, 32.2, 0), parent="chest")
m.group("fore_r", (5.2, 26.4, 0), parent="arm_r")
m.group("hand_r", (5.3, 20.8, 0), parent="fore_r")
m.group("arm_l", (-5.6, 32.4, 0), parent="chest")
m.group("fore_l", (-6.6, 24.8, 0), parent="arm_l")
m.group("hand_l", (-6.9, 17.4, 0), parent="fore_l")
m.group("fingers_l", (-6.9, 13.8, -0.6), parent="hand_l")
m.group("thumb_l", (-4.6, 15.8, -1.4), parent="hand_l")
for s, k in ((1, "r"), (-1, "l")):
    m.group("leg_" + k, (2.3 * s, 21.0, 0), parent="root")
    m.group("shin_" + k, (2.4 * s, 12.6, 0), parent="leg_" + k)
    m.group("foot_" + k, (2.4 * s, 3.0, 0.2), parent="shin_" + k)

# ------------------------------------------------------------------ legs: black baggy trousers, white striped warmers, black pointed boots
for s, k in ((1, "r"), (-1, "l")):
    x = 2.4 * s
    m.cube("thigh_" + k, "leg_" + k, (x - 2.4, 12.4, -2.5), (x + 2.4, 21.4, 2.5), BLK, faces=all_faces(seamp, ("up",)))
    m.cube("crease_" + k, "leg_" + k, (x - 2.5, 15.6, -2.6), (x + 2.5, 16.0, 2.6), BLK_L)
    m.cube("tcuff_" + k, "leg_" + k, (x - 2.7, 12.0, -2.8), (x + 2.7, 13.4, 2.8), BLK_L, color2=BLK, grad=True, faces=all_faces(outline(BLK_D), ("up",)))
    m.cube("warm_" + k, "shin_" + k, (x - 2.0, 6.0, -2.0), (x + 2.0, 12.4, 2.0), WH, faces=all_faces(stripes(ys=((0.18, RED), (0.42, GRN), (0.72, RED))), ("up",)))
    m.cube("warm_bag_" + k, "shin_" + k, (x - 2.3, 3.0, -2.3), (x + 2.3, 6.4, 2.3), WH, faces=all_faces(stripes(ys=((0.35, GRN),)), ("up",)))
    for i in range(3):  # ruffled bottom of the warmers
        a = math.radians(i * 120 + 30 * s)
        px, pz = x + math.cos(a) * 2.0, math.sin(a) * 2.0
        m.cube(f"ruf{i}_" + k, "shin_" + k, (px - 0.7, 2.6, pz - 0.5), (px + 0.7, 4.2, pz + 0.5), WH_D, origin=(px, 4, pz),
               rot=(12 * math.sin(a), 0, -12 * math.cos(a)), faces=all_faces(outline(WH_DD)))
    m.cube("boot_" + k, "foot_" + k, (x - 1.7, 0.0, -2.2), (x + 1.7, 3.2, 2.0), BLK, faces=all_faces(inkp))
    m.cube("toe_" + k, "foot_" + k, (x - 1.3, 0.0, -4.6), (x + 1.3, 2.0, -1.8), BLK, faces=all_faces(inkp))
    m.cube("toetip_" + k, "foot_" + k, (x - 0.6, 0.6, -6.6), (x + 0.6, 1.6, -4.2), BLK_L, origin=(x, 1.0, -4.4), rot=(-18, 0, 0))
    m.cube("heel_" + k, "foot_" + k, (x - 0.9, 0.0, 1.4), (x + 0.9, 1.4, 2.6), BLK_D)
    m.cube("sole_" + k, "foot_" + k, (x - 1.8, -0.05, -4.7), (x + 1.8, 0.4, 2.7), 0x2C2C34)

# ------------------------------------------------------------------ hips / overall bib / straps
m.cube("hips", "body", (-4.6, 19.0, -2.7), (4.6, 23.4, 2.7), BLK, faces=all_faces(inkp))
m.cube("belt", "body", (-4.7, 22.6, -2.8), (4.7, 23.4, 2.8), BLK_L)
m.cube("bib", "chest", (-3.2, 22.8, -2.9), (3.2, 27.6, -2.5), BLK, faces={"north": pocketp})
m.cube("pocket", "chest", (-1.6, 23.6, -3.05), (1.6, 26.0, -2.85), BLK_L, faces={"north": pocketp})
for s, k in ((1, "r"), (-1, "l")):
    m.cube("strap_" + k, "chest", (2.2 * s - 0.5, 27.2, -2.8), (2.2 * s + 0.5, 33.2, -2.45), BLK)
    m.cube("strapb_" + k, "chest", (2.2 * s - 0.5, 23.0, 2.45), (2.2 * s + 0.5, 33.2, 2.8), BLK)
    m.cube("button_" + k, "chest", (2.2 * s - 0.35, 27.0, -3.0), (2.2 * s + 0.35, 27.7, -2.75), WH_DD)

# ------------------------------------------------------------------ torso: white shirt, collar, jagged hem, jagged back flaps
m.cube("torso", "chest", (-4.3, 22.4, -2.5), (4.3, 33.4, 2.5), WH,
       faces={"north": cloth(n=2), "south": cloth(n=3), "east": cloth(n=1), "west": cloth(n=1)})
m.cube("shirt_shadow", "chest", (-4.32, 29.0, -2.6), (-2.6, 33.4, -2.5), WH_D)
m.cube("neck", "chest", (-1.3, 32.8, -1.2), (1.3, 35.2, 1.4), SKIN_D)
for s, k in ((1, "r"), (-1, "l")):
    m.cube("collar_" + k, "chest", (0.2 if s > 0 else -2.8, 32.2, -3.0), (2.8 if s > 0 else -0.2, 34.0, -2.3), WH_L, color2=WH, grad=True,
           origin=(1.4 * s, 33.4, -2.6), rot=(-18, 0, -24 * s), faces={"north": outline()})
    m.cube("collar_bk_" + k, "chest", (0.2 if s > 0 else -3.4, 32.8, -2.3), (3.4 if s > 0 else -0.2, 34.4, 2.4), WH, origin=(1.6 * s, 33.4, 0),
           rot=(0, 0, 10 * s), faces=all_faces(outline()))
for i in range(7):  # jagged torn hem, front
    x = -3.8 + i * 1.27
    ln = 1.6 + (i % 3) * 0.8
    m.cube(f"hemf{i}", "hem_f", (x - 0.75, 22.4 - ln, -2.85), (x + 0.75, 22.8, -2.45), WH if i % 2 else WH_L, origin=(x, 22.6, -2.6),
           rot=(4, 0, (i - 3) * 6), faces={"north": combo(cloth(n=1, ink=False), outline(WH_DD)), "south": outline(WH_DD)})
for i in range(7):
    x = -3.8 + i * 1.27
    ln = 1.4 + ((i + 1) % 3) * 0.9
    m.cube(f"hemb{i}", "hem_b", (x - 0.75, 22.4 - ln, 2.45), (x + 0.75, 22.8, 2.85), WH_D if i % 2 else WH, origin=(x, 22.6, 2.6),
           rot=(-4, 0, (i - 3) * 6), faces={"south": combo(cloth(n=1, ink=False), outline(WH_DD))})
# the jagged white "star" flaps flaring out behind the shoulders (art: big spiky shape behind his right side)
for i, (x, ln, rx, rz) in enumerate([(3.0, 9.0, 28, -40), (1.2, 7.0, 32, -18), (-0.8, 6.0, 30, 6), (-2.6, 5.2, 26, 26), (3.8, 6.0, 14, -70)]):
    m.cube(f"flap{i}", "cape", (x - 0.9, 32.2 - ln, 2.4), (x + 0.9, 32.4, 2.9), WH if i % 2 else WH_L, origin=(x, 32.2, 2.6),
           rot=(rx, 0, rz), faces=all_faces(combo(cloth(n=1, ink=False), outline(WH_DD))))
    m.cube(f"flapt{i}", "cape", (x - 0.4, 32.2 - ln - 2.4, 2.45), (x + 0.4, 32.2 - ln + 0.2, 2.85), WH_D, origin=(x, 32.2, 2.6),
           rot=(rx, 0, rz), faces=all_faces(outline(WH_DD)))

# ------------------------------------------------------------------ swirl ribbons at the left hip
for i, (dx, dy, ln, rz) in enumerate([(0, 0, 5.2, -24), (-1.0, -0.2, 4.0, 10)]):
    m.cube(f"sw_a{i}", "swirl", (-4.9 + dx - 0.5, 21.6 - ln + dy, 0.4 + i * 0.6), (-4.9 + dx + 0.5, 21.6 + dy, 1.0 + i * 0.6), WH, origin=(-4.6, 21.6, 1.0),
           rot=(-8, 0, rz), faces=all_faces(outline(WH_DD)))
for i, (ln, rz) in enumerate([(3.0, 70), (2.4, 130), (2.0, 190)]):
    m.cube(f"sw_b{i}", "swirl2", (-5.6 - 0.45, 16.6 - ln, 1.3), (-5.6 + 0.45, 16.6, 1.9), WH if i % 2 else WH_L, origin=(-5.6, 16.6, 1.6),
           rot=(0, 0, rz), faces=all_faces(outline(WH_DD)))
m.cube("sw_curl", "swirl2", (-4.6, 13.6, 1.2), (-3.2, 15.0, 2.0), WH, faces=all_faces(outline(WH_DD)))

# ------------------------------------------------------------------ head: skull (eyes, upper grin), jaw (lower teeth), mouth cavity
m.cube("skull", "head", (-3.8, 37.0, -4.0), (3.8, 42.0, 3.0), SKIN, faces={"north": face_upper, "east": skinp, "west": skinp, "south": hairp, "up": hairp})
m.cube("maw_in", "head", (-3.4, 34.8, -3.8), (3.4, 37.4, 1.6), MOUTH, faces=all_faces(lambda F: F.rect(0, 0, F.w, F.h, GUM if R.random() < 0.3 else MOUTH)))
m.cube("jaw_base", "jaw", (-3.7, 34.4, -4.05), (3.7, 37.1, 2.0), SKIN, faces={"north": face_lower, "east": skinp, "west": skinp, "down": skinp,
                                                                           "up": lambda F: F.rect(0, 0, F.w, F.h, MOUTH)})
m.cube("tongue", "jaw", (-1.6, 36.6, -3.4), (1.6, 37.2, 0.4), GUM, color2=MOUTH, grad=True)
for s in (1, -1):  # cheek cracks splitting toward the ears (grin goes ear to ear)
    m.cube(f"cheek_{s}", "head", (3.75 * s - 0.1, 36.4, -3.6), (3.75 * s + 0.1, 38.6, -1.0), MOUTH, origin=(3.8 * s, 37.5, -2.3), rot=(-20, 0, 0))
# ------------------------------------------------------------------ hair: cap + ~26 sharp spikes + bangs + back spikes + feathers
m.cube("hair_cap", "head", (-4.3, 41.0, -4.4), (4.3, 43.0, 3.6), WH, faces=all_faces(hairp))
m.cube("hair_side_r", "head", (3.6, 36.4, -3.0), (4.5, 40.4, 3.2), WH, faces=all_faces(hairp))
m.cube("hair_side_l", "head", (-4.5, 36.4, -3.0), (-3.6, 40.4, 3.2), WH, faces=all_faces(hairp))


def spike(name, parent, base, ln, w, rx, rz, ry=0, col=WH):
    x, y, z = base
    m.cube(name, parent, (x - w / 2, y, z - w / 2), (x + w / 2, y + ln * 0.6, z + w / 2), col, origin=base, rot=(rx, ry, rz), faces=all_faces(tipp))
    m.cube(name + "t", parent, (x - w / 4, y + ln * 0.5, z - w / 4), (x + w / 4, y + ln, z + w / 4), WH_L, origin=base, rot=(rx, ry, rz), faces=all_faces(tipp))


# crown spikes radiating up/out (bigger toward the char's right, like the art)
for i in range(9):
    a = math.radians(i * 40 + 10)
    cx, cz = math.cos(a) * 2.8, math.sin(a) * 2.6 + 0.2
    ln = 5.4 + (2.2 if cx > 0.5 else 0) + R.uniform(0, 1.6)
    tilt = 46 + R.uniform(-8, 10)
    rx = math.sin(a) * tilt if math.sin(a) > -0.3 else 12  # front spikes lean BACK so the face stays clear
    spike(f"crown{i}", "hair_top", (cx, 41.6, cz), ln, 2.5, rx, -math.cos(a) * tilt, col=WH if i % 2 else WH_L)
for i in range(4):
    spike(f"top{i}", "hair_top", (-1.5 + i * 1.0, 42.4, 0.4 + (i % 2)), 4.2 + (i % 2) * 1.5, 2.2, (i - 1.5) * 8, -18 + i * 10)
# big side spikes sticking out sideways (silhouette)
for i, (s, y, z, ln, tilt) in enumerate([(1, 39.0, -1.5, 7.0, 76), (1, 37.6, 0.8, 5.6, 92), (-1, 39.2, -0.8, 5.6, 72), (-1, 37.8, 1.2, 4.4, 96), (1, 40.6, 1.6, 6.0, 60)]):
    spike(f"side{i}", "head", (3.8 * s, y, z), ln, 1.7, 0, -tilt * s)
# back spikes hanging down the nape
for i in range(5):
    x = -3.2 + i * 1.6
    spike(f"back{i}", "hair_b", (x, 40.6, 3.2), 6.0 + (i % 2) * 1.6, 1.8, 150 - (i % 2) * 14, (i - 2) * -14)
# bangs: sharp spikes over the forehead, gap over the eyes
for i, (x, ln, rz) in enumerate([(-3.6, 3.4, -14), (-0.2, 2.0, 0), (3.6, 4.0, 16)]):
    spike(f"bang{i}", "bangs", (x, 42.2, -4.3), ln, 1.6, 172, rz)
# feathers (teal / white / red / black bands) stuck in the hair, char's right, pointing up and out
for i, (dx, ln, rz, rx, band) in enumerate([(0.0, 9.0, -34, -10, [WH_L, TEAL, TEAL, BLK, WH_L, TEAL_D]),
                                           (1.2, 7.6, -58, 6, [RED, WH_L, BLK, TEAL, RED, BLK])]):
    x = 2.4 + dx
    m.cube(f"feather{i}", "feather", (x - 0.8, 42.2, 0.2 + i * 0.5), (x + 0.8, 42.2 + ln, 0.5 + i * 0.5), TEAL, origin=(x, 42.2, 0.4),
           rot=(rx, 0, rz), faces={"north": featherp(band), "south": featherp(band), "east": outline(), "west": outline()})
    m.cube(f"quill{i}", "feather", (x - 0.15, 41.0, 0.25 + i * 0.5), (x + 0.15, 42.4, 0.45 + i * 0.5), WH_D, origin=(x, 42.2, 0.4), rot=(rx, 0, rz))
m.cube("feather_band", "feather", (1.6, 41.6, -0.4), (4.4, 42.6, 1.6), BLK, origin=(3, 42, 0.6), rot=(0, 0, -20))

# ------------------------------------------------------------------ right arm: striped short sleeve, pale thin arm, long fingers
m.cube("sleeve_r", "arm_r", (3.5, 28.0, -1.9), (7.0, 33.6, 1.9), WH, origin=(5, 31, 0), rot=(0, 0, 6),
       faces=all_faces(stripes(ys=((0.62, RED), (0.8, GRN))), ("up",)))
m.cube("uarm_r", "arm_r", (4.25, 25.6, -1.0), (6.15, 28.6, 1.0), SKIN, faces=all_faces(skinp))
m.cube("elbow_r", "fore_r", (4.15, 25.0, -1.05), (6.25, 26.8, 1.05), SKIN_D)
m.cube("farm_r", "fore_r", (4.3, 21.2, -0.95), (6.1, 25.6, 0.95), SKIN, faces=all_faces(skinp))
m.cube("wband_r", "fore_r", (4.15, 21.0, -1.1), (6.25, 21.8, 1.1), BLK)
m.cube("palm_r", "hand_r", (4.35, 18.6, -1.2), (6.05, 21.2, 1.0), SKIN, faces=all_faces(skinp))
for i in range(4):
    z = -0.9 + i * 0.6
    m.cube(f"fing{i}_r", "hand_r", (5.4 - 0.25, 15.6 + (i % 2) * 0.4, z - 0.25), (5.4 + 0.25, 18.8, z + 0.25), SKIN_D, origin=(5.4, 18.7, z), rot=(-8, 0, 4))
    m.cube(f"nail{i}_r", "hand_r", (5.4 - 0.22, 15.0 + (i % 2) * 0.4, z - 0.22), (5.4 + 0.22, 15.9 + (i % 2) * 0.4, z + 0.22), BLK, origin=(5.4, 18.7, z), rot=(-8, 0, 4))
m.cube("thumb_r", "hand_r", (4.3, 18.0, -1.6), (4.8, 20.0, -1.1), SKIN_D, origin=(4.6, 19.8, -1.2), rot=(-20, 0, 16))

# ------------------------------------------------------------------ LEFT arm: huge ink-black clawed limb out of a striped sleeve
m.cube("sleeve_l", "arm_l", (-8.6, 28.4, -2.4), (-3.6, 34.0, 2.4), WH, origin=(-5.6, 31, 0), rot=(0, 0, -8),
       faces=all_faces(stripes(ys=((0.6, RED), (0.78, GRN))), ("up",)))
m.cube("shoulder_l", "arm_l", (-8.0, 26.0, -2.0), (-4.0, 30.0, 2.0), BLK, faces=all_faces(inkp))
m.cube("uarm_l", "arm_l", (-7.8, 23.6, -1.9), (-4.4, 27.4, 1.9), BLK, faces=all_faces(inkp))
for i, (y, z) in enumerate([(27.6, 0.6), (25.4, -0.4)]):  # ink drips / jagged ridge on the back of the arm
    m.cube(f"ridge{i}_l", "arm_l", (-8.4, y - 1.0, z - 0.5), (-7.4, y + 1.0, z + 0.5), BLK_L, origin=(-7.8, y, z), rot=(0, 0, 30))
m.cube("elbow_l", "fore_l", (-8.6, 22.6, -2.3), (-4.6, 25.8, 2.4), BLK, faces=all_faces(inkp))
m.cube("elbow_spike", "fore_l", (-7.4, 22.8, 1.8), (-6.2, 25.0, 4.2), BLK_L, origin=(-6.8, 24, 2.2), rot=(-35, 0, 0))
m.cube("farm_l", "fore_l", (-9.4, 17.6, -2.7), (-4.4, 23.2, 2.7), BLK, faces=all_faces(inkp))
m.cube("farm_vein", "fore_l", (-9.5, 18.4, -1.0), (-9.3, 22.6, -0.6), mix(BLK_L, WH_DD, 0.4))
m.cube("cuff_stripe_l", "fore_l", (-9.55, 22.2, -2.85), (-4.25, 22.7, 2.85), RED)
m.cube("cuff_stripe2_l", "fore_l", (-9.55, 21.5, -2.85), (-4.25, 22.0, 2.85), GRN)
for i in range(3):  # jagged spines along the forearm (outer side)
    y = 18.6 + i * 1.6
    m.cube(f"fspine{i}_l", "fore_l", (-10.6, y - 0.45, -0.4 + i * 0.5), (-8.8, y + 0.45, 0.4 + i * 0.5), BLK_L, origin=(-9.2, y, i * 0.5), rot=(0, 0, -24))
m.cube("palm_l", "hand_l", (-9.8, 13.6, -2.9), (-3.9, 17.8, 2.6), BLK, faces=all_faces(inkp))
m.cube("knuckles_l", "hand_l", (-9.9, 13.2, -3.1), (-3.8, 14.4, 1.2), BLK_L, color2=BLK, grad=True)
for i in range(4):  # four long jointed claws, knuckles at fingers_l pivot
    x = -9.1 + i * 1.5
    m.cube(f"fbase{i}_l", "fingers_l", (x - 0.55, 10.2, -2.6 + i * 0.1), (x + 0.55, 14.0, -1.4 + i * 0.1), BLK, origin=(x, 13.8, -2.0), rot=(-6, 0, (i - 1.5) * -5),
           faces=all_faces(inkp))
    m.cube(f"fmid{i}_l", "fingers_l", (x - 0.45, 7.6, -2.9 + i * 0.1), (x + 0.45, 10.6, -1.9 + i * 0.1), BLK, origin=(x, 10.4, -2.4), rot=(-16, 0, (i - 1.5) * -6),
           faces=all_faces(inkp))
    m.cube(f"talon{i}_l", "fingers_l", (x - 0.3, 4.6, -3.6 + i * 0.1), (x + 0.3, 8.0, -2.8 + i * 0.1), BLK_L, origin=(x, 7.8, -2.6), rot=(-26, 0, (i - 1.5) * -7),
           faces=all_faces(clawp))
m.cube("thumb_base_l", "thumb_l", (-4.4, 13.2, -2.0), (-3.4, 16.0, -0.9), BLK, origin=(-4.0, 15.8, -1.4), rot=(-10, 0, 22), faces=all_faces(inkp))
m.cube("thumb_claw_l", "thumb_l", (-3.8, 10.8, -2.4), (-3.2, 13.6, -1.6), BLK_L, origin=(-4.0, 15.8, -1.4), rot=(-20, 0, 26), faces=all_faces(clawp))
m.cube("pinky_l", "hand_l", (-10.4, 12.2, -0.4), (-9.4, 15.6, 0.6), BLK, origin=(-9.8, 15.4, 0), rot=(0, 0, -16), faces=all_faces(inkp))
m.cube("pinky_claw_l", "hand_l", (-10.9, 9.6, -0.3), (-10.3, 12.6, 0.4), BLK_L, origin=(-9.8, 15.4, 0), rot=(-8, 0, -22), faces=all_faces(clawp))


# ================================================================== animation
HIDE = (.001, .001, .001)

REST = {
    "chest": (-6, 0, 0), "head": (6, 0, 0), "jaw": (0, 0, 0),
    "arm_r": (6, 0, 6), "fore_r": (16, 0, 0), "hand_r": (0, 0, 0),
    "arm_l": (8, 0, -8), "fore_l": (14, 0, 4), "hand_l": (4, 0, 0), "fingers_l": (14, 0, 0), "thumb_l": (0, 0, 0),
    "leg_r": (4, 0, 2), "shin_r": (-6, 0, 0), "foot_r": (2, 0, 0),
    "leg_l": (2, 0, -3), "shin_l": (-4, 0, 0), "foot_l": (2, 0, 0),
    "hem_f": (0, 0, 0), "hem_b": (0, 0, 0), "cape": (0, 0, 0), "swirl": (0, 0, -6), "swirl2": (0, 0, 10),
}


def rest(b):
    return REST.get(b, (0, 0, 0))


class A:
    def __init__(self, name, ticks, loop=False, additive=False):
        self.name, self.ticks, self.loop, self.tr, self.additive = name, ticks, loop, {}, additive

    def k(self, bone, ch, keys):
        self.tr.setdefault(bone, {}).setdefault(ch, []).extend(keys)
        return self

    def rot(self, bone, *keys): return self.k(bone, "rotation", keys)
    def pos(self, bone, *keys): return self.k(bone, "position", keys)
    def scl(self, bone, *keys): return self.k(bone, "scale", keys)

    def r(self, bone, *keys):
        """absolute rotation keys framed by the rest pose at 0 and at the end"""
        ks = list(keys)
        base = (0, 0, 0) if self.additive else rest(bone)
        if ks[0][0] > 0: ks.insert(0, (0, *base))
        if ks[-1][0] < self.ticks: ks.append((self.ticks, *base))
        return self.rot(bone, *ks)

    def d(self, bone, *keys):
        """rotation keys as DELTAS from the rest pose"""
        rx, ry, rz = (0, 0, 0) if self.additive else rest(bone)
        return self.r(bone, *[(t, x + rx, y + ry, z + rz) for (t, x, y, z) in keys])

    def drape(self, bone, keys, delay=2):
        bx, by, bz = (0, 0, 0) if self.additive else rest(bone)
        seen, out = set(), []
        for (t, x, y, z) in keys:
            tt = min(self.ticks, t + delay)
            if tt in seen: continue
            seen.add(tt); out.append((tt, bx + x, by + y, bz + z))
        if out[0][0] > 0: out.insert(0, (0, bx, by, bz))
        return self.rot(bone, *out)

    def hair(self, keys, delay=2):
        """x>0 = hair flicks forward, z>0 = toward +X"""
        self.drape("hair_b", [(t, x * 0.8, 0, z * 0.5) for (t, x, y, z) in keys], delay)
        self.drape("hair_top", [(t, x * 0.4, 0, z * 0.5) for (t, x, y, z) in keys], delay)
        self.drape("bangs", [(t, x * 0.4, 0, z * 0.3) for (t, x, y, z) in keys], delay)
        self.drape("feather", [(t, x * 0.9, 0, z * 1.0) for (t, x, y, z) in keys], delay + 1)
        return self

    def cloth(self, keys, delay=2):
        """x>0 = shirt tails / flaps kick forward, z>0 = toward +X"""
        self.drape("hem_f", [(t, x, 0, z * 0.4) for (t, x, y, z) in keys], delay)
        self.drape("hem_b", [(t, x * 0.8, 0, z * 0.4) for (t, x, y, z) in keys], delay)
        self.drape("cape", [(t, x * 0.7, 0, z * 0.6) for (t, x, y, z) in keys], delay + 1)
        self.drape("swirl", [(t, x * 0.8, 0, z) for (t, x, y, z) in keys], delay + 1)
        self.drape("swirl2", [(t, x * 1.2, 0, z * 1.4) for (t, x, y, z) in keys], delay + 3)
        return self

    def done(self):
        if not self.additive:
            for b, v in REST.items():
                if b not in self.tr or "rotation" not in self.tr[b]:
                    self.rot(b, (0, *v))
        tracks = {b: {ch: sorted([(t / 20.0, x, y, z) for (t, x, y, z) in v], key=lambda q: q[0]) for ch, v in chs.items()}
                  for b, chs in self.tr.items()}
        m.anim(self.name, self.ticks / 20.0, tracks, loop=self.loop)


def bodyp(a, *keys):
    ks = list(keys)
    if ks[0][0] > 0: ks.insert(0, (0, 0, 0, 0))
    if ks[-1][0] < a.ticks: ks.append((a.ticks, 0, 0, 0))
    a.pos("body", *ks)


def legs(a, kr, kl=None, sr=None, sl=None, fr=None, fl=None):
    a.d("leg_r", *kr)
    a.d("leg_l", *(kl or [(t, x, -y, -z) for (t, x, y, z) in kr]))
    if sr: a.d("shin_r", *sr)
    if sl or sr: a.d("shin_l", *(sl or sr))
    if fr: a.d("foot_r", *fr)
    if fl or fr: a.d("foot_l", *(fl or fr))


def claw(a, *keys):
    """finger curl deltas: x>0 = curl into a fist, x<0 = splay open"""
    a.d("fingers_l", *keys)
    a.d("thumb_l", *[(t, x * 0.5, 0, -x * 0.4) for (t, x, y, z) in keys])


# ------------------------------------------------------------------ idle (80 loop): slow lanky sway, claw flexes, hand-over-face grin, head tilt
a = A("idle", 80, loop=True)
a.pos("body", (0, 0, 0, 0), (20, 0, -0.3, 0), (40, 0, 0, 0), (60, 0, -0.3, 0), (80, 0, 0, 0))
a.d("chest", (0, 0, 0, 0), (20, 2, 2, 1), (40, 0, 0, 0), (60, 2, -2, -1), (80, 0, 0, 0))
a.d("head", (0, 0, 0, 0), (14, -6, -6, -8), (30, -6, -6, -8), (40, 0, 0, 0), (52, 2, 6, 18), (54, 0, 8, 22), (62, 0, 8, 20), (70, 0, 0, 0), (80, 0, 0, 0))
a.d("jaw", (0, 0, 0, 0), (12, -10, 0, 0), (18, -2, 0, 0), (22, -10, 0, 0), (30, 0, 0, 0), (52, 0, 0, 0), (54, -14, 0, 0), (56, -4, 0, 0), (58, -12, 0, 0),
    (64, 0, 0, 0), (80, 0, 0, 0))
# right hand drifts up over the face (the art's pose), fingers spread, then drops
a.d("arm_r", (0, 0, 0, 0), (8, 6, 0, 0), (14, 56, -14, -26), (30, 58, -14, -28), (38, 4, 0, 0), (80, 0, 0, 0))
a.d("fore_r", (0, 0, 0, 0), (8, 8, 0, 0), (14, 92, 0, 0), (30, 94, 0, 0), (38, 4, 0, 0), (80, 0, 0, 0))
a.d("hand_r", (0, 0, 0, 0), (14, 10, 0, 0), (30, 10, 0, 0), (38, 0, 0, 0), (80, 0, 0, 0))
a.d("arm_l", (0, 0, 0, 0), (20, 3, 0, -1), (40, -2, 0, 1), (60, 4, 0, -2), (80, 0, 0, 0))
a.d("fore_l", (0, 0, 0, 0), (40, 6, 0, 0), (80, 0, 0, 0))
claw(a, (0, 0, 0, 0), (40, 0, 0, 0), (44, -26, 0, 0), (47, 30, 0, 0), (50, -14, 0, 0), (54, 20, 0, 0), (60, 0, 0, 0), (80, 0, 0, 0))
legs(a, [(0, 0, 0, 0), (40, 1, 0, 1), (80, 0, 0, 0)], [(0, 0, 0, 0), (40, -1, 0, -1), (80, 0, 0, 0)])
a.drape("hair_b", [(0, 0, 0, 1), (20, -2, 0, 0), (40, 0, 0, -1), (54, 2, 0, -5), (62, 0, 0, 2), (80, 0, 0, 1)], 3)
a.drape("feather", [(0, 0, 0, 0), (20, -4, 0, 3), (40, 0, 0, -2), (56, 4, 0, -8), (64, -2, 0, 4), (80, 0, 0, 0)], 4)
a.cloth([(0, 1, 0, 1), (40, -1, 0, -1), (80, 1, 0, 1)], 4)
a.done()

# ------------------------------------------------------------------ walk (20 loop, additive over idle): long loping stride, heavy claw arm swinging late
a = A("walk", 20, loop=True, additive=True)
a.d("leg_r", (0, 30, 0, 0), (5, 2, 0, 0), (10, -26, 0, 0), (15, 2, 0, 0), (20, 30, 0, 0))
a.d("shin_r", (0, 0, 0, 0), (5, -4, 0, 0), (10, -4, 0, 0), (13, -46, 0, 0), (17, -26, 0, 0), (20, 0, 0, 0))
a.d("foot_r", (0, -14, 0, 0), (5, -4, 0, 0), (10, 12, 0, 0), (14, 18, 0, 0), (20, -14, 0, 0))
a.d("leg_l", (0, -26, 0, 0), (5, 2, 0, 0), (10, 30, 0, 0), (15, 2, 0, 0), (20, -26, 0, 0))
a.d("shin_l", (0, -4, 0, 0), (3, -46, 0, 0), (7, -26, 0, 0), (10, 0, 0, 0), (15, -4, 0, 0), (20, -4, 0, 0))
a.d("foot_l", (0, 12, 0, 0), (4, 18, 0, 0), (10, -14, 0, 0), (15, -4, 0, 0), (20, 12, 0, 0))
a.pos("body", (0, 0, -0.6, 0), (5, 0, 0.4, 0), (10, 0, -0.6, 0), (15, 0, 0.4, 0), (20, 0, -0.6, 0))
a.rot("body", (0, 0, 7, -2), (10, 0, -7, 2), (20, 0, 7, -2))
a.d("chest", (0, -3, -6, 3), (5, -1, 0, 0), (10, -3, 6, -3), (15, -1, 0, 0), (20, -3, -6, 3))
a.d("head", (0, 2, 4, -3), (5, -2, 0, 0), (10, 2, -4, 3), (15, -2, 0, 0), (20, 2, 4, -3))
a.d("arm_r", (0, -24, 0, 0), (10, 26, 0, 0), (20, -24, 0, 0))
a.d("fore_r", (0, 4, 0, 0), (10, 18, 0, 0), (20, 4, 0, 0))
a.d("arm_l", (0, 16, 0, 0), (3, 20, 0, 0), (13, -14, 0, 0), (20, 16, 0, 0))  # heavy, lagging
a.d("fore_l", (0, 6, 0, 0), (5, 14, 0, 0), (15, 0, 0, 0), (20, 6, 0, 0))
a.d("fingers_l", (0, -6, 0, 0), (5, 10, 0, 0), (15, -10, 0, 0), (20, -6, 0, 0))
a.drape("hair_b", [(0, -6, 0, 3), (5, -10, 0, 0), (10, -6, 0, -3), (15, -10, 0, 0), (20, -6, 0, 3)], 2)
a.drape("feather", [(0, -10, 0, 6), (5, -14, 0, 0), (10, -10, 0, -6), (15, -14, 0, 0), (20, -10, 0, 6)], 3)
a.drape("hem_f", [(0, 6, 0, 2), (5, 2, 0, 0), (10, 6, 0, -2), (15, 2, 0, 0), (20, 6, 0, 2)], 2)
a.drape("cape", [(0, 8, 0, 3), (5, 12, 0, 0), (10, 8, 0, -3), (15, 12, 0, 0), (20, 8, 0, 3)], 3)
a.drape("swirl", [(0, -8, 0, 6), (10, 8, 0, -6), (20, -8, 0, 6)], 3)
a.drape("swirl2", [(0, -10, 0, 10), (10, 10, 0, -10), (20, -10, 0, 10)], 5)
a.done()

# ------------------------------------------------------------------ claw_swipe (26): claw cocked out wide 0-9, horizontal rake across t12, follow-through
a = A("claw_swipe", 26)
a.r("arm_l", (4, 40, 50, -40), (8, 70, 76, -36), (10, 76, 60, -20), (12, 84, -40, 0), (14, 80, -70, 6), (18, 64, -60, 0), (22, 30, -20, -6))
a.d("fore_l", (4, 20, 0, 0), (8, 30, 0, 0), (12, -4, 0, 0), (16, 0, 0, 0), (22, 10, 0, 0))
claw(a, (4, -30, 0, 0), (9, -40, 0, 0), (12, -10, 0, 0), (14, 20, 0, 0), (20, 10, 0, 0))
a.d("hand_l", (8, -20, 0, 0), (12, 10, 0, 0), (16, 20, 0, 0))
a.d("chest", (4, 2, 24, 0), (9, 4, 34, 2), (11, 0, 10, 0), (12, -6, -30, 0), (14, -8, -38, 0), (19, -4, -20, 0))
a.d("head", (4, 0, -16, 0), (9, -4, -22, 0), (12, 0, 18, 0), (14, 0, 24, 0), (20, 0, 8, 0))
a.d("jaw", (6, -16, 0, 0), (12, -24, 0, 0), (16, -8, 0, 0))
a.d("arm_r", (6, -20, 0, 20), (12, 20, 0, 30), (18, 0, 0, 10))
bodyp(a, (8, 0, -0.6, 0.4), (12, 0, -1.0, -1.2), (16, 0, -0.8, -1.0))
a.rot("body", (0, 0, 0, 0), (9, 0, 14, 0), (12, 0, -12, 0), (16, 0, -16, 0), (26, 0, 0, 0))
legs(a, [(8, -10, 0, 4), (12, 22, 0, 0), (18, 16, 0, 0)], [(8, 10, 0, -4), (12, -16, 0, 0), (18, -10, 0, 0)],
     sr=[(12, -20, 0, 0), (18, -14, 0, 0)], sl=[(12, -6, 0, 0)])
a.hair([(0, 0, 0, 0), (8, -4, 0, -10), (12, 4, 0, 14), (15, 0, 0, 10), (22, 0, 0, 0)], 1)
a.cloth([(0, 0, 0, 0), (9, 0, 0, -10), (13, -4, 0, 14), (20, 0, 0, 4), (26, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ claw_combo (36): backhand t9 (outward), forehand rake t17, overhead slam t27
a = A("claw_combo", 36)
a.r("arm_l", (4, 70, -60, 0), (7, 80, -70, 0), (9, 76, 50, -20), (11, 70, 70, -26), (14, 74, 60, -30), (17, 84, -40, 0), (19, 80, -64, 0),
    (22, 140, 0, -16), (24, 168, 0, -10), (26, 120, 0, -6), (27, 60, 0, -4), (30, 54, 0, -6), (34, 20, 0, -8))
a.d("fore_l", (4, 50, 0, 0), (9, 0, 0, 0), (14, 30, 0, 0), (17, 0, 0, 0), (22, 30, 0, 0), (27, -4, 0, 0), (31, 10, 0, 0))
claw(a, (4, 20, 0, 0), (8, -30, 0, 0), (12, 20, 0, 0), (16, -40, 0, 0), (19, 20, 0, 0), (23, -40, 0, 0), (27, 10, 0, 0), (32, 0, 0, 0))
a.d("hand_l", (8, 20, 0, 0), (17, -10, 0, 0), (24, -30, 0, 0), (27, 30, 0, 0), (32, 0, 0, 0))
a.d("chest", (4, 0, -26, 0), (7, 0, -32, 0), (9, -4, 26, 0), (12, -2, 30, 0), (17, -8, -30, 0), (20, 6, -10, 0), (24, 14, 0, 0), (27, -26, 0, 0),
    (30, -22, 0, 0), (34, -6, 0, 0))
a.d("head", (4, 0, 18, 0), (9, -4, -18, 0), (14, 0, -16, 0), (17, 0, 20, 0), (24, 10, 0, 0), (27, -12, 0, 0), (32, -2, 0, 0))
a.d("jaw", (4, -10, 0, 0), (9, -26, 0, 0), (13, -6, 0, 0), (17, -28, 0, 0), (22, -10, 0, 0), (27, -36, 0, 0), (32, -6, 0, 0))
a.d("arm_r", (4, 10, 0, 30), (9, -20, 0, 20), (17, 20, 0, 34), (24, -30, 0, 40), (27, 20, 0, 30), (32, 4, 0, 6))
bodyp(a, (7, 0, -0.4, 0), (9, 0, -0.6, -0.6), (17, 0, -0.8, -1.2), (24, 0, 0.6, -1.0), (27, 0, -2.0, -2.2), (31, 0, -1.6, -1.8))
a.rot("body", (0, 0, 0, 0), (7, 0, -12, 0), (9, 0, 12, 0), (14, 0, 12, 0), (17, 0, -14, 0), (22, 0, 0, 0), (36, 0, 0, 0))
legs(a, [(7, -8, 0, 0), (9, 14, 0, 0), (17, -12, 0, 0), (24, 6, 0, 4), (27, 30, 0, 0), (31, 26, 0, 0)],
     [(7, 8, 0, 0), (9, -12, 0, 0), (17, 14, 0, 0), (24, -4, 0, -4), (27, -24, 0, 0), (31, -20, 0, 0)],
     sr=[(9, -10, 0, 0), (27, -40, 0, 0), (31, -34, 0, 0)], sl=[(17, -10, 0, 0), (27, -10, 0, 0)])
a.hair([(0, 0, 0, 0), (7, 0, 0, 10), (10, 0, 0, -12), (15, 0, 0, -8), (18, 0, 0, 12), (24, -12, 0, 0), (28, 18, 0, 0), (32, 4, 0, 0), (36, 0, 0, 0)], 1)
a.cloth([(0, 0, 0, 0), (8, 0, 0, 10), (11, 0, 0, -12), (18, 0, 0, 12), (24, -8, 0, 0), (28, 14, 0, 0), (36, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ grab_slam (56): reach t12 (grab), hoist overhead 14-30, SLAM into the floor t36
a = A("grab_slam", 56)
a.r("arm_l", (5, 20, 30, -30), (9, 60, 10, -10), (12, 92, -8, 4), (16, 100, -6, 2), (22, 140, 0, -4), (28, 170, 0, -8), (30, 176, 0, -10),
    (33, 150, 0, -6), (36, 40, 0, 0), (40, 34, 0, 0), (46, 30, 0, -4), (52, 14, 0, -8))
a.d("fore_l", (5, 40, 0, 0), (9, 10, 0, 0), (12, 0, 0, 0), (16, 30, 0, 0), (28, 40, 0, 0), (33, 20, 0, 0), (36, -6, 0, 0), (44, 10, 0, 0))
claw(a, (5, -40, 0, 0), (10, -50, 0, 0), (12, 50, 0, 0), (36, 50, 0, 0), (38, -30, 0, 0), (44, -10, 0, 0), (50, 0, 0, 0))
a.d("hand_l", (9, -20, 0, 0), (12, 10, 0, 0), (28, 30, 0, 0), (33, -10, 0, 0), (36, 30, 0, 0), (44, 0, 0, 0))
a.d("chest", (5, 6, 20, 0), (9, -10, 4, 0), (12, -18, -6, 0), (16, -6, -4, 0), (22, 10, 0, -4), (28, 22, 0, -8), (30, 24, 0, -8), (33, 16, 0, -4),
    (36, -34, 0, 0), (40, -30, 0, 0), (46, -16, 0, 0), (52, -4, 0, 0))
a.d("head", (5, 0, -10, 0), (12, -6, 6, 0), (22, 16, 0, 6), (30, 22, 0, 10), (33, 14, 0, 4), (36, -14, 0, 0), (40, -16, 0, 0), (46, -4, 0, 0))
a.d("jaw", (5, -6, 0, 0), (12, -30, 0, 0), (16, -8, 0, 0), (24, -30, 0, 0), (30, -46, 0, 0), (36, -60, 0, 0), (40, -40, 0, 0), (48, -10, 0, 0))
a.d("arm_r", (5, -10, 0, 20), (12, -30, 0, 30), (22, -10, 0, 50), (30, -20, 0, 60), (36, 20, 0, 30), (44, 6, 0, 10))
a.d("fore_r", (12, 30, 0, 0), (30, 50, 0, 0), (36, 10, 0, 0))
bodyp(a, (5, 0, -0.6, 0.6), (10, 0, -1.0, -1.4), (12, 0, -1.2, -2.0), (18, 0, -0.4, -0.8), (28, 0, 0.6, 0), (33, 0, 0.8, 0), (36, 0, -2.6, -1.6),
      (40, 0, -2.4, -1.4), (48, 0, -0.8, -0.4))
a.rot("body", (0, 0, 0, 0), (5, 0, 12, 0), (12, 0, -4, 0), (28, 0, 0, -6), (30, 0, 0, -8), (36, 0, 0, 2), (56, 0, 0, 0))
legs(a, [(5, -6, 0, 0), (10, 30, 0, 0), (12, 34, 0, 0), (20, 6, 0, 6), (30, -6, 0, 8), (36, 40, 0, 6), (40, 38, 0, 6), (48, 10, 0, 2)],
     [(5, 6, 0, 0), (10, -20, 0, 0), (12, -24, 0, 0), (20, -2, 0, -6), (30, 4, 0, -8), (36, -16, 0, -6), (40, -14, 0, -6), (48, -4, 0, -2)],
     sr=[(10, -30, 0, 0), (20, -6, 0, 0), (36, -60, 0, 0), (40, -56, 0, 0), (48, -14, 0, 0)], sl=[(10, -6, 0, 0), (36, -20, 0, 0)])
a.hair([(0, 0, 0, 0), (10, -10, 0, 0), (14, 6, 0, 0), (28, -14, 0, -6), (33, -16, 0, 0), (37, 22, 0, 0), (42, 8, 0, 0), (56, 0, 0, 0)], 1)
a.cloth([(0, 0, 0, 0), (12, -10, 0, 0), (28, -8, 0, -6), (36, 20, 0, 0), (42, 6, 0, 0), (56, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ feather_darts (30): plucks a feather fan from the hair, flicks t13, second fan t21
a = A("feather_darts", 30)
a.r("arm_r", (4, 150, -10, -20), (7, 168, -14, -26), (10, 140, -20, 10), (12, 90, -30, 20), (13, 70, -30, 24), (16, 100, 10, 30), (18, 150, 0, 10),
    (20, 110, 20, -10), (21, 80, 30, -24), (24, 60, 20, -10), (28, 20, 0, 0))
a.d("fore_r", (4, 80, 0, 0), (7, 100, 0, 0), (10, 40, 0, 0), (13, 0, 0, 0), (16, 60, 0, 0), (18, 70, 0, 0), (21, 0, 0, 0), (25, 20, 0, 0))
a.d("hand_r", (7, 30, 0, 0), (10, 40, 0, 0), (13, -40, 0, 0), (18, 40, 0, 0), (21, -40, 0, 0), (25, 0, 0, 0))
a.d("chest", (4, 8, 16, 0), (7, 10, 20, 0), (10, 6, 10, 0), (13, -12, -24, 0), (16, 4, 10, 0), (18, 6, 14, 0), (21, -14, -20, 0), (25, -6, -6, 0))
a.d("head", (4, 6, 14, 10), (7, 10, 16, 14), (13, -6, -10, 0), (18, 4, 10, 6), (21, -6, -8, 0), (26, 0, 0, 0))
a.d("jaw", (7, -6, 0, 0), (13, -26, 0, 0), (16, -8, 0, 0), (21, -30, 0, 0), (26, -4, 0, 0))
a.r("arm_l", (6, 20, 0, -30), (13, -10, 0, -36), (21, -10, 0, -36), (26, 10, 0, -14))
claw(a, (6, -30, 0, 0), (13, 30, 0, 0), (21, 30, 0, 0), (26, 0, 0, 0))
bodyp(a, (7, 0, 0.3, 0.4), (13, 0, -0.6, -0.8), (18, 0, 0, 0.2), (21, 0, -0.6, -0.8), (26, 0, -0.2, -0.2))
legs(a, [(7, 6, 0, 0), (13, -16, 0, 0), (18, 0, 0, 0), (21, -16, 0, 0)], [(7, -4, 0, 0), (13, 18, 0, 0), (18, 0, 0, 0), (21, 18, 0, 0)],
     sl=[(13, -14, 0, 0), (21, -14, 0, 0)])
# feathers bend hard (plucked / re-grown)
a.drape("feather", [(0, 0, 0, 0), (5, -30, 0, -20), (8, -40, 0, -26), (12, 40, 0, 20), (16, -30, 0, -20), (20, 40, 0, 16), (26, 0, 0, 0)], 0)
a.hair([(0, 0, 0, 0), (7, -6, 0, -6), (13, 10, 0, 8), (18, -6, 0, -6), (21, 10, 0, 6), (28, 0, 0, 0)], 1)
a.cloth([(0, 0, 0, 0), (13, -6, 0, 6), (21, -6, 0, 6), (30, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ ink_lunge (30): drops low 0-8, explodes forward t9, claw spear-thrust t13, skid + recover
a = A("ink_lunge", 30)
a.r("arm_l", (4, -30, 0, -20), (8, -40, 0, -24), (11, 70, 0, 0), (13, 96, 0, 6), (16, 92, 0, 4), (20, 60, 0, -4), (26, 20, 0, -8))
a.d("fore_l", (4, 50, 0, 0), (8, 60, 0, 0), (13, -10, 0, 0), (18, 0, 0, 0), (24, 10, 0, 0))
claw(a, (4, 40, 0, 0), (8, 30, 0, 0), (11, -40, 0, 0), (13, -50, 0, 0), (18, -20, 0, 0), (24, 10, 0, 0))
a.d("hand_l", (8, 30, 0, 0), (13, -10, 0, 0))
a.d("chest", (4, -24, 10, 0), (8, -30, 14, 0), (11, -30, -10, 0), (13, -34, -20, 0), (18, -24, -10, 0), (24, -8, 0, 0))
a.d("head", (4, 20, -8, 0), (8, 26, -10, 0), (13, 20, 14, 0), (18, 14, 6, 0), (24, 2, 0, 0))
a.d("jaw", (4, -10, 0, 0), (8, -20, 0, 0), (13, -44, 0, 0), (18, -20, 0, 0), (24, -4, 0, 0))
a.d("arm_r", (4, -40, 0, 30), (8, -50, 0, 34), (13, -70, 0, 20), (18, -40, 0, 20), (26, -6, 0, 4))
a.d("fore_r", (8, 30, 0, 0), (13, 10, 0, 0))
bodyp(a, (4, 0, -2.4, 0.8), (8, 0, -3.2, 1.0), (10, 0, -1.4, -1.4), (13, 0, -1.8, -3.0), (18, 0, -1.6, -2.4), (24, 0, -0.6, -0.6))
legs(a, [(4, 30, 0, 4), (8, 40, 0, 4), (10, -10, 0, 0), (13, 40, 0, 0), (18, 36, 0, 0), (24, 10, 0, 0)],
     [(4, 24, 0, -4), (8, 30, 0, -4), (10, -30, 0, 0), (13, -34, 0, 0), (18, -28, 0, 0), (24, -6, 0, 0)],
     sr=[(4, -50, 0, 0), (8, -66, 0, 0), (10, -10, 0, 0), (13, -50, 0, 0), (18, -44, 0, 0), (24, -10, 0, 0)],
     sl=[(4, -50, 0, 0), (8, -66, 0, 0), (10, -4, 0, 0), (13, -6, 0, 0), (24, -4, 0, 0)])
a.hair([(0, 0, 0, 0), (8, 6, 0, 0), (11, -24, 0, 0), (14, -20, 0, 0), (18, 10, 0, 0), (24, 0, 0, 0)], 1)
a.cloth([(0, 0, 0, 0), (8, 6, 0, 0), (11, -24, 0, 0), (15, -18, 0, 0), (20, 10, 0, 0), (30, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ ground_rake (40): claw raised 0-10, drives into the floor t14, rakes forward 14-28 (spike line)
a = A("ground_rake", 40)
a.r("arm_l", (5, 120, 10, -30), (10, 150, 0, -24), (13, 80, 0, -10), (14, 50, 0, -4), (20, 40, 0, -2), (28, 30, 0, 0), (31, 40, 0, -6), (36, 16, 0, -8))
a.d("fore_l", (10, 40, 0, 0), (14, 0, 0, 0), (28, 0, 0, 0), (34, 10, 0, 0))
claw(a, (5, -40, 0, 0), (10, -50, 0, 0), (14, 30, 0, 0), (18, 40, 0, 0), (22, 30, 0, 0), (26, 40, 0, 0), (30, 0, 0, 0))
a.d("hand_l", (10, -30, 0, 0), (14, 40, 0, 0), (28, 40, 0, 0), (32, 0, 0, 0))
a.d("chest", (5, 14, 10, 0), (10, 20, 14, -4), (14, -40, -10, 0), (18, -42, -6, 2), (22, -40, -10, -2), (26, -42, -6, 2), (30, -30, 0, 0), (36, -8, 0, 0))
a.d("head", (5, 6, -6, 0), (10, 8, -8, 0), (14, 18, 6, 0), (28, 20, 4, 0), (34, 6, 0, 0))
a.d("jaw", (6, -16, 0, 0), (14, -50, 0, 0), (18, -30, 0, 0), (22, -50, 0, 0), (26, -30, 0, 0), (30, -46, 0, 0), (36, -6, 0, 0))
a.d("arm_r", (5, -20, 0, 30), (14, 30, 0, 40), (28, 30, 0, 40), (34, 4, 0, 8))
a.d("fore_r", (14, 40, 0, 0), (28, 40, 0, 0))
bodyp(a, (5, 0, 0.6, 0.6), (10, 0, 1.0, 0.8), (14, 0, -3.4, -1.6), (28, 0, -3.2, -1.8), (34, 0, -1.0, -0.6))
legs(a, [(10, -8, 0, 6), (14, 46, 0, 6), (28, 44, 0, 6), (34, 14, 0, 2)], [(10, 4, 0, -6), (14, -20, 0, -6), (28, -18, 0, -6), (34, -4, 0, -2)],
     sr=[(14, -70, 0, 0), (28, -68, 0, 0), (34, -20, 0, 0)], sl=[(14, -30, 0, 0), (28, -30, 0, 0)], fr=[(14, 20, 0, 0), (28, 20, 0, 0)])
a.hair([(0, 0, 0, 0), (10, -10, 0, 0), (14, 24, 0, 0), (20, 10, 0, 6), (26, 10, 0, -6), (32, 4, 0, 0), (40, 0, 0, 0)], 1)
a.cloth([(0, 0, 0, 0), (10, 6, 0, 0), (14, -24, 0, 0), (22, -18, 0, 0), (30, -10, 0, 0), (40, 0, 0, 0)], 1)
a.done()

# ------------------------------------------------------------------ guard_counter (40): huge claw raised as a shield 4-24 (braced, peeking), counter rake t28
a = A("guard_counter", 40)
a.r("arm_l", (4, 90, 40, 40), (8, 100, 50, 46), (16, 98, 48, 44), (18, 104, 52, 48), (20, 98, 48, 44), (24, 100, 60, 40), (26, 80, 70, 10),
    (28, 84, -50, 0), (30, 80, -70, 4), (34, 50, -40, 0), (38, 20, -10, -6))
a.d("fore_l", (4, 50, 0, -20), (8, 70, 0, -24), (24, 70, 0, -24), (26, 30, 0, 0), (28, -4, 0, 0), (34, 10, 0, 0))
claw(a, (4, -40, 0, 0), (8, -60, 0, 0), (24, -60, 0, 0), (26, -20, 0, 0), (28, 30, 0, 0), (34, 0, 0, 0))
a.d("chest", (4, -10, 20, 0), (8, -14, 24, 0), (24, -14, 26, 0), (26, -6, 34, 0), (28, -8, -30, 0), (31, -10, -36, 0), (36, -4, -8, 0))
a.d("head", (4, -10, -20, 0), (8, -12, -22, 0), (12, -12, -14, 8), (16, -12, -22, 0), (20, -12, -14, -6), (24, -12, -22, 0), (28, 0, 20, 0), (34, 0, 6, 0))
a.d("jaw", (4, -4, 0, 0), (12, -14, 0, 0), (14, -4, 0, 0), (18, -14, 0, 0), (24, -10, 0, 0), (28, -36, 0, 0), (34, -6, 0, 0))
a.d("arm_r", (4, -20, 0, 24), (24, -20, 0, 26), (28, 30, 0, 20), (34, 6, 0, 6))
bodyp(a, (4, 0, -1.4, 0.6), (8, 0, -1.6, 0.8), (24, 0, -1.6, 0.8), (28, 0, -1.0, -1.4), (32, 0, -0.8, -1.2))
a.rot("body", (0, 0, 0, 0), (8, 0, 14, 0), (24, 0, 16, 0), (28, 0, -16, 0), (34, 0, -6, 0), (40, 0, 0, 0))
legs(a, [(4, -20, 0, 6), (8, -24, 0, 8), (24, -24, 0, 8), (28, 22, 0, 0), (34, 10, 0, 0)], [(4, 24, 0, -6), (8, 28, 0, -8), (24, 28, 0, -8), (28, -14, 0, 0)],
     sr=[(8, -16, 0, 0), (24, -16, 0, 0), (28, -20, 0, 0)], sl=[(8, -40, 0, 0), (24, -40, 0, 0), (28, -6, 0, 0)])
a.hair([(0, 0, 0, 0), (8, -6, 0, -6), (24, -6, 0, -6), (28, 6, 0, 14), (32, 0, 0, 8), (40, 0, 0, 0)])
a.cloth([(0, 0, 0, 0), (8, 4, 0, -4), (24, 4, 0, -4), (29, -6, 0, 14), (36, 0, 0, 2), (40, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ spin_kick (28): chamber 0-8, full spin on the left leg, long black leg sweeps t12, lands 16
a = A("spin_kick", 28)
a.rot("root", (0, 0, 0, 0), (6, 0, 30, 0), (9, 0, -60, 0), (12, 0, -200, 0), (15, 0, -300, 0), (18, 0, -350, 0), (22, 0, -360, 0), (28, 0, -360, 0))
a.d("leg_r", (4, 30, 0, 10), (8, 50, 0, 14), (10, 60, 0, 70), (12, 40, 0, 86), (15, 30, 0, 60), (18, 10, 0, 10), (22, 0, 0, 0))
a.d("shin_r", (4, -60, 0, 0), (8, -80, 0, 0), (11, -6, 0, 0), (15, -10, 0, 0), (18, -40, 0, 0), (22, 0, 0, 0))
a.d("leg_l", (8, -4, 0, 0), (12, 0, 0, -6), (18, 4, 0, 0))
a.d("shin_l", (6, -20, 0, 0), (12, -6, 0, 0), (18, -30, 0, 0), (22, -10, 0, 0))
a.d("chest", (6, 4, 10, -6), (12, 0, 0, -20), (15, 0, 0, -16), (19, -6, 0, 0))
a.d("head", (6, -4, -20, 0), (12, 0, 10, 16), (16, 0, 0, 8), (20, 0, 0, 0))
a.d("jaw", (8, -20, 0, 0), (12, -36, 0, 0), (18, -10, 0, 0))
a.r("arm_l", (6, 30, 0, -40), (12, 10, 0, -70), (16, 20, 0, -50), (22, 14, 0, -10))
a.r("arm_r", (6, 20, 0, 40), (12, 0, 0, 70), (16, 10, 0, 40), (22, 6, 0, 6))
claw(a, (6, 20, 0, 0), (12, -30, 0, 0), (18, 0, 0, 0))
bodyp(a, (6, 0, -1.0, 0), (10, 0, 0.8, 0), (13, 0, 1.0, 0), (17, 0, -1.2, 0), (22, 0, -0.4, 0))
a.hair([(0, 0, 0, 0), (8, 0, 0, 14), (12, 0, 0, -22), (16, 0, 0, -18), (20, 0, 0, 8), (28, 0, 0, 0)], 1)
a.cloth([(0, 0, 0, 0), (8, 0, 0, 14), (12, 0, 0, -26), (17, 0, 0, -20), (22, 0, 0, 6), (28, 0, 0, 0)], 1)
a.done()

# ------------------------------------------------------------------ ink_quake (40): hoists the claw high (fist) 0-14, hammers the floor t17, ink spikes ring t20
a = A("ink_quake", 40)
a.r("arm_l", (5, 110, 0, -40), (10, 160, 0, -30), (14, 176, 0, -20), (16, 110, 0, -8), (17, 46, 0, -2), (22, 44, 0, -4), (28, 46, 0, -4), (34, 20, 0, -8))
a.d("fore_l", (10, 50, 0, 0), (14, 60, 0, 0), (17, -6, 0, 0), (28, 0, 0, 0))
claw(a, (5, 40, 0, 0), (10, 70, 0, 0), (17, 70, 0, 0), (22, 70, 0, 0), (26, 0, 0, 0))
a.d("hand_l", (14, -30, 0, 0), (17, 30, 0, 0), (26, 0, 0, 0))
a.r("arm_r", (5, 110, 0, 40), (10, 150, 0, 34), (14, 160, 0, 24), (17, 50, 0, 10), (24, 40, 0, 10), (34, 6, 0, 6))
a.d("chest", (5, 18, 0, 0), (10, 26, 0, 6), (14, 30, 0, 6), (17, -44, 0, 0), (22, -42, 0, 0), (28, -36, 0, 0), (35, -8, 0, 0))
a.d("head", (5, 16, 0, 0), (14, 26, 0, 8), (17, -6, 0, 0), (19, -4, 0, 10), (21, -4, 0, -8), (24, 0, 0, 0), (34, 0, 0, 0))
a.d("jaw", (5, -30, 0, 0), (14, -60, 0, 0), (17, -10, 0, 0), (20, -60, 0, 0), (28, -40, 0, 0), (36, -6, 0, 0))
bodyp(a, (5, 0, 0.8, 0.6), (14, 0, 1.4, 1.0), (17, 0, -3.4, -1.8), (22, 0, -3.0, -1.6), (30, 0, -1.6, -0.8))
legs(a, [(10, -6, 0, 10), (14, -8, 0, 12), (17, 50, 0, 12), (24, 46, 0, 12), (32, 12, 0, 2)],
     sr=[(14, 10, 0, 0), (17, -76, 0, 0), (24, -70, 0, 0), (32, -16, 0, 0)], fr=[(17, 24, 0, 0), (24, 22, 0, 0)])
a.hair([(0, 0, 0, 0), (10, -10, 0, 0), (14, -14, 0, 0), (18, 30, 0, 0), (22, 10, 0, 8), (25, 10, 0, -8), (32, 2, 0, 0), (40, 0, 0, 0)], 1)
a.cloth([(0, 0, 0, 0), (12, 8, 0, 0), (18, -26, 0, 0), (24, -14, 0, 0), (34, -4, 0, 0), (40, 0, 0, 0)], 1)
a.done()

# ------------------------------------------------------------------ ink_tendrils (40): claw stabbed into the floor t14 (tendrils under the target), wrench up t24 (spikes)
a = A("ink_tendrils", 40)
a.r("arm_l", (5, 60, 30, -40), (10, 120, 10, -30), (13, 90, 0, -10), (14, 40, 0, 0), (20, 38, 0, 0), (22, 42, 0, 0), (24, 90, 0, -10), (27, 110, 0, -14),
    (32, 60, 0, -8), (37, 16, 0, -8))
a.d("fore_l", (10, 30, 0, 0), (14, -10, 0, 0), (22, -10, 0, 0), (24, 40, 0, 0), (32, 20, 0, 0))
claw(a, (5, -40, 0, 0), (10, -50, 0, 0), (14, -60, 0, 0), (17, -40, 0, 0), (20, -60, 0, 0), (22, -30, 0, 0), (24, 60, 0, 0), (30, 40, 0, 0), (36, 0, 0, 0))
a.d("hand_l", (14, 60, 0, 0), (22, 60, 0, 0), (24, -20, 0, 0), (30, 0, 0, 0))
a.d("chest", (5, 8, 20, 0), (10, 14, 24, -6), (14, -38, 0, -10), (22, -36, 0, -10), (24, -6, -10, 0), (27, 4, -14, 0), (34, -4, 0, 0))
a.d("head", (5, 0, -14, 0), (14, 26, 0, 6), (18, 26, 0, 14), (22, 26, 0, 8), (24, 10, 0, 0), (27, 16, 0, 0), (34, 0, 0, 0))
a.d("jaw", (6, -10, 0, 0), (14, -40, 0, 0), (18, -24, 0, 0), (24, -66, 0, 0), (30, -40, 0, 0), (36, -6, 0, 0))
a.d("arm_r", (5, -10, 0, 30), (14, 20, 0, 50), (22, 20, 0, 50), (27, -20, 0, 60), (34, 4, 0, 6))
bodyp(a, (10, 0, 0.6, 0.4), (14, 0, -3.0, -1.0), (22, 0, -2.8, -1.0), (26, 0, -0.4, 0.2), (32, 0, -0.2, 0))
legs(a, [(10, -4, 0, 4), (14, 36, 0, 8), (22, 36, 0, 8), (26, 4, 0, 2)], [(10, 4, 0, -4), (14, -10, 0, -14), (22, -10, 0, -14), (26, 0, 0, -2)],
     sr=[(14, -60, 0, 0), (22, -58, 0, 0), (27, -8, 0, 0)], sl=[(14, -20, 0, 0), (22, -20, 0, 0)])
a.hair([(0, 0, 0, 0), (10, -6, 0, 0), (14, 20, 0, 6), (22, 16, 0, 0), (25, -20, 0, 0), (30, -6, 0, 0), (40, 0, 0, 0)], 1)
a.cloth([(0, 0, 0, 0), (14, -20, 0, 0), (22, -16, 0, 0), (26, 14, 0, 0), (34, 0, 0, 0), (40, 0, 0, 0)], 1)
a.done()

# ------------------------------------------------------------------ mad_cackle (44, enraged): head thrown back laughing, shoulders shaking, ink orbs t18 / 26 / 34
a = A("mad_cackle", 44)
a.d("chest", (4, -10, 0, 0), (8, -14, 0, 0), (12, 20, 0, 0), (16, 26, 0, 3), (18, 22, 0, -3), (20, 26, 0, 3), (22, 22, 0, -3), (24, 26, 0, 3),
    (26, 22, 0, -3), (28, 26, 0, 3), (30, 22, 0, -3), (32, 26, 0, 3), (34, 22, 0, -3), (38, 8, 0, 0))
a.d("head", (4, -14, 0, 0), (8, -18, 0, 0), (12, 34, 0, 0), (16, 40, 0, 10), (18, 34, 0, -10), (20, 40, 0, 10), (22, 34, 0, -10), (24, 40, 0, 12),
    (26, 34, 0, -10), (28, 40, 0, 10), (30, 34, 0, -10), (32, 40, 0, 10), (34, 34, 0, -10), (38, 10, 0, 0))
a.d("jaw", (4, -6, 0, 0), (8, -10, 0, 0), (12, -60, 0, 0), (14, -40, 0, 0), (16, -64, 0, 0), (18, -40, 0, 0), (20, -64, 0, 0), (22, -40, 0, 0),
    (24, -64, 0, 0), (26, -40, 0, 0), (28, -64, 0, 0), (30, -40, 0, 0), (32, -64, 0, 0), (34, -44, 0, 0), (40, -6, 0, 0))
a.r("arm_r", (4, 50, -14, -26), (8, 58, -14, -28), (12, 20, 0, 60), (18, 10, 0, 80), (26, 14, 0, 84), (34, 10, 0, 80), (40, 6, 0, 10))
a.d("fore_r", (4, 90, 0, 0), (8, 94, 0, 0), (12, 20, 0, 0), (34, 30, 0, 0))
a.r("arm_l", (8, 20, 0, -20), (12, 40, 0, -60), (16, 70, 0, -50), (18, 110, 0, -30), (20, 60, 0, -50), (24, 70, 0, -50), (26, 110, 0, -30), (28, 60, 0, -50),
    (32, 70, 0, -50), (34, 110, 0, -30), (38, 40, 0, -20))
claw(a, (12, -40, 0, 0), (16, 30, 0, 0), (18, -60, 0, 0), (22, 30, 0, 0), (26, -60, 0, 0), (30, 30, 0, 0), (34, -60, 0, 0), (40, 0, 0, 0))
bodyp(a, (8, 0, -0.8, 0.4), (12, 0, 0.6, 0.6), (34, 0, 0.6, 0.6), (40, 0, 0, 0))
legs(a, [(8, 10, 0, 4), (12, -6, 0, 8), (34, -6, 0, 8), (40, 0, 0, 0)], sr=[(8, -14, 0, 0), (12, 6, 0, 0), (34, 6, 0, 0)])
a.hair([(0, 0, 0, 0), (8, 6, 0, 0), (12, -20, 0, 0), (16, -26, 0, 8), (20, -20, 0, -8), (24, -26, 0, 8), (28, -20, 0, -8), (32, -26, 0, 8), (38, -6, 0, 0),
        (44, 0, 0, 0)], 1)
a.cloth([(0, 0, 0, 0), (12, -6, 0, 0), (18, -4, 0, 6), (26, -4, 0, -6), (34, -4, 0, 6), (44, 0, 0, 0)], 1)
a.done()

# ------------------------------------------------------------------ claw_frenzy (48, enraged): rakes t10 / 16 / 22 / 28 alternating, rising double-claw finisher t36
a = A("claw_frenzy", 48)
al, ch, hd, bp, hr, cl = [], [], [], [], [], []
for i, T in enumerate((10, 16, 22, 28)):
    sd = 1 if i % 2 == 0 else -1  # 1 = forehand (out -> across), -1 = backhand
    al += [(T - 3, 70 + i * 4, 70 * sd, -30 * sd if sd > 0 else 0), (T, 84, -50 * sd, 0), (T + 1, 80, -66 * sd, 0)]
    ch += [(T - 3, -4, 26 * sd, 0), (T, -12, -30 * sd, 0)]
    hd += [(T - 3, 0, -16 * sd, 0), (T, -4, 16 * sd, 6 * sd)]
    bp += [(T - 3, 0, -0.6, -0.4 - i * 0.1), (T, 0, -1.0, -1.4 - i * 0.1)]
    hr += [(T - 3, -4, 0, -10 * sd), (T, 6, 0, 14 * sd)]
    cl += [(T - 3, -40, 0, 0), (T, 20, 0, 0)]
a.r("arm_l", *al, (32, 20, 0, -40), (34, -30, 0, -20), (36, 150, 0, -10), (38, 170, 0, -10), (42, 100, 0, -10), (46, 30, 0, -8))
a.d("fore_l", (7, 30, 0, 0), (10, 0, 0, 0), (13, 30, 0, 0), (16, 0, 0, 0), (19, 30, 0, 0), (22, 0, 0, 0), (25, 30, 0, 0), (28, 0, 0, 0), (32, 50, 0, 0),
    (36, -10, 0, 0), (42, 10, 0, 0))
claw(a, *cl, (32, -60, 0, 0), (36, -40, 0, 0), (40, 20, 0, 0), (46, 0, 0, 0))
a.r("arm_r", (7, 40, 0, 30), (16, 50, 0, 40), (28, 40, 0, 30), (32, -20, 0, 20), (36, 150, 0, 10), (38, 170, 0, 10), (42, 100, 0, 10), (46, 10, 0, 6))
a.d("fore_r", (32, 50, 0, 0), (36, 0, 0, 0))
a.d("chest", *ch, (32, -30, 0, 0), (36, 24, 0, 0), (38, 28, 0, 0), (42, 6, 0, 0))
a.d("head", *hd, (32, 10, 0, 0), (36, 30, 0, 0), (38, 34, 0, 0), (44, 6, 0, 0))
a.d("jaw", (7, -30, 0, 0), (10, -10, 0, 0), (13, -30, 0, 0), (16, -10, 0, 0), (19, -30, 0, 0), (22, -10, 0, 0), (25, -30, 0, 0), (28, -10, 0, 0),
    (32, -20, 0, 0), (36, -64, 0, 0), (42, -30, 0, 0), (46, -4, 0, 0))
bodyp(a, *bp, (32, 0, -2.8, -2.0), (36, 0, 2.6, -2.6), (38, 0, 3.0, -2.6), (42, 0, -0.6, -1.6), (46, 0, -0.2, -0.4))
legs(a, [(7, 20, 0, 0), (10, -16, 0, 0), (13, 22, 0, 0), (16, -16, 0, 0), (19, 24, 0, 0), (22, -14, 0, 0), (25, 26, 0, 0), (28, 26, 0, 0), (32, 40, 0, 4),
         (36, -20, 0, 0), (40, -10, 0, 0), (44, 0, 0, 0)],
     [(7, -16, 0, 0), (10, 22, 0, 0), (13, -16, 0, 0), (16, 24, 0, 0), (19, -14, 0, 0), (22, 26, 0, 0), (25, -16, 0, 0), (28, -18, 0, 0), (32, 34, 0, -4),
      (36, 10, 0, 0), (40, 4, 0, 0), (44, 0, 0, 0)],
     sr=[(7, -30, 0, 0), (10, -6, 0, 0), (16, -30, 0, 0), (22, -30, 0, 0), (28, -20, 0, 0), (32, -70, 0, 0), (36, -6, 0, 0), (40, -30, 0, 0)],
     sl=[(10, -30, 0, 0), (16, -6, 0, 0), (22, -6, 0, 0), (28, -10, 0, 0), (32, -70, 0, 0), (36, -40, 0, 0), (40, -20, 0, 0)])
a.hair([(0, 0, 0, 0)] + hr + [(32, 10, 0, 0), (36, -26, 0, 0), (40, 10, 0, 0), (48, 0, 0, 0)], 1)
a.cloth([(0, 0, 0, 0), (10, -6, 0, 10), (16, -6, 0, -10), (22, -6, 0, 10), (28, -6, 0, -10), (32, 6, 0, 0), (37, -26, 0, 0), (42, 10, 0, 0), (48, 0, 0, 0)], 1)
a.done()

# ------------------------------------------------------------------ death (40): grin stretches, staggers; the heavy claw drags him down sideways onto it
a = A("death", 40)
a.d("chest", (4, 20, 10, 6), (8, 24, -6, -4), (12, 0, 0, -10), (18, -20, 0, -20), (26, -30, 0, -24), (40, -30, 0, -24))
a.d("head", (4, 30, 0, 14), (8, 30, 0, -14), (12, 10, 0, -10), (20, -10, 0, -30), (26, -14, 0, -36), (40, -14, 0, -38))
a.d("jaw", (4, -60, 0, 0), (8, -66, 0, 0), (14, -30, 0, 0), (22, -50, 0, 0), (40, -46, 0, 0))
a.r("arm_l", (4, -20, 0, -30), (8, -30, 0, -36), (14, 20, 0, -10), (20, 40, 0, 10), (26, 30, 0, 20), (40, 30, 0, 20))
claw(a, (4, -50, 0, 0), (8, -60, 0, 0), (16, 20, 0, 0), (24, 40, 0, 0), (32, 30, 0, 0), (36, 34, 0, 0), (40, 30, 0, 0))
a.r("arm_r", (4, 60, -10, -30), (8, 70, -14, -30), (14, 20, 0, 40), (24, 20, 0, 80), (40, 20, 0, 84))
a.d("fore_r", (4, 90, 0, 0), (8, 94, 0, 0), (14, 20, 0, 0), (40, 10, 0, 0))
bodyp(a, (4, 0, 0.4, 1.0), (8, 0, 0.2, 1.2), (14, 0, -3.0, 0.4), (20, 0, -3.6, 0), (40, 0, -3.6, 0))
a.pos("root", (0, 0, 0, 0), (16, 0, 0, 0), (24, -3.0, 2.4, -1.0), (28, -5.0, 3.0, -1.0), (31, -4.6, 3.4, -1.0), (34, -5.0, 3.0, -1.0), (40, -5.0, 3.0, -1.0))
a.rot("root", (0, 0, 0, 0), (16, 0, 0, 0), (22, -14, 0, 30), (27, -20, 0, 74), (30, -18, 0, 68), (33, -20, 0, 74), (40, -20, 0, 74))
legs(a, [(4, -10, 0, 0), (8, -12, 0, 6), (14, 50, 0, 10), (20, 60, 0, 12), (28, 30, 0, 12), (40, 26, 0, 12)],
     sr=[(8, 10, 0, 0), (14, -80, 0, 0), (20, -90, 0, 0), (28, -40, 0, 0), (40, -36, 0, 0)])
a.hair([(0, 0, 0, 0), (5, 10, 0, 6), (9, 14, 0, -6), (14, -10, 0, 0), (22, -10, 0, -20), (28, 10, 0, 20), (32, 4, 0, 10), (40, 6, 0, 12)])
a.cloth([(0, 0, 0, 0), (6, 10, 0, 0), (14, -10, 0, 0), (22, -14, 0, -14), (28, 10, 0, 16), (40, 6, 0, 10)])
a.drape("feather", [(0, 0, 0, 0), (20, -10, 0, -20), (28, 20, 0, 40), (34, 10, 0, 30), (40, 12, 0, 32)], 1)
a.done()

os.makedirs(os.path.dirname(OUT), exist_ok=True)
m.save(OUT)
print("cubes", len(m.cubes), "anims", [x["name"] for x in m.anims], "maxY", round(max(c["to"][1] for c in m.cubes), 1), "atlas rows", m.cy + m.rowh)
