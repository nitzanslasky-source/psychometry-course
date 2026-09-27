# Topic 31 — Triangles: changes (course review 2026-09)

All answer keys were already correct. The main work: fix the lesson order, teach the rules the practice already uses, rewrite every written solution in TeX, and fix figures. Guided questions are renumbered automatically. There are now 26 (3 new).

## Order fix
- **"Equilateral Triangle Area" (geo-017-after) and old Q7 (geo31-g018, midpoints in an equilateral triangle) now come after the 30°-60°-90° lesson and its question.** Before, they came before Pythagoras. The video now finds the height from the golden triangle: the altitude cuts the triangle into two 30-60-90 halves, so h = (a/2)·√3. It no longer says "we'll learn Pythagoras in a moment". The Pythagoras calculation stays as a check slide.
  - Slides: "Two golden halves" (new script), "Check with Pythagoras" (was "Simplify"), "Area formula" (the "÷ 2 ÷ 2 = ÷ 4" note, no colons), "a-two-three-four" (plus a link to the 30-30-120 triangle, which has the same area).
  - 30-60-90 lesson, slide "Using 30°-30°-120°": now says "you'll see this formula again in the next lesson" (before, it said "look familiar?").
  - The equilateral rows moved from the "Triangle area" card to the "Special right triangles" card, which now comes after the video.
  - "Next lesson" / "last lesson" references fixed in the Q13 (old Q11) video and in the 45°-45°-90° lesson.

## New teaching (lesson slides)
**"Triangles" (geo-009)**
- New slide **"Angle bisector"** after "Altitude outside", with a new figure. It covers the third special line: two equal angles, no equal pieces, no right angle.
- **"Exterior angle"**: new clean figure (the extension of AC past C, γ inside and δ outside, no leftover parallel line). The exterior angle is now called δ, not γ, and the proof uses γ + δ = 180° and α + β + γ = 180°.
- **"Two routes"** and the Q3 video: the exterior angle is now a **core rule**. The lines "we don't use this rule a lot" and "optional" are gone.
- **"Between diff and sum"**: "big minus small" is said and shown on the board. New: whole-number count = 2 × shorter side − 1 (7 and 12 → 13).
- Recap and memory card updated (bisector row, core exterior angle, whole-number count row).

**"Special Triangles" (geo-013)**
- **"Isosceles triangle"** slide: plain figure (the symmetry line, right angle and base ticks now appear only on the next slide). The board shows (180° − 44°)/2 as a fraction. New: the converse, "base angles equal ⇔ legs equal", on the board, in the recap and on the card.
- **"Right triangle"** slide: plain figure (the median to the hypotenuse is on the next slide only).
- Median to the hypotenuse: "very rare" became "less common, comes back in circles" (T33 needs it).
- "Equilateral" board: 180° ÷ 3 (no colon).

**"Area of Triangles" (geo-016)**
- New slide **"Area two ways"** (6-8-10 with altitude h; leg × leg = hypotenuse × altitude, h = 4.8).
- New slide **"Largest possible area"** (sides 6 and 8 → area ≤ 24, equal only at 90°), with a new figure.
- Recap and card: two new rows. The card now has a named line: **"Same base, same height → same area (the vertex moves along a parallel line)"**. This line is also said in "A Median Halves the Area", slide 3.

**"The Pythagorean Theorem" (geo-019)**
- New slide **"Acute or obtuse?"**: c² = a² + b² → right, > → obtuse, < → acute (c is the longest side), with the example 5, 5, 8. There is a new row on the Pythagoras card.

**"Pythagorean Triples" (geo-024)**
- 8-15-17 is now "less common, but it appears" (the first Pythagoras question is 8-15-17), not "very, very rare". The slide, the sidebar and the card are updated.

## New guided questions (each with a solution video)
| New no. | id | Method | Answer |
|---|---|---|---|
| Q7 | q-r26-t31-01 | Area two ways: right triangle 15-20-25, altitude to the hypotenuse (traps 6 and 12.5) | 12 |
| Q8 | q-r26-t31-02 | Largest possible area: sides 6 and 8, which could be the area? (25, 48, 20, 28) | 20 |
| Q12 | q-r26-t31-03 | Acute/obtuse test: sides 6, 7, 10, which angle is obtuse? (trap: C) | obtuse at B |

