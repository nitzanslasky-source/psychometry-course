# Audit T18 - Exercises with Letters (additions of the 2026-09 patch)

Sources: `math_patches/t18_CHANGES.md`, `math_patches/t18.py`, `real_exam/quant_real.md` (full text), original course = `course18.json` (pre-patch).
Rule 2 (coordinator): a method is kept when ORIGINAL course questions need it, even without a real-exam match.
Real letter puzzles found (number_properties / divisibility_remainders): 2022_autumn_q1_15, 2024_autumn_q1_15, 2025_autumn_q1_06, 2019_spring_q2_16, 2023_spring_q2_09, 2025_spring_q1_13, 2022_winter_q1_07, 2023_winter_q1_15, 2024_winter_q1_19, 2019_winter_q1_17, 2026_spring_q2_12, 2025_winter_q1_06 (12 items).

| Addition | Where | Class | Verdict | Evidence (real ids / count) |
|---|---|---|---|---|
| "B + something = B → 0" only in the ones column | `digit-puzzles` slide 4; Q1, Q4 videos | FIX | KEEP | - |
| New slide "Carries" (carry 0/1 for two numbers, up to 2-3 for 3-4 numbers; middle column X + Y ends in X → Y = 0 or 9) | `digit-puzzles` new slide 5 | METHOD | KEEP | 2025_winter_q1_06 (AB + AB = CDA), 2022_autumn_q1_15 (AAA × 3 = EDCB), 2023_spring_q2_09; rule 2: original q-526, q-527 |
| Leading-digit rule: "two numbers" + four 3-digit numbers can reach 3996 | leading-digit slide | FIX | KEEP | original q-527 |
| Q7 video confusing line deleted; Q9 method 2 rewritten; q-536, q-532 solutions | solve-q-518 (Q7), solve-q-520 (Q9) slide 3, q-536, q-532 | FIX | KEEP | - |
| The 4 steps: "check the leftmost digit and the size"; "plug in numbers or the choices" | `digit-puzzles` slide 2 | METHOD | KEEP | 2019_spring_q2_16 (35A × 4B = 15CC5: size), 2026_spring_q2_12 (A1 × A1 = 1BB), 2025_spring_q1_13 |
| Bar notation explained and used everywhere | "What letters mean" slide, all stems | FIX | KEEP | - |
| Plug-in slide: unlike test numbers, third number; "asked for one letter? plug in the choices" | `digit-puzzles` plug-in slide | METHOD | KEEP | 2025_spring_q1_13 (A − B = ?), 2022_winter_q1_07 (A = ?) |
| Minus → plus: also division → multiplication | minus → plus slide | METHOD | KEEP | 2025_spring_q1_13, 2024_winter_q1_19 (subtraction puzzles); rule 2: q-518, q-539 (division) |
| Algebraic-form slide: when to use each route | algebraic-form slide, recap | METHOD | KEEP | 2025_autumn_q1_06 (AB + BA = 11(A+B)), 2023_winter_q1_15, 2019_winter_q1_17 |
| New video "Number Facts for Letter Puzzles" - slide "Repdigits" (AA = 11A, AAA = 3·37·A, BBBB ÷ BB = 101) | `r26-t18-facts` slide 2 + card rows | METHOD | KEEP | 2022_autumn_q1_15 (AAA × 3), 2024_winter_q1_19 (AAB − BAA); rule 2: q-516, q-518, q-536, q-539, alg-extra-unit-t18-3-5 |
| Slide "Reversals" (AB ± BA, ABC − CBA = 99(A − C), multiples of 99) | `r26-t18-facts` slide 3 + card rows | METHOD | KEEP | 2025_spring_q1_13 (AB − BA = 27), 2025_autumn_q1_06 (AB + BA), 2024_winter_q1_19 (AAB − BAA = 99); rule 2: q-514, q-524, q-532 |
| Slide "Products" (ones digits decide; digit count of a product; estimating squares) | `r26-t18-facts` slide 4 + card rows | METHOD | KEEP | 2019_spring_q2_16, 2026_spring_q2_12, 2020_winter_q2_05; rule 2: q-517, q-536, alg-extra-unit-t18-3-3 |
| Slide "Powers: ones digit" (cycles 2, 4, 8, 6; 2^50) | `r26-t18-facts` slide 5 + card row "Ones digits of powers repeat" + card tip "The ones digit of 2^50…" + recap line "Powers: the ones digits repeat in a cycle" | CONTENT | REMOVE | 0 real questions on the ones digit of a power; no original T18 question needs it; already taught in T15 (tools video, kept there by rule 2) |
| Slide "Largest and smallest" (with a given digit sum) | `r26-t18-facts` slide 6 + card rows | METHOD | KEEP | 2025_autumn_q1_05 (two-digit, digit sum 5), 2024_autumn_q2_06; rule 2: q-529 |
| Card mem-r26-t18-facts (new) | after the video | card | KEEP (minus the power rows) | - |
| Guided Q10 q-r26-t18-01 (2A6 + B8 = 3A4, carry trap, B = 9) + solve video | advanced section | practice | KEEP | 2025_winter_q1_06, 2022_autumn_q1_15 |
| Guided Q11 q-r26-t18-02 (which could be ABC − CBA: 495) + solve video | advanced section | practice | KEEP | 2024_winter_q1_19 (AAB − BAA = 99), 2025_spring_q1_13 |
| Guided Q12 q-r26-t18-03 (which could be A3 × B7: 851; ones digit + size) + solve video | advanced section | practice | KEEP | 2019_spring_q2_16, 2026_spring_q2_12 |
| Practice q-r26-t18-04 (A8 + A8 + A8 = 1A4, carry of 2) | unit-t18-3 | practice | KEEP | 2022_autumn_q1_15 (AAA × 3: carries of 2) |
| Practice q-r26-t18-05 (4AB + CB = 5A0, B + C) | unit-t18-3 | practice | KEEP | 2025_winter_q1_06, 2023_spring_q2_09 |
| Practice q-r26-t18-06 (how many digits can a 3-digit × 2-digit product have) | unit-t18-3 | CONTENT (question type) | REMOVE | 0 real questions ask for the digit count of a product (the size check is only a step inside 2019_spring_q2_16). The idea for sums is already covered by original q-521 |
| Practice q-r26-t18-07 (ones digit of A7 × B3 × C9) | unit-t18-3 | practice | KEEP | 2019_spring_q2_16, 2020_winter_q2_05 |
| Practice q-r26-t18-08 (ones digit of 2^50) | unit-t18-3 | CONTENT | REMOVE | 0 real; T15 has the same type (q-r26-t15-13 and original alg-extra-unit-t15-3-2) |
| Practice q-r26-t18-09 (AAA ÷ 37 = 1A) | unit-t18-3 | practice | KEEP | 2022_autumn_q1_15 (repdigit AAA); original q-516 |
| Practice q-r26-t18-10 (ABC − CBA = 693, B = A + C) | unit-t18-3 | practice | KEEP | 2024_winter_q1_19 |
| Rewritten extras 2 (A + B instead of A:B) and 7 (smallest A, carry) | alg-extra-unit-t18-3-2, -3-7 | FIX | KEEP | 2022_winter_q1_07 (A + B = 9 with AB/BA) |
| Text: "A, B and C represent digits. Given: …" standard stems, bar, "ones digit", TeX solutions | all questions | FIX | KEEP | - |

