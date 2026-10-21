# External course review, group D2 (tricks, plugging in, methods, 700+, tips: second half), 21 Oct 2026

22 videos reviewed. I read every transcript in full. Our course was checked with grep on `scratchpad/ext/course/tNN.txt`, trying several phrasings for each idea. Exam frequency comes from `studio-build/real_exam/quant_real.md` (19 English sections, 2019 to 2026).

**Overall:** this half is mostly "real exam walk-throughs" (Winter/Spring/Summer/Fall 23 to 25) and a three-part plugging-in series. Our course already covers nearly every "trick" here. Examples:
- cube and box diagonals (t35)
- 30-60-90, 45-45-90 and the bronze triangle (t31)
- hexagon diagonals 2a and a√3, and the hexagon around a circle (t34)
- a triangle in a parallelogram is half of it (t32)
- cross-multiplying to compare fractions (t03)
- swapping x% of y (t01, t23)
- the two-change percent formula (t23)
- choosing who stays out (t28)
- the median halves the area (t31)
- multiplying equations (t06)
- conjugates (t11)
- x² ranges (t12)
- the line through the origin (t37)
- circles on a diameter (t36)
- odd ÷ even is never an integer (t16)
- overlap min/max (t24)
- odd number of divisors, and testing divisors only up to the root (t14)
- radii to points of tangency (t33)
- cycles with remainders (t21)
- flexible drawings (t38)
- the weighted-average seesaw (t25)
- "first pick doesn't matter" (t29)

The real findings are few. The main ones:
1. What to do with a "None of the above is necessarily true" or "cannot be determined" choice when plugging in.
2. A shorter way to handle "a value joins, find the new average".
3. A few one-line geometry facts that real exam questions test directly.

Tags: GAP = we don't teach it. PARTIAL = we teach part of it. BETTER = their explanation is clearer. CHECK = their video is wrong or misleading.
Recommendations: ADD / ADD AS ONE-LINE TIP / SKIP.

---

## 1. Psychometric trick in a minute - 12 [4Fu8HHKHoug]
**What it teaches:** the cube's space diagonal is a√3, and the box's diagonal is √(a²+b²+c²).
- **Nothing new.** We cover both in t35: "the face diagonal is a root two, and the body diagonal is a root three", and "In a box: the root of a squared plus b squared plus c squared".

## 2. Psychometric trick in a minute - 4 [BKl-NDQ4-QU]
**What it teaches:** for an equilateral triangle in a circle of radius R, the side is R√3. The circle inside that triangle has half the radius.
- **PARTIAL.** In t33 (nested shapes: "triangle, circle, triangle") we teach "outer side is twice the inner side, area four times". We never say it in radius terms: the circle around an equilateral triangle has twice the radius of the circle inside it, and the side is R√3.
  - Exam: **2019_winter_q2_08** asks for exactly this. The inner radius is 1, so the outer radius is 2 and the ring is 4π − π = 3π.
  - **ADD AS ONE-LINE TIP** at the end of the t33 nested-shapes lesson: "Same picture in radii: the circle around an equilateral triangle has twice the radius of the circle inside it." Also add a guided question in that spirit, with a ring and new numbers.

## 3. Quantitative Tricks - Psychometrics Winter 25 [GJbn--rXb7c]
**What it teaches:** real-exam Winter 25 walk-through:
- simplify the givens first
- |expr| = k gives two cases
- x^(3n) = 1, decided by whether n is odd or even
- handshakes
- B+B always ends in an even digit
- divisible by 10 and 15, so divisible by 6 (plug 30)
- (m−1)(m−2) divisible by 3, so m is not
- a cone in a cylinder is ⅓, and halving the radius divides the volume by 4
- the side of a hexagon around a circle is 2R/√3
- turning words into equations
- plugging in answers, starting from a round one, for a commission question

Findings:
- **PARTIAL: among any three consecutive integers, *exactly* one divides by 3.** In t15 we have "Every third integer divides by three, so one of these three numbers must divide by three". That is only "at least one".
  - Exam: **2025_winter_q1_14**, "(M−1)(M−2) divisible by 3, which of M, M+1, M+2 is certainly not". It uses the "exactly one" part: the multiple of 3 is already among M−1 and M−2, so M can't be one.
  - Group D1 found the same point. **ADD AS ONE-LINE TIP** in t15 (one tip covers both): "Exactly one: once you know which one it is, the next two are not."
