# Audit: Topic 38 (Geometric reasoning). Were the additions justified by the real exam?

Sources: `math_patches/t38_CHANGES.md`, `math_patches/t38.py`, `real_exam/quant_real.md` (regenerated full-text version), and the pre-patch course `course18.json`.
Real-exam groups read in full: geometric_comprehension (9), triangles (24), quadrilaterals (43), 3d_geometry (32), circles (37), lines_angles (13). I also searched all 760 questions for: obtuse/acute, bisect, greatest/largest/maximal, "cannot be determined"/"necessarily", plane/cross-section, unfold/shortest/ant.

Rules applied (brief + coordinator):
- An added topic, rule or question type stays only if the real exam has it.
- An added method that ORIGINAL course questions need stays (rule 2).
- An added question whose type exists only in the original course, and not on the real exam, is removed.

Main findings from the real exam:
- **Two fixed sides, a free angle (the rods rule, the greatest area ab): 2 real questions.**
  - 2025_spring_q1_15 (full text now: parallelogram with sides x, y and 0° < α < 90°; the necessarily true answer is S < x·y).
  - 2025_winter_q1_13 ("Which of the two triangles has the larger area? – equal"). The figure is not in the text, but the pattern fits θ vs 180° − θ.
- **Same base, apex on a parallel line → same area: 3 real questions.** 2020_spring_q1_06 (a ∥ b, trapezoid areas equal), 2026_spring_q1_08 and 2025_autumn_q1_13 (trapezoid triangles on the same base).
- **Extreme cases / "necessarily" / "cannot be determined": very common.** 2024_spring_q2_14, 2024_winter_q1_20, 2026_spring_q2_16, 2023_winter_q1_14, 2024_autumn_q2_15, 2023_spring_q1_19, 2024_spring_q2_01.
- **Acute/right/obtuse from the three sides (c² vs a² + b²): 0 real questions.** The obtuse questions go by angles (2019_winter_q1_05: 3 : 1 : 1) or by altitudes (2022_autumn_q2_06).
- **Angle-bisector ratio: 0 real questions.** The only bisector hits (2022_autumn_q2_02, 2021_spring_q1_06) are about angles or diagonals, not the ratio.
- **Cube cross-sections, shortest path on a cube's surface, a point inside/outside a circle from an angle on a diameter, circle vs square with equal perimeters: 0 real questions each.**

