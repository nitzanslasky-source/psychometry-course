# Topic 34 (Polygons): changes for the teacher

Patch: `math_patches/t34.py`. Check: `python3 math_check.py 34` gives 0 problems, 0 warnings and 0 layout problems.

## 1. Wrong rules
The review found no wrong rules in the videos. Two places taught a shaky method, and I fixed both:
- **Practice p12 solution** used "the angle between a tangent and a chord is half the arc". T33 does not teach this rule. The solution now uses the taught route: radius ⊥ tangent, triangle OAF is equilateral, so ∠AFT = 30° and ∠ATF = 90°.
- **Q9 video, slide 4** said "in regular polygon questions the drawing is accurate… measure with your fingers". I removed this. The slide now gives the real reason: the square's side is a hypotenuse, and AE is only a leg. The board item now says "Square side = hypotenuse > leg AE".

## 2. Missing methods (added)
**Polygons lesson (geo-104): 3 new slides**
- **"How many diagonals"** (new slide 5, after "Split into triangles"). It reuses the heptagon figure. From one vertex you can draw n − 3 diagonals, which make n − 2 triangles. In total there are n(n − 3)/2 diagonals, because each diagonal has two ends. Example: a heptagon has 14.
- **"Exterior angles"** (new slide 12, with a new figure: a pentagon with every side extended). Exterior angle = 180° − angle. All the exterior angles together make 360° (the "walk around the polygon" reason). In a regular polygon each one is 360°/n, which is the same as the central angle. This explains why the teacher's "complete to 180" tip works.
- **"Angle → sides"** (new slide 13):
  - The fast method: n = 360/(180 − angle). Example: 150° → 12 sides.
  - The classic question "which could be an angle of a regular polygon?": 140° works (9 sides), 130° does not (7.2).
- **Concave polygons:** slide 7 ("Regular") has two new spoken lines. The folded hexagon still has the angle sum 720°. One of its angles is bigger than 180°.
- **Recap** has two new board lines: the diagonal count, and exterior angles / n from an angle.
- The sidebar has the 3 new labels, and every slide's highlight was reset to match.

**New lesson video: "Polygons Meeting at a Point" (r26-t34-meet), 4 slides, with a new figure (hexagon + square)**
- The angles around a point add up to 360°. For the hexagon and the square, the gap is x = 360° − 120° − 90° = 150°.
- Close the gap into a triangle. Both of its sides equal the common side, so it is isosceles. Base angles: (180° − 150°)/2 = 15°.
- Recap: polygons that fill a point have angles that add up to 360° (the honeycomb example).
- The lesson comes with a new memory card, "Polygons meeting at a point" (mem-r26-t34-meet).

**New guided questions (each has a solution video with two slides)**
- **Q13** (q-r26-t34-01): each angle is 160°. How many sides? Answer 18. The video shows the formula way first, then the exterior-angle way. It also explains the trap choice 9 (using 180 instead of 360).
- **Q14** (q-r26-t34-02): 7 diagonals from one vertex. How many diagonals in all? Answer 35. The video explains two traps: 70 (forgot to halve) and 45 (counted the sides too).
- **Q15** (q-r26-t34-03): a square and a regular pentagon on a common side. Find ∠ADG. ∠DAG = 162°, so the answer is 9°. The video explains the trap choice 18° (both base angles together).
- The three solution videos use the group name "Advanced Polygons III". They come after Q12, followed by the new lesson, its card and Q15.

**Other teaching additions**
- **Q6 video, slide 3:** two new spoken lines. In a regular hexagon the short diagonal = side × √3, and the long diagonal = 2 × side.
- **"Haman's ear" (Two Hexagon Partitions, slide 4):** the video now also calls it "the star partition". It explains that a Haman's ear is a cookie with three corners. The line about the hamantasch paper was removed.

**Memory cards**
- **"Polygons — rules to know":** three new rows (diagonals, exterior angles, sides from one angle). Two new tips ("could it be an angle?" and concave polygons).
- **"Regular polygons — facts to know":** a new table, "Regular hexagon, side a":
  - radius a
  - short diagonal a√3
  - long diagonal 2a
  - area 6·a²√3/4 = (3√3/2)a²
  - triangle ACE = ½ of the hexagon
  - rectangle ACDF = ⅔ of the hexagon

  The "Haman's ear" row is now called "Haman's ear (star)".
- **New card:** "Polygons meeting at a point".

