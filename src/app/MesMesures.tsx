"use client";

import { useId, useState, useSyncExternalStore, type ChangeEvent } from "react";
import { lireCm, mesures, type CodeMesure, type MesMesures as Valeurs } from "@/mesures";
import { depuisCsv, versCsv } from "@/mesuresCsv";
import { abonner, decoder, enregistrer, lireBrut } from "./mesMesuresStockage";

type Props = {
  codes: CodeMesure[];
  /** Plus petite et plus grande valeur du tableau des tailles, pour se repérer. */
  fourchettes: Partial<Record<CodeMesure, [string, string]>>;
};

export function MesMesures({ codes, fourchettes }: Props) {
  const valeurs = decoder(useSyncExternalStore(abonner, lireBrut, () => null));
  const [message, setMessage] = useState("");
  const idFichier = useId();

  function sauver(nouvelles: Valeurs, succes: string) {
    setMessage(
      enregistrer(nouvelles)
        ? succes
        : "Ce navigateur ne garde pas les mesures : téléchargez-les pour ne pas les perdre.",
    );
  }

  function telecharger() {
    const fichier = new Blob(["﻿" + versCsv(valeurs)], { type: "text/csv;charset=utf-8" });
    const lien = document.createElement("a");
    lien.href = URL.createObjectURL(fichier);
    lien.download = "mes-mesures.csv";
    lien.click();
    URL.revokeObjectURL(lien.href);
  }

  async function charger(e: ChangeEvent<HTMLInputElement>) {
    const fichier = e.target.files?.[0];
    e.target.value = ""; // pour pouvoir recharger le même fichier
    if (!fichier) return;
    const { valeurs: lues, ignorees } = depuisCsv(await fichier.text());
    const nombre = Object.keys(lues).length;
    if (nombre === 0) {
      setMessage("Aucune mesure reconnue dans ce fichier.");
      return;
    }
    const pourCePatron = codes.filter((c) => lues[c] !== undefined).length;
    sauver(
      { ...valeurs, ...lues },
      `${pluriel(nombre, "mesure chargée", "mesures chargées")}, dont ${pourCePatron} pour ce patron` +
        (ignorees ? ` ; ${pluriel(ignorees, "ligne non reconnue", "lignes non reconnues")}.` : "."),
    );
  }

  function effacer() {
    if (window.confirm("Effacer toutes vos mesures de ce navigateur ?")) sauver({}, "Mesures effacées.");
  }

  const remplies = codes.filter((c) => lireCm(valeurs[c] ?? "") !== undefined).length;
  const vide = Object.keys(valeurs).length === 0;

  return (
    <section className="conteneur mesures mes-mesures">
      <h2>Mes mesures</h2>
      <p className="mes-mesures-intro">
        Les mesures du corps dont ce patron a besoin, en centimètres. Elles restent dans ce
        navigateur et resservent sur les autres fiches ; téléchargez-les pour les retrouver
        ailleurs ou après avoir vidé le cache.
      </p>
      <div className="tableau">
        <table>
          <thead>
            <tr>
              <th scope="col">Mesure du corps</th>
              <th scope="col">Tailles 36 à 44</th>
              <th scope="col">Ma mesure</th>
            </tr>
          </thead>
          <tbody>
            {codes.map((code) => {
              const texte = valeurs[code] ?? "";
              const fausse = texte.trim() !== "" && lireCm(texte) === undefined;
              const fourchette = fourchettes[code];
              return (
                <tr key={code}>
                  <td>
                    <label htmlFor={`${idFichier}-${code}`}>{mesures[code].libelle}</label>
                    <span className="aide">{mesures[code].aide}</span>
                  </td>
                  <td className="repere">{fourchette && (fourchette[0] === fourchette[1] ? fourchette[0] : `${fourchette[0]} – ${fourchette[1]}`)}</td>
                  <td>
                    <input
                      id={`${idFichier}-${code}`}
                      className="saisie"
                      type="text"
                      inputMode="decimal"
                      autoComplete="off"
                      value={texte}
                      aria-invalid={fausse}
                      onChange={(e) => sauver({ ...valeurs, [code]: e.target.value }, "")}
                    />
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
      <p className="mes-mesures-bilan">
        {remplies} sur {codes.length} mesures remplies
      </p>
      <div className="boutons">
        <button type="button" className="bouton plein" onClick={telecharger} disabled={vide}>
          Télécharger mes mesures
        </button>
        <label htmlFor={idFichier} className="bouton contour">
          Charger un fichier de mesures
        </label>
        <input id={idFichier} type="file" accept=".csv,text/csv" className="cache" onChange={charger} />
        {!vide && (
          <button type="button" className="bouton lien" onClick={effacer}>
            Effacer
          </button>
        )}
      </div>
      <p className="mes-mesures-message" role="status">
        {message}
      </p>
    </section>
  );
}

function pluriel(n: number, un: string, plusieurs: string): string {
  return `${n} ${n > 1 ? plusieurs : un}`;
}
