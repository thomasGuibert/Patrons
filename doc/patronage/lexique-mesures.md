# Lexique des mesures : livre → Seamly2D

Correspondance entre les termes du livre et les noms de mesures Seamly (`mesures/*.smms`) ou
les variables du patron (`#nom`). Un terme absent = question à l'utilisateur, puis nouvelle
ligne ici. Statut : **validé** (décidé avec l'utilisateur) ou **proposé** (à confirmer).

## Mesures du corps

| Terme du livre | Seamly | Statut | Remarque |
|---|---|---|---|
| Tour de taille | `waist_circ` | proposé | |
| Tour de hanches | `hip_circ` | proposé | T44.smms : 90, plus petit que le T38 du livre (92) : fichier à revoir ? |
| Tour de genou | `leg_knee_circ` | proposé | non utilisé par le fond de pantalon droit |
| Hauteur taille-hanches | `height_waist_side_to_hip` | validé | fond de pantalon droit |
| Hauteur taille-montant | `height_waist_side - leg_crotch_to_floor` | validé | montant mesuré debout (pas `rise_length_side_sitting`) |
| Hauteur taille-genou | `height_waist_side_to_knee` | validé | fond de pantalon droit |
| Hauteur pantalon | `#haut_pantalon` = `height_waist_side - #garde_sol` | validé | longueur de vêtement ; `#garde_sol` = 12 (100,1 en T44, livre 100 en T38) |
| Longueur de manche | `arm_shoulder_tip_to_wrist` | validé | manche montée |
| Tour de poignet | `arm_wrist_circ` | validé | manche montée |
| Tour d'emmanchure devant + dos | `(SplPath_K_C3+SplPath_K_C3_1)` | validé | mesuré sur les courbes du fond de base maille (formule dans l'outil, pas en variable) |
| Profondeur d'emmanchure | `Line_C2_K1` | validé | méthode vidéo, voir `doc/sources/manche/profondeur-emmanchure/` |

## Valeurs de vêtement (variables du patron)

| Terme du livre | Variable | Valeur | Statut |
|---|---|---|---|
| Largeur de manche = fraction du tour d'emmanchure | `#frac_largeur` | 3/4 | validé (écart FR 1/3 / EN 3/4) |
| Hauteur du coude | `#haut_coude` | `#long_manche*35/60` | validé |
| Largeur du bas de manche | `#larg_bas` | `arm_wrist_circ+#aisance_poignet` (2,8) | validé |
| Largeur du genou (pantalon) | `#larg_genou` | 48 | validé |
| Largeur du bas de pantalon | `#larg_bas_pant` | 40 | validé |
| Aisance taille (pantalon) | `#aisance_taille` | 4 | validé |
| Taille descendue (pantalon) | `#descente_taille` | 4 | validé |
| Aisance hanches (pantalon) | `#aisance_hanches` | 2 | validé |

## Fichiers de mesures

- `mesures/T44.smms` (cm) : utilisé par `patrons/fond_base_maille.sm2d`. Ne contient ni tour
  ni profondeur d'emmanchure, ni tour de bras, ni largeur genou/bas de vêtement.
