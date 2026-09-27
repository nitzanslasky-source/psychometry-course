# Review — Topics 15 and 16

Note on keys: `correct:` is 0-based (0 = choice 1). I checked every guided and practice question with that reading. **All keys are correct in both topics.** The problems are in some rules, some solution texts and the topic order.

---

## Topic 15: Division & Remainder

**Depends on:** T1 (number words: remainder) · T4 (multiplication formulas: Q4, Q10) · T5 (units-digit method: Q11, q-448) · T14 (LCM: q-438, extra-6; "no shared prime factor": Q7; number of divisors: q-445) · **T16** (products of consecutive integers: Q10, q-444, q-447, q-449, extra-5) · T9/T10 (roots: q-455) · T8 (powers: extra-2) · **T22/T23** (ratio and percent: Q5, q-439; these come later).
**Needed by:** T16 (divisible by 4/8/16: Q16, q-483, q-492) · T18 (digit problems) · T21 (cycles use remainders).
**Order:** T15 and T16 need each other. I suggest **T16 before T15**. T16 needs only "divisible by 4 or 8", and students can check that by simple division.

### Most important points
1. **Slide 5 teaches a rule that is wrong in general.** It says: "Use the same trick for any bigger number that isn't in the table." Students will check 12 as 2·6 or 18 as 3·6, and get wrong answers. The condition "the two parts share no prime factor" appears only in the Q7 video. Put it on slide 5 and on the memory card: 12 = 3·4 (not 2·6), 18 = 2·9, 24 = 3·8.
2. **Slide 7 (zebras) teaches the nested-fraction rule wrongly.** It says "divide by four — and by five". For 1/2 of 1/4 this rule gives 4, but the true answer is 8. Say "4·5 = 20" and show "k → 5k → 20k", like the Q1 video (Method 2) does.
3. **Many advanced and practice questions use tools that the lesson never teaches:**
   - products of consecutive integers (Q10, q-444, q-447, q-449, extra-5), taught only in T16;
   - "a remainder by 6 tells you the remainder by 3, but not by 4 or 9" (q-441, q-453), said only in the Q13 video;
   - the digit sum gives the *remainder* when you divide by 3 or 9 (extra-3);
   - units-digit cycles of powers (extra-2);
   - "mod" and "≡" notation in the solutions of Q11, q-444, q-448, q-456. Students never saw this notation, and a weak student will be lost.

### 1. Coverage — missing or thin
- **Reverse remainder questions.** Example: "100 divided by n leaves remainder 4. How many n are possible?" The idea: n divides 96, and n > 4. This is a common NITE type and it is missing.
- **Counting multiples in a range** (Q8). Teach the rule: the number of multiples of d from A to B = ⌊B/d⌋ − ⌊(A−1)/d⌋. The video's "1/10 is more than 1/11" argument is fine for long ranges. In a short range it can fail by 1.
- **Remainder of a difference.** Example: a leaves 2 and b leaves 5 when divided by 7. Then a − b leaves 2 − 5 = −3, so the remainder is −3 + 7 = 4. Slide 12 covers only sums and products.
- **Remainder when the divisor changes** (from 10 to 5, from 6 to 3): make it one line on the card.
- **The rule for 11 with 4 digits** (1,331, 2,442): the alternating sum. The q-440 solution names "alternating sum", but the lesson calls it "outer − middle". Also, 482 gives −2 with the lesson's rule, and negative results are never explained.
- **Divisibility of sums:** "if d divides a and d divides a + b, then d divides b" (used in Q14 claim 3). Put it on the board once.

### 2. Teaching quality per level
- **Weak:**
  - Slides 2–6 are clear, with good examples.
  - They get lost at Q10 ("three consecutive integers always divide by 6" is not taught yet) and at the "mod" solutions.
  - q-445 (lockers) and q-455 (√3) are far above this level.
  - The slide 12 "bonus" is used later (Q14, q-443, q-456), but the memory card leaves it out. Add it.
- **Medium:**
  - The method advice is mixed. Q9 and Q10 say "plugging in is the recommended route, by far". Q13 says "use plugging in only if you can't solve it the first two ways". The memory card says "plugging in x = 0 is usually fastest". But in Q10, a = 1 gives 0, and 0 kills every choice.
  - Give one clear rule:
    - A plug-in can **disprove** "necessarily". One counterexample is enough.
    - A plug-in cannot **prove** "necessarily".
    - Avoid values that give 0.
- **Strong:**
  - Bored by slides 2–3.
  - Gets good material in Q8, Q10, q-444, q-445 and q-449.
  - Missing for them: the reverse-remainder type, the remainder of a difference, and the shortcut "a known remainder → N − r is a multiple of d".

