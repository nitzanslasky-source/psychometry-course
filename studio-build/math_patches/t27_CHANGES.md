# Topic 27 — Motion: changes

Patch: `math_patches/t27.py`. Check: `python3 math_check.py 27` shows 0 problems, 0 warnings and 0 layout problems (94 slides).

## Summary
- Questions: 36 rewritten (all 13 guided and the 23 practice questions that stay), 22 added (7 guided with solution videos and 15 practice), 4 removed.
  Before: 40 questions (13 guided, 27 practice). Now: 58 questions (20 guided, 38 practice).
- Lesson videos: 4 existing lessons changed (10 slides changed, 2 slides added). 2 new lesson videos: "Special Motion Cases" (7 slides) and "Percents, Letters and Graphs" (6 slides).
- Solution videos: 7 new (Questions 14–20). 12 existing ones edited (text and notation, plus real teaching changes in Q12 and Q13).
- Memory cards: "Motion — rules to know" rebuilt. New card "Motion — special cases".
- Figures: 5 new distance–time graphs (2 on lesson slides, 3 in questions).
- All answer keys were already correct. Every new or changed question was solved again from scratch.

## 1. Wrong or misleading teaching (fixed)
- **Average Speed, slide 4:** it said "the average speed sits closer to the slower speed" with no condition. That is only true for **equal distances**. The slide now also says **equal times → the plain average** (1 hour at 60 and 1 hour at 90 → 75). The teacher asks "equal distances, or equal times?" before calculating.
- **Average Speed, slide 1:** "Honestly? Rare on the exam." was removed. Students skip what is called rare, and Q3 and the practice test it.
- **Q12 video, estimate slide:** it said "the estimate doesn't settle this one". It does. 1.5 times as fast → 6 hours; 1.8 is between 1.5 and 2, so the time is between 4.5 and 6 → only 5. The slide now shows this.
- **Q13 video:** it opened with the equation and then said "not how we'll do it on the exam". Now relative speed is Method 1 and the equation is only a check (Method 2).
- **Memory card:** the circular-track row covered only the same direction. It now also has opposite directions (add the speeds; one lap together per meeting). p10 and p19 need this.

## 2. Methods added
In **"Distance, Speed and Time"**:
- **Slide 4 (Units):** a table of minutes as fractions of an hour (12 = ⅕, 15 = ¼, 20 = ⅓, 30 = ½, 40 = ⅔, 45 = ¾), with why 20 minutes = ⅓.
- **New slide 6 "The table":** the distance–speed–time table (one row per person or part of the trip; distance = speed × time in every row; add distances and times, never speeds). Q3 and Q11 used it before it was taught.
- **Slide "Draw a sketch":** a one-line reminder of Pythagoras (a² + b² = c²). Q2 needs it, and geometry (T31) comes later. The sketch habit is spelled out: a dot for each starting point, an arrow for each direction, and the gap. The formula triangle was already drawn on slide 3; only its notes changed (÷ instead of ":").

In **"Speed Ratios"**: new slide **"What is fixed?"**. It gives 4 quick situations (fixed time, distance, time, speed) before Q4. The recap now has all three rules and "First ask: what is fixed?".

In **"Relative Speed"**, slide 5: a real sketch on the board (chaser and leader, gap = 2 km).

In **"Average Speed"**, recap: estimate first (which side of the middle?), and the optional check 2ab/(a+b) for equal distances. The Q3 video ends with this check (72, 48 → 57.6).

**New lesson video "Special Motion Cases"** (after Q13):
1. Train length: passing a post = the train's length; a tunnel or bridge = tunnel + train.
2. Two trains passing: the sum of the lengths, at the relative speed.
3. Current and wind: downstream = boat + current, upstream = boat − current; current = half the difference, boat = the average.
4. Circular track in both directions: same direction subtract, opposite add; one lap per meeting.
5. Meeting twice: together 3 road lengths → 3 times the time and 3 times each walker's first distance.
6. Recap.

**New lesson video "Percents, Letters and Graphs"** (after Q17):
1. Speed % → time % table: +25% → −20%, +50% → −33⅓%, +100% → −50%, −20% → +25%. Method: write it as a fraction and flip it. T26 teaches the same rule for rate and time.
2. Answers in letters: plug in easy numbers (not 0 or 1), find the target, and test every choice.
3. Distance–time graphs: steepness = speed, flat = stop, and the average speed includes the stop.
4. Two travelers on one graph: a line going down means going back; crossing lines = a meeting; calculate when the crossing cannot be read exactly.
5. Recap.

**New guided questions**, each with a solution video:

