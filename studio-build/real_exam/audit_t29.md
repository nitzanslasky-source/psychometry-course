# Audit T29 - Probability, incl. the added geometric-probability lesson (additions by the 2026-09 fixers)

Source: `math_patches/t29_CHANGES.md`, `math_patches/t29.py`. Real exam: regenerated `real_exam/quant_real.md` (probability group 24 q. read in full; combinatorics, overlapping_sets, charts_tables probability items, and keyword searches over all 760 for "at random / probability / chance"). All cited ids re-checked against the regenerated file.
Rule 2 (coordinator): an added method that ORIGINAL course questions already need is kept ("orig" = the original question).

Real-exam probability picture: sequential / tree (2020_autumn_q2_17, 2022_winter_q1_06, 2024_winter_q1_16, 2025_autumn_q2_16), without replacement (2020_spring_q1_14, 2024_autumn_q2_14, 2025_winter_q2_14), exactly k (2022_autumn_q2_15, 2021_spring_q1_20, 2024_autumn_q2_14), dice sums (2019_spring_q2_13, 2023_spring_q1_17, 2025_spring_q2_16), AND of independent events (2023_winter_q2_02, 2024_spring_q2_20, 2023_autumn_q1_14), unfair die (2020_winter_q1_18). Geometric (area) probability: 0 of 760 - no question anywhere picks a random point in a figure.

| Addition | Where | Class | Verdict | Evidence (real ids / count) |
|---|---|---|---|---|
| "OR → add the SEPARATE cases" + two-or-five example | wp-151 slide 2 "And · Or" | FIX | KEEP | - |
| New slide "OR with overlap" (first + second − both; 1-30 divisible by 4 or 6) | wp-151 new slide 3; mem-probability row "OR, cases overlap" | CONTENT | KEEP | 2020_spring_q1_07 (1-30 divisible by 2 or 7 - same structure), overlapping_sets group (6 q.); orig wp29-p24 (identical example) |
| Size check "AND → smaller, OR → bigger" | wp-151 slide 3 last lines; mem-probability tip | METHOD | UNSURE | No real question where it eliminates choices (e.g. 2024_spring_q2_20: all choices are smaller); no original needs it. Harmless one-liner; teacher decides. |
| Q7/Q9 "dependent" → "forced choice" | solve-wp29-g154, -g156 | FIX | KEEP | - |
| Q8 "six heads already — a seventh?" | solve-wp29-g155 | FIX | KEEP | - |
| Q12(→Q16) story example 7/9 → 5/9 | solve-wp29-g160 | FIX | KEEP | - |
| Dice symmetry: off-topic opposite-faces remark removed, 7 − x reason added | wp-159 slide 2; mem-probability tip | FIX | KEEP | 2019_spring_q2_13, 2025_spring_q2_16 (≥17 ↔ ≤4 by symmetry) |
| Rule "two n-sided dice → most likely sum n + 1" | wp-159 slide 2 (last 3 lines); mem-probability tip | CONTENT | KEEP (rule 2) | 0 real (2023_spring_q1_17 uses a 4-faced die but asks P(sum = 4), not the most likely sum); orig wp29-p05 needs it |
| "Possible = the group they choose FROM" (sub-group) | wp-146 slide 4 (lines appended); mem-probability row "Chosen from a smaller group" | FIX / CONTENT | KEEP (rule 2) | 0 real sub-group questions; orig wp29-p26 needs it |
| Q10 line "drawn together = one after the other, without replacement" | solve-wp29-g157 slide 2; mem-probability tip | METHOD | KEEP | 2020_spring_q1_14, 2024_autumn_q2_14, 2025_winter_q2_14 |
| Q11 video reordered (simple way first, cases as check) | solve-wp29-g158 slides 2-3 | FIX | KEEP | - |
| Recap slide updated | wp-159 slide 3 | FIX | KEEP | - |
| NEW VIDEO r26-t29-more-rules slide "At least one" (1 − none) | r26-t29-more-rules slide 2; card row "At least one" | METHOD | KEEP | 2025_winter_q2_14 (1 − (8/9)(7/8) = 2/9); orig wp29-p21, p27 |
| - slide "Exactly one" (one order × number of orders) | r26-t29-more-rules slide 3; card row "Exactly one / exactly k" | METHOD | KEEP | 2022_autumn_q2_15, 2021_spring_q1_20, 2024_autumn_q2_14; orig p23, p25, p11 |
| - slide "Two stages: a tree" (SVG tree) | r26-t29-more-rules slide 4; card row "Two stages (tree)" | METHOD | KEEP | 2020_autumn_q2_17, 2022_winter_q1_06, 2024_winter_q1_16; orig p10 |
| - slide "Unknown count" (5/(5+x) = 1/3; work back) | r26-t29-more-rules slide 5; card row "Unknown count" | CONTENT | REMOVE | 0 real (2020_winter_q1_18 is an unfair die whose probabilities sum to 1 - a different type); no original needs it (orig g150/p06 give the total) |
| Guided Q12 OR with overlap (soccer/chess) | q-r26-t29-01 + solve-q-r26-t29-01 | OR overlap | KEEP | 2020_spring_q1_07; orig p24 |
| Guided Q13 at least one (guessing 3 questions) | q-r26-t29-02 + solve-q-r26-t29-02 | at least one | KEEP | 2025_winter_q2_14; orig p27 |
| Guided Q14 two boxes and a coin (tree) | q-r26-t29-03 + solve-q-r26-t29-03 | tree | KEEP | 2020_autumn_q2_17, 2022_winter_q1_06; orig p10 |
| Guided Q15 red marbles to add so P = 3/4 | q-r26-t29-04 + solve-q-r26-t29-04 | unknown count | REMOVE | 0 |
| NEW VIDEO r26-t29-geometric "Geometric Probability" (title + "Area over area", "Areas you need", "Circle in a square", "Triangle in a rectangle", 3 SVG figures) | r26-t29-geometric (all slides) | CONTENT | REMOVE | 0 of 760 (no random point in a figure anywhere; the charts set 2021_spring_q1_17..20 is roulettes read from a chart, not area ratios); no original needs it |
| Guided Q22 square side 6, circle radius 2 (figure) | q-r26-t29-05 + solve-q-r26-t29-05 | geometric | REMOVE | 0 |
| Memory card "Geometric probability" | mem-r26-t29-geometric | geometric | REMOVE | 0 |
| Practice unknown count (6 red, P = 2/5) | q-r26-t29-06 | unknown count | REMOVE | 0 |
| Practice unknown count (socks, 2 added) | q-r26-t29-07 | unknown count | REMOVE | 0 |
| Practice raffle, 2 drawn together, at least one | q-r26-t29-08 | at least one / drawn together | KEEP | 2025_winter_q2_14 |
| Practice rain / walk (tree) | q-r26-t29-09 | tree | KEEP | 2020_autumn_q2_17 |
| Practice overlap from "neither" | q-r26-t29-10 | OR overlap | KEEP | 2020_autumn_q1_11 (overlapping sets with "not … and not …"), 2020_spring_q1_07 |
| Practice committee, both chosen | q-r26-t29-11 | without replacement / specific items | KEEP | 2020_spring_q1_14 (the 2 dice remain), 2024_spring_q2_20 |
| Practice triangle in 8 × 5 rectangle (figure) | q-r26-t29-12 | geometric | REMOVE | 0 |
| Practice round target radius 10 / 2 (figure) | q-r26-t29-13 | geometric | REMOVE | 0 |
| Practice square, P = 0.36 → x (figure) | q-r26-t29-14 | geometric | REMOVE | 0 |
| Solutions rewritten, stems cleaned, American spelling, card OR row fixed | all T29 | FIX | KEEP | - |

