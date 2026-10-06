# Topic 15 — Division & Remainder: changes

Patch: `math_patches/t15.py`. Check: `python3 math_check.py 15` shows 0 problems, 0 warnings and 0 layout problems.
The topic order is unchanged: T15 still comes before T16. For this reason, products of consecutive integers are now taught inside T15.

## Summary
- Questions: 39 rewritten, 14 added (2 guided with solution videos and 12 practice), 2 removed.
  Before: 41 questions (14 guided and 27 practice). Now: 53 questions (16 guided and 37 practice).
- Main lesson "Division & Remainder": 6 slides rewritten, 2 slides changed (÷ instead of ":"), 2 slides added. It now has 15 slides and runs about 9.3 minutes.
- New lesson video "More Remainder Tools": 7 slides, about 4.3 minutes. It is the first item of the advanced section.
- New solution videos for the two new guided questions.
- Existing solution videos changed: Q1, Q2, Q4, Q5, Q8, Q9, Q10 and Q13 (old numbers). The guided questions are renumbered automatically: 1–5 in the theory section and 6–16 in the advanced section.
- Memory card "Divisibility signs & remainders" rewritten. New card "More remainder tools".

## 1. Wrong teaching (fixed)
- **Slide 5, now titled "Build a divisor":** the old line "use the same trick for any bigger number" invited 12 = 2·6. The slide now says: split the divisor into parts with no common factor, for example 12 = 3·4, 15 = 3·5, 18 = 2·9 and 24 = 3·8. It also shows the trap: 6 divides by 2 and by 6, but not by 12.
- **Slide 7 (zebras):** the old rule "divide by four and by five" is replaced with "build it from the inside": k → 5k → 20k, so you multiply the denominators. The counterexample "½ of ¼ means divisible by 8, not 4" is on the board. The lesson now agrees with the Q1 solution.
- **Slide 6 (by 11):** there is now one rule, "alternate + − + −". For three digits this is the old "outer minus middle". The slide adds a four-digit example (1,331) and a negative result (482 gives −2, so it does not divide). The q-440 solution now uses the same rule.
- **Plug-in advice made consistent** in the Q4, Q9, Q10 and Q13 videos, on both cards and in the new "Plugging in: the rule" slide:
  - one value that fails knocks out a choice;
  - values that work prove nothing;
  - avoid values that give 0.
  The contradicting lines were removed: "recommended route, by far", "use plugging in only if you can't solve it", and "plugging in x = 0 is usually fastest". Choosing x = 0 is still presented as safe for the "which expression could be the number" type.
- **"mod" and "≡" notation** removed from all solutions (Q11, q-444, q-448, q-456, Q4, Q14, q-450).

## 2. Methods added
**Main lesson:**
- New slide "Digit sum → remainder" (by 3 or 9): 5,432 → 14, so it leaves 5 when divided by 9 and 2 when divided by 3.
- "Combine remainders" now adds the difference (4 − 5 = −1 → +7 → 6), with a check on real numbers. It also adds the rule "a and a + b divide by d → b divides by d" (needed for Q14 claim 3).
- New slide "Change the divisor": from 10 to 5 the remainder is kept, and a remainder that is too big is divided again. From 6 to 4 it is unknown. The rule is that the new divisor must divide the old one (needed for q-441, q-453 and Q13).

**New video "More Remainder Tools"** (before the advanced questions):
1. Take away the remainder: N − r divides by d. It includes the reverse question "100 ÷ n leaves 4": n divides 96 and n > 4, which gives 8 values.
2. Counting multiples: write the first and last multiple as d·k, then count = last k − first k + 1 (three-digit multiples of 11: 81).
3. Units digit: only the units digits matter, and powers repeat (7, 9, 3, 1). This replaces "mod" in Q11 and q-448.
4. **Numbers in a row (the short consecutive-integers slide):** two in a row divide by 2 and three in a row divide by 6. It shows the hidden forms a³ − a and n² − n, and the warning that n(n + 2) is not "in a row". This covers Q10, q-444, q-447, q-449 and extra-5 without T16.
5. Plugging in: the rule. The example n(n+1)(n+2) shows that one value (n = 2) leaves three choices, so you need a second value.
6. Recap.

