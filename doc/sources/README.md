# Sources de patronage

Photos du livre (colonnes FR/EN) et transcriptions, rangées par type de pièce puis par
construction. Les numéros de page sont ceux du livre. Trois livres ESMOD Éditions, collection « Devenir modéliste » (références données par Thomas
le 2026-10-27), dont les numéros de page se recouvrent :

- **La maille en coupé-cousu** (S. Delhumeau, 272 p., « livre vert ») : fonds maille, manche
  montée, pantalon, tableau des tailles p. 29 ;
  https://www.esmod-editions.com/la-maille-en-coupe-cousu-c2x25707945
- **Le vêtement féminin, tome 1** (240 p.) : le flou (jupes, chemisiers, corsages, robes) ;
  https://www.esmod-editions.com/le-vetement-feminin-tome-1-c2x18195498
- **Le vêtement féminin, tome 2** (240 p.) : pantalons de ville, tailleurs, vestes, manteaux ;
  https://www.esmod-editions.com/le-vetement-feminin-tome-2-c2x18195500

Pages chaîne et trame : p. 62-81 (base du mannequin, 5 pièces, fond sans pince, élargissement
tailleur) du **tome 2** (confirmé par Thomas) ; élargissement corsage p. 108-109 du **tome 1** ;
manches p. 132-135 et 150-153 du tome 2 (à confirmer).

| Pièce | Construction | Pages | Transcription | Patron |
|---|---|---|---|---|
| Buste | `buste/fond-base-maille/` : fond de base maille (cadre, encolure, épaule, côté, dessous de bras, emmanchures) | 44-47 | non | `patrons/fond_base_maille.sm2d` |
| Buste | `buste/deplacement-epaule/` : déplacement de la ligne d'épaule vers l'avant (1,8 cm) | 48-49 | oui | – |
| Buste | `buste/elargissements-maille/` : introduction aux élargissements, T-shirt souple, sweater | ?, 56, 57 | oui | – |
| Buste | `buste/base-mannequin/` : base du mannequin, corsage à pinces chaîne et trame (cadre, encolures, épaules, pinces, côtés, emmanchures, vérifications, toile en 4 parties) — Vêtement féminin T2, et T1 p. 76-85 (identique) | 62-71 | oui | – |
| Buste | `buste/base-mannequin-5-pieces/` : base du mannequin en 5 pièces avec petit côté (près du corps, tailleur) — Vêtement féminin T2 | 72-75 | oui | – |
| Buste | `buste/fond-base-sans-pince/` : fond de base sans pince (vêtement large, maille), proche du fond maille — Vêtement féminin T2 | 76-77 | oui | – |
| Buste | `buste/elargissement-tailleur/` : élargissement fond de base tailleur près du corps (depuis la base à pinces) — Vêtement féminin T2 | 78-81 | oui | – |
| Buste | `buste/elargissement-corsage/` : élargissement fond de base corsage (flou, depuis la base à pinces) — Vêtement féminin T1 | 108-109 | oui | – |
| Buste | `buste/tshirt-liquette/` : modèle T-shirt liquette manches courtes | 60-61 | oui | – |
| Manche | `manche/manche-montee/` : manche montée de base (cadre, tête de manche, crans, coude) | 68-73 | oui | `patrons/fond_base_maille.sm2d`, bloc Manche |
| Manche | `manche/manche-montee-chaine-trame/` : manche montée de base chaîne et trame (cadre, tête, embu, crans de montage) — Vêtement féminin T2 (à confirmer) | 132-135 | oui | – |
| Manche | `manche/manche-tailleur/` : manche tailleur deux pièces (cadre, saignée, bas, coude, tête, crans, patte) — Vêtement féminin T2 (à confirmer) | 150-153 | oui | – |
| Manche | `manche/profondeur-emmanchure/` : méthode de la vidéo Meriame Couture | – | oui | – |
| Pantalon | `pantalon/fond-pantalon-droit/` : fond de pantalon droit (mesures T38, cadre, devant, dos, vérifications) | 238-243 | oui | `patrons/fond_pantalon_droit.sm2d` |
| Pantalon | `pantalon/elargissements/` : élargissements de pantalon (numéros vus sur la 2e photo) | 244-245 | oui | – |
| Pantalon | `pantalon/jogging-jersey/` : jogging jersey ou molleton, ceinture et bas en bord-côtes | à confirmer | oui | – |
| Col | `col/encolure-v-bande-jersey/` : encolure V finie en bande jersey piquée milieu devant | à confirmer | oui | – |
| Tailles | `tailles/tableau-36-44/` : tableau des mesures du corps femme, tailles 36 à 44 | 29 | oui | `mesures/femme/T36.smms` à `T44.smms` |
| Tailles | `tailles/tableau-homme-44-54/` : tableau des mesures du corps homme, tailles 44 à 54 | ? | oui | `mesures/homme/T44.smms` à `T54.smms` |
| Pantalon | `pantalon/modele-pantalon-souple/` : modèle pantalon souple, ceinture bord-côtes, poches | 246-247 | oui | – |

Nouvelle source : créer `<pièce>/<construction>/`, nommer les photos
`pXX-YY-<sujet>.jpg`, compresser (~2000 px, qualité 82) et ajouter une ligne ici.
