# Topic 6 — Equations: Fundamentals — changes (course review 2026-09)

Patch: `math_patches/t06.py`. Check: `python3 math_check.py 6` gives 0 problems, 0 warnings and 0 layout problems (51 slides).
I solved every new or changed question again with exact arithmetic. Each has exactly one correct choice, and the key matches its solution video.

## 1. Wrong or overstated rules
- Systems lesson, slide 2: "as many equations as unknowns and you can solve it" now says **usually**. The teacher adds that the next topic shows systems with no solution or with endless solutions. The Q2 video says "so we can usually solve it".
- Teacher draw notes: ":4" is now "÷4" (lesson slide 2), and ":3" is now "÷3" (Q2 video).
- q-156 had the choice "Seven". The new choices are Exactly one / Exactly two / Infinitely many / None. The solution explains the divide-by-x trap.

## 2. Methods added
**Lesson "Equations — Fundamentals"** (8 → 12 slides; sidebar updated):
- New slide 6 **Cross-multiply**: 3/(x+1) = 2/(x−1). The restriction comes first, and the slide states the condition on the board: only when one fraction equals one fraction.
- New slide 7 **Forbidden answer**: x/(x−2) = 2/(x−2) gives x = 2, which is forbidden, so there is no solution.
- New slide 9 **Minus before a fraction**: (x+1)/2 − (x−3)/5 = 2. Every numerator goes in brackets, and −2(x−3) = −2x + 6. Writing −6 gives the wrong answer 7.
- New slide 11 **Test the choices**: 6/(x−1) = x − 2. The forbidden choice is skipped, and the others are tested until one works.
- Recap rebuilt with 7 lines covering the new rules. The closing line now points to three questions.

**Lesson "Systems of Equations"** (7 → 10 slides; sidebar updated):
- All pairs of equations on the board are now stacked with a brace (`cases`).
- New slide 5 **Add and subtract**: x+y=10 and x−y=4. The slide draws the bracket when subtracting, (x+y) − (x−y) = 2y, and teaches the shortcut x = sum/2, y = difference/2. The old one-line mention on the Elimination slide now points to this slide.
- New slide 8 **Get x + y directly**: 3x+y=17 and x+3y=11. Adding gives x+y = 7, and subtracting gives x−y = 3.
- New slide 9 **Multiply equations**: xy=12 and x/y=3, with x, y > 0. Multiplying gives x² = 36. Dividing gives y² = 4.
- Recap rebuilt as a "which method when?" list (coefficient 1 / same or opposite / no match / combination / product and quotient).

**New guided questions, each with a 2-method solution video**
- Q4 `q-r26-t06-01`: (x+2)/3 − (x−4)/6 = x/2 → 4. Covers the LCD with a minus. The sign trap gives 0.
- Q5 `q-r26-t06-02`: (2x+1)/(x−2) = (x+3)/(x−2) → no solution. Covers the forbidden answer and testing the choices.
- Q6 `q-r26-t06-03`: 5x+3y=41 and 3x+5y=39. Asks for x+y (answer 10) by adding the equations. The long way gives decimals.
- Q7 `q-r26-t06-04`: xy=20 and x/y=5, with x, y > 0. Asks for x−y (answer 8) by multiplying the equations, or by substitution.

**Memory cards (new; the topic had none)**
- `mem-r26-t06-single` (after the first lesson): the moves, restriction, cross-multiplying, minus before a fraction, identity/contradiction, and testing the choices.
- `mem-r26-t06-systems` (after the systems lesson): a method-choice table, the add/subtract shortcut, and multiplying or dividing the equations.

## 3. Text (all 45 remaining original questions)
- Every stem, choice and solution is now TeX. There is no ":" for division anywhere, and no plain-text math.
- Every system of equations is stacked (`Given:` + `cases` + `x = ?` on its own line). The restrictions ("Given: x ≠ 2 and x ≠ 4.") go on their own line.
- q-153: "0 < x, y" is now "x > 0 and y > 0". Its solution now shows the multiply-the-equations shortcut first.
- Every solution shows the numbers and uses the taught method. Rewritten highlights:
  - t6-2-3: add the equations → 5(x+y) = 55 → 11.
  - t6-2-4: subtract → x − y = −3, with a warning about the order of subtraction.
  - t6-1-4: (x+y)² − 2xy = 144 − 70 = 74.
  - q-162 and q-148: brackets plus the half-sum/half-difference shortcut.
  - q-152: reciprocal step.
  - q-155: why dividing by x is allowed here.
  - t6-1-5 and t6-4-7: cross-multiplying.
  - The one-line solutions of the t6-1-* items are gone, and so is the template text "The requested expression is …".
- q-171 distractors "31" and "21" were not built on real mistakes. They are now −1 (bracket not opened) and 5 (wrong cross-multiplication). The key stays choice 1, and x = 2 stays choice 4, so the video still matches.
- q-169 and q-170: text choices are in TeX. "−5/2" is written as −\frac{5}{2}.

## 4. Figures
- None in this topic.

