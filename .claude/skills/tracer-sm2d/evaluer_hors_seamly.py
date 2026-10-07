"""Évaluateur minimal de fichiers Seamly2D (.sm2d) pour contrôler un tracé sans Seamly.

Repère mathématique (y vers le haut), angles trigonométriques en degrés, comme l'écran Seamly.
Couvre les outils utilisés dans ce dépôt. Usage : python3 sm2d_eval.py fichier.sm2d [--dump]
"""
import math, re, sys, os
import xml.etree.ElementTree as ET


def bez(p0, p1, p2, p3, n=200):
    pts = []
    for i in range(n + 1):
        t = i / n
        a = (1 - t) ** 3; b = 3 * (1 - t) ** 2 * t; c = 3 * (1 - t) * t * t; d = t ** 3
        pts.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0],
                    a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))
    return pts


def plen(pts):
    return sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))


def polar(p, ang, l):
    r = math.radians(ang)
    return (p[0] + l * math.cos(r), p[1] + l * math.sin(r))


def angle(a, b):
    return math.degrees(math.atan2(b[1] - a[1], b[0] - a[0])) % 360


def inter(p1, p2, p3, p4):
    d = (p1[0] - p2[0]) * (p3[1] - p4[1]) - (p1[1] - p2[1]) * (p3[0] - p4[0])
    if abs(d) < 1e-12:
        raise ValueError('droites parallèles')
    t = ((p1[0] - p3[0]) * (p3[1] - p4[1]) - (p1[1] - p3[1]) * (p3[0] - p4[0])) / d
    return (p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1]))


