# Pyjama : adaptations à partir des fonds du dépôt

Objectif : un haut T-shirt **col V** et un **pantalon** à taille élastique, en **jersey**.
Rien n'est tracé tant que les questions ne sont pas tranchées (chaîne `lire-patronage` →
`.etapes.md` validé → `tracer-sm2d`).

## Sources disponibles

| Pièce | Base tracée | Pages du livre transcrites |
|---|---|---|
| Haut | `patrons/fond_base_maille.sm2d` (devant, dos, manche ; embu 1,43 à régler) | encolure V en bande jersey (`col/encolure-v-bande-jersey/`) |
| Pantalon | `patrons/fond_pantalon_droit.sm2d` (T44, vérifié) | élargissements p. 244-245, pantalon souple p. 246-247, jogging jersey (`pantalon/jogging-jersey/`) |

## 1. T-shirt col V

Étapes détaillées et questions : `patrons/tshirt_col_v.etapes.md`. En résumé, sur le fond de
base maille :
1. dégager le point d'encolure H de 3 cm le long de l'épaule (devant et dos) ;
2. descendre le milieu dos de 2 cm, retracer l'encolure dos en courbe ;
3. descendre le milieu devant de 13 cm sous E, encolure devant en droite ;
4. retirer la largeur de la bande (≤ 1,5 cm en jersey) ;
5. bande jersey pliée en deux : rectangle 1/2 encolure × largeur finie, pointe en onglet piquée
   au milieu devant, milieu dos au pli ; couture 0,7.
Valeurs 3 / 2 / 13 : exemples du livre.

## 2. Pantalon : trois modèles possibles

Les trois partent du fond droit (devant et dos superposés, sans ouverture : passe les hanches en
jersey) ; couturages 0,7, ourlet 2,5.

| | a) Souple p. 246 | b) Jogging | c) Droit + ceinture du jogging |
|---|---|---|---|
| Jambe | élargie (p. 244 : enfourchure +1-2,5 / −1-3, côtés libres) | amincie : genou 42, bas 34 | fond tel quel (genou 48, bas 40), élargissements p. 244 en option |
| Bas | ourlet 2,5 | bord-côtes 6 cm, AB = 3/4 du bas | ourlet 2,5 |
| Taille | descendue de 2, ceinture **p. 256 manquante** | descendue de 3, ceinture bord-côtes AB = 3/4 × 1/2 taille, ou jersey AB = 1/2 taille ; hauteur (4 + 0,5) × 2 | comme b |
| Poches | oui | oui (option) | non |
| Source complète | non (p. 256) | oui | oui (assemblage de b et du fond) |

Avec b, le patron change très peu : `#larg_genou` = 42 et `#larg_bas_pant` = 34 (variables du
fond), une ligne de taille à 3 cm, une coupe à 6 cm du bas, puis deux rectangles.

Point d'attention hérité du fond : côté dos évasé de B4 à B5 en T44 (`waist_circ` 76 à vérifier).

## Décisions

- 2026-10-07 : matière → jersey.
- 2026-10-07 : base du pantalon → `patrons/fond_pantalon_droit.sm2d` (branche
  `claude/recuperer-skills-vavt5l`, fusionnée ici).
- 2026-10-07 : encolure V → méthode du livre (bande jersey piquée milieu devant).

## Questions ouvertes

1. Modèle de pantalon : a, b ou c ? Recommandation : **c** pour un pantalon « normal » (jambe
   droite, ourlet) ; **b** si un bas resserré en bord-côtes convient. a n'est complet qu'avec la
   p. 256.
2. Ceinture : bord-côtes (3/4) ou jersey du pyjama (1/2, note du livre) ?
3. Élargissements p. 244 : oui / non, et valeurs.
4. Haut : manche longue ou courte ?
5. Questions du col V : `patrons/tshirt_col_v.etapes.md`.
6. Numéros des pages jogging et encolure V.