| # | id | Question | Answer | Main trap |
|---|---|---|---|---|
| Q14 | q-r26-t27-01 | train 300 m, post in 15 s, bridge 500 m | 40 s | 25 (forgets the train) |
| Q15 | q-r26-t27-02 | 48 km down in 2 h, up in 3 h; current? | 4 kph | 8 (not halved), 20 (the boat) |
| Q16 | q-r26-t27-03 | circle 1.2 km, opposite directions, 20 and 16 kph | 2 min | 18 (same-direction answer) |
| Q17 | q-r26-t27-04 | meet 4 km from A, then 2 km from B; road? | 10 km | 12, 6, 14 |
| Q18 | q-r26-t27-05 | 25% faster saves 12 min; usual time? | 60 min | 48 (time −25%, and it is the new time) |
| Q19 | q-r26-t27-06 | d km in t h; minutes for k km | 60kt/d | shows why speed 60 is a bad number to plug in |
| Q20 | q-r26-t27-07 | graph: fastest part of a trip | 25 kph | 20 (a line going down "looks slower") |

**Strong-student tricks, now taught by name:** estimate and eliminate (Average Speed recap, Q3, Q12); plug in numbers (new lesson, Q19, p02, p03); work back from the answers (Q11 video, card tip, p16, p17); the 2ab/(a+b) check.

**Other teaching fixes in the existing videos:**
- Q9 and Q8 explain "dividing by a fraction = multiplying by its reciprocal".
- Q11 explains why the equation is multiplied by 36 (the smallest number that 12, 3 and 18 all go into, after 2x/24 = x/12).
- Q2's video adds the Pythagoras numbers (169 − 144 = 25).

## 3. Text
- ":" used for division was replaced by "÷" or a fraction bar in every draw note, card and solution. Real ratios keep ":" and the note says "ratio". Clock times such as 08:30 stay as they are.
- American spelling in all topic videos (kilometer, meter, memorize, traveled, toward).
- "so" meaning "therefore" in the middle of a sentence was removed everywhere: in written solutions, and in 14 spoken lines (for example "…— so the time is equal" → "… So the time is equal").
- Every written solution was rewritten. Each one now uses short steps with the numbers in TeX, uses the method the lesson taught, and names the trap choice.
- Stems:
  - Q2: "displacement" became "horizontal distance from its starting point".
  - Q4: "towards one another" became "toward each other".
  - Q10 and Q12: "180-meter" and "1,350-kilometer" were reworded. This removes the "180−meter" display bug in the video, and all pre-loaded stems on slides were refreshed.
  - Units were added where they were missing ("at 30" → "at 30 kph", "in kph?").
  - p15 now says "reach the stopped van" instead of "first catch it".
  - p19 states the counting rule clearly.
  - Letters are now in TeX (p02, p03, p17).
- **p10** used a central angle (circles, T33, taught later). It now asks for the **fraction of the track** (answer ⅙). The key stays choice 4.

## 4. Figures
- New distance–time graphs in the course figure style: two on lesson slides, plus Q20, practice q-r26-t27-19 (two cyclists, values given by dashed guide lines, not by a grid) and q-r26-t27-20 (a trip with a stop).
- The question figures show the site's standard caption "Figure not necessarily drawn to scale". Every value needed is labeled, so this does not matter. The teacher may still want to hide the caption for graphs.

## 5. Practice
- **Removed (near-duplicates or one-step):**
  - p14 (≈ Q13)
  - p21 (≈ Q3)
  - p22 (one-step meeting)
  - p23 (≈ Q1)
- **Added 15 exam-level questions:**
  - two trains passing (08)
  - train length from two passes (09)
  - plane and wind, with the trap 480 = the average speed (10)
  - current as a multiple of the boat's speed (11)
  - circular track, speed ratio from both directions (12)
  - meeting twice, distance (13) and time (14)
  - speed % → time % (15, 16)
  - answers in letters (17, 18)
  - graphs (19, 20)
  - average speed with equal times (21) and "first third" (22)
- **Order:** easy → hard: basics, then ratios and percents, chases and meetings, average speed, trains and rivers, circles, letters, graphs, and exam-hard at the end.
- Methods that practice used without teaching (current, train length, circular track in opposite directions) are now all taught before the practice section.

## For the teacher to decide
- The new videos are in "Further guided examples", after Q13. They could also go into "Learn and try".
- p13 (scientific notation) stays as an easy warm-up. It is more exponents than motion.
- Q2 still depends on Pythagoras. The lesson now gives a one-line reminder. The other option is to move Q2 after T31.

## Pass 2 (2026-09-27): remove/restore plan + summary lesson
Check: `python3 math_check.py 18 27 28 33` shows 0 problems, 0 warnings and 0 layout problems.

