# Topic 21 — Trial, limits and patterns: changes

Patch: `math_patches/t21.py`. Check: `python3 math_check.py 21` shows 0 problems and 0 layout problems. The 7 warnings left are all clock times ("07:30", "8:00"). These are real times, not division.

## Summary
- Questions: 41 rewritten, 11 added (2 guided with solution videos and 9 practice), 2 removed.
  The topic had 16 guided and 27 practice questions. It now has 18 guided and 34 practice questions.
- Slides: 3 added ("Cheapest k different", "Worst case + 1", "Days and last digits"), 2 removed ("A recurring motif" and one old Q13 method). About 20 slides changed.
- New videos: 2 solution videos (the new guided questions, numbered 9 and 15 after renumbering).
- Memory cards: both cards updated ("Trial and error: three types" and "Trial & error toolkit").
- The second "Minimum & Maximum" video is renamed "More Minimum & Maximum".

## 1. Wrong rule fixed (priority)
- **Q13 (now Q14) video, "The range has no holes":** this said "In min-max questions the possible values form a continuous range. No holes." That is false in general, and the skip questions in this same topic (Q6, p03) have holes. The video now has:
  - **Method 1 · Count the spare markers** (now first): 24 × 3 = 72, 86 − 72 = 14 spare, so at least 24 − 14 = 10 boxes stay at 3. Nine is impossible.
  - **Method 2 · Only the ends?**: the possible values are 10 to 23 with no holes, **because the count can change by 1 at a time** (each spare marker lifts one box). Only then must the impossible choice be at an end. The teacher then says: "This is NOT a general rule." Example: the 4-or-9 token jumps by 5 (24, 29, 34…), so there are holes.
  - The old "Edge cases" slide and the separate spare-markers slide were merged into these two slides.
  - The intro now says: "the same question as Question 8, with the same numbers" (the review asked for a clear "Question 8 again").
- **Toolkit card:** the row "'Cannot be' in a min–max question → the range has no holes" now says: "the odd one is at an end ONLY if the value can change by 1 at a time. Fixed jumps (+5, +3…) leave holes."
- The written solution of the question says the same.

## 2. Methods added
- **Worst luck + 1 (pigeonhole).** Topic 20 already teaches this with the socks-pair example, so it is not taught again here. There is one short, applied slide "Worst luck + 1" in "More Minimum & Maximum" (after "At least"). It points back to Algebraic Understanding and uses it as a min-max idea: 4 players, and the game ends at 3 wins, so the worst luck is 2 wins each = 8 rounds, and 8 + 1 = 9 rounds at most. The wording matches T20: "worst luck + 1".
  - New guided question **q-r26-t21-01** (socks 10 red / 8 blue / 6 green, sure of 3 of the same color → 7) with a solution video. Method 1: worst luck 2 + 2 + 2 = 6, then + 1. Method 2: each wrong choice answers a different question (4 = the pair from T20, 17 = three red, 9 = three of each).
  - Practice: q-r26-t21-03 (sure of 2 black balls → 16), q-r26-t21-04 (cards 1 to 20, sure of a pair that adds up to 21 → 11, hard), q-r26-t21-05 (30 students → at least 3 born in the same month; this is also "must be true").
  - p14 (four players) solution now uses "worst luck + 1".
- **Must be true.** New guided question **q-r26-t21-02** (five different positive integers with sum 20; "the largest is at least 6") with a solution video. Method 1: find counterexamples to kill three choices. Method 2: prove the one left (1 + 2 + 3 + 4 + 5 = 15 ≠ 20). Practice: q-r26-t21-05 (months) and q-r26-t21-06 (three friends, 25 marbles, "the largest share is at least 10").
  - "How to Approach Word Problems", slide 4 ("Possible vs must", now called "Must or could") is a short reminder of Topics 1 and 20, in their wording: "Could be true → one example is enough · Must be true → every allowed case". It is not taught again here. The "three types" card tip uses the same words, and the toolkit card rows point to Topics 1 and 20.
