"""Dossier technique placé devant les pièces du patron : informations et tableau des mesures,
coupe, matériel et fournitures avec le métrage, plan des valeurs de couture, nomenclature, puis la
gamme de montage, au choix « pro » (tableau opération, schéma, outil, commentaire, point de
contrôle) ou « amateur » (pas à pas illustré).

Le contenu rédigé vient de patrons/<nom>.dossier.toml ; les pièces (formes, valeurs de couture,
quantités) viennent de l'export SVG des pièces et du .sm2d, sans géométrie recalculée.
Toujours en A4 portrait, même devant un patron en A3.

Usage : python3 dossier.py <nom>_pieces.svg <fichier.sm2d> sortie.pdf [--montage pro|amateur]
                            [--mesures <fichier .smms|.vit>] [--taille 40|T-Thomas]
"""
import argparse, glob, math, os, re, sys, tomllib
import xml.etree.ElementTree as ET
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, CondPageBreak, Flowable, Frame, KeepTogether, PageBreak,
                                PageTemplate, Paragraph, Spacer, Table, TableStyle)

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.abspath(os.path.join(ICI, '..', '..', '..'))
sys.path.insert(0, os.path.join(ICI, '..', 'tracer-sm2d'))
from pdf_depuis_seamly import PX_CM, lire_svg  # noqa: E402

CM = 72 / 2.54
W, H = A4
MARGE = 1.8 * CM

# charte Atelier AT : encre sur papier blanc, rouge garance en touche, bleu de travail
ENCRE = colors.HexColor('#14110e')
GARANCE = colors.HexColor('#a8321f')
BLEU = colors.HexColor('#1c2f4d')
GRIS = colors.HexColor('#6b6660')
FILET = colors.HexColor('#c9c2b6')
FOND = colors.HexColor('#efe9de')

POLICES = os.path.join(RACINE, 'outils', 'polices')
for nom, fichier in (('Titre', 'IMFeFCrm28P.ttf'), ('Capitales', 'IMFeENsc28P.ttf'),
                     ('Texte', 'SortsMillGoudy-Regular.ttf'), ('Texte-Italique', 'SortsMillGoudy-Italic.ttf'),
                     ('Mesure', 'CourierPrime-Regular.ttf'), ('Mesure-Gras', 'CourierPrime-Bold.ttf')):
    pdfmetrics.registerFont(TTFont(nom, os.path.join(POLICES, fichier)))
pdfmetrics.registerFontFamily('Texte', normal='Texte', italic='Texte-Italique', bold='Texte', boldItalic='Texte-Italique')

S = {
    'titre': ParagraphStyle('titre', fontName='Titre', fontSize=26, leading=30, alignment=TA_CENTER, textColor=ENCRE),
    'sous': ParagraphStyle('sous', fontName='Capitales', fontSize=15, leading=18, alignment=TA_CENTER, textColor=GARANCE),
    'h': ParagraphStyle('h', fontName='Capitales', fontSize=14, leading=17, textColor=ENCRE, spaceBefore=10, spaceAfter=2),
    'texte': ParagraphStyle('texte', fontName='Texte', fontSize=10.5, leading=14, textColor=ENCRE),
    'liste': ParagraphStyle('liste', fontName='Texte', fontSize=10.5, leading=14, textColor=ENCRE, leftIndent=10, bulletIndent=0),
    'cellule': ParagraphStyle('cellule', fontName='Texte', fontSize=9, leading=11, textColor=ENCRE),
    'entete': ParagraphStyle('entete', fontName='Capitales', fontSize=9.5, leading=11, alignment=TA_CENTER, textColor=ENCRE),
    'centre': ParagraphStyle('centre', fontName='Texte', fontSize=9, leading=11, alignment=TA_CENTER, textColor=ENCRE),
    'etape': ParagraphStyle('etape', fontName='Titre', fontSize=15, leading=18, textColor=ENCRE, spaceBefore=4, spaceAfter=3),
    'pas': ParagraphStyle('pas', fontName='Texte', fontSize=11, leading=15, textColor=ENCRE, spaceAfter=4),
    'note': ParagraphStyle('note', fontName='Texte-Italique', fontSize=9.5, leading=12, textColor=GRIS),
}

# libellés publics des mesures du corps (mêmes que src/tailles.ts)
LIBELLES = {
    'bust_circ': 'Tour de poitrine', 'waist_circ': 'Tour de taille', 'hip_circ': 'Tour de hanches',
    'neck_circ': "Tour d'encolure", 'height_waist_side': 'Hauteur taille-sol',
    'arm_shoulder_tip_to_wrist': 'Longueur de bras', 'leg_crotch_to_floor': 'Hauteur entrejambe-sol',
}


def cm(v):
    """12.5 -> « 12,5 » ; 12.0 -> « 12 »."""
    return ('%.1f' % v).rstrip('0').rstrip('.').replace('.', ',')


# ---------------------------------------------------------------- mesures
def lire_mesures(chemin):
    """Valeurs d'un fichier de mesures : .smms (taille de base) ou .vit (individuel)."""
    txt = open(chemin, encoding='utf-8').read()
    if chemin.endswith('.vit'):
        return {n: float(v) for n, v in re.findall(r'<m name="([^"]+)" value="([-\d.]+)"', txt)}
    return {n: float(b) for b, n in re.findall(r'<m base="([-\d.]+)"[^>]* name="([^"]+)"', txt)}


def tableau_gamme(gamme):
    """{taille: {mesure: cm}} pour toutes les tailles de mesures/<gamme>/T*.smms."""
    res = {}
    for f in glob.glob(os.path.join(RACINE, 'mesures', gamme, 'T*.smms')):
        res[int(re.search(r'T(\d+)\.smms$', f).group(1))] = lire_mesures(f)
    return dict(sorted(res.items()))


# ---------------------------------------------------------------- pièces
def largeurs(sm2d):
    """Valeur de couture courante (la plus fréquente des pièces) et d'ourlet (la plus grande des
    valeurs posées sur un bord), pour les textes {couture} et {ourlet} du dossier."""
    courantes, bords = [], []
    for pc in ET.parse(sm2d).getroot().iter('piece'):
        if pc.get('seamAllowance') != 'true':
            continue
        courantes.append(float(pc.get('width') or 0))
        # une formule (ex. #haut_elastique, repli de coulisse) n'est pas un ourlet : ignorée
        bords += [float(n.get(k)) for n in pc.iter('node') for k in ('before', 'after')
                  if re.fullmatch(r'[\d.]+', n.get(k) or '')]
    couture = max(set(courantes), key=courantes.count) if courantes else 1
    return {'couture': cm(couture), 'ourlet': cm(max(bords + [couture]))}


def infos_pieces(sm2d):
    """Pièces du .sm2d dans l'ordre du fichier : nom -> (quantité, au pli)."""
    res = {}
    for pc in ET.parse(sm2d).getroot().iter('piece'):
        d = pc.find('data')
        if d is None or pc.get('seamAllowance') != 'true':
            continue
        res[pc.get('name')] = (int(d.get('quantity') or 1), d.get('onFold') == 'true')
    return res


