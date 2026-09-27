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
