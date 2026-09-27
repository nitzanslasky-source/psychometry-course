# Topic 33 – Circles: changes (course review 2026-09)

`python3 math_check.py 33`: 0 problems, 0 warnings, 0 layout problems.

## 1. Wrong or unclear statements
- **Q1 (angle on the major arc), Method 3** was too short ("112 is 360 minus twice the angle"). It is now shown step by step on the board: base angles x and y, then (180° − 2x) + (180° − 2y) = 112°, so x + y = 124°.
- **Inscribed quadrilateral proof:** the note said "write 2α on the side facing A". The central angle 2α is on the side of C (it rests on arc BCD). Fixed.
- **Equal chords** slide: removed the SSS congruence proof (SSS is not taught in T31) and added a figure. It keeps only the rule and "join the ends to O".
- **Q16, Method 3:** "write 1+ on each of the three arcs" was only true for three 60° pieces. It now says: the curved part is half a circle, π·1, a bit more than 3.
- **Q20 estimate:** new reason. The circle fits in a 6 by 6 square, so 6·BC < 36 and BC < 6.
- **adv-p06:** the solution read "2p+3q:2". It now reads $2p+\frac{3q}{2}$.
- **p16:** "A kite with opposite angles of 90° and 72°" is now "A kite whose two unequal opposite angles are 90° and 72°".
- **Q2:** removed "Pavlov". It now says "Always, automatically — every time", and the slide title is "Automatic: draw the radii".
- **Q22:** the last line said "That's it for circles. On to the summary". A new lesson now comes after it, so the line was changed.

## 2. Methods that were used but never taught (now taught)
| Method | Where it is taught | Guided question (new, with solution video) | Practice |
|---|---|---|---|
| The perpendicular from the center cuts a chord in half: $d^2+(\frac{chord}{2})^2=r^2$ | new slide "Chord and center" (Angles in a Circle) | Q2: chord 16, distance 6 → circumference 20π | p22, adv-p21, new: parallel chords, "which statement is true" |
| Equal tangent pieces in a circle inside a triangle; right triangle $r=\frac{a+b-c}{2}$; quadrilateral around a circle $AB+CD=BC+AD$ | new slide "Circle inside a triangle" (Tangents) | Q4: legs 8 and 15 → r = 3 | adv-p26 (now has a figure), adv-p15, new: quadrilateral around a circle, new: BD in triangle 10-12-8 |
| Distance between the centers of touching circles: R + r and R − r | new slide "Tangent circles" (Tangents) | covered in the Q4 group videos and Q13 | new: internally touching circles (9 and 4 → 5), new: "which cannot be the distance" |
| Scaling: radius ×k → C ×k, S ×k² (T36 was needed early) | new slide "Scale the radius" (Area and Circumference) | Q6: circumference +50% → area +125% | p24, new: area ×9 → C ×3, new: radius −10% → area −19% |
| Wheel turns = distance ÷ circumference, with units | new slide "Wheels" | – | adv-p22 |
| Right triangle in a circle: hypotenuse = diameter; a rectangle's diagonal = diameter | extra line and board item on "Angle on a diameter" | (Q14 already uses it) | adv-p25 |
| Segment = sector − triangle; two equal circles through each other's centers (equilateral triangles, 120°, lens = 2 segments); common external tangent (right trapezoid, $DC=2\sqrt{Rr}$ for touching circles); chord of a ring (ring = πh²) | **new lesson video "More Circle Tools"** (end of "Further guided examples") | Q26: segment (radius 6, 60°); Q27: common tangent (radii 8 and 2 → 8) | adv-p23, adv-p27, adv-p20, adv-p21, new: ring from a 16 cm chord (64π) |

Guided questions are renumbered automatically. There are now 27 (22 + 5). The new ones are Q2, Q4, Q6, Q26 and Q27.

## 3. Text (every question and video)
- All 76 existing solutions were rewritten in TeX, with the numbers shown and fractions instead of ":". This covers "3π:2", "πr(1−α:90)", "144:360=2:5" and the others.
- Missing spaces were fixed ("radii,8", "totaling(π+2)r" and the others).
- Givens are now stacked with `cases` in the stems of Q11 (was Q8), Q47 (was Q18), Q51 (was Q22), p23 and adv-p15, and in 2 new questions.
- Q18 now says where B and C are: "B and C lie on the arc AD that does not contain F".
- Q12 no longer says "α-sector". It says "one sector with angle α".
- Board items with ":" as division now use fractions: Q1, Q2, Q7, "On a diameter", "25π÷5".
- The colons inside the math on Q21 and Q22 were moved out of the math.
- The on-screen question copies ("non−overlapping") were refreshed from the stems.
- British spellings in the videos were changed to American (centre/CENTRE, centimetres, practise, Recognise).
- Q9: a "golden triangle" reminder box was added: 30°-60°-90° has sides x, x√3, 2x. The silver triangle box was already on Q8.
- Nested shapes, triangle case: the unproved claim was replaced by the picture. The inner triangle is turned upside down, and the outer triangle is 4 copies of it.