- **All min/max rules on one board.** Slide 2 of "More Minimum & Maximum" is now "Three min/max rules", with one example each (total 26): max of one → give the others the least (1 + 2 + 23); min of the largest → share as equally as possible (7 + 9 + 10); min of one → give the others the most (each at most 10: 10 + 10 + 6). The teacher explains why rules 2 and 3 only *sound* opposite. The recap and the toolkit card use the same wording.
- **1 + 2 + … + k = k(k+1)/2.** New slide "Cheapest k different" in the first "Minimum & Maximum" video. It is taught with the pairing trick (1 + 8 = 2 + 7 = … = 9, four pairs = 36). Q3 method 2, p07 and p27 use it. It was added to the recap and to the "three types" card.
- **Spare units** ("fill everyone to the minimum, then count what is left") is now a named row on the toolkit card. It is Method 1 of Q14, and p25's solution uses it.
- **Sequence plug-in rule** (Patterns video, slide 4): "Two choices survive? Also try n = 4. n = 1 only as a quick extra check." Recap and card updated. Practice: q-r26-t21-07 (a_n = 4n + 1), q-r26-t21-08 (sum of first n terms is n² + 2n → 10th term 21; hard, 120 is the trap), q-r26-t21-09 (2 + 4 + … + 2n = n(n + 1)). Each one has an n = 1 tie that n = 3 breaks.
- **Days of the week and last digits.** New slide "Days and last digits" in "Patterns & Cycles": Tuesday + 30 days → Thursday; units digit of 3²² → cycle 3, 9, 7, 1 → 9; "remainder 0 means the last one in the cycle". Recap and card updated. Practice: q-r26-t21-10 (Monday + 100 days → Wednesday), q-r26-t21-11 (units digit of 7⁵⁰ → 9).

## 3. Teaching fixes in the videos
- First "Minimum & Maximum": the "A recurring motif" slide was removed, and its point is now one line on "Ranges". "Bold words" now says: "In our questions, find that word yourself and circle it", because our stems cannot show bold. The Q3 video now says "Find the key word and circle it" instead of "Read the bold word".
- "How to Approach Word Problems", slide 5, and "Smart Trial & Error", slide 2, were shortened. The "spoon-fed at school" lines were removed.
- Q9 (now Q10) video, method 2: renamed "Last digit — and its limit". It says honestly that for the maximum the last digit cannot help, so we just multiply.
- Q12 (now Q13) video: "They ask 'at least' / 'at most'" is now "They ask for the smallest / the largest".
- Division ":" replaced with ÷: "28 ÷ 4 = 7" (More Min & Max), "12 ÷ 4 = 3" (Q10 video). Q16 draw notes: "18: 7:30…" is now "every 18 min → 7:30…".
- The recap of "More Minimum & Maximum" now leads into the new socks question before the last-digit questions.
- The sidebars of all "Advanced" solution videos list the new questions. The build renumbers them automatically.

## 4. Questions rewritten (text)
All 16 old guided questions and all 25 kept practice questions now have written solutions with TeX, the numbers in each step, a space after every comma, no "so" in the middle of a sentence, and "Choice N" at the end, matching the key.
- Stems reworded: g007 (Q3), g014 (Q7, "Which of the following can be the number of dancers?"), g017 (Q10), p06 ("NOT true"), p07 (TeX n), p12 (**"any of them may be blue"** added, as the review asked), p16, p17, p24 ("must also be red" instead of "necessarily").
- p05: every day is written out in full ("start 48 → sell 24, keep 24 → add 72 → 96").
- p13: the "cheapest upgrade per kilogram" argument is replaced by a full list of all 6 mixes of 5 packages that make 28 kg, sorted by the number of 8-kg packages (costs 36, 37, 37, 38, 38, 38).
- Q4: "Halving forty-five would describe a different rule" is now "Don't subtract first: 46 − 1 = 45 and then 45 ÷ 2 is the wrong order."
- Q14 (boxes again): the solution now starts "The same boxes as the earlier question, now with a shortcut."

## 5. Practice
- Removed near-duplicates: **p26** (the same 4/9 six-pack question as Q6) and **p23** (the same "different amounts" question as Q3 and p07).
- Added 9 new questions (see section 2). Exam-hard items now: p12, p13, p17, p18, q-r26-t21-04, -05, -06, -08 and p19/p24.
- Order is now easy → hard: p21, p02, p04, p01, p08, p22, p27, p07, p16, p11, p10, t21-07, t21-10, t21-11, t21-03, p05, p09, p15, p20, p03, p25, p14, p19, p24, p06, t21-09, t21-05, t21-06, p12, t21-08, t21-04, p13, p17, p18.

