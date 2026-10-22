# Topic 33 (Circles): the teacher's Hebrew videos vs the English course

Read-only review, 2026-10-22. Nothing in the course was changed.

- Hebrew source: `~/Downloads/03-Geometry-Original-Subtitles.txt`, lines 3446-5096 (all of it read): theory 3446-3884,
  basic lesson 3886-4259, advanced lesson 4260-5096.
- English: the current reading scripts `studio-build/ai_scripts/<id>.json` (spec `math_patches/_ai_vis_t33.py`), the base
  translation `studio-build/base-v18.html` (question stems only, for the number changes), and `math_patches/t33_CHANGES.md`.
- Recording status from `python3 video_status.py --list ...`. **Done (recorded):** geo-075, solve-q-r26-t33-01.
  **Re-read:** solve-geo33-g076. **Not recorded yet (record list):** everything else in the topic - geo-074 (-2, -3), geo-077,
  geo-079, geo-081, geo-084, geo-093, geo-097-after (-2), every solve-geo33-g078 … g102 except g076, r26-t33-more-tools (-2, -3),
  solve-q-r26-t33-02 … -05.

**Match scale.** As in the t23 report: new numbers alone are not a change (memory rule *questions-differ-from-hebrew*).
SAME = same idea and every one of her methods. CHANGED = same idea, but a method, the example type or the question asked is
different (the cell says what). PARTIAL = some of her content or one of her methods is missing. MISSING = no English equivalent.

**Her names.** זווית היקפית / מרכזית → "inscribed / central angle"; נשענת על הקשת → "intercepts the arc" (her "walls" image is
kept: geo-075 slide 1 "Stand at C … you see the same arc", g076 slide 2 "The chords B A and B C are your walls"); משולש כסף / זהב →
"silver / gold triangle"; בניית עזר → "helper line"; חישוב חלקי → "partial calculation"; הערכת סדר גודל → "estimation"; הצבת מספרים /
הצבת תשובות → "plugging in numbers / plugging in the answers"; חוסם חסום → "inscribed and circumscribed question"; פקמן → "three-quarter
circle". Her Pavlov line ("tangent → radius → 90°, automatically") is kept as "Make that a habit. Tangents, then radii, then
right angles" (g078) and "Automatically" (summary).

**Video ids.** They follow her segment numbers with no gaps: 74 terms, 75 angles, 76 its example, 77 tangents, 78 its example,
79 area/circumference, 80 its example, 81 sector/arc, 82-83 its two examples, 84 basic-lesson intro, 85-92 the eight basic
questions, 93 advanced intro, 94-102 the nine advanced questions. geo-074 is split into three parts (camera lesson); the "three
objects" part at the end of her segment 97 became its own video, geo-097-after (+ -2).

---

## 1. Hebrew → English (her videos, in her order)

