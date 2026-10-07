# Pyjama : adaptations à partir des fonds du dépôt

Objectif : un haut T-shirt **col V** et un **pantalon** à taille élastique, en **jersey**.
Rien n'est tracé tant que les questions ne sont pas tranchées (chaîne `lire-patronage` →
`.etapes.md` validé → `tracer-sm2d`).

## Sources disponibles

| Pièce | Base tracée | Pages du livre transcrites |
|---|---|---|
| Haut | `patrons/fond_base_maille.sm2d` (devant, dos, manche ; embu 1,43 à régler) | élargissements maille p. 56-57, épaule p. 48-49, T-shirt liquette p. 60-61, encolure V, crans p. 72 |
| Pantalon | `patrons/fond_pantalon_droit.sm2d` (T44, vérifié) | élargissements p. 244-245, pantalon souple p. 246-247, jogging jersey (`pantalon/jogging-jersey/`) |

## 1. Haut : T-shirt col V

Étapes détaillées et questions : `patrons/haut_pyjama.etapes.md`. Le livre enchaîne (p. 60,
T-shirt liquette) :
1. élargir le fond pour un T-shirt souple (p. 56 : épaule +0,5, carrure +0,5, dessous de bras
   +1,5 et −1,5, taille +0,5, bas +1) ;
2. encolure V (3 à l'épaule, −2 au dos, −13 au devant ; bande jersey ≤ 1,5, pointe en onglet) ;
3. déplacer la ligne d'épaule de 1,8 vers l'avant (p. 48) ;
4. prolonger le milieu devant de 1 à 1,5 vers le bas ;
5. **manche reconstruite sur la nouvelle emmanchure** (même méthode p. 68-71, le bloc Manche
   existant suit en changeant les courbes lues), crans p. 72 avec le cran de tête décalé de 1,8 ;
6. couture 0,7, ourlet 2,5.
Valeurs : exemples du livre.

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
5. Questions du haut : `patrons/haut_pyjama.etapes.md`.
6. Numéros des pages jogging et encolure V.
