# Topic 28 — Counting possibilities: changes

Patch: `math_patches/t28.py`. Check: `python3 math_check.py 28` shows 0 problems, 0 warnings and 0 layout problems (113 slides).

## Summary
- Questions: 41 rewritten, 27 added (9 guided with solution videos, 18 practice), 3 removed.
  The topic had 44 questions (17 guided, 27 practice). It now has 68 (26 guided, 42 practice).
- New lesson videos (2): "Roads, Zeros and "At Least One"" (7 slides) and "Together, Apart and Repeats" (7 slides).
- New solution videos (9): Questions 13 and 19–26 (the guided questions are renumbered automatically in course order;
  the old Q13–Q17 are now Q14–Q18).
- Lesson slides changed: 6 ("Add or Subtract Cases" 2, "Choosing a Group" 2, "Mutual Action" title slide, 1 wording fix in the first video); slides added: 2 ("Groups with no names", "The checklist" in "Choosing a Group").
- Solution videos changed: Q7, Q8 (÷ instead of ":"), Q10 (spelling), Q11 (cancelling), Q12 and Q17 (intro line), Q14 (whole slide 2), Q15 (spelling), Q17 (2 lines). All guided sidebars updated.
- Memory cards: both updated ("Counting possibilities" gets the 5-step checklist; "Advanced counting tools" gets a "More methods" table and moves to the end of its section).
- Figures: 1 new question figure (road map for Q19) and 1 slide figure (road map in the new video).

## 1. Wrong or misleading teaching (fixed)
- **Q14 video:** the teacher started with the free tens digit ("because nothing restricts it"). That contradicts the rule "most restricted position first". Now it starts with the hundreds digit, then the forced units digit, then the free tens digit.
- **Q17 video:** "Worried you missed one? Six is fewer than we've already found…" is replaced by "We found seven. Choice six is too few. Forty-two and seven hundred twenty would need many more rows — and there are no more." "Choose the one who stays in place" is now "who stays out".
- **One name:** the video "Two-Way Connections" is now "Mutual Action", the name the cards and the other videos use.
- **"Rare" removed:** "Add or Subtract Cases" no longer says "very rare … one question every few years"; the slide is now "Why learn it: less common, needed for probability". "Choosing a Group" no longer says "very hard, and very rare".
- **Q12 / Q17 intros:** "Last question of the set" is no longer true (new questions follow), so they now say the question number.

## 2. Methods added
In **"Choosing a Group"**:
- "Who stays out" is now a general rule: choose k of n = choose the n − k who stay out (8 of 10 = 2 of 10 = 45).
- New slide "Groups with no names": named → keep the count, no names → ÷ 2 (6 people into two groups of 3: 20 → 10).
- New slide "The checklist" (5 steps: order? repetition? restriction first / forced = 1? counted twice → ÷2 or ÷k!? cases (+) or all − forbidden?). Also the first table of the memory card.
- New guided **Q13** (6 friends into two unnamed groups of 3 = 10), 2 methods.

New video **"Roads, Zeros and "At Least One""** (advanced section, after Q18):
- Road maps: "and" along a path = ×, "or" between paths = + (drawn map, 3·2 + 2·4 = 14).
- The zero trap: even three-digit numbers from 0–5 without repeats, split by "units digit 0" / "2 or 4": 20 + 32 = 52 (trap: 60).
- At least one = all − none (three-digit codes with a repeated digit: 1000 − 720 = 280).
- Which is the base? 4 letters into 3 mailboxes = 3⁴, not 4³ ("each object chooses").
- Quick checks: test a formula on a small case; elimination by size (order matters → the bigger choice; group → divide).
- Guided **Q19** road map with figure (23), **Q20** four-digit even numbers from 0–4 (60, 2 methods), **Q21** codes with at least one 5 (3439, with the double-counting trap explained), **Q22** 5 letters into 3 mailboxes (243, with a small-case check).

