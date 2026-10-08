---
name: tracer-sm2d
description: Trace un fichier d'étapes validé en patron Seamly2D (.sm2d) et le vérifie par export. Use when il faut créer ou modifier un patron .sm2d, tracer une pièce, ou vérifier un patron dans Seamly.
---

Entrée : `patrons/<patron>.etapes.md` **validé** par l'utilisateur (produit par
`lire-patronage`). Sans fichier validé, repasser par `lire-patronage`.

Références :
- [`SEAMLY.md`](SEAMLY.md) : syntaxe XML des outils et pièges de Seamly (à lire avant d'écrire du XML).
- [`doc/patronage/gestes.md`](../../../doc/patronage/gestes.md) : geste → outil Seamly.
- [`doc/patronage/lexique-mesures.md`](../../../doc/patronage/lexique-mesures.md) : mesures.
- Patron de référence : `patrons/fond_base_maille.sm2d` (3 blocs, pièces avec étiquettes).

## Étapes

### 1. Protéger le travail de l'utilisateur

L'utilisateur édite aussi dans Seamly (positions d'étiquettes, poignées de courbes, pièces
déplacées). Avant d'écrire un `.sm2d` existant :
- `git diff --ignore-cr-at-eol` sur le fichier : toute différence vient de l'utilisateur ;
- `patrons/<fichier>.sm2d.autosave` (non enregistré) et `.locked` (fichier ouvert dans Seamly) ;
- reporter ces modifications dans la nouvelle version, ou commiter la version de
  l'utilisateur d'abord.

Préférer l'**édition ciblée** du XML existant à la régénération complète.

Terminé quand : chaque modification de l'utilisateur est soit commitée, soit reportée.

### 2. Tracer

Écrire le XML par un **script Python générateur** dans le dossier temporaire de session
(jamais de XML long tapé à la main) :
- un élément par étape, **dans l'ordre du fichier d'étapes** ;
- noms de points du livre (règles de nommage dans `SEAMLY.md`) ;
- formules du fichier d'étapes recopiées, pas de nombre calculé à la main ;
- nouveau patron : squelette de `patrons/fond_base_maille.sm2d` (unité **cm**, mesures en chemin
  relatif `../mesures/<fichier>.smms`), pas `patrons/template.sm2d` (en mm).

### 3. Vérifier

```
python .claude/skills/tracer-sm2d/verifier.py patrons/<fichier>.sm2d
```

Le script exporte en SVG et PNG via la ligne de commande Seamly (sur une copie, le fichier
peut rester ouvert), puis affiche pour chaque pièce ses dimensions et la position de ses
sommets. Il signale toute erreur Seamly.

- Chaque valeur de la section « Contrôles » du fichier d'étapes est mesurée et comparée.
  Mesurer une longueur entre deux **sommets** de la pièce, jamais via une largeur englobante
  (une courbe qui déborde la fausse : l'embu de la manche a été faux de 0,35 cm ainsi).
- Ouvrir le PNG et regarder la forme : angles parasites, bosses, courbe du mauvais côté.

Terminé quand : export sans erreur, chaque contrôle chiffré dans sa tolérance (ou l'écart
signalé à l'utilisateur), PNG examiné.

Sans Seamly (session cloud) : `python3 .claude/skills/tracer-sm2d/evaluer_hors_seamly.py
<fichier> --dump` évalue les formules et les points (outils usuels, repère y vers le haut) et
signale les `Line_` lus sans segment ; `rendre_hors_seamly.py <fichier> <sortie.png>` dessine
les contours des pièces et les crans. Validé sur `fond_base_maille.sm2d` (tour 43,10, embu
1,43). Ne remplace pas l'export Seamly : le signaler à l'utilisateur.
PDF imprimables d'un patron : skill `exporter-pdf` (export SVG par Seamly, jamais de géométrie
recalculée hors Seamly).

### 4. Livrer

- Commit du `.sm2d` (et du fichier d'étapes s'il a évolué).
- Rapport à l'utilisateur : valeurs contrôlées, écarts, choix de réglage faits (poignées).
- Rappeler de **fermer le fichier dans Seamly sans enregistrer puis de le rouvrir** : sinon
  la version ouverte écrase la nouvelle.
- Reporter dans `SEAMLY.md` tout nouveau piège Seamly découvert.