| Addition | Where | Class | Verdict | Evidence |
|---|---|---|---|---|
| Q9 math error fixed (3, 6 and 60° is 30-60-90, not equilateral), rods-rule name, "height grows only up to 90°", 105° = 75° area, Q9 solution | solve-geo38-g183 slides 2–5; geo38-g183 solution | FIX | KEEP | correction |
| Q4 / Q5 near-true first figures + exaggerated later figures; "look about equal" now matches | geo38-g178, geo38-g179 figures + their video slides | FIX | KEEP | figures |
| Q3 pointer → rods rule; "vertex moves straight away" + warning; Q12 "edges" → "extremes"; one goodbye only | solve-geo38-g176 s3/s4; geo-175 s3; solve-geo38-g186; last guided video | FIX | KEEP | wording |
| "Two rods" slide (wider angle → longer third side; height and area grow up to 90°, then shrink; θ and 180° − θ same area) | geo-175 new slide "Two rods" (+ figure); mem card row "Two fixed sides, the angle opens" | METHOD | KEEP | 2025_spring_q1_15, 2025_winter_q1_13 |
| "Greatest area" slide (triangle ab/2, parallelogram ab) | geo-175 new slide "Greatest area"; mem card row "Greatest area with sides a, b" | METHOD | KEEP | 2025_spring_q1_15 (S < xy) |
| "Acute or obtuse?" slide (c² vs a² + b², example 7, 8, 10) | geo-175 new slide "Acute or obtuse?"; mem card row "Acute, right or obtuse?" | CONTENT | REMOVE | 0 real questions; no original question needs it |
| Guided: sides 6 and 10 → greatest area 30 (trap 24) | q-r26-t38-01 + video | rods rule | KEEP | 2025_spring_q1_15 |
| "Slide the apex" slide (same base, apex on a parallel → same area, perimeter changes) | geo-177 new slide "Slide the apex" (+ figure); mem card row "Slide the apex" | METHOD | KEEP | 2020_spring_q1_06, 2026_spring_q1_08, 2025_autumn_q1_13 |
| "Push to the extremes" slide (end, middle, find what is free; "cannot be determined" check) | geo-177 new slide "Push to the extremes"; mem card rows "Must / could / cannot", "Flexible drawing", "Extreme cases", "Cannot be determined?"; the 2 new tips | METHOD | KEEP | 2024_spring_q2_14, 2024_winter_q1_20, 2026_spring_q2_16, 2023_winter_q1_14, 2024_autumn_q2_15 |
| Guided: trapezoid diagonals → area ABE = area DCE | q-r26-t38-02 + video | same base, same height | KEEP | 2026_spring_q1_08, 2025_autumn_q1_13 |
| Q10 angle-bisector ratio shortcut (KN/NL = KM/ML) | solve-geo38-g184 slide 5 (the board item "Shortcut: KN/NL = KM/ML > 1" + 2 spoken lines); the geo38-g184 solution line "Shortcut: the bisector gives …" | METHOD | REMOVE | 0 real bisector-ratio questions. The original Q10 already has its own congruence solution, so the shortcut is not needed (the fixer doubted it too) |
| Q4 video line "TR is free — that's the 'find what is free' check" | solve-geo38-g178 slide 4 | METHOD | KEEP | ties Q4 to the extremes checklist (evidence as above) |
| Memory card moved to the end of the learn section | mem card (CARD) move | FIX | KEEP | order |
| p03, p19, p22 and Q2–Q10 solutions rewritten; ". So"; spelling | solutions | FIX | KEEP | wording |
| Figures: Q9 H cut off, v788 labels, p04 "O", p06 semicircle removed, p20 segment removed, p21 redrawn | figures | FIX | KEEP | figures |
| Practice: parallelogram 4 and 9, greatest area 36 | q-r26-t38-03 | rods rule | KEEP | 2025_spring_q1_15 |
| Practice: ∠APB = 100° on a diameter → P inside | q-r26-t38-04 | point vs circle from an angle | REMOVE | 0 real |
| Practice: 5, 12, x with 13 < x < 17 → obtuse | q-r26-t38-05 | acute/obtuse from sides | REMOVE | 0 real |
| Practice: P slides on a parallel, area fixed, perimeter changes | q-r26-t38-06 | slide the apex | KEEP | 2020_spring_q1_06, 2026_spring_q1_08 |
| Practice: cube cross-section, 7 sides impossible | q-r26-t38-07 | plane sections (original-only type, cf. geo38-g186) | REMOVE | 0 real |
| Practice: shortest path on a cube, 2√5 | q-r26-t38-08 | surface path | REMOVE | 0 real |
| Practice: 50° vs 130° → same area, longer third side | q-r26-t38-09 | rods rule | KEEP | 2025_winter_q1_13, 2025_spring_q1_15 |
| Practice: sides 6 and 8, area 25 impossible | q-r26-t38-10 | rods rule / greatest area | KEEP | 2025_spring_q1_15 |
| Practice: circle vs square with equal perimeter → 4 : π | q-r26-t38-11 | shape efficiency (original-only type, cf. geo38-g173) | REMOVE | 0 real |

## TO REMOVE
- Videos: none (both new solution videos stay).
- Slides:
  - geo-175 slide "Acute or obtuse?" and its sidebar entry.
  - solve-geo38-g184 slide 5: the board item "Shortcut: KN/NL = KM/ML > 1" and its 2 spoken lines ("A shortcut for strong students: …", "KN to NL is like KM to ML …").
- Questions:
  - q-r26-t38-04, q-r26-t38-05, q-r26-t38-07, q-r26-t38-08, q-r26-t38-11. Update the practice order.
  - geo38-g184 solution: remove the added line "Shortcut: the bisector gives KN/NL = KM/ML, and KM > ML (KM is the hypotenuse)."
- Card rows: the geo38 memory card, the row "Acute, right or obtuse? | longest side c: …".

## ORIGINAL ITEMS REMOVED BY FIXERS (restore candidates)
- Questions unplaced:
  - geo38-core-p18 (a square and a rectangle, both with perimeter 32)
  - geo38-core-p26 (4 vertical + 3 horizontal lines, counting)
- Slides and lines replaced:
  - solve-geo38-g183 slide 2. The statement "A 60 degree angle would send us straight to an equilateral triangle" was mathematically wrong and was replaced. Slide 3's "angle-opening principle" was renamed.
  - solve-geo38-g176. The goodbye lines "What can I wish you …" were removed and moved to the last guided video.
  - geo-175 slide 3. The board rule and the spoken line "If I move the vertex away …" were rewritten ("straight away").
  - solve-geo38-g186 (Q12). "edges" was reworded to "extremes" on the board and in the spoken lines.
  - geo38-g184 (Q10) and the solutions of Q2, Q3, Q4, Q5, Q8, Q9, p03, p19 and p22 were rewritten.
- Figures:
  - geo38-g178 (Q4) and geo38-g179 (Q5): the question figures and the slide copies were replaced by new first and exaggerated drawings.
  - geo38-g183 (Q9): the figure was replaced.
  - geo38-core-p06: the semicircle was removed.
  - geo38-core-p20: the orange segment was removed.
  - geo38-core-p21: the figure was redrawn.
  - v788: the labels were moved.
