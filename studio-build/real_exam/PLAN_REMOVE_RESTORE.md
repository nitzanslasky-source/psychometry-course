# Plan: what to remove and what to restore after the 2026-09 math patches

This plan applies the teacher's final rule to the 38 audits (`real_exam/audit_t01.md` … `audit_t38.md`). Where an auditor's
verdict differs from the rule, the rule wins. Each change from an audit is marked **[changed from audit]** with the reason.
Borderline cases were re-checked against `quant_real.md` and `course18.json`. Nothing has been edited yet; this is the
plan only.

## The rule, as applied
1. **Original content stays.** Everything in `course18.json` / `base-v18.html` must be taught.
2. **An added item stays** if (a) its content or question type is on the real exam, OR (b) its content or question type
   is already in the original course. This covers extra practice of an original question type, and methods needed to
   solve original questions. **Otherwise the item is removed.** Nothing is shortened: an item is either kept or
   removed. A slide that mixes kept and removed content loses only the lines about the removed content.
3. **Error fixes stay** (wrong rules, false statements, typos, notation, figures, giveaways). But when a fixer deleted a
   TRUE original statement, it is restored.
4. **Original questions, slides and card content that were deleted or replaced are restored**, with the same text
   clean-up as the rest of the course:
   - math in TeX
   - no ":" for division
   - several givens stacked in `cases`
   - numbers shown in the solutions

   If an original was changed only because it used a later topic, the original comes back and moves to just after the
   topic that teaches it. Its content is not rewritten.
5. **Test used to decide "original type".** An original question (or original slide or card) must test the same skill.
   A combination counts when an original question already combines the same skills. The same topic heading alone does
   not count.

## Global instructions (apply everywhere)
- **Removing a guided question** also removes its `solve-` video. Then:
  - renumber the guided questions after it (title slides "Question N", sidebars `sb`, and "in Question N" references)
  - fix every "N guided questions" or "N questions next" line on section titles and recap slides
- **Removing a slide** also removes its sidebar entry and its recap line. Lesson title slides that list the removed
  idea drop those words.
- **Removing a practice question** also removes it from its section's practice order (`M.practice_order`).
- **Restored questions** go back into their original section, at their original position in the `course18.json` flow.
  The practice order stays easy to hard, so insert them at the matching difficulty.
- **Replaced in place, and the new version is a kept type.** Restore the original under its own id. The fixer's new
  version may stay as an extra question under a new id (`q-r26-tNN-<next>`). This is marked "new version → new id".
  If the new version is only the same item reformatted, it is dropped.
- **Distractor and choice changes** that were not error fixes (a wrong choice swapped for another wrong choice): the
  original choices are restored. They are listed per topic under "RESTORE, choices". Pure rewording with the same
  meaning and the same key is clean-up and stays as it is.
- **Reworded lines and card rows with the same content** stay as they are. Only content that was lost comes back.

## Totals

**REMOVE**

| Item | Count |
|---|---|
| Added questions removed | 73 |
| Their solution videos removed | 21 |
| Whole lesson videos removed | 1 (`r26-t29-geometric`, 5 slides) |
| Whole slides removed | 27 (22 in kept videos + the 5 slides of `r26-t29-geometric`) |
| Slides that only lose lines | 11 |
| Card rows, tips and cells removed or edited | 33 |
| Whole cards removed | 1 (`mem-r26-t29-geometric`) |

**RESTORE**

| Item | Count |
|---|---|
| Deleted original questions put back (all of `original_removed.json`) | 113 |
| Original questions replaced in place, put back | 26 |
| Restored originals moved to a later topic | 7: six of the 26 (q-018 → T2; q-131, q-132, q-expression-extra-09 → T8; wp26-p10, wp27-p10 → T33) plus the deleted alg-extra-unit-t18-3-4 → T28 |
| Original questions with choices restored | 7: q-156, q-171, q-203, q-317, q-323, alg-extra-unit-t17-3-4, alg-extra-exponent-extra-6 (T8, also in the 26) |
| Original slides put back | 10 |
| Groups of original lines or card content put back | about 45 |

**KEPT although the auditor said REMOVE or UNSURE**

About 75 items. Most are extra practice of a type the original course already tests, or content the original course
already teaches.

## Overview for the teacher: which added topics and question types are removed

**Algebra (T1–T20)**
- T7 Equations: systems with no solution / infinitely many solutions (parameter k).
- T8 Exponents: counting zeros at the end of a number; ordering huge powers with different bases (2⁴⁰ vs 3³⁰).
- T9 Roots: roots of decimals (√0.09, √0.0016).
- T10 Exponent techniques:
  - comparing powers by equal exponents (2³⁰ vs 3²⁰)
  - exponential inequalities with a base between 0 and 1
  - "aˣ = bˣ ⇒ x = 0"
- T11: the card row "compare powers" and 2 practice items (decimal root, huge powers).
- T13 Absolute value: writing a range as |x − m| < r (the midpoint trick).
- T14 Primes:
  - zeros at the end (of n! or products)
  - perfect cubes (smallest k)
  - finding a number from its GCD and LCM
- T15 Remainders: the "reverse" question ("100 ÷ n leaves 4, how many n?").
- T19 New operation: the integer part [x].
- T4: the "twin identity" (a+b)² + (a−b)² (two lines only).

**Word problems (T21–T29)**
- T21: finding a term from a formula for the sum of the first n terms.
- T23 Percent: percentage points / percent change of a rate.
- T27 Motion: two trains passing each other (with lengths); meeting twice.
- T28 Counting:
  - groups with no names (÷2)
  - road maps
  - the zero-digit trap
- T29 Probability:
  - **geometric probability (the whole lesson and card)**
  - "unknown count" (how many balls to add)
  - the "AND smaller / OR bigger" size check

**Geometry (T30–T38)**
- T30: the C-shape bend (360°); the units-digit tip.
- T32:
  - the concave "arrow" rule
  - the trapezoid midsegment
  - the trapezoid "butterfly" (equal side triangles)
- T33: a quadrilateral around a circle (AB + CD = BC + AD); two circles meeting at two points (distance range).
- T34: "could this be an angle of a regular polygon?"
- T35: water rising when an object sinks (displacement); the shortest path on a cube's surface.
- T37: "which quadrant?" questions; negative slope.
- T38: the shortest path on a cube; the angle-bisector ratio shortcut.

**Kept, because the original course already has the type (the auditor had said remove)**
- factoring trinomials, and quadratic equations solved by factoring
- fraction = 0, and "every number except 1"
- sums of equal powers; common factor of powers; decimal squares
- roots of different order (original q-245)
- domain of a root
- "no solution" absolute-value questions; sums of distances
- ones digit of powers; days of the week as a cycle
- "to be sure" / worst case (original wp21-p14)
- piecewise operations solved backwards
- "how many digits can a product have" (original q-521)
- objects into boxes (original codes with repetition)
- "exactly one"; changing a ratio
- painted cube; solids of revolution; bricks in a box; liters (original geo-119 teaches millilitres)
- acute or obtuse from the sides (original geo38-core-p25)
- plane sections of a solid; circle vs square with equal perimeters; a point inside a circle from an angle
- distance–time graphs (real chart set 2019_spring_q1_16–20)
- percent change of area/volume; map area; a cone filled to part of its height
- "n from an angle"; counting diagonals; the octagon area
- line equations and intercepts
- "which marked point could be √x"
- all the T31 and T33 extra triangle and circle items the auditors left as UNSURE

**Restored everywhere:** all 113 deleted original questions, the replaced originals, and the true lines the fixers had
deleted. The teacher named three of these:
- T30 "a right angle almost always has a dot in the square"
- T33 the SSS proof of equal chords
- T32 the "Completions" approach slide (checked: it is correct)

