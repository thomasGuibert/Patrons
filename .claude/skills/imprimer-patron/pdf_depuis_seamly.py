"""Patron imprimable (PDF A4 ou A3 à l'échelle 1) à partir de l'export SVG des pièces fait par Seamly.

La géométrie n'est pas recalculée : les tracés de Seamly (coupe, couture, crans, droit-fil,
étiquettes) sont recopiés tels quels, chaque pièce seulement déplacée et, si cela économise des
feuilles, tournée d'un quart de tour. Chaque grande pièce a son propre assemblage de feuilles,
choisi pour le moins de feuilles puis le moins de raccords ; les petites pièces se logent dans
la place libre. Page 1 : notice, carré de contrôle de Seamly et plan d'assemblage.

Export Seamly (sur le PC) : seamly2d.exe -b <nom> -d <dossier> -f 0 --exportOnlyDetails <nom>.sm2d
Usage : python3 pdf_depuis_seamly.py <nom>_pieces.svg sortie.pdf "Titre" [fichier.sm2d] [--a3]
Le .sm2d, facultatif, ne sert qu'au texte de la notice (taille, quantités).
"""
import math, os, re, sys
import xml.etree.ElementTree as ET
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3, A4
from reportlab.lib.utils import simpleSplit

NS = '{http://www.w3.org/2000/svg}'
PT_PX = 72 / 96          # Seamly exporte en pixels à 96 ppp
CM = 72 / 2.54           # points PDF par cm
MARGE = 0.5              # marge de page (cm) : imprimable par les imprimantes courantes
JEU = 0.2                # jeu minimal entre une grande pièce et le bord de son assemblage (cm)
ECART = 0.5              # écart autour des petites pièces logées dans la place libre (cm)
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


FORMATS = {'A4': A4, 'A3': A3}
FEUILLES = {'portrait': A4, 'paysage': A4[::-1]}


def taille_cm(pc):
    x0, y0, x1, y1 = pc['bb']
    return (x1 - x0) / PX_CM, (y1 - y0) / PX_CM


def local(pc, px, py):
    """Point SVG (px) -> repère de la pièce posée (cm, origine en haut à gauche, y vers le bas).
    Quart de tour horaire si pc['rot'] : déplacement rigide, la forme est inchangée."""
    u, v = (px - pc['bb'][0]) / PX_CM, (py - pc['bb'][1]) / PX_CM
    if pc.get('rot'):
        u, v = pc['h0'] - v, u
    return u + pc['x'], v + pc['y']


def assemblages(pieces):
    """Un bloc de feuilles par grande pièce ; les petites se logent dans la place libre."""
    for pc in pieces:
        pc['l0'], pc['h0'] = taille_cm(pc)
    restantes = sorted(pieces, key=lambda pc: -pc['l0'] * pc['h0'])
    blocs = []
    while restantes:
        pc = restantes.pop(0)
        choix = []
        for nom, (pw, ph) in FEUILLES.items():
            uw, uh = pw / CM - 2 * MARGE, ph / CM - 2 * MARGE
            for rot in (False, True):
                l, h = (pc['h0'], pc['l0']) if rot else (pc['l0'], pc['h0'])
                nc, nl = math.ceil((l + 2 * JEU) / uw), math.ceil((h + 2 * JEU) / uh)
                raccords = nl * (nc - 1) + nc * (nl - 1)
                choix.append((nc * nl, raccords, rot, nom, nc, nl, uw, uh, l, h))
        n, rac, rot, nom, nc, nl, uw, uh, l, h = min(choix)
        bloc = dict(feuille=nom, nc=nc, nl=nl, uw=uw, uh=uh, pieces=[pc])
        pc['rot'] = rot
        pc['x'], pc['y'] = (nc * uw - l) / 2, (nl * uh - h) / 2     # centrée dans le bloc
        # place libre : bandes au-dessus/au-dessous et à gauche/droite de la pièce
        libres = [(0, 0, nc * uw, pc['y']), (0, pc['y'] + h, nc * uw, nl * uh),
                  (0, 0, pc['x'], nl * uh), (pc['x'] + l, 0, nc * uw, nl * uh)]
        for pt in list(restantes):
            for r in (False, True):
                pl, ph_ = (pt['h0'], pt['l0']) if r else (pt['l0'], pt['h0'])
                zone = next((z for z in libres if z[2] - z[0] >= pl + 2 * ECART and z[3] - z[1] >= ph_ + 2 * ECART), None)
                if zone:
                    pt['rot'] = r; pt['x'], pt['y'] = zone[0] + ECART, zone[1] + ECART
                    bloc['pieces'].append(pt); restantes.remove(pt)
                    libres.remove(zone)
                    libres += [(zone[0], pt['y'] + ph_ + ECART, zone[2], zone[3]),
                               (pt['x'] + pl + ECART, zone[1], zone[2], pt['y'] + ph_ + ECART)]
                    break
        blocs.append(bloc)
    return blocs


