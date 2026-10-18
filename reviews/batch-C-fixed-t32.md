# Batch C, topic 32: fixes applied (Claude, 18 Oct 2026)

Source review: `reviews/batch-C.md` (Codex). Scope: topic 32, lessons #211–#247 (geo-042 … solve-q-r26-t32-07), 37 videos. Topic 33 was fixed in parallel by another agent and is not covered here.

## Result

- **Must findings: 58 of 58 handled.**
  - 56 were fixed in the source.
  - 2 are prompter-only and were verified: the "all four halves" display in #213 and #215 had already been fixed by the coordinator in `reading_studio.py`.
- **Should findings: 56 of 56 fixed.**
- **0 parked.**
- **0 skipped.** All 37 lessons were on `video_status.py --list record`, with no take in `~/Documents/Course.recordings/_reading/<id>/`. I checked this at the start, and nothing in my scope was recorded during the job.
- **#228 geo-056 was READY** and was not changed.
- **First five delivered early.** At the coordinator's request, #211–#215 were finished first, together with their W20 check, and reported as "first five done".

Canonical source edited: `studio-build/math_patches/_ai_vis_t32.py`. The `ai_scripts/*.json` files were regenerated from it.

Not edited: `_method_visuals.py`, `_camera_parts.py`, `_math_vars_display.py`, `reading_studio.py`, the display registry, other topics, and `_ai_vis_t33.py`.

New spec helpers in `_ai_vis_t32.py`:
- `wipe`: a white rectangle that hides an old label or template.
- `wipep`: a white polygon that hides a piece that was cut and moved.
- `NOFIG32`: (video, slide) pairs that give the working the whole board, as `NOFIG31` did in batch B. Used for g062 slide 3 and t32-07 slide 2.
- Working rows for question slides now sit in a column to the right of a narrower copy, at x = 1350. A column under the copy was being shrunk by the renderer's fit-to-height (scale down to 0.74) whenever the stem was tall, which made rows tiny and pushed them over the choices.

Kept: every method, her voice (short sentences, "choice number N", numbers as words, no symbols, no "!" or labels), the fonts, the dark-blue pen, and the method titles "Method N · core".

Structure changes (all unrecorded):
- **geo-042 part 1:** the angle-sum examples are now an x slide and a y slide, so `CAMERA_SPLIT` part 2 starts at slide 8.
- **geo-047:** two new slides, "Equal or perpendicular diagonals" and "Forty-five, sixty, a hundred fifty".
- **geo-050:** a new slide, "Area: two examples".
- **g055:** method 2 is now two slides.
- **g058:** a new slide, "The perimeter".
- **g061:** a new slide, "The triangle ABP".
- **g062:** now 5 slides: the main diagonal / Pythagoras / a square minus a square / the area / other ways.
- **g063:** a new slide, "The gold triangle".
- **r26-t32-perimeter:** now 5 slides.
- **t32-07:** a new slide, "Squaring a sum".
- **Paragraphs added or split** in most lessons: one step per sentence, each with its own board row.

## Per lesson

### #211 geo-042 (camera, part 1)
- [must] Non-example "four sides, not closed": **fixed**. It is now an open chain of 4 red segments with dots at the two ends and a "gap" label. The caption reads "4 sides, not closed ✗", and the speech says "its ends don't meet, so it isn't closed".
- [must] Bundled calculations: **fixed**. Each step is a separate hand-written row at its own clause, to the right of the figure and below the face bubble:
  - 80 + 95 = 175 → 175 + 110 = 285 → x = 360 − 285 → 360 − 280 = 80 → 80 − 5 = 75.
  - 75 goes on the figure only at "so x is seventy-five".
  - The y example is on its own slide (90 + 90 = 180 → 180 + 120 = 300 → y = 360 − 300 → y = 60).
  - So is the 240 example (30 + 40 = 70 → 70 + 50 = 120 → 360 − 120 → = 240).
  - The "all four angles add to 360" reason is kept.
- [should] "Kingdom of quadrilaterals": **fixed**. It now says "So far we've finished lines, angles and triangles. Now let's look at quadrilaterals, shapes with four sides. We'll start with a general one."
- [should] Mental route for 360 − 285: **fixed**. "Let's take away two hundred eighty first. Three hundred sixty minus two hundred eighty is eighty. Then we take away five more…" Both steps are written as rows.

### #212 geo-042-2 (camera, part 2)
- [must] The kite definition: **fixed**. "A kite has two equal sides next to each other. The other two sides are equal too. In this picture, the top pair is shorter. All four sides can also be equal, as in a rhombus." The arrow label is "pull a corner", and the adjacent pairs keep their own ticks.
- [must] Tree captions: **fixed**. The speech now says "Going down a line of the tree, a shape only gains properties. So a square has all the rectangle rules. It also has all the rhombus rules. But knowing that a shape is a rectangle doesn't guarantee that it's a square."
  - The captions are "square → rectangle rules + rhombus rules" and "rectangle → not necessarily a square".
  - The tree labels are "down a line: more properties" and "rectangle: not necessarily a square", with the R–S edge traced. They no longer mention page position or the trapezoid branch.
