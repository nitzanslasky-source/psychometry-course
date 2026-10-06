# Topic 7 (Equations): changes (course review 2026-09)

Patch: `math_patches/t07.py`. `python3 math_check.py 7` gives 0 problems, 0 warnings and 0 layout problems.

## 1. Wrong statements fixed
- **Q16 video, Method 3, "Brainwave two"**: the old line said "each letter is bigger than the next". That is false for negative numbers. The new line says: all three ratios are bigger than 1, so their product x/w is bigger than 1.
- **q-214 solution**: rewritten cleanly (x ≤ 1 and y ≤ 1 give 4x + 3y ≤ 7 < 10, a contradiction). It now also shows why choices 2, 3 and 4 fail. Choice wording changed from "and/or" to "x > 1 or y > 1 (or both)".
- **Q20 video**: now says why "cannot be determined" is wrong: every allowed case gives a = 0. The first line changed from "Last question on equations" to "Last question in this set", because more questions follow now.

## 2. Methods added
**Main lesson "Solving Equations Smarter"** (9 slides before, 12 now, about 8 min):
- Slide 2: new habit "or check x = 0 separately".
- Slides 5, 6 and 9 (one equation with two unknowns, build the expression, break it apart): each one now has a worked mini-example on the board. The line "How do you know which one? Practice." was removed.
- **New slide "Which operation?"**, a checklist: mirror coefficients → add or subtract; a letter missing from the answers → make it cancel; products or ratios → multiply or divide; strange target → multiply one equation first; nothing fits → plug in.
- Slide "Hidden formula": now shows both (x + y)² and (x − y)², the rule "know two of x ± y, x² + y², xy → get the third", and a number example.
- **New slide "Plug in numbers"** with 4 rules: the numbers must fit all the givens; avoid 0 and 1; check all four choices; if two choices match, plug in again.
- **New slide "Try the choices"** (work back from the answers). It warns that a choice that works is one solution, not always the only one.
- The recap slide was updated.

**New lesson "More Equation Tools"** (end of Advanced study B, 2.6 min): multiplying or dividing equations, x + 1/x (and x − 1/x), and systems with no solution or infinitely many (parameter k).
- Guided Q21 (q-r26-t07-01) divides two equations. Guided Q22 (q-r26-t07-02) is x + 1/x = 3. Guided Q23 (q-r26-t07-03) asks which k makes a system have no solution. Each has a solution video.

**New lesson "Quadratic Equations"** (new section "Quadratic equations", placed after Advanced study B, 4.4 min). The whole course had no lesson on this before. Slides: standard form and "everything to one side"; factoring with "product c, sum b"; the zero-product rule gives two solutions, and the sign flips; special cases (no number term, no x term, the same two numbers → one solution, x² = −4 → no solution); **the trap a² = b² ⇒ a = b or a = −b**; try the choices; a fraction equals 0 (throw out solutions that make the denominator 0); recap.
- Guided Q24 (q-r26-t07-04): x² − 2x = 15, factoring, plus trying the choices. Guided Q25 (q-r26-t07-05): (x + 1)² = (x − 3)², the a² = b² trap, plus expanding. Guided Q26 (q-r26-t07-06): (x² − 7x + 12)/(x − 3) = 0, the extraneous solution, plus trying the choices. Each has a solution video with 2 methods.

**New memory card** "Equations: traps and shortcuts" (`mem-r26-t07-equations`), right after the main lesson. Topic 7 had no card before. It has three tables: Traps, Which operation?, and Quadratic equations (4 steps), plus tips.

