# Topic 24: Overlapping groups (changes)

Source: `student_review/review_t23-24.md` (Topic 24 part) and `PLAN.md`. Patch: `math_patches/t24.py`.
Check: `python3 math_check.py 24` gives 0 problems, 0 warnings and 0 layout problems (70 slides).

## Counts
- Questions rewritten: 23. That is all 8 guided questions and the 15 remaining practice questions. Every written solution now shows the numbers in TeX. Stems are clearer, and spelling is US.
- Questions added: 11. Three are guided questions with solution videos (q-r26-t24-01 to 03). Eight are practice questions (q-r26-t24-04 to 11).
- Questions removed: 2 near-duplicates. **wp24-p04** repeated guided Question 1 (given both, find neither). **wp24-p02** repeated p08 and Question 9 (everyone is in at least one group).
- Topic total: 25 questions before, 34 after. Guided went from 8 to 11 and practice from 17 to 23.
- Slides changed: 12. Slides added: 3 in existing videos plus 1 in the Question 5 video.
- Videos added: 5. There are 2 lessons, "Two-Way Tables" (5 slides) and "Three Groups" (4 slides), plus 3 solution videos.
- Memory cards: `mem-overlap` rewritten. New card `mem-r26-t24-more`, "Two-way tables and three groups".
- Figures: none. The topic has no question figures.

## Priority 1: wrong or misleading rules
- "Overlap Ranges" slide 4: the note said "Write max(8, 7) → 7", but max(8, 7) = 8. It now says "the smaller of 8 and 7 → 7".
- "Overlap Ranges" slide 8 ("Spot the wording", was slide 7) said "'At most' → maximum [overlap], 'at least' → minimum". That rule is wrong for questions about "only" or "neither" (p16, p07). The new board says that "at most" and "at least" refer to **the thing they ask about**, and adds "Ask: to make THIS small, what must the overlap be?" Two examples follow: at least music only → max overlap; at most neither → max overlap. The recap (slide 11) and the memory card are fixed to match.
- Question 9 (wp24-g078, butterflies, was Q8): "photograph **different** butterflies" could be read as "no overlap". It now says "Two researchers photograph butterflies … show 40 different butterflies."
- p13 (three groups): the solution ended with "we still need a construction". It now proves the answer 0 with a full construction: 35 fiction+history, 30 fiction+science, 30 history+science, 5 fiction only.
- The on-screen "Twenty−one" (a math minus inside a word) in the Question 5 video is gone. The stem now uses numerals, and the slide descriptions are regenerated.

## Priority 2: methods added
- **Other regions (range)**: new slide 7 "Other regions" in "Overlap Ranges". Same 12/8/7 example. The overlap is 3 to 7. From it: at least one = A + B − both, 8 to 12 (larger group up to A + B, never more than the total). Neither = total − union, 0 to 4. Music only = A − both, 1 to 5, and its minimum uses the MAXIMUM overlap.
  - Guided: **new Question 6** (q-r26-t24-01, swim but not run, answer 5). It targets the "at least → min overlap" trap: the trap answer 23 is the most, not the least. Its solution video has 2 methods.
  - Practice: q-r26-t24-07 (greatest neither), -10 (greatest "tennis only"), -11 (which could be "at least one"), plus the existing p07 and p16.
  - Question 5's video now starts with the simpler route. Neither = 48 − union, and the union goes from 21 to 32, so neither goes from 16 to 27. The complements method is now Method 2 and the elimination insight is Method 3.
- **Exactly one**: new slide 6 "Exactly one" in "Exact Overlap". It shows the strip (5 + 4 = 9), then the formula A + B − 2·both (10 + 9 − 10 = 9), then union − both. It is also on the recap and the card. Practice: p12, p17, and the new hard q-r26-t24-08 (greatest exactly one = 43).
- **Two-way (2×2) table**: new lesson video `r26-t24-two-way`. It starts with the trap: 20% of the women and 30% of the men can't be added or averaged. Next it fills a table with totals (plug in 100), and then covers "percent of what?", where the words after "of" pick the whole (row, column or all).
  - Guided: **Question 10** (q-r26-t24-02, walkers, 25%). One slide explains each distractor.
  - Practice: q-r26-t24-04 (counts), -05 (percents), -06 (fractions, exam level).
