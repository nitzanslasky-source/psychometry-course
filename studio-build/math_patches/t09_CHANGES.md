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

## 2026-10-06 pen or click
Function `pen_or_click` (runs last, after `cut_repeats`). The teacher's approved split: in lessons the content appears by click and the pen only marks; in solution videos the setup and mechanical lines appear by click, and only the key step (plus the marks on the choices) is written by hand. Where a hand-written line comes before click lines, the board leaves an empty row for it. Spoken lines, math, questions and slide count are unchanged. No topic 9 video is recorded. Topic total: 61 pen cues -> 14 by hand, 47 by click (14 pen cues left).
- roots (30 -> 2 by hand, 28 clicks). Every written line is a click now. By hand: circle the absolute-value bars, box the last rule. "= 7 and 7² = 49" and "= −4 and (−4)³ = −64" are one line each ("= 7  since 7² = 49"). Slides 2, 4, 7, 10 are a bit smaller and closer so they fit; slide 4's empty gap under √72 is closed.
- solve-q-r26-t09-01 (5 -> 3 by hand, 2 clicks). By hand: ⁴√(9⁶) = 9^(6/4) = 9^(3/2) (method 1), 9⁶ = (3²)⁶ = 3¹² (method 2), circle. Clicks: 9^(3/2) = 27, ⁴√(3¹²) = 27.
- solve-q-r26-t09-02 (5 -> 2 by hand, 3 clicks). By hand: (3√3)² = 9 · 3 = 27 (the move), circle. Clicks: the other three squares.
- solve-q-r26-t09-03 (5 -> 2 by hand, 3 clicks). Clicks: the three tries (x = −2, 3, 6). By hand: x + 6 = x² -> (−2)² = 4 = −2 + 6 (why −2 is a trap), circle.
- r26-t09-traps (3 -> 0 by hand, 3 clicks): the √70 estimate, (√2 + √3)², the √3 + √5 vs √15 chain.
- solve-q-r26-t09-04 (2 -> 1 by hand, 1 click). Click: the four values at x = 1/4. By hand: circle.
- solve-q-r26-t09-05 (4 -> 2 by hand, 2 clicks). By hand: (√3)⁶ = 3³ = 27, circle. Clicks: (∛5)⁶ = 25, the sixth roots.
- solve-q-r26-t09-06 (4 -> 2 by hand, 2 clicks). By hand: Bottom: (√3 − √2)(√3 + √2) = 1, circle. Clicks: Top line, the method 2 check.
- r26-t09-summary (3 -> 0 by hand, 3 clicks).

## 2026-10-06 renumber pass
Function `renumber_pass` (runs last, after `pen_or_click`). Goal: the English Topic 9 must not look like the Hebrew
course. Same ideas, traps, levels and methods. `RN_RECORDED` is empty: no topic 9 take in ~/Documents/Course.recordings.
The Hebrew Topic 9 is one lesson plus 15 study-guide questions (q-233..q-247) with no videos. The 6 guided questions
with videos (q-r26-t09-01..06) were written in English, so they and their videos are unchanged.
Check: `python3 math_check.py 9 32` and `python3 math_check.py 8 9 32` → 0 problems, 0 warnings, 0 layout problems.
Every answer and trap below was re-computed in python. The lesson was rendered and checked.

**Questions** (stem, choices, key and written solution changed together; the solutions now name the trap where there is one)
| Id | Old (Hebrew) | New | Answer · key |
|---|---|---|---|
| q-233 | ∛8 − ∛0 − ∛(−1) = 3 | ∛27 − ∛(−1) − ∛0; traps 2 (sign), 3 (ignores ∛−1) | 4 · 3 → 4 |
| q-234 | ⁶√(−64) | ⁴√(−81) | no real value · 1 → 3 |
| q-235 | ∛(5⁶) = 25 | ∛(7⁶); trap 343 (6 − 3) | 49 · 1 → 3 |
| q-236 | 81^(1/4) = 3 | 256^(1/4); traps 64 (= 256 · ¼), 16 (square root only); 2nd way: root twice | 4 · 3 → 4 |
| q-237 | √27 · √3 = 9 | √20 · √5; trap 100 | 10 · 4 → 2 |
| q-238 | √31 · √31 = 31 | √23 · √23 | 23 · 2 → 3 |
| q-239 | ∛9 · ∛9 · ∛9 = 9 | ∛6 · ∛6 · ∛6 (both methods kept: (∛6)³, ∛216) | 6 · 1 → 2 |
| q-240 | √50 / √2 = 5 | √98 / √2; traps 49, 14 | 7 · 1 → 4 |
| q-241 | √3 / √48 = 1/4 | √2 / √72; trap 1/36 | 1/6 · 3 → 1 |
| q-242 | index 2.5 over √243 = 3 | index 1.5 over √125: (125^½)^(2/3) = 125^(1/3) | 5 · 3 → 1 |
| q-243 | 3·√7 = √63 | 2·√13; traps √26, √338 | √52 · 1 → 3 |
| q-244 | 3·∛2 = ∛54 | 3·∛4; trap ∛36 (squared instead of cubed) | ∛108 · 1 → 2 |
| q-245 | smallest of π, 3, ∛30, √7 | smallest of √10, ∛25, 3, π (one root a bit under 3, one a bit over) | ∛25 · 4 → 2 |
| q-246 | closest to √3: 1.6/1.7/1.8/1.9 | closest to √5: 2.1/2.2/2.3/2.4 (same check: 2.25² = 5.0625 > 5) | 2.2 · 2 → 2 |
| q-247 | x = √(5x): how many solutions | √(7x) = x; trap 1 (divided by x) | 2 · 3 → 2 |
| q-227 (Hebrew T8, now T9 practice) | (7³)^(2/3) = 49 | (6³)^(2/3) | 36 · 1 → 4 |
| q-r26-t09-19 (practice) | √3 + √5 vs √15: was the "Square of a sum" lesson example word for word | √5 + √7 vs √35: squares 12 + 2√35 vs 35 → √140 vs √529 (now "<") | < · 1 → 3 |
| alg-extra-root-practice-3 (practice) | √(x²), x < 0: the rule written on the Summary board | √(9x²), x < 0; trap 3x | −3x · 3 → 2 |

