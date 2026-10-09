"""Génère des images (PNG + SVG) à partir de patrons Seamly2D (.sm2d), sans Seamly.

Usage : python3 sm2d_images.py <fichier.sm2d> [...] --sortie <dossier>
        python3 sm2d_images.py vignettes <fichier.sm2d> [...] --sortie vignettes [--taille 800]
        python3 sm2d_images.py dessins <fichier.sm2d> [...] --sortie vignettes [--style sauge]   (vêtement cousu, devant/dos ;
        styles : papier, epure, ardoise, blueprint, kraft, sauge, indigo, moutarde)
        python3 sm2d_images.py fiches <fichier.sm2d> [...] --sortie vignettes   (patron -> vêtement cousu, une image)

Pour chaque patron :
  <nom>_brouillon.png/svg : tous les blocs de brouillon (points nommés, lignes, courbes)
  <nom>_pieces.png/svg    : les pièces (ligne de couture, marge, droit-fil, nom)
Les SVG sont à l'échelle 1:1 (unités en cm).
"""
import argparse, math, os, re, sys
import xml.etree.ElementTree as ET
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

PX_PAR_CM = 37.795275591
LINESTYLES = {'solidLine': '-', 'dashLine': '--', 'dotLine': ':', 'dashDotLine': '-.',
              'dashDotDotLine': '-.', 'none': None}
COULEURS = {'black': '#222222', 'darkBlue': '#1f3a93', 'green': '#2e8b57', 'mediumseagreen': '#3cb371',
            'blue': '#1f5fd1', 'red': '#c0392b', 'darkRed': '#8b1a1a', 'darkGreen': '#1e6b3a',
            'goldenrod': '#b8860b', 'lightsalmon': '#e9967a', 'orange': '#e67e22', 'violet': '#8e44ad',
            'deeppink': '#d6337a', 'lime': '#4caf50', 'cornflowerblue': '#6495ed', 'deepskyblue': '#00a5e0'}


def d(a):
    r = math.radians(a)
    return math.cos(r), math.sin(r)


def angle_de(p, q):
    a = math.degrees(math.atan2(q[1] - p[1], q[0] - p[0]))
    return a % 360


def bezier(p0, p1, p2, p3, n=60):
    pts = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        pts.append((u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
                    u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1]))
    return pts


def longueur(pts):
    return sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))


def inter_droites(a1, a2, b1, b2):
    x1, y1 = a1; x2, y2 = a2; x3, y3 = b1; x4, y4 = b2
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(den) < 1e-12:
        return None
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
    return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))


