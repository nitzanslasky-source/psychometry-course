# Topic 18 (Exercises with Letters): the teacher's Hebrew videos vs the English course

Read-only review, 2026-10-22. Nothing in the course was changed.

- Hebrew source: `~/Downloads/01-Algebra-Original-Subtitles.txt`, lines 18204-18762 (source 12; all of it read).
- English: the current reading scripts `studio-build/ai_scripts/<id>.json` (spec `math_patches/_ai_vis_t18.py`), practice list from the course dump.
- Recording status (`video_status.py`): **done** = digit-puzzles, digit-puzzles-2, solve-q-512 … 519, r26-t18-facts,
  solve-q-r26-t18-01, solve-q-r26-t18-03. **Re-read pending** = solve-q-520. **Recorded, waiting to be sent** =
  solve-q-r26-t18-02. r26-t18-summary = summary page. The whole topic is recorded.

**Match scale.** New numbers alone are not a change. SAME = same idea and all her methods. CHANGED = same idea, method / example
type / order differs. PARTIAL = some of her content or one of her methods is missing. MISSING = no English equivalent.

**Structure and numbering.** Her section: one theory lesson with three worked examples, then 6 advanced questions, then 20
practice questions. English splits the lesson into two camera parts (digit-puzzles, digit-puzzles-2) and gives each of her
three in-lesson examples its own solution video (q-512, q-513, q-514); her 6 advanced questions are q-515 … q-520. No gaps.
Several of her lesson facts (the "1 on the left" rule, the special digits, subtraction → addition) were moved from the lesson
into the solution video that first needs them (q-512, q-513, q-516).

**Her names.** תרגילים באותיות → "exercises with letters / letter puzzles"; כתיבה במאונך → "write it vertically"; ספרת האחדות /
הספרה השמאלית → "the ones column / the leftmost digit"; ספרות מיוחדות → "the special digits 0, 1, 5, 6"; הצגה אלגברית → "write the
number with its place values (10A + B)"; הערכת סדר גודל → "checking the square's size first".

---

## 1. Hebrew → English (her videos, in her order)

