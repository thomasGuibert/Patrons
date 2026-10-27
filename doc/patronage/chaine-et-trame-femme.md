# Bases chaîne et trame femme : analyse des pages du Vêtement féminin

Pages reçues le 2026-10-27 (chapitre « Les bases de corsage / Basic bodices », p. 62-81),
rangées et transcrites dans `doc/sources/buste/` :

| Dossier | Pages | Ce que c'est | Usage annoncé par le livre |
|---|---|---|---|
| `base-mannequin/` | 62-71 | Corsage à pinces, développement à plat du mannequin (« base classique ») | « Nous allons utiliser cette base pour les exercices qui suivront et réaliser des vêtements » ; toile en 4 parties (découpes bretelles) |
| `base-mannequin-5-pieces/` | 72-75 | La même base recomposée avec un petit côté (dos, dos côté, petit côté, devant côté, devant) | « volumes très près du corps comme la robe bustier ou volumes plus structurés comme un tailleur » |
| `elargissement-tailleur/` | 78-81 | Fond de base tailleur près du corps : la base à pinces élargie (aisances) | « vêtements classiques avec une manche montée » ; varie pour tailleur, veste, manteau |
| `fond-base-sans-pince/` | 76-77 | Fond sans pince | « vêtement large », « particulièrement adapté [...] maille » |

Livres (ESMOD Éditions, références de Thomas, détail dans `doc/sources/README.md`) :
*Le vêtement féminin* tome 1 traite le flou (jupes, chemisiers, corsages, robes), le tome 2 les
tailleurs, vestes, manteaux et pantalons de ville. Le fond maille, la manche montée et le
tableau de tailles viennent de *La maille en coupé-cousu*. Attribution retenue, à confirmer :
le PDF (base du mannequin, p. 62-71) vient du tome 1 et les photos (p. 72-81) du tome 2.
Si c'est bien le cas, la base en 5 pièces et l'élargissement tailleur partent de la base du
mannequin du **tome 2**, qui n'a pas été photographiée : il faudra vérifier qu'elle est
identique à celle du tome 1 (mêmes numéros de page, même figure 3 citée).

## Les deux corsages : flou et tailleur

Le mot « flou » n'apparaît pas dans ces pages, mais c'est le sujet du tome 1. Lecture retenue :

- **Corsage flou = base du mannequin à pinces** (p. 62-71). C'est la base près du corps, sans
  aisance ajoutée hormis les 3 cm de construction sur les hanches, avec 5 pinces de taille,
  une pince de poitrine à l'épaule et une pince d'omoplate. Elle sert de point de départ à
  tout le reste, et c'est celle d'une robe ou d'un chemisier.
- **Corsage tailleur** : deux constructions qui partent toutes deux de la base à pinces.
  - **Fond tailleur près du corps** (p. 78-81) : mêmes pinces, contours élargis pour
    l'aisance d'un vêtement porté par-dessus (encolure, épaule, carrure, emmanchure plus
    basse, côtés).
  - **Base en 5 pièces** (p. 72-75) : découpage avec petit côté, sans aisance ajoutée. C'est
    une structure de coupe (les pinces passent dans les découpes), pas un élargissement.

Le fond sans pince est un troisième fond, pour le large et la maille : c'est presque notre
fond maille actuel (comparaison dans sa transcription).

## Différences flou / tailleur (valeurs du livre)

