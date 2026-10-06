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

## Pass 2 (2026-09-27, teacher-approved remove/restore plan)

**Removed:** nothing (the plan removes nothing in Topic 3).

**Restored (6 original practice questions, original stem, choices and key; clean-up only: TeX, numeric solutions):**
- alg-extra-unit-t3-1-1: "Which is greater: 3/7 or 5/9?" (first / equal / depends / second) - key: the second fraction.
- alg-extra-unit-t3-1-2: "Which is largest? 15/16, 4/5, 7/8, 10/11" - key 15/16.
- alg-extra-unit-t3-1-3: "Given x > 0. Which is greater: 7/(x+2) or 7/(x+5)?" - key: the first fraction.
- alg-extra-unit-t3-1-4: "Which is greater: 3/√10 or 2/√5?" - key: the first expression.
- alg-extra-unit-t3-1-6: "Which is smaller: 3/5 or 4/6?" - key: the first fraction.
- alg-extra-unit-t3-1-7: "Given c > 1. For which x is (c+x)/(c−x) the smallest?" (−1, 0, 1/2, 1) - key −1.

**New versions kept under new ids** (they test kept methods): q-r26-t03-09 (smallest of 21/19 ... 24/22),
q-r26-t03-10 (largest of 3/√2 ... 6/√7), q-r26-t03-11 (−1 < x < 0 order). The new versions of -1, -3 and -6 were dropped.
The "cross-multiplying always works" wording stays corrected (wrong rule). Practice re-ordered easy to hard (25 items).

**Summary video** `r26-t03-summary` "Comparing Fractions: Summary" (about 2.4 min), last item of the learn section,
right before the practice. Slides: Summary · Cross-multiply · Signs first · Quick shortcuts · Distance from 1 ·
Add to top and bottom · Square or flip · x by range · Plug in numbers · Before you practice.

## 2026-10-02 Hebrew check of the solution videos