## 3. Text
- Every question in the topic (33 existing ones) was rewritten in clean TeX. Examples: `$x^7 = x^6 y$` instead of `{x}^{7}`, and `\frac{a - 5b}{4}`, so the fraction in Q4 now shows correctly.
- Given equations are now stacked with `\begin{cases}` (18 questions).
- Colons used for division were removed from all solutions (q-180, q-184, q-189, q-199, q-204, q-208, q-212, q-217 and others) and from 3 draw notes (Q8 and Q17 videos). The real ratio question q-216 keeps ":" and says "ratio".
- "0 < m, n" became "m > 0, n > 0" (q-203). "0 < x, a" became "x > 0, a > 0" (q-204). "0 < x" became "x > 0" (q-211). "a, b, c, d ≠ 0" (q-186) and "m, n ≠ 0" (q-180) were written out one by one.
- q-203: choice 4 "m² − 2" was replaced with "−n", a trap that comes from m² = n².
- The one-line alg-extra solutions were written out step by step with numbers (for example t7-5-5: 2(x − 6) = x + 8 → x = 20).
- Solutions no longer use "so" to mean "therefore". Solutions that used plug-in or estimation now show those checks (q-181, q-184, q-190).
- In the videos, formulas are named instead of numbered ("the square of a sum", "the difference of squares"): Q11, Q15, Q18 and Q19. Q10 now says Method 1 is enough for the exam. Q14 explains why using 1s was safe there. American spelling ("math", "recognize"). ", so x is" became ". So x is".

## 4. Figures
- None in this topic.

## 5. Practice
- **Removed** the 7 clone items alg-extra-unit-t7-1-1 … 7 (copies of t7-5-x).
- The section "Additional source-bank variants" was renamed **"Retry set (same types as Questions 1–6)"** and keeps q-172 … q-177.
- **Added 15 practice questions** (q-r26-t07-07 … 21):
  - Quadratics: solutions of x² − 6x + 8, 2x² = 8x (the divide-by-x trap), x² = y² → |x| = |y|, (x² − 9)/(x − 3) = 0, x² − 10x + 25 (one solution), (2x − 1)² = (x + 4)² with x > 0.
  - x − 1/x = 4, and x² + 1/x² = 14 → x + 1/x.
  - Dividing equations (xy, yz → x/z), multiplying equations (xyz with three products).
  - Parameter systems: infinitely many solutions → k; infinitely many → a + b.
  - Plugging in on purpose: 4y from x = 2y + 3; xy in terms of k.
  - An estimation question (19/20 x = 38).
- Independent practice is now ordered easy → hard: the alg-extra warm-ups first, and q-215, q-208 and q-214 last. It has 42 items, about 15 of them exam-hard.

## Counts
- Questions: 40 of the 40 existing questions rewritten (text, TeX and solutions; all keys unchanged). 21 added (6 guided + 15 practice). 7 removed.
- Videos: 2 new lessons and 6 new solution videos. The main lesson has 6 slides rewritten and 3 slides added. 10 existing solution videos were edited directly (1 math fix, the rest wording and notation). All 20 got spelling and "so" fixes.

## Worked around the API / for the teacher to decide
- The API cannot create sections. The patch adds the section "Quadratic equations" by hand: it goes into `D['sections']`, into `M.sections` and into the topic's `sections` list, right after `equation-b`.
- The new guided questions are numbered 21–26 and sit at the end of the learn part, so the numbering stays in order. Please decide whether the quadratics lesson should move earlier. It fits well after Q7, but then "Question 24" would come right after "Question 7".
- The main lesson is now about 8 minutes long. If that is too long, "Plug in numbers" and "Try the choices" could become a separate short video.
- Existing solution-video titles are still the raw stem text (for example "Given: {x}^{7}…"). That is the base data, not something this patch changed. The "Q None" numbering shown on practice items comes from the renderer, not from this topic's data.
- T4/T5 practice uses quadratics before this lesson (see PLAN.md). Those topics may want a pointer to T7, or the quadratics lesson could move earlier in the course.

