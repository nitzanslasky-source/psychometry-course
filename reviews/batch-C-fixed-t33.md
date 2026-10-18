# Batch C, topic 33: fixes applied (Claude, 18 Oct 2026)

Source review: `reviews/batch-C.md` (Codex), topic 33 only: #248–#285, 38 lessons from geo-074 to solve-q-r26-t33-05. Another agent fixes topic 32 in `_ai_vis_t32.py`, which was not touched here.

## Result

- **must: 55 of 55 fixed. should: 41 of 41 fixed.** Multi-part bullets were counted once and every clause was handled.
- **0 parked.**
- **0 skipped.** All 38 lessons were still Record, with no take in `~/Documents/Course.recordings/_reading/<id>/`. This was checked before editing and checked again at the end.
- **Needs Claude:** prompter display only, 7 lessons (list below). The speech was reworded wherever that avoided a bad display.

Canonical source edited: `math_patches/_ai_vis_t33.py` only. It regenerates the 38 `ai_scripts/<id>.json` files.
Not edited: `_method_visuals.py`, `_camera_parts.py`, `_math_vars_display.py`, `reading_studio.py`, the display registry, other topics.

New helpers in `_ai_vis_t33.py`:
- `NOFIG33` (set): a question slide that shows our enlarged copy instead of the question figure, as `NOFIG31` did in batch B.
- `LEFT(fig, y, x, w)`: places that copy, optionally at a new width.
- `ROWS(y0, dy, *items, x, w)`: readable working rows in the right column.
- `FLOW(items, cols)`: flows rows into one or two columns by their real height. The renderer pushes an overlapping box down.
- A `_w` row width in `_layout`, so two columns of rows can sit side by side.
- A final "batch C layout pass" block, just before the camera-parts split. It places the crowded slides so that no row runs into the choices.

Everything kept: every original method and its order, her voice (W1–W21, "choice number N", numbers as words, no symbols or labels), the method vocabulary, fonts and design, the dark-blue geometry pen, and figure orientation.

Structural changes, all in unrecorded lessons:
- Several question videos now open with a question slide, then show our copy on hide-figure slides with readable rows: g076, t33-01, g078, t33-02, g083, g085, g086, g087, g088, g089, g090, g091, g092, g094, g095, g096, g097, g098, g099, g101, g102, t33-04, t33-05.
- New slides:
  - t33-01: "The circumference", which teaches C = πd = 2πr at first use.
  - geo-079: "Why πr²", built from 8 slices.
  - g083: "Four ninths of the area".
  - g089: "The circumference and pi".
  - g092: the triangle of centres, and circle A alone.
  - g094: "The triangle's area".
  - g096: 4 → 6 slides; the scale reasoning is now "Method 4 · Understanding: the scale".
  - g097: the rotation figure.
  - g098: a construction slide.
  - g099: "Three pieces".
  - g101: "Now try four".
  - more-tools: "The shared region in numbers", with a second radius-2 case.
  - t33-05: "Why the short formula works" and "Check: nine and four".
  - t33-03: Method 1 is split into two slides, and Method 2 too.
  - geo-097-after: "Length factor, area factor".
- geo-074 part 1 lost its one-sentence ¶7: the letter r is now named in ¶5, where the label appears.

## Checks (final state)

