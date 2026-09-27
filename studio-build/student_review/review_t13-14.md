# Review: Topics 13 and 14

Note on keys: `correct:` is 0-based (0 = choice 1). I checked every question and every key with that reading. **All keys in both topics are correct.** The errors I found are in teaching text and solution wording (listed under "Correctness").

---

## Topic 13: Absolute Value

**Depends on:**
- T12, the "small side / big side" rule for x² inequalities. Slide 9 says "like the second-degree inequalities from before".
- T9, √(x²) = |x|, used in q-379.
- T5, the shortcut formula (a ± b)², used in Q11 method 2 and q-374.
- T8, powers of negative numbers (odd/even exponent), used in q-376.
- T7, two equations with two unknowns, used in Q10.
- T16, sign rules for products (+·− = −), used in Q1, q-373 and q-381. **T16 comes later.** Either move the sign rules earlier, or add one board line here.
- The "necessarily / possible / not necessarily" wordings (Q6–Q9). The course first explains them in Q9 ("the wording is new"). If T20 teaches them, T20 must come first. If not, teach them here.

**Needed by:** T14 Q7 (|x − y|), T16 (slides on |y| > 0), T17 (number line, distances), T20.

### Most important points
1. **Slide 7 and the memory card teach "|x| = −x (x < 0)". The extra practice (alg-extra-unit-t13-3-6) marks "x < 0" as wrong. The key there says x ≤ 0.** Both statements are true, but they answer different questions. As a definition, "x < 0" is fine. As a sign clue ("given |x| = −x, what do we know?"), the answer is x ≤ 0, because zero works too. A student who learned the board will pick choice 1. q-380 uses the same idea (|A| = −A means A ≤ 0).
   - Fix: add a 4th sign clue to slide 7 and the card: "|x| = −x → x ≤ 0 (zero or negative)".
2. **|x − a| as distance between x and a is never taught, but the solutions use it.** q-372 ("distance from x to −2") and extra-5 (min of |x−3|+|x−5|) depend on it.
   - This is also the fastest method for inequalities: |x − 2| < 4 means "x is within 4 of 2", so −2 < x < 6 in one step.
   - Add one slide after slide 9, with a number-line picture: centre 2, arrows of 4 to each side.
3. **A real NITE question type is missing: the reverse direction.** "Which inequality describes −3 < x < 7?" Answer: |x − 2| < 5 (centre = midpoint, radius = half the length). Strong students need this. It follows directly from point 2.

### 1. Coverage: missing or thin
- **Inequalities with a negative right side:** |x| < −3 has no solution, and |x| > −3 is true for all x. Slide 8 covers this only for equations. This is a common trap.
- **Equations where the right side contains x** (Q10: |x| = 6 + x; q-380). Students must check that the right side is ≥ 0, or check each candidate in the original equation. The course never says this. Add one line to slide 8: "Letter on the right side? Check your answers."
- **x/|x| = ±1** (1 if x > 0, −1 if x < 0). Q5 is exactly this. One board line would make Q5 a 5-second question.
- **|a − b| = |b − a|** and **|x|² = x²**. These are only mentioned in passing (Q9 video: "behaves like an even power"). Put both on the rules card.
- **|a/b| = |a|/|b|**. Q1 choice 4 uses it. Add it to rule two on slide 5.

### 2. Teaching quality per level
- **Weak:**
  - Slide 3, "The minus just drops off", is dangerous with letters. A weak student will write |−x| = x, or |x| = x for all x. Add a warning with a number: "x = −3: then −x = 3. For letters the minus does NOT just drop."
  - Slide 9: the explanation switches to "absolute value of x bigger than five" (not on the board). It lists only whole numbers (6, 7, 8…). This is confusing. Use the board example, and show 4.5 as well.
  - There is a big jump from Q5 (easy) to Q6–Q13 (all hard). Put one medium question between them, such as |2x − 1| = 7 or |x| < 5 with integers.
- **Medium:**
  - Follows well. Q10 and Q11 show three methods each, which is good.
  - Q8 is heavy, but the video is slow and clear.
  - This student needs a short card: "4 question wordings: necessarily true / could be true / cannot be true / not necessarily true". Put it before Q6.
- **Strong:**
  - Bored by slides 2–4.
  - Would like the distance and midpoint method (points 2 and 3) and x/|x| = ±1.
  - The exam-hard traps here are good (Q8, Q9, q-381, q-385).

### 3. Correctness
- **extra-t13-3-1 solution is broken template text:** "The expression inside the bars is negative b; its distance from zero is b." It should say "3 − 8 = −5; its distance from zero is 5."
- **Q12 video, slide 2:** "Six to seven is the bait — that's what you get if you forget to subtract the one." This is wrong. If you forget to subtract 1, you get 5.5 < x < 6.5. The range 6 < x < 7 comes from **adding** 1 instead of subtracting. Fix the sentence.
- **Q9 video:** the board line "|a+b|² > 4 = (a+b)² > 4" is a broken chain. Write it as two lines: "|a+b|² > 4" and "|a+b|² = (a+b)²".
- **Slide 7 vs extra-6:** see Most important point 1.
- **Colon used for division** in solutions: Q5 "2x:|x|", Q6 "c = a:3", q-372 "x = 1:2", q-377 "x:y", q-380 "−1:2", q-381 "P:Q". In English "1:2" reads as a ratio, not one half. Use a fraction or "÷".
- All 13 guided questions, 15 practice questions and 7 extras have correct keys. q-385's counterexamples check out.

