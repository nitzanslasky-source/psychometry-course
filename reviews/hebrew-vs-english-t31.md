# Topic 31 (Triangles): the teacher's Hebrew videos vs the English course

Read-only review, 2026-10-22. Nothing in the course was changed.

- Hebrew source: `~/Downloads/03-Geometry-Original-Subtitles.txt`, lines 404-1727 (basics 404-1196, advanced 1198-1727; all of it read).
- English: the current reading scripts `studio-build/ai_scripts/<id>.json` (spec `math_patches/_ai_vis_t31.py`), the base
  translation `studio-build/base-v18.html`, the question data in `math_patches/t31.py`, and the change log `math_patches/t31_CHANGES.md`.
- Recording status from `python3 video_status.py --list record / send / reread / done`.
  **Not recorded:** only `geo-023` (the optional Pythagoras proof).
  **Recorded, waiting for a re-read:** geo-013, geo-024, geo-026, solve-geo31-g034, solve-geo31-g038, **solve-geo31-g040**.
  **Recorded, sent to Codex:** geo-009, geo-009-2, geo-009-3. **Done:** every other topic-31 video.

**Match scale** (same as the t23 report). English questions use new numbers on purpose, so new numbers alone are not a change.
SAME = same idea and every one of her methods. CHANGED = same idea, but the method, the example type or the order is different.
PARTIAL = one of her methods/tips is missing. MISSING = no English equivalent.

**Her names.** משולש זהב → "the gold (golden) triangle"; משולש כסף → "the silver triangle" (her joke that it's "our own name, so
the gold one won't feel lonely" is kept); משולש בורקס → the "square sandwich" picture (teacher-approved 2026-10-11; English still
mentions the borekas once); חמסה בת מצווה בר מצווה → "high five, a dozen, and one more" (teacher-approved); "a-2-3-4"
(ריקודי עם) → "a folk dance teacher counting a-two-three-four" (kept); חלוקה בשורש ("ignore the root, divide, attach it back")
→ "divide nine by three, then times root three" (the same trick; the summary uses her exact wording); הברקה / חשיבה
פסיכומטרית → "an insight"; קיזוז צלעות → "cancelling sides"; מינימום מקסימום → "a minimum and maximum question".

**The numbering gaps.** Her subtitle segments are 9-28 (basics) and 31-40 (advanced). There is no g029 or g030. **29 = the basics
block "20 שאלות תרגול עצמי" (line 1196)**, a practice set with no video, like topic 30's practice blocks (segments 3 and 8).
**30 has nothing in the subtitles.** Between 1196 and 1200 there is only the heading "משולשים לימוד מתקדם" and then straight
into her first advanced question. It is probably the advanced-section header or a short intro that wasn't transcribed. Going by
the subtitles, nothing was lost. (In topic 30 the advanced section has no number of its own, so this is an inference.) 41 = the
advanced practice block (line 1727); topic 32 starts at geo-042.

**Order.** English mostly keeps her order, with one deliberate move (t31_CHANGES.md "Order fix"). Her "שטח משולש שווה צלעות"
(segment 17b) and its question (18) came right after the area lesson. There she derived the height with Pythagoras, before the
Pythagoras lesson. In English they come **after the gold-triangle lesson and its question** (geo-026 → g027 → geo-017-after →
g018 → geo-027-after → g028).

---

## 1. Hebrew → English (her videos, in her order)

