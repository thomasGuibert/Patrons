# Bas de pyjama (pantalon souple, ceinture jersey) : étapes

Sources (transcriptions à côté des photos) :
- `doc/sources/pantalon/fond-pantalon-droit/` : fond tracé dans `patrons/fond_pantalon_droit.sm2d` ;
- `doc/sources/pantalon/elargissements/` : élargissements (p. 244-245) ;
- `doc/sources/pantalon/modele-pantalon-souple/` : modèle souple (p. 246-247) ;
- `doc/sources/pantalon/jogging-jersey/` : ceinture élastiquée, note « ceinture en jersey ».
Fichier cible : `patrons/bas_pyjama.sm2d`, copie de `fond_pantalon_droit.sm2d` (décision) — en cm. Mesures : `mesures/T44.smms`.

Ordre du livre (p. 246) : fond droit devant et dos superposés → élargissements (p. 244) →
descendre la taille → (poches) → ceinture sur la 1/2 taille descendue → coutures, ourlets, crans.

Conventions : points du fond (gauche = côté, droite = entrejambe ; devant indices 1-2-3, dos
3-4-5, voir `fond_pantalon_droit.etapes.md`). Nouveaux points suffixés `e` (élargis) ou préfixés
`c` (ceinture).

## Entrées
- Points hérités (fond) : devant A3, A2, B1, B2, C1, C2, D1, D2, E1, E2 ; dos A5, B5, B3, B4, C4,
  C5, D3, D4, E3, E4 ; courbes d'enfourchure C2B2, C5B3 et de taille PlatA3-A2, A5-RenA5B5-B5.
- Variables :
  - Élargissements (p. 244, valeurs à choisir dans les plages du livre, question 3) :
    `#el_enf_h` (1 à 2,5), `#el_enf_v` (1 à 3), `#el_taille_cote` = 0,5, `#el_A`, `#el_B`,
    `#el_C` (côté au montant, au genou, au bas : non chiffrés par le livre).
  - `#desc_taille_pyj` = 2 (p. 247, lu sur le schéma).
  - Ceinture (page jogging) : `#haut_elastique` = 4 (exemple), ceinture jersey
    AB = 1/2 tour de taille, AC = (`#haut_elastique` + 0,5) × 2.

## Étapes
### 1. Élargissements (p. 244-245)
1. Pointe d'enfourchure devant C2e : C2 + `#el_enf_h` vers l'entrejambe, puis `#el_enf_v` vers le bas ; dos C5e : idem depuis C5
2. Taille côté : A2e = A2 + `#el_taille_cote` vers le côté ; dos B5e = B5 + `#el_taille_cote`
3. Côté : C1e, D1e, E1e (devant) et C4e, D3e, E3e (dos) = points du fond + `#el_A`, `#el_B`, `#el_C` vers le côté
4. Entrejambe : D2e, E2e, D4e, E4e selon la question 4 (symétrie des jambes)
5. Retracer l'enfourchure B2 → C2e (devant) et B3 → C5e (dos), milieux devant et dos inchangés
6. Retracer les côtés en aplatissant la hanche, sans bosse avec la jambe ; retracer les jambes
   « symétriquement en suivant les courbes du fond »
7. Contrôles du livre : entrejambes devant / dos assemblés (continuité de l'enfourchure), côtés
   devant / dos assemblés (forme de la taille)

### 2. Taille descendue (p. 247)
8. Nouvelle ligne de taille devant et dos, parallèle à l'ancienne à `#desc_taille_pyj` dessous :
   points cA3 (milieu devant), cA2e (côté devant), cA5 (milieu dos), cB5e (côté dos), sur les
   milieux et les côtés retracés ; courbes de taille retracées

### 3. Poches (p. 246-247) : non tracées (décision)

### 4. Ceinture en jersey (page jogging, note)
9. Mesurer la 1/2 taille descendue : courbe devant + courbe dos (étape 8)
10. Rectangle ABDC : AB = 1/2 tour de taille (étape 9), AC = (`#haut_elastique` + 0,5) × 2 ;
    ceinture entière par symétrie sur DB ; pliure à mi-hauteur
11. Élastique : longueur finie + 2 cm (longueur finie à mesurer sur la personne)

### Pièces
12. Devant ×2, Dos ×2, Ceinture ×1. Couture 0,7 ; ourlet 2,5 ; crans de
    montage (milieux, côtés de la ceinture).

## Contrôles
- Entrejambes devant / dos : écart à mesurer (0,92 sur le fond, décision 19 du fond).
- Côtés devant / dos : même longueur.
- Tour de taille descendue ≥ tour de hanches du corps ? (pas d'ouverture : en jersey le livre
  l'admet, à vérifier sur la personne).

## Décisions
- 2026-10-07 : modèle → pantalon souple p. 246 (élargissements p. 244), plus ample que le fond
  droit pour un pyjama ; la ceinture de la p. 256 (absente) est remplacée par celle du jogging.
- 2026-10-07 : ceinture → **même jersey que le pyjama** (note de la page jogging : AB = 1/2 tour
  de taille, AC = (hauteur élastique + 0,5) × 2), pas de bord-côtes.

- 2026-10-07 : fichier → `patrons/bas_pyjama.sm2d`, copie du fond (comme le haut, sans objection).
- 2026-10-07 : poches → sans.

## Questions ouvertes
1. ~~Fichier cible~~, 2. ~~Poches~~ : tranchées (voir Décisions).
3. Valeurs d'élargissement : enfourchure (1-2,5 / 1-3) et côtés A, B, C.
4. Entrejambe : élargi comme le côté (jambe « symétrique ») ou inchangé ?
5. Hauteur de l'élastique : 4 cm (exemple du livre) ?
