# Topic 19 — Defining a New Operation: changes (course review 2026-09)

Check: `python3 math_check.py 19` gives 0 problems, 0 warnings and 0 layout problems.

## 1. Wrong or weak rules fixed
- **Lesson 1, "Operation first":** the slide said a new operation comes "before powers, times, divide — only brackets beat it". That is not a real rule. It now says: "First turn every ◆(…) into a plain number, then do the rest as usual." It also says that on the exam, an operation between two numbers (a★b) inside a longer exercise always comes with brackets. The recap line and the memory card row were changed to match.
- **Q13 (q-553), method 2 ("the insight"):** the old argument ("same power on both letters → a/b or b/a") could not pick between a/b and b/a. Now: the squared tops are equal and cancel, so the ratio is (b²a)/(a²b) = b/a in one line.
- **Q12 (q-552), method 2:** "Some students stop right here. Why?" was removed. Now: "Only choice 2 has 13 on top — a strong hint, but one more line makes it sure." Then the bottom is calculated.
- **Q15 (q-555):** "A negative power flips floors" (slang from T11) is now "Dividing by a fraction is multiplying by its reciprocal". "NECESSARILY true" is now "MUST be true".
- **q-567 (was ambiguous):** it is now defined only for positive integers. Choice 2, "x~0 = 10x", used y = 0 and became "x~1 = 10x + 1". The key is unchanged (choice 4). The unclear sentence "Repeated inputs and appending 0 are allowed" was removed.
- **Q9 (q-549) and Q16 (q-556) videos:** both plug in x = 1. Each video now says that 0 and 1 can make a false rule look true, and why it is safe here (only one choice survives). If two choices survived, you would try a second number.

## 2. Methods added
**Lesson 1 (Defining a New Operation), now 11 slides:**
- New slide 5, **"Brackets on every input"**: ◆(x) = x² − 2x with ◆(−3) = 15 and ◆(x+1) = x² − 1. It shows the no-brackets trap crossed out.
- Slide 9, **"Order can matter"**: to say "not always", one counterexample is enough. To say "always", swap the letters in the algebra. Never test with equal values. It also teaches the habit of circling which number goes in which slot.
- Slide 10, **"Unknown input"**: it now also shows how to work back from the answers.
- The recap and sidebar were updated. The video now says "Five questions next".

**Lesson 2 (Operation Patterns), now 9 slides.** Every board has a small worked example, which the weak student needed:
- Conditions: the piecewise definition written as `cases`, with ◆(3) = 6 and ◆(4) = 9.
- **New: "Conditions backwards"** (◆(x) = 9). Try both rules and reject the answer that does not fit its own rule (4.5 is rejected, 4 is kept), or work back from the answers.
- Circular: a full example going down and back up (◆(3) = 12).
- Isolate: the example 2◆(x) + 1 = ◆(x) + x, so ◆(x) = x − 1.
- **New: "Definition in words"**: the integer part [x], with [3.7] = 3, [5] = 5 and [−2.3] = −3 (the trap). It also lists other word definitions (remainder, divisors, digit sum). The rule: write examples first.
- **"Must be true?"** (was "Necessarily true?"): linked to Topic 1's must/could/cannot. It includes plug-in rules: use 2 or 3 and avoid 0, 1 and equal values, with a live example where 0 fools you. If two choices survive, try a second number.
- New 7-line recap and new sidebar.

**5 new guided questions, each with a 2-method solution video:**
| New no. | id | Method taught | Answer |
|---|---|---|---|
| Q4 | q-r26-t19-01 | ◆(x+1) with brackets; plug-in where x = 0 leaves two choices, so try x = 2 | x² − 1 (choice 2) |
| Q5 | q-r26-t19-02 | Which a★b is always commutative: counterexample, then swapping letters | ab + a + b (choice 3) |
| Q8 | q-r26-t19-03 | Solve ◆(x) = 24 with odd/even rules, rejecting x = 8 | 6 (choice 2) |
| Q12 | q-r26-t19-04 | Integer part [−2.5] + [2.5] + [0.5] | −1 (choice 3) |
| Q16 | q-r26-t19-05 | ◆(2) − ◆(−2): only the odd powers survive, doubled (and ◆(k) + ◆(−k): only the even ones) | 48 (choice 3) |

