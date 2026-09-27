# Audit: Topic 36 (Similarity and scale). Were the additions justified by the real exam?

Sources: `math_patches/t36_CHANGES.md`, `math_patches/t36.py`, `real_exam/quant_real.md` (regenerated full-text version), and the pre-patch course `course18.json`.
Real-exam groups read in full: similarity (4), triangles (24), quadrilaterals (43), 3d_geometry (32), circles (37). I also searched all 760 questions for: scale, map, percent/% together with area/side/volume, sphere, parallel, similar.

Rules applied (brief + coordinator):
- An added topic, rule or question type stays only if the real exam has it.
- An added method that ORIGINAL course questions need stays (rule 2).
- An added question whose type exists only in the original course, and not on the real exam, is removed.

Main findings from the real exam:
- **Same height → area ratio = base ratio: very common (5+).** 2025_autumn_q1_13 (trapezoid, ABD : DBC = a : b), 2026_spring_q1_08 (trapezoid, ABD = ¾x), 2023_winter_q2_13 (PBC = ⅔ ABC → PC), 2025_autumn_q2_04, 2022_autumn_q1_02.
- **Line parallel to a side (parts and whole side): 3 real questions.** 2019_spring_q2_02 (ED ∥ BC, trapezoid area), 2023_winter_q2_12 (AB ∥ DE, DC = ⅓AC, dark area 8x), 2020_autumn_q2_02 (trapezoid cut by EF).
- **Trapezoid with its diagonals (a², ab, ab, b²): 2 real questions.**
  - 2019_winter_q1_19: square, trapezoid ABFE, ABG = 16·EFG, answer ⅖a². This is exactly the a², ab, ab, b² split.
  - 2026_spring_q1_08: trapezoid, triangles ABC vs ABD.
- **Altitude to the hypotenuse: 2 real questions.** 2020_autumn_q2_20 (right triangle, AD = √6, which fits h² = p·q = 2·3; the figure is not in the text) and 2026_spring_q1_16 (rectangle in a right triangle, AE = 4/x, a product rule from similar triangles).
- **Map scale: 1 real question.** 2026_spring_q1_18 (smallest scale so that 5 m ≥ 0.1 mm on the map → 1 : 50,000). It is a length scale that asks you to find the scale. There are 0 real map-area questions, but the original geo36-core-p23 is a map-area question.
- **Percent change of lengths → area/volume: 0 real questions.** The only real factor question is 2026_spring_q1_20 (volume × 2 → surface × (∛2)²), and the original k² / k³ rule already covers it. The original geo36-core-p20 (area +125% → side?) and the moved geo35-core-p27 (dimensions −25%) need the percent → factor → power → percent route.
- **Cone filled to part of its height (the water forms a similar cone): 0 real questions.** The original geo36-core-p16 is a cone cut parallel to its base at ⅔ of the height.

