# Audit: Topic 25 (Averages). Were the additions justified by the real exam?

Sources:
- What changed: `math_patches/t25_CHANGES.md` and `math_patches/t25.py`.
- The real exam: `real_exam/quant_real.md`, the regenerated version.
- The original course: `base-v18.html`.

I read the real-exam averages group in full (23 questions), plus the averages-related questions in work_rate and percentages.

## What the real exam shows
- **How many values (a value joins or leaves).** 2026_spring_q2_15 (Daniel joins, 80 → 80.5, grade 96) and 2020_winter_q2_20 (the average without the manager).
- **Balance / deviations from a reference.** 2025_autumn_q1_18 (heights relative to the class average), 2024_spring_q1_07 (gorillas 135 → 120), 2026_spring_q2_15.
- **Evenly spaced.** 2024_winter_q2_07 (children born at equal intervals, 15 and 9 → average 12).
- **Every value changes (+k, ×k).** 2025_autumn_q2_15 (the average of a + 1 and b − 1; half the average of 2a and 2b), 2022_winter_q1_08.
- **Largest / smallest possible with an average.** 2025_spring_q1_05 (Monday more calls than any other day → at least 5), 2024_winter_q1_17 (the smallest number of episodes = x + 1).
- **Weighted averages.** 2021_spring_q2_09 (40% of boxes at 60, 60% at 40 → 48), 2024_autumn_q2_01, 2019_spring_q2_19.
- **Plug in numbers.** 2025_autumn_q2_15, 2022_winter_q1_08, 2025_winter_q2_16.

| Addition | Where | Class | Verdict | Evidence |
|---|---|---|---|---|
| "Evenly spaced" slide; recap; card row | wp-080 slide 3; mem-averages row | METHOD | KEEP | 2024_winter_q2_07 |
| Guided Q6: nine consecutive even numbers, average 30 → largest 38, with its video | q-r26-t25-04; solve-q-r26-t25-04 | evenly spaced | KEEP | 2024_winter_q2_07 |
| Practice: eight consecutive odd numbers | q-r26-t25-09 | evenly spaced | KEEP | 2024_winter_q2_07 |
| Practice: the average of 13 … 57 | q-r26-t25-10 | evenly spaced | KEEP | 2024_winter_q2_07 |
| "The balance" slide; recap; card row | wp-080 slide 6 | METHOD | KEEP | 2025_autumn_q1_18, 2024_spring_q1_07, 2026_spring_q2_15 |
| Guided Q4: balance with five scores → 83, with its video | q-r26-t25-02; solve-q-r26-t25-02 | balance | KEEP | 2024_spring_q1_07, 2025_autumn_q1_18 |
| Practice: balance with 5 numbers | q-r26-t25-06 | balance | KEEP | 2024_spring_q1_07 |
| "A base number" slide (97, 102, 104, 99 → 100.5); card row | wp-080 slide 8 | METHOD | KEEP | the same deviation mechanic as the balance: 2024_spring_q1_07, 2022_autumn_q2_03 (290/200/230 around 240) |
| Practice: base number 1,000 → 1,002 | q-r26-t25-13 | base number | KEEP | as above |
| "Every value changes" slide (+k, ×k, ages in 5 years); card row | wp-080 slide 10 | METHOD | KEEP | 2025_autumn_q2_15, 2022_winter_q1_08 |
| Guided Q7: the average of 3a+2, 3b+2, 3c+2 = 62, with its video | q-r26-t25-05; solve-q-r26-t25-05 | every value changes | KEEP | 2025_autumn_q2_15 |
| Practice: ages in 3 years + a newborn | q-r26-t25-11 | every value changes + how many | KEEP | 2025_autumn_q2_15, 2026_spring_q2_15 |
| "Largest possible value" slide (others as small as possible; "different" trap); card row + tip | wp-081 slide 5 | METHOD | KEEP | 2025_spring_q1_05, 2024_winter_q1_17. Original wp25-p15 ("at most … December") |
| Guided Q5: six different positive integers, average 9 → 39, with its video | q-r26-t25-03; solve-q-r26-t25-03 | largest possible with an average | KEEP | 2025_spring_q1_05, 2024_winter_q1_17 (the "different" twist has 0 real questions) |
| Practice: the smallest possible largest of 4 different integers | q-r26-t25-08 | min of the largest with an average | KEEP | 2025_spring_q1_05 |
| "How many were there?" slide; card row | wp-081 slide 7 | METHOD | KEEP | 2026_spring_q2_15, 2020_winter_q2_20 |
| Guided Q2: 70 → 73 with 94 → 7, with its video | q-r26-t25-01; solve-q-r26-t25-01 | how many | KEEP | 2026_spring_q2_15 (almost identical), 2020_winter_q2_20 |
| Practice: how many workers now | q-r26-t25-07 | how many | KEEP | 2020_winter_q2_20 |
| Weighted averages: "heavy side gets the SMALL part"; "closer to the bigger group"; "50 and 70 give 60 only if the groups are equal"; recap; card rows/tips | wp-086 | METHOD | KEEP | 2021_spring_q2_09, 2024_autumn_q2_01 |
| Practice: three groups weighted, 72 (trap 70⅔) | q-r26-t25-12 | weighted average | KEEP | 2024_autumn_q2_01, 2021_spring_q2_09 |
| Q13 video "Method 3 · Extra per item"; card row | solve-wp25-g090 slide 4 | METHOD | KEEP | 2021_spring_q2_09 (40 + 0.4·20 = 48) |
| Q3 plug-in warning + "go straight to method two"; choices reworded | solve-wp25-g084, wp25-g084 | FIX/METHOD | KEEP | 2025_autumn_q2_15, 2022_winter_q1_08 |
| Card tip "positive / different / integers change the answer" | mem-averages | METHOD | KEEP | 2025_spring_q1_05 |
| Written solutions in TeX, ":" → ratio wording, "two−test" minus sign | whole topic | FIX | KEEP | — |

## TO REMOVE
- Nothing. Every addition matches real question types.

## ORIGINAL ITEMS REMOVED BY FIXERS (to restore)
- **Question wp25-p06** (unplaced, "same idea as p08 and p12"): "Two positive rope lengths have an average equal to one of the lengths. What is their ratio?" (1:1, 1:2, 2:3, 3:4; key 1).
- **Question wp25-p05 replaced by a different question.** The original was "What is the average of ⅔ and ⅙?" (5/12, 1/4, 1/3, 5/6; key 1). It is now "average 40, 16 removed, average 43, how many numbers at first?" (7/8/9/10). The new question is a valid "how many" item (2026_spring_q2_15), but the original was lost. Restore it (for example, add the new one as a q-r26 id instead).
- **Question wp25-p25 changed.** The original was "Seven consecutive integers have an average of 23. What is their sum?" (168/175/161/154; key 3). It is now "…What is the largest of them?" (26/27/29/30).
- **Question wp25-p23 numbers changed.** The original had test 68 and project 92, weights 3 : 1, answer 74 (74/72/76/80). It now has 72 and 88, answer 76.
- **Question wp25-p11 changed.** The original condition "b = a + 2" was removed from "Two real numbers satisfy b = a + 2, and their average is 3a. What is their average in terms of b?" The choices and key are the same.
- **wp25-g084 (Q3)**: the choices were only reworded ("N times the average of the four numbers"), same key.
- **mem-averages**: the "See-saw" row was only reworded ("weight ratio … → distance ratio"). No original row was lost.
