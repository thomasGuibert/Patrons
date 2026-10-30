"""Génère patrons/poncho_bain.sm2d (poncho de bain en éponge : devant, dos, manches coude, capuche, poche kangourou).

Usage : python3 outils/poncho/build.py [T40] [patrons/poncho_bain.sm2d]
Tailles XS à XL = femme 36 à 44 ; trois longueurs (petit, normal, grand) tracées sur le devant et le dos.
Étapes et choix : patrons/poncho_bain.etapes.md (issue #89). Modèle d'Atelier AT, pas tiré du livre
ni des patrons du commerce joints à l'issue.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'bolero'))
from gen import Fichier

T = sys.argv[1] if len(sys.argv) > 1 else 'T40'
f = Fichier(f'../mesures/femme/{T}.smms')

# ---------------- variables (choix de modèle) ----------------
V = f.var
V('tour_max', '(bust_circ+hip_circ)/2+abs(hip_circ-bust_circ)/2', "Le plus fort des tours de poitrine et de hanches")
V('aisance', 64, "Aisance du poncho : de quoi se changer dessous, bras rentrés")
V('demi_larg', '(#tour_max+#aisance)/4', "Demi-largeur du devant (et du dos) en haut, au pli")
V('evase', 4, "Évasement du côté, du dessous de bras au bas")
V('pente', 3, "Pente d'épaule, de l'encolure au bord du devant")
V('larg_enc', 'neck_circ/6+2.5', "Demi-largeur d'encolure, élargie pour la capuche")
V('prof_enc_dev', 'neck_circ/6+4', "Profondeur d'encolure devant")
V('prof_enc_dos', 4.5, "Profondeur d'encolure dos")
V('emman', 'bust_circ/8+13.5', "Hauteur de l'emmanchure sur le côté : la demi-largeur de manche")
V('long_coude', 'arm_shoulder_tip_to_wrist*0.55', "Du bout d'épaule au coude")
V('long_manche', '#long_coude+2-(#demi_larg-#larg_enc-shoulder_length)', "Manche : du bord du devant au coude, le devant couvrant déjà le haut du bras")
V('resserre', 2, "La manche se resserre un peu au coude (sur la demi-largeur)")
V('long_genou', 'height_neck_back-height_waist_side+height_waist_side_to_knee', "De la nuque au genou")
V('long_petit', '#long_genou-22', "Longueur petit : mi-cuisse")
V('long_normal', '#long_genou-8', "Longueur normal : au-dessus du genou")
V('long_grand', '#long_genou+8', "Longueur grand : sous le genou")
V('ourlet', 3, "Ourlet du bas")
V('ouv_haut', 'neck_back_to_waist_b-4', "Haut de l'ouverture de côté, depuis l'épaule")
V('ouv_long', 24, "Longueur de l'ouverture de côté, pour passer les mains")
V('poche_y', 'neck_back_to_waist_b+1', "Haut de la poche kangourou, depuis l'épaule")
V('poche_h', 26, "Hauteur de la poche")
V('poche_demi', '#demi_larg*0.5', "Demi-largeur de la poche, en bas")
V('poche_haut_demi', '#poche_demi*0.6', "Demi-largeur du haut de la poche, entre les deux entrées de mains")
V('poche_ouv', 17, "Hauteur des entrées de mains, en biais")
V('haut_cap', 'height*0.21', "Hauteur de capuche, de l'encolure au sommet")
V('prof_cap', 'neck_circ*0.75', "Profondeur de capuche, du bord du visage à l'arrière de la tête")

COUTURE, OURLET, COULISSE, POCHE = 1, 3, 3.5, 2.5
N = dict(notch=True)
b = f.bloc('Poncho de bain')


def corps(s, x, prof_enc):
    """Devant ou dos, au pli : s = suffixe des points, x = abscisse du milieu, prof_enc = profondeur d'encolure."""
    O = b.single('O' + s, x, 0, f'O{s} : milieu, à hauteur d\'épaule (au pli)')
    Fn = b.end('Fn' + s, O, 270, prof_enc, 'milieu de l\'encolure', 'dashLine')
    E = b.end('E' + s, O, 0, '#larg_enc', 'encolure à l\'épaule')
    X = b.end('X' + s, O, 0, '#demi_larg', 'demi-largeur du haut')
    Ep = b.end('Ep' + s, X, 270, '#pente', 'bord d\'épaule, pente d\'épaule sous X')
    b.ligne(E, Ep, 'solidLine')
    Em = b.end('Em' + s, Ep, 270, '#emman', 'dessous de bras : bas de la couture de manche', 'solidLine')
    Hc = b.end('Hc' + s, Fn, 270, f'#long_grand-{prof_enc}', 'milieu du bas, longueur grand', 'dashLine')
    H = b.end('H' + s, Hc, 0, '#demi_larg+#evase', 'côté du bas, évasé', 'solidLine')
    b.ligne(Em, H, 'solidLine')
    Ou1 = b.along('Ou1' + s, Em, H, '#ouv_haut-#pente-#emman', 'cran : haut de l\'ouverture de côté')
    Ou2 = b.along('Ou2' + s, Em, H, '#ouv_haut-#pente-#emman+#ouv_long', 'cran : bas de l\'ouverture de côté')
    b.spl('cEnc' + s, Fn, E, '0', '#larg_enc*0.6', f'AngleLine_{E}_{Ep}-90', f'{prof_enc}*0.55',
          'encolure : horizontale au milieu, d\'équerre sur l\'épaule')
    coupes = []
    for lg in ('normal', 'petit'):
        c = b.end(f'C{lg[0]}{s}', Fn, 270, f'#long_{lg}+#ourlet-{prof_enc}', f'coupe {lg} au milieu (longueur + ourlet)')
        cs = b.axe(f'C{lg[0]}s{s}', c, 0, Em, H, f'coupe {lg} sur le côté')
        b.chemin_interne(f'coupe_{lg}{s}', [c, cs])
        coupes.append(f'coupe_{lg}{s}')
    noeuds = [('p', Fn, dict(sa=(0, COUTURE))), ('c', 'cEnc' + s, 0), ('p', E), ('p', Ep), ('p', Em, N),
              ('p', Ou1, N), ('p', Ou2, N), ('p', H, dict(sa=(COUTURE, OURLET))), ('p', Hc, dict(sa=(OURLET, 0)))]
    return noeuds, coupes


