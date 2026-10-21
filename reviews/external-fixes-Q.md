# External-course fixes, part Q: topics 33 and 34 (21 Oct 2026)

Files changed: `studio-build/math_patches/_ai_vis_t34.py`, `studio-build/math_patches/_ai_vis_t33.py`,
`studio-build/summary_pages/t33.json`, `studio-build/summary_pages/t34.json` (+ the regenerated `ai_scripts/*.json` of
these topics). Before-copies: `reviews/before-2026-10-21-external-fixes/_ai_vis_t33.py`, `_ai_vis_t34.py`; the two
summary jsons are also in `scratchpad/xf-Q/before/`. No git, no shared studio build.

**Recording status (checked first):** `video_status.py --list record` lists geo-104, geo-104-2, -3, -4, geo-097-after and
r26-t33-more-tools as Record, and none of them has a folder in `~/Documents/Course.recordings/_reading/`. Recorded in
topic 33: geo-074 (all parts), geo-075, solve-geo33-g076, solve-q-r26-t33-01. Nothing recorded was edited.

**New video ids (lesson parts, R37: a lesson past ~5-6 min is split at an idea boundary).** These are made by
`_camera_parts.split` and added to the course by `add_to_course` at build time, like the other topics' parts:
- `geo-104-5` (camera lesson geo-104 is now 5 parts; parts 1-3 unchanged in content, only "(Part k of 5)").
- `geo-097-after-2` (the nested-shapes lesson in 2 parts, title now "Four Nested Shapes").
- `r26-t33-more-tools-2`, `r26-t33-more-tools-3` (More Circle Tools in 3 parts, one tool each).
Lengths: geo-104-4 3.8 min, geo-104-5 4.0; geo-097-after 3.5, -2 3.3; more-tools 3.9, -2 2.9, -3 2.2.
Topic 33 had no MORE_SPLITS loop, so I added the same one-line loop topic 34 uses (right after the CAMERA_SPLIT line).

---

## 1. Topic 34: "count the sides" (geo-104, now parts 4 and 5)

**Where and why there.** geo-104 part 4 ("The diagonals") already shows that the diagonals from one corner cut the angle
into equal parts, using "every regular polygon fits in a circle" + inscribed angles on equal arcs. Part 3 taught the
central angle 360/n, and topic 33 (before 34 in the plan) taught "an inscribed angle is half the central angle on the
same arc". So the rule follows in one step from what is on the screen: one side's arc gives 180/n. The new slides sit
right after "The diagonals". Topic 34 nowhere else teaches it (q-r26-t34-02 counts diagonals, n - 3; g110 is the
pentagon middle angle by three ways; g111 the nonagon statements), so nothing is re-taught.

**Conditions stated (3.5) and checked in every example:** regular polygon; the angle's corner is a corner of the
polygon; both arms go through corners; count the sides on the far side between the arms. The crossing example states
its own condition: diagonals from two neighbouring corners, each skipping one corner.