| # | Her video (Hebrew title · English gloss) | Lines | What she teaches / how she solves it (every method) | English equivalent | Match |
|---|---|---|---|---|---|
| 1a | פתיח · Intro | 18206-18213 | Calculations in letters instead of digits; like the weekend-paper puzzles, only much smaller | digit-puzzles slide 0 | SAME |
| 1b | הטכניקה ב-4 שלבים · The four steps | 18214-18219 | (1) write vertically, (2) ones digit, (3) leftmost digit, (4) plug in numbers | digit-puzzles-2 slide 1 | SAME (English adds "use the steps that help, not every step every time" and its own warm-up A4 + 3B = 71) |
| 1c | אותיות = ספרות · Letters are digits | 18222-18236 | AB is a number (23), not A × B; "a number written in another language"; different digits only if stated (22, 33 otherwise); most exam questions say "different" | digit-puzzles slides 1-2 | SAME (the "another language" image kept) |
| 1d | AB + AD = CDB (example) | 18237-18265 | Vertically; ones: B + D = B → D is 0; left: A + A = CD = 10 → A = 5, C = 1 → 6 | solve-q-512 (BA + DA = CCA) | SAME |
| 1e | ספרה שמאלית אינה 0 · The leftmost digit is never 0 | 18266-18272 | "I don't call a number 08, it's not an area code" | digit-puzzles slide 2 ("zero eight has the value eight") | SAME |
| 1f | ספרה שמאלית חדשה = 1 · A new leftmost digit is 1 | 18273-18304 | If the sum has more digits than the numbers added, the new left digit is 1 (A + A ≤ 18; 99 + 99 = 198) | solve-q-512 slide 1 | SAME (English adds "this rule is for adding two numbers, not three or four") |
| 1g | ספרות מיוחדות · Special digits | 18305-18334 | 0, 1, 5, 6 keep their last digit when squared; 5 × even ends in 0, × odd in 5; 6 × even keeps that digit; "saves plug-ins" | solve-q-513 slide 0 | SAME (moved into the question) |
| 1h | BA × A = CA (example) | 18337-18351 | A × A ends in A → special digit; of the choices 0 or 5; not 0 (it would give 0) → 5 | solve-q-513 (CB × B = ACB) | SAME (English also checks 25 × 5 = 125) |
| 1i | הצבת מספרים – "מחשב היה מריץ הכל" · Plugging in is the real method | 18352-18361 | Every letter puzzle is solved by plugging in; a computer would try everything; the steps are shortcuts that tell us what not to try | digit-puzzles-2 slide 1 | SAME (almost word for word) |
| 1j | AB − BA מתחלק בהכרח ב- (example) | 18364-18385 | No result given → no shortcuts, just plug in: 51 − 15 = 36 (11 out), then the next number 52 − 25 = 27 (6, 4 out) → 9; the pattern "AB − BA always ÷ 9, AB + BA always ÷ 11" | solve-q-514 (AB + BA, necessarily divides → 11) | CHANGED: the question is now the sum version (71 + 17 = 88, then 72 + 27 = 99 → 11). Her plug-in method and both patterns are kept; "AB − BA = 9(A − B)" is now a remark at the end (and the 3-digit version ×99 is added in r26-t18-02) |
| 1k | טיפ: חיסור → חיבור · Turn subtraction into addition | 18386-18399 | AA − BB = BB → BB + BB = AA: now B can only be 1-4 (55 + 55 > 100) | solve-q-516 slide 0 (the same AA − BB = BB example) | SAME |
| 1l | הצגה אלגברית · Place values | 18400-18437 | 27 = 10·2 + 7, 538 = 5·100 + 3·10 + 8; AB = 10A + B, ABC = 100A + 10B + C; AB − BA = 9(A − B); "strong students like it, I recommend plugging in, much faster" | digit-puzzles slide 3 + solve-q-514 slide 1 | SAME ("usually plugging in two numbers is faster, but this form is what we need when a puzzle comes in words") |
| 1m | סיכום · Close | 18438-18450 | Recap: vertical, ones, leftmost, plug in; plugging in works in almost every topic | digit-puzzles-2 slide 1, r26-t18-summary | SAME |
| 2 | ABC − AB = CC, מה C (Q, easy+) | 18454-18506 | Vertically; **subtraction → addition** (CC + AB = ABC); new left digit → A = 1; ones: C + B = C → B = 0; then either "two-digit + 10 gives 100-something only for 99 → C = 9" or the carry reasoning (no carry from the ones, so C + 1 = 10) | solve-q-515 (BCA + BC = AAA, C = ?) | CHANGED: a different, simpler puzzle (an addition, where the left-digit rule explicitly does **not** apply, and the answer comes from the ones column, C = 0). Her tools for this question are taught elsewhere: subtraction → addition and the new-left-digit rule in q-516, the carry-into-a-column "the added digit is 9" idea in r26-t18-01. Her size shortcut "only 99 + 10 reaches a three-digit number" is not used |
| 3 | AAA-type, B + C עם תשובות באותיות (Q, easy+) | 18509-18534 | Vertically; subtraction → addition; two two-digit numbers give 111 → A = 1; column-by-column works "but it's really unnecessary": 111 − 55 = 56, just subtract; the answer is written as AA = 11 | solve-q-516 (AAA − 46 = BC) | SAME (her "don't go column by column, just subtract" kept, and the AA = 11 answer form) |
| 4 | AB × AB = 2CB (Q, medium+) | 18537-18597 | (1) Estimate the size: 15² … 17² are 200-something, 20² = 400 → A = 1 ("an important tool"); ones B·B ends in B → special digit, 0 and 1 too small → 5 or 6; 15² gives 4, not offered → 16 → 5; (2) "the brilliant way": special digits + the choices (B − A is 5 to 8) and A ≠ 0 → B = 6 without calculating | solve-q-517 (CA × CA = 6BA) | SAME (both methods: the size estimate, and starting from the special digits with the choices and "C is a leading digit, not zero") |
| 5 | CBA / AA = 15 (Q, medium+) | 18600-18636 | Division → multiplication (AA × 15 = CBA); ones: 5 × A ends in A → 0 or 5; A ≠ 0 (leading digit) → 55; 15 × 55 = 550 + half of it (275) = 825 → 15 | solve-q-518 (CBA / AA = 17) | SAME (division → multiplication, the ones column, A ≠ 0, and splitting the multiplication 10 × 55 + 7 × 55) |
| 6 | AC + CB = DA, ספרות ראשוניות (Q, hard) | 18639-18690 | Inventory: prime digits 2, 3, 5, 7, four letters → all four used; trial and error with the answers (A = 5 works: 52 + 23 = 75), then rule out 2, 3, 7 | solve-q-519 (AB + BC = CD, C = ?) | SAME (inventory, "all four digits are used", testing the choices; English first rules out 2 and 3 by the smallest possible sum) |
| 7 | x = (ספרת העשרות)³ + סכום ספרותיו (Q, hard) | 18693-18758 | (1) Algebra: 10A + B = A³ + A + B → 9A = A³ → A = 3; (2) plug in the answers: 5³ is already too big, 2 gives a "1B" number, 3 gives 30 + B for every B | solve-q-520 (x = units³ + 4·digit sum) | SAME (both methods; the English version needs a short search over U, which it explains) |
| 8 | 20 שאלות תרגול עצמי · 20 practice questions | 18762 | — | q-521 … q-540 (20) + alg-extra ×3 + q-r26-t18-04/07 | SAME (all 20 kept) |

