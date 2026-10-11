# New exam methods — teacher guide (2026-10-06)

Read before recording. One section per method: what it is, why it works, the cue, a worked example, common mistakes, limits, and how many real exam questions it helps on. Not part of the course.

---

# Topic 1 — "Number" is not "integer" (card row only)

**What it is.** In NITE questions the word *number* (with no *integer* next to it) means any number, fractions and decimals included. Only *integer* means a whole number.

**Why it matters.** The trap answer counts only the whole numbers. If the question says "how many numbers x between A and B make 3x a whole number", the fractions count too.

**Cue.** "How many numbers…" / "numbers between…" where the word *integer* is missing.

**Worked example (on the card).** 4 < x < 6, and 3x is whole. Then 12 < 3x < 18, so 3x = 13, 14, 15, 16, 17 → five numbers: 4⅓, 4⅔, 5, 5⅓, 5⅔. The trap answer is 1 (only x = 5).

**Method.** Turn the condition into the thing that must be whole (here 3x), find its range, and count the whole values in that range.

**Common mistakes.** Counting only whole x; including the ends when the inequality is strict (3x = 12 and 18 are out).

**When it fails.** If the question does say "integer", count whole numbers only.

**Real exam questions it helps on:** 1.

Note: the card uses new numbers (4 and 6) instead of 10 and 12, to keep the course examples original.

---

# Topic 5 — Count the Powers (power count)

**What it is.** A five-second check for expression questions with letters in the answer choices. Count the "power" of the question and of each choice. The right answer has the question's power.

**How to count.**
- The power of a piece = how many letters are multiplied in it: x → 1, xy → 2, x²y → 3 (x·x·y).
- A number in front doesn't count: 5x² → 2. A number alone → 0.
- Multiplying adds powers (x·y → 2). Dividing subtracts: x²/y → 1, y/x → 0, 1/x → −1.
- Plus and minus: do NOT add. Check each piece. All pieces have the same power → a "clean" expression with that power. Different powers (x + 1: 1 and 0) → "mixed".
- A clean bracket acts like one piece: (x + y)² → 2, 1/(x + y) → −1.

**Why it works (simply).** Every legal step — opening brackets, factoring, cancelling — keeps the number of letters in every piece balanced. (In math words: the expression is *homogeneous* of a certain degree, and equal expressions have equal degrees.) So a choice with a different power, or a mixed choice, can never equal the question.

**Cue.** Letters in the question and letters in the choices ("= ?" expression questions); also after a plug-in tie.

**Worked examples (in the lesson).**
1. (x² − y²)/(x + y) + y; choices x², x + 1, x, 1/x. Top 2, bottom 1 → 2 − 1 = 1; + y → 1. Clean, power 1. Choices: 2, mixed, 1, −1 → answer x.
2. x(x + 2y) + y²; choices (x + y)², x + y, (x² + y²)/x, x + y². Pieces x², 2xy, y² → power 2. Choices: 2, 1, 1, mixed → answer (x + y)².

**Bonus: breaking ties.** Plugging in 1s often makes several choices equal (a², ab and b² are all 1). Before plugging in again, count the powers of the tied choices — usually only one has the question's power. (Guided Question 17 shows this.)

**Common mistakes.** Adding powers across a plus sign (x² + y² is power 2, not 4); counting the number in front (2a is power 1); forgetting that division subtracts (1/x is −1, not 1).

**When it does not help.** (1) All four choices have the question's power — then plug in. (2) The question itself is mixed (like x² + 3) — no single power, so plug in. When two choices survive, plug in once or compare one leading term.

**Real exam questions it helps on:** about 10 letter-choice questions; it decides 4 alone and breaks 4 of 5 plug-in ties seen.

**Course items.** Lesson `r26-t05-power-count` (5.4 min); guided q-r26-t05-17 (decides alone; answer x(x − y)) and q-r26-t05-18 (tie with ones; answer 2b); card rows + tip "Tie? Check the powers first."; one summary slide.

---

# Topics 10–11 — Given power → asked power

**What it is.** They give you one power (or root) of a letter and ask for a different power of the same letter. Don't find the letter. Jump straight from the given power to the asked one.

**Method.**
1. Write both as powers of the letter (roots become fractions: ∛b = b^(1/3), √(x³) = x^(3/2)).
2. r = asked exponent ÷ given exponent.
3. Raise both sides of the given to the power r.

