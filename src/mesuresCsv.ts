import { estCodeMesure, lireCm, mesures, type CodeMesure, type MesMesures } from "./mesures.ts";

/**
 * Fichier de mesures : une ligne par mesure, « code;mesure;cm », séparateur point-virgule et
 * virgule décimale pour s'ouvrir tel quel dans un tableur français.
 */
export function versCsv(valeurs: MesMesures): string {
  const lignes = ["code;mesure;cm"];
  for (const code of Object.keys(mesures) as CodeMesure[]) {
    const cm = lireCm(valeurs[code] ?? "");
    if (cm !== undefined) lignes.push(`${code};${mesures[code].libelle};${String(cm).replace(".", ",")}`);
  }
  return lignes.join("\r\n") + "\r\n";
}

export type Import = { valeurs: MesMesures; ignorees: number };

/**
 * Relit un fichier de mesures, même retouché dans un tableur : séparateur « ; », « , » ou
 * tabulation, mesure reconnue par son code ou son libellé, valeur dans la dernière colonne.
 */
export function depuisCsv(texte: string): Import {
  const parLibelle = new Map(
    (Object.keys(mesures) as CodeMesure[]).map((code) => [normaliser(mesures[code].libelle), code]),
  );
  const valeurs: MesMesures = {};
  let ignorees = 0;

  const lignes = texte.replace(/^﻿/, "").split(/\r?\n/).filter((l) => l.trim() !== "");
  for (const [i, ligne] of lignes.entries()) {
    const cellules = decouper(ligne);
    const code = cellules.find((c) => estCodeMesure(c.trim()))?.trim() as CodeMesure | undefined;
    const reconnu = code ?? cellules.map((c) => parLibelle.get(normaliser(c))).find(Boolean);
    const cm = lireCm(cellules.at(-1) ?? "");
    if (reconnu && cm !== undefined) valeurs[reconnu] = String(cm).replace(".", ",");
    else if (i > 0) ignorees++; // la première ligne est l'en-tête
  }
  return { valeurs, ignorees };
}

function decouper(ligne: string): string[] {
  const sep = ligne.includes(";") ? ";" : ligne.includes("\t") ? "\t" : ",";
  // Avec « , » comme séparateur, « 88,5 » se retrouve coupé en deux : on recolle la décimale.
  const cellules = ligne.split(sep).map((c) => c.replace(/^"|"$/g, ""));
  if (sep === "," && cellules.length > 1 && /^\d+$/.test(cellules.at(-1)!) && /^\d+$/.test(cellules.at(-2)!)) {
    const decimale = cellules.pop()!;
    cellules.push(`${cellules.pop()},${decimale}`);
  }
  return cellules;
}

function normaliser(texte: string): string {
  return texte.trim().toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[’']/g, "'");
}
