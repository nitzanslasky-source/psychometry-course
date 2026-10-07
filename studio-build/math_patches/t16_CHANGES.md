# Topic 16 — Integers: changes

Patch: `math_patches/t16.py`. Check: `python3 math_check.py 16` shows 0 problems, 0 warnings and 0 layout problems.

## Summary
- Questions: 42 rewritten, 15 added (4 guided with solution videos and 11 practice), 1 removed (q-477).
  The topic had 16 guided and 27 practice questions. It now has 20 guided and 37 practice questions.
- New lesson video: "Sums of Consecutive Integers" (7 slides, about 2.6 minutes).
- New solution videos: 4 (for the 4 new guided questions).
- Lesson videos changed:
  - "Integers": 3 slides changed, 1 added ("Signs of sums").
  - "Consecutive Integers": 1 slide changed.
  - "Even & Odd": 4 slides changed.
  - "Products of Consecutive Integers": 5 slides changed, 2 added ("Only a candidate", "Count the twos").
- Solution videos changed (small edits): the videos for q-457, q-458, q-460, q-461, q-463, q-464, q-465 and q-469. In all solution videos, the title and slide description now show the new wording of the question.
- Memory cards: 4 changed (signs, consecutive, even & odd, special products), 1 new ("Sums of consecutive integers").
- No figures in this topic.
- Guided questions are renumbered automatically in course order (1 to 20).

## 1. Wrong rule fixed (priority 1): "Plug in the smallest numbers — the product is the divisor"
This rule was on slides 4 and 7 of "Products of Consecutive Integers" and on the "Special products" card. It is false in general. For example, 1·3·5 = 15, but 7·9·11 = 693 is not divisible by 5. It also leads students to the wrong answer on T15 q-444.
- **Slide 3 (Three and four):** now gives the reason for each rule. Four in a row: one factor divides by 4, another is even, and one divides by 3, so 8·3 = 24. The line "Check yourself with other numbers — it always works" was removed.
- **Slide 4, renamed "Smallest case":** the smallest case is now only a memory aid for the three rules we just proved. It is "not a way to find new rules".
- **New slide 5, "Only a candidate":** shows 1·3·5 = 15 against 7·9·11 = 693, where only 3 survives. It teaches the method:
  1. cross out every choice that does not divide the smallest case;
  2. test a second case that avoids the factor you are checking.

  It also warns that 3·5·7 and 5·7·9 have a 5 inside, so they will not catch the mistake.
- **Slide 6 (Even products):** now gives the proof first, (2a)(2b) = 4ab, and the smallest case only after it. "Zero divides by every number — it tells you nothing."
- **Recap:** the proven rules ("Always: …"); "Anything else: the smallest case is only a candidate — cross out, then test a second case"; "Integer? Count the twos".
- **Card "Special products":** new intro, a "Why" column for every proven rule, and a second table: 3 consecutive odd numbers, smallest case 15, second case 693, always divisible by 3 only. There is a new tip about the method.
- **New guided question (q-r26-t16-04):** "n is a positive odd number. n(n+2)(n+4) is necessarily divisible by — 45 / 15 / 5 / 3". The key is 3. The old rule gives 15. The solution video crosses out 45, tests 7·9·11 and explains why 3 always works. It also shows the trap: 3·5·7 and 5·7·9 both divide by 15.
- **Practice for the method:** q-r26-t16-11 ((n+1)(n+2)(n+3) with n positive: the smallest case is 24, but only 6 is guaranteed) and q-r26-t16-12 (n² − 1 for odd n: n = 1 gives 0, which tells you nothing; the answer is 8).

Other corrections:
- **"Integers", slide 5:** the title was "Always positive", but x² can be 0. It is now "Never negative".
- **Q1 video (q-457):** "The exam always gives you that restriction" is now "The exam usually states it".
- **q-457 solution:** it said "(1) and (2) claim too much". Now: (1) claims too much; (2) and (4) contradict y < 0.
- **"Even & Odd", slide 8 (now "What a plug-in proves"):**
  - For ± and ×, parity depends only on the parities you put in, so one plug-in for each parity case settles the question.
  - Division needs three close plug-ins.
  - "A plug-in can disprove 'always' — it can't prove it."
