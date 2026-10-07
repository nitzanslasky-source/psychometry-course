# Topic 23 — Percentages: changes

Patch: `math_patches/t23.py`. Check: `python3 math_check.py 23` shows 0 problems, 0 warnings and 0 layout problems.

## Summary
- Questions: all 37 existing questions were rewritten (text, TeX, solutions with numbers). 14 questions were added: 5 guided questions with solution videos and 9 exam-level practice questions. No questions were removed.
  The topic had 10 guided and 27 practice questions. It now has 15 guided and 36 practice questions.
- Lesson "Calculating Percentages": 5 slides changed and 1 slide added ("Thirds and families").
- Lesson "Percent of a Percent": 2 slides changed and 2 slides added ("Multipliers", "Up and down").
- New lesson video: "Percent Traps and Shortcuts" (7 slides, about 3 minutes).
- New solution videos: 5 (for the new guided questions). 4 existing solution videos changed.
- Memory card "Percentages to know" was updated and moved. New card: "Percent traps and shortcuts".
- Figures: this topic has no question figures. Nothing to fix.

Guided questions are numbered automatically in course order. The new multiplier question is now Question 6. The old Questions 6–10 are now Questions 7–11. The new questions after the traps video are Questions 12–15.

## 1. Wrong or confusing teaching (fixed)
- **Method name:** the lesson and the card called the ratio method "the triple value". Topic 22 calls it "the triangle value". Now it is "triangle value" everywhere.
- **Lesson 1, slide 4:** the old line "Can't halve it precisely? Half of thirty-two is sixteen — so it's sixteen and a bit" is gone. The new slide 5 says: half of 33 is 16½, half of ⅓ is ⅙, so ⅙ = 16⅔%.
- **Q8 video (now Q9), method 2:** choice 1 was skipped. The teacher now shows it: the percent is multiplied by ⅔ and the whole by 3/2, so it is balanced.
- **Q7 video (now Q8), method 2:** the tongue-twister is now "a percent of b equals b percent of a — you can swap them".
- **Q10 (now Q11):** "litres" became "liters" (American spelling, as in the question). The video no longer says "Last question of the set". Other spelling: "practised" became "practiced", and "colour" became "color".

## 2. Methods added
**Lesson 1 "Calculating Percentages"**
- Slide 4 was split into two slides. Slide 4 covers halves and tenths. The new slide 5, "Thirds and families", covers ⅓ and ⅙, then 3/8, 5/8, 3/5 and 7/20 on the board.
- Slide 6 (percent equation): the teacher says the letter-inside-the-percent example is exam level ("come back to it after the guided questions").
- Slide 7 (equal ratios): "the triangle value from the ratio lesson". The two ratio tables (percent | amount) were already on the board. The teacher now also names the two columns.
- Slide 9 (more tools): the **change rule** is now on the board: change in % = change ÷ original × 100 (80 → 100: 20/80 = 25%).
- Recap: adds "Change: divide by the ORIGINAL" and uses "Triangle value".

**Lesson 2 "Percent of a Percent"**
- New slide 4, **Multipliers**: up x% is ×(1 + x/100), down x% is ×(1 − x/100). Two changes: multiply the factors. Examples: +10% twice = ×1.21, so +21%. −25% then −20% = ×0.6, so a 40% loss.
- New slide 5, **Up and down**: +20% then −20% = ×0.96, a 4% loss, in either order. The rule: up p% and down p% always loses p²/100 %. For strong students: any two changes give a + b + ab/100 (+25 and −20 give 0).
- "Working backwards" slide: adds 96 ÷ 0.8 = 120.
- Recap: adds "Several changes? Multiply the factors".
- The memory card now comes after Question 1, because it lists the percent tree, which Question 1 teaches.