## Pass 2 (teacher-approved remove/restore plan, 2026-09-27)
**Removed**
- `r26-t07-more-tools`: slide "Solutions of a system" and its sidebar entry; the title slide now says "Two more tools … multiplying or dividing equations, and the famous x plus one over x"; recap line "Same left side: different right → none; same → infinitely many" removed; "Three questions now" → "Two questions now".
- Guided q-r26-t07-03 (parameter k, no solution) and `solve-q-r26-t07-03`. The quadratic guided questions are renumbered 23–25 (title slides, sidebars, spoken "Question twenty-three…").
- Practice q-r26-t07-17 and q-r26-t07-18 (removed from the `unit-t7-5` order).
- Card `mem-r26-t07-equations`: tip "Two equations: make the left sides equal…".

**Restored**
- alg-extra-unit-t7-1-1 … -1-7 back in `unit-t7-1`, original position, text cleaned (TeX, stacked givens, numeric solutions). Section title back to "Additional source-bank variants".
- q-203: original choice 4, $m^2 - 2$.
- `equation-strategy` slide 6: board line "Add, subtract — or divide — the equations" and the two spoken lines (practice, recognize the patterns); the new example stays. Slide 8: "See x minus y, x squared plus y squared, and x times y together? That's this formula…" and "Find the right formula, plug in what you know, and isolate what they ask for." Recap: "Asked for an expression? Build it directly — use the checklist".

**Summary video (new)** `r26-t07-summary` "Equations: Summary", at the end of the Quadratic equations section, right before the practice: Summary · Don't divide by x · Plus AND minus · Quadratics · Fraction = 0 · Build the expression · Hidden formulas · Two unknowns · Plug in or try · Before you practice.

## 2026-10-02 new numbers + order
Goal: the English topic is clearly not a copy of the Hebrew course. Every method, tip and trap stays, and so does the psychometric style. Nothing in topic 7 is recorded (both functions have a `RECORDED = set()` guard).

**New numbers** (`new_numbers`). Every number was re-checked in python, and every solution video was rewritten to match its question (board, spoken numbers, choice numbers, title).
- Lesson `equation-strategy`: the Hebrew's own examples are replaced: x³ = x²y → p³ = p²q; x⁴ − 9x² → x⁴ − 49x²; (x − 6)² = 16 → (x − 2)² = 36 (also on the "Try the choices" slide). The mirror coefficients are now 3x + 8y, 8x + 3y, and the slide says "multiply by four" (as in Q14). The plug-in rules now use the new Q17 and Q18. Board text and lines that were word-for-word translations are reworded (slides 5, 6, 8 and 9). The memory card uses the same examples.
- Guided Q1–Q20 (q-178 … q-197) all have new numbers or letters. Q11 has a story tweak: "square of the difference = sum of the squares". Where the correct choice was in the same position as in the Hebrew course, it has moved. The one exception is q-186: its key stays 4 so the tip "three are gone, so mark the fourth" still works.
- Self-practice q-198 … q-217 and the variants q-172 … q-177 all have new numbers, and their answer positions are mixed. None of them duplicates a guided question.

**Order** (`order_changes`)
- Lesson: "Break it apart" now comes before "Hidden formula" (right after the "Which operation?" checklist). Guided q-197 now comes before q-196. The lines "The last type" and "Last question of the set" were updated, and the question numbers update automatically.
- Advanced A: q-187 (the word problem, medium) now comes before q-186 (the proportion, medium). Both have the same Hebrew level.
- Rejected: moving q-188 earlier (it starts the 188–189–190 block of equation-combining questions). Swapping q-179 and q-180 in Advanced B (q-180 leads straight into q-181). Swapping q-182 and q-183 (q-183 is the closing "understanding" question). Reordering the first theory questions (each one matches a lesson slide).