- **Q7 and Q8 videos (q-463, q-464):** the plug-ins now "point to" the answer, and the teacher gives the reason (consecutive evens divide by 8; three in a row divide by 6). The Q8 intro said "Last question."; it now says "Question N".

## 2. Methods added (priority 2)
- **Signs of sums:** a new slide in "Integers":
  - (+) + (+) → +, and (−) + (−) → −;
  - mixed signs: the bigger size wins (−7 + 3 = −4, 7 + (−3) = 4);
  - bigger − smaller > 0, even for negatives (−2 − (−5) = 3).

  The recap and the sign card have these rules too.
  - Guided: q-r26-t16-01 (x < 0 < y and x + y > 0, so |y| > |x|), with a solution video.
  - Practice: q-r26-t16-05, -06 and -07.
- **Odd powers keep the sign** and **zero is neither positive nor negative:** added to slide "Never negative" and to the sign card.
- **Sums of consecutive integers:** the new lesson video "Sums of Consecutive Integers", placed after Question 4 (q-459). Its slides:
  - sum = count × middle;
  - with an even count, the middle ends in .5;
  - consecutive integers: an odd count means the sum divides by the count, and an even count means it never does (4a + 6);
  - counting integers from a to b gives b − a + 1, and counting evens or odds gives (b − a)/2 + 1;
  - neighbors: b² − a² = a + b (the review asked for this shortcut for strong students);
  - a recap.

  There is also a new card, "Sums of consecutive integers".
  - Guided: q-r26-t16-02 (the sum of 7 consecutive integers is 91, so the largest is 16) and q-r26-t16-03 (the sum of 4 consecutive integers is always even, but never divisible by 4). Both have solution videos.
  - Practice: -08 (sum of 5 is 85), -09 (which could be the sum of 4 consecutive integers: 26), -10 (integers from −5 to 20), -14 (10 consecutive integers with sum 5), -15 (odd integers from 11 to 59).
- **Odd product ⇔ every factor is odd:** added to "Even & Odd" slide 6, the recap and the parity card.
- **Count the twos:** a new slide in "Products of Consecutive Integers", with m²(n+1)/8 (always an integer) against m(n+1)/8 (not always). Q16 (q-472) is its guided question.
  - Practice: new q-r26-t16-13, plus q-483 and q-492. The q-472 and q-492 solutions now count the twos.
- **Plug-in rules on the cards:**
  - "A plug-in can disprove 'always' but cannot prove it" (parity card).
  - "Check that the choices give different values before you plug in; if two tie, choose other numbers" (the Q12 tip, now on the consecutive card and said on slide 4 of "Consecutive Integers").

## 3. Text (priority 3)
- Every question in the topic (guided and practice) has TeX math, ÷ or fraction bars instead of ":", and solutions that show the numbers.
- Several givens are stacked with `\begin{cases}`: q-457, q-466, q-467, q-468, q-480 and q-491.
- **Reworded stems:**
  - **q-460 (Q4):** it asked which statement "guarantees" an odd result, but the key was "can never be odd". It is now "Which of the following is true about the expression …?" with the choices "always odd / odd when x is odd and y is even / odd when x is even and y is odd / always even". The key is still choice 4, and the two spoken lines were adjusted.
  - **q-473:** "Which is not necessarily even? … (4) all of the above are even" contradicted itself. It is now "Which of the following expressions is necessarily even?", and the choices list combinations. The key is choice 4 (all three).
  - **q-465 (Q9):** the "number line" wording is gone (it came before T17 teaches number lines). The stem is now just "Given: p < q < 0 < r < s", and the video line was adjusted.
  - **q-471:** "are necessarily odd" → "is necessarily odd" (there is one answer).
  - **q-461 and q-463:** "4y:x³" and "(x²−1):2" are now fractions, and the stems say "most precise description".
