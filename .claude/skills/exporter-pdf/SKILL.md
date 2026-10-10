---
name: exporter-pdf
description: Produit les PDF imprimables (A4 et A3, échelle 1) d'un patron à partir de l'export des pièces par Seamly2D, puis les publie sur le site. Use when l'utilisateur veut le PDF d'un patron ou d'une pièce, refaire les PDF après une modification, ou publier un nouveau patron en téléchargement.
---

Chaîne : `.sm2d` → Seamly exporte les pièces en SVG (sur le PC) → SVG poussé sur la branche →
`pdf_depuis_seamly.py` le découpe en feuilles (session cloud) → `public/pdf/` → PR fusionnée.

Règles fixées par Thomas :
- **Aucune géométrie recalculée hors Seamly.** 1 mm compte en couture ; un recalcul maison
  s'écartait de 5 mm à un angle aigu. Le PDF reprend les tracés du SVG de Seamly tels quels,
  pièces seulement déplacées ou tournées d'un quart de tour.
- **Limiter les feuilles à scotcher** : un assemblage par grande pièce, portrait ou paysage,
  le moins de feuilles puis le moins de raccords (le script le fait).
- Ne jamais modifier l'état du dépôt `D:\Document\repos\Patrons` (pas de checkout, commit,
  reset, stash, worktree) sans son accord.

## 1. Pièces prêtes dans Seamly

Avant tout export, chaque pièce doit avoir sa couture à l'extérieur, son droit-fil centré et ses
étiquettes entièrement à l'intérieur, sans superposition (voir `tracer-sm2d/SEAMLY.md`). Les
corrections se poussent sur la branche de travail.

## 2. Export SVG par Seamly, sur le PC

Seamly n'existe pas dans la session cloud, et la session cloud ne lit pas le disque du PC.
Lancer une session Remote Control sur le dossier `D:\Document\repos\Patrons` avec ces consignes
(remplacer `<branche>` et la liste des patrons) :

1. `git fetch origin <branche>` puis
   `git archive origin/<branche> patrons mesures | tar -x -C C:\Users\guibe\seamly2d\export_branche`
2. Depuis `export_branche\patrons`, pour chaque `<nom>` :
   `"C:\Program Files (x86)\Seamly2D\seamly2d.exe" -b <nom> -d C:\Users\guibe\seamly2d\export_svg -f 0 --exportOnlyDetails <nom>.sm2d`
   avec 120 s maximum par commande. Jamais de plan de coupe ni de dialogue d'impression :
   Seamly s'y bloque sur l'imprimante EPSON.
3. Pousser les SVG depuis un clone à part :
   `git clone --branch <branche> --single-branch https://github.com/thomasGuibert/Patrons.git C:\Users\guibe\seamly2d\push_svg`
   (ou `git -C ... pull` s'il existe), copier les `.svg` dans `export/seamly/`, commit, push
   sur `<branche>` uniquement, sans force.
4. Répondre en une phrase : fichiers poussés (noms, tailles) ou blocage.

Ensuite : arrêter la session Remote Control, puis `git pull` dans la session cloud. Sortie
attendue : `export/seamly/<nom>_pieces.svg`.

## 3. PDF, dans la session cloud

Le slug est celui de `src/patrons.ts` : le site sert `/pdf/<slug>.pdf` et `/pdf/<slug>-a3.pdf`.
Un nouveau patron doit y être ajouté pour apparaître sur le site.

```
python3 .claude/skills/tracer-sm2d/pdf_depuis_seamly.py export/seamly/<nom>_pieces.svg public/pdf/<slug>.pdf "<Titre>" patrons/<nom>.sm2d
python3 .claude/skills/tracer-sm2d/pdf_depuis_seamly.py export/seamly/<nom>_pieces.svg public/pdf/<slug>-a3.pdf "<Titre>" patrons/<nom>.sm2d --a3
```

Ensuite supprimer `.claude/skills/tracer-sm2d/__pycache__/` (non suivi).

## Autre taille ou sur-mesure, en une commande sur le PC

`mesures_vers_pdf.py` enchaîne l'export Seamly avec d'autres mesures et le PDF, sans fenêtre ni
clic (≈ 3 s par patron). Le `.sm2d` n'est pas modifié et la notice affiche la bonne taille.

```
python .claude/skills/exporter-pdf/mesures_vers_pdf.py patrons/<nom>.sm2d <sortie> "<Titre>" --taille 40 --a3
python .claude/skills/exporter-pdf/mesures_vers_pdf.py patrons/<nom>.sm2d <sortie> "<Titre>" --mesure waist_circ=80 --mesure hip_circ=98
python .claude/skills/exporter-pdf/mesures_vers_pdf.py patrons/<nom>.sm2d <sortie> "<Titre>" --mesures <fichier.vit|.smms>
```

- `--taille` : taille standard du multitaille lié (`--gsize` de Seamly, tailles paires 22 à 72).
- `--mesure` : sur-mesure ; le script écrit un `.vit` SeamlyMe avec les valeurs du multitaille
  (à `--taille` si donnée) dont celles indiquées sont remplacées. Noms : ceux du `.smms`.
- Sortie : `<sortie>/<nom>-<taille|sur-mesure>.pdf`, et `-a3.pdf` avec `--a3`.

Pour un PDF hors du PC, `pdf_depuis_seamly.py ... --taille <texte>` corrige la taille de la
notice quand le SVG a été exporté avec d'autres mesures que celles liées au `.sm2d`.

## 4. Contrôle visuel

`pdftoppm -r 40 -png -f 1 -l 1` sur chaque PDF, puis une mosaïque des feuilles. Regarder : la
notice (carré 5 × 5 de Seamly, liste des pièces, plans d'assemblage), aucune pièce coupée hors
de son assemblage, étiquettes et droit-fil lisibles. Un défaut de tracé se corrige dans le
`.sm2d` (retour à l'étape 1), jamais dans le PDF.

## 5. Publication

Commit des SVG et des PDF, `git rebase origin/main`, PR avec le skill `pr`, fusion en
**squash** quand la vérification Vercel est verte (demande de Thomas). Joindre les PDF dans le
fil et dire le nombre de feuilles et de raccords par pièce.
