# External course review, group A (algebra, fractions, whole numbers, equations, calculations), 21 Oct 2026

Reviewer: Claude. Codex is doing the same review separately.
Sources: 26 transcripts from `scratchpad/ext/t/` (group-A.txt), read in full. I compared them with `course/tNN.txt` (slide text and question stems) and checked real-exam frequency in `real_exam/quant_real.md`.

**Overall.** Our course already covers almost everything in these videos, usually in more depth and with more traps. This is especially true of topics 2/3 (fractions), 4/5 (expressions), 13 (absolute value), 14–16 (primes, remainders, consecutive numbers) and 21 (cycles). The real gaps are small. Most of them are missing "named method" sentences, plus two lesson-sized holes: **fractions with letter denominators** and **power equations, even vs odd**.

7 of the 26 files have no speech, only "[Music]" (on-screen quizzes). I couldn't review them; they are listed at the end.

Totals: **19 videos reviewed with speech, 7 with no speech. 9 GAP (all PARTIAL), 2 BETTER, 2 CHECK.**

---

## Equations

### Can you solve these 7 questions – Psychometric Equations [zCl9rWztp1g]
Teaches: seven mixed equation questions: an exponential equation with the same base, two equations with three unknowns (add or subtract, looking ahead at the choices), cancelling before cross-multiplying, a² = b², a product equal to zero (counting solutions; x² = −9 gives none), |A| = |B|, and a common factor that is itself a bracket.

- **GAP (PARTIAL): simplify each fraction before you cross-multiply.** Their example has a fraction with (x+4) on top (after factoring x² − 16) and (x+4) below, times 5/10. Cancel first and you are left with x − 4 = ½. Cross-multiplying straight away makes a mess.
  - What we have: the t06 "Cross-multiply" slide only gives the condition (one fraction on each side). Nothing says "first cancel what you can inside each fraction, and note the restriction".
  - Exam: **2026_spring_q2_08** is exactly this: (3x+4)(3x−4)/(3x+4)² = 2. You cancel one (3x+4) and keep 3x+4 ≠ 0.
  - Where: t06 linear-equations, after "Cross-multiply", plus one new solve-q in t06 or t07 (same idea, new numbers). Per R37 a one-off trick gets about 2 minutes in that question.
  - Recommendation: **ADD** (one sentence in the slide and one question).
- Everything else here is covered: same base (t10 solve-q-250), add or subtract and look at what they ask (t06 "Ask what they want", t07 q-195 and q-188), a² = b² (t07 r26-t07-05), product equals zero and counting solutions (t07 q-192, t11 q-299, t07 summary), |A| = |B| (t13), a bracket as the common factor (t04 "Bracket as a factor").
- **CHECK:** As transcribed, question 1 ends with "√x = 3 + 2/3 … x = 1". That is inconsistent: √x = 11/3 would give x = 121/9. It is probably a transcription error, but don't reuse their numbers without solving it again. (ASR also garbled x² − 16 into "x − 4x + 4".)

### Equations with Higher Powers [tjloMVQ736I]
Teaches: solving xⁿ = k by taking the n-th root. With an even power: ± when k > 0, and no solution when k < 0. With an odd power: exactly one solution, and k may be negative. The same works when the base is a bracket, e.g. (x−2)² = 49 → x−2 = ±7, and (2x−4)³ = −27 → 2x−4 = −3. Nested case: (x²+1)² = 81 → x²+1 = 9 or −9, and the second is impossible.

- **GAP (PARTIAL): no single "power equation" rule.**
  - What we have, in pieces: ± for squares (t07 q-193, t07 summary), "odd roots accept negatives, even roots don't" (t09 "Odd & even roots"), "an odd power keeps the sign" (t08 r26-t08-05, t16).
  - What's missing is the rule as an equation-solving tool:
    - even power = positive → two solutions
    - even power = negative → none
    - odd power → exactly one solution
    - equal odd powers → equal numbers; equal even powers → equal or opposite
  - Also missing: the nested case where one branch is impossible.
  - Exam: **2020_spring_q2_08**: x ≠ y integers, which equation is impossible? Answer: x³ = y³, while x² = y² and |x| = |y| are possible. Also **2021_autumn_q1_13** (how many values of x).
  - Where: t07, a short lesson slide "Power equations: even or odd" with 3 examples: x⁴ = 16 / x⁴ = −16 / x³ = −8, then a bracket base, then the nested case. Add a link back from t09 "Odd & even roots".
  - Recommendation: **ADD**.

---

## Fractions

