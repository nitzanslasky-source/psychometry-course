# Audit T16 - Integers (additions of the 2026-09 patch)

Sources: `math_patches/t16_CHANGES.md`, `math_patches/t16.py`, `real_exam/quant_real.md` (full text), original course = `course18.json` (pre-patch).
Rule 2 (coordinator): a method is kept when ORIGINAL course questions need it, even without a real-exam match.

| Addition | Where | Class | Verdict | Evidence (real ids / count) |
|---|---|---|---|---|
| Wrong rule "smallest product is the divisor" fixed: slide 3 reasons, slide 4 "Smallest case" as memory aid only, slide "Even products" proof first, recap | `consecutive-products` slides 3, 4, 6, recap; card mem-products | FIX | KEEP | real trap exists: 2019_winter_q1_16 (a, a+2, a+4: product by 4? no) |
| New slide "Only a candidate" (1·3·5 vs 7·9·11; cross out, then test a second case) | `consecutive-products` new slide 5; card mem-products second table + tip | FIX / METHOD | KEEP | 2019_winter_q1_16, 2021_spring_q2_19, 2024_winter_q2_18 |
| Guided q-r26-t16-04 (n odd: n(n+2)(n+4) necessarily divisible by 3) + solve-q-r26-t16-04 | theory section after solve-q-464 | FIX practice | KEEP | 2019_winter_q1_16 (three consecutive odd numbers) |
| "Always positive" → "Never negative" (x² can be 0) | `whole-numbers` slide 5 | FIX | KEEP | - |
| q-457 solution/video wording; q-463/q-464 videos give the reason; "What a plug-in proves" slide | solve-q-457, solve-q-463, solve-q-464, `parity` slide 8 + mem-parity | FIX | KEEP | - |
| New slide "Signs of sums" (same signs, mixed signs: bigger size wins, bigger − smaller > 0) + card mem-signs "Add" table | `whole-numbers` new slide 4 | CONTENT/METHOD | KEEP | 2026_spring_q2_10 (a < b, \|b\| < \|a\|), 2024_spring_q2_18 (\|x+y\| = \|x\| − \|y\|), 2025_spring_q1_19, 2020_winter_q2_14; rule 2: original q-465, q-467, q-491 |
| Guided q-r26-t16-01 (x < 0 < y, x + y > 0 → \|y\| > \|x\|) + solve-q-r26-t16-01 | theory after solve-q-457 | practice | KEEP | 2026_spring_q2_10, 2024_spring_q2_18 |
| Practice q-r26-t16-05 (signs of sums) | unit-t16-3 | practice | KEEP | 2023_autumn_q1_01, 2026_spring_q2_10 |
| Practice q-r26-t16-06 (a + b < 0, ab > 0 → both negative) | unit-t16-3 | practice | KEEP | 2024_spring_q2_18, 2023_autumn_q1_01 |
| Practice q-r26-t16-07 (x < y < 0: y − x positive) | unit-t16-3 | practice | KEEP | 2020_winter_q2_14, 2025_winter_q1_01 |
| Odd powers keep the sign; zero neither positive nor negative | `whole-numbers` slide "Never negative" + mem-signs tips | METHOD | KEEP | 2025_winter_q1_18 (x^{2n} = x^{−n}), 2024_spring_q2_08, 2023_autumn_q1_01 |
| New video "Sums of Consecutive Integers" - slide "Count × middle" | `r26-t16-consecutive-sums` slide 2 | METHOD | KEEP | 2019_spring_q1_02 (sum of 3 consecutive = 33), 2020_winter_q2_01; rule 2: alg-extra-unit-t16-3-2, -3-5, -3-7, q-469, q-478, q-484 |
| Slide "Even count" (middle ends in .5) | same video slide 3 | METHOD | KEEP | 2020_winter_q2_01 (cards 3..8 in pairs); rule 2: alg-extra-unit-t16-3-7 (four consecutive evens, sum 44) |
| Slide "Divisible by the count?" (odd count → divides; even count → never, 4a + 6) | same video slide 4 | METHOD | KEEP | 2019_winter_q1_16 (a+b+c of a, a+2, a+4 divisible by 3), 2024_autumn_q2_12 (write the total with one letter: 3k + 20, which total is possible). "Even count never" part: no direct real item |
| Slide "Counting integers" (b − a + 1; evens/odds (b − a)/2 + 1) | same video slide 5 | METHOD | KEEP | 2023_winter_q1_20, 2020_autumn_q1_12, 2024_spring_q2_07; rule 2: alg-extra-unit-t16-3-3 |
| Slide "Squares of neighbors" (b² − a² = a + b) | same video slide 6 + card row + recap line | METHOD | KEEP (rule 2) | 0 real questions on consecutive squares. Rule 2: original q-458, q-468, q-482, q-487 (and removed original q-477) need it |
| Card mem-r26-t16-sums (new) | after solve-q-r26-t16-03 | card | KEEP | as the slides above |
| Guided q-r26-t16-02 (7 consecutive integers, sum 91, largest) + solve-q-r26-t16-02 | theory after the new video | practice | KEEP | 2019_spring_q1_02 |
| Guided q-r26-t16-03 (sum of 4 consecutive integers always even, not ÷4) + solve-q-r26-t16-03 | theory | practice | KEEP | 2019_winter_q1_16 ("necessarily" property of a consecutive sum), 2024_autumn_q2_12 |
| Practice q-r26-t16-08 (5 consecutive, sum 85) | unit-t16-3 | practice | KEEP | 2019_spring_q1_02 |
| Practice q-r26-t16-09 (which could be the sum of 4 consecutive: 26) | unit-t16-3 | practice | KEEP | 2024_autumn_q2_12, 2019_spring_q1_12 (same "which could be the total" type) |
| Practice q-r26-t16-10 (integers from −5 to 20) | unit-t16-3 | practice | KEEP | 2020_autumn_q1_12, 2023_winter_q1_20 |
| Practice q-r26-t16-14 (10 consecutive integers, sum 5) | unit-t16-3 | practice | KEEP | 2019_spring_q1_02 (count × middle) |
| Practice q-r26-t16-15 (odd integers from 11 to 59) | unit-t16-3 | practice | KEEP | 2020_autumn_q1_12; original alg-extra-unit-t16-3-3 |
| Odd product ⇔ every factor odd | `parity` slide 6, recap, mem-parity tip | METHOD | KEEP | 2020_spring_q1_04 (a^b + 1 = 2c → a odd), 2023_winter_q1_06 |
| New slide "Count the twos" (m²(n+1)/8 vs m(n+1)/8) | `consecutive-products` new slide | METHOD | KEEP | 2024_autumn_q2_03 (x^{x+1}/2^x), 2021_autumn_q2_14, 2022_autumn_q2_05 |
| Practice q-r26-t16-13 (which is necessarily an integer) | unit-t16-3 | practice | KEEP | 2022_autumn_q2_05, 2023_winter_q1_06 |
| Practice q-r26-t16-11 ((n+1)(n+2)(n+3): only 6) | unit-t16-3 | FIX practice | KEEP | 2021_spring_q2_19 |
| Practice q-r26-t16-12 (odd n: n² − 1 by 8; n = 1 gives 0) | unit-t16-3 | FIX practice | KEEP | 2022_winter_q1_20. Note: duplicate of T15 q-r26-t15-12 |
| Plug-in rules on cards ("disprove, not prove"; "check the choices give different values") | mem-parity, mem-consecutive, `consecutive-integers` slide 4 | METHOD | KEEP | 2024_winter_q2_18, 2019_winter_q1_16 |
| Text: TeX, ÷, stacked givens; q-460, q-473, q-465, q-471, q-461, q-463 stems; q-489, q-471, q-478, q-469 solutions | all questions | FIX | KEEP | - |

## TO REMOVE
- Nothing. (Every addition is either a fix, has real evidence, or is needed by original course questions.)

## ORIGINAL ITEMS REMOVED OR REPLACED BY THE FIXERS (restore candidates)
- Removed: `q-477` (a, b, c consecutive, c² − a² = 48, b = ?).
- Replaced slide content: `consecutive-products` slide 4 "Just plug in" (now "Smallest case"; old rule "plug in the smallest numbers - the product is the divisor" was false), slide 3 line "Check yourself with other numbers - it always works", slide "Even products", recap; `whole-numbers` slide 5 title "Always positive"; `parity` slide 8 "Three plug-ins" (now "What a plug-in proves"); card mem-products rewritten.
- Changed question content (not only wording): `q-460` (stem and all four choices rewritten; key still 4), `q-473` (stem flipped to "necessarily even", choices now combinations), `q-465` ("number line" wording removed), `q-489` solution rewritten (old argument was wrong).

Counts: KEEP 31 · REMOVE 0 · UNSURE 0
