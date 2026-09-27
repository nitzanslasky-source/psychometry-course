# Audit T19 - Defining a New Operation (additions of the 2026-09 patch)

Sources: `math_patches/t19_CHANGES.md`, `math_patches/t19.py`, `real_exam/quant_real.md` (full text), original course = `course18.json` (pre-patch).
Rule 2 (coordinator): a method is kept when ORIGINAL course questions need it, even without a real-exam match.
Real defined_operations group: 16 items (+ 2025_autumn_q1_07 in coordinate_system). None is piecewise (odd/even or x ≥ 0 branches), none uses an integer part [x].

| Addition | Where | Class | Verdict | Evidence (real ids / count) |
|---|---|---|---|---|
| "Operation first" rule replaced ("turn every ◆(…) into a number first"; a★b inside an exercise comes with brackets) | `new-operation` slide "Operation first", recap, card row | FIX | KEEP | - |
| Q13 (q-553) method 2, Q12 (q-552) method 2, Q15 (q-555) wording, q-567 made unambiguous, Q9/Q16 plug-in caveats | solution videos, q-567 | FIX | KEEP | - |
| New slide "Brackets on every input" (◆(−3), ◆(x+1)) | `new-operation` new slide 5 + card rows | METHOD | KEEP | 2025_spring_q2_05 (2 $ −6), 2021_autumn_q2_06 ($(−2, 3)), 2023_autumn_q1_12 ($(1/a²)), 2022_autumn_q2_14 ($(x+1)) |
| Slide "Order can matter" (counterexample for "not always"; swap letters for "always"; never equal values) | `new-operation` slide 9 + card row | METHOD | KEEP | 2021_autumn_q2_06 ($(−2,3) / $(3,−2)), 2026_spring_q1_19 (claims: counterexample); rule 2: q-567, alg-extra-unit-t19-3-4 |
| Slide "Unknown input": work back from the answers | `new-operation` slide 10 | METHOD | KEEP | 2024_winter_q2_20 (inverse operation), 2020_autumn_q1_09; rule 2: alg-extra-unit-t19-3-5 |
| Worked examples added to every board of "Operation Patterns" (conditions forward, circular, isolate) | `operation-patterns` slides | FIX | KEEP | circular/recursive: 2022_autumn_q2_14 ($(x+1) = 2·$(x)); rule 2: q-545, q-546, q-547, q-548, q-566, q-569 |
| New slide "Conditions backwards" (◆(x) = 9 with two rules; reject answers that break their own rule) | `operation-patterns` new slide 4 + card row "conditions with the result given" | CONTENT | REMOVE | 0 real piecewise questions (forward or backward); no original course question solves a piecewise operation backwards |
| New slide "Definition in words" - the method (write examples first; remainder, divisors, digit sum) | `operation-patterns` new slide 7 + card row | METHOD | KEEP | 2024_spring_q2_05 (remainder by 50), 2026_spring_q1_19 (digit sum), 2024_autumn_q1_18 (n ones), 2023_winter_q2_14; rule 2: q-556, q-571, q-576 |
| Same slide - its main example, the integer part [x] ([3.7] = 3, [−2.3] = −3) | `operation-patterns` "Definition in words" boards "[x] = the largest integer…" and "[3.7] = 3 [5] = 5 [−2.3] = ?" + card example | CONTENT | REMOVE | 0 real questions use an integer part / floor. Replace the example with a real word definition (remainder by 50, digit sum) |
| Slide "Must be true?" (was "Necessarily true?"): link to T1, plug-in rules (avoid 0, 1, equal values; second number) | `operation-patterns` slide 8 + card tips | METHOD | KEEP | 2026_spring_q1_19, 2020_autumn_q1_09, 2023_spring_q1_20 |
| Guided Q4 q-r26-t19-01 (◆(x+1) for ◆(x) = x² − 2x) + solve video | theory section | practice | KEEP | 2022_autumn_q2_14, 2023_autumn_q1_12 |
| Guided Q5 q-r26-t19-02 (which a★b is always commutative) + solve video | theory section | practice | KEEP | 2021_autumn_q2_06; "which definition has property P" type: 2020_autumn_q1_09, 2023_spring_q1_20, 2021_spring_q1_08 |
| Guided Q8 q-r26-t19-03 (solve ◆(x) = 24 with odd/even rules) + solve video | theory section | CONTENT (piecewise backwards) | REMOVE | 0 real |
| Guided Q12 q-r26-t19-04 ([−2.5] + [2.5] + [0.5]) + solve video | advanced section | CONTENT (integer part) | REMOVE | 0 real |
| Guided Q16 q-r26-t19-05 (◆(2) − ◆(−2): odd powers survive) + solve video, card row "◆(k) − ◆(−k)" | advanced section | METHOD practice | KEEP (rule 2) | 0 real; same type as original q-564, q-568 |
| Card mem-new-operation rewritten (15 rows) | card | FIX | KEEP except rows listed below | - |
| Practice q-r26-t19-06 (◆(−2), bracket trap) | unit-t19-3 | practice | KEEP | 2025_spring_q2_05, 2021_autumn_q2_06 |
| Practice q-r26-t19-07 (◆(x−1), answers in x) | unit-t19-3 | practice | KEEP | 2022_autumn_q2_14, 2024_autumn_q1_18 |
| Practice q-r26-t19-08 (◆(1/x)) | unit-t19-3 | practice | KEEP | 2023_autumn_q1_12 |
| Practice q-r26-t19-09 (◆(3) = 6, ◆(5) = 20: which could be the definition) | unit-t19-3 | practice | KEEP | 2022_autumn_q2_14, 2021_spring_q1_08; original q-543 |
| Practice q-r26-t19-10 (odd/even rule applied 4 times, forward) | unit-t19-3 | practice of an original type | KEEP | 0 real piecewise, but the type is original course content (q-545) |
| Practice q-r26-t19-11 (for how many integers ◆(x) = 4, two branches) | unit-t19-3 | CONTENT (piecewise backwards) | REMOVE | 0 real |
| Practice q-r26-t19-12 (circular rule ×3 − 2) | unit-t19-3 | practice | KEEP | 2022_autumn_q2_14; original q-569 |
| Practice q-r26-t19-13 (period-3 operation 1/(1 − x), nested) | unit-t19-3 | practice | KEEP | 2023_spring_q1_20 ($($(x)) = x), 2025_autumn_q2_13 ($($(√2))), 2020_autumn_q1_09 |
| Practice q-r26-t19-14 ([x] = 3, which x) | unit-t19-3 | CONTENT (integer part) | REMOVE | 0 real |
| Practice q-r26-t19-15 (two-digit numbers with digit sum 5) | unit-t19-3 | practice | KEEP | 2025_autumn_q1_05 (two-digit, digit sum 5), 2026_spring_q1_19 |
| Practice q-r26-t19-16 (a★b = ab − a − b must be true; a = 0 trap) | unit-t19-3 | practice | KEEP | 2026_spring_q1_19 |
| Practice q-r26-t19-17 (◆(x) = x³ must be true; 0 and 1 fool you) | unit-t19-3 | practice | KEEP | 2026_spring_q1_19, 2023_spring_q1_20 |
| Text: TeX, cases for piecewise/circular, "necessarily" → "must be true", extras' NITE stems | all questions | FIX | KEEP | - |

