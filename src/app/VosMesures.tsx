"use client";

import { useRef, useState, useSyncExternalStore } from "react";
import { enCm, mesuresCorps, tailleParDefaut, tailles, type Mesure, type Taille } from "@/tailles";
import {
  abonner, depuisCsv, enregistrer, inhabituelle, lireCm, saisie, saisieServeur, versCsv, type Saisie,
} from "@/vosMesures";

/** Tableau à remplir avec ses propres mesures, gardées dans le navigateur et en fichier CSV. */
export function VosMesures({ mesures }: { mesures: Mesure[] }) {
  const valeurs = useSyncExternalStore(abonner, saisie, saisieServeur);
  const [brouillons, setBrouillons] = useState<Partial<Record<Mesure, string>>>({});
  const [reference, setReference] = useState<Taille>(tailleParDefaut);
  const [message, setMessage] = useState("");
  const fichier = useRef<HTMLInputElement>(null);
  const i = tailles.indexOf(reference);
  const remplies = mesures.filter((m) => valeurs[m] !== undefined).length;

  function saisir(m: Mesure, texte: string) {
    setBrouillons((b) => ({ ...b, [m]: texte }));
    const v = lireCm(texte);
    const s: Saisie = { ...valeurs };
    if (v !== null) s[m] = v;
    else if (!texte.trim()) delete s[m];
    else return;
    enregistrer(s);
  }

  function partirDeLaTaille() {
    const s: Saisie = { ...valeurs };
    for (const m of mesures) if (s[m] === undefined) s[m] = mesuresCorps[m].cm[i];
    setBrouillons({});
    enregistrer(s);
    setMessage(`Cases vides remplies avec la taille ${reference}.`);
  }

  function telecharger() {
    const url = URL.createObjectURL(new Blob([versCsv(valeurs)], { type: "text/csv;charset=utf-8" }));
    const a = document.createElement("a");
    a.href = url;
    a.download = "mes-mesures.csv";
    a.click();
    URL.revokeObjectURL(url);
  }

  async function importer(f: File | undefined) {
    if (!f) return;
    const { saisie: lues, ignorees } = depuisCsv(await f.text());
    const n = Object.keys(lues).length;
    if (n) {
      setBrouillons({});
      enregistrer({ ...valeurs, ...lues });
    }
    setMessage(
      n
        ? `${n} mesure${n > 1 ? "s" : ""} reprise${n > 1 ? "s" : ""} du fichier${ignorees ? `, ${ignorees} ligne${ignorees > 1 ? "s" : ""} ignorée${ignorees > 1 ? "s" : ""}` : ""}.`
        : "Aucune mesure reconnue dans ce fichier.",
    );
    if (fichier.current) fichier.current.value = "";
  }

  function effacer() {
    if (!confirm("Effacer toutes vos mesures de ce navigateur ?")) return;
    setBrouillons({});
    enregistrer({});
    setMessage("Mesures effacées.");
  }

  return (
    <section className="conteneur mesures vos-mesures" id="vos-mesures">
      <h2>Vos mesures</h2>
      <p className="note">
        Notez vos mesures du corps, en centimètres, prises près du corps sans serrer. Elles restent
        dans ce navigateur et servent pour tous les patrons ; gardez-en une copie en fichier pour
        les retrouver ailleurs.
      </p>
      <div className="tableau">
        <table>
          <thead>
            <tr>
              <th scope="col">Mesure du corps</th>
              <th scope="col">
                <label>
                  Taille{" "}
                  <select value={reference} onChange={(e) => setReference(Number(e.target.value) as Taille)}>
                    {tailles.map((t) => (
                      <option key={t} value={t}>
                        {t}
                      </option>
                    ))}
                  </select>
                </label>
              </th>
              <th scope="col">Vous</th>
            </tr>
          </thead>
          <tbody>
            {mesures.map((m) => {
              const v = valeurs[m];
              const texte = brouillons[m] ?? (v === undefined ? "" : enCm(v));
              const faux = texte.trim() !== "" && lireCm(texte) === null;
              const douteux = !faux && v !== undefined && inhabituelle(m, v);
              return (
                <tr key={m}>
                  <td>
                    <label htmlFor={`m-${m}`}>{mesuresCorps[m].libelle}</label>
                  </td>
                  <td className="ref-taille">{enCm(mesuresCorps[m].cm[i])}</td>
                  <td>
                    <input
                      id={`m-${m}`}
                      inputMode="decimal"
                      autoComplete="off"
                      placeholder={enCm(mesuresCorps[m].cm[i])}
                      value={texte}
                      aria-invalid={faux || douteux}
                      title={faux ? "Un nombre en cm, par exemple 92,5" : douteux ? "Valeur inhabituelle : à vérifier" : undefined}
                      onChange={(e) => saisir(m, e.target.value)}
                      onBlur={() => setBrouillons((b) => ({ ...b, [m]: undefined }))}
                    />
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
      <p className="compte">
        {remplies} / {mesures.length} mesures notées
      </p>
      <div className="boutons">
        <button type="button" className="bouton contour" onClick={partirDeLaTaille} disabled={remplies === mesures.length}>
          Compléter avec la taille {reference}
        </button>
        <button type="button" className="bouton contour" onClick={telecharger} disabled={!Object.keys(valeurs).length}>
          Télécharger mes mesures
        </button>
        <button type="button" className="bouton contour" onClick={() => fichier.current?.click()}>
          Reprendre un fichier
        </button>
        <input
          ref={fichier}
          type="file"
          accept=".csv,text/csv"
          hidden
          onChange={(e) => importer(e.target.files?.[0])}
        />
        {Object.keys(valeurs).length > 0 && (
          <button type="button" className="lien" onClick={effacer}>
            Effacer
          </button>
        )}
      </div>
      <p className="message" role="status">
        {message}
      </p>
    </section>
  );
}
