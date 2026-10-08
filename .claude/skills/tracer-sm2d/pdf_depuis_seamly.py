"""Patron imprimable (PDF A4 à l'échelle 1) à partir de l'export SVG des pièces fait par Seamly.

La géométrie n'est pas recalculée : les tracés de Seamly (coupe, couture, crans, droit-fil,
étiquettes) sont recopiés tels quels, chaque pièce seulement déplacée (translation) pour ne pas
se superposer. Page 1 : notice, carré de contrôle 5 × 5 cm et plan d'assemblage ; puis les
pages A4 à scotcher bord à bord.

Export Seamly (sur le PC) : seamly2d.exe -b <nom> -d <dossier> -f 0 --exportOnlyDetails <nom>.sm2d
Usage : python3 pdf_depuis_seamly.py <nom>_pieces.svg sortie.pdf "Titre" [fichier.sm2d]
Le .sm2d, facultatif, ne sert qu'au texte de la notice (taille, quantités).
"""
import math, os, re, sys
import xml.etree.ElementTree as ET
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import simpleSplit

NS = '{http://www.w3.org/2000/svg}'
PT_PX = 72 / 96          # Seamly exporte en pixels à 96 ppp
CM = 72 / 2.54           # points PDF par cm
MARGE = 1.0              # marge de page (cm)
ECART = 1.5              # écart entre pièces (cm)
PX_CM = 96 / 2.54


def lire_chemin(d):
    """Commandes M, L, C absolues (les seules qu'écrit Seamly) -> [(op, [x, y, ...])]."""
    jet = re.findall(r'[MLCZmlcz]|-?[\d.]+(?:e[-+]?\d+)?', d)
    res, op, nb = [], None, {'M': 2, 'L': 2, 'C': 6, 'Z': 0}
    i = 0
    while i < len(jet):
        t = jet[i]
        if t.isalpha():
            if t.islower() and t != 'z':
                raise ValueError('commande relative non prévue : ' + t)
            op = t.upper(); i += 1
            if op == 'Z':
                res.append(('Z', []))
            continue
        res.append((op, [float(v) for v in jet[i:i + nb[op]]]))
        i += nb[op]
        if op == 'M':
            op = 'L'
    return res


def translation(tr):
    if not tr:
        return 0.0, 0.0
    m = re.fullmatch(r'matrix\(1,0,0,1,(-?[\d.e+-]+),(-?[\d.e+-]+)\)', tr.replace(' ', ''))
    if not m:
        raise ValueError('transformation non prévue : ' + tr)
    return float(m.group(1)), float(m.group(2))


def lire_svg(path):
    """Pièces : nom, chemins [(style, commandes en px absolus)], boîte englobante (px)."""
    racine = ET.parse(path).getroot()
    pieces = []
    for g in racine.findall(NS + 'g'):
        chemins = []
        def parcourir(el, dx, dy, style):
            tx, ty = translation(el.get('transform'))
            dx, dy = dx + tx, dy + ty
            style = dict(style)
            for k in ('fill', 'stroke', 'stroke-width', 'fill-rule'):
                if el.get(k) is not None:
                    style[k] = el.get(k)
            if el.tag == NS + 'path' and el.get('d'):
                cmds = [(op, [v + (dx if j % 2 == 0 else dy) for j, v in enumerate(vals)])
                        for op, vals in lire_chemin(el.get('d'))]
                chemins.append((style, cmds))
            for e in el:
                parcourir(e, dx, dy, style)
        parcourir(g, 0.0, 0.0, {})
        xs = [v for _, cm in chemins for op, vals in cm for v in vals[0::2]]
        ys = [v for _, cm in chemins for op, vals in cm for v in vals[1::2]]
        if xs:
            pieces.append(dict(nom=g.get('id'), chemins=chemins, bb=(min(xs), min(ys), max(xs), max(ys))))
    return pieces


def infos_sm2d(path):
    """Texte de notice seulement : taille, et « couper n fois (au pli) » par pièce."""
    if not path:
        return '', {}
    racine = ET.parse(path).getroot()
    m = racine.find('measurements')
    taille = re.sub(r'\D', '', os.path.basename(m.text)) if m is not None and m.text else ''
    coupe = {}
    for pc in racine.iter('piece'):
        d = pc.find('data')
        if d is None:
            continue
        q = int(d.get('quantity') or 1)
        coupe[pc.get('name')] = ('Couper %d fois au pli' % q) if d.get('onFold') == 'true' else \
            ('Couper %d fois (en symétrie)' % q if q > 1 else 'Couper 1 fois')
    return taille, coupe


