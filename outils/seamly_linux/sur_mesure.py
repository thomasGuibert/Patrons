"""PDF sur mesure demandé depuis le site : vérifie la demande, puis lance mesures_vers_pdf.py.

Usage : python3 sur_mesure.py <dossier de sortie>
La demande arrive par les variables d'environnement (jamais par le shell) :
  PATRON  slug du site (haut-pyjama…)   FORMAT  a4 ou a3
  MESURES JSON {nom de mesure Seamly: cm}
Sortie : <dossier>/patron.pdf. Seamly : variable SEAMLY2D, sous xvfb-run.
"""
import json, os, re, shutil, subprocess, sys, tempfile

RACINE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SKILL = os.path.join(RACINE, '.claude', 'skills', 'exporter-pdf')
sys.path.insert(0, SKILL)
from toutes_tailles import PATRONS  # noqa: E402

# taille dont viennent les mesures que le site ne demande pas
TAILLE_DE_DEPART = 40


def main():
    sortie = sys.argv[1]
    slug, fmt = os.environ.get('PATRON', ''), os.environ.get('FORMAT', '')
    noms = {s: (nom, titre) for nom, (s, titre) in PATRONS.items()}
    if slug not in noms:
        sys.exit(f'patron inconnu : {slug!r}')
    if fmt not in ('a4', 'a3'):
        sys.exit(f'format inconnu : {fmt!r}')
    connues = set(re.findall(r'name="([a-z_]+)"', open(os.path.join(RACINE, 'mesures', 'T40.smms'), encoding='utf-8').read()))
    try:
        mesures = json.loads(os.environ.get('MESURES', ''))
    except ValueError:
        sys.exit('mesures illisibles')
    if not isinstance(mesures, dict) or not mesures:
        sys.exit('aucune mesure')
    args = []
    for n, v in mesures.items():
        if n not in connues or n in ('size', 'height'):
            sys.exit(f'mesure inconnue : {n!r}')
        if not isinstance(v, (int, float)) or not 1 <= v <= 250:
            sys.exit(f'{n} : valeur hors bornes')
        args += ['--mesure', f'{n}={v:g}']

    nom, titre = noms[slug]
    tmp = tempfile.mkdtemp(prefix='sur_mesure_')
    try:
        subprocess.run([sys.executable, os.path.join(SKILL, 'mesures_vers_pdf.py'),
                        os.path.join(RACINE, 'patrons', nom + '.sm2d'), tmp, titre,
                        '--taille', str(TAILLE_DE_DEPART), *args] + (['--a3'] if fmt == 'a3' else []), check=True)
        os.makedirs(sortie, exist_ok=True)
        shutil.move(os.path.join(tmp, f'{nom}-sur-mesure{"-a3" if fmt == "a3" else ""}.pdf'),
                    os.path.join(sortie, 'patron.pdf'))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    main()
