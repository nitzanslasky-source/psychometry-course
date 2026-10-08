# Topic 26 – Work and rates: changes (course review 2026-09)

All answer keys were already correct. The changes add missing methods, make the boards clearer, clean up the text and rebalance the practice set.

## Counts
- Questions rewritten: 35. That is all 11 guided questions plus 24 practice questions. Every solution is now 2–3 short lines with numbers in TeX, with no ":" for division and no "so" in the middle of a sentence.
- Questions added: 12. That is 4 guided questions with solution videos and 8 practice questions (`q-r26-t26-01` … `-12`).
- Questions removed: 3 near-duplicates (p02, p14, p15).
- Videos added: 4 solution videos. Lesson slides added: 5, in 3 lessons. Slides added in solution videos: 2. About 20 existing slides were changed.
- Figures: none (topic 26 has no question figures).
- Practice: 27 → 32 questions, ordered easy → medium → exam-hard. 8 are exam-hard.

## New methods (each has a lesson slide, a guided question with a video, and practice)
| Method | Lesson slide | Guided question | Practice |
|---|---|---|---|
| Rate in percent → time ("fraction, flip it, multiply the time"; +25% rate → −20% time) | "Rate in percent" (Work, Rate and Time) | Q2: printer 20% faster, 60 → 50 min | new -05, p25, new -09 (hard) |
| Two workers: shortcut ab/(a+b), two equal workers → half the time | "Two-worker shortcut" (Working Together) | Q5: 10 h and 15 h → 6 h | p11 (shortcut added), new -06, new -10 (letters) |
| Sense check: together < the fastest alone, together ≥ fastest ÷ 2 | "Sense check" (Working Together) | Q5, Method 1 (eliminate first, no calculation) | Q12 (cleaners) solution |
| A worker joins or leaves midway (whole job − done = left; worker-days, or pick a job size) | "Joins or leaves" (Worker-Hours) | Q8: pipe A alone 3 h, then B joins | p22, p23, p26, new -07, -08, -12 (hard) |
| Average rate = total work ÷ total time (linked to averages in T25 and to motion in T27) | "Average rate" (Worker-Hours) | Q11: 60 parts at 30/h, then 60 at 20/h → 24 | p09, p10 (new), new -11 |
| Pick a job size = LCM of the times (default for weak students) | "One job = 1" line reworded; Q3 video mentions the LCM | Q3 Method 2, Q8 Method 1 | p22, p26 solutions |
| Plug in numbers for letter answers | Q1 video, new "Method 3 · Plug in numbers" slide | Q1 | p12, p17, -10 |
| General V rule (blank in Team/Time → V; blank in Work → upside-down V, with an example) | New "The V rule" slide in the Q6 (old Q4) video | Q6 | p05, p27 solutions |

Guided questions are renumbered automatically. The learn section is now Q1–Q8, and the advanced section is Q9–Q15.

## Lessons
- **Work, Rate and Time:** "work ÷ rate" instead of "work : rate" on the board. New slide "Rate in percent". The recap has a new line. The "One job = 1" slide now says: pick a job size = LCM. The triangle on slide 2 was already drawn (the student-view dump does not show figures, so the reviewer missed it).
- **Working Together:** new slides "Two-worker shortcut" and "Sense check". The recap now says when to use which method ("Nice common multiple → equalize times · otherwise fractions"). The closing line now says "Three questions next". "litres" → "liters".
- **Team Questions:** "Team questions need more time…" → "work ALWAYS sits in the middle — Team, Work, Time".
- **Work Time → Worker-Hours:** one name everywhere (video, board, memory card, Q7 and Q14 videos). New slides "Joins or leaves" and "Average rate". The recap was updated.

