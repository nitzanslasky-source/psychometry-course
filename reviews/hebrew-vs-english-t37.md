# Topic 37 (The coordinate system): the teacher's Hebrew videos vs the English course

Read-only review, 2026-10-22. Nothing in the course was changed.

- Hebrew source: `~/Downloads/03-Geometry-Original-Subtitles.txt`, lines 8588-9459 (all of it read).
- English: `scratchpad/ext/course/t37.txt` (every video's spoken text) and `q37.txt` (practice questions), the current flow in
  `~/Downloads/Psychometric-Teacher-Studio-v19-hybrid.html`, the base translation `studio-build/base-v18.html` (flow checked).
- **Recording status:** topic 37 has no reading scripts in `ai_scripts/` yet (only `r26-t37-summary.json`), so none of its
  videos are in the `video_status.py` tracker. **Nothing in topic 37 is recorded**; every target below is unrecorded.
- Note on her Hebrew coordinates: the subtitles are right-to-left, so a point she reads as "x = 3, y = 6" may appear as (6, 3)
  in the text. The table uses her spoken values.

**Match scale.** New numbers alone are not a change (memory rule *questions-differ-from-hebrew*).
SAME = same idea and every one of her methods. CHANGED = same idea, but the method, the example type or the order differs.
PARTIAL = some of her content or one of her methods is missing. MISSING = no English equivalent.

**Her names carry over:** ראשית הצירים → "the origin"; מדרגות → "stairs / steps"; קומות → "floors" ("climbed 3 floors"); חישוב חלקי →
"partial calculation"; הערכת סדר גודל → "estimating sizes"; משולש כסף / זהב → "silver / golden triangle"; שאלת קצה → "an edge question";
"לעבור נתון נתון" → "go given by given".

**Id numbering.** geo-154 (lesson 1), geo-155 (lesson 2) + g156, geo-157 (lesson 3, circle) + g158, geo-159 (lesson 4, slope) +
g160, geo-161 (the intro to the question lesson), g162-g169 (her 8 sample questions). Every one of her segments has an id in her
order; no gaps (geo-152/153 and geo-170/171 are not geometry ids).

---

## 1. Hebrew → English (her videos, in her order)

| # | Her video (Hebrew title · English gloss) | Lines | What she teaches / how she solves it (every method) | English equivalent | Match |
|---|---|---|---|---|---|
| 1 | ערכי נקודות במערכת צירים · Reading points | 8590-8648 | Two axes, origin (0,0); a point can be anywhere; notation A(x, y), x always first; drop perpendiculars to read A(5,3), B(−5,1), C(2,−3); "very basic, most of you know it" | geo-154 slides 1-7, 10 | SAME (A(6,2), B(−4,3), C(−2,−4)). English adds the four quadrants, reflections across the axes, and "a point on an axis has 0" |
| 2 | מציאת אורך קטע · Length of a segment | 8650-8744 | Parallel to y when the x's are equal; length by subtracting the y's (2 − (−1) = 3) or, when the points are on opposite sides, by eye: up to the axis + down from it; parallel to x: same side → subtract (4 − 1). A line that doesn't cut an axis is parallel to it; a line parallel to neither cuts each once. Slanted: lines parallel to the axes → right triangle → Pythagoras (3, 4, 5). "Forget the distance formula; it is Pythagoras anyway" | geo-155 (all slides) | SAME (8, 6, 8-15-17). English adds the classic mistake 7 − 2, "a segment can stop before the axis", and "if the answers are roots, don't take the root" |
| 3 | היקף משולש ABC · Triangle perimeter from coordinates | 8747-8793 | BC split at the y-axis (5 + 9 = 14); drop the altitude from A (5 + 3 = 8); split the base by A's x (3 and 6); 6-8-10 and silver 8, 8, 8√2. "It's really Pythagoras: review the triples and the silver/golden triangles." Recap: parallel → subtract or add the parts; slanted → right triangle | solve-geo37-g156 (19 + 12; 16 + 8; 24 and 7; silver 24√2; 7-24-25) | SAME (every step and her closing advice; English adds "don't add the altitude" and two traps) |
| 4 | מעגל במערכת צירים · Circle on the plane | 8795-8882 | Find the radius first; tangent to both axes → radii to the axes form a square, centre (r, r) like (3,3); centre on an axis → radius = x of the point − x of the centre; most common: centre at the origin → radius to a given point → right triangle (3, 4, 5) → 10π, 25π | geo-157 (all slides) | SAME ((5,5); 9 − 5 = 4; 10-24-26 → 52π, 676π). English adds the other quadrants ((−6, 6)), "the centre's x is not the radius unless it touches the y-axis", and the square of side 2r |
| 5 | מעגל r = 6, y של A = 3 · Find α (circle) | 8843-8882 | Close a right triangle: leg 3, hypotenuse 6 → no Pythagoras needed: a leg that is half the hypotenuse → golden triangle → α = 30. Harder version: the sector = 36π/12 (360/30, or "90 fits 3 times") | solve-geo37-g158 (r = 8, y = 4; sector 64π/12 = 16π/3) | SAME |
| 6 | שיפוע ישר · Slope: equal steps, lines through the origin | 8884-9033 | Constant slope → "stairs" → congruent triangles → equal widths and heights. C(3,4) given, AB = BC = CD: each step 3 wide, 2 high → AD: 9 and 6 → √117. Alternative: one step's length × 3. **Then she shows √117 = 3√13 by the digit-sum test (1+1+7 = 9, so 117 divides by 9: 9 × 13).** Lines through the origin: x : y constant ((2,1), (4,2), (6,3)) | geo-159 (A(−24,0), C(0,10): steps 12 × 5; AD = 39) | CHANGED: (a) the main path is now "Pythagoras on one step × 3" (5-12-13 → 39), her full-triangle √117 is the "heavy numbers" alternative; (b) her root case survives only as one line ("root 13 × 3 = root 117, because 117 is 9 times 13"); **her digit-sum way of seeing 117 = 9 × 13 is gone.** English adds: slope = up ÷ across (not the step length), negative side, non-origin lines, slope 0 / no slope, y = mx + b |
| 7 | ישר דרך הראשית – A(−a,−b) · Which can't be B (edge question) | 8968-9033 | Helper triangles a, b and x, y → similar (90°, parallel lines) → x/y = a/b; plug each choice in: a²/b² ≠ a/b because a ≠ b → the answer; check the others anyway (1/b ÷ 1/a = a/b; 2a/2b). "Not easy, rewind; an edge question at the end of a section" | solve-geo37-g160 (A(−3p,−3q); p³/q³) | SAME (every step and her closing words). English adds a faster plug-in-numbers method (p = 1, q = 2) and why cubing breaks the ratio |
| 8 | מערכת צירים – פתיח · Intro: two kinds of questions | 9035-9045 | Kind 1: standard geometry with the data on the axes, pull the data out; kind 2: understanding lines (parallel, crossing) | geo-161 | SAME |
| 9 | טרפז ישר זווית, E ראשית · Right trapezoid, E is the origin (medium+) | 9047-9089 | AD ∥ x-axis (same y) → 5 − 2 = 3; AE = EB → triangles on the line are similar, here congruent (equal hypotenuses) → 2, 2 → BC = 7, height 4 → 20 | solve-geo37-g162 (A(4,3), D(10,3) → 6; 4 and 3 → 14, 6 → 60) | SAME (English adds the traps 36 and 48). **Order:** English plays g163 before g162 |
| 10 | סיבוב מלבן – נפח · Rotate a rectangle about its side ∥ y (medium) | 9091-9131 | Full turn → cylinder; base area × height; dimensions from the opposite corners (differences 9 − 5 = 4, 12 − 2 = 10; the fixed y / fixed x along each side) → 160π. "A 3D question on the axes" | solve-geo37-g163 (corners (−4,2), (2,9) → r 6, h 7 → 252π) | SAME (English adds "the width is the radius because we turn around the side" and the traps 63π, 294π) |
| 11 | שטחים כהים – A(4,4) · Shaded areas, circle at the origin (hard) | 9133-9246 | (1) Scheme: half circle − triangle; radius = silver 4√2 → 32π → 16π. **Partial calculation**: the answer must be 16π − something → only choice 2; "on the exam mark and move on, it's probably the last question". In the lesson: triangle with the outside height 4 → 8√2; partial calculation also works from the triangle's side. (2) Estimating: approximate each choice (√2 ≈ 1.5) → choice 4 is negative; then a 4 × 4 square (16): "the top shaded part is at least the square, the bottom one similar" → choices 3 and 1 out. Recommended: the math with partial calculation | solve-geo37-g164 (A(8,8) → 8√2 → 64π; 64π − 32√2) | CHANGED: the scheme, partial calculation (from both sides), the outside height, the negative choice and her recommendation are all kept. **Her square comparison was replaced by two bounds** (semicircle > 192, triangle < 48 → area > 144), and the English says why: "the top piece is an eighth of the circle — smaller than the square". That is correct, and it is also true of her numbers: there the top piece is 45°/360° of 32π = 4π ≈ 12.6, less than the 16 square, so her "at least 16" step does not hold (her final answer is still right). The negative-choice check uses √128 < 12 instead of √2 ≈ 1.5 |
| 12 | משושה משוכלל על הצירים · Regular hexagon, CD on the x-axis (hard) | 9248-9283 | The shaded part = 5 equilateral triangles (3 rhombi → equal-area triangles; the white corner triangle has the same area); C(2,0) → 120° → 60° → golden 30-60-90 → side 4 → 5 · 16√3/4 = 20√3 | solve-geo37-g165 (C(4,0) → side 8 → 80√3) | SAME (English names the 30-30-120 triangle) |
| 13 | ישרים מקבילים m, n · Parallel lines, find B (hard) | 9285-9318 | "When it's not clear, go given by given"; a right triangle under each line; parallel → equal slope → similar triangles → y-leg is half the x-leg → down 2 floors → B(0,2). "A similarity question on the axes" | solve-geo37-g166 (C(8,6), A(4,10) → ¾ or "halved" → B(0,7)) | SAME (English adds the y = mx + b check) |
| 14 | נקודות משותפות עם ציר x · How many common points with the x-axis (medium) | 9321-9370 | Kind-2 question; sketch; go through the choices (possible → cross out): 1 (slanted), 0 (parallel), infinitely many (on the axis) → 2 impossible (needs a parabola). Three situations: parallel–perpendicular, crossing or not, coinciding | solve-geo37-g167 (impossible choice: 3) | SAME |
| 15 | ישר a ו-ישר b – מה נכון בהכרח · Lines a and b, which must be true (medium) | 9373-9423 | a misses the x-axis → parallel to it → every point has the same y; **efficiency: choices 1 and 3 have the same opening, so after 1 fails check 3 and skip 2 and 4**; mark and move on, check the rest in the lesson; trial and error (draw the two points) also works, understanding is better | solve-geo37-g168 (a misses the y-axis, b the x-axis) | SAME (the axes are swapped; her "same opening" trick is kept: "one and two start the same … its twin is the next one to check"). English adds "keep the right coordinate: x on a vertical line, y on a horizontal one" |
| 16 | ישר שאינו מאונך לצירים · Line perpendicular to neither axis (medium+) | 9425-9456 | Sketch; a point with the same x → vertical (forbidden); the shortcut: the point can't share the given x or the given y | solve-geo37-g169 (through (3,−5); (−1,−5) impossible) | SAME |
| 17 | 20 שאלות תרגול עצמי · 20 self-practice questions | 9459 | — | geo37-core-p01 … p27 (q37.txt) | SAME (kept, more added) |

**Count by row (17 rows):** SAME 15 · CHANGED 2 (6, 11) · PARTIAL 0 · MISSING 0.

### Count by video (her 17 units)

| Unit | Match |
|---|---|
| Lesson 1 points | SAME |
| Lesson 2 segment length | SAME |
| Q triangle perimeter (g156) | SAME |
| Lesson 3 circle | SAME |
| Q circle α (g158) | SAME |
| Lesson 4 slope | CHANGED (main path swapped; the digit-sum step gone) |
| Q origin line, which can't be B (g160) | SAME |
| Intro to the question lesson (geo-161) | SAME |
| Q trapezoid (g162) | SAME (played after g163) |
| Q rotation (g163) | SAME |
| Q shaded areas (g164) | CHANGED (her square comparison replaced by bounds; hers was not valid) |
| Q hexagon (g165) | SAME |
| Q parallel lines (g166) | SAME |
| Q common points (g167) | SAME |
| Q lines a and b (g168) | SAME |
| Q neither perpendicular (g169) | SAME |
| 20 practice questions | SAME |

**By video: SAME 15 · CHANGED 2 · PARTIAL 0 · MISSING 0.**

---

## 2. English → Hebrew (English topic-37 parts with no Hebrew equivalent = added)

| English video / part | Added content | Hebrew source? | Recorded? |
|---|---|---|---|
| geo-154 slides "Four quadrants", "Reflections", "On an axis" | Quadrants, reflections across the axes / the origin, points on an axis | none | no |
| geo-155 (parts) | The 7 − 2 classic mistake, line vs segment, "look for the number under the root" | none | no |
| geo-157 slides "Any quadrant" + parts | Tangent circles in other quadrants; centre's x ≠ radius | none | no |
| geo-159 slides "Slope is a ratio", "Negative side too", "Other lines", "The line equation" | Slope as up ÷ across, slope 0 / undefined, y = mx + b | none | no |
| solve-geo37-g160 slides 2 and 6 | Plug in numbers (p = 1, q = 2); why cubing fails | none | no |
| r26-t37-box + solve-q-r26-t37-10 | Area of a slanted triangle by boxing it in | none | no |
| solve-q-r26-t37-05 | Midpoint: repeat the move / average the coordinates | none | no |
| solve-q-r26-t37-07 | Where a line given by an equation cuts the axes | none | no |
| solve-geo37-g166 (part) | The y = mx + b check | none | no |
| traps added in g156, g162, g163 | 55 + 24√2, 80; 36, 48; 63π, 294π | none | no |
| r26-t37-summary, mem-coordinates | Summary and reference card | none | no / — |
| practice geo37-core-p21 … p27 and the r26 practice | Extra practice | none | — |

---

## 3. Missing from English: restore?

| # | Her content | Where it would go | Target recorded? | Recommendation |
|---|---|---|---|---|
| 1 | geo-159: the digit-sum way to see that 117 = 9 × 13 (so √117 = 3√13) | geo-159 slide "The length AD", after "117 is 9 times 13", 1 sentence: "How do you see it? 1 + 1 + 7 is 9, so 117 divides by 9" | no | **Optional.** It is a quick check worth having, but the English numbers (39) no longer need it; it only fits the one-line root example |
| 2 | g164: her square comparison | — | no | **Not needed; do not restore.** It does not hold in her numbers either (the top piece is 4π ≈ 12.6 < 16). The English bounds are the correct replacement |
| 3 | The order g162 (trapezoid) → g163 (rotation) | the flow | — | **Not needed** (both are kind-1 questions, either order works). Optional to restore her order |

## 4. Wrong in the English (not about her content)

- **The lesson `r26-t37-box` ("Area of a Slanted Triangle") is not in the flow.** The video exists, but the flow goes from
  solve-geo37-g156 straight to the question q-r26-t37-10 and its solution "Box it in", so a student meets that question before
  the box method is taught (the solution video then teaches it). Either add r26-t37-box to the flow before q-r26-t37-10 or drop it
  on purpose. (Topics 35, 36 and 38 have their added lessons in the flow; this is the only one missing.)