## TO REMOVE
- Video `r26-t18-facts`, slide "Powers: ones digit" (whole slide); in the same video's "Recap" slide the board line "Powers: the ones digits repeat in a cycle"; remove "Powers: ones digit" from the sidebar.
- Card `mem-r26-t18-facts`: row "Ones digits of powers repeat" and the tip "The ones digit of $2^{50}$: …".
- Practice `q-r26-t18-06`, `q-r26-t18-08`.

## ORIGINAL ITEMS REMOVED OR REPLACED BY THE FIXERS (restore candidates)
- Removed: `alg-extra-unit-t18-3-1` (digit sum 11, reversing makes it 27 smaller), `alg-extra-unit-t18-3-4` (how many three-digit numbers from 2, 5, 8 - removed as "counting is T28").
- Changed question content: `alg-extra-unit-t18-3-2` (asked A:B, now asks A + B), `alg-extra-unit-t18-3-7` (now "smallest possible A"), q-514 (Q3) stem changed to "which necessarily divides AB + BA" with "nonzero digits", q-519 (Q8) wording.
- Replaced slide/video content: `digit-puzzles` slide 4 line "B plus something equals B, so it's zero"; leading-digit rule; algebraic-form line "plugging in is faster most of the time"; Q7 (solve-q-518) video line "With a five here we'd use the five-rule"; Q9 (solve-q-520) method 2 "cube sits on the tens digit".

Counts: KEEP 24 · REMOVE 3 · UNSURE 0
