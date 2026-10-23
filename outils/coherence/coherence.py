"""Contrôles de cohérence des tracés, sur toutes les tailles et des jeux de mesures sur mesure.

Usage : python3 outils/coherence/coherence.py [patron ...] [--maj-references] [--seamly]
        (sans patron : chaque patrons/<patron>.coherence.toml)

Pour chaque patron décrit par patrons/<patron>.coherence.toml, et pour chaque jeu de mesures
(tailles des gammes du fichier, profils de mesures/profils-essai.toml) :
1. Courbes sans angle : pas de coin le long d'une courbe, ni aux raccords entre pièces une fois
   cousues (les angles de part et d'autre de la couture font 180°), ni au pli.
2. Points immobiles : chaque point du tracé est à la place notée dans
   patrons/references/<patron>.json. Après un déplacement voulu : --maj-references.
3. Longueurs : les deux bords d'une couture ont la longueur attendue (écart b − a dans la plage ;
   b − rapport × a pour un bord réduit, comme un bord-côte).
4. Crans : les crans d'un bord tombent sur ceux de l'autre (l'écart de longueur peut se répartir).
--seamly : vérifie aussi que le calcul hors Seamly trace comme Seamly (périmètre et dimensions
de chaque pièce), avec Seamly2D (variable SEAMLY2D ; sous Linux, lancer sous xvfb-run).
Sortie en Markdown ; code de retour 1 si un contrôle échoue. Mode d'emploi : skill verifier-patron.
"""
import glob, json, math, os, re, shutil, subprocess, sys, tempfile, tomllib

from pieces import RACINE, ev, pieces

PATRONS = os.path.join(RACINE, 'patrons')
REFERENCES = os.path.join(PATRONS, 'references')
PROFILS = os.path.join(RACINE, 'mesures', 'profils-essai.toml')
# profils sur mesure : comme le site, mesures manquantes prises en femme 40
BASE_PROFILS = os.path.join(RACINE, 'mesures', 'femme', 'T40.smms')

ANGLE_MAX = 1.0       # degrés, coin toléré sur une courbe ou à un raccord
POINT_MAX = 0.005     # cm, déplacement toléré d'un point (0,05 mm)
ECART_COUTURE = (-0.1, 0.1)   # cm, b − a par défaut
CRAN_MAX = 0.15       # cm, au-delà de la part d'écart de longueur
SEAMLY_MAX = 0.05     # cm, calcul hors Seamly contre export Seamly


def fr(x, d=2):
    return f'{x:.{d}f}'.replace('.', ',').replace('-', '−')


# ---------- jeux de mesures

def jeux(config):
    """[(étiquette, fichier de mesures, valeurs remplacées)]"""
    res = []
    for gamme in config.get('gammes', []):
        for f in sorted(glob.glob(os.path.join(RACINE, 'mesures', gamme, 'T*.smms')),
                        key=lambda f: int(re.search(r'T(\d+)', f).group(1))):
            res.append((f'{gamme} {re.search(r"T(\d+)", f).group(1)}', f, None))
    if config.get('profils', False):
        with open(PROFILS, 'rb') as f:
            for nom, valeurs in tomllib.load(f).items():
                res.append((f'sur mesure « {nom} »', BASE_PROFILS, {k: float(v) for k, v in valeurs.items()}))
    return res


# ---------- géométrie

def tourne(a, b, c):
    """Angle signé (degrés, sens trigo) dont tourne a→b→c en b."""
    u = (b[0] - a[0], b[1] - a[1]); v = (c[0] - b[0], c[1] - b[1])
    return math.degrees(math.atan2(u[0] * v[1] - u[1] * v[0], u[0] * v[0] + u[1] * v[1]))


def sens(piece):
    p = piece.pts
    aire = sum(p[i - 1][0] * p[i][1] - p[i][0] * p[i - 1][1] for i in range(len(p)))
    return 1 if aire > 0 else -1


