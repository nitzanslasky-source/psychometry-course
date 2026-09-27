# Audit: Topic 21 (Trial, limits and patterns). Were the additions justified by the real exam?

Sources:
- What changed: `math_patches/t21_CHANGES.md` and `math_patches/t21.py`.
- The real exam: `real_exam/quant_real.md`, the regenerated full-text version with 760 questions.
- The original course: `base-v18.html`, used to check which question types the original course already tests (rule 2).

Real-exam groups read in full: trial_and_error, generality, averages, combinatorics, divisibility_remainders, number_properties and work_rate. I also searched all 760 questions for these keywords: sure/certain/guarantee, weekday names, units/last digit, term/sequence, "different integers", necessarily, at least/at most.

Rules applied:
- (1) Original content stays. See "ORIGINAL ITEMS REMOVED BY FIXERS" at the end.
- (2) An added method that original course questions need is kept.
- A new practice question of a type the ORIGINAL course already tests is not a new type. It is kept, but flagged when the real exam has 0 questions of that type.

## What the real exam shows
- **Pigeonhole / worst case.** 2019_winter_q1_14: n participants choose from n−1 countries, so "some country got at least 2" is necessarily true. 2025_autumn_q1_03: the most key attempts. No real question has the "draw blind until sure" form.
- **Weekday offset (+N days) and units digit of a power: 0 real questions.** The units-digit questions that exist (2021_spring_q1_09, 2020_winter_q2_05, 2023_spring_q1_02) are not about cycles of powers. The real cycle and remainder questions (2023_spring_q1_07, 2023_winter_q2_07) are covered by the original "Repeating cycles" slide.
- **A formula for the n-th term or for the sum of the first n terms: 0 real questions.** The real sequence questions are all done term by term: 2024_spring_q1_14, 2024_winter_q1_01, 2021_autumn_q2_04 and 2019_spring_q2_15.
- **"k different positive amounts" questions: 0 real.** But the original course tests this type: wp21-g007, wp21-g020, wp21-p07, wp21-p27 (and wp21-p23, which the fixers removed).
- **Min/max rules.** Max of one → give the others the least: 2020_spring_q1_01. Min of the largest → share equally: 2025_spring_q1_05, 2022_autumn_q1_18. Min of one → give the others the most: 2025_winter_q1_15, 2021_autumn_q2_11. Min/max with an average: 2024_winter_q1_17.
- **Must be true / necessarily: very common.** Examples: 2026_spring_q1_04, 2025_winter_q2_11, 2024_spring_q2_03, 2019_winter_q1_14, 2023_spring_q2_08.

| Addition | Where | Class | Verdict | Evidence |
|---|---|---|---|---|
| "No holes" rule corrected (Method 1 spare markers, Method 2 only-the-ends, "NOT a general rule") | solve-wp21-g021 (Q14) slides 2–3; wp21-g021 solution; toolkit row "Cannot be" | FIX | KEEP | correction of a false rule |
| Spare units as a named card row | mem-trial-toolkit row "Everyone has a minimum…" | FIX (the method was already in the original Q13 video, Method 3) | KEEP | also 2020_spring_q1_01 |
| "Must or could" (was "Possible vs must"), slide 5 and wp-012 slide 2 shortened | wp-001 slides 4–5, wp-012 slide 2 | FIX | KEEP | wording |
| Bold words → circle the word; "A recurring motif" slide folded into one line; Q10/Q13/Q16 wording; ÷ for ":" | wp-006, solve-wp21-g007/g017/g020/g025 | FIX | KEEP | — |
| "Three min/max rules" board (replaces "Max one, min the rest"); recap; toolkit row | wp-016 slide 2 + recap; toolkit row "Max of one / min of the largest / min of one" | METHOD | KEEP | 2020_spring_q1_01, 2025_spring_q1_05, 2025_winter_q1_15 |
| "Worst luck + 1" slide (4 players, 3 wins → 9) | wp-016 slide 3; recap line; toolkit row "To be sure…" | METHOD | KEEP | 2019_winter_q1_14, 2025_autumn_q1_03. Original wp21-p14 also needs it |
| Guided Q9 socks → 7, with its video | q-r26-t21-01; solve-q-r26-t21-01 | practice of an original type (T20 socks; T21 p14) | KEEP | method: 2019_winter_q1_14. Flag: the blind-draw form has 0 real questions |
| Practice: sure of 2 black balls → 16 | q-r26-t21-03 | original type (blind draw, T20) | KEEP (flag) | 0 real in the blind-draw form; the method is justified by 2019_winter_q1_14 |
| Practice: cards 1–20, sure of a pair summing to 21 → 11 | q-r26-t21-04 | original type | KEEP (flag) | as above |
| Practice: 30 students → 3 in the same month | q-r26-t21-05 | pigeonhole must-be-true | KEEP | 2019_winter_q1_14 (same type) |
| Guided Q15: five different integers with sum 20, "largest ≥ 6", with its video | q-r26-t21-02; solve-q-r26-t21-02 | METHOD (must be true) | KEEP | 2026_spring_q1_04, 2025_winter_q2_11, 2024_spring_q2_03 |
| Practice: three friends, 25 marbles, "largest share ≥ 10" | q-r26-t21-06 | must be true + min of the largest | KEEP | 2025_spring_q1_05, 2026_spring_q1_04 |
| "Cheapest k different": 1+2+…+k = k(k+1)/2; recap line; card row | wp-006 slide 5; wp-006 recap; mem-trial-error row "Different positive amounts" | METHOD | KEEP (rule 2) | 0 real "different amounts" questions, but original wp21-g007, wp21-g020, wp21-p07, wp21-p27 are this type, and the Q3 method-2, p07 and p27 solutions use it |
| Sequence plug-in: n = 3, and n = 4 if two choices survive | wp-008 slides 4 and 6; mem-trial-error row "Patterns · sequences" | METHOD (refines the original "Plug in n = 3" slide) | KEEP | plug-in with n in the choices: 2025_winter_q2_16, 2022_winter_q1_19. Original wp21-g010 |
| Practice: n-th term a_n = 4n + 1 | q-r26-t21-07 | original type (formula with n in the choices, as in wp21-g010) | KEEP (flag) | 0 real n-th-term questions. First to cut if practice is long |
| Practice: 2 + 4 + … + 2n = n(n+1) | q-r26-t21-09 | original type (sum through day n, as in wp21-g010) | KEEP (flag) | 0 real. First to cut |
| Practice: sum of the first n terms is n² + 2n → 10th term | q-r26-t21-08 | CONTENT (a new sub-type: from S_n to a term; not in the original course) | REMOVE | 0 real |
| "Days and last digits" slide (weekday + N; units digit of 3²²; remainder 0 = last in the cycle); sidebar entry; recap wording; toolkit wording | wp-022 slide 4; wp-022 recap line "Cycle → remainder (days: ÷ 7, last digits: find the cycle)"; mem-trial-toolkit row "Repeating cycle" words "lamps, days of the week (÷ 7), last digits of powers" | CONTENT | REMOVE | 0 real questions, and no original course question of this type (the original card row was only "Repeating cycle — Use the remainder") |
| Practice: Monday + 100 days | q-r26-t21-10 | CONTENT | REMOVE | 0 |
| Practice: units digit of 7⁵⁰ | q-r26-t21-11 | CONTENT | REMOVE | 0 |
| Rewritten solutions and stems (g007, g014, g017, p05, p06, p07, p12, p13, p16, p17, p24, Q4); p14 solution uses worst luck + 1 | questions | FIX | KEEP | — |

