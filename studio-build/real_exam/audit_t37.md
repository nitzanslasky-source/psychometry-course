# Audit: Topic 37 (The coordinate system). Were the additions justified by the real exam?

Sources: `math_patches/t37_CHANGES.md`, `math_patches/t37.py`, `real_exam/quant_real.md` (regenerated full-text version), and the pre-patch course `course18.json`.
Real-exam groups read in full: coordinate_system (17), plus geometric_comprehension (9) and circles (37), which contain coordinate questions. I also searched all 760 questions for: quadrant, reflect/symmetr/mirror, midpoint, slope, "y = …x", axis/axes/intersect.

Rules applied (brief + coordinator):
- An added topic, rule or question type stays only if the real exam has it.
- An added method that ORIGINAL course questions need stays (rule 2).
- An added question whose type exists only in the original course, and not on the real exam, is removed.

Main findings from the real exam:
- **The word "quadrant": 0 real questions.** No real question asks "in which quadrant".
  - Real questions do reason with signs of letter coordinates: 2022_autumn_q2_13 (a, b, c, d on a diameter through the origin) and 2020_winter_q1_20.
  - Original questions geo37-g158, geo37-core-p04 and geo37-core-p17 say "in the first quadrant" in the stem. So the meaning of the quadrants is needed to read original questions.
- **Reflection through the origin: 1 real question.** 2022_autumn_q2_13: E and F are ends of a diameter of a circle centered at the origin, so F = (−x, −y). Related: 2025_autumn_q1_07 ($(x, y) = (y, x)$, a swap, which the slide does not cover). Original geo37-core-p21 is a reflection question.
- **Midpoint and equal division of a segment: 2 real questions.** 2021_autumn_q1_14 (A is the midpoint of OB, s + t = 18) and 2020_spring_q2_03 (points divide AO into 4 equal parts → (4, 2)).
- **Area of a slanted polygon on a grid (box it in and subtract the corners): 3 real questions.** 2020_autumn_q1_05 (dark quadrilateral, area 15), 2019_winter_q2_03 (trapezoid, area 15), 2025_winter_q2_06 (lattice octagon, area 7).
- **Slope, negative slope, line equations y = mx + b, intercepts of ax + by = c: 0 real questions.** No coordinate question gives a line by an equation. The nearest is 2021_spring_q1_12 (region y < x), which the slides do not teach. The original course has geo37-core-p25 (2x + 3y = 12 with the axes) and geo37-core-p26 (distance to y = −2). These need "put y = 0 / x = 0" and the horizontal line y = c. They do not need a negative slope.
- **Letters in coordinates, solved by plugging in numbers: 3 real questions.** 2020_winter_q1_20, 2021_autumn_q1_14, 2022_autumn_q2_13.
- **Lengths with roots in the choices: 3 real questions.** 2026_spring_q1_13, 2022_winter_q1_16, and 2023_autumn_q2_05 (compare AB with 30).

