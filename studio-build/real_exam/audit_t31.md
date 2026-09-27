# Audit T31 – Triangles (report only, nothing edited)

Sources: `math_patches/t31_CHANGES.md`, `math_patches/t31.py`, `real_exam/quant_real.md` (regenerated), real exam figures
(all 24 triangles questions + related quadrilateral/similarity/circle figures viewed), pre-patch course `course18.json`.

Policy: same as audit_t30.md. A rule the ORIGINAL course questions need is kept (coordinator rule 2). A new question whose
type is not on the real exam but is already tested by original course questions is UNSURE; not on the real exam and not in
the original course is REMOVE.

Real triangles questions (24): 2020_autumn_q1_03, 2020_autumn_q2_20, 2021_autumn_q2_02, 2022_autumn_q1_03, 2022_autumn_q2_06,
2024_autumn_q1_17, 2024_autumn_q2_02, 2024_autumn_q2_07, 2025_autumn_q2_04, 2019_spring_q1_13, 2020_spring_q2_09,
2021_spring_q2_14, 2024_spring_q1_04, 2024_spring_q2_14, 2025_spring_q2_03, 2025_spring_q2_04, 2026_spring_q1_16,
2026_spring_q2_06, 2019_winter_q1_05, 2019_winter_q1_19, 2020_winter_q1_04, 2023_winter_q2_13, 2024_winter_q1_20,
2025_winter_q1_13. No real question anywhere in the 760 asks about the triangle inequality / possible third side, or tests
acute/obtuse from side lengths.

| Addition | Where (video id / slide / question ids) | Class | Verdict | Evidence (real question ids / count) |
|---|---|---|---|---|
| Order fix: "Equilateral Triangle Area" + old Q7 moved after the 30-60-90 lesson; height from two golden halves; "Check with Pythagoras" | geo-017-after (slides "Two golden halves", "Check with Pythagoras", "Area formula", "a-two-three-four"), geo31-g018, cards mem-special-right / mem-triangle-area | FIX | KEEP | 2024_autumn_q1_17 (equilateral area) |
| 30-30-120 link ("same area", "you'll see this formula again") | geo-026 slide "Using 30°-30°-120°", geo-017-after slide "a-two-three-four" | FIX | KEEP | wording/links only |
| Exterior angle made a core rule; new clean figure; δ naming | geo-009 slides "Exterior angle", "Two routes"; Q3 video; card | FIX | KEEP | 2026_spring_q2_06 (exterior β = 2α), 2024_spring_q2_14 (α > β by exterior angle) |
| "Big minus small" said on "Between diff and sum" | geo-009 slide "Between diff and sum" | FIX | KEEP | – |
| Whole-number third side: count = 2 × shorter − 1 | geo-009 slide "Between diff and sum" (board + spoken line); card mem-triangle-rules row "Whole-number third side"; geo31-foundation-p22 solution | METHOD | UNSURE | 0 real (no triangle-inequality question in 760). Helps only original geo31-foundation-p22 (which can also be solved by listing the range) |
| Angle bisector (third special line) | geo-009 new slide "Angle bisector"; sidebar; card row "Angle bisector" | CONTENT | KEEP (rule 2) | Original questions need it: geo31-advanced-p07, -p15, -p20, foundation-p08, -p13. Real triangle-bisector questions: 0 (bisector concept only in 2022_autumn_q2_02, circles) |
| Isosceles: converse "base angles equal ⇔ legs equal"; plain figures | geo-013 slides "Isosceles triangle" and next; recap; card mem-special-triangles row + tip | FIX | KEEP | Used by original solutions (e.g. solve-geo32-g058); real 2020_autumn_q1_03, 2024_autumn_q2_07 use isosceles angle/side links |
| Median to hypotenuse "less common, comes back in circles" | geo-013 | FIX | KEEP | 2020_autumn_q1_03 (AD = DC = DB) |
| "Equilateral" board 180° ÷ 3 | geo-013 | FIX | KEEP | – |
| Area two ways (leg×leg = hyp×altitude) | geo-016 new slide "Area two ways"; card mem-triangle-area row "Area two ways" | METHOD | KEEP (rule 2) | Needed by original geo31-advanced-p17. Real: 2020_autumn_q2_20 (altitude to the hypotenuse, same configuration) |
| Largest possible area: sides a, b → area ≤ ab/2 | geo-016 new slide "Largest possible area"; card row "Largest area" | CONTENT | KEEP | 2025_spring_q1_15 (parallelogram with sides x, y and 0°<α<90° → S < x·y; same principle, 1 real) |
| "Same base, same height → same area" named on card and in "A Median Halves the Area" slide 3 | card mem-triangle-area; geo-018-after | METHOD | KEEP | 2026_spring_q1_08, 2025_autumn_q1_13, 2023_winter_q2_13, 2025_autumn_q2_04 |
| Acute or obtuse? c² vs a²+b² | geo-019 new slide "Acute or obtuse?"; card mem-pythagoras row "Right, acute or obtuse?"; Q19 (old Q16) solution | METHOD | KEEP (rule 2) | 0 real. Needed by original geo31-g033 (obtuse at C, AB = 6 → perimeter), geo31-advanced-p18, old Q16 |
| 8-15-17 "less common, but it appears" | geo-024 slide 6, sidebar, card mem-triples | FIX | KEEP | wording; real triples: 2024_autumn_q2_02 (9-12-15) |
| Q20 (old Q17) video ends with a sketch | solve-geo31-g034 (Q20) | FIX | KEEP | – |
| ":" → "÷" in draw notes; stacked givens; all solutions rewritten; glitches; "Next lesson" references | many | FIX | KEEP | – |
| Triple-from-the-perimeter trick (solution only) | geo31-advanced-p21 solution | METHOD | KEEP | Triple recognition: 2024_autumn_q2_02, 2024_winter_q2_01 (3-4-5) |
| Work back from the choices, then the conjugate | geo31-advanced-p22 solution | METHOD | KEEP | Working back from answers: 2024_autumn_q1_17, 2025_spring_q2_04 |
| Figures: fig v48, v58, v62, p11, adv-p10, g036 (Q22), p20 (new figure, shorter stem) | geo-009, geo-013, geo31-foundation-p11, -p20, geo31-advanced-p10, geo31-g036 | FIX | KEEP | – |
| adv-p01 rewritten ("one median is also an altitude"), adv-p05/-p16 "reflex angle" defined, stacked stems | geo31-advanced-p01, -p05, -p16, others | FIX | KEEP (see restore section for adv-p01) | – |
| Guided Q7: right triangle 15-20-25, altitude to the hypotenuse = 12 | q-r26-t31-01 + video solve-q-r26-t31-01 | CONTENT (type) | KEEP | 2020_autumn_q2_20 (altitude to the hypotenuse of a right triangle) |
| Guided Q8: sides 6 and 8, which could be the area | q-r26-t31-02 + video solve-q-r26-t31-02 | CONTENT (type) | KEEP | 2025_spring_q1_15 |
| Guided Q12: sides 6, 7, 10, which angle is obtuse | q-r26-t31-03 + video solve-q-r26-t31-03 | CONTENT (type) | UNSURE | 0 real; type in original (g033, adv-p18) |
| Practice -04: which could be an acute triangle (6, 7, 9) | q-r26-t31-04 (foundation) | CONTENT (type) | UNSURE | 0 real; original type |
| Practice -05: largest area of sides 10 and 7 (35) | q-r26-t31-05 (foundation) | CONTENT (type) | KEEP | 2025_spring_q1_15 |
| Practice -06: 30-30-120 area, legs 10 (25√3) | q-r26-t31-06 (foundation) | CONTENT (type) | UNSURE | 0 real 30-30-120 area; type in original lesson geo-026 slide "Using 30°-30°-120°" |
| Practice -07: angle B obtuse, AB = 8, BC = 15 → 17 < AC < 23 | q-r26-t31-07 (advanced) | CONTENT (type) | UNSURE | 0 real; original type (g033, adv-p18) |
| Practice -08: sides 5, 8 and area 20 → angle A = 90° | q-r26-t31-08 (advanced) | CONTENT (type) | KEEP | 2025_spring_q1_15 |
| Practice -09: area 18, AB = 4 → BC ≥ 9 | q-r26-t31-09 (advanced) | CONTENT (type) | KEEP | 2025_spring_q1_15 |
| Practice -10: altitude to the other side in any triangle (area two ways) | q-r26-t31-10 (advanced) | CONTENT (type) | UNSURE | 0 real (no real question finds a second altitude from the area); original type (adv-p17, foundation-p23) |
| Practice -11: whole-number third sides of 8 and 13 that make an obtuse triangle | q-r26-t31-11 (advanced) | CONTENT (type) | UNSURE | 0 real (neither the count nor the obtuse test); both parts are original types (p22, g033) |

