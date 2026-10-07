# Haut de pyjama (T-shirt col V) : étapes

Sources (transcriptions à côté des photos) :
- `doc/sources/buste/elargissements-maille/` : élargissement T-shirt souple (p. 56) ;
- `doc/sources/col/encolure-v-bande-jersey/` : encolure V en bande jersey (pages à confirmer) ;
- `doc/sources/buste/deplacement-epaule/` : déplacement de la ligne d'épaule (p. 48-49) ;
- `doc/sources/buste/tshirt-liquette/` : enchaînement d'un T-shirt complet (p. 60-61) ;
- `doc/sources/manche/manche-montee/` : manche (p. 68-71) et crans (p. 72).
Fichier cible : `patrons/haut_pyjama.sm2d`, copie de `fond_base_maille.sm2d` (décision 1) — en cm. Mesures : `mesures/T44.smms`.

Ordre du livre (p. 60) : élargissements → côté → emmanchure → encolure → épaule → milieu devant →
bas → manche sur la nouvelle emmanchure → crans, coutures, ourlets.

Conventions : points du fond de base maille (devant et dos superposés, axe = milieux devant et
dos, haut vers X). Nouveaux points préfixés `v` (noms uniques dans le fichier, comme `m` pour la
manche). Côté = vers la droite du fond (C1, D1…), « extérieur » = en s'éloignant de l'axe.

## Entrées
- Points hérités (bloc « Fond de base maille ») : H (point d'encolure à l'épaule), K (bout
  d'épaule), D, D1 (carrure devant), D2 (carrure dos), C2 (côté, dessous de bras), C3 (fin de la
  platitude d'emmanchure), B1 (taille, côté), A1 (bas, côté), E (milieu devant, encolure), F
  (milieu dos, encolure), A (milieu, bas). Segment H→K existant.
- Bloc « Manche » : il lit le tour d'emmanchure sur les courbes du fond (`SplPath_K_C3`,
  `SplPath_K_C3_1`) ; il devra lire les **nouvelles** courbes (étape 20).
- Variables (toutes des exemples du livre, réglables) :
  - Corps (p. 56) : `#el_epaule` = 0,5 ; `#el_carrure` = 0,5 ; `#desc_carrure` = 0,75 ;
    `#el_dessous_bras` = 1,5 ; `#desc_dessous_bras` = 1,5 ; `#el_taille` = 0,5 ; `#el_bas` = 1.
  - Encolure V : `#degag_epaule` = 3 ; `#desc_dos` = 2 ; `#desc_devant` = 13 ;
    `#larg_bande` = 1,5 (maximum du livre).
  - Épaule (p. 48) : `#decal_epaule` = 1,8.
  - Devant (p. 60) : `#prolong_devant` = 1,5 (« 1 à 1,5 »).
  - Manche : `#long_manche` existant (longue) ; courte : question 6.

## Étapes
### 1. Élargissement du corps (p. 56)
1. vK : point sur une droite — prolonger H→K au-delà de K de `#el_epaule` (longueur `Line_H_K + #el_epaule`)
2. vD : point sur une droite — sur l'axe, D descendu de `#desc_carrure`
3. vD1, vD2 : perpendiculaires à l'axe depuis vD — `Line_D_D1 + #el_carrure`, `Line_D_D2 + #el_carrure`
4. vC2 : point à distance depuis C2 — `#el_dessous_bras` vers l'extérieur (perpendiculaire à l'axe) puis `#desc_dessous_bras` vers le bas (deux gestes : point d'aide `vC2a`, puis vC2)
5. vB1 : perpendiculaire à l'axe en B — `Line_B_B1 + #el_taille`
6. vA1 : perpendiculaire à l'axe en A — `Line_A_A1 + #el_bas`
7. Côté : courbe vC2 – vB1 – vA1 « en courbes harmonieuses » (poignées : réglage)
8. Platitudes d'emmanchure en vC2, perpendiculaires au côté : vC3d (devant) = 1,5 ; vC3b (dos) = 1 [p. 56]
9. Emmanchure devant : courbe vK – vD1 – vC3d ; emmanchure dos : courbe vK – vD2 – vC3b

### 2. Encolure V (remplace l'élargissement d'encolure de la p. 56, décision du 2026-10-07)
10. vH : sur H→K, HvH = `#degag_epaule`
11. vF : sur l'axe F→A, FvF = `#desc_dos` ; vE : sur l'axe E→A, EvE = `#desc_devant`
12. Encolure dos : platitude perpendiculaire au milieu dos depuis vF, puis courbe jusqu'à vH
13. Encolure devant : droite vH → vE
14. Retirer la largeur de bande (décision 3) : 3 / 2 / 13 = ligne finie ; lignes de couture décalées
    de `#larg_bande` vers l'extérieur : vH2 sur H→K à `#degag_epaule + #larg_bande` de H ; vF2 sur
    l'axe à `#desc_dos + #larg_bande` de F ; vE2 = intersection de l'axe et de la parallèle à vH–vE
    décalée de `#larg_bande` vers l'extérieur. Courbe dos vH2→vF2 (avec platitude), droite vH2→vE2.
    Les étapes 15 à 17 et la bande partent de ces lignes de couture.

### 3. Déplacement de l'épaule (p. 48)
15. vHp, vKp : parallèle à vH–vK côté devant à `#decal_epaule`, intersections avec l'encolure devant
    (droite vH2–vE2) et l'emmanchure devant (courbe vK–vD1–vC3d) [p. 48, fig. 1 ; côté devant,
    décision 4]