- **Three groups**: new lesson video `r26-t24-three-groups`. It teaches "count who is missing": min in all three = total − (missing A + missing B + missing C), or 0. The same thing in one line is A + B + C − 2·total. It also covers why 0 can happen (the p13 construction) and that the max in all three is the smallest group.
  - Guided: **Question 11** (q-r26-t24-03, phone/laptop/tablet, 25%). Its traps are 55% (two groups only) and 70% (the maximum).
  - Practice: q-r26-t24-09 (answer 15) and the fixed p13.
- **Work in percent** is now a tip on the memory card. p15's solution now contrasts with Question 7: 55% + 45% = 100% alone forces nothing, but "20% do neither" does.
- Weak-student fixes:
  - "Exact Overlap" slide 3 now says that the strip is the circles "unrolled into one line".
  - Question 2's video shows the easier route (through the union) first. The strip is now Method 2.

## Priority 3: text
- All 23 existing questions got solutions with numbers in TeX, with no words-only steps and no "so" meaning "therefore" in mid-sentence.
- Stems that started with number words ("Fourteen cut…", "Forty-eight are round…") now use numerals.
- Stray spaces around 3 stems were removed. p06 now says "All ranges include both ends" once, instead of "(inclusive)" twice. p11 now asks "the range of possible numbers of people who use both".
- US spelling in all topic videos: organiser → organizer, flavours → types, recognise → recognize, torch → flashlight (Question 1 stem and video).
- Question 3 video: the note "15 : 9 = 5 : 3" is now marked as a ratio.
- The titles of all solution videos show the current stems.

## Priority 5: practice
- Order is easy → hard: p17, p14, p12, new-04, p09, p01, p08, p11, p15, new-11, new-07, p16, p03, p06, p07, p10, new-05, new-10, p05, new-08, new-06, new-09, p13.
- 15 or more items are exam level: p03, p05, p06, p07, p10, p11, p13, p15, p16 and new 05 to 11.

## Placement and numbering
- The two new lessons, with Questions 10 and 11 and the new card, come after Question 9 in the second section. That section is renamed "More methods and guided examples".
- New Question 6 sits right after Question 5, so the old Questions 6–8 are now 7–9. Titles, spoken numbers and sidebars were renumbered automatically.

## API workarounds
- Solution-video titles and "on screen" descriptions were rebuilt inside the patch (`tidy`), because `set_q` does not refresh them.

## For the teacher to decide
- The 2×2 table and three groups are separate short lessons, not slides inside "Exact Overlap". Please check that this is the order you want.
- (Pass 2: p02 and p04 are restored - see below.) p17 (easy exactly one) was kept as an easy warm-up.

## Pass 2 (teacher-approved plan, 2026-09-27)
**Removed:** nothing. `q-r26-t24-08` stays ("exactly one" is an original type).

**Restored:** `wp24-p02` (26 art, 19 music, 11 both → 34) and `wp24-p04` (120 hikers, neither → 15), with TeX choices and numeric solutions. They are placed at the easy start of the practice (p02 first, p04 after p14).

**Summary lesson added:** `r26-t24-summary` "Summary: Overlapping Groups" (about 2.8 minutes), at the end of "More methods and guided examples", right before the practice.
Slides: Summary · Four regions (a full group = its only-region + both) · Count each once (A + B − both + neither = total) · Maximum overlap (the smaller group) · Minimum overlap ((A + B) − total, or 0; fractions and percents) · Other regions (union, neither, A only; "at most / at least" of the thing they ask) · The squares method (strip, exactly one = A + B − 2·both) · Two-way tables (plug in 100, rows/columns, "of the ..." is the whole) · Three groups (min = total − the missing ones, A + B + C − 2·total, max = smallest group) · Before you practice (range or exact?, which region?, what overlap makes THIS big or small?, who is the whole?, plus the common traps).

