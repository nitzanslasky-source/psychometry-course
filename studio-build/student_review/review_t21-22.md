# Review — Topics 21 and 22

Note on answer keys: `correct:` is 0-based (0 = choice 1). I checked every key with that reading. I solved every guided and practice question.

---

# Topic 21: Trial, limits and patterns

**Depends on:** remainders (T15: Q6 method 2, Q15, "Cycle → remainder"); divisibility by 2/3 and even/odd (T16: Q7 method 2); LCM (T14: slide "Meeting times", Q16, p08, p22). p08 uses the word "least common multiple", but T21 only says "common multiple". Also: strict inequalities with integers, "fewer than 7 = at most 6" (T12: p02, p19); powers of 2 (T10: Q5); fractions (T2–T3: p06, p15, p17); a linear expression L = 6v + 3s − 1 (T6: Q2 method 2). The must/possible distinction (T20) is taught again on slide 4 of the first video, so point back to T20 there. **Not taught anywhere:** 1 + 2 + … + k = k(k+1)/2 (Q3 method 2 uses it with no explanation).
**Needed by:** T22 (plug in the answers, "size" thinking); T24 overlapping groups (min/max, as slide 3 says); T25 averages (min/max of one value); T26/T27 (two schedules meeting); T28 counting (listing cases in order).

## 1. Coverage — what is missing

- **Worst case / pigeonhole** ("how many must you take to be SURE you have two of the same colour?"). This is a classic NITE min/max question. It is not taught here, and it is not taught anywhere in the course. p14 (four players, longest game) is exactly this idea, but it is only in practice. Add one slide to the min/max lesson: "To be sure → imagine the unluckiest case, then add one." Board example: socks of 3 colours → 4 socks.
- **"Must be true" questions.** Slide 4 of the first video teaches possible vs must. But almost every question asks "possible" or "impossible". Only p24 ("necessarily") and p06 test it. Add 1 guided + 2 practice "which must be true" questions.
- **Sequences with a formula in n.** Only Q5 teaches plug in n = 3. The practice set has **zero** questions of this type. Add 2–3 (a_n given → find a_10; sum formula in the choices).
- **Calendar cycles** ("100 days after Monday is…") and **last-digit cycles** of powers (7^n). Both are cycle-by-remainder questions the exam likes. Neither appears. Add one each to the Patterns & Cycles video, or state which topic covers them.
- **The formula k(k+1)/2.** The patterns lesson says "forget school formulas". But this one formula is used in Q3, p07, p23. Teach it once as "the cheapest k different positive whole numbers".

## 2. Teaching quality per level

**Weak student**
- The topic has two videos called "Minimum & Maximum", and "Patterns" then "Patterns & Cycles". The second set repeats the first with new rules. The weak student sees two sets of rules and mixes them. Example: video 1 says "min of the largest → balance". Video 2 says "to minimise one — give all the others the maximum". Both are right, but they sound opposite. Put them on one board, side by side, with one example each.
- Q8 and Q13 are the **same question** (same id text, same choices). A weak student will think it is a mistake. Title Q13 "Question 8 again — the shortcut".
- Q13 method 3 (spare markers: 86 − 72 = 14, so at least 10 boxes stay at 3) is the clearest route. Q8 is solved by long testing first, then Q13 teaches a "no holes" rule that is not safe (see Correctness). Lead with the spare-markers method.
- Q4 solution: "Halving forty-five would describe a different rule" is unclear. Say: "Don't subtract first: 46 − 1 = 45, then halve — that is the wrong order."
- Q3 video: "Read the bold word: the LARGEST". The stem on screen is plain "largest". Make the key word bold in all stems, or the tip makes no sense.
- Division is written with ":" in solutions ("28 : 4 = 7", "12 : 4 = 3"). In the next topic ":" also means a ratio. Use ÷ or a fraction bar.

