# Real-exam coverage audit: geometry (topics 30–38), 21 Oct 2026

Read-only audit. Sources: all 190 geometry questions in `studio-build/real_exam/quant_real.md` (quadrilaterals 43, circles 37, 3d_geometry 32, triangles 24, coordinate_system 17, lines_angles 13, polygons 11, geometric_comprehension 9, similarity 4). Course text from the scratchpad extract (`ext/course/t30–t38`, `q30–q38`, plus t51). I read every lesson in full and checked solution videos and practice items by id and grep.

Many exam stems refer to a figure that isn't in the text. I classified those by the idea the question asks for.

Ratings. **Explained:** clear = taught with the reason, a worked example and the conditions (W22); mentioned = named or used without being taught; missing = not there. **Practice:** practised = at least 2 course questions, at least one with a video; thin = 1 question, or written explanations only; none = no course question.

"V" = the course question has a solution video; "w" = written explanation only. Video ids leave out the `solve-` prefix. Recording status comes from `video_status.py --list record`. In geometry, only t33 and t34 still have videos to record. t30–t32 and t35–t38 are recorded or in production.

---

## Lines and angles (13)

| type | exam count + ids | explained where (rating) | practised where (rating) | flag |
|---|---|---|---|---|
| L1 Angles around a point, vertical angles, straight angle (3 lines through one point) | 4: 2020a q2_04, 2025s q1_04, 2025w q2_04 | geo-001, geo-001-2, r26-t30-summary-2 (clear) | g006 V, foundation-p01…p04, p17, advanced-p05, p10 (practised) | — |
| L2 Parallel lines + transversal: small/large angles, Z, U, zig-zag | 6: 2019s q1_09, 2019w q2_04, 2023w q2_03 | geo-001-3, geo-001-4, summary-2 auxiliary line (clear) | g002 V, g005 V, g007 V, q-r26-t30-03 V, foundation-p05…p13, advanced-p01 (practised) | — |
| L3 Are the lines parallel? Where do non-parallel lines meet? | 2: 2024w q2_14, 2021s q2_20 | Parallel test (U adds up to 180) in geo-001-4 (clear). **"The lines meet on the side where the two U angles add up to less than 180" is missing** (mentioned only) | q-r26-t30-01 V, q-r26-t30-04 w for the test; none for "which side" (thin) | 2021s q2_20 can't be solved from what we teach |
| L4 Three lines form a triangle: exterior angle | 1: 2025a q1_08 | t31 geo-009-2 (clear) | g010 V, advanced-p09 w (practised) | — |

## Triangles (24)

| type | exam count + ids | explained where (rating) | practised where (rating) | flag |
|---|---|---|---|---|
| T1 Angle chasing with isosceles triangles, angle sum, exterior angle; letters in the answers | 7: 2020a q1_03, 2021a q2_02, 2024a q2_07, 2026s q2_06, 2020w q1_04, 2025s q2_03 | geo-013, geo-009-2, r26-t31-summary-2 (plugging in) (clear) | g010, g011, g015, g031 V; foundation-p01, p05, p13…p20; advanced-p07, p15, p19, p20 (practised) | — |
| T2 Area comparisons: same base/height, median, sum of areas, equal areas with supplementary angles | 5: 2025a q2_04, 2019s q1_13, 2024s q1_04, 2023w q2_13, 2025w q1_13 | geo-016, geo-018-after, summary-2; the 40°/140° equal-area idea only in t38 summary (clear) | g017 V, g038 V, g018 V, q-r26-t36-01 V, q-r26-t38-01 V, foundation-p10, advanced-p08, p23, p27 (practised) | The 40/140 idea first appears in t38 (day 43), late for a triangle item |
| T3 Pythagoras, triples, 30-60-90 / 45-45-90, equilateral area | 5: 2020a q2_20, 2024a q2_02, 2021s q2_14, 2024a q1_17, 2025s q2_04 | geo-019, geo-024, geo-026, geo-027-after, geo-017-after (clear) | g020…g028 V, q-r26-t31-01 V, foundation-p03, p06, p09, advanced-p12, p13, p17 (practised) | — |
| T4 Similar triangles inside triangles/squares (hourglass, altitude to the hypotenuse) | 2: 2019w q1_19, 2026s q1_16 | t36 geo-139 (clear) | g146 V, g145 V, q-r26-t36-12 w, core-p09 w (practised) | Taught in t36 (day 36–40) |
| T5 Structural facts: altitudes of an obtuse triangle (2 outside), what two medians cut a triangle into, angle ratio, exterior angle bigger than either remote angle, a point at equal distances from A and B | 5: 2022a q2_06, 2020s q2_09, 2019w q1_05, 2024s q2_14, 2024w q1_20 | geo-009 says only "for some sides" the altitude falls outside. Two medians, the exterior-angle inequality and the perpendicular-bisector locus are not taught (mentioned) | foundation-p16 w, advanced-p09 w, advanced-p11 w; t30 foundation-p17 (ratio) (thin) | 5 items, each needs one fact we never state |

