# Topic 18 — Exercises with Letters: changes

Patch: `math_patches/t18.py`. Check: `python3 math_check.py 18` shows 0 problems, 0 warnings and 0 layout problems.
Every puzzle (old and new) was checked by computer search over all digits: each has exactly one correct choice.

## Summary
- Questions: 34 rewritten, 10 added (3 guided with solution videos and 7 practice), 2 removed.
  Before, the topic had 36 questions (9 guided and 27 practice). Now it has 44 (12 guided and 32 practice).
- Main lesson "Exercises with Letters": 7 slides changed and 1 slide added ("Carries"). It is now about 8.9 minutes long.
- New lesson video: "Number Facts for Letter Puzzles" (7 slides, about 3 minutes). It is the first item in the advanced section.
- New solution videos: Questions 10, 11 and 12.
- Existing solution videos changed: Q1, Q4, Q7, Q8 and Q9 (method 2 rewritten). The sidebar of the Q4–Q9 videos now lists Questions 4 to 12.
- Memory card "Exercises with letters — toolkit" updated. New card: "Number facts for letter puzzles".
- Figures: this topic has none.

## 1. Wrong or misleading teaching (fixed)
- **Lesson slide 4:** "B plus something equals B, so it's zero" is now "ends in B. Nothing carries into the ones column, so it's zero." A new last line says the rule is safe only in the ones column.
- **New slide 5 "Carries":** the carry from two numbers is 0 or 1. From three or four numbers it can be 2 or 3 (8 + 8 + 8 = 24). The trap example is 1X7 + Y5 = 2X2. The carry from the ones means Y = 9, not 0 (147 + 95 = 242). Rule on the board: in a middle column, "X + Y ends in X" means Y = 0 or Y = 9.
- **Leading-digit slide:** the rule is now "**two** numbers, more digits in the sum → leading digit 1". A new line and board item say that four three-digit numbers can reach 3996, so the leading digit can be 2 or 3 (q-527).
- **Q7 video:** deleted the confusing "With a five here we'd use the five-rule".
- **Q9 video, method 2:** the unclear "cube sits on the tens digit" sentence is gone. The method now really plugs in the choices: T = 3 → 30 + U = U³ + 3 + U → U³ = 27. The other choices give U³ = 45, 18, 36, and none of these is a cube.
- **Q1 and Q4 videos:** the "B = 0" step now says why: nothing carries into the ones column.
- **q-536 solution:** the false reason "any BB ≥ 22 makes these four-digit" is fixed. Now: 55 × 22 = 1210, 66 × 22 = 1452 and 77 × 22 = 1694 have four digits, and 33 × 11 = 363 works.
- **q-532 solution:** deleted the self-correction "621 and 226? No —".

## 2. Methods added
In the main lesson:
- **The 4 steps:** step 3 is now "Check the leftmost digit **and the size**" (estimate first). Step 4 is now "Plug in numbers — **or the choices**".
- **"What letters mean":** one line explains the bar: the letters under a bar are the digits of ONE number. Every question now uses the bar.
- **Plug-in slide:** a warning to use test numbers that are not alike, and to try a third number if two choices survive. A new board line: "Asked for one letter? Plug in the choices, from the middle one."
- **Minus → plus slide:** one line added: flip a division into a multiplication (used in Q7).
- **Algebraic-form slide:** says when to use each route. If a result is given, work the columns. For "always divisible by" with no result, plug in two numbers or use the algebraic form. This replaces "plugging in is faster most of the time".
- **Recap** updated to match.

The **new lesson video "Number Facts for Letter Puzzles"** covers:
1. Repdigits: AA = 11A, AAA = 111A = 3·37·A, BBBB ÷ BB = 101 (used in Q5, Q7, q-539 and the extras).
2. Reversals: AB ± BA, ABC − CBA = 99(A − C). Multiples of 99 have middle digit 9, and their outer digits add up to 9 (q-532).
3. Products: only the ones digits decide the ones digit. Digit count of a product = the two counts added, or one fewer. Estimating squares.
4. Ones digits of powers repeat in a cycle (2, 4, 8, 6 …). Example: 2⁵⁰ ends in 4.
5. Largest and smallest number with a given digit sum (q-529).
6. Recap.

