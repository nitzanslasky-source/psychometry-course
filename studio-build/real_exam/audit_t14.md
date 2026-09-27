# Audit T14 — Prime Numbers (report only)

Sources: `math_patches/t14_CHANGES.md`, `math_patches/t14.py`, fixed `real_exam/quant_real.md`; original course from
`base-v18.html` / git `8965af3`.

Exam facts used: primes/parity (2020_winter_q1_02 consecutive primes, 2024_autumn_q2_03 prime > 2 is odd,
2025_autumn_q1_05 two-digit primes with digit sum 5, 2022_winter_q2_12 product of two primes: 66/78/85/105), divisors/LCM/GCD
(2023_spring_q2_06 common divisor of 84 and 210, 2025_winter_q2_10 divisible by 10 and 15 ⇒ by 6, 2024_spring_q1_06 LCM 70,
2022_winter_q1_02 LCM 30, 2020_autumn_q1_12, 2024_autumn_q2_13 divisible by a and b but not by ab, 2021_autumn_q2_14 N²K,
2024_winter_q1_04 3⁶, 2023_winter_q2_08 even divisors of 40, 2021_spring_q1_14 49 = 7², 2025_autumn_q2_07 divisor counts),
factorisation equations (2021_spring_q2_15 2ᵃ·6ᵇ = 9·2ᵇ·6ᵃ, 2019_winter_q2_16 2⁷·3²·x = 8!), prime in a product
(2023_autumn_q2_16 y = ab/x with primes a, b), squares via exponents (2024_spring_q2_07 x divisible by 3 and √x integer).
**0** real questions on trailing zeros, on "smallest k making a perfect square/cube", on perfect cubes of integers, or on
GCD × LCM = a × b.

