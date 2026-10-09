/** Le cachet rond de la maison : ATELIER en haut, FAIT POUR DURER en bas, A·T au centre. */
export function Ecusson({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 220 220" className={className} role="img" aria-label="Atelier AT, fait pour durer">
      <defs>
        <path id="ecusson-haut" d="M 40 110 A 70 70 0 0 1 180 110" />
        <path id="ecusson-bas" d="M 36 110 A 74 74 0 0 0 184 110" />
      </defs>
      <circle cx="110" cy="110" r="100" fill="none" stroke="currentColor" strokeWidth="1.6" />
      <circle cx="110" cy="110" r="94" fill="none" stroke="currentColor" strokeWidth=".7" />
      <circle cx="110" cy="110" r="56" fill="none" stroke="currentColor" strokeWidth=".7" strokeDasharray="3 3" />
      <text fontSize="15" letterSpacing="6" fill="currentColor">
        <textPath href="#ecusson-haut" startOffset="50%" textAnchor="middle">ATELIER</textPath>
      </text>
      <text fontSize="10.5" letterSpacing="3.2" fill="currentColor" dominantBaseline="hanging">
        <textPath href="#ecusson-bas" startOffset="50%" textAnchor="middle">FAIT POUR DURER</textPath>
      </text>
      <text x="110" y="128" textAnchor="middle" fontSize="50" fill="currentColor">
        A<tspan fontSize="22" dy="-14">·</tspan><tspan dy="14">T</tspan>
      </text>
      <circle cx="32" cy="110" r="2" fill="currentColor" />
      <circle cx="188" cy="110" r="2" fill="currentColor" />
    </svg>
  );
}
