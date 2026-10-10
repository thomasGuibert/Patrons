"""Essai : un patron tracé par Seamly2D Linux, sans écran, à partir de mesures quelconques.

Usage : python3 essai.py <seamly2d> <dossier de sortie>

Pour le bas de pyjama :
1. exporte en T44 et compare au SVG exporté par le Seamly Windows (export/seamly/) ;
2. exporte en taille 40 (fichier T40.smms écrit ici, puis --gsize 40 sur T44.smms) ;
3. exporte en sur-mesure (fichier individuel .vit écrit ici) ;
4. fait le PDF A4 de chaque variante.
Le résumé (Markdown) est écrit sur la sortie standard.
"""
import math, os, re, shutil, subprocess, sys, time
import xml.etree.ElementTree as ET

RACINE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
PATRON = 'bas_pyjama'
TITRE = 'Bas de pyjama'
PX_CM = 96 / 2.54
NS = '{http://www.w3.org/2000/svg}'
SUR_MESURE = {'waist_circ': 80, 'hip_circ': 98}


def mesures_t44():
    racine = ET.parse(os.path.join(RACINE, 'mesures', 'T44.smms')).getroot()
    return [(m.get('name'), float(m.get('base')), float(m.get('size_increase')))
            for m in racine.iter('m')]


def ecrire_taille(chemin, taille):
    """Copie de T44.smms où base = base + (taille - 44) / 2 * size_increase."""
    texte = open(os.path.join(RACINE, 'mesures', 'T44.smms'), encoding='utf-8').read()
    texte = texte.replace('<size base="44"/>', '<size base="%d"/>' % taille)
    def ligne(m):
        base, nom, inc = float(m.group(1)), m.group(2), float(m.group(3))
        return m.group(0).replace('base="%s"' % m.group(1),
                                  'base="%g"' % round(base + (taille - 44) / 2 * inc, 2), 1)
    texte = re.sub(r'<m base="([\d.]+)"[^>]*name="([^"]+)" size_increase="(-?[\d.]+)"/>', ligne, texte)
    open(chemin, 'w', encoding='utf-8').write(texte)


def ecrire_individuel(chemin, valeurs):
    """Fichier de mesures individuel (.vit) : T44 avec quelques valeurs remplacées."""
    lignes = ''.join('        <m name="%s" value="%g"/>\n' % (nom, valeurs.get(nom, base))
                     for nom, base, _ in mesures_t44())
    open(chemin, 'w', encoding='utf-8').write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<vit>\n    <version>0.3.3</version>\n'
        '    <read-only>false</read-only>\n    <notes/>\n    <unit>cm</unit>\n'
        '    <pm_system>998</pm_system>\n    <personal>\n        <family-name/>\n'
        '        <given-name/>\n        <birth-date>1800-01-01</birth-date>\n'
        '        <gender>unknown</gender>\n        <email/>\n    </personal>\n'
        '    <body-measurements>\n' + lignes + '    </body-measurements>\n</vit>\n')


def exporter(seamly, travail, nom, mesures, options=()):
    """Copie le patron en le reliant à `mesures`, exporte en SVG. -> (svg, durée, journal)."""
    dossier = os.path.join(travail, nom)
    os.makedirs(dossier, exist_ok=True)
    texte = open(os.path.join(RACINE, 'patrons', PATRON + '.sm2d'), encoding='utf-8').read()
    texte = re.sub(r'<measurements>[^<]*</measurements>',
                   '<measurements>%s</measurements>' % os.path.basename(mesures), texte)
    copie = os.path.join(dossier, nom + '.sm2d')
    open(copie, 'w', encoding='utf-8').write(texte)
    if os.path.dirname(os.path.abspath(mesures)) != dossier:
        shutil.copy(mesures, dossier)
    debut = time.time()
    r = subprocess.run([seamly, '-m', os.path.join(dossier, os.path.basename(mesures)), *options,
                        '-b', nom, '-d', dossier, '-f', '0', '--exportOnlyDetails', copie],
                       capture_output=True, text=True, errors='replace', timeout=300)
    duree = time.time() - debut
    journal = 'code %d\n%s' % (r.returncode, (r.stdout + r.stderr)[-3000:])
    svgs = [f for f in os.listdir(dossier) if f.endswith('.svg')]
    return (os.path.join(dossier, svgs[0]) if svgs else None), duree, journal, copie