### שברים לפסיכומטרי 1 (Fractions 1) [FxvotZTqxs8]
Teaches: what a fraction is, its parts, proper/improper/mixed fractions and converting between them, expanding and reducing. It also uses expanding to solve 5/7 = 10/x.

- **GAP (PARTIAL): solve a proportion by spotting the factor.**
  - Their examples: in 5/7 = 10/x the top went ×2, so x = 7·2 = 14. In 2/9 = x/27 the bottom went ×3, so x = 6. In 3/x = 12/16 the top went ÷4, so x = 4. No cross-multiplying.
  - What we have: t06 teaches only cross-multiplying. t22's ratio tables scale ratios, but that isn't linked to fraction equations.
  - Where: t06 "Cross-multiply" slide: "When one top or bottom is an easy multiple of the other, just scale."
  - Recommendation: **ADD AS ONE-LINE TIP** with one numeric example. It is common inside ratio, similarity and percentage questions.
- Everything else is covered (t02 fraction-basics).

### Fractions for the Psychometric Test 2 [AO6P4Htdf5c]
Teaches: adding and subtracting fractions with the same or different denominators, the steps of the common denominator, mixed numbers (add the whole parts first when adding, convert when subtracting), and the cross ("butterfly") formula (ad + bc)/bd.

- Nothing new. We cover it in t02 fraction-add ("Same denominator", "Expand just one/both", "Common denominator", "Whole & mixed numbers") and t02 shortcuts ("Cross shortcut", "Mixed numbers fast"). Our rule for mixed numbers is more precise than theirs: "use the safe way when the second fraction part is bigger" beats their blanket "always convert when subtracting".

### שברים לפסיכומטרי 3 (Fractions 3) [fvboLyVsKgI]
Teaches: multiplying fractions, cancelling any top with any bottom, a whole number written over 1, dividing (multiply by the reciprocal, and the "ears" method), the main fraction bar, and "a fraction of a number = multiply".

- Nothing new. Covered in t02 fraction-multiply ("Cancel first", "Whole numbers", "Use the reciprocal", "Stacked fractions", "Whole over a fraction", "Of means times").
- They recommend the "ears" method. We show it and deliberately advise skipping it, because students swap top and bottom. I'd keep ours.

### שברים לפסיכומטרי 4 (Fractions 4) [3vnlCeXqLnU]
Teaches: decimals: benchmarks worth memorizing (0.1, 0.2, 0.25, 0.5, 0.75, 0.125; 0.3 is not ⅓), converting decimals to fractions and back, padding with zeros, ×/÷ by 10, 100, 1000.

- Nothing new. Covered in t02 decimals, which goes further (multiplying, dividing, ÷0.25, comparing).
- **CHECK:** "4 ÷ 1000 = 0.4" as transcribed. It should be 0.004. Probably a transcription error, but don't copy it.

### Fractions for the Psychometric Test 5 [IhBSV__ucSU]
Teaches:
- comparing fractions: same denominator; same numerator (smaller bottom wins); expanding to match; cross-multiplying; the ½ benchmark; negatives reverse the order
- tricks:
  - 1 ÷ (a/b) = b/a
  - n ÷ (1/k) = nk
  - (a/b) ÷ c = a/(bc)
  - when dividing fractions, cancel top with top and bottom with bottom before using the ears method
  - where the minus sign may go

- Nothing new. Covered in t03 compare-fractions ("Benchmark ½", "Same top or bottom", "Make them match", "Cross-multiply", "Negatives"), t02 ("Use the reciprocal", "Whole over a fraction", "÷0.5, ÷0.25, ÷0.2", "Negative fractions") and t01 Reciprocals.
- Their top-with-top cancelling gives the same result as our "flip, then cancel diagonally". There is no reason to add a second rule.

### Fractions for Psychometrics 6 [i0_QJF5QeEQ]
Teaches: fractions with letters:
- common denominator xy
- choosing the **smallest** common denominator (5/2x + 1/4x → 4x, not 8x²)
- (a−b)(a+b) = a² − b² as the common denominator
- a complex fraction where top and bottom both sit over (x−3), so the inner denominators cancel
- "cancel only a factor that multiplies everything"

