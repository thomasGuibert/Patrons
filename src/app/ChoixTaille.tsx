"use client";

import { useState, useSyncExternalStore } from "react";
import { tailleParDefaut, tailles, type Mesure, type Taille } from "@/tailles";
import { abonner, saisie, saisieServeur } from "@/vosMesures";

type Choix = Taille | "sur-mesure";
type Format = "a4" | "a3";

const ATTENTE_MAX = 10 * 60 * 1000;
const pause = (ms: number) => new Promise((r) => setTimeout(r, ms));

export function ChoixTaille({ slug, mesures }: { slug: string; mesures: Mesure[] }) {
  const [taille, setTaille] = useState<Choix>(tailleParDefaut);
  const [enCours, setEnCours] = useState<Format | null>(null);
  const [message, setMessage] = useState("");
  const valeurs = useSyncExternalStore(abonner, saisie, saisieServeur);
  const manquantes = mesures.filter((m) => valeurs[m] === undefined).length;

  async function surMesure(format: Format) {
    setEnCours(format);
    setMessage("Votre patron se trace à vos mesures. Cela prend une à deux minutes ; gardez cette page ouverte.");
    try {
      const r = await fetch("/api/sur-mesure", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ patron: slug, format, mesures: valeurs }),
      });
      if (r.status === 503) throw new Error("Le patron sur mesure n'est pas encore ouvert. Revenez bientôt.");
      if (!r.ok) throw new Error("La demande n'a pas pu être envoyée. Vérifiez vos mesures et réessayez.");
      const { demande } = (await r.json()) as { demande: string };
      const debut = Date.now();
      for (;;) {
        await pause(5000);
        if (Date.now() - debut > ATTENTE_MAX) throw new Error("Le tracé prend trop de temps. Réessayez un peu plus tard.");
        const e = await fetch(`/api/sur-mesure/${demande}`).then((x) => (x.ok ? x.json() : { etat: "attente" }));
        if (e.etat === "echec") throw new Error("Le tracé a échoué avec ces mesures. Vérifiez-les et réessayez.");
        if (e.etat === "pret") break;
      }
      const a = document.createElement("a");
      a.href = `/api/sur-mesure/${demande}/pdf?patron=${slug}&format=${format}`;
      a.download = "";
      a.click();
      setMessage("Votre patron est prêt : le téléchargement commence.");
    } catch (e) {
      setMessage(e instanceof Error ? e.message : "Une erreur est survenue.");
    } finally {
      setEnCours(null);
    }
  }

  const bouton = (format: Format, classe: string) => {
    const libelle = `Télécharger · ${format.toUpperCase()}`;
    if (taille !== "sur-mesure") {
      return (
        <a href={`/pdf/${slug}-${taille}${format === "a3" ? "-a3" : ""}.pdf`} className={`bouton ${classe}`} download>
          {libelle}
        </a>
      );
    }
    return (
      <button
        type="button"
        className={`bouton ${classe}`}
        disabled={manquantes > 0 || enCours !== null}
        aria-busy={enCours === format}
        onClick={() => surMesure(format)}
      >
        {enCours === format && <span className="roue" aria-hidden />}
        {enCours === format ? "Tracé en cours" : libelle}
      </button>
    );
  };

  return (
    <>
      <fieldset className="choix-taille">
        <legend>Taille</legend>
        <div className="tailles">
          {([...tailles, "sur-mesure"] as Choix[]).map((t) => (
            <label key={t}>
              <input
                type="radio"
                name="taille"
                value={t}
                checked={t === taille}
                disabled={enCours !== null}
                onChange={() => {
                  setTaille(t);
                  setMessage("");
                }}
              />
              <span className={t === "sur-mesure" ? "large" : undefined}>{t === "sur-mesure" ? "Sur mesure" : t}</span>
            </label>
          ))}
        </div>
      </fieldset>
      {taille === "sur-mesure" && manquantes > 0 && (
        <p className="a-completer">
          <a href="#vos-mesures">Notez vos mesures</a> pour tracer le patron à votre taille : il en manque {manquantes}.
        </p>
      )}
      <div className="boutons">
        {bouton("a4", "plein")}
        {bouton("a3", "contour")}
      </div>
      {message && (
        <p className="attente" role="status">
          {message}
        </p>
      )}
    </>
  );
}