**Why it works.** Raising both sides of an equation to the same power keeps them equal, and a power of a power multiplies the exponents: (b^g)^r = b^(g·r). We choose r so that g·r is the asked exponent. It is the same idea as "raise both sides to the reciprocal power" (Question 14), where the asked exponent is 1.

**Cue.** An exponent/root equation is given, and the question asks for b², b^(2/3), √(x³)… — not b itself.

**Worked example (card).** ∛b = 5. Asked b^(2/3). r = (2/3) ÷ (1/3) = 2. b^(2/3) = (b^(1/3))² = 5² = 25.
**Guided question (topic 11, Question 16).** ⁴√(x³) = 8, find √(x³): r = (3/2) ÷ (3/4) = 2 → 64. The trap 16 is x itself.

**Common mistakes.** Stopping at the letter (answering x instead of the asked expression); dividing the exponents the wrong way (given ÷ asked); raising only one side; forgetting a number in front (it must be raised too: (2b^…)⁴ gives 16 in front).

**When it fails.** When the unknown is IN the exponent and must be solved (like 3^(x+1) = 27) — use equal bases or try the choices.

**Real exam questions it helps on:** 6.

**Course items.** Topic 11 only: card row in "Advanced exponents and roots" after the reciprocal-power row, and guided q-r26-t11-13 with a solution video. Topic 10 is unchanged.

---

# Topic 12 — Ranges in two moves; the most precise range; range of a/b

## 1. Ranges in two moves
**What it is.** A way to solve any "for which values of x" inequality without ever flipping a sign.
1. **Endpoint:** pretend the inequality sign is "=", and solve. That number is the border of the answer.
2. **Direction:** test one easy legal number (usually 0). True → the answer is the side containing that number; false → the other side.

**Why it works.** Two continuous sides can change which one is bigger only at a point where they are equal. So the border is where they are equal, and one test number shows which side is right.

**Worked example (lesson slide).** 5 − 2x > x − 4. Endpoint: 5 − 2x = x − 4 → x = 3. x = 0: 5 > −4 true, and 0 is below 3 → x < 3.
**In a guided video.** Question 1 (3 + x < 15 + 3x): endpoint −6 already kills three choices; x = 0 gives the direction → −6 < x.

**Common mistakes.** Testing the endpoint itself (it gives "equal", not a direction); testing an illegal number.

**Limits.** If x is in a denominator, the value that makes it zero is a border too — test a number on each side. A "touching" endpoint (like x = 0 in x² > 0) does not switch the sides — when in doubt, test both sides. Quadratics have two endpoints: test the middle part.

## 2. The most precise range (choices are ranges)
**Rule.** Test a number that some choices contain and others don't.
- It works → it must be in the answer → every choice that leaves it out is wrong.
- It fails → it can't be in the answer → every choice that contains it is wrong.
**Guided question (Question 11).** x² + 3x < 10; choices x < 2 · −2 < x < 5 · −5 < x < 2 · x > −5. x = 3 fails → choices 2, 4 out. x = −6 fails → choice 1 out → −5 < x < 2. No solving needed.
**Tip.** Choose numbers where the choices disagree, and near their ends.

**Real exam questions it helps on (sections 1–2):** about 15.

## 3. Range of a/b (traps card)
**Rule (all positive).** Smallest a/b = smallest top ÷ largest bottom; largest a/b = largest top ÷ smallest bottom. Example 2 < a < 6, 1 < b < 3 → 2/3 < a/b < 6.
**Why.** A fraction grows when its top grows and when its bottom shrinks.
**Common mistake.** Dividing end by end (2/1 and 6/3 → "2 < a/b < 2" nonsense).
**Limit.** Only for positive ranges; with negatives, check the four corners; the bottom must not reach 0.
**Real exam questions:** 1–2.

---

# Teacher guide — new methods in topics 15, 17, 18 (read before recording)