**New lesson video "Percent Traps and Shortcuts"** (after the old Q10, in "Further guided examples"):
1. **"More than" or "of"?** 150% of 80 = 120 = 50% more than 80. 150% more than 80 = 200. Rule: p% more than = (100 + p)% of.
2. **Percentage points:** a pass rate of 20% → 25% is up 5 percentage points, and up 25%.
3. **Mixtures:** find what stays the same (add water → the salt stays). Example: 200 g at 10% salt, add 50 g of water to get 8%.
4. **Letters in the choices: plug in numbers** (not 0 or 1, and a different number for each letter). If two choices match, try new numbers.
5. **Estimate and test:** 90 out of 320 is between 25% (80) and 30% (96). Test a round choice: 150 × 1.2 = 180.
6. Recap.

**New guided questions** (each one has a solution video):
- Q6 `q-r26-t23-01`: +25% then −12% → 10% higher. Methods: multipliers (1.25 × 0.88 = 1.1), plug in 100, and a + b + ab/100.
- Q12 `q-r26-t23-02`: pass rate 40% → 50% means the number of students who passed rose 25% (the trap is 10%). Methods: plug in 100, and the multiplier 50/40.
- Q13 `q-r26-t23-03`: desk = 150% of the chair, table = 150% more than the chair → the table is 66⅔% more than the desk. The video goes through each trap choice.
- Q14 `q-r26-t23-04`: mixture. 300 g at 20% sugar → add 100 g of sugar to reach 40% (the water stays at 240 g). Methods: what stays, and test the choices.
- Q15 `q-r26-t23-05`: letters. N students, g girls, 25% of the girls play chess → 25g/N %. Methods: plug in numbers (N = 200, g = 80), and build the expression.

**Memory cards**
- "Percentages to know": "triangle value". New rows: "Change in percent" and "Multiplier". New tips: the p²/100 rule and a + b + ab/100.
- New "Percent traps and shortcuts" card after the traps video: more than vs of, percentage points, mixtures, plugging in numbers, estimating, testing the choices.

## 3. Text (every question)
- All math is in $TeX$. Letters in stems and choices are in TeX (Q8/Q9 "$10\%$ of $6x$", and more).
- There is no ":" for division anywhere (p08, p17, p23, p25, p26). Only real ratios (p14, p18) use ":", and the solution uses the word "ratio".
- p08: the two given equations are stacked in `\begin{cases}`.
- Every solution shows the numbers (the guided solutions used to be words only). No "so" in the middle of a sentence to mean "therefore" (p05, p10, p12).
- Solutions use the taught methods and add the shortcuts the review asked for:
  - p03: 96 = 2⁵·3, so each ×3/2 uses up one factor 2, and review 6 is the first that is not a whole number.
  - p17: an estimate between 25% and 30%.
  - p27: 85% = 306, so 5% = 18 and 100% = 360, or test 360.
  - p16, p18, p20: a check by plugging in numbers.
  - p22: the p²/100 rule.
  - p10, p24, p07: multipliers.
  - p23: "the salt stays".
- p21 repeated the lesson example (16% of 25). It is now 28% of 75 = 21 (swap: 75% of 28).
- p03 wording: "not a whole number" instead of "no longer an integer number of credits".
- The titles of the solution videos now match the rewritten stems.

## 4. Practice
- 9 new exam-level questions:
  - `-06`: 10% growth for 3 years = 33.1%
  - `-07`: percentage points, statements I/II
  - `-08`: a rate from 5% to 4% is a 20% fall
  - `-09`: 300% more than = 400% of
  - `-10`: 120% → 150% of the original = a 25% rise
  - `-11`: remove water from a drink
  - `-12`: mix two drinks (16%, not the 15% average)
  - `-13`: work backwards: +20% then −25% gives 180, from 200
  - `-14`: letters: x(1 − p²/10000)
- The practice section is now ordered easy → hard: first straight calculations, then percent-of-a-percent, then percentage points and wording traps, then multipliers, mixtures, letters, and finally p03.
- Mixture question p23 is kept, because mixtures are now taught.

## For the teacher to decide
- Mixtures are taught here, in one slide, one guided question and 3 practice questions. No other topic teaches mixtures. If mixtures should become a full topic later, this block can move there.
- The a + b + ab/100 formula is presented as "for strong students". Weak students can keep using plug in 100 and multipliers.