- **Solutions:**
  - **q-489:** the "1..8" argument was wrong (4 of 8 primes is exactly half). It now uses n = 9 (4 of 9 are prime) and gives a counterexample for every wrong choice.
  - **q-471:** gives real examples where m is even (m = 0) and odd (m = 121).
  - **q-478:** a shorter method (sum = 3b, then b² − 1 = 24).
  - **q-469:** adds the "sum ÷ 3 = middle" route.
- **Videos and cards:** ":" as division was replaced with ÷ on boards, draw notes and labels (the "Integers" slide 4, "Even & Odd" slide 7, the videos for q-458, q-461, q-463, q-464 and q-469, and the parity card).
- The extra practice items (alg-extra-unit-t16-3-1 … 7) have NITE-style stems, TeX choices and worked solutions.

## 4. Practice (priority 5)
- Removed **q-477** (difference of squares of consecutive numbers). The same idea already appears in Q3, Q16 and q-482. q-482 stays, because it practices the new b² − a² = a + b shortcut.
- Added 11 exam-style items (q-r26-t16-05 … 15). Exam-level items for strong students now include -06, -09, -11, -12, -13, -14, q-480, q-488, q-489, q-490, q-491 and q-492.
- The practice section is ordered easy → hard (37 items).

## 5. For the teacher to decide
- **Topic order:** the review and the plan suggest teaching T16 before T15 (T15 uses the consecutive-product rules). The math API cannot reorder topics, so this patch does not change the order. It needs a course-level decision.
- **T15 q-444:** that question is where the old "smallest product" rule gave the wrong answer. T16 now teaches the candidate method, but the T15 solution itself belongs to the T15 patch.
- **API note:** existing solution-video titles and slide descriptions do not update when a stem changes, so the patch refreshes them itself (section 10 of t16.py).

## Pass 2 (teacher-approved plan, 2026-09-27)
**Removed:** nothing (per the plan).

**Restored:** q-477 (a, b, c consecutive positive integers, c² − a² = 48, b = 12). Text clean-up only: TeX, a full numeric solution (c² − a² = (c − a)(c + a) = 2(2a + 2) = 4b = 48, check 169 − 121 = 48). Placed in the practice after q-482 (same type, same difficulty).

**Summary video** `r26-t16-summary` "Integers: Summary", the last item of the advanced section, right before the practice. Slides: Summary · Multiply and divide · Signs of sums · Never negative · Consecutive integers · Sums in a row · Even and odd · Parity: plug in · Products in a row · Candidates and twos · Before you practice.

## 2026-10-05 cut repeats
Function `cut_repeats` (runs last). Nothing in topic 16 is recorded. Only "Sums of Consecutive Integers" was long compared to its questions; the other lessons are unchanged.
- **`r26-t16-consecutive-sums`**: 2.6 → 1.2 min. Kept: "Counting integers" and "Squares of neighbors" (no question video teaches them). Title slide says the next two questions teach count × middle.
  - Cut "Count × middle" → taught in Q5 `solve-q-r26-t16-02`; added there the "why" (the numbers pair up around the middle) + board item "Sum = count × middle".
  - Cut "Even count" (middle ends in .5) → one line + board item in Q6 `solve-q-r26-t16-03` on 1 + 2 + 3 + 4: middle 2.5, 4 · 2.5 = 10.
  - Cut "Divisible by the count?" → taught in Q6 (4a + 6). "Remember: an odd count…" → "The rule: an odd count…".
  - Cut "Recap".

## 2026-10-06 renumber pass
So the English course does not look like the Hebrew one: every Hebrew-derived question has new numbers, letters or story.
The idea, the trap, the level and the methods stay the same, and every guided solution video is rewritten to match
(speech, draw cues, video title, slide description). Nothing in Topic 16 is recorded, so nothing had to be kept as it was.
Function `renumber_pass(M)` in t16.py runs last (after `cut_repeats`).

