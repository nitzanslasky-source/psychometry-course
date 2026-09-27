# Audit t03: Comparing Fractions (additions from the 2026-09 fixers)

Sources: `math_patches/t03_CHANGES.md` and `math_patches/t03.py`. Lesson video `compare-fractions`, learn section
`fraction-theory`, practice `unit-t3-1`, card `mem-compare`. Originals checked against git `0205ceb^:content/full-course/topics/t3.json`.

Note on the evidence file: the first version of `real_exam/quant_real.md` lost stem text after a `<` sign; this audit
then read the full stems from `~/nite-psychometry/content/psychometric_*_quant.json`. **Re-check (after the file was
regenerated with full text):** every id cited below was re-read in the fixed file; all stems and keys match what was
used. The inequalities group (35 items) was read in full again; two more supporting items were found and added
(2025_autumn_q1_16, 2023_spring_q1_08). No verdict changed.

Key real questions used below (full text):
- **2021_autumn_q2_16**: girls/boys 16/15, 17/16, 18/17 in grades 7-9; in which grade is the proportion of girls the greatest? (key: 7th). The proportions are 16/31, 17/33, 18/35. Girls:boys is 16/15, 17/16, 18/17: +1 on the top and the bottom above 1 moves the ratio toward 1, which is the same as comparing the extras 1/15 > 1/16 > 1/17. The proportions add a 1/2 piece at each step (+1 top, +2 bottom), and 16/31 > 1/2, so they fall toward 1/2.
- **2022_autumn_q1_08**: 0 < a < 1/4; which is the smallest of −1/a, −a, −√a, −a/4? (key: −1/a). This is the x-range order for a small positive number, with negatives: compare without the minus, then reverse.
- **2021_autumn_q1_07**: 1 < x < 2; which is the greatest of 2x, 2/x, x², x^x? (plug in a value from the range and use the x > 1 order).
- **2026_spring_q1_17**: −1/2 < 1/x < 1/2 (x ≠ 0); exact range of x (key: x < −2 or 2 < x). Flipping only works for the same sign, and the sign of the bottom is unknown.
- **2020_autumn_q1_13**: 0 < a, 0 < (a+b)/a < 1; which is necessarily true? (a fraction inequality with a bottom of known sign).
- **2023_autumn_q1_01**: 0 < a, c < b < 0; which is necessarily positive? (signs first).
- **2020_autumn_q2_19**: a < 1, b < 1, M = ab; M can be any number (plug in negatives, not only 0 < a, b < 1).
- **2025_autumn_q1_16** (added in re-check): 0 < a, (21−3a)/(2a+1) < 0; which is necessarily true? (key: 7 < a). The bottom is known to be positive, so the sign of the fraction is the sign of the top: a fraction inequality that depends on the sign of the bottom.
- **2023_spring_q1_08** (added in re-check): x·y < |x·y| < y, necessarily true? (key: −1 < x < 0). The −1 < x < 0 range appears as the answer.

