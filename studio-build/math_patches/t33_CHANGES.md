# Topic 33 – Circles: changes (course review 2026-09)

`python3 math_check.py 33`: 0 problems, 0 warnings, 0 layout problems.

## 1. Wrong or unclear statements
- **Q1 (angle on the major arc), Method 3** was too short ("112 is 360 minus twice the angle"). It is now shown step by step on the board: base angles x and y, then (180° − 2x) + (180° − 2y) = 112°, so x + y = 124°.
- **Inscribed quadrilateral proof:** the note said "write 2α on the side facing A". The central angle 2α is on the side of C (it rests on arc BCD). Fixed.
- **Equal chords** slide: removed the SSS congruence proof (SSS is not taught in T31) and added a figure. It keeps only the rule and "join the ends to O".
- **Q16, Method 3:** "write 1+ on each of the three arcs" was only true for three 60° pieces. It now says: the curved part is half a circle, π·1, a bit more than 3.
- **Q20 estimate:** new reason. The circle fits in a 6 by 6 square, so 6·BC < 36 and BC < 6.
- **adv-p06:** the solution read "2p+3q:2". It now reads $2p+\frac{3q}{2}$.
- **p16:** "A kite with opposite angles of 90° and 72°" is now "A kite whose two unequal opposite angles are 90° and 72°".
- **Q2:** removed "Pavlov". It now says "Always, automatically — every time", and the slide title is "Automatic: draw the radii".
- **Q22:** the last line said "That's it for circles. On to the summary". A new lesson now comes after it, so the line was changed.

## 2. Methods that were used but never taught (now taught)
| Method | Where it is taught | Guided question (new, with solution video) | Practice |
|---|---|---|---|
| The perpendicular from the center cuts a chord in half: $d^2+(\frac{chord}{2})^2=r^2$ | new slide "Chord and center" (Angles in a Circle) | Q2: chord 16, distance 6 → circumference 20π | p22, adv-p21, new: parallel chords, "which statement is true" |
| Equal tangent pieces in a circle inside a triangle; right triangle $r=\frac{a+b-c}{2}$; quadrilateral around a circle $AB+CD=BC+AD$ | new slide "Circle inside a triangle" (Tangents) | Q4: legs 8 and 15 → r = 3 | adv-p26 (now has a figure), adv-p15, new: quadrilateral around a circle, new: BD in triangle 10-12-8 |
| Distance between the centers of touching circles: R + r and R − r | new slide "Tangent circles" (Tangents) | covered in the Q4 group videos and Q13 | new: internally touching circles (9 and 4 → 5), new: "which cannot be the distance" |
| Scaling: radius ×k → C ×k, S ×k² (T36 was needed early) | new slide "Scale the radius" (Area and Circumference) | Q6: circumference +50% → area +125% | p24, new: area ×9 → C ×3, new: radius −10% → area −19% |
| Wheel turns = distance ÷ circumference, with units | new slide "Wheels" | – | adv-p22 |
| Right triangle in a circle: hypotenuse = diameter; a rectangle's diagonal = diameter | extra line and board item on "Angle on a diameter" | (Q14 already uses it) | adv-p25 |
| Segment = sector − triangle; two equal circles through each other's centers (equilateral triangles, 120°, lens = 2 segments); common external tangent (right trapezoid, $DC=2\sqrt{Rr}$ for touching circles); chord of a ring (ring = πh²) | **new lesson video "More Circle Tools"** (end of "Further guided examples") | Q26: segment (radius 6, 60°); Q27: common tangent (radii 8 and 2 → 8) | adv-p23, adv-p27, adv-p20, adv-p21, new: ring from a 16 cm chord (64π) |

Guided questions are renumbered automatically. There are now 27 (22 + 5). The new ones are Q2, Q4, Q6, Q26 and Q27.

