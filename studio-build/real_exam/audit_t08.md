# Audit T8 — Exponent Laws, Fundamentals (report only)

Sources: `math_patches/t08_CHANGES.md`, `math_patches/t08.py`, `real_exam/quant_real.md` (fixed full-text version; the
stems that were cut at "<" were also checked against `nite-psychometry/data/psychometric_*_quant.json`).
Original course = `base-v18.html` / git `8965af3:content/full-course/topics/t8.json` (before the 2026-09 patches).

Exam facts used: power/root questions are all short "simplify / same base / equation" items
(2022_autumn_q1_04, 2019_spring_q2_01, 2020_winter_q2_03, 2024_autumn_q1_16, 2024_spring_q1_02, 2023_autumn_q2_04,
2021_spring_q2_15, 2020_autumn_q2_06, 2025_winter_q1_18, 2026_spring_q1_06). There are **0** real questions on: sums of
equal powers (2ⁿ+2ⁿ), ordering huge powers by equal exponents (2³⁰ vs 3²⁰), trailing zeros / digit counts, or decimal
powers (0.3², 0.2³).

| Addition | Where | Class | Verdict | Evidence |
|---|---|---|---|---|
| "2⁴ = 4²" overclaim fixed ("among positive whole numbers") + card tip 1 | `exponents` slide "2⁴ = 4²"; card `powers` tip 1 | FIX | KEEP | — (2026_spring_q1_06 uses 2⁴=4²) |
| "b an even whole number" | `exponents` slide "When aᵇ = 1" | FIX | KEEP | — |
| Exponent 0 by a ÷5 "staircase" (no division law before it is taught); negative exponents moved before "Bases 1 and 0" | `exponents` slides "Exponent 1 and 0", "Negative exponents", "Bases 1 and 0" | FIX | KEEP | — |
| q-227, extra-2, extra-7 moved to T9 (need roots) | T9 practice | FIX | KEEP | — |
| Slide text fixes ("two hundred sixteen", "Core questions next", sidebar, section title) | `exponents` slides 9, 15 | FIX | KEEP | — |
| New slide "Adding equal powers" (2ⁿ+2ⁿ=2ⁿ⁺¹, trap 2²ⁿ) | `exponents` slide 14 | METHOD | KEEP (rule 2) | Exam: 0 questions. Kept because original T11 q-293 (2ˣ = 2ʸ+2ʸ+2ʸ+2ʸ, original video "Count the copies") needs it. |
| Traps video title slide | `r26-t08-traps` slide 1 | — | KEEP | (video stays; 4 of 5 content slides kept) |
| "Between 0 and 1" (x³<x²<x, powers of ½, decimal places) | `r26-t08-traps` "Between 0 and 1" | METHOD | KEEP | 2022_autumn_q1_08 (0<a<¼, smallest of −1/a, −a, −√a, −a/4), 2021_autumn_q1_07 (1<x<2, ordering x², 2/x, xˣ); original alg-extra-unit-t12-3-3. The decimal-places half has 0 exam support. |
| "Compare powers" (same base 2¹⁰ vs 4⁴; same exponent 2³⁰ vs 3²⁰; same base ⇒ equal exponents) | `r26-t08-traps` "Compare powers" | METHOD | KEEP | Same-base rewrite: 2024_autumn_q1_16, 2024_spring_q1_02; equal exponents: 2023_autumn_q2_04, 2021_spring_q2_15; comparing xʸ vs yˣ: 2026_spring_q1_06; original alg-extra-exponent-extra-6. The 2³⁰ vs 3²⁰ example itself has 0 exam support. |
| "Counting zeros" (2⁴·5⁴=10⁴, zeros = smaller exponent) | `r26-t08-traps` "Counting zeros" | CONTENT | REMOVE | 0 real questions on trailing zeros/digit counts; no original question needs it (q-228 is the plain same-exponent law). |
| "Signs with letters" (odd power keeps sign, (−x)² vs −x²) | `r26-t08-traps` "Signs with letters" | METHOD | KEEP | 2023_autumn_q1_01 (a·b²·c positive), 2024_spring_q2_08 (y·x²·z), 2020_spring_q2_08 (x³=y³ impossible) |
| "Check with a number" | `r26-t08-traps` "Check with a number" | METHOD | KEEP | 2020_winter_q2_03, 2019_spring_q1_11, 2024_spring_q2_16 |
| Guided Q "2ⁿ+2ⁿ+2ⁿ+2ⁿ" + solution video | q-r26-t08-01, solve-q-r26-t08-01 | CONTENT (type) | REMOVE | 0 real questions of this type |
| Guided Q "0<x<1, smallest of x, x², x³, x⁻²" + video | q-r26-t08-02, solve-q-r26-t08-02 | METHOD | KEEP | 2022_autumn_q1_08, 2021_autumn_q1_07 |
| Guided Q "largest of 2⁴⁰, 3³⁰, 5²⁰, 10¹⁰" + video | q-r26-t08-03, solve-q-r26-t08-03 | CONTENT (type) | REMOVE | 0 real questions ordering huge powers |
| Guided Q "zeros at the end of 2⁷·5⁴" + video | q-r26-t08-04, solve-q-r26-t08-04 | CONTENT | REMOVE | 0 |
| Guided Q "x³y²<0, necessarily" + video | q-r26-t08-05, solve-q-r26-t08-05 | METHOD | KEEP | 2023_autumn_q1_01, 2024_spring_q2_08 |
| New solution videos for original q-224, q-226, q-231 (q-231 moved into core) | solve-q-224, solve-q-226, solve-q-231 | FIX | KEEP | original questions |
| Card Laws row "aⁿ+aⁿ=2aⁿ, copies" | card `powers`, Laws table | METHOD | KEEP (rule 2) | original q-293 (T11) |
| Card Laws row "(−1)ⁿ" | card `powers`, Laws table | METHOD | KEEP | 2025_winter_q1_18 (x³ⁿ=1: n odd ⇒ x=1, n even ⇒ x=±1) |
| Card table "More powers to know" (2⁹, 2¹⁰, 10ⁿ, 10⁻ⁿ) | card `powers` | METHOD | KEEP | 2024_autumn_q1_16 (8³=2⁹=512, 4⁶), 2024_autumn_q1_18 (10ⁿ) |
| Card "Exam traps" rows: Between 0 and 1 / Compare powers / Signs | card `powers`, table "Exam traps" | METHOD | KEEP | as the matching slides above |
| Card "Exam traps" row "Zeros at the end" | card `powers`, table "Exam traps" | CONTENT | REMOVE | 0 |
| Card tips: smallest prime base; check with a number | card `powers` tips 3, 4 | METHOD | KEEP | 2024_autumn_q1_16, 2024_spring_q1_02; 2020_winter_q2_03 |
| All solutions in TeX, NITE-style stems, q-232 reworded | all T8 questions | FIX | KEEP | — |
| Practice copies-3: 3ⁿ+3ⁿ+3ⁿ | q-r26-t08-06 | CONTENT (type) | REMOVE | 0 |
| Practice copies-5: (5·5¹²)/5¹⁰ | q-r26-t08-07 | CONTENT (type) | REMOVE | 0 |
| Practice copies-eq: 2ⁿ⁺¹+2ⁿ⁺¹=32 | q-r26-t08-08 | CONTENT (type) | REMOVE | 0 |
| Practice dec-sq: 0.3² | q-r26-t08-09 | CONTENT (type) | REMOVE | 0 decimal-power questions (the only decimals on the exam are in word problems) |
| Practice dec-cube: 0.2³·10⁴ | q-r26-t08-10 | CONTENT (type) | REMOVE | 0 |
| Practice neg-01: −1<x<0, largest of x, x², x³, x⁴ | q-r26-t08-11 | METHOD | KEEP | 2022_autumn_q1_08, 2023_spring_q1_08 (−1<x<0) |
| Practice cmp-base: largest of 16², 8³, 2¹², 4⁵ | q-r26-t08-12 | METHOD | KEEP | 2024_autumn_q1_16, 2024_spring_q1_02 |
| Practice cmp-order: 2⁵⁰, 3³⁰, 5²⁰ | q-r26-t08-13 | CONTENT (type) | REMOVE | 0 |
| Practice cmp-eq: 4ˣ=8⁴ | q-r26-t08-14 | METHOD | KEEP | 2023_autumn_q2_04, 2024_spring_q1_02, 2020_autumn_q2_06 |
| Practice zeros-eq: 2³·5⁶=? (value) | q-r26-t08-15 | original law (same exponent) | KEEP | "evaluate a product of powers": 2022_autumn_q1_04; original q-228 |
| Practice digits: digits of 4⁵·5⁸ | q-r26-t08-16 | CONTENT (type) | REMOVE | 0 |
| Practice sign-odd / sign-neg / sign-2 | q-r26-t08-17, 18, 19 | METHOD | KEEP | 2023_autumn_q1_01, 2024_spring_q2_08, 2020_spring_q2_08 |
| Practice ab1: (x−2)^(x+3)=1, how many x | q-r26-t08-20 | original content (aᵇ=1) | KEEP | 2025_winter_q1_18; original q-231, q-290 |
| Practice mix-1/2/3 ("which law") | q-r26-t08-21, 22, 23 | original laws | KEEP | 2022_autumn_q1_04, 2019_spring_q2_01, 2020_winter_q2_03 |

