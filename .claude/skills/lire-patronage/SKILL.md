---
name: lire-patronage
description: Transcrit les photos d'un livre de patronage en fichier d'étapes à faire valider avant tout tracé. Use when l'utilisateur fournit des pages ou photos de patronage, demande de lire ou transcrire une construction, ou veut préparer le tracé d'une nouvelle pièce.
---

Chaîne complète : **lire-patronage** (ce skill) → étapes validées par l'utilisateur → `tracer-sm2d`.
Ce skill s'arrête au fichier d'étapes validé ; il ne touche à aucun `.sm2d`.

Références partagées avec `tracer-sm2d` :
- [`doc/patronage/gestes.md`](../../../doc/patronage/gestes.md) : vocabulaire fermé des gestes.
- [`doc/patronage/lexique-mesures.md`](../../../doc/patronage/lexique-mesures.md) : terme du livre → nom Seamly.

## Étapes

### 1. Situer les sources

Les photos vivent dans `doc/sources/<pièce>/<construction>/`, indexées par
`doc/sources/README.md`. Nouvelle source : créer le dossier, nommer les photos
`pXX-YY-<sujet>.jpg`, ajouter la ligne d'index.

Travailler **uniquement sur les pages que l'utilisateur désigne**. Une étape venue d'une autre
page (même visible sur la photo) n'entre qu'avec son accord explicite.

Terminé quand : chaque page désignée est identifiée par son numéro et sa photo.

### 2. Transcrire

Écrire `transcription.md` à côté des photos (modèle : `doc/sources/manche/manche-montee/transcription.md`).

- Le **texte** est la source de vérité ; le schéma sert de contrôle.
- Recopier le texte français phrase par phrase, dans l'ordre du livre.
- Lire la colonne anglaise en regard, ligne à ligne ; chaque écart devient une ligne **⚠** avec
  la lecture probable et sa raison (ordre de grandeur, cohérence avec les autres formules).
- Marquer comme **exemple** toute valeur « ex. : … », tout tableau de taille, tout réglage « à
  l'œil » / « au pistolet ».
- Section finale « Points des schémas non définis dans le texte » : chaque point nommé sur le
  schéma sans définition écrite, avec ce que le schéma suggère.

Terminé quand : chaque paragraphe des pages a sa transcription, chaque écart FR/EN est marqué,
chaque point nommé du schéma est défini (texte ou section finale).

### 3. Écrire le fichier d'étapes

`patrons/<patron>.etapes.md`, au format ci-dessous. Une étape = **un geste** de
`gestes.md`, dans l'ordre du livre, avec les **noms de points du livre**. Chaque longueur est
une formule en noms de mesures du lexique ou en variables, jamais un nombre calculé à la main
là où le livre donne une formule.

Pour chaque mesure du livre : la chercher dans `lexique-mesures.md`. Absente → question
ouverte (étape 4), et proposer une entrée.

Terminé quand : chaque phrase de construction de la transcription correspond à une étape ou à
une ligne « non tracé » justifiée.

### 4. Lister les questions ouvertes

En fin de fichier d'étapes, une question par :
- écart FR/EN ;
- mesure absente du lexique ou choix de fichier de mesures ;
- **sens** (côté, intérieur/extérieur, haut/bas) lu seulement sur le schéma : ces lectures sont
  souvent fausses, chacune est une question ;
- point hérité d'une construction antérieure absent du patron : demander les pages manquantes ;
- valeur d'exemple à remplacer par une mesure ou une variable.

### 5. Faire valider

Poser les questions **une à la fois**, chacune avec les options et une recommandation argumentée
(chiffres à l'appui quand c'est possible : un ordre de grandeur tranche souvent un écart FR/EN).
Reporter chaque réponse dans la section « Décisions » du fichier d'étapes.

Terminé quand : plus aucune question ouverte **et** l'utilisateur a confirmé le fichier
d'étapes. Alors seulement, passer la main à `tracer-sm2d`.

## Format du fichier d'étapes

```markdown
# <Patron> : étapes

Sources : doc/sources/<pièce>/<construction>/ (p. XX-YY), transcription.md
Fichier cible : patrons/<fichier>.sm2d, bloc « <Bloc> » (en cm)
Mesures : mesures/<fichier>.smms

## Entrées
- Points hérités : <points d'un autre bloc utilisés, ou « aucun »>
- Mesures : <nom Seamly> (<terme du livre>)…
- Variables : #<nom> = <formule ou valeur> (<origine : livre, exemple, choix>)

## Étapes
1. <Point> : <geste> — <formule> [p. XX] (<remarque : exemple, lu sur le schéma…>)
2. …

## Contrôles
- <grandeur> attendue <valeur ou plage> (<source>)

## Décisions
- <date> : <question> → <réponse>

## Questions ouvertes
1. …
```
