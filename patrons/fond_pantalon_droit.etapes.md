# Fond de pantalon droit : étapes
Sources : doc/sources/pantalon/fond-pantalon-droit/ (p. 238-243), transcription.md (corrigée, commit cbd946d), relecture.md
Fichier cible : patrons/fond_pantalon_droit.sm2d, bloc « Fond de pantalon droit » (en cm) — proposition, voir question 6
Mesures : mesures/T44.smms existant (décision 1)
Conventions de ce fichier : axe XY vertical, A en haut. Angles Seamly : 0 droite, 90 haut,
180 gauche, 270 bas. **Gauche = côté** (indices 1 devant, 4 et 3 dos), **droite = entrejambe /
enfourchure** (indices 2 devant, 3 et 5 dos), lecture du schéma (question 7). Devant et dos
sont superposés sur le même axe, comme dans le livre.
## Entrées
- Points hérités : aucun.
- Mesures (lexique, statut « proposé ») :
  - `waist_circ` (tour de taille ; T38 livre 68)
  - `hip_circ` (tour de hanches ; T38 livre 92)
  - `height_waist_side_to_hip` (hauteur taille-hanches, AB ; T38 livre 22)
  - `height_waist_side - leg_crotch_to_floor` (hauteur taille-montant, AC, mesurée debout ;
    T38 livre 27, T44 27,1)
  - `height_waist_side_to_knee` (hauteur taille-genou, AD ; T38 livre 58)
  - `leg_knee_circ` (tour de genou ; T38 livre 38) : **non utilisé** par la construction (elle
    utilise la largeur du genou, valeur de vêtement).
  - Hauteur pantalon (AE ; T38 livre 100) : mesure ou variable, question 3.
- Variables :
  - `#aisance_taille` = 4 (livre p. 238)
  - `#descente_taille` = 4 (livre p. 238 : taille descendue de 4 cm sous la taille morphologique)
  - `#aisance_hanches` = 2 (livre p. 238)
  - `#taille_ais` = `waist_circ + #aisance_taille` (livre : « tour de taille avec aisance »)
  - `#hanches_ais` = `hip_circ + #aisance_hanches` (livre : « tour de hanches avec aisance »)
  - `#haut_pantalon` = 100 (livre, **exemple T38**, question 3)
  - `#larg_genou` = 48 (livre, **exemple**, « évoluent selon le modèle et la mode », question 4)
  - `#larg_bas_pant` = 40 (livre, **exemple**, question 4)
Les nombres fixes du texte (1 cm, 3 cm, 0,5 cm, 1/7, 1/10…) sont recopiés tels quels dans les
formules : ce sont des données du livre, pas des calculs.
## Étapes
### Cadre (p. 238)
1. A : point de départ — ligne de taille morphologique sur l'axe XY (DL, milieu de jambe) [p. 238]
2. B : point à distance, vers le bas (270) — AB = `height_waist_side_to_hip` [p. 238]
3. C : point à distance, vers le bas (270) — AC = `height_waist_side - leg_crotch_to_floor` [p. 238]
4. D : point à distance, vers le bas (270) — AD = `height_waist_side_to_knee` [p. 238]
5. E : point à distance, vers le bas (270) — AE = `#haut_pantalon` [p. 238] (exemple, question 3)
6. F : point à distance, vers le bas (270) — AF = `#descente_taille` [p. 238]
7. Axe A–E : droite en tirets (droit-fil devant et dos) [p. 238]
   - Non tracé : X et Y (bouts de l'axe sans cote dans le livre ; l'axe utile est A–E).
   - Non tracé : les perpendiculaires à l'axe en A, B, C, D, E, F comme droites séparées ; elles
     existent à travers les points posés depuis B, C, D, E, F à 0° / 180° (étapes suivantes). La
     perpendiculaire en A (taille morphologique) ne porte aucun point.
