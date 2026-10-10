import { mesuresCorps, enCm, type Mesure } from "./tailles";

/**
 * Les mesures saisies par la personne, communes à tous les patrons : gardées dans ce navigateur
 * (localStorage), et en fichier CSV pour les retrouver ailleurs.
 */
export type Saisie = Partial<Record<Mesure, number>>;

const CLE = "atelier-at:mesures";
const vide: Saisie = {};
const abonnes = new Set<() => void>();
let brut: string | null = null;
let cache: Saisie = vide;

function lire(): string | null {
  try {
    return localStorage.getItem(CLE);
  } catch {
    return null;
  }
}

/** Instantané stable tant que le stockage ne change pas (pour useSyncExternalStore). */
export function saisie(): Saisie {
  const r = lire();
  if (r !== brut) {
    brut = r;
    cache = nettoyer(r ? safeJson(r) : null);
  }
  return cache;
}

export function saisieServeur(): Saisie {
  return vide;
}

export function abonner(f: () => void): () => void {
  abonnes.add(f);
  const ailleurs = (e: StorageEvent) => e.key === CLE && f();
  window.addEventListener("storage", ailleurs);
  return () => {
    abonnes.delete(f);
    window.removeEventListener("storage", ailleurs);
  };
}

export function enregistrer(s: Saisie) {
  try {
    if (Object.keys(s).length) localStorage.setItem(CLE, JSON.stringify(s));
    else localStorage.removeItem(CLE);
  } catch {
    // stockage refusé (navigation privée…) : la saisie reste valable jusqu'au rechargement
    brut = null;
    cache = s;
  }
  abonnes.forEach((f) => f());
}

function safeJson(t: string): unknown {
  try {
    return JSON.parse(t);
  } catch {
    return null;
  }
}

function estMesure(c: string): c is Mesure {
  return Object.prototype.hasOwnProperty.call(mesuresCorps, c);
}

function nettoyer(o: unknown): Saisie {
  const s: Saisie = {};
  if (o && typeof o === "object") {
    for (const [c, v] of Object.entries(o)) {
      if (estMesure(c) && typeof v === "number" && v > 0 && v < 300) s[c] = v;
    }
  }
  return s;
}

/** « 92,5 », « 92.5 » ou « 92 cm » → 92.5 ; null si ce n'est pas une longueur plausible. */
export function lireCm(t: string): number | null {
  const m = t.trim().replace(/\s*cm$/i, "").replace(",", ".");
  if (!/^\d+(\.\d+)?$/.test(m)) return null;
  const v = Number(m);
  return v > 0 && v < 300 ? v : null;
}

/** Hors de la plage des tailles proposées, élargie : probablement une erreur de saisie. */
export function inhabituelle(m: Mesure, cm: number): boolean {
  const t = mesuresCorps[m].cm;
  return cm < Math.min(...t) * 0.6 || cm > Math.max(...t) * 1.6;
}

/** CSV pour un tableur français : séparateur « ; », virgule décimale, UTF-8 avec BOM. */
export function versCsv(s: Saisie): string {
  const lignes = ["mesure;libellé;cm"];
  for (const m of Object.keys(mesuresCorps) as Mesure[]) {
    const v = s[m];
    if (v !== undefined) lignes.push(`${m};${mesuresCorps[m].libelle};${enCm(v)}`);
  }
  return "﻿" + lignes.join("\r\n") + "\r\n";
}

const sansAccent = (t: string) =>
  t.normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/[’']/g, "'").toLowerCase().trim();

/**
 * Relit un CSV exporté ici (ou retouché dans un tableur) : chaque ligne nomme une mesure,
 * par sa clé ou son libellé, et finit par sa valeur en cm. Séparateur « ; », « , » ou tabulation.
 */
export function depuisCsv(texte: string): { saisie: Saisie; ignorees: number } {
  const lignes = texte.replace(/^﻿/, "").split(/\r?\n/).filter((l) => l.trim());
  const sep = lignes.some((l) => l.includes(";")) ? ";" : lignes.some((l) => l.includes("\t")) ? "\t" : ",";
  const parLibelle = new Map<string, Mesure>(
    (Object.keys(mesuresCorps) as Mesure[]).map((m) => [sansAccent(mesuresCorps[m].libelle), m]),
  );
  const s: Saisie = {};
  let ignorees = 0;
  for (const l of lignes) {
    const cols = l.split(sep).map((c) => c.trim().replace(/^"(.*)"$/, "$1").trim());
    if (cols.length < 2) continue;
    const m = estMesure(cols[0]) ? cols[0] : cols.slice(0, -1).map((c) => parLibelle.get(sansAccent(c))).find(Boolean);
    const v = lireCm(cols[cols.length - 1]);
    if (m && v !== null) s[m] = v;
    else if (!/^mesure$/i.test(cols[0])) ignorees++;
  }
  return { saisie: s, ignorees };
}
