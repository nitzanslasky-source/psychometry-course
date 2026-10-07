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

## 2026-10-06 renumber pass
The goal is that the English course does not look like the Hebrew one. Every Hebrew-derived question gets a new story (names, objects, setting) and new numbers. The math structure, the trap, the level and the methods stay the same. Every guided solution video is rewritten to match: speech, draw cues, board items, tables and sequence boxes, the video title, and the title-slide line that names the story. Nothing in Topic 21 is recorded (checked ~/Documents/Course.recordings), so nothing had to be kept as it was. Function `renumber_pass(M)` in t21.py runs last (after `summary` and `cut_repeats`; topic 21 has no `practice_methods` lines).

**Counts:** 16 guided questions renumbered with their 16 solution videos rewritten. 20 practice questions renumbered (wp21-p01 … p20). Lesson examples: none are Hebrew-derived (the lessons were cut to their Hebrew intros on 10-05; the remaining examples, such as the summary, "Tuesday + 30 days", 3²² and the 26 = 1 + 2 + 23 board, were made in English), so no new numbers were needed. Two lines that named the old lamps now say "flags" (the Patterns & Cycles lesson and the toolkit card). Practice: **35 → 26**.

**wp21-g015 = wp21-g021 (word for word the same):** In the Hebrew, the teacher solves the planters question by plugging in (advanced trial and error). Later, in the advanced min-max lesson, he comes back to the same question to show the shortcut. Neither one is a stray copy, because each has its own video and method. They are now two different questions of the same type. Q8 (g015): 22 baskets, 80 apples, plugging in → 7. Q14 (g021): 26 children, 90 stickers, the spare-units shortcut plus the "only the ends" range idea → 13. The Q8 video now ends "We'll come back to this type with a shortcut". The Q14 video starts "Stickers this time — the same type as Question eight, with new numbers", and its written solution starts "The same type as the apple baskets, now with a shortcut."

**Order:** Q9 (g017, spelling test) and Q10 (g018, piggy banks) are rated easy+ in the Hebrew. They move before the socks question (medium), right after "More Minimum & Maximum". The socks question is now Q11. Nothing in either video depends on the other (the last-digit trick is still taught in g017 before g019 uses it "from before"). The titles and sidebars are renumbered by the build. The correct-answer positions changed. Guided keys are now 3, 2, 2, 2, 1 | 2, 3, 4, 3, 1, 2, 4, 2, 2, 3, 3 (before: 4, 4, 4, 2, 4, …).

