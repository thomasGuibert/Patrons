# Boléro (veste courte doublée, devant arrondi ouvert, col officier) : étapes

Sources (transcriptions à côté des photos) :
- `doc/sources/buste/base-mannequin/` : base du mannequin (T2 p. 62-71 = T1 p. 76-85) ;
- `doc/sources/buste/elargissement-tailleur/` : fond tailleur près du corps (T2 p. 78-81) ;
- `doc/sources/manche/manche-tailleur/` : manche tailleur deux pièces (T2 p. 150-153) ;
- `doc/sources/manche/profondeur-ecart-emmanchure/` : profondeur et écart d'emmanchure (T1 p. 144).
Analyse : `doc/patronage/chaine-et-trame-femme.md`.

Fichier : `patrons/bolero.sm2d`, mesures `../mesures/femme/T38.smms` (taille de référence du livre).
Le fichier est produit par `outils/bolero/build.py` (`python3 outils/bolero/build.py T38 patrons/bolero.sm2d`) : base, fond tailleur et pièces de contrôle sont gardés
dans le fichier (hors plan de coupe, `inLayout="false"`) pour suivre le livre pas à pas.

## Choix (Thomas ou livre)
- **Sans épaulette** : `#epaulette` = 0 (Thomas, 2026-10-27).
- **L4 remonté de 0,5** au-dessus de la ligne d'épaule (annotation du tome 1, confirmée par Thomas).
- **Col officier** (Thomas, 2026-10-27, `doc/sources/col/col-officier/`) : l'encolure du fond tailleur est gardée telle quelle (bord à bord, déjà fermée au milieu devant) ; le col se pose dessus. Hauteur 3 cm (`#col_hauteur`, exemple du livre). Pas de croisure ni de boutonnage : le boléro reste bord à bord.
- Point de poitrine P2 : intersection de cercles côté extérieur (`crossPoint` 2), sinon la pince disparaît.
- Carrure : déplacements horizontaux (parallèles à la ligne de poitrine).
- Fond tailleur : le « milieu devant + 0,75 » (croisure) n'est **pas** appliqué, le boléro est bord à bord.
- Manche : IT = 1,25 (livre 1 à 1,5), bas de manche 24 (exemple du livre), JK = 0,5 et HL = 5
  (« à régler » au livre) en variables `#m_JK`, `#m_HL`.