- **GAP (PARTIAL): adding and subtracting fractions whose denominators are letters or brackets.**
  - What we have: t05 "No cancelling!" adds two letter fractions with common denominator xy. The t03 summary has one line, "Letters in fractions". The practice stems have 1/a + 1/b (t02) and 1/(1 + 1/x) (t05).
  - No lesson shows how to pick the common denominator when the denominators share a letter (2x and 4x), are opposite brackets (a−b and a+b), or need factoring first (ab − b² = b(a−b)). None shows clearing a complex fraction by multiplying top and bottom by the inner denominator.
  - Exam (frequent):
    - **2025_winter_q1_08**: a/(a−b) − b/(a+b)
    - **2020_autumn_q2_16**: (a² + b²)/(ab − b²) − 2a/(a−b)
    - **2021_autumn_q1_15**: forms of 1/x + 1/y + 1/z
    - **2020_winter_q2_13**: (x+y)/(1/x + 1/y)
    - **2019_spring_q1_10**: (x/y)/(z/w)
  - Where: a short slide-set in t05 expression-strategy, "Fractions with letters: the common denominator". Three examples, easy to hard: 2x and 4x, a−b and a+b, factor ab − b² first. Then one solve-q with new numbers, using plug-in as Method 2.
  - Recommendation: **ADD**. This is the most valuable gap in group A.

---

## Algebra basics

### מבוא לאלגברה לפסיכומטרי 1 (Intro to Algebra 1) [8xZbORXH248]
Teaches: order of operations (brackets, powers/roots, ×÷ left to right, +−; a fraction bar or a root acts as brackets) and the tip (a−b)/(b−a) = −1.

- Nothing new (t01 order-of-operations including "The fraction bar"; t05 "Opposite brackets", solve-q-130 and solve-q-136).

### Introduction to Psychometric Algebra 2 [sGx8SELVLdo]
Teaches:
- mental ×: split 12 into 10 + 2
- ÷ by splitting the dividend: 200/6 = 180/6 + 18/6 + 2/6
- the last digit of a product, used to eliminate choices
- checking a division choice with the last digit
- numbers ending in 0, 1, 5, 6 keep that last digit in any power (56⁵ − 35⁴ ends in 1)

- Covered: t01 "Splitting a factor", "Smart division", "Last digit".
- **GAP (PARTIAL): checking a division choice by its last digit.** Is 132 ÷ 6 equal to 18? 18 × 6 ends in 8, not 2, so no. 22 × 6 ends in 2, so keep it. Our "Last digit" slide does products only.
  - Recommendation: **ADD AS ONE-LINE TIP** in t01 "Last digit": "for a division, multiply the choice by the divisor and compare last digits". Exam value is low but it costs nothing.
- **GAP (PARTIAL): powers of numbers ending in 0, 1, 5 or 6.** Their example: 56⁵ − 35⁴ → 6 − 5 → ends in 1. They say it was on a real exam.
  - What we have: t21 teaches last-digit cycles for 3 and 2, and t18 says 0/1/5/6 keep their last digit when squared. We never say "cycle of length 1, so any power".
  - Recommendation: **ADD AS ONE-LINE TIP** in t21's cycles part. No such item in our English exam set, so keep it to a line.

### Introduction to Algebra for Psychometrics 3 [X2kCJDyJ-co]
Teaches: expression vs equation, like terms, opening brackets, bracket × bracket, common factor (numbers and letters), and the cancelling rule: the factor must multiply everything in its numerator and everything in its denominator.

- Nothing new (t04 expression-basics; t02 "What cancelling means" uses the same test: "does it multiply the ENTIRE top and the ENTIRE bottom?").

### מבוא לאלגברה לפסיכומטרי 4 (Intro to Algebra 4) [7Daf5MKVoiM]
Teaches: the three contracted formulas, read in both directions, 23² − 22² = 45, (5b + 4a)², the trap "(5+b)² ≠ 25 + b²", and −(a+b)² inside a fraction.

- Covered (t04 r26-t04-formulas: "(a + b)²", "Power first", "Number shortcuts", "Formulas backward"; solve-q-r26-t04-02 51² − 49²).
- **BETTER (small): put squaring a product and squaring a sum side by side.**
  - Theirs: (5b)² — multiplication inside, square each part: 25b². (5+b)² — plus inside, this is not allowed, use the formula.
  - Ours: the "(a + b)²" slide shows only the sum trap. The product rule sits far away in t08 "Same exponent".
  - Why theirs helps: weak students mix the two both ways. They write 25 + b², and after learning the formula they sometimes "open" (5b)² with a middle term.
  - Change: one sentence in t04 "(a + b)²": "With times inside the bracket you may square each part, so (3x)² is 9x². With plus inside you may not, so use the formula."

### Introduction to Algebra for the Psychometric Entrance Test 5 [BgiIZ4BW9oo]
Teaches: absolute value as distance, its place in the order of operations, nested absolute values, |a/b| and |ab| split, |a| ≠ a when a < 0, |a−b| = |b−a|, |a+b| ≤ |a| + |b| (equal when same sign), |a−b| ≥ |a| − |b|.