| Addition | Where | Class | Verdict | Evidence |
|---|---|---|---|---|
| Q3 "the common mistake won't be in the choices" → "a trap can be there at any level" | solve-geo36-g138 slide 3 | FIX | KEEP | correction |
| Q6 "Corresponding angles …"; slide 5 uses part to part instead of "work across ×1.25" | solve-geo36-g144 slides 2 and 5 | FIX | KEEP | correction |
| Q5 trap 256 explained correctly | solve-geo36-g142 slide 3 | FIX | KEEP | correction |
| "From the course —" removed; SSS/SAS "rarely needed"; "Man with glasses" with one image only; "On the exam"; spelling | geo-143 slide 6; geo-139 recap; geo-134 slide 12 | FIX | KEEP | wording |
| "Part to part" slide (AD/DB = AE/EC, but DE ↔ the WHOLE side) | geo-139 new slide 8 "Part to part"; recap line; mem-similar-triangles "Shortcuts" row 1 | METHOD | KEEP | 2019_spring_q2_02, 2023_winter_q2_12, 2020_autumn_q2_02 |
| Altitude to the hypotenuse: h² = p·q, leg² = part·hypotenuse (numbers 6, 8, 10) | geo-139 slide "Altitude to hypotenuse" (added lines, figure numbers); solve-geo36-g146 slide 3 (Q8) shortcut lines "h² = p · q = 9 · 16"; mem-similar-triangles "Shortcuts" row 3 | METHOD | KEEP | 2020_autumn_q2_20, 2026_spring_q1_16 |
| "Same height" slide (area ratio = base ratio, no squaring) | geo-139 new slide "Same height"; recap line; mem-similar-triangles "Shortcuts" row 2 | METHOD | KEEP | 2025_autumn_q1_13, 2026_spring_q1_08, 2023_winter_q2_13, 2025_autumn_q2_04, 2022_autumn_q1_02 |
| "Trapezoid diagonals" slide (a², ab, ab, b²) | geo-139 new slide "Trapezoid diagonals"; mem-similar-triangles "Shortcuts" row 4 | METHOD | KEEP | 2019_winter_q1_19, 2026_spring_q1_08 |
| Rectangle on the diagonal: a worked example with numbers | geo-139 slide 11 "Rectangle on diagonal" (rewritten) | FIX | KEEP | makes an original slide concrete |
| "NOT always similar: rectangles, rhombuses, isosceles, right triangles" | geo-135 slide 2 (added lines); mem-similarity tip | FIX | KEEP | clarification (see 2023_spring_q2_14: equal angles but not congruent) |
| "All spheres are similar" | geo-141 slide 3; mem-similar-solids tip | FIX | KEEP | needed for the original Q12 (geo36-g150) |
| "Half-height cone" slide (water to half the height = ⅛) | geo-141 new slide 6 "Half-height cone" (+ figure); sidebar entry; mem-similar-solids row "Cone filled to half its height" | CONTENT | UNSURE | 0 real questions. It removes a trap, but the original geo36-core-p16 (a cone cut parallel to its base at ⅔ of the height) can be solved with the original k³ slides. Keep it only if the teacher thinks p16 needs this picture |
| "Percent change" slide (percent → factor → power → back; +10% → +21% / +33.1%; area +44% → sides +20%) | geo-143 new slide 8 "Percent change"; recap line "Percent: turn it into a factor first …"; mem-similar-solids row "Sides +10%"; tip "Percent → factor → power → back to percent" | METHOD needed by original items | KEEP (rule 2) | 0 real questions; needed for original geo36-core-p20 (area +125% → side) and geo35-core-p27 (now in this practice) |
| New lesson "Map Scale" (1 : n, units ladder, length example, area example, recap) | video r26-t36-map-scale (6 slides) | CONTENT | KEEP | Length: 2026_spring_q1_18 (1 real question). Area: 0 real questions, but needed for original geo36-core-p23 (map area), so kept under rule 2 |
| Card "Map scale" | mem-r26-t36-map-scale | CONTENT | KEEP | same as above |
| Card tip "Stuck? Plug in …" | mem-similar-triangles tip | METHOD | KEEP | 2023_winter_q2_12 (x in the choices), 2024_winter_q1_03 |
| Guided: same height, BD : DC = 2 : 3, total 40 → ABD = 16 | q-r26-t36-01 + video | same height | KEEP | 2023_winter_q2_13, 2025_autumn_q1_13 |
| Guided: trapezoid bases 4, 6, AOB = 8 → 50 | q-r26-t36-02 + video | trapezoid diagonals | KEEP | 2019_winter_q1_19 |
| Guided: cube edge +20% → volume +72.8% | q-r26-t36-03 + video solve-q-r26-t36-03 | percent change (original-only type) | REMOVE | 0 real (original p20 and p27 stay) |
| Guided: 1 : 20,000, 7.5 cm → 1.5 km | q-r26-t36-04 + video | map length scale | KEEP | 2026_spring_q1_18 |
| Guided: 1 : 40,000, 5 cm² → 0.8 km² | q-r26-t36-05 + video solve-q-r26-t36-05 | map area (original-only type) | REMOVE | 0 real (original p23 stays) |
| Written solutions/stems rewritten (TeX, cases, "ratio", traps named); p19 wording; p04 note | all guided + original practice | FIX | KEEP | wording |
| Figures: Q5 two plain cubes; v646 turned triangle; v648 numbers; v656 radii; label moves; alt text | geo36-g142 + slides; v646, v648, v656, v631, v632; Q9, Q12 | FIX | KEEP | figures |
| Practice: part to part, EC = 9 | q-r26-t36-06 | parallel line | KEEP | 2019_spring_q2_02, 2023_winter_q2_12 |
| Practice: segment vs the whole side, BC = 10 | q-r26-t36-07 | parallel line | KEEP | 2019_spring_q2_02, 2023_winter_q2_12 |
| Practice: same height, BD = 8 | q-r26-t36-08 | same height | KEEP | 2023_winter_q2_13, 2025_autumn_q1_13 |
| Practice: ADE : DBE = 1 : 2 (same height inside a parallel picture) | q-r26-t36-09 | same height | KEEP | 2023_winter_q2_12, 2025_autumn_q1_13 |
| Practice: trapezoid AOB = 4, COD = 25 → BOC = 10 | q-r26-t36-10 | trapezoid diagonals | KEEP | 2019_winter_q1_19 |
| Practice: trapezoid bases 3, 9 → COD = 9/16 | q-r26-t36-11 | trapezoid diagonals | KEEP | 2019_winter_q1_19 |
| Practice: leg² = part·hypotenuse, AB = 10 | q-r26-t36-12 | altitude to the hypotenuse | KEEP | 2020_autumn_q2_20, 2026_spring_q1_16 |
| Practice: cone glass to ⅔ of its height → 64 | q-r26-t36-13 | cone filled to part of its height | REMOVE | 0 real |
| Practice: sphere radius −10% → surface −19% | q-r26-t36-14 | percent change (original-only type) | REMOVE | 0 real |
| Practice: circle area +69% → radius +30% | q-r26-t36-15 | percent change (original-only type) | REMOVE | 0 real |
| Practice: 36 km = 12 cm → scale 1 : 300,000 | q-r26-t36-16 | map length scale (find the scale) | KEEP | 2026_spring_q1_18 (also asks for the scale) |
| Practice: two maps, 18 cm² → 2 cm² | q-r26-t36-17 | map area (original-only type) | REMOVE | 0 real |
| Practice: 1 : 5,000, 4 × 3 cm field → 30,000 m² | q-r26-t36-18 | map area (original-only type) | REMOVE | 0 real |

