# Topic 13 — Absolute Value: changes

Patch: `math_patches/t13.py`. Check: `python3 math_check.py 13` shows 0 problems, 0 warnings and 0 layout problems.

## Summary
- Questions: all 35 existing questions rewritten (28 course questions and 7 extras), 12 added (4 guided with solution videos and 8 practice), none removed.
  The topic had 13 guided and 22 practice questions. It now has 17 guided and 30 practice.
- Main lesson "Absolute Value": 7 slides changed, 2 slides added ("Signs of a product", "Negative right side"). New sidebar.
- New lesson video "Absolute Value — Exam Tools" (7 slides, about 3.5 minutes), at the start of the advanced section.
- New solution videos: 4 (the new guided questions). The guided questions are renumbered automatically: the new ones are Q6, Q7, Q12 and Q16, so the old Q6–Q13 are now Q8, Q9, Q10, Q11, Q13, Q14, Q15 and Q17.
- Existing solution videos: 10 changed (details below). All sidebars list the new question numbers.
- Memory card "Absolute value — rules to know" rewritten. New card "Question wordings" before the advanced questions.
- 1 new figure (number line "within 4 of 2") on the tools lesson.

## 1. Wrong or misleading teaching (fixed)
- **Sign clue |x| = −x.** The lesson slide and the card only said "|x| = −x (x < 0)". As a clue the answer is **x ≤ 0** (zero works too), and extra-6 keys x ≤ 0. Slide 7 now has 4 clues. The new clue is |x| = −x → x ≤ 0, and the teacher points at the zero trap. The Q1 video (slide 3) and the card show the same 4 clues.
- **"The minus just drops off"** (lesson slide 3) now applies only to plain numbers. There is a new warning for letters: "if x = −3, then −x = 3 and |x| = 3 ≠ x".
- **Q12 video (old numbering; now Q15):** "Six to seven is the bait — what you get if you forget to subtract the one" was false. The line now says "if you ADD the one instead of subtracting it".
- **Q9 video (now Q11):** the broken board line "|a+b|² > 4 = (a+b)² > 4" is now two correct lines: "|a+b| > 2 → |a+b|² > 4" and "|a+b|² = (a+b)² → (a+b)² > 4".
- **extra-t13-3-1:** the template solution ("negative b … is b") is replaced by "3 − 8 = −5, and |−5| = 5".
- **Lesson slide 9 (inequalities):** the explanation no longer uses a different example ("x bigger than five", whole numbers only). It now explains the board example |x − 2| > 4 and |x − 2| < 4, and uses 4.5 and 3.5 as examples.

## 2. Methods added
Main lesson:
- Slide 5: rule two now also covers fractions: |a/b| = |a|/|b|.
- New slide "Signs of a product": a·b > 0 → same signs, a·b < 0 → opposite signs, x/|x| = 1 or −1. The course uses the sign rules in Q1 before topic 16 teaches them. This slide teaches them here.
- New slide "Negative right side": |x+1| < −3 has no solution, |x+1| > −3 is true for every x, and |x+1| ≤ 0 gives only x = −1.
- Slide "Plug in": avoid 0, 1, −1 and numbers from the choices. If two choices survive, plug in again.
- Recap updated. It ends with "Seven questions next".

New lesson "Absolute Value — Exam Tools":
1. Squares and bars: |x|² = x², √(x²) = |x|, |a − b| = |b − a|.
2. Square both sides (allowed because both sides are ≥ 0). Example: |x − 1| = |x + 3| gives x = −1.
3. Letter on the right: |x − 6| = 2x. The right side must be ≥ 0. Check each answer: −6 is fake, so x = 2 only.
4. Distance: |x − a| is the distance between x and a, shown on a number-line figure (|x − 2| < 4 → −2 < x < 6). It also covers a plus inside: |x + 5| is the distance from −5.
5. From a range to bars (the midpoint trick): −3 < x < 7 → |x − 2| < 5 (the center, and half the length).
6. Recap.

New card **"Question wordings"**: necessarily / could / cannot / not necessarily / possible but not necessarily. Each row gives the meaning and how to find the answer. It refers back to the topic-1 lesson "Must, Could, Cannot".

Existing videos now use the new tools:
- Q3 and Q4: a short "distance picture" solution added.
- Q5: the second plug-in is −2 instead of −1, and the teacher links it to x/|x| = −1.
- Q10 (now Q13): "letter on the right side, so check" line.
- Q11 (now Q14): squaring both sides is named as the lesson tool.
- Q9 (now Q11): points to the wordings card.

**New guided questions** (each with a solution video):

| New # | id | Question | Answer | Method |
|---|---|---|---|---|
| Q6 | q-r26-t13-01 | \|2x − 1\| = 7, all values | 4 or −3 | medium bridge before the advanced part; two cases + check |
| Q7 | q-r26-t13-02 | which has no solution? | \|x+2\| < −1 | negative right side |
| Q12 | q-r26-t13-03 | \|x + 4\| = 3x, all values | 2 only | letter on the right: 2 methods (check / right side ≥ 0) |
| Q16 | q-r26-t13-04 | which inequality is exactly −3 < x < 7? | \|x − 2\| < 5 | midpoint trick; 2 methods (center / check the ends) |