## 3. Text (every question and video)
- All 76 existing solutions were rewritten in TeX, with the numbers shown and fractions instead of ":". This covers "3π:2", "πr(1−α:90)", "144:360=2:5" and the others.
- Missing spaces were fixed ("radii,8", "totaling(π+2)r" and the others).
- Givens are now stacked with `cases` in the stems of Q11 (was Q8), Q47 (was Q18), Q51 (was Q22), p23 and adv-p15, and in 2 new questions.
- Q18 now says where B and C are: "B and C lie on the arc AD that does not contain F".
- Q12 no longer says "α-sector". It says "one sector with angle α".
- Board items with ":" as division now use fractions: Q1, Q2, Q7, "On a diameter", "25π÷5".
- The colons inside the math on Q21 and Q22 were moved out of the math.
- The on-screen question copies ("non−overlapping") were refreshed from the stems.
- British spellings in the videos were changed to American (centre/CENTRE, centimetres, practise, Recognise).
- Q9: a "golden triangle" reminder box was added: 30°-60°-90° has sides x, x√3, 2x. The silver triangle box was already on Q8.
- Nested shapes, triangle case: the unproved claim was replaced by the picture. The inner triangle is turned upside down, and the outer triangle is 4 copies of it.

## 4. Figures fixed
- **Q6 (g085 + solution slides):** the "12" that read as "O12" was replaced by a dimension line under AB.
- **p05:** the center O is removed. The stem never mentions it, and it showed that AC is a diameter. The "8" was moved away from the center.
- **p15:** the center O is removed. It gave away that AC is a diameter.
- **Q15 (g095):** radius OD is no longer drawn in the question. The shaded region is now D–C–E–arc, with no edge OD.
- **Q12 (g091):** the 12 angle arcs that formed an unexplained inner circle are removed.
- **Q18 (g098):** B was moved (200° instead of 225°), so chord BF no longer looks like a diameter.
- **p20 and Q5 (g083):** the double "O" is removed.
- **p03, adv-p06:** the α and γ that the stems never mention are now "?". On p03 the "140°" was moved off chord CD.
- **p11:** the figure was redrawn. The "?" is at B. The 144° label was dropped because it could not fit inside the thin angle (the angle is given in the stem).
- **adv-p15:** redrawn so that only neighbors touch. B and D no longer touch, and neither do A and C.
- **Label overlaps fixed:** p19 (O), adv-p04 (a, 3c), adv-p11 (3t), Q24 (was Q21, the "C").
- **adv-p26:** new figure (right triangle 6-8 with its circle).
- **Lesson figures:**
  - The stray "A" on the circle slide is removed.
  - The inscribed quadrilateral is now clearly not a rectangle (A = 70°, C = 110°).
  - O is now drawn on the proof slide.
  - The "Quarters and eighths" slide starts with quarters; the teacher draws the eighth.
  - The nested triangles are shown upside down.
- **New figures:** equal chords, chord and perpendicular, circle inside a triangle, tangent circles, segment, two equal circles, common tangent, chord of a ring, and figures for the new questions.

## 5. Practice
- **Removed (near-duplicates):**
  - p09 and p13: "tangents → quadrilateral 360°", which was used 5 times.
  - p25 and adv-p08: "ring = big − small", which was used 5 times.
- **Added (9 new):**
  - Foundation: area ×9 → C ×? ; internally touching circles.
  - Advanced: quadrilateral around a circle; BD in a triangle with its inscribed circle; ring from a tangent chord; two parallel chords; "which statement is true" (chord 8 in radius 5); "which cannot be the distance between the centers"; radius −10% → area −19%.
  - That adds 2 more "which statement" questions.
- **Size:** 54 practice questions became 59 (foundation 26, advanced 33). Both sections are ordered easy → hard.
- **Memory cards:**
  - Circle rules card: added right angle → diameter, chord and center, circle inside a triangle, quadrilateral around a circle, and tangent circles (R ± r).
  - Formulas card: added scaling and wheel turns, plus a hexagon tip (side = radius).
  - New card "Circles — more tools".

