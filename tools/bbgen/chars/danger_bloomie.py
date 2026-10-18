"""Danger Bloomie (DANGER AU Miss Bloomie, "the soldier") - generates assets/fpe/bbmodels/danger_bloomie.bbmodel.
Reference: docs/ref/confirmed/danger_bloomie.jpg - long navy double-breasted greatcoat down to the floor (pale piping lines,
grey-blue buttons, belt, puffed shoulders, cream/black striped cuffs), funnel collar up to the nose, pale blue-grey face with black
bangs over the eyes, black brimmed hat with two horns (one black, one cream-striped) and a cream WARNING triangle badge,
two very long cream/black striped ribbons hanging from the hat's right side, black assault rifle (AK) held low in the LEFT hand.
Blockbench space: Y up, ground 0, faces -Z. Character's RIGHT = +X.
Rotation cheat-sheet (file values): arm/leg rx>0 = swing forward, torso/head rx>0 = lean back / look up,
ry>0 = turn to the character's left, rz>0 = hanging part swings toward +X (character's right).
Rifle: barrel along -Z in the rifle group; barrel elevation = arm_l + fore_l + rifle (rx).
Run: python3 tools/bbgen/chars/danger_bloomie.py
"""
import math, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from bbgen import Model, mix  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "../../../src/main/resources/assets/fpe/bbmodels/danger_bloomie.bbmodel")

# ------------------------------------------------------------------ palette
NAVY, NAVY_D, NAVY_L = 0x23263D, 0x15172A, 0x343857
PIPE, PIPE_D = 0x8FA4BA, 0x5D6E84
BUTTON, BUTTON_D = 0x9FB4C6, 0x60758A
CREAM, CREAM_D = 0xDCCB9C, 0xB09E70
BLACK, BLACK_L = 0x111118, 0x2A2A36
HAIR, HAIR_HI, HAIR_D = 0x15151E, 0x2C2E40, 0x08080D
FACE, FACE_D, FACE_L = 0xC4D3D9, 0x8FA2AC, 0xE2ECEF
GUN, GUN_L, GUN_D = 0x17181E, 0x3B3E4A, 0x0A0A0E
STEEL, STEEL_D = 0xB8C0CA, 0x6E7682
OLIVE, OLIVE_D = 0x4E5534, 0x30341E
F_CORE, F_MID, F_OUT = 0xFFF6C0, 0xFFC040, 0xFF7A1C

m = Model("danger_bloomie", S=8, atlas=2048)
R = m.rng


# ------------------------------------------------------------------ painters
def all_faces(fn, skip=()):
    return {k: fn for k in ("north", "south", "east", "west", "up", "down") if k not in skip}


def combo(*fns):
    def f(F):
        for fn in fns: fn(F)
    return f


def frame(c, sides="lrtb"):
    def f(F):
        if "t" in sides: F.rect(0, 0, F.w, 1, c)
        if "b" in sides: F.rect(0, F.h - 1, F.w, 1, c)
        if "l" in sides: F.rect(0, 0, 1, F.h, c)
        if "r" in sides: F.rect(F.w - 1, 0, 1, F.h, c)
    return f


def vline(x, c, y0=0, y1=None):
    return lambda F: F.rect(int(x if x >= 0 else F.w + x), y0, 1, (y1 if y1 is not None else F.h) - y0, c)


