"""Des mesures au PDF imprimable, sans intervention : Seamly exporte les pièces avec les mesures
voulues (ligne de commande, aucune fenêtre), puis pdf_depuis_seamly.py les met en feuilles.
À lancer sur le PC (Seamly2D installé).

Usage : python mesures_vers_pdf.py patrons/<nom>.sm2d <dossier_sortie> "<Titre>" [mesures] [--a3]

Mesures (sans option : celles liées au .sm2d, ex. T44) :
  --taille 40               taille standard du fichier multitaille lié (tailles paires 22 à 72)
  --mesure waist_circ=80    sur-mesure : valeurs du fichier lié (à --taille si donnée) dont
                            certaines remplacées ; répétable. Noms : ceux du .smms (waist_circ…)
  --mesures <fichier>       fichier de mesures existant (.vit individuel SeamlyMe ou .smms)

Sortie : <dossier_sortie>/<nom>-<taille|sur-mesure>.pdf (A4), et -a3.pdf avec --a3.
Le .sm2d n'est pas modifié : Seamly travaille sur une copie.
"""
import argparse, os, re, shutil, subprocess, sys, tempfile, time

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ICI, '..', 'tracer-sm2d'))
from pdf_depuis_seamly import exporter as en_pdf  # noqa: E402

SEAMLY = os.environ.get('SEAMLY2D', r'C:\Program Files (x86)\Seamly2D\seamly2d.exe')
M_SMMS = re.compile(r'<m base="([-\d.]+)" height_increase="[-\d.]+" name="([^"]+)" size_increase="([-\d.]+)"')


def mesures_liees(sm2d):
    m = re.search(r'<measurements>([^<]+)</measurements>', open(sm2d, encoding='utf-8').read())
    if not m:
        sys.exit(f'{sm2d} : aucun fichier de mesures lié')
    return os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(sm2d)), m.group(1)))


def ecrire_vit(smms, taille, valeurs, dst):
    """Fichier individuel SeamlyMe : chaque mesure du multitaille à la taille voulue, puis remplacée."""
    txt = open(smms, encoding='utf-8').read()
    base = int(re.search(r'<size base="(\d+)"', txt).group(1))
    taille = taille or base
    connues = {}
    for b, nom, inc in M_SMMS.findall(txt):
        if nom not in ('size', 'height'):
            connues[nom] = round(float(b) + (taille - base) / 2 * float(inc), 3)
    inconnues = set(valeurs) - set(connues)
    if inconnues:
        sys.exit('mesures inconnues : %s\nconnues : %s' % (', '.join(sorted(inconnues)), ', '.join(connues)))
    connues.update(valeurs)
    lignes = '\n'.join(f'        <m name="{n}" value="{v:g}"/>' for n, v in connues.items())
    open(dst, 'w', encoding='utf-8').write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<vit>\n    <version>0.3.3</version>\n'
        '    <read-only>false</read-only>\n    <notes/>\n    <unit>cm</unit>\n    <pm_system>998</pm_system>\n'
        '    <personal>\n        <family-name/>\n        <given-name/>\n        <birth-date>1800-01-01</birth-date>\n'
        '        <gender>unknown</gender>\n        <email/>\n    </personal>\n'
        f'    <body-measurements>\n{lignes}\n    </body-measurements>\n</vit>\n')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('sm2d'); ap.add_argument('sortie'); ap.add_argument('titre')
    ap.add_argument('--taille', type=int)
    ap.add_argument('--mesure', action='append', default=[], metavar='NOM=VALEUR')
    ap.add_argument('--mesures', metavar='FICHIER')
    ap.add_argument('--a3', action='store_true')
    a = ap.parse_args()
    if a.mesures and (a.taille or a.mesure):
        ap.error('--mesures ne se combine pas avec --taille ni --mesure')
    if a.taille and not (a.taille % 2 == 0 and 22 <= a.taille <= 72):
        ap.error('--taille : taille paire de 22 à 72')

    nom = os.path.splitext(os.path.basename(a.sm2d))[0]
    tmp = tempfile.mkdtemp(prefix='mesures_pdf_')
    try:
        # copie du patron et de ses mesures liées (même chemin relatif) : le .sm2d peut rester ouvert
        copie = os.path.join(tmp, 'patrons', nom + '.sm2d')
        os.makedirs(os.path.dirname(copie))
        shutil.copy(a.sm2d, copie)
        liees = mesures_liees(a.sm2d)
        dst = os.path.normpath(os.path.join(os.path.dirname(copie), os.path.relpath(liees, os.path.dirname(os.path.abspath(a.sm2d)))))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(liees, dst)

        if a.mesure:
            valeurs = {}
            for kv in a.mesure:
                k, _, v = kv.partition('=')
                valeurs[k.strip()] = float(v.replace(',', '.'))
            vit = os.path.join(tmp, 'sur_mesure.vit')
            ecrire_vit(liees, a.taille, valeurs, vit)
            opts, libelle = ['-m', vit], 'sur-mesure'
        elif a.mesures:
            fichier = os.path.abspath(a.mesures)
            opts = ['-m', fichier]
            t = re.search(r'<size base="(\d+)"', open(fichier, encoding='utf-8').read())
            libelle = t.group(1) if fichier.endswith('.smms') and t else 'sur-mesure'
        elif a.taille:
            opts, libelle = ['--gsize', str(a.taille)], str(a.taille)
        else:
            opts, libelle = [], re.sub(r'\D', '', os.path.basename(liees))

        svgs = os.path.join(tmp, 'svg')
        debut = time.time()
        r = subprocess.run([SEAMLY, '-b', nom, '-d', svgs, '-f', '0', '--exportOnlyDetails', *opts, copie],
                           capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=180)
        svg = os.path.join(svgs, nom + '_pieces.svg')
        messages = [l for l in (r.stdout + r.stderr).splitlines() if not l.startswith('INFO')]
        if r.returncode != 0 or not os.path.exists(svg):
            sys.exit(f'export Seamly en échec (code {r.returncode}) :\n' + '\n'.join(messages))
        print(f'export Seamly : {time.time() - debut:.1f} s')

        os.makedirs(a.sortie, exist_ok=True)
        base = os.path.join(a.sortie, f'{nom}-{libelle}')
        for fmt, chemin in [('A4', base + '.pdf')] + ([('A3', base + '-a3.pdf')] if a.a3 else []):
            n = en_pdf(svg, chemin, a.titre, copie, fmt, libelle)
            print(f'{chemin} : {n} pages')
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    main()
