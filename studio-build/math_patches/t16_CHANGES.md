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