def foot(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    t = ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / (dx * dx + dy * dy)
    return (a[0] + t * dx, a[1] + t * dy)


def ray_curve(p, ang, pts):
    d = (math.cos(math.radians(ang)), math.sin(math.radians(ang)))
    best = None
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        e = (b[0] - a[0], b[1] - a[1])
        den = d[0] * e[1] - d[1] * e[0]
        if abs(den) < 1e-12:
            continue
        w = (a[0] - p[0], a[1] - p[1])
        t = (w[0] * e[1] - w[1] * e[0]) / den
        u = (w[0] * d[1] - w[1] * d[0]) / den
        if -1e-9 <= u <= 1 + 1e-9:
            # Seamly : intersection de la droite (les deux sens) avec la courbe, la plus proche
            q = (p[0] + t * d[0], p[1] + t * d[1])
            if best is None or abs(t) < best[0]:
                best = (abs(t), q)
    if best is None:
        raise ValueError('axe sans intersection avec la courbe')
    return best[1]


def cut(pts, length):
    acc = 0
    for i in range(len(pts) - 1):
        s = math.dist(pts[i], pts[i + 1])
        if acc + s >= length:
            t = (length - acc) / s
            return (pts[i][0] + t * (pts[i + 1][0] - pts[i][0]), pts[i][1] + t * (pts[i + 1][1] - pts[i][1]))
        acc += s
    return pts[-1]


class Pattern:
    def __init__(self, path):
        self.path = path
        self.root = ET.parse(path).getroot()
        self.meas = {}
        mpath = os.path.join(os.path.dirname(path), self.root.findtext('measurements'))
        for m in ET.parse(mpath).getroot().iter('m'):
            self.meas[m.get('name')] = float(m.get('base'))
        self.vars = {}
        self.P = {}      # id -> (x, y)
        self.name = {}   # id -> nom
        self.byname = {}
        self.lines = set()
        self.curves = {}  # nom de courbe -> points échantillonnés
        self.curve_by_id = {}
        self.warn = []
        for v in self.root.find('variables'):
            self.vars[v.get('name')] = self.ev(v.get('formula'))
        for blk in self.root.iter('draftBlock'):
            for el in blk.find('calculation'):
                self.tool(el)

    # --- formules
    def ev(self, f, cur=None):
        f = f.replace(',', '.') if False else f

        def rep(m):
            t = m.group(0)
            if t in ('sqrt', 'sin', 'cos', 'tan', 'abs', 'min', 'max', 'atan', 'asin', 'acos'):
                return 'math.' + t if t not in ('abs', 'min', 'max') else t
            if t == 'CurrentLength':
                return repr(cur)
            if t.startswith('#'):
                return repr(self.vars[t])
            if t in self.meas:
                return repr(self.meas[t])
            if t.startswith('AngleLine_'):
                a, b = self.two(t[10:])
                return repr(angle(self.byname[a], self.byname[b]))
            if t.startswith('Line_'):
                a, b = self.two(t[5:])
                if (a, b) not in self.lines:
                    self.warn.append(f'{t} lu sans segment {a}->{b}')
                return repr(math.dist(self.byname[a], self.byname[b]))
            if t.startswith('Spl'):
                if t not in self.curves:
                    raise KeyError(f'courbe inconnue {t}')
                return repr(plen(self.curves[t]))
            raise KeyError(f'symbole inconnu {t}')
        expr = re.sub(r'#?[A-Za-z_][A-Za-z0-9_]*', rep, f)
        return float(eval(expr, {'math': math}))

    def two(self, s):
        names = sorted(self.byname, key=len, reverse=True)
        for a in names:
            if s.startswith(a + '_') and s[len(a) + 1:] in self.byname:
                return a, s[len(a) + 1:]
        raise KeyError('segment ' + s)

    def put(self, el, p, line_from=None):
        i = el.get('id')
        self.P[i] = p
        n = el.get('name')
        if n in self.byname:
            self.warn.append(f'nom en double {n}')
        self.name[i] = n
        self.byname[n] = p
        if line_from is not None:
            self.lines.add((self.name[line_from], n))

    def g(self, el, k):
        return self.P[el.get(k)]

    def tool(self, el):
        t = el.get('type')
        if el.tag == 'line':
            self.lines.add((self.name[el.get('firstPoint')], self.name[el.get('secondPoint')]))
            return
        if el.tag == 'point':
            if t == 'single':
                self.put(el, (float(el.get('x')), -float(el.get('y'))))
            elif t == 'endLine':
                b = self.g(el, 'basePoint')
                self.put(el, polar(b, self.ev(el.get('angle')), self.ev(el.get('length'))), el.get('basePoint'))
            elif t == 'alongLine':
                a, b = self.g(el, 'firstPoint'), self.g(el, 'secondPoint')
                L = self.ev(el.get('length'), math.dist(a, b))
                self.put(el, polar(a, angle(a, b), L), el.get('firstPoint'))
            elif t == 'normal':
                a, b = self.g(el, 'firstPoint'), self.g(el, 'secondPoint')
                L = self.ev(el.get('length'), math.dist(a, b))
                self.put(el, polar(a, angle(a, b) + 90 + self.ev(el.get('angle', '0')), L), el.get('firstPoint'))
            elif t == 'lineIntersect':
                self.put(el, inter(self.g(el, 'p1Line1'), self.g(el, 'p2Line1'), self.g(el, 'p1Line2'), self.g(el, 'p2Line2')))
            elif t == 'height':
                self.put(el, foot(self.g(el, 'basePoint'), self.g(el, 'p1Line'), self.g(el, 'p2Line')), el.get('basePoint'))
            elif t == 'curveIntersectAxis':
                pts = self.curve_by_id[el.get('curve')]
                self.put(el, ray_curve(self.g(el, 'basePoint'), self.ev(el.get('angle')), pts), el.get('basePoint'))
            elif t == 'lineIntersectAxis':
                b = self.g(el, 'basePoint')
                self.put(el, inter(b, polar(b, self.ev(el.get('angle')), 10), self.g(el, 'p1Line'), self.g(el, 'p2Line')), el.get('basePoint'))
            elif t == 'pointOfContact':
                c = self.g(el, 'center'); r = self.ev(el.get('radius'))
                a, b = self.g(el, 'firstPoint'), self.g(el, 'secondPoint')
                dx, dy = b[0] - a[0], b[1] - a[1]
                fx, fy = a[0] - c[0], a[1] - c[1]
                A = dx * dx + dy * dy; B = 2 * (fx * dx + fy * dy); C = fx * fx + fy * fy - r * r
                disc = B * B - 4 * A * C
                if disc < 0:
                    raise ValueError('cercle sans intersection')
                sols = [(-B + sg * math.sqrt(disc)) / (2 * A) for sg in (-1, 1)]
                pts = [(a[0] + t_ * dx, a[1] + t_ * dy) for t_ in sols]
                self.put(el, min(pts, key=lambda q: math.dist(q, a)))  # le plus proche du premier point
            elif t in ('cutSplinePath', 'cutSpline'):
                pts = self.curve_by_id[el.get('splinePath') or el.get('spline')]
                self.put(el, cut(pts, self.ev(el.get('length'))))
            else:
                raise NotImplementedError(t)
        elif el.tag == 'spline':
            if t == 'simpleInteractive':
                p1, p4 = self.g(el, 'point1'), self.g(el, 'point4')
                pts = bez(p1, polar(p1, float(el.get('angle1')), float(el.get('length1'))),
                          polar(p4, float(el.get('angle2')), float(el.get('length2'))), p4)
                nm = f"Spl_{self.name[el.get('point1')]}_{self.name[el.get('point4')]}"
            elif t == 'pathInteractive':
                pp = list(el.iter('pathPoint'))
                pts = []
                for a, b in zip(pp, pp[1:]):
                    P0, P3 = self.P[a.get('pSpline')], self.P[b.get('pSpline')]
                    seg = bez(P0, polar(P0, float(a.get('angle2')), float(a.get('length2'))),
                              polar(P3, float(b.get('angle1')), float(b.get('length1'))), P3)
                    pts += seg if not pts else seg[1:]
                nm = f"SplPath_{self.name[pp[0].get('pSpline')]}_{self.name[pp[-1].get('pSpline')]}"
            else:
                raise NotImplementedError(t)
            if el.get('duplicate'):
                nm += '_' + el.get('duplicate')
            self.curves[nm] = pts
            self.curve_by_id[el.get('id')] = pts
        elif el.tag == 'arc' and t == 'arcWithLength':
            c = self.g(el, 'center'); r = self.ev(el.get('radius'))
            a1 = self.ev(el.get('angle1')); a2 = a1 + math.degrees(self.ev(el.get('length')) / r)
            self.curve_by_id[el.get('id')] = [polar(c, a1 + (a2 - a1) * i / 200, r) for i in range(201)]
        else:
            raise NotImplementedError(f'{el.tag} {t}')


if __name__ == '__main__':
    p = Pattern(sys.argv[1])
    if '--dump' in sys.argv:
        for i, n in p.name.items():
            x, y = p.P[i]
            print(f'{n:8s} {x:8.2f} {y:8.2f}')
        for n, pts in p.curves.items():
            print(f'{n:22s} {plen(pts):7.2f}')
    for w in sorted(set(p.warn)):
        print('ATTENTION', w)