- Modèle : bas à `#bolero_sous_bras` = 9 cm sous le dessous de bras du fond tailleur (mesurés
  sur la couture de côté), arrondi du devant `#bolero_arrondi` = 6 cm. Le bas est d'équerre avec
  le milieu dos et avec le côté, pour un bas sans angle une fois cousu. Pinces de taille non reportées (le boléro s'arrête au-dessus) ;
  pince d'épaule devant (poitrine) et pince d'omoplate gardées.
- Dos : milieu dos cambré (L → F1), donc **couture milieu dos**, dos coupé ×2 (pas au pli).
- Coutures 1 cm partout.

## Pièces
- Dos boléro ×2, Devant boléro ×2, Dessus de manche ×2, Dessous de manche ×2.
- Crans : tête de manche (embu réparti devant/dos au prorata des emmanchures), V sur le dessous
  (posé sur le dessous de bras), coude à 20 cm de P et de U/U', saignée à 20 cm de Q/Q' et 15 cm
  de K/K' (p. 153). Crans d'emmanchure : 1 au dos (en face de la ligne de coude), 2 au devant (en
  face de la saignée), embu réparti régulièrement. Le livre les place après la toile : **à
  confirmer sur la toile**.
- Tête de manche : le dessous part de U' et arrive en K avec l'angle qui prolonge le dessus une
  fois cousu (pas d'angle aux coutures de coude et de saignée).
- Col officier ×2 (une moitié par côté, couture milieu dos comme le dos) : rectangle AB = demi-encolure
  mesurée sur la couture d'encolure du boléro (milieu dos - épaule + épaule - milieu devant), AD = 3 cm,
  AE = DE' = AB/3, BB' = AB/10, B'B'' = AD - 0,5 perpendiculaire à EB', cran F à AF = demi-encolure dos.
  Droit-fil le long du milieu dos. La page ne dit ni le nombre de pièces (dessus, dessous) ni l'entoilage :
  **à confirmer** avant de couper.
- **Parementure** (Thomas, 2026-10-27) : 8 cm au bord de devant (`#facing_larg`, livre : 8 cm minimum pour les cols
  tailleur), le bord descend d'équerre depuis un point à 4 cm de l'encolure sur l'épaule (`#facing_epaule`, livre : 3,5 à
  5 cm) jusqu'au bas. Parementure ×2 dans le tissu, devant entier en tissu (la parementure se pose dessus).
- **Doublure** (tome 2 p. 203, `doc/sources/doublure/doublure-de-veste/`) : mêmes formes que le boléro, valeurs de
  couture du livre : épaule 1,5, côté 1,5 (au-dessus de la taille), le reste 1. Dos doublure ×2 (couture milieu dos),
  devant doublure ×2 arrêté au bord de parementure, dessus et dessous de manche doublure ×2 (couture 1 partout : les
  valeurs du livre pour la tête de manche, de 0 à 3, ne se placent pas sans ambiguïté sur la photo). Le bas est coupé à
  la ligne du bas du boléro : ourlet de doublure (+1 cm, repli de 3 cm) du livre non repris, le boléro n'a pas d'ourlet de 4 cm.
  **À confirmer** : hauteur du bas de doublure, valeurs de tête de manche.
- **À faire** : rien d'autre dans les pages reçues.

## PDF
Les pièces de contrôle (base, fond tailleur, écarts) sont hors plan de coupe dans Seamly mais l'export des pièces les
sort quand même : pour imprimer, on retire d'abord les pièces `inLayout="false"` d'une copie du `.sm2d`, puis
`mesures_vers_pdf.py` (skill exporter-pdf) sur cette copie, une taille à la fois (T36 à T44, A4 et A3).
Boléro T38 : 12 feuilles A4 (4 pour manche dessus + col, 4 devant, 2 dos, 2 dessous de manche). Les étiquettes du col
tiennent dans sa bande de 3 cm (nom et quantité à gauche, taille à droite).

## Vérifications (2026-10-27)
`python3 outils/coherence/coherence.py bolero` (contrôles dans `patrons/bolero.coherence.toml`) ;
calcul hors Seamly identique à Seamly (0,2 mm).

| Taille | Tête de manche | Emmanchure dos + devant | Embu | Profondeur |
|---|---|---|---|---|
| T36 | 46,23 | 22,16 + 21,65 | 2,41 | 17,36 |
| T38 | 47,18 | 22,78 + 22,32 | 2,08 | 17,53 |
| T40 | 48,21 | 23,45 + 23,06 | 1,70 | 17,71 |
| T42 | 49,30 | 24,18 + 23,84 | 1,28 | 17,89 |
| T44 | 50,45 | 24,96 + 24,66 | 0,84 | 18,07 |

Livre : embu 3,5 cm en lainage souple, 2 cm en tissu sec. T38 est dans la cible ; l'embu baisse
avec la taille (la hauteur de tête suit la profondeur, la largeur suit l'emmanchure). JK et HL ne
le corrigent presque pas (T44 : HL 4 → 0,92). À revoir avec la toile avant de grader.

Écart d'emmanchure (T38) : base 9,75 (livre 10,75), fond tailleur 12,25 (livre 12,75).

Défauts restants (contrôle « virages brusques », angle sur 1,5 cm) :
- **Corrigé le 2026-10-27** (poignées des courbes seulement, aucun point déplacé) : dessous de manche entre V et K
  (44° → 12°) et dessus de manche (30° → 9°). Les poignées sont les paramètres `k('…')` de `build.py`.
  Les crans (cran de tête, devant) glissent d'1 mm au plus, la longueur de tête change de moins d'1 mm.
- Reste : emmanchure devant en I2tp (15 à 18° en T36-T38) et dos près de J2tp (16° en T36). Les corriger demande de
  changer la longueur de l'emmanchure de 1 à 2 mm, donc de déplacer d'autant les points de la manche calculés sur elle :
  à décider avec Thomas.

## Étapes (générées avec le tracé, formule et page du livre)

### Corsage : base, fond tailleur, boléro

1. **A** : Point de départ = `(0, 0)` (p. 62 : axe XY, A milieu dos)
2. **B** : depuis A, angle 0 = `hip_circ/2+#constr_hanches` (p. 62 : AB = 1/2 tour de hanches + 3)
3. **F** : depuis A, angle 90 = `height_waist_side_to_hip` (p. 62 : hauteur taille-hanches (22))
4. **E** : depuis B, angle 90 = `height_waist_side_to_hip` (p. 62 : BE = hauteur taille-hanches)
5. **C** : depuis E, angle 90 = `neck_front_to_waist_f` (p. 62 : longueur taille devant)
6. **D** : depuis F, angle 90 = `neck_back_to_waist_b` (p. 62 : longueur taille dos)
7. **G** : depuis E, angle 270 = `#petites_hanches` (p. 62 : G à 9 cm sous E)
8. **H** : depuis F, angle 270 = `#petites_hanches` (p. 62 : petites hanches)
9. **E1** : depuis E, angle 180 = `bustpoint_to_bustpoint_half` (p. 62 : EE1 = 1/2 écart de poitrine)
10. **I** : depuis C, angle 270 = `sqrt(bustpoint_to_neck_front^2-bustpoint_to_bustpoint_half^2)` (p. 62 : CP = hauteur de poitrine sur la parallèle au milieu par E1 ; I = ligne de poitrine sur le milieu devant)
11. **P** : depuis I, angle 180 = `bustpoint_to_bustpoint_half` (p. 62 : P, point de poitrine)
12. **J** : depuis I, angle 180, jusqu'à AD (p. 62 : ligne de poitrine IJ)
13. **L** : sur DJ = `Line_D_J/2` (p. 62 : L = 1/2 DJ)
14. **K** : depuis L, angle 0, jusqu'à EC (p. 62 : ligne de carrure)
15. **A1** : depuis A, angle 0 = `hip_circ/4-1` (p. 62 : AA1 = 1/4 hanches − 1)
16. **B1** : depuis B, angle 180 = `hip_circ/4+1` (p. 62 : BB1 = 1/4 hanches + 1)
17. **J1** : depuis J, angle 0 = `bust_circ/4` (p. 62 : JJ1 = 1/4 poitrine)
18. **I1** : depuis I, angle 180 = `bust_circ/4+2` (p. 62 : II1 = 1/4 poitrine + 2)
19. **C1** : depuis C, angle 180 = `neck_circ/2/3+0.5` (p. 64 : CC1 = 1/3 de 1/2 encolure + 0,5)
20. **C2** : depuis C1, angle 90 = `Line_C_C1` (p. 64 : C1C2 = CC1)
21. **C3** : sur C1C2 = `Line_C1_C2/2` (p. 64 : C1C3 = 1/2 C1C2)
22. **C3h** : depuis C3, angle 180 = `20` (p. 64 : perpendiculaire à C1C2 sur 20 cm)
23. **C4** : cercle (C2, r) ∩ C3hC3 = `shoulder_length` (p. 64 : longueur d'épaule depuis C2)
24. **D1** : depuis D, angle 0 = `(neck_circ/2/3)*7/6` (p. 64 : DD1 = 1/3 de 1/2 encolure + son 1/6)
25. **D2** : depuis D1, angle 90 = `Line_D_D1/3` (p. 64 : D1D2 = 1/3 DD1)
26. **L1** : depuis L, angle 0 = `across_back_b/2` (p. 64 : LL1 = 1/2 carrure dos)
27. **L2** : depuis L1, angle 90 = `Line_D_D1+3` (p. 64 : L1L2 = DD1 + 3)
28. **L2h** : depuis L2, angle 0 = `8` (p. 64 : perpendiculaire en L2)
29. **L3** : cercle (D2, r) ∩ L2hL2 = `shoulder_length+#pince_omoplate` (p. 64 : D2L3 = épaule + pince d'omoplate)
30. **N1** : A1J1 ∩ FE (figure p. 67 : N1 = côté dos ∩ taille)
31. **N2** : B1I1 ∩ FE (figure p. 67 : N2 = côté devant ∩ taille)
32. **M1** : depuis N1, angle 180 = `(Line_F_N1+Line_N2_E-waist_circ/2-#pinces)/2` (p. 64 : M1N1 = (excédent − pinces)/2)
33. **M2** : depuis N2, angle 0 = `(Line_F_N1+Line_N2_E-waist_circ/2-#pinces)/2` (p. 64 : N2M2 = (excédent − pinces)/2)
34. **J2** : sur M1J1 = `(neck_back_to_waist_b+neck_front_to_waist_f)/4+2` (p. 68 : M1J2 = (long. taille dos + devant)/4 + 2)
35. **I2** : sur M2I1 = `(neck_back_to_waist_b+neck_front_to_waist_f)/4+2` (p. 68 : M2I2 = M1J2)
36. **cHdos** : courbe A1–M1 (p. 64 : joindre A1M1 en courbe)
37. **cHdev** : courbe B1–M2 (p. 64 : B1M2, courbe identique)
38. **F1** : depuis F, angle 0 = `#pince_dos1` (p. 66 : pince milieu dos, F1)
39. **D3** : sur D2L3 = `shoulder_length/2` (p. 66 : D2D3 = 1/2 épaule)
40. **L4b** : sur L3D2 = `shoulder_length/2` (p. 66 : L3L4 = 1/2 épaule)
41. **L4** : perpendiculaire en L4b à L4bL3 = `#remonte_L4` (annotation T1 : L4 remonté de 0,5)
42. **Q** : depuis F1, angle 0 = `#pos_pince_dos` (p. 66 : Q à 8,5 cm de F1)
43. **Q1** : depuis Q, angle 180 = `#pince_dos2/2` (p. 66 : Q1)
44. **Q2** : depuis Q, angle 0 = `#pince_dos2/2` (p. 66 : Q2)
45. **U** : Q1D3 ∩ LK (figure p. 69 : U = Q1D3 ∩ carrure)
46. **Tp** : Q1D3 ∩ JI (figure p. 69 : T = Q1D3 ∩ poitrine)
47. **Z** : sur D3Q1 = `#long_pince_omoplate` (p. 66 : D3Z = 7)
48. **V** : sur UTp = `Line_U_Tp/4` (p. 66 : UV = 1/4 UT)
49. **Qh** : depuis Q, angle 270, jusqu'à AB (p. 66 : parallèle au milieu dos par Q)
50. **V1** : depuis Qh, angle 90 = `#pointe_dos` (p. 66 : V1 à 9 cm au-dessus des hanches)
51. **S** : sur Q2M1 = `Line_Q2_M1/2` (p. 66 : S au milieu de Q2M1)
52. **S1** : depuis S, angle 180 = `#pince_dos3/2` (p. 66 : 3e pince dos)
53. **S2** : depuis S, angle 0 = `#pince_dos3/2` (p. 66 : 3e pince dos)
54. **Sh** : depuis S, angle 90, jusqu'à JI (p. 66 : jusqu'à la ligne de poitrine)
55. **Sb** : depuis S, angle 270, jusqu'à HG (p. 66 : jusqu'aux petites hanches)
56. **P1** : sur C2C4 = `shoulder_length/2` (p. 68 : C2P1 = 1/2 épaule)
57. **P3** : depuis P, angle 90 = `#remonte_P` (p. 68 : P3 = P remonté de 2)
58. **P2** : cercles (P3) ∩ (P1) = `Line_P3_P1 ; bust_circ/12` (p. 68 : P1P2 = 1/12 tour de poitrine (branches égales))
59. **K1c** : depuis K, angle 180 = `across_chest_f/2` (p. 68 : pince fermée, KK1 = 1/2 carrure devant)
60. **C5** : sur P2C4o = `Line_C2_P1` (p. 68 : P2C5 = C2P1 (pince rouverte))
61. **K1** : sur K1coP3 = `0` (p. 68 : K1 (pince rouverte))
62. **E2** : depuis E1, angle 180 = `#pince_dev1/2` (p. 68 : 1re pince devant)
63. **E3** : depuis E1, angle 0 = `#pince_dev1/2` (p. 68 : 1re pince devant)
64. **E4** : depuis P, angle 270 = `#descente_E4` (p. 68 : E4 = P descendu de 2)
65. **E1h** : depuis E1, angle 270, jusqu'à AB (p. 68 : parallèle au milieu devant par E1)
66. **e** : depuis E1h, angle 90 = `#pointe_dev` (p. 68 : e à 6 cm au-dessus des hanches)
67. **t** : sur M2E2 = `Line_M2_E2/2` (p. 68 : t au milieu de M2E2)
68. **t1** : depuis t, angle 180 = `#pince_dev2/2` (p. 68 : 2e pince devant)
69. **t2** : depuis t, angle 0 = `#pince_dev2/2` (p. 68 : 2e pince devant)
70. **th** : depuis t, angle 90, jusqu'à JI (p. 68 : jusqu'à la ligne de poitrine)
71. **tb** : depuis t, angle 270, jusqu'à HG (p. 68 : jusqu'aux petites hanches)
72. **J2p** : depuis J2, angle AngleLine_M1_J2+90 = `#plat_emm_dos` (p. 68 : platitude 1 cm en J2)
73. **I2p** : depuis I2, angle AngleLine_M2_I2-90 = `#plat_emm_dev` (p. 68 : platitude 2 cm en I2)
74. **cEmmDos** : courbe J2p–L1–L3 (p. 68 : emmanchure dos J2L1L3, angle droit en L3)
75. **cEmmDev** : courbe I2p–K1–C5 (p. 68 : emmanchure devant I2K1C5, angle droit en C5)
76. **Dp** : depuis D, angle 0 = `#plat_enc_dos` (p. 68 : platitude 2 cm au milieu dos)
77. **Cp** : depuis C, angle 180 = `#plat_enc_dev` (p. 68 : platitude 1 cm au milieu devant)
78. **cEncDos** : courbe Dp–D2 (p. 68 : encolure dos, angle droit en D)
79. **cEncDev** : courbe Cp–C2 (p. 68 : encolure devant, angle droit en C)
80. **Ct** : depuis C, angle 270 = `#t_enc_dev` (p. 78 : milieu devant descendu de 2)
81. **C2t** : sur C2P1 = `#t_ouv_epaule` (p. 78 : encolure devant ouverte de 0,6 sur l'épaule)
82. **Dt** : depuis D, angle 270 = `#t_enc_dos` (p. 78 : milieu dos descendu de 0,1)
83. **D2t** : sur D2D3 = `#t_ouv_epaule` (p. 78 : encolure dos ouverte de 0,6 sur l'épaule)
84. **C5t** : sur P2C5 = `shoulder_length+#t_allong_epaule-(Line_C2_P1-#t_ouv_epaule)` (p. 78 : pince fermée, épaule devant = longueur d'épaule + 0,5 depuis la nouvelle encolure)
85. **L3t** : sur L4L3 = `shoulder_length+#t_allong_epaule-(Line_D2_D3-#t_ouv_epaule)` (p. 78 : pince fermée, épaule dos = longueur d'épaule + 0,5 depuis la nouvelle encolure)
86. **K1t** : depuis K1, angle 180 = `#t_carrure_dev` (p. 78 : carrure devant + 0,5)
87. **L1t** : depuis L1, angle 0 = `#t_carrure_dos` (p. 78 : carrure dos + 1)
88. **I2a** : depuis I2, angle 180 = `#t_dessous_bras` (p. 78 : dessous de bras élargi de 2, parallèle à la ligne de poitrine)
89. **I2t** : depuis I2a, angle 270 = `#t_descente_bras` (p. 78 : puis descendu de 1,75)
90. **J2a** : depuis J2, angle 0 = `#t_dessous_bras` (p. 78 : dessous de bras dos élargi de 2)
91. **J2t** : depuis J2a, angle 270 = `#t_descente_bras` (p. 78 : puis descendu de 1,75)
92. **M1t** : depuis M1, angle 0 = `#t_taille` (p. 78 : taille + 1,25)
93. **M2t** : depuis M2, angle 180 = `#t_taille` (p. 78 : taille + 1,25)
94. **A1t** : depuis A1, angle 0 = `#t_hanches` (p. 78 : hanches + 1,5)
95. **B1t** : depuis B1, angle 180 = `#t_hanches` (p. 78 : hanches + 1,5)
96. **cCoteDos** : courbe J2t–M1t–A1t (p. 80 : côté dos adouci en courbe légère)
97. **cCoteDev** : courbe I2t–M2t–B1t (p. 80 : côté devant, symétrique)
98. **J2tp** : depuis J2t, angle 180 = `#plat_emm_dos` (platitude 1 cm (comme la base))
99. **I2tp** : depuis I2t, angle 0 = `#plat_emm_dev` (platitude 2 cm (comme la base))
100. **cEmmDosT** : courbe J2tp–L1t–L3t (p. 80 : emmanchure dos retracée par les nouveaux points)
101. **cEmmDevT** : courbe I2tp–K1t–C5t (p. 80 : emmanchure devant retracée)
102. **Dtp** : depuis Dt, angle 0 = `#plat_enc_dos` (platitude 2 cm au milieu dos)
103. **Ctp** : depuis Ct, angle 180 = `#plat_enc_dev` (platitude 1 cm au milieu devant)
104. **cEncDosT** : courbe Dtp–D2t (p. 80 : nouvelle encolure dos)
105. **cEncDevT** : courbe Ctp–C2t (p. 80 : nouvelle encolure devant)
106. **Cemm** : sur L3tC5ta = `Line_L3t_C5ta/2` (T1 p. 144 : C = 1/2 AB, bouts d'épaule joints)
107. **bHc** : sur la courbe cCoteDos = `#bolero_sous_bras` (modèle : bas au côté dos, mesuré sur la couture de côté)
108. **bHc1** : sur la courbe cCoteDos = `#bolero_sous_bras-0.5` (tangente au côté (bas d'équerre avec le côté))
109. **bHc2** : sur la courbe cCoteDos = `#bolero_sous_bras+0.5` (tangente au côté)
110. **bHd** : depuis bHc, angle 180, jusqu'à LF1 (modèle : bas au milieu dos)
111. **bFc** : sur la courbe cCoteDev = `#bolero_sous_bras` (modèle : bas au côté devant, mesuré sur la couture de côté)
112. **bFc1** : sur la courbe cCoteDev = `#bolero_sous_bras-0.5` (tangente au côté)
113. **bFc2** : sur la courbe cCoteDev = `#bolero_sous_bras+0.5` (tangente au côté)
114. **bFm** : depuis bFc, angle 0, jusqu'à CtB (modèle : bas au milieu devant)
115. **bR1** : depuis bFm, angle 90 = `#bolero_arrondi` (modèle : départ de l'arrondi sur le milieu devant)
116. **bR2** : depuis bFm, angle 180 = `#bolero_arrondi` (modèle : fin de l'arrondi sur le bas)
117. **cArrondi** : courbe bR1–bR2 (modèle : devant arrondi, ouvert sans fermeture)
118. **cBasDos** : courbe bHd–bHc (modèle : bas d'équerre avec le milieu dos et avec le côté)
119. **cBasDev** : courbe bFc–bR2 (modèle : bas d'équerre avec le côté, raccordé à l'arrondi)
120. **mA** : Point de départ = `(75, -72)` (p. 150 : droit fil milieu de manche)
121. **mB** : depuis mA, angle 270 = `#long_manche+#epaulette` (p. 150 : AB = longueur de manche + épaulette)
122. **mC** : depuis mA, angle 270 = `Line_Cemm_J2t*7/8` (p. 150 : AC = hauteur d'emmanchure − son 1/8)
123. **mD** : depuis mA, angle 270 = `#haut_coude+#epaulette` (p. 150 : AD = 35 + épaulette)
124. **mE** : depuis mA, angle 180 = `0.7*(Line_J2t_J2tp+SplPath_J2tp_L3t)/2` (p. 150 : AE = 7/10 emmanchure dos : 2)
125. **mF** : depuis mA, angle 0 = `0.7*(Line_I2t_I2tp+SplPath_I2tp_C5t)/2` (p. 150 : AF = 7/10 emmanchure devant : 2)
126. **mEp** : depuis mB, angle 180 = `Line_mA_mE` (p. 150 : BE' = AE)
127. **mFp** : depuis mB, angle 0 = `Line_mA_mF` (p. 150 : BF' = AF)
128. **mG** : depuis mC, angle 180, jusqu'à mEmEp (p. 150 : G = segment C ∩ EE')
129. **mH** : depuis mC, angle 0, jusqu'à mFmFp (p. 150 : H = segment C ∩ FF')
130. **mI** : sur mEmG = `Line_mE_mG/2+1` (p. 150 : EI = 1/2 EG + 1)
131. **mIp** : sur mFmH = `Line_mF_mH/2+1` (p. 150 : FI' = 1/2 FH + 1)
132. **mIpp** : depuis mIp, angle 180 = `0.75` (p. 150 : I'I'' = 0,75)
133. **mJ** : depuis mH, angle 180 = `2.5` (p. 150 : HJ = 2,5)
134. **mJp** : depuis mH, angle 0 = `2.5` (p. 150 : HJ' = 2,5)
135. **mK** : depuis mJ, angle 90 = `#m_JK` (p. 150 : JK = 0,5 (à régler))
136. **mKp** : depuis mJp, angle 90 = `#m_JK` (p. 150 : J'K' = 0,5 (à régler))
137. **mL** : depuis mH, angle 90 = `#m_HL` (p. 150 : HL = 5 (à régler))
138. **mR** : depuis mD, angle 180, jusqu'à mEmEp (figure p. 151 : R = ligne de coude ∩ EE')
139. **mM** : depuis mD, angle 0, jusqu'à mFmFp (figure p. 151 : M = ligne de coude ∩ FF')
140. **mMp** : depuis mM, angle 180 = `5` (p. 150 : MM' = 5)
141. **mRp** : depuis mR, angle 180 = `1` (p. 152 : RR' = 1)
142. **mO** : depuis mFp, angle 90 = `2` (p. 150 : F'O = 2, sur FF' (figure p. 151))
143. **mW** : sur mRmO = `Line_mR_mO/2` (p. 152 : équerre en P passant par R et O (cercle de diamètre RO))
144. **mP** : cercle (mW, r) ∩ mEpmFp = `Line_mR_mO/2` (p. 152 : P sur le bas du cadre, angle droit RPO)
145. **mQ** : sur mPmO = `#bas_manche/2+2` (p. 152 : PQ = bas/2 + 2 (dessus))
146. **mQp** : sur mPmO = `#bas_manche/2-2` (p. 152 : PQ' = bas/2 − 2 (dessous))
147. **mS** : sur mEmG = `Line_mE_mG/4` (p. 152 : S = 1/4 EG)
148. **mT** : depuis mI, angle 90 = `#m_IT` (p. 152 : IT = 1 à 1,5)
149. **mU** : depuis mT, angle 180 = `2.5` (p. 152 : TU = 2,5)
150. **mUp** : depuis mT, angle 0 = `2.5` (p. 152 : TU' = 2,5)
151. **mX1** : sur mUmRp = `Line_mU_mRp/2` (p. 152 : moitié de R'U)
152. **mX1o** : perpendiculaire en mX1 à mX1mRp = `0.5` (p. 152 : ressortir de 0,5)
153. **mX2** : sur mUpmR = `Line_mUp_mR/2` (p. 152 : moitié de RU')
154. **mX2o** : perpendiculaire en mX2 à mX2mR = `0.5` (p. 152 : ressortir de 0,5)
155. **mV** : sur mCmJ = `Line_mC_mJ/2` (p. 152 : V = 1/2 CJ, cran de dessous de manche)
156. **mTete** : courbe mU–mS–mA–mIpp–mL–mKp (p. 152 : tête du dessus K'LI''ASU)
157. **mTeteDessous** : courbe mUp–mV (p. 152 : dessous U'V en s'appuyant sur U'C)
158. **mTeteDessous2** : courbe mV–mK (p. 152 : dessous VK, finir en légère courbe)
159. **mSaignee** : courbe mKp–mM–mQ (p. 152 : saignée du dessus K'MQ, angle droit en Q)
160. **mSaigneeD** : courbe mK–mMp–mQp (p. 152 : saignée du dessous KM'Q', angle droit en Q')
161. **mCoude** : courbe mU–mX1o–mRp–mP (p. 152 : coude du dessus UR'P, angle droit en P)
162. **mCoudeD** : courbe mUp–mX2o–mR–mP (p. 152 : coude du dessous U'RP)
163. **mCt** : sur la courbe mTete = `(SplPath_mU_mKp+SplPath_mUp_mV+SplPath_mV_mK)*(Line_J2t_J2tp+SplPath_J2tp_L3t)/((Line_J2t_J2tp+SplPath_J2tp_L3t)+(Line_I2t_I2tp+SplPath_I2tp_C5t))-SplPath_mUp_mV` (p. 152 : cran de tête, embu réparti devant et dos au prorata des emmanchures)
164. **mCc1** : sur la courbe mCoude = `SplPath_mU_mP-20` (p. 153 : cran de coude à 20 cm de P (dessus))
165. **mCc2** : sur la courbe mCoude = `20` (p. 153 : cran de coude à 20 cm de U (dessus))
166. **mCc3** : sur la courbe mCoudeD = `SplPath_mUp_mP-20` (p. 153 : cran de coude à 20 cm de P (dessous))
167. **mCc4** : sur la courbe mCoudeD = `20` (p. 153 : cran de coude à 20 cm de U' (dessous))
168. **mCs1** : sur la courbe mSaignee = `SplPath_mKp_mQ-20` (p. 153 : cran de saignée à 20 cm de Q (dessus))
169. **mCs2** : sur la courbe mSaignee = `15` (p. 153 : cran de saignée à 15 cm de K' (dessus))
170. **mCs3** : sur la courbe mSaigneeD = `SplPath_mK_mQp-20` (p. 153 : cran de saignée à 20 cm de Q' (dessous))
171. **mCs4** : sur la courbe mSaigneeD = `15` (p. 153 : cran de saignée à 15 cm de K (dessous))
172. **cranDev** : sur la courbe cEmmDevT = `SplPath_mV_mK*((Line_J2t_J2tp+SplPath_J2tp_L3t)+(Line_I2t_I2tp+SplPath_I2tp_C5t))/(SplPath_mU_mKp+SplPath_mUp_mV+SplPath_mV_mK)-Line_I2t_I2tp` (p. 152 : crans devant, en face de la saignée (embu réparti régulièrement, à confirmer sur la toile))
173. **cranDos** : sur la courbe cEmmDosT = `SplPath_mUp_mV*((Line_J2t_J2tp+SplPath_J2tp_L3t)+(Line_I2t_I2tp+SplPath_I2tp_C5t))/(SplPath_mU_mKp+SplPath_mUp_mV+SplPath_mV_mK)-Line_J2t_J2tp` (p. 152 : cran dos, en face de la ligne de coude (à confirmer sur la toile))
