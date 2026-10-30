import type { StaticImageData } from "next/image";
import boleroF from "../vignettes/femme/bolero_fiche.png";
import bonnetBainF from "../vignettes/femme/bonnet_bain_fiche.png";
import ponchoBainF from "../vignettes/femme/poncho_bain_fiche.png";
import fondBaseMailleF from "../vignettes/femme/fond_base_maille_fiche.png";
import fondBaseMaillePlancheF from "../vignettes/femme/fond_base_maille_planche.png";
import fondPantalonDroitF from "../vignettes/femme/fond_pantalon_droit_fiche.png";
import fondPantalonDroitPlancheF from "../vignettes/femme/fond_pantalon_droit_planche.png";
import hautPyjamaF from "../vignettes/femme/haut_pyjama_fiche.png";
import basPyjamaF from "../vignettes/femme/bas_pyjama_fiche.png";
import fondBaseMailleH from "../vignettes/homme/fond_base_maille_fiche.png";
import fondBaseMaillePlancheH from "../vignettes/homme/fond_base_maille_planche.png";
import fondPantalonDroitH from "../vignettes/homme/fond_pantalon_droit_fiche.png";
import fondPantalonDroitPlancheH from "../vignettes/homme/fond_pantalon_droit_planche.png";
import hautPyjamaH from "../vignettes/homme/haut_pyjama_fiche.png";
import basPyjamaH from "../vignettes/homme/bas_pyjama_fiche.png";
import { mesuresBas, mesuresHaut, type Gamme, type Mesure } from "./tailles";

export type Famille = "vetement" | "base";

export type Patron = {
  slug: string;
  nom: string;
  famille: Famille;
  /** Référence de catalogue : « Réf. 101 » pour un vêtement, « Planche n° 001 » pour une base. */
  ref: string;
  resume: string;
  enCours?: boolean;
  /** Le patron puis le vêtement cousu, en largeur, tracé dans une taille de chaque gamme. */
  vignette: Partial<Record<Gamme, StaticImageData>>;
  /** Gammes où le patron existe ; toutes si absent. */
  gammes?: Gamme[];
  /** Pas de patron sur mesure tant que les mesures qu'il demande ne sont pas toutes saisissables. */
  sansSurMesure?: boolean;
  /** Un seul patron pour toutes les tailles : ce texte remplace le choix de taille et le tableau des tailles. */
  tailleUnique?: string;
  /** Nom public de chaque taille (« XS » pour 36…), à la place du numéro. */
  nomsTailles?: Record<number, string>;
  /** Faux tant que la gamme de montage n'est pas rédigée : pas de choix de notice, le dossier se limite à la nomenclature. */
  choixMontage?: boolean;
  /** Les pièces seules, pour le rayon des bases. */
  planche?: Partial<Record<Gamme, StaticImageData>>;
  description?: string;
  caracteristiques?: { libelle: string; valeur: string }[];
  valeurs?: { titre: string; lignes: { libelle: string; cm: string }[] };
  /** Mesures du corps montrées dans le tableau des tailles. */
  mesures: Mesure[];
  /** Toutes les mesures du corps dont le patron a besoin, à saisir pour le sur-mesure. */
  saisie: Mesure[];
  /** Le PDF commence par un dossier technique (public/pdf/<gamme>/dossier/), gamme de montage au choix. */
  dossier?: boolean;
};

