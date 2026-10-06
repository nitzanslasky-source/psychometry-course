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

## 2026-10-05 cut repeats
Function `cut_repeats` (runs last). Nothing in topic 31 is recorded. Rule: a lesson slide is cut only if a question video after it teaches the same idea again.
- **`geo-016` "Area of Triangles"** 6.0 → 4.1 min. These two slides are not in the Hebrew lesson. Both are cut:
  - "Area two ways" (legs 6, 8, hypotenuse 10, h = 4.8). Taught again in full by `solve-q-r26-t31-01`: the area two ways, and the short rule "leg × leg = hypotenuse × altitude".
  - "Largest possible area" (sides 6 and 8, at most 24). Taught again in full by `solve-q-r26-t31-02`: the height is at most 6, the area is at most 24, and "two sides and no angle: up to half their product".
  - The recap loses the two matching board items. Sidebar: "Area two ways" and "Largest possible area" removed.
- **`geo-019` "The Pythagorean Theorem"** 2.3 → 1.5 min (the Hebrew lesson is 1.2). Slide "Acute or obtuse?" is cut; `solve-q-r26-t31-03` teaches the test. That video only showed the obtuse case, so ONE line + board item moved there (slide 2, right after "So we use the squares."): board "Longest side c: c² = a² + b² → right / c² > a² + b² → obtuse / c² < a² + b² → acute"; spoken "The rule: square the longest side. Compare it with the other two squares, added." "Equal — a right angle. Bigger — obtuse. Smaller — acute." That video goes from 1.0 to 1.2 min. Sidebar: "Acute or obtuse?" removed.
- **Teacher's rule (a question must never be a lesson example):** `geo-009` slide 13 "Between diff and sum" used 7 and 12, the numbers of the next question g012. The lesson example now uses 5 and 9: "For 5 and 9 it's 9 minus 5 — not 5 minus 9." "More than 4 and less than 14." "5, 6, and so on up to 13. That's 9 lengths." "Twice 5 is 10, minus 1 — 9." The teacher writes "2 × 5 − 1 = 9". Same message; this slide has no figure. g012 is unchanged.
- Kept: `geo-026` (30-60-90). Its extra slides 9–10 (the 30-30-120 triangle) are not taught again by any question video. Q `geo31-g027` uses only the 30-60-90 ratio. In topic 32, three solution videos use the 30-30-120 triangle as an extra link and do not teach it again: `solve-geo32-g046` (one line), `solve-geo32-g060` slide 6 and `solve-geo32-g063` slide 4 ("Bonus · 30°-30°-120°"). It also appears in `geo-017-after` slide 5 and the summary. **For the teacher to decide**; nothing changed.
- AI summaries: `r26-t31-summary` (Area: "count the area twice", 30/40/50; and the special triangles) still matches. Everything it sums up is still taught before it, now in the question videos.


## 2026-10-06 renumber pass
So the English course does not look like the Hebrew one, every Hebrew-derived question has new numbers (or new letters,
where it only has letters). The idea, condition, trap, level and methods stay the same, and only numbers, letters and
choice order changed. Function `renumber_pass(M)` runs last, after `cut_repeats`. Nothing in topic 31 is recorded
(checked ~/Documents/Course.recordings), so `RN_RECORDED` is empty. Every guided solution video was rewritten to match:
speech, draw cues, board items and choice numbers. Every figure with a changed number was redrawn to scale or relabelled.

**Counts:**
- **Guided:** 23 renumbered (g010 to g040), with their 23 solution videos rewritten.
- **Practice:** 40 Hebrew practice questions renumbered (foundation p01 to p20, advanced p01 to p20).
- **Lesson, summary and card examples:** 9 changed (listed below).
- **Practice clean-up: 63 → 48.**

**Practice clean-up (approved):**
- **Copies removed:** q-r26-t31-12 (same stem as advanced-p01) and foundation-p26 (same idea as foundation-p10, "a median halves the area").
- **English extra warm-ups:** kept 3: foundation-p22 (whole-number third side), advanced-p23 (area ratio with a midpoint) and advanced-p27 (two triangles on one base). Removed foundation-p21, p23, p24, p25, p27 and advanced-p21, p22, p24, p25, p26.
- **September items removed** because the Hebrew practice already has their type: q-06 (30-30-120 / equilateral area; Hebrew foundation-p11, advanced-p11, p12), q-07 (side opposite an obtuse angle; Hebrew advanced-p18) and q-10 (area two ways for an altitude; Hebrew advanced-p17, p04).
- **September items kept**, because the Hebrew practice does not have their type: q-04 (acute test), q-05, q-08, q-09 (largest possible area) and q-11 (obtuse count).
- **Order:** unchanged (it already goes easy → hard).

