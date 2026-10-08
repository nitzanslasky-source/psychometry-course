# Topic 22 — General word problems and ratios: changes (course review 2026-09)

Patch: `math_patches/t22.py`. Check: `python3 math_check.py 22` gives 0 problems, 0 warnings and 0 layout problems.
Guided questions are renumbered automatically. Learn and try now has Q1–Q12, and Further guided examples has Q13–Q23.

## 1. Wrong or misleading statements fixed
- **Ratios, slide 3:** removed "don't worry about being tricked on the order — the exam avoids that wording".
  It now says: "Always match names to numbers in order. The exam does test this."
- **Ratios, slide 6:** removed the "give the plain x to the smaller one" tip. It did nothing on the 1.5 : 2 example.
  The tip now appears in *Give It to the Little Guy*, slide 2, with a letter example: "A is twice B → B = x, A = 2x".
  It is also removed from the Ratios memory card, which comes before that video, and added to the toolkit card.
- **Q17 (was Q14), method 2 (size estimate):** replaced "58 is double 29" with real bounds.
  She gave away at most ¼ of the tiles, so the start is at most 29 · 4/3 ≈ 38.7.
  She gave away at least ⅙, so the start is at least 29 · 6/5 = 34.8. Only 36 is in that range.
- **Q21 (was Q18), title slide:** "Last question of the set" is no longer true, so it now says "Question eighteen", which is renumbered automatically.

## 2. Methods added
| Method | Where it is taught | Guided question (solution video) | Practice |
|---|---|---|---|
| Inverse proportion (workers × days stays the same) | Equal Ratios: new slide "Inverse proportion" and a recap line | Q3: 6 workers, 10 days → 4 workers (answer 15) | q-r26-t22-08, -09 |
| Three-part ratios (make the shared letter equal) | Ratios: new slide "Three-part ratios" | Q8: choir 2:3 and 4:5, 30 tenors (answer 70) | q-r26-t22-06, -07, -19 |
| Changing a ratio (keep the unchanged part fixed) | Ratios: new slide "Changing a ratio" | Q9: club 5:4 → 10 boys leave → 5:6 (answer 54, two methods) | q-r26-t22-13, -18 (plus p31, p35) |
| "Or part of" → round up | Read, Organize, Calculate: new slide with the 50 people / 12 per van example | (existing Q5, company hire) | q-r26-t22-14, -15 |
| Letters in the choices → choose numbers | New video **Three Exam Tools** | Q22: pens and notebooks, $y(2x+3)$ | q-r26-t22-10, -11 (plus p08) |
| Assume all the same | Three Exam Tools | Q23: cars and motorcycles (answer 12, plus "assume the other kind") | q-r26-t22-12 (plus p21, p36) |
| One equation, two unknowns → only a multiple can be found | Three Exam Tools | (existing Q20 blocks) | q-r26-t22-16 (cannot be determined), -17 (= 75) |
| The shortcuts of the second section | New 1-minute video **Shortcuts Ahead**, before Q13: write the whole exercise first, plug in, size estimate, divisibility of the total, what changed?, scale everything, start from the end | — | — |

Other teaching changes:
- **Triangle value:** now also called "cross-multiply and divide", with an added sense check ("a bit more than 15").
  The Equal Ratios recap adds "One up, one down? Inverse" and "Before you calculate: bigger or smaller?".
- **Q19 (was Q16):** the video now starts with "What changed?", then two equations, then plugging in the answers.
- **Memory cards:**
  - *Ratios and equal ratios* gets new rows for inverse proportion, two ratios with one shared letter, and one part changing. Its new tips are "read in order", "bigger or smaller?" and "the total divides by the sum of the parts".
  - *Toolkit* gets new rows for choosing numbers, assuming all the same, and one equation with two unknowns. It also gets the little-guy and choose-numbers tips, and TeX in place of the plain "3:1", "A : B" and "8→10".

