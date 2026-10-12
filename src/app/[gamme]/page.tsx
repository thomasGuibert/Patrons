import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { patrons, rayons } from "@/patrons";
import { estGamme, gammes, listeGammes } from "@/tailles";
import { Vignette } from "../Vignette";

type Props = { params: Promise<{ gamme: string }> };

export const dynamicParams = false;

export function generateStaticParams() {
  return listeGammes.map((gamme) => ({ gamme }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { gamme } = await params;
  return { title: estGamme(gamme) ? `Patrons ${gammes[gamme].nom.toLowerCase()} · Atelier AT` : "Atelier AT" };
}

export default async function Catalogue({ params }: Props) {
  const { gamme } = await params;
  if (!estGamme(gamme)) notFound();
  const { nom, tailles } = gammes[gamme];
  const autre = listeGammes.find((g) => g !== gamme)!;

  return (
    <main>
      <section className="conteneur vitrine" aria-label="La gamme">
        <h1 className="titre-gamme">Patrons {nom.toLowerCase()}</h1>
        <p className="mention">
          <span>Patrons en A4 et A3</span>
          <span>
            Tailles {tailles[0]} à {tailles[tailles.length - 1]}
          </span>
          <Link href={`/${autre}`}>Voir les patrons {gammes[autre].nom.toLowerCase()}</Link>
        </p>
      </section>

      {rayons.map((rayon) => {
        const articles = patrons.filter((p) => p.famille === rayon.famille);
        const bases = rayon.famille === "base";
        return (
          <section
            key={rayon.famille}
            id={bases ? "bases" : "vetements"}
            className={`conteneur rayon${bases ? " bases" : ""}`}
          >
            <div className="rayon-tete">
              <h2>{rayon.titre}</h2>
              <span className="script">{rayon.script}</span>
              <p>{rayon.note || `${articles.length} modèles`}</p>
            </div>
            <ul className="grille">
              {articles.map((patron) => (
                <li key={patron.slug}>
                  <Link href={`/${gamme}/${patron.slug}`} className="article">
                    <figure>
                      <Vignette
                        image={bases ? patron.planche?.[gamme] : patron.vignette[gamme]}
                        sizes={bases ? "(max-width: 520px) 100vw, 300px" : "(max-width: 700px) 100vw, 600px"}
                      />
                    </figure>
                    <div className="article-texte">
                      {bases && <p className="planche-leg">{patron.ref} · base</p>}
                      <div className="article-ligne">
                        <h3>{patron.nom}</h3>
                        {!bases && <span className="ref">{patron.ref}</span>}
                      </div>
                      {patron.enCours && <span className="statut">En cours</span>}
                      <p>{patron.resume}</p>
                    </div>
                  </Link>
                </li>
              ))}
            </ul>
          </section>
        );
      })}
    </main>
  );
}