---

# Per topic

## T1 Algebraic fundamentals
**Summary:** nothing is removed. Three deleted drill questions come back, and q-018 goes back to its fraction form in T2.

**REMOVE:** none.

**RESTORE**
- Questions, all into `unit-t1-1` (Mixed practice) except where noted:
  - q-003 (84 − 36)
  - q-004 (95 + (−38))
  - q-033 (63 − 27): this one goes into `intro-add` (flow-0010)
- q-018, original "200 : 6 = ?", choices 33⅙ / **33⅓** / 33⅔ / 33⅚, with its original explanation:
  - write it as "200 ÷ 6 = ?"
  - it used fractions (T2), so move it into the T2 practice `unit-t2-1`
  - new version → new id: the quotient-and-remainder version stays in T1 as `q-r26-t01-25` (remainders are original T1
    content and alg-extra-unit-t15-3-7)

**Kept (checked):** every T1 addition, including the consecutive even/odd items. Their type is original: T16 q-458,
q-468, alg-extra-unit-t16-3-7.

## T2 Fractions
**Summary:** nothing is removed. Three deleted questions and one replaced question come back.

**REMOVE:** none.

**RESTORE**
- q-041, q-042, q-045 → `unit-t2-1`.
- alg-extra-unit-t2-1-2: the original "Evaluate 5/6 − 1/4" (choices 7/12, 1/2, 2/3, 1/3; key 7/12). New version → new id:
  "7/10 − 1/4" as `q-r26-t02-25`.
- Receives q-018 from T1 (see T1).

## T3 Comparing fractions
**Summary:** nothing is removed. Six extra items that the fixers rewrote come back in their original form. The old
"cross-multiplying always works" text is not restored, because it is a wrong rule.

**REMOVE:** none.

**RESTORE** (the original stem, choices and key in each case, in TeX):
- alg-extra-unit-t3-1-1: "Which is greater: 3/7 or 5/9?"
- alg-extra-unit-t3-1-2: "Which is largest? 15/16, 4/5, 7/8, 10/11"
- alg-extra-unit-t3-1-3: "For positive x, which is greater: 7/(x+2) or 7/(x+5)?"
- alg-extra-unit-t3-1-4: "Which is greater: 3/√10 or 2/√5?"
- alg-extra-unit-t3-1-6: "Which is smaller: 3/5 or 4/6?"
- alg-extra-unit-t3-1-7: "For c > 1, which x makes (c+x)/(c−x) smallest?"

New versions:
- The new versions of -2, -4 and -7 test kept methods, so they become new ids `q-r26-t03-09`, `-10` and `-11`:
  - smallest of 21/19 … 24/22
  - largest of 3/√2 … 6/√7
  - −1 < x < 0 order
- The new versions of -1, -3 and -6 are the same comparisons in another format, so they are dropped.

**No action:** the "cross-multiply always works" lines (`compare-fractions` slides 5, 6, 11; `mem-compare` intro and row)
stay corrected. They state a wrong rule.

## T4 Expressions: fundamentals
**Summary:** the only thing removed is the "twin identity" (a+b)² + (a−b)² = 2a² + 2b². The trinomial questions stay.

**REMOVE**
- `solve-q-120` slide 2: the lines "Write '(a + b)² + (a − b)² = 2a² + 2b²'" and "Bonus: with a PLUS between the
  squares…".
- q-120 explanation: the last line "Twin identity: …".
- Evidence: 0 real questions and 0 original questions use it.

**KEEP [changed from audit]:** the auditor had these as REMOVE. They are trinomial factoring, which the original course
tests in 5 questions: alg-extra-unit-t4-1-3, q-127, q-expression-extra-05, alg-extra-unit-t5-1-3,
alg-extra-expression-self-3.
- q-r26-t04-05 + `solve-q-r26-t04-05`
- q-r26-t04-06 + `solve-q-r26-t04-06` (this is trinomial + reduce; the original has the reduce type in
  q-expression-extra-15 and alg-extra-unit-t4-1-4)
- q-r26-t04-11, -12, -13

The guided numbering does not change.

**RESTORE**
- q-108, q-109, q-111, q-117 → `unit-t4-1`.
- The original `expression-basics` "Recap" content: the three formulas (a+b)², (a−b)², (a−b)(a+b), and the line
  "Circle the three formulas… Two big takeaways: taking out a common factor, and the three formulas. Now try a
  question". Put it on the final recap of the lesson pair, the `r26-t04-formulas` Recap, which now closes the original
  slides 9–12.
