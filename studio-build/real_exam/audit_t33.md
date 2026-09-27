# Audit T33 – Circles (report only, nothing edited)

Sources: `math_patches/t33_CHANGES.md`, `math_patches/t33.py`, `real_exam/quant_real.md` (regenerated), real exam figures
(all 37 circles questions + circle items in coordinate_system/polygons viewed), pre-patch course `course18.json`.

Policy: same as audit_t30.md. A rule the ORIGINAL course questions need is kept (coordinator rule 2). A new question whose
type is not on the real exam but is already tested by original course questions is UNSURE; not on the real exam and not in
the original course is REMOVE.

Key real-exam facts from the figures: tangent circles (2020_autumn_q2_14 internal, 2020_spring_q1_03 and 2019_spring_q2_20
external); equal tangent pieces (2026_spring_q2_13); segment = sector − triangle (2021_spring_q1_16, 2025_spring_q2_07);
ring whose chord touches the inner circle (2019_winter_q2_08: equilateral triangle between incircle and circumcircle,
ring = 3π); wheels (2024_spring_q1_13, 2022_winter_q1_18). No quadrilateral circumscribed about a circle, no "two circles
meet at two points" distance range, no percent change of radius/area, no incircle of a right triangle.

| Addition | Where (video id / slide / question ids) | Class | Verdict | Evidence (real question ids / count) |
|---|---|---|---|---|
| Q1 method 3 shown step by step; inscribed-quadrilateral proof note (2α on the side of C); Q16 method 3 corrected; Q20 estimate reason; adv-p06 "2p+3q/2"; p16 kite wording; Q2 "Pavlov" removed; Q22 closing line; Q9 golden-triangle reminder box; nested triangles picture | solve-geo33-g076 (Q1), geo-075 slide 6, solve-geo33-g096, solve-geo33-g100, geo33-advanced-p06, geo33-foundation-p16, solve-geo33-g078, solve-geo33-g102, solve-geo33-g088, geo-097-after | FIX | KEEP | – |
| Equal chords slide: SSS proof removed, figure added | geo-075 slide "Equal chords" | FIX | KEEP (see restore section) | – |
| All 76 solutions in TeX, spacing, stacked givens, US spelling, Q18/Q12 wording | all geo33-* | FIX | KEEP | – |
| Figures fixed (Q6 g085, p05, p15, Q15 g095, Q12 g091, Q18 g098, p20, Q5 g083, p03, adv-p06, p11, adv-p15, label overlaps, lesson figures) | as listed in t33_CHANGES §4 | FIX | KEEP (see restore section) | – |
| Chord and center: perpendicular from the center halves the chord, d² + (chord/2)² = r² | geo-075 new slide "Chord and center"; card mem-circle-rules row "Chord and center" + tip | METHOD | KEEP | Needed by original geo33-foundation-p22, geo33-advanced-p21 (rule 2). Real: 2020_autumn_q1_14 (distance from O to side AD of the inscribed square, 1 real, used implicitly) |
| Circle inside a triangle: equal tangent pieces; right triangle r = (a+b−c)/2 | geo-077 new slide "Circle inside a triangle"; card row "Circle inside a triangle" | METHOD | KEEP | Equal tangent pieces: 2026_spring_q2_13. Needed by original geo33-advanced-p26 (rule 2) |
| Quadrilateral around a circle: AB + CD = BC + AD | same slide; card mem-circle-rules row "Quadrilateral around a circle" | CONTENT | REMOVE | 0 real; no original question (adv-p15 is a chain of tangent circles, solved from R + r) |
| Tangent circles: distance between centers R + r / R − r | geo-077 new slide "Tangent circles"; card row "Tangent circles" | METHOD | KEEP | 2020_autumn_q2_14 (internal), 2020_spring_q1_03, 2019_spring_q2_20 (external); original adv-p15, foundation-p18 |
| Scaling: radius ×k → C ×k, S ×k² | geo-079 new slide "Scale the radius"; card mem-circle-formulas row "Scaling" | METHOD | KEEP | 2020_autumn_q2_14 (circumference is linear in the diameter); original geo33-foundation-p24 (rule 2) |
| Wheel turns = distance ÷ circumference, units | geo-079 new slide "Wheels"; card row "Wheel turns" | METHOD | KEEP | 2024_spring_q1_13, 2022_winter_q1_18, 2023_winter_q1_08 (arc on a circular course); original adv-p22 |
| Right triangle in a circle: hypotenuse = diameter; rectangle's diagonal = diameter | geo-075 slide 4 (new line + board item); card row "Right angle on the circle" | METHOD | KEEP | 2024_winter_q2_13 (AB²+BD²+AC²+CD² = 8r²), 2019_winter_q1_01, 2019_spring_q1_01 |
| Hexagon tip: side = radius | card mem-circle-formulas tip | METHOD | KEEP | 2024_spring_q1_19, 2024_autumn_q1_13, 2025_winter_q2_15 |
| More Circle Tools: segment = sector − triangle | new video r26-t33-more-tools slide "Segment = sector − triangle"; card mem-r26-t33-more-tools row "Segment" | METHOD | KEEP | 2021_spring_q1_16, 2025_spring_q2_07, 2020_autumn_q1_14 |
| More Circle Tools: two equal circles through each other's centers (lens) | r26-t33-more-tools slide "Two equal circles"; card row | METHOD | KEEP (rule 2) | 0 real; needed by original geo33-advanced-p27 (radius 4, distance 4) |
| More Circle Tools: common external tangent (right trapezoid, DC = 2√(Rr)) | r26-t33-more-tools slide "Common tangent"; card row + tip | METHOD | KEEP (rule 2) | Needed by original geo33-advanced-p20. Real only the equal-radius case: 2024_winter_q1_06 |
| More Circle Tools: chord of a ring (ring = π h²) | r26-t33-more-tools slide "Chord of a ring"; card row | METHOD | KEEP | 2019_winter_q2_08 (ring whose chord, the triangle side, touches the inner circle); original adv-p21 |
| Guided Q2: chord 16, distance 6 → circumference 20π | q-r26-t33-01 + video solve-q-r26-t33-01 | CONTENT (type) | KEEP | 2020_autumn_q1_14 (1 real, thin) |
| Guided Q4: incircle of a right triangle 8-15-17 → r = 3 | q-r26-t33-02 + video solve-q-r26-t33-02 | CONTENT (type) | UNSURE | 0 real (only the equilateral incircle 2019_winter_q2_08, solved differently); original type adv-p26 |
| Guided Q6: circumference +50% → area +125% | q-r26-t33-03 + video solve-q-r26-t33-03 | CONTENT (type) | UNSURE | 0 real percent-change question; original type foundation-p24 |
| Guided Q26: segment, radius 6, 60° | q-r26-t33-04 + video solve-q-r26-t33-04 | CONTENT (type) | KEEP | 2021_spring_q1_16, 2025_spring_q2_07 |
| Guided Q27: common tangent of touching circles, radii 8 and 2 → 8 | q-r26-t33-05 + video solve-q-r26-t33-05 | CONTENT (type) | UNSURE | Real only the equal-radius case (2024_winter_q1_06); original type adv-p20 |
| Practice -06: area ×9 → circumference ×3 | q-r26-t33-06 (foundation) | CONTENT (type) | KEEP | 2020_autumn_q2_14, 2020_spring_q2_13 (area ↔ circumference) |
| Practice -07: internally touching circles 9 and 4 → AB = 5 | q-r26-t33-07 (foundation) | CONTENT (type) | KEEP | 2020_autumn_q2_14 (internal tangency) |
| Practice -08: quadrilateral around a circle, AD = 10 | q-r26-t33-08 (advanced) | CONTENT (type) | REMOVE | 0 real; not original |
| Practice -09: BD in triangle 10-12-8 with its inscribed circle | q-r26-t33-09 (advanced) | CONTENT (type) | UNSURE | Equal tangent pieces appear (2026_spring_q2_13) but no real incircle-of-a-triangle length question; original type adv-p26 |
| Practice -10: ring from a 16 cm chord → 64π | q-r26-t33-10 (advanced) | CONTENT (type) | KEEP | 2019_winter_q2_08 |
| Practice -11: two parallel chords 6 and 8, radius 5 → 7 | q-r26-t33-11 (advanced) | CONTENT (type) | KEEP | 2020_autumn_q1_14 (chord–center, 1 real, thin) |
| Practice -12: "which statement is true", chord 8 in radius 5 | q-r26-t33-12 (advanced) | CONTENT (type) | KEEP | 2020_autumn_q1_14 (chord–center, 1 real, thin) |
| Practice -13: circles 3 and 5 meet at two points – which cannot be the distance | q-r26-t33-13 (advanced) | CONTENT (type) | REMOVE | 0 real; not original |
| Practice -14: radius −10% → area −19% | q-r26-t33-14 (advanced) | CONTENT (type) | UNSURE | 0 real; original type foundation-p24 |