| # | Her video (Hebrew title · English gloss) | Lines | What she teaches / how she solves it (every method) | English equivalent | Match |
|---|---|---|---|---|---|
| 1a | משולשים – תיכון וגובה · Median and altitude | 405-430 | Median = vertex to midpoint; 3 medians meet at a point; the 2:1 rule "not relevant, forget it"; altitude = 90° to the side or its extension; 3 altitudes meet; obtuse triangle: the altitude is outside ("imagine this is the floor") | geo-009 slides 0-3 | SAME (English adds what a median/altitude does *not* promise, and a whole slide on the **angle bisector**, slide 4, which she doesn't teach here) |
| 1b | סכום זוויות 180 + הוכחה · Angle sum and proof | 431-439 | Parallel line through the vertex, two Z's, three angles on a straight line | geo-009-2 slides 1-2 | SAME (English adds two examples and "at most one obtuse or right angle") |
| 1c | זווית חיצונית · Exterior angle | 440-456 | Definition; proof (180 − γ + α + β = 180); "not used much on the exam, you can find the adjacent angle instead, but it saves time" | geo-009-2 slides 3-4 | SAME (English shows both ways side by side; the "saves time when it fits" tone follows teacher decision 3 of 2026-10-08) |
| 1d | צלע גדולה מול זווית גדולה · Big side opposite big angle | 457-468 | α<β<γ → a<b<c; works both ways; the angle opening wider makes the opposite side longer | geo-009-3 slide 1 | SAME (English adds: in a right triangle the hypotenuse is the longest) |
| 1e | אי-שוויון המשולש · Two sides > the third | 469-489 | Side 7 with sticks 4 + 3 that can't close; home → country club, a straight line is shortest | geo-009-3 slides 2-3 (9 = 4 + 5; home → sports club) | SAME (English adds the examples 5,6,9 yes and 2,3,8 no) |
| 1f | הרחבה: הפרש < צלע < סכום · Difference < side < sum | 490-502 | Moves b across: c > a − b; so a side is between the difference and the sum | geo-009-3 slide 4 | SAME. English adds the whole-number count trick "twice the shorter side minus one" |
| 2 | ש: זווית אלפא (קודקודיות) · Q: α with a vertical angle | 504-510 | Vertical angle = α; α + 3α + 2α = 180 → α = 30 | solve-geo31-g010 (3x, 4x, 5x → 15) | SAME (English adds a check and the trap 45 = 3x) |
| 3 | ש: 2α+γ · Q: 2α + γ (exterior angle) | 512-531 | One unknown is needed; α = 180 − β (adjacent), γ = 2β (exterior); 2(180 − β) + 2β = 360 | solve-geo31-g011 (m + n/2 = 180) | SAME (English adds a 2nd method, plugging in k = 60) |
| 4 | ש: ערכו של x (5, 9) · Q: third side | 533-549 | 9 − 5 < x < 9 + 5; 4 itself not allowed → 9 | solve-geo31-g012 (6, 13 → 11) | SAME (English adds a number line) |
| 4w | סיכום שיעור · Lesson wrap | 550-556 | The angle sum matters most; also remember the exterior angle, it saves seconds | end of g012 + geo-009-3 slide 5 | SAME |
| 5a | משולש שווה שוקיים · Isosceles | 563-585 | Legs, base, base angles, vertex angle; the median to the base is also the altitude and the bisector; **"just remember it's symmetric: fold the paper"**, no proofs needed | geo-013 slides 1-3 | SAME (English adds number examples and the converse) |
| 5b | משולש שווה צלעות · Equilateral | 586-599 | All 60 (180 ÷ 3); "isosceles from every direction", turn it | geo-013 slide 4 | SAME |
| 5c | משולש ישר זווית · Right triangle, median to the hypotenuse | 600-615 | Legs/hypotenuse, the hypotenuse is the longest; the median to the hypotenuse = half of it, two isosceles triangles; "very rare on the exam" | geo-013 slides 5-6 | SAME (English adds the "look across from the square mark" trick) |
| 6 | ש: שווה צלעות, dac = 30 · Q: equilateral, bisector | 617-631 | 60 − 30 = 30, so a bisector → also a median → 5 + 5 = 10 | solve-geo31-g014 (7 → 14) | SAME (English adds the trap 7 = half the side) |
| 7 | ש: שני משולשים שווי שוקיים · Q: two isosceles triangles | 633-656 | 150/2 = 75; **rule out choice 3 because only part of the angle can't be all of 75**; base angle 75 again → 30 → 75 − 30 = 45 | solve-geo31-g015 (28° → 76 → 28 → 48) | SAME (the early elimination is kept, as choice 4) |
| 7w | סיכום משולשים מיוחדים · Wrap: triangles are inside every shape | 657-663 | Short recap + "we'll meet them all through quadrilaterals and circles; triangles always hide inside other shapes" | none (geo-013 ends "Now let's see some sample questions") | MISSING (trivial, one motivating sentence) |
| 8 | שטח משולשים · Area of triangles | 665-726 | cm² from a 1×1 square; rectangle 4×3 = 12 by counting; right triangle = half a rectangle → legs ÷ 2; any triangle: altitude → two half-rectangles → side × its altitude ÷ 2; "a triangle has no real base"; obtuse: altitude outside, **use only the side, not the extended length** | geo-016 slides 1-7 | SAME (English adds the worked check that two sides with their own altitudes give the same area, and the trap number 10 → 20) |
| 9 | ש: ישרים מקבילים, de = 3cd · Q: parallel lines, area ratio | 727-759 | (1) x, 3x, the same h → divide fractions → 3. (2) No calculation: cut 3x into x, x, x → four equal triangles | solve-geo31-g017 (5x → 5) | SAME (both methods; English adds the trap 25) |
| 10 | שטח משולש שווה צלעות · Area of an equilateral triangle | 760-793 | Altitude = median → Pythagoras a² − (a/2)² → h = a√3/2 → a²√3/4; why memorise it; the "a-2-3-4" folk-dance mnemonic | geo-017-after slides 1-4 | CHANGED: **the height comes from the gold triangle** ((a/2)·√3), and her Pythagoras derivation is kept as a check (slide 2). **The video was moved** after the gold-triangle lesson. The mnemonic is kept; English adds the examples 8 → 16√3 and 6 → 9√3 and a link to the 30-30-120 triangle |
| 11 | ש: שווה צלעות, אמצעי צלעות · Q: midpoints in an equilateral triangle | 794-827 | Perimeter 6 → sides 2, halves 1; the small triangle is equilateral (two 1's + 60°); big − small; **keep the /4, don't simplify, so the subtraction is easy** → 3√3/4 | solve-geo31-g018 (perimeter 30 → 75√3/4) | SAME (every step incl. "keep the four"; English adds the ¼-area ratio and "side × k → area × k²") |
| 12 | טיפ: תיכון חוצה שטח · Tip: a median halves the area | 828-850 | Any triangle; the same base (median) + the same altitude (outside for the obtuse half) → equal areas; "see a median, you know it automatically" | geo-018-after slide 1 | SAME (English adds "same area ≠ same shape" and slide 2, the vertex moving along a parallel line) |
| 13 | מבוא לפיתגורס · Pythagoras intro | 852-870 | The anecdote (a cult of maths; he drowned a student over √2); a² + b² = c²; only in a right triangle | geo-019 slides 0-4 | SAME (the anecdote is shortened, the drowning is left out; English adds the examples 6-8-10 and 13-5-12, what a square root is, and a non-example 4-5-6) |
| 14 | ש: 3, 4 → ac · Q: hypotenuse | 871-888 | **First rule out 3 and 4: the hypotenuse is longest** ("4.01 could be, 4 can't"); then 9 + 16 = 25 → 5 | solve-geo31-g020 (20, 21 → 29) | SAME (English also rules out 41 = 20 + 21 with the triangle rule) |
| 15 | ש: 2, 3 → √13 · Q: an irrational hypotenuse | 890-900 | 4 + 9 = 13; not round → leave √13 | solve-geo31-g021 (5, 7 → √74) | SAME (English adds "between 8 and 9" and the traps 12, 74, √24) |
| 16 | ש: יתר וניצב · Q: a missing leg | 902-922 | Leg² = hypotenuse² − leg² → √11; "a very important technique"; teaser for the next lessons, the proof lesson "not a must but warmly recommended" | solve-geo31-g022 (10, 7 → √51) + slide 1 | SAME (the wrap and the teaser are kept word for word; English adds the traps 3 and √149) |
| 17 | הוכחת פיתגורס · Proof of Pythagoras (optional) | 924-968 | Squares on the sides (area meaning); cut-and-move visual; the 4-triangles-in-a-big-square algebra: (a+b)² = c² + 2ab | geo-023 (**not recorded**) | SAME (English adds why the middle shape is a square and a rearrangement picture) |
| 18 | שלשות פיתגוריות · Pythagorean triples | 970-1018 | 3-4-5, 5-12-13; most pairs give a root (1, 2 → √5); NITE loves triples; 8-15-17 "very rare, no need" + a trick for it (8×2 = 16 ∓ 1); a triple is a ratio → ×2, ×3…; the hypotenuse is always the longest; mnemonic חמסה/בת מצווה/בר מצווה | geo-024 slides 0-4 | CHANGED (teacher-approved): the mnemonic became "high five, a dozen, one more"; 8-15-17 is reduced to one line and the 16 ∓ 1 trick is gone (teacher decision 1, 2026-10-08). English adds the k² proof, ½-multiples and the trap "36 as the hypotenuse" |
| 19 | ש: שלושה משולשים · Q: three right triangles | 1019-1051 | 5-12-13 → 12; 9, 12 = 3-4-5 × 3 → 15; 15, 15: Pythagoras, **write 2 × 225 instead of 450** → 15√2; teaser: the silver triangle would do it instantly | solve-geo31-g025 (15, 39 → 36; 36, 48 → 60; 60, 60 → 60√2) | SAME (every step incl. "write 2 × 60²" and the teaser; English adds the √(k²·n) rule and a "how do triples jump out" slide) |
| 20 | משולש זהב · The gold triangle | 1053-1126 | From an equilateral 2a: altitude → 30-60-90; Pythagoras → a√3; ratio a : a√3 : 2a; the short leg = half the hypotenuse; one side is enough (vs two for Pythagoras); examples 5, hypotenuse 8, **1 opposite the 60** (1/√3, 2/√3), 6 opposite the 60; **division by a root: "ignore the root, 6 ÷ 3 = 2, attach √3"** | geo-026 slides 0-7 | SAME (all of it, incl. "a long leg is not the short leg" and the division trick with its reason; English adds 12√3 ÷ √3 and slides 8-9, **the 30-30-120 triangle**, not in her lesson) |
| 21 | ש: משולש זהב, היקף · Q: gold triangle perimeter | 1127-1140 | Short leg 4 → 8, 4√3; "after practice write it straight on the triangle; if it's hard, use the a-ratios" → 12 + 4√3 | solve-geo31-g027 (5 → 15 + 5√3) | SAME (both ways of writing it; English adds a Pythagoras check) |
| 22 | משולש כסף (בורקס) · The silver triangle | 1141-1167 | "Our own invention"; right + isosceles, 45°; a, a, a√2 via Pythagoras; leg → ×√2, hypotenuse → ÷√2 with the root trick (10/√2 = 5√2) | geo-027-after slides 0-3 (7 → 7√2; 16 → 8√2; 6√2 → 6) | SAME (the borekas picture became a square sandwich, teacher-approved, borekas still named; English adds the square's diagonal) |
| 23 | ש: משולש כסף, היקף · Q: silver triangle perimeter | 1168-1194 | Hypotenuse 10: (1) ÷√2 by the trick → 5√2; (2) as an equation a√2 = 10; perimeter 10 + 10√2; "practise until it's automatic" | solve-geo31-g028 (18 → 18 + 18√2) | SAME (both of her ways; English adds a 3rd, Pythagoras, the trap "half of 18", and "30° → gold, 45° → silver") |
| 24 | 20 שאלות תרגול עצמי (יסודות) · 20 basic self-practice (segment 29) | 1196 | — | geo31-foundation-p01 … p20 (+ p22) | SAME |
| 25 | (segment 30) | — | No subtitle content, only the heading "משולשים לימוד מתקדם" | none | — (see "numbering gaps"; not counted) |
| 26 | ש: β באמצעות α · Q: β in terms of α (medium+) | 1200-1266 | (1) Angle sum in ABE: 60 + β + (180 − α) = 180; (2) exterior angle α = β + 60, "shortens the end"; (3) plug in: the letter that's in the answers, α obtuse → 100 → β = 40 (several routes), rule out the rest | solve-geo31-g031 (x → y = x − 60; x = 110) | SAME (all three methods. English says "the figure isn't drawn to scale, just pick an easy value" where she picked an obtuse value because α looks obtuse) |
| 27 | ש: α > β, B = 60 · Q: which side is longest (medium) | 1268-1296 | α + β = 120; α > 60 > β; the side opposite the biggest angle; mark it, "no need to check the last choice" | solve-geo31-g032 (B = 50, 65) | SAME |
| 28 | ש: קהה זווית, היקף · Q: obtuse triangle, perimeter (fairly hard) | 1298-1361 | Min/max: perimeter > 4 (triangle rule); **insight: only the smallest choice above the minimum can be right** (else 3 right answers), shown on a number line; full max: AB is the longest (opposite the obtuse angle) → < 6 | solve-geo31-g033 (AB = 10: > 20, < 30 → 24) | SAME (all three steps) |
| 29 | ש: לא בהכרח שווה שוקיים · Q: not necessarily isosceles (easy+) | 1363-1396 | Isosceles properties; 70/55/55 → yes; altitude = bisector → symmetric; **skip the unclear choice and hope to rule out the next**; median with α + α = 180 → altitude too → yes; mark the unclear one | solve-geo31-g034 (64/58) | SAME (the "skip the unclear choice" strategy is kept; English adds a counterexample sketch for the answer) |
| 30 | ש: שטח מרובע ABCD · Q: area of ABCD (fairly easy) | 1398-1431 | Triples instead of full Pythagoras: 3-4-5, 5-12-13 (bat/bar mitzvah); area = two right triangles; cancel before multiplying (12/2 × 5) → 36 | solve-geo31-g035 (12, 16 → 20; 20, 52 → 48; 576) | SAME (scaled ×4 triples; cancel-first kept; English adds the trap 616) |
| 31 | ש: זהב → כסף, היקף · Q: gold → silver perimeter (easy+) | 1433-1461 | 30-60-90: hypotenuse 8 → 4, 4√3; 45-45-90: 4/√2 by the root trick → 2√2; add up | solve-geo31-g036 (20 → 10, 10√3 → 5√2) | SAME (English adds "BD is a leg in one triangle and the hypotenuse in the other" and "only the outside sides") |
| 32 | ש: שטח כהה · Q: shaded area (hard) | 1463-1533 | "Shaded = subtraction"; complete the data (altitude = median → EC = 2); gold → DE = 2√3; big − small (also by the a²√3/4 formula); **insight: shaded = two triangles with base AD and an outside altitude BE**, mirror images | solve-geo31-g037 (BE = 4, AD = 3√3 → 12√3) | SAME (both methods and the formula check; English adds the trap 6√3) |
| 33 | ש: הפרש שטחים, DC = 2BD · Q: area difference (medium+) | 1535-1593 | (1) Letters x, 2x, h: xh = 12 → 12 − 6; (2) area ratio = base ratio; (3) cut into three equal triangles, 6 each | solve-geo31-g038 (DC = 3BD, 56 → 28) | SAME (all three views) |
| 34 | ש: ארבעה ריבועים, הפרש היקפים · Q: four squares, perimeter difference (medium) | 1595-1663 | (1) Full: AE = 2√2 (silver diagonals), AF = √5 (Pythagoras), subtract; (2) insight: cancel the shared and equal sides → AE − AG; (3) **at the end of the exam: estimate √3 ≈ 1.7, √2 ≈ 1.4** → two negative choices out ("this shows up on the exam") | solve-geo31-g039 (side 5 → 10√2 − 10) | CHANGED: (1) and (2) are the same. In (3) English **rules out by sign without decimals** ("√2 and √3 are bigger than 1") and first proves the answer must be positive. It's the same two choices out, and the "with seconds left" framing is kept. This follows the no-decimal-estimates rule. (The summary r26-t31-summary-2 slide 7 still says "about 1.4 / 1.7".) |
| 35 | ש: שני משולשים שווי צלעות, a:b · Q: ratio a : b (medium) | 1665-1725 | Bold = b + b + (b − a) = 3a → 3b = 4a and **STOP: "the ratio is 3:4 or 4:3, and the psychometric exam has no order distractor", so rule out every other choice**; dividing by 4b is "unnecessary in the exam"; (2) plug in the answers: 1 (a = b impossible), 3 (a > b impossible), 3/4 checks | solve-geo31-g040 (three times the perimeter → 3b = 10a → 3/10) | PARTIAL: the algebra, the "many students get stuck here" point, and plugging in (1 out, 3/10 checks) are kept. **Her "no order distractor" shortcut is missing.** English gets out of the stuck point with "a < b so a/b < 1, try b = 10" plus the full ÷10b step. The shortcut still works with the English choices (1/3, 1, 3/10, 3/8: 10/3 was removed on purpose, t31.py line 3433, "the real exams never offer a ratio AND its reverse (checked: 0)"). Teacher decision 2 (2026-10-08) put this line into the video; the 10-14 reading script lost it |
| 36 | 20 שאלות תרגול עצמי (מתקדם) · 20 advanced self-practice (segment 41) | 1727 | — | geo31-advanced-p01 … p20 (+ p23, p27) | SAME |

**Count by row (43 counted rows; row 25 not counted):** SAME 38 · CHANGED 3 (10, 18, 34) · PARTIAL 1 (35) · MISSING 1 (7w).

### Count by video (her 35 units)

| Unit | Match |
|---|---|
| Lesson 1 משולשים (1a-1f + wrap) | SAME |
| Q α (10), Q 2α+γ (11), Q third side (12) | SAME ×3 |
| Lesson 2 משולשים מיוחדים (5a-5c) | SAME |
| Q equilateral bisector (14) | SAME |
| Q two isosceles (15) + wrap | SAME (her one-sentence closing "triangles hide in every shape" was dropped, trivial) |
| Lesson 3 שטח משולשים (16) | SAME |
| Q parallel lines (17) | SAME |
| Equilateral area (17b) | CHANGED (derived from the gold triangle, moved after it; her Pythagoras route is a check) |
| Q midpoints (18) | SAME |
| Median tip (18b) | SAME |
| Pythagoras intro (19) | SAME |
| Q 20, Q 21, Q 22 | SAME ×3 |
| Proof (23) | SAME |
| Triples (24) | CHANGED (teacher-approved mnemonic swap; 8-15-17 cut by teacher decision) |
| Q three triangles (25) | SAME |
| Gold triangle (26) | SAME |
| Q 27 | SAME |
| Silver triangle (27b) | SAME |
| Q 28 | SAME |
| Basic practice (29) | SAME |
| Q 31-38 (eight advanced questions) | SAME ×8 |
| Q 39 four squares | CHANGED (sign instead of decimal estimate) |
| Q 40 a : b | PARTIAL ("no order distractor" shortcut missing) |
| Advanced practice (41) | SAME |

**By video: SAME 31 · CHANGED 3 · PARTIAL 1 · MISSING 0** (35 units including the two practice sets).

---

## 2. English → Hebrew: English material with no Hebrew equivalent

- geo-009 slide 4: the **angle bisector** as a third special line (she has only the median and the altitude in this lesson). geo-009-2: "at most one obtuse angle". geo-009-3: the whole-number count "twice the shorter side minus one".
- geo-013 slide 5: the "look across from the square mark" hypotenuse trick.
- geo-018-after slide 2: the vertex moving along a line parallel to the base keeps the area.
- solve-geo31-g011 slide 1: plugging in k = 60. solve-geo31-g020: ruling out 41 with the triangle rule.
- solve-geo31-g018 slides 2-3: the ¼-area ratio, and "every length × k → area × k²".
- geo-024: the k² proof, ½-multiples, and the trap of a triple in the wrong positions.
- solve-geo31-g025 slides 2-3: the √(k²·n) = k√n rule (needed for 60√2) and "how triples jump out".
- geo-026 slides 7-9: 12√3 ÷ √3, and **the 30-30-120 triangle** (sides a, a, a√3, area a²√3/4); linked again in geo-017-after.
- geo-027-after: the square's diagonal = side·√2. solve-geo31-g028: a Pythagoras method and "30° → gold, 45° → silver".
- solve-geo31-g034 slide 2: a sketch of why the median-of-7 triangle need not be isosceles.
- Three new question videos: solve-q-r26-t31-01 (the altitude to the hypotenuse by counting the area twice: leg × leg = hypotenuse × altitude),
  -02 (the biggest area from two sides, ≤ ab/2), -03 (acute/right/obtuse from the three sides, comparing c² with a² + b²).
- Two summary videos: r26-t31-summary, r26-t31-summary-2.
- Traps named in nearly every question video (her videos rarely name traps).

---

## 3. Recommendations

| What is missing / different | Where it would go | Length | Target video status | Recommendation |
|---|---|---|---|---|
| Her **"no order distractor"** shortcut in Q 40: once 3b = 10a, the ratio is 3 to 10 or 10 to 3, and the exam never offers both orders, so only 3/10 can be right. No need to divide by 10b | solve-geo31-g040 slide 0, right after "Many students get stuck here: how do I get to a over b?" (it can replace or come before the "a is the smaller side… if b is ten" check) | 2 sentences | **recorded, on the re-read list**, so it costs almost nothing now | **RESTORE.** It is her named exam shortcut. It works with the English choices (they were changed precisely so that it does), and the teacher already approved it on 2026-10-08. The reading script dropped it by accident |
| Q 39 estimate: √2 ≈ 1.4, √3 ≈ 1.7 | solve-geo31-g039 slide 3 | — | done | NOT NEEDED. Ruling out by sign gives the same two eliminations with no decimals (memory rule *no-decimal-estimates*). **But** r26-t31-summary-2 slide 7 still teaches "root two about one point four, root three about one point seven". Make the summary match the video (or the other way round) |
| Closing of lesson 2: "you'll meet these triangles everywhere; triangles hide inside quadrilaterals, circles…" | end of geo-013 (last line) | 1 sentence | recorded, on the re-read list | OPTIONAL (a motivating line; no teaching content) |
| 8-15-17 trick (8 × 2 = 16, ∓ 1) | geo-024 | — | re-read | NOT NEEDED (she herself said "don't bother"; teacher decision 1 removed it) |
| Pythagoras anecdote (the drowned student) | geo-019 | — | done | NOT NEEDED (flavour only) |
| Equilateral area via Pythagoras first | geo-017-after | — | done | NOT NEEDED. The English order (after the gold triangle) fixes a real problem: in her order this lesson used Pythagoras before it was taught. Her Pythagoras route is kept as the check slide |

**Nothing in the English is wrong compared with her.** Every method and named trick of hers is there, except the Q 40 shortcut
above. The g039 sign argument and the moved equilateral-area lesson are deliberate and sound. One inconsistency inside the English:
summary-2's decimal root estimates don't match the g039 video.

**RESTORE list:** 1 item, solve-geo31-g040, the "no order distractor" line (2 sentences, video on the re-read list).