**Numbers (recomputed, also numerically from the figure coordinates):** pentagon small angle 36 = 180/5, central 72;
whole angle 3 x 36 = 108. Decagon (n = 10, new; the exam's nonagon item 2026_spring_q2_19 asks one side = 20): one side
18, alpha between AD and AG = 3 x 18 = 54; whole angle 8 x 18 = 144 = 180 - 36. Hexagon (new shape; the exam's
2023_spring_q2_03 is a pentagon with answer 108): AC and BD cross at P, angle PBC = 30 (arc CD), angle PCB = 30 (arc AB),
BPC = 120 = the hexagon's angle; the pentagon second run 180 - 36 - 36 = 108.

**Guided question:** not added; the lesson holds two worked examples plus the crossing case, and part 5 opens with the
exam-type crossing angle.

### Changes to existing paragraphs (geo-104)
- **geo-104 split** `CAMERA_SPLIT`: BEFORE 4 parts → AFTER 5 parts; new entry `(17, "Let's continue with the diagonals of a
  regular polygon.")`. Part 4 = The diagonals, Count the sides, Ten sides (ends with the automatic "Okay. I'll see you in
  the next part."). Part 5 = Crossing diagonals, Triangles from the center, The hexagon, Summary.
- **geo-104-5 Summary, paragraph 4.** BEFORE: "The diagonals from one corner cut its angle into equal parts. The radii
  cut the polygon into n isosceles triangles, and in the hexagon, six equilateral triangles. Take a moment to memorize
  these, and I'll see you in the next video." AFTER: "The diagonals from one corner cut its angle into equal parts, one
  hundred eighty over n each. So an angle at a corner, with its arms through two other corners, is the sides between its
  arms, times one hundred eighty over n. The radii cut the polygon into n isosceles triangles, and in the hexagon, six
  equilateral triangles. Take a moment to memorize these, and I'll see you in the next video."
  Board row p104z4 BEFORE "Diagonals from a corner: equal angles" → AFTER "Angle at a corner = sides between the arms ·
  180°/n" (shown at the same cue).
- Summary page t34.json: new rule row "Angle at a corner, arms through corners (regular) | 180°/n for every side between
  the arms | 10 sides, 3 between: 3·18° = 54°" (page rebuilt privately, math checks pass, still one page).

### New slides (all NEW text; BEFORE = nothing). Exact text, with what is shown at which words

#### geo-104-4 slide 3 "Count the sides"
- **3.1** Let's look at those small angles again. In the regular pentagon, each one was thirty-six. In the regular hexagon, each one was thirty. And there's a pattern here. Thirty-six is one hundred eighty divided by five. And thirty is one hundred eighty divided by six.  
  _shown:_ p104cnt_line @ "In the regular pentagon"; p104cnt_one @ "each one was thirty-six"; p104k1 @ "Thirty-six is one hundred eighty divided by five"; p104k2 @ "thirty is one hundred eighty divided by six"
- **3.2** Why one hundred eighty divided by n? Because each small angle is an inscribed angle, and it intercepts the arc under one side. The central angle on that same arc is three hundred sixty divided by n. In the pentagon, that's seventy-two. And an inscribed angle is half of the central angle on the same arc. So each small angle is half of three hundred sixty over n. That's one hundred eighty over n, and in the pentagon, half of seventy-two is thirty-six.  
  _shown:_ p104cnt_cen @ "The central angle on that same arc"; p104k3 @ "is three hundred sixty divided by n"; p104cnt_c72 @ "In the pentagon, that's seventy-two"; p104k3b @ "That's one hundred eighty over n"
- **3.3** So every side adds one hundred eighty over n to an angle like this. Here's the rule. Take an angle whose corner is a corner of the polygon, and whose two arms go through two other corners. Count the sides between the two arms, on the far side from the corner. The angle is that number of sides, times one hundred eighty over n.  
  _shown:_ p104k4 @ "Here's the rule"
- **3.4** Let's check it on the whole angle of the pentagon. Its arms are the two sides at the corner. Between them, on the far side, there are three sides. Three times thirty-six is one hundred eight. That's exactly the pentagon's angle, like we found before.  
  _shown:_ p104cnt_whole @ "Between them, on the far side"; p104k5 @ "Three times thirty-six"; p104cnt_w108 @ "That's exactly the pentagon's angle"
- **3.5** This works only in a regular polygon, because only there are all the sides equal, so all their arcs are equal. And the angle's corner must be a corner of the polygon, and both arms must go through corners too. Only then is it an inscribed angle on those arcs.  
  _shown:_ p104k6 @ "This works only in a regular polygon"

#### geo-104-4 slide 4 "Ten sides"
- **4.1** Let's use it. Here's a regular polygon with ten sides, A to J. From corner A, we draw two diagonals, to D and to G. What is the angle alpha between them?  
  _shown:_ p104dec_line @ "Here's a regular polygon with ten sides"
- **4.2** First, what one side adds. One hundred eighty divided by ten is eighteen. So every side between the arms adds eighteen degrees.  
  _shown:_ p104e1 @ "One hundred eighty divided by ten"
- **4.3** Now we count the sides between the arms, from D to G. They are D E, E F and F G. That's three sides. So alpha is three times eighteen, which is fifty-four.  
  _shown:_ p104dec_sides @ "D E, E F and F G"; p104e2 @ "So alpha is three"; p104dec_val @ "which is fifty-four"
- **4.4** Let's check the rule on the whole angle at A. Its arms are the sides A B and A J. From B to J there are eight sides. Eight times eighteen is one hundred forty-four. Let's also check it with the formula sheet. Three hundred sixty divided by ten is thirty-six. One hundred eighty minus thirty-six is one hundred forty-four. That's the same angle. [pause] Okay. I'll see you in the next part.  
  _shown:_ p104dec_whole @ "From B to J there are eight"; p104e3 @ "Eight times eighteen"; p104dec_w144 @ "is one hundred forty-four. Let's"; p104e4 @ "eighty minus thirty-six is one hundred forty-four"

#### geo-104-5 slide 1 "Polygons (Part 5 of 5)"
- **1.1** Let's continue with the diagonals of a regular polygon.  
  _shown:_ —

#### geo-104-5 slide 2 "Crossing diagonals"
- **2.1** Now an angle where two diagonals cross. A B C D E F is a regular hexagon. The diagonals A C and B D cross at the point P. What is angle B P C?  
  _shown:_ p104hxc_line @ "A B C D E F is a regular hexagon"
- **2.2** P isn't a corner of the hexagon, so we can't count sides at P. But look at triangle B P C. Its other two angles are at B and at C, and those are corners. So let's find those two angles, and then use the triangle's one hundred eighty.  
  _shown:_ p104hxc_tri @ "look at triangle B P C"
- **2.3** In a hexagon, one side adds one hundred eighty divided by six, thirty. The angle at B is between B C and B D. Its arms go through C and D, and between them there's one side, C D. So angle P B C is thirty.  
  _shown:_ p104h1 @ "one hundred eighty divided by six"; p104hxc_b @ "The angle at B is between"; p104h2 @ "So angle P B C is thirty"; p104hxc_b30 @ "So angle P B C is thirty"
- **2.4** The angle at C is between C B and C A. Its arms go through B and A, and between them there's one side, A B. So angle P C B is thirty too.  
  _shown:_ p104hxc_c @ "The angle at C is between"; p104h3 @ "So angle P C B is thirty too"; p104hxc_c30 @ "So angle P C B is thirty too"
- **2.5** The angles of triangle B P C add up to one hundred eighty. So angle B P C is one hundred eighty minus thirty minus thirty. That's one hundred twenty.  
  _shown:_ p104h4 @ "one hundred eighty minus thirty"; p104hxc_p @ "That's one hundred twenty"
- **2.6** One hundred twenty is exactly the hexagon's angle. In a regular pentagon, the same two diagonals cross at one hundred eighty minus thirty-six minus thirty-six. That's one hundred eight, the pentagon's angle. So when two diagonals start at two neighboring corners, and each one skips just one corner, they cross at the polygon's own angle.  
  _shown:_ p104h5 @ "hundred eighty minus thirty-six minus thirty-six"; p104h6 @ "So when two diagonals start"

#### geo-104-5 slide 5 "Summary"
- **5.1** Let's sum up. The angle sum is one hundred eighty times the bracket, n minus two. Or split from one corner into n minus two triangles. And every extra side adds one hundred eighty.  
  _shown:_ p104z1 @ "Let's sum up"
- **5.2** Regular means all the sides and all the angles are equal. Then one angle is the sum divided by n. The pentagon is one hundred eight, the hexagon is one hundred twenty, and the octagon is one hundred thirty-five.  
  _shown:_ p104z2 @ "Regular means"
- **5.3** The central angle and the exterior angle are both three hundred sixty divided by n. Each one completes the polygon's angle to one hundred eighty.  
  _shown:_ p104z3 @ "The central angle and the exterior angle"
- **5.4** The diagonals from one corner cut its angle into equal parts, one hundred eighty over n each. So an angle at a corner, with its arms through two other corners, is the sides between its arms, times one hundred eighty over n. The radii cut the polygon into n isosceles triangles, and in the hexagon, six equilateral triangles. Take a moment to memorize these, and I'll see you in the next video.  
  _shown:_ p104z4 @ "The diagonals from one corner"; p104z5 @ "The radii cut"


### Board / visual requirements (topic 34)
- **Count the sides** (`p104cnt`): the regular pentagon with the diagonals from the bottom corner and the dashed circle
  at "In the regular pentagon"; the middle small angle (teal arc) + the arc under the top side (thick teal) + "36°" at
  "each one was thirty-six"; the two radii to that side (orange dashed) and the central wedge at "The central angle on
  that same arc", "72°" only at "In the pentagon, that's seventy-two"; the whole corner angle (orange) with the three far
  sides thick teal, numbered 1, 2, 3, at "Between them, on the far side", "108°" under the corner at "That's exactly the
  pentagon's angle". Rows (right): 180° ÷ 5 = 36°, 180° ÷ 6 = 30°, central angle of one side = 360°/n, inscribed angle
  = half = 180°/n, each side between the arms: 180°/n, 3 · 36° = 108°, "Only: regular, corner on a corner, arms through
  corners" — each at its own clause.
- **Ten sides** (`p104dec`): regular decagon A…J (A at the bottom), diagonals AD and AG, α marked; DE, EF, FG thick
  teal numbered 1-3 at "D E, E F and F G"; "54°" at "which is fifty-four"; the whole angle at A + the 8 far sides orange
  at "From B to J there are eight"; "144°" at "is one hundred forty-four. Let's". Rows: one side 180° ÷ 10 = 18°,
  3 · 18° = 54°, whole angle 8 · 18° = 144°, 180° − 36° = 144°.
- **Crossing diagonals** (`p104hxc`): regular hexagon A…F with BC at the bottom, AC and BD crossing at P; triangle BPC
  tinted at "look at triangle B P C"; angle at B (teal) + side CD thick teal at "The angle at B is between", "30°" at "So
  angle P B C is thirty"; angle at C (orange) + side AB thick orange, "30°" at "So angle P C B is thirty too"; the angle at
  P + "120°" at "That's one hundred twenty". Rows: one side 180° ÷ 6 = 30°, ∠PBC = 30°, ∠PCB = 30°,
  ∠BPC = 180° − 30° − 30° = 120°, pentagon: 180° − 36° − 36° = 108°, "Neighboring corners, each skips one: the polygon's
  angle".
- Pen-safe: no ✗; hand rows use only ÷ · − ° and \angle (falls back to typed when the pen lacks a glyph).

### Read-aloud check (topic 34)
Read every new / changed paragraph aloud against the handwriting frames (`scratchpad/xf-Q/fr/geo-104-4`, `geo-104-5`).
Fixed while reading: "D E, E F and F G" (the prompter showed the first D unstyled; now "They are D E, E F and F G");
two dense sentences split (36 / 30; the formula-sheet check); "which is one hundred twenty" → "That's one hundred twenty";
"the same two diagonals give…" → "cross at…". "Those small angles" (4.3.1) refers to the 36° / 30° angles of the slide
just before and the figure shows the 36° one at that moment. "an angle like this" (4.3.3) follows the shown small angle.
Every "it" names its angle or rule in the sentence before. Frames fixed after looking: the decagon's top label F was cut
(view box), the rule row wrapped into two lines (shortened), the crossing figure was small and its 30° labels touched the
corners (figure wider, labels moved), the count slide ran off the slide in the typed build (rows 30 px). Ready.

---

## 2. Topic 33: circle, triangle, circle (geo-097-after, now 2 parts)

**Where:** geo-097-after (Record, no take) — the nested-shapes lesson; a fourth arrangement after "Triangle, circle,
triangle". **Prerequisites (one-sentence reminders only):** radius to the point of tangency is perpendicular (geo-077,
before it); the gold triangle 30-60-90 (topic 31, named "gold triangle" in this course); the scaling rule lengths × k →
area × k² (already on this lesson's last slide). **Why:** the right triangle O M C: angle C is half of 60 (symmetry), so
across from 30 is r = half the hypotenuse R → R = 2r; the long leg MC = r√3 → side = 2r√3 = R√3.
**Condition said:** "Again, the triangle must be equilateral" + board row "The triangle is equilateral"; both circles have
the same center O. **Numbers (new; the exam 2019_winter_q2_08 uses r = 1 → 3π):** r = 3 → R = 6, 9π and 36π (×4), ring
27π = 3 · 9π, side 6√3; second run r = 2 → 16π − 4π = 12π = 3 · 4π.

### Changes to existing paragraphs (geo-097-after)
- Title slide: BEFORE "Three Nested Shapes" / "I want to use the last question to show you three useful arrangements of
  shapes inside shapes. Each one comes with a fixed ratio. Once we see why, it's worth remembering them." AFTER "Four
  Nested Shapes" / "…to show you four useful arrangements…" (rest unchanged). The part titles "Four Nested Shapes (Part k of 2)"
  are set on the course videos by add_to_course.
- `MORE_SPLITS`: part 2 starts at "Circle, triangle, circle" with "Let's continue with nested shapes."; part 1 ends with
  the automatic "Okay. I'll see you in the next part." after "…and its area is a quarter."
- Length factor, paragraph 2. BEFORE: "In the first two arrangements, every length is multiplied by root two. So the
  areas are multiplied by two. In the triangle arrangement, every length is multiplied by two. So the areas are
  multiplied by four." AFTER: "…In the two triangle arrangements, every length is multiplied by two. So the areas are
  multiplied by four." New row f7t10d "Circle, triangle, circle: lengths ×2, areas ×4" at "every length is multiplied by
  two"; f7t10c now at "In the two triangle arrangements".
- Length factor, paragraph 3. BEFORE: "So remember the three area ratios, the outer area over the inner area. They are
  two, two, and four. Take a moment to memorize this. [pause] Okay. I'll see you in the next video." AFTER: "So remember
  the four area ratios, the outer area over the inner area. They are two, two, four and four. Take a moment to memorize
  this, and I'll see you in the next video." Row f7t11 → "Outer area over inner area: 2, 2, 4, 4".
- Summary page t33.json, the shaded-areas paragraph: added "circle-triangle-circle (equilateral) **four times**: R = 2r,
  the ring is 3 small circles."

### Board / visual requirements
- `f7nD` (slide "Circle, triangle, circle"): big circle → equilateral triangle ABC → small circle → O, each at its words;
  the dashed teal radius OM with the right angle and "r" at "Draw the small radius r"; OC orange "R" at "Now draw the big
  radius R"; triangle OMC tinted at "We get the right triangle"; the 30° arc at C at "so it's thirty"; "r√3" under MC at
  "The long leg, M C". Rows: The triangle is equilateral / Big radius = 2 × small radius / Across from 30°: half the
  hypotenuse / r = R/2, so R = 2r / Side = 2r√3 = R√3.
- `f7nE` (slide "The ring"): the same figure with 3 on OM at "Say the small radius is three", 6 on OC at "The big radius is
  twice that", the ring tinted at "Questions like to ask about the ring", 6√3 under BC at "And the triangle's side". Rows:
  Small π·3² = 9π, Big π·6² = 36π, Big area = 4 × small area, Ring 36π − 9π = 27π = 3·9π, r = 2: 16π − 4π = 12π = 3·4π,
  Side = 6√3.

### Read-aloud check
Read against the frames (`fr/geo-097-after-2`). "this radius"/"it" never stand alone: each radius is named (small radius
r, from O to M; big radius R, from O to the corner C). "that corner's angle" follows "the corner C". Fixed after looking:
the label A was cut at the top (view box). Ready.

### New / changed slides, exact text (topic 33), with what is shown at which words

#### geo-097-after slide 1 "Four Nested Shapes (Part 1 of 2)"
- **1.1** I want to use the last question to show you four useful arrangements of shapes inside shapes. Each one comes with a fixed ratio. Once we see why, it's worth remembering them.  
  _shown:_ —

#### geo-097-after-2 slide 1 "Four Nested Shapes (Part 2 of 2)"
- **1.1** Let's continue with nested shapes.  
  _shown:_ —

#### geo-097-after-2 slide 2 "Circle, triangle, circle"
- **2.1** The fourth one is circle, triangle, circle. Again, the triangle must be equilateral. A circle around the triangle, with its three corners on the circle. And a circle inside the triangle, touching all three sides. Both circles have the same center, O.  
  _shown:_ f7nD_line @ "The fourth one is circle"; f7t12 @ "the triangle must be equilateral"; f7nD_tri @ "with its three corners on the circle"; f7nD_in @ "touching all three sides"; f7nD_o @ "the same center, O"
- **2.2** Here the big radius is twice the small radius. Let's see why. Draw the small radius r, from O to M, the point where the small circle touches the bottom side. A radius to the point of tangency is perpendicular to the side. So there's a right angle at M.  
  _shown:_ f7t13 @ "the big radius is twice"; f7nD_r @ "Draw the small radius r"
- **2.3** Now draw the big radius R, from O to the corner C. We get the right triangle O M C.  
  _shown:_ f7nD_R @ "Now draw the big radius R"; f7nD_omc @ "We get the right triangle"
- **2.4** The angle at C is half of the triangle's sixty degrees, so it's thirty. Why half? Because the equilateral triangle is symmetric, so the line from the corner C to the center cuts that corner's angle into two equal halves. So O M C is a gold triangle, thirty, sixty, ninety.  
  _shown:_ f7nD_c30 @ "so it's thirty"
- **2.5** In a gold triangle, the side across from the thirty is half of the hypotenuse. Here the side across from the thirty is r, and the hypotenuse is big R. So r is half of big R, and big R is two times r.  
  _shown:_ f7t14 @ "In a gold triangle"; f7t15 @ "So r is half of big R"
- **2.6** The gold triangle also gives us the side. The long leg, M C, is r root three. M is the middle of the side B C, so the whole side is two r root three. And two r is big R, so the side is big R root three.  
  _shown:_ f7nD_mc @ "The long leg, M C"; f7t16 @ "so the whole side is two r root three"

#### geo-097-after-2 slide 3 "The ring"
- **3.1** Let's try it in numbers. Say the small radius is three. The big radius is twice that, six. The small circle's area is pi times three squared, nine pi. The big circle's area is pi times six squared, thirty-six pi.  
  _shown:_ f7nE_line @ "Let's try it in numbers"; f7nE_r3 @ "Say the small radius is three"; f7nE_R6 @ "The big radius is twice that"; f7t17 @ "pi times three squared"; f7t18 @ "pi times six squared"
- **3.2** Thirty-six pi is four times nine pi. So the big circle's area is four times the small circle's area. That's the scaling rule again. Every length is multiplied by two, so the area is multiplied by two squared, four.  
  _shown:_ f7t19 @ "So the big circle's area is four times"
- **3.3** Questions like to ask about the ring, the part between the two circles. The ring is the big circle minus the small one. Thirty-six pi minus nine pi is twenty-seven pi. And twenty-seven pi is three times nine pi. So the ring is three small circles.  
  _shown:_ f7nE_ring @ "Questions like to ask about the ring"; f7t20 @ "Thirty-six pi minus nine pi"
- **3.4** It's three small circles for any radius. With a small radius of two, the big radius is four. The big circle is sixteen pi, the small one is four pi, and the ring is twelve pi. Twelve pi is three times four pi.  
  _shown:_ f7t21 @ "With a small radius of two"
- **3.5** And the triangle's side is big R root three. Here big R is six, so the side is six root three.  
  _shown:_ f7nE_side @ "And the triangle's side"; f7t22 @ "so the side is six root three"

#### geo-097-after-2 slide 4 "Length factor, area factor"
- **4.1** Now, this is important. A length factor isn't an area factor. The area factor is the length factor, squared.  
  _shown:_ f7t9 @ "The area factor is the length factor"
- **4.2** In the first two arrangements, every length is multiplied by root two. So the areas are multiplied by two. In the two triangle arrangements, every length is multiplied by two. So the areas are multiplied by four.  
  _shown:_ f7t10 @ "In the first two arrangements"; f7t10b @ "So the areas are multiplied by two"; f7t10c @ "In the two triangle arrangements"; f7t10d @ "every length is multiplied by two"
- **4.3** So remember the four area ratios, the outer area over the inner area. They are two, two, four and four. Take a moment to memorize this, and I'll see you in the next video.  
  _shown:_ f7t11 @ "the outer area over the inner area"

#### r26-t33-more-tools slide 1 "More Circle Tools (Part 1 of 3)"
- **1.1** Here are three more circle tools. They come up in some of the harder circle questions. And right after this lesson, two questions teach two more tools.  
  _shown:_ —

#### r26-t33-more-tools-2 slide 3 "Same chord, same ring"
- **3.1** So if the chord is ten, then h is half of it, five. And the ring is pi times five squared, twenty-five pi. We don't need either radius.  
  _shown:_ f9t10 @ "So if the chord is ten"; f9t10b @ "And the ring is pi times"
- **3.2** Let's check it on rings with a chord of ten. Radii twelve and thirteen, the five, twelve, thirteen triangle. The big circle is pi times thirteen squared, a hundred sixty-nine pi. The small one is pi times twelve squared, a hundred forty-four pi.  
  _shown:_ f9rings_line @ "Radii twelve and thirteen"; f9rings_r1a @ "The big circle is pi"
- **3.3** The ring is the big circle minus the small one. A hundred sixty-nine pi minus a hundred forty-four pi is twenty-five pi, just like the rule says.  
  _shown:_ f9rings_r1b @ "A hundred sixty-nine pi minus"
- **3.4** Radii five and five root two, a silver triangle with legs five and five. Five root two, squared, is fifty. Fifty pi minus twenty-five pi is twenty-five pi again.  
  _shown:_ f9rings_p2 @ "Radii five and five root two"; f9rings_p2a @ "Five root two, squared"; f9rings_p2b @ "Fifty pi minus twenty-five pi"
- **3.5** And here's the limiting picture, where the small circle has shrunk to a single point, the center. Then the chord goes through the center, so it's a diameter of ten. The ring becomes a whole circle with radius five, twenty-five pi. The same answer.  
  _shown:_ f9rings_p3 @ "the limiting picture"; f9rings_p3a @ "twenty-five pi. The same"
- **3.6** So when two circles have the same center, and a chord of the big circle touches the small circle, we find the ring's area like this. Take half the chord, square that length, then multiply by pi. [pause] Okay. I'll see you in the next part.  
  _shown:_ f9t11a @ "So when two circles have the same center"; f9t11 @ "Take half the chord"

#### r26-t33-more-tools-3 slide 1 "More Circle Tools (Part 3 of 3)"
- **1.1** Here's one more circle tool.  
  _shown:_ —

#### r26-t33-more-tools-3 slide 2 "A trapezoid in a circle"
- **2.1** The third tool is a trapezoid inside a circle. When a trapezoid is inscribed in a circle, it's always an isosceles trapezoid. Let's see why, with two rules we already know.  
  _shown:_ f9trap_line @ "The third tool is a trapezoid"; f9z7 @ "it's always an isosceles trapezoid"
- **2.2** Here's trapezoid A B C D, inscribed in a circle. A B is parallel to D C. Say angle A is seventy.  
  _shown:_ f9z1 @ "A B is parallel to D C"; f9trap_a70 @ "Say angle A is seventy"
- **2.3** First, the trapezoid rule. Two angles on the same leg add up to one hundred eighty. Angles A and D are both on the leg A D. So angle D is one hundred eighty minus seventy, which is one hundred ten.  
  _shown:_ f9trap_d110 @ "So angle D is one hundred eighty minus"; f9z2 @ "So angle D is one hundred eighty minus"
- **2.4** Now the circle rule. In an inscribed quadrilateral, opposite angles add up to one hundred eighty. Angle C is opposite angle A. So angle C is one hundred eighty minus seventy, which is one hundred ten too.  
  _shown:_ f9trap_c110 @ "So angle C is one hundred eighty minus"; f9z3 @ "So angle C is one hundred eighty minus"
- **2.5** So angle C and angle D are equal, and they're the two angles on the base D C. Angle B is on the same leg as C, so it's one hundred eighty minus one hundred ten, which is seventy. That's the same as angle A. So the base angles are equal on both bases.  
  _shown:_ f9trap_b70 @ "minus one hundred ten, which is seventy"; f9z4 @ "So the base angles"
- **2.6** And equal base angles give equal legs. Drop the heights from D and from C to the base A B. We get two right triangles with the same height and the same angle of seventy at the bottom. So they're the same triangle, and their long sides are equal. Those long sides are the legs A D and B C. So the trapezoid is isosceles.  
  _shown:_ f9trap_h @ "Drop the heights"; f9trap_legs @ "Those long sides are the legs"; f9z5 @ "So the trapezoid is isosceles"
- **2.7** Seventy was just an example. Say angle A is sixty-four. Then angle D is one hundred sixteen, because it's on the same leg as A. And angle C is one hundred sixteen too, because it's opposite A. They're equal again, for any angle.  
  _shown:_ f9z6 @ "Then angle D is one hundred sixteen"
- **2.8** So when a question says a trapezoid is inscribed in a circle, you know right away that it's isosceles. Its legs are equal, its base angles are equal, and its diagonals are equal too. And a trapezoid with unequal legs can never be inscribed in a circle. Now let's see the other two tools in questions, and I'll see you in the next video.  
  _shown:_ —


---

## 3. Topic 33: a trapezoid inscribed in a circle is isosceles (r26-t33-more-tools, now 3 parts)

**Where and why there.** geo-075 (the inscribed-quadrilateral rule) is recorded, and so are g076 and q-r26-t33-01. The
unrecorded topic-33 videos after it: geo-077 (tangents), g078, q-r26-t33-02, geo-079 (area), g080, q-r26-t33-03,
geo-081 … g092, geo-093 … g102, r26-t33-more-tools, q-r26-t33-04/05. None of the questions uses an inscribed
quadrilateral (grep: only geo-075 / g076 do). The lesson "More Circle Tools" is a lesson of extra circle rules for harder
questions, so the rule goes there as its third tool, in its own part (r26-t33-more-tools-3). No proposal needed.
**Prerequisites (said as reminders):** inscribed quadrilateral, opposite angles 180° (geo-075); two angles on one leg of
a trapezoid add up to 180° (topic 32 trapezoid lesson). The step "equal base angles → equal legs" is NOT taught in topic
32 (it teaches only the other direction), so it gets its own reason: the two heights give two right triangles with the
same height and the same 70° angle. **Numbers:** A = 70 → D = 110 (leg AD), C = 110 (opposite A) → B = 180 − 110 = 70;
second run A = 64 → D = C = 116. Checked on the figure coordinates (70, 70, 110, 110). Helps on 2024_autumn_q1_13-type
"can / can't be inscribed" items.

### Changes to existing paragraphs (r26-t33-more-tools)
- Title slide. BEFORE: "Here are two more circle tools. They come up in some of the harder circle questions. And right
  after this lesson, two questions teach two more tools." AFTER: "Here are three more circle tools. …" (rest unchanged).
- "Same chord, same ring", last paragraph. BEFORE: "So when two circles have the same center, and a chord of the big
  circle touches the small circle, we find the ring's area like this. Take half the chord, square that length, then
  multiply by pi. Now let's see the other two tools in questions. [pause] Okay. I'll see you in the next video." AFTER:
  "…then multiply by pi." (the part closing "Okay. I'll see you in the next part." is added automatically; the goodbye
  moved to the end of the new trapezoid slide).
- `MORE_SPLITS`: parts at "Two equal circles" (part 1), "Chord of a ring" with "Let's continue with more circle tools."
  (part 2), "A trapezoid in a circle" with "Here's one more circle tool." (part 3).
- Summary page t33.json: new rule row "Trapezoid in a circle: always **isosceles** | same leg 180° + opposite 180°: equal
  base angles | 70°: ∠D = ∠C = 110°".

### Board / visual requirements (`f9trap`)
Circle with trapezoid ABCD (AB bottom, DC top, parallel arrows) at "The third tool is a trapezoid"; angle A 70° (teal) at
"Say angle A is seventy"; leg AD thick teal + angle D 110° (orange) at "So angle D is one hundred eighty minus"; angle C
110° at "So angle C is one hundred eighty minus"; angle B 70° at "minus one hundred ten, which is seventy"; the two dashed
heights with right angles and the two right triangles tinted at "Drop the heights"; double ticks on AD and BC at "Those
long sides are the legs". Rows: Trapezoid in a circle ⇒ isosceles / AB ∥ DC / leg AD: ∠D = 180° − 70° = 110° /
opposite: ∠C = 180° − 70° = 110° / ∠C = ∠D, so ∠A = ∠B = 70° / Legs: AD = BC, isosceles / 64°: ∠D = ∠C = 116°.

### Read-aloud check
Read against `fr/r26-t33-more-tools-3`. "They" (the two right triangles), "their long sides" → named "the legs A D and
B C" in the next sentence. Fixed after looking: the labels A and B were cut at the sides (B looked like "E"; view box
widened) and the 70° labels sat on the dashed heights (moved closer to the corners). Ready.

---

## Checks
- Spec runs `python3 math_patches/_ai_vis_t33.py` and `_ai_vis_t34.py`: no PROBLEMS.
- Private builds only: `scratchpad/xf-Q/test.html` and `testhw.html` (AI_HANDWRITE=all).
- `SRC=test.html python3 ai_check.py` on geo-104, -2, -3, -4, -5, geo-097-after, -2, r26-t33-more-tools, -2, -3: all OK
  (notes only: "three hundred sixty" wording, as before).
- `math_check.py 33 34`: PROBLEMS 0 / WARNINGS 0; layout: 1 finding, `solve-geo33-g089 #2 items 0.1 and 9 overlap`, a
  video I did not touch (topic 33 rebuilds every video, so it is listed; it was not part of this change). The earlier
  layout finding on my "Count the sides" slide (a row off the slide in the typed build) is fixed. Same with AI_HANDWRITE=all.
- `w19_check.py` on the changed parts: the new dense sentences were split; left as is: "Why half? Because…" (W15, the
  answer is in the same line) and the transitions "First, the trapezoid rule." / "Now the circle rule." (lead into full
  sentences, allowed by W19).
- Frames of every changed slide rendered from the handwriting build and looked at (`scratchpad/xf-Q/fr/<vid>/sheet_*.png`):
  no early results, rows readable, no overlaps after the fixes listed in the read-aloud notes.
- Summary pages t33 / t34 rebuilt privately (`scratchpad/xf-Q/sum33.html`, `sum34.html`): math checks pass, one page each.

## Proposals for recorded videos
None needed: all three additions fit unrecorded videos. (Optional, only if geo-075 is ever re-read: after the inscribed-
quadrilateral rule one sentence "We'll see later that a trapezoid inside a circle is always isosceles." — not worth a
re-read on its own.)

## Needs Claude
1. **New part videos** geo-104-5, geo-097-after-2, r26-t33-more-tools-2, r26-t33-more-tools-3 appear in the Reading
   Studio / `video_status.py` only after the next shared studio + Reading Studio rebuild (I built privately only). The part
   titles change to "Polygons (Part k of 5)", "Four Nested Shapes (Part k of 2)", "More Circle Tools (Part k of 3)".
2. **Prompter display:** "nine π", "four π" stay words while "36 π", "16 π" become digits (geo-097-after-2, The ring);
   "36 π −9 π" lacks the space after the minus. Wanted: "9π", "4π", "36π − 9π".
3. **Crossing-diagonals figure** (geo-104-5 slide 2): the triangle BPC is small inside the whole hexagon, so its three
   angle labels (30°, 120°, 30°) are small (16-18 px). Readable, but an enlarged cut-out of triangle BPC (like the
   enlarged segment in q-r26-t33-04) would be nicer if Codex flags it.
