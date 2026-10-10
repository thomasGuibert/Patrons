import type { StaticImageData } from "next/image";
import fondBaseMaille from "../vignettes/fond_base_maille_fiche.png";
import fondBaseMaillePlanche from "../vignettes/fond_base_maille_planche.png";
import fondPantalonDroit from "../vignettes/fond_pantalon_droit_fiche.png";
import fondPantalonDroitPlanche from "../vignettes/fond_pantalon_droit_planche.png";
import hautPyjama from "../vignettes/haut_pyjama_fiche.png";
import basPyjama from "../vignettes/bas_pyjama_fiche.png";
import type { CodeMesure } from "./mesures";
import type { Mesure } from "./tailles";

export type Famille = "vetement" | "base";

export type Patron = {
  slug: string;
  nom: string;
  famille: Famille;
  /** Référence de catalogue : « Réf. 101 » pour un vêtement, « Planche n° 001 » pour une base. */
  ref: string;
  resume: string;
  enCours?: boolean;
  /** Le patron puis le vêtement cousu, en largeur. */
  vignette?: StaticImageData;
  /** Les pièces seules, pour le rayon des bases. */
  planche?: StaticImageData;
  description?: string;
  caracteristiques?: { libelle: string; valeur: string }[];
  valeurs?: { titre: string; lignes: { libelle: string; cm: string }[] };
  /** Mesures du corps montrées dans le tableau des tailles. */
  mesures: Mesure[];
  /** Toutes les mesures du corps que le tracé (`patrons/*.sm2d`) utilise : le tableau « Mes mesures ». */
  mesuresTrace: CodeMesure[];
};

const traceHaut: CodeMesure[] = [
  "bust_circ",
  "waist_circ",
  "hip_circ",
  "neck_circ",
  "neck_back_to_waist_b",
  "neck_front_to_waist_f",
  "across_back_b",
  "across_chest_f",
  "shoulder_length",
  "arm_shoulder_tip_to_wrist",
  "arm_wrist_circ",
  "height_waist_side_to_hip",
];

const tracePantalon: CodeMesure[] = [
  "waist_circ",
  "hip_circ",
  "height_waist_side",
  "height_waist_side_to_hip",
  "height_waist_side_to_knee",
  "leg_crotch_to_floor",
];

export const patrons: Patron[] = [
  {
    slug: "haut-pyjama",
    nom: "Haut de pyjama col V",
    famille: "vetement",
    ref: "Réf. 101",
    resume: "T-shirt souple en jersey, à manches longues.",
    vignette: hautPyjama,
    description:
      "Un T-shirt souple à encolure V et manches longues, à coudre dans un jersey.",
    mesures: ["poitrine", "taille", "hanches"],
    mesuresTrace: traceHaut,
    caracteristiques: [
      { libelle: "Pièces", valeur: "Devant, dos, manche ×2, bande d'encolure" },
    ],
  },
  {
    slug: "bas-pyjama",
    nom: "Bas de pyjama",
    famille: "vetement",
    ref: "Réf. 102",
    resume: "Pantalon en jersey à taille élastique.",
    vignette: basPyjama,
    description: "Un pantalon en jersey à taille élastique, droit et confortable.",
    mesures: ["taille", "hanches", "tailleSol"],
    mesuresTrace: tracePantalon,
    caracteristiques: [
      { libelle: "Pièces", valeur: "Devant ×2, dos ×2, ceinture" },
    ],
  },
  {
    slug: "fond-pantalon-droit",
    nom: "Fond de pantalon droit",
    famille: "base",
    ref: "Planche n° 001",
    resume: "Devant et dos, à adapter à son propre modèle.",
    vignette: fondPantalonDroit,
    planche: fondPantalonDroitPlanche,
    description:
      "La base de tous les pantalons du catalogue : un devant et un dos, à transformer pour dessiner son propre modèle.",
    mesures: ["taille", "hanches", "tailleSol"],
    mesuresTrace: tracePantalon,
    caracteristiques: [
      { libelle: "Pièces", valeur: "Devant ×2, dos ×2" },
    ],
    valeurs: {
      titre: "Aisances et valeurs de mode",
      lignes: [
        { libelle: "Aisance au tour de taille", cm: "4" },
        { libelle: "Aisance au tour de hanches", cm: "2" },
        { libelle: "Taille descendue sous la taille morphologique", cm: "4" },
        { libelle: "Largeur au genou", cm: "48" },
        { libelle: "Largeur du bas", cm: "40" },
      ],
    },
  },
  {
    slug: "fond-base-maille",
    nom: "Fond de base maille",
    famille: "base",
    ref: "Planche n° 002",
    resume: "Devant, dos et manche, pour les hauts en jersey.",
    vignette: fondBaseMaille,
    planche: fondBaseMaillePlanche,
    description:
      "Le fond des hauts en jersey : un devant, un dos et une manche, à transformer pour dessiner son propre modèle.",
    mesures: ["poitrine", "taille", "hanches"],
    mesuresTrace: traceHaut,
    caracteristiques: [
      { libelle: "Pièces", valeur: "Devant, dos, manche ×2" },
    ],
  },
];

export const rayons: { famille: Famille; titre: string; script: string; note: string }[] = [
  { famille: "vetement", titre: "Vêtements", script: "à coudre", note: "" },
  { famille: "base", titre: "Bases", script: "à transformer", note: "Des fonds à adapter à son propre modèle" },
];

export function trouverPatron(slug: string): Patron | undefined {
  return patrons.find((p) => p.slug === slug);
}