def angle_interieur(piece, nom):
    """Angle intérieur de la pièce au point nommé (degrés, 0 à 360)."""
    i, p = piece.repere[nom], piece.pts
    return 180 - sens(piece) * tourne(p[i - 1], p[i], p[(i + 1) % len(p)])


def proche(piece, i):
    """Point nommé le plus proche (sur le contour) de l'indice i : « vKp » ou « 2,1 cm après vKp »."""
    nom, j = min(piece.repere.items(), key=lambda kv: min(abs(piece.cumul[kv[1]] - piece.cumul[i]),
                                                       piece.tour - abs(piece.cumul[kv[1]] - piece.cumul[i])))
    d = math.dist(piece.pts[i], piece.pts[j])
    return nom if d < 0.05 else f'à {fr(d, 1)} cm de {nom}'


# ---------- 1. courbes sans angle

def angles_courbe(pcs, c):
    """[(angle en degrés, où)] : coins le long des tronçons et aux raccords."""
    tr = c['troncons']
    res = []
    for piece, a, b in tr:
        p = pcs[piece]
        idx = p.indices(a, b)
        t = [tourne(p.pts[idx[k - 1]], p.pts[idx[k]], p.pts[idx[k + 1]]) for k in range(1, len(idx) - 1)]
        pire = (0.0, None)
        for k in range(len(t)):
            voisins = [t[j] for j in (k - 1, k + 1) if 0 <= j < len(t)]
            coin = abs(t[k] - sum(voisins) / len(voisins)) if voisins else abs(t[k])
            if coin > pire[0]:
                pire = (coin, k + 1)
        if pire[1] is not None:
            res.append((pire[0], f'{piece} {proche(p, idx[pire[1]])}'))
    raccords = list(zip(tr, tr[1:])) + ([(tr[-1], tr[0])] if c.get('fermee') else [])
    for (p1, _, b1), (p2, a2, _) in raccords:
        somme = angle_interieur(pcs[p1], b1) + angle_interieur(pcs[p2], a2)
        lieu = f'{p1} {b1}' if (p1, b1) == (p2, a2) else f'raccord {p1} {b1} / {p2} {a2}'
        res.append((abs(somme - 180), lieu))
    for cle, (piece, pt) in (('pli_debut', (tr[0][0], tr[0][1])), ('pli_fin', (tr[-1][0], tr[-1][2]))):
        if c.get(cle):
            res.append((abs(2 * angle_interieur(pcs[piece], pt) - 180), f'pli {piece} {pt}'))
    return res


# ---------- 3 et 4. coutures et crans

def bord(pcs, troncons, raccords=True):
    """Longueur du bord et repères le long du bord : crans et (si raccords) raccords entre tronçons."""
    long, reperes = 0.0, []
    for k, (piece, a, b) in enumerate(troncons):
        pts, crans = pcs[piece].troncon(a, b)
        if k and raccords:
            reperes.append((long, f'raccord {troncons[k - 1][0]} {troncons[k - 1][2]} / {piece} {a}'))
        reperes += [(long + d, f'cran {piece} {n}') for d, n in crans]
        long += sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))
    return long, reperes


def controler_couture(pcs, c, motif):
    """(écart b − rapport × a, [messages sur les crans])"""
    raccords = c.get('crans_aux_raccords', True)
    k = c.get('rapport', 1)
    k = motif.ev(k) if isinstance(k, str) else float(k)
    la, ra = bord(pcs, c['a'], raccords)
    lb, rb = bord(pcs, c['b'], raccords)
    la, ra = la * k, [(d * k, n) for d, n in ra]
    ecart = lb - la
    msgs = []
    if len(ra) != len(rb):
        msgs.append(f'{len(ra)} repère(s) d\'un côté ({", ".join(n for _, n in ra) or "aucun"}), '
                    f'{len(rb)} de l\'autre ({", ".join(n for _, n in rb) or "aucun"})')
        return ecart, msgs
    bas, haut = min(0, ecart) - CRAN_MAX, max(0, ecart) + CRAN_MAX
    for (da, na), (db, nb) in zip(ra, rb):
        if not bas <= db - da <= haut:
            msgs.append(f'{na} à {fr(da)} cm, {nb} à {fr(db)} cm (écart {fr(db - da)}, '
                        f'longueurs : {fr(ecart)})')
    return ecart, msgs