**Medium student**
- Q12 method 1: "They ask 'at least' — so plug in the SMALLER one first." The stem says "smallest", not "at least". Say "They ask for the smallest".
- Q9 method 2 (last digit): for the maximum it ends with "16 × 2 = 32 → 320". That is just the full multiplication. The trick adds nothing here. Keep the last-digit trick for Q11, where it really works.
- p12 does not say how many robots are blue. The medium student gets stuck. Add "Any robot may be blue" to the stem.

**Strong student**
- The first video (5 slides of "how to use this chapter") and the "Why it matters" slide ("at school you were spoon-fed…") are slow. Cut them to one slide each.
- Q2 method 2 (L + 1 is a multiple of 3), Q6 method 2 (remainder), Q7 method 2 (divisibility), Q15 method 2: good, fast. More of this.
- They need harder traps: pigeonhole, "must be true", a two-condition skip question (two swap sizes at once, like p03 with 2/7/12).

## 3. Correctness

- **All keys are correct** (Q1–Q16, p01–p27).
- **Q13 method 1 teaches a false general rule.** "In min-max questions, the possible values form a range — and the range is continuous. No holes." The memory card repeats it: "'Cannot be' in a min–max question → the range has no holes — the answer is at an end." This is false in general, and it contradicts this topic's own "skip" lesson (Q2, Q6, p03, p26 all have holes). It is true in Q13 only because you can move one marker at a time. Fix: "No holes **only when you can change the answer by 1 at a time**. With fixed jumps (5, 3…) there ARE holes." Change the memory card row too.
- Q12 video: "They ask 'at least'" — wrong word (see above).
- p13 solution: "cheapest upgrade per kilogram" is not a full proof. The answer 36 is right (I checked all 5-package mixes). Better: "list the few mixes of 5 packages that make 28 kg" (4 of them) — this is trial and error, the topic's own method.
- p03, p05, p14, p21 solutions are correct but short. p05 says "Tuesday ends with 24+72=96" without saying 24 is kept and 72 are added. Write each day in full: "start 48 → sell 24, keep 24 → add 72 → 96".

## 4. Methods and tricks to add

- **"Worst case + 1"** slide for "to be sure" questions (Min & Max video 2, after slide 3).
- **One min/max board** (both videos): "Max of one → give the others the least. Min of the largest → share as equally as possible. Min of one → give the others the most." One example each, same total.
- **Spare-units method** (Q13 method 3) as a named tool on the memory card: "fill everyone to the minimum, then count what is left". It solves Q3, Q8, p07, p23, p25 in one line.
- **Sequence plug-in rule** (Patterns video): "n = 3. If two choices survive, also try n = 4." Also: "check n = 1 as a quick sanity check".
- **Cycle table**: position → remainder, with 3 exam uses (lamps, days of the week, last digit).

## 5. Practice

- Quantity: 16 guided + 27 practice. Enough.
- Spread: mostly easy–medium. Hard ones: p12, p13, p17, p18. There is no difficulty order. Put p21, p02, p04 first; p13, p17, p18 last.
- Repetitive: the 4/9 swap appears in Q6 and again in p26 (same numbers 4 and 9, same 24→54 list). p03, p10, p11 are the same "constant step" idea. Distinct-integers appears in Q3, p07, p23, p27. Replace two of these with pigeonhole and must-be-true questions.
- Missing in practice: sequence formula in n (0), days of week (0), worst case (only p14).

## 6. Verdict

- **Weak:** partly. Can do step-by-step patterns and simple min/max. Gets confused by the two sets of min/max rules and may trust the "no holes" rule on a skip question.
- **Medium:** mostly yes for skip, remainder and min/max questions. Unreliable on formula sequences (no practice) and "to be sure" questions (not taught).
- **Strong:** yes for this material. Missing the hardest exam types (pigeonhole, must-be-true).

