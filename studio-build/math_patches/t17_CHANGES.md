# Topic 17 — The Number Line: changes (course review 2026-09)

Patch: `math_patches/t17.py`. Check: `python3 math_check.py 17` → 0 problems, 0 warnings, 0 layout problems.

## 1. Wrong or unclear rules fixed (priority 1)
- **Negative exponents now get the same message everywhere.** With the arrows, you keep the negative exponent (−1 is just a small power). Without the arrows (comparing ranges, or "same operation"), you flip it first. Both ways give the same answer.
  - Lesson 1, slide 6 (Exceptional powers): two new lines say when to flip and point ahead to the arrows.
  - Lesson 2, slide 7 (Three steps): the "No need to flip" line is replaced by the two-case rule.
  - Lesson 2 recap: new board line "Negative side: odd powers only · negative exponent: keep it".
  - Memory card: the tip "a negative exponent flips the base" now gives the two-case rule.
- **"Odd" is now defined for a negative base** (Lesson 2, slide 5, new board line "Odd: 3, 5, −1, −3, 1/3, 1/5"): any power that keeps the minus sign, including odd roots and negative odd powers. Lesson 2, slide 2 now says "Negative fractions: right — for odd powers." The same wording is on the card.
- **Hierarchy (Lesson 1, slide 5):** "ALWAYS bigger, whatever power or root" now says "after any positive power or root; for negatives, odd ones only", on the board and in the script.
- **Same operation (Lesson 1, slide 7):** now says "positive numbers only", with the counter-example −3 < −2 but (−3)² > (−2)² on the board. The card tip says the same.
- **Q8 (q-500), Method 2:** removed the invalid "replace every ten with a two" trick. New plug-in: x = 1/1024 = (1/2)¹⁰, which has a clean tenth root. Added a warning: change only x, never the numbers in the question.
- **Q3 (q-495) written solution:** replaced the wrong reason with a correct one (b·a² = ab·a, a·b² = ab·b, and a < b).
- Lesson 1, slide 4 and the card: "12 : 3" became "12 ÷ 3" (and "12 ÷ 1/3"). Slide 4 now ends by pointing ahead to multiplying by a negative number.
- Lesson 1 recap: board lines now include the conditions (positive powers and roots; flip a negative exponent; positive numbers only).
- The review's "broken board text" (four ranges) was an export artifact. The boards were fine, so nothing changed there.

## 2. Missing methods added (priority 2)
**New lesson video `r26-t17-reading-the-line`, "Reading the Number Line"** (8 slides, about 4.6 min). It is the first item of the advanced section, before Q3:
1. Times a negative: you land on the other side of zero and the order flips (2 < 5 → −2 > −5). A negative fraction times a number above 1 moves away from zero, so it gets smaller.
2. Reciprocals: the full table for the four ranges. For numbers with the same sign, the order flips (2 < x < 5 → 1/5 < 1/x < 1/2).
3. Test numbers: 2, 1/2, −1/2, −2, plus the borders −1, 0, 1 when they are allowed. "Nice numbers" for roots: 1/4, ±1/8, −1/32.
4. Must or could: for "necessarily", one counter-example is enough to rule it out, and you find one by pushing the values to the edges. For "could", one example is enough to prove it.
5. Picture questions: write the range under each letter. Unless the figure is "drawn to scale", trust only the order of the points, not the distances. The slide has a number-line figure.
6. Distance and midpoint: distance = bigger − smaller; midpoint = (a+b)/2; "a third of the way".
7. Recap.

**New memory card `mem-r26-t17-reading`** (after the new lesson): a reciprocal table, a table of numbers to plug in, and a distance and midpoint table, plus tips.
The existing card also got a new row: "× a negative number".

