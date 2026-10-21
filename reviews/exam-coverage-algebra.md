# Exam coverage audit, group X = algebra (21 Oct 2026, read-only)

Scope: every real question in `real_exam/quant_real.md` for divisibility_remainders (36), inequalities_absolute (35), equations (33), algebraic_expressions (32), exponents_roots (27), number_properties (27), generality (20), defined_operations (16), number_line (2) and trial_and_error (2). That is **230 questions, all read**.
Course checked: every lesson's spoken text in t04–t21 and t51 (read in full), the video lists of t01–t21 and t51, every question stem in q01–q21, plus targeted reads of solution videos. Where a type is taught only in t22 (word problems, outside this group), I say so.
Ratings: **C** = explained clearly (why + worked example + conditions), **M** = mentioned only, **X** = missing. Practice: **P** = practised (2+ questions, at least one with a video), **T** = thin, **N** = none. [V] = has a solution video, [p] = written only.
Recording status comes from `video_status.py --list record`. In t01–t21 and t51, only these are still to record: **all of t51**, `operation-patterns`, `solve-q-549`, `solve-q-r26-t16-04` and `wp-001`. Every other target video below is already recorded or in production, so any addition there means a new video or a re-record.

**Totals: 67 question types. Explained: 55 C / 8 M / 4 X. Practice: 52 P / 10 T / 5 N.**

---

## Divisibility & remainders (36)

| type | exam count + ids | explained where (rating) | practised where (rating) | flag |
|---|---|---|---|---|
| D1 Divisible by both a and b → LCM, not a·b; counting common multiples; two cycles meeting | 6: 2020_autumn_q1_12, 2024_autumn_q2_13, 2022_winter_q1_02 (+2021_autumn_q1_20, 2024_spring_q1_06, 2025_winter_q2_10) | t15 r26-t15-remainder-tools (4 and 6 → 12k, "not 24"); t14 solve-q-390 (LCM, 3 methods); t14 summary; t21 solve-wp21-g025 (meeting cycles, "jump by the bigger") **C** | q-390, q-430, wp21-g025 [V]; q-422, r26-t15-06, wp21-p08, t14-4-2 [p] **P** | — |
| D2 Largest number that surely divides a sum / product / power | 8: 2025_autumn_q2_18, 2025_spring_q2_20, 2021_autumn_q2_14 (+2021_spring_q2_19, 2024_winter_q1_04, 2024_winter_q2_18, 2022_autumn_q2_05, 2019_spring_q2_17) | solve-q-r26-t15-15 (6k+9m = 3(2k+3m), trap of equal values); t14 primes-3 (check the prime ingredients); t16 consecutive-products; t15 summary ("write it as divisor × whole number") **C** | q-390, q-394, q-395, q-432, r26-t15-15 [V]; q-442, q-449, q-451, q-455, r26-t14-15 [p] **P** | 2019_spring_q2_17 (x>y, both multiples of z ⇒ x ≥ 2z) has no direct match; plugging in numbers solves it |
| D3 Story relation forces a multiple (a = 3b ⇒ a+b = 4b; 25% more ⇒ 9k; K, K+9, K+11 ⇒ 3K+20) | 3: 2021_autumn_q1_17, 2019_spring_q1_12, 2024_autumn_q2_12 | t15 divisibility-2 (end: "a quarter of a group"); solve-q-431, q-434; t22 g035/g047 (total ÷ sum of the ratio parts) **C** | q-423, q-427, q-431, q-434 [V]; q-439, q-451 [p] **P** | — |
| D4 Remainder stories: dealing in turns, which season/group, nested sharing, remainder of a sum | 4: 2023_spring_q1_07, 2023_winter_q2_07, 2025_spring_q2_02, 2020_winter_q1_07 | t21 wp-022 (cycles; remainder 0 = last one); t15 divisibility-3 (the shop); t15 summary (work with remainders) **C** | wp21-g024, q-r26-t15-01 [V]; r26-t21-10, q-438, q-452 [p] **P** | "item n is in group ⌈n/size⌉" (episode 120, 13 per season → season 10) is never said aloud |
| D5 Two remainder conditions together (odd and r2 by 3 → r? by 6; r1 by 2, 3 and 4) | 2: 2022_winter_q2_13, 2023_winter_q1_01 | remainder-tools tool 1 (take the remainder away) + LCM; divisibility-4 (changing the divisor) **C** | q-424 [V]; q-437, q-441, q-453 [p] **P** | — |
| D6 Divisors: count, list, common divisor, "is it an integer" from the prime factorization | 6: 2025_autumn_q2_07, 2023_winter_q2_08, 2026_spring_q2_14 (+2023_spring_q2_06, 2023_autumn_q2_16, 2021_spring_q1_14) | t14 prime-tools ((exponent+1) product, with why); primes-2/3; summary (odd count ⇔ square; 3 divisors = p²) **C** | q-388, q-389, q-397, q-402 [V]; q-403, q-411, q-417, q-445 [p] **P** | "Even divisors only" (40 → 5) is not shown anywhere |
| D7 Numbers in a row / fixed gaps and divisibility (a, a+2, a+4; (M−1)(M−2); squares that are multiples of 3) | 3: 2019_winter_q1_16, 2025_winter_q1_14, 2024_spring_q2_07 | t16 consecutive-products, r26-t16-consecutive-sums; solve-q-432 ("every third integer"); t14 more-tools (squares have even exponents) **C** | q-432, q-464, r26-t16-03, r26-t16-04 [V]; r26-t16-11 [p] **P** | solve-q-r26-t16-04 is still to record |
| D9 Non-integers with a property (numbers between 10 and 12 whose product with 3 is an integer) | 1: 2023_winter_q1_20 | **X** | **N** | A weak student answers "1" (only 11) |
| D10 Fraction of what is left | 1: 2022_winter_q1_04 | t02 solve-q-r26-t02-05 **C** | r26-t02-05 [V]; r26-t02-08, -09 [p] **P** | — |
| (digit puzzles 2026_spring_q2_12, 2025_winter_q1_06) | 2 | see N1 | | |

