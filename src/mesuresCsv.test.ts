import assert from "node:assert/strict";
import { test } from "node:test";
import { depuisCsv, versCsv } from "./mesuresCsv.ts";

test("le fichier téléchargé se relit à l'identique", () => {
  const valeurs = { bust_circ: "88,5", waist_circ: "70", leg_crotch_to_floor: "79.5" };
  assert.deepEqual(depuisCsv(versCsv(valeurs)), {
    valeurs: { bust_circ: "88,5", waist_circ: "70", leg_crotch_to_floor: "79,5" },
    ignorees: 0,
  });
});

test("le fichier écrit une mesure par ligne, sans les cases vides ni fausses", () => {
  assert.equal(
    versCsv({ hip_circ: "98", waist_circ: "", neck_circ: "beaucoup" }),
    "code;mesure;cm\r\nhip_circ;Tour de hanches;98\r\n",
  );
});

test("une mesure se reconnaît aussi à son libellé, et les lignes inconnues sont comptées", () => {
  const csv = "﻿mesure;cm\nTour de Hanches;98\ntour d’encolure;37\nlongueur de jupe;60\ntour de taille;\n";
  assert.deepEqual(depuisCsv(csv), { valeurs: { hip_circ: "98", neck_circ: "37" }, ignorees: 2 });
});

test("un fichier repassé par un tableur anglais (virgules) se relit aussi", () => {
  const csv = 'code,mesure,cm\nbust_circ,Tour de poitrine,"88,5"\nwaist_circ,Tour de taille,70\n';
  assert.deepEqual(depuisCsv(csv).valeurs, { bust_circ: "88,5", waist_circ: "70" });
});
