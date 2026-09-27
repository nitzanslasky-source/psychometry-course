# Audit: Topic 6 (Equations: Fundamentals). Additions vs. the real NITE exam

Sources: `math_patches/t06_CHANGES.md`, `math_patches/t06.py`, and the original course as students saw it before the patch (`student_review/t6.md`). Evidence comes from `real_exam/quant_real.md` (re-checked 2026-09-27 against the regenerated full-text file; the earlier copy cut stems after "<"). I read the `equations` group (33 questions) and the `algebraic_expressions` group (32) in full, and grepped the whole file for "no value", "no solution", "infinit", "satisf", "how many values", x/y and products.

Context: the original course already taught these things, so they are not new content:
- "If an answer makes a denominator zero, throw it out" (LE slide 5).
- Testing the choices (the q-171 video, Method 2).
- Cross-multiplying (mentioned in the q-171 video).
- "Ask what they want / x+y may be enough" (SY slide 6).
- Subtracting with brackets (SY slide 4).
- xy and x/y systems (practice q-153).
- A parameter that gives no solution (t6-1-7).
- "How many solutions" (q-156).

Lessons: LE = `linear-equations` ("Equations — Fundamentals"). SY = `systems` ("Systems of Equations"). Slide numbers are after the patch.

## Table

| Addition | Where | Class | Verdict | Evidence (real ids / count) |
|---|---|---|---|---|
| "can solve it" now says "usually", plus a note on no/infinite solutions | SY slide 2; solve-q-164 slide 2 | FIX | KEEP | n/a |
| ":4" and ":3" become "÷4" and "÷3" in draw notes | LE slide 2; solve-q-164 slide 3 | FIX | KEEP | n/a |
| q-156 choices changed (Exactly one/two/Infinitely many/None) | q-156 | FIX | KEEP | n/a |
| q-171 distractors 31/21 become −1/5 | q-171 | FIX | KEEP | n/a |
| All systems stacked with `cases`, all math in TeX, solutions rewritten, q-153 "x > 0 and y > 0" | all 45 remaining original questions; SY slides 3–5 | FIX | KEEP | n/a |
| Cross-multiply slide (3/(x+1) = 2/(x−1), condition "only one fraction = one fraction") | LE slide 6 "Cross-multiply" | METHOD (extends a mention in the original q-171 video) | KEEP | 2026_spring_q2_08 (after cancelling, a fraction = 2), 2020_autumn_q2_01 (x/3 = (x+8)/4), 2022_winter_q2_16 |
| Forbidden-answer slide (x/(x−2) = 2/(x−2): the only root is forbidden, so "no solution") | LE slide 7 "Forbidden answer" | CONTENT built from two ORIGINAL rules (LE slide 4 "No solution" + LE slide 5 "an answer that makes a denominator zero is out"); original q-171 has the forbidden value x = 2 as a choice | KEEP (changed from REMOVE on re-check) | Real questions where a stated restriction rules out the only root, so the answer is "not possible": 2019_winter_q2_15 (s+t = s−t forces t = 0, but s, t > 0; correct answer), 2020_spring_q2_08 (x³ = y³ forces x = y, but x ≠ y; correct answer). Restriction removes a root: 2023_autumn_q2_03 (x ≠ 0), 2024_winter_q2_06 (b ≠ 1 kills a factor, a = 5), 2020_spring_q1_15 (x ≠ 0). Total 5. None of them uses a denominator as the source of the restriction; the logic is the same. Also demonstrates the original rule tested by original q-171. |
| Minus before a fraction (numerator in brackets, −2(x−3) = −2x+6) | LE slide 9 "Minus before a fraction" | METHOD (sign technique for the LCD) | KEEP | 2025_autumn_q2_17 (×6 through x/2 + xy/3 − y/2), 2020_autumn_q2_16 and 2025_winter_q1_08 (fraction minus fraction with multi-term numerators) |
| Test the choices (6/(x−1) = x−2, skip forbidden values) | LE slide 11 "Test the choices" | METHOD | KEEP | 2022_autumn_q1_13, 2025_winter_q2_03, 2025_autumn_q1_01 |
| LE recap rebuilt (7 lines) and sidebar | LE slide 12; LE sidebar | FIX (follows the slides) | KEEP, but adjust | No change needed now that slide 7 and Q5 stay. |
| Add and subtract: x+y=10, x−y=4; x = sum/2, y = difference/2 | SY slide 5 "Add and subtract" | METHOD | KEEP | 2025_winter_q2_05 (x+y = −2, x−y = ±2), 2019_winter_q2_02 (add the equations), 2022_autumn_q2_01 (subtract) |
| Get x+y (or x−y) directly by adding or subtracting | SY slide 8 "Get x + y directly" | METHOD | KEEP | 2023_spring_q1_04 (exactly this: x+2y=5, 2x+y=13, x+y=?), 2024_spring_q1_18, 2023_winter_q2_15 |
| Multiply or divide equations (xy=12, x/y=3) | SY slide 9 "Multiply equations" | METHOD (the type was already in the original as q-153) | KEEP | 2021_spring_q1_07 (2ab=cde, a/d=3, b/e=6 gives c = 2·3·6 = 36). Only 1 real id. |
| SY recap "which method when?" and sidebar | SY slide 10; SY sidebar | FIX (follows the slides) | KEEP | n/a |
| Guided Q4: (x+2)/3 − (x−4)/6 = x/2, with a 2-method video | q-r26-t06-01; solve-q-r26-t06-01 | METHOD practice (minus before a fraction, test the choices) | KEEP | 2025_autumn_q2_17, 2022_autumn_q1_13 |
| Guided Q5: (2x+1)/(x−2) = (x+3)/(x−2), "no solution" | q-r26-t06-02; solve-q-r26-t06-02 | CONTENT (forbidden-answer type; see slide 7) | KEEP (changed from REMOVE) | 2019_winter_q2_15, 2020_spring_q2_08 (only root excluded by a stated restriction → "not possible"); original q-171 (forbidden choice x = 2) |
| Guided Q6: 5x+3y=41, 3x+5y=39, x+y=? | q-r26-t06-03; solve-q-r26-t06-03 | METHOD (add the equations) | KEEP | 2023_spring_q1_04, 2024_spring_q1_18, 2020_autumn_q1_01 |
| Guided Q7: xy=20, x/y=5, x−y=? | q-r26-t06-04; solve-q-r26-t06-04 | METHOD (multiply the equations; type already in the original q-153) | KEEP | 2021_spring_q1_07 |
| p05: 5/(x+2) = 3/(x−2), cross-multiply | q-r26-t06-05 | METHOD practice | KEEP | 2026_spring_q2_08, 2020_autumn_q2_01 |
| p06: x/2 − (x−6)/4 = 3, minus before a fraction | q-r26-t06-06 | METHOD practice | KEEP | 2025_autumn_q2_17 |
| p07: which number solves 12/x = x+1 (test the choices) | q-r26-t06-07 | METHOD practice | KEEP | 2022_autumn_q1_13, 2025_winter_q2_03 |
| p08: a such that 3(x+a) = 3x+12 has infinitely many solutions | q-r26-t06-08 | CONTENT (parameter for identity/contradiction; the original had t6-1-7 of this type) | KEEP | 2021_spring_q1_08 (pick definitions so that "no x satisfies", i.e. 2x+5 = 2x+7), 2024_winter_q1_08 (identity: "a can be any number") |
| p09: x/(x−3) = 2 + 3/(x−3), root forbidden, "no value" | q-r26-t06-09 | CONTENT (forbidden-answer type; see slide 7) | KEEP (changed from REMOVE) | 2019_winter_q2_15, 2020_spring_q2_08, 2023_autumn_q2_03 |
| p10: hard LCD with a minus and a −1 | q-r26-t06-10 | METHOD practice | KEEP | 2025_autumn_q2_17, 2021_spring_q2_06 |
| p11: x+y=15, x−y=−3, y=? (half-difference) | q-r26-t06-11 | METHOD practice | KEEP | 2025_winter_q2_05, 2019_winter_q2_02 |
| p12: 3x+2y=20, x+y=7, 2x+y=? (subtract to get it directly) | q-r26-t06-12 | METHOD practice | KEEP | 2023_spring_q1_04, 2023_winter_q2_15, 2021_spring_q2_06 |
| p13: x(y+2)=24, x(y−1)=12, y=? (divide or subtract) | q-r26-t06-13 | METHOD practice | KEEP | 2021_spring_q1_07 (combining product equations). Weak, only 1 id. |
| p14: (x+y)/(x−y) = 3, so x/y = ? | q-r26-t06-14 | METHOD practice (clear the fraction, find a relation between the variables) | KEEP | 2021_spring_q1_03 ((a+c)/b = 2, relation), 2019_winter_q1_15, 2022_winter_q2_16 |
| p15: how many solutions does (x−1)/(x−1) = 1 have ("every number except 1") | q-r26-t06-15 | CONTENT (solution set cut by a restriction; the forbidden-answer idea) | REMOVE (confirmed on re-check) | 0. No real question has the answer "every number except k" (an identity cut by a restriction). The phrase appears only as a wrong choice in 2020_autumn_q2_19 (correct: "any number, including 1"). "How many values" questions exist (2021_autumn_q1_13, 2020_autumn_q2_03, 2020_autumn_q2_13) and identities exist (2024_winter_q1_08), but none combines them with a restriction. |
| p16: 3x−2y=5, so 6x−4y+1 = ? (with a "cannot be determined" choice) | q-r26-t06-16 | METHOD practice (get the combination directly) | KEEP | 2020_autumn_q1_01 (2x+2y=340, so 3x+3y=?), 2021_spring_q2_06 |
| p17: xy=6, yz=10, xz=15, so xyz = ? | q-r26-t06-17 | METHOD practice (multiply the equations) | UNSURE (confirmed on re-check) | The method has only 1 real id (2021_spring_q1_07). The full-text file has no question with three pairwise products (searched xyz, yz, xz, abc). It could be a legitimate stretch item or an off-exam type. |
| Card: Solving one equation (9 rows plus 3 tips) | mem-r26-t06-single | Summary of original rules plus the kept methods | KEEP | Every row maps to an original rule or a kept method. The "x in the denominator … an answer that breaks it is out" row is the original rule. |
| Card: Systems, which method? (6 rows plus 2 tips) | mem-r26-t06-systems | Summary of the kept methods | KEEP | See slides 5, 8 and 9 above. |