## For the teacher to decide
- p11 no longer shows "144°" in the figure. It did not fit inside the angle. The value is only in the stem.
- Stems with stacked givens (Q47, Q51) make the question text smaller on the solution slides. This follows the "givens one on top of the other" rule.
- "Distance between the centers" (R ± r) has a lesson slide and practice questions, but no guided question of its own. The existing guided Q12/Q16 (tangent circles) use it.

## Pass 2 (teacher-approved remove/restore plan, 2026-09-27)
`python3 math_check.py 26 27 33 34`: 0 problems, 0 warnings, 0 layout problems.

**Removed (4 items)**
- Tangents video, slide "Circle inside a triangle": the board item "Quadrilateral around a circle: AB + CD = BC + AD" and its spoken line. The triangle part stays.
- Circle rules card: the row "Quadrilateral around a circle".
- Practice q-r26-t33-08 (quadrilateral around a circle) and q-r26-t33-13 (two circles meeting at two points).

**Restored**
- Practice: geo33-foundation-p09, -p13, -p25 and geo33-advanced-p08 are back. Their solutions are now in TeX with the numbers shown. The p13 givens are stacked. On p09 and p13 the unused "α" in the figure is now "?", as on the other figures.
- "Equal chords" slide: the original proof is back ("Join each chord's ends to the center: two triangles, radius, radius, equal chord — identical triangles"). The new figure stays.
- Q3 solution (tangents): the "Pavlov" line is back.
- "Let's solve a sample question." / "Let's see a psychometric question." are still spoken at the end of the Tangents and the Area and Circumference lessons. A sample question still follows each one.
- Q22 closing line: not restored. It is no longer the last circles video, because "More Circle Tools" and the new summary come after it.
- Received from other topics: wp26-p10 (rough circular floor, answer $\frac{3\pi}{4}$ hours) and wp27-p10 (runners on a circular track, central angle 60°). Both are in the foundation practice. wp26-p10 comes after the circle-area items and wp27-p10 after the central-angle / arc-fraction items.
- Practice size: foundation 26 → 31 (3 restored, 2 moved in), advanced 33 → 32 (2 removed, 1 restored). Both sections are still ordered easy → hard.

**Summary lessons (new)**
- `r26-t33-summary` "Circles: Summary", at the end of "Learn and try", right before the foundation practice. Slides: Summary · Radii · Central and inscribed · Diameter, quad · Chords · Tangents · Circle in a triangle · Area and circumference · Sectors and arcs · Before you practice.
- `r26-t33-summary-2` "Advanced Circles: Summary", at the end of "Further guided examples", right before the advanced practice. Slides: Summary · Shaded areas · Segments · Nested shapes · Special triangles · Tangent and ring · The whole, not the parts · Numbers and estimates · Before you practice.