## Pass 2 (teacher-approved plan, 2026-09-27)
**Removed** (percentage points / percent change of a rate - not on the real exam and not in the original course):
- Lesson "Percent Traps and Shortcuts": the slide "Percentage points", its sidebar entry and its recap line. The intro now says "two traps", and the recap says "Three questions next".
- Card "Percent traps and shortcuts": the row "Percentage points"; the intro now says "Two traps".
- Guided question `q-r26-t23-02` (pass rate) and its solution video. The guided questions after it are renumbered (now Questions 12-14).
- Practice `q-r26-t23-07` and `q-r26-t23-08`.
- `q-r26-t23-10` (kept): its solution no longer uses the words "percentage points". The trap line now says the rise of 30 is measured against 120, not against the original 100.

**Restored:**
- `wp23-p21`: the original "What is 16% of 25?" (2 / 6 / 8 / 4, key 4), in TeX with a numeric solution. The "28% of 75" version stays as a new practice question `q-r26-t23-15` (right after it).
- Lesson "Calculating Percentages", slide "Thirds and families": the original line "Can't halve it precisely? Half of thirty-two is sixteen — so it's sixteen and a bit." It comes right before the exact value (16½ + ⅙ = 16⅔).

**Summary lesson added:** `r26-t23-summary` "Summary: Percentages" (about 3.4 minutes), at the end of "Further guided examples", right before the practice.
Slides: Summary · The percent formula (percent = over 100, "of" = times, p/100 × whole = part, the swap) · Fractions to know · Equal ratios ("multiply along the diagonal, divide by what's left") · The 10% method · Change in percent (divide by the original, working backwards) · What is my 100%? (plug in 100, the whole after "of"/"than", each new percent sits on the new amount, when 100 fails) · Multipliers (several changes, up p and down p, the percent tree) · Traps and shortcuts ("more than" vs "of", mixtures, plug in numbers, estimate / test a choice) · Before you practice ("What is my 100%? It can change when there are several stages", "of" or "more than", divide by the original, what stays the same in a mixture, plus the common traps).

## 2026-10-05 cut repeats
Function `cut_repeats` (runs last). "Percent Traps and Shortcuts" is back to a short intro: every idea that the three question videos right after it teach is cut from the lesson; what no question teaches stays, and small rules move as one spoken line + one board item into the question video that uses them. Nothing in topic 23 is recorded. Questions, numbers, methods and the memory card `mem-r26-t23-traps` are unchanged.
- **`r26-t23-traps`** Percent Traps and Shortcuts: 6 → 2 slides, 2.6 → 0.6 min. Title now: "The exam loves a few percent traps. We'll meet them in the questions. First, one shortcut no question shows: estimate." Kept slide "Estimate" (what percent of 320 is 90 → between 25% and 30% → choice 2), because no question video teaches estimating; it ends "Three questions next. Try each one first. Then watch." Sidebar: "Estimate".
- Cut "More than or of?" → Q12 `solve-q-r26-t23-03` (desk 150% of, table 150% more). MOVED the general rule there: "The rule: p percent more than a number is a hundred plus p percent of it." + board "p% more than = (100 + p)% of".
- Cut "Mixtures" (add water, salt stays) → Q13 `solve-q-r26-t23-04` (add sugar, water stays). MOVED the other direction there, at the start of method 1: "Mixtures: always ask what stays the same. Add water, and the sugar stays. Add sugar, and the water stays." + board "Mixtures: find what stays the same".
- Cut "Letters: plug in numbers" → Q14 `solve-q-r26-t23-05` (plug in N = 200, g = 80). MOVED the number-choice rules there: "Easy numbers: not zero, not one, a different number for each letter. If two choices hit the target, pick new numbers and test only those two." + board "Not 0, not 1, different numbers · two hit? new numbers".
- Cut the second half of "Estimate and test" (after a 20% rise the price is 180 → test 150) → Q13 method 2 tests the round choice (100). Recap cut.
- Question videos: Q12 1.2 → 1.3, Q13 1.2 → 1.3, Q14 1.0 → 1.2 min. **Net: −1.6 min.**
- Unchanged: "Calculating Percentages" and "Percent of a Percent" (long like the Hebrew B56/B57 theory; not flagged), the summary lesson. No video said "as we saw in the lesson" about a cut idea. AI summary `r26-t23-summary` not edited; its "Traps and shortcuts" slide recaps ideas that are still taught (now in Q12–Q14 and the Estimate slide).
- Follow-up check (same day): every idea on the cut slides has a named home, so no change was made. "150% of 80 = 50% more than 80 = 120" and "150% more = 200" → Q12 (the same of / more than contrast, the rule on the board, and the choice-4 trap). Salt-water example (add water, salt stays; 1% → whole; minus the old total) → Q13 method 1 (the same steps with sugar, plus the moved add-water line). "What percent of a is b" plug-in → Q14 method 1, and part ÷ whole × 100 → Q14 method 2. "After a 20% rise the price is 180 → test 150 × 1.2" → test a round choice: Q13 method 2. Undoing a rise or fall: "Percent of a Percent" slide "Working backwards" (96 = 80% → 120) and Q10 tank. Multiplier ×1.2: "Percent of a Percent" slide "Multipliers".