**Counts:** 16 guided questions renumbered (q-457 … q-472) with their 16 solution videos rewritten; 20 practice questions
renumbered (q-473 … q-492); lesson examples renumbered in 4 lessons (Integers: 3 slides, Consecutive Integers: 2 slides,
Even & Odd: 6 slides, Products of Consecutive Integers: 2 slides). Practice: 38 → 26.
The English-made items (guided q-r26-t16-01 … 04, kept practice items, the English slides "Signs of sums", "Only a candidate",
"Count the twos", "Sums of Consecutive Integers", the summary) keep their numbers. The smallest cases 1·2, 1·2·3, 1·2·3·4, 2·2, 2·4
and the powers of 2 and 3 are the method itself and stay.

**Practice clean-up (38 → 26):**
- Copies removed: q-r26-t16-08 (sum of 5 = 85, same as X2 and guided Q5), -14 (10 consecutive with sum 5, the cancel-around-zero
  idea of X5), -15 (odd integers 11 to 59, same as X3).
- Extra warm-ups kept (3): X1 (a, b odd → a + b even), X2 (sum of 3 consecutive = 48), X3 (even integers between −7 and 9).
  Removed X4, X5, X6, X7.
- September items kept (3, types the Hebrew practice does not have): -06 (signs from a sum and a product), -09 (which number can
  be the sum of 4 consecutive integers), -11 (the candidate method). Removed -05, -07 (sign of sums/differences: guided Q2, Q13
  and q-485), -10 (counting a range: X3), -12 (n² − 1 by 8: guided Q10, q-492), -13 (count the twos: guided Q20, q-492).
- I kept 26 rather than the audit's 25 so every kept September item practises a type nothing else covers.