def coat_cloth(n=3, dark=NAVY_D, light=NAVY_L):
    def f(F):
        for y in range(F.h):
            k = y / max(1, F.h - 1)
            for x in range(F.w):
                F.px(x, y, mix(NAVY, dark, 0.15 + 0.25 * k) if R.random() > 0.08 else mix(NAVY, light, 0.4))
        for i in range(n):
            x = int((i + 0.5) * F.w / n) + R.randint(-1, 1)
            for y in range(F.h // 4, F.h):
                F.px(x, y, mix(NAVY, dark, 0.65))
                F.px(x + 1, y, mix(NAVY, light, 0.45))
    return f


def stripes(c1, c2, period=6, slope=1.0, edge=None):
    def f(F):
        for y in range(F.h):
            for x in range(F.w):
                v = int(y + x * slope) % period
                F.px(x, y, c1 if v < period // 2 else c2)
        if edge is not None:
            F.rect(0, 0, 1, F.h, edge); F.rect(F.w - 1, 0, 1, F.h, edge)
    return f


def hair_strands(F):
    for x in range(F.w):
        r = R.random()
        c = HAIR_HI if r > 0.8 else HAIR_D if r < 0.25 else HAIR
        for y in range(F.h):
            F.px(x, y, mix(c, HAIR_D, 0.4 * y / max(1, F.h - 1)))


def gun_paint(F):
    for y in range(F.h):
        for x in range(F.w):
            F.px(x, y, GUN if R.random() > 0.1 else GUN_D)
    F.rect(0, 0, F.w, 1, GUN_L)


def warning(F):
    W, H = F.w, F.h
    F.rect(0, 0, W, H, BLACK)
    cx, top, bot = W / 2, 1.0, H - 1.0
    hw = (bot - top) * 0.62
    F.poly([(cx, top), (cx + hw, bot), (cx - hw, bot)], CREAM)
    F.poly([(cx, top + 3.2), (cx + hw - 3, bot - 1.6), (cx - hw + 3, bot - 1.6)], mix(CREAM, CREAM_D, 0.25))
    F.rect(int(cx) - 1, int(top + 6), 2, int((bot - top) * 0.42), BLACK)
    F.rect(int(cx) - 1, int(bot) - 4, 2, 2, BLACK)


def face_front(F):
    W, H = F.w, F.h  # 48x48
    for y in range(H):
        for x in range(W):
            c = mix(FACE_L, FACE, min(1, y / 20))
            if y > 30: c = mix(c, FACE_D, (y - 30) / 30)
            F.px(x, y, c)
    # shadow cast by the bangs + a faint cold eye under the hair on her right (viewer's left)
    F.rect(0, 0, W, 8, mix(FACE_D, HAIR, 0.5))
    F.rect(6, 15, 11, 2, mix(FACE_D, 0x2A3A48, 0.6))   # shadowed right eye (viewer's left), barely there
    F.rect(9, 16, 5, 1, 0x2A3A48)
    F.disc(39, 27, 1.6, mix(FACE, 0xA8B8C4, 0.7))  # cheek tint


def flash_paint(c1, c2):
    def f(fs):
        for F in fs.values():
            for y in range(F.h):
                for x in range(F.w):
                    c = mix(c1, c2, y / max(1, F.h - 1))
                    if R.random() < 0.2: c = mix(c, 0xFFFFFF, 0.35)
                    F.px(x, y, c, glow=True)
    return f


# ------------------------------------------------------------------ skeleton
m.group("root", (0, 0, 0))
m.group("body", (0, 12.6, 0), parent="root")
m.group("coat_f", (0, 13.0, -2.15), parent="body")
m.group("coat_fr", (0.6, 6.8, -2.75), parent="coat_f")
m.group("coat_fl", (-0.6, 6.8, -2.75), parent="coat_f")
m.group("coat_b", (0, 13.0, 2.15), parent="body")
m.group("coat_b2", (0, 6.8, 2.75), parent="coat_b")
m.group("coat_r", (3.1, 13.0, 0), parent="body")
m.group("coat_l", (-3.1, 13.0, 0), parent="body")
m.group("chest", (0, 13.6, 0), parent="body")
m.group("head", (0, 22.4, 0), parent="chest")
m.group("hat", (0, 27.6, 0), parent="head")
m.group("horn_r", (1.9, 31.4, 0.4), parent="hat")
m.group("horn_l", (-1.9, 31.4, 0.4), parent="hat")
for k, (x, z) in (("a", (4.0, -0.6)), ("b", (3.5, 2.0))):
    m.group(f"rib_{k}1", (x, 27.9, z), parent="hat")
    m.group(f"rib_{k}2", (x + 1.5, 19.7, z), parent=f"rib_{k}1")
    m.group(f"rib_{k}3", (x + 2.1, 11.6, z), parent=f"rib_{k}2")
m.group("bangs", (0, 28.0, -3.1), parent="head")
m.group("lock_r", (2.9, 27.6, -2.0), parent="head")
m.group("lock_l", (-2.9, 27.6, -2.0), parent="head")
for s, k in ((1, "r"), (-1, "l")):
    m.group("arm_" + k, (3.95 * s, 20.6, 0), parent="chest")
    m.group("fore_" + k, (3.95 * s, 16.9, 0), parent="arm_" + k)
    m.group("hand_" + k, (3.95 * s, 13.4, 0), parent="fore_" + k)
G = (-3.95, 12.3, 0.0)  # rifle grip
m.group("rifle", G, parent="hand_l")
m.group("mag", (-3.95, 12.0, -2.8), parent="rifle")
m.group("bayonet", (-3.95, 12.75, -14.0), parent="rifle")
m.group("gl", (-3.95, 11.6, -6.0), parent="rifle")
m.group("flash", (-3.95, 12.75, -14.2), parent="rifle")
m.group("mag2", (3.95, 11.8, -0.2), parent="hand_r")
m.group("mine", (3.95, 11.6, -0.6), parent="hand_r")
for s, k in ((1, "r"), (-1, "l")):
    m.group("leg_" + k, (1.35 * s, 12.2, 0), parent="root")
    m.group("shin_" + k, (1.35 * s, 6.6, 0), parent="leg_" + k)
    m.group("foot_" + k, (1.35 * s, 1.4, 0), parent="shin_" + k)

# ------------------------------------------------------------------ legs (mostly hidden by the coat): black trousers + boots
for s, k in ((1, "r"), (-1, "l")):
    x = 1.35 * s
    m.cube("thigh_" + k, "leg_" + k, (x - 1.2, 6.4, -1.2), (x + 1.2, 12.4, 1.2), BLACK, color2=BLACK_L, grad=True)
    m.cube("calf_" + k, "shin_" + k, (x - 1.1, 1.6, -1.1), (x + 1.1, 6.8, 1.1), BLACK_L, color2=BLACK, grad=True)
    m.cube("boot_" + k, "foot_" + k, (x - 1.25, 0.0, -2.6), (x + 1.25, 1.8, 1.3), BLACK,
           faces={"north": frame(GUN_L, "t"), "east": frame(GUN_L, "t"), "west": frame(GUN_L, "t")})
    m.cube("toe_" + k, "foot_" + k, (x - 0.9, 0.0, -3.4), (x + 0.9, 1.1, -2.4), BLACK_L)

# ------------------------------------------------------------------ greatcoat skirt: split front, back with vent, flared sides
m.cube("hips", "body", (-3.15, 11.6, -2.15), (3.15, 13.8, 2.15), NAVY, color2=NAVY_D, grad=True)
m.cube("cf_up", "coat_f", (-3.3, 6.6, -2.45), (3.3, 13.2, -1.85), NAVY, origin=(0, 13.0, -2.15), rot=(5, 0, 0),
       faces={"north": combo(coat_cloth(3), vline(-12, PIPE), vline(4, PIPE_D))})
for s, k in ((1, "r"), (-1, "l")):
    x0, x1 = (0.4, 4.1) if s > 0 else (-4.1, -0.4)
    edge = vline(0 if s > 0 else -1, PIPE)
    m.cube("cf_lo_" + k, "coat_f" + k, (x0, 0.6, -3.05), (x1, 7.0, -2.45), NAVY, origin=(0.6 * s, 6.8, -2.75), rot=(6, 0, 0),
           faces={"north": combo(coat_cloth(2), edge, frame(PIPE, "b")), "south": coat_cloth(1, NAVY_D, NAVY)})
m.cube("cb_up", "coat_b", (-3.3, 6.6, 1.85), (3.3, 13.2, 2.45), NAVY, origin=(0, 13.0, 2.15), rot=(-5, 0, 0),
       faces={"south": coat_cloth(3)})
m.cube("cb_lo", "coat_b2", (-4.1, 0.6, 2.45), (4.1, 7.0, 3.05), NAVY, origin=(0, 6.8, 2.75), rot=(-6, 0, 0),
       faces={"south": combo(coat_cloth(3), lambda F: F.rect(F.w // 2, 0, 1, F.h, PIPE_D), frame(PIPE, "b"))})
for s, k in ((1, "r"), (-1, "l")):
    m.cube("cs_" + k, "coat_" + k, (3.1 * s - 0.35, 0.8, -2.7), (3.1 * s + 0.35, 13.2, 2.7), NAVY, origin=(3.1 * s, 13.0, 0), rot=(0, 0, 8 * s),
           faces={"east": combo(coat_cloth(3), frame(PIPE, "b")), "west": combo(coat_cloth(3), frame(PIPE, "b"))})
    m.cube("cs_corner_f" + k, "coat_" + k, (3.1 * s - 0.9, 0.8, -3.0), (3.1 * s + 0.2, 12.4, -2.4), NAVY_D, origin=(3.1 * s, 13.0, 0), rot=(4, 0, 8 * s))
    m.cube("cs_corner_b" + k, "coat_" + k, (3.1 * s - 0.9, 0.8, 2.4), (3.1 * s + 0.2, 12.4, 3.0), NAVY_D, origin=(3.1 * s, 13.0, 0), rot=(-4, 0, 8 * s))

# ------------------------------------------------------------------ torso: double-breasted front, belt, buttons, collar
m.cube("torso", "chest", (-3.0, 13.4, -2.1), (3.0, 20.9, 2.1), NAVY, color2=NAVY_D, grad=True,
       faces={"north": combo(coat_cloth(2), lambda F: F.line(F.w - 10, 0, F.w - 10, F.h, PIPE), lambda F: F.line(F.w - 10, F.h - 1, F.w - 4, F.h - 6, PIPE)),
              "south": combo(coat_cloth(2), frame(PIPE_D, "t"))})
m.cube("bust", "chest", (-2.7, 16.6, -2.4), (2.7, 20.4, -2.0), NAVY, color2=NAVY_D, grad=True, faces={"north": frame(PIPE_D, "lr")})
m.cube("belt", "chest", (-3.25, 13.0, -2.35), (3.25, 14.1, 2.35), BLACK, faces={"north": frame(PIPE_D, "tb")})
m.cube("buckle", "chest", (0.4, 12.8, -2.6), (2.0, 14.3, -2.25), STEEL_D, faces={"north": lambda F: F.rect(3, 3, F.w - 6, F.h - 6, BLACK)})
m.cube("belt_tail", "chest", (1.6, 10.6, -2.55), (2.4, 13.2, -2.3), BLACK, origin=(2, 13, -2.4), rot=(0, 0, 6))
for i, y in enumerate((15.3, 17.4, 19.4)):
    for j, x in enumerate((-1.3, 1.9)):
        m.cube(f"btn{i}{j}", "chest", (x - 0.42, y - 0.42, -2.62), (x + 0.42, y + 0.42, -2.3), BUTTON,
               faces={"north": lambda F: (F.rect(0, F.h - 2, F.w, 2, BUTTON_D), F.rect(1, 1, 2, 2, 0xD8E4EE))})
m.cube("collar", "chest", (-2.35, 20.4, -2.3), (2.35, 24.4, 2.2), NAVY, color2=NAVY_D, grad=True,
       faces={"north": combo(coat_cloth(1), frame(PIPE, "t"), lambda F: F.line(F.w * 0.66, 0, F.w * 0.66, F.h, PIPE_D)),
              "up": lambda F: F.rect(2, 2, F.w - 4, F.h - 4, NAVY_D), "east": frame(PIPE, "t"), "west": frame(PIPE, "t"),
              "south": frame(PIPE, "t")})
m.cube("collar_flap", "chest", (0.3, 20.6, -2.6), (2.5, 24.3, -2.2), NAVY_L, origin=(1.4, 22.6, -2.4), rot=(0, -8, 0), faces={"north": frame(PIPE, "lt")})
m.cube("collar_btn", "chest", (1.6, 23.2, -2.85), (2.3, 23.9, -2.55), BUTTON)

# ------------------------------------------------------------------ head: pale face, bangs, side locks
m.cube("skull", "head", (-3.0, 22.6, -3.0), (3.0, 28.4, 3.0), FACE, faces={"north": face_front, "up": hair_strands, "south": hair_strands})
m.cube("hair_back", "head", (-3.35, 21.6, 0.2), (3.35, 28.3, 3.4), HAIR, faces=all_faces(hair_strands))
m.cube("bang_main", "bangs", (-3.3, 26.6, -3.55), (3.3, 28.2, -2.95), HAIR, faces=all_faces(hair_strands))
# heavy sweep over her left eye (viewer's right), short fringe over the right eye
for i, (x, ln, rz) in enumerate([(-2.8, 4.6, 4), (-1.8, 4.4, 8), (-0.8, 3.6, 14), (0.4, 2.2, 18), (1.6, 1.6, 10), (2.7, 2.2, -6)]):
    m.cube(f"bang{i}", "bangs", (x - 0.62, 28.0 - ln, -3.75), (x + 0.62, 27.8, -3.1), HAIR_HI if i == 3 else HAIR, origin=(x, 27.8, -3.4), rot=(4, 0, rz),
           faces=all_faces(hair_strands))
for s, k in ((1, "r"), (-1, "l")):
    m.cube("lock_" + k + "_a", "lock_" + k, (2.9 * s - 0.6, 20.0, -2.6), (2.9 * s + 0.6, 27.8, -1.2), HAIR, origin=(2.9 * s, 27.6, -2.0), rot=(0, 0, 4 * s),
           faces=all_faces(hair_strands))
    m.cube("lock_" + k + "_b", "lock_" + k, (3.1 * s - 0.45, 18.4, -2.2), (3.1 * s + 0.45, 22.0, -1.4), HAIR_D, origin=(3.1 * s, 22, -1.8), rot=(0, 0, 10 * s))
    m.cube("lock_" + k + "_c", "lock_" + k, (3.2 * s - 0.55, 21.2, -1.3), (3.2 * s + 0.55, 27.6, 0.6), HAIR, faces=all_faces(hair_strands))

# ------------------------------------------------------------------ hat: crown, brim pulled low over the eyes, side points, horns, badge
m.cube("hat_band", "hat", (-3.55, 27.3, -3.55), (3.55, 28.7, 3.55), BLACK, faces=all_faces(frame(PIPE_D, "b"), ("up", "down")))
m.cube("hat_crown", "hat", (-3.25, 28.5, -3.15), (3.25, 31.2, 3.25), BLACK, color2=BLACK_L, grad=True, origin=(0, 28.5, 0), rot=(-3, 0, 4),
       faces={"north": frame(PIPE_D, "lr"), "east": frame(PIPE_D, "lr"), "west": frame(PIPE_D, "lr")})
m.cube("hat_top", "hat", (-2.6, 31.0, -2.5), (2.6, 31.9, 2.6), BLACK_L, origin=(0, 28.5, 0), rot=(-3, 0, 4))
m.cube("brim", "hat", (-5.4, 27.0, -4.4), (5.4, 27.7, 4.4), BLACK, origin=(0, 27.4, 0), rot=(0, 0, 5),
       faces={"up": frame(PIPE_D), "down": lambda F: F.rect(0, 0, F.w, F.h, GUN_D)})
m.cube("brim_front", "hat", (-4.6, 26.9, -6.6), (4.6, 27.6, -4.0), BLACK, origin=(0, 27.3, -4.2), rot=(-22, 0, 5),
       faces={"up": frame(PIPE, "t"), "north": frame(PIPE)})
m.cube("brim_point_r", "hat", (5.0, 26.9, -2.8), (8.4, 27.6, 1.6), BLACK, origin=(5.0, 27.4, 0), rot=(0, 10, -24), faces={"up": frame(PIPE_D)})
m.cube("brim_tip_r", "hat", (8.0, 26.95, -1.8), (9.8, 27.5, 0.6), BLACK, origin=(5.0, 27.4, 0), rot=(0, 10, -30))
m.cube("brim_point_l", "hat", (-7.4, 26.9, -2.6), (-5.0, 27.6, 1.6), BLACK, origin=(-5.0, 27.4, 0), rot=(0, -10, 16), faces={"up": frame(PIPE_D)})
m.cube("brim_back", "hat", (-4.4, 26.9, 4.0), (4.4, 27.6, 5.8), BLACK, origin=(0, 27.3, 4.2), rot=(14, 0, 5))
# horns: right one black spike, left one cream striped
HR = dict(origin=(1.9, 31.4, 0.4), rot=(10, 0, -22))
m.cube("horn_r_a", "horn_r", (0.9, 31.0, -0.6), (2.9, 33.8, 1.4), BLACK, faces=all_faces(frame(PIPE_D, "lr")), **HR)
m.cube("horn_r_b", "horn_r", (1.25, 33.6, -0.3), (2.55, 36.0, 1.1), BLACK, **HR)
m.cube("horn_r_c", "horn_r", (1.55, 35.8, 0.0), (2.25, 37.9, 0.8), BLACK_L, **HR)
HL = dict(origin=(-1.9, 31.4, 0.4), rot=(6, 0, 18))
SH = stripes(CREAM, BLACK, 6, 0.8)
m.cube("horn_l_a", "horn_l", (-2.9, 31.0, -0.6), (-0.9, 33.6, 1.4), CREAM, faces=all_faces(SH), **HL)
m.cube("horn_l_b", "horn_l", (-2.6, 33.4, -0.3), (-1.2, 35.6, 1.1), CREAM, faces=all_faces(SH), **HL)
m.cube("horn_l_c", "horn_l", (-2.25, 35.4, 0.0), (-1.55, 37.0, 0.7), BLACK, **HL)
m.cube("badge", "hat", (1.0, 28.0, -3.85), (4.6, 31.4, -3.35), BLACK, origin=(2.8, 29.7, -3.6), rot=(-4, -28, 6), faces={"north": warning})
m.cube("badge_pin", "hat", (2.55, 31.1, -3.75), (3.05, 31.6, -3.35), STEEL, origin=(2.8, 29.7, -3.6), rot=(-4, -28, 6))
# ribbons: two long cream/black striped ribbons from the hat's right side, knotted at the root
RS = stripes(CREAM, BLACK, 8, 1.1, edge=CREAM_D)
m.cube("rib_knot", "hat", (3.3, 27.2, -1.4), (4.7, 28.8, 2.8), CREAM, faces=all_faces(stripes(CREAM, BLACK, 6, 0.6)))
for k, (x, z) in (("a", (4.0, -0.6)), ("b", (3.5, 2.0))):
    w = 0.75 if k == "a" else 0.65
    m.cube(f"rib_{k}1_c", f"rib_{k}1", (x - w, 19.6, z - 0.2), (x + w, 27.9, z + 0.2), CREAM, origin=(x, 27.9, z), rot=(0, 0, 10), faces=all_faces(RS))
    m.cube(f"rib_{k}2_c", f"rib_{k}2", (x + 1.5 - w, 11.5, z - 0.2), (x + 1.5 + w, 19.7, z + 0.2), CREAM, origin=(x + 1.5, 19.7, z), rot=(0, 0, 4), faces=all_faces(RS))
    m.cube(f"rib_{k}3_c", f"rib_{k}3", (x + 2.1 - w, 2.6 if k == "a" else 4.6, z - 0.2), (x + 2.1 + w, 11.6, z + 0.2), CREAM, origin=(x + 2.1, 11.6, z),
           rot=(0, 0, 2), faces=all_faces(RS))
    m.cube(f"rib_{k}_tip", f"rib_{k}3", (x + 2.1 - w * 0.6, 1.6 if k == "a" else 3.6, z - 0.15), (x + 2.1 + w * 0.6, 2.8 if k == "a" else 4.8, z + 0.15), BLACK,
           origin=(x + 2.1, 11.6, z), rot=(0, 0, 2))

# ------------------------------------------------------------------ arms: puffed shoulders, sleeves, striped cuffs, black gloves
for s, k in ((1, "r"), (-1, "l")):
    x = 3.95 * s
    m.cube("shoulder_" + k, "arm_" + k, (x - 1.35, 18.8, -1.45), (x + 1.35, 21.6, 1.45), NAVY, color2=NAVY_D, grad=True, origin=(x, 20.6, 0), rot=(0, 0, 8 * s),
           faces={"up": frame(PIPE_D), "north": frame(PIPE_D, "t")})
    m.cube("sleeve_" + k, "arm_" + k, (x - 1.0, 16.6, -1.05), (x + 1.0, 19.2, 1.05), NAVY, color2=NAVY_D, grad=True, faces={"north": coat_cloth(1)})
    m.cube("forearm_" + k, "fore_" + k, (x - 1.05, 14.4, -1.1), (x + 1.05, 17.1, 1.1), NAVY, color2=NAVY_D, grad=True)
    m.cube("cuff_" + k, "fore_" + k, (x - 1.3, 13.2, -1.35), (x + 1.3, 15.0, 1.35), CREAM, faces=all_faces(stripes(CREAM, BLACK, 6, 1.0), ("up", "down")))
    m.cube("glove_" + k, "hand_" + k, (x - 0.9, 11.4, -0.95), (x + 0.9, 13.6, 0.95), BLACK, color2=BLACK_L, grad=True)
    m.cube("thumb_" + k, "hand_" + k, (x - 0.3 * s - 0.3, 11.8, -1.3), (x - 0.3 * s + 0.3, 13.0, -0.7), BLACK_L, origin=(x, 13, -1), rot=(14, 0, 0))

# ------------------------------------------------------------------ rifle (AK pattern, all black) in the left hand
gx = G[0]


def rc(name, x0, y0, z0, x1, y1, z1, c=GUN, parent="rifle", **kw):
    if "faces" not in kw and "paint" not in kw:
        kw["faces"] = all_faces(gun_paint)
    return m.cube(name, parent, (gx + x0, y0, z0), (gx + x1, y1, z1), c, **kw)


rc("rcv", -0.5, 12.0, -4.0, 0.5, 13.4, 0.6)
rc("rcv_top", -0.45, 13.4, -3.6, 0.45, 13.8, 0.4, GUN_L, faces=None)
rc("rsight", -0.3, 13.4, -4.4, 0.3, 14.0, -3.5)
rc("guard", -0.58, 12.1, -8.0, 0.58, 13.3, -4.0, faces=all_faces(combo(gun_paint, lambda F: [F.rect(x, 3, 1, F.h - 6, GUN_L) for x in range(3, F.w - 2, 5)])))
rc("gas", -0.3, 13.3, -7.6, 0.3, 13.8, -4.0)
rc("barrel", -0.25, 12.5, -13.0, 0.25, 13.0, -8.0, GUN_L, faces=None)
rc("fsight", -0.2, 13.0, -12.1, 0.2, 14.1, -11.6)
rc("brake", -0.36, 12.38, -14.0, 0.36, 13.12, -13.0)
rc("grip", -0.42, 10.4, -0.2, 0.42, 12.1, 0.8, origin=(gx, 12.0, 0.3), rot=(-16, 0, 0))
rc("stock", -0.45, 11.4, 0.6, 0.45, 13.2, 5.8, origin=(gx, 13.0, 0.6), rot=(7, 0, 0))
rc("butt", -0.55, 10.6, 5.5, 0.55, 13.2, 6.3, origin=(gx, 13.0, 0.6), rot=(7, 0, 0))
rc("mag_a", -0.4, 9.8, -3.6, 0.4, 12.0, -2.0, parent="mag", origin=(gx, 12.0, -2.8), rot=(14, 0, 0))
rc("mag_b", -0.4, 7.9, -4.2, 0.4, 10.0, -2.6, parent="mag", origin=(gx, 9.9, -3.4), rot=(32, 0, 0))
rc("bay_blade", -0.12, 12.55, -18.2, 0.12, 13.05, -14.0, STEEL, parent="bayonet", faces={"north": lambda F: F.rect(0, 0, F.w, F.h, STEEL_D)})
rc("bay_tip", -0.1, 12.65, -19.2, 0.1, 12.95, -18.1, STEEL, parent="bayonet", faces=None)
rc("bay_ring", -0.4, 12.3, -14.4, 0.4, 13.2, -13.6, STEEL_D, parent="bayonet", faces=None)
rc("gl_tube", -0.45, 11.0, -8.0, 0.45, 12.1, -4.4, OLIVE, parent="gl", faces=all_faces(frame(OLIVE_D)))
rc("gl_trig", -0.2, 10.4, -4.8, 0.2, 11.0, -4.4, OLIVE_D, parent="gl", faces=None)
rc("fl_a", -0.9, 11.85, -16.4, 0.9, 13.65, -14.0, F_MID, parent="flash", faces=None, glow=True, paint=flash_paint(F_CORE, F_OUT))
rc("fl_b", -1.4, 11.35, -15.2, 1.4, 14.15, -14.1, F_CORE, parent="flash", faces=None, glow=True, origin=(gx, 12.75, -14.6), rot=(0, 0, 45),
   paint=flash_paint(F_CORE, F_MID))
rc("fl_c", -0.5, 12.25, -18.0, 0.5, 13.25, -16.0, F_OUT, parent="flash", faces=None, glow=True, paint=flash_paint(F_MID, F_OUT))
# right-hand props: spare magazine (reload), hazard mine (warning-triangle disc)
m.cube("mag2_a", "mag2", (3.55, 9.8, -1.0), (4.35, 12.0, 0.6), GUN, faces=all_faces(gun_paint), origin=(3.95, 12, -0.2), rot=(14, 0, 0))
m.cube("mag2_b", "mag2", (3.55, 7.9, -1.6), (4.35, 10.0, 0.0), GUN, faces=all_faces(gun_paint), origin=(3.95, 9.9, -0.8), rot=(32, 0, 0))
m.cube("mine_disc", "mine", (2.6, 10.2, -1.95), (5.3, 11.0, 0.75), OLIVE, faces={"up": warning, "north": frame(CREAM), "east": frame(CREAM),
       "west": frame(CREAM), "south": frame(CREAM)})
m.cube("mine_led", "mine", (3.75, 11.0, -0.8), (4.15, 11.4, -0.4), 0xFF3020, glow=True)

# ================================================================== animation framework
PROPS = ["flash", "bayonet", "gl", "mag2", "mine"]
HIDE = (0, .001, .001, .001)
REST = {
    "root": (0, 0, 0), "root@p": (0, 0, 0), "body": (0, 0, 0), "body@p": (0, 0, 0), "chest": (0, 0, 0), "head": (0, 0, 0),
    "arm_l": (12, 0, 6), "fore_l": (22, 0, 0), "hand_l": (0, 0, 0), "rifle": (-64, 0, 0), "rifle@p": (0, 0, 0),
    "arm_r": (16, 0, -14), "fore_r": (48, 0, 0), "hand_r": (0, 0, 0),
    "leg_r": (0, 0, 2), "shin_r": (0, 0, 0), "foot_r": (0, 0, 0), "leg_l": (0, 0, -2), "shin_l": (0, 0, 0), "foot_l": (0, 0, 0),
}
# shouldered aim (left shoulder, right hand on the handguard)
AIM = {"chest": (0, -14, 0), "head": (-2, 12, 0), "arm_l": (78, 0, 10), "fore_l": (14, 0, 0), "rifle": (-92, 0, 0),
       "arm_r": (84, 34, 0), "fore_r": (16, 0, 0)}
KNEEL = {"root@p": (0, -4.6, 0), "leg_r": (-6, 0, 4), "shin_r": (-88, 0, 0), "foot_r": (60, 0, 0), "leg_l": (82, 0, -4), "shin_l": (-82, 0, 0),
         "foot_l": (0, 0, 0)}
HIP = {"chest": (0, -8, 0), "head": (0, 8, 0), "arm_l": (34, 0, 8), "fore_l": (40, 0, 0), "rifle": (-74, 0, 0), "arm_r": (60, 36, 0), "fore_r": (40, 0, 0)}


def P(*dicts, **kw):
    out = {}
    for d in dicts + (kw,):
        for k, v in d.items(): out[k.replace("__", "@")] = v
    return out


def add(base, bone, d):
    v = base.get(bone, REST.get(bone, (0, 0, 0)))
    return tuple(v[i] + d[i] for i in range(3))


class A:
    def __init__(self, name, ticks, loop=False):
        self.name, self.ticks, self.loop, self.tr, self.poses = name, ticks, loop, {}, []
        self.sec_extra = {}

    def k(self, bone, ch, keys):
        self.tr.setdefault(bone, {}).setdefault(ch, []).extend(keys)
        return self

    def rot(self, bone, *keys): return self.k(bone, "rotation", keys)
    def pos(self, bone, *keys): return self.k(bone, "position", keys)
    def scl(self, bone, *keys): return self.k(bone, "scale", keys)

    def pose(self, t, d):
        self.poses.append((t, d))
        return self

    def show(self, bone, t0, t1, s=1.0, grow=1.0):
        ks = [HIDE]
        if t0 > 0: ks += [(max(0.01, t0 - grow), .001, .001, .001)]
        ks += [(t0, s, s, s)]
        if t1 < self.ticks: ks += [(t1, s, s, s), (min(self.ticks, t1 + grow), .001, .001, .001)]
        if t0 <= 0: ks[0] = (0, s, s, s)
        self.scl(bone, *ks)

    def flashes(self, ticks, s=1.0):
        ks = [HIDE]
        for t in ticks:
            ks += [(t - 0.4, .001, .001, .001), (t, s, s, s * 1.2), (t + 0.9, s * 0.6, s * 0.6, s * 1.5), (t + 1.3, .001, .001, .001)]
        self.scl("flash", *ks)

    def recoil(self, ticks, kick=10, back=0.8, arm="arm_l"):
        """add recoil spikes on top of the baked rifle/arm/chest tracks"""
        self.recoil_ticks = getattr(self, "recoil_ticks", []) + [(t, kick, back, arm) for t in ticks]

    def ribbon(self, keys):
        self.sec_extra["rib"] = [(k[0], tuple(k[1:])) for k in keys]

    # ---- bake poses (carry-forward) into tracks
    def _sample(self, series, t):
        if t <= series[0][0]: return series[0][1]
        for (t0, v0), (t1, v1) in zip(series, series[1:]):
            if t0 <= t <= t1:
                u = (t - t0) / max(1e-6, t1 - t0)
                return tuple(v0[i] + (v1[i] - v0[i]) * u for i in range(3))
        return series[-1][1]

    def done(self):
        poses = sorted(self.poses, key=lambda p: p[0])
        bones = set(REST)
        for _, d in poses: bones |= set(d)
        series = {}
        for b in bones:
            cur = REST.get(b, (0, 0, 0))
            s = []
            for t, d in poses:
                cur = d.get(b, cur) if b in d else cur
                s.append((t, cur))
            # collapse equal neighbours
            series[b] = s
        # recoil overlay
        for (t, kick, back, arm) in getattr(self, "recoil_ticks", []):
            for b, dv in ((arm, (kick, 0, 0)), ("chest", (kick * 0.35, 0, 0)), ("head", (kick * 0.3, 0, 0)), ("rifle@p", (0, 0, back))):
                base = self._sample(series[b], t)
                pre = self._sample(series[b], t - 0.5)
                post = self._sample(series[b], t + 1.4)
                s = [p for p in series[b] if not (t - 0.5 < p[0] < t + 1.4)]
                s += [(t - 0.5, pre), (t + 0.4, tuple(base[i] + dv[i] for i in range(3))), (t + 1.4, post)]
                series[b] = sorted(s, key=lambda p: p[0])
        for b, s in series.items():
            name, ch = (b.split("@")[0], "position") if "@" in b else (b, "rotation")
            if b in ("root@p", "body@p", "rifle@p") or ch == "rotation":
                self.k(name, ch, [(t, *v) for t, v in s])
        self.series = series
        self._secondary()
        for p in PROPS:
            if p not in self.tr or "scale" not in self.tr[p]:
                self.scl(p, HIDE)
        tracks = {}
        for b, chs in self.tr.items():
            tracks[b] = {}
            for ch, v in chs.items():
                seen, out = set(), []
                for q in sorted(v, key=lambda q: q[0]):
                    tt = round(min(self.ticks, max(0, q[0])), 3)
                    if tt in seen: continue
                    seen.add(tt); out.append((tt / 20.0, *q[1:]))
                tracks[b][ch] = out
        m.anim(self.name, self.ticks / 20.0, tracks, loop=self.loop)

    # ---- automatic secondary motion (ribbons, coat, hair, horns lag behind the body)
    def _secondary(self):
        S = self.series
        n = int(self.ticks)
        ts = list(range(0, n + 1, 2 if n > 30 else 1))
        if ts[-1] != n: ts.append(n)

        def tor(t, bones):
            v = [0, 0, 0]
            for b in bones:
                x = self._sample(S[b], t)
                for i in range(3): v[i] += x[i]
            return [((q + 180) % 360) - 180 for q in v]  # full flips / spins count as upright again

        def vel(t, b="root@p"):
            a, c = self._sample(S[b], t - 1), self._sample(S[b], t + 1)
            return [(c[i] - a[i]) / 2 for i in range(3)]

        def wrap(t):
            if self.loop: return t % self.ticks
            return max(0, t)

        hat_chain = ["root", "body", "chest", "head"]
        extra = self.sec_extra.get("rib")
        for k in ("a", "b"):
            for i in range(3):
                lag = 1.5 * (i + 1) + (0.8 if k == "b" else 0)
                keys = []
                for t in ts:
                    tt = wrap(t - lag)
                    th = tor(tt, hat_chain)
                    v = vel(tt)
                    g = 0.55 if i == 0 else 0.35
                    rx = -th[0] * g + v[2] * 10 * g
                    rz = -th[2] * g - v[0] * 10 * g
                    if extra:
                        e = self._sample(extra, tt)
                        rx += e[0] * (0.6 + 0.3 * i); rz += e[2] * (0.6 + 0.3 * i)
                    sway = math.sin((t + i * 6 + (5 if k == "b" else 0)) / max(4, self.ticks) * math.tau * (1 if self.loop else 2)) * 2.5
                    keys.append((t, max(-80, min(80, rx + sway * 0.6)), 0, max(-80, min(85, rz + sway))))
                self.rot(f"rib_{k}{i + 1}", *keys)
        # coat: front halves follow the legs, back flares when legs go back / kneeling, sides open on lean
        cf, cfr, cfl, cb, cb2, cr, cl, lr, ll, hr, hl = ([] for _ in range(11))
        for t in ts:
            Lr, Ll = self._sample(S["leg_r"], t)[0], self._sample(S["leg_l"], t)[0]
            body = tor(wrap(t - 1.5), ["root", "body"])
            v = vel(wrap(t - 1.5))
            fwd = max(Lr, Ll, 0)
            cf.append((t, fwd * 0.35 - body[0] * 0.3 + v[2] * 6, 0, 0))
            cfr.append((t, max(0, Lr) * 0.45 - min(0, Lr) * 0.1, 0, 0))
            cfl.append((t, max(0, Ll) * 0.45 - min(0, Ll) * 0.1, 0, 0))
            back = min(Lr, Ll, 0)
            cb.append((t, back * 0.45 - body[0] * 0.3 + v[2] * 6 - max(0, fwd - 50) * 0.15, 0, 0))
            cb2.append((t, back * 0.3 - max(0, fwd - 50) * 0.1, 0, 0))
            Zr, Zl = self._sample(S["leg_r"], t)[2], self._sample(S["leg_l"], t)[2]
            cr.append((t, 0, 0, max(0, Zr - 2) * 0.7 - body[2] * 0.4 - v[0] * 6))
            cl.append((t, 0, 0, min(0, Zl + 2) * 0.7 - body[2] * 0.4 - v[0] * 6))
            th = tor(wrap(t - 2), hat_chain)
            vv = vel(wrap(t - 2))
            lr.append((t, -th[0] * 0.4 + vv[2] * 5, 0, -th[2] * 0.4 - vv[0] * 5))
            hr.append((t, -th[0] * 0.15 + vv[2] * 3, 0, -th[2] * 0.2))
        self.rot("coat_f", *cf); self.rot("coat_fr", *cfr); self.rot("coat_fl", *cfl)
        self.rot("coat_b", *cb); self.rot("coat_b2", *cb2); self.rot("coat_r", *cr); self.rot("coat_l", *cl)
        self.rot("lock_r", *lr); self.rot("lock_l", *lr)
        self.rot("horn_r", *hr); self.rot("horn_l", *hr)


# ================================================================== animations
def aim(elev=0, yaw=0, **kw):
    """shouldered aim; elev = barrel pitch up (deg), yaw = upper-body turn (ry>0 = to her left)"""
    d = P(AIM, arm_l=(78 + elev, 0, 10), arm_r=(84 + elev, 34, 0), chest=(0, -14 + yaw, 0), head=(-2 + elev * 0.4, 12, 0))
    d.update(P(**kw))
    return d


def hip(elev=0, yaw=0, **kw):
    d = P(HIP, arm_l=(34 + elev, 0, 8), arm_r=(60 + elev, 36, 0), chest=(0, -8 + yaw, 0))
    d.update(P(**kw))
    return d


STAND = P(KNEEL, root__p=(0, 0, 0), leg_r=REST["leg_r"], shin_r=(0, 0, 0), foot_r=(0, 0, 0), leg_l=REST["leg_l"], shin_l=(0, 0, 0), foot_l=(0, 0, 0))

# ------------------------------------------------------------------ idle (4 s): low-ready, slow breathing, tap the magazine, glance aside
a = A("idle", 80, loop=True)
a.pose(0, P(REST))
a.pose(20, P(REST, body__p=(0, -0.15, 0), chest=(-1, 0, 0), head=(2, 0, 0)))
a.pose(36, P(REST))
a.pose(42, P(REST, arm_r=(40, 30, -6), fore_r=(60, 0, 0), head=(-8, 6, 0), chest=(0, 4, 0)))   # reach over to the magazine
a.pose(46, P(REST, arm_r=(46, 34, -6), fore_r=(54, 0, 0), rifle=(-60, 0, 0), head=(-8, 6, 0), chest=(0, 4, 0)))  # tap
a.pose(48, P(REST, arm_r=(40, 30, -6), fore_r=(60, 0, 0), head=(-8, 6, 0), chest=(0, 4, 0)))
a.pose(50, P(REST, arm_r=(46, 34, -6), fore_r=(54, 0, 0), rifle=(-61, 0, 0), head=(-8, 6, 0), chest=(0, 4, 0)))
a.pose(56, P(REST, head=(0, -10, 0), chest=(0, -2, 0), body__p=(0, -0.15, 0)))
a.pose(70, P(REST, head=(0, -8, 2), chest=(-1, 0, 0)))
a.pose(80, P(REST))
a.done()

# ------------------------------------------------------------------ walk (one stride, 20): measured patrol march, rifle at low ready in both hands
a = A("walk", 20, loop=True)
W = P(REST, arm_r=(40, 30, -4), fore_r=(50, 0, 0), arm_l=(20, 0, 6), fore_l=(30, 0, 0), rifle=(-70, 0, 0))
for t, s in ((0, 1), (10, -1), (20, 1)):
    a.pose(t, P(W, leg_r=(26 * s, 0, 2), leg_l=(-26 * s, 0, -2), shin_r=(-4 if s > 0 else -14, 0, 0), shin_l=(-14 if s > 0 else -4, 0, 0),
                foot_r=(-8 * s, 0, 0), foot_l=(8 * s, 0, 0), body__p=(0, -0.4, 0), body=(-3, 4 * s, 0), chest=(0, -3 * s, 0), head=(2, -2 * s, 0),
                rifle=(-70 + 3 * s, 0, 0)))
for t, s in ((5, 1), (15, -1)):
    a.pose(t, P(W, leg_r=(0, 0, 2), leg_l=(0, 0, -2), shin_r=(-30 if s < 0 else 0, 0, 0), shin_l=(-30 if s > 0 else 0, 0, 0),
                body__p=(0, 0.5, 0), body=(-3, 0, 0), chest=(0, 0, 0), head=(2, 0, 0)))
a.done()

# ------------------------------------------------------------------ burst (30): shoulder 0..8, rack 6, 3 rounds 10/12/14, re-acquire, 3 rounds 20/22/24
a = A("burst", 30)
a.pose(0, P(REST))
a.pose(4, P(REST, body__p=(0, -0.5, 0), arm_l=(30, 0, 6), rifle=(-70, 0, 0), arm_r=(50, 30, -4), fore_r=(60, 0, 0), head=(4, 6, 0)))
a.pose(6, P(REST, body__p=(0, -0.6, 0), arm_l=(50, 0, 8), fore_l=(30, 0, 0), rifle=(-80, 0, 0), arm_r=(70, 30, 0), fore_r=(50, 0, 0), head=(2, 8, 0)))
a.pose(9, aim(2, body__p=(0, -0.6, 0), leg_r=(-14, 0, 3), leg_l=(16, 0, -3)))
a.pose(15, aim(4, body__p=(0, -0.6, 0), leg_r=(-14, 0, 3), leg_l=(16, 0, -3)))
a.pose(18, aim(-1, yaw=3, body__p=(0, -0.6, 0), leg_r=(-14, 0, 3), leg_l=(16, 0, -3)))
a.pose(25, aim(3, yaw=3, body__p=(0, -0.6, 0), leg_r=(-14, 0, 3), leg_l=(16, 0, -3)))
a.pose(27, aim(-6, yaw=4, body__p=(0, -0.4, 0)))
a.pose(30, P(REST))
a.flashes([10, 12, 14, 20, 22, 24])
a.recoil([10, 12, 14, 20, 22, 24], kick=9, back=0.9)
a.done()

# ------------------------------------------------------------------ spray (52): brace 0..8, full auto 10..42 sweeping her left -> right, smoking muzzle, sag
a = A("spray", 52)
SP = dict(body__p=(0, -1.0, 0), leg_r=(-22, 0, 6), leg_l=(24, 0, -6), shin_l=(-18, 0, 0), root=(0, 0, 0))
a.pose(0, P(REST))
a.pose(5, P(hip(-6, 10, **SP), chest=(6, 10, 0), body__p=(0, -1.4, 0)))
a.pose(9, hip(0, 40, **SP))
a.pose(26, hip(2, 0, **SP))
a.pose(42, hip(4, -40, **SP))
a.pose(45, hip(14, -44, **SP))
a.pose(48, P(REST, chest=(-6, -20, 0), head=(-10, -6, 0), body__p=(0, -0.5, 0), rifle=(-52, 0, 0)))
a.pose(52, P(REST))
shots = list(range(10, 43, 2))
a.flashes(shots, 0.9)
a.recoil(shots, kick=6, back=0.6)
a.done()

# ------------------------------------------------------------------ grenade_launcher (36): kneel 0..8, slide a shell in 11, raise 14, THUMP 16, recoil, rise
a = A("grenade_launcher", 36)
a.show("gl", 0, 36)
a.pose(0, P(REST))
a.pose(6, P(REST, KNEEL, chest=(-10, 0, 0), arm_r=(10, 0, -20), fore_r=(60, 0, 0), arm_l=(40, 0, 8), rifle=(-90, 0, 0)))
a.pose(9, P(KNEEL, hip(-10, 0), arm_r=(60, 40, 0), fore_r=(70, 0, 0), chest=(-12, -8, 0), head=(-14, 10, 0)))
a.pose(11, P(KNEEL, hip(-10, 0), arm_r=(66, 44, 0), fore_r=(40, 0, 0), chest=(-12, -8, 0), head=(-14, 10, 0), rifle=(-70, 0, 0)))
a.pose(14, P(KNEEL, hip(26, 6), chest=(4, -2, 0), head=(10, 10, 0)))
a.pose(15.5, P(KNEEL, hip(28, 6), chest=(4, -2, 0), head=(10, 10, 0)))
a.pose(17, P(KNEEL, hip(52, 6), chest=(18, -2, 0), head=(18, 10, 0), body=(8, 0, 0), root__p=(0, -4.6, 1.4)))
a.pose(22, P(KNEEL, hip(30, 4), chest=(8, 0, 0), head=(8, 6, 0), body=(2, 0, 0), root__p=(0, -4.6, 1.0)))
a.pose(28, P(KNEEL, hip(0, 0), chest=(0, 0, 0), root__p=(0, -4.4, 0.8)))
a.pose(33, P(REST, body__p=(0, -0.6, 0)))
a.pose(36, P(REST))
a.flashes([16], 1.5)
a.done()

# ------------------------------------------------------------------ shotgun (26): step in 0..7, low hip shot 10 (master-key launcher), recoil slide, rack, recover
a = A("shotgun", 26)
a.show("gl", 0, 26)
a.pose(0, P(REST))
a.pose(4, P(hip(-4, 18), chest=(-8, 18, 0), leg_r=(-10, 0, 4), leg_l=(30, 0, -4), shin_l=(-20, 0, 0), body__p=(0, -0.8, 0), head=(-6, 4, 0)))
a.pose(8, P(hip(-14, -6), chest=(-14, -6, 0), leg_r=(-26, 0, 6), leg_l=(38, 0, -6), shin_l=(-26, 0, 0), body__p=(0, -1.6, 0), body=(-6, 0, 0), head=(-10, 8, 0)))
a.pose(9.5, P(hip(-16, -6), chest=(-16, -6, 0), leg_r=(-26, 0, 6), leg_l=(38, 0, -6), shin_l=(-26, 0, 0), body__p=(0, -1.6, 0), body=(-6, 0, 0), head=(-10, 8, 0)))
a.pose(11, P(hip(16, -2), chest=(14, -2, 0), body=(10, 0, 0), leg_r=(-30, 0, 6), leg_l=(26, 0, -6), body__p=(0, -1.0, 1.6), head=(16, 4, 0)))
a.pose(14, P(hip(8, 0), chest=(8, 0, 0), body=(6, 0, 0), leg_r=(-20, 0, 6), leg_l=(14, 0, -6), body__p=(0, -0.8, 1.0)))
a.pose(17, P(hip(0, 0), arm_r=(70, 36, 0), fore_r=(10, 0, 0), chest=(0, 0, 0), body=(0, 0, 0), body__p=(0, -0.6, 0.4)))   # pump forward
a.pose(19, P(hip(0, 0), arm_r=(56, 36, 0), fore_r=(60, 0, 0), body__p=(0, -0.6, 0.4)))                                    # and back
a.pose(26, P(REST))
a.flashes([10], 1.8)
a.recoil([10], kick=26, back=1.5)
a.done()

# ------------------------------------------------------------------ butt_bash (26): flip the rifle stock-first 0..6, coil, lunge 9, CRACK 11, follow-through
a = A("butt_bash", 26)
a.pose(0, P(REST))
a.pose(4, P(REST, arm_l=(40, 0, 10), fore_l=(60, 0, 0), rifle=(-20, 180, 0), arm_r=(60, 30, 0), fore_r=(40, 0, 0), chest=(0, 10, 0)))
a.pose(8, P(REST, arm_l=(-20, 0, 20), fore_l=(80, 0, 0), rifle=(-60, 180, 0), arm_r=(30, 40, 0), fore_r=(60, 0, 0), chest=(-4, 40, 0),
            body=(0, 14, 0), head=(0, -30, 0), leg_r=(-14, 0, 4), leg_l=(20, 0, -4), body__p=(0, -0.8, 0)))
a.pose(10, P(REST, arm_l=(70, 0, 16), fore_l=(10, 0, 0), rifle=(-80, 180, 0), arm_r=(80, 40, 0), fore_r=(20, 0, 0), chest=(-16, -30, 0),
             body=(-10, -16, 0), head=(-6, 26, 0), leg_r=(-30, 0, 6), leg_l=(44, 0, -6), shin_l=(-26, 0, 0), body__p=(0, -1.4, -1.0)))
a.pose(12, P(REST, arm_l=(84, 0, 18), fore_l=(4, 0, 0), rifle=(-88, 180, 0), arm_r=(88, 40, 0), fore_r=(12, 0, 0), chest=(-20, -36, 0),
             body=(-12, -18, 0), head=(-6, 30, 0), leg_r=(-32, 0, 6), leg_l=(46, 0, -6), shin_l=(-28, 0, 0), body__p=(0, -1.6, -1.2)))
a.pose(16, P(REST, arm_l=(66, 0, 14), fore_l=(20, 0, 0), rifle=(-80, 180, 0), arm_r=(70, 40, 0), fore_r=(30, 0, 0), chest=(-10, -24, 0),
             body=(-6, -10, 0), head=(-4, 20, 0), leg_r=(-24, 0, 6), leg_l=(34, 0, -6), shin_l=(-20, 0, 0), body__p=(0, -1.2, -0.8)))
a.pose(20, P(REST, arm_l=(40, 0, 10), fore_l=(60, 0, 0), rifle=(-30, 180, 0), chest=(0, 4, 0), body__p=(0, -0.5, 0)))
a.pose(23, P(REST, rifle=(-64, 360, 0)))
a.pose(26, P(REST, rifle=(-64, 360, 0)))
a.done()

# ------------------------------------------------------------------ ribbon_whip (34): wind-up crouch 0..8, double heel spin 8..20 (lash 12, 16), stagger, settle
a = A("ribbon_whip", 34)
SPIN = dict(arm_l=(30, 0, -60), fore_l=(10, 0, 0), rifle=(-40, 0, 0), arm_r=(20, 0, -70), fore_r=(10, 0, 0), body__p=(0, -0.8, 0))
a.pose(0, P(REST))
a.pose(6, P(REST, root=(0, 40, 0), chest=(-6, 20, 0), head=(-6, 10, 0), body__p=(0, -1.6, 0), leg_r=(20, 0, 4), leg_l=(-10, 0, -4), shin_r=(-30, 0, 0),
            arm_r=(30, 0, -20), arm_l=(30, 0, 30)))
a.pose(8, P(REST, root=(0, 50, 0), chest=(-8, 24, 0), head=(-8, 14, 0), body__p=(0, -1.8, 0), leg_r=(24, 0, 4), leg_l=(-12, 0, -4), shin_r=(-36, 0, 0),
            arm_r=(30, 0, -20), arm_l=(30, 0, 30)))
a.pose(12, P(REST, SPIN, root=(0, -170, 0), chest=(4, -10, 0), head=(6, -8, 0), leg_r=(0, 0, 12), leg_l=(0, 0, -6)))
a.pose(16, P(REST, SPIN, root=(0, -420, 0), chest=(4, -10, 0), head=(6, -8, 0), leg_r=(0, 0, 14), leg_l=(0, 0, -8)))
a.pose(20, P(REST, root=(0, -640, 0), chest=(-4, -20, 0), head=(-4, -10, 0), body__p=(0, -1.2, 0), leg_r=(-10, 0, 8), leg_l=(16, 0, -6),
             arm_r=(40, 0, -30), arm_l=(30, 0, 20)))
a.pose(24, P(REST, root=(0, -710, 0), chest=(2, 6, 0), head=(4, 8, 0), body__p=(0, -0.4, 0)))
a.pose(28, P(REST, root=(0, -722, 0)))
a.pose(34, P(REST, root=(0, -720, 0)))
a.ribbon([(0, 0, 0, 0), (6, 0, 0, -20), (9, 0, 0, 30), (11, -10, 0, 80), (17, -10, 0, 85), (21, 0, 0, 50), (25, 0, 0, -20), (30, 0, 0, 8), (34, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ suppress (64): drop to one knee 0..12, steady stream 14..56 every 3, sweep a little, rise
a = A("suppress", 64)
a.pose(0, P(REST))
a.pose(6, P(REST, KNEEL, chest=(-8, 0, 0), arm_l=(50, 0, 8), rifle=(-80, 0, 0)))
a.pose(12, P(KNEEL, aim(-4, -2)))
for i, t in enumerate(range(14, 57, 6)):
    a.pose(t, P(KNEEL, aim(-4 + (i % 2), (-2 + (6 if i % 2 else -6)))))
a.pose(58, P(KNEEL, aim(-10, 0)))
a.pose(61, P(REST, body__p=(0, -0.8, 0), rifle=(-50, 0, 0)))
a.pose(64, P(REST))
sh = list(range(14, 57, 3))
a.flashes(sh, 0.8)
a.recoil(sh, kick=5, back=0.5)
a.done()

# ------------------------------------------------------------------ reload (32): tilt rifle 0..6, drop the empty mag 9, fetch a fresh one 12..17, seat 20, rack 25
a = A("reload", 32)
a.show("mag2", 12, 20)
a.scl("mag", (0, 1, 1, 1), (8.6, 1, 1, 1), (9, 1, 1, 1), (13, 1, 1, 1), (13.5, .001, .001, .001), (19.6, .001, .001, .001), (20, 1, 1, 1))
a.pos("mag", (0, 0, 0, 0), (8.6, 0, 0, 0), (10, 0, -2, 0), (11.5, 0, -5, 0), (13, 0, -9, 0), (13.5, 0, 0, 0), (32, 0, 0, 0))
a.rot("mag", (0, 0, 0, 0), (8.6, 0, 0, 0), (13, 40, 0, 0), (13.5, 0, 0, 0), (32, 0, 0, 0))
RL = dict(arm_l=(46, 0, 14), fore_l=(54, 0, 0), rifle=(-88, 0, 50), head=(-24, -14, 0), chest=(-8, 10, 0), body__p=(0, -0.4, 0))
a.pose(0, P(REST))
a.pose(5, P(REST, RL, arm_r=(50, 30, 0), fore_r=(50, 0, 0)))
a.pose(8, P(REST, RL, arm_r=(56, 36, 0), fore_r=(40, 0, 0)))
a.pose(9.5, P(REST, RL, arm_r=(40, 36, 0), fore_r=(40, 0, 0), rifle=(-84, 0, 56)))   # thumb the release, mag drops
a.pose(13, P(REST, RL, arm_r=(-10, 0, -10), fore_r=(30, 0, 0), head=(-20, -30, 0)))    # hand to the coat pouch
a.pose(16, P(REST, RL, arm_r=(30, 20, 0), fore_r=(60, 0, 0)))
a.pose(19, P(REST, RL, arm_r=(52, 36, 0), fore_r=(36, 0, 0)))
a.pose(20.5, P(REST, RL, arm_r=(58, 38, 0), fore_r=(28, 0, 0), rifle=(-92, 0, 46)))  # slap it home
a.pose(23, P(REST, RL, rifle=(-90, 0, -20), arm_r=(70, 30, 0), fore_r=(30, 0, 0), head=(-14, -6, 0)))
a.pose(25, P(REST, RL, rifle=(-90, 0, -20), arm_r=(46, 50, 0), fore_r=(60, 0, 0), head=(-14, -6, 0)))  # rack the handle
a.pose(27, P(REST, RL, rifle=(-90, 0, -10), arm_r=(64, 34, 0), fore_r=(30, 0, 0), head=(-6, 0, 0)))
a.pose(32, P(REST))
a.done()

# ------------------------------------------------------------------ backstep (22): crouch 0..3, back-flip 4..11, land 12, snap shot 16, rise
a = A("backstep", 22)
a.pose(0, P(REST))
a.pose(3, P(REST, body__p=(0, -2.0, 0), chest=(-14, 0, 0), leg_r=(30, 0, 2), leg_l=(30, 0, -2), shin_r=(-60, 0, 0), shin_l=(-60, 0, 0),
            foot_r=(30, 0, 0), foot_l=(30, 0, 0), arm_l=(40, 0, 10), arm_r=(-20, 0, -20)))
FLIP = dict(leg_r=(70, 0, 2), leg_l=(70, 0, -2), shin_r=(-90, 0, 0), shin_l=(-90, 0, 0), chest=(-20, 0, 0), arm_l=(60, 0, 20), arm_r=(60, 0, -30),
            fore_r=(70, 0, 0), head=(-20, 0, 0))
C = 14.0
for t, th, h in ((5, 60, 6), (7, 150, 10), (9, 250, 9), (11, 340, 3)):
    r = math.radians(th)
    a.pose(t, P(REST, FLIP, root=(th, 0, 0), root__p=(0, h + C - C * math.cos(r), -C * math.sin(r))))
a.pose(12, P(REST, root=(360, 0, 0), root__p=(0, -2.4, 0), body__p=(0, -1.0, 0), leg_r=(40, 0, 4), leg_l=(-10, 0, -4), shin_r=(-60, 0, 0), shin_l=(-30, 0, 0),
             chest=(-12, 0, 0), arm_l=(50, 0, 10), arm_r=(60, 30, -10)))
a.pose(14, P(aim(-2), root=(360, 0, 0), root__p=(0, -1.6, 0), leg_r=(30, 0, 4), leg_l=(-10, 0, -4), shin_r=(-40, 0, 0), shin_l=(-20, 0, 0)))
a.pose(17, P(aim(4), root=(360, 0, 0), root__p=(0, -1.4, 0), leg_r=(30, 0, 4), leg_l=(-10, 0, -4), shin_r=(-40, 0, 0), shin_l=(-20, 0, 0)))
a.pose(22, P(REST, root=(360, 0, 0)))
a.flashes([16], 1.1)
a.recoil([16], kick=14, back=1.0)
a.done()

# ------------------------------------------------------------------ bullet_hail (84, enraged): plant 0..10, empty the drum skyward 12..40, swing down, aimed 50..74
a = A("bullet_hail", 84)
UP = dict(arm_l=(168, 0, -6), fore_l=(0, 0, 0), rifle=(-78, 0, 0), arm_r=(150, -20, 20), fore_r=(30, 0, 0), chest=(14, 0, 0), head=(30, 0, 0),
          leg_r=(-10, 0, 10), leg_l=(10, 0, -10), body__p=(0, -0.8, 0))
a.pose(0, P(REST))
a.pose(5, P(REST, body__p=(0, -1.6, 0), chest=(-10, 0, 0), head=(-16, 0, 0), leg_r=(-6, 0, 10), leg_l=(6, 0, -10), arm_l=(30, 0, 10), arm_r=(30, 30, -10)))
a.pose(10, P(REST, UP))
for i, t in enumerate(range(12, 41, 4)):
    a.pose(t, P(REST, UP, chest=(14 + (2 if i % 2 else -2), 4 if i % 2 else -4, 0), head=(32, 0, 3 if i % 2 else -3)))
a.pose(43, P(REST, UP, chest=(4, 0, 0), head=(6, 0, 0), arm_l=(120, 0, 0)))
a.pose(48, P(aim(0), leg_r=(-10, 0, 10), leg_l=(10, 0, -10), body__p=(0, -0.8, 0)))
for i, t in enumerate(range(50, 75, 8)):
    a.pose(t, P(aim(1, -6 if i % 2 else 4), leg_r=(-10, 0, 10), leg_l=(10, 0, -10), body__p=(0, -0.8, 0)))
a.pose(76, P(aim(-6, 0), body__p=(0, -0.5, 0)))
a.pose(80, P(REST, rifle=(-40, 0, 0), head=(10, 0, 0)))
a.pose(84, P(REST))
up = list(range(12, 41, 2))
aimed = list(range(50, 75, 4))
a.flashes(up + aimed, 1.0)
a.recoil(up, kick=-5, back=0.5)
a.recoil(aimed, kick=8, back=0.8)
a.ribbon([(0, 0, 0, 0), (10, 0, 0, 0), (40, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ bayonet_lunge (30): fix bayonet 0..6, coil low 8..11, dash 12, THRUST 14, twist 17, wrench out
a = A("bayonet_lunge", 30)
a.show("bayonet", 4, 27, grow=1.5)
a.pose(0, P(REST))
a.pose(3, P(REST, arm_l=(50, 0, 10), fore_l=(40, 0, 0), rifle=(-92, 0, 0), arm_r=(60, 40, -10), fore_r=(20, 0, 0), head=(-14, 10, 0), chest=(-6, 0, 0)))
a.pose(5, P(REST, arm_l=(50, 0, 10), fore_l=(40, 0, 0), rifle=(-92, 0, 0), arm_r=(70, 44, -10), fore_r=(4, 0, 0), head=(-14, 10, 0), chest=(-6, 0, 0)))
a.pose(9, P(hip(-6, 20), arm_l=(10, 0, 8), fore_l=(70, 0, 0), rifle=(-80, 0, 0), arm_r=(30, 40, 0), fore_r=(60, 0, 0), chest=(-10, 24, 0), body=(-6, 10, 0),
            leg_r=(-30, 0, 6), leg_l=(40, 0, -6), shin_l=(-40, 0, 0), body__p=(0, -2.2, 0), head=(-8, -14, 0)))
a.pose(11, P(hip(-8, 24), arm_l=(4, 0, 8), fore_l=(74, 0, 0), rifle=(-78, 0, 0), arm_r=(26, 40, 0), fore_r=(64, 0, 0), chest=(-12, 28, 0), body=(-8, 12, 0),
             leg_r=(-32, 0, 6), leg_l=(42, 0, -6), shin_l=(-44, 0, 0), body__p=(0, -2.4, 0), head=(-8, -18, 0)))
a.pose(13, P(hip(0, -18), arm_l=(80, 0, 12), fore_l=(4, 0, 0), rifle=(-84, 0, 0), arm_r=(86, 34, 0), fore_r=(4, 0, 0), chest=(-22, -20, 0), body=(-16, -8, 0),
             leg_r=(-40, 0, 6), leg_l=(56, 0, -6), shin_l=(-20, 0, 0), shin_r=(-10, 0, 0), body__p=(0, -2.6, -1.6), head=(-10, 18, 0)))
a.pose(15, P(hip(0, -22), arm_l=(84, 0, 12), fore_l=(0, 0, 0), rifle=(-84, 0, 0), arm_r=(90, 34, 0), fore_r=(0, 0, 0), chest=(-24, -22, 0), body=(-18, -10, 0),
             leg_r=(-42, 0, 6), leg_l=(58, 0, -6), shin_l=(-18, 0, 0), shin_r=(-10, 0, 0), body__p=(0, -2.8, -2.0), head=(-10, 22, 0)))
a.pose(17, P(hip(0, -22), arm_l=(80, 0, 12), fore_l=(4, 0, 0), rifle=(-84, 0, 90), arm_r=(88, 34, 0), fore_r=(4, 0, 0), chest=(-22, -22, 0), body=(-18, -10, 0),
             leg_r=(-40, 0, 6), leg_l=(56, 0, -6), shin_l=(-18, 0, 0), body__p=(0, -2.8, -2.0), head=(-10, 22, 0)))   # twist the blade
a.pose(20, P(hip(-4, 10), arm_l=(30, 0, 10), fore_l=(50, 0, 0), rifle=(-80, 0, 0), chest=(-4, 10, 0), body=(-4, 4, 0),
             leg_r=(-20, 0, 6), leg_l=(26, 0, -6), body__p=(0, -1.4, 0.6), head=(-6, -4, 0)))   # yank back
a.pose(25, P(REST, body__p=(0, -0.6, 0), arm_r=(50, 40, -10), fore_r=(30, 0, 0), arm_l=(30, 0, 8)))
a.pose(30, P(REST))
a.done()

# ------------------------------------------------------------------ hazard_mine (36): kneel 0..8, sow three warning-triangle mines 12 / 20 / 28, stand
a = A("hazard_mine", 36)
a.scl("mine", HIDE, (3, .001, .001, .001), (5, 1, 1, 1), (12, 1, 1, 1), (12.6, .001, .001, .001), (15, .001, .001, .001), (16.5, 1, 1, 1), (20, 1, 1, 1),
      (20.6, .001, .001, .001), (23, .001, .001, .001), (24.5, 1, 1, 1), (28, 1, 1, 1), (28.6, .001, .001, .001))
MN = dict(arm_l=(20, 0, 30), fore_l=(30, 0, 0), rifle=(-40, 0, 0))   # rifle slung back against the hip
a.pose(0, P(REST))
a.pose(5, P(REST, MN, arm_r=(-30, 0, -10), fore_r=(40, 0, 0), chest=(0, -10, 0), head=(-10, -20, 0)))   # pull a mine from the coat
a.pose(8, P(REST, KNEEL, MN, arm_r=(10, 0, -16), fore_r=(60, 0, 0), chest=(-14, -6, 0), head=(-14, 0, 0)))
for t0, yaw in ((12, 0), (20, -26), (28, 26)):
    a.pose(t0 - 3, P(REST, KNEEL, MN, arm_r=(-20, -yaw, -10), fore_r=(50, 0, 0), chest=(-18, yaw * 0.6, 0), head=(-10, yaw * 0.5, 0)))
    a.pose(t0, P(REST, KNEEL, MN, arm_r=(70, -yaw, -6), fore_r=(0, 0, 0), chest=(-26, yaw, 0), head=(-6, yaw, 0)))   # slide it out across the ground
    a.pose(t0 + 2, P(REST, KNEEL, MN, arm_r=(60, -yaw, -8), fore_r=(10, 0, 0), chest=(-24, yaw, 0), head=(-6, yaw, 0)))
a.pose(31, P(REST, KNEEL, MN, chest=(-6, 0, 0), arm_r=(20, 0, -16), fore_r=(40, 0, 0)))
a.pose(36, P(REST))
a.done()

# ------------------------------------------------------------------ marksman (50): kneel + shoulder 0..10, hold breath 10..34 (laser), CRACK 36, work the bolt 40..44, stand
a = A("marksman", 50)
a.pose(0, P(REST))
a.pose(6, P(REST, KNEEL, chest=(-8, 0, 0), arm_l=(50, 0, 8), rifle=(-80, 0, 0)))
a.pose(10, P(KNEEL, aim(1, -6, head=(-4, 18, -12))))
a.pose(22, P(KNEEL, aim(1.5, -6, head=(-4, 18, -14), body__p=(0, -0.2, 0))))
a.pose(34, P(KNEEL, aim(1, -6, head=(-4, 18, -14))))
a.pose(35.5, P(KNEEL, aim(0.5, -6, head=(-4, 18, -14))))
a.pose(37, P(KNEEL, aim(22, -2, head=(10, 14, -6)), body=(8, 0, 0), root__p=(0, -4.6, 1.8)))
a.pose(40, P(KNEEL, aim(6, -4, head=(0, 14, -8)), root__p=(0, -4.6, 1.2)))
a.pose(42, P(KNEEL, aim(6, -4, head=(0, 14, -8)), arm_r=(60, 60, 0), fore_r=(60, 0, 0), root__p=(0, -4.6, 1.2)))  # pull the bolt
a.pose(44, P(KNEEL, aim(4, -4, head=(0, 14, -8)), root__p=(0, -4.6, 1.2)))
a.pose(47, P(REST, body__p=(0, -0.8, 0)))
a.pose(50, P(REST))
a.flashes([36], 1.8)
a.recoil([36], kick=8, back=1.6)
a.done()

# ------------------------------------------------------------------ death (40): shot stagger 0..6, sag to her knees 12, rifle slips, topple forward 24, hat rolls off
a = A("death", 40)
a.pos("hat", (0, 0, 0, 0), (20, 0, 0, 0), (24, 0, 1.0, -2.0), (28, 0, -3.0, -6.0), (32, 0, -8.0, -9.0), (40, 0, -9.0, -10.0))
a.rot("hat", (0, 0, 0, 0), (20, 0, 0, 0), (26, -30, 0, 20), (32, -70, 20, 60), (40, -80, 20, 70))
a.pose(0, P(REST))
a.pose(3, P(REST, chest=(18, 10, 0), head=(26, 0, 6), body=(6, 0, 0), arm_l=(30, 0, 30), arm_r=(10, 0, -40), body__p=(0, 0, 1.0), leg_l=(-14, 0, -4)))
a.pose(7, P(REST, chest=(10, 4, 0), head=(14, 0, 4), body=(4, 0, 0), arm_l=(20, 0, 16), rifle=(-80, 0, 0), arm_r=(30, 30, -10), fore_r=(60, 0, 0),
            body__p=(0, -0.6, 1.0)))
a.pose(12, P(REST, KNEEL, leg_r=(70, 0, 4), shin_r=(-80, 0, 0), foot_r=(10, 0, 0), chest=(-10, 0, 0), head=(-20, 0, 0), arm_l=(0, 0, 10), fore_l=(10, 0, 0),
             rifle=(-30, 0, 40), arm_r=(20, 20, -10), fore_r=(40, 0, 0), root__p=(0, -5.4, 0)))
a.pose(18, P(REST, KNEEL, leg_r=(74, 0, 4), shin_r=(-84, 0, 0), chest=(-16, 0, 0), head=(-30, 0, 6), arm_l=(-6, 0, 8), fore_l=(4, 0, 0),
             rifle=(30, 0, 80), arm_r=(10, 0, -6), fore_r=(20, 0, 0), root__p=(0, -5.6, 0)))
a.pose(24, P(REST, KNEEL, leg_r=(74, 0, 4), shin_r=(-84, 0, 0), chest=(-10, 0, 0), head=(-10, 0, 10), arm_l=(150, 0, 20), arm_r=(150, 0, -20),
             rifle=(30, 0, 80), root=(-60, 0, 0), root__p=(0, -4.0, -1.0)))
a.pose(28, P(REST, leg_r=(20, 0, 4), leg_l=(10, 0, -4), shin_r=(-20, 0, 0), shin_l=(-10, 0, 0), chest=(4, 0, 0), head=(10, 20, 0),
             arm_l=(160, 0, 30), arm_r=(160, 0, -30), rifle=(30, 0, 80), root=(-92, 0, 0), root__p=(0, -0.2, -1.0)))
a.pose(31, P(REST, leg_r=(14, 0, 4), leg_l=(6, 0, -4), chest=(0, 0, 0), head=(6, 30, 0), arm_l=(166, 0, 34), arm_r=(160, 0, -36), rifle=(30, 0, 80),
             root=(-88, 0, 0), root__p=(0, 0.4, -1.0)))
a.pose(34, P(REST, leg_r=(10, 0, 4), leg_l=(4, 0, -4), chest=(2, 0, 0), head=(8, 34, 0), arm_l=(168, 0, 36), arm_r=(162, 0, -38), rifle=(30, 0, 80),
             root=(-90, 0, 0), root__p=(0, -0.2, -1.0)))
a.pose(40, P(REST, leg_r=(10, 0, 4), leg_l=(4, 0, -4), chest=(2, 0, 0), head=(8, 34, 0), arm_l=(168, 0, 36), arm_r=(162, 0, -38), rifle=(30, 0, 80),
             root=(-90, 0, 0), root__p=(0, -0.2, -1.0)))
a.flashes([])
a.done()

os.makedirs(os.path.dirname(OUT), exist_ok=True)
m.save(OUT)
print("cubes", len(m.cubes), "anims", [(x["name"], x["length"]) for x in m.anims])
