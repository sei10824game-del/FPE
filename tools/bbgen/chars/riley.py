"""Riley (original FPE student) - generates assets/fpe/bbmodels/riley.bbmodel.
Reference: docs/ref/confirmed/riley.png. Paper-cutout girl (hitbox 0.6 x 1.7): big round white head with ONE huge staring
eye, an enormous toothy grin with two long fangs, white hair with a swept fringe + a flaring white ponytail tied with a small
black bow (the "bat ear"), white short-sleeve shirt (flared, jagged sleeves, collar, two buttons, chest/hem pocket), teal-grey
cel shadow bands, dark stick limbs with a clawed left hand, big dark trapezoid boots, a thin black devil tail with an arrow
tip, and a dark KNIFE in the right hand.
Blockbench space: Y up, ground 0, faces -Z. Character's RIGHT = +X.
Rotation signs: arm/leg rx>0 = swing forward, torso/head rx>0 = lean back, ry>0 = turn to the character's left,
rz>0 = toward +X. Position z<0 = forward, y>0 = up. Knife blade points along -Z at rest: blade dir = arm rx + knife rx
(0 = forward, 90 = up, -50 = forward-down).
Every key tick matches entity/characters/Riley.java.  Run: python3 tools/bbgen/chars/riley.py
"""
import math, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from bbgen import Model, mix  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "../../../src/main/resources/assets/fpe/bbmodels/riley.bbmodel")

WH, WH_L, WH_D = 0xE7E9E4, 0xF7F8F4, 0xC4CAC5
SH, SH_D = 0x8FA7A4, 0x6C8481           # teal-grey cel shadow
HAIR, HAIR_D = 0xEFF1EC, 0xB5C0BC
LINE = 0x17131C
DK, DK_L, DK_D = 0x3B3447, 0x574D66, 0x241F2C   # dark limbs / boots / tail
BLADE, BLADE_E, HANDLE = 0x2C2834, 0x8A8498, 0x1E1A22
GUARD = 0x5E5868
CLEAR = (0, 0, 0, 0)

m = Model("riley", S=8, atlas=2048)
R = m.rng
ALL = ("north", "south", "east", "west", "up", "down")


# ------------------------------------------------------------------ painters
def all_faces(fn, skip=()):
    return {k: fn for k in ALL if k not in skip}


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
                F.px(x, y, mix(base, dark, 0.04 + 0.28 * k * k + (0.1 if x < 2 or x > F.w - 3 else 0)))
        for i in range(n):
            x = int((i + 0.5) * F.w / n) + R.randint(-2, 2)
            for y in range(int(F.h * 0.35), F.h):
                F.px(x, y, mix(base, SH, 0.45))
        if ink: outline()(F)
    return f


def shadowband(x0, x1, slope=0.6, w=0.35):
    """diagonal teal-grey cel-shadow band across a face (art: light falls from the upper right)"""
    def f(F):
        for y in range(F.h):
            for x in range(F.w):
                u = (x - x0 * F.w + y * slope) / F.w
                if 0 <= u <= w and x0 * F.w <= x + y * slope <= x1 * F.w + y * slope:
                    F.px(x, y, mix(SH, SH_D, 0.2 * y / F.h))
        outline()(F)
    return f


def dark(base=DK, ink=True):
    def f(F):
        for y in range(F.h):
            for x in range(F.w):
                F.px(x, y, mix(DK_L, base, min(1, 0.5 + 0.7 * y / max(1, F.h))) if R.random() > 0.04 else DK_L)
        if ink: outline(DK_D)(F)
    return f


def hairp(base=HAIR, ink=True):
    def f(F):
        for y in range(F.h):
            for x in range(F.w):
                F.px(x, y, mix(WH_L, base, min(1, 0.3 + y / max(1, F.h))))
        for x in range(1, F.w, 4):
            xx = x + R.randint(0, 1)
            for y in range(R.randint(2, 5), F.h - 1):
                F.px(xx, y, mix(base, HAIR_D, 0.55))
        if ink: outline()(F)
    return f


def spikep(tip_left, col=HAIR, edge=LINE, shade=HAIR_D):
    def f(F):
        for y in range(F.h):
            for x in range(F.w):
                u = (x + .5) / F.w
                u = 1 - u if not tip_left else u
                half = 0.5 * u
                v = abs((y + .5) / F.h - 0.5)
                if v > half: F.px(x, y, CLEAR)
                elif v > half - 1.3 / F.h: F.px(x, y, edge)
                else: F.px(x, y, mix(col, shade, 0.3 * (1 - u) + 0.2 * (y / F.h)))
    return f


def toothp(down, col=WH_L, edge=LINE):
    def f(F):
        for y in range(F.h):
            for x in range(F.w):
                v = (y + .5) / F.h
                v = v if down else 1 - v
                half = 0.5 * (1 - v)
                d = abs((x + .5) / F.w - 0.5)
                if d > half + 0.02: F.px(x, y, CLEAR)
                elif d > half - 1.2 / F.w: F.px(x, y, edge)
                else: F.px(x, y, mix(col, WH_D, 0.4 * v))
    return f


def clear(F):
    F.rect(0, 0, F.w, F.h, CLEAR)