**Top 3 changes**
1. Fix the "range has no holes" rule in Q13 method 1 and the memory card (add "only when you can change by 1").
2. Add a "worst case + 1" (pigeonhole) slide with 1 guided + 2 practice questions, and 2–3 practice questions on formula sequences with n = 3.
3. Merge the two min/max rule sets onto one board; label Q13 as "Q8 again"; teach 1 + … + k = k(k+1)/2 and the spare-units method once.

---

# Topic 22: General word problems and ratios

**Depends on:** linear equations and brackets (T6–T7: Q7, Q8, Q15, p06, p32, p34); two equations in two unknowns (Q16, Q18, p17 — check which topic teaches it); fractions (T2–T3: Q10–Q14, p13, p19, p26); absolute value (T13: slide 7 "|A − B| = 12"); inequalities, strict vs ≤ (T12: Q9, "Enough, not enough"); divisibility (T16: slide "Units and divisibility", Q5, Q15 method 2); x² and square roots (T8–T10: p01, p08). From T21: plug in the answers, size estimate, elimination.
**Needed by:** T23 percentages (part of a whole, stages "write the whole exercise first"); T25 averages; T26 work and T27 motion (rates, the ratio table); T24 overlapping groups (fractions of groups); T36 similarity and T31 triangles (side ratios, the ratio table). The ratio table/triangle value should come before all of these.

## 1. Coverage — what is missing

- **Combining two ratios** (A:B = 2:3 and B:C = 4:5 → A:B:C = 8:12:15). This is very common on NITE and is not taught. p02 is close but uses "times as many". Add one slide to the Ratios video and 2 practice questions.
- **Inverse proportion.** The ratio table only shows direct proportion. The "costs as" slide touches it, but there is no rule: "more workers → fewer days: multiply, don't divide". Students will use the triangle value on an inverse question and get it wrong. Add one slide, or say clearly that T26 covers it.
- **Word problems with letters in the answers** ("a pen costs x, a notebook costs 2 more… how much for y of each?"). Very common on the exam. Only p08 has letters. Teach: "choose easy numbers (x = 2, y = 3), compute, test each choice" — the same plug-in as T21.
- **"Assume they are all the same"** (all stools → 126 legs, then each cart adds 1). p21 and p36 use it in the solution, but it is never taught. It is a fast exam method. Add it to the toolkit card and one guided video.
- **Changing a ratio by adding to one or both parts** (mixtures). Only p31 and p35. No lesson.
- **"Cannot be determined"** answers. p29 has one, and Q17 explains why one equation is not enough. Say it as a rule: "one equation, two unknowns → you can only find a combination that is a multiple of it."
- Only in passing: "or part of" rounding up. The rule is only on the recap board of "Read, Organise, Calculate". Put it on a teaching slide with the bus example ("50 people, 12 per van → 5 vans").

## 2. Teaching quality per level

**Weak student**
- **":" means two things.** In this topic "3:5" is a ratio, but "8 × 15 : 6", "144 : 6 = 24", Q10's "5:3.5" and p14's "18:120" mean divide. English exam papers use ÷ or a fraction bar. In a ratio lesson this is very confusing. Use a fraction bar for division everywhere.
- "Triangle value" is a translation of a Hebrew term. Say once: "(also called cross-multiplying and dividing)". The name is fine, but the weak student must see it is the same as cross-multiplying.
- Q8 written solution is one dense sentence: "the younger age and the age gap are both one ratio unit in a 1:2 age ratio". The weak student cannot follow it. Write the table (now / 4 years ago) and the equation, as in the video.
- Ratios slide 6 tip "give the plain x to the smaller one" is placed on a 3:4 example, where it does nothing. Move it to "Give It to the Little Guy" (A is twice B → B = x, A = 2x). The Ratios memory card also gives the "little guy" tip before that video is shown.
- Ratios slide 3: "don't worry about being tricked on the order — the exam avoids that wording." Remove this. Students must always match names to numbers in order. Q12 and p22 are exactly this trap.

