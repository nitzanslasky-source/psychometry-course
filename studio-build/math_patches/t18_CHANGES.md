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


## 2026-10-06 practice: new methods
Function `practice_methods` (runs last; append only). 2 practice questions, Method 2 · Words, no columns (10A + B, collect).
- alg-extra-unit-t18-3-6: 10A + B = 4(A + B) → B = 2A → tens 2 → ones 4.
- q-530: 50 + A = 3(10A + 7) → A = 1 → X = 15, digit sum 6 (checked: the only solution).
All new lines verified numerically (python: fitting values, choice values, power by scaling). `math_check.py 18 32`: PROBLEMS 0, WARNINGS 0, LAYOUT 0.

## 2026-10-06 renumber pass
So the English course does not look like the Hebrew one: every Hebrew-derived question has new numbers or letters.
The idea, the trap, the level and the methods stay the same, and every guided solution video is rewritten to match
(board, speech, draw cues, video title, slide description). Nothing in Topic 18 is recorded (no take in
~/Documents/Course.recordings), so nothing had to be kept. Function `renumber_pass(M)` in t18.py runs last.

**Counts:** 9 guided questions renumbered (q-512 … q-520) with their 9 solution videos rewritten; 20 practice questions
renumbered (q-521 … q-540) + 1 kept warm-up (X6, it was the lesson's own example); lesson examples: "Exercises with
Letters" slides 1 and 3 (32 + 57 → 46 + 38, 23 → 47), toolkit card (27 → 47), number-facts card (52 ± 25 → 73 ± 37,
521 − 125 → 412 − 214, tip 24²/27² → 23²/28²). Practice: 33 → 25.
Kept on purpose: the English-made guided Q10–12, the "Number Facts" lesson and the summary (their examples do not equal
any question now), September items q-r26-t18-04 (three-number carry) and -07 (units digit of a product) — types the
Hebrew practice does not have. Letter-only questions (q-512, q-515, q-523, q-531, q-533) got moved letters and a new
choice order, as allowed.