## Quadrilaterals (43)

| type | exam count + ids | explained where (rating) | practised where (rating) | flag |
|---|---|---|---|---|
| Q1 Triangle or parallelogram inside a rectangle/parallelogram: "apex on the opposite side = half", area bookkeeping | 6: 2020a q1_08, 2022a q1_02, 2022w q1_05, 2020w q1_05, 2023w q1_07, 2023s q1_06 | geo-067-after (clear) | g067 V, g068 V, g059 V, advanced-p02, p08, p16 (practised) | — |
| Q2 Trapezoid: triangles on the diagonals, same height so area ratio = base ratio | 5: 2025a q1_13, 2026s q1_08, 2021s q2_05, 2020s q1_06, 2020a q2_02 | geo-067-after, r26-t32-summary-2, t31 summary-2, t36 summary (clear) | g069 V, q-r26-t36-02 V, advanced-p17 w, q-r26-t36-10 w (practised) | — |
| Q3 Square/rhombus: diagonal ↔ side ↔ area; greatest distance = diagonal | 6: 2026s q2_09, 2019w q2_13, 2022a q2_08, 2020s q2_12, 2024s q2_01, 2022w q2_14 | geo-043, geo-050, t38 geo-175 (clear) | g044 V, g051 V, g060 V, foundation-p07, q-r26-t38-12 (practised) | — |
| Q4 Right triangles hidden in quadrilaterals (Pythagoras, special angles, heights) | 11: 2025s q1_01, 2021s q1_01, 2020w q2_17, 2024w q1_02, 2025a q2_05, 2025w q1_05, 2024w q2_01, 2023a q1_06, 2021a q1_01, 2024s q2_15, 2020w q2_02 | geo-047 (special angles), geo-054 (drop the heights), geo-056 (clear) | g046, g049, g053, g055, g062, g063 V, q-r26-t32-01/02 V, foundation-p16, p19, p23, q-r26-t32-08, -09 (practised) | — |
| Q5 Perimeter of composite figures (shared sides, staircase, frame, notch) | 6: 2024a q1_20, 2023w q1_14, 2023a q1_13, 2023s q2_13, 2022w q2_08, 2025w q2_02 | r26-t32-perimeter (clear) | q-r26-t32-06 V, g072 V, advanced-p10, p14, p15, p19, foundation-p01, p18 (practised) | — |
| Q6 Properties and the family tree: "not necessarily true" | 3: 2021s q1_06, 2026s q2_16, 2025s q1_15 | geo-042-2, geo-045, geo-047 (clear) | g066 V, t38 g183 V, foundation-p14, p20, advanced-p11 (practised) | — |
| Q7 Angle sums in quadrilaterals and trapezoids | 2: 2019s q2_03, 2022w q2_06 | geo-042, geo-054 (clear) | g057 V, g071 V, foundation-p02, p03 (practised) | — |
| Q8 Whole pieces: border tiles, whole stickers in a triangle, integer sides | 3: 2026s q2_11, 2023a q2_17, 2023s q1_18 | **Missing** in geometry. The only analogue is the painted cube in 3D (r26-t35-cubefacts) | none | Grouped with G1 in the gaps list |
| Q9 A line parallel to the base cuts a trapezoid off a triangle | 1: 2019s q2_02 | t36 geo-139 (clear) | g140 V, g148 V (practised) | Taught late (t36), but our course keeps the item there |

## Circles (37)

