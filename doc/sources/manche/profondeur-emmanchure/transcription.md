# Profondeur d'emmanchure : transcription de la vidéo

Source : vidéo Meriame Couture (Facebook, 54 s), copie locale dans `doc/` :
`Comment trouver la profondeur d emmanchure C est une question qu on m a souvent posé… (2).mp4`.
Parole transcrite automatiquement (Whisper) puis corrigée ; gestes relevés sur les images.

## Parole

> Tu veux tracer le patron de ta manche mais tu ne sais pas comment trouver la profondeur
> d'emmanchure ? Reste ici, je te montre comment faire.
>
> Prends ton patron devant et le patron dos et place-les côté contre côté, bien l'un contre
> l'autre, afin d'avoir la forme de l'emmanchure totale.
>
> Relie l'extrémité des deux emmanchures, trace un trait, divise-le en deux et relie le
> milieu du trait avec le côté.
>
> Mesure ce trait que tu viens de tracer et place la mesure sur une feuille de papier.
> On va devoir faire un calcul. Moi j'ai 17,2 cm.
>
> Le calcul est le suivant : 17,2 − (17,2 / 5) = 17,2 − 3,44 = 13,8 cm, qui correspond à
> la mesure de ma profondeur d'emmanchure.
>
> Ce qui veut dire que sur le patron [de manche], pour trouver ma ligne de profondeur
> d'emmanchure, je vais descendre à partir du haut de 13,8 cm.

## Gestes (images)

- Devant et dos posés à plat, coutures de côté jointives au dessous de bras.
- Trait entre les deux bouts d'épaule ; mesure au mètre ruban du milieu de ce trait jusqu'au
  point de côté (dessous de bras) : 17,2 cm.
- Calcul écrit à la main : `17,2 − (17,2/5) = 17,2 − 3,44 = 13,76 ≈ 13,8`.
- Sur la manche : lignes de construction dos / devant, tête de manche tracée au-dessus.

## Lecture pour le projet

- Le trait mesuré (X) correspond à la `prof_emm` du livre (manche montée jersey).
- Les 13,8 cm de la vidéo sont en réalité une **hauteur de tête de manche** (4/5 de X).
  Le livre utilise 2/3 de X pour le jersey : **on garde 2/3** (décision du 2026-09-27).
- Dans `patrons/fond_base_maille.sm2d`, devant et dos partagent le bout d'épaule K : le milieu
  des deux bouts d'épaule devient K1 = pied de la perpendiculaire de K sur la ligne de côté
  B1–C2 prolongée, et `prof_emm = Line_C2_K1` (≈ 19,5 cm en T44, calcul approché).
  Si les bouts d'épaule devant et dos diffèrent un jour, revenir au milieu des deux.