Not audited: the 13 practice removals (t6-4-1/2/3/5, t6-2-1/2/5/6/7, q-141, t6-1-1/2/3). They are removals, not additions.

## TO REMOVE
- Question `q-r26-t06-15` (practice, section `unit-t6-1`). Remove it from the `unit-t6-1` practice order.
- Nothing else. On re-check with the full-text file, the forbidden-answer items (LE slide 7, `q-r26-t06-02` with `solve-q-r26-t06-02`, `q-r26-t06-09`) are KEEP. See the table.

## UNSURE
- `q-r26-t06-17` (xy=6, yz=10, xz=15, so xyz = ?). The multiply-equations method has only one real id (2021_spring_q1_07), and the three-product type does not appear on the exam.

## ORIGINAL ITEMS REMOVED BY FIXERS
Source: `math_patches/t06.py` section 2 (`M.unplace`), set_slide/edit_lines calls, compared with `student_review/t6.md`.

Questions unplaced (removed from practice; restore them by placing them back in their sections):
- `unit-t6-4` (single-equation practice): `alg-extra-unit-t6-4-1` (2x−5=1), `alg-extra-unit-t6-4-2` (3(x−2)=6), `alg-extra-unit-t6-4-3` ((x+7)/4 = 12/4), `alg-extra-unit-t6-4-5` (x/2 + 9 = 25/2).
- `unit-t6-2` (systems practice): `alg-extra-unit-t6-2-1` (2x+3y=19, 3x+2y=16, x), `alg-extra-unit-t6-2-2` (…=24/21, y), `alg-extra-unit-t6-2-5` (…=39/36, 2x+y), `alg-extra-unit-t6-2-6` (…=44/41, xy), `alg-extra-unit-t6-2-7` (…=49/46, x²+y²).
- `unit-t6-1` (mixed practice): `q-141` ((x+3)/4 = 5), `alg-extra-unit-t6-1-1` (5x+7=52), `alg-extra-unit-t6-1-2` (x+y=13, x−y=3, x), `alg-extra-unit-t6-1-3` (2x+3y=31, 3x+2y=29, x+y).
Total: 13 questions.