**Removed (plan):**
- "Special Motion Cases": the slides "Two trains" and "Meeting twice", their Recap lines and sidebar entries. The title slide no longer mentions meeting twice. The recap now says "Three questions next."
- Guided q-r26-t27-04 (meeting twice) and its solution video. Later guided questions were renumbered: the guided questions now run 1 to 18.
- Practice q-r26-t27-08 (two trains), -13 and -14 (meeting twice).
- Card "Motion — special cases": the rows "Two trains pass each other" and "Two walkers meet … meet again". The intro no longer mentions meeting twice.

**Removed (teacher decision: distance-time graphs):**
- In `r26-t27-graphs`: the slides "Distance–time graphs" and "Two travelers", with their figures, recap lines and sidebar entries. The video is now called "Percents and Letters" (2 concept slides and a recap, which says "Two questions next.").
- Guided q-r26-t27-07 (graph) and its solution video. Practice q-r26-t27-19 and -20.
- The card table "Distance–time graphs". The code that drew the 5 graphs was deleted too.

**Restored:**
- Practice wp27-p14, wp27-p21, wp27-p22 and wp27-p23 (the original text, with TeX and the numbers shown in the solutions; p21 now says "8 kph"). They are placed in the practice order by difficulty.
- wp27-p10: the original question (central angle, 45°/72°/90°/60°, key 60°) is restored. It is **moved to the T33 foundation practice** (`geo33-foundation-practice`), because central angles belong to circles. The pass-1 version ("what fraction of the track", key 1/6) stays in the T27 practice as a new question, **q-r26-t27-23**.
- "Average Speed", slide 1: the line "Honestly? Rare on the exam." is back, followed by the original "the idea behind it shows up in disguise" line.

**Summary lesson added:** `r26-t27-summary` "Summary" (about 2.4 minutes). It is at the end of "Further guided examples", right before the practice. Slides: Summary · The formula · The table · Average speed · What is fixed? · Relative speed · Special cases (train, river, circle) · Percents and letters · Before you practice (units, what is fixed, toward each other or a chase / the starting gap, average speed = total ÷ total; traps: 20 minutes ≠ 0.2 hour, the average of the speeds, sketch).

## 2026-10-05 cut repeats
Function `cut_repeats` (runs last, after the canvas/text loop; slides it edits keep their canvas text). Each lesson is back to a short intro like the Hebrew course. Every idea that a question video right after it teaches is cut from the lesson; ideas no question teaches stay, or move as one spoken line + one board item into the question video that uses them. Nothing in topic 27 is recorded. Questions, numbers, methods and memory cards are unchanged.
- **`r26-t27-special` Special Motion Cases**: 5 → 1 slide, 2.3 → 0.3 min. Kept: the title slide ("Trains that have a length. Boats on a river. And circular tracks. Each one has one idea — and we'll learn each one in its question."). Cut: "Train length" → Q14 `solve-q-r26-t27-01` (post = own length, bridge = bridge + train, same drawing); "Current" → Q15 `solve-q-r26-t27-02` (boat ± current, subtract the equations, halve); "Circular track" → Q13 `solve-wp27-g121` (same direction: one extra lap, subtract) and Q16 `solve-q-r26-t27-03` (opposite: one lap together, add); Recap. MOVED into Q14: "Until now, every body was a dot. A train is not a dot — it has a length." + board "A train has a length: past a post = its length · bridge = bridge + train". MOVED into Q15: "With the current — downstream — add it. Against it — upstream — subtract. A plane with the wind? The same: a tailwind adds, a headwind subtracts." + board "Down = boat + current · up = boat − current (wind: the same)".
- **`r26-t27-graphs` Percents and Letters**: 4 → 1 slide, 1.7 → 0.2 min. Kept: the title slide + "Two questions next — one of each." Cut: "Speed % → time %" → Q17 `solve-q-r26-t27-05` (fraction, flip it, +25% speed = −20% time, the 25% trap); "Answers in letters" → Q18 `solve-q-r26-t27-06` (plug in easy numbers, not 0 or 1, target, test every choice); Recap. MOVED into Q17: "Slower works the same way: twenty percent slower is speed times four fifths — so the time is times five quarters, twenty-five percent MORE." + board "Speed × 4/5 → time × 5/4: −20% speed = +25% time". Q18's warning line now ends "Two choices give the target? Try other numbers on those two." (The +50% → −33⅓% row is gone; the same flip method, and the summary still shows −25% → +33⅓%.)
- **Recaps only** (the rest of these lessons is the Hebrew intro — speed ratios rules, relative speed with the "gap only" idea, the motion basics — so it stays): `wp-106` Distance, Speed and Time 8 → 7 slides (4.0 min, the recap was almost silent); `wp-108-after` Average Speed 5 → 4 slides, 2.5 → 2.1 (estimate first and 2ab/(a+b) are both in Q3); `wp-110` Speed Ratios 7 → 6, 1.9 → 1.8; `wp-113` Relative Speed 6 → 5, 1.8 → 1.7. Each keeps its "questions next" line at the end of its last slide.
- Question videos lengthened: Q14 0.6→0.7, Q15 0.6→0.8, Q17 0.9→1.1, Q18 1.0→1.1. **Net: −3.5 min.**
- No video said "as we saw in the lesson" about a cut idea. AI summary `r26-t27-summary` not edited; everything it recaps is still taught (in lessons kept or in the question videos).
- **Follow-up (same day).** Two intros and two lost ideas fixed (end of `cut_repeats`):
  - `r26-t27-special` (0.4 min) now says what the section is about and gives one framing line: "The formula stays the same: distance equals time times speed. Only the distance, or the speed, is different."
  - `r26-t27-graphs` (0.2 min) adds the warning "a percent faster is NOT the same percent less time."
  - RESTORED in Q17 `solve-q-r26-t27-05` slide 2: "Fifty percent faster: speed × 3/2, time × 2/3 — 33⅓% less. Twice as fast: half the time." Board item: "+50% speed → time × 2/3: −33⅓% · twice as fast → half the time". Both examples came from the cut "Speed % → time %" slide.
  - RESTORED in Q15 `solve-q-r26-t27-02` check slide: "the boat in still water is the average of the two speeds — (24 + 16) ÷ 2 = 20". Board item: "Boat = (down + up) ÷ 2". This came from the cut "Current" slide.
  - Rechecked every other cut idea, and each is taught in a question video:
    - train post and tunnel/bridge → Q14
    - "current = half the difference" → Q15 (2c = 8)
    - circle, same direction → Q13
    - circle, opposite directions → Q16
    - flip the fraction, ±20/25% → Q17
    - letters: plug in, not 0 or 1, target, test every choice, two hits → new numbers → Q18
    - Average Speed recap (estimate first, 2ab/(a+b)) → Q3
    - the other recaps only repeated slides that were kept
  - Net for topic 27 is now −3.0 min.