- Nothing new (t13 Parts 1–3 and tools, including "same signs, equal; different signs, smaller"). Their statements are correct.

### Introduction to Psychometric Algebra 7 [_DsoqzfzURw]
Teaches: eight sample questions:
- |a+b|/|a−b| = 1 → a = 0 or b = 0
- 8!·7!/(8! + 7!): take out 7!
- (7x+14)/(x² − 4)
- an order-of-operations drill
- |x|/|x+1| > 1, solved by testing the choices
- (a² − 9)/(3 − a)
- x³ + 4x² + 4x over x² + 2x
- |x²|·(−x), solved by plug-in with a second value

- Covered: t28 factorial sums ("take out the smaller factorial"), t04/t05 difference of squares and opposite brackets, t05 and t51 plug-in.
- **GAP (one-line tip): with absolute values (or even powers), plug in a positive AND a negative number.** They say it explicitly and their last question needs it (x = 1 leaves two choices, x = −1 settles it).
  - What we have: t05 "Choosing numbers" says avoid 0 and 1 and use different values, but not "include a negative when there are bars or even powers". t13's summary says only "plug in a number that fits".
  - Exam: inequalities_absolute has 35 items. Many "which is equal to" items with |x| fall to a positive-only test.
  - Recommendation: **ADD AS ONE-LINE TIP** in t05 "Choosing numbers" and the t13 summary.

---

## Whole numbers

### Whole numbers for psychometrics 1 [Gq-PxHdOdew]
Teaches: what "divides by" means, even and odd (0 is even), ± and × rules ("one even makes the product even"), odd ÷ even is never an integer, and simplifying a choice before checking it (b/2a type).

- Covered (t16 parity, solve-q-461 "simplify first", t01 Even & odd).
- **BETTER (small): don't memorize the table, test it.** Their framing: "you don't need to memorize the even/odd table; if you forget, run a quick example with 1 and 2 in your head".
  - Ours: t16 lists all the rules with examples, but never tells the student how to rebuild one they've forgotten. (t02 "Test a rule" has this idea, but only for fractions.)
  - Why theirs helps: a weak student who forgets a rule mid-exam has a 3-second fallback.
  - Change: one sentence at the end of the t16 parity rules: "Not sure? Take one for odd and two for even, and just calculate."

### Whole numbers for psychometrics 3 [lm0VmWeIt2w]
Teaches:
- divides / divisor, divisors come in pairs, perfect squares have an odd number of divisors (x with exactly 3 divisors → √x is an integer)
- common divisor and GCD, primes (2 is the only even prime; 1 is not prime)
- a product divides by each factor and each sub-product; counting the divisors of 2ab and 2c²
- notation: 2n, 3n, 6m with different letters

- Nothing new (t14 divisor pairs and solve-q-402, divisor-counting rule, t15 "we use separate letters", t01 Primes). Our q-402 is more precise than theirs: √x is a **prime**.

### Whole numbers for psychometrics 4 [c-KJ50aQnc8]
Teaches:
- computing a remainder via mixed numbers, by "filling up", or as change in a shop
- small ÷ big → the remainder is the small number; the biggest remainder is the divisor − 1
- the number to plug in = the remainder itself, then jumps of the divisor (2, 5, 8, 11…)
- 3n + 2 notation
- one plug-in can't confirm a number when "cannot be determined" is a choice

