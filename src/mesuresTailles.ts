import { readFileSync } from "node:fs";
import path from "node:path";
import type { CodeMesure } from "./mesures";
import { tailles } from "./tailles";

/**
 * Mesures de chaque taille, lues au build dans `mesures/T36.smms` à `T44.smms` : le repère
 * « de … à … » à côté de chaque case du tableau « Mes mesures ».
 */
export function fourchettes(codes: CodeMesure[]): Partial<Record<CodeMesure, [string, string]>> {
  const parTaille = tailles.map((t) =>
    readFileSync(path.join(process.cwd(), "mesures", `T${t}.smms`), "utf8"),
  );
  const resultat: Partial<Record<CodeMesure, [string, string]>> = {};
  for (const code of codes) {
    const valeurs = parTaille
      .map((smms) => smms.match(new RegExp(`<m base="([\\d.]+)"[^>]* name="${code}"`))?.[1])
      .filter((v): v is string => v !== undefined)
      .map(Number);
    if (valeurs.length === 0) continue;
    const cm = (v: number) => String(v).replace(".", ",");
    resultat[code] = [cm(Math.min(...valeurs)), cm(Math.max(...valeurs))];
  }
  return resultat;
}