### Devant : largeurs (p. 238)
8. C1 : perpendiculaire à l'axe passant par C, vers la gauche (180) — CC1 = `#hanches_ais/7` [p. 238]
9. C2 : perpendiculaire à l'axe passant par C, vers la droite (0) — CC2 = `Line_C_C1` (« CC2 = CC1 ») [p. 238]
10. B1 : perpendiculaire à l'axe passant par B, vers la gauche (180) — BB1 = `Line_C_C1` (« BB1 = CC1 ») [p. 238]
11. B2 : perpendiculaire à l'axe passant par B, vers la droite (0) — BB2 = `#hanches_ais/10` [p. 238]
### Devant : taille (p. 240)
12. A1 : perpendiculaire à l'axe passant par F, vers la droite (0) — FA1 = `(#taille_ais/2 - 1)/5` [p. 240]
13. A2 : point à distance depuis A1, vers la gauche (180), sur la ligne F — A1A2 = `#taille_ais/4 + 1` [p. 240] (position sur F lue sur le schéma, question 9)
14. A3 : point à distance depuis A1, vers le bas (270) — A1A3 = 1 [p. 240] (« descendre », perpendiculaire à la ligne de taille)
### Devant : jambe (p. 240)
15. D1 : perpendiculaire à l'axe passant par D, vers la gauche (180) — DD1 = `#larg_genou/4 - 1` [p. 240]
16. D2 : perpendiculaire à l'axe passant par D, vers la droite (0) — DD2 = `Line_D_D1` [p. 240]
17. E1 : perpendiculaire à l'axe passant par E, vers la gauche (180) — EE1 = `#larg_bas_pant/4 - 1` [p. 240]
18. E2 : perpendiculaire à l'axe passant par E, vers la droite (0) — EE2 = `Line_E_E1` [p. 240]
19. Droites E1D1 et D1C1 (côté de jambe devant) [p. 240]
20. Droite E2D2 (entrejambe devant, bas) [p. 240]
21. MilD2C2 : milieu de D2C2 — `Line_D2_C2/2` (ou `CurrentLength/2`) [p. 240] (nom technique, absent du livre)
22. RenD2C2 : perpendiculaire à D2C2 depuis MilD2C2 — 0.5, vers l'intérieur de la pièce [p. 240] (sens : question 13 ; nom technique)
23. Courbe D2 – RenD2C2 – C2 (entrejambe devant retracé en courbe, remplace la droite D2C2) [p. 240]
### Devant : enfourchure, côté, taille (p. 240)
24. Courbe C2B2 (enfourchure devant) [p. 240] (poignées : réglage)
25. Droite B2A3 (milieu devant) [p. 240]
26. Droite C1B1 (côté) [p. 240]
27. Courbe B1A2 « légère courbe » (côté, hanche → taille) [p. 240] (poignées : réglage)
    - Non tracé sans accord : « au besoin, adoucir au pistolet l'angle formé en C1 » (question 17).
28. PlatA3 : platitude de 0.5 depuis A3, perpendiculaire à B2A3, vers A2 [p. 240] (« environ 0,5 cm » ; sens : question 16 ; nom technique)
29. Courbe PlatA3 – A2 (ligne de taille devant) [p. 240] (poignées : réglage)
### Dos : largeurs (p. 240)
30. C3 : perpendiculaire à l'axe passant par C, vers la droite (0) — CC3 = `#hanches_ais/6 + #hanches_ais/6/20` [p. 240] (écart FR/EN et lecture de « son 1/20e » : question 8)
31. C4 : perpendiculaire à l'axe passant par C, vers la gauche (180) — CC4 = `Line_C_C3` (« CC4 = CC3 ») [p. 240]
32. C5 : point à distance depuis C3, vers le bas (270) — C3C5 = 1 [p. 240]
33. B4 : perpendiculaire à l'axe passant par B, vers la gauche (180) — BB4 = `Line_C_C4` (« BB4 = CC4 ») [p. 240]
34. B3 : point à distance depuis B4, vers la droite (0), sur la ligne B — B4B3 = `Line_B1_B2 + 1` [p. 240]
    (Seamly : `Line_B1_B2` n'existe que si un segment B1→B2 existe : ajouter une droite B1→B2
    invisible, `lineType="none"`.)