## 2026-10-06 new exam methods
Function `add_methods` (runs last). Nothing in topic 27 is recorded (checked ~/Documents/Course.recordings: only algebra topics 1–6). Check: `python3 math_check.py 27 32` → 0 problems, 0 warnings, 0 layout problems.
- **Product in the middle.** Every motion table in the topic now has the columns **Speed · Distance · Time** (like Team · Work · Time), so the V works. Changed tables (label column kept first): `wp-106` slide 6 "The table", `solve-wp27-g109` slide 2, `solve-wp27-g114` slide 2, `solve-wp27-g118` slide 2, `solve-wp27-g119` slide 2, `r26-t27-summary` slide 3. Every spoken/drawn line on those slides was checked: they name rows and values, never a column position, so nothing else had to change except: `wp-106` "Three columns: distance, speed, time." → "Three columns: speed, distance, time. Distance in the middle — because distance is speed times time, just like work in Team, Work, Time."; `solve-wp27-g119` "A distance–time–speed table." → "A speed–distance–time table."; card tip → "speed–distance–time table (distance in the middle)". Tables that are not motion tables (minutes/hours, Time · Distance identical ratios, Gap · Time · Speed difference) were not touched.
- **Speed Ratios (`wp-110`)**: new slide 7 "Two things change? The V" (sidebar "Two things change"): A 3× as fast as B for half as long, A covers 90 km → rows (3, 90, 1) and (1, ?, 2) → upside-down V → 1·90·2 ÷ (3·1) = 60 km, with the "why" and a sense check. The closing line moved to the new slide and now says "Three questions next". Video 1.8 → 3.0 min.
- **New guided question `q-r26-t27-31`** (Question 6, right after Q5; later guided questions renumber automatically) + solution video `solve-q-r26-t27-31` (1.4 min): van goes 3× as far at 1.5× the speed, scooter 40 min → V: 1·3·40 ÷ (1·1.5) = **80** (choice 2); Method 2 by factors 40 × 3 × 2/3. Traps 180 (speed not flipped), 120 (speed ignored), 20. The "Question N" sidebar of the learn guided group now has one more entry.
- **Card `mem-motion`**: Ratios table row "Two things change → table Speed · Distance · Time, distance in the middle → the V (A: 3, 90, 1 · B: 1, ?, 2 → 60)"; new tip "\"x times slower / smaller\" = ÷ x: A is 3 times slower than B → A's speed = B's ÷ 3".