| Addition | Where | Class | Verdict | Evidence (real ids / count) |
|---|---|---|---|---|
| Cross-multiply: condition "both bottoms positive", plus the proof 55/88 vs 56/88 | `compare-fractions` slide 5 "Cross-multiply" | FIX | KEEP | wrong rule ("always works") fixed |
| "To decimals": "remember cross-multiplying?" | `compare-fractions` "To decimals" | FIX | KEEP | wording |
| Squaring only for positive numbers (−3 < 2 but 9 > 4) | "Roots? Square it" | FIX | KEEP | wrong rule fixed |
| Flipping reverses the order only for the same sign | "Flip them" | FIX | KEEP | wrong rule fixed |
| Recap slide rewritten (conditions, shortcut list, "signs first") | "Recap" | FIX | KEEP | follows the kept items below |
| Negatives slide, part 1: the 1/(−2) vs 1/3 trap and "move the minus to the top" | new slide "Negatives" (after "Cross-multiply") | FIX | KEEP | shows why the new cross-multiply condition is needed |
| Negatives slide, part 2: ordering two negative fractions (−2/3 > −3/4: compare without the minus, then reverse) + card row "Signs first" | "Negatives"; `mem-compare` row "Signs first" | CONTENT | KEEP | 2022_autumn_q1_08; sign reasoning: 2023_autumn_q1_01 (2) |
| Distance from 1 above 1 (7/6 = 1 + 1/6 vs 19/16 = 1 + 3/16) + card row extension | "Distance from 1"; card row "Distance from 1" | METHOD | KEEP | 2021_autumn_q2_16 (girls:boys 1+1/15 > 1+1/16 > 1+1/17); also the original course's q-089 uses fractions above 1 (1) |
| Add the same number to the top and the bottom (toward 1) + card row | new slide "Add to top and bottom"; card row "Add to top and bottom" | METHOD | KEEP | 2021_autumn_q2_16 (16/15 → 17/16 → 18/17 falls toward 1) (1) |
| Order of x, x², √x, 1/x by range (0<x<1, x>1, −1<x<0) + card table "x by range" | new slide "x, x² or 1/x?"; card table "x by range" | METHOD/CONTENT | KEEP | 2022_autumn_q1_08 (−1<x<0 / 0<a<1 rows), 2021_autumn_q1_07 (x>1 row); the −1<x<0 range also in 2023_spring_q1_08 (3) |
| Plug-in rules (legal values, avoid 0 and 1, try another kind of number) + "necessarily" vs "could be" + card row "Plug in numbers" + tip 3 | new slide "Which numbers?"; card row and tip | METHOD | KEEP | 2020_autumn_q2_19, 2020_autumn_q1_13, 2024_spring_q1_03; "can be": 2020_spring_q2_14 (many more "necessarily" items) |
| Decimals to know (1/2 ... 1/9) | "To decimals" (2 new lines); card table "Decimals to know" | METHOD | KEEP | 2023_spring_q2_12 (5/6 = 83⅓%), 2026_spring_q1_15 (3% of 33⅓), 2025_autumn_q2_03 (60/240 = 25%) |
| Method 4 "Pieces of 1/5" (mediant pulls the fraction toward 1/5) | `solve-q-099`, new slide "Method 4 · Pieces of 1/5" | METHOD | KEEP | 2021_autumn_q2_16 (16/31 → 17/33 → 18/35 adds a 1/2 piece and falls toward 1/2) (1) |
| Conditions added in solution videos ("all positive") | `solve-q-097` slide 3, `solve-q-099` slide 4 | FIX | KEEP | follows the fixed rules |
| Guided Q11: a<0<b, which is necessarily true (signs; flip and square traps) | `q-r26-t03-01` + video `solve-q-r26-t03-01` | CONTENT (question) | KEEP | 2023_autumn_q1_01, 2026_spring_q1_17, 2020_autumn_q2_19 (3) |
| Guided Q12: 0<a<b, largest of a/b, (a+1)/(b+1), (a+5)/(b+5), 5a/5b | `q-r26-t03-02` + video `solve-q-r26-t03-02` | METHOD (question) | KEEP | tests the kept "add to top and bottom" method: 2021_autumn_q2_16 (1) |
| Guided Q13: 0<x<1, the order of x², x, √x, 1/x | `q-r26-t03-03` + video `solve-q-r26-t03-03` | CONTENT (question) | KEEP | 2022_autumn_q1_08, 2021_autumn_q1_07 (2) |
| Solution-video sidebars Question 1–13; lesson sidebar with 14 labels | all t3 solution videos; `compare-fractions` | FIX | KEEP | mechanical |
| All 27 solutions rewritten in TeX; q-087 counterexamples | all t3 questions | FIX | KEEP | text |
| Stem fixes (÷ instead of ":", wording, cases) | q-092 (+ `solve-q-092` draw note), q-093, q-094, q-095, q-088, q-087 | FIX | KEEP | text |
| Spoken lines "…, so …" split | all t3 videos | FIX | KEEP | text |
| GRE-style items rewritten as NITE 4-choice items (benchmark ½, same top/bottom, cross-multiply) | `alg-extra-unit-t3-1-1`, `-t3-1-3`, `-t3-1-6` | FIX | KEEP | format fix; original methods |
| t3-1-4 replaced: largest of 3/√2, 4/√3, 5/√5, 6/√7 (squaring) | `alg-extra-unit-t3-1-4` | FIX | KEEP | replaces a near-duplicate of the lesson example; original method (like q-097) |
| t3-1-5 numeric solution | `alg-extra-unit-t3-1-5` | FIX | KEEP | text |
| t3-1-2 replaced: smallest of 21/19, 22/20, 23/21, 24/22 (add to top and bottom above 1) | `alg-extra-unit-t3-1-2` | METHOD (question) | KEEP | 2021_autumn_q2_16 (1) |
| t3-1-7 replaced: −1<x<0, largest of x, x², x³, 1/x | `alg-extra-unit-t3-1-7` | CONTENT (question) | KEEP | 2022_autumn_q1_08 (1) |
| Practice: 7/9 vs (7+x)/(9+x) | `q-r26-t03-04` | METHOD (question) | KEEP | 2021_autumn_q2_16 (1) |
| Practice: x>1, smallest of 1/√x, 1/x, √x, 1/x² | `q-r26-t03-05` | CONTENT (question) | KEEP | 2021_autumn_q1_07 (1) |
| Practice: a<b<0, necessarily true (flip with the same sign) | `q-r26-t03-06` | CONTENT (question) | KEEP | 2026_spring_q1_17, 2023_autumn_q1_01 (2) |
| Practice: largest of four negative fractions (minus in the bottom) | `q-r26-t03-07` | CONTENT (question) | KEEP | 2022_autumn_q1_08 (1). No real item compares numeric negative fractions |
| Practice: b<0<d and a/b<c/d, so ad>bc (the negative-bottom trap) | `q-r26-t03-08` | CONTENT (question) | KEEP (weakest) | 2026_spring_q1_17 (bottom of unknown sign), 2020_autumn_q1_13 (fraction inequality, "necessarily"), 2025_autumn_q1_16 (fraction inequality decided by the sign of the bottom) (3). The exact cross-multiply trap never appears |
| Practice order (operations first, then easy → hard) | `unit-t3-1` | FIX | KEEP | order |
| Card intro, conditions in rows (Cross-multiply, Same bottom / same top, Square them), new row "Flip them" (the rule was already taught), tips 1–2 | `mem-compare` | FIX | KEEP | follows the fixed rules |

