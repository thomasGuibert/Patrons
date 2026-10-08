import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { libellesStatut, patrons, trouverPatron } from "@/patrons";
import { Vignette } from "../../Vignette";

type Props = { params: Promise<{ slug: string }> };

export function generateStaticParams() {
  return patrons.map((p) => ({ slug: p.slug }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const patron = trouverPatron((await params).slug);
  return { title: patron ? `${patron.nom} · Patrons` : "Patrons" };
}

export default async function FichePatron({ params }: Props) {
  const patron = trouverPatron((await params).slug);
  if (!patron) notFound();

  return (
    <main>
      <div className="conteneur">
        <Link href="/#catalogue" className="retour">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.8" aria-hidden="true">
            <path d="M10 3L5 8l5 5" />
          </svg>
          Retour au catalogue
        </Link>
      </div>

      <section className="conteneur fiche">
        <figure className="fiche-image">
          <Vignette patron={patron} priorite />
        </figure>
        <div className="fiche-texte">
          <span className={`statut statut-${patron.statut}`}>{libellesStatut[patron.statut]}</span>
          <h1>{patron.nom}</h1>
          {patron.description && <p className="chapeau">{patron.description}</p>}
          {patron.caracteristiques && (
            <dl className="caracteristiques">
              {patron.caracteristiques.map((c) => (
                <div key={c.libelle}>
                  <dt>{c.libelle}</dt>
                  <dd>{c.valeur}</dd>
                </div>
              ))}
            </dl>
          )}
          <div className="boutons">
            <a href={`/pdf/${patron.slug}.pdf`} className="bouton bouton-plein" download>
              Télécharger le PDF (A4)
            </a>
            <a href={`/pdf/${patron.slug}-a3.pdf`} className="bouton bouton-contour" download>
              Version A3
            </a>
          </div>
        </div>
      </section>

      {patron.valeurs && (
        <section className="bande-blanche">
          <div className="conteneur section-ligne">
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
          </div>
        </section>
      )}
    </main>
  );
}