| Addition | Where | Class | Verdict | Evidence |
|---|---|---|---|---|
| False line deleted ("primes are the small numbers you never meet … times table") | `primes` slide "What a prime is" | FIX | KEEP | — |
| GCD/LCM rule made exact (lower power / higher power), official names; recap underlines LOWER/HIGHER; card; Q5 video | `prime-tools` slides "Greatest common (GCD)", "Greatest guaranteed (LCM)", "Recap"; card `mem-factor-tools`; solve-q-389, solve-q-390 | FIX | KEEP | 2023_spring_q2_06, 2025_winter_q2_10, 2024_spring_q1_06 |
| GCD/"guaranteed divisor" questions (old Q4, Q5) moved after the Factor Tools lesson | flow | FIX | KEEP | — |
| Solution text fixes (q-420, q-422, extra 4-1, 4-2, 4-4) | questions | FIX | KEEP | — |
| Slide "0, 1 and 2": 0, 1, negatives not prime; "odd sum/difference of two primes → one is 2" | `primes` slide 3 | METHOD | KEEP | 2020_winter_q1_02, 2024_autumn_q2_03; original q-391, q-412, q-415 |
| New slide "Is it prime?" (√n test, digit-sum test for 3, fake primes 51, 57, 87, 91, 119) | `primes` slide 5 | METHOD | KEEP | 2025_autumn_q1_05, 2022_winter_q2_12; original q-407, q-413, alg-extra-unit-t14-4-7 (91) |
| Recap: parity + √n lines, "Four questions next" | `primes` "Recap" | FIX | KEEP | — |
| Card `mem-primes`: primes to 60, facts (0/1/negatives, parity, √n), fake-primes table, digit-sum tip | `mem-primes` | METHOD | KEEP | as the two slides |
| New slide "GCD vs LCM" (table, GCD×LCM = a×b check, trap: multiplying the two numbers) | `prime-tools` slide 4 | METHOD | KEEP | trap: 2024_autumn_q2_13, 2025_winter_q2_10; original q-422 (4 and 6 ⇒ 24?), q-389, q-390 |
| Break & build: "letters as primes? plug in 2, 3, 5, 7, check every choice" | `prime-tools` slide "Break & build" | METHOD | KEEP | 2023_autumn_q2_16, 2024_autumn_q2_03; original q-394 |
| Symmetric divisors: odd number of divisors ⇔ perfect square | `prime-tools` slide "Symmetric divisors" | CONTENT | KEEP (rule 2) | Exam: counting divisors 2021_spring_q1_14, 2025_autumn_q2_07. Needed by original q-417 ("number of divisors is odd ⇒ √n integer"). |
| Factor Tools recap + card `mem-factor-tools` (6 rows, 3 tips) | `prime-tools` "Recap"; `mem-factor-tools` | FIX/METHOD | KEEP | as above |
| More Factor Tools title slide | `r26-t14-more-tools` slide 1 | — | KEEP | — |
| "Squares & cubes" (18k a square → k=2; 18k a cube → k=12) | `r26-t14-more-tools` "Squares & cubes" | METHOD | KEEP (rule 2) for squares · UNSURE for the cube half | Squares: original alg-extra-unit-t14-4-6 (smallest k with 18k a square) needs it; exam 2024_spring_q2_07, 2021_autumn_q2_14 use "a square has even exponents". Cubes: 0 exam, 0 original — cannot be removed without splitting the slide. |
| "Prime equations" (2ᵃ·3ᵇ = 72; p²q = 50) | `r26-t14-more-tools` "Prime equations" | METHOD | KEEP | 2021_spring_q2_15, 2019_winter_q2_16; original q-396, q-408 |
| "Zeros at the end" (pairs of 2 and 5) | `r26-t14-more-tools` "Zeros at the end" | CONTENT | REMOVE | 0 real questions; no original question needs it |
| "A prime in a product" (+ counterexample 6 \| 4·9) | `r26-t14-more-tools` "A prime in a product" | METHOD | KEEP | 2023_autumn_q2_16, 2024_autumn_q2_13; original q-395 |
| More Factor Tools recap | `r26-t14-more-tools` "Recap" | — | KEEP (edit) | drop its zeros line |
| New card "More factor tools": rows Perfect square, Prime equation, A prime divides a product; 2 tips | `mem-r26-t14-more-tools` | METHOD | KEEP | as slides |
| Card row "Perfect cube" | `mem-r26-t14-more-tools` | CONTENT | UNSURE | same as the cube half of the slide: 0 exam, 0 original |
| Card row "Zeros at the end" | `mem-r26-t14-more-tools` | CONTENT | REMOVE | 0 |
| Old Q15 video closing: "never true is also not necessarily true" | solve-q-395 | METHOD | KEEP | 2022_winter_q1_20, 2021_spring_q1_15 |
| Guided Q4 "which is prime: 91, 119, 113, 133" + video | q-r26-t14-01, solve-q-r26-t14-01 | METHOD | KEEP | 2022_winter_q2_12, 2025_autumn_q1_05 |
| Guided Q12 smallest k with 24k a perfect cube + video | q-r26-t14-02, solve-q-r26-t14-02 | CONTENT (type) | REMOVE | 0 |
| Guided Q13 2ᵃ·3ᵇ = 108, a−b + video | q-r26-t14-03, solve-q-r26-t14-03 | METHOD | KEEP | 2021_spring_q2_15, 2019_winter_q2_16 |
| Guided Q14 zeros at the end of 20⁴·15³ + video | q-r26-t14-04, solve-q-r26-t14-04 | CONTENT (type) | REMOVE | 0 |
| Text: TeX, "÷", stacked conditions, rewording (q-396, q-401, q-400, q-407, q-415) | T14 questions and slides | FIX | KEEP | — |
| Practice how many primes between 80 and 100 | q-r26-t14-05 | METHOD | KEEP | 2025_autumn_q1_05 |
| Practice sum of primes between 50 and 60 | q-r26-t14-06 | METHOD | KEEP | 2025_autumn_q1_05, 2022_winter_q2_12 |
| Practice 1<n<120 not divisible by 2, 3, 5, 7 ⇒ prime | q-r26-t14-07 | METHOD | KEEP | √n test; 2025_autumn_q1_05 |
| Practice GCD 6, LCM 180, one number 36 → the other | q-r26-t14-08 | CONTENT (type) | REMOVE | 0 (GCD×LCM formula questions) |
| Practice LCM of p³q and p²q⁴ | q-r26-t14-09 | METHOD | KEEP | LCM: 2025_winter_q2_10, 2024_spring_q1_06, 2022_winter_q1_02; original q-410 type |
| Practice smallest k with 2³·3⁴·5·k a square | q-r26-t14-10 | CONTENT (type) | REMOVE | 0 on the exam (original extra 4-6 is the same type) |
| Practice smallest m with 2⁴·3²·m a cube | q-r26-t14-11 | CONTENT (type) | REMOVE | 0 |
| Practice p²q = 75, p+q | q-r26-t14-12 | METHOD | KEEP | 2021_spring_q2_15, 2019_winter_q2_16 |
| Practice 6ˣ·5ʸ = 1080, x+y | q-r26-t14-13 | METHOD | KEEP | 2021_spring_q2_15 (mixed bases 2ᵃ·6ᵇ) |
| Practice zeros at the end of 20! | q-r26-t14-14 | CONTENT (type) | REMOVE | 0 |
| Practice 14 \| ab ⇒ 7 divides a or b | q-r26-t14-15 | METHOD | KEEP | 2023_autumn_q2_16 |

