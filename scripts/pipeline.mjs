// Prüfstrecke ohne n8n für den Modellvergleich. Liest JSON von stdin, schreibt JSON nach stdout.
//   node scripts/pipeline.mjs bauen    { mails: {name: mail} }
//   node scripts/pipeline.mjs pruefen  { faelle: {name: {mail, antwort}}, bestellungen: {nummer: zeile} }
// Alle Regeln stammen aus den Code-Nodes des Workflows (siehe knoten.mjs).
import { readFileSync } from 'node:fs';
import { knoten } from './knoten.mjs';

const KONFIG = { ollama_model: 'qwen2.5:7b', konfidenz_schwelle: 0.75 };
const eingabe = JSON.parse(readFileSync(0, 'utf8'));
const eingang = (mail) => {
  const e = knoten('Eingang prüfen', { body: mail });
  if (!e.gueltig) throw new Error(`Ungültige Mail: ${e.fehler.join(', ')}`);
  return e;
};

function bauen(mail) {
  return knoten('Prompt bauen', {}, { Konfiguration: KONFIG, 'Eingang prüfen': eingang(mail) }).ollama_request;
}

// Gleicher Ablauf wie im Workflow: validieren, bei Auftragsbestätigungen zusätzlich gegen die Bestellung prüfen
function pruefen({ mail, antwort }, bestellungen) {
  let v = knoten('Ausgabe validieren', antwort, {
    Konfiguration: KONFIG,
    'Prompt bauen': { mail: eingang(mail).mail },
  });
  if (v.entscheidung === 'ticket' && v.daten.kategorie === 'auftragsbestaetigung') {
    v = knoten('AB prüfen', bestellungen[v.daten.bestellnummer] ?? {}, { 'Ausgabe validieren': v });
  }
  return { status: v.entscheidung, gruende: v.gruende, warnungen: v.warnungen, daten: v.daten, ab_pruefung: v.ab ?? null };
}

const [schritt] = process.argv.slice(2);
let ausgabe;
if (schritt === 'bauen') {
  ausgabe = Object.fromEntries(Object.entries(eingabe.mails).map(([n, m]) => [n, bauen(m)]));
} else if (schritt === 'pruefen') {
  ausgabe = Object.fromEntries(Object.entries(eingabe.faelle).map(([n, f]) => [n, pruefen(f, eingabe.bestellungen)]));
} else {
  throw new Error('Aufruf: node scripts/pipeline.mjs bauen|pruefen');
}
process.stdout.write(JSON.stringify(ausgabe));
