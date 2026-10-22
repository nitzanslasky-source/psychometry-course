# Topic 32 (Quadrilaterals): the teacher's Hebrew videos vs the English course

Read-only review, 2026-10-22. Nothing in the course was changed.

- Hebrew source: `~/Downloads/03-Geometry-Original-Subtitles.txt`, lines 1729-3443 (all of it read): basics 1729-2792,
  advanced 2794-3443.
- English: the current reading scripts `studio-build/ai_scripts/<id>.json` (spec `math_patches/_ai_vis_t32.py`), the base
  translation `studio-build/base-v18.html` (video titles, flow, source segments), the practice questions in the text dump
  `scratchpad/ext/course/q32.txt`, and the printable summary page `studio-build/summary_pages/t32.json` (it replaces
  r26-t32-summary and r26-t32-summary-2).
- Recording status from `python3 video_status.py --list <status>`. **No topic-32 video is in "record" (unrecorded).**
  **Recorded and done:** every other topic-32 video. **Recorded, marked "reread":** geo-047, geo-052, solve-geo32-g068,
  r26-t32-perimeter. So any line added to a video means re-recording it. The summary page is printed, not recorded, so it can
  take a line without any recording.

**Match scale** (as in the topic-23 report). The English course gives every question new numbers on purpose, so new numbers on
their own are not a change. SAME = same idea and every one of her methods. CHANGED = same idea, but the method, the example
type or what is asked is different (the cell says what). PARTIAL = one of her methods, tips or warnings is missing (the cell says
exactly what). MISSING = no English equivalent.

**Her method names in English.** משולש כסף / משולש זהב → "silver triangle" / "gold triangle"; שלשה פיתגורית → "Pythagorean
triple"; ה-Z המוכר → "our familiar Z"; פתרון מתמטי / פתרון פסיכומטרי → "the math way" / "by understanding" (English never says
"psychometric solution"); עקרון הסימטריה → "the symmetry principle"; עקרון יחסים (same height) → "equal heights: the area ratio
is the base ratio"; חיסור שטחים / השלמות → "subtract the white parts" / "completions, pair the pieces that make a whole"; הצבת
מספרים → "plug in numbers"; שרטוט מוקצן → "draw an exaggerated rectangle / parallelogram"; דלתון → "kite, also called a deltoid".

