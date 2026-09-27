# Audit T11 — Laws of Exponents & Roots, Advanced (report only)

Sources: `math_patches/t11_CHANGES.md`, `math_patches/t11.py`, fixed `real_exam/quant_real.md`; original course from
`base-v18.html` / git `8965af3`.

Exam facts used: nested roots/fractional powers (2020_spring_q2_02, 2024_winter_q1_07, 2019_winter_q1_13), undoing a power
(2020_spring_q1_15, 2023_winter_q1_05, 2021_autumn_q2_07), conjugates (2025_autumn_q1_20 = 1/(√5−2)-style sum,
2019_spring_q1_11 = (1−a)/(1+√a)), product = 0 (2024_winter_q2_06), power = 1 / parity cases (2025_winter_q1_18),
(√55+1)² (2022_winter_q2_19), 0<a<1 ordering (2022_autumn_q1_08). **0** real questions on: decimal roots, huge-power
ordering, roots of different order.

| Addition | Where | Class | Verdict | Evidence |
|---|---|---|---|---|
| Q4 video "2 and 4 pattern" limited to positive whole numbers + fractions warning; q-306 solution | solve-q-291 slide 3; q-291, q-306 | FIX | KEEP | 2026_spring_q1_06 |
| q-312 solution ("a = −1 only" overclaim) | q-312 | FIX | KEEP | — |
| Domains added (q-297, q-298, q-302); ambiguous "1 < x, y" / "0 < x, y" stacked | q-297, q-298, q-302, q-291, q-318 | FIX | KEEP | — |
| Slide 1 "Most rules here you already know"; recap "Five questions next" | `advanced-powers` slides 1, "Recap" | FIX | KEEP | — |
| Slide "Patterns to spot": (x+y)², aᵇ=bᵃ ⇒ 2 and 4, copies of equal powers | `advanced-powers` slide 3 | METHOD | KEEP (rule 2) | (x+y)² and 2&4 are original (q-292, q-291, q-306); copies needed by original q-293 |
| Tools video title slide | `r26-t11-tools` slide 1 | — | KEEP | — |
| "Root of a root" (multiply indices; bring a factor inside first) | `r26-t11-tools` "Root of a root" | METHOD | KEEP | 2020_spring_q2_02; original q-297, q-309 |
| "Undo a power" (raise to the reciprocal power) | `r26-t11-tools` "Undo a power" | METHOD | KEEP | 2020_spring_q1_15, 2023_winter_q1_05; original q-301 |
| "Conjugates" both ways | `r26-t11-tools` "Conjugates" | METHOD | KEEP | 2019_spring_q1_11, 2025_autumn_q1_20; original q-298, q-308 |
| "Product = 0" (never divide by √x) | `r26-t11-tools` "Product = 0" | METHOD | KEEP | 2024_winter_q2_06, 2020_spring_q1_15; original q-299 |
| "'Or' claims" (power = 1 cases; kill "A or B" with one case) | `r26-t11-tools` "\"Or\" claims" | METHOD | KEEP | 2025_winter_q1_18; original q-290 (needs it) |
| Tools recap | `r26-t11-tools` "Recap" | — | KEEP | — |
| Old Q3 (q-290) moved after the tools lesson; guided renumbering | T11 flow | FIX | KEEP | — |
| Guided Q11 1/(√5−2) − 1/(√5+2) + video | q-r26-t11-01, solve-q-r26-t11-01 | CONTENT | KEEP | 2025_autumn_q1_20 (same structure) |
| Guided Q15 x>0, ∛(x√x)=2 + video | q-r26-t11-02, solve-q-r26-t11-02 | METHOD | KEEP | 2020_spring_q1_15, 2020_spring_q2_02 |
| Q9 video new Method 1 "Clear the root" | solve-q-296 slide 3 | METHOD | KEEP | 2019_spring_q1_11, 2025_autumn_q1_20 |
| Q10/Q12/Q13/Q14 video edits (drop "favourite is four"; product-is-0 opening; 108 = 4·27 check; (1/16)^(−½) check) | solve-q-297, -299, -300, -301 | FIX | KEEP | — |
| New card: "Tools" table (9 rows) | `mem-r26-t11-advanced` | METHOD | KEEP | as the tools slides |
| Card "From topics 8 to 10": rows equal powers added; between 0 and 1; square of a sum; power equation | `mem-r26-t11-advanced` | METHOD | KEEP | q-293 (rule 2); 2022_autumn_q1_08; 2022_winter_q2_19; 2023_autumn_q2_04 |
| Card "From topics 8 to 10" row "compare powers: make the exponents equal" | `mem-r26-t11-advanced` | CONTENT | REMOVE | 0 |
| Card "From topics 8 to 10" row "different roots: raise to a common power" | `mem-r26-t11-advanced` | CONTENT | REMOVE | 0 |
| Card tips (two routes, check choices differ, √a+√b≠√(a+b), estimate with squares) | `mem-r26-t11-advanced` tips | METHOD | KEEP | 2020_winter_q2_03, 2023_autumn_q1_07; original q-310 |
| Text: TeX, plug-in checks in q-288, q-293, q-297, q-298, q-304, q-305, q-311, q-314, q-321; q-303, q-317 distractor, stacked givens, NITE stems | T11 questions | FIX | KEEP | — |
| Practice (0.2)³·10⁴/√0.0016 | q-r26-t11-03 | CONTENT (type) | REMOVE | 0 decimal root/power questions |
| Practice 2/(√7+√5) | q-r26-t11-04 | CONTENT | KEEP | 2025_autumn_q1_20, 2019_spring_q1_11 |
| Practice 9ˣ·27ˣ = 1/3 | q-r26-t11-05 | METHOD | KEEP | 2024_spring_q1_02, 2023_autumn_q2_04, 2024_autumn_q1_16 |
| Practice a+b=10, ab=9 → √a+√b | q-r26-t11-06 | CONTENT | KEEP | 2022_winter_q2_19, 2024_spring_q2_16 |
| Practice order of 2¹⁰⁰, 10³⁰, 3⁶⁰ | q-r26-t11-07 | CONTENT (type) | REMOVE | 0 |
| Practice 0<x<1: largest of ∛x, x^(−½), x⁻², x³ | q-r26-t11-08 | METHOD | KEEP | 2022_autumn_q1_08 |
| Practice a≠1, aᵇ=1 → "b=0 or a=−1" | q-r26-t11-09 | METHOD | KEEP | 2025_winter_q1_18; original q-290 |
| Practice x√x = 4√x → 0 or 4 | q-r26-t11-10 | METHOD | KEEP | 2024_winter_q2_06, 2020_spring_q1_15; original q-299 |
| Practice chain of conjugates = 1 | q-r26-t11-11 | CONTENT | KEEP | conjugate simplification: 2025_autumn_q1_20, 2019_spring_q1_11 (the telescoping chain itself is harder than any real item) |
| Practice √(2√(2√2)) = 2^(7/8) | q-r26-t11-12 | METHOD | KEEP | 2020_spring_q2_02; original q-309 |

