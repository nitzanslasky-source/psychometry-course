# Audit: Topic 22 (General word problems and ratios). Were the additions justified by the real exam?

Sources:
- What changed: `math_patches/t22_CHANGES.md` and `math_patches/t22.py`.
- The real exam: `real_exam/quant_real.md`, the regenerated full-text version with 760 questions.
- The original course: `base-v18.html`.

Real-exam groups read in full: work_rate, equations, generality, and percentages (the ratio questions are filed under it). I also searched all 760 questions for "ratio" and "n : m".

Rules applied:
- (1) Original content stays. See the section at the end.
- (2) An added method that original questions need is kept.
- A new question of a type the original course already tests is kept, and flagged if it has 0 real questions.

## What the real exam shows
- **Three-part ratio with a shared letter.** 2020_spring_q2_06 (nurses : head nurses 3 : 2, head nurses : secretaries 7 : 4) and 2025_autumn_q1_15. A plain three-part split: 2023_autumn_q2_06 (5 : 9 : 11).
- **Inverse proportion.** 2025_spring_q2_13 (4 machines for 9 h vs 9 machines for 4 h), 2024_autumn_q1_05 (pumps) and 2026_spring_q1_07.
- **Changing a ratio (a : b → something is added or removed → c : d): 0 real questions.** All ratio questions were checked. But the original course tests it: wp22-p31 (blue : white folders 5 : 7, 18 blue added → equal) and wp22-p35 (juice : water 3 : 5, water added → 1 : 3).
- **Round up to whole units.** 2023_winter_q2_07 (episode 120 → season 10) and 2020_autumn_q2_07 (day 34). There are 0 real "or part of" pricing questions, but original wp22-g033 (Q5: "every minute or part of a minute") is this type.
- **Letters in the choices.** 2019_spring_q1_15, 2022_winter_q1_19, 2020_winter_q1_16, 2024_spring_q2_02.
- **Assume all the same.** 2021_spring_q2_08 (80 tickets at 30 or 20, total 1,800).
- **One equation, two unknowns.** 2020_autumn_q1_01, 2021_spring_q2_06, and "cannot be determined" choices in 2024_autumn_q1_14 and 2025_autumn_q1_06.