New video **"Together, Apart and Repeats"**:
- Glue for "together" (×2 or ×k! inside), "not together" = all − together, gaps for "no two side by side", identical items (÷ factorial of each repeat), round table ((n − 1)!).
- Guided **Q23** 3 math books together (144), **Q24** two girls not side by side (72: gaps, and all − together), **Q25** BANANA (60), **Q26** round table with a glued pair (48, 2 methods).

These now teach the methods that practice already used without a lesson: p15 (gaps), p23 (glue), p25 (identical letters), p26 (round table).

## 3. Text
- Every guided and practice solution rewritten with the numbers in TeX (the old ones were mostly words: "four times six is twenty-four").
- No ":" for division left (p03, p12, p25, p27, and the draw notes of Q7 and Q8 now use ÷ or fractions).
- Mid-sentence "so" removed (Q14, Q15, Q16). British spellings fixed (colour, neighbour, organised).
- Missing spaces after commas fixed (p17–p20, p24, Q10).
- "three−digit" / "two−digit" with a minus sign: the slide notes of all solution videos are rebuilt from the stems.
- Reworded: Q3 (simpler code wording), Q15 (conditions one under the other, C × D in TeX), p06 and p16 (letters in TeX), p18 (clear "which two numbers came up"), p20 (clear "pairs of digits"), p21, p24, p25.
- Q11 video: the cancelling is now written as a fraction and done one step at a time (8 with 4·2, then 6 with 3).

## 4. Practice
- Removed: p04 and p07 (one-step n!, duplicates of Q6), p13 (worst-case key puzzle, not counting).
- Added 18 (q-r26-t28-10 … 27): road maps (2, one hard round trip = 96), zero-digit cases (2), at least one (3), objects into boxes (2), glue / not together (2), gaps (1), identical items (2, one with a zero), round table not together (1), unnamed groups/pairs (2), 8 of 10 (1).
- Order is now easy → hard (one-step first, then cases, complements and arrangements, then the puzzles p18, p20). About 20 items are exam-medium or exam-hard.

## For the teacher to decide
- The review asked to use the checklist "in every solution video". It is used in the new videos; the 12 old learn-section solution videos were not changed for this.
- The road-diagram slide is in the new video, not in "Multiply the Choices" (it needs "or = add", which comes later).
- p02 and p16 test exponents more than counting; kept as short factorial/power practice.
- The API has no way to shrink a slide table, so Q15's stem was shortened ("A and B on top, C and D below") to keep the Q15 video table clear of the answer choices.

## Pass 2 (2026-09-27): remove/restore plan + summary lesson
Check: `python3 math_check.py 18 27 28 33` shows 0 problems, 0 warnings and 0 layout problems.

**Removed (plan):**
- "Choosing a Group" (wp-137): the slide "Groups with no names", its sidebar entry and its recap line. The recap says the original "Two questions next — one of each." again.
- `r26-t28-cases`: the slides "Road maps" (with its figure) and "The zero trap", their recap lines and sidebar entries. The video is renamed **"Boxes and 'At Least One'"**. The title slide and the recap ("Two questions next — one of each.") were updated.
- Guided q-r26-t28-01 (groups with no names), -02 (road map, with its figure) and -03 (zero among the digits), with their solution videos. The guided questions were renumbered: learn 1–12, advanced 13–23. The original line "Last question of the set." in the Q12 video is back, because Q12 is again the last question of the section.
- Practice q-r26-t28-10, -11, -12, -13, -24 and -25.
- Card `mem-counting`: the row "Groups with no names". Card `mem-counting-advanced`: the rows "Road map" and "A zero among the digits", and the two tips about the direct road and digits with a zero.

**Kept (plan):** "Which is the base?" slide, guided q-r26-t28-05 (mailboxes), practice -16 and the card row "Objects into boxes".