## 4. Figures fixed
- **Q6 (g085 + solution slides):** the "12" that read as "O12" was replaced by a dimension line under AB.
- **p05:** the center O is removed. The stem never mentions it, and it showed that AC is a diameter. The "8" was moved away from the center.
- **p15:** the center O is removed. It gave away that AC is a diameter.
- **Q15 (g095):** radius OD is no longer drawn in the question. The shaded region is now D–C–E–arc, with no edge OD.
- **Q12 (g091):** the 12 angle arcs that formed an unexplained inner circle are removed.
- **Q18 (g098):** B was moved (200° instead of 225°), so chord BF no longer looks like a diameter.
- **p20 and Q5 (g083):** the double "O" is removed.
- **p03, adv-p06:** the α and γ that the stems never mention are now "?". On p03 the "140°" was moved off chord CD.
- **p11:** the figure was redrawn. The "?" is at B. The 144° label was dropped because it could not fit inside the thin angle (the angle is given in the stem).
- **adv-p15:** redrawn so that only neighbors touch. B and D no longer touch, and neither do A and C.
- **Label overlaps fixed:** p19 (O), adv-p04 (a, 3c), adv-p11 (3t), Q24 (was Q21, the "C").
- **adv-p26:** new figure (right triangle 6-8 with its circle).
- **Lesson figures:**
  - The stray "A" on the circle slide is removed.
  - The inscribed quadrilateral is now clearly not a rectangle (A = 70°, C = 110°).
  - O is now drawn on the proof slide.
  - The "Quarters and eighths" slide starts with quarters; the teacher draws the eighth.
  - The nested triangles are shown upside down.
- **New figures:** equal chords, chord and perpendicular, circle inside a triangle, tangent circles, segment, two equal circles, common tangent, chord of a ring, and figures for the new questions.

## 5. Practice
- **Removed (near-duplicates):**
  - p09 and p13: "tangents → quadrilateral 360°", which was used 5 times.
  - p25 and adv-p08: "ring = big − small", which was used 5 times.
- **Added (9 new):**
  - Foundation: area ×9 → C ×? ; internally touching circles.
  - Advanced: quadrilateral around a circle; BD in a triangle with its inscribed circle; ring from a tangent chord; two parallel chords; "which statement is true" (chord 8 in radius 5); "which cannot be the distance between the centers"; radius −10% → area −19%.
  - That adds 2 more "which statement" questions.
- **Size:** 54 practice questions became 59 (foundation 26, advanced 33). Both sections are ordered easy → hard.
- **Memory cards:**
  - Circle rules card: added right angle → diameter, chord and center, circle inside a triangle, quadrilateral around a circle, and tangent circles (R ± r).
  - Formulas card: added scaling and wheel turns, plus a hexagon tip (side = radius).
  - New card "Circles — more tools".

## For the teacher to decide
- p11 no longer shows "144°" in the figure. It did not fit inside the angle. The value is only in the stem.
- Stems with stacked givens (Q47, Q51) make the question text smaller on the solution slides. This follows the "givens one on top of the other" rule.
- "Distance between the centers" (R ± r) has a lesson slide and practice questions, but no guided question of its own. The existing guided Q12/Q16 (tangent circles) use it.

## Pass 2 (teacher-approved remove/restore plan, 2026-09-27)
`python3 math_check.py 26 27 33 34`: 0 problems, 0 warnings, 0 layout problems.

**Removed (4 items)**
- Tangents video, slide "Circle inside a triangle": the board item "Quadrilateral around a circle: AB + CD = BC + AD" and its spoken line. The triangle part stays.
- Circle rules card: the row "Quadrilateral around a circle".
- Practice q-r26-t33-08 (quadrilateral around a circle) and q-r26-t33-13 (two circles meeting at two points).

**Restored**
- Practice: geo33-foundation-p09, -p13, -p25 and geo33-advanced-p08 are back. Their solutions are now in TeX with the numbers shown. The p13 givens are stacked. On p09 and p13 the unused "α" in the figure is now "?", as on the other figures.
- "Equal chords" slide: the original proof is back ("Join each chord's ends to the center: two triangles, radius, radius, equal chord — identical triangles"). The new figure stays.
- Q3 solution (tangents): the "Pavlov" line is back.
- "Let's solve a sample question." / "Let's see a psychometric question." are still spoken at the end of the Tangents and the Area and Circumference lessons. A sample question still follows each one.
- Q22 closing line: not restored. It is no longer the last circles video, because "More Circle Tools" and the new summary come after it.
- Received from other topics: wp26-p10 (rough circular floor, answer $\frac{3\pi}{4}$ hours) and wp27-p10 (runners on a circular track, central angle 60°). Both are in the foundation practice. wp26-p10 comes after the circle-area items and wp27-p10 after the central-angle / arc-fraction items.
- Practice size: foundation 26 → 31 (3 restored, 2 moved in), advanced 33 → 32 (2 removed, 1 restored). Both sections are still ordered easy → hard.

**Summary lessons (new)**
- `r26-t33-summary` "Circles: Summary", at the end of "Learn and try", right before the foundation practice. Slides: Summary · Radii · Central and inscribed · Diameter, quad · Chords · Tangents · Circle in a triangle · Area and circumference · Sectors and arcs · Before you practice.
- `r26-t33-summary-2` "Advanced Circles: Summary", at the end of "Further guided examples", right before the advanced practice. Slides: Summary · Shaded areas · Segments · Nested shapes · Special triangles · Tangent and ring · The whole, not the parts · Numbers and estimates · Before you practice.
