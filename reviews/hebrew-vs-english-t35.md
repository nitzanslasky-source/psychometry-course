# Topic 35 (Three-dimensional geometry): the teacher's Hebrew videos vs the English course

Read-only review, 2026-10-22. Nothing in the course was changed.

- Hebrew source: `~/Downloads/03-Geometry-Original-Subtitles.txt`, lines 5995-7028 (all of it read).
- English: the per-topic text dump `scratchpad/ext/course/t35.txt` (every video's spoken text) and `q35.txt` (the practice
  questions), the current flow in `~/Downloads/Psychometric-Teacher-Studio-v19-hybrid.html`, and the base translation
  `studio-build/base-v18.html` (checked for g121, g125, g126, g131).
- **Recording status:** topic 35 has no reading scripts in `ai_scripts/` yet (only `r26-t35-summary.json`), so none of its
  videos are in the `video_status.py` tracker (they appear in no list: record / send / done / check / reread). **Nothing in
  topic 35 is recorded**; every target below is unrecorded and is about to be rewritten anyway.

**Match scale.** The English course gives every question new numbers on purpose (memory rule *questions-differ-from-hebrew*), so new
numbers on their own do not count as a change.
SAME = same idea and every one of her methods, new numbers only. CHANGED = same idea, but the method, the example type or the order
is different (the cell says what). PARTIAL = some of her content or one of her methods is missing (the cell says exactly what).
MISSING = no English equivalent.

**Her names carry over:** גוף ישר / גוף מחודד → "straight solid / pointed solid"; יחסי נפחים / יחידות יחס → "volume ratios / ratio
units"; משולשים פנימיים → "inner triangles"; חוסם חסום → "inscribed and circumscribed"; הברקה → "a psychometric flash";
קובייה הונגרית → "Rubik's cube questions" (the natural English name).

**Id numbering.** Her section is one lesson (definitions), a 4-line intro and 12 questions; the ids are geo-119 (lesson), geo-120
(intro), g121-g132 (her 12 questions, in her order). No gaps: nothing of hers was merged or dropped. The current flow keeps her
order and inserts three added mini-lessons (water, cones, cube facts) with one question each, plus a summary.

---

## 1. Hebrew → English (her videos, in her order)

