import { test } from 'node:test';
import assert from 'node:assert/strict';
import { validiere } from './helfer.mjs';

const verworfen = (r, feld) => {
  assert.equal(r.daten[feld], null);
  assert.ok(r.warnungen.includes(`beleg_fehlt:${feld}`), r.warnungen.join());
};

test('eine erfundene Bestellnummer wird verworfen', () => {
  verworfen(validiere('Vielen Dank.', { bestellnummer: '4500018266' }), 'bestellnummer');
});

test('eine Teilnummer zählt nicht als Beleg', () => {
  verworfen(validiere('Bestellung 4500018266', { bestellnummer: '450001826' }), 'bestellnummer');
});

test('Trennzeichen in Nummern sind erlaubt', () => {
  const r = validiere('Rechnung RE 2026 08817', { rechnungsnummer: 'RE-2026-08817' });
  assert.equal(r.daten.rechnungsnummer, 'RE-2026-08817');
});

for (const schreibweise of ['37.440,00', '37440.00', "37'440.00", '37 440,00']) {
  test(`Betrag in der Schreibweise ${schreibweise} gilt als belegt`, () => {
    assert.equal(validiere(`Summe ${schreibweise} EUR`, { betrag: 37440 }).daten.betrag, 37440);
  });
}

test('ein Betrag, der nur Teil einer größeren Zahl ist, wird verworfen', () => {
  verworfen(validiere('Summe 137.440,00 EUR', { betrag: 37440 }), 'betrag');
});

test('Stückpreis mit vier Nachkommastellen gilt als belegt', () => {
  assert.equal(validiere('je Stück 0,0420 EUR', { einzelpreis: 0.042 }).daten.einzelpreis, 0.042);
});

for (const schreibweise of ['20.11.2026', '20.11.', '20. November', '2026-11-20']) {
  test(`Liefertermin als "${schreibweise}" gilt als belegt`, () => {
    assert.equal(validiere(`Lieferung am ${schreibweise} geplant`, { liefertermin: '2026-11-20' }).daten.liefertermin, '2026-11-20');
  });
}

test('aus einer Kalenderwoche darf kein Datum werden', () => {
  verworfen(validiere('Lieferung in KW 48', { liefertermin: '2026-11-27' }), 'liefertermin');
});

test('fällt das Pflichtfeld durch die Belegprüfung, entscheidet ein Mensch', () => {
  const r = validiere('Wir bestätigen.', { kategorie: 'auftragsbestaetigung', bestellnummer: '4500099999' });
  assert.equal(r.entscheidung, 'review');
  assert.ok(r.gruende.includes('pflichtfeld_fehlt:bestellnummer'));
});
