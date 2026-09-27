# Audit: Topic 4 (Expressions: Fundamentals). Report only

Sources: `math_patches/t04_CHANGES.md` and `math_patches/t04.py`, checked against `real_exam/quant_real.md` (760 questions).
**Re-check 2026-09-27:** I re-ran every REMOVE and UNSURE verdict against the regenerated `quant_real.md`, which now has the full text after "<". I scanned all 70 non-geometry questions that contain a square, all geometry and word-problem questions with a squared letter, and "≠" and "no solution" stems. I also checked the original course (`student_review/t4.md`, `t5.md`) for trinomial and twin-identity questions.
I read these groups in full: algebraic_expressions (32) and equations (33). I also grepped every question that has `^2`, `sqrt`, `1/x` or `ab`.

Key real-exam facts for this topic:
- **Difference of squares** (numbers or letters) appears 7 times: 2021_spring_q2_17 (17.5² − 7.5²), 2021_autumn_q2_09, 2020_winter_q1_15, 2019_winter_q1_02, 2025_spring_q1_07, 2019_spring_q1_11 and 2022_winter_q1_20.
- **Expanding/comparing squared brackets** appears in 2021_autumn_q1_13 ((x+1)² − (x−1)²), 2025_winter_q2_03, 2024_winter_q1_08, 2023_winter_q1_02 and 2025_winter_q2_05 (x+y and |x−y| → xy).
- **The (u + 1/u)² identity** appears in 2024_autumn_q2_11 ((b/a + a/b)² = b²/a² + 2 + a²/b²) and 2024_spring_q2_16.
- **Recognizing a perfect square backward** appears in 2023_spring_q1_13 and 2024_spring_q2_16.
- **A bracket as a common factor** appears in 2024_winter_q2_06 (2ab − 10b = 2a − 10) and 2021_autumn_q2_03.
- **Factoring a trinomial x² + bx + c (sum–product)**: 0 real questions need it (confirmed on the full text). Closest cases:
  - 2023_autumn_q2_04 (m^{2x} = m·m^{x²}) leads to x² − 2x + 1 = 0. That is a perfect square, covered by the formulas lesson.
  - 2021_spring_q1_08, choice 4 (15 − 2x = 2x² + 3), leads to x² + x − 6 = 0. The question does not need it solved: choice 3 (2x + 5 = 2x + 7) is visibly impossible.
  - 2025_spring_q2_17 (√(x² − x)) is a common factor, x(x − 1).
  - 2020_autumn_q2_03 (4x² − 64 = 0) is a difference of squares.
  - 2026_spring_q2_08 is given already factored.
- **The original course tests trinomial factoring in 5 questions**:
  - alg-extra-unit-t4-1-3 (x² + 8x + 15), in Topic 4.
  - q-127, Topic 5 guided Q7 (x² + 11x + 24).
  - q-expression-extra-05 (x² + 13x + 40), Topic 5.
  - alg-extra-unit-t5-1-3 (x² + 12x + 35), Topic 5.
  - alg-extra-expression-self-3 (x² + 10x + 24), Topic 5. The Topic 5 patch removed it (listed in `original_removed.json`).

  The original course never taught the method. Under the teacher's rule (original questions stay and must be taught), the lesson that teaches it stays.
- **The twin identity (a+b)² + (a−b)² = 2a² + 2b²**: 0 real questions (confirmed on the full text). The nearest are 2022_autumn_q2_13 (a² + b² vs c² + d², coordinates on a circle) and 2024_autumn_q1_08 (average of x² and y²), and neither uses the identity. No original course question uses it either.

