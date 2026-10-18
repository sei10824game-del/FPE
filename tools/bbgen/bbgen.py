"""Tiny .bbmodel generator (Blockbench 'Generic Model', per-face UV, procedurally painted atlas, pure stdlib).
Blockbench space: Y up, ground y=0, entity faces -Z (north), world +X = east. Units = 1/16 block.
Use only to bootstrap models; afterwards the .bbmodel is edited in Blockbench."""
import base64, json, math, random, struct, uuid, zlib

FACES = ["north", "east", "south", "west", "up", "down"]
SHADE = {"north": 1.0, "south": 0.78, "east": 0.88, "west": 0.88, "up": 1.12, "down": 0.6}

def u():
    return str(uuid.uuid4())

def hexrgb(c):
    return ((c >> 16) & 255, (c >> 8) & 255, c & 255)

class Canvas:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.px = bytearray(w * h * 4)

    def set(self, x, y, rgba):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 4
            self.px[i:i + 4] = bytes(rgba)

    def get(self, x, y):
        i = (y * self.w + x) * 4
        return tuple(self.px[i:i + 4])

    def png(self):
        raw = b"".join(b"\x00" + bytes(self.px[y * self.w * 4:(y + 1) * self.w * 4]) for y in range(self.h))
        def chunk(t, d):
            c = struct.pack(">I", len(d)) + t + d
            return c + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)
        return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", self.w, self.h, 8, 6, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(raw, 6)) + chunk(b"IEND", b"")

class Face:
    """a painted rectangle of the atlas; coordinates in texels, (0,0) = top-left as seen from outside."""
    def __init__(self, cv, glow, x, y, w, h):
        self.cv, self.glow, self.x, self.y, self.w, self.h = cv, glow, x, y, w, h

    def px(self, x, y, c, a=255, glow=False):
        if 0 <= x < self.w and 0 <= y < self.h:
            (self.glow if glow else self.cv).set(self.x + x, self.y + y, (*hexrgb(c), a) if not isinstance(c, tuple) else c)
            if glow:
                self.cv.set(self.x + x, self.y + y, (*hexrgb(c), a))

    def rect(self, x, y, w, h, c, glow=False):
        for j in range(int(y), int(y + h)):
            for i in range(int(x), int(x + w)):
                self.px(i, j, c, glow=glow)

    def disc(self, cx, cy, r, c, glow=False):
        for j in range(int(cy - r) - 1, int(cy + r) + 2):
            for i in range(int(cx - r) - 1, int(cx + r) + 2):
                if (i + .5 - cx) ** 2 + (j + .5 - cy) ** 2 <= r * r:
                    self.px(i, j, c, glow=glow)

    def poly(self, pts, c, glow=False):
        ys = [p[1] for p in pts]
        for j in range(int(min(ys)), int(max(ys)) + 1):
            xs = []
            n = len(pts)
            for k in range(n):
                (x1, y1), (x2, y2) = pts[k], pts[(k + 1) % n]
                if (y1 <= j + .5 < y2) or (y2 <= j + .5 < y1):
                    xs.append(x1 + (j + .5 - y1) * (x2 - x1) / (y2 - y1))
            xs.sort()
            for a in range(0, len(xs) - 1, 2):
                for i in range(int(round(xs[a])), int(round(xs[a + 1]))):
                    self.px(i, j, c, glow=glow)

    def line(self, x1, y1, x2, y2, c, t=1, glow=False):
        n = int(max(abs(x2 - x1), abs(y2 - y1))) + 1
        for k in range(n + 1):
            x = x1 + (x2 - x1) * k / max(1, n); y = y1 + (y2 - y1) * k / max(1, n)
            self.disc(x, y, t / 2, c, glow=glow)

def shade(c, m):
    r, g, b = hexrgb(c)
    return (min(255, int(r * m)), min(255, int(g * m)), min(255, int(b * m)), 255)

def mix(a, b, t):
    ra, ga, ba = hexrgb(a); rb, gb, bb = hexrgb(b)
    return (int(ra + (rb - ra) * t) << 16) | (int(ga + (gb - ga) * t) << 8) | int(ba + (bb - ba) * t)

