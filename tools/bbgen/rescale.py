#!/usr/bin/env python3
"""Uniformly scale a .bbmodel about the model origin (feet at y=0).

Scales cube from/to/origin/inflate, outliner group origins and 'position' keyframes.
Rotations, scale keyframes and UVs are left alone (per-face UVs just stretch).

usage: rescale.py <file.bbmodel> <factor>          scale by factor
       rescale.py <file.bbmodel> --height <blocks>  scale so max cube top == blocks
       rescale.py <file.bbmodel>                    print current height (max cube top / 16)
"""
import json
import sys


def height(d):
    return max(max(e['from'][1], e['to'][1]) + e.get('inflate', 0) for e in d['elements'] if 'from' in e) / 16


def _v(x, s):
    if isinstance(x, (int, float)):
        return round(x * s, 4)
    try:
        return str(round(float(x) * s, 4))
    except (TypeError, ValueError):
        return '(%s)*%s' % (x, s) if str(x).strip() else x  # molang expression


def rescale(d, s):
    for e in d['elements']:
        for k in ('from', 'to', 'origin'):
            if k in e:
                e[k] = [round(c * s, 4) for c in e[k]]
        if 'inflate' in e:
            e['inflate'] = round(e['inflate'] * s, 4)

    def walk(n):
        if isinstance(n, dict):
            if 'origin' in n:
                n['origin'] = [round(c * s, 4) for c in n['origin']]
            for c in n.get('children', []):
                walk(c)
    for n in d['outliner']:
        walk(n)
    for a in d.get('animations', []):
        for an in (a.get('animators') or {}).values():
            for k in an.get('keyframes', []):
                if k.get('channel') == 'position':
                    for dp in k.get('data_points', []):
                        for ax in ('x', 'y', 'z'):
                            if ax in dp:
                                dp[ax] = _v(dp[ax], s)
    return d


def main(argv):
    path = argv[1]
    d = json.load(open(path))
    h = height(d)
    if len(argv) == 2:
        print('%.3f' % h)
        return
    s = float(argv[3]) / h if argv[2] == '--height' else float(argv[2])
    rescale(d, s)
    json.dump(d, open(path, 'w'))
    print('%s: %.3f -> %.3f (x%.4f)' % (path, h, height(d), s))


if __name__ == '__main__':
    if len(sys.argv) == 1:  # self-check
        d = {'elements': [{'from': [0, 0, 0], 'to': [1, 32, 1], 'origin': [0, 16, 0], 'inflate': 0.5}],
             'outliner': [{'origin': [0, 8, 0], 'children': [{'origin': [1, 2, 3], 'children': []}]}],
             'animations': [{'animators': {'a': {'keyframes': [
                 {'channel': 'position', 'data_points': [{'x': 1, 'y': '2', 'z': 'math.sin(q.anim_time)'}]},
                 {'channel': 'rotation', 'data_points': [{'x': 10, 'y': 0, 'z': 0}]}]}}}]}
        rescale(d, 2)
        assert d['elements'][0]['to'] == [2, 64, 2] and d['elements'][0]['inflate'] == 1
        assert d['outliner'][0]['children'][0]['origin'] == [2, 4, 6]
        kf = d['animations'][0]['animators']['a']['keyframes']
        assert kf[0]['data_points'][0] == {'x': 2, 'y': '4.0', 'z': '(math.sin(q.anim_time))*2'}
        assert kf[1]['data_points'][0]['x'] == 10
        assert abs(height(d) - 65 / 16) < 1e-9
        print('ok')
    else:
        main(sys.argv)