class Patron:
    def __init__(self, chemin):
        self.chemin = chemin
        self.racine = ET.parse(chemin).getroot()
        self.unite = self.racine.findtext('unit') or 'cm'
        self.echelle = {'cm': 1.0, 'mm': 0.1, 'inch': 2.54}[self.unite]  # -> cm
        self.vars = {}
        self.points = {}      # id -> (nom, (x, y)) en unités du fichier, y vers le haut
        self.courbes = {}     # id -> dict(nom, pts, couleur, style)
        self.segments = []    # (p1, p2, couleur, style)
        self.labels = {}      # id -> (mx, my)
        self.objets_par_nom = {}
        self.blocs = []
        self.lire_mesures()
        self.lire_variables()
        self.calculer()

    # ---------- formules ----------
    def lire_mesures(self):
        m = self.racine.findtext('measurements')
        if not m:
            return
        src = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(self.chemin)), m.strip()))
        r = ET.parse(src).getroot()
        for e in r.iter('m'):
            v = e.get('base') or e.get('value')
            try:
                self.vars[e.get('name')] = float(v)
            except (TypeError, ValueError):
                self.vars[e.get('name')] = self.eval(v)

    def lire_variables(self):
        for v in self.racine.iter('variable'):
            self.vars[v.get('name')] = self.eval(v.get('formula'))

    def valeur(self, nom, ctx):
        if nom in ctx:
            return ctx[nom]
        if nom in self.vars:
            return self.vars[nom]
        if nom in self.objets_par_nom:
            return self.objets_par_nom[nom]
        m = re.fullmatch(r'(Line|AngleLine)_(\w+?)_(\w+)', nom)
        if m:
            noms = {n: p for n, p in self.points.values()}
            # découpe ambiguë : essayer toutes les coupures possibles
            parties = (m.group(2) + '_' + m.group(3)).split('_')
            for i in range(1, len(parties)):
                a, b = '_'.join(parties[:i]), '_'.join(parties[i:])
                if a in noms and b in noms:
                    return math.dist(noms[a], noms[b]) if m.group(1) == 'Line' else angle_de(noms[a], noms[b])
        raise KeyError(f'symbole inconnu : {nom}')

    FONCTIONS = {'sqrt': math.sqrt, 'sin': lambda a: math.sin(math.radians(a)),
                 'cos': lambda a: math.cos(math.radians(a)), 'tan': lambda a: math.tan(math.radians(a)),
                 'asin': lambda x: math.degrees(math.asin(x)), 'acos': lambda x: math.degrees(math.acos(x)),
                 'atan': lambda x: math.degrees(math.atan(x)), 'abs': abs, 'min': min, 'max': max,
                 'round': round, 'pi': math.pi}

    def eval(self, f, ctx=None):
        ctx = ctx or {}
        f = f.replace(',', '.').replace('^', '**')
        env = {}

        def sub(m):
            n = m.group(0)
            if n in self.FONCTIONS:
                return n
            k = f'_v{len(env)}'
            env[k] = self.valeur(n, ctx)
            return k
        expr = re.sub(r'[A-Za-z_#][A-Za-z0-9_#]*', sub, f)
        return float(eval(expr, {'__builtins__': {}, **self.FONCTIONS}, env))

    # ---------- géométrie ----------
    def P(self, i):
        return self.points[i][1]

    def nom(self, i):
        return self.points[i][0]

    def ajouter_point(self, e, p):
        self.points[e.get('id')] = (e.get('name'), p)
        self.labels[e.get('id')] = (float(e.get('mx', 0.13)), float(e.get('my', 0.26)))

    def trait(self, e, a, b):
        st = e.get('lineType', 'solidLine')
        if LINESTYLES.get(st):
            self.segments.append((a, b, e.get('lineColor', 'black'), st))

    def calculer(self):
        for bloc in self.racine.findall('draftBlock'):
            ids = []
            for e in bloc.find('calculation'):
                ids.append(e.get('id'))
                getattr(self, 'outil_' + e.tag)(e)
            self.blocs.append((bloc.get('name'), ids))

    def outil_point(self, e):
        t = e.get('type')
        g = lambda k: self.eval(e.get(k))
        if t == 'single':
            p = (float(e.get('x')) , -float(e.get('y')))
            self.ajouter_point(e, p)
        elif t == 'endLine':
            b = self.P(e.get('basePoint'))
            dx, dy = d(g('angle'))
            L = g('length')
            p = (b[0] + L * dx, b[1] + L * dy)
            self.ajouter_point(e, p); self.trait(e, b, p)
        elif t == 'alongLine':
            a, b = self.P(e.get('firstPoint')), self.P(e.get('secondPoint'))
            L = self.eval(e.get('length'), {'CurrentLength': math.dist(a, b)})
            ux, uy = (b[0] - a[0]) / math.dist(a, b), (b[1] - a[1]) / math.dist(a, b)
            p = (a[0] + L * ux, a[1] + L * uy)
            self.ajouter_point(e, p); self.trait(e, a, p)
        elif t == 'normal':
            a, b = self.P(e.get('firstPoint')), self.P(e.get('secondPoint'))
            dx, dy = d(angle_de(a, b) + 90 + g('angle'))
            L = g('length')
            p = (a[0] + L * dx, a[1] + L * dy)
            self.ajouter_point(e, p); self.trait(e, a, p)
        elif t == 'lineIntersect':
            p = inter_droites(self.P(e.get('p1Line1')), self.P(e.get('p2Line1')),
                              self.P(e.get('p1Line2')), self.P(e.get('p2Line2')))
            self.ajouter_point(e, p)
        elif t == 'height':
            b, a, c = self.P(e.get('basePoint')), self.P(e.get('p1Line')), self.P(e.get('p2Line'))
            vx, vy = c[0] - a[0], c[1] - a[1]
            t_ = ((b[0] - a[0]) * vx + (b[1] - a[1]) * vy) / (vx * vx + vy * vy)
            p = (a[0] + t_ * vx, a[1] + t_ * vy)
            self.ajouter_point(e, p); self.trait(e, b, p)
        elif t == 'curveIntersectAxis':
            b = self.P(e.get('basePoint'))
            dx, dy = d(g('angle'))
            far = (b[0] + 1000 * dx, b[1] + 1000 * dy)
            pts = self.courbes[e.get('curve')]['pts']
            best = None
            for q1, q2 in zip(pts, pts[1:]):
                x = inter_droites(b, far, q1, q2)
                if x is None:
                    continue
                s = ((x[0] - q1[0]) * (q2[0] - q1[0]) + (x[1] - q1[1]) * (q2[1] - q1[1])) / max(math.dist(q1, q2)**2, 1e-12)
                if -1e-9 <= s <= 1 + 1e-9:
                    tt = (x[0] - b[0]) * dx + (x[1] - b[1]) * dy
                    if best is None or abs(tt) < abs(best[0]):
                        best = (tt, x)
            p = best[1]
            self.ajouter_point(e, p); self.trait(e, b, p)
        elif t == 'pointOfContact':
            c = self.P(e.get('center')); r = g('radius')
            a, b = self.P(e.get('firstPoint')), self.P(e.get('secondPoint'))
            vx, vy = b[0] - a[0], b[1] - a[1]
            A = vx * vx + vy * vy
            B = 2 * (vx * (a[0] - c[0]) + vy * (a[1] - c[1]))
            C = (a[0] - c[0])**2 + (a[1] - c[1])**2 - r * r
            disc = math.sqrt(max(B * B - 4 * A * C, 0))
            sols = [(-B + s * disc) / (2 * A) for s in (1, -1)]
            sur = [s for s in sols if -1e-9 <= s <= 1 + 1e-9]
            s = sur[0] if len(sur) == 1 else min(sur or sols, key=lambda s: abs(s))
            p = (a[0] + s * vx, a[1] + s * vy)
            self.ajouter_point(e, p)
        elif t in ('cutSpline', 'cutSplinePath'):
            pts = self.courbes[e.get('spline') or e.get('splinePath')]['pts']
            reste = g('length')
            p = pts[-1]
            for a, b in zip(pts, pts[1:]):
                L = math.dist(a, b)
                if L >= reste:
                    s = reste / L if L else 0
                    p = (a[0] + s * (b[0] - a[0]), a[1] + s * (b[1] - a[1]))
                    break
                reste -= L
            self.ajouter_point(e, p)
        else:
            raise NotImplementedError(f'outil point {t}')

    def outil_line(self, e):
        a, b = self.P(e.get('firstPoint')), self.P(e.get('secondPoint'))
        self.trait(e, a, b)

    def outil_arc(self, e):
        c = self.P(e.get('center'))
        r = self.eval(e.get('radius'))
        a1 = self.eval(e.get('angle1'))
        t = e.get('type')
        if t == 'arcWithLength':
            a2 = a1 + math.degrees(self.eval(e.get('length')) / r)
        else:
            a2 = self.eval(e.get('angle2'))
            if a2 < a1:
                a2 += 360
        pts = [(c[0] + r * math.cos(math.radians(a1 + (a2 - a1) * i / 60)),
                c[1] + r * math.sin(math.radians(a1 + (a2 - a1) * i / 60))) for i in range(61)]
        self.courbes[e.get('id')] = dict(nom=f'Arc_{self.nom(e.get("center"))}', pts=pts,
                                         couleur=e.get('color', 'black'), style=e.get('penStyle', 'solidLine'))

    def outil_spline(self, e):
        t = e.get('type')
        suff = '_' + e.get('duplicate') if e.get('duplicate') else ''
        if t == 'simpleInteractive':
            p1, p4 = self.P(e.get('point1')), self.P(e.get('point4'))
            a1, a2 = d(self.eval(e.get('angle1'))), d(self.eval(e.get('angle2')))
            l1, l2 = self.eval(e.get('length1')), self.eval(e.get('length2'))
            pts = bezier(p1, (p1[0] + l1 * a1[0], p1[1] + l1 * a1[1]), (p4[0] + l2 * a2[0], p4[1] + l2 * a2[1]), p4)
            nom = f'Spl_{self.nom(e.get("point1"))}_{self.nom(e.get("point4"))}{suff}'
        elif t == 'cubicBezier':
            pts = bezier(*(self.P(e.get(k)) for k in ('point1', 'point2', 'point3', 'point4')))
            nom = f'Spl_{self.nom(e.get("point1"))}_{self.nom(e.get("point4"))}{suff}'
        elif t == 'pathInteractive':
            pp = e.findall('pathPoint')
            pts = []
            for a, b in zip(pp, pp[1:]):
                pa, pb = self.P(a.get('pSpline')), self.P(b.get('pSpline'))
                da, db = d(self.eval(a.get('angle2'))), d(self.eval(b.get('angle1')))
                la, lb = self.eval(a.get('length2')), self.eval(b.get('length1'))
                seg = bezier(pa, (pa[0] + la * da[0], pa[1] + la * da[1]), (pb[0] + lb * db[0], pb[1] + lb * db[1]), pb)
                pts += seg if not pts else seg[1:]
            nom = f'SplPath_{self.nom(pp[0].get("pSpline"))}_{self.nom(pp[-1].get("pSpline"))}{suff}'
        else:
            raise NotImplementedError(f'courbe {t}')
        self.courbes[e.get('id')] = dict(nom=nom, pts=pts, couleur=e.get('color', 'black'),
                                         style=e.get('penStyle', 'solidLine'))
        self.objets_par_nom[nom] = longueur(pts)

    # ---------- pièces ----------
    def pieces(self):
        for bloc in self.racine.findall('draftBlock'):
            modeling = {m.get('id'): m for m in bloc.find('modeling')}
            for piece in bloc.find('pieces').findall('piece'):
                contour = []  # liste de (pts, largeur_avant, largeur_apres) par nœud
                largeur = float(piece.get('width', 0)) if piece.get('seamAllowance') == 'true' else 0.0
                for n in piece.find('nodes').findall('node'):
                    obj = modeling[n.get('idObject')].get('idObject')
                    if n.get('type') == 'NodePoint':
                        pts = [self.P(obj)]
                    else:
                        pts = list(self.courbes[obj]['pts'])
                        if n.get('reverse') == '1':
                            pts.reverse()
                    av = float(n.get('before')) if n.get('before') not in (None, '') else largeur
                    ap = float(n.get('after')) if n.get('after') not in (None, '') else largeur
                    contour.append((n.get('type'), pts, av, ap))
                yield bloc.get('name'), piece, rogner(contour), largeur