### Dos : taille (p. 240)
35. A4 : point à distance depuis F, vers le haut (90), sur l'axe — FA4 = 3 [p. 240] (position sur l'axe lue sur le schéma, question 10)
36. A5 : perpendiculaire à l'axe passant par A4, vers la droite (0) — A4A5 = 0.5 [p. 240] (sens lu sur le schéma, question 11)
37. B5 : intersection du cercle de centre A5 et de rayon `#taille_ais/4 - 1` avec la ligne F, du côté gauche [p. 240] (« en appui sur la ligne de taille descendue » ; geste absent de gestes.md, question 12)
38. Droite A5B5 (ligne de taille dos droite, construction en tirets) [p. 242]
### Dos : jambe (p. 242)
39. D3 : perpendiculaire à l'axe passant par D, vers la gauche (180) — DD3 = `#larg_genou/4 + 1` [p. 242]
40. D4 : perpendiculaire à l'axe passant par D, vers la droite (0) — DD4 = `Line_D_D3` [p. 242]
41. E3 : perpendiculaire à l'axe passant par E, vers la gauche (180) — EE3 = `#larg_bas_pant/4 + 1` [p. 242]
42. E4 : perpendiculaire à l'axe passant par E, vers la droite (0) — EE4 = `Line_E_E3` [p. 242]
43. Droites E3D3 et D3C4 (côté de jambe dos) [p. 242]
44. Droite E4D4 (entrejambe dos, bas) [p. 242]
45. MilD4C5 : milieu de D4C5 — `Line_D4_C5/2` [p. 242] (nom technique)
46. RenD4C5 : perpendiculaire à D4C5 depuis MilD4C5 — 0.5, vers l'intérieur de la pièce [p. 242] (sens : question 14 ; nom technique)
47. Courbe D4 – RenD4C5 – C5 (entrejambe dos retracé en courbe) [p. 242]
### Dos : enfourchure, côté, taille (p. 242)
48. Courbe C5B3 (enfourchure dos) [p. 242] (poignées : réglage)
49. Droite B3A5 (milieu dos) [p. 242]
50. Droites C4B4 et B4B5 (côté dos) [p. 242]
    - Non tracé sans accord : « au besoin, adoucir les angles avec le pistolet » (question 17).
51. MilA5B5 : milieu de A5B5 — `Line_A5_B5/2` [p. 242] (nom technique)
52. RenA5B5 : perpendiculaire à A5B5 depuis MilA5B5 — 0.5, vers l'intérieur de la pièce [p. 242] (sens : question 15 ; nom technique)
53. Courbe A5 – RenA5B5 – B5 (ligne de taille dos) [p. 242] (poignées : réglage)
### Pièces (hors gestes, p. 242 « relever séparément le devant et le dos »)
54. Pièce **Devant** : A3 – PlatA3 – (courbe) – A2 – (courbe) – B1 – C1 – D1 – E1 – E2 – D2 – (courbe par RenD2C2) – C2 – (courbe) – B2 – A3 (question 6)
55. Pièce **Dos** : A5 – (courbe par RenA5B5) – B5 – B4 – C4 – D3 – E3 – E4 – D4 – (courbe par RenD4C5) – C5 – (courbe) – B3 – A5 (retournement : question 6)
56. Pièce **Carré 5x5** dans un bloc « Carré 5x5 », sans marge (choix, pas du livre ; comme `fond_base_maille.sm2d`)
- Non tracé : variante avec ouverture à la taille (réduction de 2 à 4 cm, schéma p. 242) : option
  de modèle, pas le fond (question 18).
- Vérifications p. 242 : reprises dans « Contrôles ».
## Contrôles
Valeurs attendues en **T38 du livre** (`waist_circ` 68, `hip_circ` 92, AB 22, AC 27, AD 58,
AE 100, genou 48, bas 40 ; donc `#taille_ais` = 72, `#hanches_ais` = 94). Calcul à la main,
tolérance ± 0,05 sauf indication. Abscisses : + à droite de l'axe (entrejambe), − à gauche (côté).
Cadre
- AF 4 ; AB 22 ; AC 27 ; AD 58 ; AE 100 (sous A). A4 à 1 sous A (3 au-dessus de F). C5 à 28 sous A.
Devant
- CC1 = CC2 = BB1 = 94/7 ≈ **13,43** ; BB2 = 94/10 = **9,40** ; largeur B1B2 = 22,83.
- FA1 = (36 − 1)/5 = **7,00** ; A1A2 = 72/4 + 1 = **19,00** → A2 à **−12,00** sur la ligne F
  (1,43 en dedans de B1 : côté qui rentre vers la taille).
