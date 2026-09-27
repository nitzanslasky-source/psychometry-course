# Audit: Topic 7 (Equations) additions vs. the real exam

Sources: `math_patches/t07_CHANGES.md`, `math_patches/t07.py`, `real_exam/quant_real.md` (groups `equations` 33 q, `algebraic_expressions` 32 q read in full; keyword search across all 760 questions for x², squares, 1/x, "satisfy", "infinitely", parameter systems, fraction equations, products/ratios of equations).

**Re-check 2026-09-27 against the regenerated `quant_real.md` (full text, no "<" truncation).** Searched all 760 questions for "no solution", "infinit", "no value", "satisf", "for which/what value", "denominator", "≠"/"\ne", "undefined", every x² expression, and "= 0". Results: still 0 systems with no/infinitely many solutions or a parameter k (the only "Infinitely many"/"Infinite" choices are 2025_winter_q1_17, a circle angle, and 2020_autumn_q2_13, values of |x − y|); still 0 fraction-equals-0 questions (all ~25 "≠" hits are given restrictions, e.g. 2023_winter_q2_06 |x| ≠ 1 is a simplification, 2024_winter_q2_06 b ≠ 1 is a common-factor question); still 0 trinomial equations that must be solved. One trinomial equation appears only inside a choice: 2021_spring_q1_08 choice 4, 2x² + 3 = 15 − 2x (it has a solution, x = 2; the question is answered by choice 3 without solving it).
**Teacher's rule applied (original content stays):** original course questions that need "product c, sum b" factoring: q-127 (x² + 11x + 24, Topic 5), q-expression-extra-05 (x² + 13x + 40), alg-extra-unit-t4-1-3 (x² + 8x + 15), alg-extra-expression-self-3 (x² + 10x + 24), alg-extra-unit-t5-1-3 (x² + 12x + 35). All five are expression factoring in Topics 4-5; no original Topic 7 question needs it. No original question anywhere is a fraction = 0, and no original question is a two-unknown system with no/infinitely many solutions (the originals q-205, alg-extra-unit-t7-5-7, alg-extra-unit-t6-1-7 are one-variable "ax = b has no solution").
Changes from this re-check: rows 20 and 48 go from REMOVE to KEEP (method needed by original questions). All other REMOVE verdicts stand.

