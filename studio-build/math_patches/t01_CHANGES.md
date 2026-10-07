# Topic 1: Algebraic Fundamentals. Changes (course review 2026-09)

Patch: `math_patches/t01.py`. Check: `python3 math_check.py 1` gives 0 problems, 0 warnings and 0 layout problems.

## Summary
- Questions: 51 rewritten (all remaining Topic 1 questions), 24 added (4 of them guided, each with a solution video), 3 removed, 3 moved.
- Videos: 2 new lesson videos, 5 new solution videos, 3 new slides in existing lessons, 20 existing slides edited.
- Memory cards: 2 new, 4 updated.
- Figures: Topic 1 has none.

## 1. Wrong or unclear rules in the videos
- **Add/Sub slides 3, 4 and 9:** "same signs → plus" now says it applies only to two signs *touching* (nothing between them). Slide 4 now says that in −8 − 6 the signs do not touch.
- **Language of Algebra slide 9:** "2k" and "2k + 1" now say "where k is an integer".
- **Language of Algebra slide 5:** "Nonzero" is now taught here (board: "Nonnegative: x ≥ 0 · Nonzero: x ≠ 0"), before the recap uses it.
- **Language of Algebra slide 13 (recap):** says that the exam prints three of these facts in the general comments of every quantitative section (0 is neither positive nor negative, 0 is even, 1 is not prime). The closing lines now introduce the two new videos.
- **Mult/Div slide 5:** removed "Remember when we called it 'times'?". That lesson does not exist.
- **Fast Calc slides 10–12:** added one line each: "squared means times itself" (50², 65²) and "percent means out of a hundred". Squares and percentages are not taught before this lesson.
- **Division sign:** every board item and draw note that used ":" for division now uses ÷ (Remainders 10 ÷ 3, 0 ÷ 9, 9 ÷ 0, 576 ÷ 8, 24 ÷ 6 · 2, 44 ÷ 4, 24 ÷ 8, recap "× ÷"). Mult/Div slide 3 has one new line: "Some books write division with a colon. It means the same thing. In this course we write the division sign or a fraction bar."
- Mid-sentence "so" (meaning "therefore") removed from 5 spoken lines. "Five/Seven questions next" changed to "Questions next", because the question counts changed.
- Add/Sub slide 1: one line for strong students: "Already fast and sure? Try the questions after this lesson first. All correct? Jump ahead."

## 2. Methods added
| Method | Where | Guided (with video) | Practice |
|---|---|---|---|
| **Exam words** (sum, difference, product, quotient, multiple, divisor/factor, divisible by, digit, distinct, at least/at most, consecutive even/odd) | New lesson `r26-t01-exam-words` (7 slides) + card `mem-r26-t01-exam-words`, section 1 after the Number words card | q-r26-t01-01 (digits / distinct / sum) | q-r26-t01-02, -03, -04, -20 |
| **Must / could / cannot + plug-in numbers** (test 0, 1, −1, ½, 10; only allowed numbers; exam strategy: break the wrong choices) | New lesson `r26-t01-must-could` (7 slides) + card `mem-r26-t01-must-could`, end of section 1 | q-r26-t01-05 (must), q-r26-t01-06 (cannot) | q-r26-t01-07, -08, -09, -10 (section 1); -17, -18, -19 (mixed practice) |
| **Minus before brackets** flips every sign inside | New slide 5 "Minus before brackets" in Order of Operations + recap line + card tip | q-r26-t01-11 | q-r26-t01-12, -22 |
| **Fraction bar** (split the top, never the bottom), practised for the first time | Order of Operations slide 6 has a new example of splitting the top (draw note) | none | q-r26-t01-13, -14, -21 |
| **Last digit + estimate to knock out choices** | New slide 9 "Last digit" in Multiplication & Division + card tips | q-r26-t01-15 | q-r26-t01-16, q-012 (new second method) |
| **×9 and ×11** (the card listed it, q-014 used it, no slide taught it) | New slide 5 "×9 and ×11" in Fast Calculation | none | q-r26-t01-23, q-014 |
| Estimation (exam-level) | none | none | q-r26-t01-24 |

