/** Tailles disponibles pour tous les patrons, et mesures du corps de chaque taille (cm). */
export const tailles = [36, 38, 40, 42, 44] as const;
export type Taille = (typeof tailles)[number];
export const tailleParDefaut: Taille = 40;

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
  /** Valeur de chaque taille, dans l'ordre de `tailles` (mesures/T36.smms à T44.smms). */
  cm: number[];
  /** Nom de la mesure dans les fichiers de mesures, pour tracer le patron sur mesure. Jamais affiché. */
  seamly: string;
  /** Comment la prendre, en une phrase. */
  conseil: string;
};

export const mesuresCorps: Record<Mesure, MesureCorps> = {
  poitrine: { libelle: "Tour de poitrine", cm: [84, 88, 92, 96, 100], seamly: "bust_circ",
    conseil: "Autour de la poitrine, à l'endroit le plus fort, ruban bien horizontal sous les bras." },
  taille: { libelle: "Tour de taille", cm: [64, 68, 72, 76, 80], seamly: "waist_circ",
    conseil: "Autour de la taille, au creux, au-dessus du nombril. Nouez-y un cordon : il sert de repère aux autres mesures." },
  hanches: { libelle: "Tour de hanches", cm: [90, 94, 98, 102, 106], seamly: "hip_circ",
    conseil: "Autour des hanches, à l'endroit le plus fort des fesses, pieds joints." },
  encolure: { libelle: "Tour d'encolure", cm: [35, 36, 37, 38, 39], seamly: "neck_circ",
    conseil: "Autour de la base du cou, en passant sur l'os saillant de la nuque." },
  longueurDos: { libelle: "Longueur taille dos", cm: [40.5, 41, 41.5, 42, 42.5], seamly: "neck_back_to_waist_b",
    conseil: "Au milieu du dos, de l'os saillant de la nuque jusqu'au cordon de taille." },
  longueurDevant: { libelle: "Longueur taille devant", cm: [36.5, 37, 37.5, 38, 38.5], seamly: "neck_front_to_waist_f",
    conseil: "Au milieu devant, du creux à la base du cou jusqu'au cordon de taille." },
  carrureDos: { libelle: "Carrure dos", cm: [34.5, 35, 35.5, 36, 36.5], seamly: "across_back_b",
    conseil: "Dans le dos, d'un pli de bras à l'autre, à mi-chemin entre l'épaule et le dessous du bras, bras le long du corps." },
  carrureDevant: { libelle: "Carrure devant", cm: [32.5, 33, 33.5, 34, 34.5], seamly: "across_chest_f",
    conseil: "Sur le devant, d'un pli de bras à l'autre, à mi-chemin entre l'épaule et le dessous du bras." },
  epaule: { libelle: "Longueur d'épaule", cm: [11.6, 12, 12.4, 12.8, 13.2], seamly: "shoulder_length",
    conseil: "Sur le dessus de l'épaule, de la base du cou jusqu'au bout de l'épaule." },
  bras: { libelle: "Longueur de bras", cm: [60, 60, 60, 60, 60], seamly: "arm_shoulder_tip_to_wrist",
    conseil: "Du bout de l'épaule jusqu'à l'os du poignet, bras légèrement plié." },
  poignet: { libelle: "Tour de poignet", cm: [15.75, 16, 16.25, 16.5, 16.75], seamly: "arm_wrist_circ",
    conseil: "Autour du poignet, sur l'os." },
  tailleSol: { libelle: "Hauteur taille-sol", cm: [105.5, 105.5, 106.5, 106.5, 107.5], seamly: "height_waist_side",
    conseil: "Sur le côté, du cordon de taille jusqu'au sol, pieds nus." },
  tailleHanches: { libelle: "Hauteur taille-hanches", cm: [22, 22, 22, 22, 22], seamly: "height_waist_side_to_hip",
    conseil: "Sur le côté, du cordon de taille jusqu'à la ligne des hanches." },
  tailleGenou: { libelle: "Hauteur taille-genou", cm: [57, 58, 59, 60, 61], seamly: "height_waist_side_to_knee",
    conseil: "Sur le côté, du cordon de taille jusqu'au milieu du genou." },
  entrejambeSol: { libelle: "Hauteur entrejambe-sol", cm: [79.5, 79, 79.5, 79, 79.5], seamly: "leg_crotch_to_floor",
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
