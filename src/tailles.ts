/** Gammes de tailles (femme, homme), et mesures du corps de chaque taille (cm). */
export type Gamme = "femme" | "homme";
export type Taille = number;

export const gammes: Record<Gamme, { nom: string; tailles: Taille[]; parDefaut: Taille }> = {
  femme: { nom: "Femme", tailles: [36, 38, 40, 42, 44], parDefaut: 40 },
  homme: { nom: "Homme", tailles: [44, 46, 48, 50, 52, 54], parDefaut: 48 },
};
export const listeGammes = Object.keys(gammes) as Gamme[];

export function estGamme(g: string): g is Gamme {
  return g in gammes;
}

export type Mesure =
  | "poitrine"
  | "taille"
  | "hanches"
  | "encolure"
  | "longueurDos"
  | "longueurDevant"
  | "carrureDos"
  | "carrureDevant"
  | "epaule"
  | "bras"
  | "poignet"
  | "tailleSol"
  | "tailleHanches"
  | "tailleGenou"
  | "entrejambeSol";

export type MesureCorps = {
  libelle: string;
  /** Valeur de chaque taille de la gamme, dans l'ordre de `gammes[g].tailles` (mesures/<gamme>/T*.smms). */
  cm: Record<Gamme, number[]>;
  /** Nom de la mesure dans les fichiers de mesures, pour tracer le patron sur mesure. Jamais affiché. */
  seamly: string;
  /** Comment la prendre, en une phrase. */
  conseil: string;
};

export const mesuresCorps: Record<Mesure, MesureCorps> = {
  poitrine: { libelle: "Tour de poitrine", seamly: "bust_circ",
    cm: { femme: [84, 88, 92, 96, 100], homme: [88, 92, 96, 100, 104, 108] },
    conseil: "Autour de la poitrine, à l'endroit le plus fort, ruban bien horizontal sous les bras." },
  taille: { libelle: "Tour de taille", seamly: "waist_circ",
    cm: { femme: [64, 68, 72, 76, 80], homme: [76, 80, 84, 88, 92, 96] },
    conseil: "Autour de la taille, au creux, au-dessus du nombril. Nouez-y un cordon : il sert de repère aux autres mesures." },
  hanches: { libelle: "Tour de hanches", seamly: "hip_circ",
    cm: { femme: [90, 94, 98, 102, 106], homme: [90, 94, 98, 102, 106, 110] },
    conseil: "Autour des hanches, à l'endroit le plus fort des fesses, pieds joints." },
  encolure: { libelle: "Tour d'encolure", seamly: "neck_circ",
    cm: { femme: [35, 36, 37, 38, 39], homme: [38, 39, 40, 41, 42, 43] },
    conseil: "Autour de la base du cou, en passant sur l'os saillant de la nuque." },
  longueurDos: { libelle: "Longueur taille dos", seamly: "neck_back_to_waist_b",
    cm: { femme: [40.5, 41, 41.5, 42, 42.5], homme: [44.1, 44.4, 44.7, 45, 45.3, 45.6] },
    conseil: "Au milieu du dos, de l'os saillant de la nuque jusqu'au cordon de taille." },
  longueurDevant: { libelle: "Longueur taille devant", seamly: "neck_front_to_waist_f",
    cm: { femme: [36.5, 37, 37.5, 38, 38.5], homme: [39.9, 40.2, 40.5, 40.8, 41.1, 41.4] },
    conseil: "Au milieu devant, du creux à la base du cou jusqu'au cordon de taille." },
  carrureDos: { libelle: "Carrure dos", seamly: "across_back_b",
    cm: { femme: [34.5, 35, 35.5, 36, 36.5], homme: [37, 38, 39, 40, 41, 42] },
    conseil: "Dans le dos, d'un pli de bras à l'autre, à mi-chemin entre l'épaule et le dessous du bras, bras le long du corps." },
  carrureDevant: { libelle: "Carrure devant", seamly: "across_chest_f",
    cm: { femme: [32.5, 33, 33.5, 34, 34.5], homme: [32, 33, 34, 35, 36, 37] },
    conseil: "Sur le devant, d'un pli de bras à l'autre, à mi-chemin entre l'épaule et le dessous du bras." },
  epaule: { libelle: "Longueur d'épaule", seamly: "shoulder_length",
    cm: { femme: [11.6, 12, 12.4, 12.8, 13.2], homme: [13.7, 14, 14.3, 14.6, 14.9, 15.2] },
    conseil: "Sur le dessus de l'épaule, de la base du cou jusqu'au bout de l'épaule." },
  bras: { libelle: "Longueur de bras", seamly: "arm_shoulder_tip_to_wrist",
    cm: { femme: [60, 60, 60, 60, 60], homme: [64, 64, 64, 64, 64, 64] },
    conseil: "Du bout de l'épaule jusqu'à l'os du poignet, bras légèrement plié." },
  poignet: { libelle: "Tour de poignet", seamly: "arm_wrist_circ",
    cm: { femme: [15.75, 16, 16.25, 16.5, 16.75], homme: [17.2, 17.4, 17.6, 17.8, 18, 18.2] },
    conseil: "Autour du poignet, sur l'os." },
  tailleSol: { libelle: "Hauteur taille-sol", seamly: "height_waist_side",
    cm: { femme: [105.5, 105.5, 106.5, 106.5, 107.5], homme: [112.1, 111.9, 111.7, 111.5, 111.3, 111.1] },
    conseil: "Sur le côté, du cordon de taille jusqu'au sol, pieds nus." },
  tailleHanches: { libelle: "Hauteur taille-hanches", seamly: "height_waist_side_to_hip",
    cm: { femme: [22, 22, 22, 22, 22], homme: [20, 20, 20, 20, 20, 20] },
    conseil: "Sur le côté, du cordon de taille jusqu'à la ligne des hanches." },
  tailleGenou: { libelle: "Hauteur taille-genou", seamly: "height_waist_side_to_knee",
    cm: { femme: [57, 58, 59, 60, 61], homme: [62, 62, 62, 62, 62, 62] },
    conseil: "Sur le côté, du cordon de taille jusqu'au milieu du genou." },
  entrejambeSol: { libelle: "Hauteur entrejambe-sol", seamly: "leg_crotch_to_floor",
    cm: { femme: [79.5, 79, 79.5, 79, 79.5], homme: [85, 84.6, 84.2, 83.8, 83.4, 83] },
    conseil: "À l'intérieur de la jambe, de l'entrejambe jusqu'au sol, pieds nus." },
};

/** Les mesures des hauts (fond de base maille) et des bas (fond de pantalon droit). */
export const mesuresHaut: Mesure[] = [
  "poitrine", "taille", "hanches", "encolure", "longueurDos", "longueurDevant",
  "carrureDos", "carrureDevant", "epaule", "bras", "poignet", "tailleHanches",
];
export const mesuresBas: Mesure[] = [
  "taille", "hanches", "tailleSol", "tailleHanches", "tailleGenou", "entrejambeSol",
];

/** « 105,5 » : virgule décimale, sans zéros inutiles. */
export function enCm(cm: number): string {
  return String(Math.round(cm * 100) / 100).replace(".", ",");
}
