# Topic 20 (Algebraic Understanding): the teacher's Hebrew videos vs the English course

Read-only review, 2026-10-22. Nothing in the course was changed.

- Hebrew source: `~/Downloads/01-Algebra-Original-Subtitles.txt`, lines 19912-20230 (source 12; all of it read).
- English: the current reading scripts `studio-build/ai_scripts/<id>.json` (spec `math_patches/_ai_vis_t20.py`), practice list from the course dump.
- Recording status (`video_status.py`): **done** = solve-q-577 … 580, solve-q-r26-t20-01 … 04, r26-t20-counting.
  **Re-read pending** = algebraic-understanding (the camera lesson, read from a script since 2026-10-13). r26-t20-summary = summary page.

**Match scale.** New numbers alone are not a change. SAME = same idea and all her methods. CHANGED = same idea, method / example
type / order differs. PARTIAL = some of her content or one of her methods is missing. MISSING = no English equivalent.

**Structure and numbering.** Her section is one short intro followed straight away by 4 sample questions ("as usual, we'll
start with a sample question"), then 10 practice questions. English keeps the intro as the camera lesson
algebraic-understanding (and adds three short tool demonstrations to it), and her 4 questions are q-577 … q-580. No gaps.

**Her names.** הבנה אלגברית → "algebraic understanding"; שאלת מינימום מקסימום → "find the biggest value b + c can ever have";
הצבת מספרים / הצבת תשובות → "plugging in numbers / plugging in the answers"; הברקה → "an insight".

---

## 1. Hebrew → English (her videos, in her order)

| # | Her video (Hebrew title · English gloss) | Lines | What she teaches / how she solves it (every method) | English equivalent | Match |
|---|---|---|---|---|---|
| 1 | הבנה אלגברית – פתיח · Intro | 19914-19930 | The last algebra topic; questions that belong to no topic or mix topics; solved by algebra, by understanding, or by plugging in numbers / answers; a small part of the exam, the questions don't repeat, no fixed principles, but the lesson and practice give tools | algebraic-understanding slides 0-1 | SAME (almost word for word; English adds slides 2-4, a short demo of each tool and "integers leave gaps") |
| 2 | a>b>c שלמים, a+b<10, מה לא יכול להיות b+c (Q, easy+) | 19932-20048 | Three ways: (1) max/min: a + b ≤ 9 (integers); c is at least 2 below a → b + c ≤ 7 → 8 is impossible; (2) plug in numbers that make b + c largest (5, 4, then c = 3); (3) plug in the answers one by one (1, −1, 8, −8 with example triples) | solve-q-577 (a + b < 16 → b + c ≤ 13, 14 impossible) | SAME (all three ways; English starts the answer-test from the biggest choice because "the question hides a biggest value") |
| 3 | x² = a³, a פי 4 → x פי כמה (Q, hard) | 20051-20105 | Start with plugging in this time: the easy pair 1, 1 (or put a = 1 and use "x is positive"), then a = 4 → x² = 64 → 8; (2) math: multiply x by k, (kx)² = (4a)³ → k² = 64 → 8; "strong students see it in their head: ×4 on the right is ×64, so ×8" | solve-q-578 (y² = b³, b × 25 → y × 125) | SAME (the same order, plug-in first, then the k method; English also shows "25³ is a square" mentally) |
| 4 | c²/ab = a/b + b/a, בהכרח אינה נכונה (Q, hard) | 20108-20166 | Common denominator → c² = a² + b²; **the insight linking algebra to geometry: Pythagoras**, a right triangle with legs a, b and hypotenuse c; a + b > c (triangle inequality), b < c (leg < hypotenuse); "c < 5" is **necessarily false**: the integers form a Pythagorean triple, and the smallest one, 3-4-5, already has c = 5 (next 6-8-10, 5-12-13); 2a = b + c is possible (4: 8 = 3 + 5) | solve-q-579 (r²/pq = p/q + q/p, which is **not necessarily true** → r < 8) | CHANGED: the simplification and the right-triangle insight (leg < hypotenuse, two sides > the third) are kept. But the question asks "not necessarily true" instead of "necessarily not true", so the answer comes from a counterexample (double 3-4-5 to 6-8-10, r = 10). **Her argument "3-4-5 is the smallest whole-number triple, so the hypotenuse can never be below 5" is no longer used** (it only appears in the summary page as "the smallest whole numbers that fit are three, four and five") |
| 5 | הצלחה לימודית Q, W, L (Q, medium+) | 20170-20226 | Grows with Q and W, shrinks with L; check each expression: a fraction grows with its top and shrinks with its bottom; Q^W grows with W because Q > 1; −L fits; the one where a bigger L makes it bigger is out | solve-q-580 (game score: C, S up, M down) | SAME (the same reasoning, incl. "C to the power of S grows with S because C > 1") |
| 6 | 10 שאלות תרגול עצמי · 10 practice questions | 20230 | — | q-581 … q-590 (10) + alg-extra ×3 + q-r26-t20-11/12 | SAME (all 10 kept) |

**Count by row (6 rows):** SAME 5 · CHANGED 1 (4) · PARTIAL 0 · MISSING 0.

**By video: SAME 5 · CHANGED 1 · PARTIAL 0 · MISSING 0** (6 units: the intro, 4 questions, the practice set — the same as the rows).

---

## 2. English → Hebrew (added in English)

| English video / part | Added content | Hebrew source? | Recorded? |
|---|---|---|---|
| algebraic-understanding slides 2-4 | Demonstrations of the three tools: a² vs a for a = 3 and a = 1/3; x² − x = 6 by the answers; a² − b² from a + b and a − b; "an integer below 5 is at most 4" | her intro names the tools | yes (re-read pending) |
| solve-q-r26-t20-01 | x > y > 0, which must be true: try a number from each region (above 1, between 0 and 1); the factorised proof | none | yes |
| solve-q-r26-t20-02 | −1 < x < 0, the smallest of x³, x, −x², 1/x | none (related to topic 17) | yes |
| r26-t20-counting | Counting integers in a range (both ends in / out / one in); the pigeonhole principle (with remainders) | none | yes |
| solve-q-r26-t20-03 | Odd numbers between 20 and 80 (steps vs numbers trap) | none | yes |
| solve-q-r26-t20-04 | Socks: the worst-luck argument / pigeonhole | none | yes |
| r26-t20-summary | Summary page | none | — |

---

## 3. Missing from English: restore?

| # | Her content | Where it would go | Target recorded? | Recommendation |
|---|---|---|---|---|
| 1 | Q4: "the numbers are a whole-number Pythagorean triple, and the smallest one is 3-4-5, so the hypotenuse is at least 5" | solve-q-579 slide 2, one sentence after "nothing in the triangle limits how long r is" ("…but it can't be short either: the smallest whole-number triple is three, four and five, so r is at least five") | yes (done) | OPTIONAL. It is her key "integers → Pythagorean triple" idea and costs one sentence, but the English question no longer needs it, and the summary page already states the 3-4-5 fact |
| 2 | Her verdicts ("all three ways are excellent", "plugging in is recommended for most students") | — | — | NOT NEEDED (R35) |

**RESTORE list: none required** (one OPTIONAL sentence in solve-q-579). Every other method she gives in topic 20 is in the
English and works with the English numbers. Nothing in the English contradicts her.