def projeter(pts, q):
    """(distance, abscisse continue i + s) du point de la polyligne le plus proche de q."""
    best = (math.inf, 0.0)
    for i, (a, b) in enumerate(zip(pts, pts[1:])):
        vx, vy = b[0] - a[0], b[1] - a[1]
        L2 = vx * vx + vy * vy
        s = 0.0 if L2 == 0 else max(0.0, min(1.0, ((q[0] - a[0]) * vx + (q[1] - a[1]) * vy) / L2))
        dd = math.dist(q, (a[0] + s * vx, a[1] + s * vy))
        if dd < best[0]:
            best = (dd, i + s)
    return best


def tronquer(pts, t0, t1):
    """Portion de la polyligne entre les abscisses t0 < t1."""
    def pt(t):
        i = min(int(t), len(pts) - 2)
        s = t - i
        return (pts[i][0] + s * (pts[i + 1][0] - pts[i][0]), pts[i][1] + s * (pts[i + 1][1] - pts[i][1]))
    return [pt(t0)] + [pts[k] for k in range(math.floor(t0) + 1, math.ceil(t1))] + [pt(t1)]


def rogner(contour, tol=0.05):
    """Comme Seamly : une courbe d'une pièce ne garde que la portion entre les points voisins posés dessus."""
    n = len(contour)
    out = []
    for i, (typ, pts, av, ap) in enumerate(contour):
        if typ != 'NodePoint' and len(pts) > 1:
            voisins = []
            for pas in (-1, 1):
                j = (i + pas) % n
                if contour[j][0] == 'NodePoint':
                    dd, t = projeter(pts, contour[j][1][0])
                    voisins.append(t if dd < tol else None)
                else:
                    voisins.append(None)
            t0 = voisins[0] if voisins[0] is not None else 0.0
            t1 = voisins[1] if voisins[1] is not None else len(pts) - 1.0
            if t1 > t0:
                pts = tronquer(pts, t0, t1)
        out.append((typ, pts, av, ap))
    return out