- **Regeneration:** `python3 math_patches/_ai_vis_t33.py <38 ids>` gives no PROBLEMS. Running it with no ids writes exactly these 38 (topic 33's ORDER is this scope).
- **Private test studio:** `OUT=…/scratchpad/test-t33.html python3 build_verbal.py` built. The shared Downloads file was not written. One earlier attempt failed inside t32, the other agent's work in progress; the retry built cleanly.
- **`ai_check`** (`SRC=` the private build): 38 of 38 OK, and the cue counts match the build.
- **`w19_check`:** 211 → 173 flags. No new flags against the baseline, compared by sentence.
- **`math_check 33`:** 0 problems, 0 warnings, layout 0 (182 slides). The same holds with `AI_HANDWRITE=all`. The baseline was also 0 layout problems; 24 overlaps that came with the new rows were fixed by the layout pass.
- **Studio layout check** (layoutcheck on the private build, per lesson): 0 overlaps and nothing off the board in all 38.
- **Step frames:** every step frame was rendered from the private build with a boardSvg contact-sheet harness and looked at. This covers all 38 lessons, plus the final states of every crowded slide in both renderers. Splits were checked for premature results: values, labels and answers appear only at their own clause.
- **Numbers:** every new number was recomputed in Python by the agent that wrote it, and the merged results were spot-checked.

## Needs Claude: display (prompter grouping only; spoken text cannot fix these without losing meaning)

- **solve-geo33-g080**
  - 3.1 "That's pi r squared over two pi r." → πr²/(2πr), with the denominator grouped.
  - 3.2 "That leaves r squared over two r." → r²/(2r).
- **solve-q-r26-t33-03**
  - 1.6 "nine over four, which is two and a quarter" → 9/4 = 2¼.
  - 2.1 "two and a quarter old areas" → 2¼.
  - 2.2 "Two and a quarter minus one is one and a quarter" → 2¼ − 1 = 1¼. Use mixed numbers, not word strings.
- **solve-geo33-g087:** verify the prompter shows 4.2 "A O is a radius, and it's five. O C is a radius too, so it's also five." as AO = 5, OC = 5, and 4.4 "So A C is five root two" as AC = 5√2.
- **solve-geo33-g096:**
  - 2.7 "Pi r plus two r, over three r." → (πr + 2r)/(3r).
  - 2.7 "r times pi plus two, all over three r" → r(π + 2)/(3r).
  - 2.7, 3.3, 3.4, 4.2, 4.4 and 6.6 "pi plus two, over three" → (π + 2)/3.
  - 4.2 "two pi plus four, over six" → (2π + 4)/6.
  - 4.3 "pi plus two, over three r" → (π + 2)/(3r); "pi plus two, over six" → (π + 2)/6; "r times pi plus two, all over three" → r(π + 2)/3.
  - 6.1 "pi plus two, over six / over nine" → (π + 2)/6, (π + 2)/9.
  - 6.3 "from pi plus two to two pi plus four" → π + 2, 2π + 4.
- **geo-097-after**
  - 2.4 "So the outer side is root two times the inner side." → outer side = √2 × inner side.
  - 3.5 "So the outer radius is root two times the inner radius." → outer radius = √2 × inner radius.
  - 3.6 "root two squared times bigger" → (√2)² times bigger.
- **solve-geo33-g102** (1.x–4.x):
  - "four theta" → 4θ; "two theta" → 2θ.
  - "ninety minus two theta" → 90 − 2θ.
  - "a hundred eighty minus four theta" → 180 − 4θ.
  - "theta over forty-five" → θ/45.
- **geo-075:** the summary-row arrows were replaced by colon captions on the board. In our renders the arrows were already spaced, so nothing is needed unless the prompter still shows tight arrows elsewhere.

## Per lesson


### #248 geo-074 (camera lesson, part 1)
- [should] ¶1/3–5/11 transitions and the detour: **fixed**. ¶1 now opens "Let's start with circle vocabulary." ¶3 drops "By the way… Most people don't know this" and "in math it even has its own name"; it keeps the round line vs. the inside with the wooden board. ¶4 says "The area of the circle means the area inside, all the wood. The circumference is the length of the round line, the edge." ¶5 opens "First, a radius." ¶11 opens "Now let's join two points on the circle with a straight line. A line like that is called a chord."
- [must] ¶12 chords "not equal" and ¶9–10 the triangle case: **fixed**. ¶12 now says "Chords don't have to have the same length… These three chords are all different", and the long/short/very-short labels appear at that sentence. ¶9 says "When the two points and the center are not on one straight line, we get a triangle". ¶10 adds "If the two points and the center are on one straight line, there's no triangle. That line is a diameter, and we'll meet it in a moment."
- [should] ¶6–8/16 the boards: **fixed**. The 14→7 and 6→12 examples are now four rows, each shown at its clause: `diameter = 14`, `radius = 14 ÷ 2 = 7`, `radius = 6`, `diameter = 2 × 6 = 12`. The speech says "Fourteen divided by two is seven… Two times six is twelve." The symbol r is no longer drawn before it is named: the radius is drawn first, and its "r" label is its own layer, shown at "We usually mark the radius with the letter r". That sentence moved into ¶5, and the old one-sentence ¶7 was removed. The circle/radius cases are kept.
- Teaching check: two radii → isosceles triangle (already taught here with three cases); diameter = 2r (taught here) → not needed.

### #249 geo-074-2 (part 2)
- [must] ¶2 inscribed-angle definition: **fixed**. It now says "An inscribed angle is made by two chords that start at the same point on the circle." The C→A/B construction is kept as the example.
- [should] ¶6/8 fragments and ¶13 the position of C: **fixed**. ¶6 now reads "Now let's look at a central angle." ¶8 now reads "An arc is a part of the circle…" ¶13 now reads "Take a point C on the other side of the circle, on the long arc, away from the teal arc. Draw two chords from C to A and to B." The walls analogy is kept.
- Teaching check: intercepted arc, the far side (taught here, used again in geo-075) → not needed.

### #250 geo-074-3 (part 3)
- [must] ¶9 "a segment doesn't reach the center": **fixed**. It now says "A sector is closed off by two radii and an arc. A segment is closed off by one chord and an arc. This small segment leaves the center O outside it. But a big segment, more than half the circle, can have O inside it." The three small figures now show the centre O (a dot and a label) in the sector, the small segment (O outside) and the big segment (O inside). Both segment cases are kept.
- [should] ¶10–11 "name each line before I do": **fixed**. Each line is drawn first ("Look at O A first." / "Now look at B C." / "Now look at D E." / "And now the line at T."), then a [short pause], and only then its name caption appears, as its own layer at the explanation. The radius, diameter-also-chord, chord and tangent distinctions are kept.
- Teaching check: no reusable rule here (vocabulary) → not needed.

### #251 geo-075
- [must] ¶18 the rectangle: **fixed**. This is now its own paragraph: "Now take a rectangle whose four corners are all on the circle. Each corner is a right angle on the circle. So by the backwards rule, the line joining its two neighbors is a diameter. That line is a diagonal. So each diagonal of this rectangle is a diameter." The rectangle is drawn first, with its corner dots and a right-angle mark. The two diagonals and "diagonal = diameter" come at "That line is a diagonal".
- [must] ¶8–9/18/21/24 the boards: **fixed**, each value at its own clause:
  - `COA = 180° − 2x` comes in its own sentence ("so angle C O A is…"). Then `AOD = 2x` and the 2x arc come in a new paragraph: "Now look at angle A O D, right next to it. C O D is a straight line, the diameter, so the two angles add up to a hundred eighty."
  - ¶9 names "Angle B O D is two y" and "The central angle A O B is made of A O D and B O D". `inscribed: x + y` and `central: 2x + 2y` are now two layers.
  - Legs 24/10 → `26` at "so the hypotenuse is twenty-six" → `r = 26 ÷ 2 = 13` at "So the radius is twenty-six divided by two".
  - 75° at A → `180° − 75° = 105°` with 105° at C → "same for B and D". Each is its own layer, and the old caption "75° + 105° = 180°" was replaced by the subtraction that is said.
  - `2α + 2β = 360°` → `α + β = 180°` at "So we divide both sides by two".
- [must] ¶26 the 35° inscribed angle and the scope: **fixed**. A real 35° inscribed angle is drawn now: vertex E on the long arc, with chords to A and B, a 35° arc and "inscribed on arc AB: 35°". It appears at "Its vertex E is on the other side of the circle, on the long arc." The speech now says "The short arcs A B and C D are equal, and so are the long arcs" (corresponding arcs). The restriction is now "Here we're comparing within this same circle", and the red caption reads "here: within the same circle".
- [should] ¶1/2/10/14/19/29 transitions and summary arrows: **fixed**. The new openings:
  - ¶1: "Last lesson we learned the words… Now let's learn the rules of the angles in a circle."
  - ¶2: "Let's start with the main rule."
  - ¶10: "Now let's use the main rule to compare inscribed angles."
  - ¶14: "Now let's use the main rule on a diameter."
  - ¶19: "Now let's look at a quadrilateral inside a circle."
  - ¶29: "So we have one main rule."
  
  The summary rows no longer use bare arrows. They use colons with spacing ("Same arc:  equal inscribed angles", "Same circle:  equal chords, equal arcs, equal central angles", …), so nothing touches.
- Teaching check: the main rule and all its consequences are taught here with a why each → no addition.

### #252 solve-geo33-g076
- [must] ¶4 eliminating 76 by looking: **fixed**. The "you can see it… much bigger than ninety" argument and the early cross are gone. It now says "But that subtraction uses a rule whose conditions aren't met here. So let's find the angle correctly." The red caption reads "180° − 104° = 76°: wrong rule". 76 (choice number three) is crossed only after 128 is found ("Seventy-six came from treating A O C B as inscribed, and it isn't."). The O-not-on-the-circle trap is kept.
- [must] ¶19 Method 3 sign steps: **fixed**. x is first marked as the whole angle at B ("Our x is the whole angle at B, angle A B C"), then α and β as separate layers. The working is written as six rows, each at its clause:
  - `x = α + β`
  - `(180° − 2α) + (180° − 2β) = 104°`
  - `360° − 2α − 2β = 104°`
  - `360° = 104° + 2α + 2β` ("let's add two alpha and two beta to both sides")
  - `256° = 2α + 2β` ("subtract one hundred four from both sides")
  - `α + β = 256° ÷ 2 = 128°` ("we divide both sides by two")
  
  All three routes are kept, with the same cut-out orientation.
- [should] ¶6/11/16 method names and the decompositions: **fixed**. The methods are now announced as "Let's start with the math way, with the main rule", "It's the math way again, this time with the big central angle" and "the math way with radii". "It's not hard… some students find it hard" was removed. New rows:
  - `∠ADC = 104° ÷ 2 = 52°`, `∠B + ∠D = 180°`, `x = 180° − 52° = 128°`.
  - `360° − 104° = 256°`, `x = 256° ÷ 2`, `200° ÷ 2 = 100°`, `56° ÷ 2 = 28°`, `x = 100° + 28° = 128°`.
  
  The method slides now hide the question figure (NOFIG33) and show our copy on the left with readable rows on the right. The tiny in-figure captions were removed. The major-arc shading is kept.
- Teaching check: reflex central angle → inscribed angle on the major arc (taught here in Method 2 with a why) → not needed.

### #253 solve-q-r26-t33-01
- [must] ¶2 2πr not yet taught: **fixed**. Slide 1 (renamed "The circumference", question figure kept) now teaches it at first use: the circumference is the length around, the edge, not the area inside; once around any circle is a bit more than three diameters, that fixed number is π (a little more than 3), so C = π × d; d = 2r so C = 2πr; two easy examples (d = 10 → 10π; r = 3 → d = 6 → 6π). Each written in its own row at its clause (C = π × d, π: a bit more than 3, d = 2r, C = 2πr, d = 10, C = 10π, r = 3, d = 6, C = 6π). The "there's a lesson soon" line is gone. No derivation of π.
- [must] ¶8–9 bundled Pythagoras: **fixed**. New slide 2 (NOFIG33: our enlarged copy instead of the question figure, LEFT) with rows r² = 6² + 8², then 6² = 36, 8² = 64, r² = 36 + 64 = 100, then r = 10 (new sentence "A length is positive, so r is ten."), then C = 2π × 10 = 20π, each at its clause; the tiny SVG captions (pyth, c) were removed. The circumference trace now appears at "The circumference is two pi r". 6–8–10 triple and the helper-line construction kept.
- [should] ¶10 πr² unexplained / chord warning: **fixed**. "That's the formula for the area, the inside of the circle, and we'll learn it in the area lesson. This question asks for the length around, not the area inside." The non-diameter warning is its own paragraph and a red "16: not a diameter" label appears beside the actual chord at "And sixteen pi comes".
- Teaching check: chord + distance + radius right triangle → **added** (4 sentences + one board line, before the goodbye). Circumference formula → now taught here (above).

### #254 geo-077
- [must] ¶16/22 tangent segments, not lines: **fixed**. "From the same point outside the circle, the two tangent segments are equal. Here they're P D and P E. Each one starts at P and stops at its touching point." The recap line and its board caption say "From one outside point, the two tangent segments are equal: a kite". The shared-hypotenuse Pythagoras why is kept.
- [must] ¶18 9/9 example on the 5/12 figure: **fixed**. A separate clean figure (f3t5: another circle, P outside, tangent segments labelled 9, then the second 9 with equal ticks) appears at "Now take another circle…"; PD = 9 → PE = 9 at "with no calculation". The 5/5/12/12 figure is untouched; the kite paragraph starts "Now back to our first figure."
- [must] ¶13 bundled 25+PD², PD², PD and the why of radius ⊥ tangent: **fixed**. Three rows: 25 + PD² = 169; PD² = 169 − 25 = 144 (at "which is a hundred forty-four"); PD = 12 (with "A length is positive"). New paragraph after the rule: the tangent touches only at D, every other point is outside so farther from O, so D is the closest point, and the shortest way from a point to a line is the perpendicular. On the board a red dashed "longer" segment from O to another point of the tangent, and the caption "D: the point of the tangent closest to O".
- [should] ¶1/2/9/14 wording: **fixed**. "Now let's learn about tangents to a circle…"; "A tangent is a straight line that touches the circle at one point only. It doesn't go inside the circle." (both "brushes" gone); "A tangent gives us a right angle when we join O to its touching point. So every time … draw the radius to the point of tangency." ("don't think too much" gone); "We can also spot it with a triple." (no "faster").
- Teaching check: radius ⊥ tangent → now taught with its why (above); equal tangent segments → already taught with why. No addition.

### #255 solve-geo33-g078
- [should] ¶2–4 method name / repeated reflex paragraph: **fixed**. Slide 1 is now the question only ("The question", with the first reaction). Method 1 opens "Let's start with the math way. Here's the figure again, bigger. We have tangents to a circle, so the first thing we do is draw the radii…", and the mnemonic is said once in the same paragraph ("Make that a habit. Tangents, then radii, then right angles."). The separate "Always, automatically… reflex" paragraph is removed. Method 2 says "by understanding, with symmetry".
- [must] ¶6/9 board: **fixed**. Both method slides are NOFIG33 (our enlarged copy on the left, readable rows on the right); the in-figure captions were removed. Method 1 rows: 90 + 90 + 68 + ∠O = 360 (at "add up to three hundred sixty"), 90 + 90 = 180, 68 + ∠O = 180, ∠O = 180 − 68 = 112 (112 on the figure at "which is a hundred twelve"), x = 112 ÷ 2 = 56 (56 at A at "is fifty-six"). Understanding: 68 ÷ 2 = 34 is written before the two 34° halves are drawn ("So each half is thirty-four"); then 180 − 90 = 90 and ∠DOP = 90 − 34 = 56 (new spoken steps) before the 56 label; then ∠DOP = ½∠DOE = x and x = 56. The 112 and 34 traps and the central/inscribed comparison are kept.
- Teaching check: "two tangents from P: angle P + central angle = 180" → **added** (a paragraph after the Method 1 answer, with a 40 → 140 second case and one board row).

### #256 solve-q-r26-t33-02
- [must] ¶3/8–10 bundles, "move to the other side", unwritten formula: **fixed**. Slide 1 is the question only; Method 1 and Method 2 slides are NOFIG33 (enlarged copy left, rows right; SVG captions removed). Rows: 8² = 64, 15² = 225, 64 + 225 = 289, 17² = 289 hypotenuse 17 (17 on the figure at "is seventeen"), (8 − r) + (15 − r) = 17, 23 − 2r = 17, 23 = 17 + 2r ("let's add two r to both sides"), 6 = 2r ("subtract seventeen from both sides"), r = 3 ("divide both sides by two"). Method 2 names "the math way again, with a short formula", states the scope (right triangles), writes r = (a + b − c)/2 with "a, b: the legs, c: the hypotenuse (right triangle)", gives the one-line why (the leg pieces a − r and b − r add up to c), then 8 + 15 − 17 = 6, r = 6 ÷ 2 = 3, and the 3-4-5 check 3 + 4 − 5 = 2, r = 2 ÷ 2 = 1, each at its clause.
- [should] ¶4 why a square / 8.5 warning / method name: **fixed**. New paragraph: the corner shape has three right angles so the fourth is too; its two sides from the centre are radii, both r; a rectangle with two equal adjacent sides is a square (tint + equal ticks shown at "Its two sides from"). The 8.5 warning is text only, nothing drawn as the incircle radius: row "17 ÷ 2 = 8.5: the circle around the triangle, not inside" and "…the circle around the triangle, the one through its three corners. So eight and a half is the radius of that outside circle, not of the circle inside." "Let's start with the math way" is said.
- Teaching check: inradius formula → taught here now (above). No addition.

### #257 geo-079
- [must] ¶2–4 πr² without a why: **fixed**. New slide "Why πr²" right after "What is π?" (circumference known by then): a circle cut into eight equal slices (alternate teal/orange), laid in a row up/down, "almost a rectangle"; height r, bottom half the circumference = πr (labels at their clauses); dashed outline + "area ≈ πr·r = πr²"; "With eight slices, the edges are still bumpy, so it's not exactly a rectangle. But the thinner the slices, the closer it gets to a real rectangle." Slide 2 says "We'll see why in a moment." Inside-vs-boundary contrast, unrolling and examples unchanged.
- [must] ¶25/33 divisor grouping: **fixed** on the board and by rewording speech: rows are now stacked fractions r = 22π/(2π) = 22/2 = 11 and 1000π/(20π) = 1000/20 = 50 turns; speech no longer says "twenty-two pi divided by two pi" / "a thousand pi divided by twenty pi" ("the pi on top and the pi on the bottom cancel, and twenty-two divided by two is eleven"; "The pi's cancel, and a thousand divided by twenty is fifty"), so the prompter cannot show a bare a π ÷ bπ.
- [should] ¶1/12/26–29: **fixed**. "Now let's calculate a circle's area and circumference."; "For a rough comparison, like the next one, that's all we need to know about pi" (board: "For a rough check: S = πr² is a bit more than 3r²"); r = 11 is its own row at "and r is eleven", the negative case its own paragraph and row ("Negative eleven, times itself, also gives a hundred twenty-one. But it isn't relevant here. A radius is a length, so it must be positive."); the wheel "rolls without slipping".
- Teaching check: area formula → now has its why (above). No further addition.

### #258 solve-geo33-g080
- [must] ¶3 "ignore the units": **fixed**. "Let's start with the math way. The question compares the numbers, in the units it gives. The area is in square centimeters, and the circumference is in centimeters. So we compare those two numbers. The area's number is four times the circumference's number." Board: "Area (in cm²) = 4 · circumference (in cm), as numbers". Method 2 also says "how many times bigger the area's number is".
- [should] ¶9–12 bundles / method names: **fixed**. Check: S = π·8² = 64π and C = 2π·8 = 16π are two rows at "That's sixty-four pi" / "That's sixteen pi", then 4·16π = 64π. Understanding ("Now let's solve it a second way, by understanding"): S/C = πr²/(2πr) at its clause, then = r²/(2r) ("The pi on top and the pi on the bottom cancel"), then = r/2 ("One r cancels too, because r isn't zero"), then r/2 = 4, then r = 2·4 = 8 (new W21 step). Positive-radius condition and the 16 diameter trap kept.
- Needs Claude (display): 3.1 "That's pi r squared over two pi r." → show πr²/(2πr) (denominator grouped); 3.2 "That leaves r squared over two r." → r²/(2r).
- Teaching check: not needed (known formulas; S/C = r/2 shown with its why).

### #259 solve-q-r26-t33-03
- [must] ¶3/6–7/12 percent denominator first taught: **fixed**. "Let's start by understanding." then "A percent change is always compared with the old amount. The old amount is a hundred percent, the whole thing. Fifty percent is half of it, and twenty-five percent is a quarter of it." (row "the old amount = 100%, half = 50%, a quarter = 25%"), then "fifty percent more means the old circumference plus half of it". Trap: "Compared with the old area, the new area is two and a quarter old areas. That's two hundred twenty-five percent… the whole new area, not the increase" (row "225%: the whole new area, not the increase"); the increase: 2¼ − 1 = 1¼, "one whole old area, plus a quarter of the old area", then "One old area is a hundred percent, and a quarter of it is twenty-five percent… a hundred twenty-five percent" (row "increase = 100% + 25% = 125% of the old area"). Square-scaling shortcut and the radius-2 trial kept; the trial is framed as "the question promises the same answer for every circle, so a circle that we choose must give it too", not a proof.
- [must] ¶9–12 premature radius 3 / bundles / prompter: **fixed**. The radius-3 circle is a separate layer shown at "so the new radius is three". Rows: C = 2π·2 = 4π; 4π ÷ 2 = 2π; 4π + 2π = 6π; 6π = 2π·3, r = 3. The areas got their own slide (same Method 2 sidebar, a second copy of the two circles): old π·2² = 4π, new π·3² = 9π (each tint at its clause), up 9π − 4π = 5π, then 5π = 4π + π, "π is a quarter of 4π: 25%", 100% + 25% = 125%. 125% is not on the board before the old-area comparison. The spoken "five pi over four pi" is gone (now "We compare the increase with the old area, four pi… Five pi is four pi, plus one more pi"), so the prompter no longer has an ungrouped 5π/4π. Scaling rows: (3/2)² = 9/4 = 2¼, then "new area = 2¼ old areas".
- Needs Claude (display): 1.6 "nine over four, which is two and a quarter" and 1.8 "Two and a quarter minus one is one and a quarter" → show 2¼ and 1¼ as mixed numbers (not word strings).
- Teaching check: percent of the old value → now taught here (above). No addition.
- Layout (coordinator, after merge): Method 1 is split into two slides: "Length × 3/2, area × 9/4" up to the new area, then "Total or increase?". The second slide starts with a carry row `new area = 2¼ old areas`. Before the split, the rows ran into the choices. Display ids after the split: 1.6, 2.1 and 2.2.

### #260 geo-081
- [must] slide 9 angle table false equalities: **fixed**. Each mapping is its own row at its own clause, worded "this angle: that part of the circle": "90°: 90°/360° = ¼ of the circle", "45°: half of 90°, ⅛ of the circle", "60°: 360° ÷ 6 = 60°, ⅙ of the circle", "40°: 360° ÷ 9 = 40°, 1/9 of the circle", "36°: 360° ÷ 10 = 36°, 1/10 of the circle", "72°: 360° ÷ 5 = 72°, ⅕ of the circle", "270° = 3·90°: ¾ of the circle", "144° = 2·72°: ⅖ of the circle", "120°: ⅓ of the circle", then "120° = 2·60° = 3·40°" at "but it's also a sixth times two". Speech adds the easy 360 ÷ n checks for 60, 36 and 72.
- [should] ¶4–5/12/17 formula vs shortcut: **fixed**. No "strongly recommend not using" / "much better" / "leave the formula". "Alpha over three hundred sixty is the fraction of the circle the sector takes. So the sector's area is alpha over three hundred sixty, times the area of the whole circle"; "The formula and the share are the same idea. For example, for ninety degrees, ninety over three hundred sixty is a quarter" (row 90°/360° = ¼: the same idea); arc: "the same fraction of the circle, but this time times the whole circumference"; recap "they say the same thing as the fractions". α named as the central angle at the centre. "equal parts" said for 8, 3 and 5 (4, 5 sectors and 6 already said it).
- [should] ¶1/18–21: **fixed**. "Now let's learn about sectors and arcs…"; the 23.5° guarantee and the "exam checks understanding, not calculators" caption are gone: "They're common fractions of the circle. But if a question gives a different angle, we use that angle, with alpha over three hundred sixty." (row "Another angle? Use α/360°"). The arc-versus-perimeter slide is unchanged; its radii are highlighted only at "the arc plus the two radii" (already so).
- Teaching check: not needed (the fraction-of-circle idea is the lesson itself).

### #261 solve-geo33-g082
- [should] ¶2: **fixed**. "If that confused you a little, great" and "and so on" are gone. It now says "Let's use Understanding. We'll find which part of the circle the arc is. To do that, we compare the arc with the whole circumference." The formula comparison is dropped, so no grouped formula is needed. The fraction route is unchanged.
- [should] ¶4–5 display: **fixed**. The tiny captions inside the figure are gone. Readable rows under a smaller copy, each at its clause:
  - "whole circle: 2π × 10 = 20π";
  - the stacked fraction 4π/20π = 4/20 = 1/5, at "Four out of twenty is a fifth" (the speech adds "because the pi cancels");
  - α = 360° ÷ 5 = 72°, at "Three hundred sixty divided by five is seventy-two".
  The five-arc cut and the sector tint are kept, and 72 does not appear before its clause.
- Teaching check: fraction of the circle → already taught (geo-081); nothing added.

### #262 solve-geo33-g083
- [should] ¶2/5: **fixed**. "let's save ourselves that" became "Let's find which fraction of the circle is shaded. That's what the sector formula means anyway." Kept: the non-overlap condition (stem), third + ninth, the 9π ÷ 9 × 4 route and the separate-sector check.
- [must] ¶4–7 working: **fixed**.
  - Slide 1 has rows 1/3 = 3/9 and 3/9 + 1/9 = 4/9 of the area, each at its clause.
  - New slide 2, "Four ninths of the area" (no question figure, same sidebar). A fresh copy with the 1/3 and 1/9 tints, and rows at their clauses: area π·3² = 9π; circumference 2π·3 = 6π; 4/9 × 6π = 8π/3 "a length, not an area" (shown only when the trap is discussed; choice 2 is crossed there); 9π ÷ 9 = π; 4 × π = 4π.
  - Separate-sector check: π is written on the small sector and 3π on the big one, then the row "two sectors: π + 3π = 4π". The speech now says "The question asks for both sectors, so don't stop at three pi."
- Teaching check: sector = fraction × area → already taught (geo-081); nothing added.

### #263 geo-084
- [should] ¶1/3: **fixed**.
  - ¶1: "In the last lessons we learned the rules of the circle. Now let's use the circle rules in questions." The title fragment is gone.
  - ¶3: "So here, two radii and the chord between them make an isosceles triangle. That needs a real triangle. If the two radii make one straight line, a diameter, there's no triangle. Isosceles triangles hide inside many circle questions." ("almost every" was softened.)
  - Kept unchanged: the three recap diagrams, the same-arc condition and the added radius.
- Teaching check: not needed (roadmap lesson).

### #264 solve-geo33-g085
- [must] ¶5/8–10/14 boards: **fixed**.
  - Slide 1: the copy is cropped to the circle (same orientation and labels), and the tiny captions are replaced by rows: ∠BOC = 180° − 120° = 60°; OB = OC (radii); 180° − 60° = 120°; 120° ÷ 2 = 60° (the two base-angle 60° labels appear only at "two is sixty"); "all three 60°: equilateral".
  - Slides 2–3 have no question figure: the enlarged same-orientation cut-out sits on the left at 600 wide, and readable rows go on the right.
  - Slide 2 rows: r = 20 ÷ 2 = 10; the general formula S = a²√3/4 at "It's a squared, times root three"; 10² = 100; S = 100√3/4; 100 ÷ 4 = 25; S = 25√3, each at its clause.
  - Slide 3 rows: long leg h = 5√3; S = (10 × 5√3)/2; 10 × 5√3 = 50√3; 50√3 ÷ 2 = 25√3. There is no early 25√3.
- [should] ¶2/8: **fixed**.
  - "Let's use the math way. We'll start with the hundred twenty degree angle…"
  - "Now let's use the diameter, twenty."
  - "So let's use the math way with the equilateral formula."
  - "It's the same math way, this time with the height."
  - The a-two-three-four mnemonic and the gold-triangle route are kept.
- Teaching check: equilateral area / gold triangle → already taught (topic 31); nothing added.

### #265 solve-geo33-g086
- [must] ¶13–14: **fixed**.
  - The paragraph "We don't need to prove it… easy question early… none of the choices…" is deleted.
  - It now says: "Now fold the figure along the line through A and the midpoint of B C. The fold swaps B and C. A B is equal to A C, so A stays where it is. And O B is equal to O C, so the center O is on that fold line too. So the radius O A lies right on the fold." Then: "The fold also swaps the two halves of the angle at A. So O A cuts the angle at A into two equal parts."
  - The board shows a dashed orange fold line (axis through A, O and the midpoint M of BC, labelled "fold line") at the fold sentence, before the 28° halves appear.
- [must] ¶6/9–10 boards: **fixed**.
  - Slide 1 rows (copy cropped to the circle): ∠BOC = 2 × 56° = 112°; OB = OC (radii); 180° − 112° = 68°; ∠OBC = 68° ÷ 2 = 34°. The 34° labels appear at "So angle O B C is thirty-four".
  - Slide 2 has no question figure. Rows: 180° − 56° = 124°; ∠ABC = 124° ÷ 2 = 62°; and, only at "Sixty-two minus thirty-four", x = 62° − 34° = 28°.
  - New enlarged detail of the angle at B (rays BC, BO, BA in the same order as the figure; 34° teal, the whole 62° orange; x red added at "So x is what's left"), labelled "the angle at B, enlarged". The speech now says "the part next to B C" instead of "its lower part", which was wrong for this figure. The original orientation is kept.
- [should] ¶2/11/15: **fixed**.
  - "a shorter psychometric way", "The math solution was quite short" and "This way is shorter, with fewer calculations" are gone.
  - ¶2: "We'll solve it in two different ways."
  - Method 2 opens: "Now let's solve it by Understanding, with symmetry. We add one helper line, the radius O A. Then we can use equal radii and symmetry, instead of finding the whole angle at B."
  - Slide 3 (no question figure) rows: 56° ÷ 2 = 28°; OA = OB (radii); x = ∠OAB = 28°.
- Teaching check: the symmetry line of an isosceles triangle in its circle (vertex–center line halves the top angle, perpendicular bisector of the base) → **not added**: the fold-line explanation from the fix already teaches it (see teaching-check-C-t33.md).

### #266 solve-geo33-g087
- [should] ¶2/12: **fixed**.
  - ¶2: "We need the false statement. So let's check each statement against the givens. Each true one is crossed out." ("even possible" and "hope" are removed.)
  - ¶12: "Three statements are true, so they're out. Only choice number four is left, so you mark it and move on. No need to check the last choice once only one remains." ("There's no time" is removed.) The classroom check is kept.
- [must] ¶9/14–16: **fixed** (board) / **needs Claude (display verify)**.
  - Slide 2: the bundled sum caption is replaced by four rows at their clauses: 4x = 180°; 180° ÷ 2 = 90°; 90° ÷ 2 = 45°; x = 45°: true. The copy is cropped to the circle.
  - Slide 4 (no question figure): triangle AOC is tinted in the circle and pulled out as an enlarged copy (same orientation, A O C labelled). On it appear 5 at "A O is a radius", 5 at "O C is a radius too", the right angle at "is ninety", the 45° base angles at "That's the silver triangle", and 5√2 at "So A C is five root two".
  - Slide 4 rows: AO = 5; OC = 5 (a radius); ∠AOC = 45° + 45° = 90°; silver: hypotenuse = leg × √2; AC = 5√2, not 5√3. ¶13 now reads choice 4 aloud first (W17).
  - Prompter: the speech is now "A O is a radius, and it's five. O C is a radius too, so it's also five." Please check that the prompter shows AO = 5, OC = 5 and AC = 5√2 (4.2, 4.4).
- Teaching check: equal chords ↔ equal central angles; silver triangle → already taught; nothing added.

### #267 solve-geo33-g088
- [must] ¶8–9: **fixed**.
  - It now says "When two circles touch from the outside, the touching point lies between the centers, on the line O M."
  - Slide 2 has no question figure: the original 7 + 7 view stays on the left the whole time, with row OM = 7 + 7 = 14.
  - On the right, a real inside-touching example: a big circle R = 5 and a small circle r = 2 inside, touching once, with both centers and the touching point on one line, labels R = 5, r = 2 and an orange 3 between the centers, plus the row "inside: R − r = 5 − 2 = 3".
  - Speech: "Compare that with circles that touch from the inside… both radii go the same way… With radii five and two, it's five minus two, which is three. In our question the circles touch from the outside, so it's seven plus seven."
  - Slide 3 continues on a fresh 7/7/14 copy.
- [must] ¶11: **fixed**. "it has to be … silver or gold" is gone. Now: "Here the hypotenuse is twice a leg, fourteen and seven. That's the gold triangle ratio we know… The silver triangle doesn't fit here, because its hypotenuse is the leg times root two." The tangent reminder (¶3) is scoped: "two tangent segments from the same point to the same circle are equal".
- [should] ¶4/7/16–17: **fixed**.
  - The helper line is no longer defined again. ¶4: "So let's add a helper line, a radius to each point of tangency. We draw it because it gives us right angles." ¶7: "To use the touching, we join the two centers."
  - The math way is named in ¶2.
  - Recap: "We used two types of helper line. First the radii to the points of tangency, which gave us right angles. Then the line between the centers, which used the touching circles."
  - Slide 4 (no question figure) has rows at their clauses: ∠AOB = 60° + 60° = 120°; kite: ∠M = 30° + 30° = 60°; 360° − 90° − 90° = 180°; 180° − 60° = 120°. The speech says the intermediate 180 aloud.
- Teaching check: inside vs outside touching distance → added as part of the fix; nothing more.

### #268 solve-geo33-g089
- [must] ¶9–10 π: **fixed**. It now says "How much is pi? Its digits go on forever, three point one four one five nine, and so on. So pi is more than three point one four, and less than three point one five."
  - Lower end: 16 × 3.14 = 50.24, worked as 16 × 3 = 48 plus 16 × 14 = 224 → 2.24.
  - Upper end: "Sixteen times point one five is two point four. So sixteen times three point one five is fifty point four."
  - Then "So sixteen pi is between fifty point two four and fifty point four. That's between fifty and fifty-one."
  - The π = 3 trap is kept ("Here that's too rough"). π is never called exactly 3.14.
- [must] ¶4/7/10 working: **fixed**.
  - Slide 1: the copy is cropped to the circles. Rows beside it at their clauses: 2πr = 10π; 2r = 10; r = 10 ÷ 2 = 5; π·5² = 25π; 25π + 39π = 64π; πR² = 64π; R² = 64; R = 8.
  - Targeting: the ring alone is shaded orange at "The shaded ring is thirty-nine pi", and the whole large circle is outlined at "together make the whole".
  - New slide 2, "The circumference and pi" (no question figure), with the large circle and R = 8. Rows: C = 2π × 8 = 16π; 3.14 < π < 3.15; 16 × 3 = 48; 16 × 14 = 224, so 16 × 0.14 = 2.24; 16 × 3.14 = 50.24; 16 × 3.15 = 48 + 2.4 = 50.4; 50.24 < 16π < 50.4; "π as 3: 16 × 3 = 48, too rough".
- Teaching check: the ring as big minus small, and "go back to the radius first" → **not added**: r26-t33-more-tools teaches the ring in full.

### #269 solve-geo33-g090
- [should] ¶2–4 circumscribed-circle facts: **fixed**. "Every triangle can be circumscribed" and the Rule one / Rule two headlines are gone. Now: "Here's the first fact. Every triangle has a circle that passes through all three of its corners." and "And here's the second fact. Every triangle has exactly one circle through its three corners. What does that mean? With these same three corners on the circle, we can't choose a different radius." The acute and obtuse examples are kept.
- [must] ¶6–7 working: **fixed**. Slide 2 now shows our copy instead of the question figure (NOFIG33), with readable rows, each at its own clause: 12² = 144, 35² = 35 × 35 = 1225, 144 + 1225 = 1369, 37 × 30 = 1110, 37 × 7 = 259, 37² = 1110 + 259 = 1369, BC = d = 37, C = 2πr = π × d, C = π × 37 = 37π. The tiny in-figure captions are removed. The right-angle mark still appears only at "The right angle is across", after the check. The full Pythagoras check and the direct πd shortcut are kept.
- [should] ¶12–13 C = πd and the traps: **fixed**. Now: "The formula is two pi r. Two r is the diameter, so two pi r is pi times the diameter. We already know the diameter, so let's use it directly." The "simpler way" verdict is gone. The traps have their own rows at their own clauses: "2π × 37 = 74π: d used as r" (at "two pi times thirty-seven gives") and "π × 18.5 = 18.5π: the 2 is missing" (at "Pi times eighteen and a half"). Each is crossed out right after.
- Teaching check: converse of Pythagoras ("three sides given → check Pythagoras → a right angle across from the longest side") is used and is new here. The script already says "This is new…". **added**: the general statement plus a 5-12-13 second case (4 sentences, last paragraph of slide 2).

### #270 solve-geo33-g091
- [should] ¶5/8–10: **fixed**. ¶5: "We need the combined share of one alpha sector and one beta sector. We don't need either angle on its own." ¶8 adds "And the sum is all we need." ¶9 drops "take out the common factor". It now says: "The circle is made of five alpha plus beta pairs, all the same. So five times alpha plus beta is three hundred sixty. Now divide both sides by five." The 30+42 and 12+60 examples are kept, with "Both pairs add up to seventy-two."
- [must] ¶11–13 target colouring and split: **fixed**. The question reading is now its own slide. The work slide shows our copy only (NOFIG33), at a bigger size, with readable rows: S = πr², S = π·(√35)² = 35π, 5α + 5β = 360°, 5(α + β) = 360°, α + β = 360° ÷ 5 = 72°, 72°/360° = 1/5, then (1/5) × 35π = 35π ÷ 5 = 7π. Each row appears at its own clause. The five equal α+β pairs are drawn as alternating arcs with bold boundary radii, shown at "five alpha plus beta pairs". At "The two shaded sectors are exactly one", the whole-disk teal tint is faded (dim), and only the requested pair is tinted red with its 72°.
- Teaching check: "find the combination you need, not each unknown" is taught here (one equation, two unknowns, sum suffices). **Not needed.**

### #271 solve-geo33-g092
- [must] ¶8–12 boards: **fixed**. The video now has 3 slides.
  - Slide 1 (question figure kept): our copy is smaller, and the readable rows are above it: C = 2π·6 = 12π, then "half the circle: ∠A = 180° ✗".
  - Slide 2 "The triangle of centers" (NOFIG33): an enlarged clean copy of the three circles, with the triangle of centres and the radii 6/14/15 at their words. Ten rows, each at its own clause: AB = 6+14 = 20, AC = 6+15 = 21, BC = 14+15 = 29, 20²+21² = 29²?, 20² = 400, 21² = 441, 400+441 = 841, 29×30 = 870, 29² = 870−29 = 841, ∠A = 90°.
  - Slide 3 "Three quarters of the circle" (NOFIG33): circle A alone, big, in the same orientation (the radii point to B and to C, with the right angle). The unwanted quarter arc is teal ¼, and the highlighted long arc stays orange with ¾. The rows are 90°/360° = 1/4, then "highlighted arc: 3/4 of 12π", then 12π ÷ 4 = 3π, then 3 × 3π = 9π, each at its clause.
- [should] ¶5–6: **fixed**. "Sharp-eyed students" is gone. Now: "We can also cross out choice number four, six pi… The highlighted arc's angle at A is three hundred sixty minus the triangle's angle at A. For the arc to be exactly half, that triangle angle would have to be one hundred eighty. But an angle of a triangle is always less than one hundred eighty. So the highlighted arc is more than half." ¶6: "To choose between choice number two and choice number three, let's find the angle. If you're ever out of time at this point, guess one of the two." It no longer claims that no quick idea exists.
- Teaching check: the centre distance of touching circles (sum of radii) is already taught (#267). **Not needed.**

### #272 geo-093
- [should] ¶1/4–5: **fixed**.
  - ¶1 is now "…Now let's use these circle rules in some more involved questions." The "Circles, the advanced level." fragment is gone.
  - ¶2 drops the exam-position promise ("the kind that come near the end of the section"). It now says "The new questions just combine them in more steps."
  - ¶4: "When a length depends on the radius, we'll write it using r." The board item says the same.
  - ¶5 names the methods in the vocabulary: "In the math way, we'll sometimes stop halfway and look at the choices. With plugging in numbers, we put a number instead of a letter. And with estimation, we rule out choices by their size." There are three board rows (The math way / Plugging in numbers / Estimation), each shown at its clause.
- Teaching check: a roadmap only. **Not needed.**

### #273 solve-geo33-g094
- [must] ¶16–20 partial-answer scope: **fixed**. Now: "In this question the triangle is exactly thirty-six. We take away a sector, a quarter of a circle with radius six. Its area is some number times pi. So here the answer must be thirty-six, minus some number of pi." Each choice is compared in that context, and each gets its own row with ✗, shown at its clause:
  - 18π − 18: "the π part is added, and only eighteen is taken away";
  - 18 − 9π: "our triangle is thirty-six, not eighteen";
  - 72 − 9π: "Seventy-two is twelve times six, with no dividing by two".
  "Pi in the wrong place" as a general rule is gone. The full sector calculation and the estimation bounds are kept as confirmations.
- [must] ¶25 "by eye < 18": **fixed** (removed). Now: "The shaded part is only a piece of the triangle. So the shaded area is more than zero, and less than thirty-six." Row: 0 < shaded < 36. ¶30 no longer says "just like the shaded part we see". Now: "That's inside our range, more than zero and less than thirty-six." ¶31: "Here the two bounds, zero and thirty-six, were enough."
- [must] ¶14/21–23/26–30 boards: **fixed**.
  - Slide 1: the 6s are each written at their own clause (OC, CB, AC). The rows under the copy are AB = 6+6 = 12, then S = (base × height) ÷ 2, then 12 × 6 = 72, then 72 ÷ 2 = 36.
  - Slides 2–3 (NOFIG33): our copy is on the left, and there are readable rows.
  - Slide 2 rows: triangle = 36; shaded = 36 − (a number)·π; the three choice rows; circle π·6² = 36π; 90°/360° = 1/4; sector (1/4) × 36π = 9π; shaded = 36 − 9π. Each is separate.
  - Slide 3 rows: triangle = 36 (from the math way); 0 < shaded < 36; 3 < π < 4; 27 < 9π < 36; then each choice with its decisive bound, shown as discussed, and crossed out right away: 18−9π < 18−27 < 0 ✗; 18π−18 > 54−18 = 36 ✗; 72−9π > 72−36 = 36 ✗; 0 < 36−9π < 9 ✓.
  - Estimation now says "From the math way, we already know the triangle is thirty-six." The 36 is the shared setup, not something re-derived.
- [should] ¶3–4/12–13/24/31 wording: **fixed**.
  - "Shaded areas." and "scheme" are gone. Now: "Let's start with the math way… So first we decide which area to subtract from which."
  - "Best way / don't work for nothing / no time on the exam" is gone. Now: "The base A B, twelve, and its height O C, six, are already known. So let's use them directly."
  - "Some students find the two legs… We don't need them here, because we already have a base and its height."
  - "The automatic construction" became "a useful construction".
  - "One of the last questions in the section" and "card up your sleeve" are gone.
  All three methods are kept.
- Teaching check: subtracting areas, partial calculation and bounds with 3 < π < 4 are all taught in this video. **Not needed.**
- Layout (coordinator, after merge): the math_check layout check showed rows on slide 1 running into the choices. Slide 1 now ends at "So A B is six plus six, twelve." From "Now the triangle's area" on, a new slide "The triangle's area" takes over (same sidebar, question figure hidden). It shows a clean copy with the 6/6/6 labels and a carry row `AB = 12, OC = 6` at "are already known", then the area rows. The Method 2/3 slides are now slides 3 and 4.

### #274 solve-geo33-g095
- [should] ¶2–7/11: **fixed**.
  - "Scheme" became "We need to decide which area to subtract from which."
  - "Let's solve it the math way." is said aloud.
  - "Hope the solution shows itself" became "So let's add the known lengths, and the radius to each touching point. That will give us a right triangle to work with."
  - "Automatic / most basic construction" became "So let's draw the radius from O to D… A radius to a touching point is perpendicular to the tangent, so we mark the right angle at D."
  - "There's no need" became "here there's a quicker way".
  The ODC − sector DOE decomposition, the gold-triangle shortcut and the clean enlarged ODC (same orientation) are kept.
- [must] ¶14/18–20 boards: **fixed**. The video now has 3 slides. Slides 2 and 3 show the enlarged triangle ODC on the left (NOFIG33), with readable rows.
  - Slide 2 rows: OC = 4+4 = 8; S = (leg × leg) ÷ 2; OC = 2 × OD: a gold triangle; DC = 4√3; 4 × 4√3 = 16√3; 16√3 ÷ 2 = 8√3.
  - Slide 3 is a fresh copy with OD 4, OE 4, EC 4, 4√3, 30° and 60° carried over. Its rows: triangle = 8√3; shaded = 8√3 − (a number)·π; circle π·4² = 16π; 60°/360° = 1/6; sector (1/6) × 16π = 16π/6; 16π/6 = 8π/3; shaded = 8√3 − 8π/3.
  Each row appears at its clause. At the answer, the orange sector is cut out (white) and only the shaded part stays tinted, so no leftover sector tint. The partial check is scoped: "Here the triangle is eight root three. We take away a sector of this circle, so its area is some number of pi." The "two remain, so we continue" step is kept.
- Teaching check: the gold-triangle recognition (hypotenuse = 2 × leg) is taught in topic 31, and a short reminder is here. **Not needed.**

### #275 solve-geo33-g096
- [must] ¶20 the three equal arcs: **fixed**. The estimation slide now uses a clean semicircle (no triangle). Two NEW dashed helper radii KU and KV are drawn and labelled, with 60° at K for each of the three sectors. The speech says: "Three times sixty is a hundred eighty, so each sector has sixty degrees at K. These are new lines, not K M and K N. Each small triangle has two radii and a sixty-degree angle between them, so it's equilateral." The chords are 1 and the arcs are > 1.
- [must] ¶27 the radius cancelling: **fixed**. Now: "Here, changing r scales all the lengths together, while the angles stay the same. So the two perimeters get the same multiplier, and their ratio stays fixed. It doesn't depend on r. But choice number two and choice number four still change when r changes. So they're out." The general "the radius must cancel / any choice with r is out at first glance" is gone. ¶28 is scoped to "this kind of comparison, the same kind of thing in one shape". The doubled-figure demo and the area/perimeter contrast are kept. This part is named aloud as a new method, **Method 4 · Understanding: the scale** ("Now let's look at choices two and four by understanding").
- [must] ¶10/14/16 board and prompter: **board fixed; prompter → Needs Claude: display** (below).
  - Algebra (NOFIG33): rows for the triangle (3r), arc 2πr ÷ 2 = πr, diameter 2r, semicircle πr + 2r, then (πr+2r)/(3r), = r(π+2)/(3r), = (π+2)/3. These are stacked fractions, so the whole denominator is grouped, and each row is at its clause (factor, cancel, result).
  - Plugging in is now two slides. On the r = 1 slide the figure shows 1/1/1/π/2, with rows: r = 1; triangle 3; semicircle π+2; ratio (π+2)/3; choice 1 π/3 ✗; choices 2, 3, 4 all (π+2)/3.
  - The r = 2 slide is a fresh figure labelled 2/2/2/2π/4, with rows: r = 2; triangle 2+2+2 = 6; semicircle 2π+4; ratio (2π+4)/6, then = (π+2)/3; choice 2 (π+2)/(3·2) = (π+2)/6 ✗; choice 4 2(π+2)/3 ✗. The choice 2 and choice 4 mismatches are written.
  - Speech: "pi plus two over three" was reworded to "pi plus two, over three" or "…, all over three".
- [should] ¶11/15/21–23: **fixed**.
  - "The way I recommend for almost everyone" became "Now let's plug in numbers."
  - "One isn't a good number" became "So r equals one ruled out one choice, but three remain. To break the tie, let's try another easy number, r equals two." The ordinary r = 1 trial, then the adaptive r = 2, are kept.
  - '1+' / '5+' / "five plus over three" became 'each arc > 1', 'curved part > 3', 'semicircle > 3 + 2 = 5', 'ratio > 5/3'. The speech says "more than five thirds", and choice 1 is π/3 < 4/3 ✗.
  - The opening drops "common at the end of the section". It names all four methods.
  All original methods are kept.
- Teaching check: "arc longer than its chord" and "a ratio of two lengths of one shape doesn't change under scaling" are used. The scale idea is now taught with its condition and a doubled example. **Not needed beyond the fix.**
- Needs Claude: display (prompter grouping, unrecorded lesson):
  - 2.7 "Pi r plus two r, over three r." → (πr + 2r)/(3r)
  - 2.7 "That gives r times pi plus two, all over three r." → r(π + 2)/(3r)
  - 2.7, 3.3, 3.4, 4.2, 4.4, 6.6 "pi plus two, over three" → (π + 2)/3
  - 4.2 "two pi plus four, over six" → (2π + 4)/6
  - 4.3 "pi plus two, over three r" → (π + 2)/(3r); "pi plus two, over six" → (π + 2)/6
  - 4.3 "r times pi plus two, all over three" → r(π + 2)/3
  - 6.1 "pi plus two, over six / over nine" → (π + 2)/6, (π + 2)/9
  - 6.3 "from pi plus two to two pi plus four" → π + 2, 2π + 4 (no fraction)

### #276 solve-geo33-g097
- [must] ¶6/9–11 midpoint orientation: **fixed**. The question slide has a new paragraph with a small figure (the inner square in another position, orange, then turned into the drawn position, teal): "Let's check one thing first. The corners of P Q R S are on the circle, but the question doesn't say where. We can turn the small square inside the circle. Its corners stay on the circle, so its size doesn't change. So let's turn it until its corners are at the points where the circle touches the big square, as in the figure." The symmetry method opens with "We use the turned position again." The corner silver triangle and the eight-triangle partition are now justified. The diagonal-formula route is kept, and it needs no turning.
- [should] ¶4/7/9: **fixed**.
  - Scale scope: "If we make this whole figure bigger, every length grows by the same factor. So both areas grow by the same factor, and their ratio stays the same."
  - "That's possible, but it's a bit long" became "There's another way too, with the whole small square."
  - Method 2 is named aloud: "Now let's solve it by understanding, with symmetry."
  - Both whole diagonals now have full-span dimension lines with end ticks and the label 2 (QS at "Look at the big square's side", PR at the diagonal step). There is no label beside a half-diagonal.
  - At the switch to the whole inner square, the corner silver-triangle tint and its 1/1/√2 labels are faded out.
  - Slides 2–3 (NOFIG33) have readable rows: r = 1; side LM = 2; KLMN 2 × 2 = 4; side PQ = √2; PQRS (√2)² = 2; diagonals PR = QS = 2; PQRS (2×2)/2 = 2; 2/4 = 1/2. The symmetry rows are "8 equal triangles", "PQRS: 4 of them", 4/8 = 1/2.
- Teaching check: the square-in-circle-in-square ratio is taught as a reusable fact in the next lesson, geo-097-after. **Not needed here.**

### #277 geo-097-after  (pairs: p_geo-097-after.py)
- [should] ¶2–3/6/11–14 conditions: **fixed**. Each arrangement now names its conditions: "a circle inside a square, touching all four sides; a square inside the circle, with its four corners on the circle" (and the reverse for circle, square, circle); triangle: "both triangles must be equilateral … touching all three sides … three corners on the circle" (board: "Both triangles equilateral"). ¶12 says "four times the inner area". The square partition and the triangle are described as the result of a rotation ("If it's drawn turned another way, we can rotate it … Turning it doesn't change its size"; "The small triangle in this picture is already turned upside down…").
- [must] ¶5/8–9 boards: **fixed**. Square case: radius 1, outer side 2, inner side √2 are three layers at their clauses (was one). Circle case: diagonal line drawn at "Now look at the square's diagonal", 2√2 at "So the diagonal is two root two", big radius √2 in its own paragraph; areas split into "Small: π·1² = π" and "Big: π·(√2)² = 2π" at their clauses. Scaling tied to the known rule ("Every length is root two times bigger. So the area is root two squared times bigger, which is two."). The length/area factor recap moved to its own slide "Length factor, area factor" with labelled rows per arrangement (square-case √2 no longer sits on the triangle slide). Prompter display of "root two times the inner side" → **needs Claude: display** (see below).
- [should] ¶1/4/16: **fixed**. "three useful arrangements"; exam-position/frequency claims removed (¶1, ¶4 now "when you see this arrangement … you already know the ratio"); close states what to remember: "the outer area over the inner area. They are two, two, and four. Take a moment to memorize this." (+ board row).
- Needs Claude: display — 2.4 "So the outer side is root two times the inner side." → "outer side = √2 × inner side"; 3.5 "So the outer radius is root two times the inner radius." → "outer radius = √2 × inner radius"; 3.6 "root two squared times bigger" → "(√2)² times bigger".
- Teaching check: length factor vs area factor (area factor = length factor²) → already a reminder from solve-geo31-g018; now stated generally on its own slide (part of the fix, no extra addition).

### #278 solve-geo33-g098  (pairs: p_solve-geo33-g098.py + p_f8place.py)
- [must] ¶4–7 board: **fixed**. Slide 1 is now the question + one reaction line; the construction moves to a new slide (same sidebar, NOFIG33) with our copy enlarged on the left and readable rows on the right: ∠AOF = 2×28° = 56°, ∠FOD = 2×57° = 114°, ∠AOD = 56° + 114° = 170°, ∠AOG + ∠EOD = 170° − 80° = 90°, each at its clause; the 56°/114° labels on the figure appear only when said (were with the radius). After B and C are used, a "focus" layer fades the B/C chords and redraws a clean circle with OA, OG, OE, OD (OF dashed), the two end arcs teal and the 80° middle clearly identifiable; then the two end sectors are tinted — the result is the SUM of the two end angles. (Clean in-place redraw rather than a second enlarged copy: same orientation, nothing else moves.)
- [should] ¶2/8–12: **fixed**. "we need its central angle … let's draw radii that give us central angles" (no "must have" claim). Sliding demo: "Now let's understand why the sum is enough … The givens don't decide it", each picture captioned "one possible position" / "another possible position". Final slide (NOFIG33) has a small clean two-arc reference ("the two end arcs: 90° together") beside the rows 90/360 = 1/4 and 1/4·16π = 16π/4 = 4π (split). The math way is named at the start; the Understanding transition is spoken.
- Teaching check: "can't find each part → find the sum" → already taught (closing line kept).

### #279 solve-geo33-g099  (pairs: p_solve-geo33-g099.py + p_f8place.py)
- [must] ¶7–9 premature 27π/36: **fixed**. Method 1 now ends its first slide at the square; a new slide "Three pieces" (NOFIG33) shows a clean copy: the three pieces shaded first with NO numbers ("The left three-quarter circle, the square, and the right three-quarter circle. Some people call each three-quarter circle a Pac-Man."), then rows circle π·6² = 36π, a quarter 36π÷4 = 9π, three quarters 3×9π = 27π (27π labels appear then), square 6² = 36 (36 label then), 27π + 36 + 27π = 54π + 36.
- [must] ¶13–14 overlap route: **fixed**. Rows at their clauses: 36π+36π = 72π, quarter 9π, triangle (6×6)/2 = 18, one piece 9π − 18, overlap 2(9π − 18) = 18π − 36 ("we double the whole difference"), 72π − (18π − 36), = 72π − 18π + 36, = 54π + 36. Spoken bracket cue replaced by "minus the overlap, eighteen pi minus thirty-six" (W5). Slide NOFIG33, figure on the left.
- [should] ¶2/16–18: **fixed**. ¶2 now "no single familiar shape around it is given, so we can't take one big area and subtract a piece". Estimation: OP drawn dashed, "OP is the diagonal of the square, so it's longer than the side, six. Every point of the right half of circle P is at least that far from O. So that half is outside circle O." Then 18π + a middle piece → union > 54π. Added the 27π vs 36 comparison (27π > 81 > 36, so 27π + 36 < 54π) before crossing 1 and 4. Close: "This bound doesn't separate them, so this estimate leaves two choices." Method names said ("Let's start with the math way", "the math way again", "Now let's estimate").
- Teaching check: union = A + B − overlap → already explained in method 2 ("counted twice, take it away once"); not needed.

### #280 solve-geo33-g100  (pairs: p_solve-geo33-g100.py; optional tc_solve-geo33-g100.py)
- [should] ¶2/5–8: **fixed**. "We'll solve it in two different ways, the math way … then with an estimate"; "Let's start with the math way"; "Now let's estimate". "wasn't bad at all" removed. EF = AB explained: "E F and A B both measure the perpendicular distance between the same two parallel sides, A D and B C. So A B is also eight." Estimate board split: square 8·8 = 64, circle < 64, 8·BC < 64, BC < 64 ÷ 8 = 8 at their clauses; the added square is labelled "helper square (dashed)" and spoken as "our helper, not part of the rectangle". The 3π/4π/8π exclusions unchanged.
- Teaching check: circumscribed square as an upper bound for any circle (area < d²) → **not added** (the estimate is already explained with its reason in the fix; kept the topic to three additions).

### #281 solve-geo33-g101  (pairs: p_solve-geo33-g101.py + p_f8place.py)
- [should] ¶2–5: **fixed**. New layer draws a small radius r (teal) and a big radius R (orange) on actual radius segments at "let's call the big one capital R", separate from the AC/AB diameters. "Let's write capital R in terms of small r, so our equation has just one unknown." (no "two unknowns are too many"/"adding is easier"). ¶5: "We divide each term by two. Two r over two is r, and ten over two is five." Board: R = (2r+10)÷2, = 2r÷2 + 10÷2, = r + 5 (two layers). Both methods kept.
- [must] ¶8–9 boards: **fixed**. Slides 2–3 are NOFIG33 with readable rows. Slide 2: So far …, π(r+5)² − πr² = 65π, (r+5)² − r² = 65, (a+b)² = a² + 2ab + b², (r+5)² = r² + 2·5·r + 25, = r² + 10r + 25, r² + 10r + 25 − r² = 65, 10r + 25 = 65, 10r = 65 − 25 = 40, r = 40 ÷ 10 = 4, each at its clause. Trials: r = 3: AC = 6, AB = 16, R = 8, big π·8² = 64π, small π·3² = 9π, 64π − 9π = 55π; r = 4: AC = 8, AB = 18, R = 9, 81π, 16π, 81π − 16π = 65π — two columns, each row at its clause.
- [must] ¶11–13 monotonicity: **fixed**. "Here the shaded area grows when r grows. C B stays ten, so capital R is always r plus five. And in the first way we saw that the shaded area is ten r plus twenty-five, times pi. So a bigger r always gives a bigger area." (row: shaded = (10r+25)π: grows with r). Scope: "With these four choices in order, and an area that grows with r, two tries are enough." 3 then 4 kept.
- Teaching check: monotone plugging-in (middle choice, discard one side) → taught here as part of the fix; nothing more.
- Layout (coordinator, after merge): the two trials did not fit on one board. The r = 4 trial now has its own slide "Now try four" (same sidebar). It opens with "Three gave fifty-five pi, too small, so two and three are out." There, a carry row `r = 3: 55π, too small` appears and choices two and three are crossed again.

### #282 solve-geo33-g102  (pairs: p_solve-geo33-g102.py + p_f8place.py)
- [must] ¶4–6/13–15 views: **fixed**. "the circle near B, whose center is O" (and the enlarged slide title "The circle near B, enlarged"). The plugging-in example has its own clean figure (equilateral triangle, same orientation, circle through B with D on AB and E on BC, DOE = 120° computed exactly), no 4θ or isosceles labels: 60° marks, then rows 4θ = 60°, θ = 60° ÷ 4 = 15°, central 2×60° = 120°, r = 1. The same figure (with 120°, r = 1, "arc = 2π/3") is the reference on the choice-check slide. Both slides NOFIG33.
- [must] ¶3/6/15 reveals: **fixed**. Base angles split into angle B = angle C, B + C = 180° − 4θ, each (180° − 4θ) ÷ 2, = 90° − 2θ (four layers at clauses); central 2(90° − 2θ) and = 180° − 4θ split, with the spoken step "Two times ninety is a hundred eighty, and two times two theta is four theta"; trial: C = 2π·1 = 2π, 120 ÷ 360 = 1/3, arc = 1/3·2π = 2π/3 as separate rows. Prompter "four theta"/"two theta" → **needs Claude: display**.
- [should] ¶12–16: **fixed**. "Now let's use plugging in numbers." (no tangled/shorter verdict). Choice 4: "Now the other three are out, so choice number four is the only one left. Let's still check it." Example, range check and r = 1 kept; no extra trials.
- Needs Claude: display — 1.1/1.3/2.1/2.2/3.x/4.2 "four theta" → "4θ", "two theta" → "2θ", "ninety minus two theta" → "90 − 2θ", "a hundred eighty minus four theta" → "180 − 4θ", "theta over forty-five" → "θ/45".
- Teaching check: not needed (plugging in numbers for letter answers explained with its why in ¶12).

### #283 r26-t33-more-tools  (pairs: p_r26-t33-more-tools.py)
- [must] ¶10–13 boards: **fixed**. Rows Circle: π·6² = 36π, Sector: 36π÷3 = 12π (12π label on the sector only then); Equilateral: a²√3/4, then 6²√3/4 = 36√3/4, then = 9√3 (9√3 labels on the cut-outs at that clause). Shared region moved to its own slide "The shared region in numbers" with a clean figure: right piece shaded, then BOTH pieces shaded at "The shared region is two pieces"; rows One piece 12π − 9√3, Two pieces 2(12π − 9√3) ("we double the whole difference"), = 24π − 18√3.
- [should] ¶2/4–6: **fixed**. "First, let's look at two equal circles, where each one passes through the center of the other." "all five segments". New line + row "This needs both conditions, equal circles, and each center on the other circle. Equal circles that are farther apart give a different angle, like the ninety degrees in the union question." Second small case added: r = 2 → sector 4π/3, triangle √3, region 2(4π/3 − √3) = 8π/3 − 2√3 (checked = (24π−18√3)/9). Rhombus argument kept. Intro exam-position claim softened.
- [must] ¶17–23 ring: **fixed**. "Circles with the same center are called concentric."; final rule "So when two circles have the same center, and a chord of the big circle touches the small circle, the ring is pi times half the chord, squared." (+ row "Same center, a chord of the big circle touching the small one:"). Pythagoras rows r² + h² = R², then "Now subtract r squared from both sides" R² − r² = h². A "back" layer fades the orange triangle and re-shows the whole ring before Ring = π(R² − r²) = πh². Chord 10 → h = 10÷2 = 5, Ring = π·5² = 25π split. Each example ring now shows its chord "10"; 169π / 144π rows, then 169π − 144π = 25π; (5√2)² = 50 then 50π − 25π = 25π; the r = 0 case is "the limiting picture, where the small circle has shrunk to a single point" (caption "small circle: a point").
- Teaching check: both tools are new here and now taught with why + second case; nothing more.

### #284 solve-q-r26-t33-04  (pairs: p_solve-q-r26-t33-04.py)
- [must] ¶5/7/9–10 working: **fixed**. Sector: 60° ÷ 360° = 1/6, circle π·6² = 36π, sector 36π ÷ 6 = 6π (three layers at clauses). Triangle slide is NOFIG33 (figure left, rows right): base angles 180° − 60° = 120°, 120° ÷ 2 = 60° ("Half of a hundred twenty is sixty"), equilateral a²√3/4, 6²√3/4 = 36√3/4, = 9√3; height route: base halves 6 ÷ 2 = 3 (two "3" labels), height 3√3, (6 × 3√3)/2 = 9√3, then segment = 6π − 9√3. Clean enlarged sector copy and both area approaches kept.
- [must] ¶16 scope: **fixed**. "So when a shaded region is a small segment, between a chord and its short arc, with a central angle below a hundred eighty, think small sector minus triangle."
- [should] ¶2/6/12–15: **fixed**. "Let's use the math way … let's decide which area to subtract." Partial-choice check is contextual: "Here the shaded area is this sector, six pi, minus the triangle … They don't use this sector, so both are out." Root comparison revealed in three rows: 9 = √81, 9√3 = √243, √243 > √144 = 12, then 3π − 9√3 < 0.
- Teaching check: segment = sector − triangle → taught in r26-t33-more-tools; not needed.

### #285 solve-q-r26-t33-05  (pairs: p_solve-q-r26-t33-05.py)
- [must] ¶14–16 why/scope: **fixed**. New slide "Why the short formula works" (NOFIG33, clean letter figure): AB = R + r, AE = R − r, DC² = (R+r)² − (R−r)², (R+r)² = R² + 2Rr + r², (R−r)² = R² − 2Rr + r², DC² = 2Rr + 2Rr = 4Rr, DC = √(4Rr) = 2√(Rr) (positive length), 2√(8·2) = 2√16 = 8 — each at its clause, brief. Scope stated and written: "Two circles touch each other from the outside, and D C is the piece of a common tangent line between its two touching points." Not touching: "but there's still a common tangent like this, cut off the same right triangle. Its hypotenuse is the distance between the centers. And if one circle is inside the other, there's no such tangent at all." Both 8/2 and 9/4 examples and the triple shortcut kept.
- [must] ¶10/13/15 boards: **fixed**. Slide 2 NOFIG33 with rows: ED = BC = 2, EB = DC, AE = 8 − 2 = 6, 6, 8, 10: BE = 8, 10² = 100, 6² = 36, BE² = 100 − 36 = 64, BE = √64 = 8 ("we take the positive root"), DC = BE = 8. Trap: 136 / 2√34 layer, then a separate "2√34 > 10 ✗" layer with "because root thirty-four is more than five". The 9/4 check has its own matching figure (radii 9 and 4, AB 13, AE 5, DC 12) with rows AB = 9 + 4 = 13, AE = 9 − 4 = 5, 5, 12, 13: DC = 12, 2√(9·4) = 2√36 = 12 ✓.
- [should] ¶3/5–8: **fixed**. "Let's draw each radius to its touching point, A D and B C. That gives two right angles…"; "let's also join the centers"; "D C is perpendicular to both parallel sides, so it's the distance between them." The math way named; the formula has its own recap slide.
- Teaching check: common external tangent 2√(Rr) → taught here with why (the fix); nothing more.