## Inequalities & absolute value (35)

| type | exam count + ids | explained where (rating) | practised where (rating) | flag |
|---|---|---|---|---|
| I1 Solve a linear inequality / exact range, also after putting in a given equation | 6: 2022_autumn_q2_12, 2019_spring_q1_06, 2024_winter_q2_05 (+2020_spring_q1_18, 2025_winter_q1_01, 2021_autumn_q1_16) | t12 inequalities (same moves, flip, "ranges in two moves", test a number for "most precise"); substitution: t12 summary line + solve-q-329 **C** | q-322, q-323, q-325, q-329, q-333, r26-t12-13 [V]; q-338, q-344, q-351 [p] **P** | Substitution is taught only inside q-329 |
| I2 Combining inequalities: add, difference of ranges, chains, transitivity | 7: 2020_winter_q2_14, 2025_spring_q2_06, 2024_spring_q1_03 (+2020_spring_q2_14, 2022_autumn_q1_06, 2024_autumn_q2_05, 2021_spring_q1_15) | taught only in questions: r26-t12-03 (adding is safe), r26-t12-04 (biggest − smallest), q-336 (four corners), q-327 (chain). The r26-t12-combining lesson only does x² **C (in questions)** | r26-t12-03, -04, q-327, q-334, q-336 [V]; r26-t12-05, -11, q-343 [p] **P** | R37: a core method, but the lesson only announces it ("one move is safe… the questions show which") |
| I3 Signs of products and fractions (incl. "fraction < 0", (a+b)/a between 0 and 1) | 5: 2023_autumn_q1_01, 2025_autumn_q1_16, 2020_autumn_q1_13 (+2020_autumn_q2_19, 2023_winter_q2_10) | t16 whole-numbers (count the minuses, with why); t12 summary + r26-t12-02, q-332 ("mark the zeros, test each part") **C** | r26-t12-02, q-332, q-465, q-466 [V]; q-354, q-476, q-485 [p] **P** | "Mark the zeros" is only in the summary and questions; t16 (day 33) comes after t12 (day 20), so t12 relies on the t01 sign rules |
| I4 From a range of 1/x back to x, across zero (−½ < 1/x < ½) | 1: 2026_spring_q1_17 | r26-t12-signs: 5 slide lines ("same sign flip, different no flip"), no example, no why **M** | r26-t17-03 [V], r26-t17-09, t12-3-5 [p]: all go from x to 1/x, none split by sign **T** | Solvable with the t12 test-a-number method (checked) |
| I5 Which root lies in a range | 1: 2023_autumn_q1_07 | t09 traps ("between two perfect squares"), pt51-estimation **C** | r26-t09-02 [V]; q-246 [p] **P** | — |
| I6 Absolute value of a letter by its sign; \|x\|/x; a+\|a\|; \|x\|−x = 6 | 5: 2025_autumn_q2_01, 2024_winter_q1_05, 2020_spring_q1_02 (+2024_autumn_q1_02, 2019_spring_q2_14) | t13 absolute-value parts 1–2, r26-t13-tools (order inside the bars) **C** | q-128, q-362 [V]; q-378, t13-3-6, expression-extra-06 [p] **P** | — |
| I7 Absolute value of a sum and sign deductions (\|x+y\| < \|x−y\| ⇒ xy < 0; xy < \|xy\| < y; t² = w²) | 7: 2021_autumn_q2_15, 2024_spring_q2_18, 2023_spring_q1_08 (+2025_spring_q1_19, 2019_winter_q2_17, 2026_spring_q2_10, 2024_spring_q2_04) | t13 absolute-value-2 (rule 3 with why; compare a number with its absolute value); t13 summary; t07 summary (equal squares: equal or opposite) **C** | r26-t13-13, q-358, q-365, q-368 [V]; q-371, q-374, q-382, q-384, q-385, q-209 [p] **P** | — |
| I8 Values of \|x−y\| from \|x\| and \|y\| | 1: 2020_autumn_q2_13 | solve-q-r26-t13-13 **C** | r26-t13-13 [V] only **T** | — |
| I9 Max/min of an absolute sum or a distance chain (flip signs to maximise; A–B–C–D smallest distance) | 2: 2021_spring_q2_11, 2022_autumn_q1_19 | **X** | **N** | Checked: nothing in the course says points can coincide or fold back |