| Addition | Where | Class | Verdict | Evidence |
|---|---|---|---|---|
| Lesson split into 2 videos (formulas moved) | expression-basics → r26-t04-formulas (old slides 9–12) | FIX | KEEP | structure only |
| Slide 1 text; slide 10 recap rewritten | expression-basics slides 1, 10 | FIX | KEEP | — |
| Like terms with roots: 3√5 − √5 = 2√5 | expression-basics slide 3 | FIX (extra example of an existing rule; supports original q-101) | KEEP | — |
| a · a³ = a⁴, "count the a's" | expression-basics slide 4; card tip | FIX (clarifies the existing multiplying-terms rule; original q-103, q-104) | KEEP | also 2019_spring_q2_01 |
| Second two-bracket example (x − 5)(x + 2) | expression-basics slide 7 | FIX | KEEP | — |
| "Cancel vs reduce" remark moved from the Q1 video | expression-basics slide 8; solve-q-120 slide 2 | FIX (move) | KEEP | — |
| NEW slide "Bracket as a factor" | expression-basics slide 9 | METHOD | KEEP | 2024_winter_q2_06, 2021_autumn_q2_03 |
| NEW slide "Power first" (3(x+3)², −x² vs (−x)²) | r26-t04-formulas | METHOD / error rule for squares | KEEP | 2022_winter_q1_15 (−(x²) + 7), 2025_winter_q2_03, 2021_autumn_q1_13 |
| NEW slide "Number shortcuts" (98·102, 31² − 29²) | r26-t04-formulas | METHOD | KEEP | 2021_spring_q2_17 |
| NEW slide "Perfect-square check" (3-step checklist) | r26-t04-formulas | METHOD | KEEP (see note on its failing example) | 2023_spring_q1_13, 2024_spring_q2_16 |
| NEW slides "Value without x" and "Value without x (2)" | r26-t04-formulas | METHOD | KEEP | 2025_winter_q2_05, 2021_autumn_q2_09, 2024_autumn_q2_11 |
| NEW recap slide | r26-t04-formulas | FIX | KEEP | — |
| NEW lesson "Factoring Trinomials" (8 slides, sum–product) | video r26-t04-trinomials | METHOD (teaches a type the original course tests) | KEEP (changed from UNSURE) | 0 real questions. It is needed for 5 original questions: alg-extra-unit-t4-1-3, q-127, q-expression-extra-05, alg-extra-unit-t5-1-3 and alg-extra-expression-self-3. Original questions must be taught |
| NEW card "Factoring trinomials" | mem-r26-t04-trinomials | METHOD | KEEP (changed from UNSURE) | Same original questions as the lesson |
| Card "Multiplication formulas": new rows | mem-formulas rows a²+b² = (a+b)² − 2ab; (x+1/x)²; bracket-factor example; 98·102 example | METHOD | KEEP | 2025_winter_q2_05; 2024_autumn_q2_11; 2024_winter_q2_06; 2021_spring_q2_17 |
| Card "Multiplication formulas": new tips | mem-formulas tips: power first; −x² vs (−x)²; (b−a)² = (a−b)²; perfect-square checklist; a·a³ | METHOD / FIX | KEEP | 2022_winter_q1_15; 2019_winter_q1_02 ((a−b)², (b−a)² as distractors); 2023_spring_q1_13 |
| Q1: "twin identity" (a+b)² + (a−b)² = 2a² + 2b² | solve-q-120 slide 2 (bonus lines); q-120 explanation, last line | CONTENT (new rule) | REMOVE (re-checked) | 0 real questions; no original question uses it either |
| Q1: rule for choosing plug-in numbers | solve-q-120 slide 3 | METHOD | KEEP | 2019_winter_q1_02, 2023_spring_q1_13, 2020_autumn_q2_16 |
| Q1, Q2 (q-120, q-121) stems, solutions, TeX | q-120, q-121 | FIX | KEEP | — |
| Guided Q3 x+y=6, xy=5 → x²+y² | q-r26-t04-01 + solve-q-r26-t04-01 | METHOD type (value without x) | KEEP | 2025_winter_q2_05 (sum/difference → product, same identity). No real question asks for exactly a²+b² |
| Guided Q4 51² − 49² | q-r26-t04-02 + solve-q-r26-t04-02 | METHOD type | KEEP | 2021_spring_q2_17 |
| Guided Q5 (a−b)² = (b−a)² | q-r26-t04-03 + solve-q-r26-t04-03 | type exists | KEEP | 2019_winter_q1_02, 2023_winter_q1_02 |
| Guided Q6 x + 1/x = 3 → x² + 1/x² | q-r26-t04-04 + solve-q-r26-t04-04 | METHOD type | KEEP | 2024_autumn_q2_11, 2024_spring_q2_16 (the identity; no real question gives a number for x + 1/x) |
| Guided Q7 x² + x − 12 (trinomial) | q-r26-t04-05 + solve-q-r26-t04-05 | CONTENT (trinomial question type) | REMOVE (re-checked) | 0 real questions of this type. The one incidental case, 2021_spring_q1_08 choice 4, does not need factoring. The kept lesson is practiced by the original trinomial questions |
| Guided Q8 (x²−9)/(x²+x−6) (trinomial + reduce) | q-r26-t04-06 + solve-q-r26-t04-06 | CONTENT (trinomial) | REMOVE (re-checked) | 0 real trinomials. Reducing by factoring appears (2026_spring_q2_08, 2025_winter_q1_08), but that is already covered by original alg-extra-unit-t4-1-4 |
| Practice a−b=3, ab=4 → a²+b² | q-r26-t04-07 | value without x | KEEP | 2025_winter_q2_05 |
| Practice x+y=8, x−y=2 → x²−y² | q-r26-t04-08 | difference of squares | KEEP | 2021_autumn_q2_09, 2020_winter_q1_15 |
| Practice 1001² − 999² | q-r26-t04-09 | difference of squares | KEEP | 2021_spring_q2_17 |
| Practice x + 1/x = 4 → x² + 1/x² | q-r26-t04-10 | (u+1/u)² | KEEP | 2024_autumn_q2_11, 2024_spring_q2_16 |
| Practice x² − 2x − 15 | q-r26-t04-11 | CONTENT (trinomial) | REMOVE (re-checked) | 0 |
| Practice x² − 7x + 12 | q-r26-t04-12 | CONTENT (trinomial) | REMOVE (re-checked) | 0 |
| Practice (x²+x−6)/(x²−4) | q-r26-t04-13 | CONTENT (trinomial + reduce) | REMOVE (re-checked) | 0 real trinomials |
| Practice (2a+b)² − (2a−b)² | q-r26-t04-14 | expanding squares | KEEP | 2021_autumn_q1_13 |
| Practice (a+b)²=49, (a−b)²=9 → ab | q-r26-t04-15 | value without x | KEEP | 2025_winter_q2_05 |
| Practice (2021² − 2019²)/2020 | q-r26-t04-16 | difference of squares | KEEP | 2021_spring_q2_17 |
| Practice x−y=5 → x² − 2xy + y² − 2x + 2y | q-r26-t04-17 | perfect square + bracket factor | KEEP | 2020_spring_q1_16 (substitute a combination), 2024_winter_q2_06 |
| Practice x²−y²=24, x+y=6 → x | q-r26-t04-18 | difference of squares | KEEP | 2021_autumn_q2_09, 2020_winter_q1_15 |
| Practice (x+3)² − (x−3)(x+3) (plug-in) | q-r26-t04-19 | expanding + METHOD plug-in | KEEP | 2021_autumn_q1_13, 2024_winter_q1_08 |
| Rewrites of 23 original practice items; q-106 plug-in line | q-100…q-119, alg-extra-unit-t4-1-1…7 | FIX / METHOD | KEEP | plug-in: 2024_autumn_q1_06 ((a−1)(a²+a+1)) |
| Removal of near-duplicates q-108, q-109, q-111, q-117 | — | not an addition (an original-content removal by the fixers) | — | Restore them. See ORIGINAL ITEMS REMOVED BY FIXERS |
| Practice reorder | unit-t4-1 | FIX | KEEP | — |

