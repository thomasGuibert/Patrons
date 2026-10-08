"""Patron imprimable (PDF A4 à l'échelle 1) depuis un .sm2d, sans Seamly.

Pièces avec ligne de coupe (couture comprise, largeurs before/after des nœuds), ligne de
couture en tirets, crans, droit-fil et étiquettes aux positions du fichier. Page 1 : notice,
carré de contrôle 5 × 5 cm et plan d'assemblage ; puis les pages A4 à scotcher bord à bord.
Usage (depuis le dossier du .sm2d) : python3 exporter_pdf.py fichier.sm2d sortie.pdf [titre]
"""
import math, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from evaluer_hors_seamly import Pattern
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

PX = 37.795          # pixels Seamly par cm
CM = 72 / 2.54       # points PDF par cm
MARGE = 1.0          # marge de page (cm)
ECART = 1.5          # écart entre pièces sur le plan (cm)


def nearest(pts, q):
    return min(range(len(pts)), key=lambda i: math.dist(pts[i], q))


def contour(p, mod, pc):
    """Sommets [(x, y), avant, après, cran] du contour fini, repère y vers le haut."""
    w = float(pc.get('width') or 0) if pc.get('seamAllowance') == 'true' else 0.0
    nodes = list(pc.iter('node'))
    seq = []
    for n in nodes:
        o = mod[n.get('idObject')]
        if n.get('type') == 'NodePoint':
            b, a = n.get('before'), n.get('after')
            seq.append(('P', p.P[o], float(b) if b else w, float(a) if a else w, n.get('notch') == 'true'))
        else:
            pts = list(p.curve_by_id[o])
            if n.get('reverse') == '1':
                pts = pts[::-1]
            seq.append(('C', pts))
    head = lambda it: it[1] if it[0] == 'P' else it[1][0]
    tail = lambda it: it[1] if it[0] == 'P' else it[1][-1]
    out = []
    for k, it in enumerate(seq):
        if it[0] == 'P':
            out.append([it[1], it[2], it[3], it[4]])
            continue
        v = it[1]
        prv, nxt = seq[k - 1], seq[(k + 1) % len(seq)]
        i0 = nearest(v, tail(prv)) if prv[0] == 'P' else 0
        i1 = nearest(v, head(nxt)) if nxt[0] == 'P' else len(v) - 1
        part = v[i0:i1 + 1] if i1 >= i0 else v[i1:i0 + 1][::-1]
        # largeur interpolée le long de la courbe, de l'« après » du nœud précédent
        # à l'« avant » du suivant (comme Seamly)
        wa = prv[3] if prv[0] == 'P' else w
        wb = nxt[2] if nxt[0] == 'P' else w
        L = [0.0]
        for i in range(1, len(part)):
            L.append(L[-1] + math.dist(part[i - 1], part[i]))
        tot = L[-1] or 1
        for q, l in zip(part, L):
            x = wa + (wb - wa) * l / tot
            out.append([q, x, x, False])
    # fusion des points confondus (bouts de courbe sur les nœuds) : le nœud garde ses largeurs
    res = []
    for s in out:
        if res and math.dist(res[-1][0], s[0]) < 1e-4:
            if s[3] or s[1] != s[2]:
                res[-1] = [s[0], s[1], s[2], s[3] or res[-1][3]]
            continue
        res.append(s)
    if len(res) > 1 and math.dist(res[0][0], res[-1][0]) < 1e-4:
        last = res.pop()
        res[0][1] = last[1] if res[0][1] == res[0][2] and not (last[1] == last[2]) else res[0][1]
    return res, w


def aire(pts):
    return sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1]
               for i in range(len(pts))) / 2


