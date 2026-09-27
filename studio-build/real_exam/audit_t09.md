# Audit T9 — Roots, Fundamentals (report only)

Sources: `math_patches/t09_CHANGES.md`, `math_patches/t09.py`, fixed `real_exam/quant_real.md`; original course from
`base-v18.html` / git `8965af3`.

Exam facts used: root questions on the real exam are simplifying (2025_spring_q1_06, 2023_spring_q2_04, 2022_winter_q1_03),
fractional powers (2022_autumn_q2_07, 2019_winter_q1_13, 2024_winter_q1_07, 2020_spring_q2_02), root equations by
squaring (2020_spring_q1_15, 2021_autumn_q2_07, 2025_winter_q2_09), conjugates (2025_autumn_q1_20, 2019_spring_q1_11),
(√a+b)² (2022_winter_q2_19), estimating a root between squares (2023_autumn_q1_07). There are **0** real questions on:
roots of decimals (√0.09, √0.0016), comparing roots of different order (√2 vs ∛3), or the domain of a root.

| Addition | Where | Class | Verdict | Evidence |
|---|---|---|---|---|
| Card tip "6/√3 = 2√3" now taught on the slide, with the reason | `roots` slide "Multiply & divide"; card `roots` tip 2 | FIX | KEEP | — |
| "√(75 : 3)" → "÷"; "fifteen questions" wording | `roots` slides 1, "Multiply & divide", "The rules table" | FIX | KEEP | — |
| Domain line: √(x−3) exists only for x ≥ 3 | `roots` slide "What a root is" (added lines) | CONTENT | KEEP (rule 2) | Exam: 0 domain questions. Kept because the original card `roots` already had the tip "Inside a square root: never negative" — the line teaches an original rule. |
| One example with x<0: √((−3)²)=3=−x | `roots` slide "Root of a square" | FIX | KEEP | original alg-extra-root-practice-3 |
| Pull out the LARGEST square + check | `roots` slide "Pull out squares" | METHOD | KEEP | 2025_spring_q1_06 (√12·√15, 2√45, 3√30, √10·√18) |
| New slide "Bring a number inside" (3√7=√63) | `roots` slide 5 | METHOD | KEEP | 2025_spring_q1_06, 2023_autumn_q1_07; original q-243, q-244 |
| New slide "Powers inside roots" (ⁿ√aᵐ=a^(m/n), 8^(2/3), √√a=⁴√a) | `roots` slide 10 | CONTENT | KEEP | 2022_autumn_q2_07, 2023_spring_q2_04, 2019_winter_q1_13, 2024_winter_q1_07, 2020_spring_q2_02 (5); original q-235, q-236 |
| New slide "Root equations" (square, check; x=√3x: factor; plug in choices) | `roots` slide 12 | METHOD | KEEP | 2020_spring_q1_15 (√x = 2·⁴√x), 2025_winter_q2_09, 2021_autumn_q2_07; original q-247, alg-extra-root-practice-5 |
| Rules-table rows a√b=√(a²b), ⁿ√aᵐ=a^(m/n) (slide + card) | `roots` slide "The rules table"; card `roots` Rules rows | METHOD | KEEP | as above |
| Traps video title slide | `r26-t09-traps` slide 1 | — | KEEP | (video stays) |
| "Roots of small numbers" (√0.09=0.3, √0.9≈0.95, √(1/9)) | `r26-t09-traps` "Roots of small numbers" | CONTENT | REMOVE | 0 real questions with decimal roots; no original question needs it |
| "Between 0 and 1" (x²<x<√x; plug in ¼) | `r26-t09-traps` "Between 0 and 1" | METHOD | KEEP | 2022_autumn_q1_08 (0<a<¼ with −√a, −a, −1/a), 2021_autumn_q1_07 |
| "Compare by squaring" + estimate a root between squares | `r26-t09-traps` "Compare by squaring" | METHOD | KEEP | 2023_autumn_q1_07 (3<x<4: which √), 2022_winter_q2_19 ((√55+1)² between); original q-245, q-246, q-287 |
| "Different roots" (√2 vs ∛3 → 6th power) | `r26-t09-traps` "Different roots" | CONTENT | REMOVE | 0 real questions. (Original q-245 has ∛30 vs √7 but is solved by comparing each to 3 — not needed.) |
| "Conjugates" ((√a+√b)(√a−√b)=a−b, 1/(√2−1)) | `r26-t09-traps` "Conjugates" | CONTENT | KEEP | 2025_autumn_q1_20, 2019_spring_q1_11 (2); original q-298, q-308 |
| "Square of a sum" ((√a+√b)²) | `r26-t09-traps` "Square of a sum" | CONTENT | KEEP | 2022_winter_q2_19, 2024_spring_q2_16; original q-287 |
| Card table "Exam traps": rows 0<x<1 / compare by squaring / conjugates / square of a sum | card `roots` | METHOD | KEEP | as slides |
| Card "Exam traps" row "roots of small numbers" | card `roots` | CONTENT | REMOVE | 0 |
| Card "Exam traps" row "square root vs cube root: 6th power" | card `roots` | CONTENT | REMOVE | 0 |
| Card tips rewritten (largest square, number over a root, never negative + √(x−3), root equations, estimate) | card `roots` tips | METHOD/FIX | KEEP | as slides |
| Guided Q1 ⁴√(9⁶) + video | q-r26-t09-01, solve-q-r26-t09-01 | CONTENT | KEEP | 2023_spring_q2_04 (⁴√2⁸) |
| Guided Q2 largest of 5.2, 3√3, 2√7, √26 + video | q-r26-t09-02, solve-q-r26-t09-02 | METHOD | KEEP | 2023_autumn_q1_07, 2025_spring_q1_06 |
| Guided Q3 √(x+6)=x + video | q-r26-t09-03, solve-q-r26-t09-03 | METHOD | KEEP | 2020_spring_q1_15, 2025_winter_q2_09 |
| Guided Q4 0<x<1, largest of x², x, √x, x³ + video | q-r26-t09-04, solve-q-r26-t09-04 | METHOD | KEEP | 2022_autumn_q1_08 |
| Guided Q5 largest of √3, ⁶√28, ∛5, ⁶√26 + video | q-r26-t09-05, solve-q-r26-t09-05 | CONTENT (type) | REMOVE | 0 |
| Guided Q6 1/(√3−√2) + video | q-r26-t09-06, solve-q-r26-t09-06 | CONTENT | KEEP | 2025_autumn_q1_20, 2019_spring_q1_11 |
| q-242 replaced by √(√81) (index 2.5 root) | q-242 | FIX | KEEP | (original listed below for restore) |
| Stems/solutions in TeX, q-247 and q-246 wording/proof | all T9 questions | FIX | KEEP | — |
| Practice √0.0016 | q-r26-t09-07 | CONTENT (type) | REMOVE | 0 |
| Practice √0.9 closest to | q-r26-t09-08 | CONTENT (type) | REMOVE | 0 |
| Practice order of 0.5², 0.5, √0.5 | q-r26-t09-09 | METHOD | KEEP | 2022_autumn_q1_08 (ordering inside (0,1)) |
| Practice 8^(2/3) | q-r26-t09-10 | CONTENT | KEEP | 2022_autumn_q2_07 |
| Practice ⁴√(x⁸) | q-r26-t09-11 | CONTENT | KEEP | 2023_spring_q2_04, 2019_winter_q1_13 |
| Practice domain of √(2−x) | q-r26-t09-12 | CONTENT (type) | REMOVE | 0 domain questions on the exam |
| Practice √(2x+3)=3 | q-r26-t09-13 | METHOD | KEEP | 2025_winter_q2_09, 2021_autumn_q2_07 |
| Practice largest of 2√11, 3√5, √43, 6.5 | q-r26-t09-14 | METHOD | KEEP | 2023_autumn_q1_07, 2025_spring_q1_06 |
| Practice smallest of ∛4, ⁶√15, √2, ⁶√17 | q-r26-t09-15 | CONTENT (type) | REMOVE | 0 |
| Practice (√7+√5)(√7−√5) | q-r26-t09-16 | CONTENT | KEEP | 2025_autumn_q1_20 |
| Practice (√5+1)² | q-r26-t09-17 | CONTENT | KEEP | 2022_winter_q2_19 |
| Practice 4/(√5−1) | q-r26-t09-18 | CONTENT | KEEP | 2025_autumn_q1_20, 2019_spring_q1_11 |
| Practice √3+√5 vs √15 | q-r26-t09-19 | METHOD | KEEP | 2022_winter_q2_19 |