- [should] The changed and kept conditions are named:
  - Stretch: "angles still right angles, now only the opposite sides are equal".
  - Squash: "opposite sides stay parallel and equal, angles not right angles".
  - Shorten: "the two longer sides… opposite sides stay parallel".
  - Kite: adjacent equal pairs.
  - Trapezoid: "move its two top corners toward each other… top and bottom stay parallel, the other two sides are no longer parallel".
  - The family slide gained one paragraph.

### #213 geo-043
- [must] "all 4/2" in the prompter: **verified**. It already displays "all four halves" (coordinator's reading_studio fix). The text is unchanged.
- [must] "If only one side grows…": **fixed**. "For a rectangle, if we double its length but keep its width the same, the area only doubles. Three by three is nine, and six by three is eighteen. Both sides must double…" A new figure `f2sq7` shows a 3×3 grid (9) next to a 6×3 grid (18).
- [must] The 12 label: **fixed**. The whole diagonal AC is traced, with dots at both ends, and "AC = d = 12" is written in the column at "is twelve". Each half's "6" is moved clear of the ticks.
- [must] Written working: **fixed**. Rows 6·6 = 36 and 36/2 = 18 come at their clauses, and the 18 inside the triangle appears only at "is eighteen". Then 4·18 = 72, then 12²/2 = 144/2, then "= 72", each in its own paragraph. The 10 example is 10² = 100, then 100/2 = 50.
- [should] "More crossing lines": **fixed**. "Draw a line from the right angle at B to the middle of the diagonal. That cuts the half square into two smaller silver triangles…" A construction layer is shown. At the switch, the old small triangle is faded (dim), and the legs AB and BC are outlined and ticked.
- [should] "So the formula works": **fixed**. "Every square has these four equal triangles, and a longer or shorter diagonal doesn't change that split. So the formula works for every square." The 10 example is introduced as "Let's check one more".
- [should] Recap: **fixed**. "All the properties we just checked hold for a square." The board reads "Square: all of these hold ✓" and lists the four checked properties. One spoken recap and the nudge "Take a moment to memorize this."

### #214 solve-geo32-g044
- [must] **Fixed.** The rows sit under the copy at a readable size, and the copy is narrower (w 240):
  - Method 1: S = d²/2 at "the product of the diagonals", then S = 14·14/2, then 14·14 = 196, then 196/2 = 98.
  - Method 2: s² + s² = 14², then 2s² = 196, then 2s²/2 = 196/2 ("we divide both sides by two"), then s² = 98.
  - The explanation "s squared is already the area… because the area is the side squared" is kept.
- [should] Transitions: **fixed**. "We'll solve it in two different ways. First the math way, with the diagonal formula. Then we'll use Pythagoras." / "Now let's use Pythagoras to find the area through the side."
- [should] Traps at their steps: **fixed**.
  - 196 (choice 3) is crossed at the "not the area yet, we still divide by two" step.
  - 49 (choice 1) is crossed at the side step ("the side is not half the diagonal").
  - The post-answer trap list is removed.

### #215 geo-045
- [must] "all4/2": **verified**. It displays "all four halves".
- [should] The symmetry: **fixed**. "Why are they equal? Imagine folding the rectangle down the middle, from top to bottom. The left half lands on the right half, and one diagonal lands exactly on the other." A dashed "fold here" line is drawn.
- [should] Area wording: **fixed**. "We count how many little squares are in each row, and how many rows there are. So the area is length times width… The two lengths can be different, or equal, as in a square." The board reads "S = length × width". The 8×3 grid and the 7×4 example are kept.

### #216 solve-geo32-g046
- [must] **Fixed.** At "Now the area of the whole rectangle", a new `whole` layer outlines and tints ABCD and marks BC = 5√3 and CD = 5 with the right angle. The gold triangle fades. S = 5√3 · 5 and = 25√3 are separate layers.
- [should] **Fixed.** "E lies on the diagonal B D, so B E and B D lie along the same line. So angle D B C is the same thirty as angle E B C." The 30° is shown before the 60° at D, which now has its own paragraph.
- [should] **Fixed.** 180° − 120° = 60° and 60° ÷ 2 = 30° are separate rows, and the two 30° marks come at "So angle E B C is thirty".
- [should] **Fixed.** The tip is now a counterexample: "If you're not sure whether a diagonal rule is guaranteed… It's still a rectangle… So we can't assume either one in a rectangle."

### #217 geo-047
- [must] Old rectangle: **fixed**. The parallelogram layer first fades the template (dim) and wipes the "rectangle" label.
- [must] Converse criteria: **fixed**. A new slide, "Equal or perpendicular diagonals", says:
  - "Both start from a shape we already know is a parallelogram."
  - Its own rectangle case (equal diagonals), with "→ rectangle".
  - Its own rhombus case (perpendicular), with "→ rhombus".
  - A red kite non-example: "perpendicular, but it isn't a parallelogram, so it isn't a rhombus".
  - Board: "If it is a parallelogram: …".
- [must] Overlapping summary: **fixed**. "A general parallelogram: the diagonals cut each other in half" now sits in the left column under the figure, and its font is not shrunk.
- [must] 45/60/150 rushed: **fixed**. A new slide has one row per case, each with its own right triangle (slanted side 8):
  - 45°: the slanted side is the hypotenuse, h = 8/√2 = 4√2, written in two rows.
  - 60°: the 30° is at the top, so the short leg is 8/2 = 4 and h = 4√3.
  - 150°: we extend CB, the adjacent angle is 180° − 150° = 30°, and h = 8/2 = 4.
- [should] The parallel-line rule: **fixed**. "Here the side A B crosses the two parallel lines through A D and B C. The angles at B and at A sit inside this U…" The U is traced. Then "C D… makes the same angles. So in this tilted example… In a rectangle, they're all ninety."
- [should] Cut and move: **fixed**. The moved piece wipes the source triangle, which is left outlined and labelled "empty", as the piece appears on the right.

### #218 solve-geo32-g048
- [must] An independent plug-in: **fixed**. "The question expects one value of x for every parallelogram… A rectangle is a parallelogram, so let's try ninety degrees at B and at C." From that: 5α = 90°, α = 18° (and the same for β). The "faster way" verdict is removed.
- [must] Rectangle copy: **fixed**. There is a new, correctly drawn rectangle `f3g48p`:
  - E is placed so that both base angles are 54° (E = (300, 93.5)), and 36° is marked at B.
  - It is labelled "a rectangle: one allowed case", and the given figure stays on the left.
  - x = 72° appears only at "which is seventy-two".
- [must] Grouping: **fixed**. The rows are x = 180° − 3α − 3β → 3α + 3β = 3(α + β) → = 3·36° = 108° → x = 180° − 108° = 72°. The speech says "We know that alpha plus beta is thirty-six. Both terms… have a factor three, so we can write them as three times that whole sum."
- [should] **Fixed.** 54° + 54° = 108° comes first, then x = 180° − 108°, then x = 72°, each a row.

### #219 solve-geo32-g049
- [must] Prompter: **fixed**. "Twenty-four times fifteen is twenty-four times ten plus twenty-four times five. Twenty-four times ten is two hundred forty. Twenty-four times five is a hundred twenty. Two hundred forty plus a hundred twenty is three hundred sixty." It displays "24 × 15 = 24 × 10 + 24 × 5. 24 × 10 = 240. …". Board rows: S = 24·15 / 24·10 = 240 / 24·5 = 120 / 240 + 120 = 360.
- [must] The whole parallelogram: **fixed**. "Now back to the whole parallelogram…", with a `whole` layer (BC = 24 and AE = 15).
- [should] **Fixed.** "A E is perpendicular to B C, so A B E is a right triangle. We can use it, with Pythagoras, to find the height." The similarity aside is removed.
- [should] **Fixed.** "Choice number four, four hundred eight, uses the slanted side seventeen instead of the height. That isn't the area formula."

### #220 solve-q-r26-t32-01
- [must] **Fixed.** "When the slanted side meets the base at thirty or at a hundred fifty degrees, the height to that base is half the slanted side. Here A B meets the line of B C at a hundred fifty, so A H is half of A B." It points to the figure.
- [should] **Fixed.** The order is now: the perpendicular would land left of B, so first extend CB, then draw the perpendicular and name its foot H.
- [should] **Fixed.** A `whole` layer covers the area step (BC = 14, AH = 5). The traps moved to their decisions:
  - 70√3 and 140 at the gold-triangle step;
  - 35 ("we don't divide by two… not a triangle") at the area step.
  - S = 14 · 5 and = 70 are separate.

### #221 geo-050
- [must] Area proof: **fixed**. "The diagonals meet at ninety degrees, and they cut each other in half… four equal right triangles… Its legs are half of one diagonal and half of the other."
  - Rows: d₁/2 · d₂/2 = d₁d₂/4 → one triangle d₁d₂/4 ÷ 2 = d₁d₂/8 → 4·d₁d₂/8 = d₁d₂/2.
  - The four quarters are tinted, then the whole outline.
  - A new slide, "Area: two examples", has a whole tinted rhombus (12 and 8): 4·6/2 = 12, 4·12 = 48, 8·12 = 96, 96/2 = 48, then 10·6 = 60 and 60/2 = 30, each at its clause.
- [should] **Fixed.** "Only if the two diagonals are equal, the rhombus is a square, like this one." A separate square figure is labelled "IF the diagonals are equal: a square". Then "Let's go back to our rhombus" before the bisection rules.
- [should] **Fixed.** "A rhombus is a parallelogram with all four sides equal." The symmetry folds now name their diagonals ("The diagonal A C is a line of symmetry… the other diagonal, B D, is a line of symmetry too").

### #222 solve-geo32-g051
- [must] **Fixed.** "What does absolute difference mean? It means the gap between the two lengths, whichever one we name first. Here that gap is fourteen."
- [must] **Fixed.** "Both equations are true. So we can add their left sides, and add their right sides…" Then "We want a alone, so we divide both sides by two", and "Now we put thirty for a in the first equation…". Rows: 2a = 60 / a = 60/2 = 30 / 30 + b = 46 / b = 46 − 30 = 16, each at its clause.
- [should] **Fixed.** The 15 label moved to the upper half AO, and the speech adds "So A O, the top half of A C, is fifteen, and O D, half of B D, is eight."

### #223 geo-052
- [must] The bow-tie: **fixed**. The second kite is now simple and turned, with its axis left to right (`f4_kw` reordered), ticks on its own adjacent pairs, and the caption "another kite, turned".
- [must] Inclusive definition:
  - "In this kite, the two pairs have different lengths. They can also be equal, and then it's a rhombus."
  - The axis is defined as "the line that joins the two corners between equal sides, here A and C… even when the kite is turned".
  - "So a kite is not necessarily symmetric along B D."
  - "does not necessarily cut…", "In this kite, the triangle on top…", "does not necessarily do that. In this kite, at B…"
  - The captions read "here: not the same" and "here: top ≠ bottom".
  - The slide and sidebar title is "Symmetric along A C" (was "Symmetric, but only one way").
- [should] **Fixed.** Rows: S_ADC = AC·BD/2 ÷ 2, then 2·S_ADC = AC·BD/2, then 10·6 = 60, 60/2 = 30, 12·8 = 96 and 96/2 = 48, each case and result at its own clause.

### #224 solve-geo32-g053
- [must] **Fixed.** "The other two sides are both five root two, so together they add a root two part, and no root three. So the perimeter is twenty plus some root two." Then: choices 2 and 4 start with ten, choice 1 has root three, so only choice 3 is left, and the full sum confirms it.
- [must] **Fixed.** "So in a kite, the main diagonal, here A C, is always a line of symmetry. The other diagonal, B D, doesn't have to be one, and here it isn't."
- [should] **Fixed.** "Remember the shortcut. To divide ten by root two, we divide ten by two, and then multiply by root two." Rows: 10/√2, then = 10/2 · √2, then = 5√2.
- [should] **Fixed.** The caption now reads "5√2 + 5√2 / only a √2 part" (scoped to this sum).

### #225 geo-054
- [must] "12×5 is60/2=30": **fixed** in the speech. "Nine plus three is twelve. Twelve times five is sixty. And sixty over two is thirty." The same for 10 + 6 = 16, 16·4 = 64, 64/2 = 32. The prompter shows separate equalities. The board has two columns of rows (setup, then each step).
- [should] **Fixed.** "Two of them are parallel, and those two are called the bases. Here they're A D and B C. The other two sides, A B and C D, are called the legs."
- [should] **Fixed.** "The two top pieces are equal… the two bottom pieces are equal… But the top pieces need not equal the bottom pieces, so the diagonals are not generally cut in half."
- [should] **Fixed.** "And in an isosceles trapezoid, alpha plus beta…", with the caption "Isosceles: opposite angles α + β = 180°". The right-triangle label is two short lines inside the orange triangle.

### #226 solve-geo32-g055
- [must] Honest method 2: **fixed**. "Now the math way, with the trapezoid area formula… For the formula, we need the bottom base too." EC = 4 comes from the area (5·EC/2 = 10, 5·EC = 20, EC = 4). Then "The two end triangles match because the trapezoid is isosceles, so B F is four too. And F E… is x." The bases are x and x + 8. No claim that the formula avoids symmetry.
- [should] **Fixed.** Method 1 (Understanding) now uses only the two equal areas: 10 + 10 = 20, 65 − 20 = 45, 5x = 45, x = 45/5 = 9. The EC = 4 working moved to method 2. Both methods are named aloud. "look how much longer" and "Same answer, but much longer" are removed.
- [should] **Fixed.** "Here a second height lets us compare the two end triangles… In general, heights often split a trapezoid into a rectangle and right triangles."
- [must] **Fixed.** Rows: (x + x + 8)·5/2 = 65 → (2x + 8)·5 = 130 → 10x + 40 = 130 → 10x = 90 → x = 90/10 = 9, with "Now divide both sides by ten". The prompter paragraph was reworded ("The sum of the bases is x plus x plus eight, which is two x plus eight. We multiply that sum by five, divide by two, and we get sixty-five"), so no detached "×5/2" appears.

### #227 solve-q-r26-t32-02
- [must] **Fixed.** Rows: 9 + 15 = 24 → S = 24·8/2 → 24/2 = 12 ("Let's halve the twenty-four first") → 12·8 = 96. The speech says "So the area is twenty-four times eight, over two". A `whole` layer tints and outlines the trapezoid.
- [should] **Fixed.** "Now we've split the trapezoid into a rectangle, A B E D, and a right triangle, D E C."

### #228 geo-056: READY (no change)

### #229 solve-geo32-g057
- [must] **Fixed.**
  - Rows: 118° + 96° + α + β = 360° → 118° + 100° = 218° → 218° − 4° = 214° → α + β = 360° − 214° = 146° → α = 146° → β = 0° ✗.
  - The impossible case has its own paragraph.
  - The optional checks 26° + 120°, 70° + 76° and 124° + 22° each have their own row, in their own column and at their own clause.
  - "In the exam you'd mark it and move on" and the not-to-scale trap are kept.
- [should] **Fixed.** "That would leave zero degrees at D, so D would no longer be a proper corner of this quadrilateral."
- [should] **Fixed.** "One hundred eighteen plus a hundred is two hundred eighteen. We added four too many, so we take away four…"

### #230 solve-geo32-g058
- [must] **Fixed.** Rows 180° − 72° = 108°, 108° − 54° = 54°, 72° + 54° = 126° and 180° − 126° = 54° come at their clauses. A new slide, "The perimeter", has a copy with every value on it and the rows AD = 4 + 9 = 13, 9 + 9 = 18, 13 + 13 = 26, 18 + 26 = 44, with the four outer edges traced.
- [should] **Fixed.** "E D is parallel to B C, and C E crosses them. Follow B C, then C E, then E D, and we get a Z." Then "The angle at E faces C D, and the angle at C faces E D. So E D equals C D."

### #231 solve-geo32-g059
- [must] **Fixed.**
  - Every pair is split into its own row, in the panel to the right of the copy: EB + 24 + EC = 50 / EB + EC = 26 / EB = EC = 13 / AC = 2·13 = 26 / triple / AB = 10.
  - Method rows: 10·24 = 240 → S_ABC = 240/2 = 120 → S_ABE = 120/2 = 60; then 10·24 = 240 → 240/4 = 60; then 24/2 = 12 → 10·12 = 120 → 120/2 = 60.
  - The roadmap names "twice by understanding and once the math way", and each method opens with its name.
- [should] **Fixed.** "Opposite triangles match in size and shape. A E D matches B E C, and A E B matches C E D. Triangles next to each other… don't have to have the same shape. But they have the same area, because B E is a median…" Then "This works because the diagonals cut each other in half, and that's true in every parallelogram." The median is marked.
- [should] **Fixed.** "Draw the line from E straight to A B, and continue it across to C D. That whole line is as long as B C… E is… halfway between A B and C D." The other half is drawn as well.

### #232 solve-geo32-g060
- [must] **Fixed.**
  - AO and OC are labelled on the left, with leaders to the half-diagonals, clear of AD.
  - At "for the whole rhombus", the whole outline is tinted.
  - Rows: S = 10·10√3/2 → 10/2 = 5 → 5·10√3 = 50√3.
  - The copy is cropped to the rhombus, and all of its text moved into rows.
- [should] **Fixed.** Each decomposition has its own sentence and layer, and the previous selection fades (dim):
  - BDA: base BD, height AO dashed, then "× 2" with BDC tinted.
  - ADC: base AC, height OD, then "× 2" with ABC.
  - Each has its own row.
- [should] **Fixed.** "Well done if you saw this" and "That's the shorter way" are removed, and the name "Insight" is kept. Rows: 10² = 100 → one: 100√3/4 → two: 200√3/4 → = 50√3.

### #233 solve-geo32-g061
- [must] **Fixed.**
  - The given copy marks are redrawn (the right angles at B and A are inside the square).
  - A new slide shows triangle ABP enlarged, in the same orientation and with the same labels.
  - It has ticks on BA and BP, the 30° at B, and α at A and P, and 75° appears at "so alpha is seventy-five".
  - A dashed stub of AD shows the square's corner, so BAP (α = 75°) and PAD (x, 15° in red) are clearly separate.
- [must] **Fixed.** "Subtract thirty from both sides, and two alpha is one hundred fifty. Divide by two, so alpha is seventy-five." Rows: 30° + α + α = 180° / 2α = 150° / α = 150°/2 = 75° / ∠PAD = 90° − 75° = 15°, the last one at its own clause.
- [should] **Fixed.** "We need its equal sides and its ninety-degree corners. P is not the point where the diagonals meet, so we can't treat it as the centre, and we won't use the diagonals." The shared-tick explanation is kept.

### #234 solve-geo32-g062
- [must] Difference of squares: **fixed** (taught here). A new slide, "A square minus a square", uses NOFIG so the working gets the whole board:
  - Why: "Multiply out the product of a minus b and a plus b… The two middle terms cancel."
  - Checks: 5² − 3² = 16 against (5 − 3)(5 + 3), and 4² − 1² = 15 against 3·5.
  - The trap: "It's not seventeen minus fifteen, squared. That would be only four."
  - The finish: 2·32 = 64, AO = √64 = 8.
  - The triple shortcut stays first.
- [must] **Fixed.** "the main diagonal, A C" and "the other diagonal, B D" (no long or short).
- [must] **Fixed.** "We cannot assume that A O equals O C. The main diagonal cuts B D in half, but B D doesn't have to cut A C in half." The caption reads "AO = OC? not given". The scoped "In this kite, A O is eight and O C is twelve, so they really are different" comes after the calculation.
- [must] **Fixed.**
  - The Pythagoras rows AO² = 17² − 15² and = (17 − 15)(17 + 15) are written.
  - The area slide shows the whole kite tinted, with AC and BD traced.
  - Rows: AC = 8 + 12 = 20 → BD = 15 + 15 = 30 → S = 20·30/2 → 30/2 = 15 → 20·15 = 300.
  - The other ways each have their own rows and tints: ABD 120, CBD 180, 120 + 180 = 300, and 2·(15·8/2) = 120, 2·(15·12/2) = 180.

### #235 solve-geo32-g063
- [should] **Fixed.** "The two base angles of this triangle add up to sixty degrees. So the top angle… is one hundred eighty minus sixty." The 30° + 30° = 60° row comes first. Then "A D and B C are the parallel bases, and B D crosses them. So the angles in the two corners of the Z, angle A D B and angle D B C, are equal", with both arcs in red. And "because this trapezoid is isosceles, its opposite angles add up to one hundred eighty".
- [should] **Fixed.** A new slide, "The gold triangle", carries all the angles found so far. "Now the perimeter, all four outer sides" traces the four edges in red. P = 7 + 7 + 7 + 14 and = 35 are separate rows, and BD = 7√3 is its own row.

### #236 geo-065
- [should] **Fixed.** "Now let's try harder quadrilateral questions." The area line no longer calls algebra wasteful. "We'll use the math way, understanding, and plugging in numbers, each where it helps." The board reads "Areas: symmetry and equal heights".

### #237 solve-geo32-g066
- [must] **Fixed.** "Every rhombus has everything a deltoid is guaranteed to have. A deltoid has two pairs of equal sides, and in each pair the equal sides are next to each other. A rhombus has all four sides equal. So the two top sides are equal and next to each other, and so are the two bottom sides." The panels show the adjacent pairs traced, with no "short diagonal".
- [should] **Fixed.** "If its diagonals were perpendicular, it would be a rhombus, and a rectangle that's a rhombus is a square. This one is not a square, so its diagonals are not perpendicular." This uses the geo-047 criterion.

### #238 solve-geo32-g067
- [must] Prompter and board: **fixed** in the speech and the board. "Open the brackets on top. We get x h plus y h, and both products are still over two."
  - Rows: S = (x + y)·h/2 → = (xh + yh)/2 → = (12 + 30)/2 → = 42/2 = 21.
  - Also x·h/2 = 6 → xh = 12 and y·h/2 = 15 → yh = 30.
  - The exact grouped prompter display is listed under Needs Claude.
- [must] **Fixed.** At "Now the shaded triangle", the corner tints fade and EBC is tinted, with its base BC (x + y) and height h. The rows moved out of the footer, into the column under the copy and to its right.
- [should] **Fixed.** "long and tiring", "Much shorter" and the exam-position comment are removed. Method 2 is "Now by understanding, with symmetry", and its reason is said: "each small rectangle is split into two equal areas by its diagonal."

### #239 geo-067-after
- [must] **Fixed.** "The triangles do not overlap, and their bases cover the whole bottom side without gaps." The board reads "No overlap, bases cover the side: shaded = ½". The parallelogram paragraph carries the same conditions.
- [should] **Fixed.** "That's clear to all of us" is removed, and "It's true here as well" is replaced by the concrete three-triangle case. The common height h is marked, with the why: "each area is its base times h, over two… the three bases together make the whole bottom side". Board: b₁h/2 + b₂h/2 + b₃h/2 = (b₁ + b₂ + b₃)h/2. Parallelogram: "Its height is the perpendicular distance between the two parallel sides, not the slanted line we drew." A dashed height is drawn.
- [should] **Fixed.** The captions say shaded / white, with a key line "Same colour, same area" (spoken as "The same colour means the same area"). The left pair fades before the right pair lights up.

### #240 solve-geo32-g068
- [should] **Fixed.**
  - "The wording isn't very clear" and "start with the data that works" are removed. It now says "Let's try choice number one, the area of E C D. … let's call it s."
  - "A D is cut into four equal parts… That puts E exactly above G… E G joins two points at the same distance from A B, so it's parallel to A B, and perpendicular to the bases."
  - The ratio labels read "3 parts" and "1", with quarter ticks, and a right-angle mark at G.
- [must] **Fixed.** s is written on ECD at "let's call it s". Rows: S_EGC = s / right rectangle = 2s / left = 3·2s = 6s / S_FEG = 6s/2 = 3s / shaded = s + 3s = 4s. Then "whole = 8s: shaded is half" comes only in the recap paragraph. The classroom check stays after "we mark choice number one and move on".
- [should] **Fixed.** "Now s means a new area, the area of A F E", with a row. A new figure shows "two allowed shapes… A F and A E are the same, so A F E has the same area. But the second rectangle is taller, so its shaded area is bigger."

### #241 solve-geo32-g069
- [must] **Fixed.** "For this base, A D, the perpendicular from B lands beyond A. So we extend D A past A… Its length, the perpendicular distance, is the height h."
- [must] **Fixed.**
  - Rows: 5h/2 = 15 → 5h = 30 → h = 6 → 5 + 20 = 25 → 25·6 = 150 → 150/2 = 75.
  - A `whole` layer outlines the trapezoid.
  - Method 2 draws both perpendicular heights (B to the line of AD, and D down to BC), with no number on them.
  - Method 2 rows: "same height: area ratio = base ratio", 20 = 4·5, 4·15 = 60, 15 + 60 = 75.
- [should] **Fixed.** "Now by understanding, using equal heights." It ends with "So when two triangles have the same perpendicular height, the area ratio is the base ratio… We didn't use that the trapezoid is isosceles, so this works for any trapezoid with these bases and this area." "Not too bad… much shorter" and "you barely write anything" are removed.

### #242 solve-geo32-g070
- [must] **Fixed.**
  - The five rectangles were already at the right grid lines: x = 3 for y 0–2, the full line y = 2, and x = 2 and x = 6 for y 2–5.
  - A new `dims` layer writes 3, 5, 2, 3, 2, 4, 2 at the spoken "On top, three by two and five by two. At the bottom, two by three, four by three, and two by three", before any area appears.
- [must] **Fixed.** Every multiplication and halving is its own paragraph and row:
  - Method 1: 8·5 = 40, 3·2/2 = 3, 5·2/2 = 5, 2·3/2 = 3, 3 then 3 + 5 + 3 + 3 = 14, then 40 − 14 = 26.
  - Method 2: one value per region (v1, v2, v3 layers), then 3 + 5 + 3 + 3 + 12 and = 26.
  - Method 3 rows: 8·2/2 = 8, 4·3 = 12, 2·3/2 = 3, 8 + 12 + 3 + 3 = 26.
- [should] **Fixed.** Every method is named aloud ("the math way"; "Now let's use understanding: pair the pieces that make a whole"; "by understanding again, with the symmetry principle").

### #243 solve-geo32-g071
- [must] **Fixed.** "The figure is not drawn to scale, so we don't read values from it. Let's take alpha a hundred ten and beta eighty, because they're easy to add and to halve. Any other allowed values would work too." Then "Forty is positive, so our numbers are allowed… All three angles of the triangle are positive."
- [should] **Fixed.** "long and tiring", the time and position claims, the algebra-versus-most-students verdict and "a very reasonable guess" are removed. It now says "a match alone isn't enough if another choice also matches, so we check the last one too… A mismatch rules a choice out right away, and only choice number three matched."
- [must] **Fixed.**
  - Algebra rows: ∠D + α + 130° + β = 360°, 360° − 130° = 230°, ∠D = 230° − α − β, ∠ADE = 115° − α/2 − β/2, x = 180° − α − (115° − α/2 − β/2), x = 180° − α − 115° + α/2 + β/2, x = 65° − α/2 + β/2.
  - "minus the whole bracket" was rewritten as "minus angle A D E… Now we open the bracket. The minus in front of it changes every sign inside."
  - Numeric rows: 110 + 130 + 80 = 320, ∠D = 360 − 320 = 40, 40/2 = 20, 110 + 20 = 130, x = 180 − 130 = 50.
  - 50° goes on the figure only at "so x is fifty degrees".

### #244 solve-geo32-g072
- [must] **Fixed.**
  - The labelled tile diagram (4x, x, 6x) is carried onto the perimeter slide, and 8 and 12 replace 4x and 6x on the same sides at "and six x is twelve".
  - Understanding gets its own copy, with 2 parts and 3 parts marked on the sides.
  - Rows: 4x:6x = 2:3, 40/2 = 20, 2 + 3 = 5 parts, 20/5 = 4, 2·4 = 8 and 3·4 = 12, 8·12 = 96.
- [should] **Fixed.** "Divide forty by twenty, so x is two." Then "Now by understanding, with a different finish. We start from the same tiles, which gave us the sides four x and six x." The "shorter way" is removed.

### #245 r26-t32-perimeter
- [must] **Fixed.**
  - Rows 2(10 + 6) = 32, 2(4 + 6) = 20, 2(6 + 6) = 24, 20 + 24 = 44, 44 = 32 + 2·6 come at their clauses.
  - A new slide, "Cut across", has its own figure: a 10-long horizontal cut, the 10 × 2 and 10 × 4 pieces, the cut traced twice, and rows 24, 28, 24 + 28 = 52, 52 = 32 + 2·10.
  - The rule comes after both examples.
- [must] **Fixed.** A new slide, "Deeper, and a corner", has:
  - a real 3-deep notch with walls labelled 3 and P = 32 + 2·3 = 38;
  - a real corner step, whose new bottom (3) and new wall (2) are paired in colour with the cut-away top and right pieces, and "P = 32".
- [should] **Fixed.**
  - The opening is now "Let's look at two useful perimeter shortcuts."
  - The push-up is explained: "The bottom of the notch is a horizontal segment. Slide it straight up to the top line. It keeps its length, and it fills exactly the gap in the top side."
  - The rules are scoped: "for straight cuts like these" and "for straight, rectangular cuts like these".

### #246 solve-q-r26-t32-06
- [should] **Fixed.**
  - "Each one keeps its length when we slide it straight up… Together they cover the whole top once, with no overlap and no gap."
  - The vertical steps are treated the same way. "The bottom, twelve, and the left side, eight, don't change", and the row is P = 12 + 8 + 12 + 8 = 40.
  - The condition is stated: "the stair path only goes right and down, with no part going back in", with the notch reminder at the end.

### #247 solve-q-r26-t32-07
- [must] **Fixed** (taught here). A new slide, "Squaring a sum" (NOFIG, the whole board), covers:
  - what squaring a sum means, and the four products;
  - why the two ab terms add;
  - two checks, (2 + 3)² = 25 against 4 + 12 + 9, and (3 + 1)² = 16 against 9 + 6 + 1;
  - the trap, "a plus b, squared, is not a squared plus b squared… only thirteen".
  - Both methods are named aloud.
- [must] **Fixed.** On the "Back to the rectangle" slide the known data come first (a + b = 17, a² + b² = 169). Then rows 17·10 = 170, 17·7 = 119, 17² = 170 + 119 = 289, 289 = 169 + 2ab, 2ab = 289 − 169 = 120 and ab = 120/2 = 60, with "we divide both sides by two" said.
- [should] **Fixed.**
  - "So this rectangle fits both givens… The math way already showed that every rectangle with these givens has area sixty."
  - The traps sit at their steps: 120 at 2ab, 65 at "thirteen is the diagonal, not a side", and 30 at the end ("half of sixty… the triangle A B C").
  - The perimeter check is now "Five plus twelve is seventeen, and two times seventeen is thirty-four", which fixes the "2 × 5 + 12" display.

## Needs Claude (display only; all paragraphs unrecorded)

1. **solve-geo32-g067 ¶7 (1.7)** — spoken: "So its area is x plus y, times h, over two. Open the brackets on top. We get x h plus y h, and both products are still over two."
   - Shown now: "(x + y) × h ÷ 2 … We get x × h + y × h, and both products are still over two."
   - Wanted: "(x + y)h/2 … We get (xh + yh)/2, and both products are still over two."
2. **solve-geo32-g067 ¶8 (1.8)** — spoken: "We found that x h is twelve and y h is thirty, so it's twelve plus thirty, over two. That's forty-two over two, which is twenty-one."
   - Wanted: "… so it's (12 + 30)/2. That's 42/2 = 21."
   - Shown now: "12 + 30, over two", which is unambiguous but not grouped.
3. **solve-q-r26-t32-07 ¶6, ¶7, ¶13–¶15 (2.2, 2.3, 3.3–3.5)** — spoken "a b" and "two a b".
   - Shown now: "a × b = a × b", "two a × b", "2a × b".
   - Wanted: "a × b = ab", "two ab" / "2ab", "289 = a² + b² + 2ab", "So it's 169 + 2ab", "2ab = 120", "ab = 60".
4. **solve-geo32-g055 ¶13 (4.1)** — optional. The spoken text was reworded and the display is now correct: "The sum of the bases is x + x + 8, which is 2x + 8. We multiply that sum by 5, divide by 2, and we get 65." If Codex still wants the grouped form, the wanted display is "(x + x + 8) × 5/2 = 65". ¶14 (4.2) shows "So 2x + 8, multiplied by five, gives 130"; the wanted grouped form is "(2x + 8) × 5 = 130".

## Checks (final build)
- **Spec regeneration:** `python3 math_patches/_ai_vis_t32.py <37 ids>` printed no PROBLEMS.
- **Private build:** `scratchpad/t32/test-t32.html`, made with `OUT=…`. The shared Downloads file was not written.
- **`SRC=… python3 ai_check.py <37 ids>`:** all 37 OK. Only the old style notes remain ("three hundred sixty", "either", "neither").
- **`w19_check.py`:**
  - Flags dropped from 194 to 166 unique sentences.
  - 25 sentences are flagged that were not flagged before. They are new working sentences that each hold one expression or one step (for example "So x plus x plus eight…" and "By the formula, two hundred eighty-nine is a squared plus b squared, plus two a b."). I judged each one by hand: one step per sentence, so they can't be split further without breaking the expression.
  - All the genuinely double-step new sentences were split.
- **`layoutcheck.py`** (topic-32 videos): 0 problems (the baseline had 1, geo-054 #5, now fixed).
- **`svgcheck.py`:** 55,908 slide steps on the final build, 0 broken.
- **Recording status** at the end of the job: all 37 still Record, with no takes.
- **Step frames:** rendered with a scratchpad renderer that uses the studio's `boardSvg`, then checked as contact sheets and enlarged final frames. Every slide I changed was inspected for premature results, overlaps and overflow. That is how I found the tiny shrunk rows on question slides and fixed them with the right-hand working column and NOFIG.
- **Prompter:** every paragraph of the 37 lessons was dumped with `reading_studio.prompter_display` and scanned for false chains. The fixes are above; the remaining wishes are under Needs Claude.
