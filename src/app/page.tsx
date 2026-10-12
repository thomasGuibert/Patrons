import Link from "next/link";
import { trouverPatron } from "@/patrons";
import { gammes, listeGammes } from "@/tailles";
import { Enseigne } from "./Enseigne";
import { Vignette } from "./Vignette";

export default function Accueil() {
  const vitrine = trouverPatron("haut-pyjama")!;
  return (
    <main>
      <Enseigne />

      <section className="conteneur vitrine" aria-label="La maison">
        <p className="devise">
          Des vêtements qui suivent la mode des saisons plutôt que les saisons de la mode.
        </p>
      </section>

      <section className="conteneur rayon" aria-label="Choisir une gamme">
        <ul className="grille gammes">
          {listeGammes.map((g) => (
            <li key={g}>
              <Link href={`/${g}`} className="article">
                <figure>
                  <Vignette image={vitrine.vignette[g]} sizes="(max-width: 700px) 100vw, 600px" />
                </figure>
                <div className="article-texte">
                  <div className="article-ligne">
                    <h2>Patrons {gammes[g].nom.toLowerCase()}</h2>
                    <span className="script">entrer</span>
                  </div>
                  <p>
                    Tailles {gammes[g].tailles[0]} à {gammes[g].tailles[gammes[g].tailles.length - 1]}, ou sur mesure.
                  </p>
                </div>
              </Link>
            </li>
          ))}
        </ul>
      </section>
    </main>
  );
}
