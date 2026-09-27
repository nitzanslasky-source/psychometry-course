# Review — Topic 29: Probability

Note on answer keys: `correct:` is 0-based (0 = choice 1). I solved every guided and practice question with that reading.

**Depends on:** fractions: multiply, reduce, cross-multiply (T2–T3: all questions; Q4 cross-multiplies, Q17 cancels a chain). Negative exponents and a fraction to a power (T8/T10: Q14, p20, p13 "7⁴/8⁵"). Odd/even rules (T16: p02, p08, p19). Ratios (T22: p18 "ratio 2:5"). Percentages (T23: p27). Overlapping groups / Venn (T24: p24, p26). Counting (T28): "with / without replacement", "dependent choice", the 6×6 grid, and C(4,2) = 6 (p23, where the solution says "six choices of positions" with no explanation).
**Needed by:** nothing later in the course (T30+ is geometry). If geometric probability is added (see below), it needs areas from T32–T33, so it should go there or in T38.
T29 straight after T28 is the right place.

## 1. Coverage — what is missing

Most important first.

- **"OR → add" is taught as a general rule, but it is only true for events that cannot happen together.** Board "And · Or" says "OR — either one is enough → add the probabilities". Then p24 (multiples of 4 or 6) needs *add and subtract the overlap*, which is never taught here. A weak student adds 7 + 5 = 12 → 12/30 = 2/5, which is choice 4 — the trap works because the rule was taught wrong. Fix the board: "OR → add **the separate cases** (cases that can't happen together). If they overlap, subtract the overlap — like T24." The memory card already says "add the separate cases"; the video should match.
- **"At least one" = 1 − "none".** This is a classic NITE pattern. It appears only in practice (p21, p27) and inside Q11 method 2. It is never named. Add a short slide after Q11: "At least one? Count the opposite: none. P(at least one) = 1 − P(none)." Example: two dice, at least one six = 1 − 25/36.
- **Unknown count in the bag (algebra).** Very common exam type: "A bag has 5 red and some blue. P(red) = 1/3. How many blue?" or "How many red must be added so that P(red) becomes 1/2?" The denominator changes with x. Q4 and p06 have a fixed total, so they do not train this. Add one guided question and 1–2 practice questions. Mention working back from the answers here — it is the fastest method.
- **Two-stage "choose a bag, then a token" (tree).** p10 needs it. It is not taught. The trap choice 5/11 (pour both bags together) is good, but students have no tool. Add a small tree visual: two branches ½ / ½, multiply along a branch, add the branches.
- **Choosing from a sub-group (conditional).** p26: "chosen from the music students" → the denominator is 18, not 40. Not taught. One sentence in the "Possible first" slide would cover it: "Possible = the group they choose FROM."
- **Drawing "at the same time".** Say explicitly: drawing two together = drawing one after the other without replacement. Exam wording often says "two are drawn together".
- **Probability with combinations** ("3 of 10 students are picked; what is the chance that Dana and Tal are both picked?"). p17 is close. Show both ways: step by step, or C(favourable)/C(total).
- **Geometric probability** (a random point in a square lands in the shaded circle = area ratio). It appears on NITE from time to time. It is not in this topic or in the geometry topics. One short slide in T33 or T38 is enough.
- **Largest sum for other dice** (p05: 8-sided dice, peak at 9). The lesson teaches only "symmetric around 7". Add: "For two n-sided dice the most likely sum is n + 1."

## 2. Teaching quality per level