def assembler(contour):
    """Polyligne fermée + largeur de marge par segment."""
    pts, larg = [], []
    n = len(contour)
    for i, (typ, p, av, ap) in enumerate(contour):
        for q in p:
            if pts and math.dist(pts[-1], q) < 1e-6:
                continue
            pts.append(q)
            larg.append(None)
    if math.dist(pts[0], pts[-1]) < 1e-6:
        pts.pop(); larg.pop()
    # largeur par segment : défaut, puis 0 si encadré par after=0 / before=0
    defaut = max(max(c[2], c[3]) for c in contour)
    w = [defaut] * len(pts)
    idx_noeud = []
    for typ, p, av, ap in contour:
        if typ == 'NodePoint':
            j = min(range(len(pts)), key=lambda k: math.dist(pts[k], p[0]))
            idx_noeud.append((j, av, ap))
    for j, av, ap in idx_noeud:
        if ap == 0:
            w[j] = 0.0
        if av == 0:
            w[(j - 1) % len(pts)] = 0.0
    return pts, w


def marge(pts, w):
    n = len(pts)
    aire = sum(pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1] for i in range(n))
    sgn = -1 if aire > 0 else 1   # extérieur à droite si contour anti-horaire
    lignes = []
    for i in range(n):
        a, b = pts[i], pts[(i + 1) % n]
        L = math.dist(a, b)
        nx, ny = sgn * -(b[1] - a[1]) / L, sgn * (b[0] - a[0]) / L
        lignes.append(((a[0] + w[i] * nx, a[1] + w[i] * ny), (b[0] + w[i] * nx, b[1] + w[i] * ny)))
    out = []
    for i in range(n):
        l1, l2 = lignes[i - 1], lignes[i]
        v1 = (l1[1][0] - l1[0][0], l1[1][1] - l1[0][1]); v2 = (l2[1][0] - l2[0][0], l2[1][1] - l2[0][1])
        cr = abs(v1[0] * v2[1] - v1[1] * v2[0]) / (math.hypot(*v1) * math.hypot(*v2))
        x = inter_droites(l1[0], l1[1], l2[0], l2[1]) if cr > 0.02 else None
        if x is None or math.dist(x, pts[i]) > 4 * max(w[i - 1], w[i], 0.1):
            out += [l1[1], l2[0]]
        else:
            out.append(x)
    return out