## 2026-10-06 practice: new methods
Function `practice_methods` (runs last in `apply`). One extra line is added at the end of each written solution; the existing lines are kept. Nothing is recorded. Most one-change questions (wp27-p05, p06, q-r26-t27-15, q-r26-t27-16) already say "same distance: the times flip", and the chases already use gap ÷ difference, so they were not given a duplicate line. No practice question says "x times slower".
- `wp27-p02` (d in t hours → 3× speed, 2t hours): Method 2 · The V in motion: rows (1, d, t), (3, ?, 2t) → 3 · 2t · d ÷ (1 · t) = 6d.
- `wp27-p12` (swimmer, evening at half speed): Method 2 · Compare by factors: 30 · 4/3 · 2 = 80 → 110 minutes.
- `wp27-p21` (2 h at 12 kph, 3 h at 8 kph): Method 2 · Percent shares as weights (by hours): 8 + 0.4 · 4 = 9.6.
- Every line checked in python. Check: `math_check.py 27 32` → 0 / 0 / 0.

## 2026-10-06 renumber pass
So the English course does not look like the Hebrew one: every Hebrew-derived question has a new story (people, vehicles,
setting) and new numbers. Concept, trap, level, condition kind and methods are the same (identical ratios instead of 3.6,
Pythagoras with a known triple, estimate-then-friendly-distance and 2ab/(a+b), ratio / plug-in / elimination, add or
subtract the speeds, starting gap, reciprocal, the two subtraction tricks, ratios + insight, equation + work back,
calculate / ratio / estimate between 1.5 and 2, relative speed on a circle + equation check). Every guided solution video is
rewritten to match (speech, draw cues, tables, bars, route, right triangle, circular-track figure, pre-loaded stem text,
video titles). Nothing in topic 27 is recorded (RN_RECORDED is empty). Function `renumber_pass(M)` runs last (after
`cut_repeats`, `add_methods`, `practice_methods`). The two practice_methods lines on p02 / p12 are rewritten with the new
numbers; the p21 line ("percent shares as weights") moves to q-r26-t27-22 because p21 is removed. No spoken line says
"Question N" (only the existing title slides, which renumber_guided keeps right).

