# Student review — Topics 1 and 2

Note on keys: `correct:` is 0-based (0 = choice 1). I checked every question in both topics with this reading. **All answer keys are correct.** The problems are in the written solutions, in the order of teaching, and in practice that is too easy.

---

# Topic 1: Algebraic Fundamentals

## Most important points
1. **Fractions in the written solutions look like division.** The solution text writes fractions with a colon: q-040 "q = 1:5, and 5 · 1:5 = 1", q-018 "2:6 reduces to 1:3 … 33 1:3". In this course ":" means *divide*, so "5 · 1:5" reads as "5 · 1 ÷ 5". This is in the source (`content/full-course/topics/t1.json`), not only in the export. Change these to real fractions (LaTeX `\frac`). Topic 2 has the same problem, and there it is worse.
2. **Section 1 (number words) is the part the exam really tests, and it gets the least practice.** It has five recall questions (q-036 to q-040). Two of them (q-038, q-040) only ask for a definition. None of the 34 mixed or fast questions use a number word. The exam does not ask "93 − 46". It does ask "x is a negative integer and y is a positive number. Which must be true?"
3. **Some things are used before they are taught** (see Teaching quality below): q-018 needs fractions, q-014 needs ×11, extra-3 needs ×25, and fast calculation uses squares and percentages.

## 1. Coverage
- **Missing: "must be / could be / cannot be" questions about number words.** Add the plug-in method: test 0, 1, −1, ½, and a big number. Topic 20 (Algebraic Understanding) covers this later, but Topic 1 is where the words are taught. A first taste belongs here.
- **Missing: English maths words** that stems use all the time: *sum, difference, product, quotient, multiple, divisor/factor, divisible by, digit (vs number), distinct/different, consecutive even/odd, at least / at most*. q-036 already uses "product" and "distinct" (in the solution) without teaching them. Add one slide or one memory-card table.
- **Tell students that the exam page prints three of these facts:** "0 is neither positive nor negative", "0 is an even number", "1 is not a prime number" (these are in the General Comments of every quantitative section). This makes them easier to remember, and it shows that the exam tests them.
- **Order of operations: a minus before brackets.** 5 − (9 − 2) is solved (q-023), but the rule "a minus before brackets flips every sign inside" is never said. The expressions topics need it.
- **Fraction bar:** slide 5 of Order of Operations teaches it ("split a numerator, never a denominator"), but no question practises it. Add two questions.
- Even: "2k" (slide 9) never says that k is an integer. Letters have not been introduced yet.
- "Nonzero ≠ positive" is on the recap board (Intro slide 13), but "nonzero" was never taught.

## 2. Teaching quality per level
**Weak student**
- Add/Sub slides 3–4: "minus, minus → plus" (slide 3), then "two minus signs, answer negative" (slide 4). A weak student will mix these up. Say it clearly: the rule is only for two signs **touching**, as in −(−4). In −8 − 6 the signs do not touch.
- The colon ":" for division (Remainders slide, 10:3) is never explained. Say once: ": means ÷".
- q-018 (200 : 6 = 33⅓) needs a remainder written as a fraction, and reducing 2/6. Both are taught in Topic 2. Move it to Topic 2 or change the answer choices to "33 remainder 2".
- The fast-calculation slides use 50², 65², 40² (slides 10–11, fast-practice-4 and 7) and 24% (slide 12). Powers and percentages have not been taught. Add one line: "65² means 65 × 65". Or mark these slides as bonus.
- Mult/Div slide 5: "Remember when we called it 'times'?" refers to a lesson that does not exist.

**Medium student**
- The methods are clear and well sense-checked (estimate, add back to check). Good.
- The memory card "Fast-calculation toolkit" lists ×9 / ×11 (47 × 11 = 517), but no slide teaches it. q-014 (666 × 11) uses it in section 5, before the fast lesson. Add a 30-second slide.
- Extra-3 (25 × 28) and extra-4 (48 × 15) in section 5 need the ×25 and split tricks from section 6. Move them to section 7, or move the Fast Calculation lesson before the mixed practice.

**Strong student**
- About 20 minutes of column addition, borrowing and long multiplication, then 27 near-identical arithmetic questions. They will be bored and get little exam value.
- Offer a **skip test**: 8 questions at the start of each lesson. All correct → jump to the traps.
- They will like the Fast Calculation lesson. Put it earlier, or give them a direct link to it.