def style_trait(st):
    return {'-': '-', '--': (0, (5, 3)), ':': (0, (1, 2)), '-.': (0, (6, 2, 1, 2))}[LINESTYLES[st]]


def couleur(c):
    return COULEURS.get(c, c if c.startswith('#') else '#222222')


def figure(xmin, xmax, ymin, ymax, titre, px_cm):
    w, h = xmax - xmin, ymax - ymin
    fig = plt.figure(figsize=(w / 2.54, h / 2.54 + 1.2))  # 1:1 en pouces pour le SVG
    ax = fig.add_axes([0, 0, 1, h / (h + 1.2 * 2.54)])
    ax.set_xlim(xmin, xmax); ax.set_ylim(ymin, ymax)
    ax.set_aspect('equal'); ax.axis('off')
    fig.text(0.5, 1 - 0.6 / (h / 2.54 + 1.2), titre, ha='center', va='center', fontsize=28, weight='bold', color='#222')
    return fig, ax


def taille_police(cm):
    return cm / 2.54 * 72


def dessiner_brouillon(p, base, sortie, px_cm):
    tous = [pt for _, pt in p.points.values()] + [q for c in p.courbes.values() for q in c['pts']]
    xs, ys = [q[0] for q in tous], [q[1] for q in tous]
    m = 4
    fig, ax = figure(min(xs) - m, max(xs) + m, min(ys) - m, max(ys) + m, f'{base} — brouillon', px_cm)
    ax.add_patch(plt.Rectangle((min(xs) - m, min(ys) - m), max(xs) - min(xs) + 2 * m, max(ys) - min(ys) + 2 * m,
                               fc='white', ec='none', zorder=0))
    for a, b, c, st in p.segments:
        ax.plot([a[0], b[0]], [a[1], b[1]], color=couleur(c), lw=0.9, linestyle=style_trait(st), zorder=2)
    for c in p.courbes.values():
        ax.plot(*zip(*c['pts']), color=couleur(c['couleur']), lw=1.6, linestyle=style_trait(c['style']), zorder=3)
    for i, (nom, pt) in p.points.items():
        ax.plot(*pt, 'o', ms=3, color='#c0392b', zorder=4)
        mx, my = p.labels[i]
        ax.text(pt[0] + mx, pt[1] - my, nom, fontsize=taille_police(0.55), color='#1a1a1a', zorder=5,
                va='top', ha='left')
    for ext in ('png', 'svg'):
        fig.savefig(os.path.join(sortie, f'{base}_brouillon.{ext}'), dpi=px_cm * 2.54, facecolor='white')
    plt.close(fig)