## 2026-10-06 new exam methods
Function `add_methods` (runs last, after `cut_repeats`). Teacher-approved methods found by solving the real exams. Nothing in topic 23 is recorded. Teacher guide: scratchpad `guide/t23-t25.md`.
- **The flip rule** (6 real exam questions). "Calculating Percentages" `wp-052`: 2 new slides before the recap. Slide 10 "Same part: flip": 40% of A = 15% of B → ratio A : B = 15 : 40 = 3 : 8, with the reason (big percent needs a small whole; 0.4A = 0.15B → A/B = 0.15/0.4), the check A = 3, B = 8 → 1.2 = 1.2, the link to topic 22 ("four mugs cost the same as three plates → 3 : 4, reversed"), fractions (2/3 of A = 4/5 of B → 6 : 5), and the limit (amounts must be EQUAL; "6 more than" → no flip, write the equation). Slide 11 "Same whole: keep": a = 50% of b, c = 125% of b → c : a = 125 : 50 = 5 : 2 (250%), board rule "Same PART → flip · Same WHOLE → keep". Sidebar + actives updated. Lesson 6.6 → 9.2 min.
- **New guided question `q-r26-t23-16`** (now Question 10, right after Q9 "not equal to 15% of 4x", the inverse-ratio question): library, 600 novels and textbooks, 45% of the novels = 30% of the textbooks → how many novels? Choices 360 / **240** / 300 / 180, key 2. Check: N : T = 30 : 45 = 2 : 3, 5 parts = 600 → N = 240; 45% of 240 = 108 = 30% of 360 ✓. Traps: 360 (no flip), 180 (30% of the total). Solution video `solve-q-r26-t23-16` (1.9 min): Method 1 the flip rule (why it flips, parts), slide 2 check and the traps. Questions 10–14 after it are renumbered 11–15 automatically; all "Advanced Percentages" sidebars now list Question 2–15.
- **The arrow map** (~13 real questions). "Percent of a Percent" `wp-053`: 2 new slides after "Working backwards". "The arrow map": each "is p% of / more / less than" sentence = an arrow from the whole to the other one, multiplier on it; along ×, against ÷; x is 20% more than y → y = x ÷ 1.2 = 5/6 = 83⅓% of x (trap 80%). "Walk the path": P = 40% of Q, R 25% more than Q → R/P = 1.25 ÷ 0.4 = 3.125 = 312.5%, check with Q = 100 (40, 125), "plug in 100 still works — the map is a second picture", limit (a fixed amount added is not a multiplier), rule "Answer = the product along the path". Sidebar + recap active updated. Lesson 5.5 → 8.3 min. "Plug in 100" is unchanged.
- **Card `mem-percent`** (Methods table, after "Multiplier"): rows "Flip rule" (3 : 8 example + same whole → keep, 125 : 50) and "Arrow map" (y = x ÷ 1.2 = 83⅓%, not 80%).
- **Card `mem-r26-t23-traps`**: new rows "Fee or tax on top: divide, don't take 75%" (paid 100 with 25% tax → 100 ÷ 1.25 = 80, not 75; check 80 · 1.25 = 100) and '"Rose BY" or "became"?' (×3.75: became 375%, rose by 275%). Intro now "Traps the exam loves, and shortcuts that save time." Tip "not 0, not 1" softened: usually avoid 0 and 1, but if 0 / "nothing changes" makes the answer obvious use it (k new students join → at k = 0 the change must be 0 → only that choice survives); if two survive, plug in a second number.
- Same softer wording where it was spoken: Q15 (was Q14) `solve-q-r26-t23-05` slide 2 ("Easy numbers: usually not zero or one, and a different number…" + board "Usually not 0 or 1, different numbers · two hit? new numbers") and the summary `r26-t23-summary` ("Usually not zero or one, and a different number for each letter.").
- Nothing that `cut_repeats` cut was re-added. Check: `math_check.py 23 32` → 0 / 0 / 0; new slides rendered and looked at.

