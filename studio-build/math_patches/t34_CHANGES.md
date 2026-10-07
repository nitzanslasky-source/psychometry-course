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

## Pass 2 (teacher-approved remove/restore plan, 2026-09-27)
`python3 math_check.py 26 27 33 34`: 0 problems, 0 warnings, 0 layout problems.

**Removed (3 items)**
- Polygons video, slide "Angle → sides": the last 5 lines ("a classic exam question: which of these could be an angle of a regular polygon?", the 140°/130° examples and the board item). "n from an angle" stays.
- Polygons card: the tip "Could it be an angle of a regular polygon? …".
- Practice q-r26-t34-06 ("which could be an interior angle", 140°).
- The guided numbering does not change.

**Restored**
- Practice geo34-core-p03 (900° → heptagon) and geo34-core-p14 (1,980° → 13 sides), with the solutions in TeX. They are placed at the start of the practice (easy).
- Polygons video, slide "+1 side = +180°": the board is back to "5: 540° → 6: 720° → 7: 900° → 8: 1080°". The label colons are outside the math, so they are not read as fractions.
- Two Hexagon Partitions, slide 4: the original line "…fold the three corners in, like the paper, and you get a hamantasch" is back. After it, one short line explains what a hamantasch is and gives the name "star partition".
- Practice size: 33 → 34, ordered easy → hard.

**Summary lesson (new)**
- `r26-t34-summary` "Polygons: Summary", at the end of the learn section, right before the practice. Slides: Summary · Angle sum · One angle · Exterior angles · Diagonals · Triangles inside · Areas · Meeting at a point · Before you practice.

## 2026-10-05 cut repeats
Function `cut_repeats` (runs last). A lesson slide is cut only when a question video after it teaches the same idea again. Nothing in topic 34 is recorded.
- **Polygons** (`geo-104`) 12.6 → 10.9 min, 17 → 15 slides (Hebrew 11.3). CUT slide 5 "How many diagonals" → `solve-q-r26-t34-02` (n − 3 from one vertex, n × 7, halve because each diagonal has two ends). CUT slide 13 "Angle → sides" → `solve-q-r26-t34-01` (formula way and the fast way through the exterior angle). Recap: the diagonals-count item and line are gone; the last item is now "Exterior angles: 360° in all" and the line "And the exterior angles always add up to 360." KEPT slide 12 "Exterior angles": the question video uses the facts but does not define the exterior angle or give the reason (walk around = 360). Sidebar: 14 labels.
- **Polygons Meeting at a Point** (`r26-t34-meet`, 1.7 min) REMOVED from the flow: its whole method (360 around the shared vertex, then the isosceles triangle on the common side) is taught again right after by `solve-q-r26-t34-03` (square + pentagon). MOVED its one extra fact into `solve-q-r26-t34-03` slide 2: "The same 360 tells you when regular polygons fill a point with no gaps: three hexagons, 3 times 120 — a honeycomb." + board item "Fill a point: 3 × 120° = 360°" (1.1 → 1.2 min). Slide 1 "the picture from the lesson" → "the exam loves this picture".
- Summary `r26-t34-summary` slides 4, 5, 8 still sum up exterior angles, the diagonal count and polygons meeting at a point — all taught in question videos now; no change needed.

## 2026-10-06 renumber pass
So the English course does not look like the Hebrew one: every Hebrew-derived question in topic 34 has new numbers
(new letters / names / a changed shape where there is one). Concept, trap, level, number of steps and methods stay the
same. Every guided solution video was rewritten to match (spoken lines, draw cues, board items, choice numbers, slide
titles that quote numbers); every changed figure was redrawn (g106, g111, g113, p04, p08, p15, p16) or relabelled with
the new letters (g110, g114, p06, p09, p12 — question figure and every slide copy). Function `renumber_pass(M)` runs
last in `apply()`, after `cut_repeats`. Nothing in topic 34 is recorded (checked ~/Documents/Course.recordings), so
`RN_RECORDED` is empty.

**Counts:** 12 guided questions renumbered, 12 solution videos rewritten (g106, g107, g111, g115 by exact number swaps
+ choice-order map; g108, g110, g112, g112-area, g113, g114, g116, g117 slide by slide). 20 Hebrew practice questions
renumbered. Lesson examples: none changed — the lesson boards only show general facts (pentagon 108°, 5: 540° …
8: 1080°, central angles), and the English-made summary / card examples (1800° → 12 sides, 140° → 9 sides, hexagon
9 diagonals, 150° → 12 sides) match no question. **Practice 34 → 25.**

