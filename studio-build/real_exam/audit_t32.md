# Audit T32 – Quadrilaterals (report only, nothing edited)

Sources: `math_patches/t32_CHANGES.md`, `math_patches/t32.py`, `real_exam/quant_real.md` (regenerated), real exam figures
(all 43 quadrilaterals questions + polygons + geometric_comprehension viewed), pre-patch course `course18.json`.

Policy: same as audit_t30.md. A rule the ORIGINAL course questions need is kept (coordinator rule 2). A new question whose
type is not on the real exam but is already tested by original course questions is UNSURE; not on the real exam and not in
the original course is REMOVE.

Key real-exam facts checked on the figures: no concave (arrow) quadrilateral anywhere; no trapezoid midsegment / midpoints
of the legs; no trapezoid with both diagonals and the "side triangles equal" (butterfly) question; no percent change of an
area; perimeter-of-pieces questions are frequent.

| Addition | Where (video id / slide / question ids) | Class | Verdict | Evidence (real question ids / count) |
|---|---|---|---|---|
| "NOT" → "not necessarily" (rectangle, parallelogram, rhombus, kite diagonals); trapezoid = exactly one pair of parallel sides; Q2/Q10/Q15 wording; properties card | geo-042/rectangle/parallelogram/rhombus/kite/trapezoid lesson slides; solve-geo32-g046, -g059, -g066; card mem-quad-family | FIX | KEEP | 2021_spring_q1_06 ("not necessarily true" about a quadrilateral), 2026_spring_q2_16 |
| Family tree "Who is also who?" + card tip | geo-042 new slide "Who is also who?"; card mem-quad-family tip | METHOD | KEEP | 2021_spring_q1_06, 2026_spring_q2_16, 2024_autumn_q1_13 (the original geo-042 already derives shapes from each other) |
| "Not sure? Sketch an extreme version" tip | card mem-quad-family tip | METHOD | KEEP | 2026_spring_q2_16, 2021_spring_q1_06 |
| Arrow rule: notch angle = sum of the other three | geo-042 new slide "The arrow rule"; card mem-quad-family tip "Concave (arrow)" | CONTENT | REMOVE | 0 real (no concave quadrilateral in 760); no original question uses it |
| Length ×k → area ×k² | geo-043 new slide "Scale it up"; card mem-quad-area tip | METHOD | KEEP | 2022_autumn_q2_08 (area doubles → side ×√2), 2024_winter_q1_03 (area ×9 → side ×3), 2023_winter_q2_12. Also original fp24, fp25 |
| Parallelogram with a 30°/45°/60° angle; height drawn from A | geo-047 new slide "Special angles"; card mem-quad-area Parallelogram row | METHOD | KEEP | 2025_autumn_q2_05 (rhombus, 45°, side √2 → height 1), 2024_winter_q1_02 (45° in a square) |
| Trapezoid midsegment; area = midsegment × h | geo-054 new slide "The midsegment"; card mem-quad-area Trapezoid row "or midsegment × h" | CONTENT | REMOVE | 0 real; no original question |
| Isosceles trapezoid: opposite angles sum 180° | trapezoid lesson, isosceles slide (board + spoken); card row "Isosceles trapezoid" | METHOD | KEEP (rule 2) | Needed by original geo32-foundation-p02. Real: 0 direct |
| Right trapezoid: drop one height (new figure) + card tips | trapezoid lesson, right-trapezoid slide; card mem-quad-area tip; mem-quad-family tip "Right trapezoid" | METHOD | KEEP | 2019_spring_q2_02 (right trapezoid BCDE), 2020_autumn_q2_02, 2021_spring_q2_05, 2025_winter_q1_05 (drop heights) |
| Trapezoid "butterfly": the two side triangles have equal areas | geo-067-after new slide 8 "Trapezoid butterfly"; card mem-equal-heights row "Trapezoid with both diagonals"; card mem-quad-family Trapezoid row text "the two side triangles have equal areas" | CONTENT | REMOVE | 0 real (real trapezoid-area questions 2026_spring_q1_08, 2025_autumn_q1_13 are plain same-height ratios, no diagonals-crossing butterfly); no original question |
| Perimeter tricks: a cut counts twice; staircase = its rectangle; a notch adds 2 × depth; glued shapes | new video r26-t32-perimeter "Perimeter Tricks"; new card mem-r26-t32-perimeter | METHOD | KEEP | 2023_winter_q1_14 (notched rectangles, 1 cm around), 2024_autumn_q1_20 (bold path = perimeter), 2022_winter_q2_08, 2019_spring_q1_05, 2023_autumn_q1_13, 2022_winter_q2_14. Also original adv-p14, -p15, -p19, -p24 |
| Perimeter + diagonal → area identity (a+b)² = a²+b²+2ab | card mem-quad-area tip | METHOD | KEEP (rule 2) | Needed by original geo32-advanced-p21. Real: 0 |
| Work back from the answers | solve-geo32-g072 (Q21) new slide "Check from the answers" | METHOD | KEEP | 2023_spring_q1_18, 2024_autumn_q1_20, 2025_winter_q2_02 |
| Bisector in a parallelogram → isosceles triangle (named) | solve-geo32-g058 (Q9) new spoken line; card mem-quad-family tip | METHOD | KEEP (rule 2) | Original Q9 (geo32-g058) and foundation-p04 are solved exactly this way. Real: 0 |
| "Isosceles triangle with a 60° angle is equilateral" | solve-geo32-g060 (Q11) new spoken line | METHOD | KEEP | 2025_winter_q1_17, 2021_spring_q1_16 |
| Midpoint quadrilateral (rectangle → rhombus, square → half-area square) | card mem-quad-family tip | CONTENT | KEEP | 2021_autumn_q1_01 (midpoints of a 2×4 rectangle → rhombus of area 4). Also original geo33-advanced-p17 |
| Area = d₁·d₂/2 for ANY quadrilateral with ⊥ diagonals | card mem-quad-area new row | METHOD | KEEP (rule 2) | Needed by original geo32-advanced-p27; real for kite/rhombus/square: 2023_spring_q1_06 (square from diagonal), 2019_winter_q2_13 |
| Q10 video: simplest way first, others "(optional)"; Q11 video reorder; Q19 video: completions slide removed | solve-geo32-g059, -g060, -g070 | FIX | KEEP (see restore section) | – |
| All 91 solutions in TeX, stacked givens, ":" → "÷", US spelling, Q20 solution check | all geo32-* | FIX | KEEP | – |
| Figures fixed (slides 2/4 irregular quadrilateral, concave slide label, trapezoid slides, right trapezoid, Q13, Q18, adv-p18, -p12, -p20, -p06, -p02) | geo-042, trapezoid lesson, geo32-g062, -g069, advanced p02/p06/p12/p18/p20 | FIX | KEEP | – |
| Guided Q5: parallelogram with a 150° angle, height outside | q-r26-t32-01 + video solve-q-r26-t32-01 | CONTENT (type) | KEEP | 2025_autumn_q2_05, 2024_winter_q2_01 (parallelogram area from a height) |
| Guided Q9: right trapezoid, one height, one triple | q-r26-t32-02 + video solve-q-r26-t32-02 | CONTENT (type) | KEEP | 2019_spring_q2_02, 2020_autumn_q2_02 |
| Guided Q10: midsegment is the average of the bases | q-r26-t32-03 + video solve-q-r26-t32-03 | CONTENT (type) | REMOVE | 0 real (midsegment) |
| Guided Q12: arrow rule in a concave quadrilateral | q-r26-t32-04 + video solve-q-r26-t32-04 | CONTENT (type) | REMOVE | 0 real (concave) |
| Guided Q23: two side triangles of a trapezoid are equal | q-r26-t32-05 + video solve-q-r26-t32-05 | CONTENT (type) | REMOVE | 0 real (butterfly) |
| Guided Q27: staircase has the perimeter of its rectangle | q-r26-t32-06 + video solve-q-r26-t32-06 | CONTENT (type) | KEEP | 2023_winter_q1_14, 2024_autumn_q1_20, 2022_winter_q2_14 |
| Guided Q28: perimeter 34 + diagonal 13 → area | q-r26-t32-07 + video solve-q-r26-t32-07 | CONTENT (type) | UNSURE | 0 real; original type (geo32-advanced-p21) |
| Practice q-08: right trapezoid perimeter | q-r26-t32-08 (foundation) | CONTENT (type) | KEEP | 2019_spring_q2_02, 2020_autumn_q2_02 |
| Practice q-09: parallelogram 30°, area | q-r26-t32-09 (foundation) | CONTENT (type) | KEEP | 2025_autumn_q2_05 |
| Practice q-10: midsegment 9, bases differ by 4 | q-r26-t32-10 (foundation) | CONTENT (type) | REMOVE | 0 real |
| Practice q-11: arrow angle x = 160° | q-r26-t32-11 (foundation) | CONTENT (type) | REMOVE | 0 real |
| Practice q-12: length and width +10% → area +21% | q-r26-t32-12 (foundation) | CONTENT (type) | UNSURE | 0 real percent-change-of-area; original type (geo32-foundation-p24, -p25) |
| Practice q-13: midpoint square of a 10 cm square (50) | q-r26-t32-13 (foundation) | CONTENT (type) | KEEP | 2021_autumn_q1_01 |
| Practice q-14: butterfly, area COD | q-r26-t32-14 (foundation) | CONTENT (type) | REMOVE | 0 real |
| Practice q-15: hard butterfly (4 and 25 → 49) | q-r26-t32-15 (advanced) | CONTENT (type) | REMOVE | 0 real |
| Practice q-16: data sufficiency, midsegment + height | q-r26-t32-16 (advanced) | CONTENT (type) | REMOVE | 0 real (midsegment) |
| Practice q-17: notch perimeter (40) | q-r26-t32-17 (advanced) | CONTENT (type) | KEEP | 2023_winter_q1_14, 2024_autumn_q1_20 |
| Practice q-18: parallelogram 60°, area | q-r26-t32-18 (advanced) | CONTENT (type) | KEEP | 2025_autumn_q2_05 |
| Practice q-19: arrow with letters (α = 30°) | q-r26-t32-19 (advanced) | CONTENT (type) | REMOVE | 0 real |
| Practice q-20: right trapezoid with 45°, area | q-r26-t32-20 (advanced) | CONTENT (type) | KEEP | 2019_spring_q2_02, 2025_autumn_q2_05 (45° height) |
| Practice q-21: midpoint rhombus of a 6×8 rectangle, perimeter | q-r26-t32-21 (advanced) | CONTENT (type) | KEEP | 2021_autumn_q1_01 |

