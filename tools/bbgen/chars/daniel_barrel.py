"""Daniel F. Barrel (FPE Advanced Class) - both forms in one generator.
  variant 0 MATURED      -> assets/fpe/bbmodels/daniel_barrel.bbmodel        (docs/ref/confirmed/daniel_barrel_matured.png)
  variant 1 CYBORG ARMED -> assets/fpe/bbmodels/daniel_barrel_cyborg.bbmodel (docs/ref/confirmed/daniel_barrel_cyborg.png)
Hitbox 0.8 x 2.5 (= 40 px): tall, thin, very long legs.
Matured: white spiky hair, black bat-horn ears, tilted white box cap with a black visor + red/black emblem lens, fanged grin,
white shirt + black tie, black suit jacket with spiked shoulders, small black bat wings, long grey-green cape-like hair strands,
long black whip tail, LEFT forearm replaced by a rifle (red ribbed magazine, warning-triangle sign on the barrel).
Cyborg: grey-blue armoured bodysuit with glowing red-pink chest plates, big round red-rimmed goggles, white hair with long white
locks, black horn ears, big black bat wings, black tail, huge black LEFT tech-arm cannon (glowing red magazine strip + warning sign).
Rotation signs (lh_common): hanging limb rx>0 = swing forward, upright part rx>0 = lean back, ry>0 = turn to the character's
left, hanging limb rz>0 = swing toward +X (character's right). Animation ticks == entity/characters/DanielBarrel.java ticks.
Run: python3 tools/bbgen/chars/daniel_barrel.py
"""
import math, os
from lh_common import Model, Kit, A, ROOT, mix, sinekeys, CLEAR, HIDE
import bbgen

_px = bbgen.Face.px
bbgen.Face.px = lambda self, x, y, c, a=255, glow=False: _px(self, int(x), int(y), c, a, glow)   # allow float texel coords

# ------------------------------------------------------------------ palettes
SKIN, SKIN_D, SKIN_L = 0xECE6E4, 0xBFB6B8, 0xFAF7F5
HAIR, HAIR_L, HAIR_D = 0xEDEEEA, 0xFFFFFF, 0xB4B9BC
CAPE, CAPE_L, CAPE_D = 0x9AA79F, 0xBCC7BF, 0x5F6C66
JK, JK_L, JK_D = 0x26222C, 0x433D4A, 0x121016
SHIRT, SHIRT_D = 0xF2F1EE, 0xC9C8CC
TIE = 0x111014
GUN, GUN_L, GUN_D = 0x3A3A44, 0x5C5C68, 0x1C1C22
MAG, MAG_L, MAG_D = 0xD8423C, 0xF07068, 0x7A1A18
RED, RED_G = 0xD0202A, 0xFF3A40
WING, WING_L, WING_D = 0x1A171E, 0x3A3540, 0x0A090C
CAP, CAP_D = 0xF0F0EE, 0xB8B8BC
SUIT, SUIT_L, SUIT_D, SUIT_DD = 0x6C7288, 0x969DB2, 0x4A4F62, 0x2C2F3C
PINK, PINK_G, PINK_D = 0xE8566A, 0xFF7486, 0x8C2434
TECH, TECH_L, TECH_D = 0x1A181E, 0x3E3A46, 0x0A090C
YEL = 0xFFE27A