| type | exam count + ids | explained where (rating) | practised where (rating) | flag |
|---|---|---|---|---|
| C1 Central/inscribed angles, angle on a diameter, isosceles triangles from radii, tangent ⟂ radius | 8: 2022a q2_02, 2023a q1_05, 2019s q1_01, 2019w q1_01, 2022a q1_07, 2025w q1_17, 2026s q2_13, 2023s q2_01 | geo-074, geo-075, geo-077, geo-084 (clear) | g076 V, g078 V, g085, g086, g087, g088 V, foundation-p03…p08, p11, p13, p14 (practised) | — |
| C2 Sectors and arcs as fractions of the circle | 5: 2023a q2_08, 2024a q2_04, 2024s q2_06, 2025s q1_17, 2026s q1_05 | geo-081 (clear) | g082 V, g083 V, g091 V, foundation-p19…p21, advanced-p01, p09, p18 (practised) | — |
| C3 Area ↔ circumference, ratios, scaling; "both a whole number" | 4: 2020s q2_13, 2020a q2_14, 2022w q2_11, 2025a q2_19 | geo-079, t36 geo-135 (clear). That π times a fraction is never a whole number (2025a q2_19) is not taught; we only say pi "isn't a round number" | g080 V, g089 V, q-r26-t33-03 V, foundation-p01, p10, p12 (practised); none for the integer idea | 1 item only |
| C4 Wheels and motion on a circle (turns × circumference; diameter vs arc at equal times; distance → central angle) | 4: 2024s q1_13, 2022w q1_18, 2020w q1_08, 2023w q1_08 | geo-079 wheel part (clear for wheels). The motion combinations are not shown | advanced-p22 w only, plus wp27-p10 w (thin) | 4 items, no video |
| C5 Shaded regions: shape minus sectors, segments, semicircles | 5: 2020a q1_14, 2021a q2_08, 2021s q1_16, 2025s q2_07, 2024w q1_06 | geo-093, r26-t33-more-tools, r26-t33-summary-2 (clear) | g094 V, g099 V, q-r26-t33-04 V, g164 V, advanced-p10, p27 (practised) | — |
| C6 Equilateral triangle with incircle and circumcircle (R = 2r); circles in a 60° corner | 2: 2019w q2_08, 2019s q2_20 | **Missing.** geo-097-after gives only the triangle-circle-triangle area ratio. t31 geo-009 even says the medians' "two to one" rule "isn't needed for the exam" | none | Contradiction with what the exam needs |
| C7 Polygons and quadrilaterals inscribed in a circle | 5: 2024a q1_13, 2020s q1_13, 2024s q1_19, 2020w q2_18, 2024w q2_13 | geo-075 (inscribed quadrilateral, rectangle diagonal = diameter), t34 geo-104-2 (clear). **"A trapezoid in a circle is isosceles" is missing** (it appears only inside foundation-p16) (mentioned) | foundation-p15, p16 w, t34 g111 V, core-p12 w (practised); none for the trapezoid | 2024s q1_19 needs t34 polygon angles, which come about 17 days after t33 |
| C8 Tangent circles; circle + rectangle with similar triangles | 2: 2025a q1_19, 2020s q1_03 | summary ("join the centres"), t36 geo-139 (clear) | g101 V, g088 V, q-r26-t33-05 V, t36 core-p18 (practised) | — |
| C9 Circle facts on the plane; number of intersection points | 2: 2023s q1_15, 2019w q1_18 | geo-157 (clear for radii). Counting how many points a circle and a square can share is only touched by g167 (line and axis) (mentioned) | g167 V, t38 core-p15 w (thin) | — |

## Polygons (11)

| type | exam count + ids | explained where (rating) | practised where (rating) | flag |
|---|---|---|---|---|
| P1 Angle sum (n−2)·180; difference of two sums | 2: 2025a q2_06, 2025w q1_03 | geo-104, geo-104-3 (clear) | g116 V, g117 V, q-r26-t34-01 V, core-p03, p14, p18 (practised) | — |
| P2 Angles in regular polygons with diagonals; polygons meeting at a vertex | 5: 2023s q2_03, 2026s q2_19, 2020w q2_04, 2020s q1_17, 2024w q1_18 | geo-104-4 (equal split at one vertex), geo-109 (corner triangle), r26-t34-meet (clear). The general "each side under the angle is worth 180/n" rule is missing (external-course-C rec. 1) | g110 V, q-r26-t34-03 V, core-p06, p09, q-r26-t34-09 (practised) | Angles between diagonals from different vertices are slow without the 180/n rule |
| P3 Regular hexagon: short diagonal a√3, long diagonal 2a, the corner triangle | 2: 2023a q2_02, 2023w q2_05 | geo-109 (clear) | g112 V, core-p01, p02, p07 (practised) | — |
| P4 Regular hexagon: width between opposite sides, radius of the inscribed circle (a√3/2) | 2: 2025s q1_18, 2025w q2_15 | geo-104-2 only says a circle "touching every side" exists and that "we mostly use the circle around it" (mentioned) | none (core-p19 is a different circle) | — |