- `mem-formulas`:
  - row "(a−b)(a+b) = a² − b²": restore the original example "48·52 = 50² − 2²" (98·102 is on the new "Number
    shortcuts" slide)
  - intro: restore "Use them forwards to expand and backwards to factor."

## T5 Expressions: strategy
**Summary:** nothing added is removed. The 12 deleted practice items come back. Q11, Q12 and extra-09 go back to their
original negative-exponent form and move to T8.

**REMOVE:** none.

**KEEP [changed from audit]:**
- q-r26-t05-01 + `solve-q-r26-t05-01` and q-r26-t05-10: a trinomial inside a fraction. The original type is
  q-expression-extra-15, (x² − 10x + 25)/(x − 5), and alg-extra-expression-self-4.
- q-r26-t05-02 + `solve-q-r26-t05-02` and q-r26-t05-08: round numbers. The original type is q-expression-extra-19
  (99·41), alg-extra-unit-t5-1-5 and alg-extra-expression-self-5.
- The `r26-t05-shortcuts` Recap keeps "Four guided questions next".

**RESTORE**
- Into the T5 practice:
  - alg-extra-expression-self-1 … self-7 (7 questions)
  - alg-extra-unit-t5-1-6, alg-extra-unit-t5-1-7
  - q-expression-extra-02, -03, -08
- These three used negative exponents or a⁰ before Topic 8 taught them. Restore the originals and **move them to T8**,
  after the `exponents` lesson:
  - q-131 (guided): the original stem (x⁻² + 4x²/x⁴)·(1/5)·(5/x⁻²), and the original `solve-q-131` slides 1–3
  - q-132 (guided): the original choice 3, a⁰ + (−1)ᵃ, and the original `solve-q-132` slide 2
  - q-expression-extra-09: the original stem (x⁻² + 2/x²)·x², key choice 3
- In T5, renumber the guided questions after Q10. In T8, they become guided questions after the kept T8 ones.
- `expression-strategy` slide 5 (Opposite brackets): restore the line "…But honestly? Trust it. It's always negative
  one." after the new proof line. The statement is true.

**No action:**
- q-128 choice order, the q-129 rewrite and the `solve-q-129` Method 2 (it used a geometry expression, which is taught
  later): these stay fixed.
- `solve-q-135` "answer = slot" tip: false, stays deleted.
- `solve-q-127` "We don't know how to factor this yet": no longer true, because the trinomial lesson stays.

## T6 Equations: fundamentals
**Summary:** nothing is removed. The 13 deleted practice items come back, with the original distractors of q-156 and
q-171 and one recap line.

**REMOVE:** none.

**KEEP [changed from audit]:**
- q-r26-t06-15, "how many solutions does (x−1)/(x−1) = 1 have". The type is original: q-156 is a "how many solutions"
  question, and "x in the denominator, an answer that breaks it is out" is original `linear-equations` slide 5.
- q-r26-t06-17 (xy, yz, xz → xyz), which the auditor left UNSURE. It is the same type that T7 keeps (q-r26-t07-16),
  multiplying equations, and the original has q-153. Real evidence: 2021_spring_q1_07.

**RESTORE**
- `unit-t6-4`: alg-extra-unit-t6-4-1, -4-2, -4-3, -4-5.
- `unit-t6-2`: alg-extra-unit-t6-2-1, -2-2, -2-5, -2-6, -2-7.
- `unit-t6-1`: q-141, alg-extra-unit-t6-1-1, -1-2, -1-3.
- Choices:
  - q-156: the original choices One / Two / Seven / The equation has no solution (key One)
  - q-171: the original distractors 31 and 21
- `systems` Recap: restore the original line "Multiply WHOLE equations to match coefficients". It is lost from the new
  list.

## T7 Equations
**Summary:** removed: two-unknown systems with no solution or infinitely many solutions, and parameter-k systems. The
quadratic-equation items (trinomials, fraction = 0) stay.

**REMOVE**
- Video `r26-t07-more-tools`:
  - slide "Solutions of a system" and its sidebar entry
  - title-slide words "and systems with no solution — or infinitely many"
  - recap line "Same left side: different right → none; same → infinitely many"
  - recap "Three questions now" → "Two questions now"
- Guided q-r26-t07-03 + `solve-q-r26-t07-03`. Renumber the guided questions after it.
- Practice q-r26-t07-17, q-r26-t07-18 (drop them from the `unit-t7-5` order).
- `mem-r26-t07-equations` tip 2: "Two equations: make the left sides equal. Different right sides → no solution…".
- Evidence: 0 real and 0 original two-unknown no-solution systems. The original only has one-variable "ax = b has no
  solution", which stays.

**KEEP [changed from audit]:**
- Items:
  - the `r26-t07-quadratic` slide "Fraction = 0" and its recap line
  - q-r26-t07-06 + `solve-q-r26-t07-06`
  - q-r26-t07-10
  - card row "A fraction = 0"
- Why they stay: these are equations with x in the denominator, where an answer that makes the bottom 0 is thrown
  out. That rule is taught and tested in the original (`linear-equations` slide 5, q-171).
- Also kept: q-r26-t07-04 + `solve-q-r26-t07-04` and q-r26-t07-07 (trinomial equations). The type "solve a quadratic
  equation, or count its solutions" is original: q-173, q-192, alg-extra-unit-t7-1-6. It is also real: 2020_autumn_q2_03,
  2023_autumn_q2_04.
- The quadratic recap keeps "Three questions now".

**RESTORE**
- alg-extra-unit-t7-1-1 … -1-7 (7 questions) → section `unit-t7-1`. Also restore that section's original title,
  "Additional source-bank variants".
- q-203: the original choice 4, "m² − 2".
- `equation-strategy`:
  - slide 6 "Build the expression": restore the board line "Add, subtract — or divide — the equations" and the lines
    "Adding the equations, subtracting them, sometimes dividing them — look for the short route…" and "How do you know
    which one? Practice. You'll start to recognise the patterns." Keep the new example.
  - slide 8 "Hidden formula": restore "See x minus y, x squared plus y squared, and x times y together? That's this
    formula." and "Find the right formula, plug in what you know, and isolate what they ask for."
  - Recap: restore the board line "Asked for an expression? Build it directly".

**No action:** "Brainwave two" (math error), "Last question on equations" (no longer true) and the formula-name lines stay
fixed.

## T8 Exponent laws
**Summary:** removed: counting zeros at the end of a number, and ordering huge powers with different bases (2⁴⁰ vs 3³⁰).
Sums of equal powers and decimal squares stay.

**REMOVE**
- Video `r26-t08-traps`: slide "Counting zeros", its sidebar label, and the words about zeros on the title slide.
- Guided q-r26-t08-03 + `solve-q-r26-t08-03` (largest of 2⁴⁰, 3³⁰, 5²⁰, 10¹⁰).
- Guided q-r26-t08-04 + `solve-q-r26-t08-04` (zeros of 2⁷·5⁴).
- Renumber the guided questions.
- Practice q-r26-t08-13 (2⁵⁰, 3³⁰, 5²⁰) and q-r26-t08-16 (digits of 4⁵·5⁸).
- Card `powers`, table "Exam traps": row "Zeros at the end".
- Evidence: 0 real and 0 original questions of these types. The original only compares same-base powers (2¹⁰ vs 4⁴),
  and the kept slide "Compare powers" covers that.

**KEEP [changed from audit]:**
- q-r26-t08-01 + `solve-q-r26-t08-01` (2ⁿ+2ⁿ+2ⁿ+2ⁿ), q-r26-t08-06, -07 and -08: sums of equal powers. The original type
  is T11 q-293.
- q-r26-t08-09 (0.3²) and q-r26-t08-10 (0.2³·10⁴): decimal powers. The original type is T2 q-065 ((0.9)²) and the
  ÷10/÷100 decimals card.

**RESTORE**
- alg-extra-exponent-extra-1 (2⁶/2³).
- alg-extra-exponent-extra-6: the original "Which is greater: 2¹⁰ or 4⁴?" with the choices "It cannot be determined /
  The first power / The second power / They are equal".
- `exponents`:
  - "Bases 1 and 0": restore the true line "A negative exponent means dividing by zero — undefined. Zero to the zero?
    Not defined in this course either."
  - "Exponent 1 and 0": the original proof 5³/5³ = 5⁰ = 1 is true, so restore it as a second way. Put it where the
    division law is taught (or right after it), so nothing is used before it is taught. The ÷5 staircase stays.
- Receives from T5: q-131, q-132 (with their original solution videos) and q-expression-extra-09.

**No action:**
- The moves of q-227, alg-extra-exponent-extra-2 and -7 to T9 follow the rule (they need roots).
- The "2⁴ = 4² is the one special case" overclaim stays fixed.

## T9 Roots
**Summary:** removed: roots of decimals. Roots of different order stay (the original q-245 has this type).

**REMOVE**
- Video `r26-t09-traps`: slide "Roots of small numbers", its sidebar label and any title-slide words.
- Practice q-r26-t09-07 (√0.0016) and q-r26-t09-08 (√0.9 closest to).
- Card `roots`, table "Exam traps": row "roots of small numbers".
- Evidence: 0 real and 0 original decimal roots.

**KEEP [changed from audit]:**
- Items:
  - slide "Different roots"
  - guided q-r26-t09-05 + `solve-q-r26-t09-05`
  - practice q-r26-t09-15
  - card row "square root vs cube root: 6th power"
- Why they stay: the original q-245 is "smallest of π, 3, ∛30, √7", which compares roots of different order.
- Also kept: practice q-r26-t09-12 (domain of √(2−x)). It teaches the original card tip "Inside a square root: never
  negative" and original q-234 ("No real value").

**RESTORE**
- q-239 (∛9·∛9·∛9).
- alg-extra-root-practice-6 (√12 × √27).
- q-242: the original "Evaluate ²·⁵√(√243)…" (choices 9/27/3/1, key 3). It is not a math error, so it comes back.

## T10 Exponents and roots: techniques
**Summary:** removed:
- comparing powers by making the exponents equal
- exponential inequalities with a base between 0 and 1
- "aˣ = bˣ ⇒ x = 0"

Sums of equal powers and common-factor questions stay.

**REMOVE**
- Video `r26-t10-power-traps`: slides "Compare powers", "Bases between 0 and 1" and "When is aˣ = bˣ?", with their
  sidebar labels and their Recap lines.
- Guided q-r26-t10-04 + `solve-q-r26-t10-04` (order of 2⁴⁵, 3³⁰, 5¹⁵).
- Guided q-r26-t10-05 + `solve-q-r26-t10-05` ((1/3)ˣ > 1/27).
- Renumbering: the section title "Ten guided questions" becomes "Eight guided questions", and the Q1–Q10 sidebars
  follow.
- Practice q-r26-t10-13, -14, -15.
- `mem-r26-t10-techniques`: rows "Comparing powers", "Base between 0 and 1" and "aˣ = bˣ, a ≠ b (positive)".
- Evidence: 0 real and 0 original questions of these types.

**KEEP [changed from audit]:** the original type is q-293 (2ˣ = 2ʸ+2ʸ+2ʸ+2ʸ), q-311 (3ⁿ − 3ⁿ⁻¹) and q-320 ((5⁴ − 5³)/4).
- q-r26-t10-02 + `solve-q-r26-t10-02` (2¹⁰ + 2¹⁰ + 2¹⁰ + 2¹⁰)
- q-r26-t10-03 + `solve-q-r26-t10-03` (3ˣ⁺² − 3ˣ = 72)
- practice q-r26-t10-06, -11, -12, -16

**RESTORE**
- q-263 (√63), q-283 (√98), q-277 (x = y = 8).
- alg-extra-unit-t10-3-1 … -3-7 (7 questions).
- alg-extra-unit-t10-2-6: the original choices "The first power / The second power".
- `powers-techniques` slide "Root equations": restore the original example √(x+7) = x − 1 with the board line
  "x − 1 ≥ 0 → x ≥ 1". Keep the new, fully solved √(x+2) = x after it.

**No action:** the false line in `solve-q-249` slide 2 stays deleted.

## T11 Exponents and roots: advanced
**Summary:** removed: the card row "compare powers" and two practice items (a decimal root, and huge powers). The
original "Laws + identities" slide and two original solution slides come back.

**REMOVE**
- Practice q-r26-t11-03 ((0.2)³·10⁴/√0.0016) and q-r26-t11-07 (order of 2¹⁰⁰, 10³⁰, 3⁶⁰).
- `mem-r26-t11-advanced`, table "From topics 8 to 10": row "compare powers: make the exponents equal".

**KEEP [changed from audit]:** the row "different roots: raise to a common power". Its type is original q-245 (see T9).

**RESTORE**
- alg-extra-unit-t11-3-1, -3-3, -3-5, -3-6.
- `advanced-powers` slide 3, the original "Laws + identities" with its script. The new "Patterns to spot" slide stays
  as an added slide after it.
- `solve-q-296`: the slide "Method 2 · Multiply the denominators" (a true method).
- `solve-q-299`: the slide "Open the brackets". It is correct: it does not divide by √x and finds 0 and 9. Put it back
  as a method next to "Product equals zero".
- `solve-q-297` slide 3: restore the line "The lesson's favourite is four — but here four gives root eight…".
- q-317: the original distractor 2/6.

**No action:** "Last question." and "No new rules here…" are no longer true after the reorder and the additions, so they
stay changed.

## T12 Inequalities
**Summary:** nothing is removed. q-340 and the original q-323 choices come back.

**REMOVE:** none.

**RESTORE**
- q-340 → its practice section.
- `inequalities` slide 4 "A minus flips it": the original demo is correct. Only ":(−4)" becomes "÷(−4)". Make sure the
  original advice survives: "I recommend you don't multiply by a minus at all… move the terms across… 4 < 12 … 1 < 3".
  Restore any of these lines that are missing.
- q-323: the original choices "0 / 12 / 1 / Any value" (key "Any value"; write it as "For every value of x" only if
  that is clean-up).

**No action:** the "cross-multiply" lines stay removed (they are true only for a positive number).

## T13 Absolute value
**Summary:** removed: writing a range as |x − m| < r (the midpoint trick). The "no solution" items and sums of distances
stay.

**REMOVE**
- Video `r26-t13-tools`: slide "From a range to bars", its sidebar label and its Recap line.
- Guided q-r26-t13-04 + `solve-q-r26-t13-04` ("which inequality is exactly −3 < x < 7"). Renumber the guided questions
  and sidebars SB1/SB2.
- Practice q-r26-t13-06 (−8 < x < 2 → bars).
- `mem-absolute-value`, table "Distance tools": row "a < x < b → |x − (a+b)/2| < (b−a)/2".
- Evidence: 0 real and 0 original questions.

**KEEP [changed from audit]:**
- q-r26-t13-02 + `solve-q-r26-t13-02` (|x+2| < −1 has no solution), q-r26-t13-05 and q-r26-t13-11 (|3x − 6| ≤ 0). They
  teach the original card tip "Right side negative? No solution. Right side zero? One case only." and original q-378.
- q-r26-t13-10 (|x−1| + |x−7| = 6). The original type is alg-extra-unit-t13-3-5 (minimum of |x−3| + |x−5|).

**RESTORE:** no questions were deleted.

**No action:** the other card rows are the same content, reworded.

## T14 Prime numbers
**Summary:** removed:
- zeros at the end of a number
- perfect cubes
- finding a number from its GCD and LCM

The three deleted questions and some true card tips come back.

**REMOVE**
- Video `r26-t14-more-tools`: slide "Zeros at the end", its sidebar label and its Recap line.
- Same video, slide "Squares & cubes": remove only the cube lines (18k a cube → k = 12). The square part stays; the
  slide can be retitled "Perfect squares".
- Guided q-r26-t14-02 + `solve-q-r26-t14-02` (24k a perfect cube).
- Guided q-r26-t14-04 + `solve-q-r26-t14-04` (zeros of 20⁴·15³).
- Renumber the advanced guided questions.
- Practice:
  - q-r26-t14-08 (GCD 6, LCM 180 → the other number): the original only asks for a GCD or an LCM
  - q-r26-t14-11 (cube)
  - q-r26-t14-14 (zeros of 20!)
- `mem-r26-t14-more-tools`: rows "Zeros at the end" and "Perfect cube" (this settles the auditor's UNSURE).
- Evidence: 0 real and 0 original questions.

**KEEP [changed from audit]:** q-r26-t14-10 (smallest k with 2³·3⁴·5·k a square). The original type is
alg-extra-unit-t14-4-6.

**RESTORE**
- q-416, q-420, q-410.
- `primes` Recap: the true lines "Know the primes up to 40 — and 97" and "Divides by every combination of its prime
  factors".
- `mem-primes` tips:
  - "A number divides by every combination of its prime factors (12 = 2·2·3 → 2, 3, 4, 6, 12)."
  - "To test a divisor, check its prime ingredients — unpack composite bases like 6 or 10² first."
- `mem-factor-tools` tip: "Divides by 2 and 5 → by 10. Divides by 2 and 6 → only 6 is sure (the 2 is inside the 6)."

**No action:** the false line "primes are the small numbers you never meet…" and the inexact GCD/LCM wording stay fixed.

## T15 Division and remainders
**Summary:** removed: the "reverse" remainder question ("100 ÷ n leaves 4, how many n?").

**REMOVE**
- Video `r26-t15-remainder-tools`, slide "Take away the remainder": remove the reverse half. That is the script from
  "Now turn it around. The exam loves this one." to "Check one: a hundred is six times sixteen, plus four. It works.",
  and its boards (100 ÷ n leaves 4…, 100 − 4 = 96, n > 4, the divisors of 96, the circle, the check). Keep the first
  half (N − r divides by d, the 53 example).
- Same video, Recap: drop ", and d > r".
- `mem-r26-t15-tools`, row "Known remainder": remove the example "100 ÷ n leaves 4 → n divides 96, n > 4: 8 values".
  Use the slide's kept 53 example as the example.
- Guided q-r26-t15-02 + `solve-q-r26-t15-02`. Renumber the guided questions.
- Practice q-r26-t15-03, q-r26-t15-04.
- Evidence: 0 real and 0 original questions. The line "The exam loves this one" is false.

**RESTORE**
- alg-extra-unit-t15-3-4, alg-extra-unit-t15-3-6.
- `mem-divisibility` was rebuilt. Put back any original row whose rule is true and is missing. The old rules for
  "by 6 / by 15", "by 11" and "divide by 4 and by 5" were wrong and stay fixed.

## T16 Integers
**Summary:** nothing is removed. q-477 comes back.

**REMOVE:** none.

**RESTORE:** q-477 (a, b, c consecutive, c² − a² = 48).

**No action:** the fixes to the false "smallest product is the divisor" rule, q-460, q-473 (they contradicted
themselves) and the q-489 solution stay.

## T17 The number line
**Summary:** nothing is removed. Two deleted questions and one original choice come back.

**REMOVE:** none.

**KEEP [changed from audit, UNSURE → KEEP]:** q-r26-t17-02 + `solve-q-r26-t17-02` and q-r26-t17-08, "which marked point
could be √x / x³", with FIG_Q11 and FIG_P3. The content (where x² and √x lie in each range) is original T17 content:
q-494, q-499, q-500, alg-extra-unit-t17-3-2. The picture format is the kept "Picture questions" slide.

**RESTORE**
- q-505, alg-extra-unit-t17-3-1.
- alg-extra-unit-t17-3-4: the original distractor "1/2 < 1/x < 1/5". It is a legal wrong choice, not an error.

**No action:** the invalid "replace every ten with a two" trick (`solve-q-500`) and the q-503 exponent fix stay fixed.

## T18 Letter puzzles
**Summary:** nothing is removed. The ones digit of powers and "how many digits can a product have" stay. Two deleted
questions and two replaced ones come back.

**REMOVE:** none.

**KEEP [changed from audit]:**
- Items:
  - the `r26-t18-facts` slide "Powers: ones digit", its recap line and sidebar entry
  - card row "Ones digits of powers repeat" and the 2⁵⁰ tip
  - practice q-r26-t18-08
- Why they stay: the original type is T15 alg-extra-unit-t15-3-2 (units digit of 7⁴).
- Also kept: practice q-r26-t18-06 (digit count of a 3-digit × 2-digit product). The original type is q-521 ("A is
  two-digit, B is four-digit; how many digits can A + B have?").

**RESTORE**
- alg-extra-unit-t18-3-1.
- alg-extra-unit-t18-3-4 (how many three-digit numbers from 2, 5, 8). It was removed as "counting is T28", so restore it
  and **move it into the T28 practice**.
- alg-extra-unit-t18-3-2: the original question asked for the ratio A : B (write "the ratio A : B"). The A + B version
  is dropped.
- alg-extra-unit-t18-3-7: the original wording ("What must A be at least?").

## T19 Defining a new operation
**Summary:** removed: the integer part [x]. Piecewise operations solved backwards stay.

**REMOVE**
- Video `operation-patterns`, slide "Definition in words": remove the [x] example (the boards "[x] = the largest integer
  that is not bigger than x", "[3.7] = 3, [5] = 5, [−2.3] = ?", the note "= −3, not −2" and the spoken lines about [x]).
  The rule and the remainder, divisor and digit-sum examples stay.
- `mem-new-operation`: the [x] example in the "definition in words" row.
- Guided q-r26-t19-04 + `solve-q-r26-t19-04`. Renumber the guided questions.
- Practice q-r26-t19-14 ([x] = 3).
- Evidence: 0 real and 0 original integer-part questions.

**KEEP [changed from audit]:**
- Items:
  - the slide "Conditions backwards" and its card row
  - q-r26-t19-03 + `solve-q-r26-t19-03`
  - practice q-r26-t19-11
- Why they stay: the original already has piecewise operations (q-545, q-546, q-547, q-565, q-569). It also has
  "given the output, find the input" (alg-extra-unit-t19-3-5, q-562, q-575 "for how many values of a does ◆(a) = …").

**RESTORE:** alg-extra-unit-t19-3-3, alg-extra-unit-t19-3-6.

**No action:** the q-567 ambiguity fix, the "Operation first" rule fix and the Q13 Method 2 fix stay.

## T20 Algebraic understanding
**Summary:** nothing is removed. "To be sure / worst case" stays. One deleted question and some true lines from the
original lesson come back.

**REMOVE:** none.

**KEEP [changed from audit]:**
- Items:
  - the `r26-t20-counting` slide "To be sure", its recap line and card row
  - guided q-r26-t20-04 + `solve-q-r26-t20-04`
  - practice q-r26-t20-09
- Why they stay: the original wp21-p14 ("first to win 4 rounds, what is the longest the game can last?") is the "worst
  luck + 1" type. T21 keeps the same slide for that reason. The real exam also has 2019_winter_q1_14.

**RESTORE**
- alg-extra-unit-t20-2-6 (a² = b² → |a| = |b|).
- `algebraic-understanding`: the original slides 2–7 were replaced by new slides on the same themes. Put back the true
  lines that were lost, in the matching new slides:
  - "No fixed recipe" → new "Three tools": "it's a fairly small part of the exam — and the questions don't repeat
    themselves. There's no repeating principle I can hand you that solves them all. But this lesson, and the practice
    after it, give you tools that open your head for questions like these."
  - "Connect topics": "A cycle of ratios cancels to one." and "…Lengths must be positive; cancelling needs nonzero
    values. Check before you use it."
  - The "Pythagoras in disguise" line points to T31 (a later topic), so it stays replaced.

## T21 Trial, limits and patterns
**Summary:** removed: finding a term from a formula for the sum of the first n terms. The weekday and last-digit cycles
stay.

**REMOVE**
- Practice q-r26-t21-08 (Sₙ = n² + 2n → 10th term). Evidence: 0 real and 0 original.

**KEEP [changed from audit]:**
- Items:
  - wp-022 slide 4 "Days and last digits"
  - its recap wording
  - the toolkit words "days of the week (÷ 7), last digits of powers"
  - practice q-r26-t21-10 (Monday + 100 days) and q-r26-t21-11 (units digit of 7⁵⁰)
- Why they stay:
  - "Repeating cycle → use the remainder" is an original card row and slide, and real (2023_spring_q1_07,
    2023_winter_q2_07). A weekday is a cycle of 7.
  - The units digit of a power is original (T15 alg-extra-unit-t15-3-2).

**RESTORE**
- wp21-p23 (36 stickers), wp21-p26 (6 packs, 4 and 9 markers).
- wp-006 slide 3 "A recurring motif" (removed; only one line of it survives).

**No action:**
- The false "range has no holes" slide (`solve-wp21-g021` #2) and the card row that said the same stay corrected.
- "Method 2 · Edge cases" was merged into the new Method 2; no content was lost.

## T22 General word problems and ratios
**Summary:** nothing is removed. Three deleted questions come back.

**REMOVE:** none.

**RESTORE:** wp22-p22, wp22-p25, wp22-p28.

**No action:** the line "the exam avoids that wording" was false and stays deleted. The little-guy tips were moved, not
lost.

## T23 Percent
**Summary:** removed: percentage points and the percent change of a rate. The original "16% of 25" and the "sixteen and
a bit" line come back.

**REMOVE**
- Video `r26-t23-traps`: slide "Percentage points", its sidebar entry and the recap line "Difference of two percents =
  percentage points". Fix the intro/recap counts ("Three traps" → "Two traps", and "Four questions next" to match).
- Guided q-r26-t23-02 + `solve-q-r26-t23-02` (pass rate). Renumber the guided questions.
- Practice q-r26-t23-07, q-r26-t23-08.
- `mem-r26-t23-traps`: row "Percentage points" (the intro count becomes "two").
- Evidence: 0 real and 0 original questions.

**RESTORE**
- wp23-p21: the original "What is 16% of 25?" (2/6/8/4, key 4). New version → new id: "28% of 75" as `q-r26-t23-15`.
- wp-052 slide 4: the line "Can't halve it precisely? Half of thirty-two is sixteen — so it's sixteen and a bit". It is
  true; keep it before the exact 16⅔% slide.

## T24 Overlapping groups
**Summary:** nothing is removed. Two deleted questions come back.

**REMOVE:** none. q-r26-t24-08 stays: "exactly one" is an original type (wp24-p12, p17).

**RESTORE:** wp24-p04, wp24-p02.

**No action:** the wrong "at most → maximum overlap" rule stays corrected.

## T25 Averages
**Summary:** nothing is removed. One deleted question and four changed ones come back.

**REMOVE:** none.

**RESTORE**
- wp25-p06.
- wp25-p05: the original "average of ⅔ and ⅙". New version → new id: the "how many at first" item as `q-r26-t25-14`.
- wp25-p25: the original "…What is their sum?" (key 161). New version → new id: "largest of them" as `q-r26-t25-15`.
- wp25-p23: the original numbers (test 68, project 92, answer 74). The new-numbers version is dropped.
- wp25-p11: the original condition "b = a + 2".

## T26 Work and rates
**Summary:** nothing is removed. The "sense check" stays. Three deleted questions come back, and p10 goes back to its
circle form in T33.

**REMOVE:** none.

**KEEP [changed from audit, UNSURE → KEEP]:** wp-094 slide "Sense check", its recap part and card tip. This method
removes 2 of the 4 choices in the real 2019_spring_q1_08.

**RESTORE**
- wp26-p02, wp26-p14, wp26-p15.
- wp26-p10: the original rough circular floor, radius 15, answers in π. It used circle area (T33), so **move it into the
  T33 practice**. New version → new id: the 600 m² half-and-half version stays in T26 as `q-r26-t26-13`.
- wp26-p12: the original "seal 2q envelopes" with its original choices. The "n envelopes" version is dropped.
- `solve-wp26-g093` slide 3: the original "Method 2 · Triple value" (a true method). Call it "triangle value", as the
  course now does. The new "Rate × time" slide stays.

## T27 Motion
**Summary:** removed: two trains passing each other (with lengths), and meeting twice. Distance–time graphs stay.

**REMOVE**
- Video `r26-t27-special`: slides "Two trains" and "Meeting twice", their Recap lines and their sidebar entries.
- Guided q-r26-t27-04 + `solve-q-r26-t27-04`. Drop "Question 17" from SPECIAL_SB and renumber.
- Practice q-r26-t27-08, q-r26-t27-13, q-r26-t27-14.
- `mem-r26-t27-special`, table "Special cases": rows "Two trains pass each other" and "Two walkers meet, go on to the
  ends, meet again", and the intro words "meeting twice".
- Evidence: 0 real and 0 original questions. The original wp27-p22 is two trains meeting as points, and it is restored.

**KEEP [changed from audit, UNSURE → KEEP]:**
- Items:
  - `r26-t27-graphs` slides "Distance–time graphs" and "Two travelers", with their figures
  - guided q-r26-t27-07 + `solve-q-r26-t27-07`
  - practice q-r26-t27-19, -20
  - the card table "Distance–time graphs"
- Why they stay: the real chart set 2019_spring_q1_16–20 (Amnon and Boaz) gives the distance each runner covered in each
  minute, and asks the distance between them (q1_20) and a runner's progress at a given moment (q1_16).

**RESTORE**
- wp27-p14, wp27-p21, wp27-p22, wp27-p23.
- wp27-p10: the original asked for the central angle (45°/72°/90°/60°). That is circles (T33), so **move it into the T33
  practice**. New version → new id: "fraction of the track" stays in T27 as `q-r26-t27-23`.
- wp-108-after slide 1: the line "Honestly? Rare on the exam." It is true: average speed appears in 1 of 760 real
  questions.

## T28 Counting
**Summary:** removed:
- groups with no names
- road maps
- the zero-digit trap

"Objects into boxes" stays. The three deleted questions come back.

**REMOVE**
- wp-137 "Choosing a Group": slide "Groups with no names" and its sidebar entry.
- Video `r26-t28-cases`: slides "Road maps" (with its figure) and "The zero trap", their Recap lines and sidebar
  entries. Rename the video: the title "Roads, Zeros and 'At Least One'" no longer fits, for example "Boxes and 'At
  Least One'".
- Guided questions, then renumber:
  - q-r26-t28-01 + `solve-q-r26-t28-01`
  - q-r26-t28-02 (+ figure) + `solve-q-r26-t28-02`
  - q-r26-t28-03 + `solve-q-r26-t28-03`
- Practice q-r26-t28-10, -11, -12, -13, -24, -25.
- `mem-counting` table 2: row "Groups with no names".
- `mem-counting-advanced`:
  - rows "Road map" and "A zero among the digits"
  - the tips "A route may use the direct road too…" and "Digits with a zero: the leading digit is never 0…"
- Evidence: 0 real and 0 original questions. The original p27 says "two NAMED teams", and no original digit set has
  a 0.

**KEEP [changed from audit]:**
- Items:
  - the slide "Which is the base?" and its recap line
  - guided q-r26-t28-05 + `solve-q-r26-t28-05` (letters into mailboxes)
  - practice q-r26-t28-16
  - the card row "Objects into boxes"
- Why they stay: each object chooses a box, so the count is (number of boxes) to the power of (number of objects). That is the original "codes with repetition" type (wp28-g128),
  which is also real (2022_winter_q2_18).

**RESTORE**
- wp28-p04, wp28-p07, wp28-p13 (p13 is also a real type: 2025_autumn_q1_03).
- Receives alg-extra-unit-t18-3-4 from T18.
- The true "rare" lines. The real exam has 2 subtract-cases questions in 760, and choosing-a-group is also rare:
  - wp-134 slide 2 "Rare and hard"
  - wp-134 slide 4 "Subtracting possibilities is even rarer."
  - wp-137 slide 2 "…Very hard, and very rare."

## T29 Probability
**Summary:** removed:
- geometric probability (the whole lesson and card)
- "unknown count" (how many balls to add)
- the "AND smaller / OR bigger" size check

Some true original lines come back, among them "opposite faces of a die add to seven".

**REMOVE**
- Whole video `r26-t29-geometric` (5 slides, 3 figures) and its sidebar.
- Card `mem-r26-t29-geometric`.
- Guided q-r26-t29-05 (+ figure) + `solve-q-r26-t29-05`. Drop "Question 22" from ADV_SB.
- Video `r26-t29-more-rules`: slide 5 "Unknown count" and its entry in LESSON_SB (shared by wp-146, wp-147-after, wp-151
  and wp-159).
- Guided q-r26-t29-04 + `solve-q-r26-t29-04`. Renumber the guided questions.
- Practice q-r26-t29-06, -07, -12, -13, -14.
- `mem-probability`: row "Unknown count".
- The size check (this settles the auditor's UNSURE):
  - wp-151 slide "OR with overlap": the last two lines "Size check: AND → smaller · OR → bigger"
  - the `mem-probability` tip "Size check: AND makes the chance smaller, OR makes it bigger."
- Evidence: 0 real and 0 original questions for all of these.

**RESTORE**
- wp29-p03, wp29-p20.
- wp-159 slide 2: the true line "By the way — opposite faces of a die always add to seven…".
- wp-151 slide 2: the line "Or questions are rare". It is true: 1 OR-probability question in 760. The new
  separate-cases condition stays.
- `mem-probability`:
  - the original OR example "1/7 + 6/7 · 1/6 = 2/7" (correct), next to the new example
  - the full original tip '"Or" questions are rare — and a second try only happens after a first miss.'
- `solve-wp29-g158`: the original slide "Method 2 · Complement".

## T30 Lines and angles
**Summary:** removed: the C-shape bend (360°) and the units-digit tip. The "dot in the right-angle square" line and three
original questions come back.

**REMOVE**
- `solve-geo30-g007`: slide "The C shape". The zig-zag slide stays.
- `mem-lines-angles`: row "Bent line (C shape)" and the units-digit tip (83° + 54° + x = 180°).
- Practice q-r26-t30-08.
- geo30-foundation-p14: undo the C-shape rewrite and the move to advanced (see RESTORE).
- Evidence: 0 real and 0 original questions.

**KEEP [changed from audit, UNSURE → KEEP]:** q-r26-t30-02 + `solve-q-r26-t30-02` (segments on a line). The original
type is geo30-advanced-p09 and -p16.

**RESTORE**
- geo30-foundation-p09, geo30-foundation-p15.
- geo30-foundation-p14: the original question (bent line, a ∥ b, x), back in the foundation practice.
- geo-001 slide "Right angle": the line "on the exam there is almost always a dot in the square". It is TRUE (see
  2020_autumn_q2_20, 2024_autumn_q2_02, 2026_spring_q1_16). The new "only if marked or given" line stays.

## T31 Triangles
**Summary:** nothing is removed. All the UNSURE extra items stay. Two original questions come back.

**REMOVE:** none.

**KEEP [changed from audit, UNSURE → KEEP]:** the original types are geo31-g033, geo31-advanced-p17, -p18, -p22, the
`geo-026` slide "Using 30°-30°-120°" and geo38-core-p25.
- q-r26-t31-03 + `solve-q-r26-t31-03`
- q-r26-t31-04, -06, -07, -10, -11
- the "whole-number third side: 2 × shorter − 1" board line, spoken line, card row and p22 shortcut (a method for the
  original geo31-foundation-p22)

**RESTORE**
- geo31-foundation-p26.
- geo31-advanced-p01: the original "Which of the following triangles is not necessarily equilateral?" with its original
  choices and key. New version → new id: "one median is also an altitude" as `q-r26-t31-12`.
- geo-019 slide 3: the line "Let's see sample questions" (it is still followed by sample questions).

**No action:** the "we don't use this rule a lot" lines about the exterior angle stay deleted (the real exam uses it).
The Pythagoras-order change and the figure changes stay.

## T32 Quadrilaterals
**Summary:** removed:
- the concave "arrow" rule
- the trapezoid midsegment
- the trapezoid "butterfly"

The "Completions" slide and five deleted questions come back.

**REMOVE**
- Video `geo-042`: slide "The arrow rule".
- Video `geo-054`: slide "The midsegment".
- Video `geo-067-after`: slide 8 "Trapezoid butterfly".
- Guided questions, then update the group sidebars:
  - q-r26-t32-03 + `solve-q-r26-t32-03` (Q10)
  - q-r26-t32-04 + `solve-q-r26-t32-04` (Q12)
  - q-r26-t32-05 + `solve-q-r26-t32-05` (Q23)
- Practice q-r26-t32-10, -11, -14 (foundation) and q-r26-t32-15, -16, -19 (advanced).
- Card cells and rows:
  - `mem-quad-family`: the tip "Concave (arrow): …", and in the Trapezoid row, column 4, the words "the two side
    triangles have equal areas" (restore the original cell)
  - `mem-quad-area`: in the Trapezoid row, column 3, "or midsegment × h (midsegment = (a+b)/2)" (restore the original
    cell)
  - `mem-equal-heights`: row "Trapezoid with both diagonals…"
- Evidence: 0 real and 0 original questions.

**KEEP [changed from audit, UNSURE → KEEP]:**
- q-r26-t32-07 + `solve-q-r26-t32-07` (perimeter + diagonal → area). The original type is geo32-advanced-p21.
- q-r26-t32-12 (+10% and +10% → +21% area). The original type is geo32-foundation-p24 and -p25.

**RESTORE**
- geo32-foundation-p05, -p08, -p12, -p19, -p22.
- `solve-geo32-g070` slide 3 "Approach 2 · Completions". It is correct: the middle 3 × 3 block really is 9 whole
  squares, and the slide itself says pairing pieces by eye would be a guess. Rename slide 4 back to "Approach 3 · Split
  with symmetry" and restore its closing line "…by completions or by symmetry."
- `solve-geo32-g059` and `solve-geo32-g060`: the original framing "learn all three" / "it's important to know all of
  them", in place of "(optional)", and the original slide order.

## T33 Circles
**Summary:** removed: a quadrilateral around a circle, and two circles meeting at two points. The SSS proof and four
deleted questions come back.

**REMOVE**
- Video `geo-077`, slide "Circle inside a triangle": the board item "Quadrilateral around a circle: AB + CD = BC + AD"
  and its spoken line "The same idea works for a quadrilateral around a circle…". The triangle part stays.
- `mem-circle-rules`: row "Quadrilateral around a circle".
- Practice q-r26-t33-08 and q-r26-t33-13.
- Evidence: 0 real and 0 original questions. The original geo33-advanced-p19 has a trapezoid around a circle but does
  not use this rule.

**KEEP [changed from audit, UNSURE → KEEP]:** original types geo33-advanced-p26, -p20 and geo33-foundation-p24.
- q-r26-t33-02 + `solve-q-r26-t33-02`
- q-r26-t33-03 + `solve-q-r26-t33-03`
- q-r26-t33-05 + `solve-q-r26-t33-05`
- q-r26-t33-09, -14

**RESTORE**
- geo33-foundation-p09, -p13, -p25, geo33-advanced-p08.
- Receives wp26-p10 (T26) and wp27-p10 (T27) into the T33 practice.
- `geo-075` slide "Equal chords": the original SSS congruence proof (true). The new figure stays.
- `solve-geo33-g078`: the "Pavlov" line (draw the radii automatically).
- `geo-077` / `geo-079`: "Let's solve a sample question." / "Let's see a psychometric question.", if a sample question
  still follows.
- `solve-geo33-g102`: "That's it for circles. On to the summary.", if it is still the last circles video.

**No action:** the Q16 Method 3 correction, the Q20 estimate reason, the figure giveaways that were removed (center O,
144°, OD, the angle arcs, α/γ → ?) and the `geo-097-after` claim stay fixed.

## T34 Polygons
**Summary:** removed: "could this be an angle of a regular polygon?". "n from an angle", counting diagonals and the
octagon area stay.

**REMOVE**
- `geo-104` slide 13 "Angle → sides": only the last 5 script lines, from "And a classic exam question: which of these
  could be an angle of a regular polygon?" to the board item "…180 − angle must divide 360".
- `mem-polygons`: the tip "Could it be an angle of a regular polygon? …".
- Practice q-r26-t34-06.
- Evidence: 0 real and 0 original questions. The words "a classic exam question" are false.

**KEEP [changed from audit]:**
- q-r26-t34-01 + `solve-q-r26-t34-01` and practice -05: "n from an angle". The original type is geo34-core-p21 and -p22.
- q-r26-t34-02 + `solve-q-r26-t34-02` and practice -07: counting diagonals. The original type is geo34-core-p23.
- Practice -10: the octagon cut from a square. The original type is geo34-g108 and -g115.

The guided numbering does not change.

**RESTORE**
- geo34-core-p03, geo34-core-p14.
- `geo-104` slide 5: the board item "5: 540° → 6: 720° → 7: 900° → 8: 1080°" (true).
- `geo-112-after` slide 4: the line "…fold the three corners in, like the paper, and you get a hamantasch".

**No action:** "measure with your fingers" (false) stays deleted. The p12 solution stays on the taught route, because
the tangent–chord rule is not taught.

## T35 Solid geometry
**Summary:** removed: water rising when an object sinks (displacement), and the shortest path on a cube's surface. Water
pouring, liters, the painted cube, solids of revolution and bricks in a box stay.

**REMOVE**
- Video `r26-t35-water`:
  - slide "Dropping in a solid" (with its figure) and its sidebar entry
  - the recap board "Rise" and its sentence "An object pushes the water up by its own volume."
- Title line "A classic on the exam…": this claim is false, so reword it (an error fix).
- Video `r26-t35-cubefacts`: slide "Walk on the surface" (with its figure) and its sidebar entry.
- Practice q-r26-t35-06, q-r26-t35-07 (displacement), q-r26-t35-11 (the ant on a cube).
- `mem-solids`, table "Water and units": row "Object sinks in water".
- `mem-cube-facts`: the tip "Shortest path on the surface: …".
- Evidence: 0 real and 0 original questions.

**KEEP [changed from audit]:**
- Items:
  - the slide "Liters and cm³" and the recap "Units" board
  - the Quick-checks board "Same units first"
  - the `geo-119` line "one milliliter is exactly one cubic centimeter"
  - the card row "Units"
  - practice q-r26-t35-04 and -13
  - `geo-120` slide 2 keeps "units"
- Why these stay: the original `geo-119` slide 10 teaches "330 millilitres — that's a volume unit" and cm³, and the
  original geo35-g121 and geo36-g151 are water-container questions.
- Also kept:
  - q-r26-t35-03 + `solve-q-r26-t35-03` and practice -14: the painted cube, original type geo35-core-p24
  - practice -16: solids of revolution, original type geo35-core-p01
  - practice -10, the Quick-checks board "Solids in a box… try each position" and the bricks tip: packing solids in a
    box, original type geo35-g131

**RESTORE**
- geo35-core-p09.
- geo35-core-p27 stays in T36: it needs k³, which is taught there, and that follows the rule.
- `geo-119` slide 2: the original 3 × 3 "Rubik" cube figure.
- `solve-geo35-g130` slide 4: the original edge-2 cube example. The new one-step box diagonal (26) stays as an added
  line.
- geo35-g121 solution: the true bound "65.1 < 21π < 66".

**No action:** the wrong cube-angle board lines (g129, g130) and the p10 giveaway sentence stay fixed.

## T36 Similarity and scale
**Summary:** nothing is removed. Percent change, map area and the cone filled to part of its height stay. Two deleted
questions and some original slide content come back.

**REMOVE:** none.

**KEEP [changed from audit]:**
- q-r26-t36-03 + `solve-q-r26-t36-03` (cube edge +20%) and practice -14, -15: percent change. The original type is
  geo36-core-p20 and geo35-core-p27.
- q-r26-t36-05 + `solve-q-r26-t36-05` (map area) and practice -17, -18. The original type is geo36-core-p23.
- Practice -13 (cone glass filled to ⅔ of its height), the `geo-141` slide "Half-height cone" and the card row "Cone
  filled to half its height" (the auditor had it UNSURE). The original type is geo36-core-p16 (a cone cut at ⅔ of its
  height).

**RESTORE**
- geo36-core-p10, geo36-core-p15.
- `geo-134` slide 12 ("man with glasses"): the original images and lines (Kenny from South Park with binoculars,
  "Batman").
- `geo-143` slide 6: the words "From the course —".
- `solve-geo36-g138` slide 3: the line "A small tip about answers: usually they don't confuse me — they help me." The
  false line "the common mistake usually won't even be in the choices" stays replaced.
- `geo-139` slide 12 "Recap": any original recap line missing from the rewrite.

**No action:** the Q5 "256" explanation fix and the Q6 part-to-part fix stay.

## T37 The coordinate system
**Summary:** removed: "which quadrant?" questions and negative slope. Line equations and intercepts stay.

**REMOVE**
- `geo-159`:
  - slide "Stairs going down" (with its figure) and its sidebar entry
  - on the slide "The line equation": the draw note 'Write "y = −3/2 x + 6" next to the stairs-going-down line' and
    the spoken line after it (they point to the removed slide; the rest of the slide stays)
- Guided q-r26-t37-01 + `solve-q-r26-t37-01`. Renumber the guided questions and re-check the "in Question N"
  references.
- Practice q-r26-t37-02, q-r26-t37-04 (which quadrant) and q-r26-t37-08 (negative slope).
- `mem-coordinates`: row "Slope | up ÷ across, with a sign…".
- Evidence: 0 real and 0 original questions of these types. The original stems only say "in the first quadrant", and
  the kept "Four quadrants" slide covers that.

**KEEP [changed from audit]:** q-r26-t37-07 + `solve-q-r26-t37-07` (4x + 3y = 24 cuts the axes) and practice -09. The
original type is geo37-core-p25 and -p26.

**RESTORE**
- geo37-core-p16.
- `solve-geo37-g166` slide 3: the line "If you prefer an equation…". Its board becomes "10 ÷ 4 = 5 ÷ ?" in fraction or
  ÷ form.

**No action:** "Hebrew version", "A is in the negative region" (backwards logic), "they never meet" (false), "tangent to
both axes → same x and y" (false) and "three, three, three, three — 12" stay fixed.

## T38 Geometric reasoning
**Summary:** removed: the shortest path on a cube, and the angle-bisector ratio shortcut. "Acute or obtuse from the
sides", plane sections and equal-perimeter shapes stay.

**REMOVE**
- `solve-geo38-g184` slide 5: the board item "Shortcut: KN/NL = KM/ML > 1" and its 2 spoken lines.
- geo38-g184 solution: the line "Shortcut: the bisector gives KN/NL = KM/ML…".
- Practice q-r26-t38-08 (the shortest path on a cube).
- Evidence: 0 real questions. The original Q10 already has its own solution, and no original question needs the
  shortcut.

**KEEP [changed from audit]:**
- The `geo-175` slide "Acute or obtuse?", the card row "Acute, right or obtuse?" and practice -05. The original is
  geo38-core-p25: "sides 7, 8, 10 — which statement is correct: obtuse / acute …".
- Practice -04 (∠APB = 100° on a diameter → P is inside). The original type is geo38-core-p17 (angles at points inside
  a circle).
- Practice -07 (a cube cross-section with 7 sides is impossible). The original type is geo38-g186 (a solid cut by one
  plane).
- Practice -11 (circle vs square with equal perimeter). The original type is geo38-g173 (equal perimeters, greatest
  area).

**RESTORE:** geo38-core-p18, geo38-core-p26.

**No action:** the "60° → equilateral" error in g183 and the figure fixes for Q4, Q5 and Q9 stay fixed.

---

## Short checklist for the person applying the plan
1. Apply the REMOVE lists topic by topic. After each topic, fix the renumbering, sidebars and "N questions" counts
   (see Global instructions).
2. Put the 113 deleted originals back into their sections.
3. Restore the 26 replaced originals:
   - 6 of them move: q-018 → T2; q-131, q-132, q-expression-extra-09 → T8; wp26-p10, wp27-p10 → T33 (and the deleted
     alg-extra-unit-t18-3-4 goes to T28)
   - the new versions that stay get new q-r26 ids: t01-25, t02-25, t03-09/10/11, t23-15, t25-14/15, t26-13, t27-23,
     t31-12
4. Restore the choices of q-156, q-171, q-203, q-317, q-323 and alg-extra-unit-t17-3-4.
5. Restore the listed original slides and lines, with the same clean-up (TeX, ÷, stacked givens).
6. Run `python3 math_check.py N` for every topic you touched. PROBLEMS and LAYOUT must be 0.
