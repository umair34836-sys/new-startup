// Generate a melody over C|Am|F|G|Am F|C with Magenta's Improv RNN and keep the best take.
import { createRequire } from "node:module";
import fs from "node:fs";
const require = createRequire(import.meta.url);
const mm = require("@magenta/music/node/music_rnn");

globalThis.performance = globalThis.performance || (await import("node:perf_hooks")).performance;
const URL = process.argv[2];
const OUT = process.argv[3];
const rnn = new mm.MusicRNN(URL);
await rnn.initialize();

// One bar of seed (16 steps): G4 C5 E5 ... a gentle rising opening over C.
const seed = {
  quantizationInfo: { stepsPerQuarter: 4 },
  totalQuantizedSteps: 16,
  notes: [
    { pitch: 67, quantizedStartStep: 0, quantizedEndStep: 4 },
    { pitch: 72, quantizedStartStep: 4, quantizedEndStep: 8 },
    { pitch: 76, quantizedStartStep: 8, quantizedEndStep: 16 },
  ],
};
const chords = ["C", "C", "Am", "Am", "F", "F", "G", "G", "Am", "F", "C", "C"];
const chordTones = { C: [0, 4, 7], Am: [9, 0, 4], F: [5, 9, 0], G: [7, 11, 2] };

function score(notes) {
  if (notes.length < 12 || notes.length > 34) return -1e9;
  let s = 0;
  const pitches = notes.map((n) => n.pitch);
  const range = Math.max(...pitches) - Math.min(...pitches);
  if (range > 16) s -= (range - 16) * 3;
  for (let i = 1; i < notes.length; i++) {
    const leap = Math.abs(notes[i].pitch - notes[i - 1].pitch);
    if (leap > 7) s -= 2;
    if (leap <= 2) s += 0.6;
  }
  for (const n of notes) {
    const step = n.quantizedStartStep + 16;
    const chord = chords[Math.floor(step / 8)];
    const onBeat = step % 4 === 0;
    if (chordTones[chord].includes(n.pitch % 12)) s += onBeat ? 1.5 : 0.5;
    else if (onBeat) s -= 1;
    if (n.quantizedEndStep - n.quantizedStartStep >= 4) s += 0.4;
  }
  const last = notes[notes.length - 1];
  if (last.pitch % 12 === 0) s += 6;
  if (last.quantizedEndStep >= 72) s += 3;
  return s;
}

const takes = [];
for (let i = 0; i < 12; i++) {
  const temp = 0.85 + 0.03 * i;
  const cont = await rnn.continueSequence(seed, 80, temp, chords);
  const notes = cont.notes.map((n) => ({ pitch: n.pitch, quantizedStartStep: n.quantizedStartStep, quantizedEndStep: n.quantizedEndStep }));
  takes.push({ temp, score: score(notes), notes });
  console.log(`take ${i} temp=${temp.toFixed(2)} notes=${notes.length} score=${score(notes).toFixed(1)}`);
}
takes.sort((a, b) => b.score - a.score);
fs.writeFileSync(OUT, JSON.stringify({ seed: seed.notes, best: takes[0], all: takes }, null, 1));
console.log("best", takes[0].temp.toFixed(2), takes[0].score.toFixed(1));