## 3D geometry (32)

| type | exam count + ids | explained where (rating) | practised where (rating) | flag |
|---|---|---|---|---|
| D1 Formulas: volume, lateral and total surface of box, cylinder, cone, pyramid, prism | 12: 2019s q2_05, 2023s q2_11, 2024a q1_04, 2022w q1_14, 2022a q2_11, 2024w q2_19, 2021s q2_12, 2025w q1_19 | geo-119, r26-t35-water (clear) | g121, g122, g127 V, q-r26-t35-01/02 V, core-p01…p04, q-r26-t35-05 (practised) | — |
| D2 How a change in r, h or the edge changes the volume (and surface) | 7: 2020a q2_08, 2020w q2_07, 2024s q2_19, 2025s q2_14, 2026s q1_20, 2021a q1_18, 2023a q1_09 | t36 geo-141, geo-143 (clear). The reverse direction (volume ×2 → edge ×∛2 → surface ×∛2²) is not shown | g142 V, g150 V, g151 V, q-r26-t36-03 V, t36 core-p12, p16 (practised); none for the reverse | 1 item (2026s q1_20) |
| D3 Lengths and angles inside solids (face/body diagonal, right triangles, cube angles, cylinder chord) | 7: 2020a q1_07, 2022a q1_20, 2025a q2_14, 2022w q2_20, 2024a q2_15, 2023w q2_11 | r26-t35-cubefacts, r26-t35-summary, t38 geo-175 (clear) | g128, g129, g130 V, q-r26-t35-02 V, core-p09, p25, q-r26-t38-13 (practised) | — |
| D4 Composite and cut solids: surface and volume of the pieces | 4: 2019s q1_14, 2019w q2_20, 2023a q2_19, 2021a q2_10 | r26-t35-summary (corner cube), t38 g186 ("a cut adds two faces") (clear) | g125 V, g132 V, g123 V, core-p05, p10, p14 (practised) | — |
| D5 Counting faces, edges, vertices; sum of the edges | 2: 2020s q1_19, 2020w q1_13 | r26-t35-cubefacts (clear) | core-p07 w only (thin) | — |

## Similarity (4)

| type | exam count + ids | explained where (rating) | practised where (rating) | flag |
|---|---|---|---|---|
| S1 Spot similar triangles; match sides by angles | 2: 2023s q2_14, 2022w q1_01 | geo-139, small–big table (clear) | g144 V, g145 V, core-p01, core-p26 (practised) | — |
| S2 Parallel cut / area ratio = (linear ratio)² | 2: 2023w q2_12, 2024w q1_03 | geo-134, geo-139 (clear) | g140 V, g148 V, core-p11 (practised) | — |

## Coordinate system (17)

| type | exam count + ids | explained where (rating) | practised where (rating) | flag |
|---|---|---|---|---|
| K1 Area of a polygon on the grid / plane (box method) | 3: 2020a q1_05, 2019w q2_03, 2025w q2_06 | r26-t37-box (clear) | q-r26-t37-10 V, g162 V, q-r26-t37-12 w (practised) | — |
| K2 Segment lengths, comparing them, farthest point, equilateral height | 4: 2019s q2_18, 2023a q2_05, 2024w q2_03, 2022w q1_16 | geo-155 (clear) | g156 V, q-r26-t37-07 V, core-p05, p14, p19 (practised) | — |
| K3 Points dividing a segment, midpoint, line through the origin | 2: 2021a q1_14, 2020s q2_03 | geo-159 (equal steps) (clear) | q-r26-t37-05 V, g160 V, g166 V, core-p02, p13, p20 (practised) | — |
| K4 Circles on the plane | 4: 2024a q1_01, 2026s q1_13, 2020w q1_20, 2023w q1_18 | geo-157 (clear) | g158 V, g164 V, core-p04, p09, p10, p17, p23 (practised) | — |
| K5 Coordinates from congruence or rectangle conditions | 2: 2024s q1_01, 2025s q2_19 | geo-154, geo-155 (clear) | core-p06 w, core-p15 w (thin) | — |
| K6 The line y = x: the region y < x, the swap (x, y) → (y, x) | 2: 2021s q1_12, 2025a q1_07 | **Missing.** geo-154 teaches reflections only across the axes and through the origin | none | — |

