# Audit T12 — Inequalities (report only)

Sources: `math_patches/t12_CHANGES.md`, `math_patches/t12.py`, fixed `real_exam/quant_real.md` (the previously cut
inequality stems now read in full, e.g. 2025_spring_q2_06 "a<10, 5<b, D=a−b", 2024_spring_q1_03 "a<2b, b<5",
2020_spring_q2_14 "b<2a, 3a<2b", 2021_spring_q1_15 "A−B<C", 2022_autumn_q1_08 "0<a<¼"); original course from
`base-v18.html` / git `8965af3`.

The real exam has 35 inequality/absolute-value questions plus related items in other groups; every T12 addition maps to
real question types, so nothing in T12 is proposed for removal.

| Addition | Where | Class | Verdict | Evidence |
|---|---|---|---|---|
| "A minus flips it" demo rebuilt (−12<−4 ÷ −4 → 3>1; −2x<6 two ways; check x=0) | `inequalities` slide 4 | FIX | KEEP | original q-322, alg-extra-unit-t12-3-1 |
| "Cross-multiply" removed ("multiply by a positive number") | `inequality-systems` slide 6; solve-q-328 slide 2; solve-q-330 slide 2 | FIX | KEEP | — |
| Q5 video: why x⁴<x⁵ gives x>1 | solve-q-326 | FIX | KEEP | — |
| Q20 (q-337) false start removed; q-350 unfinished line fixed | q-337, q-350 solutions | FIX | KEEP | — |
| Lesson 1 recap "× or ÷ by a negative" | `inequalities` "Recap" | FIX | KEEP | — |
| Worked "x² on the big side" example (−2x² ≤ −32 → x ≥ 4 or x ≤ −4) + recap line | `inequality-systems` slide 6 "x² inequalities" | FIX | KEEP | the big-side rule was already on the original slide; original q-345 is exactly this example |
| Signs lesson title slide | `r26-t12-signs` slide 1 | — | KEEP | — |
| "Between 0 and 1" (x²<x<√x<1<1/x; x>1 reversed; negatives: −½) | `r26-t12-signs` "Between 0 and 1" | METHOD | KEEP | 2022_autumn_q1_08, 2021_autumn_q1_07, 2023_spring_q1_08; original alg-extra-unit-t12-3-3, q-347 |
| "Reciprocals" (same sign flips, different signs no flip) | `r26-t12-signs` "Reciprocals" | CONTENT | KEEP | 2026_spring_q1_17 (−½<1/x<½ ⇒ x<−2 or x>2), 2020_autumn_q1_13; original alg-extra-unit-t12-3-5, 3-7 |
| "Sign table" for products/fractions | `r26-t12-signs` "Sign table" | METHOD | KEEP | 2025_autumn_q1_16 ((21−3a)/(2a+1)<0), 2023_winter_q2_10 (|x|(x−2)≤0); original q-332, q-352, q-354 |
| "Must, could, cannot" (+ numbers to try) | `r26-t12-signs` "Must, could, cannot" | METHOD | KEEP | 2020_autumn_q2_19, 2021_autumn_q1_16, 2021_spring_q1_15, 2024_winter_q2_05, 2020_spring_q2_14 |
| Signs recap | `r26-t12-signs` "Recap" | — | KEEP | — |
| Combining lesson title slide | `r26-t12-combining` slide 1 | — | KEEP | — |
| "Add them" (same direction) | `r26-t12-combining` "Add them" | METHOD | KEEP | 2020_winter_q2_14 (a+b choices), 2024_spring_q1_03; original q-350 |
| "Never subtract" end from end (flip b, then add) | `r26-t12-combining` "Never subtract" | METHOD | KEEP | 2025_spring_q2_06 (D=a−b, exact range D<5), 2020_winter_q2_14 (a−b<−11) |
| "Multiply" (four corners) | `r26-t12-combining` "Multiply" | METHOD | KEEP | 2020_autumn_q2_19 (a<1, b<1 ⇒ ab can be anything), 2019_winter_q2_07; original q-336 |
| "Range of x²" (0 inside the range) | `r26-t12-combining` "Range of x²" | METHOD | KEEP | 2020_spring_q1_18 (2x+1≤0 ⇒ x²≥¼), 2022_winter_q1_15 (A=−x²+7 ⇒ A≤7) |
| Combining recap | `r26-t12-combining` "Recap" | — | KEEP | — |
| Existing video additions: x/(x+1) grows (Q11), pointer to sign table (Q13), chain on a number line (Q15), numbers-to-try board line (Q20) | solve-q-330, -332, -334, -337 | METHOD | KEEP | 2020_autumn_q1_13; 2025_autumn_q1_16; 2024_spring_q1_03; 2021_autumn_q1_16 |
| Guided Q9 −1<x<0: greatest of x, x², x³, 1/x + video | q-r26-t12-01, solve-q-r26-t12-01 | METHOD | KEEP | 2022_autumn_q1_08, 2023_spring_q1_08 |
| Guided Q10 (x−2)(x+5)<0 + video | q-r26-t12-02, solve-q-r26-t12-02 | METHOD | KEEP | 2023_winter_q2_10, 2025_autumn_q1_16 |
| Guided Q17 a>b, c>d: necessarily + video | q-r26-t12-03, solve-q-r26-t12-03 | METHOD | KEEP | 2020_winter_q2_14, 2021_spring_q1_15 |
| Guided Q18 range of x−y + video | q-r26-t12-04, solve-q-r26-t12-04 | METHOD | KEEP | 2025_spring_q2_06, 2020_winter_q2_14 |
| Card `mem-inequalities`: move-across example, "multiply by an unknown only if you know its sign", x²>a example | `mem-inequalities` rows | FIX/METHOD | KEEP | 2020_autumn_q2_19; original q-331, q-345 |
| New card "Inequality traps" (combining/ranges; signs & special numbers; question words; 2 tips) | `mem-r26-t12-traps` | METHOD | KEEP | as the two lessons |
| Text: TeX everywhere, stacked conditions, q-323/q-325/q-338 choices as full ranges/sentences, "most precise range" | T12 questions | FIX | KEEP | — |
| Practice range of a−b with b negative | q-r26-t12-05 | METHOD | KEEP | 2025_spring_q2_06 |
| Practice x² from −3<x<2 | q-r26-t12-06 | METHOD | KEEP | 2020_spring_q1_18, 2022_winter_q1_15 |
| Practice x+y>10, x−y>4 ⇒ x>7 | q-r26-t12-07 | METHOD | KEEP | 2020_winter_q2_14, 2024_spring_q1_03 |
| Practice x>1: smallest of 1/x, 1/x², √x, x | q-r26-t12-08 | METHOD | KEEP | 2021_autumn_q1_07 |
| Practice (x+1)/(x−4)<0 integer count | q-r26-t12-09 | METHOD | KEEP | 2025_autumn_q1_16 |
| Practice x<y<0 "could be true" | q-r26-t12-10 | METHOD | KEEP | 2026_spring_q2_10, 2023_autumn_q1_01 |
| Practice range of ab with negative ends | q-r26-t12-11 | METHOD | KEEP | 2020_autumn_q2_19; original q-336 |
| Practice a>b>0 "cannot be true" with reciprocals | q-r26-t12-12 | METHOD | KEEP | 2026_spring_q1_17; original alg-extra-unit-t12-3-7 |