| # | Her video (Hebrew title · English gloss) | Lines | What she teaches / how she solves it (every method) | English equivalent | Match |
|---|---|---|---|---|---|
| 1 | הגדרות ונוסחאות תלת מימד · 3D definitions and formulas | 5996-6224 | Don't be afraid of 3D, the questions are simple. Edge, face, base; prism (lift identical polygons); cylinder; lateral area = unroll the cylinder (toilet roll) → 2πr·h; box lateral (2a+2b)c, cube 4a²; **one general rule: base perimeter × height**; total surface = lateral + 2 bases (cube 6a², box 2(ab+ac+bc), cylinder 2πrh + 2πr²) "understand, don't memorise"; volume = content (a 330 ml cola can, cm³), stacked rectangles → base area × height; cube a³, cylinder πr²h; pointed solids (cone = clown hat, pyramid): ⅓ of the straight solid that "should have been there"; recap | geo-119 (all slides) | SAME (the cola can is a 500 ml water bottle). English adds: a prism lying on its side (find the two identical faces; the height joins them), 1 ml = 1 cm³, the height goes straight down not along a slanted edge, and a "formula page" slide (what NITE gives, what to know by heart) |
| 2 | תלת מימד – פתיח · Intro to the question lesson | 6226-6230 | Last lesson the basics; now higher-level questions and recurring nuances | geo-120 slide 1 | SAME (English adds a "What's ahead" slide) |
| 3 | חרוט מלא נוזל · Which container holds the cone's liquid (medium) | 6232-6321 | Cone r=√5, h=6 → ⅓ of the cylinder → 10π ≈ 31 (π = 3.14). Go through the choices: bigger or equal → mark, smaller → eliminate. Cube 3³ = 27 ("a cube is edge cubed: a 3D square"), cylinder 9π, box 5·3·2 = 30 ("just multiply the dimensions"), square pyramid 16·6/3 = 32 ✓. "Eliminated three → on the exam mark the fourth." The two key principles: straight vs pointed | solve-geo35-g121 (cone r=√6, h=12 → 24π) | CHANGED: (a) the estimate of π: English bounds it, "π is more than 3 and less than 3.5" → 72 < water < 84, instead of her 3.14; (b) the right choice (the pyramid) is choice 2, so English marks it and checks the rest "in the lesson", instead of her "eliminate three, mark the fourth". English adds the close-call warning (the box is 72, π is MORE than 3). Every principle is kept |
| 4 | גליל וחרוט – נפחים שווים · Cylinder + cone, equal volumes (easy+) | 6324-6369 | (1) Equation πr²h = πr²H/3, cancel the base → H = 3h. (2) Volume-ratio insight: same base and height → cone = ⅓; height ×3 → volume ×3 → 3h, answered without solving. "This principle helps in harder questions" | solve-geo35-g122 (cone = 4 × cylinder → 12h) | SAME (both methods; the numbers add one step, ×4, and English adds the trap 3h) |
| 5 | תיבה 120 – הגוף הכהה · Box 120, the shaded prism (medium+) | 6372-6436 | (1) Add unknowns: 2x·y·z = 120; the shaded solid is straight (equal bases) — a triangular prism; xy/2·z = half of xyz = 30. (2) Symmetry from above: the line cuts the rectangle in halves, the diagonal halves again → ¼ → a wall instead of a line → ¼ of 120 = 30. "There is almost always a shorter way" | solve-geo35-g123 (320, AM:MB = 1:3 → ⅛ → 40) | SAME (both methods and her closing words) |
| 6 | מנסרה ישרה – שטח מעטפת · Right prism, lateral area (medium) | 6439-6468 | (1) Formula: base perimeter × height; 3-4-5 triple; add 3+4+5, or "the average is 4, so 3×4"; ×2 = 24. (2) Add the three faces 10+6+8. "Pick the way that suits you" | solve-geo35-g124 (9-12-15, height 5 → 180) | SAME (both methods, the average shortcut kept). English adds that this prism lies on its side and the trap 288 (total surface area) |
| 7 | 8 קוביות – שטח פנים מינימלי · 8 cubes, smallest surface area (medium+) | 6471-6555 | Min/max question. Three of the four shapes are NOT boxes, "there is no formula", so (1) trial and error: 1 face = 1 cm², count front/top/side and double by symmetry (34, cube 24, 30, 32); out of time → once 24 < 34 you can already drop choice 1 ("this comes near the end of the section"). (2) Insight: apart = 48 faces = maximum; each contact loses 2 faces; most compact = smallest → the cube | solve-geo35-g125 (18 cubes, four boxes 1×2×9, 2×3×3, 1×1×18, 1×3×6) + slide 3 (a 6-cube staircase) | CHANGED: all four English choices are boxes, so her reason for counting ("no formula for these shapes") no longer fits the question itself; the counting of a non-box shape moved to an added slide (the staircase). Trial and error, the symmetry doubling, the out-of-time elimination and the "pack them tight" insight are all kept. (The change goes back to the base translation, which already used 12 cubes in boxes) |
| 8 | גליל חסום בתיבה · Cylinder inscribed in a box (hard) | 6558-6648 | Inscribed/circumscribed, as in circles. (1) Full math: side a = diameter → r = a/2 → πa³/2 over 2a³ = π/4 (with the fraction-division "arcs"). (2) Plug in numbers: **not 1, because the radius would be ½ — take a = 2** → 4π/16 = π/4, check the choices. (3) Estimate: ratio of volumes is constant, so any answer with a is a distractor; π/2 ≈ 1.5 > 1 impossible; π/4 ≈ ¾ makes sense. Verdict: full math not recommended, plugging in the safest, estimating depends on the answers | solve-geo35-g126 (side 2k, height 5k; asks the fraction OUTSIDE the cylinder → 1 − π/4) | CHANGED: (a) the question asks for the part outside (1 − π/4) instead of her cylinder/box ratio; (b) the reason for not plugging in 1 is different: in English k = 1 "can't separate" choices 1, 3, 4 (her reason, a fractional radius, does not arise because the side is 2k). All three methods and her verdict are kept; English adds the power count (power 3 − 3 = 0) |
| 9 | פירמידה נוסרה מקובייה · Pyramid cut from a cube, 18 left (medium) | 6650-6692 | (1) Scheme cube − pyramid = 18 → a³ − a³/3 = 18 → a = 3 → 9. (2) Ratio units: pyramid 1, cube 3, rest 2 → 2 units = 18 → 9. "Volume ratios really help" | solve-geo35-g127 (60 left → 30) | SAME (English adds that here a is not even a whole number, so the ratio way wins) |
| 10 | גובה פירמידה מרובעת · Height of a square pyramid (medium+) | 6695-6753 | (1) Build an inner right triangle (height ⟂ base ⟂ every line on it); half the diagonal from the silver triangle (÷√2) = 1; Pythagoras → √15. (2) Estimate: height < slanted edge 4 (anchor √16) → drop 2√5, √17, 4√2 (≈ 4×1.4) | solve-geo35-g128 (side 4√2, edge 7 → √33) | SAME (both methods, the anchor √49, "possible, not certain yet") |
| 11 | קובייה – שטח המשולש הכהה · Cube, area of the face-diagonal triangle (hard) | 6755-6829 | (1) Base = face diagonal 2, height via an inner right triangle (1, √2) → √3, area √3. (2) Flash: three face diagonals → equilateral → a²√3/4. Then three angle situations in a cube: edge & diagonal of another face 90°, edge & diagonal of the same face 45°, two face diagonals 60° (connect the third) | solve-geo35-g129 (edge 4√2 → 16√3) | SAME (both methods and the three angles; English adds the warning that the 90° case needs the lines to meet at one corner) |
| 12 | קובייה – היקף משולש ABC · Cube, perimeter of edge/face-diagonal/body-diagonal triangle (medium+) | 6831-6913 | Edge 1, face diagonal √2, 90° angle → Pythagoras √3 → 1+√2+√3. Then: cube body diagonal = edge × √3 ("square √2, a 3D square √3"); exam example edge 5 → 5√3; back: 12 ÷ √3 = 4√3 (her "drop the root, divide, attach the root" trick); a box has no fixed ratio → two right triangles (3,4 → 5; 5,12 → 13 "חמסה, בת מצווה, בר מצווה") | solve-geo35-g130 (edge 3 → 3+3√2+3√3; edge 8; diagonal 27 → 9√3; box 9,12,8 → 15 → 17) | SAME (every move; English explains why the division trick works and adds the one-step formula √(a²+b²+c²)). Her 5-12-13 Hebrew mnemonic (hamsa / bat-mitzvah / bar-mitzvah) is gone, naturally, because the English box uses 8-15-17 |
| 13 | קוביות בתוך תיבה · How many cubes fit in a box (medium+) | 6916-6969 | First ask: liquid or solid? Liquid spreads, solids may leave gaps (8 small cubes fit a cube exactly; in a crate only 4). She **draws the packing**: 3 along, 2 deep, a floor of 6, two floors = 12, a third floor won't close. Then the exam way: how many times the edge goes into each dimension, ignore the remainder, multiply | solve-geo35-g131 (edge 4 into 18×9×11 → 16) | CHANGED: the exam method is the same, but English skips her drawn floor-by-floor packing (it goes straight to "no time to draw") and her two little pictures (fits exactly / only 4 fit) are reduced to one sentence. English adds the trap of dividing the volumes (27) |
| 14 | קובייה הונגרית · Remove a corner cube (medium) | 6972-7025 | Volume: 8 → 7, drops. Surface: lose 3 faces, 3 hidden ones appear → unchanged. Three situations: corner 0, middle of an edge +2, centre of a face +4; "lost + gained always complete 6" | solve-geo35-g132 (27 cubes, edge 4) | SAME |
| 15 | 20 שאלות תרגול עצמי · 20 self-practice questions (no video) | 7028 | — | geo35-core-p01 … p27 (q35.txt, practice section) | SAME (all kept, with extra ones added) |