**The numbering (geo-042 to g072).** Her segments run 42-72 with one gap, **64**: that is her basics summary video ("בואו נמשיך
לסיכום", line 2790). It has no subtitles, so it can't be compared. English made it r26-t32-summary, and also added
r26-t32-summary-2 for her second summary (line 3441, also without subtitles). Both summaries are now replaced by the printed
page `summary_pages/t32.json`. Two of her videos became two English videos each. **42** is split into the camera parts geo-042
and geo-042-2 (CAMERA_SPLIT: the family of quadrilaterals starts part 2). **67** is split into the question g067 and the lesson
geo-067-after (her symmetry-principle extension, lines 2955-3003, which she gave inside the same video).

---

## 1. Hebrew → English (her videos, in her order)

| # | Her video (Hebrew title · English gloss) | Lines | What she teaches / how she solves it (every method) | English equivalent | Match |
|---|---|---|---|---|---|
| 42a | מרובע · The quadrilateral | 1730-1754 | Closed shape, 4 sides; one angle can be bigger than 180; angle sum 360 proved by a diagonal (two triangles, the blue and green angles); "almost the only rule for a general quadrilateral" | geo-042 slides 0-4 | SAME (English adds non-examples and three angle-sum examples, slides 5-7) |
| 42b | סוגי המרובעים · The family and how one turns into another | 1755-1793 | Square, rectangle, parallelogram, rhombus, kite, trapezoid; stretch a square → rectangle; step on it → parallelogram; shorten → rhombus (turn it, "like on playing cards"); squash a square → rhombus; squash a rhombus → kite; move the sides of a rectangle → trapezoid; next we start with the square | geo-042-2 slides 1-3, 5 | SAME (English adds the family tree, "a special kind of", and "underline the shape's name") |
| 43 | ריבוע · The square | 1795-1865 (theory to 1846) | Equal sides, 90° angles; diagonals equal, bisect each other, perpendicular, bisect the angles (45s); 4 silver triangles, also 2, also infinitely many; area a² ("that's why we call it squared"), 5×5 grid = 25; diagonal formula b²/2, why: half-diagonal triangle ×4; the square is "yes" to every property | geo-043 slides 1-5, 7 | SAME (grid 6×6, derivation with diagonal 12; English adds the diagonal = side·√2 and slide 6, "every length ×k → area ×k²") |
| 44 | שאלה: ריבוע שאלכסונו 10 · Square with diagonal 10, find the area | 1848-1865 | Formula: 10·10/2 = 50. "I could find the side with Pythagoras, but there's no reason" | solve-geo32-g044 (diagonal 14 → 98) | SAME (English adds the Pythagoras route she mentioned and skipped, the "stop at s², the area" tip, and the traps 196 and 49) |
| 45 | מלבן · The rectangle | 1867-1901 | A stretched square; opposite sides equal, 90° angles, parallel sides; diagonals equal (it's symmetric) and bisect each other; NOT perpendicular, NOT angle bisectors (unlike the square); area length×width, 10×5 grid = 50 | geo-045 slides 1-3 | SAME (8×3 grid; the "why equal" is a fold) |
| 46 | שאלה: מלבן עם זווית 120 · Rectangle, CD = 2, angle E = 120° | 1903-1940 | Halves of the diagonals equal → isosceles → 30 and 30; triangle DBC 30-60-90 → gold triangle → BC = 2√3 → area 4√3. Closing tips: not sure of a rule? draw an exaggerated (very low, very wide) rectangle and look; triangles hide inside quadrilaterals | solve-geo32-g046 (CD = 5 → 25√3) | SAME (both closing tips kept, slide 2) |
| 47 | מקבילית · The parallelogram | 1942-2016 | Squashed rectangle; opposite sides equal and parallel; opposite angles equal, neighbours sum to 180, proof by extending the sides into parallel lines (all large angles β, all small α); diagonals not equal, bisect each other, not angle bisectors, not perpendicular, exaggerated drawing; area a·h, why: cut the triangle off the rectangle and move it | geo-047 slides 1-4, 6-7 | SAME (English adds slide 5, the rectangle and rhombus tests, and slides 8-9, the height with 30/45/60/150° angles) |
| 48 | שאלה: זוויות במקבילית · Angles only, find the "?" | 2018-2042 | Neighbours: 3α + 3β = 180 → α + β = 60; triangle ABE: 180 − 2(α + β) = 60; "we never find α or β, only their sum" | solve-geo32-g048 (5α, 5β → x = 72) | SAME (English adds a second method: plug in a rectangle, α = β = 18) |
| 49 | שאלה: שטח מקבילית עם אנך · Parallelogram 4, 7, 5, find the area | 2044-2072 | Pythagoras comes back a lot; redraw the givens; opposite sides → BE = 3; triple 3-4-5 → height 4; 7×4 = 28 | solve-geo32-g049 (8-15-17, 24×15 = 360) | SAME (English adds the trap "slanted side × base") |
| 50 | מעוין · The rhombus | 2074-2120 | All sides equal, opposite angles equal, a "perfected parallelogram"; diagonals perpendicular, not equal, bisect each other and the angles; tip: don't memorize, remember it's symmetric left-right AND top-bottom; area = product of diagonals/2, why: half-diagonal triangles ×4 | geo-050 slides 1-4 | SAME (English adds the number examples, slide 5, and "equal diagonals → square") |
| 51 | שאלה: סכום והפרש אלכסונים · Diagonal sum 14, difference 2, perimeter | 2122-2156 | What "absolute difference" means; two equations, add them → 8 and 6; halves 4 and 3; 3-4-5 → side 5 → perimeter 20; closing tip: a rhombus is symmetric, right = left, top = bottom | solve-geo32-g051 (46 and 14 → 30, 16 → 8-15-17 → 68) | SAME (English adds the area trap 240) |
| 52 | דלתון · The kite | 2158-2205 | A squashed rhombus; symmetric left-right only; main and secondary diagonal; main = line of symmetry, two congruent triangles; perpendicular; main bisects the secondary (like the isosceles altitude = median = bisector) and the head angles; two isosceles triangles on one base; area = product of diagonals/2, why: triangle ADC ×2 | geo-052 slides 1-5 | SAME |
| 53 | שאלה: היקף דלתון · Kite, 45° and 60°, DC = 4, perimeter | 2207-2245 | Bottom: isosceles + 60° → equilateral → BD = 4; top: 45-45-90, silver, hypotenuse ÷ √2 → 2√2; stop at "8 + roots": only one choice fits. **Tip: once you see a silver triangle, expect √2 in the answer (an integer leg gives a √2 hypotenuse, and the other way round); some choices have √3, some √2.** Kite symmetric only left-right, so no need to memorize the rules | solve-geo32-g053 (sides 10 → 20 + 10√2) | PARTIAL: everything is there, including stopping early and crossing out the choice with √3. **Her general tip, "a silver triangle → expect √2 in the answer", is not said.** English crosses out the √3 choice only after it has computed 5√2 |
| 54 | טרפז · The trapezoid | 2247-2312 | Bases parallel, not equal; legs not parallel (else a parallelogram); angles on one leg sum to 180 (parallel lines); area (a + b)h/2, why: copy, flip, attach → parallelogram, half of it; "memorize, you won't prove it"; isosceles trapezoid: symmetric, base angles equal, legs extend to an isosceles triangle, diagonals equal and cut into matching pieces; right trapezoid: always two right angles | geo-054 slides 1-5 | SAME (English adds examples, "isosceles: opposite angles sum to 180", and the right-trapezoid tip "drop a height → rectangle + right triangle") |
| 55 | שאלה: טרפז שווה שוקיים, שטח 30 · Isosceles trapezoid, area 30, triangle 3, height 3, find AD | 2314-2368 | EC = 2 from the triangle's area; **tip for every trapezoid question: always drop both heights**; symmetric → BF = 2, the left triangle is 3 too; common mistake: it looks like a square, x ≠ 3, drawings aren't accurate; middle rectangle 30 − 6 = 24 → 3x = 24 → x = 8. Then the formula way, and her warning: **"many students see trapezoid + area and go straight to the trapezoid formula — see how much longer it is"** | solve-geo32-g055 (65, 10, 5 → x = 9) | PARTIAL: both methods, in her order, and the "it isn't a square" mistake are kept. The "drop both heights" tip is softened to "here a second height lets us compare… in general, heights often split a trapezoid" (the summary page keeps "drop the heights"). **Her closing warning about the habit of going straight to the formula is cut** (R35, no which-way-is-better verdict) |
| 56 | מרובעים יסודות לימוד – פתיח · Basic practice intro | 2370-2373 | Last lesson the rules, now basic questions | geo-056 | SAME (English adds: write the shape's properties on the figure, only the useful ones; the answer often hides in a triangle) |
| 57 | שאלה: מה אינו יכול להיות α · What can't α be (easy) | 2375-2411 | 360 → α + β = 140; neither can be 140 or more (β would be 0); check the choices; trap: "α looks acute" — drawings aren't to scale | solve-geo32-g057 (α + β = 146) | SAME |
| 58 | שאלה: היקף מקבילית · Parallelogram perimeter, AB = 5, AE = 2, 70°, 55° (easy) | 2413-2466 | Opposite sides; D = 70, A = C = 110 (opposite or neighbours); ECD = 55 → CE is a bisector; triangle EDC: 55 (by the angle sum, or by the Z) → isosceles → ED = 5 → AD = 7 → perimeter 24 | solve-geo32-g058 (9, 4, 72°, 54° → 44) | SAME (both ways to the 55/54; English adds the pattern "a bisector in a parallelogram cuts off an isosceles triangle"). Her spoken sum "7+5+7+7" was a slip; English is correct |
| 59 | שאלה: שטח ABE במלבן · Rectangle, perimeter of EBC = 9, area of ABE (easy+) | 2468-2552 | Diagonals equal and bisect → 2.5 each → AC = 5 → 3-4-5 → AB = 3. "Learn all the ways now; on the exam take the first one you see." (a) median → equal areas: ABC = 6 → 3; (b) the diagonals cut the rectangle (and every parallelogram) into 4 equal-area triangles: 12/4 = 3; (c) base × height, height = half of BC | solve-geo32-g059 (24, 50 → 10-24-26 → 60) | SAME (all three ways, in her order; "learn them all, take the first one you see" is on the summary page) |
| 60 | שאלה: שטח מעוין, BD = 4, 60° · Rhombus area (medium) | 2554-2634 | Two formulas (side × height, or diagonals/2 for any quadrilateral with perpendicular diagonals); gold triangle → 2√3 → AC = 4√3 → 8√3; other ways to add it up (4 small triangles, top/bottom, left/right); insight: isosceles with 60 → equilateral → two equilateral triangles, a²√3/4 ×2; her verdict "this is the shorter, psychometric way" | solve-geo32-g060 (BD = 10 → 50√3) | SAME (every method; only her verdict sentence is gone, R35. English adds the 30-30-120 link) |
| 61 | שאלה: ריבוע ומשולש שווה צלעות · Square with an equilateral triangle AOD, find α (medium) | 2636-2693 | Pick only the relevant square properties (no diagonals here; mark the angles next to α); mark equal sides with the same tick; the catch: the triangle's sides equal the square's; ABO isosceles; top angle 90 − 60 = 30 → 2α = 150 → α = 75 | solve-geo32-g061 (triangle BPC, asks angle PAD) | CHANGED: all her steps are there, but English asks for the angle next to the 75° one, so it adds one step (90 − 75 = 15) and makes 75 the trap |
| 62 | שאלה: שטח דלתון · Kite area from parts of the diagonals (easy+) | 2695-2743 | A kite = two isosceles triangles; the main diagonal is altitude, median, bisector → OD = OB = 4; 5-4-3 → AO = 3; (12·8)/2, "reduce first" → 48; other ways: two isosceles triangles, or four right triangles | solve-geo32-g062 (17, 15, 12 → 8 → 300) | SAME (English adds "the main diagonal is NOT cut in half" and the difference-of-squares shortcut 17² − 15²) |
| 63 | שאלה: היקף טרפז שווה שוקיים · Isosceles trapezoid, AB = AD = 2, 30° (easy+) | 2745-2790 | Isosceles ABD → 30, 30, 120; same leg → B = 60 → DBC = 30 (or by the Z); C = 60 (equal base angles, or completes A to 180); BCD = 30-60-90 gold → hypotenuse = 2 × short leg = 4 → perimeter 10 | solve-geo32-g063 (7 → 35) | SAME (English adds the 30-30-120 link, BD = 7√3) |
| 64 | סיכום יסודות · Basics summary | (2790, mentioned only) | no subtitles | summary_pages/t32.json (replaces r26-t32-summary) | not comparable |
| P1 | 20 שאלות תרגול עצמי · 20 basic self-practice questions | 2792 | — | geo32-foundation-p01 … p22 | SAME (22 questions, new numbers) |
| 65 | מרובעים לימוד מתקדם – פתיח · Advanced intro | 2794-2799 | Harder questions, "nuances that come back now and then" | geo-065 | SAME (English also previews the question types) |
| 66 | שאלה: מה אינו בהכרח נכון · Which is not necessarily true (medium) | 2801-2866 | Go statement by statement, cross out what's surely true. Her statements are two-way: "every rectangle is a parallelogram, **but not every parallelogram is a rectangle**", the same for rhombus/kite and square/rectangle; she checks both halves using the "most outstanding property"; "a kite with equal sides is a rhombus"; 3 out → mark the 4th without checking; answer: "every parallelogram is a rhombus" | solve-geo32-g066 (answer: "every parallelogram has perpendicular diagonals", shown false by a 9×4 rectangle) | CHANGED: the statements are one-way, and the "but not every…" half becomes a by-the-way remark, so students no longer practise checking both directions; the false statement is about a diagonal property instead of a whole shape. Her method (cross out, mark the 4th on the exam, check in the lesson) is kept |
| 67a | שאלה: מלבן, משולשים 3 ו-9 · Rectangle, triangles 3 and 9, find EBC (easy+) | 2868-2954 | (1) Math way: xh = 6, yh = 18, (x + y)h/2 = 12, "long and exhausting, but a base/anchor when you don't see the short way"; (2) symmetry: drop a height, each diagonal halves its rectangle → 3 + 9 = 12; "that's why it's an easy+ question" | solve-geo32-g067 (6 and 15 → 21) | SAME (both methods and the anchor idea, "the math way works even when we don't see a shortcut"; only the "long and exhausting" verdict is gone) |
| 67b | עקרון הסימטריה – הרחבה · The symmetry principle extended | 2955-3003 | A diagonal halves a rectangle; one triangle on the base with its tip on the top = half; any number of triangles whose bases fill the side; the whole parallelogram family; in a parallelogram, cut by a line parallel to the sides; harder: base cut into 3, shaded = 1/3 of 1/2 = 1/6 | geo-067-after | SAME (the harder example is a quarter → 1/8) |
| 68 | שאלה: איזה נתון מספיק · Which data is sufficient (rather hard) | 3006-3088 | E and G are midpoints. (1) Area ECD = S → its twin is S, right rectangle 2S; **left = right (same base, same height)** → left 2S → shaded S → total 2S; quick insight: white = 1/4 of the rectangle, shaded = 1/2. On the exam, mark and run. (2) AFE, (3) FBG: F's position unknown → no. (4) out | solve-geo32-g068 (AE = 3·ED, BG = 3·GC) | CHANGED: same method and the same reasons for choices 2-4, but with 3:1 points instead of midpoints her "the left and right rectangles are equal by symmetry" step becomes "three times as big" (6s), and the insight becomes "ECD is an eighth, the shaded part a half". It still works |
| 69 | שאלה: טרפז, שטח כהה 10 · Isosceles trapezoid, shaded 10, bases 3 and 6 (medium) | 3090-3172 | (1) Math: external height, 3h/2 = 10 → h = 20/3 = the trapezoid's height → 30; (2) same height → area ratio = base ratio; BC = 2 × AD → white 20; shown by a median: three triangles of 10, "a parallelogram even forms, BD its diagonal"; "if the base were 3× bigger, the area 3×"; "you hardly write anything" | solve-geo32-g069 (5 and 20, 15 → 75) | SAME (both methods, the parallelogram remark and the "3×" line; English adds the trap 60) |
| 70 | שאלה: מחומש על משבצות · Shaded pentagon on a 20-square grid (medium) | 3174-3270 | "A trapezoid? count the sides: a pentagon, we never learned it"; shaded-area questions, two approaches. (1) Subtract: 20 − (2 + 1 + 2 + 3) = 12 (main, most common); (2) completions: **count whole squares, pair the cut half-squares into whole ones by eye**, count 12; (3) symmetry: split into rectangles, each triangle = half its rectangle, 2 + 1 + 2 + 3 + 4 = 12; closing: subtract, or split by completions or by symmetry | solve-geo32-g070 (40 squares → 26) | CHANGED: (1) and (3) and the closing are the same. **(2) her square-by-square completion is replaced** by "every sloping side is a corner rectangle's diagonal, so each shaded piece has a white twin" (deliberate: the spec makes completions exact, and summary-2 adds "pair only pieces that really complete each other, a guess by eye is not a method"). As a result, English methods 2 and 3 now rest on the same rectangle-halves idea |
| 71 | שאלה: חוצה זווית במרובע כללי · Bisector in a general quadrilateral, letters (hard) | 3272-3396 | What's hard: 360 → D, halve, triangle AED, with letters, in under a minute, second-to-last question. (1) Full algebra, crossing out choices as the 45 and then the +β/2 appear; (2) plug in α = 100, β = 70 (in the figure AND in the choices) → 30; drawback: you must cross out all the others; **"if you run out of time and must move on, the first match is a reasonable educated guess"**; **a shortcut while checking ("some already see it's too big")**; closing: algebra is fine if you're strong and fast, most students find plugging in easier, especially at the end of the section | solve-geo32-g071 (B = 130°, α = 110, β = 80 → 50) | PARTIAL: both methods, the crossing out during the algebra, "in the figure and in the choices", and the drawback ("a match alone isn't enough… we check the last one too") are kept. **Missing: the educated-guess-when-out-of-time tip, and the "it's already too big" shortcut.** Her "which way for whom" closing is cut (R35) |
| 72 | שאלה: 5 מלבנים זהים · Five congruent rectangles, perimeter 32 (medium+) | 3398-3441 | The hidden fixed ratio from the arrangement: x, 3x → 1:3; sides 3x, 5x; 16x = 32 → x = 2; "they didn't ask for x, and it's not a choice"; area 6 × 10 = 60 | solve-geo32-g072 (6 rectangles, 1:4, 40 → 96) | SAME (English adds a second finish with the 2:3 ratio of the sides) |
| — | סיכום מתקדם · Advanced summary | (3441, mentioned only) | no subtitles | summary_pages/t32.json (replaces r26-t32-summary-2) | not comparable |
| P2 | 20 שאלות תרגול עצמי · 20 advanced self-practice questions | 3443 | — | geo32-advanced-p01 … p22 | SAME (22 questions) |

**Count by row (34 rows, without the two summaries that have no Hebrew text):** SAME 27 · CHANGED 4 (61, 66, 68, 70) ·
PARTIAL 3 (53, 55, 71) · MISSING 0.

### Count by video (her 32 units)

| Unit | Match |
|---|---|
| Lesson 42 (42a + 42b) quadrilaterals | SAME |
| Lessons 43 square, 45 rectangle, 47 parallelogram, 50 rhombus, 52 kite, 54 trapezoid | SAME (all six) |
| Examples 44, 46, 48, 49, 51 | SAME |
| Example 53 kite perimeter | PARTIAL (the "silver triangle → expect √2" tip) |
| Example 55 trapezoid area 30 | PARTIAL (her warning about going straight to the formula; "drop both heights" softened) |
| Intro 56; Q 57, 58, 59, 60, 62, 63 | SAME |
| Q 61 square + equilateral triangle | CHANGED (asks the neighbouring angle, one extra step) |
| Basic practice (20) | SAME |
| Intro 65 | SAME |
| Q 66 not necessarily true | CHANGED (one-way statements) |
| Q 67 (+ the extension) | SAME |
| Q 68 sufficient data | CHANGED (3:1 points instead of midpoints) |
| Q 69 trapezoid, equal heights | SAME |
| Q 70 pentagon on a grid | CHANGED (her completion counting replaced by exact rectangle halves) |
| Q 71 bisector, letters | PARTIAL (educated-guess tip, "too big" shortcut) |
| Q 72 congruent rectangles | SAME |
| Advanced practice (20) | SAME |

**By video: SAME 25 · CHANGED 4 · PARTIAL 3 · MISSING 0** (32 units including the two practice sets).

---

## 2. English → Hebrew: English content with no Hebrew equivalent

- **solve-q-r26-t32-01** (parallelogram with a 150° angle: the height lands outside), **solve-q-r26-t32-02** (right trapezoid,
  drop a height, 6-8-10), **r26-t32-perimeter** (cuts count twice, notches, corner steps), **solve-q-r26-t32-06** (staircase
  perimeter), **solve-q-r26-t32-07** (rectangle from perimeter + diagonal, squaring a sum). All course additions.
- Big added parts inside her videos: geo-042 slides 2, 5-7 (non-examples, three angle-sum examples); geo-042-2 slide 4 (the
  family tree); geo-043 slide 6 (lengths ×k → area ×k²); geo-047 slide 5 (rectangle and rhombus tests) and slides 8-9 (heights
  with 30/45/60/150°); geo-054 slide 5 (right-trapezoid tip); geo-056 slide 1 (write the properties on the figure); the second
  methods in g044 (Pythagoras), g048 (plug in a rectangle) and g072 (ratio parts); g058's "bisector cuts off an isosceles
  triangle"; g062's difference of squares.
- The two summaries (her summary videos have no subtitles, so they can't be checked) are now the printed page
  `summary_pages/t32.json`.

---

## 3. Recommendations

Every topic-32 video is recorded, so any line added to a video means re-recording that video. The printed summary page
(`summary_pages/t32.json`) needs no recording, and it is the cheap place for a missing tip.

| What is missing | Where it would go | Length | Target recorded? | Recommendation |
|---|---|---|---|---|
| g071: "If time runs out after the first match, mark it: it's a reasonable educated guess" (+ optionally the "already too big" shortcut) | the summary page, the "Letters instead of numbers" row (or solve-geo32-g071 slide 3, after "we check the last one too") | 1 sentence (2 with the shortcut) | g071 recorded (done); the page needs no recording | **RESTORE** on the summary page: a real exam tactic she gives for the hardest question type, and it costs nothing there. Re-recording g071 for it is OPTIONAL |
| g053: "Once you see a silver triangle, expect √2 in the answer (a gold triangle → √3)" | solve-geo32-g053 slide 1 or 2, or the summary page | 1 sentence | g053 recorded (done) | OPTIONAL: English already crosses out the √3 choice, just after the calculation instead of before it. Put it on the summary page if wanted |
| g055: her warning "many students see trapezoid + area and go straight to the formula; see how much longer it is" | solve-geo32-g055 slide 3 | 1-2 sentences | recorded (done) | NOT NEEDED: it is a which-way-is-better verdict (R35); both ways are shown, and the summary page says "drop the heights" |
| g071 closing (algebra if you're strong, plugging in for most students); g060 "the shorter, psychometric way"; g067 "long and exhausting" | — | — | recorded | NOT NEEDED (R35 verdicts; nothing is taught in them) |
| g066: two-way statements ("…but not every Y is X") | solve-geo32-g066 | — | recorded | NOT NEEDED: the reverse direction is still said for every statement, and geo-042-2 teaches "not necessarily" going up the tree |
| g070: her square-by-square completion counting | — | — | recorded | NOT NEEDED: changed on purpose (the English spec makes the completions exact, and summary-2 warns against pairing by eye). Note only that English methods 2 and 3 now use the same idea |
| g068 (midpoints → 3:1), g061 (extra step) | — | — | recorded | NOT NEEDED: her method still works with the English version |

**Where the English is wrong compared with her:** nothing found. The one difference in arithmetic is her own slip in g058
("7 + 5 + 7 + 7", line 2462); the English sum is correct.