Notes:
- **Perfect-square check slide.** Its failing example (x² + 10x + 16) points to the sum-product method. The trinomial lesson now stays, so the pointer stays too.
- **Trinomial lesson and card: KEEP.** They teach the method that 5 original questions need. The added q-r26 trinomial questions are still removed: their type has no real exam question, and the original questions already give practice.
- **Topic 5 note:** the Topic 5 patch removed the original alg-extra-expression-self-3 (x² + 10x + 24). It should be restored.

## TO REMOVE
- Question q-r26-t04-05 and its solution video solve-q-r26-t04-05 (guided Q7, x² + x − 12)
- Question q-r26-t04-06 and its solution video solve-q-r26-t04-06 (guided Q8, (x²−9)/(x²+x−6)). Renumber the guided sidebar ("Question 1 … Question 6").
- Practice q-r26-t04-11 (x² − 2x − 15)
- Practice q-r26-t04-12 (x² − 7x + 12)
- Practice q-r26-t04-13 ((x²+x−6)/(x²−4))
- In solve-q-120, slide 2: the lines `Write "(a + b)² + (a − b)² = 2a² + 2b²"` and "Bonus: with a PLUS between the squares…". In q-120's explanation, the last line "Twin identity: …".

## UNSURE (teacher decides)
- None. The trinomial lesson and card moved to KEEP because they teach original questions.

