"""Infected Zip - generates assets/fpe/bbmodels/infected_zip.bbmodel.
Reference (only trusted one): docs/ref/confirmed/infected_zip.jpg - black ink-sketch hunched quadruped monster:
long spindly forelimbs reaching the ground, digitigrade hind legs, bristling spiky back + mane, head held LOW and forward with
hollow round eyes and a long gaping jaw full of white teeth, Zip's white spiral-diamond hat on top, big bat wings rising from the
shoulders (membranes hatched with pale patches), long bristly tail.
Hitbox 1.5 x 2.3 blocks -> shoulder hump ~32 px, spikes / wings rise a bit above.
Blockbench space: Y up, ground 0, faces -Z, character's RIGHT = +X. Animation rotations are OFFSETS from the built rest pose.
Signs: hanging limb rx>0 swings forward; backward-pointing part (tail) rx<0 lifts it; upward part rx>0 tilts back;
wing_r rz<0 swings the wing out/down (beat), wing_l mirrored.
Run: python3 tools/bbgen/chars/infected_zip.py
"""
import math, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.dirname(__file__))
from bbgen import mix  # noqa: E402
from alice import Builder, A  # noqa: E402

DIR = os.path.join(os.path.dirname(__file__), "../../../src/main/resources/assets/fpe/bbmodels/")

INK, INK_D, INK_HI, HATCH = 0x131318, 0x060608, 0x2C2C36, 0x4A4A58
MEM, MEM_HI = 0x15151B, 0x7A788A
PAPER, PAPER_D = 0xECEAF2, 0xA4A2B0
TEETH, TEETH_D = 0xF2F0E8, 0x9A968C
MOUTH = 0x1A0A0E
EYE_RING, GLINT = 0xC8C6D4, 0xFFFFFF


# ================================================================== painters
def ink(B, strokes=1.0, base=INK):
    R = B.R

    def f(F):
        for y in range(F.h):
            for x in range(F.w):
                r = R.random()
                F.px(x, y, INK_D if r < 0.12 else mix(base, INK_HI, 0.35) if r > 0.9 else base)
        n = int(max(1, F.w * F.h / 14) * strokes)
        for _ in range(n):  # pen hatching
            x, y = R.uniform(0, F.w), R.uniform(0, F.h)
            ln = R.uniform(2, 6)
            ang = R.choice((0.9, 1.1, 2.1, 2.3, 1.57)) + R.uniform(-0.15, 0.15)
            F.line(x, y, x + math.cos(ang) * ln, y + math.sin(ang) * ln, HATCH if R.random() < 0.6 else INK_HI, 1)
    return f


