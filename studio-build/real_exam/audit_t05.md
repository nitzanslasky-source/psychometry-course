# Audit: Topic 5 (Expressions): were the additions justified by the real exam?

**Re-check (2026-09-27) against the regenerated, untruncated `quant_real.md`:** the real-exam counts are unchanged. There are
0 numeric trinomials to factor and 0 exact products near a round number. The only letter trinomial on the exam, 2023_autumn_q2_04
(x² − 2x + 1 = 0), is a perfect square. Applying the teacher's rule that original questions must be taught changed 3 verdicts
from REMOVE to KEEP: the "Sum and product" slide, the "Round numbers" slide and the card row "Near a round number". The
pre-patch source is `student_review/t5.md`.

Sources: `math_patches/t05_CHANGES.md`, `math_patches/t05.py`, `real_exam/quant_real.md` (760 questions). I read the whole
`algebraic_expressions` group (32 questions) and the `inequalities_absolute` group. I grepped all 760 questions for trinomials
(`x^2 ± bx ± c`), numeric products near round numbers, numeric differences of squares, "given a block" stems, and sign
questions.

Key search results:
- **Trinomial factoring with sum and product** (x² + bx + c with numeric b, c): **0 of 760**. No real stem or choice contains a
  numeric trinomial. The only quadratics are identity-type questions (squares, sum × difference, (a−1)(a²+a+1)).
- **Exact product near a round number** (99·41, 999·25, 98·102): **0**. The only numeric product is 2020_spring_q2_11,
  "closest to 304 × 329", which asks for an estimate (choices 10× apart). The rounding trick is not needed there.
- **Numeric difference of squares, already written as a² − b²**: 1 (2021_spring_q2_17, 17.5² − 7.5²).
- **Given a block / given a relation → value of another expression**: 2020_spring_q2_01, 2023_winter_q1_02, 2021_autumn_q2_09,
  2020_winter_q1_15 (4).
- **Simplify a rational or letter expression, letters in the choices** (plug-in or split): 2020_autumn_q2_16, 2021_autumn_q1_15,
  2020_winter_q2_13, 2023_winter_q2_06, 2025_winter_q1_08, 2023_spring_q1_13, 2024_autumn_q2_11 (7+).
- **Sign questions ("which is necessarily positive/negative")**: 2023_autumn_q1_01, 2021_autumn_q2_15 (2), and |x|/x:
  2024_winter_q1_05.

## Table

