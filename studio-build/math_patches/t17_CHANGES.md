# Topic 17 — The Number Line: changes (course review 2026-09)

Patch: `math_patches/t17.py`. Check: `python3 math_check.py 17` → 0 problems, 0 warnings, 0 layout problems.

## 1. Wrong or unclear rules fixed (priority 1)
- **Negative exponents now get the same message everywhere.** With the arrows, you keep the negative exponent (−1 is just a small power). Without the arrows (comparing ranges, or "same operation"), you flip it first. Both ways give the same answer.
  - Lesson 1, slide 6 (Exceptional powers): two new lines say when to flip and point ahead to the arrows.
  - Lesson 2, slide 7 (Three steps): the "No need to flip" line is replaced by the two-case rule.
  - Lesson 2 recap: new board line "Negative side: odd powers only · negative exponent: keep it".
  - Memory card: the tip "a negative exponent flips the base" now gives the two-case rule.
- **"Odd" is now defined for a negative base** (Lesson 2, slide 5, new board line "Odd: 3, 5, −1, −3, 1/3, 1/5"): any power that keeps the minus sign, including odd roots and negative odd powers. Lesson 2, slide 2 now says "Negative fractions: right — for odd powers." The same wording is on the card.
- **Hierarchy (Lesson 1, slide 5):** "ALWAYS bigger, whatever power or root" now says "after any positive power or root; for negatives, odd ones only", on the board and in the script.
- **Same operation (Lesson 1, slide 7):** now says "positive numbers only", with the counter-example −3 < −2 but (−3)² > (−2)² on the board. The card tip says the same.
- **Q8 (q-500), Method 2:** removed the invalid "replace every ten with a two" trick. New plug-in: x = 1/1024 = (1/2)¹⁰, which has a clean tenth root. Added a warning: change only x, never the numbers in the question.
- **Q3 (q-495) written solution:** replaced the wrong reason with a correct one (b·a² = ab·a, a·b² = ab·b, and a < b).
- Lesson 1, slide 4 and the card: "12 : 3" became "12 ÷ 3" (and "12 ÷ 1/3"). Slide 4 now ends by pointing ahead to multiplying by a negative number.
- Lesson 1 recap: board lines now include the conditions (positive powers and roots; flip a negative exponent; positive numbers only).
- The review's "broken board text" (four ranges) was an export artifact. The boards were fine, so nothing changed there.

## 2. Missing methods added (priority 2)
**New lesson video `r26-t17-reading-the-line`, "Reading the Number Line"** (8 slides, about 4.6 min). It is the first item of the advanced section, before Q3:
1. Times a negative: you land on the other side of zero and the order flips (2 < 5 → −2 > −5). A negative fraction times a number above 1 moves away from zero, so it gets smaller.
2. Reciprocals: the full table for the four ranges. For numbers with the same sign, the order flips (2 < x < 5 → 1/5 < 1/x < 1/2).
3. Test numbers: 2, 1/2, −1/2, −2, plus the borders −1, 0, 1 when they are allowed. "Nice numbers" for roots: 1/4, ±1/8, −1/32.
4. Must or could: for "necessarily", one counter-example is enough to rule it out, and you find one by pushing the values to the edges. For "could", one example is enough to prove it.
5. Picture questions: write the range under each letter. Unless the figure is "drawn to scale", trust only the order of the points, not the distances. The slide has a number-line figure.
6. Distance and midpoint: distance = bigger − smaller; midpoint = (a+b)/2; "a third of the way".
7. Recap.

**New memory card `mem-r26-t17-reading`** (after the new lesson): a reciprocal table, a table of numbers to plug in, and a distance and midpoint table, plus tips.
The existing card also got a new row: "× a negative number".

**Five new guided questions, each with a solution video** (Q10–Q14, at the end of the advanced section):
- Q10 `q-r26-t17-01`: picture with a, b, c, d. Which is necessarily negative? (Answer: choice 2, b·c·d.)
- Q11 `q-r26-t17-02`: picture with x and points K, L, M, N. Which point could be √x? (Answer: choice 3, M.)
- Q12 `q-r26-t17-03`: −4 < x < −2, find the range of 6/x. Reciprocals with negative numbers. (Answer: choice 3.) The video shows two methods.
- Q13 `q-r26-t17-04`: x < −1 < y < 0, which is necessarily true? The test at the edges shows xy can equal 1. (Answer: choice 2, x+y < −1.)
- Q14 `q-r26-t17-05`: a point one third of the way from −7 to 5. (Answer: choice 3, −3.)