| # | Her video (Hebrew title · English gloss) | Lines | What she teaches / how she solves it (every method) | English equivalent | Match |
|---|---|---|---|---|---|
| 1 | מונחים במעגל · Circle terms | 3447-3511 | מעגל vs עיגול (the line vs the disc, wooden board); radius, all radii equal (rotating radius), r; chord, many chords of different lengths; diameter = longest chord = 2r; inscribed angle (vertex on the circle, between 2 chords; not inside/outside); central angle; arc (short or long, chord makes 2 arcs, "people think an arc is short"); "an angle intercepts the arc" = the walls image | geo-074 slides 1-2, 5-7; geo-074-2 slides 1-5 | SAME (the circle/disc distinction is adapted for English: "circle can mean the line or the region; check if they ask area or length"). English adds: 2 radii + chord = isosceles, semicircle, minor/major arc, and geo-074-3 (tangent preview, sector, segment, naming quiz). The walls image moved to geo-075/g076 |
| 2 | זוויות במעגל · Angles in a circle | 3513-3567, 3604-3610 | Central = 2 × inscribed on the same arc (wherever the vertex is); inscribed on the same / equal arcs are equal; inscribed on a diameter = 90 (½ of 180) "very important"; inscribed quadrilateral (all 4 vertices on the circle), opposite angles = 180 (70 → 110), proof with 2α + 2β = 360; closing: one main rule, the others follow from it | geo-075 slides 0-1, 4-5, 7-9, 12 | SAME. English adds: the proof of the main rule (slide 3), the case with the center outside the angle (2), the vertex-on-the-arc warning (4), the backwards rule (right triangle → hypotenuse = diameter; rectangle's diagonals, slide 6), equal chords ↔ equal arcs, perpendicular from the center halves a chord (10-11) |
| 3 | דוגמה: aocb אינו מרובע חסום · Example: AOCB is not inscribed | 3570-3603 | Trap: O is not on the circle, so not 180 − 90 (and "you can see by eye it is much more than 90"); (1) draw an inscribed angle on the same arc (45) → new inscribed quadrilateral → 180 − 45 = 135; (2) the reflex central angle 270, ABC is its inscribed angle (walls) → 135 | solve-geo33-g076 (104° → 128°) | SAME (both methods, the walls image). English adds a 3rd route (radius OB, two isosceles triangles) and names the trap choice 76 = 180 − 104. Her "you can see it by eye" remark is not said |
| 4 | משיקים למעגל · Tangents | 3612-3632, 3649-3654 | Tangent touches at one point (inside → chord, outside → just a line); radius ⟂ tangent at the point of tangency, "every time: helper line, radius to the point of tangency"; two tangents from one point are equal and form a kite with the radii | geo-077 slides 1-2, 4-5 | SAME. English adds why the radius is perpendicular (shortest distance), a 5-12-13 numeric example (slide 3), and the kite's symmetry line OP halving the angle |
| 5 | דוגמה: שני משיקים, זווית 40 · Example: two tangents, angle 40 | 3635-3648 | Pavlov: radii → 90, 90; quadrilateral sum 360 → central 140; the asked angle is inscribed on it → 70 | solve-geo33-g078 (68 → 112 → 56) | SAME. English adds the symmetry route (kite axis halves 68 → 34 → 56), the general fact "angle at P + central angle = 180", and the traps 112 / 34 |
| 6 | שטח והיקף מעגל · Area and circumference | 3656-3713 | πr², 2πr; what π is (peel the circumference, it holds 3 diameters and a bit → π a bit more than 3), **π ≈ 3.14 (3.141592…), "even 3.1 is enough for the exam"**; π is a fixed number, not an unknown, written as a letter because it isn't round (3.14r², 6.28r); r = 5 → 25π, 10π; circumference 16π → r = 8; area 64π → r = 8, −8 is not relevant | geo-079 slides 1-2, 4-8 (r = 6, d = 14, 22π, 121π) | PARTIAL: everything is there **except the value π ≈ 3.14**. geo-079 only says "π is a bit more than three" and "keep the π" - the number 3.14 is never taught in the lesson, yet g089 later needs 3.14 < π < 3.15. English adds the area proof (pizza slices → rectangle, slide 3), the diameter trap (slide 6) and wheels (slide 9) |
| 7 | דוגמה: שטח = היקף · Example: area equals circumference | 3716-3736 | Ignore the units; πr² = 2πr → divide by π, by r → r = 2; check: 4π = 4π | solve-geo33-g080 (area = 4 × circumference → r = 8) | SAME (the story is tweaked from "equal" to "four times"; her check is kept; "ignore the units" becomes "compare the numerical values"). English adds the ratio route (area/circumference = r/2) and the traps 4 and 16 |
| 8 | גזרה וקשת במעגל · Sector and arc | 3738-3842 | Sector = slice of pizza; formula α/360 · πr², and **her strong advice: "don't use the formula, solve by understanding"**; quarter / eighth / fifth (25π → 5π); arc formula α/360 · 2πr, again "leave the formula"; sixth, third, two fifths = 144; angles to know: 90 ¼, 45 ⅛, 60 ⅙, 40 1/9, 36 1/10, 72 1/5, and extensions 270, 144, 120; **"on the exam these are the angles; they don't test if we are pocket calculators, no 23.5° angles"** | geo-081 slides 1-8 | CHANGED: all the content and the full angle list are there, but her advice is softened to "the formula and the share are the same idea … often it's quicker to see which part it is", and her claim that the exam uses only these friendly angles is replaced by "if a question gives a different angle, use α/360". English adds the sector perimeter (arc + 2 radii, slide 9) |
| 9 | דוגמה: קשת 2π, r = 3 · Example: arc 2π, radius 3 | 3845-3860 | "You could use the formula - no need": circumference 6π, 2π of 6π = ⅓ → α = 120 | solve-geo33-g082 (r 10, arc 4π → ⅕ → 72) | SAME |
| 10 | דוגמה: שטח גזרות 45° + 90° · Example: two sectors | 3863-3884 | 90 = ¼, 45 = ⅛ → ⅜ of 16π = 6π; closing "no formulas in arc and sector, just see the part" | solve-geo33-g083 (40° + 120° = 4/9 of 9π = 4π) | SAME (English adds the circumference trap and the sector-by-sector check) |
| 11 | מעגלים יסודות לימוד – פתיח · Basic lesson intro | 3887-3890 | "We'll practise basic and more advanced questions using only these rules" | geo-084 | SAME (English adds a recap of the three key rules and the term "helper line") |
| 12 | 120°, קוטר 8, משולש כהה · AOC = 120, diameter 8, shaded triangle (easy) | 3892-3919 | 180 − 120 = 60; "isosceles triangles hide inside circles because the radii are equal"; isosceles + 60 = equilateral; radius 4; a²√3/4 ("2 3 4 a") → 4√3 | solve-geo33-g085 (diameter 20 → 25√3) | SAME (the "a-two-three-four" count is kept). English adds the height route |
| 13 | משולש שווה שוקיים חסום, 30° · Inscribed isosceles, top angle 30 (easy) | 3922-3961 | (1) Mathematical: central = 60 → equilateral BOC; base angles 75 → 75 − 60 = 15. (2) Psychometric: radius OA bisects the top angle by symmetry, **"no need to prove it, this is not the bagrut, it is an easy question at the start of the section"** → isosceles AOB → 15. "Shorter, I prefer it" | solve-geo33-g086 (56° → 28) | CHANGED: both methods are there, but in method 2 English proves the symmetry with a folding argument (slide 2) instead of her "no need to prove it on the psychometric". Her preference verdict is cut (R35). English adds the traps 34 and 62 |
| 14 | ארבעה מיתרים שווים – איזו טענה אינה נכונה · Four equal chords, which statement is not true (easy+) | 3964-4029 | Go statement by statement, cross out what is true; (1) inscribed angles on equal chords are equal; (2) equal central angles, 4x = 180, "halve twice" → 45; (3) inscribed on a diameter = 90; "on the exam you're done, mark 4, no time to check"; in the lesson: AOC is a silver triangle → √2, not √3 (gold) | solve-geo33-g087 (AO = 5 → 5√2 vs 5√3) | SAME (every step, including "halve twice" and "no need to check the last choice") |
| 15 | שני מעגלים חופפים משיקים · Two congruent touching circles, find α (medium) | 4031-4087 | No number given - start from the givens; two tangents from M are equal → kite needs helper lines; radius to the tangent point (common) → 90, 90, still stuck; second, less common helper line: join the centers → OM = 2r; right triangle with hypotenuse = 2 × leg → gold → 30 at M, twice → **α = 60 (the angle at M)**; "this time backwards, from the sides to the angle" | solve-geo33-g088 (r = 7; asks angle AOB → 120) | CHANGED: every step is there, but English asks for the angle at the center O (120 = 60 + 60, or via the kite) instead of her angle at M (30 + 30 = 60). English adds the comparison with circles touching from the inside (R − r) and the trap 60 |
| 16 | מעגל בתוך מעגל, היקף 6π, כהה 16π · Small circle 6π, ring 16π, big circumference (medium) | 4090-4128 | r = 3, area 9π; big = 9π + 16π = 25π → R = 5 → 10π; the choices are ranges: **π ≈ 3.14, "just move the decimal point": 10 × 3.14 = 31.4 → between 31 and 32** | solve-geo33-g089 (10π, ring 39π → R = 8 → 16π, between 50 and 51) | CHANGED: the whole chain is the same, but with 16π **her decimal-point shortcut no longer works**. English needs two bounds, 3.14 < π < 3.15, and the long products 16 × 0.14 and 16 × 0.15. Neither 3.14 nor 3.15 was taught in geo-079 (row 6). t33_CHANGES.md already lists this as "LEFT, teacher to decide" (the base translation had 8π / 65π → 18π, between 56 and 57) |
| 17 | 5-12-13 – היקף המעגל החוסם · Sides 5, 12, 13: circumference of the circumscribed circle (medium+) | 4131-4166 | Every triangle has exactly one circumscribed circle; **recognise the triple 5-12-13 ("חמסה, בת-מצווה, בר-מצווה")** → right triangle (new: from 3 sides to "it is right"); inscribed 90° → it lies on a diameter → BC = 13 is the diameter; circumference = diameter × π, "no need to halve and double" → 13π | solve-geo33-g090 (12-35-37 → 37π) | CHANGED: the two facts, the backwards rule and "π × diameter" are all there, but **her "recognise the triple" step is gone**: 12-35-37 is not a triple students know, so English checks Pythagoras by squaring 35 and 37 (and then adds a difference-of-squares shortcut). The numbers were changed on purpose to avoid 3-4-5 / 5-12-13 / 6-8-10 (t33_CHANGES.md); the base translation had 7-24-25 |
| 18 | רדיוס √12, 4α + 4β · Radius √12, four α and four β sectors (medium+) | 4169-4207 | Area 12π (the square cancels the root); 4α + 4β = 360, one equation two unknowns, only the sum: divide by 4 or take out the common factor → 90 = ¼ (30+60, 10+80, endless) → 3π | solve-geo33-g091 (√35, 5α + 5β → 72 = ⅕ → 7π) | SAME |
| 19 | שלושה מעגלים משיקים 1, 2, 3 · Three touching circles, radii 1, 2, 3, arc of A (medium+) | 4210-4255 | Circumference 2π; peek at the choices: 2π is the whole circle → out; π would need a 180° triangle angle → out; out of time → guess between two, 50% instead of 25%; sides 3, 4, 5, **"again a Pythagorean triple"** → 90 → the arc is ¾ → 1.5π | solve-geo33-g092 (radii 6, 14, 15 → 20-21-29 → 9π) | CHANGED: both eliminations and the 50% guess are kept, but **the triple-recognition step is gone**: 20-21-29 has to be squared out (English adds a difference-of-squares check at the end). The base translation had radii 2, 4, 6 → 6-8-10 |
| 20 | מעגלים לימוד מתקדם – פתיח · Advanced intro | 4261-4268 | You already have the tools for most circle questions; now edge questions, recurring principles, psychometric thinking that saves time or solves even when unsure | geo-093 | SAME (English also names the two recurring ideas, shaded areas and inscribed/circumscribed shapes, and the three quick ways) |
| 21 | משיק, oa = ob, r = 2 · Tangent, OA = OB, shaded area (medium+) | 4270-4401 | Shaded areas = subtract (a recurring edge principle); scheme triangle − sector; silver triangle, auto helper line radius to the tangent point, height = bisector = median → 2, 2; **"don't run to the legs, you already have base and height"** → 4; partial calculation: "4 minus something with π" → crosses out 3 choices; then the sector π (¼ of 4π); estimation: triangle 4, the shaded part is less than half → < 2; 2π − 2 too big, 2 − π negative ("they hide negatives behind letters"), 8 − π ≈ 5 too big; "estimation sometimes rules out only one or two, a card up the sleeve" | solve-geo33-g094 (r = 6 → 36 − 9π) | SAME (all three ways, "don't run to the legs", negative answers, "sometimes only one or two"). Her personal verdict (math + partial is safer) is cut (R35); her bound "less than half of the triangle" becomes the bound 0-36 |
| 22 | משולש ישר זווית משיק, r = 6 · Right triangle tangent at B and D, r = 6 (hard) | 4404-4471 | The scheme is not obvious, so place the givens and let it appear; at B the 90 is marked, at D BD is not a radius, so draw the radius OD; triangle ODC − sector; hypotenuse 12 = 2 × 6 → gold (not Pythagoras) → 6√3 → 18√3; **partial calculation: only choice 1 has 18√3 → mark it**; sector 6π (60 = ⅙); or start from the sector: "something − 6π" also leaves one choice | solve-geo33-g095 (OE = EC = 4 → 8√3 − 8π/3) | CHANGED: the same steps, but with the new choices **the partial calculation on the triangle leaves two choices**, so the sector has to be found (English says so: "this time the partial calculation doesn't finish the job"). Her sector-first remark is kept, changed to "you need both parts" |
| 23 | חצי מעגל ומשולש · Semicircle and triangle, ratio of perimeters (medium) | 4474-4577 | Inscribed/circumscribed questions: write everything with r; (1) math: equilateral → 3r; the semicircle's perimeter is not only half the circumference, add the diameter → 2r + πr; common factor, cancel r → 3/(2 + π). (2) **Plug in r = 1 - "the recommended way for almost everyone"**; r = 1 in the choices settles it. (3) Estimation: each arc > 1 (shortest path), so > 5 → about 3/5; choices with r change with the radius, but the ratio of perimeters can't → any choice with r is a distractor (except area ÷ perimeter) | solve-geo33-g096 (semicircle ÷ triangle = (π + 2)/3) | CHANGED: all three of her ways and her "r in a ratio must cancel" rule (with the area/perimeter exception) are there, but the ratio is turned upside down, and **r = 1 alone no longer settles it**: three choices survive, so English plugs in r = 2 as well. Her "recommended for almost everyone" verdict is cut. English's estimate draws two extra helper radii to show each arc > 1 |
| 24 | ריבוע, מעגל, ריבוע · Square-circle-square, ratio of areas (medium+) | 4579-4634 | Plug in r = 1: big square side = diameter = 2 → 4; small square: via silver triangles (√2), "a bit long", or diagonals × diagonals / 2 = 2 → ratio 2; shortcut by symmetry: 8 identical triangles vs 4 | solve-geo33-g097 (small ÷ big = ½) | SAME (both ways and the silver-triangle detour). English inverts the ratio, and adds rotating the inner square to the touching points |
| 25 | שלושה אובייקטים · Three nested objects to know by heart | 4635-4657 | Square-circle-square: area × 2, side × √2 ("has appeared several times; if you know it you mark 2 automatically"); circle-square-circle: area × 2, radius × √2; equilateral triangle-circle-triangle: area × 4, side × 2 ("we didn't prove it, you can") | geo-097-after slides 1-3 | SAME. English proves each one, and adds a 4th arrangement in geo-097-after-2 (circle-triangle-circle: R = 2r, the ring = 3 small circles, length factor vs area factor) |
| 26 | סכום קשתות AG + ED · Sum of two arcs (hard) | 4659-4737 | Helper radii for central angles; inscribed 20 → central 40 (another helper radius OF), 55 → 110; can't find each angle, only the sum: 150 − 90 = 60 (30+30, 20+40, "it doesn't matter" - shift the middle part); ⅙ of 12π = 2π | solve-geo33-g098 (28°, 57°, 80° → 90° → 4π) | SAME (including the sliding middle part) |
| 27 | שני מעגלים נחתכים, ¼ היקף · Two intersecting circles, the union (hard) | 4740-4840 | Shaded area with no subtraction; from the givens: ¼ of the circumference → 90 central angles → rhombus with a right angle = square; pacman + square + pacman = 3π + 4 + 3π = 6π + 4; estimation: > one circle + half a circle → rules out 2 choices, 50%; **if you must gamble: "by eye the grey middle looks big, so +4 rather than +2"** | solve-geo33-g099 (r = 6 → 54π + 36) | PARTIAL: her solution and her estimate (rule out two) are there, and English adds a second exact way (two circles − overlap) with a stricter proof of the bound. **Her eye-based tie-break between the last two is not given**; English just says "a reasonable guess between the two" |
| 28 | מלבן משיק, שטח מלבן = שטח מעגל · Rectangle tangent to the circle, BC (medium+) | 4843-4893 | (1) EF is a diameter = 2 = AB; 2·BC = π → π/2. (2) Estimation: BC < diameter 2; π, 2π, 2π/3 all > 2 → out; "no need to even calculate π/2 ≈ 1.5" | solve-geo33-g100 (r = 4 → 2π) | SAME (both ways). English justifies the bound with a helper square around the circle (area < 64 → BC < 8) |
| 29 | מעגל קטן בתוך גדול, 16π · Small circle inside, tangent at A, ring 16π (medium+) | 4896-4995 | (1) Big − small = 16π; express R by r (easier to add than subtract): R = r + 2; (a+b)², r² cancels → r = 3. (2) Plug in the answers **from the middle**: two tries are always enough (why); try 2 → 12π too small → 1 and 2 out; try 3 → 16π ✓ | solve-geo33-g101 (CB = 10, 65π → r = 4) | SAME (both ways and the "start in the middle, two tries" reasoning). Her small reason "easier to add than subtract" is not said |
| 30 | משולש שווה שוקיים וקשת · Isosceles triangle and an arc with α (hard) | 4998-5094 | (1) Math: base angles 90 − α/2; central 180 − α ("we halved and doubled - spot it early"); α/360 · 2πr → adapt to the choices (πr), split 180/180 − α/180 = 1 − α/180. (2) Plug in numbers: the easiest special case α = 60 (equilateral), r = 1 → 2π/3; test all choices ("can't mark yet, must cross out 3") | solve-geo33-g102 (top angle 4θ → πr(1 − θ/45)) | SAME (both ways, "halved and doubled", fitting the choices, splitting the fraction, θ = 15 chosen to make the equilateral case) |
| 31 | 20 שאלות תרגול עצמי (יסודות) · 20 self-practice questions, basics (no video) | 4259 | - | geo33-foundation-p01 … p21 | SAME (present, new numbers; not compared item by item) |
| 32 | 20 שאלות תרגול עצמי (מתקדם) · 20 self-practice questions, advanced (no video) | 5096 | - | geo33-advanced-p01 … p20 (+ p22, p27) | SAME (present, new numbers; not compared item by item) |

**Count by row (32 rows):** SAME 22 · CHANGED 8 (8, 13, 15, 16, 17, 19, 22, 23) · PARTIAL 2 (6, 27) · MISSING 0.

### Count by video (her 26 units)

| Unit | Match |
|---|---|
| Theory 1 מונחים (1) | SAME |
| Theory 2 זוויות במעגל + example (2-3) | SAME |
| Theory 3 משיקים + example (4-5) | SAME |
| Theory 4 שטח והיקף + example (6-7) | PARTIAL (π ≈ 3.14 not taught) |
| Theory 5 גזרה וקשת + 2 examples (8-10) | CHANGED (her "skip the formula" advice softened, "exam angles are friendly" claim dropped) |
| Basic intro (11) | SAME |
| Q 120° diameter (12) | SAME |
| Q inscribed isosceles (13) | CHANGED (symmetry proved instead of "no need to prove") |
| Q four equal chords (14) | SAME |
| Q two touching circles (15) | CHANGED (asks the angle at O, not at M) |
| Q ring 16π, estimate (16) | CHANGED (decimal-point shortcut lost; needs 3.14/3.15) |
| Q 5-12-13 circumscribed (17) | CHANGED (triple recognition lost) |
| Q 4α + 4β (18) | SAME |
| Q three touching circles (19) | CHANGED (triple recognition lost) |
| Advanced intro (20) | SAME |
| Q tangent, 4 − π (21) | SAME |
| Q right triangle, 18√3 − 6π (22) | CHANGED (partial calculation no longer finishes) |
| Q semicircle ratio (23) | CHANGED (r = 1 alone no longer decides; ratio inverted) |
| Q square-circle-square + three objects (24-25) | SAME |
| Q sum of arcs (26) | SAME |
| Q two intersecting circles (27) | PARTIAL (her gamble tie-break missing) |
| Q rectangle (28) | SAME |
| Q small circle inside, 16π (29) | SAME |
| Q isosceles arc (30) | SAME |
| 20 practice, basics (31) | SAME |
| 20 practice, advanced (32) | SAME |

**By video: SAME 15 · CHANGED 8 · PARTIAL 2 · MISSING 0** (26 units including the two practice sets; rows 24-25 are one
Hebrew video).

---

## 2. English with no Hebrew equivalent (added)

- **geo-074-3**: tangent preview, sector, **segment** (vs sector), naming quiz. geo-074 slide 4: two radii + chord = isosceles; slide 7 semicircle.
- **geo-075**: proof of the main rule (slide 3), center-outside case (2), vertex-on-the-arc warning (4), **backwards rule** and the
  rectangle's diagonals (6; she teaches the backwards rule only inside question 17), equal chords ↔ equal arcs (10),
  perpendicular from the center halves a chord (11).
- **geo-077**: why radius ⟂ tangent, a 5-12-13 tangent-length example, the kite's symmetry axis.
- **geo-079**: area proof by pizza slices (3), diameter-vs-radius trap (6), wheels and turns (9).
- **geo-081**: perimeter of a sector (9).
- **geo-097-after-2**: 4th nested arrangement (circle-triangle-circle, R = 2r, ring = 3 small circles), length factor vs area factor.
- **r26-t33-more-tools (-2, -3)**: two equal circles through each other's centers (the lens), the ring from a tangent chord
  (π·(chord/2)²), an inscribed trapezoid is isosceles.
- **solve-q-r26-t33-01 … -05**: chord + distance → radius, incircle of a right triangle (r = (a + b − c)/2), circumference +50% →
  area +125%, the segment (sector − triangle), common external tangent of two touching circles (2√(Rr)).
- **r26-t33-summary, -summary-2**: summaries.
- Extra methods inside her questions: g076 3rd route (radii), g078 symmetry, g080 ratio r/2, g085 height route, g090 / g092
  difference of squares, g096 second plug-in (r = 2), g099 circles − overlap.

---

## 3. Recommendations

| # | Missing / changed from her | Where it would go | Length | Target recorded? | Verdict |
|---|---|---|---|---|---|
| 1 | **π ≈ 3.14** (her "3.141592…, 3.14 is enough"). Without it, g089 suddenly uses 3.14 < π < 3.15 that was never taught | geo-079 slide 4, after "π is a bit more than three" | 1-2 sentences ("Its value is about 3.14. For most questions 'a bit more than three' is enough, but when the choices are close ranges, use 3.14.") | No (geo-079 is unrecorded) | **RESTORE** |
| 2 | Her **decimal-point estimate** (10 × 3.14 = 31.4) no longer works in g089 (16π needs 16 × 0.14 and a 3.15 upper bound) | solve-geo33-g089: change the numbers so the big circumference is 10π × k, e.g. small circumference 8π (r = 4), ring 84π → big area 100π, R = 10 → 20π ≈ 62.8, "between 62 and 63" (double 31.4; trap 60 with π = 3). Differs from her 6π / 16π / 10π | Rewrite of slide 1 (shorter than now) | No | **RESTORE** (already flagged "LEFT, teacher to decide" in t33_CHANGES.md) |
| 3 | Her **"recognise the Pythagorean triple"** step in g090 (12-35-37 has to be squared out) | solve-geo33-g090: use a triple students know that is not hers, e.g. 7-24-25 (the base translation's numbers) or 9-12-15 / 15-20-25; keep the difference-of-squares line as an optional check | Slide 1 gets shorter | No | **RESTORE** |
| 4 | The same triple-recognition step in g092 (radii 6, 14, 15 → 20-21-29) | solve-geo33-g092: radii giving a multiple of 3-4-5, e.g. 3, 6, 9 → 9-12-15 (or the base's 2, 4, 6 → 6-8-10) | Slide 1 gets shorter | No | **RESTORE** |
| 5 | "On the psychometric there is no need to prove the symmetry" (the point of her psychometric method in Q13) | solve-geo33-g086 slide 2, before or instead of the folding argument | 1 sentence | No | OPTIONAL (the fold is short and correct; her line explains why the method is fast) |
| 6 | "The exam uses these friendly angles; it doesn't test you as a pocket calculator" | geo-081 slide 8 | 1-2 sentences | No | OPTIONAL (motivates memorising the list; the current "use α/360 otherwise" is also true) |
| 7 | Her eye-based tie-break in Q27 ("looks big → +4") | solve-geo33-g099 slide 3 | 1 sentence | No | NOT NEEDED (she herself calls it a gamble) |
| 8 | Q15 asks the angle at O instead of her angle at M; Q22 partial calculation leaves two; Q23 needs a second plug-in | g088 / g095 / g096 | - | No | NOT NEEDED (every method of hers still appears and works) |

**Anything wrong in the English?** No mathematical errors found in the topic-33 scripts (the arithmetic in g089, g090,
g092, g099 and summary-2's 2√(18·2) = 12 was checked). The only real teaching gap is row 1: g089 relies on π ≈ 3.14 / 3.15, which
the lesson never gives.