def crans_orphelins(pcs, coutures):
    vus = set()
    for c in coutures:
        for piece, a, b in c['a'] + c['b']:
            p = pcs[piece]
            vus |= {(piece, i) for i in p.indices(a, b)}
    return [f'{n} ({nom})' for nom, p in pcs.items() for i, n in p.crans.items() if (nom, i) not in vus]


# ---------- 2. points

def points(motif):
    return {motif.name[i]: [round(x, 3), round(y, 3)] for i, (x, y) in motif.P.items()}


def ecrire_references(chemin, refs):
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    lignes = ['{']
    for k, (jeu, pts) in enumerate(refs.items()):
        lignes.append(f'  {json.dumps(jeu, ensure_ascii=False)}: {{')
        lignes += [f'    {json.dumps(n, ensure_ascii=False)}: [{x}, {y}]' + (',' if j < len(pts) - 1 else '')
                   for j, (n, (x, y)) in enumerate(pts.items())]
        lignes.append('  }' + (',' if k < len(refs) - 1 else ''))
    lignes.append('}')
    open(chemin, 'w', encoding='utf-8').write('\n'.join(lignes) + '\n')


def comparer_points(ref, actuels, types):
    bouges = []
    for n, (x, y) in ref.items():
        if n not in actuels:
            bouges.append(f'{n} supprimé')
        else:
            d = math.dist((x, y), actuels[n])
            if d > POINT_MAX:
                bouges.append(f'{n} ({types.get(n, "?")}) déplacé de {fr(d * 10, 1)} mm')
    nouveaux = [n for n in actuels if n not in ref]
    return bouges, nouveaux


# ---------- 0. Seamly

def contours_seamly(sm2d, mesures, valeurs, tmp):
    """{pièce: (périmètre, largeur, hauteur)} de l'export Seamly, ou None et le message d'erreur."""
    sys.path.insert(0, os.path.join(RACINE, '.claude', 'skills', 'exporter-pdf'))
    sys.path.insert(0, os.path.join(RACINE, '.claude', 'skills', 'tracer-sm2d'))
    from mesures_vers_pdf import ecrire_vit
    from verifier import pieces as pieces_svg
    seamly = os.environ.get('SEAMLY2D', r'C:\Program Files (x86)\Seamly2D\seamly2d.exe')
    if valeurs:
        fichier = os.path.join(tmp, 'mesures.vit')
        ecrire_vit(mesures, None, valeurs, fichier)
    else:
        fichier = mesures
    sortie = os.path.join(tmp, 'svg')
    shutil.rmtree(sortie, ignore_errors=True)
    nom = os.path.splitext(os.path.basename(sm2d))[0]
    # Seamly réécrit le fichier qu'il ouvre : il travaille sur une copie (mesures liées à côté)
    copie = os.path.join(tmp, 'patrons', nom + '.sm2d')
    if not os.path.exists(copie):
        shutil.copytree(os.path.join(RACINE, 'mesures'), os.path.join(tmp, 'mesures'), dirs_exist_ok=True)
        os.makedirs(os.path.dirname(copie), exist_ok=True)
        shutil.copy(sm2d, copie)
    r = subprocess.run([seamly, '-b', nom, '-d', sortie, '-f', '0', '--exportOnlyDetails', '-m', fichier, copie],
                       capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=180)
    svg = os.path.join(sortie, nom + '_pieces.svg')
    if r.returncode != 0 or not os.path.exists(svg):
        return None, f'export Seamly en échec (code {r.returncode})'
    res = {}
    for piece, pts in pieces_svg(svg):
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        res[piece] = (sum(math.dist(pts[i], pts[(i + 1) % len(pts)]) for i in range(len(pts))),
                      max(xs) - min(xs), max(ys) - min(ys))
    return res, None