### 4. Methods to add or teach differently
- **Distance picture** (slide after 9): "|x − a| = distance from x to a. |x − a| < r: within r of a. |x − a| > r: farther than r." Then solve Q3 and Q4 by drawing.
- **Midpoint trick** (same slide): range a < x < b ↔ |x − (a+b)/2| < (b−a)/2.
- **x/|x| = ±1** on slide 7.
- **Plug-in warning** (slide 10): choose a number that is not special. Q5 shows the problem: x = −3 made −x equal to 3. Say it on slide 10: "avoid 0, 1, −1, and numbers that appear in the answers."
- **Squaring both sides** to remove bars (Q11 method 2, q-374): it is legal because both sides are ≥ 0. Teach it once on a slide instead of only inside a solution.

### 5. Practice
- Quantity is good: 13 guided, 15 practice, 7 extras.
- Order is wrong: the 15 practice questions are mostly exam-hard (q-376, q-381, q-382, q-385), and the easy extras come last. Put the extras first, as a warm-up.
- The extras' solutions are one line and very terse. Weak students need one worked step each.
- Missing practice: negative right side in an inequality, the reverse-midpoint question, and one more "what is the expression" plug-in item (like Q5).
- Not repetitive. Good variety of wordings.

### 6. Verdict
- **Weak:** Can do the basic equations and inequalities (Q2–Q4). Will get lost at Q6–Q13 and fall into the "|x| = −x" and "minus drops off" traps.
- **Medium:** Will solve most exam questions. Needs the "right side contains x" check and the 4 wordings card.
- **Strong:** Will be fine, and faster with the distance and midpoint tools.

**Top 3 changes:**
1. Fix the sign clue: "|x| = −x → x ≤ 0" (slide 7, card). Also fix the broken extra-1 solution and the Q12 "bait" sentence.
2. Add a "distance on the number line" slide: |x − a|, then the midpoint/reverse question and a negative right side.
3. Teach the 4 question wordings and the sign rules before Q6 (or confirm that T16/T20 come first). Add one medium bridge question between Q5 and Q6.

---

## Topic 14: Prime Numbers

**Depends on:**
- T8, exponents (a^c divides a^d when c ≤ d; Q14, Q4, q-410).
- T9, roots (√n in Q10, q-420, and √3 in Q9).
- T4/T5, taking out a common factor (Q13, and the GCD explanation in Q4 and theory B slide 2).
- T13, absolute value (Q7: A = |x − y|).
- T2, "reduced fraction" (q-419).
- T16, parity (odd + odd = even) in Q11, q-412 and q-415. **T16 comes later.** Q11 video explains parity in two sentences, which is enough for Q11, but the practice needs it too.
- T15, divisibility rules (digit sum for 3). You need these to see that 87 = 3·29 (q-403) or 51 and 57 are not prime (q-407). **T15 comes later.**

**Needed by:** T15 (divisibility, "parts must not share a prime"), T16 (guaranteed divisors, consecutive products), T18, T19, T28.

### Most important points
1. **Q4 (GCD) and Q5 ("greatest guaranteed divisor" = LCM) come in section A, before "Factor tools" (theory B) teaches them.** Q4 video even says "least common multiple" with no explanation. Move Q4–Q5 after theory B, or move theory B slides 2–3 into theory A.
2. **The LCM rule is taught vaguely.** The words are "offset it", "count it once" and "shared ones once" (recap slide 7, memory card).
   - For 72 = 2³·3² and 90 = 2·3²·5, a student can read "shared once" as 2·3·5 = 30.
   - Say it as the mirror of the GCD: "**GCD: each shared prime at its LOWER power. LCM: every prime at its HIGHER power.**" Show both on one table.
   - Also say the standard names ("greatest common divisor", "least common multiple"). The extras use them.
3. **No primality test is taught.** Slide 4 says "know primes up to 40", but the practice goes higher: 43 (Q11), 47/53/59 (q-407), 87 (q-403), 91 (extra-7).
   - Add: "To test n, try the primes up to √n."
   - Add a list of fake primes: 51 = 3·17, 57 = 3·19, 87 = 3·29, 91 = 7·13, 119 = 7·17. These are classic NITE traps.
   - extra-t14-4-5's solution uses the √n test, but the course never teaches it.

