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
