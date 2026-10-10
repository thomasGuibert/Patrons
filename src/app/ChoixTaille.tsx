"use client";

import { useState } from "react";
import { tailleParDefaut, tailles, type Taille } from "@/tailles";

export function ChoixTaille({ slug }: { slug: string }) {
  const [taille, setTaille] = useState<Taille>(tailleParDefaut);

  return (
    <>
      <fieldset className="choix-taille">
        <legend>Taille</legend>
        <div className="tailles">
          {tailles.map((t) => (
            <label key={t}>
              <input
                type="radio"
                name="taille"
                value={t}
                checked={t === taille}
                onChange={() => setTaille(t)}
              />
              <span>{t}</span>
            </label>
          ))}
        </div>
      </fieldset>
      <div className="boutons">
        <a href={`/pdf/${slug}-${taille}.pdf`} className="bouton plein" download>
          Télécharger · A4
        </a>
        <a href={`/pdf/${slug}-${taille}-a3.pdf`} className="bouton contour" download>
          Télécharger · A3
        </a>
      </div>
    </>
  );
}
