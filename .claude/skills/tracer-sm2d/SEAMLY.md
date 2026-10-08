# Seamly2D : syntaxe et pièges

Seamly2D v2026.7, format de fichier `<version>0.7.4</version>`. Exécutable :
`C:\Program Files (x86)\Seamly2D\seamly2d.exe`. Exemples officiels :
`C:\Program Files (x86)\Seamly2D\samples\patterns\*.sm2d`.

## Fichier

```xml
<pattern>
    <version>0.7.4</version>
    <unit>cm</unit>
    <description/>
    <notes/>
    <patternLabel>…</patternLabel>
    <measurements>../mesures/T44.smms</measurements>
    <variables>
        <variable description="…" formula="3/4" name="#frac_largeur"/>
    </variables>
    <draftBlock name="…">
        <calculation>…points, lignes, courbes…</calculation>
        <modeling>…copies des objets utilisés par les pièces…</modeling>
        <pieces>…</pieces>
        <groups/>
        <images/>
    </draftBlock>
</pattern>
```

- `id` : entiers uniques dans tout le fichier.
- **Noms de points uniques dans tout le fichier**, tous blocs confondus. Plusieurs pièces
  dans un même fichier → préfixe par bloc (`mA`, `mB`… pour la manche). Caractères : lettres,
  chiffres, `_` ; **pas d'apostrophe** : I' → `Ip`.
- Changer le nom d'un `draftBlock` est sans effet sur les formules.

## Formules

- Mesures : leur nom Seamly (`waist_circ`). Variables : `#nom`.
- **Les variables sont calculées avant les objets** : une variable qui lit `Line_…`,
  `SplPath_…` vaut 0, **sans erreur**. Toute formule qui lit le dessin va directement dans
  l'outil.
- `Line_X_Y`, `AngleLine_X_Y` n'existent que si un segment X→Y existe, **dans ce sens**
  (créé par l'outil du point ou par `<line>`, éventuellement `lineType="none"`). Sens inverse :
  `AngleLine_Y_X` = `(AngleLine_X_Y+180)`.
- Courbes : `Spl_<p1>_<p4>` (courbe simple), `SplPath_<premier>_<dernier>` (chemin) ;
  courbe dupliquée (`duplicate="1"`) : suffixe `_1`.
- Une formule peut lire un objet d'un autre bloc du même fichier (jamais d'un autre fichier).
- Angles en degrés, sens trigonométrique à l'écran : 0 droite, 90 haut, 180 gauche, 270 bas.

## Outils (points)

Attributs d'affichage communs : `mx="0.132292" my="0.264583" showPointName="true"`, et pour
les outils qui tracent un trait `lineColor="black" lineType="solidLine|dashLine|dotLine|none"
lineWeight="0.35"`.

```xml
<point id="1" name="A" type="single" x="0" y="0" …/>
<point id="2" name="B" type="endLine" basePoint="1" angle="0" length="#larg" …/>
<point id="3" name="E" type="alongLine" firstPoint="1" secondPoint="2" length="Line_A_B/2" …/>
<point id="4" name="G3" type="normal" firstPoint="10" secondPoint="11" length="1" angle="0" …/>
<point id="5" name="G1" type="lineIntersect" p1Line1="6" p2Line1="7" p1Line2="8" p2Line2="9" …/>
<point id="6" name="X1" type="lineIntersectAxis" basePoint="1" angle="…" p1Line="2" p2Line="3" …/>
<point id="7" name="K1" type="height" basePoint="26" p1Line="9" p2Line="29" …/>
<point id="8" name="N" type="cutSpline" spline="40" length="7" …/>
<point id="9" name="N2" type="cutSplinePath" splinePath="41" length="7" …/>
<line id="10" firstPoint="1" secondPoint="4" lineColor="black" lineType="solidLine" lineWeight="0.35"/>
```

- `normal` : direction premier→second point tournée de **+90°** (sens trigonométrique),
  puis `angle` ajouté. `angle="180"` place le point de l'autre côté. Vérifier le côté sur le
  PNG.
- `height` crée le segment base→pied, pas un segment vers les extrémités de la droite.

## Courbes

```xml
<spline id="20" type="simpleInteractive" point1="3" point4="5"
        angle1="7.44" length1="4.5" angle2="180" length2="9.5"
        color="black" lineWeight="0.35" penStyle="solidLine"/>
<spline id="21" type="pathInteractive" color="black" lineWeight="0.35" penStyle="solidLine">
    <pathPoint pSpline="3" angle1="…" length1="0" angle2="…" length2="2"/>
    <pathPoint pSpline="4" angle1="…" length1="2" angle2="…" length2="0"/>
</spline>
<spline id="22" type="cubicBezier" point1="3" point2="30" point3="31" point4="5" color="black"/>
```

