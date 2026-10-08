import Image from "next/image";
import type { Patron } from "@/patrons";

export function Vignette({ patron, priorite = false }: { patron: Patron; priorite?: boolean }) {
  if (!patron.vignette) {
    return <div className="vignette vignette-vide">Vignette à venir</div>;
  }
  return (
    <Image
      src={patron.vignette}
      alt=""
      className="vignette"
      sizes="(max-width: 700px) 100vw, 600px"
      priority={priorite}
    />
  );
}