## TO REMOVE
- Video r26-t29-more-rules: slide 5 "Unknown count" (and its entry in LESSON_SB, which is shared by wp-146, wp-147-after, wp-151, wp-159).
- Guided q-r26-t29-04 + video solve-q-r26-t29-04.
- Whole video r26-t29-geometric (5 slides, 3 figures) and its sidebar.
- Guided q-r26-t29-05 (+ figure) + video solve-q-r26-t29-05; drop "Question 22" from ADV_SB (renumbering follows).
- Memory card mem-r26-t29-geometric.
- Practice q-r26-t29-06, -07, -12, -13, -14.
- mem-probability row "Unknown count".

UNSURE (teacher decides): wp-151 slide "OR with overlap" last two lines ("Size check: AND → smaller · OR → bigger") and the mem-probability tip "Size check: AND makes the chance smaller, OR makes it bigger."

## ORIGINAL ITEMS REMOVED BY FIXERS (restore - originals stay)
Questions removed (unplaced):
- wp29-p03 (two 8-sided dice, matching results; ≈ Q9)
- wp29-p20 (k boxes with cards 1..m; ≈ Q14 with new letters)

Questions whose content was replaced: none of substance (wp29-g160 choices only put into TeX, "Which statement is true?" → "Which of the following is correct?"; the other stems are rewording).

Slides / lines whose original content was overwritten:
- wp-151 "And · Or" slide 2: script replaced (original said "OR → add" without the separate-cases condition, and "Or questions are rare").
- wp-159 slide 2: original line "By the way — opposite faces of a die always add to seven…" deleted.
- wp-159 slide 3 "Recap": script replaced.
- solve-wp29-g158 (Q11): slide 2 "Two cases" → "Method 1 · Count the lockers"; slide 3 "Method 2 · Complement" → "Method 2 · Two cases" (the original complement method was removed from this video and moved to the new "At least one" slide).
- Single lines replaced in solve-wp29-g154, -g155, -g156, -g160 (see FIX rows).
- wp-146 slide 4: original script kept, lines only appended.
Memory card mem-probability: table "Rules" rows replaced - the original OR row example "1/7 + 6/7 · 1/6 = 2/7" was replaced by the 2-or-5 example; tips replaced - original tip '"Or" questions are rare — and a second try only happens after a first miss.' reduced to "A second try only happens after a first miss." The "Two dice: number of ways for each sum" table is untouched.
