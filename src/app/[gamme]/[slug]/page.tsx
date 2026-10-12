import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { patrons, trouverPatron } from "@/patrons";
import { enCm, estGamme, gammes, listeGammes, mesuresCorps } from "@/tailles";
import { VosMesures } from "../../VosMesures";
import { ChoixTaille } from "../../ChoixTaille";
import { Vignette } from "../../Vignette";

type Props = { params: Promise<{ gamme: string; slug: string }> };

export const dynamicParams = false;

export function generateStaticParams() {
  return listeGammes.flatMap((gamme) => patrons.map((p) => ({ gamme, slug: p.slug })));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { gamme, slug } = await params;
  const patron = trouverPatron(slug);
  return { title: patron && estGamme(gamme) ? `${patron.nom} (${gammes[gamme].nom.toLowerCase()}) · Atelier AT` : "Atelier AT" };
}

export default async function FichePatron({ params }: Props) {
  const { gamme, slug } = await params;
  const patron = trouverPatron(slug);
  if (!patron || !estGamme(gamme)) notFound();
  const bases = patron.famille === "base";
  const { nom, tailles } = gammes[gamme];

  return (
    <main>
      <section className="conteneur fiche">
        <figure className="fiche-image">
          <Vignette image={patron.vignette[gamme]} priorite sizes="(max-width: 1200px) 100vw, 1136px" />
        </figure>
        <div className="fiche-texte">
          <div className="fiche-intro">
            <p className="fil">
              <Link href={`/${gamme}`}>{nom}</Link>
              {" · "}
              <Link href={`/${gamme}#${bases ? "bases" : "vetements"}`}>{bases ? "Bases" : "Vêtements"}</Link>
              {" · "}
              {patron.ref}
            </p>
            {patron.enCours && <span className="statut">En cours</span>}
            <h1>{patron.nom}</h1>
            {patron.description && <p className="chapeau">{patron.description}</p>}
          </div>
          <div className="fiche-achat">
            {patron.caracteristiques && (
              <dl className="etiquette">
                {patron.caracteristiques.map((c) => (
                  <div key={c.libelle}>
                    <dt>{c.libelle}</dt>
                    <dd>{c.valeur}</dd>
                  </div>
                ))}
              </dl>
            )}
            <ChoixTaille key={gamme} gamme={gamme} slug={patron.slug} mesures={patron.saisie} />
          </div>
        </div>
      </section>

      <section className="conteneur mesures">
        <h2>Tableau des tailles {nom.toLowerCase()}</h2>
        <div className="tableau">
          <table className="tailles-corps">
            <thead>
              <tr>
                <th scope="col">Mesure du corps</th>
                {tailles.map((t) => (
                  <th scope="col" key={t}>
                    {t}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {patron.mesures.map((m) => (
                <tr key={m}>
                  <td>{mesuresCorps[m].libelle}</td>
                  {mesuresCorps[m].cm[gamme].map((cm, i) => (
                    <td key={tailles[i]}>{enCm(cm)}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <VosMesures key={gamme} gamme={gamme} mesures={patron.saisie} />

      {patron.valeurs && (
        <section className="conteneur mesures">
          <h2>{patron.valeurs.titre}</h2>
          <div className="tableau">
            <table>
              <thead>
                <tr>
                  <th scope="col">Valeur</th>
                  <th scope="col">cm</th>
                </tr>
              </thead>
              <tbody>
                {patron.valeurs.lignes.map((l) => (
                  <tr key={l.libelle}>
                    <td>{l.libelle}</td>
                    <td>{l.cm}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      )}
    </main>
  );
}
