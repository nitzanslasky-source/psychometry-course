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