- `angle2`/`length2` d'une `simpleInteractive` : poignée partant de `point4`.
- **Poignées déplaçables à la souris seulement si angle et longueur sont des nombres.**
  L'utilisateur veut des courbes interactives : poignées numériques, ajustées numériquement
  pour passer par les points du livre.
- `cubicBezier` : poignées fixées par des points construits (non déplaçables).

## Pièces

```xml
<modeling>
    <point id="100" idObject="1" inUse="true" type="modeling" mx="…" my="…" showPointName="true"/>
    <spline id="101" idObject="20" inUse="true" type="modelingSpline"/>   <!-- modelingPath pour un chemin -->
</modeling>
<pieces>
    <piece id="110" name="Manche" seamAllowance="true" width="0.7" version="2" inLayout="true"
           united="false" locked="false" forbidFlipping="false" hideMainPath="false"
           color="#ffffff" fill="nobrush" mx="0" my="0">
        <data … quantity="2" onFold="false" orientation="Indéfini" rotationWay="Aucun" tilt="Aucun"
              mx="755.9" my="1322.8" width="3" height="5" fontSize="0" visible="true">
            <line alignment="4" bold="false" italic="false" sfIncrement="3" text="%pName%"/>
            <line alignment="4" bold="false" italic="true" sfIncrement="0" text="%mFabric% X%pQuantity%"/>
        </data>
        <patternInfo fontSize="63" height="5" width="8" mx="…" my="…" rotation="0" visible="true"/>
        <grainline arrowLength="1.27" arrows="0" length="50" mx="…" my="…" rotation="90" visible="true"/>
        <nodes>
            <node idObject="100" type="NodePoint"/>
            <node idObject="101" reverse="0" type="NodeSpline"/>   <!-- NodeSplinePath pour un chemin -->
        </nodes>
    </piece>
</pieces>
```

- Les nœuds référencent les copies de `<modeling>`, pas les objets de `<calculation>`.
- Contour dans l'ordre ; `reverse="1"` parcourt la courbe à l'envers.
- **Sens du contour** : à l'écran (y vers le bas), parcourir la pièce dans le sens des aiguilles
  d'une montre (aire signée négative en y vers le haut, comme `fond_base_maille`). Dans l'autre
  sens, la couture est posée **à l'intérieur** et le plan de coupe superpose les pièces (haut de
  pyjama, 2026-10-08). Pour inverser : ordre des nœuds inversé, `reverse` 0↔1, `before`↔`after`.
- Point sur une courbe (cran) : répéter la courbe de part et d'autre du point dans la liste des
  nœuds ; Seamly coupe la courbe entre les points voisins.
- Cran : attributs de nœud `notch="true" notchType="slit" notchSubtype="straightforward"
  notchLength="0.4" notchWidth="0.25" notchAngle="0" notchCount="1" showNotch="true"
  showSecondNotch="true"` (jersey : cran ≤ 4 mm).
- `data`, `patternInfo`, `grainline` : `mx`/`my` en **pixels** (37,795 px/cm) dans le repère
  du brouillon ; le droit-fil part de (`mx`,`my`) et monte de `length` cm si `rotation="90"`.
- Étiquettes (`data`, `patternInfo`, `mx`/`my` = coin haut gauche, `width`/`height` en cm) et
  droit-fil : **toujours dans la pièce**, sans se superposer ni croiser le droit-fil. Une
  étiquette posée hors de la pièce est recentrée par Seamly, par-dessus l'autre. Pièce étroite
  (bande, ceinture) : étiquettes côte à côte, `arrowLength` réduit (0,5).
- Pièce de contrôle d'échelle (carré 5×5) : `seamAllowance="false"` pour une ligne imprimée
  exacte.

## Export en ligne de commande

```
seamly2d.exe -b <nom> -d <dossier> -f 0 --exportOnlyDetails <fichier.sm2d>   # SVG (3 = PNG)
```

Code de sortie 66 et ligne `CRITIQUE` en cas d'erreur (formule, symbole inconnu, fichier déjà
ouvert). Exporter une **copie** : le fichier ouvert dans Seamly est verrouillé. Le SVG est à
96 dpi ; le premier `<path>` du groupe `id="<pièce>"` est la ligne de couture.
