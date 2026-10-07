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

## 2026-10-02 new numbers + order
Functions `new_numbers(M)` and `order_changes(M)` run last. `RECORDED = set()` (nothing in Topic 6 is recorded). Same ideas, same traps, same methods. Every item was re-solved in Python, and each has exactly one correct choice.

**Guided questions (the videos were rewritten with the new numbers: board, spoken numbers, circle-choice lines and titles)**
| Q | Hebrew / study guide | New | Key |
|---|---|---|---|
| 1 q-171 | 2/(x−2) = 1/(x−1) → 0; study guide 3/(x−4) = 1/(x−2) → 1 | 4/(x−2) = 3/(x−3) → 6. Choices −1 (straight-across trap), 6, 18 (sign slip), 3 (forbidden). Common denominator, cross-multiply note, test the choices | 2 |
| 4 q-164 | 6x+3y = 27, x+y = 5; study guide 36 / 7 | 8x+4y = 44, x+y = 9 → x = 2. Isolate y (they ask for x); divide by 4, then subtract. New trap line: 11 is 2x+y | 2 |
| 5 q-165 | 3x+y = 25, 2x+3y = 33; study guide 2x+y = 19, 3x+2y = 31 | 4x+y = 22, 3x+2y = 24 → x = 4. ×2 to match y; "could match x: ×3 and ×4 → 12x"; substitution check. Trap 20 = 5x | 3 |

**Practice:**
- q-166: 3x+11 = 2
- q-167: 5(4−x) = 2(x−4) (both sides are 0 again)
- q-168: 3(x−2)/7 = 3
- q-169: (12x+8)/4 = (6x+4)/2 → any number (now choice 4)
- q-170: 9(x+2)/3 = 3x+4 → no value (now choice 4)
- q-159: 5x+3y = −1, x = −2
- q-160: x+2y = 16, x+y = 9, asks for y
- q-161: 3x−3y = 0, 2x+y = 9
- q-162: x+y = 30, x−y = 8
- q-163: 3(x−1)−2y = 6+y, x+y = 7
- q-139: 3x−8 = 2x+5
- q-140: 4(x−3) = 20
- q-141: (x+5)/2 = 7
- q-142: (5x+10)/5 = 6
- q-143: (4x+2)/5 − (x+2)/3 = (2x+8)/10 → 4 (sign trap −1)
- q-144: 5x+y = 38, y = 3
- q-145: x+3y = 17, 3x = 6
- q-146: 3x+y = 19, x−y = 1
- q-147: x+4y = 18, x+y = 6
- q-148: x+y = 22, x−y = 6
- q-149: 2x+5y = 24, 3x−y = 2
- q-150: 3x+5y = 29, 2x+10y = 46
- q-151: 2x+3y = 4, 3x−2y = 19
- q-152: (1/x)/4 = 2
- q-153: xy = 32, x/y = 2
- q-154: 1/(x+2) = 3/(x+4) → −1
- q-155: x² = 2y, y = 5x
- q-156: 4x = 9x (choices: no solution / One / Two / Nine)
- q-157: (a+1)(b+1) = 6, ab = −4 → 9
- q-158: ((x−3)−(3−x))/(2+x) = 1 → 8

The new choice sets give correct-answer positions that differ from the original ones. Solutions now name the traps.

**newExtension:** alg-extra-unit-t6-4-1 was 2x−5 = 1, a near-copy of the Hebrew lesson example 2x−5 = 3. It is now 3x−4 = 11.

**Lesson "Equations — Fundamentals":**
- The Hebrew's own "every x / no solution" pair (2(x+3) = 2x+6 / 2x+9) is now 5(x+2) = 5x+7 (no solution) and 5(x+2) = 5x+10 (every x).
- The "Fractions & brackets" example (x+3)/4 = 5 was the Hebrew practice q-141. It is now (x−4)/5 = 3 ("not x minus twenty").
- The memory-card row was updated to match.

