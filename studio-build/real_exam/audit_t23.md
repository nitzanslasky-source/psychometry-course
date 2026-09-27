# Audit: Topic 23 (Percentages). Were the additions justified by the real exam?

Sources:
- What changed: `math_patches/t23_CHANGES.md` and `math_patches/t23.py`.
- The real exam: `real_exam/quant_real.md`, the regenerated full-text version.
- The original course: `base-v18.html`.

I read the real-exam percentages group in full (42 questions). I also searched all 760 questions for "percentage point", salt/sugar/juice/concentration/mixture, "more than", and rates.

## What the real exam shows
- **Several changes / multipliers.** 2021_spring_q1_13 (the choice is literally (90/100)(105/100)²·a, and the other choices are the "just add the percents" traps), 2024_autumn_q1_03, 2022_winter_q2_17, 2023_spring_q1_16, 2024_winter_q1_01, 2026_spring_q2_07 (+k% then +20% → 132, work backwards).
- **"More than" vs "of".** 2023_spring_q2_12 (x greater than y by 20% → y = 83⅓% of x), 2020_winter_q1_17, 2019_spring_q2_12.
- **Fraction–percent families (⅓, ⅙, ⅝ …).** Appear in the choices of 2023_spring_q2_12 (83⅓), 2024_spring_q2_13 (66⅔), 2025_autumn_q2_03 (33⅓) and 2026_spring_q1_15 (33⅓).
- **Letters in the choices.** 2024_spring_q1_16, 2024_winter_q1_15, 2021_spring_q1_13.
- **Percentage points, or the percent change of a rate: 0 real questions.** There are 0 "percentage point" hits in all 760 questions, and no question asks by what percent a percentage changed. The original course has no such question either.
- **Mixtures / concentration: 0 liquid mixture questions.** One structurally equal question: 2025_autumn_q2_03 (200 cubes, 30% yellow, 40 purple added, yellow stays at 60 → 25%). The original course tests mixtures: wp23-p23 (300 g at 20% salt, add water → 15%).

