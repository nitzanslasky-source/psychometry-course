# External course review, group D1 (tricks, plugging in, methods, 700+, tips: first half), 21 Oct 2026

22 videos reviewed. I read every transcript in full. Our course was checked with grep on `scratchpad/ext/course/tNN.txt` (several phrasings for each idea). Exam frequency comes from `studio-build/real_exam/quant_real.md` (19 English sections).

Overall: our course already covers almost everything this channel calls a "trick": bronze triangle, octagon cut, seesaw, product over sum, speed ratios, x% of y swap, the two-change formula, the reversal rules for 11 and 9, coprime splitting, pigeonhole, odd number of divisors, circles on a diameter, the "man with glasses", conjugates, and the times-eleven method. The real gaps are a few geometry rules (the trapezoid midsegment, R = 2r in an equilateral triangle, the "same triangle" trap), some extra plugging-in rules for topic 51 (cannot be determined, which kinds of numbers to try, same value allowed), and a few one-line number-property rules.

Tags: GAP = we don't teach it. PARTIAL = we teach part of it. BETTER = their explanation is clearer. CHECK = their video is wrong or misleading.
Recommendations: ADD / ADD AS ONE-LINE TIP / SKIP. Per R37, if an ADD is a one-off trick, it goes in a question (about 2 minutes) rather than as a bare line. If it is a rule several questions use, it goes in the lesson.

---

## 1. 10 psychometric tricks that few people know [TblUUTriCCQ]
**What it teaches:** Ten short tips. The maths ones are:
- a product of n even numbers divides by 2^n
- chase time = starting gap ÷ difference of speeds
- the bronze (120-30-30) triangle
- an octagon cut into a square, 4 rectangles and 4 silver triangles
- the deviations from the average add up to 0
- two percent changes: a + b + ab/100
- a line perpendicular to two lines of a plane is perpendicular to the whole plane
- in n consecutive integers exactly one divides by n

The rest are writing-task and analogy tips, which I ignored.

- **PARTIAL: a product of n even numbers divides by 2^n.** In t16 we have "two even numbers → product divides by four" and "two even numbers in a row → eight". We never give the general rule that each even factor brings its own 2. Their example: p and q are primes > 100, so (p+1)(q+1) surely divides by 4.
  - Exam: number_properties has 27 questions; this rule shows up inside "necessarily divisible by" questions.
  - **ADD AS ONE-LINE TIP** in the t16 lesson, right after the "two even numbers → four" paragraph: "Three even numbers bring three twos, so their product divides by eight."
- **PARTIAL: exactly one of n consecutive integers divides by n.** t15 and t16 say "every third integer divides by three, so one of these three…". That is "at least one". The useful consequence is missing: the next multiple is n steps away. Their example: (m+3)(m+4)(m+5)(m+6) divides by 5, so one of those four is the multiple of 5. That means m+2 and m+7 are not.
  - Exam: rare (consecutive-integer questions are about 39 hits, mostly sums and products).
  - **ADD AS ONE-LINE TIP** in the t15 consecutive-numbers paragraph.
- **Nothing new on the rest. We cover:**
  - chase: t27, "Same direction — a chase. Subtract the speeds", with head start = gap
  - bronze triangle: t31 cuts it in half into gold triangles (a, a, a√3); t34 has the hexagon corner triangle with "the same area as an equilateral triangle"
  - octagon: t34, square + 4 rectangles + 4 corner triangles
  - deviations: t25, "The fifth score must balance them"
  - two-change formula: t23, "a short formula for two changes in a row"
  - line perpendicular to a face: t35, "The edge is perpendicular to the whole face"
- **CHECK:** the transcript says primes greater than 100 "are even". It means odd. This is probably a transcription error, but don't copy it: p+1 is even because p is odd.

## 2. 5 Random Psychometric Exam Tips - Part 2 [RyQH9afoi48]
**What it teaches:**
- the exterior angle = the sum of the two far angles
- equal sides give equal angles only inside the same triangle
- the line joining the centres of tangent circles passes through the tangency point
- the radius to a tangency point is a good helper line
- writing-task and verbal tips, which I ignored

