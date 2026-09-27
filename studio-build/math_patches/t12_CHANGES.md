# Topic 12 — Inequalities: changes

Patch: `math_patches/t12.py`. Check: `python3 math_check.py 12` shows 0 problems, 0 warnings and 0 layout problems.

## Summary
- Questions: 42 rewritten, 12 added (4 guided with solution videos, 8 practice), 1 removed (q-340).
  The topic had 16 guided and 27 practice questions. It now has 20 guided and 34 practice questions.
- 13 slides changed in existing videos. The sidebars of the 8 advanced solution videos now list Questions 9 to 20.
- 2 new lesson videos: "Signs, Fractions & Must-Be-True" (6 slides) and "Combining Inequalities & Ranges" (6 slides).
- 4 new solution videos, for the new guided questions.
- 1 new memory card: "Inequality traps". The old card "Inequality rules" got 3 rows changed or added.
- Figures: this topic has none.

The guided questions are renumbered in course order: the new ones are Q9, Q10, Q17 and Q18, so the old Q9–Q16 are now Q11–Q16, Q19 and Q20.

## 1. Wrong or misleading teaching (fixed)
- **Lesson 1, slide 4 ("A minus flips it"):** the old demo ended with "1 < 3 … same answer — three greater than one". Students could not see why that was the same answer. The new demo:
  - −12 < −4 divided by −4 gives 3 > 1, so the sign must flip.
  - Then it solves −2x < 6 in two ways: divide by −2 and flip (x > −3), or move the terms across (−6 < 2x, so −3 < x) with no flip.
  - It ends with a check using x = 0.
  - Students now see one flip done in full.
- **"Cross-multiply" removed** from lesson 2 slide 6, from the Q7 video (the slide title is now "Multiply by 6, then the rule") and from the Q11 (old Q9) video. The teacher now says "multiply both sides by 6 / by 2(x + 1) — a positive number, so nothing flips".
- **Q5 video:** the unclear "you could even ignore the ninety — x⁴ < x⁵" is now explained: divide x⁴ < x⁵ by x⁴ (it is positive), so x > 1.
- **Q20 (old Q16, q-337) solution text:** removed the false start (x = −1, y = −0.5 was not a counterexample).
- **q-350 solution text:** removed the unfinished "Add the two inequalities: (a − b) + (something)". It now uses the chain, plus a correct way to add them (b − a < 0 and a + b < 0, which gives 2b < 0).
- **Garbled boards (review §3):** I rendered them. Lesson 1 slide 2 and lesson 2 slide 6 display correctly on the slides. The loss happened only in the text dump the reviewer read. Q9 and Q11 on screen also show proper fraction bars. No change was needed.

## 2. Methods added
**Lesson 1:** the recap now says "× or ÷ by a negative" (it said ":").

**Lesson 2, slide 6:** added a worked **x² on the big side** example: −2x² ≤ −32. Divide by −2 and flip to get x² ≥ 16, so x ≥ 4 or x ≤ −4. A number check follows. The recap line now reads "x² small side: between the roots · big side: outside".

**New lesson "Signs, Fractions & Must-Be-True"** (start of the advanced section, before the first advanced question):
1. **Between 0 and 1:** x² < x < √x < 1 < 1/x, tested with x = 1/4. For x > 1 the order turns around (tested with 4). For negatives, plug in −1/2.
2. **Reciprocals:** same sign → the sign flips; different signs → no flip. Three examples.
3. **Sign table** for a product or a fraction: mark the zeros, then test one number in each part. Example: 3x(1 − 3x) > 0 gives 0 < x < 1/3 (this is q-352).
4. **Must / could / cannot:** one counterexample kills "necessarily true"; one example keeps "could be true"; "cannot" breaks the givens. The list of numbers to try: 0, 1, −1, ½, a big number.
5. Recap.

**New lesson "Combining Inequalities & Ranges"** (right before Q19, the xy range question, old Q15):
1. **Add** inequalities that point the same way: 1 < a < 3 and 2 < b < 5 give 3 < a + b < 8.
2. **Never subtract** end from end. The trap is shown: for a − b, biggest a minus smallest b gives −4 < a − b < 1. Another way: flip b, then add.
3. **Multiply:** end by end only when everything is positive. Otherwise check the four corners (−1 < a < 3 and 2 < b < 5 give −5 < ab < 15). Division works the same way, and the bottom must not be 0.
4. **Range of x²:** from −3 < x < 2 you get 0 ≤ x² < 9, not 4 < x² < 9.
5. Recap.

