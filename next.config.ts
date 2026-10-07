import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Évite que `next dev` réinjecte un bloc générique dans CLAUDE.md / AGENTS.md.
  agentRules: false,
};

export default nextConfig;