- A3 : +7,00, 1 sous F. Milieu devant B2A3 ≈ 17,17.
- DD1 = DD2 = 48/4 − 1 = **11,00** ; EE1 = EE2 = 40/4 − 1 = **9,00**.
Dos
- CC3 = CC4 = BB4 = 94/6 × 21/20 ≈ **16,45** (C3 à 3,02 au-delà de C2, comme sur le schéma).
  Pour mémoire, lecture anglaise (taille) : 72/6 × 21/20 = 12,60.
- B4B3 = 22,83 + 1 = **23,83** → B3 à **+7,38** (en dedans de B2 = +9,40, comme sur le schéma).
- A5 : +0,50, 1 sous A. A5B5 = 72/4 − 1 = **17,00** → B5 à √(17² − 3²) ≈ 16,73 de A5 en
  horizontale, soit **−16,23** sur la ligne F (0,22 en dedans de B4 = −16,45).
- Milieu dos B3A5 ≈ 22,10.
- DD3 = DD4 = 48/4 + 1 = **13,00** ; EE3 = EE4 = 40/4 + 1 = **11,00**.
Vérifications du livre (p. 242)
- **Tour de taille reconstitué** 2 × (ligne de taille devant PlatA3…A2 + ligne de taille dos
  A5…B5) : cordes 19,03 + 17,00 = 36,03 → **≈ 72,1 à 72,2** avec le bombé des courbes ;
  attendu `#taille_ais` = 72, tolérance ± 0,5 (A1A2 = 1/4 + 1 et A5B5 = 1/4 − 1 se compensent).
- Tour de hanches reconstitué à la ligne B, 2 × (B1B2 + B4B3) = 2 × 46,66 = **93,33** ; pour
  mémoire `#hanches_ais` = 94 (−0,67 : c'est la construction du livre, à signaler, pas à corriger).
- Longueurs de côté (A2 ou B5 → E1 ou E3) : devant ≈ 5,00 + 18,06 + 31,10 + 42,05 = **96,2** ;
  dos ≈ 5,00 + 18,00 + 31,19 + 42,05 = **96,2**. Écart attendu < 0,2.
- Entrejambes (droites, avant creusement) : devant C2→D2→E2 ≈ 31,10 + 42,05 = **73,15** ;
  dos C5→D4→E4 ≈ 30,20 + 42,05 = **72,25**. Écart ≈ **0,9** (dos plus court), attendu du
  livre ; à mesurer et signaler (question 19).
- Enfourchure : assembler les entrejambes devant et dos en C2/C5 et vérifier la continuité de
  la courbe C2B2 + C5B3 (contrôle visuel sur le PNG).
## Décisions
1. **Fichier de mesures** : tracer directement en T44, avec le fichier `mesures/T44.smms`
   existant (option b). Pas de T38. Les contrôles T38 restent un repère de calcul.
2. **Hauteurs** : AB = `height_waist_side_to_hip`, AD = `height_waist_side_to_knee`, AC =
   montant debout `height_waist_side - leg_crotch_to_floor` (option b).
## Questions ouvertes
À poser une à la fois, dans cet ordre (les premières conditionnent les suivantes).
1. **Fichier de mesures.** Le livre est en T38 (tableau p. 239) ; le dépôt n'a que
   `mesures/T44.smms`.
   - a) Créer `mesures/T38.smms` avec les valeurs du livre (`waist_circ` 68, `hip_circ` 92,
     `height_waist_side_to_hip` 22, `rise_length_side_sitting` 27, `height_waist_side_to_knee` 58,
     `leg_knee_circ` 38) et tracer dessus.
   - b) Tracer directement en T44.
   - c) Les deux : T38 d'abord, puis bascule du patron sur T44.
   - Recommandation : **c**. En T38, chaque contrôle ci-dessus se compare au chiffre près au
     schéma du livre (C3 à 3,02 au-delà de C2, B3 en dedans de B2…) : une erreur de tracé se
     voit tout de suite. La T44 est suspecte pour ce patron : `hip_circ` 90 < 92 du T38 du livre,
     écart taille/hanches 14 cm contre 24 ; en T44, A2 tomberait à −13,20 (FA1 7,80 − A1A2
     21,00) contre B1 à −13,14 : côté devant sans galbe de hanche. Choisir la taille 38 dans le
     T44 multitaille ne suffit pas (il donne taille 64, hanches 78, pas 68/92). Faire valider les
     mesures T44 à part avant la bascule.