def coupe(sommets):
    """Ligne de coupe : chaque arête décalée vers l'extérieur, raccords en onglet."""
    pts = [s[0] for s in sommets]
    n = len(pts)
    sg = 1 if aire(pts) > 0 else -1
    lignes = []
    for i in range(n):
        a, b = pts[i], pts[(i + 1) % n]
        dx, dy = b[0] - a[0], b[1] - a[1]
        l = math.hypot(dx, dy) or 1
        nx, ny = sg * dy / l, -sg * dx / l
        ws, we = sommets[i][2], sommets[(i + 1) % n][1]
        lignes.append(((a[0] + nx * ws, a[1] + ny * ws), (b[0] + nx * we, b[1] + ny * we)))
    res = []
    for i in range(n):
        (p1, p2), (p3, p4) = lignes[i - 1], lignes[i]
        d = (p1[0] - p2[0]) * (p3[1] - p4[1]) - (p1[1] - p2[1]) * (p3[0] - p4[0])
        lim = 3 * max(sommets[i][1], sommets[i][2], 0.3)
        if abs(d) > 1e-9:
            t = ((p1[0] - p3[0]) * (p3[1] - p4[1]) - (p1[1] - p3[1]) * (p3[0] - p4[0])) / d
            q = (p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1]))
            if math.dist(q, pts[i]) <= lim:
                res.append(q)
                continue
        if math.dist(p2, p3) < 1e-6:
            res.append(p2)
        else:
            res += [p2, p3]          # angle trop aigu : coin coupé
    return res


def attrs(el):
    return el.attrib if el is not None else None


def lire(path):
    p = Pattern(path)
    mod = {}
    for b in p.root.iter('draftBlock'):
        for e in b.find('modeling'):
            mod[e.get('id')] = e.get('idObject')
    etiquette = [l.get('text') for l in (p.root.find('patternLabel') if p.root.find('patternLabel') is not None else [])]
    taille = ''
    m = p.root.find('measurements')
    if m is not None and m.text:
        taille = re.sub(r'\D', '', os.path.basename(m.text)) or ''
    pieces = []
    for pc in p.root.iter('piece'):
        if pc.get('inLayout') == 'false':
            continue
        sommets, w = contour(p, mod, pc)
        fini = [s[0] for s in sommets]
        cut = coupe(sommets) if pc.get('seamAllowance') == 'true' else fini
        crans = []
        idx = {id(s): i for i, s in enumerate(sommets)}
        for i, s in enumerate(sommets):
            if s[3]:
                # cran : du point fini vers la ligne de coupe, sur la bissectrice extérieure
                a, b, c = fini[i - 1], fini[i], fini[(i + 1) % len(fini)]
                sg = 1 if aire(fini) > 0 else -1
                def nrm(u, v):
                    dx, dy = v[0] - u[0], v[1] - u[1]; l = math.hypot(dx, dy) or 1
                    return (sg * dy / l, -sg * dx / l)
                n1, n2 = nrm(a, b), nrm(b, c)
                nx, ny = n1[0] + n2[0], n1[1] + n2[1]; l = math.hypot(nx, ny) or 1
                ww = max(s[1], s[2], 0.4)
                crans.append((b, (b[0] + nx / l * ww, b[1] + ny / l * ww)))
        boites = []
        for tag in ('patternInfo', 'data'):
            el = pc.find(tag)
            if el is None or el.get('visible') != 'true':
                continue
            x, y = float(el.get('mx')) / PX, -float(el.get('my')) / PX
            wd, ht = float(el.get('width')), float(el.get('height'))
            if tag == 'data':
                q = int(el.get('quantity') or 1)
                txt = [(pc.get('name'), True),
                       (('Couper %d fois au pli' % q) if el.get('onFold') == 'true'
                        else ('Couper %d fois' % q if q > 1 else 'Couper 1 fois'), False)]
                if q > 1 and el.get('onFold') != 'true':
                    txt.append(('(en symétrie)', False))
            else:
                txt = []
                for t in etiquette:
                    t = t.replace('%size%', taille).replace('%pName%', pc.get('name'))
                    if '%' not in t:
                        txt.append((t, False))
            boites.append(((x, y - ht, x + wd, y), txt))
        fil = None
        el = pc.find('grainline')
        if el is not None and el.get('visible') == 'true':
            x, y = float(el.get('mx')) / PX, -float(el.get('my')) / PX
            r = math.radians(float(el.get('rotation') or 90))
            L = float(el.get('length'))
            fil = ((x, y), (x + L * math.cos(r), y + L * math.sin(r)), float(el.get('arrowLength') or 1))
        pli = None
        if pc.find('data') is not None and pc.find('data').get('onFold') == 'true':
            for i, s in enumerate(sommets):
                j = (i + 1) % len(sommets)
                if s[2] == 0 and sommets[j][1] == 0 and math.dist(fini[i], fini[j]) > 1:
                    pli = (fini[i], fini[j])
        pieces.append(dict(nom=pc.get('name'), fini=fini, coupe=cut, crans=crans, boites=boites,
                           fil=fil, pli=pli, couture=pc.get('seamAllowance') == 'true'))
    return pieces, etiquette, taille


