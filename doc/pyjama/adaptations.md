# Pyjama : adaptations à partir des fonds du dépôt

Objectif : un haut T-shirt **col V** et un **pantalon droit souple** à taille élastique.
Ce document liste les transformations ; rien n'est tracé tant que les questions ouvertes ne
sont pas tranchées (chaîne `lire-patronage` → `.etapes.md` validé → `tracer-sm2d`).

## État de départ

| Pièce | Ce qui existe | Manque |
|---|---|---|
| Haut | `patrons/fond_base_maille.sm2d` : devant, dos, manche (embu 1,43 à régler) | page du livre sur l'encolure V |
| Pantalon | transcription du fond droit (p. 238-243), des élargissements (p. 244-245) et du modèle souple (p. 246-247) | **aucun `.sm2d`** ; page 256 (ceinture plate) |

## 1. Pantalon de pyjama

Le livre présente le fond droit (p. 238) comme « utilisable tel quel pour un pantalon droit et
souple, un fuseau ou un jogging […] sans ouverture à la taille ». Le modèle p. 246 en est
presque un bas de pyjama ; il suffit de retirer les poches (ou de les garder).

Enchaînement (source entre crochets) :

1. Tracer le **fond de pantalon droit** devant + dos superposés [p. 238-243], nouveau fichier
   `patrons/pantalon.sm2d` (en cm, `mesures/T44.smms`). Trancher d'abord l'écart CC3
   hanches/taille (voir transcription).
2. **Élargissements** [p. 244-245] — seule la taille milieu reste à 0 :
   - pointe d'enfourchure devant et dos : +1 à 2,5 cm vers l'entrejambe, −1 à 3 cm vers le bas
     (variables `#elarg_enf_h`, `#elarg_enf_v`) ;
   - côté à la taille : +0,5 cm ;
   - côté au montant (A), au genou (B), au bas (C) : valeurs libres, le livre n'en donne pas
     (variables `#elarg_A`, `#elarg_B`, `#elarg_C`) ;
   - retracer enfourchure, hanches et jambes, puis vérifier entrejambe et côtés assemblés.
3. **Descendre la taille** de 2 cm devant et dos [p. 247, lu sur le schéma].
4. **Poches** [p. 246-247] : optionnelles pour un pyjama.
5. **Ceinture élastiquée** sur le 1/2 tour de taille descendue [p. 256, page manquante].
   Alternative sans la page 256 : coulisse à même (prolonger le haut de 2 × largeur de
   l'élastique + 1 cm, replier, piquer).
6. Couturages 0,7 cm, ourlet 2,5 cm [p. 246].

Point d'attention : sans ouverture, le haut du pantalon doit **passer les hanches**. En jersey
c'est le cas (c'est le cadre du livre). En tissu chaîne et trame (popeline, flanelle), il faut
élargir le haut jusqu'au tour de hanches + aisance et laisser l'élastique froncer : hors livre.

## 2. T-shirt col V

**Aucune source du livre dans le dépôt** : la méthode ci-dessous est la transformation
classique d'une encolure V, à remplacer par celle du livre si elle existe (photo à fournir).

Points concernés dans le bloc « Fond de base maille » : H (point d'encolure à l'épaule,
commun devant/dos), E (milieu devant, haut), courbe d'encolure devant H→E1 (id 18), courbe
d'encolure dos H→F1 (id 21), ligne de milieu devant E→A (pliure).

1. **Élargir l'encolure à l'épaule** : H' sur la ligne d'épaule H→K, HH' = `#elarg_encolure`
   (0,5 à 1 cm). L'épaule étant commune, le dos change aussi : retracer l'encolure dos H'→F1.
2. **Point du V** : V sur le milieu devant sous E, EV = `#prof_v`. En T44, H est à
   `neck_circ/6` ≈ 6,3 cm au-dessus de E ; un V de pyjama descend en général à 16-20 cm sous
   le point d'encolure, soit EV ≈ 10 à 14 cm. À vérifier au miroir avec un mètre.
3. **Encolure devant** : droite H'V (éventuellement bombée de 0,2-0,3 cm vers l'extérieur au
   milieu pour qu'elle tombe droite une fois portée). Elle remplace la courbe H→E1 dans la pièce
   « Devant ».
4. **Bande d'encolure** en bord-côtes, largeur finie 2 à 2,5 cm, coupée double. Longueur :
   environ 90 % de l'encolure dos + 95-100 % des côtés du V (le bord-côtes tendu sur une droite
   doit rester presque à plat). Finition de la pointe : **croisée** (plus simple) ou **en onglet**.
5. **Contrôles** : longueur encolure devant H'V + dos H'F1 (×2), passage de tête (un V passe
   toujours si EV ≥ ~8 cm), épaule devant = épaule dos après élargissement.

Hors encolure, pour un pyjama : manche longue (déjà tracée) ou courte (couper à la hauteur
voulue), éventuellement bord-côtes aux poignets.

## Questions ouvertes

1. Matière du pyjama : jersey (cadre du livre) ou tissu chaîne et trame ?
2. Le livre a-t-il une page « encolure V » (ou « encolure en pointe ») ? Si oui, la photographier.
3. Ceinture : photographier la p. 256, ou coulisse à même ?
4. Poches : avec ou sans ?
5. Valeurs d'élargissement : enfourchure (1-2,5 / 1-3), côtés A, B, C.
6. Profondeur du V (`#prof_v`) et élargissement d'encolure (`#elarg_encolure`).
7. Haut : manche longue ou courte ?
8. Écart CC3 du fond de pantalon (1/6 tour de hanches FR / tour de taille EN).
9. Fichier de mesures : `T44.smms` a un tour de hanches de 90, moins que le T38 du livre (92).
   Bonnes mesures pour la personne qui portera le pyjama ?