- **Nothing new on the rest.** We cover:
  - |x| = k gives two cases (t13)
  - the handshake / "action between two at the same time" (t28)
  - AB+BA decomposition (t18)
  - "why not just multiply ten by twenty-five", the coprime rule (t14)
  - a cone is ⅓ of its cylinder (t35)
  - "Halve the radius, a quarter" (t36)
  - the hexagon around a circle (t34, "seven over root three")
  - plugging in answers from the round one (t51)

## 4. Quantitative Tricks - Summer Psychometrics 25 [UKtnKBiqqD8]
**What it teaches:**
- a rule-of-three ink question
- **new average = old average + (newcomer − old average) ÷ new count**
- the units digit of 8⁶
- in an expression subtraction, look at one term only
- 30-60-90 in a rectangle
- the range of a/b: max is largest a ÷ smallest b
- factorial cancelling
- hexagon angles 120°
- a coordinate trapezoid with a 45° isosceles triangle
- a percent chain where you plug in the answers, starting with the round middle one

Findings:
- **BETTER: a value joins, so the average moves by its distance from the OLD average, divided by the NEW count.** Their example: 7 numbers with average 30, then 110 is added. 30 + 80/8 = 40.
  - Our t25 rule is "compare it to the new average", and then the old values balance it. That works well when the new average is given (the "how many before" questions). But when the new average is the unknown, the most common type, our rule asks the student to compare to something they don't know.
  - Their version is one line and always starts from known numbers. It is also our own "share the change over all the values" idea: the newcomer brings an extra (110 − 30 = 80), and that extra is shared among all 8.
  - Exam: averages has 23 questions. **2024_spring_q1_07** is this type: 3 gorillas averaging 135, and a 4th makes the average 120. So 120 = 135 + d/4, d = −60, and the 4th gorilla is 75 kg. Find-the-newcomer and find-the-new-average questions are the core of the averages topic.
  - **Change:** in t25 (lesson part with "Now a new number joins a group"), add a second case where the new average is the question. Say it in our words: "The newcomer is 80 above the old average. That extra is shared by all eight numbers now, so the average goes up by 10."
  - Keep the balance rule for "how many before". In the summary, replace "Compare the new value to the new average" with: "Joins: its distance from the old average, shared by the new count. Need the count? Use the balance."
- **Nothing new on the rest.** We cover:
  - the last digit of a product (t01)
  - the range of a quotient, "multiplying ranges end by end… when dividing" (t12)
  - factorial cancelling (t28)
  - interior angles (t34)
  - plugging in the middle choice (t51, "start with a middle choice")

## 5. Quantitative Tricks Psychometrics Fall 25 [hb2NPz39MiU]
**What it teaches:**
- consecutive a, b with 4a = 3b: write a = b−1
- an equilateral triangle's area gives its side, so its perimeter can be found
- AB+BA is a multiple of 11, and a two-digit multiple of 11 has equal digits
- triangles with the same height: area ratio = base ratio
- chain ratios with a shared middle term
- an inequality: multiply by a denominator known to be positive
- 2^k·k! = 2·4·…·2k
- hourglass similarity
- estimating (√3 ≈ 1) versus conjugates
- the average of 4 heights → the sum of 4 areas
- a rhombus with a silver triangle
- the difference of polygon angle sums with a common factor
- a negative exponent in a defined operation
- perpendicular walls in 3D
- multiples of 3 as 3a + 3b
- no circle has both an integer circumference and an integer area
- a motion table

Findings:
- **Nothing new.** We cover:
  - writing consecutive numbers with one letter (t16)
  - AB+BA (t18)
  - same height means base ratio (t31: "if the height is the same but one base is three times as long, that area is three times as big")
  - A to B to C as one to two to three (t22)
  - polygon angle sums (t34)
  - an edge perpendicular to a face (t35)
  - conjugates (t11)
  - estimation (t51)
- **SKIP: the integer circumference and area circle.** It is a one-off insight question. I found nothing like it in quant_real.md.
- **SKIP: the 2^k·k! product.** It is the D1 "product of n even numbers" tip again, so it is covered by D1's recommendation.

