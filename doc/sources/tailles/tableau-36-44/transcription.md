# Tableau des tailles 36 à 44 : transcription

Source : `p29-tableau-tailles.jpg` (même livre que les fonds, p. 29), envoyée par Thomas le
2026-10-10. Intitulés en italien / indonésien / chinois recopiés tels quels. Unité : cm.
« Évolution de taille » = écart d'une colonne à la suivante (2 points de taille).

| N° | Mesure | Évol. | 36 | 38 | 40 | 42 | 44 |
|---|---|---|---|---|---|---|---|
| 1 | Lunghezza vita-parte posteriore - Panjang Punggung - 背长 | 0.5 | 40.5 | 41 | 41.5 | 42 | 42.5 |
| 2 | Lunghezza vita-parte anteriore - Panjang Dada - 前长 | 0.5 | 36.5 | 37 | 37.5 | 38 | 38.5 |
| 3 | Circonferenza torace - Lingkar dada - 胸围 | 4 | 84 | 88 | 92 | 96 | 100 |
| 4 | Altezza torace - Tinggi dada - 胸高 | 0.5 | 21.5 | 22 | 22.5 | 23 | 23.5 |
| 5 | 1/2 Distanza seni - 1/2 Lebar dada - 1/2 胸距 | 0.25 | 9 | 9.25 | 9.5 | 9.75 | 10 |
| 6 | Circonferanza vita - Lingkar pinggang - 腰围 | 4 | 64 | 68 | 72 | 76 | 80 |
| 7 | Circonferanza addome - Lingkar panggul kecil - 腹围 | 4 | 81 | 85 | 89 | 93 | 97 |
| 8 | Circonferanza bacino - Lingkar panggul besar - 臀围 | 4 | 90 | 94 | 98 | 102 | 106 |
| 9 | Circonferanza collo - Lingkar leher - 领围 | 1 | 35 | 36 | 37 | 38 | 39 |
| 10 | 1/2 Spalle parte posteriore - 1/2 Lebar punggung - 1/2 背宽 | 0.25 | 17.25 | 17.5 | 17.75 | 18 | 18.25 |
| 11 | 1/2 Spalle parte anteriore - 1/2 Lebar dada - 1/2 前宽 | 0.25 | 16.25 | 16.5 | 16.75 | 17 | 17.25 |
| 12 | Lunghezza spalla - Panjang bahu - 小肩宽 | 0.4 | 11.6 | 12 | 12.4 | 12.8 | 13.2 |
| 13 | Giro manico - Lingkar kerung lengan - 袖窿围 | 1 | 38.5 | 39.5 | 40.5 | 41.5 | 42.5 |
| 14 | Altezza vita-sottomanica - Pinggang ketiak - 袖根至腰围长 | 0.25 | 21.25 | 21.5 | 21.75 | 22 | 22.25 |
| 15 | Lunghezza braccio - Panjang lengan - 臂长 | 0 | 60 | 60 | 60 | 60 | 60 |
| 16 | Circonferenza braccio - Lingkar lengan - 臂围 | 1 | 25 | 26 | 27 | 28 | 29 |
| 17 | Lunghezza al gomito - Tinggi siku - 肘高 | 0 | 35 | 35 | 35 | 35 | 35 |
| 18 | Circonferenza polsino - Lingkar pergelangan - 胸围 | 0.25 | 15.75 | 16 | 16.25 | 16.5 | 16.75 |
| 19 | Altezza vita-bacino - Pinggang ke panggul besar - 臀高 | 0 | 22 | 22 | 22 | 22 | 22 |
| 20 | Altezza fianchi di profilo - Tinggi duduk - 立档长 | 0.5 | 26 | 26.5 | 27 | 27.5 | 28 |
| 21 | Altezza cavallo - Ukuran pesak - 横档长 | 2 | 58 | 60 | 62 | 64 | 66 |
| 22 | Altezza ginocchio - Tinggi lutut - 膝高 | 1 | 57 | 58 | 59 | 60 | 61 |
| 23 | Lunghezza vita-terra - Pinggang ke lantai - 前下半身长 | 1 | 105 | 105 | 106 | 106 | 107 |
| 24 | Altezza laterale vita-terra - Pinggang Samping ke lantai - 侧下半身长 | 1 | 105.5 | 105.5 | 106.5 | 106.5 | 107.5 |

Aucune cellule douteuse : la photo est nette et chaque ligne suit exactement son évolution,
sauf les lignes 23 et 24, qui montent de 1 toutes les deux colonnes (le tableau l'écrit ainsi).

## Traduction en mesures Seamly (`mesures/T36.smms` à `T44.smms`)

| Ligne | Nom Seamly | Formule | T44 avant → après |
|---|---|---|---|
| 3 | `bust_circ` | ligne 3 | 88 → 100 |
| 6 | `waist_circ` | ligne 6 | 76 → 80 |
| 8 | `hip_circ` | ligne 8 | 90 → 106 |
| 1 | `neck_back_to_waist_b` | ligne 1 | 44,1 → 42,5 |
| 2 | `neck_front_to_waist_f` | ligne 2 | 39,9 → 38,5 |
| 9 | `neck_circ` | ligne 9 | 38 → 39 |
| 10 | `across_back_b` | 2 × ligne 10 (le fond trace DD2 = 1/2 carrure dos) | 37 → 36,5 |
| 11 | `across_chest_f` | 2 × ligne 11 | 32 → 34,5 |
| 12 | `shoulder_length` | ligne 12 | 13,7 → 13,2 |
| 15 | `arm_shoulder_tip_to_wrist` | ligne 15 | 64 → 60 |
| 18 | `arm_wrist_circ` | ligne 18 | 17,2 → 16,75 |
| 24 | `height_waist_side` | ligne 24 (incrément 0,5 en moyenne) | 112,1 → 107,5 |
| 19 | `height_waist_side_to_hip` | ligne 19 | 20 → 22 |
| 20 | `rise_length_side_sitting` | ligne 20 | 27,1 → 28 |
| 22 | `height_waist_side_to_knee` | ligne 22 | 62 → 61 |
| 20, 24 | `leg_crotch_to_floor` | ligne 24 − ligne 20 (le montant vaut la ligne 20, cf. lexique) | 85 → 79,5 |

Hors tableau, déduites de l'ancien T44 avec ses incréments (aucun patron ne les utilise) :
`neck_back_to_waist_front`, `height_neck_back`, `crotch_length`, `leg_thigh_upper_circ`,
`leg_calf_circ`, `leg_knee_circ`. `height` reste à 170 (Seamly refuse une stature hors liste).

Lignes du tableau sans place dans les fichiers (aucun patron ne les utilise) : 4, 5, 7, 13, 14,
16, 17, 21, 23.

## Variable de vêtement à revoir

`#garde_sol` (12 cm entre le bas du pantalon et le sol) est fixe. Avec la hauteur taille-sol du
tableau, le pantalon fait 93,5 cm en T38, alors que le livre donne une hauteur de pantalon de
100 en T38 (p. 239). Laissé tel quel en attendant la décision de Thomas.