**Practice clean-up (35 → 26):**
- Copies removed: wp21-p26 (six packs of 4 or 9 markers, the same as the old guided token question), wp21-p23 (36 stickers in different amounts, the same as guided Q3), q-r26-t21-11 (units digit of 7⁵⁰, the same as Topic 15 and Topic 18 items).
- Extra warm-ups: 3 kept (p21 printer, p27 largest of five scores, p25 spare pencils). Removed p22 (lights every 8 and 14 s, the same as guided Q18 and the summary's 8-and-14 example) and p24 (52 lockers, one red in every 4, locker 2, the same as the old guided lamps question).
- September items: 3 kept, each a type the Hebrew practice does not have: -07 (n-th term, plug in n = 3), -10 (Monday + 100 days), -06 (must be true, three different shares of 25). Removed -03 and -04 ("to be sure": worst luck + 1 is practised by p14 and guided Q9), -05 (birthdays: worst luck + must), -09 (sum of evens: the same plug-in as -07 and guided Q5).
- That is one above the audit target of 25, because three September types are not in the Hebrew practice.
- New order, easy → hard: p21, p02, p04, p01, p08, p27, p07, p16, p11, p10, -07, -10, p05, p09, p15, p20, p03, p25, p14, p19, p06, -06, p12, p13, p17, p18.

**Checks:** every key was brute-forced in Python. This covered all pop routes, all vehicle lines, all chip totals, every distribution for the baskets and stickers, every piggy-bank sequence, every split of 36 cards, every 5-box mix and every rope combination. Each question has exactly one correct choice, and each trap is still a choice: the wrong road (4), the skipped 20 / 32 / 23, n = 1 tie, 27 = 27 tenors, 7 just below the minimum 8, "at least ⅕" as the maximum (70, 140), off-by-one ranges, 34 → 1 + 1, 110 after the removal, 09:20 = third, Wednesday's 18 and Friday's 3, 6 additional workers. Every step in the videos was recomputed. A duplicate check over a build of all topics (stems, choices, lesson boards and lines, cards) found only number coincidences, with no question equal to another question or to a lesson example. The new numbers also differ from the Hebrew transcript (spaceships 3 small, 4 m / 2.5 m cars, 20 hair ties, 30 eggs, 7/11 coin, 50 animals, 20 planters / 70, 9–15 questions ⅓, 7 jars 8/32, 13 kids, 21 marbles, 65 eggs / 20, 40 kids every 3, coffee 12/15).
- The word "disc" was not used, because the NITE terminology pass turns it into "circle". The game piece is a "plastic game chip".
- `python3 math_check.py 21 32` → PROBLEMS 0, WARNINGS 0, LAYOUT 0. All 16 videos were rendered and looked at: the tables and sequence boxes match, and the sidebars highlight the right question.

| id (new Q) | old | new | answer |
|---|---|---|---|
| g004 (Q1) | 2 large crystals, large → 4 small, 3 breaks; 4/5/6/7 | phone game, 2 large bubbles, large → 5 small, 3 pops; 5/6/9/10 (totals 4 or 9) | 9 (3) |
| g005 (Q2) | van 5 m, scooter 2 m, gap 1 m; 8, 11, 14, 10 | truck 10 m, car 4 m, gap 2 m at a traffic light; 16, 20, 22, 28 | 20 (2) |
| g007 (Q3) | mentor, 32 pins, different amounts | Noa, 42 postcards to friends | 8 (2) |
| g009 (Q4) | drill 46 reps, halve −1, round 4 | bakery 78 loaves Mon, halve −1, Thursday | 8 (2) |
| g010 (Q5) | 3 crates doubling, total through day n | app 5 downloads doubling | 5(2ⁿ − 1) (1) |
| g013 (Q6) | token 4/9, 6 tosses; 41 | game chip 2/6, 7 tosses; 32 | 32 (2) |
| g014 (Q7) | festival dancers = 3 × singers, actors more, 70 | choir sopranos = 3 × altos, tenors more, 63 | 24 (3) |
| g015 (Q8) | 24 boxes, 86 markers, ≥ 3 | 22 baskets, 80 apples, ≥ 3 | 7 (4) |
| g017 (Q9) | quiz 12–20 questions, 16 students, ≥ ¼ | spelling test 10–25 words, 14 students, ≥ ⅕ | 28 and 350 (3) |
| g018 (Q10) | 9 jars, 6 … 42, ≥ 3 more, 5th | 8 piggy banks, 5 … 47, ≥ 4 more, 4th | 17 to 31 (1) |
| q-r26-t21-01 (Q11) | socks (English-made, unchanged) | – | 7 (3) |
| g019 (Q12) | 17 campers, 4–6 + 2–5 − (1–3) | 23 children at a fair, 3–5 + 2–4 tickets − (1–3) | 46 and 184 (2) |
| g020 (Q13) | Amir/Beth/Cara, 30 counters | Lior/Maya/Noam, 36 cards | 13 and 33 (4) |
| g021 (Q14) | identical to g015 (24 boxes, 86 markers) | 26 children, 90 stickers, ≥ 3 (spare units + ends) | 13 (2) |
| q-r26-t21-02 (Q15) | must be true (English-made, unchanged) | – | (4) |
| g023 (Q16) | 58 files, ×2, −16, day 3 before deletion | 40 bacteria, ×2, −30, day 3 before removal | 140 (2) |
| g024 (Q17) | 56 lamps, one blue in every 4, lamp 2 | 60 flags, one red in every 5, flag 3 | 43 (3) |
| g025 (Q18) | lights 18 / 24 min from 07:30, 4th | buses 16 / 20 min from 06:40, 4th | 10:40 (3) |
| p01 | 120 pieces, circles = squares > triangles | 150 beads, red = blue > green | 46 (3) |
| p02 | Nora / Sam sketchbooks, cases | Ella / Ben stamps, postcards | 5–19; 2–10 (2) |
| p03 | 4 vouchers of 2 / 7 / 12 | 3 stamps of 3 / 7 / 11 cents | 23 (3) |
| p04 | passes 120 / 60 / 30, 8, exactly 3 museum | tickets 90 / 50 / 20, 7, exactly 2 theater | 200–550 (4) |
| p05 | card shop, half sold, +3 per sold, 24 | pet shop, half sold, +2 per sold, 32 | 108 (3) |
| p06 | 1, ⅓, ⅑, … (÷ 3) | 2, ½, ⅛, … (÷ 4); reordered | "some term negative" (1) |
| p07 | 28 badges, n teams | 21 medals | n = 7 (2) |
| p08 | seats 1–270, every 6th / 9th | pages 1–240, every 8th / 12th | 10 (3) |
| p09 | 6 musicians (2) + 8 actors (4), 9 attend | 7 parents (3 cakes) + 5 teachers (1), 10 come | 20–24 (3) |
| p10 | 48 questions, +3 / −2, answers 42 | 40 questions, +4 / −2, answers 35 | 128 (4) |
| p11 | card 5 / 2, 7 draws, ÷ 8 | spinner 4 / 1, 6 spins, ÷ 7 | 21 (3) |
| p12 | 18 robots, ≥ half move, ≥ 4 blue stay | 24 students, glasses, ≥ 5 stay | 0–19 (3) |
| p13 | 2 / 4 / 6 / 8 kg at 3 / 6 / 8 / 10, 28 kg in 5 | 3 / 6 / 9 / 12 kg at 4 / 7 / 10 / 12 dollars, 42 kg in 5 | 44 (4) |
| p14 | 4 players, 5 min, stop at 4 wins | 5 friends, 4 min, stop at 3 wins | 44 (1) |
| p15 | 3–9 yellow, 5–8 black | 4–11 red pens, 6–9 blue pens | 11/17 (3) |
| p16 | 148 m fence, 3 m stripes, 2 m gaps | 116 m wall, 4 m stripes, 3 m gaps | 17 (2) |
| p17 | ribbons 18, 10, 5, 3; 7 | ropes 20, 12, 7, 3; 8 | 8 (4) |
| p18 | four 7-credit + three 1-credit tokens | five 5-cent + three 1-cent coins | 23 (2) |
| p19 | 27 volunteers, ⅓ remote | 33 store workers, ⅓ at night | 17–21 (1) |
| p20 | 8 parcels/h, +3 per extra, 7 volunteers | 12 boxes/h, +2 per extra, 6 workers | 132 (1) |

## 2026-10-06 review (renumber pass)
Independent review: all 16 guided (videos step by step), 20 practice items, practice removals, order change and the two
flag lines checked; keys brute-forced, traps present, same type/steps; nothing matches the Hebrew subtitles. No changes.

## 2026-10-07 methods spread
Function `spread_methods(M)` in t21.py runs last (after `renumber_pass`). Every guided and practice question was checked against the 2026-10-06 methods; a method is added only where it really solves the question, checked with numbers. Nothing in topic 21 is recorded (checked ~/Documents/Course.recordings).
- **The most precise range** (topic 12: test a number inside one choice and outside another), for "exact range" questions where the choices are ranges:
  - wp21-g018 (piggy banks, Q10): written line + **new slide 3 "Method 2 · The most precise range"** (+0.4 min): test 13 ✗ (choice 4 out), 35 ✗ (choice 3 out), 17 ✓ (choice 2 out) → choice 1. Slide 2 renamed "Method 1 · Min front, max back". Board lines by click, the pen only crosses out / circles.
  - wp21-p09 (cakes): written line. 20 ✓ → choice 4 out; 26 needs 8 parents ✗ → choices 1, 2 out.
  - wp21-p19 (stockers): written line. 22 ✗ → choice 3 out; 16 ✗ → choices 2, 4 out.
- Not added (checked): g017, g019, g020, p02, p04, p12 — testing the ends is the same work as the existing min/max solution. The remainder / LCM questions (g005, g013, g025, p03, p08, p10) already use the tag-it idea. No letter-answer question fits the power count (Q29 and Q5 choices are mixed or exponential).


## 2026-10-07 study-plan order
Function `plan_order_fix` (runs LAST). Students follow the study plan (`src/lib/planData.ts` ORDER), not topic numbers; named methods were checked against the plan rank of their teaching topic.
- wp21-p09, wp21-p19, wp21-g018: "Method 2 · The most precise range" → "Shortcut · The most precise range" + why (the right range holds every possible value and no impossible one). Topic 21 (day 8) is before topic 12 (day 20).
- Video solve-wp21-g018 (not recorded) slide 3: title → "Shortcut · The most precise range", one spoken why-line added. Rendered, checked.
- Video solve-q-r26-t21-01 (not recorded) slides 2–3: dropped "as in / the socks question from Algebraic Understanding" (topic 20 is near the END of the plan); the pair trap is now explained in place. wp-001 (not recorded) slide 4: "from Topics 1 and 20" → "from Topic 1". Cards: mem-trial-toolkit ("see Algebraic Understanding" → self-contained worst-luck row; "Topics 1 and 20" → "Topic 1"), mem-trial-error tip (same).
`python3 math_check.py 5 7 10 21 22 25 26 28 30 31 33 37 32` → PROBLEMS 0, WARNINGS 0, LAYOUT 0.