- **GAP: the "same triangle" trap.** Two angles that face equal sides are not equal when they sit in two different triangles. Our t31 isosceles lesson teaches the rule both ways ("If two angles of a triangle are equal, the sides opposite them are equal"), but it never warns that the rule works only inside one triangle. I grepped "same triangle", "different triangles" and "another triangle": none of them are about this.
  - Exam: triangles has 24 questions; this is a classic figure trap.
  - **ADD AS ONE-LINE TIP** in the t31 isosceles lesson, and use it as the trap choice in one t31 question.
- **Nothing new on the rest. We cover:**
  - exterior angle: t31, solved "with an exterior angle"
  - line of centres: t33, internal and external tangency
  - radius to the tangency point: t33, "When there's a point of tangency, we draw the radius to it"

## 3. 5 Random Tips for the Psychometric Entrance Test - Part 1 [1qn8W26YVJA]
**What it teaches:**
- defined operations: read the rule as "$(something) = 2·something + 1", including the inverse case $(2x) = 5x − 3 → $(x) = 2.5x − 3
- the percent formula part = percent × whole / 100, with roots (√5% of √20 = 1/10)
- an inequality chain: use only two of its sides
- a shape comes with its properties; a trapezoid inscribed in a circle must be isosceles
- an analogy tip, which I ignored

- **GAP: a trapezoid inscribed in a circle is isosceles.** It is in neither t32 nor t33 (I grepped trapezoid + inscribed/circle).
  - Exam: no trapezoid-in-a-circle question in the 19 English sections.
  - **ADD AS ONE-LINE TIP** (low priority) in the t33 inscribed-shapes lesson. Reason: the parallel chords cut equal arcs, so the legs are equal.
- **Nothing new on the rest. We cover:**
  - defined operations: t19, "rewrite the rule so it works on any input… x is half of two x. So the diamond takes half of its input, and then adds five". That is the same idea.
  - percent with letters: t23, "part over the whole, times a hundred", with the 25g/N example
  - chaining inequalities: t12, "Chain them"

## 4. 700+ for the Psychometric Entrance Test 3 [d3GMxDiXul8]
**What it teaches:** integer extras:
- divisibility by 7 (drop the last digit, subtract twice it) and by 11 (alternating sum)
- coprime pairs for divisibility by a product (12 = 3·4, not 2·6)
- pigeonhole (11 numbers → two end in the same digit, so their difference divides by 10)
- which parities a quotient can have (even/odd, odd/odd …)
- primes up to 100; 97 is the largest two-digit prime; odd ÷ 2 leaves 1; the largest remainder is the divisor − 1
- multiple + multiple, multiple + non-multiple, non-multiple + non-multiple
- the parity of prime + prime

- **PARTIAL: the sum-of-multiples rules.** We use "both parts are multiples of three, so the sum is" (t15). We don't say the other two cases:
  - a multiple + a non-multiple is never a multiple
  - two non-multiples can be either (1+2 = 3, 1+4 = 5)

  These rule out "necessarily" choices fast.
  - Exam: divisibility_remainders has 36 questions, and "necessarily" statements are common there.
  - **ADD** in the t15 lesson: three sentences, each with a number example (per R37, as a short rule with examples, not a bare line).
- **SKIP: divisibility by 7.** The channel itself says it's almost never needed. Dividing is just as fast.
- **Nothing new on the rest. We cover:**
  - 11 rule: t15, "alternate subtraction and addition across the digits"
  - coprime: t14 and t15, including "Eighteen divides by two and by six, but… not by twelve"
  - pigeonhole: t20, r26-t20-counting
  - quotient parity: t16, "Even over odd…", "Odd over even cannot give an integer"
  - primes: t14, primes to 40 and ninety-seven
  - largest remainder: t15
  - prime + prime: t14, "If two primes give an odd sum… one of them is two"
- **CHECK:** he first says "if one of the numbers is prime, the GCD is 1", then corrects himself (14 and 7). Don't copy the first version. Two *different* primes are coprime; a prime and its own multiple are not.

## 5. 700+ for the Psychometric Exam 5 [1R1dv00rHIY]
**What it teaches:** circle facts:
- circles on a diameter: the small circumferences add up to the big one
- two equal circles on a diameter make 4 equal areas
- more equal circles on a diameter cover less total area
- two equal circles through each other's centres: the shared area is between ⅓ and ½ of a circle, and the shared arc is ⅓ of the circumference
- the 3 altitudes of an equilateral triangle make 6 congruent gold triangles, and R = 2r, so the circle areas are ×4
- volume factors read from the formula (r ×2 and h ×3 → ×12)

