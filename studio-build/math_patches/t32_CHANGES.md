# Topic 32 — Quadrilaterals: changes (course review 2026-09)

Patch: `math_patches/t32.py`. Check: `python3 math_check.py 32` gives 0 problems, 0 warnings and 0 layout problems.
Every answer key was re-solved, and every "Circle choice N" in a video matches its key.

## 1. Wrong rules fixed ("NOT" became "not necessarily")
- **Rectangle, slide 3:** the board and the teacher now say "not necessarily perpendicular / not necessarily angle bisectors". A square is a rectangle, and its diagonals ARE perpendicular.
- **Parallelogram, slide 5:** the diagonals are "not necessarily" equal or perpendicular. New line: "Equal diagonals? Then it is a rectangle. Perpendicular? Then it is a rhombus."
- **Rhombus, slide 3:** the diagonals are "not necessarily equal". If they are equal, it is a square.
- **Kite, slides 3–4:** the diagonals are "not necessarily equal". The secondary diagonal "doesn't necessarily" bisect its angles. "Head angles" became "the angles between the equal sides — A and C".
- **Trapezoid, slide 2:** the definition is now "exactly one pair of parallel sides". It used to be "the legs aren't parallel".
- **Q2 video, slide 5:** "you'll see it right away: not necessarily".
- **Q15 video:** a kite's shared base is "the secondary diagonal", not "the short diagonal".
- **Q10 video:** "four equal areas" is true "in every parallelogram", not only in the rectangle, rhombus and square.
- **Properties card:** all of the above, plus the trapezoid definition.

## 2. Methods added
| Method | Where it is taught | Guided question (solution video) | Practice |
|---|---|---|---|
| Family tree: which shape is also which | Quadrilaterals video, new slide "Who is also who?" (tree figure) | Q15 (existing) | adv-p11, fp14 (existing) |
| The arrow rule: the notch angle equals the sum of the other 3 angles | Quadrilaterals video, new slide "The arrow rule" | q-r26-t32-04 (after Q8) | q-11, q-19 |
| Length ×k → area ×k² | Square video, new slide "Scale it up" | — | fp25, q-12 |
| Parallelogram with a 30°/45°/60° angle | Parallelogram video, new slide "Special angles"; height drawn from A (it was from D, which fell outside BC) | q-r26-t32-01 (150° angle, height outside) | q-09, q-18 |
| Trapezoid midsegment; area = midsegment × h | Trapezoid video, new slide "The midsegment" | q-r26-t32-03 | q-10, q-16 |
| Isosceles trapezoid: opposite angles add up to 180° | Trapezoid video, isosceles slide (board and spoken) | — | fp02 |
| Right trapezoid: drop one height | Trapezoid video, right-trapezoid slide (new figure) | q-r26-t32-02 | q-08, q-20 |
| Trapezoid "butterfly": the two side triangles have equal areas | Equal Heights video, new slide 8 | q-r26-t32-05 (after Q18) | q-14, q-15 (hard: AOD·BOC = side²) |
| A cut counts twice; staircase = its rectangle; a notch adds 2 × depth | New lesson video `r26-t32-perimeter` "Perimeter Tricks" (after Q21) + new card "Perimeter tricks" | q-r26-t32-06 (staircase) | q-17 (notch), adv-p14/p15/p19/p24 |
| Perimeter + diagonal → area (identity), and working back from the answers | — | q-r26-t32-07 (identity, then "try the 5-12-13 triple") | adv-p21 |
| Work back from the answers | Q21 video, new slide "Check from the answers" (area 24x², try 150) | Q21 | — |
| A bisector in a parallelogram gives an isosceles triangle | Named in the Q9 video + on the card | Q9 | fp04 |
| Midpoint quadrilateral (rectangle → rhombus, square → square with half the area) | Properties card | — | q-13, q-21 |
| Area = d₁·d₂/2 for ANY quadrilateral with perpendicular diagonals | Area card (new row) | Q11 (already said) | adv-p27 |

The new guided questions get new numbers automatically. In course order they are: Parallelogram group Q5; Trapezoid group Q9 and Q10; Quadrilateral Questions Q12; Advanced II Q23; Perimeter Q27 and Q28. The sidebars of these groups were updated.