## 2026-10-06 practice: new methods
Function `practice_methods` (runs last in `apply`). One extra line is added at the end of each written solution; the existing lines are kept. Nothing is recorded.
- `wp23-p26` (worker 25% more than trainee → trainee ?% lower): Method 2 · Arrow map: ÷1.25 = ×0.8 → 20% lower.
- `wp23-p14` (p% = 90, q% = 150 of the same balance): Method 2 · Flip rule, same whole → keep: p : q = 3 : 5 → 5p = 3q (flip is the trap).
- `wp23-p13` (+40%, then down to +12%): Method 2 · Arrow map: 1.12 ÷ 1.4 = 0.8 → 20% fall.
- `q-r26-t23-10` (120% then 150% of the original): Method 2 · Arrow map: 1.5 ÷ 1.2 = 1.25 → 25%.
- `q-r26-t23-09` (300% more → what percent): "Rose BY" or "became"? → became 400%.
- `q-r26-t23-13` (+20%, −25%, now 180): Method 2 · Arrow map backwards: 180 ÷ 0.75 ÷ 1.2 = 200.
- Every line checked in python. Check: `math_check.py 23 32` → 0 / 0 / 0.

## 2026-10-06 renumber pass
So the English course does not look like the Hebrew one: every Hebrew-derived question has new numbers and a new story
(names, objects, setting). The idea, the trap, the level, the kind of condition and the methods stay the same. Every guided
solution video is rewritten to match (speech, draw cues, board tables / chains, video title). Function `renumber_pass(M)` in
t23.py runs last (after `cut_repeats`, `add_methods`, `practice_methods`). Nothing in Topic 23 is recorded (no take in
~/Documents/Course.recordings), so nothing had to be kept as it was.

**Counts:** 10 guided questions renumbered (wp23-g054, g057 … g065) with their 10 solution videos rewritten; 20 practice
questions renumbered (wp23-p01 … p20, incl. the "Method 2" lines added by practice_methods to p13 / p14); lesson examples:
6 slides of "Calculating Percentages" and 8 slides of "Percent of a Percent", plus the memory card "Percentages to know"
(7 examples, 3 tips). English-made items (q-r26-t23-01/-03/-04/-05/-16, the traps lesson, the summary, kept extras and
September items) keep their numbers. Practice: 35 → 26 (audit target ≈ 25).

**Order:** wp23-g058 (75% off — the easiest) moves before wp23-g057 (fraction left), so it is now Question 2 and g057 is
Question 3. Sidebar highlights and spoken "question two / three" follow (checked in the render). The rest stays.

