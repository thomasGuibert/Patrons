import { inflateRawSync } from "node:zlib";
import { trouverPatron } from "./patrons";
import { mesuresCorps, type Mesure } from "./tailles";

/**
 * Patron sur mesure, côté serveur : le site lance le workflow GitHub « Sur mesure »
 * (.github/workflows/sur-mesure.yml), qui trace le patron avec Seamly et le dépose en artefact.
 * Jeton : variable GITHUB_TOKEN_SUR_MESURE (accès « Actions » en lecture et écriture au dépôt).
 */
const DEPOT = "thomasGuibert/Patrons";
const WORKFLOW = "sur-mesure.yml";

export const formats = ["a4", "a3"] as const;
export type Format = (typeof formats)[number];

export function disponible(): boolean {
  return Boolean(process.env.GITHUB_TOKEN_SUR_MESURE);
}

async function github(chemin: string, init: RequestInit = {}): Promise<Response> {
  return fetch(`${process.env.GITHUB_API_URL ?? "https://api.github.com"}/repos/${DEPOT}${chemin}`, {
    ...init,
    cache: "no-store",
    headers: {
      Accept: "application/vnd.github+json",
      Authorization: `Bearer ${process.env.GITHUB_TOKEN_SUR_MESURE}`,
      "X-GitHub-Api-Version": "2022-11-28",
      ...init.headers,
    },
  });
}

/** Vérifie la demande ; renvoie un message d'erreur, ou null si elle est complète. */
export function verifier(slug: unknown, format: unknown, mesures: unknown): string | null {
  const patron = typeof slug === "string" ? trouverPatron(slug) : undefined;
  if (!patron) return "patron inconnu";
  if (!formats.includes(format as Format)) return "format inconnu";
  if (!mesures || typeof mesures !== "object") return "mesures absentes";
  for (const m of patron.saisie) {
    const v = (mesures as Record<string, unknown>)[m];
    if (typeof v !== "number" || !(v > 0 && v < 300)) return `mesure manquante : ${mesuresCorps[m].libelle}`;
  }
  return null;
}

export async function lancer(slug: string, format: Format, mesures: Partial<Record<Mesure, number>>): Promise<string> {
  const patron = trouverPatron(slug)!;
  const demande = crypto.randomUUID().replace(/-/g, "").slice(0, 16);
  const seamly = Object.fromEntries(patron.saisie.map((m) => [mesuresCorps[m].seamly, mesures[m]]));
  const r = await github(`/actions/workflows/${WORKFLOW}/dispatches`, {
    method: "POST",
    body: JSON.stringify({
      ref: "main",
      inputs: { demande, patron: slug, format, mesures: JSON.stringify(seamly) },
    }),
  });
  if (!r.ok) throw new Error(`GitHub ${r.status} : ${await r.text()}`);
  return demande;
}

type Run = { id: number; display_title: string; status: string; conclusion: string | null };

async function trouverRun(demande: string): Promise<Run | undefined> {
  const r = await github(`/actions/workflows/${WORKFLOW}/runs?event=workflow_dispatch&per_page=50`);
  if (!r.ok) throw new Error(`GitHub ${r.status}`);
  const { workflow_runs } = (await r.json()) as { workflow_runs: Run[] };
  return workflow_runs.find((w) => w.display_title === `sur-mesure ${demande}`);
}

export type Etat = "attente" | "pret" | "echec";

export async function etat(demande: string): Promise<Etat> {
  const run = await trouverRun(demande);
  if (!run || run.status !== "completed") return "attente";
  return run.conclusion === "success" ? "pret" : "echec";
}

/** Le PDF de l'artefact ; l'artefact est supprimé ensuite (les mesures n'ont pas à traîner). */
export async function pdf(demande: string): Promise<Uint8Array | null> {
  const run = await trouverRun(demande);
  if (!run) return null;
  const a = await github(`/actions/runs/${run.id}/artifacts`);
  if (!a.ok) return null;
  const { artifacts } = (await a.json()) as { artifacts: { id: number; name: string }[] };
  const art = artifacts.find((x) => x.name === "sur-mesure");
  if (!art) return null;
  const z = await github(`/actions/artifacts/${art.id}/zip`);
  if (!z.ok) return null;
  const contenu = premierFichier(new Uint8Array(await z.arrayBuffer()));
  await github(`/actions/artifacts/${art.id}`, { method: "DELETE" }).catch(() => undefined);
  return contenu;
}

/** Premier fichier d'une archive zip (l'artefact n'en contient qu'un). */
export function premierFichier(zip: Uint8Array): Uint8Array {
  const v = new DataView(zip.buffer, zip.byteOffset, zip.byteLength);
  let fin = zip.length - 22;
  while (fin >= 0 && v.getUint32(fin, true) !== 0x06054b50) fin--;
  if (fin < 0) throw new Error("zip illisible");
  const cd = v.getUint32(fin + 16, true);
  if (v.getUint32(cd, true) !== 0x02014b50) throw new Error("zip illisible");
  const methode = v.getUint16(cd + 10, true);
  const taille = v.getUint32(cd + 20, true);
  const local = v.getUint32(cd + 42, true);
  const debut = local + 30 + v.getUint16(local + 26, true) + v.getUint16(local + 28, true);
  const donnees = zip.subarray(debut, debut + taille);
  if (methode === 0) return donnees;
  if (methode === 8) return new Uint8Array(inflateRawSync(donnees));
  throw new Error(`zip : méthode ${methode}`);
}
