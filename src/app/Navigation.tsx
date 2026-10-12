"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { estGamme, type Gamme } from "@/tailles";

/** Les rayons de la gamme en cours de visite ; depuis l'accueil, ceux des patrons femme. */
export function Navigation() {
  const segment = usePathname().split("/")[1] ?? "";
  const gamme: Gamme = estGamme(segment) ? segment : "femme";
  return (
    <nav aria-label="Navigation principale" className="nav">
      <Link href={`/${gamme}#vetements`}>Vêtements</Link>
      <Link href={`/${gamme}#bases`}>Bases</Link>
    </nav>
  );
}