## 3. Text
- **All 37 existing written solutions were rewritten** (12 guided and 25 practice) in TeX, with the numbers shown. This removed:
  - every ":" used for division (5:√2, 25:4, 10:√3, 84:12…)
  - the typos "side,4.8", "a135°", "hexagon's120°", "triangle:48" and "18;48"
  - the untaught terms. p21 and p22 now use "exterior angle", which is now taught. p23 uses the n − 3 rule, which is now taught.
- **p09 solution** now uses the isosceles trapezoid ABGH, the method from Q4 way 2. It no longer needs the circle.
- **Stems:**
  - The given conditions are now stacked with `\begin{cases}` in g106 (Q1), p09 and p16.
  - Q4 (g110) now says "angle ADB (marked x in the figure)", and p06 says "angle BAC (marked α)".
  - p22 now says "exterior angle" instead of "exterior turning angle".
  - p18 has clearer wording ("By how much is … greater", "whole numbers").
  - The stem copy on the Q12 slides showed "12−sided" (a math minus). It is now synced to "12-sided".
- **Boards:** every ":" used for division is now a fraction:
  - 540°:5, 108°:3 and 360°:6 in the lesson
  - 540°:5 and (180°−108°):2 in the Q4 video
  - 360°:8 in the Q5 video
  - 720°:6 and 30:3 in the Q6 video

  The teacher's appear labels use ÷. Slide 6 ("+1 side") showed "5: 540° → 6: 720°", which read like ratios. It now shows "540° → 720° → 900° → 1080° (5, 6, 7, 8 sides)".
- **American spelling:** "centre" → "center" and "practise" → "practice" in the topic's videos.

## 4. Figures
- **p09:** removed the extra segment FC. The question does not use it.
- **Q5 (g111):** moved the "O" label off the radius line. I also fixed the copies on the 3 slides of the Q5 video and on the lesson's "Isosceles triangles" slide (v490, v510–v512).
- **Lesson "Regular" slide (v487):** the figure now has a description. It had an empty one.
- **Existing question figures:** 24 of the 25 are cropped to the drawing (g106 already filled its frame). They keep the 16:9 frame, so the lines and labels are 1.1–1.5 times bigger. I checked all of them in renders.
  - The height of the drawing limits the zoom. For a bigger gain, the site would need to allow taller figure frames. That is a site decision, not a patch decision.
- **New figures, in the same style (ink, teal, light-teal fill, DejaVu 20):**
  - Exterior angles (lesson)
  - Hexagon + square (new lesson)
  - Square + pentagon (Q15)
  - Pentagon with an inner equilateral triangle (practice)
  - A square with its corners cut off to make an octagon (practice)
  - A hexagon with rectangle ACDF shaded (practice)

  None of them labels the answer.

## 5. Practice (27 → 33 questions, ordered from easy to hard)
- **Removed two near-duplicates:**
  - p03 (900° → heptagon), the same as the last step of Q12
  - p14 (1,980° → 13 sides), the same as Q11
- **Added 8 questions:**
  - q-r26-t34-04: angle of a regular decagon (144°). A warm-up.
  - q-r26-t34-05: exterior angle 24°. What is the angle sum? (2,340°)
  - q-r26-t34-06: which could be an angle of a regular polygon? (140°)
  - q-r26-t34-07: 20 diagonals. How many sides? (8, by working back from the answers)
  - q-r26-t34-08: a square, a hexagon and an unknown regular polygon fill a point. (12 sides)
  - q-r26-t34-09: a pentagon with an inner equilateral triangle ABF. Find ∠AEF. (66°) Exam level.
  - q-r26-t34-10: an octagon cut from a square with side 2+√2. Find its area. (4+4√2) Exam-hard octagon question.
  - q-r26-t34-11: a hexagon with side 4. Find the area of ACDF. (16√3) Uses the diagonal a√3 and the ⅔ fact. Exam level.
- **Exam-level items now:** p04, p10, p13, p15, p16, p19, p12, and new items 09, 10 and 11. That is 10 or more.

## Could not do / for the teacher to decide
- The review asked to "put the table on the slide-10 board". The table is already there (a table item on "Three to know"). The student-view text dump just does not print tables. I made no change.
- The review suggested splitting the practice into foundation and advanced sections. The API has no function for creating a new section, so I kept one section and ordered it from easy to hard. If you want two sections, the natural split is before p05 ("Pentagon ABCDE consists of square BCDE…").
- "Haman's ear" is kept, now explained and also called the "star partition". You can drop the name if you prefer.
- Slide 11 ("Diagonals: equal parts") already gives the rule before the reason, so I left it unchanged.