# ---------- rapport

class Rapport:
    def __init__(self):
        self.lignes, self.echec = [], False

    def ok(self, texte):
        self.lignes.append(f'- ✅ {texte}')

    def ko(self, texte, details=()):
        self.echec = True
        self.lignes.append(f'- ❌ {texte}')
        self.lignes += [f'  - {d}' for d in details]

    def titre(self, texte):
        self.lignes.append(f'\n{texte}\n')


def controler(nom, maj, avec_seamly, rapport):
    sm2d = os.path.join(PATRONS, nom + '.sm2d')
    with open(os.path.join(PATRONS, nom + '.coherence.toml'), 'rb') as f:
        config = tomllib.load(f)
    courbes, coutures = config.get('courbe', []), config.get('couture', [])
    chemin_ref = os.path.join(REFERENCES, nom + '.json')
    refs = json.load(open(chemin_ref, encoding='utf-8')) if os.path.exists(chemin_ref) else {}
    nouvelles_refs = {}

    angles = {c['nom']: [] for c in courbes}        # nom -> [(angle, où, jeu)]
    ecarts = {c['nom']: [] for c in coutures}       # nom -> [(écart, jeu)]
    crans = {c['nom']: [] for c in coutures}        # nom -> [message]
    orphelins, deplaces, nouveaux, seamly, erreurs = set(), [], set(), [], []
    ecart_seamly = 0.0
    tmp = tempfile.mkdtemp(prefix='coherence_')
    try:
        for jeu, mesures, valeurs in jeux(config):
            try:
                motif = ev.Pattern(sm2d, mesures, valeurs)
                pcs = pieces(motif)
                for c in courbes:
                    angles[c['nom']] += [(a, ou, jeu) for a, ou in angles_courbe(pcs, c)]
                for c in coutures:
                    e, msgs = controler_couture(pcs, c, motif)
                    ecarts[c['nom']].append((e, jeu))
                    crans[c['nom']] += [f'{jeu} : {m}' for m in msgs]
                orphelins |= set(crans_orphelins(pcs, coutures))
            except Exception as e:  # formule ou outil que le calcul hors Seamly ne sait pas faire
                erreurs.append(f'{jeu} : {type(e).__name__} {e}')
                continue
            actuels = points(motif)
            nouvelles_refs[jeu] = actuels
            if jeu in refs:
                types = {}
                for el in motif.root.iter('point'):
                    if el.get('name'):
                        types[el.get('name')] = el.get('type')
                b, n = comparer_points(refs[jeu], actuels, types)
                deplaces += [f'{jeu} : {x}' for x in b]
                nouveaux |= set(n)
            if avec_seamly:
                res, err = contours_seamly(sm2d, mesures, valeurs, tmp)
                if err:
                    seamly.append(f'{jeu} : {err}')
                    continue
                for piece, p in pcs.items():
                    if piece not in res:
                        seamly.append(f'{jeu} : pièce {piece} absente de l\'export Seamly')
                        continue
                    xs, ys = [q[0] for q in p.pts], [q[1] for q in p.pts]
                    calc = (p.tour, max(xs) - min(xs), max(ys) - min(ys))
                    for lib, a, b in zip(('périmètre', 'largeur', 'hauteur'), calc, res[piece]):
                        ecart_seamly = max(ecart_seamly, abs(a - b))
                        if abs(a - b) > SEAMLY_MAX:
                            seamly.append(f'{jeu} : {piece}, {lib} {fr(a)} cm calculé, {fr(b)} cm dans Seamly')
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    rapport.titre(f'## {nom}')
    if erreurs:
        rapport.ko('Calcul du tracé impossible', erreurs)
    if avec_seamly:
        if seamly:
            rapport.ko('Le calcul hors Seamly ne trace pas comme Seamly', seamly)
        else:
            rapport.ok(f'Calcul hors Seamly identique à Seamly : {fr(ecart_seamly * 10, 1)} mm d\'écart au plus '
                       f'(périmètre et dimensions des pièces)')

    rapport.titre('**1. Courbes sans angle**')
    for c in courbes:
        pires = sorted(angles[c['nom']], key=lambda x: x[0], reverse=True)
        tol = c.get('angle_max', ANGLE_MAX)
        par_jeu = {}
        for a, ou, jeu in angles[c['nom']]:
            if a > tol:
                par_jeu.setdefault(jeu, []).append(f'{fr(a, 1)}° ({ou})')
        if par_jeu:
            rapport.ko(f'{c["nom"]} : coins au-delà de {fr(tol, 1)}°',
                       [f'{jeu} : {", ".join(m)}' for jeu, m in par_jeu.items()])
        elif pires:
            a, ou, jeu = pires[0]
            rapport.ok(f'{c["nom"]} : {fr(a, 1)}° au plus ({jeu}, {ou})')

    rapport.titre('**2. Points immobiles**')
    if maj:
        ecrire_references(chemin_ref, nouvelles_refs)
        rapport.ok(f'Références mises à jour : patrons/references/{nom}.json')
    elif not refs:
        rapport.ko(f'Pas de références : lancer avec --maj-references')
    elif deplaces:
        rapport.ko(f'{len(deplaces)} point(s) déplacé(s) ; si c\'est voulu, lancer avec --maj-references',
                   deplaces)
    else:
        rapport.ok('Aucun point déplacé' + (f' (nouveaux : {", ".join(sorted(nouveaux))})' if nouveaux else ''))
    absents = [j for j in nouvelles_refs if refs and j not in refs and not maj]
    if absents:
        rapport.ko('Jeux de mesures sans référence : lancer avec --maj-references', absents)

    rapport.titre('**3. Longueurs des coutures** (écart = b − a)')
    for c in coutures:
        bas, haut = c.get('ecart', ECART_COUTURE)
        es = ecarts[c['nom']]
        if not es:
            continue
        mauvais = [(e, j) for e, j in es if not bas <= e <= haut]
        plage = f'{fr(min(e for e, _ in es))} à {fr(max(e for e, _ in es))} cm'
        if mauvais:
            rapport.ko(f'{c["nom"]} : écart attendu de {fr(bas)} à {fr(haut)} cm, mesuré {plage}',
                       [f'{j} : {fr(e)} cm' for e, j in mauvais])
        else:
            rapport.ok(f'{c["nom"]} : {plage}')

    rapport.titre('**4. Crans**')
    for c in coutures:
        if crans[c['nom']]:
            rapport.ko(f'{c["nom"]} : crans qui ne se correspondent pas', crans[c['nom']])
        else:
            rapport.ok(f'{c["nom"]}')
    if orphelins:
        rapport.ko('Crans sans couture décrite dans le fichier .coherence.toml', sorted(orphelins))


def main():
    args = sys.argv[1:]
    maj, avec_seamly = '--maj-references' in args, '--seamly' in args
    noms = [a for a in args if not a.startswith('--')] or sorted(
        os.path.basename(f)[:-len('.coherence.toml')] for f in glob.glob(os.path.join(PATRONS, '*.coherence.toml')))
    rapport = Rapport()
    rapport.lignes.append('# Cohérence des tracés')
    for nom in noms:
        controler(nom, maj, avec_seamly, rapport)
    print('\n'.join(rapport.lignes))
    sys.exit(1 if rapport.echec else 0)


if __name__ == '__main__':
    main()