Guided questions are renumbered automatically. The topic now has 21 guided questions: 13 in the theory section and 8 in the advanced section. Sidebars and spoken "Question N" lines were updated. Solution-video titles now follow the rewritten stems.

**Memory card** rewritten with 15 rows. New rows: negative/expression input, inside an exercise, unknown input, always a★b = b★a?, conditions with the result given, definition in words, ◆(k) − ◆(−k), and must be true. New tips: plug-in dangers, and "necessarily = must (Topic 1)".

## 3. Text (all 36 existing questions)
- Every stem, choice and solution is now in TeX. There are no ":" divisions (q-544, 553, 555, 561, 563, 565, 572, 573, 574 used them) and no commas without a space.
- Piecewise and circular definitions are stacked as `cases`: q-545, 546, 547, 565, 569. The two definitions in q-551 and q-570 are stacked, and so are q-558's two lines.
- q-546: "non-negative even x, x > 1" became "even x ≥ 0 … x ≥ 2" (same meaning, clearer).
- q-553: "(x ≠ y, both nonzero)" is now a sentence.
- q-570: choice "−1/2" is now written −½ properly.
- q-571: choice "x" is now TeX.
- "Necessarily true / not always correct" became "must be true / not always true" (Q9, Q15, Q16, q-573, q-574).
- The extra questions' word-style solutions ("two plus three plus six is eleven") now use numbers and symbols. Their stems are in NITE style ("3★5 = ?"), and extra-5 now stacks its two given equations.
- The draw note "(1/2) : (1/4)" in the Q13 video is now "÷".

## 4. Figures
- None in this topic.

## 5. Practice (unit-t19-3)
- **Removed 2 near-duplicates:** extra-3 (F(F(2)), which repeats Q2) and extra-6 (H(H(4))). Nested questions were over-represented.
- **Added 12 questions** (q-r26-t19-06 … 17):
  - ◆(−2) with the bracket trap
  - ◆(x−1) with answers in x
  - ◆(1/x) (exam-hard)
  - find the operation from two given values ("could be")
  - an odd/even rule applied 4 times
  - "for how many integers is ◆(x) = 4?" with two branches (exam-hard)
  - a circular rule with ×3 − 2
  - a period-3 operation, 1/(1−x) (exam-hard)
  - [x] = 3: which x could it be
  - two-digit numbers with digit sum 5
  - a★b = ab − a − b "must be true" (a = 0 trap)
  - ◆(x) = x³ must-be-true, where x = 0 fools you and x = 1 leaves two choices (exam-hard)
- The practice set now has 37 questions (was 27), ordered easy → hard. The easy extras come first, and q-573 and q-574 come last. Find-the-operation, conditions (including solving backwards), circular, word-definition and expression-input questions are now all practised.

## For the teacher to decide
- **Integer-part notation.** I used `[x]`, the usual exam notation. q-556 already uses ⟦x⟧ for another word definition.
- **q-562 and q-575.** They are really equation questions with a ◆ label. I kept them as mix practice, as the review allows.
- **q-556's ⟦ ⟧ brackets** are plain characters around TeX, as before. The API has no TeX double-bracket that is known to render safely.

## Pass 2 (2026-09-27, teacher-approved remove/restore plan + summary lesson)
**Removed (the integer part [x] — not on the exam, not in the original course):**
- Video "Operation Patterns", slide "Definition in words": the [x] boards, the "= −3, not −2" note and the spoken lines about [x]. The rule ("write 2–3 examples first") and the remainder / number of divisors / digit-sum examples stay (now on the board too).
- Memory card: the [x] example in the "Definition in words" row (now the remainder example $47=5\cdot9+2$ from q-576).
- Guided question q-r26-t19-04 ($[-2.5]+[2.5]+[0.5]$) and its solution video. Guided questions renumber automatically (the advanced section is now Questions 13–20).
- Practice q-r26-t19-14 ($[x]=3$).
- Kept as the plan says: "Conditions backwards" slide and card row, q-r26-t19-03 + video, practice q-r26-t19-11.

