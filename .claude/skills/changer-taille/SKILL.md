---
name: changer-taille
description: Lit la photo d'un tableau de tailles et en tire le fichier de mesures Seamly d'une nouvelle taille (mesures/T40.smms, T46.smms…), puis vérifie les patrons dans cette taille. Use when l'utilisateur envoie un tableau de tailles, veut une autre taille, ou veut grader un patron.
---

Une taille = un fichier `mesures/T<n>.smms`. Les patrons (`patrons/*.sm2d`) ne sont pas
dupliqués : ils sont écrits en formules sur les noms de mesures Seamly et restent reliés à
`../mesures/T44.smms` tant que l'utilisateur ne décide pas autrement.

Références :
- `mesures/T44.smms` : modèle (format, ordre et noms des lignes, incréments par taille).
- [`doc/patronage/lexique-mesures.md`](../../../doc/patronage/lexique-mesures.md) : terme du tableau → nom Seamly.
- Skill `tracer-sm2d` (`verifier.py`, `SEAMLY.md`) pour l'export de contrôle.

## Étapes

### 1. Ranger la photo

Photo du tableau dans `doc/sources/tailles/<source>/` (convention et index de
`doc/sources/README.md`). Si l'utilisateur ne précise pas la taille voulue, la demander.

Terminé quand : la photo est rangée et indexée, la taille cible est connue.

### 2. Lire le tableau

Écrire `transcription.md` à côté de la photo : le tableau **recopié tel quel**, toutes ses
lignes et colonnes, avant toute interprétation.

Règles de lecture :
- **Disposition** : repérer d'abord la forme du tableau.
  - une colonne par taille → lire la colonne de la taille cible ;
  - une colonne « base » + une colonne « incrément » (ou « gradation ») → noter les deux ; la
    valeur cible vaut `base + (n - taille_base) / 2 * incrément` (un incrément par écart de 2
    tailles, sauf si le tableau dit autre chose).
- **Unités** : cm par défaut ; une valeur en mm (ordre de grandeur ×10) est convertie et signalée.
- **Nombres** : virgule décimale française → point dans le `.smms`. Un chiffre douteux (flou,
  coupé, 1/7, 3/8, 5/6) est **⚠ douteux**, avec la lecture probable et sa raison (progression
  des tailles voisines, cohérence avec T44).
- **Ligne illisible ou coupée** : ⚠ et question, jamais de valeur devinée.
- Les intitulés du tableau sont recopiés exactement ; c'est l'étape 3 qui les traduit.

Terminé quand : chaque cellule de la photo est transcrite ou marquée ⚠.

### 3. Traduire en mesures Seamly et faire valider

Tableau `terme du tableau | nom Seamly | valeur T<n> | valeur T44 | remarque` :
- correspondance via le lexique ; terme absent → question à l'utilisateur, puis nouvelle ligne
  dans le lexique (statut **proposé**) ;
- terme sans équivalent Seamly (ex. tour de tête, hauteur de tête) : laissé hors du fichier et
  signalé ;
- mesure de `T44.smms` absente du tableau : question (l'extrapoler depuis T44 ou la fournir) ;
- cohérence : signaler tout écart > 1 cm avec l'extrapolation depuis T44
  (`base + (n - 44) / 2 * size_increase`) et tout sens inattendu (un tour qui baisse quand la
  taille monte). L'écart peut venir du tableau : le signaler, ne pas corriger seul.

Une valeur mal lue donne un patron faux **sans message d'erreur** : rien n'est généré avant la
validation.

Terminé quand : l'utilisateur a validé chaque ligne, ⚠ comprises.

### 4. Écrire `mesures/T<n>.smms`

Par un script Python dans le dossier temporaire de session, à partir de `T44.smms` :
- mêmes lignes, même ordre, mêmes noms ; seules changent `<size base="n"/>`, la ligne `size` et
  les `base` des mesures ;
- garder `<height base="170"/>` et la ligne `height` à 170 : Seamly refuse une valeur hors de sa
  liste (« 180 not in enumeration »). Même erreur sur la taille → demander une taille de la
  liste Seamly ;
- `size_increase` : ceux du tableau s'il en donne, sinon ceux de T44.

Terminé quand : le XML se relit sans erreur et contient exactement les noms de T44, avec les
valeurs validées.

### 5. Passer en revue les variables de vêtement

Lister les variables `#…` des patrons dont la formule est un **nombre fixe** (ex.
`#larg_genou` 48, `#larg_bas_pant` 40, `#garde_sol` 12, aisances). Elles valent pour toutes les
tailles. Demander à l'utilisateur lesquelles doivent suivre la taille ; celles-là sont
réécrites en formule sur les mesures (ou sur `size`) avec son accord, en suivant `tracer-sm2d`
(étape 1 : protéger ses modifications Seamly).

Terminé quand : chaque variable fixe est confirmée ou réécrite.

### 6. Vérifier les patrons dans la nouvelle taille

Seamly tourne sur le PC de l'utilisateur (Windows) : passer par une session sur son appareil,
dans son clone du dépôt.

Pour chaque patron :
- copie temporaire `patrons/_<nom>_T<n>.sm2d` avec `<measurements>../mesures/T<n>.smms</measurements>` ;
- `python .claude/skills/tracer-sm2d/verifier.py patrons/_<nom>_T<n>.sm2d`, puis supprimer la copie ;
- comparer aux dimensions de l'export T44 : chaque pièce grandit ou rétrécit dans le sens de la
  taille, sans erreur Seamly ;
- ouvrir le PNG : courbes retournées, pièces qui se croisent, points qui sautent (une formule qui
  passe en négatif dans les petites tailles).

Terminé quand : chaque patron exporte sans erreur et sa forme est examinée.

### 7. Livrer

- Commit de la photo, de `transcription.md`, de `mesures/T<n>.smms` et du lexique (jamais la
  copie temporaire).
- Rapport : lectures ⚠ et leur résolution, termes sans équivalent, variables revues, dimensions
  principales par pièce en T44 et T<n>.
- Pour voir la taille dans Seamly : relier le patron au nouveau fichier depuis le menu des
  mesures, et fermer **sans enregistrer** si le patron doit rester relié à T44.
- Ajouter `T<n>.smms` à la section « Fichiers de mesures » du lexique.