**Practice clean-up:** copy removed: p21 (150° → 12 sides = the card example and the same type as guided q-r26-t34-01).
English extras: kept p26 (one regular angle from n) and p27 (star partition: half the hexagon); removed p22 (exterior
angles — q-r26-t34-05 practises them), p23 (diagonals from one vertex — q-r26-t34-07), p24 (hexagon area — g107),
p25 (octagon corner triangles — p17). September items: kept q-05 (exterior angles), q-07 (total diagonal count),
q-09 (regular polygons on a common side → isosceles) — types the Hebrew practice does not have; removed q-04 (one
angle of a decagon), q-08 (polygons filling a point — p13, p15), q-10 (octagon area — p17, g108), q-11 (hexagon
rectangle area — g112, p27). Order easy → hard kept (the removed items just drop out).

**Kept on purpose:** the English-made guided q-r26-t34-01 … 03 and their videos. g110, g114, p06, p09, p12 and p19
have no numbers: new letters (and new names in g114) + new choice order; their answers (36°, both, 22.5°, 90°, 90°,
4:1) cannot change. p19 has no letters in the stem: choice order only. The octagon-pattern examples "side 3, side 7"
in g108's video stay (not Hebrew: the Hebrew used 4 and 1). Guided order unchanged (it already goes topic by topic,
easy → hard inside each group). The correct answer moved in 10 of 12 guided questions.

**Checks:** every answer recomputed in Python; every method in each video recomputed with the new numbers (g106 two
partitions, g112 golden triangle + estimates 24·1.75 = 42 / 24√2 ≈ 34 / 28·1.5 = 42, g112-area full way + 1/6 way,
g113 plug in 1 + counting sides / rhombi, g116 simplifying 1440 → 144 → 72 + anchor 1080 → 1260 → 1440, g117
formula + "+6 sides"). Exactly one correct choice in each; traps still in the choices (one triangle 36√3, half the
rectangles 200 + 100√2, trapezoid only 285, 24√3 just under 42, n − 2 = 8, hexagon = number of extra sides, 70/16·8 = 35,
polygon angle 135° in p15, the given perimeter 28 in p13, n + 1 = 13 in p20). New numbers checked against the Hebrew
subtitles (3-4-5 with 4 → 28, side 6 → 54√3, octagon 6 → 72 + 72√2, pentagon statements, ACE 18 → 12√3, side 2 → 3√3,
3 squares, 2 + 2√2, 1260° → 9, 10 and 13 sides → pentagon): none land back on them; the triple is 8-15-17 (not 3-4-5
/ 5-12-13). Duplicate scan over topics 1–34: no question equals another question or a lesson / card example.
`python3 math_check.py 34 32` → PROBLEMS 0, WARNINGS 0, LAYOUT 0. Rendered and looked at all 12 rewritten videos and
all 12 changed question figures. No "Question N" in spoken lines.