class Model:
    def __init__(self, name, S=8, atlas=1024):
        self.name, self.S, self.A = name, S, atlas
        self.cv, self.glow = Canvas(atlas, atlas), Canvas(atlas, atlas)
        for i in range(0, len(self.glow.px), 4):
            self.glow.px[i:i + 4] = b"\x00\x00\x00\xff"
        self.cx = self.cy = self.rowh = 0
        self.groups, self.cubes, self.outliner = {}, [], []
        self.anims = []
        self.rng = random.Random(7)

    # -- structure
    def group(self, name, origin=(0, 0, 0), rot=(0, 0, 0), parent=None):
        g = {"name": name, "origin": list(origin), "rotation": list(rot), "uuid": u(), "children": [], "color": 0, "export": True}
        self.groups[name] = g
        (self.groups[parent]["children"] if parent else self.outliner).append(g)
        return g

    def _alloc(self, w, h):
        w, h = int(math.ceil(w)), int(math.ceil(h))
        if self.cx + w + 1 > self.A:
            self.cx, self.cy, self.rowh = 0, self.cy + self.rowh + 1, 0
        x, y = self.cx, self.cy
        self.cx += w + 1
        self.rowh = max(self.rowh, h)
        if y + h > self.A:
            raise RuntimeError("atlas full")
        return x, y

    def cube(self, name, parent, frm, to, color=0x808080, origin=None, rot=(0, 0, 0), inflate=0, color2=None, grad=False,
             grain=0.05, faces=None, glow=False, paint=None):
        """faces: {face: fn(Face)} custom painters run after the base fill. paint: fn(dict face->Face) for whole cube."""
        S = self.S
        fr, t = [float(x) for x in frm], [float(x) for x in to]
        o = list(origin) if origin else [(fr[i] + t[i]) / 2 for i in range(3)]
        size = [t[i] - fr[i] for i in range(3)]
        dims = {"north": (size[0], size[1]), "south": (size[0], size[1]), "east": (size[2], size[1]), "west": (size[2], size[1]), "up": (size[0], size[2]), "down": (size[0], size[2])}
        fobj, fdict = {}, {}
        for f in FACES:
            w, h = dims[f]
            pw, ph = max(1, int(round(w * S))), max(1, int(round(h * S)))
            x, y = self._alloc(pw, ph)
            F = Face(self.cv, self.glow, x, y, pw, ph)
            fobj[f] = F
            fdict[f] = {"uv": [x, y, x + pw, y + ph], "texture": 0}
            for j in range(ph):
                for i in range(pw):
                    c = mix(color, color2, j / max(1, ph - 1)) if (grad and color2 is not None) else color
                    n = 1 + (self.rng.random() - .5) * 2 * grain
                    self.cv.set(x + i, y + j, shade(c, SHADE[f] * n))
                    if glow:
                        self.glow.set(x + i, y + j, (*hexrgb(color), 255))
        if faces:
            for f, fn in faces.items():
                fn(fobj[f])
        if paint:
            paint(fobj)
        c = {"name": name, "box_uv": False, "rescale": False, "locked": False, "light_emission": 0, "render_order": "default",
             "allow_mirror_modeling": True, "from": fr, "to": t, "autouv": 0, "color": 0, "inflate": inflate,
             "origin": o, "rotation": list(rot), "faces": fdict, "type": "cube", "uuid": u()}
        self.cubes.append(c)
        self.groups[parent]["children"].append(c["uuid"])
        return c

    # -- animation: anim(name, length, loop) -> {bone: {"rotation": [(t,x,y,z)], "position": [...]}}
    def anim(self, name, length, tracks, loop=False):
        animators = {}
        for bone, chans in tracks.items():
            kfs = []
            for ch, keys in chans.items():
                for (t, x, y, z) in keys:
                    kfs.append({"channel": ch, "data_points": [{"x": x, "y": y, "z": z}], "uuid": u(), "time": t, "color": -1, "interpolation": "catmullrom"})
            animators[self.groups[bone]["uuid"]] = {"name": bone, "type": "bone", "keyframes": kfs}
        self.anims.append({"uuid": u(), "name": name, "loop": "loop" if loop else "once", "override": False, "length": length, "snapping": 24, "selected": False, "anim_time_update": "", "blend_weight": "", "start_delay": "", "loop_delay": "", "animators": animators})

    def _tree(self, ns):
        out = []
        for n in ns:
            if isinstance(n, str):
                out.append(n)
            else:
                g = dict(n)
                g["children"] = self._tree(n["children"])
                out.append(g)
        return out

    def save(self, path):
        def tex(cv, name):
            return {"path": "", "name": name, "folder": "", "namespace": "", "id": "0", "particle": False, "render_mode": "default", "render_sides": "auto",
                    "frame_time": 1, "frame_order_type": "loop", "frame_order": "", "frame_interpolate": False, "visible": True, "internal": True, "saved": True,
                    "uuid": u(), "source": "data:image/png;base64," + base64.b64encode(cv.png()).decode()}
        t0, t1 = tex(self.cv, self.name + ".png"), tex(self.glow, self.name + "_glow.png")
        t1["id"] = "1"
        # cubes reference texture index 0 (colour). glow texture is shown in the texture list only.
        doc = {"meta": {"format_version": "4.10", "model_format": "free", "box_uv": False}, "name": self.name, "model_identifier": "", "visible_box": [1, 1, 0],
               "variable_placeholders": "", "variable_placeholder_buttons": [], "unhandled_root_fields": {},
               "resolution": {"width": self.A, "height": self.A}, "elements": self.cubes, "outliner": self._tree(self.outliner),
               "textures": [t0, t1], "animations": self.anims}
        json.dump(doc, open(path, "w"))