**New guided questions:**

| New # | id | Question | Answer |
|---|---|---|---|
| Q5 | q-r26-t15-01 | a leaves 2 and b leaves 5 (divided by 7); remainder of a − b | 4 (the trap is 3) |
| Q9 | q-r26-t15-02 | 75 ÷ n leaves 3: how many values of n? | 9 (the traps are 12, 10 and 6) |

**Existing guided questions:**
- Q8 (q-430, now Q10) now counts exactly with first and last multiples. The old "1/10 > 1/11" argument became Method 2, with a warning that it can be off by one in a short range.
- Q5 (q-427, now Q6) no longer uses a ratio, which is taught only in T22. It uses 60% = 3/5 → 5k and 3k.

## 3. Text
- Every question in the topic now has its math in TeX and uses ÷ or fractions instead of ":". Stems are reworded in NITE style ("What will be the remainder if … is divided by …?", "It cannot be determined from the information given.").
- Given equations are stacked in q-431 and q-451. The claims in q-430 and q-435 are each on their own line.
- q-428 (slot machine) is reworded clearly, with the payout rules on separate lines. q-445 (lockers) now explains what "changes the state" means.
- q-448: the garbled sentence is replaced with a clear units-digit solution.
- q-452: the case d = 9 is added (99,999 + 1 = 100,000, and the remainder is still 1).
- alg-extra-1: the confusing "plus 8; reduce that" is now n + 5 = 5(k + 1) + 3.
- The solution video titles and pre-loaded stem notes are updated to match the new stems.
- Q13 video: "three ways to decide" is now "two ways" (the video has two methods).

## 4. Practice
- Removed: alg-extra-unit-t15-3-4 (same type as Q2 and q-437) and alg-extra-unit-t15-3-6 (an LCM question that belongs to T14).
- Added 12 questions (q-r26-t15-03 … 14):
  - reverse remainder ×2
  - counting multiples ×2
  - remainder of a difference ×1, and x² − 2x with a known remainder ×1
  - the "18 = 2·9, not 3·6" trap ×1
  - digit sum 40 → remainder by 9 ×1
  - nested fractions (⅔ of the members, then ¾ of those) ×1
  - odd n: n² − 1 divides by 8 ×1
  - units digit of 3²⁵ ×1
  - remainder 1 by 2, 3, 4 and 5 → 61 ×1
- The practice is ordered from easy to hard. There are now about 15 exam-level items, with q-444, q-455 and q-445 at the end.
- Every new answer was checked by brute force over many values.

## For the teacher to decide
- If T16 is later moved before T15, the "Numbers in a row" slide can be cut or shortened to a reminder.
- q-445 (lockers, a divisor-count question from T14) and q-455 (mostly a roots question) are kept as the last, hardest items. You could move them to T14 and T10.
- The main lesson grew from 6.4 to 9.3 minutes. If that is too long, "Change the divisor" can move into the tools video.

## Pass 2 (teacher-approved plan, 2026-09-27)
**Removed** (the "reverse" remainder question, "100 ÷ n leaves 4: how many n?"; 0 real-exam and 0 original questions of this type):
- "More Remainder Tools", slide "Take away the remainder": the reverse half (100 ÷ n leaves 4, 96, n > 4, the divisors of 96, the check). The first half (N − r divides by d, the 53 example) stays.
- Same video, Recap: ", and d > r" dropped.
- Card "More remainder tools", row "Known remainder": the example is now the slide's 53 example (53 ÷ 7 leaves 4 → 53 − 4 = 49 = 7·7).
- Guided question q-r26-t15-02 (75 ÷ n leaves 3) and its solution video. The guided questions after it renumber automatically (now 15 guided: 1–5 theory, 6–15 advanced).
- Practice q-r26-t15-03 and q-r26-t15-04.