Counts after the re-check: 34 KEEP, 6 REMOVE, 0 UNSURE.

## ORIGINAL ITEMS REMOVED BY FIXERS
Original (non q-r26) items that `math_patches/t04.py` removed or replaced, compared with the pre-patch course in `student_review/t4.md`.

**Removed. Restore these:**
- Practice question q-108: (3a − b) − (−b + 3a). Removed by `M.unplace` as a "near-duplicate". Put it back into unit-t4-1 practice.
- Practice question q-109: (−q + p) − (−p − q). Same removal; restore it.
- Practice question q-111: (3x + 4)². Same removal; restore it.
- Practice question q-117: (x − 8)(x + 8). Same removal; restore it.

**Replaced or rewritten.** The original content was changed; the item still exists. Restore the original if it must stay word for word:
- Lesson video expression-basics, slide 13 "Recap". The original slide was replaced by a new recap, now slide 10. The original board showed the three formulas (a+b)², (a−b)², (a−b)(a+b) and the line "Circle the three formulas… Two big takeaways: taking out a common factor, and the three formulas. Now try a question". The new recap drops the formulas line; the formulas get their own recap in r26-t04-formulas.
- Lesson video expression-basics, slides 9–12: (a + b)², (a − b)², Sum × difference and Formulas backward. They were not deleted: they moved to the new video r26-t04-formulas. Only the first line of the (a + b)² slide changed, plus spelling. Nothing is lost, but they are no longer in the original video.
- Lesson video expression-basics, slide 1 (title). Two lines were reworded; the second now says the formulas come in the next video.
- Worked solution solve-q-120, slide 2. The line "Small nuance: equal terms added and subtracted CANCEL out. REDUCING is different…" was removed from here and moved to expression-basics slide 8.
- Card mem-formulas, row "(a−b)(a+b) = a² − b²". The original example "48·52 = 50² − 2²" was replaced by "98·102 = 100² − 2² = 9996".
- Card mem-formulas, intro. "Use them forwards to expand and backwards to factor." was replaced by a longer sentence.
- Card mem-formulas, tip "(a−b)/(b−a) = −1". It was merged into a longer tip that keeps the same content.
- Questions q-120 and q-121 (guided Q1 and Q2): the stems were shortened and the explanations rewritten.
- All 23 kept practice items (q-100 … q-119, alg-extra-unit-t4-1-1 … -7): stems, choices order and explanations were rewritten.
  - The "(factor)" and "Simplify / Factor / Evaluate" stems became "Which of the following is equal to …?".
  - The q-112 key moved to choice 3 (same answer).

  The question content is unchanged.
- Practice order of unit-t4-1: reordered.