| id | old (English, Hebrew-derived) | new | answer |
|---|---|---|---|
| geo34-g106 | 5-12-13: AB = BC = AE = 12, DE = 5 → 204 | 8-15-17: 15, 15, 15, DE = 8 (redrawn) | 345 (2) |
| geo34-g107 | hexagon side 8 → 96√3 | side 12 | 216√3 (4) |
| geo34-g108 | octagon side 5 → 50 + 50√2 | side 10 | 200 + 200√2 (1) |
| geo34-g110 | pentagon ABCDE, angle ADB | PQRST, angle PSQ; new order | 36° (3) |
| geo34-g111 | octagon, false "P = 8r" (45°, 67.5°) | regular 9-sided polygon, false "P = 9r" (40°, 70°), redrawn, new order | statement 3 (3) |
| geo34-g112 | perimeter ACE 30 → 20√3 | ACE 42 → AC 14 | 28√3 (2) |
| geo34-g112-area | hexagon side 6 → 27√3 | side 10 | 75√3 (3) |
| geo34-g113 | 4 squares, Maya "3 ×", Daniel "areas" → only Daniel | 5 squares (redrawn), Ella / Adam, plug in 1 | only Adam (4) |
| geo34-g114 | octagon, AB ⊥ CD at E, Lina / Noam → both | KL ⊥ MN at T, Sara / Ben; new order | both (2) |
| geo34-g115 | white 8 + 8√2 | 12 + 12√2 | 12 + 12√2 (1) |
| geo34-g116 | angle sum 1,620° → 11 | 1,440° (trap 8) | 10 (3) |
| geo34-g117 | 12 and 17 sides → heptagon | 14 and 20 sides (trap hexagon) | octagon (2) |
| p01 | hexagon side 3 → AGHF 24 | side 5 | 40 (2) |
| p02 | four hexagons, side 2.4 → 12 | side 2.6 | 13 (3) |
| p03 | which polygon has 900° → heptagon | 1,620° (trap 9 sides) | 11 sides (2) |
| p04 | 4 octagons around a square opening → 5/8 | 6 hexagons around a hexagonal opening (redrawn) | 1/2 (2) |
| p05 | square side 4 + right isosceles roof → 12 + 4√2 | side 6 | 18 + 6√2 (1) |
| p06 | octagon ABCDEFGH, angle BAC | KLMNPQRS, angle LKM; new order | 22.5° (4) |
| p07 | hexagon side 7 → CF 14 | side 9 | 18 (4) |
| p08 | two heptagons, boundary 84 → 49 | two octagons (redrawn), boundary 70 | 40 (2) |
| p09 | octagon, α = DEF, β = ABG | PQRSTUVW, α = STU, β = PQV; new order | 90° (3) |
| p10 | 8 circles r 2 → 20π | r 3 | 45π (4) |
| p11 | parallelogram vs regular pentagon / heptagon / decagon | trapezoid vs regular pentagon / hexagon / octagon | trapezoid (3) |
| p12 | hexagon ABCDEF, tangent at F, T → ATF | KLMNPQ, tangent at Q, S → KSQ; new order | 90° (1) |
| p13 | six rhombi, perimeter 20 → 30 | perimeter 28 | 42 (3) |
| p14 | angle sum 1,980° → 13 | 2,160° | 14 (2) |
| p15 | decagon + 5 attached triangles → 144° | octagon + 4 attached triangles (redrawn) | 157.5° (4) |
| p16 | AB = AE = 4a, BC = a, 120° → 8√3a² | AB = AE = 6a, BC = 2a (redrawn) | 21√3a² (2) |
| p17 | octagon side 3, cross → 9 + 18√2 | side 8 | 64 + 128√2 (2) |
| p18 | P: n + 1, Q: m + 3 → 180°(n − m − 2) | K: a + 2, L: b + 5, a > b + 3 | 180°(a − b − 3) (2) |
| p19 | ratio of circle areas 4 : 1 | new choice order | 4 : 1 (4) |
| p20 | 10 regions → 9 sides | 13 regions | 12 (3) |

## 2026-10-06 review
Independent review of the renumber pass (built with / without `renumber_pass`, every question, solution video, lesson,
card and figure compared and rendered; keys and video methods recomputed; Hebrew subtitles and course-wide duplicate
scan checked). No errors found, no changes made. `math_check.py 34 35 36 37 38 32` and full `math_check.py` → 0 / 0 / 0.
Judgment calls (left as is): g111 octagon → regular 9-sided polygon: same message (n > 6 ⇒ side < r ⇒ P < n·r),
same elimination method and level (40°/70° instead of 45°/67.5°); the video and figure match. p03 now has
"a polygon with 11 sides" choices instead of polygon names (same concept, sum → n). p04 4 octagons → 6 hexagons around
an opening (same counting idea, ratio 1/2).

## 2026-10-07 methods spread
- Checked every question for the 2026-10-06 methods: none is faster or new here (the plug-in questions already plug in). No change.


## 2026-10-07 no decimal estimates
Function `no_decimal_estimates` (runs last). Teacher: a student cannot estimate roots or π to one decimal place; estimates use whole-number benchmarks only (perfect squares, squaring, a factor into the root, 3 < π < 3.5). Videos with a recording are skipped by a build-time guard.
- solve-geo34-g111 "The hexagon is the balance": "2πr — about 6.28 radii" -> π < 3.5, so less than 7 radii (one line split into two).
- solve-geo34-g112 "Psychometric · Estimate": √3 ≈ 1.7 / 24 × 1.75 / 28 × 1.5 -> divide both sides, then a factor into the root: 24√3 ÷ 6 = 4√3 = √48 < 7; 24√2 is smaller still; 28√2 ÷ 14 = 2√2 = √8 < 3; 28√3: 2√3 = √12 > 3. Board by click, pen only for marks/cross-outs. 19 lines (was 19).
- Left: solve-geo34-g114 / geo34-g114 "1 + 1.4 against 2" (the taught √2 ≈ 1.4).
Check: `python3 math_check.py 34 32` -> 0 / 0 / 0. Rendered and looked at.