- Mostly covered (t15 divisibility-3 and 4: the same shop picture, 5 ÷ 8 leaves 5, biggest remainder, 4k + 3, "k can be zero").
- **GAP (PARTIAL): no explicit plug-in method for remainder questions.** "Which number do I plug in?" is never stated. Our solutions do it (x = 4 in the ÷8 question, 9 and 5 in the ÷7 question), but the lesson never says: "the smallest such number is the remainder itself; for a second value add the divisor; and before choosing a number over 'cannot be determined', try a second value".
  - Exam: divisibility_remainders has 36 items, one of the bigger groups.
  - Where: t15 divisibility-4, right after the "four k plus three" paragraph (per R37 it's a core method used in several questions).
  - Recommendation: **ADD** (2–3 sentences and one example).

### מספרים שלמים לפסיכומטרי 5 (Whole numbers 5) [ns9Dfz1Ezv8]
Teaches:
- consecutive, even-consecutive and odd-consecutive notation
- sum 1..n = n(n+1)/2; average of consecutive numbers = (first + last)/2 = the middle number; count = big − small + 1
- product of n consecutive numbers divides by n!; n(n² − 1) divides by 6
- 2 consecutive evens divide by 8, 3 consecutive evens by 48, k even numbers by 2ᵏ
- the sum of 2 consecutive numbers is odd and their product is even

- Covered: t16 consecutive-integers, consecutive-products (2 → 2, 3 → 6, 4 → 24, 2 evens → 4, consecutive evens → 8, x³ − x, x² − 1), r26-t16-consecutive-sums (count +1, middle), t21 (sum 1..k), t20 counting.
- **GAP (PARTIAL): the general pattern "k numbers in a row → divisible by k!".** We stop at four → 24. Five in a row → 120 is used in their Whole numbers 7 question, a(a² − 1)(a² − 4)/10. Three consecutive evens → 48 and k evens → 2ᵏ are missing too.
  - Exam: no English real-exam item uses these. Recommendation: **ADD AS ONE-LINE TIP** in t16 consecutive-products: "the pattern goes on: five in a row divide by 120". **SKIP** 48 and 2ᵏ.

### מספרים שלמים לפסיכומטרי 7 (Whole numbers 7) [9eitxdgGyoU]
Teaches: sample questions:
- prime + parity → a = 2
- five consecutive numbers in a(a² − 1)(a² − 4)
- the divisors of 2c²
- the parity of a + 3bc
- the remainder of x + y (two plug-ins)
- 2⁵·3⁵·5⁵ does not divide by 64
- boys = 7 × girls, so the total is a multiple of 8
- candies: divisible by 6, and divisible by 5 after removing 4

- Nothing new beyond the k! tip above. Covered in t14, t15 (ratio-to-multiple, remainder plug-ins) and t16.

---

## Transcripts with no speech (music only, not reviewable)
- האם אתה שולט באלגברה לפסיכומטרי [3bQgomrp4Yc]
- האם אתה שולט במספרים שלמים לפסיכומטרי [NrruR_dbbyA]
- האם אתה שפיץ באלגברה לפסיכומטרי [6XOzToiZrO0]
- חלוקה בשורש [mSm1fzlgxBw]
- תרגול חישובים לפסיכומטרי 1 [kORwVkJcxFg]
- תרגול חישובים לפסיכומטרי 2 [W5wVWVnEv6w]
- תרגול חישובים לפסיכומטרי 3 [-G0alqxNgIQ]

These are probably on-screen quiz videos. If they matter, someone would have to watch them; the transcripts have nothing to compare.

---

## Top recommendations (most valuable first)

1. **t05: add "Fractions with letters: the common denominator".** Pick the smallest common denominator (2x and 4x → 4x), use a² − b² for a−b and a+b, factor first (ab − b² = b(a−b)), and clear a complex fraction by multiplying by the inner denominator. Add one solve-q with new numbers. Why: at least 5 real-exam items (2025_winter_q1_08, 2020_autumn_q2_16, 2021_autumn_q1_15, 2020_winter_q2_13, 2019_spring_q1_10), and no lesson teaches it today.
2. **t07: add "Power equations: even or odd".** Even power = positive → ±; even = negative → none; odd → exactly one; equal odd powers → equal numbers. Include a bracket base and the nested case. Why: 2020_spring_q2_08 and 2021_autumn_q1_13; today the pieces are spread over t07, t08 and t09.
3. **t15 divisibility-4: state the plug-in method for remainders.** Use the remainder itself, then add the divisor. Try a second value before rejecting "cannot be determined". Why: 36 real-exam remainder items; our solutions already rely on it.
4. **t06: "simplify each fraction before cross-multiplying"**, with its restriction, plus one question modelled on 2026_spring_q2_08, (3x+4)(3x−4)/(3x+4)² = 2.
5. **t05 "Choosing numbers" and the t13 summary: with |x| or even powers, test a positive and a negative number.** Why: 35 inequalities_absolute items; a positive-only test often leaves two choices.
6. **t06 "Cross-multiply": a one-line tip to spot the expansion factor** (5/7 = 10/x → ×2 → 14) instead of cross-multiplying.
7. **t04 "(a + b)²": one contrast sentence**: (3x)² = 9x² (product, square each part) vs (3 + x)² (sum, use the formula).
8. **t16 parity: one sentence**: "forgot a rule? test 1 (odd) and 2 (even)".
9. **t01 "Last digit": one-line tip** for checking a division choice (choice × divisor, compare last digits).
10. **t16 consecutive-products: "the pattern continues: five in a row → 120".** **t21 cycles: "0, 1, 5, 6 keep their last digit in any power".** Both one line each, low exam weight.

Not recommended: their "ears" method (we deliberately advise against it), and cancelling top-with-top when dividing (same result as our flip-then-cancel, so it only adds a rule).
