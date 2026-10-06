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