## Equations (33)

| type | exam count + ids | explained where (rating) | practised where (rating) | flag |
|---|---|---|---|---|
| E1 Get the asked combination without solving (add, subtract or scale the equations) | 6: 2020_autumn_q1_01, 2023_spring_q1_04, 2025_autumn_q2_17 (+2024_spring_q1_18, 2021_spring_q2_06, 2019_winter_q2_02) | t06 systems ("Ask what they want", "Get x + y directly"); t05 r26-t05-shortcuts ("Given a block"); pt51-plug-numbers-3 (4x+6y=18 → 6x+9y) **C** | r26-t06-03, q-189, q-190, q-195 [V]; t6-2-3, t6-2-4, q-212, r26-t06-16 [p] **P** | — |
| E2 Plain systems, substitution chains | 4: 2022_autumn_q2_01, 2022_winter_q1_13, 2023_winter_q2_15 (+2021_spring_q1_07) | t06 systems (substitution, elimination, why) **C** | q-164, q-165, q-179 [V]; q-146–q-163 [p] **P** | — |
| E3 Story → equation (ticket prices, ages, snake and lizard, goals) | 5: 2021_spring_q2_08, 2024_autumn_q1_14, 2022_autumn_q1_14 (+2025_autumn_q2_02, 2020_winter_q1_03) | t22 wp-027 (parts 1–3), wp-037 (outside this group); t51 pt51-plug-answers **C** | t22 g039, g049, r26-t22-05 [V]; pt-q07, pt-q09 [V, to record] **P** | — |
| E4 Factor out a non-zero common factor instead of dividing (incl. a(b−c) = 3a, 2ab−10b = 2a−10) | 4: 2021_autumn_q2_03, 2024_winter_q2_06, 2023_autumn_q2_03 (+2025_autumn_q1_01) | t06 "Don't divide by x"; t04 "Bracket as a factor"; t07 summary; solve-q-191; solve-pt-q24 (xy+5y = 2x+10, the same structure) **C** | q-185, q-191, pt-q24 [V]; q-199, q-210 [p] **P** | pt-q24 is in t51, still to record; grouping four terms is never named |
| E5 Squares and formulas inside equations ((x+1)² − (x−1)² = 0; x+y and \|x−y\| → xy) | 6: 2021_autumn_q1_13, 2025_winter_q2_05, 2020_autumn_q2_03 (+2025_winter_q2_03, 2026_spring_q2_08, 2020_spring_q1_16) | t04 formulas ("Value without x"); t07 summary; solve-q-120, q-196, r26-t07-05 **C** | q-120, q-193, q-196, r26-t07-05 [V]; q-198, r26-t07-12 [p] **P** | — |
| E6 Rational equation | 1: 2022_autumn_q1_13 | t06 linear-equations (x in the denominator, test the choices) **C** | q-171, r26-t06-01, -02 [V] **P** | — |
| E7 Possible / impossible equation; equal odd powers (x³ = y³ with x ≠ y) | 2: 2020_spring_q2_08, 2019_winter_q2_15 | Only pieces: t08 "an odd power keeps the sign", t07 summary "equal squares: equal or opposite". No rule that equal odd powers mean equal numbers **M** | q-187 [V]; q-202, q-209 [p], all about squares **T** | External review A flagged this ("power equations: even or odd"); still open because t07 is recorded |
| E8 A bound from a square (A = −x² + 7 ≤ 7; 4a² + b² = 16 ⇒ \|a\| ≤ 2) | 2: 2022_winter_q1_15, 2020_winter_q2_08 | t16 "an even power is never negative"; r26-t12-combining (range of x²). Never used as a tool for a maximum **M** | r26-t12-06, q-345 [p] **T** | Checked: plugging in for 2022_winter_q1_15 needs 3 numbers |
| E9 What a relation means ((a+c)/b = 2 ⇒ b is the average; integer a/b = 2/5 ⇒ a = 2k, b = 5k) | 2: 2021_spring_q1_03, 2022_winter_q2_16 | averages in t25; "write it as divisor × k" in t15 summary; no ratio-with-integers example in t01–t21 **M** | q-431 [V] (nearby) **T** | — |
| E10 Isolate one letter in a literal equation (1/y = 3z/(1−3zx)) | 1: 2019_winter_q1_15 | solve-q-186 (tool: cross-multiply and divide), t06 "isolate a letter" **M** | q-186 [V]; q-206, q-217 [p] **T** | Plugging in numbers works |