**New practice questions:**
- q-r26-t13-05: true for every x (negative right side)
- q-r26-t13-06: range −8 < x < 2 → bars (midpoint)
- q-r26-t13-07: |x|/x + 2y/|y| (x/|x|)
- q-r26-t13-08: |2 − x| + |x| for x > 2 (plug-in expression)
- q-r26-t13-09: |x − 2| = 2x + 1 (letter on the right, fake answer)
- q-r26-t13-10: number of integers with |x − 1| + |x − 7| = 6 (distance, exam-hard)
- q-r26-t13-11: |3x − 6| ≤ 0 (zero right side)
- q-r26-t13-12: |x| = −x and |y| = y (the x ≤ 0 clue)

## 3. Text
- Every stem, choice and solution is now in TeX. No colons for division: the old "2x:|x|", "a:3", "1:2", "x:y", "−1:2" and "P:Q" are now fractions.
- Conditions are stacked with `cases` in q-358, q-363, q-365, q-367, q-371, q-373, q-375, q-377, q-378, q-380, q-381, q-382 and q-r26-t13-12.
- The wording is NITE style: "Which of the following is necessarily true?", "How many different values can x have?". In q-376 and q-384 the words "odd", "positive" and "negative" are no longer set as TeX text.
- q-382 choice 4 was "Correct for every a and b", which makes no sense as a choice. It is now "a > 0 and b > 0". The key is unchanged (choice 2).
- Every solution now shows its numbers, with a check or counterexamples where useful. The 7 extras now have worked steps instead of one terse line.
- Videos: British spellings changed to American (kilometers, memorize, Analyze). A mid-sentence "— so" / ", so" is now "… . So …". The Q5 video no longer says "Last question." (it now says "Question five.").

## 4. Figures
- There were no question figures in this topic. One slide figure was added: a number line showing |x − 2| < 4 as "4 steps each side of 2" (tools lesson, "Distance" slide). Its style matches the course (colors and font).

## 5. Practice
- Reordered easy → hard. The easy extras now come first as a warm-up, and the exam-hard items come last (q-376, q-384, q-382, q-381, q-385).
- No near-duplicates were removed. The review found the set not repetitive.
- There are now about 12 exam-level items: q-372, q-377, q-380, q-381, q-382, q-384, q-385, q-376, and new 06, 09, 10, 12.

## Not done / for the teacher to decide
- **Topic order:** the sign rules (topic 16) and the must/could/cannot wordings (topic 20) are now taught briefly here, so nothing is used before it is taught. If topic 16 or topic 20 moves earlier, the "Signs of a product" slide and the wordings card can stay as short reminders.
- Solution-video titles for questions with stacked conditions show the raw text of the stem ("\begin{cases}…") in the navigation label. This is the same as in other topics. It happens because the API builds the label from the plain stem.
- The lesson video is now about 8.7 minutes long (it was 6.3). The strong-student tools went into a separate 3.6-minute video to keep the main lesson for weak students.

## Pass 2 (teacher-approved remove/restore plan, 2026-09-27)

**Removed** (not on the real exam and not in the original course: writing a range as |x − m| < r):
- Video "Absolute Value — Exam Tools": slide "From a range to bars", its sidebar label and its Recap line.
- Guided question q-r26-t13-04 ("which inequality is exactly −3 < x < 7") and its solution video. The advanced guided questions are renumbered (now Questions 8–16), sidebars updated.
- Practice q-r26-t13-06 (−8 < x < 2 → bars), also taken out of the practice order.
- Memory card "Absolute value", table "Distance tools": the row "a < x < b → |x − (a+b)/2| < (b−a)/2".

**Kept** (as the plan says): the "no solution / every x / one solution" items (q-r26-t13-02, -05, -11) and the sum of distances (q-r26-t13-10).

**Restored:** nothing - no original question was deleted in this topic.

**New: summary video** `r26-t13-summary` "Absolute Value — Summary", at the end of the advanced section, right before the independent practice (about 2.6 minutes).
Slides: Summary · Distance from zero · The rules · Sign clues · Equations · Inequalities · Negative right side · Distance · Plug in · Before you practice.
It only repeats what the lessons teach. The last slide lists the checks (is the letter positive, negative or zero? both cases? right side negative or zero? letter on the right: checked? which question word?) and the traps (forgetting zero, losing the second case, keeping a fake answer).

## 2026-10-01 elite comparison

Teacher-approved addition: the sum rule |a + b| ≤ |a| + |b| is now taught as a **sign-reading tool** (same signs → the sizes add; opposite signs → they cancel). Targets the real exams 2021 autumn II-15, 2024 spring II-18, 2025 spring I-19, 2020 autumn II-13 (2019 winter II-17 is already covered by |a − b| = |b − a|).

- Main lesson, slide "The rules": the line "if you don't memorize this one, that's fine" now says the rule becomes a sign-reading tool in the advanced part.
- Video "Absolute Value — Exam Tools" ("Five tools" now), two new slides before the recap:
  - **Add or cancel**: |−3 + (−5)| = 8 = 3 + 5, |−3 + 5| = 2 = 5 − 3; example |x| = 9, |y| = 2 → |x + y| is 11 or 7.
  - **Read the signs**: |x + y| < |x − y| → x · y < 0; |x + y| = |x| − |y| → opposite signs and |x| ≥ |y|; |a + b| < |a| → b has the opposite sign of a.
  - Recap: new line "Same signs → sizes add · opposite signs → cancel". Sidebar updated.