Sidebars were updated for all three lessons that got new slides.

## 3. Order of teaching (used before taught)
- **q-018** (200 : 6 = 33⅓) needed fractions (Topic 2). It now asks for the quotient and the remainder: "quotient 33, remainder 2". The distractor "32, remainder 8" teaches that a remainder must be smaller than the divisor.
- **q-014** (666 × 11), **extra-3** (25 × 28) and **extra-4** (48 × 15) moved from Mixed practice to Fast-calculation practice. They come after the lesson that teaches their tricks now. *Workaround:* the API has no "move", and `unplace` deletes the question, so the patch keeps a copy and puts it back (`move_q`).
- The Exam Words video comes before q-036, which uses "product".

## 4. Text (all questions)
- Every solution was rewritten with numbers in `$TeX$`. No ":" for division anywhere. Short sentences, no mid-sentence "so".
- Stems with ":" now use ÷ (q-011, 015–017, 019, 020, 022, 023, 025, 026, 028–030, extra-5). The plain-text stems and choices of the extra and fast-practice questions (e.g. "25×28 = ?", "3526") are now TeX with thousands commas.
- Fixed: q-008 (self-contradicting "every column writes 1"), extra-2 (unclear "shared offset"), extra-1…7 and fast-practice 1–7 (word-only solutions now show every number), q-040 and q-018 (colon fractions), q-037 (odd `\text{odd}` font).

## 5. Practice
- Removed near-duplicates: q-003 and q-033 (two-digit borrowing, same as q-031), and q-004 (adding a negative, same as q-032).
- Mixed practice is ordered easy → hard and ends with 6 exam-level items (brackets, fraction bar, must/could/cannot, "distinct", −1 < x < 0).
- Fast-calculation practice is ordered easy → hard and ends with an estimation item.
- Exam-level items in the topic: about 16 new ones (must/could/cannot, vocabulary traps, bracket traps, estimation).
- New questions: the correct answer is in a different position from one question to the next. Every distractor comes from a real mistake, and every solution names the trap.

## Memory cards
- **Number words:** remainder example uses ÷. Even/odd says "k an integer". Consecutive says "even/odd: by 2". New row "Nonzero". New tip: the three facts the exam prints.
- **Signs and the times table:** "Two signs touching" (was "side by side"). New tips on the last-digit check and on estimating.
- **Order of operations:** ÷ instead of ":". New tip on a minus before brackets. The split-numerator tip now has a correct example.
- **Fast-calculation toolkit:** ×10 ÷ 2 etc. instead of ":". The ×9 example is added (now taught). New tips: what "²" and "%" mean.

## For the teacher to decide
- **Skip test for strong students:** the review asks for 8 questions at the start of each lesson. The course has no mechanism for this. I added one spoken line in Add/Sub slide 1 instead.
- **Fast Calculation position:** it is still after the mixed practice (section 6). The review suggests moving it earlier. I left the order and moved the three questions that needed it instead.
- **Colon line:** Mult/Div slide 3 now says that some books use ":" for division. Delete it if you prefer not to mention ":" at all.
- The new videos use "could be true". Topic 20 uses "can be true". You may want the same word in both topics.

## Pass 2 (2026-09-27, approved remove/restore plan + summary lessons)
**Removed:** nothing (the plan keeps every Topic 1 addition).

**Restored (4):**
- q-003 ($84-36$) and q-004 ($95+(-38)$) are back in "Mixed arithmetic practice" (easy end of the order); q-033 ($63-27$) is back in "Addition and subtraction" after q-032. Their solutions are rewritten in TeX with every number shown.
- q-018 is back in its original form, "$200\div 6=?$" with the choices $33\frac{1}{6}$ / $33\frac{1}{3}$ / $33\frac{2}{3}$ / $33\frac{5}{6}$ (key $33\frac{1}{3}$). It needs fractions, so it moves to the Topic 2 practice (`unit-t2-1`, after q-044).
- The quotient-and-remainder version stays in Topic 1 as a new question **q-r26-t01-25** (same place in the practice order).

