# Handoff : contexte téléphone / cloud

**Émetteur :** session Claude Code dans le cloud, pilotée depuis le téléphone
(claude.ai/code, conteneur éphémère). **Destinataire :** la session Claude Code sur le PC.

Les deux sessions travaillent sur la même branche `claude/recuperer-skills-vavt5l` et ne
peuvent pas se parler directement : **git est le seul canal**. Ce document résume ce que
la session téléphone/cloud sait et que la session PC n'a peut-être pas vu. Le suivi
principal du projet reste `doc/handoff/2026-09-27-manche-montee.md` (tenu à jour par le PC).

## Règles de cohabitation

- Une seule session à la fois modifie la branche. `git pull` avant de reprendre, commit +
  push avant de passer la main.
- Le téléphone/cloud ne lance pas Seamly2D : les tracés et les vérifications par export
  SVG se font sur le PC. Le cloud sert à lire les photos, transcrire, ranger, écrire.

## Ce que la session téléphone/cloud a fait

- Importé les 25 skills de mattpocock/skills dans `.claude/skills/` (voir son `README.md`).
- Cherché un skill de patronage existant (claude.ai + registre skills.sh, une quinzaine de
  requêtes, dont seamly2d et valentina) : **aucun**. Il faut écrire les nôtres.
- Proposé l'architecture en deux skills + fichier d'étapes validé + lexique des mesures
  + script de contrôle (reprise dans le handoff manche-montee).
- Transcrit les pages 68-73 de la manche montée et relevé l'écart FR/EN 1/3 ↔ 3/4.
- Rangé `doc/sources/` par type de pièce (`buste/`, `manche/`, `pantalon/`) avec un index
  `doc/sources/README.md`, et ajouté 7 nouvelles photos (compressées ~2000 px). Chemins du
  handoff manche-montee mis à jour.

## À faire côté PC après le pull

- La vidéo `.mp4` de la profondeur d'emmanchure n'est pas dans git : la déplacer dans
  `doc/sources/manche/profondeur-emmanchure/` si on veut la garder avec sa transcription,
  et corriger la ligne 3 de `transcription.md` qui dit encore « copie locale dans `doc/` ».

## Nouvelles sources, pas encore transcrites

Premières observations à la lecture des photos (à confirmer lors de la transcription) :

- **Buste, p. 44-47 (`buste/fond-base-maille/`)** : c'est la construction d'origine de
  `patrons/fond_base_maille.sm2d` (XY, AB, BE, EC = 1/2 BE + 1, BF, CD, AA1…DD2, encolure,
  épaule GJ = 1/3 GH, côté, B1C2 = (long. taille dos augmentée + long. taille devant)/4
  + 1,5, emmanchures C2D1K / C2D2K, ligne d'épaule décalée de 1,8 cm vers l'avant).
  Utile pour vérifier le patron existant étape par étape et comme **premier cas de test**
  du skill `lire-patronage`, puisqu'on a déjà le résultat attendu.
- **Pantalon, p. 238-243 (`pantalon/fond-pantalon-droit/`)** :
  - Mesures de base T38 (tableau p. 239, lecture à vérifier) : hauteur pantalon 100,
    taille-hanches 22, taille-montant 27, taille-genou 58, tour de taille 68,
    tour de hanches 92, tour de genou 38. Plus largeur du genou 48 et bas de pantalon 40.
    Aisances : taille + 4 cm descendue de 4 cm, hanches + 2 cm.
  - `mesures/T44.smms` a `height_waist_side_to_hip`, `rise_length_side_sitting`,
    `height_waist_side_to_knee`, `leg_knee_circ`, mais pas de largeur de bas : il faudra
    un lexique livre → Seamly pour le pantalon aussi.
  - **Écart FR/EN p. 240** : CC3 = « 1/6e du tour de **hanches** avec aisance + son 1/20e »
    en français, « 1/6th of **waist** measurement with ease » en anglais. Le devant utilise
    les hanches (CC1 = 1/7e), donc le français est probablement juste. À trancher.
- **Pantalon, p. 244-245 (`pantalon/elargissements/`)** : élargissements (1 à 2,5 cm,
  1 à 3 cm, 0,5 cm) et retracés. Page de gauche sans numéro visible ; 244 déduit du renvoi
  « voir page 244 » de la p. 246.
- **Pantalon, p. 246-247 (`pantalon/modele-pantalon-souple/`)** : modèle pantalon souple,
  ceinture bord-côtes, poches (photo remise à l'endroit).

## Suite proposée

1. Terminer la manche (embu ≈ 1,43 cm, voir handoff manche-montee).
2. Transcrire le buste p. 44-47 et le comparer à `fond_base_maille.sm2d` : ça valide le
   format du fichier d'étapes sur un patron déjà juste.
3. Écrire les skills `lire-patronage` et `tracer-sm2d`, puis les tester sur le pantalon.

## Skills suggérés

- `writing-for-agents` pour les SKILL.md, `domain-modeling` pour le lexique des mesures,
  `grilling` pour trancher les écarts FR/EN, `tdd` pour le script de contrôle.