## 6. Quantitative Tricks from Actual Exams - Spring '25 [HDsilEEeMq0]
**What it teaches:**
- turn 2 into √4 and 3 into √9, then compare roots
- in a long product, follow only the x² term
- AB − BA = 9(A − B)
- the bronze triangle in a hexagon inside a rectangle
- |a + b| < a gives b < 0 and |b| < 2a
- a defined operation with a negative exponent
- add two inequalities that point the same way
- √x·√(x−1) is never an integer for x > 1
- x even, y divisible by 4, so x+y is surely divisible only by 2

Findings:
- **Nothing new.** We cover:
  - moving a number under the root (t09, t10)
  - tracking one term of a product (t05)
  - the AB − BA decomposition (t18)
  - the bronze triangle in a hexagon (t31, t34). This is exam **2025_spring_q1_18**.
  - adding inequalities (t12)
  - the 2n / 4m notation (t16)
- **CHECK:** for √x·√(x−1), they argue "consecutive numbers can't both be perfect squares, so the product isn't an integer". That reasoning is incomplete. Two non-integer roots *can* multiply to an integer, for example √2·√8 = 4. The real reason is that x(x−1) is never a perfect square for x > 1. Don't copy their argument as stated.

## 7. The eight most well-known tricks in psychometrics [ynqko3vRUew]
**What it teaches:**
- Pythagorean triples and their multiples
- the silver and gold triangles
- the equilateral area a²√3/4
- a triangle in a parallelogram is half of it
- cross-multiplying to compare fractions
- the average of evenly spaced numbers is the middle number
- x% of y = y% of x
- n! arrangements in a row

Findings:
- **Nothing new.** We have all eight:
  - triples (t31)
  - special triangles (t31)
  - equilateral area (t31)
  - the parallelogram triangle (t32, "the shaded triangle is half of the whole parallelogram")
  - cross-multiplying (t03)
  - "For equally spaced numbers, the middle is their average" (t16, t25)
  - the swap (t01, t23)
  - factorials (t28)
- **CHECK:** their swap example, as transcribed, is "72% of 12 = 12.5% of 72 = 9". 72% of 12 is 8.64. It only works as "72% of 12.5". That is probably a transcription slip, but don't copy the numbers.

## 8. Understanding and reasoning for psychometrics 10 [2v-JUelYD4A]
**What it teaches:** verbal logic: all/some/most statements and what follows from them.
- **Out of scope.** This is verbal reasoning, not quantitative. Nothing for our math course.

## 9. What should you do about a month before the exam? [6qnsWrPXFbU]
**What it teaches:** study advice. If you can only solve an early question by plugging in, and it takes you long, revise the topic. Chain inequalities (x > y > w). Square √x + √y and use x + y. The rest is verbal and English tips.

Findings:
- **Nothing new on the maths.** We cover chaining inequalities (t12, "Chain them") and squaring both sides (t04, t07).
- **CHECK:** the sample as heard is √(x+y) = 3, √x + √y = 5, so xy = 64. These numbers are impossible: x + y = 9 with xy = 64 has no real solution. Either the transcript is garbled or the source question had other numbers. If we ever build a question like this, check that the system has a real solution.

## 10. How to improve a high score in psychometrics? [QH9Amfrx6NE]
**What it teaches:** a sales pitch for private lessons, with examples:
- test divisors only up to √n
- only perfect squares have an odd number of divisors
- 16% of 25 = 25% of 16
- in a regular hexagon, the circumradius = the side and the short diagonal = side·√3
- draw radii to the points of tangency
- the incenter is where the angle bisectors meet
- a work formula
- lemons: weighted average where the distances are in the opposite ratio of the counts
- logic contrapositive, and some verbal and English items

Findings:
- **Nothing new.** We cover:
  - "Divisors come in pairs, so only a perfect square has an odd number of them" (t14)
  - "divide it by the primes up to its square root" (t14)
  - the swap (t23)
  - hexagon diagonals (t34)
  - "When there's a point of tangency, we draw the radius to it" (t33)
  - "The weights are two to one, so the distances are one to two" (t25)
- **SKIP: incenter = meeting point of the angle bisectors.** No real exam question in quant_real.md uses an angle bisector at all (0 hits).