def contours(pc):
    """Ligne de couture et ligne de coupe d'une pièce exportée (cm, y vers le bas) : les deux plus
    grands tracés non remplis ; la coupe est la plus grande."""
    traces = []
    for style, cmds in pc['chemins']:
        if style.get('fill', 'black') != 'none' and style.get('fill') is not None:
            continue
        pts = []
        for op, v in cmds:
            if op == 'M' and pts:
                break                         # un seul sous-tracé : crans et droit-fil sont à part
            if op in ('M', 'L'):
                pts.append((v[0] / PX_CM, v[1] / PX_CM))
            elif op == 'C':
                p0 = pts[-1]
                for k in range(1, 9):
                    t = k / 8
                    pts.append(tuple((1 - t) ** 3 * p0[i] + 3 * (1 - t) ** 2 * t * v[i] / PX_CM
                                     + 3 * (1 - t) * t ** 2 * v[2 + i] / PX_CM + t ** 3 * v[4 + i] / PX_CM for i in (0, 1)))
        if len(pts) > 3:
            traces.append(pts)
    aire = lambda p: abs(sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(p, p[1:] + p[:1]))) / 2
    traces.sort(key=aire, reverse=True)
    return (traces[1], traces[0]) if len(traces) > 1 else (traces[0], traces[0])


def dist_polyligne(p, poly):
    best = 1e9
    for a, b in zip(poly, poly[1:] + poly[:1]):
        dx, dy = b[0] - a[0], b[1] - a[1]
        l2 = dx * dx + dy * dy
        t = 0 if l2 == 0 else max(0, min(1, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / l2))
        best = min(best, math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy))
    return best


def valeurs_couture(couture, coupe):
    """Tronçons de la ligne de couture de même valeur de couture, coupés aux angles :
    [(valeur cm, [points])]. La valeur est l'écart entre couture et coupe, lu sur l'export."""
    pts = [p for i, p in enumerate(couture) if i == 0 or math.dist(p, couture[i - 1]) > 1e-6]
    if math.dist(pts[0], pts[-1]) < 1e-6:
        pts.pop()
    n = len(pts)
    segs = []
    for i in range(n):
        a, b = pts[i], pts[(i + 1) % n]
        m = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        segs.append((round(dist_polyligne(m, coupe) * 10) / 10, a, b))

    def angle(i):
        """Changement de direction au sommet i (degrés)."""
        a, b, c = pts[i - 1], pts[i], pts[(i + 1) % n]
        u = math.atan2(b[1] - a[1], b[0] - a[0]); v = math.atan2(c[1] - b[1], c[0] - b[0])
        return abs((math.degrees(v - u) + 180) % 360 - 180)

    coupures = [i for i in range(n) if segs[i][0] != segs[i - 1][0] or angle(i) > 35]
    if not coupures:
        coupures = [0]
    troncons = []
    for k, i in enumerate(coupures):
        j = coupures[(k + 1) % len(coupures)]
        idx = list(range(i, j if j > i else j + n))
        chemin = [segs[q % n][1] for q in idx] + [segs[idx[-1] % n][2]]
        vals = [segs[q % n][0] for q in idx]
        troncons.append((max(set(vals), key=vals.count), chemin))
    return troncons


def longueur(chemin):
    return sum(math.dist(a, b) for a, b in zip(chemin, chemin[1:]))


def point_milieu(chemin):
    """Point à mi-longueur et direction du tronçon à cet endroit."""
    reste = longueur(chemin) / 2
    for a, b in zip(chemin, chemin[1:]):
        l = math.dist(a, b)
        if l >= reste and l > 0:
            t = reste / l
            return (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])), ((b[0] - a[0]) / l, (b[1] - a[1]) / l)
        reste -= l
    a, b = chemin[-2], chemin[-1]
    l = math.dist(a, b) or 1
    return b, ((b[0] - a[0]) / l, (b[1] - a[1]) / l)


