import Image, { type StaticImageData } from "next/image";

export function Vignette({
  image,
  priorite = false,
  sizes = "(max-width: 700px) 100vw, 600px",
}: {
  image?: StaticImageData;
  priorite?: boolean;
  sizes?: string;
}) {
  if (!image) {
    return <div className="vignette vignette-vide">Vignette à venir</div>;
  }
  return <Image src={image} alt="" className="vignette" sizes={sizes} priority={priorite} />;
}
