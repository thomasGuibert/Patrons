"""Génère patrons/bolero.sm2d (base du mannequin, fond tailleur, manche tailleur, boléro).

Usage : python3 outils/bolero/build.py [T38] [patrons/bolero.sm2d]
Étapes et choix : patrons/bolero.etapes.md.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen import Fichier, ETAPES

T = sys.argv[1] if len(sys.argv) > 1 else 'T38'
f = Fichier(f'../mesures/femme/{T}.smms')

# ---------------- variables (valeurs du livre) ----------------
V = f.var
V('constr_hanches', 3, "Aisance de construction sur 1/2 tour de hanches (AB), livre p. 62")
V('petites_hanches', 9, "Ligne de petites hanches sous la taille (EG), livre p. 62")
V('pince_dos1', 1, "1re pince dos, milieu dos (tableau des pinces, p. 64)")
V('pince_dos2', 3, "2e pince dos (p. 64)")
V('pince_dos3', 1, "3e pince dos (p. 64)")
V('pince_dev1', 3, "1re pince devant (p. 64)")
V('pince_dev2', 2, "2e pince devant (p. 64)")
V('pinces', '#pince_dos1+#pince_dos2+#pince_dos3+#pince_dev1+#pince_dev2', "Total des pinces de taille (10 cm)")
V('pince_omoplate', 1, "Pince d'omoplate (exemple D2L3 = 12 + 1, p. 64)")
V('remonte_L4', 0.5, "L4 remonté au-dessus de la ligne d'épaule (annotation du tome 1, confirmée par Thomas)")
V('pos_pince_dos', 8.5, "Centre Q de la 2e pince dos depuis F1 (p. 66)")
V('long_pince_omoplate', 7, "Longueur de la pince d'omoplate D3Z (p. 66)")
V('pointe_dos', 9, "V1 au-dessus de la ligne de grandes hanches (p. 66)")
V('pointe_dev', 6, "e au-dessus de la ligne de grandes hanches (p. 68)")
V('remonte_P', 2, "P3 : pointe de la pince de poitrine, 2 cm au-dessus de P (p. 68)")
V('descente_E4', 2, "E4 : pointe de la 1re pince devant, 2 cm sous P (p. 68)")
V('plat_emm_dev', 2, "Platitude du dessous d'emmanchure devant (p. 68)")
V('plat_emm_dos', 1, "Platitude du dessous d'emmanchure dos (p. 68)")
V('plat_enc_dos', 2, "Platitude de l'encolure au milieu dos (p. 68)")
V('plat_enc_dev', 1, "Platitude de l'encolure au milieu devant (p. 68)")
# fond tailleur près du corps (p. 78)
V('t_enc_dev', 2, "Fond tailleur : milieu devant descendu (p. 78)")
V('t_enc_dos', 0.1, "Fond tailleur : milieu dos descendu (p. 78)")
V('t_ouv_epaule', 0.6, "Fond tailleur : encolure ouverte sur l'épaule (p. 78)")
V('t_allong_epaule', 0.5, "Fond tailleur : longueur d'épaule allongée (p. 78)")
V('t_carrure_dev', 0.5, "Fond tailleur : carrure devant (p. 78)")
V('t_carrure_dos', 1, "Fond tailleur : carrure dos (p. 78)")
V('t_dessous_bras', 2, "Fond tailleur : dessous de bras élargi (p. 78)")
V('t_descente_bras', 1.75, "Fond tailleur : dessous de bras descendu (p. 78)")
V('t_taille', 1.25, "Fond tailleur : taille élargie (p. 78)")
V('t_hanches', 1.5, "Fond tailleur : hanches élargies (p. 78)")
# manche tailleur (T2 p. 150-153)
V('epaulette', 0, "Hauteur d'épaulette : boléro sans épaulette (Thomas, 2026-10-27)")
V('long_manche', 'arm_shoulder_tip_to_wrist', "Longueur de manche (tableau ligne 15)")
V('haut_coude', 35, "Hauteur de coude AD (livre : 35 cm ; tableau ligne 17)")
V('bas_manche', 24, "Largeur du bas de manche (exemple du livre : 24 cm)")
V('m_JK', 0.5, "JK = J'K' : 0,5 cm, à régler selon l'embu (livre p. 150)")
V('m_HL', 5, "HL : 5 cm, à régler (livre p. 150)")
V('m_IT', 1.25, "IT : 1 à 1,5 cm (livre), milieu de la fourchette")
# boléro (choix de modèle, pas du livre)
V('bolero_sous_bras', 9, "Boléro : longueur sous le dessous de bras du fond tailleur (choix de modèle, ~8-10 cm)")
V('col_hauteur', 3, "Col officier : hauteur AD (exemple du livre, tome 1)")
V('bolero_arrondi', 6, "Boléro : rayon de l'arrondi du bas devant (choix de modèle)")

b = f.bloc('Corsage : base, fond tailleur, boléro')
P = 'p. 62'
# ---- Figure 1 : cadre
b.single('A', 0, 0, 'p. 62 : axe XY, A milieu dos')
b.end('B', 'A', 0, 'hip_circ/2+#constr_hanches', 'p. 62 : AB = 1/2 tour de hanches + 3', 'solidLine')
b.end('F', 'A', 90, 'height_waist_side_to_hip', 'p. 62 : hauteur taille-hanches (22)', 'dashLine')
b.end('E', 'B', 90, 'height_waist_side_to_hip', 'p. 62 : BE = hauteur taille-hanches', 'dashLine')
b.ligne('F', 'E', 'solidLine')
b.end('C', 'E', 90, 'neck_front_to_waist_f', 'p. 62 : longueur taille devant', 'dashLine')
b.end('D', 'F', 90, 'neck_back_to_waist_b', 'p. 62 : longueur taille dos', 'dashLine')
b.end('G', 'E', 270, '#petites_hanches', 'p. 62 : G à 9 cm sous E', 'dashLine')
b.end('H', 'F', 270, '#petites_hanches', 'p. 62 : petites hanches')
b.ligne('H', 'G', 'dashLine')
b.end('E1', 'E', 180, 'bustpoint_to_bustpoint_half', 'p. 62 : EE1 = 1/2 écart de poitrine')
b.end('I', 'C', 270, 'sqrt(bustpoint_to_neck_front^2-bustpoint_to_bustpoint_half^2)',
      'p. 62 : CP = hauteur de poitrine sur la parallèle au milieu par E1 ; I = ligne de poitrine sur le milieu devant')
b.end('P', 'I', 180, 'bustpoint_to_bustpoint_half', 'p. 62 : P, point de poitrine')
b.axe('J', 'I', 180, 'A', 'D', 'p. 62 : ligne de poitrine IJ', 'dashLine')
b.ligne('D', 'J')
b.along('L', 'D', 'J', 'Line_D_J/2', 'p. 62 : L = 1/2 DJ')
b.axe('K', 'L', 0, 'E', 'C', 'p. 62 : ligne de carrure', 'dashLine')
b.end('A1', 'A', 0, 'hip_circ/4-1', 'p. 62 : AA1 = 1/4 hanches − 1')
b.end('B1', 'B', 180, 'hip_circ/4+1', 'p. 62 : BB1 = 1/4 hanches + 1')
b.end('J1', 'J', 0, 'bust_circ/4', 'p. 62 : JJ1 = 1/4 poitrine')
b.end('I1', 'I', 180, 'bust_circ/4+2', 'p. 62 : II1 = 1/4 poitrine + 2')
b.ligne('A1', 'J1', 'dotLine'); b.ligne('B1', 'I1', 'dotLine')
# ---- encolure et épaule devant
b.end('C1', 'C', 180, 'neck_circ/2/3+0.5', 'p. 64 : CC1 = 1/3 de 1/2 encolure + 0,5')
b.end('C2', 'C1', 90, 'Line_C_C1', 'p. 64 : C1C2 = CC1')
b.along('C3', 'C1', 'C2', 'Line_C1_C2/2', 'p. 64 : C1C3 = 1/2 C1C2')
b.end('C3h', 'C3', 180, 20, 'p. 64 : perpendiculaire à C1C2 sur 20 cm', 'dotLine')
b.contact('C4', 'C2', 'C3h', 'C3', 'shoulder_length', 'p. 64 : longueur d\'épaule depuis C2')
# ---- encolure et épaule dos
b.end('D1', 'D', 0, '(neck_circ/2/3)*7/6', 'p. 64 : DD1 = 1/3 de 1/2 encolure + son 1/6')
b.end('D2', 'D1', 90, 'Line_D_D1/3', 'p. 64 : D1D2 = 1/3 DD1')
b.end('L1', 'L', 0, 'across_back_b/2', 'p. 64 : LL1 = 1/2 carrure dos')
b.end('L2', 'L1', 90, 'Line_D_D1+3', 'p. 64 : L1L2 = DD1 + 3', 'dotLine')
b.end('L2h', 'L2', 0, 8, 'p. 64 : perpendiculaire en L2', 'dotLine')
b.contact('L3', 'D2', 'L2h', 'L2', 'shoulder_length+#pince_omoplate', 'p. 64 : D2L3 = épaule + pince d\'omoplate')
# ---- Figure 2 : côtés
b.inter('N1', 'A1', 'J1', 'F', 'E', 'figure p. 67 : N1 = côté dos ∩ taille')
b.inter('N2', 'B1', 'I1', 'F', 'E', 'figure p. 67 : N2 = côté devant ∩ taille')
b.ligne('F', 'N1'); b.ligne('N2', 'E')
GALBE = '(Line_F_N1+Line_N2_E-waist_circ/2-#pinces)/2'
b.end('M1', 'N1', 180, GALBE, 'p. 64 : M1N1 = (excédent − pinces)/2')
b.end('M2', 'N2', 0, GALBE, 'p. 64 : N2M2 = (excédent − pinces)/2')
b.along('J2', 'M1', 'J1', '(neck_back_to_waist_b+neck_front_to_waist_f)/4+2',
        'p. 68 : M1J2 = (long. taille dos + devant)/4 + 2', 'solidLine')
b.along('I2', 'M2', 'I1', '(neck_back_to_waist_b+neck_front_to_waist_f)/4+2', 'p. 68 : M2I2 = M1J2', 'solidLine')
HT = 'height_waist_side_to_hip/3'
b.spl('cHdos', 'A1', 'M1', '90', HT, 'AngleLine_M1_J2+180', HT, 'p. 64 : joindre A1M1 en courbe')
b.spl('cHdev', 'B1', 'M2', '90', HT, 'AngleLine_M2_I2+180', HT, 'p. 64 : B1M2, courbe identique')
# ---- pinces dos
b.end('F1', 'F', 0, '#pince_dos1', 'p. 66 : pince milieu dos, F1')
b.ligne('L', 'F1', 'solidLine'); b.ligne('F1', 'A', 'solidLine')
b.along('D3', 'D2', 'L3', 'shoulder_length/2', 'p. 66 : D2D3 = 1/2 épaule')
b.along('L4b', 'L3', 'D2', 'shoulder_length/2', 'p. 66 : L3L4 = 1/2 épaule')
b.normal('L4', 'L4b', 'L3', '#remonte_L4', '0', 'annotation T1 : L4 remonté de 0,5')
b.end('Q', 'F1', 0, '#pos_pince_dos', 'p. 66 : Q à 8,5 cm de F1')
b.end('Q1', 'Q', 180, '#pince_dos2/2', 'p. 66 : Q1')
b.end('Q2', 'Q', 0, '#pince_dos2/2', 'p. 66 : Q2')
b.ligne('Q1', 'D3', 'dotLine')
b.inter('U', 'Q1', 'D3', 'L', 'K', 'figure p. 69 : U = Q1D3 ∩ carrure')
b.inter('Tp', 'Q1', 'D3', 'J', 'I', 'figure p. 69 : T = Q1D3 ∩ poitrine')
b.along('Z', 'D3', 'Q1', '#long_pince_omoplate', 'p. 66 : D3Z = 7')
b.ligne('U', 'Tp')
b.along('V', 'U', 'Tp', 'Line_U_Tp/4', 'p. 66 : UV = 1/4 UT')
b.axe('Qh', 'Q', 270, 'A', 'B', 'p. 66 : parallèle au milieu dos par Q', 'dotLine')
b.end('V1', 'Qh', 90, '#pointe_dos', 'p. 66 : V1 à 9 cm au-dessus des hanches')
b.ligne('Q2', 'M1')
b.along('S', 'Q2', 'M1', 'Line_Q2_M1/2', 'p. 66 : S au milieu de Q2M1')
b.end('S1', 'S', 180, '#pince_dos3/2', 'p. 66 : 3e pince dos')
b.end('S2', 'S', 0, '#pince_dos3/2', 'p. 66 : 3e pince dos')
b.axe('Sh', 'S', 90, 'J', 'I', 'p. 66 : jusqu\'à la ligne de poitrine')
b.axe('Sb', 'S', 270, 'H', 'G', 'p. 66 : jusqu\'aux petites hanches')
# ---- pince de poitrine
b.along('P1', 'C2', 'C4', 'shoulder_length/2', 'p. 68 : C2P1 = 1/2 épaule')
b.end('P3', 'P', 90, '#remonte_P', 'p. 68 : P3 = P remonté de 2')
b.ligne('P3', 'P1', 'solidLine')
b.cercles('P2', 'P3', 'Line_P3_P1', 'P1', 'bust_circ/12', '2', 'p. 68 : P1P2 = 1/12 tour de poitrine (branches égales)')
b.ligne('P3', 'P2', 'solidLine')
b.end('K1c', 'K', 180, 'across_chest_f/2', 'p. 68 : pince fermée, KK1 = 1/2 carrure devant')
ROT = 'AngleLine_P3_P2-AngleLine_P3_P1'
b.rotation('P3', ROT, ['C4', 'K1c'], 'o')   # C4o = C5, K1co = K1 (pince rouverte)
b.along('C5', 'P2', 'C4o', 'Line_C2_P1', 'p. 68 : P2C5 = C2P1 (pince rouverte)', 'solidLine')
b.along('K1', 'K1co', 'P3', '0', 'p. 68 : K1 (pince rouverte)')
# ---- pinces de taille devant
b.end('E2', 'E1', 180, '#pince_dev1/2', 'p. 68 : 1re pince devant')
b.end('E3', 'E1', 0, '#pince_dev1/2', 'p. 68 : 1re pince devant')
b.end('E4', 'P', 270, '#descente_E4', 'p. 68 : E4 = P descendu de 2')
b.axe('E1h', 'E1', 270, 'A', 'B', 'p. 68 : parallèle au milieu devant par E1', 'dotLine')
b.end('e', 'E1h', 90, '#pointe_dev', 'p. 68 : e à 6 cm au-dessus des hanches')
b.ligne('M2', 'E2')
b.along('t', 'M2', 'E2', 'Line_M2_E2/2', 'p. 68 : t au milieu de M2E2')
b.end('t1', 't', 180, '#pince_dev2/2', 'p. 68 : 2e pince devant')
b.end('t2', 't', 0, '#pince_dev2/2', 'p. 68 : 2e pince devant')
b.axe('th', 't', 90, 'J', 'I', 'p. 68 : jusqu\'à la ligne de poitrine')
b.axe('tb', 't', 270, 'H', 'G', 'p. 68 : jusqu\'aux petites hanches')

# ---- emmanchures et encolures de la base
b.ligne('D2', 'D3', 'solidLine'); b.ligne('L4', 'L3', 'solidLine'); b.ligne('D3', 'Z', 'solidLine'); b.ligne('Z', 'L4', 'solidLine')
b.end('J2p', 'J2', 'AngleLine_M1_J2+90', '#plat_emm_dos', 'p. 68 : platitude 1 cm en J2', 'solidLine')
b.end('I2p', 'I2', 'AngleLine_M2_I2-90', '#plat_emm_dev', 'p. 68 : platitude 2 cm en I2', 'solidLine')
b.ligne('J2p', 'L1'); b.ligne('L1', 'L3'); b.ligne('I2p', 'K1'); b.ligne('K1', 'C5')
b.chemin('cEmmDos', [('J2p', 'AngleLine_J2_J2p', '0', 'Line_J2p_L1*0.4'),
                     ('L1', '90', 'Line_J2p_L1*0.4', 'Line_L1_L3*0.4'),
                     ('L3', 'AngleLine_L4_L3+90', 'Line_L1_L3*0.3', '0')], 'p. 68 : emmanchure dos J2L1L3, angle droit en L3')
b.chemin('cEmmDev', [('I2p', 'AngleLine_I2_I2p', '0', 'Line_I2p_K1*0.4'),
                     ('K1', '90', 'Line_I2p_K1*0.4', 'Line_K1_C5*0.4'),
                     ('C5', 'AngleLine_P2_C5-90', 'Line_K1_C5*0.3', '0')], 'p. 68 : emmanchure devant I2K1C5, angle droit en C5')
b.end('Dp', 'D', 0, '#plat_enc_dos', 'p. 68 : platitude 2 cm au milieu dos', 'solidLine')
b.end('Cp', 'C', 180, '#plat_enc_dev', 'p. 68 : platitude 1 cm au milieu devant', 'solidLine')
b.spl('cEncDos', 'Dp', 'D2', '0', 'Line_D_D1*0.45', 'AngleLine_D2_D3-90', 'Line_D1_D2*0.6', 'p. 68 : encolure dos, angle droit en D')
b.spl('cEncDev', 'Cp', 'C2', '180', 'Line_C_C1*0.45', 'AngleLine_C2_P1+90', 'Line_C1_C2*0.5', 'p. 68 : encolure devant, angle droit en C')

b.piece('Dos base', [('p', 'D'), ('p', 'Dp'), ('c', 'cEncDos', 0), ('p', 'D2'), ('p', 'D3'), ('p', 'Z'), ('p', 'L4'), ('p', 'L3'),
                     ('cp', 'cEmmDos', 1), ('p', 'J2p'), ('p', 'J2'), ('p', 'M1'), ('c', 'cHdos', 1), ('p', 'A1'), ('p', 'A'),
                     ('p', 'F1'), ('p', 'L')], couture=0, inlayout=False, info=dict(data=(3, -25), pinfo=(3, -20), grain=(5, -2, 15)))
b.piece('Devant base', [('p', 'C5'), ('p', 'P2'), ('p', 'P3'), ('p', 'P1'), ('p', 'C2'), ('c', 'cEncDev', 1), ('p', 'Cp'), ('p', 'C'),
                        ('p', 'B'), ('p', 'B1'), ('c', 'cHdev', 0), ('p', 'M2'), ('p', 'I2'), ('p', 'I2p'), ('cp', 'cEmmDev', 0)],
        couture=0, inlayout=False, info=dict(data=(40, -25), pinfo=(40, -20), grain=(45, -2, 15)))

# ================= fond tailleur près du corps (T2 p. 78-81) =================
b.end('Ct', 'C', 270, '#t_enc_dev', 'p. 78 : milieu devant descendu de 2')
b.along('C2t', 'C2', 'P1', '#t_ouv_epaule', 'p. 78 : encolure devant ouverte de 0,6 sur l\'épaule')
b.end('Dt', 'D', 270, '#t_enc_dos', 'p. 78 : milieu dos descendu de 0,1')
b.along('D2t', 'D2', 'D3', '#t_ouv_epaule', 'p. 78 : encolure dos ouverte de 0,6 sur l\'épaule')
b.along('C5t', 'P2', 'C5', 'shoulder_length+#t_allong_epaule-(Line_C2_P1-#t_ouv_epaule)',
        'p. 78 : pince fermée, épaule devant = longueur d\'épaule + 0,5 depuis la nouvelle encolure', 'solidLine')
b.along('L3t', 'L4', 'L3', 'shoulder_length+#t_allong_epaule-(Line_D2_D3-#t_ouv_epaule)',
        'p. 78 : pince fermée, épaule dos = longueur d\'épaule + 0,5 depuis la nouvelle encolure', 'solidLine')
b.end('K1t', 'K1', 180, '#t_carrure_dev', 'p. 78 : carrure devant + 0,5')
b.end('L1t', 'L1', 0, '#t_carrure_dos', 'p. 78 : carrure dos + 1')
b.end('I2a', 'I2', 180, '#t_dessous_bras', 'p. 78 : dessous de bras élargi de 2, parallèle à la ligne de poitrine')
b.end('I2t', 'I2a', 270, '#t_descente_bras', 'p. 78 : puis descendu de 1,75')
b.end('J2a', 'J2', 0, '#t_dessous_bras', 'p. 78 : dessous de bras dos élargi de 2')
b.end('J2t', 'J2a', 270, '#t_descente_bras', 'p. 78 : puis descendu de 1,75')
b.end('M1t', 'M1', 0, '#t_taille', 'p. 78 : taille + 1,25')
b.end('M2t', 'M2', 180, '#t_taille', 'p. 78 : taille + 1,25')
b.end('A1t', 'A1', 0, '#t_hanches', 'p. 78 : hanches + 1,5')
b.end('B1t', 'B1', 180, '#t_hanches', 'p. 78 : hanches + 1,5')
for a, m, h in (('J2t', 'M1t', 'A1t'), ('I2t', 'M2t', 'B1t')):
    b.ligne(a, m); b.ligne(m, h); b.ligne(a, h)
b.chemin('cCoteDos', [('J2t', '270', '0', 'Line_J2t_M1t*0.4'), ('M1t', 'AngleLine_J2t_A1t', 'Line_J2t_M1t*0.3', 'Line_M1t_A1t*0.3'),
                      ('A1t', '270', 'Line_M1t_A1t*0.4', '0')], 'p. 80 : côté dos adouci en courbe légère')
b.chemin('cCoteDev', [('I2t', '270', '0', 'Line_I2t_M2t*0.4'), ('M2t', 'AngleLine_I2t_B1t', 'Line_I2t_M2t*0.3', 'Line_M2t_B1t*0.3'),
                      ('B1t', '270', 'Line_M2t_B1t*0.4', '0')], 'p. 80 : côté devant, symétrique')
b.end('J2tp', 'J2t', 180, '#plat_emm_dos', 'platitude 1 cm (comme la base)', 'solidLine')
b.end('I2tp', 'I2t', 0, '#plat_emm_dev', 'platitude 2 cm (comme la base)', 'solidLine')
b.ligne('J2tp', 'L1t'); b.ligne('L1t', 'L3t'); b.ligne('I2tp', 'K1t'); b.ligne('K1t', 'C5t')
b.chemin('cEmmDosT', [('J2tp', '180', '0', 'Line_J2tp_L1t*0.5'), ('L1t', '90', 'Line_J2tp_L1t*0.35', 'Line_L1t_L3t*0.4'),
                      ('L3t', 'AngleLine_L4_L3+90', 'Line_L1t_L3t*0.3', '0')], 'p. 80 : emmanchure dos retracée par les nouveaux points')
b.chemin('cEmmDevT', [('I2tp', '0', '0', 'Line_I2tp_K1t*0.55'), ('K1t', '90', 'Line_I2tp_K1t*0.3', 'Line_K1t_C5t*0.4'),
                      ('C5t', 'AngleLine_P2_C5-90', 'Line_K1t_C5t*0.3', '0')], 'p. 80 : emmanchure devant retracée')
b.end('Dtp', 'Dt', 0, '#plat_enc_dos', 'platitude 2 cm au milieu dos', 'solidLine')
b.end('Ctp', 'Ct', 180, '#plat_enc_dev', 'platitude 1 cm au milieu devant', 'solidLine')
b.spl('cEncDosT', 'Dtp', 'D2t', '0', 'Line_D_D1*0.45', 'AngleLine_D2_D3-90', 'Line_D1_D2*0.7', 'p. 80 : nouvelle encolure dos')
b.spl('cEncDevT', 'Ctp', 'C2t', '180', 'Line_C_C1*0.5', 'AngleLine_C2_P1+90', 'Line_C1_C2*0.6', 'p. 80 : nouvelle encolure devant')

b.piece('Dos fond tailleur', [('p', 'Dt'), ('p', 'Dtp'), ('c', 'cEncDosT', 0), ('p', 'D2t'), ('p', 'D3'), ('p', 'Z'), ('p', 'L4'), ('p', 'L3t'),
                     ('cp', 'cEmmDosT', 1), ('p', 'J2tp'), ('p', 'J2t'), ('cp', 'cCoteDos', 0), ('p', 'A1t'), ('p', 'A'),
                     ('p', 'F1'), ('p', 'L')], couture=0, inlayout=False, info=dict(data=(3, -25), pinfo=(3, -20), grain=(5, -2, 15)))
b.piece('Devant fond tailleur', [('p', 'C5t'), ('p', 'P2'), ('p', 'P3'), ('p', 'P1'), ('p', 'C2t'), ('c', 'cEncDevT', 1), ('p', 'Ctp'), ('p', 'Ct'),
                        ('p', 'B'), ('p', 'B1t'), ('cp', 'cCoteDev', 1), ('p', 'I2t'), ('p', 'I2tp'), ('cp', 'cEmmDevT', 0)],
        couture=0, inlayout=False, info=dict(data=(40, -25), pinfo=(40, -20), grain=(45, -2, 15)))
b.piece('Controle ecart', [('p', 'L1t'), ('p', 'K1t'), ('p', 'I2t'), ('p', 'J2t')], couture=0, inlayout=False)
b.piece('Controle ecart base', [('p', 'L1'), ('p', 'K1'), ('p', 'I2'), ('p', 'J2')], couture=0, inlayout=False)

# ---- profondeur d'emmanchure (T1 p. 144) : devant et dos assemblés par le dessous de bras
b.ligne('I2t', 'J2t')
b.deplacement('AngleLine_I2t_J2t', 'Line_I2t_J2t', ['C5t'], 'a')
b.ligne('L3t', 'C5ta')
b.along('Cemm', 'L3t', 'C5ta', 'Line_L3t_C5ta/2', 'T1 p. 144 : C = 1/2 AB, bouts d\'épaule joints')
b.ligne('Cemm', 'J2t')
EMM_DOS = '(Line_J2t_J2tp+SplPath_J2tp_L3t)'
EMM_DEV = '(Line_I2t_I2tp+SplPath_I2tp_C5t)'
PROF = 'Line_Cemm_J2t'

# ================= boléro (modèle) : coupé sous les bras, devant arrondi ouvert =================
b.coupe('bHc', 'cCoteDos', '#bolero_sous_bras', 'modèle : bas au côté dos, mesuré sur la couture de côté')
b.coupe('bHc1', 'cCoteDos', '#bolero_sous_bras-0.5', 'tangente au côté (bas d\'équerre avec le côté)')
b.coupe('bHc2', 'cCoteDos', '#bolero_sous_bras+0.5', 'tangente au côté')
b.ligne('bHc1', 'bHc2')
b.axe('bHd', 'bHc', 180, 'L', 'F1', 'modèle : bas au milieu dos', 'dotLine')
b.coupe('bFc', 'cCoteDev', '#bolero_sous_bras', 'modèle : bas au côté devant, mesuré sur la couture de côté')
b.coupe('bFc1', 'cCoteDev', '#bolero_sous_bras-0.5', 'tangente au côté')
b.coupe('bFc2', 'cCoteDev', '#bolero_sous_bras+0.5', 'tangente au côté')
b.ligne('bFc1', 'bFc2')
b.axe('bFm', 'bFc', 0, 'Ct', 'B', 'modèle : bas au milieu devant', 'dotLine')
b.end('bR1', 'bFm', 90, '#bolero_arrondi', 'modèle : départ de l\'arrondi sur le milieu devant')
b.end('bR2', 'bFm', 180, '#bolero_arrondi', 'modèle : fin de l\'arrondi sur le bas')
b.ligne('bHd', 'bHc'); b.ligne('bFc', 'bR2')
b.spl('cArrondi', 'bR1', 'bR2', '270', '#bolero_arrondi*0.55', '0', '#bolero_arrondi*0.55', 'modèle : devant arrondi, ouvert sans fermeture')
b.spl('cBasDos', 'bHd', 'bHc', 'AngleLine_L_F1+90', 'Line_bHd_bHc/3', 'AngleLine_bHc1_bHc2-90', 'Line_bHd_bHc/3',
      'modèle : bas d\'équerre avec le milieu dos et avec le côté')
b.spl('cBasDev', 'bFc', 'bR2', 'AngleLine_bFc1_bFc2+90', 'Line_bFc_bR2/3', '180', 'Line_bFc_bR2/3',
      'modèle : bas d\'équerre avec le côté, raccordé à l\'arrondi')
# ================= manche tailleur (T2 p. 150-153) =================
m = b   # même bloc : les crans d'emmanchure lisent la tête de manche
m.single('mA', 75, -72, 'p. 150 : droit fil milieu de manche')
m.end('mB', 'mA', 270, '#long_manche+#epaulette', 'p. 150 : AB = longueur de manche + épaulette', 'dashLine')
m.end('mC', 'mA', 270, PROF + '*7/8', 'p. 150 : AC = hauteur d\'emmanchure − son 1/8')
m.end('mD', 'mA', 270, '#haut_coude+#epaulette', 'p. 150 : AD = 35 + épaulette')
m.end('mE', 'mA', 180, '0.7*' + EMM_DOS + '/2', 'p. 150 : AE = 7/10 emmanchure dos : 2', 'dotLine')
m.end('mF', 'mA', 0, '0.7*' + EMM_DEV + '/2', 'p. 150 : AF = 7/10 emmanchure devant : 2', 'dotLine')
m.end('mEp', 'mB', 180, 'Line_mA_mE', 'p. 150 : BE\' = AE', 'dotLine')
m.end('mFp', 'mB', 0, 'Line_mA_mF', 'p. 150 : BF\' = AF', 'dotLine')
m.ligne('mE', 'mEp', 'dotLine'); m.ligne('mF', 'mFp', 'dotLine')
m.axe('mG', 'mC', 180, 'mE', 'mEp', 'p. 150 : G = segment C ∩ EE\'', 'dotLine')
m.axe('mH', 'mC', 0, 'mF', 'mFp', 'p. 150 : H = segment C ∩ FF\'', 'dotLine')
m.ligne('mE', 'mG'); m.ligne('mF', 'mH')
m.along('mI', 'mE', 'mG', 'Line_mE_mG/2+1', 'p. 150 : EI = 1/2 EG + 1')
m.along('mIp', 'mF', 'mH', 'Line_mF_mH/2+1', 'p. 150 : FI\' = 1/2 FH + 1')
m.end('mIpp', 'mIp', 180, 0.75, 'p. 150 : I\'I\'\' = 0,75')
m.end('mJ', 'mH', 180, 2.5, 'p. 150 : HJ = 2,5')
m.end('mJp', 'mH', 0, 2.5, 'p. 150 : HJ\' = 2,5')
m.end('mK', 'mJ', 90, '#m_JK', 'p. 150 : JK = 0,5 (à régler)')
m.end('mKp', 'mJp', 90, '#m_JK', 'p. 150 : J\'K\' = 0,5 (à régler)')
m.end('mL', 'mH', 90, '#m_HL', 'p. 150 : HL = 5 (à régler)')
m.axe('mR', 'mD', 180, 'mE', 'mEp', 'figure p. 151 : R = ligne de coude ∩ EE\'', 'dotLine')
m.axe('mM', 'mD', 0, 'mF', 'mFp', 'figure p. 151 : M = ligne de coude ∩ FF\'', 'dotLine')
m.end('mMp', 'mM', 180, 5, 'p. 150 : MM\' = 5')
m.end('mRp', 'mR', 180, 1, 'p. 152 : RR\' = 1')
m.end('mO', 'mFp', 90, 2, 'p. 150 : F\'O = 2, sur FF\' (figure p. 151)')
m.ligne('mR', 'mO')
m.along('mW', 'mR', 'mO', 'Line_mR_mO/2', 'p. 152 : équerre en P passant par R et O (cercle de diamètre RO)')
m.contact('mP', 'mW', 'mEp', 'mFp', 'Line_mR_mO/2', 'p. 152 : P sur le bas du cadre, angle droit RPO')
m.ligne('mP', 'mO')
m.along('mQ', 'mP', 'mO', '#bas_manche/2+2', 'p. 152 : PQ = bas/2 + 2 (dessus)')
m.along('mQp', 'mP', 'mO', '#bas_manche/2-2', 'p. 152 : PQ\' = bas/2 − 2 (dessous)')
m.along('mS', 'mE', 'mG', 'Line_mE_mG/4', 'p. 152 : S = 1/4 EG')
m.ligne('mS', 'mC', 'dotLine')
m.end('mT', 'mI', 90, '#m_IT', 'p. 152 : IT = 1 à 1,5')
m.end('mU', 'mT', 180, 2.5, 'p. 152 : TU = 2,5')
m.end('mUp', 'mT', 0, 2.5, 'p. 152 : TU\' = 2,5')
m.ligne('mU', 'mRp'); m.ligne('mUp', 'mR')
m.along('mX1', 'mU', 'mRp', 'Line_mU_mRp/2', 'p. 152 : moitié de R\'U')
m.normal('mX1o', 'mX1', 'mRp', 0.5, 180, 'p. 152 : ressortir de 0,5')
m.along('mX2', 'mUp', 'mR', 'Line_mUp_mR/2', 'p. 152 : moitié de RU\'')
m.normal('mX2o', 'mX2', 'mR', 0.5, 180, 'p. 152 : ressortir de 0,5')
m.ligne('mC', 'mJ')
m.along('mV', 'mC', 'mJ', 'Line_mC_mJ/2', 'p. 152 : V = 1/2 CJ, cran de dessous de manche')
m.ligne('mP', 'mQ')
# lignes d'appui des courbes
for a_, b_ in (('mU', 'mS'), ('mU', 'mA'), ('mA', 'mKp'), ('mS', 'mA'), ('mA', 'mIpp'), ('mA', 'mL'), ('mIpp', 'mL'), ('mIpp', 'mKp'), ('mL', 'mKp'),
               ('mKp', 'mM'), ('mM', 'mQ'), ('mK', 'mMp'), ('mMp', 'mQp'), ('mX1o', 'mRp'), ('mRp', 'mP'), ('mU', 'mX1o'),
               ('mUp', 'mX2o'), ('mX2o', 'mR'), ('mR', 'mP'), ('mX1o', 'mP'), ('mX2o', 'mP'), ('mUp', 'mC'), ('mUp', 'mV'), ('mV', 'mK')):
    m.ligne(a_, b_)
m.ligne('mKp', 'mQ'); m.ligne('mK', 'mQp'); m.ligne('mU', 'mP'); m.ligne('mUp', 'mP')
PERP = 'AngleLine_mP_mQ-90'
m.chemin('mTete', [('mU', 'AngleLine_mU_mS', '0', 'Line_mU_mS*0.35'),
                   ('mS', 'AngleLine_mU_mA', 'Line_mU_mS*0.35', 'Line_mS_mA*0.35'),
                   ('mA', '0', 'Line_mS_mA*0.4', 'Line_mA_mIpp*0.4'),
                   ('mIpp', 'AngleLine_mA_mKp', 'Line_mA_mIpp*0.35', 'Line_mIpp_mL*0.35'),
                   ('mL', 'AngleLine_mIpp_mKp', 'Line_mIpp_mL*0.35', 'Line_mL_mKp*0.35'),
                   ('mKp', 'AngleLine_mL_mKp', 'Line_mL_mKp*0.35', '0')], 'p. 152 : tête du dessus K\'LI\'\'ASU')
m.chemin('mTeteDessous', [('mUp', 'AngleLine_mUp_mX2o+180-AngleLine_mU_mS+AngleLine_mU_mX1o', '0', 'Line_mUp_mV*0.4'),
                          ('mV', '0', 'Line_mUp_mV*0.4', '0')], 'p. 152 : dessous U\'V en s\'appuyant sur U\'C')
m.chemin('mTeteDessous2', [('mV', '0', '0', 'Line_mV_mK*0.4'),
                           ('mK', 'AngleLine_mK_mMp+AngleLine_mKp_mM-AngleLine_mL_mKp-180', 'Line_mV_mK*0.4', '0')], 'p. 152 : dessous VK, finir en légère courbe')
m.chemin('mSaignee', [('mKp', 'AngleLine_mKp_mM', '0', 'Line_mKp_mM*0.35'), ('mM', 'AngleLine_mKp_mQ', 'Line_mKp_mM*0.35', 'Line_mM_mQ*0.35'),
                      ('mQ', PERP, 'Line_mM_mQ*0.35', '0')], 'p. 152 : saignée du dessus K\'MQ, angle droit en Q')
m.chemin('mSaigneeD', [('mK', 'AngleLine_mK_mMp', '0', 'Line_mK_mMp*0.35'), ('mMp', 'AngleLine_mK_mQp', 'Line_mK_mMp*0.35', 'Line_mMp_mQp*0.35'),
                       ('mQp', PERP, 'Line_mMp_mQp*0.35', '0')], 'p. 152 : saignée du dessous KM\'Q\', angle droit en Q\'')
m.chemin('mCoude', [('mU', 'AngleLine_mU_mX1o', '0', 'Line_mU_mX1o*0.35'), ('mX1o', 'AngleLine_mU_mRp', 'Line_mU_mX1o*0.35', 'Line_mX1o_mRp*0.35'),
                    ('mRp', 'AngleLine_mX1o_mP', 'Line_mX1o_mRp*0.35', 'Line_mRp_mP*0.35'), ('mP', PERP, 'Line_mRp_mP*0.35', '0')],
         'p. 152 : coude du dessus UR\'P, angle droit en P')
m.chemin('mCoudeD', [('mUp', 'AngleLine_mUp_mX2o', '0', 'Line_mUp_mX2o*0.35'), ('mX2o', 'AngleLine_mUp_mR', 'Line_mUp_mX2o*0.35', 'Line_mX2o_mR*0.35'),
                     ('mR', 'AngleLine_mX2o_mP', 'Line_mX2o_mR*0.35', 'Line_mR_mP*0.35'), ('mP', PERP, 'Line_mR_mP*0.35', '0')],
         'p. 152 : coude du dessous U\'RP')
# ---- crans (p. 152-153)
TETE = '(SplPath_mU_mKp+SplPath_mUp_mV+SplPath_mV_mK)'
m.coupe('mCt', 'mTete', TETE + '*' + EMM_DOS + '/(' + EMM_DOS + '+' + EMM_DEV + ')-SplPath_mUp_mV',
        'p. 152 : cran de tête, embu réparti devant et dos au prorata des emmanchures')
m.coupe('mCc1', 'mCoude', 'SplPath_mU_mP-20', 'p. 153 : cran de coude à 20 cm de P (dessus)')
m.coupe('mCc2', 'mCoude', '20', 'p. 153 : cran de coude à 20 cm de U (dessus)')
m.coupe('mCc3', 'mCoudeD', 'SplPath_mUp_mP-20', 'p. 153 : cran de coude à 20 cm de P (dessous)')
m.coupe('mCc4', 'mCoudeD', '20', 'p. 153 : cran de coude à 20 cm de U\' (dessous)')
m.coupe('mCs1', 'mSaignee', 'SplPath_mKp_mQ-20', 'p. 153 : cran de saignée à 20 cm de Q (dessus)')
m.coupe('mCs2', 'mSaignee', '15', 'p. 153 : cran de saignée à 15 cm de K\' (dessus)')
m.coupe('mCs3', 'mSaigneeD', 'SplPath_mK_mQp-20', 'p. 153 : cran de saignée à 20 cm de Q\' (dessous)')
m.coupe('mCs4', 'mSaigneeD', '15', 'p. 153 : cran de saignée à 15 cm de K (dessous)')
N = dict(notch=True)
RAPPORT = '(' + EMM_DOS + '+' + EMM_DEV + ')/' + TETE
b.coupe('cranDev', 'cEmmDevT', 'SplPath_mV_mK*' + RAPPORT + '-Line_I2t_I2tp',
        'p. 152 : crans devant, en face de la saignée (embu réparti régulièrement, à confirmer sur la toile)')
b.coupe('cranDos', 'cEmmDosT', 'SplPath_mUp_mV*' + RAPPORT + '-Line_J2t_J2tp',
        'p. 152 : cran dos, en face de la ligne de coude (à confirmer sur la toile)')
N2 = dict(notch=True, count=2)
b.piece('Dos boléro', [('p', 'Dt'), ('p', 'Dtp'), ('c', 'cEncDosT', 0), ('p', 'D2t'), ('p', 'D3'), ('p', 'Z'), ('p', 'L4'), ('p', 'L3t'),
                       ('cp', 'cEmmDosT', 1), ('p', 'cranDos', N), ('cp', 'cEmmDosT', 1), ('p', 'J2tp'), ('p', 'J2t'), ('cp', 'cCoteDos', 0), ('p', 'bHc'), ('c', 'cBasDos', 1), ('p', 'bHd'), ('p', 'L')],
        qte=2, couture=1, info=dict(data=(2, -54), pinfo=(2, -50.5), grain=(12, -35, 12)))
b.piece('Devant boléro', [('p', 'C5t'), ('p', 'P2'), ('p', 'P3'), ('p', 'P1'), ('p', 'C2t'), ('c', 'cEncDevT', 1), ('p', 'Ctp'), ('p', 'Ct'),
                          ('p', 'bR1'), ('c', 'cArrondi', 0), ('p', 'bR2'), ('c', 'cBasDev', 1), ('p', 'bFc'), ('cp', 'cCoteDev', 1), ('p', 'I2t'), ('p', 'I2tp'),
                          ('cp', 'cEmmDevT', 0), ('p', 'cranDev', N2), ('cp', 'cEmmDevT', 0)],
        qte=2, couture=1, info=dict(data=(36, -50), pinfo=(36, -46.5), grain=(46, -36, 12)))
m.piece('Dessus de manche', [('p', 'mU'), ('cp', 'mTete', 0), ('p', 'mCt', N), ('cp', 'mTete', 0), ('p', 'mKp'),
                              ('cp', 'mSaignee', 0), ('p', 'mCs2', N), ('cp', 'mSaignee', 0), ('p', 'mCs1', N), ('cp', 'mSaignee', 0),
                              ('p', 'mQ'), ('p', 'mP'),
                              ('cp', 'mCoude', 1), ('p', 'mCc1', N), ('cp', 'mCoude', 1), ('p', 'mCc2', N), ('cp', 'mCoude', 1)],
        qte=2, couture=1, info=dict(data=(71, -55), pinfo=(71, -50), grain=(75, -20, 20)))
m.piece('Dessous de manche', [('p', 'mUp'), ('cp', 'mTeteDessous', 0), ('p', 'mV', N), ('cp', 'mTeteDessous2', 0), ('p', 'mK'),
                               ('cp', 'mSaigneeD', 0), ('p', 'mCs4', N), ('cp', 'mSaigneeD', 0), ('p', 'mCs3', N), ('cp', 'mSaigneeD', 0),
                               ('p', 'mQp'), ('p', 'mP'),
                               ('cp', 'mCoudeD', 1), ('p', 'mCc3', N), ('cp', 'mCoudeD', 1), ('p', 'mCc4', N), ('cp', 'mCoudeD', 1)],
        qte=2, couture=1, info=dict(data=(74, -45), pinfo=(74, -40), grain=(78, -20, 15)))

# ================= col officier (tome 1, « Col officier / Mandarin collar ») =================
# AB = demi-encolure mesurée sur la couture d'encolure du boléro : milieu dos - épaule + épaule - milieu devant.
ENC_DOS = '(Line_Dt_Dtp+Spl_Dtp_D2t)'
ENC = '(' + ENC_DOS + '+Spl_Ctp_C2t+Line_Ct_Ctp)'
b.single('kA', 100, -10, 'col officier : A, milieu dos, sur le droit-fil')
b.end('kB', 'kA', 0, ENC, 'AB = 1/2 encolure du vêtement', 'solidLine')
b.end('kD', 'kA', 90, '#col_hauteur', 'AD = hauteur du col, perpendiculaire à AB', 'solidLine')
b.end('kC', 'kB', 90, '#col_hauteur', 'rectangle ABCD', 'solidLine')
b.ligne('kD', 'kC', 'solidLine')
b.end('kE', 'kA', 0, 'Line_kA_kB/3', 'AE = 1/3 AB', 'solidLine')
b.end('kE2', 'kD', 0, 'Line_kA_kB/3', 'DE\' = 1/3 AB', 'solidLine')
b.end('kB1', 'kB', 90, 'Line_kA_kB/10', 'BB\' = 1/10 AB (1/15 pour une encolure plus dégagée)', 'solidLine')
b.normal('kB2', 'kB1', 'kE', '#col_hauteur-0.5', 180, 'B\'B\'\' perpendiculaire à EB\', B\'B\'\' = AD - 0,5', 'solidLine')
b.ligne('kE', 'kB1'); b.ligne('kE2', 'kB2')
b.chemin('cColBas', [('kE', '0', '0', 'Line_kE_kB1*0.4'), ('kB1', '2*AngleLine_kE_kB1', 'Line_kE_kB1*0.4', '0')],
         'EB\' en courbe au perroquet (bord d\'encolure du col)')
b.chemin('cColHaut', [('kE2', '0', '0', 'Line_kE2_kB2*0.4'), ('kB2', '2*AngleLine_kE2_kB2', 'Line_kE2_kB2*0.4', '0')],
         'E\'B\'\' en légère courbe (bord du col)')
b.along('kF0', 'kA', 'kB', ENC_DOS, 'AF = 1/2 encolure dos', 'none')
b.courbe_axe('kF', 'kF0', 90, 'cColBas', 'cran F sur le bord d\'encolure du col')
b.piece('Col officier', [('p', 'kD'), ('p', 'kE2'), ('cp', 'cColHaut', 0), ('p', 'kB2'), ('p', 'kB1'),
                         ('cp', 'cColBas', 1), ('p', 'kF', N), ('cp', 'cColBas', 1), ('p', 'kE'), ('p', 'kA')],
        qte=2, couture=1, info=dict(data=(102, -12.6), pinfo=(108.5, -12.6), grain=(101, -10.9, 2.5),
                                    data_dim=(5, 2), pinfo_dim=(5, 2)))

with open(sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'patrons', 'bolero.sm2d'), 'w') as out:
    out.write(f.xml('BOLÉRO'))
