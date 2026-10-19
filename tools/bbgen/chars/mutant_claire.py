"""Mutant Claire (FPE Green mutant student, CLAIRE 001) - generates assets/fpe/bbmodels/mutant_claire.bbmodel.
Reference: docs/ref/confirmed/mutants_sheet.png (label CLAIRE 001): white shaggy bob/hood with two pointed wolf ears,
the whole face is a HUGE black maw full of jagged white teeth, a single black eye up on her right, oversized white
collared shirt (sleeves swallow the hands, only black claws poke out), black strap across the chest to a big white
satchel on her right hip, white shorts, black jagged legs and big black clawed feet. Hunched, ink-outlined, monochrome.
Blockbench space: Y up, ground 0, faces -Z. Character's RIGHT = +X.
Rotation signs (file values): arm/leg rx>0 = swing forward, torso/head rx>0 = lean back / look up, jaw rx<0 = open,
ry>0 = turn to the character's left, rz>0 = hanging part swings toward +X (character's right).
Every key tick matches entity/characters/MutantClaire.java.
Run: python3 tools/bbgen/chars/mutant_claire.py
"""
import math, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from bbgen import Model, mix  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "../../../src/main/resources/assets/fpe/bbmodels/mutant_claire.bbmodel")

# ------------------------------------------------------------------ palette (monochrome ink drawing)
WH, WH_D, WH_DD, WH_L = 0xF1F1F3, 0xC6C7CE, 0x9C9EA8, 0xFFFFFF
BLK, BLK_L, BLK_D = 0x17171C, 0x34343E, 0x0A0A0D
LINE = 0x24242C
MOUTH, MOUTH_L, GUM = 0x0C0B0F, 0x2A1B22, 0x3A2630
TOOTH, TOOTH_D = 0xFCFCFC, 0xBFC0C8
PAPER, INK = 0xFAFAF6, 0x8A8E98

m = Model("mutant_claire", S=8, atlas=2048)
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


def cloth(base=WH, dark=WH_D, n=2, hem=True, ink=True):
    """white cloth: soft vertical shading, fold lines, ink outline"""
    def f(F):
        for y in range(F.h):
            for x in range(F.w):
                k = y / max(1, F.h - 1)
                F.px(x, y, mix(base, dark, 0.08 + 0.32 * k * k))
        for i in range(n):
            x = int((i + 0.5) * F.w / n) + R.randint(-2, 2)
            for y in range(int(F.h * 0.25), F.h):
                F.px(x, y, mix(base, WH_DD, 0.45))
                F.px(x + 1, y, mix(base, WH_L, 0.5))
        if hem: F.rect(0, F.h - 3, F.w, 1, WH_DD)
        if ink: outline()(F)
    return f


def hairp(F):
    """shaggy white hair: strands with grey separations + ink edge"""
    cols = [R.random() for _ in range(F.w)]
    for x in range(F.w):
        for y in range(F.h):
            c = WH_L if cols[x] > 0.8 else mix(WH, WH_D, 0.5) if cols[x] < 0.12 else WH
            c = mix(c, WH_D, 0.45 * (y / max(1, F.h - 1)) ** 2)
            F.px(x, y, c)
    outline(WH_DD)(F)


