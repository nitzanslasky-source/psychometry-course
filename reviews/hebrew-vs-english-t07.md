# Topic 7 (Equations): the teacher's Hebrew videos vs the English course

Read-only review, 2026-10-22. Nothing in the course was changed.

- Hebrew source: `~/Downloads/01-Algebra-Original-Subtitles.txt`, lines 3895-4790: her "משוואות תאוריה" block
  (3895-4139), "משוואות לימוד מתקדם א" (4140-4459) and "לימוד מתקדם ב" (source 7, 4464-4790). All of it read. Line
  numbers below are file lines.
- **Boundary.** The "תאוריה" block belongs here, not to topic 6: its seven questions are `q-191` … `q-197`, which the
  English puts in topic 7 (both in the base translation and in the current flow). Topic 6 ends at line 3893.
- English: topics 1-12 have no reading scripts yet, so the English side is `scratchpad/ext/course/t07.txt` and `q07.txt`
  (51 questions), the base translation `base-v18.html`, and the current flow in
  `~/Downloads/Psychometric-Teacher-Studio-v19-hybrid.html`.
- **Recording status.** Topic 7 is not in `video_status.py` (it covers only the Reading Studio topics). Her older English
  takes exist for `equation-strategy` and all twenty of her questions `solve-q-178` … `solve-q-197` (in
  `real_exam/added_by_nitzan.json`). `r26-t07-more-tools`, its three solution videos and the summary have none. Topics
  1-12 are redone LAST in the plan, so any restore goes into the redo scripts.

**Her structure.** Theory: a short intro (dividing by an unknown), then seven questions, each with a video; between the
questions she gives one-line intros to the next technique (product = 0, even root, one equation with two unknowns,
computing an expression, the hidden formula, breaking an equation apart). Advanced A: 7 questions. Advanced B: 6
questions. English ids: theory = `q-191` … `q-197`; advanced A = `q-184` … `q-190`; advanced B = `q-178` … `q-183`; no gaps.
The English flow swaps two pairs (197 before 196; 187 before 186); nothing depends on her order.

**Good change in the current English.** The base `equation-strategy` had eight slides that pre-taught every technique;
the current one keeps only her opening (dividing by an unknown) and teaches each technique in the question that uses it,
exactly as she does.

SAME = same idea and every one of her methods (new numbers only). CHANGED = same idea, different method / example /
place. PARTIAL = part of her content missing. MISSING = no English equivalent.

---

## 1. Hebrew → English (her videos, in her order)

### Theory (תאוריה)

