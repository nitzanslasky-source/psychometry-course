# Audit: Topic 34 (Polygons). Were the additions justified by the real exam?

Sources: `math_patches/t34_CHANGES.md`, `math_patches/t34.py`, `real_exam/quant_real.md` (regenerated full-text version), and the pre-patch course `course18.json` (to see which original questions need a method).
Real-exam groups read in full: polygons (11), circles (37), quadrilaterals (43), triangles (24), geometric_comprehension (9). I also searched all 760 questions for: diagonal, exterior, hexagon, octagon, "how many sides", common vertex.

Rules applied (brief + coordinator):
- An added topic, rule or question type stays only if the real exam has it.
- If an added method is needed to solve ORIGINAL course questions, its teaching stays (rule 2).
- An added question whose type exists only in the original course, and not on the real exam, is removed. The original questions of that type stay.

Main findings from the real exam:
- **Angles of regular polygons: common.** 2023_spring_q2_03 (pentagon, 108°), 2020_winter_q2_04 (pentagon, 36°), 2026_spring_q2_19 (9-gon, 20°), 2020_spring_q1_17 (pentagons around a point, 144°), 2024_winter_q1_18 (hexagon + square). Angle-sum questions: 2025_autumn_q2_06 (21 sides vs 17 sides), 2025_winter_q1_03 (pentagon).
- **Polygons meeting at a point / on a common side: 2 questions.** 2024_winter_q1_18 (regular hexagon + square FGHE on side FE, α = 75°): this is exactly the new lesson's hexagon + square gap triangle. 2020_spring_q1_17 (5 pentagons with a common vertex).
- **Regular hexagon lengths: 4 questions.** 2023_autumn_q2_02 (trapezoid ABCF, long diagonal 2a), 2025_spring_q1_18 (hexagon in a rectangle, short diagonal a√3), 2023_winter_q2_05 (DG with CE ⊥ DG), 2025_winter_q2_15 (hexagon around a circle, r = a√3/2).
- **Number of diagonals (n − 3, n(n − 3)/2): 0 real questions.**
- **"Find n from one angle" (n = 360/(180 − angle)) and "could it be an angle of a regular polygon?": 0 real questions.** The only n ↔ angle question goes forward (2025_autumn_q2_06: n → angle sum).
- **Exterior angles by name: 0 real questions.** But 180° − 360°/n (the exterior/central-angle route) solves the regular-angle questions above.
- **Regular-octagon area (octagon cut from a square): 0 real questions.** The only octagon questions are 2025_winter_q2_06 (a lattice octagon, area by counting) and 2024_autumn_q1_13 (which diagonal can be a diameter).
- **Original course needs:** geo34-core-p23 ("nine diagonals from each vertex") needs n − 3. geo34-core-p21 (150° → n) and geo34-core-p22 (interior = 4 × exterior) need exterior angles and n = 360/exterior. So these teachings stay under rule 2.

