# Audit T20 - Algebraic Understanding (additions of the 2026-09 patch)

Sources: `math_patches/t20_CHANGES.md`, `math_patches/t20.py`, `real_exam/quant_real.md` (full text), original course = `course18.json` (pre-patch).
Rule 2 (coordinator): a method is kept when ORIGINAL course questions need it, even without a real-exam match.
Searched the real exam for "worst case / to be sure / pigeonhole" questions (drawing socks, "necessarily exist two…"): 0 found.

| Addition | Where | Class | Verdict | Evidence (real ids / count) |
|---|---|---|---|---|
| "Can be true" → "could be true"; "not necessarily true" added; q-581 "cannot be true" | slides, card, stems | FIX | KEEP | real wording: 2021_spring_q1_15 ("not necessarily true") |
| Old Q3 video: false triangle line replaced by algebra (a+b)² = c² + 2ab; q-585 solution | solve-q-579, q-585 | FIX | KEEP | - |
| Main lesson slide "Three tools" (plug in, test the answers, algebra) | `algebraic-understanding` new slide 2 | METHOD | KEEP | 2024_spring_q2_03, 2020_autumn_q2_19, 2019_spring_q1_15 |
| Slide "Must, could, cannot" (T1 reminder + "not necessarily true") | new slide 3 | FIX | KEEP | 2021_spring_q1_15, 2020_winter_q1_07 ("cannot be") |
| Slide "Which numbers?" (one number per region, try a = b, second number if two survive) | new slide 4 | METHOD | KEEP | 2023_spring_q1_08, 2020_autumn_q2_19, 2026_spring_q1_06 (x, y from 2, 3, 4) |
| Slide "Between 0 and 1" (x² < x < √x < 1 < 1/x; negatives; one number decides "largest for every x") | new slide 5 | METHOD | KEEP | 2021_autumn_q1_07 (1 < x < 2 largest), 2020_spring_q1_18, 2023_spring_q1_08 |
| Slide "Integer gaps" (strictness, n increasing integers: last ≥ first + n − 1, test extreme choices first) | new slide 6 | METHOD | KEEP | 2022_autumn_q1_18 (piles differ by < 3), 2024_spring_q1_03; rule 2: q-577, q-582, q-584 |
| Slide "Scaling" general rule (x² = a³ → factor^(3/2)) | new slide 7; solve-q-578 end | METHOD | KEEP | 2025_winter_q2_09 (√x = 2√y → x² = 16y²), 2019_winter_q1_13; rule 2: q-578, q-589 |
| Slide "Connect topics": Pythagoras replaced by algebra c² = a² + b² → c > a, c > b; "three can't all be bigger than one" | new slide 8 | FIX | KEEP | rule 2: q-579, q-585 |
| Recap slide | new slide 9 | - | KEEP | - |
| New video "Counting Integers & Pigeonhole" - slides "From a to b", "Strictly between", "Only odd or even" (incl. letters in the choices: plug in small numbers) | `r26-t20-counting` slides 2-4 + card rows | METHOD | KEEP | 2023_winter_q1_20 (strictly between 10 and 12), 2020_autumn_q1_12, 2024_spring_q2_07; rule 2: q-586, q-588 |
| Slide "Pigeonhole" (13 numbers, 12 remainders) | `r26-t20-counting` slide 5 + card row | METHOD | KEEP (rule 2) | 0 real; needed by original q-583 (and q-590) |
| Slide "To be sure" (worst luck first, then one more; socks) | `r26-t20-counting` slide 6 + recap line + card row | CONTENT | REMOVE | 0 real "to be sure / worst case drawing" questions; no original course question of this type |
| Card mem-r26-t20-counting (new) | after the video | card | KEEP minus the "to be sure" row | - |
| Guided Q1 q-r26-t20-01 (x > y > 0: which must be true; two plug-ins) + solve video | section `understanding` | practice | KEEP | 2020_winter_q2_14, 2024_spring_q1_03, 2020_autumn_q2_19 |
| Guided Q2 q-r26-t20-02 (−1 < x < 0: smallest) + solve video | `understanding` | practice | KEEP | 2021_autumn_q1_07, 2023_spring_q1_08 |
| Guided Q7 q-r26-t20-03 (odd numbers between 20 and 80) + solve video | `understanding` | practice | KEEP | 2023_winter_q1_20, 2020_autumn_q1_12 |
| Guided Q8 q-r26-t20-04 (socks: smallest number to be sure of a pair) + solve video | `understanding` | CONTENT | REMOVE | 0 real |
| Old Q1 (q-577) video: key step on the board, extreme choices first | solve-q-577 | METHOD | KEEP | 2022_autumn_q1_18 |
| Old Q4 (q-580) stem "all greater than 1"; "Last question" lines moved | q-580, solve-q-580 | FIX | KEEP | - |
| Practice q-r26-t20-05 (0 < x < 1: smallest → x²) | unit-t20-2 | practice | KEEP | 2021_autumn_q1_07, 2020_spring_q1_18 |
| Practice q-r26-t20-06 (x < y < 0: x² > y²) | unit-t20-2 | practice | KEEP | 2026_spring_q2_10, 2024_spring_q2_04 |
| Practice q-r26-t20-07 (integers with 10 < x² < 100 → 12) | unit-t20-2 | practice | KEEP | 2024_spring_q2_07 (count squares up to 100), 2020_spring_q1_18 (negative values of x) |
| Practice q-r26-t20-08 (even numbers from 2n to 8n → 3n + 1) | unit-t20-2 | practice | KEEP | 2019_spring_q1_15, 2022_winter_q1_19 (letters in the choices); original q-588 type |
| Practice q-r26-t20-09 (socks: to be sure of two blue) | unit-t20-2 | CONTENT | REMOVE | 0 real |
| Practice q-r26-t20-10 (x³ = y², y × 8 → x × 4) | unit-t20-2 | practice | KEEP | 2025_winter_q2_09; original q-578 |
| Practice q-r26-t20-11 (formula structure: taxi price → n/d) | unit-t20-2 | practice of an original type | KEEP | original q-580 type; real closest 2022_winter_q1_19, 2019_spring_q1_15 (build the formula from a story) |
| Practice q-r26-t20-12 (x² < x → x³ < x²) | unit-t20-2 | practice | KEEP | 2020_spring_q1_18, 2023_spring_q1_08; original q-498 type (T17) |
| Text: TeX, stacked conditions, q-585 fraction bars, q-586 wording, plug-in first in q-584/q-586/q-588, extras | all questions | FIX | KEEP | - |

