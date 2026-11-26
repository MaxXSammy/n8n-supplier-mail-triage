// Führt den JavaScript-Code eines n8n-Code-Nodes außerhalb von n8n aus.
// Der Code wird direkt aus der Workflow-Datei gelesen: Getestet wird genau das, was in n8n läuft.
import { readFileSync } from 'node:fs';

const WORKFLOW = new URL('../workflows/01_mail_triage.json', import.meta.url);
const nodes = JSON.parse(readFileSync(WORKFLOW, 'utf8')).nodes;

/**
 * Nur für Code-Nodes im Modus "Run Once for Each Item".
 * @param {string} name   Name des Nodes im Workflow
 * @param {object} json   Eingabe des Nodes ($json)
 * @param {object} andere Ausgaben früherer Nodes, auf die der Code per $('Name') zugreift
 * @returns {object}      Das json-Objekt, das der Node zurückgibt
 */
export function knoten(name, json, andere = {}) {
  const node = nodes.find((n) => n.name === name);
  if (!node?.parameters.jsCode) throw new Error(`Kein Code-Node "${name}" im Workflow`);
  const $ = (anderer) => {
    if (!(anderer in andere)) throw new Error(`"${name}" braucht die Ausgabe von "${anderer}"`);
    return { item: { json: andere[anderer] } };
  };
  // Kopie, damit ein Node die Eingabe eines Tests nicht verändern kann
  return new Function('$json', '$', node.parameters.jsCode)(structuredClone(json), $).json;
}
