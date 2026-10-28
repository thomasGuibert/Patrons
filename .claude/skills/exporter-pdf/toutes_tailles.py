"""Refait les PDF du site (A4 et A3) de chaque patron dans chaque taille de mesures/<gamme>/T*.smms.

Usage : python toutes_tailles.py [--gamme femme|homme] [--dossiers-seuls] [patron ...]
        (sans patron : tous les patrons du site ; sans --gamme : les deux gammes)
Sortie : public/pdf/<gamme>/<slug>-<taille>.pdf et <slug>-<taille>-a3.pdf ; pour les patrons qui ont
un patrons/<nom>.dossier.toml, le dossier technique seul dans ses deux versions :
public/pdf/<gamme>/dossier/<slug>-<taille>-pro.pdf et -amateur.pdf (le site le joint au patron).
--dossiers-seuls : ne refait que les dossiers.
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
    'bolero': ('bolero', 'Boléro'),
}
GAMMES = ('femme', 'homme')


def main():
    args = sys.argv[1:]
    gammes = GAMMES
    seuls = '--dossiers-seuls' in args
    args = [x for x in args if x != '--dossiers-seuls']
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
            dossier = os.path.exists(os.path.join(RACINE, 'patrons', nom + '.dossier.toml'))
            if seuls and not dossier:
                continue
            for t in tailles:
                tmp = tempfile.mkdtemp(prefix='tailles_')
                try:
                    subprocess.run([sys.executable, script, os.path.join(RACINE, 'patrons', nom + '.sm2d'), tmp, f'{titre} ({gamme})',
                                    '--mesures', os.path.join(RACINE, 'mesures', gamme, f'T{t}.smms'), '--a3']
                                   + (['--dossiers', os.path.join(tmp, 'dossier')] if dossier else []),
                                   check=True)
                    if dossier:
                        os.makedirs(os.path.join(sortie, 'dossier'), exist_ok=True)
                        for montage in ('pro', 'amateur'):
                            shutil.move(os.path.join(tmp, 'dossier', f'{nom}-{t}-{montage}.pdf'),
                                        os.path.join(sortie, 'dossier', f'{slug}-{t}-{montage}.pdf'))
                    for suffixe in () if seuls else ('', '-a3'):
                        shutil.move(os.path.join(tmp, f'{nom}-{t}{suffixe}.pdf'),
                                    os.path.join(sortie, f'{slug}-{t}{suffixe}.pdf'))
                finally:
                    shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    main()
