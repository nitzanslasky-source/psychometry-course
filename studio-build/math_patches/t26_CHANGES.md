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
