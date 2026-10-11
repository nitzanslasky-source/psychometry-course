# Deep pass — organizing methods for combinatorics / probability / factorials / overlap / trial & error / generality (88 real Qs)
Mini-examples are my own. Ids = real questions (not copied).

## 0. KEY FINDING — the exam's "combinatorics" label is half extreme-case reasoning
12 of the 24 real "combinatorics" questions are NOT slot-counting at all; they are min/max, worst case, pigeonhole or "which total is impossible":
2023_autumn_q1_04, 2023_autumn_q2_01, 2025_autumn_q1_03, 2020_spring_q1_01, 2023_spring_q1_05, 2024_spring_q1_08, 2024_spring_q2_17, 2025_spring_q1_03, 2019_winter_q1_14, 2019_winter_q2_05, 2022_winter_q1_17, 2023_winter_q1_19.
Topic 28 never sends the student there: its intro has only "Type 1: list it" and "Multiply the Choices"; no mention of Topic 20/21 (grep "Topic 21" in t28 = nothing).
CUE: the question asks "at most / at least / necessarily / cannot be" → MOVE: this is the Topic 21 extreme routine (push / worst luck + 1 / remainder test), not the 5-step checklist.
Mini-example: "17 pupils from 5 classes, every class has at least one. At most how many from one class?" → give 4 classes 1 each → 13.
Fit: one "router" slide in the t28 intro + summary (~0.5 min) and 2–3 such questions in the t28 practice. VERDICT: WORTH IT (12 Qs; a student who files them under "counting formulas" looks for nCr and wastes 1–2 min).

## 1. Counting — ONE method: "stages → multiply → then fix order / repeats / double counts"
Course: taught as ONE named method. t28 memory card "The 5-step checklist": "1 Does order matter? … 2 Repetition allowed? … 3 A restriction? most restricted position first … 4 Counted twice? divide by 2 or k! … 5 One count or cases? separate cases: add · 'not', 'at least one': all − forbidden". Summary: "Work in stages. How many options at each stage? Multiply."
Works: 2026_spring_q2_20, 2022_winter_q2_18, 2020_winter_q2_06, 2025_winter_q1_02, 2023_autumn_q2_07, 2022_autumn_q1_16, 2021_spring_q2_16, 2024_spring_q1_05, 2024_autumn_q1_07, 2019_winter_q1_07, 2023_spring_q1_05 (11).
Fails (structural/spatial, need a small case): 2020_autumn_q1_16, 2025_spring_q1_08, 2023_winter_q1_19 — covered by tips "Test it on a small case you can draw" (t28), "count a small case by hand" (t20).
VERDICT: already taught well.

## 2. Extreme / min-max routine ("push the others, then build an example"; "worst luck + 1")
Course: taught as one named method in t21 ("Minimum & Maximum", "More Minimum & Maximum"): "Max of one → give the others the least · Min of the largest → share as equally as possible · Min of one → give the others the most", "Prove the bound, then build it", "To be sure → worst luck + 1"; t20 "worst luck (one in each box), then one more"; t20 tip "An integer less than 12 is at most 11" (strict → step one integer).
Works (16 here): 2023_autumn_q2_01, 2020_spring_q1_01, 2024_spring_q2_17, 2022_winter_q1_17, 2022_autumn_q1_18, 2021_spring_q2_10, 2025_autumn_q1_03, 2023_spring_q1_05, 2019_winter_q1_14, 2023_winter_q1_19, + overlap ranges 2024_spring_q1_08, 2019_spring_q2_04, 2020_winter_q1_14, 2023_autumn_q2_20, 2024_autumn_q1_19, 2020_autumn_q1_11.
Gap: only the routing from other topics (see §0).
VERDICT: already taught well.

## 3. "Which total is impossible" routine (common step / remainder, then list in order)
Course: t21 card "Constant step → Test by remainder: all totals leave the same remainder", "Keep an order: no 5s, one 5, two 5s", "'Three times as many…' → count must be divisible by 3".
Works: 2019_winter_q2_05 (all prices ×3), 2023_autumn_q1_04 (10−d divisible by 3), 2025_spring_q1_03, 2024_winter_q2_16, 2023_spring_q2_10, 2022_autumn_q1_18 (6).
VERDICT: already taught well.

