import type { MesMesures } from "@/mesures";

/**
 * Les mesures saisies restent dans le navigateur (localStorage), communes à toutes les fiches :
 * celles prises pour un haut resservent pour le bas.
 */
const cle = "patrons.mes-mesures";
const evenement = "patrons:mes-mesures";
/** Repli quand le navigateur refuse le stockage : les mesures tiennent le temps de la visite. */
let memoire: string | null = null;

export function abonner(rappel: () => void): () => void {
  const surStockage = (e: StorageEvent) => e.key === cle && rappel();
  window.addEventListener("storage", surStockage); // un autre onglet
  window.addEventListener(evenement, rappel); // cet onglet
  return () => {
    window.removeEventListener("storage", surStockage);
    window.removeEventListener(evenement, rappel);
  };
}

/** Le texte brut : une chaîne stable tant que rien ne change, comme le veut useSyncExternalStore. */
export function lireBrut(): string | null {
  try {
    return localStorage.getItem(cle);
  } catch {
    return memoire; // stockage bloqué (cookies refusés)
  }
}

export function decoder(brut: string | null): MesMesures {
  try {
    const valeurs: unknown = JSON.parse(brut ?? "{}");
    return valeurs && typeof valeurs === "object" ? (valeurs as MesMesures) : {};
  } catch {
    return {};
  }
}

/** false si le navigateur refuse de garder les mesures au-delà de la visite. */
export function enregistrer(valeurs: MesMesures): boolean {
  const nettoyees = Object.fromEntries(Object.entries(valeurs).filter(([, v]) => v?.trim()));
  memoire = Object.keys(nettoyees).length === 0 ? null : JSON.stringify(nettoyees);
  try {
    if (memoire === null) localStorage.removeItem(cle);
    else localStorage.setItem(cle, memoire);
    return true;
  } catch {
    return false;
  } finally {
    window.dispatchEvent(new Event(evenement));
  }
}