- **PARTIAL: equilateral triangle, R = 2r.** In t33 we teach "triangle, circle, triangle… four times" (the outer triangle side is twice the inner side). We never state the companion fact for "circle, triangle, circle": the circle around the triangle has twice the radius of the circle inside it, so 4 times the area. This is exactly real exam **2019_winter_q2_08**: r = 1, find the ring, answer 3π. I found no ring or annulus question like it in t33.
  - **ADD** to the t33 nested-shapes lesson as a fourth arrangement (circle, triangle, circle → ×4, so the ring = 3 inner circles). Back it with the centroid 2:1 or with the 30-60-90 triangle at the centre.
- **PARTIAL: the overlap of two circles through each other's centres.** t33 teaches it exactly (two equilateral triangles, 120°, two segments). It doesn't give the size benchmark "a bit more than a third of a circle (about 0.39), less than half". Their 700+ 8 question compares two such figures with no calculation at all, just using "more than a third".
  - **ADD AS ONE-LINE TIP** in t33 after the shared-region paragraph, for estimation.
- **Nothing new on the rest. We cover:**
  - circumferences on a diameter: t36 g137, "The big circumference ALWAYS equals the sum of the small ones — no matter how many, even if they're different sizes"
  - 4 equal areas: t36, "the man with glasses"
  - total area shrinks: t36 g137, "cover just a sixth of the big AREA"
  - volume factors: t36, "radius times three, height times two... volume times eighteen"
- Note: the circumference rule is real exam **2020_autumn_q2_14** (sum of the small circumferences = x). It is filed under Circles, but we teach it only in t36, which is an older studio version still to be rewritten. Keep it in the t36 rewrite, and add one line where t33 teaches circumference.

## 6. 700+ for the Psychometric Exam 7 [ifaktTaBF4s]
**What it teaches:**
- equal times → speed ratio = distance ratio
- equal distances → the time ratio is the speed ratio flipped
- the same in work problems (rate ratio = work ratio)
- two workers together: product over sum

**Nothing new. We cover:**
- t27 wp-110 "Speed Ratios": "What is fixed? Time, speed, or distance?", "Speeds three to four — times four to three. Flip it."
- t26: flip rule, and "the two-worker shortcut… multiply the two times, and divide by their sum"

## 7. 700+ לפסיכומטרי 1 [lOFt8-N8XA0]
**What it teaches:** mental arithmetic:
- times 11 (write the two digits apart and put their sum in the middle)
- 64·56 = 60² − 4²; 37² = (30+7)²; 59² = (60−1)²
- 25 = 100/4; 2.5 = 5/2
- add or subtract by making a round number (18+27 = 20+25; 83−27 = 86−30)
- teen × teen (17·18)
- the last digit first

- **Nothing new. We cover:**
  - times 11: t01, "Times eleven is times ten, plus one more copy"
  - same distance from a round number: t05 and t04, "Two numbers the same distance from a round number? Sum times difference"
  - near a round number: t01
  - 25 is a quarter of 100: t01
  - "Add the same amount to BOTH numbers — and the gap between them doesn't change": t01
  - last digit: t51
- **SKIP: the teen × teen trick.** It's narrow, and our near-round method does the same job.
- Their times-11 "digit sum in the middle" is not better than ours. It only works for two-digit numbers, and ours works for any number.

## 8. 700+ לפסיכומטרי 2 [LevVhkxuWVI]
**What it teaches:**
- rationalising with the conjugate (2/(√5−√3) = √5+√3)
- powers of positive fractions get smaller
- exponential equations with the same base
- an exponential **inequality** with a base between 0 and 1 flips the sign
- products and quotients of roots with the same index
- ∛7·∛7·∛7 = 7
- which is smallest of √5, ∛9, ⁴√17, ⁵√31 (compare each with 2 using 4, 8, 16, 32)
- √2 ≈ 1.41, √3 ≈ 1.73, √5 ≈ 2.24
- 2^x + 2^x = 2^(x+1); 3^7 + 3^8 = 4·3^7

- **GAP: exponential inequality with a fraction base.** It isn't in t11 or t12. Even the channel says it has never seen one on the exam, and there is none in the 19 English sections.
  - **SKIP**, or one line in t11 for strong students only.
