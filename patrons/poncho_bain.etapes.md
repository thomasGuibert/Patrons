# Poncho de bain : étapes

Demande d'Amélie (issue #89) : un poncho pour se sécher et se changer à l'abri des regards (plage,
bateau après une plongée), ample, avec poche kangourou, ouvertures sur les côtés pour passer les
mains, manches au coude et capuche qui tienne ; gamme de montage, métrage, tailles XS à XL et
longueurs petit, normal, grand. Elle a joint deux patrons du commerce comme exemples : ce patron-ci
n'en est pas une copie, il est construit sur les mesures du tableau femme.

Généré par `outils/poncho/build.py`. Matière : éponge de coton (tissée, bouclée) ; aucune base de
maille n'est utilisée. Tailles **XS, S, M, L, XL = femme 36, 38, 40, 42, 44** (noms dans
`patrons/poncho_bain.dossier.toml` et `src/patrons.ts`). Les trois longueurs sont dans le même
patron : le bas du devant et du dos pour grand, deux traits intérieurs pour normal et petit (lignes
de coupe, ourlet compris). PDF : `toutes_tailles.py --gamme femme poncho_bain`.

## Choix de modèle (à valider à l'essayage)

| Variable | Valeur (M) | Pourquoi |
| --- | --- | --- |
| `#tour_max` | max(poitrine, hanches) = 98 | Le poncho doit passer aux deux. |
| `#aisance` | 64 cm | De quoi se changer dessous, bras rentrés : tour du poncho 162 cm. |
| `#demi_larg` | (tour + aisance) / 4 = 40,5 | Devant et dos au pli. |
| `#evase` | 4 cm | Évasement du côté jusqu'au bas. |
| `#pente` | 3 cm | Pente d'épaule, de l'encolure au bord. |
| `#larg_enc` | encolure / 6 + 2,5 | Encolure élargie pour la capuche. |
| `#prof_enc_dev`, `#prof_enc_dos` | encolure / 6 + 4 ; 4,5 | Encolure dos assez creusée pour une courbe sans cassure. |
| `#emman` | poitrine / 8 + 13,5 = 25 | Demi-tour de manche (manche de 50 cm de tour). |
| `#long_manche` | coude + 2 − débord du devant = 15,6 | Le devant couvre déjà le haut du bras ; la manche finit au coude. |
| `#long_petit / normal / grand` | genou − 22 ; − 8 ; + 8 (84,5 ; 98,5 ; 114,5) | Depuis l'épaule : mi-cuisse, au-dessus, sous le genou. |
| `#ouv_haut`, `#ouv_long` | taille dos − 4 ; 24 cm | Ouverture de côté à hauteur des mains. |
| `#poche_*` | sous la taille, 26 cm de haut, 40 cm en bas | Poche kangourou, entrées de mains en biais de 17 cm. |
| `#haut_cap`, `#prof_cap` | stature × 0,21 ; encolure × 0,75 | Capuche 35,7 × 27,8 cm, coulisse et cordon pour qu'elle tienne. |

## Devant et dos (au pli)

1. O milieu, à hauteur d'épaule ; Fn milieu d'encolure ; E encolure à l'épaule ; X demi-largeur ;
   Ep sous X de la pente ; Em sous Ep de `#emman` (cran de dessous de bras).
2. Hc milieu du bas (longueur grand), H côté du bas évasé ; côté Em H.
3. Ou1, Ou2 sur Em H : crans de l'ouverture de côté.
4. Encolure Fn E : horizontale au milieu, d'équerre sur l'épaule.
5. Lignes de coupe normal et petit (`coupe_normal`, `coupe_petit`) : longueur + ourlet, du milieu
   au côté.
6. Devant seulement : emplacement de la poche (Q0 à Q4).

## Manche (×2, au pli sur le dessus du bras)

mA mB = `#emman` (bord d'emmanchure : moitié sur le devant, moitié sur le dos), mA mC = longueur,
bas resserré de 2 cm.

## Capuche (×2)

cA cB = encolure devant + dos (cran cE à la couture d'épaule) ; cA cF = bord du visage ; milieu dos
cF–cR–cB horizontal au sommet, vertical à l'arrière, rentrant vers la nuque.

## Poche kangourou (au pli)

Haut pK0 pK1, entrée de main pK1 pK2 en biais, côté et bas.

## Coutures

1 cm partout ; 3 cm à l'ourlet du bas et des manches ; 3,5 cm au bord du visage (coulisse de 2,5 cm
pour un cordon de 8 à 10 mm) ; 2,5 cm aux entrées de poche ; 0 au pli.

## Contrôles

`python3 outils/coherence/coherence.py poncho_bain` : épaules, côtés et crans d'ouverture, manche
sur devant et dos, capuche sur encolure à 0,00 cm ; encolure et milieu dos de capuche sans angle.
