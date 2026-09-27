# Handoff : skills de patronage Seamly2D et manche montée

Date : 2026-09-27. Branche : `claude/recuperer-skills-vavt5l`.

## Objectif

Pouvoir donner à Claude des photos d'un livre de patronage (instructions pas à pas +
schéma) et obtenir un patron Seamly2D (`.sm2d`) juste : étapes dans le bon ordre,
bonnes mesures, bon vocabulaire XML Seamly.

Une tentative précédente (dans une autre session) avait échoué sur trois points :
l'ordre des étapes n'était pas suivi, les mesures étaient fausses, et le vocabulaire
`.sm2d` manquait. Le troisième point est couvert par les fichiers existants
(`patrons/tshit_base.sm2d` sert de référence).

## État du dépôt

- `.claude/skills/` : 25 skills importés de https://github.com/mattpocock/skills
  (commit `c55ee46`, voir `.claude/skills/README.md`). Aucun skill de patronage n'existe
  ni dans ces skills ni sur skills.sh (recherche faite : sewing, patternmaking,
  seamly2d, valentina, couture… rien d'utile).
- `patrons/tshit_base.sm2d` : T-shirt maille de base, **en cm**, utilise
  `../mesures/T44.smms`. Référence pour le vocabulaire XML (`endLine`, `alongLine`,
  `normal`, `curveIntersectAxis`, `spline simpleInteractive`, `arcWithLength`, pièces…).
- `patrons/template.sm2d` : squelette vide, **en mm**. Piège : ne pas en partir tel quel
  pour un patron en cm, sinon les longueurs fixes sont 10× trop petites.
- `mesures/T44.smms` : mesures T44 en cm. Ne contient **ni** tour ni profondeur
  d'emmanchure, **ni** tour de bras.
- `doc/sources/manche-montee/` : photos des pages 68-73 du livre + `transcription.md`
  (texte français recopié, écarts FR/EN signalés). C'est la source de vérité pour la
  manche : lire ce fichier plutôt que de re-transcrire les photos.

## Architecture décidée (pas encore construite)

Deux skills avec un fichier intermédiaire validé par l'utilisateur :

1. **`lire-patronage`** : photo → `patrons/<pièce>.etapes.md`.
   - Transcrit le **texte** (le schéma sert seulement à vérifier).
   - Compare les colonnes FR et EN et signale chaque écart.
   - Une étape = un geste d'un vocabulaire fermé (point sur ligne, perpendiculaire,
     milieu, intersection, ligne, courbe, cran).
   - En tête : points hérités d'étapes antérieures (si non définis : s'arrêter et
     demander les pages manquantes) + mesures du livre utilisées.
   - Valeurs d'exemple (« ex. : 20 cm ») et réglages à l'œil marqués comme tels.
   - **L'utilisateur relit ce fichier avant tout tracé.**
2. **Lexique des mesures** partagé : terme du livre → nom Seamly → fraction.
   À tenir dans un `CONTEXT.md` (skill `domain-modeling`). Terme absent → demander.
3. **`tracer-sm2d`** : `.etapes.md` validé → `.sm2d`, un élément par étape, même ordre,
   mêmes noms de points que le livre. Aide-mémoire geste → type XML tiré de
   `tshit_base.sm2d`. Les valeurs du livre deviennent des variables (increments).
4. **Script de contrôle** (sans IA) : ordre étapes ↔ éléments, formules n'utilisant que
   des mesures/variables connues, pas de nombre en dur là où le livre donne une formule,
   unité du fichier, longueurs clés (tête de manche vs emmanchure).

## Manche montée : étapes dans l'ordre Seamly (décisions validées, voir plus bas)

La manche est un **deuxième bloc de brouillon dans `patrons/tshit_base.sm2d`** (en cm).

Variables :
- `tour_emm` = longueur emmanchure dos (splinePath K-D2-C3, id 31) + devant (K-D1-C3, id 32),
  calculée en direct depuis le bloc du T-shirt (≈ 43,1 cm en T44, calcul approché).
