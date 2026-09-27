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
