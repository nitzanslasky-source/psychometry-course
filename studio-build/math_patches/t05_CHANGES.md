# Topic 5 — Expressions: changes (course review 2026-09)

Patch: `math_patches/t05.py`. Check: `python3 math_check.py 4 5` gives 0 problems, 0 layout problems and 1 warning. The warning is a real exception: Q9 states two *claims*, and they are already on separate lines.

## 1. Wrong teaching, fixed
- **Q1 video**: I removed the tip "when the answer equals a choice number, it sits in that slot". It is false: Q1 itself has 3 in slot 1. The board notes now use ÷, for example "1 ÷ 1/2 = 2" and "12 ÷ 2 = 6".
- **Q9 video, Method 1**: "That's not what she started with ✗" is not a proof. Now the video says the two sides look different but could still be equal, then tests numbers: A = 1, B = 2 gives 1/3 vs 3/2, so they are not equal. **Method 2** no longer refers to geometry (180 + α)/2, which is not taught yet. It now uses the split rule from the lesson.
- **Lesson, "Opposite brackets"**: "Honestly? Trust it" is replaced by a one-line proof, b − a = −(a − b).
- **Q8**: the choices had the value first and the condition second, which did not fit "If ___ then … equals ___". They now read "x > 0 ; 3", "x < 0 ; 4" and so on. "0 < x" is now "x > 0". The key is unchanged (choice 2).

## 2. Methods added
**Lesson "Working with Expressions"** now has 11 slides (was 9), and the sidebar is updated:
- New slide 4, **Splitting a fraction**: (a+b)/c = a/c + b/c ✓ but c/(a+b) ≠ c/a + c/b ✗, with the numbers 6/(1+2) = 2 vs 6/1 + 6/2 = 9.
- New slide 9, **Choosing numbers**: different letters get different values (2, 3, 5). 0 and 1 cause ties. Obey every condition. If an equation is given, pick numbers that make it true. If there is a tie, keep only the tied choices and try new numbers.
- Slide 7 (repeated bracket) gets one line: "If they give you the block's value, put the number in its place."
- The Recap board is updated.

**New lesson video `r26-t05-shortcuts` "Exam Shortcuts"** (5 slides) comes at the end of the Advanced section, after Q14:
- **Sum and product**: one reminder slide that points back to Topic 4's "Factoring Trinomials" lesson, with one example (x² + 9x + 20).
- **Round numbers**: 99·41 = 4,100 − 41, and 96·104 = 100² − 4².
- **Given a block**: if x + y = 5, then 3x + 3y + 1 = 16.
- Recap.

**Four new guided questions with solution videos** (Questions 15–18, all in the Advanced section):
- Q15 `q-r26-t05-01`: (x² − 2x − 15)/(x − 5) − x = 3. It is solved with sum and product. The plug-in method shows a tie at x = 0.
- Q16 `q-r26-t05-02`: 98·102 − 99·101 = −3, using sum × difference around 100.
- Q17 `q-r26-t05-03`: given a − b = 3, (b − a)² + 2a − 2b = 15. It is solved with the block, and by plugging in a = 3, b = 0.
- Q18 `q-r26-t05-04`: (a²b + ab²)/(ab) = a + b. This is the plug-in trap: with a = b = 1, three choices tie.

**New memory card `mem-r26-t05-expressions`** (the topic had none). It sits at the end of the Advanced section and has:
- a rules table: split ✓/✗, |x|/x, round numbers, given block (the rows already in the Topic 4 cards are not repeated)
- a "Pick your method" checklist, which the review said was missing after the advanced section
- tips on choosing plug-in numbers

## 3. Used before taught (fixed inside the topic)
- **Q11** used negative exponents, which are only taught in Topic 8. It is rewritten as (1/x² + 4x²/x⁴)·(1/5)·5/(1/x²). The structure and the answer (5, choice 3) are the same. Both video slides are rewritten.
- **Q12 choice 3**, a⁰ + (−1)ᵃ, is replaced by (a+1)² − (a−1)² = 4a, which uses a Topic 4 identity. The key is still choice 4. The video now shows (a+2) + (a+2)² = (a+2)(a+3) on the board, as the review asked.
- **extra-09** used x⁻². It is rewritten as (3/x² − x/x³)·x²/2 = 1, and the key is now choice 1.
- **Q7**: "We don't know how to factor this yet" now says: "You know sum and product from Topic 4, but here the choices are faster."
- The round-number items (extra-19 and t5-1-5) now come after the round-numbers lesson.

## 4. Text
- Every question in the topic (guided and practice) now has TeX stems, choices and solutions. There is no ":" for division anywhere. Every solution shows the numbers and names the choice. The words-only solutions ("Group the x terms…") are rewritten.
- **extra-07**: the choice that could be read two ways, "a+4b:a", is now $a+\frac{4b}{a}$.
- Q9 stem: each claim is on its own line with its condition. Q4 stem: I removed "What is the value of the expression: … = ?". Q7 and the factoring items: "Which of the following expressions is necessarily equal to …?". Q12 stem: I removed the stray space before the period.
- Conditions are written as "Given: …" on their own line. The two-condition stems (Q18 and practice item 15) use `\begin{cases}`.
- **Q14 video**: the estimate now anchors on 63·500 = 31,500 instead of the draw note "≈ 30,000 : 60".
- Q5 and Q10 title slides now say the first method can be skipped.
- "so" meaning "therefore" in the middle of a sentence is fixed in the Q2, Q3, Q6 and Q14 videos.