**Practice clean-up (35 → 26):**
- Copy removed: q-r26-t23-15 (28% of 75, the same swap item as wp23-p21 and Topic 1's fast-practice-6).
- Extra warm-ups kept (3): p25 (12,000 → 13,500), p26 (25% more → 20% less, arrow map), p24 (30% off vs 20% + 15%). Removed
  p21 (16% of 25 = the lesson's swap example), p22 (+20% −20% = the lesson's "Up and down" example), p23 (salt water —
  mixtures stay in -11, -12 and guided Q14), p27 (backwards from 306 — as p05 and guided Q12).
- September items kept (3, types the Hebrew practice does not have): -09 ("300% more" = 400% of), -11 (remove water),
  -12 (mix two drinks). Removed -06 (growth over years, as p10), -10 (second rise against the new price, as p13),
  -13 (backwards through two changes, as p10), -14 (up p% / down p% with letters, as p18 / p16 / p20).

**Lesson examples changed** (the English-made slides — thirds, multipliers, up and down, flip rule, arrow map — keep theirs):
- Calculating Percentages: 37% → 29% (tickets 29 / 58); 20% = 1/5 → 30% = 3/10; 3/4 → 11/25 (= 44%); 2/5 → 7/50 (= 14%);
  65% of 80 = 52 → 45% of 80 = 36 (equation and ratio table); A% of 60 is 21 (A = 35) → A% of 75 is 21 (A = 28);
  (20+x)% of 60 = (80−x)% of 40 (x = 20) → (10+x)% of 60 = (60−x)% of 40 (x = 18); 15% = 42 → 35% = 98 → 15% = 54 → 35% = 126;
  30% / 35% of 230 (69, 80.5) → of 270 (81, 94.5), 10% of 66 → 10% of 48; swap 16% of 25 = 4 → 36% of 25 = 9;
  30% of the whole is 54 → 63 (whole 210); change 80 → 100 (25%) → 50 → 60 (20%).
- Percent of a Percent: +25% then −20% (no change) → +80% then −25% (+35%, not +55%; the a + b + ab/100 line follows:
  80 − 25 − 20 = 35); lose 25% then 20% (40%) → lose 30% then 20% (44%, not 50%; the multiplier slide follows: 0.7 × 0.8 =
  0.56); Lena/Noor/Ari (+25%, −40% → 25% lower) → Maya/Ben/Eli (+20%, −25% → 10% lower, not 5%); +20% then a fixed 15
  credits → +10% then a fixed 20 credits (30% / 20%; the arrow-map limit line says "plus twenty credits" too);
  after a 20% loss 96 remain (120) → after a 30% loss 91 remain (130).
- Card "Percentages to know": the method examples follow the lesson (45% of 80 = 36; 15% → 54 ⇒ 35% → 126; 35% of 270 =
  81 + 13.5; 50 → 60 is 20%; 100 → 180 → 135); complement 75%/25% → 35%/65%; percent tree 60% × 45% → 70% × 40% = 28%
  (not the Q1 numbers); tips: +80% −25% → +35%; the 1/n rule example +20%, −16⅔% → +25%, −20%; 80 − 25 − 20 = 35.
- No question equals a lesson or card example (checked over topics 1–23).

**Checks:** every new answer and every video step recomputed in Python with fractions; each key is the only correct
choice (letter items checked with numbers: T = 25, s = 10; q = 20; y = 55); the trap choices are still there (see table).
Duplicate check over a build of topics 1–23 (stems, numbers, lesson boards / lines, card cells): no copies.
`python3 math_check.py 23 32` → PROBLEMS 0, WARNINGS 0, LAYOUT 0. Rendered all 10 solution videos and both lessons and
looked at them (titles Question 1–12, sidebar highlights, chains and tables). No quadratic trinomial added.

| id | old (Hebrew) | new | answer |
|---|---|---|---|
| wp23-g054 (Q1) | survey: 55% no bicycle; of owners 40% electric, rest ordinary only → 27% (18 / 40 / 60 / 27) | students: 35% play no instrument; of players 80% piano, rest guitar only → 13% (20 / 52 / 13 / 80) | 13% (3) |
| wp23-g058 (Q2, was Q3) | display item 760 credits, −75% → 190 (180 / 570 / 685 / 190) | winter coat 680, clearance −75% → 170 (510 drop / 170 / 605 / 160) | 170 (2) |
| wp23-g057 (Q3, was Q2) | battery used 72.5% → 11/40 left (11/20 / 1/4 / 7/40 / 11/40) | ink cartridge used 57.5% → 17/40 (23/40 = used / 17/40 / 17/20 = 85% / 2/5) | 17/40 (2) |
| wp23-g059 (Q4) | fee 60 → 66 → 72: 10% vs 1/11 → first larger | cinema ticket 40 → 50 → 60: 25% vs 20% → first larger; method 2 "add 25% again" (62.5 > 60); choices reordered | first larger (3) |
| wp23-g060 (Q5) | player gives away 25% of points, bonus 30% of the rest → 2.5% lower (trap 5% higher) | Noa loses 30% of her coins, prize 40% of the rest → 2% fewer (trap 10% more) | 2% fewer (2) |
| wp23-g061 (Q7) | Rae 20% more than Sol, Tia 16⅔% less than Rae → 1 (+1/5, −1/6); 1.2 / 1.04 / 1 / 0.8 | Dana 50% more than Omer, Lior 33⅓% less than Dana → 1 (+1/2, −1/3); 3/2 / 7/6 (trap 50 − 33⅓) / 2/3 / 1; board examples +1/4 −1/5, +1/5 −1/6 | 1 (4) |
| wp23-g062 (Q8) | 50% of 15% of x = 12 → 22.5% of x = 36 (36 / 24 / 30 / 48) | 25% of 18% of y = 9 → 13.5% of y = 27 (18 / 27 / 22.5 / 36); swap example 37% of 64 | 27 (2) |
| wp23-g063 (Q9) | not equal to 15% of 4x: 10% of 6x, 60% of x, 5% of 12x, 30% of 4x | not equal to 16% of 5y: 40% of 2y, 8% of 10y, 32% of 5y, 20% of 4y (both methods: compare tops, inverse ratio) | 32% of 5y (3) |
| wp23-g064 (Q11) | timber 80% Monday / rest Tuesday, difference 36 planks → 12 (12 / 9 / 18 / 24) | farmer 70% to a market / rest to a juice factory, difference 48 kg → 36 (24 / 36 / 48 = difference / 84 = market); shortcut via 10% | 36 (2) |
| wp23-g065 (Q12) | tank, 20% removed each hour, 128 L after 2 h → 200 (160 / 180 / 240 / 200) | rain barrel, 10% used each day, 243 L after 2 days → 300 (270 = one day back / 324 / 300 / 280) | 300 (3) |
| wp23-p01 | 75% of 8/9 → 2/3 | 60% of 5/12 → 1/4 (1/3, 3/5, 1/4, 7/12) | 1/4 (3) |
| wp23-p02 | 80 beads, half white, 65% of rest purple → 14 orange | 60 pens, a third blue, 45% of rest black → 22 red (18 = black) | 22 (3) |
| wp23-p03 | 96 credits, +50% per review → first not whole after 6 | stamp 112 = 2⁴·7, +50% per year → after year 5 | 5 (3) |
| wp23-p04 | 40% of 25% of x = 9 → 3/10 x = 27 | 80% of 12.5% of x = 8 → 7/10 x = 56 | 56 (4) |
| wp23-p05 | hits 40%, misses 18 → 30 attempts | basketball, scores 65%, misses 14 → 40 shots | 40 (3) |
| wp23-p06 | 15 juniors, 25%–75% → max 45 seniors | choir, 12 sopranos, 20%–60% → max 48 others (60 = total trap) | 48 (4) |
| wp23-p07 | allowance +50%, gives 20% of new → 120% | Dina's salary +40%, saves 25% of new → 105% (trap 115%) | 105% (3) |
| wp23-p08 | a + b = 200, a = b + 60 → b is 35% | x + y = 250, x = y + 40 → y is 42% | 42% (2) |
| wp23-p09 | 15% of 3x is 18 → 45% of x | 35% of 2x is 21 → 70% of x (35 / 70 / 17.5 / 105) | 70% (2) |
| wp23-p10 | camera +10% two years, 63 above → 300 | painting +20% two years, 220 above → 500 (720 = final value) | 500 (4) |
| wp23-p11 | laptop owners 3 : 1, 40% touch-screen → 70% not | car owners 3 to 2, 30% electric → 82% not | 82% (3) |
| wp23-p12 | 75% certified, 18 first-aid only, coaching = none → 36 | 70% team sport, 24 basketball only, football = none → 60 | 60 (3) |
| wp23-p13 | bicycle 40% above, fall to 12% above → 20% | laptop 60% above, fall to 20% above → 25% (trap 40%); arrow map 1.2 ÷ 1.6 = 0.75 | 25% (2) |
| wp23-p14 | same balance: p% = 90, q% = 150 → 5p = 3q | same shopping budget: a% = 120, b% = 280 → 7a = 3b (flip 3a = 7b is the trap) | 7a = 3b (4) |
| wp23-p15 | equal blue / yellow chalk, half used, 14 blue + 6 yellow left → 70% yellow | equal red / green marbles, half out, 9 red + 15 green left → 62.5% red | 62.5% (3) |
| wp23-p16 | museum N visitors, b audio guides → b²/N | school T students, s in a science club → s²/T; choices reordered | s²/T (1) |
| wp23-p17 | coat 240 → 174 → 25 < a < 30 | boots 320 → 248 → 20 < a < 25 (22.5; dividing by 248 gives the 25–30 trap) | (1) |
| wp23-p18 | library p% to A, p% of rest to B → 100 : (100 − p) | baker q% to a café, q% of rest to a school → 100 : (100 − q); choices reordered | (2) |
| wp23-p19 | tablet; the ratio alone is not enough | bicycle; same idea, example 3/4; choices reordered | the ratio (3) |
| wp23-p20 | jacket −36, price x → 3600/(x + 36) | lamp −45, price y → 4500/(y + 45) | (3) |

## 2026-10-06 review (renumber pass)
Independent review (pre/post build diff, keys recomputed, Hebrew subtitles compared). Guided, practice, lessons: keys and
methods correct, traps kept. Fixed four places that landed back on the Hebrew:
- Lesson wp-052 #6: (10+x)% of 60 = (60−x)% of 40 — the Hebrew had (10+x)% of 80 = (60−x)% of 60 → now (5+x)% of 60 =
  (70−x)% of 40, 3(5+x) = 2(70−x), 5x = 125, x = 25 (check: 30% of 60 = 18 = 45% of 40).
- Lesson wp-052 #7 + card: 15% → 54, 35% → 126 — the Hebrew asked 14% → 56, 35%? → now 25% → 90 (÷3 → 5% = 18, ×5).
- Lesson wp-053 #6: "Maya +20% than Ben, Eli −25% than Maya" — the Hebrew's wage question is Maya +25% / −20% → now
  "Tal earns 60% more than Ben. Eli earns 45% less than Tal": 100 → 160 → 88, 12% lower (not 15% higher).
- solve-wp23-g061 board example "+1/4 then −1/5" (= the Hebrew question's +25%, −20%) → "+1/3 then −1/4" (spoken line
  too); card tip "+25%, −20%" → "+33⅓%, −25%".
Open (judgment): "35% of 270" in the 10% method keeps the Hebrew's 35% (= 30% + 5% split, whole differs, builds on the 30%
line just before).

