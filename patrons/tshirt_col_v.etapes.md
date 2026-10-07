# T-shirt col V : étapes

Sources : doc/sources/col/encolure-v-bande-jersey/ (pages à confirmer), transcription.md
Fichier cible : à décider (question 1) — en cm
Mesures : mesures/T44.smms

Conventions : points du fond de base maille (devant et dos superposés, axe X–Y = milieu devant
et dos, haut vers X). Nouveaux points préfixés `v` (noms uniques dans tout le fichier, comme `m`
pour la manche) ; le livre ne les nomme pas, sauf la bande (A, B, C, D, C', D' → `vbA`…).

## Entrées
- Points hérités (bloc « Fond de base maille ») : H (point d'encolure à l'épaule, commun devant /
  dos), K (bout d'épaule), E (milieu devant, encolure), F (milieu dos, encolure), A (bas, sur
  l'axe). Segment H→K existant (`Line_H_K`).
- Mesures : aucune nouvelle.
- Variables :
  - `#degag_epaule` = 3 (exemple du livre)
  - `#desc_dos` = 2 (exemple du livre)
  - `#desc_devant` = 13 (exemple du livre)
  - `#larg_bande` = 1,5 (livre : « ne devra pas dépasser 1,5 cm » ; valeur : question 3)

## Étapes
### Encolure (figure 1)
1. vH : point sur une droite — sur H→K, HvH = `#degag_epaule` [fig. 1]
2. vF : point sur une droite — sur l'axe F→A, FvF = `#desc_dos` [fig. 1]
3. vE : point sur une droite — sur l'axe E→A, EvE = `#desc_devant` [fig. 1] (cote depuis E lue sur le schéma)
4. Courbe vH → vF (encolure dos), arrivée perpendiculaire au milieu dos [fig. 1] (poignées : réglage ; platitude au milieu dos : question 4)
5. Droite vH → vE (encolure devant en V) [fig. 1]
6. « Retirer la valeur de la bande » [fig. 1] : dépend de la question 2.
   - Si les 3 / 2 / 13 sont la ligne **finie** : vH2 sur H→K à `#degag_epaule + #larg_bande` de H ;
     vF2 sur l'axe à `#desc_dos + #larg_bande` de F ; vE2 = intersection de l'axe et de la
     parallèle à vH–vE décalée de `#larg_bande` vers l'extérieur ; courbe vH2→vF2, droite vH2→vE2
     = lignes de couture.
   - Si ce sont déjà les lignes de couture : rien à tracer.
7. Contrôle : 1/2 encolure = courbe dos + droite devant (lignes de couture) [fig. 1, « mesurer la 1/2 encolure »]
### Bande (figures 2 à 4), bloc séparé
8. vbA : point de départ [fig. 2]
9. vbB : point à distance, vers la droite (0) — vbA vbB = 1/2 encolure (étape 7) [fig. 2]
10. vbC : point à distance, vers le bas (270) — vbA vbC = `#larg_bande` [fig. 2]
11. vbD : point à distance depuis vbC, vers la droite (0) — vbC vbD = `Line_vbA_vbB` [fig. 2]
12. Droites vbA vbB (pliure), vbC vbD, vbB vbD ; vbA vbC = milieu dos, sens chaînette [fig. 2]
13. Bout du V : vbB recule sur la pliure pour que vbD vbB suive le prolongement du milieu devant
    quand vbD est posé sur vE (2 ou vE2) le long de l'encolure devant [fig. 3] : recul =
    `#larg_bande / tan(angle entre encolure devant et milieu devant)` (reconstruction ; calcul
    absent du livre, question 5)
14. vbCp, vbDp : symétriques de vbC, vbD par rapport à vbA vbB (pliure) [fig. 4]
15. Pièce **Bande d'encolure** : vbCp – vbC – vbD – vbB – vbDp – vbCp ; milieu vbC vbCp au pli,
    couture 0,7 partout ailleurs [fig. 3-4] ; droit-fil = sens chaînette, parallèle à vbA vbC
### Pièces
16. Pièce **Devant** : encolure H–E1–E remplacée par la droite vH–vE (ou vH2–vE2) ; l'épaule part
    de vH.
17. Pièce **Dos** : encolure H–F1–F remplacée par la courbe vH–vF (ou vH2–vF2).

## Contrôles
- Épaule devant = épaule dos (même point vH, épaule commune) : vH–K = `shoulder_length` − 3.
- Bande : longueur vbA vbB = 1/2 encolure à ± 0,1 (le jersey n'est pas réduit, contrairement
  au bord-côtes).
- Passage de tête : encolure totale (2 × 1/2 encolure) ≥ ~58 cm (à vérifier sur la personne ;
  avec un V de 13 c'est très large).

## Décisions
(aucune)

## Questions ouvertes
1. **Fichier cible** : nouveau `patrons/tshirt_col_v.sm2d` (copie de `fond_base_maille.sm2d`,
   le fond reste intact) ou bloc ajouté dans `fond_base_maille.sm2d` ?
   Recommandation : **copie**. Les pièces Devant et Dos changent (encolure) : dans le même fichier
   il faudrait dupliquer les pièces ; une copie garde le fond comme référence et la manche suit.
2. **« Retirer la valeur de la bande »** : les 3 / 2 / 13 sont-ils la ligne finie (la bande
   s'ajoute vers l'intérieur, donc couture décalée de 1,5 vers l'extérieur) ou déjà la ligne de
   couture ?
   Recommandation : **ligne finie, puis décaler** : c'est la lecture littérale de « élargir
   selon le modèle, puis seulement ensuite retirer la valeur de la bande ». Effet en T44 :
   dégagement 4,5 à l'épaule, 3,5 au dos, pointe du V environ 2 cm plus bas.
3. **Largeur de bande finie** `#larg_bande` : 1,5 (maximum du livre) ou moins (1 à 1,2) ?
   Recommandation : **1,5** pour un pyjama, plus simple à piquer ; le livre fixe 1,5 comme limite
   pour éviter les becs.
4. **Encolure dos** : courbe directe vH→vF arrivant perpendiculaire au milieu dos, ou platitude
   droite comme le fond (F1–F, 3 cm) ?
   Recommandation : **platitude reprise** (segment droit perpendiculaire au milieu dos, puis
   courbe), cohérent avec le fond et nécessaire pour que le dos plié ne fasse pas de pointe.
5. **Bout de bande en onglet** : calculer le recul de vbB par la formule (étape 13) ou poser la
   bande sur le devant dans Seamly et relever le milieu devant comme le livre ?
   Recommandation : **formule**, elle suit une taille ou une profondeur de V différente sans
   retouche ; contrôler visuellement sur le PNG.
6. **Pages** : numéros des pages encolure V et jogging (pour nommer les photos `pXX-YY-…`).
