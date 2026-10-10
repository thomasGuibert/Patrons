import type { ReactNode } from "react";
import type { Mesure } from "@/tailles";

/** Moitié gauche du corps, de face ; la moitié droite est son reflet autour de x = 100. */
const DEMI_CORPS =
  "M92,50 L92,63 Q80,68 62,74 Q52,79 50,100 L44,180 Q42,210 42,234 Q37,252 44,266 Q52,270 54,256 " +
  "L56,234 L60,180 Q66,130 70,106 Q68,128 76,152 Q70,170 66,192 Q64,240 72,300 Q78,350 82,396 " +
  "L80,414 Q80,422 88,422 L98,422 L97,398 Q96,350 95,300 Q96,250 100,216";

function Corps({ x, titre }: { x: number; titre: string }) {
  return (
    <g transform={`translate(${x} 0)`} className="corps">
      <ellipse cx={100} cy={30} rx={15} ry={19} />
      <path d={DEMI_CORPS} />
      <path d={DEMI_CORPS} transform="translate(200 0) scale(-1 1)" />
      <text x={100} y={438} className="vue">
        {titre}
      </text>
    </g>
  );
}

const fleche = (x1: number, y1: number, x2: number, y2: number) => <line x1={x1} y1={y1} x2={x2} y2={y2} />;
const tour = (cx: number, cy: number, rx: number, ry: number) => <ellipse cx={cx} cy={cy} rx={rx} ry={ry} />;
/** Hauteur mesurée sur le côté (vue de dos), du cordon de taille vers le bas. */
const hauteur = (x: number, y2: number) => (
  <>
    <line x1={x} y1={152} x2={x} y2={y2} />
    <line x1={x - 4} y1={y2} x2={x + 4} y2={y2} />
    <line x1={x - 4} y1={152} x2={x + 4} y2={152} />
  </>
);

/** Où se prend chaque mesure : vue de face à gauche (0-200), de dos à droite (200-400). */
const TRACES: Record<Mesure, ReactNode> = {
  encolure: tour(100, 62, 9, 3),
  poitrine: tour(100, 114, 33, 5),
  taille: tour(100, 152, 25, 4),
  hanches: tour(100, 192, 35, 5),
  poignet: tour(49, 236, 8, 2.5),
  carrureDevant: fleche(70, 98, 130, 98),
  epaule: fleche(92, 60, 63, 70),
  bras: <polyline points="57,72 45,100 39,180 37,236" />,
  longueurDevant: fleche(100, 64, 100, 152),
  entrejambeSol: fleche(100, 220, 100, 420),
  longueurDos: fleche(300, 52, 300, 152),
  carrureDos: fleche(270, 96, 330, 96),
  tailleHanches: hauteur(352, 192),
  tailleGenou: hauteur(364, 300),
  tailleSol: hauteur(376, 422),
};

export function Silhouette({ mesures, actif }: { mesures: Mesure[]; actif: Mesure | null }) {
  return (
    <svg viewBox="0 0 400 446" className="silhouette" role="img" aria-label="Où prendre chaque mesure, de face et de dos">
      <Corps x={0} titre="Devant" />
      <Corps x={200} titre="Dos" />
      {mesures.some((m) => m.startsWith("taille") && m !== "taille") && (
        <line x1={318} y1={152} x2={380} y2={152} className="repere" />
      )}
      {mesures.map((m) => (
        <g key={m} className={m === actif ? "trace actif" : "trace"}>
          {TRACES[m]}
        </g>
      ))}
    </svg>
  );
}
