"""Shared helpers for the three Lord Hansel form generators (lord_hansel.py / lord_hansel_premature.py / lord_hansel_true.py).
Blockbench space: Y up, ground 0, faces -Z. Character's RIGHT = +X.
Rotation signs: hanging limb rx>0 = swing forward, upright part (torso/head) rx>0 = lean back / look up, ry>0 = turn to the
character's left, hanging limb rz>0 = swing toward +X. Position z<0 = forward, y>0 = up.
Animation times are written in ticks and converted to seconds (tick/20) in A.done()."""
import math, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from bbgen import Model, mix  # noqa: E402,F401

ROOT = os.path.join(os.path.dirname(__file__), "../../../src/main/resources/assets/fpe/bbmodels/")
ALL = ("north", "south", "east", "west", "up", "down")
CLEAR = (0, 0, 0, 0)
HIDE = (.001, .001, .001)


class Kit:
    """painters + shape helpers bound to one Model"""

    def __init__(self, m):
        self.m, self.R = m, m.rng

    # ---------------------------------------------------------------- painters
    @staticmethod
    def all_faces(fn, skip=()):
        return {k: fn for k in ALL if k not in skip}

    @staticmethod
    def combo(*fns):
        def f(F):
            for fn in fns: fn(F)
        return f

    @staticmethod
    def flat(c, glow=False):
        return lambda F: F.rect(0, 0, F.w, F.h, c, glow=glow)

    @staticmethod
    def clear(F):
        F.rect(0, 0, F.w, F.h, CLEAR)

    @staticmethod
    def outline(c):
        return lambda F: (F.rect(0, 0, F.w, 1, c), F.rect(0, F.h - 1, F.w, 1, c), F.rect(0, 0, 1, F.h, c), F.rect(F.w - 1, 0, 1, F.h, c))

    @staticmethod
    def grad(top, bot):
        def f(F):
            for y in range(F.h):
                c = mix(top, bot, y / max(1, F.h - 1))
                for x in range(F.w): F.px(x, y, c)
        return f

    def strands(self, base, light, dark, ink=None, step=2):
        """fur / hair: vertical gradient + streaks"""
        R = self.R
        def f(F):
            for y in range(F.h):
                for x in range(F.w):
                    F.px(x, y, mix(light, base, min(1, 0.25 + 0.75 * y / max(1, F.h))))
            for x in range(0, F.w, step):
                xx = x + R.randint(0, 1)
                y0 = R.randint(0, max(1, F.h // 3))
                for y in range(y0, F.h):
                    F.px(xx, y, mix(base, dark, 0.35 + 0.4 * y / max(1, F.h)))
            for _ in range(F.w * F.h // 30):
                F.px(R.randint(0, F.w - 1), R.randint(0, F.h - 1), light)
            if ink is not None:
                Kit.outline(ink)(F)
        return f

    @staticmethod
    def pointed(fn, tip=6):
        def f(F):
            fn(F)
            n = min(tip, F.h)
            for yy in range(F.h - n, F.h):
                for xx in range(F.w):
                    if abs(xx + .5 - F.w / 2) > (F.h - yy) * F.w / (2 * n):
                        F.px(xx, yy, CLEAR)
        return f

    @staticmethod
    def jagged(fn, tooth=3, depth=1.2):
        def f(F):
            fn(F)
            for x in range(F.w):
                zz = int(abs((x % (2 * tooth)) - tooth) * depth)
                for y in range(F.h - zz, F.h):
                    F.px(x, y, CLEAR)
        return f

    @staticmethod
    def spikep(tip_left, col, dark, glow_edge=None):
        """horizontal spike: a triangle on the face pointing left (texel) or right"""
        def f(F):
            for y in range(F.h):
                for x in range(F.w):
                    u = (x + .5) / F.w
                    u = 1 - u if not tip_left else u
                    half = 0.5 * u
                    v = abs((y + .5) / F.h - 0.5)
                    if v > half: F.px(x, y, CLEAR)
                    elif v > half - 1.2 / F.h: F.px(x, y, glow_edge if glow_edge else dark, glow=glow_edge is not None)
                    else: F.px(x, y, mix(col, dark, 0.3 * (1 - u) + 0.2 * (y / F.h)))
        return f

    @staticmethod
    def thornp(col, dark, up=True):
        """vertical thorn: triangle pointing up (tip at top) or down"""
        def f(F):
            for y in range(F.h):
                for x in range(F.w):
                    v = (y + .5) / F.h if up else 1 - (y + .5) / F.h
                    half = 0.5 * v
                    if abs((x + .5) / F.w - 0.5) > half: F.px(x, y, CLEAR)
                    else: F.px(x, y, mix(col, dark, v * 0.6))
        return f

    def cracks(self, base, dark, red, n=None, glow=True):
        """black body with glowing red cracks (corruption)"""
        R = self.R
        def f(F):
            for y in range(F.h):
                for x in range(F.w):
                    F.px(x, y, mix(base, dark, 0.2 + 0.5 * ((x * 7 + y * 3) % 11) / 11 * 0.6 + 0.3 * y / max(1, F.h)))
            for _ in range(n if n is not None else max(1, F.w * F.h // 220)):
                x, y = R.uniform(0, F.w), R.uniform(0, F.h)
                for _k in range(R.randint(3, 7)):
                    nx, ny = x + R.uniform(-4, 4), y + R.uniform(1, 5)
                    F.line(x, y, nx, ny, red, 1.6, glow=glow)
                    x, y = nx, ny
        return f

    def bark(self, base, light, dark):
        R = self.R
        def f(F):
            for y in range(F.h):
                for x in range(F.w):
                    F.px(x, y, mix(base, dark, 0.25 + 0.35 * math.sin(x * 0.9 + math.sin(y * 0.15) * 2) ** 2))
            for _ in range(max(1, F.w // 3)):
                x = R.uniform(0, F.w); y = 0
                while y < F.h:
                    ny = y + R.uniform(2, 6); nx = x + R.uniform(-1.2, 1.2)
                    F.line(x, y, nx, ny, light, 1)
                    x, y = nx, ny
        return f

    # ---------------------------------------------------------------- shapes
    @staticmethod
    def tip(start, L, rx, rz):
        a, c = math.radians(rx), math.radians(rz)
        y = L * math.cos(a)
        return (start[0] - y * math.sin(c), start[1] + y * math.cos(c), start[2] + L * math.sin(a))

    def seg(self, name, parent, start, L, t, rx, rz, col, painter=None, top=None, td=None, glow=False):
        """a limb segment growing UP from start (rx tilts back, rz tilts toward -X); returns its tip"""
        x, y, z = start
        p = painter or Kit.flat(col)
        d = td or t
        self.m.cube(name, parent, (x - t / 2, y, z - d / 2), (x + t / 2, y + L, z + d / 2), col, origin=start, rot=(rx, 0, rz),
                    faces={"north": p, "south": p, "east": p, "west": p, "up": top or p, "down": p}, glow=glow)
        return Kit.tip(start, L, rx, rz)

    def thorn(self, name, parent, base, L, w, rx, rz, col, dark, ry=0):
        """thin pointed thorn growing UP from base (double-sided, crossed planes)"""
        x, y, z = base
        tp = Kit.thornp(col, dark)
        self.m.cube(name, parent, (x - w / 2, y, z - w / 2), (x + w / 2, y + L, z + w / 2), col, origin=base, rot=(rx, ry, rz),
                    faces={"north": tp, "south": tp, "east": tp, "west": tp, "up": Kit.clear, "down": Kit.flat(dark)})

    def hspike(self, name, parent, base, length, h, d, yaw, roll, col, dark, side=1):
        x, y, z = base
        x0, x1 = (x, x + length) if side > 0 else (x - length, x)
        self.m.cube(name, parent, (x0, y - h / 2, z - d / 2), (x1, y + h / 2, z + d / 2), col, origin=base, rot=(0, yaw, roll),
                    faces={"north": Kit.spikep(side > 0, col, dark), "south": Kit.spikep(side < 0, col, dark),
                           "up": Kit.clear, "down": Kit.clear, "east": Kit.clear, "west": Kit.clear})

    def plane(self, name, parent, c, w, h, painter, rot=(0, 0, 0), d=0.12, hang=True):
        """double sided card hanging down (hang) or standing up from c"""
        x, y, z = c
        y0, y1 = (y - h, y) if hang else (y, y + h)
        self.m.cube(name, parent, (x - w / 2, y0, z - d / 2), (x + w / 2, y1, z + d / 2), 0, origin=c, rot=rot,
                    faces={"north": painter, "south": painter, "east": Kit.clear, "west": Kit.clear, "up": Kit.clear, "down": Kit.clear})


# ==================================================================== animation builder
class A:
    def __init__(self, m, name, ticks, loop=False, props=()):
        self.m, self.name, self.ticks, self.loop, self.tr, self.props = m, name, ticks, loop, {}, props

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
    def s(self, bone, *keys): return self.scl(bone, *self._frame(keys, (1, 1, 1)))

    def show(self, bone, t0, t1, grow=2, peak=1.15):
        """prop visible between t0 and t1 (pops in / out)"""
        ks = [(0, *HIDE)]
        if t0 > 0.5: ks.append((t0 - 0.5, *HIDE))
        ks += [(t0, .3, .3, .3), (t0 + grow, peak, peak, peak), (t0 + grow + 1, 1, 1, 1), (t1, 1, 1, 1)]
        if t1 < self.ticks - 1:
            ks += [(t1 + 1, .3, .3, .3), (t1 + 1.5, *HIDE), (self.ticks, *HIDE)]
        return self.scl(bone, *ks)

    def lag(self, bone, keys, delay=2, gain=1.0):
        seen, out = set(), []
        for (t, x, y, z) in keys:
            tt = min(self.ticks, t + delay)
            if tt in seen: continue
            seen.add(tt); out.append((tt, x * gain, y * gain, z * gain))
        return self.r(bone, *out)

    def wave(self, bones, keys, delay=1.5, gain=1.0):
        """propagate keys down a chain of bones with increasing lag (tails, tendrils, hair)"""
        for i, b in enumerate(bones):
            self.lag(b, keys, delay * (i + 1), gain)
        return self

    def done(self):
        for p in self.props:
            if p not in self.tr or "scale" not in self.tr[p]:
                self.scl(p, (0, *HIDE))
        tracks = {b: {ch: sorted([(t / 20.0, x, y, z) for (t, x, y, z) in v], key=lambda q: q[0]) for ch, v in chs.items()}
                  for b, chs in self.tr.items()}
        self.m.anim(self.name, self.ticks / 20.0, tracks, loop=self.loop)


def mirror(keys):
    return [(t, x, -y, -z) for (t, x, y, z) in keys]


def sinekeys(n, step, amp, ph=0, period=None, base=(0, 0, 0)):
    period = period or n
    return [(t, base[0] + amp[0] * math.sin((t + ph) / period * 2 * math.pi), base[1] + amp[1] * math.sin((t + ph) / period * 2 * math.pi),
             base[2] + amp[2] * math.sin((t + ph) / period * 2 * math.pi)) for t in range(0, n + 1, step)]
