# Topic 9 — Roots — Fundamentals: changes

Source: `student_review/review_t9-10.md` (Topic 9 part) and `PLAN.md`. Patch: `math_patches/t09.py`.
Check: `python3 math_check.py 9` gives 0 problems, 0 warnings and 0 layout problems.

## Counts
- Questions rewritten: 21. That is all 14 remaining core questions (q-233 to q-247) plus 6 extra-practice questions. q-242 got new content.
- Questions added: 19. Six are guided questions with solution videos (q-r26-t09-01 to 06), and 13 are practice questions (q-r26-t09-07 to 19).
- Questions removed: 2 near-duplicates. **q-239** repeated q-238 (a root times itself). **alg-extra-root-practice-6** repeated q-237 (a product under one root).
- Topic total: 22 questions before, 39 after.
- Main lesson video `roots`: 6 slides changed in content (1, 2, 3, 4, 7, 13) plus sidebar re-indexing on 5 others, 3 slides added (10 slides became 13). The sidebar grew from 9 to 12 labels.
- Videos added: 7. One is a new lesson, `r26-t09-traps` "Roots — Exam traps" (7 slides, about 4 minutes). The other six are solution videos, `solve-q-r26-t09-01` to `06` (Questions 1–6).
- Memory card `roots`: rules table extended, new "Exam traps" table, and the tips rewritten.
- Figures: none. The topic has none.

## Priority 1 — wrong or untaught rules in the video and on the card
Nothing in the video was mathematically false. These are the fixes:
- The card tip "6/√3 = 2√3 — ignore the root, then put it back" was never taught. It is now taught on slide 7 (Multiply & divide) with the reason: 3 = √3·√3. The card tip is reworded as "divide by the number under the root, keep the root".
- Slide 7: the teacher note "√(75 : 3)" now reads "√(75 ÷ 3)".
- Slide 1 said "fifteen questions" and slide 13 said "fifteen questions, no videos in between". Both are updated, because some questions now have solution videos.

## Priority 2 — methods added (with where they are used)
Main video `roots` (final slide numbers):
- Slide 2 (What a root is): **domain**. √(x − 3) exists only for x ≥ 3. Practiced in q-r26-t09-12.
- Slide 3 (Root of a square): **one example with x < 0**. x = −3 gives √9 = 3 = −x. Practiced in practice-3.
- Slide 4 (Pull out squares): **pull out the LARGEST square**. √72 = 2√18 is not finished. Then the check: is the number left inside still divisible by 4, 9 or 25?
- **NEW slide 5 "Bring a number inside"**: 3√7 = √63, 2∛5 = ∛40, and why it helps (3√7 = √63 < √64 = 8). Used by q-243, q-244 and guided Question 2.
- **NEW slide 10 "Powers inside roots"**: ⁿ√(aᵐ) = a^(m/n) (⁴√(3⁸) = 9), fractional powers backwards (8^(2/3) = (∛8)² = 4, "take the root first"), and a root of a root, √(√a) = ⁴√a. Used by q-235, q-236, q-242, guided Question 1 and practice 10–11.
- **NEW slide 12 "Root equations"**: square both sides, then check in the original equation. It also covers x = √(3x): don't divide by x, factor, 2 solutions. Plus the exam shortcut "plug in the choices". Used by q-247, practice-5, guided Question 3 and practice 13.
  - The review offered two options: move q-247 and practice-5 to T10, or teach squaring here. I taught it here, so no question leaves the topic and T10's patch is untouched.
- Slide 13 (rules table): two new rows, a√b = √(a²b) and ⁿ√(aᵐ) = a^(m/n).

New lesson video `r26-t09-traps` "Roots — Exam traps". It is placed after q-247, when all the basic drills are done.
1. Roots of small numbers: √0.09 = 0.3 (half the decimal digits), the trap √0.9 ≈ 0.95 (not 0.3), and √(1/9) = 1/3.
2. Between 0 and 1: x² < x < √x (example x = 0.25). For x > 1 the order is the other way. Plug in ¼ in "which is largest" questions.
3. Compare by squaring: 4√3 vs 5√2 means 48 vs 50 (positive numbers only). Estimate a root between two perfect squares (8 < √70 < 9).
4. Different roots: √2 vs ∛3. Raise both to the 6th power: 8 vs 9.
5. Conjugates: (√a + √b)(√a − √b) = a − b, and 1/(√2 − 1) = √2 + 1.
6. Square of a sum: (√a + √b)² = a + b + 2√(ab). The example is √3 + √5 vs √15. This is also the tool T10 q-287 needs.

Guided questions (each has a solution video; strong-student tricks are named in the videos):

| # | id | Question | Key | Method in the video |
|---|---|---|---|---|
| 1 | q-r26-t09-01 | ⁴√(9⁶) | 27 (choice 2) | power over index; 2nd method: primes. Trap 6 − 4 → 81 |
| 2 | q-r26-t09-02 | largest of 5.2, 3√3, 2√7, √26 | 2√7 (choice 3) | bring inside / square each (27.04, 27, 28, 26) |
| 3 | q-r26-t09-03 | √(x+6) = x | 3 (choice 2) | plug in the answers; why −2 is a fake solution (no quadratic needed) |
| 4 | q-r26-t09-04 | 0 < x < 1, largest of x², x, √x, x³ | √x (choice 3) | special value x = ¼ |
| 5 | q-r26-t09-05 | largest of √3, ⁶√28, ∛5, ⁶√26 | ⁶√28 (choice 2) | 6th power: 27, 28, 25, 26 |
| 6 | q-r26-t09-06 | 1/(√3 − √2) | √3 + √2 (choice 2) | conjugate; 2nd method: work back from the answers |