**Lesson, summary and card examples changed:**
- **Hebrew numbers:**
  - "Triangles" slide "Between diff and sum": 5 and 9 (the Hebrew guided question) → 4 and 9. The card row now reads "sides 4 and 9: 2·4−1 = 7 lengths".
  - 30-60-90 lesson: "3 → hypotenuse 6" and "5 → 5√3" (Hebrew) → 11 → 22 and 10 → 10√3. Its "long leg 2 → 2/√3, 4/√3" (the Hebrew's 1 → 1/√3, 2/√3) → long leg 5 → 5/√3, 10/√3.
  - Summary "Triples": the multiples 6:8:10 and 9:12:15 (Hebrew) → 27:36:45 · 25:60:65 · 24:45:51.
  - g028 closing line: "5, 5√2, 10" (Hebrew) → "6, 6√2, 12".
- **Collisions with a question:**
  - Triples lesson, "Match the positions": 15, 20 → 25 (guided q-01's sides) → 27, 36 → 45.
  - Triples lesson: "Our first Pythagoras question was exactly 8, 15, 17" → "You'll meet it, doubled, in the next question" (g025 now uses 8-15-17 × 2).
  - Area lesson, "Any side as base": side 8, height 5, area 20 (practice q-08's numbers) → side 9, height 6, area 27.
  - Summary "Area": legs 30, 40, hypotenuse 50 (now part of g025) → legs 36, 48, hypotenuse 60, altitude 28.8.
  - Card tips: 14/√2 = 7√2 → 22/√2 = 11√2, and √65 → √53.

**Kept on purpose:**
- The English-made guided q-r26-t31-01 to 03 and the kept September practice items are not Hebrew-derived, so they are unchanged.
- Structural angles stay where the method needs them: 30° and 60° in the equilateral items, 120° in foundation-p11, 45° and 30° in the special right triangles.
- Letter-only questions changed letters and choice order only: g011, g031, foundation-p14, p16, p20 and advanced p01, p05, p07, p14, p15, p16, p20.
- The mnemonics (hamsa / bat mitzvah / bar mitzvah, 8·2 = 16 ± 1, a-two-three-four) are the teacher's methods and were kept.
- Summary-2 examples (p = 120 → 50, AB = 8 → 16 < P < 24, DC = 4BD area 45 → 9 and 36) do not equal any new question. advanced-p08 was moved from 9/36 to 11/44 for that reason.

**Checks:**
- **Answers:** every new answer and every video step was recomputed in Python. Every choice set has exactly one correct value, and the trap answers are still among the choices (sum/difference, a forgotten root, a forgotten ÷2, the hypotenuse used as a height, the median instead of the altitude, the angle at A instead of x, and others).
- **Triples:** no question keeps its old triple. Triples are not repeated across questions: 16-30-34 only in g025, 24-32-40 only in foundation-p06, 18-24-30 only in advanced-p13, 33-44-55 only in advanced-p17, 10-24-26 only in advanced-p10, 5-12-13 only in advanced-p04, 8-15-17 only in foundation-p09, and 12-16-20 / 20-48-52 only in g035.
- **Hebrew subtitles:** every new number was checked against 03-Geometry-Original-Subtitles.txt (triangles section). No guided question lands on a Hebrew number set.
- **Duplicate scan (topics 30–31):** no question has the same number set as another question, and none equals a lesson, summary or card example.
- **Check run:** `python3 math_check.py 31 32` gives PROBLEMS 0, WARNINGS 0, LAYOUT 0.
- **Rendering:** all changed solution videos, the lessons geo-024 and geo-026, and every changed figure were rendered and looked at.
- **Spoken lines:** no spoken line says "Question N".

| id | old (English base) | new | answer (choice) |
|---|---|---|---|
| geo31-g010 | vertical angle 2x at A, 3x, 4x → x = 20° | 3x (vertical at A), 4x, 5x → 12x = 180°; figure redrawn (45°, 60°, 75°) | 15° (2) |
| geo31-g011 | letters u, p, q; p + q/2 | letters k, m, n; m + n/2 | 180° (3) |
| geo31-g012 | AC = 7, BC = 12 → 5 < AB < 19 | AC = 6, BC = 13 → 7 < AB < 19; figure redrawn | 11 (3) |
| geo31-g014 | equilateral, ∠DAC = 30°, DC = 6 | DC = 7 | 14 (2) |
| geo31-g015 | AB = AC, vertex 24°, BC = CD → 78, 24, 54 | vertex 28° → 76, 28, 48; figure redrawn | 48° (3) |
| geo31-g017 | DE = 4CD → ratio 4 | DE = 5CD → 5 (six equal small triangles); figure redrawn | 5 (1) |
| geo31-g020 | legs 8, 15 → 17 | legs 20, 21 → 29 (√841); figure redrawn | 29 (2) |
| geo31-g021 | legs 4, 7 → √65 | legs 5, 7 → √74; figure redrawn | √74 (1) |
| geo31-g022 | leg 8, hypotenuse 11 → √57 | leg 7, hypotenuse 10 → √51; figure redrawn | √51 (4) |
| geo31-g025 | 10, 26 → 24 (5-12-13 ×2); 18, 24 → 30 (3-4-5 ×6); 30√2 | 16, 34 → 30 (8-15-17 ×2); 30, 40 → 50 (3-4-5 ×10); 50√2; figure redrawn | 50√2 (3) |
| geo31-g027 | 30° at C, AB = 6 → 18 + 6√3 | AB = 5 → 15 + 5√3 | 15 + 5√3 (1) |
| geo31-g018 | equilateral, perimeter 18, midpoints → 27√3/4 | perimeter 30 (side 10, halves 5) → 100√3/4 − 25√3/4 | 75√3/4 (2) |
| geo31-g028 | 45°, hypotenuse 14 → 14 + 14√2 | hypotenuse 18 → 18 + 18√2 | 18 + 18√2 (1) |
| geo31-g031 | letters p, q; choices p−60, 150−p, 180−p, 2p−120; plug-in p = 100 → q = 40 (= Hebrew) | letters x, y; choices 180−x, x−60, 2x−140, 140−x; plug-in x = 110 → y = 50 (choices give 70, 50, 80, 30) | x − 60° (2) |
| geo31-g032 | ∠B = 40°, α + β = 140, α > 70; choices AB / cannot / BC / AC | ∠B = 50° (Hebrew 60), α + β = 130, α > 65; choices AB / AC / BC / cannot; figure redrawn (82°, 50°, 48°) | BC (3) |
| geo31-g033 | obtuse at C, AB = 6: 12 < P < 18; choices 22.5, 13.5, 12, 18 | AB = 10 (Hebrew 2): 20 < P < 30; choices 30, 20, 24, 35; example 7, 7, 10 (changed in review) | 24 (3) |
| geo31-g034 | angles 76° and 52°; median 6 to a side of 4 | angles 64° and 58° (Hebrew 70/55); median 7 to a side of 10; choice order changed | the median one (3) |
| geo31-g035 | legs 6, 8 (3-4-5 ×2) → AC 10; hyp 26 (5-12-13 ×2) → CD 24; area 144 | legs 12, 16 (3-4-5 ×4) → AC 20; hyp 52 (5-12-13 ×4) → CD 48; area 96 + 480 = 576; trap 616 (52 used as a height) | 576 (3) |
| geo31-g036 | AD = 12 → BD 6, AB 6√3, BC = CD = 3√2; P = 12 + 6√3 + 6√2 | AD = 20 (Hebrew 8) → BD 10, AB 10√3, BC = CD = 5√2; P = 20 + 10√3 + 10√2 | (4) |
| geo31-g037 | BE = 3, AD = 2√3 → DE 3√3; 15√3 − 9√3 = 6√3 | BE = 4, AD = 3√3 (Hebrew 2, √3) → DE 4√3, AE 7√3; 28√3 − 16√3 = 12√3; flash way 2 · (3√3 · 4 / 2); figure: A raised so AD : DE = 3 : 4 | 12√3 (2) |
| geo31-g038 | area 32, DC = 3BD → 8, 24, difference 16 | area 56, DC = 3BD (Hebrew 18, DC = 2BD) → 14, 42, difference 28 | 28 (3) |
| geo31-g039 | squares of side 3: 6√2 − 6; AF = 3√5 | squares of side 5 (Hebrew 1): 10√2 − 10; AF = √125 = 5√5; estimate 8.5 − 5, 10 − 14 | 10√2 − 10 (4) |
| geo31-g040 | bold = twice the small perimeter: 3b − a = 6a → 3/7; plug a = 3, b = 7 | bold = three times the small perimeter (Hebrew: once, 3/4): 3b − a = 9a → 3/10; plug a = 3, b = 10; trap 1/3 (forgets − a); figure redrawn (a/b = 0.3) | 3/10 (3) |
| geo31-foundation-p01 | isosceles AC = BC, exterior 146° at A → x = 112° | exterior 142° → base angles 38° | 104° (3) |
| geo31-foundation-p02 | sides 8, 10, 13 → β < α < γ | AB = 11, AC = 9, BC = 7 → α < β < γ | α < β < γ (3) |
| geo31-foundation-p03 | equilateral ADC, ∠BAD = 30°, BD = 7 | BD = 9 | DC = 9 (2) |
| geo31-foundation-p04 | sides 11 and 8, which cannot be third (3) | sides 14 and 5 | 9 (4) |
| geo31-foundation-p05 | parallel lines, AB = BC, ∠B = 42° → y = 69° | ∠B = 46° | 67° (3) |
| geo31-foundation-p06 | right at B, AC = 25, BC = 20 (3-4-5 × 5), area 150 | AC = 40, BC = 32 (3-4-5 × 8) | 384 (2) |
| geo31-foundation-p07 | ∠A = 35°, ∠B = 85°, AB = 12 → AC > 12 | ∠A = 40°, ∠B = 75°, AB = 14 (∠C = 65°; trap ∠C = 55°) | AC > 14 (4) |
| geo31-foundation-p08 | AC = BC = 10, ∠A = 60°, bisector CD → DB = 5 | AC = BC = 16 | 8 (3) |
| geo31-foundation-p09 | AD ⊥ BC, AB = 13, BD = 5, AC = √313 (5-12-13) → DC = 13 | AB = 17, BD = 8, AC = √421 (8-15-17) | 14 (1) |
| geo31-foundation-p10 | median, area 30 → 15 | area 42 | 21 (2) |
| geo31-foundation-p11 | DE ∥ AC, two 120° angles, BD = 6 → 9√3 | BD = 10 | 25√3 (4) |
| geo31-foundation-p12 | AB = 26, AC = 19 → BC > 7 | AB = 31, AC = 17 | BC > 14 (1) |
| geo31-foundation-p13 | right at B, bisector AC, ∠ADB = 52° → β = 71° | ∠ADB = 56° | 73° (3) |
| geo31-foundation-p14 | acute angle 2α → exterior 90° + 2α | acute angle 3θ | 90° + 3θ (3) |
| geo31-foundation-p15 | other acute angle split into 5 equal angles x → 15° | split into 4 equal angles t (traps 22.5°, 36°) | 18° (3) |
| geo31-foundation-p16 | triangle PQR, exterior u > v at P, Q → QR < PR | triangle KLM, exterior s > t at K, L | LM < KM (4) |
| geo31-foundation-p17 | AB = AC, AD ⊥ BC, AE = EC, ∠BAD = 24° → x = 48° | ∠BAD = 22° | 44° (3) |
| geo31-foundation-p18 | vertical angles at O, 48° and 76° → β = α − 28° | 52° and 71° | α − 19° (2) |
| geo31-foundation-p19 | parallel verticals, 136° and 24° → α = 112° | 128° and 31° | 97° (2) |
| geo31-foundation-p20 | letters p, q, r; point E → r = 180° − q + p | letters x, y, z; point D (number check 65°, 125°) | 180° − y + x (4) |
| geo31-advanced-p01 | not necessarily equilateral: altitude that bisects its angle (1st); example 5, 5, 6 | same 4 kinds reworded/reordered: "one angle bisector is also an altitude"; example 7, 7, 4 | bisector = altitude (2) |
| geo31-advanced-p02 | right isosceles AB = BC = 4 + equilateral ACD | AB = BC = 6 (figure label 6) | 12 + 12√2 (2) |
| geo31-advanced-p03 | equal side = 4 × base, perimeter : leg | equal side = 5 × base | 11/5 (2) |
| geo31-advanced-p04 | AB = 9, BC = 12 (3-4-5 × 3), equal areas | AB = 5, BC = 12 (5-12-13), AC = 13, area 30; figure redrawn to scale | 60/13 (1) |
| geo31-advanced-p05 | average of the three reflex angles | same (no numbers), reworded, choices 240/270/300/330 | 300° (3) |
| geo31-advanced-p06 | shortest 2, longest 7 | shortest 3, longest 9 (6 < x < 9) | 7.5 (2) |
| geo31-advanced-p07 | ABC, AB = AC, BD bisects B, AD = DB | triangle KLM, KL = KM, LN bisects L, KN = NL; figure relabelled, ticks now on KN and NL (old ticks wrongly suggested AD = AB) | 72° (2) |
| geo31-advanced-p08 | BD = ¾ BC, ADC = 14 | BD = ⅘ BC, ADC = 11 (D moved to 4/5 in the figure) | 44 (2) |
| geo31-advanced-p09 | B = 35°, A > 45°, cannot be 75° | B = 25°, A > 60°, cannot be 80° (others 95/110/130) | 80° (2) |
| geo31-advanced-p10 | right at C, AC = 12, BC = 16 (3-4-5 × 4), D midpoint | AC = 10, BC = 24 (5-12-13 × 2), DC = DB = 12; figure redrawn | equal areas, ADC smaller perimeter (3) |
| geo31-advanced-p11 | angles 2x, 4x, 6x; sides 5, 5√3, 10 | angles 3x, 6x, 9x; sides 9, 9√3, 18 (trap 9, 12, 15) | 9, 9√3, 18 (4) |
| geo31-advanced-p12 | BC = 2, CE = 2√3, AD = 4√3 → AB = 16 | BC = 3, CE = 3√3, AD = 5√3 → EB = 6, AE = 15; figure redrawn to scale | 21 (2) |
| geo31-advanced-p13 | AB = 13, BD = 12 (5-12-13), AC = √61 → 18 | AB = 30, BD = 24 (3-4-5 × 6), AC = √373 → AD = 18, DC = 7; figure redrawn | 31 (2) |
| geo31-advanced-p14 | necessarily true for every isosceles; example 5, 5, 8 | same, choices reordered; example 4, 4, 7 (49 > 32) | altitude to base < leg (2) |
| geo31-advanced-p15 | A, C, B; CE, CF bisectors; angle CEF = 2t | K, M, L; MP, MR bisectors; angle MPR = 2k; figure relabelled | 90° − 2k (3) |
| geo31-advanced-p16 | reflex angle at 3rd vertex split in 3: δ = 60° + (α+β)/3 | split in 4, angles β, γ, θ: θ = 45° + (β+γ)/4 (+ plug-in check) | 45° + (β+γ)/4 (3) |
| geo31-advanced-p17 | right at A, AB = 8, AC = 15 (8-15-17) → 120/17 | AB = 33, AC = 44 (3-4-5 × 11), BC = 55; figure redrawn | 132/5 (4) |
| geo31-advanced-p18 | side opposite obtuse angle 8 → sum 10 | 11 → sum 15 (example 7, 8, 11: 121 > 113) | 15 (4) |
| geo31-advanced-p19 | 2p+q+42°, p+2q+66° → 84° | 2p+q+46°, p+2q+50° → p = 46°, q = 42° | 88° (3) |
| geo31-advanced-p20 | A, B, C, D, angle 2t | P, Q, R, S, angle 2k; figure relabelled | 45° − k/2 (1) |

## 2026-10-06 review
Independent check of the renumber pass (built with and without `renumber_pass`, compared every question, video, lesson and card).
Checked: 23 guided questions and their videos, 40 renumbered practice questions, 9 lesson/summary/card examples, practice
removals (63 → 48), all 44 changed figures and all 23 solution-video boards rendered and looked at. Every key recomputed: one
correct choice each, traps still present, triangle inequality / triples / special-triangle ratios valid. Nothing recorded.
No "Question N" in speech. Duplicate scan (topics 1–33): no question equals another question or a lesson/card example.

Fixed:
- **g015 video:** a spoken line still said "only PART of that angle can't be 78 too" (old number) → 76.
- **g033:** the choice set 20 / 22.5 / 30 / 37.5 with AB = 10 was the Hebrew's set (4 / 4.5 / 6 / 7.5 with AB = 2) times 5,
  answer 22.5 = 4.5 × 5. New choices 30 / 20 / 24 / 35 (answer 24, still choice 3; 20 and 30 are still the "equal to the
  bound" traps), example 7, 7, 10 (100 > 98, obtuse). Explanation and video (number line, "two too big" insight) updated.
- **Summary "Area":** the altitude example gave 28.8 (1728 / 60), an awkward decimal → legs 45, 60, hypotenuse 75: 2700 / 75 = 36.

`python3 math_check.py 31 32` → PROBLEMS 0, WARNINGS 0, LAYOUT 0.
