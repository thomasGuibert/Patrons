# Gestes de patronage → outils Seamly2D

Vocabulaire fermé partagé par les skills `lire-patronage` (une étape = un geste) et
`tracer-sm2d` (un geste = un élément XML). Syntaxe XML détaillée :
`.claude/skills/tracer-sm2d/SEAMLY.md`.

| Geste (livre) | Exemple | Outil Seamly (`type`) |
|---|---|---|
| Point de départ | « A départ » | `single` |
| Point à distance dans une direction | « AC = 60 cm vers le bas » | `endLine` (angle : 0 droite, 90 haut, 180 gauche, 270 bas) |
| Point sur une droite | « AI = 2/3 … sur AC » | `alongLine` |
| Milieu | « E = 1/2 AB » | `alongLine`, longueur `Line_A_B/2` |
| Perpendiculaire depuis un point d'une droite | « tracer une perpendiculaire de 1 cm » | `normal` |
| Parallèle / perpendiculaire à l'axe passant par un point | « tracer II' parallèle à AB » | `endLine` depuis le point, ou `alongLine` sur le côté opposé du cadre |
| Intersection de deux droites | « G1 = GG' ∩ II' » | `lineIntersect` |
| Intersection d'une droite partant d'un point avec une autre droite | « axe de la platitude jusqu'à HH1 » | `lineIntersectAxis` |
| Intersection d'un cercle (point, rayon) et d'une droite | « porter B5 à 17 cm de A5, en appui sur la ligne F » | `pointOfContact` (Point d'intersection d'un arc et d'une droite) |
| Pied de la perpendiculaire (projection) | « K1 = projeté de K sur le côté » | `height` |
| Point sur une courbe à une distance | « cran à 7 cm de I » | `cutSpline` / `cutSplinePath` |
| Droite | « joindre IF1 en ligne droite » | `<line>` (ou le trait de l'outil qui crée le point) |
| Courbe | « joindre en courbe C2B2 » | `simpleInteractive` (2 points), `pathInteractive` (plusieurs) |
| Platitude de x cm | « platitude de 1 cm depuis I, perpendiculaire à … » | segment **droit** de x cm (`endLine` perpendiculaire), la courbe commence au bout |
| Creuser / rentrer de x à la moitié | « à la moitié, rentrer de 0,5 cm, retracer en courbe » | milieu (`alongLine`) + `normal` de x vers l'intérieur, courbe qui passe par ce point |
| Cran | « 1 cran à 7 cm de la ligne de côté » | nœud de pièce `notch="true"` (point sur la courbe) |

Conventions :
- « Rentrer », « creuser » : vers l'intérieur de la pièce. Le côté réel se vérifie
  toujours sur le schéma **et** auprès de l'utilisateur (erreur déjà commise sur G3).
- Les courbes du livre passent par les points nommés ; leurs poignées sont un réglage
  (valeurs numériques, réglables à la souris), pas une donnée du livre.
- Deux courbes qui se suivent sans point du livre entre elles → une seule courbe.
