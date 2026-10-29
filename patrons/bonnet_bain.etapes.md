# Bonnet de bain cheveux longs : étapes

Demande d'Amélie (issue #83) : « un bonnet de bain en maille pour cheveux longs ». La photo
jointe montre un patron du commerce (bande centrale au pli et deux côtés). Ce patron-ci n'en
est pas une copie : il est construit à partir du tour de tête, avec la même idée de montage en
trois pièces, et de la place en plus à l'arrière pour les cheveux.

Généré par `outils/bonnet/build.py`. Gamme femme, tailles 36 à 44 ; le tour de tête
(`head_circ`) a été ajouté aux fichiers `mesures/femme/T*.smms` : 54 à 58 cm, 1 cm par taille.

## Choix de modèle (à valider à l'essayage)

| Variable | Valeur | Pourquoi |
| --- | --- | --- |
| `#reduction` | 0,9 | Maille de bain : le bord fait 90 % du tour de tête, pour tenir sans serrer. |
| `#larg_bande` | 10 cm | Bande centrale du front à la nuque. |
| `#bas_cote` | (tour × 0,9 − 2 × 10) / 2 | Le bord du bonnet = 2 bouts de bande + 2 bas de côté. |
| `#haut_cote` | tour × 0,19 | Du bord au-dessus de l'oreille jusqu'à la bande (10,6 cm en 40). |
| `#volume` | 4 cm | Cheveux longs : le côté déborde en arrière de la nuque. |
| `#haut_volume` | 0,45 × hauteur | Hauteur du volume arrière. |
| `#pos_sommet` | 0,4 × bas | Sommet du côté, plus près du front que de la nuque. |

## Côté (×2, en symétrie)

1. A : bord, côté front. AB = `#bas_cote`, bord du bonnet jusqu'à la nuque.
2. S0 sur AB à `#pos_sommet` ; S au-dessus de S0 à `#haut_cote` (sommet, cran).
3. R0 : AB prolongé de `#volume` ; R au-dessus de R0 à `#haut_volume`.
4. Courbe A–S : part d'équerre du bord en A, arrive à l'horizontale en S.
5. Courbe S–R–B : horizontale en S, verticale en R, d'équerre sur le bord en B.

## Bande centrale (×1, au pli)

1. bA bB, au pli = longueur de la couture du côté (A–S–B).
2. Demi-largeur `#larg_bande / 2` aux deux bouts.
3. Cran bS à la longueur de A–S depuis le front : il tombe sur le cran S du côté.

## Coutures

0,6 cm sur les coutures ; 1 cm au bord du bonnet (rabattu et piqué au zigzag ou à la
recouvreuse, avec ou sans élastique fin) ; 0 au pli.

## Contrôles

- Couture côté / bande : 0,00 cm d'écart dans toutes les tailles
  (`python3 outils/coherence/coherence.py bonnet_bain`).
- Couture A–S–B sans angle ; angles droits au bord en A et B, et aux bouts de bande.
- En 40 : bande 35,6 cm de long, côté 19,2 × 10,6 cm, bord du bonnet 50,4 cm pour une tête de 56.