## TO REMOVE
- Video `r26-t20-counting`: slide "To be sure" (whole slide), its recap board line "To be sure: worst luck, then one more", and "To be sure" in the sidebar. (Video title "Counting Integers & Pigeonhole" can stay.)
- Card `mem-r26-t20-counting`: the "to be sure / worst luck" row or tip.
- Guided `q-r26-t20-04` + `solve-q-r26-t20-04` (renumber; the words "you've finished algebra" that moved to the end of Q8 must move to the new last question).
- Practice `q-r26-t20-09`.

## ORIGINAL ITEMS REMOVED OR REPLACED BY THE FIXERS (restore candidates)
- Removed question: `alg-extra-unit-t20-2-6` (a² = b² → |a| = |b|).
- Removed slides: `algebraic-understanding` original slides 2-7 were deleted by `M.remove_slides(LESSON, [2, 3, 4, 5, 6, 7])`: "No fixed recipe", "Must, can, cannot", "Extreme cases", "Scaling", "Connect topics", "Recap". They were replaced by new slides with the same themes (the old line "There's no repeating principle I can hand you" and the Pythagoras reference are gone). Restore candidates if the teacher wants the original wording.
- Changed question content: q-581 ("necessarily not correct" → "cannot be true"), q-585 ("x:y, y:z, z:x" → fraction bars; "Exactly one/two"), q-586 ("between x and y (not including x)" → "greater than x and smaller than y"), q-583 and q-590 reworded, q-580 stem ("(1 < S, W, D)" → sentence).
- Replaced video content: solve-q-579 (old Q3) rewritten (false triangle line removed), solve-q-577 method 3 order, solve-q-580 line "Last question of algebra" removed.

Counts: KEEP 26 · REMOVE 3 · UNSURE 0
