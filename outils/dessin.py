"""Dessin technique (flat sketch) du vêtement cousu, construit à partir des pièces du patron."""
import math, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

STYLES = {
    'papier':    dict(fond='#f6f1e7', tissu='#ffffff', trait='#2b2b2b', piqure='#8a8a8a'),
    'epure':     dict(fond='#ffffff', tissu='#ffffff', trait='#111111', piqure='#9a9a9a'),
    'ardoise':   dict(fond='#2f3437', tissu='#2f3437', trait='#f2efe9', piqure='#a9b0b3'),
    'blueprint': dict(fond='#1d3f6e', tissu='#1d3f6e', trait='#e8f1ff', piqure='#8fb3e3', grille='#2b5288'),
    'kraft':     dict(fond='#c9a77c', tissu='#f3e9d8', trait='#4a3423', piqure='#9c7b5c', ombre='#a8865d'),
    'sauge':     dict(fond='#dfe6dc', tissu='#c96f4a', trait='#3b2a22', piqure='#f3d9cb', ombre='#b9c4b5'),
    'indigo':    dict(fond='#f4f1ec', tissu='#2e4a7d', trait='#16243d', piqure='#a9bde0', ombre='#e2ddd4'),
    'moutarde':  dict(fond='#1f2a2e', tissu='#d9a441', trait='#1f2a2e', piqure='#7a5a1c'),
}


def miroir(pts):
    return [(-x, y) for x, y in pts]