Key real-exam facts used below:
- Two-variable linear systems appear often (2020_autumn_q1_01, 2022_autumn_q2_01, 2023_spring_q1_04, 2024_spring_q1_18, 2019_winter_q2_02, 2025_autumn_q2_17), but **none** asks whether a system has no solution / infinitely many solutions, and **none** has a parameter k in the coefficients (0 questions). 2021_spring_q1_08 (no x with #(x) = $(x)) is a one-variable defined-operation question, not a system.
- Quadratic equations: **no real question requires factoring a trinomial with two distinct roots (product c, sum b)**. The only trinomial is 2023_autumn_q2_04 (m^{2x} = m·m^{x²} → x² − 2x + 1 = 0), a perfect square. Other "quadratics" are pure squares or cancel to linear: 2020_autumn_q2_03 (4x² − 64 = 0, x = ±4), 2021_autumn_q1_13, 2025_winter_q2_03, 2022_autumn_q1_14, 2022_autumn_q1_13.
- a² = b² → a = ±b: 2021_autumn_q1_13, 2020_spring_q2_08, 2024_spring_q2_04 (3 questions).
- Fraction equal to 0 with an extraneous root: **0 questions**. (2026_spring_q2_08 is a fraction = 2 where cancelling is allowed; the extraneous value never arises.)
- (x ± 1/x)² middle term: 2024_autumn_q2_11 ((b/a + a/b)² = b²/a² + 2 + a²/b²).
- Multiplying/dividing equations with products or ratios: 2021_spring_q1_07.

| # | Addition | Where (video id / slide / question ids) | Class | Verdict | Evidence (real question ids / count) |
|---|---|---|---|---|---|
| 1 | "Brainwave two" false statement corrected | Q16 solution video, Method 3 | FIX | KEEP | - |
| 2 | q-214 solution rewritten, choice wording "or (or both)" | q-214 | FIX | KEEP | - |
| 3 | Q20 video: why "cannot be determined" is wrong; "Last question in this set" | Q20 solution video | FIX | KEEP | - |
| 4 | Title slide script rewritten | `equation-strategy` slide 1 | FIX | KEEP | - |
| 5 | Habit "or check x = 0 separately" before dividing by x | `equation-strategy` slide 2 (added lines) | METHOD | KEEP | 2020_autumn_q2_03 (choice "among them 0"), 2023_autumn_q2_03, 2024_winter_q2_06 |
| 6 | Worked mini-examples on slides "One eq, two unknowns", "Build the expression", "Break it apart" | `equation-strategy` slides 5, 6, 9 | FIX (clarifies existing slides) | KEEP | slide 6 example = 2023_spring_q1_04 |
| 7 | New slide "Which operation?" checklist (mirror coefficients; letter missing → cancel; products/ratios → multiply/divide; multiply one equation first; else plug in) | `equation-strategy` new slide 7 "Which operation?" | METHOD | KEEP | 2023_spring_q1_04, 2019_winter_q2_02, 2021_spring_q1_07, 2025_autumn_q2_17 |
| 8 | "Hidden formula" extended: (x − y)², "know two of x ± y, x² + y², xy → get the third" | `equation-strategy` slide 8 "Hidden formula" | METHOD | KEEP | 2025_winter_q2_05, 2021_autumn_q2_09, 2020_winter_q1_15 |
| 9 | New slide "Plug in numbers" (4 rules) | `equation-strategy` new slide 10 "Plug in numbers" | METHOD | KEEP | 2019_winter_q1_15, 2023_winter_q2_15, 2021_autumn_q2_03 |
| 10 | New slide "Try the choices" | `equation-strategy` new slide 11 "Try the choices" | METHOD | KEEP | 2022_autumn_q1_13, 2025_winter_q2_03, 2026_spring_q2_08 |
| 11 | Recap updated | `equation-strategy` slide 12 "Recap" | FIX | KEEP | - |
| 12 | New lesson slide "Multiply or divide" (equations) | `r26-t07-more-tools` slide "Multiply or divide" | METHOD | KEEP | 2021_spring_q1_07 (multiply a/d · b/e), 2024_spring_q1_18 (multiplied equation) |
| 13 | New lesson slide "x + 1/x" (square it, middle term 2; x − 1/x → −2) | `r26-t07-more-tools` slide "x + 1/x" | METHOD (formula shortcut) | KEEP | 2024_autumn_q2_11 (1 question, exact rule) |
| 14 | New lesson slide "Solutions of a system" (no solution / infinitely many, parameter k) | `r26-t07-more-tools` slide "Solutions of a system" (+ title-slide line and recap line about it) | CONTENT | REMOVE (re-checked) | 0 real two-unknown systems with no/infinitely many solutions or a parameter k. The one real "no solution" question, 2021_spring_q1_08 (2x + 5 = 2x + 7), is one-variable and is already covered by the originals q-205 / alg-extra-unit-t7-5-7 |
| 15 | Guided Q21: divide two product equations (x²y, xy² → x/y) + solution video | q-r26-t07-01, `solve-q-r26-t07-01` | practice of #12 | KEEP | 2021_spring_q1_07 |
| 16 | Guided Q22: x + 1/x = 3 → x² + 1/x² + solution video | q-r26-t07-02, `solve-q-r26-t07-02` | practice of #13 | KEEP | 2024_autumn_q2_11 |
| 17 | Guided Q23: k for which a system has no solution + solution video | q-r26-t07-03, `solve-q-r26-t07-03` | tests #14 | REMOVE | 0 real questions |
| 18 | New section "Quadratic equations" + lesson video | section `r26-t07-quadratic`, video `r26-t07-quadratic` | container | KEEP (holds kept slides 19, 21-24) | see rows below |
| 19 | Slide "What it looks like": standard form, everything to one side = 0, divide out common number | `r26-t07-quadratic` slide "What it looks like" | CONTENT | KEEP | 2020_autumn_q2_03 (4x² − 64 = 0), 2023_autumn_q2_04 (→ x² − 2x + 1 = 0) |
| 20 | Slide "Factor": two numbers with product c and sum b | `r26-t07-quadratic` slide "Factor" | METHOD | KEEP (changed from REMOVE on re-check) | Real exam: 0 trinomials to factor (2021_spring_q1_08 choice 4 only). Kept under the teacher's rule: the method is needed for 5 original questions: q-127, q-expression-extra-05, alg-extra-unit-t4-1-3, alg-extra-expression-self-3, alg-extra-unit-t5-1-3. Note: the same method is taught in `r26-t04-trinomials` (Topic 4); if that lesson stays, this slide is a second teaching of it, applied to equations |
| 21 | Slide "Two solutions": zero-product on the factors, the sign flips | `r26-t07-quadratic` slide "Two solutions" | CONTENT | KEEP | 2020_autumn_q2_03 (4(x − 4)(x + 4) = 0; the correct choice is "among them −4") |
| 22 | Slide "Special cases": no number term, no x term (±), perfect square → one solution, x² = −4 → none | `r26-t07-quadratic` slide "Special cases" | CONTENT | KEEP | 2020_autumn_q2_03, 2023_autumn_q2_04 (perfect square), 2020_winter_q2_08 (a = 4 forces b² < 0) |
| 23 | Slide "The trap: a² = b² → a = b or a = −b" | `r26-t07-quadratic` slide "The trap: a² = b²" | CONTENT | KEEP | 2021_autumn_q1_13, 2020_spring_q2_08, 2024_spring_q2_04 (3) |
| 24 | Slide "Try the choices" (quadratics; "which could be x") | `r26-t07-quadratic` slide "Try the choices" | METHOD | KEEP | 2023_autumn_q2_04, 2025_winter_q2_03, 2022_autumn_q1_13 |
| 25 | Slide "Fraction = 0": numerator 0, denominator ≠ 0, throw out extraneous root | `r26-t07-quadratic` slide "Fraction = 0" | CONTENT | REMOVE | 0 real questions |
| 26 | Recap of quadratic lesson | `r26-t07-quadratic` slide "Recap" | FIX | KEEP (without the line for #25) | - |
| 27 | Guided Q24: x² − 2x = 15 (trinomial factoring) + solution video | q-r26-t07-04, `solve-q-r26-t07-04` | CONTENT (question type: solve a trinomial equation with two distinct roots) | REMOVE (re-checked) | 0 real questions of this type; also 0 original questions of this type (the originals factor expressions, they do not solve equations) |
| 28 | Guided Q25: (x + 1)² = (x − 3)² + solution video | q-r26-t07-05, `solve-q-r26-t07-05` | tests #23 | KEEP | 2021_autumn_q1_13 (same form) |
| 29 | Guided Q26: (x² − 7x + 12)/(x − 3) = 0, extraneous root + solution video | q-r26-t07-06, `solve-q-r26-t07-06` | tests #20 + #25 | REMOVE | 0 real questions |
| 30 | Practice: solutions of x² − 6x + 8 = 0 | q-r26-t07-07 | CONTENT (same type as #27) | REMOVE (re-checked) | 0 real, 0 original questions of this type |
| 31 | Practice: 2x² = 8x, number of solutions (divide-by-x trap) | q-r26-t07-08 | original-course rule | KEEP | 2020_autumn_q2_03, 2023_autumn_q2_03 |
| 32 | Practice: x² = y² → |x| = |y| necessarily | q-r26-t07-09 | tests #23 | KEEP | 2020_spring_q2_08, 2024_spring_q2_04 |
| 33 | Practice: (x² − 9)/(x − 3) = 0 | q-r26-t07-10 | tests #25 | REMOVE | 0 |
| 34 | Practice: x² − 10x + 25 = 0, how many values | q-r26-t07-11 | tests #22 (perfect square) | KEEP | 2023_autumn_q2_04 (1); count format as 2021_autumn_q1_13 |
| 35 | Practice: x > 0, (2x − 1)² = (x + 4)² | q-r26-t07-12 | tests #23 | KEEP | 2021_autumn_q1_13 |
| 36 | Practice: x − 1/x = 4 → x² + 1/x² | q-r26-t07-13 | tests #13 | KEEP | 2024_autumn_q2_11 |
| 37 | Practice: x² + 1/x² = 14 → x + 1/x | q-r26-t07-14 | tests #13 | KEEP | 2024_autumn_q2_11 |
| 38 | Practice: xy = 12, yz = 6 → x/z | q-r26-t07-15 | tests #12 | KEEP | 2021_spring_q1_07 |
| 39 | Practice: three products → xyz | q-r26-t07-16 | tests #12 | KEEP | 2021_spring_q1_07 |
| 40 | Practice: k for infinitely many solutions | q-r26-t07-17 | tests #14 | REMOVE | 0 |
| 41 | Practice: system with infinitely many solutions → a + b | q-r26-t07-18 | tests #14 | REMOVE | 0 |
| 42 | Practice: x = 2y + 3 → 4y (plug in) | q-r26-t07-19 | tests #9 | KEEP | 2021_autumn_q2_03, 2019_winter_q1_15 |
| 43 | Practice: x + y = k, x − y = 2 → xy (plug in / hidden formula) | q-r26-t07-20 | tests #8, #9 | KEEP | 2025_winter_q2_05 |
| 44 | Practice: 3/4 x + 1/5 x = 38 (estimate) | q-r26-t07-21 | linear equation with fractions; METHOD estimate | KEEP | 2022_winter_q1_13, 2020_autumn_q2_01 |
| 45 | Card "Traps" rows: x³ = x²y; (x − 6)² = 16; a² = b²; "Cannot be determined" | `mem-r26-t07-equations`, table "Traps" rows 1, 2, 3, 5 | summary of kept rules | KEEP | 2023_autumn_q2_03, 2020_autumn_q2_03, 2021_autumn_q1_13, 2024_autumn_q1_14 |
| 46 | Card "Traps" row "A fraction = 0" | `mem-r26-t07-equations`, table "Traps" row 4 | tests #25 | REMOVE | 0 |
| 47 | Card table "Which operation?" (7 rows) | `mem-r26-t07-equations`, table "Which operation?" | METHOD | KEEP | as rows 7, 8, 9, 10, 12, 13 |
| 48 | Card table "Quadratic equations" (4-step factoring procedure) | `mem-r26-t07-equations`, table "Quadratic equations" | summary of kept #19-#21 | KEEP (changed from REMOVE on re-check) | follows #20 (original questions q-127, q-expression-extra-05, etc.); steps 1 and 4 also match 2020_autumn_q2_03 |
| 49 | Card tip 1: x² = 9 two solutions, (x − 5)² = 0 one, x² = −4 none | `mem-r26-t07-equations` tips[0] | tests #22 | KEEP | 2020_autumn_q2_03, 2023_autumn_q2_04, 2020_winter_q2_08 |
| 50 | Card tip 2: left sides equal → no solution / infinitely many | `mem-r26-t07-equations` tips[1] | tests #14 | REMOVE | 0 |
| 51 | Card tip 3: "necessarily true" counterexample | `mem-r26-t07-equations` tips[2] | METHOD | KEEP | 2021_spring_q1_03, 2022_winter_q2_16 |
| 52 | Text / TeX rewrites of 40 questions, cases stacking, colons removed, "0 < m, n" etc., "so" wording, formula names in Q11/Q15/Q18/Q19 videos | all T7 questions and solution videos | FIX | KEEP | - |
| 53 | q-203 choice 4 replaced by −n (m² = n² trap) | q-203 | FIX | KEEP | trap backed by 2020_spring_q2_08 |
| 54 | 7 clone items removed; section `unit-t7-1` renamed "Retry set (same types as Questions 1-6)"; practice reordered | `alg-extra-unit-t7-1-1`..`7`, `unit-t7-1`, `unit-t7-5` | FIX | KEEP | - |

## TO REMOVE

Videos / slides
- Slide "Solutions of a system" in video `r26-t07-more-tools` (and its sidebar entry "Solutions of a system"); in the same video delete the title-slide words "and systems with no solution — or infinitely many" and the recap line "Same left side: different right → none; same → infinitely many"; recap "Three questions now" becomes two.
- Slide "Fraction = 0" in video `r26-t07-quadratic` (and sidebar entry "Fraction = 0"); recap line "Fraction: denominator ≠ 0".
- Solution videos `solve-q-r26-t07-03`, `solve-q-r26-t07-04`, `solve-q-r26-t07-06`.

Questions
- Guided: q-r26-t07-03, q-r26-t07-04, q-r26-t07-06 (quadratic lesson recap "Three questions now" becomes one question: Q25).
- Practice: q-r26-t07-07, q-r26-t07-10, q-r26-t07-17, q-r26-t07-18 (also drop them from the `unit-t7-5` practice order).

Card `mem-r26-t07-equations`
- Table "Traps", row 4: "A fraction = 0 | Numerator = 0 and denominator ≠ 0 — throw out bad solutions".
- Tip 2: "Two equations: make the left sides equal. Different right sides → no solution. Same right sides → infinitely many."

## Counts
- KEEP 43 (of which FIX 10), REMOVE 11, UNSURE 0 (54 rows). (Before the re-check: KEEP 41, REMOVE 13; rows 20 and 48 changed.)

## ORIGINAL ITEMS REMOVED BY FIXERS

Everything below existed in the course before the patch (`student_review/t7.md`, `course18.json`) and was removed or replaced by `math_patches/t07.py`. Under the teacher's rule these can be restored.

Questions removed
- `alg-extra-unit-t7-1-1` Solve 7x + 9 = 86.
- `alg-extra-unit-t7-1-2` x + y = 17, x − y = 3. Find x.
- `alg-extra-unit-t7-1-3` 2x + 3y = 41, 3x + 2y = 39. Find x + y.
- `alg-extra-unit-t7-1-4` x + y = 16, xy = 63. Find x² + y².
- `alg-extra-unit-t7-1-5` Solve (x − 7)/(x + 9) = 1/2.
- `alg-extra-unit-t7-1-6` x(x − 7) = 0, sum of all real solutions.
- `alg-extra-unit-t7-1-7` For what value of k does (7 − k)x = 9 have no solution?
  (All 7 were unplaced from section `unit-t7-1` as "clones" of alg-extra-unit-t7-5-1..7; same types, different numbers.)

Question content replaced
- `q-203` choice 4: original "m² − 2" replaced by "−n" (key unchanged, choice 1).
- All 40 existing Topic 7 questions (q-172 … q-217, alg-extra-unit-t7-5-1..7): stems, choices and solutions rewritten in new TeX/wording (keys unchanged). The math is the same; listed so the originals can be compared if wanted.

Section
- `unit-t7-1` title "Additional source-bank variants" renamed to "Retry set (same types as Questions 1–6)".
- `unit-t7-5` practice order replaced (original order: q-198 … q-217, then alg-extra-unit-t7-5-1..7).

Lesson video `equation-strategy` (original 9 slides; slides rewritten, original lines dropped)
- Sidebar: original list (9 entries) replaced by the new 11-entry list.
- Slide 1 "Solving Equations Smarter": script rewritten (original 4 lines kept, one line added).
- Slide 5 "One equation, two unknowns": rewritten; original lines kept, example added.
- Slide 6 "Build the expression": original board line "Add, subtract — or divide — the equations", the draw note "Underline Add, subtract and divide", and the lines "Adding the equations, subtracting them, sometimes dividing them — look for the short route straight to what they want." and "How do you know which one? Practice. You'll start to recognise the patterns." were removed.
- Slide 7 (now 8) "Hidden formula": original board (only (x − y)² = x² + y² − 2xy) and the lines "See x minus y, x squared plus y squared, and x times y together? That's this formula." and "Find the right formula, plug in what you know, and isolate what they ask for." were replaced.
- Slide 8 (now 9) "Break it apart": the draw note "Draw brackets grouping the pieces into the small equations" and the line "Once you know the trick, these become simple. You'll see it in question seven." were replaced.
- Slide 9 (now 12) "Recap": board line "Asked for an expression? Build it directly" replaced by "…Use the checklist"; "the next seven questions" line reworded.

Solution videos (original lines replaced)
- `solve-q-179` slide 4: "Brainwave two: each letter is bigger than the next…" (math error for negatives; a FIX, do not restore as is).
- `solve-q-187` slide 2: "First short multiplication formula."
- `solve-q-178` slides 1-2: "A word problem hiding a short multiplication formula." and "That second one is the third short multiplication formula."
- `solve-q-182` slides 2-3: "Expand the left side with the first formula." and "Shortcut: the right side IS a short multiplication formula."
- `solve-q-181` slide 2: "…that's a short multiplication formula."
- `solve-q-183` slide 1: "Last question on equations."
- Draw notes with ":" for division: `solve-q-184` "22 : 11/15 = …", `solve-q-180` "m/n = m : 1/m = …" and "m/n = 2 : 1/2 = 4".
- All 20 solution videos `solve-q-178` … `solve-q-197` and `equation-strategy`: global spelling / "so" wording fixes.

No original card rows existed in Topic 7 (the card `mem-r26-t07-equations` is new). No original slide or video was deleted outright.