## 2026-10-01 elite comparison
Target: real exam 2023_autumn_q2_20 (every pair of three groups shares a given number → range of all three).
- The rule "Max in all three = the smallest group" stays exactly as taught. It is the ceiling when only the group sizes are known.
- **Lesson "Three Groups" (r26-t24-three-groups): new slide "Pairs given"** after "Can it be zero?". Clubs of 40, 35 and 30; pairs share 12, 9 and 15. Someone in all three is in every pair, so the maximum is the smallest pair overlap: 9 (not 30). The minimum here can be 0 (12 + 9, 12 + 15 and 9 + 15 all fit in the clubs). Recap has a new line; sidebar updated.
- **Card mem-r26-t24-more**: new row "Max in all three, pairs given — the smallest pair overlap — pairs 12, 9, 15 → 9".
- **Summary (r26-t24-summary), slide "Three groups"**: new line "Pairs given? Max in all three = the smallest pair overlap".
- **New practice question q-r26-t24-12** (last in the practice): choir 50, band 45, drama 40; pairs 14, 11, 16; greatest possible number in all three = 11 (choice 2). Traps: 40 (smallest group), 16 (largest pair), 41 (sum of the pairs).

## 2026-10-05 cut repeats
Function `cut_repeats` (runs last). The two lessons added this month go back to a short intro. A lesson slide is cut only where the guided question right after it teaches the same thing. Nothing in topic 24 is recorded. Questions, numbers, methods and the memory card are unchanged.
- **`r26-t24-two-way` Two-Way Tables**: 5 → 2 slides, 1.9 → 0.7 min. Kept: the title slide. Slide 2 "Two traits" is rewritten as a short intro: the trap "Percents of different groups: don't add, don't average" (Q10 does not teach this, so it stays here) + "Plug in 100 → a table with totals" + "Let's see it in a guided question. Try it first." Cut: the worked glasses example ("Fill the table", 24%) → Q10 `solve-q-r26-t24-02` builds the same table (plug in 100, rows, columns, totals). "Percent of what?" → Q10 ("of the students who WALK. The whole is the walk column", the wrong-whole traps, "Always ask: percent of WHAT?"). Recap cut. Its "rows add across · columns add down" now comes in Q10, which says "Add down the walk column: forty-eight students walk."
- **`r26-t24-three-groups` Three Groups**: 5 → 4 slides, 2.8 → 2.3 min. Slide 2 "Count who is missing" drops the worked 50-employee example, because Q11 `solve-q-r26-t24-03` solves the same kind of question with both methods. The rule stays on the slide in two board lines: "Min in all three = total minus everyone who misses a group" and "A + B + C − 2 · total". The line "two groups: once, three groups: twice" also stays. KEPT unchanged: "Can it be zero?" (the zero case with a built example, and "max in all three = the smallest group", the teacher-approved rule), and "Pairs given" (the teacher-approved pair-overlap step). No question video teaches either one. Recap cut, and its four items are on the memory card and in the summary. "So here: from zero to nine." now ends with "Now a guided question — try it first."
- Q10 `solve-q-r26-t24-02` 1.1 → 1.2 min (reworded line). **Net: −1.6 min.**
- Not flagged and not changed: wp-067, wp-068, wp-069. No video says "as we saw in the lesson" about a cut idea. The AI summary `r26-t24-summary` was not edited. Everything it sums up is still taught.
- **Follow-up (same day): every cut idea checked again.** Two-Way Tables: the 20% + 30% "don't add, don't average" trap is on the kept slide 2. The table with totals and plug-in 100 → Q10 method 1. "The words after 'of' tell you the whole" → Q10 slides 2–3 ("of the students who WALK… the whole is the walk column", "Always ask: percent of WHAT? That's the row or column you divide by"). The recap's board line "Rows add across · columns add down" had disappeared, so it now comes back in Q10 `solve-q-r26-t24-02` slide 2 as a board item. The spoken line there is now "Rows add across, columns add down. Add down the walk column: forty-eight students walk." Three Groups: the 50-employee example (who is missing, "even if they are all different people", total minus the missing, A + B + C − 2 · total) → Q11 methods 1 and 2. The recap items are on the kept slides 2–4: "or 0" and "max = the smallest group" on "Can it be zero?", the pair rule on "Pairs given". Q11 also says "70% is the maximum — the smallest group". Nothing else was lost. One analogy is dropped: "It's the same sudoku as the strip". Q10 stays 1.2 min; net still −1.6 min.