New guided questions (end of the advanced section), each with a solution video:
- **Q10 (q-r26-t18-01)** 2A6 + B8 = 3A4, B = ? → 9. Carry trap: the distractor is 0.
- **Q11 (q-r26-t18-02)** Which could be ABC − CBA? → 495 (the multiple of 99).
- **Q12 (q-r26-t18-03)** Which could be A3 × B7? → 851. Solved with the ones digit (ends in 1) and the size (221 to 9021).

## 3. Text (all questions)
- Every stem now uses the standard form "A, B and C represent digits. Given: $\overline{AB}+…$". The bar is used everywhere. The long notes in parentheses ("each letter being the digit in that position", "literally 6", "repdigit") are gone. "Units digit" is now "ones digit", as in the lesson.
- Q3: "necessarily divisible by —" is now "Which of the following necessarily divides AB + BA?", with "nonzero digits" (BA must be a two-digit number).
- Q8: "distinct prime digits (i.e. …)" is now "different digits, and each of them is a prime number".
- All written solutions are rewritten in TeX with the numbers shown. They use the method the lesson teaches (columns, carries, plugging in the choices). The algebraic form comes after that when it helps. The review listed the heavy algebra in q-522, q-525, q-530, q-533, q-534 and q-540. It is now replaced:
  - q-540: flip to BA + B3 = 1AB. Ones: B = A + 3. Plug in the choices.
  - q-534: flip. The tens column needs a carry, so A = B + 2 and C = B − 2.
  - q-533: the tens need a carry, so A = B + 1. Then A = 9.
  - q-522: the ones column gives 2B ending in 0, so B = 5.
  - q-525: B·B ends in 4, and B = 8 is too big.
  - q-530: plug in the choices.
- No ":" for division is left (it was in q-533, q-539 and extra 2). The checker shows no missing spaces after commas.
- Solution-video titles now match the new stems. Spelling: "organised" is now "organized".

## 4. Practice
- **Removed:** extra t18-3-1 (a near-copy of q-524: reverse, 27 smaller). Also extra t18-3-4 (a counting question: that method is taught in T28, which comes later).
- **Rewritten extras:**
  - Extra 2 no longer asks for a ratio A:B, because ratios are taught later. It now asks for A + B (answer 9, by plugging in the choices).
  - Extra 7 is now "$\overline{4A}+\overline{4A}=\overline{9B}$, smallest possible A" (5), solved with the carry.
- **New practice (exam level):**
  - q-r26-t18-04: A8 + A8 + A8 = 1A4, a carry of 2 → A = 4. The trap choice is 9.
  - q-r26-t18-05: 4AB + CB = 5A0 → B + C = 14 (the carry makes C = 9).
  - q-r26-t18-06: digits of a (three-digit) × (two-digit) product → 4 or 5.
  - q-r26-t18-07: ones digit of A7 × B3 × C9 → 9. The trap choice is "cannot be determined".
  - q-r26-t18-08: ones digit of 2⁵⁰ → 4.
  - q-r26-t18-09: AAA ÷ 37 = 1A → A = 5.
  - q-r26-t18-10: ABC − CBA = 693 and B = A + C (stacked conditions) → 891.
- **Order:** the practice section now goes from easy (ones digit of 38 × 47, digits of a sum) to exam-hard. The last items are q-r26-t18-05, q-r26-t18-04, q-536, q-537, q-r26-t18-10 and q-540.

## For the teacher to decide
- **q-537 (remainders, T15) and q-538 (primes, T14)** stay as mixed review, because those topics come before T18.
- **Ones digit of powers (cycles)** is now taught here, on one slide with one practice question. If the T15 patch also teaches it, one of the two can be cut.
- **Guided question order:** the three new guided questions (10–12) are at the end of the advanced section, so Questions 4–9 keep their numbers. Q10 (carry) could also go into the theory section right after Q3.
- The API had no function for the sidebar "active" index of existing slides. After inserting the Carries slide, the patch shifts those indexes directly on the slide data.

## Pass 2 (teacher-approved plan, 2026-09-27)

