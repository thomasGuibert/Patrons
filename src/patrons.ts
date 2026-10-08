import type { StaticImageData } from "next/image";
import fondBaseMaille from "../vignettes/fond_base_maille_fiche.png";
import fondPantalonDroit from "../vignettes/fond_pantalon_droit_fiche.png";

export type Statut = "verifie" | "trace" | "en-cours";

export type Patron = {
  slug: string;
  nom: string;
  resume: string;
  statut: Statut;
  vignette?: StaticImageData;
  description?: string;
  caracteristiques?: { libelle: string; valeur: string }[];
  valeurs?: { titre: string; lignes: { libelle: string; cm: string }[] };
};

export const libellesStatut: Record<Statut, string> = {
  verifie: "Tracé et vérifié",
  trace: "Tracé",
  "en-cours": "En cours",
};

export const patrons: Patron[] = [
  {
    slug: "fond-pantalon-droit",
    nom: "Fond de pantalon droit",
    resume: "Devant et dos, base de tous les pantalons.",
    statut: "verifie",
    vignette: fondPantalonDroit,
    description:
      "La base de tous les pantalons du catalogue : un devant et un dos, tracés sur le même axe, puis relevés séparément.",
    caracteristiques: [
      { libelle: "Taille", valeur: "44" },
      { libelle: "Pièces", valeur: "Devant ×2, dos ×2" },
      { libelle: "Hauteur", valeur: "100,1 cm" },
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
    resume: "Devant, dos et manche pour le jersey.",
    statut: "trace",
    vignette: fondBaseMaille,
    description:
      "Le fond des hauts en jersey : un devant, un dos et une manche, d'où part le haut de pyjama.",
    caracteristiques: [
      { libelle: "Taille", valeur: "44" },
      { libelle: "Pièces", valeur: "Devant, dos, manche" },
    ],
  },
  {
    slug: "haut-pyjama",
    nom: "Haut de pyjama col V",
    resume: "T-shirt souple en jersey, tiré du fond maille.",
    statut: "en-cours",
    description:
      "Un T-shirt souple à encolure V, élargi à partir du fond de base maille, avec une manche reconstruite sur la nouvelle emmanchure.",
  },
  {
    slug: "bas-pyjama",
    nom: "Bas de pyjama",
    resume: "Pantalon à taille élastique, tiré du fond droit.",
    statut: "en-cours",
    description:
      "Un pantalon en jersey à taille élastique, adapté du fond de pantalon droit.",
  },
];

export function trouverPatron(slug: string): Patron | undefined {
  return patrons.find((p) => p.slug === slug);
}