## TO REMOVE
- Slide: video `r26-t14-more-tools`, slide "Zeros at the end" (plus its sidebar label and the matching line on the "Recap" slide).
- Questions + solution videos: q-r26-t14-02 + solve-q-r26-t14-02; q-r26-t14-04 + solve-q-r26-t14-04. (Advanced guided numbering changes.)
- Practice questions: q-r26-t14-08, q-r26-t14-10, q-r26-t14-11, q-r26-t14-14.
- Card row: `mem-r26-t14-more-tools`, row "Zeros at the end".
- UNSURE (teacher decides): cube half of slide `r26-t14-more-tools` "Squares & cubes" and card row "Perfect cube".

Counts (table rows): KEEP 29 (incl. 6 FIX) · REMOVE 8 · UNSURE 1 (card row "Perfect cube"; the cube half of the kept "Squares & cubes" slide is flagged with it).

## ORIGINAL ITEMS REMOVED BY FIXERS (to restore)
- **q-416** ("Given t > 1 and t² is a prime number. Then t is necessarily —", choices odd/even/not an integer/less than 5) — removed as the same as guided Q10 (q-401).
- **q-420** ("m has exactly three distinct divisors. Then √m is necessarily —", choices prime/even/divisible by 5/not an integer) — removed as the third "exactly 3 divisors" item.
- **q-410** ("p, q, r distinct primes; M = p²q³r, N = p³qr². GCD of M and N?") — removed as the same as guided Q5 (q-389).
- Video `primes`, slide "What a prime is" — original line "The primes are the small numbers you never meet as an answer inside the times table." deleted (it was false).
- Video `primes`, slide **"1 and 2"** replaced by "0, 1 and 2" (original: "1 is not prime · 2 is the only even prime"; kept in substance); "Recap" rewritten (original "Know the primes up to 40 — and 97", "Divides by every combination of its prime factors", "Five questions next").
- Video `prime-tools`, slides **"Greatest common"** and **"Greatest guaranteed"** rewritten as "(GCD)"/"(LCM)" (original wording "take out a common factor", "shared ones counted once"); "Recap", "Break & build", "Symmetric divisors", "Factor Tools" title scripts rewritten.
- Video solve-q-389, slide **"Take out a common factor"** replaced by "Lower power"; video solve-q-390, slide **"Break down and offset"** replaced by "Higher power".
- Card `mem-primes` — original table "Primes up to 40" (4 rows) replaced by a table up to 60; original Facts row "1 | is not prime" reworded; original tips "A number divides by every combination of its prime factors (12 = 2·2·3 → 2, 3, 4, 6, 12)." and "To test a divisor, check its prime ingredients — unpack composite bases like 6 or 10² first." removed.
- Card `mem-factor-tools` — original rows "Greatest COMMON divisor … the smaller power | 72, 90 → 18", "Greatest GUARANTEED divisor … a prime in both counts once | → 360", "Exactly 3 divisors | a prime squared", "Number of divisors | each exponent + 1, multiplied" replaced by reworded rows; original tip "Divides by 2 and 5 → by 10. Divides by 2 and 6 → only 6 is sure (the 2 is inside the 6)." removed.
- **q-415** — the condition "1 < p" removed from the stem; **q-396** stem reworded ("a has exactly two prime factors: 2 and 5", asks for the smallest value).
- Guided numbering: all T14 guided questions renumbered (old Q4/Q5 moved to theory B).
