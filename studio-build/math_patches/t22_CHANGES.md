# Topic 22 — General word problems and ratios: changes (course review 2026-09)

Patch: `math_patches/t22.py`. Check: `python3 math_check.py 22` gives 0 problems, 0 warnings and 0 layout problems.
Guided questions are renumbered automatically. Learn and try now has Q1–Q12, and Further guided examples has Q13–Q23.

## 1. Wrong or misleading statements fixed
- **Ratios, slide 3:** removed "don't worry about being tricked on the order — the exam avoids that wording".
  It now says: "Always match names to numbers in order. The exam does test this."
- **Ratios, slide 6:** removed the "give the plain x to the smaller one" tip. It did nothing on the 1.5 : 2 example.
  The tip now appears in *Give It to the Little Guy*, slide 2, with a letter example: "A is twice B → B = x, A = 2x".
  It is also removed from the Ratios memory card, which comes before that video, and added to the toolkit card.
- **Q17 (was Q14), method 2 (size estimate):** replaced "58 is double 29" with real bounds.
  She gave away at most ¼ of the tiles, so the start is at most 29 · 4/3 ≈ 38.7.
  She gave away at least ⅙, so the start is at least 29 · 6/5 = 34.8. Only 36 is in that range.
- **Q21 (was Q18), title slide:** "Last question of the set" is no longer true, so it now says "Question eighteen", which is renumbered automatically.

## 2. Methods added
| Method | Where it is taught | Guided question (solution video) | Practice |
|---|---|---|---|
| Inverse proportion (workers × days stays the same) | Equal Ratios: new slide "Inverse proportion" and a recap line | Q3: 6 workers, 10 days → 4 workers (answer 15) | q-r26-t22-08, -09 |
| Three-part ratios (make the shared letter equal) | Ratios: new slide "Three-part ratios" | Q8: choir 2:3 and 4:5, 30 tenors (answer 70) | q-r26-t22-06, -07, -19 |
| Changing a ratio (keep the unchanged part fixed) | Ratios: new slide "Changing a ratio" | Q9: club 5:4 → 10 boys leave → 5:6 (answer 54, two methods) | q-r26-t22-13, -18 (plus p31, p35) |
| "Or part of" → round up | Read, Organize, Calculate: new slide with the 50 people / 12 per van example | (existing Q5, company hire) | q-r26-t22-14, -15 |
| Letters in the choices → choose numbers | New video **Three Exam Tools** | Q22: pens and notebooks, $y(2x+3)$ | q-r26-t22-10, -11 (plus p08) |
| Assume all the same | Three Exam Tools | Q23: cars and motorcycles (answer 12, plus "assume the other kind") | q-r26-t22-12 (plus p21, p36) |
| One equation, two unknowns → only a multiple can be found | Three Exam Tools | (existing Q20 blocks) | q-r26-t22-16 (cannot be determined), -17 (= 75) |
| The shortcuts of the second section | New 1-minute video **Shortcuts Ahead**, before Q13: write the whole exercise first, plug in, size estimate, divisibility of the total, what changed?, scale everything, start from the end | — | — |

Other teaching changes:
- **Triangle value:** now also called "cross-multiply and divide", with an added sense check ("a bit more than 15").
  The Equal Ratios recap adds "One up, one down? Inverse" and "Before you calculate: bigger or smaller?".
- **Q19 (was Q16):** the video now starts with "What changed?", then two equations, then plugging in the answers.
- **Memory cards:**
  - *Ratios and equal ratios* gets new rows for inverse proportion, two ratios with one shared letter, and one part changing. Its new tips are "read in order", "bigger or smaller?" and "the total divides by the sum of the parts".
  - *Toolkit* gets new rows for choosing numbers, assuming all the same, and one equation with two unknowns. It also gets the little-guy and choose-numbers tips, and TeX in place of the plain "3:1", "A : B" and "8→10".

