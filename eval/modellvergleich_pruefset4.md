# Modellvergleich auf `pruefset4`

Gleicher Prompt, gleiches JSON-Schema, gleiche Prüfregeln. Alle Mails sind synthetisch.

| Kennzahl | qwen | haiku |
|---|---|---|
| Modell | qwen2.5:7b | claude-haiku-5-5 |
| Mails | 99 | 99 |
| Kategorie richtig | 78 % (77/99) | 96 % (95/99) |
| ohne mehrdeutige Mails | 81 % (60/74) | 99 % (73/74) |
| ohne Kategorie sonstiges | 86 % (64/74) | 95 % (70/74) |
| Ticket ohne Mensch | 75 % (74/99) | 57 % (56/99) |
| falsch automatisch geroutet | 11 | 2 |
| Pflicht-Reviews erkannt | 100 % (3/3) | 100 % (3/3) |
| Felder richtig ausgelesen | 100 % (31/31) | 100 % (31/31) |
| AB-Entscheidung richtig | 92 % (12/13) | 85 % (11/13) |
| AB fälschlich durchgewunken | 0 | 0 |
| Antwortzeit Median | 3.3 s | 4.9 s |
| Tokens je Mail (ein / aus) | 1086 / 231 | 3592 / 1031 |
| Listenpreis laut CLI, 1.000 Mails | – | 0.71 USD |
| Regel-Basislinie ohne KI | 59 % (58/99) | 59 % (58/99) |
