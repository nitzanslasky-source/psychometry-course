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

## 2026-10-02 new numbers (not identical to the Hebrew course)
Goal: the English Topic 5 must not look like a copy of the Hebrew course. Every idea, trap, difficulty level and method stays; the numbers, letters, stories and choice order change. Code: `new_numbers(M)` at the end of `apply` (with a `RECORDED` set, empty for now — a question put in it keeps its old version and video).

**Guided questions (question, key, written solution and the whole solution video, incl. board notes, spoken numbers and the video title):**
| Q | Old (Hebrew / study guide) | New | Key |
|---|---|---|---|
| 1 q-135 | 12 over 1 over (1/3 + 1/6) = 6 (Hebrew 4 … 1/2 + 1/4) | 10 over 1 over (1/2 + 1/5) = 7; distractors 7/10, 10/7, 100/7 (stop early / multiply instead of divide) | 3 |
| 2 q-136 | 7 − (p−q)/(q−p) = 8 | 10 − (y−x)/(x−y) = 11; trap 9 | 1 |
| 3 q-137 | (c+d)(t−3) + (c+d)(t+3) | (m+2n)(k−6) + (m+2n)(k+6) = 2k(m+2n); ones still give one match | 2 |
| 4 q-138 | (a+b+c+d)² − (a+b−c−d)² | (p+q+r+s)² − (p−q+r−s)²  = 4(p+r)(q+s); second plug-in 3, 0, 1, 2 (= 32) | 1 |
| 5 q-125 | (18² − 18) − (17² + 17) | (13² − 13) − (12² + 12) = 0; choices 12, 1, 0, 13 (all units digits differ) | 3 |
| 6 q-126 | {[(p−q)−r]−s+q} | {[(w−x)+y]−z+x} = w+y−z; all-ones gives a tie (choices 1 and 2) → w=20, x=3, y=4, z=5 | 2 |
| 7 q-127 | x² + 11x + 24 | x² + 15x + 36 = (x+12)(x+3); every choice multiplies to 36 | 3 |
| 8 q-128 | abs(x)/x + 5 | x/abs(x) + 8 → x<0 ; 7 | 3 |
| 9 q-129 | Daniel/Maya, (A+B)/A and A/(A+B) | Tom/Dana with a difference: Tom B/(A−B) = B/A − 1 (false), Dana (A−B)/B = A/B − 1 (true); claims stacked | 2 |
| 10 q-130 | [(p−q) − (q−p)]/(p−q) = 2 | [3(m−n) − (n−m)]/(m−n) = 4; plug-in m=5, n=3 | 3 |
| 11 q-133 | 1 + (4b²+4ab)/(a²−b²) | 1 + (6b²+6ab)/(a²−b²) = (a+5b)/(a−b) | 3 |
| 12 q-134 | 32,004 ÷ 63 = 508 | 33,046 ÷ 41 = 806; choices 406, 508, 602, 806 — the units-digit check now eliminates 508 and 602 again (as in the Hebrew video) | 4 |

**Practice:** q-122 (15 over 1 over (1/3 + 1/5) = 8), q-123 ((d−c)/(c−d) − 4 = −5), q-124 ((3a+b)(z+7) + (3a+b)(z−7)), q-expression-extra-08 (was a letters-only copy of the Hebrew video question; now [(x−y) − 2(y−x)]/(y−x) = −3), q-expression-extra-11 (was a letters-only copy of the Hebrew video question; now 1 − (2b²+2ab)/(a²−b²) = (a−3b)/(a−b)).

**Lesson "Working with Expressions":** new examples a/b + b/a → x/y + 2y/x; the main-bar slide shows the new Question 1; opposite numbers 15/−15 → 8/−8, plug-in 7, 2 → 10, 4; repeated bracket (a+b)(u∓4) → (x+2)(y∓5). Reworded on-screen text: the expression/equation lines and the four plug-in rules.

