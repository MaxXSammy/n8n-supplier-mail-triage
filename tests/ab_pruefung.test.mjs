// Abgleich der Auftragsbestätigung mit der Bestellung (Regeln: docs/fachkonzept.md)
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { knoten } from '../scripts/knoten.mjs';
import { mail, antwort } from './helfer.mjs';

const BESTELLUNG = {
  bestellnummer: '4500018266', menge: '1000', einzelpreis: '3.1200', waehrung: 'EUR', wunschtermin: '2026-11-20',
  mail_domain: 'alpen.example', abc_xyz: 'AX', liefertreue_prozent: '95', neu: false,
  versendet_am: '2026-11-01T10:00:00+01:00', lieferant_name: 'Alpen', einkaeufer: 'Weber',
  einstellungen: { liefertreue_schwelle_kritisch: '90', liefertreue_schwelle_standard: '80', blindbestaetigung_minuten: '30' },
};

function pruefe({ daten = {}, bestellung = {}, text = 'Wir bestätigen.', kopf = {} } = {}) {
  return knoten('AB prüfen', { ...BESTELLUNG, ...bestellung }, {
    'Ausgabe validieren': {
      entscheidung: 'ticket', gruende: [], warnungen: [], mail: mail(text, kopf),
      daten: antwort({ kategorie: 'auftragsbestaetigung', menge: 1000, einzelpreis: 3.12, liefertermin: '2026-11-20', ...daten }),
    },
  });
}

const arten = (r) => r.ab.abweichungen.map((a) => a.art);

test('passende AB eines zuverlässigen Lieferanten geht automatisch durch', () => {
  const r = pruefe();
  assert.equal(r.ab.ergebnis, 'automatisch_bestaetigt');
  assert.equal(r.ticket.team, 'Disposition');
});

test('unbekannte Bestellnummer geht ins Review', () => {
  const r = pruefe({ bestellung: { bestellnummer: null } });
  assert.equal(r.entscheidung, 'review');
  assert.ok(r.gruende.includes('bestellung_unbekannt'));
});

for (const [name, fall, art] of [
  ['höherer Preis', { daten: { einzelpreis: 3.2 } }, 'preis'],
  ['niedrigerer Preis', { daten: { einzelpreis: 3.0 } }, 'preis'],
  ['andere Menge', { daten: { menge: 1100 } }, 'menge'],
  ['späterer Termin', { daten: { liefertermin: '2026-11-21' } }, 'termin_spaeter'],
  ['fehlender Termin', { daten: { liefertermin: null } }, 'termin_fehlt'],
  ['unsicherer Termin', { daten: { liefertermin_unsicher: true } }, 'termin_unsicher'],
  ['andere Währung', { daten: { waehrung: 'EUR' }, bestellung: { waehrung: 'CHF' }, text: 'Preis 3,12 EUR' }, 'waehrung'],
]) {
  test(`Abweichung: ${name} geht an den Einkäufer`, () => {
    const r = pruefe(fall);
    assert.equal(r.ab.ergebnis, 'abweichung');
    assert.deepEqual(arten(r), [art]);
    assert.equal(r.ticket.zustaendig, 'Weber');
  });
}

test('ein früherer Termin ist keine Abweichung', () => {
  assert.deepEqual(arten(pruefe({ daten: { liefertermin: '2026-11-19' } })), []);
});

test('eine Währung, die nicht im Mailtext steht, löst nichts aus', () => {
  assert.deepEqual(arten(pruefe({ daten: { waehrung: 'USD' } })), []);
});

for (const [text, bestellt] of [
  ['3000 Stk zu 0.92 EUR', 'CHF'],
  ['Preis 3,12 €', 'CHF'],
  ['Preis Fr. 3.12', 'EUR'],
]) {
  test(`Währung aus dem Mailtext, auch wenn das Modell keine liefert: "${text}" bei Bestellung in ${bestellt}`, () => {
    assert.deepEqual(arten(pruefe({ text, bestellung: { waehrung: bestellt } })), ['waehrung']);
  });
}

for (const text of ['Preis 3,12 CHF, Fracht 40 EUR', 'Fr. Weber bestätigt den Auftrag.', 'Wir bestätigen wie bestellt.']) {
  test(`kein Währungsalarm: "${text}"`, () => {
    assert.deepEqual(arten(pruefe({ text, bestellung: { waehrung: 'CHF' } })), []);
  });
}

test('eine Währungsabweichung wird nur einmal gemeldet', () => {
  const r = pruefe({ daten: { waehrung: 'EUR' }, bestellung: { waehrung: 'CHF' }, text: 'Preis 3,12 EUR' });
  assert.deepEqual(arten(r), ['waehrung']);
});

test('Mengenänderung wegen Verpackungseinheit meldet auch die Stammdaten', () => {
  const r = pruefe({ daten: { menge: 1100 }, text: 'Anpassung an unsere Verpackungseinheit.' });
  assert.deepEqual(arten(r), ['menge', 'stammdaten_pruefen']);
});

test('fremde Absender-Domain verhindert die automatische Bestätigung', () => {
  const r = pruefe({ kopf: { absender: 'vertrieb@a1pen.example' } });
  assert.equal(r.ab.ergebnis, 'manuell_pruefen');
  assert.deepEqual(r.ab.pruefgruende, ['absender_domain_abweichend']);
});

for (const [artikel, liefertreue, ergebnis] of [
  ['AX', '90', 'automatisch_bestaetigt'],
  ['AX', '89.9', 'manuell_pruefen'],
  ['CX', '85', 'manuell_pruefen'],
  ['CZ', '80', 'automatisch_bestaetigt'],
  ['CZ', '79', 'manuell_pruefen'],
]) {
  test(`${artikel}-Artikel mit ${liefertreue} % Liefertreue: ${ergebnis}`, () => {
    assert.equal(pruefe({ bestellung: { abc_xyz: artikel, liefertreue_prozent: liefertreue } }).ab.ergebnis, ergebnis);
  });
}

test('neuer Lieferant wird immer manuell geprüft', () => {
  assert.deepEqual(pruefe({ bestellung: { neu: true } }).ab.pruefgruende, ['neuer_lieferant']);
});

test('Bestätigung nach wenigen Minuten gilt als Blindbestätigung', () => {
  const r = pruefe({ bestellung: { versendet_am: '2026-11-02T09:50:00+01:00' } });
  assert.deepEqual(r.ab.pruefgruende, ['blindbestaetigung_verdacht']);
});