**Five new guided questions, each with a solution video** (Q10–Q14, at the end of the advanced section):
- Q10 `q-r26-t17-01`: picture with a, b, c, d. Which is necessarily negative? (Answer: choice 2, b·c·d.)
- Q11 `q-r26-t17-02`: picture with x and points K, L, M, N. Which point could be √x? (Answer: choice 3, M.)
- Q12 `q-r26-t17-03`: −4 < x < −2, find the range of 6/x. Reciprocals with negative numbers. (Answer: choice 3.) The video shows two methods.
- Q13 `q-r26-t17-04`: x < −1 < y < 0, which is necessarily true? The test at the edges shows xy can equal 1. (Answer: choice 2, x+y < −1.)
- Q14 `q-r26-t17-05`: a point one third of the way from −7 to 5. (Answer: choice 3, −3.)

The old Q9 video no longer says "That's the number line done". The sidebars of the advanced solution videos now list Questions 3–14.

## 3. Text (priority 3)
- All 9 guided and all remaining practice questions were rewritten in TeX: no ":" for division, spaces after commas, and no decimals like −0.794 that you can't work out by hand. The solutions now use nice numbers (t = −1/8, x = −1/32, x = 1/1024, and so on) and the methods taught in the lessons.
- Choices were cleaned up (for example "\left(r − q\right) < \left(s − p\right)" → "r − q < s − p"). The "orderings" stem of q-499 was reworded. q-503's exponent "−1/2" was fixed, and in the extra item t17-3-4 the impossible choice "1/2 < 1/x < 1/5" was replaced.
- q-504 (the gap a − b) is kept, now worded as a distance on the number line, so it fits the new distance slide. The review suggested moving it to T12 or T20.
- Video titles and slide notes now match the new stems.

