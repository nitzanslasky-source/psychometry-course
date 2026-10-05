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