def dessiner(c, pieces, ox, oy, e=1.0, detail=True):
    """Bloc -> PDF : (ox, oy) = position PDF du coin haut-gauche du bloc, e = échelle."""
    for pc in pieces:
        P = lambda px, py: (lambda q: (ox + q[0] * CM * e, oy - q[1] * CM * e))(local(pc, px, py))
        for style, cmds in pc['chemins']:
            remplir = style.get('fill', 'black') != 'none'
            if not detail and remplir:
                continue                      # pas de texte sur le plan réduit
            p = c.beginPath()
            for op, v in cmds:
                if op == 'M':
                    p.moveTo(*P(v[0], v[1]))
                elif op == 'L':
                    p.lineTo(*P(v[0], v[1]))
                elif op == 'C':
                    p.curveTo(*P(v[0], v[1]), *P(v[2], v[3]), *P(v[4], v[5]))
                else:
                    p.close()
            c.setLineWidth(float(style.get('stroke-width', 1)) * PT_PX * (1 if detail else 0.5))
            if remplir:
                c.drawPath(p, stroke=0, fill=1, fillMode=0 if style.get('fill-rule') == 'evenodd' else 1)
            else:
                c.drawPath(p, stroke=1, fill=0)


def touchees(bloc):
    """Feuilles du bloc traversées par un tracé (les autres ne sont pas imprimées)."""
    res = set()
    for pc in bloc['pieces']:
        for _, cmds in pc['chemins']:
            prev = None
            for op, v in cmds:
                if not v:
                    continue
                q = local(pc, v[-2], v[-1])
                for t in range(9 if prev else 1):
                    x = q[0] if prev is None else prev[0] + (q[0] - prev[0]) * t / 8
                    y = q[1] if prev is None else prev[1] + (q[1] - prev[1]) * t / 8
                    res.add((min(int(y // bloc['uh']), bloc['nl'] - 1), min(int(x // bloc['uw']), bloc['nc'] - 1)))
                prev = q
    return res


def exporter(svg, dst, titre, sm2d=None, format='A4'):
    global FEUILLES
    FEUILLES = {'portrait': FORMATS[format], 'paysage': FORMATS[format][::-1]}
    pieces = lire_svg(svg)
    taille, coupe = infos_sm2d(sm2d)
    carre = next((pc for pc in pieces if pc['nom'].lower().startswith('carr')), None)
    if carre:
        pieces.remove(carre)                  # imprimé sur la notice, à l'échelle 1
    blocs = assemblages(pieces)
    pages = []
    for b in blocs:
        b['pleines'] = touchees(b)
        b['nom'] = ' + '.join(pc['nom'] for pc in b['pieces'])
        for r in range(b['nl']):
            for k in range(b['nc']):
                if (r, k) in b['pleines']:
                    pages.append((b, r, k))
    for i, (b, r, k) in enumerate(pages):
        b.setdefault('num', {})[(r, k)] = i + 2
    nomp = lambda r, k: '%s%d' % (chr(65 + r), k + 1)

    c = canvas.Canvas(dst, pagesize=FORMATS[format])
    c.setTitle(('%s, taille %s' % (titre, taille) if taille else titre) + ', ' + format)
    W0, H0 = FORMATS[format]
    y = H0 - 1.8 * CM
    c.setFont('Helvetica-Bold', 20); c.drawString(1.8 * CM, y, titre); y -= 22
    c.setFont('Helvetica', 12)
    c.drawString(1.8 * CM, y, ('Taille %s · ' % taille if taille else '') + 'tracé et export Seamly2D'); y -= 24
    notice = ("Imprimer à 100 % (« taille réelle », sans ajustement à la page). Vérifier le carré de "
              "contrôle ci-contre : 5 cm de côté. Chaque pièce a ses propres feuilles : couper chaque "
              "feuille sur le cadre gris là où elle touche une voisine, puis scotcher bord à bord selon "
              "le plan (lettre = rangée, chiffre = colonne). Tracé extérieur : ligne de coupe, coutures "
              "comprises ; tracé intérieur : ligne de couture.")
    c.setFont('Helvetica', 10)
    for t in simpleSplit(notice, 'Helvetica', 10, 12 * CM):
        c.drawString(1.8 * CM, y, t); y -= 13
    if carre:
        carre['rot'] = False; carre['x'] = carre['y'] = 0
        carre['l0'], carre['h0'] = taille_cm(carre)
        dessiner(c, [carre], W0 - 1.8 * CM - carre['l0'] * CM, H0 - 1.8 * CM)
    y -= 8
    c.setFont('Helvetica-Bold', 11); c.drawString(1.8 * CM, y, 'Pièces et assemblages (%d feuilles %s)' % (len(pages), format)); y -= 15
    c.setFont('Helvetica', 10)
    for b in blocs:
        n = len(b['pleines'])
        rac = sum(1 for (r, k) in b['pleines'] for (rr, kk) in ((r + 1, k), (r, k + 1)) if (rr, kk) in b['pleines'])
        quoi = ', '.join(pc['nom'] + (' (' + coupe[pc['nom']].lower() + ')' if pc['nom'] in coupe else '') for pc in b['pieces'])
        pp = sorted(b['num'].values())
        ligne = '%s : %d feuille%s %s, %d raccord%s, pages %s' % (
            quoi, n, 's' if n > 1 else '', b['feuille'], rac, 's' if rac > 1 else '',
            '%d à %d' % (pp[0], pp[-1]) if len(pp) > 1 else pp[0])
        larg = 12 * CM if carre and y > H0 - 2.5 * CM - carre['h0'] * CM else W0 - 3.6 * CM
        for t in simpleSplit(ligne, 'Helvetica', 10, larg):
            c.drawString(2.1 * CM, y, t); y -= 13
    # plans d'assemblage, à la même échelle, rangés en lignes
    y -= 14
    dispo = W0 - 3.6 * CM - 0.8 * CM * (len(blocs) - 1)
    e = min(0.12, dispo / CM / sum(max(b['nc'] * b['uw'], 2 / 0.12) for b in blocs),
            (y - 2 * CM) / CM / max(b['nl'] * b['uh'] for b in blocs))
    x, haut = 1.8 * CM, 0
    for b in blocs:
        bw, bh = b['nc'] * b['uw'] * CM * e, b['nl'] * b['uh'] * CM * e
        if x + bw > W0 - 1.8 * CM:
            x, y, haut = 1.8 * CM, y - haut - 22, 0
        c.setFillGray(0)
        lignes = simpleSplit(b['nom'], 'Helvetica-Bold', 8, max(bw, 2 * CM))
        for j, t in enumerate(lignes):
            c.setFont('Helvetica-Bold', 8); c.drawString(x, y - 9 - 9 * j + 9 * (len(lignes) - 1), t)
        for r in range(b['nl']):
            for k in range(b['nc']):
                X, Y = x + k * b['uw'] * CM * e, y - 14 - (r + 1) * b['uh'] * CM * e
                ok = (r, k) in b['pleines']
                c.setLineWidth(0.4); c.setStrokeGray(0.55 if ok else 0.85)
                c.rect(X, Y, b['uw'] * CM * e, b['uh'] * CM * e)
                c.setFillGray(0.45 if ok else 0.75); c.setFont('Helvetica', 6.5)
                c.drawString(X + 2, Y + b['uh'] * CM * e - 8, nomp(r, k) + (' p. %d' % b['num'][(r, k)] if ok else ' vide'))
        c.setStrokeGray(0); c.setFillGray(0)
        dessiner(c, b['pieces'], x, y - 14, e, detail=False)
        x += max(bw, 2 * CM) + 0.8 * CM; haut = max(haut, bh + 14)
    c.showPage()

    for i, (b, r, k) in enumerate(pages):
        pw, ph = FEUILLES[b['feuille']]
        uw, uh = b['uw'], b['uh']
        c.setPageSize((pw, ph))
        c.saveState()
        p = c.beginPath(); p.rect(MARGE * CM, MARGE * CM, uw * CM, uh * CM)
        c.clipPath(p, stroke=0, fill=0)
        dessiner(c, b['pieces'], (MARGE - k * uw) * CM, ph - (MARGE - r * uh) * CM)
        c.restoreState()
        c.setLineWidth(0.3); c.setStrokeGray(0.55)
        c.rect(MARGE * CM, MARGE * CM, uw * CM, uh * CM)
        c.setStrokeGray(0); c.setFillGray(0.3); c.setFont('Helvetica', 7)
        c.drawString(MARGE * CM + 4, ph - MARGE * CM - 9, '%s · %s · feuille %s · page %d/%d' % (
            titre, b['nom'], nomp(r, k), i + 2, len(pages) + 1))
        # nom de la voisine sur chaque bord à raccorder
        for (rr, kk), cote in (((r - 1, k), 'haut'), ((r + 1, k), 'bas'), ((r, k - 1), 'gauche'), ((r, k + 1), 'droite')):
            if (rr, kk) not in b['pleines']:
                continue
            t = 'raccord ' + nomp(rr, kk)
            c.saveState()
            if cote == 'haut':
                c.translate(pw / 2, ph - MARGE * CM - 9)
            elif cote == 'bas':
                c.translate(pw / 2, MARGE * CM + 3)
            elif cote == 'gauche':
                c.translate(MARGE * CM + 9, ph / 2); c.rotate(90)
            else:
                c.translate(MARGE * CM + uw * CM - 3, ph / 2); c.rotate(90)
            c.drawCentredString(0, 0, t); c.restoreState()
        c.setFillGray(0)
        c.showPage()
    c.save()
    return len(pages) + 1


if __name__ == '__main__':
    fmt = 'A3' if '--a3' in sys.argv else 'A4'
    args = [a for a in sys.argv[1:] if a != '--a3']
    n = exporter(args[0], args[1], args[2], args[3] if len(args) > 3 else None, fmt)
    print(sys.argv[2], n, 'pages')
