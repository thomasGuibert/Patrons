"""Générateur de patrons/bolero.sm2d (base du mannequin, fond tailleur, manche tailleur, boléro).

Chaque appel d'outil porte la phrase du livre qu'il trace ; la liste sert aussi à écrire le
fichier d'étapes.
"""
import sys
from xml.sax.saxutils import quoteattr

ETAPES = []  # (bloc, nom, geste, formule, source)


class Bloc:
    def __init__(self, f, nom):
        self.f = f
        self.nom = nom
        self.calc = []
        self.mod = []
        self.pieces = []

    # ---------- outils ----------
    def _pt(self, name, typ, src, geste, formule='', ligne='none', **attrs):
        i = self.f.nid()
        self.f.ids[name] = i
        a = dict(id=i, name=name, type=typ, mx='0.132292', my='0.264583', showPointName='true')
        a.update(attrs)
        if typ not in ('single', 'lineIntersect', 'pointOfIntersectionCircles', 'pointOfContact',
                       'curveIntersectAxis_noline'):
            a.update(lineColor='black', lineType=ligne, lineWeight='0.35')
        self.calc.append('<point ' + ' '.join(f'{k}={quoteattr(str(v))}' for k, v in a.items()) + '/>')
        ETAPES.append((self.nom, name, geste, formule, src))
        return name

    def I(self, n):
        return self.f.ids[n]

    def single(self, n, x, y, src='', geste='Point de départ'):
        return self._pt(n, 'single', src, geste, f'({x}, {y})', x=x, y=y)

    def end(self, n, base, angle, length, src='', ligne='none'):
        return self._pt(n, 'endLine', src, f'depuis {base}, angle {angle}', length, ligne,
                        basePoint=self.I(base), angle=angle, length=length)

    def along(self, n, p1, p2, length, src='', ligne='none'):
        return self._pt(n, 'alongLine', src, f'sur {p1}{p2}', length, ligne,
                        firstPoint=self.I(p1), secondPoint=self.I(p2), length=length)

    def normal(self, n, p1, p2, length, angle, src='', ligne='none'):
        return self._pt(n, 'normal', src, f'perpendiculaire en {p1} à {p1}{p2}', length, ligne,
                        firstPoint=self.I(p1), secondPoint=self.I(p2), length=length, angle=angle)

    def inter(self, n, a1, a2, b1, b2, src=''):
        return self._pt(n, 'lineIntersect', src, f'{a1}{a2} ∩ {b1}{b2}', '',
                        p1Line1=self.I(a1), p2Line1=self.I(a2), p1Line2=self.I(b1), p2Line2=self.I(b2))

    def axe(self, n, base, angle, l1, l2, src='', ligne='none'):
        return self._pt(n, 'lineIntersectAxis', src, f'depuis {base}, angle {angle}, jusqu\'à {l1}{l2}', '', ligne,
                        basePoint=self.I(base), angle=angle, p1Line=self.I(l1), p2Line=self.I(l2))

    def contact(self, n, centre, l1, l2, rayon, src=''):
        return self._pt(n, 'pointOfContact', src, f'cercle ({centre}, r) ∩ {l1}{l2}', rayon,
                        center=self.I(centre), firstPoint=self.I(l1), secondPoint=self.I(l2), radius=rayon)

    def cercles(self, n, c1, r1, c2, r2, cross, src=''):
        return self._pt(n, 'pointOfIntersectionCircles', src, f'cercles ({c1}) ∩ ({c2})', f'{r1} ; {r2}',
                        c1Center=self.I(c1), c2Center=self.I(c2), c1Radius=r1, c2Radius=r2, crossPoint=cross)

    def courbe_axe(self, n, base, angle, courbe, src='', ligne='none'):
        return self._pt(n, 'curveIntersectAxis', src, f'depuis {base}, angle {angle}, jusqu\'à la courbe {courbe}', '', ligne,
                        basePoint=self.I(base), angle=angle, curve=self.f.ids[courbe])

    def coupe(self, n, chemin, longueur, src=''):
        return self._pt(n, 'cutSplinePath', src, f'sur la courbe {chemin}', longueur, splinePath=self.f.ids[chemin], length=longueur)

    def ligne(self, a, b, typ='none'):
        i = self.f.nid()
        self.calc.append(f'<line id="{i}" firstPoint="{self.I(a)}" secondPoint="{self.I(b)}" '
                         f'lineColor="black" lineType="{typ}" lineWeight="0.35"/>')

    def spl(self, nom, p1, p4, a1, l1, a2, l2, src='', trait='solidLine'):
        """Courbe simple ; a2/l2 : poignée partant de p4."""
        i = self.f.nid()
        self.f.ids[nom] = i
        self.calc.append(f'<spline id="{i}" type="simpleInteractive" point1="{self.I(p1)}" point4="{self.I(p4)}" '
                         f'angle1={quoteattr(a1)} length1={quoteattr(l1)} angle2={quoteattr(a2)} length2={quoteattr(l2)} '
                         f'color="black" lineWeight="0.35" penStyle="{trait}"/>')
        ETAPES.append((self.nom, nom, f'courbe {p1}–{p4}', '', src))
        return nom

    def chemin(self, nom, pts, src='', trait='solidLine'):
        """pts : liste (point, angle_sortie, long_avant, long_apres) ; angle1 = angle+180."""
        i = self.f.nid()
        self.f.ids[nom] = i
        corps = ''
        for p, ang, la, lb in pts:
            corps += (f'<pathPoint pSpline="{self.I(p)}" angle1={quoteattr(f"({ang})+180")} length1={quoteattr(la)} '
                      f'angle2={quoteattr(ang)} length2={quoteattr(lb)}/>')
        self.calc.append(f'<spline id="{i}" type="pathInteractive" color="black" lineWeight="0.35" penStyle="{trait}">{corps}</spline>')
        ETAPES.append((self.nom, nom, 'courbe ' + '–'.join(p for p, *_ in pts), '', src))
        return nom

    def rotation(self, centre, angle, objets, suffixe):
        i = self.f.nid()
        src = ''.join(f'<item idObject="{self.I(o)}"/>' for o in objets)
        dst = ''
        for o in objets:
            j = self.f.nid()
            self.f.ids[o + suffixe] = j
            dst += f'<item idObject="{j}" mx="0.132292" my="0.264583"/>'
        self.calc.append(f'<operation id="{i}" type="rotation" center="{self.I(centre)}" angle={quoteattr(angle)} '
                         f'suffix="{suffixe}"><source>{src}</source><destination>{dst}</destination></operation>')

    def deplacement(self, angle, longueur, objets, suffixe):
        i = self.f.nid()
        src = ''.join(f'<item idObject="{self.I(o)}"/>' for o in objets)
        dst = ''
        for o in objets:
            j = self.f.nid()
            self.f.ids[o + suffixe] = j
            dst += f'<item idObject="{j}" mx="0.132292" my="0.264583"/>'
        self.calc.append(f'<operation id="{i}" type="moving" angle={quoteattr(angle)} length={quoteattr(longueur)} '
                         f'suffix="{suffixe}"><source>{src}</source><destination>{dst}</destination></operation>')

    # ---------- pièces ----------
    def piece(self, nom, noeuds, qte=1, pli=False, couture=1, info=None, inlayout=True, chemins=()):
        """noeuds : liste de ('p', point) | ('c', courbe, reverse) | ('cp', chemin, reverse),
        avec option dict(notch=True) en 4e position pour un point."""
        nodes = ''
        for nd in noeuds:
            kind = nd[0]
            if kind == 'p':
                mid = self.f.nid()
                self.mod.append(f'<point id="{mid}" idObject="{self.I(nd[1])}" inUse="true" type="modeling" '
                                f'mx="0.132292" my="0.264583" showPointName="true"/>')
                extra = ''
                if len(nd) > 2 and nd[2].get('notch'):
                    extra = (' notch="true" notchType="slit" notchSubtype="straightforward" notchLength="0.6" '
                             f'notchWidth="0.25" notchAngle="0" notchCount="{nd[2].get("count", 1)}" showNotch="true" showSecondNotch="true"')
                if len(nd) > 2 and nd[2].get('sa'):
                    av, ap = nd[2]['sa']
                    extra += f' before="{av}" after="{ap}"'
                nodes += f'<node idObject="{mid}" type="NodePoint"{extra}/>'
            else:
                mid = self.f.nid()
                t = 'modelingSpline' if kind == 'c' else 'modelingPath'
                self.mod.append(f'<spline id="{mid}" idObject="{self.f.ids[nd[1]]}" inUse="true" type="{t}"/>')
                nt = 'NodeSpline' if kind == 'c' else 'NodeSplinePath'
                nodes += f'<node idObject="{mid}" reverse="{1 if nd[2] else 0}" type="{nt}"/>'
        ipaths = ''
        if chemins:
            ipaths = '<iPaths>' + ''.join(f'<record path="{self.f.ids[c]}"/>' for c in chemins) + '</iPaths>'
        info = info or {}
        dx, dy = info.get('data', (0, 0))
        px, py = info.get('pinfo', (0, 0))
        gx, gy, gl = info.get('grain', (0, 0, 10))
        matiere = info.get('matiere', 'Tissu')
        dw, dh = info.get('data_dim', (7, 2.5))
        pw, ph = info.get('pinfo_dim', (7, 3))
        i = self.f.nid()
        self.pieces.append(
            f'<piece id="{i}" name={quoteattr(nom)} seamAllowance="{"true" if couture else "false"}" width="{couture}" '
            f'version="2" inLayout="{"true" if inlayout else "false"}" united="false" locked="false" forbidFlipping="false" '
            f'hideMainPath="false" color="#ffffff" fill="nobrush" mx="0" my="0">'
            f'<data annotation="" foldPosition="" fontSize="0" height="{dh}" letter="" mx="{dx * 37.795:.3f}" my="{dy * 37.795:.3f}" '
            f'onFold="{"true" if pli else "false"}" orientation="Indéfini" quantity="{qte}" rotation="0" rotationWay="Aucun" '
            f'tilt="Aucun" visible="true" width="{dw}">'
            f'<line alignment="4" bold="true" italic="false" sfIncrement="3" text="%pName%"/>'
            f'<line alignment="4" bold="false" italic="true" sfIncrement="0" text="x%pQuantity% {matiere}"/></data>'
            f'<patternInfo fontSize="0" height="{ph}" mx="{px * 37.795:.3f}" my="{py * 37.795:.3f}" rotation="0" visible="true" width="{pw}"/>'
            f'<grainline arrowLength="1" arrows="0" length="{gl}" mx="{gx * 37.795:.3f}" my="{gy * 37.795:.3f}" rotation="90" visible="true"/>'
            f'<nodes>{nodes}</nodes>{ipaths}</piece>')

    def chemin_interne(self, nom, points):
        i = self.f.nid()
        self.f.ids[nom] = i
        nodes = ''
        for p in points:
            mid = self.f.nid()
            self.mod.append(f'<point id="{mid}" idObject="{self.I(p)}" inUse="true" type="modeling" '
                            f'mx="0.132292" my="0.264583" showPointName="true"/>')
            nodes += f'<node idObject="{mid}" type="NodePoint"/>'
        self.mod.append(f'<path id="{i}" name={quoteattr(nom)} type="1" typeLine="solidLine" cut="false" '
                        f'firstToCountour="false" lastToCountour="false" visible="true"><nodes>{nodes}</nodes></path>')

    def xml(self):
        return (f'<draftBlock name={quoteattr(self.nom)}><calculation>' + '\n'.join(self.calc) +
                '</calculation><modeling>' + '\n'.join(self.mod) + '</modeling><pieces>' + '\n'.join(self.pieces) +
                '</pieces><groups/><images/></draftBlock>')


