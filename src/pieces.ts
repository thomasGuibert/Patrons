/**
 * Le catalogue des pièces que l'atelier sait tracer (fonds, manches, cols), rangées par partie du vêtement.
 * Les vêtements complets n'y figurent pas : ils sont au catalogue de chaque gamme.
 */

/** Le matériau : tissu qui s'étire (maille) ou tissu tissé (chaîne et trame). */
export type Matiere = "maille" | "chaine-trame";

/** Le type de couture : le flou (vêtements souples) ou le tailleur (vêtements construits). */
export type Couture = "flou" | "tailleur";

export type Piece = {
  nom: string;
  note: string;
  matieres: Matiere[];
  coutures: Couture[];
  /** Déjà tracée dans un patron de l'atelier (les autres sont prêtes à tracer). */
  tracee?: boolean;
};

export type Partie = { titre: string; script: string; pieces: Piece[] };

export const matieres: Record<Matiere, { nom: string; aide: string }> = {
  maille: { nom: "Maille", aide: "Jersey, molleton : le tissu s'étire" },
  "chaine-trame": { nom: "Chaîne et trame", aide: "Toile, lainage : le tissu ne s'étire pas" },
};

export const coutures: Record<Couture, { nom: string; aide: string }> = {
  flou: { nom: "Flou", aide: "Chemisiers, robes, hauts souples" },
  tailleur: { nom: "Tailleur", aide: "Vestes, tailleurs, manteaux" },
};

export const parties: Partie[] = [
  {
    titre: "Corps",
    script: "devant & dos",
    pieces: [
      { nom: "Fond de base maille", note: "Devant et dos sans pince, pour tous les hauts en jersey.", matieres: ["maille"], coutures: ["flou"], tracee: true },
      { nom: "Corsage à pinces", note: "La base près du corps, d'où partent tous les corsages et toutes les vestes.", matieres: ["chaine-trame"], coutures: ["flou", "tailleur"], tracee: true },
      { nom: "Fond de corsage", note: "La base à pinces élargie pour chemisiers et robes.", matieres: ["chaine-trame"], coutures: ["flou"] },
      { nom: "Fond sans pince", note: "Pour les vêtements amples.", matieres: ["chaine-trame", "maille"], coutures: ["flou"] },
      { nom: "Fond tailleur près du corps", note: "La base élargie pour se porter sur un chemisier.", matieres: ["chaine-trame"], coutures: ["tailleur"], tracee: true },
      { nom: "Corsage cinq pièces", note: "Coupe à petit côté, pour le très ajusté.", matieres: ["chaine-trame"], coutures: ["tailleur"] },
    ],
  },
  {
    titre: "Manches",
    script: "montées",
    pieces: [
      { nom: "Manche montée maille", note: "La manche de base des hauts en jersey, avec ses crans.", matieres: ["maille"], coutures: ["flou"], tracee: true },
      { nom: "Manche montée", note: "La manche de base en une pièce, avec son embu.", matieres: ["chaine-trame"], coutures: ["flou", "tailleur"] },
      { nom: "Manche tailleur deux pièces", note: "Dessus et dessous de manche, coudée.", matieres: ["chaine-trame"], coutures: ["tailleur"], tracee: true },
      { nom: "Manche chemisier et poignet", note: "Blousante au poignet, avec évasements ou plis.", matieres: ["chaine-trame"], coutures: ["flou"] },
      { nom: "Manche coudée", note: "Ajustée, avec une pince de coude.", matieres: ["chaine-trame"], coutures: ["flou"] },
      { nom: "Manche gaine", note: "Très moulante, en maille ou en biais.", matieres: ["chaine-trame", "maille"], coutures: ["flou"] },
      { nom: "Manche gigot", note: "Ample en tête, ajustée à l'avant-bras ; deux versions.", matieres: ["chaine-trame"], coutures: ["flou"] },
      { nom: "Manches ballon, bouffante, papillon", note: "Les manches courtes évasées.", matieres: ["chaine-trame"], coutures: ["flou"] },
    ],
  },
  {
    titre: "Cols et encolures",
    script: "pour finir",
    pieces: [
      { nom: "Encolure V en bande de jersey", note: "Bande d'encolure piquée au milieu devant.", matieres: ["maille"], coutures: ["flou"], tracee: true },
      { nom: "Col officier", note: "Col droit montant, sans pied.", matieres: ["chaine-trame"], coutures: ["flou", "tailleur"] },
      { nom: "Col montant à pinces", note: "L'encolure prolongée en entonnoir.", matieres: ["chaine-trame"], coutures: ["flou"] },
      { nom: "Col évasé et col Médicis", note: "Cols montants qui s'ouvrent vers le haut.", matieres: ["chaine-trame"], coutures: ["flou"] },
      { nom: "Col cavalier", note: "Col de chemise, col et pied d'une seule pièce.", matieres: ["chaine-trame"], coutures: ["flou"] },
      { nom: "Col transformable", note: "Se porte fermé ou ouvert.", matieres: ["chaine-trame"], coutures: ["flou"] },
      { nom: "Col Claudine", note: "Col plat aux pointes arrondies.", matieres: ["chaine-trame"], coutures: ["flou"] },
      { nom: "Col Eton", note: "Col plat aux pointes droites.", matieres: ["chaine-trame"], coutures: ["flou"] },
      { nom: "Col tailleur, cassure droite", note: "Col et revers de veste, avec parementure.", matieres: ["chaine-trame"], coutures: ["tailleur"] },
      { nom: "Col tailleur, cassure courbe", note: "Le revers roule en arrondi.", matieres: ["chaine-trame"], coutures: ["tailleur"] },
      { nom: "Col châle", note: "Col et revers d'un seul tenant, avec dessous de col.", matieres: ["chaine-trame"], coutures: ["tailleur"] },
      { nom: "Grand col châle", note: "Le châle élargi sur les épaules.", matieres: ["chaine-trame"], coutures: ["tailleur"] },
      { nom: "Petit col châle", note: "Un châle montant, plus étroit.", matieres: ["chaine-trame"], coutures: ["tailleur"] },
      { nom: "Capuche", note: "Tracée depuis l'encolure du vêtement.", matieres: ["chaine-trame", "maille"], coutures: ["flou", "tailleur"] },
    ],
  },
  {
    titre: "Pantalons",
    script: "jambes",
    pieces: [
      { nom: "Fond de pantalon droit", note: "Devant et dos, la base de tous les pantalons.", matieres: ["maille"], coutures: ["flou"], tracee: true },
    ],
  },
];