- **PARTIAL: bounding roots of higher index between whole numbers.** t51 estimation teaches square roots between two whole numbers ("Root fifty is between seven and eight"). It doesn't teach cube, 4th or 5th roots against the nearest perfect power (∛9 > ∛8 = 2, ⁵√31 < ⁵√32 = 2).
  - Exam: higher-index roots appear (for example **2023_spring_q2_04**, ⁴√(2^8)).
  - **ADD AS ONE-LINE TIP** in pt51-estimation-2 or t11: "Any root: compare with the nearest perfect power."
- **Nothing new on the rest. We cover:**
  - conjugates: t11, "Method 1 · Conjugates"
  - √5: t11, "about two point two four"
  - 2^x + 2^x: t10, the trap line; t08, "three times three to the n. Three to the n plus one"
  - root laws: t09 and t11

## 9. 700+ לפסיכומטרי 4 [Y_rDJ5VLC3U]
**What it teaches:**
- the triangle midsegment (parallel, half, area ¼) and the **trapezoid midsegment** (parallel, = the average of the bases; any 2 of its 4 properties prove the other 2)
- a quadrilateral around a circle: the sums of opposite sides are equal (Pitot)
- the same perimeter gives the biggest area to the more regular shape, and the same area gives the smallest perimeter
- the perpendicular from the centre bisects the chord, the arc and the central angle
- the tangent-chord angle = the inscribed angle on the other side

- **GAP: trapezoid midsegment = (top + bottom)/2.** It's not in t32 (no "midsegment", "midline", "average of the bases" or "half the sum"). The triangle midsegment is in t36 ("DF is called a midpoint segment… parallel to the third side", ratio 1:2) and in t31 g018.
  - Exam: quadrilaterals is the 2nd-largest geometry block (43 questions). **2020_autumn_q2_02** (EF splits a trapezoid into two trapezoids, area ratio 3:7) looks like a midsegment question. Its answer fits bases 1 and 9 with a midsegment of 5, but check the figure.
  - **ADD** in the t32 trapezoid lesson: the rule, why it's true (it's an average, like the area formula's (a+b)/2), and 2 examples. It also gives the trapezoid area as midsegment × height.
- **GAP: Pitot (opposite sides of a quadrilateral around a circle add up to the same).** t33 has the parent rule, "two tangent segments from the same point… are equal". There is no tangential-quadrilateral question in the English sections.
  - **ADD AS ONE-LINE TIP** inside a t33 question where it fits (it follows in one line from the equal-tangents rule). Otherwise SKIP.
- **GAP: the tangent-chord angle.** It's not in t33, and none of the 9 "tangent" items in the English sections needs it.
  - **SKIP.** It's a matriculation theorem, and the exam's tangent questions use radius ⟂ tangent and equal tangents.
- **Nothing new on the rest. We cover:**
  - isoperimetric: t38, "two regular shapes with the same perimeter — … the hexagon has the bigger area", "The circle I make will have the biggest area"
  - perpendicular bisects the chord: t33. The equal arcs and central angle are partly there ("equal chords cut off equal arcs"), which is enough.

## 10. 700+ לפסיכומטרי 6 [CymNj3AXP3w]
**What it teaches:** the weighted average of two groups with a "scale":
1. Put the two values at the ends.
2. Put the average near the bigger group.
3. Stretch the ratio of the amounts so it adds up to the gap.
4. The small number goes on the short side.

Examples: 69 and 83 with weights 4:3 → 75; 52 kg and 72 kg with 31:93 → 67.

**Nothing new. We cover:** t25 has exactly this as the seesaw, with its own visuals. "The weights are two to one, so the distances are one to two. We cut the gap into two plus one, three units… The heavy side gets the small part." Ours (cut the gap into units) is simpler than theirs (stretch the ratio until it adds up to the gap). No change.

## 11. 700+ לפסיכומטרי 8 [lpcBrWkckCs]
**What it teaches:** a set of sample questions:
- (24²−23²)/(81−34)
- 2^(x+2) is how many times 2^(x−2)?
- 3 random integers → two have an even sum (pigeonhole on parity)
- an isosceles trapezoid with perpendicular diagonals: midsegment = height
- 2 equal circles on a diameter, ratio of black to white
- a weighted percent with 6:7 (34%, 47% → 41%)
- a circular track in opposite directions with the 3rd meeting at 30 min, so the 1st meeting is at 10 min
- comparing chains of overlapping circles with the "> ⅓" benchmark