- Memory card: the |a + b| ≤ |a| + |b| row explains add / cancel; three new sign-clue rows.
- New guided question **q-r26-t13-13** (advanced section, right after q-366) with solution video (Method 1 read the signs, Method 2 try the four sign cases). |a| = 7, |b| = 3, |a + b| < |a − b| → |a + b| = ? Answer: choice 2 (4).
- New practice question **q-r26-t13-14** (after q-384): a, b ≠ 0, |a − b| = |a| + |b| → necessarily a · b < 0. Answer: choice 1.
- Summary video, slide "The rules": the sum line now says "same signs add, opposite signs cancel" and "read it backwards".
- Both questions solved by computer (all sign cases / a grid of values): exactly one correct choice each.


## 2026-10-04 question = lesson example fixed
- Lesson "absolute-value" slide 9: example |x + 3| = 8 (same as guided q-359) -> |x + 4| = 6, x = 2 or −10. Question and its video unchanged.

## 2026-10-05 cut repeats
Function `cut_repeats` (runs last). Nothing in topic 13 is recorded.
- **Absolute Value** (8.7 → 3.4 min, Hebrew 6.2 incl. its first sample question). Kept the Hebrew lesson's part: distance from zero, plus or minus inside, whole expression, the rules, when |a + b| = |a| + |b|; ends "Seven questions next … each question teaches one more tool". Cut: sign clues → Q1 (slide 3 shows all four); signs of a product → Q1; x/|x| → Q5; equations (two cases) → Q2 and Q6; inequalities small/big side → Q3 and Q4; negative right side → Q7; plug in (avoid 0, ±1, plug again if two survive) → Q5; recap.
  - Rewording: Q2 "You know the move" → "The move: two cases."; Q5 "You know what that means — plug in." → "That means we may plug in a number."; Q5 "That's the tool from the lesson: …" → "A useful fact: x over its absolute value is one for every positive x — and minus one for every negative x."
  - Moved into Q7: "Bars = a negative number → no solution" + one line (the equation version).
- **Absolute Value — Exam Tools** (4.5 → 1.7 min). Kept "Squares and bars" and "Distance" (used in practice, |x − 1| + |x − 7|; no question video here). Cut: square both sides → Q15 method 2; letter on the right → Q13; add or cancel and |x + y| < |x − y| → Q12; recap.
  - Q15: "The tool from the lesson" → "A tool for bars on both sides …" + board item "Bars on both sides → square both sides".
  - Q13: "Remember the tool" → "The tool: solve — then check every answer."; one line at the end "a letter on the right side? Check every answer in the original equation."
  - Q12: new short slide "Other wordings": |x + y| = |x| − |y| → opposite signs, |x| ≥ |y|; |a + b| < |a| → b has the opposite sign of a, and |b| < 2|a| (both were only on the cut slide; used in practice q-r26-t13-14, q-382, q-384).

## 2026-10-06 new exam methods
Function `add_methods` (runs last, after `cut_repeats`). Nothing in topic 13 is recorded.
- **New lesson video `r26-t13-mirror` "The Mirror Test"** (3.7 min, 5 slides: title, The idea, Flip all signs, Swap the letters, Limits). Placed in the advanced section right after Question 12 (sign reading + "Other wordings"). Teaches: flip all signs / swap the letters; if the given is unchanged, the mirror of any legal example is legal, so a choice that turns into its OPPOSITE in the mirror cannot be necessarily true. Examples (original): |a + b| < |a| + |b|, necessarily negative: a, b − a, a·b, a + b → a·b (flip kills the other three); x² + y² = 13, necessarily true: x > 0, x < y, x + y > 0, x² ≤ 13 → x² ≤ 13 (flip kills 1 and 3, swap kills 2; "twins stay, only opposites go out"). Limits: the given must not change; simplify a choice first (x − y + 2y = x + y; "which is NOT equal" questions); formulas for a mirror-unchanged quantity must not change; if every choice survives, plug in.
  - Note: the rule is stated as "turns into its opposite", not "changes" — a choice can change into a twin (x² ≤ 13 → y² ≤ 13) and still be true.
- **New guided question q-r26-t13-15** (now Question 13): a² + b² = 2ab + 9, necessarily true? a − b = 3 · a > b · |a − b| = 3 · a + b = 3 → choice 3. Solution video `solve-q-r26-t13-15` (2.1 min): Method 1 mirror test (swap kills 1, 2; flip kills 4), Method 2 algebra (a − b)² = 9, trap a = 0, b = 3. Checked by computer over a grid of values: only choice 3 always holds. Later guided questions shift by one (renumbered automatically); the "Question N" sidebars of the advanced group now include it.
- Question 16 (q-368, |x + 3y| = |3x + y|): one line at the end of its plug-in method — the swap mirror kills choices 3 and 4 with no numbers.
- Card "Absolute value — rules to know", Sign clues: new row "the given does not change when you flip all signs or swap the letters → a choice that turns into its opposite is not necessarily true".