2. **Correspondance des hauteurs** (lexique, statut « proposé »). Hauteur taille-hanches →
   `height_waist_side_to_hip`, taille-montant → `rise_length_side_sitting`, taille-genou →
   `height_waist_side_to_knee`.
   - Options : valider ; ou d'autres mesures Seamly (par ex. montant mesuré debout,
     `height_waist_side` − `leg_crotch_to_floor` = 27,1 en T44).
   - Recommandation : **valider**. Les valeurs T44 (20 ; 27,1 ; 62) sont du bon ordre de grandeur
     par rapport au livre (22 ; 27 ; 58) et le montant assis est la mesure habituelle du
     « montant ». Passer ces lignes en « validé » dans `lexique-mesures.md`.
3. **Hauteur pantalon AE** (100 en T38) : longueur de vêtement ou mesure du corps ?
   - a) Variable `#haut_pantalon` = 100 (valeur du livre).
   - b) `height_waist_side` (taille → sol, 112,1 en T44).
   - c) Variable reliée à une mesure, par ex. `height_waist_side - <hauteur de cheville>`.
   - Recommandation : **a** pour le tracé T38, puis **c** à la bascule T44. Le livre la range dans
     les « mesures de base » mais la dit « hauteur totale du pantalon » : c'est une longueur
     finie, choisie. `height_waist_side` en T44 (112,1) donnerait un pantalon qui touche le sol ;
     100 sur une silhouette de 170 cm s'arrête vers la cheville.
4. **Largeur du genou 48 et du bas 40** : valeurs d'exemple (« évoluent selon le modèle et la
   mode »).
   - a) Variables fixes `#larg_genou` = 48, `#larg_bas_pant` = 40, identiques en T44.
   - b) Variables reliées à des mesures (par ex. `leg_knee_circ` + aisance ; en T38 38 + 10 = 48).
   - Recommandation : **a**. Ce sont des largeurs de mode, pas des mesures du corps ; en T44
     elles donnent DD1 = 11, EE1 = 9, cohérents avec des hanches de 92. Le tour de genou 38 du
     tableau n'est pas utilisé par la construction ; le relier créerait une règle absente du
     livre. Ajouter les deux variables au lexique.
5. **Aisances en variables** : `#aisance_taille` = 4, `#descente_taille` = 4,
   `#aisance_hanches` = 2 (valeurs du livre).
   - Options : variables séparées (proposé) ; ou valeurs en dur dans les formules.
   - Recommandation : **variables**. Elles se règlent par matière (le livre parle de maille
     non stretch) et apparaissent chacune dans 4 à 6 formules.
6. **Fichier cible et organisation.**
   - Proposition : nouveau `patrons/fond_pantalon_droit.sm2d` (squelette de
     `fond_base_maille.sm2d`, en cm) ; bloc « Fond de pantalon droit » avec devant et dos
     superposés sur le même axe comme au livre ; pièces **Devant** et **Dos** séparées ; bloc
     « Carré 5x5 » avec sa pièce de contrôle d'échelle ; X et Y non tracés.
   - « Le dos sera retourné pour obtenir un dos droit » : pièce Dos en miroir, ou telle quelle ?
   - Recommandation : **proposition telle quelle, Dos sans miroir**. Un pantalon se coupe de toute
     façon en 2 × 2 pièces en vis-à-vis : le retournement du livre sert au relevé papier, pas au
     patron numérique. Superposer devant et dos garde la comparaison directe avec le schéma
     p. 241.