## TO REMOVE
- Slides:
  - wp-022 "Days and last digits" (slide 4) and its sidebar entry.
  - Restore the wp-022 recap line to "Cycle → remainder", without "(days: ÷ 7, last digits: find the cycle)".
- Questions: q-r26-t21-08, q-r26-t21-10, q-r26-t21-11. Update the practice order.
- Card rows: mem-trial-toolkit row "Repeating cycle". Remove the added "days of the week (÷ 7), last digits of powers" (the original row: "Repeating cycle | Use the remainder").

## ORIGINAL ITEMS REMOVED BY FIXERS (to restore)
- **Question wp21-p23** (unplaced as a near-duplicate): "Thirty-six stickers are given to children, with each child receiving a different positive integer number. What is the greatest possible number of children?" (7/9/10/8, key 3).
- **Question wp21-p26** (unplaced as a near-duplicate of Q6): "A club buys exactly six packs. Small packs contain 4 markers and large packs contain 9 markers. Which total number of markers is impossible?" (24/39/54/42, key 3).
- **Slide wp-006 #3 "A recurring motif"** (removed). Its point is now one line on wp-001 slide 5 / "Ranges".
- **Slide solve-wp21-g021 #2 "Method 1 · The range has no holes"** (replaced). It taught a FALSE general rule ("the range is continuous, no holes"). It is replaced by the correct "Method 2 · Only the ends?". Restoring it would restore the error, so the teacher should decide.
- **Slide solve-wp21-g021 #3 "Method 2 · Edge cases"** (removed and merged). Its checks (24 × 3 = 72 < 86 ✗; 23 × 3 = 69 → 17 ✓) are now inside the new Method 2 ("10 to 23").
- **Slide solve-wp21-g021 #4 "Method 3 · Count the spare markers"**: kept, moved to Method 1.
- **Slide wp-016 #2 "Max one, min the rest"** (replaced by "Three min/max rules"; its two rules are included there).
- **Slide wp-001 #4 "Possible vs must"**: rewritten as "Must or could", same content. The "spoon-fed at school" lines were removed from wp-001 slide 5 and wp-012 slide 2.
- **Card mem-trial-toolkit**: the original rows "Maximise one — give all the others the minimum" and "'At least'/'at most' in the answers — plug in the smaller/bigger first" were reworded. The row "'Cannot be' … the range has no holes — the answer is at an end" was corrected (a false rule).
- **Card mem-trial-error**: the tip "Possible → one legal example … Must / impossible → you need a reason" was reworded.
- Stems reworded without changing the question: wp21-g014, wp21-p12 ("any of them may be blue" added), wp21-p17. The wp21-p13 solution was replaced by a full listing.