**Count by row (15 rows):** SAME 11 · CHANGED 4 (3, 7, 8, 13) · PARTIAL 0 · MISSING 0.

### Count by video (her 15 units)

| Unit | Match |
|---|---|
| Lesson: definitions and formulas | SAME |
| Intro | SAME |
| Q cone liquid (g121) | CHANGED (π bounded 3-3.5 instead of 3.14; correct choice found early) |
| Q cylinder + cone (g122) | SAME |
| Q box 120 shaded prism (g123) | SAME |
| Q prism lateral area (g124) | SAME |
| Q 8 cubes min surface (g125) | CHANGED (choices are all boxes; non-box counting moved to an extra slide) |
| Q cylinder in box (g126) | CHANGED (asks the outside part; different reason for not plugging in 1) |
| Q pyramid from cube (g127) | SAME |
| Q pyramid height (g128) | SAME |
| Q cube triangle area (g129) | SAME |
| Q cube triangle perimeter (g130) | SAME |
| Q cubes in a box (g131) | CHANGED (her drawn packing walkthrough condensed) |
| Q Rubik's cube (g132) | SAME |
| 20 practice questions | SAME |

**By video: SAME 11 · CHANGED 4 · PARTIAL 0 · MISSING 0.**

---

## 2. English → Hebrew (English topic-35 videos and parts with no Hebrew equivalent = added)