class Fichier:
    def __init__(self, mesures):
        self.n = 0
        self.ids = {}
        self.blocs = []
        self.vars = []
        self.mesures = mesures

    def nid(self):
        self.n += 1
        return self.n

    def var(self, nom, formule, desc):
        self.vars.append(f'<variable description={quoteattr(desc)} formula={quoteattr(str(formule))} name="#{nom}"/>')

    def bloc(self, nom):
        b = Bloc(self, nom)
        self.blocs.append(b)
        return b

    def xml(self, titre):
        return ('<?xml version="1.0" encoding="UTF-8"?>\n<pattern>\n<!--Généré par un script (fil Bases chaîne et trame femme), puis modifiable dans Seamly2D.-->\n'
                '<version>0.7.4</version><unit>cm</unit><description/><notes/>'
                f'<patternLabel><line alignment="1" bold="true" italic="false" sfIncrement="3" text={quoteattr(titre)}/>'
                '<line alignment="4" bold="false" italic="true" sfIncrement="0" text="T%size%"/>'
                '<line alignment="4" bold="false" italic="false" sfIncrement="0" text="%pName%"/></patternLabel>'
                f'<measurements>{self.mesures}</measurements><variables>' + '\n'.join(self.vars) + '</variables>\n' +
                '\n'.join(b.xml() for b in self.blocs) + '\n</pattern>\n')