7. **Côtés des indices** (lus seulement sur les schémas p. 239 et 241) : à gauche de l'axe
   (côté) B1, C1, D1, E1, A2 et B4, C4, D3, E3, B5 ; à droite (entrejambe) A1, A3, B2, C2, D2, E2
   et B3, C3, C5, D4, E4, A5.
   - Options : valider ; ou inverser devant et/ou dos.
   - Recommandation : **valider** (relecture.md § 3 : « sûr » pour chaque point). Les chiffres le confirment : C3 (16,45) dépasse C2 (13,43) et
     B3 (7,38) reste en dedans de B2 (9,40), exactement comme dessiné ; l'enfourchure dos plus
     longue que le devant est la norme.
8. **CC3 : écart FR/EN et lecture de « son 1/20e ».** FR « (1/6 du tour de **hanches** avec
   aisance) + son 1/20 » ; EN « 1/6th of **waist** measurement with ease + 1/20th of its
   measurement ».
   - a) Hanches, 1/20 du sixième : 94/6 × 21/20 = **16,45**.
   - b) Taille (anglais) : 72/6 × 21/20 = **12,60**.
   - c) Hanches + 1/20 des hanches : 94/6 + 94/20 = **20,37**.
   - Recommandation : **a**. En b, C3 serait à 12,60, en dedans de C2 (13,43) : le schéma montre
     C3 au-delà de C2, et la fourche dos serait plus courte que la devant. En c, C3 serait à
     6,9 au-delà de C2, le schéma montre un écart d'environ 3 (a donne 3,02). Le devant
     utilise aussi les hanches (CC1 = 1/7). La relecture mesure CC4 ≈ 1,3 × CC1 sur le schéma
     (a : 1,22 ; b : 0,94).
9. **A2 sur la ligne de taille descendue F**, A1A2 mesuré le long de cette ligne (texte : « A1A2
   = 1/4 du tour de taille avec aisance + 1 cm », sans dire sur quelle ligne).
   - a) A2 sur la ligne F, à 19,00 de A1 (−12,00).
   - b) A2 sur la ligne F mais A1A2 compté depuis A3 (corde oblique de 19 : A2 à −11,97).
   - c) A2 sur la ligne morphologique A.
   - Recommandation : **a**. Le schéma p. 241 place A2 sur la même ligne que F, A1 et B5 ; A1 est
     défini sur F (FA1) ; b ne change que 0,03 et complique ; c contredit la taille descendue de
     4 cm voulue au p. 238.
10. **A4 sur l'axe** à FA4 = 3, c'est-à-dire 3 au-dessus de F, 1 sous A.
    - Options : au-dessus de F sur l'axe (proposé) ; sous F (3 sous F, 7 sous A).
    - Recommandation : **au-dessus**. Schéma p. 241 : A4 juste sous A, au-dessus de F ; le milieu
      dos doit monter plus haut que le milieu devant (A3 à 5 sous A, A5 à 1 sous A), ce que donne
      « au-dessus ».
11. **Sens de A5** : A4A5 = 0,5 « perpendiculairement à l'axe XY », sens non écrit.
    - Options : vers la droite, côté enfourchure (+0,50) ; vers la gauche (−0,50).
    - Recommandation : **droite**. Schéma p. 241 : A5 à droite de A4 ; le milieu dos B3A5 s'incline
      alors comme dessiné (B3 à +7,38 → A5 à +0,50).