Counts: KEEP 27 (of which 4 FIX), REMOVE 12, UNSURE 2.

## TO REMOVE
- Video geo-042 (Quadrilaterals): slide "The arrow rule".
- Video geo-054 (Trapezoid): slide "The midsegment".
- Video geo-067-after (Equal Heights): slide 8 "Trapezoid butterfly".
- Questions + their solution videos: q-r26-t32-03 (solve-q-r26-t32-03, guided Q10), q-r26-t32-04 (solve-q-r26-t32-04, guided Q12), q-r26-t32-05 (solve-q-r26-t32-05, guided Q23). Update the group sidebars accordingly.
- Practice questions: q-r26-t32-10, q-r26-t32-11, q-r26-t32-14 (foundation); q-r26-t32-15, q-r26-t32-16, q-r26-t32-19 (advanced).
- Card mem-quad-family: tip "Concave (arrow): the angle in the notch = the sum of the other three angles."; Trapezoid row column 4 text "the two side triangles have equal areas" (restore the original cell).
- Card mem-quad-area: Trapezoid row column 3 text "or midsegment × h (midsegment = (a+b)/2)" (restore the original cell).
- Card mem-equal-heights: row "Trapezoid with both diagonals – The two side triangles have equal areas ("butterfly")".

## ORIGINAL ITEMS REMOVED BY FIXERS (to restore)
- geo32-foundation-p05 (unplaced): equilateral triangle side = perimeter of a square, triangle perimeter 216 → square side. (Real type exists: 2024_autumn_q1_17 perimeter/area of an equilateral triangle.)
- geo32-foundation-p08 (unplaced): four congruent squares, routes of sides/diagonals – which is shortest. (Real type exists: 2020_spring_q2_12, diagonal vs two sides.)
- geo32-foundation-p12 (unplaced): marked right angles, find α (angle chasing).
- geo32-foundation-p19 (unplaced): kite AB = 17, BO = 8, OC = 9 → area. (Real type exists: 2023_autumn_q1_06 kite area.)
- geo32-foundation-p22 (unplaced): rhombus diagonals 16 and 30 → perimeter. (Real type exists and is almost identical: 2019_winter_q2_13, rhombus diagonals 1 and 2 → perimeter.)
- solve-geo32-g070 (Q19): original slide 3 (the "completions" approach) removed; slide 4 renamed "Approach 2 · Split with symmetry"; spoken lines changed.
- solve-geo32-g059 (Q10): slides reordered (slide 5 moved to 4); "learn all three" / "it's important to know all of them" replaced by "(optional)".
- solve-geo32-g060 (Q11): slide 6 rewritten as "Way 1 · Two equilateral triangles"; the diagonal ways marked "(optional)".
- geo-042 slides 2 and 4: original quadrilateral figure (was a parallelogram) replaced; trapezoid slides 2–4 and right-trapezoid slide figures replaced (these are figure corrections).