## 2026-10-05 cut repeats
Function `cut_repeats` (runs last). A lesson slide is cut only when a question video after it teaches the same idea again. Nothing in topic 33 is recorded.
- **Angles in a Circle** (`geo-075`) 5.2 → 4.3 min. CUT slide 9 "Chord and center" (not in the Hebrew lesson): the next question video `solve-q-r26-t33-01` teaches it (perpendicular from the center halves the chord, the radius is the hypotenuse, Pythagoras). Slide 8 "Equal chords" now ends "Now let's solve a sample question." KEPT slide 8 "Equal chords": `solve-geo33-g087` uses equal chords → equal angles, but not equal arcs and not the reason.
- **Tangents** (`geo-077`) 3.4 → 2.0 min (Hebrew 1.6). CUT slide 5 "Circle inside a triangle" → `solve-q-r26-t33-02` (equal tangent pieces from each vertex, the little square at the right angle, leg + leg − hypotenuse over 2; the lesson example 6-8-10 was the same kind of question). CUT slide 6 "Tangent circles": joining the centers and R + r are taught in `solve-geo33-g088` (OM = 4 + 4) and `solve-geo33-g092`. MOVED into `solve-geo33-g088` slide 3 one line, "Two circles touch? Join the centers. Outside each other — R plus r. One inside the other — R minus r.", with the board item "Touching circles: outside R + r · inside R − r" (2.5 → 2.7 min). Slide 4 now ends "Let's solve a sample question." Sidebar: 3 labels.
- **Area and Circumference** (`geo-079`) 4.8 → 4.2 min. CUT slide 8 "Scale the radius" → `solve-q-r26-t33-03` (lengths grow like r, areas like r²). MOVED its backwards line into `solve-q-r26-t33-03` slide 2: "It works backwards too: the area 9 times bigger — the radius only 3 times bigger." + board item "Backwards: S × 9 → r × 3" (1.0 → 1.1 min). KEPT slide 9 "Wheels" (no question video teaches it).
- **More Circle Tools** (`r26-t33-more-tools`) 2.5 → 1.3 min, 5 → 3 slides. CUT slide 2 "Segment" → `solve-q-r26-t33-04` (sector minus triangle). CUT slide 4 "Common tangent" → `solve-q-r26-t33-05` (same numbers 8 and 2, same steps, same 2√(Rr) shortcut — the question equaled the lesson example). Title slide: "Two more tools for the hardest circle questions. Two more come in the questions after this lesson." Slide "Two equal circles" no longer uses the word "segment" before it is taught: "The shaded region is two equal pieces. Each one: a 120-degree sector minus the triangle AOB." Board: "Common region = 2 × (sector − triangle)". KEPT "Two equal circles" and "Chord of a ring". Sidebar: 2 labels.
- Summaries `r26-t33-summary` / `-summary-2` still sum up every cut idea; all are now taught in question videos — no change needed.

## 2026-10-06 renumber pass
So the English course does not look like the Hebrew one: every Hebrew-derived question in topic 33 has new numbers
(and new letters / a changed story where there is one). Concept, trap, level and methods stay the same. Every guided
solution video was rewritten to match (spoken lines, draw cues, board items, slide titles that quote numbers), and every
changed figure was redrawn or relabelled. Function `renumber_pass(M)` runs last in `apply()`, after `cut_repeats`.
Nothing in topic 33 is recorded (checked ~/Documents/Course.recordings), so `RN_RECORDED` is empty.

**Counts:** 22 guided questions renumbered, with 22 solution videos rewritten (7 rewritten slide by slide: g083, g092,
g094, g095, g100, g101, g102; the others by exact number swaps, plus a choice-order map for "choice N"). 40 Hebrew
practice questions plus wp26-p10 and wp27-p10 (Hebrew word problems that live in this practice) renumbered = 42.
Lesson / summary / card examples changed: 6 (see below). **Practice 63 → 49** (foundation 24, advanced 25).

**Lesson examples:** Angles in a Circle: "70° at A, 110° at C" (the Hebrew example) → 75° / 105°. Sectors and Arcs,
"Fifths": "circle 25π → sector 5π" (the Hebrew example) → 40π → 8π. Summary 1: "r = 5, d = 3 → chord 8" (same as
q-r26-t33-11/12) → "r = 17, d = 8 → half chord 15 → chord 30". Summary 2: "4α + 4β = 360° → α + β = 90°" (the Hebrew
g091) → "3α + 3β → 120°". More-tools card: "radius 6, 60°: 6π − 9√3" (= guided q-r26-t33-04) → "radius 12: 24π − 36√3";
"radius 4: 32π/3 − 8√3" (= adv-p27) → "radius 6: 24π − 18√3".