| Addition | Where | Class | Verdict | Evidence |
|---|---|---|---|---|
| p12 solution without "tangent–chord = half the arc" | geo34-core-p12 solution | FIX | KEEP | correction |
| Q9 "measure with your fingers" replaced by the real reason | solve-geo34-g114 slide 4 | FIX | KEEP | correction |
| "How many diagonals" (n − 3 from one vertex, n(n − 3)/2 in all) | geo-104 new slide 5 "How many diagonals"; recap board line "Diagonals: n − 3 … n(n − 3)/2"; mem-polygons row "Diagonals" | METHOD needed by original items | KEEP (rule 2) | 0 real questions; needed for original geo34-core-p23 (and used in p11's solution) |
| "Exterior angles" (sum 360°, regular: 360°/n = central angle) | geo-104 new slide 12 "Exterior angles" + figure; recap line "Exterior angles: 360° in all"; mem-polygons row "Exterior angles" | METHOD | KEEP | regular-angle questions 2023_spring_q2_03, 2020_spring_q1_17, 2024_winter_q1_18 (also 2026_spring_q2_19); needed for original p21, p22 |
| "Angle → sides": n = 360/(180 − angle), example 150° → 12 | geo-104 new slide 13 "Angle → sides" (first part, up to the "150°: … 12 sides" board item); recap part "regular: n = 360°/(180° − angle)"; mem-polygons row "Sides from one angle (regular)" | METHOD needed by original items | KEEP (rule 2) | 0 real questions; needed for original geo34-core-p21 and p22 |
| "Could it be an angle of a regular polygon?" (140° yes, 130° no) | geo-104 slide 13 "Angle → sides", the last 5 script lines (from "And a classic exam question…" to the board item "Could it be an angle of a regular polygon? 180 − angle must divide 360"); mem-polygons tip "Could it be an angle of a regular polygon? …" | CONTENT | REMOVE | 0 real questions; not needed by any original question. (The slide calls it "a classic exam question", which is false.) |
| Concave polygons: angle sum still 180(n − 2) | geo-104 slide 6 two spoken lines; mem-polygons tip "A concave polygon …" | FIX (explains the original folded-hexagon figure) | KEEP | clarification of an original slide |
| New lesson "Polygons Meeting at a Point" (hexagon + square, gap 150°, isosceles, 15°; honeycomb recap) | video r26-t34-meet (4 slides) | CONTENT | KEEP | 2024_winter_q1_18 (same picture), 2020_spring_q1_17. Count: 2 |
| Card "Polygons meeting at a point" | mem-r26-t34-meet | CONTENT | KEEP | same as above |
| Guided Q13: each angle 160° → 18 sides | q-r26-t34-01 + video solve-q-r26-t34-01 | question type "n from an angle" | REMOVE | 0 real questions of this type (only original p21/p22 have it) |
| Guided Q14: 7 diagonals from one vertex → 35 in all | q-r26-t34-02 + video solve-q-r26-t34-02 | question type "count diagonals" | REMOVE | 0 real questions (only original p23 has it) |
| Guided Q15: square + regular pentagon on a common side, ∠ADG = 9° | q-r26-t34-03 + video solve-q-r26-t34-03 | CONTENT (polygons on a common side) | KEEP | 2024_winter_q1_18 (hexagon + square on a common side) |
| Q6 video: short diagonal = side·√3, long diagonal = 2·side | solve-geo34-g112 slide 3, two spoken lines | METHOD | KEEP | 2025_spring_q1_18, 2023_autumn_q2_02, 2025_winter_q2_15 |
| Card table "Regular hexagon, side a" (radius a, short diagonal a√3, long 2a, area, ACE = ½, ACDF = ⅔) | mem-hexagon-partitions new table | METHOD | KEEP | 2025_spring_q1_18, 2023_autumn_q2_02, 2023_winter_q2_05, 2025_winter_q2_15. Count: 4 |
| "Haman's ear" explained, also called "star partition" | geo-112-after slide 4; mem-hexagon-partitions row name | FIX | KEEP | wording |
| All 37 written solutions rewritten in TeX; stems (cases blocks, "marked x"), p09 method, ":" → fractions, "5: 540°" board, American spelling | guided + practice solutions; geo-104 slide 5 board; Q4/Q5/Q6 boards | FIX | KEEP | wording/notation |
| Figures: p09 extra FC removed, Q5 "O" moved, v487 description, 24 figures cropped | question figures and their slide copies | FIX | KEEP | figures |
| Practice: regular decagon angle (144°) | q-r26-t34-04 | question type: regular-polygon angle | KEEP | 2023_spring_q2_03, 2020_winter_q2_04, 2026_spring_q2_19 |
| Practice: exterior angle 24° → angle sum 2,340° | q-r26-t34-05 | question type "n from an angle" | REMOVE | 0 real questions |
| Practice: which could be an angle of a regular polygon? (140°) | q-r26-t34-06 | CONTENT | REMOVE | 0 real questions |
| Practice: 20 diagonals → 8 sides | q-r26-t34-07 | question type "count diagonals" | REMOVE | 0 real questions |
| Practice: square + hexagon + unknown regular polygon fill a point → 12 | q-r26-t34-08 | polygons at a point | KEEP | 2020_spring_q1_17, 2024_winter_q1_18 |
| Practice: pentagon with inner equilateral triangle ABF, ∠AEF = 66° | q-r26-t34-09 | regular-pentagon angle chase | KEEP | 2023_spring_q2_03, 2020_winter_q2_04 |
| Practice: octagon cut from a square with side 2 + √2, area 4 + 4√2 | q-r26-t34-10 | regular-octagon area (original-course type: g108, g115) | REMOVE | 0 real questions of this type |
| Practice: hexagon side 4, area of ACDF = 16√3 | q-r26-t34-11 | hexagon diagonals/areas | KEEP | 2025_spring_q1_18, 2023_autumn_q2_02 |

## TO REMOVE
- Videos: `solve-q-r26-t34-01`, `solve-q-r26-t34-02`.
- Slides: geo-104 slide 13 "Angle → sides": remove only the last 5 script lines, from "And a classic exam question: which of these could be an angle of a regular polygon?" to the board item "Could it be an angle of a regular polygon? 180 − angle must divide 360". The rest of the slide stays.
- Questions: q-r26-t34-01, q-r26-t34-02, q-r26-t34-05, q-r26-t34-06, q-r26-t34-07, q-r26-t34-10. Update the practice order and the guided numbering (Q13 and Q14 disappear, and the "Advanced Polygons III" group keeps only Q15).
- Card rows: mem-polygons, the tip "Could it be an angle of a regular polygon? Only if 180° − angle divides 360° exactly."

## ORIGINAL ITEMS REMOVED BY FIXERS (restore candidates)
- Questions unplaced:
  - geo34-core-p03 (900° → heptagon)
  - geo34-core-p14 (1,980° → 13 sides)
- Slides and lines replaced:
  - solve-geo34-g114 slide 4. The whole script was rewritten. The removed text said the drawing is accurate and you can "measure with your fingers". That was a wrong claim, so restore it only if the teacher wants it back.
  - geo-104 slide 5. The board item "5: 540° → 6: 720° → 7: 900° → 8: 1080°" was replaced.
  - geo-112-after slide 4. The line "… fold the three corners in, like the paper, and you get a hamantasch" was replaced.
- Solutions changed in method:
  - geo34-core-p09 used the circle; it now uses the trapezoid ABGH.
  - geo34-core-p12 used tangent–chord = half the arc; it now uses radius ⊥ tangent.
  - All the other written solutions were reworded.
- Figures changed:
  - geo34-core-p09: segment FC removed.
  - geo34-g111: the O label moved.
  - 24 question figures were cropped.