def build(form):
    cy = form == "cyborg"
    m = Model("daniel_barrel_cyborg" if cy else "daniel_barrel", S=8, atlas=2048)
    K = Kit(m)
    R = m.rng
    af, flat, clear = K.all_faces, K.flat, K.clear

    # -------------------------------------------------------------- painters
    def noise(base, dark, amt=0.25):
        def f(F):
            for y in range(F.h):
                for x in range(F.w):
                    F.px(x, y, mix(base, dark, amt * R.random() + 0.25 * y / max(1, F.h)))
        return f

    def cloth(base, light, dark):
        """suit cloth: vertical gradient + soft fold lines"""
        def f(F):
            for y in range(F.h):
                for x in range(F.w):
                    F.px(x, y, mix(light, base, min(1, 0.4 + 0.6 * y / max(1, F.h))))
            for _ in range(max(1, F.w // 6)):
                x = R.uniform(1, F.w - 2)
                F.line(x, R.uniform(0, F.h * 0.3), x + R.uniform(-2, 2), F.h * R.uniform(0.6, 1), dark, 1)
        return f

    def metal(base, light, dark, panels=True):
        def f(F):
            for y in range(F.h):
                for x in range(F.w):
                    F.px(x, y, mix(light, dark, 0.15 + 0.6 * y / max(1, F.h)))
            if panels:
                for y in range(3, F.h - 1, 9):
                    F.rect(0, y, F.w, 1, dark)
                    F.rect(0, y + 1, F.w, 1, light)
            K.outline(dark)(F)
        return f

    def maga(F):
        """red ribbed magazine"""
        for y in range(F.h):
            for x in range(F.w):
                F.px(x, y, MAG_D if y % 5 == 0 else mix(MAG_L, MAG, 0.3 + 0.5 * x / max(1, F.w)), glow=cy and y % 5 != 0)
        K.outline(MAG_D)(F)

    def strip(F):
        """cyborg magazine strip: graded red-pink bars, glowing"""
        for y in range(F.h):
            for x in range(F.w):
                if y % 6 < 4 and 1 <= x < F.w - 1:
                    F.px(x, y, mix(0xFFB0B8, PINK_D, y / max(1, F.h)), glow=True)
                else:
                    F.px(x, y, TECH_D)

    def warn(F):
        """warning triangle: white triangle, red border, black '!' (transparent around)"""
        W, H = F.w, F.h
        for y in range(H):
            for x in range(W):
                v = (y + .5) / H
                d = abs((x + .5) / W - 0.5)
                if d > 0.5 * v: F.px(x, y, CLEAR)
                elif d > 0.5 * v - 0.13 or v > 0.86: F.px(x, y, RED)
                else: F.px(x, y, 0xFAFAF4)
        F.rect(W / 2 - 1, H * 0.35, 2, H * 0.3, 0x111111)
        F.rect(W / 2 - 1, H * 0.7, 2, 2, 0x111111)

    def warn_circle(F):
        W, H = F.w, F.h
        F.rect(0, 0, W, H, TECH)
        F.disc(W / 2, H / 2, min(W, H) / 2 - 0.5, RED_G, glow=True)
        F.disc(W / 2, H / 2, min(W, H) / 2 - 2.5, 0xFFF4F0, glow=True)
        F.rect(W / 2 - 1, H * 0.25, 2, H * 0.32, 0xC01020)
        F.rect(W / 2 - 1, H * 0.64, 2, 2, 0xC01020)

    def hairp(base, light, dark):
        return K.strands(base, light, dark, None, 2)

    def bat(root_left, col=WING, rib=WING_L, edge=WING_D):
        pts = [(0, .30), (.42, .02), (1, 0), (.93, .52), (.78, .38), (.66, .86), (.50, .58), (.33, 1.0), (.18, .66), (0, .62)]
        def f(F):
            F.rect(0, 0, F.w, F.h, CLEAR)
            P = [((x if root_left else 1 - x) * F.w, y * F.h) for (x, y) in pts]
            F.poly(P, col)
            for (x, y) in ((.78, .38), (.50, .58), (.18, .66)):     # finger ribs from the root
                F.line(P[0][0], P[0][1] + 2, (x if root_left else 1 - x) * F.w, y * F.h, rib, 1)
            F.line(P[0][0], P[0][1], P[2][0], P[2][1], rib, 1.6)
        return f

    def face(F):
        W, H = F.w, F.h
        for y in range(H):
            for x in range(W):
                F.px(x, y, mix(SKIN_L, SKIN_D, 0.1 + 0.45 * y / H))
        # white spiky fringe
        for x in range(W):
            top = 9 + int(5 * abs(math.sin(x * 0.42))) + (4 if x % 9 == 4 else 0)
            for y in range(top):
                F.px(x, y, mix(HAIR_L, HAIR_D, y / 16))
            F.px(x, top, HAIR_D)
        if cy:
            F.disc(W / 2, 37, 3, 0xE6B8B8)                               # small smile
            F.line(W / 2 - 6, 35, W / 2, 38, 0x6A2A30, 1)
            F.line(W / 2, 38, W / 2 + 6, 35, 0x6A2A30, 1)
            for s in (-1, 1):
                F.px(W / 2 + s * 12, 33, 0xF0C0C8)
        else:
            for s in (-1, 1):                                            # sharp eyes: black almond, glowing red iris
                ex = W / 2 + s * 10
                for x in range(-6, 7):
                    yy = 20 + int(s * x * 0.3)
                    F.rect(ex + x, yy, 1, 4 if abs(x) < 4 else 2, 0x141016)
                F.rect(ex - 1, 21, 3, 2, RED_G, glow=True)
                F.px(ex + 1, 21, 0xFFFFFF)
                F.line(ex - 7, 16 + s * 2, ex + 7, 16 - s * 2, 0x55505A, 1)  # angry brows
            # wide fanged grin
            for x in range(9, W - 9):
                u = (x - 9) / (W - 18)
                top = 31 - 2 * math.sin(math.pi * u)
                bot = 33 + 7 * math.sin(math.pi * u)
                for y in range(int(top), int(bot) + 1):
                    F.px(x, y, mix(0x5A0E1C, 0x2A0610, (y - top) / max(1, bot - top)))
                if x % 3 == 0: F.px(x, int(top), 0xFFFFFF)
            F.rect(W / 2 - 3, 36, 6, 3, 0xC03A4A)                         # tongue
            for s in (-1, 1):
                fx = W / 2 + s * 7
                F.poly([(fx - 2, 30), (fx + 2, 30), (fx, 36)], 0xFFFFFF)      # fangs
                F.line(W / 2 + s * 15, 28, W / 2 + s * 13, 32, 0x5A0E1C, 1)

    def face_side(F):
        for y in range(F.h):
            for x in range(F.w):
                F.px(x, y, mix(SKIN, SKIN_D, 0.3 + 0.4 * y / F.h))
        for y in range(int(F.h * 0.75)):                       # hair covers upper / back part
            for x in range(F.w):
                if y < F.h * 0.25 or x > F.w * 0.55 - 0.15 * y:
                    F.px(x, y, mix(HAIR_L, HAIR_D, y / F.h))

    def shirt_front(wide, tie_top, tie_bot):
        """black jacket sides, white shirt middle with a black tie (texel x0 = character's right)"""
        def f(F):
            W, H = F.w, F.h
            cl = cloth(JK, JK_L, JK_D)
            cl(F)
            sw = W * (0.24 if wide else 0.3)
            for y in range(H):
                ww = sw * (1 - 0.35 * y / H) if wide else sw
                for x in range(int(W / 2 - ww), int(W / 2 + ww)):
                    F.px(x, y, mix(SHIRT, SHIRT_D, 0.15 + 0.3 * abs(x - W / 2) / max(1, ww)))
                F.px(int(W / 2 - ww) - 1, y, JK_L)
                F.px(int(W / 2 + ww), y, JK_L)
            # tie
            for y in range(int(tie_top * H), int(tie_bot * H)):
                tw = 3 if y > tie_top * H + 5 else 2
                F.rect(W / 2 - tw, y, tw * 2, 1, TIE)
            if tie_bot >= 0.99:
                pass
            else:
                yb = int(tie_bot * H)
                F.poly([(W / 2 - 3, yb), (W / 2 + 3, yb), (W / 2, yb + 4)], TIE)
            for y in range(4, H - 2, 9):                           # shirt buttons
                F.px(W / 2 + 4, y, SHIRT_D)
        return f

    def plate(F):
        """glowing pink chest plate with a hot rim"""
        for y in range(F.h):
            for x in range(F.w):
                F.px(x, y, mix(PINK, PINK_D, 0.2 + 0.5 * y / F.h), glow=False)
        K.outline(PINK_G)(F)
        for x in range(F.w):
            F.px(x, 0, 0xFFC0C8, glow=True); F.px(x, F.h - 1, PINK_G, glow=True)
        for y in range(F.h):
            F.px(0, y, PINK_G, glow=True); F.px(F.w - 1, y, PINK_G, glow=True)

    def suit_front(F):
        W, H = F.w, F.h
        for y in range(H):
            for x in range(W):
                F.px(x, y, mix(SUIT_L, SUIT, 0.3 + 0.6 * y / H))
        F.line(W / 2, 0, W / 2, H, SUIT_DD, 1)
        for y in range(6, H, 8):
            F.line(W * 0.25, y, W * 0.75, y, SUIT_D, 1)
        for s in (-1, 1):
            F.line(W / 2 + s * W * 0.42, 0, W / 2 + s * W * 0.3, H, SUIT_D, 1)

    def suit_side(F):
        for y in range(F.h):
            for x in range(F.w):
                F.px(x, y, mix(SUIT, SUIT_D, 0.3 + 0.5 * y / F.h))
        F.line(F.w / 2, 0, F.w / 2, F.h, SUIT_DD, 1)

    def goggle(F):
        W, H = F.w, F.h
        F.rect(0, 0, W, H, CLEAR)
        F.disc(W / 2, H / 2, W / 2 - 0.2, RED_G, glow=True)
        F.disc(W / 2, H / 2, W / 2 - 2.6, 0x0E0C10)
        F.disc(W / 2, H / 2, 2.4, RED_G, glow=True)
        F.disc(W / 2 - 3, H / 2 - 3, 1.2, 0xFFFFFF, glow=True)

    clothp = cloth(JK, JK_L, JK_D)
    gunp = metal(GUN, GUN_L, GUN_D)
    techp = metal(TECH, TECH_L, TECH_D)
    suitp = af(suit_side) | {"north": suit_front}
    hairw = hairp(HAIR, HAIR_L, HAIR_D)
    _cp = hairp(CAPE, CAPE_L, CAPE_D) if not cy else hairp(0xE4E6E8, 0xFFFFFF, 0xA6ACB4)
    _edge = CAPE_D if not cy else 0x8A909A
    def capep(F):
        _cp(F)
        for y in range(F.h):
            F.px(0, y, _edge); F.px(F.w - 1, y, _edge)

    # -------------------------------------------------------------- skeleton (identical names/pivots in both forms)
    m.group("root", (0, 0, 0))
    m.group("body", (0, 20, 0), parent="root")
    m.group("chest", (0, 21, 0), parent="body")
    m.group("head", (0, 32.6, -0.2), parent="chest")
    m.group("jaw", (0, 33.8, -1.6), parent="head")
    m.group("ear_r", (2.6, 38.0, 0.9), parent="head")
    m.group("ear_l", (-2.6, 38.0, 0.9), parent="head")
    m.group("hair_c", (0, 36.6, 2.6), parent="head")
    m.group("hair_r", (2.2, 36.4, 2.0), rot=(8, 0, 6), parent="head")
    m.group("hair_r2", (4.0, 22.6, 3.4), parent="hair_r")
    m.group("hair_l", (-2.2, 36.4, 2.0), rot=(8, 0, -6), parent="head")
    m.group("hair_l2", (-4.0, 22.6, 3.4), parent="hair_l")
    m.group("wing_r", (1.2, 29.6, 1.9), rot=(0, -24, 16), parent="chest")
    m.group("wing_l", (-1.2, 29.6, 1.9), rot=(0, 24, -16), parent="chest")
    m.group("arm_r", (4.1, 30.6, 0), rot=(0, 0, 5), parent="chest")
    m.group("fore_r", (4.1, 24.8, 0), parent="arm_r")
    m.group("hand_r", (4.1, 19.6, 0), parent="fore_r")
    m.group("arm_l", (-4.1, 30.6, 0), rot=(0, 0, -4), parent="chest")
    m.group("fore_l", (-4.1, 24.8, 0), parent="arm_l")
    m.group("gun", (-4.1, 21.0, 0), parent="fore_l")
    m.group("flash", (-4.1, 9.6 if cy else 3.4, 0), parent="gun")
    TAIL = ["tail", "tail1", "tail2", "tail3", "tail4", "tail5"]
    trot = [(58, 28, 0), (22, 0, 0), (-12, -6, 0), (-26, -6, 0), (-30, 0, 0), (-28, 0, 0)]
    for i, b in enumerate(TAIL):
        m.group(b, (0, 19.4, 1.4 + 4.4 * i), rot=trot[i], parent="body" if i == 0 else TAIL[i - 1])
    for s, k in ((1, "r"), (-1, "l")):
        m.group("leg_" + k, (1.45 * s, 19.6, 0), parent="body")
        m.group("shin_" + k, (1.45 * s, 10.2, 0), parent="leg_" + k)

    # -------------------------------------------------------------- legs
    for s, k in ((1, "r"), (-1, "l")):
        x = 1.45 * s
        L, Sh = "leg_" + k, "shin_" + k
        if not cy:
            m.cube("thigh_" + k, L, (x - 1.1, 10.0, -1.15), (x + 1.1, 20.2, 1.15), JK, faces=af(clothp))
            m.cube("shinc_" + k, Sh, (x - 1.0, 1.6, -1.05), (x + 1.0, 10.4, 1.05), JK, faces=af(clothp))
            m.cube("crease_" + k, L, (x - 0.15, 10.4, -1.25), (x + 0.15, 19.6, -1.1), JK_L, faces=af(flat(JK_L)))
            m.cube("cuff_" + k, Sh, (x - 1.15, 1.3, -1.2), (x + 1.15, 2.4, 1.2), JK_D, faces=af(flat(JK_D)))
            m.cube("shoe_" + k, Sh, (x - 1.2, 0, -3.4), (x + 1.2, 1.6, 1.3), 0x2E2C34, faces=af(metal(0x2E2C34, 0x4E4A56, 0x141216, False)))
            m.cube("toe_" + k, Sh, (x - 0.8, 0, -4.8), (x + 0.8, 1.1, -3.2), 0x2E2C34, faces=af(flat(0x26242C)))
            m.cube("sole_" + k, Sh, (x - 1.25, -0.01, -4.6), (x + 1.25, 0.35, 1.35), 0x8A8890, faces=af(flat(0x8A8890)))
        else:
            m.cube("thigh_" + k, L, (x - 1.2, 10.0, -1.25), (x + 1.2, 20.2, 1.25), SUIT, faces=suitp)
            m.cube("hipplate_" + k, L, (x - 1.35, 15.6, -1.4), (x + 1.35, 19.6, 1.4), SUIT_D, origin=(x, 17.6, 0), rot=(0, 0, 4 * s), faces=af(metal(SUIT, SUIT_L, SUIT_D, False)))
            m.cube("shinc_" + k, Sh, (x - 1.1, 3.0, -1.15), (x + 1.1, 10.4, 1.15), SUIT, faces=suitp)
            m.cube("knee_" + k, Sh, (x - 0.9, 8.8, -1.55), (x + 0.9, 11.2, -1.0), SUIT_D, faces=af(metal(SUIT_L, SUIT_L, SUIT_D, False)))
            m.cube("knee_glow_" + k, Sh, (x - 0.3, 9.6, -1.62), (x + 0.3, 10.4, -1.5), PINK_G, faces=af(flat(PINK_G, True)))
            m.cube("flare_" + k, Sh, (x - 1.6, 0, -2.6), (x + 1.6, 3.4, 1.8), SUIT_D, faces=af(metal(SUIT, SUIT_L, SUIT_DD, False)))
            m.cube("flare2_" + k, Sh, (x - 1.3, 3.2, -1.6), (x + 1.3, 4.6, 1.5), SUIT_D, faces=af(flat(SUIT_DD)))
            m.cube("toe_" + k, Sh, (x - 1.0, 0, -3.8), (x + 1.0, 1.4, -2.4), SUIT_DD, faces=af(flat(SUIT_DD)))

    # -------------------------------------------------------------- hips / torso
    if not cy:
        m.cube("pelvis", "body", (-2.5, 17.6, -1.45), (2.5, 19.4, 1.45), JK, faces=af(clothp))
        m.cube("belt", "body", (-2.6, 19.0, -1.55), (2.6, 20.6, 1.55), 0x141216, faces=af(metal(0x141216, 0x2E2C34, 0x060506, False)))
        m.cube("buckle", "body", (-0.7, 19.2, -1.75), (0.7, 20.4, -1.5), 0xB8BCC4, faces=af(metal(0xC8CCD4, 0xEEEEF2, 0x7A7E86, False)))
        m.cube("waist", "chest", (-2.4, 20.8, -1.4), (2.4, 25.4, 1.4), JK,
               faces=af(clothp) | {"north": shirt_front(False, 0.0, 0.62)})
        m.cube("ribs", "chest", (-3.3, 25.0, -1.75), (3.3, 31.0, 1.75), JK,
               faces=af(clothp) | {"north": shirt_front(True, 0.0, 1.0), "up": flat(JK_D)})
        m.cube("tie_knot", "chest", (-0.5, 29.4, -1.95), (0.5, 30.6, -1.7), TIE, faces=af(flat(TIE)))
        for s in (1, -1):
            k = "r" if s > 0 else "l"
            m.cube("lapel_" + k, "chest", (s * 1.6 - 0.45, 25.2, -1.95), (s * 1.6 + 0.45, 30.8, -1.72), JK_L, origin=(s * 1.6, 30.8, -1.8),
                   rot=(0, 0, -14 * s), faces=af(K.pointed(flat(JK_L), 6)))
            m.cube("collar_" + k, "chest", (s * 0.75 - 0.5, 29.8, -2.0), (s * 0.75 + 0.5, 31.6, -1.75), SHIRT, origin=(s * 0.75, 31.6, -1.85),
                   rot=(0, 0, 30 * s), faces=af(K.pointed(flat(SHIRT), 4)))
            m.cube("jhem_" + k, "chest", (s * 2.3 - 1.1, 19.0, -1.6), (s * 2.3 + 1.1, 21.2, 1.6), JK, origin=(s * 2.3, 21.2, 0),
                   rot=(0, 0, 6 * s), faces=af(K.pointed(clothp, 3)))
            # spiked shoulders
            x = 3.9 * s
            m.cube("pad_" + k, "chest", (x - 1.3, 29.2, -1.9), (x + 1.3, 31.4, 1.9), JK, origin=(x, 30.3, 0), rot=(0, 0, -12 * s), faces=af(metal(JK, JK_L, JK_D, False)))
            for j, (dz, L, rz, rx) in enumerate(((-1.1, 3.6, -26, -12), (0.2, 4.4, -40, 0), (1.3, 3.4, -58, 14))):
                K.thorn(f"pspike{j}_{k}", "chest", (x + 0.5 * s, 31.0, dz), L, 1.0, rx, rz * s, JK, JK_L)
        m.cube("neck", "chest", (-0.9, 30.6, -0.9), (0.9, 33.2, 0.9), SKIN_D, faces=af(flat(SKIN_D)))
    else:
        m.cube("pelvis", "body", (-2.6, 17.4, -1.5), (2.6, 20.8, 1.5), SUIT, faces=suitp)
        m.cube("belt", "body", (-2.7, 19.4, -1.6), (2.7, 20.6, 1.6), SUIT_DD, faces=af(flat(SUIT_DD)))
        m.cube("beltlight", "body", (-0.5, 19.6, -1.7), (0.5, 20.4, -1.55), PINK_G, faces=af(flat(PINK_G, True)))
        m.cube("waist", "chest", (-2.3, 20.8, -1.4), (2.3, 25.4, 1.4), SUIT, faces=suitp)
        for j in range(3):
            y = 21.4 + j * 1.3
            m.cube(f"abs{j}", "chest", (-1.8, y, -1.6), (1.8, y + 0.8, -1.3), SUIT_D, faces=af(flat(SUIT_DD if j % 2 else SUIT_D)))
        m.cube("ribs", "chest", (-3.4, 25.0, -1.8), (3.4, 31.0, 1.8), SUIT, faces=suitp | {"up": flat(SUIT_D)})
        for s in (1, -1):
            k = "r" if s > 0 else "l"
            m.cube("plate_" + k, "chest", (s * 1.65 - 1.45, 26.6, -2.15), (s * 1.65 + 1.45, 29.6, -1.7), PINK, origin=(s * 1.65, 28.1, -1.9),
                   rot=(0, 0, -6 * s), faces=af(plate))
            m.cube("plateb_" + k, "chest", (s * 1.3 - 1.0, 25.4, -2.0), (s * 1.3 + 1.0, 26.5, -1.7), PINK_D, faces=af(plate))
            x = 3.8 * s
            m.cube("pad_" + k, "chest", (x - 1.4, 28.8, -2.0), (x + 1.4, 31.4, 2.0), SUIT_L, origin=(x, 30.1, 0), rot=(0, 0, -14 * s), faces=af(metal(SUIT_L, 0xB8BED0, SUIT_D, False)))
            m.cube("padline_" + k, "chest", (x - 1.45, 29.4, -2.05), (x + 1.45, 29.8, 2.05), PINK_G, origin=(x, 30.1, 0), rot=(0, 0, -14 * s), faces=af(flat(PINK_G, True)))
        m.cube("collar", "chest", (-1.4, 30.4, -1.4), (1.4, 33.0, 1.4), TECH, faces=af(metal(TECH, TECH_L, TECH_D, False)))
        m.cube("spine", "chest", (-0.6, 22.0, 1.7), (0.6, 30.6, 2.3), SUIT_D, faces=af(metal(SUIT_D, SUIT, SUIT_DD)))

    # -------------------------------------------------------------- head
    m.cube("skull", "head", (-3.0, 32.6, -3.0), (3.0, 38.6, 2.6), SKIN,
           faces={"north": face, "east": face_side, "west": face_side, "south": hairw, "up": hairw, "down": flat(SKIN_D)})
    m.cube("chin", "jaw", (-2.0, 32.4, -3.02), (2.0, 33.8, -1.2), SKIN,
           faces=af(flat(SKIN_D)) | {"north": K.grad(SKIN, SKIN_D), "up": flat(0x3A0810)})
    if not cy:
        for s in (1, -1):
            K.thorn("fang_" + ("r" if s > 0 else "l"), "jaw", (s * 0.9, 33.6, -2.9), 1.0, 0.5, 180, 0, 0xFFFFFF, 0xD8D8D8)
    # hair spikes: flaring out at cheek level, crown, back
    spikes = [(2.8, 35.0, -1.0, 4.6, -100, -10), (2.8, 36.4, 0.2, 4.0, -78, 10), (2.6, 33.6, 0.8, 3.6, -125, 15), (2.4, 37.8, 1.2, 3.4, -55, 25),
              (2.0, 38.4, -1.8, 3.0, -35, -20), (1.6, 35.8, 2.4, 3.6, -100, 60)]
    for s, k in ((1, "r"), (-1, "l")):
        for j, (x, y, z, L, rz, rx) in enumerate(spikes):
            K.thorn(f"hspk{j}_{k}", "head", (x * s, y, z), L * (1.15 if cy else 1), 1.7, rx, rz * s, HAIR, HAIR_D)
    for j, (x, L, rz) in enumerate(((-1.6, 2.6, 14), (0.2, 3.2, -6), (1.8, 2.4, -16))):
        K.thorn(f"fringe{j}", "head", (x, 38.2, -3.05), L, 1.6, 170, rz, HAIR_L, HAIR_D)
    for j, (x, z, L, rx) in enumerate(((0, 2.6, 3.4, 70), (-1.6, 2.4, 3.0, 60), (1.6, 2.4, 3.0, 60), (0, 1.0, 2.6, 30))):
        K.thorn(f"backspk{j}", "head", (x, 37.4, z), L, 1.8, rx, 0, HAIR, HAIR_D)
    # black bat-horn ears
    for s, k in ((1, "r"), (-1, "l")):
        g = "ear_" + k
        K.thorn("earo_" + k, g, (2.6 * s, 38.0, 0.9), 8.6 if cy else 9.0, 3.0, 4, -24 * s, WING, WING_L)
        K.thorn("eari_" + k, g, (2.6 * s, 38.4, 0.5), 6.0, 1.6, 4, -24 * s, 0x4A4452, WING)
        K.thorn("earb_" + k, g, (2.9 * s, 38.0, 1.2), 3.6, 2.0, 14, -62 * s, WING, WING_L)
    if not cy:
        # tilted white box cap, black band + visor, emblem lens
        m.group("cap", (0, 38.4, -0.4), rot=(-4, 0, -9), parent="head")
        m.cube("capbox", "cap", (-3.3, 38.2, -3.4), (3.1, 42.6, 1.9), CAP, faces=af(K.combo(K.grad(0xFFFFFF, CAP_D), K.outline(0x9C9CA2))))
        m.cube("capband", "cap", (-3.35, 38.1, -3.45), (3.15, 39.0, 1.95), 0x18161C, faces=af(flat(0x18161C)))
        m.cube("visor", "cap", (-3.2, 38.1, -5.0), (3.0, 38.6, -3.3), 0x18161C, faces=af(metal(0x18161C, 0x34303A, 0x08070A, False)))
        def lens(F):
            W, H = F.w, F.h
            F.rect(0, 0, W, H, 0x101014)
            F.disc(W / 2, H / 2, min(W, H) / 2 - 1, RED_G, glow=True)
            F.disc(W / 2, H / 2, min(W, H) / 2 - 3, 0x101014)
            F.line(W / 2 - 4, H / 2 - 4, W / 2 + 4, H / 2 + 4, RED_G, 1.5, glow=True)
            F.line(W / 2 + 4, H / 2 - 4, W / 2 - 4, H / 2 + 4, RED_G, 1.5, glow=True)
        m.cube("lens", "cap", (-0.2, 39.3, -3.62), (2.7, 42.1, -3.35), 0x101014, faces=af(flat(0x101014)) | {"north": lens})
        m.cube("lens2", "cap", (-2.6, 40.6, -3.5), (-1.2, 41.9, -3.35), 0x101014, faces=af(flat(0x2A2A30)))
    else:
        # goggles + headset
        for s, k in ((1, "r"), (-1, "l")):
            m.cube("goggle_" + k, "head", (s * 1.45 - 1.45, 34.4, -3.45), (s * 1.45 + 1.45, 37.3, -2.95), 0x0E0C10,
                   faces=af(clear) | {"north": goggle, "south": goggle})
            m.cube("phone_" + k, "head", (s * 3.0 - 0.4, 34.2, -1.6), (s * 3.0 + 0.4, 37.2, 1.0), SUIT_D, faces=af(metal(SUIT, SUIT_L, SUIT_D, False)))
            m.cube("phonel_" + k, "head", (s * 3.4 - 0.05, 35.2, -0.8), (s * 3.4 + 0.05, 36.2, 0.2), PINK_G, faces=af(flat(PINK_G, True)))
        m.cube("gbridge", "head", (-0.4, 35.6, -3.3), (0.4, 36.1, -3.0), TECH, faces=af(flat(TECH)))
        m.cube("gband", "head", (-3.05, 35.4, -3.0), (3.05, 36.2, 2.65), TECH, faces=af(flat(TECH)) | {"north": clear})

    # -------------------------------------------------------------- long cape-like hair strands
    for s, k in ((1, "r"), (-1, "l")):
        g1, g2 = "hair_" + k, "hair_" + k + "2"
        for j in range(2):
            x = (2.6 + j * 1.3) * s
            K.plane(f"lockA{j}_{k}", g1, (x, 36.2, 2.1 + j * 0.6), 3.0, 14.4, capep, rot=(6 + j * 4, 0, (3 + j * 6) * s))
        for j in range(2):
            x = (4.0 + j * 1.2) * s
            K.plane(f"lockB{j}_{k}", g2, (x, 23.4, 3.1 + j * 0.5), 3.0 - j * 0.4, 12.5 - j * 3.0, K.pointed(capep, 10), rot=(4 + j * 4, 0, (4 + j * 7) * s))
    for j in range(3):
        K.plane(f"lockC{j}", "hair_c", ((j - 1) * 1.8, 36.6, 2.7 + abs(j - 1) * 0.2), 2.8, 17.0 - abs(j - 1) * 3.0, K.pointed(capep, 10), rot=(10, 0, (j - 1) * 5))

    # -------------------------------------------------------------- wings
    ws = 1.55 if cy else 1.3
    for s, k in ((1, "r"), (-1, "l")):
        g = "wing_" + k
        W_, H_ = 9.0 * ws, 8.0 * ws
        x0, x1 = (1.2, 1.2 + W_) if s > 0 else (-1.2 - W_, -1.2)
        root_left_n = s < 0
        m.cube("membrane_" + k, g, (x0, 29.6 - H_ * 0.62, 1.88), (x1, 29.6 + H_ * 0.38, 2.0), WING,
               faces=af(clear) | {"north": bat(not root_left_n), "south": bat(root_left_n)})
        m.cube("wbone_" + k, g, (min(1.2 * s, (1.2 + W_ * 0.95) * s), 29.4, 1.8), (max(1.2 * s, (1.2 + W_ * 0.95) * s), 30.0, 2.1), WING_L,
               origin=(1.2 * s, 29.7, 1.95), rot=(0, 0, 15 * s), faces=af(flat(WING_L)))
        K.thorn("wclaw_" + k, g, ((1.2 + W_ * 0.42) * s, 31.4, 1.95), 1.6, 0.6, 0, -20 * s, WING_L, WING_D)

    # -------------------------------------------------------------- arms
    for s, k in ((1, "r"), (-1, "l")):
        x = 4.1 * s
        if not cy:
            def sleeve_badge(F):
                clothp(F)
                F.disc(F.w / 2, 10, 4.5, 0xFFFFFF); F.disc(F.w / 2, 10, 3.6, RED)
                F.line(F.w / 2 + 1.5, 8, F.w / 2 - 1.5, 9.6, 0xFFFFFF, 1); F.line(F.w / 2 - 1.5, 10, F.w / 2 + 1.5, 11.6, 0xFFFFFF, 1)
                F.line(F.w / 2 + 1.5, 11.6, F.w / 2 - 1.5, 12.4, 0xFFFFFF, 1)
            m.cube("upper_" + k, "arm_" + k, (x - 0.9, 24.6, -0.95), (x + 0.9, 31.0, 0.95), JK, faces=af(clothp) | ({"north": sleeve_badge} if s > 0 else {}))
            m.cube("elbow_" + k, "fore_" + k, (x - 0.95, 24.0, -1.0), (x + 0.95, 25.4, 1.0), JK_D, faces=af(flat(JK_D)))
        else:
            m.cube("upper_" + k, "arm_" + k, (x - 0.95, 24.6, -1.0), (x + 0.95, 31.0, 1.0), SUIT, faces=suitp)
            m.cube("elbow_" + k, "fore_" + k, (x - 1.0, 24.0, -1.05), (x + 1.0, 25.4, 1.05), SUIT_D, faces=af(metal(SUIT_D, SUIT, SUIT_DD, False)))
    # RIGHT arm: sleeve, white cuff, black clawed glove
    x = 4.1
    if not cy:
        m.cube("forec_r", "fore_r", (x - 0.85, 20.2, -0.9), (x + 0.85, 24.6, 0.9), JK, faces=af(clothp))
        m.cube("cuffw_r", "fore_r", (x - 0.95, 19.6, -0.95), (x + 0.95, 20.6, 0.95), SHIRT, faces=af(flat(SHIRT)))
    else:
        m.cube("forec_r", "fore_r", (x - 0.9, 19.8, -0.95), (x + 0.9, 24.6, 0.95), SUIT, faces=suitp)
        m.cube("cuffw_r", "fore_r", (x - 1.0, 19.4, -1.0), (x + 1.0, 20.4, 1.0), PINK_D, faces=af(flat(PINK_G, True)))
    m.cube("palm_r", "hand_r", (x - 0.85, 17.4, -0.85), (x + 0.85, 19.8, 0.85), TECH, faces=af(metal(0x1E1C22, 0x3A3640, 0x0C0B0E, False)))
    for f in range(4):
        fz = -0.65 + f * 0.43
        m.cube(f"claw{f}", "hand_r", (x - 0.16 + 0.3, 14.8, fz - 0.16), (x + 0.16 + 0.3, 17.6, fz + 0.16), TECH, origin=(x + 0.3, 17.6, fz),
               rot=(-10 + f * 6, 0, 6), faces=af(K.grad(0x3A3640, 0x050406)))
    m.cube("thumb_r", "hand_r", (x - 1.0, 15.8, -0.9), (x - 0.7, 17.8, -0.6), TECH, origin=(x - 0.85, 17.8, -0.75), rot=(-14, 0, -14), faces=af(flat(TECH)))

    # LEFT arm: weapon
    x = -4.1
    if not cy:
        m.cube("forec_l", "fore_l", (x - 0.85, 21.2, -0.9), (x + 0.85, 24.6, 0.9), JK, faces=af(clothp))
        m.cube("ring_l", "fore_l", (x - 1.05, 20.6, -1.05), (x + 1.05, 21.6, 1.05), GUN_L, faces=af(metal(GUN_L, 0x8A8A96, GUN_D, False)))
        m.cube("receiver", "gun", (x - 1.0, 14.6, -1.35), (x + 1.0, 20.8, 1.35), GUN, faces=af(gunp))
        m.cube("scope", "gun", (x - 0.55, 15.4, -2.5), (x + 0.55, 20.0, -1.35), GUN_D, faces=af(metal(GUN_D, GUN, 0x08080A, False)))
        m.cube("scopelens", "gun", (x - 0.4, 15.2, -2.35), (x + 0.4, 15.45, -1.5), RED_G, faces=af(flat(RED_G, True)))
        m.cube("grip", "gun", (x - 0.5, 16.6, 1.3), (x + 0.5, 19.4, 2.6), GUN_D, origin=(x, 19.4, 1.9), rot=(-18, 0, 0), faces=af(flat(GUN_D)))
        m.cube("mag", "gun", (x - 2.6, 14.4, -0.8), (x - 0.95, 20.0, 0.8), MAG, origin=(x - 1.0, 20.0, 0), rot=(0, 0, 10), faces=af(maga))
        m.cube("shroud", "gun", (x - 0.8, 9.4, -0.8), (x + 0.8, 14.8, 0.8), GUN, faces=af(K.combo(gunp, lambda F: [F.rect(i, 3, 1, F.h - 6, GUN_D) for i in range(1, F.w - 1, 3)])))
        m.cube("barrel", "gun", (x - 0.45, 4.6, -0.45), (x + 0.45, 9.6, 0.45), GUN_D, faces=af(metal(GUN_D, GUN_L, 0x08080A, False)))
        m.cube("muzzle", "gun", (x - 0.75, 3.4, -0.75), (x + 0.75, 4.8, 0.75), GUN_D, faces=af(gunp) | {"down": lambda F: (F.rect(0, 0, F.w, F.h, GUN_D), F.disc(F.w / 2, F.h / 2, 2.2, 0x050505))})
        m.cube("sign", "gun", (x - 2.4, 5.4, -0.95), (x + 2.4, 9.6, -0.82), 0xFFFFFF, faces=af(clear) | {"north": warn, "south": warn})
        m.cube("signpost", "gun", (x - 0.15, 7.4, -0.85), (x + 0.15, 8.8, -0.45), GUN_D, faces=af(flat(GUN_D)))
    else:
        # huge black tech arm: forearm block, spikes, glowing magazine strip, warning sign, cannon bore + claws
        m.cube("techshoulder", "arm_l", (x - 1.9, 27.6, -1.9), (x + 1.3, 31.8, 1.9), TECH, faces=af(techp))
        K.thorn("tspk_s", "arm_l", (x - 1.6, 31.2, 0.6), 3.4, 1.2, 20, 40, TECH, TECH_L)
        m.cube("techfore", "gun", (x - 2.0, 11.0, -1.8), (x + 1.4, 24.6, 1.8), TECH, faces=af(techp))
        m.cube("techcuff", "gun", (x - 2.2, 9.6, -2.0), (x + 1.6, 11.6, 2.0), TECH_L, faces=af(metal(TECH_L, 0x5A5464, TECH_D, False)))
        m.cube("magstrip", "gun", (x - 2.25, 12.0, -1.3), (x - 1.95, 22.8, 0.1), PINK, faces=af(flat(TECH_D)) | {"west": strip, "east": strip})
        m.cube("magfront", "gun", (x - 0.8, 12.4, -1.95), (x + 0.6, 19.0, -1.75), PINK, faces=af(flat(TECH_D)) | {"north": strip})
        m.cube("signc", "gun", (x - 1.0, 19.8, -2.05), (x + 1.0, 21.8, -1.8), RED, faces=af(flat(TECH)) | {"north": warn_circle})
        for j, (y, L, rz) in enumerate(((22.6, 3.6, 62), (19.0, 4.2, 66), (15.4, 3.8, 70), (12.2, 3.0, 74))):
            K.thorn(f"tfin{j}", "gun", (x - 1.8, y, 1.2), L, 1.3, 40, rz, TECH, TECH_L)
        m.cube("bore", "gun", (x - 1.0, 9.2, -1.0), (x + 0.6, 9.7, 0.8), 0x050505, faces=af(flat(0x050505)) | {"down": lambda F: (F.rect(0, 0, F.w, F.h, TECH), F.disc(F.w / 2, F.h / 2, 3, RED_G, glow=True))})
        for f in range(3):
            fz = -1.3 + f * 1.25
            m.cube(f"tclaw{f}", "gun", (x - 2.0 + 0.2, 7.0, fz - 0.3), (x - 2.0 + 0.8, 10.0, fz + 0.3), TECH, origin=(x - 1.5, 10.0, fz),
                   rot=(0, 0, -16), faces=af(K.grad(TECH_L, 0x050406)))
    # muzzle flash prop (glow)
    fy = 9.6 if cy else 3.4
    sz = 1.5 if cy else 1.0
    def star(F):
        F.rect(0, 0, F.w, F.h, CLEAR)
        F.poly([(F.w / 2, 0), (F.w * 0.62, F.h * 0.4), (F.w, F.h / 2), (F.w * 0.62, F.h * 0.6), (F.w / 2, F.h), (F.w * 0.38, F.h * 0.6), (0, F.h / 2), (F.w * 0.38, F.h * 0.4)], YEL, glow=True)
        F.disc(F.w / 2, F.h / 2, F.w * 0.16, 0xFFFFFF, glow=True)
    for j, ry in enumerate((0, 90)):
        m.cube(f"flash{j}", "flash", (x - 1.6 * sz, fy - 4.0 * sz, -0.05), (x + 1.6 * sz, fy, 0.05), YEL, origin=(x, fy, 0), rot=(0, ry, 0),
               faces=af(clear) | {"north": star, "south": star})
    m.cube("flashcore", "flash", (x - 0.6 * sz, fy - 1.6 * sz, -0.6 * sz), (x + 0.6 * sz, fy - 0.2, 0.6 * sz), YEL, faces=af(flat(0xFFF6C0, True)))

    # -------------------------------------------------------------- whip tail (tapering), spade tip
    for i, b in enumerate(TAIL):
        t = 1.0 - i * 0.09
        z0 = 1.4 + 4.4 * i
        tc = (0xFF2020, 0x20FF20) if os.environ.get("DBG_TAIL") else (WING_L, WING_D)   # debug: bright tail for the dark preview
        m.cube("tailc" + str(i), b, (-t / 2, 19.4 - t / 2, z0), (t / 2, 19.4 + t / 2, z0 + 4.6), WING, faces=af(K.grad(*tc)))
    zt = 1.4 + 4.4 * 6
    m.cube("tailtip", "tail5", (-1.2, 19.35, zt - 0.4), (1.2, 19.45, zt + 2.2), WING, faces=af(flat(WING)) | {"up": K.pointed(flat(WING), 10), "down": K.pointed(flat(WING), 10)})
    m.cube("tailtipv", "tail5", (-0.05, 18.2, zt - 0.4), (0.05, 20.6, zt + 2.2), WING, faces=af(flat(WING)) | {"east": K.pointed(flat(WING), 10), "west": K.pointed(flat(WING), 10)})
    return m, K


# ================================================================== animation helpers
PROPS = ("flash",)
HAIRS = ("hair_r", "hair_l", "hair_c")


def legs(a, kr, kl=None, sr=None, sl=None):
    a.r("leg_r", *kr)
    a.r("leg_l", *(kl or [(t, x, -y, -z) for (t, x, y, z) in kr]))
    if sr: a.r("shin_r", *sr)
    if sl or sr: a.r("shin_l", *(sl or sr))


def sec(a, keys, d=1, tail=True, wings=True):
    """secondary motion from body motion keys (t, pitch, yaw, roll): pitch<0 = thrown forward (hair/wings fling back)"""
    a.lag("hair_r", [(t, -x * 0.5, 0, z * 0.4 + abs(x) * 0.25) for (t, x, y, z) in keys], d + 1)
    a.lag("hair_l", [(t, -x * 0.5, 0, z * 0.4 - abs(x) * 0.25) for (t, x, y, z) in keys], d + 1)
    a.lag("hair_r2", [(t, -x * 0.35, 0, z * 0.3 + abs(x) * 0.2) for (t, x, y, z) in keys], d + 3)
    a.lag("hair_l2", [(t, -x * 0.35, 0, z * 0.3 - abs(x) * 0.2) for (t, x, y, z) in keys], d + 3)
    a.lag("hair_c", [(t, -x * 0.6, 0, z * 0.3) for (t, x, y, z) in keys], d + 2)
    a.lag("ear_r", [(t, x * 0.2, 0, -abs(x) * 0.15) for (t, x, y, z) in keys], d)
    a.lag("ear_l", [(t, x * 0.2, 0, abs(x) * 0.15) for (t, x, y, z) in keys], d)
    if wings:
        a.lag("wing_r", [(t, 0, -abs(x) * 0.6 + y * 0.3, z * 0.3) for (t, x, y, z) in keys], d + 1)
        a.lag("wing_l", [(t, 0, abs(x) * 0.6 + y * 0.3, z * 0.3) for (t, x, y, z) in keys], d + 1)
    if tail:
        a.wave(("tail", "tail1", "tail2", "tail3", "tail4", "tail5"), [(t, -x * 0.4, -y * 0.6 + z * 0.5, 0) for (t, x, y, z) in keys], 1.5)
    return a


def flashes(a, ticks, big=1.3):
    ks = [(0, *HIDE)]
    for t in ticks:
        ks += [(t - 0.3, *HIDE), (t, big, big, big), (t + 0.8, big * 0.6, big * 0.6, big * 0.6), (t + 1.4, *HIDE)]
    ks.append((a.ticks, *HIDE))
    seen, out = set(), []
    for k in sorted(ks):
        if k[0] in seen: continue
        seen.add(k[0]); out.append(k)
    a.scl("flash", *out)


def tailk(a, keys, scale=(1, 1, 1, 1, 1, 1), delay=1.0):
    """explicit whip: keys (t, rx, ry, 0) for the base; each further segment gets scale[i] * keys, lagged"""
    for i, b in enumerate(("tail", "tail1", "tail2", "tail3", "tail4", "tail5")):
        if i == 0:
            a.r(b, *keys)
        else:
            a.lag(b, [(t, x * scale[i], y * scale[i], z * scale[i]) for (t, x, y, z) in keys], delay * i)


def tailpose(a, poses):
    """explicit whole-tail poses: poses = [(t, [rx0..rx5], ry0, rz0)] (rx deltas per segment, ry/rz on the base).
    The tail root sits at the small of the back, so over-the-shoulder poses tilt it to his right (rz<0) to clear the torso/head."""
    for i, b in enumerate(("tail", "tail1", "tail2", "tail3", "tail4", "tail5")):
        a.r(b, *[(p[0], p[1][i], p[2] if i == 0 else 0, (p[3] if len(p) > 3 else 0) if i == 0 else 0) for p in poses])


T_LOW = [10, 10, 10, 10, 10, 10]
T_OVER = [-118, -42, -38, -14, 0, 8]          # rears up behind the right shoulder, tip hooked forward
T_COIL = [-118, -30, -20, 0, 10, 20]          # raised high, tip hooked forward
T_SPEAR = [-118, -62, -58, 16, 25, 23]        # straight forward past the right shoulder
T_CRACK = [-118, -62, -58, -4, 10, 8]         # lashed forward and down
T_ZERO = [0] * 6



# ================================================================== MATURED
def anims_matured(m):
    def NA(n, t, loop=False): return A(m, n, t, loop, PROPS)

    # idle (80): cocky slouch, breathing, rifle hanging heavy, tail swish, ear twitch, hand flex
    a = NA("idle", 80, True)
    a.pos("body", (0, 0, 0, 0), (20, 0, -0.25, 0), (40, 0, 0, 0), (60, 0, -0.25, 0), (80, 0, 0, 0))
    a.rot("chest", (0, -3, 0, 0), (20, -1, 3, 1), (40, -3, 0, 0), (60, -1, -3, -1), (80, -3, 0, 0))
    a.rot("head", (0, 0, 0, 6), (24, -3, 6, 9), (40, 0, 0, 6), (64, -2, -5, 3), (80, 0, 0, 6))
    a.rot("arm_r", (0, 4, 0, 4), (40, 8, 0, 6), (80, 4, 0, 4))
    a.rot("fore_r", (0, 12, 0, 0), (40, 16, 0, 0), (80, 12, 0, 0))
    a.rot("hand_r", (0, 0, 0, 0), (46, 0, 0, 0), (49, -20, 0, 0), (52, 6, 0, 0), (55, -14, 0, 0), (58, 0, 0, 0), (80, 0, 0, 0))
    a.rot("arm_l", (0, 6, 0, -3), (40, 4, 0, -5), (80, 6, 0, -3))
    a.rot("fore_l", (0, 6, 0, 0), (40, 8, 0, 0), (80, 6, 0, 0))
    a.rot("leg_r", (0, -2, 0, 2), (80, -2, 0, 2))
    a.rot("leg_l", (0, 4, 0, -3), (80, 4, 0, -3))
    a.rot("shin_l", (0, -6, 0, 0), (80, -6, 0, 0))
    a.rot("ear_r", (0, 0, 0, 0), (50, 0, 0, 0), (52, -10, 0, -12), (54, 0, 0, 0), (56, -8, 0, -8), (58, 0, 0, 0), (80, 0, 0, 0))
    a.rot("ear_l", (0, 0, 0, 0), (20, 0, 0, 0), (22, -10, 0, 12), (24, 0, 0, 0), (80, 0, 0, 0))
    for b, ph, amp in (("tail", 0, (4, 10, 0)), ("tail1", 6, (4, 12, 0)), ("tail2", 12, (5, 14, 0)), ("tail3", 18, (6, 16, 0)), ("tail4", 24, (6, 18, 0)), ("tail5", 30, (8, 20, 0)),
                       ("wing_r", 0, (0, 6, 3)), ("wing_l", 0, (0, -6, -3)), ("hair_r", 10, (2, 0, 2)), ("hair_l", 30, (2, 0, -2)), ("hair_r2", 20, (2, 0, 3)), ("hair_l2", 40, (2, 0, -3)), ("hair_c", 15, (3, 0, 1))):
        a.rot(b, *sinekeys(80, 10, amp, ph))
    a.done()

    # walk (24): long lanky strides, swagger, rifle swinging, tail + hair trailing
    a = NA("walk", 24, True)
    a.pos("body", (0, 0, 0, 0), (6, 0, 0.8, 0), (12, 0, 0, 0), (18, 0, 0.8, 0), (24, 0, 0, 0))
    a.rot("body", (0, 0, 6, 0), (6, 0, 0, 2), (12, 0, -6, 0), (18, 0, 0, -2), (24, 0, 6, 0))
    a.rot("chest", (0, -6, -8, 0), (12, -6, 8, 0), (24, -6, -8, 0))
    a.rot("leg_r", (0, 34, 0, 0), (6, 0, 0, 0), (12, -30, 0, 0), (18, 0, 0, 0), (24, 34, 0, 0))
    a.rot("leg_l", (0, -30, 0, 0), (6, 0, 0, 0), (12, 34, 0, 0), (18, 0, 0, 0), (24, -30, 0, 0))
    a.rot("shin_r", (0, 0, 0, 0), (14, -50, 0, 0), (19, -18, 0, 0), (24, 0, 0, 0))
    a.rot("shin_l", (0, 0, 0, 0), (2, -50, 0, 0), (7, -18, 0, 0), (12, 0, 0, 0), (24, 0, 0, 0))
    a.rot("arm_r", (0, -26, 0, 6), (12, 30, 0, 8), (24, -26, 0, 6))
    a.rot("fore_r", (0, 10, 0, 0), (12, 30, 0, 0), (24, 10, 0, 0))
    a.rot("arm_l", (0, 16, 0, -4), (12, -12, 0, -6), (24, 16, 0, -4))
    a.rot("fore_l", (0, 6, 0, 0), (12, 2, 0, 0), (24, 6, 0, 0))
    a.rot("head", (0, 4, -6, -3), (6, 2, 0, 0), (12, 4, 6, 3), (18, 2, 0, 0), (24, 4, -6, -3))
    for b, ph, amp in (("tail", 0, (4, 12, 0)), ("tail1", 2, (4, 14, 0)), ("tail2", 4, (6, 16, 0)), ("tail3", 6, (6, 18, 0)), ("tail4", 8, (8, 18, 0)), ("tail5", 10, (8, 20, 0))):
        a.rot(b, *sinekeys(24, 3, amp, ph))
    for b, base in (("hair_r", (-8, 0, 4)), ("hair_l", (-8, 0, -4)), ("hair_r2", (-6, 0, 4)), ("hair_l2", (-6, 0, -4)), ("hair_c", (-10, 0, 0))):
        a.rot(b, *sinekeys(24, 3, (3, 0, 2), 4, base=base))
    a.rot("wing_r", (0, 0, -8, 0), (6, 0, -4, 6), (12, 0, -8, 0), (18, 0, -4, 6), (24, 0, -8, 0))
    a.rot("wing_l", (0, 0, 8, 0), (6, 0, 4, -6), (12, 0, 8, 0), (18, 0, 4, -6), (24, 0, 8, 0))
    a.done()

    # rifle_burst (34): swing rifle up 0-9 (torso turns right so the rifle shoulder leads), aim, 3 shots t14/17/20, lower 26-34
    a = NA("rifle_burst", 34)
    a.r("arm_l", (5, 60, 0, -10), (9, 96, 0, 6), (11, 90, 0, 8), (14, 90, 0, 8), (14.6, 104, 0, 8), (16, 90, 0, 8), (17, 90, 0, 8), (17.6, 104, 0, 8), (19, 90, 0, 8), (20, 90, 0, 8), (20.6, 108, 0, 8), (22, 92, 0, 8), (26, 86, 0, 8), (31, 20, 0, 0))
    a.r("fore_l", (9, -4, 0, 0), (26, -4, 0, 0), (31, 6, 0, 0))
    a.r("chest", (6, 0, -18, 0), (9, 2, -26, 0), (14, 2, -26, 0), (14.6, 6, -24, 0), (16, 2, -26, 0), (17.6, 6, -24, 0), (19, 2, -26, 0), (20.6, 8, -23, 0), (24, 2, -24, 0), (30, 0, -4, 0))
    a.r("head", (6, 0, 16, -4), (9, -4, 24, -10), (24, -4, 24, -10), (30, 0, 4, 0))
    a.r("arm_r", (6, 30, 0, 30), (10, 40, 0, 40), (24, 40, 0, 40), (30, 10, 0, 6))
    a.r("fore_r", (10, 40, 0, 0), (24, 40, 0, 0))
    a.p("body", (8, 0, -0.6, 0.3), (14, 0, -0.6, 0.3), (14.6, 0, -0.6, 0.7), (17.6, 0, -0.6, 0.9), (20.6, 0, -0.6, 1.2), (24, 0, -0.4, 0.6), (30, 0, 0, 0))
    legs(a, [(8, 16, 0, 2), (24, 16, 0, 2), (30, 0, 0, 0)], [(8, -16, 0, -4), (24, -16, 0, -4), (30, 0, 0, 0)], sr=[(8, -10, 0, 0), (24, -10, 0, 0)], sl=[(8, -14, 0, 0), (24, -14, 0, 0)])
    flashes(a, (14, 17, 20))
    sec(a, [(0, 0, 0, 0), (9, 0, -20, 0), (14, 4, -20, 4), (17, 4, -20, -4), (20, 6, -20, 4), (26, 0, -10, 0), (34, 0, 0, 0)])
    a.done()

    # rifle_bash (28): rifle cocked far out-left 0-8, horizontal butt-swing hits t11, follow-through 11-15, recover
    a = NA("rifle_bash", 28)
    a.r("arm_l", (4, 30, -10, -60), (8, 40, -20, -100), (10, 80, 0, -30), (11, 92, 0, 10), (13, 80, 0, 50), (15, 70, 0, 60), (20, 40, 0, 30), (26, 0, 0, 0))
    a.r("fore_l", (8, 30, 0, 0), (11, 0, 0, 0), (15, 10, 0, 0), (24, 0, 0, 0))
    a.r("chest", (4, 4, 30, 6), (8, 6, 44, 8), (10, -4, 10, 0), (11, -10, -22, -4), (13, -12, -40, -6), (16, -8, -36, -4), (22, -2, -10, 0))
    a.r("head", (8, 0, -30, 0), (11, -6, 14, 0), (14, -4, 26, 0), (22, 0, 6, 0))
    a.r("arm_r", (6, -20, 0, 30), (8, -30, 0, 40), (11, 30, 0, 20), (14, 50, 0, 10), (22, 10, 0, 6))
    a.r("fore_r", (8, 30, 0, 0), (14, 50, 0, 0), (22, 10, 0, 0))
    a.p("body", (6, 0, -0.6, 1.0), (8, 0, -0.8, 1.2), (11, 0, -1.0, -1.8), (14, 0, -0.8, -2.2), (20, 0, -0.3, -0.8), (26, 0, 0, 0))
    legs(a, [(6, 10, 0, 0), (11, -34, 0, 0), (16, -28, 0, 0), (24, 0, 0, 0)], [(6, -8, 0, 0), (11, 26, 0, 0), (16, 20, 0, 0), (24, 0, 0, 0)],
         sr=[(11, -10, 0, 0), (16, -10, 0, 0), (24, 0, 0, 0)], sl=[(11, -30, 0, 0), (16, -26, 0, 0), (24, 0, 0, 0)])
    sec(a, [(0, 0, 0, 0), (8, 2, 40, 6), (11, -10, -20, -8), (14, -10, -40, -10), (22, -2, -10, 0), (28, 0, 0, 0)])
    a.done()

    # tail_whip (30): tail sweeps low behind 0-7, rears up over the shoulder 7-11, CRACKS forward/down t13, recoils 15-20, settles
    a = NA("tail_whip", 30)
    tailpose(a, [(4, T_LOW, 40, 0), (8, T_OVER, 10, -39), (11, T_COIL, 0, -39), (13, T_CRACK, 0, -36), (15, T_CRACK, 0, -36),
                 (18, [-80, -30, -20, 0, 0, 0], 6, -14), (24, [-10, 0, 0, 0, 0, 0], 0, 0), (30, T_ZERO, 0, 0)])
    a.r("chest", (4, 4, 20, 4), (8, 10, 30, 6), (11, 0, 10, 0), (13, -18, -14, 0), (16, -14, -10, 0), (24, 0, 0, 0))
    a.r("head", (8, 6, -20, 0), (13, -10, 10, 0), (20, 0, 0, 0))
    a.r("arm_r", (6, -20, 0, 50), (10, -30, 0, 60), (13, 40, 0, 20), (20, 20, 0, 10), (26, 0, 0, 0))
    a.r("arm_l", (6, 10, 0, -30), (13, 30, 0, -10), (24, 0, 0, 0))
    a.p("body", (8, 0, 0.6, 0.6), (11, 0, 1.0, 0.4), (13, 0, -1.0, -1.2), (18, 0, -0.4, -0.6), (26, 0, 0, 0))
    legs(a, [(8, -6, 0, 0), (13, -20, 0, 0), (22, 0, 0, 0)], [(8, 10, 0, 0), (13, 22, 0, 0), (22, 0, 0, 0)], sr=[(13, -10, 0, 0)], sl=[(13, -24, 0, 0)])
    sec(a, [(0, 0, 0, 0), (8, 6, 20, 0), (13, -14, -10, 0), (20, -2, 0, 0), (30, 0, 0, 0)], tail=False)
    a.done()

    # fang_bite (32): crouch 0-6, lunge t7, jaw gapes 8-11, BITE t12, drains 12-22 (shaking), shoves off t24, recover
    a = NA("fang_bite", 32)
    a.p("body", (4, 0, -2.4, 0.6), (6, 0, -2.6, 0.8), (8, 0, -1.0, -2.6), (12, 0, -1.4, -3.0), (22, 0, -1.4, -3.0), (24, 0, -0.6, -1.0), (30, 0, 0, 0))
    a.r("chest", (4, -20, 0, 0), (6, -24, 0, 0), (8, -30, 0, 0), (12, -34, 0, 0), (16, -32, 6, 0), (18, -34, -6, 0), (20, -32, 6, 0), (22, -32, 0, 0), (24, -6, 0, 0), (30, 0, 0, 0))
    a.r("head", (6, 20, 0, 0), (10, 26, 0, 0), (12, -6, 0, 0), (16, -2, 8, 4), (18, -2, -8, -4), (20, -2, 8, 4), (22, 0, 0, 0), (24, 10, 0, 0), (30, 0, 0, 0))
    a.r("jaw", (6, 0, 0, 0), (9, -38, 0, 0), (11, -42, 0, 0), (12, -2, 0, 0), (22, -4, 0, 0), (24, -20, 0, 0), (27, 0, 0, 0))
    for s, k in ((1, "r"), (-1, "l")):
        a.r("arm_" + k, (6, -30, 0, 30 * s), (8, 60, 0, 40 * s), (12, 90, 0, -10 * s), (22, 90, 0, -14 * s), (24, 30, 0, 30 * s), (30, 0, 0, 0))
        a.r("fore_" + k, (8, 10, 0, 0), (12, 40, 0, 0), (22, 40, 0, 0), (26, 0, 0, 0))
    legs(a, [(4, 40, 0, 0), (6, 44, 0, 0), (8, -10, 0, 0), (12, 30, 0, 0), (22, 30, 0, 0), (26, 0, 0, 0)], [(4, 30, 0, 0), (6, 30, 0, 0), (8, -40, 0, 0), (12, -30, 0, 0), (22, -30, 0, 0), (26, 0, 0, 0)],
         sr=[(4, -70, 0, 0), (8, -10, 0, 0), (12, -40, 0, 0), (22, -40, 0, 0), (26, 0, 0, 0)], sl=[(4, -60, 0, 0), (8, -20, 0, 0), (12, -30, 0, 0), (22, -30, 0, 0), (26, 0, 0, 0)])
    a.r("wing_r", (6, 0, 20, 30), (8, 0, -30, -10), (12, 0, 10, 40), (22, 0, 10, 40), (26, 0, 0, 0))
    a.r("wing_l", (6, 0, -20, -30), (8, 0, 30, 10), (12, 0, -10, -40), (22, 0, -10, -40), (26, 0, 0, 0))
    sec(a, [(0, 0, 0, 0), (6, -10, 0, 0), (8, -30, 0, 0), (12, -30, 0, 0), (22, -26, 0, 0), (24, 4, 0, 0), (32, 0, 0, 0)], wings=False)
    a.done()

    # wing_dash (30): wings fold, crouch 0-6, dash t7 (low and flat), claw rake t11, wings snap open to brake t14, recover
    a = NA("wing_dash", 30)
    a.p("body", (5, 0, -2.0, 1.0), (7, 0, -2.6, -1.6), (11, 0, -2.0, -3.0), (14, 0, -0.6, -2.0), (20, 0, 0, -0.6), (28, 0, 0, 0))
    a.r("chest", (5, -24, 0, 0), (7, -44, 0, 0), (11, -30, -30, 0), (13, -20, -40, 0), (14, -4, -20, 0), (20, 0, 0, 0))
    a.r("head", (5, 20, 0, 0), (7, 34, 0, 0), (11, 20, 24, 0), (14, 4, 10, 0), (20, 0, 0, 0))
    a.r("arm_r", (5, -40, 0, 20), (7, -60, 0, 10), (9, 100, 0, 60), (11, 110, 0, -40), (13, 90, 0, -60), (16, 40, 0, -20), (24, 0, 0, 0))
    a.r("fore_r", (9, 40, 0, 0), (11, 0, 0, 0), (16, 20, 0, 0), (24, 0, 0, 0))
    a.r("arm_l", (5, -40, 0, -20), (7, -60, 0, -10), (11, -30, 0, -20), (14, 10, 0, -40), (24, 0, 0, 0))
    a.r("wing_r", (4, 0, 30, -20), (7, 0, 50, -30), (11, 0, 50, -30), (13, 0, -30, 40), (14, 0, -40, 50), (18, 0, -20, 20), (26, 0, 0, 0))
    a.r("wing_l", (4, 0, -30, 20), (7, 0, -50, 30), (11, 0, -50, 30), (13, 0, 30, -40), (14, 0, 40, -50), (18, 0, 20, -20), (26, 0, 0, 0))
    legs(a, [(5, 40, 0, 0), (7, -20, 0, 0), (11, 30, 0, 0), (14, 40, 0, 0), (22, 0, 0, 0)], [(5, 20, 0, 0), (7, -60, 0, 0), (11, -50, 0, 0), (14, -20, 0, 0), (22, 0, 0, 0)],
         sr=[(5, -60, 0, 0), (7, -10, 0, 0), (11, -40, 0, 0), (14, -20, 0, 0), (22, 0, 0, 0)], sl=[(5, -50, 0, 0), (7, -40, 0, 0), (11, -60, 0, 0), (14, -20, 0, 0), (22, 0, 0, 0)])
    sec(a, [(0, 0, 0, 0), (5, -10, 0, 0), (7, -40, 0, 0), (11, -36, 0, 0), (14, 10, 0, 0), (22, 0, 0, 0), (30, 0, 0, 0)], wings=False)
    a.done()

    # tail_snare (36): tail coils at the side 0-8, lashes far forward at hip height t12, holds, YANKS back t20 (body leans back), recover
    a = NA("tail_snare", 36)
    tailpose(a, [(4, T_LOW, 50, 0), (8, T_COIL, 20, -39), (11, T_OVER, 0, -39), (12, T_SPEAR, 0, -38), (16, T_SPEAR, 0, -38), (18, T_OVER, 0, -39),
                 (20, T_COIL, 0, -39), (22, T_COIL, 0, -39), (28, [-60, -10, -10, 0, 0, 0], 0, -10), (34, T_ZERO, 0, 0), (36, T_ZERO, 0, 0)])
    a.r("chest", (6, 0, 20, 0), (12, -10, -30, 0), (16, -8, -30, 0), (20, 16, 20, 0), (24, 10, 10, 0), (32, 0, 0, 0))
    a.r("head", (6, 0, -10, 0), (12, -6, 30, 0), (20, 6, -10, 0), (30, 0, 0, 0))
    a.r("arm_r", (8, 10, 0, 40), (12, 60, 0, 30), (16, 60, 0, 30), (20, -30, 0, 40), (28, 0, 0, 0))
    a.r("arm_l", (8, 20, 0, -20), (12, 40, 0, -30), (20, 10, 0, -40), (28, 0, 0, 0))
    a.p("body", (8, 0, 0, 0.6), (12, 0, -0.6, -1.4), (16, 0, -0.6, -1.4), (20, 0, -0.4, 1.4), (24, 0, -0.2, 1.0), (32, 0, 0, 0))
    legs(a, [(12, -26, 0, 0), (16, -24, 0, 0), (20, 20, 0, 0), (28, 0, 0, 0)], [(12, 24, 0, 0), (16, 22, 0, 0), (20, -10, 0, 0), (28, 0, 0, 0)],
         sr=[(12, -10, 0, 0), (20, -30, 0, 0), (28, 0, 0, 0)])
    sec(a, [(0, 0, 0, 0), (12, -10, -30, 0), (20, 16, 20, 0), (30, 0, 0, 0)], tail=False)
    a.done()

    # mag_dump (50): brace low 0-10, sweeping full-auto spray 14-38 (torso sweeps right->left, recoil chatter), reload slap 40-46
    a = NA("mag_dump", 50)
    ks = [(6, 70, 0, 0), (10, 90, 0, 6)]
    for t in range(14, 39, 2):
        ks += [(t, 98, 0, 6), (t + 1, 90, 0, 6)]
    ks += [(41, 30, 0, -10), (46, 40, 0, -20), (49, 10, 0, 0)]
    a.r("arm_l", *ks)
    a.r("fore_l", (10, -6, 0, 0), (38, -6, 0, 0), (42, 40, 0, 0), (46, 50, 0, 0), (50, 0, 0, 0))
    a.r("chest", (6, -6, -10, 0), (10, -8, 30, 0), (14, -6, 30, 0), (26, -6, 0, 0), (38, -6, -32, 0), (41, 0, -10, 0), (44, -10, 20, 0), (48, -2, 0, 0))
    a.r("head", (10, 4, -26, 0), (14, 4, -26, 0), (26, 4, 0, 0), (38, 4, 28, 0), (42, 10, 0, 0), (44, 14, 20, 0), (48, 0, 0, 0))
    a.r("arm_r", (6, 40, 0, 20), (10, 70, 0, -20), (38, 70, 0, -20), (42, 50, 30, -40), (44, 70, 40, -60), (45, 60, 40, -50), (49, 0, 0, 0))
    a.r("fore_r", (10, 50, 0, 0), (38, 50, 0, 0), (44, 70, 0, 0), (49, 0, 0, 0))
    a.r("jaw", (14, -20, 0, 0), (38, -24, 0, 0), (42, 0, 0, 0))
    a.r("gun", (40, 0, 0, 0), (44, 0, 0, 0), (45, 0, 0, -10), (46, 0, 0, 0))
    bk = [(4, 0, -1.6, 0.4), (10, 0, -2.2, 0.6)]
    for t in range(14, 39, 4):
        bk += [(t, 0, -2.2, 0.9), (t + 2, 0, -2.2, 0.6)]
    bk += [(42, 0, -1.0, 0.2), (50, 0, 0, 0)]
    a.p("body", *bk)
    legs(a, [(6, 30, 0, 6), (38, 30, 0, 6), (46, 10, 0, 0)], [(6, -24, 0, -8), (38, -24, 0, -8), (46, -6, 0, 0)],
         sr=[(6, -40, 0, 0), (38, -40, 0, 0), (46, -10, 0, 0)], sl=[(6, -30, 0, 0), (38, -30, 0, 0), (46, -10, 0, 0)])
    fl = [(0, *HIDE), (13.7, *HIDE)]
    for t in range(14, 39, 2):
        fl += [(t, 1.3, 1.3, 1.3), (t + 1, 0.6, 0.6, 0.6)]
    fl += [(39.5, *HIDE), (50, *HIDE)]
    a.scl("flash", *fl)
    sec(a, [(0, 0, 0, 0), (10, -4, 30, 0), (16, -4, 24, 4), (22, -4, 10, -4), (28, -4, -6, 4), (34, -4, -20, -4), (38, -4, -30, 0), (44, 0, 10, 0), (50, 0, 0, 0)])
    a.done()

    # bat_swarm (38): wings stretch wide + high 0-10, head thrown back; 4 hard wing beats release bats t14/17/20/23, fold back
    a = NA("bat_swarm", 38)
    wr, wl = [(4, 0, 10, 30), (10, 0, 30, 60)], [(4, 0, -10, -30), (10, 0, -30, -60)]
    for t in (14, 17, 20, 23):
        wr += [(t - 1.5, 0, 40, 70), (t, 0, -40, 10)]
        wl += [(t - 1.5, 0, -40, -70), (t, 0, 40, -10)]
    wr += [(27, 0, 20, 40), (34, 0, 0, 0)]; wl += [(27, 0, -20, -40), (34, 0, 0, 0)]
    a.r("wing_r", *wr); a.r("wing_l", *wl)
    a.r("chest", (6, 14, 0, 0), (10, 20, 0, 0), (14, -10, 0, 0), (17, -6, 0, 0), (20, -10, 0, 0), (23, -12, 0, 0), (28, 0, 0, 0))
    a.r("head", (6, 20, 0, 0), (10, 30, 0, 0), (14, -10, 0, 0), (24, -10, 0, 0), (30, 0, 0, 0))
    a.r("jaw", (10, -10, 0, 0), (14, -40, 0, 0), (24, -38, 0, 0), (28, 0, 0, 0))
    a.r("arm_r", (6, 30, 0, 70), (10, 40, 0, 110), (14, 70, 0, 60), (24, 70, 0, 60), (32, 0, 0, 0))
    a.r("arm_l", (6, 30, 0, -50), (10, 40, 0, -80), (14, 60, 0, -40), (24, 60, 0, -40), (32, 0, 0, 0))
    a.p("body", (10, 0, 0.6, 0.4), (14, 0, 0.2, -0.4), (24, 0, 0.2, -0.4), (32, 0, 0, 0))
    legs(a, [(10, 6, 0, 6), (14, -10, 0, 4), (26, 0, 0, 0)])
    sec(a, [(0, 0, 0, 0), (10, 12, 0, 0), (14, -10, 0, 4), (17, -8, 0, -4), (20, -10, 0, 4), (23, -12, 0, -4), (30, 0, 0, 0), (38, 0, 0, 0)], wings=False)
    a.done()

    # hazard_zone (34): hoists the rifle overhead two-handed 0-10, rams the butt-end into the ground t14 (warning sign planted), holds, wrenches free 24-30
    a = NA("hazard_zone", 34)
    a.r("arm_l", (5, 120, 0, -10), (10, 168, 0, 10), (12, 120, 0, 10), (14, 20, 0, 6), (22, 24, 0, 6), (26, 50, 0, -10), (32, 0, 0, 0))
    a.r("fore_l", (10, 10, 0, 0), (14, 0, 0, 0), (26, 10, 0, 0), (32, 0, 0, 0))
    a.r("arm_r", (5, 110, 0, -40), (10, 160, 0, -30), (12, 120, 0, -30), (14, 30, 0, -40), (22, 34, 0, -40), (26, 60, 0, -20), (32, 0, 0, 0))
    a.r("fore_r", (10, 20, 0, 0), (14, 20, 0, 0), (26, 40, 0, 0), (32, 0, 0, 0))
    a.r("chest", (5, 10, 0, 0), (10, 18, 0, 0), (12, 6, 0, 0), (14, -40, 0, 0), (22, -38, 0, 0), (26, -10, 0, 0), (32, 0, 0, 0))
    a.r("head", (10, -10, 0, 0), (14, 30, 0, 0), (22, 26, 0, 6), (28, 0, 0, 0))
    a.p("body", (5, 0, 0.6, 0), (10, 0, 1.4, 0), (12, 0, 0.8, 0), (14, 0, -3.4, -0.6), (22, 0, -3.2, -0.6), (26, 0, -1.0, 0), (32, 0, 0, 0))
    legs(a, [(10, -4, 0, 4), (14, 50, 0, 8), (22, 50, 0, 8), (28, 0, 0, 0)], [(10, 4, 0, -4), (14, -20, 0, -8), (22, -20, 0, -8), (28, 0, 0, 0)],
         sr=[(14, -70, 0, 0), (22, -70, 0, 0), (28, 0, 0, 0)], sl=[(14, -60, 0, 0), (22, -60, 0, 0), (28, 0, 0, 0)])
    a.s("gun", (13, 1, 1, 1), (14, 1.06, 0.94, 1.06), (15.5, 1, 1, 1))
    sec(a, [(0, 0, 0, 0), (10, 12, 0, 0), (14, -30, 0, 0), (16, -26, 0, 4), (22, -26, 0, 0), (28, 0, 0, 0), (34, 0, 0, 0)])
    a.done()

    # screech (34): deep inhale 0-10 (arches back, arms in), SCREECH t14-26 (jaw wide, arms + wings flung, body trembles), recover
    a = NA("screech", 34)
    a.r("chest", (6, 14, 0, 0), (10, 22, 0, 0), (13, -14, 0, 0), (14, -16, 0, 0), (16, -14, 0, 2), (18, -16, 0, -2), (20, -14, 0, 2), (22, -16, 0, -2), (24, -14, 0, 0), (26, -12, 0, 0), (32, 0, 0, 0))
    a.r("head", (10, 26, 0, 0), (14, -16, 0, 0), (26, -14, 0, 0), (32, 0, 0, 0))
    a.r("jaw", (10, -6, 0, 0), (13, -46, 0, 0), (26, -44, 0, 0), (30, 0, 0, 0))
    for s, k in ((1, "r"), (-1, "l")):
        a.r("arm_" + k, (6, 30, 0, -20 * s), (10, 40, 0, -30 * s), (14, 20, 0, 90 * s), (26, 24, 0, 86 * s), (32, 0, 0, 0))
        a.r("fore_" + k, (10, 80, 0, 0), (14, 10, 0, 0), (28, 10, 0, 0), (32, 0, 0, 0))
        a.r("wing_" + k, (10, 0, 30 * s, -20 * s), (14, 0, -40 * s, 60 * s), (26, 0, -36 * s, 56 * s), (32, 0, 0, 0))
        a.r("ear_" + k, (10, 20, 0, 0), (14, -20, 0, -20 * s), (26, -20, 0, -20 * s), (30, 0, 0, 0))
    a.p("body", (10, 0, -0.8, 0.3), (14, 0, 0.4, 0.6), (26, 0, 0.4, 0.6), (32, 0, 0, 0))
    legs(a, [(10, 6, 0, 0), (14, -6, 0, 8), (26, -6, 0, 8), (32, 0, 0, 0)])
    sec(a, [(0, 0, 0, 0), (10, 16, 0, 0), (14, -20, 0, 0), (18, -20, 0, 6), (22, -20, 0, -6), (26, -16, 0, 0), (34, 0, 0, 0)], wings=False)
    a.done()

    # piercing_round (44): drops to one knee 0-8, long steady aim 8-27 (cheek on the stock), FIRES t28 (huge kick, skids back), rises 34-44
    a = NA("piercing_round", 44)
    a.p("body", (6, 0, -8.8, 0.6), (8, 0, -9.4, 0.6), (27, 0, -9.4, 0.6), (28.5, 0, -9.0, 2.6), (32, 0, -9.2, 2.4), (38, 0, -3.0, 1.0), (44, 0, 0, 0))
    a.r("arm_l", (6, 70, 0, 0), (8, 90, 0, 10), (27, 90, 0, 10), (28.5, 130, 0, 10), (31, 100, 0, 10), (34, 80, 0, 10), (42, 0, 0, 0))
    a.r("fore_l", (8, -4, 0, 0), (27, -4, 0, 0), (42, 0, 0, 0))
    a.r("arm_r", (6, 50, 0, -10), (8, 80, 0, -50), (27, 80, 0, -50), (28.5, 100, 0, -40), (34, 70, 0, -40), (42, 0, 0, 0))
    a.r("fore_r", (8, 30, 0, 0), (34, 30, 0, 0), (42, 0, 0, 0))
    a.r("chest", (6, -8, -20, 0), (8, -6, -30, 0), (27, -6, -30, 0), (28.5, 14, -28, 0), (32, 6, -28, 0), (38, 0, -10, 0))
    a.r("head", (8, 4, 26, -16), (27, 4, 26, -16), (28.5, 20, 26, -10), (34, 4, 20, -10), (42, 0, 0, 0))
    a.r("ear_r", (8, -20, 0, -30), (27, -20, 0, -30), (29, 20, 0, 10), (34, 0, 0, 0))
    a.r("ear_l", (8, -20, 0, 30), (27, -20, 0, 30), (29, 20, 0, -10), (34, 0, 0, 0))
    legs(a, [(6, 80, 0, 4), (34, 80, 0, 4), (40, 14, 0, 0)], [(6, -6, 0, -4), (34, -6, 0, -4), (40, -6, 0, 0)],
         sr=[(6, -84, 0, 0), (34, -84, 0, 0), (40, -16, 0, 0)], sl=[(6, -86, 0, 0), (34, -86, 0, 0), (40, -10, 0, 0)])
    a.scl("flash", (0, *HIDE), (27.7, *HIDE), (28, 2.2, 2.2, 2.2), (29.5, 1.2, 1.2, 1.2), (30.5, *HIDE), (44, *HIDE))
    sec(a, [(0, 0, 0, 0), (8, -6, -20, 0), (27, -6, -20, 0), (29, 20, -20, 0), (34, 4, -10, 0), (44, 0, 0, 0)])
    a.done()

    # transform (130; matured model shows 0-90): rifle arm sparks + jerks 0-30, clutches chest, drops to a knee t40, convulses (40/62/80),
    # arches back with arms + wings flung wide 80-90 -> cyborg model takes over at t90
    a = NA("transform", 130)
    a.r("arm_l", (6, 20, 0, -10), (10, 40, 0, -30), (12, 10, 0, -5), (16, 50, 0, -40), (18, 20, 0, -10), (24, 60, 0, -50), (26, 30, 0, -10), (40, 10, 0, -20), (44, 50, 0, -60), (62, 20, 0, -30), (66, 60, 0, -70), (80, 30, 0, -110), (90, 30, 0, -120), (130, 30, 0, -120))
    a.r("arm_r", (6, 50, -40, -30), (12, 60, -50, -40), (40, 60, -50, -40), (62, 70, -50, -40), (80, 30, 0, 110), (90, 30, 0, 120), (130, 30, 0, 120))
    a.r("fore_r", (12, 60, 0, 0), (62, 60, 0, 0), (80, 10, 0, 0), (130, 10, 0, 0))
    a.r("chest", (6, 10, 0, 0), (12, -10, 0, 0), (20, -16, 8, 0), (30, -20, -8, 0), (40, -30, 0, 0), (42, -36, 0, 6), (44, -28, 0, -6), (62, -34, 0, 0), (64, -42, 6, 0), (66, -30, -6, 0), (76, -20, 0, 0), (80, 26, 0, 0), (90, 34, 0, 0), (130, 34, 0, 0))
    a.r("head", (6, 20, 0, 0), (12, -10, 16, 10), (30, -14, -16, -10), (40, -20, 0, 0), (62, -10, 20, 10), (66, -20, -20, -10), (80, 40, 0, 0), (90, 46, 0, 0), (130, 46, 0, 0))
    a.r("jaw", (38, 0, 0, 0), (40, -30, 0, 0), (44, -10, 0, 0), (62, -34, 0, 0), (66, -10, 0, 0), (80, -44, 0, 0), (130, -44, 0, 0))
    a.p("body", (12, 0, -0.6, 0), (30, 0, -1.4, 0), (40, 0, -9.6, 0), (76, 0, -9.4, 0), (82, 0, -9.0, 0), (90, 0, -9.0, 0), (130, 0, -9.0, 0))
    legs(a, [(30, 10, 0, 0), (40, 80, 0, 4), (130, 80, 0, 4)], [(30, -6, 0, 0), (40, -6, 0, -4), (130, -6, 0, -4)],
         sr=[(30, -14, 0, 0), (40, -84, 0, 0), (130, -84, 0, 0)], sl=[(30, -10, 0, 0), (40, -86, 0, 0), (130, -86, 0, 0)])
    a.r("gun", (8, 0, 0, 0), (9, 0, 0, 8), (10, 0, 0, -6), (11, 0, 0, 0), (22, 0, 0, 0), (23, 0, 0, 10), (24, 0, 0, -8), (25, 0, 0, 0), (60, 0, 0, 0), (62, 0, 0, 12), (63, 0, 0, -10), (64, 0, 0, 0), (130, 0, 0, 0))
    a.s("gun", (40, 1, 1, 1), (80, 1.2, 1.15, 1.2), (90, 1.3, 1.25, 1.3), (130, 1.3, 1.25, 1.3))
    for s, k in ((1, "r"), (-1, "l")):
        a.r("wing_" + k, (40, 0, 20 * s, -10 * s), (62, 0, 10 * s, 20 * s), (80, 0, -40 * s, 70 * s), (130, 0, -40 * s, 70 * s))
        a.r("ear_" + k, (40, -20, 0, 20 * s), (80, 30, 0, -20 * s), (130, 30, 0, -20 * s))
    a.wave(("tail", "tail1", "tail2", "tail3", "tail4", "tail5"), [(0, 0, 0, 0), (20, 20, 30, 0), (30, -10, -30, 0), (40, 20, 20, 0), (62, -20, -30, 0), (66, 20, 30, 0), (80, -40, 0, 0), (130, -40, 0, 0)], 1.2)
    sec(a, [(0, 0, 0, 0), (40, -30, 0, 0), (62, -34, 0, 10), (66, -30, 0, -10), (80, 26, 0, 0), (130, 30, 0, 0)], tail=False, wings=False)
    a.done()

    # death (40): shot-through stagger 0-6, rifle drags him down, knees give 10-18, topples backwards, tail + wings go limp
    a = NA("death", 40)
    a.r("chest", (4, 20, 0, 6), (10, -20, 0, 10), (18, -30, 0, 0), (40, -30, 0, 0))
    a.r("head", (4, 30, 0, 0), (10, -10, 0, 20), (18, 10, 0, 30), (40, 10, 0, 30))
    a.r("jaw", (4, -30, 0, 0), (40, -24, 0, 0))
    a.r("arm_l", (6, 20, 0, -20), (12, -10, 0, 10), (40, -10, 0, 10))
    a.r("arm_r", (4, 30, 0, 60), (12, 40, 0, 30), (24, 120, 0, 40), (40, 130, 0, 50))
    legs(a, [(10, -10, 0, 0), (18, 70, 0, 6), (40, 74, 0, 6)], [(10, 10, 0, 0), (18, 60, 0, -6), (40, 64, 0, -6)], sr=[(18, -100, 0, 0), (40, -100, 0, 0)])
    a.p("root", (10, 0, 0, 0), (18, 0, -8, 0), (28, 0, 1.6, 4), (40, 0, 1.8, 6))
    a.r("root", (18, 0, 0, 0), (28, 74, 0, 0), (32, 86, 0, 0), (36, 82, 0, 0), (40, 84, 0, 0))
    for s, k in ((1, "r"), (-1, "l")):
        a.r("wing_" + k, (10, 0, 20 * s, 20 * s), (28, 0, 0, -40 * s), (40, 0, 0, -50 * s))
    a.wave(("tail", "tail1", "tail2", "tail3", "tail4", "tail5"), [(0, 0, 0, 0), (10, 20, 30, 0), (28, -30, 10, 0), (40, -20, 10, 0)], 2)
    sec(a, [(0, 0, 0, 0), (6, 20, 0, 0), (18, -20, 0, 10), (28, 40, 0, 0), (40, 30, 0, 0)], tail=False, wings=False)
    a.done()


# ================================================================== CYBORG ARMED
def anims_cyborg(m):
    def NA(n, t, loop=False): return A(m, n, t, loop, PROPS)

    # idle (60): upright combat stance, hovering servo bob, tech arm hangs heavy, wings flutter, tail coils
    a = NA("idle", 60, True)
    a.pos("body", (0, 0, 0, 0), (15, 0, 0.35, 0), (30, 0, 0, 0), (45, 0, 0.35, 0), (60, 0, 0, 0))
    a.rot("chest", (0, 2, 0, 0), (30, 0, 2, 0), (60, 2, 0, 0))
    a.rot("head", (0, 0, 0, 0), (12, 0, 8, 4), (18, 0, 8, 4), (20, 0, -4, 0), (40, 0, -6, -3), (60, 0, 0, 0))
    a.rot("arm_l", (0, 4, 0, -6), (30, 6, 0, -7), (60, 4, 0, -6))
    a.rot("fore_l", (0, 10, 0, 0), (30, 14, 0, 0), (60, 10, 0, 0))
    a.rot("arm_r", (0, 0, 0, 6), (30, 4, 0, 8), (60, 0, 0, 6))
    a.rot("fore_r", (0, 16, 0, 0), (30, 20, 0, 0), (60, 16, 0, 0))
    a.rot("hand_r", (0, 0, 0, 0), (36, 0, 0, 0), (38, -20, 0, 0), (40, 0, 0, 0), (60, 0, 0, 0))
    a.rot("leg_r", (0, 0, 0, 3), (60, 0, 0, 3))
    a.rot("leg_l", (0, 0, 0, -3), (60, 0, 0, -3))
    for b, ph, amp in (("tail", 0, (4, 12, 0)), ("tail1", 5, (4, 14, 0)), ("tail2", 10, (6, 16, 0)), ("tail3", 15, (6, 18, 0)), ("tail4", 20, (8, 20, 0)), ("tail5", 25, (8, 22, 0)),
                       ("wing_r", 0, (0, 10, 8)), ("wing_l", 0, (0, -10, -8)), ("hair_r", 8, (2, 0, 3)), ("hair_l", 23, (2, 0, -3)), ("hair_r2", 16, (3, 0, 4)), ("hair_l2", 31, (3, 0, -4)), ("hair_c", 12, (3, 0, 1))):
        a.rot(b, *sinekeys(60, 5, amp, ph))
    a.done()

    # walk (20): heavy mechanical stride, tech arm counter-swings, wings half-open
    a = NA("walk", 20, True)
    a.pos("body", (0, 0, 0, 0), (5, 0, 0.6, 0), (10, 0, 0, 0), (15, 0, 0.6, 0), (20, 0, 0, 0))
    a.rot("body", (0, 0, 5, 0), (10, 0, -5, 0), (20, 0, 5, 0))
    a.rot("chest", (0, -8, -6, 0), (10, -8, 6, 0), (20, -8, -6, 0))
    a.rot("leg_r", (0, 32, 0, 0), (5, 0, 0, 0), (10, -30, 0, 0), (15, 0, 0, 0), (20, 32, 0, 0))
    a.rot("leg_l", (0, -30, 0, 0), (5, 0, 0, 0), (10, 32, 0, 0), (15, 0, 0, 0), (20, -30, 0, 0))
    a.rot("shin_r", (0, 0, 0, 0), (12, -46, 0, 0), (16, -16, 0, 0), (20, 0, 0, 0))
    a.rot("shin_l", (0, 0, 0, 0), (2, -46, 0, 0), (6, -16, 0, 0), (10, 0, 0, 0), (20, 0, 0, 0))
    a.rot("arm_r", (0, -24, 0, 8), (10, 28, 0, 8), (20, -24, 0, 8))
    a.rot("fore_r", (0, 14, 0, 0), (10, 30, 0, 0), (20, 14, 0, 0))
    a.rot("arm_l", (0, 14, 0, -8), (10, -10, 0, -8), (20, 14, 0, -8))
    a.rot("fore_l", (0, 14, 0, 0), (20, 14, 0, 0))
    a.rot("head", (0, 4, -4, 0), (10, 4, 4, 0), (20, 4, -4, 0))
    for b, ph, amp in (("tail", 0, (4, 12, 0)), ("tail1", 2, (4, 14, 0)), ("tail2", 4, (6, 16, 0)), ("tail3", 6, (6, 18, 0)), ("tail4", 8, (8, 18, 0)), ("tail5", 10, (8, 20, 0))):
        a.rot(b, *sinekeys(20, 2, amp, ph))
    for b, base in (("hair_r", (-10, 0, 5)), ("hair_l", (-10, 0, -5)), ("hair_r2", (-8, 0, 5)), ("hair_l2", (-8, 0, -5)), ("hair_c", (-12, 0, 0))):
        a.rot(b, *sinekeys(20, 2, (3, 0, 2), 3, base=base))
    a.rot("wing_r", (0, 0, -10, 10), (5, 0, -4, 18), (10, 0, -10, 10), (15, 0, -4, 18), (20, 0, -10, 10))
    a.rot("wing_l", (0, 0, 10, -10), (5, 0, 4, -18), (10, 0, 10, -10), (15, 0, 4, -18), (20, 0, 10, -10))
    a.done()

    # cannon_shot (34): cannon swung up 0-9, charge shudder 10-15 (arm swells), BOOM t16 (arm kicks up, body thrown back), recover
    a = NA("cannon_shot", 34)
    a.r("arm_l", (6, 60, 0, -6), (9, 94, 0, 4), (12, 90, 0, 4), (13, 91, 0, 3), (14, 89, 0, 5), (15, 90, 0, 4), (16, 132, 0, 4), (19, 110, 0, 4), (24, 90, 0, 4), (31, 10, 0, 0))
    a.r("fore_l", (9, -6, 0, 0), (16, -10, 0, 0), (24, -6, 0, 0), (32, 0, 0, 0))
    a.s("gun", (10, 1, 1, 1), (15, 1.12, 1.08, 1.12), (16, 0.92, 1.1, 0.92), (18, 1.04, 1, 1.04), (21, 1, 1, 1))
    a.r("chest", (6, 0, -20, 0), (9, 0, -30, 0), (15, -4, -30, 0), (16, 20, -26, 0), (19, 12, -28, 0), (26, 0, -10, 0))
    a.r("head", (9, -4, 26, -6), (16, 16, 24, -6), (22, 0, 24, -6), (30, 0, 0, 0))
    a.r("arm_r", (6, 20, 0, 40), (9, 30, 0, 50), (16, -20, 0, 70), (22, 20, 0, 40), (30, 0, 0, 0))
    a.p("body", (9, 0, -0.8, 0), (15, 0, -1.0, -0.2), (16, 0, -0.4, 2.8), (19, 0, -0.6, 2.4), (26, 0, -0.2, 0.8), (32, 0, 0, 0))
    legs(a, [(9, 20, 0, 4), (16, 30, 0, 4), (24, 20, 0, 4), (32, 0, 0, 0)], [(9, -20, 0, -6), (16, -28, 0, -6), (24, -20, 0, -6), (32, 0, 0, 0)],
         sr=[(9, -16, 0, 0), (16, -30, 0, 0), (26, 0, 0, 0)], sl=[(9, -20, 0, 0), (16, -10, 0, 0), (26, 0, 0, 0)])
    flashes(a, (16,), 2.0)
    sec(a, [(0, 0, 0, 0), (9, 0, -20, 0), (16, 22, -20, 0), (22, 6, -14, 0), (34, 0, 0, 0)])
    a.done()

    # gatling (54): arm locks forward 0-8, barrel spin-up 8-12, roaring stream 12-42 (chatter + walking sweep), steam vent cool-down 44-54
    a = NA("gatling", 54)
    ks = [(6, 70, 0, 0), (8, 90, 0, 4), (12, 90, 0, 4)]
    for t in range(12, 43, 2):
        ks += [(t, 95, 0, 4), (t + 1, 89, 0, 4)]
    ks += [(46, 60, 0, 0), (52, 0, 0, 0)]
    a.r("arm_l", *ks)
    rk = [(8, 0, 0, 0)]
    for t in range(8, 44, 1):
        rk.append((t, 0, (t - 8) * 40, 0))
    a.rot("gun", (0, 0, 0, 0), *rk[1:], (54, 0, 36 * 40, 0))
    a.r("chest", (8, -4, -26, 0), (12, -4, -24, 0), (22, -4, -6, 0), (32, -4, -34, 0), (42, -4, -20, 0), (48, 0, -6, 0))
    a.r("head", (8, 0, 24, 0), (22, 0, 8, 0), (32, 0, 30, 0), (42, 0, 20, 0), (50, 0, 0, 0))
    a.r("arm_r", (8, 50, 0, -30), (42, 50, 0, -30), (50, 0, 0, 0))
    a.r("fore_r", (8, 60, 0, 0), (42, 60, 0, 0), (50, 0, 0, 0))
    bk = [(8, 0, -1.4, 0)]
    for t in range(12, 43, 3):
        bk += [(t, 0, -1.4, 0.7), (t + 1.5, 0, -1.5, 0.4)]
    bk += [(46, 0, -0.6, 0), (54, 0, 0, 0)]
    a.p("body", *bk)
    legs(a, [(8, 24, 0, 6), (42, 24, 0, 6), (50, 0, 0, 0)], [(8, -24, 0, -8), (42, -24, 0, -8), (50, 0, 0, 0)],
         sr=[(8, -26, 0, 0), (42, -26, 0, 0), (50, 0, 0, 0)], sl=[(8, -26, 0, 0), (42, -26, 0, 0), (50, 0, 0, 0)])
    fl = [(0, *HIDE), (11.7, *HIDE)]
    for t in range(12, 43, 2):
        fl += [(t, 1.25, 1.25, 1.25), (t + 1, 0.7, 0.7, 0.7)]
    fl += [(43.5, *HIDE), (54, *HIDE)]
    a.scl("flash", *fl)
    sec(a, [(0, 0, 0, 0), (8, -2, -20, 0), (16, -2, -10, 4), (24, -2, -6, -4), (32, -2, -30, 4), (42, -2, -20, 0), (54, 0, 0, 0)])
    a.done()

    # rocket_salvo (46): drops to a knee, cannon angled to the sky 0-10, six launches t14..29 (kick each), rises 36-46
    a = NA("rocket_salvo", 46)
    sh = (14, 17, 20, 23, 26, 29)
    ks = [(6, 100, 0, -10), (10, 140, 0, -14)]
    for t in sh:
        ks += [(t, 140, 0, -14), (t + 0.8, 156, 0, -14), (t + 2, 142, 0, -14)]
    ks += [(34, 120, 0, -10), (42, 0, 0, 0)]
    a.r("arm_l", *ks)
    a.r("chest", (6, 4, -16, 0), (10, 10, -20, 0), *[(t + 0.8, 16, -20 + (i % 2) * 6, 0) for i, t in enumerate(sh)], (32, 10, -16, 0), (40, 0, 0, 0))
    a.r("head", (10, 20, 16, 0), (30, 20, 16, 0), (40, 0, 0, 0))
    a.r("arm_r", (6, 20, 0, 40), (10, 30, 0, 60), (30, 30, 0, 60), (40, 0, 0, 0))
    a.p("body", (6, 0, -8.8, 0.6), (10, 0, -9.4, 0.6), *[(t + 0.8, 0, -9.8, 0.9) for t in sh], (32, 0, -9.4, 0.6), (40, 0, -2, 0), (46, 0, 0, 0))
    legs(a, [(6, 80, 0, 4), (32, 80, 0, 4), (40, 14, 0, 0)], [(6, -6, 0, -4), (32, -6, 0, -4), (40, -6, 0, 0)],
         sr=[(6, -84, 0, 0), (32, -84, 0, 0), (40, -16, 0, 0)], sl=[(6, -86, 0, 0), (32, -86, 0, 0), (40, -10, 0, 0)])
    flashes(a, sh, 1.6)
    a.r("wing_r", (10, 0, 10, 40), (30, 0, 10, 40), (40, 0, 0, 0))
    a.r("wing_l", (10, 0, -10, -40), (30, 0, -10, -40), (40, 0, 0, 0))
    sec(a, [(0, 0, 0, 0), (10, 10, -10, 0), *[(t + 0.8, 16, -10, 4 * (1 if i % 2 else -1)) for i, t in enumerate(sh)], (36, 4, 0, 0), (46, 0, 0, 0)], wings=False)
    a.done()

    # tail_pierce (32): tail rears up over the shoulder 0-9, spears forward t12, snaps back 14-17, second spear t20, coils home
    a = NA("tail_pierce", 32)
    tailpose(a, [(4, [-60, -20, 0, 0, 0, 0], 10, -12), (9, T_COIL, 0, -39), (11, T_OVER, 0, -39), (12, T_SPEAR, 0, -38), (14, T_SPEAR, 0, -38), (16, T_OVER, 0, -39),
                 (17, T_COIL, 0, -39), (19, T_OVER, 0, -39), (20, T_SPEAR, 0, -38), (22, T_SPEAR, 0, -38), (25, T_COIL, 0, -20), (30, T_ZERO, 0, 0), (32, T_ZERO, 0, 0)])
    a.r("chest", (6, 10, 0, 0), (9, 14, 0, 0), (12, -16, 0, 0), (16, 6, 0, 0), (20, -18, 6, 0), (24, -6, 0, 0), (30, 0, 0, 0))
    a.r("head", (9, -6, 0, 0), (12, 10, 0, 0), (20, 12, 0, 0), (28, 0, 0, 0))
    a.r("arm_r", (6, -10, 0, 30), (12, 30, 0, 20), (20, 30, 0, 24), (28, 0, 0, 0))
    a.r("arm_l", (6, -10, 0, -20), (12, 20, 0, -14), (20, 20, 0, -20), (28, 0, 0, 0))
    a.p("body", (9, 0, 0.4, 0.6), (12, 0, -0.6, -1.0), (16, 0, 0, 0.2), (20, 0, -0.6, -1.2), (28, 0, 0, 0))
    legs(a, [(9, -6, 0, 0), (12, -20, 0, 0), (16, -4, 0, 0), (20, -22, 0, 0), (28, 0, 0, 0)], [(9, 8, 0, 0), (12, 20, 0, 0), (20, 20, 0, 0), (28, 0, 0, 0)],
         sl=[(12, -20, 0, 0), (20, -20, 0, 0), (28, 0, 0, 0)])
    sec(a, [(0, 0, 0, 0), (9, 10, 0, 0), (12, -16, 0, 0), (16, 6, 0, 0), (20, -18, 0, 0), (30, 0, 0, 0)], tail=False)
    a.done()

    # tail_spin (32): crouch + wind 0-9, full 360 spin 10-18 with tail stretched flat (hit t14), skid + recover
    a = NA("tail_spin", 32)
    a.rot("root", (0, 0, 0, 0), (6, 0, 30, 0), (9, 0, 40, 0), (11, 0, -20, 0), (13, 0, -110, 0), (15, 0, -200, 0), (17, 0, -290, 0), (19, 0, -350, 0), (22, 0, -366, 0), (26, 0, -360, 0), (32, 0, -360, 0))
    tailk(a, [(6, 30, 40, 0), (9, 20, 60, 0), (11, -50, -10, 0), (14, -56, -20, 0), (18, -50, -10, 0), (21, 0, 20, 0), (28, 0, 0, 0)],
          scale=(1, -0.3, 0.4, 0.5, 0.5, 0.4), delay=0.6)
    a.p("body", (6, 0, -2.0, 0), (9, 0, -2.4, 0), (14, 0, -1.6, 0), (19, 0, -2.2, 0), (24, 0, -0.8, 0), (30, 0, 0, 0))
    a.r("chest", (6, -14, 30, 0), (9, -16, 34, 0), (14, -10, -14, 0), (19, -14, -20, 0), (24, -4, 0, 0))
    for s, k in ((1, "r"), (-1, "l")):
        a.r("arm_" + k, (9, 20, 0, 30 * s), (14, 20, 0, 80 * s), (19, 20, 0, 60 * s), (26, 0, 0, 0))
        a.r("wing_" + k, (9, 0, 20 * s, 0), (14, 0, -30 * s, 40 * s), (19, 0, -20 * s, 30 * s), (26, 0, 0, 0))
    legs(a, [(6, 30, 0, 10), (19, 30, 0, 14), (26, 0, 0, 0)], [(6, -10, 0, -10), (19, -10, 0, -14), (26, 0, 0, 0)],
         sr=[(6, -50, 0, 0), (19, -50, 0, 0), (26, 0, 0, 0)], sl=[(6, -30, 0, 0), (19, -30, 0, 0), (26, 0, 0, 0)])
    sec(a, [(0, 0, 0, 0), (9, -10, 30, 0), (14, -10, -40, 20), (19, -10, -30, 10), (24, 0, -10, 0), (32, 0, 0, 0)], tail=False, wings=False)
    a.done()

    # tech_smash (38): hoists the tech arm high, rising onto the toes 0-12, hangs 12-15, SLAMS t18 (deep crouch, arm buried), wrench out 26-38
    a = NA("tech_smash", 38)
    a.r("arm_l", (6, 120, 0, -10), (12, 176, 0, 4), (15, 180, 0, 6), (17, 110, 0, 6), (18, 40, 0, 4), (24, 36, 0, 4), (28, 60, 0, -10), (36, 0, 0, 0))
    a.r("fore_l", (12, 30, 0, 0), (17, 0, 0, 0), (26, 0, 0, 0), (36, 0, 0, 0))
    a.r("chest", (6, 10, -10, 0), (12, 18, -16, 0), (15, 20, -16, 0), (18, -40, 10, 0), (24, -38, 10, 0), (30, -10, 0, 0), (36, 0, 0, 0))
    a.r("head", (12, -16, 10, 0), (18, 26, 0, 0), (24, 22, 0, 0), (32, 0, 0, 0))
    a.r("arm_r", (6, -20, 0, 40), (12, -30, 0, 60), (18, 40, 0, 30), (24, 40, 0, 30), (32, 0, 0, 0))
    a.p("body", (6, 0, 0.8, 0.4), (12, 0, 1.6, 0.6), (15, 0, 1.8, 0.6), (18, 0, -4.0, -1.0), (24, 0, -3.8, -1.0), (30, 0, -1.0, 0), (36, 0, 0, 0))
    legs(a, [(12, -6, 0, 4), (18, 56, 0, 8), (24, 56, 0, 8), (32, 0, 0, 0)], [(12, 6, 0, -4), (18, -22, 0, -8), (24, -22, 0, -8), (32, 0, 0, 0)],
         sr=[(12, 10, 0, 0), (18, -80, 0, 0), (24, -80, 0, 0), (32, 0, 0, 0)], sl=[(18, -60, 0, 0), (24, -60, 0, 0), (32, 0, 0, 0)])
    a.s("gun", (17, 1, 1, 1), (18, 1.1, 0.92, 1.1), (20, 1, 1, 1))
    a.r("wing_r", (12, 0, 20, 50), (18, 0, -20, -10), (24, 0, -20, -10), (32, 0, 0, 0))
    a.r("wing_l", (12, 0, -20, -50), (18, 0, 20, 10), (24, 0, 20, 10), (32, 0, 0, 0))
    sec(a, [(0, 0, 0, 0), (12, 16, -10, 0), (18, -36, 10, 0), (22, -30, 10, 6), (30, 0, 0, 0), (38, 0, 0, 0)], wings=False)
    a.done()

    # jet_dash (34): wings cocked back, crouch 0-6, thrust t8 (flat dash), tech-arm jab t12, plants and UPPERCUTS t20 (rising), lands 24-34
    a = NA("jet_dash", 34)
    a.p("body", (5, 0, -2.0, 1.0), (8, 0, -1.4, -2.0), (12, 0, -1.2, -3.0), (16, 0, -2.4, -2.0), (20, 0, 2.0, -1.4), (23, 0, 1.4, -0.6), (28, 0, 0, 0))
    a.r("chest", (5, -26, 0, 0), (8, -44, -10, 0), (12, -30, -30, 0), (16, -26, 10, 0), (20, 16, -20, 0), (24, 6, -10, 0), (30, 0, 0, 0))
    a.r("head", (8, 30, 0, 0), (12, 20, 20, 0), (20, -10, 10, 0), (28, 0, 0, 0))
    a.r("arm_l", (5, -30, 0, -20), (8, -50, 0, -10), (11, 80, 0, 0), (12, 96, 0, 6), (14, 80, 0, 0), (17, 10, 0, -20), (20, 172, 0, 10), (22, 160, 0, 10), (28, 40, 0, 0), (33, 0, 0, 0))
    a.r("fore_l", (8, 40, 0, 0), (12, 0, 0, 0), (17, 60, 0, 0), (20, 0, 0, 0), (30, 0, 0, 0))
    a.r("arm_r", (5, -40, 0, 20), (8, -60, 0, 10), (12, -40, 0, 30), (20, -30, 0, 40), (28, 0, 0, 0))
    a.r("wing_r", (4, 0, 40, -20), (8, 0, 60, -40), (14, 0, 50, -30), (20, 0, -30, 50), (24, 0, -10, 30), (30, 0, 0, 0))
    a.r("wing_l", (4, 0, -40, 20), (8, 0, -60, 40), (14, 0, -50, 30), (20, 0, 30, -50), (24, 0, 10, -30), (30, 0, 0, 0))
    legs(a, [(5, 40, 0, 0), (8, -10, 0, 0), (12, 20, 0, 0), (16, 40, 0, 0), (20, -10, 0, 0), (26, 0, 0, 0)], [(5, 20, 0, 0), (8, -60, 0, 0), (12, -50, 0, 0), (16, -20, 0, 0), (20, 10, 0, 0), (26, 0, 0, 0)],
         sr=[(5, -60, 0, 0), (8, -20, 0, 0), (16, -50, 0, 0), (20, -10, 0, 0), (26, 0, 0, 0)], sl=[(5, -50, 0, 0), (8, -50, 0, 0), (16, -30, 0, 0), (20, -30, 0, 0), (26, 0, 0, 0)])
    sec(a, [(0, 0, 0, 0), (5, -10, 0, 0), (8, -40, 0, 0), (12, -30, 0, 0), (16, -20, 0, 0), (20, 20, 0, 0), (28, 0, 0, 0), (34, 0, 0, 0)], wings=False)
    a.done()

    # goggle_laser (62): hovers up, head bows while goggles charge 0-28 (arms spread, shaking), head snaps up t30, beam sweeps 30-52, cools
    a = NA("goggle_laser", 62)
    a.p("body", (10, 0, 1.4, 0), (28, 0, 1.8, 0), (30, 0, 1.6, 0.6), (52, 0, 1.6, 0.6), (58, 0, 0.4, 0), (62, 0, 0, 0))
    a.r("head", (8, 26, 0, 0), (20, 30, 0, 0), (22, 28, 2, 0), (24, 30, -2, 0), (26, 28, 2, 0), (28, 30, 0, 0), (30, -12, 0, 0), (32, -6, 0, 0), (52, -6, 0, 0), (58, 0, 0, 0))
    a.r("chest", (10, 6, 0, 0), (28, 10, 0, 0), (30, -6, 0, 0), (36, -6, 14, 0), (44, -6, -14, 0), (52, -6, 0, 0), (58, 0, 0, 0))
    for s, k in ((1, "r"), (-1, "l")):
        a.r("arm_" + k, (10, 10, 0, 50 * s), (28, 10, 0, 60 * s), (30, 20, 0, 40 * s), (52, 20, 0, 40 * s), (58, 0, 0, 0))
        a.r("wing_" + k, (10, 0, -20 * s, 50 * s), (28, 0, -30 * s, 60 * s), (30, 0, -10 * s, 30 * s), (52, 0, -10 * s, 30 * s), (58, 0, 0, 0))
        a.r("ear_" + k, (10, -20, 0, -10 * s), (30, 20, 0, 0), (52, 20, 0, 0), (56, 0, 0, 0))
    a.s("head", (26, 1, 1, 1), (29, 1.06, 1.06, 1.06), (31, 1, 1, 1))
    legs(a, [(10, 10, 0, 6), (52, 10, 0, 6), (58, 0, 0, 0)], [(10, -6, 0, -6), (52, -6, 0, -6), (58, 0, 0, 0)], sr=[(10, -30, 0, 0), (52, -30, 0, 0), (58, 0, 0, 0)])
    sec(a, [(0, 0, 0, 0), (10, 6, 0, 0), (28, 10, 0, 6), (30, -10, 0, 0), (36, -6, 14, 0), (44, -6, -14, 0), (52, -6, 0, 0), (62, 0, 0, 0)], wings=False)
    a.done()

    # emp_pulse (36): curls up, arms crossed over the glowing plates 0-12 (chest swells), BURSTS t16 (arms + wings flung wide), recover
    a = NA("emp_pulse", 36)
    a.r("arm_r", (6, 60, 0, -40), (12, 80, 0, -60), (15, 80, 0, -62), (16, 30, 0, 100), (24, 30, 0, 96), (32, 0, 0, 0))
    a.r("arm_l", (6, 60, 0, 40), (12, 80, 0, 56), (15, 80, 0, 58), (16, 30, 0, -96), (24, 30, 0, -92), (32, 0, 0, 0))
    a.r("fore_r", (12, 90, 0, 0), (16, 0, 0, 0), (28, 0, 0, 0))
    a.r("fore_l", (12, 60, 0, 0), (16, 0, 0, 0), (28, 0, 0, 0))
    a.r("chest", (6, -14, 0, 0), (12, -26, 0, 0), (13, -24, 0, 2), (14, -26, 0, -2), (15, -24, 0, 0), (16, 18, 0, 0), (24, 14, 0, 0), (32, 0, 0, 0))
    a.s("chest", (10, 1, 1, 1), (15, 1.05, 1.03, 1.08), (16, 1.08, 1.06, 1.1), (19, 1, 1, 1))
    a.r("head", (12, 30, 0, 0), (16, -20, 0, 0), (24, -16, 0, 0), (32, 0, 0, 0))
    a.p("body", (12, 0, -2.4, 0), (16, 0, 1.0, 0), (24, 0, 0.6, 0), (32, 0, 0, 0))
    for s, k in ((1, "r"), (-1, "l")):
        a.r("wing_" + k, (12, 0, 40 * s, -30 * s), (16, 0, -40 * s, 70 * s), (24, 0, -36 * s, 64 * s), (32, 0, 0, 0))
    legs(a, [(12, 40, 0, 4), (16, -4, 0, 12), (24, -4, 0, 10), (32, 0, 0, 0)], sr=[(12, -70, 0, 0), (16, 0, 0, 0)])
    sec(a, [(0, 0, 0, 0), (12, -20, 0, 0), (16, 20, 0, 0), (20, 16, 0, 6), (24, 14, 0, -6), (36, 0, 0, 0)], wings=False)
    a.done()

    # grenade_lob (36): cannon tilted up as a mortar 0-8, three thumps t12/16/20 (arm bucks, knees absorb), lowers
    a = NA("grenade_lob", 36)
    sh = (12, 16, 20)
    ks = [(6, 110, 0, -6), (9, 130, 0, -8)]
    for t in sh:
        ks += [(t, 130, 0, -8), (t + 1, 150, 0, -8), (t + 3, 132, 0, -8)]
    ks += [(26, 110, 0, -6), (33, 0, 0, 0)]
    a.r("arm_l", *ks)
    a.r("chest", (6, 4, -14, 0), (9, 8, -18, 0), *[(t + 1, 16, -18, 0) for t in sh], *[(t + 3, 8, -18, 0) for t in sh], (28, 0, -6, 0))
    a.r("head", (9, 16, 16, 0), (24, 16, 16, 0), (32, 0, 0, 0))
    a.r("arm_r", (9, 10, 0, 50), (24, 10, 0, 50), (32, 0, 0, 0))
    a.p("body", (9, 0, -1.0, 0), *[(t + 1, 0, -1.8, 0.5) for t in sh], *[(t + 3, 0, -1.1, 0.2) for t in sh], (30, 0, 0, 0))
    legs(a, [(9, 20, 0, 6), (24, 20, 0, 6), (32, 0, 0, 0)], [(9, -20, 0, -6), (24, -20, 0, -6), (32, 0, 0, 0)],
         sr=[(9, -30, 0, 0), (24, -30, 0, 0), (32, 0, 0, 0)], sl=[(9, -26, 0, 0), (24, -26, 0, 0), (32, 0, 0, 0)])
    flashes(a, sh, 1.5)
    sec(a, [(0, 0, 0, 0), (9, 6, -14, 0), (13, 14, -14, 4), (17, 14, -14, -4), (21, 14, -14, 4), (28, 0, 0, 0), (36, 0, 0, 0)])
    a.done()

    # hazard_strike (44): small hop 0-7, PUNCHES the ground t10 (warning sigils spread), braces kneeling while they detonate 24-30, rises
    a = NA("hazard_strike", 44)
    a.p("body", (4, 0, -1.6, 0), (7, 0, 1.6, -0.6), (10, 0, -4.4, -1.0), (22, 0, -4.2, -1.0), (24, 0, -4.6, -1.0), (27, 0, -4.0, -1.0), (30, 0, -4.4, -1.0), (36, 0, -1.4, 0), (44, 0, 0, 0))
    a.r("arm_l", (4, 60, 0, -20), (7, 150, 0, 0), (9, 90, 0, 0), (10, 20, 0, 6), (30, 20, 0, 6), (36, 30, 0, -10), (42, 0, 0, 0))
    a.r("chest", (4, -10, 0, 0), (7, 14, -10, 0), (10, -42, 6, 0), (30, -38, 6, 0), (36, -10, 0, 0), (42, 0, 0, 0))
    a.r("head", (7, -10, 0, 0), (10, 30, 0, 0), (24, 20, 10, 0), (28, 20, -10, 0), (36, 0, 0, 0))
    a.r("arm_r", (7, -30, 0, 50), (10, 30, 0, 50), (30, 30, 0, 50), (40, 0, 0, 0))
    a.s("gun", (9, 1, 1, 1), (10, 1.12, 0.9, 1.12), (12, 1, 1, 1))
    legs(a, [(4, 30, 0, 0), (7, -10, 0, 0), (10, 50, 0, 10), (30, 50, 0, 10), (38, 0, 0, 0)], [(4, 20, 0, 0), (7, 10, 0, 0), (10, -30, 0, -10), (30, -30, 0, -10), (38, 0, 0, 0)],
         sr=[(4, -50, 0, 0), (7, -20, 0, 0), (10, -70, 0, 0), (30, -70, 0, 0), (38, 0, 0, 0)], sl=[(4, -40, 0, 0), (10, -70, 0, 0), (30, -70, 0, 0), (38, 0, 0, 0)])
    a.r("wing_r", (7, 0, -20, 60), (10, 0, 30, -20), (30, 0, 30, -20), (38, 0, 0, 0))
    a.r("wing_l", (7, 0, 20, -60), (10, 0, -30, 20), (30, 0, -30, 20), (38, 0, 0, 0))
    sec(a, [(0, 0, 0, 0), (7, 12, 0, 0), (10, -36, 0, 0), (24, -30, 0, 8), (28, -30, 0, -8), (36, 0, 0, 0), (44, 0, 0, 0)], wings=False)
    a.done()

    # overdrive (80, ENRAGED): overload charge 0-30 (hunched, trembling, chest swelling), rocket ring burst t34 (arms + wings wide),
    # spinning gatling sweep 40-60 (full turn), leaps and double-slams the ground t66, smoking recovery
    a = NA("overdrive", 80)
    a.s("chest", (0, 1, 1, 1), (30, 1.1, 1.06, 1.12), (34, 1, 1, 1))
    ch = [(4, -20, 0, 0)] + [(t, -24 + (t % 4) * 1.5, 0, 3 if t % 4 else -3) for t in range(6, 31, 2)] + [(34, 20, 0, 0), (40, -4, 0, 0), (60, -4, 0, 0), (62, 14, 0, 0), (64, 18, 0, 0), (66, -44, 0, 0), (72, -40, 0, 0), (78, 0, 0, 0)]
    a.r("chest", *ch)
    a.rot("root", (0, 0, 0, 0), (40, 0, 0, 0), (45, 0, -90, 0), (50, 0, -180, 0), (55, 0, -270, 0), (60, 0, -360, 0), (80, 0, -360, 0))
    a.r("head", (4, 26, 0, 0), (30, 30, 0, 0), (34, -20, 0, 0), (40, 0, 0, 0), (62, -10, 0, 0), (66, 30, 0, 0), (74, 20, 0, 0), (80, 0, 0, 0))
    a.r("arm_l", (4, 40, 0, 30), (30, 50, 0, 40), (34, 40, 0, -100), (38, 70, 0, -20), (40, 90, 0, 0), *[(t, 92 + (t % 2) * 4, 0, 0) for t in range(41, 60)], (62, 170, 0, 0), (64, 176, 0, 0), (66, 30, 0, 0), (72, 30, 0, 0), (78, 0, 0, 0))
    a.r("arm_r", (4, 40, 0, -30), (30, 50, 0, -40), (34, 40, 0, 100), (38, 30, 0, 40), (60, 30, 0, 40), (62, 170, 0, 0), (64, 176, 0, 0), (66, 30, 0, 0), (72, 30, 0, 0), (78, 0, 0, 0))
    a.p("body", (4, 0, -2.0, 0), (30, 0, -2.6, 0), (34, 0, 1.0, 0), (40, 0, -1.2, 0), (60, 0, -1.2, 0), (63, 0, 3.4, 0), (66, 0, -4.6, -1.0), (72, 0, -4.4, -1.0), (78, 0, -0.6, 0), (80, 0, 0, 0))
    legs(a, [(4, 30, 0, 4), (30, 34, 0, 4), (34, -4, 0, 12), (40, 20, 0, 6), (60, 20, 0, 6), (63, -10, 0, 0), (66, 54, 0, 8), (72, 54, 0, 8), (78, 0, 0, 0)],
         [(4, -10, 0, -4), (30, -12, 0, -4), (34, -4, 0, -12), (40, -20, 0, -6), (60, -20, 0, -6), (63, 10, 0, 0), (66, -24, 0, -8), (72, -24, 0, -8), (78, 0, 0, 0)],
         sr=[(4, -60, 0, 0), (30, -66, 0, 0), (34, 0, 0, 0), (40, -26, 0, 0), (60, -26, 0, 0), (63, -10, 0, 0), (66, -80, 0, 0), (72, -80, 0, 0), (78, 0, 0, 0)],
         sl=[(4, -30, 0, 0), (30, -30, 0, 0), (34, 0, 0, 0), (40, -26, 0, 0), (60, -26, 0, 0), (66, -60, 0, 0), (72, -60, 0, 0), (78, 0, 0, 0)])
    for s, k in ((1, "r"), (-1, "l")):
        a.r("wing_" + k, (4, 0, 30 * s, -20 * s), (30, 0, 36 * s, -30 * s), (34, 0, -40 * s, 80 * s), (40, 0, -20 * s, 40 * s), (60, 0, -20 * s, 40 * s), (63, 0, -40 * s, 70 * s), (66, 0, 30 * s, -20 * s), (74, 0, 0, 0))
    a.r("gun", (38, 0, 0, 0), *[(t, 0, (t - 38) * 45, 0) for t in range(39, 61)], (62, 0, 1080, 0), (80, 0, 1080, 0))
    fl = [(0, *HIDE), (33.7, *HIDE), (34, 1.8, 1.8, 1.8), (35.5, *HIDE), (40.7, *HIDE)]
    for t in range(41, 60, 2):
        fl += [(t, 1.2, 1.2, 1.2), (t + 1, 0.6, 0.6, 0.6)]
    fl += [(60.5, *HIDE), (80, *HIDE)]
    a.scl("flash", *fl)
    sec(a, [(0, 0, 0, 0), (4, -20, 0, 0), (16, -22, 0, 6), (24, -22, 0, -6), (30, -24, 0, 0), (34, 20, 0, 0), (40, -4, -30, 0), (60, -4, -30, 0), (63, 16, 0, 0), (66, -40, 0, 0), (74, -20, 0, 0), (80, 0, 0, 0)], wings=False)
    a.done()

    # transform (130; cyborg model shows 90-130): kneeling hunched at t90, unfolds and rises 90-104, goggles flare, wings snap open,
    # deep inhale 104-110, ROAR t112 (arms + tech arm flung wide), settles into the combat stance
    a = NA("transform", 130)
    a.p("body", (90, 0, -9.0, 0), (96, 0, -6.0, 0), (104, 0, 0.4, 0), (108, 0, 0.2, 0), (112, 0, 0.8, 0), (120, 0, 0.6, 0), (130, 0, 0, 0))
    a.r("chest", (90, -40, 0, 0), (96, -30, 0, 0), (104, 0, 0, 0), (108, 14, 0, 0), (112, -14, 0, 0), (114, -12, 0, 2), (116, -14, 0, -2), (120, -6, 0, 0), (130, 0, 0, 0))
    a.r("head", (90, 30, 0, 0), (100, 20, 0, 0), (104, -10, 0, 0), (108, 20, 0, 0), (112, -24, 0, 0), (120, -14, 0, 0), (130, 0, 0, 0))
    a.r("jaw", (108, 0, 0, 0), (112, -40, 0, 0), (120, -36, 0, 0), (126, 0, 0, 0))
    a.r("arm_r", (90, 40, 0, -20), (100, 30, 0, 30), (108, 40, 0, -20), (112, 30, 0, 110), (120, 30, 0, 100), (130, 0, 0, 0))
    a.r("arm_l", (90, 30, 0, 20), (100, 40, 0, -30), (108, 50, 0, 20), (112, 40, 0, -100), (120, 40, 0, -90), (130, 0, 0, 0))
    a.r("fore_r", (108, 80, 0, 0), (112, 10, 0, 0), (130, 0, 0, 0))
    a.s("gun", (90, 0.7, 0.75, 0.7), (98, 0.9, 0.9, 0.9), (104, 1.08, 1.06, 1.08), (108, 1, 1, 1), (112, 1.1, 1.05, 1.1), (116, 1, 1, 1))
    legs(a, [(90, 80, 0, 4), (96, 60, 0, 4), (104, 0, 0, 6), (112, -4, 0, 12), (120, -4, 0, 10), (130, 0, 0, 0)],
         [(90, -6, 0, -4), (96, -6, 0, -4), (104, 0, 0, -6), (112, 4, 0, -12), (120, 4, 0, -10), (130, 0, 0, 0)],
         sr=[(90, -84, 0, 0), (96, -60, 0, 0), (104, 0, 0, 0)], sl=[(90, -86, 0, 0), (96, -70, 0, 0), (104, 0, 0, 0)])
    for s, k in ((1, "r"), (-1, "l")):
        a.r("wing_" + k, (90, 0, 40 * s, -40 * s), (100, 0, 30 * s, -20 * s), (104, 0, -40 * s, 70 * s), (108, 0, -10 * s, 20 * s), (112, 0, -50 * s, 80 * s), (120, 0, -40 * s, 70 * s), (130, 0, 0, 0))
        a.r("ear_" + k, (90, -30, 0, 30 * s), (104, 10, 0, -10 * s), (112, 20, 0, -20 * s), (124, 0, 0, 0))
    a.wave(("tail", "tail1", "tail2", "tail3", "tail4", "tail5"), [(0, 0, 0, 0), (90, 30, 30, 0), (104, -30, -20, 0), (112, -50, 0, 0), (120, -30, 10, 0), (130, 0, 0, 0)], 1.2)
    sec(a, [(0, 0, 0, 0), (90, -40, 0, 0), (104, 10, 0, 0), (108, 14, 0, 0), (112, -20, 0, 0), (120, -6, 0, 0), (130, 0, 0, 0)], tail=False, wings=False)
    a.done()

    # death (40): systems fail - jolting sparks 0-10, tech arm drops dead, knees buckle, slumps forward onto the cannon
    a = NA("death", 40)
    a.r("chest", (2, 10, 0, 6), (4, -6, 0, -6), (6, 10, 0, 6), (8, -4, 0, -4), (12, 20, 0, 0), (20, -30, 0, 0), (40, -40, 0, 0))
    a.r("head", (2, -20, 10, 0), (4, 10, -10, 0), (6, -16, 10, 0), (12, 30, 0, 0), (24, 40, 0, 20), (40, 40, 0, 20))
    a.r("arm_l", (6, 20, 0, -20), (12, 0, 0, 0), (40, 0, 0, 0))
    a.r("arm_r", (6, 30, 0, 50), (14, 0, 0, 20), (40, 0, 0, 20))
    a.s("gun", (10, 1, 1, 1), (14, 1, 1, 1))
    legs(a, [(10, 0, 0, 0), (18, 80, 0, 6), (40, 84, 0, 6)], [(10, 0, 0, 0), (18, 80, 0, -6), (40, 84, 0, -6)], sr=[(18, -100, 0, 0), (40, -100, 0, 0)])
    a.p("root", (12, 0, 0, 0), (18, 0, -8, 0), (28, 0, 1.6, -4), (40, 0, 1.8, -6))
    a.r("root", (18, 0, 0, 0), (28, -70, 0, 0), (32, -84, 0, 0), (36, -80, 0, 0), (40, -82, 0, 0))
    for s, k in ((1, "r"), (-1, "l")):
        a.r("wing_" + k, (8, 0, -20 * s, 40 * s), (20, 0, 10 * s, -30 * s), (40, 0, 10 * s, -50 * s))
    a.wave(("tail", "tail1", "tail2", "tail3", "tail4", "tail5"), [(0, 0, 0, 0), (6, 30, 30, 0), (20, -10, -20, 0), (40, -20, 10, 0)], 2)
    sec(a, [(0, 0, 0, 0), (4, -10, 0, 8), (8, 10, 0, -8), (20, -30, 0, 0), (32, -60, 0, 0), (40, -60, 0, 0)], tail=False, wings=False)
    a.done()


for form in ("matured", "cyborg"):
    mm, _ = build(form)
    (anims_cyborg if form == "cyborg" else anims_matured)(mm)
    path = ROOT + mm.name + ".bbmodel"
    mm.save(path)
    print(mm.name, "cubes", len(mm.cubes), "anims", len(mm.anims), [a["name"] for a in mm.anims])