## 5. Practice
**Removed** (13 near-duplicates):
- t6-4-1, t6-4-2, t6-4-3 (this also removes the odd "= 12/4" item), t6-4-5.
- t6-2-1 (an exact copy of lesson slide 5), t6-2-2, t6-2-5, t6-2-6, t6-2-7. The 2x+3y / 3x+2y template is kept only in t6-2-3 and t6-2-4, which practise the shortcut.
- q-141 (identical to the lesson example), t6-1-1, t6-1-2, t6-1-3 (a clone of t6-2-3).

**Added** (13 practice questions, `q-r26-t06-05` … `-17`):
- Single-equation practice: 05 cross-multiplying (the trap gives −8), 06 minus before a fraction, 07 testing the choices (12/x = x+1), 08 parameter for infinitely many solutions (a = 4), 09 extraneous answer where you cannot cross-multiply directly (no solution), 10 exam-hard LCD with the minus and the −1 traps.
- Systems practice: 11 half-difference with a negative number (y = 9, trap 6), 12 get 2x+y directly by subtracting, 13 x(y+2)=24 and x(y−1)=12 by dividing or subtracting (y = 4).
- Mixed practice: 14 (x+y)/(x−y)=3 → x/y = 2, 15 how many solutions does (x−1)/(x−1)=1 have (every number except 1), 16 3x−2y=5 → 6x−4y+1 = 11 with a "cannot be determined" distractor, 17 xy=6, yz=10, xz=15 → xyz = 30.

**Sizes:** practice goes from 51 to 51 (sections 14 / 10 / 27), plus 4 new guided questions. Each section is ordered easy → hard. About 16 items are now exam-level (new 07–10, 13–17, plus q-143, q-153, q-156, q-157, q-158, t6-1-4, t6-1-7).

## Notes and decisions for the teacher
- **Question numbers.** The numbers are locked, so the new guided questions are Q4 and Q5 (after Q1, in the single-equation section) and Q6 and Q7 (after Q2 and Q3, in the systems section). On screen, the order reads 1, 4, 5 and 2, 3, 6, 7. Renumber if you prefer, since nothing is recorded yet.
- **Topic 5 tip.** The Topic 5 review says the tip "answer = choice number sits in that slot" is contradicted by q-159, q-161, q-163, q-149 and q-150, which list 4, 3, 2, 1. I left those choice orders as they are (descending order is normal NITE style). This depends on the Topic 5 owner removing that tip.
- **x² before exponents.** The lesson example and Q7 use x² = 36 and x² = 100 (known squares, positive root given). Exponents are formally taught only in Topic 8. Check that this is acceptable.
- **Not done:** a guided example for q-157 (expanding (m+1)(n+1)). Expanding brackets is taught in Topics 4 and 5, so I kept it as an exam-level practice item with a full solution.
- **Tool limitation.** `tmp_check/view/t6.md` takes question text from the exported site (`content/full-course/topics/t6.json`), not from the patched data. The questions there still show the old text until the site is re-exported. The videos in that file do reflect the patch. I checked the questions with a direct dump of the patched data instead.

## Pass 2 (2026-09-27, teacher-approved remove/restore plan + summary lessons)
**Removed:** nothing (the plan keeps every addition, including q-r26-t06-15 and q-r26-t06-17).

**Restored:**
- 13 practice questions are back, cleaned up (TeX, "Given:" with stacked equations in `cases`, full numeric solutions), and placed easy to hard:
  - Single-equation practice: alg-extra-unit-t6-4-1, -4-2, -4-3, -4-5
  - Systems practice: alg-extra-unit-t6-2-1, -2-2, -2-5, -2-6, -2-7
  - Mixed practice: q-141, alg-extra-unit-t6-1-1, -1-2, -1-3
- q-156: the original choices One / Two / Seven / The equation has no solution (key: One).
- q-171: the original distractors 31 and 21 (the choices are 1, 31, 21, 2; key 1).
- Systems Recap: the board line is now "No match → multiply WHOLE equations to match coefficients". This brings back the original line "Multiply WHOLE equations to match coefficients".

**Summary lessons added (the topic is learn → practice → learn → practice, so there are two):**
- `r26-t06-summary`, "Summary: One Equation". It comes at the end of "Single equations", before the single-equation practice, and has 10 slides: Summary · Same on both sides · Brackets and fractions · Minus before a fraction · x cancels · x in the denominator · Cross-multiply · Don't divide by x · Test the choices · Before you practice.
- `r26-t06-summary-2`, "Summary: Systems of Equations". It comes at the end of "Systems of equations", before the systems practice, and has 8 slides: Summary · Two equations · Substitution · Add or subtract · Match coefficients · Ask what they want · Multiply equations · Before you practice.

**Small fix:** the title slides of the four new guided videos now keep the lesson name as the slide label. The big title still shows the number. Before this fix, renumbering changed the label twice, so a slide was labeled "Question 4" while its big title said "Question 2".

Check: `python3 math_check.py 5 6` gives 0 problems, 0 warnings for Topic 6 and 0 layout problems.
