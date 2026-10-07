# Topic 12 — Inequalities: changes

Patch: `math_patches/t12.py`. Check: `python3 math_check.py 12` shows 0 problems, 0 warnings and 0 layout problems.

## Summary
- Questions: 42 rewritten, 12 added (4 guided with solution videos, 8 practice), 1 removed (q-340).
  The topic had 16 guided and 27 practice questions. It now has 20 guided and 34 practice questions.
- 13 slides changed in existing videos. The sidebars of the 8 advanced solution videos now list Questions 9 to 20.
- 2 new lesson videos: "Signs, Fractions & Must-Be-True" (6 slides) and "Combining Inequalities & Ranges" (6 slides).
- 4 new solution videos, for the new guided questions.
- 1 new memory card: "Inequality traps". The old card "Inequality rules" got 3 rows changed or added.
- Figures: this topic has none.

The guided questions are renumbered in course order: the new ones are Q9, Q10, Q17 and Q18, so the old Q9–Q16 are now Q11–Q16, Q19 and Q20.

## 1. Wrong or misleading teaching (fixed)
- **Lesson 1, slide 4 ("A minus flips it"):** the old demo ended with "1 < 3 … same answer — three greater than one". Students could not see why that was the same answer. The new demo:
  - −12 < −4 divided by −4 gives 3 > 1, so the sign must flip.
  - Then it solves −2x < 6 in two ways: divide by −2 and flip (x > −3), or move the terms across (−6 < 2x, so −3 < x) with no flip.
  - It ends with a check using x = 0.
  - Students now see one flip done in full.
- **"Cross-multiply" removed** from lesson 2 slide 6, from the Q7 video (the slide title is now "Multiply by 6, then the rule") and from the Q11 (old Q9) video. The teacher now says "multiply both sides by 6 / by 2(x + 1) — a positive number, so nothing flips".
- **Q5 video:** the unclear "you could even ignore the ninety — x⁴ < x⁵" is now explained: divide x⁴ < x⁵ by x⁴ (it is positive), so x > 1.
- **Q20 (old Q16, q-337) solution text:** removed the false start (x = −1, y = −0.5 was not a counterexample).
- **q-350 solution text:** removed the unfinished "Add the two inequalities: (a − b) + (something)". It now uses the chain, plus a correct way to add them (b − a < 0 and a + b < 0, which gives 2b < 0).
- **Garbled boards (review §3):** I rendered them. Lesson 1 slide 2 and lesson 2 slide 6 display correctly on the slides. The loss happened only in the text dump the reviewer read. Q9 and Q11 on screen also show proper fraction bars. No change was needed.

## 2. Methods added
**Lesson 1:** the recap now says "× or ÷ by a negative" (it said ":").

**Lesson 2, slide 6:** added a worked **x² on the big side** example: −2x² ≤ −32. Divide by −2 and flip to get x² ≥ 16, so x ≥ 4 or x ≤ −4. A number check follows. The recap line now reads "x² small side: between the roots · big side: outside".

**New lesson "Signs, Fractions & Must-Be-True"** (start of the advanced section, before the first advanced question):
1. **Between 0 and 1:** x² < x < √x < 1 < 1/x, tested with x = 1/4. For x > 1 the order turns around (tested with 4). For negatives, plug in −1/2.
2. **Reciprocals:** same sign → the sign flips; different signs → no flip. Three examples.
3. **Sign table** for a product or a fraction: mark the zeros, then test one number in each part. Example: 3x(1 − 3x) > 0 gives 0 < x < 1/3 (this is q-352).
4. **Must / could / cannot:** one counterexample kills "necessarily true"; one example keeps "could be true"; "cannot" breaks the givens. The list of numbers to try: 0, 1, −1, ½, a big number.
5. Recap.

**New lesson "Combining Inequalities & Ranges"** (right before Q19, the xy range question, old Q15):
1. **Add** inequalities that point the same way: 1 < a < 3 and 2 < b < 5 give 3 < a + b < 8.
2. **Never subtract** end from end. The trap is shown: for a − b, biggest a minus smallest b gives −4 < a − b < 1. Another way: flip b, then add.
3. **Multiply:** end by end only when everything is positive. Otherwise check the four corners (−1 < a < 3 and 2 < b < 5 give −5 < ab < 15). Division works the same way, and the bottom must not be 0.
4. **Range of x²:** from −3 < x < 2 you get 0 ≤ x² < 9, not 4 < x² < 9.
5. Recap.