## 2026-10-02 review
- Fixed q-179: the Hebrew has only ONE choice > 1. In the new version, 9 also passed the "x/w > 1" test. Choice 4 is now 1/9, so the brainwave removes choices 1, 3 and 4 and leaves choice 2, as in the Hebrew. The solution and video slide 4 were updated.
- Judged and kept: q-187 ("square of the difference = sum of the squares"). It has the same message: translate the words, expand a multiplication formula, get 2ab = 0, so one number is 0. It is still medium, with the same choices and the same key idea. Also kept: q-175 (now a < b). It is a variant practice item and the skill is unchanged. Its guided twin q-194 keeps the b < a direction, so both directions are practiced.
- Checked with no changes needed: all the theory and advanced A/B guided questions against the Hebrew levels and methods (estimation in q-184, three negatives and "mark the fourth" in q-190, the three methods in q-178, and the distinct plug-in values in q-180 and q-181), the lesson back-references (Questions 6, 14, 15, 16–18), and about 30 practice questions.


## 2026-10-04 question = lesson example fixed
- Lesson "r26-t07-more-tools" slide 3: the example x + 1/x = 3 (same as q-r26-t04-04, whose video is recorded, and q-r26-t07-02) -> x + 1/x = 5, so x² + 1/x² = 23 (board, spoken line, label).
- q-r26-t07-02 -> x + 1/x = 6, answer 34 (choice 2); choices 36, 34, 38, 32; solution video "solve-q-r26-t07-02" updated (board, words, draw cues).
- Lesson "r26-t07-quadratic" slide 6: the example (x + 1)² = (x − 3)² (same as guided q-r26-t07-05) -> (x + 3)² = (x − 1)², x = −1. Question and its video unchanged.
- q-r26-t07-10 was (x² − 9)/(x − 3) = 0 of the same lesson, slide 8 -> (x² − 36)/(x − 6) = 0, x = −6 (choice 2).
- q-r26-t07-15 was xy = 12, yz = 6 of "r26-t07-more-tools" slide 2 -> xy = 24, yz = 8, x/z = 3 (choice 1).


## 2026-10-05 pen vs clicks trial
"Pen for the thinking, clicks for the copying" (function `pen_or_click`, runs last). Copied / mechanical lines now appear on NEXT as board items at the same moment; the key idea and all marks (circle, underline, tick, cross out, short notes beside an item) stay as pen cues. Where a hand-written line comes before a click line, the board leaves an empty row for it. Spoken lines, math, questions, slide count and sidebars are unchanged.
- equation-strategy (18 -> 12 by hand, 6 clicks). Clicks: p = 0 or q = p; "Or: check p = 0 separately"; x² = 0 -> x = 0; x² = 49 -> x = 7 or x = −7; x = 8 or x = −4; the xy = 12, yz = 6 -> x/z = 2 example on "Which operation?". By hand: p = 0 -> 0 = 0, p²(p − q) = 0, x²(x² − 49) = 0, circle the three values, x − 2 = ±6, all underlines / brackets / circles / ticks, "b > a in every case", the "+" line under the system.
- solve-q-191 (5 -> 3 by hand, 2 clicks). Clicks: m = 2: 32 = 16n -> n = 2; m⁴(m − n) = 0 -> m = 0 or n = m. By hand: m = 0: 0 = 0 · n, cross out m⁴ + "only if m ≠ 0", circle choice 4.
- solve-q-192 (4 -> 2 by hand, 2 clicks). Clicks: x² = 0 -> x = 0; x² = 25 -> x = ±5. By hand: x²(x² − 25) = 0, circle.
- solve-q-193 (3 -> 2 by hand, 1 click). Click: x = 5 or x = −13. By hand: x + 4 = 9 or x + 4 = −9, circle.
- solve-q-194 (4 -> 2 by hand, 2 clicks). Clicks: ×5: a − 6b = 5 − 5b; a − b = 5 > 0. By hand: a = 5 + b, circle.
- solve-q-195 (3 -> 2 by hand, 1 split). By hand: 13x + 13y = 65, 13(x + y) = 65. Split: x + y = 5 is a click, circling choice 2 by hand.
- solve-q-197 (4 -> 2 by hand, 1 click, 1 split). By hand: (a + b) + (2a + c) + (b + c) + c and the values 4, 7, 8 under the brackets. Click: 4 + 7 + 8 + c = 24. Split: 19 + c = 24 -> c = 5 click, circle by hand.
- solve-q-196 (4 -> 2 by hand, 2 clicks). Clicks: (x − y)² = x² + y² − 2xy; 2xy = 36 -> xy = 18. By hand: 7² = 85 − 2xy, circle.