## Solution videos
- Q1: Method 1 renamed "Step by step". It says what the table is, and each "write" note names its row (the table was already on the slide). "Triple value" → "Method 2 · Rate × time" (x/y → 3x/y → × 4y = 12x). New "Method 3 · Plug in numbers".
- Q3 (inlets): new stem ("Two identical inlets each fill a tank in 8 hours…"). Clock times are now "9 a.m." / "3 p.m." instead of 09:00 / 15:00, so they don't look like a colon. The LCM is named.
- Q4 (orders): the two-worker shortcut was added to Method 2.
- Q6 (display boards): the V method now states the general rule. A new "The V rule" slide adds the upside-down V example. ":" → "÷".
- Q7 (path): "work time" → "worker-days".
- Q9 (scanners): "give to the poor one" → "the times two goes on the SMALLER side. Then both sides are equal." The stem no longer shows "high−speed" with a math minus.
- Q12, Q14, Q15: ":" → "÷" in every "Write …" note. Q14 Method 3 is now called "Worker-hours".
- "on screen" notes now match the rewritten stems. "memorise" → "memorize", "square metres" → "square meters".

## Memory card
Division uses ÷. New rows: rate % → time, pick a job size (LCM), two workers ab/(a+b) and equal workers → half, joins/leaves, average rate. The card now says when to equalize and when to use fractions. New tips: sense check, the general V rule, plug in numbers for letter answers.

## Practice
- Reworded: p01 ("the total number of boxes folded by Eva and boxes labeled by Max"), p26 ("A container is emptied by drain A…"), p07 / p21 / p25 / p19 (they now ask "how many hours/minutes", to match the bare-number choices).
- p12: "2q envelopes" → "n envelopes". The answer is nq/p; the solution checks it with numbers.
- p10: circle area (T33, far ahead) removed. The floor is now 600 m², half smooth and half rough, and the answer is 90 minutes. The average-rate trap (80) is one of the choices.
- Removed: p02 (copy of Q1), p14 (copy of Q13 Ava/Ben/Cleo), p15 (copy of Q9 scanners).
- New: -05 (rate −20%), -06 (find B from together), -07 (A leaves after 3 days), -08 (find A after a phase – hard), -09 (speed +50% and job +20% – hard), -10 (ab/(a+b) with letters), -11 (average rate), -12 (workers join; asks for the whole time – hard).

## For the teacher to decide
- Moving T26 right before T27 (Motion) is outside this patch and should be done in the course order. The new "Average rate" slide already points ahead to average speed.
- The "Sense check" rule is taught as "together ≥ fastest ÷ 2 (exactly half only if equally fast)". Please confirm that this wording works for the videos.
- The API cannot rename a video, so the patch renames Work Time → Worker-Hours by setting the video/title-slide fields directly. It also updates the stale "on screen" notes of pre-loaded questions directly.

## Pass 2 (2026-09-27, approved remove/restore plan + summary lesson)
**Removed:** nothing. The "Sense check" slide, its recap part and card tip stay (plan: KEEP).

**Restored (6, one of them moved):**
- wp26-p02 (printer B 3 times as fast, $12x$), wp26-p14 (third hose, $\frac1{10}$) and wp26-p15 (experts vs trainees, $\frac83$) are back in the practice; letters in TeX, solutions with the numbers.
- wp26-p12 is again the original "seal $2q$ envelopes" with its original choices (key $\frac{2q^2}{p}$); the "$n$ envelopes" version is dropped. Solution checked with numbers.
- wp26-p10 is again the original rough circular floor of radius 15 (key $\frac{3\pi}{4}$ hours). It uses circle area, so it is **moved to the Topic 33 foundation practice** (end of that section). The "600 m², half smooth and half rough" version stays in Topic 26 as new question **q-r26-t26-13** (exam-hard part).
- `solve-wp26-g093` (Question 1): the original "Method 2 · Triple value" slide is back as "Method 2 · Triangle value" (the name the course now uses; "÷" instead of ":"). The added slides follow as "Method 3 · Rate × time" and "Method 4 · Plug in numbers".

**Summary lesson (1 new video):** `r26-t26-summary` "Summary", at the end of "Further guided examples", right before the practice. Slides: Summary · The formula · Three relationships · Rate in percent · One job = 1 · Working together · Two workers · Team questions · Worker-hours · Average rate · Before you practice. Only content the Topic 26 lessons and guided solutions teach.

