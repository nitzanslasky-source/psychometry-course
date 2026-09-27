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