def decale(pts, dist):
    """Décale une polyligne de `dist` vers sa gauche (sens de parcours)."""
    out = []
    for i, p in enumerate(pts):
        a = pts[max(i - 1, 0)]; b = pts[min(i + 1, len(pts) - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1
        out.append((p[0] - dy / L * dist, p[1] + dx / L * dist))
    return out


def lisse(pts, n=8):
    """Chaikin : arrondit légèrement une polyligne ouverte."""
    for _ in range(n // 4):
        q = [pts[0]]
        for a, b in zip(pts, pts[1:]):
            q += [(0.75 * a[0] + 0.25 * b[0], 0.75 * a[1] + 0.25 * b[1]),
                  (0.25 * a[0] + 0.75 * b[0], 0.25 * a[1] + 0.75 * b[1])]
        q.append(pts[-1])
        pts = q
    return pts


class Dessin:
    def __init__(self):
        self.formes = []   # (pts, fermé)
        self.piqures = []
        self.lignes = []

    def forme(self, pts):
        self.formes.append(pts)

    def piqure(self, pts):
        self.piqures.append(pts)

    def ligne(self, pts):
        self.lignes.append(pts)

    def bornes(self):
        tous = [q for f in self.formes for q in f]
        return (min(q[0] for q in tous), max(q[0] for q in tous), min(q[1] for q in tous), max(q[1] for q in tous))

    def decale(self, dx, dy):
        T = lambda L: [(x + dx, y + dy) for x, y in L]
        d = Dessin()
        d.formes = [T(f) for f in self.formes]; d.piqures = [T(f) for f in self.piqures]; d.lignes = [T(f) for f in self.lignes]
        return d


def rendre(vues, chemin_base, taille_px=800, style='papier', ax=None, legendes=False, cadre=1.15, haut=0.0):
    st = STYLES[style]
    gap, x0, places = 8, 0, []
    for v in vues:
        xmin, xmax, ymin, ymax = v.bornes()
        places.append(v.decale(x0 - xmin, -ymin))
        x0 += xmax - xmin + gap
    W = x0 - gap
    H = max(v.bornes()[3] for v in places)
    cote = max(W, H) * cadre
    seul = ax is None
    if seul:
        fig = plt.figure(figsize=(taille_px / 100, taille_px / 100), dpi=100)
        ax = fig.add_axes([0, 0, 1, 1])
        fig.patch.set_facecolor(st['fond'])
    x0_, y0_ = W / 2 - cote / 2, H / 2 - cote / 2 + cote * haut
    ax.set_xlim(x0_, x0_ + cote); ax.set_ylim(y0_, y0_ + cote)
    ax.set_aspect('equal'); ax.axis('off')
    ax.add_patch(plt.Rectangle((x0_, y0_), cote, cote, fc=st['fond'], ec='none', zorder=0))
    if 'grille' in st:
        pas = 5
        k0 = math.floor(x0_ / pas)
        for i in range(int(cote / pas) + 2):
            ax.plot([(k0 + i) * pas] * 2, [y0_, y0_ + cote], color=st['grille'], lw=0.6, zorder=0.5)
        k0 = math.floor(y0_ / pas)
        for i in range(int(cote / pas) + 2):
            ax.plot([x0_, x0_ + cote], [(k0 + i) * pas] * 2, color=st['grille'], lw=0.6, zorder=0.5)
    lw = taille_px / 320
    for v in places:
        if 'ombre' in st:
            for f in v.formes:
                ax.fill(*zip(*[(x + cote * 0.012, y - cote * 0.012) for x, y in f]), fc=st['ombre'], ec='none', zorder=1)
        for f in v.formes:
            ax.fill(*zip(*f), fc=st['tissu'], ec=st['trait'], lw=lw, joinstyle='round', zorder=2)
        for f in v.lignes:
            ax.plot(*zip(*f), color=st['trait'], lw=lw * 0.6, solid_capstyle='round', zorder=3)
        for f in v.piqures:
            ax.plot(*zip(*f), color=st['piqure'], lw=lw * 0.5, linestyle=(0, (3, 2.5)), zorder=3)
    if legendes:
        for v, txt in zip(places, ('devant', 'dos')):
            xmin, xmax, ymin, _ = v.bornes()
            ax.text((xmin + xmax) / 2, ymin - cote * 0.03, txt, ha='center', va='top',
                    fontsize=taille_px / 62, color=st['trait'])
    if seul:
        for ext in ('png', 'svg'):
            fig.savefig(f'{chemin_base}.{ext}', dpi=100, facecolor=st['fond'])
        plt.close(fig)


def planche(vues_par_patron, chemin, taille_px=400):
    """Planche de comparaison : une ligne par patron, une colonne par style."""
    noms = list(STYLES)
    n, m = len(vues_par_patron), len(noms)
    fig, axs = plt.subplots(n, m, figsize=(m * taille_px / 100, n * taille_px / 100 + 0.5), dpi=100)
    fig.patch.set_facecolor('#ffffff')
    for i, vues in enumerate(vues_par_patron):
        for j, s in enumerate(noms):
            rendre(vues, None, taille_px, s, ax=axs[i][j])
            if i == 0:
                axs[i][j].set_title(s, fontsize=16, pad=8)
    fig.subplots_adjust(left=0.005, right=0.995, bottom=0.005, top=0.94, wspace=0.03, hspace=0.03)
    fig.savefig(chemin, dpi=100, facecolor='#ffffff')
    plt.close(fig)


# ---------------- haut (fond de base maille) ----------------
def haut(p):
    N = {n: q for n, q in p.points.values()}
    C = {c['nom']: c['pts'] for c in p.courbes.values()}
    def spl(a, b):
        for k, v in C.items():
            if k.startswith('Spl') and k.endswith(f'_{a}_{b}'):
                return list(v)
            if k.startswith('Spl') and k.endswith(f'_{b}_{a}'):
                return list(reversed(v))
    ox = N['E'][0]                       # milieu devant / dos
    T = lambda L: [(x - ox, y) for x, y in L]
    manche_long = math.dist(N['mA'], N['mC'])
    manche_dessous = math.dist(N['mI'], N['mIp']) / 2
    manche_bas = math.dist(N['mF1'], N['mF2']) / 2
    vues = []
    for nom, encolure, emmanchure in (('devant', ('H', 'E1', 'E'), C['SplPath_K_C3_1']),
                                      ('dos', ('H', 'F1', 'F'), C['SplPath_K_C3'])):
        h, e1, e = encolure
        col = T(spl(h, e1) + [N[e]])                     # H -> milieu
        emm = T(emmanchure)                              # K -> C3
        cote = T([N['C3'], N['C2'], N['C1'], N['B1'], N['A1'], N['A']])
        K, H_ = T([N['K']])[0], T([N['H']])[0]
        # demi-corps gauche (x < 0), contour : milieu encolure -> H -> K -> emmanchure -> côté -> bas milieu
        demi = list(reversed(col)) + [K] + emm[1:] + cote[1:]
        corps = demi + list(reversed(miroir(demi)))[1:-1]
        d = Dessin()
        d.forme(corps)
        # manches (gauche puis miroir)
        a = math.radians(243)
        u = (math.cos(a), math.sin(a)); n = (-u[1], u[0])          # n : vers le corps
        poignet_ext = (K[0] + manche_long * u[0], K[1] + manche_long * u[1])
        poignet_int = (poignet_ext[0] + manche_bas * n[0], poignet_ext[1] + manche_bas * n[1])
        dessous = emm[-1]
        manche = [K, poignet_ext, poignet_int, dessous] + list(reversed(emm))[1:-1]
        poignet_p = [(poignet_ext[0] - 2.5 * u[0], poignet_ext[1] - 2.5 * u[1]),
                     (poignet_int[0] - 2.5 * u[0], poignet_int[1] - 2.5 * u[1])]
        for f in (lambda L: L, miroir):
            d.forme(f(manche))
            d.piqure(f(poignet_p))
        # ourlet du bas (pas de col : le patron n'a pas de pièce d'encolure)
        yb = T([N['A']])[0][1] + 2.5
        xa = T([N['A1']])[0][0]
        d.piqure([(xa + 0.3, yb), (-xa - 0.3, yb)])
        vues.append(d)
    return vues


# ---------------- pantalon (fond de pantalon droit) ----------------
def pantalon(p):
    N = {n: q for n, q in p.points.values()}
    L = lambda a, b: math.dist(N[a], N[b])
    yA = N['F'][1]
    niv = {
        'taille': (yA, (L('A2', 'A3') + L('A5', 'B5')) / 2),
        'hanches': (N['B'][1], (L('B1', 'B2') + L('B4', 'B3')) / 2),
        'fourche': (N['C'][1], (L('C1', 'C2') + L('C4', 'C3')) / 2),
        'genou': (N['D'][1], (L('D1', 'D2') + L('D3', 'D4')) / 2),
        'bas': (N['E'][1], (L('E1', 'E2') + L('E3', 'E4')) / 2),
    }
    yt, wt = niv['taille']; yh, wh = niv['hanches']; yf, wf = niv['fourche']
    yg, wg = niv['genou']; yb, wb = niv['bas']
    vues = []
    for nom in ('devant', 'dos'):
        # jambe gauche : entrejambe de la fourche au bas (léger écart), côté extérieur droit
        xb_int = -0.12 * wb
        xb_ext = xb_int - wb
        ext = lisse([(-wt, yt), (-wh, yh), (xb_ext, yb)])
        jambe = [(0, yt)] + ext + [(xb_int, yb), (0, yf)]
        d = Dessin()
        corps = jambe + list(reversed(miroir(jambe)))[1:-1]
        d.forme(corps)
        # pas de ceinture : le patron n'a pas de pièce de ceinture
        # couture milieu devant / dos, ourlets
        d.ligne([(0, yt), (0, yf)])
        for sg in (1, -1):
            d.piqure([(sg * (xb_ext + 0.4), yb + 3), (sg * (xb_int - 0.4), yb + 3)])
        vues.append(d)
    return vues
