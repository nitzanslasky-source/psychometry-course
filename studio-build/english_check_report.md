# Verbal originals: NITE-English check (2026-09-27)

Method: blind "spot the fake" tests. A fresh expert tester sees our originals shuffled with real official-English
NITE items of the same type (restored from exams_new_mix / exams_old_mix) and marks each REAL or IMITATION.
"Caught" = called imitation with confidence >= 3. Editors rewrote between rounds (rules: blind_tells.txt;
mechanical check: lint_originals.py; scripts in the session scratchpad: mix.py, score.py).

| Group | Round 1 caught | Final caught | Real items wrongly accused (final) |
|---|---|---|---|
| Sentence completion pt 2 (P41b) | 23/33 | **0/33** (round 4) | 16/55 |
| Sentence completion pt 1 (P41a) | 30/34 | 23/34 | 0/61 |
| Logic + sentences (P4243) | 38/54 | 38/54 | 0/59 |
| Science + rules (P4748) | 48/54 | 47/54 | 0/59 |
| Parables + strengthen/weaken (P4546) | 50/54 | 49/54 | 0/34 |
| Paragraphs (P44) | 47/47 | 47/47 | 0/62 |
| Reading passages (PRC) | 8/8 | 8/8 | 0/12 |
| Video questions (A/B/C) | 31/49 | 36/49 | 1/122 |

Testers' verdicts contradicted each other across rounds (too native vs too Hebrew; famous facts vs invented
authorities), so most groups oscillated rather than converged. The recipe that passed (P41b): draft in Hebrew,
then a professional (not word-for-word) translation; traces only in connectors and set phrases.

After the last rewrite every group was independently cold-solved (blind, then compared to the key): all keys
confirmed; ambiguous items fixed; real-world facts checked and corrected (P44: 11, reading: 7, P4748: 3).
Internal fields: he_draft (Hebrew draft), style_donor, facts - never exported to the student site.