**Additions to existing solution videos:**
- Q11 (old Q9): why x/(x+1) grows with x.
- Q13 (old Q11): points to the sign table.
- Q15 (old Q13): the chain is drawn on a number line.
- Q20 (old Q16): the numbers-to-try list is now a board line.

**New guided questions** (each has a solution video):

| # | id | Question | Answer |
|---|---|---|---|
| Q9 | q-r26-t12-01 | −1 < x < 0: which of x, x², x³, 1/x is the greatest? | x² (plug in −½) |
| Q10 | q-r26-t12-02 | (x − 2)(x + 5) < 0 | −5 < x < 2 (sign table) |
| Q17 | q-r26-t12-03 | a > b and c > d: which is necessarily true? | a + c > b + d; counterexamples for a − c > b − d, ac > bd and a/c > b/d |
| Q18 | q-r26-t12-04 | −2 < x < 5 and 1 < y < 4: range of x − y | −6 < x − y < 4; choice 2 (−3 < x − y < 1) is the end-from-end trap |

**Memory cards:**
- "Inequality rules" now has:
  - the move-across example (−2x < 6 → −6 < 2x)
  - a row "multiply by an unknown only if you know its sign"
  - a worked example for x² > a
- New card "Inequality traps" (after the last advanced question) has three tables: combining and ranges; signs and special numbers; question words. It ends with two tips.

## 3. Text (all 42 remaining questions)
- Every stem, choice and solution is in TeX, with no ":" for division. The old solutions wrote 1:2, 2x:5, −5x:2, 1:3 and so on.
- Stems with several conditions are stacked with `\begin{cases}`: q-327, 329, 333, 334, 336, 339, 343, 347, 348, 350, 351, 353, 355, 356 and 357, and extra-6.
- Every solution shows the numbers. The 7 extras had word-only solutions, and each now has worked lines and a check.
- Solutions use the taught method:
  - sign table for q-352 and q-354
  - try-a-number for q-332
  - "multiply by a positive number" for q-328, q-330 and q-355
- Several solutions also mention the faster way.
- **Q2 (q-323) choices** were "0 / 12 / 1 / Any value". They are now ranges: "Only for x < 0", "Only for x > 12", "Only for x < 1", "For every value of x". The key is unchanged (choice 4).
- q-325 choice 3 is now "For no value of x" (it said "(empty set)"). q-338 choices are full sentences. q-352 and q-357 write −1/3 as −⅓, not as (−1)/3.
- Wording like "precise domain" and "From this it necessarily follows that:" is now "most precise range" and "Which of the following is necessarily true?"

## 4. Practice
- Removed **q-340**, a near-duplicate of q-339.
- The 8 new exam-level questions:

  | id | Question | Skill |
  |---|---|---|
  | q-r26-t12-05 | range of a − b when b is negative | range of a difference |
  | q-r26-t12-06 | x² from −3 < x < 2 | x² range trap |
  | q-r26-t12-07 | x + y > 10 and x − y > 4 | add the inequalities: x > 7 |
  | q-r26-t12-08 | smallest of 1/x, 1/x², √x, x for x > 1 | order above 1 |
  | q-r26-t12-09 | (x + 1)/(x − 4) < 0 | integer count with a sign table |
  | q-r26-t12-10 | x < y < 0 | "could be true" |
  | q-r26-t12-11 | range of ab with negative ends | four corners |
  | q-r26-t12-12 | a > b > 0 | "cannot be true" with reciprocals |

- The section is ordered easy → hard. The 7 easy extras come first as a warm-up. The exam-hard items come last: q-350, the new 10 and 11, q-355, q-356 and q-357.

## Answer checks
I solved every new and changed question from scratch. Each has exactly one correct choice, and the key matches its solution video ("Circle choice N"). Keys of the existing questions are unchanged.

## Notes for the teacher
- The API has no call to change a board item's text only. I changed the item text directly on the slide (lesson 1 recap, lesson 2 recap), and the patch marks those videos as touched.
- The new lesson "Signs, Fractions & Must-Be-True" sits at the start of the advanced section, so the first two advanced questions are now the new Q9 and Q10. If you prefer the old Q9 (x/(x+1)) to open the section, move the video and its two questions after it.
- Q15 (old Q13, "which is NOT necessarily true") has a choice that is never true. That is fine for the key, but you may want to reword the stem to "Which of the following is not true?"