def ranger(pieces, largeur):
    """Rangement en étagères, sans rotation (le droit-fil reste vertical)."""
    for pc in pieces:
        xs = [q[0] for q in pc['coupe']]; ys = [q[1] for q in pc['coupe']]
        pc['bb'] = (min(xs), min(ys), max(xs), max(ys))
    ordre = sorted(pieces, key=lambda pc: -(pc['bb'][3] - pc['bb'][1]))
    x = y = ECART; haut = 0
    for pc in ordre:
        w = pc['bb'][2] - pc['bb'][0]; h = pc['bb'][3] - pc['bb'][1]
        if x + w + ECART > largeur and x > ECART:
            x = ECART; y += haut + ECART; haut = 0
        pc['dx'] = x - pc['bb'][0]; pc['dy'] = -(y) - pc['bb'][3]   # plan : y vers le bas
        x += w + ECART; haut = max(haut, h)
    return max(largeur, max(pc['dx'] + pc['bb'][2] for pc in pieces) + ECART), y + haut + ECART


def dessiner(c, pieces, tr, k=1.0, detail=True):
    """tr : (x, y) plan (cm, y vers le haut, origine coin haut-gauche) -> points PDF."""
    for pc in pieces:
        m = lambda q: tr((q[0] + pc['dx'], q[1] + pc['dy']))
        def poly(pts, ferme=True):
            pth = c.beginPath(); pth.moveTo(*m(pts[0]))
            for q in pts[1:]:
                pth.lineTo(*m(q))
            if ferme:
                pth.close()
            c.drawPath(pth, stroke=1, fill=0)
        c.setDash(); c.setLineWidth(1.0 * k if detail else 0.6)
        poly(pc['coupe'])
        if not detail:
            continue
        if pc['couture']:
            c.setLineWidth(0.5); c.setDash(4, 3)
            poly(pc['fini'])
            c.setDash()
        c.setLineWidth(0.8)
        for a, b in pc['crans']:
            c.line(*m(a), *m(b))
        if pc['pli']:
            a, b = pc['pli']
            c.setLineWidth(0.5); c.setDash(1, 2); c.line(*m(a), *m(b)); c.setDash()
            # mention « pli » le long du bord, côté intérieur de la pièce
            sg = 1 if aire(pc['fini']) > 0 else -1
            dx, dy = b[0] - a[0], b[1] - a[1]; l = math.hypot(dx, dy)
            mid = ((a[0] + b[0]) / 2 - sg * dy / l * 0.5, (a[1] + b[1]) / 2 + sg * dx / l * 0.5)
            X, Y = m(mid); X1, Y1 = m(b); X0, Y0 = m(a)
            ang = math.degrees(math.atan2(Y1 - Y0, X1 - X0))
            if ang > 90 or ang <= -90:
                ang += 180
            c.saveState(); c.translate(X, Y); c.rotate(ang)
            c.setFont('Helvetica', 9 * k); c.drawCentredString(0, -3, 'PLI DU TISSU'); c.restoreState()
        if pc['fil']:
            a, b, al = pc['fil']
            c.setLineWidth(0.8); c.line(*m(a), *m(b))
            for p0, p1 in ((a, b), (b, a)):
                ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
                for s in (1, -1):
                    q = (p1[0] - al * math.cos(ang + s * 0.4), p1[1] - al * math.sin(ang + s * 0.4))
                    c.line(*m(p1), *m(q))
        for (x0, y0, x1, y1), txt in pc['boites']:
            if not txt:
                continue
            X0, Y0 = m((x0, y0)); X1, Y1 = m((x1, y1))
            w, h = X1 - X0, Y1 - Y0
            poids = [1.4 if gras else 1.0 for _, gras in txt]
            fs = h / (sum(poids) * 1.25)
            for t, gras in txt:
                f = 'Helvetica-Bold' if gras else 'Helvetica'
                fs = min(fs, w / max(c.stringWidth(t, f, 1) * (1.4 if gras else 1), 1e-6))
            fs = min(fs, 16)
            y = Y1 - (h - sum(poids) * fs * 1.25) / 2
            for (t, gras), pw in zip(txt, poids):
                f = 'Helvetica-Bold' if gras else 'Helvetica'
                y -= fs * pw * 1.25
                c.setFont(f, fs * pw); c.drawCentredString((X0 + X1) / 2, y + fs * pw * 0.25, t)


