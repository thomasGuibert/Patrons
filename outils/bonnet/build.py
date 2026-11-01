"""Génère patrons/bonnet_bain.sm2d (bonnet de bain en maille, cheveux longs : 2 côtés et une bande centrale).

Usage : python3 outils/bonnet/build.py [T40] [patrons/bonnet_bain.sm2d]
Taille unique (Thomas, 2026-10-29) : le tracé ne lit aucune mesure ; le fichier de mesures lié ne sert qu'à Seamly.
Étapes et choix : patrons/bonnet_bain.etapes.md (issue #83). Modèle d'Atelier AT, pas tiré du livre.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'bolero'))
from gen import Fichier

T = sys.argv[1] if len(sys.argv) > 1 else 'T40'
f = Fichier(f'../mesures/femme/{T}.smms')

# ---------------- variables (choix de modèle) ----------------
V = f.var
V('tour_tete', 56, "Taille unique : tour de tête moyen, le bonnet va de 52 à 60 cm grâce à la maille")
V('reduction', 0.875, "Maille de bain (élasthanne) : bord de 49 cm, 94 % d'une tête de 52 et 82 % d'une tête de 60")
V('larg_bande', 10, "Largeur de la bande centrale, du front à la nuque")
V('bas_cote', '(#tour_tete*#reduction-2*#larg_bande)/2', "Bas du côté : le tour du bord moins les deux bouts de bande, partagé entre les deux côtés")
V('haut_cote', '#tour_tete*0.19', "Hauteur du côté, du bord au sommet (couture de bande)")
V('volume', 4, "Cheveux longs : débord du côté en arrière de la nuque, pour loger les cheveux relevés")
V('haut_volume', '#haut_cote*0.45', "Hauteur du point de volume arrière au-dessus du bord")
V('pos_sommet', '#bas_cote*0.4', "Sommet du côté depuis le front, sur le bas")

b = f.bloc('Bonnet de bain')
N = dict(notch=True)

# ---- Côté
b.single('A', 0, 0, 'A : bord, côté front (tempe)')
b.end('B', 'A', 0, '#bas_cote', 'AB = bas du côté, bord du bonnet jusqu\'à la nuque', 'solidLine')
b.along('S0', 'A', 'B', '#pos_sommet', 'S0 sur AB, sous le sommet')
b.end('S', 'S0', 90, '#haut_cote', 'S : sommet du côté, au-dessus de S0')
b.end('R0', 'B', 0, '#volume', 'R0 : prolongement de AB en arrière de la nuque')
b.end('R', 'R0', 90, '#haut_volume', 'R : volume arrière pour les cheveux longs')
# devant du côté : part d'équerre du bord, arrive à l'horizontale au sommet
b.spl('cAvant', 'A', 'S', '90', '#haut_cote*0.55', '180', '#pos_sommet*0.6', 'courbe A–S, d\'équerre en A, horizontale en S')
# arrière : horizontale au sommet, verticale au volume, d'équerre sur le bord en B
b.chemin('cArriere', [('S', '0', '0', '(#bas_cote-#pos_sommet+#volume)*0.55'),
                      ('R', '270', '(#haut_cote-#haut_volume)*0.6', '#haut_volume*0.5'),
                      ('B', '270', '#haut_volume*0.6', '0')],
         'courbe S–R–B : horizontale en S, verticale en R, d\'équerre sur le bord en B')

# crans de montage : triangles vers l'extérieur au quart, à la moitié et aux trois quarts de la couture A–S–B
# (le cran S reste un petit trait : c'est le repère de construction du sommet)
LONG = '(Spl_A_S+SplPath_S_B)'
b.coupe('M1', 'cAvant', LONG + '/4', 'cran de montage M1 : au quart de la couture A–S–B depuis A', simple=True)
b.coupe('M2', 'cArriere', LONG + '/2-Spl_A_S', 'cran de montage M2 : à la moitié de la couture A–S–B depuis A')
b.coupe('M3', 'cArriere', LONG + '*3/4-Spl_A_S', 'cran de montage M3 : aux trois quarts de la couture A–S–B depuis A')
TRI = dict(notch=True, type='vExternal', long=0.5, larg=0.5)

COUTURE, BORD = 0.6, 1
ELASTIQUE = ('Élasticité : sens de la largeur',)
b.piece('Côté', [('p', 'A', dict(sa=(BORD, COUTURE))), ('c', 'cAvant', 0), ('p', 'M1', TRI), ('c', 'cAvant', 0),
                 ('p', 'S', dict(notch=True)),
                 ('cp', 'cArriere', 0), ('p', 'M2', TRI), ('cp', 'cArriere', 0), ('p', 'M3', TRI), ('cp', 'cArriere', 0),
                 ('p', 'B', dict(sa=(COUTURE, BORD)))],
        qte=2, couture=COUTURE,
        info=dict(data=(3.2, -8.4), pinfo=(3.2, -4.9), grain=(12.5, -1.2, 7), data_dim=(8, 3.3), pinfo_dim=(8, 3.3),
                  lignes=ELASTIQUE))

# ---- Bande centrale, au pli dans sa longueur (pli à droite) ; longueur = couture du côté (A–S–B)
b.single('bA', 28, -16, 'bA : bande, bout du front, sur le pli')
b.end('bB', 'bA', 270, LONG, 'bA bB = longueur de la couture du côté (A–S–B), au pli', 'dashLine')
b.end('bA2', 'bA', 180, '#larg_bande/2', 'bA bA2 = demi-largeur de bande (bord du front)', 'solidLine')
b.end('bB2', 'bB', 180, '#larg_bande/2', 'bB bB2 = demi-largeur de bande (bord de la nuque)', 'solidLine')
b.end('bS', 'bA2', 270, 'Spl_A_S', 'cran bS : sommet du côté, à la longueur de la courbe A–S depuis le front', 'none')
b.along('bM1', 'bA2', 'bB2', LONG + '/4', 'cran de montage bM1 : en face de M1')
b.along('bM2', 'bA2', 'bB2', LONG + '/2', 'cran de montage bM2 : en face de M2')
b.along('bM3', 'bA2', 'bB2', LONG + '*3/4', 'cran de montage bM3 : en face de M3')
b.ligne('bA2', 'bB2', 'solidLine')
# contour dans le sens des aiguilles d'une montre (couture à l'extérieur) : le pli est à droite
b.piece('Bande centrale', [('p', 'bA', dict(sa=(BORD, 0))), ('p', 'bB', dict(sa=(0, BORD))), ('p', 'bB2', dict(sa=(BORD, COUTURE))),
                           ('p', 'bM3', TRI), ('p', 'bM2', TRI), ('p', 'bS', N), ('p', 'bM1', TRI),
                           ('p', 'bA2', dict(sa=(COUTURE, BORD)))],
        qte=1, pli=True, couture=COUTURE,
        info=dict(data=(23.3, -12.5), pinfo=(23.3, -9.2), grain=(25.5, 13, 8), data_dim=(4.4, 4.4), pinfo_dim=(4.4, 4),
                  matiere='Tissu, au pli', lignes=('Élasticité :', 'largeur')))

# ---- Carré de contrôle 5 x 5 cm (imprimé sur la notice du PDF, à l'échelle 1)
c = f.bloc('Carré 5x5')
c.single('Z', 38, -4, 'Z : coin du carré de contrôle')
c.end('Z1', 'Z', 0, 5, 'ZZ1 = 5 cm', 'solidLine')
c.normal('Z2', 'Z1', 'Z', 5, 0, 'Z1Z2 = 5 cm, perpendiculaire à ZZ1', 'solidLine')
c.normal('Z3', 'Z2', 'Z1', 5, 0, 'Z2Z3 = 5 cm, perpendiculaire à Z1Z2', 'solidLine')
c.ligne('Z', 'Z3', 'solidLine')
c.piece('Carré 5x5', [('p', 'Z'), ('p', 'Z1'), ('p', 'Z2'), ('p', 'Z3')], couture=0,
        info=dict(nu=True, data=(38.2, -2.5), data_dim=(4.6, 1.5), matiere=''))

with open(sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'patrons', 'bonnet_bain.sm2d'), 'w') as out:
    out.write(f.xml('BONNET DE BAIN').replace('text="T%size%"', 'text="Taille unique"').replace('fil Bases chaîne et trame femme', 'issue #83, bonnet de bain'))
