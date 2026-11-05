"""usage: python3 tools/bbgen/connectivity.py NAME [margin]  - lists cube groups that are not connected to the main body in the rest pose."""
import json, math, sys, itertools
def rot(v, r):
    x, y, z = [math.radians(a) for a in r]
    cx, sx, cy, sy, cz, sz = math.cos(x), math.sin(x), math.cos(y), math.sin(y), math.cos(z), math.sin(z)
    px, py, pz = v
    py, pz = py * cx - pz * sx, py * sx + pz * cx          # Rx
    px, pz = px * cy + pz * sy, -px * sy + pz * cy          # Ry
    px, py = px * cz - py * sz, px * sz + py * cz           # Rz
    return (px, py, pz)
def about(p, o, r):
    v = rot(tuple(p[i] - o[i] for i in range(3)), r)
    return tuple(v[i] + o[i] for i in range(3))
def main(name, margin=0.6):
    d = json.load(open(f'src/main/resources/assets/fpe/bbmodels/{name}.bbmodel'))
    els = {e['uuid']: e for e in d['elements']}
    boxes = []
    def walk(n, chain):
        if isinstance(n, str):
            e = els[n]; f, t = e['from'], e['to']; inf = e.get('inflate', 0)
            pts = [about(p, e['origin'], e['rotation']) for p in itertools.product(*[(f[i]-inf, t[i]+inf) for i in range(3)])]
            for o, r in chain: pts = [about(p, o, r) for p in pts]
            boxes.append((e['name'], [min(p[i] for p in pts) for i in range(3)], [max(p[i] for p in pts) for i in range(3)]))
        else:
            for c in n['children']: walk(c, [(n['origin'], n['rotation'])] + chain)
    for n in d['outliner']: walk(n, [])
    N = len(boxes); par = list(range(N))
    def find(a):
        while par[a] != a: par[a] = par[par[a]]; a = par[a]
        return a
    for i in range(N):
        for j in range(i + 1, N):
            a, b = boxes[i], boxes[j]
            if all(a[1][k] - margin <= b[2][k] and b[1][k] - margin <= a[2][k] for k in range(3)): par[find(i)] = find(j)
    comps = {}
    for i in range(N): comps.setdefault(find(i), []).append(boxes[i][0])
    comps = sorted(comps.values(), key=len, reverse=True)
    print(f'{name}: {N} cubes, {len(comps)} connected groups; main body = {len(comps[0])} cubes')
    for c in comps[1:]: print('  DETACHED:', len(c), c[:8])
if __name__ == '__main__': main(sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else 0.6)