def chemins(svg):
    """{pièce: [liste de nombres de chaque <path>, coordonnées locales à la pièce]}."""
    res = {}
    for g in ET.parse(svg).getroot().findall(NS + 'g'):
        res[g.get('id')] = [[float(x) for x in re.findall(r'-?[\d.]+(?:e[-+]?\d+)?', p.get('d'))]
                            for p in g.iter(NS + 'path')]
    return res


def largeur(svg, piece):
    nombres = chemins(svg)[piece][0]
    xs, ys = nombres[0::2], nombres[1::2]
    return (max(xs) - min(xs)) / PX_CM, (max(ys) - min(ys)) / PX_CM


def comparer(svg_a, svg_b):
    """Écart maximal (mm) entre les tracés de mêmes pièces, chemin par chemin."""
    a, b = chemins(svg_a), chemins(svg_b)
    lignes = []
    for piece in sorted(set(a) | set(b)):
        if piece not in a or piece not in b:
            lignes.append('| %s | absente d\'un côté | |' % piece)
            continue
        if len(a[piece]) != len(b[piece]) or any(len(x) != len(y) for x, y in zip(a[piece], b[piece])):
            lignes.append('| %s | structure différente (%d / %d chemins) | |' % (
                piece, len(a[piece]), len(b[piece])))
            continue
        ecart = max((abs(x - y) for pa, pb in zip(a[piece], b[piece]) for x, y in zip(pa, pb)),
                    default=0) / PX_CM * 10
        lignes.append('| %s | %d chemins | %.3f mm |' % (piece, len(a[piece]), ecart))
    return lignes


def main():
    seamly, sortie = sys.argv[1], os.path.abspath(sys.argv[2])
    os.makedirs(sortie, exist_ok=True)
    pdf = os.path.join(RACINE, '.claude', 'skills', 'tracer-sm2d', 'pdf_depuis_seamly.py')
    t44 = os.path.join(RACINE, 'mesures', 'T44.smms')
    t40 = os.path.join(sortie, 'T40.smms')
    perso = os.path.join(sortie, 'perso.vit')
    ecrire_taille(t40, 40)
    ecrire_individuel(perso, SUR_MESURE)
    variantes = [('T44', t44, ()), ('T40', t40, ()), ('T40-gsize', t44, ('--gsize', '40')),
                 ('sur-mesure', perso, ())]
    print('## Seamly2D Linux sans écran : %s\n' % PATRON)
    print('| Variante | Export | Durée | Ceinture (l × h) | PDF A4 |\n|---|---|---|---|---|')
    svgs, journaux = {}, []
    for nom, mesures, options in variantes:
        svg, duree, journal, copie = exporter(seamly, sortie, nom, mesures, options)
        journaux.append('### %s\n```\n%s\n```' % (nom, journal))
        if not svg:
            print('| %s | échec | %.1f s | | |' % (nom, duree))
            continue
        svgs[nom] = svg
        l, h = largeur(svg, 'Ceinture')
        sortie_pdf = os.path.join(sortie, '%s-%s.pdf' % (PATRON, nom))
        r = subprocess.run([sys.executable, pdf, svg, sortie_pdf, TITRE, copie],
                           capture_output=True, text=True)
        etat = r.stdout.strip() or ('échec : ' + r.stderr[-300:].replace('\n', ' '))
        print('| %s | OK | %.1f s | %.1f × %.1f cm | %s |' % (nom, duree, l, h, etat))
    windows = os.path.join(RACINE, 'export', 'seamly', PATRON + '_pieces.svg')
    if 'T44' in svgs:
        print('\n### T44 Linux comparé au Seamly Windows (export/seamly)\n')
        print('| Pièce | Chemins | Écart max |\n|---|---|---|')
        print('\n'.join(comparer(svgs['T44'], windows)))
    if 'T40' in svgs and 'T40-gsize' in svgs:
        print('\n### T40 par fichier comparé à T40 par --gsize\n')
        print('| Pièce | Chemins | Écart max |\n|---|---|---|')
        print('\n'.join(comparer(svgs['T40'], svgs['T40-gsize'])))
    print('\n## Journaux Seamly\n')
    print('\n'.join(journaux))
    if len(svgs) < len(variantes):
        sys.exit(1)


if __name__ == '__main__':
    main()