| Point | Base à pinces (flou) | Fond tailleur près du corps |
|---|---|---|
| Encolure devant | milieu en C, épaule en C2 | milieu descendu de 2 ; épaule ouverte de 0,6 |
| Encolure dos | milieu en D, épaule en D2 | milieu descendu de 0,1 ; épaule ouverte de 0,6 |
| Longueur d'épaule | longueur d'épaule (dos : + 1 de pince d'omoplate) | + 0,5, pince fermée, dans le prolongement |
| Carrure | 1/2 carrure devant / dos | devant + 0,5 ; dos + 1 |
| Dessous de bras | (long. taille dos + devant)/4 + 2 au-dessus de la taille | + 2 vers l'extérieur, puis 1,75 plus bas |
| Taille | 1/2 tour de taille (excédent pris par 5 pinces + galbes) | + 1,25 devant et dos |
| Hanches | 1/4 tour ± 1 (côté déplacé de 1 vers le dos) | + 1,5 devant et dos |
| Milieu devant | DF | option + 0,75 (épaisseur de ceinture) |
| Pinces | pince de poitrine 1/12 du tour de poitrine, omoplate 1, taille 1 + 3 + 1 dos, 3 + 2 devant | les mêmes, inchangées |

Gain total sur le demi-tour : environ 4 à la poitrine (2 + 2), 2,5 à la taille, 3 aux hanches.

## Mesures utilisées

Toutes figurent dans le tableau p. 29 déjà transcrit (`doc/sources/tailles/tableau-36-44/`) :

| Mesure | Ligne du tableau | Déjà dans `mesures/femme/*.smms` |
|---|---|---|
| Tour de poitrine, taille, hanches | 3, 6, 8 | oui |
| Longueur taille dos / devant | 1, 2 | oui |
| Tour d'encolure | 9 | oui |
| Carrure dos / devant | 10, 11 | oui |
| Longueur d'épaule | 12 | oui |
| Hauteur taille-hanches (le livre écrit 22 cm en dur) | 19 | oui (`height_waist_side_to_hip`) |
| **Hauteur de poitrine** (de C, milieu devant encolure, en ligne droite jusqu'au point de poitrine) | 4 | **non** |
| **1/2 écart de poitrine** | 5 | **non** |
| Tour d'emmanchure, hauteur taille-dessous de bras (vérification seulement) | 13, 14 | non |

Constantes du livre : petites hanches 9 cm sous la taille, pince d'omoplate 1 cm, 2e pince dos
centrée à 8,5 cm de F1 et longue de 7 cm sous l'épaule, pointes de pince à 9 cm (dos) et 6 cm
(devant) au-dessus des grandes hanches, remontée de 2 cm de la pointe de poitrine.

Contrôles faits sur le tableau, en T38 :
- FN1 + N2E = 50 − 3,5 = 46,5, comme dans le livre ; excédent 12,5 = pinces 10 + galbes 2,5.
- Hauteur de dessous de bras (41 + 37)/4 + 2 = 21,5, soit exactement la ligne 14 du tableau.
- Pince de poitrine 88/12 = 7,33, comme dans le livre.
- De la T36 à la T44, l'écart hanches − taille est toujours de 26 cm, donc l'excédent reste à
  12,5 : le tableau des pinces (10 cm) et les galbes de 1,25 conviennent à toutes les tailles.

## Ce qui manque pour tracer dans Seamly

1. **Manche tissée** : absente de ces pages. Pour le boléro (veste doublée), la manche du
   tome 2 (tailleur) est la plus probable. La manche montée déjà transcrite vient de
   *La maille en coupé-cousu* et va avec le fond maille, et le livre lui-même renvoie à une « manche de base en chaîne
   et trame » (plus de tête, plus d'embu). Il faut ces pages-là pour le boléro.
2. **Élargissement fond de base veste** (p. 82 et suivantes) : il se devine par transparence
   sur la p. 81 sans avoir été photographié. Pour le boléro, qui est plutôt une veste, ce sont
   peut-être les bonnes valeurs.
3. **Deux mesures à ajouter** aux fichiers de tailles et au sur-mesure : hauteur de poitrine et
   1/2 écart de poitrine (lignes 4 et 5 du tableau), avec un nom Seamly à choisir sur le PC.
4. **Sur-mesure** : le livre fixe les pinces à 10 cm et met le reste dans les galbes de côté.
   Cela marche pour le tableau (hanches − taille = 26). Avec un écart hanches − taille plus
   faible (moins de 21 cm environ), les galbes deviendraient négatifs. Il faudra une règle
   (réduire les pinces au prorata ?) que le livre ne donne pas.
5. **Points non définis par le texte**, lus sur les figures (notés dans les transcriptions) :
   N1, N2, M1, M2, U, T, K, et pour la base en 5 pièces la façon de répartir les valeurs C, D,
   E, F de part et d'autre des axes.
6. **Gestes Seamly à prévoir** : fermer une pince et retracer l'épaule ou la carrure (pince
   d'omoplate, pince de poitrine), ce qui demande des rotations de points. La base en 5 pièces
   demande aussi de relever des pièces séparées et de les recomposer (point 0), avec des outils
   de déplacement et de rotation. C'est faisable, mais plus lourd que les fonds maille.

## Ordre de tracé proposé (en attente de l'accord de Thomas)

1. Ajouter hauteur et écart de poitrine aux mesures femme.
2. Tracer la base du mannequin à pinces (`patrons/base_mannequin.sm2d`) et la vérifier avec les
   contrôles p. 70.
3. Tracer le fond tailleur près du corps comme un bloc qui reprend la base sans en déplacer
   les points.
4. Tracer la base en 5 pièces seulement si un modèle en a besoin (veste cintrée, robe
   bustier).
5. Tracer la manche tissée, une fois ses pages reçues.