**Removed from practice (8):** copies alg-extra-…-1 (same 9(A − B) = 27 as q-524) and q-r26-t18-08 (2⁵⁰ = the facts
lesson's worked example); extra warm-ups beyond 3: alg-extra-…-2 (same type as X6), alg-extra-…-3 (same type as -07);
September items whose type the Hebrew practice has: -05 (middle column → 9: q-534, q-540), -06 (how many digits:
q-521), -09 (AAA ÷ 37: q-539 repdigits, and = the lesson's 555 = 37·15), -10 (ABC − CBA: q-532).
Kept warm-ups: X5 (AAA ÷ 37), X6, X7. Order: easy → hard.

**Old → new (id · old · new · answer)**
| id | old | new | answer |
|---|---|---|---|
| q-512 (G1) | AB + CB = DDB, A+C+D | BA + DA = CCA, B+C+D (check 30 + 80 = 110) | 12, choice 4 |
| q-513 (G2) | BA × A = CA, A? (16·6 = 96) | CB × B = AB, B? (15·5 = 75); choices 4, 0, 5, 7 | 5, choice 3 |
| q-514 (G3) | AB + BA divisible by 9/6/11/4; tests 51, 52 | choices 3/11/4/10; tests 71 + 17 = 88, 72 + 27 = 99; algebraic form | 11, choice 2 |
| q-515 (G4) | ABC + AB = CCC, B? (202 + 20) | BCA + BC = AAA, C? (303 + 30 = 333) | 0, choice 1 |
| q-516 (G5) | AAA − 37 = BC → 74 | AAA − 46 = BC → 111 − 46 = 65 | B+C = AA, choice 3 |
| q-517 (G6) | AB² = 6CB, B−A could be (26² = 676) | AB² = 2CB (15² = 225 → 4 not offered, 16² = 256); choices 6, 5, 7, 8; both methods | 5, choice 2 |
| q-518 (G7) | CBA ÷ AA = 13 → 55·13 = 715 | CBA ÷ AA = 17 → 7A ends in A → A = 5, 55·17 = 935 | 17, choice 1 |
| q-519 (G8) | primes, AC + CD = BA (52 + 23 = 75), C = 2 | primes, AB + BC = CD (32 + 25 = 57), C? choices 7, 3, 5, 2; plug in + rule out | 5, choice 3 |
| q-520 (G9) | x = U³ + digit sum → 33 | x = U³ + 4·digit sum → 6T = U³ + 3U → 63; algebra + plug in | 6, choice 4 |
| q-521 | 2-digit + 4-digit → 4 or 5 digits | 3-digit + 5-digit → 5 or 6 digits | choice 2 |
| q-522 | AB × 2 = 1B0 | AB × 6 = 4B0 (75 × 6 = 450) | A−B = 2, choice 3 |
| q-523 | A<B<C, A+B+C = 1B | X<Y<Z, X+Y+Z = 1Y, new choice order | 15, choice 3 |
| q-524 | AB − BA = 27 | AB − BA = 45 | 5, choice 2 |
| q-525 | AB × B = B4 (12·2) | AB × B = B9 (13·3; trap B = 7) | 4, choice 2 |
| q-526 | ABC + CCC = D00 (345 + 555) | ABC + AAA = D00 (456 + 444 = 900) | A = 4, choice 3 |
| q-527 | four 3-digit numbers → 3 | five 3-digit numbers (≤ 4995) → 4 | choice 3 |
| q-528 | k = AB + CD + 31 | k = AB + CD + 53 = 11(2A + 7); tests 99, 121 | 11, choice 3 |
| q-529 | digit sum 8: 800 − 107 | digit sum 9: 900 − 108 | 792, choice 3 |
| q-530 | ones 5, reversal = 3(X + 2) → 15 | ones 8, reversal = 3(X + 9) → 18 (Method 2 line updated) | 9, choice 2 |
| q-531 | (AC + CB + BA)/(A+B+C) | (BA + CB + AC)/(A+B+C), new order | 11, choice 3 |
| q-532 | hundreds 4 more → 396 | 7 more → 693 (841 − 148) | choice 2 |
| q-533 | BA + A = AB, A = 9 | AB + B = BA, B = 9 (89 + 9 = 98) | choice 2 |
| q-534 | ABC − BBB = 198 → 4 | ABC − BBB = 297 → 6 (444 + 297 = 741) | choice 2 |
| q-535 | 1A × B = 9B → 9 | 1A × B = 8B → 7 (17·5 = 85) | choice 3 |
| q-536 | AA × BB = ACA → 33 | → 44 (44·11 = 484); choices 55, 44, 88, 66 | choice 2 |
| q-537 | digits 1–7, remainder < 3 → 7 | digits 1–8, remainder < 4 → 8 | choice 2 |
| q-538 | digit sum = 4 × ones → 31 | = 5 × ones → 41 (82 not prime) | 5, choice 2 |
| q-539 | BBBB ÷ BB = A0A (101) | BBBBBB ÷ BBB = A00A (1001) | 1, choice 3 |
| q-540 | 1AB − BA = B3 (147 − 74) | 1AB − BA = B2 (168 − 86 = 82) | 14, choice 2 |
| alg-extra-…-6 | 4 × digit sum, tens 2 → 24 (= lesson example) | 7 × digit sum, tens 6 → 63 | 3, choice 2 |

**Checks:** every column puzzle brute-forced over all digit assignments (leading digits nonzero, "different" and "prime"
conditions applied): each "= ?" question has one forced value and exactly one choice matches; each "could be" question has
exactly one choice among the possible values; "necessarily divides" checked over all digits. Every video step redone
with the new numbers; no old number left in the solution videos. Duplicate check over topics 1–18: no topic-18 question
equals another question; no question equals a lesson or card example. `python3 math_check.py 18 32` → PROBLEMS 0,
WARNINGS 0, LAYOUT 0; all 9 rewritten videos and the lesson rendered and looked at.

## 2026-10-06 review (of the renumber pass)
Brute-forced all 29 renumbered items over every digit assignment: each key is the only matching choice, traps kept.
Videos and lesson/card examples checked. No changes. Judgment calls (kept): q-520 now "U³ + 4 × digit sum" (with
multiplier 1 the only solution is the Hebrew 33, so a new number needs a multiplier; 4 is the only one with a clean
single answer); q-519 and q-526 changed the letter pattern (the Hebrew patterns have one unique solution each, so new
numbers need a new pattern); q-538 now has one non-prime candidate (82) instead of two.

## 2026-10-06 Hebrew back-check
Every guided/practice question, lesson slide and card of Topic 18 was compared with the teacher's Hebrew video subtitles
(01-Algebra-Original-Subtitles.txt, lines 18204–18764). Nothing in Topic 18 is recorded. Fixes in `hebrew_backcheck(M)`
(runs last). Keys brute-forced; traps and methods kept; `python3 math_check.py 18 32` → 0 / 0 / 0; videos rendered.

| id | Hebrew (subtitles) | was | new | answer |
|---|---|---|---|---|
| q-517 | AB·AB = 2CB, B−A? choices 5–8, 15² = 225 / 16² = 256 | identical (renumber had moved base 6CB onto it) | $\overline{CA}\cdot\overline{CA}=\overline{6BA}$, $A-C$? choices 6, 2, 4, 5; 25² = 625 gives 3 (not offered), 26² = 676 gives 4; insight method: A ∈ {5, 6}, 20² < 6xx < 30² → C = 2 | 4 (3) |
| q-513 | lesson example BA·A = CA, value of A (5) | CB·B = AB (letters renamed), 15·5 = 75 | $\overline{CB}\cdot B=\overline{ACB}$, choices 7, 5, 0, 4; 25·5 = 125; "six times fourteen, eighty-four" in the video | 5 (2) |
| card mem-letters | "08 → 8", 5 + 0 = 5, 5·4 = 20, 5·7 = 35, 6·8 = 48 | same examples | 07 → 7, 4 + 0 = 4, 5·8 = 40, 5·9 = 45, 6·14 = 84 | — |
| summary #6 | 15² = 225, 16² = 256 (Hebrew sample question) | same | 35·35 = 1225, 46·46 = 2116 | — |

Left: q-512 (AB+AD=CDB → BA+DA=CCA, other answer), q-514 (AB−BA → AB+BA, tests 71/72), q-515 (ABC−AB=CC → BCA+BC=AAA),
q-516 (AAA−55=BC → AAA−46=BC; B+C = AA = 11 is forced by the letter choices), q-518 (÷15 → ÷17), q-519 (Hebrew
AC+CB=DA, 52+23=75, A = 5 → ours AB+BC=CD, 32+25=57, C = 5; the digits 2, 3, 5, 7 are forced by "prime digits"),
q-520 (tens³ + digit sum → units³ + 4·digit sum, tens digit 6): numbers or layout already different.
Note: new q-517 is close to base-v18's own version (6CB, B−A, 25/26) with other letters and choices — hundreds digit 6 is
the only one besides 2 where two special-digit squares exist.


## 2026-10-07 methods spread
Function `spread_methods` (runs last; append only; a recorded video is skipped at build time). Nothing in topic 18 is recorded.
- **Method 2 · Write 10A + B and collect** (the "Words, no columns" move, used here on column puzzles where it is as fast or faster) — written line in 6 questions, each checked by brute force over all digits:
  q-r26-t18-01 (10A cancels → 10B = 90 → B = 9), q-533 (9A = 8B → A = 8, B = 9), q-535 (B(A + 9) = 80 → A = 7; A = 1 also fits but is not a choice), q-r26-t18-04 (20A = 80 → A = 4), alg-extra-unit-t18-3-7 (2A = 10 + B → A ≥ 5), q-526 (222A + 12 is a whole hundred → A = 4).
- **Video solve-q-r26-t18-01** (Question 10): new last slide 4 "Method 2 · Write 10A + B and collect" — two click lines (206 + 10A + 10B + 8 = 304 + 10A; 10B = 90 → B = 9), pen only to circle choice 4. About +0.3 min.
- Skipped (already shown): q-520, q-530, alg-extra-unit-t18-3-6 (words, no columns), q-514, q-524, q-531, q-532, q-528, q-r26-t18-02, q-523 (already algebraic). Power count / tag it: no fitting question.


## 2026-10-07 trim added repeats

Teacher: only OUR additions that re-teach something learned earlier in the study plan are trimmed; the Hebrew course's own repeats stay. `trim_added_repeats(M)` runs last in apply(); helpers in `_trim_repeats.py` (videos with a take recorded before its CUTOFF are left as recorded). Notes updated in added_notes.json.

- r26-t18-facts: slide 'Powers: ones digit' removed (topics 21 and 15); 'Three' → 'Two' facts + one reminder line. ~29 s.

## 2026-10-08 Hebrew points restored
Function `hebrew_points_back` (runs LAST; helpers `math_patches/_hebrew_back.py`, a video with a take recorded before its
CUTOFF is left as recorded and the point goes to the written solution instead). Rule: cut repeats, never content. The
teacher's Hebrew lesson (01-Algebra-Original-Subtitles.txt, lines 18204-18451) has 11 teaching points; 7 are still taught
(4 steps, letters = digits / not a product / different digits, units column → 0, more digits → leading 1 + why 99 + 99,
special digits 0 1 5 6 with the 5 and 6 facts, plug in two neighbouring numbers, minus → plus, algebraic form). The
advanced section has no Hebrew lesson ("Number Facts for Letter Puzzles" is ours) - nothing to restore there.
Nothing in topic 18 is recorded. Lost and restored (spoken lines only, no board change):
- **`digit-puzzles` "The 4 steps"** (+≈19 s): every letter question can be solved by plugging in; a computer would try every option - we're not computers, so steps 1-3 are shortcuts that tell us what we no longer need to plug in.
- **`digit-puzzles` "What letters mean"** (+≈10 s): the leftmost digit is never zero - nobody writes oh-six, it's not a phone area code (the board showed A ∈ {1…9} but it was never said; first said in the advanced lesson).
- **`solve-q-514` "Plug in numbers"** (+≈4 s): the AB + BA / AB − BA pattern comes back on the exam - worth remembering.
- **`solve-q-514` "Algebraic form"** (+≈13 s): the teacher's advice on the route - strong math students like the algebraic form; on the exam two quick numbers are usually faster.
Lesson 2.4 → 2.9 min, q-514 1.0 → 1.3 min. Notes: added_notes.json "lines".
`math_check.py 18 32`: PROBLEMS 0, WARNINGS 0, LAYOUT 0. Rendered and looked at.