# ---------------------------------------------------------------- métrage
def metrage(pieces, infos, laize, garde=None):
    """Longueur de tissu (cm), estimée en rangées : les pièces coupées en double ou au pli sur le
    tissu plié (laize / 2), les autres à plat sur toute la laize. Droit-fil dans la longueur du
    tissu (vertical à l'export). +10 % pour les raccords et le rétrécissement, arrondi aux 10 cm."""
    plie, plat = [], []
    for pc in pieces:
        if pc['nom'] not in infos or (garde and not garde(pc['nom'])):
            continue
        q, pli = infos[pc['nom']]
        x0, y0, x1, y1 = pc['bb']
        l, h = (x1 - x0) / PX_CM + 1, (y1 - y0) / PX_CM + 1
        if pli:
            plie += [(l, h)] * q                  # contre la pliure : une pièce entière à chaque fois
        elif q % 2 == 0 and l <= laize / 2:
            plie += [(l, h)] * (q // 2)           # deux épaisseurs : une paire symétrique par placement
        else:
            plat += [(l, h)] * q

    def rangees(rects, largeur):
        total, x, haut = 0, 0, 0
        for l, h in sorted(rects, key=lambda r: -r[1]):
            if x + l > largeur:
                total, x, haut = total + haut, 0, 0
            x, haut = x + l, max(haut, h)
        return total + haut

    brut = rangees(plie, laize / 2) + rangees(plat, laize)
    return math.ceil(brut * 1.1 / 10) * 10


# ---------------------------------------------------------------- dessins
class Image(Flowable):
    """Dessin technique, rogné à son contenu, centré dans la largeur donnée."""

    def __init__(self, chemin, largeur, hauteur_max):
        from PIL import Image as PImage
        im = PImage.open(chemin).convert('L')
        boite = im.point(lambda v: 255 if v < 250 else 0).getbbox()
        self.im = im.crop(boite) if boite else im
        l, h = self.im.size
        e = min(largeur / l, hauteur_max / h)
        self.w, self.h, self.largeur = l * e, h * e, largeur

    def wrap(self, *_):
        return self.largeur, self.h

    def draw(self):
        self.canv.drawImage(ImageReader(self.im), (self.largeur - self.w) / 2, 0, self.w, self.h)


class PlanCoutures(Flowable):
    """Pièces réduites (ligne de couture pleine, coupe en tirets) et valeur de couture de chaque bord."""

    def __init__(self, pieces, infos, largeur, hauteur):
        self.largeur, self.hauteur = largeur, hauteur
        self.pieces = []
        for pc in pieces:
            if pc['nom'] not in infos:
                continue
            couture, coupe = contours(pc)
            xs = [p[0] for p in coupe]; ys = [p[1] for p in coupe]
            self.pieces.append(dict(nom=pc['nom'], q=infos[pc['nom']], couture=couture, coupe=coupe,
                                    bb=(min(xs), min(ys), max(xs), max(ys)), troncons=valeurs_couture(couture, coupe)))
        self.echelle, self.places = self.ranger()

    def ranger(self):
        """Rangées de pièces à une même échelle, la plus grande qui tient (place pour les cotes)."""
        bord = 20                                 # pt autour de chaque pièce, pour les valeurs
        tailles = [(p['bb'][2] - p['bb'][0], p['bb'][3] - p['bb'][1]) for p in self.pieces]
        def essai(e):
            places, x, y, haut = [], 0, 0, 0
            for (l, h) in tailles:
                lw, hw = l * CM * e + 2 * bord, h * CM * e + 2 * bord + (36 if h * CM * e < 30 else 0)
                if x + lw > self.largeur and x > 0:
                    x, y, haut = 0, y + haut, 0
                places.append((x + bord, y + bord)); x += lw; haut = max(haut, hw)
            return places, y + haut
        e = 0.5
        while e > 0.02:
            places, h = essai(e)
            if h <= self.hauteur and all(l * CM * e + 40 <= self.largeur for l, _ in tailles):
                return e, places
            e *= 0.95
        return e, essai(e)[0]

    def wrap(self, *_):
        return self.largeur, self.hauteur

    def draw(self):
        c, e = self.canv, self.echelle
        for p, (px, py) in zip(self.pieces, self.places):
            x0, y0 = p['bb'][0], p['bb'][1]
            T = lambda q: (px + (q[0] - x0) * CM * e, self.hauteur - py - (q[1] - y0) * CM * e)
            def tracer(pts, tirets):
                ch = c.beginPath(); ch.moveTo(*T(pts[0]))
                for q in pts[1:]:
                    ch.lineTo(*T(q))
                ch.close()
                c.setDash(*((3, 2),) if tirets else ())
                c.drawPath(ch, stroke=1, fill=0)
            c.setStrokeColor(GARANCE); c.setLineWidth(0.6); tracer(p['coupe'], True)
            c.setStrokeColor(ENCRE); c.setLineWidth(1); tracer(p['couture'], False)
            c.setDash()
            # nom et quantité au centre
            xs = [q[0] for q in p['couture']]; ys = [q[1] for q in p['couture']]
            cx, cy = T(((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2))
            q, pli = p['q']
            if (max(ys) - min(ys)) * CM * e < 30:     # pièce mince : nom dessous
                cy = T((0, max(p['bb'][3], max(ys))))[1] - 24
            c.setFillColor(ENCRE); c.setFont('Texte', 9.5); c.drawCentredString(cx, cy + 2, p['nom'])
            c.setFont('Texte-Italique', 8.5)
            c.drawCentredString(cx, cy - 9, ('%d au pli' % q) if pli else '×%d' % q)
            # sens de parcours : la normale extérieure dépend de l'orientation du contour
            pts = p['couture']
            sens = -1 if sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(pts, pts[1:] + pts[:1])) > 0 else 1
            for val, chemin in p['troncons']:
                if longueur(chemin) * CM * e < (6 if val == 0 else 14):
                    continue
                (mx, my), (ux, uy) = point_milieu(chemin)
                nx, ny = -uy * sens, ux * sens            # extérieur, repère de la pièce (y vers le bas)
                ex, ey = T((mx, my))
                d = val * CM * e + 7
                tx, ty = ex + nx * d, ey - ny * d
                ang = math.degrees(math.atan2(-uy, ux))
                if ang > 90:
                    ang -= 180
                elif ang < -90:
                    ang += 180
                c.saveState(); c.translate(tx, ty); c.rotate(ang)
                c.setFillColor(GARANCE); c.setFont('Mesure', 7.5)
                c.drawCentredString(0, -2.5, 'pli' if val == 0 else '%s cm' % cm(val))
                c.restoreState()


class Schema(Flowable):
    """Petits schémas de montage, en coupe ou à plat : tissu en bleu de travail (endroit plein,
    envers clair), piqûres en garance."""

    def __init__(self, nom, largeur, hauteur, valeurs=None):
        self.nom, self.largeur, self.hauteur = nom, largeur, hauteur
        self.v = valeurs or {'couture': '0,7', 'ourlet': '2,5'}

    def wrap(self, *_):
        return self.largeur, self.hauteur

    # épaisseur de tissu vue en coupe : endroit plein (bleu), envers en clair
    def couche(self, x0, x1, y, endroit_dessus=True, label=None):
        c = self.canv
        c.setFillColor(BLEU if endroit_dessus else FOND); c.setStrokeColor(BLEU); c.setLineWidth(0.6)
        c.rect(x0, y, x1 - x0, 2, stroke=1, fill=1)
        c.setFillColor(FOND if endroit_dessus else BLEU)
        c.rect(x0, y - 2, x1 - x0, 2, stroke=1, fill=1)
        if label:
            c.setFillColor(GRIS); c.setFont('Texte-Italique', 7); c.drawString(x0, y + 5, label)

    def piqure(self, x, y0, y1):
        c = self.canv
        c.setStrokeColor(GARANCE); c.setLineWidth(1.1); c.line(x, y0, x, y1)

    def cote(self, x0, x1, y, texte):
        c = self.canv
        c.setStrokeColor(GRIS); c.setLineWidth(0.5); c.line(x0, y, x1, y)
        for x in (x0, x1):
            c.line(x, y - 2.5, x, y + 2.5)
        c.setFillColor(GRIS); c.setFont('Mesure', 7); c.drawCentredString((x0 + x1) / 2, y + 3.5, texte)

    def surjet(self, x, y0, y1):
        c = self.canv
        c.setStrokeColor(GARANCE); c.setLineWidth(0.6)
        n, pas = 5, (y1 - y0) / 5
        for k in range(n):
            ch = c.beginPath(); ch.moveTo(x - 4, y0 + k * pas)
            ch.curveTo(x + 6, y0 + k * pas, x + 6, y0 + (k + 1) * pas, x - 4, y0 + (k + 1) * pas)
            c.drawPath(ch, stroke=1, fill=0)

    REF = (110, 70)                       # boîte où chaque schéma est dessiné, mise ensuite à l'échelle

    def draw(self):
        c, (L, Hh) = self.canv, self.REF
        f = getattr(self, 's_' + self.nom, None)
        if not f:
            raise ValueError('schéma inconnu : ' + self.nom)
        e = min(self.largeur / L, self.hauteur / Hh)
        c.saveState()
        c.translate((self.largeur - L * e) / 2, (self.hauteur - Hh * e) / 2); c.scale(e, e)
        f(L, Hh)
        c.restoreState()

    def s_coupe(self, L, H):
        """Tissu plié, pièce posée contre la pliure, droit-fil parallèle à la lisière."""
        c = self.canv
        x0, x1, y0, y1 = 8, L - 8, 8, H - 14
        c.setStrokeColor(BLEU); c.setFillColor(FOND); c.setLineWidth(0.8)
        c.rect(x0, y0, x1 - x0, y1 - y0, stroke=1, fill=1)
        c.setFont('Texte-Italique', 7); c.setFillColor(GRIS)
        c.drawString(x0, y1 + 3, 'pliure'); c.drawRightString(x1, y1 + 3, 'lisières')
        c.setStrokeColor(BLEU); c.setLineWidth(2); c.line(x0, y1, x1, y1)
        px0, px1, py0 = x0 + 10, x0 + (x1 - x0) * 0.55, y0 + 6
        ch = c.beginPath(); ch.moveTo(px0, y1); ch.lineTo(px1, y1); ch.lineTo(px1 - 6, py0); ch.lineTo(px0, py0); ch.close()
        c.setFillColor(colors.white); c.setStrokeColor(ENCRE); c.setLineWidth(0.8); c.drawPath(ch, stroke=1, fill=1)
        ax = (px0 + px1) / 2
        c.setStrokeColor(GARANCE); c.line(ax - 15, (y1 + py0) / 2, ax + 15, (y1 + py0) / 2)
        for s in (-1, 1):
            c.line(ax + s * 15, (y1 + py0) / 2, ax + s * 11, (y1 + py0) / 2 + 3)
            c.line(ax + s * 15, (y1 + py0) / 2, ax + s * 11, (y1 + py0) / 2 - 3)

    def s_surjet(self, L, H):
        """Deux pièces endroit contre endroit, piquées à 0,7 cm du bord, surjetées."""
        x0, x1, ym = 10, L - 22, H / 2
        self.couche(x0, x1, ym + 5, endroit_dessus=False, label='pièce du dessus')
        self.couche(x0, x1, ym - 5, endroit_dessus=True)
        self.canv.setFillColor(GRIS); self.canv.setFont('Texte-Italique', 7)
        self.canv.drawString(x0, ym - 18, 'pièce du dessous')
        self.piqure(x1 - 14, ym - 10, ym + 10)
        self.surjet(x1, ym - 9, ym + 9)
        self.cote(x1 - 14, x1, ym + 15, self.v['couture'])

    def s_bande_pliee(self, L, H):
        """Bande pliée en deux dans la longueur, envers contre envers."""
        c, x0, x1, ym = self.canv, 14, L - 14, H / 2
        self.couche(x0 + 8, x1, ym + 5, endroit_dessus=True)
        self.couche(x0 + 8, x1, ym - 5, endroit_dessus=False)
        c.setStrokeColor(BLEU); c.setLineWidth(4.2)
        c.arc(x0 + 2, ym - 7, x0 + 14, ym + 7, 90, 180)
        c.setFillColor(GRIS); c.setFont('Texte-Italique', 7); c.drawString(x0, ym + 13, 'pli')

    def s_bande(self, L, H):
        """Bande pliée posée sur l'endroit de l'encolure, bords bruts ensemble."""
        c, x0, x1, ym = self.canv, 10, L - 18, H / 2 - 4
        self.couche(x0, x1, ym - 6, endroit_dessus=True, label=None)
        c.setFillColor(GRIS); c.setFont('Texte-Italique', 7); c.drawString(x0, ym - 19, 'encolure')
        b0 = x0 + (x1 - x0) * 0.35
        self.couche(b0 + 6, x1, ym + 3, endroit_dessus=False)
        self.couche(b0 + 6, x1, ym + 12, endroit_dessus=True)
        c.setStrokeColor(BLEU); c.setLineWidth(4.2); c.arc(b0, ym + 1, b0 + 12, ym + 14, 90, 180)
        c.setFillColor(GRIS); c.drawString(b0, ym + 20, 'bande pliée')
        self.piqure(x1 - 14, ym - 10, ym + 16)
        self.cote(x1 - 14, x1, ym + 24, self.v['couture'])

    def s_onglet(self, L, H):
        """Pointe du V : devant plié dans l'axe, extrémités de la bande piquées dans le prolongement du V."""
        c = self.canv
        cx, top, bas = L / 2, H - 10, 12
        c.setStrokeColor(ENCRE); c.setLineWidth(0.8)
        c.line(cx - 40, top, cx, bas + 18); c.line(cx + 40, top, cx, bas + 18)
        c.setStrokeColor(BLEU); c.setLineWidth(5)
        c.line(cx - 36, top, cx - 3, bas + 26); c.line(cx + 36, top, cx + 3, bas + 26)
        c.setStrokeColor(GARANCE); c.setLineWidth(1.1); c.setDash(2, 1.5); c.line(cx, bas + 30, cx, bas + 4); c.setDash()
        c.setFillColor(GRIS); c.setFont('Texte-Italique', 7)
        c.drawString(cx + 6, bas + 6, 'piqûre dans l\'axe'); c.drawString(cx + 38, top - 10, 'bande')

    def s_manche(self, L, H):
        """Manche posée à plat sur l'emmanchure, crans ensemble."""
        c = self.canv
        cx, y = L / 2, H * 0.35
        c.setStrokeColor(ENCRE); c.setLineWidth(0.8)
        ch = c.beginPath(); ch.moveTo(cx - 48, y); ch.curveTo(cx - 30, y + 30, cx + 30, y + 30, cx + 48, y)
        c.drawPath(ch, stroke=1, fill=0)
        c.setStrokeColor(BLEU); c.setLineWidth(1.4)
        ch = c.beginPath(); ch.moveTo(cx - 48, y + 2); ch.curveTo(cx - 30, y + 33, cx + 30, y + 33, cx + 48, y + 2)
        c.drawPath(ch, stroke=1, fill=0)
        c.setFillColor(GARANCE)
        for dx, dy in ((0, 25), (-30, 17), (30, 17)):
            p = c.beginPath(); p.moveTo(cx + dx - 3, y + dy + 6); p.lineTo(cx + dx + 3, y + dy + 6); p.lineTo(cx + dx, y + dy); p.close()
            c.drawPath(p, stroke=0, fill=1)
        c.setFillColor(GRIS); c.setFont('Texte-Italique', 7)
        c.drawCentredString(cx, y + 36, 'cran d\'épaule'); c.drawCentredString(cx, y - 12, 'emmanchure')

    def s_cotes(self, L, H):
        """Haut plié endroit contre endroit ; couture du bas de manche au bas du corps."""
        c = self.canv
        x, y = 40, 2
        pts = [(x, y), (x, y + 44), (x - 22, y + 30), (x - 30, y + 40), (x - 2, y + 62), (x + 40, y + 62), (x + 40, y)]
        ch = c.beginPath(); ch.moveTo(*pts[0])
        for p in pts[1:]:
            ch.lineTo(*p)
        ch.close()
        c.setStrokeColor(ENCRE); c.setFillColor(FOND); c.setLineWidth(0.8); c.drawPath(ch, stroke=1, fill=1)
        c.setStrokeColor(GARANCE); c.setLineWidth(1.2); c.setDash(2, 1.5)
        c.line(x - 26, y + 33, x + 3, y + 47); c.line(x + 3, y + 47, x + 3, y + 3); c.setDash()
        c.setFillColor(GRIS); c.setFont('Texte-Italique', 6.5)
        c.drawString(x + 44, y + 30, 'une seule'); c.drawString(x + 44, y + 22, 'couture')

    def s_ourlet(self, L, H):
        """Bord replié sur l'envers et surpiqué à deux aiguilles."""
        c, x0, x1, ym = self.canv, 16, L - 10, H / 2
        self.couche(x0, x1, ym + 5, endroit_dessus=True)
        self.couche(x0, x0 + (x1 - x0) * 0.55, ym - 5, endroit_dessus=False)
        c.setStrokeColor(BLEU); c.setLineWidth(4.2); c.arc(x0 - 6, ym - 7, x0 + 6, ym + 7, 90, 270)
        for dx in (0, 5):
            self.piqure(x0 + (x1 - x0) * 0.45 + dx, ym - 9, ym + 10)
        self.cote(x0, x0 + (x1 - x0) * 0.55, ym - 17, self.v['ourlet'])
        c.setFillColor(GRIS); c.setFont('Texte-Italique', 7); c.drawString(x0, ym + 13, 'pli du bas')

    def s_jambe(self, L, H):
        """Jambe pliée endroit contre endroit, entrejambe piqué de l'enfourchure au bas."""
        c = self.canv
        x, y = 25, 2
        pts = [(x, y), (x + 4, y + 56), (x + 22, y + 66), (x + 44, y + 66), (x + 40, y)]
        ch = c.beginPath(); ch.moveTo(*pts[0])
        for p in pts[1:]:
            ch.lineTo(*p)
        ch.close()
        c.setStrokeColor(ENCRE); c.setFillColor(FOND); c.setLineWidth(0.8); c.drawPath(ch, stroke=1, fill=1)
        c.setStrokeColor(GARANCE); c.setLineWidth(1.2); c.setDash(2, 1.5)
        c.line(x + 3, y + 2, x + 6, y + 54); c.setDash()
        c.setFillColor(GRIS); c.setFont('Texte-Italique', 7); c.drawString(x + 50, y + 30, 'entrejambe')

    def s_enfourchure(self, L, H):
        """Pantalon vu de face : l'enfourchure, piquée du milieu devant au milieu dos, doublée dans la courbe."""
        c = self.canv
        pts = [(22, 64), (88, 64), (96, 4), (66, 4), (55, 30), (44, 4), (14, 4)]
        ch = c.beginPath(); ch.moveTo(*pts[0])
        for p in pts[1:]:
            ch.lineTo(*p)
        ch.close()
        c.setStrokeColor(ENCRE); c.setFillColor(FOND); c.setLineWidth(0.8); c.drawPath(ch, stroke=1, fill=1)
        c.setStrokeColor(GARANCE); c.setLineWidth(1.2); c.setDash(2, 1.5); c.line(55, 63, 55, 31); c.setDash()
        c.setLineWidth(0.8); c.line(57.5, 44, 57.5, 31)
        c.setFillColor(GRIS); c.setFont('Texte-Italique', 7); c.drawString(60, 50, 'enfourchure')

    def s_anneau(self, L, H):
        """Ceinture fermée en anneau, élastique fermé en chevauchement."""
        c = self.canv
        cx, cy = 28, H / 2
        c.setStrokeColor(BLEU); c.setLineWidth(5); c.ellipse(cx - 24, cy - 18, cx + 24, cy + 18)
        c.setStrokeColor(GARANCE); c.setLineWidth(1.2); c.line(cx, cy - 22, cx, cy - 13)
        c.setFillColor(GRIS); c.setFont('Texte-Italique', 7); c.drawCentredString(cx, cy - 32, 'ceinture')
        ex = 82
        c.setStrokeColor(ENCRE); c.setFillColor(colors.white); c.setLineWidth(0.8)
        c.rect(ex - 24, cy - 6, 30, 12, stroke=1, fill=1); c.rect(ex - 6, cy - 6, 30, 12, stroke=1, fill=1)
        c.setStrokeColor(GARANCE)
        ch = c.beginPath(); ch.moveTo(ex - 6, cy - 5)
        for k in range(1, 7):
            ch.lineTo(ex - 6 + k * 1, cy + (5 if k % 2 else -5))
        c.drawPath(ch, stroke=1, fill=0)
        c.setFillColor(GRIS); c.drawCentredString(ex, cy - 18, 'élastique, 2 cm')

    def s_coulisse(self, L, H):
        """Haut du pantalon : élastique surjeté sur l'envers du bord, replié une fois et surpiqué."""
        c, x0, x1, ym = self.canv, 16, L - 10, H / 2
        self.couche(x0, x1, ym + 5, endroit_dessus=True)
        self.couche(x0, x0 + (x1 - x0) * 0.55, ym - 9, endroit_dessus=False)
        c.setStrokeColor(BLEU); c.setLineWidth(4.2); c.arc(x0 - 8, ym - 11, x0 + 8, ym + 7, 90, 270)
        c.setStrokeColor(ENCRE); c.setFillColor(colors.white); c.setLineWidth(0.6)
        c.rect(x0 + 3, ym - 5, (x1 - x0) * 0.5, 7, stroke=1, fill=1)
        self.surjet(x0 + (x1 - x0) * 0.55, ym - 9, ym + 2)
        self.piqure(x0 + (x1 - x0) * 0.55 + 6, ym - 13, ym + 10)
        self.cote(x0, x0 + (x1 - x0) * 0.55, ym - 21, '3')
        c.setFillColor(GRIS); c.setFont('Texte-Italique', 7)
        c.drawString(x0, ym + 13, 'pli de la taille, élastique dans le repli')

    def s_ceinture(self, L, H):
        """Ceinture pliée, élastique dans le pli, posée sur l'endroit du pantalon."""
        c, x0, x1, ym = self.canv, 10, L - 18, H / 2 - 8
        self.couche(x0, x1, ym - 6, endroit_dessus=True)
        c.setFillColor(GRIS); c.setFont('Texte-Italique', 7); c.drawString(x0, ym - 19, 'pantalon')
        b0 = x0 + 10
        self.couche(b0 + 6, x1, ym + 3, endroit_dessus=False)
        self.couche(b0 + 6, x1, ym + 22, endroit_dessus=True)
        c.setStrokeColor(BLEU); c.setLineWidth(4.2); c.arc(b0, ym + 1, b0 + 12, ym + 24, 90, 180)
        c.setStrokeColor(ENCRE); c.setFillColor(colors.white); c.setLineWidth(0.6)
        c.rect(b0 + 9, ym + 9, (x1 - b0) * 0.55, 6, stroke=1, fill=1)
        c.setFillColor(GRIS); c.drawString(b0, ym + 29, 'ceinture, élastique dans le pli')
        self.piqure(x1 - 14, ym - 10, ym + 26)
        self.cote(x1 - 14, x1, ym - 22, self.v['couture'])


    def s_poche(self, L, H):
        """Poche kangourou posée sur le devant : entrées de mains en biais libres, le reste surpiqué."""
        c = self.canv
        cx, y0, y1 = L / 2, 8, 50
        c.setStrokeColor(ENCRE); c.setFillColor(FOND); c.setLineWidth(0.8)
        c.rect(cx - 50, 2, 100, H - 4, stroke=1, fill=1)
        c.setFillColor(GRIS); c.setFont('Texte-Italique', 7); c.drawString(cx - 48, H - 10, 'devant')
        haut, bas, ouv = 18, 32, 20
        pts = [(cx - haut, y1), (cx + haut, y1), (cx + bas, y1 - ouv), (cx + bas, y0), (cx - bas, y0), (cx - bas, y1 - ouv)]
        ch = c.beginPath(); ch.moveTo(*pts[0])
        for q in pts[1:]:
            ch.lineTo(*q)
        ch.close()
        c.setFillColor(colors.white); c.setStrokeColor(ENCRE); c.drawPath(ch, stroke=1, fill=1)
        c.setStrokeColor(BLEU); c.setLineWidth(1.6)
        c.line(cx + haut, y1, cx + bas, y1 - ouv); c.line(cx - haut, y1, cx - bas, y1 - ouv)
        c.setStrokeColor(GARANCE); c.setLineWidth(1.1); c.setDash(2, 1.5)
        d = 2
        ch = c.beginPath(); ch.moveTo(cx + bas - d, y1 - ouv); ch.lineTo(cx + bas - d, y0 + d); ch.lineTo(cx - bas + d, y0 + d)
        ch.lineTo(cx - bas + d, y1 - ouv); c.drawPath(ch, stroke=1, fill=0)
        c.line(cx - haut, y1 - d, cx + haut, y1 - d); c.setDash()
        c.setFillColor(GRIS); c.setFont('Texte-Italique', 7)
        c.drawString(cx + haut - 4, y1 + 4, 'entrée de main'); c.drawCentredString(cx, y0 + 6, 'surpiqûre')

    def s_ouverture(self, L, H):
        """Couture de côté interrompue entre les deux crans : l'ouverture pour passer les mains."""
        c = self.canv
        x, y0, y1 = L / 2, 4, H - 4
        c.setStrokeColor(ENCRE); c.setFillColor(FOND); c.setLineWidth(0.8)
        c.rect(x - 22, y0, 22, y1 - y0, stroke=1, fill=1); c.rect(x, y0, 22, y1 - y0, stroke=1, fill=1)
        o1, o2 = y1 - 22, y0 + 22
        c.setStrokeColor(GARANCE); c.setLineWidth(1.2); c.setDash(2, 1.5)
        c.line(x, y1, x, o1); c.line(x, o2, x, y0); c.setDash()
        c.setStrokeColor(BLEU); c.setLineWidth(1)
        for xx in (x - 3, x + 3):
            c.line(xx, o1, xx, o2)
        c.setStrokeColor(GARANCE); c.setLineWidth(1.4)
        for yy in (o1, o2):
            c.line(x - 5, yy, x + 5, yy)
        c.setFillColor(GRIS); c.setFont('Texte-Italique', 7)
        c.drawString(x + 25, o1 - 2, 'cran'); c.drawString(x + 25, o2 - 2, 'cran')
        c.drawRightString(x - 25, (o1 + o2) / 2, 'surpiqûres')

    def s_coulisse_capuche(self, L, H):
        """Bord de capuche replié deux fois en coulisse, cordon glissé dedans."""
        c, x0, x1, ym = self.canv, 16, L - 10, H / 2
        self.couche(x0, x1, ym + 7, endroit_dessus=True, label=None)
        self.couche(x0, x0 + (x1 - x0) * 0.45, ym - 7, endroit_dessus=False)
        c.setStrokeColor(BLEU); c.setLineWidth(4.2); c.arc(x0 - 8, ym - 9, x0 + 8, ym + 9, 90, 270)
        c.setFillColor(GARANCE); c.setStrokeColor(GARANCE); c.circle(x0 + 6, ym, 2.4, stroke=0, fill=1)
        self.piqure(x0 + (x1 - x0) * 0.42, ym - 11, ym + 12)
        c.setFillColor(GRIS); c.setFont('Texte-Italique', 7)
        c.drawString(x0, ym + 15, 'bord du visage'); c.drawString(x0 + 12, ym - 20, 'cordon')


# ---------------------------------------------------------------- document
def paragraphe(texte, style='texte'):
    return Paragraph(texte.replace('\n', ' '), S[style])


def dossier(svg, sm2d, dst, montage='pro', mesures=None, taille=None, gamme=None, nom=None):
    """Écrit le dossier en A4 ; renvoie le nombre de pages.
    mesures : fichier de mesures de l'export (.smms d'une taille, ou .vit du sur-mesure).
    taille : libellé (« 40 », « T-Thomas », « sur-mesure »). gamme : femme ou homme.
    nom : nom du patron (patrons/<nom>.dossier.toml), par défaut celui du .sm2d."""
    nom = nom or os.path.splitext(os.path.basename(sm2d))[0]
    with open(os.path.join(RACINE, 'patrons', nom + '.dossier.toml'), 'rb') as f:
        D = tomllib.load(f)
    # {couture} et {ourlet} dans les textes : valeurs lues dans le .sm2d
    L = largeurs(sm2d)
    def remplir(v):
        if isinstance(v, str):
            return v.replace('{couture}', L['couture']).replace('{ourlet}', L['ourlet'])
        if isinstance(v, list):
            return [remplir(x) for x in v]
        if isinstance(v, dict):
            return {k: remplir(x) for k, x in v.items()}
        return v
    D = remplir(D)
    pieces = [pc for pc in lire_svg(svg) if not pc['nom'].lower().startswith('carr')]
    infos = infos_pieces(sm2d)
    pieces.sort(key=lambda pc: list(infos).index(pc['nom']) if pc['nom'] in infos else 99)
    valeurs = lire_mesures(mesures) if mesures else {}
    if gamme is None and mesures and os.path.basename(os.path.dirname(os.path.abspath(mesures))) in ('femme', 'homme'):
        gamme = os.path.basename(os.path.dirname(os.path.abspath(mesures)))
    sur_mesure = not (taille or '').isdigit()
    # [tailles] du .toml : nom public de chaque taille (XS, S…) ; sinon le numéro
    noms_tailles = D.get('tailles', {})
    libelle = ('Taille %s' % noms_tailles.get(str(taille), taille)) if taille and taille != 'sur-mesure' else 'Sur mesure'

    pages_total = {'n': 0}

    def cadre(c, doc):
        c.saveState()
        c.setStrokeColor(FILET); c.setLineWidth(0.5)
        c.line(MARGE, H - 1.3 * CM, W - MARGE, H - 1.3 * CM)
        c.setFillColor(GRIS); c.setFont('Capitales', 9)
        c.drawString(MARGE, H - 1.15 * CM, 'Atelier AT')
        c.setFont('Texte-Italique', 9)
        c.drawRightString(W - MARGE, H - 1.15 * CM, '%s · %s · %s' % (D['titre'], D['reference'], libelle))
        c.line(MARGE, 1.3 * CM, W - MARGE, 1.3 * CM)
        c.drawString(MARGE, 0.9 * CM, 'Fait pour durer')
        c.drawRightString(W - MARGE, 0.9 * CM, 'Dossier, page %d' % doc.page)
        c.restoreState()
        pages_total['n'] = doc.page

    doc = BaseDocTemplate(dst, pagesize=A4, leftMargin=MARGE, rightMargin=MARGE, topMargin=1.8 * CM, bottomMargin=1.8 * CM,
                          title='%s, %s, dossier' % (D['titre'], libelle.lower()), author='Atelier AT')
    largeur = W - 2 * MARGE
    doc.addPageTemplates([PageTemplate('p', [Frame(MARGE, 1.8 * CM, largeur, H - 3.6 * CM, id='f',
                                                   leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)], onPage=cadre)])
    E = []

    # 1. informations
    E += [paragraphe(D['titre'], 'titre'), Spacer(1, 2), paragraphe('Informations', 'sous'),
          paragraphe('%s · %s' % (D['reference'], libelle), 'centre'), Spacer(1, 14)]
    dessin = os.path.join(RACINE, 'vignettes', gamme or 'femme', nom + '_dessin.png')
    if os.path.exists(dessin):
        E += [Image(dessin, largeur * 0.9, 8.5 * CM), Spacer(1, 4),
              Table([['devant', 'dos']], colWidths=[largeur / 2] * 2,
                    style=[('FONT', (0, 0), (-1, -1), 'Texte-Italique', 9), ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                           ('TEXTCOLOR', (0, 0), (-1, -1), GRIS)])]
    E += [Spacer(1, 10), paragraphe(D['description'])]
    E += [Paragraph('Tableau des mesures', S['h']), Spacer(1, 4)]
    noms = [m for m in D['mesures']]
    if not sur_mesure and gamme:
        tab = tableau_gamme(gamme)
        tailles = list(tab)
        lignes = [['Taille'] + [noms_tailles.get(str(t), str(t)) for t in tailles]]
        lignes += [[LIBELLES.get(m, m)] + [cm(tab[t].get(m, 0)) for t in tailles] for m in noms]
        col = tailles.index(int(taille)) + 1 if int(taille) in tailles else None
    else:
        lignes = [['', 'Vos mesures']] + [[LIBELLES.get(m, m), cm(valeurs.get(m, 0))] for m in noms]
        col = 1
    n = len(lignes[0])
    l0 = 4.2 * CM
    st = [('FONT', (0, 0), (-1, -1), 'Mesure', 9.5), ('FONT', (0, 0), (0, -1), 'Texte', 10),
          ('FONT', (1, 0), (-1, 0), 'Mesure-Gras', 9.5),
          ('GRID', (0, 0), (-1, -1), 0.5, FILET), ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
          ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('BACKGROUND', (0, 0), (-1, 0), FOND),
          ('TOPPADDING', (0, 0), (-1, -1), 4), ('BOTTOMPADDING', (0, 0), (-1, -1), 4)]
    if col:
        st += [('BOX', (col, 0), (col, -1), 1.2, GARANCE), ('TEXTCOLOR', (col, 0), (col, -1), GARANCE)]
    E += [Table(lignes, colWidths=[l0] + [3 * CM if n == 2 else min(2 * CM, (largeur - l0) / (n - 1))] * (n - 1), style=st, hAlign='LEFT'),
          Spacer(1, 4), paragraphe('Mesures du corps, en centimètres. Les aisances sont comprises dans le patron.', 'note')]

    # 2. coupe, matériel, fournitures
    E += [PageBreak(), Paragraph('La coupe', S['h']), paragraphe(D['coupe']['texte']), Spacer(1, 4)]
    E += [Paragraph('Le matériel', S['h'])]
    E += [Paragraph(m['nom'], S['liste'], bulletText='·') for m in D.get('materiel', [])]
    E += [Paragraph('Les fournitures', S['h'])]
    # laize : une largeur de tissu, ou une liste (un métrage par largeur, Amélie #88)
    laizes = D['coupe'].get('laize', 150)
    laizes = laizes if isinstance(laizes, list) else [laizes]
    for f in D.get('fournitures', []):
        if f.get('metrage'):
            # « matiere » : métrage des seules pièces de cette matière (tissu et doublure se coupent à part)
            garde = (lambda n, m=f['matiere']: D['matieres'].get(n, D['matieres']['defaut']) == m) if f.get('matiere') else None
            q = ', '.join('%s m en %d cm' % (('%.2f' % (metrage(pieces, infos, l, garde) / 100)).replace('.', ','), l)
                          for l in laizes) + ' de large'
        elif f.get('mesure') and f['mesure'] in valeurs:
            q = '%s cm' % cm(round(valeurs[f['mesure']] * f.get('coef', 1) + f.get('ajout', 0)))
        else:
            q = f.get('quantite', '')
        E += [Paragraph('<b>%s</b> : %s%s' % (f['designation'], f['renseignement'], ('. <font name="Mesure">%s</font>' % q) if q else ''),
                        S['liste'], bulletText='·')]
    E += [Spacer(1, 3), paragraphe('Métrage calculé pour la %s, tissu plié en deux, avec une marge de 10 %%.'
                                   % (libelle.lower() if not sur_mesure else 'taille sur mesure'), 'note')]
    E += [Paragraph('Le dossier', S['h'])]
    for t in ('Les informations et le tableau des mesures', 'La coupe, le matériel et les fournitures',
              'Le plan des valeurs de couture et la nomenclature',
              *(('La gamme de montage, ' + ('en tableau' if montage == 'pro' else 'pas à pas'),) if D.get('gamme') else ()),
              'Puis les pièces du patron à imprimer à 100 %'):
        E += [Paragraph(t, S['liste'], bulletText='·')]

    # 3. plan des valeurs de couture
    E += [PageBreak(), Paragraph('Plan des valeurs de couture', S['h']),
          paragraphe('Valeurs comprises dans le patron, en centimètres : trait plein, ligne de couture ; '
                     'tirets, ligne de coupe.', 'note'), Spacer(1, 6)]
    par_matiere = {}
    for pc in pieces:
        if pc['nom'] in infos:
            par_matiere.setdefault(D['matieres'].get(pc['nom'], D['matieres']['defaut']), []).append(pc)
    haut_dispo = H - 3.6 * CM - 2.6 * CM
    for matiere, pcs in par_matiere.items():
        bandeau = Table([[matiere.upper()]], colWidths=[largeur],
                        style=[('FONT', (0, 0), (-1, -1), 'Capitales', 11), ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('BACKGROUND', (0, 0), (-1, -1), FOND), ('BOX', (0, 0), (-1, -1), 0.6, ENCRE)])
        E += [bandeau, PlanCoutures(pcs, infos, largeur, (haut_dispo - 30) / len(par_matiere))]

    # 4. nomenclature
    E += [PageBreak(), Paragraph('Nomenclature', S['h']), Spacer(1, 4)]
    lignes = [['Rep.', 'Nbr', 'Désignation', 'Matière, renseignement']]
    for i, (n_, (q, pli)) in enumerate(infos.items(), 1):
        lignes.append([str(i), ('%d au pli' % q) if pli else str(q), n_, D['matieres'].get(n_, D['matieres']['defaut'])])
    for f in D.get('fournitures', []):
        if f.get('metrage'):
            continue
        if f.get('mesure') and f['mesure'] in valeurs:
            q = '%s cm' % cm(round(valeurs[f['mesure']] * f.get('coef', 1) + f.get('ajout', 0)))
        else:
            q = f.get('quantite', '1')
        lignes.append(['', Paragraph(q, S['centre']), f['designation'], Paragraph(f['renseignement'], S['cellule'])])
    E += [Table(lignes, colWidths=[1.6 * CM, 3.2 * CM, 5.4 * CM, largeur - 10.2 * CM], repeatRows=1,
                style=[('FONT', (0, 0), (-1, 0), 'Capitales', 10), ('FONT', (0, 1), (-1, -1), 'Texte', 10),
                       ('FONT', (0, 1), (1, -1), 'Mesure', 9.5),
                       ('BACKGROUND', (0, 0), (-1, 0), FOND), ('GRID', (0, 0), (-1, -1), 0.5, FILET),
                       ('BOX', (0, 0), (-1, -1), 0.8, ENCRE), ('ALIGN', (0, 0), (1, -1), 'CENTER'),
                       ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('TOPPADDING', (0, 0), (-1, -1), 5),
                       ('BOTTOMPADDING', (0, 0), (-1, -1), 5)])]

    # 5. gamme de montage (absente tant que le montage n'est pas rédigé : le dossier s'arrête à la nomenclature)
    etapes = D.get('gamme', [])
    if not etapes:
        doc.build(E)
        return pages_total['n']
    E += [PageBreak()]
    if montage == 'pro':
        E += [Paragraph('Gamme de montage', S['h']), Spacer(1, 4)]
        P = lambda t, s='cellule': Paragraph(t, S[s])
        entete = Table([[P('<b>Produit</b> : %s' % D['titre']), P('Référence : %s' % D['reference']), P('Mode de lancement : unitaire')],
                        ['', P('Quantité : 1'), '']],
                       colWidths=[largeur * 0.45, largeur * 0.27, largeur * 0.28],
                       style=[('GRID', (0, 0), (-1, -1), 0.5, ENCRE), ('SPAN', (0, 0), (0, 1)), ('SPAN', (2, 0), (2, 1)),
                              ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')])
        cond = Table([[P(t, 'entete') for t in ('Matière d\'œuvre', 'Machines', 'Type de point', 'Points / cm', 'Temps')],
                      [P('<br/>'.join(f['designation'] for f in D.get('fournitures', []))),
                       P('<br/>'.join(D['technique']['machines'])), P('<br/>'.join(D['technique']['points'])),
                       P(D['technique']['points_cm'], 'centre'), P('%s (indicatif)' % D['technique']['temps'], 'centre')]],
                     colWidths=[largeur * 0.2, largeur * 0.27, largeur * 0.27, largeur * 0.11, largeur * 0.15],
                     style=[('GRID', (0, 0), (-1, -1), 0.5, ENCRE), ('BACKGROUND', (0, 0), (-1, 0), FOND),
                            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')])
        bandeau = lambda t: Table([[t]], colWidths=[largeur], style=[('FONT', (0, 0), (-1, -1), 'Capitales', 10.5),
                                                                     ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                                                     ('BACKGROUND', (0, 0), (-1, -1), FOND),
                                                                     ('BOX', (0, 0), (-1, -1), 0.8, ENCRE)])
        E += [bandeau('Gamme de montage générale'), entete, bandeau('Conditions technologiques'), cond, Spacer(1, 8)]
        cw = [0.9 * CM, 3.6 * CM, 3.9 * CM, 2.1 * CM]
        cw += [(largeur - sum(cw)) * 0.55, (largeur - sum(cw)) * 0.45]
        lignes = [[P(t, 'entete') for t in ('N°', 'Opération', 'Schéma', 'Outil', 'Commentaire', 'Point de contrôle')]]
        for i, e in enumerate(etapes, 1):
            sch = Schema(e['schema'], cw[2] - 8, 2.4 * CM, L) if e.get('schema') else ''
            lignes.append([P(str(i), 'centre'), P(e['operation']), sch, P(e.get('outil', ''), 'centre'),
                           P(e.get('commentaire', '')), P(e.get('controle', ''))])
        E += [Table(lignes, colWidths=cw, repeatRows=1,
                    style=[('GRID', (0, 0), (-1, -1), 0.5, ENCRE), ('BACKGROUND', (0, 0), (-1, 0), FOND),
                           ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('TOPPADDING', (0, 0), (-1, -1), 4),
                           ('BOTTOMPADDING', (0, 0), (-1, -1), 4)])]
    else:
        E += [paragraphe('Le montage pas à pas', 'titre'), Spacer(1, 6),
              paragraphe('Toutes les coutures se font endroit contre endroit, à %s cm du bord, sauf indication contraire. ' % L['couture'] +
                         'Avant de commencer, essayez votre point sur une chute de jersey : la couture doit pouvoir '
                         's\'étirer sans que le fil casse.', 'note'), Spacer(1, 6)]
        for i, e in enumerate(etapes, 1):
            texte = [Paragraph('%d. %s' % (i, e.get('titre', e['operation'])), S['etape'])]
            texte += [Paragraph(t, S['pas']) for t in e.get('texte', [e.get('commentaire', '')])]
            if e.get('controle'):
                texte += [Paragraph('<i>À vérifier : %s</i>' % e['controle'][0].lower() + e['controle'][1:], S['note'])]
            sch = Schema(e['schema'], 5.2 * CM, 3.4 * CM, L) if e.get('schema') else ''
            E += [KeepTogether(Table([[texte, sch]], colWidths=[largeur - 5.8 * CM, 5.8 * CM],
                                     style=[('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 0),
                                            ('LINEBELOW', (0, 0), (-1, -1), 0.4, FILET),
                                            ('BOTTOMPADDING', (0, 0), (-1, -1), 8)])), Spacer(1, 4)]
    doc.build(E)
    return pages_total['n']


def joindre(dossier_pdf, patron_pdf, dst):
    """PDF final : le dossier puis les pages du patron (dst peut être patron_pdf)."""
    import io
    from pypdf import PdfReader, PdfWriter
    lus = [PdfReader(io.BytesIO(open(f, 'rb').read())) for f in (dossier_pdf, patron_pdf)]
    w = PdfWriter()
    for r in lus:
        w.append(r)
    titre = (lus[1].metadata or {}).get('/Title')
    if titre:
        w.add_metadata({'/Title': titre})
    with open(dst, 'wb') as f:
        w.write(f)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('svg'); ap.add_argument('sm2d'); ap.add_argument('sortie')
    ap.add_argument('--montage', choices=('pro', 'amateur'), default='pro')
    ap.add_argument('--mesures'); ap.add_argument('--taille'); ap.add_argument('--gamme', choices=('femme', 'homme'))
    a = ap.parse_args()
    print(a.sortie, dossier(a.svg, a.sm2d, a.sortie, a.montage, a.mesures, a.taille, a.gamme), 'pages')