### 3. Correctness
- All keys are correct.
- **Slide 5 and slide 7:** rules stated too generally (see points 1 and 2 above).
- **q-448 solution:** the sentence "since 3x + 9 must end in 10's digit-0 pattern: 3x ≡ 1 mod 10" is garbled. Write instead: "13x + 9 ends in 0 → 3x ends in 1 → x ends in 7."
- **q-452 solution:** says "no carry for d ≤ 8", but does not handle d = 9. (99999 + 1 = 100000, digit sum 1, remainder 1 — the answer is still 1.) Add this one line.
- **alg-extra-unit-t15-3-1 solution:** "plus 8; reduce that to remainder 3" is confusing. Write: n + 5 = 5(k + 1) + 3.
- **Memory card:** the "x = 0" tip conflicts with the Q10 video and with T16 ("never plug in 0"). Say when 0 is safe (the remainder-expression type, as in Q4) and when it is not ("necessarily divisible by").
- **Q1 solution:** it is correct. But slide 7 of the lesson ("÷4 ✓ and ÷5 ✓") teaches a different rule, so the lesson and the solution disagree.

### 4. Methods and tricks to add
- **Slide 5:** "Split into parts with no common factor", with a quick counterexample: 6 divides by 2 and by 6, but not by 12.
- **Slide 8:** "N − r is divisible by d". Then one reverse question on the board.
- **Slide 3:** "the digit sum gives the remainder by 3 or 9". Example: 12,345 → 15 → remainder 6 when divided by 9.
- **Slide 12:** add the difference case, with a "+7 if negative" note. Add the same to the card.
- **Before Q10:** a 30-second "three in a row → divisible by 6" (or move T16 first).
- **Units digit:** "the last digit of a product depends only on the last digits". Use it for Q11 and q-448 instead of mod.

### 5. Practice
- 20 practice questions + 7 extras is enough.
- The spread is wide: q-439, q-441 and q-454 are easy; q-444, q-445 and q-455 are very hard. The middle is thin.
- q-445 (lockers) is really a T14 divisor-count question.
- q-455 is a roots question. Its divisibility content is trivial.
- Missing practice types:
  - reverse remainder;
  - counting multiples (only Q8);
  - remainder of a difference;
  - a "12 = 3·4" check with a 2·6 trap.
- Good: q-437, q-450 and q-453 use the taught methods directly.

### 6. Verdict
- **Weak:** can do signs 2–11 and simple remainders. Will fail the consecutive-product and "mod" questions.
- **Medium:** mostly ready. May fall into the 2·6 trap and the nested-fraction trap, because the lesson itself teaches them.
- **Strong:** ready for most items. Gaps: reverse remainder, counting multiples, remainder of a difference.

**Top 3 changes:**
1. Fix slide 5 (the no-common-factor condition) and slide 7 (nested fractions → multiply the denominators).
2. Put T16 (consecutive products) before T15, or add one slide on it here. Remove "mod" notation from the solutions.
3. Add a slide on "N − r divisible by d", with reverse-remainder and counting-multiples questions. Put one consistent plug-in rule on the card.

---

## Topic 16: Integers

**Depends on:** T1 (zero, integer, positive) · **T4** (multiplication formulas: Q2, Q7, Q10, Q12, Q13, Q16, q-477, q-482, q-487) · **T7** (quadratic equations: Q13, q-478, q-484) · T8 (powers: parity of powers, q-479) · T13 (absolute value: slide 5, Q1) · T12 (inequalities: Q11, q-491) · **T17** (number-line picture: Q9; this topic comes later) · T14 (primes, "count the twos": q-481, q-489, q-490, Q16) · T15 (divisible by 4/8/16: Q16, q-483, q-492).
**Needed by:** **T15** (Q10, q-444, q-447, q-449, extra-5) · T17 · T18 · T20 · T21.

### Most important points
1. **The "Special products" rule is false as a general rule.** Slides 4 and 7 and the memory card say: "Plug in the smallest numbers — the product is the divisor." This works only for the six cases in the table. Counterexamples:
   - Three consecutive odd numbers: 1·3·5 = 15, but 7·9·11 = 693 is not divisible by 5.
   - n(n + 2): 1·3 = 3, but 2·4 = 8 is not divisible by 3.
   - T15 q-444: the smallest case gives 120, but only 24 is guaranteed. A student who follows this rule picks 60 (wrong).

   The correct rule: the smallest case gives the **biggest possible** divisor. Use it to cross out choices that don't divide it. Then test a second value before you trust the rest.
2. **Sign of a sum is never taught.** The sign lesson covers only × and ÷. But Q10 (choice 2), Q11, q-485 and q-491 need these rules:
   - negative + negative = negative;
   - if the signs are different, the sign of a sum depends on which number is bigger in size.

   Add one slide.