Counts: KEEP 24 (of which 12 FIX), REMOVE 0, UNSURE 7.

## TO REMOVE
- Nothing is a clear REMOVE. The 7 UNSURE items all follow one question for the teacher: "extra fixer questions of a type
  the original course already tests, but which never appears on the real exam – keep or remove?" If the answer is remove:
  - Questions q-r26-t31-03 (+ video solve-q-r26-t31-03, guided Q12), q-r26-t31-04, q-r26-t31-06, q-r26-t31-07, q-r26-t31-10, q-r26-t31-11.
  - geo-009 slide "Between diff and sum": the board item "Whole-number lengths: 2 × shorter side − 1" and its spoken line
    "Quick count: twice the shorter side, minus 1..."; card mem-triangle-rules row "Whole-number third side"; the
    "2 × 9 − 1" shortcut in the geo31-foundation-p22 solution.

## ORIGINAL ITEMS REMOVED BY FIXERS (to restore)
- geo31-foundation-p26 (unplaced): "A median divides a triangle into two smaller triangles. One of them has area 19 cm². What is the area of the original triangle?"
- geo31-advanced-p01: original question "Which of the following triangles is not necessarily equilateral?" was rewritten to a different question (key "one median is also an altitude", only isosceles). The original stem/choices/key are replaced.
- geo-009 slide "Two routes" and the Q3 video: the original lines "we don't use this rule a lot" / "optional" about the exterior angle were deleted (the real exam does use it: 2026_spring_q2_06, 2024_spring_q2_14 – so the deletion is justified, listed only for completeness).
- geo-017-after (Equilateral Triangle Area): original script "we'll learn Pythagoras in a moment" and the Pythagoras-first derivation replaced (Pythagoras kept as a check slide); video moved after the 30-60-90 lesson.
- geo-024 (Pythagorean Triples): the line "But don't bother yourself with it." (about 8-15-17) was deleted; "very, very rare" replaced.
- geo-019: the spoken line "Let's see sample questions" (slide 3) was deleted.
- geo-013: figures on "Isosceles triangle" and "Right triangle" slides lost their symmetry line / median (moved to the next slide only).
- geo31-foundation-p20: stem shortened and a new figure replaces the original (text-only) version.