| Addition | Where | Class | Verdict | Evidence |
|---|---|---|---|---|
| Ratios slide 3: "the exam does test order" | wp-034 slide 3 | FIX | KEEP | — |
| Little-guy tip moved to wp-039 slide 2 and to the mem-general-advanced tips | wp-034 slide 6, wp-039 slide 2, cards | FIX | KEEP | — |
| Q17 method 2 real bounds; Q21 title; Q19 reordered ("What changed?" first) | solve videos | FIX | KEEP | — |
| Triangle value, also called "cross-multiply and divide", with a sense check; recap "bigger or smaller?" | wp-028 slides 3 and 6 | FIX/METHOD | KEEP | 2021_autumn_q1_06, 2020_autumn_q1_10 |
| "Inverse proportion" slide; recap line; mem-ratios row | wp-028 slide 4 + recap; mem-ratios | METHOD | KEEP | 2025_spring_q2_13, 2024_autumn_q1_05, 2026_spring_q1_07 |
| Guided Q3: 6 workers, 10 days → 4 workers, with its video | q-r26-t22-02; solve-q-r26-t22-02 | inverse proportion | KEEP | 2025_spring_q2_13 |
| Practice: food supply, 30 → 36 hikers | q-r26-t22-08 | inverse proportion | KEEP | 2025_spring_q2_13, 2024_autumn_q1_05 |
| Practice: 8 machines, 2 break after 3 h | q-r26-t22-09 | inverse / work units | KEEP | 2026_spring_q1_07, 2023_winter_q2_09 |
| "Three-part ratios" slide; recap line; mem-ratios row | wp-034 slide 8 + recap | CONTENT | KEEP | 2020_spring_q2_06, 2025_autumn_q1_15, 2023_autumn_q2_06 (3 questions) |
| Guided Q8: choir 2 : 3 and 4 : 5, with its video | q-r26-t22-01; solve-q-r26-t22-01 | three-part ratio | KEEP | 2020_spring_q2_06 |
| Practice: A : B = 3 : 4, B : C = 6 : 5 | q-r26-t22-06 | three-part ratio | KEEP | 2020_spring_q2_06 |
| Practice: red : green 5 : 2, blue 1.5 × green | q-r26-t22-07 | three-part ratio | KEEP | 2020_spring_q2_06, 2025_autumn_q1_15 |
| Practice: profit, A = 2B, B = 1.5C | q-r26-t22-19 | three-part ratio | KEEP | 2020_spring_q2_06, 2023_autumn_q2_06 |
| "Changing a ratio" slide (keep the unchanged part fixed); recap line; mem-ratios row | wp-034 slide 9 + recap | METHOD | KEEP (rule 2) | 0 real, but original wp22-p31 and wp22-p35 need it |
| Guided Q9: club 5 : 4, 10 boys leave → 5 : 6, with its video | q-r26-t22-03; solve-q-r26-t22-03 | original type (p31/p35) | KEEP (flag) | 0 real. It is the guided example for a slide kept under rule 2 |
| Practice: 4 : 3, 6 girls join → equal | q-r26-t22-13 | original type | KEEP (flag) | 0 real. First to cut (p31 is almost the same question) |
| Practice: 5 : 6, 4 red out / 4 blue in → 1 : 2 | q-r26-t22-18 | original type | KEEP (flag) | 0 real. First to cut |
| "Or part of: round up" slide | wp-031 slide 3 + sidebar | METHOD | KEEP | 2023_winter_q2_07, 2020_autumn_q2_07. Original wp22-g033 |
| Practice: 139 people, buses of 45 | q-r26-t22-14 | round up | KEEP | 2023_winter_q2_07, 2020_autumn_q2_07 |
| Practice: parking, "half-hour or part of it" | q-r26-t22-15 | original type (g033 pricing) | KEEP (flag) | 0 real "or part of" pricing questions |
| New video "Three Exam Tools": Letters in the choices | r26-t22-exam-tools slide 2; toolkit row | METHOD | KEEP | 2019_spring_q1_15, 2022_winter_q1_19, 2020_winter_q1_16 |
| Guided Q22: y(2x+3), with its video | q-r26-t22-04; solve-q-r26-t22-04 | letters in the choices | KEEP | 2022_winter_q1_19, 2019_spring_q1_15 |
| Practice: m members, 20 − 150/m | q-r26-t22-10 | letters in the choices | KEEP | 2022_winter_q1_19 |
| Practice: n boxes of k pencils | q-r26-t22-11 | letters in the choices | KEEP | 2019_spring_q1_15, 2020_winter_q1_16 |
| Three Exam Tools: Assume all the same; toolkit row | r26-t22-exam-tools slide 3 | METHOD | KEEP | 2021_spring_q2_08 |
| Guided Q23: cars and motorcycles, with its video | q-r26-t22-05; solve-q-r26-t22-05 | assume all the same | KEEP | 2021_spring_q2_08 |
| Practice: 25 questions, +4 / −1 | q-r26-t22-12 | assume all the same | KEEP | 2021_spring_q2_08 |
| Three Exam Tools: One equation, two unknowns; toolkit row | r26-t22-exam-tools slide 4 | METHOD | KEEP | 2020_autumn_q1_01, 2021_spring_q2_06, 2024_autumn_q1_14 |
| Practice: 3n + 2p = 17 → cannot be determined | q-r26-t22-16 | same | KEEP | 2024_autumn_q1_14, 2025_autumn_q1_06 |
| Practice: 4n + 6p = 50 → 75 | q-r26-t22-17 | same | KEEP | 2020_autumn_q1_01, 2021_spring_q2_06 |
| New video "Shortcuts Ahead" | r26-t22-shortcuts | METHOD | KEEP | 2022_winter_q1_04, 2023_autumn_q2_06, 2026_spring_q1_14 |
| mem-ratios tips "read in order", "bigger or smaller?", "the total divides by the sum of the parts" | mem-ratios | METHOD | KEEP | 2023_autumn_q2_06, 2021_autumn_q1_17 |
| ":" → ÷, TeX, text of p30/p09/p03/p14/Q11/p17/Q10/p23/p05, US spelling | whole topic | FIX | KEEP | — |

## TO REMOVE
- Nothing is required. Every addition is either justified by the real exam or needed by original questions (rule 2).
- Flagged practice to cut first if the teacher wants to trim: q-r26-t22-13, q-r26-t22-18, q-r26-t22-15. None of their types appears on the real exam.

## ORIGINAL ITEMS REMOVED BY FIXERS (to restore)
- **Question wp22-p22** (unplaced as a near-duplicate of Q15): "A festival has 5/6 as many visitors as local residents. Visitors make up what fraction of all the people at the festival?" (6/11, 1/6, 5/11, 5/6; key 3).
- **Question wp22-p25** (unplaced as a near-duplicate of Q21): "Iris and Owen have 30 counters altogether. Iris gives Owen 9 counters and then has 4 fewer than Owen. What was the ratio of Iris's counters to Owen's before the transfer?" (11:4, 3:2, 4:1, 13:17; key 1).
- **Question wp22-p28** (unplaced as a near-duplicate of Q17): "A box of beads is split into two piles. One quarter of the first pile is used, and one sixth of the second pile is used. The two remaining piles contain 18 and 25 beads, in an unknown order. How many beads were in the box?" (60/54/43/48; key 2).
- **Spoken line, wp-034 slide 3**: "don't worry about being tricked on the order — the exam avoids that wording". Removed because it is false. The teacher should decide.
- **Spoken line, wp-034 slide 6**: "Tip: give the plain x to the smaller one. Then you never have to divide." Moved to wp-039 slide 2, not lost.
- **mem-ratios tips** "Give the plain x to the smaller quantity" and "One thing is twice another? The ×2 goes on the smaller side". Moved to mem-general-advanced, not lost.
- **wp22-p23**: the choices changed from 16:24/16:00/15:24/15:36 to the same times in a.m./p.m. format (same question).
- **wp22-p30**: the stem was rewritten for clarity (same key, 18).
- **solve-wp22-g048**: methods reordered, none removed.