### Part A: remove / restore
- **Removed:** nothing. The plan keeps the "Powers: ones digit" slide, its card row and tip, q-r26-t18-08 and q-r26-t18-06.
- **Restored (4 originals):**
  - alg-extra-unit-t18-3-1 (digit sum 11, the reversal is 27 smaller; the answer is 74). It is back in the practice. The solution uses stacked givens (cases), 9(A − B) = 27, and a check.
  - alg-extra-unit-t18-3-2: the original question is back: "What is the ratio A : B?", with choices 2:3, 5:4, 4:5, 3:2 and key 5:4 (10A + B = 6A + 6B → 4A = 5B). The A + B version is dropped.
  - alg-extra-unit-t18-3-7: the original wording "What must A be at least?" is back. Choices and key are unchanged (5).
  - alg-extra-unit-t18-3-4 (three-digit numbers from 2, 5, 8 with no repeats; the answer is 6): restored and **moved to the T28 practice** (`wp28-practice`, topic 28), placed before its first question. The T28 patch runs later and its `practice_order` does not list this id, so for now it ends up LAST in the T28 practice. The T28 owner should add it to the easy group of that order.
- The T18 practice order stays easy → hard: t18-3-1 goes next to q-524, which uses the same 9(A − B) fact.

### Part B: summary lesson
- New video `r26-t18-summary` "Letter Puzzles: Summary" (about 3 minutes). It is the last item of "Digit puzzles · advanced study", right before the independent practice (one practice section, so one summary).
- Slides: Summary · Letters are digits · The 4 steps · The ones column · Leading digit & size · Special digits · Plug in · Algebraic form · Products & powers · Largest & smallest · Before you practice.
- Content comes only from the main lesson and "Number Facts". The final slide has these checks: must the letters be different · which column, is there a carry · how many numbers are added, does the size fit · one letter asked → plug in the choices. It also lists the traps: a forgotten carry, a leading zero, "leading digit 1" used with more than two numbers, and a matching last digit taken as proof.

## 2026-10-05 cut repeats
Function `cut_repeats` (runs last). Nothing in topic 18 is recorded.
- **`digit-puzzles` "Exercises with Letters"** → the Hebrew intro: 8.9 → 1.8 min. Kept: title, "The 4 steps", "What letters mean" (the Hebrew intro explains both). Each question then teaches one more tool.
  - Cut "The 4 steps in action" → Q1 `solve-q-512` runs the same four steps.
  - Cut "Carries" (its 1X7 + Y5 example was the same as Q10) → Q10 `solve-q-r26-t18-01` teaches the middle-column carry; added "in a middle column: zero or nine; two numbers carry at most one, three or four can carry two or three" + board item.
  - Cut "Leading digit" → taught in Q1; added the why (99 + 99 = 198) and the limit (only for two numbers) + board item.
  - Cut "Special digits" → taught in Q2 `solve-q-513`; added the 5 × even / odd and 6 × even facts + board item; "Remember the special digits?" reworded.
  - Cut "Plug in numbers" → taught in Q3 `solve-q-514` (51, 52; AB ± BA). "Plug in the choices from the middle" → one line in Q8 `solve-q-519`.
  - Cut "Minus → plus" → taught in Q5 `solve-q-516` and Q7 `solve-q-518`.
  - Cut "Algebraic form" → taught in Q3 method 2 and Q9; added ABC = 100A + 10B + C in Q3 + board item.
  - Cut "Recap".
- **`r26-t18-facts` "Number Facts for Letter Puzzles"**: 3.2 → 2.0 min. Kept: repdigits, powers' ones digit, largest/smallest (no question teaches them).
  - Cut "Reversals" → taught in Q11 `solve-q-r26-t18-02`; added the why (algebraic form, the middle digit cancels) + board item.
  - Cut "Products" → taught in Q12 `solve-q-r26-t18-03` (ones digit; 3 or 4 digits).
  - Cut "Recap".
- Cards unchanged.

## 2026-10-06 new exam methods
Function `add_methods` (runs last, after `cut_repeats`). Nothing in topic 18 is recorded.
- Digit WORD equations join the 4-step routine: "Words, no columns? Write 10A + B and collect: 10A + B = 4(A + B) → 6A = 3B → B = 2A: 12, 24, 36, 48" (checked: exactly these four two-digit numbers).
  - Lesson "Exercises with Letters", slide 2: board line + 4 spoken lines after step 4 (1.8 → 2.4 min).
  - Summary, slide "The 4 steps": the same board line + one spoken line.
  - Card "Exercises with letters — toolkit", table "The four steps": new row "Words, no columns".
  - Question 9 (q-520, already solved with 10T + U): one line naming the move before "Cancel U from both sides".