Every sample-question video of the original Hebrew course was compared with its English solution video (function
`hebrew_check` in `t03.py`). Only spoken lines and "Write ..." draw notes were added; no slide, board item, question
or key changed. The Hebrew has 9 sample-question videos; `solve-q-fraction-compare` (7/15, 1/2, 9/17) has no Hebrew
video (it repeats the lesson's "compare with ½" method) and was left as it is.

| English video | Hebrew methods / tips | Added to the English |
|---|---|---|
| solve-q-091 (1−½)(1−⅓)(1−¼) (Hebrew: 1−⅓, 1−¼, 1−⅕) | complete to 1 = shortcut 1 (the long way with a common denominator shown first); fractions multiply top×top, bottom×bottom; cancel before multiplying = shortcut 2 | the long way (1 = 3/3), "shortcut one / shortcut two", how fractions multiply |
| solve-q-092 4.5·0.2÷30 (Hebrew: 2.5·0.2÷25) | way A fractions (0.2 = 2/10, one place after the point; ÷ = × reciprocal; to a decimal: make the bottom 100); way B decimals (count the places: 1 + 1 = 2; hundredths ÷ n) | "one place after the point", "make the bottom one hundred", the place count spelled out |
| solve-q-093 S/Q·P/S + R/Q | math (cancel, add tops) = recommended; plug in all 1s, check the choices are distinct FIRST, one plug-in is enough; the math is recommended, master the basics | why the choices are checked first; closing "recommended: the math; plug-in for practice / panic" |
| solve-q-094 X/Y | math: each choice expanded or not (squaring = ×X on top, ×Y on the bottom → equal only if X = Y); spot it → mark and move on; or cancel; plug-in X=1, Y=2; "both ways are good" | "equal only if X = Y — possible, not necessary", "don't see it? cancel", "both ways are good" |
| solve-q-095 a=(b−0.25)/(b−1) (Hebrew: b−½) | understanding top/bottom; plug in b = 2 choice by choice — choice 1 cannot be eliminated, three out → mark the fourth; "understand, but plug-in is excellent too" | the plug-in now goes choice by choice and eliminates three; closing "which way is better" |
| solve-q-096 0 < x/y < 1 (Hebrew: a/b) | late hard question with a trap; start with plug-in (understanding is harder); must eliminate 3; second plug-in — but which? 2,3 / 3,4 / 1,3 are useless (same case), both negative; closer to zero = bigger; verify choice 4 with negatives; understanding: two cases, bottom bigger in absolute value, number line, each choice possible / not necessary, flip > 1 | why plug-in first; "which second plug-in? not 2 and 3 — same case"; the "closer to zero" rule; choice 4 checked with the negatives; a number-line draw note; choice 3 in the understanding part |
| solve-q-097 largest of 2/√2, 7/√2, 2/√7, 7/√7 (Hebrew: 3, 5 and √3, √5) | 4 fractions, not 2 as in the lesson → tournament of easy pairs, 3 comparisons; squaring (estimates are enough: "more than 8 is enough"); understanding (tops and bottoms repeat: biggest top + smallest bottom); "pick what is comfortable" | why a tournament, "three comparisons", "no need for exact values", "the tops and bottoms repeat", "pick the one that feels comfortable" |
| solve-q-098 0 < p < 1 < q (Hebrew: x, y) | tournament (bottoms AND tops positive; final stuck → "open your eyes": order doesn't matter in addition → exactly 1; the other > 1); plug-in: "with letters you can always plug in", ½ is the easiest fraction, 2 for y would give fractions → smart choice 1.5; "both excellent" | tops positive, "now what? open your eyes", "order doesn't matter when you add", why not q = 2, "you can always plug in", "both excellent" |
| solve-q-099 3/16, 4/21, 5/26 (Hebrew: 2/11, 3/17, 4/23) | the FULL order is asked; common denominator is off the table (big bottoms, no calculator); way 1 same tops; way 2 cross-multiply — every pair = 3 comparisons, smarter: two + the choices; way 3 flip (creative) | "they want the full order", why a common bottom is out (it is 4368), "every pair = three comparisons" |

**The English has more than the Hebrew (kept):** Q1 video (benchmark ½ + cross-multiply check); q-091 "telescoping
product"; q-092 left-to-right rule and the 0.3 / 0.09 traps; q-095 "+/+" sign check; q-097 explicit "all positive"
before squaring; q-099 "all positive" before flipping and Method 4 "Pieces of 1/5".
**Hebrew points changed on purpose (kept):** the numbers of five questions differ from the Hebrew (changed in the
earlier adaptation) — the Hebrew methods were applied to the current numbers. "Cross-multiplying always works" stays
corrected to "both bottoms positive".

Check: `python3 math_check.py 3 32` → PROBLEMS 0, WARNINGS 0, LAYOUT problems 0. All nine changed videos rendered
(`tmp_check/t3sol-solve-q-0NN.png`); boards unchanged.

## 2026-10-02 new numbers (not identical to the Hebrew course)

Teacher: "the same concept but with different numbers". Function `new_numbers` in `t03.py` (runs last). Every question
that comes from the Hebrew course got new numbers: same concept, same method(s), same trap, same difficulty, same
answer type. Guided questions differ from BOTH the Hebrew study guide and the Hebrew sample-question video. Their
solution videos keep every slide and every teaching step (including today's Hebrew-check additions); only the numbers
changed — spoken lines, "Write ..." notes, the q-099 method-4 title, and the video title shown in the list.
`q-fraction-compare` (source: "New companion question", not from the Hebrew) was left as it is. Not touched:
`alg-extra-unit-t3-*`, `q-r26-t03-*`.

| Question | Hebrew study guide (and Hebrew video) | New | Key | Still the same concept / trap |
|---|---|---|---|---|
| q-091 (guided) | (1−½)(1−⅓)(1−¼) = ¼ (video: (1−⅓)(1−¼)(1−⅕) = ⅖) | (1−¼)(1−⅕)(1−⅙) = ½; choices ½, ⅓, ¾, ⅚ | 1 | complete to 1, then the product telescopes (4s and 5s cancel); distractors = the first / last bracket |
| q-092 (guided) | 4.5 · 0.2 ÷ 30 = 0.03 (video: 2.5 · 0.2 ÷ 25 = 0.02) | 5.5 · 0.2 ÷ 22 = 0.05; choices 0.05, 0.5, 0.11, 1.1 | 1 | fractions way (11/2 · 1/5 · 1/22 = 1/20, make the bottom 100) and decimals way (55 · 2, two places → 1.1, then ÷ 22); traps one decimal hop away |
| q-093 (guided) | S/Q · P/S + R/Q = (P+R)/Q (video: D/A · B/D + C/A) | 2z/y · x/z + w/y = (2x+w)/y; choices (2x+w)/y, (2x+w)/(2y), (x+w)/y, (z+w)/(2y) | 1 | cancel, then add tops; all-1s plug-in gives 3, 3/2, 2, 1 — all different, one plug-in is enough |
| q-094 (guided) | X/Y; 7X/7Y, X²/Y², X·Y/Y², X²/(YX) → X²/Y² (video: A/B, 5A/5B) | m/n; 4m/4n, m·n/n², m²/n², m²/(nm) → m²/n² | 3 (was 2) | "not necessarily equal": squaring = ×m on top, ×n on the bottom; plug-in m = 1, n = 2 gives ¼ |
| q-095 (guided) | b > 1, a = (b−0.25)/(b−1) (video: b − ½) | b > 2, a = (b−1.5)/(b−2); plug-in b = 3 → 1.5 | 1 | top loses less than the bottom → a > 1; same 4 choices (a > 1, 0 < a < 1, −1 < a < 0, a < −1) |
| q-096 (guided) | 0 < x/y < 1; y<x, x<y, xy = 1, 1 < y/x (video: a/b) | 0 < x/y < ⅓; y<x, x<y, xy = 3, 3 < y/x | 4 | plug x = 1, y = 4 leaves choices 2 and 4; the second plug-in must be two negatives (−1, −4); flip → y/x > 3 |
| q-097 (guided) | 2/√2, 7/√2, 2/√7, 7/√7 (video: 3, 5 over √3, √5) | 4/√2, 9/√2, 4/√6, 9/√6; squares 8, 40.5, under 3, 13.5 | 2 | tournament (same bottoms, then same top), squaring, biggest top + smallest bottom |
| q-098 (guided) | 0 < p < 1 < q (video: 0 < x < 1 < y) | 1 < p < 2 < q; same four expressions; smart plug-in p = 1.5, q = 2.5 (not 3) → ¼, 1, 1.5, 2.5 | 4 | tournament: choice 2 is exactly 1, choice 4 is more than 1; "why not a whole number for q" kept |
| q-099 (guided) | 5/26, 4/21, 3/16 (video: 2/11, 3/17, 4/23) | 6/19, 5/16, 4/13 | 1 | same tops (60/190, 60/192, 60/195); cross-multiply 64 < 65, 95 < 96 (choices 2 and 4 out, then 3); flip 3⅙, 3⅕, 3¼; "pieces of 1/3" (+1 top, +3 bottom; 4/13 < 1/3) |
| q-081 | (¼ + ⅙) ÷ 25/12 = ⅕ | (⅙ + 1/10) ÷ 16/15 = ¼; choices ½, ¼, ⅓, ¾ | 2 | add the top, then multiply by the reciprocal; the 15 cancels |
| q-082 | (a/c · d/a) ÷ (c/b · a/c) = bd/ac | (2b/d · c/b) ÷ (d/a · b/d) = 2ac/bd; choices 2bc/ad, 2ac/bd, 2c²/d², bd/(2ac) | 2 | cancel in the top and the bottom, then divide; traps: multiplying instead of dividing, the upside-down answer |
| q-083 | ⅙ + ¼ − ⅓ = 1/12 | ⅛ + ⅙ − ¼ = 1/24; choices ⅛, 1/12, 1/48, 1/24 | 4 | least common denominator 24 (not 8 · 6 = 48) |
| q-084 | largest of 6/7, 7/8, 8/9, 9/10 | 16/17, 17/18, 18/19, 19/20 | 4 | distance from 1 |
| q-085 | L = 3/7 − M; 2/7, 9/28, 5/14, 13/35 | L = 4/9 − M; 1/3, 13/36, 7/18, 11/28 | 4 | smallest L ↔ largest M; 12/36 < 13/36 < 14/36, then cross-multiply 196 < 198 |
| q-086 | not equal to ¾: −1 + 7/4, 2 − 5/4, 21/28, 9/16 | not equal to ⅔: −1 + 5/3, 3 − 7/3, 14/21, 4/9 | 4 | the squared fraction (4/9 = (2/3)²) is the one that is not equal |
| q-087 | m/n integer: 1 < m−n, 0 < m−n < 1, 1 < n/m, 0 < n/m < 1 | 2 < m−n, 0 < m−n < 2, 2 < n/m, 0 < n/m < 1 | 4 | m/n ≥ 2 → 0 < n/m ≤ ½; m − n can be small (1, 0.5) or big (6, 2) |
| q-088 | a > 1; x = 1, 2/5, −2/5, −4/5 | a > 2; x = 2, 1/3, −1/3, −2/3 | 4 | bottom positive; smaller x → smaller top and bigger bottom; check with a = 3 |
| q-089 | smallest of 7/6, 9/7, 19/15, 19/16 | 13/12, 11/9, 25/21, 25/23 | 1 | above 1: compare the extras (1/12 vs 2/23 is close: 23 < 24) |
| q-090 | order of 6/50, 5/38, 4/33 | order of 3/25, 4/31, 5/41 | 3 | cross-multiply pairs (123 < 125, 155 < 164); decimals 0.12, 0.122, 0.129 |

No new question repeats another topic-3 question or a lesson / summary example (q-097 avoids 3/√2 of q-r26-t03-10;
q-089 no longer repeats the lesson's 7/6 and 19/16). All new numbers solved from scratch (python check).

Check: `python3 math_check.py 3 32` → PROBLEMS 0, WARNINGS 0, LAYOUT problems 0. All nine guided videos rendered
(`tmp_check/t3new-q-0NN.png`); the student view `tmp_check/view-3-32/t3.md` read for all 19 changed questions.

## 2026-10-02 review: same message

Teacher: "make sure all the new questions really convey the same message; if something has 2 methods, the English
must have 2 methods too." Each of the 15 renumbered questions (guided q-095 … q-099, practice q-081 … q-090) was
compared with the Hebrew sample-question video and the base English version (idea, condition, trap, difficulty,
answer type, and every method re-done with the new numbers). q-091 … q-094 are recorded and were not touched.

| Question | Verdict | Methods (Hebrew / base → English now) |
|---|---|---|
| q-095 | same message ✓ (b > 2, top loses 1.5, bottom loses 2 → a > 1) | 2 → 2 (top vs bottom; plug in b = 3, three choices out) |
| q-096 | **fixed**: "0 < x/y < 1/3" added a new idea (flip → > 3). Back to **0 < m/n < 1**; letters m, n; choices reordered (m·n = 1, n < m, 1 < n/m, m < n), key 3. Plug-ins m = 1, n = 3 (leaves 3 and 4), then m = −1, n = −3 (removes 4) | 2 → 2 (plug in twice incl. both negative; understanding: same sign, bottom bigger in absolute value, number line, flip > 1) |
| q-097 | same message ✓ (4, 9 over √2, √6) | 3 → 3 (tournament, 3 comparisons; squaring 8, 40.5, < 3, 13.5; biggest top + smallest bottom, tops and bottoms repeat) |
| q-098 | **fixed**: "1 < p < 2 < q" lost the fraction-vs-above-1 idea. Back to **0 < a < 1 < b**; letters a, b; choices reordered (a/(b−a), b/(b−a), (b−a)/(a+b), (b+a)/(a+b)), key 2 | 2 → 2 (tournament: semi-finals on the shared bottoms, final = exactly 1 vs top > bottom; smart plug-in a = ½, b = 2.5 (not 3) → ¼, 5/4, ⅔, 1) |
| q-099 | same message ✓ (6/19, 5/16, 4/13) | 3 → 3 + the English extra (same tops 60; cross-multiply with two comparisons + choices; flip; pieces of 1/3) |
| q-081 | same ✓; **added** base method 2 to the written solution (multiply top and bottom by 30 → 8/32) | 2 → 2 |
| q-082 | same ✓; **added** base method 2 (multiply by the flip of the bottom product, cancel across) | 2 → 2 |
| q-083 | same ✓; **added** base method 2 (first and last fractions first: −1/8 + 1/6 = 1/24) | 2 → 2 |
| q-084 | same ✓; **added** the base "common bottom" method as a note (works, but 58,140 → distance from 1 is the smart way) | 2 → 2 |
| q-085 | same ✓ (direction of subtraction + compare) | 2 → 2 |
| q-086 | same ✓ | 1 → 1 |
| q-087 | same ✓ (m/n ≥ 2 → flip; m − n small or big) | 2 → 2 |
| q-088 | same ✓ | 1 → 1 (+ check with a = 3) |
| q-089 | same ✓; **added** a decimals check (the base solution's method) | 2 → 2 |
| q-090 | same ✓ (cross-multiply pairs + decimals, as in the base) | 1 → 2 |

All numbers re-solved in python. Check: `python3 math_check.py 3 32` → PROBLEMS 0, WARNINGS 0, LAYOUT problems 0.
Rendered `tmp_check/t3rev-q-096.png` and `tmp_check/t3rev-q-098.png`.

## 2026-10-02 Fractions summary

Teacher: the "Comparing Fractions summary" should be a **Fractions summary** — a short review of the main ideas of
the whole fractions unit before the mixed practice, not the basics (those are in the topic 2 summary). Same video id
(`r26-t03-summary`) and place (end of the learn section, right before "Independent practice").

- Title: "Fractions: Summary". The title slide points back to the basic moves already reviewed; nothing basic is repeated.
- 8 concept slides, each one rule + one mini example with fresh numbers (all checked in python):
  1. Calculate smart — complete to 1 and cancel in a chain: (1+1/4)(1+1/5)(1+1/6) = 7/4; decimals → fractions,
     bottom 100: 1.2 · 0.5 ÷ 15 = 1/25 = 0.04 (q-091, q-092).
  2. Letters in fractions — cancel, then add the tops: a/c · b/a + d/c = (b+d)/c; expanding keeps the value,
     squaring or adding to both does not (x = 1, y = 3) (q-093, q-094).
  3. Cross-multiply, signs first — 4/9 ? 3/7: 28 > 27; 4/(−9) ? −3/7: −4/9 < −3/7 (lesson slides 5–6, q-r26-t03-01).
  4. Shortcuts — benchmark ½ (6/13 < ½ < 10/19), make the tops match (4/7 = 8/14 > 8/15), distance from 1
     (20/21 < 24/25) (lesson slides 2–4, 8).
  5. Square or flip — 3/√5 > 4/√10 (18/10 > 16/10); 4/17 < 5/21 (flips 4¼ > 4⅕) (lesson slides 10, 13, q-097, q-099).
  6. Top vs bottom — k > 3: (k−1)/(k−3) > 1; add to both → toward 1 (2/9 < 1/2, 9/4 > 2); 0 < p/q < 1: same sign,
     q farther from 0, q/p > 1; p = −2, q = −5 shows q < p (q-095, q-096, q-r26-t03-02).
  7. Many fractions — tournament 3/10, 7/10 | 7/11, 7/9 → 7/9; full order: compare two, cross out choices (q-097–q-099).
  8. Plug in numbers — legal values (0 < x < 1: x = 1/3 gives 1/9 < 1/3 < 1 < 3), smart values (a = ½, b = 1½ give
     whole numbers), a second plug-in of a different kind (lesson slides 11–12, q-096, q-098, q-r26-t03-03).
- "Before you practice": signs first · both bottoms positive before cross-multiplying · which shortcut do the numbers
  invite · legal values with letters.

Check: `python3 math_check.py 3 32` → PROBLEMS 0, WARNINGS 0, LAYOUT problems 0. Rendered `tmp_check/fracsum.png`.


## 2026-10-04 question = lesson example fixed
- alg-extra-unit-t3-1-4 was the example 3/√10 vs 2/√5 of "compare-fractions" (recorded) -> now 3/√6 vs 2/√3 (squares 9/6 > 8/6); answer still choice 2, the first.

## 2026-10-06 review
Course-wide duplicate scan: practice q-r26-t03-11 was identical to guided q-r26-t12-01 (−1 < x < 0, largest of x, x², x³,
1/x) and close to q-r26-t08-11. It now asks for the SMALLEST of the same four (answer 1/x, choice 4).
Function `review_dups` at the end of t03.py.

## 2026-10-06 Hebrew back-check
Every topic-3 question (guided + practice), lesson slide and card example compared with the teacher's Hebrew video subtitles
(01-Algebra-Original-Subtitles.txt, lines 1438–2270 "השוואת שברים" + "שברים" sample questions; 632–1435 glanced).
Function `hebrew_backcheck(M)` runs last in t03.py.

Fixed (not recorded):
| item | old (= Hebrew) | new | answer |
|---|---|---|---|
| q-fraction-compare + solve-q-fraction-compare | 7/15 < ½ < **9/17** ("half of 17 is 8.5, 9 > 8.5" = Hebrew lesson's benchmark example 5/11 vs 9/17) | 7/15 < ½ < **11/21** (half of 21 is 10.5, 11 > 10.5; check 2·11 = 22 > 21) | choice 1 (unchanged); video speech + draw cue + board question rewritten |
| card "Comparing fractions" → Square them | 3/√10 > 2/√5 because 9/10 > 4/5 (the Hebrew lesson example) | 4/√19 > 3/√11 because 16/19 > 9/11 (176 > 171) | — |

Recorded (listed only, not changed): lesson `compare-fractions` uses Hebrew lesson examples 5/11 vs 15/34 (→15/33), 2/5 vs 3/8
(0.4 / 0.375), 3/√10 vs 2/√5, plug-in x = ½, y = 2 with y/(y−x) vs (y−x)/(y+x) (4/3 vs 3/5); guided q-091 (1−½)(1−⅓)(1−¼)
shares two factors with the Hebrew (1−⅓)(1−¼)(1−⅕); q-093 = Hebrew D/A·B/D + C/A with letters changed; q-094 = Hebrew
A/B question with letters changed; q-096 = Hebrew 0 < a/b < 1 question with letters changed; summary `r26-t03-summary`
slide 4 shows the same letter pattern. Left: card "plug in x = ½, y = 2" (standard values, mirrors the recorded lesson);
practice q-084 (16/17 … 19/20) shares only 16/17 with the Hebrew distance-from-1 example (16/17 vs 12/13) — not a match.
Checks: keys recomputed (7/15 < ½ < 11/21; 16/19 > 9/11); 11/21 and 4/√19, 3/√11 appear nowhere else in topics 1–3 nor
in the Hebrew. `python3 math_check.py 3 32` → 0 / 0 / 0. Rendered solve-q-fraction-compare (tmp_check/hbc3.png).