**Restored** (originals, text clean-up only):
- alg-extra-unit-t15-3-4 (remainder 3 by 4 and 2 by 5, smallest = 7) and alg-extra-unit-t15-3-6 (smallest number divisible by 8 and 12 = 24, the LCM from T14). Choices in TeX, full numeric solutions. Both placed back in the practice at matching difficulty.
- Card "Divisibility signs & remainders": checked against the original. Every true original row is present (the 15 row is covered by "12, 15, 18, 24"); the old 6/15, 11 and "÷4 and ÷5" rules stay fixed.

**Summary video** `r26-t15-summary` "Division & Remainder: Summary" (about 2 minutes), the last item of the advanced section, right before the practice. Slides: Summary · Divisibility signs · Build a divisor · Divisibility stories · Remainder basics · Combine remainders · Change the divisor · Counting and units digits · Numbers in a row · Before you practice.

## 2026-10-05 cut repeats
Function `cut_repeats` (runs last). Nothing in topic 15 is recorded.
- **`divisibility` "Division & Remainder"**: 9.3 → 6.8 min. The signs and the remainder basics stay (the Hebrew course has them as theory too).
  - Cut "Divisibility stories" (the zebras) → taught in Q1 `solve-q-423` (eliminate what can't be; build from the inside k → 4k → 12k). Added in Q1 method 2: "a fraction of a fraction — multiply the denominators. Half of a quarter? It must divide by eight" + board item.
  - Cut "Algebraic form" (N = 6k + 2) → taught in Q4 `solve-q-426` (3x + 1) and Q14 `solve-q-435` (6k + 3); the hop pattern in Q2 `solve-q-424`.
  - Cut "Combine remainders" → Q5 `solve-q-r26-t15-01` (difference, negative → add the divisor) now also says "for a sum add, for a product multiply" + board item; the "a and a + b" rule is taught in Q15 `solve-q-436`. The matching recap item was removed.
  - Q6 `solve-q-427` said "like the zebras" → "like the chess class".
- **`r26-t15-remainder-tools` "More Remainder Tools"**: 3.7 → 2.2 min. Kept: take away the remainder, units digit (powers repeat), numbers in a row (Q11 teaches only part of it).
  - Cut "Counting multiples" → taught in Q9 `solve-q-430`; added there "Don't forget the plus one — from three to seven there are five numbers" + board item "Count = last k − first k + 1".
  - Cut "Plugging in: the rule" → taught in Q4 (never a value that gives 0), Q10 (one failing example is proof), Q11 (avoid 0; try a second value), Q14 (examples that work are not proof).
  - Cut "Recap".
- For the teacher: the AI summary script `ai_scripts/r26-t15-summary.json` still says "there's no such thing as a third of a zebra". The zebra example is gone from the lesson (the idea is in Q1). Not edited.

## 2026-10-06 new exam methods
Function `add_methods` (runs last, after `cut_repeats`). Nothing in topic 15 is recorded.
- **"More Remainder Tools"**: new slide 5 "Tag it" (sidebar item added; video 2.2 → 4.1 min); slide 1 now says "four short tools"; the closing line moved to the new slide. Teaches: write each condition as a tag (a = 6k, b = 10m; k and m are unknown, they guarantee nothing); multiply → tags multiply (60km → 60); add → only the shared factor (6k + 10m = 2(3k + 5m) → 2, why: 3k + 5m can be 8 or 11); divide → every factor of the bottom must be in the tags (ab/15 = 4km ✓, a/4 = 3k/2 ✗); "by 4 and by 6" → tag 12k (LCM), not 24k; plugging in → different values for different letters (a = b = 30 gives a false 60; 6 + 10 = 16).
- **New guided question q-r26-t15-15** (after Question 10, now Question 11): x divisible by 6, y divisible by 9, largest number x + y is necessarily divisible by: 18 · 15 · 9 · 3 → 3. Traps: 18 (equal values x = y = 18 → 36), 15 (smallest values 6 + 9), 9. Solution video `solve-q-r26-t15-15` (1.4 min): Method 1 tag it (6k + 9m = 3(2k + 3m)), then "The trap · Equal values". Checked by computer: gcd of all 6k + 9m is 3.
  - The teacher's suggested example (x, y multiples of 3, choices 3/6/9/12) is a real exam question (2025 autumn), so an original pair was used instead; the slide example (multiple of 6 + multiple of 10) avoids the real "multiple of 4 + even" question too.
- Card "More remainder tools": new row "Necessarily divisible by…? → Tag it" (rules + example).


## 2026-10-06 practice: new methods
Function `practice_methods` (runs last; append only). 2 practice questions, Method 2 · Tag it.
- q-r26-t15-07: a = 9k + 3, b = 9m + 7 (different letters) → a − b = 9(k − m − 1) + 5 → 5.
- q-453: a + 2 = 6k + 5; the tag 6k is not always a multiple of 4 → k = 0 gives remainder 1, k = 1 gives 3 → cannot be determined.
- The other necessarily-divisible questions (q-442, q-451, q-449, q-444, q-455, q-438) already solve with tags, so nothing added there.
All new lines verified numerically (python: fitting values, choice values, power by scaling). `math_check.py 15 32`: PROBLEMS 0, WARNINGS 0, LAYOUT 0.

## 2026-10-06 renumber pass
So the English course does not look like the Hebrew one: every Hebrew-derived question has new numbers, and the
stories have new names, objects and settings. The idea, the trap and the methods stay the same, and every guided
solution video is rewritten to match (board, speech, draw cues, video title). New numbers also avoid the Hebrew video
versions (zebras 1/4·1/5, Shimrit's cubes, 5·3 remainders, 4x + 1, 97X, 18, 6 vs 7 / 18 vs 20, c = 7a, 2a³ − 2a, 18a + 6,
x leaves 4 by 6). Nothing in Topic 15 is recorded, so nothing had to be kept as it was. Function `renumber(M)` in t15.py runs last.

**Counts:** 14 guided questions renumbered (q-423 … q-436) with their 14 videos rewritten; 20 practice questions
renumbered (q-437 … q-456); 9 lesson slides' examples renumbered (lesson "Division & Remainder": by 2/5/10, by 3/9, by 4/8,
build a divisor, by 11, the remainder trap, biggest remainder, change the divisor) + the memory card; "More Remainder
Tools": the units-digit example (it was the old q-433, 12 · 286) and the tools card (count example, A(A+4)(A+8) tip).
Practice: 37 → 25 (the audit's target).

**Order:** guided order unchanged (it already goes easy → hard; videos refer back to Q1). Correct-answer position moved in
29 of the 34 questions. The advanced-section sidebars now list Question 11 (the Tag-it question) too.

**Practice clean-up (37 → 25):**
- Copies removed: q-r26-t15-07 (= guided Q5, remainder of a − b), q-r26-t15-13 (units digit of 3²⁵ = warm-up 7⁴),
  warm-up 3-4 (= guided Q2, two leftover conditions).
- Warm-ups kept (3): 3-7 (N = dq + r), 3-3 (12,345 by 9 → digit-sum remainder), 3-2 (units digit of 7⁴).
  Removed: 3-1 (n + 5, trivial), 3-5 (numbers in a row; q-447/q-449/q-444 cover it), 3-6 (LCM; q-437/q-438 cover it).
- September items kept (2, types the Hebrew practice lacks): 06 (count the three-digit multiples of 24),
  09 (divisible by 18: 2·9, not 3·6). Removed: 05 (counting, kept 06 instead), 08 (remainder of x² − 2x; q-443 covers
  product of remainders), 10 (digit sum 40 → by 9; warm-up 3-3 covers it), 11 (2/3 then 3/4; q-438 covers fraction of a
  fraction), 12 (n² − 1 by 8; q-449/q-444), 14 (leaves 1 by 2, 3, 4, 5; q-437 covers take-away-the-remainder).
- The "Method 2 · Tag it" line of q-453 is rewritten with the new numbers (q-r26-t15-07's line went with the copy).

**Checks:** every answer and distractor brute-forced in Python (exactly one correct choice each; traps kept: 24 = 8·3 in
Q3, "difference" 3 in q-441, 2+1 = 3 in q-453, 675 divisible by 3 but odd in Q14, smallest case 360 in q-444, 16 counting
odd and even in q-454). Duplicate check over the whole build (topics 1–15 questions, lesson boards, draw notes, cards):
no question equals another question or a lesson example (only coincidental single numbers like 540/560 in arithmetic
lessons). `math_check.py 15 32` → PROBLEMS 0, WARNINGS 0, LAYOUT 0; `SRC=tmp_check/check-15-32.html python3 ai_check.py
r26-t15-summary` → OK (the summary is unchanged; "a third of a student" refers to its own 1/3 of 1/6 board, still true).
All 16 changed videos rendered and looked at.

| id | old (numbers / story) | new | answer |
|---|---|---|---|
| q-423 (G) | Maya's class: 1/3 chess girls, 1/4 of those piano; 45, 40, 48, 26 | Daniel's class: 1/5 basketball boys, 1/3 of those guitar; 35, 45, 42, 32 | 45 (2) |
| q-424 (G) | Nora's beads: rows of 4 → 3 left, rows of 5 → 2 left; 42, 27, 22, 12 | Tamar's stamps: rows of 5 → 4 left, rows of 3 → 1 left; 28, 40, 34, 16 | 34 (3) |
| q-425 (G) | max x·y, remainders by 7 and 4 (trap 28) | remainders by 8 and 3; 7, 2, 14, 24 (trap 24) | 14 (3) |
| q-426 (G) | remainder 1 by 3: 3x+5, 6x+8, (3x+4)², (3x+6)² | remainder 4 by 5: 5x+7, (5x+2)², 10x+8, (5x+5)² | (5x+2)² (2) |
| q-427 (G) | 60% study French; 460–490 | 30% of a sports club play tennis; 530–560 | 540 (2) |
| q-428 (G) | slot machine 85X, 5/10/15 shekels, Maya won 15 | game machine 61X, 4/8/12 tokens, Noa won 12 | 2 values (3) |
| q-429 (G) | not by 12: 1,236 / 2,148 / 3,224 / 4,344 | 1,428 / 3,152 / 5,172 / 2,316 | 3,152 (2) |
| q-430 (G) | Eitan 10 vs 11, Dana 12 vs 14 (both right) | Yoav 14 vs 13 (64 < 69), Michal 15 vs 22 (60 > 41) | only Michal (2) |
| q-431 (G) | c = 5a, a = b/3; 5, 3, 9, 16 | c = 4a, a = b/5; 4, 5, a+b by 12, a+b+c by 10 | a+b by 12 (3) |
| q-432 (G) | 3a³ − 3a; 12, 18, 24, 36 | 5a³ − 5a; 60, 40, 30, 20 | 30 (3) |
| q-433 (G) | 12a + 8 by 10; 285–288 | 14a + 6 by 10; 343–346 | 346 (4) |
| q-434 (G) | casino, 500 tokens, lost x, 2x, 3x; 10, 30, 20, 45 | amusement-park card, 700 points, rides x, 2x, 3x; 25, 40, 20, 50 | 40 (2) |
| q-435 (G) | x leaves 3 by 6; Adam 2x by 6, Ben x by 3, Gal x by 9 | x leaves 4 by 8; Yuval 2x by 8, Noga x by 4, Itay x by 12 | only Itay wrong (2) |
| q-436 (G) | sum of three integers by 3 (1+4+7, 6+4+2) | sum by 6 (2+8+14, 6+1+5), claims reordered | "one divisible → others" (2) |
| q-437 | class, groups of 3 and 5, one group of 2; 35, 27, 32, 25 | hikers, teams of 4 and 5, one team of 3; 27, 43, 38, 29 | 43 (2) |
| q-438 | Tom, marbles, 4 children, friends 3 and 5 → 60 | grandmother, stickers, 3 grandchildren, friends 2 and 7; 21, 42, 14, 84 | 42 (2) |
| q-439 | 25% of college students ride bicycles; 106, 214, 316, 217 | 75% of employees come by train; 238, 412, 326, 315 | 412 (2) |
| q-440 | by 11: 482, 693, 925, 997 | 562, 719, 374, 948 | 374 (3) |
| q-441 | leaves 3 by 10 → by 5 | leaves 4 by 14 → by 7; 0, 3, 4, cannot | 4 (3) |
| q-442 | 30 + 10x not necessarily by 10, 2, 5, 4 | 18 + 6x; 2, 4, 6, 3 | 4 (2) |
| q-443 | leaves 7 by 9 → 2x | leaves 5 by 8 → 3x; 5, 7, 3, 0 | 7 (2) |
| q-444 | A even, A³ + 12A² + 32A; 18, 32, 24, 60 | A³ + 24A² + 128A = A(A+8)(A+16); 60, 16, 48, 24 | 24 (4) |
| q-445 | Lior, 80 lockers; 49, 50, 55, 78 | Ron, 90 light bulbs; 50, 72, 64, 88 | 64 (3) |
| q-446 | Ann/Ben/Carl, 5 towers, tallest 8; 13, 15, 20, 25 | Gil/Hila/Ido, 7 towers, tallest 9; 15, 21, 28, 35 | 21 (2) |
| q-447 | n² − n by 10; 5, 3, 4, 8 | n² + n by 10; 3, 6, 4, 8 | 4 (3) |
| q-448 | 13x + 9 by 10; 240, 187, 253, 322 | 17x + 3 by 10; 248, 263, 251, 239 | 251 (3) |
| q-449 | n by 4, n(n+4) → 32 | n by 3, n(n+3); 9, 18, 27, 36 | 18 (2) |
| q-450 | mother, candies, 3 children, 1 left, eldest ×3 → 10 | coach, balls, 4 teams, 3 left, one team ×2; 35, 15, 20, 23 | 15 (2) |
| q-451 | b = 3a, c = 3b, d = 3c → 40 | b = 2a, c = 2b, d = 2c; 2, 15, 8, 4 | 15 (2) |
| q-452 | taxi, 5 identical digits, fax = +1, by 5 | pizzeria, 7 identical digits, delivery line = +1, by 7; 0, 6, 1, 2 | 1 (3) |
| q-453 | leaves 3 by 6 → a + 2 by 4 | leaves 2 by 9 → a + 1 by 6; 3, 0, 1, cannot | cannot (4) |
| q-454 | even numbers 0–60 leaving 4 by 5 | odd numbers 0–80 leaving 3 by 5; 16, 7, 8, 15 | 8 (3) |
| q-455 | y = √3·x/2, y by 6 → x² by 48 | y = √2·x/3, y by 4; 18, 72, 8, 36 | 72 (2) |
| q-456 | x+y+z by 3; impossible: x+y leaves 2, z by 3 | x+y+z by 4; impossible: x+y leaves 3, z by 4 (now choice 4) | (4) |
| lesson | 376; 330, 2,745; 417; 765; 3,524; 6,320 | 538; 460, 3,815; 942; 846; 2,716; 7,240 | – |
| lesson | 162; 715; 44/66/77/88; 121, 132; 320/480/640 | 234; 836; 22/33/55/99; 143, 165; 160/240/560 | – |
| lesson | 4 ÷ 7 → 4; 30 shekels, bottles 7 → 2; 4 shekels | 5 ÷ 8 → 5; 35 shekels, sandwiches 8 → 3; 5 shekels | – |
| lesson | x ÷ 5: 1, 2, 3, 4, 0, 1; by 10 → 9 | x ÷ 4: 1, 2, 3, 0, 1, 2; by 12 → 11 | – |
| lesson | change divisor: 3 by 10 → 5; 8 by 10 → 5; 3 by 6 → 4 (= q-441 / q-453) | 4 by 15 → 5; 13 by 15 → 5; 1 by 4 → 6 | – |
| card | 1/4 of 1/5 → 20k (the zebras) | 1/2 of 1/7 → 14k | – |
| tools | 12 · 286 (old q-433); multiples of 11 → 81 (old q-430); A(A+4)(A+8) → 120 | 16 · 327; multiples of 16 → 56; A(A+8)(A+16) → 360 | – |

The guided questions made in English (q-r26-t15-01, q-r26-t15-15), the kept practice items and the summary video keep
their numbers.

## 2026-10-06 review
Independent check of the renumber pass (14 guided + 20 practice, 14 videos, lessons "Division & Remainder" / "More
Remainder Tools", 2 cards, practice 37 → 25). Every key brute-forced in Python (exactly one correct choice each, traps
still distractors), every video step redone with the new numbers, kind of condition and methods compared with the
pre-renumber version; removals checked (only copies / extra warm-ups / September items of covered types). No new
quadratic trinomial (q-444 keeps its inherited one: A(A+8)(A+16)). No question equals another question or a lesson example.
- Lesson "Division & Remainder", slide "Change the divisor": the "can't know" example had become "leaves 1 by 4 → by 6?"
  (a BIGGER new divisor, which hides the real trap). Back to the Hebrew kind — a smaller divisor that does not divide the
  old one — with new numbers: "x leaves 2 when divided by 8. By 6?" (x = 2 → r2, x = 10 → r4 → can't know); speech and
  rule line ("Six doesn't divide eight") updated, and the memory card row "New divisor" (by 8 → by 6: unknown).
  (Not 10 → 4: that is the summary video's example; not 9 → 6: that is q-453.)
`python3 math_check.py 15 32` → 0 / 0 / 0. Rendered divisibility, solve-q-430, -434, -436.
- (review, teacher decision: same message AND same difficulty as the Hebrew) — all verified in Python:
  - q-430: back to the Hebrew conclusion "both right". Yoav: by 3 and 5 (→15: 105 = 15·7 … 990 = 15·66 → 60) vs by 17
    (102 = 17·6 … 986 = 17·58 → 53). Michal: by 2 and 9 (→18: 108 = 18·6 … 990 = 18·55 → 50) vs by 4 and 5 (→20: 100 = 20·5 …
    980 = 20·49 → 45). Choices Only Yoav / Only Michal / Both are right / Both are wrong · key 3. Video keeps both methods
    (count exactly; estimate 1/15 > 1/17, 1/18 > 1/20); written solution rewritten.
  - q-436: back to "sum divisible by 3" (the Hebrew kind). Claims: greatest remainder 2 / one divisible → the other two
    (key 2; fails: 9 + 5 + 7 = 21) / all three leave 2 (5 + 8 + 11 = 24) / two divisible → the third. Video + intro
    ("a sum divisible by three") + written solution rewritten.
  - q-444: easier trinomial: n = A³ + 24A² + 80A = A(A+4)(A+20) → 8·m(m+2)(m+10) → 24. Choices 132, 16, 48, 24 · key 4
    (A = 2 → 264: not by 16 or 48, trap 132 divides it; A = 4 → 768 knocks out 132). Note: no non-Hebrew choice is as small as
    A² + 12A + 32: with A even, the answer stays 24 (not 48) only when both shifts are 2·(even), so (A+4)(A+8) is the only
    such pair with coefficient 12; (A+4)(A+20) is the next smallest. Memory-card tip updated (A(A+4)(A+20), A = 2 → 264).
  - q-447: back to n² − n, where n itself is the multiple of 5: choices 4, 2, 0, 9 · key 0 (n = 30: 870 ✓); 4 is the
    trap (n + 1 a multiple of 5).
  - q-450: two tries, as in the Hebrew: 5 teams, 2 balls left; one team gets twice each of the other four → x = 6s;
    6 leaves 1 ✗, 12 leaves 2 ✓. Choices 42 (works, not smallest), 12, 30 (leaves 0), 22 (not by 6) · key 2.
  `python3 math_check.py 15 32` → 0 / 0 / 0. Rendered solve-q-430 and solve-q-436.