export const patrons: Patron[] = [
  {
    slug: "bolero",
    nom: "Boléro à manches",
    famille: "vetement",
    ref: "Réf. 103",
    resume: "Veste courte bord à bord, en tissu, avec col officier et doublure.",
    gammes: ["femme"],
    sansSurMesure: true,
    vignette: { femme: boleroF },
    description:
      "Une veste courte à manches, bord à bord, à col officier, doublée. Le patron comprend la parementure et la doublure, avec leur nomenclature.",
    mesures: ["poitrine", "taille", "hanches"],
    saisie: mesuresHaut,
    dossier: true,
    choixMontage: false,
    caracteristiques: [
      { libelle: "Pièces", valeur: "Devant ×2, dos ×2, dessus et dessous de manche ×2, col officier ×2, parementure ×2" },
      { libelle: "Doublure", valeur: "Devant ×2, dos ×2, dessus et dessous de manche ×2" },
      { libelle: "Tissu", valeur: "Chaîne et trame" },
    ],
  },
  {
    slug: "bonnet-bain",
    nom: "Bonnet de bain cheveux longs",
    famille: "vetement",
    ref: "Réf. 104",
    resume: "Bonnet en maille de bain, avec de la place à l'arrière pour les cheveux longs.",
    gammes: ["femme"],
    sansSurMesure: true,
    tailleUnique: "Pour un tour de tête de 52 à 60 cm : la maille de bain s'ajuste.",
    vignette: { femme: bonnetBainF },
    description:
      "Un bonnet de bain en trois pièces, deux côtés et une bande centrale du front à la nuque. L'arrière s'arrondit pour loger les cheveux longs relevés.",
    mesures: [],
    saisie: [],
    caracteristiques: [
      { libelle: "Pièces", valeur: "Côté ×2, bande centrale au pli" },
      { libelle: "Tissu", valeur: "Maille de bain extensible (élasthanne), le plus grand sens d'élasticité autour de la tête" },
      { libelle: "Taille", valeur: "Unique, tour de tête de 52 à 60 cm" },
      { libelle: "Coutures", valeur: "0,6 cm comprises, bord rabattu de 1 cm" },
    ],
  },
  {
    slug: "poncho-bain",
    nom: "Poncho de bain",
    famille: "vetement",
    ref: "Réf. 105",
    resume: "Poncho ample en éponge à capuche, pour se sécher et se changer à l'abri des regards.",
    gammes: ["femme"],
    sansSurMesure: true,
    nomsTailles: { 36: "XS", 38: "S", 40: "M", 42: "L", 44: "XL" },
    vignette: { femme: ponchoBainF },
    description:
      "Un poncho ample en éponge, pour se sécher et se changer sur la plage ou sur un bateau. Capuche à coulisse qui reste en place, manches au coude, poche kangourou, et une ouverture de chaque côté pour passer les mains et s'habiller dessous. Trois longueurs dans le même patron.",
    mesures: ["poitrine", "hanches", "encolure", "bras"],
    saisie: [],
    dossier: true,
    caracteristiques: [
      { libelle: "Pièces", valeur: "Devant et dos au pli, manche ×2, capuche ×2, poche kangourou" },
      { libelle: "Longueurs", valeur: "Petit (mi-cuisse), normal (au-dessus du genou), grand (sous le genou), tracées sur le patron" },
      { libelle: "Tissu", valeur: "Éponge de coton bouclée, 350 à 450 g/m²" },
      { libelle: "Fournitures", valeur: "Cordon de capuche 1,30 m, biais 70 cm" },
    ],
  },
  {
    slug: "haut-pyjama",
    nom: "Haut de pyjama col V",
    famille: "vetement",
    ref: "Réf. 101",
    resume: "T-shirt souple en jersey, à manches longues.",
    vignette: { femme: hautPyjamaF, homme: hautPyjamaH },
    description:
      "Un T-shirt souple à encolure V et manches longues, à coudre dans un jersey.",
    mesures: ["poitrine", "taille", "hanches"],
    saisie: mesuresHaut,
    dossier: true,
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
    vignette: { femme: basPyjamaF, homme: basPyjamaH },
    description: "Un pantalon en jersey à taille élastique, droit et confortable.",
    mesures: ["taille", "hanches", "tailleSol"],
    saisie: mesuresBas,
    dossier: true,
    caracteristiques: [
      { libelle: "Pièces", valeur: "Devant ×2, dos ×2, taille repliée sur l'élastique" },
      { libelle: "Variante", valeur: "Short : ligne de coupe en tirets" },
    ],
  },
  {
    slug: "fond-pantalon-droit",
    nom: "Fond de pantalon droit",
    famille: "base",
    ref: "Planche n° 001",
    resume: "Devant et dos, à adapter à son propre modèle.",
    vignette: { femme: fondPantalonDroitF, homme: fondPantalonDroitH },
    planche: { femme: fondPantalonDroitPlancheF, homme: fondPantalonDroitPlancheH },
    description:
      "La base de tous les pantalons du catalogue : un devant et un dos, à transformer pour dessiner son propre modèle.",
    mesures: ["taille", "hanches", "tailleSol"],
    saisie: mesuresBas,
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
    vignette: { femme: fondBaseMailleF, homme: fondBaseMailleH },
    planche: { femme: fondBaseMaillePlancheF, homme: fondBaseMaillePlancheH },
    description:
      "Le fond des hauts en jersey : un devant, un dos et une manche, à transformer pour dessiner son propre modèle.",
    mesures: ["poitrine", "taille", "hanches"],
    saisie: mesuresHaut,
    caracteristiques: [
      { libelle: "Pièces", valeur: "Devant, dos, manche ×2" },
    ],
  },
];

export const rayons: { famille: Famille; titre: string; script: string; note: string }[] = [
  { famille: "vetement", titre: "Vêtements", script: "à coudre", note: "" },
  { famille: "base", titre: "Bases", script: "à transformer", note: "Des fonds à adapter à son propre modèle" },
];

export function dansGamme(p: Patron, g: Gamme): boolean {
  return !p.gammes || p.gammes.includes(g);
}

export function trouverPatron(slug: string): Patron | undefined {
  return patrons.find((p) => p.slug === slug);
}
