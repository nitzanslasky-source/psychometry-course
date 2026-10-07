# Topic 20: Algebraic Understanding. Changes

Patch: `math_patches/t20.py`. Running `python3 math_check.py 20` shows 0 problems, 0 warnings and 0 layout problems.

## Summary
- **Questions:** 20 rewritten, 12 added (4 guided with solution videos, 8 practice) and 1 removed.
  - Before: 21 questions (4 guided, 17 practice).
  - Now: 32 questions (8 guided, 24 practice).
- **Main lesson "Algebraic Understanding":** rebuilt. It had 7 slides and now has 9. The title slide is the same, and the other 8 slides are new or rewritten. It is about 5.5 minutes long.
- **New lesson video "Counting Integers & Pigeonhole":** 7 slides, about 2.7 minutes. It comes after the old Question 4.
- **New solution videos:** 4. The guided questions are renumbered in course order:
  - Q1 and Q2 are new (plug-in questions).
  - Q3 to Q6 are the old Q1 to Q4.
  - Q7 and Q8 are new (counting and pigeonhole).
- **Existing solution videos:**
  - Old Q1: 3 slides changed.
  - Old Q2: 2 slides edited.
  - Old Q3: rewritten (2 slides changed, 1 added).
  - Old Q4: 2 slides edited.
  - All sidebars now list Questions 1 to 8.
- **Memory cards:**
  - "Must, can, cannot" is rewritten as "Algebraic understanding".
  - New card: "Counting integers and pigeonhole".
- **Figures:** none in this topic.

## Wording: "could", as in Topic 1
- "Can be true" is now **"could be true"** everywhere: slides, card and stems. This matches Topic 1's lesson `r26-t01-must-could`.
- Slide 3 now says: "You met these three words in Topic 1. A quick reminder — then we go deeper." It also adds "not necessarily true", because the exam uses it.
- "Necessarily true" is kept in the old stems (q-579, q-587, extra 4). The card explains it as "Must be true / necessarily true".
- q-581 said "necessarily not correct". It now says "cannot be true".

## 1. Wrong statements (fixed)
- **Old Q3 video:** "Two sides of a triangle are always longer than the third" is gone. The video now proves choice 1 with algebra: (a+b)² = c² + 2ab > c². At the end it says: "the sum of any two sides of a triangle is longer than the third" (in geometry).
- **q-585:** the solution said "impossible, so certainly not necessarily correct". It now just says that (4) cannot be true.

## 2. Methods added
**Main lesson, rebuilt:**
1. **Three tools** (was "No fixed recipe"). The tools are: plug in numbers, test the answers, algebra. Students try them in that order. The line "There's no repeating principle I can hand you" is gone.
2. **Must, could, cannot:** a short reminder of Topic 1, plus "not necessarily true".
3. **Which numbers? (new).** This goes deeper than Topic 1's list:
   - read which numbers are allowed
   - try one number from each region (x > 1, 0 < x < 1, −1 < x < 0, x < −1)
   - try a = b when the letters may be equal
   - if two choices survive, try a second number
4. **Between 0 and 1 (new):**
   - for 0 < x < 1: x² < x < √x < 1 < 1/x (checked with x = ¼)
   - with negative numbers, farther from 0 means smaller
   - "which is the largest, for every x in a range": one number from the range decides
5. **Integer gaps** (was "Extreme cases"). The order is now: strictness first (< 12 means ≤ 11), then gaps and chaining. Two things are new:
   - the general chain: n increasing integers give last ≥ first + (n − 1)
   - "test the most extreme choices first"
6. **Scaling:** adds the general rule. When x² = a³, x changes by (factor)^(3/2), so 16^(3/2) = 64 (and 9^(3/2) = 27 in Q4).
7. **Connect topics:**
   - Pythagoras (Topic 31, taught later) is no longer needed. The slide teaches the algebra instead: c² = a² + b² with all numbers positive gives c > a and c > b. It adds "you'll meet this again in geometry, as Pythagoras."
   - The cycle of fractions is kept, with a new line: "the three can't all be bigger than one".
8. **Recap:** updated.