**Solution videos:** inside the videos the Hebrew's own numeric examples were replaced too ((10−1)−1 → (12−2)−3; "1, 2, 3 or 10, 13, 72" → "2, 5, 7 or 11, 20, 64"; 5 − 2 / 2 − 5 → 7 − 4 / 4 − 7). Method 4 of Q5 is now "Count the copies". Pre-loaded copies of the choices on the slides are kept in sync.

**Not changed:** q-131, q-132 and q-expression-extra-09 (Hebrew Topic 5 originals) now live in Topic 8 — their new numbers belong with the Topic 8 pass. q-r26-t05-* and the newExtension items are unchanged.

Check: `python3 math_check.py 5 32` → 0 problems, 0 warnings (the old q-129 warning is gone), 0 layout problems.

## 2026-10-02 review (new numbers checked against the Hebrew videos)
- q-127: choice 4 is now (x+8)(x+4.5) (product 36, sum 12.5), like the Hebrew 4.5 choice. The plug-in slide has the Hebrew tip
  back: a choice giving a non-whole number (9·5.5) needs no calculation — it can only match a non-whole expression.
- q-135: the Hebrew Q1 side tip is back ("no visual traps: an answer equal to a choice number sits in that slot").
- q-129: the split-the-top slide has the geometry example back, as a difference: (180−α)/2 = 90 − α/2.
- q-130: the trap line now names the sign mistake (reading n−m as m−n gives 3−1 = 2), not only "forgot the 3".
- q-138: the 3 methods (plug in ones, plug in 3, 0, 1, 2 — the Hebrew also used a zero — and two blocks) are correct.
- Every other changed question, practice item and lesson example was re-done by hand: one correct choice each, the plug-ins
  leave one survivor (ties where the Hebrew had them), the units digit still decides q-125 and q-134. No change.

## 2026-10-02 order changes
Function `order_changes(M)`, which runs after `new_numbers`. It does not change any numbers or review fixes.
- **Theory.** "Opposite brackets" now comes before "The main fraction bar" in four places: the lesson slides, the lesson recap, the
  summary video and the guided questions. 10 − (y−x)/(x−y) is now Question 1 and the layered fraction is Question 2. Why: a one-step
  first question is a gentler start than a three-layer one, and the lesson, recap and summary keep the same order as the questions.
  Openers: "First guided question." moved to the opposite-brackets video. The lesson line "This exact one is Question 1" now says
  "You'll meet this exact one in the guided questions" (no number). The sidebars and active marks were updated.
- **Advanced expressions.** The order now goes easy → hard by the teacher's own Hebrew levels: (13²−13)−(12²+12) (easy+),
  33,046/41 (easy+), x²+15x+36 (easy+), x/|x| (easy+), 3(m−n)−(n−m) (medium), nested brackets (medium+), Tom and Dana (medium+),
  1+(6b²+6ab)/(a²−b²) (hard). The Hebrew order mixed these levels. The big division now comes right after the question where the
  units digit is taught, and its video uses that trick. Its opener "Last question." became "Question six. Plain numbers again."
  The lesson line "You'll practise that after Question …" still points to the last advanced question. In the build, it becomes
  "in the questions ahead".
- **Correct-answer positions** that were still the same as in the Hebrew course:
  - q-126: the key moved from 2 to 1 (w+y−z, w−y+z, w+y+z, w−2x+y−z). With all ones, choices 1 and 2 still tie. The values for
    w=20, x=3, y=4, z=5 are now listed as 19, 21, 29, 13.
  - q-127: the key moved from 3 to 2 ((x+18)(x+2), (x+12)(x+3), (x+36)(x+1), (x+8)(x+4.5)). The sums are 20, 15, 37, 12.5, and the
    plug-in values are 57, 52, 74 and "not whole".
  - In both questions the key, the written solution and every "Choice N" or "circle choice N" line in the video were updated.
    I checked both questions again by hand.
- **Rejected:**
  - Reordering the lesson slides "Plug in numbers", "Choosing numbers" and "Pick your method". They build on each other.
  - Reordering the guided questions in "Exam Shortcuts". They follow that lesson's slide order.
  - Reordering the practice sections. They are already easy → hard.
  - Moving the other guided keys. They already differ from the Hebrew course.