## Algebraic expressions (32)

| type | exam count + ids | explained where (rating) | practised where (rating) | flag |
|---|---|---|---|---|
| A1 The three formulas forward and backward; factor first; identities (incl. a³−1) | 11: 2021_spring_q2_17, 2025_spring_q1_07, 2023_spring_q1_13 (+2019_winter_q1_02, 2024_autumn_q2_11, 2024_autumn_q1_06, 2021_autumn_q2_09, 2020_winter_q1_15, 2023_winter_q1_02, 2024_winter_q1_08, 2025_spring_q2_01) | t04 r26-t04-formulas (middle term, backward, number shortcuts, x + 1/x, perfect-square check) **C** | q-120, q-121, r26-t04-01–04, q-138, r26-t05-18 [V]; q-111–q-119, r26-t04-07, -18 [p] **P** | The difference of cubes is never shown (q-106 [p] is the nearest); plugging in covers it |
| A2 Adding or subtracting fractions with letter or bracket denominators; complex fractions | 5: 2025_winter_q1_08, 2020_autumn_q2_16, 2020_winter_q2_13 (+2023_winter_q2_06, 2021_autumn_q1_15); related: 2019_spring_q1_10, 2024_spring_q2_16 | t05 expression-strategy "No cancelling!" does one example (denominator xy). No common denominator for (a−b) and (a+b), no factoring ab−b² first, no clearing a complex fraction **M**. Plugging in numbers (t05, t51) and Count the Powers (t05) are taught clearly as fallbacks | q-133 [V]; expression-extra-11, r26-t02-23, r26-t05-15 [p]. None has two bracket denominators **T** | **Biggest gap in this group.** External review A also called it "the most valuable gap"; still open because t05 is recorded |
| A3 Numeric fraction calculation | 3: 2023_autumn_q1_02, 2026_spring_q2_05, 2023_winter_q2_01 | t02 fraction-add, shortcuts **C** | r26-t02-10 [V]; q-051–q-055, r26-t02-20–22 [p] **P** | — |
| A4 Which expression is biggest or smallest in a range | 4: 2021_autumn_q1_07, 2022_autumn_q1_08, 2019_winter_q2_07 (+2019_spring_q1_10) | t17 number-line, powers-on-number-line (arrows); t08 traps; t03 compare-fractions **C** | q-098, r26-t03-02, r26-t08-02, q-497, q-500 [V]; q-507, q-511 [p] **P** | — |
| A5 Story or table with letters → expression | 3: 2020_autumn_q1_02, 2020_spring_q1_08, 2019_winter_q2_14 | pt51-plug-numbers-3 (choose numbers in a ratio or story); t22 r26-t22-04 **C** | r26-t22-04 [V]; pt-q13, pt-q14 [V, to record] **P** | Depends on t51, which is still to record |
| A6 Fractions of a whole in a story | 3: 2020_autumn_q2_01, 2021_autumn_q1_04, 2024_winter_q2_15 | t02 (of the remaining), t22 **C** | r26-t02-05 [V]; r26-t02-07, -08, -24 [p] **P** | — |
| A7 Given relations → put in the block | 1: 2020_spring_q2_01 | t05 shortcuts "Given a block" **C** | r26-t05-03 [V]; r26-t05-05 [p] **P** | — |
| A8 Decimal place value (AB.CDE = 10A + B + C/10 + …) | 1: 2020_autumn_q1_15 | t02 decimals (places right of the point); t18 digit-puzzles (10A + B) **C** | none with letters for decimal places **T** | Small |
| A9 Least and most total under per-item limits | 1: 2025_autumn_q1_14 | t21 wp-016 (three rules) **C** | wp21-g019, g020 [V]; wp21-p25, p27 [p] **P** | — |