**New lesson "Counting Integers & Pigeonhole"** (after the old Q4):
- from a to b, both ends included: b − a + 1
- strictly between: b − a − 1; one end included: b − a
- every second number (only odd or only even): (last − first)/2 + 1
- letters in the choices: plug in small numbers and count
- pigeonhole principle, with 13 numbers and 12 remainders: two numbers with the same remainder have a difference that divides by 12
- "to be sure": worst luck first, then one more

**New guided questions:**

| No. | Id | Method | Answer |
|---|---|---|---|
| Q1 | q-r26-t20-01 | x > y > 0: which must be true? Plug in 3 and 2 (three choices survive), then ½ and ¼ | x² > y² |
| Q2 | q-r26-t20-02 | −1 < x < 0: which is the smallest? One number (−½), then order the negatives | 1/x |
| Q7 | q-r26-t20-03 | How many odd numbers are there between 20 and 80? Two methods | 30 |
| Q8 | q-r26-t20-04 | Socks: the smallest number to be sure of a pair (pigeonhole) | 4 |

The review asked for a medium guided must/could/cannot question before Q1. Q1 and Q2 fill that gap.

**Changes inside existing solution videos:**
- **Old Q1:**
  - Method 1 writes the key step on the board: b + c = (a + b) − (a − c) ≤ 11 − 2 = 9.
  - Method 3 now tests the extreme choices first (10, then −10). After that it checks the others.
- **Old Q2:** adds the general rule at the end: x = a^(3/2), so the factor is 9^(3/2) = 27.
- **Old Q3:** now starts with the algebra. It writes a/b = a²/(ab) and b/a = b²/(ab), then gets c² = a² + b². Choices 3 and 4 follow from c² > b². The counterexample is 3-4-5 against 6-8-10.
- **Old Q4:**
  - The stem now says "S, W and D are all greater than 1" (it used to say "(1 < S, W, D)").
  - "Last question of algebra" is removed, because the counting lesson comes after it. The words "you've finished algebra" moved to the end of Q8.

## 3. Text
- Every question in the topic is rewritten in TeX, with no ":" used for division.
- The stems of q-577, q-578, q-582, q-584 and extra 7 now show their given conditions one on top of the other.
- q-585 used "x:y, y:z, z:x". It now uses fraction bars, and says "Exactly one" / "Exactly two".
- q-586: "between x and y (not including x)" became "greater than x and smaller than y".
- q-583 and q-590 are reworded in plainer English.
- q-584, q-586 and q-588: the plug-in route now comes first, then the counting rule.
- Extras:
  - Solutions use numbers, not words ("five,six,seven,eight").
  - The missing spaces after commas are fixed.
  - Extra 2 (max of ab) now tests pairs first. The (a−b)² ≥ 0 argument comes second.
- Fewer "so" in the middle of sentences in the solutions I rewrote. They use "Therefore" instead.

## 4. Practice (24 questions, ordered easy → hard)
- **Removed:** extra 6 (a² = b²). It repeated the "squares" idea of extra 3. The size question q-r26-t20-05 replaces it.
- **Added:**
  - q-r26-t20-05: 0 < x < 1, which is the smallest? Answer: x².
  - q-r26-t20-06: x < y < 0, which must be true? Answer: x² > y².
  - q-r26-t20-07: how many integers satisfy 10 < x² < 100? Answer: 12. This is hard: the trap 6 forgets the negative numbers.
  - q-r26-t20-08: how many even numbers from 2n to 8n? Answer: 3n + 1. n = 1 leaves two choices, so the student must try a second number.
  - q-r26-t20-09: socks, to be sure of two blue socks. Answer: 16.
  - q-r26-t20-10: scaling with a new pair: x³ = y², y × 8, so x × 4.
  - q-r26-t20-11: a formula-structure question like Q4 (taxi price). Answer: n/d.
  - q-r26-t20-12: x² < x, which must be true? Answer: x³ < x². This is hard: first find 0 < x < 1.
- **Order:** the easy extras come first, then medium, then the exam-hard items at the end: q-585, -07, q-583, -09, -12, q-589, q-590.
- **Exam-level items:** about 14.
- I checked every key of the new and changed questions by brute force: exactly one correct choice each.