**Restored:**
- Practice wp28-p04, wp28-p07 and wp28-p13 (original text, solutions in TeX with the numbers shown), in the practice order by difficulty.
- The true "rare" lines: wp-134 slide 2 "Rare and hard" (the original slide; its last line also says that probability uses this idea); wp-134 slide 4 "Subtracting possibilities is even rarer."; wp-137 slide 2 "…Very hard, and very rare."
- alg-extra-unit-t18-3-4 comes from T18 (the T18 patch moves it). It is first in the T28 practice order, the easiest question.

**Summary lesson added:** `r26-t28-summary` "Summary" (about 2.2 minutes). It is at the end of "Further guided examples", after the advanced card and right before the practice. Slides: Summary · Stages: multiply · Repetition and rows · Counted twice? · Who stays out · Cases · Objects into boxes · Together and apart · Before you practice (the 5 checklist questions; traps: adding instead of multiplying, dividing without a reason, a zero that leads a number).

## 2026-10-01 elite comparison

Teacher-approved addition: **factorials as algebra**, in the lesson "Factorial Expressions". Targets the 12 real-exam factorial questions found (2020 winter I-19, 2022 autumn I-17, 2020 autumn I-4, 2024 winter II-17, 2019 winter II-16, 2021 autumn II-5, 2021 spring I-5, 2022 winter II-7, 2025 winter I-7, 2025 spring I-14, 2026 spring II-18, 2025 autumn I-17 — the last is solved by the existing "plug in a small legal value").

- Video "Factorial Expressions": four new slides before the recap:
  - **Know them by sight**: 3! … 7! (120, 720, 5040); example a! = 6 · 20 = 120 → a = 5.
  - **A run of neighbors**: b!/a! = (a + 1)…b; backwards: b! = 56 · a! → 56 = 7 · 8 → a = 6, b = 8; n!/(n − 1)! = n, n!/(n − 2)! = n(n − 1).
  - **Sums of factorials**: take out the smaller one: 5! + 6! = 5! · 7, 6! + 8! = 6! · 57, 8! − 7! = 7 · 7!; never subtract inside the "!".
  - **Factorials and primes**: 7! = 2⁴ · 3² · 5 · 7; divisible by 16 yes, by 32 / 25 no; count the 2s, not the even numbers.
  - Recap rewritten with the new lines; sidebar updated. The video is now about 4.6 minutes (was 2.1).
- Advanced memory card: four new rows (Know by sight, Run of neighbors, Sum of factorials, Primes in n!).
- New guided question **q-r26-t28-28** (right after the lesson, before wp28-g141) with solution video: (10! − 9!)/8! = 81, choice 2 (Method 1 take out 9!, Method 2 everything in 8!).
- New practice (after wp28-p02): **q-r26-t28-31** (720 + 5040)/6! = 8, choice 2; **q-r26-t28-29** x!/y! = 110 → x + y could be 20, choice 2; **q-r26-t28-30** largest k with 2ᵏ dividing 9! = 7, choice 3.
- Summary video: new slide "Factorial algebra" after "Repetition and rows"; sidebar updated.
- All four questions solved by computer: exactly one correct choice each.