## 2026-10-06 new exam methods
Function `add_methods` (runs last). Card only, no video change.
- **Card `mem-overlap`**, new tip after "Percents? Stay in percent…": "No total given? Look for a natural one: 24 hours, 7 days, 100%. Awake 18 hours, at work 10 hours → both for at least 18 + 10 − 24 = 4 hours." (the hidden total; 1 real exam question). Teacher guide: scratchpad `guide/t23-t25.md`.
- Check: `math_check.py 24 32` → 0 / 0 / 0.

## 2026-10-06 practice: new methods
Function `practice_methods` (runs last in `apply`). One extra line is added at the end of each written solution; the existing lines are kept. Nothing is recorded. Few questions fit: most practice questions give the total, and the topic 23 methods do not fit overlap questions.
- `wp24-p08` (Spanish 3/4, Italian 5/8, everyone at least one): Hidden total: the whole club = 1 → 3/4 + 5/8 − 1 = 3/8 (exact, since nobody is in neither).
- `wp24-p05` (which overlap is forced): Hidden total: the whole town = 1 → under 50 and pets overlap by at least 4/5 + 2/5 − 1 = 1/5.
- Every line checked in python. Check: `math_check.py 24 32` → 0 / 0 / 0.

## 2026-10-06 renumber pass
So the English course does not look like the Hebrew one: every Hebrew-derived question has a new story (new names, groups
and setting) and new numbers. The idea, the trap, the level and the methods stay the same (Venn / pizza picture, the
squares strip, A + B − total, max overlap = the smaller group, the pair-overlap step — all still taught). Every guided
solution video is rewritten to match (speech, draw cues, strips, video title, pre-loaded question text). Nothing in Topic 24
is recorded, so nothing had to be kept as it was. Function `renumber_pass(M)` in t24.py runs last (after `cut_repeats`,
`add_methods` and `practice_methods`; the two "Hidden total" lines that practice_methods added to p05 / p08 are rewritten
with the new numbers).

**Counts:** 8 guided questions renumbered (wp24-g070 … g078) with their 8 solution videos rewritten; 10 practice questions
renumbered (wp24-p01 … p10). Lesson examples renumbered: pizza (Overlapping Groups), 6 slides of Overlap Ranges (the
12-student example, 5 + 7 = 12, 65% / 55%, 2/3 + 1/2), 7 slides of Exact Overlap (the 18-member club on 5 slides,
1/5 and 1/3, "forty different items"), and the memory card example. Practice: 26 → 16.
English-made items (guided q-r26-t24-01 … 03, the two-way / three-groups lessons, the summary, kept practice items) keep
their numbers.

**Order:** the two exact questions (old Q8 fractions + people, old Q9 "different species" reading trap) move to the start of
the advanced group (now Q4, Q5): they come right after the exact lesson and Q1–Q3, and the range questions follow (Q6 minimum
in percent, Q7 could-be neither, Q8 at-least trap, Q9 not necessarily true). Correct-answer positions moved in 7 of 8
guided questions. Practice ordered easy → hard.