**Weak student**
- Q7 video: "Two dice, a target sum — and a dependent choice", and "One out of six — a dependent choice". But the question says the rolls are *independent*. In probability, "dependent" means something different from the T28 counting term. This will confuse the weak student. Say "a **forced** choice: only one number works".
- Q11 opens with "The hard kind: an OR question", then the lockers are solved with cases, a complement, and "cover two of seven". Three methods in one minute is a lot for a weak student. Put the simple one first: "2 lockers out of 7 → 2/7". Then show the cases as the check.
- Dice Symmetry slide: "opposite faces of a die always add to seven" has nothing to do with the sum of two dice. The weak student will mix the two ideas. Remove it, or connect it: "swap every face x for 7 − x: a sum of 9 becomes a sum of 5" (this is the argument in Q12's text solution — the video never says it).
- Q14 needs negative exponents ("a negative exponent flips it"). This is fine if T8/T10 came earlier. Method 2 (plug in) saves the weak student. Good.
- Q17's cancelling chain is clear on the board. Good.
- Solution texts use "so" in the middle of a sentence where "therefore" is meant: Q3 "The next draw so has…", Q9 "is so one times…", Q10 "so has probability…", Q16 "She must so choose…", p18 "Heads so occupies…". This reads as an error. Use "so" at the start ("So the next draw has…") or "therefore".
- p07 and p14 write "2:14=one seventh" and "2:12=one sixth". Mixed symbols and words. Write 2/14 = 1/7.

**Medium student**
- "Possible first" is a good routine, and it is used in every video. Good.
- The idea "a stage that can't go wrong has probability 1" (Q9, Q10, Q13) is strong and well repeated. Good.
- Q12 video: "one friend picks seven, another picks nine. Same idea." 7 and 9 are *not* the same distance from 7, so this example contradicts the rule on the board. Use "one picks 5, another picks 9".
- Q8 video: "And Sam? Seven heads in a row — what are the chances?" Sam has six heads. It means "a seventh head", but say it.
- The medium student has no slide for "exactly k successes" (p23, p25): pick the positions, multiply, then multiply by the number of orders. Q10 method 2 and p22 do the "two orders — add" idea, so a 30-second slide "Exactly one red in two draws = RB + BR" would connect them.

**Strong student**
- The lesson part (Q1–Q6) is slow for them, but the videos are short, so it is fine.
- Good exam flashes: symmetry of position (Q17), start with the restricted stage (Q13), check choices before plugging in (Q14). Keep them.
- Missing for this level: the "unknown count" algebra, "at least one", the tree, and overlap in OR. These are exactly the harder exam questions.

## 3. Correctness

All 17 guided keys and all 27 practice keys are correct. All solution texts match their questions. I re-solved the ones that looked risky: p05 (sum 9 has 8 ways), p14 (inputs 3 and 7 → 5/36), p15 (2/9), p16 (5/64), p17 (1/10), p19 (½), p24 (10/30), p26 (5/9).

Wording or teaching errors (not wrong keys):
- **Board "OR → add the probabilities"** is false for overlapping events and is contradicted by p24 (see Coverage). This is the main one.
- **Q7 video: "dependent choice"** for independent dice (see Weak student).
- **Q12 video: "seven… nine. Same idea."** is a wrong example of symmetry.
- **Q8 video: "Seven heads"** should be "six heads — a seventh?".
- p02 is correct, but the solution assumes each colour appears at least once. It is fine because choice 6 gives 4 white and 4 black.

## 4. Methods and tricks to add or teach differently

- **"At least one" slide** (after Q11): 1 − P(none). Use two dice and p27-style percentages.
- **Overlap slide** after "And · Or": OR = add − overlap. Link to T24 Venn. Example: 1–30, divisible by 4 or 6.
- **Tree picture** (after Q16): branches, multiply along, add across. Q16, p10 and p15 all become one method.
- **Work back from the answers** for unknown-count bags: put each choice into the fraction and check.
- **Sanity check by size**: "AND makes it smaller, OR makes it bigger." It eliminates choices fast (e.g., in Q5, 9/16 is bigger than ½, so it is out immediately).
- **Symmetry by 7 − x** in the Dice Symmetry video, in place of the opposite-faces tangent.
- **Most likely sum = n + 1** for two n-sided dice (one line on the memory card).
- **Position symmetry** (Q17) could also be used for p17: any 2 of 5 people are equally likely to get the books → 1/C(5,2) = 1/10.

## 5. Practice

- 27 questions is enough. The spread is good: p01–p09 easy, p10–p27 medium, with p13–p17 at exam-hard level.
- **Repetitive:** p03 is exactly Q9 (two 8-sided dice match). p20 is Q14 with new letters. p15 is Q16 with smaller numbers. Replace p03 with an unknown-count bag question.
- **Practice uses methods never taught:** p10 (tree), p23 (C(4,2) and "exactly k"), p24 (overlap), p26 (sub-group), p21/p27 ("at least one"). Either teach them (Section 4) or move them to the end, labelled "challenge".
- p05 is a good trap (7 feels like "the top" but these are 8-sided dice), but only once the n + 1 rule is taught.
- Most practice questions use tokens/dice/coins. Add one story-type question (people, a committee, a lottery) as on the real exam.

## 6. Verdict

- **Weak:** Can solve simple one-draw and "and" questions. Will fail "or" with overlap, "at least one", and trees.
- **Medium:** Reliable on the core types. Will lose points on p10/p21/p24/p26-type questions, because they are never taught.
- **Strong:** Enjoys the symmetry tricks. Needs the unknown-count algebra and overlap/complement rules for the hardest exam items.

**Top 3 changes, in priority order:**
1. Fix "OR → add" on the board: add only separate cases, and subtract the overlap otherwise (link to T24). Add one guided example.
2. Add a short "at least one = 1 − none" slide and a tree-diagram slide (two stages, multiply along, add across). Then p10, p21, p27 and p15 are all covered.
3. Add a guided question and 1–2 practice questions with an unknown number of tokens (algebra plus working back from the answers). Replace p03, which is a copy of Q9.