- **PARTIAL: repeated meetings on a circular track.** t27 has "They meet when together they have covered one full lap". It doesn't have the next step: every meeting is one more lap together, so the meetings are equally spaced and the 3rd meeting is at 3 × the time of the 1st.
  - Exam: motion has 12 questions, and only 1 is circular.
  - **ADD AS ONE-LINE TIP** in that t27 question.
- **PARTIAL / ADD with the trapezoid midsegment:** an isosceles trapezoid with perpendicular diagonals has height = midsegment = (a+b)/2. Each part of the height is a median to the hypotenuse of a right isosceles triangle.
  - **ADD** as one hard t32 practice question after the midsegment rule is taught. Low priority.
- **Nothing new on the rest. We cover:**
  - difference of squares and the round subtraction: t05, t01
  - pigeonhole: t20
  - man with glasses: t36
  - seesaw: t25
  - powers division: t08 and t10
  - circle overlap: see entry 5

## 12. 9 Tips for Picking Numbers on the Psychometric Exam [RUhEI3ah2jk]
**What it teaches:**
- plug in 0 first when it's allowed
- different letters may get the same value unless they're said to be different (0 for all of them)
- choose numbers that make roots whole (x = 1/8 or −8 for a cube root)
- rule out three; don't mark the first choice that fits
- when they ask "must be true", one plug can never rule out "cannot be determined". Plug a second number of a very different size (0 and 6000), or use algebra.
- "could be true": one example that works is enough
- vary the *kind* of number: integer → fraction → root (x = √2 makes x² prime), positive → negative, even ↔ odd (1, 2, 3 then 2, 3, 4)

- **BETTER: same value for every letter.** In pt51-plug-numbers-3 our summary says "Give different letters different numbers". pt51-plug-numbers-2 explains that this is about ties *when the choices have letters*, but the summary line reads as a general rule. Theirs: when the choices are numbers, the fastest legal plug is often the same easy value for every letter (all zeros), and that's allowed.
  - Why it's better for a weak student: our general line makes them avoid the fastest plug.
  - **Change:** in the pt51-plug-numbers-3 summary and in pt51-summary, say "When the choices have letters, give different letters different numbers. When the choices are numbers, one easy value for every letter, often zero, is fine, if the question allows it."
- **PARTIAL: "cannot be determined" and plugging in.** t51 has "if the answer changes with your choice, then it cannot be determined", plus the trap of picking it too fast. It never says:
  - a plug can never rule out "cannot be determined"
  - to *show* that the answer changes, the second number has to be really different (0, then a big number, a negative or a fraction)
  - if two very different numbers give the same result, back it up with a reason or with algebra before ruling out "cannot be determined"

  Exam: "cannot be determined" / "none of the above"-type choices appear 24 times in the English sections.
  - **ADD** in pt51-plug-numbers-3: 3–4 sentences and one short example. This is the most valuable plugging point in the group.
- **PARTIAL: a list of kinds of numbers to try.** t12 has it ("zero, one, negative one, one half... and a big number"), but only for inequalities. t51 doesn't give it as a general plugging tool for "must be true" or "could be true" questions (number_properties 27, generality 20).
  - **ADD** to pt51-plug-numbers-2, after "choose numbers that help tell the choices apart". Include a root (√2) and a switch in parity (odd-even-odd → even-odd-even) as examples.
- **PARTIAL: choose numbers that make the root whole.** t51 says "skip zero and one, start with two or three". It never says to pick a perfect square or cube when the expression has a root (x = 4 or 9 for √x; x = 8 or 1/8 for ∛x).
  - **ADD AS ONE-LINE TIP** in pt51-plug-numbers-2.
- **Nothing new on the rest. We cover:**
  - rule out three: t51, many times
  - could be true: t20, "When it asks what could be true, one allowed example that works is enough"
  - zero first: t51 summary, "give one letter an easy value, zero first"