**Checks:** every key brute-forced in Python over integer ranges (exactly one correct choice; for "necessarily" questions every
wrong choice has a counterexample); every plug-in and method in the videos recomputed; the original traps are still choices.
Duplicate check over the whole build of topics 1–16 (all question stems/choices, lesson boards and draw cues, cards): no new
question equals another question or a lesson/card example. `python3 math_check.py 16 32` → PROBLEMS 0, WARNINGS 0, LAYOUT 0.
Rendered all 4 lessons and all 16 solution videos and looked at them. No quadratic trinomial was added (q-484 keeps the
original's perfect-square step).

| id | old (Hebrew) | new | answer |
|---|---|---|---|
| q-457 (G1) | y ≠ 0, x⁶y⁵/\|y\| < 0 | a ≠ 0, a³b⁴/\|a\| < 0 | a < 0 (4); trap "a < 0 and b < 0" |
| q-458 (G3) | consecutive evens a<b<c, (c² − a²)/b | consecutive evens p<q<r, (r² − p²)/(2q) | 4 (3); trap 2 = gap of 1 |
| q-459 (G4) | (d−a)/(c−b) − (a−c)/(d−c) | (r−p)/(s−r) − (q−s)/(r−q) | 4 (4); trap 0 = lost minus |
| q-460 (G7) | xʸ + yˣ + 7 + 6x, x+y odd | mⁿ + nᵐ + 9 + 4n, m+n odd | always even (1) |
| q-461 (G8) | x even ≠ 0, y odd: 4y/x³ | a odd, b even ≠ 0: 2a/b² | always a fraction (2); trap "anything" |
| q-462 (G9) | x − y = 4 | a − b = 2; choices a²+b²+3b, a²−b², 4a−b, 3a²+2b | a² − b² (2) |
| q-463 (G10) | x odd, (x² − 1)/2 | n odd, (n² − 1)/4 | always even (1) |
| q-464 (G11) | (x³ − x)/3 always even | (x³ − x)/2 always — | divisible by 3 (4) |
| q-465 (G13) | p<q<0<r<s, necessarily negative | w<x<0<y<z, new choices | (x−w)(y−z) (1) |
| q-466 (G14) | a<b, ab<0, necessarily positive | x>y, xy<0 | (y−x)/y (2) |
| q-467 (G15) | d<e, d+e+f>0, makes f positive | p>q, p+q+r<0, makes r negative | 0 < q (4); trap 0 < p |
| q-468 (G16) | two pairs of consecutive evens, (n²−m²+q²−p²)/(p+n) | two pairs of consecutive integers, (b²−a²+d²−c²)/(b+c) | 2 (3); tie trap at a = c = 1 kept |
| q-469 (G17) | consecutive integers, a²+b²=c², sum 12 | consecutive evens, sum 24 | 24 (2); 12 (3-4-5) is now a trap |
| q-470 (G18) | x = (a−6)² + (a+5)³ | y = (b−3)² + (b+8)³ | y odd (4) |
| q-471 (G19) | 2m+1 = (p+1)²q⁵(r−1)² | 2k+1 = a³(b+1)²(c−5)⁴ | a (2) |
| q-472 (G20) | m even, n odd, /8 | a odd, b even; non-integer ab²/8 | (4) |
| q-473 | x − y = 6 | m − n = 8 | all three (1) |
| q-474 | pencils 4 / 5, class D odd | café chairs 4 / 7, large tables odd | odd (3) |
| q-475 | m, n odd; m·n/2 | a, b odd; (a/2)·b | (2) |
| q-476 | p⁵q⁴ < 0 | m⁶n³ < 0 | n < 0 (1) |
| q-477 | c² − a² = 48 | z² − x² = 56 | y = 14 (2) |
| q-478 | product = 8 × sum | product = 16 × sum | b = 7 (4) |
| q-479 | 10⁷ + 7¹⁰ | 6⁵ + 5⁶ | odd (4) |
| q-480 | n<m, m²n even, m+n odd; mn² odd | a<b, ab² even, a+b odd; a²b odd | (2) |
| q-481 | primes p ≤ q; p(q+1) | primes a ≤ b; a(b+3) | (3) |
| q-482 | a² − b² = −9 | x² − y² = −13 | 13 (1) |
| q-483 | n³/2: 54, 66, 86, 256 | n³/2: 74, 108, 62, 90 | 108 (2) |
| q-484 | a² + c² = 12b − 16, sum 9 | a² + c² = 20b − 48 | 15 (2) |
| q-485 | x<y<z<0; x(y+z) | a<b<c<0; c(a+b) | (1) |
| q-486 | 2n+1 = j(4j+1) | 2k+1 = t(6t+5) | odd (2) |
| q-487 | x = a²−b²+3a−3b | x = m²−n²+5n−5m | even (3) |
| q-488 | (m+1)(4n+m) | (a−1)(6b+a) | even (4) |
| q-489 | at least half of 1..n (n>1) | more than half of 1..2n+1 | odd (4) |
| q-490 | ab = 36 | ab = 100 | if a odd then b even (1) |
| q-491 | a<b, ab<c; b<0 and c<0 impossible | x>y, xy<z; x<0 and z<0 impossible | (3) |
| q-492 | m even, n odd; m(n−1)(n+1)/16 | a odd, b even; b(a−1)(a+1)/16 | (3) |
| lesson Integers | (−2)(5)(−3)(−4), (−2)(−5)(−3)(−4); (−12)÷(−3), (−12)÷3; x = −7 | (−4)(3)(−2)(−5), (−4)(−3)(−2)(−5); (−18)÷(−6), (−18)÷6; x = −9 | – |
| lesson Consecutive | 0…4; −2, −1, 0; a = 2, b = 3; "a could be 17" | 5…9; −3, −2, −1; a = 8, b = 9; 23 | – |
| lesson Even & Odd | 6, 14, 42, 684, 7,320; 6+10, 9+13, 6+9, 13−9; 4·2, 3·5, 2·3; 6+9−4+13+7, 8+11−6+15; 8·11+7·12−9·5, 6(x+3); 15÷5, 5÷3, 10÷5, 14÷3, 6÷2, 20÷2, 10÷6 | 8, 16, 38, 572, 9,150; 8+12, 7+11, 8+7, 11−7; 4·6, 3·7, 2·5; 8+5−2+11+3, 4+7−10+9; 6·13+5·10−3·7, 4(x+5); 21÷7, 7÷3, 12÷3, 8÷3, 18÷6, 12÷2, 6÷4 | – |
| lesson Products | 1·2 … 4·5 (2, 6, 12, 20); 3·4·5 = 60 | 3·4 … 6·7 (12, 20, 30, 42); 7·8·9 = 504 | – |

## 2026-10-06 review
Independent check of the renumber pass (16 guided + 20 practice, 16 solution videos, 4 lessons, practice removals), built with
and without `renumber_pass` and compared. Every key recomputed in Python (brute force; exactly one correct choice, traps still
choices), every video step redone with the new numbers, no old numbers left; lesson examples re-checked (sign counts, parity
counts, division examples). Duplicate check over a build of topics 1–16: no question equals another question or a lesson/card
example. Nothing in topic 16 is recorded. No quadratic trinomial added.
Fixed (the kind of condition had changed from the Hebrew; restored with new numbers):
- q-468: the pass changed consecutive EVENS to consecutive integers (answer 2). Back to two pairs of consecutive even numbers,
  new letters and denominator: a<b and c<d consecutive evens, a + d ≠ 0, (b² − a² + d² − c²)/(a + d). Choices 4(a+c), 2, a+c, 4 ·
  key 4; 2 is the gap-of-one trap. Video keeps both methods: formula three (gaps of two → 4(a+c+2)/(a+c+2) = 4), and the plug-in
  with the tie check (a = c = 2 gives 16, 2, 4, 4 → tie; a = 2, c = 8 gives 40, 2, 10, 4; b = 4, d = 10: 48/12 = 4).
- q-469: the pass changed consecutive integers to consecutive EVENS. Back to consecutive integers x<y<z with x² + y² = z²; it now
  asks which could be x + z: choices 10, 8, 12, 6 · key 2 (3, 4, 5 → 8; −1, 0, 1 → 0 not a choice). Trap 12 = the sum of all three
  (the Hebrew's answer). Video keeps both methods: one unknown (y² = 4y, two solutions), and testing the answers (middle =
  (x + z) ÷ 2).
- q-489 (practice): the pass made it "more than half of 1 … 2n+1" (only odd-length lists, easier). Back to the Hebrew kind with new
  numbers: n > 1, at least half of the integers from 2 to n are — not prime / even / odd / prime · key 2 (brute force n = 2…299:
  even never below half; odd fails n = 4, prime fails n = 10, not prime fails n = 3).
`python3 math_check.py 16 32` → 0 / 0 / 0. Rendered solve-q-468, -469, -472.
- q-464 (follow-up, teacher: same message): back to the Hebrew answer "always even" with the trap "divisible by 4", new form
  (n − n³)/3 = −(n − 1)n(n + 1)/3 = −6k/3 = −2k. Choices divisible by 4 / a fraction / even / odd · key 3 (Python, n = −50…50:
  always an even integer, not always divisible by 4). Video keeps both methods: plug in n = 1, 2, 3 → 0, −2, −8 (−2 rules out
  "divisible by 4"; a minus doesn't change parity), and the math way (common factor, contracted formula, three in a row → 6k).
  Written solution rewritten. `math_check.py 16 32` → 0 / 0 / 0; rendered solve-q-464.

## 2026-10-06 Hebrew back-check
Compared every guided and practice question, every lesson slide and the cards with the teacher's Hebrew video subtitles
(01-Algebra-Original-Subtitles.txt, lines 15738–17362). Nothing in topic 16 is recorded. Five guided questions and one lesson
example had landed back on the Hebrew videos' numbers (mostly the Hebrew expression with the letters swapped); fixed in
`hebrew_backcheck(M)` (runs last). Same type, trap, level and methods; solution videos rewritten (speech, draw cues, titles).

| id | Hebrew video | was | new | answer |
|---|---|---|---|---|
| q-457 (G1) | a⁴b³/\|b\| < 0 → b < 0 | a³b⁴/\|a\| < 0 | a⁵b²/\|a\| < 0 | a < 0 (4); trap "a < 0 and b < 0" |
| q-461 (G8) | x even, y odd: 2y/x² | a odd, b even: 2a/b² | 6a/b² (= 3a/2k²); plug-ins 3/2, 9/2, 9/8 | always a fraction (2) |
| q-462 (G9) | x − y = 2; 2x−y, x²+y²+3x, 3x²+2y, x²−y²; plug 3, 1 | a − b = 2; same choices; plug 3, 1 | a − b = 6; a²+b²+5b, b²+ab, 6a−b, 5a²+4b; plug 7, 1 (55, 8, 41, 249) | b² + ab = b(a+b) (2) |
| q-463 (G10) | x odd, (x² − 1)/4; plug 5, 1, 3 | (n² − 1)/4; plug 5, 1, 3 | (9n² − 1)/4 = (3n−1)(3n+1)/4; plug 1, 3, 5 → 2, 20, 56 | always even (1) |
| q-472 (G20) | a(b+1)²/8, a²b²/8, ((a+b)²−(a−b)²)/8, (b−1)(b+1)/8 | b(a+1)²/8, (a−1)(a+1)/8, ((a+b)²−(a−b)²)/8, ab²/8 | b³(a+2)/8, (a+1)(a+3)/8, ((a+b)²+(a−b)²−2a²)/8, ab²/8 | ab²/8 (4) |
| lesson Even & Odd, slide 6 | 6·13 + 5·14 − 7·9; 4x + 5y − 8 | 6·13 + 5·10 − 3·7; 4(x+5), 4x+5 | 4·15 + 9·8 − 7·3; 2(x+7), 2x+7 | – |

Left on purpose: q-465, q-466, q-467 (letter-only sign questions — letters, given and choice order already differ from the
Hebrew; no numbers to change), q-460 (mⁿ + nᵐ + 9 + 4n vs 4y + xʸ + yˣ + 5: only the 4 is shared), q-458/459/464/468/469/470/471
(different numbers or condition), the lesson demos 6 ÷ 2 = 3 and 2 · 3 = 6 and the smallest cases 1·2·3 etc. (the method
itself). Keys brute-forced in Python (exactly one correct choice; traps still choices); duplicate check over topics 1–38.
`python3 math_check.py 16 32` → 0 / 0 / 0. Rendered the Even & Odd lesson and solve-q-457, -461, -462, -463, -472.


## 2026-10-07 methods spread
Function `spread_methods` (runs last). Went through all 46 questions (20 guided + 26 practice) for the 2026-10-06 methods.
- **Mirror test** (topic 13), one-letter form: a letter that appears only in an even power can change sign and the given stays the same, so any choice that fixes its sign is out. Written lines only:
  - `q-457` (a⁵b²/|a| < 0): flip b → choices 2 and 3 (they fix b's sign) are out; a⁵ < 0 → a < 0 (choice 4).
  - `q-476` (m⁶n³ < 0): flip m → choices 2 (m < 0) and 4 (0 < m) are out; n³ < 0 → n < 0 (choice 1).
  Checked by computer (grid of values: the given is unchanged by the flip; only the key is always true). No extra slide: the q-457 video already says "we learned nothing about b", and the one-letter flip is a small step beyond the lesson's two mirrors (flip all signs / swap).
- Not added: the mirror test does not fit q-465, q-466, q-467, q-485, q-491, q-r26-t16-01 (the given changes in every mirror); q-r26-t16-06 (it would only remove one choice, slower than the existing line). Tag it: the parity / divisibility questions already write the tags (q-461 b = 2k, q-483 n = 2k, q-r26-t16-03 / -09 4a + 6, q-463 8k, q-472 / q-492 count the twos); products of consecutive numbers (q-r26-t16-04, -11) are outside its use. Power count: q-458 / q-468 have letters in the choices but "consecutive even" adds numbers (b = a + 2), so the powers don't count — not used. Pick values: the consecutive-number questions already check with values.
- Recorded videos: none in topic 16.
`python3 math_check.py 14 15 16 32`: PROBLEMS 0, WARNINGS 0, LAYOUT 0.