LONGUEURS = ('Bas : grand.', 'Traits : normal, petit.')

# ---- Devant, avec l'emplacement de la poche
noeuds, coupes = corps('', 0, '#prof_enc_dev')
b.end('Q0', 'O', 270, '#poche_y', 'poche : haut, au milieu')
b.end('Q1', 'Q0', 0, '#poche_haut_demi', 'poche : coin du haut')
b.end('Q2a', 'Q0', 270, '#poche_ouv', '')
b.end('Q2', 'Q2a', 0, '#poche_demi', 'poche : bas de l\'entrée de main')
b.end('Q4', 'Q0', 270, '#poche_h', 'poche : bas, au milieu')
b.end('Q3', 'Q4', 0, '#poche_demi', 'poche : coin du bas')
b.chemin_interne('place_poche', ['Q0', 'Q1', 'Q2', 'Q3', 'Q4'])
b.piece('Devant', noeuds, qte=1, pli=True, couture=COUTURE, chemins=['place_poche'] + coupes,
        info=dict(data=(4, 22), pinfo=(4, 30), grain=(30, 75, 30), data_dim=(16, 4.4), pinfo_dim=(14, 4),
                  matiere='Éponge, au pli', lignes=LONGUEURS))

# ---- Dos
noeuds, coupes = corps('d', 60, '#prof_enc_dos')
b.piece('Dos', noeuds, qte=1, pli=True, couture=COUTURE, chemins=coupes,
        info=dict(data=(64, 22), pinfo=(64, 30), grain=(90, 50, 30), data_dim=(16, 4.4), pinfo_dim=(14, 4),
                  matiere='Éponge, au pli', lignes=LONGUEURS))

