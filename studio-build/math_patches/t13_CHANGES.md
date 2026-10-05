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