| # | Her video (Hebrew · English gloss) | Lines | What she teaches / how she solves it (every method) | English equivalent | Match |
|---|---|---|---|---|---|
| T0 | צמצום בנעלם · Dividing by an unknown | 3897-3908 | You may divide both sides by x (same operation on both sides) only if x ≠ 0; dividing by 0 is undefined | `equation-strategy` slides 1-2 | SAME |
| T1 | x³ = x²y, y = ? | 3910-3943 | "At a glance y = x"; test x = 2 → y = 2; test **x = 0 → any y works**; the mistake was dividing by x²; **then the rule for degree 2 and up: take out a common factor → a product equal to 0 → at least one factor is 0** | `solve-q-191` (m⁵ = m⁴n), Methods 1-2 | SAME |
| T2 | x⁴ − 4x² = 0: number of solutions | 3945-3970 | They ask how many values; factor x²(x² − 4); x² = 0 → 0; x² = 4 → ±2; three solutions. Then the intro: an even root gives two solutions | `solve-q-192` (x⁴ − 25x² = 0) | SAME (English adds the trap "divide by x² → two") |
| T3 | (x − 7)² = 25 | 3972-3994 | Root both sides: ±5; **"on the exam √25 alone means only 5; inside an equation it's plus or minus"**; x = 12 or 2 → two solutions. Then the intro: one equation, two unknowns → no values, but relations (who is bigger, how many times) | `solve-q-193` ((x + 4)² = 81) | SAME |
| T4 | (a − 3b)/2 = 1 − b: what must be true | 3996-4010 | Multiply both sides by 2, move terms: a = 2 + b, so a is bigger than b by 2 → a > b | `solve-q-194` ((a − 6b)/5 = 1 − b) | SAME (English adds the trap a = 5b) |
| T5 | חישוב ביטוי · Computing an expression: 2x + 4y = 17, 5x + 3y = 11, x + y = ? | 4012-4057 | **Don't find each unknown; compute the requested expression directly** (add, subtract, divide equations); don't eliminate a letter here — keep both; add → 7x + 7y = 28 → 4; **"How did I know to add? Nothing to know — rare questions, a matter of practice: look for the same coefficient so you can take it out."** Then the intro to the hidden-formula type ("rare, but be aware") | `solve-q-195` (4x + 9y = 30, 9x + 4y = 35), slides 1-2 | SAME (her "how did I know" kept as a slide; English adds the subtract trap x − y) |
| T6 | x − y = 4, x² + y² = 106, xy = ? | 4060-4102 | You could isolate and solve a quadratic (minutes); instead **find the hidden formula** (x − y)²; **write −2xy LAST so x² + y² stays together as given**; 16 = 106 − 2xy → 45; then the intro "breaking an equation apart" | `solve-q-196` (x − y = 7, x² + y² = 85) | SAME (her "write 2xy last" kept; English adds a check 9 and 2 and two traps) |
| T7 | 2a + 3b + 3c = 22, a + b = 2, 2b + c = 1, a + c = 12; c = ? | 4105-4137 | Solving each letter takes forever; **break the big equation apart** (a + a, b + b + b, c + c + c) and substitute the small equations one by one → 15 + c = 22 → c = 7 | `solve-q-197` (3a + 2b + 3c = 24…) | SAME (English adds the trap 19) |

### Advanced A (לימוד מתקדם א)