## Changes to existing guided questions and videos
- **Q20 video (old Q17, "not necessarily isosceles")**: now ends with a sketch of a slanted median of 6 to a side of 4, so the answer is not only "the one we could not eliminate".
- Draw notes with ":" for division → "÷" (Q5, Q16, the 30-60-90 and 45-45-90 lessons). In Q13, the triple notes read "5-12-13 × 2". In Q24, the note says "area ratio 1 : 3".
- Stems: all given conditions are stacked with `\begin{cases}` (old Q3, Q4, Q5, Q8–Q10, Q12, Q13, Q20).
- **Every written solution** (guided and practice) was rewritten in TeX with the numbers shown. Specific fixes:
  - Q2: "p + q/2" is now a fraction.
  - Old Q7 and old Q12 now show the full calculation.
  - Q19 (old Q16) uses the new obtuse test (3.75, 3.75, 6).
  - adv-p20: 45° − t/2.
  - adv-p21: the triple 10-24-26 is shown first, then the algebra.
  - adv-p22: work back from the choices, then the conjugate.
  - adv-p17: "area two ways".
  - p22: the 2 × 9 − 1 shortcut.
  - Glitches fixed: "obtainh", "a6–8–10", "angle,90°", "Its square is".

## Figures
- fig v48 → new "exterior angle" figure (see above). New figures also for the angle bisector, area two ways, largest area, Q7 (new) and p20.
- v58, v62: plain versions (no next-slide content).
- **p11**: the "D" label moved to the right of the point, and "120°" moved further left (no more "12D").
- **adv-p10**: the equal ticks on CD and DB are longer and bolder.
- **g036 (Q22, old Q19)**: bigger angle arcs. The "30°" and "45°" labels now sit inside the angles, off the lines. This is fixed in the question and in its solution slide.
- **p20**: new figure (triangle, line ℓ ∥ BC, the extension of AC meets ℓ at E; angles p, q, r). The stem is shorter and refers to the figure.

## Practice (61 questions; was 54)
- **Removed:** foundation p26 (the third "median halves the area" question; p10 and adv-p08 remain).
- **Rewritten:**
  - adv-p01 no longer repeats Q20's "altitude = bisector" answer. The key is now "one median is also an altitude" (only isosceles). The distractor is "two medians are also altitudes" (equilateral). The "twice half" word puzzle is gone.
  - adv-p05, adv-p16: "reflex angle" is now defined in the stem (= 360° minus the interior angle).
  - Stems with several conditions are stacked (foundation p03, p06–p09, p12, p17; advanced p04, p07, p10, p12, p13, p17, p20); adv-p23's ratio is written in words.
- **New (8):**
  - Foundation: q-r26-t31-04 acute test (6, 7, 9) · -05 largest area of sides 10 and 7 (35) · -06 30-30-120 area with legs 10 (25√3).
  - Advanced (exam level): -07 angle B obtuse, AB = 8, BC = 15, so 17 < AC < 23 (20) · -08 sides 5, 8 and area 20, so angle A = 90° · -09 area 18 and AB = 4, so BC ≥ 9 (10) · -10 altitude to the other side in any triangle (8) · -11 whole-number third sides of 8 and 13 that make an obtuse triangle (10).
- **Order:** both sections now go easy → hard. The one-rule questions come first, then the multi-step ones, then the new exam-level items. adv-p22 (conjugate) is last.

## Not done / for the teacher
- Q20 (old Q17, median of 6 to a side of 4) is still solved mainly by elimination; the video now adds the sketch.
- The "triple from the perimeter" trick is taught only in the adv-p21 solution, not in a lesson slide.
- The small "24°" label in foundation p17 touches line AD; it was not listed in the review, so I left it.
- API workaround: the solution-video sidebars are set in the patch per question group (the solution videos between two lessons), so the automatic renumbering gives 1…16 and 17…26. Figure copies on solution slides are edited together with the question figure (set_q does not update them).

## Pass 2 (2026-09-27, teacher-approved remove/restore plan + summary lessons)

**Removed:** nothing (the plan keeps every T31 addition).

**Restored**
- `geo31-foundation-p26` (median halves the area, 19 → 38) is back in the foundation practice, right after p10. Solution now shows the numbers ($19+19=38$).
- `geo31-advanced-p01`: the original question "Which of the following triangles is not necessarily equilateral?" with its original four choices and key (choice 1: an altitude that also bisects its angle). Only clean-up: $60°$ in TeX, the 5, 5, 6 example in TeX.
- The Pass 1 version of that question ("one median is also an altitude", key 2) stays as a new extra item `q-r26-t31-12` in the advanced practice (placed a few items later, so the two are not back to back).
- `geo-019` slide 3: the original closing line "Let's see sample questions — first finding the hypotenuse, then finding a leg." is back. The added slide "Acute or obtuse?" that follows now opens with "But first — one more use of the squares…" and ends with "Now the sample questions: the hypotenuse, a leg — and then this test."

**Summary lessons (new)**
- `r26-t31-summary` (end of "Learn and try", right before the foundation practice, ~3.7 min): Three lines · Angles · Sides · Special triangles · Area · Pythagoras · Triples · Special right triangles · Before you practice.
- `r26-t31-summary-2` (end of "Further guided examples", right before the advanced practice, ~3.2 min): Letters in the answers · The longest side · Trap it: min and max · Not necessarily · Shaded areas · Same height · Faster ways · Before you practice.