## 4. Probability — three doors: COUNT / PATH / SYMMETRY
- COUNT (outcomes equally likely, small table: dice sums, a bag) → wanted/possible. Ex: two 4-sided dice, sum 5 → 4/16. Works: 2019_spring_q2_13, 2023_spring_q1_17, 2025_spring_q2_16, 2026_spring_q1_02, 2019_winter_q2_19, 2020_spring_q1_14 (6).
- PATH (story happens in steps: draws one after another, rounds, branches) → multiply the step chances along the path, first step "free", add paths. Ex: 3 red 3 blue, two draws, different colours → 1·3/5. Works: 2020_autumn_q2_17, 2022_autumn_q2_15, 2023_autumn_q1_14, 2024_autumn_q2_14, 2025_autumn_q2_16, 2024_spring_q2_20, 2023_winter_q2_02, 2022_winter_q1_06 (8).
- SYMMETRY (where does one special item end up / who wins a fair draw) → 1/n, or k/n if k places are picked. Ex: 1 gold coin among 10, pick 3 → 3/10. Works: 2024_winter_q1_16, 2025_winter_q2_14, 2020_spring_q1_14 (3).
- Doesn't fit: 2020_winter_q1_18 (sum of probabilities = 1), 2021_autumn_q1_03 (range count), 2019_spring_q1_04 / 2025_spring_q1_20 / 2020_spring_q2_05 (mis-tagged averages).
Course: all three are taught, but as a 13-row rule list (t29 card "Rules": wanted/possible, complement, AND, OR, at least one, exactly k, tree, "First pick doesn't matter", …) plus a closing checklist ("What is possible…? AND or OR…? 'At least one'? Use 1− none"). Symmetry: "One red marble out of nine. First, third or last — always one ninth." There is no top-level "which door?" decision.
Fit: a 3-row top table on the t29 card + 1 summary slide (~0.7 min). VERDICT: BORDERLINE→WORTH (cheap reorganization of existing content; covers 17/24 real probability Qs; it's the closest analogue to the "V method" here).

## 5. Letters in the story/choices → plug numbers; best value = the "nothing-changes" value
CUE: letters in the choices and a story where some value makes the answer obvious without any formula (0 extra people → 0 change; the newcomer equals the average → average unchanged; no red/green items → everything is purple).
Mini-example: "n friends share a bill of B; k more join; how much less does each pay?" → k=0 → 0 → kills every choice not 0 at k=0.
Re-check on the 88: clean single-plug win in 2019_spring_q1_15 (x=0), 2020_spring_q2_05 (y=x), 2020_spring_q2_16 (n=k=0 → 80). Partial (leaves 2, second plug needed): 2022_winter_q1_19 (k=0), 2023_winter_q2_02 (n=0 → P=1), 2025_autumn_q1_17 (k=1). Ordinary plug-in (n=2 etc.) also works on all six.
Course: plug-in is ONE named method (t51 "Plugging In Numbers": "Eliminate 3", "Not 3? Plug again", "Distinct results", "Convenient numbers", "Keep the conditions"). But the "trivial-case" value is not taught, and t23 card says the opposite: "Plugging in numbers: not 0, not 1"; t51: "1 … in powers, products and quotients it changes nothing".
Fit: one sentence on the t51 "Convenient numbers" slide + soften the t23 tip ("0 is fine when it makes the answer obvious; if two survive, plug again") (~0.3 min). VERDICT: BORDERLINE (3 clean wins here, likely a few more in averages/percent; main value is removing the contradictory "not 0" rule).

## 6. Turn it around — count the smaller side (who stays out / what remains / absences)
Works: 2022_autumn_q1_16, 2023_autumn_q2_07, 2020_spring_q1_14, 2021_spring_q2_16, 2024_autumn_q1_19, 2024_autumn_q1_07 (alt) (6).
Course: taught in each place — t28 "Choosing many? Choose who stays out instead … Always count the smaller side"; t24 "Turn it around: who is NOT in all three?"; t29 complement/"at least one = 1 − none". Not linked across topics, but each instance is taught where it's needed.
VERDICT: already taught well (optional one-line cross-reference).

## 7. Overlap — one picture
Course: one framework — t24 "two types: Range / Exact", pizza picture, "A+B−both+neither=total", max overlap = smaller group, min = (A+B)−total, "the squares method", Three Groups "total minus everyone who misses a group". Works on all 6 real overlap Qs + 2024_spring_q1_08.
Gap: HIDDEN TOTAL. 2020_winter_q1_14 gives no total — it's 24 hours. Cue "no total given → is there a natural one (24 h, 7 days, 12 months, 100%, 360°)?". Only 1 Q in 88; t24 already has "Percents? Stay in percent".
Fit: one tip line on the t24 card. VERDICT: BORDERLINE (1 Q, but a real trap; costs nothing).

## 8. Factorials — taught as one toolkit
t28 "Factorial Expressions" + card: "expand only until you match", "know by sight 120/720/5040", "run of neighbors b!/a!", "sum: take out the smaller factorial", "primes in n!", plug n=2. Works on all 12. VERDICT: already taught well. (Parity shortcut in 2019_winter_q2_16 — x must be odd — one-off.)

## 9. Small recurring cues (not worth separate content)
- Choices are unevaluated formulas (6·6!, 1/7², (1/2)^n, 5/36) → build the answer stage by stage and match the shape; the distractors are the wrong models (1/6!, 1/7·3). Ids: 2024_autumn_q1_07, 2023_autumn_q1_14, 2019_winter_q2_19, 2023_winter_q2_02, 2024_spring_q2_20, 2025_autumn_q2_16 (6). Course partial: t28 tip "Choices that differ by a factor (210 and 35)? Order matters: the bigger one." BORDERLINE (saves seconds, not minutes).
- Per-unit thinking (what ONE game / sentence / cycle contributes): 2021_spring_q2_10, 2022_autumn_q2_10, 2019_winter_q1_20 (3). Not worth.
- Ratio of two probabilities → ratio of counts: 2019_spring_q2_13, 2022_winter_q1_06 (2); t29 Q15 already does it. Not worth.
