# Sweat homme (encolure ronde, fentes, poche poitrine) : étapes

Modèle : dessin technique envoyé par Thomas le 2026-10-20 (sweat manches longues, poche
poitrine, fentes au bas du devant, bord-côtes d'encolure, de poignets et de bas).

Sources (transcriptions à côté des photos) :
- `doc/sources/buste/elargissements-maille/` : élargissement **sweater** (p. 57) ;
- `doc/sources/buste/deplacement-epaule/` : déplacement de la ligne d'épaule (p. 48-49) ;
- `doc/sources/buste/tshirt-liquette/` : enchaînement d'un haut complet (p. 60-61) ;
- `doc/sources/manche/manche-montee/` : manche (p. 68-71) et crans (p. 72) ;
- `doc/sources/pantalon/jogging-jersey/` : construction des bandes bord-côtes (fig. 3 :
  longueur = 3/4 de la ligne mesurée sur le patron, largeur = hauteur finie × 2).
Fichier cible : `patrons/sweat_homme.sm2d`, construit comme `haut_pyjama.sm2d` (même fond, même
manche, même déplacement d'épaule), en cm. Mesures : `mesures/homme/T44.smms`.

## Composition

| Pièce | Coupe | Matière | Taille finie T44 (voir Réalisation) |
|---|---|---|---|
| Devant | 1 au pli | molleton | fentes en bas de côté |
| Dos | 1 au pli | molleton | |
| Manche | 2 | molleton | |
| Bord-côte d'encolure | 1 | bord-côtes | 2,5 fini (coupé 5) |
| Poignet | 2 | bord-côtes | 7 fini (coupé 14) |
| Bord-côte de bas devant | 1 | bord-côtes | 6 fini (coupé 12), d'une fente à l'autre |
| Bord-côte de bas dos | 1 | bord-côtes | 6 fini (coupé 12), d'une fente à l'autre par le dos |
| Poche | 1 | molleton (ou contraste) | 12 × 10 fini |
| Haut de poche | 1 | molleton (ou contraste) | 12 × 5 fini, plié en deux |
| Patte | 1 | mercerie | ruban + anneau D pris dans la couture poche / haut de poche |

## Entrées
- Points hérités du fond de base maille (bloc « Corps ») : H, K, D, D1, D2, C2, A, A1, E, F, F1.
- Variables :
  - Corps sweater (p. 57) : `#el_epaule` 1,5 ; `#el_carrure` 1,5 ; `#desc_carrure` 1,5 ;
    `#el_dessous_bras` 3,5 ; `#desc_dessous_bras` 3 ; `#el_bas` 2 ; côté droit (pas de taille).
  - Encolure sweater (p. 57) : `#degag_epaule` 3,5 ; `#desc_dos` 2 ; `#desc_devant` 3,5. Ligne
    de couture du bord-côte (le livre : élargissements « calculés pour un passage de tête
    confortable » en finition bord-côtes).
  - Épaule (p. 48) : `#decal_epaule` 1,8.
  - Côté avancé (lecture du dessin, question 1) : `#avance_cote` 8 au bas ; `#haut_fente` 5
    au-dessus du bas du corps (fente totale ≈ 11 avec le bord-côte).
  - Bord-côtes : `#red_bc` 3/4 (p. jogging, fig. 3) ; `#bc_encolure` 2,5 ; `#bc_poignet` 7 ;
    `#bc_bas` 6 (hauteurs finies).
  - Manche : `#long_manche` = `arm_shoulder_tip_to_wrist + #blouse_manche - #el_epaule -
    #bc_poignet`, `#blouse_manche` 2 ; `#aisance_poignet` 8 (bas de manche froncé dans le poignet).
  - Poche : `#larg_poche` 12 ; `#haut_poche` 10 ; `#haut_haut_poche` 5.

## Étapes
### 1. Élargissement sweater (p. 57)
1. vK : H→K prolongé de `#el_epaule`
2. vD descendu de `#desc_carrure` sur l'axe ; vD1, vD2 : `Line_D_D1 + #el_carrure`, `Line_D_D2 + #el_carrure`
3. vC2 : C2 sorti de `#el_dessous_bras` puis descendu de `#desc_dessous_bras`
4. vA1 : A→A1 prolongé de `#el_bas`
5. Côté droit vC2–vA1 (sweater : pas de cintrage)
6. Platitudes d'emmanchure en vC2, perpendiculaires au côté : devant 1,5 (vC3d), dos 1 (vC3b)
7. Emmanchures devant vK–vD1–vC3d et dos vK–vD2–vC3b

### 2. Encolure (p. 57)
8. vH : sur H→K à `#degag_epaule` ; vF : milieu dos descendu de `#desc_dos` ; vE : milieu
   devant descendu de `#desc_devant`
9. Encolure dos : platitude perpendiculaire au milieu dos depuis vF (vF3, longueur `Line_F_F1`), puis courbe jusqu'à l'épaule
10. Encolure devant : courbe vH → vE, platitude perpendiculaire au milieu devant en vE

### 3. Déplacement de l'épaule (p. 48)
11. Comme le haut de pyjama : parallèle à vH–vK côté devant à `#decal_epaule` (vHp, vKp),
    reportée au dos par symétrie (vHpp, vKpp)

### 4. Côté avancé, fentes et bas
12. Bas droit A–vA1 sur les deux pièces (pas de prolongement du milieu devant : il corrige la
    poitrine d'une femme, question 2)
13. vA1d : sur A→vA1, recul de `#avance_cote` (bas du côté devant) ; vA1b : symétrique de vA1d
    par rapport au côté vC2–vA1 (bas du côté dos, même longueur de côté)
14. Côté devant vC2–vA1d, côté dos vC2–vA1b ; crans de haut de fente vFd, vFb à `#haut_fente`
    du bas

### 5. Manche (p. 60 fig. 2, p. 68-72)
15. Manche de base reconstruite sur la nouvelle emmanchure (même construction que le haut de
    pyjama, `#creux_tete_dos` 2), longueur `#long_manche`, bas `arm_wrist_circ + #aisance_poignet`
16. Contrôle d'embu (0,5 à 1) ; crans p. 72

### 6. Bord-côtes et poche (blocs séparés)
17. Encolure : rectangle `#red_bc` × encolure de couture (dos + devant, × 2) sur `2 × #bc_encolure`
18. Poignet : `#red_bc` × bas de manche sur `2 × #bc_poignet`
19. Bas devant : `#red_bc` × bas devant (× 2) ; bas dos : `#red_bc` × bas dos (× 2) ; sur `2 × #bc_bas`
20. Poche `#larg_poche` × `#haut_poche` ; haut de poche `#larg_poche` × `2 × #haut_haut_poche`

### Pièces
21. Couture 0,7 partout (bas, poignets et encolure montés en bord-côtes : pas d'ourlet).

## Réalisation (2026-10-20, `patrons/sweat_homme.sm2d`)

Généré par script à partir de `haut_pyjama.sm2d` (encolure V, bas liquette et côté cintré
retirés), **exporté sans erreur par Seamly2D Linux** (même version que le PC) dans la session
cloud. Blocs : « Corps » (Devant, Dos), « Manche », « Bord-côtes et poche », « Carré 5x5 ».
Écarts au fichier d'étapes :
- Embu : avec le creux du livre en G3 (1) la tête est plus courte que l'emmanchure sweater
  (−1,06). `#creux_tete_dos` porté à 3 : embu 0,75. Autre réglage possible : creux 2 et
  hauteur de tête 0,70 au lieu de 2/3 (embu 0,53).
- Tête de manche : courbes simples, poignées égales, ajustées pour passer à 0,03 de G3 et 0,02
  de H3 (départ dans le prolongement des platitudes, arrivée horizontale en E).
- Points techniques : vAf (pied pour la symétrie du côté), vA1d, vA1b, vFd, vFb (crans de fente).

Valeurs T44 homme (export Seamly) :

| Grandeur | Valeur |
|---|---|
| Emmanchure dos + devant (platitudes comprises) | 51,80 |
| Tête de manche / **embu** | 52,54 / **0,75** |
| Largeur de manche / longueur (sans poignet) | 39,85 / 57,50 |
| Côté devant / dos | 40,33 / 40,34 |
| Demi-largeur au dessous de bras (devant = dos) | 25,31 (tour fini 101,2 pour 88 de poitrine) |
| Bas devant (entre fentes) / dos (entre fentes) | 34,0 / 66,0 |
| Encolure de couture | 52,1 |
| Longueur milieu dos, bord-côte compris | 69,1 |
| Bord-côtes coupés : encolure / poignet / bas devant / bas dos | 39,1 × 5 / 18,9 × 14 / 25,5 × 12 / 49,5 × 12 |

## Contrôles
- Épaules devant et dos de même longueur ; côtés devant et dos de même longueur.
- Embu 0,5 à 1.
- Encolure de couture : 52,1 pour un tour de tête de 56,7 (T44 homme). Le passage de tête
  repose sur l'élasticité du molleton et du bord-côte (encolure du livre p. 57, non modifiée).
- Bord-côtes : longueur = 3/4 de la ligne mesurée.

## Décisions
- 2026-10-20 : Thomas demande le sweat **homme T44** (`mesures/homme/T44.smms`).
- 2026-10-20 : embu réglé par le creux de la tête côté dos (même levier que le haut de pyjama,
  décision 8) : 3 au lieu de 1, embu 0,75.

## Questions ouvertes (tracé fait avec la recommandation, à confirmer)
1. **Fentes** : sur le dessin, elles sont sur le devant à ~8 cm des côtés, et le bord-côte du
   dos est d'un seul tenant. Lecture retenue : couture de côté avancée en biais (0 sous le
   bras, 8 cm au bas), ouverte en fente au bas. Autre lecture : couture de côté normale, fente
   sur le côté.
2. **Milieu devant** : pas de prolongement de 1 à 1,5 (correction de poitrine, inutile en homme).
3. **Déplacement d'épaule 1,8** : gardé comme sur le haut de pyjama.
4. **Hauteurs** : bord-côte encolure 2,5, poignets 7, bas 6 (lues sur le dessin), réduction
   3/4 partout (livre, jogging).
5. **Longueur** : corps arrêté sur la ligne de hanches (A), bord-côte de bas en dessous.
6. **Poche** : 12 × 15 au total, à gauche porté, à 4 cm du milieu devant, haut à 9 cm sous
   l'encolure (proportions du dessin). Pas encore de repère de placement sur le devant.