## 4. Figures (priority 4)
- There were no figures in this topic before. There are now 6 new number-line SVGs in the course figure style (viewBox 640×160, axis #71818d, dots #087f83, labels #203344 in DejaVu Sans). They are used by 5 questions and 1 lesson slide. Only the order of the points matters, and every stem says "not drawn to scale". The renderer also adds its own "not drawn to scale" note.

## 5. Practice (priority 5)
- **Removed:** q-505 (Q3 turned around) and extra t17-3-1 (a one-step question).
- **Added 10 exam-level items:**
  - `-06`: picture, smallest of a, ab, a/b, a²
  - `-07`: picture, x/y − 1 is positive
  - `-08`: picture, which point could be x³
  - `-09`: reciprocal of −2 < x < −1/2
  - `-10`: range of 1 − 3x (a negative multiplier)
  - `-11`: x³ < x, border trap: −1, 1 and −1/2 all fail
  - `-12`: point twice as far from A as from B
  - `-13`: "could equal 1"
  - `-14`: 0 < x < 1 < y, counter-examples at the edges
  - `-15`: 1/a vs b/a vs 1/b
- The practice set is now ordered easy → hard. It has 25 items (was 17), and about 12 of them are exam level.

## Counts
- Questions: 23 rewritten, 15 added (5 guided + 10 practice), 2 removed.
- Slides: 9 changed (Lesson 1 slides 4, 5, 6, 7, 9; Lesson 2 slides 2, 5, 7, 9; Q8 slide 3; Q9 one line).
- Videos: 6 added (1 lesson + 5 solution videos).
- Cards: 1 updated, 1 new.
- Figures: 6 new.

## For the teacher to decide
- The new lesson comes before Q3, so Q4, Q5 and Q9 can use "must/could" and negative multipliers. If you prefer it after Q9, move `r26-t17-reading-the-line` and its card.
- Comparing powers with different bases (2³⁰ vs 3²⁰) is not repeated here. It is taught in the T10 patch.

## Pass 2 (teacher-approved plan, 2026-09-27)

### Part A: remove / restore
- **Removed:** nothing (the plan keeps every addition, including q-r26-t17-02 / -08, "which marked point could be √x / x³").
- **Restored (2 questions, 1 choice):**
  - q-505 (1 < m < n, which is the largest?) is back in the practice. Text in TeX, and the solution shows the numbers (m = 2, n = 4) and the "strong on strong" reason.
  - alg-extra-unit-t17-3-1 (−1 < x < 0, which is the largest?) is back in the practice, with a worked check (x = −1/2).
  - alg-extra-unit-t17-3-4: the original distractor "1/2 < 1/x < 1/5" is back as choice 2 (it replaces "−1/2 < 1/x < −1/5"). Key unchanged (choice 1).
- The practice order stays easy → hard: t17-3-1 goes in the easy group, q-505 in the middle (after q-503).
- No action (as planned): the "replace every ten with a two" fix in solve-q-500 and the q-503 fix stay.

### Part B: summary lesson
- New video `r26-t17-summary` "The Number Line: Summary" (about 3.5 minutes). It is the last item of "The number line · advanced study", right before the independent practice (this topic has one practice section, so one summary).
- Slides: Summary · Four ranges · Multiply & divide · Hierarchy · Exceptions first · The arrows · Reciprocals · Test numbers · Must or could? · Distance & midpoint · Before you practice.
- Content comes only from the two lessons and "Reading the Number Line". The final slide has these checks: which range, are the borders allowed · any exceptions · positive or negative (mirror, flip for times a negative) · necessarily or could. It also lists the common traps.


## 2026-10-04 question = lesson example fixed
- Lesson "r26-t17-reading-the-line" slide 5 broke "r + q < s + p" for 0 < p < q < 1 < r < s - the answer of guided q-496 -> now 0 < a < b < 1 < c < d, "is d − c < b − a?", broken by a = 0.4, b = 0.5, c = 1.1, d = 3.

## 2026-10-05 cut repeats
Function `cut_repeats` (runs after `dedupe_examples`). Nothing in topic 17 is recorded. The two first lessons are unchanged.
- **`r26-t17-reading-the-line` "Reading the Number Line"**: 4.7 → 2.4 min. Kept: times a negative, reciprocals, test numbers + borders (no question video teaches them as rules).
  - Cut "Must or could?" → taught in Q4 `solve-q-496` (push to the edges to break it), Q9 `solve-q-501`, Q13. Added in Q4 one line + board item: "Necessarily true? One counter-example kills it — push to the edges".
  - Cut "Picture questions" → taught in Q10 `solve-q-r26-t17-01` (range under each letter; not to scale). Added there one line + pen note: trust only the order, not the distances (a board item did not fit next to the figure).
  - Cut "Distance & midpoint" → its example "from −7 to 5, a third of the way" WAS question Q14 `solve-q-r26-t17-05`. Q14 now explains the midpoint trap with the formula (+ board item "Midpoint = (a + b)/2"). Card `mem-r26-t17-reading`: the "a third of the way" example changed to −8 + ⅓ · 12 = −4.
  - "Test numbers": the clean-root numbers (¼, ⅛, 1/32) are taught in Q7 and Q8 → replaced by one line. They stay on the card.
  - Cut "Recap".

## 2026-10-06 new exam methods
Function `add_methods` (runs last). Card "The number line — ranges and arrows": new table "Signs hidden in the given" (second table, after the powers table): x² < x → 0 < x < 1; x < 2x → x > 0; x/3 > x → x < 0; a < b < 3a → a > 0, so b > 0 — each with the reason. No video changed.


## 2026-10-06 practice: new methods
Nothing added. The one fitting question for "signs hidden in the given" (q-510, 3a < x < a) already uses it as its first step; the range questions already test one number per choice.
All new lines verified numerically (python: fitting values, choice values, power by scaling). `math_check.py 17 32`: PROBLEMS 0, WARNINGS 0, LAYOUT 0.

## 2026-10-06 renumber pass

Goal: the English course must not look like the Hebrew course. Every Hebrew-derived item now has new numbers, letters or story, and the choices are in a new order. The concept, the trap, the level and the methods stay the same. Nothing in topic 17 is recorded (no takes in ~/Documents/Course.recordings), so nothing had to be kept as it was. Code: `renumber_pass()` at the end of t17.py, which runs last.

**Counts:** 9 guided questions renumbered, with all 9 solution videos rewritten (board cues, spoken lines and choice numbers). 10 practice questions renumbered. About 25 lesson examples renumbered across both Hebrew lessons, plus the matching examples on the two memory cards. Practice went from 27 to 17 (the audit target was about 15).

**Practice clean-up:**
- Removed 2 copies: q-r26-t17-10 (the same stem as alg-extra-4, "2<x<5") and alg-extra-1 (a copy of t01/t03/t08 items).
- Removed 3 extra warm-ups (3 kept: distance, midpoint, a<−2): alg-extra-2 (it repeats the lesson's 0<x<1 example with x=1/4), alg-extra-4 (it was exactly the "Reading the line" lesson example 2<x<5 → 1/5<1/x<1/2) and alg-extra-7.
- Removed 5 September items whose type the Hebrew practice already covers: -07 (a second "picture → expression" question; -06 stays), -11 (a "could be" question on x³<x; q-509 covers it), -13 (could equal 1), -14 (necessarily true with 0<x<1<y), -15 (the largest with reciprocals).
- **Kept on purpose (4 September items, types the Hebrew practice lacks):** -06 (picture → expression), -08 (picture → which point), -09 (range of 1/x for negatives), -12 (a point dividing a segment 2 : 1). This is why the total is 17, not 15.
- The new practice order runs from easy to hard.

**Card fixes:** mem-r26-t17-reading had the examples 5−(−8)=13 and (−9+3)/2=−3, which are exactly practice warm-ups alg-extra-3 and -6. They are now 7−(−3)=10 and (−10+4)/2=−3. The "Tenth root" row is now "Sixth root, x=1/64", to match Q8.

### Guided (old → new · answer)
| id | old | new | answer |
|---|---|---|---|
| q-493 Q1 | 1<a<b<c<d; not correct: a·d<c (choice 4) | 1<p<q<r<s; choices reordered; p·s<r | choice 2 |
| q-494 Q2 | −1<t<0, smallest of t⁶, t⁵, ∛t, t⁻¹ | −1<m<0, smallest of m³, m⁻³, m⁸, ⁵√m (exception + root→power + arrows kept) | choice 2, m⁻³ |
| q-495 Q3 | 1<a<b<c, smallest of b·c², a·b², b·a², b³; plug-in 2,3,4 | 1<x<y<z, smallest of x·y², y³, y·z², y·x²; plug-in 2,3,5 → 18, 27, 75, 12 | choice 4, y·x² |
| q-496 Q4 | 0<p<q<1<r<s; counter-example r=1.1, q=0.9, s=1.2, p=0.1 | 0<a<b<1<c<d; choices reordered; test numbers c=3, a=¼; d=6, b=⅓; counter-example c=1.2, b=0.8, d=1.3, a=0.2 → 2 > 1.5 | choice 2, c+b<d+a |
| q-497 Q5 | −1<a<0<b<c<1, largest; a=−½, b=¼, c=½ | −1<k<0<m<n<1; reordered; k=−½, m=⅓, n=½ → −1/4, −1/2, −1/12, −1/6 | choice 3, k·m·n |
| q-498 Q6 | x⁶<x⁵ → range | x⁴<x³ → range; ranges reordered; tests 16 vs 8, 1/16 vs 1/8 | choice 4, 0<x<1 |
| q-499 Q7 | −1<x<0, order x⁵, x, ⁵√x, x⁻⁵; x=−1/32 | −1<y<0, order y⁷, y, ∛y, y⁻⁷; y=−1/8; all 3 methods (axis, plug-in, power-sequence shortcut) kept | choice 3, y⁻⁷<∛y<y<y⁷ |
| q-500 Q8 | 0<x<1, largest of x¹⁰, ¹⁰√x, 10x, 10/x; x=1/1024 | 0<t<1, largest of 6t, 6/t, t⁶, ⁶√t; t=1/64 → 6/64, 384, tiny, ½ | choice 2, 6/t |
| q-501 Q9 | a²<a<c·b<b<c; 0.1/0.3/0.5 and 0.3/0.5/0.9 | p²<p<r·q<q<r; reordered; 0.2/0.5/0.6 (sum 0.8) and 0.4/0.7/0.8 (sum 1.2) | choice 4, p+r<1 |

### Practice (old → new · answer)
| id | old | new | answer |
|---|---|---|---|
| q-502 | 0<x<y<1, necessarily >1: y/x | 0<m<n<1; reordered; n/m (counter-example ⅓+½=5/6) | 3 |
| q-503 | largest of (1/3)^{2, ½, −½, −2} | base 1/5, same exponents; (1/5)⁻²=25, trap √5 | 2 |
| q-504 | b<a, ±2 changes, distance grows by 4 | d<c, ±3 changes, grows by 6 | 2 (add 3 to c, subtract 3 from d) |
| q-505 | 1<m<n, largest; m=2, n=4 | 1<p<q; p=2, q=5 → 20, 8, 125, 50 | 3, q³ |
| q-506 | 0<\|b\|<1, w=b⁴ | 0<\|c\|<1, k=c⁶ | 3, 0<k<\|c\| |
| q-507 | 0<a<b<1/3; a²+b², 3b, a+b, b/a | 0<m<n<1/4; 4n, n/m, m+n, m²+n² | 2, n/m |
| q-508 | −1<y<0; 1/y, y⁵, 5y, y | −1<k<0; 3k, k, k³, 1/k | 3, k³ |
| q-509 | x⁵<x<x⁴ → range | x⁷<x<x⁶ → range | 2, x<−1 |
| q-510 | 3a<x<a, largest | 4b<y<b; check b=−1, y=−3 | 3, y² |
| q-511 | −1<P<0<Q<1, smallest of 0, PQ, P²Q², P³Q³ | −1<M<0<N<1; 0, MN, M⁴N⁴, M³N³ (still one even power and one odd power) | 4, MN |

### Lesson examples (unrecorded Hebrew lessons) and cards
- **The Number Line:**
  - Mirror: 12·3=36 / 12·⅓=4 → 15·2=30 / 15·⅕=3. The number line from −40 to 40 still covers these numbers; I rendered it to check.
  - Multiply & divide: 8·3=24, 12÷3=4, 12·⅓=4, 12÷⅓=36 → 9·2=18, 10÷5=2, 10·⅕=2, 10÷⅕=50.
  - Hierarchy: ⁵√(9/8) vs √(5/6) → ⁵√(11/10) vs √(7/9).
  - Exceptions: (−3)², (2/5)⁻² → (−5)², (3/8)⁻².
  - Same operation: 7⁻³ vs 6⁻³ → 5⁻⁴ vs 4⁻⁴.
- **Powers on the Number Line:**
  - Each range: 3, 9, 27 → 5, 25, 125. 1/64 < 1/16 < 1/4 < 1/2 → 1/729 < 1/81 < 1/9 < 1/3. (−½)³ → (−⅓)³ = −1/27. (−3)³ = −27 → (−2)³ = −8.
  - Finding the range: x<x³<x² → x<x⁵<x⁴ (answer still −1<x<0).
- **mem-number-line card:** updated to the same examples.

### Verification
- I brute-forced every renumbered question with random values in its range. Each has exactly one correct choice, and it matches the key. The "not necessarily" and "possible" items come out as sometimes-true. Q7 has exactly one order that is always true. All the worked numbers in the videos and solutions were recomputed.
- Duplicate check against topics 1–17 (questions and lesson or card text): no identical items. The only overlap is q-498 and q-509 sharing the four standard range choices, which is natural.
- `python3 math_check.py 17 32`: PROBLEMS 0, WARNINGS 0, LAYOUT 0. I rendered both lessons and all 9 solution videos (tmp_check/ren17a/b/c.png) and checked them.

## 2026-10-06 review (of the renumber pass)
Checked every renumbered guided and practice question (keys brute-forced, one correct choice, traps kept, same type and
level), the lesson/card examples, and all 9 rewritten videos.
- **Fixed:** the rewritten videos of Q4–Q9 (solve-q-496 … solve-q-501) had lost their number-line board items — the pass
  replaced the slide scripts without the `A('A number line … appears', nl)` cues, so "Mark a and b on the line" pointed at
  nothing. The 7 number lines (0–2; −1–1 and −1–0 in Q5; −2–2; −1–0; 0–1; 0–1) are back in `rn_guided`, at the same
  places as before. Rendered and looked at.
- Everything else is correct; no other change.
