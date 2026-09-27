# Topic 28 — Counting possibilities: changes

Patch: `math_patches/t28.py`. Check: `python3 math_check.py 28` shows 0 problems, 0 warnings and 0 layout problems (113 slides).

## Summary
- Questions: 41 rewritten, 27 added (9 guided with solution videos, 18 practice), 3 removed.
  The topic had 44 questions (17 guided, 27 practice). It now has 68 (26 guided, 42 practice).
- New lesson videos (2): "Roads, Zeros and "At Least One"" (7 slides) and "Together, Apart and Repeats" (7 slides).
- New solution videos (9): Questions 13 and 19–26 (the guided questions are renumbered automatically in course order;
  the old Q13–Q17 are now Q14–Q18).
- Lesson slides changed: 6 ("Add or Subtract Cases" 2, "Choosing a Group" 2, "Mutual Action" title slide, 1 wording fix in the first video); slides added: 2 ("Groups with no names", "The checklist" in "Choosing a Group").
- Solution videos changed: Q7, Q8 (÷ instead of ":"), Q10 (spelling), Q11 (cancelling), Q12 and Q17 (intro line), Q14 (whole slide 2), Q15 (spelling), Q17 (2 lines). All guided sidebars updated.
- Memory cards: both updated ("Counting possibilities" gets the 5-step checklist; "Advanced counting tools" gets a "More methods" table and moves to the end of its section).
- Figures: 1 new question figure (road map for Q19) and 1 slide figure (road map in the new video).

## 1. Wrong or misleading teaching (fixed)
- **Q14 video:** the teacher started with the free tens digit ("because nothing restricts it"). That contradicts the rule "most restricted position first". Now it starts with the hundreds digit, then the forced units digit, then the free tens digit.
- **Q17 video:** "Worried you missed one? Six is fewer than we've already found…" is replaced by "We found seven. Choice six is too few. Forty-two and seven hundred twenty would need many more rows — and there are no more." "Choose the one who stays in place" is now "who stays out".
- **One name:** the video "Two-Way Connections" is now "Mutual Action", the name the cards and the other videos use.
- **"Rare" removed:** "Add or Subtract Cases" no longer says "very rare … one question every few years"; the slide is now "Why learn it: less common, needed for probability". "Choosing a Group" no longer says "very hard, and very rare".
- **Q12 / Q17 intros:** "Last question of the set" is no longer true (new questions follow), so they now say the question number.

## 2. Methods added
In **"Choosing a Group"**:
- "Who stays out" is now a general rule: choose k of n = choose the n − k who stay out (8 of 10 = 2 of 10 = 45).
- New slide "Groups with no names": named → keep the count, no names → ÷ 2 (6 people into two groups of 3: 20 → 10).
- New slide "The checklist" (5 steps: order? repetition? restriction first / forced = 1? counted twice → ÷2 or ÷k!? cases (+) or all − forbidden?). Also the first table of the memory card.
- New guided **Q13** (6 friends into two unnamed groups of 3 = 10), 2 methods.

New video **"Roads, Zeros and "At Least One""** (advanced section, after Q18):
- Road maps: "and" along a path = ×, "or" between paths = + (drawn map, 3·2 + 2·4 = 14).
- The zero trap: even three-digit numbers from 0–5 without repeats, split by "units digit 0" / "2 or 4": 20 + 32 = 52 (trap: 60).
- At least one = all − none (three-digit codes with a repeated digit: 1000 − 720 = 280).
- Which is the base? 4 letters into 3 mailboxes = 3⁴, not 4³ ("each object chooses").
- Quick checks: test a formula on a small case; elimination by size (order matters → the bigger choice; group → divide).
- Guided **Q19** road map with figure (23), **Q20** four-digit even numbers from 0–4 (60, 2 methods), **Q21** codes with at least one 5 (3439, with the double-counting trap explained), **Q22** 5 letters into 3 mailboxes (243, with a small-case check).

New video **"Together, Apart and Repeats"**:
- Glue for "together" (×2 or ×k! inside), "not together" = all − together, gaps for "no two side by side", identical items (÷ factorial of each repeat), round table ((n − 1)!).
- Guided **Q23** 3 math books together (144), **Q24** two girls not side by side (72: gaps, and all − together), **Q25** BANANA (60), **Q26** round table with a glued pair (48, 2 methods).

