import { test } from 'node:test';
import assert from 'node:assert/strict';
import { knoten } from '../scripts/knoten.mjs';

const eingang = (extra = {}) => knoten('Eingang prüfen', {
  body: { message_id: '<1@x>', from: 'A <a@alpen.example>', subject: 'Angebot', body: 'Hallo', ...extra },
});

test('fehlende Pflichtfelder werden abgewiesen', () => {
  const r = eingang({ subject: '  ', body: undefined });
  assert.equal(r.gueltig, false);
  assert.equal(r.fehler.length, 2);
});

test('HTML wird zu Text, Skripte verschwinden', () => {
  const r = eingang({ body: '<p>Preis&nbsp;5 EUR</p><script>alert(1)</script><b>Gruß</b>' });
  assert.match(r.mail.text, /Preis 5 EUR/);
  assert.doesNotMatch(r.mail.text, /[<>]|alert/);
});

test('lange Mails werden gekürzt und markiert', () => {
  const r = eingang({ body: 'x'.repeat(7000) });
  assert.equal(r.mail.text.length, 6000);
  assert.equal(r.mail.gekuerzt, true);
});

test('Weiterleitung mit AW: und Zitat hat denselben Inhaltsschlüssel', () => {
  const a = eingang({ message_id: '<1@x>', subject: 'Angebot', body: 'Unser Preis' });
  const b = eingang({ message_id: '<2@x>', subject: 'AW: WG: Angebot', body: 'Unser   Preis\n> alte Nachricht' });
  assert.equal(a.mail.inhalts_key, b.mail.inhalts_key);
});

test('anderer Absender ergibt anderen Inhaltsschlüssel', () => {
  assert.notEqual(eingang().mail.inhalts_key, eingang({ from: 'b@andere.example' }).mail.inhalts_key);
});

test('der Prompt klammert die Mail ein und entfernt spitze Klammern im Absender', () => {
  const { mail } = eingang();
  const r = knoten('Prompt bauen', {}, {
    Konfiguration: { ollama_model: 'qwen2.5:7b' },
    'Eingang prüfen': { mail },
  });
  const nutzer = r.ollama_request.messages[1].content;
  assert.equal(nutzer.match(/<\/?mail>/g).length, 2);
  assert.match(nutzer, /Absender: A a@alpen\.example\n/);
  assert.equal(r.ollama_request.options.temperature, 0);
});