## 2026-10-05 lesson back to the Hebrew short intro
Function `hebrew_intro` (runs last). The Hebrew section "Equations — theory" has no long lesson: it opens with a short intro (about 1 minute) and then teaches each idea inside its own question video. Nothing in topic 7 is recorded.
- **`equation-strategy`** (same id, same place, same title "Solving Equations Smarter"): 12 slides, 8.9 min → 2 slides, 0.6 min. Title slide: "In this section: different techniques for solving the equations we get on the exam. Each question that follows teaches one of them." One concept slide, "Dividing by an unknown": same operation on both sides is allowed; divide both sides by x only if x ≠ 0; if x = 0, you divide by 0, and that is undefined; "Let's see it in the questions." The sidebar is now just "Dividing by an unknown". Removed slides: dividing by x (worked example), product = 0, squares, one equation with two unknowns, build the expression, which operation, break it apart, hidden formula, plug in numbers, try the choices, recap.
- **Ideas now taught in the question videos** (only where they were missing):
  - Q1 `solve-q-191` (slide 3): ADDED the line "The rule for a power of two and up: take out a common factor. You get a product equal to zero — and then at least one factor is zero." with the board item "Power 2 and up: common factor → product = 0", right before the factored line. "Factor instead:" → "Here:". 1.2 → 1.4 min.
  - Q5 `solve-q-195` (slide 2): ADDED "They ask for an expression? Build it straight from the equations — add them or subtract them." with the board item "Asked for an expression? Add or subtract the equations" (the space for the hand-written lines stays under it). 0.8 → 1.0 min.
  - Already taught, unchanged: Q2 `solve-q-192` (common factor; a product = 0 → one factor is 0), Q3 `solve-q-193` (root in an equation → plus or minus), Q4 `solve-q-194` (one equation, two unknowns → we can compare, not find), Q6 `solve-q-197` (break the big equation into the small ones), Q7 `solve-q-196` (hidden formula (x − y)² = x² + y² − 2xy on the board).
- "Plug in numbers" and "Try the choices" are not added back (taught in topics 5 and 51). No topic 7 video said "as we saw in the lesson", so no reference needed rewording.
- Memory card `mem-r26-t07-equations` stays as the written summary (its examples p³ = p²q and (x − 2)² = 36 are now only on the card).
- For the teacher: the AI summary video `r26-t07-summary` does not mention the lesson by name. Its slides "Build the expression" (mirror coefficients / missing letter / products or ratios) and "Plug in or try" sum up ideas that the removed lesson slides taught. Mirror coefficients, the missing letter, and products or ratios are still taught in Q5, Q12–Q14 and "More Equation Tools". Plug-in and try-the-choices come from topics 5 and 51. No change was made.

## 2026-10-05 cut repeats
Function `cut_repeats` (runs last, after `hebrew_intro`). Same approach as equation-strategy: a lesson slide is cut only where a question video in the same section teaches the same idea. Nothing in topic 7 is recorded.
- **More Equation Tools** (1.8 → 0.4 min): title + one "What's ahead" slide (the two tools named, "try each one before you watch"). Cut: multiply or divide the equations → Q21; x + 1/x → Q22; recap.
  - Moved into Q22 (new short slide "With a minus"): "(x − 1/x)² = x² + 1/x² − 2 — the middle term is minus two, then add two."
