# Topic 36: Similarity and scale. Changes (course review 2026-09)

Patch: `math_patches/t36.py`. Checks: `python3 math_check.py 36` and `python3 math_check.py 35 36` both give 0 problems, 0 warnings and 0 layout problems.

## 1. Wrong or misleading teaching (priority 1)
- **Q3 video, slide 3:** removed "In a harder question, the common mistake usually won't even be in the choices". The slide now says: "A trap answer can be there at any level. Found the answer you expected? Read the question again."
- **Q6 video, slide 2:** "Parallel lines, equal acute angles" is now "Corresponding angles between parallel lines are equal".
- **Q6 video, slide 5:** the "work across ×1.25" step is gone. The slide now uses the part-to-part rule, which the lesson now teaches (see 2). The teacher's draw notes say "ratio 1 : 2".
- **Q5 video, slide 3:** the trap 256 is now explained correctly. It comes from squaring the area ratio.
- **"From the course —"** removed (Volume Changes, slide 6). The recap of "Similar Triangles and Rectangles" was also reworded: SSS and SAS are now "two more ways to prove similarity, rarely needed on the exam".
- **"Man with glasses" (Similarity, slide 12):** only one image is left. Kenny, Batman and binoculars are gone.
- "On the psychometric" (used as a noun) is now "On the exam". British "centimetres" is now "centimeters".

## 2. Methods added (priority 2)
Lesson **Similar Triangles and Rectangles** (geo-139), now 14 slides:
- **New slide "Part to part"** (after "Parallel to the base"): AD/DB = AE/EC is allowed, but DE is always compared with the WHOLE side. This resolves the clash between Q4 and Q6. Slide 7 now leads into it.
- **Altitude to the hypotenuse:** numbers 6, 8, 10 are added to the figure. The shortcuts h² = p·q and leg² = its part · hypotenuse are added, checked with 3.6, 6.4 and 4.8.
- **New slide "Same height":** the area ratio equals the base ratio, with no squaring. The contrast is 3 : 5, not 9 : 25.
- **New slide "Trapezoid diagonals":** the four triangles have areas a², ab, ab and b². Example: 4, 6, 6, 9.
- **Rectangle on the diagonal:** now a worked example with numbers (12 × 8, AP = 9, so AR = 6), including the leftover pieces (2/6 = 3/9).
- **Recap:** now includes the part-to-part rule and the same-height rule.

Lesson **Similarity in Regular Shapes**: a new line says which shapes are NOT always similar: rectangles, rhombuses, isosceles triangles and right triangles.

Lesson **Similar Solids**:
- "All spheres are similar" added (needed for Q12).
- **New slide "Half-height cone":** water up to half the height fills only 1/8 of the cone.

Lesson **Volume Changes**: **new slide "Percent change"**, following the steps percent → factor → power → back to percent (+10% gives +21% area and +33.1% volume; area +44% means sides +20%). The recap line was updated.