### 1. Coverage: missing or thin
- **Perfect squares and cubes by exponents:** "smallest k so that 18k is a perfect square/cube" (extra-6). This is a classic question. Teach it as "all exponents even (or multiples of 3)". It is not taught.
- **Odd number of divisors ↔ perfect square (any square, not only p²).** Slide 5 shows only prime squares. q-417 needs the general rule (36 has 9 divisors).
- **Equations solved by unique factorization:** "2^a·3^b = 72 → a = 3, b = 2", or "p, q primes, p²q = 50 → p = 5, q = 2". This is common on the exam and is missing.
- **GCD × LCM = a × b** (for two numbers). A quick shortcut and a checking tool. Missing.
- **Zeros at the end of a number** = number of pairs of 2 and 5 (e.g., 2⁵·5³·7 ends in 3 zeros). Uses exactly this topic's "ingredients" idea. Missing.
- **0, 1 and negative numbers are not prime.** Only 1 is mentioned.
- "If a prime divides a product, it divides one of the factors." Used in Q15 (1), and taught only inside that solution.

### 2. Teaching quality per level
- **Weak:**
  - Slide 2: "The primes are the small numbers you never meet as an answer inside the times table." This is not true (7 = 1·7, and 2, 3, 5, 7 are all answers in the table) and it confuses. Delete it.
  - Lost at Q4/Q5 (point 1).
  - Q14 with four letters as exponents is hard. Method 2 (plug in 2, 3, 5, 7) saves them, which is good.
  - The colon for division on the board (slide 5: "20 : 4 = 5") and in solutions (Q16 "280:35", q-417 "n:d") reads as a ratio in English. Use ÷.
- **Medium:**
  - The "break and build" idea (theory B slide 4) is the best part of the topic. Clear and useful.
  - Needs the GCD/LCM table from point 2 to be reliable.
  - Q15's answer is "never true", but the question asks "not necessarily true". Say once: "never true is also not necessarily true."
- **Strong:**
  - Would like the divisor-count formula (given, good), GCD×LCM, the zeros trick and the perfect-square exponent test.
  - Q13, Q15, q-408 and q-421 are good exam-hard items.

### 3. Correctness
- All keys are correct (17 guided, 20 practice, 7 extras). I solved Q1, Q13, Q16, q-407, q-408, q-414, q-419 and q-421 in full.
- **Slide 2 (theory A):** the "times table" sentence is false (see above).
- **Q4 video** uses "least common multiple" before it is taught (see point 1).
- **Recap slide 7:** the teacher underlines "counted once", but the board says "shared ones once". This is a small mismatch, and the rule is imprecise (point 2).
- **q-420 solution:** "and it is always integers" should be "and it is always an integer".
- **q-422 solution:** "24 is only the PRODUCT of 4 and 6 divided by nothing" is confusing. Better: "24 is just 4 × 6. The product is too big because 4 and 6 share a factor of 2."
- **extra-t14-4-2 solution** ("After removing the shared factor 6, the required factors two and three are coprime") is unclear. Better: "12 = 2²·3, 18 = 2·3². Take each prime at its higher power: 2²·3² = 36."
- **extra-t14-4-4** uses "a common divisor divides the difference". This is not taught. Keep it only as a strong-student item, with one line of explanation.
- **Q16 wording:** "The prime factors of a are 2 and 5 only" could be read as "2 only" (a = 16). The video says "from BOTH". Write "a has exactly two prime factors: 2 and 5."

### 4. Methods to add or teach differently
- **One GCD/LCM table** (theory B slide 3): the same two numbers, lower power vs higher power, side by side. Add a warning: "Multiplying the numbers is almost always wrong" (Q5 choice 96, q-422).
- **"Primes near the target" number line** (Q1, q-407, q-418): write the primes 2–60 once on a strip. It is the same drawing each time.
- **√n primality test + fake-primes list:** add to slide 4 and the memory card.
- **Parity of primes:** one board line on slide 3: "Sum or difference of two primes is odd → one of them is 2." It is used in Q11, q-412 and q-415.
- **Plug in the smallest primes** (2, 3, 5, 7) for letter questions like Q14. Make it a named method on theory B slide 4.

### 5. Practice
- Quantity is good: 17 guided, 20 practice, 7 extras. The spread is good: easy (q-404, q-406, extras) up to hard (q-408, q-421).
- Repetitive:
  - "y² is prime" appears twice (Q9, q-416).
  - "Exactly 3 divisors" appears three times (Q10, Q17, q-420).
  - GCD with letter primes appears twice (Q4, q-410).
  - Replace one of each with a perfect-square/cube question, a unique-factorization equation, or a zeros-at-the-end question.
- Order: again the extras (easy) come after the hard practice. Put them first.
- The practice uses the taught methods well, except the √n test and perfect squares (not taught).

### 6. Verdict
- **Weak:** Will handle the basic primes, factor trees and divisor checks. Will mix up GCD and LCM and fall for the fake primes (87, 91).
- **Medium:** Will solve most questions once GCD and LCM are clear. The "break and build" idea carries them.
- **Strong:** Ready for most exam items. Missing a few fast tools (perfect-square exponents, GCD×LCM, zeros).

**Top 3 changes:**
1. Move Q4–Q5 after theory B, and teach GCD/LCM as "lower power / higher power" in one table (replace "offset" and "shared ones once").
2. Add the √n primality test and a fake-primes list (51, 57, 87, 91, 119). Delete the "times table" sentence.
3. Add perfect squares/cubes by exponents and unique-factorization equations (1 slide, 2–3 questions). Replace the repeated "y² prime" and "3 divisors" items.
