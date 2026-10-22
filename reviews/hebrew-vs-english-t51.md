# Topic 51 (Psychometric Thinking): the teacher's Hebrew videos vs the English course

Read-only review, 2026-10-22. Nothing in the course was changed.

- Hebrew source (named in the header and comments of `math_patches/_ai_vis_t51.py`): `studio-build/pt_src/seg1_intro.txt` (486 lines),
  `seg2_plug_answers.txt` (180), `seg3_plug_numbers.txt` (415), `seg4_estimation.txt` (287), `seg5_insights.txt` (169). All of it was read.
- English: the current reading scripts `studio-build/ai_scripts/pt51-*.json` and `solve-pt-q01…q24(-2).json` (spec `math_patches/_ai_vis_t51.py`,
  flow order `F9_FLOW`). Topic 51 is **not** in `base-v18.html`. The original English translation is `studio-build/modulesV51.py`,
  and that is what I used as "the base". The topic summary video `pt51-summary` was replaced by the summary page `summary_pages/t51.json`.
  Its old script `ai_scripts/pt51-summary.json` (6 Oct) is stale but still on disk.
- Recording status (`python3 video_status.py --list record`): **every topic-51 video is unrecorded** (all 39 ids, from pt51-intro to
  pt51-understanding). She reads all of topic 51 on camera (`studio_ai.py`, `TEACHER_TOPICS = {51}`). So every restore below costs no re-recording.

**Match scale** (same as the t23 report). English questions get new numbers on purpose, and new numbers alone are not a change.
SAME = same idea and every one of her methods. CHANGED = same idea, but a method, a claim or the question type is different.
PARTIAL = part of her content or one of her methods is missing. MISSING = no English equivalent.

**Her structure.** Each Hebrew segment is **one lesson video**: a short opening, then 3-5 worked "sample questions" (each opens with
"Question N, position in the section, difficulty"), then a summary. In English each segment became a short lesson (heavily expanded)
plus one solution video per sample question (pt-q01…q23), and the long ones are split into camera parts (`-2`, `-3`, `-4`).
The id numbers don't follow her question numbers: pt-q01-05 = seg1, q06-09 = seg2, q10-15 = seg3, q16-19 = seg4, q20-23 = seg5, and
**q24 is new** (no Hebrew source). There are no gaps.

**Her method names in English:** שיטות העל → "super-methods"; הצבת תשובות → "plugging in the answers"; הצבת מספרים → "plugging in
numbers"; הערכת סדר גודל → "order-of-magnitude estimation"; הברקה → "insight"; חישוב חלקי → "partial calculation"; חישוב בערך → (no
separate name, part of the estimate); הדרך המתמטית/הטריוויאלית → "the math way / the calculating way"; ספרה אחרונה → "the last digit".

---

## 1. Hebrew → English (her videos, in her order)

### Seg 1: מבוא לחשיבה פסיכומטרית · Intro to psychometric thinking (one video, seg1 lines 1-486)