## TO REMOVE

None. Every METHOD/CONTENT addition matches at least one real question.

Weak spots for the teacher (kept, but each rests on only one real question):
- "Add to top and bottom", "Pieces of 1/5", "Distance from 1 above 1" and the practice items `q-r26-t03-02`, `q-r26-t03-04` and `alg-extra-unit-t3-1-2` rest only on 2021_autumn_q2_16.
- `q-r26-t03-07` and `alg-extra-unit-t3-1-7` rest only on 2022_autumn_q1_08.
- `q-r26-t03-08`: the negative-bottom cross-multiply trap itself never appears. The support is indirect (2026_spring_q1_17, 2020_autumn_q1_13, 2025_autumn_q1_16).

Teacher's rule check (original questions must be taught): the kept methods also serve original Topic 3 questions: squaring (q-097, `alg-extra-unit-t3-1-4` original), flipping (q-099), 0<x<1 order (original `alg-extra-unit-t3-1-5`), signs with negative values in a fraction (q-088: a > 1, (a+x)/(a−x) with x = −2/5, −4/5), distance from 1 (q-084 below 1, q-089 above 1), add to top and bottom / pieces (q-099: 3/16, 4/21, 5/26). This only strengthens the KEEP verdicts; nothing moves.

Side note (out of scope; it is about original content): none of the 760 real questions is a bare "which of these numeric fractions is the largest". On the real exam, comparing fractions appears inside chart questions (2020_autumn_q1_18, 2022_autumn_q2_19, 2023_spring_q1_11, 2024_winter_q2_08) and word problems (2021_autumn_q2_16).

## ORIGINAL ITEMS REMOVED BY FIXERS

Checked against the pre-patch course (`git show 0205ceb^:content/full-course/topics/t3.json` and
`0205ceb^:studio-build/course18.json`). No original question, video, slide or card row was deleted. All 17 original
practice items are still in `unit-t3-1` (the fixers' `practice_order` lists every one). The lesson kept all 11 original
slides (4 new ones were inserted), and every original row of `mem-compare` is still there (edited). But three original
questions were **replaced in place**: same id, new stem, choices and key, so the original question is gone:

| Id | Original question (pre-patch) | Now | Fixers' reason |
|---|---|---|---|
| `alg-extra-unit-t3-1-2` | Which is largest? 15/16, 4/5, 7/8, 10/11 (key 15/16; "one minus the reciprocal") | smallest of 21/19, 22/20, 23/21, 24/22 | near-duplicate of q-084 |
| `alg-extra-unit-t3-1-4` | Which is greater: 3/√10 or 2/√5? (GRE format: first / second / equal / neither is real; key: first) | largest of 3/√2, 4/√3, 5/√5, 6/√7 | same as the lesson's "Roots? Square it" example |
| `alg-extra-unit-t3-1-7` | For c > 1, which value of x makes (c+x)/(c−x) smallest among −1, 0, 1/2, 1? (key −1) | −1<x<0, largest of x, x², x³, 1/x | near-duplicate of q-088 |

These were rewritten into NITE 4-choice format. The original comparison is still inside the new question, so there is
nothing to restore unless the teacher wants the exact original wording:
- `alg-extra-unit-t3-1-1`: was "Which is greater: 3/7 or 5/9?" (first / equal / depends / second). Now "which is greater than 1/2" with 3/7 and 5/9 among the choices.
- `alg-extra-unit-t3-1-3`: was "For positive x, which is greater: 7/(x+2) or 7/(x+5)?". Now "largest of four" with both among the choices.
- `alg-extra-unit-t3-1-6`: was "Which is smaller: 3/5 or 4/6?". Now "smallest of 3/5, 2/3, 5/8, 7/11" (2/3 = 4/6).

Original spoken text replaced (not removed). Every item below states the wrong rule "cross-multiplying always works", so
restoring it would put back an error. It is listed only for completeness:
- `compare-fractions` slide 5: "Big numbers? Don't panic — it still works. It's secretly a common denominator, comparing the tops." and "One method that always works beats five you half-remember."
- `compare-fractions` slide 6: "But remember what always works?"
- `compare-fractions` slide 11 "Recap": the items "Cross-multiply: always works — products above the numerators" and "Also: benchmark ½ · match tops or bottoms · distance from 1 · square roots away", the draw note "Circle 'always works'", and the spoken lines ("It always works, it's simple, and it eats everything", "Even with letters and scary expressions — cross-multiply…").
- `mem-compare` intro "Cross-multiplication always works — the rest are shortcuts." and the Cross-multiply row "always (…)".