## 3. Text
- **All 91 questions:** every written solution was rewritten in TeX, with the numbers shown. Fractions use `\frac` instead of "divided by". There is a space after every comma: "2,6" was fixed in Q19, and so were Q16, Q6 "a60°", fp10, adv-p13, p14, p20, p21, p25 and p26. No "so" is used in the middle of a sentence.
- **Q20 solution:** it now reads $125°-\frac\alpha2-\frac\beta2$, and a check with numbers was added.
- **Givens stacked with `cases`:** Q2, Q4, Q6, Q9, Q11, Q13, Q14, Q17, Q18, adv-p03, p05, p07, p13, p14 and p17. adv-p08 now says "the ratio x:y:z".
- **Colon used for division:** fixed in the board item "(180°−120°):2" and in the notes "6 × 6 : 2" and "144 : 2". The notes for real ratios (Q17, Q18) now say "ratio".
- **Q10 video:** the simplest way (four equal areas) now comes first. The median way and base × height are marked "(optional)".
- **Q11 video:** "two equilateral triangles" now comes first. The diagonal ways are marked "(optional)".
- **Q19 video:** the "completions" slide was removed, because it ended with "it doesn't settle it". Now there are two approaches.
- **American spelling in T32 videos:** centimeter, memorize, practice, color.

## 4. Figures fixed
- **Quadrilaterals slides 2 and 4:** now a truly irregular quadrilateral. The old one was a parallelogram.
- **Concave slide:** the B label is moved off side AB.
- **Trapezoid slides 2–4:** now a non-isosceles trapezoid.
- **Right-trapezoid slide:** now a real right trapezoid. The old one was isosceles.
- **Q13 (g062 and its 4 slide copies):** the "12" is moved under BO.
- **Q18 (g069 and its copies):** "14 cm²" is moved inside the shaded triangle.
- **adv-p18:** "12" now sits on a dimension line over the whole of AD.
- **adv-p12:** the top α is moved to the vertical angle inside the rectangle, away from the label A.
- **adv-p20:** the 45° mark is the parallelogram angle, and it no longer touches a line.
- **adv-p06:** the 15° label is clear of the lines, and the C label is off BF.
- **adv-p02:** AE:ED is now drawn 12:7.
- **New figures:** family tree, arrow rule, scaling squares, parallelogram 30°, midsegment, butterfly, perimeter tricks, and the figures for all new questions.

## 5. Practice
- **Removed (5):**
  - fp05 and fp08 (trivial filler)
  - fp12 (pure T30 line angles)
  - fp19 and fp22 (repeats of "half-diagonals → triple")
- **Added 14:** 7 in Foundation, 7 in Advanced. Foundation: right trapezoid, parallelogram 30°, midsegment, arrow angle, +10%/+10% → 21%, midpoint square, butterfly. Advanced: hard butterfly (4 and 25 → 49), data sufficiency (midsegment + height), notch perimeter, parallelogram 60°, arrow with letters, right trapezoid 45°, midpoint rhombus.
- **Order:** both practice sets are now ordered easy → hard.
- **Totals:** Foundation 27 → 29, Advanced 27 → 34.

## For the teacher to decide
- fp06, fp15 and adv-p12 are really T30 angle-chasing questions. I kept them, because they use quadrilaterals. They could move to T30.
- fp25 (area ×k²) is now taught here, on the Square slide. T36 teaches it again for similar figures.
- T33 adv-p17 uses "the midpoint square has half the area". It is now on the T32 properties card and in practice item q-13.

## Pass 2 (2026-09-27, teacher-approved remove/restore plan + summary lessons)

**Removed (added items the plan drops)**
- Lesson slides: "The arrow rule" (geo-042), "The midsegment" (geo-054), "Trapezoid butterfly" (geo-067-after). Sidebars back to the original lists (geo-042 keeps "Who is also who?").
- Guided questions with their solution videos: `q-r26-t32-03` (midsegment), `-04` (arrow rule), `-05` (butterfly). Group sidebars fixed; guided questions renumber automatically.
- Practice: `q-r26-t32-10`, `-11`, `-14` (foundation), `-15`, `-16`, `-19` (advanced).
- Cards: `mem-quad-family` tip "Concave (arrow)…" and the Trapezoid diagonals cell (back to the original "—"); `mem-quad-area` Trapezoid "Remember" cell back to the original "sum of the bases × height ÷ 2"; `mem-equal-heights` row "Trapezoid with both diagonals…".

