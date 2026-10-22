# Topic 19 (Defining a New Operation): the teacher's Hebrew videos vs the English course

Read-only review, 2026-10-22. Nothing in the course was changed.

- Hebrew source: `~/Downloads/01-Algebra-Original-Subtitles.txt`, lines 18765-19910 (source 12; all of it read).
- English: the current reading scripts `studio-build/ai_scripts/<id>.json` (spec `math_patches/_ai_vis_t19.py`), the practice
  list from the course dump, and the answer choices from `~/Downloads/Psychometric-Teacher-Studio-v19-hybrid.html`.
- Recording status (`video_status.py`): **done** = new-operation, solve-q-541 … 548, solve-q-550, solve-q-552 … 555,
  solve-q-r26-t19-01/02/03/05/18. **Re-read pending** = new-operation-2, new-operation-3, solve-q-551, solve-q-556.
  **Not recorded** = operation-patterns, solve-q-549. r26-t19-summary = summary page.

**Match scale.** New numbers alone are not a change. SAME = same idea and all her methods. CHANGED = same idea, method / example
type / order differs. PARTIAL = some of her content or one of her methods is missing. MISSING = no English equivalent.

**Structure and numbering.** Her section: lesson 1 "intro to a new operation" (3 worked examples), lesson 2 "complex new
operations" (6 types, one worked example each), 7 advanced questions, 20 practice questions. English splits lesson 1 into three
camera parts (new-operation, -2, -3) and replaces lesson 2 with a short video (operation-patterns: "each question that follows
shows one type, and teaches it right there", plus a new type, the inverse operation). Each of her 9 lesson examples became its
own solution video (q-541 … q-549, in her order), and her 7 advanced questions are q-550 … q-556. No gaps.

**Her names.** הגדרת פעולה חדשה → "defining a new operation"; the dollar sign → kept as the exam's usual symbol, but the course
uses a **diamond**; פעולה על ביטוי → "an operation on an expression"; תנאים → "a rule with conditions"; פעולה מעגלית → "a rule that
uses itself"; בידוד פעולה → "treat diamond of x like an unknown, a box, and isolate it"; פתרון הברקתי → "by understanding" / "a
shortcut".

---

## 1. Hebrew → English (her videos, in her order)

| # | Her video (Hebrew title · English gloss) | Lines | What she teaches / how she solves it (every method) | English equivalent | Match |
|---|---|---|---|---|---|
| 1a | מה זו פעולה חדשה · What a new operation is | 18767-18824 | New on the exam, but needs only known techniques; the dot for "times", the plus sign, the small 2 (a power), the root: a symbol + a definition, then you can solve | new-operation slides 0-1 | SAME |
| 1b | הפעולה לב · The heart | 18825-18846 | x ♥ y = 2(x + y); 8 ♥ 5 = 26 (what's before / after the heart) | new-operation slide 2 (a ♥ b = 5(a + b); 7 ♥ 3, 2 ♥ 6) | SAME (English adds the trap of multiplying only the first number) |
| 1c | בפסיכומטרי: דולר · On the exam: $ | 18847-18850 | Mostly $, sometimes # or brackets | new-operation slide 3 | SAME (English uses a diamond in its own questions and says so) |
| 1d | $a = a² − a, $4 (example) | 18853-18868 | Put 4 wherever a was, same template → 12 | solve-q-541 (a² − 4a, ◆6) | SAME (English adds a factorise-first method and the "only into a²" trap) |
| 1e | סדר פעולות · Order of operations | 18869-18897 | The new operation comes first, before ×, ÷, powers, except brackets; $a·$b ≠ $(ab) and $a + $b ≠ $(a + b), "think of squares: 3² + 4² isn't 7²; if unsure, ask what you'd do with a square" | new-operation-2 slide 2 | SAME (her square analogy kept word for word) |
| 1f | פעולה בתוך פעולה · Nested, $$3 with $x = x² (example) | 18898-18925 | Inner brackets first, then the outer → 81 | new-operation-2 slide 3 + solve-q-542 (◆◆5) | SAME (English adds the trap "stop after the inner one" and a power method x⁴) |
| 1g | מציאת פעולה · $3 = 24, which can't be the definition (example) | 18926-18979 | The operation could be infinitely many things (8x); test each choice with 3; 10x − 5 gives 25 → the answer; "in the exam mark it and move on, here we check the rest" | new-operation-3 slide 1 + solve-q-543 (◆3 = 21) | SAME |
| 1h | סיכום שיעור 1 · Close | 18980-18987 | Nothing complicated; next lesson the complex types | new-operation-3 slide 4 | SAME |
| 2a | פעולה על ביטוי · $2x = x − 3, $10 (example) | 18998-19016 | 10 takes the place of 2x, not x → x = 5 → 2 | solve-q-544 (◆2x = x + 5, ◆14) | SAME (English adds the trap 19 and a "rewrite the rule for any input" method) |
| 2b | תנאים · Odd / even rule, $$$3 (example) | 19017-19047 | Inside out; check odd / even before each step (3 → 6 → 31 → 62) | solve-q-545 (◆◆◆1) | SAME |
| 2c | פעולה מעגלית · $x = 5 − $(x − 2), $0 = 0 (example) | 19048-19093 | Keep running down until only numbers are left, then back up → 5 | solve-q-546 (◆x = 9 − ◆(x − 2), ◆0 = 2) | SAME (English adds the pattern method 2, 7, 2, 7) |
| 2d | $x = $(x − 1), $1 = 0 (example) | 19095-19114 | Down to $1 → 0 | solve-q-547 (◆1 = 9) | SAME (English adds the trap "1 is the input where it stops, not the value") |
| 2e | בידוד פעולה · 2$x − 5x = 4 + $x (example) | 19115-19151 | "Very rare on the exam"; isolate $x like an unknown → $x = 5x + 4 → 24; then it's a simple question | solve-q-548 (5◆x − 3x = 8 + 4◆x) | SAME (the "box" image added; her "very rare" remark is not said) |
| 2f | מה נכון בהכרח · $x = x², which is not necessarily true (example) | 19152-19245 | **Tip: when the operation appears in every choice, skip it at once and come back at the end** (it can eat a lot of time); algebra on each choice; or plug in x = 1 ("faster, less confusing") | solve-q-549 (◆t = t², not always true) | SAME (the skip-and-return tip is kept, a little softer: "if it looks long, you can leave it for later"; both methods kept; English explains why not x = 0) |
| 2g | סיכום שיעור 2 · Close | 19246-19254 | These are the types the exam can bring | operation-patterns slide 0 | SAME |
| 3 | $(x, y, z) = x^(yz) + …, $($(1,2,3), 0, 1) (Q, easy+) | 19258-19322 | (1) Inner first: 18, then 18⁰ + 0¹⁸ + 1⁰ = 2; (2) **the insight: the 0 in the outer operation makes the inner result irrelevant** (anything⁰ = 1, 0^anything = 0) → 2 without computing the inner one | solve-q-550 (◆(1, 1, ◆(2, 1, 4)) → 35) | CHANGED: the standard method is the same, but in the English question the inner value **is** needed (outer = 2 + z). Her insight survives only as a side example at the end ("◆(z, 0, 1) is 2, whatever z is") |
| 4 | $ ו-# – נוסחאות כפל מקוצר (Q, medium) | 19325-19408 | (1) Three calculations; (2) spot the shortcut formulas: $ = (x − y)², # = (x + y)² → (2² + 1²)… → 25 | solve-q-551 (→ 289) | SAME |
| 5 | √(2x² + y²), $($(a,a), a) / $(a, $(a,a)) (Q, medium+) | 19412-19518 | (1) Full math: inner = a√3, top a√7, bottom a√5 → √(7/5); (2) plug in a = 1 ("one plug-in is enough, the choices are numbers"); **shortcut: once the top is √7, stop — the bottom has the inputs swapped and x is doubled, so it can't be √7 too, and only one choice has √7 on top** | solve-q-552 (√(8x² + y²) → √(73/17)) | PARTIAL: both methods are there, but **her early-stop shortcut is missing**, and the English even says the opposite: "Careful, the top alone doesn't give the answer… we need the bottom too". With the English choices (1, √(17/73), √(73/17), √(9/8)) her shortcut still works: only one choice has 73 on top |
| 6 | (x − y)² / (xy²), $(a,b) / $(b,a) (Q, hard) | 19521-19635 | Three ways: (1) math — **don't open the squared brackets early, they may cancel**; (2) the insight: the tops are equal (opposites squared), so only the bottoms matter; the result must be a/b or b/a with equal exponents → only one choice fits; (3) plug in, but **first check the choices come out different**: 1, 2 makes two equal, so use 2, 1 | solve-q-553 ((x − y)² / (xy³) → a²/b²) | SAME (all three; "don't open the squared brackets yet, they might cancel" and "check the choices are different" kept. English's understanding method derives a²/b² instead of eliminating by "equal exponents") |
| 7 | ABC: A² + B³ + C⁴, הקטן ביותר (Q, easy+) | 19638-19705 | Two topics in one; (1) compute each choice, dropping as you go; (2) insight: the 4th power should go to the smallest digit → the one with 1 in the units | solve-q-554 (A⁴ + B³ + C²) | SAME (both; English also places the cube) |
| 8 | $x = 1/x, נכון בהכרח (Q, hard) | 19708-19813 | For each choice, technical (multiply by positive a, no sign flip) and by understanding (1/x is x⁻¹; bigger denominator → smaller fraction; a number times its reciprocal is 1) | solve-q-555 (◆x = 3/x) | SAME (both methods for every choice) |
| 9 | [x] = כמה פעמים 2 בפירוק (Q, hard) | 19816-19905 | Two topics; understand the definition on the example (20 → 2); plug in x = 1 ("with plug-ins we can't mark a choice that works, we must knock out the others"); then by understanding: ×2 adds exactly one 2; +2 doesn't; squaring doubles the count | solve-q-556 (count of 5s) | SAME |
| 10 | 20 שאלות תרגול עצמי · 20 practice questions | 19910 | — | q-557 … q-576 (20) + alg-extra ×3 + q-r26-t19-07/11/19/20 | SAME (all 20 kept) |

**Count by row (23 rows):** SAME 21 · CHANGED 1 (3) · PARTIAL 1 (5) · MISSING 0.

### Count by video (her units)

| Unit | Match |
|---|---|
| Lesson 1 (1a-1h, incl. 3 examples) | SAME |
| Lesson 2 complex types (2a-2g, incl. 6 examples) | SAME (now taught inside q-544 … q-549) |
| Q3 three-number operation | CHANGED (her "the 0 makes the inner value irrelevant" is only a side example) |
| Q5 √(2x² + y²) | PARTIAL (her early-stop shortcut is missing and contradicted) |
| Q4, Q6, Q7, Q8, Q9 | SAME |
| 20 practice questions | SAME |

**By video: SAME 8 · CHANGED 1 · PARTIAL 1 · MISSING 0** (10 units: 2 lessons, 7 questions, the practice set).

---

## 2. English → Hebrew (added in English)

| English video / part | Added content | Hebrew source? | Recorded? |
|---|---|---|---|
| new-operation-2 slide 1 | Whatever goes in, goes in brackets: ◆(−2), ◆(x + 2) | none | yes (re-read pending) |
| new-operation-2 slide 3 (part) | A nested two-number operation (the star) | none | yes (re-read pending) |
| new-operation-3 slides 2-3 | Order of inputs matters (a ★ b vs b ★ a; don't test with equal numbers); an unknown input → an equation | none | yes (re-read pending) |
| operation-patterns | The inverse operation (undo the steps in reverse order) | none | **no** |
| 2nd methods in q-541, q-542, q-544, q-546 | Factorise first; x⁴; rewrite the rule; the 2, 7, 2, 7 pattern | none | yes |
| solve-q-r26-t19-01 | ◆(x + 1) with ◆x = x² − 2x | none | yes |
| solve-q-r26-t19-02 | Which operations are commutative | none | yes |
| solve-q-r26-t19-03 | Backwards with a conditional rule (◆x = 24, odd or even?) | none | yes |
| solve-q-r26-t19-05 | ◆2 − ◆(−2) for a long polynomial: even powers cancel | none | yes |
| solve-q-r26-t19-18 | ◆◆x = x: which rules undo themselves | none | yes |
| r26-t19-summary | Summary page | none | — |

---

## 3. Missing from English: restore?

| # | Her content | Where it would go | Target recorded? | Recommendation |
|---|---|---|---|---|
| 1 | **Q5 early stop:** "the top is √73; the bottom has the inputs swapped and only the first is multiplied by 8, so it can't be √73 as well; only one choice has 73 on top → stop" | solve-q-552 slide 2, replacing "Careful, the top alone doesn't give the answer…", ~2-3 sentences | yes (done) | **RESTORE.** It is her named shortcut, it works with the English choices, and the current English line tells the student the opposite. Needs one slide re-read |
| 2 | Q3: a question where the 0 really makes the inner calculation unnecessary | solve-q-550: change the outer inputs so one of them is 0 (e.g. ◆(◆(2,1,4), 0, 1) → 2, with 33/35 as traps) | yes (done) | OPTIONAL. The idea is already taught in the closing example of slide 1; making it the main question needs new choices and a re-recording |
| 3 | Isolating the operation is "very rare on the exam" | solve-q-548 | yes | NOT NEEDED (frequency remark only) |
| 4 | Her method verdicts ("plugging in is recommended for the rest", "the insight for strong students") | — | — | NOT NEEDED (R35) |

**RESTORE list:** (1) the Q5 early-stop shortcut in solve-q-552 (recorded; one slide). In that same slide the English currently
contradicts her, so this is also the one place in topic 19 where the English says something against her method.
