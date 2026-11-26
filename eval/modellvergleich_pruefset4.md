# Modellvergleich auf `pruefset4`

Gleicher Prompt, gleiches JSON-Schema, gleiche Prüfregeln. Alle Mails sind synthetisch.

| Kennzahl | qwen |
|---|---|
| Modell | qwen2.5:7b |
| Mails | 99 |
| Kategorie richtig | 78 % (77/99) |
| ohne mehrdeutige Mails | 81 % (60/74) |
| ohne Kategorie sonstiges | 86 % (64/74) |
| Ticket ohne Mensch | 75 % (74/99) |
| falsch automatisch geroutet | 11 |
| Pflicht-Reviews erkannt | 100 % (3/3) |
| Felder richtig ausgelesen | 100 % (31/31) |
| AB-Entscheidung richtig | 92 % (12/13) |
| AB fälschlich durchgewunken | 0 |
| Antwortzeit Median | 3.3 s |
| Tokens je Mail (ein / aus) | 1086 / 231 |
| Listenpreis laut CLI, 1.000 Mails | – |
| Regel-Basislinie ohne KI | 59 % (58/99) |