def face_front(F):
    W, H = F.w, F.h
    for y in range(H):
        for x in range(W):
            F.px(x, y, mix(WH_L, WH, 0.2 + 0.6 * y / H))
    # teal-grey shadow under the fringe on the character's right cheek (texel left), slanting down-right like the art
    F.poly([(0, 10), (20, 10), (12, 26), (0, 34)], SH)
    F.poly([(0, 30), (6, 27), (3, 36), (0, 38)], SH_D)
    # huge staring eye (char right) + a smaller squinting eye half hidden under the long lock (char left)
    ex, ey = 20, 22
    F.disc(ex, ey, 10.8, LINE)
    F.disc(ex, ey, 8.9, WH_L)
    F.disc(ex + 1.4, ey + 1.2, 2.4, LINE)
    F.disc(ex + 1.4, ey + 1.2, 1.0, 0x5A1E2A, glow=True)
    F.line(ex - 6, ey - 4, ex - 3, ey - 6, WH_D, 1)
    F.disc(41, 24, 6.4, LINE)
    F.disc(41, 24, 4.9, WH_L)
    F.disc(40, 24.5, 1.5, LINE)
    F.rect(34, 16, 15, 4, SH)           # lid shadow from the lock
    # GRIN: wide, corners curling up into the cheeks, two rows of teeth, zig-zag bite line, ink outline
    top = lambda x: 36 - 3.5 * math.exp(-((x - 5) / 3.0) ** 2) - 3.5 * math.exp(-((x - 49) / 3.0) ** 2)
    bot = lambda x: 37.5 + 14 * math.sin(math.pi * min(1, max(0, (x - 4) / 46)))
    for x in range(3, 52):
        for y in range(int(top(x)), int(bot(x)) + 1):
            F.px(x, y, WH_L)
    mid = lambda x: top(x) + (bot(x) - top(x)) * 0.48
    for x in range(5, 50):
        zz = mid(x) + (1.4 if (x // 3) % 2 else -1.4) * min(1, (bot(x) - top(x)) / 9)
        F.px(x, int(zz), LINE)
        F.px(x, int(zz) + 1, mix(LINE, WH_D, 0.5))
    for x in range(8, 50, 5):
        F.line(x, top(x) + 1, x, mid(x) - 1, WH_D, 1)
        F.line(x + 2, mid(x) + 2, x + 2, bot(x) - 1, WH_D, 1)
    # the two long fangs (art: upper canines hanging well below the bite line)
    for fx in (14, 38):
        F.poly([(fx - 3.5, top(fx)), (fx + 3.5, top(fx)), (fx + 0.5, top(fx) + 13), (fx - 0.5, top(fx) + 13)], LINE)
        F.poly([(fx - 2.4, top(fx) + 0.5), (fx + 2.4, top(fx) + 0.5), (fx + 0.2, top(fx) + 11.5), (fx - 0.2, top(fx) + 11.5)], WH_L)
    for x in range(3, 52):
        for k in (0, 1):
            F.px(x, int(top(x)) - 1 - k, LINE)
            F.px(x, int(bot(x)) + 1 + k, LINE)
    F.line(2, 31, 4, 35, LINE, 1)
    F.line(52, 31, 50, 35, LINE, 1)


def knife_side(tip_left):
    """blade profile on the side faces: dark steel, pale bevelled edge on the bottom, blood fleck"""
    def f(F):
        for y in range(F.h):
            for x in range(F.w):
                c = BLADE if y < F.h - 2 else BLADE_E
                if y == 1: c = mix(BLADE, BLADE_E, 0.4)
                F.px(x, y, c)
        F.rect(0, 0, F.w, 1, LINE)
    return f


def pocketp(F):
    cloth(n=1, ink=True)(F)
    x0, x1, y0, y1 = int(F.w * 0.55), int(F.w * 0.88), int(F.h * 0.22), int(F.h * 0.7)
    F.rect(x0, y0, x1 - x0, 1, LINE)
    F.rect(x0, y0, 1, y1 - y0 - 3, LINE)
    F.rect(x1, y0, 1, y1 - y0 - 3, LINE)
    for x in range(x0, x1 + 1):
        F.px(x, int(y1 - 3 + 3 * math.sin(math.pi * (x - x0) / max(1, x1 - x0))), LINE)


def shirt_front(F):
    cloth(n=0, ink=False)(F)
    # diagonal shadow band running from the right shoulder (texel left top) down across like the art
    F.poly([(0, 6), (F.w * 0.25, 0), (F.w, F.h * 0.55), (F.w, F.h * 0.85)], SH)
    F.rect(F.w // 2, 0, 1, F.h, mix(WH_D, LINE, 0.4))
    for by in (0.4, 0.75):
        F.disc(F.w // 2 + 4, F.h * by, 1.8, LINE)
        F.disc(F.w // 2 + 4, F.h * by, 0.9, WH_L)
    outline()(F)


def sleevep(F):
    cloth(n=1)(F)
    F.rect(0, F.h - 3, F.w, 2, SH)


# ------------------------------------------------------------------ shape helpers
def spike(name, parent, base, length, h, d, yaw, roll, col=HAIR, side=1, edge=LINE, shade=HAIR_D, pitch=0):
    x, y, z = base
    x0, x1 = (x, x + length) if side > 0 else (x - length, x)
    p_n, p_s = spikep(side > 0, col, edge, shade), spikep(side < 0, col, edge, shade)
    m.cube(name, parent, (x0, y - h / 2, z - d / 2), (x1, y + h / 2, z + d / 2), col, origin=base, rot=(pitch, yaw, roll),
           faces={"north": p_n, "south": p_s, "up": clear, "down": clear, "east": clear, "west": clear})


def tooth(name, parent, c, w, h, down=True, col=WH_L, rot=(0, 0, 0), d=None, edge=LINE):
    x, y, z = c
    d = d or w
    y0, y1 = (y - h, y) if down else (y, y + h)
    p = toothp(down, col, edge)
    m.cube(name, parent, (x - w / 2, y0, z - d / 2), (x + w / 2, y1, z + d / 2), col, origin=c, rot=rot,
           faces={"north": p, "south": p, "east": p, "west": p, "up": clear, "down": clear})


def knife(prefix, parent, hx, hy, hz, L=4.0):
    """knife along -Z from a fist at (hx,hy,hz)"""
    m.cube(prefix + "_handle", parent, (hx - 0.22, hy - 0.32, hz - 0.5), (hx + 0.22, hy + 0.32, hz + 1.0), HANDLE,
           faces=all_faces(lambda F: (F.rect(0, 0, F.w, F.h, HANDLE), [F.rect(i, 0, 1, F.h, DK_L) for i in range(2, F.w, 4)])))
    m.cube(prefix + "_guard", parent, (hx - 0.42, hy - 0.62, hz - 0.78), (hx + 0.42, hy + 0.5, hz - 0.5), GUARD, faces=all_faces(outline(LINE)))
    m.cube(prefix + "_blade", parent, (hx - 0.1, hy - 0.5, hz - 0.78 - L), (hx + 0.1, hy + 0.38, hz - 0.78), BLADE,
           faces={"east": knife_side(False), "west": knife_side(True), "up": lambda F: F.rect(0, 0, F.w, F.h, LINE),
                  "down": lambda F: F.rect(0, 0, F.w, F.h, BLADE_E), "north": outline(LINE), "south": outline(LINE)})
    tipz = hz - 0.78 - L
    # tip: triangle in the side view, sloping from the spine down to the edge
    def tipf(left):
        def f(F):
            for y in range(F.h):
                for x in range(F.w):
                    u = (x + .5) / F.w
                    u = u if not left else 1 - u          # u=0 at the blade, 1 at the point
                    if (y + .5) / F.h < u * 0.85: F.px(x, y, CLEAR)
                    else: F.px(x, y, BLADE_E if y >= F.h - 2 else BLADE)
        return f
    m.cube(prefix + "_tip", parent, (hx - 0.1, hy - 0.5, tipz - 1.3), (hx + 0.1, hy + 0.38, tipz), BLADE,
           faces={"east": tipf(False), "west": tipf(True), "up": clear, "down": clear, "north": clear, "south": clear})


# ------------------------------------------------------------------ skeleton
m.group("root", (0, 0, 0))
m.group("body", (0, 10.0, 0), parent="root")
m.group("chest", (0, 12.2, 0), parent="body")
m.group("head", (0, 18.6, 0), parent="chest")
m.group("bangs", (0, 26.6, -3.5), parent="head")
m.group("lock", (-2.0, 25.6, -3.5), parent="head")
m.group("pony", (0, 27.0, 2.6), parent="head", rot=(52, 0, 0))
m.group("pony2", (0, 30.2, 2.6), parent="pony")
m.group("bow", (0, 27.8, 1.2), parent="head")
m.group("hem", (0, 12.2, 0), parent="body")
m.group("arm_r", (3.0, 17.4, 0), parent="chest")
m.group("fore_r", (3.2, 13.8, 0), parent="arm_r")
m.group("hand_r", (3.2, 10.4, 0), parent="fore_r")
m.group("knife", (3.2, 9.8, 0), parent="hand_r")
m.group("arm_l", (-3.0, 17.4, 0), parent="chest")
m.group("fore_l", (-3.2, 13.8, 0), parent="arm_l")
m.group("hand_l", (-3.2, 10.4, 0), parent="fore_l")
m.group("fan", (-3.2, 9.8, 0), parent="hand_l")
m.group("tail", (0, 10.4, 1.6), parent="body", rot=(38, 0, 0))
m.group("tail2", (0, 10.4, 4.6), parent="tail", rot=(-30, 0, 0))
m.group("tail3", (0, 10.4, 7.4), parent="tail2", rot=(-34, 0, 0))
for s, k in ((1, "r"), (-1, "l")):
    m.group("leg_" + k, (1.1 * s, 10.0, 0), parent="root")
    m.group("shin_" + k, (1.1 * s, 6.4, 0), parent="leg_" + k)

# ------------------------------------------------------------------ legs: dark sticks + big trapezoid boots
for s, k in ((1, "r"), (-1, "l")):
    x = 1.1 * s
    m.cube("thigh_" + k, "leg_" + k, (x - 0.32, 6.2, -0.32), (x + 0.32, 10.0, 0.32), DK, faces=all_faces(dark()))
    m.cube("calf_" + k, "shin_" + k, (x - 0.3, 3.2, -0.3), (x + 0.3, 6.5, 0.3), DK, faces=all_faces(dark()))
    m.cube("knee_" + k, "shin_" + k, (x - 0.38, 6.0, -0.38), (x + 0.38, 6.8, 0.38), DK_D)
    m.cube("bootshaft_" + k, "shin_" + k, (x - 0.9, 1.6, -0.9), (x + 0.9, 3.9, 0.9), DK, origin=(x, 2.0, 0), rot=(0, 0, -6 * s),
           faces=all_faces(dark(), ("down",)))
    m.cube("bootcuff_" + k, "shin_" + k, (x - 1.05, 3.5, -1.05), (x + 1.05, 4.1, 1.05), DK_L, faces=all_faces(outline(DK_D)))
    m.cube("boot_" + k, "shin_" + k, (x - 1.25, 0.0, -2.1), (x + 1.25, 1.9, 1.1), DK, faces=all_faces(dark()))
    m.cube("toe_" + k, "shin_" + k, (x - 1.0, 0.0, -2.9), (x + 1.0, 1.2, -2.0), DK, origin=(x, 0, -2.0), rot=(0, 0, 0), faces=all_faces(dark()))
    m.cube("sole_" + k, "shin_" + k, (x - 1.3, -0.02, -2.95), (x + 1.3, 0.3, 1.15), DK_D)

# ------------------------------------------------------------------ shirt: flared white shirt, collar, buttons, pocket, shadow band
m.cube("torso", "chest", (-2.6, 14.4, -1.4), (2.6, 18.2, 1.4), WH,
       faces={"north": shirt_front, "south": cloth(n=2), "east": cloth(n=1), "west": cloth(n=1), "up": cloth(n=0), "down": cloth(n=0)})
m.cube("waist", "body", (-2.9, 11.6, -1.6), (2.9, 14.6, 1.6), WH,
       faces={"north": combo(cloth(n=0), lambda F: F.poly([(F.w * 0.4, 0), (F.w, 0), (F.w, F.h * 0.4)], SH), outline()),
              "south": cloth(n=2), "east": cloth(n=1), "west": cloth(n=1), "up": clear, "down": cloth(n=0)})
m.cube("shoulders", "chest", (-2.9, 17.4, -1.3), (2.9, 18.3, 1.3), WH, faces=all_faces(cloth(n=0)))
# hem flare panels (hinged at the waist line)
m.cube("hem_fill", "hem", (-3.0, 9.3, -1.6), (3.0, 12.2, 1.6), WH, faces=all_faces(cloth(n=0, ink=False)))
m.cube("hem_f", "hem", (-3.3, 9.0, -1.95), (3.3, 12.2, -1.65), WH, origin=(0, 12.2, -1.8), rot=(10, 0, 0),
       faces={"north": pocketp, "south": cloth(n=0), "east": cloth(n=0), "west": cloth(n=0), "up": clear, "down": outline()})
m.cube("hem_b", "hem", (-3.3, 9.0, 1.65), (3.3, 12.2, 1.95), WH, origin=(0, 12.2, 1.8), rot=(-10, 0, 0), faces=all_faces(cloth(n=2), ("up",)))
for s, k in ((1, "r"), (-1, "l")):
    m.cube("hem_" + k, "hem", (3.0 * s - 0.15, 9.0, -1.9), (3.0 * s + 0.15, 12.2, 1.9), WH, origin=(3.0 * s, 12.2, 0), rot=(0, 0, 9 * s),
           faces=all_faces(cloth(n=1), ("up",)))
    # little jagged corner flicks of the hem
    spike("hemflick_" + k, "hem", (3.3 * s, 9.4, -1.85), 1.0, 1.0, 0.25, 0, -30 * s, col=WH, side=s, shade=WH_D)
# collar: neck ring + two pointed flaps
m.cube("collar", "chest", (-1.3, 18.0, -1.2), (1.3, 18.7, 1.1), WH, faces=all_faces(outline()))
for s, k in ((1, "r"), (-1, "l")):
    m.cube("collarflap_" + k, "chest", (0.05 * s if s > 0 else -1.75, 16.4, -1.62), (1.75 if s > 0 else -0.05, 18.4, -1.42), WH,
           origin=(0.0, 18.4, -1.5), rot=(0, 0, 8 * s), faces={"north": toothp(True, WH_L), "south": clear, "east": clear, "west": clear, "up": clear, "down": clear})
m.cube("neck", "chest", (-0.33, 18.0, -0.33), (0.33, 19.4, 0.33), DK, faces=all_faces(dark()))

# ------------------------------------------------------------------ arms: flared jagged short sleeves, dark stick arms
for s, k in ((1, "r"), (-1, "l")):
    x = 3.2 * s
    a, f, h = "arm_" + k, "fore_" + k, "hand_" + k
    m.cube("sleeve_" + k, a, (x - 1.0, 15.4, -1.25), (x + 1.0, 18.3, 1.25), WH, origin=(3.0 * s, 17.6, 0), rot=(0, 0, 10 * s),
           faces=all_faces(sleevep))
    spike("slvspk0_" + k, a, (x + 0.8 * s, 15.7, -0.6), 1.6, 1.1, 0.3, 0, -28 * s, col=WH, side=s, shade=WH_D)
    spike("slvspk1_" + k, a, (x + 0.6 * s, 15.6, 0.7), 1.3, 0.9, 0.3, 0, -44 * s, col=WH, side=s, shade=WH_D)
    m.cube("upper_" + k, a, (x - 0.3, 13.6, -0.3), (x + 0.3, 15.8, 0.3), DK, faces=all_faces(dark()))
    m.cube("elbow_" + k, f, (x - 0.36, 13.4, -0.36), (x + 0.36, 14.2, 0.36), DK_D)
    m.cube("forearm_" + k, f, (x - 0.28, 10.4, -0.28), (x + 0.28, 13.8, 0.28), DK, faces=all_faces(dark()))
    m.cube("fist_" + k, h, (x - 0.5, 9.3, -0.5), (x + 0.5, 10.6, 0.5), DK, faces=all_faces(dark()))
    m.cube("thumb_" + k, h, (x - 0.25, 9.8, -0.75), (x + 0.25, 10.4, -0.4), DK_L)
# left hand: open spiky claw (art: splayed dark fingers)
for i, (dx, dz, rz, rx) in enumerate(((-0.35, -0.3, -18, 12), (0.0, -0.45, -4, 20), (0.35, -0.3, 10, 14), (0.0, 0.35, 0, -18))):
    tooth(f"claw{i}", "hand_l", (-3.2 + dx, 9.4, dz), 0.42, 1.6, down=True, col=DK, rot=(rx, 0, rz), edge=DK_D)
# right hand: the knife
knife("knife", "knife", 3.2, 9.8, 0.0, L=3.6)
# fan of three spare knives (left hand, knife_fan)
for i, yaw in enumerate((-22, 0, 22)):
    m.group(f"fank{i}", (-3.2, 9.8, 0), parent="fan", rot=(0, yaw, 0))
    knife(f"fan{i}", f"fank{i}", -3.2, 9.8, 0.0, L=2.6)

# ------------------------------------------------------------------ tail: thin black devil tail, arrow tip
m.cube("tail_a", "tail", (-0.24, 10.16, 1.6), (0.24, 10.64, 4.8), DK, faces=all_faces(dark()))
m.cube("tail_b", "tail2", (-0.2, 10.2, 4.5), (0.2, 10.6, 7.6), DK, faces=all_faces(dark()))
m.cube("tail_c", "tail3", (-0.17, 10.23, 7.3), (0.17, 10.57, 9.6), DK, faces=all_faces(dark()))
# spade/arrow tip: flat diamond standing in the Y/Z plane (reads in profile like the art) + inner bevel
m.cube("arrow", "tail3", (-0.13, 9.4, 9.3), (0.13, 11.4, 11.3), DK, origin=(0, 10.4, 10.3), rot=(45, 0, 0), faces=all_faces(dark()))
m.cube("arrow_in", "tail3", (-0.18, 10.0, 9.9), (0.18, 10.8, 10.7), DK_L, origin=(0, 10.4, 10.3), rot=(45, 0, 0))


# ------------------------------------------------------------------ head: round white head (core + bevels), face, fangs
def headside(F):
    for y in range(F.h):
        for x in range(F.w):
            F.px(x, y, mix(WH_L, WH, 0.3 + 0.6 * y / F.h))
    outline()(F)


m.cube("skull", "head", (-3.4, 19.6, -3.2), (3.4, 26.2, 3.2), WH,
       faces={"north": face_front, "south": hairp(), "east": headside, "west": headside, "up": hairp(), "down": headside})
m.cube("skull_w", "head", (-3.85, 20.4, -2.7), (3.85, 25.4, 2.7), WH,
       faces={"north": headside, "south": hairp(), "east": headside, "west": headside, "up": clear, "down": headside})
m.cube("skull_h", "head", (-2.8, 19.1, -2.7), (2.8, 26.6, 2.7), WH,
       faces={"north": headside, "south": hairp(), "east": headside, "west": headside, "up": hairp(), "down": headside})
for s, x in ((1, 1.62), (-1, -1.18)):
    tooth("fang_" + ("r" if s > 0 else "l"), "head", (x, 22.0, -3.32), 0.62, 1.5, down=True, d=0.18)
# hair cap (top + back), the forehead fringe hangs over it
m.cube("hair_cap", "head", (-3.75, 24.9, -3.45), (3.75, 27.3, 3.6), HAIR, faces=all_faces(hairp()))
m.cube("hair_top", "head", (-3.0, 27.2, -2.9), (3.0, 27.9, 3.1), HAIR, faces=all_faces(hairp()))
m.cube("hair_back", "head", (-3.9, 20.2, 2.9), (3.9, 25.6, 3.75), HAIR, faces=all_faces(hairp()))
for i, x in enumerate((-3.0, -1.0, 1.0, 3.0)):
    tooth(f"backtip{i}", "head", (x, 20.3, 3.3), 1.8, 1.6, down=True, col=HAIR, d=0.8)
# side hair: panels down the temples ending in points (hides the boxy head sides)
for s_, k in ((1, "r"), (-1, "l")):
    m.cube("side_" + k, "head", (3.75 * s_ - 0.35, 21.6, -3.0), (3.75 * s_ + 0.35, 26.0, 3.2), HAIR, faces=all_faces(hairp()))
    for i, z in enumerate((-2.2, -0.2, 1.8)):
        tooth(f"sidetip{i}_{k}", "head", (3.75 * s_, 21.7, z), 0.7, 1.6, down=True, col=HAIR, d=1.8)
# fringe: pointed blades swept toward the character's right (+X) like the art, tips at different heights
BANGS = [(-3.6, 1.6, 24.9, 4), (-2.1, 1.7, 24.6, 8), (-0.5, 1.8, 24.7, 12), (1.1, 1.7, 24.5, 16), (2.6, 1.4, 24.2, 22)]
for i, (x, w, yb, rz) in enumerate(BANGS):
    m.cube(f"bang{i}", "bangs", (x, yb, -3.85), (x + w, 26.8, -3.45), HAIR, origin=(x + w / 2, 26.8, -3.65), rot=(0, 0, rz),
           faces={"north": combo(hairp(), lambda F: [F.px(xx, yy, CLEAR) for yy in range(F.h - 9, F.h) for xx in range(F.w)
                                                     if abs(xx + .5 - F.w * 0.3) > (F.h - yy) * F.w / 16]),
                  "south": hairp(), "east": hairp(), "west": hairp(), "up": hairp(), "down": clear})
# big swept spikes sticking out on the character's right (art: pointed locks flaring beside the face)
spike("rspk0", "bangs", (3.4, 24.6, -2.6), 3.6, 2.2, 1.0, 10, -18, side=1)
spike("rspk1", "bangs", (3.6, 22.6, -1.6), 3.0, 1.8, 0.9, 6, 20, side=1)
spike("rspk2", "head", (3.6, 26.0, 0.8), 2.4, 1.6, 1.0, -10, -32, side=1)
# char-left: a long lock hanging over the small eye
m.cube("lock0", "lock", (-2.9, 21.6, -3.9), (-1.1, 25.6, -3.5), HAIR, origin=(-2.0, 25.6, -3.7), rot=(0, 0, -6),
       faces={"north": combo(hairp(), lambda F: F.poly([(0, F.h), (F.w * 0.25, F.h - 7), (F.w, F.h)], CLEAR)), "south": hairp(),
              "east": hairp(), "west": hairp(), "up": hairp(), "down": clear})
spike("lspk0", "lock", (-3.6, 23.4, -2.2), 1.6, 1.4, 1.0, 0, 22, side=-1)
# ponytail: flaring white wedge sticking up/back (art: the big white shape behind the head), bow at its root
m.cube("pony_a", "pony", (-1.2, 26.8, 1.6), (1.2, 30.4, 3.6), HAIR, faces=all_faces(hairp()))
m.cube("pony_b", "pony2", (-1.9, 30.0, 1.4), (1.9, 33.2, 3.8), HAIR, faces=all_faces(hairp()))
for i, (x, rz) in enumerate(((-1.4, -14), (0.0, 0), (1.4, 14))):
    tooth(f"ponytip{i}", "pony2", (x, 33.1, 2.6), 1.4, 2.2, down=False, col=HAIR, d=2.0, rot=(0, 0, rz))
for s, k in ((1, "r"), (-1, "l")):
    tooth("bowloop_" + k, "bow", (1.25 * s, 27.9, 1.2), 2.4, 3.3, down=False, col=DK, rot=(-8, 0, -24 * s), d=0.6, edge=DK_D)
m.cube("bowknot", "bow", (-0.55, 27.6, 0.8), (0.55, 28.5, 1.7), DK_D)


# ================================================================== animation
PROPS = ["fan"]
HIDE = (.001, .001, .001)


class A:
    def __init__(self, name, ticks, loop=False):
        self.name, self.ticks, self.loop, self.tr = name, ticks, loop, {}

    def k(self, bone, ch, keys):
        self.tr.setdefault(bone, {}).setdefault(ch, []).extend(keys)
        return self

    def rot(self, bone, *keys): return self.k(bone, "rotation", keys)
    def pos(self, bone, *keys): return self.k(bone, "position", keys)
    def scl(self, bone, *keys): return self.k(bone, "scale", keys)

    def _frame(self, keys, zero):
        ks = list(keys)
        if ks[0][0] > 0: ks.insert(0, (0, *zero))
        if ks[-1][0] < self.ticks and not self.loop: ks.append((self.ticks, *zero))
        return ks

    def r(self, bone, *keys): return self.rot(bone, *self._frame(keys, (0, 0, 0)))
    def p(self, bone, *keys): return self.pos(bone, *self._frame(keys, (0, 0, 0)))

    def hide(self, bone, t0, t1, grow=1.5):
        """bone vanishes at t0 (thrown) and pops back in at t1 with overshoot"""
        return self.scl(bone, (0, 1, 1, 1), (t0 - 0.3, 1, 1, 1), (t0, *HIDE), (t1, *HIDE), (t1 + grow, 1.25, 1.25, 1.25),
                        (t1 + grow + 1, 1, 1, 1), (self.ticks, 1, 1, 1))

    def show(self, bone, t0, t1, grow=2):
        return self.scl(bone, (0, *HIDE), (max(0, t0 - 0.5), *HIDE), (t0, .3, .3, .3), (t0 + grow, 1.15, 1.15, 1.15), (t0 + grow + 1, 1, 1, 1),
                        (t1, 1, 1, 1), (t1 + 0.6, *HIDE), (self.ticks, *HIDE))

    def lag(self, bone, keys, delay=2, gain=1.0):
        seen, out = set(), []
        for (t, x, y, z) in keys:
            tt = min(self.ticks, t + delay)
            if tt in seen: continue
            seen.add(tt); out.append((tt, x * gain, y * gain, z * gain))
        return self.r(bone, *out)

    def sec(self, keys, delay=2):
        """secondary motion from body impulse keys (x>0 = whip back, z>0 = toward +X): hair, ponytail, bow, hem, tail lag in a chain"""
        self.lag("bangs", [(t, -abs(x) * 0.2, 0, z * 0.3) for (t, x, y, z) in keys], delay)
        self.lag("lock", [(t, x * 0.4, 0, z * 0.5) for (t, x, y, z) in keys], delay + 1)
        self.lag("pony", [(t, x * 0.8, y * 0.3, z * 0.6) for (t, x, y, z) in keys], delay + 1)
        self.lag("pony2", [(t, x * 0.6, 0, z * 0.6) for (t, x, y, z) in keys], delay + 2)
        self.lag("bow", [(t, x * 0.5, 0, z * 0.8) for (t, x, y, z) in keys], delay + 2)
        self.lag("hem", [(t, -x * 0.3, 0, z * 0.3) for (t, x, y, z) in keys], delay)
        if "tail" not in self.tr:
            self.lag("tail", [(t, -x * 0.6, -z * 0.8, 0) for (t, x, y, z) in keys], delay + 1)
            self.lag("tail2", [(t, -x * 0.5, -z * 0.7, 0) for (t, x, y, z) in keys], delay + 2)
            self.lag("tail3", [(t, -x * 0.5, -z * 0.7, 0) for (t, x, y, z) in keys], delay + 3)
        return self

    def done(self):
        for p in PROPS:
            if p not in self.tr or "scale" not in self.tr[p]:
                self.scl(p, (0, *HIDE))
        tracks = {b: {ch: sorted([(t / 20.0, x, y, z) for (t, x, y, z) in v], key=lambda q: q[0]) for ch, v in chs.items()}
                  for b, chs in self.tr.items()}
        m.anim(self.name, self.ticks / 20.0, tracks, loop=self.loop)


def legs(a, kr, kl=None, sr=None, sl=None):
    a.r("leg_r", *kr)
    a.r("leg_l", *(kl or [(t, x, -y, -z) for (t, x, y, z) in kr]))
    if sr: a.r("shin_r", *sr)
    if sl or sr: a.r("shin_l", *(sl or sr))


def wave(n, f, step=5):
    return [(t, *f(t / n * 2 * math.pi)) for t in range(0, n + 1, step)]


# ------------------------------------------------------------------ idle (60 loop): twitchy bounce, crazed head tilts, knife twirl in the right hand
a = A("idle", 60, loop=True)
a.pos("body", *wave(60, lambda w: (0, -0.25 + 0.25 * math.cos(2 * w), 0)))
a.rot("chest", *wave(60, lambda w: (-4 + 2 * math.sin(2 * w), 0, 2 * math.sin(w))))
a.rot("head", (0, 0, 0, 8), (10, 0, 0, 10), (14, -4, 6, 18), (24, -4, 6, 20), (28, 0, 0, 6), (40, 2, -4, -6), (48, 2, -4, -8), (52, 0, 0, 8), (60, 0, 0, 8))
a.rot("arm_r", *wave(60, lambda w: (34 + 4 * math.sin(2 * w), 0, 8), 10))
a.rot("fore_r", *wave(60, lambda w: (34 + 3 * math.sin(2 * w + 1), 0, 0), 10))
a.rot("knife", (0, -40, 0, 0), (30, -40, 0, 0), (32, -40, 0, 90), (34, -40, 0, 200), (36, -40, 0, 300), (38, -40, 0, 360), (60, -40, 0, 360))
a.rot("arm_l", *wave(60, lambda w: (8 + 3 * math.sin(2 * w + 2), 0, -18 - 3 * math.sin(2 * w)), 10))
a.rot("fore_l", (0, 16, 0, 0), (60, 16, 0, 0))
a.rot("hand_l", *wave(60, lambda w: (10 * math.sin(4 * w), 0, 0)))
a.rot("leg_r", (0, 0, 0, 4), (60, 0, 0, 4))
a.rot("leg_l", (0, 0, 0, -4), (60, 0, 0, -4))
a.rot("tail", *wave(60, lambda w: (4 * math.sin(w), 14 * math.sin(2 * w), 0)))
a.rot("tail2", *wave(60, lambda w: (6 * math.sin(w + 1), 16 * math.sin(2 * w - 0.8), 0)))
a.rot("tail3", *wave(60, lambda w: (8 * math.sin(w + 2), 20 * math.sin(2 * w - 1.6), 0)))
a.rot("pony", *wave(60, lambda w: (3 * math.sin(2 * w - 0.6), 0, 4 * math.sin(w))))
a.rot("pony2", *wave(60, lambda w: (4 * math.sin(2 * w - 1.2), 0, 5 * math.sin(w - 0.5))))
a.rot("hem", *wave(60, lambda w: (1.5 * math.sin(2 * w - 0.5), 0, 0), 10))
a.done()

# ------------------------------------------------------------------ walk (20 loop): hunched stalking skip, knife held low and ready, tail bobbing
a = A("walk", 20, loop=True)
a.pos("body", (0, 0, 0, 0), (3, 0, 0.7, 0), (5, 0, 0, 0), (10, 0, 0, 0), (13, 0, 0.7, 0), (15, 0, 0, 0), (20, 0, 0, 0))
a.rot("body", (0, -4, 6, 0), (5, -6, 0, 0), (10, -4, -6, 0), (15, -6, 0, 0), (20, -4, 6, 0))
a.rot("chest", (0, -6, -4, 0), (10, -6, 4, 0), (20, -6, -4, 0))
a.rot("leg_r", (0, 30, 0, 0), (5, 0, 0, 0), (10, -28, 0, 0), (15, 0, 0, 0), (20, 30, 0, 0))
a.rot("leg_l", (0, -28, 0, 0), (5, 0, 0, 0), (10, 30, 0, 0), (15, 0, 0, 0), (20, -28, 0, 0))
a.rot("shin_r", (0, 0, 0, 0), (12, -36, 0, 0), (16, -12, 0, 0), (20, 0, 0, 0))
a.rot("shin_l", (0, 0, 0, 0), (2, -36, 0, 0), (6, -12, 0, 0), (10, 0, 0, 0), (20, 0, 0, 0))
a.rot("arm_r", (0, -10, 0, 0), (10, 12, 0, 0), (20, -10, 0, 0))
a.rot("arm_l", (0, 22, 0, 0), (10, -20, 0, 0), (20, 22, 0, 0))
a.rot("head", (0, 2, 0, -4), (5, -2, 0, 0), (10, 2, 0, 4), (15, -2, 0, 0), (20, 2, 0, -4))
a.rot("pony", (0, 8, 0, 4), (5, -4, 0, 0), (10, 8, 0, -4), (15, -4, 0, 0), (20, 8, 0, 4))
a.rot("pony2", (0, 6, 0, 6), (6, -6, 0, 0), (10, 6, 0, -6), (16, -6, 0, 0), (20, 6, 0, 6))
a.rot("tail", (0, 6, 12, 0), (5, -4, 0, 0), (10, 6, -12, 0), (15, -4, 0, 0), (20, 6, 12, 0))
a.rot("tail2", (0, 4, 14, 0), (6, -6, 0, 0), (10, 4, -14, 0), (16, -6, 0, 0), (20, 4, 14, 0))
a.rot("tail3", (0, 4, 18, 0), (7, -8, 0, 0), (10, 4, -18, 0), (17, -8, 0, 0), (20, 4, 18, 0))
a.rot("hem", (0, 3, 0, 0), (5, -2, 0, 0), (10, 3, 0, 0), (15, -2, 0, 0), (20, 3, 0, 0))
a.done()

# ------------------------------------------------------------------ slash_combo (32): forehand slash t7, backhand t13, pull back 15-18, THRUST stab t21
a = A("slash_combo", 32)
a.r("chest", (4, 4, -38, 0), (6, 0, -42, 0), (7, -6, 30, 0), (9, -4, 40, 0), (11, -2, 42, 0), (13, -8, -34, 0), (16, 0, -24, 0), (18, 2, -20, 0), (21, -16, 6, 0), (25, -10, 4, 0), (30, 0, 0, 0))
a.r("arm_r", (4, 70, 0, 60), (6, 74, 0, 66), (7, 84, 0, -26), (9, 80, 0, -40), (11, 82, 0, -38), (13, 86, 0, 58), (16, 30, 0, 30), (18, 10, 0, 20), (21, 96, 0, 0), (25, 80, 0, 4), (30, 20, 0, 4))
a.r("fore_r", (6, 20, 0, 0), (7, 0, 0, 0), (11, 30, 0, 0), (13, 0, 0, 0), (16, 70, 0, 0), (18, 84, 0, 0), (21, 0, 0, 0), (25, 10, 0, 0), (30, 20, 0, 0))
a.r("knife", (4, -70, 0, 0), (7, -80, 0, 0), (13, -80, 0, 0), (18, -100, 0, 0), (21, -96, 0, 0), (25, -90, 0, 0), (30, -30, 0, 0))
a.r("arm_l", (4, 20, 0, -40), (7, -20, 0, -50), (13, 30, 0, -30), (18, 40, 0, -20), (21, -30, 0, -40), (28, 0, 0, -10))
a.r("fore_l", (7, 20, 0, 0), (21, 30, 0, 0))
a.r("head", (4, 0, 24, 10), (7, -4, -16, -6), (11, 0, -20, -8), (13, -4, 20, 8), (18, 2, 14, 12), (21, -10, -4, 0), (26, 0, 0, 10))
a.p("body", (4, 0, -0.4, 0.4), (7, 0, -0.5, -1.0), (13, 0, -0.5, -1.8), (18, 0, -0.6, -1.4), (21, 0, -1.0, -3.0), (25, 0, -0.6, -2.4), (30, 0, 0, -0.6))
legs(a, [(4, -8, 0, 4), (7, -20, 0, 4), (13, -12, 0, 6), (18, -6, 0, 4), (21, -36, 0, 0), (25, -30, 0, 0), (30, 0, 0, 0)],
     [(4, 10, 0, -4), (7, 20, 0, -4), (13, 14, 0, -6), (21, 34, 0, 0), (25, 28, 0, 0), (30, 0, 0, 0)],
     sr=[(7, 10, 0, 0), (21, 20, 0, 0), (26, 10, 0, 0)], sl=[(7, -16, 0, 0), (21, -30, 0, 0), (26, -20, 0, 0)])
a.sec([(0, 0, 0, 0), (4, -4, 0, -12), (7, 10, 0, 18), (13, 10, 0, -20), (18, -4, 0, -6), (21, 18, 0, 4), (26, 4, 0, 0), (32, 0, 0, 0)], delay=1)
a.done()

# ------------------------------------------------------------------ overhead_stab (32): the ART POSE - knife up overhead, claw out, head tilted, trembling (0-13),
#                                                                    PLUNGE t16, twist 17-21, yank out, recover
a = A("overhead_stab", 32)
a.r("chest", (8, 12, 10, -8), (10, 13, 12, -9), (12, 12, 10, -8), (13, 16, 12, -10), (16, -26, -6, 4), (19, -24, -4, 2), (23, -14, 0, 0), (30, 0, 0, 0))
a.r("arm_r", (8, 168, 0, 16), (10, 172, 0, 18), (12, 168, 0, 16), (13, 186, 0, 14), (15, 90, 0, 8), (16, 40, 0, 4), (19, 38, 0, 4), (23, 60, 0, 6), (30, 20, 0, 4))
a.r("fore_r", (8, 10, 0, 0), (13, 24, 0, 0), (16, 0, 0, 0), (23, 20, 0, 0), (30, 20, 0, 0))
a.r("knife", (8, -80, 0, 0), (13, -86, 0, 0), (16, -84, 0, 0), (17, -84, 0, 25), (19, -84, 0, -25), (21, -84, 0, 0), (26, -60, 0, 0), (30, -30, 0, 0))
a.r("arm_l", (8, 10, 0, -82), (10, 14, 0, -86), (12, 10, 0, -82), (16, 40, 0, -40), (22, 20, 0, -30), (30, 0, 0, 0))
a.r("fore_l", (8, -10, 0, -20), (16, 30, 0, 0), (26, 10, 0, 0))
a.r("hand_l", (8, 0, 0, -20), (10, 20, 0, -30), (12, 0, 0, -20), (16, 30, 0, 0))
a.r("head", (8, 8, -10, 22), (10, 10, -12, 26), (12, 8, -10, 22), (16, -18, 0, 4), (20, -14, 6, -6), (24, -6, 0, 10), (30, 0, 0, 0))
a.p("body", (8, 0, 0.3, 0.6), (13, 0, 0.6, 0.8), (16, 0, -1.4, -1.6), (20, 0, -1.2, -1.4), (26, 0, -0.4, -0.6), (32, 0, 0, 0))
legs(a, [(8, 6, 0, 14), (13, 8, 0, 16), (16, -34, 0, 6), (22, -30, 0, 6), (30, 0, 0, 0)],
     [(8, -10, 0, -16), (13, -12, 0, -18), (16, 28, 0, -6), (22, 24, 0, -6), (30, 0, 0, 0)],
     sr=[(13, 0, 0, 0), (16, 30, 0, 0), (24, 20, 0, 0)], sl=[(8, -14, 0, 0), (16, -40, 0, 0), (24, -30, 0, 0)])
a.sec([(0, 0, 0, 0), (8, -6, 0, 8), (13, -10, 0, 10), (16, 24, 0, -4), (20, 8, 0, 6), (26, 2, 0, 0), (32, 0, 0, 0)], delay=1)
a.done()

# ------------------------------------------------------------------ lunge_stab (30): coiled crouch 0-8, DASH t9, arm-extended stab t12, skid 13-18, recover
a = A("lunge_stab", 30)
a.r("chest", (6, -26, -20, 0), (8, -28, -24, 0), (10, -34, 4, 0), (12, -38, 8, 0), (17, -30, 6, 0), (24, -10, 0, 0))
a.r("arm_r", (6, -40, 0, 14), (8, -46, 0, 16), (10, 70, 0, 4), (12, 100, 0, 0), (17, 96, 0, 2), (24, 40, 0, 4))
a.r("fore_r", (6, 90, 0, 0), (8, 96, 0, 0), (10, 20, 0, 0), (12, 0, 0, 0), (18, 10, 0, 0), (26, 20, 0, 0))
a.r("knife", (6, -60, 0, 0), (10, -80, 0, 0), (12, -100, 0, 0), (18, -96, 0, 0), (26, -40, 0, 0))
a.r("arm_l", (6, 40, 0, -20), (10, -40, 0, -30), (12, -60, 0, -34), (18, -40, 0, -30), (26, 0, 0, -10))
a.r("head", (6, 14, 18, 0), (8, 18, 20, 0), (12, 30, -6, 0), (18, 26, -4, 0), (26, 0, 0, 0))
a.p("body", (6, 0, -2.4, 1.0), (8, 0, -2.8, 1.2), (10, 0, -1.2, -2.0), (12, 0, -1.6, -3.6), (17, 0, -1.6, -3.2), (24, 0, -0.4, -0.8), (30, 0, 0, 0))
legs(a, [(6, 50, 0, 0), (8, 56, 0, 0), (10, 30, 0, 0), (12, 60, 0, 0), (18, 54, 0, 0), (26, 0, 0, 0)],
     [(6, 30, 0, 0), (8, 34, 0, 0), (10, -30, 0, 0), (12, -50, 0, 0), (18, -44, 0, 0), (26, 0, 0, 0)],
     sr=[(6, -80, 0, 0), (8, -90, 0, 0), (10, -40, 0, 0), (12, -50, 0, 0), (18, -50, 0, 0), (26, 0, 0, 0)],
     sl=[(6, -60, 0, 0), (8, -66, 0, 0), (10, -10, 0, 0), (12, 0, 0, 0), (26, 0, 0, 0)])
a.sec([(0, 0, 0, 0), (8, -12, 0, 0), (12, 26, 0, 0), (18, 16, 0, 4), (26, 2, 0, 0), (30, 0, 0, 0)], delay=1)
a.done()

# ------------------------------------------------------------------ knife_throw (26): wind-up overhead 0-9, THROW t11 (knife leaves the hand), new knife flicked out t19
a = A("knife_throw", 26)
a.r("chest", (6, 12, -34, 4), (9, 14, -40, 6), (11, -14, 24, -2), (14, -10, 20, 0), (20, 0, 4, 0), (26, 0, 0, 0))
a.r("arm_r", (6, 150, 0, 18), (9, 166, 0, 20), (11, 60, 0, -10), (13, 30, 0, -16), (18, 20, 0, 0), (20, 40, 0, 20), (22, 30, 0, 8))
a.r("fore_r", (6, 40, 0, 0), (9, 60, 0, 0), (11, 0, 0, 0), (18, 20, 0, 0), (21, 50, 0, 0), (24, 30, 0, 0))
a.r("knife", (6, -60, 0, 0), (9, -70, 0, 0), (11, -60, 0, 0), (19, -40, 0, 180), (21, -40, 0, 360), (26, -40, 0, 360))
a.hide("knife", 11, 18.5)
a.r("arm_l", (6, 80, 0, 10), (9, 90, 0, 14), (11, 40, 0, -30), (14, 10, 0, -40), (22, 0, 0, -10))
a.r("fore_l", (6, -10, 0, 0), (11, 20, 0, 0))
a.r("hand_l", (6, 0, 0, 0), (9, -20, 0, 0))
a.r("head", (6, -4, 26, -6), (9, -4, 30, -8), (11, -10, -14, 6), (16, -6, -10, 10), (22, 0, 0, 14), (26, 0, 0, 0))
a.p("body", (6, 0, -0.4, 1.0), (9, 0, -0.5, 1.4), (11, 0, -0.6, -1.0), (15, 0, -0.4, -0.8), (22, 0, 0, 0))
legs(a, [(6, 14, 0, 4), (9, 18, 0, 4), (11, -24, 0, 4), (16, -20, 0, 4), (24, 0, 0, 0)],
     [(6, -20, 0, -4), (9, -22, 0, -4), (11, 24, 0, -4), (16, 18, 0, -4), (24, 0, 0, 0)],
     sr=[(9, -14, 0, 0), (11, 10, 0, 0)], sl=[(9, -10, 0, 0), (11, -26, 0, 0), (18, -10, 0, 0)])
a.sec([(0, 0, 0, 0), (9, -8, 0, -10), (11, 16, 0, 14), (16, 6, 0, 4), (22, 0, 0, 0)], delay=1)
a.done()

# ------------------------------------------------------------------ knife_fan (36): fans three spare knives out in the claw (3-8), right-hand throw t14,
#                                                                 cross-body wind 16-20, backhand FAN toss t22, new knife flicked out
a = A("knife_fan", 36)
a.show("fan", 3, 22)
a.hide("knife", 14, 26)
a.r("chest", (4, 4, 14, 0), (8, 6, -10, 0), (11, 10, -30, 0), (14, -10, 20, 0), (18, 6, 40, 0), (20, 8, 46, 0), (22, -8, -34, 0), (26, -4, -24, 0), (34, 0, 0, 0))
a.r("arm_l", (3, 20, 0, -20), (6, 70, 0, 10), (8, 76, 0, 14), (12, 60, 0, 10), (16, 70, 0, 50), (20, 80, 0, 64), (22, 86, 0, -70), (25, 80, 0, -76), (32, 10, 0, -10))
a.r("fore_l", (3, 40, 0, 0), (6, 30, 0, 0), (16, 50, 0, 0), (20, 60, 0, 0), (22, 0, 0, 0), (30, 20, 0, 0))
a.r("hand_l", (6, 0, 0, 0), (8, 0, 30, 0), (20, 0, 40, 0), (22, 0, -10, 0))
a.r("fan", (3, -80, 0, 0), (8, -70, 0, 0), (20, -100, 0, 0), (22, -90, 0, 0))
a.r("arm_r", (6, 40, 0, 10), (9, 150, 0, 16), (12, 164, 0, 20), (14, 60, 0, -14), (17, 30, 0, -10), (22, 20, 0, 20), (27, 30, 0, 10), (30, 40, 0, 12))
a.r("fore_r", (12, 50, 0, 0), (14, 0, 0, 0), (22, 30, 0, 0), (28, 50, 0, 0), (32, 30, 0, 0))
a.r("knife", (9, -60, 0, 0), (12, -70, 0, 0), (26, -40, 0, 180), (28, -40, 0, 360), (36, -40, 0, 360))
a.r("head", (4, -10, 10, 14), (8, -6, -6, 10), (12, -4, 20, 0), (14, -8, -10, 0), (19, 0, -30, -8), (22, -8, 16, 10), (28, 0, 4, 16), (34, 0, 0, 0))
a.p("body", (8, 0, -0.3, 0.2), (12, 0, -0.4, 0.8), (14, 0, -0.5, -0.8), (20, 0, -0.6, 0.6), (22, 0, -0.8, -1.2), (28, 0, -0.2, -0.4), (34, 0, 0, 0))
legs(a, [(8, 0, 0, 4), (12, 14, 0, 4), (14, -20, 0, 4), (20, 10, 0, 6), (22, -24, 0, 8), (30, 0, 0, 0)],
     [(8, 0, 0, -4), (12, -18, 0, -4), (14, 20, 0, -4), (20, -14, 0, -6), (22, 22, 0, -8), (30, 0, 0, 0)],
     sr=[(14, 8, 0, 0), (22, 10, 0, 0), (30, 0, 0, 0)], sl=[(14, -20, 0, 0), (22, -24, 0, 0), (30, 0, 0, 0)])
a.sec([(0, 0, 0, 0), (12, -6, 0, -8), (14, 12, 0, 10), (20, -6, 0, 14), (22, 16, 0, -18), (28, 4, 0, -4), (34, 0, 0, 0)], delay=1)
a.done()

# ------------------------------------------------------------------ feint_stab (30): big FAKE overhead swing to the right t6 (no hit), springy side-hop 8-13,
#                                                                 low upward GUT stab from the other side t17, giggle recover
a = A("feint_stab", 30)
a.r("root", (3, 0, 0, 6), (6, 0, 0, 10), (8, 0, 0, -6), (11, 0, 0, -18), (13, 0, 0, -10), (15, 0, 20, -4), (17, 0, 30, 0), (21, 0, 24, 0), (27, 0, 0, 0))
a.r("chest", (3, 10, -20, 0), (6, -10, -26, 0), (8, 0, 10, 0), (11, 4, 20, 0), (14, -6, 20, 0), (17, -24, -10, 0), (21, -18, -6, 0), (27, 0, 0, 0))
a.r("arm_r", (3, 150, 0, 30), (5, 158, 0, 34), (6, 100, 0, 40), (8, 60, 0, 24), (11, 10, 0, 30), (14, -20, 0, 10), (16, 50, 0, 0), (17, 100, 0, -6), (21, 92, 0, -4), (27, 20, 0, 4))
a.r("fore_r", (5, 10, 0, 0), (8, 40, 0, 0), (14, 80, 0, 0), (17, 0, 0, 0), (22, 10, 0, 0), (28, 20, 0, 0))
a.r("knife", (3, -70, 0, 0), (6, -80, 0, 0), (14, -60, 0, 0), (17, -110, 0, 0), (21, -104, 0, 0), (28, -40, 0, 0))
a.r("arm_l", (3, -10, 0, -30), (6, 20, 0, -40), (11, 0, 0, -80), (14, 20, 0, -40), (17, -30, 0, -30), (24, 0, 0, -10))
a.r("head", (3, 10, -16, 10), (6, 0, -20, 14), (11, 6, 20, -20), (17, -12, -10, 4), (21, -8, -6, 18), (25, 4, 0, 22), (30, 0, 0, 0))
a.p("root", (3, 0, 0, 0), (6, 0, -0.4, -0.6), (8, 0, 0.2, 0), (11, 0, 1.6, 0), (13, 0, 0, 0), (15, 0, -0.6, -1.0), (17, 0, -1.0, -2.2), (22, 0, -0.6, -1.6), (28, 0, 0, 0))
legs(a, [(6, -10, 0, 8), (8, 20, 0, 10), (11, 50, 0, 20), (13, 10, 0, 8), (15, -20, 0, 4), (17, -40, 0, 0), (22, -34, 0, 0), (28, 0, 0, 0)],
     [(6, 10, 0, -6), (8, 30, 0, -10), (11, 46, 0, -24), (13, 10, 0, -8), (15, 20, 0, 0), (17, 36, 0, 0), (22, 30, 0, 0), (28, 0, 0, 0)],
     sr=[(8, -40, 0, 0), (11, -80, 0, 0), (13, -20, 0, 0), (17, 10, 0, 0), (24, 0, 0, 0)], sl=[(8, -40, 0, 0), (11, -84, 0, 0), (13, -20, 0, 0), (17, -40, 0, 0), (24, 0, 0, 0)])
a.sec([(0, 0, 0, 0), (6, 8, 0, 14), (11, -12, 0, -20), (13, 10, 0, -10), (17, 18, 0, 8), (24, 4, 0, 0), (30, 0, 0, 0)], delay=1)
a.done()

# ------------------------------------------------------------------ tail_whip (28): crouch + coil, back turned 0-8, full SPIN t9-15 (tail lash hits t12), stagger out
a = A("tail_whip", 28)
a.r("root", (6, 0, -40, 0), (8, 0, -50, 0), (10, 0, 40, 0), (12, 0, 170, 0), (14, 0, 290, 0), (16, 0, 350, 0), (19, 0, 368, 0), (23, 0, 360, 0), (28, 0, 360, 0))
a.r("tail", (6, -50, -20, 0), (8, -56, -30, 0), (10, -36, 40, 0), (12, -40, 60, 0), (14, -30, 50, 0), (17, -10, -20, 0), (21, 0, 10, 0), (26, 0, 0, 0))
a.r("tail2", (6, 30, -20, 0), (8, 36, -30, 0), (10, 30, 40, 0), (12, 30, 40, 0), (15, 20, 30, 0), (18, 0, -30, 0), (22, 0, 10, 0), (26, 0, 0, 0))
a.r("tail3", (6, 30, -30, 0), (9, 30, -40, 0), (11, 34, 30, 0), (13, 34, 40, 0), (16, 20, 30, 0), (19, 0, -40, 0), (23, 0, 12, 0), (27, 0, 0, 0))
a.r("chest", (6, -20, 20, 0), (8, -24, 26, 0), (12, -10, -20, 0), (16, -6, -10, 0), (22, 0, 0, 0))
a.r("arm_r", (6, 20, 0, 40), (12, 30, 0, 80), (16, 20, 0, 50), (24, 20, 0, 6))
a.r("arm_l", (6, 20, 0, -40), (12, 30, 0, -80), (16, 20, 0, -50), (24, 0, 0, -6))
a.r("knife", (6, -40, 0, 0), (28, -40, 0, 0))
a.r("head", (6, 10, -30, 0), (8, 12, -40, 0), (12, -4, 20, 10), (17, 0, 10, -10), (24, 0, 0, 0))
a.p("body", (6, 0, -2.0, 0), (8, 0, -2.4, 0), (11, 0, -0.6, 0), (13, 0, -0.8, 0), (18, 0, -1.4, 0), (24, 0, 0, 0))
legs(a, [(6, 40, 0, 6), (8, 46, 0, 8), (12, 10, 0, 20), (16, 20, 0, 10), (24, 0, 0, 0)], [(6, 30, 0, -6), (8, 34, 0, -8), (12, -10, 0, -20), (16, 10, 0, -10), (24, 0, 0, 0)],
     sr=[(6, -70, 0, 0), (8, -80, 0, 0), (12, -20, 0, 0), (18, -40, 0, 0), (24, 0, 0, 0)])
a.sec([(0, 0, 0, 0), (8, -6, 20, 0), (12, 10, -30, -24), (16, 6, 0, -14), (22, 0, 0, 0)], delay=1)
a.done()

# ------------------------------------------------------------------ backstab (44): hand over the grin, giggling crouch 0-8, POOF vanish t10 (gone 10-15 while
#                                                               she teleports behind the target), pops back t16 crouched, raises knife 17-21, STAB t22
a = A("backstab", 44)
a.scl("root", (0, 1, 1, 1), (8, 1, 1, 1), (9, 1.12, 0.85, 1.12), (10, *HIDE), (15.5, *HIDE), (16, 0.6, 1.3, 0.6), (17, 1.1, 0.92, 1.1), (18.5, 1, 1, 1), (44, 1, 1, 1))
a.r("chest", (2, -6, 0, 4), (4, -12, 0, -4), (6, -8, 0, 4), (8, -16, 0, -2), (16, -30, 0, 0), (19, 4, 0, 0), (21, 8, 0, 0), (22, -28, 0, 0), (26, -26, 0, 0), (34, -10, 0, 0), (42, 0, 0, 0))
a.r("arm_l", (2, 100, 0, 30), (8, 100, 0, 34), (16, 30, 0, -40), (22, 40, 0, -30), (34, 10, 0, -10))
a.r("fore_l", (2, 60, 0, 0), (8, 60, 0, 0), (16, 10, 0, 0))
a.r("head", (2, 6, 0, 14), (4, -2, 0, -10), (6, 6, 0, 14), (8, -6, 0, -12), (16, 20, 0, 10), (21, 14, 0, 26), (22, -16, 0, 4), (28, -10, 0, 0), (36, 0, 0, 12), (44, 0, 0, 0))
a.r("arm_r", (2, 20, 0, 20), (8, 10, 0, 24), (16, 20, 0, 20), (18, 140, 0, 14), (21, 178, 0, 12), (22, 40, 0, 4), (26, 36, 0, 4), (32, 60, 0, 6), (40, 20, 0, 4))
a.r("fore_r", (8, 40, 0, 0), (18, 10, 0, 0), (22, 0, 0, 0), (32, 20, 0, 0), (40, 20, 0, 0))
a.r("knife", (8, -40, 0, 0), (18, -80, 0, 0), (21, -86, 0, 0), (22, -84, 0, 0), (25, -84, 0, 30), (28, -84, 0, 0), (36, -40, 0, 0), (44, -30, 0, 0))
a.p("body", (4, 0, -1.4, 0), (8, 0, -2.0, 0), (16, 0, -3.0, 0), (19, 0, -0.6, 0), (22, 0, -2.0, -1.2), (28, 0, -1.6, -1.0), (36, 0, -0.4, 0), (44, 0, 0, 0))
legs(a, [(8, 40, 0, 6), (16, 60, 0, 8), (19, 20, 0, 4), (22, 50, 0, 0), (30, 40, 0, 0), (40, 0, 0, 0)], [(8, 30, 0, -6), (16, 50, 0, -8), (19, 14, 0, -4), (22, -20, 0, 0), (30, -10, 0, 0), (40, 0, 0, 0)],
     sr=[(8, -70, 0, 0), (16, -100, 0, 0), (19, -30, 0, 0), (22, -70, 0, 0), (30, -60, 0, 0), (40, 0, 0, 0)],
     sl=[(8, -60, 0, 0), (16, -90, 0, 0), (19, -20, 0, 0), (22, -10, 0, 0), (40, 0, 0, 0)])
a.sec([(0, 0, 0, 0), (4, 4, 0, -10), (6, -4, 0, 10), (8, 4, 0, -8), (16, -10, 0, 0), (21, -8, 0, 10), (22, 22, 0, 0), (30, 6, 0, 0), (44, 0, 0, 0)], delay=1)
a.done()

# ------------------------------------------------------------------ pounce_stab (42): coil 0-9, LEAP t10 (knees tucked, knife high), lands astride the target t20 with a
#                                                                 downward stab, re-raise + stab t27, last big stab t34, hop off
a = A("pounce_stab", 42)
a.r("chest", (6, -24, 0, 0), (9, -30, 0, 0), (12, 14, 0, 0), (17, 18, 0, 0), (20, -36, 0, 0), (24, 6, 0, -6), (27, -34, 0, 4), (31, 10, 0, 6), (34, -40, 0, 0), (38, -20, 0, 0), (42, 0, 0, 0))
a.r("arm_r", (6, -30, 0, 16), (9, -40, 0, 20), (12, 160, 0, 14), (17, 176, 0, 12), (20, 40, 0, 4), (24, 170, 0, 10), (27, 40, 0, 2), (31, 176, 0, 6), (34, 30, 0, -6), (38, 50, 0, 4), (42, 20, 0, 4))
a.r("fore_r", (9, 60, 0, 0), (12, 10, 0, 0), (20, 0, 0, 0), (24, 20, 0, 0), (27, 0, 0, 0), (31, 20, 0, 0), (34, 0, 0, 0), (42, 20, 0, 0))
a.r("knife", (9, -40, 0, 0), (12, -80, 0, 0), (20, -84, 0, 0), (34, -84, 0, 0), (38, -70, 0, 0), (42, -30, 0, 0))
a.r("arm_l", (6, -30, 0, -16), (9, -40, 0, -20), (12, 30, 0, -70), (17, 40, 0, -80), (20, 60, 0, -20), (24, 50, 0, -40), (27, 60, 0, -20), (31, 150, 0, -6), (34, 40, 0, 6), (40, 0, 0, -10))
a.r("fore_l", (17, 20, 0, 0), (20, 40, 0, 0), (31, 10, 0, 0), (34, 10, 0, 0))
a.r("head", (6, 16, 0, 0), (9, 20, 0, 0), (12, 6, 0, 14), (17, 4, 0, 20), (20, -24, 0, 0), (24, 6, 0, 18), (27, -24, 0, -6), (31, 10, 0, -16), (34, -30, 0, 0), (40, 0, 0, 12))
a.p("body", (6, 0, -2.6, 0.6), (9, 0, -3.0, 0.8), (11, 0, 0.8, -0.4), (15, 0, 1.6, -0.6), (19, 0, -1.0, -0.6), (20, 0, -3.4, -1.0), (24, 0, -2.6, -1.0), (27, 0, -3.4, -1.0), (31, 0, -2.4, -1.0),
    (34, 0, -3.8, -1.2), (38, 0, -1.6, -0.6), (42, 0, 0, 0))
legs(a, [(6, 46, 0, 6), (9, 50, 0, 8), (12, 70, 0, 10), (17, 80, 0, 12), (20, 80, 0, 18), (34, 80, 0, 18), (38, 40, 0, 6), (42, 0, 0, 0)],
     [(6, 36, 0, -6), (9, 40, 0, -8), (12, 60, 0, -10), (17, 70, 0, -12), (20, 70, 0, -18), (34, 70, 0, -18), (38, 30, 0, -6), (42, 0, 0, 0)],
     sr=[(6, -80, 0, 0), (9, -90, 0, 0), (12, -110, 0, 0), (17, -120, 0, 0), (20, -110, 0, 0), (34, -110, 0, 0), (38, -50, 0, 0), (42, 0, 0, 0)])
a.sec([(0, 0, 0, 0), (9, -10, 0, 0), (12, 20, 0, 0), (17, -14, 0, 0), (20, 22, 0, 0), (24, -8, 0, 6), (27, 18, 0, -4), (31, -8, 0, 4), (34, 24, 0, 0), (40, 4, 0, 0), (42, 0, 0, 0)], delay=1)
a.done()

# ------------------------------------------------------------------ blade_spin (34): arms flung out 0-6, spinning top 6-26 (hits t10/16/22), dizzy wobble 26-34
a = A("blade_spin", 34)
a.r("root", (4, 0, -30, 0), (6, 0, -36, 0), (10, 0, 150, 0), (13, 0, 300, 0), (16, 0, 510, 0), (19, 0, 690, 0), (22, 0, 870, 0), (26, 0, 1060, 0), (30, 0, 1084, 0), (34, 0, 1080, 0))
a.r("arm_r", (4, 10, 0, 70), (6, 10, 0, 86), (26, 10, 0, 86), (30, 30, 0, 40), (34, 0, 0, 0))
a.r("arm_l", (4, 10, 0, -70), (6, 10, 0, -86), (26, 10, 0, -86), (30, 20, 0, -40), (34, 0, 0, 0))
a.r("fore_r", (6, 0, 0, 0), (26, 0, 0, 0), (30, 20, 0, 0))
a.r("knife", (4, 0, 0, 0), (26, 0, 0, 0), (32, -40, 0, 0))
a.r("hand_l", (6, 0, 0, -20), (26, 0, 0, -20))
a.r("chest", (4, 10, 20, 0), (6, 6, 24, 0), (10, 4, -10, 0), (26, 4, -10, 0), (29, -6, 0, 8), (31, 0, 0, -8), (34, 0, 0, 0))
a.r("head", (4, 12, 0, 0), (10, 16, 0, 10), (26, 16, 0, 10), (28, 0, 20, 20), (30, 4, -16, -20), (32, 2, 10, 14), (34, 0, 0, 0))
a.r("hem", (8, -20, 0, 0), (26, -20, 0, 0), (30, 4, 0, 0))
a.r("tail", (8, -60, 0, 0), (26, -60, 0, 0), (30, 10, 30, 0))
a.r("tail2", (8, 26, 0, 0), (26, 26, 0, 0), (30, 0, -30, 0))
a.r("tail3", (8, 30, 0, 0), (26, 30, 0, 0), (31, 0, 30, 0))
a.r("pony", (8, 20, 0, 30), (26, 20, 0, 30), (30, -10, 0, -10))
a.r("pony2", (8, 20, 0, 20), (26, 20, 0, 20), (31, -10, 0, -10))
a.p("body", (4, 0, -1.0, 0), (6, 0, -0.6, 0), (10, 0, 0.4, 0), (16, 0, 0.2, 0), (22, 0, 0.4, 0), (26, 0, 0, 0), (29, 0, -0.8, 0), (34, 0, 0, 0))
legs(a, [(4, 10, 0, 6), (6, 0, 0, 8), (26, 0, 0, 8), (29, 20, 0, 12), (31, -10, 0, 0), (34, 0, 0, 0)], [(4, 10, 0, -6), (6, 0, 0, -8), (26, 0, 0, -8), (29, -16, 0, -4), (31, 14, 0, -10), (34, 0, 0, 0)],
     sr=[(4, -20, 0, 0), (6, 0, 0, 0), (29, -20, 0, 0), (34, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ frenzy (46, enraged): six manic stabs t8/12/16/20/24/28 alternating high/low, head jerking,
#                                                              final wide horizontal SLASH t34, panting grin
a = A("frenzy", 46)
STABS = (8, 12, 16, 20, 24, 28)
ar, fr, kn, ch, hd, bd = [], [], [], [], [], []
for i, t in enumerate(STABS):
    hi = i % 2 == 0
    ar += [(t - 2, 20 if hi else 0, 0, 24), (t, 120 if hi else 76, 0, 4 if hi else -4)]
    fr += [(t - 2, 90, 0, 0), (t, 0, 0, 0)]
    kn += [(t - 2, -90, 0, 0), (t, -126 if hi else -84, 0, 0)]
    ch += [(t - 2, 2, -20, 0), (t, -18, 12 if hi else 6, 4 if hi else -4)]
    hd += [(t - 2, 6, 10, 20 if hi else -20), (t, -10, -6, -10 if hi else 10)]
    bd += [(t - 2, 0, -0.6, -0.3 * i), (t, 0, -1.0, -0.3 * i - 0.8)]
a.r("arm_r", (3, 10, 0, 20), *ar, (31, 30, 0, 60), (32, 60, 0, 70), (34, 86, 0, -40), (38, 80, 0, -46), (44, 20, 0, 4))
a.r("fore_r", (3, 60, 0, 0), *fr, (32, 20, 0, 0), (34, 0, 0, 0), (40, 20, 0, 0))
a.r("knife", (3, -70, 0, 0), *kn, (32, -80, 0, 0), (34, -84, 0, 0), (42, -40, 0, 0))
a.r("chest", (3, 6, 0, 0), *ch, (32, 6, -40, 0), (34, -10, 34, 0), (38, -6, 30, 0), (44, 4, 0, 0))
a.r("head", (3, 10, 0, 20), *hd, (32, 4, 20, 10), (34, -6, -14, -6), (38, 16, 0, 14), (41, 10, 0, -10), (44, 6, 0, 0))
a.p("body", (3, 0, -0.4, 0), *bd, (32, 0, -0.6, -2.4), (34, 0, -1.0, -3.0), (40, 0, -0.2, -1.4), (46, 0, 0, 0))
a.r("arm_l", (3, 30, 0, -50), (16, 40, 0, -60), (28, 30, 0, -70), (34, -40, 0, -40), (44, 0, 0, -10))
a.r("hand_l", *[(t, 20 if (t // 4) % 2 else -20, 0, 0) for t in range(4, 33, 4)])
legs(a, [(3, -10, 0, 4), *[(t, -30 if i % 2 else -20, 0, 4) for i, t in enumerate(STABS)], (34, -36, 0, 0), (40, -20, 0, 0), (46, 0, 0, 0)],
     [(3, 10, 0, -4), *[(t, 20 if i % 2 else 30, 0, -4) for i, t in enumerate(STABS)], (34, 34, 0, 0), (40, 20, 0, 0), (46, 0, 0, 0)],
     sr=[(8, 16, 0, 0), (34, 20, 0, 0), (42, 0, 0, 0)], sl=[(8, -30, 0, 0), (34, -36, 0, 0), (42, 0, 0, 0)])
a.sec([(0, 0, 0, 0)] + [(t, 14, 0, 10 if i % 2 else -10) for i, t in enumerate(STABS)] + [(32, -8, 0, -16), (34, 18, 0, 20), (40, 4, 0, 0), (46, 0, 0, 0)], delay=1)
a.done()

# ------------------------------------------------------------------ carve (60, enraged signature): lunging claw GRAB t10, holds the victim up, three carving cuts
#                                                              t20 (diag down), t28 (back-diag), t36 (deep stab + twist), wild kick-off t48
a = A("carve", 60)
a.r("arm_l", (6, -20, 0, -30), (8, 60, 0, -10), (10, 96, 0, 6), (14, 104, 0, 8), (20, 110, 0, 4), (28, 104, 0, 10), (36, 110, 0, 6), (46, 100, 0, 6), (48, 60, 0, -30), (52, 20, 0, -40), (58, 0, 0, -10))
a.r("fore_l", (8, 0, 0, 0), (10, -10, 0, 0), (14, 10, 0, 0), (46, 10, 0, 0), (50, 20, 0, 0))
a.r("hand_l", (8, -30, 0, 0), (10, 20, 0, 0), (14, 30, 0, 0), (46, 30, 0, 0), (48, -30, 0, 0), (54, 0, 0, 0))
a.r("arm_r", (6, 20, 0, 20), (14, 30, 0, 30), (17, 160, 0, 40), (18, 166, 0, 44), (20, 70, 0, -30), (23, 60, 0, -36), (25, 150, 0, -40), (26, 156, 0, -44), (28, 70, 0, 30),
    (31, 30, 0, 20), (33, -10, 0, 16), (34, -20, 0, 14), (36, 96, 0, 0), (38, 94, 0, 0), (42, 90, 0, 0), (48, 40, 0, 20), (56, 20, 0, 6))
a.r("fore_r", (14, 40, 0, 0), (18, 10, 0, 0), (20, 0, 0, 0), (26, 10, 0, 0), (28, 0, 0, 0), (34, 90, 0, 0), (36, 0, 0, 0), (48, 20, 0, 0))
a.r("knife", (14, -60, 0, 0), (18, -100, 0, 0), (20, -84, 0, 0), (26, -100, 0, 0), (28, -84, 0, 0), (34, -100, 0, 0), (36, -96, 0, 0), (38, -96, 0, 40), (40, -96, 0, -40), (42, -96, 0, 30),
    (48, -60, 0, 0), (56, -30, 0, 0))
a.r("chest", (6, 6, 0, 0), (10, -20, -20, 0), (14, -4, -10, 0), (18, 10, 20, -6), (20, -14, -20, 6), (26, 10, -24, 6), (28, -14, 20, -6), (34, 6, 10, 0), (36, -20, -4, 0), (42, -14, 0, 0),
    (46, 6, 0, 0), (48, 20, 0, 0), (54, 4, 0, 0))
a.r("head", (6, 10, 0, 0), (10, -10, 10, -10), (14, 6, 0, 24), (18, 10, -10, 28), (20, -10, 10, 0), (26, 10, 10, -26), (28, -10, -10, 0), (34, 10, 0, 22), (36, -20, 0, 0),
    (42, 14, 0, 30), (46, 20, 0, -20), (50, 6, 0, 10), (58, 0, 0, 0))
a.p("body", (6, 0, -1.0, 0.6), (10, 0, -0.6, -2.0), (14, 0, 0, -1.0), (36, 0, -0.6, -1.6), (46, 0, 0, -0.6), (48, 0, 0.3, 0.6), (54, 0, 0, 0))
legs(a, [(6, 20, 0, 4), (10, -30, 0, 4), (14, -10, 0, 6), (36, -24, 0, 6), (44, -10, 0, 4), (46, 20, 0, 6), (48, 96, 0, 4), (50, 90, 0, 4), (54, 20, 0, 0), (58, 0, 0, 0)],
     [(6, -20, 0, -4), (10, 30, 0, -4), (14, 12, 0, -6), (36, 24, 0, -6), (46, -10, 0, -4), (48, -16, 0, -4), (54, 0, 0, 0)],
     sr=[(10, 20, 0, 0), (46, -80, 0, 0), (48, 0, 0, 0), (52, -30, 0, 0), (56, 0, 0, 0)], sl=[(10, -20, 0, 0), (48, -14, 0, 0), (56, 0, 0, 0)])
a.sec([(0, 0, 0, 0), (10, 14, 0, -6), (18, -8, 0, 14), (20, 14, 0, -12), (26, -8, 0, -14), (28, 14, 0, 12), (34, -6, 0, 6), (36, 18, 0, 0), (40, 8, 0, 10), (48, -14, 0, 0),
       (54, 4, 0, 0), (60, 0, 0, 0)], delay=1)
a.done()

# ------------------------------------------------------------------ giggle (36): crazed laughing fit - doubles over 0-6, head snaps back cackling t10-26 (fear pulse t14),
#                                                               shoulders shaking, knife twirled, settles with the grin cocked
a = A("giggle", 36)
SHK = [(t, 1 if (t // 2) % 2 else -1) for t in range(8, 29, 2)]
a.r("chest", (3, -22, 0, 0), (6, -26, 0, 0), (10, 16, 0, 0), *[(t, 14 + 4 * s, 0, 5 * s) for t, s in SHK[1:]], (30, 4, 0, 0), (36, 0, 0, 0))
a.r("head", (3, -20, 0, 10), (6, -24, 0, 14), (10, 34, 0, -6), (14, 40, 0, 8), *[(t, 36 + 4 * s, 4 * s, 10 * s) for t, s in SHK[4:]], (30, 4, 0, 24), (36, 0, 0, 0))
a.r("arm_l", (3, 40, 0, 20), (6, 70, 0, 30), (10, 40, 0, -110), (26, 40, 0, -120), (30, 20, 0, -30), (36, 0, 0, 0))
a.r("fore_l", (6, 40, 0, 0), (10, -20, 0, 0), (26, -20, 0, 0))
a.r("hand_l", *[(t, 0, 0, 25 * s) for t, s in SHK])
a.r("arm_r", (3, 20, 0, 20), (6, 30, 0, 20), (10, 120, 0, 60), (26, 130, 0, 66), (30, 40, 0, 20), (36, 0, 0, 0))
a.r("fore_r", (10, 30, 0, 0), (26, 30, 0, 0))
a.r("knife", (8, -40, 0, 0), (12, -40, 0, 360), (16, -40, 0, 720), (20, -40, 0, 1080), (24, -40, 0, 1440), (36, -40, 0, 1440))
a.p("body", (3, 0, -0.8, 0), (6, 0, -1.2, 0), (10, 0, 0.6, 0.6), *[(t, 0, 0.3 + 0.3 * s, 0.6) for t, s in SHK[1:]], (30, 0, 0, 0), (36, 0, 0, 0))
legs(a, [(3, 20, 0, 4), (6, 26, 0, 4), (10, -6, 0, 10), (26, -6, 0, 10), (32, 0, 0, 4)], sr=[(6, -40, 0, 0), (10, 0, 0, 0)])
a.sec([(0, 0, 0, 0), (6, -10, 0, 0), (10, 18, 0, 0)] + [(t, 12, 0, 10 * s) for t, s in SHK[1:]] + [(30, 2, 0, 0), (36, 0, 0, 0)], delay=1)
a.done()

# ------------------------------------------------------------------ death (40): jolt, knife slips from the fingers t8, knees buckle 10-18,
#                                                               topples backward 18-30 (still grinning), tail and ponytail flop
a = A("death", 40)
a.r("root", (6, 0, 0, 0), (18, -10, 0, 6), (24, 50, 0, 10), (28, 86, 0, 8), (30, 80, 0, 8), (32, 84, 0, 8), (40, 84, 0, 8))
a.p("root", (6, 0, 0, 0), (18, 0, -2.0, 0), (24, 0, -1.4, 0.8), (28, 0, -0.4, 1.4), (40, 0, -0.4, 1.4))
a.r("chest", (2, 16, 0, 0), (4, 20, 0, -6), (10, -20, 0, 10), (18, -30, 0, 6), (26, 10, 0, 0), (40, 10, 0, 0))
a.r("head", (2, 20, 0, 0), (4, 26, 0, -10), (10, -20, 0, 30), (18, -30, 0, 20), (26, 10, 30, 10), (30, 6, 34, 10), (40, 6, 34, 10))
a.r("arm_r", (2, 30, 0, 40), (6, 20, 0, 30), (10, 0, 0, 10), (24, -20, 0, 70), (28, -10, 0, 90), (40, -10, 0, 90))
a.r("arm_l", (2, 30, 0, -40), (10, 0, 0, -10), (24, -20, 0, -60), (28, -10, 0, -84), (40, -10, 0, -84))
a.r("knife", (2, -40, 0, 0), (7, -40, 0, 0), (12, 60, 0, 90), (16, 120, 0, 180), (40, 120, 0, 180))
a.p("knife", (7, 0, 0, 0), (12, 0, -4, -1), (16, 0, -8.6, -2), (40, 0, -8.6, -2))
legs(a, [(4, -6, 0, 6), (10, 20, 0, 10), (18, 40, 0, 16), (26, 34, 0, 12), (30, 14, 0, 12), (40, 10, 0, 12)], [(4, 6, 0, -6), (10, 30, 0, -8), (18, 50, 0, -14), (26, 20, 0, -12), (30, 0, 0, -10), (40, -4, 0, -10)],
     sr=[(10, -40, 0, 0), (18, -90, 0, 0), (26, -40, 0, 0), (30, -14, 0, 0), (40, -10, 0, 0)])
a.r("tail", (18, -20, 20, 0), (28, 40, -10, 0), (40, 40, -10, 0))
a.r("tail2", (20, -10, 20, 0), (30, 30, 0, 0), (40, 30, 0, 0))
a.r("tail3", (22, -10, 20, 0), (32, 30, 0, 0), (40, 30, 0, 0))
a.r("pony", (18, 10, 0, 10), (28, -50, 0, 10), (31, -36, 0, 6), (40, -40, 0, 6))
a.r("pony2", (20, 10, 0, 0), (30, -30, 0, 0), (40, -26, 0, 0))
a.r("hem", (24, -20, 0, 0), (40, -16, 0, 0))
a.done()

m.save(OUT)
print("cubes", len(m.cubes))