- **Quadratic Equations** (4.4 → 1.4 min): kept "What it looks like" (standard form, divide out a common number) and "Special cases" (no number term, no x term, a perfect square → one solution, x² = −4 → none). The perfect-square case is now said as "a perfect square: (x − 3)²" (it used to lean on the cut factor slide). Ends with "Three questions now. Each one teaches one more tool."
  - Cut: factor (product c, sum b) → Q23; two solutions / sign flip → Q23; the trap a² = b² → Q24; try the choices → Q23 method 2; fraction = 0 → Q25; recap.
  - Moved into Q23: board item "One side = 0, then factor: product = c, sum = b" + one line, before the first written line; and in method 2 "A choice that works is ONE solution. How many? Factor." + one line.
- Q23 1.2 → 1.6 min, Q22 0.8 → 1.0 min. Card and AI summary unchanged.


## 2026-10-06 practice: new methods
Function `practice_methods` (runs last, after `cut_repeats`; append only). 8 practice questions.
- Method 2 · Power count: q-212 (x + y in terms of a, c): choice 1 power −1, choice 4 mixed → out; x = y = 1 (a = c = 11) decides → 2.
- Shortcut: pick values that fit: q-206 (y = 2 → x = 3 → 3/2), q-175 (a = 0 → b = 6; one fitting pair knocks out choices 2–4), q-202 (m = 1 → n = 0), q-172 (a = 1 ties choices 1, 2, 4; second set a = 0, b = 7 → cannot be determined), q-r26-t07-15 (y = 1 → 24/8 = 3), q-199 (x = 1 → x + y = 1/4), q-204 (a = 1 → x = 1/2).
All new lines verified numerically (python: fitting values, choice values, power by scaling). `math_check.py 7 32`: PROBLEMS 0, WARNINGS 0, LAYOUT 0.


