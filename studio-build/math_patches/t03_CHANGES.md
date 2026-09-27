# Topic 3 – Comparing Fractions: changes (course review 2026-09)

Patch: `math_patches/t03.py`. Check: `python3 math_check.py 3` → 0 problems, 0 warnings, 0 layout problems.
All keys (old and new) were re-solved; the new ones were also checked numerically with random values.

## 1. Wrong rules fixed (lesson video "Comparing Fractions" + memory card)
- **Cross-multiply "always works" / "eats everything, even letters" removed.** New condition everywhere: *both bottoms
  positive*. Slide 5 now also shows why it works: 5/8 = 55/88, 7/11 = 56/88 (the products are the new tops).
- **New slide "Negatives"** (after cross-multiply): the trap 1/(−2) vs 1/3 (products say the wrong answer), the fix
  "move the minus to the top", and ordering two negative fractions (−2/3 > −3/4: compare without the minus, then reverse).
- **Squaring** (slide "Roots? Square it"): "the bigger stays bigger" now says *for positive numbers*, with the
  counterexample −3 < 2 but 9 > 4 on the board.
- **Flipping** (slide "Flip them"): now says *only for the same sign*, with −2 < 3 and −1/2 < 1/3 on the board.
- **Recap slide** rewritten: cross-multiply with positive bottoms, list of shortcuts with their conditions, "signs first".
- "To decimals" slide: "remember what always works?" → "remember cross-multiplying?".
- Solution videos: Q8 (squaring) and Q10 (flipping) now say "all positive" before using the rule.

## 2. Methods added
- **Distance from 1 above 1** (slide 8): 7/6 = 1 + 1/6, 19/16 = 1 + 3/16 — compare the extras.
- **New slide "Add to top and bottom"**: 3/5 → 4/6 → 5/7 → 6/8 grows toward 1; above 1 it shrinks toward 1; positive numbers only.
- **New slide "x, x² or 1/x?"**: the order for 0 < x < 1, x > 1 and −1 < x < 0, each checked by plugging in (1/4, 4, −1/2).
- **New slide "Which numbers?"**: plug-in rules (legal values, avoid 0 and 1, two survive → a different kind of number)
  and the meaning of "necessarily true" vs "could be true".
- **Decimals to know** on the "To decimals" slide and in the card (1/2 ... 1/9).
- **Q10 solution: new Method 4 "Pieces of 1/5"** (strong students): each step adds 1 to the top and 5 to the bottom,
  which pulls the fraction toward 1/5 (3/16 < 1/5), so the list climbs.
- Sidebar of the lesson updated (14 labels); lesson now 15 slides.
- **New guided questions + solution videos** (placed after Q10):
  - Q11 `q-r26-t03-01` — a < 0 < b, which is necessarily true (signs first; flip and square traps). Key 1.
  - Q12 `q-r26-t03-02` — 0 < a < b, largest of a/b, (a+1)/(b+1), (a+5)/(b+5), 5a/5b (add to top and bottom). Key 3.
  - Q13 `q-r26-t03-03` — 0 < x < 1, the correct order of x², x, √x, 1/x (x-range table). Key 1.
  - All Topic-3 solution videos now show the sidebar Question 1–13.
- **Memory card** rewritten: sign condition in the intro and in every method row, new rows (Signs first, Add to top and
  bottom, Flip them), a table "x by range", a table "Decimals to know", three tips.

## 3. Text
- Every solution in the topic (10 guided + 17 practice) rewritten in TeX: no ":" for division, numbers shown in every
  step, no "so" mid-sentence. This fixes the broken Q1 solution ("2×7=14<15 …") and the Q7 solution.
- q-087: solution rewritten with two clear counterexamples (m = 0.4, n = 0.2 kills choice 1; m = 4, n = 2 kills choice 2).
- Stems: q-092 "4.5 · 0.2 : 30" → "4.5 · 0.2 ÷ 30" (Q3 video draw note too); q-093 "P, Q, R, S ≠ 0 (positive numbers)"
  → "P, Q, R and S are positive numbers"; q-094 "ratios … the ratio X/Y" → "expressions … X/Y", "X, Y ≠ 0" → "X ≠ 0 and Y ≠ 0";
  q-095 and q-088 conditions stacked with \begin{cases}; q-087 "distinct" → "different"; q-088 choices −2/5, −4/5 written with the minus in front.
- Spoken lines in all Topic-3 videos: "… — so …" / "…, so …" split into "… . So …".

## 5. Practice (17 → 22, ordered easy → hard)
- The four GRE-style "first / second / equal / cannot be determined" items rewritten as NITE questions with 4 numeric choices:
  t3-1-1 (which is greater than 1/2 — benchmark), t3-1-3 (x > 0, largest of four fractions with x), t3-1-6 (smallest of
  3/5, 2/3, 5/8, 7/11), t3-1-4 (now a new item: largest of 3/√2, 4/√3, 5/√5, 6/√7 — no longer the lesson example).
- Near-duplicates replaced (same ids, new content): t3-1-2 (was ≈ q-084) → smallest of 21/19, 22/20, 23/21, 24/22 (add to
  top and bottom above 1); t3-1-7 (was ≈ q-088) → −1 < x < 0, largest of x, x², x³, 1/x. t3-1-5 got a numeric solution.
- New practice: `q-r26-t03-04` (7/9 vs (7+x)/(9+x)), `-05` (x > 1, smallest), `-06` (a < b < 0, necessarily true),
  `-07` (largest of four negative fractions, minus in the bottom), `-08` (b < 0 < d and a/b < c/d → ad > bc: the
  negative-bottom cross-multiplying trap).
- Exam-level items now: q-087, q-088, q-090, t3-1-2, t3-1-4, t3-1-7, q-r26-t03-04, -06, -07, -08.
- Order: fraction operations (q-083, q-086, q-081, q-082) first as review, then comparison easy → hard.

## Not done / for the teacher to decide
- Nothing removed from the topic; no figures in this topic.
- "Roots? Square it" (slide 10) stays before the roots topic; it already says "we'll learn roots properly later".
  Move it later if you prefer.
- q-081, q-082, q-083 (fraction operations, not comparison) stay in the practice set, first. The API has no "label", so
  they are not labeled "review".
- The review asked to tell students that ":" means divide on the exam; the brief says never ":" for division, so the
  course now uses ÷ everywhere. Decide if you want to mention the exam's ":" once in the Q3 video.
- Q6 "a = b − 0.25/b − 1" in the review was only the text summary of the board; the board itself shows the TeX fraction.
- Tool note: `student_view.py` reads questions and cards from `content/full-course/topics/t3.json`, not from the patched
  build, so `tmp_check/view/t3.md` still shows the old questions, card and no new solution videos. The patched data
  itself was checked directly and on rendered slides.
- Solution-video `title` fields still hold the old raw stem text (e.g. `\frac{...}`); the API has no setter, and the
  visible slide header uses "Fraction Questions".
