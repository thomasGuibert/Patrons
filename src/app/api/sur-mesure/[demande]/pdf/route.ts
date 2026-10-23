import { disponible, pdf } from "@/surMesure";
import { trouverPatron } from "@/patrons";

/** Le PDF terminé, en téléchargement. */
export async function GET(req: Request, { params }: { params: Promise<{ demande: string }> }) {
  const { demande } = await params;
  if (!/^[0-9a-f]{16}$/.test(demande) || !disponible()) return new Response("Introuvable", { status: 404 });
  const contenu = await pdf(demande).catch(() => null);
  if (!contenu) return new Response("Introuvable", { status: 404 });
  const q = new URL(req.url).searchParams;
  const slug = trouverPatron(q.get("patron") ?? "")?.slug ?? "patron";
  // « T-Thomas » → haut-pyjama-t-thomas.pdf (nom de fichier en ASCII)
  const taille = (q.get("nom") ?? "")
    .normalize("NFD")
    .replace(/[^A-Za-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .toLowerCase()
    .slice(0, 20);
  const nom = `${slug}-${taille ? `t-${taille}` : "sur-mesure"}${q.get("format") === "a3" ? "-a3" : ""}.pdf`;
  return new Response(contenu as BodyInit, {
    headers: {
      "Content-Type": "application/pdf",
      "Content-Disposition": `attachment; filename="${nom}"`,
      "Cache-Control": "no-store",
    },
  });
}