## 2026-10-06 practice: new methods
Function `practice_methods` (runs last; append only). 3 practice questions.
- Method 2 · Mirror test: q-r26-t13-14 (|a − b| = |a| + |b|: swap kills 1, 2; flip kills 4 → ab < 0, no numbers), q-381 (PQ < 0, P/Q < Q/P: flip kills 2, 3, 4 → |Q| < |P|). Both checked by computer over a grid of values.
- Method 2 · The most precise range: q-375 (a = −5 kills 2, 3; a = −20 kills 4).
- Not used: q-374/q-371 (only a one-letter flip leaves the given unchanged — not one of the two taught mirrors), q-382 (given not a mirror), q-379 (every choice survives).
All new lines verified numerically (python: fitting values, choice values, power by scaling). `math_check.py 13 32`: PROBLEMS 0, WARNINGS 0, LAYOUT 0.

## 2026-10-06 renumber pass
This pass makes sure the English course does not look like the Hebrew one. Every Hebrew-derived question now has new numbers or letters. The idea, the trap, the difficulty, the kind of condition and the methods all stay the same. Every guided solution video is rewritten to match: board, speech, draw cues, video title and canvas notes. Nothing in Topic 13 is recorded, so no question had to stay as it was.
The function `renumber(M)` in t13.py runs last.

**Counts:** 13 guided questions renumbered (q-358 … q-370), with their 13 videos rewritten. 15 practice questions renumbered (q-371 … q-385). 4 slides of the "Absolute Value" lesson got new examples. The "Exam Tools" distance example has new numbers and a new number-line figure, and 3 card rows have new numbers. Practice: 30 → 20.

**Practice clean-up (30 → 20):** all 15 Hebrew questions are kept, with new numbers.
- Extra warm-ups: 3 of 7 kept: |3 − 8|, |x| < 3, and |x| = −x (the zero trap). Removed: the sum of the solutions of |x − 3| = 5 (Questions 2 and 6 cover it), x < 0: |x| − x (Question 5), the minimum of |x − 3| + |x − 5| (q-r26-t13-10 keeps the distance-sum type), and the integers in |x − 3| ≤ 2 (q-383).
- September items: 2 of 8 kept, because the Hebrew practice does not cover their types: -10 (sum of distances) and -11 (bars ≤ 0). Removed: -05 (Question 7 covers it), -07 x/|x| (Question 5), -08 |2 − x| + |x| (the q-373 type), -09 letter on the right (q-380), -12 (q-378), and -14 (q-384; the mirror-test practice stays in q-381).
- Order: warm-ups first, then easy → hard.

**Lesson and card (Hebrew lesson examples):** 5 and −7 → 4 and −6 (2 km instead of 3 km); |6|, |−9| → |8|, |−4|; |5 − 11| = 6 (the trap was 16) → |4 − 13| = 9 (the trap is 17); |−2 + (−5)| and |−2 + 5| → |−3 + (−6)| and |−3 + 6|. In Exam Tools, |x − 2| < 4 → |x − 3| < 4 (−1 < x < 7, with a new figure), and the "plus inside" example |x + 5| → |x + 6|. Card rows: |x + 3| = 8 → |x − 4| = 5, and |x − 2| ≶ 4 → |x − 3| ≶ 4.

**Checks:** every key was brute-forced in Python with random and grid samples. Each question has exactly one correct choice, every original trap is still a choice, and every number in the videos was recomputed. A duplicate scan over all questions, videos and cards in Topics 1–13 found no question equal to another question or to a lesson or card example. One near-match came up: q-362 first became "8 + 3x/|x|", which looked close to Topic 5's q-128 (x/|x| + 8). It is now 10 + 4x/|x|. No quadratic trinomial was introduced. `math_check.py 13 32` gives PROBLEMS 0, WARNINGS 0 and LAYOUT 0. All 15 changed videos were rendered and checked by eye.