## TO REMOVE
- Video `operation-patterns`, slide "Conditions backwards" (whole slide); remove it from the sidebar and its line from the recap.
- Video `operation-patterns`, slide "Definition in words": remove the integer-part example (boards "[x] = the largest integer that is not bigger than x", "[3.7] = 3, [5] = 5, [−2.3] = ?" and the note "= −3, not −2", and the script lines about [x]); keep the rule "definition in words: write examples first" with a real-type example (remainder, digit sum).
- Card `mem-new-operation`: row "conditions with the result given" and the [x] example in the "definition in words" row.
- Guided `q-r26-t19-03` + `solve-q-r26-t19-03`; guided `q-r26-t19-04` + `solve-q-r26-t19-04` (renumber guided questions afterwards).
- Practice `q-r26-t19-11`, `q-r26-t19-14`.

## ORIGINAL ITEMS REMOVED OR REPLACED BY THE FIXERS (restore candidates)
- Removed: `alg-extra-unit-t19-3-3` (F(x) = x² − 3, F(F(2))), `alg-extra-unit-t19-3-6` (H(x) = 1/x, H(H(4))).
- Changed question content: `q-567` (now only positive integers; choice 2 "x~0 = 10x" became "x~1 = 10x + 1"; sentence "Repeated inputs and appending 0 are allowed" removed), `q-546` condition rewritten ("x ≥ 2"), "necessarily true" stems → "must be true" (q-549, q-555, q-556, q-573, q-574).
- Replaced slide/video content: `new-operation` slide "Operation first" (old rule "before powers, times, divide - only brackets beat it"), `operation-patterns` slide "Necessarily true?" (now "Must be true?"), solve-q-553 method 2 ("same power on both letters → a/b or b/a"), solve-q-552 line "Some students stop right here. Why?", solve-q-555 "A negative power flips floors".

Counts: KEEP 23 · REMOVE 6 · UNSURE 0