## 13. Algebra or placements on the psychometric test- Which method will raise your score- [PjlHQgnPHT4]
**What it teaches:** when plugging in is good (one method for many questions, mid scores, fast calculators) and when algebra wins. Examples:
- bc = b+c (plug b = c = 2)
- AB − BA = 9 → 10A+B − (10B+A) → A − B = 1
- a + 2b = 3a + 2 → a = b − 1, so they're consecutive. Plugging here is slow.
- a < b < c < 0 → sign rules beat plugging
- a leaves remainder 2 when divided by 4: what does a+3 leave when divided by 3? Write a = 4n+2 → it cannot be determined; plugging can't confirm that.
- the smallest 2/5 − m → find the largest m by comparing with ⅓
- simplifying a root expression with algebra

- **PARTIAL: signs that plugging is the wrong tool.** t51 teaches when to plug. It never names when *not* to: when the given is a condition that your numbers must satisfy and you can't see such numbers at once, simplify the given first. It often hands you the relation directly (a = b − 1 → consecutive). Case 4 of t51 ("more letters than equations… give one letter an easy value… solve for the rest") partly covers this.
  - **ADD AS ONE-LINE TIP** in pt51-plug-numbers-3 case 4: "If it's hard to find numbers that fit the given, simplify the given first."
- **Nothing new on the rest. We cover:**
  - "solve every question both ways": t51
  - sign rules by understanding: t51, pt51-understanding
  - place values 10A+B: t18
  - "write it as divisor times a whole number": t15
  - fraction benchmarks: t02 and t03
  - "cannot be determined": see entry 12
- **CHECK (opinion, not maths):** he says he plugs in only 1–2 times per exam, and that high scorers can't rely on it. That contrasts with our "the most important technique on the exam". No change is needed, because we already teach the math way first and both ways at home. Just don't import his framing.

## 14. Meet the Channel's Cheat Sheet [Dk7-RmDzzxQ]
**What it teaches:** an odd number of divisors means a perfect square (144). The rest is an ad.
**Nothing new.** t14: "Divisors come in pairs, so only a perfect square has an odd number of them."

## 15. Meet the Channel's Trick Collection [6rfRISectIA]
**What it teaches:** circles on a diameter: the sum of their circumferences = the big circumference (ratio 1:1). The rest is an ad.
**Nothing new.** t36 g137 (see the note in entry 5 about also adding it to t33).

## 16. Psychometric trick in 1 minute - 1 [3vPQMuwfTzc]
**What it teaches:** for 3a/7 = 18, divide both sides by 3 first (a/7 = 6, so a = 42) instead of multiplying by 7 first.
- **GAP (small):** t06 and t07 isolate x in the usual order. Neither says "divide by the number on top first when it goes into the other side". It saves a big multiplication.
  - Exam: equations has 33 questions; minor saving.
  - **ADD AS ONE-LINE TIP** in the t06 lesson where fractions with x on top are solved.

## 17. Psychometric trick in 1 minute - 11 [RjBO87NjJTE]
**What it teaches:** the average of evenly spaced numbers is the middle number, or (first + last)/2. Example: the average of the multiples of 7 from 1 to 100 is (7+98)/2.
- **Nothing new.** t25: "Evenly spaced numbers are symmetric… it's the middle one, or first plus last, over two."
- **CHECK:** (7+98)/2 = 105/2 = **52.5**, but the transcript says "52". This may be a transcription error, but don't copy the number.

## 18. Psychometric trick in 1 minute - 6 [UZL-L4R_od4]
**What it teaches:** AB + BA divides by 11 and AB − BA divides by 9. Example: AB + BA = 8C → 88 → C² = 64.
**Nothing new.** t18: "A two-digit number plus its reversal is divisible by eleven. A two-digit number minus its reversal is divisible by nine. And a three-digit number minus its reversal is divisible by ninety-nine."

## 19. Psychometric trick in 1 minute - 8 [eVKTBIWzM_M]
**What it teaches:** the order of percent changes doesn't matter, so do the round ones first.
**Nothing new.** t23: "The same result, in any order", using the multipliers. You could add "so do the round change first" as a few words, but it's optional.

## 20. Psychometric trick in 10 minutes [wAhSE77IHn0]
**What it teaches:** divisible by two coprime numbers → divisible by their product. Example: 18 = 2·9, not 3·6.
**Nothing new.** t15: "Why not split twelve as two times six? Look at eighteen…" and t14: "three and seven share nothing".