## Exponents & roots (27)

| type | exam count + ids | explained where (rating) | practised where (rating) | flag |
|---|---|---|---|---|
| X1 Exponent laws, same base, break bases into primes | 8: 2022_autumn_q1_04, 2024_autumn_q1_16, 2021_spring_q2_15 (+2019_spring_q2_01, 2020_winter_q2_03, 2024_spring_q1_02, 2023_spring_q2_04, 2022_winter_q1_03) | t08 exponents (each law with why), t10 summary (smallest prime base) **C** | q-131, q-226, q-248, q-288, q-289 [V]; q-223–q-230, q-253–q-259 [p] **P** | — |
| X2 Roots as fractional powers; moving between forms (a^(2x) = 8 ⇒ a^x = √8) | 7: 2022_autumn_q2_07, 2019_winter_q1_13, 2023_winter_q1_05 (+2024_winter_q1_07, 2020_spring_q2_02, 2021_autumn_q2_07, 2025_winter_q2_09) | t09 roots ("Roots as powers", "Powers inside roots"); t11 summary (reciprocal power) **C** | q-297, q-301, r26-t09-01, r26-t11-02, r26-t11-13 [V]; q-235, q-236, q-280, q-285 [p] **P** | — |
| X3 Exponential and power equations (same base; a^b = 1 cases) | 4: 2023_autumn_q2_04, 2025_winter_q1_18, 2020_autumn_q2_06 (+2020_spring_q1_15) | t08 "When aᵇ = 1" (3 cases), "Compare powers" (same base ⇒ same exponent); t10 summary **C** | q-231, q-250, q-252, q-290, r26-t10-03 [V]; q-256–q-259, r26-t10-10, r26-t10-12 [p] **P** | Checked: 2025_winter_q1_18 is solvable with the t08 three cases |
| X4 Root algebra: conjugate, √m² − √n² split, perfect square under a root | 4: 2019_spring_q1_11, 2025_autumn_q1_20, 2024_spring_q2_16 (+2025_spring_q1_06) | t09 summary (partner); t11 summary (split a−b) **C** | q-298, r26-t09-06, r26-t11-01 [V]; r26-t11-04, q-308 [p] **P** | — |
| X5 Size of (√55 + 1)² | 1: 2022_winter_q2_19 | t09 traps (square of a sum; estimate a root) **C** | r26-t09-02 [V]; r26-t09-17 [p] **P** | — |
| X6 xʸ against yˣ; √x = x; root–power facts | 3: 2026_spring_q1_06, 2020_winter_q1_06 (+2024_spring_q1_15) | t08 "2⁴ = 4²"; t11 summary ("root x equals x") **C** | q-291 [V]; q-232, q-306 [p] **P** | 2024_spring_q1_15 (calculator) is an insight item |

## Number properties (27)

| type | exam count + ids | explained where (rating) | practised where (rating) | flag |
|---|---|---|---|---|
| N1 Digit puzzles in columns; reversals (AB ± BA, AAB − BAA, AAA × 3) | 7 (+2 in divisibility): 2025_spring_q1_13, 2024_winter_q1_19, 2022_autumn_q1_15 (+2025_autumn_q1_06, 2019_spring_q2_16, 2022_winter_q1_07, 2023_spring_q2_09, 2026_spring_q2_12, 2025_winter_q1_06) | t18 parts 1–2 (four steps), r26-t18-facts, summary (reversal ⇒ 11, 9, 99; AAA = 111A) **C** | q-512–q-519, r26-t18-01–03 [V]; q-522–q-540 [p] **P** | — |
| N2 Two-digit number described in words (10A + B); digit sums | 6: 2024_autumn_q1_15, 2019_winter_q1_17, 2023_winter_q1_15 (+2023_spring_q1_02, 2024_autumn_q2_06, 2025_autumn_q1_05) | t18 digit-puzzles-2 (words → 10A + B, two worked examples); r26-t18-summary **C** | q-520 [V]; t18-3-6, q-530, q-538, q-571 [p] **P** | — |
| N3 Parity of expressions (incl. odd ÷ even is not an integer) | 7: 2022_winter_q1_20, 2023_winter_q1_06, 2024_autumn_q2_03 (+2020_spring_q1_04, 2023_spring_q2_08, 2024_spring_q2_08, 2026_spring_q1_01) | t16 parity (every case with why) **C** | q-460–q-463, q-471, q-472 [V]; q-473, q-475, q-480, q-486 [p] **P** | — |
| N4 Units digit | 2: 2021_spring_q1_09, 2020_winter_q2_05 | t01 multiply-divide (the last digit of a product); t21 wp-022 (cycles of last digits) **C** | r26-t18-03 [V]; q-447, t15-3-2, r26-t18-07 [p] **P** | The units digit of a sum with a carry (b = a + 17) is not shown |
| N5 Prime facts (2 is the only even prime; a product of two primes) | 2: 2020_winter_q1_02, 2022_winter_q2_12 | t14 primes parts 1–3 **C** | q-391, q-401, r26-t14-01 [V]; q-404, q-415 [p] **P** | — |
| N6 Sum of consecutive numbers | 1: 2019_spring_q1_02 | t16 r26-t16-consecutive-sums **C** | r26-t16-02 [V]; t16-3-2 [p] **P** | — |
| N7 Squeezed between consecutive squares (√(x² − x) is never an integer); small power trial | 2: 2025_spring_q2_17, 2021_spring_q2_07 | Trial is fine (t21); the "between (x−1)² and x²" idea is absent **M** | none for the squeeze **N** | — |