## 5. Practice
**Removed 12 near-duplicates:**
- extra-02 (a clone of Q2 / q-123)
- extra-03, self-6 and t5-1-6 (repeated-bracket clones)
- extra-08 (a copy of Q10)
- self-1, self-2, self-3, self-4, self-5 and self-7 (twins of the unit-t5-1 items)
- t5-1-7 (a twin of extra-17)

**Added 12 exam-level practice items** (`q-r26-t05-05` … `-16`):
- given a block, three items: x − 2y = 4; a/b = 3; x − 1/x = 3 → x² + 1/x² = 11
- round numbers, two items: 999·25; (101² − 99²)/4
- factoring with a minus: one item
- plug-in ties, two items: (x³ + x²)/x, where all four choices tie at x = 1; (a² − b²)/(a − b) − 2b
- split-fraction trap: one item, 6/(x + y)
- sign question: one item, x < 0 < y, which expression is positive
- nested fraction with letters: one item, 1/(1 + 1/x)
- constant expression with a condition: one item

**Total practice:** 37 before, 37 after. The "Independent practice" section is ordered from easy to hard. "Additional examples" is ordered easy to hard too.

## Counts
- Questions rewritten: 38. Added: 16 (4 guided + 12 practice). Removed: 12.
- Slides changed: about 20. Slides added: 2 in the lesson, plus 5 in the new lesson video and 12 in the new solution videos.
- Videos added: 5 (1 lesson + 4 solution). Figures: none in this topic. Cards added: 1.
- I checked every new or changed key numerically with random legal values. Each has exactly one correct choice.

## For the teacher to decide
- **Numbering**: Questions 15–18 sit after Q14 so that the "Question N" numbering stays in order. The review wanted the "block" guided question near the lesson's repeated-bracket slide, so slide 7 now points forward to it ("after Question 14").
- **Topic 4 overlap (resolved)**: Topic 4 teaches trinomial factoring. Topic 5 keeps only a one-slide reminder and the guided Q15 (factoring inside a fraction). I dropped the card rows that repeat Topic 4 cards (sum and product, (a−b)/(b−a) = −1, 96·104). Practice item 07 is now x − 1/x = 3 → 11, so it does not repeat Topic 4's x + 1/x = 3 item.
- **Sign questions** ("if x < 0 < y, which is positive?"): only one practice item is added here. A full treatment belongs to the inequalities topic.

## Pass 2 (2026-09-27, teacher-approved remove/restore plan + summary lesson)
**Removed:** nothing (the plan keeps every addition in Topic 5).

**Restored (15 questions + 1 line):**
- 12 practice questions are back, cleaned up (TeX, "= ?" stems, conditions on their own line, full numeric solutions), and placed easy to hard:
  - Independent practice: q-expression-extra-02, -03, -08, alg-extra-expression-self-1 … self-7
  - Source-bank practice: alg-extra-unit-t5-1-6, -1-7
- q-131 (guided): the original stem with negative exponents, (x⁻² + 4x²/x⁴)·(1/5)·(5/x⁻²), and the original `solve-q-131` slides 1–3. It **moves to Topic 8**.
- q-132 (guided): the original choice 3, a⁰ + (−1)ᵃ, and the original `solve-q-132` slide 2. It **moves to Topic 8**.
- q-expression-extra-09: the original (x⁻² + 2/x²)·x² = 3 (key choice 3). It **moves to Topic 8 practice**, next to the other negative-exponent item (after alg-extra-exponent-extra-4).
- In Topic 8, q-131 and q-132 come after the Topic 8 guided questions, before the Topic 8 summary. Their solution videos get the Topic 8 video title and sidebar. The Topic 8 patch runs after this one, so this last step runs when all patches have finished (a small hook on `M.finish`).
- The "Opposite brackets" lesson slide has its original line back after the new proof: "Honestly? Trust it. It's always negative one."
- In Topic 5, the guided questions are renumbered automatically. Old Q13–Q18 are now Q11–Q16, and the spoken references follow ("after Question 12", "in Question 13"). The Advanced Expressions sidebars no longer list the two questions that moved.

**Summary lesson added:** `r26-t05-summary`, "Summary: Expressions". It sits at the end of Advanced expressions, right before the independent practice. It has 10 slides: Summary · Expression or equation? · Splitting a fraction · The main fraction bar · Opposite brackets · Take it out front (repeated bracket, sum and product) · Round numbers · Given a block · Plug in numbers · Before you practice (4 checks and the common traps).

**Small fix:** the title slides of the new guided videos now keep the lesson name as the slide label. The big title still shows the number. Before this fix, automatic renumbering could change that label twice (for example "Question 11" on a video whose big title was "Question 13").

Check: `python3 math_check.py 5 6` gives 0 problems and 0 layout problems. The 1 warning is the known exception: Q9 (q-129) states two claims.