**Order changes:**
- Lesson: "No solution" now comes before "Every x works". The sidebar, the recap line, the summary slide "x cancels" and the card row follow the same order.
- Guided questions after lesson 1: q-171 (cross-multiply) → q-r26-t06-02 (forbidden answer) → q-r26-t06-01 (minus before a fraction). This is the lesson's own slide order and goes easy → hard. The automatic renumbering makes them Questions 1, 2, 3.
- Rejected:
  - Swapping q-164 and q-165. Substitution is taught first, and q-164 is the easier one.
  - Swapping the substitution and elimination slides. The elimination slide says "same answer as substitution".
  - Reordering the practice sections. They are already easy → hard.

Check: `python3 math_check.py 6 32` → 0 problems, 0 warnings, 0 layout problems. I rendered the changed videos and checked them.

## 2026-10-02 review
- Fixed q-169: (12x+8)/4 = (6x+4)/2 is true for every x, so the old number choices 0, 2 and 4 were also correct. The stem is now "Which of the following statements is true?". The choices are: only x = 0 / only x = 2 / no value of x / every value of x (key 4). A trap line was added to the solution.
- Checked with no changes needed: the guided questions q-171, q-r26-t06-02, q-r26-t06-01, q-164 and q-165 (Hebrew methods plus a second method each, all re-solved), all the lesson examples, the order changes, and more than 25 practice questions. q-157 (a+b = 9 with no whole-number a and b) is fine as an expression question, and the Hebrew/study-guide version had the same property.


## 2026-10-04 question = lesson example fixed
- alg-extra-unit-t6-2-1 was the system of "systems" slide 6 -> now 2x + 3y = 13, 3x + 2y = 17; x = 5 (choice 2). The solution makes the y terms cancel, as the lesson advises.
- alg-extra-unit-t6-1-6 was x(x − 5) = 0 of "linear-equations" slide 10 -> now x(x + 4) = 0; sum of solutions −4 (choice 1).


## 2026-10-05 pen vs clicks trial
"Pen for the thinking, clicks for the copying" (function `pen_or_click`, runs last). Copied / mechanical lines that the teacher used to write by hand now appear on NEXT as board items, in the same place in the script. The key idea and all marks (circle, underline) stay as pen cues. Where a hand-written line comes before a click line, the board leaves an empty row for it. Spoken lines, math, questions and slide count are unchanged.
- solve-q-r26-t06-03 (9 pen cues -> 4 by hand, 5 clicks). By hand: circle "x + y", 8(x + y) = 80 -> x + y = 10, circle choice 3 (twice). Clicks: (5x + 3y) + (3x + 5y) = 41 + 39, 8x + 8y = 80, the ×3 / ×5 equations (stacked), 16y = 72 -> y = 4.5, 5x + 13.5 = 41 -> x = 5.5 -> x + y = 10.
- solve-q-r26-t06-04 (7 pen cues -> 2 by hand, 3 clicks, 2 split). By hand: xy · (x/y) = 20 · 5 (method 1 key), x/y = 5 -> x = 5y (method 2 key). Clicks: x² = 100 -> x = 10, 10y = 20 -> y = 2, 5y · y = 20 -> y² = 4 -> y = 2. Split: "x − y = 10 − 2 = 8" and "x = 10, x − y = 8" are clicks; circling choice 3 stays by hand. Slide 2 items are a bit smaller (size 38) so the board is not crowded.


## 2026-10-06 practice: new methods
Function `practice_methods` (runs last; append only). 2 practice questions, "Shortcut: pick values that fit" (taught later in topic 51, so phrased as a shortcut with a one-line why).
- q-r26-t06-16 (3x − 2y = 5, 6x − 4y + 1): y = 0 → x = 5/3 → 11; second set x = 1, y = −1 → 11 again, so "cannot be determined" is out.
- q-r26-t06-14 ((x + y)/(x − y) = 3, x/y): y = 1 (y ≠ 0) → x = 2 → 2.
All new lines verified numerically (python: fitting values, choice values, power by scaling). `math_check.py 6 32`: PROBLEMS 0, WARNINGS 0, LAYOUT 0.