def dessiner_pieces(p, base, sortie, px_cm):
    items = []
    for bloc, piece, contour, largeur in p.pieces():
        pts, w = assembler(contour)
        pts = [(x * p.echelle, y * p.echelle) for x, y in pts]
        w = [x * p.echelle for x in w]
        sa = marge(pts, w) if largeur > 0 else None
        items.append((piece, pts, sa))
    # disposition côte à côte, alignées en haut
    x0, gap = 0, 6
    places = []
    hmax = 0
    for piece, pts, sa in items:
        ref = sa or pts
        xmin, xmax = min(q[0] for q in ref), max(q[0] for q in ref)
        ymin, ymax = min(q[1] for q in ref), max(q[1] for q in ref)
        dx, dy = x0 - xmin, -ymax
        places.append((piece, pts, sa, dx, dy, (xmin, xmax, ymin, ymax)))
        x0 += xmax - xmin + gap
        hmax = max(hmax, ymax - ymin)
    m = 3
    fig, ax = figure(-m, x0 - gap + m, -hmax - m, m, f'{base} — pièces', px_cm)
    for piece, pts, sa, dx, dy, (xmin, xmax, ymin, ymax) in places:
        T = lambda q: (q[0] + dx, q[1] + dy)
        if sa:
            ax.fill(*zip(*map(T, sa)), fc='#f4efe6', ec='#555', lw=1.0, zorder=1)
        ax.fill(*zip(*map(T, pts)), fc='#fbf8f2' if sa else 'none', ec='#111', lw=1.8, zorder=2)
        nom = piece.get('name')
        data = piece.find('data')
        q = data.get('quantity', '1') if data is not None else '1'
        pli = data is not None and data.get('onFold') == 'true'
        cx, cy = T(((xmin + xmax) / 2, (ymin + ymax) / 2))
        h = ymax - ymin
        fs = taille_police(min(2.2, max(0.6, (xmax - xmin) / 9)))
        lignes = f'{nom}\nx{q}' + ('  — au pli' if pli else '')
        ax.text(cx, cy + h * 0.12, lignes, ha='center', va='center', fontsize=fs, color='#222', zorder=4,
                linespacing=1.3, bbox=dict(fc='#fbf8f2', ec='none', pad=2))
        g = piece.find('grainline')
        if g is not None and g.get('visible') == 'true':
            gx, gy = float(g.get('mx')) / PX_PAR_CM, -float(g.get('my')) / PX_PAR_CM
            L = p.eval(g.get('length')) * p.echelle
            r = math.radians(float(g.get('rotation', 90)))
            a = T((gx, gy)); b = T((gx + L * math.cos(r), gy + L * math.sin(r)))
            ax.annotate('', xy=b, xytext=a, arrowprops=dict(arrowstyle='<|-|>', color='#1f3a93', lw=1.4,
                                                            mutation_scale=18), zorder=3)
        # cotes de la pièce
        ax.text(cx, T((0, ymin))[1] - 1.2, f'{xmax - xmin:.1f} × {ymax - ymin:.1f} cm (avec marge)' if sa else
                f'{xmax - xmin:.1f} × {ymax - ymin:.1f} cm', ha='center', va='top',
                fontsize=taille_police(0.6), color='#666')
    for ext in ('png', 'svg'):
        fig.savefig(os.path.join(sortie, f'{base}_pieces.{ext}'), dpi=px_cm * 2.54, facecolor='white')
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('fichiers', nargs='+')
    ap.add_argument('--sortie', default='images')
    ap.add_argument('--px-cm', type=float, default=20, help='résolution des PNG (pixels par cm)')
    a = ap.parse_args()
    os.makedirs(a.sortie, exist_ok=True)
    for f in a.fichiers:
        base = os.path.splitext(os.path.basename(f))[0]
        p = Patron(f)
        if not any(b.find('calculation') is not None and len(b.find('calculation')) for b in p.racine.findall('draftBlock')):
            continue
        dessiner_brouillon(p, base, a.sortie, a.px_cm)
        dessiner_pieces(p, base, a.sortie, a.px_cm)
        print('ok', base)




# ---------- vignettes pour un site ----------
def dessiner_vignette(p, base, sortie, taille_px=800, fond='#f6f1e7', papier='#ffffff',
                      trait='#2b2b2b', accent='#c8553d', ax=None, legendes=False, cadre=1.18, haut=0.0,
                      police=None):
    """Vignette carrée : pièces seules, sans texte ni cotes (le carré de contrôle est exclu)."""
    items = []
    for bloc, piece, contour, largeur in p.pieces():
        if piece.get('seamAllowance') != 'true':
            continue
        pts, w = assembler(contour)
        sa = marge(pts, w) if largeur > 0 else pts
        q = piece.find('data')
        items.append((pts, sa, piece.get('name'), q.get('quantity', '1') if q is not None else '1',
                      q is not None and q.get('onFold') == 'true'))
    # disposition en ligne, alignées en bas
    gap = 5
    x0, places = 0, []
    for pts, sa, *_ in items:
        xmin, xmax = min(q[0] for q in sa), max(q[0] for q in sa)
        ymin = min(q[1] for q in sa)
        places.append((pts, sa, x0 - xmin, -ymin))
        x0 += xmax - xmin + gap
    W = x0 - gap
    H = max(max(q[1] for q in sa) + dy for _, sa, _, dy in places)
    cote = max(W, H) * cadre
    cx, cy = W / 2, H / 2 + cote * haut
    seul = ax is None
    if seul:
        fig = plt.figure(figsize=(taille_px / 100, taille_px / 100), dpi=100)
        ax = fig.add_axes([0, 0, 1, 1])
        fig.patch.set_facecolor(fond)
    ax.set_xlim(cx - cote / 2, cx + cote / 2); ax.set_ylim(cy - cote / 2, cy + cote / 2)
    ax.set_aspect('equal'); ax.axis('off')
    ax.add_patch(plt.Rectangle((cx - cote / 2, cy - cote / 2), cote, cote, fc=fond, ec='none', zorder=0))
    lw = taille_px / 320  # épaisseur proportionnelle à la taille de la vignette
    for pts, sa, dx, dy in places:
        T = lambda L: list(zip(*[(x + dx, y + dy) for x, y in L]))
        ax.fill(*T(sa), fc=papier, ec=trait, lw=lw, joinstyle='round', zorder=2)
        xs, ys = T(pts)
        ax.plot(list(xs) + [xs[0]], list(ys) + [ys[0]], color=accent, lw=lw * 0.6,
                linestyle=(0, (5, 4)), zorder=3)
        # droit-fil stylisé au centre de la pièce
        X, Y = T(pts)
        mx = (min(X) + max(X)) / 2; y1, y2 = min(Y), max(Y)
        hh = y2 - y1
        ax.annotate('', xy=(mx, y2 - hh * 0.22), xytext=(mx, y1 + hh * 0.22),
                    arrowprops=dict(arrowstyle='<|-|>', color=trait, lw=lw * 0.5, mutation_scale=lw * 5), zorder=3)
    if legendes:
        for (pts, sa, nom, qte, pli), (_, _, dx, dy) in zip(items, places):
            X = [x + dx for x, _ in sa]; Y = [y + dy for _, y in sa]
            txt = nom + (f' ×{qte}' if qte != '1' else '') + ('\nau pli' if pli else '')
            ax.text((min(X) + max(X)) / 2, min(Y) - cote * 0.03, txt, ha='center', va='top',
                    fontsize=taille_px / 62 * (1.15 if police else 1), color=trait,
                    fontproperties=police, linespacing=1.1)
    if seul:
        for ext in ('png', 'svg'):
            fig.savefig(os.path.join(sortie, f'{base}.{ext}'), dpi=100, facecolor=fond)
        plt.close(fig)