## Generality (20)

| type | exam count + ids | explained where (rating) | practised where (rating) | flag |
|---|---|---|---|---|
| G1 Story with letters → formula (candies, the friends who forgot wallets) | 2: 2019_spring_q1_15, 2022_winter_q1_19 | pt51-plug-numbers-3 (the boat example, k = 0 trick, almost the same item) **C** | pt-q13, pt-q14 [V, to record]; r26-t22-04 [V] **P** | t51 is still to record |
| G2 One person gives to another: the gap changes by twice the amount | 2: 2020_spring_q2_07, 2024_spring_q2_03 | t22 solve-q-r26-t22-20 ("one card changes the gap by two", with why) **C** | r26-t22-20, wp22-g050, pt-q02, pt-q09 [V] **P** | Taught in t22 and t51 only |
| G3 Doubling or halving sequences and their totals | 3: 2021_autumn_q2_04, 2024_spring_q1_14, 2019_spring_q2_15 | t21 wp-008, wp-022, wp-001-2 (write the terms out) **C** | wp21-g009, g010, g023 [V]; wp21-p06 [p] **P** | The 100-term halving sum (between 1 and 2) needs "the total never reaches 2", which is never taught |
| G4 Story → equation or plug in the answers (prize, olives, weights) | 6: 2019_winter_q1_03, 2024_winter_q1_09, 2021_spring_q1_11 (+2019_spring_q2_06, 2023_spring_q2_02, 2022_autumn_q2_10) | t22 wp-027/wp-037; pt51-plug-answers **C** | t22 [V] many; pt-q06–pt-q09 [V, to record] **P** | — |
| G5 Integer trial under conditions (P points per gain) | 1: 2023_spring_q2_10 | t21 wp-001 (try in order) **C** | wp21-g013 [V]; wp21-p10, p11 [p] **P** | — |
| G6 Min/max (piles within 2; points range) | 2: 2022_autumn_q1_18, 2021_spring_q2_10 | t21 wp-016 **C** | wp21-g007, g020, g021 [V] **P** | — |
| G7 Back-and-forth schedule cycle | 1: 2019_winter_q1_20 | t21 wp-022, g025 **C** | wp21-g024, g025 [V] **P** | — |
| G8 Equal-sum pairs (cards 3..8 → total ÷ 3) | 1: 2020_winter_q2_01 | only inside wp21-g007 (pairs from both ends) **M** | **T** | — |
| G9 Cut roads to disconnect A from B | 1: 2021_autumn_q1_19 | **X** | **N** | Rare |
| G10 Integer + √2 (what can still be an integer) | 1: 2024_spring_q1_17 | **X** | **N** | Rare |

## Defined operations (16)