## TO REMOVE
- Videos: `solve-q-r26-t36-03`, `solve-q-r26-t36-05`. If the UNSURE item resolves to remove, also remove geo-141 slide "Half-height cone".
- Slides:
  - None for sure.
  - UNSURE: geo-141 slide 6 "Half-height cone" and its sidebar entry "Half-height cone".
- Questions: q-r26-t36-03, q-r26-t36-05, q-r26-t36-13, q-r26-t36-14, q-r26-t36-15, q-r26-t36-17, q-r26-t36-18. Update the practice order and the guided numbering. The Map Scale solution group keeps only q-r26-t36-04.
- Card rows:
  - UNSURE: mem-similar-solids, the row "Cone filled to half its height".

## ORIGINAL ITEMS REMOVED BY FIXERS (restore candidates)
- Questions unplaced:
  - geo36-core-p10 (tangent circles)
  - geo36-core-p15 (the heptagon)
- Topic 35's patch moved geo35-core-p27 into this practice. See audit_t35.
- Slides and lines replaced:
  - geo-134 slide 12 ("man with glasses"). The extra images (Kenny, Batman, binoculars) were removed. The lines "… like Kenny from South Park, with a pair of binoculars" and "… this 'Batman' up here" were replaced.
  - geo-143 slide 6. The words "From the course —" were removed.
  - solve-geo36-g138 slide 3. The lines "A small tip about answers: usually they don't confuse me — they help me." and "In a harder question, the common mistake usually won't even be in the choices …" were replaced.
  - solve-geo36-g144 slide 5. The whole script was rewritten; the removed step was "work across ×1.25". Slide 2's line "Parallel lines, equal acute angles" was also replaced.
  - solve-geo36-g142 slide 3. The explanation of 256 was replaced.
  - geo-139 slide 11 ("Rectangle on diagonal") and slide 12 ("Recap"). Both scripts were fully rewritten.
  - solve-geo36-g148 slide 5 (Q10). The board item "15:3" became "15 ÷ 3".
- Figures:
  - geo36-g142 (Q5). The 4×4×4 grid block was replaced by two plain cubes, on the question and on both slides.
  - v646 ("Turn it around") was redrawn.
  - v648 and v656 were changed.