## 3. Text
- **":" for division is gone everywhere in the topic.** This covers the teacher draw notes ("8 × 15 ÷ 6", "144 ÷ 6", "112 ÷ 4", "20 ÷ 3", "÷4"), the Equal Ratios recap board ("then ÷ the rest"), and the solutions (p04, p10, p14, p15, p20, p28, p35 and Q13's "5:3.5", which is now $\frac{5}{3.5}$).
  Every real ratio stays as ":" and the text says "ratio". Draw notes such as "N : P = 5 : 3" now read "Write the ratio …".
  The ratio stems and choices are now in TeX: Q7, p16, p24, p31, p35.
- **p30 (ambiguous):** it now says each player gives tokens "just before leaving" to "every other player still in the room".
  It asks how many tokens the fifth player "has left after giving out his tokens, as he leaves". The key is 18, and $2n+8$ is now clearly the count before giving.
  The solution shows the numbers and checks $n=5$.
- **p09:** the confusing solution is rewritten: all four packs are listed in choice order, and choice (2) = 38 is the largest.
- **p03 / p14:** the solutions now finish with $540-132=408$ and $0.30+0.12=0.42$.
- **Q11 (was Q8):** the solution is now a table (now / 4 years ago) followed by the equation $2(x-4)=x+2$.
- **p17:** the stem now says "sells $x$ meters of silk (as many meters as the price of one meter)", and the two conditions are stacked in the solution.
- Every solution (all 18 old guided and all practice questions) is rewritten in TeX with the numbers shown.
  No "so" meaning "therefore" is left in the middle of a sentence, and British spellings are gone.
- **Q10 stem:** ", so each of the 5 remaining rooms" is split into two sentences.
- **p23:** the times are now "9 a.m." / "4 p.m." in place of "09:00", which read like a ratio.
- **p05:** "neighbour" → "neighbor", the question now reads "Which of the following could be…", and the solution checks $n=12$.
- **Videos:**
  - "Read, Organise, Calculate" → "Organize".
  - colour → color and practise → practice.
  - Mid-sentence ", so …" / "— so …" in spoken lines → ". So, …".
  - The math minus inside words on the Q5 slide ("5−minute") is now a hyphen.
  - The solution-video titles are refreshed from the current stems ("centre" → "center").

## 4. Figures
- None in this topic.

## 5. Practice
- **Removed near-duplicates:** p22 (same as Q15, apprentices), p25 (same as Q21, counters) and p28 (same as Q17, tiles).
- **Added 14 practice questions** (q-r26-t22-06 … -19). Exam-hard ones: -07, -09, -11, -15, -18, -19, together with the existing p18, p24, p26, p27 and p30.
- **Practice now has 48 questions** (was 37), ordered easy → hard.
  It starts with p03, p04, p08 and p12. It ends with the hard group -07, -09, -11, -15, -18, p26, p24, p27, p18 and p30.

## Counts
- Questions rewritten: 52 (all 18 old guided and 34 practice). Added: 5 guided and 14 practice. Removed: 3.
- Slides added: 5 in existing videos (Inverse proportion, Or part of, Three-part ratios, Changing a ratio, plus the little-guy lines).
  Slides changed: about 12 (recaps, Q14 method 2, Q16 reordering and more).
- Videos added: 2 lessons (Shortcuts Ahead, Three Exam Tools) and 5 solution videos.

## For the teacher to decide
- *Give It to the Little Guy*, slide 5, still says "50 shekels", while the rest of the course uses "credits". I left it unchanged.
- I kept p21 and p36 (assume all the same) and p31 and p35 (changing a ratio) next to the new questions of the same type.
  If practice feels long, these are the first to cut.
- The review asks to put "What must the total divide by?" as the first line of every ratio question. I added it only as a card tip and a Ratios recap line. I did not edit every video.

## Pass 2 (teacher-approved remove/restore plan + summary lesson)
**Removed:** nothing (the plan keeps all the additions).

**Restored (3):** the original practice questions pass 1 had removed as near-duplicates are back, with text clean-up only:
- **wp22-p22** (visitors are 5/6 of the residents → visitors are 5/11 of everyone). The solution now plugs in 6 residents and 5 visitors. Placed after p10.
- **wp22-p25** (Iris and Owen, 30 counters, 9 are passed → 11 : 4). The choices are in TeX ratio form, and the solution shows every step: 13 and 17 after, 22 and 8 before, 22 : 8 = 11 : 4. Placed after q-r26-t22-13.
- **wp22-p28** (bead piles, 1/4 and 1/6 used, 18 and 25 left → 54). The "18:3×4" division colons are gone: (3/4)F = 18 → F = 24, (5/6)G = 25 → G = 30, 24 + 30 = 54. Placed after p26.

**New: summary video `r26-t22-summary` "Summary: Word Problems and Ratios"** (about 3.9 min), at the end of "Further guided examples" (after the advanced memory card), right before the practice. Slides: Summary · Three stages · Words to math · Equal ratios · Inverse proportion · Ratios: use x · The part that stays · Build the equation · Ranges and rounding · Exam shortcuts · Before you practice (checks: what exactly did they ask, bigger or smaller and direct or inverse, which part stays the same, the ×2 goes on the smaller side, can it really be found or only a multiple; traps: a ratio read in the wrong order, using the ratio table for workers and days, and giving the number of units instead of the number of people).

## 2026-10-01 elite comparison
Target: real exam 2024_spring_q2_03 and 2020_spring_q2_07 (the wrong choices use "the gap changes by k" and miss that the gap can turn around).
- **Lesson "Build the Equation" (wp-037): new slide "Giving: the gap changes twice"** after "Before and after". Table Dan 30 / Noa 20: gives 3 → gap 4; gives 5 → equal; gives 7 → Noa ahead by 4. Rules on the board: "A gives k to B → the gap changes by 2k" and "To make them equal: give half the gap". Recap has a new line "Gives k → the gap changes by 2k". Sidebar updated.
- **New guided question q-r26-t22-20** (right after the rooms question), with a solution video: shelf A has 26 more books than shelf B; after moving some books B has 6 more. Answer 16 (choice 3): the gap changes by 26 + 6 = 32, and 32 ÷ 2 = 16. Traps: 32 (gap changes by k), 13 (only equal), 10 (forgets the turn). Video: Method 1 · The gap, Method 2 · Before and after (x cancels: 2k − 26 = 6).
- **wp22-p25** (already back in the practice, Pass 2): the written solution now starts with the gap method (giving 9 moves the gap by 18; Iris was 18 − 4 = 14 ahead → 22 and 8 → 11 : 4). The equation method stays after it. Key unchanged.
- Not added: no change to the memory card or the summary lesson (not part of this request).
