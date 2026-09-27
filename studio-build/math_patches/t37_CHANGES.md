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