**Additions to existing solution videos:**
- Q11 (old Q9): why x/(x+1) grows with x.
- Q13 (old Q11): points to the sign table.
- Q15 (old Q13): the chain is drawn on a number line.
- Q20 (old Q16): the numbers-to-try list is now a board line.

**New guided questions** (each has a solution video):

| # | id | Question | Answer |
|---|---|---|---|
| Q9 | q-r26-t12-01 | −1 < x < 0: which of x, x², x³, 1/x is the greatest? | x² (plug in −½) |
| Q10 | q-r26-t12-02 | (x − 2)(x + 5) < 0 | −5 < x < 2 (sign table) |
| Q17 | q-r26-t12-03 | a > b and c > d: which is necessarily true? | a + c > b + d; counterexamples for a − c > b − d, ac > bd and a/c > b/d |
| Q18 | q-r26-t12-04 | −2 < x < 5 and 1 < y < 4: range of x − y | −6 < x − y < 4; choice 2 (−3 < x − y < 1) is the end-from-end trap |

**Memory cards:**
- "Inequality rules" now has:
  - the move-across example (−2x < 6 → −6 < 2x)
  - a row "multiply by an unknown only if you know its sign"
  - a worked example for x² > a
- New card "Inequality traps" (after the last advanced question) has three tables: combining and ranges; signs and special numbers; question words. It ends with two tips.

## 3. Text (all 42 remaining questions)
- Every stem, choice and solution is in TeX, with no ":" for division. The old solutions wrote 1:2, 2x:5, −5x:2, 1:3 and so on.
- Stems with several conditions are stacked with `\begin{cases}`: q-327, 329, 333, 334, 336, 339, 343, 347, 348, 350, 351, 353, 355, 356 and 357, and extra-6.
- Every solution shows the numbers. The 7 extras had word-only solutions, and each now has worked lines and a check.
- Solutions use the taught method:
  - sign table for q-352 and q-354
  - try-a-number for q-332
  - "multiply by a positive number" for q-328, q-330 and q-355
- Several solutions also mention the faster way.
- **Q2 (q-323) choices** were "0 / 12 / 1 / Any value". They are now ranges: "Only for x < 0", "Only for x > 12", "Only for x < 1", "For every value of x". The key is unchanged (choice 4).
- q-325 choice 3 is now "For no value of x" (it said "(empty set)"). q-338 choices are full sentences. q-352 and q-357 write −1/3 as −⅓, not as (−1)/3.
- Wording like "precise domain" and "From this it necessarily follows that:" is now "most precise range" and "Which of the following is necessarily true?"

## 4. Practice
- Removed **q-340**, a near-duplicate of q-339.
- The 8 new exam-level questions:

  | id | Question | Skill |
  |---|---|---|
  | q-r26-t12-05 | range of a − b when b is negative | range of a difference |
  | q-r26-t12-06 | x² from −3 < x < 2 | x² range trap |
  | q-r26-t12-07 | x + y > 10 and x − y > 4 | add the inequalities: x > 7 |
  | q-r26-t12-08 | smallest of 1/x, 1/x², √x, x for x > 1 | order above 1 |
  | q-r26-t12-09 | (x + 1)/(x − 4) < 0 | integer count with a sign table |
  | q-r26-t12-10 | x < y < 0 | "could be true" |
  | q-r26-t12-11 | range of ab with negative ends | four corners |
  | q-r26-t12-12 | a > b > 0 | "cannot be true" with reciprocals |

- The section is ordered easy → hard. The 7 easy extras come first as a warm-up. The exam-hard items come last: q-350, the new 10 and 11, q-355, q-356 and q-357.

## Answer checks
I solved every new and changed question from scratch. Each has exactly one correct choice, and the key matches its solution video ("Circle choice N"). Keys of the existing questions are unchanged.

## Notes for the teacher
- The API has no call to change a board item's text only. I changed the item text directly on the slide (lesson 1 recap, lesson 2 recap), and the patch marks those videos as touched.
- The new lesson "Signs, Fractions & Must-Be-True" sits at the start of the advanced section, so the first two advanced questions are now the new Q9 and Q10. If you prefer the old Q9 (x/(x+1)) to open the section, move the video and its two questions after it.
- Q15 (old Q13, "which is NOT necessarily true") has a choice that is never true. That is fine for the key, but you may want to reword the stem to "Which of the following is not true?"

## Pass 2 (plan `real_exam/PLAN_REMOVE_RESTORE.md`, teacher-approved 2026-09-27)
**Removed:** nothing. The plan removes nothing in T12.