**Practice clean-up (26 → 16):** no copies in this topic (copies list empty). Extra-bank items kept (3): p17 exactly one,
p16 at-least-only trap, p13 three groups / zero case. Removed p11 (range of both: p01, p03, guided), p12 (exactly one: p17),
p14 ("of the French pupils": guided Q10), p15 (both from neither: guided Q2). September items kept (3, types the Hebrew
practice does not have): q-05 (two-way table, percents of different groups), q-09 (three groups, minimum), q-12 (pairs
given — teacher-approved). Removed q-04 (table by counts: q-05), q-06 ("of the chess players" = guided Q10), q-07 (greatest
neither = p07), q-08 (greatest exactly one), q-10 (greatest only-region: p16 and guided Q8), q-11 (could-be union = guided Q7).

**Checks:** every answer and every method step recomputed in Python (exact fractions); g071 brute-forced over all overlaps;
g075's possible "neither" values listed (15 … 28, only 19 among the choices); g076 / p05 each pair sum computed (exactly one
statement not forced / forced); traps still among the choices (smaller-group trap 28% in p07, the whole-group ratio 5:8 in
g072, the union 27 and "forgot to add back" 28 in g077, the maximum 162 in g074, etc.). Duplicate check over topics 1–24
(stems, lesson boards and lines, cards): no new question equals another question or a lesson/card example (only incidental
shared numbers in unrelated topics). Each new question compared side by side with its original: same type, same condition
kind, same number of steps, same choice kind. `python3 math_check.py 24 32` → PROBLEMS 0, WARNINGS 0, LAYOUT 0. Rendered
all 3 lessons and the 8 solution videos and looked at them (pizza with 6 slices / 4 shaded, 15-box grids with 10 shaded,
strips with the new labels, titles Question 1–9 and sidebars correct). No quadratic trinomial added.

