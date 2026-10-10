/**
 * Mesures du corps que les patrons utilisent, sous leur nom Seamly (`mesures/*.smms`).
 * Le libellé et l'aide servent au tableau « Mes mesures » de chaque fiche.
 */
export const mesures = {
  bust_circ: {
    libelle: "Tour de poitrine",
    aide: "Ruban horizontal, à l'endroit le plus fort de la poitrine.",
  },
  waist_circ: {
    libelle: "Tour de taille",
    aide: "Au creux de la taille, ruban à plat sans serrer.",
  },
  hip_circ: {
    libelle: "Tour de hanches",
    aide: "Ruban horizontal, à l'endroit le plus fort des fesses.",
  },
  neck_circ: {
    libelle: "Tour d'encolure",
    aide: "À la base du cou, en passant sur la vertèbre saillante.",
  },
  neck_back_to_waist_b: {
    libelle: "Longueur taille dos",
    aide: "De la vertèbre saillante du cou jusqu'à la taille, au milieu du dos.",
  },
  neck_front_to_waist_f: {
    libelle: "Longueur taille devant",
    aide: "Du creux à la base du cou jusqu'à la taille, au milieu devant.",
  },
  across_back_b: {
    libelle: "Carrure dos",
    aide: "D'un pli de bras à l'autre dans le dos, une dizaine de centimètres sous la nuque.",
  },
  across_chest_f: {
    libelle: "Carrure devant",
    aide: "D'un pli de bras à l'autre devant, à mi-chemin entre l'épaule et la poitrine.",
  },
  shoulder_length: {
    libelle: "Longueur d'épaule",
    aide: "De la base du cou jusqu'au bout de l'épaule.",
  },
  arm_shoulder_tip_to_wrist: {
    libelle: "Longueur de bras",
    aide: "Du bout de l'épaule jusqu'au poignet, bras légèrement plié.",
  },
  arm_wrist_circ: {
    libelle: "Tour de poignet",
    aide: "Autour du poignet, sur l'os.",
  },
  height_waist_side: {
    libelle: "Hauteur taille-sol",
    aide: "Sur le côté, de la taille jusqu'au sol, pieds nus.",
  },
  height_waist_side_to_hip: {
    libelle: "Hauteur taille-hanches",
    aide: "Sur le côté, de la taille jusqu'à la ligne du tour de hanches.",
  },
  height_waist_side_to_knee: {
    libelle: "Hauteur taille-genou",
    aide: "Sur le côté, de la taille jusqu'au milieu du genou.",
  },
  leg_crotch_to_floor: {
    libelle: "Hauteur entrejambe-sol",
    aide: "À l'intérieur de la jambe, de l'entrejambe jusqu'au sol, pieds nus.",
  },
} satisfies Record<string, { libelle: string; aide: string }>;

export type CodeMesure = keyof typeof mesures;

export function estCodeMesure(code: string): code is CodeMesure {
  return Object.hasOwn(mesures, code);
}

/** Mesures saisies par l'utilisateur, en cm, telles qu'il les a tapées (« 88,5 »). */
export type MesMesures = Partial<Record<CodeMesure, string>>;

/** Lit « 88,5 » ou « 88.5 » ; undefined si ce n'est pas une mesure plausible en cm. */
export function lireCm(texte: string): number | undefined {
  const t = texte.trim().replace(",", ".");
  if (!/^\d+(\.\d+)?$/.test(t)) return undefined;
  const cm = Number(t);
  return cm > 0 && cm < 300 ? cm : undefined;
}