## 3. Correctness
- All keys are correct.
- **q-008 solution contradicts itself:** "every column writes 1 and carries 1", then "tens … write 2". Fix it: "Ones: 11, write 1 carry 1. Tens and hundreds: 12, write 2 carry 1."
- **Extra-2 (804 − 297) solution is unclear:** "add back the three minus the shared offset that was subtracted too much." Replace it with: "804 − 300 = 504. We took 3 too many, so add 3 back: 507."
- **Solutions for extra-1 to extra-7 and fast-practice-5 give no numbers,** only words ("Evaluate the bracket and the two products, then subtract"). A weak student cannot check a step. Write the numbers.
- q-040, q-018: the colon-fraction display (point 1 above).
- q-037 choice 1 renders "\text{odd}" in a different font from the other choices. This is cosmetic.

## 4. Methods and tricks to add
- **Plug-in numbers for number words** (Intro, after slide 13): "Must x·y be positive? Try x = −1, y = −1 … then x = −1, y = 2." Make it a habit: test 0, 1, −1, ½.
- **Unit-digit elimination** (Mult/Div recap): 9 × 13 must end in 7, so only 117 or 97 are possible, and 97 is too small. This is fast and it kills choices.
- **Estimate to eliminate** (already on slide 13 of Fast Calc). Tie it to the answer choices in the practice solutions ("choices 1 and 4 are too far from 3,700").
- **Consecutive numbers:** one line saying that consecutive even numbers differ by 2. This is used often in word problems.

## 5. Practice
- There are enough questions for arithmetic: 20 in the lessons, 27 mixed, 7 fast. The spread of difficulty is narrow: easy to medium, with no exam-level question.
- The mixed practice has no number-word questions and no fraction-bar questions. Add about 6: 3 must/could questions, 1 "sum of opposites / product of reciprocals" in a sentence, and 2 fraction-bar questions.
- Many are repeats (q-003, q-031, q-033 are all two-digit borrowing). Cut 3–4 of them.
- The fast-practice questions match the lesson well: each one uses one trick.

## 6. Verdict
- **Weak:** Yes for arithmetic and signs. They will stumble on q-018 and on the squares in Fast Calc, and they are under-trained on number words.
- **Medium:** Yes for arithmetic. Not yet reliable on "must be true" questions about number words.
- **Strong:** They learn nothing new until Fast Calc. They need a skip path and harder number-word traps.

**Top 3 changes**
1. Add 6–10 exam-style number-word questions (must/could be, plug-in 0, 1, −1, ½) to section 1 and to the mixed practice. Add a short vocabulary table (sum, product, quotient, multiple, divisor, digit, distinct).
2. Fix the order of teaching: q-018 → Topic 2; q-014, extra-3 and extra-4 → after Fast Calc; teach ×11 in a slide or drop it from the card; one line explaining squares; define "nonzero"; say "k is an integer".
3. Fix the solutions: colon-fractions → real fractions; q-008; extra-2; add numbers to all extra and fast solutions.

---

# Topic 2: Fractions — Fundamentals

## Most important points
1. **The written solutions are hard to read in a fraction topic.** Every solution writes fractions with a colon: q-075 "8 : 16:5 = 8 · 5:16 = 40:16 = 5:2 = 2 1:2", q-054 "2 17:36", q-048 "6:25 · 5:9 = 30:225". Here ":" means both *divide* and *fraction* in one line. This is the most urgent fix in both topics. Use `\frac` (the question stems already do).
2. **The practice ceiling is low.** There is one short word problem (extra-6), no "fraction of a quantity", no mixed-operation expressions, and no stacked fractions with a sum inside. The exam uses fractions inside word problems and expressions, not as bare drills.
3. **"LCM" is used in solutions (q-068, q-053, q-054, q-055) but the video never uses the word.** Either say "LCM = least common multiple = the smallest common denominator" in Add/Sub slide 5, or write "common denominator 15" in the solutions.

## 1. Coverage
Topic 3 covers comparing fractions well (benchmark ½, cross-multiply, plug in). So the gaps here are:
- **"Of" means times.** "⅔ of 36", "¾ of the remaining". This is the bridge to word problems and it is never taught. Add one slide in "Multiplying" and 3 questions.
- **Stacked fractions with sums**, e.g. (1 + ½) / (2 − ⅓). This is the exam form. Slides 6–7 only stack single fractions. Tie it to Topic 1: "the fraction bar is brackets; do top and bottom first".
- **Negative fractions:** −a/b = (−a)/b = a/(−b). This is not covered at all, and it is needed in Topic 4 onward.
- **Splitting a numerator:** (a + b)/c = a/c + b/c. Topic 1 said it, and it fits naturally next to "What cancelling means" (slide 10).
- **Fraction–decimal pairs to know by heart:** the card has ⅓. Add ⅔ = 0.666…, ⅙, ⅕ multiples, and 1/20 = 0.05, 1/25 = 0.04.
- **Dividing by 0.5 / 0.25 / 0.2 = multiplying by 2 / 4 / 5.** This is fast and common in motion and rate questions.