## TO REMOVE
- Slide: video `r26-t08-traps`, slide "Counting zeros" (and its sidebar label; the title slide's list of topics if it names zeros).
- Questions + their solution videos: q-r26-t08-01 + solve-q-r26-t08-01; q-r26-t08-03 + solve-q-r26-t08-03; q-r26-t08-04 + solve-q-r26-t08-04. (Guided numbering in T8 then changes: Questions 4–8 → 4–5.)
- Practice questions: q-r26-t08-06, q-r26-t08-07, q-r26-t08-08, q-r26-t08-09, q-r26-t08-10, q-r26-t08-13, q-r26-t08-16.
- Card row: card `powers`, table "Exam traps", row "Zeros at the end".

Counts (table rows): KEEP 27 (incl. 7 FIX) · REMOVE 12 · UNSURE 0.

## ORIGINAL ITEMS REMOVED BY FIXERS (to restore)
- **alg-extra-exponent-extra-1** ("Evaluate 2⁶/2³", choices 8/2/4/16, key 8) — removed from practice as a near-duplicate of q-225.
- **alg-extra-exponent-extra-6** — choices and key replaced. Original: "Which is greater: 2¹⁰ or 4⁴?" with choices "It cannot be determined from the information given / The first power / The second power / They are equal", key "The first power".
- **q-227, alg-extra-exponent-extra-2, alg-extra-exponent-extra-7** — not deleted, but moved out of T8 into T9 practice (their topic field is now 9).
- Video `exponents`, slide "Exponent 1 and 0" — original proof (5³/5³ = 5⁰ = 1) replaced by the ÷5 staircase.
- Video `exponents`, slides "Bases 1 and 0" and "Negative exponents" — original order (Bases 1 and 0 before Negative exponents) swapped; the "Bases 1 and 0" line "A negative exponent means dividing by zero — undefined. Zero to the zero? Not defined in this course either." replaced.
- Video `exponents`, slide "2⁴ = 4²" — original script ("the one special case… any other pair, one side is always bigger") replaced.
- Card `powers`, tips — original "2⁴=4²=16 — the one time swapping base and exponent gives the same number." and "Different bases? Rewrite with the smallest prime base: 8=2³, 9=3²." replaced by reworded versions.
- All original stems/solutions were reworded (NITE style, TeX); the original texts are in git `8965af3`.
