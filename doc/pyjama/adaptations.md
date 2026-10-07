# Pyjama : adaptations à partir des fonds du dépôt

Objectif : un haut T-shirt **col V** et un **pantalon droit souple** à taille élastique.
Ce document liste les transformations ; rien n'est tracé tant que les questions ouvertes ne
sont pas tranchées (chaîne `lire-patronage` → `.etapes.md` validé → `tracer-sm2d`).

## État de départ

Matière : **jersey** (décidé le 2026-10-07), le cadre du livre : le fond de pantalon sans
ouverture passe les hanches, aucune adaptation hors livre n'est nécessaire.

| Pièce | Base dans le dépôt | Manque |
|---|---|---|
| Haut | `patrons/fond_base_maille.sm2d` : devant, dos, manche (embu 1,43 à régler) | page du livre sur l'encolure V |
| Pantalon | `patrons/fond_pantalon_droit.sm2d` + `.etapes.md` (T44, 19 décisions, vérifié) ; transcriptions p. 244-247 | page 256 (ceinture plate) |

## 1. Pantalon de pyjama

Le livre présente le fond droit (p. 238) comme « utilisable tel quel pour un pantalon droit et
souple, un fuseau ou un jogging […] sans ouverture à la taille ». Le modèle p. 246 en est
presque un bas de pyjama ; il suffit de retirer les poches (ou de les garder).

Enchaînement (source entre crochets). Proposition : nouveau fichier
`patrons/pantalon_pyjama.sm2d` qui repart d'une copie de `fond_pantalon_droit.sm2d` (le fond
reste intact) ; les élargissements s'ajoutent comme nouveaux points, noms du fond + suffixe `e`.

1. **Base** : le fond droit tracé, devant et dos superposés [p. 238-243, déjà fait].
2. **Élargissements** [p. 244-245] — seule la taille milieu (A3 devant, A5 dos) reste à 0 :

   | Endroit (livre) | Devant | Dos | Valeur |
   |---|---|---|---|
   | Pointe d'enfourchure, vers l'entrejambe | C2 → C2e | C5 → C5e | `#elarg_enf_h` : 1 à 2,5 |
   | Pointe d'enfourchure, vers le bas | idem | idem | `#elarg_enf_v` : 1 à 3 |
   | Taille côté | A2 → A2e | B5 → B5e | 0,5 |
   | A : côté au montant | C1 → C1e | C4 → C4e | `#elarg_A` : libre |
   | B : côté au genou | D1 → D1e | D3 → D3e | `#elarg_B` : libre |
   | C : côté au bas | E1 → E1e | E3 → E3e | `#elarg_C` : libre |

   Côté entrejambe (D2, E2, D4, E4) : le schéma ne montre pas de flèche, mais le livre dit
   « dessiner les jambes dos et devant symétriquement » → à confirmer (question).
   Puis retracer enfourchure (B2→C2e, B3→C5e), hanches aplaties, jambes ; vérifier entrejambes
   et côtés assemblés (`verifier.py`).
3. **Descendre la taille** de 2 cm devant et dos [p. 247, lu sur le schéma] : nouvelle ligne de
   taille parallèle à l'ancienne (`#descente_pyjama` = 2).
4. **Poches** [p. 246-247] : optionnelles pour un pyjama.
5. **Ceinture élastiquée** sur le 1/2 tour de taille descendue [p. 256, page manquante].
   Alternative sans la page 256 : coulisse à même (prolonger le haut de 2 × largeur de
   l'élastique + 1 cm, replier, piquer).
6. Couturages 0,7 cm, ourlet 2,5 cm [p. 246].

Point d'attention hérité du fond (handoff pantalon) : côté dos évasé de B4 à B5 en T44
(`waist_circ` 76 à vérifier). L'élargissement de 0,5 en B5 l'accentue : à regarder sur le PNG.

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

## Décisions

- 2026-10-07 : matière → jersey.
- 2026-10-07 : base du pantalon → `patrons/fond_pantalon_droit.sm2d` (branche
  `claude/recuperer-skills-vavt5l`, fusionnée ici).

## Questions ouvertes

1. Le livre a-t-il une page « encolure V » (ou « encolure en pointe ») ? Si oui, la photographier.
2. Ceinture : photographier la p. 256, ou coulisse à même ?
3. Poches : avec ou sans ?
4. Valeurs d'élargissement : enfourchure (1-2,5 / 1-3), côtés A, B, C ; élargir aussi
   l'entrejambe (symétrie) ou seulement le côté ?
5. Profondeur du V (`#prof_v`) et élargissement d'encolure (`#elarg_encolure`).
6. Haut : manche longue ou courte ?
7. Fichier : `patrons/pantalon_pyjama.sm2d` copié du fond (proposé), ou un 2e bloc dans
   `fond_pantalon_droit.sm2d` ? Idem pour le haut : `tshirt_col_v.sm2d` ou bloc supplémentaire.