3. **Sums of consecutive integers are missing.** "Sum = count × middle (average)" is only said in the Q13 video, but extra-2, extra-5 and extra-7 need it. Also missing: the NITE trap "the sum of 3 (any odd number of) consecutive integers divides by 3; the sum of 4 consecutive integers never divides by 4".

### 1. Coverage — missing or thin
- **Odd powers keep the sign** (Q1, q-476 need this). Slide 5 shows only even powers.
- **"An odd product means every factor is odd"** (Q15, q-486, extra-4). This is said only in the Q15 video. Put it on slide 6 and on the card.
- **Counting integers in a range:** from a to b inclusive there are b − a + 1; for even numbers only, see extra-3. Not taught.
- **"Count the twos"** (Q16 video) is a strong method for "is it an integer / divisible by 8" questions. Make it a lesson slide.
- **Zero is neither positive nor negative:** it is only said in the Q10 video. Put it on the sign card.

### 2. Teaching quality per level
- **Weak:**
  - The sign and parity videos are short and clear.
  - They get lost at Q2, Q12 and Q13: difference of squares plus quadratics, with no reminder.
  - Q9 uses a number-line picture before T17 teaches it.
  - Slide 8's "three close plug-ins" feels like proof, but it is not.
- **Medium:**
  - "Plug in" is presented as almost always best. But the Q16 video warns that plugging in can fail.
  - Teach one clear rule:
    - A plug-in can only **disprove** "always".
    - For division, test both parities of every letter.
- **Strong:**
  - Bored by slides 2–4 of the sign video.
  - Q11, Q14, Q15 and Q16 are good exam-level questions.
  - Wants the shortcut for consecutive a and b: b² − a² = a + b (Q2, q-477, q-482).

### 3. Correctness
- All keys are correct.
- **Special products rule:** false in general (see point 1).
- **q-489 solution:** it claims "primes fail quickly — among 1..8 only 2, 3, 5, 7 are prime". But that is exactly half, so it does *not* disprove "at least half are prime". Use 1..9 instead (4 primes out of 9).
- **q-473:** the stem asks "which is **not** necessarily even?", and the key is "(4) all of the above are even". The stem and the answer contradict each other. Reword the stem: "Which of the following is true?"
- **Q4 (q-460):** the stem asks which statement "guarantees the expression will be odd". The key, "the expression can never be odd", is not a condition. Reword the stem: "What can you say about the expression?"
- **Slide 5:** the title "Always positive" is wrong, because x² can be 0. Change it to "Never negative".
- **Q1 solution:** "(1) and (2) claim too much" — no: (2) *contradicts* y < 0.
- **Minor:**
  - Q15 asks "which … **are** necessarily odd" (plural), but only one answer is correct.
  - The Q1 video says "the exam always gives you that restriction". That is too strong.

### 4. Methods and tricks to add
- **New slide after slide 4 (signs of sums):**
  - neg + neg < 0;
  - with mixed signs, the bigger size wins;
  - "bigger minus smaller > 0" (this is now only in the Q9 video).
- **Consecutive video, new slide:**
  - sum = count × middle;
  - an odd count → the sum divides by the count;
  - the (b² − a² = a + b) shortcut.
- **Parity slide 6:** add "odd product ⇔ all factors odd".
- **Special products:** replace "the product is the divisor" with "the smallest case gives the candidate — cross out, then check one more value". Show the counterexample 1·3·5 vs 7·9·11.
- **Q12 video tip:** "check that the choices give different values before you plug in". This is excellent. Put it on a card.

### 5. Practice
- 20 practice questions + 7 extras is enough, with a good easy → hard spread.
- Repetitive: the difference-of-squares consecutive item appears four times (Q2, Q12, q-477, q-482). Replace one of them with a sum-of-consecutive item ("the sum of 5 consecutive numbers is 85 — what is the largest?").
- Missing practice types:
  - sign of a sum (only q-485);
  - counting integers in a range;
  - a sum of 4 consecutive integers and divisibility.
- The practice uses the taught methods well: parity by deleting powers (q-479, q-488), and the odd-product rule (q-486).

### 6. Verdict
- **Weak:** OK on pure sign and parity questions. Lost on the algebra-heavy consecutive questions, and may trust a wrong "smallest product" answer.
- **Medium:** ready for most items. Needs the sign-of-sum rule and a safe plug-in rule.
- **Strong:** ready. Needs the sum-of-consecutive traps and the "count the twos" method as a lesson slide.

**Top 3 changes:**
1. Fix the Special-products rule (the smallest case gives a candidate, not a guarantee) and show a counterexample.
2. Add a slide on signs of sums, and one on sums of consecutive integers (count × middle, odd/even count). Put "odd powers keep the sign" and "odd product ⇔ all factors odd" on the cards.
3. Teach T16 before T15, and fix q-473, q-460 and the q-489 solution.