def main_vignettes(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('fichiers', nargs='+')
    ap.add_argument('--sortie', default='vignettes')
    ap.add_argument('--taille', type=int, default=800)
    a = ap.parse_args(argv)
    os.makedirs(a.sortie, exist_ok=True)
    for f in a.fichiers:
        base = os.path.splitext(os.path.basename(f))[0]
        p = Patron(f)
        if not any(pc.get('seamAllowance') == 'true' for _, pc, _, _ in p.pieces()):
            continue
        dessiner_vignette(p, base, a.sortie, a.taille)
        print('vignette', base)


def main_dessins(argv):
    import dessin
    ap = argparse.ArgumentParser()
    ap.add_argument('fichiers', nargs='+')
    ap.add_argument('--sortie', default='vignettes')
    ap.add_argument('--taille', type=int, default=800)
    ap.add_argument('--style', default='sauge', choices=list(dessin.STYLES))
    a = ap.parse_args(argv)
    os.makedirs(a.sortie, exist_ok=True)
    for f in a.fichiers:
        base = os.path.splitext(os.path.basename(f))[0]
        p = Patron(f)
        vues = vues_dessin(p)
        if vues is None:
            print('pas de modèle de dessin pour', base)
            continue
        dessin.rendre(vues, os.path.join(a.sortie, base + '_dessin'), a.taille, a.style)
        print('dessin', base)


def dessiner_fiche(p, vues, chemin_base, taille_px=800, style='atelier'):
    """Une image : le patron (style papier) -> le vêtement cousu (style choisi)."""
    import dessin
    st = dessin.STYLES[style]
    atelier = 'titre' in st
    encre = st['trait'] if atelier else '#2b2b2b'
    fond = st['fond'] if atelier else '#f6f1e7'
    fig = plt.figure(figsize=(2 * taille_px / 100, taille_px / 100), dpi=100)
    fig.patch.set_facecolor(fond)
    gauche = fig.add_axes([0, 0, 0.5, 1]); droite = fig.add_axes([0.5, 0, 0.5, 1])
    opts = dict(fond=fond, trait=encre, accent=st['accent'], papier='#ffffff',
                police=dessin.police(st['legende'])) if atelier else {}
    dessiner_vignette(p, None, None, taille_px, ax=gauche, legendes=True, cadre=1.45, haut=0.06, **opts)
    dessin.rendre(vues, None, taille_px, style, ax=droite, legendes=True, cadre=1.45, haut=0.06)
    titres = ('Le patron', 'Une fois cousu') if atelier else ('LE PATRON', 'UNE FOIS COUSU')
    for ax, txt, coul in ((gauche, titres[0], encre), (droite, titres[1], st['trait'])):
        if atelier:
            ax.text(0.5, 0.93, txt, transform=ax.transAxes, ha='center', va='center',
                    fontsize=taille_px / 30, color=coul, fontproperties=dessin.police(st['titre']))
        else:
            ax.text(0.5, 0.93, txt, transform=ax.transAxes, ha='center', va='center',
                    fontsize=taille_px / 40, color=coul, weight='bold')
    if atelier:
        # filet pointillé entre les deux moitiés, interrompu par la pastille
        for y0, y1 in ((0.06, 0.40), (0.60, 0.88)):
            fig.add_artist(plt.Line2D([0.5, 0.5], [y0, y1], transform=fig.transFigure, color=encre,
                                      lw=taille_px / 800, linestyle=(0, (2, 3))))
    # pastille flèche à la jonction
    sur = fig.add_axes([0.5 - 0.035, 0.5 - 0.07, 0.07, 0.14]); sur.axis('off')
    sur.set_xlim(-1, 1); sur.set_ylim(-1, 1); sur.set_aspect('equal')
    sur.add_patch(plt.Circle((0, 0), 0.95, fc='#ffffff', ec=encre, lw=taille_px / 400))
    sur.annotate('', xy=(0.55, 0), xytext=(-0.55, 0),
                 arrowprops=dict(arrowstyle='-|>', color=st['accent'] if atelier else encre,
                                 lw=taille_px / 300, mutation_scale=taille_px / 40))
    for ext in ('png', 'svg'):
        fig.savefig(f'{chemin_base}.{ext}', dpi=100, facecolor=fond)
    plt.close(fig)


def dessiner_planche(p, chemin_base, taille_px=800, style='atelier'):
    """Planche technique d'une base : les pièces seules, légendées, sous un titre."""
    import dessin
    st = dessin.STYLES[style]
    fig = plt.figure(figsize=(taille_px / 100, taille_px / 100), dpi=100)
    fig.patch.set_facecolor('#ffffff')
    ax = fig.add_axes([0, 0, 1, 1])
    dessiner_vignette(p, None, None, taille_px, ax=ax, legendes=True, cadre=1.42, haut=0.05,
                      fond='#ffffff', trait=st['trait'], accent=st['accent'], papier='#ffffff',
                      police=dessin.police(st['legende']))
    ax.text(0.5, 0.92, 'Le patron', transform=ax.transAxes, ha='center', va='center',
            fontsize=taille_px / 22, color=st['trait'], fontproperties=dessin.police(st['titre']))
    for ext in ('png', 'svg'):
        fig.savefig(f'{chemin_base}.{ext}', dpi=100, facecolor='#ffffff')
    plt.close(fig)


def main_planches(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('fichiers', nargs='+')
    ap.add_argument('--sortie', default='vignettes')
    ap.add_argument('--taille', type=int, default=800)
    a = ap.parse_args(argv)
    os.makedirs(a.sortie, exist_ok=True)
    for f in a.fichiers:
        base = os.path.splitext(os.path.basename(f))[0]
        dessiner_planche(Patron(f), os.path.join(a.sortie, base + '_planche'), a.taille)
        print('planche', base)


def main_fiches(argv):
    import dessin
    ap = argparse.ArgumentParser()
    ap.add_argument('fichiers', nargs='+')
    ap.add_argument('--sortie', default='vignettes')
    ap.add_argument('--taille', type=int, default=800)
    ap.add_argument('--style', default='atelier', choices=list(dessin.STYLES))
    a = ap.parse_args(argv)
    os.makedirs(a.sortie, exist_ok=True)
    for f in a.fichiers:
        base = os.path.splitext(os.path.basename(f))[0]
        p = Patron(f)
        vues = vues_dessin(p)
        if vues is None:
            print('pas de modèle de dessin pour', base)
            continue
        dessiner_fiche(p, vues, os.path.join(a.sortie, base + '_fiche'), a.taille, a.style)
        print('fiche', base)


def vues_dessin(p):
    import dessin
    noms = {n for n, _ in p.points.values()}
    if {'vHp', 'vHpp', 'vE2', 'vF2'} <= noms:
        return dessin.haut_pyjama(p)
    if {'cA3', 'cA5', 'cA2e', 'cB5e'} <= noms:
        return dessin.pantalon(p, pyjama=True)
    if {'mE', 'K', 'E1', 'F1'} <= noms:
        return dessin.haut(p)
    if {'A5', 'B5', 'E3', 'E4'} <= noms:
        return dessin.pantalon(p)
    return None


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'vignettes':
        main_vignettes(sys.argv[2:])
    elif len(sys.argv) > 1 and sys.argv[1] == 'fiches':
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        main_fiches(sys.argv[2:])
    elif len(sys.argv) > 1 and sys.argv[1] == 'planches':
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        main_planches(sys.argv[2:])
    elif len(sys.argv) > 1 and sys.argv[1] == 'dessins':
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        main_dessins(sys.argv[2:])
    else:
        main()