**Restored**
- Foundation practice `geo32-foundation-p05`, `-p08`, `-p12`, `-p19`, `-p22`, placed by difficulty. Clean-up only: solutions in TeX with the numbers shown, "therefore"; p19's givens stacked with `cases`.
- `solve-geo32-g070` (Q19): slide 3 "Approach 2 · Completions" is back; slide 4 is "Approach 3 · Split with symmetry" again, with its original opening line and the closing line "…by completions or by symmetry."
- `solve-geo32-g059`: original framing ("Learn all three", "it's important to know all of them") and original order (median, four equal areas, base × height). Kept clean-ups: the "Circle choice 3" note and "true in every parallelogram…".
- `solve-geo32-g060`: original framing and order (diagonals first, "get to know them all", the two-equilateral-triangles way as slide 6). Slide 6 keeps its fix: the original said "the angle opposite AD is 60 too" (that is the given angle); it now says "angle ADB is 60 too".

**Summary lessons (new)**
- `r26-t32-summary` (end of "Learn and try", before the foundation practice, ~3.6 min): The family · The diagonals · Angles · Area formulas · The height · Drop a height · Scale it up · In questions · Before you practice.
- `r26-t32-summary-2` (end of "Further guided examples", after the perimeter card, before the advanced practice, ~2.8 min): Not necessarily · Equal halves · Area ratios · Shaded areas · Letters and hidden ratios · Perimeter tricks · Perimeter and diagonal · Before you practice.

## 2026-10-05 cut repeats
Function `cut_repeats` (runs last). A lesson slide is cut only when the next question video teaches the same idea again. Nothing in topic 32 is recorded.
- **Perimeter Tricks** (`r26-t32-perimeter`) 1.4 → 0.9 min, 4 → 3 slides. CUT slide 3 "The staircase": the next question video `solve-q-r26-t32-06` teaches it in full (push the steps out, P = 2 × (width + height), no step length needed). Title slide now says "Two here — and one more in the question." The notch slide now opens "A notch: the border goes in, and comes back out." (it said "a notch is different" from the staircase) and ends "Now a question." Sidebar: "A cut counts twice", "A notch adds".
- KEPT: "A cut counts twice" and "A notch adds" (no question video teaches them). `geo-042` "Quadrilaterals" slide 6 (family tree) is longer than the Hebrew, but the only video that uses it (`solve-geo32-g066`) is far later, in the second section — kept. `geo-067-after` is not a repeat (g068 uses it, does not re-teach it).
- Summary `r26-t32-summary-2` slide 7 still sums up the staircase (taught in the question video) — no change needed.

## 2026-10-06 renumber pass
So the English course does not look like the Hebrew one: every Hebrew-derived question has new numbers (letter-only items: new letters / names and a new choice order). Idea, trap, level, number of steps and methods stay. Function `renumber_pass(M)` runs last (after `cut_repeats`; t32 has no `add_methods` / `practice_methods` / `pen_or_click`). Nothing in topic 32 is recorded.

**Counts:** 21 guided questions renumbered (20 with new numbers, g066 new choice order), all 21 solution videos rewritten (speech, draw cues, board items, the question-figure copies on the slides, choice numbers). 40 Hebrew practice questions renumbered. Lesson / card examples changed: 2 (summary-2 "1/3 of the base → 1/6" was the Hebrew lesson example → 1/5 → 1/10; the perimeter card tip 12 × 8 / 2(12 + 8) copied guided q-06 → 9 × 5). **Practice 62 → 48.**

**Figures:** relabeled where only the numbers change; redrawn where the shape depends on them: g068 (E, G at 3 : 1), g069 (AD : BC = 1 : 4), g070 (new 8 × 5 grid and pentagon), found. p09 (13 / 7 L-shape), p10 (7 × 5 grid), p16 (24 × 18 rectangle), p17 (ten rhombuses), p18 (3 × 4 array), p19 (kite 5 / 12 / 8), adv. p02 (AE : ED = 14 : 9), p08 (DE = 4EC), p17 (3a / 7a / EF 2a). g061 keeps its drawing with new vertex letters. All rendered and checked.

**Practice clean-up:** copies removed: q-r26-t32-18 (= q-09), adv-p21 (= guided q-07), found-p22 (rhombus from its diagonals = g051 / adv-p23). English extras: kept 4 (found-p23 isosceles trapezoid area, found-p24 only the base grows, adv-p22 octagon, adv-p27 any ⊥ diagonals); removed found-p25 (= the lesson example "diagonal +50% → 125%"), p21, p26, p27, adv-p23, p24, p25, p26. September: kept q-08, q-09, q-12, q-17 (types the Hebrew practice lacks); removed q-13 and q-21 (midpoint quadrilateral = Hebrew found-p16) and q-20 (trapezoid + special triangle: Hebrew adv-p03, and the same drop-a-height type as q-08). Order easy → hard.