The old Q9 video no longer says "That's the number line done". The sidebars of the advanced solution videos now list Questions 3–14.

## 3. Text (priority 3)
- All 9 guided and all remaining practice questions were rewritten in TeX: no ":" for division, spaces after commas, and no decimals like −0.794 that you can't work out by hand. The solutions now use nice numbers (t = −1/8, x = −1/32, x = 1/1024, and so on) and the methods taught in the lessons.
- Choices were cleaned up (for example "\left(r − q\right) < \left(s − p\right)" → "r − q < s − p"). The "orderings" stem of q-499 was reworded. q-503's exponent "−1/2" was fixed, and in the extra item t17-3-4 the impossible choice "1/2 < 1/x < 1/5" was replaced.
- q-504 (the gap a − b) is kept, now worded as a distance on the number line, so it fits the new distance slide. The review suggested moving it to T12 or T20.
- Video titles and slide notes now match the new stems.

## 4. Figures (priority 4)
- There were no figures in this topic before. There are now 6 new number-line SVGs in the course figure style (viewBox 640×160, axis #71818d, dots #087f83, labels #203344 in DejaVu Sans). They are used by 5 questions and 1 lesson slide. Only the order of the points matters, and every stem says "not drawn to scale". The renderer also adds its own "not drawn to scale" note.

## 5. Practice (priority 5)
- **Removed:** q-505 (Q3 turned around) and extra t17-3-1 (a one-step question).
- **Added 10 exam-level items:**
  - `-06`: picture, smallest of a, ab, a/b, a²
  - `-07`: picture, x/y − 1 is positive
  - `-08`: picture, which point could be x³
  - `-09`: reciprocal of −2 < x < −1/2
  - `-10`: range of 1 − 3x (a negative multiplier)
  - `-11`: x³ < x, border trap: −1, 1 and −1/2 all fail
  - `-12`: point twice as far from A as from B
  - `-13`: "could equal 1"
  - `-14`: 0 < x < 1 < y, counter-examples at the edges
  - `-15`: 1/a vs b/a vs 1/b
- The practice set is now ordered easy → hard. It has 25 items (was 17), and about 12 of them are exam level.

## Counts
- Questions: 23 rewritten, 15 added (5 guided + 10 practice), 2 removed.
- Slides: 9 changed (Lesson 1 slides 4, 5, 6, 7, 9; Lesson 2 slides 2, 5, 7, 9; Q8 slide 3; Q9 one line).
- Videos: 6 added (1 lesson + 5 solution videos).
- Cards: 1 updated, 1 new.
- Figures: 6 new.

## For the teacher to decide
- The new lesson comes before Q3, so Q4, Q5 and Q9 can use "must/could" and negative multipliers. If you prefer it after Q9, move `r26-t17-reading-the-line` and its card.
- Comparing powers with different bases (2³⁰ vs 3²⁰) is not repeated here. It is taught in the T10 patch.

## Pass 2 (teacher-approved plan, 2026-09-27)

### Part A: remove / restore
- **Removed:** nothing (the plan keeps every addition, including q-r26-t17-02 / -08, "which marked point could be √x / x³").
- **Restored (2 questions, 1 choice):**
  - q-505 (1 < m < n, which is the largest?) is back in the practice. Text in TeX, and the solution shows the numbers (m = 2, n = 4) and the "strong on strong" reason.
  - alg-extra-unit-t17-3-1 (−1 < x < 0, which is the largest?) is back in the practice, with a worked check (x = −1/2).
  - alg-extra-unit-t17-3-4: the original distractor "1/2 < 1/x < 1/5" is back as choice 2 (it replaces "−1/2 < 1/x < −1/5"). Key unchanged (choice 1).
- The practice order stays easy → hard: t17-3-1 goes in the easy group, q-505 in the middle (after q-503).
- No action (as planned): the "replace every ten with a two" fix in solve-q-500 and the q-503 fix stay.

### Part B: summary lesson
- New video `r26-t17-summary` "The Number Line: Summary" (about 3.5 minutes). It is the last item of "The number line · advanced study", right before the independent practice (this topic has one practice section, so one summary).
- Slides: Summary · Four ranges · Multiply & divide · Hierarchy · Exceptions first · The arrows · Reciprocals · Test numbers · Must or could? · Distance & midpoint · Before you practice.
- Content comes only from the two lessons and "Reading the Number Line". The final slide has these checks: which range, are the borders allowed · any exceptions · positive or negative (mirror, flip for times a negative) · necessarily or could. It also lists the common traps.
