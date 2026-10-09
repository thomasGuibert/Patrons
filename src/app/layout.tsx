import type { Metadata } from "next";
import { Courier_Prime, IM_Fell_French_Canon, Pinyon_Script, Sorts_Mill_Goudy } from "next/font/google";
import Link from "next/link";
import { Ecusson } from "./Ecusson";
import "./globals.css";

const titres = IM_Fell_French_Canon({
  subsets: ["latin"],
  weight: "400",
  style: ["normal", "italic"],
  variable: "--font-titre",
});

const texte = Sorts_Mill_Goudy({
  subsets: ["latin"],
  weight: "400",
  style: ["normal", "italic"],
  variable: "--font-texte",
});

const manuscrite = Pinyon_Script({
  subsets: ["latin"],
  weight: "400",
  variable: "--font-manuscrite",
});

const machine = Courier_Prime({
  subsets: ["latin"],
  weight: "400",
  variable: "--font-machine",
});

export const metadata: Metadata = {
  title: "Atelier AT",
  description:
    "Patrons de vêtements faits pour durer, à imprimer chez soi en A4 ou en A3.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="fr"
      className={`${titres.variable} ${texte.variable} ${manuscrite.variable} ${machine.variable}`}
    >
      <body>
        <header className="entete">
          <div className="conteneur entete-ligne">
            <Link href="/" className="marque">
              <Ecusson className="ecusson" />
            </Link>
            <nav aria-label="Navigation principale" className="nav">
              <Link href="/#vetements">Vêtements</Link>
              <Link href="/#bases">Bases</Link>
            </nav>
          </div>
        </header>
        {children}
        <footer className="pied">
          <div className="conteneur pied-ligne">
            <span>Atelier AT · Fait pour durer</span>
            <span>Patrons à imprimer chez soi</span>
          </div>
        </footer>
      </body>
    </html>
  );
}