## Could not do / for the teacher to decide
- The stems cannot show bold text, so key words like LARGEST are not bold. The video now tells students to circle the word themselves.
- Q8 and Q14 are still the same question on purpose (first by testing the answers, then with the shortcut). The Q14 video and solution now say so clearly. If you would rather merge them, Q14's slides could become methods 2 and 3 of Q8.
- Clock times (07:30 and similar) still trigger the checker's colon warning. They are genuine exceptions.
- The review asks to merge the two sets of min/max rules. Both videos are kept, but the second video now shows all three rules on one board, and the two recaps and cards use the same words.

## Pass 2 (teacher-approved remove/restore plan + summary lesson)
**Removed (1):** practice q-r26-t21-08 (sum of the first n terms is n² + 2n → 10th term). It is not on the real exam and not in the original course. It is also gone from the practice order.

**Restored (3):**
- Practice **wp21-p23** (36 stickers, different amounts → 8 children). Clean-up only: a clearer stem ("a different positive whole number of stickers") and a full solution: 1 + 2 + … + 8 = (8 · 9)/2 = 36, and nine children need 36 + 9 = 45 > 36. Choice 4. Placed after p10.
- Practice **wp21-p26** (six packs of 4 or 9 markers → 42 is impossible). Clean-up only: a full solution (24, 29, …, 54, and 42 is skipped). Choice 4. Placed after p03.
- **"Minimum & Maximum", slide 3 "A recurring motif"** is back as it was, with its sidebar entry. The line that pass 1 had moved onto "Ranges" was removed, so the point is not made twice. The video now has: Ranges, A recurring motif, Bold words, Squeeze the others, Balance the group, Cheapest k different, Recap.

**Kept, as the plan says:** "Days and last digits", q-r26-t21-10 and -11, and the corrected "no holes" slide and card row.

**New: summary video `r26-t21-summary` "Summary: Trial, Limits and Patterns"** (about 3.4 min), at the end of "Further guided examples", right before the practice. Slides: Summary · Three types · Try in order · The skip · Push the right way · Different amounts · Worst luck + 1 · Patterns · Cycles · Before you practice (checks: which type, which way to push and does the example really work, must or could, constant step and the skip, the edges; traps: being inside the range is not enough, n = 1 alone, and "at least" is a lower limit, not the answer when they ask for the maximum). The examples all come from the lessons, not from the practice questions.

Practice now: 27 original questions (all of them) + 8 added = 35.

