"use client";

import { useState } from "react";
import { coutures, matieres, parties, type Couture, type Matiere } from "@/pieces";

const listeMatieres = Object.keys(matieres) as Matiere[];
const listeCoutures = Object.keys(coutures) as Couture[];

function Filtre<T extends string>({
  legende,
  choix,
  valeur,
  libelle,
  onChange,
}: {
  legende: string;
  choix: T[];
  valeur: T | null;
  libelle: (c: T) => string;
  onChange: (c: T | null) => void;
}) {
  return (
    <fieldset className="choix-taille">
      <legend>{legende}</legend>
      <div className="tailles">
        {[null, ...choix].map((c) => (
          <label key={c ?? "tout"}>
            <input type="radio" name={legende} checked={valeur === c} onChange={() => onChange(c)} />
            <span className="large">{c ? libelle(c) : "Toutes"}</span>
          </label>
        ))}
      </div>
    </fieldset>
  );
}

export function CataloguePieces() {
  const [matiere, setMatiere] = useState<Matiere | null>(null);
  const [couture, setCouture] = useState<Couture | null>(null);

  return (
    <>
      <section className="conteneur filtres-pieces" aria-label="Trier les pièces">
        <Filtre legende="Matériau" choix={listeMatieres} valeur={matiere} libelle={(m) => matieres[m].nom} onChange={setMatiere} />
        <Filtre legende="Couture" choix={listeCoutures} valeur={couture} libelle={(c) => coutures[c].nom} onChange={setCouture} />
        <dl className="legende-pieces">
          {listeMatieres.map((m) => (
            <div key={m}>
              <dt><span className={`pastille ${m}`}>{matieres[m].nom}</span></dt>
              <dd>{matieres[m].aide}</dd>
            </div>
          ))}
          {listeCoutures.map((c) => (
            <div key={c}>
              <dt><span className={`pastille ${c}`}>{coutures[c].nom}</span></dt>
              <dd>{coutures[c].aide}</dd>
            </div>
          ))}
          <div>
            <dt><span className="tracee">Tracée</span></dt>
            <dd>Déjà dans un patron de l&apos;atelier</dd>
          </div>
        </dl>
      </section>

      {parties.map((partie) => {
        const pieces = partie.pieces.filter(
          (p) => (!matiere || p.matieres.includes(matiere)) && (!couture || p.coutures.includes(couture)),
        );
        if (pieces.length === 0) return null;
        return (
          <section key={partie.titre} className="conteneur rayon">
            <div className="rayon-tete">
              <h2>{partie.titre}</h2>
              <span className="script">{partie.script}</span>
              <p>{pieces.length > 1 ? `${pieces.length} pièces` : "1 pièce"}</p>
            </div>
            <ul className="pieces">
              {pieces.map((piece) => (
                <li key={piece.nom} className="piece">
                  <div className="piece-ligne">
                    <h3>{piece.nom}</h3>
                    {piece.tracee && <span className="tracee">Tracée</span>}
                  </div>
                  <p>{piece.note}</p>
                  <p className="pastilles">
                    {piece.matieres.map((m) => (
                      <span key={m} className={`pastille ${m}`}>{matieres[m].nom}</span>
                    ))}
                    {piece.coutures.map((c) => (
                      <span key={c} className={`pastille ${c}`}>{coutures[c].nom}</span>
                    ))}
                  </p>
                </li>
              ))}
            </ul>
          </section>
        );
      })}
    </>
  );
}
