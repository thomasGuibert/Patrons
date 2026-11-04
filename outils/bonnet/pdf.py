"""PDF du bonnet de bain (taille unique) : comme pdf_depuis_seamly.py, mais la flèche des pièces
indique l'élasticité de la maille (issue #103) et non le droit-fil : la légende devient « Élasticité ».

Usage : python3 outils/bonnet/pdf.py <bonnet_bain_pieces.svg> [dossier de sortie]
"""
import os, sys
RACINE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
sys.path.insert(0, os.path.join(RACINE, '.claude', 'skills', 'tracer-sm2d'))
import pdf_depuis_seamly as p

class Toile:
    def __init__(self, c): self._c = c
    def __getattr__(self, n): return getattr(self._c, n)
    def drawCentredString(self, x, y, t, *a, **k):
        return self._c.drawCentredString(x, y, 'Élasticité' if t == 'Droit fil' else t, *a, **k)

dessiner = p.dessiner
p.dessiner = lambda c, *a, **k: dessiner(Toile(c), *a, **k)

svg = sys.argv[1]
sortie = sys.argv[2] if len(sys.argv) > 2 else os.path.join(RACINE, 'public', 'pdf', 'femme')
sm2d = os.path.join(RACINE, 'patrons', 'bonnet_bain.sm2d')
for suffixe, fmt in (('', 'A4'), ('-a3', 'A3')):
    dst = os.path.join(sortie, f'bonnet-bain-unique{suffixe}.pdf')
    print(dst, p.exporter(svg, dst, 'Bonnet de bain', sm2d, fmt, 'unique'), 'pages')