## Geometric comprehension (9)

| type | exam count + ids | explained where (rating) | practised where (rating) | flag |
|---|---|---|---|---|
| G1 Visual/spatial counting and fitting: count the quadrilaterals in a figure, cover a trapezoid with whole 1×10 strips, roll a box, walk a square's perimeter step by step | 4: 2021a q2_12, 2021a q2_13, 2025w q2_12, 2019s q1_07 | **Missing** (no lesson in t38 or t51) | none | With Q8, 7 exam items have no coverage at all |
| G2 Grid areas and composite perimeters | 2: 2024a q2_09, 2019s q1_05 | g070 (completions), r26-t32-perimeter (clear) | g070 V, foundation-p09, p10, q-r26-t32-06 V (practised) | — |
| G3 Which data fixes the answer ("area alone gives the perimeter of …") | 1: 2025a q1_02 | r26-t38-summary, geo-042-2 (clear) | foundation-p20 w, t38 core-p19 w, g183 V (practised) | — |
| G4 Extreme position (farthest point, largest radius) | 1: 2023s q1_19 | geo-175 (clear) | q-r26-t38-12 w, core-p25 w, g182 V (practised) | — |
| G5 Symmetric points on a circle centred at the origin | 1: 2022a q2_13 | geo-154 (reflection through the origin) (clear) | q-r26-t37-03 w (thin) | — |

---

## Gaps and weak spots, ranked (exam count × weakness)

1. **Spatial and "whole pieces" reasoning: 7 items, missing, no practice.** G1 + Q8: 2021a q2_12, 2021a q2_13, 2025w q2_12, 2019s q1_07, 2026s q2_11, 2023a q2_17, 2023s q1_18.
   - Sanity check: 2026s q2_11 (5×9 room, grey border tiles). The white tiles are the inner 3×7 = 21. Our only border-counting idea is the painted cube in 3D. Nothing in t32/t38 teaches the 2D version. Counting simple quadrilaterals (2021a q2_12) needs a system: by number of regions, or by which vertices are used. We never teach one.
   - Where: a new t38 lesson, "Counting and fitting pieces", after geo-177, with prerequisites t32 and t35 cubefacts. Teach four moves, each with a worked example:
     - count systematically (by size or by the regions used);
     - border vs inside: the inside is (L−2)(W−2), the 2D twin of the painted cube;
     - an area bound plus a fitting check, for covering with whole pieces and fitting whole stickers;
     - track one marked corner while you roll or walk, one step at a time.
   - Practice: 4–5 questions, 2 with videos.
   - Status: t38 is recorded, so this means new videos.
2. **Equilateral triangle: R = 2r, and the centre splits each altitude 2:1. 2 items, missing, and the course contradicts it.** C6: 2019w q2_08, 2019s q2_20.
   - Sanity check: 2019w q2_08. Join O to a vertex and to the midpoint of a side. The angle at the vertex is 30° and r is the short leg, so R = 2r = 2, and the ring is π(4 − 1) = 3π. Our course never shows this gold triangle. t31 geo-009 tells students the 2:1 median rule "isn't needed for the exam".
   - Where: t33 geo-097-after, "Three Nested Shapes", which still has to be recorded. Add a fourth picture: one equilateral triangle with both of its circles, R = 2r, and the ring = 3πr², shown through the 30-60-90 triangle. Also change the "isn't needed" sentence in t31 geo-009 to "you'll see it again with circles". geo-009 is recorded, so this is a re-record or a cut, so check with the teacher. Practice: 2 questions (one ring, one circle tangent to two sides at 60°), 1 with a video.
