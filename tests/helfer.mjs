import { knoten } from '../scripts/knoten.mjs';

export const mail = (text, extra = {}) => ({
  mail_id: '<test@example>',
  absender: 'Vertrieb <vertrieb@alpen.example>',
  betreff: 'Bestellung',
  text,
  empfangen_am: '2026-11-02T10:00:00+01:00',
  ...extra,
});

// Vollständige, schemagültige Antwort des Modells. Tests überschreiben nur, was sie brauchen.
export const antwort = (extra = {}) => ({
  begruendung: 'Test', kategorie: 'sonstiges', konfidenz: 0.95, lieferant: null,
  bestellnummer: null, rechnungsnummer: null, angebotsnummer: null, artikel: null,
  einzelpreis: null, menge: null, betrag: null, waehrung: null, liefertermin: null,
  liefertermin_unsicher: false, abweichungsgrund: null, dringlichkeit: 'mittel',
  zusammenfassung: 'Test', ...extra,
});

export function validiere(text, daten = {}, { betreff, roh, llm } = {}) {
  const m = mail(text, betreff === undefined ? {} : { betreff });
  const eingabe = llm ?? { message: { content: roh ?? JSON.stringify(antwort(daten)) } };
  return knoten('Ausgabe validieren', eingabe, {
    Konfiguration: { konfidenz_schwelle: 0.75 },
    'Prompt bauen': { mail: m },
  });
}
