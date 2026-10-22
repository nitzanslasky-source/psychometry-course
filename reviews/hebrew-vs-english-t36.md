# Topic 36 (Similarity and scale): the teacher's Hebrew videos vs the English course

Read-only review, 2026-10-22. Nothing in the course was changed.

- Hebrew source: `~/Downloads/03-Geometry-Original-Subtitles.txt`, lines 7030-8586 (all of it read).
- English: `scratchpad/ext/course/t36.txt` (every video's spoken text) and `q36.txt` (practice questions), the current flow in
  `~/Downloads/Psychometric-Teacher-Studio-v19-hybrid.html`, the base translation `studio-build/base-v18.html` (flow checked).
- **Recording status:** topic 36 has no reading scripts in `ai_scripts/` yet (only `r26-t36-summary.json`), so none of its
  videos are in the `video_status.py` tracker. **Nothing in topic 36 is recorded**; every target below is unrecorded.

**Match scale.** New numbers alone are not a change (memory rule *questions-differ-from-hebrew*).
SAME = same idea and every one of her methods. CHANGED = same idea, but the method, the example type, the claim or the order
differs (the cell says what). PARTIAL = some of her content or one of her methods is missing. MISSING = no English equivalent.

**Her names carry over:** יחס קווי / יחס שטחים / יחס נפחים → "linear (length) ratio / area ratio / volume ratio"; טבלת משולש קטן–גדול →
"the small–big table"; ערך משולש → "multiply diagonally, divide by the one left"; קו מקביל לבסיס / דמיון באלכסון (אנך ליתר) / שעון חול →
"parallel to the base / altitude to the hypotenuse / hourglass"; האיש עם המשקפיים → "the man with glasses" (Kenny, Batman kept);
דמיון חלקי → "partial similarity"; יחידות יחס → "ratio units".

**Id numbering.** geo-134 (lesson 1), geo-135 (lesson 2), g136-g138 (her 3 regular-shape questions), geo-139 (lesson 3), g140,
geo-141 (lesson 4, 3D), g142, geo-143 (lesson 5, volume changes), g144-g151 (her 8 sample questions). Every one of her segments has
an id, in her order; there are no gaps inside the topic (geo-133 and geo-152/153 do not exist as geometry ids; they sit at the
topic boundaries and no video of hers is missing there).

---

## 1. Hebrew → English (her videos, in her order)

| # | Her video (Hebrew title · English gloss) | Lines | What she teaches / how she solves it (every method) | English equivalent | Match |
|---|---|---|---|---|---|
| 1 | דמיון – יחס קווי ויחס שטחים · Linear ratio and area ratio | 7031-7219 | Why similarity comes last; similar = same shape, other size; same size = congruent. Matching lines (radius↔radius, not diameter↔chord); the linear ratio is constant for every pair (2→4); angles don't change; not only sides: heights, medians, diagonals, even differences of sides; squares (diagonal ×2 → side ×2). Area ratio = linear²: square 1→2 = 4 small squares; grid triangle 1,2 → 3,6 = 9 small triangles; circle 1:2 → 1:4. **The "man with glasses" (Kenny / Batman) pattern**: two small circles on the diameter → the top leftover = one small circle. Recap | geo-134 (all slides) | SAME (square 2→6 = 9, triangle 1,2 → 4,8 = 16; small circle = 3 units). English adds a worked "difference of sides" example (8−5 → 16−10) and "square both parts / take the root of both" (16:25, 25:49 → 5:7) |
| 2 | דמיון בצורות משוכללות · Regular shapes | 7221-7279 | Regular shapes are always similar. Equilateral 1:2 → 4 small inside; squares 3:5 → 9:25 (as units: 9 → 25, 18 → 50); hexagons 2:3 → 4:9 ("think before I reveal"); circles 1:3 → 1:9; **circumference is a line → linear ratio** (4 → 12) | geo-135 | SAME (1:3 → 9, 4:7 → 16:49, 5:6 → 25:36, 2:5, 8 → 20). English adds: same number of sides only; rectangles and right triangles are NOT automatically similar |
| 3 | מחומש משוכלל – צלע ×3 · Regular pentagon, side ×3 | 7281-7302 | Draw it (5x → 15x), then: no need, side is a line, perimeter is a line → ×3 | solve-geo36-g136 (decagon, ×5) | SAME (English adds the trap 25 = area) |
| 4 | שלושה מעגלים על הקוטר · Three circles on the diameter, R = 5 | 7304-7380 | Radius 5/3 is "annoying" (מעפן), so use similarity: small r, big 3r → circumferences 1:3 → three small = one big = 10π. General rule: the big circumference = sum of the circumferences on its diameter, any number, even different sizes | solve-geo36-g137 (six circles, R = 9 → 18π) | SAME (English adds that this holds for circumferences only: the six circles cover a sixth of the area) |
| 5 | מעגל על AO – כהה מול לבן · Circle on AO, dark : white | 7382-7438 | Linear 1:2 → areas 1:4, but they asked dark : white → 4 − 1 → 1:3. **Her tip:** the answers usually help, not confuse; a common mistake (1:4) usually does NOT appear among the choices, so if your answer isn't there, reread the question; only in very easy questions may the common-mistake answer appear; the harder the question, the more the answers help. Closing: you can always calculate (x, 2x), but similarity takes seconds | solve-geo36-g138 (AC = ¼ AB → 1:16 → 1:15) + slide 2 (plug in numbers) | **CHANGED: her tip is reversed.** English keeps "usually they don't confuse me, they help me", then says "A trap answer can be there at any level, in easy questions and in hard ones. Like here: 1 to 16 is choice 1", the opposite of her "the common-mistake answer usually won't be there". The units method and the plug-in alternative are kept |
| 6 | דמיון בצורות לא משוכללות · Non-regular shapes: triangles and rectangles | 7440-7751 | AA (two angles enough); matching sides = opposite equal angles; **"from years of experience": make a small–big table, then the triangle value finds the missing side**; turning the triangle doesn't matter; the ratio between two sides inside one triangle is equal too (6/8 = 3/4); a fraction = a colon. Exam types: (1) parallel to the base, common mistake AE ↔ EC (EC is not a side); (2) "diagonal similarity" / altitude to hypotenuse, almost only in right triangles, matching sides sit on different sides of the drawing; (3) hourglass (Z angles, a side matches its continuation). Rectangles: check both ratios, or the ratio inside each rectangle; on the exam: a rectangle with its corner on the big one's diagonal → similar, including the leftover pieces. ~90% of questions are triangles or rectangles | geo-139 (all slides) | SAME (every point; English adds the part-to-part rule for a parallel line, the two altitude-to-hypotenuse shortcuts (altitude² = product of the parts; leg² = its part × hypotenuse), a numeric rectangle-on-diagonal example (12×8, 9 → 6) and the SSS/SAS theorems as rare). Note: the lesson's table slide says "find what's missing" without naming her triangle-value step; it is used later, in g145 ("multiply diagonally, divide by the one left") |
| 7 | DE מקביל לבסיס – כהה : לבן · Parallel cut, triangle : trapezoid | 7705-7743 | Common mistake: ratio 2:1 (DB is not a side); opposite the equal angle → the whole AB: 2:3 → 4:9 → trapezoid 5 → 4:5 | solve-geo36-g140 (AD 4, DB 3 → 16:33) | SAME (English adds the traps 16:49 and 4:7) |
| 8 | דמיון בגופים תלת-ממדיים · Similar solids | 7753-7817 | Volume ratio = linear³; similar solids: all matching edges (height, radius) in one ratio; cubes always similar: 1→2 = 8 small cubes (area 1:4, volume 1:8); cylinders/cones similar only if radii AND heights share the ratio (2:3, 4:6 → 4:9, 8:27); "check that they are really similar" | geo-141 | SAME (1→4 = 64; radii 2:4, heights 4:8). English adds: surface area is still squared; all spheres are similar; the half-height cone glass holds ⅛ |
| 9 | פאת קובייה גדולה פי 9 · Face area 9×, how many small cubes | 7819-7849 | Area given, volume asked → in-between step: root → linear 1:3 → cube → 27 | solve-geo36-g142 (36× → 1:6 → 216) | SAME (English adds the layer check 6×6×6 and the traps 36, 1296) |
| 10 | יחסי נפחים · Volume changes | 7851-7984 | Cube edge ×3: count (9 per floor × 3 = 27) and the formula (3a)³ = 27a³; cylinder/cone: height only → direct (can on a can); radius → square of the change, via the formula π(3r)²h = 9πr²h; cone height ×3 → ×3 (the 3s cancel); recap: cube cubed, cylinder/cone "check what changed and by how much" | geo-143 | SAME (edge ×5 = 125; radius ×2 = 4). English adds: both change → multiply the factors; factor vs percent (×4 = +300%) |
| 11 | AB ∥ ED – אורך AC · Parallel cut, find AC (medium) | 7986-8071 | AA proof. (1) Full math: small/big in a fixed order, cross-multiply, gather x on the side with more x → 9 → 12; also inside one triangle (6/x = 8/(x+3)), "swap x and 8, the same equation". (2) Psychometric: parts of sides: BD : DC = AE : EC (1:3) → EC 9; or across (2 → 3 is ×1.5 so 6 → 9). Verdict: here the psychometric way is much shorter | solve-geo36-g144 (BD 10, DC 15, AE 4 → AC 10) | SAME (every method; the "across" ratio is AE = 0.4 of BD → 0.4 × 15). English adds the reminder that ED itself must go against the whole side |
| 12 | ריבוע במשולש ישר זווית · Square in a right triangle, find BE (medium+) | 8073-8164 | Three similar triangles (α, 90−α). (1) Full math with the two small triangles (her personal preference), fixed order, triangle value → x²/2. (2) Plug in numbers: "unknowns in question and answers → plug in"; not 1 (legs 2 and 1, not a known triangle) but x = 2 → silver triangles, congruent → BE = 2; plugging only eliminates; her preference here: plug in | solve-geo36-g145 (AF = 5 → x²/5, plug in x = 5) | SAME (every step, her preferences kept) |
| 13 | גובה ליתר – AD · Altitude to the hypotenuse, BD 4, DC 9 (hard) | 8166-8241 | Plug in a numeric angle (20°, 70°) to see what matches; warning: don't plug in 45° and conclude silver (contradiction); "a number seems missing": only two numbers but the equation has four parts; work inside the same triangle: AD/BD = DC/AD → AD² = 36 → 6 | solve-geo36-g146 (3 and 27 → 9) | SAME (every step). English adds the shortcut "altitude² = the two parts multiplied" and a Pythagoras check |
| 14 | מעגלים קונצנטריים – יצחק וניצה · Concentric circles, two claims (medium+) | 8243-8317 | (1) Circle formulas: 3πr vs 2πr → Yitzhak right; ring 9/4 − 1 = 5/4 > 1 → Nitza right → both. (2) Similarity: perimeter is linear → ×1.5 immediately; areas: **expand 1:1.5 → 2:3 (no fractions)** → 4:9 → ring 5 > 4 | solve-geo36-g147 (r and 1.3r; Noah / Emma) | SAME in method (both ways; the "expand to whole numbers" step: 1:1.3 → 10:13 → 100:169, ring 69 < 100). The result differs on purpose: with 1.3 the ring is smaller, so only Noah is right (English adds the warning "the ring looks big in the figure"). **Error in English:** the two slide titles are "Circles way · Liam" and "Circles way · Maya", but the people in the question are Noah and Emma |
| 15 | קטע אמצעים – שטח הטרפז 6 · Midpoint segment, trapezoid 6 (medium+) | 8319-8422 | Midsegment ∥ third side → similar. (1) Full math with y, h, 2h → yh = 4 → 2. (2) Linear 1:2 → areas 1:4 → trapezoid 3 units = 6 → 2. (3) The midsegment rule: join the three midpoints → 4 congruent triangles (3 parallelograms) → 6/3 = 2. Preference: know the rule → shortest; else the ratios; default the full math | solve-geo36-g148 (trapezoid 21 → 7) | SAME (all three ways and her order of preference) |
| 16 | שני משושים משוכללים · Two regular hexagons, perimeter ratio (medium+) | 8424-8490 | (1) Hexagon = 6 equilateral triangles → sides √8 and 2 → √8 = 2√2 → √2 : 1. (2) Similar (same family) → area ratio 2:1 → root → √2 : 1 | solve-geo36-g149 (150√3, 30√3 → √5 : 1) | SAME |
| 17 | רעשן – שני כדורים · A rattle, two spheres (medium) | 8492-8518 | Psychometric only: spheres similar; small diameter = big radius → 1:2 → 1:8 → difference 7 units → 7 | solve-geo36-g150 (small diameter = half the big radius → 1:4 → 63) | SAME (the extra half adds one step; English adds "radius with radius" and the trap 64) |
| 18 | כף מדידה חרוטית · Measuring cone, h/3 and r/5 (medium+) | 8520-8583 | (1) Full 3D math, compare numerators only (same /3) → 75. (2) Partial similarity: the cones aren't similar, but bases (circles) and heights (lines) are → height ×3, radius ×5 → ×25 → 75 | solve-geo36-g151 (h/6, r/2 → 24) | SAME |
| 19 | 20 שאלות תרגול עצמי · 20 self-practice questions | 8586 | — | geo36-core-p01 … p27 (q36.txt) | SAME (kept, more added) |

**Count by row (19 rows):** SAME 18 · CHANGED 1 (5) · PARTIAL 0 · MISSING 0.

### Count by video (her 19 units)

| Unit | Match |
|---|---|
| Lesson 1 linear / area ratio | SAME |
| Lesson 2 regular shapes | SAME |
| Q pentagon (g136) | SAME |
| Q circles on a diameter (g137) | SAME |
| Q dark : white circle (g138) | CHANGED (her "answers help, the common mistake usually isn't there" tip reversed) |
| Lesson 3 non-regular shapes | SAME |
| Q parallel cut 4:5 (g140) | SAME |
| Lesson 4 similar solids | SAME |
| Q face area 9× (g142) | SAME |
| Lesson 5 volume changes | SAME |
| Q8-Q15 sample questions (g144-g151) | SAME (8 videos) |
| 20 practice questions | SAME |

**By video: SAME 18 · CHANGED 1 · PARTIAL 0 · MISSING 0.**

---

## 2. English → Hebrew (English topic-36 parts with no Hebrew equivalent = added)

| English video / part | Added content | Hebrew source? | Recorded? |
|---|---|---|---|
| geo-134 slides "Not only sides" (part), "Square both parts" | Worked difference example; ratios without a 1 and backwards with roots | none (her rule is stated, not worked) | no |
| geo-135 slide "Always similar" (part) | Same number of sides; rectangles / right triangles not automatically similar | none | no |
| geo-139 slides "Part to part", altitude shortcuts, rectangle example, recap line on SSS/SAS | The part-to-part rule; altitude² = product of parts; leg² = part × hypotenuse; other similarity theorems | her g144 uses part-to-part; the rest none | no |
| geo-141 slides on surface area, spheres, "Half-height cone" | Surfaces squared; all spheres similar; a cone filled to half its height holds ⅛ | none | no |
| geo-143 slides "Both change", "Factor vs percent" | Multiply separate factors; ×4 = +300% | none | no |
| solve-q-r26-t36-01 | Same height, not similar → areas follow the bases (no squaring) | none | no |
| solve-q-r26-t36-02 | Trapezoid with diagonals: a², b², ab, ab | none | no |
| solve-q-r26-t36-03 | Cube edge +20% → volume +72.8% | none | no |
| r26-t36-map-scale, solve-q-r26-t36-04, -05 | Map scale: lengths ×n, areas ×n², the unit ladder | none (the topic title "and scale" is English-only) | no |
| solve-geo36-g146 slide 3 | Pythagoras check | none | no |
| traps added in g136, g140, g142, g150 | 25, 16:49, 36 / 1296, 64 | none | no |
| r26-t36-summary, mem-similarity, mem-similar-triangles, mem-similar-solids, mem-r26-t36-map-scale | Summary and reference cards | none | no / — |
| practice geo36-core-p21 … p27, the r26 practice questions | Extra practice | none | — |

---

## 3. Missing from English: restore?

| # | Her content | Where it would go | Target recorded? | Recommendation |
|---|---|---|---|---|
| 1 | **g138: her tip about the answers** ("in a harder question the common-mistake answer usually isn't among the choices; if yours isn't there, reread; only in very easy questions may it appear") | solve-geo36-g138 slide 2 | no | **Teacher's decision; do not restore as is.** The English deliberately says the opposite, and the English course everywhere teaches named trap choices (dozens of "X is the trap" lines, built into its questions). Her claim is hard to check and conflicts with the rest of the course. If she wants her idea kept, a version that fits both: "The choices are there to help: if the answer you expected is missing, you probably slipped, so read the question again. And if it IS there, check it anyway." (2 sentences). Note the current English half-contradicts itself: "usually they don't confuse me, they help me", then the trap is choice 1 |
| 2 | geo-139: name her triangle-value step after the small–big table ("then the triangle value finds the missing side") | geo-139 slide "Small–big table", 1 sentence | no | **Optional** (the step is used in g145); one sentence keeps her full method together where she teaches it |

## 4. Wrong in the English

- **solve-geo36-g147: the slide titles "Circles way · Liam" and "Circles way · Maya" don't match the people in the question,
  Noah and Emma** (the spoken text and the question stem use Noah / Emma). It is a leftover of an earlier rename: in
  `math_patches/t36.py` the question was first patched to 1.4r with Liam / Maya (line ~603), then renumbered to 1.3r with
  Noah / Emma (line ~1809), and the two slide titles were not updated. Fix them to "Circles way · Noah" / "· Emma".
- solve-geo36-g138: the answers tip contradicts her (see 3.1).