| Addition | Where | Class | Verdict | Evidence |
|---|---|---|---|---|
| Q1 video: false "answer = slot" tip removed; ÷ notation | solve-q-121 | FIX | KEEP | - |
| Q9 video: Method 1 real counterexample; Method 2 without geometry | solve-q-129 | FIX | KEEP | - |
| "Opposite brackets": one-line proof b − a = −(a − b) | expression-strategy slide (Opposite brackets) | FIX | KEEP | - |
| Q8 choices reordered "x > 0 ; 3" | q-128 | FIX | KEEP | - |
| Q11, Q12 choice 3, extra-09: removed negative exponents / a⁰ (used before taught) | q-131, solve-q-131, q-132, solve-q-132, q-expression-extra-09 | FIX | KEEP | - |
| Q7 line "You know sum and product from Topic 4…" | solve-q-127 | FIX | KEEP | - |
| TeX in all stems/choices/solutions, extra-07 choice, stem wording, "Given:" lines, Q5/Q10 title slides, "so" wording | whole topic | FIX | KEEP | - |
| Q14 video estimate anchored on 63·500 | solve-q-134 slide 2 | FIX | KEEP | - |
| Recap board and sidebar updated | expression-strategy (Recap, sidebar) | FIX | KEEP | - |
| 12 near-duplicate practice items removed; practice reordered | extra-02/03/08, self-1..7, t5-1-6, t5-1-7 | FIX | KEEP (the removal stands) | - |
| New slide "Splitting a fraction": (a+b)/c ✓, c/(a+b) ✗ | expression-strategy, slide 4 "Splitting a fraction" | METHOD | KEEP | 2021_autumn_q1_15 (choices 2 and 4 are exactly the split/false split), 2020_winter_q2_13, 2023_spring_q1_13 |
| New slide "Choosing numbers" (plug-in rules, ties) | expression-strategy, slide 9 "Choosing numbers" | METHOD | KEEP | 2020_autumn_q2_16, 2025_winter_q1_08, 2023_winter_q2_06 |
| Slide 7 line: "if they give the block's value, put the number in" | expression-strategy slide 7 (repeated bracket) | METHOD | KEEP | 2020_spring_q2_01, 2023_winter_q1_02, 2021_autumn_q2_09 |
| New lesson video "Exam Shortcuts": title slide | r26-t05-shortcuts, slide "Exam Shortcuts" | METHOD (container) | KEEP (as is; only the guided-question count changes) | see "Given a block", "Sum and product", "Round numbers" |
| Shortcuts slide "Sum and product" (trinomial factoring reminder, x²+9x+20) | r26-t05-shortcuts, slide "Sum and product" | METHOD (needed by original questions) | KEEP (changed from REMOVE) | Real exam: 0 numeric trinomials. But original items test the method: q-127 (guided Q7, x²+11x+24), q-expression-extra-05 (x²+13x+40), alg-extra-unit-t5-1-3 (x²+12x+35), and alg-extra-expression-self-3 (x²+10x+24, removed by the fixers). The original course never taught it; the original Q7 video said "We don't know how to factor this yet". The slide points to Topic 4's `r26-t04-trinomials`, so that lesson must stay too |
| Shortcuts slide "Round numbers" (99·41 = 4,100 − 41; 96·104 = 100² − 4²) | r26-t05-shortcuts, slide "Round numbers" | METHOD (needed by original questions) | KEEP (changed from REMOVE) | Real exam: 0 exact products near a round number; 2020_spring_q2_11 is an estimate only. But original items need exactly this trick: q-expression-extra-19 (99·41; the original solution says "Use 99 = 100 − 1"), alg-extra-unit-t5-1-5 (95·105), and alg-extra-expression-self-5 (96×104, removed by the fixers). The original lesson did not teach it |
| Shortcuts slide "Given a block" (x+y=5 → 3x+3y+1) | r26-t05-shortcuts, slide "Given a block" | METHOD | KEEP | 2020_spring_q2_01, 2023_winter_q1_02, 2020_winter_q1_15 |
| Shortcuts slide "Recap" | r26-t05-shortcuts, slide "Recap" | METHOD | KEEP (all tool lines stay; "Four guided questions next" becomes "Two") | as above |
| Q15 guided: (x²−2x−15)/(x−5) − x, sum and product | q-r26-t05-01 + video solve-q-r26-t05-01 | CONTENT (added question type: trinomial inside a fraction) | REMOVE (re-checked, unchanged) | Real exam: 0 numeric trinomials. The method stays for the original items (see "Sum and product"), and those items already give the practice. The plug-in-tie method it also shows is kept in Q18 |
| Q16 guided: 98·102 − 99·101 | q-r26-t05-02 + video solve-q-r26-t05-02 | added question type (round numbers) | REMOVE (re-checked, unchanged) | Real exam: 0 of this type. The method stays for the original extra-19 and t5-1-5, which already practise it |
| Q17 guided: a − b = 3 → (b−a)² + 2a − 2b | q-r26-t05-03 + video solve-q-r26-t05-03 | METHOD (given block, plug-in legal numbers) | KEEP | 2020_spring_q2_01, 2023_winter_q1_02, 2021_autumn_q2_09 |
| Q18 guided: (a²b+ab²)/(ab), plug-in tie trap | q-r26-t05-04 + video solve-q-r26-t05-04 | METHOD (plug-in, ties) | KEEP | 2020_autumn_q2_16, 2025_winter_q1_08, 2023_winter_q2_06 |
| Card: rule row "(a+b)/c = a/c + b/c ✓" | mem-r26-t05-expressions, Rules row 1 | METHOD | KEEP | 2021_autumn_q1_15 |
| Card: rule row "c/(a+b) ≠ c/a + c/b ✗" | mem-r26-t05-expressions, Rules row 2 | METHOD | KEEP | 2021_autumn_q1_15 (choice 4 trap), 2020_winter_q2_13 |
| Card: rule row "\|x\|/x = ±1" | mem-r26-t05-expressions, Rules row 3 | card row for original Q8 content | KEEP | 2024_winter_q1_05 |
| Card: rule row "Near a round number: 99·41" | mem-r26-t05-expressions, Rules row 4 | METHOD (needed by original questions) | KEEP (changed from REMOVE) | q-expression-extra-19, alg-extra-unit-t5-1-5 (see "Round numbers") |
| Card: rule row "Given a block? Put in its value" | mem-r26-t05-expressions, Rules row 5 | METHOD | KEEP | 2020_spring_q2_01, 2023_winter_q1_02 |
| Card: table "Pick your method" (6 rows) | mem-r26-t05-expressions, table 2 | METHOD | KEEP | 2020_autumn_q2_16 (plug in), 2024_autumn_q2_11 / 2019_winter_q1_02 (square, sum × difference), 2020_spring_q2_11 (estimate). Row 3 also names "x²+bx+c": there is no real-exam evidence, but original items q-127, extra-05 and t5-1-3 need it |
| Card: tips (inside-out, no cancelling, plug-in numbers, ties) | mem-r26-t05-expressions, tips | METHOD | KEEP | 2020_winter_q2_13, 2025_winter_q1_08 |
| Practice: given block x − 2y = 4 | q-r26-t05-05 | METHOD (given block) | KEEP | 2020_spring_q2_01, 2021_autumn_q2_09 |
| Practice: a/b = 3 → (a−b)/(a+b) | q-r26-t05-06 | METHOD (given relation, plug-in) | KEEP | 2023_winter_q1_02 (x = 2y → (x−y)²) |
| Practice: x − 1/x = 3 → x² + 1/x² | q-r26-t05-07 | METHOD (square the given block) | KEEP | 2021_autumn_q2_09, 2020_winter_q1_15 (identity on a given block), 2024_autumn_q2_11 ((b/a + a/b)², middle term 2) |
| Practice: 999·25 | q-r26-t05-08 | added question type (round numbers) | REMOVE (re-checked, unchanged) | Real exam: 0. The original extra-19 and t5-1-5 already practise the method |
| Practice: (101² − 99²)/4 | q-r26-t05-09 | METHOD (sum × difference on numbers) | KEEP | 2021_spring_q2_17 (1) |
| Practice: (x²+4x−12)/(x−2), sum and product | q-r26-t05-10 | added question type (trinomial inside a fraction) | REMOVE (re-checked, unchanged) | Real exam: 0. The original extra-05, t5-1-3 and q-127 already practise the method |
| Practice: (x³+x²)/x, plug-in tie | q-r26-t05-11 | METHOD (plug-in, ties) | KEEP | 2020_autumn_q2_16, 2023_winter_q2_06 |
| Practice: (a²−b²)/(a−b) − 2b, plug-in tie | q-r26-t05-12 | METHOD (plug-in, ties; sum × difference) | KEEP | 2025_winter_q1_08, 2020_winter_q1_15 |
| Practice: which equals 6/(x+y) (split trap) | q-r26-t05-13 | METHOD (split rule) | KEEP | 2021_autumn_q1_15 |
| Practice: x < 0 < y, which is necessarily positive | q-r26-t05-14 | CONTENT (sign question) | KEEP | 2023_autumn_q1_01, 2021_autumn_q2_15 (2) |
| Practice: 1/(1 + 1/x) nested fraction | q-r26-t05-15 | METHOD (inside out, plug-in tie) | KEEP | 2020_winter_q2_13, 2019_spring_q1_10, 2021_autumn_q1_15 |
| Practice: (a²+2a)/a − (a²−4)/(a−2) = constant | q-r26-t05-16 | question type (expression with a constant value, the type of original Q12) | KEEP | 2020_spring_q2_01 (answer is a constant), 2025_winter_q1_08 |