| id | old (Hebrew) | new | answer |
|---|---|---|---|
| q-358 (G1) | ab < 0, a < \|a\| | xy < 0, y < \|y\| | \|x\| = x (4) |
| q-359 (G2) | \|x+3\| = 8, could be | \|x+7\| = 9 | −16 (3); trap −2 |
| q-360 (G3) | \|x+5\| < 8 | \|x+3\| < 7 | 3 (3); trap 5 |
| q-361 (G4) | 6 < \|x+3\|, cannot | 5 < \|x+2\| | 1 (2); trap 5 |
| q-362 (G5) | x<0: 5 + 2x/\|x\| | x<0: 10 + 4x/\|x\| | 6 (2); the first plug-in x = −6 ties with −x |
| q-363 (G8) | \|b\| = a, b ≠ a, 3c = a | \|n\| = m, n ≠ m, 4k = m | n < k < m (2) |
| q-364 (G9) | p<q<0<r<s | a<b<0<c<d | \|b\| < \|a\| (2) |
| q-365 (G10) | d<c<b, \|b\|<\|c\| | z<y<x, \|x\|<\|y\| | x ≠ \|x\| not nec. (3) |
| q-366 (G11) | 2 < \|a+b\|, factor 3 | 3 < \|x+y\|, factor 5 | \|x+y\| < \|x\|+\|y\| (2) |
| q-367 (G15) | 3\|x\|+6\|y\|=27, x+2\|y\|=3 | 4\|x\|+12\|y\|=44, x+3\|y\|=1 | −5 (2) |
| q-368 (G16) | \|x+3y\| = \|3x+y\| | \|x+4y\| = \|4x+y\| | \|x\| = \|y\| (3) |
| q-369 (G17) | 11 < \|2x+1\| < 13 | 7 < \|2x−1\| < 9 | −4<x<−3 (3); traps 3<x<4, −5<x<−4 |
| q-370 (G18) | x+\|x\| < 14 | x+\|x\| < 12 | x < 6 (3) |
| q-371 | d≠0, \|c+d\|=\|c−d\| | q≠0, \|p+q\|=\|p−q\| | p = 0 (2) |
| q-372 | \|x+2\| < \|x−2\| | \|x+4\| < \|x−4\| | −5 (3) |
| q-373 | m<0, n>0: \|mn\| | a>0, b<0: \|ab\| | a·\|b\| (3) |
| q-374 | \|a+b\| = \|a−b\| | \|m+n\| = \|m−n\| | mn = 0 (2) |
| q-375 | \|a\|+5=b, b>9 | \|x\|+3=y, y>10 | x < −7 (2); Method 2 line rewritten |
| q-376 | b^m ≠ \|b\|^m | a^n ≠ \|a\|^n | a<0 and n odd (4) |
| q-377 | x<−2, \|x\|=\|y\| | x<−3, \|x\|=\|y\| | 9 < y² (3) |
| q-378 | \|x\|≠x, \|−5x\|≠−5x | \|x\|≠x, \|−3x\|≠−3x | no number (4) |
| q-379 | (a−b)² < 4 | (x−y)² < 9 | \|x−y\| < 3 (3) |
| q-380 | \|4x+2\|=10, \|2x+1\|=−2x−1 | \|6x+9\|=21, \|2x+3\|=−2x−3 | −5 (2) |
| q-381 | PQ<0, P/Q<Q/P | st<0, s/t<t/s | \|t\| < \|s\| (3); mirror Method 2 rewritten |
| q-382 | a≠b, a−b=\|a+b\| | x≠y, x−y=\|x+y\| | x=0 or y=0 (4) |
| q-383 | \|x+6\| < 4, integers | \|x+8\| < 5 | 9 (3); trap 10 |
| q-384 | \|c\|+\|d\|=\|c+d\| | \|m\|+\|n\|=\|m+n\| | "integers" (2) |
| q-385 | p<q<\|pqr\|<r | a<b<\|abc\|<c | \|ab\| < 1 (3) |

The English-made guided questions (q-r26-t13-01, -02, -03, -13, -15) and the kept warm-up and September items keep their numbers.

## 2026-10-06 review
Independent check of the renumber pass (13 guided + 15 practice, 13 videos, lesson "Absolute Value", "Exam Tools", card). Every key recomputed (exactly one correct choice, Hebrew trap still a choice), every video step redone with the new numbers (no old numbers left in board/speech/draw), explanations and Method 2 lines match, practice removals valid (only English extras/September items; 3 warm-ups kept). Nothing recorded, no trinomial added. Duplicate scan topics 1–16: no clash. Rendered solve-q-367, -369, r26-t13-tools. No changes needed.
- Note for the teacher: the kept warm-up alg-extra-unit-t13-3-6 (|x| = −x → x ≤ 0) is the same as a "Sign clues" row on the memory card (it was like that before this pass).
- `python3 math_check.py 13 32` and the full `python3 math_check.py` → 0 / 0 / 0.

## 2026-10-06 Hebrew back-check
Every guided and practice question, lesson slide and card of topic 13 was compared with the teacher's Hebrew video
subtitles (01-Algebra-Original-Subtitles.txt, lines 11081–13680: lesson + 8 sample questions). Nothing in topic 13 is
recorded. Fixes are in `hebrew_backcheck(M)` in t13.py (runs last). Keys brute-forced; `python3 math_check.py 13 32` → 0/0/0;
changed videos rendered and checked.