def blackp(F):
    """black limb with a cool sheen streak and torn lighter specks"""
    for y in range(F.h):
        for x in range(F.w):
            c = mix(BLK_L, BLK, min(1, y / max(1, F.h - 1) * 1.3))
            if R.random() < 0.05: c = BLK_L
            F.px(x, y, c)
    F.rect(max(1, F.w // 4), 1, max(1, F.w // 8), max(1, F.h - 3), mix(BLK_L, WH_DD, 0.25))


def teethp(F):
    for y in range(F.h):
        for x in range(F.w):
            F.px(x, y, mix(TOOTH, TOOTH_D, y / max(1, F.h - 1) * 0.5))
    outline(0x50505A)(F)


def mouthp(F):
    for y in range(F.h):
        for x in range(F.w):
            F.px(x, y, mix(MOUTH_L, MOUTH, min(1, y / max(1, F.h - 1) * 1.6)) if R.random() > 0.05 else GUM)


def face_front(F):
    """skull front: white hair-shadowed forehead, slanted black eye (char right = texel left), maw top edge"""
    W, H = F.w, F.h
    for y in range(H):
        for x in range(W):
            F.px(x, y, mix(WH, WH_D, 0.15 + 0.4 * (y / H)))
    F.rect(0, H - 2, W, 2, LINE)  # upper lip ink line
    # the single black eye (slanted almond with a pale glint)
    ex, ey = 15, int(H * 0.5)
    F.poly([(ex - 12, ey + 1), (ex - 2, ey - 8), (ex + 11, ey - 4), (ex + 6, ey + 5), (ex - 3, ey + 7)], BLK)
    F.line(ex - 13, ey - 8, ex + 10, ey - 12, LINE, 1.5)  # angry brow
    F.disc(ex + 2, ey - 1, 1.3, 0xE8F4FF, glow=True)
    outline()(F)


# ------------------------------------------------------------------ skeleton
m.group("root", (0, 0, 0))
m.group("body", (0, 12, 0), parent="root")
for k, o in (("hem_f", (0, 12.5, -2.7)), ("hem_b", (0, 12.5, 2.7)), ("hem_r", (4.3, 12.5, 0)), ("hem_l", (-4.3, 12.5, 0))):
    m.group(k, o, parent="body")
m.group("chest", (0, 12.8, 0), parent="body")
m.group("bag", (4.0, 20.6, 0.6), parent="chest")
m.group("head", (0, 21.0, -1.2), parent="chest")
m.group("jaw", (0, 23.2, 1.6), parent="head")
m.group("bangs", (0, 29.8, -4.6), parent="head")
m.group("hair_b", (0, 29.6, 2.4), parent="head")
m.group("hair_r", (4.0, 29.6, -1.6), parent="head")
m.group("hair_l", (-4.0, 29.6, -1.6), parent="head")
m.group("ear_r", (2.6, 30.0, -0.6), parent="head")
m.group("ear_l", (-2.6, 30.0, -0.6), parent="head")
for s, k in ((1, "r"), (-1, "l")):
    m.group("arm_" + k, (4.7 * s, 20.2, 0.2), parent="chest")
    m.group("fore_" + k, (4.9 * s, 15.0, 0.2), parent="arm_" + k)
    m.group("hand_" + k, (4.9 * s, 9.0, 0.2), parent="fore_" + k)
    m.group("papers_" + k, (4.9 * s, 8.4, -0.6), parent="hand_" + k)
    m.group("leg_" + k, (2.3 * s, 12.0, 0), parent="root")
    m.group("shin_" + k, (2.3 * s, 8.0, 0.2), parent="leg_" + k)
    m.group("foot_" + k, (2.3 * s, 2.2, 0.4), parent="shin_" + k)

# ------------------------------------------------------------------ legs: white shorts, black jagged legs, BIG black clawed feet
for s, k in ((1, "r"), (-1, "l")):
    x = 2.3 * s
    m.cube("shorts_" + k, "leg_" + k, (x - 2.1, 8.2, -2.2), (x + 2.1, 12.4, 2.2), WH, faces=all_faces(cloth(n=2), ("up",)))
    m.cube("shcuff_" + k, "leg_" + k, (x - 2.3, 7.7, -2.4), (x + 2.3, 8.8, 2.4), WH_L, color2=WH_D, grad=True, faces=all_faces(outline(), ("up", "down")))
    m.cube("knee_" + k, "leg_" + k, (x - 1.2, 6.8, -1.1), (x + 1.2, 8.3, 1.3), BLK, faces=all_faces(blackp))
    m.cube("shin_" + k, "shin_" + k, (x - 1.15, 4.4, -1.0), (x + 1.15, 8.2, 1.4), BLK, faces=all_faces(blackp))
    m.cube("calf_" + k, "shin_" + k, (x - 1.7, 1.8, -1.5), (x + 1.7, 5.0, 1.9), BLK, faces=all_faces(blackp))  # flared, torn trouser end
    for i in range(4):  # jagged tatters around the flare
        a = i * 90 + 30
        px, pz = x + math.cos(math.radians(a)) * 1.6, 0.2 + math.sin(math.radians(a)) * 1.7
        m.cube(f"tat{i}_" + k, "shin_" + k, (px - 0.45, 1.4, pz - 0.45), (px + 0.45, 3.4, pz + 0.45), BLK_L if i % 2 else BLK,
               origin=(px, 3.2, pz), rot=(14 * math.sin(math.radians(a)), 0, -14 * math.cos(math.radians(a))))
    m.cube("foot_" + k, "foot_" + k, (x - 1.8, 0.0, -2.8), (x + 1.8, 2.3, 2.2), BLK, faces=all_faces(blackp))
    m.cube("instep_" + k, "foot_" + k, (x - 1.4, 1.6, -2.4), (x + 1.4, 2.9, 1.4), BLK_L, color2=BLK, grad=True)
    m.cube("heel_" + k, "foot_" + k, (x - 0.5, 0.2, 1.8), (x + 0.5, 1.3, 3.3), BLK, origin=(x, 0.8, 2.2), rot=(-25, 0, 0))
    for i in range(3):  # three hooked claws
        cx = x - 1.1 + i * 1.1
        m.cube(f"toe{i}_" + k, "foot_" + k, (cx - 0.45, 0.0, -4.2), (cx + 0.45, 1.4, -2.6), BLK, origin=(cx, 0.8, -2.8), rot=(-12, (i - 1) * -14, 0))
        m.cube(f"claw{i}_" + k, "foot_" + k, (cx - 0.28, -0.2, -5.4), (cx + 0.28, 0.6, -4.0), BLK_L, color2=WH_DD, grad=True,
               origin=(cx, 0.4, -4.2), rot=(28, (i - 1) * -16, 0))

# ------------------------------------------------------------------ hips + oversized shirt tails
m.cube("pelvis", "body", (-4.2, 10.8, -2.4), (4.2, 13.2, 2.4), WH, faces=all_faces(cloth(n=3, hem=False), ("up",)))
m.cube("hem_fc", "hem_f", (-4.6, 8.2, -3.1), (4.6, 12.6, -2.5), WH, origin=(0, 12.5, -2.7), rot=(6, 0, 0),
       faces={"north": combo(cloth(n=3), lambda F: F.rect(F.w // 2, 0, 1, F.h, LINE))})
m.cube("hem_bc", "hem_b", (-4.6, 7.8, 2.5), (4.6, 12.6, 3.1), WH, origin=(0, 12.5, 2.7), rot=(-6, 0, 0), faces={"south": cloth(n=4)})
for s, k in ((1, "r"), (-1, "l")):
    m.cube("hem_s" + k, "hem_" + k, (4.3 * s - 0.3, 8.0, -2.8), (4.3 * s + 0.3, 12.6, 2.8), WH, origin=(4.3 * s, 12.5, 0), rot=(0, 0, 8 * s),
           faces={"east": cloth(n=2), "west": cloth(n=2)})
    m.cube("hem_corner" + k, "hem_f", (2.6 * s - 1.0, 7.4, -3.2), (2.6 * s + 1.0, 8.6, -2.6), WH_D, origin=(2.6 * s, 8.4, -2.9), rot=(0, 0, 12 * s),
           faces={"north": outline()})

# ------------------------------------------------------------------ torso: big shirt, collar, placket + buttons, pocket, chest strap
m.cube("torso", "chest", (-4.4, 12.6, -2.6), (4.4, 21.0, 2.6), WH,
       faces={"north": combo(cloth(n=2, hem=False), lambda F: F.rect(F.w // 2 + 3, 0, 1, F.h, LINE)),
              "south": cloth(n=3, hem=False), "east": cloth(n=1, hem=False), "west": cloth(n=1, hem=False)})
m.cube("placket", "chest", (0.0, 12.6, -2.85), (0.9, 20.2, -2.55), WH_L, faces={"north": outline()})
for i in range(4):
    m.cube(f"button{i}", "chest", (0.2, 19.0 - i * 2.0, -3.0), (0.7, 19.5 - i * 2.0, -2.75), WH_DD)
m.cube("pocket", "chest", (-3.6, 16.4, -2.85), (-1.2, 18.6, -2.55), WH_L, faces={"north": combo(outline(), lambda F: F.rect(0, 4, F.w, 1, LINE))})
m.cube("shadow_chest", "chest", (-4.42, 16.0, -2.7), (-2.6, 21.0, -2.5), WH_D, faces={"north": lambda F: F.rect(0, 0, F.w, F.h, WH_D)})
for s, k in ((1, "r"), (-1, "l")):
    m.cube("collar_" + k, "chest", (0.2 * s if s > 0 else -2.8, 19.8, -3.1), (2.8 if s > 0 else -0.2, 21.6, -2.4), WH_L, color2=WH, grad=True,
           origin=(1.4 * s, 21, -2.7), rot=(-18, 0, -22 * s), faces={"north": outline()})
    m.cube("collar_bk" + k, "chest", (0.2 * s if s > 0 else -3.6, 20.6, -2.4), (3.6 if s > 0 else -0.2, 21.8, 2.4), WH, origin=(1.6 * s, 21, 0), rot=(0, 0, 10 * s),
           faces=all_faces(outline()))
# black strap: char-left shoulder -> char-right hip (front), and down the back
m.cube("strap_f", "chest", (-0.45, 11.3, -3.05), (0.45, 22.9, -2.7), BLK, origin=(0.2, 17.0, -2.85), rot=(0, 0, 41), faces=all_faces(blackp))
m.cube("strap_b", "chest", (-0.45, 11.3, 2.7), (0.45, 22.9, 3.05), BLK, origin=(0.2, 17.0, 2.85), rot=(0, 0, 41), faces=all_faces(blackp))
m.cube("strap_top", "chest", (-3.3, 20.8, -2.9), (-1.9, 21.5, 2.9), BLK)

# ------------------------------------------------------------------ satchel (hangs from the strap at the right hip)
m.cube("bag_body", "bag", (4.6, 9.4, -1.4), (10.0, 15.4, 3.0), WH,
       faces={"east": combo(cloth(n=2), lambda F: F.rect(3, 3, F.w - 6, F.h - 6, WH_D), outline()), "north": cloth(n=2), "south": cloth(n=2),
              "west": cloth(n=1), "down": outline()})
m.cube("bag_flap", "bag", (4.5, 12.6, -1.6), (10.15, 15.7, 3.2), WH_L, color2=WH, grad=True,
       faces={"east": combo(outline(), lambda F: F.rect(0, F.h - 3, F.w, 2, WH_D)), "north": outline(), "south": outline(), "up": outline()})
m.cube("bag_buckle", "bag", (10.1, 11.8, 0.3), (10.5, 13.4, 1.3), BLK)
m.cube("bag_ring", "bag", (4.4, 15.2, 0.2), (5.4, 16.2, 1.0), BLK_L)
m.cube("bag_hang", "bag", (4.4, 15.6, 0.3), (5.0, 20.8, 0.9), BLK, origin=(4.7, 20.6, 0.6), rot=(0, 0, -6))
m.cube("bag_paper", "bag", (6.0, 15.4, -0.8), (8.8, 16.6, 2.2), PAPER, origin=(7.4, 15.5, 0.7), rot=(0, 0, 8),
       faces={"east": lambda F: [F.rect(1, y, F.w - 3, 1, INK) for y in range(2, F.h, 3)], "north": lambda F: F.rect(1, 3, F.w - 2, 1, INK)})

# ------------------------------------------------------------------ head: skull + maw (upper teeth, hinged jaw with lower teeth), one eye
m.cube("neck", "head", (-1.4, 20.0, -1.6), (1.4, 23.4, 1.4), BLK_D)
m.cube("skull", "head", (-3.9, 25.0, -4.6), (3.9, 29.6, 2.6), WH, faces={"north": face_front, "south": hairp, "east": hairp, "west": hairp, "up": hairp})
m.cube("maw_in", "head", (-3.4, 20.8, -4.4), (3.4, 25.2, 1.6), MOUTH, faces=all_faces(mouthp))
m.cube("tongue", "jaw", (-2.0, 22.6, -3.6), (2.0, 23.4, 0.6), GUM, color2=MOUTH, grad=True)
m.cube("jaw_base", "jaw", (-3.8, 20.6, -4.7), (3.8, 23.0, 2.0), WH,
       faces={"north": combo(cloth(n=1, hem=False), lambda F: F.rect(0, 0, F.w, 2, LINE)), "east": cloth(n=1, hem=False), "west": cloth(n=1, hem=False),
              "down": cloth(n=1, hem=False), "up": mouthp, "south": hairp})
m.cube("chin_shadow", "jaw", (-3.6, 20.45, -4.5), (3.6, 20.7, 1.8), WH_DD)
# jagged teeth: diamonds (45 deg about z) = pointed white fangs; upper hang down, lower point up
up_t = [(-3.0, 1.5), (-1.95, 2.1), (-0.9, 1.4), (0.15, 2.3), (1.2, 1.5), (2.2, 2.0), (3.1, 1.4)]
for i, (x, sz) in enumerate(up_t):
    m.cube(f"tu{i}", "head", (x - sz / 2, 25.0 - sz / 2, -4.55), (x + sz / 2, 25.0 + sz / 2, -3.7), TOOTH, origin=(x, 25.0, -4.1), rot=(0, 0, 45),
           faces=all_faces(teethp))
for i, z in enumerate((-3.0, -1.6, -0.3)):  # side fangs (visible in 3/4 views)
    for s in (1, -1):
        m.cube(f"tus{i}{'r' if s > 0 else 'l'}", "head", (3.2 * s - 0.45, 24.4, z - 0.55), (3.2 * s + 0.45, 25.5, z + 0.55), TOOTH,
               origin=(3.2 * s, 25.0, z), rot=(45, 0, 0), faces=all_faces(teethp))
lo_t = [(-2.8, 1.6), (-1.6, 1.2), (-0.45, 1.9), (0.75, 1.3), (1.85, 1.9), (2.95, 1.3)]
for i, (x, sz) in enumerate(lo_t):
    m.cube(f"tl{i}", "jaw", (x - sz / 2, 23.0 - sz / 2, -4.6), (x + sz / 2, 23.0 + sz / 2, -3.8), TOOTH, origin=(x, 23.0, -4.2), rot=(0, 0, 45),
           faces=all_faces(teethp))
for i, z in enumerate((-2.6, -1.0)):
    for s in (1, -1):
        m.cube(f"tls{i}{'r' if s > 0 else 'l'}", "jaw", (3.1 * s - 0.4, 22.6, z - 0.5), (3.1 * s + 0.4, 23.6, z + 0.5), TOOTH,
               origin=(3.1 * s, 23.1, z), rot=(45, 0, 0), faces=all_faces(teethp))

# ------------------------------------------------------------------ shaggy hair hood, bangs, side panels, back, wolf ears
m.cube("hair_cap", "head", (-4.4, 27.6, -5.0), (4.4, 30.4, 3.2), WH, faces=all_faces(hairp))
m.cube("hair_top", "head", (-3.8, 30.2, -4.2), (3.8, 31.0, 2.6), WH_L, faces=all_faces(hairp))
for i, (x, ln, rz) in enumerate([(-3.6, 2.6, 10), (-2.4, 3.4, 4), (-1.2, 2.0, -6), (0.0, 2.9, 3), (1.2, 1.4, -4), (2.6, 0.9, -12), (3.7, 2.4, -16)]):
    # bangs: short over the eye (x 1..3) so the eye stays visible
    m.cube(f"bang{i}", "bangs", (x - 0.7, 29.9 - ln, -5.4 - 0.1 * (i % 2)), (x + 0.7, 30.0, -4.8 - 0.1 * (i % 2)), WH if i % 2 else WH_L,
           origin=(x, 29.9, -5.0), rot=(6, 0, rz), faces=all_faces(hairp))
m.cube("hb_main", "hair_b", (-4.5, 21.8, 2.0), (4.5, 30.0, 3.8), WH, faces=all_faces(hairp))
for i in range(7):
    x = -3.9 + i * 1.3
    ln = 1.8 + (i % 3) * 1.0 + R.uniform(0, 0.6)
    m.cube(f"hb_tip{i}", "hair_b", (x - 0.65, 22.0 - ln, 2.3 + (i % 2) * 0.3), (x + 0.65, 22.4, 3.6 + (i % 2) * 0.3), WH_D if i % 2 else WH,
           origin=(x, 22.2, 3.0), rot=(-10, 0, (i - 3) * 8), faces=all_faces(hairp))
for s, k in ((1, "r"), (-1, "l")):
    # long flat side panels framing the maw, down past the chin (the "hood" look)
    m.cube("hs_main_" + k, "hair_" + k, (4.0 * s - 0.65, 20.2, -4.8), (4.0 * s + 0.65, 29.8, 2.6), WH,
           faces={"east": hairp, "west": hairp, "north": hairp, "south": hairp, "down": outline()})
    for i in range(4):
        z = -4.2 + i * 1.8
        ln = 8.8 + (i % 2) * 1.4 + R.uniform(0, 0.8)
        m.cube(f"hs_lock{i}_" + k, "hair_" + k, (4.5 * s - 0.45, 29.0 - ln, z - 0.6), (4.5 * s + 0.45, 29.0, z + 0.6), WH_D if i % 2 else WH_L,
               origin=(4.5 * s, 29.0, z), rot=(-3, 0, (6 + i * 3) * s), faces=all_faces(hairp))
    for i in range(2):  # sharp flicks at the bottom corners
        m.cube(f"hs_flick{i}_" + k, "hair_" + k, (4.3 * s - 0.4, 18.6, -4.3 + i * 2.2), (4.3 * s + 0.4, 21.4, -3.5 + i * 2.2), WH,
               origin=(4.3 * s, 21.2, -3.9 + i * 2.2), rot=(10, 0, 26 * s), faces=all_faces(hairp))
    # pointed wolf ears: two diamonds (outer white, inner grey) sunk into the cap, tilted out
    ex = 2.6 * s
    m.cube("ear_o_" + k, "ear_" + k, (ex - 1.45, 29.2, -1.1), (ex + 1.45, 32.1, 0.0), WH, origin=(ex, 30.65, -0.6), rot=(0, 0, 45 - 8 * s),
           faces=all_faces(hairp))
    m.cube("ear_i_" + k, "ear_" + k, (ex - 0.9, 29.7, -1.25), (ex + 0.9, 31.5, -1.0), WH_DD, origin=(ex, 30.65, -0.6), rot=(0, 0, 45 - 8 * s))
    m.cube("ear_tip_" + k, "ear_" + k, (ex - 0.35, 31.6, -0.9), (ex + 0.35, 33.2, -0.2), WH, origin=(ex, 31.6, -0.6), rot=(0, 0, -16 * s),
           faces=all_faces(hairp))

# ------------------------------------------------------------------ arms: huge sleeves swallowing the hands, black claws poking out
for s, k in ((1, "r"), (-1, "l")):
    x = 4.9 * s
    m.cube("shoulder_" + k, "arm_" + k, (x - 1.7, 18.6, -1.7), (x + 1.7, 21.2, 2.1), WH, origin=(x, 20, 0.2), rot=(0, 0, 10 * s),
           faces=all_faces(cloth(n=1, hem=False)))
    m.cube("sleeve_" + k, "arm_" + k, (x - 1.45, 14.4, -1.45), (x + 1.45, 19.8, 1.85), WH, faces=all_faces(cloth(n=2, hem=False)))
    m.cube("elbow_" + k, "fore_" + k, (x - 1.55, 13.6, -1.55), (x + 1.55, 15.6, 1.95), WH_D, color2=WH, grad=True, faces=all_faces(outline(), ("up", "down")))
    m.cube("fsleeve_" + k, "fore_" + k, (x - 1.85, 9.4, -1.9), (x + 1.85, 14.2, 2.3), WH, faces=all_faces(cloth(n=2, hem=False), ("down",)))
    m.cube("cuff_" + k, "fore_" + k, (x - 2.05, 8.4, -2.1), (x + 2.05, 9.8, 2.5), WH_L, color2=WH_D, grad=True,
           faces={"north": combo(outline(), lambda F: F.rect(0, 2, F.w, 1, WH_DD)), "south": outline(), "east": outline(), "west": outline(), "down": mouthp})
    m.cube("fold_" + k, "fore_" + k, (x - 1.9, 11.4, -2.0), (x + 1.9, 11.8, 2.4), WH_D)
    m.cube("dark_" + k, "fore_" + k, (x - 1.7, 8.35, -1.8), (x + 1.7, 8.5, 2.2), BLK_D)
    for i in range(3):  # claws curling out of the cuff
        cz = -1.0 + i * 1.1
        m.cube(f"finger{i}_" + k, "hand_" + k, (x - 0.35 + (i - 1) * 0.9, 6.6, cz - 0.35), (x + 0.35 + (i - 1) * 0.9, 9.2, cz + 0.35), BLK,
               origin=(x + (i - 1) * 0.9, 9.0, cz), rot=(-10 + i * 4, 0, (i - 1) * -10 * s), faces=all_faces(blackp))
        m.cube(f"talon{i}_" + k, "hand_" + k, (x - 0.25 + (i - 1) * 0.9, 5.2, cz - 0.95), (x + 0.25 + (i - 1) * 0.9, 7.0, cz - 0.45), BLK_L, color2=WH_DD,
               grad=True, origin=(x + (i - 1) * 0.9, 6.8, cz - 0.4), rot=(-30 + i * 4, 0, (i - 1) * -10 * s))
    m.cube("thumb_" + k, "hand_" + k, (x - 2.0 * s - 0.3, 6.8, -1.6), (x - 2.0 * s + 0.3, 8.9, -1.0), BLK, origin=(x - 1.6 * s, 8.8, -1.2), rot=(-20, 0, -18 * s))
    # props: crumpled test papers + pencils (paper_storm)
    m.cube("ppr_a_" + k, "papers_" + k, (x - 1.6, 4.2, -1.0), (x + 1.4, 7.8, -0.8), PAPER, origin=(x, 6, -0.9), rot=(0, 0, 18 * s),
           faces={"north": lambda F: ([F.rect(2, y, F.w - 5, 1, INK) for y in range(3, F.h - 2, 4)], F.rect(F.w - 8, 2, 5, 5, 0xC03030), outline(INK)(F))})
    m.cube("ppr_b_" + k, "papers_" + k, (x - 1.4, 4.6, -1.4), (x + 1.6, 8.0, -1.2), PAPER, origin=(x, 6, -1.3), rot=(0, 0, -14 * s),
           faces={"north": lambda F: ([F.rect(2, y, F.w - 5, 1, INK) for y in range(3, F.h - 2, 4)], outline(INK)(F))})
    for j in range(2):
        m.cube(f"pencil{j}_" + k, "papers_" + k, (x - 0.25 + j * 0.8 - 0.4, 3.0, -1.9), (x + 0.25 + j * 0.8 - 0.4, 8.6, -1.5), WH_D, color2=BLK, grad=True,
               origin=(x, 6, -1.7), rot=(0, 0, (-24 + j * 30) * s))


# ================================================================== animation
PROPS = ["papers_r", "papers_l"]
HIDE = (.001, .001, .001)

REST = {
    "chest": (-30, 0, 0), "head": (26, 0, 0), "jaw": (-16, 0, 0),
    "arm_r": (34, 0, 6), "fore_r": (10, 0, 0), "hand_r": (0, 0, 0),
    "arm_l": (34, 0, -6), "fore_l": (10, 0, 0), "hand_l": (0, 0, 0),
    "leg_r": (16, 0, 2), "shin_r": (-28, 0, 0), "foot_r": (12, 0, 0),
    "leg_l": (16, 0, -2), "shin_l": (-28, 0, 0), "foot_l": (12, 0, 0),
    "bag": (26, 0, 4), "hem_f": (-6, 0, 0), "hem_b": (6, 0, 0),
}
BODY_Y = -0.9  # crouch from the bent knees


def rest(b):
    return REST.get(b, (0, 0, 0))


def R_(b, t):
    return (t, *rest(b))


class A:
    def __init__(self, name, ticks, loop=False):
        self.name, self.ticks, self.loop, self.tr = name, ticks, loop, {}

    def k(self, bone, ch, keys):
        self.tr.setdefault(bone, {}).setdefault(ch, []).extend(keys)
        return self

    def rot(self, bone, *keys): return self.k(bone, "rotation", keys)
    def pos(self, bone, *keys): return self.k(bone, "position", keys)
    def scl(self, bone, *keys): return self.k(bone, "scale", keys)

    def r(self, bone, *keys):
        """rotation keys framed by the rest pose at 0 and at the end"""
        ks = list(keys)
        if ks[0][0] > 0: ks.insert(0, R_(bone, 0))
        if ks[-1][0] < self.ticks: ks.append(R_(bone, self.ticks))
        return self.rot(bone, *ks)

    def d(self, bone, *keys):
        """rotation keys given as DELTAS from the rest pose"""
        rx, ry, rz = rest(bone)
        return self.r(bone, *[(t, x + rx, y + ry, z + rz) for (t, x, y, z) in keys])

    def show(self, bone, *wins):
        keys = [(0, *HIDE)]
        for (t0, t1) in wins:
            keys += [(t0 - 0.5, *HIDE), (t0, 1, 1, 1), (t0 + 1, 1.2, 1.2, 1.2), (t0 + 2, 1, 1, 1), (t1, 1, 1, 1), (t1 + 0.5, *HIDE)]
        return self.scl(bone, *keys)

    def drape(self, chain, keys, delay=2, gain=0.8, base=None):
        g = 1.0
        for i, b in enumerate(chain):
            seen, out = set(), []
            bx, by, bz = rest(b)
            for (t, x, y, z) in keys:
                tt = min(self.ticks, t + delay * i)
                if tt in seen: continue
                seen.add(tt); out.append((tt, bx + x * g, by + y * g, bz + z * g))
            self.rot(b, *out)
            g *= gain
        return self

    def hair(self, keys, delay=2):
        """x>0 = hair flicks forward, z>0 = toward +X"""
        self.drape(["hair_b"], [(t, x * 0.7, 0, z * 0.5) for (t, x, y, z) in keys], delay=delay)
        self.drape(["hair_r"], [(t, x * 0.5, 0, z * 0.6 + max(0, -x) * 0.25) for (t, x, y, z) in keys], delay=delay)
        self.drape(["hair_l"], [(t, x * 0.5, 0, z * 0.6 - max(0, -x) * 0.25) for (t, x, y, z) in keys], delay=delay)
        self.drape(["bangs"], [(t, x * 0.35, 0, z * 0.3) for (t, x, y, z) in keys], delay=delay)
        self.drape(["ear_r"], [(t, x * 0.4, 0, z * 0.3) for (t, x, y, z) in keys], delay=delay + 1)
        self.drape(["ear_l"], [(t, x * 0.4, 0, z * 0.3) for (t, x, y, z) in keys], delay=delay + 1)
        return self

    def cloth(self, keys, delay=2, bag=True):
        """x>0 = shirt tails kick forward, z>0 = flare toward +X"""
        self.drape(["hem_f"], [(t, x, 0, z * 0.4) for (t, x, y, z) in keys], delay=delay)
        self.drape(["hem_b"], [(t, x * 0.8, 0, z * 0.4) for (t, x, y, z) in keys], delay=delay)
        self.drape(["hem_r"], [(t, x * 0.2, 0, z + abs(x) * 0.3) for (t, x, y, z) in keys], delay=delay)
        self.drape(["hem_l"], [(t, x * 0.2, 0, z - abs(x) * 0.3) for (t, x, y, z) in keys], delay=delay)
        if bag: self.drape(["bag"], [(t, x * 0.8, 0, z * 0.9 + abs(x) * 0.2) for (t, x, y, z) in keys], delay=delay + 1)
        return self

    def done(self):
        for p in PROPS:
            if p not in self.tr or "scale" not in self.tr[p]:
                self.scl(p, (0, *HIDE))
        for b, v in REST.items():
            if b not in self.tr or "rotation" not in self.tr[b]:
                self.rot(b, (0, *v))
        if "body" not in self.tr or "position" not in self.tr["body"]:
            self.pos("body", (0, 0, BODY_Y, 0))
        tracks = {b: {ch: sorted([(t / 20.0, x, y, z) for (t, x, y, z) in v], key=lambda q: q[0]) for ch, v in chs.items()}
                  for b, chs in self.tr.items()}
        m.anim(self.name, self.ticks / 20.0, tracks, loop=self.loop)


def legs(a, kr, kl=None, sr=None, sl=None, fr=None, fl=None):
    """leg DELTA keys (from rest) for the right leg; left mirrors y/z unless given"""
    a.d("leg_r", *kr)
    a.d("leg_l", *(kl or [(t, x, -y, -z) for (t, x, y, z) in kr]))
    if sr: a.d("shin_r", *sr)
    if sl or sr: a.d("shin_l", *(sl or sr))
    if fr: a.d("foot_r", *fr)
    if fl or fr: a.d("foot_l", *(fl or fr))


def bodyp(a, *keys):
    """body position keys, y relative to the crouched rest height"""
    ks = list(keys)
    if ks[0][0] > 0: ks.insert(0, (0, 0, 0, 0))
    if ks[-1][0] < a.ticks: ks.append((a.ticks, 0, 0, 0))
    a.pos("body", *[(t, x, y + BODY_Y, z) for (t, x, y, z) in ks])


def sym(a, bone_r, keys_r, bone_l=None):
    """same delta keys for both sides (mirrored y/z)"""
    a.d(bone_r, *keys_r)
    a.d(bone_l or bone_r.replace("_r", "_l"), *[(t, x, -y, -z) for (t, x, y, z) in keys_r])


# ------------------------------------------------------------------ idle (80 loop): hunched breathing, chattering jaw, creepy head tilt, ear twitch
a = A("idle", 80, loop=True)
a.pos("body", (0, 0, BODY_Y, 0), (20, 0, BODY_Y - 0.35, 0), (40, 0, BODY_Y, 0), (60, 0, BODY_Y - 0.35, 0), (80, 0, BODY_Y, 0))
a.d("chest", (0, 0, 0, 0), (20, 2, 0, 1), (40, 0, 0, 0), (50, -2, 6, -2), (60, 1, 0, 0), (80, 0, 0, 0))
a.d("head", (0, 0, 0, 0), (28, -2, -10, 0), (46, 0, 0, 0), (48, 2, 10, 24), (51, 0, 8, 28), (56, 0, 8, 22), (58, 0, 8, 27), (66, 0, 0, 0), (80, 0, 0, 0))
a.d("jaw", (0, 0, 0, 0), (8, -4, 0, 0), (10, 4, 0, 0), (12, -6, 0, 0), (14, 6, 0, 0), (16, 0, 0, 0), (44, -6, 0, 0), (49, -26, 0, 0), (52, 6, 0, 0),
    (54, -14, 0, 0), (60, 0, 0, 0), (80, 0, 0, 0))
a.d("arm_r", (0, 0, 0, 0), (20, -4, 0, 2), (40, 2, 0, -1), (60, -3, 0, 2), (80, 0, 0, 0))
a.d("arm_l", (0, 2, 0, 0), (20, -2, 0, -1), (40, -3, 0, 2), (60, 2, 0, -2), (80, 2, 0, 0))
a.d("fore_r", (0, 0, 0, 0), (40, 6, 0, 0), (80, 0, 0, 0))
a.d("fore_l", (0, 4, 0, 0), (40, 0, 0, 0), (80, 4, 0, 0))
a.d("hand_r", (0, 0, 0, 0), (30, 0, 0, 0), (32, -24, 0, 0), (34, 6, 0, 0), (36, -18, 0, 0), (40, 0, 0, 0), (80, 0, 0, 0))
a.d("hand_l", (0, 0, 0, 0), (66, 0, 0, 0), (68, -20, 0, 0), (71, 0, 0, 0), (80, 0, 0, 0))
legs(a, [(0, 0, 0, 0), (40, 2, 0, 1), (80, 0, 0, 0)], [(0, 0, 0, 0), (40, -2, 0, -1), (80, 0, 0, 0)],
     sr=[(0, 0, 0, 0), (40, -3, 0, 0), (80, 0, 0, 0)])
a.d("ear_r", (0, 0, 0, 0), (22, 0, 0, 0), (23, -14, 0, 18), (26, 0, 0, 0), (49, -6, 0, 10), (80, 0, 0, 0))
a.d("ear_l", (0, 0, 0, 0), (70, 0, 0, 0), (71, -14, 0, -18), (74, 0, 0, 0), (80, 0, 0, 0))
a.drape(["hair_b"], [(0, 0, 0, 1), (20, -2, 0, 0), (40, 0, 0, -1), (52, 2, 0, -6), (60, 0, 0, 2), (80, 0, 0, 1)], delay=3)
a.drape(["hair_r"], [(0, 0, 0, 1), (40, 1, 0, -1), (50, 0, 0, -4), (56, 0, 0, 6), (80, 0, 0, 1)], delay=4)
a.drape(["hair_l"], [(0, 0, 0, -1), (40, 1, 0, 1), (50, 0, 0, -4), (56, 0, 0, 6), (80, 0, 0, -1)], delay=4)
a.cloth([(0, 1, 0, 1), (40, -1, 0, -1), (80, 1, 0, 1)], delay=4)
a.done()

# ------------------------------------------------------------------ walk (20 loop): lurching hunched stride, sleeves dragging, head bobbing
a = A("walk", 20, loop=True)
a.d("leg_r", (0, 26, 0, 0), (5, 2, 0, 0), (10, -24, 0, 0), (15, 2, 0, 0), (20, 26, 0, 0))
a.d("shin_r", (0, 6, 0, 0), (5, 0, 0, 0), (10, -2, 0, 0), (13, -40, 0, 0), (17, -24, 0, 0), (20, 6, 0, 0))
a.d("foot_r", (0, -16, 0, 0), (5, -6, 0, 0), (10, 14, 0, 0), (14, 20, 0, 0), (20, -16, 0, 0))
a.d("leg_l", (0, -24, 0, 0), (5, 2, 0, 0), (10, 26, 0, 0), (15, 2, 0, 0), (20, -24, 0, 0))
a.d("shin_l", (0, -2, 0, 0), (3, -40, 0, 0), (7, -24, 0, 0), (10, 6, 0, 0), (15, 0, 0, 0), (20, -2, 0, 0))
a.d("foot_l", (0, 14, 0, 0), (4, 20, 0, 0), (10, -16, 0, 0), (15, -6, 0, 0), (20, 14, 0, 0))
a.pos("body", (0, 0, BODY_Y - 0.5, 0), (5, 0, BODY_Y + 0.4, 0), (10, 0, BODY_Y - 0.5, 0), (15, 0, BODY_Y + 0.4, 0), (20, 0, BODY_Y - 0.5, 0))
a.rot("body", (0, 0, 8, -3), (10, 0, -8, 3), (20, 0, 8, -3))
a.d("chest", (0, -4, -6, 4), (5, -1, 0, 0), (10, -4, 6, -4), (15, -1, 0, 0), (20, -4, -6, 4))
a.d("head", (0, 2, 6, -4), (2, -3, 4, -6), (5, 3, 0, 0), (10, 2, -6, 4), (12, -3, -4, 6), (15, 3, 0, 0), (20, 2, 6, -4))
a.d("jaw", (0, -4, 0, 0), (2, 4, 0, 0), (5, -8, 0, 0), (10, -4, 0, 0), (12, 4, 0, 0), (15, -8, 0, 0), (20, -4, 0, 0))
a.d("arm_r", (0, -22, 0, 2), (10, 26, 0, 4), (20, -22, 0, 2))
a.d("arm_l", (0, 26, 0, -4), (10, -22, 0, -2), (20, 26, 0, -4))
a.d("fore_r", (0, 2, 0, 0), (3, 0, 0, 0), (10, 22, 0, 0), (13, 26, 0, 0), (20, 2, 0, 0))
a.d("fore_l", (0, 22, 0, 0), (3, 26, 0, 0), (10, 2, 0, 0), (13, 0, 0, 0), (20, 22, 0, 0))
a.d("hand_r", (0, 10, 0, 0), (10, -16, 0, 0), (20, 10, 0, 0))
a.d("hand_l", (0, -16, 0, 0), (10, 10, 0, 0), (20, -16, 0, 0))
a.hair([(0, -6, 0, 4), (5, -10, 0, 0), (10, -6, 0, -4), (15, -10, 0, 0), (20, -6, 0, 4)], delay=2)
a.cloth([(0, 8, 0, 4), (5, 2, 0, 0), (10, 8, 0, -4), (15, 2, 0, 0), (20, 8, 0, 4)], delay=2)
a.done()

# ------------------------------------------------------------------ maw_chomp (24): rears back + gapes 0-9, lunging SNAP at 11, savage shake, recover
a = A("maw_chomp", 24)
a.d("chest", (5, 14, 0, 0), (8, 18, 0, 0), (10, -16, 0, 0), (11, -24, 0, 0), (14, -20, 0, 0), (18, -10, 0, 0))
a.d("head", (5, 14, 0, 0), (8, 18, 0, 0), (10, -16, 0, 0), (11, -22, 0, 0), (12, -20, 0, 14), (13, -20, 0, -14), (14, -20, 0, 10), (15, -20, 0, -8),
    (18, -8, 0, 0))
a.d("jaw", (4, -30, 0, 0), (8, -50, 0, 0), (10, -54, 0, 0), (11, 12, 0, 0), (12, 8, 0, 0), (15, 10, 0, 0), (18, -16, 0, 0), (21, -6, 0, 0))
bodyp(a, (8, 0, -1.0, 1.4), (10, 0, -0.4, -2.4), (11, 0, -0.6, -3.2), (16, 0, -0.6, -2.8))
sym(a, "arm_r", [(5, 20, 0, 24), (8, 26, 0, 30), (10, -40, 0, 26), (11, -50, 0, 30), (15, -30, 0, 20), (20, -8, 0, 6)])
sym(a, "fore_r", [(8, 30, 0, 0), (11, 0, 0, 0), (16, 20, 0, 0)])
legs(a, [(8, 22, 0, 2), (11, 30, 0, 0), (16, 26, 0, 0)], [(8, 22, 0, -2), (11, -26, 0, 0), (16, -20, 0, 0)],
     sr=[(8, -30, 0, 0), (11, -6, 0, 0), (16, -10, 0, 0)], sl=[(8, -30, 0, 0), (11, 10, 0, 0), (16, 6, 0, 0)])
a.hair([(0, 0, 0, 0), (6, -10, 0, 0), (10, 0, 0, 0), (11, 18, 0, 0), (13, 6, 0, 10), (15, 6, 0, -10), (18, -4, 0, 0), (24, 0, 0, 0)], delay=1)
a.cloth([(0, 0, 0, 0), (8, 6, 0, 0), (11, -12, 0, 0), (15, 4, 0, 0), (24, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ sleeve_flail (32): right sleeve whips across 8, left back 15, double overhead slam 23
a = A("sleeve_flail", 32)
a.r("arm_r", (4, 60, -70, 20), (6, 66, -84, 20), (8, 84, 30, 0), (10, 80, 56, 0), (13, 40, 20, 4), (17, 120, 0, 30), (20, 172, 0, 14), (23, 60, 0, 6),
    (26, 50, 0, 6), (29, 30, 0, 6))
a.r("arm_l", (6, 30, 0, -10), (11, 62, 72, -20), (13, 68, 84, -20), (15, 84, -30, 0), (17, 80, -56, 0), (19, 120, 0, -30), (21, 172, 0, -14),
    (23, 60, 0, -6), (26, 50, 0, -6), (29, 30, 0, -6))
a.r("fore_r", (4, 60, 0, 0), (8, 0, 0, 0), (10, 24, 0, 0), (13, 40, 0, 0), (20, 40, 0, 0), (23, 0, 0, 0), (26, 20, 0, 0))
a.r("fore_l", (11, 60, 0, 0), (15, 0, 0, 0), (17, 24, 0, 0), (21, 40, 0, 0), (23, 0, 0, 0), (26, 20, 0, 0))
a.d("hand_r", (6, 30, 0, 0), (8, -30, 0, 0), (11, 10, 0, 0), (23, -30, 0, 0), (26, 0, 0, 0))
a.d("hand_l", (13, 30, 0, 0), (15, -30, 0, 0), (18, 10, 0, 0), (23, -30, 0, 0), (26, 0, 0, 0))
a.d("chest", (5, 4, -30, 0), (8, -4, 30, 0), (10, -4, 36, 0), (12, 2, -26, 0), (15, -4, 30, 0), (17, -4, -34, 0), (20, 16, 0, 0), (23, -24, 0, 0),
    (26, -20, 0, 0))
a.d("head", (5, 0, 20, 0), (8, -6, -20, 0), (12, 0, 18, 0), (15, -6, -22, 0), (20, 14, 0, 0), (23, -10, 0, 0), (26, -6, 0, 0))
a.d("jaw", (4, -40, 0, 0), (8, -20, 0, 0), (12, -44, 0, 0), (15, -20, 0, 0), (20, -60, 0, 0), (23, 6, 0, 0), (26, -10, 0, 0))
bodyp(a, (8, 0, -0.2, -0.6), (15, 0, -0.2, -1.2), (20, 0, 0.6, -1.2), (23, 0, -1.6, -2.0), (27, 0, -1.4, -1.8))
legs(a, [(8, -12, 0, 0), (15, 14, 0, 0), (23, -20, 0, 0), (27, -18, 0, 0)], [(8, 12, 0, 0), (15, -12, 0, 0), (23, 26, 0, 0), (27, 22, 0, 0)],
     sr=[(23, 20, 0, 0), (27, 16, 0, 0)], sl=[(23, -30, 0, 0), (27, -26, 0, 0)])
a.hair([(0, 0, 0, 0), (5, 0, 0, 12), (9, -4, 0, -14), (12, 0, 0, 12), (16, -4, 0, -14), (20, -10, 0, 0), (23, 16, 0, 0), (27, 4, 0, 0), (32, 0, 0, 0)])
a.cloth([(0, 0, 0, 0), (8, -4, 0, -10), (15, -4, 0, 10), (20, -6, 0, 0), (23, 14, 0, 0), (32, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ bag_swing (34): grabs the strap 0-6, hauls the satchel back 6-14, whirls it round 17
a = A("bag_swing", 34)
a.r("bag", (4, 18, 0, 20), (8, -20, 0, 60), (12, -50, 0, 100), (14, -56, 0, 112), (16, 30, 0, 96), (17, 86, 0, 40), (18, 96, 0, -10), (20, 84, 0, -50),
    (23, 50, 0, -40), (27, 20, 0, 10), (30, 14, 0, 6))
a.r("arm_r", (3, 60, 0, -10), (6, 110, 0, -20), (10, 60, 0, 60), (14, 30, 0, 100), (16, 70, 0, 80), (17, 96, 0, 20), (19, 92, 0, -30), (23, 50, 0, -10),
    (29, 26, 0, 6))
a.r("fore_r", (3, 70, 0, 0), (6, 80, 0, 0), (10, 10, 0, 0), (17, 0, 0, 0), (23, 20, 0, 0))
a.d("hand_r", (6, -40, 0, 0), (17, 20, 0, 0), (24, 0, 0, 0))
a.r("arm_l", (6, 10, 0, -20), (14, 70, 0, -30), (17, -20, 0, -40), (22, 0, 0, -20), (30, 26, 0, -6))
a.d("chest", (6, 4, -10, 0), (12, 6, -46, 0), (14, 6, -50, 0), (16, -6, 0, 0), (17, -10, 40, 0), (19, -12, 54, 0), (23, -6, 30, 0), (28, 0, 4, 0))
a.d("head", (6, 0, 10, 0), (14, 4, 30, 6), (17, -8, -20, 0), (20, -6, -30, 0), (26, 0, -6, 0))
a.d("jaw", (6, -10, 0, 0), (14, -50, 0, 0), (17, -60, 0, 0), (20, -30, 0, 0), (26, 0, 0, 0))
a.rot("body", (0, 0, 0, 0), (14, 0, -24, 0), (17, 0, 20, 0), (20, 0, 30, 0), (34, 0, 0, 0))
bodyp(a, (14, 0, -0.6, 1.0), (17, 0, -0.8, -1.4), (22, 0, -0.6, -1.2))
legs(a, [(14, -20, 0, 6), (17, 22, 0, 0), (24, 16, 0, 0)], [(14, 20, 0, -6), (17, -24, 0, 0), (24, -14, 0, 0)],
     sr=[(14, -10, 0, 0), (17, -24, 0, 0)], sl=[(14, -30, 0, 0), (17, 6, 0, 0)])
a.hair([(0, 0, 0, 0), (12, 4, 0, 16), (17, -6, 0, -20), (22, -4, 0, -10), (34, 0, 0, 0)])
a.cloth([(0, 0, 0, 0), (14, 4, 0, 12), (18, -8, 0, -20), (26, -2, 0, -4), (34, 0, 0, 0)], bag=False)
a.done()

# ------------------------------------------------------------------ pounce (36): deep crouch 0-9, launches 10, airborne tuck + gaping maw, crash-bite 20
a = A("pounce", 36)
bodyp(a, (6, 0, -2.6, 1.2), (9, 0, -3.0, 1.4), (11, 0, 2.0, -1.0), (14, 0, 5.0, -2.0), (17, 0, 3.4, -2.2), (20, 0, -2.6, -2.0), (24, 0, -2.2, -1.8),
      (30, 0, -0.6, -0.6))
a.rot("root", (0, 0, 0, 0), (9, 0, 0, 0), (12, -20, 0, 0), (16, -34, 0, 0), (20, -12, 0, 0), (24, -4, 0, 0), (30, 0, 0, 0), (36, 0, 0, 0))
a.d("chest", (6, -24, 0, 0), (9, -26, 0, 0), (11, 18, 0, 0), (14, 10, 0, 0), (20, -30, 0, 0), (24, -26, 0, 0), (30, -6, 0, 0))
a.d("head", (6, 22, 0, 0), (9, 26, 0, 0), (12, 10, 0, 0), (16, 6, 0, 0), (20, -8, 0, 0), (21, -6, 0, 10), (22, -6, 0, -10), (24, 0, 0, 0))
a.d("jaw", (6, 0, 0, 0), (9, 4, 0, 0), (12, -40, 0, 0), (17, -62, 0, 0), (19, -64, 0, 0), (20, 12, 0, 0), (23, 6, 0, 0), (28, -14, 0, 0))
sym(a, "arm_r", [(6, 50, 0, 6), (9, 56, 0, 8), (11, -50, 0, 24), (14, 110, 0, 20), (17, 140, 0, 14), (20, 60, 0, 10), (24, 50, 0, 10), (30, 10, 0, 0)])
sym(a, "fore_r", [(9, 10, 0, 0), (12, 40, 0, 0), (17, 0, 0, 0), (20, 10, 0, 0)])
sym(a, "hand_r", [(14, 30, 0, 0), (18, -30, 0, 0), (20, 20, 0, 0), (26, 0, 0, 0)])
legs(a, [(6, 40, 0, 4), (9, 46, 0, 4), (11, -30, 0, 0), (14, 50, 0, 4), (17, 56, 0, 4), (20, 40, 0, 6), (24, 34, 0, 4), (30, 6, 0, 0)],
     sr=[(6, -70, 0, 0), (9, -80, 0, 0), (11, 20, 0, 0), (14, -80, 0, 0), (17, -90, 0, 0), (20, -70, 0, 0), (24, -60, 0, 0), (30, -10, 0, 0)],
     fr=[(9, 20, 0, 0), (11, -40, 0, 0), (16, -20, 0, 0), (20, 20, 0, 0), (26, 10, 0, 0)])
a.hair([(0, 0, 0, 0), (9, 6, 0, 0), (12, -26, 0, 0), (17, -18, 0, 0), (20, 26, 0, 0), (24, 6, 0, 0), (36, 0, 0, 0)], delay=1)
a.cloth([(0, 0, 0, 0), (9, 6, 0, 0), (12, -30, 0, 0), (17, -24, 0, 0), (21, 26, 0, 0), (26, 4, 0, 0), (36, 0, 0, 0)], delay=1)
a.done()

# ------------------------------------------------------------------ talon_stomp (30): rears on the left leg, right clawed foot raised high, STOMP 14
a = A("talon_stomp", 30)
legs(a, [(4, 30, 0, 4), (8, 60, 0, 6), (11, 72, 0, 6), (13, 10, 0, 2), (14, -6, 0, 0), (18, -4, 0, 0), (24, 0, 0, 0)],
     [(8, -6, 0, -4), (11, -10, 0, -4), (14, 20, 0, -2), (18, 16, 0, -2), (24, 4, 0, 0)],
     sr=[(4, -40, 0, 0), (8, -70, 0, 0), (11, -76, 0, 0), (13, -10, 0, 0), (14, 8, 0, 0), (18, 4, 0, 0)],
     sl=[(8, 6, 0, 0), (14, -30, 0, 0), (18, -24, 0, 0), (24, -6, 0, 0)],
     fr=[(8, 30, 0, 0), (11, 34, 0, 0), (14, -16, 0, 0), (16, -8, 0, 0)], fl=[(14, 10, 0, 0)])
bodyp(a, (8, -0.6, 0.8, 0.4), (11, -0.8, 1.0, 0.4), (14, 0, -1.6, -0.6), (17, 0, -1.2, -0.6), (24, 0, -0.2, 0))
a.rot("body", (0, 0, 0, 0), (8, 0, 0, -8), (11, 0, 0, -10), (14, 0, 0, 2), (18, 0, 0, 0), (30, 0, 0, 0))
a.d("chest", (8, 18, 0, -4), (11, 22, 0, -4), (13, -10, 0, 0), (14, -20, 0, 2), (17, -16, 0, 0), (23, -4, 0, 0))
a.d("head", (8, 10, 0, 6), (11, 14, 0, 8), (14, -16, 0, 0), (15, -14, 0, 8), (16, -14, 0, -8), (18, -10, 0, 0), (24, 0, 0, 0))
a.d("jaw", (8, -40, 0, 0), (11, -46, 0, 0), (14, -64, 0, 0), (18, -50, 0, 0), (24, -10, 0, 0))
sym(a, "arm_r", [(8, 30, 0, 50), (11, 40, 0, 62), (14, 30, 0, 14), (17, 26, 0, 20), (24, 4, 0, 4)])
sym(a, "fore_r", [(8, 40, 0, 0), (14, 0, 0, 0), (18, 14, 0, 0)])
a.hair([(0, 0, 0, 0), (8, -8, 0, -4), (11, -10, 0, -6), (14, 20, 0, 0), (16, 6, 0, 6), (19, -4, 0, -2), (30, 0, 0, 0)], delay=1)
a.cloth([(0, 0, 0, 0), (8, 6, 0, -6), (12, 10, 0, -8), (15, -16, 0, 4), (19, 6, 0, 0), (30, 0, 0, 0)], delay=1)
a.done()

# ------------------------------------------------------------------ howl (44): coils in 0-11, rears up and HOWLS 14-34 (shockwaves 14 / 22 / 30)
a = A("howl", 44)
a.d("chest", (6, -14, 0, 0), (11, -18, 0, 0), (14, 34, 0, 0), (16, 40, 0, 0), (22, 38, 0, 2), (26, 40, 0, -2), (30, 38, 0, 0), (34, 30, 0, 0), (40, 4, 0, 0))
a.d("head", (6, -12, 0, 0), (11, -16, 0, 0), (14, 30, 0, 0), (16, 34, 0, 0), (18, 30, 0, 4), (20, 34, 0, -4), (22, 30, 0, 4), (24, 34, 0, -4),
    (26, 30, 0, 4), (28, 34, 0, -4), (30, 30, 0, 4), (32, 34, 0, 0), (36, 20, 0, 0), (40, 4, 0, 0))
a.d("jaw", (6, 10, 0, 0), (11, 12, 0, 0), (14, -66, 0, 0), (16, -72, 0, 0), (19, -62, 0, 0), (22, -72, 0, 0), (25, -62, 0, 0), (30, -72, 0, 0),
    (34, -60, 0, 0), (40, -16, 0, 0))
sym(a, "arm_r", [(6, 50, -30, -30), (11, 56, -36, -36), (14, 0, 0, 74), (16, -10, 0, 84), (22, -6, 0, 80), (30, -10, 0, 84), (34, 0, 0, 70), (40, 10, 0, 10)])
sym(a, "fore_r", [(6, 60, 0, 0), (11, 70, 0, 0), (14, 0, 0, 0), (34, 10, 0, 0)])
sym(a, "hand_r", [(14, -30, 0, 0), (17, 10, 0, 0), (20, -20, 0, 0), (34, 0, 0, 0)])
bodyp(a, (6, 0, -1.4, 0.4), (11, 0, -1.8, 0.4), (14, 0, 0.8, 0.6), (34, 0, 0.6, 0.6), (40, 0, 0, 0))
legs(a, [(6, 20, 0, 4), (11, 24, 0, 4), (14, -6, 0, 10), (34, -6, 0, 10), (40, 0, 0, 2)], sr=[(6, -30, 0, 0), (11, -34, 0, 0), (14, 10, 0, 0), (34, 8, 0, 0)])
sym(a, "ear_r", [(11, 10, 0, 0), (14, -50, 0, 30), (34, -46, 0, 26), (40, 0, 0, 0)])
a.drape(["hair_b"], [(0, 0, 0, 0), (11, 6, 0, 0), (14, -24, 0, 0), (17, -30, 0, 0), (20, -22, 0, 0), (23, -30, 0, 0), (26, -22, 0, 0), (30, -30, 0, 0),
                     (36, -10, 0, 0), (44, 0, 0, 0)], delay=1)
a.drape(["hair_r"], [(0, 0, 0, 0), (14, -16, 0, 20), (18, -20, 0, 26), (22, -16, 0, 20), (26, -20, 0, 26), (30, -16, 0, 22), (38, 0, 0, 0)], delay=1)
a.drape(["hair_l"], [(0, 0, 0, 0), (14, -16, 0, -20), (18, -20, 0, -26), (22, -16, 0, -20), (26, -20, 0, -26), (30, -16, 0, -22), (38, 0, 0, 0)], delay=1)
a.drape(["bangs"], [(0, 0, 0, 0), (14, -20, 0, 0), (34, -20, 0, 0), (40, 0, 0, 0)])
a.cloth([(0, 0, 0, 0), (11, 4, 0, 0), (14, -16, 0, 0), (18, -10, 0, 6), (22, -16, 0, -6), (26, -10, 0, 6), (30, -16, 0, -6), (38, 0, 0, 0)], delay=1)
a.done()

# ------------------------------------------------------------------ paper_storm (34): digs failed tests + pencils out of the satchel, hurls 12 / 20 / 27
a = A("paper_storm", 34)
a.show("papers_r", (6, 12), (23, 27))
a.show("papers_l", (15, 20), (23, 27))
a.r("bag", (2, 30, 0, 14), (5, 40, 0, 20), (8, 20, 0, 6))
a.r("arm_r", (3, -20, 0, 40), (5, -30, 0, 46), (8, 100, 0, 30), (10, 160, 0, 34), (12, 70, -20, 0), (14, 50, -24, 0), (18, 30, 0, 10), (22, 130, 0, 30),
    (25, 160, 0, 26), (27, 60, -30, 10), (30, 40, 0, 6))
a.r("arm_l", (6, 10, 0, -10), (11, 90, 40, 10), (13, 110, 50, 10), (16, 150, 0, -30), (18, 168, 0, -32), (20, 64, 20, 0), (22, 130, 0, -30), (25, 160, 0, -26),
    (27, 60, 30, -10), (30, 40, 0, -6))
a.r("fore_r", (5, 40, 0, 0), (10, 60, 0, 0), (12, 0, 0, 0), (16, 20, 0, 0), (25, 60, 0, 0), (27, 0, 0, 0))
a.r("fore_l", (13, 50, 0, 0), (18, 60, 0, 0), (20, 0, 0, 0), (25, 60, 0, 0), (27, 0, 0, 0))
a.d("hand_r", (10, 40, 0, 0), (12, -40, 0, 0), (25, 40, 0, 0), (27, -40, 0, 0))
a.d("hand_l", (18, 40, 0, 0), (20, -40, 0, 0), (25, 40, 0, 0), (27, -40, 0, 0))
a.d("chest", (4, 0, -26, 6), (8, 10, -20, 0), (10, 14, -24, 0), (12, -12, 26, 0), (14, -10, 20, 0), (18, 14, 24, 0), (20, -12, -24, 0), (25, 20, 0, 0),
    (27, -14, 0, 0), (30, -8, 0, 0))
a.d("head", (4, -10, -20, 0), (10, 10, 10, 0), (12, -6, -20, 0), (18, 10, -10, 0), (20, -6, 20, 0), (25, 12, 0, 0), (27, -8, 0, 0))
a.d("jaw", (6, 0, 0, 0), (12, -40, 0, 0), (16, -10, 0, 0), (20, -40, 0, 0), (24, -10, 0, 0), (27, -60, 0, 0), (30, -20, 0, 0))
bodyp(a, (12, 0, -0.4, -0.6), (20, 0, -0.4, -0.8), (25, 0, 0.6, 0), (27, 0, -0.8, -1.0))
legs(a, [(12, -16, 0, 0), (20, 14, 0, 0), (27, -10, 0, 0)], [(12, 16, 0, 0), (20, -14, 0, 0), (27, 12, 0, 0)])
a.hair([(0, 0, 0, 0), (10, -6, 0, 4), (12, 10, 0, -10), (18, -6, 0, -4), (20, 10, 0, 10), (25, -8, 0, 0), (27, 12, 0, 0), (34, 0, 0, 0)])
a.cloth([(0, 0, 0, 0), (12, 0, 0, -8), (20, 0, 0, 8), (27, 8, 0, 0), (34, 0, 0, 0)], bag=False)
a.done()

# ------------------------------------------------------------------ tooth_spit (30): rears back gulping 0-10, spits a fan of fangs 13, again 19
a = A("tooth_spit", 30)
a.d("chest", (6, 14, 0, 0), (10, 18, 0, 0), (12, -14, 0, 0), (13, -18, 0, 0), (15, 6, 0, 0), (17, 12, 0, 0), (19, -18, 0, 0), (22, -14, 0, 0), (26, -4, 0, 0))
a.d("head", (6, 16, 0, 0), (10, 22, 0, 0), (12, -18, 0, 0), (13, -24, 0, 0), (15, 10, 0, 0), (17, 18, 0, 0), (19, -24, 0, 0), (22, -16, 0, 0), (26, 0, 0, 0))
a.d("jaw", (4, 10, 0, 0), (10, 12, 0, 0), (12, -40, 0, 0), (13, -60, 0, 0), (15, 6, 0, 0), (17, 10, 0, 0), (18, -40, 0, 0), (19, -64, 0, 0), (22, -40, 0, 0),
    (26, -10, 0, 0))
sym(a, "arm_r", [(6, -16, 0, 14), (10, -20, 0, 18), (13, 20, 0, 10), (17, -10, 0, 16), (19, 24, 0, 10), (25, 6, 0, 2)])
sym(a, "fore_r", [(10, 30, 0, 0), (13, 0, 0, 0), (17, 26, 0, 0), (19, 0, 0, 0)])
bodyp(a, (10, 0, -0.4, 0.8), (13, 0, -0.6, -0.8), (17, 0, -0.4, 0.4), (19, 0, -0.6, -1.0), (24, 0, -0.2, -0.4))
legs(a, [(10, 8, 0, 4), (13, -6, 0, 4), (19, -8, 0, 4)], sr=[(10, -10, 0, 0), (13, 4, 0, 0), (19, 6, 0, 0)])
a.drape(["ear_r"], [(0, 0, 0, 0), (10, -20, 0, 10), (13, 10, 0, 0), (17, -20, 0, 10), (19, 10, 0, 0), (30, 0, 0, 0)])
a.drape(["ear_l"], [(0, 0, 0, 0), (10, -20, 0, -10), (13, 10, 0, 0), (17, -20, 0, -10), (19, 10, 0, 0), (30, 0, 0, 0)])
a.drape(["hair_b"], [(0, 0, 0, 0), (10, -10, 0, 0), (13, 16, 0, 0), (17, -10, 0, 0), (19, 16, 0, 0), (24, 0, 0, 0)], delay=1)
a.drape(["hair_r"], [(0, 0, 0, 0), (10, -8, 0, 0), (13, 12, 0, 0), (17, -8, 0, 0), (19, 12, 0, 0), (24, 0, 0, 0)], delay=1)
a.drape(["hair_l"], [(0, 0, 0, 0), (10, -8, 0, 0), (13, 12, 0, 0), (17, -8, 0, 0), (19, 12, 0, 0), (24, 0, 0, 0)], delay=1)
a.cloth([(0, 0, 0, 0), (13, -6, 0, 0), (19, -8, 0, 0), (30, 0, 0, 0)])
a.done()

# ------------------------------------------------------------------ jaw_spikes (40): rears up arms high 0-11, SLAMS the maw into the floor 14, gnaws (spike line)
a = A("jaw_spikes", 40)
a.d("chest", (6, 26, 0, 0), (11, 34, 0, 0), (13, -30, 0, 0), (14, -48, 0, 0), (16, -44, 0, 0), (20, -46, 0, 4), (24, -44, 0, -4), (28, -46, 0, 0), (32, -30, 0, 0),
    (36, -8, 0, 0))
a.d("head", (6, 20, 0, 0), (11, 26, 0, 0), (13, -10, 0, 0), (14, -26, 0, 0), (17, -24, 0, 12), (20, -24, 0, -12), (23, -24, 0, 12), (26, -24, 0, -12),
    (29, -22, 0, 0), (34, -6, 0, 0))
a.d("jaw", (6, -50, 0, 0), (11, -60, 0, 0), (13, -64, 0, 0), (14, 12, 0, 0), (17, -24, 0, 0), (19, 10, 0, 0), (22, -24, 0, 0), (24, 10, 0, 0), (27, -24, 0, 0),
    (29, 10, 0, 0), (34, -10, 0, 0))
sym(a, "arm_r", [(6, 130, 0, 20), (11, 150, 0, 24), (13, 90, 0, 10), (14, 60, 0, 16), (28, 60, 0, 16), (32, 40, 0, 10), (37, 6, 0, 0)])
sym(a, "fore_r", [(11, 30, 0, 0), (14, 0, 0, 0), (28, 0, 0, 0)])
sym(a, "hand_r", [(14, -40, 0, 0), (17, -20, 0, 0), (20, -40, 0, 0), (23, -20, 0, 0), (26, -40, 0, 0), (32, 0, 0, 0)])
bodyp(a, (6, 0, 0.8, 0.6), (11, 0, 1.2, 0.8), (14, 0, -3.0, -1.6), (28, 0, -2.8, -1.6), (34, 0, -1.0, -0.6))
legs(a, [(6, -6, 0, 6), (11, -10, 0, 8), (14, 44, 0, 10), (28, 42, 0, 10), (34, 16, 0, 4)],
     sr=[(11, 10, 0, 0), (14, -60, 0, 0), (28, -58, 0, 0), (34, -20, 0, 0)], fr=[(14, 20, 0, 0), (28, 20, 0, 0)])
a.hair([(0, 0, 0, 0), (8, -8, 0, 0), (11, -12, 0, 0), (14, 26, 0, 0), (18, 10, 0, 10), (21, 10, 0, -10), (24, 10, 0, 10), (27, 10, 0, -10), (32, 4, 0, 0),
        (40, 0, 0, 0)], delay=1)
a.cloth([(0, 0, 0, 0), (11, 6, 0, 0), (14, -20, 0, 0), (20, -14, 0, 0), (30, -10, 0, 0), (40, 0, 0, 0)], delay=1)
a.done()

# ------------------------------------------------------------------ maw_trap (36): sleeves raised 0-12, slammed down 16 (ground jaws under the target), mimes the bite 26
a = A("maw_trap", 36)
sym(a, "arm_r", [(5, 90, 0, 30), (10, 150, 0, 28), (13, 156, 0, 26), (15, 90, 0, 10), (16, 66, 0, 8), (20, 64, 0, 14), (23, 70, 0, 24), (26, 66, 0, -6),
                 (29, 60, 0, 0), (33, 20, 0, 0)])
sym(a, "fore_r", [(10, 40, 0, 0), (16, 0, 0, 0), (26, 0, 0, 0), (30, 20, 0, 0)])
sym(a, "hand_r", [(16, -50, 0, 0), (20, 20, 0, 0), (23, 30, 0, 0), (26, -60, 0, 0), (30, 0, 0, 0)])
a.d("chest", (5, 16, 0, 0), (10, 24, 0, 0), (13, 26, 0, 0), (16, -36, 0, 0), (20, -32, 0, 0), (23, -30, 0, 0), (26, -40, 0, 0), (30, -24, 0, 0), (34, -4, 0, 0))
a.d("head", (5, 10, 0, 0), (13, 20, 0, 0), (16, -10, 0, 0), (20, 4, 0, 0), (23, 8, 0, 0), (26, -14, 0, 0), (27, -12, 0, 10), (28, -12, 0, -10), (30, -6, 0, 0))
a.d("jaw", (5, -30, 0, 0), (13, -50, 0, 0), (16, -20, 0, 0), (20, -60, 0, 0), (24, -70, 0, 0), (26, 12, 0, 0), (28, 6, 0, 0), (32, -10, 0, 0))
bodyp(a, (10, 0, 0.6, 0.4), (16, 0, -2.2, -1.0), (26, 0, -2.4, -1.2), (32, 0, -0.6, -0.2))
legs(a, [(10, -4, 0, 6), (16, 36, 0, 10), (26, 38, 0, 10), (32, 10, 0, 2)], sr=[(16, -50, 0, 0), (26, -52, 0, 0), (32, -10, 0, 0)])
a.hair([(0, 0, 0, 0), (12, -10, 0, 0), (16, 18, 0, 0), (22, 0, 0, 0), (26, 14, 0, 0), (28, 4, 0, 8), (30, 4, 0, -8), (36, 0, 0, 0)], delay=1)
a.cloth([(0, 0, 0, 0), (12, 6, 0, 0), (16, -16, 0, 0), (26, -14, 0, 0), (36, 0, 0, 0)], delay=1)
a.done()

# ------------------------------------------------------------------ devour (60, enraged): lunging sleeve grab 12, hoists prey to the maw, chomps 24/32/40, flings 50
a = A("devour", 60)
sym(a, "arm_r", [(5, -20, 0, 30), (9, 40, 0, 26), (11, 90, 0, -6), (12, 96, 0, -12), (16, 110, 0, -16), (21, 130, 0, -20), (24, 128, 0, -22), (28, 132, 0, -18),
                 (32, 128, 0, -22), (36, 132, 0, -18), (40, 128, 0, -22), (45, 160, 0, -10), (48, 166, 0, 0), (50, 70, 0, 20), (53, 56, 0, 24), (58, 10, 0, 4)])
sym(a, "fore_r", [(9, 40, 0, 0), (12, 10, 0, 0), (21, 50, 0, 0), (40, 50, 0, 0), (48, 40, 0, 0), (50, 0, 0, 0), (55, 20, 0, 0)])
sym(a, "hand_r", [(9, 30, 0, 0), (12, -50, 0, 0), (40, -50, 0, 0), (50, 40, 0, 0), (55, 0, 0, 0)])
a.d("chest", (5, 10, 0, 0), (9, -16, 0, 0), (12, -26, 0, 0), (16, -10, 0, 0), (21, 10, 0, 0), (24, 4, 0, 4), (28, 12, 0, -2), (32, 4, 0, -4), (36, 12, 0, 2),
    (40, 4, 0, 4), (45, 26, 0, 0), (48, 30, 0, 0), (50, -20, 0, 0), (54, -16, 0, 0), (58, -4, 0, 0))
a.d("head", (5, 10, 0, 0), (12, -10, 0, 0), (21, 20, 0, 0), (24, -14, 0, 14), (26, -10, 0, -12), (28, 16, 0, 0), (32, -14, 0, -14), (34, -10, 0, 12), (36, 16, 0, 0),
    (40, -16, 0, 14), (42, -12, 0, -10), (45, 20, 0, 0), (50, -10, 0, 0), (56, 0, 0, 0))
a.d("jaw", (5, -30, 0, 0), (12, -50, 0, 0), (18, -40, 0, 0), (22, -72, 0, 0), (24, 12, 0, 0), (27, 8, 0, 0), (29, -66, 0, 0), (32, 12, 0, 0), (35, 8, 0, 0),
    (37, -70, 0, 0), (40, 12, 0, 0), (44, 6, 0, 0), (48, -20, 0, 0), (50, -60, 0, 0), (54, -30, 0, 0), (58, -6, 0, 0))
bodyp(a, (5, 0, -0.8, 1.0), (10, 0, -0.6, -2.2), (12, 0, -0.8, -3.0), (21, 0, 0.6, -1.6), (40, 0, 0.6, -1.6), (48, 0, 0.8, -1.0), (50, 0, -1.2, -2.4), (55, 0, -0.8, -1.6))
legs(a, [(5, 20, 0, 2), (10, 30, 0, 0), (12, 34, 0, 0), (21, 6, 0, 6), (40, 6, 0, 6), (50, 30, 0, 0), (55, 24, 0, 0)],
     [(5, 20, 0, -2), (10, -20, 0, 0), (12, -26, 0, 0), (21, 6, 0, -6), (40, 6, 0, -6), (50, -20, 0, 0), (55, -14, 0, 0)],
     sr=[(5, -30, 0, 0), (12, -10, 0, 0), (21, 10, 0, 0), (40, 10, 0, 0), (50, -10, 0, 0)], sl=[(5, -30, 0, 0), (12, 10, 0, 0), (21, 10, 0, 0), (50, 10, 0, 0)])
a.hair([(0, 0, 0, 0), (8, -10, 0, 0), (12, 14, 0, 0), (24, 6, 0, 10), (26, 6, 0, -10), (32, 6, 0, -10), (34, 6, 0, 10), (40, 6, 0, 10), (42, 6, 0, -10),
        (48, -14, 0, 0), (50, 20, 0, 0), (56, 4, 0, 0), (60, 0, 0, 0)], delay=1)
a.cloth([(0, 0, 0, 0), (12, -14, 0, 0), (24, 4, 0, 6), (32, 4, 0, -6), (40, 4, 0, 6), (48, 10, 0, 0), (50, -20, 0, 0), (60, 0, 0, 0)], delay=1)
a.done()

# ------------------------------------------------------------------ frenzy (46, enraged): four lunging bite+rake strikes at 10 / 18 / 26 / 34 (r, l, r, both)
a = A("frenzy", 46)
ch, hd, jw, ar, al, bp, hr = [], [], [], [], [], [(0, 0, 0, 0)], []
for i, T in enumerate((10, 18, 26, 34)):
    side = 1 if i % 2 == 0 else -1
    ch += [(T - 4, 12, 20 * side, 0), (T, -24, -24 * side, 0), (T + 2, -20, -20 * side, 0)]
    hd += [(T - 4, 18, -10 * side, 0), (T, -18, 10 * side, 8 * side), (T + 2, -14, 8 * side, -6 * side)]
    jw += [(T - 4, -60, 0, 0), (T, 12, 0, 0), (T + 2, 4, 0, 0)]
    bp += [(T - 4, 0, -0.4, 0.4), (T, 0, -1.0, -2.4), (T + 2, 0, -0.8, -2.0)]
    hr += [(T - 4, -12, 0, 6 * side), (T, 16, 0, -10 * side)]
    if i == 3:
        ar += [(T - 4, 150, 0, 20), (T, 50, 0, -10), (T + 3, 40, 0, -6)]
        al += [(T - 4, 150, 0, -20), (T, 50, 0, 10), (T + 3, 40, 0, 6)]
    elif side > 0:
        ar += [(T - 4, 130, -10, 40), (T, 40, 30, -16), (T + 2, 30, 30, -10)]
        al += [(T - 4, 10, 0, -14), (T, -20, 0, -20)]
    else:
        al += [(T - 4, 130, 10, -40), (T, 40, -30, 16), (T + 2, 30, -30, 10)]
        ar += [(T - 4, 10, 0, 14), (T, -20, 0, 20)]
a.r("chest", *[(t, x - 30, y, z) for (t, x, y, z) in ch], (42, -30, 0, 0))
a.r("head", *[(t, x + 26, y, z) for (t, x, y, z) in hd], (42, 26, 0, 0))
a.r("jaw", *[(t, x - 16, y, z) for (t, x, y, z) in jw], (42, -18, 0, 0))
a.r("arm_r", *ar, (42, 34, 0, 6))
a.r("arm_l", *al, (42, 34, 0, -6))
sym(a, "fore_r", [(6, 40, 0, 0), (10, 0, 0, 0), (14, 30, 0, 0), (18, 10, 0, 0), (22, 40, 0, 0), (26, 0, 0, 0), (30, 40, 0, 0), (34, 0, 0, 0), (40, 10, 0, 0)])
bodyp(a, *bp[1:], (42, 0, -0.2, -0.4))
legs(a, [(6, 20, 0, 0), (10, -20, 0, 0), (14, 26, 0, 0), (18, -24, 0, 0), (22, 26, 0, 0), (26, -20, 0, 0), (30, 28, 0, 0), (34, 30, 0, 0), (40, 6, 0, 0)],
     [(6, -20, 0, 0), (10, 26, 0, 0), (14, -20, 0, 0), (18, 28, 0, 0), (22, -22, 0, 0), (26, 26, 0, 0), (30, -20, 0, 0), (34, -26, 0, 0), (40, -4, 0, 0)],
     sr=[(6, -40, 0, 0), (10, -6, 0, 0), (14, -40, 0, 0), (18, -10, 0, 0), (22, -40, 0, 0), (26, -6, 0, 0), (30, -40, 0, 0), (34, -30, 0, 0)],
     sl=[(6, -6, 0, 0), (10, -40, 0, 0), (14, -6, 0, 0), (18, -40, 0, 0), (22, -6, 0, 0), (26, -40, 0, 0), (30, -6, 0, 0), (34, -30, 0, 0)])
a.hair([(0, 0, 0, 0)] + hr + [(46, 0, 0, 0)], delay=1)
a.cloth([(0, 0, 0, 0), (10, -14, 0, 6), (18, -14, 0, -6), (26, -14, 0, 6), (34, -16, 0, 0), (46, 0, 0, 0)], delay=1)
a.done()

# ------------------------------------------------------------------ jaw_lock (60, grab): gapes + sleeves spread 0-8, lunges and CLAMPS 10, lifts the prey 11-14,
# thrashes it (head + chest whip side to side, peaks 16/20/24/28/32/36 = server sway, gnaw clamps 18/26/34), winds up to her right 38-45, hurls it left 46
a = A("jaw_lock", 60)
TH = [16, 20, 24, 28, 32, 36]
hd, ch, jw = [(4, 8, 0, 0), (8, 20, 0, 0), (10, -20, 0, 0), (14, -6, 0, 0)], [(4, 8, 0, 0), (8, 16, 0, 0), (10, -28, 0, 0), (14, -10, 0, 0)], \
    [(4, -40, 0, 0), (8, -64, 0, 0), (9, -70, 0, 0), (10, 14, 0, 0), (12, 10, 0, 0), (14, 12, 0, 0)]
for i, T in enumerate(TH):
    s = 1 if i % 2 == 0 else -1  # +1 = prey swung to her right
    hd.append((T, -6, -24 * s, 14 * s))
    ch.append((T + 1, -10, -14 * s, 4 * s))
for T in (18, 26, 34):
    jw += [(T - 2, -6, 0, 0), (T, 16, 0, 0), (T + 2, 10, 0, 0)]
hd += [(38, -4, 0, 0), (43, 0, -34, 12), (45, 2, -38, 14), (46, -8, 40, -22), (48, -6, 56, -26), (52, -2, 30, -8), (57, 0, 4, 0)]
ch += [(38, -10, 0, 0), (43, -6, -40, 0), (45, -4, -46, 0), (46, -14, 40, 0), (48, -16, 54, 0), (52, -8, 24, 0), (57, 0, 4, 0)]
jw += [(37, 10, 0, 0), (45, 14, 0, 0), (46, -56, 0, 0), (48, -64, 0, 0), (52, -30, 0, 0), (57, -6, 0, 0)]
a.d("head", *hd)
a.d("chest", *ch)
a.d("jaw", *jw)
# sleeves: spread wide (anticipation), clamp round the prey, clutch through the thrash, fling out with the toss
sym(a, "arm_r", [(4, 20, 0, 30), (8, 36, 0, 46), (10, 56, 0, -14), (14, 50, 0, -20), (36, 54, 0, -18), (43, 40, 0, 4), (46, 70, 0, 10), (48, 60, 0, 30),
                 (53, 20, 0, 10)])
sym(a, "fore_r", [(8, 20, 0, 0), (10, 40, 0, 0), (14, 56, 0, 0), (36, 56, 0, 0), (44, 40, 0, 0), (46, 0, 0, 0), (53, 10, 0, 0)])
sym(a, "hand_r", [(8, 30, 0, 0), (10, -40, 0, 0), (36, -40, 0, 0), (46, 30, 0, 0), (52, 0, 0, 0)])
bodyp(a, (4, 0, -0.6, 0.6), (8, 0, -1.4, 1.4), (10, 0, -0.6, -2.6), (14, 0, 0.2, -2.0), (36, 0, 0.2, -2.0), (43, 0.8, -0.4, -1.6), (46, -0.8, -0.8, -2.2),
      (50, -0.6, -0.4, -1.6), (56, 0, 0, -0.4))
a.rot("body", (0, 0, 0, 0), (14, 0, 0, 0), *[(T + 1, 0, -6 * (1 if i % 2 == 0 else -1), 0) for i, T in enumerate(TH)], (38, 0, 0, 0), (45, 0, -14, 0),
      (47, 0, 18, 0), (52, 0, 8, 0), (60, 0, 0, 0))
legs(a, [(8, 24, 0, 4), (10, 34, 0, 2), (14, 10, 0, 8), (36, 10, 0, 8), (45, -4, 0, 10), (47, 20, 0, 0), (54, 6, 0, 0)],
     [(8, 24, 0, -4), (10, -24, 0, 0), (14, 6, 0, -8), (36, 6, 0, -8), (45, 20, 0, -4), (47, -10, 0, -10), (54, -2, 0, 0)],
     sr=[(8, -40, 0, 0), (10, -14, 0, 0), (14, -20, 0, 0), (36, -20, 0, 0), (45, -30, 0, 0), (47, -6, 0, 0)],
     sl=[(8, -40, 0, 0), (10, 8, 0, 0), (14, -20, 0, 0), (36, -20, 0, 0), (45, -10, 0, 0), (47, -30, 0, 0)])
sym(a, "ear_r", [(8, -24, 0, 16), (10, -40, 0, 30), (36, -36, 0, 26), (46, -10, 0, 0), (52, 0, 0, 0)])
a.hair([(0, 0, 0, 0), (8, -10, 0, 0), (10, 18, 0, 0)] + [(T + 1, 6, 0, -14 * (1 if i % 2 == 0 else -1)) for i, T in enumerate(TH)]
       + [(38, 4, 0, 0), (45, 0, 0, -16), (47, -6, 0, 22), (50, 4, 0, 12), (56, 0, 0, 0), (60, 0, 0, 0)], delay=1)
a.cloth([(0, 0, 0, 0), (8, 6, 0, 0), (10, -14, 0, 0)] + [(T + 1, -4, 0, -8 * (1 if i % 2 == 0 else -1)) for i, T in enumerate(TH)]
        + [(45, 0, 0, -12), (47, -8, 0, 16), (54, 0, 0, 2), (60, 0, 0, 0)], delay=1)
a.done()

# ------------------------------------------------------------------ sleeve_snare (52, pull + pin): cocks the right sleeve back 0-9, LASHES it out 10, REELS
# the prey in 11-19 (leans back, hauling), SLAMS it to the floor 20 and pins it with the right sleeve, left claw rakes 24/30/36, two-sleeve shove 42
a = A("sleeve_snare", 52)
a.r("arm_r", (4, -10, 10, 34), (9, -46, 20, 52), (10, 108, -10, 2), (13, 112, -8, 2), (16, 64, 0, 12), (19, 40, 0, 16), (20, 84, 0, -6), (24, 78, 0, -4),
    (30, 82, 0, -6), (36, 78, 0, -4), (40, 78, 0, -6), (41, 46, 0, 0), (42, 98, 0, -8), (45, 92, 0, -6), (50, 40, 0, 6))
a.r("fore_r", (4, 40, 0, 0), (9, 76, 0, 0), (10, 0, 0, 0), (13, 4, 0, 0), (16, 64, 0, 0), (19, 100, 0, 0), (20, 4, 0, 0), (40, 6, 0, 0), (41, 50, 0, 0),
    (42, 0, 0, 0), (46, 10, 0, 0))
a.d("hand_r", (9, 40, 0, 0), (10, -24, 0, 0), (13, -50, 0, 0), (19, -60, 0, 0), (20, -66, 0, 0), (40, -60, 0, 0), (42, -10, 0, 0), (48, 0, 0, 0))
al = [(5, 40, 0, -14), (9, 66, 0, -22), (10, -20, 0, -24), (13, -14, 0, -20), (17, 60, 0, -20), (19, 130, 0, -22), (20, 70, 0, -10)]
fl, hl, ch, hd, jw, bp = [(9, 30, 0, 0), (10, 20, 0, 0), (19, 50, 0, 0), (20, 0, 0, 0)], [(19, 30, 0, 0), (20, -40, 0, 0)], \
    [(4, 6, -20, 0), (9, 8, -40, 0), (10, -18, 26, 0), (13, -12, 24, 0), (16, 10, 6, 0), (19, 18, 0, 0), (20, -32, 0, 0)], \
    [(4, 0, 12, 0), (9, 6, 28, 0), (10, -10, -18, 0), (13, -4, -14, 0), (16, 6, 0, 0), (19, 12, 0, 0), (20, -22, 0, 0)], \
    [(4, -30, 0, 0), (9, -44, 0, 0), (10, -64, 0, 0), (13, -50, 0, 0), (16, -20, 0, 0), (19, -60, 0, 0), (20, 8, 0, 0)], \
    [(4, 0, -0.6, 0.6), (9, 0, -1.2, 1.0), (10, 0, -0.6, -1.6), (13, 0, -0.6, -1.4), (16, 0, -0.6, 0.8), (19, 0, -0.4, 1.0), (20, 0, -1.3, -1.4)]
for T in (24, 30, 36):  # left-claw rakes into the pinned prey
    al += [(T - 2, 150, 0, -30), (T, 46, 8, 8), (T + 2, 56, 0, 0)]
    fl += [(T - 2, 50, 0, 0), (T, 0, 0, 0), (T + 2, 10, 0, 0)]
    hl += [(T - 2, 40, 0, 0), (T, -50, 0, 0)]
    ch += [(T - 2, -22, -10, 0), (T, -36, 12, 0), (T + 2, -32, 8, 0)]
    hd += [(T - 2, -10, 6, 0), (T, -30, -8, 6), (T + 2, -26, -4, 0)]
    jw += [(T - 2, -56, 0, 0), (T, 14, 0, 0), (T + 2, 6, 0, 0)]
    bp += [(T - 2, 0, -1.1, -1.2), (T, 0, -1.5, -1.6)]
al += [(40, 60, 0, -10), (41, 46, 0, 0), (42, 98, 0, 8), (45, 92, 0, 6), (50, 40, 0, -6)]
fl += [(41, 50, 0, 0), (42, 0, 0, 0), (46, 10, 0, 0)]
hl += [(42, -10, 0, 0), (48, 0, 0, 0)]
ch += [(40, -30, 0, 0), (41, -34, 0, 0), (42, -14, 0, 0), (45, -10, 0, 0), (50, -2, 0, 0)]
hd += [(40, -20, 0, 0), (42, -6, 0, 0), (44, 8, 0, 0), (50, 0, 0, 0)]
jw += [(40, 0, 0, 0), (42, -60, 0, 0), (45, -40, 0, 0), (50, -8, 0, 0)]
bp += [(40, 0, -1.1, -1.4), (41, 0, -1.3, -1.2), (42, 0, -0.8, -2.4), (45, 0, -0.6, -2.0), (50, 0, -0.2, -0.4)]
a.r("arm_l", *al)
a.r("fore_l", *fl)
a.d("hand_l", *hl)
a.d("chest", *ch)
a.d("head", *hd)
a.d("jaw", *jw)
bodyp(a, *bp)
a.rot("body", (0, 0, 0, 0), (9, 0, -16, 0), (10, 0, 12, 0), (13, 0, 10, 0), (19, 0, 0, 0), (52, 0, 0, 0))
legs(a, [(9, -16, 0, 4), (10, 26, 0, 2), (13, 30, 0, 2), (16, 40, 0, 4), (19, 44, 0, 4), (20, 30, 0, 8), (40, 30, 0, 8), (42, 10, 0, 2), (48, 4, 0, 0)],
     [(9, 24, 0, -4), (10, -20, 0, -2), (13, -16, 0, -2), (16, 24, 0, -4), (19, 30, 0, -4), (20, 14, 0, -8), (40, 14, 0, -8), (42, -22, 0, -2), (48, -4, 0, 0)],
     sr=[(9, -20, 0, 0), (10, -6, 0, 0), (16, -10, 0, 0), (19, -6, 0, 0), (20, -44, 0, 0), (40, -44, 0, 0), (42, -14, 0, 0)],
     sl=[(9, -40, 0, 0), (10, -10, 0, 0), (16, -20, 0, 0), (19, -16, 0, 0), (20, -36, 0, 0), (40, -36, 0, 0), (42, -4, 0, 0)],
     fr=[(16, -20, 0, 0), (19, -24, 0, 0), (20, 20, 0, 0), (40, 20, 0, 0), (42, 0, 0, 0)])
a.hair([(0, 0, 0, 0), (9, -6, 0, 10), (10, 14, 0, -12), (14, 4, 0, -4), (19, -12, 0, 0), (20, 22, 0, 0), (24, 8, 0, 4), (30, 8, 0, 4), (36, 8, 0, 4),
        (41, 10, 0, 0), (42, -12, 0, 0), (46, 4, 0, 0), (52, 0, 0, 0)], delay=1)
a.cloth([(0, 0, 0, 0), (9, 4, 0, 10), (10, -10, 0, -12), (16, 6, 0, 0), (19, 8, 0, 0), (20, -18, 0, 0), (40, -14, 0, 0), (42, 6, 0, 0), (52, 0, 0, 0)], delay=1)
a.done()

# ------------------------------------------------------------------ death (40): stagger back with a slack gaping maw, knees buckle, faceplants forward
a = A("death", 40)
a.d("chest", (4, 26, 0, 6), (8, 30, 0, -4), (12, 10, 0, 0), (16, -20, 0, 0), (22, -30, 0, 0), (40, -30, 0, 0))
a.d("head", (4, 26, 0, 10), (8, 30, 0, -14), (12, 16, 0, 10), (16, -10, 0, 0), (22, -20, 0, 24), (40, -20, 0, 26))
a.d("jaw", (4, -60, 0, 0), (8, -64, 0, 0), (12, -30, 0, 0), (16, -50, 0, 0), (22, -40, 0, 0), (40, -44, 0, 0))
sym(a, "arm_r", [(4, -30, 0, 40), (8, -36, 0, 46), (14, 10, 0, 20), (20, 120, 0, 30), (24, 160, 0, 40), (40, 164, 0, 44)])
sym(a, "fore_r", [(8, 20, 0, 0), (20, 0, 0, 0), (40, 10, 0, 0)])
bodyp(a, (4, 0, 0.6, 1.0), (8, 0, 0.4, 1.2), (14, 0, -3.0, 0), (18, 0, -3.4, 0), (24, 0, -2.4, 0), (40, 0, -2.4, 0))
a.pos("root", (0, 0, 0, 0), (16, 0, 0, 0), (22, 0, 2.6, -2.0), (26, 0, 3.0, -3.0), (29, 0, 3.6, -3.0), (31, 0, 3.0, -3.0), (40, 0, 3.0, -3.0))
a.rot("root", (0, 0, 0, 0), (16, 0, 0, 0), (22, -40, 0, 0), (26, -66, 0, 4), (29, -60, 0, 4), (31, -66, 0, 4), (40, -66, 0, 4))
legs(a, [(4, -10, 0, 0), (8, -12, 0, 6), (14, 50, 0, 10), (18, 60, 0, 12), (24, 30, 0, 12), (40, 26, 0, 12)],
     sr=[(8, 10, 0, 0), (14, -80, 0, 0), (18, -90, 0, 0), (24, -40, 0, 0), (40, -36, 0, 0)])
a.drape(["ear_r"], [(0, 0, 0, 0), (12, -30, 0, 20), (40, -40, 0, 30)])
a.drape(["ear_l"], [(0, 0, 0, 0), (12, -30, 0, -20), (40, -40, 0, -30)])
a.hair([(0, 0, 0, 0), (5, 10, 0, 6), (9, 14, 0, -6), (14, -10, 0, 0), (20, -20, 0, 0), (26, 24, 0, 0), (30, 14, 0, 0), (40, 16, 0, 0)])
a.cloth([(0, 0, 0, 0), (6, 10, 0, 0), (14, -10, 0, 0), (22, -20, 0, 0), (27, 20, 0, 0), (40, 14, 0, 0)])
a.done()

os.makedirs(os.path.dirname(OUT), exist_ok=True)
m.save(OUT)
print("cubes", len(m.cubes), "anims", [x["name"] for x in m.anims], "maxY", max(c["to"][1] for c in m.cubes), "atlas rows", m.cy + m.rowh)