## TO REMOVE (after re-check)

Counts: KEEP 27, REMOVE 4, UNSURE 0. The 10 FIX rows are kept by rule and are not counted.

- Question `q-r26-t05-01` (guided Q15) and its solution video `solve-q-r26-t05-01`.
- Question `q-r26-t05-02` (guided Q16) and its solution video `solve-q-r26-t05-02`.
- Practice question `q-r26-t05-08` (999·25).
- Practice question `q-r26-t05-10` ((x²+4x−12)/(x−2)).

No longer removed (changed to KEEP under the original-content rule): the slides "Sum and product" and "Round numbers" in
`r26-t05-shortcuts` (with their sidebar entries, title-slide mentions and Recap lines), and the card row
`mem-r26-t05-expressions` "Near a round number".

Mechanical follow-ups:
- `r26-t05-shortcuts` Recap: change "Four guided questions next" to "Two guided questions next".
- Q17 and Q18 then become Questions 15 and 16. Update their title slides ("Question seventeen/eighteen") and the solution
  videos' sidebar `sb`, which then has 2 entries.
- The Q17 and Q18 videos do not refer to Q15 or Q16.
- The "Sum and product" slide points back to Topic 4's `r26-t04-trinomials`. Keep that lesson, or reword this slide to stand alone.