def membrane(B):
    R = B.R

    def f(F):
        for y in range(F.h):
            for x in range(F.w):
                F.px(x, y, mix(MEM, INK_D, 0.3 * y / max(1, F.h - 1)))
        for _ in range(max(1, F.w * F.h // 160)):  # pale torn patches (white paper showing through, like the sketch)
            cx, cy = R.uniform(0, F.w), R.uniform(0, F.h)
            F.disc(cx, cy, R.uniform(1.2, 3), mix(MEM, MEM_HI, R.uniform(0.35, 0.7)))
        for _ in range(max(2, F.w * F.h // 10)):
            x, y = R.uniform(0, F.w), R.uniform(0, F.h)
            F.line(x, y, x + R.uniform(-1, 1), y + R.uniform(3, 7), HATCH, 1)
        for i in range(0, F.w, 5):  # veins
            F.line(i, 0, i + 1, F.h, INK_D, 1)
        F.rect(0, 0, F.w, 1, INK_D)
    return f


def ribs_p(B):
    def f(F):
        ink(B, 0.6)(F)
        for i in range(1, max(2, F.w // 5)):
            x = i * 5
            F.line(x, 0, x - 2, F.h, HATCH, 1)
            F.line(x + 1, 0, x - 1, F.h, INK_D, 1)
    return f


def face_p(B):
    def f(F):
        W, H = F.w, F.h
        ink(B, 0.5)(F)
        for cx in (0.27 * W, 0.73 * W):
            cy = 0.42 * H
            F.disc(cx, cy, 0.24 * W, EYE_RING)
            F.disc(cx, cy, 0.19 * W, INK_D)
            F.disc(cx, cy, 0.13 * W, 0x000000)
            F.disc(cx + (0.04 * W if cx < W / 2 else -0.04 * W), cy - 0.03 * H, 0.05 * W, GLINT, glow=True)
        F.line(0.05 * W, 0.12 * H, 0.42 * W, 0.2 * H, INK_D, 1)
        F.line(0.95 * W, 0.12 * H, 0.58 * W, 0.2 * H, INK_D, 1)
        for x in (0.2, 0.8):  # ink drips under the eyes
            F.line(x * W, 0.66 * H, x * W, H, INK_D, 1)
    return f


def teeth_down(n):
    def f(F):
        F.rect(0, 0, F.w, F.h, MOUTH)
        tw = F.w / n
        for i in range(n):
            x0 = i * tw
            F.poly([(x0, 0), (x0 + tw, 0), (x0 + tw * 0.5, F.h)], TEETH)
            F.line(x0 + tw * 0.5, 0, x0 + tw * 0.5, F.h * 0.5, TEETH_D, 1)
    return f


def teeth_up(n):
    def f(F):
        F.rect(0, 0, F.w, F.h, MOUTH)
        tw = F.w / n
        for i in range(n):
            x0 = i * tw
            F.poly([(x0, F.h), (x0 + tw, F.h), (x0 + tw * 0.5, 0)], TEETH)
    return f


def mouth_p(F):
    F.rect(0, 0, F.w, F.h, MOUTH)
    for x in range(0, F.w, 4):
        F.line(x, 0, x + 2, F.h, 0x2A1018, 1)


def hat_p(F):
    W, H = F.w, F.h
    F.rect(0, 0, W, H, PAPER)
    F.rect(0, 0, W, 1, INK_D); F.rect(0, H - 1, W, 1, INK_D); F.rect(0, 0, 1, H, INK_D); F.rect(W - 1, 0, 1, H, INK_D)
    cx, cy = W / 2, H / 2
    pts, a = [], 0.0
    while a < 4.2 * math.pi:  # square-ish spiral like the drawing
        r = 0.45 * min(W, H) * (a / (4.2 * math.pi))
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        a += 0.25
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        F.line(x1, y1, x2, y2, INK_D, 1)


def paper_p(F):
    F.rect(0, 0, F.w, F.h, PAPER)
    F.rect(0, 0, F.w, 1, INK_D); F.rect(0, F.h - 1, F.w, 1, INK_D)


def claw_p(F):
    for y in range(F.h):
        for x in range(F.w):
            F.px(x, y, mix(INK_D, PAPER_D, 0.5 * y / max(1, F.h - 1)) if x else INK_HI)


# ================================================================== model
def blade2(B, name, parent, base, ln, w, d, rot, col, tip=None):
    """cheap 2-cube spike growing along +Y from base"""
    x, y, z = base
    B.c(name, parent, (x - w / 2, y, z - d / 2), (x + w / 2, y + ln * 0.6, z + d / 2), col, origin=base, rot=rot, faces=B.all(ink(B, 0.5)))
    B.c(name + "t", parent, (x - w * 0.22, y + ln * 0.55, z - d * 0.3), (x + w * 0.22, y + ln, z + d * 0.3), tip or col, origin=base, rot=rot)


def build(B):
    g, c, blade = B.g, B.c, B.blade
    b2 = lambda *a, **k: blade2(B, *a, **k)
    sk = ink(B)
    S = B.all
    st = B.strands(INK, HATCH, INK_D, ink=INK_D)

    g("root", (0, 0, 0))
    g("pelvis", (0, 20, 6), "root")
    c("hips", "pelvis", (-3.1, 17.8, 2.6), (3.1, 23.4, 9.8), INK, faces=S(sk))
    c("rump", "pelvis", (-2.4, 22.6, 4.0), (2.4, 24.2, 9.2), INK_D, faces=S(sk))
    for s, k in ((1, "r"), (-1, "l")):
        c("hipknob_" + k, "pelvis", (2.7 * s - 1, 19.5, 4.6), (2.7 * s + 1, 22.5, 7.4), INK_HI, faces=S(sk))

    # ---------------- hind legs: thigh fwd-down, shin back-down, metatarsus, clawed foot
    for s, k in ((1, "r"), (-1, "l")):
        x = 3.0 * s
        g("leg_" + k, (x, 20, 6), "pelvis", rot=(35, 0, 0))
        c("thigh_" + k, "leg_" + k, (x - 1.5, 14.5, 4.4), (x + 1.5, 21, 7.6), INK, faces=S(sk))
        c("thigh2_" + k, "leg_" + k, (x - 1.0, 11, 5.0), (x + 1.0, 15, 7.0), INK, faces=S(sk))
        c("knee_" + k, "leg_" + k, (x - 0.9, 10.4, 4.6), (x + 0.9, 12.2, 5.6), INK_HI)
        g("shin_" + k, (x, 11, 6), "leg_" + k, rot=(-85, 0, 0))
        c("shinb_" + k, "shin_" + k, (x - 0.8, 2, 5.2), (x + 0.8, 11, 6.8), INK, faces=S(sk))
        b2("hock_" + k, "shin_" + k, (x, 9, 6.6), 3.0, 0.6, 0.5, (120, 0, 0), INK_D, tip=INK_HI)
        g("ank_" + k, (x, 2, 6), "shin_" + k, rot=(60, 0, 0))
        c("meta_" + k, "ank_" + k, (x - 0.6, -4, 5.4), (x + 0.6, 2, 6.6), INK, faces=S(sk))
        g("foot_" + k, (x, -4, 6), "ank_" + k, rot=(-10, 0, 0))
        c("pad_" + k, "foot_" + k, (x - 1.1, -5, 4.6), (x + 1.1, -4, 7.0), INK_D, faces=S(sk))
        for i, o in enumerate((-0.8, 0, 0.8)):
            c(f"toe{i}_{k}", "foot_" + k, (x + o - 0.25, -5, 1.6), (x + o + 0.25, -4.4, 4.8), INK_D, rot=(0, o * 14 * s, 0),
              origin=(x + o, -4.7, 4.6), faces=S(claw_p))

    # ---------------- torso (hunched, rising to a shoulder hump)
    g("body", (0, 21, 4), "pelvis")
    c("belly", "body", (-2.8, 18.6, -6), (2.8, 23.2, 4.6), INK, rot=(22, 0, 0), origin=(0, 21, 4), faces={**S(sk), "down": ribs_p(B)})
    c("ribcage", "body", (-3.9, 21.6, -9.5), (3.9, 28.2, 3.5), INK, rot=(26, 0, 0), origin=(0, 23, 2), faces={**S(sk), "east": ribs_p(B), "west": ribs_p(B)})
    c("hump", "body", (-4.6, 25.0, -9.0), (4.6, 31.6, -2.4), INK, rot=(14, 0, 0), origin=(0, 28, -5), faces=S(sk))
    c("scruff", "body", (-3.6, 30.4, -8.2), (3.6, 32.2, -2.8), INK_D, rot=(14, 0, 0), origin=(0, 28, -5), faces=S(sk))
    for s, k in ((1, "r"), (-1, "l")):
        c("shoulder_" + k, "body", (4.2 * s - 1.4, 25.2, -8.2), (4.2 * s + 1.4, 29.4, -3.8), INK, faces=S(sk))
        c("scap_" + k, "body", (2.2 * s - 1.2, 30.6, -6.4), (2.2 * s + 1.2, 31.6, -1.6), INK_HI, rot=(14, 0, -10 * s), origin=(2.2 * s, 31, -4))
    # spine spikes (big dorsal row + two smaller flank rows), bristling back like the drawing
    g("spines", (0, 30, -4), "body")
    for i in range(13):
        u = i / 12.0
        z = 8.5 - u * 15.5
        y = 23.6 + 8.6 * math.sin(min(1, u * 1.15) * math.pi / 2)
        ln = 2.5 + 4.5 * math.sin(u * math.pi) + (1.2 if i % 2 else 0)
        blade(f"sp{i}", "spines", (0, y, z), ln, 1.0, 0.7, (48 + 20 * (1 - u), 0, (i % 3 - 1) * 6), INK, tip=INK_HI)
    for s, k in ((1, "r"), (-1, "l")):
        for i in range(4):
            u = (i + 0.5) / 4
            z = 6 - u * 12
            y = 22.6 + 7.2 * u
            b2(f"fsp{i}_{k}", "spines", (2.4 * s, y, z), 2.2 + 1.6 * math.sin(u * math.pi), 0.6, 0.5, (60, 0, -34 * s), INK_D, tip=HATCH)
    # chest fur hanging under the neck
    g("chestfur", (0, 25, -9), "body")
    for i, x in enumerate((-2.2, -0.8, 0.6, 2.0)):
        B.lock(f"cf{i}", "chestfur", (x, 25.4, -9.6), 4.0 + (i % 2) * 1.5, 0.9, 0.4, (-8, 0, (i - 1.5) * 8), INK, tip=INK_D, paint=st)

    # ---------------- forelimbs: long and spindly, elbow kinked back, three hooked fingers on the floor
    for s, k in ((1, "r"), (-1, "l")):
        x = 4.6 * s
        g("arm_" + k, (x, 27, -6), "body", rot=(-20, 0, 4 * s))
        c("uarm_" + k, "arm_" + k, (x - 1.2, 20, -7.2), (x + 1.2, 28, -4.8), INK, faces=S(sk))
        c("uarm2_" + k, "arm_" + k, (x - 0.8, 16, -6.8), (x + 0.8, 20.5, -5.2), INK, faces=S(sk))
        b2("elbsp_" + k, "arm_" + k, (x, 17, -5.4), 2.6, 0.6, 0.5, (100, 0, 0), INK_D, tip=INK_HI)
        g("fore_" + k, (x, 16, -6), "arm_" + k, rot=(40, 0, -4 * s))
        c("forearm_" + k, "fore_" + k, (x - 0.7, 3.6, -6.7), (x + 0.7, 16, -5.3), INK, faces=S(sk))
        c("wrist_" + k, "fore_" + k, (x - 0.9, 3.0, -7.0), (x + 0.9, 5.0, -5.0), INK_D)
        g("hand_" + k, (x, 3, -6), "fore_" + k, rot=(-20, 0, 0))
        c("palm_" + k, "hand_" + k, (x - 1.3, 1.2, -7.4), (x + 1.3, 3.2, -4.8), INK, faces=S(sk))
        for i, o in enumerate((-1.0, 0, 1.0)):
            g(f"fing{i}_{k}", (x + o, 1.6, -7.2), "hand_" + k, rot=(60, o * 12 * s, 0))
            c(f"fb{i}_{k}", f"fing{i}_{k}", (x + o - 0.3, -1.6, -7.5), (x + o + 0.3, 1.6, -6.9), INK, faces=S(sk))
            c(f"fc{i}_{k}", f"fing{i}_{k}", (x + o - 0.22, -3.4, -7.45), (x + o + 0.22, -1.4, -6.95), INK_D, rot=(-25, 0, 0),
              origin=(x + o, -1.5, -7.2), faces=S(claw_p))
        c("thumb_" + k, "hand_" + k, (x + 1.2 * s - 0.25, 0.6, -5.4), (x + 1.2 * s + 0.25, 2.2, -4.9), INK_D, rot=(-30, 0, 20 * s), origin=(x + 1.2 * s, 2, -5))

    # ---------------- wings: planar sheets in the wing-local YZ plane, tilted out by the wing group
    for s, k in ((1, "r"), (-1, "l")):
        x = 2.8 * s
        g("wing_" + k, (x, 30.5, -4), "body", rot=(2, 10 * s, -30 * s))
        c("wbone_" + k, "wing_" + k, (x - 0.6, 30.5, -4.6), (x + 0.6, 40.5, -3.4), INK, faces=S(sk))
        c("wmem0_" + k, "wing_" + k, (x - 0.12, 31.5, -3.4), (x + 0.12, 40.2, 0.8), MEM, faces=S(membrane(B)))
        g("wing2_" + k, (x, 40.5, -4), "wing_" + k, rot=(50, 0, 0))
        c("wbone2_" + k, "wing2_" + k, (x - 0.5, 40.5, -4.5), (x + 0.5, 52, -3.5), INK, faces=S(sk))
        c("wclaw_" + k, "wing2_" + k, (x - 0.3, 51.6, -5.8), (x + 0.3, 53.4, -4.6), INK_D, rot=(-40, 0, 0), origin=(x, 52, -4), faces=S(claw_p))
        c("wmem1_" + k, "wing2_" + k, (x - 0.12, 40.8, -3.5), (x + 0.12, 51.5, 1.0), MEM, faces=S(membrane(B)))
        # fingers hang from the wing wrist and fan from straight down (front) to straight back; membranes span toward the next finger
        for i, (ab, ln, wd) in enumerate(((2, 12, 4.4), (-30, 14, 5.6), (-62, 14, 5.6), (-94, 11, 5.0))):
            fg = f"wf{i}_{k}"
            g(fg, (x, 52, -4), "wing2_" + k, rot=(ab - 52, 0, 0))
            c(f"wfb{i}_{k}", fg, (x - 0.32, 52 - ln, -4.32), (x + 0.32, 52, -3.68), INK, faces=S(sk))
            c(f"wfm{i}_{k}", fg, (x - 0.1, 52 - ln * 0.9, -3.7), (x + 0.1, 52 - 0.6, -3.7 + wd), MEM, faces=S(membrane(B)))
            c(f"wft{i}_{k}", fg, (x - 0.2, 52 - ln - 1.6, -4.2), (x + 0.2, 52 - ln + 0.2, -3.8), INK_D, faces=S(claw_p))

    # ---------------- tail: long bristly brush with a pale blade tip
    prev, z0 = "pelvis", 9.4
    for i, (ln, w, rx) in enumerate(((6.5, 2.6, 28), (6.5, 2.2, 14), (6, 1.8, 8), (5.5, 1.4, -6), (4.5, 1.0, -10))):
        tg = f"tail{i}"
        g(tg, (0, 21.5, z0), prev, rot=(rx, 0, 0))
        c(f"tseg{i}", tg, (-w / 2, 21.5 - w / 2, z0), (w / 2, 21.5 + w / 2, z0 + ln + 0.3), INK, faces=S(sk))
        for j in range(2):
            zz = z0 + 1 + j * ln * 0.45
            b2(f"tsp{i}{j}", tg, (0, 21.5 + w / 2 - 0.2, zz), 2.6 + (1 - i / 5) * 2, 0.7, 0.5, (70, 0, (j * 2 - 1) * 12), INK, tip=INK_HI)
            for s in ((1, -1) if j == 0 else ()):
                b2(f"tfr{i}{j}{'rl'[s < 0]}", tg, (s * w / 2, 21.5, zz + 0.5), 1.6 + (1 - i / 5) * 1.6, 0.4, 0.4, (80, 0, -60 * s), INK_D, tip=HATCH)
        prev, z0 = tg, z0 + ln
    c("tblade", prev, (-0.3, 20.0, z0 - 0.4), (0.3, 23.0, z0 + 3.4), PAPER_D, faces={**S(claw_p), "east": paper_p, "west": paper_p})
    c("tblade2", prev, (-0.25, 20.8, z0 + 3.2), (0.25, 22.4, z0 + 5.4), PAPER, faces=S(paper_p))

    # ---------------- neck / head (held low), hollow eyes, long gaping jaw, spiky mane, spiral hat
    g("neck", (0, 29.5, -6.2), "body", rot=(-28, 0, 0))
    c("neck0", "neck", (-2.1, 27.4, -12.8), (2.1, 31.0, -5.8), INK, faces=S(sk))
    for i in range(3):
        b2(f"nsp{i}", "neck", (0, 30.8, -7 - i * 2), 2.4 + i * 0.4, 0.7, 0.5, (55, 0, (i - 1) * 10), INK, tip=INK_HI)
    g("head", (0, 29.2, -12.6), "neck", rot=(10, 0, 0))
    c("skull", "head", (-3.4, 26.2, -18.8), (3.4, 32.4, -11.8), INK, faces={**S(sk), "north": face_p(B)})
    c("brow", "head", (-3.7, 31.4, -19.4), (3.7, 32.6, -15.6), INK_D, rot=(-8, 0, 0), origin=(0, 32, -17))
    for s, k in ((1, "r"), (-1, "l")):
        c("cheek_" + k, "head", (3.1 * s - 0.7, 25.6, -18.4), (3.1 * s + 0.7, 28.4, -13.4), INK_HI, faces=S(sk))
    c("snout", "head", (-2.4, 24.6, -23.6), (2.4, 27.6, -17.8), INK, rot=(-12, 0, 0), origin=(0, 27, -18), faces={**S(sk), "down": teeth_down(6)})
    c("nose", "head", (-1.0, 26.8, -24.2), (1.0, 27.8, -23.2), INK_D, rot=(-12, 0, 0), origin=(0, 27, -18))
    c("upteeth", "head", (-2.3, 23.4, -23.5), (2.3, 24.6, -18.0), TEETH, rot=(-12, 0, 0), origin=(0, 27, -18),
      faces={"north": teeth_down(6), "east": teeth_down(5), "west": teeth_down(5), "south": mouth_p, "down": mouth_p, "up": mouth_p})
    for s, k in ((1, "r"), (-1, "l")):
        b2("fang_" + k, "head", (1.9 * s, 23.6, -22.6), 2.4, 0.6, 0.6, (180, 0, 0), TEETH, tip=TEETH)
    g("jaw", (0, 25.2, -14), "head", rot=(-34, 0, 0))
    c("jawbone", "jaw", (-2.3, 23.2, -23.8), (2.3, 25.0, -13.6), INK, faces={**S(sk), "up": teeth_up(6)})
    c("lowteeth", "jaw", (-2.1, 25.0, -23.4), (2.1, 26.0, -14.6), TEETH, faces={"north": teeth_up(6), "east": teeth_up(7), "west": teeth_up(7), "up": mouth_p, "south": mouth_p})
    c("tongue", "jaw", (-1.0, 24.8, -21.0), (1.0, 25.4, -14.4), MOUTH, faces=S(mouth_p))
    c("chin", "jaw", (-1.6, 22.4, -23.4), (1.6, 23.4, -19.0), INK_D, faces=S(sk))
    g("drool", (0, 23.2, -21), "jaw")
    for i, x in enumerate((-1.2, 0.9)):
        B.lock(f"dr{i}", "drool", (x, 23.4, -21.5 + i * 2), 3.5 + i, 0.5, 0.4, (0, 0, 0), INK_D, tip=INK_D)
    # mane: spiky hair bursting back and up from the skull
    g("mane_t", (0, 32, -15), "head")
    g("mane_b", (0, 30, -12), "head")
    g("mane_s", (0, 29, -15), "head")
    for i, (x, z, rx, rz, ln) in enumerate(((-2.4, -17, 60, 30, 6), (-0.8, -16, 70, 8, 7.5), (0.8, -16, 70, -8, 7.5), (2.4, -17, 60, -30, 6),
                                              (-1.6, -14, 95, 20, 8), (1.6, -14, 95, -20, 8), (0, -18.5, 40, 0, 5))):
        blade(f"mt{i}", "mane_t", (x, 32.2, z), ln, 1.1, 0.7, (rx, 0, rz), INK, tip=INK_HI, paint=st)
    for i, (x, y, rx, rz, ln) in enumerate(((-2.6, 30.5, 120, 25, 7), (0, 31, 115, 0, 8), (2.6, 30.5, 120, -25, 7), (-1.6, 28, 135, 40, 6), (1.6, 28, 135, -40, 6))):
        b2(f"mb{i}", "mane_b", (x, y, -12.2), ln, 1.0, 0.7, (rx, 0, rz), INK, tip=INK_D)
    for s, k in ((1, "r"), (-1, "l")):
        for i, (y, z, rx, rz, ln) in enumerate(((30.5, -17.5, 20, -75, 6), (28.5, -16, 50, -95, 7), (26.8, -14, 90, -110, 5.5), (31.4, -14.5, 70, -55, 6.5))):
            b2(f"ms{i}_{k}", "mane_s", (3.2 * s, y, z), ln, 0.9, 0.6, (rx, 0, rz * s), INK, tip=HATCH)
    for i, x in enumerate((-1.8, -0.2, 1.4)):  # ragged bangs over the eyes
        B.lock(f"bang{i}", "mane_t", (x, 32.4, -18.9), 3.2 + (i % 2), 0.9, 0.4, (-14, 0, (i - 1) * 12), INK, tip=INK_D, paint=st)
    g("hat", (0.6, 32.6, -16), "head", rot=(-12, 0, -16))
    c("hatcard", "hat", (-2.6, 33.4, -16.35), (2.6, 38.6, -15.65), PAPER, rot=(0, 0, 45), origin=(0.0, 36, -16),
      faces={"north": hat_p, "south": hat_p, "east": paper_p, "west": paper_p, "up": paper_p, "down": paper_p})
    c("hatstem", "hat", (-0.4, 32.2, -16.3), (0.4, 34.0, -15.7), INK_D)
    c("hatbit", "hat", (3.4, 38.6, -16.3), (4.8, 40.0, -15.7), PAPER, rot=(0, 0, 30), origin=(4.1, 39.3, -16), faces=S(hat_p))


# ================================================================== animation
class Z(A):
    def sec(self, keys, delay=2):
        """secondary motion from a body signal (t, x, z): x = lurch forward(+)/back, z = sway toward +X"""
        self.drape("mane_t", [(t, -x * 0.6, 0, z * 0.5) for (t, x, z) in keys], delay)
        self.drape("mane_b", [(t, -x * 0.8, 0, z * 0.6) for (t, x, z) in keys], delay + 1)
        self.drape("mane_s", [(t, -x * 0.4, 0, z * 0.7) for (t, x, z) in keys], delay)
        self.drape("chestfur", [(t, -x * 0.9, 0, z * 0.9) for (t, x, z) in keys], delay)
        self.drape("drool", [(t, -x * 1.2, 0, z * 1.2) for (t, x, z) in keys], delay + 1)
        self.drape("hat", [(t, -x * 0.3, 0, z * 0.5) for (t, x, z) in keys], delay + 1)
        self.drape("spines", [(t, -abs(x) * 0.12, 0, 0) for (t, x, z) in keys], delay)
        for i in range(4):
            self.drape(f"wf{i}_r", [(t, -x * (0.3 + 0.12 * i), 0, 0) for (t, x, z) in keys], delay + i)
            self.drape(f"wf{i}_l", [(t, -x * (0.3 + 0.12 * i), 0, 0) for (t, x, z) in keys], delay + i)
        return self

    def tail(self, keys, lag=1.5):
        """(t, lift, swing): lift>0 raises the tail (curls it up), swing>0 swings it toward +X; lags down the chain"""
        for i in range(5):
            gain = 0.7 + 0.15 * i
            self.drape(f"tail{i}", [(t, -lift * gain, swing * gain, 0) for (t, lift, swing) in keys], int(round(i * lag)))
        return self

    def wings(self, t, beat=0.0, sweep=0.0, fold=0.0, spread=0.0, r=True, l=True):
        """beat>0 swings wings out/down, beat<0 raises them over the back; sweep>0 sweeps them back; fold>0 closes the fingers,
        spread>0 opens the elbow"""
        for s, k, on in ((1, "r", r), (-1, "l", l)):
            if not on: continue
            self.rot("wing_" + k, (t, sweep, 0, -beat * s))
            self.rot("wing2_" + k, (t, -spread * 0.7 + fold * 0.6, 0, 0))
            for i in range(4):
                self.rot(f"wf{i}_{k}", (t, fold * (0.3 + 0.25 * i) - spread * (0.2 + 0.25 * i), 0, 0))
        return self

    def legs(self, t, d=0.0, lean=0.0, r=None, l=None):
        """crouch: d>0 lowers the pelvis (~d px); per-leg override r/l = (thigh, shin, ankle, foot)"""
        k = d * 4.0
        base = (k, -k * 1.7, k * 1.1, -k * 0.4)
        for side, ov in (("r", r), ("l", l)):
            th, sh, an, fo = ov if ov else base
            self.at(t, **{"leg_" + side: (th, 0, 0), "shin_" + side: (sh, 0, 0), "ank_" + side: (an, 0, 0), "foot_" + side: (fo, 0, 0)})
        self.pos("pelvis", (t, 0, -d, lean))
        return self

    def arms(self, t, r=(0, 0, 0), l=(0, 0, 0), fr=(0, 0, 0), fl=(0, 0, 0), hr=(0, 0, 0), hl=(0, 0, 0)):
        """arm offsets given for the RIGHT side convention; left rz/ry are mirrored automatically"""
        m = lambda v: (v[0], -v[1], -v[2])
        self.at(t, arm_r=r, arm_l=m(l), fore_r=fr, fore_l=m(fl), hand_r=hr, hand_l=m(hl))
        return self

    def claws(self, t, curl=0.0, side=None):
        for k in (("r", "l") if side is None else (side,)):
            for i in range(3):
                self.rot(f"fing{i}_{k}", (t, curl, 0, 0))
        return self


Z0 = (0, 0, 0)


def anims(B):
    def mk(name, ticks, loop=False):
        return Z(B, name, ticks, {}, (), loop)

    # ---------------- idle (60): ragged breathing, head twitch, jaw working, wings flex, tail sways
    a = mk("idle", 60, loop=True)
    for t, j in ((0, 0), (15, 1), (30, 0), (45, -1), (60, 0)):
        a.at(t, body=(-1.5 * abs(j), 2 * j, 0), neck=(3 * abs(j), 0, 0), head=(-3 * abs(j), -6 * j, 5 * j), jaw=(-6 * abs(j), 0, 0))
        a.pos("body", (t, 0, 0.3 * abs(j), 0))
        a.wings(t, beat=-4 * abs(j), spread=3 * abs(j), fold=0)
    a.at(36, head=(4, 8, 14)).at(38, head=(-2, -4, -8))
    a.tail([(0, 0, 6), (15, 4, 0), (30, 0, -6), (45, 4, 0), (60, 0, 6)])
    a.claws(0, 0).claws(20, -10).claws(40, 6).claws(60, 0)
    a.sec([(0, 0, 1), (15, 2, -1), (30, 0, 1), (45, 2, -1), (60, 0, 1)], delay=4)
    a.done(base_layer=True)

    # ---------------- walk (24): stalking quadruped gait, diagonal pairs (front R + hind L), head bobs low, wings bob
    a = mk("walk", 24, loop=True)
    for k, ph in (("r", 0), ("l", 12)):
        def T(t): return (t + ph) % 24
        hk = "l" if k == "r" else "r"
        # foreleg k forward at 0, back at 12; hind leg of the other side in phase
        a.rot("arm_" + k, *sorted([(T(0), 26, 0, 0), (T(12), -22, 0, 0), (T(18), -6, 0, 0), (T(24) or 24, 26, 0, 0)]))
        a.rot("fore_" + k, *sorted([(T(0), -10, 0, 0), (T(12), 10, 0, 0), (T(16), -36, 0, 0), (T(20), -30, 0, 0), (T(24) or 24, -10, 0, 0)]))
        a.rot("hand_" + k, *sorted([(T(0), -10, 0, 0), (T(12), 16, 0, 0), (T(16), 30, 0, 0), (T(24) or 24, -10, 0, 0)]))
        a.rot("leg_" + hk, *sorted([(T(0), 20, 0, 0), (T(12), -20, 0, 0), (T(24) or 24, 20, 0, 0)]))
        a.rot("shin_" + hk, *sorted([(T(0), -6, 0, 0), (T(12), 8, 0, 0), (T(16), -34, 0, 0), (T(20), -22, 0, 0), (T(24) or 24, -6, 0, 0)]))
        a.rot("ank_" + hk, *sorted([(T(0), 0, 0, 0), (T(12), -10, 0, 0), (T(16), 24, 0, 0), (T(24) or 24, 0, 0, 0)]))
    for tr in list(a.tr.values()):  # make loops start at 0
        for ch, ks in tr.items():
            if not any(q[0] == 0 for q in ks):
                last = max(ks, key=lambda q: q[0]); ks.append((0, *last[1:]))
    a.pos("pelvis", (0, 0, -0.5, 0), (6, 0, 0.5, 0), (12, 0, -0.5, 0), (18, 0, 0.5, 0), (24, 0, -0.5, 0))
    a.rot("pelvis", (0, 0, 5, 3), (12, 0, -5, -3), (24, 0, 5, 3))
    a.rot("body", (0, 2, -6, -2), (6, -2, 0, 0), (12, 2, 6, 2), (18, -2, 0, 0), (24, 2, -6, -2))
    a.rot("neck", (0, 4, 0, 0), (6, -2, 0, 0), (12, 4, 0, 0), (18, -2, 0, 0), (24, 4, 0, 0))
    a.rot("head", (0, -4, 8, 3), (12, -4, -8, -3), (24, -4, 8, 3))
    a.rot("jaw", (0, -4, 0, 0), (6, 2, 0, 0), (12, -4, 0, 0), (18, 2, 0, 0), (24, -4, 0, 0))
    for t, j in ((0, 1), (6, -1), (12, 1), (18, -1), (24, 1)):
        a.wings(t, beat=3 * j, fold=2 * j)
    a.tail([(0, 2, -10), (12, 2, 10), (24, 2, -10)], lag=1)
    a.sec([(0, 4, 3), (6, -3, 0), (12, 4, -3), (18, -3, 0), (24, 4, 3)], delay=2)
    a.done(base_layer=True)

    # ---------------- maul (34): rear back + jaw gapes 0-11, LUNGE 13, jaws SNAP 15, tear/shake 16-23, recover
    a = mk("maul", 34)
    a.at(0, body=Z0, neck=Z0, head=Z0, jaw=Z0)
    a.at(9, body=(10, 0, 0), neck=(-22, 0, 0), head=(-20, 0, 0), jaw=(-34, 0, 0))
    a.arms(9, r=(-20, 0, 6), l=(-20, 0, 6), fr=(10, 0, 0), fl=(10, 0, 0))
    a.at(12, body=(12, 0, 0), neck=(-26, 0, 0), head=(-24, 0, 0), jaw=(-52, 0, 0))
    a.at(14, body=(-16, 0, 0), neck=(26, 0, 0), head=(14, 0, 0), jaw=(-50, 0, 0), P_root=(0, 0, -3))
    a.arms(14, r=(50, 0, -6), l=(50, 0, -6), fr=(-20, 0, 0), fl=(-20, 0, 0), hr=(30, 0, 0), hl=(30, 0, 0))
    a.at(15, jaw=(26, 0, 0), head=(18, 0, 0))
    for t, j in ((17, 1), (19, -1), (21, 1), (23, -1)):
        a.at(t, head=(16, 22 * j, 18 * j), neck=(24, 10 * j, 0), body=(-14, 6 * j, 4 * j), jaw=(24, 0, 0))
    a.at(26, body=(-6, 0, 0), neck=(8, 0, 0), head=(4, 0, 0), jaw=(-10, 0, 0), P_root=(0, 0, -2))
    a.arms(24, r=(30, 0, 0), l=(30, 0, 0), fr=(-10, 0, 0), fl=(-10, 0, 0))
    a.at(34, body=Z0, neck=Z0, head=Z0, jaw=Z0, P_root=Z0).arms(34)
    a.legs(0).legs(10, 1.6, 1.2).legs(14, 0.2, -2.2).legs(24, 0.8, -1).legs(34)
    a.wings(0).wings(10, beat=-14, spread=6).wings(14, beat=20, sweep=16, fold=8).wings(24, beat=6).wings(34)
    a.claws(0).claws(10, -20).claws(14, 30).claws(34)
    a.tail([(0, 0, 0), (10, 10, 0), (14, -8, 0), (17, 0, 14), (21, 0, -14), (34, 0, 0)])
    a.sec([(0, 0, 0), (10, -10, 0), (14, 14, 0), (17, 4, 8), (19, 4, -8), (21, 4, 8), (23, 4, -8), (34, 0, 0)], delay=1)
    a.done()

    # ---------------- claw (34): rears onto hind legs 0-8, R swipe peaks 12, L wind 16, L swipe 20, drop 26-34
    a = mk("claw", 34)
    a.at(0, body=Z0, pelvis=Z0)
    a.at(8, pelvis=(-16, 0, 0), body=(-22, -18, 0), neck=(8, 0, 0), head=(16, 14, 0), jaw=(-30, 0, 0))
    a.arms(8, r=(-130, 0, 30), l=(-30, 0, 10), fr=(-40, 0, 0), fl=(20, 0, 0))
    a.claws(8, -30, "r")
    a.at(12, pelvis=(-14, 0, 0), body=(-12, 26, 6), head=(10, -16, 0), jaw=(-40, 0, 0))
    a.arms(12, r=(40, 0, -30), l=(-60, 0, 20), fr=(-10, 0, 0), fl=(-30, 0, 0))
    a.claws(12, 30, "r").claws(12, -30, "l")
    a.at(16, pelvis=(-16, 0, 0), body=(-20, 22, 0), head=(14, -10, 0))
    a.arms(16, r=(20, 0, -20), l=(-140, 0, 34), fr=(0, 0, 0), fl=(-40, 0, 0))
    a.at(20, pelvis=(-12, 0, 0), body=(-10, -28, -6), head=(8, 18, 0), jaw=(-44, 0, 0))
    a.arms(20, r=(-20, 0, 0), l=(44, 0, -32), fr=(0, 0, 0), fl=(-10, 0, 0))
    a.claws(20, 30, "l").claws(20, 0, "r")
    a.at(26, pelvis=(-2, 0, 0), body=(4, -8, 0), head=(-4, 4, 0), jaw=(-12, 0, 0))
    a.arms(26, r=(10, 0, 0), l=(20, 0, -10), fr=(-6, 0, 0), fl=(-10, 0, 0))
    a.at(34, pelvis=Z0, body=Z0, neck=Z0, head=Z0, jaw=Z0).arms(34).claws(34)
    a.legs(0).legs(8, -0.5, 1.5).legs(12, 0.8, -1).legs(20, 0.8, -1.4).legs(28, 0.6).legs(34)
    a.wings(0).wings(8, beat=-20, spread=14).wings(12, beat=10, sweep=-6, r=True, l=False).wings(12, beat=-16, l=True, r=False)
    a.wings(20, beat=-14, r=True, l=False).wings(20, beat=12, sweep=-6, r=False, l=True).wings(34)
    a.tail([(0, 0, 0), (8, -10, 0), (12, -6, -16), (20, -6, 16), (34, 0, 0)])
    a.sec([(0, 0, 0), (8, -12, 0), (12, 8, 10), (16, -4, 0), (20, 8, -10), (34, 0, 0)], delay=1)
    a.done()

    # ---------------- tail_sweep (40): coil low + twist 0-10, two full spins 10-28 (hits 12/16/20/24), skid to a stop
    a = mk("tail_sweep", 40)
    a.at(0, root=Z0)
    a.at(10, root=(0, -40, 0), body=(-6, 20, 0), head=(0, 26, 0))
    for t, y in ((12, 40), (16, 130), (20, 220), (24, 310), (28, 390), (32, 372), (36, 362), (40, 360)):
        a.at(t, root=(0, y, 0))
    a.at(12, body=(-10, -12, -6), head=(6, -24, -10)).at(28, body=(-10, -12, -6), head=(6, -24, -10))
    a.at(33, body=(-4, 8, 4), head=(2, 10, 8)).at(40, body=Z0, head=Z0)
    a.at(0, jaw=Z0).at(12, jaw=(-30, 0, 0)).at(28, jaw=(-30, 0, 0)).at(40, jaw=Z0)
    a.legs(0).legs(10, 2.0).legs(12, 1.2).legs(28, 1.2).legs(33, 1.8).legs(40)
    a.arms(0).arms(10, r=(-10, 0, 20), l=(-10, 0, 20)).arms(12, r=(-30, 0, 40), l=(-30, 0, 40), fr=(20, 0, 0), fl=(20, 0, 0))
    a.arms(28, r=(-30, 0, 40), l=(-30, 0, 40), fr=(20, 0, 0), fl=(20, 0, 0)).arms(40)
    a.wings(0).wings(10, beat=-10, fold=20).wings(12, beat=34, sweep=24, spread=10).wings(28, beat=34, sweep=24, spread=10).wings(34, beat=-6).wings(40)
    a.tail([(0, 0, 0), (10, -2, 40), (12, 14, -30), (28, 14, -30), (32, 6, 14), (36, 0, -6), (40, 0, 0)], lag=1)
    a.sec([(0, 0, 0), (10, 0, -10), (12, 0, 24), (28, 0, 24), (33, 0, -14), (40, 0, 0)])
    a.done()

    # ---------------- wing_slash (36): right wing cocks high + back 0-14, CHOP forward across at 17, follow-through, refold
    a = mk("wing_slash", 36)
    a.at(0, body=Z0)
    a.at(13, body=(-8, 28, 8), neck=(-6, -10, 0), head=(-6, -20, 0), jaw=(-20, 0, 0))
    a.wings(0).wings(13, beat=-36, sweep=30, spread=16, r=True, l=False).wings(13, beat=-8, fold=10, r=False, l=True)
    a.wings(15, beat=-40, sweep=34, spread=18, r=True, l=False)
    a.at(17, body=(8, -34, -10), neck=(10, 10, 0), head=(10, 24, 0), jaw=(-40, 0, 0))
    a.wings(17, beat=56, sweep=-60, spread=20, r=True, l=False).wings(17, beat=10, sweep=10, r=False, l=True)
    a.wings(21, beat=64, sweep=-70, spread=10, fold=6, r=True, l=False)
    a.at(24, body=(4, -24, -6), head=(4, 16, 0), jaw=(-16, 0, 0))
    a.wings(28, beat=20, sweep=-20, r=True, l=False).wings(36)
    a.at(36, body=Z0, neck=Z0, head=Z0, jaw=Z0)
    a.legs(0).legs(13, 1.0, 1).legs(17, 1.6, -1.5).legs(24, 1.2, -1).legs(36)
    a.arms(0).arms(13, r=(-20, 0, 10), l=(10, 0, 0)).arms(17, r=(30, 0, -10), l=(-20, 0, 10), fr=(-20, 0, 0)).arms(36)
    a.claws(0).claws(13, -20).claws(17, 30).claws(36)
    a.tail([(0, 0, 0), (13, 6, -24), (17, -4, 30), (24, 0, 16), (36, 0, 0)], lag=1)
    a.sec([(0, 0, 0), (13, -6, -10), (17, 12, 16), (24, 4, 6), (36, 0, 0)], delay=1)
    a.done()

    # ---------------- pounce (44): deep coil 0-13, LEAP 14 (full stretch), airborne tuck 18-22, LAND ~24 (splat), rise
    a = mk("pounce", 44)
    a.at(0, body=Z0, P_root=Z0, pelvis=Z0)
    a.at(12, body=(4, 0, 0), neck=(-16, 0, 0), head=(-12, 0, 0), jaw=(-14, 0, 0), pelvis=(6, 0, 0))
    a.arms(12, r=(-20, 0, 0), l=(-20, 0, 0), fr=(40, 0, 0), fl=(40, 0, 0), hr=(10, 0, 0), hl=(10, 0, 0))
    a.legs(0).legs(12, 3.2, 1.6)
    a.at(15, body=(14, 0, 0), pelvis=(-16, 0, 0), neck=(-6, 0, 0), head=(-14, 0, 0), jaw=(-56, 0, 0), P_root=(0, 3, 0))
    a.arms(15, r=(90, 0, -14), l=(90, 0, -14), fr=(-20, 0, 0), fl=(-20, 0, 0), hr=(-30, 0, 0), hl=(-30, 0, 0))
    a.legs(15, -0.6, 0, r=(-60, 50, -40, 20), l=(-60, 50, -40, 20))
    a.at(20, body=(0, 0, 0), pelvis=(-4, 0, 0), jaw=(-60, 0, 0), P_root=(0, 5, 0))
    a.arms(20, r=(70, 0, -24), l=(70, 0, -24), fr=(-30, 0, 0), fl=(-30, 0, 0))
    a.legs(20, 0, 0, r=(30, -40, 20, 0), l=(30, -40, 20, 0))
    a.at(24, body=(-18, 0, 0), pelvis=(4, 0, 0), neck=(14, 0, 0), head=(14, 0, 0), jaw=(10, 0, 0), P_root=(0, 0, 0))
    a.arms(24, r=(40, 0, -30), l=(40, 0, -30), fr=(-30, 0, 0), fl=(-30, 0, 0), hr=(20, 0, 0), hl=(20, 0, 0))
    a.legs(24, 3.0, -1)
    a.at(30, body=(-10, 0, 0), pelvis=(2, 0, 0), head=(6, 0, 0), jaw=(-20, 0, 0))
    a.arms(30, r=(26, 0, -20), l=(26, 0, -20))
    a.legs(30, 2.2, -0.6)
    a.at(44, body=Z0, pelvis=Z0, neck=Z0, head=Z0, jaw=Z0).arms(44).legs(44)
    a.wings(0).wings(12, beat=-20, fold=24).wings(15, beat=40, sweep=10, spread=20).wings(18, beat=-30, spread=20)
    a.wings(22, beat=20, spread=16).wings(24, beat=44, sweep=-10, spread=14).wings(30, beat=10).wings(44)
    a.claws(0).claws(12, -10).claws(15, -40).claws(24, 40).claws(44)
    a.tail([(0, 0, 0), (12, 14, 0), (15, -18, 0), (20, 10, 0), (24, 20, 0), (32, -4, 0), (44, 0, 0)], lag=1)
    a.sec([(0, 0, 0), (12, -8, 0), (15, -20, 0), (20, 10, 0), (24, 22, 0), (32, -6, 0), (44, 0, 0)])
    a.done()

    # ---------------- scribble (44): hunches, claws high 0-14, frantic alternating rakes into the floor 16-34 (every 2 ticks)
    a = mk("scribble", 44)
    a.at(0, body=Z0)
    a.at(12, body=(-14, 0, 0), neck=(-14, 0, 0), head=(-20, 0, 0), jaw=(-40, 0, 0))
    a.arms(12, r=(-110, 0, 20), l=(-110, 0, 20), fr=(-40, 0, 0), fl=(-40, 0, 0))
    a.claws(12, -40)
    for i, t in enumerate(range(16, 36, 2)):
        s = 1 if i % 2 == 0 else -1
        k, o = ("r", "l") if s > 0 else ("l", "r")
        a.at(t, body=(10, 8 * s, 4 * s), neck=(14, 0, 0), head=(16, -10 * s, 8 * s), jaw=(-30 - 10 * (i % 3), 0, 0))
        a.at(t, **{"arm_" + k: (56, 0, -8 * s), "fore_" + k: (-20, 0, 0), "arm_" + o: (-60, 0, 14 * -s), "fore_" + o: (-40, 0, 0)})
        a.claws(t, 40, k).claws(t, -30, o)
    a.at(40, body=(2, 0, 0), neck=(2, 0, 0), head=(4, 0, 0), jaw=(-10, 0, 0)).arms(40, r=(10, 0, 0), l=(10, 0, 0))
    a.at(44, body=Z0, neck=Z0, head=Z0, jaw=Z0).arms(44).claws(44)
    a.legs(0).legs(12, 0.6, 1).legs(16, 1.8, -1).legs(34, 1.8, -1).legs(44)
    a.wings(0).wings(12, beat=-24, spread=16)
    for i, t in enumerate(range(16, 36, 4)):
        a.wings(t, beat=8, fold=10).wings(t + 2, beat=-6, spread=8)
    a.wings(44)
    a.tail([(0, 0, 0), (12, 16, 0)] + [(t, 10, 16 * (1 if (t // 2) % 2 == 0 else -1)) for t in range(16, 36, 2)] + [(44, 0, 0)], lag=1)
    a.sec([(0, 0, 0), (12, -10, 0)] + [(t, 6, 8 * (1 if (t // 2) % 2 == 0 else -1)) for t in range(16, 36, 2)] + [(44, 0, 0)], delay=1)
    a.done()

    # ---------------- ink_spit (40): head rears back, throat swells 0-14, three spits 16/20/24 (head snaps), recover
    a = mk("ink_spit", 40)
    a.at(0, body=Z0, neck=Z0, head=Z0, jaw=Z0)
    a.at(12, body=(-14, 0, 0), neck=(-30, 0, 0), head=(-24, 0, 0), jaw=(-8, 0, 0))
    a.scl("neck", (0, 1, 1, 1), (10, 1.3, 1.2, 1.1), (14, 1.45, 1.3, 1.1), (16, 1, 1, 1), (18, 1.3, 1.15, 1.05), (20, 1, 1, 1),
          (22, 1.25, 1.1, 1.05), (24, 1, 1, 1), (40, 1, 1, 1))
    for t, yaw in ((16, -10), (20, 0), (24, 10)):
        a.at(t - 2, neck=(-16, 0, 0), head=(-16, yaw, 0), jaw=(-10, 0, 0), body=(-8, 0, 0))
        a.at(t, neck=(18, 0, 0), head=(18, yaw, 0), jaw=(-60, 0, 0), body=(8, yaw * 0.6, 0))
    a.at(30, neck=(6, 0, 0), head=(4, 0, 0), jaw=(-20, 0, 0), body=(2, 0, 0))
    a.at(40, body=Z0, neck=Z0, head=Z0, jaw=Z0)
    a.legs(0).legs(12, -0.4, 1).legs(16, 0.8, -0.6).legs(24, 1.0, -0.8).legs(40)
    a.arms(0).arms(12, r=(-14, 0, 6), l=(-14, 0, 6)).arms(16, r=(10, 0, 0), l=(10, 0, 0)).arms(40)
    a.wings(0).wings(12, beat=-20, spread=12).wings(16, beat=14).wings(18, beat=-4).wings(20, beat=14).wings(22, beat=-4).wings(24, beat=14).wings(40)
    a.claws(0).claws(12, 20).claws(40)
    a.tail([(0, 0, 0), (12, -10, 0), (16, 10, 0), (20, 10, 0), (24, 10, 0), (40, 0, 0)])
    a.sec([(0, 0, 0), (12, -12, 0), (16, 12, 0), (18, -4, 0), (20, 12, 0), (22, -4, 0), (24, 12, 0), (32, 0, 0), (40, 0, 0)], delay=1)
    a.done()

    # ---------------- roar (44): rears up + wings flare 0-12, ROAR 14 (jaw max, mane bristles), shudder 14-30, drop
    a = mk("roar", 44)
    a.at(0, body=Z0, pelvis=Z0)
    a.at(10, pelvis=(-12, 0, 0), body=(-20, 0, 0), neck=(-16, 0, 0), head=(-24, 0, 0), jaw=(-10, 0, 0))
    a.arms(10, r=(-50, 0, 30), l=(-50, 0, 30), fr=(30, 0, 0), fl=(30, 0, 0))
    a.claws(10, -40)
    for t, j in ((14, 0), (17, 1), (20, -1), (23, 1), (26, -1), (29, 1), (32, 0)):
        a.at(t, pelvis=(-14, 0, 0), body=(-24 + 2 * j, 2 * j, 2 * j), neck=(22, 0, 0), head=(20 + 3 * j, 4 * j, 4 * j), jaw=(-80 - 6 * j, 0, 0))
        a.arms(t, r=(-40, 0, 46 + 4 * j), l=(-40, 0, 46 - 4 * j), fr=(20, 0, 0), fl=(20, 0, 0))
        a.wings(t, beat=-14 + 6 * j, spread=30, sweep=-10)
    a.scl("mane_t", (0, 1, 1, 1), (12, 1, 1, 1), (14, 1.25, 1.35, 1.25), (32, 1.25, 1.35, 1.25), (38, 1, 1, 1), (44, 1, 1, 1))
    a.scl("mane_b", (0, 1, 1, 1), (12, 1, 1, 1), (14, 1.25, 1.35, 1.25), (32, 1.25, 1.35, 1.25), (38, 1, 1, 1), (44, 1, 1, 1))
    a.scl("spines", (0, 1, 1, 1), (12, 1, 1, 1), (14, 1.15, 1.3, 1.1), (32, 1.15, 1.3, 1.1), (38, 1, 1, 1), (44, 1, 1, 1))
    a.at(38, pelvis=(-2, 0, 0), body=(6, 0, 0), neck=(4, 0, 0), head=(0, 0, 0), jaw=(-20, 0, 0)).arms(38, r=(14, 0, 0), l=(14, 0, 0))
    a.at(44, pelvis=Z0, body=Z0, neck=Z0, head=Z0, jaw=Z0).arms(44).claws(44)
    a.legs(0).legs(10, -0.4, 1.4).legs(14, 0.6, 1.4).legs(32, 0.6, 1.4).legs(38, 1.0).legs(44)
    a.wings(0).wings(10, beat=-30, spread=24).wings(38, beat=6).wings(44)
    a.tail([(0, 0, 0), (10, 16, 0), (14, 26, 0), (20, 22, 6), (26, 26, -6), (32, 22, 0), (38, 0, 0), (44, 0, 0)], lag=1)
    a.sec([(0, 0, 0), (10, -14, 0), (14, 12, 0), (17, 6, 6), (20, 10, -6), (23, 6, 6), (26, 10, -6), (32, 4, 0), (38, -6, 0), (44, 0, 0)], delay=1)
    a.done()

    # ---------------- frenzy (56): three savage lunges (10 / 24 / 38) with gnashing bites + rakes in between, then pant
    a = mk("frenzy", 56)
    a.at(0, body=Z0, P_root=Z0)
    for n, t0 in enumerate((10, 24, 38)):
        s = 1 if n % 2 == 0 else -1
        a.at(t0 - 4, body=(10, 14 * s, 0), neck=(-20, 0, 0), head=(-20, -10 * s, 0), jaw=(-60, 0, 0), P_root=(0, 0, 1))
        a.arms(t0 - 4, r=(-40, 0, 10), l=(-40, 0, 10), fr=(30, 0, 0), fl=(30, 0, 0))
        a.legs(t0 - 4, 2.0, 1.4)
        a.at(t0, body=(-18, -10 * s, 0), neck=(24, 0, 0), head=(16, 12 * s, 10 * s), jaw=(-60, 0, 0), P_root=(0, 0, -3))
        a.arms(t0, r=(70, 0, -10), l=(70, 0, -10), fr=(-30, 0, 0), fl=(-30, 0, 0))
        a.legs(t0, 0.4, -2.4)
        a.at(t0 + 2, jaw=(26, 0, 0), head=(20, 6 * s, 14 * s))
        k, o = ("r", "l") if s > 0 else ("l", "r")
        a.at(t0 + 5, body=(-6, 20 * s, 6 * s), head=(10, -20 * s, -10 * s), jaw=(-40, 0, 0),
             **{"arm_" + k: (40, 0, -36 * s), "fore_" + k: (-10, 0, 0), "arm_" + o: (-20, 0, 0)})
        a.at(t0 + 7, jaw=(20, 0, 0))
        a.legs(t0 + 6, 1.0, -1)
        a.wings(t0 - 4, beat=-24, spread=20).wings(t0, beat=36, sweep=-10, spread=16).wings(t0 + 6, beat=-10)
        a.claws(t0 - 4, -30).claws(t0, 30).claws(t0 + 5, 40, k)
    a.at(48, body=(8, 0, 0), neck=(-6, 0, 0), head=(-4, 0, 0), jaw=(-30, 0, 0), P_root=Z0).arms(48, r=(6, 0, 0), l=(6, 0, 0)).legs(48, 1.0)
    for t, j in ((50, 1), (52, 0), (54, 1)):
        a.at(t, body=(8 - 4 * j, 0, 0), jaw=(-30 + 14 * j, 0, 0))
    a.at(56, body=Z0, neck=Z0, head=Z0, jaw=Z0, P_root=Z0).arms(56).legs(0).legs(56).wings(0).wings(56).claws(0).claws(56)
    a.tail([(0, 0, 0)] + [(t0 + d, v, sw) for t0 in (10, 24, 38) for (d, v, sw) in ((-4, 14, 0), (0, -10, 0), (5, 4, 20 if t0 != 24 else -20))] + [(56, 0, 0)], lag=1)
    a.sec([(0, 0, 0)] + [(t0 + d, v, sw) for t0 in (10, 24, 38) for (d, v, sw) in ((-4, -12, 0), (0, 16, 0), (5, 4, 10 if t0 != 24 else -10))] + [(56, 0, 0)], delay=1)
    a.done()

    # ---------------- tail_stab (34): tail coils over the back like a scorpion 0-13, STAB over the head at 16, hold, retract
    a = mk("tail_stab", 34)
    a.at(0, body=Z0, pelvis=Z0)
    a.at(12, pelvis=(10, 0, 0), body=(-6, 0, 0), neck=(-10, 0, 0), head=(-8, 0, 0), jaw=(-26, 0, 0))
    a.at(12, tail0=(-70, 0, 0), tail1=(-50, 0, 0), tail2=(-40, 0, 0), tail3=(-40, 0, 0), tail4=(-30, 0, 0))
    a.at(14, tail0=(-76, 0, 0), tail1=(-56, 0, 0), tail2=(-44, 0, 0), tail3=(-44, 0, 0), tail4=(-34, 0, 0))
    a.at(16, pelvis=(-6, 0, 0), body=(10, 0, 0), neck=(14, 0, 0), head=(8, 0, 0), jaw=(-50, 0, 0), P_root=(0, 0, -1.5))
    a.at(16, tail0=(-128, 0, 0), tail1=(-50, 0, 0), tail2=(-20, 0, 0), tail3=(4, 0, 0), tail4=(10, 0, 0))
    a.at(20, tail0=(-124, 0, 0), tail1=(-46, 0, 0), tail2=(-18, 0, 0), tail3=(8, 0, 0), tail4=(14, 0, 0))
    a.at(23, tail0=(-100, 0, 0), tail1=(-52, 0, 0), tail2=(-30, 0, 0), tail3=(-10, 0, 0), tail4=(-4, 0, 0), jaw=(-30, 0, 0))
    a.at(28, tail0=(-40, 0, 0), tail1=(-20, 0, 0), tail2=(-10, 0, 0), tail3=(-6, 0, 0), tail4=(0, 0, 0), pelvis=(2, 0, 0), body=(2, 0, 0))
    a.at(34, tail0=Z0, tail1=Z0, tail2=Z0, tail3=Z0, tail4=Z0, pelvis=Z0, body=Z0, neck=Z0, head=Z0, jaw=Z0, P_root=Z0)
    a.legs(0).legs(12, 1.6, 1).legs(16, 1.2, -1).legs(23, 1.2, -1).legs(34)
    a.arms(0).arms(12, r=(-10, 0, 10), l=(-10, 0, 10), fr=(20, 0, 0), fl=(20, 0, 0)).arms(16, r=(16, 0, 6), l=(16, 0, 6)).arms(34)
    a.wings(0).wings(12, beat=20, sweep=-10, spread=10).wings(16, beat=34, sweep=-20, spread=14).wings(24, beat=10).wings(34)
    a.claws(0).claws(12, -20).claws(16, 30).claws(34)
    a.sec([(0, 0, 0), (12, -10, 0), (16, 14, 0), (23, 4, 0), (34, 0, 0)], delay=1)
    a.done()

    # ---------------- wing_gust (42): wings rise high 0-12, BEAT 16, recover-rise 22, BEAT 26, settle
    a = mk("wing_gust", 42)
    a.at(0, body=Z0, pelvis=Z0, P_root=Z0)
    a.at(12, pelvis=(-10, 0, 0), body=(-14, 0, 0), neck=(-10, 0, 0), head=(-14, 0, 0), jaw=(-20, 0, 0), P_root=(0, 0.6, 0))
    a.arms(12, r=(-30, 0, 20), l=(-30, 0, 20), fr=(20, 0, 0), fl=(20, 0, 0))
    for tb, tr in ((16, 22), (26, 32)):
        a.at(tb, pelvis=(-14, 0, 0), body=(-4, 0, 0), neck=(16, 0, 0), head=(14, 0, 0), jaw=(-50, 0, 0), P_root=(0, 2.0, 0))
        a.arms(tb, r=(-10, 0, 40), l=(-10, 0, 40), fr=(-10, 0, 0), fl=(-10, 0, 0))
        a.wings(tb - 4, beat=-50, sweep=-14, spread=26).wings(tb, beat=58, sweep=-34, spread=26).wings(tb + 2, beat=62, sweep=-30, spread=20, fold=10)
        a.at(tr, pelvis=(-10, 0, 0), body=(-12, 0, 0), neck=(-6, 0, 0), head=(-8, 0, 0), jaw=(-20, 0, 0), P_root=(0, 0.6, 0))
    a.wings(0).wings(36, beat=-6, spread=6).wings(42)
    a.at(42, pelvis=Z0, body=Z0, neck=Z0, head=Z0, jaw=Z0, P_root=Z0).arms(42)
    a.legs(0).legs(12, 1.2, 1.0).legs(16, -0.4, 1.4).legs(22, 1.0, 1.0).legs(26, -0.4, 1.4).legs(34, 1.0).legs(42)
    a.claws(0).claws(12, -20).claws(16, 20).claws(26, 20).claws(42)
    a.tail([(0, 0, 0), (12, 16, 0), (16, -12, 0), (22, 14, 0), (26, -12, 0), (34, 4, 0), (42, 0, 0)], lag=1)
    a.sec([(0, 0, 0), (12, -14, 0), (16, 16, 0), (22, -10, 0), (26, 16, 0), (34, -4, 0), (42, 0, 0)], delay=1)
    a.done()

    # ---------------- ink_tendrils (46): rears 0-10, SLAMS both claws into the floor at 14, pumps ink 16-30 (tendrils 18/22/26), tears free
    a = mk("ink_tendrils", 46)
    a.at(0, body=Z0, pelvis=Z0)
    a.at(10, pelvis=(-16, 0, 0), body=(-24, 0, 0), neck=(-10, 0, 0), head=(-16, 0, 0), jaw=(-30, 0, 0))
    a.arms(10, r=(-150, 0, 14), l=(-150, 0, 14), fr=(-30, 0, 0), fl=(-30, 0, 0))
    a.claws(10, -40)
    a.at(14, pelvis=(6, 0, 0), body=(16, 0, 0), neck=(16, 0, 0), head=(14, 0, 0), jaw=(-64, 0, 0), P_root=(0, -0.5, 0))
    a.arms(14, r=(54, 0, -4), l=(54, 0, -4), fr=(-10, 0, 0), fl=(-10, 0, 0), hr=(40, 0, 0), hl=(40, 0, 0))
    a.claws(14, 60)
    for t, j in ((17, 1), (20, -1), (23, 1), (26, -1), (29, 1)):
        a.at(t, body=(14 + 2 * j, 2 * j, 2 * j), neck=(14, 0, 0), head=(12 + 3 * j, 6 * j, 0), jaw=(-60 + 8 * j, 0, 0), P_root=(0, -0.5 - 0.3 * j, 0))
        a.arms(t, r=(52 + 3 * j, 0, -4), l=(52 - 3 * j, 0, -4), fr=(-10, 0, 0), fl=(-10, 0, 0), hr=(40, 0, 0), hl=(40, 0, 0))
    a.at(34, pelvis=(-6, 0, 0), body=(-10, 0, 0), neck=(-6, 0, 0), head=(-6, 0, 0), jaw=(-20, 0, 0), P_root=Z0)
    a.arms(34, r=(-40, 0, 10), l=(-40, 0, 10), fr=(20, 0, 0), fl=(20, 0, 0))
    a.claws(34, -20)
    a.at(46, pelvis=Z0, body=Z0, neck=Z0, head=Z0, jaw=Z0).arms(46).claws(46)
    a.legs(0).legs(10, -0.4, 1.4).legs(14, 1.8, -1).legs(30, 1.8, -1).legs(34, 0.6).legs(46)
    a.wings(0).wings(10, beat=-30, spread=24).wings(14, beat=40, sweep=-10, spread=20).wings(30, beat=30, spread=16).wings(36, beat=-6).wings(46)
    a.tail([(0, 0, 0), (10, 14, 0), (14, -14, 0), (20, -10, 10), (26, -10, -10), (34, 6, 0), (46, 0, 0)], lag=1)
    a.sec([(0, 0, 0), (10, -14, 0), (14, 18, 0), (20, 8, 4), (26, 8, -4), (34, -6, 0), (46, 0, 0)], delay=1)
    a.done()

    # ---------------- dive_bomb (60): coil 0-10, LAUNCH 12 (wing beat), rise flapping 12-20, NOSE-DIVE 20 (wings swept back),
    #                  impact ~24-28 (wings slam open, crater), slow recovery
    a = mk("dive_bomb", 60)
    a.at(0, body=Z0, pelvis=Z0, P_root=Z0, root=Z0)
    a.at(10, body=(6, 0, 0), neck=(-14, 0, 0), head=(-16, 0, 0), jaw=(-20, 0, 0))
    a.arms(10, r=(-20, 0, 0), l=(-20, 0, 0), fr=(40, 0, 0), fl=(40, 0, 0))
    a.legs(10, 3.4, 1.4)
    a.wings(0).wings(10, beat=-50, spread=26, sweep=-10)
    a.at(12, root=(-30, 0, 0), body=(10, 0, 0), neck=(-10, 0, 0), head=(-20, 0, 0), jaw=(-50, 0, 0), P_root=(0, 3, 0))
    a.arms(12, r=(-40, 0, 20), l=(-40, 0, 20), fr=(-10, 0, 0), fl=(-10, 0, 0))
    a.legs(12, -0.6, 0, r=(-50, 40, -30, 30), l=(-50, 40, -30, 30))
    a.wings(12, beat=64, sweep=-30, spread=26)
    for t, j in ((14, 0), (16, 1), (18, 0)):
        a.wings(t, beat=-50 if j == 0 else 60, spread=26, sweep=-14)
        a.at(t, P_root=(0, 4 + j, 0))
    a.at(18, root=(-24, 0, 0))
    a.legs(18, 0, 0, r=(30, -50, 30, 10), l=(30, -50, 30, 10))
    a.at(20, root=(40, 0, 0), body=(-6, 0, 0), neck=(20, 0, 0), head=(16, 0, 0), jaw=(-70, 0, 0), P_root=(0, 5, 0))
    a.arms(20, r=(110, 0, -10), l=(110, 0, -10), fr=(-30, 0, 0), fl=(-30, 0, 0), hr=(-20, 0, 0), hl=(-20, 0, 0))
    a.legs(20, 0, 0, r=(-60, 40, -30, 20), l=(-60, 40, -30, 20))
    a.wings(20, beat=-14, sweep=60, fold=40)
    a.at(23, root=(46, 0, 0), P_root=(0, 3, 0)).wings(23, beat=-10, sweep=66, fold=44)
    a.at(26, root=(0, 0, 0), body=(-20, 0, 0), pelvis=(6, 0, 0), neck=(16, 0, 0), head=(14, 0, 0), jaw=(-20, 0, 0), P_root=(0, -1.5, 0))
    a.arms(26, r=(50, 0, -40), l=(50, 0, -40), fr=(-30, 0, 0), fl=(-30, 0, 0), hr=(30, 0, 0), hl=(30, 0, 0))
    a.legs(26, 3.6, -1)
    a.wings(26, beat=60, sweep=-20, spread=26)
    a.scl("spines", (0, 1, 1, 1), (24, 1, 1, 1), (26, 1.2, 1.35, 1.1), (36, 1.2, 1.35, 1.1), (44, 1, 1, 1), (60, 1, 1, 1))
    a.at(32, body=(-14, 0, 0), pelvis=(4, 0, 0), head=(-10, 0, 0), jaw=(-70, 0, 0), P_root=(0, -1, 0))
    a.wings(32, beat=40, spread=20).legs(32, 3.0, -0.6)
    a.at(44, body=(-4, 0, 0), pelvis=(0, 0, 0), neck=(0, 0, 0), head=(0, 0, 0), jaw=(-16, 0, 0), P_root=Z0)
    a.arms(44, r=(16, 0, -10), l=(16, 0, -10)).legs(44, 1.0).wings(44, beat=10)
    a.at(60, body=Z0, pelvis=Z0, neck=Z0, head=Z0, jaw=Z0, root=Z0, P_root=Z0).arms(60).legs(60).wings(60)
    a.claws(0).claws(10, -10).claws(20, -40).claws(26, 50).claws(44, 10).claws(60)
    a.tail([(0, 0, 0), (10, 14, 0), (12, -24, 0), (18, -10, 0), (20, 24, 0), (26, 30, 0), (32, -6, 0), (44, 0, 0), (60, 0, 0)], lag=1)
    a.sec([(0, 0, 0), (10, -8, 0), (12, -20, 0), (18, -10, 0), (20, 16, 0), (26, 24, 0), (32, -8, 0), (44, 0, 0), (60, 0, 0)])
    a.done()

    # ---------------- sky_snatch (64): coil 0-7, LUNGE 9, jaws + claws SNATCH 10, hug 12, wing-beat LIFTOFF 14, flaps 21/28 carrying the
    #                  victim (bites 22/30 = head shakes), wings fold 34, NOSE-DIVE 36, IMPACT ~40 (lets go), rise
    a = mk("sky_snatch", 64)
    HUG = dict(r=(52, 0, -18), l=(52, 0, -18), fr=(-62, 0, -10), fl=(-62, 0, -10), hr=(30, 0, 0), hl=(30, 0, 0))
    a.at(0, body=Z0, pelvis=Z0, neck=Z0, head=Z0, jaw=Z0, root=Z0, P_root=Z0)
    a.at(7, body=(8, 0, 0), pelvis=(6, 0, 0), neck=(-18, 0, 0), head=(-16, 0, 0), jaw=(-36, 0, 0))
    a.arms(7, r=(-24, 0, 10), l=(-24, 0, 10), fr=(34, 0, 0), fl=(34, 0, 0))
    a.legs(0).legs(7, 2.6, 1.6)
    a.at(9, body=(-16, 0, 0), pelvis=(-6, 0, 0), neck=(26, 0, 0), head=(14, 0, 0), jaw=(-60, 0, 0), P_root=(0, 0, -2))
    a.arms(9, r=(84, 0, 14), l=(84, 0, 14), fr=(-14, 0, 0), fl=(-14, 0, 0), hr=(-30, 0, 0), hl=(-30, 0, 0))
    a.legs(9, 0.2, -2.0)
    a.at(10, jaw=(22, 0, 0), head=(18, 0, 0)).arms(10, **HUG)
    a.at(12, body=(-8, 0, 0), pelvis=(-4, 0, 0), neck=(-4, 0, 0), head=(-8, 0, 0), jaw=(14, 0, 0), P_root=(0, 0, -1.5)).arms(12, **HUG)
    a.legs(12, 2.4, 1.0)
    a.at(14, root=(-16, 0, 0), body=(-12, 0, 0), pelvis=(-10, 0, 0), neck=(-8, 0, 0), head=(-10, 0, 0), jaw=(16, 0, 0), P_root=(0, 1.5, 0))
    a.legs(14, -0.4, 0, r=(-50, 40, -30, 30), l=(-50, 40, -30, 30))
    for t in (16, 20, 24, 28, 32):
        a.arms(t, **HUG)
    for t, y in ((18, 2.5), (21, 2.0), (25, 2.6), (28, 2.0), (32, 2.6)):
        a.at(t, P_root=(0, y, 0))
    a.at(20, root=(-10, 0, 0), body=(-10, 0, 0), neck=(-10, 0, 0), head=(-14, 0, 0), jaw=(10, 0, 0))
    for tb, j in ((22, 1), (30, -1)):  # bites while airborne: jaw re-clamps, head worries the prey side to side
        a.at(tb - 1, head=(-18, 0, 0), jaw=(-26, 0, 0))
        a.at(tb, head=(14, 16 * j, 14 * j), neck=(10, 8 * j, 0), jaw=(24, 0, 0))
        a.at(tb + 2, head=(10, -14 * j, -12 * j), neck=(6, -6 * j, 0), jaw=(18, 0, 0))
        a.at(tb + 4, head=(-10, 0, 0), neck=(-8, 0, 0), jaw=(12, 0, 0))
    a.legs(20, 0, 0, r=(30, -50, 30, 10), l=(30, -50, 30, 10)).legs(32, 0, 0, r=(24, -44, 26, 10), l=(24, -44, 26, 10))
    a.wings(0).wings(7, beat=-40, spread=24, sweep=-8).wings(10, beat=-46, spread=26)
    a.wings(14, beat=66, sweep=-24, spread=26)
    for tu, td in ((18, 21), (25, 28)):
        a.wings(tu, beat=-48, spread=26, sweep=-12).wings(td, beat=62, sweep=-20, spread=26)
    a.wings(32, beat=-36, spread=22)
    a.at(34, root=(14, 0, 0), body=(-4, 0, 0), neck=(10, 0, 0), head=(6, 0, 0), jaw=(16, 0, 0), P_root=(0, 2.6, 0))
    a.wings(34, beat=-20, sweep=40, fold=24)
    a.at(36, root=(40, 0, 0), neck=(18, 0, 0), head=(14, 0, 0), P_root=(0, 4.5, 0)).arms(36, **HUG)
    a.wings(36, beat=-12, sweep=64, fold=44).wings(39, beat=-10, sweep=68, fold=46)
    a.legs(36, 0, 0, r=(-64, 40, -30, 24), l=(-64, 40, -30, 24))
    a.at(39, root=(44, 0, 0), P_root=(0, 3.5, 0), jaw=(16, 0, 0)).arms(39, **HUG)
    a.at(41, root=Z0, body=(-20, 0, 0), pelvis=(6, 0, 0), neck=(18, 0, 0), head=(14, 0, 0), jaw=(-64, 0, 0), P_root=(0, -1.6, 0))
    a.arms(41, r=(72, 0, -30), l=(72, 0, -30), fr=(-26, 0, 0), fl=(-26, 0, 0), hr=(36, 0, 0), hl=(36, 0, 0))
    a.legs(41, 3.6, -1)
    a.wings(41, beat=62, sweep=-22, spread=26)
    a.scl("spines", (0, 1, 1, 1), (39, 1, 1, 1), (41, 1.2, 1.35, 1.1), (50, 1.2, 1.35, 1.1), (56, 1, 1, 1), (64, 1, 1, 1))
    a.at(48, body=(-10, 0, 0), pelvis=(2, 0, 0), neck=(-4, 0, 0), head=(-12, 0, 0), jaw=(-50, 0, 0), P_root=(0, -0.8, 0))
    a.arms(48, r=(30, 0, -14), l=(30, 0, -14), fr=(-10, 0, 0), fl=(-10, 0, 0)).legs(48, 2.4, -0.4).wings(48, beat=30, spread=16)
    a.at(64, body=Z0, pelvis=Z0, neck=Z0, head=Z0, jaw=Z0, root=Z0, P_root=Z0).arms(64).legs(64).wings(64)
    a.claws(0).claws(7, -20).claws(9, -50).claws(10, 60).claws(36, 60).claws(41, -30).claws(48, 10).claws(64)
    a.tail([(0, 0, 0), (7, 14, 0), (9, -14, 0), (14, -26, 0), (18, -14, 8), (21, -22, -8), (25, -14, 8), (28, -22, -8),
            (34, 10, 0), (36, 28, 0), (41, -10, 0), (46, 16, 0), (54, 0, 0), (64, 0, 0)], lag=1)
    a.sec([(0, 0, 0), (7, -10, 0), (9, 14, 0), (14, -18, 0), (18, -8, 4), (21, -14, -4), (25, -8, 4), (28, -14, -4),
           (36, 22, 0), (41, 26, 0), (48, -6, 0), (64, 0, 0)], delay=1)
    a.done()

    # ---------------- wing_pin (52): rears + wings high 0-7, HOP 8, both claws SLAM the victim down 11, wings wrap it 14,
    #                  gnaws 20/28/36 (head snaps down), rake + release 44, refold
    a = mk("wing_pin", 52)
    PIN = dict(r=(64, 0, -8), l=(64, 0, -8), fr=(-12, 0, 0), fl=(-12, 0, 0), hr=(44, 0, 0), hl=(44, 0, 0))
    a.at(0, body=Z0, pelvis=Z0, neck=Z0, head=Z0, jaw=Z0, P_root=Z0)
    a.at(6, pelvis=(-14, 0, 0), body=(-20, 0, 0), neck=(-8, 0, 0), head=(-14, 0, 0), jaw=(-40, 0, 0))
    a.arms(6, r=(-120, 0, 24), l=(-120, 0, 24), fr=(-36, 0, 0), fl=(-36, 0, 0))
    a.legs(0).legs(6, 1.6, 1.4)
    a.at(9, pelvis=(-10, 0, 0), body=(-14, 0, 0), P_root=(0, 2.0, -1.5))
    a.arms(9, r=(-90, 0, 14), l=(-90, 0, 14), fr=(-30, 0, 0), fl=(-30, 0, 0))
    a.legs(9, -0.4, 0, r=(-30, 30, -20, 10), l=(-30, 30, -20, 10))
    a.at(11, pelvis=(8, 0, 0), body=(20, 0, 0), neck=(14, 0, 0), head=(12, 0, 0), jaw=(-56, 0, 0), P_root=(0, -1.0, -2))
    a.arms(11, r=(70, 0, -10), l=(70, 0, -10), fr=(-8, 0, 0), fl=(-8, 0, 0), hr=(50, 0, 0), hl=(50, 0, 0))
    a.legs(11, 2.4, -1.4)
    a.at(14, pelvis=(6, 0, 0), body=(16, 0, 0), neck=(8, 0, 0), head=(6, 0, 0), jaw=(-30, 0, 0), P_root=(0, -0.8, -2)).arms(14, **PIN)
    for tb, j in ((20, 1), (28, -1), (36, 1)):
        a.at(tb - 3, body=(12, 0, 0), neck=(-12, 0, 0), head=(-18, 0, 0), jaw=(-62, 0, 0))
        a.at(tb, body=(22, 4 * j, 0), neck=(28, 0, 0), head=(26, 8 * j, 0), jaw=(18, 0, 0), P_root=(0, -1.2, -2))
        a.at(tb + 2, neck=(24, 10 * j, 0), head=(22, -18 * j, -16 * j), jaw=(14, 0, 0))
        a.at(tb + 4, body=(16, 0, 0), neck=(8, 0, 0), head=(6, 0, 0), jaw=(-24, 0, 0), P_root=(0, -0.8, -2))
        a.arms(tb, r=(68, 0, -8), l=(68, 0, -8), fr=(-16, 0, 0), fl=(-16, 0, 0), hr=(52, 0, 0), hl=(52, 0, 0)).arms(tb + 4, **PIN)
    a.legs(14, 2.2, -1.4).legs(40, 2.2, -1.4)
    a.arms(40, **PIN)
    a.at(41, body=(12, -16, 0), head=(4, 16, 0), jaw=(-40, 0, 0))
    a.arms(41, r=(30, 0, 24), l=(64, 0, -8), fr=(-30, 0, 0))
    a.at(44, body=(10, 26, 6), neck=(4, 0, 0), head=(0, -20, 0), jaw=(-50, 0, 0), P_root=(0, 0, -1))
    a.arms(44, r=(66, 0, -50), l=(20, 0, 0), fr=(-6, 0, 0), fl=(-10, 0, 0))
    a.claws(44, 50, "r")
    a.at(52, body=Z0, pelvis=Z0, neck=Z0, head=Z0, jaw=Z0, P_root=Z0).arms(52).legs(52)
    a.wings(0).wings(6, beat=-44, spread=26, sweep=-10).wings(9, beat=-30, spread=24)
    a.wings(11, beat=40, sweep=-30, spread=20).wings(14, beat=58, sweep=-60, fold=18)
    for tb in (20, 28, 36):
        a.wings(tb, beat=62, sweep=-64, fold=22).wings(tb + 4, beat=56, sweep=-58, fold=16)
    a.wings(41, beat=56, sweep=-58, fold=16).wings(44, beat=-20, spread=20).wings(52)
    a.claws(0).claws(6, -40).claws(11, 60).claws(40, 60).claws(41, -30, "r").claws(52)
    a.tail([(0, 0, 0), (6, 18, 0), (11, -8, 0), (14, 10, 10), (22, 12, -10), (30, 12, 10), (38, 12, -10), (44, 0, -24), (52, 0, 0)], lag=1)
    a.sec([(0, 0, 0), (6, -14, 0), (11, 18, 0), (14, 10, 0)] + [(tb + d, v, 0) for tb in (20, 28, 36) for (d, v) in ((-3, -8), (0, 14))]
          + [(44, 6, 12), (52, 0, 0)], delay=1)
    a.done()

    # ---------------- tail_lasso (48): tail coils high over the back 0-11, LASHES straight out over the head 13 (snare), reels the
    #                  victim in 14-24 (tail curls back up, body braces), squeezes it overhead 26-30, SLAMS it down in front 36, recovers
    a = mk("tail_lasso", 48)
    TL = ("tail0", "tail1", "tail2", "tail3", "tail4")

    def tl(t, *v):
        a.at(t, **{n: (x, 0, 0) for n, x in zip(TL, v)})
    a.at(0, body=Z0, pelvis=Z0, neck=Z0, head=Z0, jaw=Z0, P_root=Z0)
    tl(0, 0, 0, 0, 0, 0)
    tl(6, -50, -30, -30, -30, -30)
    tl(11, -80, -60, -48, -46, -36)
    a.at(11, pelvis=(10, 0, 0), body=(-8, 0, 0), neck=(-14, 0, 0), head=(-10, 0, 0), jaw=(-30, 0, 0))
    a.arms(11, r=(-10, 0, 12), l=(-10, 0, 12), fr=(20, 0, 0), fl=(20, 0, 0))
    tl(13, -132, -40, -12, 6, 12)
    a.at(13, pelvis=(-6, 0, 0), body=(12, 0, 0), neck=(14, 0, 0), head=(10, 0, 0), jaw=(-56, 0, 0), P_root=(0, 0, -1.5))
    a.arms(13, r=(20, 0, 6), l=(20, 0, 6))
    tl(15, -128, -36, -8, 16, 30)  # tip whips around the victim
    tl(19, -118, -50, -30, -10, 10)
    a.at(19, pelvis=(14, 0, 0), body=(-14, 0, 0), neck=(-12, 0, 0), head=(-18, 0, 0), jaw=(-40, 0, 0), P_root=(0, 0, 1.0))
    a.arms(19, r=(-34, 0, 16), l=(-34, 0, 16), fr=(46, 0, 0), fl=(46, 0, 0), hr=(-20, 0, 0), hl=(-20, 0, 0))
    tl(24, -104, -66, -44, -24, 0)
    a.at(24, pelvis=(8, 0, 0), body=(-16, 0, 0), neck=(-22, 0, 0), head=(-26, 0, 0), jaw=(-20, 0, 0), P_root=(0, 0, 0.5))
    a.arms(24, r=(-50, 0, 30), l=(-50, 0, 30), fr=(30, 0, 0), fl=(30, 0, 0))
    for t, j in ((26, 1), (28, -1), (30, 1), (32, 0)):  # squeeze: coil tightens in pulses, jaw roars at the trapped prey
        tl(t, -104 - 4 * j, -66 - 6 * j, -44 - 8 * j, -28 - 10 * j, -4 - 8 * j)
        a.at(t, jaw=(-60 - 10 * abs(j), 0, 0), head=(-28, 6 * j, 6 * j))
    tl(34, -96, -76, -52, -36, -16)
    a.at(34, pelvis=(10, 0, 0), body=(-20, 0, 0), neck=(-18, 0, 0), head=(-20, 0, 0), jaw=(-30, 0, 0))
    tl(36, -150, -44, 24, 44, 40)
    a.at(36, pelvis=(-8, 0, 0), body=(16, 0, 0), neck=(18, 0, 0), head=(14, 0, 0), jaw=(-66, 0, 0), P_root=(0, -0.5, -1))
    a.arms(36, r=(40, 0, -16), l=(40, 0, -16), fr=(-20, 0, 0), fl=(-20, 0, 0), hr=(30, 0, 0), hl=(30, 0, 0))
    tl(39, -146, -40, 28, 48, 44)
    tl(42, -70, -30, -10, 0, 0)
    a.at(42, pelvis=(2, 0, 0), body=(4, 0, 0), neck=(4, 0, 0), head=(2, 0, 0), jaw=(-20, 0, 0), P_root=Z0).arms(42, r=(10, 0, 0), l=(10, 0, 0))
    tl(48, 0, 0, 0, 0, 0)
    a.at(48, body=Z0, pelvis=Z0, neck=Z0, head=Z0, jaw=Z0, P_root=Z0).arms(48)
    a.legs(0).legs(11, 1.4, 1).legs(13, 1.0, -1).legs(19, 2.4, 1.4).legs(24, 2.0, 1.0).legs(34, 2.2, 1).legs(36, 1.4, -1.2).legs(48)
    a.wings(0).wings(11, beat=-20, spread=16).wings(13, beat=30, sweep=-20, spread=18).wings(19, beat=40, sweep=20, spread=26)
    a.wings(24, beat=-30, spread=22).wings(34, beat=-40, spread=26).wings(36, beat=50, sweep=-20, spread=20).wings(42, beat=6).wings(48)
    a.claws(0).claws(11, -20).claws(19, 50).claws(34, 40).claws(36, -30).claws(48)
    a.sec([(0, 0, 0), (11, -10, 0), (13, 14, 0), (19, -14, 0), (24, -10, 0), (28, -12, 4), (32, -12, -4), (36, 18, 0), (42, 2, 0), (48, 0, 0)], delay=1)
    a.done()

    # ---------------- death (40): convulse + shriek 0-8, hind legs buckle 16, topples onto its side 28, wings drape, still
    a = mk("death", 40)
    a.at(0, body=Z0, root=Z0, P_root=Z0)
    a.at(4, pelvis=(-10, 0, 0), body=(-16, 0, 6), neck=(-20, 0, 0), head=(-30, 10, 10), jaw=(-80, 0, 0))
    a.arms(4, r=(-60, 0, 40), l=(-60, 0, 40))
    a.at(8, body=(-12, 0, -6), head=(-20, -10, -10))
    a.at(16, pelvis=(6, 0, 0), body=(12, 0, 0), neck=(16, 0, 0), head=(20, 0, 0), jaw=(-40, 0, 0))
    a.arms(16, r=(30, 0, 20), l=(30, 0, 20), fr=(-20, 0, 0), fl=(-20, 0, 0))
    a.at(22, root=(0, 0, 30), P_root=(0, 1.0, 0))
    a.at(28, root=(0, 0, 78), P_root=(0, 4.6, 0), body=(6, 0, 0), head=(10, 0, 20), jaw=(-50, 0, 0))
    a.arms(28, r=(40, 0, 60), l=(10, 0, -20), fr=(-20, 0, 0), fl=(-10, 0, 0))
    a.at(31, root=(0, 0, 70), P_root=(0, 5.4, 0))
    a.at(40, root=(0, 0, 76), P_root=(0, 4.6, 0), body=(4, 0, 0), head=(14, 0, 24), jaw=(-60, 0, 0))
    a.legs(0).legs(4, -0.6).legs(16, 5.0).legs(28, 3.0).legs(40, 2.0)
    a.wings(0).wings(4, beat=-40, spread=30).wings(16, beat=10, fold=20).wings(28, beat=40, fold=50).wings(40, beat=50, fold=60)
    a.claws(0).claws(4, -50).claws(16, 40).claws(40, 70)
    a.tail([(0, 0, 0), (4, 30, 0), (16, -10, 0), (28, -20, 20), (40, -24, 26)], lag=1)
    a.sec([(0, 0, 0), (4, -16, 10), (8, -10, -10), (16, 16, 0), (28, 0, 30), (40, 0, 40)], delay=1)
    a.done()


if __name__ == "__main__":
    b = Builder("infected_zip", 1.0, False, 6)
    build(b)
    anims(b)
    b.m.save(DIR + "infected_zip.bbmodel")
    print("infected_zip cubes", len(b.m.cubes), "anims", [x["name"] for x in b.m.anims])