## 2026-10-06 Hebrew back-check
All guided and practice questions, the two lessons, the cards and both summaries of Topic 6 were compared with the
teacher's Hebrew video subtitles (lines 3666–3894: 2x − 5 = 3, 2x² + 6 = 2(x² + 3), 4x − 5 = 2x + 2(x − 3),
2/(x − 2) = 1/(x − 1), 6x + 3y = 27 & x + y = 5, 3x + y = 25 & 2x + 3y = 33; also skimmed the equation sample questions
in lines 3895–4790 for practice look-alikes). No matches (recorded or not): every item already uses other numbers.
Nothing changed. `python3 math_check.py 6 32` → 0 / 0 / 0.

## 2026-10-07 practice clean-up
Function `practice_cleanup` (runs LAST, after `practice_methods`). Teacher-approved. Practice **64 → 36**, still three
sections, each easy → hard: Single-equation practice 18 → 5 (q-166 … q-170), Systems practice 15 → 7 (q-159 … q-163 +
alg-extra-unit-t6-2-3 x + y, -2-4 x − y by adding/subtracting the equations), Mixed equation practice 31 → 24 (the other
20 Hebrew + alg-extra-unit-t6-1-7 (5 − k)x = 7 no solution + review q-r26-t06-16 (3x − 2y = 5 → 6x − 4y + 1), -14
((x + y)/(x − y) = 3 → x/y), -17 (xy, yz, xz → xyz)). All 30 Hebrew kept. Their "Method 2" lines (PRACTICE_METHODS:
q-r26-t06-16, -14) stay with them. No guided question, lesson, video or card changed.

| removed | why |
|---|---|
| alg-extra-unit-t6-4-1, -4-2, -4-5, -1-1 | copies: one-step linear equations = Hebrew q-166 / q-140 / q-141 / q-139 |
| alg-extra-unit-t6-4-7 | copy of alg-extra-unit-t6-1-5 (= Hebrew q-154) |
| alg-extra-unit-t6-1-2 | copy: x + y = 13, x − y = 3 = Hebrew q-148 |
| alg-extra-unit-t6-1-3 | copy of alg-extra-unit-t6-2-3 |
| alg-extra-unit-t6-2-1, -2-2, -2-5, -2-6, -2-7 | copies: the same 2x + 3y / 3x + 2y system five more times |
| q-r26-t06-11 | copy: x + y = 15, x − y = −3 = Hebrew q-162 |
| alg-extra-unit-t6-4-3, -4-4, -4-6 | extra over 3: linear equations = Hebrew q-141 / q-139 / q-140 |
| alg-extra-unit-t6-1-4 | extra over 3: x + y, xy → x² + y² = topic 4 guided q-r26-t04-01 |
| alg-extra-unit-t6-1-5 | extra over 3: (x − 5)/(x + 7) = 1/2 = Hebrew q-154 |
| alg-extra-unit-t6-1-6 | extra over 3: x(x + 4) = 0 is topic 7 (product = 0) |
| q-r26-t06-05 | review: 5/(x + 2) = 3/(x − 2) = Hebrew q-154 / guided q-171 |
| q-r26-t06-06 | review: x/2 − (x − 6)/4 = 3 = Hebrew q-143 / guided q-r26-t06-01 |
| q-r26-t06-07 | review: 12/x = x + 1 is a quadratic in disguise (x² + x − 12 = 0, not exam material) |
| q-r26-t06-08 | review: parameter, infinitely many solutions = Hebrew q-169 / q-170 (kept (5 − k)x = 7) |
| q-r26-t06-09 | review: no solution (domain) = guided q-r26-t06-02, Hebrew q-170 |
| q-r26-t06-10 | review: three-fraction equation = Hebrew q-143 |
| q-r26-t06-12 | review: 2x + y from a system = kept alg-extra-unit-t6-2-3 / -2-4, guided q-r26-t06-03 |
| q-r26-t06-13 | review: divide the equations = Hebrew q-153, guided q-r26-t06-04 |
| q-r26-t06-15 | review: (x − 1)/(x − 1) = 1, how many solutions = Hebrew q-156 / q-169, guided q-r26-t06-02 |

`python3 math_check.py 3 4 5 6 8 32` → 0 / 0 / 0.