## ORIGINAL ITEMS REMOVED BY FIXERS

The pre-patch text is in `student_review/t5.md`. The removed question ids match `real_exam/original_removed.json`.

Questions unplaced (removed from practice) by `practice()` in `t05.py`:
- `q-expression-extra-02` (For a ≠ b, 4 − (a−b)/(b−a))
- `q-expression-extra-03` ((u+v)(t−5)+(u+v)(t+5))
- `q-expression-extra-08` ([(p−q)−(q−p)]/(p−q))
- `alg-extra-expression-self-1` (Simplify 4x+6y−2x−3y)
- `alg-extra-expression-self-2` (Simplify 4(x+4)−3(x+1))
- `alg-extra-expression-self-3` (Factor x²+10x+24, a trinomial item)
- `alg-extra-expression-self-4` ((x²−16)/(x−4))
- `alg-extra-expression-self-5` (Evaluate 96×104, a round-number item)
- `alg-extra-expression-self-6` ((u+v)(w−4)+(u+v)(w+4))
- `alg-extra-expression-self-7` ((4x²+24x)/(4x))
- `alg-extra-unit-t5-1-6` ((u+v)(w−5)+(u+v)(w+5))
- `alg-extra-unit-t5-1-7` ((5x²+35x)/(5x))

Original question content replaced (beyond TeX or wording):
- `q-131` (guided Q11): the stem (x⁻² + 4x²/x⁴)·(1/5)·(5/x⁻²) was replaced by the 1/x² form. The choices and key (5) are unchanged.
- `q-132` (guided Q12): choice 3, a⁰ + (−1)ᵃ, was replaced by (a+1)² − (a−1)². The key (choice 4) is unchanged.
- `q-expression-extra-09`: the stem (x⁻² + 2/x²)·x², key 3 (choice 3), was replaced by (3/x² − x/x³)·x²/2, key 1 (choice 1).
- `q-129` (guided Q9): the stem was rewritten. Maya's condition changed from "(A ≠ −B, B ≠ 0)" to "for every B ≠ 0 and A ≠ −B", and "necessarily true" became "true".
- `q-128` (guided Q8): the choice order changed from "value ; condition" to "condition ; value". The key is unchanged.

Original slides whose whole script was replaced (`set_slide(..., script=...)`):
- `expression-strategy` Recap (originally slide 9, now slide 11). The sidebar was also rewritten, with 2 entries added.
- `solve-q-129` slide 3 (Method 2; the original used the geometry expression (180 + α)/2).
- `solve-q-131` slides 2 and 3 (the original used negative exponents).
- `solve-q-132` slide 2 (the original went through a⁰ + (−1)ᵃ).

Original spoken or drawn lines removed or replaced inside kept slides:
- `solve-q-135` slide 2: the "side tip about the exam" line ("When an answer equals a choice NUMBER … it sits in slot three") was deleted; the fixers found it false. Two draw lines changed ":" to "÷".
- `solve-q-127` slides 1 and 2: "We don't know how to factor this yet — so let the answers do the work." and "We haven't learned to factor this kind of expression. No problem — the choices will help us. Open them up." were replaced.
- `solve-q-129` slide 2: the draw line with "✗" and the line "…That's not what she started with." were replaced.
- `solve-q-131` slide 1: "Negative powers — and a plug-in that makes them disappear." was replaced.
- `solve-q-134` slide 2: four estimate lines (including "≈ 30,000 : 60 = 500") were replaced.
- `expression-strategy` slide 5 (Opposite brackets): "…But honestly? Trust it. It's always negative one." was replaced.
- `so_fixes`: one sentence each in `solve-q-136` slide 2, `solve-q-137` slide 3, `solve-q-126` slide 3 and `solve-q-134` slide 3 was split at "so" (wording only).

No original video or memory card was removed. Topic 5 had no original card.

Out of scope, a note for the Topic 4 audit: Topic 4's "Factoring Trinomials" lesson has no numeric-trinomial question on the real
exam, but it is still needed, because original Topic 5 items (q-127, extra-05, t5-1-3, self-3) test the method.