| English video / part | Added content | Hebrew source? | Recorded? |
|---|---|---|---|
| geo-119 slide "Lying down" | A prism on its side: find the identical faces, the height joins them | none | no |
| geo-119 slide "On the formula page" | What the NITE formula page gives and what to know by heart | none | no |
| geo-119 (parts) | 1 ml = 1 cm³; the height goes straight down, not along a slanted edge | none | no |
| geo-120 slide "What's ahead" | Overview of the lesson | none | no |
| r26-t35-water + solve-q-r26-t35-01 | Liters ↔ cm³ ↔ m³; water height = volume ÷ base area; pouring keeps the volume | none | no |
| r26-t35-cones + solve-q-r26-t35-02 | Solids of revolution (rectangle → cylinder, right triangle → cone; the radius counts more); slant height ≠ height | none | no |
| r26-t35-cubefacts + solve-q-r26-t35-03 | Box diagonal √(a²+b²+c²) / longest rod; faces-edges-vertices of prisms and pyramids; three face areas → volume; quick impossibility checks; the painted cube | none (her g130 diagonal moves are the seed) | no |
| solve-geo35-g125 slide 3 | Counting the faces of a non-box staircase | her g125 reason for counting (her shapes were not boxes) | no |
| solve-geo35-g126 (part) | The power count (power 3 − 3 = 0) | none (from the algebra topics) | no |
| traps added in g122, g124, g131, g130 | 3h, 288, the volume-division trap, etc. | none | no |
| r26-t35-summary | Spoken summary of the whole topic | none | no |
| mem-solids, mem-cube-facts | Reference cards | none | — |
| practice geo35-core-p21 … p27 and the 3 r26 questions | Extra practice | none | — |

---

## 3. Missing from English: restore?

Nothing of hers is missing outright. The four CHANGED rows, and what the rewriters could do:

| # | Her content | Where it would go | Target recorded? | Recommendation |
|---|---|---|---|---|
| 1 | g125: her reason to count faces — "three of the shapes are not boxes, there is no formula" | solve-geo35-g125: either make choices 1, 3, 4 non-box shapes (L-shapes, steps, like hers) so slide 1 counts real non-box shapes, or keep the boxes and add 1 sentence: "for a box there is a formula, but counting works for any shape" | no | **Optional** (the staircase slide already teaches counting a non-box shape). Note: with four boxes the English "Instead of formulas — let's count" is slightly odd, because the box formula 2(ab+bc+ca) exists and is in the written explanation |
| 2 | g131: her drawn packing (a floor of 6, two floors, the third won't close) before the exam method | solve-geo35-g131 slide 1, 2-3 sentences with a picture (4 along, 2 deep → 8 per floor, 2 floors) | no | **Optional.** It makes "ignore the remainder" visible for weak students; costs ~3 sentences |
| 3 | g121: π ≈ 3.14 | solve-geo35-g121 | no | **Not needed.** The English bounds (3 < π < 3.5) are her estimating idea in the course's whole-number style (memory rule *no-decimal-estimates*), and the numbers were chosen so the bounds decide it |
| 4 | g126: "don't plug in 1, the radius would be a fraction" | solve-geo35-g126 slide 2 | no | **Not needed.** The English reason (1 can't separate the choices) is a true and better-fitting reason for these numbers; her idea "pick a convenient number, not automatically 1" is kept |

**Nothing in the English is wrong compared with her.** All her named principles (straight vs pointed, volume ratios, inner
triangles, the three cube angles, √3 for the body diagonal, liquid vs solid, the three Rubik's-cube situations) are in the
English, in her order.