| # | Her part (Hebrew · gloss) | Lines | What she teaches / every method | English equivalent | Match |
|---|---|---|---|---|---|
| 1a | פתיח · Opening | 1-33 | The exam predicts academic success and ranks candidates; the questions are "special": school way vs shortcut / creative thinking; like gifted tests; a few super-methods let us solve "as if gifted"; each gets its own lesson; **practise all these lessons *before* you start studying**, and at home solve both ways | pt51-intro slides 1-3, 5-7 | PARTIAL (trivial): all there except "go through these lessons before you start studying the other topics" (the base had it, modulesV51 line 401). English adds slide 4 (25×4×37÷37, 999×3) and names the three methods up front (slide 6) |
| 1b | שאלה 17 – שורש 16,384 · Q17, √16,384 | 35-92 | No calculator but there are answers; calculating way = square every choice; **last digit** (6×6=36, 4×4=16 → choices 2, 3 out); 200² = 40,000 → 202 too big (**order-of-magnitude**); "the answers are part of the question"; thinking vs calculating | solve-pt-q01 (√19,044) + q01-2 slide 3 | SAME. English adds why only the last digits matter, and q01-2 (23×47 by the last digit; √1,849 by the size; when to use each) |
| 1c | שאלה 15 – סלי ביצים · Q15, egg baskets | 94-169 | Before/after table, x; 7/11 → ×11, open, 900 = 18x, **divide by 9 first**; then plug in the answers; "don't check in order, **start with the most convenient (round)**"; 50 → 350/550 → 7/11. **"In a large part of these questions the right answer really is that first round answer — NITE rewards whoever thinks this way"** | solve-pt-q02 (9/13, 500/600; "divide by 11 first") + q02-2 | CHANGED: every method is there, but her claim is reversed. q02-2 says "Starting with a round number makes the check easier. **But it doesn't guarantee that the round number is right.**" English adds the trap (forgetting to add the eggs to B) and a 2nd example (x²+x = 110) |
| 1d | שאלה 20 – ביטוי אלגברי · Q20, what does it equal | 171-262 | "What does it equal" = an equivalent choice; open the short formula, collect; **split into 3 fractions** instead of a common factor (2ab/2ab = 1 cancels +1… she has −1); then **plug in numbers**: a = b = 1 (allowed, "nobody said different"), result 2; check each choice; **"we don't look for the right one, we must rule out 3"** | solve-pt-q03 + q03-2 | SAME (English adds why a lucky match is possible, and a 2nd example: 2^(x+1) + 2^x) |
| 1e | שאלה 20 – גליל חסום בקובייה · Q20, cylinder in a cube | 264-354 | πr²h, the formula sheet; slide the edge inward → diameter = a; **the bracket trap** (a/2 without brackets → choice 1); then estimation: cube = a³, cylinder a bit less; π ≈ 3; three choices bigger than the cube; "by the way 3/4 makes sense"; NITE gave 3 impossible choices on purpose, not 3/4, 2/3, 4/5 | solve-pt-q04 (edge 3a) + q04-2 | SAME (English adds why the volume is base × height and a 2nd example: a circle in a square) |
| 1f | שאלה 20 – שתי קוביות · Q20, two dice | 356-466 | Fair dice = regular dice; a table by the red die; 1/6 × 5/6 (**"and" → multiply**); **"or" → add** → 15/36 = 5/12; "long, not trivial"; what an insight is (unique to the question, rarer, practise); the insight: 36 − 6 doubles = 30, split equally by symmetry → 15/36 | solve-pt-q05 | CHANGED: the question is now "**at least as large**" (ties count), so the answer is 21/36 = 7/12 and the insight ends with "15 + the 6 doubles". All her steps and both probability rules are kept. English adds the trap "symmetric, so a half" |
| 1g | סיכום · Summary | 467-486 | School way vs shortcut; 3 super-methods that work in very many cases; rare insight questions; separate lessons follow; practise; at home solve both ways, use whatever comes to mind | pt51-intro-wrap | SAME (English adds slide 3, "the signs we met") |

### Seg 2: הצבת תשובות · Plugging in the answers (one video, seg2 lines 1-180)

| # | Her part | Lines | What she teaches / every method | English equivalent | Match |
|---|---|---|---|---|---|
| 2a | פתיח · Opening | 2-5 | "We met the super-methods; now we go deeper into plugging in the answers; a sample question" | pt51-plug-answers slide 0 | SAME. English then adds a whole lesson (slides 1-5: why it works, the two signs, x(x+3) = 40, starting from the middle of ordered choices, "fits every given", what to try first) |
| 2b | שאלה 2 – שני אי-שוויונים · Q2, two inequalities | 7-52 | Q2 should be easy, so why two inequalities? Because of the answers; plug in 1 → out; **2 is out without calculating (a positive gives a positive)**; −3 fits → **once a choice fits, mark it, no need to rule out 3**; NITE plants seemingly hard questions to reward whoever stops and thinks | solve-pt-q06 (x² < 25, 3x+6 < 0) | SAME (the "positive gives positive" shortcut is applied to choice 3; English adds the trap choice −7, which passes only one given) |
| 2c | שאלה 13 – נדב ועמית · Q13, Nadav and Amit's cards | 54-83 | Could build an equation, "but why?"; **estimation first**: Nadav > half → 45 and 47 out; plug in the round one (60) → fits; **"starting from convenient answers is very important, also because in a large part of the questions the round answers are where the right answer is; NITE builds the questions that way"** | solve-pt-q07 (90 cards, 1/5) | CHANGED: the methods are all there (cross out what makes no sense, then the round choice), but her claim is replaced by the opposite: "In another question, the convenient choice may fail… We always choose easy arithmetic first" |
| 2d | שאלה 18 – קובי, מכנסיים וחולצה · Q18, Kobi's discounts | 85-142 | Two equations is hard; plug in from convenient answers: 100 → 290 ✗, 200 → 330 ✗ ("I'm a bit bummed"); **"usually the right one is round – not always; this question is here to teach what to do then: just carry on"**; 180 ✗; 3 out → mark the 4th without checking; **estimation shortcut**: 300 is much closer to 290 than to 330, so 125 (near 100), not 180 | solve-pt-q08 (280 instead of 500; 50, 150, 140 → 75) | CHANGED: every step and the estimation shortcut are there (English even explains why each 10 changes the total by 4). Her framing "usually, but not always" became "round numbers make checking easier, but they don't have to be right" |
| 2e | שאלה 18 – רון ומירי · Q18, Ron and Miri's stamps | 144-166 | No round/convenient answer → just start from the first; 9 → 12 and 6 ✓; "Q18, end of the section, and it was simple – amazing" | solve-pt-q09 slides 0-1 (4 stamps; 12 → 16 and 8) | SAME |
| 2f | סיכום · Summary | 167-180 | The answers help; a fit → mark it; estimation rules out illogical answers; **start from round answers – "in most cases that will also be the right answer, not always, but in most"**; 3 out → mark the 4th | solve-pt-q09 slide 2 | CHANGED: everything except "in most cases the round one is right", which is dropped (the base had it, modulesV51 lines 700-703, 850) |