## 2026-10-05 cut repeats
Function `cut_repeats` (runs last). Each lesson is back to a short intro like the Hebrew course. If a question video in the same flow already teaches an idea, it is cut from the lesson. Ideas that no question teaches stay, or move into the question video that uses them as one spoken line plus one board item. Nothing in topic 26 is recorded. Questions, numbers, methods and the memory card are unchanged.
- **`wp-092` Work, Rate and Time**: 8 → 3 slides, 4.4 → 1.8 min. Kept: title, "The formula" (with the triangle) and "Rate has a time unit". The Hebrew theory lesson teaches exactly these two. Added the closing line "Now two questions. Try each one first — then watch the solution." Cut:
  - "Work = rate × time": the same drill as the triangle. Q1 method 3 does it.
  - "Three relationships": the direct ones are in Q1 method 1 (same time, triple rate → triple the samples; more time → more work). The inverse one is in Q2, the printer question. MOVED into Q2 `solve-q-r26-t26-01`: "The rule: when the work is fixed, faster means less time — inverse." + board "Work fixed: rate ×2 → time ×½ (inverse)".
  - "Rate in percent": taught in Q2 method 1. MOVED "the other way" there: "rate down twenty percent is times four fifths — so the time is times five quarters, up twenty-five percent." + board "Rate −20% → time ×5/4 = +25%".
  - "One job = 1": taught in Q3 `solve-wp26-g095` (one eighth of a tank per hour; method 2 uses the LCM, a 24-unit tank). ADDED there: "We don't know the tank's size — so call the whole tank one job." + board "One job = 1 → 8 hours: 1/8 per hour".
  - Recap.
- **`wp-094` Working Together**: 7 → 3 slides, 2.5 → 0.9 min. Kept: title, "Add the rates" and "Working against you" (the Hebrew intro). Added "Let's see it in three questions." Cut:
  - "Match the times": Q4 method 1 (equalize the times).
  - "Two-worker shortcut": Q4 method 2 and Q5 method 2 (times over plus). MOVED into Q5 `solve-q-r26-t26-02` method 2: "Two equal workers? Together they need half the time. And this shortcut is for two workers only — three workers, add the rates." + board "Equal workers → half the time · 3 workers → add rates".
  - "Sense check": Q5 method 1 (less than the fastest, more than half of it), and also Q4.
  - Recap.
- **`wp-097` Team Questions**: not cut. "Now remember the three relationships." → "Remember from the first questions:", because that slide is gone.
- **`wp-099` Worker-Hours**: 7 → 2 slides, 2.3 → 0.6 min. Kept: title and "What worker-hours are" (the Hebrew intro). Added "Let's see it in the questions." Cut:
  - "Jobs in phases": Q7 path question (18 × 8 + 12 × 7; "thirty workers never worked together").
  - "Joins or leaves": Q8 pipes (whole − done = left; the "whole pool from the start" trap).
  - "Average rate": Q11 `solve-q-r26-t26-04` (total work ÷ total time; the slow rate gets more time). This one is in "Further guided examples", the first question that uses it. MOVED there: "It's a weighted average — weighted by TIME. You'll meet the same trap with average speed." + board "Average rate: weighted by time".
  - "Matching units": Q10 `solve-wp26-g102` (hours become minutes). ADDED there: "Combine only matching units — convert first." + board "Combine only matching units".
  - Recap.
