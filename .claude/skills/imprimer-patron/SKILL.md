---
name: imprimer-patron
description: Produit les PDF imprimables (A4 et A3, échelle 1, feuilles à scotcher) d'un patron Seamly2D depuis son export SVG. Use when il faut créer ou mettre à jour le PDF d'un patron, le rendre imprimable ou téléchargeable sur le site, ou réduire le nombre de feuilles et de raccords.
---

Entrée : `patrons/<nom>.sm2d` déjà vérifié avec `tracer-sm2d`. Sortie : `export/seamly/<nom>_pieces.svg`,
`public/pdf/<slug>.pdf` (A4) et `public/pdf/<slug>-a3.pdf` (A3).

**Les tracés viennent toujours de Seamly** : le PDF recopie l'export SVG de Seamly, pièces
seulement déplacées ou tournées d'un quart de tour. Un recalcul de la géométrie hors Seamly
s'écartait de 5 mm (bout de la bande d'encolure), or 1 mm compte en couture.

## Étapes

### 1. Exporter les pièces avec Seamly

```
python .claude/skills/tracer-sm2d/verifier.py patrons/<nom>.sm2d --sortie export/seamly
```

Exporte une copie (le fichier peut rester ouvert dans Seamly) en `<nom>_pieces.svg` et `.png`.
Seul le SVG se commite : supprimer le PNG. Sans Seamly (session cloud), s'arrêter et demander
l'export à l'utilisateur.

Terminé quand : « Export OK » affiché, `<nom>_pieces.svg` remplacé, PNG supprimé.

### 2. Générer les PDF

Slug et titre : ceux de l'entrée du patron dans `src/patrons.ts` (champs `slug` et `nom`).
Dépendance : `reportlab` (`python -m pip install --user reportlab` si absent).

```
python .claude/skills/imprimer-patron/pdf_depuis_seamly.py export/seamly/<nom>_pieces.svg public/pdf/<slug>.pdf "<Titre>" patrons/<nom>.sm2d
python .claude/skills/imprimer-patron/pdf_depuis_seamly.py export/seamly/<nom>_pieces.svg public/pdf/<slug>-a3.pdf "<Titre>" patrons/<nom>.sm2d --a3
```

Le rangement est automatique : chaque grande pièce a son **assemblage** de feuilles (portrait
ou paysage, quart de tour permis), choisi pour le moins de feuilles puis le moins de
**raccords** (bords à scotcher) ; les petites pièces se logent dans la place libre. Page 1 :
notice, carré 5 × 5 de Seamly, plan d'assemblage.

Terminé quand : les deux PDF existent.

### 3. Contrôler

Rendre la page 1 et une feuille de chaque assemblage en PNG (`pymupdf`, à installer comme
`reportlab`) et les regarder :
- plan d'assemblage lisible, chaque pièce entière dans son assemblage ;
- sur chaque feuille, le nom de la voisine sur chaque bord à raccorder ;
- étiquettes, crans et droit-fil présents ; aucune pièce coupée par une feuille absente.

Terminé quand : chaque point vérifié sur les PNG, en A4 et en A3.

### 4. Livrer

- Commit du SVG et des deux PDF ; message « Ajoute le PDF imprimable du <patron> » (`Refs #18`).
- Rapport : feuilles et raccords par assemblage, en A4 et en A3 (lus sur le plan d'assemblage).
- Rappeler d'imprimer à 100 % et de vérifier le carré 5 × 5 avant de couper.
