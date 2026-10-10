import { disponible, etat } from "@/surMesure";

/** Où en est la demande : attente, pret ou echec. */
export async function GET(_: Request, { params }: { params: Promise<{ demande: string }> }) {
  const { demande } = await params;
  if (!/^[0-9a-f]{16}$/.test(demande)) return Response.json({ erreur: "demande inconnue" }, { status: 404 });
  if (!disponible()) return Response.json({ erreur: "indisponible" }, { status: 503 });
  try {
    return Response.json({ etat: await etat(demande) });
  } catch (e) {
    console.error(e);
    return Response.json({ etat: "attente" });
  }
}