### Seg 3: הצבת מספרים · Plugging in numbers (one video, seg3 lines 1-415)

| # | Her part | Lines | What she teaches / every method | English equivalent | Match |
|---|---|---|---|---|---|
| 3a | פתיח · Opening | 2-4 | "The most common of our super-methods" | pt51-plug-numbers slide 0 | SAME. English adds a 4-part lesson (pt51-plug-numbers 1-4, ~20 min): restrictions, zero, two letters, ratio case, more letters than equations, the "nothing changes" value, counterexamples, "cannot be determined / none of the above" |
| 3b | שאלה 17 – שורש בתוך שורש · Q17, root inside a root (x ≥ 3) | 6-45 | School way = spot the short formula; but an expression with x and **number choices → same value for every allowed x → a particular case**; x = 3, the smallest/most convenient → √7; "Q17, solved in 10 seconds"; **case 1: an expression with an unknown. Careful: an *expression* is "something = ?"; an *equation* is "something = something", and there you must not plug in** | solve-pt-q10 (x ≥ 4 → √6) + pt51-plug-numbers slide 2 (the expression vs equation warning) | SAME (English adds why x = 0 isn't allowed and the algebra as a 2nd way; her "Q17, 10 seconds" line is not said) |
| 3c | שאלה 20 – משולשים וחוצה זווית · Q20, triangles and a bisector | 47-126 | The long angle chase; alpha in every choice → **case 2: an unknown in the answers**; choose a value **"logical according to the drawing – not 120"** → 50; β = 120; **rule out, don't look for the right one**; "a result ending in 5 can't be 120" without calculating; 3 out → mark the 4th; **"we lowered the difficulty: with numbers it would be a beginning-of-section question; we flattened the exam's difficulty"** | solve-pt-q11 | CHANGED (one nuance): every method is there, plus the full algebra. But her rule for choosing the angle ("one that looks logical in the drawing") became "fit the angle conditions, not just the drawing", and pt51-plug-numbers-2 slide 1 adds "Don't choose an angle just because it looks that size in the drawing". The English reason is sound (alpha = 40 breaks the triangle) |
| 3d | שאלה 19 – עצרת · Q19, factorial | 128-207 | Teaches the factorial (5!, 4!, 3!); few solve it with algebra; a = 1 (smallest positive whole) → 2; only 2 out → **a 2nd plug-in, and don't recheck the ones already out**; a = 2: **6! "6×5 = 30 already too big", stop** | solve-pt-q12 (a!·(a+2)!) | SAME ("8×7 = 56 already more than 48"; English explains why 1 causes ties and adds the short algebra) |
| 3e | שאלה 20 – עטים ודיו · Q20, pens and ink | 209-287 | "Wow, confusing" (x/y words per pen); letters in the answers → plug in; **x = y = 1 → every choice gives 1, nothing ruled out**; why: powers, products, division – 1 changes nothing → **choose values that give distinct answers**; x = 2, y = 1 → 2 pens; "we turned Q20 into Q2" | solve-pt-q13 (x³y words) | CHANGED: English looks at the choices *before* plugging and skips 1 (and also rejects x = y = 2), instead of plugging 1, seeing it fail, then explaining why. The rule "choose distinct-result numbers" and x = 2, y = 1 are kept. Her "we turned Q20 into Q2" is not said |
| 3f | שאלה 20 – שמלה בהנחה · Q20, Ella's dress | 289-341 | "From its position it's probably less simple than it looks – but we're not in the difficulty game"; x in the answers; **in percent questions plug in 100**; where? not at x (120 is awkward) but **at the whole, the original price**; 20 out of 100 = 20%; rule out the rest | solve-pt-q14 (40 shekels) | SAME (her line about the position/difficulty game is not said; English adds the one-line algebra) |
| 3g | שאלה 12 – אורית ובתיה · Q12, Orit and Batya | 343-389 | No letter anywhere – but a ratio → **case 3: ratio problems** (1:2 = 2:4 = 10:20); a table; 1 shekel → 1/4 is a fraction → **"who chose the 1? I did – so I can change it"** → 4 → 7:4 | solve-pt-q15 (a third → 3 → 5:3) | SAME |
| 3h | סיכום · Summary | 390-415 | Works like magic; **double advantage: difficulty and time**; when: expression with an unknown, unknown in the answers, ratio; rules: rule out 3, 3 out → mark the 4th, otherwise another plug-in, choose distinct-result and convenient numbers, change an inconvenient plug-in; the most important technique, practise | pt51-plug-numbers slide 1 + pt51-plug-numbers-4 slide 4 | SAME (moved before the questions; English adds the 4th case, more letters than equations) |

### Seg 4: הערכת סדר גודל · Order-of-magnitude estimation (one video, seg4 lines 1-287)

| # | Her part | Lines | What she teaches / every method | English equivalent | Match |
|---|---|---|---|---|---|
| 4a | פתיח · Opening | 2-5 | "A bit less known, but works great" | pt51-estimation slide 0 | SAME. English adds a lesson (pt51-estimation 1-2: 19×51 with choices ×10 apart, benchmark squares, roots between whole numbers, √90+√26, fraction sums, the signs, the trap when the choices are close) |
| 4b | שאלה 19 – גזרה פחות משולש · Q19, sector minus triangle (r = 1) | 9-99 | Shaded = sector − triangle; in estimation we rule out 3. **Way 1: the pattern of the calculation – "where is the π?"**: the π is in the sector, so look for "π minus a number": "number − π" ✗, "π / number" ✗ (2 out in seconds); "some questions π is always on the right side, in others only one choice has it right"; **way 2: π ≈ 3 → a negative area is out** ("the exam won't write −5, it hides it behind π"); then **partial calculation**: the pizza (1/4 = 90°, 1/8 = 45°) → π/8, peek at the choices, only one has π/8 | solve-pt-q16 (r = 2) | **PARTIAL: her "where is the π" pattern method is missing**, and it works perfectly with the English choices (4 − π is "number − π"; π/√2 is "π / number"). English instead first calculates the triangle (Pythagoras → area 1) and the sector (π/2), and bounds π between 3 and **3.2** to place the area between 0.5 and 0.6. The negative-area rule, "hides it behind the π", the pizza and the named "partial calculation" are kept. The base had the π pattern (modulesV51 lines 1289-1294, 1346) |
| 4c | שאלה 20 – √2/(1+√2) · Q20, a root fraction | 100-171 | The conjugate trick "only some 5-unit students know"; if not: **√2 ≈ 1.4** → 1.4/2.4 = 14/24 → **swap for a close fraction that reduces nicely, 15/25 = 3/5 = 0.6**; compare the choices numerically; **the 3 numbers to know: π ≈ 3, √2 ≈ 1.4, √3 ≈ 1.7** | solve-pt-q17 (√2/(2+√2)) + pt51-estimation slide 3 + pt51-estimation-2 slide 2 | CHANGED: the conjugate is there. The estimate uses **bounds** (√2 between 1 and 1.5; the fraction between 1/4 and 1) instead of plugging in 1.4, and the lesson says "we never need the digits of root two". Her "three numbers to know" list is gone (this follows the later *no-decimal-estimates* rule). Her "close fraction that reduces nicely" moved to the estimation lesson (29/59 → 30/60) |
| 4d | שאלה 20 – מלבן ורבעי מעגלים · Q20, rectangle and quarter circles | 173-241 | The middle segment needs a helper line + Pythagoras – **what if you don't see it? estimate**. "Figures aren't necessarily accurate – how can I estimate?" **(1) most exam figures are accurate; (2) rule of thumb: regular shapes (square, circle, equilateral triangle, cube) are accurate**, ratios are kept when you scale; a whole lesson on this later. The middle part is **more than a radius (1) and less than the diameter (2)**; **"use your eraser to measure"**; width between 3 and 4 → area between 6 and 8; √3 ≈ 1.7 → 6.8 ✓, √2 ≈ 1.4 → 5.6 ✗, 8 ✗, 10 ✗ | solve-pt-q18 (r = 2: 16√3, 16√2, 32, 40) | CHANGED, and **it contradicts her**: q18 says "On the exam, a figure is not necessarily drawn to scale. So can I estimate from the figure? **No, we shouldn't measure the sketch.**" It then does the helper line + Pythagoras (x² = 12, between 3 and 4) – which is exactly the construction her estimate was meant to avoid. Her accuracy rule, the regular-shapes rule and the eraser are **missing**. Her estimate still works with the English numbers (middle part between 2 and 4 → AD between 6 and 8 → area between 24 and 32). The base had her version (modulesV51 lines 1325-1331) |
| 4e | שאלה 13 – אלכוהול בשני בקבוקים · Q13, alcohol in two bottles | 243-276 | 20% of 2.2 by 10% (move the decimal point) = 0.44; **2% of 3 is negligible – don't calculate it**; look for "0.44 and a bit" → 0.5; built on purpose to reward whoever sees it's negligible | solve-pt-q19 (3.2 L at 20%, 2 L at 3%) | SAME (English bounds the small part below 0.2 instead of just calling it negligible) |
| 4f | סיכום · Summary | 277-287 | A new super-method; saves time; **rescues you when stuck** (a missed helper line, the √2 expression) | pt51-estimation-2 slide 3 (the second sign: "a long calculation or I'm stuck… a helper line… an expression where I don't know where to start") | SAME (moved before the questions; the estimation block has no closing summary) |

### Seg 5: הברקות · Insights (one video, seg5 lines 1-169)

| # | Her part | Lines | What she teaches / every method | English equivalent | Match |
|---|---|---|---|---|---|
| 5a | פתיח · Opening | 2-14 | The questions reward creativity; 3 super-methods cover much; insight questions: specific to one question, what works once won't work again; the only preparation: practise a lot, "open your head" | pt51-insights slides 1-2, 5 | SAME. English adds slides 3-4 (how to look: repeats, double/half, shared parts; 48+73+96 − (46+71+94)) |
| 5b | שאלה 6 – שברים · Q6, (1/3+1/4)/(2/3+2/4) | 16-44 | Common denominator 12, divide fractions (reciprocal or "the arcs") → 1/2; insight: the bottom is exactly double the top; **banana and apple**; **NITE wrote 2/4 not 1/2 on purpose**; "I love this question" | solve-pt-q20 (1/5, 1/6; "2/6 not 1/3") | SAME (English adds the flip trap → 2) |
| 5c | שאלה 19 – רוני משקיע · Q19, Roni's investment | 46-100 | Solvable in seconds without calculating; simpler example first (100 shekels, 10%; invest half → 5%); half the money → half the percent: 2% + (1%…4%) → 3%-6%; **if you calculate: work with ratios (2% = half of 4%, 8% = double)**; **find the minimum, then look at the answers – only one fits** | solve-pt-q21 (60,000; 8%; 4%-16% → 6%-12%) | SAME (both shortcuts kept; English adds the trap 12%-24%) |
| 5d | שאלה 16 – הפרש היקפים · Q16, difference of perimeters | 102-133 | The long way (Pythagoras twice); **cancel the shared side DE**; AB = DC cancel; a line parallel to AB → two more equal pieces cancel → 2y… (she says the result is "y and y" = 2y; the choice) | solve-pt-q22 (result 2(x − y)) | SAME |
| 5e | שאלה 20 – אחוז ניצחונות · Q20, basketball wins | 135-160 | 20% of 30 = 6 by 10% = 3; 24 losses; from game 31 only wins **until wins = losses** (50% = 50:50) → 24; "Q20 solved in seconds, no calculation" | solve-pt-q23 (30% of 40 → 28) | SAME (English adds the trap 20 = half of 40) |
| 5f | סיכום · Summary | 161-169 | Each question had a different idea; the super-methods cover most; practise insight questions to open your head | solve-pt-q23 slide 2 | SAME |

**Count by row (33 rows):** SAME 22 · CHANGED 9 (1c, 1f, 2c, 2d, 2f, 3c, 3e, 4c, 4d) · PARTIAL 2 (1a, 4b) · MISSING 0.

### Count by video (her 5 lesson videos)

| Her video | Match |
|---|---|
| Seg 1, intro (Q17 roots, Q15 eggs, Q20 algebra, Q20 cylinder, Q20 dice) | CHANGED (the round-answer claim was reversed; the dice question became "at least as large") |
| Seg 2, plugging in the answers | CHANGED (every method kept; "the round answer is usually the right one" is dropped or reversed throughout) |
| Seg 3, plugging in numbers | CHANGED (minor: the pens question pre-empts the failed 1; "logical by the drawing" was reworded) |
| Seg 4, estimation | PARTIAL (the "where is the π" method is missing; her figure-accuracy rule and the eraser are missing and contradicted; √2 ≈ 1.4 / √3 ≈ 1.7 replaced by bounds) |
| Seg 5, insights | SAME |

**By video: SAME 1 · CHANGED 3 · PARTIAL 1 · MISSING 0.**

### A pattern across the topic: the "question N, position, difficulty" openings

Every one of her sample questions opens with its place and level ("שאלה 20, אחרונה בפרק, רמת קושי גבוהה") and often closes with
"look – Q20, solved in seconds". This is the backbone of her thesis (a question harder than its position = there's a shortcut;
plugging in "flattens the exam's difficulty"). The base kept all of them (modulesV51 lines 412-1386). The current scripts keep the idea
only in q06, q09, q11, q23 and the plug-numbers lesson (slide 1), and drop it from q01-q05, q07, q08, q10, q12-q14 and q16-q18.

---

## 2. English → Hebrew (English topic-51 videos and parts with no Hebrew equivalent = added)

| English video / part | Added content | Hebrew source? | Recorded? |
|---|---|---|---|
| pt51-intro slide 4 | 25×4×37÷37 and 999+999+999: "look before you calculate" | none | no |
| solve-pt-q01-2 (whole) | Last digit (23×47), size (√1,849), when to use each | none (her ideas, new examples) | no |
| solve-pt-q02-2 slide 2 | When to plug in the answers; x² + x = 110 | none | no |
| solve-pt-q03-2 slide 3 | When to plug in numbers; 2^(x+1) + 2^x | none | no |
| solve-pt-q04-2 slide 2 (part) | When to estimate; a circle in a square of side 10 | none | no |
| solve-pt-q05 (part) | The "at least as large" twist (ties), the probability definition, the "it's a half" trap | none | no |
| pt51-intro-wrap slide 3 | The signs for each method | none | no |
| pt51-plug-answers slides 1-5 | A full lesson: why it works, two signs, x(x+3) = 40, start from the middle of ordered choices, "fits every given" | only her one-line opening | no |
| solve-pt-q06 (part) | The trap choice −7 (passes one given only) | none | no |
| pt51-plug-numbers 1-4 (most of it, 4 parts) | Why it works ((x+2)² − x(x+4)); restrictions; zero first; zero/one ties with powers; two letters with the same value; a ratio example (½ + ⅓ of a number); **more letters than equations** (4x + 6y = 18); "the value where nothing changes" (boat, k = 0); always-true vs a counterexample; "cannot be determined" / "none of the above" | only her summary list (3 cases + rules) | no |
| solve-pt-q10-q14 (2nd ways) | The algebra after each plug-in | none (she only said "the school way would be…") | no |
| solve-pt-q24 (whole) | xy + 5y = 2x + 10: more letters than equations, the "cannot be determined" trap | none | no |
| pt51-estimation 1-2 (most of it) | 19×51 with choices ×10 apart; benchmark squares; roots between whole numbers; √2 < 1.5 < √3; √90 + √26; 29/59 + 39/81; the signs; the trap when choices are close (29×41 → last digit) | her "close fraction" trick and her summary signs | no |
| solve-pt-q16 slide 0 (part) | The triangle area by Pythagoras and π between 3 and 3.2 (replaces her π pattern) | none | no |
| solve-pt-q17 slide 1 | Bounding the fraction between 1/4 and 1 | none (replaces her 1.4) | no |
| solve-pt-q18 slides 0-1 | Helper line + Pythagoras bounds (replaces her figure estimate) | none | no |
| pt51-insights slides 3-4 | How to look for an insight; 48+73+96 − (46+71+94) | none | no |
| pt51-understanding (whole) | "Understanding" as a method: signs, even/odd, x² vs x on (0,1) | none ("Hebrew lessons don't name it", spec line 3200) | no |
| summary_pages/t51.json | Replaces the pt51-summary video ("six methods" table) | none | — |

---

## 3. Missing from English: restore?

| # | Her content | Where it would go | Target recorded? | Recommendation |
|---|---|---|---|---|
| 1 | **"Where is the π?"**: the shape of the calculation rules out choices before any number (sector − triangle → "π minus a number"; "number − π" and "π / number" are out); "sometimes only one choice has it right, sometimes none" | solve-pt-q16 slide 0, as the first estimation step (about 4-5 sentences). With the English choices it rules out choices 1 (4 − π) and 3 (π/√2) | no | **RESTORE.** It is one of her named methods, it works with the English numbers, and it could replace the triangle calculation and the decimal bound "π < 3.2" (which goes against the *no-decimal-estimates* rule). The old summary script and the base both still say it |
| 2 | **Estimating from the figure**: "not necessarily drawn to scale, but most figures are accurate; regular shapes (square, circle, equilateral triangle, cube) are accurate; check with your eraser"; the middle part is more than a radius and less than a diameter | solve-pt-q18, as the estimation way (about 6 sentences), keeping the Pythagoras bounds as the math way (or her "root of 12 = 2√3" finish) | no | **RESTORE, but she must decide first.** Right now q18 says the opposite ("No, we shouldn't measure the sketch"), and so do pt51-plug-numbers-2 slide 1 and geo-001-4. With the English numbers her estimate gives a middle part between 2 and 4, so AD is between 6 and 8 and the area between 24 and 32 (choice 1). She also promises "a whole lesson later on when figures are accurate": check that it exists in the English course |
| 3 | **"The round answer is usually the right one; NITE builds questions to reward it"** (said 4 times: Q15, Q13, Q18, the seg-2 summary) | solve-pt-q02-2 slide 1, solve-pt-q07 slide 1, solve-pt-q08 slide 3, solve-pt-q09 slide 2, pt51-plug-answers slide 5 (one sentence each) | no | **RESTORE in a soft form** ("very often the round choice turns out to be the right one, but not always, so still check it"). At the moment the English says the opposite. It is her claim, so check it against the real exams first (memory rule *verify-before-adding-content*) |
| 4 | The numbers to know: √2 ≈ 1.4, √3 ≈ 1.7, and plugging 1.4 into the root fraction | solve-pt-q17 slide 1, pt51-estimation slide 3 | no | Optional; she must decide. These are her Hebrew must-knows, and they work with the English numbers (1.4/3.4 ≈ 0.4 = √2 − 1). But her later *no-decimal-estimates* rule is why the English uses bounds. Note that the stale `ai_scripts/pt51-summary.json` still says "root two about 1.4, root three about 1.7", while the summary page says neither |
| 5 | The "question N, position, difficulty" openings and the "Q20, solved in seconds" closings | the first line of each sample question (q01-q05, q07, q08, q10, q12-q14, q16-q18) | no | Optional. One phrase each; they carry her "harder than its position = a shortcut" idea, which the English summary also uses ("when a question looks too hard for its place") |
| 6 | "Go through all these lessons before you start studying the other topics" | pt51-intro slide 7 | no | Optional, one sentence |
| 7 | Q20 pens: plug in 1 first and *see* it fail | solve-pt-q13 slide 0 | no | Not needed: English keeps the lesson (1 can't separate powers and products) and says it before plugging in |
| 8 | Q20 angles: "choose a value that looks logical in the drawing" | solve-pt-q11 slide 0 | no | Not needed: English gives a better reason (the value must fit the angle conditions). Reword only if she wants her phrase back |

**Where English contradicts her:** (a) q18 tells the student not to estimate from the figure, which is her method; (b) q02-2, q07 and q08 say
the round answer isn't more likely to be right, while she says it usually is; (c) q16 uses the decimal bound "π < 3.2", against her
own no-decimal rule (her version only needs π ≈ 3). Nothing is recorded yet, so all of this can be fixed before she reads it on camera.
