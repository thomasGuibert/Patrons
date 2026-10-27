import type { Metadata } from "next";
import { CataloguePieces } from "./CataloguePieces";

export const metadata: Metadata = { title: "Pièces · Atelier AT" };

export default function Pieces() {
  return (
    <main>
      <section className="conteneur vitrine" aria-label="Les pièces">
        <h1 className="titre-gamme">Pièces</h1>
        <p className="devise">Les pièces que l&apos;atelier sait tracer à vos mesures, pour composer un vêtement.</p>
      </section>
      <CataloguePieces />
    </main>
  );
}