| type | exam count + ids | explained where (rating) | practised where (rating) | flag |
|---|---|---|---|---|
| O1 Evaluate: nested, two inputs, special rules (remainder, \|x\|, "x times") | 9: 2021_autumn_q2_06, 2025_autumn_q2_13, 2020_winter_q1_01 (+2023_autumn_q1_12, 2025_spring_q2_05, 2025_winter_q2_08, 2024_spring_q2_05, 2022_winter_q2_10, 2023_winter_q2_14) | t19 new-operation parts 1–3 (brackets, inside-out, slots) **C** | q-541, q-542, q-545, q-550–q-553 [V]; q-557–q-576 [p] **P** | — |
| O2 Self-inverse and inverse operations | 3: 2020_autumn_q1_09, 2023_spring_q1_20, 2024_winter_q2_20 | t19 operation-patterns (inverse = undo the steps in reverse, with the trap) **to record**; summary (rules that undo themselves) **C** | r26-t19-18 [V] (self-inverse); r26-t19-20 [p] (inverse, written only) **P** | The lesson that teaches inverses is still to record, and the inverse itself is practised only in writing |
| O3 Which definition fits a property; true/false claims | 4: 2022_autumn_q2_14, 2024_autumn_q1_18, 2021_spring_q1_08 (+2026_spring_q1_19) | t19 new-operation-3 ("no definition: test each choice"); summary (step property, both sides) **C** | r26-t19-18, q-554 [V]; r26-t19-19, q-567, q-570 [p] **P** | "No x makes #(x) = $(x)" is reached only through the t06 no-solution idea |

## Number line (2) and trial & error (2)

| type | exam count + ids | explained where (rating) | practised where (rating) | flag |
|---|---|---|---|---|
| L1 Absolute-value ranges drawn on the line (\|x\| ≤ 5; 4 ≤ \|x\| ≤ 6) | 1: 2023_autumn_q1_15 | t13 absolute-value-3 (band against two rays) **C** | q-369 [V]; t13-3-4 [p] **P** | — |
| L2 Value of an equally spaced point | 1: 2025_spring_q1_02 | t17 summary (a third of the way, midpoint); r26-t17-05 **C** | r26-t17-05 [V]; r26-t17-12, t17-3-6 [p] **P** | — |
| T1 Estimate a product | 1: 2020_spring_q2_11 | pt51-estimation (19 × 51) **C**, to record | pt-q16–pt-q19 [V, to record]; r26-t01-24 [p] **P** | — |
| T2 Cheapest way to buy an exact amount from a price table | 1: 2021_spring_q1_04 | t21 wp-001 (try in order) **C** | wp21-p04, p13 [p] **T** | — |

---

## Gaps and weak spots, ranked (exam count × weakness)

1. **Fractions with letter or bracket denominators (A2): 5 items, plus 2 related.** Rated M/T.
   - What's missing: how to choose the common denominator when the denominators share a letter, are opposite brackets (a−b, a+b), or need factoring first (ab − b² = b(a−b)); clearing a complex fraction ((x+y)/(1/x+1/y) → multiply the top and the bottom by xy).
   - Sanity check, 2020_autumn_q2_16 with our plug-in method: a=3, b=1 gives 2, and choices 1 and 2 tie. A second number, a=4, b=2, gives 1, so choice 2. It works, but it takes two rounds of fraction arithmetic. 2025_winter_q1_08 with a=2, b=1 is one round (5/3, choice 1).
   - Where: t05, after `expression-strategy` (prerequisites: t02 fraction-add, and the t04 common factor and difference of squares). t05 is recorded, so this is a new video "Fractions with letters".
   - What to add: 3 examples, easy to hard (2x and 4x; a−b and a+b; factor ab − b² first), then one complex fraction. Then 3 practice questions, one with a video, using plug-in as method 2.
2. **Equal powers, odd against even (E7, plus X3 links): 2–3 items.** Rated M/T.
   - Missing rules: equal odd powers mean equal numbers; equal even powers mean equal or opposite; an even power equal to a negative number has no solution.
   - Sanity check, 2020_spring_q2_08: with our tools a student shows choices 1 and 2 are possible (x=2, y=−2) but has no reason why x³ = y³ is impossible, so is likely to pick choice 4.
   - Where: t07, after the summary, or as a link from t09 "Odd & even roots". t07 is recorded, so this is a new short video.
   - What to add: x⁴ = 16, x⁴ = −16, x³ = −8, then a bracket base, then x³ = y³ ⇒ x = y. Then 2 practice questions, one with a video.
3. **All of t51 is still to record.** This is a production gap, not a content gap. The scripts teach plugging in numbers, plugging in the answers and estimation clearly. They are the stated fallback for A2, E8, E10 and I4, and the main method for A5, G1, G4 and T1 (day 6 in planData, very early). pt-q24 (the 2024_winter_q2_06 structure) and pt-q13/q14 (letters in a story) wait for this too. Recording t51 has the highest impact of any action here.
4. **Combining inequalities is taught only inside questions, and the reciprocal rule has no example (I2 R37, I4): 7 + 1 items.** I2 is rated C because r26-t12-03/-04 and q-336 do teach it, but `r26-t12-combining` only announces "one move is safe, the others are traps", and `r26-t12-signs` is 5 lines with no why and no worked case.
   - Where: t12, a new lesson (both are recorded).
   - What to add: add two ranges; subtract with biggest − smallest; one-sided ranges (a < 10, b > 5 ⇒ a − b < 5); a chain (a < 2b < 10). Then −½ < 1/x < ½ solved by splitting into x > 0 and x < 0, and checked with the test-number method.
   - Sanity check, 2026_spring_q1_17: the t12 test-number method solves it (x = 1 rules out choices 2 and 3; x = ¼ rules out choice 4).