**Restored (3):**
- q-340 is back in the practice, after q-339 (it was removed as a near-duplicate). Only clean-up: the givens are stacked, and the solution shows the numbers. Answer: x = −4 (choice 3). I solved it again.
- `inequalities` slide 4 "A minus flips it": the original demo and advice are back, exactly as in the original. This includes "I recommend you don't multiply by a minus at all", "move the terms across… 4 < 12" and "÷4 → 1 < 3". Only ":(−4)" and ":4" changed, to "÷(−4)" and "÷4". The added −2x < 6 example (both ways, with a check) stays on a new slide 5, "The same with x". It uses the same sidebar entry.
- q-323: the original choices are back: 0 / 12 / 1 / Any value. The key is "Any value" (choice 4), and it matches the solution video ("So any value works. Choice four.").

**Summary video (new):** `r26-t12-summary`, "Inequalities: Summary". It is at the end of the advanced section, after the "Inequality traps" card and right before the practice. Slides: Summary · Same moves · x disappears · Systems · x² inequalities · Test the choices · Signs and fractions · Combining ranges · Must, could, cannot · Before you practice. About 3 minutes.

Check: `python3 math_check.py 12` gives 0 problems, 0 warnings and 0 layout problems. The same is true for `11 12` together.


## 2026-10-04 question = lesson example fixed
- q-r26-t12-06 was −3 < x < 2 of "r26-t12-combining" slide 5 -> −4 < x < 3, so 0 ≤ x² < 16 (choice 2).