## 2026-10-07 methods spread
Function `spread_methods(M)` in t23.py runs last (after `renumber_pass`). Every line was checked with numbers. Nothing in topic 23 is recorded.
- **Arrow map** (taught in "Percent of a Percent", before both questions):
  - wp23-g061 (Dana, Omer, Lior; Q7): written line + **new slide 4 "Method 3 · Arrow map"** (+0.4 min): Omer ×1.5 → Dana ×2/3 → Lior, product 1 → choice 4.
  - q-r26-t23-03 (desk, chair, table; Q13): written line + **new slide 3 "Method 2 · Arrow map"** before "The traps" (+0.45 min): desk ← ×1.5 chair ×2.5 → table, 2.5 ÷ 1.5 = 5/3 → 66⅔% → choice 2.
- **Shortcut · Percent shares as weights** (topic 25): q-r26-t23-12 (juice mix) — 60% of the liters at 20%: 10% + 0.6 · 10% = 16%. Line only (taught later).
- Not added (checked): g060, q-r26-t23-01, g065, p07, p10, p24 (multipliers already shown — the same as the arrow map); p13, p26, p14, q-r26-t23-16, q-r26-t23-09 (method already there); q-r26-t23-05, p16, p20 (letter choices: power count leaves all four or three choices).
- Slides: 2, about +0.85 min in total.