**Summary lessons (2 new videos):**
- `r26-t01-summary` "Summary", at the end of "4 · Order of operations", right before "Mixed arithmetic practice". Slides: Summary · Number words · Opposites · reciprocals · Exam words · Must · could · cannot · Adding signed numbers · Multiplying signs · Calculating by hand · Order of operations · Before you practice (about 2.5 min).
- `r26-t01-summary-fast` "Summary: Fast Calculation", at the end of "6 · Fast calculation", right before "Fast-calculation practice". Slides: Summary · Sums and differences · Split a factor · Double, halve, ×25 · Near a round number · Pairs and cancelling · Special products · Percent and estimates · Before you practice (about 2 min).
- Content is only what the Topic 1 lessons teach; the existing recap slides are unchanged.


## 2026-10-04 question = lesson example fixed
- q-r26-t01-14 was the same as the fraction-bar example in "order-of-operations" (recorded): (20 + 8)/4 -> now (24 + 8)/4; answer 24/4 + 8/4 (choice 2).

## 2026-10-06 new exam methods
Function `add_methods` (runs last). Topic 1 is recorded, so only the memory card changes.
- Card "Number words" (mem-definitions): new row after "Integer": **"Number" (the word "integer" is missing)** = any number, fractions included; only "integer" means a whole number. Example: numbers x with 4 < x < 6 and 3x whole → 3x = 13, 14, 15, 16, 17 → five numbers (4⅓, 4⅔, 5, 5⅓, 5⅔), not just 5. (Helps on 1 real exam question; new numbers, not the exam's.)

## 2026-10-07 practice renumber + clean-up
Function `renumber_practice` (runs last). Goal: the English practice must not look like the Hebrew course. Same concept,
trap, level and method; only numbers and choice order change. Practice is never recorded. Recorded and left exactly as
they are: every Topic 1 lesson except Fast Calculation and the two summaries, and the guided solution videos -01, -05, -06 and -15.
Not recorded: guided q-r26-t01-11 (solve-q-r26-t01-11). It was written in English, so it is not changed. Lesson questions
q-021..q-040 (sections 2–4, no videos) are not practice and were not changed in this pass.
Check: `python3 math_check.py 1 2 32` → 0 problems, 0 warnings, 0 layout. Every key was brute-forced in python (exactly one
correct choice). Every trap was recomputed. No new stem equals a stem, lesson board item or card example in topics 1–38, a base-v18 stem
or a number pair in the Hebrew subtitles.

| Id | Old (Hebrew) | New | Answer · key old → new |
|---|---|---|---|
| q-001 | 34 + 48 | 29 + 56 (trap 75 = no carry) | 85 · 1 → 1 |
| q-003 | 84 − 36 | 72 − 45 (traps 33 = smaller from bigger, 37) | 27 · 3 → 3 |
| q-006 | 31 − 58 | 34 − 71 (trap 37 = sign lost) | −37 · 2 → 4 |
| q-002 | 73 − (−46) | 64 − (−29) (trap 35 = sign flip ignored) | 93 · 4 → 2 |
| q-004 | 95 + (−38) | 83 + (−47) (traps 130, 46 = no borrow) | 36 · 2 → 2 |
| q-005 | −62 − 25 | −54 − 28 (trap −26) | −82 · 1 → 3 |
| q-007 | 468 + 85 | 376 + 57 (two carries; traps 423, 333; estimate kept) | 433 · 2 → 3 |
| q-008 | 666 + 555 | 888 + 444 (three carries; trap 1,222 = no carries) | 1,332 · 2 → 1 |
| q-009 | 8,003 − 994 | 6,002 − 997 (subtract 1,000, give 3 back; trap 4,999) | 5,005 · 3 → 2 |
| q-010 | 5,005 − 606 | 7,003 − 405 (two pieces; trap 6,608) | 6,598 · 2 → 4 |
| q-011 | (−64) ÷ (−8) | (−54) ÷ (−6) | 9 · 1 → 3 |
| q-015 | 320 ÷ 5 | 435 ÷ 5 (split 400 + 35) | 87 · 1 → 2 |
| q-016 | 192 ÷ 4 | 276 ÷ 4 (split 240 + 36) | 69 · 4 → 1 |
| q-012 | 9 · 13 | 7 · 16 (split; 2nd way kept: last digit 2 leaves 112/92, more than 7 · 15 = 105) | 112 · 1 → 3 |
| q-013 | 12 · 14 | 13 · 14 (split 10 + 4) | 182 · 4 → 1 |
| q-017 | 3,618 ÷ 18 | 3,232 ÷ 16 (split 3,200 + 32; check by multiplying) | 202 · 4 → 4 |
| q-019 | 18 ÷ (8 − 2) − (−4) · 3 | 24 ÷ (9 − 5) − (−2) · 4 (traps 32 = left to right, −2) | 14 · 1 → 2 |
| q-020 | 12 ÷ (−4) − (−6) · (−2) | 20 ÷ (−5) − (−3) · (−4) (trap 8) | −16 · 4 → 3 |
| q-014 (Fast practice) | 666 × 11 | 534 × 11 (×10 plus one copy) | 5,874 · 4 → 3 |
| q-018 (in the Topic 2 practice) | 200 ÷ 6 = 33⅓ | 250 ÷ 6: remainder 4 → 4/6 = 2/3 (choices in sixths/thirds as before) | 41⅔ · 2 → 3 |
| fast-practice-1 (extra) | 98 × 37 (one away from the summary example 98 × 36) | 98 × 43 | 4,214 · 4 → 4 |

**Practice clean-up (42 → 29: Mixed practice 30 → 23, Fast-calculation practice 12 → 6)**
- Copies removed (checked against the current build): alg-extra-1 (297 + 68) and -2 (804 − 297), the same "move across / shift"
  tricks as the Fast Calculation examples; alg-extra-5 (72 ÷ 12, a times-table copy of the lesson questions);
  fast-practice-3 (702 − 398, the same as the summary 802 − 395); q-r26-t01-25 (200 ÷ 6 quotient and remainder, the same
  sum as q-018); q-r26-t01-18 (−1 < x < 0 largest, the same question in topics 3, 8, 12, 17).
- Extra-bank drills: 2 warm-ups kept in Mixed practice (alg-extra-6 signs, alg-extra-7 brackets). 4 kept in Fast practice,
  one per trick (near a round number, friendly ×125, around a centre, cancel). This is the only practice for that lesson. Removed: alg-extra-3 (25 × 28)
  and -4 (48 × 15), the same as the lesson/summary examples 44 × 25, 36 × 25, 36 × 15 and 28 × 15; fast-practice-6 (16% of 75, the lesson uses 24% of 75);
  fast-practice-7 (85², the lesson uses 65² and the summary 35²).
- September items of a type the Hebrew practice covers, removed: q-r26-t01-22 (signs and brackets: q-002, q-019, q-020),
  q-r26-t01-17 (must be true; section 1 has four of these), q-r26-t01-23 (86 × 9, the same slide and type as q-014 ×11).
- Kept (types the Hebrew practice does not have): q-r26-t01-21 (fraction bar), -20 (distinct factors), -19 (cannot be prime), -24 (estimate).
- Order easy → hard: + − with carries/borrows → signs → bigger sums → ÷ and × → long division → order of operations → exam-level.
  Fast practice: ×11 → near round → ×125 → around a centre → cancel → estimate. The target was about 28. The result is 29,
  because the fast-calculation lesson needs its own drills.

### 2026-10-07 (2) lesson-section questions q-021..q-040
Function `renumber_lesson_questions` (runs last). These are the Hebrew study questions inside sections 1–4, with no solution videos.
The recorded lessons before them only say "Questions next". No spoken line quotes their numbers, so nothing recorded refers to
them. Same checks as above: keys brute-forced, traps recomputed, no duplicate with any question, lesson board item or card in topics 1–38
or with base-v18, and nothing taken from the Hebrew subtitles. None of them equals the recorded lesson examples (17·8, 576÷8, 12·9, 398+57,
602−198, 703−286, 24÷6·2, 5−(9−2), 12/(2+4) …).

| Id | Old (Hebrew) | New | Answer · key old → new |
|---|---|---|---|
| q-021 | 4 + 6·5 | 7 + 3·6 (trap 60 = add first) | 25 · 3 → 3 |
| q-022 | 6·(2 − 5) ÷ (−3) | 4·(3 − 8) ÷ (−2) (trap −10 = sign) | 10 · 3 → 2 |
| q-023 | 5 − (9 − 6 ÷ 3) | 3 − (12 − 10 ÷ 5); both ways kept (÷ first / open the brackets); trap −11 | −7 · 2 → 2 |
| q-024 | [12 + (−7)]·[(−6) − (−6)] − (−2) | [15 + (−9)]·[(−4) − (−4)] − (−3); zero bracket; trap −45 | 3 · 1 → 2 |
| q-025 | 24 ÷ [2·(7 − 4) ÷ 3] | 36 ÷ [3·(8 − 2) ÷ 9]; trap 8 = no brackets | 18 · 1 → 3 |
| q-026 | (−63) ÷ 9 | (−72) ÷ 8 | −9 · 2 → 2 |
| q-027 | 14·6 | 15·7 (split 10 + 5) | 105 · 1 → 2 |
| q-028 | 91 ÷ 7 | 84 ÷ 6 (split 60 + 24) | 14 · 2 → 3 |
| q-029 | 75 ÷ 5 | 85 ÷ 5 (split 50 + 35) | 17 · 2 → 4 |
| q-030 | 3,366 ÷ 11 | 4,856 ÷ 8 (split 4,800 + 56; check) | 607 · 1 → 2 |
| q-031 | 93 − 46 | 81 − 37 (borrow) | 44 · 1 → 1 |
| q-032 | 68 + (−25) | 57 + (−34) (trap 91) | 23 · 4 → 2 |
| q-033 | 63 − 27 | 52 − 18 (borrow; traps 46, 44) | 34 · 4 → 4 |
| q-034 | 4,853 + 76 | 3,762 + 57 (one carry) | 3,819 · 3 → 2 |
| q-035 | 743 − 347 | 652 − 267 (two borrows; trap 415) | 385 · 4 → 2 |
| q-036 | product of the two smallest two-digit primes (trap 11·11) | product of the two largest one-digit primes (traps 7·7, 7·9) | 35 · 2 → 1 |
| q-037 | which statement about 1 is not correct | same idea, reworded, choices reordered | "prime" · 2 → 4 |
| q-038 | m, n opposites: m + n | x, y opposites: x + y (choices reordered) | 0 · 3 → 4 |
| q-039 | smallest two-digit prime ÷ 4: remainder | smallest two-digit prime ÷ 3: remainder (trap 1 = uses 10) | 2 · 1 → 2 |
| q-040 | p, q reciprocals: p·q | a, b reciprocals: a·b (choices reordered) | 1 · 1 → 3 |


## 2026-10-07 methods spread
Nothing added. Checked all 65 questions against every new method: no letter-expression questions (power count), the must/could/cannot items already plug in or use the tag form (q-r26-t01-06 writes q = 2k, q-r26-t01-19 uses 6k), and the mirror test cuts only one choice in q-r26-t01-09. The one unrecorded solution video (solve-q-r26-t01-11, brackets) has no fitting method, so no slide.
All new lines verified numerically (python: power by scaling, fitting values, choice values, mirror values). `math_check.py 1 2 3 4 5 6 7 8 9 10 32`: PROBLEMS 0, WARNINGS 0, LAYOUT 0.
