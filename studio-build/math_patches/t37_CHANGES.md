# Topic 37 — The coordinate system: changes (course review 2026-09)

Patch: `math_patches/t37.py`. Check: `python3 math_check.py 37` → 0 problems, 0 warnings, 0 layout problems.

## In numbers
- Questions: 37 rewritten (text/solutions), 12 added (4 guided with solution videos, 8 practice), 1 removed (p16).
- Videos: 1 new short lesson, 4 new solution videos. 7 slides added to existing videos, about 15 slides changed.
- Figures: 16 figures fixed (one fix often covers the same figure on several slides), 9 new figures drawn.

## 1. Wrong or misleading statements (videos)
- **Question 6 video, slide 5:** removed "In the Hebrew version we compared...". It now says: you may want to compare the top piece with the 6-by-6 square, but that is not reliable here (9π ≈ 28 < 36).
- **Question 3 video, slide 2:** the logic was backwards ("a and b are positive, because A is in the negative region"). Now: "We are given that a and b are positive — so A is in the third quadrant."
- **Question 3 video, slide 3:** the vague "once I raise them to a power I can't cancel" is replaced. A new slide "Plug in numbers" now comes first (a = 1, b = 2: (1, 8) is off the line, the other three choices are on it). The algebra follows.
- **Question 9 video, slide 3, board line 1:** "Parallel to one axis → perpendicular to the other — they never meet" was wrong (a vertical line does meet the x-axis). Now: "Parallel to an axis → never meets that axis · perpendicular to the other axis". The spoken line says the same.
- **Circles video, slide 3:** "if the circle is tangent to both axes, the center has the same x and y" is true only in the first quadrant. The line now says "in the first quadrant".
- **Question 2 video, slide 4:** the confusing "three, three, three, three — 12" became "360 divided by 30 is 12".
- Board items with ":" for division became fractions (Question 3 video "2/3 vs 8/27"; Question 8 video "Ratio of the legs: 4/10 = ?/5").
- **Question 8 video, last line:** the y = mx + b remark now matches the new line-equation slide ("b is where the line cuts the y-axis").

## 2. Methods added (they were used in questions but never taught)
- **Quadrants** — video 1 (The Coordinate Plane), new slide 8 "Four quadrants": the picture with I (+,+), II (−,+), III (−,−), IV (+,−), and "a point on an axis is in no quadrant".
  Guided question (new Question 1): (a, b) is in quadrant II; where is (b, −a)? Its solution video also teaches plugging in numbers.
  Practice: q-r26-t37-02 (which point is in quadrant II), q-r26-t37-04 (ab < 0 and a > b, where is (b, a)? exam-hard).
- **Reflections** — video 1, new slide 9 "Reflections": across the x-axis (x, −y), across the y-axis (−x, y), through the origin (−x, −y), with a figure.
  Practice: p21 (existing), q-r26-t37-03 (two reflections, then the length PR = 10; exam-hard).
- **Midpoint and "repeat the move"** — Slope video, new slide 5 "Midpoint": average of the x values and of the y values; knowing one end and the midpoint, repeat the move.
  Guided question (after Question 5): M(2, −1) is the midpoint and A(−4, 3); find B. Practice: p22, p02 (existing), q-r26-t37-06 (distance from the midpoint to the origin).
- **Negative slope** — Slope video, new slide 8 "Stairs going down": from (0, 6), 2 right and 3 down; slope −3/2; "up to the right +, down to the right −".
  Practice: q-r26-t37-08 (where a falling line cuts the y-axis).
- **Line equations** — Slope video, new slides 13 "The line equation" (y = mx + b; m = slope, b = where the line cuts the y-axis; y = −2 is horizontal, x = 4 is vertical) and 14 "Cutting the axes" (put y = 0 / x = 0; example 3x + 5y = 15).
  Guided question (after the midpoint question): 4x + 3y = 24 cuts the axes at A and B; AB = 10 (negative slope, 6-8-10).
  Practice: p25, p26 (existing, now taught), q-r26-t37-09 (y = −2x + b through (3, 1); exam-level).