## 11. Plugging in for psychometrics 1 [n1vqPnB7Kh4]
**What it teaches:** plugging in the answers. When to use it: the choices are numbers, or the question asks what "could be" or "cannot be". Start from the simplest choices. In a "could be" question, the first choice that works is the answer, because the exam has only one right answer.
- **Nothing new.** pt51-plug-answers covers the method, and t01 covers the three question words ("Could be true: one allowed example is enough"). Their "cannot be" angle example (a quadrilateral where 170° would leave nothing for the 4th angle) is nice, but it is not new.

## 12. Plugging in for psychometrics 2 [DRs-o-nrXs4]
**What it teaches:** plugging in numbers for "must be true" questions:
- choose numbers that satisfy the givens
- a choice that fits proves nothing; a choice that fails is out
- plug again until three choices are out
- **a "none of the above is necessarily true" choice can never be ruled out this way**, so if you are left with it and one other, solve with math
- good numbers to try are 1, −1, 0, fractions, negatives, very large and very small numbers, and roots (x = √3 so that x² is prime)
- "could be" works the other way: one fitting example, and you mark that choice

Findings:
- **GAP: the "None of the above / cannot be determined" choice when plugging in.** Our t51 plug-numbers lessons say "We don't look for the correct answer. We eliminate three." We never say what to do when choice 4 is "None of the above statements is necessarily true" or "It cannot be determined". A number can never rule that choice out, so plugging in can at best leave two choices. You then have two options:
  - (a) use understanding or algebra to decide whether the other survivor must always hold, or
  - (b) actively look for a number that breaks the survivor. If you find one, the answer is "None of the above".

  Also, if every allowed number keeps the same survivor, that is a strong hint, but not a proof.
  - Exam: quant_real.md has about 10 "None of the above … is necessarily true/correct" choices and about 14 "It cannot be determined…" choices. Examples: **2021_autumn_q1_16** (the answer *is* "none"), 2022_autumn_q1_06, 2024_winter_q1_05, 2019_winter_q1_05, 2022_winter_q2_08, 2025_autumn_q1_13. That is roughly one question per sitting, often in the harder half.
  - **ADD** to pt51-plug-numbers-2, the "rule out three" section: a short paragraph plus one worked example with new numbers. Their own example has the given (x+y)² > x² + y²: plugging leaves "xy > 0" and "none", and opening the brackets gives xy > 0. Build ours on a different given. Add one line to the t51 summary too: "A 'none' or 'cannot be determined' choice is never ruled out by a number. Two left with it? Try to break the other one, or prove it."
- **PARTIAL: which numbers to try in "must be true" questions.** pt51-plug-numbers-2 teaches "choose numbers that give distinct results; skip 0 and 1 with powers; give different letters different numbers". It doesn't say that the second try should *change the type* of number (negative instead of positive, a fraction instead of a whole number), even though that is what usually breaks a wrong choice. Their two examples both break a choice by flipping signs. t17 has the four-range idea, and t12 has "plug in a number from each range", but t51 never connects them.
  - **ADD AS ONE-LINE TIP** in pt51-plug-numbers-2, at the "tie-breaker" paragraph: "For the tie-breaker, change the kind of number: a negative, or a fraction between zero and one, if the question allows it."
- **PARTIAL: "could be" with plugging in numbers.** pt51-plug-numbers-3 says "To show that something is not always true, one example where it fails is enough." The mirror rule is missing there: in a "could be true" question, one allowed example where the choice works is enough, so mark it. We have it in t01 ("Could be true: one allowed example is enough"), but t01 is an old studio script. Their side-by-side, the same given (xy < 0) with a "must be" question and then a "could be" question, is a clear way to show the difference.
  - **ADD AS ONE-LINE TIP** in pt51-plug-numbers-3, after the "not always true" line. Optionally show the two question words on one given.

## 13. Plugging in for psychometrics 3 [NqbR3Xqy8fQ]
**What it teaches:** mixed practice:
- plugging in answers for a 2x + y = 5 system
- for an expression with √x and √y, plug in perfect squares (x = 4, y = 1)
- plugging in answers for a motion question, jumping to the large choice once the small one is far off
- a digit-ratio number (31, then 62)
- n chords through one point: draw n = 2 and n = 3
- a coordinate triangle with a = 1 and a = 2
- marbles x², y
- last digits for a "B ends in 5" question

Findings:
- **Nothing new.** pt51-plug-numbers and pt51-plug-answers cover all of these choices. "Choose numbers whose roots are whole" is implied by our "choose a convenient number". The chord drawing (plug a small n and draw it) is a nice example, but not a new method.

