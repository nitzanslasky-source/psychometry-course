# Topic 7 (Equations): changes (course review 2026-09)

Patch: `math_patches/t07.py`. `python3 math_check.py 7` gives 0 problems, 0 warnings and 0 layout problems.

## 1. Wrong statements fixed
- **Q16 video, Method 3, "Brainwave two"**: the old line said "each letter is bigger than the next". That is false for negative numbers. The new line says: all three ratios are bigger than 1, so their product x/w is bigger than 1.
- **q-214 solution**: rewritten cleanly (x ≤ 1 and y ≤ 1 give 4x + 3y ≤ 7 < 10, a contradiction). It now also shows why choices 2, 3 and 4 fail. Choice wording changed from "and/or" to "x > 1 or y > 1 (or both)".
- **Q20 video**: now says why "cannot be determined" is wrong: every allowed case gives a = 0. The first line changed from "Last question on equations" to "Last question in this set", because more questions follow now.

## 2. Methods added
**Main lesson "Solving Equations Smarter"** (9 slides before, 12 now, about 8 min):
- Slide 2: new habit "or check x = 0 separately".
- Slides 5, 6 and 9 (one equation with two unknowns, build the expression, break it apart): each one now has a worked mini-example on the board. The line "How do you know which one? Practice." was removed.
- **New slide "Which operation?"**, a checklist: mirror coefficients → add or subtract; a letter missing from the answers → make it cancel; products or ratios → multiply or divide; strange target → multiply one equation first; nothing fits → plug in.
- Slide "Hidden formula": now shows both (x + y)² and (x − y)², the rule "know two of x ± y, x² + y², xy → get the third", and a number example.
- **New slide "Plug in numbers"** with 4 rules: the numbers must fit all the givens; avoid 0 and 1; check all four choices; if two choices match, plug in again.
- **New slide "Try the choices"** (work back from the answers). It warns that a choice that works is one solution, not always the only one.
- The recap slide was updated.

**New lesson "More Equation Tools"** (end of Advanced study B, 2.6 min): multiplying or dividing equations, x + 1/x (and x − 1/x), and systems with no solution or infinitely many (parameter k).
- Guided Q21 (q-r26-t07-01) divides two equations. Guided Q22 (q-r26-t07-02) is x + 1/x = 3. Guided Q23 (q-r26-t07-03) asks which k makes a system have no solution. Each has a solution video.

**New lesson "Quadratic Equations"** (new section "Quadratic equations", placed after Advanced study B, 4.4 min). The whole course had no lesson on this before. Slides: standard form and "everything to one side"; factoring with "product c, sum b"; the zero-product rule gives two solutions, and the sign flips; special cases (no number term, no x term, the same two numbers → one solution, x² = −4 → no solution); **the trap a² = b² ⇒ a = b or a = −b**; try the choices; a fraction equals 0 (throw out solutions that make the denominator 0); recap.
- Guided Q24 (q-r26-t07-04): x² − 2x = 15, factoring, plus trying the choices. Guided Q25 (q-r26-t07-05): (x + 1)² = (x − 3)², the a² = b² trap, plus expanding. Guided Q26 (q-r26-t07-06): (x² − 7x + 12)/(x − 3) = 0, the extraneous solution, plus trying the choices. Each has a solution video with 2 methods.

**New memory card** "Equations: traps and shortcuts" (`mem-r26-t07-equations`), right after the main lesson. Topic 7 had no card before. It has three tables: Traps, Which operation?, and Quadratic equations (4 steps), plus tips.

## 3. Text
- Every question in the topic (33 existing ones) was rewritten in clean TeX. Examples: `$x^7 = x^6 y$` instead of `{x}^{7}`, and `\frac{a - 5b}{4}`, so the fraction in Q4 now shows correctly.
- Given equations are now stacked with `\begin{cases}` (18 questions).
- Colons used for division were removed from all solutions (q-180, q-184, q-189, q-199, q-204, q-208, q-212, q-217 and others) and from 3 draw notes (Q8 and Q17 videos). The real ratio question q-216 keeps ":" and says "ratio".
- "0 < m, n" became "m > 0, n > 0" (q-203). "0 < x, a" became "x > 0, a > 0" (q-204). "0 < x" became "x > 0" (q-211). "a, b, c, d ≠ 0" (q-186) and "m, n ≠ 0" (q-180) were written out one by one.
- q-203: choice 4 "m² − 2" was replaced with "−n", a trap that comes from m² = n².
- The one-line alg-extra solutions were written out step by step with numbers (for example t7-5-5: 2(x − 6) = x + 8 → x = 20).
- Solutions no longer use "so" to mean "therefore". Solutions that used plug-in or estimation now show those checks (q-181, q-184, q-190).
- In the videos, formulas are named instead of numbered ("the square of a sum", "the difference of squares"): Q11, Q15, Q18 and Q19. Q10 now says Method 1 is enough for the exam. Q14 explains why using 1s was safe there. American spelling ("math", "recognize"). ", so x is" became ". So x is".

## 4. Figures
- None in this topic.

## 5. Practice
- **Removed** the 7 clone items alg-extra-unit-t7-1-1 … 7 (copies of t7-5-x).
- The section "Additional source-bank variants" was renamed **"Retry set (same types as Questions 1–6)"** and keeps q-172 … q-177.
- **Added 15 practice questions** (q-r26-t07-07 … 21):
  - Quadratics: solutions of x² − 6x + 8, 2x² = 8x (the divide-by-x trap), x² = y² → |x| = |y|, (x² − 9)/(x − 3) = 0, x² − 10x + 25 (one solution), (2x − 1)² = (x + 4)² with x > 0.
  - x − 1/x = 4, and x² + 1/x² = 14 → x + 1/x.
  - Dividing equations (xy, yz → x/z), multiplying equations (xyz with three products).
  - Parameter systems: infinitely many solutions → k; infinitely many → a + b.
  - Plugging in on purpose: 4y from x = 2y + 3; xy in terms of k.
  - An estimation question (19/20 x = 38).
- Independent practice is now ordered easy → hard: the alg-extra warm-ups first, and q-215, q-208 and q-214 last. It has 42 items, about 15 of them exam-hard.

## Counts
- Questions: 40 of the 40 existing questions rewritten (text, TeX and solutions; all keys unchanged). 21 added (6 guided + 15 practice). 7 removed.
- Videos: 2 new lessons and 6 new solution videos. The main lesson has 6 slides rewritten and 3 slides added. 10 existing solution videos were edited directly (1 math fix, the rest wording and notation). All 20 got spelling and "so" fixes.

## Worked around the API / for the teacher to decide
- The API cannot create sections. The patch adds the section "Quadratic equations" by hand: it goes into `D['sections']`, into `M.sections` and into the topic's `sections` list, right after `equation-b`.
- The new guided questions are numbered 21–26 and sit at the end of the learn part, so the numbering stays in order. Please decide whether the quadratics lesson should move earlier. It fits well after Q7, but then "Question 24" would come right after "Question 7".
- The main lesson is now about 8 minutes long. If that is too long, "Plug in numbers" and "Try the choices" could become a separate short video.
- Existing solution-video titles are still the raw stem text (for example "Given: {x}^{7}…"). That is the base data, not something this patch changed. The "Q None" numbering shown on practice items comes from the renderer, not from this topic's data.
- T4/T5 practice uses quadratics before this lesson (see PLAN.md). Those topics may want a pointer to T7, or the quadratics lesson could move earlier in the course.
