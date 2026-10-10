/** Tailles disponibles pour tous les patrons, et mesures du corps de chaque taille (cm). */
export const tailles = [36, 38, 40, 42, 44] as const;
export type Taille = (typeof tailles)[number];
export const tailleParDefaut: Taille = 40;

export type Mesure = "poitrine" | "taille" | "hanches" | "tailleSol";

export const mesuresCorps: Record<Mesure, { libelle: string; cm: string[] }> = {
  poitrine: { libelle: "Tour de poitrine", cm: ["84", "88", "92", "96", "100"] },
  taille: { libelle: "Tour de taille", cm: ["64", "68", "72", "76", "80"] },
  hanches: { libelle: "Tour de hanches", cm: ["90", "94", "98", "102", "106"] },
  tailleSol: { libelle: "Hauteur taille-sol", cm: ["105,5", "105,5", "106,5", "106,5", "107,5"] },
};