## 2. Teaching quality per level
**Weak student**
- The pizza, grid and bar visuals are very good. The cancelling slide ("does it multiply the ENTIRE top?") is excellent.
- Expanding slide 7: "Two quarters is a half — but two halves is a whole" is unclear. Say it directly: "Change only the bottom: 2/4 → 2/2. That is 1, not ½."
- q-065 uses (0.9)². Powers have not been taught. Write 0.9 · 0.9.
- No section before Add/Sub has a memory card. A weak student has nothing to review for lessons 1–2. The combined card after lesson 3 helps, but it comes late.
- Decimal slide 2 (place value) depends on a board that the notes do not show. Check that the place-value table is clearly drawn.

**Medium student**
- "Name the operation, then the rule" (Add/Sub recap) is the right habit. Add a practice block that mixes the four operations in one expression, e.g. (½ + ⅓) : ⅚, so they practise choosing the rule.
- The solutions of q-047 and q-048 do **not** cancel first (35/70, 30/225), but the video says "cancel FIRST". Rewrite them to show the cancel. 30/225 is exactly the "monster fraction" the video warned about.

**Strong student**
- Shortcuts to add: a/b + c/d = (ad + bc)/bd; 1/a − 1/b = (b − a)/ab; ÷0.25 = ×4; 0.125 = ⅛.
- **Elimination** is not shown at all. Example, q-054: 3¼ − 0.78 ≈ 2.47, so the answer is below 2½. That kills 2½ and 2 19/36. A denominator of 13 is impossible here, which kills 2 5/13. Show this once as "Method 2" in a solution.
- Several "decimal" questions are faster as fractions: 0.75 : 1.5 = ¾ : 3/2 (slide 9 mentions this; good). Make it a named habit.

## 3. Correctness
- All keys are correct. All video calculations check out (14/15 · 25/21 = 10/9; 3⅙ − 1¾ = 1 5/12; 4.8 : 0.06 = 80; 0.03 · 0.4 = 0.012, etc.).
- The colon-fraction display in all solutions (point 1 above).
- Extra-1 to extra-7 solutions give no numbers (e.g. extra-5: "divide numerator and denominator by 125" without the result 3/8). Add the numbers.
- **Answer-position pattern:** in the 7 extra questions, 5 have the correct answer in choice 1. Shuffle them.
- **Extra-2 (5/6 − 1/4) is exactly the example from Add/Sub slide 6.** Replace it with a new pair.

## 4. Methods and tricks to add
- **Estimate before you calculate** (Add/Sub recap): turn each fraction into a rough decimal and eliminate choices. See q-053: 0.28 + 0.58 ≈ 0.86, and 31/36 ≈ 0.86.
- **"Of" = × slide** (Multiplying, after slide 2), with ⅔ of 36 = 24 and "⅓ spent, then ¼ of the rest".
- **Plug-in check for rules:** when unsure whether a/b + c/d = (a + c)/(b + d), try ½ + ½. This teaches the plug-in habit that Topic 3 relies on.
- **Mixed numbers in addition:** for strong students, add the whole parts and the fraction parts separately when no borrowing is needed (4⅔ − 2¼ = 2 + 5/12). Keep "convert to improper" as the safe default.

## 5. Practice
- The count is fine: 20 in the lessons + 20 mixed + 7 extra. The spread is easy to medium, with nothing exam-hard.
- The practice matches the methods taught well: expand, reduce, flip, common denominator.
- It is repetitive: q-041, q-042, q-076 and q-078 are all "fill the missing term", and q-044, q-045, q-079 and q-080 are all mixed↔improper. Cut 3.
- Add about 8: 3 "fraction of a quantity" or word problems (like extra-6 but two-step), 2 mixed-operation expressions, 2 stacked fractions with sums inside, and 1 negative-fraction question.

## 6. Verdict
- **Weak:** Yes for single-operation drills. They will be confused by the colon solutions and have not met word-problem use.
- **Medium:** Yes for calculation. Not yet reliable on multi-step expressions and "fraction of the remainder" problems.
- **Strong:** Learns fast but meets no exam-level question. They need shortcuts, elimination and harder stacked fractions.

**Top 3 changes**
1. Replace every "a:b" fraction in the written solutions with a real fraction. Also make q-047 and q-048 cancel first, and add numbers to the extra solutions.
2. Add a "fraction of a quantity / of = ×" slide and about 8 harder questions: word problems, mixed operations, stacked fractions with sums, and negative fractions.
3. Teach the name "LCM / smallest common denominator" and add a strong-student layer: shortcuts (÷0.25 = ×4, ad + bc over bd) and one worked example of estimate-and-eliminate. Also fix q-065 (power before it is taught), extra-2 (duplicate) and the answer-position pattern.
