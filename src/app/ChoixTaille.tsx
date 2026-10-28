"use client";

import { useState, useSyncExternalStore } from "react";
import { gammes, type Gamme, type Mesure, type Taille } from "@/tailles";
import {
  abonner, abonnerNom, enregistrerNom, NOM_MAX, nomTaille, nomTailleServeur, nomValide, normaliserNom, saisie, saisieServeur,
} from "@/vosMesures";

type Choix = Taille | "sur-mesure";
type Format = "a4" | "a3";
type Montage = "amateur" | "pro";

const MONTAGES: { valeur: Montage; libelle: string; aide: string }[] = [
  { valeur: "amateur", libelle: "Pas à pas", aide: "Le montage expliqué étape par étape, illustré." },
  { valeur: "pro", libelle: "Gamme d'atelier", aide: "Le montage en tableau : opération, schéma, outil, point de contrôle." },
];

/** Le dossier technique puis le patron, en un seul PDF (assemblé dans le navigateur). */
async function assembler(dossier: string, patron: string): Promise<Blob> {
  const { PDFDocument } = await import("pdf-lib");
  const [d, p] = await Promise.all(
    [dossier, patron].map(async (url) => {
      const r = await fetch(url);
      if (!r.ok) throw new Error(url);
      return PDFDocument.load(await r.arrayBuffer());
    }),
  );
  const pages = await d.copyPages(p, p.getPageIndices());
  pages.forEach((page) => d.addPage(page));
  const titre = p.getTitle();
  if (titre) d.setTitle(titre);
  return new Blob([(await d.save()) as BlobPart], { type: "application/pdf" });
}

function telecharger(href: string, nom = "") {
  const a = document.createElement("a");
  a.href = href;
  a.download = nom;
  a.click();
}

const ATTENTE_MAX = 10 * 60 * 1000;
const pause = (ms: number) => new Promise((r) => setTimeout(r, ms));

type Jeu = { suffixe: string; libelle: string };

export function ChoixTaille({
  gamme, slug, mesures, dossier, surMesure: surMesureOuvert = true, jeux = [],
}: { gamme: Gamme; slug: string; mesures: Mesure[]; dossier: boolean; surMesure?: boolean; jeux?: Jeu[] }) {
  const { tailles, parDefaut } = gammes[gamme];
  const [taille, setTaille] = useState<Choix>(parDefaut);
  const [montage, setMontage] = useState<Montage>("amateur");
  const [enCours, setEnCours] = useState<Format | null>(null);
  const [message, setMessage] = useState("");
  const valeurs = useSyncExternalStore(abonner, saisie, saisieServeur);
  const manquantes = mesures.filter((m) => valeurs[m] === undefined).length;
  const nomSaisi = useSyncExternalStore(abonnerNom, nomTaille, nomTailleServeur);
  const nom = normaliserNom(nomSaisi);
  const nomFaux = !nomValide(nom);

  async function surMesure(format: Format) {
    setEnCours(format);
    setMessage("Votre patron se trace à vos mesures. Cela prend une à deux minutes ; gardez cette page ouverte.");
    try {
      const r = await fetch("/api/sur-mesure", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ patron: slug, format, mesures: valeurs, nom, montage: dossier ? montage : "" }),
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
      telecharger(`/api/sur-mesure/${demande}/pdf?${new URLSearchParams({ patron: slug, format, nom })}`);
      setMessage("Votre patron est prêt : le téléchargement commence.");
    } catch (e) {
      setMessage(e instanceof Error ? e.message : "Une erreur est survenue.");
    } finally {
      setEnCours(null);
    }
  }

  async function avecDossier(t: Taille, format: Format, patron: string) {
    setEnCours(format);
    setMessage("");
    try {
      const pdf = await assembler(`/pdf/${gamme}/dossier/${slug}-${t}-${montage}.pdf`, patron);
      const url = URL.createObjectURL(pdf);
      telecharger(url, patron.split("/").pop());
      setTimeout(() => URL.revokeObjectURL(url), 60_000);
    } catch {
      // sans le dossier, le patron seul reste téléchargeable
      telecharger(patron);
    } finally {
      setEnCours(null);
    }
  }

  const bouton = (format: Format, classe: string, jeu?: Jeu) => {
    const libelle = `${jeu ? `${jeu.libelle} · ` : "Télécharger · "}${format.toUpperCase()}`;
    if (taille !== "sur-mesure") {
      const patron = `/pdf/${gamme}/${jeu ? `${slug}-${jeu.suffixe}` : slug}-${taille}${format === "a3" ? "-a3" : ""}.pdf`;
      return (
        <a
          href={patron}
          className={`bouton ${classe}`}
          download
          aria-busy={enCours === format}
          onClick={(e) => {
            if (!dossier || jeu) return;
            e.preventDefault();
            if (enCours === null) avecDossier(taille, format, patron);
          }}
        >
          {enCours === format && <span className="roue" aria-hidden />}
          {libelle}
        </a>
      );
    }
    return (
      <button
        type="button"
        className={`bouton ${classe}`}
        disabled={manquantes > 0 || nomFaux || enCours !== null}
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
          {((surMesureOuvert ? [...tailles, "sur-mesure"] : tailles) as Choix[]).map((t) => (
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
      {taille === "sur-mesure" && (
        <div className="nom-taille">
          <label htmlFor="nom-taille">Nom de la taille</label>
          <span className="champ">
            <span aria-hidden>T-</span>
            <input
              id="nom-taille"
              autoComplete="given-name"
              placeholder="Thomas"
              maxLength={NOM_MAX + 2}
              value={nomSaisi}
              disabled={enCours !== null}
              aria-invalid={nomFaux}
              aria-describedby="nom-taille-aide"
              onChange={(e) => enregistrerNom(e.target.value)}
            />
          </span>
          <small id="nom-taille-aide">
            {nomFaux
              ? `Lettres, chiffres, espaces, tirets ou apostrophes, ${NOM_MAX} au plus.`
              : `Imprimé sur le patron : ${nom ? `T-${nom}` : "« Sur mesure »"}.`}
          </small>
        </div>
      )}
      {dossier && (
        <fieldset className="choix-taille">
          <legend>Notice de montage</legend>
          <div className="tailles">
            {MONTAGES.map((m) => (
              <label key={m.valeur}>
                <input
                  type="radio"
                  name="montage"
                  value={m.valeur}
                  checked={m.valeur === montage}
                  disabled={enCours !== null}
                  onChange={() => setMontage(m.valeur)}
                />
                <span className="large">{m.libelle}</span>
              </label>
            ))}
          </div>
          <small className="aide-montage">{MONTAGES.find((m) => m.valeur === montage)?.aide}</small>
        </fieldset>
      )}
      <div className="boutons">
        {bouton("a4", "plein")}
        {bouton("a3", "contour")}
      </div>
      {taille !== "sur-mesure" &&
        jeux.map((jeu) => (
          <div className="boutons" key={jeu.suffixe}>
            {bouton("a4", "contour", jeu)}
            {bouton("a3", "contour", jeu)}
          </div>
        ))}
      {message && (
        <p className="attente" role="status">
          {message}
        </p>
      )}
    </>
  );
}
