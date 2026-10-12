import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Évite que `next dev` réinjecte un bloc générique dans CLAUDE.md / AGENTS.md.
  agentRules: false,
  // Anciennes adresses, d'avant les gammes femme et homme : les patrons étaient en tailles femme.
  async redirects() {
    return [
      { source: "/patrons/:slug", destination: "/femme/:slug", permanent: true },
      { source: "/pdf/:fichier([^/]+\\.pdf)", destination: "/pdf/femme/:fichier", permanent: true },
    ];
  },
};

export default nextConfig;