## TO REMOVE
- Slides: video `r26-t09-traps`, slide "Roots of small numbers"; video `r26-t09-traps`, slide "Different roots" (plus their sidebar labels and the matching lines on the title slide, if any).
- Questions + solution video: q-r26-t09-05 + solve-q-r26-t09-05 (guided numbering 1–6 → 1–5).
- Practice questions: q-r26-t09-07, q-r26-t09-08, q-r26-t09-12, q-r26-t09-15.
- Card rows: card `roots`, table "Exam traps", rows "roots of small numbers" and "square root vs cube root: 6th power".

Counts (table rows): KEEP 32 (incl. 5 FIX) · REMOVE 9 · UNSURE 0.

## ORIGINAL ITEMS REMOVED BY FIXERS (to restore)
- **q-239** (∛9·∛9·∛9 = ?, choices 9/27/3/1) — removed from the core as "same idea as q-238".
- **alg-extra-root-practice-6** ("Evaluate √12 × √27", choices 18/9/36/324) — removed as a duplicate of q-237.
- **q-242** — content replaced. Original: "Evaluate ²·⁵√(√243). Here the fractional root index 2.5 means raising to the power 1/2.5 …" (choices 9/27/3/1, key 3). Now "√(√81) = ?" with the same choices/key.
- Card `roots` tips — original tips "Pull out squares: √72=√36·2=6√2.", "Number over a root: 6/√3=2√3 — ignore the root, then put it back.", "Inside a square root: never negative." replaced by reworded/expanded tips; original Rules row "√ab=√a·√b | a,b≥0" rewritten (same content).
- Video `roots` slides 1, 2, 3, 4, "Multiply & divide", "The rules table": original scripts edited (lines added/changed, "fifteen questions, no videos" removed). Originals in `base-v18.html`.
- Received from T8 (not removed): q-227, alg-extra-exponent-extra-2, alg-extra-exponent-extra-7.
