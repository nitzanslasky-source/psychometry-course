# Audit T17 - The Number Line (additions of the 2026-09 patch)

Sources: `math_patches/t17_CHANGES.md`, `math_patches/t17.py`, `real_exam/quant_real.md` (full text), original course = `course18.json` (pre-patch).
Rule 2 (coordinator): a method is kept when ORIGINAL course questions need it, even without a real-exam match.
Real "number_line" group has only 2 items (2023_autumn_q1_15, 2025_spring_q1_02); the same skills appear in inequalities_absolute (35) as text-given orders and ranges.

| Addition | Where | Class | Verdict | Evidence (real ids / count) |
|---|---|---|---|---|
| Negative exponent: one two-case rule everywhere | `number-line` slide 6, `powers-on-number-line` slide 7 + recap, card mem-number-line tip | FIX | KEEP | - |
| "Odd" defined for a negative base; "Negative fractions: right - for odd powers" | `powers-on-number-line` slides 2, 5; card | FIX | KEEP | - |
| Hierarchy condition (positive powers/roots; negatives: odd only) | `number-line` slide 5 | FIX | KEEP | - |
| "Same operation" only for positive numbers (−3 < −2 but squares flip) | `number-line` slide 7 + card tip | FIX | KEEP | 2024_spring_q2_04 (t² = w²), 2026_spring_q2_10 |
| q-500 method 2 trick removed; new x = 1/1024 plug-in; q-495 solution reason | solve-q-500 slide 3, q-495 expl | FIX | KEEP | - |
| "12 : 3" → "12 ÷ 3"; recap conditions | `number-line` slide 4, recap; card | FIX | KEEP | - |
| New video "Reading the Number Line" - slide "Times a negative" (order flips) + card row "× a negative number" | `r26-t17-reading-the-line` slide 2; mem-number-line row | METHOD | KEEP | 2025_spring_q2_06 (D = a − b range), 2020_winter_q2_14, 2019_spring_q1_06; rule 2: original q-510 (3a < x < a) |
| Slide "Reciprocals" (four-range table; same sign → order flips) | same video slide 3 + mem-r26-t17-reading table | METHOD | KEEP | 2026_spring_q1_17 (−1/2 < 1/x < 1/2 → exact range of x); rule 2: alg-extra-unit-t17-3-4, q-508, q-500 |
| Slide "Test numbers" (2, 1/2, −1/2, −2, borders; nice numbers for roots) | same video slide 4 + card table | METHOD | KEEP | 2023_spring_q1_08, 2021_autumn_q1_07 (1 < x < 2, largest), 2020_spring_q1_18 |
| Slide "Must or could" (counterexample at the edges; one example proves "could") | same video slide 5 | METHOD | KEEP | 2020_autumn_q2_19 (M can be any number, including 1), 2020_winter_q2_14, 2024_spring_q1_03 |
| Slide "Picture questions" (range under each letter; trust order, not distances) | same video slide 6 + figure FIG_DEMO | METHOD / format | KEEP | real number-line figures: 2025_spring_q1_02, 2023_autumn_q1_15; same task in text form: 2023_autumn_q1_01; rule 2: original q-465 (p < q < 0 < r < s "on a number line") |
| Slide "Distance & midpoint" (bigger − smaller, (a+b)/2, a third of the way) + card table | same video slide 7 | METHOD | KEEP | 2025_spring_q1_02 (equal gaps on a number line, find B), 2020_spring_q2_03 (4 equal parts); rule 2: alg-extra-unit-t17-3-3, -3-6, q-504 |
| New card mem-r26-t17-reading | after the new video | card | KEEP | as above |
| Guided Q10 q-r26-t17-01 (figure a, b, c, d; necessarily negative: b·c·d) + solve video | advanced section | practice | KEEP | 2023_autumn_q1_01 (c < b < 0 < a: which product necessarily positive), 2021_autumn_q2_15 |
| Guided Q11 q-r26-t17-02 (figure: which point could be √x) + solve video | advanced section | practice (new format) | UNSURE | The math (√x vs x in a range) is original T17 content, but "which marked point could represent f(x)" has 0 real items; closest real format 2023_autumn_q1_15 ("which drawing could describe"), 2023_autumn_q1_07 (3 < x < 4: which value could x be). Teacher to decide |
| Guided Q12 q-r26-t17-03 (−4 < x < −2, range of 6/x) + solve video | advanced section | practice | KEEP | 2026_spring_q1_17 |
| Guided Q13 q-r26-t17-04 (x < −1 < y < 0, edges: x + y < −1) + solve video | advanced section | practice | KEEP | 2020_winter_q2_14 (10 < b, a < −1 → a − b < −11), 2025_spring_q2_06 |
| Guided Q14 q-r26-t17-05 (point one third of the way from −7 to 5) + solve video | advanced section | practice | KEEP | 2025_spring_q1_02, 2020_spring_q2_03 |
| 6 new number-line SVG figures | Q10, Q11, -06, -07, -08, demo slide | FIX / format | KEEP (follow their questions) | 2025_spring_q1_02 has a number-line figure |
| Practice q-r26-t17-06 (figure: smallest of a, ab, a/b, a²) | unit-t17-3 | practice | KEEP | 2023_autumn_q1_01; original q-497, q-511 type |
| Practice q-r26-t17-07 (figure: x/y − 1 positive) | unit-t17-3 | practice | KEEP | 2021_autumn_q2_15, 2023_autumn_q1_01 |
| Practice q-r26-t17-08 (figure: which point could be x³) | unit-t17-3 | practice (new format) | UNSURE | same as Q11 |
| Practice q-r26-t17-09 (reciprocal of −2 < x < −1/2) | unit-t17-3 | practice | KEEP | 2026_spring_q1_17 |
| Practice q-r26-t17-10 (range of 1 − 3x) | unit-t17-3 | practice | KEEP | 2025_spring_q2_06, 2019_spring_q1_06 |
| Practice q-r26-t17-11 (x³ < x, which could be x; border trap) | unit-t17-3 | practice | KEEP | 2020_spring_q1_18; original q-498, q-509 type |
| Practice q-r26-t17-12 (point twice as far from A as from B) | unit-t17-3 | practice | KEEP | 2025_spring_q1_02, 2020_spring_q2_03 |
| Practice q-r26-t17-13 (−1 < a < 0 < b: could equal 1) | unit-t17-3 | practice | KEEP | 2020_autumn_q2_19 |
| Practice q-r26-t17-14 (0 < x < 1 < y, edges) | unit-t17-3 | practice | KEEP | 2020_winter_q2_14 |
| Practice q-r26-t17-15 (0 < a < b < 1: largest of 1/a, b/a, 1/b) | unit-t17-3 | practice | KEEP | 2021_autumn_q1_07 (largest of 2x, 2/x, x², x^x) |
| Text: TeX, nicer numbers, q-499 stem, q-503 exponent, alg-extra t17-3-4 impossible choice | all questions | FIX | KEEP | - |

## TO REMOVE
- Nothing certain. UNSURE (teacher decides): guided `q-r26-t17-02` + `solve-q-r26-t17-02` and practice `q-r26-t17-08` ("which marked point could represent √x / x³": no real item of this format; the underlying math is original T17 content). If removed, also drop FIG_Q11 and FIG_P3.

## ORIGINAL ITEMS REMOVED OR REPLACED BY THE FIXERS (restore candidates)
- Removed: `q-505` (1 < m < n, largest of n³, mn², m²n, m³), `alg-extra-unit-t17-3-1` (−1 < x < 0, greatest of x, x³, −1, x²).
- Replaced content: solve-q-500 Method 2 ("replace every ten with a two" trick - it was invalid); q-495 written solution reason; alg-extra-unit-t17-3-4 choice "1/2 < 1/x < 1/5" replaced; q-499 "orderings" stem reworded; q-503 exponent fixed; `powers-on-number-line` slide 7 line "No need to flip" replaced; q-504 reworded as a distance.

Counts: KEEP 28 · REMOVE 0 · UNSURE 2