**Medium student**
- The "Further guided examples" section brings new tools (write the whole exercise first, scale everything, start from the end, size estimate, subtract the equations) only inside solution videos. There is no lesson for them. That is fine for a strong student. The medium student needs a 1-minute video before Q10: "Five shortcuts you will see now", with one line each.
- Q14 method 2 (size estimate) says "58 is double 29 — she'd have had to give away half". Give the real bound: at most a quarter was given away, so the start was at most 29 × 4/3 ≈ 38. At least one sixth, so at least 29 × 6/5 ≈ 35. Only 36 fits.
- Q16: good — three methods, the "what changed?" method is the best. Lead with it.

**Strong student**
- Good for them: Q5 (even difference), Q13 size estimate, Q15 divisibility, Q17 scaling, Q18 from the end.
- They need harder items: three-part ratios, inverse proportion, letters in the answers, two-stage ratio change.

## 3. Correctness

- **All keys are correct** (Q1–Q18, p01–p37).
- **p30 is ambiguous.** "How many tokens does the fifth player have when leaving?" Before giving, he has 2n + 8 — that is choice 1. After giving, 18 — the key. Write: "…have left after giving out tokens, as he leaves?"
- **p09 solution is confusing.** It lists the packs in a new order and then says "the first pack is largest". The first pack in the choices (4 large + 4 small = 36) is not the largest. Write: "Choice 2 (6 large + 2 small) = 38 is the largest."
- p03 and p14 solutions stop before the final number. p03: add "540 − 132 = 408". p14: add "0.30 + 0.12 = 0.42".
- p17 wording "sells x meters of silk" is odd but correct (x = 11 used as a length). Say "sells as many meters of silk as its price per meter".

## 4. Methods and tricks to add

- **Ratio units, then one real number** — already the core. Add a 3-part-ratio slide ("make the shared letter the same number").
- **"Assume all the same"** (p21, p36) as a named tool with a guided video.
- **Plug in numbers for letter answers** (link to T21's n = 3).
- **Inverse proportion slide:** "same work: workers × days stays fixed".
- **Check the answer size before you calculate** (Q2 video's sense check "fewer than 24"). Make it a board habit on every ratio-table question.
- **Divisibility from ratios** (slide 8 + Q15): very strong. Add to every ratio question's first line: "What must the total divide by?"

## 5. Practice

- Quantity: 18 guided + 37 practice. Plenty.
- Spread: good. Easy (p03, p04, p08, p12, p33) to hard (p18, p24, p26, p27, p30). No order — put easy ones first.
- Repetitive: p28 is Q14 again (1/4 and 1/6, piles in unknown order). p22 is Q12 again (x/y as many → fraction of all). p25 is Q18 again. Keep one of each pair, or change the numbers and the wording more.
- Missing in practice: three-part ratios, inverse proportion, letter answers (only p08), "or part of" rounding (0 in practice).
- Good ones: p18 (row/column sums), p27 (score changes), p29 (cannot be determined), p35 (mixture).

## 6. Verdict

- **Weak:** partly. Can translate phrases and use the ratio table. Confused by ":" as both ratio and division, and by terse solutions (Q8). No method for three-part ratios or inverse proportion.
- **Medium:** mostly yes. Unreliable on three-part ratios, letter answers and the untaught shortcuts in the second section.
- **Strong:** yes. Would like harder ratio questions and fewer repeats.

**Top 3 changes**
1. Add three-part ratios and inverse proportion (one slide + 2 practice questions each), and letter-answer word problems with plug-in numbers.
2. Stop using ":" for division in this topic (and T21). Use a fraction bar or ÷. Remove the "the exam avoids order tricks" line.
3. Fix p30 (ambiguous), p09 (confusing solution), p03/p14 (unfinished solutions), and rewrite Q8's solution as a table. Teach "assume all the same" and the "or part of" rule on real slides.