**Lesson "Roots — Fundamentals"** (the Hebrew lesson's examples; board item, click label and spoken line changed together):
√49 / x² = 49 → √36 / x² = 36 · √((−8)²) = 8 → √((−10)²) = 10 · √72 = 6√2, √200 = 10√2 → √48 = 4√3, √300 = 10√3, and
the "largest square" tip √72 = 2√18 → √48 = 2√12 = 4√3 ("12 is still divisible by four") · 3√5 + 2√5, √72 + √32 →
4√7 + 2√7 = 6√7, √48 + √75 = 9√3 · √75/√3 = 5 → √108/√3 = 6 · 6/√3 = 2√3 → 10/√5 = 2√5 · ∛(−64) → ∛(−125) = −5 ·
√(9 + 16) vs √9 + √16 → √(25 + 144) = 13 vs 5 + 12 = 17. "Bring a number inside": 3√7 = √63 < 8 was the Hebrew question
q-243 → 5√2 = √50 > √49 = 7.
Memory card: tips √72 → √48 = 4√3 and 6/√3 → 10/√5 = 2√5; examples ∛(5⁶) = 5² (the old q-235) → ⁴√(3⁸) = 3², 3√7 = √63 → 5√2 = √50.
No question in topic 9 is now the same as a lesson example in topics 1–9 (checked with a script). One question looks
close to a lesson rule but was kept: guided Q4 (0 < x < 1, which is largest). It applies the rule and is not a copy of an example.

**Order**
- Guided Question 1 (⁴√(9⁶), the fraction 3/2) moved to after q-235 and q-236. Those two are the easy "power over index" and
  "fourth root" items, so the order is now easy → hard. It is still Question 1.
- q-238 (√23 · √23) now comes before q-237 (√20 · √5): the easiest product comes first.
- Answer positions: every Hebrew key moved except q-246's (its choices go up in order, and the key is still choice 2).
- The practice is sorted from easy to hard.
- Not changed: the solution videos (written in English) and the traps and summary videos.

**Practice clean-up** (full build, with the T8 patch: 21 → 11 questions)
- Copies removed (each one checked): alg-extra-root-practice-6 (√12·√27, same as q-237), q-r26-t09-13 (√(2x+3) = 3, same as
  -5), alg-extra-exponent-extra-2 (27^(2/3), same as q-r26-t09-10 and the Summary example), q-r26-t09-14 (same as guided Q2).
- Extra-bank warm-ups: 3 kept: -3 (|x|), -2 (√45, pull out a square), exponent-extra-7 (√50 + √8, simplify and add). Removed: -1, -4, -5, -7.
- September items of a type the Hebrew already covers, removed: q-r26-t09-10 (8^(2/3); it was also the lesson example) and
  q-r26-t09-11 (⁴√(x⁸), same type as q-235).
- Kept, because the Hebrew does not cover these types: q-r26-t09-09 (between 0 and 1), -12 (where a root is defined), -15 (6th power),
  -16 (partner product), -17 (square of a sum), -18 (partner on the bottom), -19 (sum against a root). Plus q-227 (Hebrew).
  The result is 11 questions, one more than the target of 10. -16 is the warm-up for -18. It could go if the teacher wants exactly 10.

## 2026-10-06 review
- Lesson "Roots — Fundamentals" slide 7 and the memory card tip: the renumber pass used 10/√5 = 2√5, but that is the Hebrew
  question q-260 word for word. Changed to 12/√6 = 2√6 (board, click labels, speech: "twelve divided by six is two … Six is
  root six times root six"). Not used anywhere else in the course or the Hebrew base.
- (q-240 √98/√2 also clashed with the topic 10 lesson example; that was fixed in t10.py, q-240 stays.)
- Checked: every renumbered question's key, traps and explanation (python); lesson diff; practice removals. Note for the
  teacher: after the clean-up the topic 9 practice has no "√(ax+b) = c" root equation (q-r26-t09-13 and the extra -5 were
  both removed); topic 10 practice covers it (q-266, q-267).
