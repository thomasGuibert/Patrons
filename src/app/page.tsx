import Link from "next/link";
import { patrons, rayons } from "@/patrons";
import { Vignette } from "./Vignette";

export default function Accueil() {
  return (
    <main>
      <div className="conteneur">
        <div className="enseigne">
          <div className="enseigne-cadre">
            <p className="enseigne-cote">
              Vêtements
              <br />
              Patrons
              <br />à imprimer
            </p>
            <div className="enseigne-centre">
              <h1 className="enseigne-nom">Atelier AT</h1>
              <p className="enseigne-sous">
                Sp<small>té</small> de vêtements faits pour durer
              </p>
            </div>
            <p className="enseigne-cote droite">
              Coupe juste
              <br />
              Couture
              <br />
              durable
            </p>
          </div>
        </div>
      </div>

      <section className="conteneur vitrine" aria-label="La maison">
        <p className="devise">
          Des vêtements qui suivent la mode des saisons plutôt que les saisons de la mode.
        </p>
        <p className="mention">
          <span>Patrons en A4 et A3</span>
          <span>Tailles 36 à 44</span>
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
                  <Link href={`/patrons/${patron.slug}`} className="article">
                    <figure>
                      <Vignette
                        image={bases ? patron.planche : patron.vignette}
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