def ranger(pieces, largeur):
    """Étagères, sans rotation : seule une translation (dx, dy en cm) est appliquée."""
    for pc in pieces:
        x0, y0, x1, y1 = pc['bb']
        pc['l'], pc['h'] = (x1 - x0) / PX_CM, (y1 - y0) / PX_CM
    x = y = ECART; haut = 0
    for pc in sorted(pieces, key=lambda pc: -pc['h']):
        if x + pc['l'] + ECART > largeur and x > ECART:
            x = ECART; y += haut + ECART; haut = 0
        pc['x'], pc['y'] = x, y              # coin haut-gauche sur le plan (cm, y vers le bas)
        x += pc['l'] + ECART; haut = max(haut, pc['h'])
    return max(largeur, max(pc['x'] + pc['l'] for pc in pieces) + ECART), y + haut + ECART


def dessiner(c, pieces, ox, oy, e=1.0, detail=True):
    """Plan -> PDF : (ox, oy) = position PDF du coin haut-gauche du plan, e = échelle."""
    for pc in pieces:
        bx, by = pc['bb'][0], pc['bb'][1]
        X = lambda px: ox + ((px - bx) / PX_CM + pc['x']) * CM * e
        Y = lambda py: oy - ((py - by) / PX_CM + pc['y']) * CM * e
        for style, cmds in pc['chemins']:
            remplir = style.get('fill', 'black') not in ('none',)
            if not detail and remplir:
                continue                      # pas de texte sur le plan réduit
            p = c.beginPath()
            for op, v in cmds:
                if op == 'M':
                    p.moveTo(X(v[0]), Y(v[1]))
                elif op == 'L':
                    p.lineTo(X(v[0]), Y(v[1]))
                elif op == 'C':
                    p.curveTo(X(v[0]), Y(v[1]), X(v[2]), Y(v[3]), X(v[4]), Y(v[5]))
                else:
                    p.close()
            c.setLineWidth(float(style.get('stroke-width', 1)) * PT_PX * (1 if detail else 0.5))
            if remplir:
                c.drawPath(p, stroke=0, fill=1, fillMode=0 if style.get('fill-rule') == 'evenodd' else 1)
            else:
                c.drawPath(p, stroke=1, fill=0)