| # | Her video | Lines | What she teaches / how she solves it | English equivalent | Match |
|---|---|---|---|---|---|
| A1 | 39 − (3/7)x = 0.5x | 4142-4205 | **Way 1, common denominator 14, but leave 39 × 14 uncalculated ("on the psychometric it will probably cancel")** → 13x = 39 × 14 → 42. **Way 2, add the fractions first** → (13/14)x = 39: **estimate** — x is a little more than 39; 18 and 30 are too small, 54 too big → 42; or finish exactly (÷ 13/14) | `solve-q-184` (33 − (2/3)x = (1/4)x → 36), Methods 1-2 | SAME |
| A2 | x³ + πx² = x²? (x ≠ 0) | 4207-4232 | Standard: factor x², x ≠ 0 multiplies both sides → cancel → x = 1 − π; **shorter: divide every term by x² right away** | `solve-q-185` (x³ + 3x² = πx²), Methods 1-2 | SAME |
| A3 | x/y = z/w: which is NOT necessarily true | 4234-4313 | **Way 1: clear the denominators** in the given and in each choice and compare ("on the exam, after eliminating three, mark the fourth; in the lesson we check it"). **Way 2: two tools — "ערך משולש" (the triangle value: multiply the diagonal, divide by the one left) to isolate a letter, and "חילופי איברים" (only diagonal terms may swap: 1/2 = 3/6 → 6/2 = 3/1, and 1/3 = 2/6)** | `solve-q-186` (p/q = r/s), Methods 1-2 | SAME (both tools kept; English doesn't use her name "the triangle value" here, although topic 23 uses that name for the same move) |
| A4 | The sum of the squares of two integers = the square of their sum | 4314-4336 | The hard part is translating words to algebra; x² + y² = (x + y)² → 0 = 2xy → a product is 0 only if a factor is 0 → x or y is 0 | `solve-q-187` (square of the difference = sum of squares) | SAME |
| A5 | Three equations, three unknowns; x = ? | 4337-4364 | **"Psychometric equations"** (3+ equations or unknowns) have a shortcut; **the clues: what they ask and which letters vanish from the choices; most are solved by adding, subtracting, or both**; add 1 and 2 → y cancels; subtract the third → x = 6. "Find the shortcut, don't work hard" | `solve-q-188` | SAME |
| A6 | Mixed-number coefficients, = 2a and = 2b; x + y = ? (hard) | 4366-4410 | Think before calculating; **the principle: you need equal coefficients** (x + 2y = 5 can't give the sum; 2x + 2y = 5 → 2.5, though x and y are unknown); **clue in the choices: they all add a and b → add**; 6x + 6y = 2a + 2b → (a + b)/3; "a last-or-second-to-last question; solving each would burn time" | `solve-q-189` (→ (a + b)/4) | SAME |
| A7 | a + b + c = x, a + 2b + 4c = z; 3a + 2b = ? | 4411-4457 | **Math: clues** (asked a, b; choices have x, z; c vanished) → eliminate c: first ×4 minus the second → 4x − z. **Plug in a = b = c = 1** → x = 3, z = 7, target 5; eliminate the negative choices without calculating | `solve-q-190` (3a + 2b + 4c = z; a + 2b = ?), Methods 1-2 | SAME (English adds "ones are usually risky; here the choices still differ") |

### Advanced B (לימוד מתקדם ב)

| # | Her video | Lines | What she teaches / how she solves it | English equivalent | Match |
|---|---|---|---|---|---|
| B1 | Difference of two integers 3, difference of squares 51; sum? | 4466-4521 | **Math**: translate; difference of squares; 3 · sum = 51 → 17. **Plug in from your head**: pairs 3 apart, **start at 8 and 5, because 7² = 49 is already too small — one square must be bigger than 51**; 39, 45, then 10 and 7 → 51. **Plug in from the choices**: sum 19 → (19 − 3)/2 → 8 and 11 → no; 17 → 7 and 10 → yes. "Personally I'd choose the math, but plugging in is excellent too" | `solve-q-178` (difference 5, squares 65 → 13), Methods 1-3 | PARTIAL: English Method 2 starts at 6 and 1 and climbs four pairs ("each step adds ten"); her rule for where to start (the bigger square must already be above the target) is missing. With the English numbers her rule lands on the answer at once: 8² = 64 < 65, so start at 9 and 4 → 81 − 16 = 65 |
| B2 | x/y = 3, y/z = 5, z/w = 4; x/w = ? | 4522-4587 | Four ways: **math** (x = 3y = 15z = 60w); **plug in w = 1 and work back**; **brainwave 1: multiply the equations** (y and z cancel); **brainwave 2: all ratios > 1, so x/w > 1; only one choice is above 1**; "all excellent" | `solve-q-179` (3, 4, 2 → 24), Methods 1-3 | SAME |
| B3 | ab = 1; a/b = ? (choices in a) | 4588-4637 | One equation, two unknowns: express b by a (the choices use a) → b = 1/a; a ÷ (1/a), done with her arcs method → a². **Plug in: not 1 and 1 (every choice gives 1)**; 2 and ½; check the choices differ; 4. Math is short and preferred | `solve-q-180` (pq = 1, q/p = 1/p²), Methods 1-2 | SAME (English divides by multiplying by the reciprocal instead of her arcs; that matches her own advice in topic 2 to avoid the arcs method) |
| B4 | 3x = 2y + 1; 4.5x² − 2y² = ? (hard) | 4638-4699 | The choices mix x and y, so you can't tell which letter to isolate; **clue in what they ask: squares → square the equation**; **trap: (2y + 1)² is not 4y² + 1**; 9x² − 4y² = 4y + 1 → halve → 2y + ½. **Plug in** y = 1 → x = 1, choices differ, 2.5; plug-in recommended for most | `solve-q-181` (2x = y + 3), Methods 1-2 | SAME |
| B5 | For all x, y: (ax + by)² = x² + y² − 2xy; \|a − b\| = ? | 4700-4763 | **Match coefficients**: a² = 1, b² = 1, 2ab = −2 → opposite signs → \|a − b\| = 2. **Shortcut: the right side is (x − y)²**; but the full method matters because some coefficient questions hide nuances | `solve-q-182` (= 9x² + y² − 6xy → 4), Methods 1-2 | SAME |
| B6 | a² + b² = 0.5b²; a = ? (hard) | 4764-4788 | ×2 → 2a² + b² = 0; looks like "can't be known", but a square is never negative and CAN be 0 → both are 0 → a = 0; "an understanding question, not a technical one"; last equations question | `solve-q-183` (a² + 2b² = ¼a² → b = 0) | SAME (English adds why "cannot be determined" is wrong) |

**Counts (21 items: T0-T7, A1-A7, B1-B6):** SAME 20 · CHANGED 0 · PARTIAL 1 (B1) · MISSING 0.

---

## 2. English → Hebrew (English topic-7 videos and parts with no Hebrew equivalent = added)

| English video / part | Added content | Hebrew source? | Her take? |
|---|---|---|---|
| Traps lines in most solutions (e.g. q-192 "divide by x² → two", q-196 "39 / 36", q-197 "19") | One wrong-answer explanation per question | none | mostly yes (the base had many) |
| `solve-q-178` Method 2 (as written) | Climbing pairs from 6 and 1 | her plug-in, see B1 | yes |
| `solve-q-183` (part) | Why "cannot be determined" is wrong | none | not checked |
| `r26-t07-more-tools` | Multiply / divide equations; x + 1/x | her B2 brainwave 1 (multiplying) and the topic-4 formulas | no |
| `solve-q-r26-t07-01` | Divide two product equations → x/y | her B2 idea | no |
| `solve-q-r26-t07-02` | x + 1/x = 6 → x² + 1/x² = 34 | none here (topic 4 has it) | no |
| `solve-q-r26-t07-05` | Two equal squares: equal or opposite | none | no |
| `r26-t07-summary` | Summary (replaced by the printable summary page) | none | — |

---

## 3. Missing from English: restore?

| # | Her content | Where it would go | Target recorded? | Recommendation |
|---|---|---|---|---|
| 1 | **B1: where to start the plug-in** ("the bigger square must already pass the target, so 7 and 4 are too small; start at 8 and 5") | `solve-q-178` Method 2, replacing the climb from 6 and 1: "Sixty-five is the gap, so the bigger square must be more than sixty-five. Eight squared is sixty-four, too small. Start at nine: nine and four. Eighty-one minus sixteen, sixty-five." (3 sentences, and it shortens the video) | her old take exists; topic in the 1-12 redo | **Restore.** It is her own reasoning, it still works with the English numbers, and it turns four tries into one |
| 2 | A3: her name "ערך משולש" → "the triangle value" | `solve-q-186` Method 2, tool one: "This is called the triangle value: multiply the diagonal, divide by the one left" (1 sentence) | same | **Optional.** Topic 23 (percentages, later in the study plan) uses "the triangle value" for the same move; naming it here first links the two |
| 3 | The one-line intros between her theory questions | — | — | Not needed: each English question opens with its own intro, which is the same content |

Nothing in topic 7 is wrong compared with her. Every one of her named methods and tips is kept, including "x = 0 breaks
the cancelling", "√25 alone is 5, but solving takes ±", "leave 39 × 14 uncalculated", "the clues are what they ask and
what vanishes from the choices", "think before you calculate", "write 2xy last", "all ratios above 1", "square both sides
and square the WHOLE right side", "the full coefficient method matters", and "a square can be zero".