(Topic 13 "The Mirror Test" was removed from the course on 2026-10-11, the teacher's decision.)

## Topic 15 — Tag it (guaranteed factors)

**What it is.** A sure method for "necessarily divisible by", "the largest number it must divide" and "necessarily an integer".

**The cue.** Conditions like "x is divisible by 6", "y is even", "a multiple of 9", and then "necessarily / certainly / greatest certain divisor".

**The move.** Write each condition as a tag: a multiple of 6 → 6k, even → 2m. Here k and m are unknown whole numbers. Then do the operation they ask for:
- **Multiply** → the tags multiply: 6k · 10m = 60km, so 60 is certain.
- **Add** → only the shared factor comes out: 6k + 10m = 2(3k + 5m), so only 2 is certain.
- **Divide** → every prime of the bottom must appear in the tags on top: ab/15 = 60km/15 = 4km ✓, but a/4 = 6k/4 = 3k/2 ✗.
- **"Divisible by a and by b"** → the tag is the LCM: by 4 and by 6 → 12k, not 24k.

**Why it works.** k and m can be any whole numbers, so they guarantee nothing (3k + 5m can be 8, 11, …). The only thing certain is the number outside the bracket. When you add, nothing can come out of the bracket except a factor both terms share.

**Worked example (guided question).** x is divisible by 6, y by 9. What is the largest number x + y is certainly divisible by? Choices 18 / 15 / 9 / 3. x + y = 6k + 9m = 3(2k + 3m), so the answer is 3. To confirm nothing bigger works: 6 + 9 = 15 (not divisible by 9 or 18) and 12 + 9 = 21 (not divisible by 15).

**Common mistakes.**
- Plugging in **equal values** for different letters. x = y = 18 gives 36, which looks divisible by 18. Different letters need different values.
- Taking the smallest case as the answer (6 + 9 = 15). The smallest case shows the biggest *possible* divisor, not the certain one.
- Multiplying the two divisors in "divisible by 4 and by 6" (24) instead of taking the LCM (12).
- Plugging in a value that gives 0.

**When it fails or isn't needed.** Remainder questions with small numbers (just plug in the smallest number). Products of consecutive numbers (you need "numbers in a row" on top of it). Digit puzzles.

**Evidence.** It helps on 15 real exam questions: 10 directly, and 5 more in the "prime bag" form of the same idea. The real sum questions offer the equal-values trap as a choice.

**In the course.** Slide 5 "Tag it" in "More Remainder Tools". Guided Question 11 (q-r26-t15-15). Row on the "More remainder tools" card. The teacher's suggested example (multiples of 3, choices 3/6/9/12) is a real 2025 exam question, so it was replaced with an original pair (6 and 9).

---

## Topic 17 — A letter against a multiple of itself fixes its sign (card only)

**The rule.** Compare a letter with a multiple of itself, and you learn its sign.
- x < 2x → subtract x: 0 < x. So x > 0 (doubling made it bigger).
- x/3 > x → a third of it is bigger, which happens only for a negative number (−6 → −2). So x < 0.
- a < b < 3a → a < 3a, so a > 0, and b > a, so b > 0 as well.
- (Next to the known one: x² < x → 0 < x < 1.)

**Why.** kx − x = (k − 1)x. With k > 1, "kx is bigger" means (k − 1)x > 0, so x > 0. With k < 1 it flips.

**Cue.** A chain of inequalities in which one letter is written as a multiple of another one (z = 2x and x < z), followed by "how many are surely positive".

**Mistake.** Assuming every letter is positive. Also: the rule says nothing about letters outside the chain.

**Evidence.** 1 real exam question (a summer exam). The course did not state this step before.

**In the course.** New table "Signs hidden in the given" on the card "The number line — ranges and arrows".

---

## Topic 18 — Digit word equations

**What it is.** A two-digit number described in words, with no columns. For example: "the number is 4 times the sum of its digits".

**The move.** Write the number as 10A + B, then collect the A's on one side and the B's on the other: 10A + B = 4(A + B) → 6A = 3B → B = 2A. The ratio gives every answer: 12, 24, 36, 48. (Check: 12 = 4 · 3.)

**Why.** "Ten A plus B" is what the digits mean. Collecting the terms leaves a simple relation between the two digits.

**Bonus fact.** A number minus its digit sum = 9 × its tens digit.

**Mistakes.** Writing AB as A·B. Forgetting that A ≠ 0. Stopping at one number when they ask "how many".

**Evidence.** It helps on 5 real exam questions (plus 1 related one).

**In the course.** One board line and spoken lines on lesson slide 2 ("The 4 steps"). The same line on the summary slide "The 4 steps". A row on the toolkit card. One line in Question 9 (q-520), which already uses 10T + U.

---

# Teacher guide: new methods in topics 23–25 (percentages, overlapping groups, averages)

Read this before you record. It is not part of the course. The counts of real exam questions come from the
solve notes (`real_exam/method_search/wp_deep_percent_averages.md`, `wp_deep_counting.md`, `wp_deep_english.md`,
`combinatorics_…_generality.md`). Every example below is new. None of them is a real exam question.

---

## Topic 23: percentages

### 1. The flip rule (same part → flip, same whole → keep)
**Where:** "Calculating Percentages", new slides "Same part: flip" and "Same whole: keep". Guided question 10 (library) and its video. A row on the card.

**What it is.** When one amount is a percent of two different things, for example "40% of A = 15% of B", the ratio of the
wholes is the two percents swapped: A : B = 15 : 40 = 3 : 8.

**Why it works.** Write it as an equation: 0.4A = 0.15B. Divide both sides by B and by 0.4: A/B = 0.15/0.4.
In words: to get the same amount, a big percent needs only a small whole. So the thing with the bigger percent is the smaller thing.
This is the same as the topic 22 rule "4 mugs cost the same as 3 plates → mug : plate = 3 : 4".

**The other case: same whole → keep the order.** a = 50% of b and c = 125% of b. Here both amounts are taken from the
same whole. So the bigger percent gives the bigger amount: c : a = 125 : 50 = 5 : 2. With b = 100 you get a = 50, c = 125.

**Cue.** "p% of A is equal to / the same as q% of B", or "a fraction of A equals a fraction of B". Then the question
asks for a ratio, a percent of one in terms of the other, or (with a total or a gap) the actual amounts.

**Worked example (the guided question).** 600 novels and textbooks. 45% of the novels = 30% of the textbooks.
N : T = 30 : 45 = 2 : 3 → 5 parts = 600 → 1 part = 120 → N = 240. Check: 45% of 240 = 108, and 30% of 360 = 108.

**It works with fractions too.** 2/3 of A = 4/5 of B → A : B = 4/5 : 2/3. Multiply both by 15: 12 : 10 = 6 : 5.

**Common mistakes.**
- Not flipping (A : B = 40 : 15). This gives the thing with the bigger percent the bigger size. In the guided question that is the 360 trap.
- Taking the percent of the total (30% of 600 = 180) instead of the percent of each pile.
- Flipping when the WHOLE is shared (a = 50% of b, c = 125% of b → c : a is NOT 50 : 125).

**When it fails.** The rule only works when the two amounts are equal. "40% of A is 6 more than 15% of B" → there is no flip. Write the equation, or test the choices.

**Real exams:** 6 questions (percents and fractions, often followed by a parts step, i.e. the gap or total = so many parts).

### 2. The arrow map
**Where:** "Percent of a Percent", new slides "The arrow map" and "Walk the path". A row on the card.

**What it is.** Each sentence like "x is p% more than y" or "P is p% of Q" becomes an arrow. It starts at the whole
(the word after "of" or "than") and points to the other one. The arrow carries its multiplier (×1.2, ×0.4, ×1.25…).
Going along an arrow, multiply. Going against it, divide. To compare two people, walk from one to the other and
multiply what you meet. The product is the answer.

**Why it works.** "x is 20% more than y" means x = 1.2y. That is one multiplication from y to x. Going back,
y = x ÷ 1.2. A chain of these is just a chain of multiplications and divisions.

**Cue.** Two or more comparison sentences ("of", "more than", "less than") about different people. Or the question
compares in the opposite direction from the sentence ("x is 20% more than y. What percent of x is y?").

**Worked examples.**
- x is 20% more than y → y = x ÷ 1.2 = x · 5/6 = 83⅓% of x. Not 80%.
- P = 40% of Q, R is 25% more than Q → from P to R: ÷0.4, then ×1.25 → 1.25 ÷ 0.4 = 3.125 → R = 312.5% of P.
  Check with Q = 100: P = 40, R = 125, 125/40 = 3.125.

**Common mistakes.**
- Reversing a percent by changing its sign ("20% more" one way = "20% less" the other way). Wrong: the whole changed.
- Pointing an arrow the wrong way. The arrow always starts at the word after "of" / "than".
- Forgetting the ×1 part: "25% more" is ×1.25, not ×0.25.

**When it fails / limits.** Every step must be a percent or a multiple. If a fixed amount is added ("then 15 credits more"),
it is not one multiplier. Use real numbers or a letter. Plug in 100 still works everywhere. The map is a second picture.
It is fastest when the chain is long or when the 100 would fall on the wrong person.

**Real exams:** about 13 questions (one-step chains, chains of 3–4 changes, going backwards, "x = 7b → 700%").

### 3. Two card lines: fee on top, and "rose by" vs "became"
**Fee or tax on top → divide, don't take 75%.** You paid 100, and that includes a 25% tax. The price before tax is
100 ÷ 1.25 = 80. Check: 80 · 1.25 = 100. The trap is 75 (100 · 0.75). Why: the 25% was added to the price before tax,
not taken from the 100. Real exams: 1 question (the trap answer was one of the choices).

**"Rose BY" or "became"?** Multipliers ×2, ×1.5, ×1.25 give ×3.75. The amount BECAME 375% of the start, and it ROSE BY 275%.
The same for doubling three times: ×8 → rose by 700%. Common mistake: answering the multiplier when the question
says "by how much did it rise". Real exams: 2 questions.

### 4. Plugging in numbers: when 0 is the best number
**Old card line:** "not 0, not 1". **New:** usually avoid 0 and 1, because they hide differences: 0 times anything is 0, and 1 squared is still 1.
BUT if 0, or "nothing changes", makes the answer obvious, use it. Example: k new students join a class. When k = 0 nothing changed,
so the right expression must give 0 (or "no change") at k = 0. Every choice that does not is out. If two choices survive,
plug in a second, ordinary number (k = 2) and test only those two.

**Why it works.** The correct formula must be true for every allowed value, including the "nothing happens" value.
A wrong formula usually breaks there.

**When it fails.** The value must be allowed by the question. If "k ≥ 1", "positive" or "different" is written, you cannot use 0.
Also, sometimes several choices survive (that is why we plug in a second number).

**Real exams:** in the counting set, 3 questions are solved by one such plug-in, and 3 more need a second plug-in after it.
The same line is now also said in Q15 (N students, g girls; it was Q14) and in the summary: "usually not zero or one".

---

## Topic 24: overlapping groups

### The hidden total
**Card line:** "No total given? Look for a natural one: 24 hours, 7 days, 100%."

**What it is.** The minimum-overlap rule (A + B − total) needs a total. Sometimes the question doesn't give one, because it is
obvious from the story: a day has 24 hours, a week 7 days, a whole is 100%.

**Worked example.** Awake 18 hours, at work 10 hours. At least 18 + 10 − 24 = 4 hours are both
awake and at work. Why: the 24 hours can't hold 28 hours of "awake" plus "at work" without at least 4 hours counted twice.

**Common mistake.** Answering 0 ("there may be no overlap") because no total is printed. Or adding 18 + 10 without a total.

**Limits.** Make sure the natural total is the real one. For example, "during the 8 working hours" means the total is 8, not 24.

**Real exams:** 1 question in the counting set.

---

## Topic 25: averages

### 1. Percent shares as weights
**Where:** Q13 (six numbers average 62, nine average 82), new slide 4 "Shares as weights". A row on the card.

**What it is.** If the group sizes are given as percents, the percents are the weights.
Average = cheap value + (share of the expensive ones) × (difference).
70% of the items cost 30, the rest cost 50 → 30 + 0.3 · 20 = 36.

**Why it works.** It is the see-saw. 30% of the weight sits at 50, so the average moves 30% of the way from 30 toward 50.
In formula form: 0.7 · 30 + 0.3 · 50 = 30 + 0.3 · (50 − 30). Balance check: 36 is 6 above 30 and 14 below 50, and 70 · 6 = 30 · 14 = 420.
And, as always, the heavy side (70%) gets the small part of the gap.

**Cue.** "x% of the … are …, the rest …", followed by "average", "average price", or "overall percent".
It also appears when money or counts are split in percents between two prices.

**Common mistakes.**
- Taking the plain middle (40). That is right only for a 50–50 split.
- Using the CHEAP share with the gap (30 + 0.7 · 20 = 44). Start from the cheap value and use the share of the EXPENSIVE ones,
  or start from the expensive value and subtract the cheap share × gap: 50 − 0.7 · 20 = 36.

**Limits.** The two values must be per item (a price per item, a score per student). If the percents are of money and not of items, check what is being averaged.

**Real exams:** 4 questions.

### 2. Groups of different sizes "in t years" (card row)
**What it is.** In t years every person is t years older. So each group's TOTAL age grows by t × the number of people in it.
5 boys and 3 girls, in 4 years: the boys' total grows by 20, the girls' by 12, so the gap between the totals grows by 8.
**Why it matters.** The card already says "every value +k → the average +k". That is true for averages. But when the question
compares TOTALS (sums) of groups of different sizes, the totals grow by different amounts.
**Common mistake.** Adding t (or 2t) to a sum. **Real exams:** 1 question.

### 3. Plug-in tip for "not necessarily equal to the average" (card tip)
The old tip: "plug in all values equal". This is good for letter answers. But when the question asks which expression is NOT
necessarily equal to the average, equal values make every choice equal the average, so nothing is ruled out.
Use uneven numbers such as 0, 0, 0, 4 (average 1): the wrong choice then gives a different number.
**Real exams:** 1 question, where the all-equal plug-in left all 4 choices.

---

# Teacher guide — new methods in topics 26–29 (read before recording)

Counts come from the fresh solve of the real exams (real_exam/method_search/wp_deep_work_motion.md, wp_deep_counting.md,
combinatorics_probability_….md). No exam text is quoted here; all examples are new.

---

## 1. Compare by factors — the V made general (Topic 26 lesson "Compare by Factors", Q16; Topic 27 slide + Q6)

**What it is.** When two or more things change at once and the question gives only relations ("3/4 as many hours",
"twice as fast", "20% more"), you don't need real numbers or equations:
new value = old value × every factor that changed. A factor that pushes the answer the same way goes in as it is;
one that pushes the opposite way is flipped. Anything that is the same in both situations cancels.

**Why it works.** The quantity is a product (or a quotient) of the things that change: work per day = hours a day ×
work per hour; notebooks = budget ÷ price; time = distance ÷ speed. Multiplying one factor by k multiplies the product
by k (if the factor is on top) or by 1/k (if it is on the bottom — that is the "flip"). Unknown shared values (the size
of the job, Ben's real rate) appear in both the old and new value and divide out.

**The cue.** Two changes + no real numbers, words like "times", "as many as", "a fraction of", "percent of".

**Worked example.** Lia works 3/4 as many hours a day as Ben; per hour she does 2/3 of what he does; Ben needs 8 days.
Per day she does 3/4 · 2/3 = 1/2 of Ben → same job takes 2 × 8 = 16 days. In one line: days = 8 × 4/3 × 3/2 = 16
(both factors push days the opposite way, so both flip).

**The V is a special case.** In a 3-column table whose middle is the product of the other two (Team · Work · Time,
Speed · Distance · Time), the V multiplies exactly the right factors and does the flipping for you. Topic 26 Question 6
Method 1 (4 × 72/30 × 5/8 = 6) is the factor rule; the V is the same thing as a picture.

**Motion version (Topic 27).** That is why the motion table is now Speed · Distance · Time — distance (the product) in the
middle. A 3× as fast as B, for half as long, covers 90 km: rows (3, 90, 1) and (1, ?, 2); blank in the middle →
upside-down V → 1·90·2 ÷ (3·1) = 60 km. Guided Q6: van 3× as far at 1.5× the speed, scooter 40 min →
1·3·40 ÷ (1·1.5) = 80 min.

**Common mistakes.** Adding the changes (+20% and −50% → −30%); not flipping a factor that pushes the other way
(gives an answer that fails the sense check: a higher price cannot buy MORE); forgetting one of the factors.
"x times slower / smaller" means ÷ x (3 times slower → speed ÷ 3), not "−3x".

**When it fails.** A fixed amount is added ("2 more boxes an hour", "+15 km/h"). That is not a factor — the percentage
depends on the unknown real value. Name the unknown with a letter and write an equation.

**Real exam questions it helps on.** 7 questions solved directly by "two changes multiply / the V" in the work and
motion sets (3 of them motion, where the old course had no V at all); the teacher's estimate including related
ratio/percent-of-rate questions in topics 26–27 is about 15.

---

## 2. Catching up = gap ÷ difference in rates (Topic 26, Q10 video slide "Same idea: catching up")

**What it is.** Something fell behind (or ahead) by a gap; now one rate is bigger than the other. Time to close the gap
= gap ÷ (difference of the rates).

**Why it works.** The normal rate keeps "using up" its share every day; only the extra part reduces the gap. It is the
chase rule from motion (gap ÷ difference in speeds) in work clothing.

**Cue.** "behind schedule", "catch up", "make up the lost time", a stop/break followed by a faster rate.

**Worked example.** Printer normally 6 h a day, down 5 days → 30 h behind. Now 16 h a day = 10 h extra a day →
30 ÷ 10 = 3 days.

**Common mistakes.** Dividing the gap by the new rate (30 ÷ 16); forgetting that the normal work continues; "without a
break" means 24 h a day.

**When it fails.** Rates that change over time, or a gap that is not a fixed amount — then go step by step / table.

**Real exam questions.** 2 work questions (not taught before), plus 1 circular-track lap question and the chase
questions already taught in topic 27.

---

## 3. "At most / at least / necessarily / impossible" in counting → Topic 21 (Topic 28 intro slide)

**What it is.** A routing rule: a "counting" question that asks for an extreme or for what must/can't happen is a
min/max question, solved with the Topic 21 routines (push the others to the extreme; worst luck + 1; remainder test for
"impossible"), not with counting formulas.

**Why it works.** These questions don't ask "how many arrangements" — they ask for a bound. A bound is found by making
everything else as small (or as big) as possible, then checking the case can really happen.

**Worked example.** 8 friends share 30 candies, each at least 2. Max for one friend: the other 7 get the least,
7 × 2 = 14 → 30 − 14 = 16. Check: 16 + 14 = 30.

**Common mistakes.** Looking for nCr/permutations; forgetting to check that the extreme case is allowed.

**Real exam questions.** 12 of the 24 real "counting" questions are this kind.

---

## 4. Groups with no names (Topic 28 card row + practice question)

**What it is.** When the groups are not labeled (pairs, two unnamed teams), count as if they had names, then divide by
(number of groups)!. For pairs: fix one person and choose her partner, then repeat.

**Why it works.** Every split into unnamed groups was counted once for every way of putting names on the groups —
that is (number of groups)! times.

**Worked example.** 4 girls into 2 pairs: with names C(4,2) = 6, ÷ 2! = 3 (fix Ana: her partner has 3 options).
6 players into 3 pairs: 5 · 3 · 1 = 15. Practice: 8 runners into 4 pairs = 7·5·3·1 = 105 (= 2,520 ÷ 4!).

**Common mistakes.** Answering C(4,2) = 6; dividing when the groups DO have names (teams Cedar and Maple, two
named teachers — then no division).

**When it fails.** Groups of different sizes are automatically distinguishable — no division.

**Real exam questions.** Not counted separately in the notes; added at the teacher's request (a classic trap).

---

## 5. Which door? COUNT / PATH / SYMMETRY (Topic 29 card + Summary slide)

**What it is.** Before calculating, decide which of three ways the question goes:
- **COUNT** — equally likely outcomes you can list (dice, one bag) → wanted ÷ all. Two dice, sum 7 → 6/36 = 1/6.
- **PATH** — the story happens in steps (draws one after another, rounds, a coin then a bag) → multiply the chances along
  the path, add the paths. 3 red 2 blue, two reds in a row → 3/5 · 2/4 = 3/10.
- **SYMMETRY** — nothing makes one person/place special → each has the same chance, 1/n (or k/n if k places are
  chosen). 5 people in a random line, Dana last → 1/5.

**Why it works.** COUNT is the definition of probability; PATH is "AND = multiply, separate cases = add" in order of
the story; SYMMETRY is COUNT where the count is obvious because all positions are interchangeable.

**Common mistakes.** Counting when the outcomes are not equally likely (sums of two dice are NOT equally likely — count
pairs); not updating the bag on a path; doing a long calculation where symmetry gives 1/n at once.

**When it fails.** "Sum of probabilities = 1" equations and a few counting-range questions don't fit a door.

**Real exam questions.** 17 of the 24 real probability questions (COUNT 6, PATH 8, SYMMETRY 3).

---

# Topic 51 — Picking values that fit (teacher guide, not part of the course)

## What it is
Plugging in numbers, Case 4. When an equation (or system) has MORE LETTERS THAN EQUATIONS and the question asks for ONE
value (a letter, or an expression like 6x + 9y), give one letter an easy value, solve the equation for the other letter(s),
and compute what they ask. Then check the answer choices.

## Why it works (simply)
One equation with two letters has infinitely many solutions. The question says the answer is ONE number, so that number must
be the same for every solution. So any legal solution will do — take the easiest one.
Example: 4x + 6y = 18, find 6x + 9y. Since 6x + 9y = 1.5·(4x + 6y), it equals 1.5·18 = 27 for every (x, y). Picking y = 0
(x = 4.5 → 6·4.5 = 27) finds this without having to spot the 1.5.

## The cue
- "Given: [one equation with x and y] ... x = ?" or "... 3x + 2y = ?"
- A condition like "y ≠ −2" or "b ≠ 3": usually a hint that the equation factors as (something)(y + 2) = 0, so the asked
  letter is forced — and that the answer does NOT depend on the other letter.
- Number choices (sometimes with "cannot be determined").

## How (the order)
1. Pick ONE letter (the one they don't ask about). Try 0 first — it kills whole terms. If 0 is not allowed or makes a mess, try 1 or 2.
2. SOLVE the equation for the other letter. (Don't pick both letters — the equation then probably won't hold.)
3. Compute what they ask; eliminate the choices that don't match.
4. Two choices left (often one is "cannot be determined")? Pick a second value and redo it. Same result → it doesn't depend on
   your choice. Different result → the answer is "cannot be determined".

## Worked example (the guided question in the course, pt-q24)
Given x ≠ −5 and xy + 5y = 2x + 10. y = ?
- x = 0 (allowed): 5y = 10 → y = 2. Choices −5 and −2 are out.
- x = 1: 6y = 12 → y = 2 again → "cannot be determined" is out. Answer: 2.
- Why: xy + 5y − 2x − 10 = (x + 5)(y − 2) = 0, and x + 5 ≠ 0, so y = 2. If x = −5 were allowed, the equation would be 0 = 0
  and y could be anything — that's exactly why the question forbids it.

(Note: the example "xy + 2x = 10 − 5y, y ≠ −2, find x" that was suggested is NOT a valid one-answer question:
it rearranges to (x + 5)(y + 2) = 20, so x changes with y (y = 0 → x = 5, y = 2 → x = 0). It was not used.)

## The "nothing-changes" value (related trick, also added)
In a story with letters, the best value is often the one where nothing happens:
- "n friends rent a boat for P shekels; k more join; how much less does each pay?" → k = 0 → nobody joins → 0 less → every
  choice that isn't 0 at k = 0 is out.
- Averages: a new value equal to the current average → the average doesn't change.
It often leaves two choices → then plug in an ordinary second number (k = 1, n = 2).
This replaces the old habit "avoid 0 and 1": 0 is fine when it kills terms or makes the answer obvious; 1 is the one that often
makes choices tie (powers, products, quotients), so be ready to plug a second set.

## Common mistakes
- Thinking "one equation, two unknowns — can't be solved" and marking "cannot be determined" (the trap distractor).
- Picking a value that breaks a condition (y ≠ −2, positive, integer) — or picking both letters so the equation fails.
- Stopping after one value when two choices still tie.
- Using it on an equation with ONE unknown (there x has one value — plug in the answer choices instead).

## When it fails
- The equation has no easy legal solution (e.g. a cubic): aim at the target expression with algebra instead.
- The system is fully determined (as many equations as letters): just solve/add the equations.
- The answer really depends on the choice → that IS the answer ("cannot be determined"), not a failure.

## How many real exam questions it helps on (from the method-search notes; counts only)
- Equations with more letters than equations, zero out / choose one letter: about 10 questions (2 fail).
- English summer 2024–26 forms, "fit-plug" (choose values that obey the given equation/condition): 9 questions, 3 of them
  clean single-plug wins where the old "equation → don't plug in" line contradicted the fastest route.
- Word problems with letters, "nothing-changes" value: 6 questions (3 clean single-plug wins, 3 need a second plug).
- In all: roughly 20–25 real questions (some overlap between the lists) — the most of any new method.