12. **Position et geste de B5.** FR : « porter B5 en ligne droite **à l'appui de** la ligne de
    taille descendue » ; EN : « **imitating** the dropped waist line ».
    - Position : a) B5 **sur** la ligne F, à 17,00 de A5 (−16,23) ; b) A5B5 parallèle à la ligne F
      (horizontale depuis A5, B5 à −16,50, 3 au-dessus de F).
    - Geste : cercle (A5, 17) ∩ ligne F, absent de `gestes.md` ; outil Seamly « point
      d'intersection d'un arc et d'une droite » (`pointOfContact`), ou à défaut un point à
      distance depuis F vers la gauche de longueur `sqrt((#taille_ais/4 - 1)^2 - 3^2) - 0.5`.
    - Recommandation : **a, avec `pointOfContact`** (et ajout de la ligne « Intersection d'un
      cercle et d'une droite » dans `gestes.md`). Le schéma p. 241 place B5 sur la ligne de A2 et
      F (relecture : « sûr ») ; « à l'appui » (le français fait foi) veut dire posé sur la ligne ; b ferait une taille
      dos droite, alors que le schéma la montre montante vers A5. L'outil garde la formule du
      livre intacte, la variante sqrt recalcule la géométrie à la main.
13. **Sens du « rentrer de 0,5 » sur D2C2** (entrejambe devant).
    - Options : vers l'intérieur de la pièce (vers l'axe, à gauche) ; vers l'extérieur (à droite).
    - Recommandation : **intérieur**, convention de `gestes.md` (« rentrer » = vers l'intérieur) :
      l'entrejambe se creuse sous la fourche pour dégager la cuisse. Le schéma est trop fin pour
      trancher à l'œil ; la relecture (mesure des pixels, p. 241 et 243) place la courbe à gauche
      de la droite, vers l'axe (« probable »). L'erreur a déjà été faite sur G3 de la manche : à confirmer.
14. **Sens du « rentrer de 0,5 » sur D4C5** (entrejambe dos).
    - Options et recommandation : **intérieur** (vers l'axe), même raison que la question 13 ;
      relecture : courbe à gauche de la droite (« probable »).
15. **Sens du « rentrer de 0,5 » sur A5B5** (taille dos).
    - Options : vers l'intérieur de la pièce (vers le bas) ; vers l'extérieur (vers le haut).
    - Recommandation : **intérieur (bas)**. Sur le schéma p. 241, deux traits relient A5 à B5 : la
      droite et, sous elle, la courbe creusée (relecture : « probable ») ; cela donne 17,04 de courbe au lieu de 17,00, sans
      effet notable sur le tour de taille (≈ 72,1).
16. **Platitude de 0,5 depuis A3** : segment droit de 0,5, perpendiculaire à B2A3, vers A2, puis
    courbe jusqu'à A2 (règle de `gestes.md`) ?
    - Options : a) segment droit puis courbe (proposé) ; b) seulement la poignée de la courbe en A3
      orientée perpendiculairement à B2A3.
    - Recommandation : **a**, pour suivre `gestes.md` et le choix fait sur la manche (platitudes =
      segments droits). Sens vers A2 : c'est le seul qui reste dans la pièce.
17. **Adoucissements « au besoin, au pistolet »** : angle en C1 (devant), angles en B4 et C4 (dos) ;
    et la « légère courbe » B1A2.
    - a) Garder les droites et les angles (tracé strict du texte), B1A2 en courbe à poignées douces.
    - b) Remplacer D1–C1–B1 (et D3–C4–B4–B5) par des courbes passant par ces points.
    - Recommandation : **a**, puis juger sur le PNG. Les angles sont faibles en T38 : en C1 la
      direction passe de 4,5° (D1C1) à 0° (C1B1), en C4 de 6,3° à 0° ; « au besoin » les réserve à
      l'œil.
18. **Variante avec ouverture à la taille** (réduction de 2 à 4 cm, 0,5 par bord sur le schéma
    p. 242) : hors fond ?
    - Options : ne pas tracer ; ajouter une variable `#reduc_taille` = 0 réglable.
    - Recommandation : **ne pas tracer** : option de modèle, pas le fond ; même principe que les
      pages de la manche reportées.
19. **Écart d'entrejambe** attendu ≈ 0,9 (devant 73,15, dos 72,25, en droites) : le livre dit
    « assembler… retracer au besoin ».
    - Options : garder le tracé du livre et signaler l'écart ; ou ajuster (par ex. E4/D4) pour
      égaliser.
    - Recommandation : **garder et signaler**. Un dos d'entrejambe un peu plus court qui se
      soutient au montage est courant, et l'ajustement n'est pas écrit dans le livre ; décision à
      revoir après la mesure réelle dans Seamly.