Counts: KEEP 22 (of which 4 FIX), REMOVE 3, UNSURE 5.

## TO REMOVE
- Video geo-077 (Tangents), slide "Circle inside a triangle": the last board item "Quadrilateral around a circle: AB+CD=BC+AD" and its spoken line "The same idea works for a quadrilateral around a circle…". Keep the triangle part.
- Card mem-circle-rules: row "Quadrilateral around a circle" (AB + CD = BC + AD).
- Questions: q-r26-t33-08 (quadrilateral around a circle), q-r26-t33-13 (which cannot be the distance between the centers).

If the teacher removes the UNSURE group ("extra questions of an original type that is not on the real exam"): q-r26-t33-02
(+ solve-q-r26-t33-02, guided Q4), q-r26-t33-03 (+ solve-q-r26-t33-03, guided Q6), q-r26-t33-05 (+ solve-q-r26-t33-05,
guided Q27), q-r26-t33-09, q-r26-t33-14.

## ORIGINAL ITEMS REMOVED BY FIXERS (to restore)
- geo33-foundation-p09 (unplaced): circles K and M intersect at A, B; MA and KB tangents; angle AMB = 72° → angle AKB.
- geo33-foundation-p13 (unplaced): isosceles ABC (AB = AC, angle BCA = 56°), circle tangent to AB, AC at D, E → angle DOE. (Real tangent-angle type exists: 2026_spring_q2_13.)
- geo33-foundation-p25 (unplaced): concentric circles r = 2, 3 → ring : small disk. (Real ring type exists: 2019_winter_q2_08.)
- geo33-advanced-p08 (unplaced): circular garden r = 600 m, path 100 m wide → area in km².
- geo-075 slide "Equal chords": the original SSS congruence proof was removed (only the rule and the figure remain).
- solve-geo33-g096 (Q16) method 3: original "write 1+ on each of the three arcs" draw line and "Same for the other two arcs…" line removed; spoken line replaced.
- solve-geo33-g100 (Q20): original estimate reason and board item "BC < 6" replaced.
- solve-geo33-g078 (Q2): the "Pavlov" line replaced; slide title changed to "Automatic: draw the radii".
- solve-geo33-g102 (Q22): closing line "That's it for circles. On to the summary." replaced.
- geo-077 and geo-079: spoken lines "Let's solve a sample question." / "Let's see a psychometric question." deleted.
- Figures: center O removed from foundation-p05 and -p15; the 144° label removed from foundation-p11 (now only in the stem); radius OD no longer drawn in Q15 (g095); the 12 angle arcs removed from Q12 (g091); α/γ replaced by "?" in p03 and adv-p06; B moved in Q18 (g098); stray "A" removed from the circle slide.
- geo-097-after (nested shapes, triangle case): the original claim replaced by an upside-down inner-triangle picture.
