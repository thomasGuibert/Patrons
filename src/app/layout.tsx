import type { Metadata } from "next";
import { Fraunces, Karla } from "next/font/google";
import Link from "next/link";
import "./globals.css";

const fraunces = Fraunces({
  subsets: ["latin"],
  weight: ["500", "700"],
  variable: "--font-titre",
});

const karla = Karla({
  subsets: ["latin"],
  weight: ["400", "500", "700"],
  variable: "--font-texte",
});

export const metadata: Metadata = {
  title: "Patrons",
  description: "Patrons de couture tracés sur mesures, à imprimer en A4 ou en A3.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="fr" className={`${fraunces.variable} ${karla.variable}`}>
      <body>
        <header className="entete">
          <div className="conteneur entete-ligne">
            <Link href="/" className="logo">
              <svg width="32" height="32" viewBox="0 0 32 32" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
                <path d="M8 4h11l5 7-3 17H9L7 11z" />
              </svg>
              Patrons
            </Link>
            <nav aria-label="Navigation principale" className="nav">
              <Link href="/#catalogue">Catalogue</Link>
              <Link href="/#methode">La méthode</Link>
              <Link href="/#mesures">Mesures</Link>
            </nav>
          </div>
        </header>
        {children}
        <footer className="conteneur pied">
          <span>Patrons, par Thomas Guibert</span>
          <a href="https://github.com/thomasGuibert/Patrons">Sources sur GitHub</a>
        </footer>
      </body>
    </html>
  );
}