- Question videos got longer: q-r26-t26-01 0.8→1.1, g095 1.1→1.2, q-r26-t26-02 0.9→1.1, g102 1.2→1.3, q-r26-t26-04 0.8→0.9. **Net: −5.1 min.**
- No video said "as we saw in the lesson" about a cut idea. The summary lesson and the AI summary `r26-t26-summary` were not edited. Everything they recap is still taught, in the lesson slides that stayed or in the question videos.
- **Follow-up check (same day):** every cut idea re-checked against the video that now teaches it; nothing was lost, so no change. Work = rate × time forwards/backwards → the triangle slide (kept) + Q1 method 3. Direct relationships → Q1 method 1; inverse → Q2 (moved line). Rate in percent (+25% → −20% and back) → Q2 method 1 + moved "−20% → +25%" line. One job = 1 / LCM → Q3 (moved line + method 2). Match the times → Q4 method 1. Two-worker shortcut (4 h and 6 h → 2.4 h, the same example) → Q4 method 2 + Q5; equal workers / three workers → Q5 (moved). Sense check (less than the fastest alone, more than half of it, cross out first) → Q5 method 1, also Q4 and Q8. Jobs in phases (don't mix team sizes) → Q7 path. Joins or leaves (whole − done = left, LCM for different rates, "left or whole?" trap) → Q8 pipes. Average rate (total ÷ total, not the plain average, weighted by time) → Q11 (moved line). Matching units → Q10 (moved line).

## 2026-10-06 new exam methods
Function `add_methods` (runs last, after `cut_repeats`). Nothing in topic 26 is recorded. Check: `python3 math_check.py 26 32` → 0 problems, 0 warnings, 0 layout problems.
- **New lesson `r26-t26-factors` "Compare by Factors" (3.3 min)**, at the end of "Further guided examples", right before the Summary. Slides: Two things change (Lia works 3/4 of Ben's hours, 2/3 per hour, Ben 8 days → per day 1/2 → 16 days) · The rule (new = old × every factor that changed; same way as is, opposite way flipped; shared cancels; 8 × 4/3 × 3/2 = 16) · The V is one case (Question 6's ratio method = this rule; the V = the rule for a 3-column table) · When it fails ("2 more an hour" is not a factor → letter + equation; word cue "times / as many as / percent of" vs "more than") · Remember.
- **New guided question `q-r26-t26-21`** (Question 16, right after the lesson) + solution video `solve-q-r26-t26-21` (1.5 min): budget +20%, price ×1.5, 30 notebooks → 30 × 6/5 × 2/3 = **24** (choice 3). Traps: 54 (price not flipped), 21 (percents added), 20 (budget forgotten). Slides: Method 1 · Compare by factors, The traps.
- **Catching up = gap ÷ difference in rates**: new slide 4 "Same idea: catching up" in the Q10 video `solve-wp26-g102` (queue question; 1.3 → 2.1 min): printer normally 6 h/day, down 5 days → 30 h behind; now 16 h/day = 10 more a day → 3 days; trap 30 ÷ 16; linked to chases in Topic 27.
- **Card `mem-work-rate`**: new row "Two or more things change (only relations)" after the Team row; new row "Catching up"; new tip "A fixed amount more is not a factor → equation".
- Nothing that the 2026-10-05 cut removed was re-added (the Summary lesson is unchanged; its "Two changes multiply" line already matches).

## 2026-10-06 practice: new methods
Function `practice_methods` (runs last in `apply`). One extra line is added at the end of each written solution; the existing lines are kept. Nothing is recorded. "Catching up = gap ÷ difference in rates" did not fit any practice question (none has a fixed gap followed by a faster rate). Questions whose written solution already is the factor rule (q-r26-t26-05, q-r26-t26-09, wp26-p25) were not given a duplicate line.
- `wp26-p05` (4 clerks, 18 in 6 min → 3 clerks, 27): Method 2 · Compare by factors: 6 · 3/2 · 4/3 = 12.
- `wp26-p27` (8 machines, 960 in 3 h → 1,600 in 4 h): Compare by factors: 8 · 5/3 · 3/4 = 10.
- `wp26-p17` (M scanners, L pages → D scanners, 3 hours): Compare by factors: L · D/M · 3.
- `wp26-p12` (p envelopes in q min → 2q envelopes): Compare by factors: q · 2q/p.
- `wp26-p13` (5 workers, 8 crates, 2 h → 1 worker, 1 crate): Compare by factors: 120 · 1/8 · 5 = 75.
- `wp26-p16` (4 slow flashes = 7 fast flashes): Compare by factors: 3/5 · 4/7 = 12/35.
- `q-r26-t26-11` (2 h at 30, 3 h at 40): Method 2 · Percent shares as weights (by hours): 30 + 0.6 · 10 = 36.
- Every line checked in python. Check: `math_check.py 26 32` → 0 / 0 / 0.

## 2026-10-06 renumber pass
So the English course does not look like the Hebrew one: every Hebrew-derived question has a new story (new objects,
names and setting) and new numbers. The idea, the trap, the level and the methods stay the same (V method and upside-down V,
ratios, adding / subtracting rates, one job = 1, pick a job size (LCM), equalize the times, two-worker shortcut, sense
check, worker-hours, merge two workers, plug in numbers, estimate, compare by factors). Every guided solution video is
rewritten to match (speech, draw cues, tables, title-slide lines, video titles, pre-loaded question notes). Nothing in
Topic 26 is recorded (checked ~/Documents/Course.recordings), so nothing had to be kept. Function `renumber_pass(M)` in
t26.py runs last (after `cut_repeats`, `add_methods`, `practice_methods`); the "Method 2 · Compare by factors" lines that
practice_methods added (p05, p12, p13, p16, p17) are rewritten with the new numbers, the "One job = 1" board item that
cut_repeats put into old Q3 now says 15 hours, and the Compare-by-Factors lesson slide "The V is one case" quotes the new
team question (3 gardeners, 40 trees, 5 hours → 4 gardeners, 96 trees: 5 × 96/40 × 3/4 = 9).

**Counts:** 11 guided questions renumbered (all Hebrew-derived: wp26-g093 … g105b) with their 11 solution videos rewritten;
19 practice questions renumbered (wp26-p01 … p09, p11 … p20; p10 lives in topic 33 and was not touched). Lesson examples
renumbered: 4 slides (wp-092 #3 rate example, wp-094 #2 add the rates, wp-094 #3 working against, wp-099 #2 worker-hours)
plus the factors-lesson slide and the memory-card tip (75 minutes = 1.25 h → 40 minutes = ⅔ hour, not 0.4).
Practice: 35 → 25. English-made items (guided q-r26-t26-01 … 04 and -21, the summary, the factors lesson, the catching-up
slide, the kept extras and September items) keep their numbers.

**Order:** unchanged on purpose. The learn order follows the lessons (Q3 tank-with-outlet teaches "one job = 1", which Q4's
fraction method uses — swapping them would be "used before taught"); the advanced order already goes medium → high as in
the Hebrew. Correct-answer positions moved in 9 of 11 guided questions.

**Practice clean-up (35 → 25):** no copies in this topic (copies list empty). Extra-bank kept (3): p24 (add the rates,
warm-up), p25 (rate +25% → time −20%), p23 (workers leave, worker-days). Removed extras: p21 (pump + leak = guided Q3 /
p19), p22 (equal worker joins = guided Q8), p26 (drain A, then B joins = guided Q8), p27 (V with the team blank = p05 /
guided Q14). September items kept (3, types the Hebrew practice does not have): q-07 (a worker with a different rate
leaves), q-08 (together, then one stops — find its rate), q-09 (two percent changes multiply). Removed: q-05 (rate −20% =
p25), q-06 (find B from together = p18), q-10 (ab/(a+b) with letters = guided Q4/Q5 shortcut), q-11 and q-13 (average-rate
trap = p09 and guided Q11), q-12 (workers join, whole job = p23 and guided Q8). Order easy → medium → exam-hard.

**Also:** old Q4 title line "Two machines" → "Two printers"; old Q3 "Two pumps fill" → "Two hoses fill, one pipe empties";
Q15 title line "Last question." → "The last team question." (a factors question follows it). New trap lines in Q3 (forgot
the outlet → 2:30 p.m.) and Q9 (doubling the wrong side → 1).

**Checks:** every key recomputed in Python with exact fractions (all match); letter questions (g093, p02, p12, p17)
brute-checked with numbers — exactly one choice fits; every "circle choice" / "Choice N" in the 16 solution videos agrees
with the key; traps still among the choices (8x added factors; 2:30 p.m. no outlet; 12 forgot the team and 16 team not
flipped; 400 = (14 + 6) × 20; 1 doubled wrong side; 72 units mix-up; 132 = A alone and 66 = half; 1/9 all three; 26 = all
workers; 18 = half the sheep and 6.75 wrong direction; 12.5 average of rates; 6⅔ fast printer as ordinary; 48 pipe-hours;
3/10 wrong side). Compared with base-v18 AND the Hebrew subtitles: no new question lands back on the old or the Hebrew
numbers / objects (e.g. Hebrew pool 6 h / 9 h at 8:00, beer 3 h / 2 h, carpenters 4 / 20 / 3, road 20 × 10 + 15 × 10,
scanners 4 / 6, mole and gardener 75 minutes, mowers 2 h / 3 h, 6 h / 12 h, carpenters table / chair, water tower);
p03 and p13 were changed again after the duplicate check (first versions shared numbers with base). Duplicate check
against all questions, lesson boards and cards of topics 1–38: only incidental shared small numbers, no equal question.
Each new question compared side by side with its original: same type, same condition kind ("twice" stays a multiple,
"x and y positive" kept, two-phase, two-team, leaves/joins unchanged), same number of steps. No quadratic trinomial.
`python3 math_check.py 26 32` → PROBLEMS 0, WARNINGS 0, LAYOUT 0. Rendered all 11 solution videos, the factors lesson
and the three changed lessons and looked at them.

| id | old (base / Hebrew-derived) | new | answer |
|---|---|---|---|
| wp26-g093 (Q1) | robot x samples / y min, rate ×3, 4y min | volunteer x flyers / y min, rate ×3, 5y min | 15x (3) |
| wp26-g095 (Q3) | 2 inlets 8 h, drain 12 h, 9 a.m. | 2 hoses fill a pond in 15 h, outlet 20 h, 7 a.m. | 7 p.m. (2) |
| wp26-g096 (Q4) | machines 4 h and 6 h → minutes | printers 6 h and 10 h → minutes | 225 (2) |
| wp26-g098 (Q6) | 5 workers 30 boards 4 h; 8 workers 72 | 3 gardeners 40 trees 5 h; 4 gardeners 96 | 9 (2) |
| wp26-g100 (Q7) | path 18 × 8 + 12 × 7 | park fence 14 × 9 + 6 × 11 | 192 (3) |
| wp26-g101 (Q9) | 3 fast = 2 × 9 standard scanners | 5 large = 2 × 10 small dishwashers | 4 (2) |
| wp26-g102 (Q10) | +24/h, 35 per 75 min, 50, 5 h | bakery: +18 orders/h, 15 per 40 min, 60, 4 h | 42 (3) |
| wp26-g103 (Q12) | cleaners 360 m²/3 h, 40 m²/2 h, 140 m² | polishers 200 m²/4 h, 30 m²/6 h, 110 m² | 120 (1) |
| wp26-g104 (Q13) | Ava, Ben, Cleo 8 h; two 16 h | Omar, Priya, Sam 9 h; two 18 h | 1/18 (3) |
| wp26-g105 (Q14) | 8 makers cabinet 6 h, 9 bench 8 h, 24 h | 12 workers stage 2 h, 14 seating 4 h, 8 h | 10 (2) |
| wp26-g105b (Q15) | feed 240 animals 6 days → 90 | hay 200 sheep 9 days → 150 | 12 (1) |
| wp26-p01 | Eva 4/6 min, Max 5/8 min, 24 min | Nora 3 gifts/5 min, Theo 7/10 min, 30 min | 39 (3) |
| wp26-p02 | printer x/h, B ×3, 4 h | oven x loaves/h, B ×4, 5 h | 20x (3) |
| wp26-p03 | 6 small or 4 large/h; 3 + 5 | tailor 12 pants or 2 coats/h; 8 + 3 | 2 h 10 min (2) |
| wp26-p04 | 7 packers 96 more than 3 | 9 sewing machines 140 more than 4 | 28 (3) |
| wp26-p05 | 4 clerks 18 in 6 min; 3 clerks 27 | 6 cashiers 45 in 10 min; 4 cashiers 54 | 18 (2) |
| wp26-p06 | machine 480/h, person 1 per 12 min | machine 360 jars/h, worker 1 per 4 min | 24 (3) |
| wp26-p07 | 4 pumps 9 h + one twice as fast | 5 printers 8 h + one three times as fast | 5 (2) |
| wp26-p08 | 5 × 8 + 6 × 10 worker-days, 10 workers | 4 × 9 + 8 × 6 painter-days, 12 painters | 7 (3) |
| wp26-p09 | 24 plain or 8 decorated mugs, 48 each | 20 small or 5 large bowls, 40 each | 8 (2) |
| wp26-p11 | pipes 6 h and 12 h | pumps 5 h and 20 h (reservoir) | 4 (3) |
| wp26-p12 | p envelopes / q min, 2q envelopes | m bottles / n min, 3n bottles | 3n²/m (2) |
| wp26-p13 | 5 workers 8 crates 2 h → one crate | 3 workers 12 boxes 3 h → one box | 45 (3) |
| wp26-p14 | 3 hoses 5 h, two 10 h | 3 sprinklers 4 h, two 12 h | 1/6 (2) |
| wp26-p15 | 3 experts = 2 × 4 trainees | 5 senior cooks = 2 × 3 junior cooks | 6/5 (2) |
| wp26-p16 | signals 4 vs 7 cycles, 3/5 s | drummers 3 vs 8 beats, 2/3 s | 1/4 s (3) |
| wp26-p17 | M scanners L pages, D scanners 3 h | K printers P pages, N printers 5 h | 5NP/K (1) |
| wp26-p18 | 4 painters 6 h, with 5th 4 h | 3 cleaners 8 h, with 4th 6 h | 24 (3) |
| wp26-p19 | tap 10 h, 3 drains 4 h, 4 taps × 15 h | pipe 8 h, 2 drains 5 h, 3 pipes × 16 h | 60 (2) |
| wp26-p20 | fast ×3, together 12 h | new robot ×4, together 10 h | 50 (4) |
| lesson wp-092 #3 | 18 labels in 3 min → 6 per minute | 45 bottles in 5 min → 9 per minute | – |
| lesson wp-094 #2, #3 | 4 + 7 = 11 per minute; 9 in, 4 out → +5 | 5 + 8 = 13; 12 in, 5 out → +7 | – |
| lesson wp-099 #2 | 3 workers × 4 h = 12 | 5 workers × 6 h = 30 | – |
| factors lesson #4 / g098 V-rule example | 5 · 30 · 4 → 8 · 72; upside-down V 8 · ? · 6 = 72 | 3 · 40 · 5 → 4 · 96; upside-down V 4 · ? · 6 = 64 | – |
| card tip | 75 minutes = 1.25 hours | 40 minutes = ⅔ hour (not 0.4) | – |

## 2026-10-06 review
Independent review of the renumber pass (built with and without `renumber_pass`, compared every changed question, video,
lesson slide and card; keys recomputed; Hebrew subtitles work section checked: pool 6 h / 9 h at 8:00, beer 3 h / 2 h,
carpenters 4·20·3 → 6·60, road 20×10 + 15×10, scanners 4 = 2×6, mole 20/h + gardener 30 per 75 min, mowers 300/2 h + 50/3 h,
Aviva–Batya 12 h / all 6 h, table 10/3 h + chair 9/5 h in 15 h, 220 for 5 days → 100 — no new question lands on them).
All 11 guided + 19 practice keys correct, one correct choice each, traps still among the choices; V method, upside-down V,
compare-by-factors and catching-up content work with the new numbers. Practice removals (35 → 25) checked.
Fixed (new function `rv_fixes`, runs at the end of `renumber_pass`):
- `solutionVisual` tables of g093, g096, g098, g105 still had the old stories/numbers (×4 → 12x; machines 3/2/5 in 12 h;
  workers 5·30·4 → 8·72 "Boards"; "Cabinet"/"Bench" 48 + 72 = 120) → rewritten to the new questions.
- g095 video slide 3 title "Method 2 · Pick a tank size" → "Pick a pond size" (the question is about a pond now).
- p16 (in `rn_practice_questions`): 3 slow beats / 8 fast beats / 2/3 s → 1/4 made the slow total a whole number (2 s),
  easier than the original 4 × 3/5 = 12/5 → 12/35. Now 5 beats / 8 beats / 2/3 s → 10/3 ÷ 8 = 5/12; distractors 16/15
  (wrong flip), 8/5, 5/8; Method 2 line updated.
`python3 math_check.py 26 32` → PROBLEMS 0, WARNINGS 0, LAYOUT 0. Rendered g095 and g098 videos and looked.

## 2026-10-07 methods spread
Function `spread_methods(M)` in t26.py runs last (after `renumber_pass`). Every question and every guided video was checked;
each line was verified with numbers. Questions that already show the method (Q1, Q2, Q6, Q16, and the practice lines added
2026-10-06 on p05, p12, p13, p16, p17, p25 …) are not touched. Nothing in topic 26 is recorded.
- **Q10 `wp26-g102` (bakery queue)** — "Method 3 · Catching up (difference in rates)": 22.5 − 18 = 4.5 fewer an hour, 4 hours → 60 − 18 = 42. Written line only (the video already has the catching-up slide).
- **Q11 `q-r26-t26-04` (average rate)** — "Method 3 · Percent shares as weights" (the hours are the weights): 20 + 0.4 · 10 = 24.
  Written line + new video slide 4 "Method 3 · Shares as weights" (+0.35 min; it finishes the "weighted by time" estimate of Method 2 exactly).
- **Q15 `wp26-g105b` (hay)** — "Method 2 · Compare by factors": sheep × ¾ → flip → 9 · 4/3 = 12. Written line only.
- **Practice p09 (potter)** — "Method 2 · Percent shares as weights" (the days are the weights): 5 + 0.2 · 15 = 8.
- **Practice p23 (two workers leave)** — "Method 2 · Compare by factors": 10 · 3/2 = 15.
- **Practice p07 (fast sixth printer)** — "Method 2 · Compare by factors": team × 8/5 → flip → 8 · 5/8 = 5.


## 2026-10-07 study-plan order
Function `plan_order_fix` (runs LAST). Students follow the study plan (`src/lib/planData.ts` ORDER), not topic numbers; named methods were checked against the plan rank of their teaching topic.
- wp26-g105b: "Method 2 · Compare by factors" → self-contained shortcut with the why (it comes before the lesson r26-t26-factors inside this topic).
`python3 math_check.py 5 7 10 21 22 25 26 28 30 31 33 37 32` → PROBLEMS 0, WARNINGS 0, LAYOUT 0.

## 2026-10-08 Hebrew points restored
Audit only — nothing to restore, no code change. The teacher's Hebrew lessons for this topic ("בעיות הספק תאוריה": formula and triangle, rate vs work ("not 4 — 4 per minute"), the x-in-y-minutes ratio example, the three direct/inverse relationships "keep them in mind for team questions"; combined rate: add rates, the one working against gets a minus (dishes), reading 2/9 as "2 pools in 9 hours", equalize the times with a common multiple before adding, hours → minutes; team questions: how to spot them, "considered hard, need understanding", ratios method, the V method with work in the middle and the upside-down V; worker-hours: one worker alone, the contractor paying wages, phases) — 16 points — were each checked against the current course. Every point is still said in the kept lesson slides (wp-092, wp-094, wp-097, wp-099) or in the question video right after (Q1 wp26-g093 direct relationships + ratios, Q2 q-r26-t26-01 the inverse rule, Q3 wp26-g095 one job = 1 and "one twelfth = one pond in twelve hours", Q4 wp26-g096 equalize the times, Q6 wp26-g098 ratios + V + the V rule, Q7 wp26-g100 phases + the contractor). The slides the cut removed from these lessons that are not in the Hebrew lesson (two-worker shortcut, sense check, jobs joining/leaving, average rate, matching units) were our additions and are taught in the questions.
