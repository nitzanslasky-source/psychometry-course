# Topic 34 (Polygons): the teacher's Hebrew videos vs the English course

Read-only review, 2026-10-22. Nothing in the course was changed.

- Hebrew source: `~/Downloads/03-Geometry-Original-Subtitles.txt`, lines 5098-5993 (all of it read). Theory 5098-5371
  ("מצולעים תאוריה": the rules lesson, then the area lesson with three examples), advanced 5372-5992 ("מצולעים לימוד
  מתקדם": a short intro and eight questions), then "תרגול עצמי" (5993).
- English: the current reading scripts `studio-build/ai_scripts/<id>.json` (spec `math_patches/_ai_vis_t34.py`), the base
  translation `studio-build/base-v18.html`, and the practice list `scratchpad/ext/course/q34.txt`.
- Recording status comes from `python3 video_status.py --list record`. **Not recorded yet: every topic-34 video**
  (geo-104 and parts -2…-5, geo-105, geo-109, geo-112-after, r26-t34-meet, every solve-geo34-g1xx and solve-q-r26-t34-01/02/03).
  The summary video r26-t34-summary is replaced by the printable page `summary_pages/t34.json`.

**Match scale.** The English course gives every question new numbers on purpose (memory rule *questions-differ-from-hebrew*),
so new numbers on their own do not count as a change. SAME = same idea and every one of her methods. CHANGED = same idea,
but the method, the example or the order is different (the cell says what). PARTIAL = some of her content or one of her
methods is missing (the cell says exactly what). MISSING = no English equivalent.

**Her names.** משולש כסף / משולש זהב → "silver triangle" / "golden triangle"; חלוקת אוזן המן → "the star partition … a
hamantasch, or Haman's ear" (geo-112-after); עוגן → "starting from an angle sum we know"; פתרון פסיכומטרי / הבנה
גאומטרית → "by understanding" or "with an estimate"; הצבת מספרים → "plugging in numbers"; נקודת האיזון → "the balance point".

**Video numbering (no gaps).** Her segments run 104 = rules lesson, 105 = area lesson intro, 106/107/108 = the area
lesson's three examples (pentagon, hexagon, octagon), which English turns into three try-first question videos,
109 = the advanced intro, 110-117 = her eight advanced questions. Segment 112 (the hexagon ACE question) also held her
partition talk and the dark-area example; English splits these off as **geo-112-after** (lesson) and
**solve-geo34-g112-area** (question). Nothing was merged away or dropped.

---

## 1. Hebrew → English (her videos, in her order)

| # | Her video (Hebrew title · English gloss) | Lines | What she teaches / how she solves it (every method) | English equivalent | Match |
|---|---|---|---|---|---|
| 1a | מהו מצולע · What a polygon is | 5099-5104 | Closed shape with 3+ sides; triangle, quadrilateral; pentagon, hexagon, heptagon, octagon | geo-104 slide 1 | SAME (English adds that non-regular shapes keep the name) |
| 1b | סכום זוויות · Angle sum | 5105-5120 | 180(n−2); check on the quadrilateral (360); or split into triangles from one corner if you forget the formula (the quadrilateral's diagonal, 180+180) | geo-104 slides 2-5 | SAME (English adds pentagon/hexagon/heptagon sums and *why* n−2) |
| 1c | הוספת צלע = +180 · Each extra side adds 180 | 5121-5130 | Erase one side, draw two: one more triangle, +180 | geo-104 slides 6-7 | SAME (English adds the 12-vs-9 sides example and sum→sides, both of which she does later in Q7/Q8) |
| 1d | מצולע משוכלל · Regular polygon | 5131-5142 | All sides AND all angles equal; the folded hexagon (equal sides, not regular); regular looks symmetric from every side | geo-104-2 slide 1 | SAME (English adds the rectangle counter-example and square / equilateral as the regular 4- and 3-gons) |
| 1e | חסימה במעגל · Inscribed in a circle | 5143-5155 | Every regular polygon fits in a circle (also has an inscribed circle, same center); the converse is false; **"the folded hexagon does not fit in a circle, so it is certainly not regular"** | geo-104-2 slide 2 | PARTIAL: everything is there except her last step, the contrapositive on the folded hexagon ("not inscribable → surely not regular") |
| 1f | גודל זווית במשוכלל · One angle of a regular polygon | 5156-5177 | Sum ÷ n; open brackets and split the fraction to 180 − 360/n, the formula-sheet form; "most students remember sum ÷ n, it's more intuitive" | geo-104-2 slide 3 + geo-104-3 slide 1 | SAME (English: "Use the form you remember better"; adds halving 1080 three times) |
| 1g | טבלת המחומש/משושה/מתומן · The table + central angle tip | 5178-5199 | Table 540/720/1080, 108/120/135, central angles 72/60/45; central angle = 360/n (link to the sector lesson: 1/5, 1/6, 1/8 of a circle); tip: if you forget the angle, find the central angle and complete to 180 | geo-104-3 slides 2-3 | SAME (her link back to the arc/sector lesson is not said; English adds exterior angles and why the tip works) |
| 1h | אלכסונים חוצים לזוויות שוות · Diagonals split the angle equally | 5200-5212 | From one pentagon corner only 2 diagonals; 3 equal angles; proof: inscribed angles on equal arcs | geo-104-4 slide 1 | SAME (English adds the hexagon, and slides 2-3 + geo-104-5 slide 1: the 180/n per side rule, a 10-gon and two crossing diagonals) |
| 1i | n משולשים שווי שוקיים; המשושה · Radii make n isosceles triangles; the hexagon | 5213-5225 | Radii from the center → n congruent isosceles triangles; hexagon: apex 60 → 6 equilateral triangles; "very important for areas and angles later" | geo-104-5 slides 2-3 | SAME (English adds the 54/54 split of the pentagon corner, which she gives in Q2) |
| 1j | חזרה · Recap | 5226-5236 | Angle sum (formula or triangles), diagonals, isosceles/equilateral triangles | geo-104-5 slide 4 | SAME |
| 2a | שטח מצולעים – פתיח · Areas: no formula, split it | 5237-5247 | No formula except the triangle; not even for a general quadrilateral; split into shapes you know | geo-105 slides 0-2 | SAME (English adds a second way, "complete to a big shape and subtract", with an easy house pentagon and an L-shaped hexagon) |
| 2b | מחומש לא משוכלל · Irregular pentagon area (Hebrew item 106) | 5249-5270 | Cut off a right triangle; the trapezoid lacks a base; 3-4-5 triple; drop a second height → a square; another 3-4-5 → 6 + 6 + 16 = 28 | solve-geo34-g106 | SAME (8-15-17 instead of 3-4-5, same steps; English adds the trap "285 = only the trapezoid") |
| 2c | משושה משוכלל צלע 6 · Regular hexagon area (item 107) | 5272-5286 | 6 equilateral triangles, a²√3/4 = 9√3; "don't stop at one triangle", ×6 = 54√3 | geo-105 slide 3 (side 4) + solve-geo34-g107 (side 12) | SAME (English adds the trap "forgot to divide by 4") |
| 2d | מתומן משוכלל צלע 6 · Regular octagon area (item 108) | 5288-5355 | The standard cut (square, 4 rectangles, 4 silver triangles); the 4 triangles make one square; leg = hyp/√2; total 72 + 72√2; **pattern 2a² + 2a²√2** (side 4 → 32 + 32√2, side 1 → 2 + 2√2); the cut works for parts too: the cross = total − 36 | geo-105 slide 4 (side 2) + solve-geo34-g108 (side 10, pattern with sides 3 and 7, the cross) | SAME (English adds *why* the corner triangle is 45-45-90 and the trap "only two rectangles") |
| 2e | סיכום שטחים · Areas wrap-up | 5356-5369 | Hexagon → equilateral triangles, octagon → that cut, irregular → split by what the question gives | geo-105 slides 2, 4 (closing lines) | SAME |
| 3 | לימוד מתקדם – פתיח · Advanced intro (item 109) | 5373-5377 | We learned the rules; now harder questions and nuances that recur | geo-109 slide 0 | SAME (the rest of geo-109 is new English teaching, see section 2) |
| 4 | מחומש – זווית אלפא · Pentagon angle α, 3 ways (Q, easy+, item 110) | 5379-5448 | (1) Isosceles triangle DCB: 108 (memorise), base angles 36, α = 108 − 36 = 72. (2) "Every pentagon diagonal makes an isosceles trapezoid + triangle": co-interior angles 108 + 72 → α = 72. (3) Diagonals split the angle into 3 equal inscribed angles: 108/3 by 90 + 18 = 36, α = 2·36 = 72 | solve-geo34-g110 (x = the middle angle, 36) | CHANGED: all three ways, with the same 90 + 18 split, but English asks for the **middle** angle (one third), not her α (two thirds). So in way 2 English needs an extra step (72 + 72 − 108 = 36) instead of reading α off the trapezoid directly; English calls it a trapezoid (via "a diagonal is parallel to the opposite side"), not an isosceles trapezoid |
| 5 | מחומש חסום במעגל – אינה נכונה · Pentagon in a circle, "not true" (Q, medium, item 111) | 5451-5561 | Eliminate surely-true claims. (1) Central angles equal (360/5 = 72). (2) Arc > chord → circle > perimeter (true for every regular polygon). (3) Congruent triangles OBC, OCD (or 54/54); **symmetry principle: a radius to a corner bisects it**. (4) Mark 4 on the exam without checking; in class: bigger angle ↔ longer side, side (72) > radius (54) → 5 sides > 5r. Then the principle: hexagon = balance point (side = radius); 7-gon: circle = 2πr ≈ 6.28r < 7r; 8-gon; below 6 it flips ("also in the quadrilateral"); "pause and think" | solve-geo34-g111 (9-gon, perimeter = 9r is the false one) | SAME (all four checks and the balance-point lesson; the 6.28r step is now "π is less than 3.5, so the circle is less than 7r" (whole-number rule); her "also true in the quadrilateral" and "pause the video" are not said) |
| 6 | משושה – היקף ACE = 18 · Hexagon, perimeter of ACE (Q, medium+, item 112) | 5564-5657 | (1) Math: prove ACE equilateral (120 − 30 − 30 = 60; or by symmetry, congruent corner triangles); side 6; golden triangle 3 → √3 → 2√3; 6·2√3 = 12√3. (2) Estimate: triangle inequality → hexagon > 18; **√3 ≈ 1.7, √2 ≈ 1.4; "12 × 1.7 is hard, use ×1.5 = 18"**; cross out 3. (3) Guessing tip: √3 choices go with hexagons/equilateral, √2 with squares/silver | solve-geo34-g112 (ACE = 42, answer 28√3) | CHANGED: the math way, the triangle inequality and the guessing tip are all there. The estimate now compares squares with whole numbers (4√3 = √48 < √49 = 7) instead of her decimals and the ×1.5 benchmark, which follows the teacher's own rule *no-decimal-estimates* (the base translation still had 1.7 / 1.4 / ×1.5). Her short "symmetry" proof of the equilateral triangle is not given |
| 6b | חלוקת אוזן המן · The two hexagon partitions | 5658-5687 | 6 equilateral triangles vs 3 rhombi vs the star (Haman's ear); every star triangle is 1/6 of the hexagon (each is half a rhombus, like an equilateral one); so use a²√3/4 for it | geo-112-after | SAME (English adds a numeric check, side 4, and "ACE is the other half") |
| 6c | השטח הכהה · Dark area, side 2 (worked example) | 5689-5699 | Long way (height, 30-60-90, base × height / 2, ×3) vs understanding: 3 × (2²√3/4) = 3√3 | solve-geo34-g112-area (side 10, 75√3) | SAME (English carries out the long way in full and adds the traps "one triangle" and "the whole hexagon") |
| 7 | משושה + ריבועים – ראם וכרמל · Hexagon with 3 squares, Ram and Carmel (Q, medium+, item 113) | 5702-5779 | (1) Plug in side 2: 24 vs 12 → Ram right; cross out 2 choices "to double your chances"; areas 12 vs 6√3, √3 ≈ 1.7 → Carmel right. (2) Understanding: count sides 12 vs 6; split the hexagon into 3 rhombi; **square vs rhombus: squeeze the angle and the area goes to 0, straighten it to 90 and it grows; the square uses its sides best** | solve-geo34-g113 (5 squares, Ella wrong, Adam right) | CHANGED: both ways are kept (plug in 1, count sides, the 3 rhombi, "if we run out of time we have two choices left"). Two differences: (a) the rhombus-vs-square reason is now "base × height, the leaning side's height is shorter", not her squeeze-the-angle picture (the base translation still had hers); (b) with five squares the area claim is already true on 3 squares, so the comparison is less tight than hers (3 squares vs 3 rhombi exactly). √3 < 2 replaces √3 ≈ 1.7 (whole-number rule) |
| 8 | מתומן – הלל ונעמי · Octagon, Hillel and Naomi (Q, hard, item 114) | 5782-5858 | The standard cut first. (1) Plug in numbers, **choose the leg AE = 1, not the side, to multiply by √2 instead of dividing**; Hillel 2 vs 1 + √2 → wrong; Naomi 2 + √2 = 2 + √2 → right. (2) Understanding: cancel equal pieces; **"never rely on the drawing — but in regular-polygon questions the drawing is accurate, it can't be drawn any other way; measure with your fingers"**; Naomi by cancelling pieces | solve-geo34-g114 (Sara LT > 2KT true, Ben true → both) | PARTIAL: the cut, the "pick the leg = 1" reason, both claims by numbers and by cancelling pieces are all there. **Her exception "in a regular polygon the drawing is accurate, you may rely on it / measure with your fingers" is missing**: the current script proves it instead (the square's side is a hypotenuse, so longer than the leg). The base translation had both the tip and the proof |
| 9 | מתומן – השטח הלבן · Octagon, white area = 2 + 2√2 (Q, hard, item 115) | 5861-5889 | "Solving it algebraically is a mistake here" (she sketches the long algebra); cut the octagon; 2 grey rectangles = 2 white ones, 4 triangles = the white square → grey = white, no calculation | solve-geo34-g115 (12 + 12√2) | SAME |
| 10 | 1,260 מעלות · Angle sum 1,260, how many sides (Q, medium, item 116) | 5892-5948 | Most questions are pentagon/hexagon/octagon, but general ones exist. (1) Formula; divide before opening: ÷10, ÷2, ÷9 → n − 2 = 7 → 9. (2) Anchor: know 540/720/1080; > 1080 → not 8, not 7; steps of +180; 1080 + 200 − 20 = 1260 | solve-geo34-g116 (1,440 → 10 sides) | SAME (same divisions and the +200 − 20 trick; English adds the trap "8 = n − 2". Her remark that most questions use the three famous polygons is in geo-109 slide 0) |
| 11 | 10 מול 13 צלעות · 10 vs 13 sides, B − A (Q, hard, item 117) | 5951-5987 | (1) 180·11 − 180·8, common factor → 3·180 = 540 = pentagon. (2) 3 more sides → 3·180 | solve-geo34-g117 (14 vs 20 → 1,080, octagon) | SAME (English adds the trap "hexagon = the 6 extra sides") |
| 12 | סיכום · Summary | 5988-5991 | Three lines ("we practised regular pentagons, hexagons, octagons and general polygons; let's sum up") | summary_pages/t34.json (r26-t34-summary) | SAME (English is a full summary) |
| 13 | תרגול עצמי · Self-practice (no video) | 5993 | — | geo34-core-p01 … p20 (+ p26, p27) in the practice section | SAME (no Hebrew text to compare question by question) |

**Count by row (28 rows):** SAME 23 · CHANGED 3 (4, 6, 7) · PARTIAL 2 (1e, 8) · MISSING 0.

### Count by video (her 15 units)

| Unit | Match |
|---|---|
| Rules lesson 104 (1a-1j) | PARTIAL (only the small "not inscribable → not regular" step is missing) |
| Area lesson 105 (2a, 2e) | SAME |
| Pentagon area 106 (2b) | SAME |
| Hexagon area 107 (2c) | SAME |
| Octagon area 108 (2d) | SAME |
| Advanced intro 109 (3) | SAME |
| Q pentagon α 110 | CHANGED (asks for the middle angle; the trapezoid way needs an extra step) |
| Q pentagon in a circle 111 | SAME |
| Q hexagon ACE 112 (6) | CHANGED (whole-number estimate instead of 1.7 / 1.4 / ×1.5, by the teacher's rule) |
| Hexagon partitions (6b) + dark area (6c), part of 112 | SAME |
| Q hexagon + squares 113 | CHANGED (rhombus-vs-square reason; five squares instead of three) |
| Q octagon Hillel/Naomi 114 | PARTIAL (the "regular-polygon drawings are accurate" tip is missing) |
| Q octagon white area 115 | SAME |
| Q 1,260 116 | SAME |
| Q 10 vs 13 sides 117 | SAME |
| Summary + practice | SAME |

**By video: SAME 11 · CHANGED 3 · PARTIAL 2 · MISSING 0** (16 units including summary + practice).

---

## 2. English with no Hebrew equivalent (added)

- **geo-104-3 slide 3**: exterior angles and their sum of 360 (the walk-around proof); explains why "central + angle = 180".
- **geo-104-4 slides 2-3, geo-104-5 slide 1**: the "180/n per side between the arms" rule for any corner angle, a 10-gon
  example, and the angle where two diagonals cross (= the interior angle).
- **geo-105 slides 1-2**: an easy house-pentagon and an L-hexagon, plus the second way "complete to a big shape and subtract".
- **geo-109 slides 1-4**: the "corner triangle" (isosceles, base angles 45 / 36 / 30) and the hexagon's diagonals (long = 2a,
  short = a√3), taught before the questions that use them (she derives them inside items 110 and 112).
- **solve-q-r26-t34-01**: one angle 160 → n = 18 (formula-sheet form and exterior angle).
- **solve-q-r26-t34-02**: counting diagonals, n − 3 from one corner, n(n − 3)/2 in all.
- **r26-t34-meet** + **solve-q-r26-t34-03**: polygons meeting at a point (360 around the point, then the isosceles gap
  triangle; tilings).
- **Printable summary** `summary_pages/t34.json` (she has only a one-line "let's sum up").

---

## 3. Recommendations

Every target video below is **not recorded yet**, so any change is cheap.

| What is missing / changed | Where it would go | Length | Verdict |
|---|---|---|---|
| Her exception "never rely on the drawing — except in regular-polygon questions: the drawing is accurate, it can't be drawn any other way; measure with your fingers" (5834-5845) | solve-geo34-g114 slide 2, right after "So L T is more than two times K T": a short "you could also see it in the figure" line, keeping the proof | 2-3 sentences | **RESTORE**: it is a named exam habit of hers that saves time on every regular-polygon comparison, and the base translation had it. Keep the proof so it isn't a guess |
| The folded hexagon "doesn't fit in a circle, so it is surely not regular" (5153-5155) | geo-104-2 slide 2, after "So it's not regular." | 1-2 sentences | OPTIONAL: a nice use of the contrapositive; the warning itself (inscribable ≠ regular) is already there |
| Q 110 asks for the middle angle instead of her α | solve-geo34-g110 | — | NOT NEEDED: all three of her ways are there and still work; only way 2 gets one extra subtraction |
| Square vs rhombus: her "squeeze the angle and the area shrinks to zero; the square uses its sides best" picture (5762-5776) | solve-geo34-g113 slide 2, after the base × height reason | 1-2 sentences | OPTIONAL: English's base × height reason is correct and shorter; her picture is more vivid. Also note that with five squares the claim is true already on three, so the question is easier than hers; three or four squares would keep her tight comparison |
| The decimal estimate √3 ≈ 1.7, √2 ≈ 1.4 and the ×1.5 benchmark (5626-5649) | solve-geo34-g112 | — | NOT NEEDED: replaced on purpose by whole-number squaring (her own rule *no-decimal-estimates*); the method still works with the English numbers |
| "Also true in the quadrilateral" / "pause the video and think" (item 111); the link back to the sector lesson (1g); the symmetry proof of ACE (item 112) | — | — | NOT NEEDED: minor asides |

**Nothing in the English is wrong compared with her.** Every method she uses still works with the English numbers.