**New lesson video "Map Scale"** (r26-t36-map-scale, 6 slides, placed after Q13's video): scale 1 : n means lengths ×n and areas ×n². It covers the units ladder (cm ÷100 → m ÷1000 → km, and 1 km² = 10¹⁰ cm²), a length example and an area example (the trap is forgetting to square).

**New guided questions, each with a solution video:**
| id | where | method | key |
|---|---|---|---|
| q-r26-t36-01 | after Q4 | same height: BD : DC = 2 : 3, total 40, find ABD | 16 (choice 1) |
| q-r26-t36-02 | after it | trapezoid diagonals: bases 4 and 6, AOB = 8, find the trapezoid | 50 (choice 3) |
| q-r26-t36-03 | after "Volume Changes" | cube edge +20%, volume +?% (plus a check with edge 10) | 72.8% (choice 3) |
| q-r26-t36-04 | after "Map Scale" | 1 : 20,000, 7.5 cm, real distance in km | 1.5 (choice 2) |
| q-r26-t36-05 | after it | 1 : 40,000, 5 cm², real area in km² | 0.8 (choice 3) |

The Q4 solution group is renamed "Similar Triangles Questions" and now holds 3 questions.

**New memory card "Map scale"** (mem-r26-t36-map-scale). The existing cards were extended:
- mem-similar-triangles: a new "Shortcuts" table (part to part, same height, h² = p·q and leg², trapezoid a², ab, ab, b²) and a "plug in" tip.
- mem-similar-solids: rows for +10% (×1.21 and ×1.331) and the half-height cone (1/8), plus tips on spheres and percents.
- mem-similarity: a "not always similar" tip.

## 3. Text (priority 3)
- All 13 guided questions and all 25 remaining original practice questions were rewritten where needed:
  - The math is now in TeX.
  - Division is written without ":"; ":" now appears only for real ratios, and the text says "ratio".
  - Several givens are stacked with `\begin{cases}` (Q4, Q6, Q8, new Q6, p03, p09, p14, p19 and new items).
  - "right angle C" is now "the right angle at C".
  - "AC = AB : 3" is now $AC=\frac13AB$.
  - Every solution shows its numbers, uses the taught method, and names the trap choices.
- **p19 wording fixed:** "AC = 10 + 4 = 14, so AF is half of AC: AF = 7."
- p04 now says the inscribed-angle step comes from the circles topic.
- Q10 video board: "15:3" is now "15 ÷ 3". Pre-loaded stem copies on the slides were synced to the new stems.

## 4. Figures (priority 4)
- **Q5 (geo36-g142):** the 4×4×4 grid block gave away 64. It is now two separate plain cubes (small and large), on the question and on both solution slides.
- **v646 "Turn it around":** now really shows the big triangle turned upside down, with the same labels.
- **v648:** the numbers 6, 8 and 10 are added.
- **v656:** the radii are now drawn on the top faces, labeled 2 and 4, so they no longer look like widths.
- **v632:** alt text / title added.
- **Readability:** "1.4r" moved off the inner circle (Q9, question and 3 slides). "Small" moved off the dashed line (Q12, question and 2 slides). "3 units" moved off the dashed line (v631).
- **14 new figures** in the same style (colors, font and 640×360 viewBox): part to part, same height (×3), trapezoid diagonals (×3), half-height cone, partly filled glass, altitude triangle, parallel-line triangles (×3) and the two cubes.

## 5. Practice (priority 5)
- **Removed:** p10 (tangent circles, not similarity) and p15 (the heptagon; a near-duplicate of the p06/p21 area-ratio items).
- **Added 13 items (q-r26-t36-06 … -18):**
  - part to part (EC = 9)
  - segment against the whole side (BC = 10)
  - same height, twice (BD = 8; ADE : DBE = 1 : 2)
  - trapezoid diagonals, twice (BOC = 10; COD = 9/16)
  - leg² = part · hypotenuse (AB = 10)
  - cone glass filled to 2/3 of its height (64)
  - sphere radius −10%, so surface −19%
  - circle area +69%, so radius +30%
  - find the scale (1 : 300,000)
  - two maps (2 cm²)
  - field in m² (30,000)
- **Moved in by T35's patch:** geo35-core-p27 (box dimensions −25%, so 27/64 remain). It fits here and sits after the percent/volume items.
- **Result:** 39 practice items, ordered easy → hard. About 14 are exam-hard (trapezoid, altitude, glass, two maps, p03, p17, p18, p19, p24, p27 …).

## API workarounds
- Solution-slide question items carry their own copy of the figure (`item['fig']`). The patch edits those copies directly next to `M.set_q(figure=...)`.
- The "Pre-loaded — question …" canvas text is re-synced to the new stems inside the patch.

## For the teacher to decide
- The Map Scale lesson and its 2 questions sit at the end of "Learn and try" (after Q13). Move them earlier if you prefer.
- "The man with glasses" name is kept, and only the extra images are removed.
- p04 (inscribed angles) stays in the set. It depends on the circles topic, which comes before T36.
- The new videos need recording. Guided numbers are assigned automatically in course order: 1–4, then 5–6 for the new triangle questions, 8 for the cube-percent question, and 17–18 for map scale.

## Pass 2 (teacher-approved plan, 2026-09-27)
**Removed:** nothing.

**Restored:**
- `geo36-core-p10` (a disk in a semicircle → $\frac12$) and `geo36-core-p15` (regular heptagon, side 2 → 5 → $\frac{25a}{4}$) are back in the practice, with TeX and full numeric solutions. p15 is with the easy items (before p21), p10 in the middle (after p09).
- `geo-134` slide 12: the original lines ("this 'Batman' up here", "like Kenny from South Park, with a pair of binoculars"). There is only one figure on this slide in the base, and it stays (with the "3 units" label fix).
- `geo-143` slide 6: "From the course — what if both change? ..." is back.
- `solve-geo36-g138` slide 3: "A small tip about answers: usually they don't confuse me — they help me." is back. The false line about harder questions stays replaced.
- `geo-139` slide 12 "Recap": the original board line "Rectangles: both dimensions use one factor" is back (it was spoken but was missing from the board).
- `geo35-core-p27` (moved here by T35) stays in the practice.

**Summary lesson added:** `r26-t36-summary` "Summary: Similarity" (about 2.8 minutes), at the end of "Learn and try" (after the map-scale card), right before the practice.
Slides: Summary · Length, area, volume · Always similar? · Similar triangles · The exam pictures · Same height · Parts and leftovers · Similar solids · Percent change · Map scale · Before you practice.

## 2026-10-05 cut repeats
Function `cut_repeats` (runs last; the old `apply` is wrapped). A lesson slide is cut only where a question video after it teaches the same idea again. Nothing in topic 36 is recorded.
- **`geo-139` "Similar Triangles and Rectangles"**: 13.2 → 11.3 min (15 → 13 slides). Cut "Same height" (taught again in `solve-q-r26-t36-01`: not similar, same height, areas follow the bases, no squaring) and "Trapezoid diagonals" (taught again in `solve-q-r26-t36-02`: hourglass a², b², side triangles a·b, 4-6-6-9). Neither slide is in the Hebrew lesson. The recap item "Same height, not similar → area ratio = base ratio" and its line are removed; the last two recap items move up.
- **`geo-143` "Volume Changes"**: 5.6 → 4.8 min (9 → 8 slides). Cut "Percent change" (taught again in `solve-q-r26-t36-03`: percent → factor, cube it, back to percent, and "44 percent is the AREA: 1.2 squared"). Recap item "Percent: factor first, then the power" and its line removed. Kept: "Factor vs percent" (×4 = +300%, ×¾ = −25%; the question does not teach it).
  - Moved into `solve-q-r26-t36-03` slide 3 (the only part of the cut slide the question did not teach): "And backwards: the area grew by 44 percent? That's times 1.44. The square root is 1.2 — so the sides grew by 20 percent." with the board item "Backwards: area × 1.44 → sides × √1.44 = 1.2". 1.0 → 1.2 min.
- **`r26-t36-map-scale` "Map Scale"**: 2.5 → 0.7 min (6 → 2 slides). Cut "Units ladder", "Length example", "Area example" and the recap: `solve-q-r26-t36-04` teaches the length step and the ladder (÷100, ÷1000), `solve-q-r26-t36-05` teaches the area trick (one map cm into the real unit first, then square; the trap of forgetting to square). Kept: the intro and "Scale 1 : n" (what the scale means, lengths × n, areas × n²), which now ends "Let's see it in the questions."
- Sidebars updated. The summary `r26-t36-summary` is unchanged (same height, trapezoid diagonals, percent and map scale are all still taught in the question videos).
- Saved: about 4.3 min.

## 2026-10-06 renumber pass
So that the English course does not look like the Hebrew one, every question that came from the Hebrew course now has new
numbers, and the stories changed a little where there is one (a box and blocks, a glass globe, a sand scoop, new names).
The idea, the trap, the level and the methods stay the same: perimeter = a length, circles on a diameter, part vs. leftover,
the whole side, area → edge → volume, full math + part to part, full math + plugging in a special case, plugging in angles +
h² = p·q + Pythagoras, circles way + similarity way, three ways for the midpoint segment, polygons way + similarity way,
partial similarity. The function `renumber_pass(M)` runs last (after `cut_repeats`). Topic 36 has no `practice_methods`,
`add_methods` or `pen_or_click`. Nothing in topic 36 is recorded (checked ~/Documents/Course.recordings: only Algebra).

**Counts:** 13 guided questions renumbered and their 13 solution videos rewritten (speech, draw cues, board items, cue
labels, choice numbers). 20 practice questions renumbered. Figures redrawn: 9 guided (decagon, six circles, quarter circle,
DE ∥ BC 4/3, box and block, ED ∥ AB 10/15/4, altitude 3/27, rings 1.3r, globe and ball) + 1 relabeled (square in a
triangle, AF = 5); practice: 10 redrawn (p02, p07, p08, p09, p11, p14, p15 octagon, p16, p19) + 3 relabeled (p03, p04, p18).
Lesson examples that used the Hebrew lesson's own numbers: 7 changed (see below). **Practice 41 → 27.**

**Lesson examples changed** (the Hebrew lessons used these exact numbers):
- "Similarity", Not only sides: square diagonal ×2 → ×3. Square both parts: linear 2:3 → 4:9 became 4:5 → 16:25.
- "Similarity in Regular Shapes", hexagons: 3:5 → 9:25 (the Hebrew squares example) became 5:6 → 25:36.
- "Similar Triangles and Rectangles": the 6-8-10 / 9-12-15 triangles (Hebrew 3-4-5 / 6-8-10) became 12-16-20 / 18-24-30
  (same shape, the three figures relabeled; the table, "turn it around" and "ratios inside" slides follow; 4:5 = 8:10 →
  4:5 = 16:20). Altitude slide: 6-8-10 → 15-20-25, so BD = 9, AD = 12, DC = 16 (whole numbers now: 12² = 144 = 9·16,
  15² = 225 = 9·25). Figure relabeled.
- "Similar Solids", cubes: the 3 × 3 × 3 = 27 count (= the Hebrew volume lesson) became 4 × 4 × 4 = 64 with a redrawn
  figure. So that it does not repeat, "Volume Changes" slide 2 went from edge ×4 (64) to edge ×5 (125), title and sidebar
  "Cube edge × 5". "Radius only": "radius ×3 → volume ×9" (Hebrew) → "radius ×5 → volume ×25".
- Memory cards: "Similarity — lengths and areas" example column 2:3 → 4:5 (16:25), and the leftover tip 1:9 → 1:8 (the
  old guided numbers) → 1:25 → 1:24. "Similar triangles" tip "an easy number (x = 3)" (old guided plug-in) → "an easy number
  that makes a special case".
Kept: the cylinders 2/4 and 4/8 (Hebrew 2:3 and 4:6, only partly the same), the man with glasses and the 1:2 circles (the
picture forces 1:2), the 1-2 → 4-8 triangle grid, the soda-can idea for height only, and all English-made lessons and
summaries (part to part, same height, trapezoid, half-height cone, percent, map scale).

**Practice clean-up:** copies removed: q-r26-t36-06, -15, -18 (as listed). September items removed because the Hebrew
practice or a kept item already drills the type: -07 (segment against the whole side), -09 (same height; -08 stays), -11
(trapezoid; -10 stays), -13 (cone glass = Hebrew p16), -14 (percent and area = Hebrew p20). Kept September items (types the
Hebrew practice does not have): -08 same height, -10 trapezoid diagonals, -12 leg² shortcut, -16 find the map scale, -17
two maps. English extras: kept p26 (warm-up) and p22 (shadow); removed p21, p23, p24, p25, p27 and the box item
geo35-core-p27 (moved here by t35; removed only if it is in this section). Order easy → hard.

**Checks:** every answer recomputed in Python, and every video step (both ways in g144, the plug-in x = 5 in g145 —
only x²/5 gives 5 —, h² = 3·27 = 81 and the Pythagoras check 9 + 729 + 162 = 900 in g146, 1.69 − 1 = 0.69 < 1 in g147,
yh = 14 in g148, sides 10 and 2√5 in g149). Each trap is still a choice: the area factor (25), 2× (36π), the whole circle
(1:16), forgot to square (4:7), the part instead of the whole (4:3), 36² (1296), EC and BC (6, 25), the leg AB (3√10),
forgot to subtract (64:1, 64:27), forgot to square the radius (12), 2³ (8). No new number lands on a Hebrew number (subtitles
checked: pentagon ×3, radius 5 / 3 circles, 1:2, AD 2 DB 1, ×9 → 27, DC 6 BC 8 AE 3, AF 2, 4 / 9 → 6, 1.5r, trapezoid 6,
12√3 / 6√3, diameter = radius, r/5 h/3). Duplicate scan over topics 30–36: p06 first got 21 like g148's trapezoid, changed
to 19; no question equals a lesson or card example. `python3 math_check.py 36 32` and `35 36` → PROBLEMS 0, WARNINGS 0,
LAYOUT 0. All 13 solution videos, the 5 lesson videos and all changed figures were rendered and checked by eye.

| id | old (English base, Hebrew-derived) | new | answer |
|---|---|---|---|
| geo36-g136 | regular octagon, side ×4 | regular decagon, side ×5 (redrawn) | ×5 (2) |
| geo36-g137 | radius 7, four circles on AB | radius 9, six circles (redrawn) | 18π (4) |
| geo36-g138 | AC = ⅓AB → 1:8 | AC = ¼AB (redrawn) | 1:15 (2) |
| geo36-g140 | AD 3, DB 2 → ADE : trapezoid | AD 4, DB 3 (redrawn) | 16:33 (3) |
| geo36-g142 | face area ×16, small cubes | box and blocks, face area ×36 | 216 (2) |
| geo36-g144 | BD 4, DC 8, AE 5 → AC | BD 10, DC 15, AE 4 (redrawn) | 10 (3) |
| geo36-g145 | AF = 3 → x²/3, plug in 3 | AF = 5, plug in 5 | x²/5 (3) |
| geo36-g146 | BD 9, DC 16 → AD | BD 3, DC 27 (redrawn) | 9 (2) |
| geo36-g147 | r, 1.4r, Liam / Maya | r, 1.3r, Noah / Emma (redrawn) | Noah only (2) |
| geo36-g148 | midpoints, trapezoid 15 | trapezoid 21 | 7 (4) |
| geo36-g149 | hexagons 72√3, 24√3 | 150√3, 30√3 | √5:1 (1) |
| geo36-g150 | display, small diameter = ⅔R | glass globe and ball, small diameter = ½R (redrawn) | 63:1 (4) |
| geo36-g151 | tank and cup, r/3, h/4 | container and sand scoop, r/2, h/6 | 24 (3) |
| p01 | a:b = 2:3 → c:d | a:b = 3:5 | 3:5 (2) |
| p02 | 4 equal parts, CG:EF | 5 equal parts A–F, DH:FG (redrawn) | 3:5 (4) |
| p03 | AE 3, CF 5 → area | AE 4, CF 6 | 24 (3) |
| p04 | AE:DE 3:5, AB 6 | 2:3, AB 8 | 12 (2) |
| p05 | perimeters √5:1 | √7:1 | √7:1 (3) |
| p06 | DEF perimeter 18 | 19 | 38 (1) |
| p07 | OA = 4·OB | OA = 5·OB (redrawn) | 9/25 (1) |
| p08 | arcs ×1.5 | ×2.5 (redrawn) | 25:4 (2) |
| p09 | AB 3, CD 5, x−2, x+4 | AB 2, CD 3, x−1, x+3 (redrawn) | 9 (1) |
| p10 | semicircle radius 6 | radius 8 (answer the same by nature) | 1/2 (1) |
| p11 | areas 5, 20 | 7, 63 (redrawn) | 3:1 (3) |
| p12 | radius ×4, height halved | radius ×3, height ÷3 | 3:1 (4) |
| p13 | area ×9x | ×16x | 4√x (3) |
| p14 | AB 10, BC 12, CD 8 | AB 8, BC 15, CD 6 (redrawn) | 20 (2) |
| p15 | heptagon side 2 → 5 | octagon side 3 → 7 (redrawn) | 49a/9 (4) |
| p16 | small cone ⅔ height | ¾ height (redrawn) | 37:27 (2) |
| p17 | AB:BC 3:2 | 4:3 | 16/49 S (2) |
| p18 | AD 4 | AD 6 (relabeled) | r + r²/6 (3) |
| p19 | AJ 5, AB 10, BC 4 | AJ 4, AB 12, BC 6 (redrawn) | 288 (2) |
| p20 | square area +125% | +96% | +40% (2) |

## 2026-10-06 review
Independent review of the renumber pass (built with / without `renumber_pass`, compared every question, video, lesson,
card and figure; keys recomputed; Hebrew subtitles and course-wide duplicate scan checked). Fixed:
- solve-geo36-g145, slide 4 title still said "Psychometric · plug in x = 3" (the video now plugs in 5) → "x = 5"
  (`review_fixes`, runs last in `renumber_pass`).
- geo36-g142 figure: the block was drawn at 1/4 of the box edge, but the edge ratio is now 1 : 6 → block redrawn at
  165/6 = 27.5 (question figure and slide copies).
Judgment call left as is: g147 now uses 1.3r (ring 0.69 < 1); the old 1.4r was a deliberate close call (0.96 vs 1). Same
type and answer, a little less "close". `math_check.py 34 35 36 37 38 32` and full `math_check.py` → 0 / 0 / 0.