**Counts:** 13 guided questions renumbered with their 13 solution videos; 19 practice questions renumbered (p01–p20; p10
lives in T33 and is not touched here); 1 September item renumbered (q-r26-t27-21: it equalled the Average Speed lesson's
own example 60 / 90 → 75). Lesson examples: 3 slides (`wp-106` #1–#2 "20 seeds / 20 km per hour" and #5 "walker 5 m/s,
half an hour → 9 km" were the Hebrew's own; `wp-113` #3 "4 + 6 = 10" were the Hebrew's 6 and 4 walkers) plus the
`mem-motion` card (its examples were Q3 / Q7's numbers). Practice: 37 → 26.

**Order:** in "Further guided examples" the ferry (old Q13, Hebrew level medium) now comes before the midpoint question
(old Q12, medium plus): Q12 = g120, Q13 = g119. Nothing in g120 uses g119. Correct-answer positions moved in 9 of 13.

**Practice clean-up (37 → 26):** copies removed: p23 (= Q1, m/s for 25 minutes), p21 (= Q3, there and back). Extra-bank
warm-ups kept (3): p27 (halves in 2 h / 3 h), p22 (toward each other), p24 (downstream). Removed p25 (= the Q15 train
idea), p26 (= the Q9 head-start chase). September items kept (4, types the Hebrew practice does not have): -21 (equal
times → plain average), -22 (first third, weighted by time), -10 (plane and wind, trap 480 = average speed), -09 (train
length from two passes). Removed: -15, -16 (speed change → time: Hebrew p05, p06), -17, -18 (letters: p02, p03), -23,
-12 (circular track: p14, p19), -11 (current: p24 and -10 stay). Order easy → hard (units warm-ups, basics, ratios, chases,
meetings, average speed, river, circle, stop / meeting puzzles, letters, wind, meetings count, halves, train length).
Kept on purpose: all English-made guided questions (q-r26-t27-01 … 06, -31) and their numbers.

**Checks:** every answer recomputed in Python with exact fractions (`verify27.py` in the scratchpad), each key the only
hit; letter questions brute-forced on several value pairs (p03 with a = b = 1 still gives two hits, as its warning line
says). Traps still among the choices (0.3 seconds/minutes, 1.7 the path, 87.5 the plain average, 5/9, 2/11 the meeting,
10 = a tenth of an hour, 54 subtracting, 10:08 car driving early, 9 the speed difference, 136 the sum, 20 "cancel",
19.2 multiplying, 24 = x only, 3⅓ forgot +60, 80 min not flipped, 3 h 36 / 9 h 36, 3 min ignores the truck, 2.5 min
adds, 12 forgets the finish, 0.3 m units, 42 equal-distance formula). Compared with the Hebrew subtitles
(02-Word-Problems 6984–8288): no new question lands on the Hebrew numbers, objects or names. Duplicate check against all
questions, lessons and cards of topics 1–27: no question equals another question or a lesson / card example (only stray
shared numbers in unrelated topics). `python3 math_check.py 27 32` → PROBLEMS 0, WARNINGS 0, LAYOUT 0. All 13 solution
videos and the two changed lessons rendered and checked (the route label on Q8 shortened to "Bus" so it does not overlap
"Oakton"). Sidebars Question 1–9 / 10–14 correct after the swap.

| id | old (base / Hebrew) | new | answer |
|---|---|---|---|
| wp27-g107 (Q1) | cart 4 m/s, 25 min (Heb: walker 5 m/s, ½ h → 9) | e-scooter 6 m/s, 50 min | 18 km (3) |
| wp27-g108 (Q2) | drone 390 kph, 2 min, ground 12 (Heb: plane 300, 1 min, 4 → 3) | gondola lift 17 kph, 6 min, ground 1.5 km | 0.8 km (2) |
| wp27-g109 (Q3) | shuttle 72 / 48 → 57.6 (Heb: 60 / 40 → 48) | car city ↔ coast 105 / 70, friendly 210 km | 84 kph (2) |
| wp27-g111 (Q4) | Noor & Eli, 1.75× → 4/11 (Heb: Danny & Dina 1.5×) | Maya & Theo on a bike trail, 1.25×; plug in 16 / 20 | 4/9 (2) |
| wp27-g112 (Q5) | boats in a canal, 3.5× → 2/7 (Heb: planes 2.5×) | rowboat & motorboat on a lake, 4.5×; plug in 4 / 18 | 2/9 (3) |
| wp27-g114 (Q7) | walkers 5 + 7, 800 m → 4 min (Heb: 6 + 4, 500 m → 3) | runners 8 + 10, 1,800 m | 6 min (1) |
| wp27-g115 (Q8) | 08:00 van 60, 08:30 car 90, 105 km → 09:00 (Heb: 6:00 80, 6:30 100, 130) | 09:00 bus 72, 09:20 car 108, 204 km | 10:20 (2) |
| wp27-g116 (Q9) | Mina 3 kph, 20 min, caught after 40 → 4.5 (Heb: Miki 4, 15, 30 → 6) | Zoe bikes 15 kph, 12 min, brother Sam catches after 20 | 24 kph (3) |
| wp27-g117 (Q10) | 9 km/12 min vs 12 km/9 min → 35 (Heb: 8/10 vs 10/8 → 27) | motorbike 6 km/10 min vs train 10 km/6 min | 64 (2) |
| wp27-g118 (Q11) | cable car 180 m, 12 s → 15 (Heb: zip line 120 m, 10 s → 12.5) | elevator 60 m, 20 s | 25 s (2) |
| wp27-g120 (Q12, was Q13) | train 1,350 km, 9 h, 80% → 5 (Heb: 1,600 km, 6 h, 50% → 4) | ferry 360 km, 12 h, 60% faster | 7.5 h (4) |
| wp27-g119 (Q13, was Q12) | midpoint 24 kph vs 20 min + 18 → 24 (Heb: 30 vs 30 min + 20 → 60) | motorcyclists 48 vs 20 min + 36 (×72) | 48 km (3) |
| wp27-g121 (Q14) | circle 600 m, 30 / 24 → 6 min (Heb: karts 500 m, 60 / 50 → 3) | runners, 400 m track, 12 / 9 (4 laps vs 3) | 8 min (3) |
| wp27-p01 | cyclist 1 lap/2 min, 3 laps/8 min, 24 min each → 21 | runner 1 lap/3 min, 2 laps/5 min, 30 min each | 22 (2) |
| wp27-p02 | ferry d in t, 3× speed, 2t → 6d | bus a in b, 2× speed, 4b | 8a (4) |
| wp27-p03 | robot x h at 2x, y h at 3y | drone a h at 3a, b h at 4b | 3a²+4b² (2) |
| wp27-p04 | bus 64 × 3 h, +48, at 80 → 3 | train 75 × 4 h, +60, at 90 | 4 (3) |
| wp27-p05 | taxi 72 kph 1 h 20, back at 48 → 2 h | cyclist 20 kph 1 h 40, back at 16 | 2 h 5 min (3) |
| wp27-p06 | 4 h, 1.6× → 2 h 30 | truck 6 h, 1.6× | 3 h 45 min (3) |
| wp27-p07 | cyclists 12 / 30, gap 9 → 30 min | truck 75, police car 100, gap 5 km | 12 min (2) |
| wp27-p08 | walker 08:00–11:00 at 4, other at 6 → 09:00 | cyclist 07:00–09:00 at 15, other at 20 | 07:30 (3) |
| wp27-p09 | van 360: 120 at 60, ¼ rest at 120, rest at 30 → 8.5 | bus 400: 100 at 50, ⅓ rest at 100, rest at 40 | 8 (3) |
| wp27-p11 | buses 180 km, +15 kph → cannot | trains 240 km, +20 kph | cannot (4) |
| wp27-p12 | swimmer 1.8 / 2.4 km, 60 m/min, half → 110 | rower 1.5 / 2.4 km, 150 m/min, half | 42 (2) |
| wp27-p13 | signal 2×10⁸ × 3×10⁻⁹ → 0.6 m | light 3×10⁸ × 4×10⁻⁹ | 1.2 m (2) |
| wp27-p14 | 3 km circle, 15 / 9 → 30 | 2 km circular road, 28 / 20 | 15 min (3) |
| wp27-p15 | vans 90 / 60, stop at 180 km 1.5 h → 3 | trucks 80 / 60, stop at 240 km 2 h | 4 (3) |
| wp27-p16 | road 140, 08:00 / 09:00, 30 km from B → 80 | road 170, 07:00 / 08:00, 50 km from B | 70 (3) |
| wp27-p17 | D in 4 h, halves v / 3v → 6 | train D in 5 h, halves v / 4v | 8 (2) |
| wp27-p18 | robot 40 jumps/min, 18 kph → 7.5 m | horse 120 strides/min, 36 kph | 5 m (2) |
| wp27-p19 | runners 500 m, 3,750 m each → 15 | cyclists 400 m, 2,600 m each | 13 (3) |
| wp27-p20 | walkers 10:00, 6 / 9, halfway 10:45 → 15 | cyclists 14:00, 16 / 24, halfway 15:30 | 30 min (2) |
| q-r26-t27-21 | 2 h at 60 + 2 h at 90 → 75 (= lesson example) | 2 h at 70 + 2 h at 30 | 50 (2) |
| lesson wp-106 #1–#2 | cracking 20 seeds / 20 km per hour | packing 25 boxes / 25 km per hour | – |
| lesson wp-106 #5 | walker 5 m/s, half an hour → 9 km | cyclist 8 m/s, 25 minutes → 480 m → 12 km | – |
| lesson wp-113 #3 | walkers 4 + 6 = 10 | 3 + 5 = 8 | – |
| card mem-motion | 0.8/12 = 1/15 h; 288/5 = 57.6; 72 and 48 → 57.6 | 1.5/9 = 1/6 h; 240/8 = 30; 40 and 24 → 30 | – |

## 2026-10-06 review
Independent review of the renumber pass (built with / without `renumber_pass`, compared all 13 guided questions + videos,
19 practice items, q-r26-t27-21, lessons wp-106 / wp-113, card mem-motion, the practice removals). All keys recomputed;
each key unique, traps still among the choices; type / condition / difficulty unchanged; videos step-by-step correct.
Fixed in t27.py:
- **g117**: 6 km / 10 min vs 10 km / 6 min landed back on the Hebrew's own first step ("10 minutes = 1/6 hour, ×6") and its
  "10 km in … minutes" car. Now motorbike 9 km in 15 min (36 kph) vs train 15 km in 9 min (100 kph) → 64 (choice 2, same
  choices 46 / 64 / 74 / 136). Video rewritten: "15 min = ¼ h, 9 × 4", "15 × 60/9 = 100", the same two subtraction tricks
  (104 − 40, 36 → 40 → 100), and identical ratios with the old "divide by 3 → 5 km every 3 minutes, ×20" step.
- **g119 video**: the first spoken line ("A speed–distance–time table … call each HALF x") came after the table and the
  fill-in draw cue; moved back before them, as in the original.
- **solutionVisual data** (new `rn_visuals`): g108, g109, g111 (Noor / Eli), g115 (Pine / van), g118, g119, g121 and p09
  still stored the old numbers / names; rewritten to the new ones.
Judgment calls (left): g115's combined speed 72 + 108 = 180 happens to equal the Hebrew's 80 + 100 = 180 (the question's own
numbers all differ); g109 keeps the 3 : 2 speed ratio (2 h + 3 h) of the base and Hebrew — it is the method's structure.
`python3 math_check.py 27 32` → 0 / 0 / 0; g117, g119, g121 rendered and checked.

## 2026-10-07 methods spread
Function `spread_methods(M)` in t27.py runs last (after `renumber_pass`). Every guided and practice question was checked
against the 2026-10-06 methods; a method is added only where it gives the key at least as fast as the existing solution
(each one checked numerically). Questions that already show the method are skipped (Q6 V/factors, chase/lap questions with
gap ÷ difference, wp27-p02/p12/p21 and q-r26-t27-22 from the 2026-10-06 practice lines). Nothing in topic 27 is recorded.
- **Q3 `wp27-g109`** (average speed 105/70): written line + new slide 3 "Method 2 · Shares as weights" (0.4 min): same distance → the times flip (2 : 3), so 2/5 of the time is at 105: 70 + 2/5 · 35 = 84. Slide 2 renamed "Method 1 · Logic, then a table". Board lines by click, pen only circles choice 2.
- **Q19 `q-r26-t27-06`** (d km in t hours, minutes for k km): written line + new slide 4 "Method 3 · Power count with units" (0.5 min): k, d are km, t is hours, the answer is a time → choices 2 (1/hours) and 4 (km²/hours) out; minutes = hours × 60 → 60 on top → choice 3. Pen only crosses out 2 and 4 and circles 3.
- **wp27-p08** (practice): Method 2 · Compare by factors: speed × 4/3 → time × 3/4: 2 · 3/4 = 1.5 h → 07:30.
- **wp27-p03** (practice): Method 2 · Power count: each part a·3a, b·4b has power 2 → choices 1, 3 out; choice 4 opens to 9a² + 24ab + 16b² → choice 2.
Total: 4 written lines, 2 slides (+0.9 min). Recorded: none.

## 2026-10-08 Hebrew points restored
Audit only — nothing to restore, no code change. On the teacher's Hebrew-based lessons (wp-106, wp-108-after, wp-110, wp-113) the 2026-10-05 cut removed only the recap slides; the cut lessons "Special Motion Cases" and "Percents and Letters" are our own additions (trains, currents and the percent/letters slides are not in the Hebrew lessons; circular tracks and +50% speed appear there only as sample questions, and are taught in Q14/Q17 and Q12/Q18). The Hebrew lessons' points ("בעיות תנועה תאוריה": motion = work, formula + triangle, same units, kph meaning, forget 3.6 — rare on the exam, convert by identical ratios, Pythagoras + always draw; average speed: the constant-speed meaning (hand example), total distance ÷ total time, NOT the average of the speeds and why it sits nearer the slow speed, weighted-average link, rare but hidden in "if it moved at a constant speed", pick a friendly distance; speed ratios: no calculation needed, ratios run through the whole section, the three rules, meeting → distances follow speeds and the whole = the sum of the parts, three ways (ratios / friendly numbers / elimination with "if he were twice as fast"), the not-meeting case (the whole = the fast one's parts only); relative speed: definition, toward / apart add (the crash), chase subtract, only the starting gap matters, head start first, units, the result of a chase is how much FASTER, not the speed) — 25 points — are all still said in the lessons or in Q3, Q4, Q5, Q7, Q8, Q9.


## 2026-10-08 coverage fixes
Function `coverage_fixes` (runs LAST; helpers `_hebrew_back.py` loaded as its own copy with CUTOFF 2026-10-08T08-43-14 UTC — a take recorded before it keeps its video unchanged and the point goes into the written solution instead; nothing in topics 21–29 is recorded). Source: the Hebrew-vs-English coverage check (WEAK / MISSING points), teacher approved "go ahead". Notes in `added_notes.json` ("from your Hebrew course (2026-10-08 coverage fix): …").
Teacher decision on Hebrew #17: as in the Hebrew, average speed is solved ONLY as total distance ÷ total time.
- **solve-wp27-g109** slide "Method 1 · Plugging in numbers": the 2ab/(a+b) "check for strong students" (board line + spoken line) removed (−≈10 s).
- **solve-wp27-g109** slide "Method 2 · Balance (averages)" (weighted average, hours as weights) replaced by **"Method 2 · Algebra"** — still total ÷ total: each way d, total distance 2d (board), total time d/105 + d/70 = d/42 (board), 2d ÷ d/42 = 84 (board, by click), "the d cancels — that's also why plugging in works" (+≈15 s; video net ≈ +5 s). Rendered, checked.
- Written solution wp27-g109: the 2ab/(a+b) check paragraph removed; "Method 2 · Balance" → "Method 2 · Algebra" (same d working).
- q-r26-t27-22: "Method 2 · Balance (averages)" → "Method 2 · Algebra" (route 3d, total time d/15, 3d ÷ d/15 = 45); the trap line no longer says "speeds must be weighted by time" — "Average speed is total distance ÷ total time, nothing else."
- q-r26-t27-21: the trap line no longer gives the 2ab/(a+b) formula ("Trap: 42 treats the two parts as equal distances; here the times are equal.").
- Card **mem-motion**, Average speed, row "Equal distances": "closer to the slower speed; check 2ab/(a+b)" → "closer to the slower speed (more time there); still total ÷ total".
- Kept: wp-108-after "Remember weighted averages? … the longer time does the pulling" (an intuition for WHY the answer sits near the slow speed, not a solving method).
`math_check.py 21 22 23 24 25 26 27 28 29 32` → PROBLEMS 0, WARNINGS 0, LAYOUT 0.
