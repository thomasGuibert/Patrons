"""Contours des pièces d'un patron, évalués hors Seamly, avec leurs points nommés et leurs crans.

Usage : python3 outils/coherence/pieces.py patrons/<patron>.sm2d
        affiche, pour chaque pièce, ses points dans l'ordre du contour, la longueur cumulée et
        les crans : de quoi écrire le fichier patrons/<patron>.coherence.toml.
"""
import math, os, sys

RACINE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(RACINE, '.claude', 'skills', 'tracer-sm2d'))
import evaluer_hors_seamly as ev  # noqa: E402

# courbes finement échantillonnées : l'angle entre deux pas voisins reste sous 0,1°
ev.ECHANTILLONS = 2000


class Piece:
    """Ligne de couture fermée : pts (cm, y vers le haut), repere[nom] = indice dans pts, crans."""

    def __init__(self, nom, pts, repere, crans):
        self.nom, self.pts, self.repere, self.crans = nom, pts, repere, crans
        self.cumul = [0.0]
        for i in range(len(pts)):
            self.cumul.append(self.cumul[-1] + math.dist(pts[i], pts[(i + 1) % len(pts)]))
        self.tour = self.cumul[-1]

    def indices(self, a, b):
        """Indices du contour de a à b, par le plus court des deux chemins."""
        ia, ib = self.repere[a], self.repere[b]
        n = len(self.pts)
        avant = (self.cumul[ib] - self.cumul[ia]) % self.tour
        if avant <= self.tour / 2:
            return [(ia + k) % n for k in range((ib - ia) % n + 1)]
        return [(ia - k) % n for k in range((ia - ib) % n + 1)]

    def troncon(self, a, b):
        """Polyligne de a à b, et position (cm depuis a) des crans qu'elle porte, extrémités exclues."""
        idx = self.indices(a, b)
        pts = [self.pts[i] for i in idx]
        long, crans = 0.0, []
        for k, i in enumerate(idx):
            if k:
                long += math.dist(pts[k - 1], pts[k])
            if 0 < k < len(idx) - 1 and i in self.crans:
                crans.append((long, self.crans[i]))
        return pts, crans


def _coupe(v, p):
    """Indice de l'échantillon de la courbe v le plus proche de p, si p est sur la courbe."""
    i = min(range(len(v)), key=lambda i: math.dist(v[i], p))
    for j in (i - 1, i):
        if 0 <= j < len(v) - 1:
            a, b = v[j], v[j + 1]
            ux, uy = b[0] - a[0], b[1] - a[1]
            n = ux * ux + uy * uy
            t = max(0, min(1, ((p[0] - a[0]) * ux + (p[1] - a[1]) * uy) / n)) if n else 0
            if math.dist(p, (a[0] + t * ux, a[1] + t * uy)) < 0.01:
                return i
    return None


def _recule(p, a, b):
    """Vrai si le point p est sur le segment b–a, avant a : a dépasse p, qu'on rejoint depuis b."""
    ux, uy = a[0] - b[0], a[1] - b[1]
    t = ((p[0] - b[0]) * ux + (p[1] - b[1]) * uy) / (ux * ux + uy * uy)
    return 0 < t < 1 - 1e-9 and math.dist(p, (b[0] + t * ux, b[1] + t * uy)) < 0.01


def pieces(motif):
    """Pièces du patron évalué (un evaluer_hors_seamly.Pattern), hors carré de contrôle."""
    copie = {}
    for b in motif.root.iter('draftBlock'):
        for e in b.find('modeling'):
            copie[e.get('id')] = e.get('idObject')
    res = {}
    for pc in motif.root.iter('piece'):
        if pc.get('seamAllowance') == 'false':
            continue
        seq = []
        for n in pc.iter('node'):
            o = copie[n.get('idObject')]
            if n.get('type') == 'NodePoint':
                seq.append(('P', motif.P[o], motif.name[o], n.get('notch') == 'true'))
            else:
                c = list(motif.curve_by_id[o])
                seq.append(('C', c[::-1] if n.get('reverse') == '1' else c, None, False))
        pts, repere, crans = [], {}, {}

        def ajouter(q):
            if not pts or math.dist(q, pts[-1]) > 1e-6:
                pts.append(q)
            return len(pts) - 1

        for k, (t, v, nom, cran) in enumerate(seq):
            if t == 'P':
                i = ajouter(v)
                repere[nom] = i
                if cran:
                    crans[i] = nom
                continue
            # comme Seamly : courbe coupée aux points voisins qui sont dessus, entière sinon
            prec, suiv = seq[k - 1], seq[(k + 1) % len(seq)]
            i0 = _coupe(v, prec[1]) if prec[0] == 'P' else None
            i1 = _coupe(v, suiv[1]) if suiv[0] == 'P' else None
            i0 = 0 if i0 is None else i0
            i1 = len(v) - 1 if i1 is None else i1
            morceau = v[i0:i1 + 1] if i1 >= i0 else v[i1:i0 + 1][::-1]
            # l'échantillon le plus proche peut dépasser le point voisin : pas de retour en arrière
            if prec[0] == 'P' and len(morceau) > 2 and _recule(prec[1], morceau[0], morceau[1]):
                morceau = morceau[1:]
            if suiv[0] == 'P' and len(morceau) > 2 and _recule(suiv[1], morceau[-1], morceau[-2]):
                morceau = morceau[:-1]
            for q in morceau:
                ajouter(q)
        if len(pts) > 1 and math.dist(pts[0], pts[-1]) < 1e-6:
            pts.pop()
            repere = {n: (i if i < len(pts) else 0) for n, i in repere.items()}
            crans = {(i if i < len(pts) else 0): n for i, n in crans.items()}
        # points du tracé par lesquels passe une courbe du contour (bouts de courbes, points de chemin)
        grille = {}
        for i, q in enumerate(pts):
            grille.setdefault((math.floor(q[0] * 100), math.floor(q[1] * 100)), []).append(i)
        for o, q in motif.P.items():
            if motif.name[o] in repere:
                continue
            gx, gy = math.floor(q[0] * 100), math.floor(q[1] * 100)
            proches = [i for dx in (-1, 0, 1) for dy in (-1, 0, 1) for i in grille.get((gx + dx, gy + dy), [])
                       if math.dist(q, pts[i]) < 1e-3]
            if proches:
                repere[motif.name[o]] = proches[0]
        res[pc.get('name')] = Piece(pc.get('name'), pts, repere, crans)
    return res


def main():
    motif = ev.Pattern(sys.argv[1])
    for nom, p in pieces(motif).items():
        print(f'== {nom} : couture {p.tour:.2f} cm')
        for n, i in sorted(p.repere.items(), key=lambda kv: kv[1]):
            print(f'  {n:8s} {p.cumul[i]:7.2f}{"  cran" if i in p.crans else ""}')


if __name__ == '__main__':
    main()