## 3. Text
- **":" for division is gone everywhere in the topic.** This covers the teacher draw notes ("8 × 15 ÷ 6", "144 ÷ 6", "112 ÷ 4", "20 ÷ 3", "÷4"), the Equal Ratios recap board ("then ÷ the rest"), and the solutions (p04, p10, p14, p15, p20, p28, p35 and Q13's "5:3.5", which is now $\frac{5}{3.5}$).
  Every real ratio stays as ":" and the text says "ratio". Draw notes such as "N : P = 5 : 3" now read "Write the ratio …".
  The ratio stems and choices are now in TeX: Q7, p16, p24, p31, p35.
- **p30 (ambiguous):** it now says each player gives tokens "just before leaving" to "every other player still in the room".
  It asks how many tokens the fifth player "has left after giving out his tokens, as he leaves". The key is 18, and $2n+8$ is now clearly the count before giving.
  The solution shows the numbers and checks $n=5$.
- **p09:** the confusing solution is rewritten: all four packs are listed in choice order, and choice (2) = 38 is the largest.
- **p03 / p14:** the solutions now finish with $540-132=408$ and $0.30+0.12=0.42$.
- **Q11 (was Q8):** the solution is now a table (now / 4 years ago) followed by the equation $2(x-4)=x+2$.
- **p17:** the stem now says "sells $x$ meters of silk (as many meters as the price of one meter)", and the two conditions are stacked in the solution.
- Every solution (all 18 old guided and all practice questions) is rewritten in TeX with the numbers shown.
  No "so" meaning "therefore" is left in the middle of a sentence, and British spellings are gone.
- **Q10 stem:** ", so each of the 5 remaining rooms" is split into two sentences.
- **p23:** the times are now "9 a.m." / "4 p.m." in place of "09:00", which read like a ratio.
- **p05:** "neighbour" → "neighbor", the question now reads "Which of the following could be…", and the solution checks $n=12$.
- **Videos:**
  - "Read, Organise, Calculate" → "Organize".
  - colour → color and practise → practice.
  - Mid-sentence ", so …" / "— so …" in spoken lines → ". So, …".
  - The math minus inside words on the Q5 slide ("5−minute") is now a hyphen.
  - The solution-video titles are refreshed from the current stems ("centre" → "center").

## 4. Figures
- None in this topic.

## 5. Practice
- **Removed near-duplicates:** p22 (same as Q15, apprentices), p25 (same as Q21, counters) and p28 (same as Q17, tiles).
- **Added 14 practice questions** (q-r26-t22-06 … -19). Exam-hard ones: -07, -09, -11, -15, -18, -19, together with the existing p18, p24, p26, p27 and p30.
- **Practice now has 48 questions** (was 37), ordered easy → hard.
  It starts with p03, p04, p08 and p12. It ends with the hard group -07, -09, -11, -15, -18, p26, p24, p27, p18 and p30.

## Counts
- Questions rewritten: 52 (all 18 old guided and 34 practice). Added: 5 guided and 14 practice. Removed: 3.
- Slides added: 5 in existing videos (Inverse proportion, Or part of, Three-part ratios, Changing a ratio, plus the little-guy lines).
  Slides changed: about 12 (recaps, Q14 method 2, Q16 reordering and more).
- Videos added: 2 lessons (Shortcuts Ahead, Three Exam Tools) and 5 solution videos.

## For the teacher to decide
- *Give It to the Little Guy*, slide 5, still says "50 shekels", while the rest of the course uses "credits". I left it unchanged.
- I kept p21 and p36 (assume all the same) and p31 and p35 (changing a ratio) next to the new questions of the same type.
  If practice feels long, these are the first to cut.
- The review asks to put "What must the total divide by?" as the first line of every ratio question. I added it only as a card tip and a Ratios recap line. I did not edit every video.

## Pass 2 (teacher-approved remove/restore plan + summary lesson)
**Removed:** nothing (the plan keeps all the additions).

**Restored (3):** the original practice questions pass 1 had removed as near-duplicates are back, with text clean-up only:
- **wp22-p22** (visitors are 5/6 of the residents → visitors are 5/11 of everyone). The solution now plugs in 6 residents and 5 visitors. Placed after p10.
- **wp22-p25** (Iris and Owen, 30 counters, 9 are passed → 11 : 4). The choices are in TeX ratio form, and the solution shows every step: 13 and 17 after, 22 and 8 before, 22 : 8 = 11 : 4. Placed after q-r26-t22-13.
- **wp22-p28** (bead piles, 1/4 and 1/6 used, 18 and 25 left → 54). The "18:3×4" division colons are gone: (3/4)F = 18 → F = 24, (5/6)G = 25 → G = 30, 24 + 30 = 54. Placed after p26.

**New: summary video `r26-t22-summary` "Summary: Word Problems and Ratios"** (about 3.9 min), at the end of "Further guided examples" (after the advanced memory card), right before the practice. Slides: Summary · Three stages · Words to math · Equal ratios · Inverse proportion · Ratios: use x · The part that stays · Build the equation · Ranges and rounding · Exam shortcuts · Before you practice (checks: what exactly did they ask, bigger or smaller and direct or inverse, which part stays the same, the ×2 goes on the smaller side, can it really be found or only a multiple; traps: a ratio read in the wrong order, using the ratio table for workers and days, and giving the number of units instead of the number of people).

## 2026-10-01 elite comparison
Target: real exam 2024_spring_q2_03 and 2020_spring_q2_07 (the wrong choices use "the gap changes by k" and miss that the gap can turn around).
- **Lesson "Build the Equation" (wp-037): new slide "Giving: the gap changes twice"** after "Before and after". Table Dan 30 / Noa 20: gives 3 → gap 4; gives 5 → equal; gives 7 → Noa ahead by 4. Rules on the board: "A gives k to B → the gap changes by 2k" and "To make them equal: give half the gap". Recap has a new line "Gives k → the gap changes by 2k". Sidebar updated.
- **New guided question q-r26-t22-20** (right after the rooms question), with a solution video: shelf A has 26 more books than shelf B; after moving some books B has 6 more. Answer 16 (choice 3): the gap changes by 26 + 6 = 32, and 32 ÷ 2 = 16. Traps: 32 (gap changes by k), 13 (only equal), 10 (forgets the turn). Video: Method 1 · The gap, Method 2 · Before and after (x cancels: 2k − 26 = 6).
- **wp22-p25** (already back in the practice, Pass 2): the written solution now starts with the gap method (giving 9 moves the gap by 18; Iris was 18 − 4 = 14 ahead → 22 and 8 → 11 : 4). The equation method stays after it. Key unchanged.
- Not added: no change to the memory card or the summary lesson (not part of this request).

## 2026-10-05 cut repeats
Function `cut_repeats` (runs last). Each lesson is back to a short intro like the Hebrew course. Every idea that a question video right after it teaches is cut from the lesson; ideas no question teaches stay, or move as one spoken line (+ board item) into the question video that uses them. Nothing in topic 22 is recorded. Questions, numbers, methods and memory cards are unchanged.
- **`wp-028` Equal Ratios**: 6 → 1 slide, 3.7 → 0.3 min. Kept the title slide (the Hebrew intro: very important, follows you everywhere); its last line is now "The easiest way to learn it: on the questions." Cut: "The ratio table" (same 6 / 42 / 15 numbers as Q1) → Q1 trays; "Triangle value" + "Cross-multiply" → Q2 exercises; "Inverse proportion" → Q3 workers; Recap. In Q1 `solve-wp22-g029`: "straight from the lesson" → "we learn it on this question"; ADDED "Put the data in a ratio table: trays in one column, biscuits in the other. Six is to forty-two as fifteen is to the missing number."; the triangle-value line now says how (multiply along the diagonal, divide by what's left). Q2 `solve-wp22-g030`: "So: triangle value." → "So: the triangle value — also called "cross-multiply and divide"." Q3 `solve-q-r26-t22-02` method 2: ADDED "The rule: one goes up, the other goes down — the product stays the same. Workers and days, speed and time." + board "One up, one down? The product stays the same".
- **`wp-031` Read, Organize, Calculate**: 5 → 2 slides, 1.8 → 0.5 min. Kept title + "Reading, not algebra" (the Hebrew intro) + "Two questions next. They check that you notice every detail." Cut: "Label every cost" → Q4 tart (selling price minus cost, 38 is the cost trap); MOVED into Q4 `solve-wp22-g032`: "Label every number: a price per hundred grams is not a price per gram, and a fixed fee is paid once." + board. "Or part of: round up" → Q5 hire; MOVED the vans example into Q5 `solve-wp22-g033`: "Same with people: fifty people, vans of twelve. Four vans and two people left — they need a fifth van." + board "50 people, vans of 12 → 5 vans (round UP)". Recap cut.
- **`wp-034` Ratios**: 11 → 7 slides, 5.5 → 3.2 min. Kept slides 1–7 (they are the Hebrew ratio lesson: what a ratio tells you, a fraction, no amounts, part of a whole, fractions in a ratio, reversed "costs as" — no question after it teaches "costs as"). Cut: "Units and divisibility" → Q6 (difference 2x → even; boys ÷ 3, girls ÷ 5, class ÷ 8); "Three-part ratios" → Q8 choir (same method and the 2 : 3 : 5 trap); "Changing a ratio" → Q9 club (keep the unchanged part, two methods); Recap. Slide 7 now ends "Four questions next. Watch the ratio units do all the work."
- **`wp-037` Build the Equation**: 6 → 2 slides, 2.4 → 0.5 min. Kept title + "Equations everywhere" (the Hebrew intro) + "Let's see it in the questions." Cut: "Choose x wisely" → Q10 rooms (x = what they ask; 18 is the trap). "Before and after" → Q10 + Q11's table; MOVED into Q10 `solve-wp22-g038`: "Moved between groups? The total stays. Removed? It drops. Added from outside? It grows." + board. "Giving: the gap changes twice" (elite addition) → Q11 shelves teaches it fully (each book changes the gap by two, the gap turns around); MOVED "give half the gap" into Q11 `solve-q-r26-t22-20` method 2: "To make them equal, you give half the gap: thirteen. Here B must end up ahead, so we need more." + board "Equal? Give half the gap". Recap cut.
- **`wp-039` Give It to the Little Guy**: 6 → 1 slide, 2.5 → 0.3 min. Kept the title slide (the Hebrew course teaches this inside the age question) + "Let's see it in two questions: an age question and a budget question." Cut: "Equal sides" → Q12 ages ("think of four and eight — you double the four"); MOVED into Q12 `solve-wp22-g039`: "Lots of students double the bigger one. That's backwards: the times two goes on the smaller side." + board "Twice? The ×2 goes on the smaller side". "Ages: gaps stay" → Q12 row for each time; MOVED "Notice: the gap is still six. Everyone ages the same — the gap stays, only the ratio changes." "Test the answers" → Q12 and Q13 method 2. "Enough, not enough" → Q13 notebooks (same inequalities). Recap cut.
- **`r26-t22-shortcuts` Shortcuts Ahead**: 3 → 1 slide, 1.1 → 0.2 min. Only the title slide, with the Hebrew advanced intro: "Advanced questions: no single formula here. We build an equation, or we understand and calculate — and each question shows a shortcut. Try each one first — then watch." The seven shortcut previews are each taught in their question: write it all first → Q15, plug in → Q16/Q17, size estimate → Q14/Q17/Q18, total divides by both → Q19, what changed → Q20, scale → Q21, start from the end → Q22.
- **`r26-t22-exam-tools` Three Exam Tools**: 5 → 2 slides, 2.4 → 1.0 min. Kept title (reworded: the first tool here, the other two in the questions) + "One equation, two unknowns" (no question after it teaches it) + "Two questions next." Cut: "Letters in the choices" → Q23 pens (choose numbers, not 0 or 1, test every choice); MOVED the tie-break into Q23 `solve-q-r26-t22-04`: "Two choices give the same result? Choose new numbers and test only those two." + board. "Assume all the same" → Q24 parking lot (both ways). Recap cut.
- Unchanged: `wp-027` From Words to Equations (the Hebrew course also has a long theory lesson here), the summary lesson, all memory cards.
- Question videos lengthened: g029 0.7→0.9, Q3 0.8→0.9, g032 0.8→0.9, g033 0.7→0.8, g038 0.8→0.9, Q11 1.1→1.3, g039 1.6→1.8, Q23 1.0→1.1. **Net: −12.3 min.**
- The only "lesson" reference to a cut idea (Q1 "straight from the lesson") is reworded. AI summary `r26-t22-summary` not edited; everything it recaps is still taught (in the kept slides or the question videos).
- **Follow-up (same day): no idea lost, no title-only lesson.** Went through every cut idea again; each now names its question video. Restored, as one line in the question that uses it:
  - "The three numbers make a triangle — hence the name." → Q1 `solve-wp22-g029` slide 3.
  - "Triangle value or cross-multiplying — pick whichever feels natural. The triangle value writes the answer straight away, without isolating x." → Q2 `solve-wp22-g030` method 2.
  - "people and the days a food supply lasts" added to the inverse rule in Q3 `solve-q-r26-t22-02`.
  - "Give the plain x to the little guy: B is x, A is three x. No fractions, no dividing later." (from "Equal sides", A is twice B → B = x) → Q19 `solve-wp22-g047`, replacing its plain "B is x, A is three x." (the board already shows B = x, A = 3x).
  - Kept out on purpose (examples only, the method is taught): the 64 − 37 profit example (Q4 does the same), "a class of 20 is impossible with 2 : 5" (Q6), "the table is your pause button", "same idea as n = 3 in sequences" (a cross-reference).
- **Short intros instead of title-only lessons** (Hebrew style, title + one concept slide with one board item, about 20 seconds):
  - `wp-028` Equal Ratios (0.4 min): title "Equal ratios. A short lesson — and one of the most important in the whole course." + slide "Same rate, two cases": follows you everywhere; board "Same rate in both cases → equal ratios"; "The easiest way to learn it: on an example." (Hebrew B32.)
  - `wp-039` Give It to the Little Guy (0.4 min): title (sounds funny, saves points) + slide "Where it helps": board "Building an equation: twice · three times · ages"; "Let's see it in two questions: an age question and a budget question." (Hebrew B43: a technique for building equations.)
  - `r26-t22-shortcuts` Shortcuts Ahead (0.3 min): title "Advanced questions: general problems." + slide "No formula here": "Not motion, not percents, not work — no formula to guide you."; board "Build an equation · or understand and calculate"; each question shows a shortcut — try it first. (Hebrew B45.) Q14 `solve-wp22-g042` lost its now-duplicate opening line "Advanced general problems. No single formula here…".
  - `r26-t22-exam-tools`: removed the slide-2 line "Last tool: knowing when you CAN'T find the answer." (the title already says it, and it is now the only tool in the lesson).
- After the follow-up: **net −11.6 min** for topic 22 (was −12.3).

## 2026-10-06 practice: new methods
Function `practice_methods` (runs last in `apply`). One extra line is added at the end of each written solution; the existing lines are kept. The flip rule, arrow map and other new methods are taught in topic 23 and later, so they are not used here. Pick values that fit (topic 51 Case 4) comes later, so it is written as a self-contained "Shortcut" with its one-line reason. Nothing is recorded.
- `q-r26-t22-17` (4n + 6p = 50 → 6n + 9p): Shortcut · Pick values that fit: p = 0 → n = 12.5 → 6 · 12.5 = 75.
- `wp22-p29` (brushes, cannot be determined): Pick values that fit: B = 24 and B = 48 both fit → not fixed.
- `wp22-p18` (2 × 2 grid, rows and columns equal): Pick values that fit: a = 1, b = 2, c = 2, d = 1 rules out choices 1–3.
- Every line checked in python. Check: `math_check.py 22 32` → 0 / 0 / 0.

## 2026-10-06 renumber pass
So the English course does not look like the Hebrew one: every Hebrew-derived question and lesson example has new numbers,
and every word problem a new story (names, objects, setting — everyday things only). The structure, the kind of condition,
the trap, the level and the methods stay the same; every guided solution video is rewritten to match (speech, draw cues,
board tables/bar, video title, slide description). Nothing in Topic 22 is recorded, so nothing had to be kept.
Function `renumber_pass(M)` in t22.py runs last (after `practice_methods`). New numbers were also checked against the
Hebrew subtitles (02-Word-Problems-Original-Subtitles.txt) so that they do not fall back onto the Hebrew numbers or objects
(e.g. 2.5 apples / 6 plums, 128 cadets, 410 shekels, motorcycle : car, "3 years ago" were all avoided).

**Counts:** 18 guided questions renumbered + 18 solution videos rewritten; 30 Hebrew practice questions renumbered;
lessons: "From Words to Equations" (7 slides) and "Ratios" (6 slides) renumbered; cards updated: Words → maths (all 10 rows),
Ratios (5 example cells), General problems toolkit (7 cells). Practice: 51 → 37.
Kept on purpose: the English-made guided questions (q-r26-t22-01 … -05, -20), the summary and "Three Exam Tools" lessons,
the 3 kept extra-bank items and the 4 kept September items keep their numbers (not Hebrew-derived).

**Practice clean-up (51 → 37):**
- Copy removed: q-r26-t22-17 (same story and structure as q-r26-t22-16).
- Extra warm-ups kept (3): p34 (ages, "3 times then twice"), p35 (blend: the unchanged part), p37 (4 adult = 7 child tickets).
  Removed p31, p32, p33, p36 (types covered by p35 / p06 / p13 / p21).
- September items kept (4, types the Hebrew practice lacks): -06 (two ratios, shared letter), -08 (inverse proportion),
  -15 ("or part of" → round up), -16 (one equation, two unknowns: cannot be determined).
  Removed -07, -09, -10, -11, -12, -13, -14, -18, -19 (each type already practised — see comments in `rn_practice`).
- 37 instead of the audit's ~36 so that "cannot be determined (not a multiple)" keeps one practice item.
- Practice re-ordered easy → hard.

**Checks:** every key computed in Python (exactly one correct choice; for range / divisibility / estimate questions every
wrong choice falls outside); every step and plug-in in the videos recomputed; the traps are still choices (cost instead of
profit, new number per row, Tom 5 years ago, both quarters from the start, compares with one group only, units, inverted
ratio …). Duplicate scan over topics 1–22 (stems, lesson boards/draw cues, cards): only incidental number overlaps.
No quadratic trinomial added. `python3 math_check.py 22 32` → 0 / 0 / 0. Rendered all changed videos and looked at them.

| id | old | new | answer |
|---|---|---|---|
| wp22-g029 (Q1) | 6 trays 42 biscuits, 15 trays | 8 vases 56 roses, 12 vases | 84 (3) |
| wp22-g030 (Q2) | 12 exercises / 8 min, 14 min | cook: 18 potatoes / 12 min, 20 min | 30 (1); sense < 36 |
| wp22-g032 (Q4) | tart 58: pastry, filling, berries | sandwich 47: bread 4/100 g, cheese 8/100 g, 6 olives × ½ | 12 (3); trap 35 = cost |
| wp22-g033 (Q5) | 3/min vs 14 per 5 min, 11.5 min | bikes: 4/hour vs 17 per 4 h, 9.5 h | 11 (4) |
| wp22-g035 (Q6) | boys 3/8 of class, difference | swimmers 5/12 of camp, runners − swimmers | 22 (2); 2x even |
| wp22-g036 (Q7) | scooter : car 3 : 8, +15,000, sum | sofa : piano 3 : 10, +14,000, sum | 26,000 (2) |
| wp22-g038 (Q10) | 6 rooms → 5, +3 | 8 rows of chairs → 7, +3 | 21 (2); trap 24 |
| wp22-g039 (Q12) | Iris 6 older, 4 yrs ago twice | Maya 9 older, 5 yrs ago twice | Tom 14 (3); trap 9 |
| wp22-g040 (Q13) | 84: 5 notebooks not 6 | Dana 105: 6 tickets not 7 | 17 (2); 15 = exactly 7 |
| wp22-g042 (Q14) | 2 oranges / 3.5 pears / 8 plums | 4 kiwis / 1.5 pineapples / 5 limes; 8, 2, 5 | 13/3 (1); 4 < total < 5 |
| wp22-g043 (Q15) | 144, 5/6 per round, 2 rounds | video game 160, 3/4 per level | 90 (3); trap 80 |
| wp22-g044 (Q16) | 3/5 as many apprentices | 5/8 as many coaches as trainees | 5/13 (4); trap 5/8 |
| wp22-g045 (Q17) | 4×, 1/4 and 1/3 rejected | bakery 2×, 1/2 and 1/5 whole-wheat | 2/5 (1); between 1/5 and 1/2 |
| wp22-g046 (Q18) | 1/4, 1/6 given; 9 and 20 left | cupcakes 1/3, 1/6 sold; 10 and 14 left | 33 (4); 28.8 ≤ start ≤ 36 |
| wp22-g047 (Q19) | clubs 3 : 1, 3 move, then 2 : 1 | buses 4 : 1, 6 move, then 2 : 1 | 45 (2); ÷5 and ÷3 |
| wp22-g048 (Q20) | 10 tasks 320, 6 tasks 208 | plumber 7 h 385, 4 h 250 | 45 (2); fee 70 |
| wp22-g049 (Q21) | 8 + 12 blocks = 1,000 g → 10 + 15 | 9 + 6 crates = 240 kg → 12 + 8 | 320 (2); × 4/3 |
| wp22-g050 (Q22) | 60 counters, 9 given, equal | Noa & Eli 70 stickers, 15 given | 5/2 (3); trap 2/5 |
| wp22-p03 | drone 540 km, 80 g, 4 km/g, 113 g | cargo boat 900 km, 50 t, 6 km/t, 87 t | 678 (2) |
| wp22-p04 | teams 3, 4, 5 split 660 | families 2, 5, 6 split 780 | 300 (2) |
| wp22-p08 | x trays × x pots × 2 | n cabinets × n drawers × 3 folders | 3n² (4) |
| wp22-p12 | crest = 8 sparks = 2/5 crown | gold = 6 silver = 3/4 platinum | 8 (1) |
| wp22-p07 | donates 1/4, spends 180, 720 left | saves 2/5, jacket 150, 450 left | 1,000 (3) |
| wp22-p14 | cocoa 120/18, sugar 300/12, 2 + 3 | syrup 50/15, coffee 400/24, 2 + 3 | 0.78 (4) |
| wp22-p06 | book +18, 4 books = 6 notebooks | large pizza +12, 3 large = 5 small | 30 (3) |
| wp22-p02 | 3× and 2× → 9x | roses 4× tulips, tulips 3× lilies → 16x | 48 (3) |
| wp22-p10 | 5 pads = 2 folders + 6 pencils | 4 coats = 3 jackets + 8 scarves, jacket = 4 scarves, 12 coats | 15 (4) |
| wp22-p22 | 5/6 as many visitors | concert 7/8 as many adults as children | 7/15 (2) |
| wp22-p16 | dogs 6 apart, 4 : 1, +2 yrs | father 30 older, 6 : 1, +9 yrs | 3 : 1 (3) |
| wp22-p25 | 30 counters, gives 9, 4 fewer | Gal & Ron 40 marbles, gives 7, 6 fewer | 3 : 2 (3) |
| wp22-p15 | 6 days × 25 berries, 18 days × 5 | squirrel 8 days × 30 nuts, 16 days × 5 | 20 (2) |
| wp22-p20 | 48,000/40 vs 3,000/15 | 72,000/60 vs 3,000/20 | 8 (3) |
| wp22-p21 | 42 stools/carts, 146 | 45 stools/chairs, 158 legs | 23 (2) |
| wp22-p19 | 1/4 given each of 3 months | tank loses 1/5 each of 3 days | 64/125 (3) |
| wp22-p13 | 2/5 then 1/3 of rest, 360 | melons 1/4 then 2/3 of rest, 480 | 640 (2) |
| wp22-p01 | (x² + 32)/x = 3x | bottles (x² + 45)/x = 6x | 3 (2) |
| wp22-p05 | eats 4, half, 3 → even | cookies: eats 5, half, packs 4 → odd | 15 (3) |
| wp22-p09 | battery 5/4: 4L4S, 6L2S, 7L, 9S | jug 4/3: 5L3S, 7L, 4L5S, 10S | 4L5S (3) |
| wp22-p11 | ÷8, −3, ×6, +18 | ÷6, −5, ×4, +20 | 0 (1) |
| wp22-p23 | 9 a.m., 5 days, 3 one-hour breaks, 32 h | 7 a.m., 4 days, 2 half-hour breaks, 31 h | 3 p.m. (3) |
| wp22-p17 | silk/cotton: sum 17, diff 5 | coffee/tea: sum 20, diff 4 | 80 (2) |
| wp22-p29 | brushes, 8 and 24 artists, 3× | tablets, 6 and 30 classes, 5× | cannot be determined (2) |
| wp22-p26 | 2/5 on rice, 3/4 repaid, 8.40 | 3/8 on flour, 2/3 repaid, 7.50 | 10 (3) |
| wp22-p28 | beads 1/4, 1/6; 18 and 25 | pencils 1/5, 1/4; 16 and 21 | 48 (3) |
| wp22-p24 | kites 3/8 and 1/4, 9× | candles' stripes 2/5 and 1/3, 6× | 5 : 1 (2) |
| wp22-p27 | ×3/5 + 24, score goes down | ×3/4 + 20, grade goes down | greater than 80 (2) |
| wp22-p18 | a, b / c, d | p, q / r, s (choices reordered) | p = s and q = r (1) |
| wp22-p30 | n ≥ 5, 2n tokens, gives 2, 5th player | n ≥ 4, 3n stickers, gives 3, 4th child | 21 (3) |
| wp-027 lesson | ×4 + 18 = 6x; 6 more, 9 less, 3 times, 2/5, ¼ less, diff 12, 2/3, 3N = 5P, 2 : 3 | ×3 + 24 = 7x; 7 more, 4 less, 5 times, 3/5, ⅓ less, diff 15, 3/4, 2N = 5P, 3 : 7 | — |
| wp-034 lesson | 3 : 5, 12 : 20, 3/8 of all, 1.5 : 2, 3N = 5P | 3 : 7, 12 : 28, 3/10 of all, 2.5 : 3, 2N = 5P | — |

## 2026-10-06 review (renumber pass)
Independent review of the renumber pass (build with / without `renumber_pass`, every guided + practice item side by side,
keys recomputed, videos checked against the Hebrew subtitles). All 18 guided, 30 practice and both lessons: keys correct,
one correct choice each, traps kept, same type / condition / steps, methods work with the new numbers.
- Fixed: lesson example "2 notebooks cost the same as 5 pens" (wp-027 #8, wp-034 #7, cards mem-word-phrases / mem-ratios)
  echoed the Hebrew lesson's "for every 2 pens, 5 pencils" → now "2 notebooks cost the same as 7 pens: 2N = 7P → N : P = 7 : 2"
  (pick 14: notebook 7, pen 2).

## 2026-10-07 methods spread
Function `spread_methods(M)` in t22.py runs last (after `renumber_pass`). Written lines only (no guided video gets a slide: the methods that fit the guided questions are taught in later topics). Methods from later topics are written as a self-contained "Shortcut · <name>" line with its one-line reason. Every line was checked with numbers. Nothing in topic 22 is recorded.
- **Power count** (topic 5): wp22-p08 (cabinets, drawers, folders) — power 2; $n^3$, $3n$, $n^2+3$ are out → $3n^2$.
- **Two moves** (topic 12): wp22-p27 (grade goes down) — endpoint $x=80$, test $x=0$ fails → $x>80$.
- **Shortcut · Percent shares as weights** (topic 25): wp22-g045 (whole-wheat loaves, guided Q17) — $\frac15+\frac23\cdot\frac3{10}=\frac25$.
- **Shortcut · Flip rule** (topic 23): wp22-p24 (candle stripes) — $\frac25L=2S$ → $L:S=2:\frac25=5:1$.
- **Shortcut · Compare by factors** (topic 26): wp22-p20 (words per picture) — words $\times24$, pictures $\times3$ → $24\div3=8$.
- Not added (checked): q-r26-t22-02 / -08 (worker-days already flips), g049 (already "both counts × 4/3"), p37 (the substitution is faster than the flip), q-r26-t22-04 (power count cuts only choice 1), q-r26-t22-16 / p29 / p18 (pick values that fit is already shown).


## 2026-10-07 study-plan order
Function `plan_order_fix` (runs LAST). Students follow the study plan (`src/lib/planData.ts` ORDER), not topic numbers; named methods were checked against the plan rank of their teaching topic.
- wp22-p08: "Method 2 · Power count" → self-contained shortcut (topic 22, day 12, before topic 5, day 13). wp22-p27: "Method 2 · Two moves" → self-contained "Shortcut · Two moves" (topic 12 is day 20).
- wp22-p18, wp22-p29: "Shortcut · Pick values that fit" → "Method 2 · Pick values that fit" (topic 51 is day 6).
`python3 math_check.py 5 7 10 21 22 25 26 28 30 31 33 37 32` → PROBLEMS 0, WARNINGS 0, LAYOUT 0.

## 2026-10-08 Hebrew points restored
Function `hebrew_points_back` (runs LAST; helpers `_hebrew_back.py`; nothing in topic 22 is recorded). Every teaching point of the Hebrew lessons "יחסים זהים", "בעיות חישוב והבנה", "יחס מתמטי", "בניית משוואה או ביטוי", "תן למסכן" and the advanced intro "בעיות כלליות" was checked against the current course (about 40 points). All still taught except two, now restored:
- **`wp-037` Build the Equation, slide "Equations everywhere"** (+≈15 s, 0.8 min): board "Tip: let x be what they ask" + "A small tip: in most cases, let x be the thing they ask for. Not always — but most questions are built that way. Then when you find x, you have the answer." (the general tip was on the cut "Choose x wisely" slide; Q10 only applies it).
- **`solve-wp22-g030` Q2, slide "Cross-multiply"** (+≈11 s, 1.2 min): "Hasn't it sunk in yet? That's fine. We'll use it so often — in word problems, geometry and algebra — that it will." (the closing remark of the Hebrew equal-ratios lesson).
- Left out on purpose (for the teacher): the Hebrew ratio lesson says the exam almost never uses the "the ratio between A and B is 4:7" wording (so as not to confuse dyslexic students). Real English NITE exams do use it (e.g. "the ratio between the number of nurses and the number of head nurses is 3 : 2"), and the lesson says "the exam does test this". Not restored.
- `math_check.py 21 22 32`: PROBLEMS 0, WARNINGS 0, LAYOUT 0.
