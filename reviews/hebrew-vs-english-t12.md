# Topic 12 (Inequalities): the teacher's Hebrew videos vs the English course

Read-only review, 2026-10-22. Nothing in the course was changed.

- Hebrew source: `~/Downloads/01-Algebra-Original-Subtitles.txt`, lines 8730-11078 (all of it read). Her structure: lesson 1
  "אי שוויונים" with 2 worked examples; lesson 2 "מערכת אי שוויונים", where she teaches each new type between worked examples
  (6 examples); then "אי שוויונות" advanced practice with 8 example questions, then 20 self-practice questions (11076).
- **Her 8th advanced question has no transcript**: lines 10976-11075 are an exact copy of the 7th (10876-10975, the min-max
  product question). So solve-q-337 cannot be checked against her.
- English: `scratchpad/ext/course/t12.txt` / `q12.txt`, base translation `base-v18.html`.
- Recording status: `video_status.py` does not track topics 1-12. **Every topic-12 video has an older camera take** (7-8 Oct 2026,
  `~/Documents/Course.recordings/1 Algebra/Topic 12 …`: inequalities (2 takes), inequality-systems, solve-q-322…337,
  r26-t12-signs, r26-t12-combining, solve-q-r26-t12-01…04 and -13). Topics 1-12 are redone last (first lesson on camera, the
  rest AI), so any restore goes into that redo.

**Match scale** as in the t23 model; new numbers alone are not a change.

---

## 1. Hebrew → English (her videos, in her order)