## 2026-10-06 pen or click
Function `pen_or_click_rest` (new, runs LAST via a final `apply` wrapper, after `cut_repeats` and `practice_methods`, because `cut_repeats` adds board items to Q21–Q25). The earlier `pen_or_click` (equation-strategy, solve-q-191..197, all recorded) is left exactly where it was, before `hebrew_intro`, since `_add_rule` relies on the room it leaves. Approved rule: setup and mechanical lines appear on click; by hand only the one or two key steps + marks on the choices; no long text by hand. Spoken lines unchanged (none said "write …"). The 18 unrecorded solution videos with pen cues: 120 pen cues → 54 by hand, 48 by click, 18 split (click line + hand mark). Lessons more-tools / quadratic / summary had no pen cues.
- Q8 solve-q-184 (10 → 5 hand, 4 click, 1 split). By hand: "×12" next to each side, cancel 33 with 11, cross out 2 and 3, "too big" on 4, circles. Clicks: 33·12 − 8x = 3x, 33·12 = 11x, x = 3·12 = 36, 33 = ¼x + ⅔x = 11/12 x, 33 ÷ 11/12 = 36.
- Q9 solve-q-185 (5 → 2 hand, 1 click, 2 split). By hand: x²(x + 3) = πx² (with room), cross out x², "x, 3, π" under the terms. Clicks: x + 3 = π, x = π − 3, x + 3 = π → x = π − 3.
- Q10 solve-q-187 (5 → 2 hand, 1 click, 2 split). By hand: the translation (a − b)² = a² + b², cross out a² and b². Clicks: the expansion, −2ab = 0, a = 0 or b = 0.
- Q11 solve-q-186 (8 → 3 hand, 5 split). By hand: ps = qr next to the question, the diagonal arrows on 2/3 = 4/6, circles. The four choice checks ("sp = qr ✓"… "pr = qs ✗") are now click lines (1)–(4) on the board + cross out / circle by hand (no more writing ps = qr three times). "diagonal ÷ leftover" is a click line "Isolate a letter: diagonal product ÷ the one left" + tick choices 1 and 3 by hand.
- Q12 solve-q-188 (3 → 2 hand, 1 click). By hand: eq1 + eq2: 4x + 3z = 22. Click: −(3x + 3z = 18) → x = 4.
- Q13 solve-q-189 (5 → 3 hand, 2 click). By hand: the coefficient sums 3⅕ + 4⅘ = 8 and 5¼ + 2¾ = 8 under the terms. Clicks: 8x + 8y = 2a + 2b, 8(x + y) = 2(a + b) → (a + b)/4.
- Q14 solve-q-190 (7 → 4 hand, 3 click). By hand: 4a + 4b + 4c = 4x, the choice signs, circles. Clicks: a + 2b = 4x − z, a = b = c = 1 → x = 3, z = 9, a + 2b = 3.
- Q15 solve-q-178 (12 → 3 hand, 6 click, 3 split). By hand: (a − b)(a + b) = 65, circles. Clicks: a − b = 5, a² − b² = 65; 5(a + b) = 65; a + b = 13; the three trials 7,2 / 8,3 / 9,4; the three choice checks (1)–(3) (were long notes next to the choices) + cross out 1 and 2 by hand.
- Q16 solve-q-179 (9 → 3 hand, 4 click, 2 split). By hand: y = 4z → x = 12z, cancel y and z, cross out / circles. Clicks: x = 3y, z = 2w → x = 24w, x/w = 24, the chain w = 1 → … → x = 24, the product of the ratios, = 3·4·2 = 24. (Slide 2 in size 36: the stem is tall.)
- Q17 solve-q-180 (6 → 4 hand, 2 click). By hand: q = 1/p, the choice values, circles. Clicks: q/p = (1/p) ÷ p = 1/p², q/p = ½ ÷ 2 = ¼.
- Q18 solve-q-181 (9 → 4 hand, 5 click). By hand: (2x)² = (y + 3)², the choice values, circles. Clicks: 4x² = y² + 6y + 9, 4x² − y² = 6y + 9, ÷2 line, y = 1 → x = 2, 2·4 − ½·1 = 7.5.
- Q19 solve-q-182 (9 → 4 hand, 5 click). By hand: 2ab = −6 → ab = −3 (opposite signs), 9x² − 6xy + y² = (3x − y)², circles. Clicks: the expansion, a = ±3, b = ±1, the two pairs → 4, a = 3, b = −1 → 4.
- Q20 solve-q-183 (4 → 1 hand, 2 click, 1 split). By hand: "≥ 0" under the two terms. Clicks: 4a² + 8b² = a², 3a² + 8b² = 0, a = 0, b = 0 (+ circle).
- Q21 solve-q-r26-t07-01 (4 → 2 hand, 1 click, 1 split). By hand: x²y ÷ xy² = 18 ÷ 12, cancel x and y, circle. Clicks: x/y = 18/12 = 3/2, the number check.
- Q22 solve-q-r26-t07-02 (4 → 2 hand, 2 click). By hand: (x + 1/x)² = 36, circle. Clicks: the expansion, x² + 2 + 1/x² = 36 → 34.
- Q23 solve-q-r26-t07-04 (6 → 3 hand, 3 click). By hand: the two numbers (−5)·3 = −15, (−5) + 3 = −2; the choice values; circle. Clicks: x² − 2x − 15 = 0, (x − 5)(x + 3) = 0, x = 5 or x = −3.
- Q24 solve-q-r26-t07-05 (7 → 2 hand, 4 click, 1 split). By hand: the second case "x + 1 = −(x − 3)" (with room), 8x = 8 → x = 1 (method 2), circle. Clicks: the trap line, a² = b² → a = b or a = −b, x + 1 = −x + 3 → 2x = 2 → x = 1, the check, the expansion.
- Q25 solve-q-r26-t07-06 (7 → 5 hand, 2 click). By hand: "bottom = 0 ✗" next to x = 3, the three short notes next to the choices, circle. Clicks: x² − 7x + 12 = 0, (x − 3)(x − 4) = 0 → x = 3 or 4.
`math_check.py 7 32`: PROBLEMS 0, WARNINGS 0, LAYOUT 0. All 18 videos rendered and looked at.