- `prof_emm` = `Line_C2_K1`, K1 = pied de la perpendiculaire de K sur la ligne de côté B1–C2
  prolongée (point d'aide, type `height`) ≈ 19,5 cm. Méthode : vidéo
  `doc/sources/profondeur-emmanchure/transcription.md`.
- `frac_largeur` = 3/4.
- `long_manche` = `arm_shoulder_tip_to_wrist` (64).
- `haut_coude` = `long_manche × 35/60`.
- `aisance_poignet` = 2,8 ; `larg_bas` = `arm_wrist_circ + aisance_poignet` (20).
- `reduc_coude` = 1.

1. A départ. B : AB = `tour_emm × frac_largeur + 1` (≈ 33,3). C, D : AC = BD = `long_manche`. Rectangle.
2. E = milieu AB, F = milieu CD, EF en tirets.
3. G = milieu AE, G' sur CD. H = milieu EB, H' sur CD.
4. I sur AC, AI = `prof_emm × 2/3` ; I' sur BD ; II'.
5. G1 = GG' ∩ II', H1 = HH' ∩ II'.
6. J sur AC, AJ = `haut_coude` ; J' ; JJ'.
7. F1, F2 : FF1 = FF2 = `larg_bas / 2`.
8. J1 = IF1 ∩ JJ', J2 = I'F2 ∩ JJ' (IF1/I'F2 servent de construction seulement).
9. **Déplacé depuis la p. 72** : J3 = J1 + 1 cm vers le milieu, J4 = J2 + 1 cm vers le milieu.
   Dessous de manche final : F1-J3 droite, J3-I droite creusée de 0,5 cm à la moitié
   puis courbe ; idem F2-J4-I'.
10. G2 sur GG1, GG2 = GG1/3 ; G3 = perpendiculaire de 1 cm au milieu de G2I, **vers
    l'extérieur** (tête bombée côté dos).
11. H2 = milieu HH1 ; H3 = perpendiculaire de 1,5 cm au milieu de H2I', **vers
    l'intérieur** (tête creusée côté devant).
12. Tête de manche : courbe (splinePath) I-G3-G2-E-H2-H3-I'. Les « platitudes » sont
    les poignées de la courbe : en I perpendiculaire au dessous de manche, 1 cm ; en I'
    1,5 cm ; en E horizontale, 1,5 cm côté dos, 1 cm côté devant.
13. Contrôle : `embu` = longueur tête de manche − `tour_emm`, attendu 0,5 à 1 cm, sinon
    s'arrêter.
14. Crans : dos à `7 + embu/2` depuis I ; devant à `8 + embu/2` et `9 + embu/2` depuis
    I' ; un cran en E. Crans coupés ≤ 4 mm (jersey).

## Décisions (grilling du 2026-09-27)

1. AB = 3/4 du tour d'emmanchure + 1 (colonne anglaise), fraction en variable `frac_largeur`.
2. Manche dans un 2e bloc de `tshit_base.sm2d`, `tour_emm` calculé en direct sur les
   courbes d'emmanchure (vérifier dans Seamly qu'une formule lit bien un autre bloc).
3. `prof_emm` = C2–K1 (méthode de la vidéo : milieu des bouts d'épaule → dessous de bras ;
   devant et dos partagent K, donc milieu = K1). Hauteur de tête AI = 2/3 × `prof_emm`
   (livre, jersey), **pas** les 4/5 de la vidéo (chaîne et trame). Limite : si les bouts
   d'épaule devant et dos diffèrent un jour, repasser par leur milieu.
4. Longueurs reliées aux mesures (voir variables).
5. Sens lus sur les schémas p. 71 et 73 : G3 vers l'extérieur, H3 vers l'intérieur, J3/J4
   vers le milieu, creusement 0,5 cm vers l'intérieur. Signe de l'angle des `normal` à
   vérifier visuellement.

Valeurs T44 attendues (calcul approché hors Seamly) : `tour_emm` ≈ 43,1, AB ≈ 33,3,
`prof_emm` ≈ 19,5, AI ≈ 13,0.

