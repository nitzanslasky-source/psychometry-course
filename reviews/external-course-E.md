# External course review, group E: single-question and real-exam solution videos

Reviewed 21 Oct 2026. 47 videos: 34 "question in a minute", 3 compilations (10 / 26 / 7 questions), 3 full section solutions
(Sections 11, 12, 13), 2 "selected exam questions" videos (Autumn 24, Summer 24), 5 "Who wants to be a psychometrician"
quiz shows and 1 "psychometric battle".

How I checked: I read every transcript in full. I grepped our compact course (`scratchpad/ext/course/tNN.txt`) for each idea
using several phrasings, and grepped `quant_real.md` (19 English sections, 2019-2026 spring) for how often it comes up.
Exam ids below come from that file.

Which of their videos match exams in our set:
- Section 11 = 2024_winter_q2
- Section 12 = 2026_spring_q1
- Autumn 24 = 2024_autumn
- Section 13 ("Summer 26") and Summer 24 are not in quant_real.md (Hebrew-only or newer sittings).

**The big picture.** Our course already teaches almost every method they use for these question types, and often a faster
one:
- the zig-zag rule for parallel lines
- "count who misses" for three overlapping groups
- choosing the one item left out
- the V table for workers
- the balance for averages

Most of their videos are worked single questions, not new methods. The real gaps are a handful of one-line facts, plus two
missing real-exam question types (the longest segment in a cylinder, and the staggered-arrival "bees" question).

Legend: `GAP` / `PARTIAL` (we teach part of it) / `BETTER` / `CHECK` (looks wrong or misleading) / `SAME` (they use the
same method we teach; I note whether theirs is faster or clearer).

---

## A. "Question in a minute" videos

### Psychometric Question in a Minute - 5 [WIQPfkiwx_c]
Two equal circles inside an equilateral triangle; perimeter. They use a radius to the tangent point, the fact that a line
from an outside point to the centre bisects the angle (30°), and the golden 30-60-90 triangle (×√3). This is our t33
tangent rules plus the t31 golden triangle (t33 l.282/501: tangent segments, the kite). SAME, and no faster. Nothing new.

### Psychometric Question in One Minute - 12 [E5II7PppErg]
A semicircle inscribed in an equilateral triangle with side 8. They use symmetry to put the centre at the midpoint, a
radius to the tangent point, a golden triangle, then r = 2√3 and area 6π. SAME (t33 radius to the touching point, t31
golden triangle). Nothing new.

### Psychometric Question in a Minute - 10 [o-ffFNLzphs]
Digits: aab − bba = 99, so how many numbers can aab be? They use place values: 99a − 99b = 99, so a − b = 1, which gives
many pairs. SAME (t18 l.44: "A B minus B A is nine times the bracket"; place values). Nothing new.

### Psychometric Question in a Minute - 14 [Vsk4Llv9at0]
3^(x+1) = a, so what is 3^(x−1)? They split 3^(x+1) = 3·3^x to get 3^x = a/3, then divide by 3 again: a/9.
SAME (t08/t10 power laws). Their route is one step longer than needed: 3^(x−1) = 3^(x+1) ÷ 3², which is a/9 in one step.
If our t10/t11 question of this type goes through 3^x first, show the "difference of the exponents is 2" shortcut. Nothing
new.

### Psychometric Question in a Minute - 25 [-I8vhBO_KAA]
Average 70. Gabriel (88) joins and the average becomes 70.5; how many students now? Their "channel trick" is a formula:
the new average equals the old average plus (newcomer − old average) ÷ the new count.
- SAME. Our t25 balance lesson (l.52-64) does exactly this with the newcomer measured from the new average: "Joins, the new
  average. Leaves, the old average." Our version needs no formula to memorise.
- Not better. Nothing new.

### Psychometric Question in a Minute - 26 [fbWjdkYwiQo]
Which root of factorials is an integer? They write √(99!·100!) as √((99!)²·100) = 99!·10. SAME idea as our t28 factorial
algebra (l.577-590: "ten factorial is ten times nine factorial"). We have no root-of-factorial question, but roots of
factorials do not appear in quant_real.md. SKIP.

### Psychometric Question in a Minute - 28 [lWvEeYOoEzs]
A quarter circle and a semicircle in a rectangle. They join the two centres (the distance is 2R + R = 3R) and use
Pythagoras with 4. SAME (t33: "To use the touching, we join the two centers"). Nothing new.

### Psychometric Question in a Minute - 30 [TjEBQa6RzjU]
"The largest of these numbers that divides 2^8 (or 25?) × 10!": they count how many times 10 can be formed by pairing
factors (10, 2×5, "2.5×4") and get 10³ = 1000.
- `CHECK`: the pairing as spoken is garbled.
  - If the number is 2^8 × 10!, there are only two 5s (from 5 and 10), so 10² is the largest power of 10 that divides it,
    not 10³.
  - If it is 25 × 10!, there are four 5s, so 10⁴ divides it.
  - Either way, "find the tens by eye" is the risky way. The safe rule is to count the 5s, because there are always more
    2s than 5s. Don't copy their counting.
- `GAP` (small): we have no question on the largest power of 10 that divides a product or factorial. quant_real.md has no
  such question. SKIP, or add a one-line tip in t14 ("a 10 needs a 2 and a 5, so count the 5s").

### Psychometric Question in a Minute - 36 [SR56H-hQ1Vo]
1/(x+50) = 51, so what is 1/(x+51)? Instead of solving for x, they flip both sides (x + 50 = 1/51), add 1 (52/51), and flip
back to get 51/52.
- `GAP` (one-line tip): "you may flip both sides of an equation when neither side is zero". Our t07 only flips inside a
  division (l.274). I could not find this anywhere in t06/t07.