- **Area of a slanted triangle (box method)** — new short lesson "Area of a Slanted Triangle" right after Question 1's solution: box it in, subtract the corner right triangles; when to use it.
  Guided question (new Question 3): A(−2, 1), B(4, −1), C(2, 5) → 36 − 20 = 16.
  Practice: q-r26-t37-11 (triangle, area 10), q-r26-t37-12 (quadrilateral, area 21; exam-hard).
- **Strong-student shortcuts**
  - Lengths video, slide 8: "Roots in the answers? Compare across² + up² with the number under the root."
  - Plug in numbers for letter questions (Question 3 video, new Question 1 video, memory card tip).
- **Memory card** — new rows: Quadrants, Reflection, Midpoint, Slanted triangle area, Slope (with sign), Parallel lines (same step), Line equation. New tips: roots in the answers; plug in easy numbers.

## 3. Text (all questions of the topic)
- Every stem, choice list and solution was rewritten in TeX (coordinates, letters, equations), with a space after every comma.
- Every solution shows the numbers step by step and uses the lesson's method (right triangle, stairs, "repeat the move", box). No ":" for division anywhere.
- "so" in the middle of a sentence became "So, ..." in solutions and spoken lines.
- The minus in coordinates like (b, −a) is now written as a sign (it showed as "(b, − a)").
- American spelling in all videos and the card (center, neighboring, practice).
- p07 reworded: "intersects the y-axis at exactly one point, and that point is not the origin."
- p03: "position vectors" replaced by "both coordinates are multiplied by the same number". p13: "scalar multiple" replaced the same way.
- p18: the solution now gives the reason: ∠DCE = ∠ADC = 60° (alternate angles, AD ∥ BC).
- p18 stem: the three givens are no longer written as three equations side by side.
- Smaller rewordings for learners: g167 ("have some number of points in common"), p11 ("a circle passes through all six vertices"), p17, g163, g164.

## 4. Figures
- **Video 1, slides 5–7:** each slide now shows only its own point (A, then B, then C). Before, all three points were drawn from slide 5.
- **Grid planes (video 1, Lengths slides 2–3):** the "O" no longer runs into the "−1" labels.
- **Lengths slide 7 (v722):** "O" moved next to the origin, away from U(−1, 0). U no longer looks like the origin.
- **p10:** the thick teal line on the x-axis (the answer) was removed.
- **p25:** the intercepts 4 and 6 (the whole question) were removed from the axes.
- **Question 8 (question and both video slides):** "n" no longer runs into "C (10, 4)", and "A (5, 7)" is no longer on line m.
- **p15:** the x-axis arrow no longer runs through "C (6, 2)". B and C labels are beside the vertices.
- **Question 3 (question and 4 video slides):** "O" and "A (−2a, −2b)" are no longer on the line.
- **Slope slides "Through the origin" / "Same multiplier" / "Negative side too":** the P, Q, R, S and O labels are no longer on the line. The dashed lines no longer run through the labels.
- **Question 4 (question and 3 video slides):** the origin label E is no longer on AB.
- **Question 5 (question and 3 video slides):** "(−2, 1)" no longer runs into the x-axis.
- **p02, p20:** point labels moved off the line. **p04:** "60°" moved off OB. **p05:** removed the extra "O" that sat on "B (0, 0)" (B is the origin). **p09:** the circle no longer runs through "O".
- **New figures:** quadrants, reflections, stairs going down, cutting the axes, box method (2), guided Question 3 (question and solution versions). All use the same style as the existing figures.

## 5. Practice
- Removed p16 (the fourth question on "a line that never cuts an axis is parallel to it"; p07, Q9 and Q10 cover it).
- Added 8 questions (see section 2). The section now has 34 questions, ordered from easy to hard. It starts with p08, p21 and the quadrant question, and ends with p15, p18, q-r26-t37-04 and q-r26-t37-12.
- Exam-level items for strong students: p11, p12, p13, p15, p17, p18, q-r26-t37-03, -04, -06, -09, -12.