**Restored (2):** alg-extra-unit-t19-3-3 ($F(F(2))$ with $F(x)=x^2-3$, answer $-2$) and alg-extra-unit-t19-3-6 ($H(H(4))$ with $H(x)=\frac1x$, answer $4$), cleaned up (TeX, numeric solutions), at the easy end of the practice.

**Summary lesson (1 new video):** `r26-t19-summary` "Summary", at the end of "Defined operations · advanced study", right before the independent practice. Slides: Summary · Read, then substitute · Brackets on every input · One step at a time · Match the whole input · Missing pieces · Conditions · Circular · both sides · Always? Must? · Before you practice. Only content the Topic 19 lessons teach.

## 2026-10-01 elite comparison

Teacher-approved addition: **property questions** — the question gives a property, not a definition, and four candidate rules. Targets the real exams 2020 autumn I-9, 2023 spring I-20, 2024 winter II-20, 2022 autumn II-14, 2024 autumn I-18 (2021 spring I-8 is solved by the existing "set them equal" skill).

- Video "Operation Patterns": three new slides before the recap (type seven):
  - **Property questions**: put each rule on trial with a test value (not 0 or 1: 1² = 1 fools you). ◆(◆(x)) = x: x² gives 3 → 9 → 81 ✗, 10 − x gives 3 → 7 → 3 ✓. Step property ◆(x + 1) = 3 · ◆(x): test two neighbors (3x: 6, 9 ✗; 3ˣ: 9, 27 ✓).
  - **Rules that undo themselves**: the families c − x (also −x) and c/x (also 1/x = x⁻¹); never x², √x, 2x, x + 5.
  - **Inverse operation**: undo the steps in reverse order (◆(x) = 2x + 3 → #(y) = (y − 3)/2), check with a number; the trap undoes them in the wrong order.
  - Recap: new line "Property? Put each rule on trial · inverse: undo in reverse order". Sidebar updated. The video is now about 6.8 minutes (was 4.5).
- Memory card: three new rows (Property given, Undoes itself, Inverse operation).
- New guided question **q-r26-t19-18** (end of the theory section, after q-549) with solution video (Method 1 trial with x = 2, Method 2 know the family). ◆(◆(x)) = x: which rule? Answer: choice 4 (6/x).
- New practice **q-r26-t19-19** (after q-r26-t19-09): ◆(x + 1) = ◆(x) + 3 → choice 2 (3x); trap x + 3.
- New practice **q-r26-t19-20** (after -19): inverse of ◆(x) = √x + 4 → choice 2 ((y − 4)²); trap y² − 4 (wrong order).
- Summary video: new slide "Property questions" after "Missing pieces"; sidebar updated.
- All three questions solved by computer: exactly one correct choice each.


## 2026-10-04 question = lesson example fixed
- Lesson "new-operation" slide 5 worked out ◆(x + 1) for ◆(x) = x² − 2x (same as guided q-r26-t19-01) -> the lesson now does ◆(x + 2) = x² + 2x (same trap). Question and its video unchanged.
- Checked and left: q-545 and q-542 share a definition with a lesson but ask a different question.

## 2026-10-05 cut repeats
Function `cut_repeats` (runs after `dedupe_examples`). Nothing in topic 19 is recorded. "Defining a New Operation" is unchanged.
- **`operation-patterns` "Operation Patterns"**: 6.8 → 1.0 min. Each type is taught by the question right after it. Kept: the title (now "Each question that follows shows one type…") and "Inverse operation" (only the practice has it).
  - Cut "Operation on an expression" → Q6 `solve-q-544`. "Conditions" → Q7 `solve-q-545`. "Conditions backwards" → Q8 `solve-q-r26-t19-03`. "Circular rules" → Q9 `solve-q-546`, Q10 `solve-q-547`. "Isolate the operation" → Q11 `solve-q-548`. "Must be true?" → Q12 `solve-q-549` (skip first, plug in, avoid 0 and 1, second number). "Property questions" and "Rules that undo themselves" → Q13 `solve-q-r26-t19-18`.
  - The step property (◆(x + 1) = 3 · ◆(x): test two neighbors; used in practice `q-r26-t19-19`) → one line + board item in Q13.
  - "Definition in words" (write 2–3 examples first; used in practice `q-576`, `q-r26-t19-15`) → one line + board item in Q21 `solve-q-556`.
  - Cut "Recap".
- Card `mem-new-operation` unchanged (it still lists every type).

## 2026-10-06 renumber pass
So the English course does not look like the Hebrew one: every Hebrew-derived question and lesson example has new numbers
(and, where it fits, a new rule number, prime, digit set or letter). The rule's structure, the kind of question
(evaluate / nested / find the rule / inverse input / circular / both sides / must be true …), the trap, the level and the
methods stay the same; every guided solution video is rewritten to match (speech, draw cues, video title, slide description).
Nothing in Topic 19 is recorded, so nothing had to be kept as it was. Function `renumber_pass(M)` in t19.py runs last
(after `cut_repeats`).

**Counts:** 16 guided questions renumbered (q-541 … q-556) with their 16 solution videos rewritten; 20 practice questions
renumbered (q-557 … q-576); lesson "Defining a New Operation": 7 slides of examples renumbered (slides 2, 3, 6, 7, 8, 9, 10);
memory card: 12 example cells + 1 tip. Practice: 40 → 27.
Kept on purpose: the English-made items (guided q-r26-t19-01, -02, -03, -05, -18; the brackets slide ◆(x) = x² − 2x; the
inverse-operation slide; the summary video) keep their numbers. The lesson's "Operation Patterns" Hebrew examples were already
cut earlier (cut_repeats), so nothing left to renumber there.

**Practice clean-up (40 → 27):**
- Copies removed: alg-extra-…-3 (F(F(2)), nested-and-stop-halfway = guided Q2, q-559, q-560), alg-extra-…-6 (H(H(4)) with 1/x =
  the "c/x undoes itself" idea of guided Q13).
- Extra warm-ups kept (3): X1 (a⋆b = 2a − b), X5 (G(t) = 19, unknown input), X7 ((−2)∘3, brackets on a negative). Removed X2, X4.
- September items kept (4, types the Hebrew practice does not have): -07 (expression input ◆(x − 1)), -11 (conditions
  backwards: how many x give 4), -19 (step property), -20 (inverse operation). Removed -06, -08, -09, -10, -12, -13, -15, -16, -17
  (each type already practised by a Hebrew item or a guided question — see the comments in `rn_practice`).
- 27 instead of the audit's 25 so that expression input and conditions-backwards each keep one practice item.

**Checks:** every key brute-forced in Python (exactly one correct choice; for must/always questions every wrong choice has a
counterexample and the right one holds over a range of values); every step and plug-in in the videos recomputed; the original
traps are still choices (stop halfway, number straight into x, odd rule on an even number, forgetting the outer root, etc.).
Duplicate scan over a build of topics 1–19 (stems, choices, lesson boards/draw cues/speech, cards): no new question equals
another question or a lesson/card example (only incidental sub-expressions like x² − 9 in other topics). No new quadratic
trinomial (q-570 and q-575 keep the original's (a + k)² / product expansion). `python3 math_check.py 19 32` → 0 / 0 / 0.
Rendered the lesson and the solution videos q-541, -543, -545, -546, -549, -552 … -556 and looked at them.

| id | old (Hebrew) | new | answer |
|---|---|---|---|
| q-541 (G1) | ◆(a) = a² − 2a, ◆(5) | ◆(a) = a² − 4a, ◆(6) | 12 (2); traps 36 = a² only, 24, 60 |
| q-542 (G2) | ◆(x) = x², ◆(◆(2)) | ◆(◆(3)) | 81 (3); trap 9 = stop halfway |
| q-543 (G3) | ◆(2) = 10, which cannot (x³+2, 4x+3, x(2x+1), 6x−2) | ◆(3) = 21 (x³−6, x(x+4), 5x+5, 8x−3) | 5x + 5 (3) |
| q-544 (G6) | ◆(3x) = x + 4, ◆(12) | ◆(2x) = x + 5, ◆(14) | 12 (1); trap 19 = 14 straight into x |
| q-545 (G7) | odd 2x / even x² − 7, ◆◆◆(5) | odd 2x / even x² − 3, ◆◆◆(3) | 66 (3); trap 33 = one step short, 12 = odd rule on 6 |
| q-546 (G9) | ◆(0) = 0, ◆(x) = 7 − ◆(x−2), ◆(6) | ◆(0) = 2, ◆(x) = 9 − ◆(x−2), ◆(6) | 7 (3); pattern 2, 7, 2, 7 |
| q-547 (G10) | ◆(1) = 6, ◆(x) = ◆(x−1), ◆(5) | ◆(1) = 9, ◆(7) | 9 (4); trap 7 = the input |
| q-548 (G11) | 3◆(x) − 4x = 10 + 2◆(x), ◆(3) | 5◆(x) − 3x = 8 + 4◆(x), ◆(4) | 20 (2) |
| q-549 (G12) | ◆(t) = t², not always: ◆(3x) = 3◆(x) | ◆(5x) = 5◆(x); also ◆(3x) = 9◆(x), ◆(x−2) = ◆(2−x) | (3) |
| q-550 (G14) | ◆(1, 1, ◆(1, 2, 2)) | ◆(1, 1, ◆(2, 1, 3)) | 20 (3); trap 18 = inner only |
| q-551 (G15) | #(◆(9, 6), ◆(8, 6)) | #(◆(10, 6), ◆(5, 4)) | 289 (2); choices 16², 17², 18², 19² |
| q-552 (G17) | √(3x² + y²), √(13/7) | √(8x² + y²) | √(73/17) (3); trap √(17/73) = slots swapped |
| q-553 (G18) | (x − y)²/(x²y), b/a | (x − y)²/(xy³) | a²/b² (3) |
| q-554 (G19) | A⁴ + B³ + C², digits 1, 2, 3 | A³ + B² + C, digits 1, 2, 4 | ◆(124) = 9 (4) |
| q-555 (G20) | ◆(x) = 1/x, ◆(a)·a = ◆(b)·b | ◆(x) = 3/x; ◆(a) < 3, a/b, ◆(a) < ◆(a+1) | ◆(a)·a = ◆(b)·b (2) |
| q-556 (G21) | number of 3s, ⟦18⟧ = 2 | number of 5s, ⟦50⟧ = 2 | ⟦5x⟧ = ⟦x⟧ + 1 (4) |
| q-557 | ◆(100, 36)/◆(64, 49) | ◆(169, 16)/◆(36, 25) | 3 (3); trap 9 = outer root forgotten |
| q-558 | #(◆(9, 6), ◆(10, 3)) min/max | #(◆(8, 5), ◆(12, 2)) | 5 (2) |
| q-559 | ◆(◆(3, 2), 6) | ◆(◆(4, 1), 8) | 9 (1) |
| q-560 | x(x − 2), ◆(◆(3)) | x(x − 3), ◆(◆(4)) | 4 (3) |
| q-561 | a/(a+1), ◆(1)…◆(5) | ◆(2)…◆(7) | 1/4 (2); trap 1/8 |
| q-562 | x(x − 4)(x + 1) = 0 | x(x + 5)(x − 2) = 0 | 3 (4); trap 2 forgets x = 0 |
| q-563 | ◆(a²) = \|a\|, ◆(1/9) | ◆(1/16) | 1/4 (3) |
| q-564 | a⁷ + … + 1, ◆(1) − ◆(−1) | a⁵ + … + 1 | 6 (1); trap 3 = not doubled |
| q-565 | (4◆2)◆3, (a+b)/(a−b) or 0 | (5◆3)◆4 | 0 (3); trap 4 = inner only |
| q-566 | ◆(x) + 6 = 8x − ◆(x), ◆(2) | ◆(x) + 2 = 10x − ◆(x), ◆(3) | 14 (2); trap 28 = not halved |
| q-567 | x~y concatenation, 45~12; x < 5~x, x~1 = 10x + 1 | 36~7; x < 2~x, x~3 = 10x + 3 | x~y = y~x (1) |
| q-568 | x⁴ + 5x² + 6x − 9, ◆(4) − ◆(−4) | x⁴ + 2x² + 7x − 5, ◆(3) − ◆(−3) | 42 (1) |
| q-569 | ◆(1) = 4, +2, ◆(6) | ◆(1) = 7, +3, ◆(5) | 19 (3); trap 22 = one step too many |
| q-570 | ◆ = x + 3, # = x², ◆(#(a)) = #(◆(a)) | ◆ = x + 5 | a = −2 (2) |
| q-571 | letter x; choices x, x−1, 10−x, x+1 | letter n; order 10−n, n+1, n, n−1 | n (3) |
| q-572 | a/b − b/a, ◆(−1, 2) = ◆(2, 1) | ◆(−1, 3) | ◆(3, 1) (3) |
| q-573 | (x − 2)/x, a, b > 2 | (x − 3)/x, a, b > 3 | ◆(a)·◆(b) < 1 (3) |
| q-574 | x² − 4 | x² − 9 | √(◆(a)+9) = ◆(a)/(a+3) + 3 (2) |
| q-575 | (x − 3)(x + 2), ◆(a) = ◆(a+5) | (x − 4)(x + 1), ◆(a) = ◆(a+4) | 1 value, a = −1/2 (2) |
| q-576 | remainders ◆(◆(47, 9), ◆(11, 4)) | ◆(◆(38, 7), ◆(23, 6)) | 3 (3); trap 2 = 5 ÷ 3 |
| lesson slide 2 | 4 · 6 = 24, 4² = 16 | 3 · 7 = 21, 5² = 25 | – |
| lesson slide 3 | a♥b = 3(a+b), 6♥2 = 24 (trap 20) | a♥b = 2(a+b), 7♥3 = 20 (trap 17) | – |
| lesson slide 6 | ◆(3) + ◆(4) = 25 vs ◆(7) = 49 | ◆(5) + ◆(1) = 26 vs ◆(6) = 36 | – |
| lesson slides 7, 9, 10 | a⋆b = 2a + b²: (2⋆3)⋆1 = 27; 3⋆4 = 22, 4⋆3 = 17; x⋆2 = 18 → 7 | a⋆b = 3a + b²: (1⋆2)⋆3 = 30; 2⋆4 = 22, 4⋆2 = 16; x⋆4 = 25 → 3 | – |
| lesson slide 8 | ◆(3) = 24, 8x | ◆(5) = 30, 6x | – |
| card | the lesson's examples, F(4t), 7 − ◆(x−2), 4x + 10, 47 ÷ 9, x⁴ + 6x at 4 | new lesson examples, F(5t), 2·◆(x−1), 2x, 29 ÷ 4, x⁴ + 3x at 5 | – |

## 2026-10-06 review (of the renumber pass)
Checked all 36 renumbered items (keys, traps, type, level), the lesson/card examples, and rendered the 6 videos the pass
had not rendered (solve-q-542, -544, -547, -548, -550, -551): all correct.
- **Fixed:** q-554 had the rule lowered from A⁴ + B³ + C² to A³ + B² + C. Now the Hebrew rule is kept with the new digits
  1, 2, 4: ◆(214) = 33, ◆(142) = 69, ◆(412) = 261, ◆(124) = 25 → choice 4. Question, explanation and both video methods
  rewritten; rendered.
- Judgment calls (kept): q-561 now starts at ◆(2) (adds a "starts at 1" trap, 1/8); q-564 has 6 terms instead of 8;
  q-556 counts 5s instead of 3s — same kind.

## 2026-10-06 Hebrew back-check
The renumber pass was compared with base-v18 only. Every guided / practice question, the lessons, the summary and the card
were now compared with the teacher's Hebrew VIDEO subtitles (01-Algebra-Original-Subtitles.txt, lines 18765–19911).
Five items had landed back on the Hebrew videos' numbers or definitions; they get new numbers once more (same type, trap,
level and methods; solution videos rewritten; keys brute-forced; no duplicate in topics 1–20). Nothing in topic 19 is
recorded. Function `hebrew_backcheck(M)` in t19.py runs last.

| id | Hebrew video | ours before | new | answer |
|---|---|---|---|---|
| lesson slide 3 + card "Basic" | x ♥ y = 2(x + y), 8 ♥ 5 | a ♥ b = 2(a + b), 7 ♥ 3 = 20 | a ♥ b = 5(a + b), 7 ♥ 3 = 50 (trap 7 · 5 + 3 = 38) | 50 |
| q-542 (guided) | $(x) = x², $($(3)) = 81 | ◆(◆(3)) = 81 | ◆(◆(5)) | 625 (3); trap 25 |
| q-545 (guided) | odd 2x / even x² − 5, $$$(3) = 62 | odd 2x / even x² − 3, ◆◆◆(3) = 66 | odd 4x / even x² − 9, ◆◆◆(1): 1 → 4 → 7 → 28 | 28 (3); traps 7, 16, 4 |
| q-549 (guided) | choices $(3x) = 9$x, $x = $($√x), $(x−4) = $(4−x) | ◆(3x) = 9◆(x), ◆(x) = ◆(◆(√x)), ◆(x−2) = ◆(2−x) | ◆(6x) = 36◆(x), ◆(√x)·◆(√x) = ◆(x), ◆(x−7) = ◆(7−x); answer ◆(5x) = 5◆(x) kept | choice 3 |
| q-550 (guided) | inner $(1, 2, 3) = 18 | inner ◆(2, 1, 3) = 18, answer 20 | ◆(1, 1, ◆(2, 1, 4)): inner 16 + 1 + 16 = 33 | 35 (3); traps 2, 33, 66 |

Partial overlaps left on purpose (only one number or the question's structure is shared; the Hebrew numbers are gone):
q-541 (answer 12 like the Hebrew $4 = 12, but a different rule and input), q-543 (input 3 like the Hebrew $3 = 24; result
and all choices differ), q-544 (◆(2x) structure; numbers differ), q-546 (circular, input 6 and step x − 2 as in Hebrew;
constants 9 and 2 instead of 5 and 0), q-548 (input 4; coefficients differ), q-551 (the two square-formula definitions are
the trick itself; all numbers differ), q-552 / q-553 / q-554 / q-555 / q-556 (Hebrew types with changed coefficients,
powers, factor 5 instead of 2). Practice: no match (the Hebrew practice is not in the subtitles; no practice item equals a
Hebrew video example).
Checks: `python3 math_check.py 19 32` → 0 / 0 / 0; rendered new-operation, solve-q-542, -545, -549, -550 and looked.


## 2026-10-07 methods spread
Every question checked against the 2026-10-06 methods; nothing added (no code). Power count does not separate the choices where letters appear (q-553: every choice has power 0; q-r26-t19-01/-07 and q-r26-t19-20 are mixed expressions; q-571 is a count, not an expression). The "flip all signs" idea is already the shortcut in q-r26-t19-05, q-564 and q-568. Nothing in topic 19 is recorded.


## 2026-10-07 trim added repeats

Teacher: only OUR additions that re-teach something learned earlier in the study plan are trimmed; the Hebrew course's own repeats stay. `trim_added_repeats(M)` runs last in apply(); helpers in `_trim_repeats.py` (videos with a take recorded before its CUTOFF are left as recorded). Notes updated in added_notes.json.

- new-operation 'Brackets on every input': the negative-input part is one line (topics 4, 8); the (x + 2) input stays. ~6 s.