**Kept on purpose:** the English-made guided q-r26-t32-01, 02, 06, 07 and the kept English practice items (not Hebrew-derived, no clash found). g061 and g066 are letter-only: same answers, new letters / order. adv-p03 keeps α = 120° (forced by the 30-60-90 idea). The lesson examples (12 → 72 square diagonal, 8 × 3 rectangle, 8 / 6 / 30° parallelogram, 10 and 6 rhombus) are not Hebrew numbers and no question equals them any more (g044 was 12 → 72 = the lesson; now 14 → 98). Guided order unchanged (already easy → hard inside each group).

**Checks:** every key recomputed in Python (one correct choice each, traps still among the choices); every video step recomputed (g059 three ways = 60, g060 five ways = 50√3, g062 three ways = 300, g071 plug-in 110 / 60 gives 90, 155, 40, 105 – only choice 3 = 40; g072 work-back: only 96 ÷ 24 is a square). New numbers checked against the Hebrew subtitles (none land on the Hebrew numbers: e.g. kite 4 → 10, trapezoid 30 / 3 / 3 → 65 / 5 / 10, plug-in 100 / 70 → 110 / 60, B = 90 → 130) and a duplicate scan over topics 1–32 questions and lesson lines (adv-p03 7 / 14 hit the special-triangles lesson "short leg 7, hypotenuse 14" → changed to 11 / 22). `python3 math_check.py 32` → PROBLEMS 0, WARNINGS 0, LAYOUT 0. Rendered g061, g068–g071, g048 videos and all question figures.

| id | old | new | answer (choice) |
|---|---|---|---|
| g044 | square diagonal 12 | diagonal 14 | 98 (2) |
| g046 | rectangle CD 3, ∠BEC 120° | CD 5 | 25√3 (3) |
| g048 | parts 3α+α, 3β+β | 3α+2α, 3β+2β | 72° (2) |
| g049 | AD 17, CD 13, EC 12 (5-12-13) | AD 24, CD 17, EC 16 (8-15-17) | 360 (3) |
| g051 | diagonals sum 34, diff 14 | sum 46, diff 14 (30, 16 → side 17) | 68 (2) |
| g053 | kite CB = CD = 6 | 10 | 20 + 10√2 (3) |
| g055 | trapezoid 54, DE 6, triangle 6 | 65, DE 5, triangle 10 | AD 9 (2) |
| g057 | A 112°, B 104° | 118°, 96° | 146° impossible (4) |
| g058 | AB 7, AE 3, 64°, 58° | 9, 4, 72°, 54° | 44 (3) |
| g059 | BC 12, perimeter 25 | BC 24, perimeter 50 (10-24-26) | 60 (2) |
| g060 | rhombus BD 6, 60° | BD 10 | 50√3 (2) |
| g061 | AOD equilateral, ∠OBC | BPC equilateral, ∠PAD | 15° (1) |
| g062 | kite 13 / BO 12 / OC 15 | 17 / 15 / 12 (8-15-17) | 300 (3) |
| g063 | AB = AD = 5, 30° | 7 | 35 (2) |
| g066 | statements | new order (false one still last) | parallelogram ⊥ diagonals (4) |
| g067 | corner areas 5, 13 | 6, 15 | 21 (2) |
| g068 | AE = 2ED, BG = 2GC | 3 : 1; choices reordered | area of ECD (1) |
| g069 | AD 4, BC 12, ABD 14 | AD 5, BC 20, ABD 15 | 75 (3) |
| g070 | 7 × 5 grid | 8 × 5 grid, new pentagon | 26 (3) |
| g071 | B 110°, plug 100 / 70 | B 130°, plug 110 / 60 | 65° − α/2 + β/2 (3) |
| g072 | perimeter 50 | perimeter 40 | 96 (3) |
| f-p01 | square 40, triangles 38 | 48, 34 | 88 (1) |
| f-p02 | y = x + 32° | y = x + 46° | 67° (2) |
| f-p03 | ∠ABC = 2t | 3k | 180° − 3k (3) |
| f-p04 | ∠BCD 124° | 136° | 22° (1) |
| f-p05 | triangle perimeter 216 | 252 | 21 (1) |
| f-p06 | α, β, γ | x, y, z; new order | 180° (2) |
| f-p07 | rhombus perimeter 36 | 44 | 23 impossible (4) |
| f-p08 | routes | new order | four sides (2) |
| f-p09 | L: 14 minus 9 | 13 minus 7 | 120 (2) |
| f-p10 | 30 squares | 35 squares | 27 (3) |
| f-p11 | — | new order | 90° (3) |
| f-p12 | 32° | 26° | 64° (3) |
| f-p13 | perimeter 11, side 4 | 17, 6 | 15 (2) |
| f-p14 | — | new order | rectangle (3) |
| f-p15 | 101°, 67° | 104°, 71° | 95° (2) |
| f-p16 | half-side 5, rhombus 13 | 9, 15 | 84 (4) |
| f-p17 | 12 rhombuses | 10 | 36° (2) |
| f-p18 | perimeter 40, 4 × 5 | 48, 3 × 4 | 14 (3) |
| f-p19 | kite 17 / 8 / 9 | 13 / 5 / 8 | 100 (2) |
| f-p20 | Leah (square) / Daniel (rhombus) | Maya (rhombus) / Ethan (square) | Ethan only (3) |
| a-p01 | short side 2 | 3 | 9 (2) |
| a-p02 | EBC 19, ECD 7 | 23, 9 | 14 (2) |
| a-p03 | AB 9, BC 18 | 13, 26 (review; was 11, 22) | 120° (2) |
| a-p04 | square 8 | 12 | 18√3 (1) |
| a-p05 | ∠DAC = 2t | 2m | 4m (1) |
| a-p06 | square 3 | 5 | 10√2 (3) |
| a-p07 | 3t, t | 3n, n | 180° − 2n (1) |
| a-p08 | DE = 3EC | 4EC | 4 : 1 : 5 (3) |
| a-p09 | square 7, small 1 | 14, small 2 | 88 (2) |
| a-p10 | rectangle perimeter 96 | 84 | 112 (2) |
| a-p11 | perimeter 40 | 52 | each side 13 (1) |
| a-p12 | 28° | 36° | 27° (1) |
| a-p13 | 2p, 2q | 2m, 2n | 90° + m + n (1) |
| a-p14 | perimeter 34, EF 7 | 46, 11 | 34 (3) |
| a-p15 | +10, CD 14 | +16, CD 13 | 52 (2) |
| a-p16 | AEC 30 = 3/10 | 42 = 7/24 | 5 (2) |
| a-p17 | 3a, 5a | 3a, 7a | 2a (2) |
| a-p18 | AD 12 | 15 | 5 (2) |
| a-p19 | p, q, r, s | a, b, c, d | 2b + 2c + 4d (2) |
| a-p20 | widths 6, 4√2 | 5, 3√2 | 30 (3) |