## Notes for the teacher
- The guided questions are renumbered by course order. The new quadrant question is Question 1 and the box question is Question 3, so the old Question 1 becomes Question 2, and so on. References like "in Question 1" inside the videos were updated automatically.
- The added lesson slides are new recordings: video 1 (2 slides), Lengths (a few lines on slide 8), Slope (4 slides), the new "Area of a Slanted Triangle" lesson and 4 solution videos.
- Please decide whether the spoken "— so ..." lines that became ". So, ..." still sound like you. Those were mechanical rewordings to follow the style rule.
- API: no gaps. Figures inside question slides (the `fig` copies on solution-video slides) were edited in place, next to the question figures.

## Pass 2 (2026-09-27, approved remove/restore plan + summary lesson)
**Removed (4 questions, 1 solution video, 1 slide, 1 card row, 3 lines):**
- Guided q-r26-t37-01 ("which quadrant", letters) and its video `solve-q-r26-t37-01`. The later guided questions renumber automatically (the box lesson's "in Question 1" still points to the triangle-perimeter question).
- Practice q-r26-t37-02 and q-r26-t37-04 (which quadrant) and q-r26-t37-08 (negative slope).
- Slope video `geo-159`: the slide "Stairs going down" (and its figure and sidebar entry). On "The line equation" slide: the draw note 'Write "y = −3/2 x + 6"…' and the spoken line after it.
- Memory card: the row "Slope | up ÷ across, with a sign…".
- Dependent lines: "Notice the stairs … a negative slope" at the end of the "Where a line cuts the axes" solution video; "Exam questions love this: they give letters, not numbers…" on the "Four quadrants" slide (it led into the removed quadrant question).

**Restored (1 question, 1 board item, 1 line):**
- geo37-core-p16 (a line through $(-4,\ 6)$ that does not cut the $y$-axis → perpendicular to the $x$-axis) is back in the practice, in the middle of the order. The text is now in TeX, and the solution shows the numbers.
- `solve-geo37-g166` slide 3: the original board is back as $\frac{10}{4}=\frac{5}{?}$, and so is the original line "If you prefer an equation: y equals two fifths x plus b. Plug in A: 7 equals 2 plus b. So, b is 5. Same answer."

**Summary lesson (1 new video):** `r26-t37-summary` "Summary" is at the end of "Learn and try", right before the practice (about 3.6 min). Slides: Summary · Points · Reflections · Along an axis · Slanted segments · Slanted triangles · Circles · Slope and midpoint · Through the origin · Lines and axes · Before you practice.

## 2026-10-05 cut repeats
Function `cut_repeats` (runs last; the old `apply` is wrapped). A lesson slide is cut only where a question video after it teaches the same idea again. Nothing in topic 37 is recorded.
- **`r26-t37-box` "Area of a Slanted Triangle"** (1.6 min, not in the Hebrew course): taken out of the flow. Every slide (box it in, subtract the three corner triangles, when to use it) is taught again by the very next video, `solve-q-r26-t37-10` ("A triangle with no horizontal side. Box it in."; box 6 · 6 = 36; corners 6, 6, 8; 36 − 20 = 16).
  - Moved into `solve-q-r26-t37-10` slide 3: "The box works for a quadrilateral too — as long as every corner touches the box." with the board item "Works for a quadrilateral too". 1.0 → 1.1 min.
- **`geo-159` "Slope"**: 6.3 → 4.8 min (13 → 11 slides). Cut "Midpoint" (taught again in `solve-q-r26-t37-05`: repeat the move, then check with the averages) and "Cutting the axes" (taught again in `solve-q-r26-t37-07`: put y = 0, then x = 0, then the right triangle). Neither is in the Hebrew lesson. Kept: "The line equation" (y = mx + b, horizontal / vertical lines; no question teaches it) and everything from the Hebrew lesson.
- Sidebar updated. The summary `r26-t37-summary` is unchanged (the box method, the midpoint and the axis points are still taught in the question videos).
- Saved: about 3.0 min.

## 2026-10-06 renumber pass
Function `renumber_pass` (runs last, after `cut_repeats`). Goal: the English Topic 37 must not look like the Hebrew
course. Same idea, trap, level and methods; new numbers (letter-only questions: new letters / axis / choice order).
`RN_RECORDED` is empty: no Topic 37 take in ~/Documents/Course.recordings (only "1 Algebra" exists).
Every coordinate figure of a changed question or lesson example was redrawn to the new points at their true positions
(new helper `RPlane`, same style as the old figures). Numbers were checked against base-v18 and the Hebrew subtitles
(03-Geometry-Original-Subtitles.txt); triples used are 7-24-25, 8-15-17, 9-12-15, 5-12-13 (step) and 10-24-26, not the
Hebrew 3-4-5 / 6-8-10. Every answer and trap was re-computed in python. Check: `python3 math_check.py 37 32` and
`python3 math_check.py 37` → 0 problems, 0 warnings, 0 layout problems. All changed videos rendered and checked.

**Guided questions (all 11 Hebrew-derived; solution videos rewritten: board, speech, draw cues, question figure)**
| Id | Old | New | Answer · key |
|---|---|---|---|
| geo37-g156 | A(4, 7), B(−8, −5), C(13, −5): 12-12 silver + 9-12-15 | A(5, 16), B(−19, −8), C(12, −8): 24-24 silver + 7-24-25; traps 55 + 24√2 (altitude as AC), 80, 31 + 24√2 | 56 + 24√2 · 1 → 3 |
| geo37-g158 | r = 10, y of A = 5 | r = 8, y of A = 4; "harder version" sector 64π/12 = 16π/3 | 30° · 2 → 3 |
| geo37-g160 | A(−2a, −2b); (a³, b³), (3a, 3b), (1/b, 1/a), (a/2, b/2) | A(−3p, −3q); (2p, 2q), (1/q, 1/p), (p³, q³), (p/3, q/3); plug-in p = 1, q = 2; cubes 1/2 vs 1/8 | (p³, q³) · 1 → 3 |
| geo37-g162 | A(3, 4), D(8, 4) → 64 (traps 40, 48, 80) | A(4, 3), D(10, 3): B(−4, −3), BC = 14, h = 6 → 60; traps 36 (rectangle), 48 (BC = 10), 120 (no ÷2) | 60 · 1 → 2 |
| geo37-g163 | (−2, 1), (3, 9): r 5, h 8 → 200π | (−4, 2), (2, 9): r 6, h 7 → 252π; traps 63π (half width), 294π (swapped), 42π | 252π · 4 → 2 |
| geo37-g164 | A(6, 6): 36π − 18√2 | A(8, 8): r = 8√2, 64π − 32√2; partial calculation + estimation (8√2 − 4π < 0; > 144) both still work | 64π − 32√2 · 2 → 4 |
| geo37-g165 | C(3, 0): side 6 → 45√3 | C(4, 0): side 8 → 5 · 16√3 = 80√3 | 80√3 · 3 → 2 |
| geo37-g166 | C(10, 4), A(5, 7) → B(0, 5) | C(8, 6), A(4, 10) → B(0, 7); both methods (halve the legs / y = ¾x + b) | (0, 7) · 3 → 4 |
| geo37-g167 | line ∩ y-axis; Infinitely many / 3 / 0 / 1 | line ∩ x-axis; 1 / Infinitely many / 0 / 3 (video: horizontal line instead of vertical) | 3 · 2 → 4 |
| geo37-g168 | (4, −3) → (4, 7) on a; (−2, 5) on b | (−6, 1) → (−6, −7) on a; (2, −3) on b; video now checks choice 1, it fails, so its twin (choice 2) | choice 2 · 1 → 2 |
| geo37-g169 | through (−2, 4); impossible (−2, 9) (same x) | through (3, −5); impossible (−1, −5) (same y → horizontal); others (6, 1), (0, 2), (−4, 3) | (−1, −5) · 1 → 2 |
The three English guided questions (q-r26-t37-05 midpoint, -07 line equation, -10 box method) were not Hebrew and are unchanged.

**Practice (Hebrew study-guide questions p01–p20; figures redrawn where there is one)**
| Id | Old | New | Answer · key |
|---|---|---|---|
| p01 | rhombus A(0, 4), D(5, 0) → 40 | A(0, 6), D(7, 0) → 84; traps 42, 168, 63 | 84 · 4 → 2 |
| p02 | A(6, 0), B(0, −2) → C(−6, −4) | A(−4, 0), B(0, 3) → C(4, 6) | (4, 6) · 4 → 3 |
| p03 | (−6, −5) & (12, 10) | (4, −6) & (−6, 9) (× −1.5); others share x or y | key 3 → 2 |
| p04 | r 6, 60° → A(3, 0) | r 14, 60° → A(7, 0) | (7, 0) · 2 → 4 |
| p05 | A(5, 12), B(0, 0), C(10, 0) → 36 | A(9, 12), B(0, 0), C(18, 0) → 48 (9-12-15); trap 42 = altitudes | 48 · 2 → 3 |
| p06 | B(−1, 3), C(5, 3), area 18 → A(5, 9) | B(−2, −1), C(6, −1), area 20 → A(6, 4); trap (6, 9) | (6, 4) · 1 → 3 |
| p07 | meets y-axis once, not ⟂ y-axis | meets x-axis once, not ⟂ x-axis; choices reordered | right triangle · 2 → 4 |
| p08 | (−3, 2) & (−3, −5) | (4, −1) & (4, 6); trap (4, −1) & (7, −1) | key 3 → 1 |
| p09 | center (12, 0), r 13 → y = 5 | center (15, 0), r 17 → y = 8 (8-15-17) | 8 · 4 → 2 |
| p10 | center on y-axis → tangent x-axis | center on x-axis → tangent y-axis | y-axis · 4 → 2 |
| p11 | B(6, 0) → radius 4 | B(9, 0) → 3x = 9, side 6 → radius 6 | 6 · 3 → 4 |
| p12 | b through (0, 3); impossible (0, −2) | b through (4, 0); impossible (−5, 0) | key 4 → 3 |
| p13 | (a, c); (−2a, −2c) | (m, n); (−3m, −3n); others (1/m, 1/n), (2n, 2m), (m, −n) | key 3 → 2 |
| p14 | A(0, 3), B(2, 0) → 13 | A(0, 5), B(3, 0) → 34; trap 64 = (3 + 5)² | 34 · 2 → 3 |
| p15 | B(−2, 2), C(6, 2), area 40 → A(2, 12) | B(−3, −1), C(5, −1), area 24 → A(1, 5); trap (1, 6) | (1, 5) · 1 → 2 |
| p16 | through (−4, 6), misses y-axis → ⟂ x-axis | through (5, −3), misses x-axis → ⟂ y-axis; trap (5, 3) | key 2 → 3 |
| p17 | square side 3 → 9π/2 − 9 | side 4 → 8π − 16 | 8π − 16 · 3 → 1 |
| p18 | A(0, t), C(2t, 0), 60° → (2t + t/√3, t) | A(0, k), C(3k, 0), 60° → (3k + k/√3, k); trap (4k, k) | key 4 → 1 |
| p19 | A(0, 5), B(6, −1) → √72 | A(0, −3), B(5, 4) → √74 (lesson "like root 72" → "root 74") | √74 · 2 → 3 |
| p20 | A(n, 6), B(−1, −2), C(1, 0) → 7 | A(n, 7), B(−2, −5), C(0, −1) → 4; trap 8 | 4 · 1 → 3 |

**Lesson examples (Hebrew-derived; board, speech, draw cues and figures changed together)**
- "The Coordinate Plane": marks 5, 7 / −2, −3 → 3, 6 / −1, −4; A(4, 3), B(−5, 2), C(−3, −3) → A(6, 2), B(−4, 3), C(−2, −4)
  (same quadrants I, II, III); "(4, 3) and (3, 4)" → "(6, 2) and (2, 6)". Reflection example P(4, 2) (English) kept.
- "Lengths on the Plane": P(3, 4), Q(3, −2), 4 + 2 = 6 → P(4, 3), Q(4, −5), 3 + 5 = 8; R(2, 3), S(7, 3), 7 − 2 = 5 →
  R(1, 4), S(7, 4), 7 − 1 = 6; −4 to 6 → −2 to 7 (2 + 7 = 9, not 7 − 2 = 5); U(−1, 0), V(4, 12) 5-12-13 → U(−2, −3), V(6, 12) 8-15-17.
- "Circles on the Plane": tangent center (4, 4) → (5, 5); (−4, 4) → (−6, 6); C(6, 0), P(8, 0), r = 2 → C(5, 0), P(9, 0), r = 4
  (memory-card tip changed to "(5, 0) does not mean r = 5"); A(5, 12), r 13, 26π / 169π → A(10, 24), r 26 (5-12-13 × 2), 52π / 676π.
- "Slope": stairs A(−8, 0), C(0, 6), step 4 across 3 up, AD = 15 → A(−24, 0), C(0, 10), step 12 across 5 up, B(−12, 5),
  D(12, 15), AD = √1521 = 39 = 3 · 13 (the one-step shortcut is now clearly the easy way); slope 3/4 → 5/12 ("not the
  length 13; 24 across, 10 up also 5/12"); origin line (2, 3), (4, 6), (6, 9), S(−2, −3) → (3, 2), (6, 4), (9, 6), S(−3, −2).
- Duplicate check (script, whole course): no question equals a lesson or card example; the only shared point is (4, 0) in
  g165 and p12 (different questions). English summary examples ((3, 5), (6, 8), box 24 − 14) unchanged.

**Order**
- Guided: the easy English questions -05 (midpoint) and -07 (line equation) now come before the hard letters question
  g160 (all three come after the Slope lesson). The cylinder g163 (medium) now comes before the trapezoid g162 (medium-plus).
  Numbering is redone automatically (Questions 1–14).
- Practice sorted easy → hard (list `RN_ORDER`). Correct-answer positions moved in almost every question (see tables).

**Practice clean-up (32 → 26)**
- Copies removed: geo37-core-p22 (midpoint from one end, same as guided q-r26-t37-05), q-r26-t37-11 (slanted-triangle box, same as guided -10).
- Extra-bank: kept 3 warm-ups p21 (reflection), p23 (circle tangent to an axis), p26 (distance to a horizontal line); removed p24, p25, p27.
- September items: removed q-r26-t37-06 (midpoint; the Hebrew p02 covers that type). Kept -03 (two reflections + length),
  -09 (line equation y = mx + b) and -12 (box method for a quadrilateral): the Hebrew practice has none of these types.
  The result is 26, one above the audit target of 25; the teacher may drop -03 or -09 for exactly 25.

## 2026-10-06 review
Independent review of the renumber pass (same method as for topics 30–33). Fixed:
- solve-geo37-g160, slide 4 title still said "Plug in choice 1"; the cubes (p³, q³) are choice 3 now → "Plug in choice 3"
  (`review_fixes`, called at the end of `renumber_pass`).
Everything else checked OK (keys, traps, all coordinate figures at their true grid points, lesson boards and figures).
Note: g169 passes through (3, −5) and p16 through (5, −3) — different questions, but near-mirror points in one topic.
`math_check.py 34 35 36 37 38 32` and full `math_check.py` → 0 / 0 / 0.

## 2026-10-07 methods spread
- spread_methods() runs last. Shortcut · Pick values that fit line in geo37-core-p13 (m = 1, n = 2). Nothing recorded.


## 2026-10-07 study-plan order
Function `plan_order_fix` (runs LAST). Students follow the study plan (`src/lib/planData.ts` ORDER), not topic numbers; named methods were checked against the plan rank of their teaching topic.
- geo37-core-p13: "Shortcut · Pick values that fit" → "Method 2 · Pick values that fit" (topic 51 is day 6).
`python3 math_check.py 5 7 10 21 22 25 26 28 30 31 33 37 32` → PROBLEMS 0, WARNINGS 0, LAYOUT 0.