## 2026-10-05 cut repeats
Function `cut_repeats` (runs last). Each lesson is back to a short intro like the Hebrew course; every idea that a question video right after it teaches is cut from the lesson; ideas no question teaches stay, or move as one spoken line (+ board item) into the question video that uses them. Nothing in topic 28 is recorded. Questions, numbers, methods and memory cards are unchanged. Lessons not flagged by the audit ("Add or Subtract Cases", "Choosing a Group") are unchanged.
- **`wp-123` Counting Possibilities**: 5 → 3 slides, 1.8 → 1.4 min. Kept: title, "Different results" (row / committee / code — no question teaches it), "Type 1: list it" (the Hebrew intro). Cut: "What is counting?" (repeated the title slide), Recap.
- **`wp-124-after` Multiply the Choices**: 6 → 1 slide, 2.1 → 0.4 min (the Hebrew course teaches this inside the meal question). Title slide + "A stage of choice is simply a moment where you have to pick something. Let's see it in two questions." Cut: Stages of choice, Why we multiply, Order doesn't matter → Q2 meal `solve-wp28-g125` (stages, 6 + 6 + 6 + 6, the grid "drinks first or fillings first", adding counts menu items); Dependent choices (× 1) → Q3 code `solve-wp28-g126`; Recap. Sidebar now empty.
- **`wp-127` With or Without Repetition**: 7 → 2 slides, 2.2 → 0.6 min. Kept: title + "The pool" (the Hebrew intro) + "Three questions next…". Cut: With repetition → Q4 `solve-wp28-g128`; Without repetition → Q5 `solve-wp28-g129`; A row: n! → Q6 `solve-wp28-g130`; Factorial; Recap. MOVED into Q4: "Same with numbers: a three-digit number may repeat digits — four four four counts." + board "444 is a three-digit number". MOVED into Q6: "The exclamation mark is called factorial: the number times every whole number below it, down to one." + board "n! = n·(n − 1)⋯2·1".
- **`wp-131` Mutual Action**: 6 → 1 slide, 2.0 → 0.3 min. Title slide (the Hebrew intro) + "Let's see it in two questions." Cut: Mutual action, Count then halve → Q7 islands `solve-wp28-g132`; Diagonals (four ways) → Q8 `solve-wp28-g133`; Recap. MOVED into Q7 (end of method 1): "Spot it on the exam: handshakes, two-way routes, games between two, diagonals." + board, and "But with roles — a president and a secretary — A-then-B and B-then-A really are different. Then don't halve." + board "Different roles? Don't halve". MOVED into Q8: "A diagonal joins two vertices that are not next to each other."
- **`wp-140-after` Factorial Expressions** (elite addition, mostly content no question teaches): 10 → 8 slides, 4.8 → 3.9 min. Cut only "Sums: take out the smaller" → the next question `solve-q-r26-t28-28` (10! − 9!: take out the smaller, never subtract inside the !), and Recap. MOVED into that question: "Same with a plus: five factorial plus six factorial is five factorial times one plus six. Don't forget the one." + board "5! + 6! = 5!·(1 + 6)". The 6! + 8! example stays on the advanced memory card. Last slide now ends "Next, a question with a minus sign: take out the smaller factorial."
- **`wp-141-after` Forced Digits**: 4 → 3 slides, 1.3 → 1.3 min. The two worked examples stay (no question teaches them). Recap cut; its line "Count each free choice once. Give every forced position a one." now ends slide 3.
- **`r26-t28-cases` Boxes and "At Least One"**: 5 → 2 slides, 2.2 → 0.9 min. Kept: title + "Quick checks" (the 210 vs 35 "order matters?" check is in no question). Cut: At least one → Q19 `solve-q-r26-t28-04`; Which is the base? → Q20 `solve-q-r26-t28-05` (same "who chooses?" and trap); Recap. MOVED into Q19: "Why? The opposite of 'at least once' is 'none' — and none is one easy count."
- **`r26-t28-arrange` Together, Apart and Repeats**: 7 → 1 slide, 2.7 → 0.2 min. Title slide + "Four questions — one for each." Cut: Together: glue → Q21 books; Not together and No two side by side → Q22 (both methods); Identical items → Q23 BANANA; Round table → Q24; Recap. MOVED into Q24 `solve-q-r26-t28-09`: "Why? Turning the whole table changes no one's neighbors. So n items around a table: n minus one, factorial." + board "n around a table: (n − 1)!".
- Question videos lengthened: g128 0.5→0.6, g130 0.6→0.7, g132 0.8→1.1, g133 1.0→1.1, q-04 1.0→1.1, q-09 0.8→1.0, q-28 0.8→1.0. **Net: −9.0 min.**
- No video said "as we saw in the lesson" about a cut idea. AI summary `r26-t28-summary` not edited; everything it recaps is still taught (kept lesson slides or the question videos).
- **Follow-up (same day).**
  - **The three lessons that were left with only a title slide now each have a short Hebrew-style intro**: a title slide with 1–2 framing lines, plus one concept slide with one board item. The new helper `_short_intro` does this.
  - `wp-124-after` "Multiply the Choices", 0.3 min:
    - Title: "In most counting questions on the exam we won't list and count. We use a faster technique: multiplying the possibilities."
    - Concept slide "Stages of choice": board "Count the options at each stage → multiply", then "A stage of choice is simply a moment where you have to pick something. Let's see how it works in two questions."
  - `wp-131` "Mutual Action", 0.4 min. This is the Hebrew B135 intro.
    - Title: "Mutual action: an action between two things at the same time — like a handshake. It's quite common on the exam, so understand it well."
    - Concept slide "Mutual action": board "A–B is the same link as B–A", then "When A shakes B's hand, B shakes A's hand. One handshake — and it's easy to count it twice. Let's see it in two questions."
  - `r26-t28-arrange` "Together, Apart and Repeats", 0.3 min:
    - Title: "Rows with a rule. Each rule changes how we count — and each one has its own trick."
    - Concept slide "Four rules": board "Together · apart · repeats · round table", then "People who must stand together — or apart. Items that repeat. And a round table. Four questions — one for each."
  - Each of the three sidebars now has one entry.
  - **Second check of the cut list**: every cut idea is taught in the question video named above. These small items are covered somewhere else:
    - The factorial examples 4! = 24, 5! = 120 and 100!: Q6 works out 6! step by step, and 5! = 120 is in "Factorial Expressions" → "Know them by sight".
    - "Three people together: glue three, × 3!": Q21 glues the 3 math books, × 3!.
    - "Every link counted from both ends": Q7 says "we counted every route twice".
    - The Counting Possibilities recap line "most questions won't need a full list": now the title line of "Multiply the Choices".
    - 6! + 8! (two steps apart): on the advanced memory card.
  - No idea was lost.
  - Net saving is now −8.9 min.