## 2026-10-06 review
Independent check of the renumber pass (build with and without `renumber_pass`, compare every question, video, card and
figure). Checked: 21 guided questions + their 21 solution videos, 40 renumbered practice questions, summary 2 and the
perimeter card, the 14 practice removals. Every key recomputed (one correct choice each, the old traps still among the
choices), every video step recomputed (incl. g059's three ways, g060's five ways, g062, g070's three approaches, g071's
plug-in 110 / 60 → 90, 155, 40, 105, g072's work-back), checked against the Hebrew subtitles (no Hebrew numbers), no
spoken "Question N", no leftover old numbers. All 53 changed question figures and all 21 videos rendered and checked.

Fixed:
- **adv. p03** — the new 11 / 22 is now the special-triangles lesson example (topic 31's renumber pass changed geo-026 to
  "Say it's 11 — the hypotenuse is 22"). Changed to AB = 13, BC = 26 (same 30-60-90 idea, answer 120°, choice 2); figure
  relabeled.
- **g048** — the figure was the old drawing relabeled (3α = 52.5°, 3β = 82.5°, so it showed x = 45°). Redrawn
  (`_rn_g048`) to the new split: 3α = 42°, 3β = 66°, x = 72°, labels 3α / 2α / 3β / 2β; the slide copies follow.

Judgment calls (left as is): g071's drawing keeps its B ≈ 110° shape labeled 130° (still obtuse, α still looks obtuse as
the video says); g055's middle rectangle (9 × 5) still looks like a square, which is exactly what the video warns about;
adv. p15's rectangle proportions are not to the new EF (not labeled); adv. p09 is the old figure doubled (14 / 2 instead
of 7 / 1), not a Hebrew number; f-p18 changed 4 × 5 → 3 × 4 so the small sides are now whole numbers (3, 4) instead of
2 and 2.5 — same steps.
`python3 math_check.py 32` → PROBLEMS 0, WARNINGS 0, LAYOUT 0.