3. **The line y = x on the plane: 2 items, missing.** K6: 2021s q1_12, 2025a q1_07.
   - Sanity check: 2025a q1_07. Swapping x and y mirrors a shape across the line y = x. Our reflections lesson covers only the axes and the origin, so a student has no way to pick the image.
   - Where: t37, after geo-159 (Slope), which introduces lines through the origin. Teach the line y = x, the points below it (y < x), and the swap as a mirror across it.
   - Practice: 2 questions with videos (a region one and a swap one). t37 is recorded, so this means a new short lesson or two solution videos.
4. **Regular polygons: the "count the sides" angle rule, plus the hexagon's width and inscribed radius. 7 items (P2 5, P4 2), half-explained or mentioned.**
   - Sanity check: 2025w q2_15. A hexagon around a circle of radius r: r is the height of one central equilateral triangle, a√3/2, so the side is 2r/√3. We teach the equilateral height and the hexagon's six triangles, but we never link the circle inside the hexagon to that height.
   - Where: t34 geo-104-4 and geo-109, both still to be recorded.
     - In geo-104-4: each side under an angle with its vertex on the polygon is worth 180/n (external-course-C rec. 1).
     - In geo-109: the short diagonal ⟂ the next side, the width between opposite sides = a√3, and the inscribed radius = a√3/2.
   - Practice: 2 new questions (hexagon in a rectangle, hexagon around a circle), 1 with a video.
5. **Wheels and motion on a circle: 4 items, explained, thin practice (1 written).** C4: 2024s q1_13, 2022w q1_18, 2020w q1_08, 2023w q1_08.
   - Where: t33 geo-079 wheel part, still to be recorded. Add one sentence: "the same time, so the speed ratio is the distance ratio (arc πr vs diameter 2r = π:2)".
   - Practice: add 2–3 questions: a wheel's speed, diameter vs arc, and a distance turned into a central angle. Give one of them a video.
6. **Triangle structure facts: 5 items, mentioned, thin practice.** T5: 2022a q2_06, 2020s q2_09, 2024s q2_14, 2024w q1_20, 2019w q1_05.
   - What's missing:
     - "an obtuse triangle has exactly two altitudes outside";
     - two medians cut a triangle into 3 triangles + 1 quadrilateral (sketch it);
     - an exterior angle is bigger than either remote angle (it is their sum);
     - the points at equal distances from A and B lie on the perpendicular bisector.
   - Where: t31 r26-t31-summary-2 (recorded), so make it a practice set: 4 "necessarily true" questions, 1–2 with videos.
7. **A trapezoid in a circle is isosceles: 1 item, mentioned only.** 2024a q1_13. Today it appears only inside foundation-p16. geo-075 is recorded, so put the sentence and its reason in r26-t33-more-tools, which is still to be recorded. Add a solution video in the 2024a q1_13 style (external-course-C rec. 2).
8. **Which side do two non-parallel lines meet on: 1 item, missing.** 2021s q2_20. t30 is recorded. Add a solution-video question: if the two U angles add up to less than 180, the lines meet on that side. Add one written question too.
9. **Thin practice where the teaching is fine:**
   - D5 counting faces, edges and vertices, and the edge sum 4(a+b+c): 2 items, core-p07 only.
   - K5 coordinates from conditions: 2 items, written only.
   - C9 intersection-count questions: 2 items.
   - Add 1 video question to each.
10. **Small conceptual one-offs:**
    - 2025a q2_19: a circle's circumference and area can't both be whole numbers, because one of them always carries π.
    - 2026s q1_20: the reverse of volume scaling (volume ×2 → edge ×∛2 → surface ×∛2²). Add this as a reverse example in t36 geo-143 (recorded) through a practice question.

Order notes (planData ORDER):
- t33 (day 5) comes well before t34 (day 22+) and t36 (day 36+). Circle-exam ideas that need polygon angles (2024s q1_19) or similarity (2025a q1_19) are correctly kept out of t33's practice, so no fix is needed.
- The 40°/140° equal-area idea (2025w q1_13, a triangle item) is taught only in t38 (day 43). A one-line mention in t31 would help, but t31 is recorded.

Counts: 49 types. Explained: 40 clear, 5 mentioned, 4 missing. Practice: 37 practised, 7 thin, 5 none.
