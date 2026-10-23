---
name: verifier-patron
description: Vérifie la cohérence d'un patron Seamly2D (.sm2d) dans toutes les tailles et en sur-mesure : courbes sans angle, points non déplacés, longueurs des coutures assemblées, crans en vis-à-vis. Use when un patron vient d'être créé ou modifié (après tracer-sm2d, une retouche de courbe, une correction après essayage), ou quand l'utilisateur demande de vérifier un patron.
---

Outil : `outils/coherence/coherence.py`. Il calcule le tracé hors Seamly : pas besoin de
Seamly, ça marche aussi dans une session cloud. Il trace chaque patron dans toutes les tailles
de ses gammes (`mesures/<gamme>/T*.smms`) et dans les jeux sur mesure de
`mesures/profils-essai.toml`.

## Étapes

### 1. Décrire les coutures (nouveau patron, nouvelle pièce ou nouvelle couture)

`patrons/<patron>.coherence.toml` dit ce qui se coud avec quoi. Modèle :
`patrons/haut_pyjama.coherence.toml`. Pour avoir les points de chaque pièce dans l'ordre du
contour, avec les crans :

```
python3 outils/coherence/pieces.py patrons/<patron>.sm2d
```

- `[[courbe]]` : une courbe qui doit tourner sans angle (emmanchure, encolure, fourche…).
  Tronçons `[pièce, de, à]` mis bout à bout. `fermee` si elle se referme sur une couture,
  `pli_debut` / `pli_fin` si un bout est au pli ou au milieu d'une pièce en double.
- `[[couture]]` : bords `a` et `b` cousus ensemble, du premier point au dernier. `ecart`
  (b − a, en cm) vaut par défaut −0,1 à 0,1, et [0,5, 1] pour un embu. `rapport` sert pour un
  bord-côte réduit (`"#red_bc"`). Mettre `crans_aux_raccords = false` si l'autre bord n'a pas
  de cran aux raccords.
- Un angle voulu (pointe d'un V, bas d'une jambe fuselée) ne va pas dans `[[courbe]]`.

Terminé quand : chaque couture et chaque courbe du patron est décrite, et l'outil ne signale
aucun cran sans couture.

### 2. Vérifier

```
python3 outils/coherence/coherence.py <patron>
```

Le rapport en Markdown contient quatre contrôles. Chaque ❌ donne la taille et le point
concernés :
1. **Courbes sans angle** : au plus 1°, le long de la courbe et aux raccords une fois cousue.
   Aussi **sans virage brusque** : le virage mesuré sur 1,5 cm avant un point et sur 1,5 cm
   après ne doit pas différer de plus de 15°. Une courbe sans coin peut quand même tourner d'un
   coup (presque droite, puis très courbe) : l'œil y voit un coin, comme au point de carrure du
   haut de pyjama à l'essayage du 2026-10-22 (31 à 48°). `virage_max` dans `[[courbe]]` change
   la tolérance d'une courbe. Pour corriger : allonger la poignée du côté qui tourne trop, et
   raccourcir celle d'en face, sans déplacer de point.
2. **Points immobiles** : chaque point est comparé à `patrons/references/<patron>.json`.
3. **Longueurs des coutures**.
4. **Crans**.

Avec Seamly installé (`SEAMLY2D`, sous Linux `xvfb-run -a`), `--seamly` vérifie en plus que le
calcul hors Seamly trace comme Seamly. Le faire après avoir ajouté un outil Seamly nouveau
dans un patron.

### 3. Traiter les écarts

- **Point déplacé** : c'est une erreur. Ne jamais déplacer un point existant sans la demande
  de l'utilisateur. On corrige la forme de la courbe, pas les points. Si le déplacement est
  voulu, lancer `--maj-references` et le dire.
- **Nouveau patron** : lancer `--maj-references` une fois pour créer ses références.
- Angle, longueur ou cran faux, dû à la modification en cours : corriger avant de livrer.
- Défaut qui existait avant la modification : le signaler à l'utilisateur, sans le corriger
  de soi-même.

Terminé quand : plus aucun ❌ dû à la modification, et les ❌ restants sont signalés à
l'utilisateur, en une ligne chacun.