16. vHpp, vKpp : symétriques de vHp, vKp par rapport à vH–vK (côté dos) [p. 48, fig. 2]
17. Pièce Devant : épaule vHp–vKp ; pièce Dos : épaule vHpp–vKpp, angles adoucis au bout d'épaule
    et à l'encolure [fig. 3]

### 4. Milieu devant et bas (p. 60)
18. Devant : prolonger le milieu devant vers le bas de `#prolong_devant` (vA), bas devant retracé
    de vA à vA1 avec platitude perpendiculaire au milieu ; dos : bas droit A–vA1
19. Bas : droit (pyjama) ; la liquette (point à 4 cm sur le côté, deux courbes inversées) n'est
    pas reprise (question 5)

### 5. Manche (p. 60 fig. 2, p. 68-72)
20. Manche de base reconstruite sur la nouvelle emmanchure : les formules du bloc « Manche » lisent
    l'emmanchure devant + dos des étapes 9 et 15-17 (au lieu de `SplPath_K_C3` et
    `SplPath_K_C3_1`) et la nouvelle profondeur d'emmanchure (`prof_emm`, méthode vidéo, depuis
    vC2) ; même construction, mêmes variables (`#frac_largeur` 3/4…)
21. Longueur : `#long_manche` (longue) ou courte (question 6) ; bas perpendiculaire au milieu
22. Contrôle embu (0,5 à 1 attendu ; 1,43 sur le fond actuel) : à reprendre sur la nouvelle
    emmanchure (question 7)
23. Crans [p. 72] : emmanchure dos 1 cran à 7 de la couture de côté ; devant 2 crans à 8 et 9 ;
    manche : dos 7 + 1/2 embu depuis I, devant 8 + 1/2 embu depuis I' et 1 cm plus loin ; cran de
    tête **décalé de `#decal_epaule`** depuis E (épaule déplacée) ; longueur des crans 0,4

### 6. Bande d'encolure (fig. 2-4 de l'encolure V), bloc séparé
24. vbA départ ; vbB à 1/2 encolure (dos + devant, lignes de couture) vers la droite ; vbC à
    `#larg_bande` vers le bas ; vbD ; rectangle ; vbA vbC = milieu dos, sens chaînette
25. Bout en onglet : recul de vbB = `#larg_bande / tan(angle encolure devant / milieu devant)` ;
    symétriques vbCp, vbDp par rapport à la pliure vbA vbB
26. Pièce Bande : vbCp – vbC – vbD – vbB – vbDp ; milieu vbC vbCp au pli ; couture 0,7 ailleurs

### Pièces
27. Devant (×1, au pli), Dos (×1, au pli), Manche (×2), Bande (×1, au pli). Couture 0,7 ;
    ourlets bas et manches 2,5.

## Contrôles
- Épaules devant et dos de même longueur (vHpvKp = vHppvKpp).
- Emmanchure devant + dos (après déplacement d'épaule) = tour lu par la manche ; embu 0,5 à 1.
- Encolure totale ≥ ~58 cm (passage de tête : le livre dit que l'encolure doit
  « impérativement » être élargie ; avec un V de 13 c'est très large).
- Bande : longueur = 1/2 encolure ± 0,1 (jersey non réduit).

## Décisions
- 2026-10-07 : question 1 → nouveau fichier `patrons/haut_pyjama.sm2d`, copie de
  `fond_base_maille.sm2d` ; le fond reste intact, la manche est copiée et reconstruite.
- 2026-10-07 : question 2 → corps élargi avec les valeurs du T-shirt souple (p. 56), encolure
  avec les valeurs du V (3 / 2 / 13) à la place de l'encolure ronde de la p. 56.

- 2026-10-07 : question 3 → 3 / 2 / 13 = encolure finie, puis lignes de couture décalées de
  `#larg_bande` vers l'extérieur.

- 2026-10-07 : question 4 → parallèle à 1,8 tracée **côté devant** (p. 47 + schéma p. 48 ; le
  « dos » du texte p. 48 est tenu pour une coquille), reportée au dos par symétrie.

## Questions ouvertes
1. ~~Fichier cible~~ : tranchée (voir Décisions).
2. ~~Élargissements p. 56 + encolure V~~ : tranchée (voir Décisions).
3. ~~Retirer la valeur de la bande~~ : tranchée (voir Décisions).
4. ~~Côté de la parallèle à 1,8~~ : tranchée (voir Décisions).
5. **Bas** : droit (recommandé pour un pyjama) ou arrondi liquette ?
6. **Manches** : longues (déjà tracées, `#long_manche` = 64) ou courtes (longueur à choisir) ?
   Poignet : ourlet 2,5 (recommandé, dans le livre) ou bord-côtes (pas de page « poignet » : règle
   du bas de jambe jogging, 3/4 du tour) ?
7. **Embu** : la nouvelle emmanchure change le tour ; recalculer, puis ne régler (hauteur ou
   bombé de tête) que s'il reste hors de 0,5 à 1 ? Recommandation : **oui**.
8. **Page de l'encolure V** et page de l'introduction aux élargissements : numéros.