## 2026-10-05 cut repeats
Function `cut_repeats` (runs last). Nothing in topic 12 is recorded.
- **Inequalities** (4.9 → 3.3 min, Hebrew 3.4). Cut "x to the plus side" and "Every x works" (the Hebrew lesson's own examples; Q1 and Q2 are the same questions with new numbers) and the recap. Slide "The same with x" ends with "Now two questions."
  - Q1: title "the tip from the lesson" → "a tip that saves you on the exam"; added the board item "Tip: move x to the side with MORE x — it stays positive" + one line before the solving.
  - Q2: new short slide "True or false?": "x disappears: true → every x · false → no x" + one line (the "false" case was only on the cut slide).
- **Systems of Inequalities** (5.5 → 0.6 min, Hebrew intro 1.0): title + one slide "solve each one separately → find where they overlap". Cut six near-twins of the questions: overlap → Q3, no overlap → Q4, test the choices x⁴ < 20 < x⁵ → Q5 (x⁴ < 90 < x⁵), chain → Q6, x² inequalities → Q7, plus an equation → Q8; recap.
  - Q7: "Remember the rule." → "and its rule."; new short slide "Small side, big side" with both rules on the board; the big side (taught only on the cut slide) uses new numbers x² > 9 (the cut slide's −2x² ≤ −32 is practice question q-345).
- **Signs, Fractions & Must-Be-True** (2.9 → 1.6 min). Cut "Sign table" → Q10; the negative example −½ → Q9 (same numbers); the list "0, 1, −1, ½, a big number" → Q20 (on its board); recap. Kept: between 0 and 1 (with 1/x), reciprocals, must/could/cannot.
- **Combining Inequalities & Ranges** (2.4 → 0.9 min). Cut "Add them" → Q17, "Never subtract" → Q18, "Multiply" (corners) → Q19, recap. Kept "Range of x²".
  - Q17: new short slide "Ranges add too": 1 < a < 3, 2 < b < 5 → 3 < a + b < 8 + one line.
  - Q19: board item "All positive? Multiply end by end. Negatives inside? Check the corners" + one line (also: when dividing, the bottom cannot be zero).

## 2026-10-06 new exam methods
Function `add_methods` (runs last).
- **RANGES IN TWO MOVES** (about 15 real exam questions): new named slide 6 "Ranges in two moves" in the lesson "Inequalities" (sidebar item added): endpoint (pretend "=", solve) → direction (test one easy legal number). Example 5 − 2x > x − 4: endpoint 3, x = 0 works → x < 3. Plus "most precise range": a number that works kills every choice that leaves it out; a number that fails kills every choice that contains it. Limits (legal numbers; a zero denominator is a border too). The line "Now two questions…" moved from slide 5 to the end of the new slide.
- Question 1 (solve-q-322): slide 3 "Quick check" → "Method 2 · Two moves" (endpoint −6 kills choices 1, 2, 4; x = 0 gives the direction). q-322 written solution gets the two-moves line.
- **New guided q-r26-t12-13** (Question 11; the old 11–20 become 12–21) after the sign-table question: Given x² + 3x < 10, the most precise range? Choices x < 2 · −2 < x < 5 · −5 < x < 2 · x > −5 → **3**. x = 3 fails → 2 and 4 out; x = −6 fails → 1 out. Method 2: two moves (endpoints −5 and 2, x = 0 works). Advanced sidebar extended to 13 questions.
- Card "Inequality rules", Types: two new first rows ("For which values of x?" two moves; "The most precise range" test rule).
- Card "Inequality traps": new row "Range of a/b (all positive)": smallest top ÷ largest bottom, largest top ÷ smallest bottom; 2 < a < 6, 1 < b < 3 ⇒ 2/3 < a/b < 6.


## 2026-10-06 practice: new methods
Function `practice_methods` (runs last; append only). 6 practice questions.
- Method 2 · Two moves: alg-extra-unit-t12-3-1 (−3x > 9 → endpoint −3, x = 0 false → x < −3), q-346 (a + 4 < a/2 → endpoint −8, a = 0 false → a < −8).
- Method 2 · The most precise range: q-355 (x = 2 kills 1, 3; x = ½ kills 4), q-354 (n = 1 kills 2, 4; n = −1 kills 1), q-353 (x = −4 alone kills 1–3), q-r26-t12-06 (x² = 0 kills 1; x² = 12.25 kills 3, 4).
All new lines verified numerically (python: fitting values, choice values, power by scaling). `math_check.py 12 32`: PROBLEMS 0, WARNINGS 0, LAYOUT 0.

## 2026-10-06 renumber pass
So the English course does not look like the Hebrew one: every Hebrew-derived question has new numbers or letters.
The idea, the trap and the methods stay the same, and every guided solution video is rewritten to match (board,
speech, draw cues, video title). Nothing in Topic 12 is recorded, so nothing had to be kept as it was.
Function `renumber(M)` in t12.py runs last.

**Counts:** 16 guided questions renumbered (q-322 … q-337) with their 16 videos rewritten; 20 practice questions
renumbered (q-338 … q-357); 4 lesson examples renumbered (lesson "Inequalities": x ≤ 5, −8 < −3, x + 5 < 14,
−12 < −4); 2 card examples that used Hebrew question numbers changed (x² ≥ 16 → x² ≥ 81; 3x(1 − 3x) > 0 → x(2 − x) > 0).
Practice: 35 → 27.

**Order:** the chain question (now Question 5, a < b + 5 and 3b − 1 < a) comes before the plug-in question
x⁴ < 300 < x⁵ (now Question 6). Neither video refers to the other. The correct-answer position moved in 35 of the 36 questions.

**Practice clean-up (35 → 27):**
- Extra warm-ups kept (3): −3x > 9 (the flip), x > 3 and x ≤ 5 (overlap), x > 2 → 1/x < 1/2 (reciprocals).
  Removed: 2x + 3 ≤ 13 and "integers in −3 < x < 5" (q-344 covers both), 0 < x < 1 → x² < x (this is the lesson
  board itself; q-347 covers it), a < b < 0 reciprocals (a copy of Topic 3's q-r26-t03-06).
- September items kept (4, their types are not in the Hebrew practice): range of a − b (05), range of x² (06),
  "could be true" (10), range of ab (11). Removed: adding inequalities (07, covered by q-350), x > 1 smallest power
  (08, covered by q-341/q-347, and a copy of Topic 3's q-r26-t03-05), fraction sign count (09, covered by q-354),
  reciprocals "cannot be true" (12, covered by the warm-up and q-343/q-357).
- I kept 27 rather than the audit's 25 on purpose, so that every kept September item practises a type nothing else covers.

**Checks:** every answer, distractor and method computed in Python (brute force over many values); `math_check.py 12 32`
gives PROBLEMS 0, WARNINGS 0, LAYOUT 0; all 17 changed videos rendered and looked at.

| id | old (Hebrew numbers) | new | answer |
|---|---|---|---|
| q-322 (G) | 3 + x < 15 + 3x | 4 + x < 18 + 3x | −7 < x (choice 2) |
| q-323 (G) | 3(4 − 3x) − 7 < 8 − 9x | 5(2 − 3x) − 4 < 7 − 15x | any value (3) |
| q-324 (G) | 2x − 5 < x + 3 < 3x − 9 | 3x − 4 < 2x + 5 < 4x − 5 | 5 < x < 9 (2) |
| q-325 (G) | 3x + 30 < 12 + 6x < 30 | 2x + 28 < 8 + 6x < 20 | no value (2) |
| q-326 (G, now Q6) | x⁴ < 90 < x⁵ | x⁴ < 300 < x⁵ | 4 (3) |
| q-327 (G, now Q5) | x < y + 2, 2y − 2 < x | a < b + 5, 3b − 1 < a | b < 3 (2) |
| q-328 (G) | (5x² − 2)/3 < (2x² + 20)/2 | (4x² − 9)/5 < (x² + 18)/2 | −6 < x < 6 (1) |
| q-329 (G) | a + b = c, a < c < b | p + q = r, q < r < p | pq < 0 (2) |
| q-330 (G) | 40/80 < x/(x+1) < 70/80 | 60/90 < x/(x+1) < 81/90 | 6 values (3) |
| q-331 (G) | (ab)² < ab², range of a | (xy)² < x²y, range of y | 0 < y < 1 (4) |
| q-332 (G) | (x − 3)/(9 − x) < 0 | (x + 1)/(7 − x) < 0 | −1 < x < 7 fails (3) |
| q-333 (G) | (x + y)² = 100, x − 3 > 0 | (x + y)² = 144, x − 4 > 0 | 0 < y < 8 (2) |
| q-334 (G) | c + b < a, a < c < b | z + y < x, x < z < y | 0 < z + y (2) |
| q-335 (G) | 2 ≤ x² − 2 ≤ 34 | 5 ≤ x² − 4 ≤ 60 | 12 (3) |
| q-336 (G) | −4 < x < 10, −30 < y < 6 | −5 < x < 8, −20 < y < 4 | −160 < xy < 100 (4) |
| q-337 (G) | x < y; x < y + 5 | a < b; a < b + 3 | a < b + 3 (1) |
| q-338 | m = x + y − 8, m < 0 | k = a + b − 6, k < 0 | integer smaller than 6 (3) |
| q-339 | 2x + 5 < 0, x² < 15 | 2x + 7 < 0, x² < 20 | −4 (4) |
| q-340 | x² < 25, 3x + 9 < 0 | x² < 36, 2x + 8 < 0 | −5 (2) |
| q-341 | x³ < x² < 3 | x³ < x² < 7 | −2 (3) |
| q-342 | 6 < x < 7 | 8 < x < 9 | x + 8 < 2x (2) |
| q-343 | p < q, r < s, q < s | a < b, c < d, b < d | d < a cannot (2) |
| q-344 | x − 3 < 6 | x − 2 < 5 | 6 (3) |
| q-345 | −2x² ≤ −32 | −4x² ≤ −100 | −3 fails (3) |
| q-346 | a + 4 < a/2 | a + 6 < a/3 | a < −9 (1) |
| q-347 | 0 < x < 1, 5y = 2x | 0 < x < 1, 4y = 3x | y² < 1 (2) |
| q-348 | a + b = 17, b < a | a + b = 21, b < a | b < 11 (2) |
| q-349 | 3y < x < −3y | 4m < n < −4m | m < 0 (3) |
| q-350 | 0 < a − b, a + b < 0 | 0 < y − x, x + y < 0 | x < 0 (1) |
| q-351 | 5x + 2y = 0, x > 2 | 3x + 2y = 0, x > 4 | y < −6 (3) |
| q-352 | 0 < 3x − 9x² | 0 < 2x − 8x² | 0 < x < 1/4 (2) |
| q-353 | x < 0, 3 < x² − 6 < 19 | x < 0, 5 < x² − 11 < 38 | −7 < x < −4 (1) |
| q-354 | (3 + n)/(3 − n) > 0 | (2 + n)/(6 − n) > 0 | −2 < n < 6 (4) |
| q-355 | 1/4 < x/(x+1) < 3/4 | 1/3 < x/(x+1) < 4/5 | 1/2 < x < 4 (3) |
| q-356 | x²y² = (xy − 2)², x > 1 | a²b² = (ab − 6)², a > 3 | 0 < b < 1 (2) |
| q-357 | y²a + y²c < (a + c)², a + c = y | k²m + k²n < (m + n)², m + n = k | k cannot be 3 (3) |
| lesson | x ≤ 5 (5, 4.5, 3, −7); −8 < −3 | x ≤ 4 (4, 3.5, 1, −6); −7 < −2 | – |
| lesson | x + 5 < 14 → x < 9 | x + 6 < 11 → x < 5 | – |
| lesson | −12 < −4, ÷(−4) → 3 > 1 | −10 < −2, ÷(−2) → 5 > 1 | – |

The "Method 2" lines in practice (q-346, q-353, q-354, q-355) are rewritten with the new numbers. The guided
questions added in 2026-09/10 (q-r26-t12-01 … 04, 13) and the kept practice items are English-made, so they keep
their numbers. No question equals a lesson example from this topic or earlier.

## 2026-10-06 review
Independent check of the renumber pass (all 36 Hebrew-derived questions, 16 solution videos, lesson "Inequalities", 2 cards, practice removals). Keys re-computed in Python (brute force); traps, kind of condition and methods compared with the pre-renumber version.
- q-341: $x^3<x^2<7$ let both $-1$ and $-2$ fit ($-1$ was not a choice, but the question asks "What is $x$?" — one value, as in the Hebrew). Now $x^3<x^2<4$, choices $1, 0, -2, -1$, key 4: only $-1$ fits, and $-2$ is the boundary trap ($4<4$ false), like the Hebrew's $-2$ ($4<3$ false).
- Lesson "Inequalities" slide 4: the click label still said "−12 < −4 appears again below" → "−10 < −2 appears again below".
`python3 math_check.py 12 32` → 0 problems, 0 warnings, 0 layout. Rendered inequalities, solve-q-327, -332, -335, -336.
- (review, teacher decision: no quadratic trinomials) q-r26-t12-13 was x² + 3x < 10 (a hidden trinomial). Replaced by a
  two-sided linear most-precise-range question: −7 ≤ 3 − 2x < 5. Choices x ≤ 5 / −5 ≤ x < 1 (trap: endpoints with wrong
  signs) / −1 < x ≤ 5 / x > −1 · key 3 (brute force on a 0.01 grid: only choice 3 matches). Video keeps both methods:
  test x = −3 (fails → choices 1, 2 out) and x = 6 (fails → choice 4 out); two moves (endpoints −1 and 5, test 0, which
  end is included). Written solution rewritten. The card row "most precise range" had no trinomial wording (unchanged).

## 2026-10-06 Hebrew back-check
Function `hebrew_backcheck` (runs last). Every guided and practice question, lesson, summary and card example was compared
with the Hebrew video subtitles (lines 8730–11078: 9 lesson examples, 7 sample questions). Nothing in topic 12 is recorded.
Keys brute-forced / recomputed in Python; videos rendered and checked. `python3 math_check.py 12 32` → 0 / 0 / 0.

| id | Hebrew video | ours before | new | answer |
|---|---|---|---|---|
| lesson `inequalities` slide 4 | −10 < −6, ÷(−2) → 5 > 3 | −10 < −2, ÷(−2) → 5 > 1 | −18 < −3, ÷(−3) → 6 > 1; move: 3 < 18, ÷3 → 1 < 6 | — |
| q-334 (guided) | z+y < x, x < z < y; y+z > 0 false | the same letters and givens | m+n < p, p < n < m; choices n<0, p<0, 0<m+n, m<0 | 0 < m+n (3) |
| q-336 (guided) | −5 < x < 10, −20 < y < 5 → −200 < xy < 100 | −5 < x < 8, −20 < y < 4 → −160 < xy < 100 | −6 < x < 9, −15 < y < 3 → corners 90, −18, −135, 27 | −135 < xy < 90 (4) |

Videos rewritten to match: solve-q-334, solve-q-336, lesson slide 4.
**Left on purpose (partial overlaps only):** q-324 (3x−4 < 2x+5 < 4x−5 → 5 < x < 9; Hebrew 3x−8 < 2x+3 < 5x−12 → 5 < x < 11:
only the 3x / 2x and the bound 5 shared); q-331 ((xy)² < x²y asks y; the Hebrew (xy)² < xy² asks x — letter question,
letters already swapped); q-329 (p+q = r, q < r < p — letters already changed, key moved). Practice: no match.

## 2026-10-06 pen or click
(Done 2026-10-07.) Function `pen_or_click(M)` in t12.py runs last (after `add_methods`, `renumber` and
`hebrew_backcheck`), on the final text. The teacher's approved split: lessons - content by click, the pen only marks;
solution videos - setup and mechanical lines by click, by hand only the one or two key steps plus the marks on the
choices. Where a hand-written line comes before click lines, the board leaves an empty row for it. Spoken lines, math,
questions and slide count are unchanged. No topic 12 video is recorded. inequality-systems, r26-t12-combining and the
summary have no pen cues.
Topic total: 128 pen cues -> 53 by hand, 69 by click, 6 split (59 pen cues left, most of them circles / cross-outs).

- inequalities (lesson, 10 -> 0 by hand, 9 clicks, 1 split). Every written line is a click: 4, 3.5, 1, −6 ✓; x + 6 − 6 < 11 − 6 (was "−6 under both sides"); x < 5; ÷(−3): 6 > 1; 3 < 18; ÷3: 1 < 6; ÷(−2): x > −3; −6 < 2x → −3 < x; x = 0 check. Split: the dots on −7 and −2 by hand, "−7 < −2" click.
- r26-t12-signs (1 -> 1 click): "same sign → flip; different signs → no flip".
- solve-q-322 (7 -> 3 by hand, 4 clicks). By hand: 4 − 18 < 3x − x (x to the side with more x), circles. Method 2 endpoint / direction lines are clicks.
- solve-q-323 (3 -> 1 by hand, 1 click, 1 split). Split: cross out −15x by hand, 6 < 7 click.
- solve-q-324 (4 -> 2 by hand, 2 clicks). By hand: 5 < x < 9 (the overlap), circle. Clicks: the two halves ("left:", "right:").
- solve-q-325 (3 -> 1 by hand, 2 clicks). The two halves are clicks; circle by hand.
- solve-q-327 (4 -> 2 by hand, 1 click, 1 split). By hand: the chain 3b − 1 < a < b + 5, circle. Split: cross out the a, 3b − 1 < b + 5 click.
- solve-q-326 (4 -> 2 by hand, 2 clicks). The tries are clicks labelled (3) x = 4 and (2) x = 3.
- solve-q-328 (5 -> 2 by hand, 3 clicks). By hand: −6 < x < 6 (between the roots), circle.
- solve-q-329 (5 -> 2 by hand, 3 clicks). By hand: q < p + q < p (substitute), circle. Lines 34.
- solve-q-r26-t12-01 (3 -> 2 by hand, 1 click). By hand: x = −½, circle. Click: the four choice values.
- solve-q-r26-t12-02 (6 -> 2 by hand, 4 clicks). By hand: the number line with −5 and 2 (sign table), circle. Clicks: the zeros, the three tests.
- solve-q-r26-t12-13 (6 -> 2 by hand, 4 clicks). By hand: the cross-outs and circle. Clicks: the two tests, the two moves.
- solve-q-330 (9 -> 5 by hand, 4 clicks). By hand: "= 2/3" and "= 9/10" under the fractions, 2x + 2 < 3x → 2 < x (multiply by the positive 3(x + 1)), circles. Clicks: the split into two inequalities (one line), 10x < 9x + 9 → x < 9, 2 < x < 9 → 3…8, the fractions 3/4 … 8/9.
- solve-q-331 (5 -> 1 by hand, 2 clicks, 2 split). By hand: y > 0. Split: cross out x² + y² < y; 0 < y < 1 + circle.
- solve-q-332 (13 -> 7 by hand, 6 clicks). By hand: "top + / bottom −" and "top − / bottom +" (the two cases), the cross-outs, circles. Clicks: the case lines; method 2 tries labelled (1), (2), (3).
- solve-q-333 (7 -> 3 by hand, 3 clicks, 1 split). By hand: x + y = ±12 and crossing out the minus, circle.
- solve-q-334 (7 -> 5 by hand, 2 clicks). By hand: the chain m + n < p < n < m, the number line, the arc, cross-outs, circle. Clicks: m < 0; n < 0, p < 0.
- solve-q-335 (5 -> 2 by hand, 3 clicks). By hand: the marks on the number line, circle. Clicks: +4: 9 ≤ x² ≤ 64; 3 ≤ x ≤ 8; ±3 … ±8. The number line now follows the click lines (its fixed position was removed); lines 34.
- solve-q-r26-t12-03 (5 -> 2 by hand, 3 clicks). By hand: a + c > b + d ✓ (add), circle. Clicks: the three counterexamples.
- solve-q-r26-t12-04 (5 -> 2 by hand, 3 clicks). By hand: biggest: 5 − 1 = 4, circle. Lines 34.
- solve-q-336 (4 -> 2 by hand, 2 clicks). The corners are clicks; cross-outs and circle by hand.
- solve-q-337 (7 -> 3 by hand, 4 clicks). By hand: a < b < b + 3, circles. Clicks: the three counterexamples, the "Try:" list.

Check: `python3 math_check.py 12 32` -> 0 problems, 0 warnings, 0 layout problems. All 23 videos rendered and checked by
eye (tmp_check/pen12a–e.png).

## 2026-10-07 methods spread
Function `spread_methods` (runs last, after `pen_or_click`). Every guided and practice question was checked for the new methods; each line verified in Python (brute force on a grid). Nothing in topic 12 is recorded (checked ~/Documents/Course.recordings); the build also skips any video that gets recorded later.
- **Method 2 · The most precise range** (written line, 7 questions): q-324 (x = 7 ✓ kills 1; x = 0 ✗ kills 4; x = 10 ✗ kills 3), q-325 (x = 6 ✗ kills 1, 4; x = 0 ✗ kills 3 → "no value"), q-328 (x = 0 ✓ alone kills 2, 3, 4), q-r26-t12-02 (0 ✓, 3 ✗, −6 ✗), q-331 (x = 2, y = ½ fits → 1, 3 out; y = −½ never fits → 2 out), q-349 (m = −1 ✓ alone kills 1, 2, 4), q-352 (x = ⅛ ✓ alone kills 1, 3, 4).
- **Method 2 · Pick values that fit** (written line, 1 question): q-347 (x = ½ → y = ⅜ kills 1, 3, 4).
- **Extra video slides** "Method 2 · Test a number" (2 slides, ≈ 0.8 min): solve-q-325 (after "Split — and no overlap": x = 6 and x = 0 by click, cross-outs by pen) and solve-q-328 (after "Multiply by 10, then the rule", before the rule slide "Small side, big side": x = 0 by click, cross out 2–4).
- Skipped: already shown (q-322, q-r26-t12-13, practice lines of 2026-10-06), counterexample / plug-in questions that already list the fitting values (q-327, q-329, q-333, q-r26-t12-03, q-337, q-350, q-351…), counting and integer questions, corner-range questions (the four-corner check is the method).
`math_check.py 12 13 32`: PROBLEMS 0, WARNINGS 0, LAYOUT 0. Both extended videos rendered and checked.

## 2026-10-07 shaded number lines
Function `number_lines` (runs last; figure helper `math_patches/_shaded_nl.py`, same look as the topic-13 "within 4 of 2"
figure: teal band, open circle for < / >, full circle for ≤ / ≥, teal arrow for a ray). In each video: ONE click figure
+ ONE short spoken line, right after the range is found. Method, numbers and answers unchanged. A video recorded before
the cutoff in `_shaded_nl.CUTOFF` is skipped (never changed); none of these was recorded when this was made.
- solve-q-325 · "Split — and no overlap": the two rays x < 2 and x > 5 above the line, never meeting (+≈6 s).
- solve-q-328 · "Multiply by 10, then the rule": x² < 36 → one segment −6 to 6, open circles (+≈6 s).
- solve-q-r26-t12-13 · "Method 2 · Two moves": −1 < x ≤ 5, open circle at −1, full circle at 5 (+≈6 s).
- solve-q-331 · "Check the sign, then cancel": 0 < y < 1 (+≈4 s).
- solve-q-332 · "Method 1 · Two cases": the sign table − + − on the line, the two outer rays shaded (+≈7 s) - it
  shows the "sign table" the last spoken line already names.
- r26-t12-summary · "x² inequalities": two lines - x² < 25 (segment), x² ≥ 49 (two rays, full circles) (+≈6 s).
- Not added: solve-q-r26-t12-02 (the teacher already draws the sign-table line by hand there, and the slide is full),
  solve-q-335 (already has a number line), recorded videos (inequalities, inequality-systems, q-322 … q-324).
`math_check.py 12 13 17 32`: PROBLEMS 0, WARNINGS 0, LAYOUT 0. Renders: tmp_check/numlines/t12.png.


## 2026-10-07 trim added repeats

Teacher: only OUR additions that re-teach something learned earlier in the study plan are trimmed; the Hebrew course's own repeats stay. `trim_added_repeats(M)` runs last in apply(); helpers in `_trim_repeats.py` (videos with a take recorded before its CUTOFF are left as recorded). Notes updated in added_notes.json.

- r26-t12-signs shrunk to ONE content slide 'Reciprocals in inequalities' (same sign → flip, different signs → no flip) + one reminder line (between 0 and 1: topics 8, 3; must/could/cannot: topics 1, 21). Slides 'Between 0 and 1' and 'Must, could, cannot' removed; video renamed 'Reciprocals in Inequalities'; sidebar = the one slide. ~54 s saved.