## Tracé réalisé (bloc « Manche » de `patrons/tshit_base.sm2d`)

Vérifié par export en ligne de commande
(`seamly2d.exe -b x -d <dossier> -f 0 --exportOnlyDetails <fichier>`) et mesure du SVG :
AB = 33,58, `tour_emm` = 43,44, AI = 13,0, tête de manche = 44,48, **embu = 1,04 cm** (hors plage).

Enseignements Seamly (à reporter dans le skill `tracer-sm2d`) :
- Les noms de points sont uniques dans **tout** le fichier : points de la manche préfixés
  `m` (`mA`, `mB`…), prime → `p` (`mIp` = I'), l'apostrophe est interdite.
- Les variables (`<variables>`) sont calculées **avant** les objets : une variable qui lit
  `Line_…`/`SplPath_…` vaut 0 sans erreur. Ces formules vont directement dans les outils
  (tour d'emmanchure `(SplPath_K_C3+SplPath_K_C3_1)`, profondeur `Line_C2_K1`, embu dans
  les crans). `SplPath_K_C3_1` = courbe dupliquée (`duplicate="1"`).
- `Line_X_Y` / `AngleLine_X_Y` n'existent que si un segment X→Y existe (outil ou `<line>`,
  éventuellement `lineType="none"`), dans ce sens-là.
- `normal` : direction premier→second point tournée de +90° (sens trigonométrique à
  l'écran) ; `angle="180"` inverse le côté.
- Pièce : un point sur une courbe (cran) se place en répétant la courbe de part et d'autre
  du point dans la liste des nœuds ; crans `notchType="slit"`, `notchLength="0.4"`.
- **Tête de manche (version actuelle, choix utilisateur)** : platitudes = segments droits
  I→`mI1` (1 cm) et I'→`mIp1` (1,5 cm) perpendiculaires au dessous de manche, puis
  3 Bézier à 4 points (`cubicBezier`, variables `Spl_<p1>_<p4>`) :
  - dos 1 : `mI1`, `mI1c` (1 cm dans l'axe de la platitude), `mG2a` (depuis G2, angle 200,
    `Line_mG2_mI*0.54`), `mG2` → passe par G3 ;
  - dos 2 : `mG2`, `mG2b` (angle 20, `Line_mG2_mE/3`), `mEc` (milieu de E–G), `mE` ;
  - devant : `mIp1`, `mIp1c` (axe de la platitude ∩ HH1), `mH`, `mE` → passe à ~0,15 de
    H2 et H3.
  Coefficients (0,54, angle 20/200) ajustés numériquement pour la T44.
  **Embu = 1,04 cm (> 1)** : à régler (hauteur de tête, largeur ou bombé), décision reportée.
- Historique : une courbe continue à 7 points (poignées 1/3 en E) donnait un embu de 0,54 ;
  une seule Bézier au dos ne peut pas passer par G3 si elle part à plat de I1 ; prendre G
  comme point de contrôle de G2→E créait une bosse.
- Sujets reportés : supprimer les milieux (`mMilG`, `mMilH`, `mMilJ3`, `mMilJ4`) et
  simplifier le dessous de manche.

## Prochaines étapes

1. Contrôler la manche dans Seamly (aspect, crans, montage avec l'emmanchure).
2. En tirer les skills `lire-patronage` et `tracer-sm2d`, le lexique des mesures et le
   script de contrôle (reprendre la mesure SVG ci-dessus).

## Skills suggérés pour la prochaine session

- `writing-for-agents` : pour rédiger les SKILL.md de `lire-patronage` et `tracer-sm2d`.
- `domain-modeling` : pour le lexique des mesures (`CONTEXT.md`).
- `grilling` : pour trancher les questions ouvertes avec l'utilisateur.
- `tdd` : pour le script de contrôle du `.sm2d`.
- `anthropic-skills:skill-creator` (si disponible) : pour tester les skills une fois écrits.
