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