def exporter(svg, dst, titre, sm2d=None):
    pieces = lire_svg(svg)
    taille, coupe = infos_sm2d(sm2d)
    meilleur = None
    for pw, ph in (A4, A4[::-1]):
        uw, uh = pw / CM - 2 * MARGE, ph / CM - 2 * MARGE
        for nc in range(1, 7):
            W, H = ranger(pieces, nc * uw)
            pleines = pages_pleines(pieces, uw, uh)
            score = (len(pleines), math.ceil(W / uw) * math.ceil(H / uh))
            if meilleur is None or score < meilleur[0]:
                meilleur = (score, (pw, ph), nc, uw, uh)
    _, (pw, ph), nc, uw, uh = meilleur
    W, H = ranger(pieces, nc * uw)
    ncol, nlig = math.ceil(W / uw), math.ceil(H / uh)
    pleines = pages_pleines(pieces, uw, uh)
    nomp = lambda r, k: '%s%d' % (chr(65 + r), k + 1)
    pages = [(r, k) for r in range(nlig) for k in range(ncol) if (r, k) in pleines]

    c = canvas.Canvas(dst, pagesize=A4)
    c.setTitle('%s, taille %s' % (titre, taille) if taille else titre)
    W0, H0 = A4
    y = H0 - 2 * CM
    c.setFont('Helvetica-Bold', 20); c.drawString(2 * CM, y, titre); y -= 22
    c.setFont('Helvetica', 12)
    c.drawString(2 * CM, y, ('Taille %s · ' % taille if taille else '') + 'tracé et export Seamly2D'); y -= 26
    notice = ("Imprimer à 100 % (« taille réelle », sans ajustement à la page). Vérifier le carré de "
              "contrôle ci-contre : il doit mesurer 5 cm de côté. Couper chaque page sur le cadre gris, "
              "côtés droit et bas, puis scotcher bord à bord en suivant le plan d'assemblage "
              "(lettre = rangée, chiffre = colonne).")
    c.setFont('Helvetica', 10)
    for t in simpleSplit(notice, 'Helvetica', 10, 11.5 * CM) + [
            'Tracé extérieur : ligne de coupe, coutures comprises.', 'Tracé intérieur : ligne de couture.']:
        c.drawString(2 * CM, y, t); y -= 14
    y -= 8
    c.setFont('Helvetica-Bold', 11); c.drawString(2 * CM, y, 'Pièces'); y -= 15
    c.setFont('Helvetica', 10)
    for pc in pieces:
        c.drawString(2.3 * CM, y, pc['nom'] + (' : ' + coupe[pc['nom']] if pc['nom'] in coupe else '')); y -= 13
    sx, sy = W0 - 7 * CM, H0 - 7 * CM
    c.setLineWidth(1); c.rect(sx, sy, 5 * CM, 5 * CM)
    c.setFont('Helvetica', 9); c.drawCentredString(sx + 2.5 * CM, sy + 2.5 * CM, '5 cm × 5 cm')
    y -= 10
    c.setFont('Helvetica-Bold', 11); c.drawString(2 * CM, y, "Plan d'assemblage (%d pages)" % len(pages)); y -= 10
    e = min((W0 - 4 * CM) / (ncol * uw * CM), (y - 2 * CM) / (nlig * uh * CM))
    num = {pg: i + 2 for i, pg in enumerate(pages)}
    for r in range(nlig):
        for k in range(ncol):
            X, Y = 2 * CM + k * uw * CM * e, y - (r + 1) * uh * CM * e
            c.setLineWidth(0.4); c.setStrokeGray(0.6 if (r, k) in num else 0.85)
            c.rect(X, Y, uw * CM * e, uh * CM * e)
            c.setFillGray(0.5 if (r, k) in num else 0.8); c.setFont('Helvetica', 7)
            c.drawString(X + 2, Y + uh * CM * e - 8, nomp(r, k) + (' (p. %d)' % num[(r, k)] if (r, k) in num else ' vide'))
    c.setStrokeGray(0); c.setFillGray(0)
    dessiner(c, pieces, 2 * CM, y, e, detail=False)
    for pc in pieces:
        c.setFont('Helvetica', 7)
        c.drawCentredString(2 * CM + (pc['x'] + pc['l'] / 2) * CM * e, y - (pc['y'] + pc['h'] / 2) * CM * e, pc['nom'])
    c.showPage()

    for i, (r, k) in enumerate(pages):
        c.setPageSize((pw, ph))
        c.saveState()
        p = c.beginPath(); p.rect(MARGE * CM, MARGE * CM, uw * CM, uh * CM)
        c.clipPath(p, stroke=0, fill=0)
        x0, x1, y0, y1 = k * uw, (k + 1) * uw, r * uh, (r + 1) * uh
        vues = [pc for pc in pieces if pc['x'] < x1 and pc['x'] + pc['l'] > x0 and pc['y'] < y1 and pc['y'] + pc['h'] > y0]
        dessiner(c, vues, MARGE * CM - x0 * CM, ph - MARGE * CM + y0 * CM)
        c.restoreState()
        c.setLineWidth(0.3); c.setStrokeGray(0.55)
        c.rect(MARGE * CM, MARGE * CM, uw * CM, uh * CM)
        c.setStrokeGray(0); c.setFillGray(0.35); c.setFont('Helvetica', 8)
        c.drawString(MARGE * CM, ph - MARGE * CM + 8, '%s%s · page %s (%d/%d)' % (
            titre, ' · taille ' + taille if taille else '', nomp(r, k), i + 2, len(pages) + 1))
        for (rr, kk), cote in (((r - 1, k), 'haut'), ((r + 1, k), 'bas'), ((r, k - 1), 'gauche'), ((r, k + 1), 'droite')):
            if (rr, kk) not in pleines:
                continue
            t = nomp(rr, kk)
            if cote == 'haut':
                c.drawCentredString(pw / 2, ph - MARGE * CM + 8, t)
            elif cote == 'bas':
                c.drawCentredString(pw / 2, MARGE * CM - 12, t)
            else:
                c.saveState()
                c.translate(MARGE * CM - 6 if cote == 'gauche' else MARGE * CM + uw * CM + 12, ph / 2)
                c.rotate(90); c.drawCentredString(0, 0, t); c.restoreState()
        c.setFillGray(0)
        c.showPage()
    c.save()
    return len(pages) + 1


def pages_pleines(pieces, uw, uh):
    """Pages A4 touchées par un tracé (échantillonnage des chemins)."""
    res = set()
    for pc in pieces:
        bx, by = pc['bb'][0], pc['bb'][1]
        for _, cmds in pc['chemins']:
            prev = None
            for op, v in cmds:
                if not v:
                    continue
                q = ((v[-2] - bx) / PX_CM + pc['x'], (v[-1] - by) / PX_CM + pc['y'])
                pts = [q] if prev is None else [(prev[0] + (q[0] - prev[0]) * t / 8, prev[1] + (q[1] - prev[1]) * t / 8) for t in range(9)]
                for x, y in pts:
                    res.add((int(y // uh), int(x // uw)))
                prev = q
    return res


if __name__ == '__main__':
    n = exporter(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else None)
    print(sys.argv[2], n, 'pages')