## For the teacher to decide
- **Topic 21** repeats "Possible vs must" and "Minimum & maximum". You may want a cross-reference, or to shorten those slides there. I did not edit Topic 21.
- **The two sock questions (G4 and q-r26-t20-09) use the same drawer on purpose.** The practice one asks the harder "two blue socks" version.
- **q-r26-t20-11 (taxi) has the same answer logic as old Q4.** The correct answer is in position 2 so that it does not repeat.

## Pass 2 (2026-09-27, teacher-approved remove/restore plan + summary lesson)
**Removed:** nothing (the plan keeps every Topic 20 addition, including "To be sure", q-r26-t20-04 and q-r26-t20-09).

**Restored:**
- alg-extra-unit-t20-2-6 ($a^2=b^2\Rightarrow|a|=|b|$), cleaned up with a numeric solution, in the easy part of the practice.
- Main lesson, true lines from the original slides, merged into the new slides without repeating:
  - "Three tools": the original "honest truth" lines (a fairly small part of the exam, the questions don't repeat themselves, no repeating principle, this lesson gives you tools that open your head). The new line "It's a small part of the exam..." was dropped so the idea is said once.
  - "Connect topics": "A cycle of ratios cancels to one" (replaces the new "cycle of fractions" wording) and "But the connection must come from the givens. Lengths must be positive; cancelling needs nonzero values. Check before you use it." (replaces the new, shorter check line).
  - The "Pythagoras in disguise" line stays replaced (it points to a later topic), as the plan says.

**Summary lesson (1 new video):** `r26-t20-summary` "Summary", at the end of "Algebraic understanding" (after the counting card), right before the independent practice. Slides: Summary · Three tools · Must, could, cannot · Which numbers? · Between 0 and 1 · Integer gaps · Scaling · Connect topics · Counting integers · Pigeonhole · Before you practice. Only content the Topic 20 lessons teach.

## 2026-10-05 cut repeats
Function `cut_repeats` (runs last). Nothing in topic 20 is recorded.
- **`algebraic-understanding`** → the Hebrew intro ("no repeating principles… we start with sample questions"): 5.8 → 1.3 min. Kept: title + "Three tools".
  - Cut "Must, could, cannot" (a Topic 1 reminder) → Q1, Q3, Q5 use the words; added in Q1 the habit "write the word" (pen note).
  - Cut "Which numbers?" → taught in Q1 `solve-q-r26-t20-01` (two regions; a second number); added "letters may be equal? try equal values" + board item.
  - Cut "Between 0 and 1" → taught in Q1 and Q2 `solve-q-r26-t20-02` (and in topic 17).
  - Cut "Integer gaps" → taught in Q3 `solve-q-577`; added the general rule "n increasing integers: last ≥ first + (n − 1)" + board item.
  - Cut "Scaling" (its example was Q4 with ×16 instead of ×9) → taught in Q4 `solve-q-578`; "The general rule from the lesson" → "The general rule".
  - Cut "Connect topics" → taught in Q5 `solve-q-579` (c² = a² + b²); added the cycle of ratios x/y · y/z · z/x = 1 + board item.
  - Cut "Recap"; its closing line moved to "Three tools".
- **`r26-t20-counting`**: 2.7 → 1.9 min. Kept: from a to b, strictly between, pigeonhole (the remainder version is not in Q8). Cut "Only odd or even" → Q7 `solve-q-r26-t20-03`; cut "To be sure" → Q8 `solve-q-r26-t20-04`; cut "Recap". "Letters in the choices? plug in small numbers and count" moved to the "Strictly between" slide.


## 2026-10-06 practice: new methods
Function `practice_methods` (runs last; append only). 1 practice question.
- q-r26-t20-10 (x³ = y², y × 8): Method 2 · Given power, asked power — r = 1/3 → x = y^(2/3) → × 8^(2/3) = 4.
All new lines verified numerically (python: fitting values, choice values, power by scaling). `math_check.py 20 32`: PROBLEMS 0, WARNINGS 0, LAYOUT 0.

## 2026-10-06 renumber pass
So the English course does not look like the Hebrew one: every Hebrew-derived question has new numbers, letters or story.
The idea, the trap, the level and the methods stay the same, and every guided solution video is rewritten to match
(speech, draw cues, video title, slide description). Nothing in Topic 20 is recorded, so nothing had to be kept as it was.
Function `renumber_pass(M)` in t20.py runs last (after `cut_repeats` and `practice_methods`).

**Counts:** 4 guided questions renumbered (q-577 … q-580) with their 4 solution videos rewritten; 10 practice questions
renumbered (q-581 … q-590). Lesson examples: the Hebrew lesson's own examples were already cut (cut_repeats); the card tips
that still quoted the Hebrew numbers changed ("less than 12 → at most 11" → 20 / 19; "9^(3/2) = 27" → "4^(3/2) = 8"), and the
counting card's two examples that equalled guided Q7 / Q8 changed (odd 21 to 79 → odd 15 to 41: 14 numbers; 3 colors: 4 socks →
4 colors: 5 socks). Practice: 25 → 15 (the audit's target).
The English-made items (guided q-r26-t20-01 … 04, the counting lesson, the summary, kept practice items) keep their numbers.

**Order:** q-580 (the formula question, no calculation) moves from the 4th to the 1st Hebrew guided place, so the guided
questions go easy → hard: Q1, Q2 plug-in → Q3 formula → Q4 integer gaps → Q5 scaling → Q6 p, q, r → counting lesson → Q7, Q8.
The lesson's last line now says "Two on plugging in first, then one on reading a formula — and three with more than one way in",
and "Next: a short lesson on counting whole numbers" moved from the end of the formula video to the end of Q6.

**Practice clean-up (25 → 15):**
- Copies removed: q-r26-t20-05 (0 < x < 1, which is smallest: the same as Topic 8's q-r26-t08-02), q-r26-t20-09 (the same drawer
  as guided Q8), alg-extra-unit-t20-2-6 (a² = b² → |a| = |b|).
- Extra warm-ups kept (3): X5 (4 < n < 9, which cannot be n²), X1 (largest of three numbers with sum 23), X4 (not necessarily true
  for two different positive integers). Removed X2 (max ab), X3 (x² + y² = 0), X7 (xy from sum and difference).
- September items kept (2, types the Hebrew practice does not have): -11 (taxi price formula), -12 (x² < x, must be true).
  Removed -06 (x < y < 0 must: the regions idea of -12 and guided Q1/Q2), -07 and -08 (counting: q-586, q-588, guided Q7),
  -10 (scaling: q-589, guided Q5).

**Checks:** every key brute-forced in Python (must / could / cannot over wide integer grids, e.g. a, b, c in −30..30; the
counting formulas over all m odd < n even in −21..30 and n = 1..29; the scaling and power factors numerically; the formula
question by monotonicity on a grid of C, S, M > 1): exactly one correct choice each, and the traps are still choices (14 just
above the maximum 13; 8 even and < 10 but impossible; 4^b·b^b; the "forgot the minus one" formulas; z < 8 true for 3-4-5 only).
Every step in the videos recomputed (15 − 2 = 13; 25³ = 5⁶, √ = 125; 9 + 16 = 25, 36 + 64 = 100). Duplicate check over a build
of topics 1–20 (stems, choices, lesson boards and lines, cards): no new question equals another question or a lesson/card example.
`python3 math_check.py 20 32` → PROBLEMS 0, WARNINGS 0, LAYOUT 0. Rendered the 4 solution videos and the lesson and looked at
them (titles Question 3–6, sidebars highlight the right question). No quadratic trinomial added.

| id | old (Hebrew) | new | answer |
|---|---|---|---|
| q-580 (G3, was G6) | plant growth: sunlight S, water W ↑, weeds D ↓; Sᵂ/D, SW − D, S − D + W, SWD | game score: coins C, stars S ↑, mistakes M ↓; C + S − M, CSM, Cˢ/M, CS − M | CSM (2) |
| q-577 (G4) | c < b < a integers, a + b < 12; b + c cannot be 1, −1, 10, −10 | a + b < 16; 2, −2, −14, 14 (max 13) | 14 (4) |
| q-578 (G5) | x² = a³, a × 9 → 36, 18, 27, 9 | y² = b³, b × 25 → 125, 50, 100, 25 | 125 (1) |
| q-579 (G6) | c²/(ab) = a/b + b/a; c < a + b, c < 6, b < c, a < c | r²/(pq) = p/q + q/p; q < r, r < p + q, r < 8, p < r | r < 8 (3) |
| q-581 | 0 < c < b < a; b = 1 and a = 3 impossible | b = 1 and a = 4 impossible; other choices c = 3, b = 5 … | (2) |
| q-582 | even a < b < c, c − a < 8, x = b − a: 1, 2, 6, 8 | c − a < 10: 3, 6, 8, 12 | 6 (2) |
| q-583 | Nadia, 13 numbers → 12 (12, 13, 14, 15) | Yoni, 9 numbers → 8 (8, 9, 10, 11) | 8 (1) |
| q-584 | a < b < c, sum 12, min c − a | x < y < z, sum 18 | 2 (2) |
| q-585 | x/y, y/z, z/x; "each > 1" was choice 4 | a/b, b/c, c/a; choices reordered | each > 1 (1) |
| q-586 | x odd < y even; (y − x − 1)/2 was choice 4 | m odd < n even; choices reordered | (n − m − 1)/2 (1) |
| q-587 | different integers, sum 25; c ≠ 5 | sum 32; c ≠ 7; choices reordered | b not the average (3) |
| q-588 | a < x < 3a → 2a − 1 | n < k < 4n → 3n − 1 | 3n − 1 (2) |
| q-589 | y = aᵃ, a × 3 → 3³ᵃ·a²ᵃ | y = bᵇ, b × 4 → 4⁴ᵇ·b³ᵇ | (1) |
| q-590 | 13 numbers, begin 5 end 2 | 12 numbers, begin 7 end 4; choices reordered | at most 3 digits (3) |
| card mem-understanding | integer < 12 → ≤ 11; 9^(3/2) = 27 | < 20 → ≤ 19; 4^(3/2) = 8 | – |
| card counting | odd 21 to 79: 30; 3 colors: 4 socks | odd 15 to 41: 14; 4 colors: 5 socks | – |

## 2026-10-06 review (of the renumber pass)
Checked all 14 renumbered items, the reorder, the card changes and the 4 videos. q-584 (sum 18), q-587 (sum 32, c ≠ 7),
q-590 (12 numbers, 7…4; still 12 > 11) are the same kind as the Hebrew. No changes.

## 2026-10-06 Hebrew back-check
Every guided / practice question, the lessons, the summary and the cards were compared with the teacher's Hebrew VIDEO
subtitles (01-Algebra-Original-Subtitles.txt, lines 19912–20234). Nothing in topic 20 is recorded. Function
`hebrew_backcheck(M)` in t20.py runs last.

| where | Hebrew video | before | new |
|---|---|---|---|
| Summary video, slide 7 (Scaling) | x² = a³, a × 4 → x × 8 | x² = a³, a × 4 → x × 4^(3/2) = x × 8 (exact Hebrew numbers) | a × 9 → x × 9^(3/2) = x × 27 ("Nine cubed is three to the sixth. Its root: three cubed — twenty-seven.") |
| Card "Algebraic understanding", scaling tip | same | 4^(3/2) = 8 | 9^(3/2) = 27 |

Left on purpose: q-580 (Hebrew Q/W/L student-success question) — story, letters and choice order were already changed;
the four expression forms are the question's logic. q-577 (a + b < 16, choices ±2, ±14 vs Hebrew < 10, ±1, ±8), q-578
(×25 → ×125 vs ×4 → ×8), q-579 (r < 8, "not necessarily true" vs Hebrew c < 5) — numbers already differ. The 3-4-5 / 6-8-10
triples in solve-q-579 are standard examples. Practice and the English-made questions: no match.
Checks: `python3 math_check.py 20 32` → 0 / 0 / 0; rendered r26-t20-summary and looked.


## 2026-10-07 methods spread
Every question checked against the 2026-10-06 methods; nothing added (no code). Already shown in the explanations: signs hidden in the given (q-r26-t20-12 starts with x² < x → 0 < x < 1), given power → asked power (q-578 "y = b^(3/2)", q-r26-t20-10 from the 2026-10-06 practice pass), at most / at least (q-577, alg-extra-unit-t20-2-1, q-584 already push the others to the extreme). Mirror test does not fit (q-579: the swap p ↔ q turns choices 1 and 4 into each other, twins, not opposites). Nothing in topic 20 is recorded.
