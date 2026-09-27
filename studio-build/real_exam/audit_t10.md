# Audit T10 — Exponents & Roots, Techniques (report only)

Sources: `math_patches/t10_CHANGES.md`, `math_patches/t10.py`, fixed `real_exam/quant_real.md`; original course from
`base-v18.html` / git `8965af3`.

Exam facts used: same-base equations (2023_autumn_q2_04, 2020_autumn_q2_06, 2024_spring_q1_02), same-exponent law with
letters (2021_spring_q2_15: 2ᵃ·6ᵇ = 9·2ᵇ·6ᵃ), root/power equations (2020_spring_q1_15 with "x ≠ 0" given, 2025_winter_q2_09,
2023_winter_q1_05), plug-in/try-the-choices friendly items (2020_winter_q2_03, 2023_autumn_q2_04). There are **0** real
questions on: sums of equal powers, common factor of powers (2ˣ⁺²−2ˣ), ordering huge powers (2³⁰ vs 3²⁰), exponential
inequalities with a base between 0 and 1, or aˣ = bˣ ⇒ x = 0.

| Addition | Where | Class | Verdict | Evidence |
|---|---|---|---|---|
| Q2 video: deleted false "the exam often places a number like that in its own position" | solve-q-249 slide 2 | FIX | KEEP | — |
| Root-equation example replaced: √(x+2)=x solved in full (the old √(x+7)=x−1 was never solved) | `powers-techniques` slide "Root equations" | FIX | KEEP | — |
| ":" → "÷" in draw notes | `powers-techniques` slides 2, 3; solve-q-249 slide 3 | FIX | KEEP | — |
| New example 2⁻⁶ ÷ 2⁻⁴ = 2⁻² | `powers-techniques` slide "Negative exponents" | METHOD | KEEP | 2019_spring_q2_01, 2024_winter_q1_07; original q-248 |
| "You can also put each choice into the exponent" | `powers-techniques` slide "Power equations" | METHOD | KEEP | 2023_autumn_q2_04, 2020_autumn_q2_06 |
| New slide "Try the choices" (plug-in for root/power equations, throws out fake solutions) | `powers-techniques` slide 10 | METHOD | KEEP | 2020_spring_q1_15, 2023_autumn_q2_04, 2020_autumn_q2_06 |
| Recap line + "Six questions next" | `powers-techniques` slide "Recap" | FIX | KEEP | — |
| Q5 video: "If x ≠ 0 is NOT given, don't divide by x — factor" | solve-q-252 slide 2 | METHOD | KEEP | 2020_spring_q1_15, 2023_autumn_q2_03 (x ≠ 0 is given exactly because 0 also solves); original q-247, q-252 |
| Traps video title slide | `r26-t10-power-traps` slide 1 | — | KEEP | (video stays; 3 content slides kept) |
| "Sums of equal powers" (2¹⁰+2¹⁰=2¹¹, 3ˣ+3ˣ+3ˣ, trap 4ˣ) | `r26-t10-power-traps` "Sums of equal powers" | METHOD | KEEP (rule 2) | Exam: 0. Kept because original T11 q-293 (2ˣ = 2ʸ+2ʸ+2ʸ+2ʸ) needs it. Note: duplicates T8 slide "Adding equal powers". |
| "Common factor" (2ˣ⁺²−2ˣ = 3·2ˣ) | `r26-t10-power-traps` "Common factor" | METHOD | KEEP (rule 2) | Exam: 0 for powers (only factorial analogues 2020_winter_q1_19, 2024_winter_q2_17). Kept because original T11 q-311 (3ⁿ−3ⁿ⁻¹), q-320 ((5⁴−5³)/4), q-321 need it. |
| "Same exponent" (aˣbˣ=(ab)ˣ) | `r26-t10-power-traps` "Same exponent" | METHOD | KEEP | 2021_spring_q2_15; original q-271, q-281 |
| "Compare powers" (2³⁰=8¹⁰<9¹⁰=3²⁰) | `r26-t10-power-traps` "Compare powers" | CONTENT | REMOVE | 0 real questions; originals only compare same-base powers (2¹²/4⁵), which T8 teaches |
| "Bases between 0 and 1" ((½)ˣ>(½)ʸ ⇒ x<y) | `r26-t10-power-traps` "Bases between 0 and 1" | CONTENT | REMOVE | 0 exponential inequalities on the exam; no original needs it |
| "When is aˣ = bˣ?" (⇒ x = 0) | `r26-t10-power-traps` "When is aˣ = bˣ?" | CONTENT | REMOVE | 0; no original needs it |
| Recap slide of the traps video | `r26-t10-power-traps` "Recap" | — | KEEP (edit) | drop its lines for the 3 removed slides |
| New card "Exponent and root techniques": rows Number over a root, Different bases, Negative exponent, Adding roots, Same exponent, Power equation, Root equation | `mem-r26-t10-techniques` | METHOD | KEEP | 2024_autumn_q1_16, 2021_spring_q2_15, 2023_autumn_q2_04, 2025_winter_q2_09 |
| Card rows "Equal powers added", "Same base, different exponents" + tip "2ˣ+2ˣ ≠ 4ˣ" | `mem-r26-t10-techniques` | METHOD | KEEP (rule 2) | original q-293, q-311, q-320 |
| Card tips: pair the families, try the choices, don't divide by x, choose easy values | `mem-r26-t10-techniques` tips | METHOD | KEEP | original q-248; 2020_spring_q1_15, 2020_winter_q2_03 |
| Card row "Comparing powers" (2³⁰ vs 3²⁰) | `mem-r26-t10-techniques` | CONTENT | REMOVE | 0 |
| Card row "Base between 0 and 1" | `mem-r26-t10-techniques` | CONTENT | REMOVE | 0 |
| Card row "aˣ=bˣ, a≠b ⇒ exponent 0" | `mem-r26-t10-techniques` | CONTENT | REMOVE | 0 |
| Guided Q6 √(2x+3)=x + video | q-r26-t10-01, solve-q-r26-t10-01 | METHOD | KEEP | 2020_spring_q1_15, 2025_winter_q2_09; original q-251, q-266 |
| Guided Q7 2¹⁰+2¹⁰+2¹⁰+2¹⁰ + video | q-r26-t10-02, solve-q-r26-t10-02 | CONTENT (type) | REMOVE | 0 real questions of this type |
| Guided Q8 3ˣ⁺²−3ˣ=72 + video | q-r26-t10-03, solve-q-r26-t10-03 | CONTENT (type) | REMOVE | 0 |
| Guided Q9 order of 2⁴⁵, 3³⁰, 5¹⁵ + video | q-r26-t10-04, solve-q-r26-t10-04 | CONTENT (type) | REMOVE | 0 |
| Guided Q10 (1/3)ˣ > 1/27 + video | q-r26-t10-05, solve-q-r26-t10-05 | CONTENT (type) | REMOVE | 0 |
| Plug-in / easy-value lines in solutions of q-268, q-270; Q7 small-number check | q-268, q-270 solutions | METHOD | KEEP | 2020_winter_q2_03 |
| Text: TeX solutions, stacked conditions, rewording (q-252, q-286, q-278, q-268, q-270, q-280, q-276, q-287, q-284, q-269, q-279, set t10-2) | T10 questions | FIX | KEEP | — |
| Practice 3ˣ+3ˣ+3ˣ | q-r26-t10-06 | CONTENT (type) | REMOVE | 0 |
| Practice 0.2ˣ = 25 | q-r26-t10-07 | METHOD | KEEP | same-base equation: 2023_autumn_q2_04, 2020_autumn_q2_06; original q-259 |
| Practice 4ˣ·25ˣ = 10⁶ | q-r26-t10-08 | METHOD | KEEP | 2021_spring_q2_15 |
| Practice √(x+12) = x | q-r26-t10-09 | METHOD | KEEP | 2020_spring_q1_15, 2025_winter_q2_09 |
| Practice x√3 = √(3x) (don't divide by x) | q-r26-t10-10 | METHOD | KEEP | 2020_spring_q1_15, 2023_autumn_q2_03; original q-252 |
| Practice (5ⁿ⁺¹−5ⁿ)/4 | q-r26-t10-11 | CONTENT (type) | REMOVE | 0 on the exam (near-copy of original T11 q-320) |
| Practice 2ˣ+2ˣ = 4ˣ | q-r26-t10-12 | CONTENT (type) | REMOVE | 0 |
| Practice 5ˣ⁻² = 7ˣ⁻² | q-r26-t10-13 | CONTENT (type) | REMOVE | 0 |
| Practice (½)²ˣ⁻¹ < 1/8 | q-r26-t10-14 | CONTENT (type) | REMOVE | 0 |
| Practice greatest of 2⁴⁰, 3³⁰, 4²⁰, 5²⁰ | q-r26-t10-15 | CONTENT (type) | REMOVE | 0 |
| Practice 3²⁰+3²⁰+3²⁰ = 9ⁿ | q-r26-t10-16 | CONTENT (type) | REMOVE | 0 |

## TO REMOVE
- Slides: video `r26-t10-power-traps`, slides "Compare powers", "Bases between 0 and 1", "When is aˣ = bˣ?" (plus their sidebar labels; remove the matching lines on the "Recap" slide).
- Questions + solution videos: q-r26-t10-02 + solve-q-r26-t10-02; q-r26-t10-03 + solve-q-r26-t10-03; q-r26-t10-04 + solve-q-r26-t10-04; q-r26-t10-05 + solve-q-r26-t10-05. (Guided count 10 → 6; section title "Ten guided questions" and the Q1–Q10 sidebars must follow.)
- Practice questions: q-r26-t10-06, q-r26-t10-11, q-r26-t10-12, q-r26-t10-13, q-r26-t10-14, q-r26-t10-15, q-r26-t10-16.
- Card rows: `mem-r26-t10-techniques`, table "Techniques", rows "Comparing powers", "Base between 0 and 1", "$a^x=b^x$, $a\ne b$ (positive)".

Counts (table rows): KEEP 23 (incl. 5 FIX) · REMOVE 17 · UNSURE 0.

## ORIGINAL ITEMS REMOVED BY FIXERS (to restore)
- **q-263** (√63 = ?, choices 4√3/3√3/2√7/3√7) — removed as a repeat of q-262.
- **q-283** (√98 = ?, choices 7√2/2√7/7√7/4√6) — removed as a repeat of q-262.
- **q-277** (Given x = y = 8, x^(y−x)·y^(x−y) = ?, choices 64/8/0/1) — removed as "trivial".
- **alg-extra-unit-t10-3-1 … 3-7** (the 7-item extra set: 4⁸/4⁵; 125^(2/3); 3ˣ⁺¹=3⁶; 4⁻³+4⁻²; (4x)³/16x²; 2¹⁴ vs 4⁶; √98+√32) — removed as the same templates as set t10-2.
- **alg-extra-unit-t10-2-6** — choices changed: original "The first power / The second power" replaced by "2¹² / 4⁵".
- Video `powers-techniques`, slide "Root equations" — original example √(x+7) = x − 1 with the board line "x − 1 ≥ 0 → x ≥ 1" replaced by √(x+2) = x.
- Video `powers-techniques`, slides "Negative exponents", "Power equations", "Recap" — original scripts edited (recap said "Five questions next").
- Video solve-q-249, slide 2 — original line "the exam often places a number like that in its own position" deleted.