| id | old (Hebrew) | new | answer |
|---|---|---|---|
| wp24-g070 (Q1) | 45 campers, flashlight 28, map 23, both 16 → neither | 52 hotel guests, pool 31, gym 26, both 17 | 12 (3) |
| wp24-g071 (Q2) | 22 machines, cut 14, polish 12, neither 3 → both | 27 printers, color 16, posters 13, neither 3 | 5 (4) |
| wp24-g072 (Q3) | both = 1/6 of photography, 1/4 of volunteers → 5:3 | both = 1/5 of chess club, 1/8 of robotics club | 4:7 (2) |
| wp24-g078 (Q4, was Q9) | butterflies 31 and 22, 40 different → both 13 | bird species 34 and 27, 45 different | 16 (1) |
| wp24-g077 (Q5, was Q8) | soup 2/5, salad 1/4, both 1/10 = 8 people → neither 36 | conference morning 1/3, evening 1/5, both 1/12 = 5 people | 33 (2) |
| wp24-g074 (Q6, was Q4) | 240 guests, 35% organizer, 80% host → min 36 | 360 wedding guests, 45% bride, 70% groom | 54 (1) |
| wp24-g075 (Q7, was Q5) | 48 students, greenhouse 21, orchard 11; neither could be 14/30/35/18 | 52 students, library 24, kitchen 13; 36/13/19/31 | 19 (3) |
| wp24-g076 (Q9, was Q7) | company: code 2/5, remote 4/5, juniors 1/5, training 1/2; juniors & remote = 1 | nurses: nights 3/10, drive 3/4, new 1/4, part time 1/2; new & drive = 1 | (3) |
| wp24-p01 | fair 150, 65% nearby, 55% train → min 30 | book fair 160, 72% students, 53% card | 40 (2) |
| wp24-p02 | art 26, music 19, both 11, all in one → 34 | basketball 31, volleyball 24, both 13 | 42 (3) |
| wp24-p03 | 3/5 company tablet = 72, 1/2 personal → min 12 | 3/4 bus pass = 135, 2/5 bicycle | 27 (3) |
| wp24-p04 | 120 hikers, map 54, compass 82, both 31 → neither 15 | 140 runners, cap 63, sunglasses 88, both 36 | 25 (2) |
| wp24-p05 | town: cycle 3/5, veg 1/4, pets 2/5, under 50 4/5; forced under 50 & pets | city: walk 2/3, dog 1/4, garden 1/3, under 60 3/4; forced under 60 & garden | (3) |
| wp24-p06 | 60 trainees 0–12: 9–12: 26, 7–10: 24, below 7: 20 → 9–10 | 70 applicants 0–20: 15–20: 31, 11–16: 26, below 11: 24 → 15–16 | 11 (2) |
| wp24-p07 | 250 students, chess 205, instrument 190 → max neither 18% | 300 hotel guests, breakfast 249, pool 216 | 17% (2) |
| wp24-p08 | Spanish 3/4, Italian 5/8, all in one → 3/8 | party: pizza 4/5, cake 2/3 | 7/15 (3) |
| wp24-p09 | 48 students, swim 28, cycle 24, 3/4 of cyclists swim → neither 14 | 56 members, hike 30, kayak 25, 3/5 of kayakers hike | 16 (3) |
| wp24-p10 | bags: blue 2/3, zips 3/4, both 1/2 → 2:3 | cars: white 3/5, four doors 4/5, both 1/2 | 1:3 (2) |
| lesson wp-067 #4 | pizza 8 slices, mushrooms 5, tomatoes 4 → 1 to 4 | 6 slices, mushrooms 4, olives 3 | 1 to 3 |
| lesson wp-068 #2–#8 | 12 students, music 8, sport 7 (min 3, max 7; union 8–12; neither 0–4; only 1–5); 5 + 7 = 12; "five and five" | 15 students, art 10, drama 9 (min 4, max 9; union 10–15; neither 0–5; only 1–6); 6 + 9 = 15; "six and six" | – |
| lesson wp-068 #9, #10 | 65% / 55% → 20%–55%; 2/3 + 1/2 − 1 = 1/6 | 60% / 50% → 10%–50%; 3/5 + 2/3 − 1 = 4/15 | – |
| lesson wp-069 #2–#6 | 18 members, Spanish 10, French 9, neither 4, both 5; exactly one 9 | 25 members, tennis 13, squash 11, neither 5, both 4; exactly one 16 | – |
| lesson wp-069 #7, #8 | overlap 1/5 of A, 1/3 of B → 2:1; "forty different items" | 1/10 of A, 1/4 of B → 3:1; "sixty" | – |
| card mem-overlap | 12 students: 8 and 7 | 15 students: 10 and 9 | – |

## 2026-10-06 review (renumber pass)
Independent review (pre/post build diff, keys recomputed, Hebrew subtitles compared). All keys / traps / methods correct;
max overlap ≤ smaller group and the pair-overlap step still taught. Fixed four guided questions that landed back on the Hebrew:
- g074 (Q6): wedding, bride / groom = the Hebrew's own setting → gallery opening, 45% know the artist, 70% the gallery
  owner (numbers unchanged: min 15% of 360 = 54; strip labels Artist only / Owner only).
- g077 (Q5): 1/3, 1/5, total 60 = the Hebrew's rice 1/3, mash 1/5, 60 workers → 1/4 morning, 1/6 evening, 1/12 both = 4
  people → 48 participants; evening only 1/12, neither 3/4 − 1/12 = 8/12 = 32. Choices 16 (union) / 32 / 12 (morning) /
  28 (forgot to add back). Video rewritten (twelfths; people first: 12, 8, not morning 36, 36 − 4 = 32).
- g078 (Q4): bird species (the Hebrew: owls photographed) → two friends' lists of movies watched, 34 / 27 / 45 → 16.
- g072 (Q3): 1/5 of chess (the Hebrew had 1/5 → 4x) → 1/9 of chess, 1/4 of robotics → 8x : 3x = 8 : 3; trap 9 : 4
  (whole clubs), 3 : 8 inverted; plug-in both = 2 → 18 and 8 → 16 : 6.