## 14. Twenty things you should know how to do quickly in psychometrics [ixOup0eLMNk]
**What it teaches:** a fluency checklist:
- times tables and a common factor (12·25 trick)
- fraction × fraction
- comparing fractions, cross-multiplying
- taking out 2^(n−1)
- an average as an equation
- special triangles, 6/√2 = 3√2
- round percents
- √a·√a = a
- rewriting 4 and 27 as powers
- d = v·t
- short multiplication formulas
- cube facts (4a² lateral, 6a² total)
- circle area and perimeter
- min/max overlap
- odd/even rules, including odd ÷ even
- similar triangles, Pythagoras
- the rule of three ("double date")
- exterior angle
- an even power is ≥ 0
- a minus before brackets

Findings:
- **Nothing new.** All covered across t01–t16, t24, t28, t31, t35. For example, t24: "The smallest overlap is the sum of the two groups, minus the total". t16: "Odd over even cannot give an integer".
- **CHECK (minor):** "min overlap = sum − total" is stated without the condition. When the sum is below the total, the minimum overlap is 0. Our t24 wording ("how far do the two groups go over the total") handles this. Keep ours.

## 15. Quantitative tricks chapter 1 [qurH2UfBKW4]
**What it teaches:** a 20-question "tricks chapter":
- a median gives equal areas
- 1001 is divisible by 7: split it as 700 + 280 + 21
- +p% then −p% always ends lower
- cube facts
- nested absolute value
- multiplying equations
- work: when a joiner halves the remaining time, the rates are equal
- glued pairs (2^6·6!)
- ABA + BAB = 111(a+b)
- |a+b| ≤ |a|+|b| (strict when the signs differ)
- reducing the weights in a weighted average
- conjugates
- a triangle in a rhombus
- odd ÷ even
- **a quadrilateral around a circle: opposite sides have equal sums**
- three-sided inequalities and x² ranges
- circles on a diameter
- the line through the origin
- 0.4% of 25 = 25% of 0.4

Findings:
- **SKIP: a quadrilateral that circumscribes a circle has equal sums of opposite sides.** We don't teach it. t33 has the tangent-segments fact it comes from ("two tangent segments from the same point to the same circle are equal"). I found no real exam question with a quadrilateral around a circle (the inscribed/circumscribed questions in quant_real.md are squares, hexagons and triangles). Not worth a lesson line.
- **Nothing new on the rest.** We cover:
  - "A Median Halves the Area" (t31, geo-018-after)
  - "Up twenty, then down twenty… four percent lower" (t23)
  - "Multiply the equations" (t06)
  - glued neighbors (t28)
  - the triangle inequality, "Rule three is about a sum" (t13)
  - conjugates (t11)
  - "x squared on the SMALL side, x is trapped between the roots" (t12)
  - the line through the origin (t37)
  - "add diameters before circumferences" (t36)
  - the swap (t23)
  - the work idea, in t26's "Two polishers as fast as A would need half the time"
- **SKIP: the "split 1001 into easy multiples of 7" trick.** It is a fine mental-math habit, but rare. Our t01 already teaches splitting numbers for mental arithmetic.

## 16. Quantitative questions in psychometrics that are important to know how to solve quickly [iTs_ifQ6nvk]
**What it teaches:** master the easy version of each topic before the hard one. Examples:
- gold triangle, equilateral triangle
- arcs of three touching circles (5πr)
- √72 = 6√2
- √(2√2) as a power
- a circle with a diameter equal to the radius (1:4 area)
- an incircle in a right triangle with similarity
- plugging in answers for x³ < x² < 4
- plugging in numbers for "which is surely an integer"
- primes, "double date" (rule of three)
- joint work (1¼ walls per hour)
- **flexible drawings**: if a square isn't fixed, CF can't be determined

Findings:
- **Nothing new.** Flexible drawing is t38: "We call these flexible-drawing questions". The rest is in t09–t11, t14, t22, t26, t31, t33, t36.
- Their study rule ("can't do question 1–10 of a topic? don't try question 11–20 yet") is good advice. It is about the order of practice, so it doesn't belong in a lesson.