| Addition | Where | Class | Verdict | Evidence |
|---|---|---|---|---|
| "Triple value" → "triangle value"; the "sixteen and a bit" line fixed; Q8/Q9 method fixes; spelling; "Last question of the set" | wp-052, card mem-percent, solve-wp23-g0xx | FIX | KEEP | — |
| "Thirds and families" slide (⅓ = 33⅓%, ⅙ = 16⅔%, ⅜, ⅝, ⅗, 7/20) | wp-052 slide 5 | METHOD | KEEP | 2023_spring_q2_12, 2024_spring_q2_13, 2026_spring_q1_15 |
| Change rule on the board (change ÷ original); recap line; mem-percent row "Change in percent" | wp-052 slide 9 + recap | METHOD | KEEP | 2024_autumn_q1_03, 2022_winter_q2_17, 2023_spring_q1_16 |
| "Multipliers" slide; recap "multiply the factors"; mem-percent row "Multiplier" | wp-053 slide 4 | METHOD | KEEP | 2021_spring_q1_13, 2024_autumn_q1_03, 2022_winter_q2_17, 2024_winter_q1_01 |
| "Up and down" slide (+20/−20 → −4%; p²/100; a + b + ab/100); two mem-percent tips | wp-053 slide 5; mem-percent tips | METHOD | KEEP | 2021_spring_q1_13 (its traps are exactly "the changes cancel / add up"), 2026_spring_q2_07 (a + b + ab/100 gives k = 10). Original wp23-p22 uses p²/100 |
| "Working backwards" line 96 ÷ 0.8 = 120 | wp-053 | METHOD | KEEP | 2026_spring_q2_07 |
| Guided Q6: +25% then −12% → +10%, with its video | q-r26-t23-01; solve-q-r26-t23-01 | multipliers | KEEP | 2021_spring_q1_13, 2024_autumn_q1_03 |
| New video "Percent Traps and Shortcuts", slide "More than or of?" | r26-t23-traps slide 2; mem-r26-t23-traps row 1 | METHOD | KEEP | 2023_spring_q2_12, 2020_winter_q1_17, 2019_spring_q2_12 |
| Traps video slide "Percentage points"; recap line "Difference of two percents = percentage points"; mem-r26-t23-traps row "Percentage points" | r26-t23-traps slide 3 | CONTENT | REMOVE | 0 real questions, and 0 original course questions |
| Guided Q12: pass rate 40% → 50% = +25% of passers, with its video | q-r26-t23-02; solve-q-r26-t23-02 | percentage points / percent change of a rate | REMOVE | 0 |
| Practice: 20% → 25% of workers, statements I/II | q-r26-t23-07 | percentage points | REMOVE | 0 |
| Practice: interest rate 5% → 4% = 20% fall | q-r26-t23-08 | percentage points | REMOVE | 0 |
| Traps video slide "Mixtures" (find what stays the same); recap line; mem-r26-t23-traps row "Mixtures" | r26-t23-traps slide 4 | CONTENT/METHOD | KEEP (rule 2) | original wp23-p23 is a mixture question and needs this. Real: 1 structural match, 2025_autumn_q2_03 |
| Guided Q14: 300 g at 20% sugar, add sugar → 40%, with its video | q-r26-t23-04; solve-q-r26-t23-04 | original type (p23) | KEEP (flag) | the guided example of a kept slide. Real: only 2025_autumn_q2_03 (cubes) |
| Practice: remove water, 25% → 40% juice | q-r26-t23-11 | original type (p23) | KEEP (flag) | as above; first to cut |
| Practice: mix 10% and 20% drinks → 16% | q-r26-t23-12 | mixture = weighted average | KEEP | weighted-average type: 2021_spring_q2_09 (40% of boxes at 60, 60% at 40) |
| Traps video slide "Letters: plug in numbers"; card row | r26-t23-traps slide 5 | METHOD | KEEP | 2024_spring_q1_16, 2024_winter_q1_15, 2021_spring_q1_13 |
| Traps video slide "Estimate and test"; card rows "Estimate", "Test the choices" | r26-t23-traps slide 6 | METHOD | KEEP | 2026_spring_q2_07 (test 10), 2023_spring_q2_12, 2025_winter_q1_20 |
| Guided Q13: desk 150% of chair, table 150% more → 66⅔%, with its video | q-r26-t23-03; solve-q-r26-t23-03 | "more than" vs "of" | KEEP | 2023_spring_q2_12, 2019_spring_q2_12 |
| Guided Q15: 25% of g girls out of N → 25g/N %, with its video | q-r26-t23-05; solve-q-r26-t23-05 | letters in the choices | KEEP | 2024_spring_q1_16, 2024_winter_q1_15 |
| Practice: 10% for 3 years = 33.1% | q-r26-t23-06 | multipliers | KEEP | 2022_winter_q2_17, 2024_autumn_q1_03 |
| Practice: 300% more than = 400% of | q-r26-t23-09 | more than vs of | KEEP | 2023_spring_q2_12, 2020_winter_q1_17 |
| Practice: 120% → 150% of the original = +25% | q-r26-t23-10 | change relative to the new base | KEEP | 2024_autumn_q1_03, 2023_spring_q1_16 |
| Practice: +20% then −25% = 180 → 200 | q-r26-t23-13 | work backwards with multipliers | KEEP | 2026_spring_q2_07 |
| Practice: x(1 − p²/10000) | q-r26-t23-14 | letters + multipliers | KEEP | 2021_spring_q1_13 |
| Solutions rewritten with shortcuts (p03, p17, p27, p16/18/20, p22, p10/24/07, p23); TeX; no ":" | practice | FIX | KEEP | — |
| mem-percent moved after Question 1 | flow | FIX | KEEP | — |

## TO REMOVE
- Videos: `solve-q-r26-t23-02` (guided Q12, pass rate).
- Slides:
  - r26-t23-traps "Percentage points" (slide 3) and its sidebar entry.
  - The r26-t23-traps recap line "Difference of two percents = percentage points".
  - The traps video intro/recap counts ("Three traps", "Four questions next") must be adjusted.
- Questions: q-r26-t23-02, q-r26-t23-07, q-r26-t23-08. Update the practice order and renumber the guided questions.
- Card rows: mem-r26-t23-traps row "Percentage points" (and the intro "Three traps …" becomes two).

## ORIGINAL ITEMS REMOVED BY FIXERS (to restore)
- **Question wp23-p21 replaced.** The original was "What is 16% of 25?" (choices 2/6/8/4, key 4). It is now "What is 28% of 75?" (18/24/28/21). The fixers changed it because it repeated the lesson example. Restore the original numbers if originals must stay.
- **wp-052 slide 4 line** "Can't halve it precisely? Half of thirty-two is sixteen — so it's sixteen and a bit". Removed as inaccurate and replaced by the exact 16⅔% explanation on the new slide 5. The teacher should decide.
- **mem-percent row** "Equal ratios (triple value)": renamed "triangle value", content the same.
- **wp23-g063**: the choices only changed to TeX (% → \%), same question.
- No original questions were unplaced in this topic.