## TO REMOVE
- Nothing. Every T12 addition matches real exam question types.

Counts (table rows): KEEP 34 (incl. 7 FIX) · REMOVE 0 · UNSURE 0.

## ORIGINAL ITEMS REMOVED BY FIXERS (to restore)
- **q-340** ("x is an integer. Given x² < 25 and 3x + 9 < 0. What is x?", choices −2/−3/−4/−5) — removed as a near-duplicate of q-339.
- Video `inequalities`, slide 4 **"A minus flips it"** — original demo replaced. Original script: "…Write ':(−4)' under both sides, then '3 > 1' … But on the exam, I recommend you don't multiply by a minus at all … Move each number to the other side: write '4 < 12' …" (ending "1 < 3 … same answer").
- Video `inequality-systems`, slide 6 "x² inequalities" — original "Cross-multiply" lines replaced; worked example added.
- Video solve-q-328, slide 2 — original title "Cross-multiply, then the rule" and cross-multiply lines replaced ("Multiply by 6, then the rule").
- Video solve-q-330, slide 2 — original "Cross-multiply the first/second" draw notes and line replaced.
- Card `mem-inequalities` — original rows "Tip: move x to the side where it stays positive | no flip needed" and "x²>a | x>√a or x<−√a (outside the roots)" replaced by versions with examples.
- **q-323** choices replaced (original "0 / 12 / 1 / Any value", key "Any value"); **q-325** choice 3 (original "No value of x (empty set)"); **q-338** choices reworded; **q-337**, **q-350** solution texts replaced.
- Guided numbering: old Q9–Q16 are now Q11–Q16, Q19, Q20.