These now teach the methods that practice already used without a lesson: p15 (gaps), p23 (glue), p25 (identical letters), p26 (round table).

## 3. Text
- Every guided and practice solution rewritten with the numbers in TeX (the old ones were mostly words: "four times six is twenty-four").
- No ":" for division left (p03, p12, p25, p27, and the draw notes of Q7 and Q8 now use ÷ or fractions).
- Mid-sentence "so" removed (Q14, Q15, Q16). British spellings fixed (colour, neighbour, organised).
- Missing spaces after commas fixed (p17–p20, p24, Q10).
- "three−digit" / "two−digit" with a minus sign: the slide notes of all solution videos are rebuilt from the stems.
- Reworded: Q3 (simpler code wording), Q15 (conditions one under the other, C × D in TeX), p06 and p16 (letters in TeX), p18 (clear "which two numbers came up"), p20 (clear "pairs of digits"), p21, p24, p25.
- Q11 video: the cancelling is now written as a fraction and done one step at a time (8 with 4·2, then 6 with 3).

## 4. Practice
- Removed: p04 and p07 (one-step n!, duplicates of Q6), p13 (worst-case key puzzle, not counting).
- Added 18 (q-r26-t28-10 … 27): road maps (2, one hard round trip = 96), zero-digit cases (2), at least one (3), objects into boxes (2), glue / not together (2), gaps (1), identical items (2, one with a zero), round table not together (1), unnamed groups/pairs (2), 8 of 10 (1).
- Order is now easy → hard (one-step first, then cases, complements and arrangements, then the puzzles p18, p20). About 20 items are exam-medium or exam-hard.

## For the teacher to decide
- The review asked to use the checklist "in every solution video". It is used in the new videos; the 12 old learn-section solution videos were not changed for this.
- The road-diagram slide is in the new video, not in "Multiply the Choices" (it needs "or = add", which comes later).
- p02 and p16 test exponents more than counting; kept as short factorial/power practice.
- The API has no way to shrink a slide table, so Q15's stem was shortened ("A and B on top, C and D below") to keep the Q15 video table clear of the answer choices.

## Pass 2 (2026-09-27): remove/restore plan + summary lesson
Check: `python3 math_check.py 18 27 28 33` shows 0 problems, 0 warnings and 0 layout problems.

**Removed (plan):**
- "Choosing a Group" (wp-137): the slide "Groups with no names", its sidebar entry and its recap line. The recap says the original "Two questions next — one of each." again.
- `r26-t28-cases`: the slides "Road maps" (with its figure) and "The zero trap", their recap lines and sidebar entries. The video is renamed **"Boxes and 'At Least One'"**. The title slide and the recap ("Two questions next — one of each.") were updated.
- Guided q-r26-t28-01 (groups with no names), -02 (road map, with its figure) and -03 (zero among the digits), with their solution videos. The guided questions were renumbered: learn 1–12, advanced 13–23. The original line "Last question of the set." in the Q12 video is back, because Q12 is again the last question of the section.
- Practice q-r26-t28-10, -11, -12, -13, -24 and -25.
- Card `mem-counting`: the row "Groups with no names". Card `mem-counting-advanced`: the rows "Road map" and "A zero among the digits", and the two tips about the direct road and digits with a zero.

**Kept (plan):** "Which is the base?" slide, guided q-r26-t28-05 (mailboxes), practice -16 and the card row "Objects into boxes".

**Restored:**
- Practice wp28-p04, wp28-p07 and wp28-p13 (original text, solutions in TeX with the numbers shown), in the practice order by difficulty.
- The true "rare" lines: wp-134 slide 2 "Rare and hard" (the original slide; its last line also says that probability uses this idea); wp-134 slide 4 "Subtracting possibilities is even rarer."; wp-137 slide 2 "…Very hard, and very rare."
- alg-extra-unit-t18-3-4 comes from T18 (the T18 patch moves it). It is first in the T28 practice order, the easiest question.

**Summary lesson added:** `r26-t28-summary` "Summary" (about 2.2 minutes). It is at the end of "Further guided examples", after the advanced card and right before the practice. Slides: Summary · Stages: multiply · Repetition and rows · Counted twice? · Who stays out · Cases · Objects into boxes · Together and apart · Before you practice (the 5 checklist questions; traps: adding instead of multiplying, dividing without a reason, a zero that leads a number).