## 17. Selected questions in Winter 23 quantitative - tricks and methods [UuAdQ7Fyqic]
**What it teaches:** real-exam Winter 23:
- sum = count × average (find the average of w, x, y, z from two pair averages)
- a^(2x) = 8, so a^x = √8 = 2√2
- odd ÷ even
- the fraction of a circular track gives the fraction of 360°
- AB = 9(A+B), so 81
- percent with multipliers (0.96, 0.8)
- steps: −9 then +10, plug in the answers
- a circle through the origin with an inscribed right angle on a diameter
- 100 boys and 101 girls in a circle: 99
- numbers between 10 and 12 whose product with 3 is an integer: thirds
- adding fractions
- exterior angle
- the hexagon short diagonal
- **one plug that matches is not the answer**
- **TV series: which season holds episode 120 (13 per season)**
- even divisors of 40
- |x|(x−2) < 0
- similar triangles (1:3 lengths → 1:9 areas)
- a line from a vertex splits the area in the ratio of the bases
- "x copies of 16x = 16x²"
- a bread-milk-cheese price system

Findings:
- **PARTIAL: which block holds the n-th item.** t21 teaches cycles with remainders ("divide by the length of the cycle, and look at the remainder"; "when the remainder is zero… it's the last one"). That gives the *position inside* a cycle. The other half is missing: *which* block it is in. The full blocks come first, so a remainder means the next block, and remainder 0 means the last item of the last full block. The common mistake is to take 120 ÷ 13 ≈ 9.2 and answer 9. Their way avoids decimals altogether: 9 seasons are 117 episodes, so the 120th is in season 10.
  - Exam: **2023_winter_q2_07** is exactly this.
  - **ADD AS ONE-LINE TIP** in the t21 cycles lesson, right after the remainder-zero line: "And which block is it in? Count the full blocks, then one more if there's a remainder." Or add a short guided question with new numbers. This one question per section of this type is cheap to cover.
- **Nothing new on the rest.** We cover:
  - "The sum is how many, times the average" (t25)
  - odd ÷ even (t16)
  - "rule out three" (t51)
  - exterior angles (t31)
  - the hexagon short diagonal (t34)
  - area factor = length factor squared (t31, t33, t36)
  - same height means base ratio (t31)
  - systems of equations (t06, t07)

  The 100/101 circle is a one-off insight question, so **SKIP**.

## 18. Selected questions from Spring 24 - tricks and methods [9Y0OJowLkEI]
**What it teaches:**
- t² = w² with t ≠ w, so t = −w and the average is 0
- 5000 mod 50 = 0, 5001 mod 50 = 1, and 4999 mod 50 = 49
- the gorilla average (their "new average" formula again)
- an even factor makes a product even
- plug in numbers for fractions-of-fractions (violins 10, strings 30, orchestra 50)
- an algebraic root simplification
- the percent formula with letters
- adding and subtracting two equations
- a cylinder volume ratio
- a square and hexagon in a circle (150°)
- probability where the first toy doesn't matter (1/7²)
- an equilateral prism base area
- giraffe ordering, liars (verbal-style logic)
- some verbal and English items

Findings:
- **Nothing new.** We cover:
  - "Two numbers with the same square are equal, or opposite" (t07)
  - "the biggest remainder is the divisor minus one" (t15)
  - "In percents, put a hundred at the whole" and choosing a convenient amount (t51)
  - the first pick (t29)
  - the even factor (t16)
- The gorilla question (**2024_spring_q1_07**) supports the BETTER finding in video 4.
- **SKIP: liar puzzles.** There are none in the real English quant sections (0 hits).

