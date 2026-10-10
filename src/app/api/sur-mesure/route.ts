import { disponible, lancer, verifier, type Format } from "@/surMesure";

/** Lance le tracé d'un patron sur mesure ; renvoie l'identifiant de la demande. */
export async function POST(req: Request) {
  if (!disponible()) return Response.json({ erreur: "indisponible" }, { status: 503 });
  const corps = await req.json().catch(() => null);
  const { patron, format, mesures } = corps ?? {};
  const faute = verifier(patron, format, mesures);
  if (faute) return Response.json({ erreur: faute }, { status: 400 });
  try {
    return Response.json({ demande: await lancer(patron, format as Format, mesures) });
  } catch (e) {
    console.error(e);
    return Response.json({ erreur: "lancement impossible" }, { status: 502 });
  }
}