## 21. Psychometric trick in 3 minutes [IahocEbK2G0]
**What it teaches:** x% of y = y% of x (48% of 12 = 12% of 48 = 48/8 = 6).
**Nothing new.** t23: "So x percent of y is equal to y percent of x. We can swap them when it makes the calculation easier."

## 22. Psychometric trick in 5 minutes [j56otFVFS7w]
**What it teaches:** the bronze triangle: isosceles with a 120° apex, so the base is a√3 and the area is a²√3/4. It appears as the corner triangle of a regular hexagon.
**Nothing new.** t31 shows it by halving into gold triangles ("the sides are a, a and a root three"). t34 has the hexagon corner triangle, "thirty, thirty and one hundred twenty… the same area as an equilateral triangle". We don't use their name for it, and we don't need it.

---

## Counts
- Videos reviewed: **22**
- GAP findings: **7**
  - same-triangle trap
  - inscribed trapezoid is isosceles
  - exponential inequality with a fraction base
  - trapezoid midsegment
  - Pitot
  - tangent-chord angle
  - divide first in equations
- PARTIAL findings (we teach part of it): **13**
  - products of evens 2^n
  - exactly one of n consecutive
  - multiple + non-multiple
  - R = 2r
  - circle-overlap benchmark
  - higher-index roots
  - circular-track meetings
  - isosceles trapezoid with perpendicular diagonals
  - "cannot be determined" with plugging
  - kinds of numbers to try
  - root-friendly numbers
  - when not to plug
  - a t33 line for circles on a diameter
- BETTER: **1** (same value for every letter)
- CHECK: **4** (primes > 100 "even"; 52 vs 52.5; "one prime → coprime"; the opinion on plugging)
- Recommended SKIP: divisibility by 7, teen × teen, exponential inequality (or one line), tangent-chord angle, Pitot (unless it fits a question)

## Top recommendations (most valuable first)
1. **t51 pt51-plug-numbers-3: "cannot be determined" and plugging in** (ADD, 3–4 sentences + one example).
   - A plug can never rule it out.
   - To show the result changes, use a really different second number (0, then a big one, a negative or a fraction).
   - If it doesn't change, back it with a reason or algebra.

   This kind of choice appears 24 times in the 19 English sections.
2. **t33 nested shapes: add "circle, triangle, circle": R = 2r in an equilateral triangle**, so the area is ×4 and the ring = 3 inner circles. This is real exam **2019_winter_q2_08**, and nothing in our circles topic gives it directly.
3. **t32 trapezoid lesson: the trapezoid midsegment = the average of the bases** (rule, why, 2 examples; area = midsegment × height). Quadrilaterals has 43 questions, and **2020_autumn_q2_02** looks like it uses it.
4. **t51 pt51-plug-numbers-3 / pt51-summary: fix "Give different letters different numbers"** so it applies only when the choices have letters. When the choices are numbers, one easy value (often 0) for all the letters is allowed and fastest.
5. **t51 pt51-plug-numbers-2: a general list of kinds of numbers to try** for must-be-true and could-be-true questions: 0, 1, a negative, a fraction, a big number, a root, and a parity switch. Today the list lives only in t12.
6. **t15 lesson: multiple + multiple / multiple + non-multiple / non-multiple + non-multiple** (always / never / can't tell), each with a number. Divisibility has 36 exam questions.
7. **t31 isosceles lesson: the "same triangle" trap.** Equal sides give equal angles only inside one triangle. Use it as a trap choice in one question.
8. **t33 circumference lesson: one line for circles on a diameter** (the small circumferences add up to the big one, any number, any sizes). This is real **2020_autumn_q2_14**. Today it's only in t36, an older studio version, so keep it in the t36 rewrite.
9. **t51 estimation: bound any root with the nearest perfect power** (∛9 > 2, ⁵√31 < 2), extending our square-root bounds to cube, 4th and 5th roots.
10. **Small one-line tips:**
    - t16: n even factors → 2^n
    - t15: exactly one of n consecutive numbers divides by n
    - t27: circular track, nth meeting at n × the first time
    - t51: pick perfect squares or cubes when there's a root
    - t51 case 4: if a fitting plug is hard to find, simplify the given first
    - t06: divide by the top number first
    - t33: the overlap of two circles through each other's centres is a bit more than ⅓ of a circle