## TO REMOVE
- Practice questions: q-r26-t11-03, q-r26-t11-07.
- Card rows: `mem-r26-t11-advanced`, table "From topics 8 to 10", rows "compare powers: make the exponents equal" and "different roots: raise to a common power".
- (No video or slide of T11 is removed.)

Counts (table rows): KEEP 29 (incl. 7 FIX) · REMOVE 4 · UNSURE 0.

## ORIGINAL ITEMS REMOVED BY FIXERS (to restore)
- **alg-extra-unit-t11-3-1** (5⁹/5⁶), **3-3** (3ˣ⁺¹ = 3⁷), **3-5** ((5x)³/25x²), **3-6** (2¹⁶ vs 4⁷) — removed from practice as T8-level templates.
- Video `advanced-powers`, slide 3 **"Laws + identities"** — replaced by "Patterns to spot". Original script: "Some questions hide a multiplication formula inside an exponent question. | (x+y)² = x²+y²+2xy | Once an exponent law gives you x plus y, this formula hands you x squared plus y squared — directly. | Circle x²+y² and 2xy | No need to find x and y separately…" (the (x+y)² idea survives as pattern 1).
- Video `advanced-powers`, slide 1 line "No new rules here — these questions combine the ones you already know." replaced; "Recap" "Six questions next." replaced.
- Video solve-q-296, slide **"Method 2 · Multiply the denominators"** — dropped (the video now has "Clear the root" + "Match the denominators").
- Video solve-q-299, slide **"Open the brackets"** — replaced by "Product equals zero" (the original √x·√x − 3√x → x = 3√x route removed).
- Video solve-q-297, slide 3 — line "The lesson's favourite is four — but here four gives root eight…" removed.
- Video solve-q-301 — "Last question." changed to "Question fourteen." (order change).
- **q-290** (old guided Question 3) moved to the end of Section B as Question 16; all guided numbers changed.
- **q-317** distractor 2/6 replaced by 3/2; **q-310** choices reworded ("Only when…", "Always"; original "No additional condition is needed"); **q-312** choices rewritten as full equations.