**Practice clean-up:** copies removed: f-p25, q-r26-t33-14, adv-p26 (list verified: ring ratio, radius −10%, incircle 6-8-10
= guided q-02). September items: kept q-07 (internal tangency), q-09 (incircle tangent lengths), q-10 (chord of a ring),
q-11 (two parallel chords) – the Hebrew practice has none of these types. Removed q-06 (area ×9 → circumference ×3 is the
board line "Backwards: S × 9 ⇒ r × 3" in guided q-03's video) and q-12 (same chord-distance type as q-11). English extras:
kept 3 warm-ups that practise lesson content with no other practice: f-p21 (sector perimeter), adv-p22 (wheel turns),
adv-p27 (two circles through each other's centers). Removed f-p22, f-p23, f-p24, f-p26, f-p27, adv-p21, adv-p23, adv-p24,
adv-p25. The order (easy → hard) is unchanged.

**Kept on purpose:** the English-made guided q-r26-t33-01 … 05 and their videos. g087 keeps its statement order (the video
goes statement by statement, the false one stays choice 4). g096 and g097 are letter-only questions: new letters (K, M, N /
KLMN, PQRS) and new choice order; the answers ((π + 2)/3 and 1/2) cannot change. g088 keeps 120° (only the radius
matters) – radius 7 and a new key position. The "angles to know" table (90 = ¼ …) and "72 + 72 = 144" stay: they are
general facts, not worked examples. f-p03 (140° → 128°), g076 (112° → 104°), g078, g086, f-p07, f-p09, f-p13, adv-p05
figures were relabelled only (the angle changes by ≤ 16°, the drawings stay not to scale but not misleading). The correct
answer moved in 17 of 22 guided questions.

**Checks:** every answer recomputed in Python (all keys); every method in each video recomputed with the new numbers
(g076 three routes, g078 two routes, g086 two routes, g094 subtraction + elimination + estimates 38.5 / 43.7 / 7.7,
g095 partial calculation + sector, g096 r = 2 plug-in, g099 estimate > 54π, g100 bound BC < 8, g101 plug in 3 then 4,
g102 θ = 15 plug-in). Traps are still in the choices (180 − angle, half the wrong arc, the central angle, π ≈ 3, diameter
for radius, arc vs area, wrong sector, double triangle, negative area, answers with r). New numbers checked against the
Hebrew subtitles (90/135, 40/140/70, r 3 arc 2π, r 4 45°+90°, AB 8, 30°, AO 1, 6π/16π, 5-12-13, √12 with 4+4 angles,
radii 1-2-3, r 2 / 6 / 1, 20°-55°-90°, CB 4 & 16π): none land back on them; Pythagorean triples are 12-35-37 and
20-21-29 (not 3-4-5 / 5-12-13 / 6-8-10). Duplicate scan over topics 1–33 (questions and lesson lines): no question equals
another question or a lesson / card example (adv-p19 moved from r = 4 to r = 8 because "r = 4, 45° → 2π" is a summary
example). `python3 math_check.py 33 32` and `math_check.py 26 27 33` → PROBLEMS 0, WARNINGS 0, LAYOUT 0. Rendered and
looked at g076, g082, g083, g087, g090, g092, g094, g095, g098, g099, g100, g101, g102 and all changed question figures.
No "Question N" was added to spoken lines.

| id | old (English, Hebrew-derived) | new | answer |
|---|---|---|---|
| geo33-g076 | AOC 112° → ABC 124° | AOC 104° | 128° (2) |
| geo33-g078 | tangents, DPE 52° → 64° | DPE 68° | 56° (4) |
| geo33-g080 | area = 3 × circumference → r 6 | 4 × | 8 (1) |
| geo33-g082 | r 6, arc 3π → 90° | r 10, arc 4π | 72° (3) |
| geo33-g083 | r 6, sectors 60° + 90° → 15π | r 3, 40° + 120° | 4π (3) |
| geo33-g085 | AB 12, AOC 120° → 9√3 | AB 20 | 25√3 (4) |
| geo33-g086 | isosceles, A 40° → ABO 20° | A 56° | 28° (1) |
| geo33-g087 | 4 equal chords, AO 3, false AC = 3√3 | AO 5, AC = 5√3 | statement 4 (4) |
| geo33-g088 | tangent congruent circles r 4 → 120° | r 7 | 120° (3) |
| geo33-g089 | small C 8π, ring 65π → 56–57 | small C 10π, ring 39π | 50–51 (4) |
| geo33-g090 | sides 7, 24, 25 → 25π | 12, 35, 37 | 37π (2) |
| geo33-g091 | r √30, six α and six β → 5π | r √35, five each | 7π (2) |
| geo33-g092 | radii 2, 4, 6 → 3π | radii 6, 14, 15 (20-21-29) | 9π (3) |
| geo33-g094 | r 4 → 16 − 4π | r 6 | 36 − 9π (2) |
| geo33-g095 | OE = EC = 12 → 72√3 − 24π | OE = EC = 4 | 8√3 − 8π/3 (3) |
| geo33-g096 | semicircle O, A, B, OAB 60° | K, M, N, KMN 60°; new order | (π+2)/3 (3) |
| geo33-g097 | squares ABCD / EFGH | KLMN / PQRS; new order | 1/2 (2) |
| geo33-g098 | r 9, 26°, 49°, GOE 90° → 3π | r 8, 28°, 57°, GOE 80° | 4π (3) |
| geo33-g099 | r 4 → 24π + 16 | r 6 | 54π + 36 (3) |
| geo33-g100 | r 3 → BC 3π/2 | r 4 | 2π (2) |
| geo33-g101 | CB 6, ring 21π → r 2 | CB 10, ring 65π | 4 (2) |
| geo33-g102 | A = 2α → πr(1 − α/90) | A = 4θ, 0 < θ < 45 | πr(1 − θ/45) (4) |
| f-p01 | wire 10 cm → 5/π | string 18 cm | 9/π (3) |
| f-p10 | AB, OB, small C 6π → 12π | CD, OD, small C 10π | 20π (1) |
| f-p12 | A, B, areas 50π → 10 | P, Q, areas 72π | 12 (3) |
| f-p02 | small diameter = big radius = 6 → 27π | = 10 | 75π (1) |
| wp26-p10 | machine 600 m²/h, halved, floor r 15 → 3π/4 h | robot 480 m²/h, halved on carpet, r 12 | 3π/5 h (3) |
| f-p06 | COB 5α → β 150° | COB 4α | 144° (4) |
| f-p14 | α central, β inscribed, 3β − α → β | φ, θ, 5θ − 2φ | θ (1) |
| f-p07 | BAC 36° → major arc 4/5 | 40° | 7/9 (3) |
| wp27-p10 | runners, 5 × as fast → 60° | cyclist and walker, 8 × | 40° (3) |
| f-p19 | r 8, 135° + 90° → arc 6π | r 6, 150° + 90° | 4π (2) |
| f-p20 | area 25π, AOC 36° → 10π | area 36π, AOC 60° (review fix) | 12π (3) |
| f-p18 | square perimeter 28 → 14π | 36 | 18π (1) |
| f-p17 | r 5, area 35 → AB 14 | r 6, area 54 | 18 (3) |
| f-p05 | area 16π, AC 8 → 90° | area 49π, AC 14 | 90° (2) |
| f-p04 | AB diameter, BAC = CAD → BC = CD | KL, LKM = MKN; new order | LM = MN (3) |
| f-p03 | COD 140° → BAD 20° | 128° | 26° (2) |
| f-p08 | BAD 2α, COD 3β → 4α − 3β | 3α, 2β | 6α − 2β (2) |
| f-p09 | AMB 72° → AKB 108° | 64° | 116° (1) |
| f-p11 | BOC 144° → ABC 72° | 136° | 68° (3) |
| f-p13 | BCA 56° → DOE 112° | 64° | 128° (3) |
| f-p16 | deltoid 90°/72°, trapezoid 104°, 3 × 40, 11-gon | 90°/84°, 112°, 5 × 36, 13-gon | deltoid (3) |
| f-p15 | area 25π → AC 10 | 64π | 16 (3) |
| adv-p01 | four arcs = 2/5 → 36° | four arcs = 4/9 | 40° (3) |
| adv-p07 | four semicircles, average m → 4πm | five, average k | 5πk (3) |
| adv-p09 | sector 150°, area = 3 × arc → r 6 | 108°, 5 × | 10 (3) |
| adv-p08 | garden r 600 m, path 100 m → 0.13π km² | lake r 400 m, walkway 100 m | 0.09π km² (2) |
| adv-p02 | five equal arcs, E mid-arc → 9° | three equal arcs | 15° (3) |
| adv-p12 | BAC 45° → r√2 | triangle KLM, LKM 45°, new order (review fix) | r√2 (3) |
| adv-p13 | r 5, arcs 2 : 1 → 5√3 | r 8 | 8√3 (2) |
| adv-p03 | r 6, square OACD → 6 − 3√2 | r 8 | 8 − 4√2 (3) |
| adv-p10 | square 6 − semicircle → 21–22 | square 8 | 38–39 (3) |
| adv-p14 | sides > 6, sectors r 3 → 9π/2 | sides > 8, r 4 | 8π (2) |
| adv-p16 | three circles r 6 → 6π | r 9 | 9π (3) |
| adv-p04 | radii a, 2b, 3c | x, 3y, 4z | π(16z² − 9y² + x²) (1) |
| adv-p05 | CAD 44°, CDB 24° → 56° | 46°, 20° | 57° (2) |
| adv-p06 | ACE 2p, EOD 3q → 2p + 3q/2 | 3m, 2n | 3m + n (3) |
| adv-p11 | ECA 3t → 6t | 2k | 4k (2) |
| adv-p17 | circumference 12π → 36 | 20π | 100 (3) |
| adv-p18 | r 4, 45° → 2π − 4 | r 10 (review fix) | 25π/2 − 25 (2) |
| adv-p19 | r 6, ADC 60° → 6π | r 8, ADC 45° | 8π (2) |
| adv-p15 | AB 6, BC 10, CD 14 → 10 | 7, 11, 15 | 11 (1) |
| adv-p20 | radii 9, 4 → perimeter 38 | 16, 9 | 74 (2) |

## 2026-10-06 review
Independent review of the renumber pass (built with and without `renumber_pass`, compared every question, explanation,
video line, board item and figure; answers recomputed; Hebrew subtitles checked; duplicate scan over topics 1–33).
All 22 guided questions and videos, 42 practice questions, 4 lesson videos and the card are correct: keys, one correct
choice each, traps still present, choice numbers in the videos follow the new order (g094/g096/g100/g101 cross-outs
re-ordered correctly), no leftover old numbers, no spoken "Question N". Figures: all 42 changed figures rendered; the
relabelled-only ones (g076, g078, g082, g086, f-p03, f-p07, f-p09, adv-p05) stay acute/obtuse as labelled and are not
misleading; the redrawn ones match. Fixed:
- **f-p20** landed back on the Hebrew lesson example (circle 16π, 135° = 3/8 → 6π, the Hebrew sectors example).
  Now area 36π, AOC 60° → COB 120° = 1/3 → 12π (traps: 6π = sector AOC, 18π = semicircle, 24π). Figure redrawn (60°).
- **adv-p12** had changed type: 45° (right isosceles BOC, BC = r√2) became 30° (equilateral, BC = r). The 45° is what
  makes the question, so it is now letters-only: triangle KLM, angle LKM 45°, LM = r√2, new choice order; figure relabelled.
- **adv-p18** (r 6, 45° sector 9π/2) used the lesson example of Sectors and Arcs ("r = 6 … an eighth: 9π/2").
  Now r = 10: 25π/2 − 25 (same trap pattern).
Judgment calls left: g094 (r 6, quarter 9π) shares the quarter-circle step with the same lesson slide, but the
question and answer (36 − 9π) differ; adv-p02 went from five equal arcs to three (same steps: divide, halve, halve).

## 2026-10-07 methods spread
- spread_methods() runs last. Q19 (geo33-g096): Method 2 · Power count line (it replaces the sentence "A ratio of two perimeters cannot contain r."), and one spoken line on video slide 4 names it as the power count. Shortcut · Pick values that fit lines in geo33-advanced-p07 (with the power-count tie-break), q-r26-t33-10, geo33-advanced-p15 and geo33-foundation-p04. No new slides. Nothing recorded.


## 2026-10-07 study-plan order
Function `plan_order_fix` (runs LAST). Students follow the study plan (`src/lib/planData.ts` ORDER), not topic numbers; named methods were checked against the plan rank of their teaching topic.
- geo33-g096: "Method 2 · Power count" → self-contained "Shortcut · Power count" (count the lengths; a ratio of perimeters cannot depend on r). geo33-advanced-p07: "(power count)" tie-break rewritten as counting lengths.
- Video solve-geo33-g096 (not recorded) slide 4: "That's the power count from algebra…" → "Count the lengths: a perimeter is one length, so perimeter over perimeter is one length over one length — they cancel. No r can stay." Rendered, checked.
`python3 math_check.py 5 7 10 21 22 25 26 28 30 31 33 37 32` → PROBLEMS 0, WARNINGS 0, LAYOUT 0.


## 2026-10-07 no decimal estimates
Function `no_decimal_estimates` (runs last). Teacher: a student cannot estimate roots or π to one decimal place; estimates use whole-number benchmarks only (perfect squares, squaring, a factor into the root, 3 < π < 3.5). Videos with a recording are skipped by a build-time guard.
- solve-geo33-g094 "Estimate the size": 18π ≈ 56.5, 72 − 9π ≈ 43.7, 36 − 9π ≈ 7.7 -> 9π > 27 (choice 1 negative), 18π > 54 so 18π − 18 > 36, 9π < 36 so 72 − 9π > 36, 36 − 9π between 0 and 9. Same pen marks next to each choice, same count of lines.
- solve-geo33-g096 Method 3: board (π+2)/3 ≈ 5.14/3 ≈ 1.7 -> π > 3 → (π+2)/3 > 5/3 (the spoken lines already said "5-plus over 3").
- solve-geo33-g100 Method 2: "2π is about 6.3" -> "6-plus — under 8". Written geo33-g100 size check: 3π, 4π, 8π are more than 9; 2π < 7.
- solve-q-r26-t33-04 "The traps" + written: 3π ≈ 9.4 < 9√3 ≈ 15.6 -> 3π < 12 < √243 = 9√3.
- r26-t33-summary-2 "Numbers and estimates": board π ≈ 3.14 -> 3 < π < 3.5.
- geo-079 "π is a number": "All we need to know: a bit more than 3" -> "more than 3 and less than three and a half".
- LEFT, teacher to decide: geo33-g089 (16π between 50 and 51, trap 48–49) and geo33-advanced-p10 (64 − 8π between 38 and 39) — the question itself needs π ≈ 3.14 (π between 3 and 3.5 cannot decide). Also geo-079 still says "even 3.1 is enough for the exam", which is not enough for g089 (16 · 3.1 = 49.6).
Check: `python3 math_check.py 33 32` -> 0 / 0 / 0. Rendered and looked at.


## 2026-10-08 coverage fixes
Function `coverage_fixes` (runs LAST in apply(); helpers from `_hebrew_back.py`, own recording guard `CF_CUTOFF` = 2026-10-08T08-47-24 UTC). Source: the Hebrew-vs-English coverage check of this topic (WEAK / MISSING points) + the teacher's decisions of 2026-10-08. No video of this topic is recorded (checked ~/Documents/Course.recordings), so everything went into the videos themselves; nothing added to `_rerecord.py`. Notes in added_notes.json. `python3 math_check.py 30 31 32 33 34 35 36 37 38` → PROBLEMS 0, WARNINGS 0, LAYOUT 0.
- **solve-geo33-g102** "Method 2 · Plugging in numbers" (+≈9 s): "Even if one fits early — don't mark it yet. A special case can fit more than one answer, so we check all four."
- Coverage-check "keep the English" notes: no change (teacher).