| Addition | Where | Class | Verdict | Evidence |
|---|---|---|---|---|
| Wrong/misleading lines fixed: Q6 "Hebrew version"; Q3 backwards logic; Q9 "never meet"; circle tangent to both axes "first quadrant"; Q2 "three, three…"; ":" → fractions; Q8 y = mx + b remark | solve-geo37-g164 s5, solve-geo37-g160 s2, solve-geo37-g167 s3, geo-157 s3, solve-geo37-g158 s4, solve-geo37-g166 s3 | FIX | KEEP | corrections |
| Q3 video: new slide "Plug in numbers" (a = 1, b = 2) before the algebra | solve-geo37-g160 new slide 3 "Plug in numbers" | METHOD | KEEP | 2020_winter_q1_20, 2021_autumn_q1_14, 2022_autumn_q2_13 |
| "Four quadrants" slide: I (+,+), II (−,+), III (−,−), IV (+,−); a point on an axis is in no quadrant | geo-154 new slide 8 "Four quadrants" (+ figure); mem-coordinates row "Quadrants" | METHOD needed by original items | KEEP (rule 2) | 0 real "quadrant" questions. The original stems geo37-g158, p04 and p17 use "first quadrant", and the sign reasoning helps with 2022_autumn_q2_13 |
| Guided Q1: (a, b) in quadrant II → where is (b, −a)? | q-r26-t37-01 + video solve-q-r26-t37-01 | question type "which quadrant" | REMOVE | 0 real questions |
| Practice: (a, b) in quadrant IV, which point is in II? | q-r26-t37-02 | "which quadrant" | REMOVE | 0 real |
| Practice: ab < 0, a > b, where is (b, a)? | q-r26-t37-04 | "which quadrant" | REMOVE | 0 real |
| "Reflections" slide: across the x-axis, across the y-axis, through the origin | geo-154 new slide 9 "Reflections" (+ figure); mem-coordinates row "Reflection" | CONTENT | KEEP | 2022_autumn_q2_13 (through the origin), 1 real question; also needed for original geo37-core-p21 |
| Practice: two reflections, then PR = 10 | q-r26-t37-03 | reflection + length | KEEP | 2022_autumn_q2_13 |
| "Midpoint" slide (average, or repeat the move) | geo-159 new slide 5 "Midpoint"; mem-coordinates row "Midpoint" | CONTENT | KEEP | 2021_autumn_q1_14, 2020_spring_q2_03 (original p22 too) |
| Guided: M(2, −1) midpoint, A(−4, 3) → B(8, −5) | q-r26-t37-05 + video | midpoint | KEEP | 2021_autumn_q1_14 |
| Practice: midpoint of A(−3, 5), B(7, −1) to the origin → 2√2 | q-r26-t37-06 | midpoint | KEEP | 2021_autumn_q1_14, 2020_spring_q2_03 |
| "Stairs going down" slide (negative slope −3/2, "up to the right +, down to the right −") | geo-159 new slide 8 "Stairs going down" (+ figure); mem-coordinates row "Slope" (up ÷ across with a sign) | CONTENT | REMOVE | 0 real questions; no original question needs a negative slope |
| Practice: line through (−2, 7) and (4, −2), y-intercept (0, 4) | q-r26-t37-08 | negative slope | REMOVE | 0 real |
| "The line equation" slide (y = mx + b; y = −2 horizontal, x = 4 vertical) | geo-159 new slide "The line equation"; mem-coordinates row "Line equation" | CONTENT needed by original items | KEEP (rule 2) | 0 real questions; needed for original geo37-core-p26 (line y = −2) and p25. Edit it: its example "Our stairs going down … y = minus three halves x plus 6" (a draw note + a spoken line) points to the removed slide, so it needs a new example |
| "Cutting the axes" slide (put y = 0 / x = 0; 3x + 5y = 15) | geo-159 new slide "Cutting the axes" (+ figure) | METHOD needed by original items | KEEP (rule 2) | 0 real questions; needed for original geo37-core-p25 (2x + 3y = 12 with the axes) |
| Guided: 4x + 3y = 24 cuts the axes → AB = 10 | q-r26-t37-07 + video solve-q-r26-t37-07 | line equation / intercepts (original-only type) | REMOVE | 0 real (original p25 stays) |
| Practice: y = −2x + b through (3, 1) → x-intercept 3.5 | q-r26-t37-09 | line equation (original-only type) | REMOVE | 0 real |
| New lesson "Area of a Slanted Triangle" (box it in, subtract the corners, when to use it) | video r26-t37-box (3 slides); mem-coordinates row "Slanted triangle area" | METHOD | KEEP | 2020_autumn_q1_05, 2019_winter_q2_03, 2025_winter_q2_06. Count: 3 |
| Guided Q3: A(−2, 1), B(4, −1), C(2, 5) → 16 | q-r26-t37-10 + video | box method | KEEP | 2020_autumn_q1_05, 2025_winter_q2_06 |
| Practice: triangle O, (6, 2), (2, 4) → 10 | q-r26-t37-11 | box method | KEEP | same |
| Practice: quadrilateral → 21 | q-r26-t37-12 | box method | KEEP | 2020_autumn_q1_05 (quadrilateral, area 15) |
| "Roots in the answers? Compare across² + up²" | geo-155 (Lengths) slide 8 board + line; mem-coordinates tip | METHOD | KEEP | 2026_spring_q1_13, 2022_winter_q1_16, 2023_autumn_q2_05 |
| "Plug in easy numbers" tip | mem-coordinates tip | METHOD | KEEP | 2020_winter_q1_20, 2021_autumn_q1_14, 2022_autumn_q2_13 |
| Card row "Parallel lines: the same slope / same step" | mem-coordinates | FIX (summary of the original "Same multiplier" slides) | KEEP | original content |
| All stems/choices/solutions in TeX; step-by-step; p07, p03, p13, p18, g167, p11, p17, g163, g164 rewordings; spelling | all topic questions | FIX | KEEP | wording |
| Figures: label collisions, answer give-aways removed (p10, p25), slides 5–7 one point each | many | FIX | KEEP | figures |

## TO REMOVE
- Videos: `solve-q-r26-t37-01`, `solve-q-r26-t37-07`.
- Slides:
  - geo-159 slide "Stairs going down" and its sidebar entry.
  - geo-159 slide "The line equation": replace the example that refers to "our stairs going down". That is the draw note 'Write "y = −3/2 x + 6" next to the stairs-going-down line' and the next spoken line. Keep the rest of the slide.
- Questions: q-r26-t37-01, q-r26-t37-02, q-r26-t37-04, q-r26-t37-07, q-r26-t37-08, q-r26-t37-09. Then:
  - Update the practice order.
  - Renumber the guided questions. Removing the new Question 1 shifts the numbers back, so re-check the "in Question N" references that were renumbered.
- Card rows: mem-coordinates, the row "Slope | up ÷ across, with a sign: up to the right +, down to the right −".

## ORIGINAL ITEMS REMOVED BY FIXERS (restore candidates)
- Questions: geo37-core-p16 (a line through (−4, 6) that does not cut the y-axis) was unplaced.
- Slides and lines replaced:
  - solve-geo37-g164 slide 5. The line "In the Hebrew version we compared the top dark piece with a square …" was replaced.
  - solve-geo37-g160 slide 2. The line "A is (−2a, −2b) — so a and b are positive, because A is in the negative region." was replaced.
  - solve-geo37-g160 slide 3. The line "once I raise them to a power I can't cancel" was replaced, and a new slide was inserted before it.
  - solve-geo37-g167 slide 3. The board line "1. Parallel to one axis → perpendicular to the other — they never meet" was wrong and was replaced, along with its spoken line.
  - geo-157 slide 3. The line "if the circle is tangent to both x and y, the centre must have the same x and y" was replaced.
  - solve-geo37-g158 slide 4. The line "three, three, three, three — 12" was replaced.
  - solve-geo37-g166 slide 3. The board "10:4 = 5: ?" and the "If you prefer an equation …" line were replaced.
- Numbering: the guided questions were renumbered (old Q1 → Q2 …), and "in Question N" references inside videos were auto-updated.
- Figures:
  - geo-154 slides 5–7 now show one point each.
  - geo37-core-p10: the teal answer line was removed.
  - geo37-core-p25: the intercept labels 4 and 6 were removed.
  - Label moves on Q3, Q4, Q5 and Q8 and on p02, p04, p05, p09, p15 and p20.