| id | matched the Hebrew video | new | answer |
|---|---|---|---|
| q-361 (+ video) | $5<\|x+2\|$, ranges $x>3$ / $x<-7$, choices 7, −8, 5 — the Hebrew question exactly | $8<\|x+1\|$ → $x>7$ or $x<-9$; choices 9, 2, −10, 11 | 2 (choice 2) |
| q-364 (+ video) | $a<b<0<c<d$ (Hebrew letters and choices); video examples −2/2, −20/20 (Hebrew's) | $p<q<0<r<s$; examples −5/5, −40/40 | $\|q\|<\|p\|$ (choice 2) |
| solve-q-370 | plug-ins 1, 10, −10 and "−1 + 1 = 0" (Hebrew video's) | plug-ins 2, 9, −8 and "−9 + 9" | unchanged (choice 3) |
| lesson absolute-value #2, #3 | "friend's house" distance story; $\|8\|=8$ | "walk to the bus stop"; $\|11\|=11$ | — |

Left on purpose (only one number shared, different equation): q-359 $\|x+7\|=9$ (Hebrew $\|x+4\|=9$), q-360 $\|x+3\|<7$
(Hebrew $\|x+4\|<7$), q-367 ($4\|x\|+12\|y\|=44$, $x+3\|y\|=1$; Hebrew $4\|x\|+8\|y\|=20$, $x+2\|y\|=1$). Letters-only
questions q-358, q-363, q-365, q-366, q-368 already differ (letters / numbers / examples). Practice: no matches.

## 2026-10-06 pen or click
(Done 2026-10-07.) Function `pen_or_click` runs LAST, after renumbering, review, add_methods and `hebrew_backcheck`, so it works on the final text. The teacher's approved split: in lessons the content appears by click and the pen only marks (arc, circle, box, star, cross out); in solution videos the setup and the mechanical lines appear by click, and only the one or two key steps (plus the marks on the choices) are written by hand. Very short notes next to a choice ("never", "x = 3", "5 = 5 ✓") count as marks. Number-line sketches stay by hand. Where a hand-written line comes before click lines, the board leaves an empty row for it. Spoken lines, math, questions and slide count are unchanged. No topic 13 video is recorded. Topic total: 165 pen cues -> 96 by hand, 66 by click, 3 split (99 pen cues left).
- absolute-value (8 -> 5 by hand, 2 clicks, 1 split). Clicks: = |−9| = 9; "Same signs: 9 = 9" and "Different signs: 3 < 9" (were written under each side). Split: 4 + 13 = 17 click + cross it out by hand. By hand: the two arcs on the number line, circle/cross out the minus, the box. Empty handwriting rows closed.
- solve-q-358 Q1 (8 -> 6 hand, 1 click, 1 split). By hand: y < |y| -> y < 0, the marks on the choices. Clicks: "x · y < 0 -> opposite signs" (+ underline by hand), "y < 0 and opposite signs -> x > 0".
- solve-q-359 Q2 (4 -> 2 hand, 2 click). By hand: the second case x + 7 = −9 -> x = −16, circle. Clicks: first case, the check.
- solve-q-360 Q3 (5 -> 3 hand, 2 click). By hand: −7 < x + 3 < 7, cross-outs/circle, the number-line sketch. Clicks: −10 < x < 4, the check.
- solve-q-361 Q4 (5 -> 4 hand, 1 click). Click: the first case x > 7. By hand: the second case x < −9, ticks, circle, number line.
- solve-q-362 Q5 (8 -> 4 hand, 3 click, 1 split). By hand: x = −6 (method 1), x < 0 -> |x| = −x (method 2), the values next to the choices, "−x = 2 ✗" + circle. Clicks: the long substitution, the x = −2 line, 4x/(−x) = −4. Split: 10 − 4 = 6 click + circle.
- solve-q-r26-t13-01 Q6 (4 -> 2 hand, 2 click). By hand: the second case 2x − 1 = −7, circle. Clicks: the first case, the double check.
- solve-q-r26-t13-02 Q7: unchanged (only the short notes on the choices and the marks).
- r26-t13-tools (5 -> 0 hand, 5 clicks). Every written line is a click; empty rows closed.
- solve-q-363 Q8 (9 -> 7 hand, 2 click). By hand: |n| = m -> m ≥ 0, the number-line sketch and k on it, the bad try m = 4, n = 4 and its fix (method 2), circles. Clicks: m > 0, n < 0; 4k = 4 -> k = 1.
- solve-q-364 Q9: unchanged (number-line sketch, the counterexample on choice 3, marks).
- solve-q-365 Q10 (7 -> 5 hand, 2 click). By hand: y < x but |y| > |x| -> y < 0, marks. Clicks: z < 0, the x = ±2 example.
- solve-q-366 Q11 (10 -> 7 hand, 3 click). By hand: the short notes on choices 3 and 4, x = 6, y = −2: 4 < 8 (the key example), marks. Clicks: the two choice-1 lines, x = 4, y = 1: 5 = 5. The rule item was at a fixed spot; it now follows the click lines.
- solve-q-r26-t13-13 Q12 (8 -> 3 hand, 5 click). By hand: underline the third given + "the sum cancels -> opposite signs" (method 1), circle the two 4s (method 2), circle. Clicks: "same signs: 10, opposite signs: 4", |a + b| = 7 − 3 = 4, the four sign cases.
- r26-t13-mirror (7 -> 0 hand, 7 clicks).
- solve-q-r26-t13-15 Q13 (10 -> 7 hand, 3 click). By hand: the swap line (method 1), (a − b)² = 9 (method 2), the short notes on the choices, circle. Clicks: the flip line, a − b = ±3 -> |a − b| = 3, the a = 0, b = 3 check.
- solve-q-r26-t13-03 Q14 (8 -> 5 hand, 3 click). By hand: the check that kills x = −1, 3x ≥ 0 (method 2), marks. Clicks: the two cases, the x = 2 check.
- solve-q-367 Q15 (15 -> 7 hand, 8 click). By hand: |x| − x = 10 (subtract the equations), the notes "2 = 8? ✗" / "5 = 5 ✓", 4·5 + 12·2 = 44 ✓, circles. Clicks: ÷4 line, |x| = 10 + x (twice), the two options, the choice-1 lines and choice-2 line of method 3. Slide 2 in size 32.
- solve-q-368 Q16 (13 -> 9 hand, 4 click). By hand: the opposite case x = −y, (x + 4y)² = (4x + y)², x = 2, y = −2, cross out 8xy, marks. Clicks: the equal case, the expansion, y² = x², x = y = 2.
- solve-q-369 Q17 (9 -> 3 hand, 6 click). By hand: the two bands on the number line, circles. Clicks: the three band lines, the three tries on the choices (1)-(3).
- solve-q-370 Q18 (9 -> 6 hand, 3 click). By hand: x < 0: 0 < 12 always, x = −8 check, marks. Clicks: x ≥ 0 case, x = −4 line, the choice-4 try.
- r26-t13-summary (2 -> 1 hand, 1 click): x = 8 or x = −12. The circle stays.
`math_check.py 13 32`: PROBLEMS 0, WARNINGS 0, LAYOUT 0. All changed videos rendered and looked at.

## 2026-10-07 methods spread
Function `spread_methods` (runs last, after `pen_or_click`). Every guided and practice question checked; each line verified in Python (grid brute force). Nothing in topic 13 is recorded. Written lines only — no extra slides: the two videos where a method fits already show it (solve-q-368 ends with the swap mirror; solve-q-370 Method 2 already tests numbers).
- **Method 2 · Mirror test**: q-368 (swap x, y: given unchanged; y < x and x < y turn into each other → 1, 4 out; x = 2, y = −2 kills 2). The video had it; the written solution did not.
- **Method 2 · The most precise range**: q-370 (x = −8 ✓ kills 1, 4; x = 2 ✓ kills 2).
- **Method 2 · Pick values that fit**: q-371 (q = 4 → p = 0; only choice 2 gives 0), q-374 (n = 1 → m = 0 → mn = 0; n = 2 gives 0 again, so not "cannot be determined").
- Skipped: q-366 and q-379 (every choice survives the mirror), q-382 / q-377 (given is not a two-letter mirror), questions with number choices (plug in already) and the ones whose explanation already shows the method.
`math_check.py 12 13 32`: PROBLEMS 0, WARNINGS 0, LAYOUT 0.

## 2026-10-07 shaded number lines
Function `number_lines` (runs last; figure helper `math_patches/_shaded_nl.py`, same look as the "within 4 of 2"
figure). ONE click figure + ONE short spoken line per video; method, numbers and answers unchanged. A video recorded
before `_shaded_nl.CUTOFF` is skipped; none of these was recorded when this was made.
- solve-q-360 · "Small side: closed range": |x + 3| < 7 - the hand-drawn distance sketch is now the click figure (dot at
  −3, 7 each way, band −10 to 4) + "Small side: one band, shaded in between. Three is inside it." (+≈4 s).
- solve-q-361 · "Big side: open range": 8 < |x + 1| - the hand sketch is now the click figure (dot at −1, 8 each way, two
  rays outward from −9 and 7) + "Big side: two rays going outward — and a forbidden gap in the middle." (+≈4 s). Room
  kept under "x > 7" for the hand-written second case.
- solve-q-369 · "Method 1 · Two symmetric bands": the two answer bands −4 < x < −3 and 4 < x < 5 (+≈6 s). The teacher's
  early hand sketch (shade 7 to 9 and −9 to −7) can go to the right of the first lines; the figure appears at the bottom.
- solve-q-370 · "Method 1 · Two cases": x < 6 as one ray, open circle at 6 (+≈6 s).
`math_check.py 12 13 17 32`: PROBLEMS 0, WARNINGS 0, LAYOUT 0. Renders: tmp_check/numlines/t13-t17.png.


## 2026-10-07 trim added repeats

Teacher: only OUR additions that re-teach something learned earlier in the study plan are trimmed; the Hebrew course's own repeats stay. `trim_added_repeats(M)` runs last in apply(); helpers in `_trim_repeats.py` (videos with a take recorded before its CUTOFF are left as recorded). Notes updated in added_notes.json.

- r26-t13-tools: √(x²) = |x| (topic 9 Roots) and the plus-inside / more-than-k distance readings (this topic's |x+3| < 7 and 8 < |x+1| questions) cut. ~31 s.

## 2026-10-08 Hebrew theory restored
Teacher: the 2026-10-05 "cut repeats" pass removed the lesson's equations / inequalities theory, assuming the question videos teach it — "that way I am missing content". absolute-value, solve-q-358 and solve-q-359 are recorded and stay as they are. The missing teaching from the Hebrew lesson now sits in the next unrecorded videos, at the moment it is used. Function `hebrew_theory_back(M)` runs LAST; a video with a take recorded before `HT_CUTOFF` keeps its recorded version. Notes updated in added_notes.json.
- **solve-q-360** "Small side: closed range" (+5 lines, 1 board item, ≈ +25 s): the range is always symmetric; WHY closed — the inside without its sign must be less than 7: 6, 5, 4 and −6, −5 fit (the minus disappears), 9 and −9 fail (the bars turn −9 into 9); "exactly like x squared smaller than a number: small side — closed range". Board item by click: "inside: 6, 5, …, −5, −6 ✓ 9, −9 ✗" (the empty row for the hand-written −7 < x + 3 < 7 now sits under it). The check "|3 + 3| = 6 < 7 ✓" moved to the right of −10 < x < 4 so the shaded number line (2026-10-07) keeps its full size above the choices.
- **solve-q-361** "Big side: open range" (+3 lines, ≈ +18 s): WHY open — the inside without its sign must be more than 8: 9, 10, 11 and −9, −10 (the minus disappears); "two rays, an open range — exactly like x squared bigger than a number". At the end: "Absolute value in an inequality is the harder part of this topic. It is also rarer on the exam."
- **solve-q-362** "Method 1 · Plugging in numbers" (+1 line, ≈ +4 s): "Like almost every topic — trial and error works here too."
- **solve-q-r26-t13-01** "Two cases" (+2 lines, ≈ +12 s; the next equation question after the recorded q-359): the general rule "the left side equals the right side — or minus the right side; the same left side, twice"; at the end the wording point: "all the values" needs both, "could be" needs one — often only one is offered.
`math_check.py 13 32`: PROBLEMS 0, WARNINGS 0, LAYOUT 0. The four videos rendered and looked at (tmp_check/htb/).

## 2026-10-08 topic 13 restored + clearer
Teacher (2026-10-08): "Also fix the things I already recorded in topic 13 that need changes. Make the explanations clear, and when a number line helps, add it." Re-recording is OK. Function `restore_and_clarify(M)` in t13.py runs LAST. Number lines use `_shaded_nl.py` (same look as 2026-10-07). Only the three recorded videos on the re-record list (`_rerecord.py`) change; any other video recorded before `RS_CUTOFF` would stay as recorded (none is).

**Re-record (topic 13): `absolute-value`, `solve-q-358`, `solve-q-359`** — option 1, re-record the whole video.

- **absolute-value** (recorded → RE-RECORD; 3.2 → 6.7 min, ≈ +3.5 min). The Hebrew lesson's theory is back, in the Hebrew order, with our own numbers (Hebrew: |x + 4| = 9, |x| > 5, |x| < 5):
  - new slide **Sign clues**: |x| > x → negative; |x| = x → zero or positive; |x| = −x → zero or negative; x > |x| → impossible (givens contradict); don't forget the zero; "comes up on the exam again and again".
  - new slide **Equations**: |x| = 5 → 5 or −5 (number line: two points 5 from 0); the rule — left side = right side, or = minus the right side; why the minus.
  - new slide **Two cases**: |x − 2| = 6 → x = 8 or x = −4, "the same left side, twice"; number line: |x − 2| = distance from 2; a plus inside = distance from the negative number.
  - new slides **Inequalities · big side / small side**: harder part; big side / small side; the range is always symmetric; |x| > 4 → x > 4 or x < −4 and WHY (the bars wipe out the minus), number line with two rays (open circles) → open range; |x| < 4 → −4 < x < 4 and WHY (−7 fails: the bars turn it into 7), number line with one band → closed range; exactly like the x² inequalities.
  - new slide **Wrap-up**: expression / equation / inequality; trial and error works here too; inequalities are harder and rarer — rewind; "Seven questions next" moved here from "When is it equal?".
  - Sidebar: + Sign clues, Equations, Inequalities, Wrap-up.
- **solve-q-358** (recorded → RE-RECORD; 1.8 → 1.4 min, ≈ −24 s): slide "The sign clues" repeated the lesson's new slide → removed; on "Decode the signs" the line now says "The sign clue from the lesson: y is NEGATIVE."
- **solve-q-359** (recorded → RE-RECORD; 0.9 → 1.1 min, ≈ +11 s): number line after the second case — |x + 7| = 9 is the distance 9 from −7: two points, 2 and −16 (+1 line).
- **solve-q-360** (≈ −9 s): today's full WHY (4 lines + the "inside: 6, 5, … ✓ 9, −9 ✗" board item) → one reminder "As in the lesson: small side — closed range. x is trapped between two numbers." The check returns under −10 < x < 4.
- **solve-q-361** (≈ −8 s): the WHY (2 lines) and "harder, rarer" → "As in the lesson: big side — open range, two separate cases."
- **solve-q-362** (≈ −5 s): "Like almost every topic — trial and error works here too" removed (the lesson's Wrap-up says it; the title slide already says "we may plug in").
- **solve-q-r26-t13-01** (≈ −15 s): the general rule → "As in the lesson: the same left side, twice."; the wording line shortened to "Here they ask for ALL the values — so we need both."
- **r26-t13-tools** (≈ +3 s): Distance slide's first line → "You met it in the lesson: bars around x minus a number give the distance from that number."
- Number lines added where they clearly help: **solve-q-363** (the hand sketch of n, k, m becomes a click figure n, 0, k, m — the order is the answer; ≈ +10 s), **solve-q-365** (the band between y and −y where x can be, left or right of zero; ≈ +11 s), **r26-t13-summary** "Inequalities" (|x − 5| < 3 one band, |x − 5| > 3 two rays; ≈ +9 s).
- Notes in added_notes.json updated for every touched slide.
`python3 math_check.py 13 32`: PROBLEMS 0, WARNINGS 0, LAYOUT 0. All changed videos rendered and looked at (tmp_check/rs13/).
