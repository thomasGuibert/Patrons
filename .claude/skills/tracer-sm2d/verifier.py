"""Vérifie un patron Seamly2D par export en ligne de commande.

Usage : python verifier.py patrons/<fichier>.sm2d [--sortie <dossier>]

Exporte une copie du patron (le fichier peut rester ouvert dans Seamly) en SVG et en PNG,
signale les erreurs Seamly, puis affiche pour chaque pièce :
- largeur, hauteur et longueur de la ligne de couture (cm) ;
- ses sommets (angle du contour > 20°) avec leurs coordonnées (cm, origine en haut à gauche
  de la pièce, y vers le bas) et la longueur de couture cumulée depuis le premier sommet.
  La longueur d'une courbe entre deux sommets = différence des longueurs cumulées.
"""
import argparse, math, os, re, shutil, subprocess, sys, tempfile

SEAMLY = os.environ.get('SEAMLY2D', r'C:\Program Files (x86)\Seamly2D\seamly2d.exe')
PX_PAR_CM = 96 / 2.54
_N = r'(-?[\d.]+(?:e[-+]?\d+)?)'
NOMBRE_XY = r'[ML]\s*' + _N + ',' + _N


def exporter(sm2d, sortie):
    """Copie le patron et son fichier de mesures dans un dossier temporaire et exporte."""
    tmp = tempfile.mkdtemp(prefix='sm2d_')
    contenu = open(sm2d, encoding='utf-8').read()
    m = re.search(r'<measurements>([^<]+)</measurements>', contenu)
    dossier = os.path.join(tmp, 'patrons')
    os.makedirs(dossier)
    copie = os.path.join(dossier, os.path.basename(sm2d))
    shutil.copy(sm2d, copie)
    if m:
        src = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(sm2d)), m.group(1)))
        dst = os.path.normpath(os.path.join(dossier, m.group(1)))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(src, dst)
    nom = os.path.splitext(os.path.basename(sm2d))[0]
    erreurs = []
    for fmt in ('0', '3'):
        r = subprocess.run([SEAMLY, '-b', nom, '-d', sortie, '-f', fmt, '--exportOnlyDetails', copie],
                           capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=180)
        lignes = [l for l in (r.stdout + r.stderr).splitlines() if not l.startswith('INFO')]
        if r.returncode != 0 or any('CRITIQUE' in l or 'CRITICAL' in l for l in lignes):
            erreurs.append(f'export format {fmt} : code {r.returncode}\n' + '\n'.join(lignes))
    shutil.rmtree(tmp, ignore_errors=True)
    return nom, erreurs


def pieces(svg):
    texte = open(svg, encoding='utf-8').read()
    for m in re.finditer(r'<g [^>]*id="([^"]+)"', texte):
        suite = texte[m.end():]
        chemin = re.search(r'<path[^>]* d="([^"]+)"', suite)
        if not chemin:
            continue
        pts = []
        for x, y in re.findall(NOMBRE_XY, chemin.group(1)):
            p = (float(x) / PX_PAR_CM, float(y) / PX_PAR_CM)
            if not pts or math.dist(p, pts[-1]) > 1e-4:
                pts.append(p)
        if len(pts) > 1 and math.dist(pts[0], pts[-1]) < 1e-4:
            pts.pop()
        yield m.group(1), pts


def sommets(pts, seuil=20):
    n = len(pts)
    res = []
    for i in range(n):
        a, b, c = pts[i - 1], pts[i], pts[(i + 1) % n]
        v1 = (b[0] - a[0], b[1] - a[1]); v2 = (c[0] - b[0], c[1] - b[1])
        if math.hypot(*v1) < 1e-6 or math.hypot(*v2) < 1e-6:
            continue
        ang = math.degrees(abs(math.atan2(v1[0] * v2[1] - v1[1] * v2[0], v1[0] * v2[0] + v1[1] * v2[1])))
        if ang > seuil:
            res.append(i)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('sm2d')
    ap.add_argument('--sortie', default=os.path.join(tempfile.gettempdir(), 'verif_sm2d'))
    a = ap.parse_args()
    os.makedirs(a.sortie, exist_ok=True)
    nom, erreurs = exporter(a.sm2d, a.sortie)
    if erreurs:
        print('ERREUR SEAMLY\n' + '\n'.join(erreurs))
        sys.exit(1)
    print(f'Export OK : {os.path.join(a.sortie, nom + "_pieces.svg")} et .png')
    for piece, pts in pieces(os.path.join(a.sortie, nom + '_pieces.svg')):
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        x0, y0 = min(xs), min(ys)
        tour = sum(math.dist(pts[i], pts[(i + 1) % len(pts)]) for i in range(len(pts)))
        print(f'\n== {piece} : {max(xs) - x0:.2f} x {max(ys) - y0:.2f} cm, couture {tour:.2f} cm')
        idx = sommets(pts)
        cumul, i0 = 0.0, idx[0] if idx else 0
        ordre = list(range(i0, len(pts))) + list(range(0, i0))
        longueurs = {}
        for k, i in enumerate(ordre):
            longueurs[i] = cumul
            cumul += math.dist(pts[i], pts[ordre[(k + 1) % len(ordre)]])
        for i in idx:
            print(f'  sommet ({pts[i][0] - x0:7.2f}, {pts[i][1] - y0:7.2f})  cumul {longueurs[i]:7.2f}')


if __name__ == '__main__':
    main()