Original slide text replaced (no original slide was deleted; slides were only inserted):
- `linear-equations` Recap (was slide 8, now 12): the 5 original board lines were rewritten into 7 lines. All 5 original ideas are still there, in new wording; the closing line "Next: a question with two fractions" became "Next: three questions".
- `systems` slide 2 "Two equations": "as many equations as unknowns — and you can solve it" became "…and USUALLY you can solve it" plus a line on no/endless solutions (FIX).
- `systems` slide 4 "Elimination": the line "Same sign instead of opposite signs? Then subtract — and keep the whole second equation in brackets." was replaced by "…Then subtract. The next slide shows how." (the bracket point moved to new slide 5).
- `systems` Recap (was slide 7, now 10): the 3 original lines ("Substitution: isolate, then plug in"; "Elimination: add or subtract to cancel a letter"; "Multiply WHOLE equations to match coefficients") were replaced by a 5-line "which method when?" list. The substitution and elimination lines survive only reworded.
- Sidebars of `linear-equations` and `systems` replaced (they list the original slides plus the new ones).
- Draw notes ":4" (`linear-equations` slide 2) and ":3" (`solve-q-164` slide 3) changed to "÷".

Original question content replaced (FIX, keep the fix unless the teacher prefers the original):
- `q-156`: original choices "One / Two / Seven / The equation has no solution" replaced by "Exactly one / Exactly two / Infinitely many / None".
- `q-171`: original distractors "31" and "21" replaced by "−1" and "5".
- All 45 remaining original questions: stems, choices and solutions rewritten to TeX with new worked solutions (text only, same question).