## 2026-10-06 new exam methods
Function `add_methods` (runs last). Nothing in topic 28 is recorded. Check: `python3 math_check.py 28 32` → 0 problems, 0 warnings, 0 layout problems.
- **Intro `wp-123` "Counting Possibilities"**: new slide 3 "At most? At least?" (sidebar entry added; 1.4 → 2.1 min): questions that say "at most / at least / necessarily / impossible" are the Topic 21 min/max method, not counting (about half of the real "counting" questions). Example: 8 friends, 30 candies, each at least 2 → others get 7 × 2 = 14 → one friend at most **16**.
- **Groups with no names** — card `mem-counting`, "Which rule?" table, new row after "A group, order does not matter": count as if the groups had names, then ÷ (number of groups)!; pairs: fix one person, choose her partner; 4 girls → 2 pairs = 6 ÷ 2! = 3 (not 6); 6 players → 3 pairs = 5·3·1 = 15.
- **New practice question `q-r26-t28-41`** (after wp28-p27, the "named teams" question): 8 runners into 4 unnamed pairs → 7·5·3·1 = **105** (choice 2); check 2,520 ÷ 4! = 105. Traps 2,520 (pairs treated as named), 420, 28.
- Note for the teacher: Pass 2 (2026-09-27) removed an earlier "Groups with no names" lesson slide, guided question and card row. Only the card row and one practice question are added back now, as requested — no slide, no guided question.

## 2026-10-06 practice: new methods
Function `practice_methods` (runs last in `apply`). One extra line is added at the end of each written solution; the existing lines are kept. Nothing is recorded. Few questions fit: almost all practice questions are true counting questions. `q-r26-t28-41` already teaches groups with no names.
- `wp28-p13` (at most how many key tests): "At most" → the Topic 21 min/max method, worst luck: 6 + 5 + 4 + 3 + 2 + 1 = 21.
- `wp28-p27` (named teams Cedar and Maple): Groups with no names? Here they have names → no division; unnamed would be 20 ÷ 2! = 10 (the trap choice).
- Every line checked in python. Check: `math_check.py 28 32` → 0 / 0 / 0.

