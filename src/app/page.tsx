import Image from "next/image";
import Link from "next/link";
import { libellesStatut, patrons, trouverPatron } from "@/patrons";
import { Vignette } from "./Vignette";

const etapes = [
  { titre: "Lire le livre", texte: "Les pages de construction sont photographiées et relues." },
  { titre: "Écrire les étapes", texte: "Chaque geste devient une étape chiffrée, validée avant tout tracé." },
  { titre: "Tracer dans Seamly2D", texte: "Le patron est construit sur les mesures, donc il suit la taille." },
  { titre: "Vérifier à l'export", texte: "Les longueurs de couture sont comparées avant publication." },
];

export default function Accueil() {
  const vedette = trouverPatron("fond-pantalon-droit")!;

  return (
    <main>
      <section className="conteneur intro">
        <div className="intro-texte">
          <p className="surtitre">Patrons de couture tracés à la main, puis au propre</p>
          <h1>Du livre de patronage au patron prêt à imprimer.</h1>
          <p className="chapeau">
            Chaque pièce part d&apos;une construction lue dans un livre, transcrite étape par étape, puis
            tracée dans Seamly2D et vérifiée par export.
          </p>
          <div className="boutons">
            <a href="#catalogue" className="bouton bouton-plein">Voir les patrons</a>
            <a href="#methode" className="bouton bouton-contour">Comment c&apos;est fait</a>
          </div>
        </div>
        <figure className="intro-image">
          <Image
            src={vedette.vignette!}
            alt="Fond de pantalon droit : les pièces devant et dos, puis le pantalon cousu"
            sizes="(max-width: 900px) 100vw, 600px"
            priority
          />
          <figcaption>Fond de pantalon droit, taille 44</figcaption>
        </figure>
      </section>

      <section id="catalogue" className="bande-blanche">
        <div className="conteneur section">
          <div className="section-titre">
            <h2>Le catalogue</h2>
            <p>{patrons.length} patrons, tous en taille 44 pour l&apos;instant</p>
          </div>
          <ul className="grille">
            {patrons.map((patron) => (
              <li key={patron.slug}>
                <Link href={`/patrons/${patron.slug}`} className="carte">
                  <Vignette patron={patron} />
                  <div className="carte-corps">
                    <span className={`statut statut-${patron.statut}`}>{libellesStatut[patron.statut]}</span>
                    <h3>{patron.nom}</h3>
                    <p>{patron.resume}</p>
                  </div>
                </Link>
              </li>
            ))}
          </ul>
        </div>
      </section>

      <section id="methode" className="conteneur section">
        <h2>La méthode, en quatre temps</h2>
        <ol className="grille etapes">
          {etapes.map((etape, i) => (
            <li key={etape.titre}>
              <span className="numero">{i + 1}</span>
              <h3>{etape.titre}</h3>
              <p>{etape.texte}</p>
            </li>
          ))}
        </ol>
      </section>

      <section id="mesures" className="bande-sauge">
        <div className="conteneur section-ligne">
          <div>
            <h2>Construit sur un tableau de mesures</h2>
            <p>Les patrons sont tracés en taille 44. D&apos;autres tailles viendront.</p>
          </div>
        </div>
      </section>
    </main>
  );
}