def exporter(src, dst, titre=None):
    pieces, etiquette, taille = lire(src)
    titre = titre or (etiquette[0] if etiquette else os.path.basename(src))
    meilleur = None
    for pw, ph in (A4, A4[::-1]):
        uw, uh = pw / CM - 2 * MARGE, ph / CM - 2 * MARGE
        for nc in range(1, 7):
            W, H = ranger(pieces, nc * uw)
            ncol, nlig = math.ceil(W / uw), math.ceil(H / uh)
            # pages non vides
            pleines = set()
            for pc in pieces:
                for q in pc['coupe']:
                    x, y = q[0] + pc['dx'], -(q[1] + pc['dy'])
                    pleines.add((int(y // uh), int(x // uw)))
            score = (len(pleines), ncol * nlig)
            if meilleur is None or score < meilleur[0]:
                meilleur = (score, (pw, ph), nc, ncol, nlig, uw, uh)
    _, (pw, ph), nc, ncol, nlig, uw, uh = meilleur
    ranger(pieces, nc * uw)
    pleines = set()
    for pc in pieces:
        pts = pc['coupe']
        for i in range(len(pts)):
            a, b = pts[i], pts[(i + 1) % len(pts)]
            for t in range(11):
                x = a[0] + (b[0] - a[0]) * t / 10 + pc['dx']; y = -(a[1] + (b[1] - a[1]) * t / 10 + pc['dy'])
                pleines.add((int(y // uh), int(x // uw)))
    nomp = lambda r, k: '%s%d' % (chr(65 + r), k + 1)
    pages = [(r, k) for r in range(nlig) for k in range(ncol) if (r, k) in pleines]

    c = canvas.Canvas(dst, pagesize=A4)
    c.setTitle('%s, taille %s' % (titre, taille))
    # page 1 : notice
    W0, H0 = A4
    y = H0 - 2 * CM
    c.setFont('Helvetica-Bold', 20); c.drawString(2 * CM, y, titre); y -= 22
    sous = [t for t in etiquette[1:] if '%' not in t]
    c.setFont('Helvetica', 12)
    c.drawString(2 * CM, y, ' · '.join(sous + ['taille %s' % taille] if taille else sous)); y -= 26
    lignes = ["Imprimer à 100 % (« taille réelle », sans ajustement à la page).",
              "Vérifier le carré de contrôle ci-contre : il doit mesurer 5 cm de côté.",
              "Couper chaque page sur le cadre gris, côtés droit et bas, puis scotcher bord à bord",
              "en suivant le plan d'assemblage (lettre = rangée, chiffre = colonne).",
              "Trait plein : ligne de coupe (coutures comprises). Tirets : ligne de couture.",
              "Pointillés : pli du tissu. Traits courts : crans. Flèche : droit-fil."]
    c.setFont('Helvetica', 10)
    from reportlab.lib.utils import simpleSplit
    for t in simpleSplit(' '.join(lignes[:4]), 'Helvetica', 10, 11.5 * CM) + lignes[4:]:
        c.drawString(2 * CM, y, t); y -= 14
    y -= 8
    c.setFont('Helvetica-Bold', 11); c.drawString(2 * CM, y, 'Pièces'); y -= 15
    c.setFont('Helvetica', 10)
    for pc in pieces:
        d = [t for (b, txt) in pc['boites'] for t, g in txt[1:] if 'Couper' in t]
        c.drawString(2.3 * CM, y, '%s : %s' % (pc['nom'], d[0] if d else '')); y -= 13
    # carré de contrôle
    sx, sy = W0 - 2 * CM - 5 * CM, H0 - 2 * CM - 5 * CM
    c.setLineWidth(1); c.rect(sx, sy, 5 * CM, 5 * CM)
    c.setFont('Helvetica', 9); c.drawCentredString(sx + 2.5 * CM, sy + 2.5 * CM, '5 cm × 5 cm')
    # plan d'assemblage
    y -= 10
    c.setFont('Helvetica-Bold', 11); c.drawString(2 * CM, y, "Plan d'assemblage (%d pages)" % len(pages)); y -= 10
    bw, bh = W0 - 4 * CM, y - 2 * CM
    e = min(bw / (ncol * uw), bh / (nlig * uh))
    ox, oy = 2 * CM, y
    tr = lambda q: (ox + q[0] * e, oy + q[1] * e)
    num = {pg: i + 2 for i, pg in enumerate(pages)}
    for r in range(nlig):
        for k in range(ncol):
            X, Y = ox + k * uw * e, oy - (r + 1) * uh * e
            c.setLineWidth(0.4); c.setStrokeGray(0.6 if (r, k) in num else 0.85)
            c.rect(X, Y, uw * e, uh * e)
            c.setFillGray(0.5 if (r, k) in num else 0.8); c.setFont('Helvetica', 7)
            c.drawString(X + 2, Y + uh * e - 8, nomp(r, k) + (' (p. %d)' % num[(r, k)] if (r, k) in num else ' vide'))
    c.setStrokeGray(0); c.setFillGray(0)
    dessiner(c, pieces, tr, detail=False)
    for pc in pieces:
        x0, y0, x1, y1 = pc['bb']
        X, Y = tr(((x0 + x1) / 2 + pc['dx'], (y0 + y1) / 2 + pc['dy']))
        c.setFont('Helvetica', 7); c.drawCentredString(X, Y, pc['nom'])
    c.showPage()
    # pages à l'échelle 1
    for i, (r, k) in enumerate(pages):
        ox, oy = MARGE * CM - k * uw * CM, ph - MARGE * CM + r * uh * CM
        c.setPageSize((pw, ph))
        c.saveState()
        pth = c.beginPath(); pth.rect(MARGE * CM, MARGE * CM, uw * CM, uh * CM)
        c.clipPath(pth, stroke=0, fill=0)
        x0, x1 = k * uw, (k + 1) * uw
        y0, y1 = -(r + 1) * uh, -r * uh
        vues = [pc for pc in pieces if pc['bb'][2] + pc['dx'] > x0 and pc['bb'][0] + pc['dx'] < x1
                and pc['bb'][3] + pc['dy'] > y0 and pc['bb'][1] + pc['dy'] < y1]
        dessiner(c, vues, lambda q: (ox + q[0] * CM, oy + q[1] * CM))
        c.restoreState()
        c.setLineWidth(0.3); c.setStrokeGray(0.55)
        c.rect(MARGE * CM, MARGE * CM, uw * CM, uh * CM)
        c.setStrokeGray(0); c.setFillGray(0.35); c.setFont('Helvetica', 8)
        c.drawString(MARGE * CM, ph - MARGE * CM + 8, '%s · taille %s · page %s (%d/%d)' % (
            titre, taille, nomp(r, k), i + 2, len(pages) + 1))
        voisins = [((r - 1, k), 'haut'), ((r + 1, k), 'bas'), ((r, k - 1), 'gauche'), ((r, k + 1), 'droite')]
        for (rr, kk), cote in voisins:
            if (rr, kk) not in pleines:
                continue
            t = '%s' % nomp(rr, kk)
            if cote == 'haut':
                c.drawCentredString(pw / 2, ph - MARGE * CM + 8, '↑ ' * 0 + t)
            elif cote == 'bas':
                c.drawCentredString(pw / 2, MARGE * CM - 12, t)
            elif cote == 'gauche':
                c.saveState(); c.translate(MARGE * CM - 6, ph / 2); c.rotate(90); c.drawCentredString(0, 0, t); c.restoreState()
            else:
                c.saveState(); c.translate(MARGE * CM + uw * CM + 12, ph / 2); c.rotate(90); c.drawCentredString(0, 0, t); c.restoreState()
        c.setFillGray(0)
        c.showPage()
    c.save()
    return len(pages) + 1


if __name__ == '__main__':
    n = exporter(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
    print(sys.argv[2], n, 'pages')