**Count by row (20 rows):** SAME 18 · CHANGED 2 (1j, 2) · PARTIAL 0 · MISSING 0.

### Count by video (her units)

| Unit | Match |
|---|---|
| Lesson (1a-1m, incl. 3 examples) | CHANGED (only example 3 was mirrored, AB − BA → AB + BA; nothing is missing) |
| Q ABC − AB = CC | CHANGED (a different puzzle; her tools appear in other videos) |
| Q B + C, Q AB², Q CBA / AA, Q primes, Q tens³ + digit sum | SAME |
| 20 practice questions | SAME |

**By video: SAME 6 · CHANGED 2 · PARTIAL 0 · MISSING 0** (8 units: the lesson, 6 questions, the practice set).

---

## 2. English → Hebrew (added in English)

| English video / part | Added content | Hebrew source? | Recorded? |
|---|---|---|---|
| digit-puzzles slide 2 (part) | The same letter is always the same digit (AA can't be 37) | implicit in hers | yes |
| digit-puzzles-2 slides 2-4 | Warm-up A4 + 3B = 71; puzzles in words ("four / seven times its digit sum") | her Q7 type | yes |
| r26-t18-facts | AA = 11A, AAA = 111A = 3·37·A, BBBB / BB = 101; largest / smallest number with a given digit sum | none | yes |
| solve-q-r26-t18-01 | 2A6 + B8 = 3A4: a carry into the column means the added digit is 9, not 0 | the idea is in her Q ABC − AB = CC | yes |
| solve-q-r26-t18-02 | ABC − CBA = 99(A − C) | her AB − BA = 9(A − B) | yes (to be sent) |
| solve-q-r26-t18-03 | A3 × B7: last digit and size bounds | none | yes |
| r26-t18-summary | Summary page | none | — |

---

## 3. Missing from English: restore?

| # | Her content | Where it would go | Target recorded? | Recommendation |
|---|---|---|---|---|
| 1 | Her advanced Q1 as a puzzle where several of her tools meet (subtraction → addition, new left digit = 1, the ones column gives 0, then "only 99 + 10 gives a three-digit sum") | solve-q-515 would need a new question | yes (done) | NOT NEEDED. Every tool is taught in another English video; q-515 deliberately shows the case where the left-digit rule does *not* apply |
| 2 | AB − BA as the main example (rather than AB + BA) | solve-q-514 | yes (done) | NOT NEEDED. Both patterns are stated, and the 3-digit reversal (×99) is added |

**RESTORE list: none.** Every method, shortcut and warning she gives in topic 18 is in the English and works with the English
numbers. Nothing in the English contradicts her.
