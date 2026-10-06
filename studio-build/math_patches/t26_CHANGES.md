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