5. **Using a square as a bound (E8): 2 items.** Rated M/T.
   - Sanity check, 2022_winter_q1_15: plug-in needs 3 values before only "A ≤ 7" is left.
   - Where: t12, next to the "Range of x²" slide in `r26-t12-combining` (recorded), so a new short video.
   - What to add: a² ≥ 0, so −x² + 7 ≤ 7; 4a² + b² = 16, so 4a² ≤ 16 and |a| ≤ 2. Then 2 practice questions.
6. **Inverse operations (O2): 3 items.** The teaching lesson `operation-patterns` is still to record, and the inverse is practised only in writing (r26-t19-20 [p]).
   - Sanity check, 2024_winter_q2_20: the lesson's rule (undo the last step first: square root, then subtract 1) gives choice 4 at once.
   - What to do: record `operation-patterns`. Add one video question in its style: the inverse of (x+1)² for positive x, where the √ step needs the positive condition.
7. **What a relation means, and literal equations (E9, E10): 3 items.** Rated M/T.
   - Missing ideas: (a+c)/b = 2 means b is the average of a and c; integer a/b = 2/5 means a = 2k, b = 5k, so b − a ≥ 3; isolating 1/y.
   - Where: t07 practice (recorded topic, but practice questions can be added without re-recording). Add 3 written questions with full explanations, and one with a video.
8. **Max/min of an absolute sum or distance chain (I9): 2 items, missing.**
   - Sanity check, 2022_autumn_q1_19: nothing in the course says points may fold back and meet, so a weak student answers 81 or 9.
   - What to add: in t17 (number-line distance, recorded), one insight question: "the distances can fold back; the smallest is the longest distance minus the others, but never below 0". In t13, one practice question on sign-flipping to make |sum| as big as possible.
9. **Single-item misses: D9, N7, G9, G10.**
   - D9 (non-integers between 10 and 12): a practice question in t01 r26-t01-must-could ("numbers are not only integers").
   - N7 (between consecutive squares): a practice question in t20.
   - G10 (integer + √2): a practice question in t09 or t20.
   - G9 (cutting roads): skip, too rare.
   - All of these can be written practice; no video needed.
10. **Small holes inside well-covered types.** Each needs one practice question or one sentence:
    - even divisors (D6, 2023_winter_q2_08): t14, after prime-tools;
    - "item n is in group ⌈n/size⌉" (D4, 2023_winter_q2_07): t21 wp-022 or r26-t21-10;
    - the total of a long halving sum stays below 2 (G3, 2019_spring_q2_15): t21 patterns;
    - the units digit of a sum with a carry (N4, 2021_spring_q1_09);
    - decimal place value with letters (A8, 2020_autumn_q1_15): t18 practice;
    - the difference of cubes by plug-in (A1, 2024_autumn_q1_06);
    - grouping four terms (E4): named once in the t04 summary.

### Study-order check (planData ORDER)

No type is taught after it is first needed in a way that breaks a question:
- t21 (day 8) uses cycles and "common multiple" before t14 and t15, but wp-022 and wp21-g025 teach them from scratch.
- t15 q-432 uses "three in a row ⇒ divisible by 6" before the t16 lesson, but q-432 explains it inside the question.
- t05 q-128 uses |x| before t13, but explains it with numbers.
- t12 sign analysis comes before t16 sign rules, but it relies on the t01 sign rules.

### Teaching-style notes (W22 / R37)

The older algebra lessons in t07, t10, t11 and t12 are roadmap-only. They announce the tools, and the solution videos teach them:
- `equation-strategy` (453 characters), `r26-t07-more-tools`, `advanced-powers`, `r26-t11-tools`;
- `inequality-systems`, `r26-t12-signs`, `r26-t12-combining`, `r26-t10-power-traps`.

The solution videos I read do the teaching well (e.g. r26-t12-04, r26-t15-15). Under R37, the core methods that are frequent on the exam belong in a lesson: combining inequalities (7 items) and sign tables (5 items). Everything in t13–t21 already meets R37.