- It saves about a minute on "find the expression, not x" questions, which is the t07 shortcut theme ("There's always a
  shortcut", l.179).
- ADD AS ONE-LINE TIP in t07 at the first question of this shape. Low exam frequency, so not a lesson item.

### Psychometric Question in a Minute - 37 [aSGy4BjM3Io]
(785² + 1) / (784² + 786²). They replace 785 with x: the bottom becomes (x−1)² + (x+1)² = 2x² + 2, so the answer is 1/2.
- `GAP` (one-line tip): "when the numbers are big and close together, call the middle one x". Our t05/t11 use shortcut
  formulas on numbers (4.2² − 3.2²) but never swap a big number for a letter.
- It is rare on our exams (no matching question in quant_real.md). ADD AS ONE-LINE TIP in t05 (shortcut formulas), or
  SKIP.

### Psychometric Question in a Minute - 41 [2955KwcuMd4]
A circle inside a square of side 4, with lines from a corner to two touching points; shaded area. They use the whole square
minus the white parts: two triangles, plus (small square minus a quarter circle), which gives 4 + π. They also warn to put
the bracket around a subtracted difference.
- SAME (t32 l.104/628, "subtract the white"; t33 radius to the touching point). Their bracket warning is good. Check that
  our t33 shaded-area questions say it when we subtract (a − b). Nothing new.

### Psychometric Question in a Minute - 42 [sFdEjN4iBhw]
√(7⁵ + 7⁵). They note that 7⁵ + 7⁵ is not 7¹⁰ ("like x + x = 2x"), so the root is √(2·7⁵) = 49√14. SAME (t10 l.66/149,
t11 l.113 "like x plus x"). Nothing new.

### Psychometric question in a minute - 8 [qXCAsi3BUR0]
2²⁴ = x^x. They rewrite 2²⁴ as (2³)⁸ = 8⁸, so x = 8. SAME (t08/t10 power of a power). Nothing new.

### Psychometric question in a minute - 13 [cXT1q7twv2g]
The area of a ring between concentric circles. You don't need each radius, only R² − r². They take half the chord (7) and
use Pythagoras: R² − r² = 49, so the area is 49π. SAME, and ours says it the same way (t33 l.653-663: "Take half the
chord, square that length, then multiply by pi"). Nothing new.

### Psychometric question in a minute - 16 [t_Gi45vwBpw]
x² − y² = 31 with x, y positive integers. They use (x+y)(x−y) = 31, and since 31 is prime, x + y = 31 and x − y = 1, so
x = 16.
- `PARTIAL`. We list factor pairs (t14 l.162/203) and teach the shortcut formula (t05/t11). I found no place that joins
  the two: "a product of two integers equals a prime, so the factors are 1 and p".
- ADD AS ONE-LINE TIP in t14 (primes): "if two positive integers multiply to a prime, one of them is 1". Exam frequency is
  low (2022_winter_q1_20 is the nearest, a parity question on n² − m²).

### Psychometric question in a minute - 17 [dqtPxOs32U0]
A square, an inner square and a circle in the corner. They use silver triangles along the diagonal: r + r√2 = 2√2, so
r = 2√2/(1+√2). SAME (t32/t33 silver triangle on the diagonal; t33 g097 has the same layout). Nothing new.

### Psychometric question in a minute - 19 [ZI6VEDlnC80]
y > |x| · y (or similar) and |x| < 1. They say:
- "If y is bigger than an absolute value of anything, y is positive."
- Then they divide by y without flipping the sign.
- "x < |x| means x is negative."
- "|x| < 7 means −7 < x < 7."

Findings:
- `PARTIAL / GAP`: our t13 l.340-349 teaches comparing a number with its own absolute value. l.23 teaches "smaller than
  its own absolute value means negative". l.327 teaches "bars smaller than a negative number? Never".
- What we lack is the general one-liner: **anything bigger than an absolute value (of any expression) is positive**. It
  decides real questions at once:
  - 2025_spring_q1_19: |a + b| < a, so a > 0.
  - 2023_spring_q1_08: |x·y| < y, so y > 0.
- ADD to the t13 absolute-value lesson (rule list at l.346-349), and use it in the first question that needs it.

### Psychometric question in a minute - 20 [Rltvm4toQQg]
AB ∥ DE with no transversal; find the angle. They extend a line until it meets the other parallel (alternate angles, then
the exterior angle of a triangle), or draw a third parallel through the bend.
- SAME, but ours is faster. t30 l.66-72 teaches both helper lines and then the zig-zag rule ("angles that point left add
  up to the angles that point right", one step).
- Their extend-the-line route takes three steps. Keep ours. Nothing new.

### Psychometric question in a minute - 23 [1EcUPET6P8Y]
√(84² + 84 + 85). They take out a common factor twice (84·85 + 85 = 85²), so the answer is 85. A second way uses last
digits: the inside ends in 5, so the root ends in 5.
- SAME for the common factor (t01/t05).
- `PARTIAL` for the last-digit check of a square root. Our t21 l.66 uses last digits only for powers.
- ADD AS ONE-LINE TIP where we teach last digits ("a square ending in 5 has a root ending in 5; a square never ends in 2,
  3, 7 or 8"). It is a quick way to rule out choices.

### Psychometric question in a minute - 24 [VPK8pUiTOpk]
A square with a "lying hourglass" (similar triangles 1:2, so areas 1:4), then a line from a vertex dividing a side 2:1, so
the areas are 2:1 too.
- SAME (t36 l.511 hourglass; t31 l.102 "same height, so the area ratio is the base ratio"). Nothing new.
- Their contrast is nice: similar triangles give the side ratio squared, a shared height gives the side ratio itself. If
  t36 doesn't already put the two side by side, it's a good one-sentence warning.

### Psychometric question in a minute - 27 [-7pLWJmK7Jw]
x/y = 6/5, so what is (x+y)/(x−y)? They set x = 1.2y, substitute, then 2.2/0.2 = 11.
- SAME topic, but their route is slower and decimal-heavy. Ours is faster: plug in x = 6, y = 5 ("plugging in numbers: a
  ratio", per the method vocabulary), which gives 11/1 at once.
- No change. If our t07/t20 question of this type shows only the algebra, add the plug-in as method 2.

### Psychometric question in a minute - 29 [rU03QxhwPts]
A circle inscribed in a triangle with sides 9, 12, 15; find AD. They use equal tangent segments: x, 9 − x and 6 + x, so
x = 3.
- SAME (t33 l.501 equal tangents).
- A faster formula exists: the tangent from A equals (perimeter ÷ 2) − the side opposite A = 18 − 15 = 3. Rare in our exam
  set (only 2019_winter_q2_08 has an inscribed circle in a triangle). SKIP the formula; the tangent-segment method is enough.

### Psychometric question in a minute - 34 [M8JyhQ0BO3o]
√(27³ − 9⁴). They write it as 3⁹ − 3⁸ = 3⁸(3 − 1), so the root is 81√2. SAME (t11 common factor with powers; "smallest
power out"). Nothing new.

### Psychometric question in a minute - 38 [KX5ZEBPzBuw]
Two touching circles and a rectangle. A chord at 90° to a tangent must be a diameter, so it is 8 and r = 4. They join the
centres: Pythagoras with 4 and 12 gives OC = 8√2, area 64√2. SAME (t33: joining centres, radius ⟂ tangent). Nothing new.

### שאלה פסיכומטרית בדקה - 4 [0uGT-7X7aS8]
√(1/√15 + √15) × ⁴√15. They use a common denominator (16/√15), then the root of a root is a fourth root, which cancels, so
the answer is 4. SAME (t09/t10/t11). Their framing, "scary at first, just do the usual steps", is good, but we already do
that. Nothing new.

### שאלה פסיכומטרית בדקה - 7 [_hEmMPxTb3I]
x/(x+1) + y/(y+1) = 1, so what is y? They multiply by the common denominator, everything cancels, xy = 1, so y = 1/x.
SAME (t06/t07). Nothing new.

### שאלה פסיכומטרית בדקה - 9 [H9Vm1Urha2M]
(2⁵⁰ − 2⁴⁹)/(2⁵¹ + 2⁴⁹). They take the smallest power out, top and bottom, which gives 1/5. SAME (t11). Nothing new.

### שאלה פסיכומטרית בדקה - 11 [V9YvEn3WNK4]
A rhombus with side x, acute angle α and area S; what is necessarily true? They use area = side × height, and the height
is less than the side (a leg is shorter than the hypotenuse), so S < x².
- SAME. t34 l.253: "In the rhombus, the side leans, so the height is shorter than the side"; t38 l.508.
- t32 l.193 teaches both area formulas. Nothing new.

### שאלה פסיכומטרית בדקה 15 [ry3CeX-HOPA]
What percent of x is x²? Method 1: plug in x = 1, which gives 100%, and keep the choice that gives 100. Method 2: the
percent formula, which gives 100x.
- `CHECK` (misleading method): plugging in x = 1 here is risky, because 1² = 1 makes many expressions equal. It only worked
  because the choices happened to differ at 1.
  - Our own rule (t22 l.378 "not zero or one, because those often make different choices look the same"; t51 l.254) is
    the right one.
  - Don't copy their x = 1. Their closing rule, "what percent is A of B: divide and times 100", is the same as ours (t23
    l.30).

### שאלה פסיכומטרית בדקה - 21 [5iP6v_CWOyM]
A quarter circle in a square with a segment of 10 and a piece of 5. They draw a radius to the touching point, then
Pythagoras: 10² + (R−5)² = R², so R = 12.5. SAME (t33). Nothing new.

### שאלה פסיכומטרית בדקה - 22 [Xqki2ZC6zrw]
A chord of 13 and a piece of 5 on the diameter, which gives the 5-12-13 triple. A radius to the touching point and
Pythagoras give R = 169/24. SAME (t31 l.356 triples; t33). Nothing new.

### שאלת פסיכומטרי בדקה - 2 [gJbY3Kt-Ix8]
x < y and y < x + z, so what is necessarily true? They add the two inequalities (same direction), so z > 0. Or they chain
them: x < y < x + z. SAME (t12 l.372-386 "Both inequalities point the same way. So we may add them"; l.138 chaining).
Nothing new.

### שאלת פסיכומטרי בדקה - 3 [fE76nROgB-s]
|x + y| = |x − y| with x ≠ y. Two cases (the insides are equal or opposite), so y = 0 or x = 0. SAME (t13 l.183 "two
cases"). Nothing new.

---

## B. Compilation videos

### 10 Psychometric Questions to Strengthen Quantitative Reasoning Skills [Zjxxh-HROAo]
Real-exam questions (percent chains, bees, cannons/LCM, fraction of the remainder, ratio change, passwords, even sum,
"x km in t hours").
- Percent chains: they plug in 100, and say to switch to algebra when the choices include "cannot be determined". SAME
  (t23 l.42; t51). Nothing new.
- **Bees** (this is real exam 2023_spring_q2_07: a bee arrives each minute, each sucks 1 mg a minute, 10 mg in total; how
  much did the first bee suck?). They list it minute by minute: 1, then 1+2, then 1+2+3, then 4 more, so the first bee
  sucked 4.
  - `PARTIAL / GAP`: our t21 teaches "step by step: write the items one at a time" (l.33, l.257), so the method is there.
    But no question in the course has staggered arrivals, a common rate and a fixed total.
  - It is a real exam item, and weak students freeze on it. ADD a question (new numbers) in t26 (work and rates) or t21,
    solved with a small minute-by-minute table.
- Cannons (every 2, 3 and 5 seconds): LCM. SAME (t21 l.277 buses; t14 LCM). Nothing new.
- Grapes (2/3, then 3/4 of the rest): SAME (t22/t03 fraction of the remainder). Nothing new.
- Ratio of salaries: multiplying or dividing both keeps the ratio, adding changes it. SAME/PARTIAL (t22 l.184 "only the
  ratio changes", l.334). Nothing new worth adding.
- Passwords of length 3 or 6 from two symbols: 2³ + 2⁶ (OR means add). SAME (t28). Nothing new.
- Choose 4 of 1-5 with an even sum: they list combinations. Ours is faster. Choosing 4 of 5 is choosing the 1 to leave out
  (t28 l.192). The total 15 is odd, so the one left out must be odd, which gives 3. Keep ours.
- "x km in t hours, so y km takes?": their "double D" rule of three (cross-multiply, divide by the third). SAME (t22 l.91-104
  "triangle value" / cross-multiplying). Nothing new.

### 26 שאלות שישפרו את היכולות הפסיכומטריות שלכם [5x2wnqu1T88]
26 short "know this rule" questions. Most are SAME. The new or partial ones:
- **Regular polygon, four neighbouring corners: the two diagonals between them cross at an angle equal to the polygon's
  interior angle** (hexagon: 120°, so α = 60°).
  - `GAP`. It is not in t34. We have "diagonals from one corner cut the angle into equal parts" (l.173/377), but not this.
  - Why it is true: with corners A, B, C, D, the diagonals AC and BD meet at P. Triangles ABC and BCD are isosceles with
    base angles (180° − θ)/2, so in triangle BPC the angle at P is 180° − (180° − θ) = θ.
  - It fits real polygon-and-diagonals items (2026_spring_q2_19 regular 9-gon with four diagonals; 2023_spring_q2_03). ADD
    as a short trick (with the why) in the t34 diagonals lesson or the first question that uses it.
- **A trapezoid inscribed in a circle is isosceles** (and every isosceles trapezoid can be inscribed).
  - `PARTIAL`: t33 l.450 teaches that opposite angles of an inscribed quadrilateral add up to 180°, and t32 l.494 teaches
    the isosceles trapezoid's opposite angles. But we never draw the conclusion.
  - 2024_autumn_q1_13 ("it is not possible that a diagonal of the ___ inscribed in the circle is a diameter", with an
    isosceles trapezoid among the choices) is the kind of question it helps with. ADD AS ONE-LINE TIP in t33 after the
    inscribed-quadrilateral rule.
- **A circle inside a quadrilateral: the two pairs of opposite sides have equal sums** (4 + 8 = 3 + 9). `GAP`, but there is
  no question like it in quant_real.md. SKIP (or one line in t33 for strong students).
- Average of evenly spaced numbers = the middle (or the mean of the two middles). SAME (t25 l.17-22).
- |a − b| / |b − a| = 1. SAME (t13 l.241).
- 33.3% of 66 by swapping: SAME (t23 l.178/330).
- Even × integer = even. SAME (t01 l.602, t16).
- An isosceles triangle whose altitude is also the median, so it also bisects the angle. SAME (t31 l.45).
- Cube with volume x³: surface 6x². SAME (t35).
- Regular pentagon + octagon sharing a side: 360 − 108 − 135. SAME (t34 l.289).
- Choose 2 of 5 = 5·4/2!. SAME (t28 l.91-93).
- x³ + x² = 0 with x ≠ 0: take out x², so x = −1. SAME (t05/t07).
- Shortcut formulas on top and bottom. SAME (t05/t11).
- Dividing fractions with "outer × outer over inner × inner" (their "ear" method). Ours (t02 l.146 "keep, change, flip")
  is fine. Not better. SKIP.
- Rectangle with its diagonals: four equal areas. SAME (t32 l.183/612).
- Multiplying an inequality by a known negative flips it. SAME (t12).
- 4·4^x = 4^(x+1). SAME (t11 l.113).
- (2x + 4y)/2 = x + 2y. SAME.

### 7 Challenging Quantitative Questions from the Channel's New Practice Book [B7Dr3Ji9QLY]
Their own practice-book items.
- Parallel lines with two bends: a parallel through each bend. SAME; our zig-zag rule is faster (t30 l.99-105).
- Letters as digits, "MY = P·U, so UMYU ÷ U": they plug in, then do long division. SAME/SKIP (t18). It is their own item,
  and long division of letter numbers is not on our exams.
- (28·101 − 28)/(27·101 + 73): they rewrite 73 as 100 − 27 and take out common factors, which gives 1. SAME (t01/t05
  common factor). Nothing new.
- **"Moki breaks in in 10 min alone. After 4 min Shuki joins and they finish in 3 more min. How long would Shuki take
  alone?"**
  - Their insight: Moki alone needed 6 more minutes, but with help it took 3. The helper halved the remaining time, so the
    helper works at the same rate: 10 min.
  - `GAP` (one-line tip). Our t26 has the forward fact ("same work in half the time", l.76) and the stage method (l.109-120),
    but not the reverse reading "the time was halved, so it is an equal partner".
  - Real exam: no direct match in quant_real.md. ADD AS ONE-LINE TIP in a t26 join-in-the-middle question, after the stage
    method.
- A cube in a 3D coordinate system (x, y, z). `GAP`, but there are 0 such items in quant_real.md, and they admit they have
  never seen one on the exam. SKIP.
- Eyal's speeds (+20%, −28 km/h): a speed × time table, so 3.6x = 5x − 140. SAME (t27/t23). Nothing new.
- √(7!) = 12√35 by grouping squares (4 and 36). SAME idea (t09/t11, t28 factorials). SKIP.

---

## C. Full section solutions

### פתרון פרק כמותי 11 [NxPwYAUFQRY] (= 2024_winter_q2)
- Parallelogram area with a 3-4-5 height; glasses/long-hair two-way table; square perimeter farthest point; pipes 1/4 − 1/8;
  isolating x in an inequality; factoring 2b(a − 5) = 2(a − 5) with b ≠ 1, so a = 5. All SAME (t31, t24, t26, t12, t07).
- Family ages: four children equally spaced from 9 to 15, so 9, 11, 13, 15. SAME (t25/t21).
- Charts:
  - "Largest ratio cars/buses": they don't divide. They look for the year whose top is bigger **and** bottom is smaller
    than the others (dominance).
  - `PARTIAL / GAP`: our t52 compares quotients by dividing and estimating (l.125-130). t03 l.99/209 compares a fraction
    with 1. I found no statement of the dominance rule ("bigger top and smaller bottom, so a bigger fraction; no need to
    calculate"), or of what to do when both grow.
  - Charts are the biggest exam group (163 items), and "which is the largest ratio / per-unit value" is common. ADD AS
    ONE-LINE TIP in t52 (ch52-tables or the practice intro), with a two-line example.
- Charts min/max ("y can be anywhere from 0 to 26,000"). SAME (t52, the extremes). Average of 8! and 10! = 8!·91/2 (take
  out 8!). SAME (t28 l.577-590). Pyramid surface; x divisible by 6, so x² is divisible by 4 (x = 2n). SAME (t16 l.53/107).
- Inverse operation (undo +1, then undo squaring). SAME (t19 l.20-22).
- Kiosk: 21 shekels with at least one of each sweet. Take one of each first, then count the ways to fill the rest. SAME as
  "fixed first, then count" in t28/t21 (listing). Nothing new.

### Solving Quantitative Section 12 [OQflXw0e_B8] (= 2026_spring_q1)
- "Even number, so I call it 2x." SAME (t16 l.107/227 "write b as two times an integer k").
- Averages, so turn them into sums at once (x + y + z > 24). SAME (t25 l.42).
- Sector areas are in the ratio of their angles. SAME (t33 l.56).
- 2⁴ = 4² is the only exception, so the answer is "cannot be determined". SAME (t08 l.72, t11 l.92).
- Workers: "3 workers in 20 min, so 2 workers in 30 min". SAME (t26 team/time opposite ways, l.76-87).
- Trapezoid: triangles ABC and ABD share a height. SAME (t31/t32 same base and height).
- **Efrat, Beni, Gilad (2026_spring_q1_14), three "give half" steps:**
  - They start with a number with enough 2s (16x) so every half stays whole.
  - `PARTIAL`. t22 l.236 teaches choosing the amount by the denominator ("choose eight, because…"), but only for one
    fraction.
  - ADD AS ONE-LINE TIP: "for repeated halving, start with 8 or 16 (one 2 for each halving)". Low cost.
- Smallest positive number whose 3% is an integer: 100/3. SAME (t23).
- Similar triangles AE/2 = 2/x. SAME (t36).
- 1/x between −½ and ½. Plugging in the answers. SAME (t12/t51).
- Map scale with the eye's 0.1 mm limit (2026_spring_q1_18). SAME method (t36 l.728 map scale), but our map-scale lesson
  has no "smallest visible distance" story. Optional new question. Low priority.
- Digit-sum operation counterexample (79 vs 80). SAME (t19 counterexamples).
- Volume ratio 2, so the side ratio is ∛2 and the area ratio is (∛2)². SAME (t36 l.574-608).
- Their speed tips ("I see even, I write 2x"; "average, so I multiply at once") are exactly our habits. Nothing new.

### Quantitative Section 13 Solution [E2k8OUeJgJI] ("Summer 26", not in our exam file)
- Negative ÷ negative; windows per floor (divide by the thing after "per"); isosceles trapezoid with a golden-triangle
  height; consecutive numbers and divisibility (try starting points). All SAME.
- Probability of the same colour: the first ball doesn't matter, then 4/9. SAME (t29 l.178-187 "First spinner doesn't
  matter").
- Mushrooms: 75 ÷ (75 + 50) h = 36 min. SAME (t26 add rates).
- Charts (horses): SAME (t52).
- √(9!·8!/3) style: split 9! = 9·8!. SAME (t28).
- Children dividing 18 books: divisors of 18 between 2 and 19. SAME (t14/t15).
- A right triangle in a circle: the hypotenuse is a diameter. SAME (t33 l.442).
- Parallelogram height from a silver triangle (÷√2). SAME (t31/t32).
- **Halving walk (½ km, ¼, ⅛, … until day 10): what he walks on the last day equals what is still left.**
  - `GAP` (one-line tip): not in t21 (patterns). It is quick and memorable, and also useful for "a tank loses half each
    hour" questions.
  - Exam frequency: not in our 19 sections, but they say it repeated an older item. ADD AS ONE-LINE TIP in t21's
    step-by-step pattern lesson. Low priority.
- abc − cba = 99(c − a): place values. SAME (t18 l.44).
- **Equilateral triangle with two overlapping pieces (DF and EG parallel to the sides): FG = (5/6)a + (4/5)a − a.** The
  overlap is the two pieces minus the whole.
  - `GAP` (one-line tip): our t24 overlap rule ("counted twice", l.88/113) is taught for people only. Saying once that it
    works for lengths on a line too ("two overlapping pieces: overlap = piece + piece − whole") links two topics.
  - ADD AS ONE-LINE TIP in t24 (or t31 if a figure question uses it).

---

## D. "Selected questions" videos

### שאלות נבחרות מפסיכומטרי סתיו 24 [L2EdGF4ikZ8] (= 2024_autumn)
- |x − y| − |y − x| = 0 (2024_autumn_q1_02). SAME (t13 l.241).
- Pumps (2024_autumn_q1_05): their single formula, work ÷ (time × people) equal on both sides.
  - SAME (t26 V table for teams, l.214/339). Their one-equation formula is compact, but our V table is the course's
    method, with its own visuals. Don't switch.
- b³ − 1 = (b − 1)(b² + b + 1) (difference of cubes).
  - `GAP`: we never teach it. They themselves say plugging in is the normal way and not to memorise it.
  - SKIP, or at most a one-line "for strong students" note in t05 (plugging in solves it).
- ab < 2(a + b), so b > 8a, so a = 1, b = 9: place values plus an inequality. SAME (t18). Nothing new.
- $(n) = n ones (2024_autumn_q1_18): $(n+1) = 10·$(n) + 1. Plug in n = 2. SAME (t19 plugging in numbers). Nothing new.
- **Three people at 4 lectures, the minimum in all three** (their own lecture example):
  - They take the minimum overlap of two (3 + 3 − 4 = 2), then place the third person on the other two lectures, so 0.
  - SAME result. Our t24 l.300-303 "count who misses each group" is faster: 1 + 1 + 2 = 4 misses, 4 − 4 = 0. Keep ours.
- Squares with x, y and a bold line equal to the perimeter (2024_autumn_q1_20). SAME (t31 l.125-126 bold-line question
  type). Nothing new.
- **AC from the figure (2024_autumn_q2_02):**
  - Their insight: extend the figure into one big right triangle, 9-12-15, so the answer is 15. The long way is the
    hourglass similarity, then 3-4-5 and 6-8-10.
  - `PARTIAL`: we teach both triples and the hourglass. "Complete the figure to a bigger shape you know" appears as
    complete-the-rectangle tricks, but I found no "complete it to one big triangle" example.
  - Worth an "insight" method in one t31/t36 question. ADD AS a method 2 in an existing hourglass question, if one fits.
- x prime > 2: x^(x+1)/2^x. The top is bigger (bigger base and bigger exponent), and odd ÷ even is never an integer.
  SAME (t16 l.42 "Odd over even cannot give an integer"). Nothing new.
- x ≤ y ≤ z ≤ x, so all are equal. SAME (t12 chaining). Nothing new.
- Shaded area of identical squares: the whole minus the white. SAME (t32 l.104).
- **c divisible by a and by b, so is it divisible by ab? (2024_autumn_q2_13): only if a and b share no factor**
  (counterexample 36: divisible by 4 and 6, not by 24).
  - SAME (t15 l.86/212: "For a combined divisor, do its factors share anything greater than one?"; t14 LCM l.85-108).
  - Their wording ("coprime" with 12 / 3 and 6 / 18 counterexamples) is similar to ours. Nothing new.
- Probability of different colours (2024_autumn_q2_14): the first doesn't matter, then 2/3. SAME (t29).
- **Cylinder with height 10 and radius 3: the maximum AB if AB is a whole number (2024_autumn_q2_15).**
  - The longest segment goes from a point on the top rim to the diametrically opposite point on the bottom rim, so
    AB² = 6² + 10² = 136. The largest whole number with square ≤ 136 is 11.
  - `GAP`: t35 has no "longest segment inside a cylinder" (or "the diagonal of a cylinder's cross-section") idea and no
    question like it. t35 is the older studio version.
  - It is a real exam question. ADD a t35 question (new numbers) when t35 is rewritten: "slice through the axis, which
    gives a rectangle 2r by h, and the longest segment is its diagonal".
- English sentence completion: not quant. Skip.

### שאלות נבחרות מפסיכומטרי קיץ 24 [v8XbeDIBO7I] (Summer 24, not in our exam file)
- Verbal logic ("only… / contrapositive"): not quant. Skip.
- An isosceles triangle with medians: each median halves the area, so ab/8. SAME (t31 l.102 same base and height).
- a²b² divisible by 6: plug in (1, 6), then swap to (6, 1) because the choices are not symmetric.
  - SAME (t15/t51 plugging in numbers). Their "swap the values when the expression is not symmetric" is a good habit. Our
    t15 plug-in questions probably do this already. Nothing new.
- **Arazi family: sum of boys' ages = sum of girls' ages. In 2 years the boys' sum is 6 more, so there are 3 more boys.**
  - SAME idea (each person adds 2 years, t25/t22). It is a nice "understanding" question: the difference grows by
    2 × (boys − girls).
  - Check that our t22/t25 has an "each one gets older by the same amount" sum question. I found a gap-stays example
    (t22 l.184) but not a sum-of-ages-of-groups one. Optional question. Low priority.
- x < 0: compare a, b, c. Plugging in −1, then by understanding (the sign of c, then moving terms). SAME (t12/t20).
- **x = y + z, y = x + z, z = x + y, so all are 0.** Add all three: x + y + z = 2(x + y + z), so the sum is 0, so x = −x =
  0.
  - `GAP` (small; nothing in t07 l.179 "three equations"). It is not in our exam file. SKIP, or a one-line tip.
- **x = ab = cde with distinct factors > 1**: use prime factorisation, and pick a number with a repeated prime (60).
  SAME/PARTIAL (t14 prime factorisation). Nothing to add.
- **Parallelogram: perimeter p > sum of diagonals l** (the triangle inequality on two triangles).
  - `PARTIAL`: t31/t20 teach the triangle inequality, but never apply it to a parallelogram's diagonals.
  - Not in our exam file. ADD AS ONE-LINE TIP in t32 only if a question fits, otherwise SKIP.
- Three candidates, two jobs: 3·2·1. SAME (t28). Leg 66 and leg 88: 6-8-10 × 11. SAME (t31 triples).
- Regular hexagon inscribed in a rectangle: golden triangles at the sides, area 2√3x² (cf. 2025_spring_q1_18). SAME (t34
  l.120-159 hexagon diagonals a√3 and 2a). Nothing new.
- 12.5% = 1/8, so x is divisible by 8, so x is even. SAME (t23 l.381-395).
- Grey area = ¾ of a circle + a square (instead of chopping pieces). SAME (t33 sectors / t32 subtract the white).
- Cube: V = a³ vs F = 6a². Equal only at a = 6, so "cannot be determined". SAME (t35 cube facts).
- a/b² = x, so a²/b = x·a (algebra instead of plugging in). SAME (t05/t20).
- $(x) = x√x applied twice: 87^(9/4). SAME (t19 inner first l.40/257; t11 exponents).
- Turtle x km/h, ant x² km/h, 1 hour apart: a speed × time table with letters, so x = t/(t − 1) > 1. SAME (t27 table).
  Their message, "don't fear letters, do the same as with numbers", is something we already say.

---

## E. Quiz shows and the battle (short rapid questions)

### Who wants to be a psychometrician - Eldar, 16, Kiryat Ata [KAIxw8C0ZeI]
- Order of operations, ∛27, quarter-circle area, 3^(a+1)/3^a, box surface 2(ab + ac + bc), x/√x = √x, percent change
  500 → 600 vs 50 → 40, golden/silver triangle areas. All SAME.
- Workers' formula "work ÷ (time × people)". SAME as our V table (t26).
- Regular hexagon: split it into a rectangle and two triangles; a rectangle's diagonals give four equal parts. SAME (t32
  l.183; t34 l.228 hexagon in sixths). Nothing new.

### Who Wants to Be a Psychometrician - Aviel and Itay, 16, Rishon LeZion [cCaupKMjxGQ]
- Exponents, 1 is not prime, α = β substitution, aa + aa = 1b8 style digits (place values or trial). SAME.
- "Pie chart: 72° = a fifth = 20%" (memorise 45° = ⅛ and 72° = ⅕).
  - `PARTIAL`: t52 has a circle chart, but I found no "angle to percent" anchors (72°, 45°, 36°).
  - Pie-chart angles are rare in our exam file. ADD AS ONE-LINE TIP in t33 or t52 only if a question converts angles to
    percents.
- "Bronze triangle" (isosceles with a 120° apex, legs x): area = x²√3/4, the same as an equilateral triangle with side x.
  Base x√3. SAME (t31 l.222 "the thirty, thirty, a hundred twenty triangle with legs a").
- Choose x − 2 of x people = choose the 2 left out = x(x − 1)/2. SAME (t28 l.192/472).

### Who Wants to be a Psychometrician - Adir, 19, Bat Yam [gbfFnLhP50Y]
- −(−a)... signs; 12/√3: "divide the numbers, then put the root back" (4√3).
  - SAME (t11 l.175 "ignore the root, six over three is two, put the root back"). Nothing new.
- 2% of 2 = 0.04; (29² − 26²)/55 by the shortcut formula; diameter ÷ circumference = 1/π, so 100/π %. SAME (t23, t05, t33).
- Arranging the letters of a 4-letter word in alphabetical order: 1/24. SAME (t29).
- 5^x + x! = 131: plug in (x = 3). SAME (t51 plugging in the answers).
- Circles inscribed in all 6 faces of a cube vs the surface: π/4. SAME (t35 + t33 square/circle ratio). Nothing new.

### Who Wants to Be a Psychometrician - Yahli, 20, Jerusalem [DNRCBChX9to]
- 12/√3 under one root; 1/(2/3) + ½; 15 of 75 = ⅕ = 20%; three dice all the same: 1 · ⅙ · ⅙ ("the first doesn't
  matter"). SAME (t09/t11, t02, t23, t29).
- Diggers: "2 holes in 2 h = 1 hole an hour", so together ½ h. SAME (t26).
- Cube facts list: V = a³, lateral area 4a², surface 6a², face diagonal a√2, body diagonal a√3. "If one is given, set it
  equal and solve."
  - SAME (t35 l.561 diagonals; t35 "Cube and Box Facts" lesson).
  - Lateral surface area is taught in t35 (l.312-362, prism and cylinder). The cube's 4a² follows from it. Nothing new.
- They correctly say plugging in only works with numbers in the choices ("there are no four choices here, so plugging
  won't help"). SAME (t51).
- "Open set" definition question (the smallest element). SAME (t19/t20 understanding a definition).

### Who wants to be a psychometrician - Roni, 17.5, Rehovot [zMkUYwAgtEQ]
- 31% of 2000; −5²/(...) with the trap that the power is only on the 5. SAME (t08 sign trap).
- Octagon angle sum − regular pentagon angle (1080 − 108 = 972), and "memorise the angle sums and the regular angles of
  the 5-, 6- and 8-gons".
  - SAME (t34 l.39 "Which sums do we know by heart?…"). Nothing new.
- Operations $ and #; choose 2 specific people of 8: 2/8 · 1/7 = 1/28; infinitely many perpendicular lines; 8^(...) to base
  2. SAME (t19, t29, t37, t11).

### קרב פסיכומטרי - 1 [wdaIE3j8ZpA]
- Mostly verbal. Quant items: isolating x; a triangle area 2·3/2; remainders.
- "**In remainder questions, plug in the remainder itself as the number**" (dividing by 7 with remainder 5: take x = 5).
  - `PARTIAL`: our t15 does this once (l.185 "a b that leaves five… so five itself") but never says it as a rule.
  - Remainders are a big exam group (36 divisibility/remainder items). ADD AS ONE-LINE TIP in the t15 remainder lesson,
    including the why: the remainder itself is the smallest number that leaves it, since it fits 0 times. Careful: it needs
    remainder > 0 and the number may need to be positive or larger than some bound.
- An isosceles triangle's altitude is shorter than the leg (a leg is shorter than the hypotenuse). SAME (t34 l.253 logic).
- A regular hexagon's long diagonal = 2 sides. SAME (t34 l.159).
- A 40° inscribed angle gives a central angle of 80°, so 80/360 = 2/9 of the circle. SAME (t33). Nothing new.

---

## Counts

- Videos reviewed: **47**
- `GAP` (incl. small gaps; PARTIAL counted separately): **12**. Angle between neighbouring diagonals; longest segment in
  a cylinder; flipping both sides of an equation; big number → x; tangential quadrilateral sums; 3D coordinates;
  difference of cubes; halving walk; overlap rule for lengths; helper halves the time → same rate; x = y + z system;
  power of 10 dividing a factorial.
- `PARTIAL`: **11**. Bigger than an absolute value → positive; bees (staggered arrivals); fraction dominance in charts;
  inscribed trapezoid is isosceles; remainder itself as the plug-in; product = prime → 1 × p; last digit of a square root;
  repeated halving → start with 8/16; complete to one big triangle; parallelogram perimeter > diagonals; pie-chart angle
  anchors.
- `BETTER`: **0**. Wherever both courses teach the same question type, our route was the same or faster: zig-zag vs extend
  the line, "count who misses" vs a step-by-step minimum overlap, "leave one out" vs listing, plugging in a ratio vs
  decimals, the balance vs a joiner formula, the V table vs a single proportion.
- `CHECK`: **2**. QiaM 30 (counting tens in a factorial product: count the 5s instead); QiaM 15 (plugging in x = 1 into x²
  vs x).

## Top recommendations (most valuable first)

1. **t13 lesson: add "anything bigger than an absolute value is positive"**, next to the existing "compare a number with
   its own absolute value" rules (l.340-349). It decides real items at once (2025_spring_q1_19 |a+b| < a; 2023_spring_q1_08
   |xy| < y). Cost: 2-3 sentences plus one example.
2. **t15: say "plug in the remainder itself" as a rule** (remainder r when dividing by d, so the easiest number is r).
   Explain why and give the conditions. It is already used once (l.185) but never named. Remainders are a large exam
   group (36 items).
3. **t35 (when rewritten): add the longest segment in a cylinder** (cut through the axis, which gives a 2r × h rectangle,
   and take its diagonal), as a question with new numbers. Real exam: 2024_autumn_q2_15.
4. **t52: add the fraction-dominance tip** ("a bigger top and a smaller bottom give a bigger fraction, no division
   needed"). Charts are the biggest exam group (163), and "largest ratio / per unit" questions are common.
5. **t34: add the "neighbouring diagonals cross at the interior angle" trick, with its 2-line why** (two isosceles corner
   triangles). Fits regular-polygon-with-diagonals items (2026_spring_q2_19, 2023_spring_q2_03).
6. **t26 (or t21): add a staggered-arrival question like the bees** (one joins each minute, a fixed total), solved with a
   minute-by-minute table. Real exam 2023_spring_q2_07; our step-by-step method covers it, but no question shows it.
7. **t33: one line, "a trapezoid inscribed in a circle is isosceles"**, right after the inscribed-quadrilateral rule
   (opposite angles 180°). Helps on "which shape can / can't be inscribed" items (2024_autumn_q1_13).
8. **t07: one-line tip "you may flip both sides of an equation"** (1/(x+50) = 51, so x + 50 = 1/51), in the
   expression-not-x shortcut questions.
9. **t24: one line saying the overlap rule works for lengths too** (overlap = piece + piece − whole), and **t26: one line
   reading "the remaining time halved when a helper joined, so the helper is an equal partner"**.
10. **Small one-line tips:** "for repeated halving, start with 8 or 16" (t22, real item 2026_spring_q1_14), the last digit
    of a square root (t21, where last digits are taught), and "product of two positive integers = a prime, so the factors
    are 1 and p" (t14).

Not recommended (SKIP): 3D coordinates, difference of cubes, the tangential-quadrilateral sum rule, the x = y + z system,
the "ear" fraction division, and switching from our V table, balance or zig-zag to their formulas. Ours are equal or
faster, and they are the course's named methods with their own visuals.