## 2026-10-06 renumber pass
So the English Topic 28 does not look like the Hebrew course: every Hebrew-derived question has new numbers and a new
story (objects, names, setting); concept, trap, level, condition kind and methods stay. Every guided solution video is
rewritten to match (speech, draw cues, board items, grids / polygon / network / dice / tables, choice numbers, video
title, pre-loaded question). Function `renumber_pass(M)` in t28.py runs last (after `cut_repeats`, `add_methods`,
`practice_methods`; the "At most" method line that practice_methods added to p13 is rewritten with the new numbers).
Nothing in Topic 28 is recorded (`RN_RECORDED` is empty). New title-slide lines no longer say "Question N".
Checked against the Hebrew subtitles (02-Word-Problems): no new version lands on the Hebrew numbers or objects
(Hebrew: digits 1–4, salad 3 × drinks 5, employee number sum 10, digits 1–5 → 125 / 60, 5 books, 4 countries, hexagon,
cola/snack 16, dice ≠ 4, 6 children 3 + 3, 5 of 6, 6!/4!, sum 5 → 50, digits 1–4 square, 28 games, 6 students → 6).

**Counts:** 17 guided questions renumbered (all wp28-g…) with 17 solution videos rewritten; 20 practice questions
renumbered (wp28-p01 … p20); lesson examples renumbered in 4 lessons (Choosing a Group #2 and #4, Forced Digits #2 and #3,
Factorial Expressions #2 first line, Summary #2 and #3) + both memory cards. Practice 44 → 30.
English-made items keep their numbers (guided q-r26-t28-04 … 09 and 28, kept practice extras and September items).

**Order:** Learn: "11 of 12" (easy, was Q12) now comes before the hard group split (was Q11) — both are taught in the
lesson right before them. Advanced, after the Forced Digits lesson: games (medium+) → heights (medium+/hard) → the digit
square (hard, was Q16, now Q18). Correct-answer positions moved in all 17 guided questions.

**Practice clean-up (44 → 30; audit target ≈ 25 — the 5 above target are September items of types the Hebrew practice
does not have, kept by the rule):** all 20 Hebrew-derived kept (renumbered). Copies removed: p25 (LEVEL = guided BANANA),
alg-extra-unit-t18-3-4 (moved in by the T18 patch; removed only if present). Extra-bank kept (3): p23 together/glue,
p24 even numbers (most restricted first), p26 round table. Extra-bank removed: p21 (= guided Q9 method), p22 (= the
Quick-checks lesson "7 choose 3"), p27 (named teams 3 + 3 of 6 = the Hebrew lesson numbers; named/unnamed still practised
by q-41 and guided Q12). September kept (types the Hebrew practice lacks): q-14 at least one, q-16 objects into boxes,
q-19 not together, q-21 repeated items, q-29 run of neighbors, q-31 sum of factorials, q-41 unnamed pairs. September
removed: q-15, q-27 (at least one again), q-17 (pool stays full = p05), q-18 (together = p23), q-20 (gaps = p15),
q-22 (repeats = q-21; near-copy), q-23 (round table = p26; near-copy of guided Q24), q-26 (who stays out = p17),
q-30 (primes in n! = p02). Practice ordered easy → hard.

**Checks:** every answer brute-forced in Python by enumeration (permutations / combinations / products — script
t28_verify.py in the scratchpad): all 37 keys match, exactly one correct choice each, every "Choice N" / "Circle choice N"
in the videos matches the key, no spoken "Question N" in the rewritten videos. Every method in each video recomputed with
the new numbers (e.g. octagon: draw 20, 28 − 8, 7+…+1 − 8, 8·5/2; square: 2·2·2·1, trial table, 12 − 4; games: formula,
test 13 → 78 / 12 → 66 / 11 → 55, growing table to 66). Traps kept among the choices (add instead of multiply,
"5 options then 5 again" = 25, ÷6 = 84, the rule-both-ways 21, unordered 33, unnamed ÷2 = 126, start-with-0 = 90,
9², 9 + 7, 7!, …). Duplicate check over topics 1–28 (stems, lesson boards and spoken lines): no new question equals
another question or a lesson / card example. Each new question compared side by side with its original: same type, same
condition kind, same number of steps. p18 now uses ordinary 6-sided dice (was 8-sided). `python3 math_check.py 28 32` →
PROBLEMS 0, WARNINGS 0, LAYOUT 0. Rendered all 17 solution videos and the changed lessons and looked at them (the games
table is now horizontal, n = 2 … 12, so it fits above the choices).

| id | old (Hebrew-derived) | new | answer (choice) |
|---|---|---|---|
| wp28-g124 (Q1) | digits 2, 4, 6, 8 increasing | digits 3, 5, 6, 9 increasing | 4 (3) |
| wp28-g125 (Q2) | café 4 fillings × 6 drinks | food truck 7 soups × 3 breads | 21 (2) |
| wp28-g126 (Q3) | 2-digit code, digit sum 12 | locker number, digit sum 14 | 5 (3) |
| wp28-g128 (Q4) | symbols A–F, 3 positions, repeats | suitcase lock, digits 1–9, 3 wheels, repeats | 729 (2) |
| wp28-g129 (Q5) | same, no repeats → 120 | same lock, no repeats | 504 (4) |
| wp28-g130 (Q6) | 6 photographs in a row | 7 trophies in a glass cabinet | 5040 (2) |
| wp28-g132 (Q7) | 5 islands, ferry routes | 6 towns, bus lines | 15 (1) |
| wp28-g133 (Q8) | heptagon diagonals | octagon diagonals | 20 (2) |
| wp28-g135 (Q9) | 5 drinks, 4 snacks, cocoa → biscuit | 6 hot drinks, 5 pastries, espresso → croissant | 26 (3) |
| wp28-g136 (Q10) | red/blue dice, sum ≠ 5 | green/yellow dice, sum ≠ 8 | 31 (3) |
| wp28-g139 (Q11, was Q12) | committee 7 of 8 | team 11 of a squad of 12 | 12 (2) |
| wp28-g138 (Q12, was Q11) | 8 children, teachers Maya/Alex, 4 + 4 | 10 hikers, guides Lena/Omar, 5 + 5 | 252 (2) |
| wp28-g140 (Q13) | 7! / 5! | 9! / 7! | 72 (2) |
| wp28-g141 (Q15) | hundreds + units = 7 | hundreds + units = 8 | 80 (2) |
| wp28-g143 (Q16, was Q17) | chess, 45 games | table-tennis league, 66 matches | 12 (3) |
| wp28-g144 (Q17, was Q18) | 7 students, 6 tallest → shortest | 8 children, photographer, 7 shortest → tallest | 8 (3) |
| wp28-g142 (Q18, was Q16) | 3, 4, 7, 8; B even, C×D even | 2, 5, 6, 9; A even, C×D even | 8 (3) |
| wp28-p01 | 6 teams, all play once | 7 chess clubs | 21 (1) |
| wp28-p02 | 2!·3!·5! prime form | 3!·4!·5! | 2⁷·3³·5 (2) |
| wp28-p03 | 4 green + 3 red vegetables, salads of 2 | 5 white + 4 yellow flowers, bouquets of 2 | 16 (1) |
| wp28-p04 | 6-digit IDs from 1–6 | locker codes from A–E | 120 (2) |
| wp28-p05 | 5 symbols, 3 in order, repeats | 3 flags, 7 colors, repeats | 343 (3) |
| wp28-p06 | n performers, 120 orders | n dancers, 24 orders | 4 (2) |
| wp28-p07 | 4 prizes to 4 finalists | 6 awards to 6 volunteers | 720 (3) |
| wp28-p08 | hat/shirt/trousers, 4 colors, all different | cap/jersey/socks, 5 colors | 60 (3) |
| wp28-p09 | 1 of 5 symbols + 3 different digits of 1–7 | 1 of 4 letters + 3 different digits of 1–8 | 1344 (2) |
| wp28-p10 | 5 swimmers, podium | 6 cyclists, podium | 120 (3) |
| wp28-p11 | trousers 3, shirts 2, dresses 2, shoes 3 | lunch: 4 mains, 3 sides, 3 soups, 2 drinks | 30 (4) |
| wp28-p12 | 55 handshakes | 36 handshakes at a reunion | 9 (2) |
| wp28-p13 | 6 keys, 6 cupboards, at most | 7 keys, 7 gym lockers | 28 (3) |
| wp28-p14 | 4 actors left, 3 musicians right | 5 singers left, 3 drummers right | 720 (1) |
| wp28-p15 | 4 identical blue + 5 distinct red beads, gaps | 5 identical white + 6 colored beads | 720 (4) |
| wp28-p16 | digits 1–9, 9ˣ = 3⁴ⁿ | 4 lamp colors, 4ˣ = 2⁶ⁿ | 3n (3) |
| wp28-p17 | 5-digit code starts 4, increasing | 6-digit code starts 3, increasing | 6 (3) |
| wp28-p18 | two 8-sided dice, sums that tell the pair | two ordinary dice | 4 (2) |
| wp28-p19 | no zero, first = last, third = 2 × second | third = 3 × second | 27 (3) |
| wp28-p20 | 8 digits, 2 digits × 4, sum ÷ 10 | 6 digits, 2 digits × 3, sum ÷ 12 | 10 (3) |
| lesson wp-137 #2 | 4 children out of 10, Danny / Yossi (the Hebrew's) | 3 children out of 9, Lior / Sam | – |
| lesson wp-137 #4 | 9 out of 10 → 10 (the Hebrew's) | 14 out of 15 → 15 | – |
| lesson wp-141-after #2, #3 | 4-digit all same (9), 4-digit palindromes (90) (Hebrew: 3-digit) | 5-digit all same (9), 5-digit mirror numbers (900); slide "Mirror digits" | – |
| lesson wp-140-after #2 | "7! = 7 · 6 · 5!" (old Q13) | "9! = 9 · 8 · 7!" (new Q13) | – |
| summary #2, #3 | 3 × 5 = 15 shirts/hats (the Hebrew salad numbers); 9!/7! = 72 (now Q13) | 5 × 4 = 20; 8!/6! = 56 | – |
| cards | examples of the old questions | examples of the new questions; pairs table to n = 12 | – |

## 2026-10-06 review
Independent review of the renumber pass (built with / without `renumber_pass`, compared every question, explanation,
solutionVisual, solution video, lesson video, card and summary). `renumber_pass(M)` is the last call in `apply()`.
All 37 keys re-computed by enumeration (itertools): every key correct, exactly one correct choice, traps still present.
Type / condition / difficulty match the originals; nothing lands back on the Hebrew subtitles' numbers or objects
(the Hebrew's dice answer 33 only remains as the unordered-trap distractor in g136). No recorded videos in Topic 28.
No spoken "Question N"; no leftover old numbers or objects in boards, speech, draw cues, titles or figures.
Fixed:
- wp28-g136 stem: "A green die and a yellow die" → "A green dice and a yellow dice" (course / NITE style uses "dice"
  for one die, as the original stem did).
- solve-wp28-g144: "Choice seven is too few" → "Seven is too few" (sounded like a choice number; there are 4 choices).
`python3 math_check.py 28 32` → PROBLEMS 0, WARNINGS 0, LAYOUT 0.
Judgment calls left for the teacher: practice removals q-15 / q-27 (at least one), q-22 (repeats with 0), q-23 (round
table with a restriction) and q-18 (together) remove September items whose type the Hebrew practice does not cover —
they repeat a kept item (q-14, q-21, p26, p23) rather than a Hebrew one; three practice answers are 720 (p07, p14, p15).