## 2026-10-05 cut repeats
Function `cut_repeats` (runs last). Each lesson is back to a short intro like the Hebrew course ("type N of trial and error, what it is, let's see a question"). Every idea that a question video right after it teaches is cut from the lesson; ideas no question teaches stay, or move as one spoken line + one board item into the question video that uses them. Nothing in topic 21 is recorded. Questions, numbers, methods and memory cards are unchanged.
- **`wp-003` General Problems**: 6 slides, 2.1 → 0.7 min. Kept: title + "Try and err" (the Hebrew intro) + "Let's see two questions of this type." Cut: "Draw the story / split into routes" → Q1 crystals (draw, follow, the other road); "test the choices" → Q2 queue; Recap. MOVED into Q2 `solve-wp21-g005` slide 2: "Keep your tries in order, and make every try pass every condition." + board "Tries in order · every try passes every condition" (from "Keep an order" and "Every condition").
- **`wp-006` Minimum & Maximum**: 8 → 3 slides, 2.9 → 0.9 min. Kept: title, Ranges, A recurring motif (the Hebrew intro). Cut: "Bold words" → Q3 already circles the key word; its line now says "Find the key word — on the exam it is printed in bold — and circle it". "Squeeze the others" → Q3 (give each as little as possible). "Balance the group" and the 26 = 1 + 2 + 23 / 7 + 9 + 10 example → still taught in "More Minimum & Maximum" (same numbers) and Q13. "Cheapest k different" → Q3 method 2 has the formula; MOVED the "why": "Pair the ends of one to eight… four pairs of nine. Thirty-six." + board "1 + 8 = 2 + 7 = 3 + 6 = 4 + 5 = 9 → 4 × 9 = 36". Recap cut.
- **`wp-008` Patterns**: 6 → 2 slides, 2.3 → 0.6 min. New single slide "Two kinds": step by step (write the items one by one) and sequences with n (plug in a number). Cut: the 52 worked example (Q4 does the same rule with 46), "Sequences" and "Plug in n = 3" → Q5 crates (no school formulas, n = 3, why not n = 1). MOVED into Q4 `solve-wp21-g009`: "Keep the rule's order: halve first, then subtract. And the drops won't be equal — so apply the rule every round." + board "Halve, then subtract — every round". MOVED into Q5 `solve-wp21-g010` method 2: "And if two choices still survive n equals three? Plug in four as well." + board "Two survive? Also try n = 4". Recap cut.
- **`wp-012` Smart Trial & Error**: 6 → 2 slides, 2.2 → 0.6 min. Kept: title + "Why it matters" (the Hebrew motivation). Cut: Work in order (tickets 6/11), The skip, Constant step (remainder) → all taught in Q6 token 4/9 (in order from the minimum, +5 swaps, skip, remainder pattern). MOVED into Q6 `solve-wp21-g013`: "Only how many fours and nines matters — not which toss came first." and "Forty-one is inside the range — and still impossible. Inside the range is not enough." + board "Inside the range is NOT enough". Recap cut ("Numbers in the answers? Plug them in" → Q7, Q8).
- **`wp-016` More Minimum & Maximum**: 6 → 2 slides, 2.5 → 1.1 min. Kept: title + "Three min/max rules" (rule 3, "min of one → give the others the most", is not taught by a question; rules 1–2 now appear here once instead of twice). Cut: "At least" → Q10 quiz ("at least a quarter" → all correct for the max); "Worst luck + 1" → Q9 socks; "Prove, then build" → MOVED into Q9 `solve-q-r26-t21-01`: "That's the rule for every min or max: show nothing more extreme works — and build a real example." + board "Min or max: prove the bound · build an example". Recap cut (last-digit trick → Q10, Q12).
- **`wp-022` Patterns & Cycles**: 8 → 2 slides, 2.8 → 1.1 min. Kept: title (the Hebrew reminder: no school formulas, term by term) + "Days and last digits" (no question video teaches them); its "The same remainder trick" → "One remainder trick", "Lamps, days, digits" → "Days, digits — and the lamps in the questions". Cut: "Term by term", "Watch the edges" → Q16 files; "Repeating cycles" → Q17 lamps; "Meeting times" → Q18 lights (bigger number, fewer jumps, the edge). MOVED "Items vs gaps" into Q18 `solve-wp21-g025` method 2: "Four flashes have only three gaps between them. Items and gaps are different counts." + board "4 flashes → 3 gaps of 72 min". Recap cut.
- Unchanged: `wp-001` How to Approach (no question repeats it), the summary lesson, both memory cards.
- Question videos lengthened: g005 1.7→1.8, g007 1.4→1.6, g009 0.9→1.0, g010 1.1→1.2, g013 1.2→1.4, g025 1.1→1.2, q-r26-t21-01 1.2→1.4. **Net: −8.8 min.**
- No video said "as we saw in the lesson" about a cut idea. AI summary `r26-t21-summary` not edited; everything it recaps is still taught (lesson slides kept or the question videos).
- **Follow-up (same day): every cut idea checked again.** One idea had disappeared. The second test from "Constant step" ("subtract twenty-four — you need a multiple of five") is now in Q6 `solve-wp21-g013` method 2 as one line + board item "41 − 24 = 17 — not a multiple of 5 ✗". Everything else that was cut is taught in the video named above. The only things gone are examples whose rule is still taught with a different example: the four-player game ("worst luck + 1" is taught with the socks in Q9), the 28-member "at least a quarter" (Q10's quiz), and the 6/11 tickets (Q6's 4/9 token).

## 2026-10-06 practice: new methods
No change. Every 2026-10-06 method is taught in topic 23 or later (flip rule, arrow map, hidden total, shares as weights, compare by factors, the V in motion, doors) or in topic 51 (pick values that fit), and none of the topic 21 practice questions has more unknowns than equations, so nothing fits without forcing it. Topic 21's own min/max method is already what these questions use. Nothing in topic 21 is recorded.