## 19. Selected questions from Fall 23 - tricks and methods [SKtT9hFzMLc]
**What it teaches:** real-exam Fall 23 (half of it is verbal: analogies, "lula"):
- the sum of 3 ages is 3 × Gadi, so Gadi is the average, and adding the average doesn't change it
- systematic listing (chess draws)
- the probability product that cancels down (1/2·2/3·…)
- |x| ≤ 5 and 4 ≤ |x| ≤ 6 on a number line
- the hexagon long diagonal 2a
- estimating Pythagoras against 30
- a ratio share (11:9:5 of 575) and ×11 mental maths
- choose 3 of 4 = 4 (choose who's out)
- x/7 = b, so x = 700% of b
- xy = 1 with x > 1, so the average is > 1
- a product of two primes = xy, so x and y are those primes
- the surface area of a quarter cylinder
- a three-set "common friends" min/max

Findings:
- **Nothing new.** We cover:
  - "If we add or remove a number equal to the average, the average doesn't change" (t25)
  - systematic listing (t21)
  - absolute-value bands (t13, t17)
  - the long diagonal (t34)
  - Pythagoras estimation (t51)
  - ratio shares (t22)
  - "times eleven" (t01)
  - "choose who stays OUT" (t28)
  - percent of (t23)
  - unique prime factorisation and divisor counting (t14)
- Their remark that plugging in can't remove choice 4 ("no statement is necessarily true") is the GAP in video 12 again. Here they say it directly and recommend going algebraic from the start when such a choice is present. That supports the ADD.
- **SKIP: "xy = 1, x > 1 → average > 1".** It is the x + 1/x ≥ 2 idea. I found nothing in quant_real.md (0 hits for xy = 1 or "reciprocal").

## 20. Selected questions from Summer 23 - tricks and methods [fTjcRSWlxj0]
**What it teaches:**
- glued pairs (2·2·2 = 8)
- a cube with surface 18, so its edge is √3 and the circle is 3π
- percent min/max of blue clothes (20%–60%)
- x² − |x| = 0: try −1, 0, 1, so 3 solutions
- increase by 4000%, so ×41
- estimate a division by multiplying the choices
- with replacement, every color sequence is equally likely
- a fraction's powers are smaller and its root bigger
- angles α, 2α, 3α give the 30-60-90 triangle
- (1+2b)² < … gives b² < 1, so −1 < b < 1 ("don't take the root of an inequality")
- three distinct primes give 8 divisors

Findings:
- **Nothing new.** We cover:
  - glued items (t28)
  - cube surface (t35)
  - overlap ranges (t24)
  - "Fifty percent more is a hundred fifty percent, so it's times one point five" (t23)
  - multiplying the choices back (t51 plug answers)
  - "Every order has the same chance" (t29)
  - power and root order in (0, 1) (t17)
  - x² ranges (t12)
  - divisor counts (t14)
- **CHECK:** for "how many solutions does x² − |x| = 0 have", they only try −1, 0, 1 and stop. Trying numbers can't show there are *no other* solutions. Here |x|(|x| − 1) = 0 proves it. If we use a solution-count question, give the reason, not just the trial.

## 21. Psychometric questions you can solve in less than 10 seconds - part C [sf-tw_jxcaw]
**What it teaches:**
- 5α + α = 360
- isolate y
- √(4⁴) via power ÷ index
- **in a regular polygon, the diagonals from four consecutive corners cross at an angle equal to the polygon's interior angle** (pentagon gives 108°)
- add equations
- 3 < x < 4, so x = √14
- x!/(x−1)! = x
- consecutive a, b = a+1
- a = 7 − x² ≤ 7
- three face diagonals of a cube make an equilateral triangle (60°)

Findings:
- **PARTIAL: the crossing-diagonals angle in a regular polygon.** t34 solves the pentagon "middle angle at S between the two diagonals" in three ways. But that is two diagonals from the *same* corner. We don't have the case of two diagonals from *neighboring* corners (AC and BD) crossing inside, or its shortcut: the angle facing side BC equals the interior angle. It works because triangle BPC has two base angles of (180° − interior)/2 each.
  - Exam: **2023_spring_q2_03**, "regular pentagon ABCDE and two of its diagonals, α = ?" (answer 108°). The 2026_spring_q2_19 nonagon with four diagonals is in the same family.
  - **ADD AS ONE-LINE TIP** in t34, after the diagonal lesson. Better still, add a guided question (a hexagon with AC and BD gives 120°, new numbers), where we show *why* with the isosceles triangle and then state the shortcut.
- **Nothing new on the rest.** We cover:
  - power ÷ index (t10, t11)
  - "nine factorial is nine times eight times seven factorial" (t28)
  - an even power is ≥ 0 (t17)
  - "two numbers in a row" with one letter (t16)
  - cube diagonals (t35)

## 22. Nine common quantitative principles in psychometrics, part B [7EbVKlsLPI0]
**What it teaches:**
- making a/b bigger or smaller (numerator and denominator)
- numbers with remainder r come in steps of the divisor
- coprime numbers: divisible by both means divisible by the product (8 and 10 do not give 80)
- even and odd powers, signs in subtraction
- prime factorisation and counting prime divisors
- writing consecutive numbers with one letter
- multiplying equations
- operating on three-sided inequalities
- shaded area = sector − triangle

Findings:
- **Nothing new.** We cover:
  - "Dividing by a positive number smaller than one makes six larger" and the size rules (t17)
  - "a number that leaves four when divided by five is five k plus four" (t15)
  - "because three and seven share nothing" (t14)
  - signs (t01, t17)
  - prime factorisation (t14)
  - consecutive numbers (t16)
  - multiplying equations (t06)
  - three-sided inequalities (t12)
  - area subtraction (t32, t33)

---

## Counts
- Videos reviewed: 22 (1 is verbal-only and out of scope)
- GAP: 1 (the none/cannot-determine choice when plugging in)
- PARTIAL: 6
  - the radius form of the equilateral nesting
  - exactly one of three consecutive integers divides by 3
  - change the kind of number for the tie-breaker
  - "could be" in t51
  - which block holds the n-th item
  - crossing diagonals in a regular polygon
- BETTER: 1 (the new average from the old average, shared by the new count)
- CHECK: 5
  - the √x·√(x−1) argument
  - the 72%-of-12 numbers
  - the impossible root system
  - the min-overlap condition
  - counting solutions by trial
- SKIP (checked, not worth adding): 9

## Top recommendations (most valuable first)
1. **t51 pt51-plug-numbers-2 (and summary): ADD how to handle a "None of the above is necessarily true" or "It cannot be determined" choice when plugging in.** A number never rules it out. When you are left with it and one other choice, try to break the other one (change the kind of number), or prove it by understanding or algebra. About 24 real questions have such a choice, and sometimes it is the answer (2021_autumn_q1_16). This is the one real hole in our plugging-in method.
2. **t25 averages lesson and summary: BETTER, add the "shared extra" form for a value that joins.** New average = old average + (newcomer − old average) ÷ new count. It starts from known numbers in the common "find the new average" and "find the newcomer" questions (2024_spring_q1_07). Keep our balance rule for "how many were there before".
3. **t34: ADD a guided question plus a one-line tip for crossing diagonals from neighboring corners.** The angle equals the interior angle (2023_spring_q2_03; nonagon 2026_spring_q2_19). Show why with the isosceles triangle.
4. **t33 nested shapes: ADD AS ONE-LINE TIP the radius form.** The circle around an equilateral triangle has twice the radius of the circle inside it, and the side is R√3. 2019_winter_q2_08 (the ring = 3π) tests it directly. Add a guided ring question with new numbers.
5. **t21 cycles lesson: ADD AS ONE-LINE TIP "which block holds the n-th item".** Count the full blocks, plus one if there is a remainder. Don't round a decimal. Exam 2023_winter_q2_07 (episode 120, 13 per season).
6. **t15: ADD AS ONE-LINE TIP "exactly one of any three consecutive integers divides by 3".** Once you know which one, the others are not. Exam 2025_winter_q1_14. Same as D1's tip, so one edit covers both.
7. **t51 pt51-plug-numbers-2: ADD AS ONE-LINE TIP: for the tie-breaker, change the kind of number** (a negative, or a fraction between 0 and 1, if allowed). That is what usually breaks a wrong "must be" choice, and it links t51 to the t17 ranges.
8. **t51 pt51-plug-numbers-3: ADD AS ONE-LINE TIP the "could be" mirror rule.** One allowed example where the choice works is enough, so mark it. Optionally show one given with a "must be" and a "could be" question side by side. Today this lives only in the old t01 script.
9. **Don't copy (CHECK):**
   - the √x·√(x−1) "one root isn't whole" argument (√2·√8 = 4 breaks it)
   - "72% of 12 = 9"
   - the impossible √x + √y = 5, x + y = 9 example
   - counting equation solutions by trying −1, 0, 1 without a reason
10. **SKIP list (checked, not worth it):**
    - opposite sides of a quadrilateral around a circle (no exam hits)
    - incenter / angle bisectors (0 hits)
    - liar puzzles (0 hits)
    - xy = 1, so the average is > 1 (0 hits)
    - the circle with integer circumference and area (one-off)
    - splitting 1001 to test 7
    - the 100-boys/101-girls circle
