# Audit T15 - Division & Remainder (additions of the 2026-09 patch)

Sources: `math_patches/t15_CHANGES.md`, `math_patches/t15.py`, `real_exam/quant_real.md` (full text), original course = `course18.json` (pre-patch).
Rule 2 (coordinator): a method is kept when ORIGINAL course questions need it, even without a real-exam match.

| Addition | Where | Class | Verdict | Evidence (real ids / count) |
|---|---|---|---|---|
| "Build a divisor": split into coprime parts, trap 12 = 2·6 | `divisibility` slide 5 + card mem-divisibility row | FIX | KEEP | also real: 2024_autumn_q2_13 (Nir's claim, 6·4 vs 36), 2025_winter_q2_10, 2020_autumn_q1_12 |
| Zebras: nested fractions, multiply the denominators | `divisibility` slide 7 + card "Divisibility stories" | FIX | KEEP | real: 2022_winter_q1_04 (2/3 then 3/4 of the rest), 2021_autumn_q1_17 |
| By 11: one rule (+ − + −), 1,331 and 482 examples | `divisibility` slide 6, card row | FIX | KEEP | original q-440 |
| ÷ instead of ":" on slides 8, 9; "mod"/"≡" removed from solutions | lesson + Q11, q-444, q-448, q-456, Q4, Q14, q-450 | FIX | KEEP | - |
| Plug-in advice made consistent (one failure knocks out, successes prove nothing, avoid 0) | Q4, Q9, Q10, Q13 videos, cards | FIX | KEEP | real: 2024_winter_q2_18, 2019_winter_q1_16 |
| Combine remainders: difference (negative → add divisor); "a and a+b divide by d → b does" | `divisibility` slide 12 + 2 card rows | METHOD | KEEP | 2020_winter_q1_07 (class + parallel class divisible by 4), 2024_spring_q2_05 (combining remainders by 50); original q-436, q-456 |
| New slide "Change the divisor" (10 → 5 keeps remainder; 6 → 4 unknown) | `divisibility` new slide 13 + card row | METHOD | KEEP | 2022_winter_q2_13 (remainder by 3 vs by 6); rule 2: original q-441, q-453, q-435 |
| New slide "Digit sum → remainder" (by 3 or 9) | `divisibility` new slide 11 + card row | METHOD | KEEP (rule 2) | real only weak: 2024_autumn_q2_12 (3k+20 → remainder 2 by 3, small numbers). Rule 2: original alg-extra-unit-t15-3-3 (12345 ÷ 9), q-452 |
| Guided Q5 q-r26-t15-01 (remainder of a − b) + solution video solve-q-r26-t15-01 | theory section | METHOD practice | KEEP | 2020_winter_q1_07, 2024_spring_q2_05 (same combining-remainders skill) |
| New video "More Remainder Tools" - slide "Take away the remainder" (N − r divides by d) | `r26-t15-remainder-tools` slide 2, first half | METHOD | KEEP | 2023_winter_q1_01 (remainder 1 by 2, 3, 4), 2025_spring_q2_02 |
| Same slide, second half: REVERSE question "100 ÷ n leaves 4: how many n?" (n divides 96, n > 4) | `r26-t15-remainder-tools` "Take away the remainder" from line "Now turn it around. The exam loves this one." to the end; card mem-r26-t15-tools row "Known remainder" example | CONTENT | REMOVE | 0 real questions of this type (no real question asks for the divisor from a remainder); no original course question either. The line "The exam loves this one" is false |
| Slide "Counting multiples" (first/last multiple, last k − first k + 1) | tools video slide 3 + card row | METHOD | KEEP | 2020_autumn_q1_12 (divisible by 4 and 6 up to 100), 2024_spring_q2_07, 2023_winter_q2_07; original q-430, q-454 |
| Slide "Units digit": product uses only units digits | tools video slide 4 (first half) + card row | METHOD | KEEP | 2020_winter_q2_05, 2021_spring_q1_09, 2019_spring_q2_16 |
| Same slide: powers repeat (7, 9, 3, 1) | tools video slide 4 (second half) + card row | METHOD | KEEP (rule 2) | 0 real questions on units digit of a power. Rule 2: original alg-extra-unit-t15-3-2 (units digit of 7^4), q-448 |
| Slide "Numbers in a row" (2 in a row → 2, 3 in a row → 6, a³ − a, n² − n, n(n+2) not in a row) | tools video slide 5 + card rows | METHOD | KEEP | 2021_spring_q2_19 (a(a+1), a divisible by 17), 2025_winter_q1_14 ((M−1)(M−2)), 2019_winter_q1_16 (a, a+2, a+4 trap) |
| Slide "Plugging in: the rule" | tools video slide 6 + card tips | METHOD | KEEP | 2024_winter_q2_18, 2021_autumn_q2_14, 2019_winter_q1_16 |
| Guided Q9 q-r26-t15-02 "75 ÷ n leaves 3: how many n?" + solve-q-r26-t15-02 | advanced section, after solve-q-429 | CONTENT (reverse remainder) | REMOVE | 0 real questions of the type |
| q-427 video: ratio replaced by 60% = 3/5 | solve-q-427 slide 2 | FIX | KEEP | - |
| q-430 video: exact count method 1, estimate becomes method 2 | solve-q-430 | METHOD | KEEP | 2020_autumn_q1_12 |
| Practice q-r26-t15-03 (50 ÷ n leaves 2, which could be n) | unit-t15-3 | CONTENT (reverse remainder) | REMOVE | 0 real |
| Practice q-r26-t15-04 (62 ÷ n leaves 6, how many n) | unit-t15-3 | CONTENT (reverse remainder) | REMOVE | 0 real |
| Practice q-r26-t15-05 (multiples of 8 from 50 to 150) | unit-t15-3 | METHOD practice | KEEP | 2020_autumn_q1_12 |
| Practice q-r26-t15-06 (three-digit numbers divisible by 3 and 8) | unit-t15-3 | METHOD practice | KEEP | 2020_autumn_q1_12 (same type) |
| Practice q-r26-t15-07 (remainder of a − b by 9) | unit-t15-3 | METHOD practice | KEEP | 2020_winter_q1_07, 2024_spring_q2_05 |
| Practice q-r26-t15-08 (x leaves 3 by 5 → remainder of x² − 2x) | unit-t15-3 | METHOD practice | KEEP | 2025_winter_q1_14 (remainder of an expression from the remainder of M); original q-443 |
| Practice q-r26-t15-09 (divisible by 18 = 2·9 trap) | unit-t15-3 | FIX practice | KEEP | 2021_autumn_q2_14 (answer 18), 2024_autumn_q2_13 |
| Practice q-r26-t15-10 (digit sum 40 → remainder by 9) | unit-t15-3 | METHOD practice | KEEP (rule 2) | type of original alg-extra-unit-t15-3-3; real only weak (2024_autumn_q2_12) |
| Practice q-r26-t15-11 (2/3 of members, 3/4 of those) | unit-t15-3 | FIX practice | KEEP | 2022_winter_q1_04 (exact type) |
| Practice q-r26-t15-12 (odd n: n² − 1 divisible by 8) | unit-t15-3 | METHOD practice | KEEP | 2022_winter_q1_20 (n² − m² same parity → by 4), 2021_autumn_q2_14. Note: same item as T16 q-r26-t16-12 (duplicate across topics) |
| Practice q-r26-t15-13 (units digit of 3^25) | unit-t15-3 | METHOD practice | KEEP (rule 2) | 0 real; same type as original alg-extra-unit-t15-3-2 |
| Practice q-r26-t15-14 (remainder 1 by 2, 3, 4, 5 → 61) | unit-t15-3 | METHOD practice | KEEP | 2023_winter_q1_01 (exact type) |
| Text: TeX, NITE stems, q-428/q-445/q-448/q-452/alg-extra-1 rewordings | all questions | FIX | KEEP | - |

## TO REMOVE
- Video `r26-t15-remainder-tools`, slide "Take away the remainder": the reverse-question part (script from "Now turn it around. The exam loves this one." through "Check one: a hundred is six times sixteen, plus four. It works." and its boards "100 ÷ n leaves 4…", "100 − 4 = 96…", "and n > 4", divisors of 96, circle, check). Keep the first part (N − r divides by d, 53 example).
- Same video, "Recap" slide: drop ", and $d>r$" only if the reverse part goes (it belongs to the reverse question).
- Card `mem-r26-t15-tools`, row "Known remainder": replace the example "$100\div n$ leaves $4$ → $n$ divides $96$, $n>4$: $8$ values" with a forward example (e.g. 53 leaves 4 by 7 → 49 = 7·7), or drop the row.
- Guided question `q-r26-t15-02` and its solution video `solve-q-r26-t15-02`.
- Practice `q-r26-t15-03`, `q-r26-t15-04`.

## ORIGINAL ITEMS REMOVED OR REPLACED BY THE FIXERS (restore candidates)
- Removed: `alg-extra-unit-t15-3-4` (remainder 3 by 4 and 2 by 5, smallest), `alg-extra-unit-t15-3-6` (smallest number divisible by 8 and 12).
- Replaced slide content (these were wrong or inconsistent rules; replacement is a FIX): `divisibility` slide 5 "By 6, by 15" (now "Build a divisor"; old line "use the same trick for any bigger number"), slide 6 "By 11" (old "outer minus middle" rule), slide 7 "Divisibility stories" (old "divide by four and by five" rule), slide 12 "Combine remainders", recap slide.
- Replaced video lines: Q4/Q9/Q10/Q13 plug-in lines ("recommended route, by far", "use plugging in only if you can't solve it", "plugging in x = 0 is usually fastest"); Q13 "three ways" → "two ways"; solve-q-427 slide 2 (ratio method); solve-q-430 slide 2 (the 1/10 > 1/11 argument is now Method 2).
- Card `mem-divisibility` rewritten (all old rows replaced by the new table).

Counts: KEEP 28 · REMOVE 4 (+1 card-row edit) · UNSURE 0