# ---- Manche, au pli sur le dessus du bras ; son bord d'emmanchure = Ep Em du devant + du dos
b.single('mA', 120, 0, 'mA : haut de manche, sur le pli (cran d\'épaule)')
b.end('mB', 'mA', 0, '#emman', 'mA mB = hauteur d\'emmanchure', 'solidLine')
b.end('mC', 'mA', 270, '#long_manche', 'mA mC = longueur de manche, au pli', 'dashLine')
b.end('mD', 'mC', 0, '#emman-#resserre', 'bas de manche, un peu resserré', 'solidLine')
b.ligne('mB', 'mD', 'solidLine')
b.piece('Manche', [('p', 'mA', dict(sa=(0, COUTURE))), ('p', 'mB'), ('p', 'mD', dict(sa=(COUTURE, OURLET))),
                   ('p', 'mC', dict(sa=(OURLET, 0)))],
        qte=2, pli=True, couture=COUTURE,
        info=dict(data=(121.5, 2), pinfo=(121.5, 6.5), grain=(139, 8, 9), data_dim=(13, 3.2), pinfo_dim=(13, 4),
                  matiere='Éponge, au pli'))

# ---- Capuche, en deux moitiés ; son bas = encolure devant + dos
LONG = '(Spl_Fn_E+Spl_Fnd_Ed)'
b.single('cA', 160, 0, 'cA : bas du bord visage, au milieu devant')
b.end('cB', 'cA', 0, LONG, 'cA cB = demi-encolure (devant + dos), milieu dos en cB', 'solidLine')
b.end('cF', 'cA', 90, '#haut_cap', 'cA cF = bord visage, hauteur de capuche', 'solidLine')
b.end('cR0', 'cA', 0, '#prof_cap', '')
b.end('cR', 'cR0', 90, '#haut_cap*0.5', 'cR : arrière de la tête, profondeur de capuche')
b.along('cE', 'cA', 'cB', 'Spl_Fn_E', 'cran cE : couture d\'épaule, à la longueur de l\'encolure devant depuis cA')
b.chemin('cDos', [('cF', '0', '0', '#prof_cap*0.55'),
                  ('cR', '270', '#haut_cap*0.32', '#haut_cap*0.22'),
                  ('cB', '235', '(#prof_cap-' + LONG + ')*0.8+2', '0')],
         'milieu dos de capuche : horizontal au sommet, vertical à l\'arrière, rentrant vers la nuque')
b.piece('Capuche', [('p', 'cA', dict(sa=(COUTURE, COULISSE))), ('p', 'cF', dict(sa=(COULISSE, COUTURE))),
                    ('cp', 'cDos', 0), ('p', 'cB'), ('p', 'cE', N)],
        qte=2, couture=COUTURE,
        info=dict(data=(164, -27), pinfo=(164, -20.5), grain=(182, -18, 10), data_dim=(14, 3.2), pinfo_dim=(14, 4),
                  matiere='Éponge'))

# ---- Poche kangourou, au pli
b.single('pK0', 210, 0, 'pK0 : haut de poche, milieu (au pli)')
b.end('pK1', 'pK0', 0, '#poche_haut_demi', 'haut de poche, entre les entrées de main', 'solidLine')
b.end('pK4', 'pK0', 270, '#poche_h', 'bas de poche, au milieu', 'dashLine')
b.end('pK3', 'pK4', 0, '#poche_demi', 'coin du bas', 'solidLine')
b.end('pK2', 'pK3', 90, '#poche_h-#poche_ouv', 'bas de l\'entrée de main', 'solidLine')
b.ligne('pK1', 'pK2', 'solidLine')
b.piece('Poche', [('p', 'pK0', dict(sa=(0, COUTURE))), ('p', 'pK1', dict(sa=(COUTURE, POCHE))),
                            ('p', 'pK2', dict(sa=(POCHE, COUTURE))), ('p', 'pK3'), ('p', 'pK4', dict(sa=(COUTURE, 0)))],
        qte=1, pli=True, couture=COUTURE,
        info=dict(data=(211, 6), pinfo=(211, 11), grain=(219, 20.5, 8), data_dim=(12, 3.2), pinfo_dim=(12, 4),
                  matiere='Éponge, au pli'))

with open(sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'patrons', 'poncho_bain.sm2d'), 'w') as out:
    out.write(f.xml('PONCHO DE BAIN').replace('fil Bases chaîne et trame femme', 'issue #89, poncho de bain'))