| # | Her video (Hebrew · English gloss) | Lines | What she teaches / every method | English equivalent | Match |
|---|---|---|---|---|---|
| 1 | אי שוויונים · Inequalities (lesson 1) | 8732-8909 | Like an equation, but the sides need not be equal; four signs (x ≤ 5: 5, 4, 4.5, 3, −7); **on the exam the sign is written like the number line, smaller on the left**; same operations as an equation; ×/÷ by a negative flips (−10 < −6, ÷(−2) → 5 > 3); **her tip: on the exam don't multiply by a minus, move the terms instead** (6 < 10 → 3 < 5) so the sign keeps its side; "both ways are mathematically correct" | `inequalities` slides 1-5 (−18 < −3; −2x < 6) | SAME (English adds "keep the sign on every line" and the same tip shown with x) |
| 2 | 5 + x < 13 + 3x (example) | 8910-8973 | **Move x to where it stays positive (where there are more x's)** → 2x > −8 → x > −4; the other way you get −x, divide by a minus and flip, "just complicating it" | solve-q-322 slide 1 (4 + x < 18 + 3x) | SAME (English adds Method 2 "two moves": endpoint + a test number) |
| 3 | 4(3 − 2x) − 5 < 9 − 8x (example) + lesson close | 8974-9037 | x cancels → 7 < 9, always true → every x, "like the equation with infinitely many solutions"; close: same moves as an equation, beware the minus, move x to its positive side | solve-q-323 | SAME (English adds the false case → no x) |
| 4 | מערכת אי שוויונים · Systems (lesson 2 intro) | 9038-9101 | Some are easy, some "can drive you a bit crazy"; double inequality or two inequalities: solve each separately, then the common range | `inequality-systems` | SAME |
| 5 | 3x − 8 < 2x + 3 < 5x − 12 (example) + "no solution" idea | 9102-9240 | **First: the right side is surely bigger than the left**; split; x to the side with more x's; x < 11, x > 5 → overlap on the number line, 5 < x < 11. Then: an inequality with no solution, the empty set ∅ ("you'll rarely meet the symbol") | solve-q-324 (3x − 4 < 2x + 5 < 4x − 5) + solve-q-325 | SAME (every step, including "the right expression is bigger than the left one". English adds plugging in the answers in the written solution) |
| 6 | 2x + 36 < 15 + 5x < 35 (example) + trial-and-error intro | 9241-9358 | x > 7 and x < 4: **"it's not OR — it must be both"**; no overlap → empty set. Then: **trial-and-error questions are very common in inequalities, often FIRST in the section; they look easy, are hard by algebra, simple by plugging in answers or numbers** | solve-q-325 (2x + 28 < 8 + 6x < 20) + solve-q-326 slide 2 "Trial and error" | SAME (the "not OR" point and the number line kept; English adds Method 2, test a number; her trial-and-error remarks moved to after the next question) |
| 7 | x⁴ < 20 < x⁵, x integer (example) + chaining intro | 9359-9458 | x can't be negative (odd power) → choices 1 and 4 out; test 2: 16 < 20 < 32 ✓, **"mark it, only one answer is right"**; 3 "just for sport" fails. Then: **chaining — two inequalities with a common side can be chained, and you may ignore the middle** (x⁴ < x⁵) | solve-q-326 (x⁴ < 300 < x⁵) | SAME ("only one answer is right, mark it and move on", "just for the exercise", and x⁴ < x⁵ as another way) |
| 8 | x < y + 1, 2y − 1 < x (example) + second-degree theory | 9459-9567 | Chain: 2y − 1 < x < y + 1, ignore x → y < 2. Then: **x² on the small side → a closed range between −√a and √a; on the big side → outside**; "rare but important" | solve-q-327 (a < b + 5, 3b − 1 < a) + solve-q-328 slides 3-4 | SAME (English adds "a < b or b < a? nothing forces either") |
| 9 | (5x² − 3)/3 < (2x² + 10)/2 (example) + equation-with-inequality intro | 9568-9724 | **Cross-multiply ("כפל באלכסון")** → 4x² < 36 → x² < 9 → −3 < x < 3; why: for positives 1² = 1, 1.5² = 2.25, 2² = 4 fit, 4², 5² don't; negatives square to positives → symmetric (−3)² = 9, (−4)² = 16. Then: an equation + an inequality → substitute, as with two equations | solve-q-328 ((4x² − 9)/5 < (x² + 18)/2) | CHANGED: English **multiplies both sides by 10** instead of cross-multiplying (the base translation still said "Cross-multiply"). The result, the small-side rule and the symmetry check with numbers (5², (−5)², 7²) are the same; English adds Method 2, test zero |
| 10 | x + y = z, x < z < y (example) + lesson close | 9725-9848 | Substitute z = x + y → double inequality → y > 0, x < 0 → xy < 0; z unknown; xy ≠ 0. Close: the types on the exam; **second-degree is the hardest part: rewatch, try a few numbers yourself**, practise | solve-q-329 (p + q = r, q < r < p) + solve-q-328 slide 4 "Rare — but know it" ("Not sure yet? Test a few numbers yourself") | SAME |
| 11 | אי שוויונות · Advanced intro | 9849-9852 | One sentence: higher-level practice to close the topic | solve-q-330 opening ("Advanced inequalities.") | SAME (trivial) |
| 12 | 30/60 < x/(x+1) < 50/60, x positive integer, how many (medium) | 9853-10081 | (1) Reduce to 1/2 and 5/6; split; **"advanced technique: multiplying by an unknown" — check its sign first (x + 1 > 0 since x is a positive integer), else the sign may need to flip**; cross-multiply; 1 < x < 5 → count 2, 3, 4 → 3. (2) Insight ("הברקה"): consecutive numerator/denominator like 1/2 and 5/6 → try x: 2/3, 3/4, 4/5; 5 gives 5/6, equal → 3. "The shortcut is shorter, but the technique matters a lot later" | solve-q-330 (60/90 < x/(x+1) < 81/90 → 6 values) | SAME (both methods, the sign check, and her closing remark. English multiplies by 3(x + 1) and 10(x + 1) instead of "cross-multiplying", same move; adds "x/(x+1) grows as x grows") |
| 13 | (xy)² < xy² (medium+) | 10082-10208 | Cancel y² only after deciding its sign: not negative, and not 0 (both sides would be equal) → positive, cancel, no flip; then x² < x: x² ≥ 0 and x is bigger, so x > 0 → cancel → 0 < x < 1 | solve-q-331 ((xy)² < x²y → 0 < y < 1) | SAME |
| 14 | (x − 4)/(8 − x) < 0, which does NOT satisfy (medium+) | 10209-10470 | (1) Sign unknown, can't clear the denominator; a fraction is negative in two cases (top +, bottom −, or the reverse); solve each, eliminate choices as you go; "long and exhausting". (2) Trial and error: plug a comfortable number from each choice's range (0, then 6 → 1, not negative → answer); "recommended on the exam" | solve-q-332 ((x + 1)/(7 − x) < 0) | SAME (both methods, "long and exhausting", "the route I recommend"; English adds the sign table as a short way to write method 1) |
| 15 | (x + y)² = 81, x − 2 > 0, x, y positive (medium) | 10471-10618 | (1) Root → ±9, but positive → 9; x > 2; isolate x from the equation and substitute → y < 7, y > 0. (2) Understanding ("in your head"): y completes x to 9 (x = 3 → 6, x = 4 → 5, x near 2 → y near 7); "a method and a half"; better if you can, saves calculation | solve-q-333 ((x + y)² = 144, x − 4 > 0) | SAME |
| 16 | x > z + y, x < z < y, which is NOT true (medium+) | 10619-10742 | Chain with many letters: z + y < x < z < y; **find two places with the same letter**: z + y < z → y < 0 (or z + y < y → z < 0); so z < y is negative, x negative, z + y negative → "y + z > 0" is the answer | solve-q-334 (m + n < p, p < n < m) | SAME (English adds the number-line picture) |
| 17 | 13 ≤ x² − 3 ≤ 33, x integer, how many (high) | 10743-10875 | Splitting works, but **"a special double inequality: the unknown only in the middle" → isolate it in one move** (+3 to all parts) → 16 ≤ x² ≤ 36; assume x positive → 4 ≤ x ≤ 6, **mirror** to −6…−4; they ask how many VALUES, x integer → 6 | solve-q-335 (5 ≤ x² − 4 ≤ 60 → 12) | SAME |
| 18 | −5 < x < 10, −20 < y < 5, range of xy (high) | 10876-10975 | Min-max: plug in the edges, treat 10 as if allowed ("the real value is a bit less"); max when positive (both +: 50; both −: 100); eliminate choices; min: one + one − → −200 already the smallest; finish: −25 irrelevant. "Analyse the cases, check the edges" | solve-q-336 (−6 < x < 9, −15 < y < 3) | SAME (English adds "multiplying ranges end by end works only when everything is positive") |
| 19 | 8th advanced question | 10976-11075 (a duplicate of row 18) | — no transcript — | solve-q-337 (a < b, which is necessarily true) | cannot be rated |
| 20 | 20 שאלות תרגול עצמי · 20 self-practice questions | 11076 (note) | — | unit `unit-t12-3` (27) + `unit-t12-2` (8) | SAME |

**Count by row (19 rateable rows):** SAME 18 · CHANGED 1 (row 9) · PARTIAL 0 · MISSING 0. Row 19 cannot be rated.

### Count by video (her 19 units: 2 lessons, 8 lesson examples, the advanced intro, 7 advanced questions, practice)

**SAME 18 · CHANGED 1 · PARTIAL 0 · MISSING 0** (plus her 8th advanced question, which has no transcript).

---

## 2. English → Hebrew (added, no Hebrew equivalent)

| English video / part | Added content | Hebrew source? |
|---|---|---|
| `inequalities` slide 6 "Ranges in two moves" + Method 2 in solve-q-322 and solve-q-r26-t12-13 | Solve as an equation for the endpoint, then test one number for the direction; for "most precise range" choices, test a number some choices contain | none |
| solve-q-323 slide 2 | x disappears and what's left is false → no x | none (she shows only the true case) |
| Test-a-number methods in solve-q-325, solve-q-328 | Eliminate range choices with one number | her trial-and-error idea, applied to new questions |
| solve-q-332 (part) | The sign table | none |
| solve-q-337 | a < b: understanding + counterexamples with negatives; "your list: 0, 1, −1, ½, a big number" | unknown (her transcript is missing) |
| r26-t12-signs, solve-q-r26-t12-01, -02 | Reciprocals flip when the signs are the same; plug in −½; sign table for (x − 2)(x + 5) < 0 | none |
| r26-t12-combining, solve-q-r26-t12-03, -04 | Range of x²; adding inequalities is safe, subtracting/multiplying/dividing are not; range of x − y (biggest minus smallest) | none |
| solve-q-r26-t12-13 | −7 ≤ 3 − 2x < 5: test numbers; two moves | none |
| r26-t12-summary | Summary text (becomes a summary page) | none |

The base translation had all her theory steps on lesson slides ("No overlap", "Test the choices", "Chain them", "x²
inequalities", "Plus an equation"); the current English moved them into the question that first uses each, which is
exactly her own order (she introduces each type right after the example before it). Nothing was lost in that move.

---

## 3. Missing from English: restore?

| # | Her content | Where it would go | Target recorded? | Recommendation |
|---|---|---|---|---|
| 1 | Cross-multiplying ("כפל באלכסון") the fraction inequality, with the condition that makes it safe (both bottoms positive) | solve-q-328 slide 1: "Cross-multiply. Both bottoms, five and two, are positive — so no flip." (1-2 sentences, replaces "multiply by ten") | yes (old take, 7 Oct); goes into the AI redo | Optional. Multiplying by 10 is equally correct; her version connects to q-330, where checking the bottom's sign before multiplying is the whole point |
| 2 | Her 8th advanced question | — | — | **Ask the teacher** for the subtitles of that video (her file has the 7th question twice), so solve-q-337 can be checked |

**RESTORE list: empty.** Every method and tip she gives in this topic is in the English videos, and nothing in English
contradicts her. Her "on the exam the sign is ALWAYS written smaller-on-the-left" became "almost always", which is safer.