Where they sit: Q1 before q-235, Q2 after q-244, Q3 before q-247, and Q4–Q6 after the traps video.

## Priority 3 — text
- Every solution is rewritten in $TeX$ with the numbers shown. No colons are used for division (q-235, q-236, q-240, q-241 and q-242 had them).
- There are no words-only solutions any more. Extra practice 1–7 were words only.
- Solutions use the method the video teaches. Several now name the trap choice.
- Stems: extra practice now uses "= ?" in TeX, not "Evaluate / Simplify". "For x<0, simplify" became "Given: $x<0$" on its own line.
- q-247: the stem is now "How many solutions does the equation $x=\sqrt{5x}$ have?"
- q-246: the solution now proves the answer (1.75² = 3.0625 > 3) instead of comparing squares loosely.
- "so" meaning "therefore" is removed from the solutions.

## Priority 5 — practice
- q-242 (a root with index 2.5, not exam material) is now √(√81) = ?. Same choices and same key (3).
- 13 new exam-level practice items:
  - √0.0016
  - √0.9 closest to
  - order of 0.5², 0.5 and √0.5
  - 8^(2/3)
  - ⁴√(x⁸)
  - domain of √(2 − x)
  - √(2x + 3) = 3
  - largest of 2√11, 3√5, √43, 6.5
  - smallest of ∛4, ⁶√15, √2, ⁶√17
  - (√7 + √5)(√7 − √5)
  - (√5 + 1)²
  - 4/(√5 − 1)
  - √3 + √5 vs √15
- The practice section is ordered easy to hard, and the topic now has 10+ exam-level items.
- All new and changed questions were solved from scratch. Each has exactly one correct choice, and the key matches its solution video.

## For the teacher to decide / notes
- **"Q None" display bug:** the review reports every question shown as "Q None". This is a numbering problem in the export, not in this topic's data. I did not fix it here.
- **Student-view tool:** `student_view.py` builds its question list from the exported site JSON (`content/full-course`), not from the patched course. So `tmp_check/view/t9.md` still shows the old questions and order until the site is re-exported. I checked the patched flow straight from the data instead.
- **Numbering:** the new guided questions are numbered Question 1–6 (T9 had no guided questions before). Please make sure `question_numbers.json` takes them in when you lock numbers.
- **Length:** the main video grew from 3.8 to about 7.3 minutes. If that is too long, you could move the new "Root equations" slide (slide 12) into the traps video.
- **T10 overlap:** T10 slide 9 also covers root equations. Now that T9 teaches "square, then check", T10 can build on it (the T10 review suggests √(x+2) = x).
- **Number line:** the review asked for a number-line picture on the 0–1 slide. I used a worked example (x = 0.25) instead, because algebra slides have no figure style to copy. A drawn number line could be added later.

## Pass 2 (2026-09-27, teacher-approved remove/restore plan + summary lesson)

**Removed (roots of decimals: 0 real and 0 original questions of this type)**
- Video "Roots — Exam traps": slide "Roots of small numbers", its sidebar label "Small numbers", and the words
  "small numbers" on the title slide (now "Numbers between zero and one, comparing roots, and a partner that removes roots.").
- Practice q-r26-t09-07 ($\sqrt{0.0016}$) and q-r26-t09-08 ($\sqrt{0.9}$ closest to).
- Memory card "roots", table "Exam traps": row "roots of small numbers".

**Restored (original course)**
- q-239 ($\sqrt[3]{9}\cdot\sqrt[3]{9}\cdot\sqrt[3]{9}$) back in its original place; solution in TeX.
- alg-extra-root-practice-6 ($\sqrt{12}\cdot\sqrt{27}$) back in the practice; stem, choices and solution in TeX.
- q-242: the original question $\sqrt[2.5]{\sqrt{243}}$ (choices 9 / 27 / 3 / 1, key 3), with the original note that
  the index 2.5 means the power $\frac{1}{2.5}$; the solution now shows the numbers
  ($243^{\frac12\cdot\frac25}=243^{\frac15}=3$).
- Practice order now also places q-227, alg-extra-exponent-extra-2 and -7 (moved here by the T8 patch) by difficulty.

**Kept as the plan says:** slide "Different roots", guided Q5, practice -15 and -12, card row "6th power".

**New: summary lesson** `r26-t09-summary` "Roots — Summary" (about 3.5 min), right before "Extra independent root
practice". Slides: Summary · What a root is · Simplify roots · Multiply & divide · Roots as powers · Not for sums ·
Comparing roots · Between 0 and 1 · Conjugates · Root equations · Before you practice.


## 2026-10-04 question = lesson example fixed
- alg-extra-root-practice-2 was √72 of "roots" slide 4 -> √45 = 3√5 (choice 3).
- alg-extra-root-practice-7 was √70 of "r26-t09-traps" slide 3 -> √55, between 7 and 8 (choice 3).

## 2026-10-05 cut repeats
Function `cut_repeats` (runs last). Nothing in topic 9 is recorded.
- **Roots — Exam traps** (3.3 → 1.3 min). Cut: "Between 0 and 1" → Question 4; "Different roots" (6th power) → Question 5; "Conjugates" → Question 6; comparing two roots by squaring → Question 2.
- Kept: "Estimate a root" (√70 between 8 and 9 — used in practice, no question video) with one opening line "Comparing two roots? Square both — like in question two. It works because both numbers are positive." Kept "Square of a sum" whole. Sidebar: Estimate a root · Square of a sum.
- Moved into Question 4 (new short slide "The rule"): the board rule 0 < x < 1: x² < x < √x (the spoken rule line moved there) and "x > 1: √x < x < x² — above one it's the other way around". 0.6 → 0.7 min.
