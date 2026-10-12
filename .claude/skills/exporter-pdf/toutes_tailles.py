"""Refait les PDF du site (A4 et A3) de chaque patron dans chaque taille de mesures/<gamme>/T*.smms.

Usage : python toutes_tailles.py [--gamme femme|homme] [patron ...]
        (sans patron : tous les patrons du site ; sans --gamme : les deux gammes)
Sortie : public/pdf/<gamme>/<slug>-<taille>.pdf et <slug>-<taille>-a3.pdf.
Seamly2D doit être installé (variable SEAMLY2D) ; sous Linux, lancer sous xvfb-run.
"""
import glob, os, re, shutil, subprocess, sys, tempfile

RACINE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
# patron .sm2d -> (slug du site, titre de la notice)
PATRONS = {
    'haut_pyjama': ('haut-pyjama', 'Haut de pyjama col V'),
    'bas_pyjama': ('bas-pyjama', 'Bas de pyjama'),
    'fond_pantalon_droit': ('fond-pantalon-droit', 'Fond de pantalon droit'),
    'fond_base_maille': ('fond-base-maille', 'Fond de base maille'),
}
GAMMES = ('femme', 'homme')


def main():
    args = sys.argv[1:]
    gammes = GAMMES
    if args[:1] == ['--gamme']:
        gammes, args = (args[1],), args[2:]
    noms = args or list(PATRONS)
    script = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mesures_vers_pdf.py')
    for gamme in gammes:
        tailles = sorted(int(re.search(r'T(\d+)\.smms$', f).group(1))
                         for f in glob.glob(os.path.join(RACINE, 'mesures', gamme, 'T*.smms')))
        sortie = os.path.join(RACINE, 'public', 'pdf', gamme)
        os.makedirs(sortie, exist_ok=True)
        for nom in noms:
            slug, titre = PATRONS[nom]
            for t in tailles:
                tmp = tempfile.mkdtemp(prefix='tailles_')
                try:
                    subprocess.run([sys.executable, script, os.path.join(RACINE, 'patrons', nom + '.sm2d'), tmp, f'{titre} ({gamme})',
                                    '--mesures', os.path.join(RACINE, 'mesures', gamme, f'T{t}.smms'), '--a3'],
                                   check=True)
                    for suffixe in ('', '-a3'):
                        shutil.move(os.path.join(tmp, f'{nom}-{t}{suffixe}.pdf'),
                                    os.path.join(sortie, f'{slug}-{t}{suffixe}.pdf'))
                finally:
                    shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    main()
