# Audit: Topic 24 (Overlapping groups). Were the additions justified by the real exam?

Sources:
- What changed: `math_patches/t24_CHANGES.md` and `math_patches/t24.py`.
- The real exam: `real_exam/quant_real.md`, the regenerated version.
- The original course: `base-v18.html`.

I read the real-exam overlapping_sets group in full (6 questions). Overlap questions filed under other groups were found by reading the percentages and combinatorics groups in full and by searching all 760 questions for "exactly one" and "all three".

## What the real exam shows (overlap questions: 12)
- **Overlap range (min/max of both).** 2019_spring_q2_04, 2020_winter_q1_14, 2024_spring_q1_08.
- **Other regions (neither).** 2020_autumn_q1_11 (the most adults in neither class; the union goes from 120 to 180) and 2024_winter_q2_02 (neither, exact).
- **Two-way tables / percent of a subgroup.** 2025_winter_q1_15 (hair colour × blue eyes, "10% of the black-haired"), 2024_winter_q2_02 (glasses × long hair, "half of those who wear glasses"), 2021_autumn_q2_11 (AC × passengers), 2020_autumn_q1_11 (adults/children × registered).
- **Three groups.** 2023_autumn_q2_20 (common to all three: 0 to 10) and 2024_autumn_q1_19 (4 lectures; the least number all three attended = 0, by counting who is missing). A related max question: 2023_winter_q1_13.
- **"Exactly one": 0 real questions.** But the original course tests it: wp24-p12 and wp24-p17 ("how many … exactly one").

| Addition | Where | Class | Verdict | Evidence |
|---|---|---|---|---|
| "max(8, 7) → 7" note corrected | wp-068 slide 4 | FIX | KEEP | — |
| "Spot the wording" rule corrected ("at most/at least refer to the thing they ask"); recap; card tip | wp-068 slides 8 and 11; mem-overlap tips | FIX | KEEP | 2020_autumn_q1_11 (at most neither → max overlap) |
| Q9 butterflies stem ("different" ambiguity); p13 construction; "Twenty−one" → numerals; US spelling; ratio note | wp24-g078, wp24-p13, Q5 video, whole topic | FIX | KEEP | — |
| "Other regions" slide (union / neither / A only from the overlap range); mem-overlap table "other regions" | wp-068 slide 7; mem-overlap | METHOD | KEEP | 2020_autumn_q1_11, 2024_winter_q2_02 |
| Q5 video: the simpler route (through the union) first; complements becomes Method 2 | solve-wp24-g075 | METHOD (reorder) | KEEP | 2020_autumn_q1_11 |
| Guided Q6: swim but not run, the least (trap 23), with its video | q-r26-t24-01; solve-q-r26-t24-01 | range of a non-overlap region | KEEP | 2020_autumn_q1_11 (the same "which overlap makes THIS region small/large" logic) |
| Practice: the greatest neither (80 guests) | q-r26-t24-07 | neither range | KEEP | 2020_autumn_q1_11 |
| Practice: the greatest "tennis only" | q-r26-t24-10 | region range | KEEP | 2020_autumn_q1_11 |
| Practice: which could be "at least one" | q-r26-t24-11 | union range | KEEP | 2020_autumn_q1_11, 2019_spring_q2_04 |
| "Exactly one" slide (strip, A + B − 2·both); recap line; mem-overlap formula row "Exactly one" | wp-069 slide 6 + recap; mem-overlap | METHOD | KEEP (rule 2) | 0 real, but original wp24-p12 and wp24-p17 need it |
| Practice: the greatest "exactly one" = 43 | q-r26-t24-08 | original type (p12/p17) + range | KEEP (flag) | 0 real. First to cut |
| New lesson "Two-Way Tables" (don't average 20% and 30%; fill with totals; "percent of what?") | r26-t24-two-way; mem-r26-t24-more | CONTENT | KEEP | 2025_winter_q1_15, 2024_winter_q2_02, 2021_autumn_q2_11, 2020_autumn_q1_11 (4) |
| Guided Q10: walkers 25%, with its video | q-r26-t24-02; solve-q-r26-t24-02 | two-way table | KEEP | 2025_winter_q1_15 |
| Practice: 30 students, girls/glasses | q-r26-t24-04 | two-way table counts | KEEP | 2024_winter_q2_02 |
| Practice: day/night shift, new workers % | q-r26-t24-05 | two-way table percents | KEEP | 2025_winter_q1_15 |
| Practice: adults/children, chess, fraction | q-r26-t24-06 | two-way table, "of what" | KEEP | 2025_winter_q1_15 |
| New lesson "Three Groups" (count who is missing; can it be 0; the max is the smallest group) | r26-t24-three-groups; mem-r26-t24-more | CONTENT | KEEP | 2023_autumn_q2_20, 2024_autumn_q1_19 (2). Original wp24-p13 is also this type |
| Guided Q11: phone/laptop/tablet 25%, with its video | q-r26-t24-03; solve-q-r26-t24-03 | three groups | KEEP | 2024_autumn_q1_19, 2023_autumn_q2_20 |
| Practice: math/art/music, the least in all three = 15 | q-r26-t24-09 | three groups | KEEP | 2024_autumn_q1_19 |
| "Work in percent" card tip; p15 contrast | mem-overlap tips; wp24-p15 | METHOD | KEEP | 2025_winter_q1_15, 2021_autumn_q2_11 |
| Weak-student fixes ("unrolled into one line"; Q2 union route first) | wp-069 slide 3; solve-wp24-g071 | FIX | KEEP | — |

## TO REMOVE
- Nothing is required. Every addition is justified by the real exam or by original questions (rule 2).
- Flagged practice to cut first: q-r26-t24-08 (the greatest "exactly one"; 0 real questions).

## ORIGINAL ITEMS REMOVED BY FIXERS (to restore)
- **Question wp24-p04** (unplaced as a near-duplicate of guided Q1): "Of 120 hikers, 54 carry a map, 82 carry a compass, and 31 carry both. How many carry neither?" (15/16/23/31; key 1).
- **Question wp24-p02** (unplaced as a near-duplicate of p08/Q9): "Every one of a group of students studies art, music, or both. There are 26 art students, 19 music students, and 11 who study both. How many students are in the group?" (56/34/30/45; key 2).
- **wp-068 "Spot the wording" rule** "'At most' → maximum [overlap], 'at least' → minimum". Replaced because it is wrong for "only"/"neither" questions. The matching mem-overlap row ""at most"/"at least" | maximum/minimum | "could be" → a range" was also replaced. The teacher should decide; restoring them would restore an error.
- **mem-overlap** was rewritten. The original rows "Maximum overlap | the smaller group | 8 and 7 → 7", "A + B − both + neither = total" and the tip "'Distinct items in either collection' is the union — neither is 0" are all still there, reworded.
- **solve-wp24-g071 and solve-wp24-g075**: methods reordered and renamed. No method slide was deleted.
- **wp24-g078 stem**: "photograph different butterflies" reworded (same question and key).
